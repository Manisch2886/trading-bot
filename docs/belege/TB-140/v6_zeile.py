#!/usr/bin/env python3
"""TB-140 V6 - liest eine Tagesreihe von stdin und druckt zu einem Datum nur,
in welchen Spalten der Wert fehlt. Kein Kurs wird ausgegeben oder in eine Zahl gewandelt.
Rueckgabe: 0 genau eine Zeile mit dem Datum, und close fehlt dort; 1 close ist vorhanden, oder die
Zeile gibt es nicht genau einmal; 2 nicht messbar (leere Eingabe, Kopfzeile ohne open_time an
erster Stelle oder ohne close, oder eine Ausnahme)."""
import sys
import traceback

# L5 des Vorgaengers: leer oder ein Text, den pandas.read_csv als Fehlwert liest
FEHLWERT = {"#N/A", "#N/A N/A", "#NA", "-1.#IND", "-1.#QNAN", "-NaN", "-nan", "1.#IND", "1.#QNAN",
            "<NA>", "N/A", "NA", "NULL", "NaN", "None", "n/a", "nan", "null"}


def main(argv):
    datum = argv[1] if len(argv) > 1 else "2026-09-01"
    zeilen = sys.stdin.read().splitlines()
    if not zeilen:
        print("NICHT MESSBAR: leere Eingabe")
        return 2
    kopf = zeilen[0].split(",")
    if kopf[0] != "open_time" or "close" not in kopf:
        print("NICHT MESSBAR: Kopfzeile ohne open_time an erster Stelle oder ohne close (%d Felder, Inhalt nicht gedruckt)" % len(kopf))
        return 2
    treffer = [z.split(",") for z in zeilen[1:] if z.split(",")[0] == datum]
    print("Kopf %s; Datenzeilen %d; letzte Datumszelle %s" % (",".join(kopf), len(zeilen) - 1, zeilen[-1].split(",")[0]))
    print("Zeilen mit open_time %s: %d" % (datum, len(treffer)))
    if len(treffer) != 1:
        print("die Zeile gibt es nicht genau einmal")
        return 1
    felder = treffer[0]
    leer = [k for k, v in zip(kopf, felder) if v == ""]
    text = [k for k, v in zip(kopf, felder) if v in FEHLWERT]
    ohne = kopf[len(felder):]
    print("Zeile %s: %d Spalten; leer: %s; Fehlwert-Text: %s; Spalte fehlt: %s" % (datum, len(felder), leer, text, ohne))
    fehlt = "close" in leer or "close" in text or "close" in ohne
    print("close fehlt: %s" % ("ja" if fehlt else "nein"))
    return 0 if fehlt else 1


if __name__ == "__main__":
    try:
        RC = main(sys.argv)
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
