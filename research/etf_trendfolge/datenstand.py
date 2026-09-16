#!/usr/bin/env python3
"""
S-B1 - Die Wache ueber `data/` (TB-39)
==============================================================================
Der Datenstand-Hash der Vorregistrierung ist der SHA-256 ueber die Dateien in
`data/`. **Eine einzige zusaetzliche Datei dort aendert ihn** und entwertet
den registrierten Zustand, bevor der Selektionslauf stattgefunden hat.

Dieses Modul ist die Wache dagegen, und sie arbeitet auf ZWEI Ebenen:

  1. **Der Hash.** `--pruefen` rechnet ihn nach und vergleicht ihn mit dem
     Soll aus dem Register. Abweichung heisst Rueckgabewert 1.
  2. **Der Ort.** `--pruefen` stellt ausserdem fest, dass der Zielordner der
     ETF-Kursdateien NICHT unter `data/` liegt. Das ist die Wache, die
     wirkt, BEVOR der Schaden entsteht - der Hash meldet ihn erst danach.

WARUM DER HASH NICHT HIER GERECHNET WIRD
------------------------------------------------------------------------------
Er kommt aus `research/vorregistrierung/herkunft.py::datenstand` - derselben
Funktion, die ihn fuer die Vorregistrierung erzeugt hat. Eine zweite
Berechnung waere genau die Doppelfuehrung, gegen die dieses Projekt seine
Regeln geschrieben hat: sie koennte dieselbe Zahl liefern und trotzdem eine
andere Frage beantworten (andere Reihenfolge, andere Dateiauswahl).

`herkunft.py` achtet auf `TB30A_BASE_DIR`. Der Selbsttest nutzt das, um die
Wache an einem NACHGEBAUTEN `data/` zu beobachten - ohne das echte je
anzufassen.
"""

import argparse
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)

import register as reg                                      # noqa: E402

# Geladen ueber `register.lade_fremdes_modul`: der fremde Ordner kommt NICHT
# auf `sys.path`, sonst verdeckte sein `beispieldaten.py` das hiesige.
herkunft = reg.lade_fremdes_modul(
    "herkunft", os.path.join(reg.VORREGISTRIERUNG_DIR, "herkunft.py"))


def stand(daten_dir=None):
    """{'datenstand': ..., 'dateien': ...} - aus `herkunft.py`, nicht neu."""
    return herkunft.datenstand(daten_dir or reg.KURSDATEN_DIR_VERBOTEN)


def stimmt_mit_soll(daten_dir=None):
    """(bool, Ist-Stand) - deckt sich `data/` mit dem registrierten Stand?"""
    ist = stand(daten_dir)
    passt = (ist["datenstand"] == reg.DATENSTAND_SOLL
             and ist["dateien"] == reg.DATENSTAND_DATEIEN_SOLL)
    return passt, ist


def ziel_liegt_ausserhalb(ziel_dir=None, data_dir=None):
    """(bool, Grund) - liegt der ETF-Datenordner ausserhalb von `data/`?

    Geprueft wird der AUFGELOESTE Pfad, nicht die Zeichenkette: ein
    symbolischer Link nach `data/` saehe sonst harmlos aus.
    """
    ziel = os.path.realpath(ziel_dir or reg.DATEN_DIR)
    daten = os.path.realpath(data_dir or reg.KURSDATEN_DIR_VERBOTEN)
    if ziel == daten or ziel.startswith(daten + os.sep):
        return False, (f"Der Zielordner {ziel} liegt unter {daten}. Jede "
                       f"Datei, die dort entsteht, aendert den "
                       f"Datenstand-Hash der Vorregistrierung.")
    return True, None


def pruefe(daten_dir=None, ziel_dir=None):
    """Beide Ebenen auf einmal. Gibt einen Befundblock zurueck."""
    passt, ist = stimmt_mit_soll(daten_dir)
    draussen, grund = ziel_liegt_ausserhalb(ziel_dir, daten_dir)
    return {
        "datenstand_ist": ist["datenstand"],
        "dateien_ist": ist["dateien"],
        "datenstand_soll": reg.DATENSTAND_SOLL,
        "dateien_soll": reg.DATENSTAND_DATEIEN_SOLL,
        "datenstand_unveraendert": passt,
        "ziel_ausserhalb_data": draussen,
        "ziel": os.path.realpath(ziel_dir or reg.DATEN_DIR),
        "grund": grund,
        "in_ordnung": passt and draussen,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--data", default=None,
                   help="ein anderer data/-Ordner (fuer Selbsttests)")
    p.add_argument("--ziel", default=None,
                   help="ein anderer Zielordner (fuer Selbsttests)")
    p.add_argument("--json", metavar="PFAD", default=None)
    args = p.parse_args(argv)

    b = pruefe(args.data, args.ziel)
    print("S-B1 - Wache ueber data/\n")
    print(f"  Ist    {b['datenstand_ist']}  ({b['dateien_ist']} Dateien)")
    print(f"  Soll   {b['datenstand_soll']}  ({b['dateien_soll']} Dateien)")
    print("  " + ("unveraendert" if b["datenstand_unveraendert"]
                   else "ABWEICHUNG"))
    print(f"\n  Zielordner der ETF-Kursdateien: {b['ziel']}")
    if b["ziel_ausserhalb_data"]:
        print("  liegt ausserhalb von data/ - richtig so.")
    else:
        print(f"  FEHLER: {b['grund']}")

    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(b, fh, indent=2, ensure_ascii=False)
        print(f"\n  geschrieben: {args.json}")

    return 0 if b["in_ordnung"] else 1


if __name__ == "__main__":
    sys.exit(main())
