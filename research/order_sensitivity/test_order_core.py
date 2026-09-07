"""
Sanity-Checks fuer order_core.py
=====================================
Ohne Test-Framework, wie in allen bisherigen Untersuchungen dieses Projekts.

Nutzung:  python3 test_order_core.py
"""

import os
import sys

import numpy as np
import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import order_core as oc

PASSED = FAILED = 0


def check(label, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  OK    {label}")
    else:
        FAILED += 1
        print(f"  FEHLER {label}   {detail}")


def reference_simulate_portfolio(trades, starting_capital, allocation_pct,
                                  max_concurrent_positions=None):
    """
    WORTGETREUE Kopie der in allen 9 Bots gleichlautenden
    `equity_simulation.py::simulate_portfolio` - hier nur, um im Test ohne
    Bot-Import dagegen pruefen zu koennen. Der Abgleich gegen die ECHTEN
    Bot-Funktionen auf den ECHTEN Daten passiert zusaetzlich in
    run_one_bot.py (25 Permutationen je Bot).
    """
    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx))
        events.append((trade["exit_time"], "exit", idx))
    events.sort(key=lambda e: (e[0], e[1] != "exit"))

    capital = starting_capital
    open_positions, skipped, executed, curve = {}, [], [], []
    for time, event_type, idx in events:
        trade = trades.loc[idx]
        if event_type == "entry":
            if max_concurrent_positions is not None and len(open_positions) >= max_concurrent_positions:
                skipped.append(idx)
                continue
            free = capital - sum(open_positions.values())
            allocation = capital * allocation_pct
            if allocation > free:
                skipped.append(idx)
                continue
            open_positions[idx] = allocation
            executed.append(idx)
        else:
            if idx not in open_positions:
                continue
            allocation = open_positions.pop(idx)
            capital += allocation * (trade["pnl_pct"] / 100)
            curve.append(round(capital, 2))

    if curve:
        series = pd.Series([starting_capital] + curve)
        running_max = series.cummax()
        max_dd = round(float(((series - running_max) / running_max * 100).min()), 2)
    else:
        max_dd = 0.0
    return {"total_return_pct": (round(capital, 2) / starting_capital - 1) * 100,
            "max_drawdown_pct": max_dd, "num_executed": len(executed), "num_skipped": len(skipped)}


# Trade-Satz MIT mehrfach belegten Einstiegszeitpunkten - genau darum geht es.
days = ["2024-01-02", "2024-01-02", "2024-01-02", "2024-01-05", "2024-01-05",
        "2024-02-01", "2024-02-01", "2024-02-14", "2024-03-03", "2024-03-03",
        "2024-03-03", "2024-04-08", "2024-05-02", "2024-05-02", "2024-06-11"]
demo = pd.DataFrame({
    "symbol": [f"S{i % 5}" for i in range(len(days))],
    "entry_time": pd.to_datetime(days),
    "exit_time": pd.to_datetime(days) + pd.to_timedelta(np.arange(len(days)) % 7 + 3, unit="D"),
    "pnl_pct": [7.5, -4.2, 19.0, -3.1, 11.4, -6.0, 2.2, 25.5, -5.0, 8.8,
                -1.5, 14.0, -7.7, 3.3, 30.0],
})

# ---------------------------------------------------------------------------
print("\n1) permuted() verschiebt NUR die Reihenfolge bei Gleichstand")
# ---------------------------------------------------------------------------
rng = np.random.default_rng(1)
for _ in range(20):
    shuffled = oc.permuted(demo, rng)
    if not shuffled["entry_time"].is_monotonic_increasing:
        break
else:
    check("die chronologische Abfolge bleibt in allen Permutationen erhalten", True)
check("Trade-Menge bleibt identisch (nur umsortiert)",
      sorted(oc.permuted(demo, rng)["pnl_pct"].tolist()) == sorted(demo["pnl_pct"].tolist()))
check("die Multimenge der Zeitstempel bleibt identisch",
      oc.permuted(demo, rng)["entry_time"].value_counts().equals(demo["entry_time"].value_counts()))

fixed = demo.assign(entry_time=pd.to_datetime([f"2024-01-{i + 1:02d}" for i in range(len(demo))]))
results = {oc.simulate_fast(*oc.as_arrays(oc.permuted(fixed, rng)), 10_000.0, 0.34, 2)["total_return_pct"]
           for _ in range(30)}
check("bei AUSSCHLIESSLICH eindeutigen Zeitstempeln ist die Permutation wirkungslos",
      len(results) == 1, f"{len(results)} verschiedene Ergebnisse")

# ---------------------------------------------------------------------------
print("\n2) simulate_fast == die in allen 9 Bots gleichlautende simulate_portfolio")
# ---------------------------------------------------------------------------
for allocation, limit in ((0.10, None), (0.10, 3), (0.34, 2), (0.02, None), (0.50, 1)):
    ref = reference_simulate_portfolio(demo, 10_000.0, allocation, limit)
    mine = oc.simulate_fast(*oc.as_arrays(demo), 10_000.0, allocation, limit)
    label = f"Allokation {allocation:.0%}, Limit {limit}"
    check(f"identische Kennzahlen ({label})",
          abs(ref["total_return_pct"] - mine["total_return_pct"]) < 1e-9
          and abs(ref["max_drawdown_pct"] - mine["max_drawdown_pct"]) < 1e-9,
          f"{ref['total_return_pct']:.6f}/{ref['max_drawdown_pct']} vs. "
          f"{mine['total_return_pct']:.6f}/{mine['max_drawdown_pct']}")
    check(f"identische Anzahl ausgefuehrter Trades ({label})",
          ref["num_executed"] == int(mine["executed"].sum()),
          f"{ref['num_executed']} vs. {int(mine['executed'].sum())}")

# ---------------------------------------------------------------------------
print("\n3) Ablehnungsgruende werden korrekt getrennt")
# ---------------------------------------------------------------------------
tight_limit = oc.simulate_fast(*oc.as_arrays(demo), 10_000.0, 0.01, 1)
check("bei winziger Allokation und Limit 1 sind alle Ablehnungen Limit-bedingt",
      (tight_limit["skip_reason"] == oc.SKIP_CAPITAL).sum() == 0
      and (tight_limit["skip_reason"] == oc.SKIP_POSITION_LIMIT).sum() > 0,
      str(np.bincount(tight_limit["skip_reason"], minlength=3)))
tight_capital = oc.simulate_fast(*oc.as_arrays(demo), 10_000.0, 0.60, None)
check("ohne Limit, aber bei grosser Allokation sind alle Ablehnungen kapitalbedingt",
      (tight_capital["skip_reason"] == oc.SKIP_POSITION_LIMIT).sum() == 0
      and (tight_capital["skip_reason"] == oc.SKIP_CAPITAL).sum() > 0,
      str(np.bincount(tight_capital["skip_reason"], minlength=3)))
roomy = oc.simulate_fast(*oc.as_arrays(demo), 10_000.0, 0.01, None)
check("ohne jeden Engpass wird nichts abgelehnt",
      roomy["executed"].all() and (roomy["skip_reason"] == oc.SKIP_NONE).all())

# ---------------------------------------------------------------------------
print("\n4) run_permutations: umstrittene Trades und Streuung")
# ---------------------------------------------------------------------------
tight = oc.run_permutations(demo, 10_000.0, 0.34, 2, 200, 7)
check("bei Engpass gibt es umstrittene Trades (Status nicht konstant)",
      tight["trades_contested"] > 0, str(tight["trades_contested"]))
check("immer+nie+umstritten ergibt genau die Trade-Anzahl",
      tight["trades_always_executed"] + tight["trades_never_executed"]
      + tight["trades_contested"] == len(demo))
check("die Calmar-Spanne ist bei Engpass echt breit",
      tight["calmar_ratio"]["min"] < tight["calmar_ratio"]["max"],
      f"{tight['calmar_ratio']['min']}..{tight['calmar_ratio']['max']}")

loose = oc.run_permutations(demo, 10_000.0, 0.01, None, 50, 7)
check("ohne Engpass ist kein Trade umstritten", loose["trades_contested"] == 0)
check("ohne Engpass ist die Spanne ein Punkt",
      loose["total_return_pct"]["min"] == loose["total_return_pct"]["max"])
check("Reproduzierbarkeit bei gleichem Seed",
      oc.strip_values(oc.run_permutations(demo, 10_000.0, 0.34, 2, 50, 3))
      == oc.strip_values(oc.run_permutations(demo, 10_000.0, 0.34, 2, 50, 3)))

# ---------------------------------------------------------------------------
print("\n5) percentile_of ordnet den Ausgangswert korrekt ein")
# ---------------------------------------------------------------------------
spread = {"values": np.arange(100, dtype=float)}
check("Wert unterhalb aller Permutationen -> 0. Perzentil", oc.percentile_of(-1, spread) == 0.0)
check("Wert oberhalb aller Permutationen -> 100. Perzentil", oc.percentile_of(999, spread) == 100.0)
check("Median-Wert -> etwa 50. Perzentil", 49.0 <= oc.percentile_of(50, spread) <= 51.0,
      str(oc.percentile_of(50, spread)))
check("percentile_of ist None-sicher", oc.percentile_of(None, spread) is None
      and oc.percentile_of(1.0, None) is None)

# ---------------------------------------------------------------------------
print("\n6) timestamp_stats")
# ---------------------------------------------------------------------------
stats = oc.timestamp_stats(demo)
# 3x 2024-01-02, 2x 01-05, 2x 02-01, 3x 03-03, 2x 05-02 = 12 Trades in Gruppen,
# dazu 3 mit eindeutigem Zeitstempel (02-14, 04-08, 06-11).
check("erkennt geteilte Zeitstempel und die groesste Gruppe",
      stats["largest_same_timestamp_group"] == 3
      and stats["trades_sharing_entry_timestamp"] == 12
      and stats["distinct_entry_timestamps"] == 8,
      str(stats))
check("bei eindeutigen Zeitstempeln ist der Anteil 0",
      oc.timestamp_stats(fixed)["share_sharing_entry_timestamp_pct"] == 0.0)

# ---------------------------------------------------------------------------
print("\n7) Kennzahlen-Konvention")
# ---------------------------------------------------------------------------
check("Calmar-Konvention identisch zu allen bisherigen Untersuchungen (82,43/6,33 = 13,02)",
      oc.calmar(82.43, -6.33) == 13.02)
check("Calmar ist bei Drawdown 0 nicht definiert", oc.calmar(50.0, 0.0) is None)
check("strip_values entfernt die rohen Permutations-Arrays",
      "values" not in oc.strip_values(tight)["calmar_ratio"])

print("\n" + "=" * 60)
print(f"{PASSED} Checks bestanden, {FAILED} fehlgeschlagen.")
print("=" * 60)
sys.exit(1 if FAILED else 0)
