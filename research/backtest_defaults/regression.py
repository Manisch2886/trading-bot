"""
Regressionscheck: aendert die Kopplung an live_params.py das Ergebnis?
================================================================================
Fuer jeden betroffenen Bot wird das ECHTE equity_simulation.py ausgefuehrt -
kein nachgebauter Testaufbau - und das Ergebnis als Pruefsumme festgehalten.
Vorher und nachher muessen exakt dieselben Zahlen herauskommen, denn alle
umgestellten Konstanten hatten bereits denselben Wert wie in live_params.py.
Waere der Regressionscheck NICHT identisch, waere das der Beweis, dass die
Kopplung doch etwas veraendert - und damit ein Abbruchgrund.

ZWEI VORKEHRUNGEN, damit der Lauf nichts anfasst, was er nicht darf:

  1. ISOLIERTER PROZESS JE BOT. Die Bots haben gleichnamige Module
     (backtest_breakout.py existiert zweimal, indicators.py neunmal). In
     einem gemeinsamen Prozess wuerde sys.modules den zuerst geladenen
     gewinnen lassen und der zweite Bot heimlich mit fremdem Code rechnen.
  2. UMGELEITETE ERGEBNISPFADE. strategy_paths.get_strategy_paths wird so
     gepatcht, dass RESULTS_DIR und LOGS_DIR in ein temporaeres Verzeichnis
     zeigen. Die echten results/-Dateien und Datenbanken des Projekts
     bleiben dadurch unberuehrt; DATA_DIR zeigt weiter auf die echten
     Kursdaten, denn genau die sollen ja gerechnet werden.

Nutzung:  python3 regression.py vorher      # Basislinie schreiben
          python3 regression.py nachher     # gegen die Basislinie pruefen
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
STRATEGIES = os.path.join(_REPO_ROOT, "strategies")
SHARED = os.path.join(_REPO_ROOT, "shared")
RESULTS_DIR = os.path.join(_DIR, "results")

# Die Bots, deren backtest-Modul in dieser Aenderung gekoppelt wird.
BETROFFEN = ["rsi2_mean_reversion", "turtle_soup_crypto", "turtle_soup_stocks",
             "volatility_breakout", "volatility_breakout_crypto"]

LAEUFER = r'''
import io, json, os, runpy, sys, contextlib

bot_dir = sys.argv[1]
temp_dir = sys.argv[2]
shared = sys.argv[3]

sys.path.insert(0, bot_dir)
sys.path.insert(0, shared)

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

puffer = io.StringIO()
with contextlib.redirect_stdout(puffer):
    runpy.run_path(os.path.join(bot_dir, "equity_simulation.py"),
                   run_name="__main__")

# Der temporaere Pfad steht in der Ausgabe ("Gespeichert als: ...") und
# ist bei jedem Lauf ein anderer. Ohne diese Normalisierung waere jeder
# Vergleich zwangslaeufig eine Abweichung - und der Regressionscheck
# damit wertlos.
ausgabe = puffer.getvalue().replace(temp_dir, "<TEMP>")
dateien = {}
res = os.path.join(temp_dir, "results")
for wurzel, _, namen in os.walk(res):
    for n in sorted(namen):
        pfad = os.path.join(wurzel, n)
        with open(pfad, "rb") as f:
            dateien[os.path.relpath(pfad, res)] = f.read().decode("utf-8", "replace")

print("---REGRESSION-JSON---")
print(json.dumps({"stdout": ausgabe, "dateien": dateien}))
'''


def lauf(bot: str) -> dict:
    bot_dir = os.path.join(STRATEGIES, bot)
    with tempfile.TemporaryDirectory(prefix=f"reg_{bot}_") as temp_dir:
        skript = os.path.join(temp_dir, "_laeufer.py")
        with open(skript, "w", encoding="utf-8") as f:
            f.write(LAEUFER)
        fertig = subprocess.run(
            [sys.executable, skript, bot_dir, temp_dir, SHARED],
            capture_output=True, text=True, timeout=1800)

    if fertig.returncode != 0:
        return {"fehler": fertig.stderr[-3000:]}

    marke = "---REGRESSION-JSON---"
    if marke not in fertig.stdout:
        return {"fehler": "kein JSON-Block in der Ausgabe:\n"
                           + fertig.stdout[-2000:] + fertig.stderr[-2000:]}
    roh = json.loads(fertig.stdout.split(marke, 1)[1])

    return {
        "stdout": roh["stdout"],
        "stdout_hash": hashlib.sha256(roh["stdout"].encode()).hexdigest(),
        "dateien": {n: hashlib.sha256(inhalt.encode()).hexdigest()
                     for n, inhalt in sorted(roh["dateien"].items())},
    }


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("vorher", "nachher"):
        print(__doc__)
        sys.exit(1)
    phase = sys.argv[1]

    os.makedirs(RESULTS_DIR, exist_ok=True)
    ziel = os.path.join(RESULTS_DIR, f"regression_{phase}.json")

    ergebnisse = {}
    for bot in BETROFFEN:
        print(f"{bot} ... ", end="", flush=True)
        ergebnisse[bot] = lauf(bot)
        if "fehler" in ergebnisse[bot]:
            print("FEHLER")
            print(ergebnisse[bot]["fehler"])
        else:
            print(f"{len(ergebnisse[bot]['dateien'])} Ergebnisdateien, "
                  f"stdout {ergebnisse[bot]['stdout_hash'][:12]}")

    with open(ziel, "w", encoding="utf-8") as f:
        json.dump(ergebnisse, f, indent=2, ensure_ascii=False)
    print(f"\ngeschrieben: {ziel}")

    if phase == "nachher":
        vorher_pfad = os.path.join(RESULTS_DIR, "regression_vorher.json")
        if not os.path.exists(vorher_pfad):
            print("Keine Basislinie vorhanden - erst 'vorher' laufen lassen.")
            sys.exit(1)
        with open(vorher_pfad, encoding="utf-8") as f:
            vorher = json.load(f)

        print("\nVERGLEICH")
        print("-" * 60)
        alles_gleich = True
        for bot in BETROFFEN:
            a, b = vorher.get(bot, {}), ergebnisse.get(bot, {})
            if "fehler" in a or "fehler" in b:
                print(f"  {bot:<28} FEHLER in einem der Laeufe")
                alles_gleich = False
                continue
            gleich = (a["stdout_hash"] == b["stdout_hash"]
                      and a["dateien"] == b["dateien"])
            print(f"  {bot:<28} {'identisch' if gleich else 'ABWEICHUNG'}")
            if not gleich:
                alles_gleich = False
                if a["stdout_hash"] != b["stdout_hash"]:
                    _zeige_diff(a["stdout"], b["stdout"])
                for n in sorted(set(a["dateien"]) | set(b["dateien"])):
                    if a["dateien"].get(n) != b["dateien"].get(n):
                        print(f"      Datei unterschiedlich: {n}")
        print("-" * 60)
        print("ALLE IDENTISCH" if alles_gleich else "MINDESTENS EINE ABWEICHUNG")
        sys.exit(0 if alles_gleich else 1)


def _zeige_diff(a: str, b: str):
    import difflib
    for zeile in list(difflib.unified_diff(a.splitlines(), b.splitlines(),
                                            "vorher", "nachher", lineterm=""))[:40]:
        print("      " + zeile)


if __name__ == "__main__":
    main()
