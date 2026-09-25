#!/usr/bin/env python3
"""
TB-107 Block E / TB-109 Block C - die Zwischenablagen von `universum_trockenlauf.py`
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

TB-109 Block C (Fable 25e (1)): die zwei weiteren Ablagen derselben Datei,
dieselbe Bauart.
  C-fa  `hole_faltenplan()` ohne JSON: nach dem Lesen kein `tb40_faltenplan_*`.
  C-fb  Faltenplan ohne Ergebnis: `RuntimeError`, der Ordner ist da, sein Pfad
        steht in der Meldung.
  C-faM Mutationsprobe "Aufraeumen weg" in `hole_faltenplan()`, mit Gegenprobe.
  C-pa  `stille_filter()`: nach dem Lauf kein `tb40_proben_*` (und kein
        `tb40_lauf_*`).
  C-pb  Probelauf ohne Ergebnis: `RuntimeError`, der Ordner `tb40_proben_*`
        ist da, sein Pfad steht in der Meldung.
  C-paM Mutationsprobe "Aufraeumen weg" in `stille_filter()`, mit Gegenprobe.
Die Mutation wird nur im Rumpf der jeweiligen Funktion gesetzt (dieselbe
Zeile `shutil.rmtree(ordner)` steht in allen drei Funktionen).

Jede Probe laeuft als eigener Prozess mit einem EIGENEN `TMPDIR`, damit nur
die Ordner dieses einen Aufrufs gezaehlt werden. Statt des echten
`loaderlauf.py` liegt neben der Kopie von `universum_trockenlauf.py` eine
Attrappe, die nur `--aus` beschreibt (oder, fuer E-b, nichts); gemessen wird
die Ablage, nicht der Loader. Fuer C-f* ersetzt der Treiber `FALTENPLAN`
durch eine Attrappe, die nur `--json` beschreibt (oder nichts).

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
# der Bot heisst "ohne_ergebnis" (oder "ohne_ergebnis_proben" und der Aufruf
# traegt --daten). TB-109: dazu die Schranken und, mit --daten, einen Lauf -
# das braucht `stille_filter()`.
_LOADER = r'''
import json, sys
a = sys.argv[1:]
bot, aus = a[a.index("--bot") + 1], a[a.index("--aus") + 1]
if bot == "ohne_ergebnis" or (bot == "ohne_ergebnis_proben" and "--daten" in a):
    print("Attrappe: kein Ergebnis")
    sys.exit(1)
ergebnis = {"bot": bot, "laeufe": [], "fehler": None,
            "schranken": {"SYMBOLE": ["S%d" % i for i in range(8)], "INTERVAL": "1d",
                          "MIN_HISTORY_DAYS": 3}}
if "--daten" in a:
    ergebnis["laeufe"] = [{"symbole": [], "ausgabe": ""}]
with open(aus, "w") as f:
    json.dump(ergebnis, f)
'''

# Die Attrappe von faltenplan_neun.py: schreibt nach --json, ausser die
# Umgebung verlangt "kein Ergebnis".
_FALTENPLAN = r'''
import json, os, sys
if os.environ.get("TB109_OHNE_ERGEBNIS"):
    print("Attrappe: kein Faltenplan")
    sys.exit(1)
with open(sys.argv[sys.argv.index("--json") + 1], "w") as f:
    json.dump({"plaene": {"attrappe": True}}, f)
'''

_TREIBER = r'''
import json, os, sys
sys.path.insert(0, sys.argv[1])
import universum_trockenlauf as ut
ut.FALTENPLAN = os.path.join(sys.argv[1], "faltenplan_attrappe.py")
art, bot = sys.argv[2], sys.argv[3]
try:
    if art == "messe_bot":
        e = ut.messe_bot(bot, [])
    elif art == "faltenplan":
        e = ut.hole_faltenplan()
    else:
        e = ut.stille_filter([bot])
    print(json.dumps({"ergebnis": e}))
except RuntimeError as fehler:
    print(json.dumps({"fehler": str(fehler)}))
'''

# Die Stelle, die die Mutationsprobe zuruecknimmt: das Entfernen - je
# Funktion (Name, Zeile). TB-109: die Zeile steht jetzt in drei Funktionen,
# gesucht wird deshalb nur im Rumpf der genannten.
AUFRAEUMEN = {
    "messe_bot": "        shutil.rmtree(ordner)\n",
    "hole_faltenplan": "        shutil.rmtree(ordner)\n",
    "stille_filter": "            shutil.rmtree(ordner)\n",
}


def _in_funktion(text, funktion, alt, neu):
    """`alt` -> `neu`, nur im Rumpf von `def funktion(` bis zum naechsten
    `def` auf Spalte 0. Bricht ab, wenn `alt` dort nicht genau einmal steht."""
    anfang = text.index("\ndef %s(" % funktion)
    ende = text.find("\ndef ", anfang + 1)
    ende = len(text) if ende < 0 else ende
    rumpf = text[anfang:ende]
    if rumpf.count(alt) != 1:
        raise AssertionError("Mutationsstelle in %s nicht genau einmal: %r" % (funktion, alt))
    return text[:anfang] + rumpf.replace(alt, neu, 1) + text[ende:]


def _lauf(bot, mutieren=False, art="messe_bot", praefix="tb40_lauf_", umgebung_extra=None):
    import json
    funktion = {"messe_bot": "messe_bot", "faltenplan": "hole_faltenplan",
                "stille_filter": "stille_filter"}[art]
    with tempfile.TemporaryDirectory() as t:
        kopie = os.path.join(t, "werkzeug")
        eigenes_tmp = os.path.join(t, "tmp")
        os.makedirs(kopie)
        os.makedirs(eigenes_tmp)
        with open(_WERKZEUG, encoding="utf-8") as f:
            text = f.read()
        zeile = AUFRAEUMEN[funktion]
        # Die Stelle wird immer gesucht (genau einmal im Rumpf), gesetzt nur mit mutieren.
        text_mut = _in_funktion(text, funktion, zeile, zeile.replace("shutil.rmtree(ordner)", "pass"))
        if mutieren:
            text = text_mut
        with open(os.path.join(kopie, "universum_trockenlauf.py"), "w", encoding="utf-8") as f:
            f.write(text)
        with open(os.path.join(kopie, "loaderlauf.py"), "w", encoding="utf-8") as f:
            f.write(_LOADER)
        with open(os.path.join(kopie, "faltenplan_attrappe.py"), "w", encoding="utf-8") as f:
            f.write(_FALTENPLAN)
        umgebung = {k: v for k, v in os.environ.items()
                    if not k.startswith("TB_SELEKTIONS")}
        umgebung["TMPDIR"] = eigenes_tmp
        umgebung.update(umgebung_extra or {})
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", _TREIBER, kopie, art, bot],
                           capture_output=True, text=True, env=umgebung)
        ordner = sorted(glob.glob(os.path.join(eigenes_tmp, praefix + "*")))
        alle = sorted(glob.glob(os.path.join(eigenes_tmp, "tb40_*")))
        try:
            aus = json.loads(r.stdout) if r.stdout.strip() else {}
        except ValueError:
            aus = {}
        return {"rc": r.returncode, "aus": aus, "ordner": ordner, "alle": alle,
                "err": r.stderr[-400:]}


def _pfad_in_meldung(r, praefix):
    fehler = r["aus"].get("fehler", "")
    genannt = {os.path.realpath(w.strip(" :\n")) for w in fehler.split() if praefix in w}
    return len(r["ordner"]) == 1 and os.path.realpath(r["ordner"][0]) in genannt


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

    # --- TB-109 Block C: tb40_faltenplan_* ------------------------------------
    F = "tb40_faltenplan_"
    r = _lauf("-", art="faltenplan", praefix=F)
    pruefe("C-fa: hole_faltenplan() ohne JSON - Ergebnis gelesen, danach kein tb40_faltenplan_* mehr",
           r["rc"] == 0 and r["aus"].get("ergebnis") == {"plaene": {"attrappe": True}}
           and r["ordner"] == [] and r["alle"] == [], _info(r))
    r = _lauf("-", art="faltenplan", praefix=F, umgebung_extra={"TB109_OHNE_ERGEBNIS": "1"})
    pruefe("C-fb: Faltenplan ohne Ergebnis - RuntimeError, Ordner steht, Pfad in der Meldung",
           r["rc"] == 0 and "Ablage bleibt stehen" in r["aus"].get("fehler", "")
           and _pfad_in_meldung(r, F), _info(r))
    _mit_gegenprobe(
        "C-faM", "Mutationsprobe 'Aufraeumen weg' in hole_faltenplan() - C-fa waere rot",
        lambda mut: _lauf("-", mutieren=mut, art="faltenplan", praefix=F),
        lambda r: r["rc"] == 0 and len(r["ordner"]) == 1, _info)

    # --- TB-109 Block C: tb40_proben_* ----------------------------------------
    P = "tb40_proben_"
    r = _lauf("attrappe_bot", art="stille_filter", praefix=P)
    pruefe("C-pa: stille_filter() - Ergebnis gelesen, danach kein tb40_proben_* und kein tb40_lauf_* mehr",
           r["rc"] == 0 and "attrappe_bot" in (r["aus"].get("ergebnis") or {})
           and r["ordner"] == [] and r["alle"] == [], _info(r))
    r = _lauf("ohne_ergebnis_proben", art="stille_filter", praefix=P)
    pruefe("C-pb: Probelauf ohne Ergebnis - RuntimeError, tb40_proben_* steht, Pfad in der Meldung",
           r["rc"] == 0 and "Ablage bleibt stehen" in r["aus"].get("fehler", "")
           and _pfad_in_meldung(r, P), _info(r))
    _mit_gegenprobe(
        "C-paM", "Mutationsprobe 'Aufraeumen weg' in stille_filter() - C-pa waere rot",
        lambda mut: _lauf("attrappe_bot", mutieren=mut, art="stille_filter", praefix=P),
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
