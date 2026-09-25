#!/usr/bin/env python3
"""
TB-107 Block E - die Zwischenablage `tb40_lauf_*` von `messe_bot()`
==============================================================================
`universum_trockenlauf.messe_bot()` legt je Bot mit `tempfile.mkdtemp` einen
Ordner `tb40_lauf_*` an; der Kindprozess `loaderlauf.py` schreibt sein
Ergebnis-JSON hinein. Bis TB-107 blieb der Ordner nach jedem Lauf liegen
(Fable 25b 3 (1): Klasse (iv) Zwischenablage, "nie entfernt" ist Befund 1).
Jetzt wird er entfernt, nachdem das Ergebnis gelesen ist. Kommt der
Kindprozess ohne Ergebnis zurueck, bleibt er stehen, und sein Pfad steht in
der Meldung (25b Bedingung (3): "entfernt oder Pfad im Beleg").

  E-a  Normallauf: nach `messe_bot()` existiert der Ordner nicht mehr.
  E-b  Kindprozess ohne Ergebnis: `RuntimeError`, der Ordner ist da, und sein
       Pfad steht in der Meldung.
  E-aM Mutationsprobe "Aufraeumen weg": E-a waere rot. Mit Gegenprobe
       (Register 40.7): ohne die Mutation scheitert sie.

Jede Probe laeuft als eigener Prozess mit einem EIGENEN `TMPDIR`, damit nur
die Ordner dieses einen Aufrufs gezaehlt werden. Statt des echten
`loaderlauf.py` liegt neben der Kopie von `universum_trockenlauf.py` eine
Attrappe, die nur `--aus` beschreibt (oder, fuer E-b, nichts); gemessen wird
die Ablage, nicht der Loader.

Aufruf: trading-env/bin/python3 research/universum_trockenlauf/test_zwischenablage.py
"""

import glob
import os
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_WERKZEUG = os.path.join(_HIER, "universum_trockenlauf.py")

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print(f"  [ok]     {name}")
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")
        print(f"  [FEHLER] {name}{(' - ' + zusatz) if zusatz else ''}")


def _mit_gegenprobe(name, text, lauf, bedingung, zusatz=lambda r: ""):
    r = lauf(True)
    pruefe(f"{name}: {text}", bedingung(r), zusatz(r))
    g = lauf(False)
    pruefe(f"{name}-G: Gegenprobe zu {name} - ohne die Mutation scheitert sie",
           not bedingung(g), zusatz(g))


# Die Attrappe von loaderlauf.py: schreibt ein Ergebnis nach --aus, ausser
# der Bot heisst "ohne_ergebnis".
_LOADER = r'''
import json, sys
a = sys.argv[1:]
bot, aus = a[a.index("--bot") + 1], a[a.index("--aus") + 1]
if bot == "ohne_ergebnis":
    print("Attrappe: kein Ergebnis")
    sys.exit(1)
with open(aus, "w") as f:
    json.dump({"bot": bot, "laeufe": [], "fehler": None}, f)
'''

_TREIBER = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import universum_trockenlauf as ut
try:
    print(json.dumps({"ergebnis": ut.messe_bot(sys.argv[2], [])}))
except RuntimeError as fehler:
    print(json.dumps({"fehler": str(fehler)}))
'''

# Die Stelle, die die Mutationsprobe zuruecknimmt: das Entfernen.
AUFRAEUMEN_NEU = "        shutil.rmtree(ordner)\n"
AUFRAEUMEN_ALT = "        pass\n"


def _lauf(bot, mutieren=False, stelle_pruefen=True):
    import json
    with tempfile.TemporaryDirectory() as t:
        kopie = os.path.join(t, "werkzeug")
        eigenes_tmp = os.path.join(t, "tmp")
        os.makedirs(kopie)
        os.makedirs(eigenes_tmp)
        with open(_WERKZEUG, encoding="utf-8") as f:
            text = f.read()
        if stelle_pruefen and text.count(AUFRAEUMEN_NEU) != 1:
            raise AssertionError("Mutationsstelle nicht genau einmal: %r" % AUFRAEUMEN_NEU)
        if mutieren:
            text = text.replace(AUFRAEUMEN_NEU, AUFRAEUMEN_ALT, 1)
        with open(os.path.join(kopie, "universum_trockenlauf.py"), "w", encoding="utf-8") as f:
            f.write(text)
        with open(os.path.join(kopie, "loaderlauf.py"), "w", encoding="utf-8") as f:
            f.write(_LOADER)
        umgebung = {k: v for k, v in os.environ.items()
                    if not k.startswith("TB_SELEKTIONS")}
        umgebung["TMPDIR"] = eigenes_tmp
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", _TREIBER, kopie, bot],
                           capture_output=True, text=True, env=umgebung)
        ordner = sorted(glob.glob(os.path.join(eigenes_tmp, "tb40_lauf_*")))
        try:
            aus = json.loads(r.stdout) if r.stdout.strip() else {}
        except ValueError:
            aus = {}
        return {"rc": r.returncode, "aus": aus, "ordner": ordner,
                "err": r.stderr[-400:]}


def _info(r):
    return f"rc {r['rc']}; Ordner {r['ordner']}; aus {str(r['aus'])[:200]}; stderr {r['err'][-200:]!r}"


def main():
    print(__doc__.strip().split("\n")[0])

    r = _lauf("attrappe_bot")
    pruefe("E-a: Normallauf - Ergebnis gelesen, danach kein tb40_lauf_* mehr",
           r["rc"] == 0 and r["aus"].get("ergebnis", {}).get("bot") == "attrappe_bot"
           and r["ordner"] == [], _info(r))

    r = _lauf("ohne_ergebnis")
    fehler = r["aus"].get("fehler", "")
    pruefe("E-b: Kindprozess ohne Ergebnis - RuntimeError, Ordner steht, Pfad in der Meldung",
           r["rc"] == 0 and "ohne Ergebnis" in fehler and len(r["ordner"]) == 1
           and os.path.realpath(r["ordner"][0]) in {os.path.realpath(p) for p in [
               w.strip(" :\n") for w in fehler.split() if "tb40_lauf_" in w]},
           _info(r))

    _mit_gegenprobe(
        "E-aM", "Mutationsprobe 'Aufraeumen weg' - der Ordner bliebe liegen, E-a waere rot",
        lambda mut: _lauf("attrappe_bot", mutieren=mut),
        lambda r: r["rc"] == 0 and len(r["ordner"]) == 1, _info)

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
