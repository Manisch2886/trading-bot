"""
Regressionslauf der Backtest-Kette (vorher/nachher)
================================================================================
Ergaenzt vergleich.py: der prueft forward_test.py, dieses Skript die
Backtest-Seite (equity_simulation.py) desselben Bots. Beide Quellen des
frueher doppelt gefuehrten Werts muessen unveraendert rechnen.

Eigener Laeufer statt research/backtest_defaults/regression.py, aus einem
konkreten Grund: jener nimmt seine Bot-Liste aus einer Modulkonstante. Sie
fuer diesen Lauf zu aendern und die alte Fassung per `git stash` zu holen,
hat beim ersten Versuch genau das Gegenteil bewirkt - der stash nahm die
Listenaenderung mit, und der "vorher"-Lauf lief auf den falschen Bots.
Hier wird die alte Fassung deshalb per `git show` gelesen, ohne den
Arbeitsbaum anzufassen.

VORGEHEN: die alte Fassung der geaenderten Dateien wird aus git in ein
temporaeres Verzeichnis geschrieben, das die uebrigen Bot-Dateien per
Symlink weiterverwendet. So laufen beide Fassungen gegen dieselben
Kursdaten, ohne dass der Arbeitsbaum je umgeschaltet wird.

Nutzung:  python3 backtest_regression.py <bot> <datei> [<datei> ...]
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
STUBS = os.path.join(_DIR, "stubs")
RESULTS_DIR = os.path.join(_DIR, "results")

LAEUFER = r'''
import io, json, os, runpy, sys, contextlib, traceback

bot_dir, temp_dir, shared, stubs, repo = sys.argv[1:6]
sys.path.insert(0, bot_dir)
sys.path.insert(0, shared)
sys.path.append(stubs)

import strategy_paths
_echt = strategy_paths.get_strategy_paths

def _umgeleitet(caller_file):
    p = dict(_echt(caller_file))
    # Regel: der Alt-Baum liefert nur den geaenderten CODE, saemtliche
    # EINGABEN kommen aus dem echten Repo, die AUSGABEN gehen ins temporaere
    # Verzeichnis. get_strategy_paths leitet alle Pfade aus dem Ort der
    # AUFRUFENDEN Datei ab; der Alt-Baum liegt unter /tmp, und dort gibt es
    # weder data/ noch config/.
    #
    # Ohne diese Umleitung waere "ABWEICHUNG" ein Artefakt des Testaufbaus:
    # der Alt-Lauf faende keine Kursdatei (DATA_DIR), und bei den Aktien-Bots
    # auch keine Symbolliste (CONFIG_DIR) - er fiele auf die Standardliste
    # mit 5 Aktien zurueck und rechnete 15 statt 510 Trades. Genau das ist
    # beim ersten Lauf dieser Art passiert.
    p["BASE_DIR"] = repo
    p["DATA_DIR"] = os.path.join(repo, "data")
    p["CONFIG_DIR"] = os.path.join(repo, "config")
    p["RESULTS_DIR"] = os.path.join(temp_dir, "results")
    p["LOGS_DIR"] = os.path.join(temp_dir, "logs")
    p["DB_FILE"] = os.path.join(temp_dir, "paper_trading.db")
    os.makedirs(p["RESULTS_DIR"], exist_ok=True)
    os.makedirs(p["LOGS_DIR"], exist_ok=True)
    return p

strategy_paths.get_strategy_paths = _umgeleitet

puffer = io.StringIO()
abbruch = None
with contextlib.redirect_stdout(puffer):
    try:
        runpy.run_path(os.path.join(bot_dir, "equity_simulation.py"),
                       run_name="__main__")
    except SystemExit:
        pass
    except BaseException:
        abbruch = traceback.format_exc()

dateien = {}
res = os.path.join(temp_dir, "results")
for wurzel, _, namen in os.walk(res):
    for n in sorted(namen):
        with open(os.path.join(wurzel, n), "rb") as f:
            dateien[n] = f.read().decode("utf-8", "replace")

print("---REG-JSON---")
print(json.dumps({"stdout": puffer.getvalue().replace(temp_dir, "<TEMP>"),
                  "dateien": dateien, "abbruch": abbruch}, default=str))
'''


def baue_alten_baum(bot: str, dateien: list, ziel: str):
    """Bot-Ordner nachbauen: geaenderte Dateien in der ALTEN Fassung aus git,
    alle uebrigen per Symlink aus dem Arbeitsbaum."""
    quelle = os.path.join(STRATEGIES, bot)
    os.makedirs(ziel, exist_ok=True)
    alt_namen = set(dateien)
    for name in os.listdir(quelle):
        if name == "__pycache__":
            continue
        if name in alt_namen:
            inhalt = subprocess.run(
                ["git", "-C", _REPO_ROOT, "show", f"HEAD:strategies/{bot}/{name}"],
                capture_output=True, text=True, check=True).stdout
            with open(os.path.join(ziel, name), "w", encoding="utf-8") as f:
                f.write(inhalt)
        else:
            os.symlink(os.path.join(quelle, name), os.path.join(ziel, name))


def lauf(bot_dir: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="reg_") as temp_dir:
        skript = os.path.join(temp_dir, "_laeufer.py")
        with open(skript, "w", encoding="utf-8") as f:
            f.write(LAEUFER)
        fertig = subprocess.run(
            [sys.executable, skript, bot_dir, temp_dir, SHARED, STUBS,
             _REPO_ROOT],
            capture_output=True, text=True, timeout=7200)
    if "---REG-JSON---" not in fertig.stdout:
        return {"fehler": fertig.stdout[-2500:] + "\n" + fertig.stderr[-2500:]}
    roh = json.loads(fertig.stdout.split("---REG-JSON---", 1)[1])
    # Ein Abbruch IM Lauf wurde bisher nur mitgeschrieben, nicht ausgewertet.
    # Damit konnten zwei gescheiterte Laeufe als "IDENTISCH" durchgehen: beide
    # ohne Ausgabe, beide ohne Ergebnisdatei, beide mit demselben Hash der
    # leeren Zeichenkette (e3b0c442...). Genau das ist passiert, als der
    # Aktien-Bot mangels yfinance-Attrappe schon beim Import scheiterte. Ein
    # gescheiterter Lauf belegt nichts und wird deshalb als Fehler behandelt.
    if roh.get("abbruch"):
        return {"fehler": "Lauf abgebrochen:\n" + roh["abbruch"]}
    if not roh["stdout"].strip():
        return {"fehler": "Lauf ohne jede Ausgabe - das belegt nichts.\n"
                          + fertig.stderr[-2500:]}
    roh["stdout_hash"] = hashlib.sha256(roh["stdout"].encode()).hexdigest()
    roh["datei_hashes"] = {n: hashlib.sha256(i.encode()).hexdigest()
                            for n, i in sorted(roh["dateien"].items())}
    return roh


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    bot, dateien = sys.argv[1], sys.argv[2:]

    print(f"Regressionslauf {bot} - geaendert: {', '.join(dateien)}\n")
    with tempfile.TemporaryDirectory(prefix="altbaum_") as basis:
        alt_dir = os.path.join(basis, bot)
        baue_alten_baum(bot, dateien, alt_dir)

        print("alte Fassung (HEAD) ... ", end="", flush=True)
        alt = lauf(alt_dir)
        print("FEHLER" if "fehler" in alt else alt["stdout_hash"][:12])
        if "fehler" in alt:
            print(alt["fehler"]); sys.exit(1)

    print("neue Fassung (Arbeitsbaum) ... ", end="", flush=True)
    neu = lauf(os.path.join(STRATEGIES, bot))
    print("FEHLER" if "fehler" in neu else neu["stdout_hash"][:12])
    if "fehler" in neu:
        print(neu["fehler"]); sys.exit(1)

    gleich = (alt["stdout_hash"] == neu["stdout_hash"]
              and alt["datei_hashes"] == neu["datei_hashes"])
    print("\n" + neu["stdout"].strip()[-500:])
    print("\n" + "-" * 60)
    print("IDENTISCH" if gleich else "ABWEICHUNG")
    if not gleich:
        import difflib
        for z in list(difflib.unified_diff(alt["stdout"].splitlines(),
                                            neu["stdout"].splitlines(),
                                            "alt", "neu", lineterm=""))[:30]:
            print("  " + z)
        for n in sorted(set(alt["datei_hashes"]) | set(neu["datei_hashes"])):
            if alt["datei_hashes"].get(n) != neu["datei_hashes"].get(n):
                print(f"  Datei unterschiedlich: {n}")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    ziel = os.path.join(RESULTS_DIR, f"backtest_regression_{bot}.json")
    with open(ziel, "w", encoding="utf-8") as f:
        json.dump({"bot": bot, "geaenderte_dateien": dateien,
                   "identisch": gleich,
                   "stdout_hash_alt": alt["stdout_hash"],
                   "stdout_hash_neu": neu["stdout_hash"],
                   "datei_hashes_alt": alt["datei_hashes"],
                   "datei_hashes_neu": neu["datei_hashes"],
                   "stdout": neu["stdout"]}, f, indent=2, ensure_ascii=False)
    print(f"geschrieben: {ziel}")
    sys.exit(0 if gleich else 1)


if __name__ == "__main__":
    main()
