#!/usr/bin/env python3
"""TB-119 - Einsetzen von Regelwerktext per exakter Ersetzung (alt -> neu), je Stelle genau ein Treffer.

Schreibt je Stelle in ein Markdown-Protokoll: Datei, Stelle, die Zeile DAVOR und die Zeile DANACH (erste nicht-leere
Zeile vor bzw. nach dem ersetzten Bereich, am alten Stand) und jede entfernte Zeile woertlich (difflib, Zeilen mit
"- "). Mit --probe wird nichts geschrieben, nur geprueft (Treffer je Stelle == 1, alle Stellen). Standardbibliothek,
Python 3.9.
"""
import difflib
import sys


def _nachbar(zeilen, i, schritt):
    while 0 <= i < len(zeilen):
        if zeilen[i].strip():
            return zeilen[i]
        i += schritt
    return "(Dateianfang)" if schritt < 0 else "(Dateiende)"


def einsetzen(stellen, protokoll, titel, probe, lesen=None):
    """stellen: Liste von (datei, name, alt, neu). Gibt 0 zurueck, wenn alles eindeutig war.
    lesen: Funktion datei -> Inhalt (Standard: Datei im Arbeitsbaum). Mit nur_protokoll (lesen gesetzt, probe=False)
    wird NICHTS geschrieben ausser dem Protokoll; stattdessen wird geprueft, dass Basis + Ersetzungen
    bytegleich mit dem Arbeitsbaum ist."""
    fehler = 0
    inhalte = {}
    for datei, name, alt, neu in stellen:
        s = inhalte.setdefault(datei, lesen(datei) if lesen else open(datei, encoding="utf-8").read())
        n = s.count(alt)
        if n != 1:
            print("FEHLER %s / %s: %d Treffer statt 1" % (datei, name, n))
            fehler += 1
    if fehler:
        return 1
    out = ["# %s" % titel, "",
           "*Erzeugt von `%s`. Je Stelle: die ganze Zeile davor und danach (erste nicht-leere Zeile vor der ersten "
           "bzw. nach der letzten beruehrten Zeile, am Stand vor der Stelle) und jede entfernte Zeile woertlich. "
           "„entfernt: keine“ heisst: reine Einfuegung.*" % " ".join(sys.argv), ""]
    for datei, name, alt, neu in stellen:
        s = inhalte[datei]
        start = s.index(alt)
        ende = start + len(alt)
        zeilen = s.split("\n")
        z0 = s.count("\n", 0, start)                       # erste beruehrte Zeile
        z1 = s.count("\n", 0, ende - 1 if alt.endswith("\n") else ende)   # letzte beruehrte Zeile
        davor = _nachbar(zeilen, z0 - 1, -1)
        danach = _nachbar(zeilen, z1 + 1, 1)
        diff = list(difflib.ndiff(alt.split("\n"), neu.split("\n")))
        weg = [z[2:] for z in diff if z.startswith("- ")]
        dazu = [z for z in diff if z.startswith("+ ")]
        out += ["## %s — %s" % (datei, name), "",
                "- **berührt ab Z. %d** (Stand vor der Stelle) · **davor:** `%s`" % (z0 + 1, davor.replace("`", "ˋ")[:300]),
                "- **danach**: `%s`" % danach.replace("`", "ˋ")[:300],
                "- **hinzugefügt:** %d Zeilen" % len(dazu),
                "- **entfernt:** %s" % ("keine" if not weg else "%d Zeilen, woertlich:" % len(weg)), ""]
        if weg:
            out += ["```"] + weg + ["```", ""]
        inhalte[datei] = s.replace(alt, neu, 1)
    if probe:
        print("PROBE: %d Stellen, alle eindeutig, nichts geschrieben" % len(stellen))
        return 0
    if lesen:
        rc = 0
        for datei, s in inhalte.items():
            gleich = s == open(datei, encoding="utf-8").read()
            print("%s  Basis + Ersetzungen == Arbeitsbaum: %s" % (datei, "ja" if gleich else "NEIN"))
            rc |= 0 if gleich else 1
        open(protokoll, "w", encoding="utf-8").write("\n".join(out) + "\n")
        print("PROTOKOLL neu geschrieben: %s" % protokoll)
        return rc
    for datei, s in inhalte.items():
        open(datei, "w", encoding="utf-8").write(s)
    open(protokoll, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("GESCHRIEBEN: %d Stellen in %d Dateien, Protokoll %s" % (len(stellen), len(inhalte), protokoll))
    return 0
