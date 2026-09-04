"""
Aufgabe 3: 2022-Stress-Periode unter der besten Kapitalmanagement-Kombination
================================================================================
Rechnet die 2022-Zahlen (Rendite, Max Drawdown) fuer die beste in
experiment_position_size_limit.py gefundene Kombination (10% Allokation,
Limit 15 - identisch zu Limit 20/unbegrenzt, siehe dortige Matrix) neu durch
und vergleicht sie mit der urspruenglichen Basiskonfiguration (10%, Limit 8).

Leitfrage: Mildert eine hoehere Kapitalauslastung (mehr gleichzeitige
Positionen bei gleicher 10%-Groesse) den in
results/volatility_breakout/PROTOTYPE_FINDINGS.md Abschnitt 10 identifizierten
"langer Baerenmarkt"-Schwachpunkt (35,9% Stop-Loss/False-Breakout-Rate im
2022-Fenster) spuerbar ab, oder bleibt er strukturell unveraendert? Die
False-Breakout-Rate selbst haengt nur von den SIGNALEN ab (unveraendert durch
Kapitalmanagement) - die Frage ist, ob die staerkere Kapitalauslastung den
PORTFOLIO-Effekt dieser Schwaeche verstaerkt (mehr gleichzeitig gebundenes
Kapital in einer schlechten Phase) oder abschwaecht (mehr Diversifikation
ueber gleichzeitige Positionen).
"""

import pandas as pd

from multi_symbol_optimise import load_all_symbol_data
from equity_simulation import collect_all_trades, simulate_portfolio, STARTING_CAPITAL, STOP_LOSS_PCT

CONFIGS = [
    ("Basis (10% Allokation, Limit 8)", 0.10, 8),
    ("Beste Kombination (10% Allokation, Limit 15)", 0.10, 15),
]

STRESS_PERIOD_START = "2022-01-01"
STRESS_PERIOD_END = "2022-12-31"


def build_daily_capital_curve(equity_df: pd.DataFrame, starting_capital: float) -> pd.Series:
    df = equity_df.copy()
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")
    df["date"] = df["time"].dt.normalize()
    daily_last = df.groupby("date")["capital_after"].last()
    full_range = pd.date_range(daily_last.index.min(), daily_last.index.max(), freq="D")
    daily_last = daily_last.reindex(full_range).ffill()
    if pd.isna(daily_last.iloc[0]):
        daily_last.iloc[0] = starting_capital
    return daily_last


def main():
    all_data = load_all_symbol_data()
    trades_full = collect_all_trades(all_data, STOP_LOSS_PCT)

    stress_start = pd.Timestamp(STRESS_PERIOD_START)
    stress_end = pd.Timestamp(STRESS_PERIOD_END)

    rows = []
    for label, allocation_pct, limit in CONFIGS:
        result = simulate_portfolio(trades_full, STARTING_CAPITAL, allocation_pct, limit)
        curve = build_daily_capital_curve(result["equity_curve"], STARTING_CAPITAL)
        window = curve[(curve.index >= stress_start) & (curve.index <= stress_end)]

        if window.empty:
            rows.append({"konfiguration": label, "rendite_2022_pct": None, "max_dd_2022_pct": None})
            continue

        start_cap = window.iloc[0]
        end_cap = window.iloc[-1]
        running_max = window.cummax()
        dd = ((window - running_max) / running_max * 100).min()
        rendite = (end_cap / start_cap - 1) * 100

        # zusaetzlich: wie viele Positionen wurden im 2022-Fenster ausgefuehrt
        # und wie viele davon per Stop-Loss (False Breakout) beendet
        eq = result["equity_curve"].copy()
        eq["time"] = pd.to_datetime(eq["time"])
        exits_in_window = eq[(eq["time"] >= stress_start) & (eq["time"] <= stress_end)]
        n_exits = len(exits_in_window)
        n_losing = (exits_in_window["pnl_pct"] < 0).sum() if n_exits else 0

        rows.append({
            "konfiguration": label,
            "rendite_2022_pct": round(rendite, 2),
            "max_dd_2022_pct": round(dd, 2),
            "start_kapital": round(start_cap, 2),
            "end_kapital": round(end_cap, 2),
            "ausgefuehrte_exits_2022": n_exits,
            "davon_negativer_pnl": int(n_losing),
            "negativer_pnl_anteil_pct": round(n_losing / n_exits * 100, 1) if n_exits else None,
        })

    df = pd.DataFrame(rows)
    print("=" * 100)
    print(f"2022-STRESS-PERIODE ({STRESS_PERIOD_START} bis {STRESS_PERIOD_END}) UNTER VERSCHIEDENEN KONFIGURATIONEN")
    print("=" * 100)
    print(df.to_string(index=False))

    print("\nHinweis: Der Anteil der SIGNALE mit Stop-Loss/False Breakout im 2022-Fenster "
          "(35,9% ueber alle Symbole, siehe PROTOTYPE_FINDINGS.md Abschnitt 10) haengt nur "
          "von der Signal-Logik ab und ist in beiden Konfigurationen identisch - hier gemessen "
          "wird der PORTFOLIO-Effekt (negativer-PnL-Anteil unter den tatsaechlich mit Kapital "
          "versorgten Positionen, je nach Kapitalauslastung unterschiedlich viele/verschiedene Trades).")


if __name__ == "__main__":
    main()
