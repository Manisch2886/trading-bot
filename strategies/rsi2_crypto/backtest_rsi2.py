"""
Backtest-Engine: RSI-2 Mean-Reversion Krypto (nach Larry Connors)
================================================================================
Long-only, Krypto, TAGESBASIS (bewusste Zeitrahmen-Entscheidung, siehe
PROTOTYPE_FINDINGS.md Abschnitt 0 - RSI-2 ist als Mean-Reversion-Strategie
auf Tagesdaten konzipiert und validiert; die Elliott-Wave-Krypto/T3-
SuperTrend-Bots laufen bewusst auf 1h/4h, aber das ist fuer eine andere
Strategiefamilie (Trendfolge/Wellenmuster) optimiert, nicht fuer Connors'
Mean-Reversion-Logik).

Identisches Grundgeruest zu rsi2_mean_reversion/backtest_rsi2.py
(eigenstaendige Kopie, Architektur-Prinzip), mit EINER wichtigen
Erweiterung: SMA_TREND_PERIOD ist hier ein Parameter (nicht fest auf 200),
weil Krypto historisch volatiler ist als Aktien und der Trendfilter fuer
Krypto empirisch neu kalibriert werden muss (siehe multi_symbol_optimise.py)
statt den Aktien-Wert unveraendert zu uebernehmen.

WICHTIG - Krypto vs. Aktien, was sich NICHT aendert: Krypto handelt 24/7,
d.h. bei TAGESKERZEN gibt es (anders als bei Aktien mit Wochenenden/
Feiertagen) an JEDEM Kalendertag eine Kerze - "Handelstage" und
"Kalendertage" fallen bei diesem Zeitrahmen fuer Krypto zusammen. Das macht
die Zeit-Exit-Logik hier sogar EINFACHER/eindeutiger als bei Aktien, nicht
komplizierter - der in der Anfrage befuerchtete "Stunden/Perioden statt
Handelstage"-Umrechnungsbedarf entfaellt durch die Tagesbasis-Entscheidung.

REGELN (identisch zur Aktien-Version, SMA_TREND_PERIOD als Parameter):

1. TRENDFILTER: Schlusskurs > SMA(SMA_TREND_PERIOD) des Schlusskurses.
2. EINSTIEG: Trendfilter erfuellt UND RSI(2) < RSI_THRESHOLD. Einstieg zum
   Schlusskurs des Signaltags. Kein Pyramiding.
3. AUSSTIEG - Prioritaet pro Tag:
   a) STOP-LOSS (falls aktiv) - Tagestief <= Stop-Kurs
   b) SMA-EXIT - Schlusskurs > SMA(5)
   c) ZEIT-EXIT - spaetestens nach MAX_HOLD_DAYS (10) Tagen, zum Schlusskurs
4. STOP-LOSS: wie bei der Aktien-Version empirisch getestet (kein Stop vs.
   feste Prozentwerte), nicht blind angenommen.

Kosten: 0.1% Gebuehr + 0.05% Slippage je Entry/Exit (Binance-Spot-Konvention,
gleiche Annahme wie bei den bestehenden Krypto-Bots).
"""

import numpy as np
import pandas as pd

from indicators import sma, rsi

RSI_PERIOD = 2
SMA_EXIT_PERIOD = 5
MAX_HOLD_DAYS = 10

TRADING_FEE_PCT = 0.1
SLIPPAGE_PCT = 0.05


def compute_indicators(price_df: pd.DataFrame, sma_trend_period: int) -> pd.DataFrame:
    df = price_df.sort_values("open_time").reset_index(drop=True).copy()
    df["sma_trend"] = sma(df["close"], sma_trend_period)
    df["sma_exit"] = sma(df["close"], SMA_EXIT_PERIOD)
    df["rsi"] = rsi(df["close"], RSI_PERIOD)
    return df


def run_backtest(price_df: pd.DataFrame, rsi_threshold: float, sma_trend_period: int,
                  stop_loss_pct: float = None, entry_cutoff=None) -> pd.DataFrame:
    df = price_df
    close = df["close"].to_numpy()
    low = df["low"].to_numpy()
    sma_trend = df["sma_trend"].to_numpy()
    sma_exit = df["sma_exit"].to_numpy()
    rsi_arr = df["rsi"].to_numpy()
    open_time = df["open_time"].to_numpy()
    n = len(df)

    start_i = sma_trend_period
    if entry_cutoff is not None:
        start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))

    trades = []
    i = start_i
    while i < n:
        if np.isnan(sma_trend[i]) or np.isnan(rsi_arr[i]):
            i += 1
            continue

        if not (close[i] > sma_trend[i] and rsi_arr[i] < rsi_threshold):
            i += 1
            continue

        entry_time = open_time[i]
        entry_price = close[i]
        entry_rsi = rsi_arr[i]
        stop_price = entry_price * (1 - stop_loss_pct / 100) if stop_loss_pct is not None else None

        exit_idx, exit_price, result = None, None, None
        max_offset = min(MAX_HOLD_DAYS, n - 1 - i)
        for offset in range(1, max_offset + 1):
            idx = i + offset
            if stop_price is not None and low[idx] <= stop_price:
                exit_idx, exit_price, result = idx, stop_price, "stop_loss"
                break
            if not np.isnan(sma_exit[idx]) and close[idx] > sma_exit[idx]:
                exit_idx, exit_price, result = idx, close[idx], "sma_exit"
                break
            if offset == MAX_HOLD_DAYS:
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
                "holding_days": holding_days, "rsi_at_entry": round(float(entry_rsi), 2),
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
    df = compute_indicators(price_df, sma_trend_period=200)
    trades = run_backtest(df, rsi_threshold=5.0, sma_trend_period=200, stop_loss_pct=5.0)

    print(f"BTCUSDT: {len(trades)} Trades gefunden.\n")
    if not trades.empty:
        win_rate = (trades["pnl_pct"] > 0).mean() * 100
        print(f"Win Rate: {win_rate:.1f}%  |  Ø PnL: {trades['pnl_pct'].mean():.2f}%  |  "
              f"Ø Haltedauer: {trades['holding_days'].mean():.1f} Tage")
