#!/usr/bin/env python3
"""
Probe zu R28 (Fable 27c, T117-4): `snapshot.VERANKERTER_DATENSTAND` gegen Register 18
==============================================================================
Der registrierte Datenstand steht in Register 18 (Quelle) und als Codekopie an
zwei Stellen: `research/vorregistrierung/auswertung.py::REGISTRIERTER_DATENSTAND`
(Probe J-r in `test_ersatzwerte.py`) und `shared/snapshot.py::VERANKERTER_DATENSTAND`.
Nach 32.5 (c) ist ein Literal nur zulaessig, wenn es eine Probe gegen den
Registertext hat. Das ist die Probe fuer die Kopie in `snapshot.py`.

Geprueft nach dem Muster von J-r (`research/vorregistrierung/test_ersatzwerte.py`):
  1. In `docs/VORREGISTRIERUNG_neuselektion.md` gibt es GENAU EINE Zeile, die mit
     "| Datenstand (`datenstand_hash`) |" beginnt.
  2. Ihr 64-stelliger Hexwert ist gleich `snapshot.VERANKERTER_DATENSTAND`.

⚠️ Diese Probe importiert nichts aus `research/vorregistrierung/`; den Registerpfad
baut sie selbst aus der Repo-Wurzel. Grund (Fable 27c, T117-4): `snapshot.py` ist
nicht im Laufbereich, und ein Import zoege es hinein.

Die Gegenprobe (Register 40.7: mit abweichendem Wert rc 1) steht in
`docs/belege/TB-124/d_gegenprobe.py`; sie setzt REGISTERDATEI bzw. die Konstante
von aussen und ruft `main()`.

Nutzung:  python3 shared/test_verankerter_datenstand.py      (rc 0 bestanden, 1 gescheitert)
"""

import os
import re
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HIER)
sys.path.insert(0, _HIER)

import snapshot  # noqa: E402

REGISTERDATEI = os.path.join(_REPO, "docs", "VORREGISTRIERUNG_neuselektion.md")
ZEILENANFANG = "| Datenstand (`datenstand_hash`) |"


def main():
    bestanden, gescheitert = 0, []

    def pruefe(name, bedingung, zusatz=""):
        nonlocal bestanden
        if bedingung:
            bestanden += 1
        else:
            gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")

    with open(REGISTERDATEI, encoding="utf-8") as f:
        zeilen = [z for z in f.read().splitlines() if z.startswith(ZEILENANFANG)]
    werte = [m.group(1) for m in (re.search(r"`([0-9a-f]{64})`", z) for z in zeilen) if m]
    anker = snapshot.VERANKERTER_DATENSTAND
    print(f"Register: {REGISTERDATEI}")
    print(f"  Zeilen mit '{ZEILENANFANG}': {len(zeilen)}, Hexwerte: {[w[:16] + '…' for w in werte]}")
    print(f"  snapshot.VERANKERTER_DATENSTAND: {anker[:16]}…")

    pruefe("R28-1: genau eine Datenstandszeile im Register", len(zeilen) == 1, str(len(zeilen)))
    pruefe("R28-2: sie traegt genau einen 64-stelligen Hexwert", len(werte) == len(zeilen) == 1, str(werte))
    pruefe("R28-3: snapshot.VERANKERTER_DATENSTAND = Register 18",
           len(werte) == 1 and anker == werte[0], f"{anker} gegen {werte}")

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
