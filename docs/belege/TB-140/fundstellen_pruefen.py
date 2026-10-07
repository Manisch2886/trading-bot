#!/usr/bin/env python3
"""TB-140 Teil 2 - Pruefung der Fundstellenliste (Form der Belege, Nr. 2).

Liest jede Zeile von fundstellen.tsv (fuenf Spalten, Tabulator: kennung, datei, zeile, art,
wortlaut; geteilt hoechstens viermal, ein Tabulator im Wortlaut bleibt Teil des Wortlauts),
oeffnet die Datei als Text und vergleicht den Wortlaut mit der genannten Zeile:
  art `zeile`  die ganze Zeile ohne fuehrende und schliessende Leerzeichen ist gleich dem Wortlaut
  art `teil`   nur fuer Registerzeilen (*.md): der Wortlaut (hoechstens 300 Zeichen) steht in der Zeile
Importiert nichts aus dem Repo, schreibt nur nach stdout.

Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 -B docs/belege/TB-140/fundstellen_pruefen.py [--liste PFAD]
Rueckgabe: 0 alle gleich, 1 mindestens ein UNGLEICH, 2 nicht messbar (Liste fehlt oder ist leer,
eine Zeile traegt keine fuenf Spalten, eine Datei ist nicht lesbar, oder eine Ausnahme)."""
import argparse
import re
import sys
import traceback

LISTE = "docs/belege/TB-140/fundstellen.tsv"
RE_KENNUNG = re.compile(r"^V[123]-\d{2,}$")
MAX_TEIL = 300


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--liste", default=LISTE)
    x = a.parse_args(argv)
    try:
        with open(x.liste, encoding="utf-8") as f:
            zeilen = [z.rstrip("\n") for z in f]
    except OSError as e:
        print("NICHT MESSBAR: Liste nicht lesbar: %s" % e)
        return 2
    zeilen = [z for z in zeilen if z]
    if not zeilen:
        print("NICHT MESSBAR: Liste leer")
        return 2
    print("# TB-140 Fundstellenpruefung, Liste %s" % x.liste)
    cache, ungleich, kennungen = {}, 0, set()
    for nr, z in enumerate(zeilen, 1):
        teile = z.split("\t", 4)
        if len(teile) != 5:
            print("NICHT MESSBAR: Zeile %d traegt %d statt 5 Spalten" % (nr, len(teile)))
            return 2
        kennung, datei, zeile, art, wortlaut = teile
        grund = None
        if not RE_KENNUNG.match(kennung):
            grund = "Kennung nicht in der Form V<n>-<nn>"
        elif kennung in kennungen:
            grund = "Kennung doppelt"
        kennungen.add(kennung)
        if datei not in cache:
            try:
                with open(datei, encoding="utf-8") as f:
                    cache[datei] = f.read().split("\n")
            except OSError as e:
                print("NICHT MESSBAR: %s nicht lesbar (%s), Zeile %d der Liste" % (datei, type(e).__name__, nr))
                return 2
        text = cache[datei]
        if grund is None:
            try:
                n = int(zeile)
            except ValueError:
                n = 0
            if not 1 <= n <= len(text):
                grund = "Zeilennummer ausserhalb der Datei"
            elif art == "zeile":
                if text[n - 1].strip() != wortlaut:
                    grund = "Wortlaut ungleich der Zeile"
            elif art == "teil":
                if not datei.endswith(".md"):
                    grund = "art teil nur fuer Registerzeilen"
                elif len(wortlaut) > MAX_TEIL:
                    grund = "Ausschnitt laenger als %d Zeichen" % MAX_TEIL
                elif not wortlaut or wortlaut not in text[n - 1]:
                    grund = "Ausschnitt steht nicht in der Zeile"
            else:
                grund = "art weder zeile noch teil"
        if grund:
            ungleich += 1
            print("UNGLEICH\t%s\t%s\t%s\t%s" % (kennung, datei, zeile, grund))
    print("Fundstellen %d, ungleich %d" % (len(zeilen), ungleich))
    print("RUECKGABE %d" % (1 if ungleich else 0))
    return 1 if ungleich else 0


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
