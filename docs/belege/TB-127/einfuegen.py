#!/usr/bin/env python3
"""TB-127 Schritt A: Einfügungen E1–E9 aus dem Auftragsdokument ausführen.

Liest je Einfügung Zieldatei (aus der Überschrift `### Datei `…``), Anker,
Art und Text (Codeblock ohne Zäune) aus dem Auftrag — nicht aus dem Gedächtnis.
Verfahren wie im Auftrag: Anker vorher zählen (str.count, Soll 1), ausführen,
erste Zeile des Texts nachher zählen (Soll 1). Ergebnis nach einfuegungen.txt.

Aufruf aus der Repo-Wurzel:  trading-env/bin/python3 docs/belege/TB-127/einfuegen.py
"""
import re
import sys
from pathlib import Path

AUFTRAG = Path("docs/auftraege/MAC_TB-127_regelwerk_tokensparen_registerkopie.md")
AUSGABE = Path("docs/belege/TB-127/einfuegungen.txt")
BLOECKE = {"E1", "E2", "E9"}  # Absätze/Blöcke: genau eine Leerzeile davor und danach

RE_DATEI = re.compile(r"^### Datei `([^`]+)`\s*$")
RE_KOPF = re.compile(r"^#### (E\d+) — ")
RE_ANKER = re.compile(r"^Anker: `([^`]+)`( \(Zeilenanfang\))? · Art: \*\*(.+?)\*\*\s*$")


def einfuegungen_lesen(text):
    """Liste von dicts (nr, datei, anker, zeilenanfang, art, text) in Auftragsreihenfolge."""
    zeilen = text.split("\n")
    datei = None
    aktuell = None
    ergebnis = []
    i = 0
    while i < len(zeilen):
        z = zeilen[i]
        m = RE_DATEI.match(z)
        if m:
            datei = m.group(1)
        m = RE_KOPF.match(z)
        if m:
            aktuell = {"nr": m.group(1), "datei": datei}
        m = RE_ANKER.match(z)
        if m and aktuell is not None:
            aktuell["anker"] = m.group(1)
            aktuell["zeilenanfang"] = bool(m.group(2))
            aktuell["art"] = m.group(3)
            # nächster Codeblock
            j = i + 1
            while zeilen[j].strip() != "```":
                j += 1
            k = j + 1
            while zeilen[k] != "```":
                k += 1
            aktuell["text"] = zeilen[j + 1:k]
            ergebnis.append(aktuell)
            aktuell = None
            i = k
        i += 1
    return ergebnis


def ausfuehren(e):
    pfad = Path(e["datei"])
    inhalt = pfad.read_text(encoding="utf-8")
    vorher = inhalt.count(e["anker"])
    zeilen = inhalt.split("\n")
    treffer = [n for n, z in enumerate(zeilen) if e["anker"] in z]
    if e["zeilenanfang"]:
        treffer = [n for n in treffer if zeilen[n].startswith(e["anker"])]
    if vorher != 1 or len(treffer) != 1:
        return vorher, False, inhalt.count(e["text"][0])
    n = treffer[0]
    block = list(e["text"])
    if e["nr"] in BLOECKE:
        if e["art"] == "nach der Zeile":
            vor = [] if zeilen[n] == "" else [""]
            nach = [] if n + 1 < len(zeilen) and zeilen[n + 1] == "" else [""]
            zeilen[n + 1:n + 1] = vor + block + nach
        elif e["art"] == "vor der Zeile":
            vor = [] if n > 0 and zeilen[n - 1] == "" else [""]
            nach = [] if zeilen[n] == "" else [""]
            zeilen[n:n] = vor + block + nach
        else:
            raise SystemExit(f"{e['nr']}: Art {e['art']!r} für Block nicht vorgesehen")
    else:
        if e["art"] == "nach der Zeile":
            zeilen[n + 1:n + 1] = block
        elif e["art"] == "vor der Zeile":
            zeilen[n:n] = block
        elif e["art"] == "ersetzt die Zeile":
            zeilen[n:n + 1] = block
        else:
            raise SystemExit(f"{e['nr']}: unbekannte Art {e['art']!r}")
    neu = "\n".join(zeilen)
    pfad.write_text(neu, encoding="utf-8")
    return vorher, True, neu.count(e["text"][0])


def main():
    liste = einfuegungen_lesen(AUFTRAG.read_text(encoding="utf-8"))
    nummern = [e["nr"] for e in liste]
    if nummern != [f"E{i}" for i in range(1, 10)]:
        sys.exit(f"Auftrag nicht wie erwartet gelesen: {nummern}")
    zeilen_aus = []
    for e in liste:
        vorher, ja, nachher = ausfuehren(e)
        zeile = (f"{e['nr']} · {e['datei']} · Anker vorher {vorher} · ausgeführt "
                 f"{'ja' if ja else 'nein'} · Text nachher {nachher}")
        print(zeile)
        zeilen_aus.append(zeile)
    AUSGABE.write_text(
        "# TB-127 Schritt A — Einfügungen (erzeugt von einfuegen.py)\n"
        "# E<n> · Datei · Anker vorher · ausgeführt ja/nein · Text nachher\n"
        + "\n".join(zeilen_aus) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
