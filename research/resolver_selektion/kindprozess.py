#!/usr/bin/env python3
"""
Was im Kindprozess passiert - gemessen, nicht begruendet (TB-52, Teil 1.2)
==============================================================================
Der Selektionslauf startet **Prozesse** (TB-40: ein Prozess je Bot, weil neun
gleichnamige `equity_simulation.py` sich sonst in `sys.modules` verdecken).
Damit stellt sich eine Frage, die man nicht am Quelltext beantworten kann:

    ⚠️ **Erbt ein Kindprozess den Selektionsmodus - und was tut er, wenn
       nicht?**

Beide denkbaren Wege haben ein Loch, und dieses Werkzeug zeigt **beide**:

  * **prozesslokal** (ein Aufruf im Elternprozess): wird **nicht** vererbt.
    Ein Kindprozess, der ihn nicht erbt, liest **still** aus dem
    Live-Bestand - genau die Ausfallform, gegen die die Schicht gebaut wird.
  * **Umgebungsvariable**: wird vererbt - kann aber aus einer frueheren
    Shell **uebrigbleiben**.

⚠️ Gemessen wird an **echten Unterprozessen**, die einen Pfad aufloesen, nicht
an einer Behauptung ueber `os.environ`.

    python3 research/resolver_selektion/kindprozess.py
    python3 research/resolver_selektion/kindprozess.py --json ergebnisse/kindprozess.json

Rueckgabewert 0, wenn alle sieben Messungen das erwartete Verhalten zeigen.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))
_SHARED = os.path.join(_WURZEL, "shared")

sys.path.insert(0, _SHARED)
import paths  # noqa: E402

# Ein Kind, das EINEN Pfad aufloest und sagt, woher er kommt.
_KIND = r'''
import json, os, sys
sys.path.insert(0, %r)
ergebnis = {}
try:
    import paths
    ergebnis["DATA_DIR"] = paths.DATA_DIR
    ergebnis["modus"] = paths.selektionsmodus()
except Exception as fehler:
    ergebnis["fehler"] = "%%s: %%s" %% (type(fehler).__name__, fehler)
json.dump(ergebnis, sys.stdout)
''' % _SHARED

# ⚠️ Dasselbe Kind OHNE `try`. Das obige faengt die Ausnahme ab, um sie
# melden zu koennen - dadurch ist sein Rueckgabewert **immer 0**. Wer "wirft"
# am Rueckgabewert messen will, braucht ein Kind, das nicht abfaengt
# (Prueffrage A1: ein gescheiterter Aufruf und ein leeres Ergebnis sehen
# sonst gleich aus).
_KIND_ROH = r'''
import sys
sys.path.insert(0, %r)
import paths
sys.stdout.write(paths.DATA_DIR)
''' % _SHARED

# Ein Kind, das selbst noch ein Kind startet - zwei Ebenen tief.
_ENKEL = r'''
import json, subprocess, sys
lauf = subprocess.run([sys.executable, "-c", %r],
                      capture_output=True, text=True)
sys.stdout.write(lauf.stdout)
''' % _KIND


def _attrappe():
    """Ein Wegwerf-Ordner mit Manifest.

    ⚠️ **Kein Snapshot von `data/`.** Nach Registertext 5 / F1a wird der
    erst am Tag des signierten Tags gezogen. Hier liegt eine Attrappe mit
    einer erfundenen Datei - sie beantwortet die Frage nach dem Kindprozess
    genauso gut und ruehrt `data/` nicht an.
    """
    ordner = tempfile.mkdtemp(prefix="tb52_attrappe_")
    with open(os.path.join(ordner, "XXXTEST_1d.csv"), "w") as datei:
        datei.write("timestamp,close\n2020-01-01,1.0\n")
    with open(os.path.join(ordner, "MANIFEST.json"), "w") as datei:
        json.dump({"snapshot_hash": "attrappe0000000000000000000000000",
                   "datenstand_hash": "attrappe", "kursdateien": 1,
                   "dateien": {"XXXTEST_1d.csv": {}}}, datei)
    return ordner, "attrappe0000000000000000000000000"


def _ohne_modus(zusatz=None):
    umgebung = dict(os.environ)
    umgebung.pop(paths.UMGEBUNG_WURZEL, None)
    umgebung.pop(paths.UMGEBUNG_HASH, None)
    if zusatz:
        umgebung.update(zusatz)
    return umgebung


def _starte(quelltext, umgebung):
    lauf = subprocess.run([sys.executable, "-c", quelltext],
                          capture_output=True, text=True, env=umgebung)
    try:
        ergebnis = json.loads(lauf.stdout) if lauf.stdout.strip() else {}
    except ValueError:
        ergebnis = {}
    ergebnis["_rc"] = lauf.returncode
    ergebnis["_stderr"] = lauf.stderr.strip()
    return ergebnis


def messen():
    ordner, hash_ = _attrappe()
    live = os.path.join(_WURZEL, "data")
    mit = _ohne_modus({paths.UMGEBUNG_WURZEL: ordner,
                       paths.UMGEBUNG_HASH: hash_})
    messungen = []

    def notiere(nummer, frage, ergebnis, erwartet, trifft, bedeutung):
        messungen.append({"nr": nummer, "frage": frage, "ergebnis": ergebnis,
                          "erwartet": erwartet, "trifft": trifft,
                          "bedeutung": bedeutung})

    # 1 -------------------------------------------------------------------
    k = _starte(_KIND, _ohne_modus())
    notiere(1, "Kind OHNE Modus - wohin zeigt DATA_DIR?",
            k.get("DATA_DIR"), live, k.get("DATA_DIR") == live,
            "Der Regelfall und der Cron-Fall: der Live-Bestand.")

    # 2 -------------------------------------------------------------------
    k = _starte(_KIND, mit)
    notiere(2, "Kind MIT Modus (Umgebungsvariable) - erbt es ihn?",
            k.get("DATA_DIR"), ordner, k.get("DATA_DIR") == ordner,
            "⭐ Die Umgebungsvariable wird vererbt. Das ist der Grund fuer "
            "diesen Weg.")

    # 3 -------------------------------------------------------------------
    e = _starte(_ENKEL, mit)
    notiere(3, "ENKEL MIT Modus - zwei Ebenen tief?",
            e.get("DATA_DIR"), ordner, e.get("DATA_DIR") == ordner,
            "Auch der Kindeskindprozess erbt. Der Selektionslauf darf also "
            "beliebig tief starten.")

    # 4 -------------------------------------------------------------------
    # ⚠️ Der Gegenbeweis fuer den prozesslokalen Weg. Der Elternprozess
    # setzt den Modus NUR in seinem eigenen Speicher; das Kind sieht nichts.
    paths._MODUS = (ordner, hash_)          # nur im Eltern-Speicher
    try:
        k = _starte(_KIND, _ohne_modus())
        still = k.get("DATA_DIR") == live and "fehler" not in k
        notiere(4, "PROZESSLOKALER Modus im Eltern - was tut das Kind?",
                k.get("DATA_DIR"), "%s (STILL falsch)" % live, still,
                "⚠️ **Das Loch des prozesslokalen Wegs, gemessen.** Der Eltern "
                "steht im Modus, das Kind liest den Live-Bestand - ohne "
                "Fehler, ohne Meldung. Genau deshalb faellt dieser Weg aus.")
    finally:
        paths._MODUS = None

    # 5 -------------------------------------------------------------------
    falsch = _ohne_modus({paths.UMGEBUNG_WURZEL: ordner,
                          paths.UMGEBUNG_HASH: "ein_anderer_hash"})
    k = _starte(_KIND_ROH, falsch)
    notiere(5, "Kind erbt einen ANDEREN Hash als der Snapshot traegt",
            "rc=%d, stderr endet auf: %s"
            % (k["_rc"], k["_stderr"].splitlines()[-1][:80]
               if k["_stderr"] else "(leer)"),
            "rc != 0, Selektionsfehler",
            k["_rc"] != 0 and "Selektionsfehler" in k["_stderr"],
            "⭐ Weil der Modus den Hash traegt und nicht nur 'an/aus', ist "
            "ein falsch geerbter Modus ein Abbruch statt eines stillen "
            "Danebengriffs.")

    # 6 -------------------------------------------------------------------
    # Der uebriggebliebene Modus: ein Prozess, der spaeter in derselben
    # Umgebung startet, ohne dass es jemand wollte.
    k = _starte(_KIND, mit)
    sagt_es = "SELEKTIONSMODUS AKTIV" in k["_stderr"]
    notiere(6, "UEBRIGGEBLIEBENER Modus - sagt der Lauf es wenigstens?",
            "stderr: %s" % (k["_stderr"].splitlines()[0][:90]
                            if k["_stderr"] else "(leer)"),
            "eine Zeile auf stderr", sagt_es,
            "⭐ Prueffrage D1. Der Lauf rechnet gegen den Snapshot - aber "
            "**stumm ist er nicht**. Im Cron-Protokoll bliebe eine Spur.")

    # 7 -------------------------------------------------------------------
    # Der Cron-Fall: cron gibt eine MINIMALE Umgebung mit, nicht die der
    # interaktiven Shell. `env -i` bildet das nach.
    leer = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": os.environ.get("HOME", "/root")}
    k = _starte(_KIND, leer)
    notiere(7, "CRON-Nachbildung (leere Umgebung) - traegt sie den Modus?",
            k.get("DATA_DIR"), live, k.get("DATA_DIR") == live,
            "⭐ Ein Cron-Lauf erbt die interaktive Shell nicht. Gegen einen "
            "in einer Shell uebriggebliebenen Modus ist er damit strukturell "
            "geschuetzt. ⚠️ **Nicht** geschuetzt waere er, stuende der Modus "
            "in der Crontab-Zeile selbst oder in einem von dort gesourcten "
            "Profil - das ist das benannte Restloch und gehoert auf den Mac.")

    shutil.rmtree(ordner, ignore_errors=True)
    return messungen


def main(argv=None):
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("--json")
    args = zerleger.parse_args(argv)

    messungen = messen()
    print("=" * 74)
    print("Der Selektionsmodus im Kindprozess - sieben Messungen")
    print("=" * 74)
    for m in messungen:
        print("\n%d) %s" % (m["nr"], m["frage"]))
        print("   gemessen : %s" % m["ergebnis"])
        print("   erwartet : %s" % m["erwartet"])
        print("   %s" % ("✓ trifft" if m["trifft"] else "⚠️ TRIFFT NICHT"))
        print("   %s" % m["bedeutung"])
    daneben = [m["nr"] for m in messungen if not m["trifft"]]
    print("\n" + "=" * 74)
    print("ERGEBNIS: %s" % ("alle 7 Messungen wie erwartet" if not daneben
                            else "⚠️ daneben: %s" % daneben))
    if args.json:
        ziel = args.json if os.path.isabs(args.json) \
            else os.path.join(_HIER, args.json)
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump(messungen, datei, indent=2, ensure_ascii=False)
            datei.write("\n")
        print("JSON: %s" % ziel)
    return 0 if not daneben else 1


if __name__ == "__main__":
    sys.exit(main())
