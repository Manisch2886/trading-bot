#!/usr/bin/env python3
"""
Der Erzeuger des Sperrlisten-Abbilds (TB-85, Registertext 36.6)
==============================================================================
Schreibt **einmalig** das Abbild der Sperrliste: genau die Punkte des
Registerabschnitts 10 mit Pfad und Hash - nicht mehr, nicht weniger (36.6,
Bauart 33.3). Gelesen wird der Registertext mit dem Parser der Sonde
(`shared/sperrlistensonde.py::lies_abschnitt_10`), damit Erzeuger und
Pruefung (ii) dieselbe Lesart haben; die Hashes werden hier frisch gemessen.

⚠️ Die Schreibregel 36.1 gilt fuer diesen Erzeuger von seinem ersten Aufruf an:

  (2)  Er schreibt einmalig. Existiert die Zieldatei, bricht er mit
       Rueckgabewert **1** ab, nennt Pfad und Hash der vorhandenen Datei und
       schreibt nichts - **auch bei identischem Inhalt** ("die Sperre ist
       staerker, wenn sie duemmer ist"). Geoeffnet wird mit `O_EXCL`, damit
       auch ein Wettlauf zwischen Pruefung und Schreiben nicht durchrutscht.
  (3)  Es gibt **keine Voreinstellung** fuer das Ziel: `--ziel` ist Pflicht.
       36.6 verlangt je Fortschreibung der Sperrliste ein neues Abbild unter
       neuem Namen; der Name traegt deshalb das Datum (Handwerk).

Rueckgabewerte (36.5)
------------------------------------------------------------------------------
    0   geschrieben - Pfad, Groesse und SHA-256 stehen in der Ausgabe
    1   BEFUND: Ziel existiert - Pfad und Hash der vorhandenen Datei genannt
    2   NICHT MOEGLICH: Register nicht lesbar, Liste nicht in erwarteter Form,
        eine genannte Datei fehlt, Schreiben gescheitert

Nutzung
------------------------------------------------------------------------------
    python3 research/vorregistrierung/sperrliste_abbild.py \\
        --ziel research/vorregistrierung/ergebnisse/sperrliste_abbild_JJJJ-MM-TT.json
"""

import argparse
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, os.path.join(BASE_DIR, "shared"))

import sperrlistensonde as sonde  # noqa: E402

OK, BEFUND, NICHT_MOEGLICH = sonde.OK, sonde.BEFUND, sonde.NICHT_PRUEFBAR
ERZEUGER = "research/vorregistrierung/sperrliste_abbild.py"


def erzeugen(ziel, register, wurzel):
    """Bildet das Abbild und schreibt es genau einmal. Liefert (rc, text)."""
    if os.path.exists(ziel):
        try:
            h = sonde.sha256_datei(ziel)
        except OSError:
            h = "(nicht lesbar)"
        return BEFUND, ("ABBRUCH (36.1 (2)): Ziel existiert, nichts geschrieben.\n"
                        "  Pfad:   %s\n  SHA-256: %s" % (ziel, h))
    try:
        abbild = sonde.bilde_abbild(register, wurzel, erzeuger=ERZEUGER)
    except sonde.Sondenfehler as e:
        return NICHT_MOEGLICH, "ABBRUCH: Abbild nicht bildbar - %s" % e

    inhalt = json.dumps(abbild, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    try:
        ordner = os.path.dirname(os.path.abspath(ziel))
        if ordner and not os.path.isdir(ordner):
            return NICHT_MOEGLICH, "ABBRUCH: Zielordner fehlt: %s" % ordner
        fd = os.open(ziel, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        return BEFUND, ("ABBRUCH (36.1 (2)): Ziel entstand waehrend des Laufs, "
                        "nichts geschrieben.\n  Pfad:   %s\n  SHA-256: %s"
                        % (ziel, sonde.sha256_datei(ziel)))
    except OSError as e:
        return NICHT_MOEGLICH, "ABBRUCH: Ziel nicht anlegbar: %s (%s)" % (ziel, e)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(inhalt)

    n_pfade = sum(len(p["pfade"]) for p in abbild["punkte"])
    return OK, ("Abbild geschrieben.\n  Pfad:    %s\n  Groesse: %d Bytes\n"
                "  SHA-256: %s\n  Punkte:  %d (aus %s Z. %d-%d), %d Pfadnennungen, "
                "HEAD %s"
                % (ziel, os.path.getsize(ziel), sonde.sha256_datei(ziel),
                   len(abbild["punkte"]), abbild["quelle"]["register"],
                   abbild["quelle"]["zeilen"][0], abbild["quelle"]["zeilen"][1],
                   n_pfade, abbild["erzeugt"]["head"][:12]))


def main(argv=None):
    z = argparse.ArgumentParser(
        description="Schreibt einmalig das Abbild der Sperrliste (36.6). "
                    "Kein Ziel als Voreinstellung (36.1 (3)); nie ueberschreiben (36.1 (2)).")
    z.add_argument("--ziel", required=True, metavar="PFAD",
                   help="die zu schreibende Abbild-Datei (muss noch fehlen)")
    z.add_argument("--register", default=None, metavar="PFAD",
                   help="das Register (Standard: <wurzel>/%s)" % sonde.REGISTER)
    z.add_argument("--wurzel", default=BASE_DIR,
                   help="Repo-Wurzel, auf die sich die Pfade beziehen")
    a = z.parse_args(argv)
    register = a.register or os.path.join(a.wurzel, sonde.REGISTER)
    rc, text = erzeugen(a.ziel, register, a.wurzel)
    print(text, file=sys.stderr if rc else sys.stdout)
    return rc


if __name__ == "__main__":
    sys.exit(main())
