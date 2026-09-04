"""
Abgrenzung zu Volatility Breakout: Signal-Ueberschneidung und Divergenz
================================================================================
Kern der Diversifikationsthese fuer Turtle Soup (auf ausdrueckliche Anfrage
geprueft): Turtle Soup (Reversal NACH einem Fehlausbruch nach UNTEN) und
Volatility Breakout (Einstieg BEI einem Ausbruch nach OBEN) sollten sich
gegenlaeufig verhalten - Turtle Soup sollte insbesondere in Phasen aktiv
sein, in denen Volatility Breakout viele Fehlausbrueche (Stop-Loss-Exits)
erlebt.

WICHTIG - bewusste Ausnahme vom "kein Cross-Strategy-Import"-Prinzip:
Dieses Skript ist eine reine VERGLEICHSANALYSE zwischen zwei bereits
bestehenden, unabhaengigen Strategien (kein gemeinsamer Code-Pfad, keine
Aenderung an volatility_breakout/) - genau wie
shared/portfolio_overview.py oder
volatility_breakout_crypto/stress_period_2022_crypto_family.py bereits
mehrere Bots gemeinsam auswerten.

TECHNISCHER HINWEIS: volatility_breakout/ und turtle_soup_stocks/ haben
gleichnamige Module (multi_symbol_optimise.py, equity_simulation.py,
indicators.py) mit unterschiedlichem Inhalt. Ein gemeinsamer Python-Prozess
wuerde durch transitive "bare"-Importe innerhalb dieser Module (z.B.
importiert equity_simulation.py intern selbst wieder multi_symbol_optimise)
zu stillen Modul-Kollisionen im sys.modules-Cache fuehren (verifiziert -
ergab falsche, aber nicht crashende Trade-Zahlen). Deshalb werden die
Volatility-Breakout-Trades in einem EIGENEN Subprozess erzeugt (mit
volatility_breakout/ als Arbeitsverzeichnis) und als CSV zwischengespeichert -
sauberste Isolation, kein Risiko einer stillen Fehlbindung.

Drei Tests:
1. Zeitliche Naehe: wie viele Turtle-Soup-Einstiege liegen innerhalb von
   OVERLAP_WINDOW_DAYS NACH einem Volatility-Breakout-Stop-Loss-Exit AUF
   DEMSELBEN Symbol? (direkter Test der Hypothese: TS "fischt" dort, wo
   VB gerade gescheitert ist)
2. Korrelation der taeglichen Portfolio-Renditen beider Strategien
   (identische Methodik wie bei den bisherigen Bot-Korrelationsanalysen).
"""

import os
import subprocess
import sys
import numpy as np
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_STRATEGIES_ROOT = os.path.dirname(_STRATEGY_DIR)
_VB_DIR = os.path.join(_STRATEGIES_ROOT, "volatility_breakout")
_SHARED_DIR = os.path.join(_STRATEGIES_ROOT, "..", "shared")
sys.path.insert(0, _SHARED_DIR)
sys.path.insert(0, _STRATEGY_DIR)

from strategy_paths import get_strategy_paths
from multi_symbol_optimise import load_all_symbol_data as ts_load_all_symbol_data
from equity_simulation import (
    collect_all_trades as ts_collect_all_trades, simulate_portfolio as ts_simulate_portfolio,
    STARTING_CAPITAL as TS_STARTING_CAPITAL, ALLOCATION_PCT as TS_ALLOCATION_PCT,
    MAX_CONCURRENT_POSITIONS as TS_MAX_CONCURRENT_POSITIONS, DONCHIAN_PERIOD, STOP_MODE,
)

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

VB_TRADES_CSV = os.path.join(RESULTS_DIR, "_vb_trades_cache.csv")
OVERLAP_WINDOW_DAYS = 10  # Turtle Soups eigener Zeit-Exit-Horizont - konsistente Groessenordnung

# Volatility Breakouts eigene Portfolio-Parameter (aus dessen live_params.py/PROTOTYPE_FINDINGS.md) -
# hier NUR als Konstanten dupliziert (kein Import), damit die Korrelationsanalyse konsistent mit
# volatility_breakout/equity_simulation.py rechnet.
VB_STARTING_CAPITAL = 10_000.0
VB_ALLOCATION_PCT = 0.10
VB_MAX_CONCURRENT_POSITIONS = 8
VB_STOP_LOSS_PCT = 8.0


def generate_vb_trades_via_subprocess() -> pd.DataFrame:
    """Erzeugt Volatility-Breakout-Trades in einem eigenstaendigen
    Subprozess (siehe Modul-Docstring - vermeidet Modul-Namenskollisionen)
    und liest sie als CSV zurueck."""
    script = f"""
import sys
sys.path.insert(0, {_VB_DIR!r})
from multi_symbol_optimise import load_all_symbol_data
from equity_simulation import collect_all_trades, STOP_LOSS_PCT
all_data = load_all_symbol_data()
trades = collect_all_trades(all_data, STOP_LOSS_PCT)
trades.to_csv({VB_TRADES_CSV!r}, index=False)
print(f"{{len(trades)}} VB-Trades geschrieben")
"""
    result = subprocess.run([sys.executable, "-c", script], cwd=_VB_DIR,
                             capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Volatility-Breakout-Subprozess fehlgeschlagen:\n{result.stderr}")
    print(f"  {result.stdout.strip()}")
    return pd.read_csv(VB_TRADES_CSV, parse_dates=["entry_time", "exit_time"])


def load_ts_trades() -> pd.DataFrame:
    all_data = ts_load_all_symbol_data()
    return ts_collect_all_trades(all_data, DONCHIAN_PERIOD, STOP_MODE)


def _count_near_failure(ts_entries: pd.DataFrame, vb_stop_exits: pd.DataFrame) -> int:
    n_near_vb_failure = 0
    for _, ts_row in ts_entries.iterrows():
        same_symbol_stops = vb_stop_exits[vb_stop_exits["symbol"] == ts_row["symbol"]]
        if same_symbol_stops.empty:
            continue
        days_since = (ts_row["entry_time"] - same_symbol_stops["exit_time"]).dt.days
        if ((days_since >= 0) & (days_since <= OVERLAP_WINDOW_DAYS)).any():
            n_near_vb_failure += 1
    return n_near_vb_failure


def test_temporal_proximity(ts_trades: pd.DataFrame, vb_trades: pd.DataFrame, n_shuffles: int = 20) -> dict:
    """Aufgabe 1: Fraktion der Turtle-Soup-Einstiege, die innerhalb von
    OVERLAP_WINDOW_DAYS NACH einem Volatility-Breakout-Stop-Loss-Exit auf
    demselben Symbol liegen - PLUS eine Zufalls-Baseline (n_shuffles
    Permutationen der VB-Exit-Daten je Symbol, Datumsbereich und Anzahl
    unveraendert), um einzuordnen, ob die beobachtete Rate ueber dem
    Zufallsniveau liegt (reines Timing-Zusammentreffen waere sonst nicht
    von echter Ueberschneidung zu unterscheiden)."""
    vb_stop_exits = vb_trades[vb_trades["result"] == "stop_loss"][["symbol", "exit_time"]].copy()
    vb_stop_exits["exit_time"] = pd.to_datetime(vb_stop_exits["exit_time"])

    ts_entries = ts_trades[["symbol", "entry_time"]].copy()
    ts_entries["entry_time"] = pd.to_datetime(ts_entries["entry_time"])

    observed = _count_near_failure(ts_entries, vb_stop_exits)

    rng = np.random.default_rng(42)
    date_min, date_max = vb_stop_exits["exit_time"].min(), vb_stop_exits["exit_time"].max()
    total_days = (date_max - date_min).days
    shuffle_counts = []
    for _ in range(n_shuffles):
        shuffled = vb_stop_exits.copy()
        random_offsets = rng.integers(0, total_days, size=len(shuffled))
        shuffled["exit_time"] = date_min + pd.to_timedelta(random_offsets, unit="D")
        shuffle_counts.append(_count_near_failure(ts_entries, shuffled))
    baseline_mean = float(np.mean(shuffle_counts))

    return {
        "ts_entries_total": len(ts_entries),
        "vb_stop_loss_exits_total": len(vb_stop_exits),
        "ts_entries_near_vb_failure_beobachtet": observed,
        "anteil_beobachtet_pct": round(observed / len(ts_entries) * 100, 2) if len(ts_entries) else None,
        "ts_entries_near_vb_failure_zufalls_baseline": round(baseline_mean, 1),
        "anteil_zufalls_baseline_pct": round(baseline_mean / len(ts_entries) * 100, 2) if len(ts_entries) else None,
        "faktor_ueber_zufall": round(observed / baseline_mean, 2) if baseline_mean else None,
    }


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


def vb_simulate_portfolio_local(trades: pd.DataFrame, starting_capital: float,
                                 allocation_pct: float, max_concurrent_positions: int) -> dict:
    """Identische Logik zu volatility_breakout/equity_simulation.py.simulate_portfolio
    (hier dupliziert statt importiert, siehe Modul-Docstring zur Import-Isolation)."""
    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx))
        events.append((trade["exit_time"], "exit", idx))
    events.sort(key=lambda e: (e[0], e[1] != "exit"))

    capital = starting_capital
    open_positions = {}
    equity_curve = []

    for time, event_type, idx in events:
        trade = trades.loc[idx]
        if event_type == "entry":
            if max_concurrent_positions is not None and len(open_positions) >= max_concurrent_positions:
                continue
            bound_capital = sum(open_positions.values())
            free_capital = capital - bound_capital
            allocation = capital * allocation_pct
            if allocation > free_capital:
                continue
            open_positions[idx] = allocation
        elif event_type == "exit":
            if idx not in open_positions:
                continue
            allocation = open_positions.pop(idx)
            pnl_pct = trade["pnl_pct"]
            result_value = allocation * (1 + pnl_pct / 100)
            capital += (result_value - allocation)
            equity_curve.append({"time": time, "capital_after": round(capital, 2)})

    return {"final_capital": round(capital, 2), "equity_curve": pd.DataFrame(equity_curve)}


def test_correlation(ts_trades: pd.DataFrame, vb_trades: pd.DataFrame) -> dict:
    """Aufgabe 2: Korrelation der taeglichen Portfolio-Renditen (jeweils
    eigenstaendige 10%/Limit-8-Simulation)."""
    ts_result = ts_simulate_portfolio(ts_trades, TS_STARTING_CAPITAL, TS_ALLOCATION_PCT, TS_MAX_CONCURRENT_POSITIONS)
    vb_result = vb_simulate_portfolio_local(vb_trades, VB_STARTING_CAPITAL, VB_ALLOCATION_PCT, VB_MAX_CONCURRENT_POSITIONS)

    ts_curve = build_daily_capital_curve(ts_result["equity_curve"], TS_STARTING_CAPITAL)
    vb_curve = build_daily_capital_curve(vb_result["equity_curve"], VB_STARTING_CAPITAL)

    common_start = max(ts_curve.index.min(), vb_curve.index.min())
    common_end = min(ts_curve.index.max(), vb_curve.index.max())
    date_range = pd.date_range(common_start, common_end, freq="D")

    combined = pd.DataFrame({
        "Turtle Soup": ts_curve.reindex(date_range).ffill().bfill(),
        "Volatility Breakout": vb_curve.reindex(date_range).ffill().bfill(),
    })
    daily_returns = combined.pct_change().dropna()
    corr = daily_returns["Turtle Soup"].corr(daily_returns["Volatility Breakout"])

    return {"gemeinsames_fenster_start": common_start.date(), "gemeinsames_fenster_ende": common_end.date(),
            "korrelation_taegliche_renditen": round(float(corr), 3)}


if __name__ == "__main__":
    print("Lade Turtle-Soup-Trades...")
    ts_trades = load_ts_trades()
    print(f"  {len(ts_trades)} Trades geladen.\n")

    print("Erzeuge Volatility-Breakout-Trades (eigener Subprozess)...")
    vb_trades = generate_vb_trades_via_subprocess()
    print()

    print("=" * 90)
    print("AUFGABE 1: ZEITLICHE NAEHE (Turtle-Soup-Einstieg nach Volatility-Breakout-Fehlausbruch)")
    print("=" * 90)
    proximity = test_temporal_proximity(ts_trades, vb_trades)
    for k, v in proximity.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 90)
    print("AUFGABE 2: KORRELATION DER TAEGLICHEN PORTFOLIO-RENDITEN")
    print("=" * 90)
    correlation = test_correlation(ts_trades, vb_trades)
    for k, v in correlation.items():
        print(f"  {k}: {v}")

    os.remove(VB_TRADES_CSV)  # temporaerer Cache, nicht Teil der committeten Ergebnisse
    os.makedirs(RESULTS_DIR, exist_ok=True)
    pd.DataFrame([proximity]).to_csv(os.path.join(RESULTS_DIR, "experiment_vb_overlap_proximity.csv"), index=False)
    pd.DataFrame([correlation]).to_csv(os.path.join(RESULTS_DIR, "experiment_vb_overlap_correlation.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_vb_overlap_{{proximity,correlation}}.csv")
