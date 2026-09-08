"""
Gegenprobe: greift die Kopplung wirklich?
================================================================================
"Vorher und nachher identisch" allein beweist wenig - dasselbe Ergebnis
kaeme heraus, wenn die Kopplung gar nicht griffe und der Backtest weiter
mit seiner alten, zufaellig gleichen Zahl rechnete. Beide Aussagen zusammen
sind erst der Beweis:

  1. regression.py:   Live-Wert unveraendert -> Ergebnis unveraendert
  2. dieses Skript:   Live-Wert VERAENDERT  -> Ergebnis veraendert sich

Dafuer wird live_params.MAX_HOLD_DAYS im Testprozess um eins verringert,
BEVOR das backtest-Modul importiert wird (der Import zieht den Wert ja
genau einmal). Danach laeuft dasselbe equity_simulation.py wie in
regression.py. Kommt exakt dasselbe Ergebnis heraus, ist die Kopplung
wirkungslos - und die Aenderung waere sinnlos.

Es wird NICHTS auf der Platte veraendert: die Aenderung lebt nur als
Attribut im Speicher des Testprozesses, live_params.py bleibt unberuehrt.

Nutzung:  python3 kopplungsnachweis.py
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile

from regression import BETROFFEN, STRATEGIES, SHARED, RESULTS_DIR

LAEUFER = r'''
import io, json, os, runpy, sys, contextlib

bot_dir, temp_dir, shared, konstante = sys.argv[1:5]

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

# Der Eingriff: live_params vor allen anderen Modulen laden und die
# Konstante veraendern. Jedes Modul, das sie spaeter importiert - allen
# voran das backtest-Modul - sieht dadurch den veraenderten Wert.
import live_params
alt = getattr(live_params, konstante)
setattr(live_params, konstante, alt - 1)

puffer = io.StringIO()
with contextlib.redirect_stdout(puffer):
    runpy.run_path(os.path.join(bot_dir, "equity_simulation.py"),
                   run_name="__main__")

print("---NACHWEIS-JSON---")
print(json.dumps({"stdout": puffer.getvalue().replace(temp_dir, "<TEMP>"),
                  "alt": alt, "neu": alt - 1}))
'''


def lauf(bot: str, konstante: str) -> dict:
    bot_dir = os.path.join(STRATEGIES, bot)
    with tempfile.TemporaryDirectory(prefix=f"nw_{bot}_") as temp_dir:
        skript = os.path.join(temp_dir, "_laeufer.py")
        with open(skript, "w", encoding="utf-8") as f:
            f.write(LAEUFER)
        fertig = subprocess.run(
            [sys.executable, skript, bot_dir, temp_dir, SHARED, konstante],
            capture_output=True, text=True, timeout=1800)
    if "---NACHWEIS-JSON---" not in fertig.stdout:
        return {"fehler": (fertig.stdout[-1500:] + fertig.stderr[-1500:])}
    roh = json.loads(fertig.stdout.split("---NACHWEIS-JSON---", 1)[1])
    roh["stdout_hash"] = hashlib.sha256(roh["stdout"].encode()).hexdigest()
    return roh


def kennzahl(text: str, marke: str) -> str:
    for zeile in text.splitlines():
        if zeile.startswith(marke):
            return zeile.split(":", 1)[1].strip()
    return "?"


def main():
    basis_pfad = os.path.join(RESULTS_DIR, "regression_nachher.json")
    with open(basis_pfad, encoding="utf-8") as f:
        basis = json.load(f)

    print("live_params.MAX_HOLD_DAYS um 1 verringert - das Ergebnis MUSS "
          "sich aendern,\nsonst greift die Kopplung nicht.\n")
    kopf = (f"{'Bot':<28} {'MAX_HOLD_DAYS':>14}  {'Endkapital vorher':>18}  "
            f"{'Endkapital nachher':>19}  Urteil")
    print(kopf)
    print("-" * len(kopf))

    alles_reagiert = True
    for bot in BETROFFEN:
        ergebnis = lauf(bot, "MAX_HOLD_DAYS")
        if "fehler" in ergebnis:
            print(f"{bot:<28} FEHLER\n{ergebnis['fehler']}")
            alles_reagiert = False
            continue
        anders = ergebnis["stdout_hash"] != basis[bot]["stdout_hash"]
        alles_reagiert &= anders
        print(f"{bot:<28} {ergebnis['alt']} -> {ergebnis['neu']:<9} "
              f"{kennzahl(basis[bot]['stdout'], 'Endkapital'):>18}  "
              f"{kennzahl(ergebnis['stdout'], 'Endkapital'):>19}  "
              f"{'reagiert' if anders else 'KEINE WIRKUNG'}")

    print("-" * len(kopf))
    print("Kopplung greift bei allen Bots." if alles_reagiert
          else "MINDESTENS EINE KOPPLUNG OHNE WIRKUNG - Aenderung pruefen!")
    sys.exit(0 if alles_reagiert else 1)


if __name__ == "__main__":
    main()
