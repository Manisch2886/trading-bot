"""
Stress-Perioden-Vergleich (2022) ueber alle fuenf Bots
============================================================
Analog zu rsi2_mean_reversion/correlation_robustness_check.py, Teil 2 -
"von Anfang an mitgedacht, nicht erst nachtraeglich" wie angefragt: prueft
den neuen Volatility-Breakout-Prototyp direkt gegen die vier bestehenden
Bots waehrend der staerksten Markt-Stressphase im gemeinsamen Fenster
(2022, Krypto-Winter + Fed-Zinserhoehungen) - Rendite und Drawdown JE BOT
waehrend dieses einen Jahres, plus eine hypothetische gleichgewichtete
5-Bot-Kombination (rein zur Einordnung, KEINE echte Kapitalallokation
zwischen Bots).
"""

import os
import pandas as pd

BASE_DIR = "/home/user/trading-bot"

CURVES = {
    "Elliott Wave (Krypto)": os.path.join(BASE_DIR, "results", "equity_curve.csv"),
    "T3/SuperTrend (Krypto)": os.path.join(BASE_DIR, "results", "t3_supertrend", "equity_curve.csv"),
    "Elliott Wave (Aktien)": os.path.join(BASE_DIR, "results", "elliott_wave_stocks", "equity_curve.csv"),
    "RSI-2 Mean-Reversion (Aktien, Prototyp)": os.path.join(BASE_DIR, "results", "rsi2_mean_reversion", "equity_curve.csv"),
    "Volatility Breakout (Aktien, Prototyp, neu)": os.path.join(BASE_DIR, "results", "volatility_breakout", "equity_curve.csv"),
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

    if len(curves) < 2:
        print("Nicht genug Kapitalkurven gefunden fuer einen Vergleich.")
        return

    print("Verfuegbare Zeitraeume je Bot:")
    for label, series in curves.items():
        print(f"  {label}: {series.index.min().date()} bis {series.index.max().date()}")

    common_start = max(s.index.min() for s in curves.values())
    common_end = min(s.index.max() for s in curves.values())
    print(f"\nGemeinsames Vergleichsfenster (alle 5 Bots aktiv): {common_start.date()} bis {common_end.date()}")

    stress_start = pd.Timestamp(STRESS_PERIOD_START)
    stress_end = pd.Timestamp(STRESS_PERIOD_END)
    if stress_start < common_start or stress_end > common_end:
        print(f"\nHinweis: Die Stress-Periode {STRESS_PERIOD_START} bis {STRESS_PERIOD_END} liegt teilweise "
              f"ausserhalb des gemeinsamen 5-Bot-Fensters - Werte unten basieren trotzdem auf der jeweils "
              f"VERFUEGBAREN Kapitalkurve je Bot (nicht auf dem gemeinsamen Fenster), damit auch juengere "
              f"Prototypen wie Volatility Breakout mit einbezogen werden koennen.")

    print("\n" + "=" * 90)
    print(f"STRESS-PERIODE {STRESS_PERIOD_START} bis {STRESS_PERIOD_END} - JE BOT")
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

    # Gleichgewichtete 5-Bot-Kombination NUR fuer Bots mit Daten im gesamten
    # Stress-Fenster (Volatility Breakout ist neu und kann eine kuerzere
    # Historie als 2022 haben - siehe Hinweis oben).
    normalised_stress = pd.DataFrame({
        label: series[(series.index >= stress_start) & (series.index <= stress_end)]
        for label, series in curves.items()
    })
    normalised_stress = normalised_stress.dropna()

    print("\n" + "=" * 90)
    print("GLEICHGEWICHTETE KOMBINATION WAEHREND DER STRESS-PERIODE")
    print("=" * 90)
    if normalised_stress.empty:
        print("Keine gemeinsame Datenbasis fuer alle Bots waehrend der Stress-Periode "
              "(voraussichtlich: Volatility Breakout hat keine Historie bis 2022 zurueck).")
    else:
        included = list(normalised_stress.columns)
        print(f"Enthaltene Bots ({len(included)}): {included}")
        norm = normalised_stress / normalised_stress.iloc[0] * 100
        portfolio = norm.mean(axis=1)
        running_max = portfolio.cummax()
        portfolio_dd = ((portfolio - running_max) / running_max * 100).min()
        portfolio_return = (portfolio.iloc[-1] / portfolio.iloc[0] - 1) * 100
        print(f"Rendite: {portfolio_return:.2f}%  |  Max Drawdown: {portfolio_dd:.2f}%")
        worst_individual = stress_df[stress_df["bot"].isin(included)]["max_drawdown_pct"].min()
        print(f"(schlechtester Einzel-Bot-Drawdown in der Stress-Periode unter den enthaltenen Bots: "
              f"{worst_individual:.2f}%)")

    os.makedirs(os.path.join(BASE_DIR, "results", "volatility_breakout"), exist_ok=True)
    stress_df.to_csv(os.path.join(BASE_DIR, "results", "volatility_breakout",
                                   "stress_period_comparison_2022.csv"), index=False)
    print(f"\nGespeichert unter: {BASE_DIR}/results/volatility_breakout/stress_period_comparison_2022.csv")


if __name__ == "__main__":
    main()
