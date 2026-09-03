"""
Backtest-Engine: RSI-2 Mean-Reversion (nach Larry Connors)
================================================================
Long-only, Aktien, Tagesbasis. Keine Wellenerkennung wie bei den Elliott-
Wave-Bots - RSI-2 scannt JEDEN Handelstag auf ein moegliches Signal, daher
laeuft der Backtest hier Tag fuer Tag durch die Kursreihe (Zustandsautomat
pro Symbol: "in Position" oder nicht), statt vorab erkannte Muster zu
simulieren.

PERFORMANCE-HINWEIS: Wie schon beim T3/SuperTrend-Bot dokumentiert
(pandas .iloc-Zugriff in Schleifen ist bei mehreren zehntausend Kerzen
extrem langsam), laeuft der Scan hier auf NumPy-Arrays statt auf
df.iloc()-Zeilenzugriffen. Zusaetzlich beginnt der Scan erst am
entry_cutoff (minus SMA(200)-Vorlauf), nicht am Anfang der gesamten
(bei manchen Aktien 60+ Jahre langen) Kurshistorie - Tage vor dem
Auswertungsfenster koennten ohnehin keine gueltigen Trades liefern.

REGELN (exakt, keine Mehrdeutigkeit - siehe Nutzeranfrage):

1. TRENDFILTER (Vorbedingung fuer einen Einstieg):
   Schlusskurs des aktuellen Tages > SMA(200) des Schlusskurses.

2. EINSTIEG:
   Trendfilter erfuellt UND RSI(2) < RSI_THRESHOLD (Connors nennt 5-10,
   Standardwert hier 5). Einstieg zum SCHLUSSKURS DES SIGNALTAGS (Standard-
   Konvention in der Connors-Literatur und bei Tages-Bar-Backtests generell;
   fuer eine spaetere Live-Umsetzung waere das - wie schon beim Elliott-Wave-
   Bot geschehen (siehe Uebergabeprotokoll, "historischer vs. aktueller
   Preis"-Bugfix) - durch den tatsaechlich verfuegbaren Kurs zum
   Ausfuehrungszeitpunkt zu ersetzen).
   Waehrend eine Position in einem Symbol offen ist, werden fuer dieses
   Symbol KEINE neuen Einstiegssignale gesucht (kein Pyramiding, max. eine
   offene Position pro Symbol gleichzeitig).

3. AUSSTIEG - "je nachdem was zuerst eintritt", explizit in dieser
   Prioritaet PRO TAG geprueft (ab dem ersten Handelstag NACH dem
   Einstiegstag):
   a) STOP-LOSS (falls aktiv, siehe Punkt 4) - Tagestief <= Stop-Kurs.
      Wird zuerst geprueft (Risikokontrolle hat Prioritaet).
   b) SMA-EXIT - Schlusskurs des Tages > SMA(5) des Schlusskurses.
   c) ZEIT-EXIT - spaetestens nach MAX_HOLD_DAYS (10) Handelstagen NACH dem
      Einstiegstag, zum Schlusskurs dieses Tages (analog zur "Balken-Anzahl,
      keine echte Zeitspanne"-Konvention bei den anderen Bots).
   Auf EINEM Tag kann immer nur GENAU EINE dieser drei Bedingungen zum
   Ausstieg fuehren - a) vor b) vor c), falls mehrere technisch zutreffen
   wuerden.

4. STOP-LOSS - EINORDNUNG (Nutzerfrage): Connors selbst verwendet in der
   Grundversion keinen festen Stop-Loss, sondern verlaesst sich auf den
   Zeit-Exit nach spaetestens 10 Tagen. Ein zusaetzlicher harter Stop ist
   trotzdem sinnvoll zu TESTEN (nicht blind anzunehmen) - siehe
   multi_symbol_optimise.py: STOP_LOSS_RANGE testet explizit sowohl "kein
   Stop" (None) als auch feste Prozentwerte gegeneinander, analog zum
   use_take_profit-Muster beim Aktien-Elliott-Wave-Bot. Vorschlag als
   Startwert, falls ein Stop gewuenscht ist: 5% unter Einstieg - etwas
   breiter als die 2-3% der anderen Bots, weil RSI-2 bewusst in kurzfristige
   Volatilitaet hineinkauft (ein zu enger Stop wuerde genau die Bewegung
   ausloesen, die die Strategie ausnutzen will) und die Haltedauer ohnehin
   durch den 10-Tage-Zeit-Exit begrenzt ist.

Kosten: dieselbe Konvention wie bei den bestehenden Bots (0.1% Gebuehr +
0.05% Slippage, je einmal fuer Entry und Exit).
"""

import numpy as np
import pandas as pd

from indicators import sma, rsi

RSI_PERIOD = 2
SMA_TREND_PERIOD = 200
SMA_EXIT_PERIOD = 5
MAX_HOLD_DAYS = 10  # Handelstage NACH dem Einstiegstag, keine Kalenderzeit

TRADING_FEE_PCT = 0.1
SLIPPAGE_PCT = 0.05


def compute_indicators(price_df: pd.DataFrame) -> pd.DataFrame:
    """Berechnet alle Indikatoren auf der VOLLEN Kurshistorie (nicht erst
    nach einer Zeitraum-Kappung) - der SMA(200)-Trendfilter braucht 200
    Handelstage Vorlauf, sonst waeren die ersten ~200 Tage jedes
    Auswertungsfensters ohne gueltigen Trendfilter (NaN)."""
    df = price_df.sort_values("open_time").reset_index(drop=True).copy()
    df["sma_trend"] = sma(df["close"], SMA_TREND_PERIOD)
    df["sma_exit"] = sma(df["close"], SMA_EXIT_PERIOD)
    df["rsi"] = rsi(df["close"], RSI_PERIOD)
    return df


def run_backtest(price_df: pd.DataFrame, rsi_threshold: float,
                  stop_loss_pct: float = None, entry_cutoff=None,
                  max_hold_days: int = MAX_HOLD_DAYS) -> pd.DataFrame:
    """Laeuft Tag fuer Tag durch die Kursreihe (Indikatoren muessen bereits
    berechnet sein, siehe compute_indicators). entry_cutoff (optional):
    Einstiege vor diesem Zeitpunkt werden verworfen UND der Scan startet
    direkt dort (kein Zeitverlust auf Jahrzehnte an ohnehin verworfenen
    Vor-Fenster-Daten). max_hold_days (optional): ueberschreibt den
    Standard-Zeit-Exit (10 Handelstage) - z.B. fuer Experimente mit
    kuerzerer Haltedauer (siehe experiment_capital_bottleneck_v2.py)."""
    df = price_df
    close = df["close"].to_numpy()
    low = df["low"].to_numpy()
    sma_trend = df["sma_trend"].to_numpy()
    sma_exit = df["sma_exit"].to_numpy()
    rsi_arr = df["rsi"].to_numpy()
    open_time = df["open_time"].to_numpy()
    n = len(df)

    start_i = SMA_TREND_PERIOD
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
        max_offset = min(max_hold_days, n - 1 - i)
        for offset in range(1, max_offset + 1):
            idx = i + offset
            if stop_price is not None and low[idx] <= stop_price:
                exit_idx, exit_price, result = idx, stop_price, "stop_loss"
                break
            if not np.isnan(sma_exit[idx]) and close[idx] > sma_exit[idx]:
                exit_idx, exit_price, result = idx, close[idx], "sma_exit"
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
                "holding_days": holding_days, "rsi_at_entry": round(float(entry_rsi), 2),
            })

        i = exit_idx + 1  # kein Pyramiding - naechster Scan erst nach dem Ausstieg dieser Position

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
    trades = run_backtest(df, rsi_threshold=5.0, stop_loss_pct=5.0)

    print(f"AAPL: {len(trades)} Trades gefunden.\n")
    if not trades.empty:
        win_rate = (trades["pnl_pct"] > 0).mean() * 100
        print(f"Win Rate: {win_rate:.1f}%  |  Ø PnL: {trades['pnl_pct'].mean():.2f}%  |  "
              f"Ø Haltedauer: {trades['holding_days'].mean():.1f} Tage")
