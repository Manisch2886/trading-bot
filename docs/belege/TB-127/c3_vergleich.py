#!/usr/bin/env python3
"""TB-127 C3: Zeichengleichheit der Einfügungen E1–E9.

Zweiter, unabhängiger Leser (eigener Parser, nicht der aus einfuegen.py):
nimmt je `#### E<n>`-Abschnitt des Auftrags den ersten Codeblock ohne Zäune
und die Zieldatei aus der letzten `### Datei`-Überschrift davor, und prüft
als Bytevergleich, dass der Text in der Zieldatei genau einmal als
zusammenhängender Block an Zeilengrenzen vorkommt. Ausgabe nach c3_vergleich.txt.

Aufruf aus der Repo-Wurzel:  trading-env/bin/python3 docs/belege/TB-127/c3_vergleich.py
"""
import re
from pathlib import Path

AUFTRAG = Path("docs/auftraege/MAC_TB-127_regelwerk_tokensparen_registerkopie.md")
AUSGABE = Path("docs/belege/TB-127/c3_vergleich.txt")

roh = AUFTRAG.read_bytes()
abschnitte = re.split(rb"\n(?=### Datei `|#### E\d+ )", roh)
datei = None
zeilen = []
alle_gut = True
for a in abschnitte:
    m = re.match(rb"### Datei `([^`]+)`", a)
    if m:
        datei = m.group(1).decode()
        continue
    m = re.match(rb"#### (E\d+) ", a)
    if not m:
        continue
    nr = m.group(1).decode()
    cb = re.search(rb"\n```\n(.*?)\n```\n", a, re.S)
    text = cb.group(1)
    ziel = Path(datei).read_bytes()
    gesamt = ziel.count(text)
    an_grenzen = ziel.count(b"\n" + text + b"\n")
    gut = gesamt == 1 and an_grenzen == 1
    nzeilen = text.count(b"\n") + 1
    alle_gut &= gut
    zeilen.append(f"{nr} · {datei} · {len(text)} Bytes · {nzeilen} Zeile(n) · "
                  f"Vorkommen {gesamt} · an Zeilengrenzen {an_grenzen} · {'GLEICH' if gut else 'ABWEICHUNG'}")

zeilen.append(f"Anzahl Einfügungen: {len(zeilen)} · Gesamt: {'alle zeichengleich, je genau einmal' if alle_gut and len(zeilen) == 9 else 'ABWEICHUNG'}")
AUSGABE.write_text("# TB-127 C3 — Zeichengleichheit (c3_vergleich.py)\n" + "\n".join(zeilen) + "\n", encoding="utf-8")
print("\n".join(zeilen))
