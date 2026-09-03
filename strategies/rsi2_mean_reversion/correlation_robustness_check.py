"""
Robustere Pruefung der Portfolio-Korrelationsanalyse (auf Rueckfrage)
============================================================================
Zwei gezielte Nachpruefungen der "praktisch unkorreliert"-Werte aus
portfolio_correlation_analysis.py:

1. Wie viele Tage im gemeinsamen Vergleichsfenster hatten TATSAECHLICH
   Trade-Exits in mindestens ZWEI der vier Bots gleichzeitig? Falls das nur
   sehr wenige Tage sind, ist die "unkorreliert"-Aussage der taeglichen
   Rendite-Korrelation grossteils ein mechanischer Effekt duenner
   Handelsaktivitaet, keine belastbare Diversifikations-Evidenz.

2. Wie verhielten sich alle vier Bots WAEHREND der staerksten
   Markt-Stressphase im Fenster (2022, "Krypto-Winter" + Fed-Zinserhoehungen)
   konkret - Rendite und Drawdown JE BOT waehrend dieses einen Jahres?
"""

import os
import pandas as pd

BASE_DIR = "/home/user/trading-bot"

CURVES = {
    "Elliott Wave (Krypto)": os.path.join(BASE_DIR, "results", "equity_curve.csv"),
    "T3/SuperTrend (Krypto)": os.path.join(BASE_DIR, "results", "t3_supertrend", "equity_curve.csv"),
    "Elliott Wave (Aktien)": os.path.join(BASE_DIR, "results", "elliott_wave_stocks", "equity_curve.csv"),
    "RSI-2 Mean-Reversion (Aktien, neu)": os.path.join(BASE_DIR, "results", "rsi2_mean_reversion", "equity_curve.csv"),
}

STRESS_PERIOD_START = "2022-01-01"
STRESS_PERIOD_END = "2022-12-31"


def load_trade_dates(csv_path: str) -> pd.Series:
    df = pd.read_csv(csv_path, parse_dates=["time"])
    return df["time"].dt.normalize()


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
    trade_dates = {}
    curves = {}
    for label, path in CURVES.items():
        if not os.path.exists(path):
            print(f"Fehlt: {label}")
            continue
        trade_dates[label] = load_trade_dates(path)
        curves[label] = build_daily_capital_curve(path)

    common_start = max(s.index.min() for s in curves.values())
    common_end = min(s.index.max() for s in curves.values())
    print(f"Gemeinsames Vergleichsfenster: {common_start.date()} bis {common_end.date()}\n")

    # --- Teil 1: Gemeinsame Handelstage ---
    print("=" * 80)
    print("TEIL 1: Tage mit Trade-Exits in mindestens 2 von 4 Bots gleichzeitig")
    print("=" * 80)

    date_range = pd.date_range(common_start, common_end, freq="D")
    activity = pd.DataFrame(index=date_range)
    for label, dates in trade_dates.items():
        dates_in_window = dates[(dates >= common_start) & (dates <= common_end)]
        activity[label] = date_range.isin(dates_in_window)

    total_days = len(date_range)
    active_bot_count = activity.sum(axis=1)
    days_with_any_trade = (active_bot_count >= 1).sum()
    days_with_2plus = (active_bot_count >= 2).sum()
    days_with_3plus = (active_bot_count >= 3).sum()
    days_with_all4 = (active_bot_count == 4).sum()

    print(f"Gesamtzahl Tage im Fenster:                {total_days}")
    print(f"Tage mit >=1 Bot mit Trade-Exit:            {days_with_any_trade} "
          f"({days_with_any_trade/total_days*100:.1f}%)")
    print(f"Tage mit >=2 Bots GLEICHZEITIG mit Exit:    {days_with_2plus} "
          f"({days_with_2plus/total_days*100:.1f}%)")
    print(f"Tage mit >=3 Bots GLEICHZEITIG mit Exit:    {days_with_3plus} "
          f"({days_with_3plus/total_days*100:.1f}%)")
    print(f"Tage mit ALLEN 4 Bots GLEICHZEITIG mit Exit: {days_with_all4} "
          f"({days_with_all4/total_days*100:.1f}%)")

    print(f"\nJe Bot: Anteil der Fenstertage mit mindestens einem Trade-Exit:")
    for label in curves:
        pct = activity[label].sum() / total_days * 100
        print(f"  {label}: {activity[label].sum()} Tage ({pct:.1f}%)")

    if days_with_2plus > 0:
        overlap_corr = activity.astype(int).corr()
        print(f"\nKorrelation der AKTIVITAETS-Indikatoren (0/1, hat der Bot an diesem Tag")
        print(f"gehandelt) - misst Timing-Ueberlappung unabhaengig von der Rendite-Richtung:")
        print(overlap_corr.round(2).to_string())

    # --- Teil 2: Stress-Periode 2022 ---
    print("\n" + "=" * 80)
    print(f"TEIL 2: Verhalten waehrend der Stress-Periode {STRESS_PERIOD_START} bis {STRESS_PERIOD_END}")
    print("=" * 80)

    stress_start = pd.Timestamp(STRESS_PERIOD_START)
    stress_end = pd.Timestamp(STRESS_PERIOD_END)

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

    # Kombiniertes 25/25/25/25-Portfolio NUR waehrend der Stress-Periode
    normalised_stress = pd.DataFrame({
        label: (series[(series.index >= stress_start) & (series.index <= stress_end)])
        for label, series in curves.items()
    })
    normalised_stress = normalised_stress.dropna()
    if not normalised_stress.empty:
        normalised_stress = normalised_stress / normalised_stress.iloc[0] * 100
        portfolio_stress = normalised_stress.mean(axis=1)
        running_max = portfolio_stress.cummax()
        portfolio_dd = ((portfolio_stress - running_max) / running_max * 100).min()
        portfolio_return = (portfolio_stress.iloc[-1] / portfolio_stress.iloc[0] - 1) * 100
        print(f"\nGleichgewichtete 4-Bot-Kombination WAEHREND der Stress-Periode:")
        print(f"  Rendite: {portfolio_return:.2f}%  |  Max Drawdown: {portfolio_dd:.2f}%")
        worst_individual = stress_df["max_drawdown_pct"].min()
        print(f"  (schlechtester Einzel-Bot-Drawdown in der Stress-Periode: {worst_individual:.2f}%)")


if __name__ == "__main__":
    main()
