#!/usr/bin/env python3
"""TB-131 Schritt A: Einfügungen E1–E5 aus dem Auftragsdokument ausführen.

Liest je Einfügung Zieldatei (aus der Zeile `Zieldatei: `…``), Anker, Art und
Text (Codeblock ohne Zäune) aus dem Auftrag — nicht aus dem Gedächtnis.
Anker in doppelten Backticks (`` `x` ``) werden als Markdown-Codespanne
gelesen: Inhalt ohne die je eine Leerstelle innen.
Verfahren wie im Auftrag: Anker vorher zählen (str.count, Soll 1), ausführen,
erste Zeile des Texts nachher zählen (Soll 1). Ergebnis nach einfuegungen.txt.

Vorlage: docs/belege/TB-128/einfuegen.py.

Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 docs/belege/TB-131/einfuegen.py --probe   (nur lesen)
  trading-env/bin/python3 docs/belege/TB-131/einfuegen.py
"""
import re
import sys
from pathlib import Path

AUFTRAG = Path("docs/auftraege/MAC_TB-131_regelwerk_nachtrag_ampel.md")
AUSGABE = Path("docs/belege/TB-131/einfuegungen.txt")
BLOECKE = {"E5"}  # Absätze/Blöcke: genau eine Leerzeile davor und danach

RE_KOPF = re.compile(r"^#### (E\d+) — ")
RE_DATEI = re.compile(r"^Zieldatei: `([^`]+)`\s*$")
RE_ANKER = re.compile(r"^Anker: (?:`` (.+?) ``|`([^`]+)`) · Art: \*\*(.+?)\*\*\s*$")


def einfuegungen_lesen(text):
    """Liste von dicts (nr, datei, anker, art, text) in Auftragsreihenfolge."""
    zeilen = text.split("\n")
    aktuell = None
    ergebnis = []
    i = 0
    while i < len(zeilen):
        z = zeilen[i]
        m = RE_KOPF.match(z)
        if m:
            aktuell = {"nr": m.group(1), "datei": None}
        m = RE_DATEI.match(z)
        if m and aktuell is not None:
            aktuell["datei"] = m.group(1)
        m = RE_ANKER.match(z)
        if m and aktuell is not None:
            aktuell["anker"] = m.group(1) if m.group(1) is not None else m.group(2)
            aktuell["art"] = m.group(3)
            j = i + 1
            while zeilen[j].strip() != "```":
                j += 1
            k = j + 1
            while zeilen[k] != "```":
                k += 1
            aktuell["text"] = zeilen[j + 1:k]
            if aktuell["datei"] is None:
                sys.exit(f"{aktuell['nr']}: keine Zieldatei-Zeile vor dem Anker")
            ergebnis.append(aktuell)
            aktuell = None
            i = k
        i += 1
    return ergebnis


def ausfuehren(e, probe):
    pfad = Path(e["datei"])
    inhalt = pfad.read_text(encoding="utf-8")
    vorher = inhalt.count(e["anker"])
    zeilen = inhalt.split("\n")
    treffer = [n for n, z in enumerate(zeilen) if e["anker"] in z]
    if vorher != 1 or len(treffer) != 1:
        return vorher, False, inhalt.count(e["text"][0]), None
    n = treffer[0]
    if probe:
        return vorher, False, inhalt.count(e["text"][0]), n + 1
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
        else:
            raise SystemExit(f"{e['nr']}: unbekannte Art {e['art']!r}")
    neu = "\n".join(zeilen)
    pfad.write_text(neu, encoding="utf-8")
    return vorher, True, neu.count(e["text"][0]), n + 1


def main():
    probe = "--probe" in sys.argv[1:]
    liste = einfuegungen_lesen(AUFTRAG.read_text(encoding="utf-8"))
    nummern = [e["nr"] for e in liste]
    if nummern != [f"E{i}" for i in range(1, 6)]:
        sys.exit(f"Auftrag nicht wie erwartet gelesen: {nummern}")
    zeilen_aus = []
    for e in liste:
        vorher, ja, nachher, ankerzeile = ausfuehren(e, probe)
        if probe:
            print(f"{e['nr']} · {e['datei']} · Anker {e['anker']!r} · Art {e['art']} · "
                  f"vorher {vorher} · Ankerzeile {ankerzeile} · Textzeilen {len(e['text'])} · "
                  f"erste Textzeile schon {nachher}")
            continue
        zeile = (f"{e['nr']} · {e['datei']} · Anker vorher {vorher} · ausgeführt "
                 f"{'ja' if ja else 'nein'} · Text nachher {nachher}")
        print(zeile)
        zeilen_aus.append(zeile)
    if probe:
        return
    AUSGABE.write_text(
        "# TB-131 Schritt A — Einfügungen (erzeugt von einfuegen.py)\n"
        "# E<n> · Datei · Anker vorher · ausgeführt ja/nein · Text nachher\n"
        + "\n".join(zeilen_aus) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
