"""
Backtest-Engine: Bollinger-Band-Squeeze-Breakout
=========================================================
Long-only, Aktien, Tagesbasis. Wie bei RSI-2 kein vorab erkanntes
Muster wie bei den Elliott-Wave-Bots - der Backtest scannt Tag fuer Tag
(Zustandsautomat pro Symbol: "in Position" oder nicht), auf NumPy-Arrays
(Performance-Lehre aus rsi2_mean_reversion/backtest_rsi2.py von Anfang an
beruecksichtigt statt erst nachtraeglich behoben).

REGELN (exakt, keine Mehrdeutigkeit):

1. SQUEEZE-ERKENNUNG:
   Bollinger-Band-Breite (Periode 20, 2 Standardabweichungen) faellt auf
   ein rollierendes 126-Tage-Tief: Breite liegt im untersten Quartil
   (<= 25.-Perzentil) der Breite der letzten 126 Handelstage (inkl.
   aktuellem Tag). SQUEEZE_LOOKBACK_DAYS und SQUEEZE_PERCENTILE sind
   Parameter, Startwerte 126 / 25 - werden in multi_symbol_optimise.py
   testweise variiert.

2. EINSTIEGS-TRIGGER (Long-only, wie alle Aktien-Bots im Projekt):
   Squeeze war am VORTAG (t-1) aktiv UND der Schlusskurs von HEUTE (t)
   liegt ueber dem oberen Bollinger-Band von HEUTE. Der Ein-Tage-Versatz
   (Squeeze gestern, Ausbruch heute) ist eine bewusste, explizite
   Festlegung - vermeidet die Mehrdeutigkeit "was, wenn Breite und
   Ausbruch am selben Tag zusammenfallen" vollstaendig, da beide Werte
   dann aus unterschiedlichen, eindeutig sortierten Tagen stammen.
   Einstieg zum SCHLUSSKURS DES AUSBRUCHSTAGS (dieselbe Konvention wie bei
   RSI-2 - Standard bei Tages-Bar-Backtests, fuer eine spaetere Live-
   Umsetzung durch den tatsaechlich verfuegbaren Kurs zu ersetzen).
   Optionaler Volumen-Bestaetigungsfilter (siehe Punkt 4): falls aktiv,
   zusaetzliche Bedingung Volumen(t) > VOLUME_FILTER_MULTIPLIER * 20-Tage-
   Durchschnittsvolumen(t).
   Kein Pyramiding - waehrend eine Position in einem Symbol offen ist,
   werden fuer dieses Symbol keine neuen Einstiegssignale gesucht.

3. AUSSTIEG - "was zuerst eintritt", explizite Prioritaet pro Tag (ab dem
   ersten Handelstag NACH dem Einstiegstag):
   a) STOP-LOSS - Tagestief <= Stop-Kurs (initial STOP_LOSS_PCT unter
      Einstieg, Startwert 5%).
   b) TRAILING-ELEMENT - bewusst NICHT Teil der Basis-Regel. Trailing-
      Take-Profit hat sich beim Aktien-Elliott-Wave-Bot als Overfitting
      erwiesen (sah im Gesamtzeitraum gut aus, hielt der Out-of-Sample-
      Pruefung nicht stand) - wird hier NICHT blind uebernommen, sondern
      separat und skeptisch in experiment_trailing_stop.py getestet, mit
      identischer OOS-Sorgfalt.
   c) ZEIT-EXIT - spaetestens nach MAX_HOLD_DAYS (Startwert 15) Handelstagen
      nach dem Einstiegstag, zum Schlusskurs dieses Tages. 15 Tage statt
      RSI-2s 10 Tage, weil Ausbruchsbewegungen tendenziell laenger laufen
      als Mean-Reversion-Trades.
   Auf einem Tag zaehlt immer nur die zuerst zutreffende Bedingung (a vor
   c fuer die Basis-Regel ohne Trailing).

4. FALSE-BREAKOUT-FILTER (Volumen-Bestaetigung):
   Fehlausbrueche sind die bekannte Hauptschwaeche von Breakout-Strategien.
   Vorschlag: Ausbruchstag-Volumen muss mindestens VOLUME_FILTER_MULTIPLIER
   (Startwert 1.5) mal so hoch sein wie das 20-Tage-Durchschnittsvolumen -
   hoheres Volumen beim Ausbruch gilt in der TA-Literatur als Zeichen
   echter, breiter getragener Kaufkraft statt eines duennen Fehlsignals.
   Wird NICHT blind fest eingebaut, sondern in experiment_false_breakout_
   filter.py mit/ohne verglichen (Win Rate, Ø PnL), bevor eine Empfehlung
   fuer den Standardwert von USE_VOLUME_FILTER erfolgt.

Kosten: dieselbe Konvention wie bei den anderen Aktien-Bots (0.1% Gebuehr +
0.05% Slippage, je einmal fuer Entry und Exit).
"""

import numpy as np
import pandas as pd

from indicators import bollinger_bands, band_width, squeeze_threshold

BB_PERIOD = 20
BB_NUM_STD = 2.0
SQUEEZE_LOOKBACK_DAYS = 126
SQUEEZE_PERCENTILE = 25.0
VOLUME_AVG_PERIOD = 20
VOLUME_FILTER_MULTIPLIER = 1.5
MAX_HOLD_DAYS = 15  # Handelstage NACH dem Einstiegstag, keine Kalenderzeit

TRADING_FEE_PCT = 0.1
SLIPPAGE_PCT = 0.05

# Mindest-Vorlauf, bevor irgendein Indikator gueltig sein kann
WARMUP_PERIOD = max(BB_PERIOD, SQUEEZE_LOOKBACK_DAYS, VOLUME_AVG_PERIOD)


def compute_indicators(price_df: pd.DataFrame, squeeze_lookback_days: int = SQUEEZE_LOOKBACK_DAYS,
                        squeeze_percentile: float = SQUEEZE_PERCENTILE) -> pd.DataFrame:
    """Berechnet alle Indikatoren auf der VOLLEN Kurshistorie (nicht erst
    nach einer Zeitraum-Kappung) - der 126-Tage-Squeeze-Vorlauf braucht
    genug Vorgeschichte, sonst waeren die ersten ~126 Tage jedes
    Auswertungsfensters ohne gueltigen Squeeze-Status (NaN)."""
    df = price_df.sort_values("open_time").reset_index(drop=True).copy()
    df["bb_middle"], df["bb_upper"], df["bb_lower"] = bollinger_bands(df["close"], BB_PERIOD, BB_NUM_STD)
    df["bb_width"] = band_width(df["bb_middle"], df["bb_upper"], df["bb_lower"])
    df["squeeze_thresh"] = squeeze_threshold(df["bb_width"], squeeze_lookback_days, squeeze_percentile)
    df["is_squeeze"] = df["bb_width"] <= df["squeeze_thresh"]
    df["vol_avg"] = df["volume"].rolling(window=VOLUME_AVG_PERIOD).mean()
    return df


def run_backtest(price_df: pd.DataFrame, stop_loss_pct: float = 5.0, entry_cutoff=None,
                  max_hold_days: int = MAX_HOLD_DAYS, use_volume_filter: bool = False,
                  volume_filter_multiplier: float = VOLUME_FILTER_MULTIPLIER) -> pd.DataFrame:
    """Laeuft Tag fuer Tag durch die Kursreihe (Indikatoren muessen bereits
    berechnet sein, siehe compute_indicators). entry_cutoff (optional):
    Einstiege vor diesem Zeitpunkt werden verworfen UND der Scan startet
    direkt dort."""
    df = price_df
    close = df["close"].to_numpy()
    low = df["low"].to_numpy()
    volume = df["volume"].to_numpy()
    vol_avg = df["vol_avg"].to_numpy()
    upper = df["bb_upper"].to_numpy()
    is_squeeze = df["is_squeeze"].to_numpy()
    open_time = df["open_time"].to_numpy()
    n = len(df)

    start_i = WARMUP_PERIOD + 1  # +1, da Punkt 2 den Squeeze-Status von t-1 braucht
    if entry_cutoff is not None:
        start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))

    trades = []
    i = start_i
    while i < n:
        if np.isnan(upper[i]) or np.isnan(close[i]):
            i += 1
            continue

        squeeze_yesterday = bool(is_squeeze[i - 1])
        breakout_today = close[i] > upper[i]

        if not (squeeze_yesterday and breakout_today):
            i += 1
            continue

        if use_volume_filter:
            if np.isnan(vol_avg[i]) or volume[i] <= volume_filter_multiplier * vol_avg[i]:
                i += 1
                continue

        entry_time = open_time[i]
        entry_price = close[i]
        stop_price = entry_price * (1 - stop_loss_pct / 100) if stop_loss_pct is not None else None

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
            break  # nicht genug Restdaten, um diese Position zu schliessen - Scan beenden

        if entry_cutoff is None or entry_time >= np.datetime64(entry_cutoff):
            pnl_pct = (exit_price - entry_price) / entry_price * 100
            total_cost_pct = 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)
            holding_days = (pd.Timestamp(open_time[exit_idx]) - pd.Timestamp(entry_time)).days
            trades.append({
                "entry_time": pd.Timestamp(entry_time), "entry_price": entry_price,
                "exit_time": pd.Timestamp(open_time[exit_idx]), "exit_price": exit_price,
                "result": result, "pnl_pct": round(pnl_pct - total_cost_pct, 2),
                "holding_days": holding_days,
            })

        i = exit_idx + 1  # kein Pyramiding

    return pd.DataFrame(trades)


if __name__ == "__main__":
    import os
    import sys
    _STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
    _SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
    sys.path.insert(0, _SHARED_DIR)
    from strategy_paths import get_strategy_paths
    _P = get_strategy_paths(__file__)

    price_df = pd.read_csv(os.path.join(_P["DATA_DIR"], "AAPL_1d.csv"), parse_dates=["open_time"])
    df = compute_indicators(price_df)
    trades = run_backtest(df, stop_loss_pct=5.0)

    print(f"AAPL: {len(trades)} Trades gefunden.\n")
    if not trades.empty:
        win_rate = (trades["pnl_pct"] > 0).mean() * 100
        print(f"Win Rate: {win_rate:.1f}%  |  Ø PnL: {trades['pnl_pct'].mean():.2f}%  |  "
              f"Ø Haltedauer: {trades['holding_days'].mean():.1f} Tage")
