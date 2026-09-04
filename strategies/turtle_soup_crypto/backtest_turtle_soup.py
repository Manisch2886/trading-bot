"""
Backtest-Engine: Turtle Soup (False-Breakout-Reversal, nach Linda Raschke/Larry Williams) - Krypto
================================================================================================================
Long-only, Krypto, Tagesbasis (siehe rsi2_crypto/backtest_rsi2.py-Docstring
fuer die Zeitrahmen-Begruendung - Handelstage=Kalendertage bei 24/7-Krypto).
Eigenstaendige Kopie von turtle_soup_stocks/backtest_turtle_soup.py
(identische Logik, Architektur-Prinzip: kein Cross-Strategy-Import).
Scannt taeglich (kein mehrtaegiges Freshness-Fenster noetig, siehe Punkt 2)
- identisches Grundmuster zu RSI-2/Volatility Breakout: State-Automat pro
Symbol auf NumPy-Arrays
(Performance-Lehre aus rsi2_mean_reversion/backtest_rsi2.py von Anfang an
beruecksichtigt).

REGELN (exakt, keine Mehrdeutigkeit):

1. SETUP-ERKENNUNG: Das Tagestief unterschreitet das rollierende
   DONCHIAN_PERIOD-Tage-Tief (Standardwert 20, wie beim klassischen
   Donchian-Ansatz - wird in multi_symbol_optimise.py mitoptimiert). Das
   Vergleichs-Tief bezieht sich NUR auf die N Tage VOR dem aktuellen Tag
   (kein Blick auf den aktuellen Tag selbst, siehe indicators.donchian_low).

2. EINSTIEGS-TRIGGER - SELBER TAG, nicht Folgetag (explizit begruendete
   Entscheidung):
   Klassischer Turtle Soup ist ein Intraday-Muster: der Kurs unterschreitet
   das N-Tage-Tief WAEHREND des Tages, kehrt aber bis zum Handelsschluss
   ueber dieses Niveau zurueck (Tagestief < Donchian-Tief, ABER
   Schlusskurs > Donchian-Tief - SELBER Balken). Diese Definition wird hier
   uebernommen statt einer "Folgetag-Bestaetigung"-Variante, aus zwei
   Gruenden:
   a) Es ist die textbuchgetreue Original-Definition (Larry Williams'
      "Oops"-Konzept / Linda Raschke: Bruch UND Rueckkehr innerhalb
      desselben Handelstages, nicht ueber mehrere Tage verteilt).
   b) Es passt konsistent zum in diesem Projekt etablierten Muster fuer
      alle taeglich scannenden Bots (RSI-2, Volatility Breakout, Pair-
      Rotation): Signal-Erkennung UND Einstieg basieren auf der jeweils
      LETZTEN verfuegbaren Kerze, kein mehrtaegiges Freshness-Fenster mit
      Status-Tracking (das bei einer "Folgetag-Bestaetigung"-Variante
      noetig waere: wie lange wird auf die Bestaetigung gewartet, bevor
      das Setup verworfen wird? - zusaetzliche, unnoetige Mehrdeutigkeit).
   Einstieg zum SCHLUSSKURS DES SIGNALTAGS (Projekt-Konvention, siehe z.B.
   RSI-2 - fuer eine spaetere Live-Umsetzung durch den tatsaechlich
   verfuegbaren Kurs zu ersetzen).
   Kein Pyramiding - waehrend eine Position offen ist, werden fuer dieses
   Symbol keine neuen Setups gesucht.

3. AUSSTIEG - Prioritaet pro Tag (ab dem ersten Handelstag NACH dem
   Einstiegstag):
   a) STOP-LOSS (falls aktiv) - Tagestief <= Stop-Kurs. ZWEI Varianten
      werden GEGENEINANDER getestet (STOP_MODE_RANGE in
      multi_symbol_optimise.py), nicht blind angenommen:
      - "structural": Stop-Kurs = Tagestief DES SETUP-TAGS selbst (der
        False-Breakout-Tiefpunkt) - strukturell aus dem Muster selbst
        abgeleitet: faellt der Kurs erneut UNTER den gerade
        zurueckeroberten Bereich, ist die Reversal-These entkraeftet.
        Dies ist die im Diskretionaer-/Setup-Trading uebliche
        Stop-Platzierung fuer False-Breakout-Muster (musterspezifisch,
        nicht willkuerlich).
      - fester Prozentsatz unter dem Einstiegspreis (wie bei den anderen
        Bots) - Vergleichswert, um zu pruefen, ob die musterspezifische
        Variante tatsaechlich einen Mehrwert bringt.
      "kein Stop" wird ebenfalls getestet (Konsistenz mit RSI-2/
      Volatility-Breakout-Methodik).
   b) ZEIT-EXIT - spaetestens nach MAX_HOLD_DAYS (Startwert 10, kuerzer
      als Volatility Breakouts 15 - False-Breakout-Reversals sind
      typischerweise kurzlebige Kursreaktionen, keine mehrwoechigen
      Trendbewegungen) Handelstagen, zum Schlusskurs dieses Tages.

Kosten: 0.1% Gebuehr + 0.05% Slippage je Entry/Exit (Projekt-Konvention).
"""

import numpy as np
import pandas as pd

from indicators import donchian_low

DONCHIAN_PERIOD = 20
MAX_HOLD_DAYS = 10

TRADING_FEE_PCT = 0.1
SLIPPAGE_PCT = 0.05

WARMUP_PERIOD = DONCHIAN_PERIOD


def compute_indicators(price_df: pd.DataFrame, donchian_period: int = DONCHIAN_PERIOD) -> pd.DataFrame:
    df = price_df.sort_values("open_time").reset_index(drop=True).copy()
    df["donchian_low"] = donchian_low(df["low"], donchian_period)
    return df


def run_backtest(price_df: pd.DataFrame, stop_mode=None, entry_cutoff=None,
                  max_hold_days: int = MAX_HOLD_DAYS, donchian_period: int = DONCHIAN_PERIOD) -> pd.DataFrame:
    """stop_mode: None ("kein Stop"), "structural" (Setup-Tag-Tief), oder
    ein float (fester Prozentsatz unter Einstieg)."""
    df = price_df
    close = df["close"].to_numpy()
    low = df["low"].to_numpy()
    donchian = df["donchian_low"].to_numpy()
    open_time = df["open_time"].to_numpy()
    n = len(df)

    start_i = WARMUP_PERIOD + donchian_period
    if entry_cutoff is not None:
        start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))

    trades = []
    i = start_i
    while i < n:
        if np.isnan(donchian[i]):
            i += 1
            continue

        setup_triggered = low[i] < donchian[i]
        reversal_confirmed = close[i] > donchian[i]

        if not (setup_triggered and reversal_confirmed):
            i += 1
            continue

        entry_time = open_time[i]
        entry_price = close[i]
        setup_day_low = low[i]

        if stop_mode is None:
            stop_price = None
        elif stop_mode == "structural":
            stop_price = setup_day_low
        else:
            stop_price = entry_price * (1 - stop_mode / 100)

        exit_idx, exit_price, result = None, None, None
        max_offset = min(max_hold_days, n - 1 - i)
        for offset in range(1, max_offset + 1):
            idx = i + offset
            if stop_price is not None and low[idx] <= stop_price:
                exit_idx, exit_price, result = idx, stop_price, "stop_loss"
                break
            if offset == max_hold_days:
                exit_idx, exit_price, result = idx, close[idx], "time_exit"
                break

        if exit_idx is None:
            break

        if entry_cutoff is None or entry_time >= np.datetime64(entry_cutoff):
            pnl_pct = (exit_price - entry_price) / entry_price * 100
            total_cost_pct = 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)
            holding_days = (pd.Timestamp(open_time[exit_idx]) - pd.Timestamp(entry_time)).days
            trades.append({
                "entry_time": pd.Timestamp(entry_time), "entry_price": entry_price,
                "exit_time": pd.Timestamp(open_time[exit_idx]), "exit_price": exit_price,
                "result": result, "pnl_pct": round(pnl_pct - total_cost_pct, 2),
                "holding_days": holding_days, "setup_day_low": setup_day_low,
            })

        i = exit_idx + 1

    return pd.DataFrame(trades)


if __name__ == "__main__":
    import os
    import sys
    _STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
    _SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
    sys.path.insert(0, _SHARED_DIR)
    from strategy_paths import get_strategy_paths
    _P = get_strategy_paths(__file__)

    price_df = pd.read_csv(os.path.join(_P["DATA_DIR"], "BTCUSDT_1d.csv"), parse_dates=["open_time"])
    df = compute_indicators(price_df)
    trades = run_backtest(df, stop_mode="structural")

    print(f"BTCUSDT: {len(trades)} Trades gefunden.\n")
    if not trades.empty:
        win_rate = (trades["pnl_pct"] > 0).mean() * 100
        print(f"Win Rate: {win_rate:.1f}%  |  Ø PnL: {trades['pnl_pct'].mean():.2f}%  |  "
              f"Ø Haltedauer: {trades['holding_days'].mean():.1f} Tage")
        print(trades["result"].value_counts())
