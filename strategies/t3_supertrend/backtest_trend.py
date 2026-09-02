"""
Backtest der T3/ADX/SuperTrend-Trendfolgestrategie
========================================================
Handelslogik (bereinigte, saubere Version der Pine-Script-Vorlage):

EINSTIEG (Long-only, wie bei der Elliott-Wave-Strategie):
- T3 Fast kreuzt T3 Slow von unten nach oben (Aufwaertssignal)
- UND ADX > Schwelle (echter Trend, keine Seitwaertsphase)

AUSSTIEG (trailing statt festem Kursziel - typisch fuer Trendfolge):
- SuperTrend dreht von Aufwaerts- auf Abwaertstrend, ODER
- T3 Fast kreuzt T3 Slow von oben nach unten, ODER
- Stop-Loss wird erreicht (NEU ggue. Original: dort gab es keinen
  expliziten Stop-Loss, nur die beiden trailing-Bedingungen oben -
  das liess Verluste im Ernstfall unbegrenzt laufen)

WICHTIG: Anders als bei Mean-Reversion/Elliott-Wave gibt es hier
bewusst KEIN festes Take-Profit-Ziel - Trendfolge will Gewinne
laufen lassen, solange der Trend haelt.
"""

import pandas as pd

from indicators import compute_indicators

# Trading-Kosten (gleiche Annahmen wie bei der Elliott-Wave-Strategie)
TRADING_FEE_PCT = 0.1
SLIPPAGE_PCT = 0.05

# Standard-Parameter (Ausgangspunkt fuer die Optimierung)
T3_FAST_LENGTH = 12
T3_SLOW_LENGTH = 25
T3_FACTOR = 0.7
DI_LENGTH = 14
ADX_LENGTH = 14
ADX_THRESHOLD = 25.0
ATR_LENGTH = 22
ATR_MULT = 3.0
STOP_LOSS_PCT = 3.0


def run_backtest(df: pd.DataFrame, t3_fast_length=T3_FAST_LENGTH, t3_slow_length=T3_SLOW_LENGTH,
                  t3_factor=T3_FACTOR, di_length=DI_LENGTH, adx_length=ADX_LENGTH,
                  adx_threshold=ADX_THRESHOLD, atr_length=ATR_LENGTH, atr_mult=ATR_MULT,
                  stop_loss_pct=STOP_LOSS_PCT, use_t3_exit=True, use_vwap_filter=False) -> pd.DataFrame:
    """
    Ein einziger Durchlauf durch die Zeitreihe (Zustandsmaschine:
    entweder in Position oder nicht) - effizienter als ein verschachtelter
    Scan wie bei der ereignisbasierten Elliott-Wave-Strategie, weil
    Trendfolge kontinuierlich beobachtet statt auf diskrete Muster wartet.

    use_vwap_filter: zusaetzliche Bedingung "Preis > VWAP" beim Einstieg.
    WICHTIG: Isolierte Tests auf einem Zeitausschnitt zeigten hoehere
    Trade-Qualitaet (Win Rate, Ø-Gewinn), aber die volle 5-Jahres-
    Equity-Simulation zeigte GERINGERE Gesamtrendite bei gleichem
    Drawdown (weniger Trades = weniger Zinseszins-Effekt). Deshalb
    standardmaessig AUS - bewusste Designentscheidung nach Vergleich.
    """
    data = compute_indicators(df, t3_fast_length, t3_slow_length, t3_factor,
                               di_length, adx_length, atr_length, atr_mult)

    # NumPy-Arrays statt .iloc-Zugriff auf den DataFrame - bei mehreren
    # zehntausend Kerzen spuerbar schneller (Pandas-Overhead je Zeile entfaellt).
    open_time = data["open_time"].to_numpy()
    close = data["close"].to_numpy()
    low = data["low"].to_numpy()
    t3_fast = data["t3_fast"].to_numpy()
    t3_slow = data["t3_slow"].to_numpy()
    adx = data["adx"].to_numpy()
    supertrend_dir = data["supertrend_dir"].to_numpy()
    vwap = data["vwap"].to_numpy()

    trades = []
    position = None  # None oder dict mit entry-Infos

    for i in range(1, len(data)):
        if pd.isna(t3_fast[i]) or pd.isna(t3_slow[i]) or pd.isna(adx[i]):
            continue

        if position is None:
            crossed_up = t3_fast[i - 1] <= t3_slow[i - 1] and t3_fast[i] > t3_slow[i]
            vwap_ok = (not use_vwap_filter) or (not pd.isna(vwap[i]) and close[i] > vwap[i])
            if crossed_up and adx[i] > adx_threshold and vwap_ok:
                entry_price = close[i]
                position = {
                    "entry_time": open_time[i],
                    "entry_price": entry_price,
                    "stop_price": entry_price * (1 - stop_loss_pct / 100),
                }
        else:
            stop_hit = low[i] <= position["stop_price"]
            trend_flip = supertrend_dir[i] == -1 and supertrend_dir[i - 1] == 1
            t3_crossed_down = use_t3_exit and t3_fast[i - 1] >= t3_slow[i - 1] and t3_fast[i] < t3_slow[i]

            if stop_hit or trend_flip or t3_crossed_down:
                exit_price = position["stop_price"] if stop_hit else close[i]
                result = "stop_loss" if stop_hit else ("trend_flip" if trend_flip else "t3_crossunder")

                pnl_pct = (exit_price - position["entry_price"]) / position["entry_price"] * 100
                pnl_pct -= 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)  # Gebuehren/Slippage wie Elliott-Wave-Bot

                trades.append({
                    "entry_time": position["entry_time"],
                    "entry_price": position["entry_price"],
                    "exit_time": open_time[i],
                    "exit_price": exit_price,
                    "result": result,
                    "pnl_pct": round(pnl_pct, 2),
                })
                position = None

    return pd.DataFrame(trades)


def print_summary(trades: pd.DataFrame):
    if trades.empty:
        print("Keine Trades ausgefuehrt.")
        return

    total_trades = len(trades)
    win_rate = (trades["pnl_pct"] > 0).mean() * 100
    total_return = trades["pnl_pct"].sum()
    avg_return = trades["pnl_pct"].mean()

    cum_returns = trades["pnl_pct"].cumsum()
    max_drawdown = (cum_returns - cum_returns.cummax()).min()

    print(f"Anzahl Trades:        {total_trades}")
    print(f"Win Rate:              {win_rate:.1f}%")
    print(f"Summe PnL (%):         {total_return:.2f}%")
    print(f"Durchschnitt PnL (%):  {avg_return:.2f}%")
    print(f"Max Drawdown (approx): {max_drawdown:.2f}%")
    print("\nErgebnis-Verteilung:")
    print(trades["result"].value_counts())
