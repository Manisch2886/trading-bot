"""
Backtest-Engine: Relative-Strength-Pair-Rotation (Aktien)
================================================================================
Long-only, Aktien, Tagesbasis. Rotiert innerhalb eines festen Aktien-Paares
(A, B) fortlaufend zwischen den beiden Assets - anders als RSI-2/Volatility
Breakout KEINE diskreten Einzel-Trades mit fixer Max-Haltedauer, sondern
eine kontinuierliche Allokations-Umschaltung, die bis zum naechsten
Rotations-Signal, Stop-Loss oder einer Entkopplungs-Pause laeuft (siehe
Punkt 3 unten - bewusste, dokumentierte Abweichung vom Max-Hold-Muster der
anderen Bots, weil Rotationsstrategien architektonisch anders funktionieren).

REGELN (exakt, keine Mehrdeutigkeit):

1. PAAR-AUSWAHL: siehe pair_discovery.py (Korrelation >= 0.70 ueber die
   252 Handelstage vor dem Auswertungsfenster, statt einer statischen
   Sektor-Zuordnung - Begruendung dort). Die Paar-Liste ist fuer die Dauer
   eines Backtest-Laufs FEST (kein laufendes Neu-Suchen von Paaren
   waehrend des Backtests).

2. ROTATIONS-SIGNAL: taegliche relative Staerke = rollierende
   LOOKBACK_DAYS-Rendite von A minus die von B (indicators.relative_strength).
   Bei jedem REBALANCE-Zeitpunkt (siehe Punkt 3): positiv -> A ist das
   bevorzugte Asset, negativ -> B. Aendert sich das bevorzugte Asset
   gegenueber der aktuellen Position, wird umgeschichtet: aktuelle Position
   (falls vorhanden) zum Schlusskurs schliessen, neue Position im
   bevorzugten Asset zum selben Schlusskurs eroeffnen ("rotation_flip").
   Bei der ALLERERSTEN gueltigen Bewertung (noch keine Position offen)
   wird direkt ins bevorzugte Asset eingestiegen - keine Sonderregel noetig,
   da "aktuelle Position wechseln" bei "keine Position" automatisch zu
   "neu eroeffnen ohne vorheriges Schliessen" wird.

3. REBALANCE-FREQUENZ: taeglich (jeden Handelstag neu bewertet) oder
   woechentlich (alle 5 Handelstage) - beides wird empirisch getestet
   (siehe multi_pair_optimise.py), keine Annahme vorab. "Woechentlich" ist
   ueber eine feste Balken-Anzahl (5) definiert, nicht ueber Kalender-
   Wochentage (robuster gegenueber Feiertagen/fehlenden Handelstagen).
   KEIN fester Zeit-Exit (anders als RSI-2/Volatility Breakout): eine
   Position laeuft, bis a) das Rotations-Signal wechselt, b) der
   Stop-Loss (falls aktiv) greift, oder c) eine Entkopplungs-Pause
   greift (Punkt 4) - architektonisch bedingt (siehe Modul-Docstring).

   STOP-LOSS: taeglich geprueft (unabhaengig von der Rebalance-Frequenz -
   Risikokontrolle hat Prioritaet, analog zur "Stop-Loss zuerst"-Konvention
   bei RSI-2/Volatility Breakout), PRIORITAET VOR dem Rotations-Signal am
   selben Tag. Wird empirisch getestet: kein Stop vs. 8% vs. 12%
   (STOP_LOSS_RANGE in multi_pair_optimise.py), nicht blind angenommen.

4. ENTKOPPLUNGS-SCHUTZ (Hauptrisiko: die Paar-Beziehung bricht strukturell
   auseinander): taeglich geprueft, rollierende 252-Tage-Korrelation der
   taeglichen Renditen (indicators.rolling_correlation, FEST, kein
   Optimierungsparameter). Faellt die Korrelation unter PAUSE_THRESHOLD
   (0.40 - deutlich unter dem 0.70-Auswahl-Schwellenwert, damit ein Paar
   nicht bei jedem kleinen Korrelations-Rueckgang um die Auswahlschwelle
   herum flackert), wird eine eventuell offene Position sofort geschlossen
   ("decoupling_exit") und das Paar pausiert (keine neuen Rotationen).
   Die Pause endet erst, wenn die Korrelation wieder auf RESUME_THRESHOLD
   (0.70 - wieder auf Auswahl-Qualitaet, nicht nur knapp ueber der
   Pause-Schwelle) steigt - Hysterese, um Pendeln an der Schwelle zu
   vermeiden. Wirksamkeit separat getestet in
   experiment_decoupling_protection.py (mit/ohne Vergleich).

Kosten: 0.1% Gebuehr + 0.05% Slippage je Entry/Exit (Projekt-Konvention).
"""

import numpy as np
import pandas as pd

from indicators import relative_strength, rolling_correlation, CORRELATION_WINDOW

LOOKBACK_DAYS = 60          # Default/Startwert, wird in multi_pair_optimise.py mitoptimiert
REBALANCE_DAYS = 5          # 1 = taeglich, 5 = woechentlich - wird mitoptimiert
PAUSE_THRESHOLD = 0.40
RESUME_THRESHOLD = 0.70

TRADING_FEE_PCT = 0.1
SLIPPAGE_PCT = 0.05

WARMUP_PERIOD = CORRELATION_WINDOW  # 252 Tage ist stets der groesste Vorlauf-Bedarf


def compute_pair_indicators(df_a: pd.DataFrame, df_b: pd.DataFrame, lookback_days: int) -> pd.DataFrame:
    """Merged beide Kurshistorien auf gemeinsame Handelstage (inner join)
    und berechnet relative Staerke + rollierende Korrelation."""
    merged = pd.merge(
        df_a[["open_time", "close", "low"]].rename(columns={"close": "close_a", "low": "low_a"}),
        df_b[["open_time", "close", "low"]].rename(columns={"close": "close_b", "low": "low_b"}),
        on="open_time", how="inner",
    ).sort_values("open_time").reset_index(drop=True)

    merged["rel_strength"] = relative_strength(merged["close_a"], merged["close_b"], lookback_days)
    merged["correlation"] = rolling_correlation(merged["close_a"], merged["close_b"])
    return merged


def run_backtest(pair_df: pd.DataFrame, symbol_a: str, symbol_b: str, lookback_days: int,
                  rebalance_days: int, stop_loss_pct: float = None, entry_cutoff=None,
                  use_decoupling_protection: bool = True) -> pd.DataFrame:
    df = pair_df
    close_a = df["close_a"].to_numpy()
    close_b = df["close_b"].to_numpy()
    low_a = df["low_a"].to_numpy()
    low_b = df["low_b"].to_numpy()
    rel_strength = df["rel_strength"].to_numpy()
    correlation = df["correlation"].to_numpy()
    open_time = df["open_time"].to_numpy()
    n = len(df)

    start_i = WARMUP_PERIOD + lookback_days
    if entry_cutoff is not None:
        start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))

    trades = []
    holding = None          # None, 'A' oder 'B'
    entry_idx = None
    entry_price = None
    stop_price = None
    paused = False

    def close_position(exit_i, exit_price, result):
        nonlocal holding, entry_idx, entry_price, stop_price
        pnl_pct = (exit_price - entry_price) / entry_price * 100
        total_cost_pct = 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)
        holding_days = int(exit_i - entry_idx)
        symbol = symbol_a if holding == "A" else symbol_b
        entry_time = open_time[entry_idx]
        if entry_cutoff is None or entry_time >= np.datetime64(entry_cutoff):
            trades.append({
                "symbol": symbol, "entry_time": pd.Timestamp(entry_time), "entry_price": entry_price,
                "exit_time": pd.Timestamp(open_time[exit_i]), "exit_price": exit_price,
                "result": result, "pnl_pct": round(pnl_pct - total_cost_pct, 2),
                "holding_days": holding_days,
            })
        holding, entry_idx, entry_price, stop_price = None, None, None, None

    for i in range(start_i, n):
        if np.isnan(rel_strength[i]) or np.isnan(correlation[i]):
            continue

        # 1) Entkopplungs-Schutz zuerst pruefen (Risikokontrolle hat Prioritaet)
        if use_decoupling_protection:
            if not paused and correlation[i] < PAUSE_THRESHOLD:
                if holding is not None:
                    exit_price = close_a[i] if holding == "A" else close_b[i]
                    close_position(i, exit_price, "decoupling_exit")
                paused = True
            elif paused and correlation[i] >= RESUME_THRESHOLD:
                paused = False

        # 2) Stop-Loss taeglich pruefen (vor dem Rotations-Signal)
        if holding is not None and stop_price is not None:
            current_low = low_a[i] if holding == "A" else low_b[i]
            if current_low <= stop_price:
                close_position(i, stop_price, "stop_loss")

        # 3) Rotations-Signal nur an Rebalance-Zeitpunkten, nur wenn nicht pausiert
        is_rebalance_day = (i - start_i) % rebalance_days == 0
        if not paused and is_rebalance_day:
            favored = "A" if rel_strength[i] > 0 else ("B" if rel_strength[i] < 0 else holding)
            if favored is not None and favored != holding:
                if holding is not None:
                    exit_price = close_a[i] if holding == "A" else close_b[i]
                    close_position(i, exit_price, "rotation_flip")
                holding = favored
                entry_idx = i
                entry_price = close_a[i] if holding == "A" else close_b[i]
                stop_price = entry_price * (1 - stop_loss_pct / 100) if stop_loss_pct is not None else None

    return pd.DataFrame(trades)


if __name__ == "__main__":
    import os
    import sys
    _STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
    _SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
    sys.path.insert(0, _SHARED_DIR)
    from strategy_paths import get_strategy_paths
    _P = get_strategy_paths(__file__)

    df_a = pd.read_csv(os.path.join(_P["DATA_DIR"], "MSFT_1d.csv"), parse_dates=["open_time"])
    df_b = pd.read_csv(os.path.join(_P["DATA_DIR"], "AAPL_1d.csv"), parse_dates=["open_time"])
    pair_df = compute_pair_indicators(df_a, df_b, lookback_days=60)
    trades = run_backtest(pair_df, "MSFT", "AAPL", lookback_days=60, rebalance_days=5, stop_loss_pct=8.0)

    print(f"MSFT/AAPL: {len(trades)} Trades gefunden.\n")
    if not trades.empty:
        win_rate = (trades["pnl_pct"] > 0).mean() * 100
        print(f"Win Rate: {win_rate:.1f}%  |  Ø PnL: {trades['pnl_pct'].mean():.2f}%  |  "
              f"Ø Haltedauer: {trades['holding_days'].mean():.1f} Tage")
        print(trades["result"].value_counts())
