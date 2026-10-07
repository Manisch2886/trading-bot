#!/usr/bin/env python3
"""TB-140 Teil 2 - Suche in Text mit benanntem Bereich. Durchsucht nur von git verfolgte Dateien,
liest sie als Text, importiert nichts aus dem Repo und schreibt nur nach stdout.
Je Treffer eine Zeile TREFFER: Muster, Datei, Zeilennummer, Text (hoechstens 300 Zeichen). Aus
Dateien namens live_params.py und mit --nur-zaehlen wird kein Text gedruckt (Sichtschutz 27.1).
Aufruf aus der Repo-Wurzel. Rueckgabe: 0 gesucht (auch bei 0 Treffern), 2 nicht messbar
(keine Datei im Bereich, git liefert keine Liste, oder eine Ausnahme)."""
import argparse
import re
import subprocess
import sys
import traceback

NIE = ("data/", "snapshots/", "trading-env/", "logs/", ".git/")   # nie durchsucht, auch wenn --pfad sie nennt
NIE_ORDNER = "ergebnisse"                                           # Sichtschutz, Register 27.1
OHNE_TEXT = ("live_params.py",)                                     # Kommentare dort tragen Kennzahlen
MAX_ZEICHEN = 300


def dateien(pfade, endungen, ohne):
    aus = subprocess.run(["git", "--no-optional-locks", "ls-files", "-z"],
                         stdout=subprocess.PIPE, check=True).stdout.decode("utf-8")
    liste = []
    for p in aus.split("\0"):
        if not p or not p.endswith(tuple(endungen)):
            continue
        if p.startswith(NIE) or NIE_ORDNER in p.split("/")[:-1]:
            continue
        if any(p == q or p.startswith(q.rstrip("/") + "/") for q in ohne):
            continue
        if pfade and not any(p == q or p.startswith(q.rstrip("/") + "/") for q in pfade):
            continue
        liste.append(p)
    return sorted(liste)


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--name", required=True, help="Kennung der Suche, zum Beispiel V1-A")
    a.add_argument("--pfad", action="append", default=[], help="Datei oder Ordner; ohne Angabe: alle verfolgten Dateien")
    a.add_argument("--endung", action="append", default=[], help="Vorgabe .py")
    a.add_argument("--ohne", action="append", default=[], help="Ordner, der im Bereich fehlt")
    a.add_argument("--muster", action="append", required=True)
    a.add_argument("--regex", action="store_true", help="Muster sind regulaere Ausdruecke, sonst feste Zeichenketten")
    a.add_argument("--ohne-gross-klein", action="store_true")
    a.add_argument("--nur-zaehlen", action="store_true", help="je Treffer nur Datei und Zeile, kein Text")
    x = a.parse_args(argv)
    endungen = x.endung or [".py"]
    liste = dateien(x.pfad, endungen, x.ohne)
    print("# TB-140 Suche %s" % x.name)
    print("BEREICH\tverfolgte Dateien, pfad %s, endung %s, ohne %s; nie %s und Ordner %s/" % (
        x.pfad or "alle", endungen, x.ohne or "nichts", list(NIE), NIE_ORDNER))
    print("DATEIEN\t%d" % len(liste))
    if not liste:
        print("NICHT MESSBAR: keine Datei im Bereich")
        return 2
    flags = re.IGNORECASE if x.ohne_gross_klein else 0
    muster = [(m, re.compile(m if x.regex else re.escape(m), flags)) for m in x.muster]
    treffer = {m: 0 for m, _ in muster}
    in_dateien = {m: set() for m, _ in muster}
    for p in liste:
        with open(p, encoding="utf-8", errors="replace") as f:
            for nr, zeile in enumerate(f, 1):
                text = zeile.strip()
                for m, r in muster:
                    for t in r.finditer(text):
                        treffer[m] += 1
                        in_dateien[m].add(p)
                        if x.nur_zaehlen or p.split("/")[-1] in OHNE_TEXT:
                            print("TREFFER\t%s\t%s\t%d\t(Text nicht gedruckt)" % (m, p, nr))
                            continue
                        von = max(0, min(t.start() - 100, len(text) - MAX_ZEICHEN))
                        print("TREFFER\t%s\t%s\t%d\t%s" % (m, p, nr, text[von:von + MAX_ZEICHEN].replace("\t", " ")))
    for m, _ in muster:
        print("MUSTER\t%s\tTreffer %d\tDateien %d" % (m, treffer[m], len(in_dateien[m])))
    print("RUECKGABE 0")
    return 0


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
