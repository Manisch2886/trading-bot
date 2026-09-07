"""
Schritt 1: vollstaendiger Sync-Check live_params.py vs. equity_simulation.py
==================================================================================
Stellt fuer ALLE 9 Bots jede Konstante gegenueber, die in beiden Dateien
vorkommt - und prueft zusaetzlich, ob Flags aus live_params.py im
Backtest-Pfad ueberhaupt WIRKSAM sind (ein Flag kann uebereinstimmen und
trotzdem folgenlos bleiben, wenn equity_simulation.py es nie liest).

Rein lesend, per AST-Parsing statt Import - so wird kein Bot-Code
ausgefuehrt und es braucht keine sys.modules-Isolation.

ZWEI STOLPERSTELLEN, die ein naiver Vergleich falsch melden wuerde:

  1. EINHEITEN. `ALLOCATION_PCT` steht in live_params.py in PROZENT
     (10, 5, 2), in equity_simulation.py als ANTEIL (0.10). 10 und 0.10
     sind also dieselbe Konfiguration, nicht zwei verschiedene. Ohne
     Normalisierung waeren alle 6 Bots mit dokumentierter Allokation
     faelschlich als abweichend gemeldet.
  2. NAMEN. Dieselbe Groesse heisst teils unterschiedlich
     (T3_FAST/T3_FAST_LENGTH, SMA_TREND_PERIOD/SMA_TREND_FILTER). Ohne
     Alias-Tabelle waeren diese Paare unsichtbar statt geprueft.

WICHTIG - reine Untersuchung: veraendert keine Datei ausserhalb von
research/sync_check/.

Nutzung:  python3 sync_table.py [--json]
"""

import ast
import json
import os
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
STRATEGIES = os.path.join(_REPO_ROOT, "strategies")
RESULTS_DIR = os.path.join(_DIR, "results")

BOTS = ["elliott_wave", "elliott_wave_stocks", "t3_supertrend",
        "rsi2_crypto", "rsi2_mean_reversion",
        "turtle_soup_crypto", "turtle_soup_stocks",
        "volatility_breakout", "volatility_breakout_crypto"]

# Dieselbe Groesse unter unterschiedlichem Namen: equity_simulation -> live_params
ALIASES = {
    "T3_FAST": "T3_FAST_LENGTH",
    "T3_SLOW": "T3_SLOW_LENGTH",
    "SMA_TREND_PERIOD": "SMA_TREND_FILTER",
}

# In live_params.py in Prozent, in equity_simulation.py als Anteil
PERCENT_VS_FRACTION = {"ALLOCATION_PCT"}

# Rein dokumentarisch, kein Konfigurationswert
IGNORE = {"LAST_UPDATED", "RESULTS_DIR", "STARTING_CAPITAL"}

# Groessen, die equity_simulation.py NICHT selbst fuehrt, die aber ueber den
# Default des jeweiligen backtest_*.py-Moduls trotzdem wirksam werden - teils
# unter anderem Namen. Ohne diese Aufloesung wuerde der Check sie faelschlich
# als "wirkungslos" melden, obwohl der Backtest exakt den Live-Wert verwendet.
BACKTEST_FALLBACK = {
    "MAX_HOLD_DAYS": "MAX_HOLD_DAYS",
    "BB_LOOKBACK": "SQUEEZE_LOOKBACK_DAYS",
    "BB_SQUEEZE_PERCENTILE": "SQUEEZE_PERCENTILE",
}


def backtest_constants(bot: str) -> dict:
    """Konstanten der backtest_*.py-Module eines Bots - sie liefern die
    Defaults, mit denen equity_simulation.py rechnet, wo es selbst keinen
    Wert setzt."""
    folder = os.path.join(STRATEGIES, bot)
    merged = {}
    for name in sorted(os.listdir(folder)):
        if name.startswith("backtest_") and name.endswith(".py"):
            merged.update(constants(os.path.join(folder, name)))
    return merged


def constants(path: str) -> dict:
    """Top-Level-GROSSBUCHSTABEN-Zuweisungen einer Datei, per AST."""
    out = {}
    for node in ast.parse(open(path).read()).body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id.isupper() and not target.id.startswith("_"):
                try:
                    out[target.id] = ast.literal_eval(node.value)
                except ValueError:
                    out[target.id] = "<nicht literal auswertbar>"
    return {k: v for k, v in out.items() if k not in IGNORE}


def compare_bot(bot: str) -> dict:
    lp_path = os.path.join(STRATEGIES, bot, "live_params.py")
    es_path = os.path.join(STRATEGIES, bot, "equity_simulation.py")
    live, esim = constants(lp_path), constants(es_path)
    es_source = open(es_path).read()

    rows, divergences = [], []
    checked_live = set()

    for es_name, es_value in sorted(esim.items()):
        live_name = ALIASES.get(es_name, es_name)
        if live_name not in live:
            rows.append({"groesse": es_name, "live_params": "— nicht dokumentiert —",
                          "equity_simulation": es_value, "status": "nur im Backtest"})
            continue
        checked_live.add(live_name)

        live_value = live[live_name]
        normalised = live_value / 100.0 if (es_name in PERCENT_VS_FRACTION
                                             and isinstance(live_value, (int, float))) else live_value
        same = normalised == es_value
        note = ""
        if es_name in PERCENT_VS_FRACTION:
            note = f"live in Prozent ({live_value}), Backtest als Anteil"
        if es_name in ALIASES:
            note = (note + "; " if note else "") + f"heisst live `{live_name}`"

        rows.append({
            "groesse": es_name, "live_params": live_value, "equity_simulation": es_value,
            "status": "identisch" if same else "ABWEICHUNG", "hinweis": note,
        })
        if not same:
            divergences.append({"groesse": es_name, "live": live_value, "backtest": es_value,
                                 "art": "Konstante"})

    # live_params-Groessen, die equity_simulation.py nicht selbst fuehrt.
    # Drei Faelle, die klar auseinandergehalten werden muessen:
    #   a) equity_simulation.py referenziert den Namen doch (dann wirksam),
    #   b) der Wert kommt ueber den Default des backtest_*.py-Moduls - dann
    #      ist zu pruefen, ob dieser Default dem Live-Wert ENTSPRICHT,
    #   c) es gibt gar keine Entsprechung - erst das ist eine echte,
    #      verhaltensrelevante Abweichung.
    backtest = backtest_constants(bot)
    for live_name, live_value in sorted(live.items()):
        if live_name in checked_live or live_name in ALIASES.values():
            continue

        if live_name in es_source:
            rows.append({"groesse": live_name, "live_params": live_value,
                          "equity_simulation": "— nicht als Konstante —",
                          "status": "im Backtest referenziert"})
            continue

        fallback_name = BACKTEST_FALLBACK.get(live_name)
        if fallback_name and fallback_name in backtest:
            effective = backtest[fallback_name]
            same = effective == live_value
            note = f"Default aus backtest_*.py"
            if fallback_name != live_name:
                note += f" (dort `{fallback_name}`)"
            rows.append({"groesse": live_name, "live_params": live_value,
                          "equity_simulation": effective,
                          "status": "identisch" if same else "ABWEICHUNG", "hinweis": note})
            if not same:
                divergences.append({"groesse": live_name, "live": live_value,
                                     "backtest": effective, "art": "Backtest-Default"})
            continue

        rows.append({"groesse": live_name, "live_params": live_value,
                      "equity_simulation": "— keine Entsprechung —",
                      "status": "nur live, im Backtest WIRKUNGSLOS"})
        divergences.append({"groesse": live_name, "live": live_value,
                             "backtest": "im Backtest-Pfad nicht vorhanden", "art": "Verhalten"})

    return {"bot": bot, "zeilen": rows, "abweichungen": divergences,
            "synchron": not divergences}


def main():
    report = [compare_bot(bot) for bot in BOTS]

    for entry in report:
        marker = "SYNCHRON" if entry["synchron"] else f"{len(entry['abweichungen'])} ABWEICHUNG(EN)"
        print(f"\n=== {entry['bot']}  —  {marker}")
        print(f"  {'Groesse':<28}{'live_params.py':>22}{'equity_simulation.py':>24}  Status")
        for row in entry["zeilen"]:
            note = f"   ({row['hinweis']})" if row.get("hinweis") else ""
            print(f"  {row['groesse']:<28}{str(row['live_params']):>22}"
                  f"{str(row['equity_simulation']):>24}  {row['status']}{note}")

    affected = [e["bot"] for e in report if not e["synchron"]]
    clean = [e["bot"] for e in report if e["synchron"]]
    print(f"\n{'=' * 100}")
    print(f"ABWEICHEND ({len(affected)}): {', '.join(affected)}")
    print(f"SYNCHRON  ({len(clean)}): {', '.join(clean)}")

    if "--json" in sys.argv:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        path = os.path.join(RESULTS_DIR, "sync_table.json")
        with open(path, "w") as f:
            json.dump({"bots": report, "abweichend": affected, "synchron": clean},
                      f, indent=2, ensure_ascii=False)
        print(f"\nGespeichert: {path}")


if __name__ == "__main__":
    main()
