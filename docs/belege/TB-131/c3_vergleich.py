#!/usr/bin/env python3
"""TB-131 C3: Zeichengleichheit der Einfügungen E1–E5 und md5 von ampel.py.

Zweiter, unabhängiger Leser (eigener Parser, nicht der aus einfuegen.py):
nimmt je `#### E<n>`-Abschnitt des Auftrags den ersten Codeblock ohne Zäune
und die Zieldatei aus der Zeile `Zieldatei: `…`` dieses Abschnitts, und prüft
als Bytevergleich, dass der Text in der Zieldatei genau einmal als
zusammenhängender Block an Zeilengrenzen vorkommt. Ausgabe nach c3_vergleich.txt.

Vorlage: docs/belege/TB-128/c3_vergleich.py.
Dazu: md5 von docs/werkzeuge/ampel.py gegen das Soll aus B1 (aus dem Auftrag gelesen).

Aufruf aus der Repo-Wurzel:  trading-env/bin/python3 docs/belege/TB-131/c3_vergleich.py
"""
import hashlib
import re
from pathlib import Path

AUFTRAG = Path("docs/auftraege/MAC_TB-131_regelwerk_nachtrag_ampel.md")
AUSGABE = Path("docs/belege/TB-131/c3_vergleich.txt")

roh = AUFTRAG.read_bytes()
abschnitte = re.split(rb"\n(?=#### E\d+ |## )", roh)  # nicht an "### " im E5-Codeblock teilen
zeilen = []
alle_gut = True
for a in abschnitte:
    m = re.match(rb"#### (E\d+) ", a)
    if not m:
        continue
    nr = m.group(1).decode()
    datei = re.search(rb"^Zieldatei: `([^`]+)`$", a, re.M).group(1).decode()
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

anzahl = len(zeilen)
zeilen.append(f"Anzahl Einfügungen: {anzahl} · Gesamt: {'alle zeichengleich, je genau einmal' if alle_gut and anzahl == 5 else 'ABWEICHUNG'}")
soll_md5 = re.search(rb"Soll nachher: md5 `([0-9a-f]{32})`", roh).group(1).decode()
ist_md5 = hashlib.md5(Path("docs/werkzeuge/ampel.py").read_bytes()).hexdigest()
zeilen.append(f"ampel.py · md5 {ist_md5} · Soll {soll_md5} · {'GLEICH' if ist_md5 == soll_md5 else 'ABWEICHUNG'}")
AUSGABE.write_text("# TB-131 C3 — Zeichengleichheit (c3_vergleich.py)\n" + "\n".join(zeilen) + "\n", encoding="utf-8")
print("\n".join(zeilen))
