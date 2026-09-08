"""
Vorher/Nachher-Lauf der Out-of-Sample-Simulation (elliott_wave_stocks)
================================================================================
Fuehrt das ECHTE oos_equity_simulation.py aus - kein Nachbau - und haelt
Kennzahlen und Ausgabe fest. Dazu werden zwei Dinge zusaetzlich erhoben,
die das Skript selbst nicht ausgibt und die fuer die Beurteilung noetig
sind:

  - die vom In-Sample-Gewinner tatsaechlich vorgeschlagene Kombination,
    inklusive use_take_profit (genau der Wert, den die fehlerhafte Fassung
    verwirft),
  - die Calmar-Ratio (Rendite / |Max Drawdown|) und die Trade-Zahlen.

VORKEHRUNGEN, damit der Lauf nichts anfasst, was er nicht darf:

  1. UMGELEITETE ERGEBNISPFADE. strategy_paths.get_strategy_paths wird so
     gepatcht, dass RESULTS_DIR/LOGS_DIR/DB_FILE in ein temporaeres
     Verzeichnis zeigen. results/elliott_wave_stocks/oos_equity_curve.csv
     im Projekt bleibt unberuehrt; DATA_DIR zeigt weiter auf die echten
     Kursdaten.
  2. EIGENER PROZESS. Die 9 Bots haben gleichnamige Module
     (backtest_elliott.py existiert zweimal). In einem gemeinsamen Prozess
     wuerde sys.modules den zuerst geladenen gewinnen lassen.

Nutzung:  python3 oos_lauf.py vorher|nachher
"""

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
# OOS-Lauf nur dessen Konstante INTERVAL braucht und seine Kurse aus den
# vorhandenen CSV-Dateien liest. Die Attrappe in stubs/ macht den Import
# moeglich und einen echten Netzabruf gleichzeitig unmoeglich.
STUBS = os.path.join(_DIR, "stubs")

LAEUFER = r'''
import io, json, os, runpy, sys, contextlib

bot_dir, temp_dir, shared, stubs = sys.argv[1:5]
sys.path.insert(0, bot_dir)
sys.path.insert(0, shared)
# Attrappen zuletzt einfuegen, damit echte Module Vorrang haetten, falls
# sie doch installiert sind.
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

# Den In-Sample-Gewinner mitschneiden: run_multi_optimisation() liefert die
# Tabelle, aus der das Skript die erste Zeile nimmt. Genau dieser Datensatz
# enthaelt use_take_profit - den Wert, den die fehlerhafte Fassung nicht
# weiterreicht. Ohne diesen Mitschnitt liesse sich hinterher nicht sagen,
# ob der Fix ueberhaupt etwas aendern KANN.
import multi_symbol_optimise
_echte_optimierung = multi_symbol_optimise.run_multi_optimisation
mitschnitt = {}

def _mit_mitschnitt(all_data):
    tabelle = _echte_optimierung(all_data)
    if not tabelle.empty:
        bester = tabelle.iloc[0]
        mitschnitt["bester"] = bester.to_dict()
        mitschnitt["bester_typen"] = {k: type(v).__name__
                                       for k, v in bester.to_dict().items()}
        mitschnitt["spalten_dtypes"] = {k: str(v) for k, v in
                                         tabelle.dtypes.astype(str).items()}
        mitschnitt["top5"] = tabelle.head(5).to_dict("records")
        # Der beste Kandidat MIT festem Ziel - er beantwortet die Frage,
        # was das Skript gemeldet haette, waere es nicht abgestuerzt.
        mit_ziel = tabelle[tabelle["use_take_profit"]]
        if not mit_ziel.empty:
            mitschnitt["bester_mit_ziel"] = mit_ziel.iloc[0].to_dict()
    return tabelle

multi_symbol_optimise.run_multi_optimisation = _mit_mitschnitt

# Auch die Trades und das Portfolio-Ergebnis abgreifen, um Kennzahlen zu
# berechnen, die das Skript selbst nicht ausgibt (Calmar).
import equity_simulation
_echte_simulation = equity_simulation.simulate_portfolio

def _mit_ergebnis(trades, startkapital, allokation, *a, **k):
    ergebnis = _echte_simulation(trades, startkapital, allokation, *a, **k)
    mitschnitt["trades_gesamt"] = int(len(trades))
    mitschnitt["startkapital"] = float(startkapital)
    mitschnitt["endkapital"] = float(ergebnis["final_capital"])
    mitschnitt["ausgefuehrt"] = int(ergebnis["num_executed"])
    mitschnitt["uebersprungen"] = int(ergebnis["num_skipped"])
    mitschnitt["max_dd"] = float(
        equity_simulation.calculate_max_drawdown(ergebnis["equity_curve"], startkapital))
    return ergebnis

equity_simulation.simulate_portfolio = _mit_ergebnis

# Ein Abbruch ist hier ein moegliches ERGEBNIS, kein Testfehler: die
# fehlerhafte Fassung stirbt an genau der Stelle, um die es geht. Der
# Mitschnitt (allen voran der In-Sample-Gewinner) muss deshalb auch dann
# herauskommen - sonst waere nicht belegbar, WARUM sie stirbt.
import traceback

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

print("---OOS-JSON---")
print(json.dumps({"stdout": puffer.getvalue().replace(temp_dir, "<TEMP>"),
                  "mitschnitt": mitschnitt,
                  "abbruch": abbruch}, default=str))
'''


def lauf() -> dict:
    with tempfile.TemporaryDirectory(prefix="oos_") as temp_dir:
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
    }


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("vorher", "nachher"):
        print(__doc__)
        sys.exit(1)
    phase = sys.argv[1]

    print(f"OOS-Lauf ({phase}) laeuft - das dauert einige Minuten ...",
          flush=True)
    ergebnis = lauf()
    if "fehler" in ergebnis:
        print("LAEUFER-FEHLER:\n" + ergebnis["fehler"])
        sys.exit(1)

    ergebnis["kennzahlen"] = kennzahlen(ergebnis["mitschnitt"])
    os.makedirs(RESULTS_DIR, exist_ok=True)
    ziel = os.path.join(RESULTS_DIR, f"oos_{phase}.json")
    with open(ziel, "w", encoding="utf-8") as f:
        json.dump(ergebnis, f, indent=2, ensure_ascii=False, default=str)

    print(ergebnis["stdout"])
    if ergebnis.get("abbruch"):
        print("ABGEBROCHEN - das Skript lief nicht durch:")
        print(ergebnis["abbruch"])
    print("In-Sample-Gewinner:", json.dumps(
        ergebnis["mitschnitt"].get("bester", {}), ensure_ascii=False, default=str))
    print("Kennzahlen:", json.dumps(ergebnis["kennzahlen"], ensure_ascii=False))
    print(f"\ngeschrieben: {ziel}")


if __name__ == "__main__":
    main()
