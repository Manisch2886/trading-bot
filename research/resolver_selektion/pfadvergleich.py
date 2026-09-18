#!/usr/bin/env python3
"""
Pfadvergleich alt gegen neu - die Bedingung, an der die TB-52-Freigabe haengt
==============================================================================
`shared/paths.py` wird von **145 Modulen** importiert und laeuft im Cron. Die
Freigabe fuer den Selektionsmodus haengt an einer einzigen Bedingung:

    ⭐ **Ohne gesetzten Modus liefert das Modul dieselben Zeichenketten wie
       vorher - fuer alle neun Bots und alle Pfadarten.**

Dieses Werkzeug misst das, statt es zu behaupten.

**Wie gemessen wird** (und warum so):

  * Die **alte** Fassung kommt aus `git show <BEZUGSCOMMIT>:shared/paths.py`,
    nicht aus dem Gedaechtnis und nicht aus einer Kopie im Arbeitsbaum.
  * Beide Fassungen laufen in **je einem eigenen Prozess** - ein Import ist
    keine Leseoperation (Prueffrage B6), und zwei Fassungen desselben Moduls
    im selben `sys.modules` verdecken sich gegenseitig (TB-40).
  * Beide liegen in **je einem eigenen Wegwerfbaum** mit gleicher Form
    (`<wurzel>/shared/paths.py`, `<wurzel>/strategies/<bot>/`). Nur so haben
    beide Fassungen dieselbe `BASE_DIR` und die Zeichenketten sind direkt
    vergleichbar. ⚠️ **Der Arbeitsbaum wird dabei nicht angefasst** - und
    `data/` bleibt unberuehrt.
  * Verglichen wird je Bot aus **der Sicht dieses Bots**: der Probeprozess
    baut `sys.path` genau so auf, wie die Bot-Dateien es tun
    (`_SHARED_DIR` aus dem eigenen Ordner abgeleitet).
  * Zusaetzlich `shared/strategy_paths.py` mit seinen sieben Schluesseln je
    Bot. Es ist **nicht** geaendert worden; es steht hier als Kontrolle, dass
    die Bot-Pfade als Ganzes stehen bleiben, nicht nur die vier aus `paths`.

⚠️ **Und das Werkzeug prueft sich selbst** (Prueffrage A5, B1): Es laeuft
denselben Vergleich ein zweites Mal gegen eine **absichtlich verstellte** alte
Fassung. Findet es dort **keinen** Unterschied, misst es nichts - dann ist der
Ausgang NICHT PRUEFBAR, nicht gruen.

    python3 research/resolver_selektion/pfadvergleich.py
    python3 research/resolver_selektion/pfadvergleich.py --json ergebnisse/pfadvergleich.json

Rueckgabewert 0 nur, wenn es **null** Unterschiede gab **und** die
Selbstprobe angeschlagen hat.
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

# ⚠️ Festgenagelt (Prueffrage B3): ein beweglicher Bezug wie `origin/main`
# macht den Vergleich nach einem Merge trivial gruen. Ist der Commit nicht zu
# finden, ist das Ergebnis NICHT PRUEFBAR (A2), nicht gruen.
BEZUGSCOMMIT = "062bacf62638f41df55d3f861feb4f6281fdef18"

BOTS = (
    "elliott_wave",
    "elliott_wave_stocks",
    "rsi2_crypto",
    "rsi2_mean_reversion",
    "t3_supertrend",
    "turtle_soup_crypto",
    "turtle_soup_stocks",
    "volatility_breakout",
    "volatility_breakout_crypto",
)

# Die Pfadarten, die die ALTE Fassung liefert. ⚠️ Genau diese werden
# verglichen - neue Namen der neuen Fassung sind Zugaenge, keine
# Unterschiede, und werden eigens ausgewiesen.
ALTE_NAMEN = ("SHARED_DIR", "BASE_DIR", "DATA_DIR", "CONFIG_DIR")

NICHT_PRUEFBAR = 2

# Der Probeprozess. Er nimmt die Sicht EINES Bots ein und schreibt jede
# oeffentliche Zeichenkette des Moduls als JSON auf die Standardausgabe.
_PROBE = r'''
import json, os, sys
bot_dir = sys.argv[1]
# ⚠️ Genau die vier Zeilen Vorspann, die jede Bot-Datei dieses Projekts traegt.
_STRATEGY_DIR = os.path.dirname(os.path.abspath(os.path.join(bot_dir, "x.py")))
_SHARED_DIR = os.path.join(
    os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

import paths
werte = {}
for name in sorted(dir(paths)):
    if name.startswith("_"):
        continue
    wert = getattr(paths, name)
    if isinstance(wert, str):
        werte["paths." + name] = wert

import strategy_paths
for schluessel, wert in sorted(
        strategy_paths.get_strategy_paths(
            os.path.join(bot_dir, "forward_test.py")).items()):
    werte["strategy_paths." + schluessel] = wert

json.dump(werte, sys.stdout)
'''


def _baum(paths_quelle):
    """Ein Wegwerfbaum in der Form des Projekts, mit dieser `paths.py`."""
    wurzel = tempfile.mkdtemp(prefix="tb52_vergleich_")
    os.makedirs(os.path.join(wurzel, "shared"))
    with open(os.path.join(wurzel, "shared", "paths.py"), "w",
              encoding="utf-8") as datei:
        datei.write(paths_quelle)
    shutil.copy2(os.path.join(_WURZEL, "shared", "strategy_paths.py"),
                 os.path.join(wurzel, "shared", "strategy_paths.py"))
    for bot in BOTS:
        os.makedirs(os.path.join(wurzel, "strategies", bot))
    # ⚠️ `data/` und `config/` werden hier ANGELEGT - sonst misst der
    # Vergleich versehentlich den Unterschied aus T46.8 mit, statt die
    # Zeichenketten. T46.8 hat seine eigene Probe in `shared/test_paths.py`.
    os.makedirs(os.path.join(wurzel, "data"))
    os.makedirs(os.path.join(wurzel, "config"))
    return wurzel


def _messen(wurzel, bot):
    """Alle Zeichenketten aus der Sicht eines Bots - oder ein Fehler."""
    umgebung = dict(os.environ)
    # ⚠️ Ohne gesetzten Modus - das ist die Bedingung, die geprueft wird.
    umgebung.pop("TB_SELEKTIONSWURZEL", None)
    umgebung.pop("TB_SELEKTIONSHASH", None)
    lauf = subprocess.run(
        [sys.executable, "-c", _PROBE, os.path.join(wurzel, "strategies", bot)],
        capture_output=True, text=True, env=umgebung)
    if lauf.returncode != 0:
        # Prueffrage A1: ein gescheiterter Aufruf ist kein leeres Ergebnis.
        raise RuntimeError("Probe fuer %s scheiterte (rc=%d): %s"
                           % (bot, lauf.returncode, lauf.stderr.strip()[-500:]))
    return json.loads(lauf.stdout)


def _ersetze_wurzel(werte, wurzel):
    """Den Baumpfad durch `<WURZEL>` ersetzen - sonst vergleicht man Tempnamen."""
    return {k: v.replace(wurzel, "<WURZEL>") for k, v in werte.items()}


def vergleiche(alt_quelle, neu_quelle):
    """Beide Fassungen ueber alle Bots messen und gegenueberstellen."""
    baum_alt = _baum(alt_quelle)
    baum_neu = _baum(neu_quelle)
    try:
        unterschiede = []
        verglichen = 0
        nur_neu = set()
        je_bot = {}
        for bot in BOTS:
            alt = _ersetze_wurzel(_messen(baum_alt, bot), baum_alt)
            neu = _ersetze_wurzel(_messen(baum_neu, bot), baum_neu)
            nur_neu |= set(neu) - set(alt)
            for name in sorted(alt):
                verglichen += 1
                if name not in neu:
                    unterschiede.append(
                        {"bot": bot, "name": name, "alt": alt[name],
                         "neu": "<FEHLT IN DER NEUEN FASSUNG>"})
                elif alt[name] != neu[name]:
                    unterschiede.append(
                        {"bot": bot, "name": name, "alt": alt[name],
                         "neu": neu[name]})
            je_bot[bot] = alt
        return {"verglichen": verglichen, "unterschiede": unterschiede,
                "nur_in_neu": sorted(nur_neu), "werte": je_bot}
    finally:
        shutil.rmtree(baum_alt, ignore_errors=True)
        shutil.rmtree(baum_neu, ignore_errors=True)


def alte_fassung():
    """Die alte `paths.py` aus dem festgenagelten Commit - oder None."""
    lauf = subprocess.run(
        ["git", "-C", _WURZEL, "show", "%s:shared/paths.py" % BEZUGSCOMMIT],
        capture_output=True, text=True)
    if lauf.returncode != 0 or not lauf.stdout.strip():
        return None
    return lauf.stdout


def main(argv=None):
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("--json", help="Ergebnis zusaetzlich als JSON")
    args = zerleger.parse_args(argv)

    alt = alte_fassung()
    if alt is None:
        print("NICHT PRUEFBAR: %s:shared/paths.py ist nicht zu finden."
              % BEZUGSCOMMIT[:8])
        print("Der Bezug ist festgenagelt (B3) - ohne ihn wird hier nichts "
              "behauptet.")
        return NICHT_PRUEFBAR
    with open(os.path.join(_WURZEL, "shared", "paths.py"), encoding="utf-8") as d:
        neu = d.read()

    ergebnis = vergleiche(alt, neu)

    # --- Die Selbstprobe (A5/B1): sieht das Werkzeug ueberhaupt etwas? -----
    verstellt = alt.replace('"data"', '"daten_verstellt"')
    if verstellt == alt:
        probe = {"gebissen": False,
                 "grund": "Die Mutation griff nicht - `\"data\"` kam nicht vor."}
    else:
        gegen = vergleiche(verstellt, neu)
        probe = {"gebissen": bool(gegen["unterschiede"]),
                 "mutation": '"data" -> "daten_verstellt" in der alten Fassung',
                 "gefundene_unterschiede": len(gegen["unterschiede"])}

    print("=" * 74)
    print("Pfadvergleich alt/neu - shared/paths.py, OHNE gesetzten Modus")
    print("=" * 74)
    print("Bezugscommit      : %s" % BEZUGSCOMMIT)
    print("Bots              : %d" % len(BOTS))
    print("Verglichene Pfade : %d" % ergebnis["verglichen"])
    print("Unterschiede      : %d" % len(ergebnis["unterschiede"]))
    for u in ergebnis["unterschiede"]:
        print("   ⚠️ %s / %s: %r -> %r"
              % (u["bot"], u["name"], u["alt"], u["neu"]))
    print()
    print("Nur in der neuen Fassung (Zugaenge, keine Unterschiede): %d"
          % len(ergebnis["nur_in_neu"]))
    for name in ergebnis["nur_in_neu"]:
        print("   + %s" % name)
    print()
    print("Selbstprobe (beisst der Vergleich?): %s"
          % ("JA, %d Unterschiede gefunden" % probe["gefundene_unterschiede"]
             if probe["gebissen"] else "NEIN - %s" % probe.get("grund", "")))
    print()

    gut = not ergebnis["unterschiede"] and probe["gebissen"]
    print("ERGEBNIS: %s" % ("GRUEN - null Unterschiede, und der Vergleich "
                            "beisst." if gut else
                            "⚠️ ABBRECHEN UND BERICHTEN."))

    if args.json:
        ziel = args.json if os.path.isabs(args.json) \
            else os.path.join(_HIER, args.json)
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump({"bezugscommit": BEZUGSCOMMIT, "bots": list(BOTS),
                       "verglichen": ergebnis["verglichen"],
                       "unterschiede": ergebnis["unterschiede"],
                       "nur_in_neu": ergebnis["nur_in_neu"],
                       "selbstprobe": probe,
                       "werte_je_bot": ergebnis["werte"]},
                      datei, indent=2, ensure_ascii=False, sort_keys=True)
            datei.write("\n")
        print("JSON: %s" % ziel)
    return 0 if gut else 1


if __name__ == "__main__":
    sys.exit(main())
