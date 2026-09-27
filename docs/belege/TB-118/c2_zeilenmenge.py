#!/usr/bin/env python3
"""
TB-118 C2 - Nachweis der Backlog-Teilung als Zeilenmenge (Fable 27b B2, Teil D C2).

Die Inhaltszeilen der alten BACKLOG.md (am Commit --basis, Standard 8a3f6f6 = Stand vor der Teilung) muessen als MULTIMENGE in der Vereinigung
der vier neuen Dateien genau einmal vorkommen. Ausgenommen sind nur Strukturzeilen: Leerzeilen, Ueberschriften
(#...), "---", Tabellenkopf (die Zeile vor einer Trennzeile) und Trennzeilen |---|. Gezaehlt wird mit Counter, ohne
Vereinheitlichung (kein set, kein sort -u - K4a).

Ausgabe: je Richtung die Abweichungen - (a) alte Zeile fehlt, (b) alte Zeile zu oft, (c) neue Inhaltszeile, die in
der alten Datei nicht vorkam (erlaubt sind nur die Kopfzeilen der Teilung; sie werden einzeln genannt).
Rueckgabewert 0: (a) und (b) leer und (c) nur die erwarteten Kopfzeilen; sonst 1.
Aufruf: python3 c2_zeilenmenge.py [--basis <commit>] [--ordner docs/projektfuehrung]
"""
import argparse
import collections
import os
import re
import subprocess
import sys

DATEIEN = ["BACKLOG.md", "BACKLOG_ENTSCHEIDUNGEN.md", "BACKLOG_ERLEDIGT_2026-09.md", "BACKLOG_SICHTSCHUTZ.md"]
TRENN = re.compile(r"^\|(\s*:?-{3,}:?\s*\|)+\s*$")


def inhalt(zeilen):
    aus = []
    for i, z in enumerate(zeilen):
        if z.strip() in ("", "---") or re.match(r"^#{1,6} ", z) or TRENN.match(z):
            continue
        if z.startswith("|") and i + 1 < len(zeilen) and TRENN.match(zeilen[i + 1]):
            continue
        aus.append(z)
    return aus


def lies(text):
    z = text.split("\n")
    return z[:-1] if z and z[-1] == "" else z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--basis", default="8a3f6f6")  # Stand vor der Teilung
    ap.add_argument("--ordner", default="docs/projektfuehrung")
    a = ap.parse_args()
    alt_text = subprocess.run(["git", "show", "%s:docs/projektfuehrung/BACKLOG.md" % a.basis],
                              stdout=subprocess.PIPE, check=True).stdout.decode("utf-8")
    alt = collections.Counter(inhalt(lies(alt_text)))
    neu, je_datei = collections.Counter(), {}
    for d in DATEIEN:
        with open(os.path.join(a.ordner, d), encoding="utf-8") as f:
            z = inhalt(lies(f.read()))
        je_datei[d] = len(z)
        neu.update(z)
    print("# TB-118 C2 Zeilenmenge: alte BACKLOG.md am %s gegen die vier Dateien in %s" % (a.basis, a.ordner))
    print("Inhaltszeilen alt: %d (%d verschiedene)" % (sum(alt.values()), len(alt)))
    for d in DATEIEN:
        print("Inhaltszeilen %-30s %d" % (d, je_datei[d]))
    print("Inhaltszeilen neu gesamt: %d" % sum(neu.values()))
    fehlt = {z: n - neu[z] for z, n in alt.items() if neu[z] < n}
    zuviel = {z: neu[z] - n for z, n in alt.items() if neu[z] > n}
    zusatz = {z: n for z, n in neu.items() if z not in alt}
    print("(a) alte Zeile fehlt: %d" % sum(fehlt.values()))
    for z, n in fehlt.items():
        print("    %dx %s" % (n, z[:120]))
    print("(b) alte Zeile zu oft: %d" % sum(zuviel.values()))
    for z, n in zuviel.items():
        print("    %dx %s" % (n, z[:120]))
    print("(c) neue Inhaltszeilen, nicht aus der alten Datei: %d" % sum(zusatz.values()))
    for z, n in zusatz.items():
        print("    %dx %s" % (n, z[:160]))
    erwartet_neu = all(z.startswith(("> ⭐ **Geteilt TB-118", "*Geteilt TB-118")) for z in zusatz)
    rc = 0 if not fehlt and not zuviel and erwartet_neu else 1
    print("Ergebnis: %s, rc %d" % ("jede alte Inhaltszeile genau einmal; neu nur die Kopfzeilen der Teilung"
                                   if rc == 0 else "ABWEICHUNG", rc))
    return rc


if __name__ == "__main__":
    sys.exit(main())
