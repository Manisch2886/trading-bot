"""
Vorher/Nachher-Lauf: Positionslimit in der OOS-Simulation (elliott_wave_stocks)
================================================================================
Fuehrt das ECHTE oos_equity_simulation.py aus - kein Nachbau - und haelt
Kennzahlen, Trades und Ausgabe fest.

Zusaetzlich zu den Kennzahlen wird die TRADE-TABELLE mitgeschnitten. Sie
ist der Schluessel zur eigentlichen Frage dieser Aufgabe: wie viele Trades
das Limit ueberhaupt betrifft. Der Rueckgabewert von simulate_portfolio()
nennt nur eine Summe uebersprungener Trades und unterscheidet nicht, ob
ein Trade am Positionslimit oder am freien Kapital gescheitert ist -
genau diese Unterscheidung braucht die Auswertung (siehe analyse.py).

Ausserdem wird die Trade-Tabelle gehasht. Da die Aenderung nur die
Portfolio-Ebene betrifft, MUESSEN vorher und nachher exakt dieselben
Trades herauskommen. Weicht der Hash ab, hat die Aenderung etwas
angefasst, das sie nicht anfassen darf - das waere ein Abbruchgrund.

VORKEHRUNGEN, damit der Lauf nichts anfasst, was er nicht darf:

  1. UMGELEITETE ERGEBNISPFADE. strategy_paths.get_strategy_paths wird so
     gepatcht, dass RESULTS_DIR/LOGS_DIR/DB_FILE in ein temporaeres
     Verzeichnis zeigen. results/elliott_wave_stocks/ bleibt unberuehrt;
     DATA_DIR zeigt weiter auf die echten Kursdaten.
  2. EIGENER PROZESS. Die 9 Bots haben gleichnamige Module
     (backtest_elliott.py existiert zweimal). In einem gemeinsamen Prozess
     wuerde sys.modules den zuerst geladenen gewinnen lassen.

Nutzung:  python3 oos_lauf.py vorher|nachher
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
BOT_DIR = os.path.join(_REPO_ROOT, "strategies", "elliott_wave_stocks")
SHARED = os.path.join(_REPO_ROOT, "shared")
RESULTS_DIR = os.path.join(_DIR, "results")
# yfinance wird von fetch_stock_data.py auf Modulebene importiert, obwohl der
# Lauf nur dessen Konstante INTERVAL braucht und seine Kurse aus den
# vorhandenen CSV-Dateien liest. Die Attrappe macht den Import moeglich und
# einen echten Netzabruf gleichzeitig unmoeglich.
STUBS = os.path.join(_DIR, "stubs")

LAEUFER = r'''
import io, json, os, runpy, sys, contextlib, traceback

bot_dir, temp_dir, shared, stubs = sys.argv[1:5]
sys.path.insert(0, bot_dir)
sys.path.insert(0, shared)
sys.path.append(stubs)

import strategy_paths
_echt = strategy_paths.get_strategy_paths

def _umgeleitet(caller_file):
    p = dict(_echt(caller_file))
    p["RESULTS_DIR"] = os.path.join(temp_dir, "results")
    p["LOGS_DIR"] = os.path.join(temp_dir, "logs")
    p["DB_FILE"] = os.path.join(temp_dir, "paper_trading.db")
    os.makedirs(p["RESULTS_DIR"], exist_ok=True)
    os.makedirs(p["LOGS_DIR"], exist_ok=True)
    return p

strategy_paths.get_strategy_paths = _umgeleitet

mitschnitt = {}

# Den In-Sample-Gewinner festhalten - er bestimmt, welche Trades ueberhaupt
# entstehen, und muss vorher/nachher identisch sein.
import multi_symbol_optimise
_echte_optimierung = multi_symbol_optimise.run_multi_optimisation

def _mit_mitschnitt(all_data):
    tabelle = _echte_optimierung(all_data)
    if not tabelle.empty:
        mitschnitt["bester"] = tabelle.iloc[0].to_dict()
    return tabelle

multi_symbol_optimise.run_multi_optimisation = _mit_mitschnitt

# Die Trade-Tabelle abgreifen UND mit welchen Argumenten simulate_portfolio
# aufgerufen wurde. Letzteres belegt schwarz auf weiss, ob das Limit
# uebergeben wurde - unabhaengig davon, was im Quelltext steht.
import equity_simulation
_echte_simulation = equity_simulation.simulate_portfolio

def _mit_ergebnis(trades, startkapital, allokation, max_concurrent_positions=None):
    trades.to_csv(os.path.join(temp_dir, "oos_trades.csv"), index=False)
    mitschnitt["limit_uebergeben"] = max_concurrent_positions
    mitschnitt["trades_gesamt"] = int(len(trades))
    ergebnis = _echte_simulation(trades, startkapital, allokation,
                                  max_concurrent_positions)
    mitschnitt["startkapital"] = float(startkapital)
    mitschnitt["allokation"] = float(allokation)
    mitschnitt["endkapital"] = float(ergebnis["final_capital"])
    mitschnitt["ausgefuehrt"] = int(ergebnis["num_executed"])
    mitschnitt["uebersprungen"] = int(ergebnis["num_skipped"])
    mitschnitt["max_dd"] = float(
        equity_simulation.calculate_max_drawdown(ergebnis["equity_curve"], startkapital))
    return ergebnis

equity_simulation.simulate_portfolio = _mit_ergebnis

puffer = io.StringIO()
abbruch = None
with contextlib.redirect_stdout(puffer):
    try:
        runpy.run_path(os.path.join(bot_dir, "oos_equity_simulation.py"),
                       run_name="__main__")
    except SystemExit:
        pass
    except BaseException:
        abbruch = traceback.format_exc()

trades_csv = os.path.join(temp_dir, "oos_trades.csv")
trades_text = open(trades_csv, encoding="utf-8").read() if os.path.exists(trades_csv) else ""

print("---OOS-JSON---")
print(json.dumps({"stdout": puffer.getvalue().replace(temp_dir, "<TEMP>"),
                  "mitschnitt": mitschnitt,
                  "abbruch": abbruch,
                  "trades_csv": trades_text}, default=str))
'''


def lauf() -> dict:
    with tempfile.TemporaryDirectory(prefix="ooslimit_") as temp_dir:
        skript = os.path.join(temp_dir, "_laeufer.py")
        with open(skript, "w", encoding="utf-8") as f:
            f.write(LAEUFER)
        fertig = subprocess.run(
            [sys.executable, skript, BOT_DIR, temp_dir, SHARED, STUBS],
            capture_output=True, text=True, timeout=7200)
    if "---OOS-JSON---" not in fertig.stdout:
        return {"fehler": fertig.stdout[-3000:] + "\n" + fertig.stderr[-3000:]}
    return json.loads(fertig.stdout.split("---OOS-JSON---", 1)[1])


def kennzahlen(m: dict) -> dict:
    if not m.get("endkapital"):
        return {}
    rendite = (m["endkapital"] / m["startkapital"] - 1) * 100
    dd = abs(m.get("max_dd") or 0)
    return {
        "rendite_pct": round(rendite, 2),
        "max_drawdown_pct": round(m.get("max_dd", 0), 2),
        # Calmar hier als Rendite ueber den GESAMTEN OOS-Zeitraum geteilt
        # durch den Betrag des Max Drawdown - nicht annualisiert. So ist es
        # zwischen den beiden Laeufen vergleichbar, worum es hier geht.
        "calmar": round(rendite / dd, 2) if dd else None,
        "endkapital": round(m["endkapital"], 2),
        "trades_gesamt": m.get("trades_gesamt"),
        "ausgefuehrt": m.get("ausgefuehrt"),
        "uebersprungen": m.get("uebersprungen"),
        "limit_uebergeben": m.get("limit_uebergeben"),
    }


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("vorher", "nachher"):
        print(__doc__)
        sys.exit(1)
    phase = sys.argv[1]

    print(f"OOS-Lauf ({phase}) laeuft - das dauert einige Minuten ...", flush=True)
    ergebnis = lauf()
    if "fehler" in ergebnis:
        print("LAEUFER-FEHLER:\n" + ergebnis["fehler"])
        sys.exit(1)

    ergebnis["kennzahlen"] = kennzahlen(ergebnis["mitschnitt"])
    ergebnis["trades_hash"] = hashlib.sha256(
        ergebnis["trades_csv"].encode()).hexdigest()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    # Die Trade-Tabelle separat ablegen - sie ist die Grundlage von analyse.py
    # und waere im JSON nur unhandlich.
    with open(os.path.join(RESULTS_DIR, f"trades_{phase}.csv"), "w",
              encoding="utf-8") as f:
        f.write(ergebnis.pop("trades_csv"))

    ziel = os.path.join(RESULTS_DIR, f"oos_{phase}.json")
    with open(ziel, "w", encoding="utf-8") as f:
        json.dump(ergebnis, f, indent=2, ensure_ascii=False, default=str)

    print(ergebnis["stdout"])
    if ergebnis.get("abbruch"):
        print("ABGEBROCHEN:\n" + ergebnis["abbruch"])
    print("Kennzahlen:", json.dumps(ergebnis["kennzahlen"], ensure_ascii=False))
    print("Trades-Hash:", ergebnis["trades_hash"][:16])
    print(f"\ngeschrieben: {ziel}")


if __name__ == "__main__":
    main()
