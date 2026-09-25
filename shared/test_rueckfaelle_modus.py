#!/usr/bin/env python3
"""
Selbsttest zu TB-105 Block C, D und E2-E4: kein Rueckfall und keine Ordner unter dem Modus
==============================================================================
Fable 24b A2: "kein Fallback unter dem Modus, gleich welcher Art";
Fable 25a (A) (iii): ein geschuetzter Lauf legt beim Start nichts im Repo an.

Teil C  Die 14 `__main__`-Bloecke mit "Keine Daten gefunden" + `exit()`:
        unter dem Modus mit leerem Datenbestand Rueckgabe 2 und die Meldung auf
        stderr; ohne Modus Rueckgabe 0 und die Meldung auf stdout wie bisher.
        Eine Mutationsprobe fuer die Bauart (an einer Stelle faellt die
        Modus-Abfrage weg), mit Gegenprobe.
        ⚠️ Die Abfrage steht an jeder Stelle selbst und fragt `paths`, nicht
        `strategy_paths`: kurven_lauf.py, determinismus_lauf.py und
        messung_primaerschluessel.py ersetzen `strategy_paths` durch ein
        Ersatzmodul, das nur `get_strategy_paths` kennt (TB-105 Befund).
Teil D  `shared/symbols_config.py`: eine Universumsdatei, die nur
        ausgeschlossene Symbole enthaelt => unter dem Modus Rueckgabe 2; ohne
        Modus die Standardliste wie bisher. Mutationsprobe mit Gegenprobe.
Teil E  Import eines Bots samt `research/exposure_messung/bot_lauf.py`
        (Bauart Trockenlauf TB-103): unter dem Modus KEIN mkdir im Baum; ohne
        Modus `results/<bot>`, `logs/<bot>` und `research/exposure_messung/daten`
        wie bisher. Zwei Mutationsproben, je eine Datei allein
        (strategy_paths.py, bot_lauf.py), mit Gegenprobe.

Alles laeuft in Wegwerfbaeumen (Kopie von shared/, den Bot-Ordnern, config/,
bot_lauf.py und requirements.lock; git-Repo mit einem Commit, weil die
Startpruefung des Modus die Codeherkunft verlangt) gegen eine Snapshot-
Attrappe OHNE Kursdateien. Jede Probe ist ein eigener Prozess (TB-40).

Aufruf:  python3 shared/test_rueckfaelle_modus.py
"""

import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_HIER)

ATTRAPPEN_HASH = "attrappe_tb105_000000000000000000"
BOTS = sorted(os.path.basename(os.path.dirname(p))
              for p in glob.glob(os.path.join(BASE_DIR, "strategies", "*", "equity_simulation.py")))
# Die 14 Stellen aus TB-104 d3_vier_rueckfaelle.txt Rang 2, aus dem Quelltext
# gefunden (nicht zweimal gefuehrt): Datei traegt "Keine Daten gefunden".
STELLEN = sorted(
    os.path.relpath(p, BASE_DIR)
    for p in glob.glob(os.path.join(BASE_DIR, "strategies", "*", "equity_simulation.py"))
    + glob.glob(os.path.join(BASE_DIR, "strategies", "*", "multi_symbol_optimise.py"))
    if "Keine Daten gefunden" in open(p, encoding="utf-8").read())

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


def _git(wurzel, *argumente):
    lauf = subprocess.run(["git", "-C", wurzel] + list(argumente),
                          capture_output=True, text=True)
    if lauf.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(argumente), lauf.stderr.strip()))
    return lauf.stdout.strip()


_OHNE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.db", "*.csv", "*.log")

# Einstieg fuer Teil D und E (liegt im Baum - die Startpruefung verlangt den
# Einstiegspunkt unter der Git-Wurzel). Audit-Haken auf os.mkdir im Baum.
EINSTIEG = r'''
import json, os, sys
wurzel = os.path.dirname(os.path.abspath(__file__))
art, bot = sys.argv[1], sys.argv[2]
mkdir = []
def haken(ereignis, args):
    if ereignis == "os.mkdir" and args:
        p = os.fsdecode(args[0])
        if p.startswith(wurzel):
            mkdir.append(os.path.relpath(p, wurzel))
sys.addaudithook(haken)
ergebnis = {}
if art == "symbole":
    sys.path.insert(0, os.path.join(wurzel, "shared"))
    import symbols_config
    ergebnis["symbole"] = list(symbols_config.SYMBOLS)
elif art == "bot":
    sys.argv = [os.path.join(wurzel, "research", "exposure_messung", "bot_lauf.py"), bot]
    sys.path.insert(0, os.path.join(wurzel, "research", "exposure_messung"))
    import bot_lauf
    import equity_simulation
ergebnis["mkdir"] = sorted(set(mkdir))
json.dump(ergebnis, sys.stdout)
'''


def baue_baum(arbeit, name, aendern=None):
    """Wegwerfbaum, optional mit einer Aenderung (relpfad, alt, neu) vor dem Commit."""
    w = os.path.join(os.path.realpath(arbeit), name)
    os.makedirs(w)
    shutil.copytree(os.path.join(BASE_DIR, "shared"), os.path.join(w, "shared"), ignore=_OHNE)
    for bot in BOTS:
        shutil.copytree(os.path.join(BASE_DIR, "strategies", bot),
                        os.path.join(w, "strategies", bot), ignore=_OHNE)
    shutil.copytree(os.path.join(BASE_DIR, "config"), os.path.join(w, "config"), ignore=_OHNE)
    os.makedirs(os.path.join(w, "research", "exposure_messung"))
    shutil.copy2(os.path.join(BASE_DIR, "research", "exposure_messung", "bot_lauf.py"),
                 os.path.join(w, "research", "exposure_messung", "bot_lauf.py"))
    shutil.copy2(os.path.join(BASE_DIR, "requirements.lock"), os.path.join(w, "requirements.lock"))
    os.makedirs(os.path.join(w, "data"))  # leer: kein Kursbestand
    with open(os.path.join(w, "einstieg.py"), "w", encoding="utf-8") as f:
        f.write(EINSTIEG)
    griff = True
    if aendern:
        rel, alt, neu = aendern
        pfad = os.path.join(w, rel)
        text = open(pfad, encoding="utf-8").read()
        griff = text.count(alt) == 1
        with open(pfad, "w", encoding="utf-8") as f:
            f.write(text.replace(alt, neu))
    _git(w, "init", "-q")
    _git(w, "add", "-A")
    _git(w, "-c", "user.name=tb105_test", "-c", "user.email=tb105@test",
         "commit", "-q", "-m", "Wegwerfbaum")
    return w, griff


def baue_attrappe(arbeit, name, universum):
    """Snapshot-Attrappe OHNE Kursdateien; Universumsdateien unter config/."""
    a = os.path.join(os.path.realpath(arbeit), name)
    os.makedirs(os.path.join(a, "config"))
    for rel, text in universum.items():
        with open(os.path.join(a, rel), "w", encoding="utf-8") as f:
            f.write(text)
    with open(os.path.join(a, "MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump({"snapshot_hash": ATTRAPPEN_HASH, "datenstand_hash": "egal",
                   "kursdateien": 0, "dateien": {rel: {} for rel in universum}}, f)
    return a


def lauf(baum, argumente, attrappe=None):
    umgebung = dict(os.environ)
    for k in ("TB_SELEKTIONSWURZEL", "TB_SELEKTIONSHASH", "TB_SELEKTIONSCOMMIT"):
        umgebung.pop(k, None)
    if attrappe:
        umgebung["TB_SELEKTIONSWURZEL"] = attrappe
        umgebung["TB_SELEKTIONSHASH"] = ATTRAPPEN_HASH
        umgebung["TB_SELEKTIONSCOMMIT"] = _git(baum, "rev-parse", "HEAD")
    r = subprocess.run([sys.executable, "-W", "ignore"] + argumente,
                       capture_output=True, text=True, cwd=baum, env=umgebung)
    return r.returncode, r.stdout, r.stderr


def echtes_universum():
    return {"config/top25_symbols.txt":
                open(os.path.join(BASE_DIR, "config", "top25_symbols.txt")).read(),
            "config/sp500_top150.txt":
                open(os.path.join(BASE_DIR, "config", "sp500_top150.txt")).read()}


def teil_c(arbeit):
    print("\nTeil C - 'Keine Daten gefunden' unter dem Modus: Rueckgabe 2")
    pruefe("C0 vierzehn Stellen", len(STELLEN) == 14, str(len(STELLEN)))
    baum, _ = baue_baum(arbeit, "c")
    attrappe = baue_attrappe(arbeit, "c_snap", echtes_universum())
    for rel in STELLEN:
        rc, out, err = lauf(baum, [os.path.join(baum, rel)], attrappe)
        pruefe("C1 %s: Modus, leerer Bestand => rc 2, Meldung auf stderr" % rel,
               rc == 2 and "Keine Daten gefunden" in err and "Keine Daten gefunden" not in out,
               "rc %d, stderr %r" % (rc, err.strip()[-200:]))
        rc, out, err = lauf(baum, [os.path.join(baum, rel)])
        pruefe("C2 %s: ohne Modus => rc 0, Meldung auf stdout wie bisher" % rel,
               rc == 0 and "Keine Daten gefunden" in out,
               "rc %d, stdout %r, stderr %r" % (rc, out.strip()[-160:], err.strip()[-160:]))
    # Mutation der Bauart (eine, nicht vierzehn): an einer Stelle faellt die
    # Modus-Abfrage weg.
    probe = STELLEN[0]
    # TB-109: seit Block B steht dieselbe Abfrage auch an der Stelle "Keine
    # Trades" derselben Datei - das Muster nennt deshalb die Meldung mit.
    alt = "        if paths.selektionsmodus() is not None:\n            sys.stderr.write(\"Keine Daten"
    neu = "        if False:\n            sys.stderr.write(\"Keine Daten"
    baum_m, griff = baue_baum(arbeit, "c_mut", (probe, alt, neu))
    pruefe("C3 Mutation 'Modus-Abfrage weg' griff", griff)
    rc, out, err = lauf(baum_m, [os.path.join(baum_m, probe)], attrappe)
    pruefe("C3 Mutation => Probe C1 rot (rc 0 statt 2)", rc != 2, "rc %d" % rc)
    rc, out, err = lauf(baum, [os.path.join(baum, probe)], attrappe)
    pruefe("C3 Gegenprobe: unveraenderter Baum => rc 2", rc == 2, "rc %d" % rc)


def teil_d(arbeit):
    print("\nTeil D - symbols_config: nach EXCLUDE_SYMBOLS leer")
    nur_ausgeschlossen = "XAUTUSDT\nPAXGUSDT\n"
    uni = dict(echtes_universum(), **{"config/top25_symbols.txt": nur_ausgeschlossen})
    attrappe = baue_attrappe(arbeit, "d_snap", uni)
    baum, _ = baue_baum(arbeit, "d")
    rc, out, err = lauf(baum, ["einstieg.py", "symbole", "-"], attrappe)
    pruefe("D1 Modus, nur ausgeschlossene Symbole => rc 2",
           rc == 2 and "kein Symbol" in err, "rc %d, %r" % (rc, err.strip()[-200:]))
    pruefe("D1b keine Standardliste gedruckt", "Standardliste (5 Symbole)" not in out, out[-200:])
    # Ohne Modus: dieselbe Datei im Live-config/ des Baums -> Standardliste wie bisher.
    with open(os.path.join(baum, "config", "top25_symbols.txt"), "w") as f:
        f.write(nur_ausgeschlossen)
    rc, out, err = lauf(baum, ["einstieg.py", "symbole", "-"])
    try:
        symbole = json.loads(out.strip().splitlines()[-1]).get("symbole")
    except (ValueError, IndexError):
        symbole = None
    pruefe("D2 ohne Modus => Standardliste wie bisher, rc 0",
           rc == 0 and symbole == ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
           and "nicht gefunden" in out, "rc %d, %r" % (rc, out[-200:]))
    # Gegenprobe: Modus mit echter Liste -> rc 0, Liste = Datei ohne Ausschluss.
    attrappe_ok = baue_attrappe(arbeit, "d_snap_ok", echtes_universum())
    baum_ok, _ = baue_baum(arbeit, "d_ok")
    rc, out, err = lauf(baum_ok, ["einstieg.py", "symbole", "-"], attrappe_ok)
    erwartet = [s.strip() for s in echtes_universum()["config/top25_symbols.txt"].splitlines()
                if s.strip() and s.strip() not in ("XAUTUSDT", "PAXGUSDT")]
    try:
        symbole = json.loads(out.strip().splitlines()[-1]).get("symbole")
    except (ValueError, IndexError):
        symbole = None
    pruefe("D3 Gegenprobe: Modus mit echter Liste => rc 0, Liste = Datei", rc == 0 and symbole == erwartet,
           "rc %d, %r" % (rc, err.strip()[-200:]))
    # Mutation: der Modus-Zweig faellt weg.
    baum_m, griff = baue_baum(arbeit, "d_mut", ("shared/symbols_config.py",
                                                "    if selektionsmodus() is not None:\n",
                                                "    if False:\n"))
    pruefe("D4 Mutation 'Modus-Zweig weg' griff", griff)
    rc, out, err = lauf(baum_m, ["einstieg.py", "symbole", "-"], attrappe)
    pruefe("D4 Mutation => Probe D1 rot (rc 0, Standardliste)", rc != 2, "rc %d" % rc)


def teil_e(arbeit):
    print("\nTeil E - Import eines Bots: Ordneranlage nur ohne Modus")
    attrappe = baue_attrappe(arbeit, "e_snap", echtes_universum())
    bot = "t3_supertrend"
    betrieb = sorted(["results/" + bot, "logs/" + bot, "research/exposure_messung/daten"])

    def mkdirs(baum, modus):
        rc, out, err = lauf(baum, ["einstieg.py", "bot", bot], attrappe if modus else None)
        try:
            return rc, json.loads(out.strip().splitlines()[-1]).get("mkdir"), err
        except (ValueError, IndexError):
            return rc, None, err

    baum, _ = baue_baum(arbeit, "e")
    rc, m, err = mkdirs(baum, True)
    pruefe("E1 Modus: Import rc 0", rc == 0, "rc %d, %r" % (rc, err.strip()[-200:]))
    pruefe("E2 Modus: 0 angelegte Ordner im Baum", m == [], str(m))
    rc, m, err = mkdirs(baum, False)
    pruefe("E3 ohne Modus: results/<bot>, logs/<bot>, exposure_messung/daten wie bisher",
           rc == 0 and m is not None and all(b in m for b in betrieb), "rc %d, %s" % (rc, m))

    for name, rel, alt, neu, erwartet, andere in [
        ("E4 Mutation strategy_paths.py: Anlage auch unter dem Modus", "shared/strategy_paths.py",
         "    if not _im_selektionsmodus():\n        os.makedirs(results_dir",
         "    if True:\n        os.makedirs(results_dir", "results/" + bot,
         "research/exposure_messung/daten"),
        ("E5 Mutation bot_lauf.py: Anlage auch unter dem Modus", "research/exposure_messung/bot_lauf.py",
         "if paths.selektionsmodus() is None:\n    os.makedirs(DATEN_DIR",
         "if True:\n    os.makedirs(DATEN_DIR", "research/exposure_messung/daten",
         "results/" + bot),
    ]:
        baum_m, griff = baue_baum(arbeit, "e_mut_" + rel.replace("/", "_"), (rel, alt, neu))
        pruefe(name + ": griff", griff)
        rc, m, err = mkdirs(baum_m, True)
        pruefe(name + " => Probe E2 rot", m is not None and erwartet in m, str(m))
        # Jede Mutation beisst allein (24b B3): die jeweils andere Stelle
        # bleibt unter dem Modus stumm.
        pruefe(name + ": die andere Stelle bleibt stumm",
               m is not None and andere not in m, str(m))
    rc, m, err = mkdirs(baum, True)
    pruefe("E6 Gegenprobe: unveraenderter Baum unter dem Modus weiter 0 Ordner", m == [], str(m))


def main():
    print(__doc__.strip().split("\n")[0])
    arbeit = tempfile.mkdtemp(prefix="tb105_rueckfaelle_")
    try:
        teil_c(arbeit)
        teil_d(arbeit)
        teil_e(arbeit)
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)
    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
