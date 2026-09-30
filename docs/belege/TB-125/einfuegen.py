# -*- coding: utf-8 -*-
"""TB-125 Schritt A: fuehrt E1-E24 aus dem Auftragsdokument aus.

Liest je Einfuegung Datei, Anker, Art und Text aus dem Auftrag
(docs/auftraege/MAC_TB-125_regelwerk_nachtrag_29_30_09.md), nicht aus
einem Gedaechtnis. Schreibt docs/belege/TB-125/einfuegungen.txt.

Aufruf (Repo-Wurzel):  trading-env/bin/python3 docs/belege/TB-125/einfuegen.py [--probe]
--probe: rechnet alles, schreibt keine Zieldatei und kein Protokoll.
Python 3.9-tauglich.
"""
import io
import os
import re
import sys

AUFTRAG = "docs/auftraege/MAC_TB-125_regelwerk_nachtrag_29_30_09.md"
PROTOKOLL = "docs/belege/TB-125/einfuegungen.txt"

TABELLE = {1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 22, 23, 24}
ABSATZ = {2, 3, 6, 19, 20}
BLOCK = {18, 21}

# E24 steht im Auftrag unter der Ueberschrift "Datei BACKLOG.md", gehoert aber
# nach seinem Titel ("Abschnitt 0, Wenn ein Dokument mitgeht") und nach B2
# ("ARBEITSWEISE: E10, E11, E12, E13, E24") in ARBEITSWEISE.md; sein Anker steht
# dort genau einmal, in BACKLOG.md keinmal (gemessen 30.09.2026). Einzige
# Abweichung von der Dateizuordnung per Ueberschrift, im Ergebnis benannt.
DATEI_KORREKTUR = {24: "docs/projektfuehrung/ARBEITSWEISE.md"}


def lies(pfad):
    with io.open(pfad, "r", encoding="utf-8", newline="") as f:
        return f.read()


def schreib(pfad, text):
    with io.open(pfad, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def einfuegungen_lesen():
    """Liefert eine Liste von dicts: n, datei, anker (Liste), art, text (Zeilenliste)."""
    zeilen = lies(AUFTRAG).split("\n")
    ergebnis = []
    datei = None
    i = 0
    while i < len(zeilen):
        z = zeilen[i]
        m = re.match(r"^### Datei `([^`]+)`\s*$", z)
        if m:
            datei = m.group(1)
            i += 1
            continue
        m = re.match(r"^#### E(\d+) ", z)
        if not m:
            i += 1
            continue
        n = int(m.group(1))
        # Ankerzeile: erste Zeile, die mit "Anker" beginnt
        j = i + 1
        while not zeilen[j].startswith("Anker"):
            j += 1
        ankerzeile = zeilen[j]
        teil, _, artteil = ankerzeile.partition("Art: ")
        spannen = re.findall(r"`([^`]+)`", teil)
        if n == 5:
            anker = spannen[:2]
        else:
            anker = spannen[:1]
        if artteil.startswith("**nach der Zeile**"):
            art = "nach"
        elif artteil.startswith("**vor der Zeile**"):
            art = "vor"
        elif artteil.startswith("**ersetzt die Zeile**"):
            art = "ersetzt"
        elif artteil.startswith("**ersetzt alle Zeilen"):
            art = "ersetzt_bereich"
        else:
            raise SystemExit("E%d: Art nicht erkannt: %r" % (n, artteil))
        # erster Codeblock nach der Ankerzeile
        k = j + 1
        while not (zeilen[k] == "```" or zeilen[k] == "~~~"):
            if zeilen[k].startswith("#### E"):
                raise SystemExit("E%d: kein Codeblock gefunden" % n)
            k += 1
        zaun = zeilen[k]
        e = k + 1
        while zeilen[e] != zaun:
            e += 1
        text = zeilen[k + 1:e]
        ergebnis.append({"n": n, "datei": DATEI_KORREKTUR.get(n, datei), "anker": anker, "art": art, "text": text})
        i = e + 1
    return ergebnis


def zeile_mit(zeilen, anker):
    treffer = [idx for idx, z in enumerate(zeilen) if anker in z]
    if len(treffer) != 1:
        raise SystemExit("Anker nicht eindeutig auf Zeilenebene: %r (%d)" % (anker, len(treffer)))
    return treffer[0]


def ausfuehren(inhalt, e):
    zeilen = inhalt.split("\n")
    text = list(e["text"])
    n, art = e["n"], e["art"]
    if art == "ersetzt_bereich":
        a = zeile_mit(zeilen, e["anker"][0])
        b = zeile_mit(zeilen, e["anker"][1])
        if b < a:
            raise SystemExit("E%d: Endanker vor Anfangsanker" % n)
        e["ersetzt_zeilen"] = zeilen[a:b + 1]
        zeilen[a:b + 1] = text
        return "\n".join(zeilen)
    idx = zeile_mit(zeilen, e["anker"][0])
    if art == "ersetzt":
        e["ersetzt_zeilen"] = [zeilen[idx]]
        zeilen[idx:idx + 1] = text
        return "\n".join(zeilen)
    pos = idx + 1 if art == "nach" else idx
    if n in ABSATZ:
        davor = zeilen[pos - 1] if pos > 0 else ""
        danach = zeilen[pos] if pos < len(zeilen) else ""
        if davor.strip() != "":
            text = [""] + text
        if danach.strip() != "":
            text = text + [""]
    elif n in BLOCK:
        davor = zeilen[pos - 1] if pos > 0 else ""
        if davor.strip() != "":
            text = [""] + text
    elif n not in TABELLE:
        raise SystemExit("E%d: keiner Klasse zugeordnet" % n)
    e["ersetzt_zeilen"] = []
    zeilen[pos:pos] = text
    return "\n".join(zeilen)


def main():
    probe = "--probe" in sys.argv
    liste = einfuegungen_lesen()
    nummern = [e["n"] for e in liste]
    if nummern != list(range(1, 25)):
        raise SystemExit("Einfuegungen nicht E1..E24: %r" % nummern)
    inhalte = {}
    zeilen_protokoll = []
    for e in liste:
        pfad = e["datei"]
        if pfad not in inhalte:
            inhalte[pfad] = lies(pfad)
        inhalt = inhalte[pfad]
        vorher = [inhalt.count(a) for a in e["anker"]]
        if all(v == 1 for v in vorher):
            inhalt = ausfuehren(inhalt, e)
            inhalte[pfad] = inhalt
            ja = "ja"
        else:
            ja = "nein"
        erste = e["text"][0]
        nachher = inhalt.count(erste)
        e["vorher"], e["ja"], e["nachher_sofort"] = vorher, ja, nachher
    # Nachher-Zaehlung am Endstand je Datei
    for e in liste:
        e["nachher"] = inhalte[e["datei"]].count(e["text"][0])
        vorher_txt = "/".join(str(v) for v in e["vorher"])
        zeilen_protokoll.append("E%d · %s · Anker vorher %s · ausgeführt %s · Text nachher %d"
                                % (e["n"], e["datei"], vorher_txt, e["ja"], e["nachher"]))
    kopf = [
        "TB-125 Schritt A — Einfügungen (Skript docs/belege/TB-125/einfuegen.py,",
        "Texte, Anker und Art gelesen aus %s)" % AUFTRAG,
        "Format: E<n> · Datei · Anker vorher (Zahl; E5 Anfang/Ende) · ausgeführt ja/nein · Text nachher (Zahl der ersten Textzeile am Endstand)",
        "Anker vorher: gezählt unmittelbar vor der jeweiligen Einfügung, in Reihenfolge E1..E24 (E23-Anker entsteht mit E22).",
        "",
    ]
    fuss = ["", "Ersetzte Zeilen je Ersetzung (Anzahl):"]
    for e in liste:
        if e["art"] in ("ersetzt", "ersetzt_bereich"):
            fuss.append("E%d: %d Zeile(n) entfernt, %d Zeile(n) eingesetzt"
                        % (e["n"], len(e.get("ersetzt_zeilen", [])), len(e["text"])))
    ausgabe = "\n".join(kopf + zeilen_protokoll + fuss) + "\n"
    sys.stdout.write(ausgabe)
    if probe:
        sys.stdout.write("\n[--probe: nichts geschrieben]\n")
        return
    for pfad, inhalt in inhalte.items():
        schreib(pfad, inhalt)
    schreib(PROTOKOLL, ausgabe)


if __name__ == "__main__":
    main()
