#!/usr/bin/env python3
"""TB-140 D1 - die Tabellen aus dem Belegordner gehen per Skript ins Ergebnis, nicht abgetippt.

  --einsetzen  ersetzt im Ergebnis jede Zeile `[[TABELLE <datei>]]` durch den Inhalt der Datei
               aus docs/belege/TB-140/ (jede Marke genau einmal, in eigener Zeile; sonst nichts geschrieben)
  --pruefen    Bytevergleich: jede Tabelle steht im Ergebnis genau einmal und an Zeilengrenzen,
               keine Marke steht mehr da, und jede Kennung der Tabellen (V1-01, V2-17, ...) steht
               in fundstellen.tsv; schreibt nichts

Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 -B docs/belege/TB-140/ergebnis_tabellen.py --einsetzen
  trading-env/bin/python3 -B docs/belege/TB-140/ergebnis_tabellen.py --pruefen > docs/belege/TB-140/ergebnis_tabellen.txt 2>&1; echo "rc $?" >> docs/belege/TB-140/ergebnis_tabellen.txt
Rueckgabe: 0 eingesetzt oder alles gleich, 1 Abweichung, 2 nicht messbar (eine Datei fehlt oder
ist leer, eine Marke steht nicht genau einmal da, oder eine Ausnahme)."""
import argparse
import os
import re
import sys
import traceback

BELEGE = "docs/belege/TB-140"
ERGEBNIS = "docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md"
TABELLEN = ("z2_stellen.md", "teil2_je_bot.md", "v1_erzeuger.md", "v1_spalte.md",
            "v2_lader_schnitt.md", "v3_endlich.md")
FUNDSTELLEN = "fundstellen.tsv"
RE_KENNUNG = re.compile(rb"\bV[123]-\d{2,}\b")


def lies(pfad):
    with open(pfad, "rb") as f:
        return f.read()


def marke(name):
    return b"[[TABELLE " + name.encode("utf-8") + b"]]"


def main(argv=None):
    a = argparse.ArgumentParser()
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument("--einsetzen", action="store_true")
    g.add_argument("--pruefen", action="store_true")
    x = a.parse_args(argv)
    pfade = [os.path.join(BELEGE, n) for n in TABELLEN] + [ERGEBNIS, os.path.join(BELEGE, FUNDSTELLEN)]
    for p in pfade:
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            print("NICHT MESSBAR: %s fehlt oder ist leer" % p)
            return 2
    tab = {n: lies(os.path.join(BELEGE, n)).rstrip(b"\n") for n in TABELLEN}
    erg = lies(ERGEBNIS)
    if x.einsetzen:
        for n in TABELLEN:
            assert erg.count(marke(n)) == 1 and erg.count(b"\n" + marke(n) + b"\n") == 1, (
                "Marke fuer %s steht nicht genau einmal in eigener Zeile" % n)
        for n in TABELLEN:
            erg = erg.replace(marke(n), tab[n])
        assert b"[[TABELLE " not in erg, "eine Marke blieb stehen"
        with open(ERGEBNIS, "wb") as f:
            f.write(erg)
        print("eingesetzt: %d Tabellen in %s" % (len(TABELLEN), ERGEBNIS))
        return 0
    bekannt = {z.split(b"\t", 1)[0] for z in lies(os.path.join(BELEGE, FUNDSTELLEN)).split(b"\n") if z}
    print("# TB-140 D1 - Tabellen im Ergebnis (ergebnis_tabellen.py --pruefen)")
    alle_gut = True
    for n in TABELLEN:
        gesamt = erg.count(tab[n])
        grenzen = (b"\n" + erg).count(b"\n" + tab[n] + b"\n")
        kenn = set(RE_KENNUNG.findall(tab[n]))
        fehlt = sorted(k.decode() for k in kenn - bekannt)
        gut = gesamt == 1 and grenzen == 1 and not fehlt
        alle_gut = alle_gut and gut
        print("TABELLE\t%s\t%d Bytes\t%d Zeile(n)\tVorkommen %d\tan Zeilengrenzen %d\tKennungen %d, nicht in %s: %d %s\t%s" % (
            n, len(tab[n]), tab[n].count(b"\n") + 1, gesamt, grenzen, len(kenn), FUNDSTELLEN, len(fehlt), fehlt,
            "GLEICH" if gut else "ABWEICHUNG"))
    marken = erg.count(b"[[TABELLE ")
    print("Marken im Ergebnis: %d (Soll 0)" % marken)
    alle_gut = alle_gut and marken == 0
    print("Gesamt: %s" % ("alle Tabellen zeichengleich, je genau einmal" if alle_gut else "ABWEICHUNG"))
    print("RUECKGABE %d" % (0 if alle_gut else 1))
    return 0 if alle_gut else 1


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben); nichts geschrieben")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
