"""
2022-Stress-Perioden-Vergleich ("Krypto-Winter") ueber alle vier Krypto-Bots
================================================================================
Leitfrage der Nutzeranfrage: wiederholt sich die bei der Aktien-Version von
Volatility Breakout gefundene Baerenmarkt-Schwaeche (siehe
results/volatility_breakout/PROTOTYPE_FINDINGS.md Abschnitt 10) auch im
Krypto-Baerenmarkt 2022, oder verhaelt sich die Strategie dort anders?
Vergleicht alle vier Krypto-Bots (2 etablierte Live-Bots + 2 neue
Prototypen) im selben Fenster, gleiche Methodik wie
volatility_breakout/stress_period_comparison.py.
"""

import os
import pandas as pd

BASE_DIR = "/home/user/trading-bot"

CURVES = {
    "Elliott Wave (Krypto, live)": os.path.join(BASE_DIR, "results", "equity_curve.csv"),
    "T3/SuperTrend (Krypto, live)": os.path.join(BASE_DIR, "results", "t3_supertrend", "equity_curve.csv"),
    "RSI-2 Mean-Reversion (Krypto, Prototyp, neu)": os.path.join(BASE_DIR, "results", "rsi2_crypto", "equity_curve.csv"),
    "Volatility Breakout (Krypto, Prototyp, neu)": os.path.join(BASE_DIR, "results", "volatility_breakout_crypto", "equity_curve.csv"),
}

STRESS_PERIOD_START = "2022-01-01"
STRESS_PERIOD_END = "2022-12-31"


def build_daily_capital_curve(csv_path: str, starting_capital: float = 10_000.0) -> pd.Series:
    df = pd.read_csv(csv_path, parse_dates=["time"]).sort_values("time")
    df["date"] = df["time"].dt.normalize()
    daily_last = df.groupby("date")["capital_after"].last()
    full_range = pd.date_range(daily_last.index.min(), daily_last.index.max(), freq="D")
    daily_last = daily_last.reindex(full_range).ffill()
    if pd.isna(daily_last.iloc[0]):
        daily_last.iloc[0] = starting_capital
    return daily_last


def main():
    curves = {}
    for label, path in CURVES.items():
        if not os.path.exists(path):
            print(f"Fehlt (erst equity_simulation.py ausfuehren): {label} -> {path}")
            continue
        curves[label] = build_daily_capital_curve(path)

    print("Verfuegbare Zeitraeume je Bot:")
    for label, series in curves.items():
        print(f"  {label}: {series.index.min().date()} bis {series.index.max().date()}")

    stress_start = pd.Timestamp(STRESS_PERIOD_START)
    stress_end = pd.Timestamp(STRESS_PERIOD_END)

    print("\n" + "=" * 100)
    print(f"STRESS-PERIODE {STRESS_PERIOD_START} bis {STRESS_PERIOD_END} (KRYPTO-WINTER) - JE BOT")
    print("=" * 100)

    rows = []
    for label, series in curves.items():
        window = series[(series.index >= stress_start) & (series.index <= stress_end)]
        if window.empty:
            rows.append({"bot": label, "rendite_2022_pct": None, "max_dd_2022_pct": None})
            continue
        start_cap = window.iloc[0]
        end_cap = window.iloc[-1]
        running_max = window.cummax()
        dd = ((window - running_max) / running_max * 100).min()
        rendite = (end_cap / start_cap - 1) * 100

        running_max_all = series.cummax()
        dd_all_time = ((series - running_max_all) / running_max_all * 100).min()

        rows.append({
            "bot": label, "start_kapital": round(start_cap, 2), "end_kapital": round(end_cap, 2),
            "rendite_2022_pct": round(rendite, 2), "max_dd_2022_pct": round(dd, 2),
            "allzeit_max_dd_pct": round(dd_all_time, 2),
        })

    stress_df = pd.DataFrame(rows)
    print(stress_df.to_string(index=False))

    normalised_stress = pd.DataFrame({
        label: series[(series.index >= stress_start) & (series.index <= stress_end)]
        for label, series in curves.items()
    }).dropna()

    print("\n" + "=" * 100)
    print("GLEICHGEWICHTETE 4-KRYPTO-BOT-KOMBINATION WAEHREND DER STRESS-PERIODE")
    print("=" * 100)
    if normalised_stress.empty:
        print("Keine gemeinsame Datenbasis fuer alle vier Bots waehrend der Stress-Periode.")
    else:
        norm = normalised_stress / normalised_stress.iloc[0] * 100
        portfolio = norm.mean(axis=1)
        running_max = portfolio.cummax()
        portfolio_dd = ((portfolio - running_max) / running_max * 100).min()
        portfolio_return = (portfolio.iloc[-1] / portfolio.iloc[0] - 1) * 100
        print(f"Rendite: {portfolio_return:.2f}%  |  Max Drawdown: {portfolio_dd:.2f}%")

    os.makedirs(os.path.join(BASE_DIR, "results", "volatility_breakout_crypto"), exist_ok=True)
    stress_df.to_csv(os.path.join(BASE_DIR, "results", "volatility_breakout_crypto",
                                   "stress_period_2022_crypto_family.csv"), index=False)
    print(f"\nGespeichert unter: {BASE_DIR}/results/volatility_breakout_crypto/stress_period_2022_crypto_family.csv")


if __name__ == "__main__":
    main()
