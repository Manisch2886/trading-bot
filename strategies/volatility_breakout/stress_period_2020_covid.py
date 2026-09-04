"""
Zweiter unabhaengiger Stresstest: COVID-Crash Februar-April 2020
========================================================================
Ergaenzt stress_period_comparison.py (2022) um ein zweites, unabhaengiges
Stress-Fenster: den schnellen, extremen Markt-Einbruch Februar-April 2020.
Leitfrage: Wiederholt sich das 2022-Muster (Volatility Breakout schwaechster
Bot, Drawdown nahe am Allzeit-Extrem) auch hier, oder war 2022 ein
Einzelfall?

WICHTIG - Datenbasis-Einschraenkung: Die beiden Krypto-Bots (Elliott Wave
Krypto, T3/SuperTrend Krypto) haben erst ab ca. September 2021 Kursdaten
(siehe stress_period_comparison.py-Ausgabe) - sie sind fuer 2020 NICHT
auswertbar und werden hier bewusst ausgelassen statt mit falschen/leeren
Werten aufgefuehrt. Der Vergleich beschraenkt sich auf die drei
Aktien-Bots mit Historie bis mindestens 2016 (Elliott Wave Aktien, RSI-2,
Volatility Breakout).
"""

import os
import pandas as pd

BASE_DIR = "/home/user/trading-bot"

CURVES = {
    "Elliott Wave (Aktien)": os.path.join(BASE_DIR, "results", "elliott_wave_stocks", "equity_curve.csv"),
    "RSI-2 Mean-Reversion (Aktien, Prototyp)": os.path.join(BASE_DIR, "results", "rsi2_mean_reversion", "equity_curve.csv"),
    "Volatility Breakout (Aktien, Prototyp, neu)": os.path.join(BASE_DIR, "results", "volatility_breakout", "equity_curve.csv"),
}

STRESS_PERIOD_START = "2020-02-01"
STRESS_PERIOD_END = "2020-04-30"


def build_daily_capital_curve(csv_path: str, starting_capital: float = 10_000.0) -> pd.Series:
    df = pd.read_csv(csv_path, parse_dates=["time"]).sort_values("time")
    df["date"] = df["time"].dt.normalize()
    daily_last = df.groupby("date")["capital_after"].last()
    full_range = pd.date_range(daily_last.index.min(), daily_last.index.max(), freq="D")
    daily_last = daily_last.reindex(full_range).ffill()
    if pd.isna(daily_last.iloc[0]):
        daily_last.iloc[0] = starting_capital
    return daily_last


def load_trade_stats(csv_path: str, start: pd.Timestamp, end: pd.Timestamp) -> dict:
    """Trade-Anzahl und Win Rate der EINZELNEN Trades (nicht Portfolio-
    Kapitalkurve) mit Exit im Fenster - fuer Volatility Breakout zusaetzlich
    zur Kapitalkurve ausgewertet (Aufgabe 1: exakt wie beim 2022-Vergleich)."""
    df = pd.read_csv(csv_path, parse_dates=["time"])
    window = df[(df["time"] >= start) & (df["time"] <= end)]
    if window.empty:
        return {"n_trades": 0, "win_rate_pct": None}
    win_rate = round((window["pnl_pct"] > 0).mean() * 100, 1)
    return {"n_trades": len(window), "win_rate_pct": win_rate}


def main():
    curves = {}
    for label, path in CURVES.items():
        if not os.path.exists(path):
            print(f"Fehlt (erst equity_simulation.py ausfuehren): {label} -> {path}")
            continue
        curves[label] = build_daily_capital_curve(path)

    print("Verfuegbare Zeitraeume je Bot (nur Aktien-Bots, s. Docstring):")
    for label, series in curves.items():
        print(f"  {label}: {series.index.min().date()} bis {series.index.max().date()}")

    stress_start = pd.Timestamp(STRESS_PERIOD_START)
    stress_end = pd.Timestamp(STRESS_PERIOD_END)
    print(f"\nStress-Fenster: {STRESS_PERIOD_START} bis {STRESS_PERIOD_END} (COVID-Crash)")

    print("\n" + "=" * 90)
    print(f"STRESS-PERIODE {STRESS_PERIOD_START} bis {STRESS_PERIOD_END} - JE BOT (Kapitalkurve)")
    print("=" * 90)

    rows = []
    for label, series in curves.items():
        window = series[(series.index >= stress_start) & (series.index <= stress_end)]
        if window.empty:
            rows.append({"bot": label, "start_kapital": None, "end_kapital": None,
                         "rendite_pct": None, "max_drawdown_pct": None})
            continue
        start_cap = window.iloc[0]
        end_cap = window.iloc[-1]
        running_max = window.cummax()
        dd = ((window - running_max) / running_max * 100).min()
        rendite = (end_cap / start_cap - 1) * 100
        rows.append({
            "bot": label, "start_kapital": round(start_cap, 2), "end_kapital": round(end_cap, 2),
            "rendite_pct": round(rendite, 2), "max_drawdown_pct": round(dd, 2),
        })

    stress_df = pd.DataFrame(rows)
    print(stress_df.to_string(index=False))

    # Zusaetzlich: Trade-Ebene (Anzahl, Win Rate) je Bot im Fenster - wie in
    # Aufgabe 1 gefordert, exakt wie beim 2022-Vergleich (der ebenfalls
    # Trade-Anzahl/Win-Rate mit auswertet, siehe PROTOTYPE_FINDINGS.md Abschnitt 8).
    print("\n" + "=" * 90)
    print("TRADE-EBENE IM FENSTER (Exit-Datum im Fenster, alle drei Aktien-Bots)")
    print("=" * 90)
    trade_rows = []
    for label, path in CURVES.items():
        if not os.path.exists(path):
            continue
        stats = load_trade_stats(path, stress_start, stress_end)
        trade_rows.append({"bot": label, **stats})
    print(pd.DataFrame(trade_rows).to_string(index=False))

    # Allzeit-Max-Drawdown je Bot (fuer den direkten Vergleich mit dem
    # Fenster-Drawdown oben, wie in Abschnitt 8/PROTOTYPE_FINDINGS.md bereits
    # fuer 2022 dokumentiert).
    print("\n" + "=" * 90)
    print("ZUM VERGLEICH: ALLZEIT-MAX-DRAWDOWN JE BOT (gesamte verfuegbare Historie)")
    print("=" * 90)
    for label, series in curves.items():
        running_max = series.cummax()
        dd_all = ((series - running_max) / running_max * 100).min()
        print(f"  {label}: {dd_all:.2f}%")

    os.makedirs(os.path.join(BASE_DIR, "results", "volatility_breakout"), exist_ok=True)
    stress_df.to_csv(os.path.join(BASE_DIR, "results", "volatility_breakout",
                                   "stress_period_comparison_2020_covid.csv"), index=False)
    print(f"\nGespeichert unter: {BASE_DIR}/results/volatility_breakout/stress_period_comparison_2020_covid.csv")


if __name__ == "__main__":
    main()
