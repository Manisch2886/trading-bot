#!/usr/bin/env python3
"""TB-129 Schritt B: Einfuegung E1 (BACKLOG-Block) aus dem Auftrag ausfuehren.

Bauart TB-128 einfuegen.py. Liest Zieldatei (Zeile `Zieldatei: `...``), Anker (erste Codespanne der
Zeile `Anker: `), Art (fett) und Text (erster ```-Codeblock ohne Zaeune) aus dem Abschnitt `#### E1 — `
des Auftrags am Commit S0 (git show) - nicht aus dem Gedaechtnis.
Verfahren wie im Auftrag: Anker vorher zaehlen (str.count, Soll 1; sonst nicht ausfuehren, vermerken),
einfuegen vor der Zeile mit genau einer Leerzeile davor und danach (eine vorhandene wird nicht verdoppelt),
erste Textzeile nachher zaehlen (Soll 1). Ergebnis nach b_einfuegung.txt.
Aufruf aus der Repo-Wurzel:  trading-env/bin/python3 docs/belege/TB-129/b_einfuegen.py <S0> [--probe]
"""
import re
import subprocess
import sys
from pathlib import Path

S0 = sys.argv[1]
PROBE = "--probe" in sys.argv[2:]
AUSGABE = Path("docs/belege/TB-129/b_einfuegung.txt")
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-129_register_fable_01a.md" % S0],
                     capture_output=True, text=True, check=True).stdout.split("\n")
i = next(k for k, s in enumerate(auf) if s.startswith("#### E1 — "))
datei = anker = art = None
k = i + 1
while True:
    s = auf[k]
    m = re.match(r"^Zieldatei: `([^`]+)`\s*$", s)
    if m:
        datei = m.group(1)
    m = re.match(r"^Anker: `([^`]+)` · Art: \*\*(.+?)\*\*", s)
    if m:
        anker, art = m.group(1), m.group(2)
    if s == "```":
        break
    k += 1
e = next(j for j in range(k + 1, len(auf)) if auf[j] == "```")
text = auf[k + 1:e]
assert datei and anker and art == "vor der Zeile", (datei, anker, art)

pfad = Path(datei)
inhalt = pfad.read_text(encoding="utf-8")
vorher = inhalt.count(anker)
zeilen = inhalt.split("\n")
treffer = [n for n, z in enumerate(zeilen) if anker in z]
erste_vorher = inhalt.count(text[0])
ausgefuehrt = False
if vorher == 1 and len(treffer) == 1 and not PROBE:
    n = treffer[0]
    vor = [] if n > 0 and zeilen[n - 1] == "" else [""]
    nach = [] if zeilen[n] == "" else [""]
    zeilen[n:n] = vor + text + nach
    pfad.write_text("\n".join(zeilen), encoding="utf-8")
    ausgefuehrt = True
nachher = pfad.read_text(encoding="utf-8").count(text[0])
zeile = (f"E1 · {datei} · Anker {anker!r} · Art {art} · Anker vorher {vorher} · Ankerzeile vorher "
         f"{treffer[0] + 1 if treffer else '-'} · Textzeilen {len(text)} · erste Textzeile vorher {erste_vorher} · "
         f"ausgeführt {'ja' if ausgefuehrt else 'nein'} · erste Textzeile nachher {nachher}")
print(zeile)
if not PROBE:
    AUSGABE.write_text("# TB-129 Schritt B — Einfügung (b_einfuegen.py, Auftrag am Commit %s)\n%s\n" % (S0, zeile),
                       encoding="utf-8")
