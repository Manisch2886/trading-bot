#!/usr/bin/env python3
"""
TB-118 C1 - BACKLOG.md in vier Dateien teilen (Fable 27b B2, Teil D C1). Einmaliges Werkzeug, Beleg.

Liest BACKLOG.md am Commit --basis (Standard HEAD) und schreibt nach --ziel (Standard docs/projektfuehrung):
  BACKLOG.md                    O  offen (Struktur der Abschnitte bleibt: jede Ueberschrift steht hier)
  BACKLOG_ENTSCHEIDUNGEN.md     E  Festlegungen, Regeln, Betreiberentscheide mit Datum (Name nach Betreiberentscheidung
                                   27.09.2026 statt "ENTSCHEIDUNGEN.md", c1_entscheidung_dateiname.txt)
  BACKLOG_ERLEDIGT_2026-09.md   D  Erledigtes und Abschnitt 8 "Gestrichen" vollstaendig
  BACKLOG_SICHTSCHUTZ.md        S  jede Zeile mit einer Groesse oder Erwartung nach Register 27.1 (nur Repo)

Die Zuordnung steht unten als Tabelle ZUORDNUNG (Zeilennummer der alten Datei -> Klasse), von Hand gelesen, Zeile
fuer Zeile; die Gruende je Zeile stehen in c1_zuordnung.txt. Strukturzeilen (Ueberschriften, Leerzeilen, "---",
Tabellenkopf und Trennzeile) haben keine Klasse: Ueberschriften stehen in BACKLOG.md alle und in den anderen drei
Dateien, sobald darunter eine Zeile dieser Datei steht; ein Tabellenkopf steht in jeder Datei, die eine Zeile der
Tabelle bekommt. In den drei neuen Dateien steht jede Ueberschrift eine Ebene tiefer (## -> ###), damit keine
Block-Ueberschrift "## 2x" in zwei Zieldateien des Nachtragswaechters steht. Jede Inhaltszeile der alten Datei steht in genau einer der vier (Nachweis c2_zeilenmenge.py).
Abbruch mit 2, wenn eine Inhaltszeile keine Klasse hat oder eine Strukturzeile eine.
"""
import argparse
import os
import re
import subprocess
import sys

QUELLE = "docs/projektfuehrung/BACKLOG.md"
DATEIEN = {"O": "BACKLOG.md", "E": "BACKLOG_ENTSCHEIDUNGEN.md", "D": "BACKLOG_ERLEDIGT_2026-09.md",
           "S": "BACKLOG_SICHTSCHUTZ.md"}


def r(a, b=None):
    return list(range(a, (b if b is not None else a) + 1))


# Klasse je Zeile der alten Datei (Stand 1e11457/f8056ef, 603 Zeilen). Gruende: c1_zuordnung.txt
Z = {}
for k, zeilen in {
    "O": r(3, 24) + r(30, 32) + [44, 45, 47] + r(57, 58)
         + [73, 75, 77, 86, 91, 92, 96, 97, 98, 99, 100, 112, 117, 136, 148, 149, 150, 155, 158, 161, 166, 171,
            176, 177, 178, 189, 207, 208, 213, 215, 216, 231, 232, 233, 274, 275, 319, 331, 332, 333]
         + r(337, 343) + r(347, 352) + [368, 378, 383, 384, 392, 404, 405, 407, 411, 414] + r(416, 421)
         + r(423, 428) + r(436, 439) + r(442, 453) + [456, 457, 458] + r(460, 465) + [468, 506, 507, 511, 514, 515]
         + [529, 530, 532] + r(534, 540) + [554, 555],
    "E": r(62, 65) + r(67, 70) + [78, 80, 90, 126] + r(138, 142) + [144, 145, 147, 151, 152, 153, 154, 157, 159,
         160, 162, 163, 164, 168, 183, 184, 185, 186, 187, 198, 200, 201, 202, 203, 221, 223, 270, 271, 278, 314,
         315, 316, 320, 321, 358] + r(362, 367) + r(369, 377) + [380, 381, 382, 466, 467, 469, 470]
         + r(472, 504) + [517, 521],
    "D": [40, 41, 42, 43, 46] + r(49, 51) + [66, 71, 72, 74, 76, 79, 81, 82, 83, 84, 85, 87, 88, 89, 93, 94, 95]
         + r(101, 111) + r(113, 116) + r(118, 125) + r(127, 135) + [137, 146, 156, 165, 169] + r(172, 175)
         + r(179, 182) + [188] + r(191, 197) + [199] + r(204, 206) + r(209, 212) + [214] + r(217, 220)
         + r(225, 230) + r(239, 242) + r(246, 261) + [265, 269, 272, 273, 276] + r(280, 286) + r(288, 295)
         + r(297, 300) + r(302, 308) + [317, 318, 323, 324, 330, 379] + r(393, 403) + [406, 408, 409, 410, 412,
         413, 415, 422, 454, 455, 459, 471, 505, 508, 509, 512, 513, 533, 546, 557, 558] + r(564, 597) + [603],
    "S": [143, 167, 170, 190, 222, 224, 440, 441, 510, 531],
}.items():
    for n in zeilen:
        if n in Z:
            raise SystemExit("Zeile %d doppelt zugeordnet (%s und %s)" % (n, Z[n], k))
        Z[n] = k

KOPF = {
    "O": ["", "> ⭐ **Geteilt TB-118; Erledigtes in `BACKLOG_ERLEDIGT_2026-09.md`, Festlegungen in `BACKLOG_ENTSCHEIDUNGEN.md`, "
               "Zeilen nach 27.1 in `BACKLOG_SICHTSCHUTZ.md` (nur Repo, bis zum Tag).**"],
    "E": ["# Entscheidungen — Festlegungen, Regeln und Betreiberentscheide aus dem Backlog", "",
          "*Geteilt TB-118 (27.09.2026, Fable 27b B2) aus `BACKLOG.md`; jede Zeile zeichengleich, Nachweis "
          "`docs/belege/TB-118/c2_zeilenmenge.txt`. Offenes steht in `BACKLOG.md`, Erledigtes in "
          "`BACKLOG_ERLEDIGT_2026-09.md`. Gehört in die Projektablage.*"],
    "D": ["# Backlog — Erledigtes (September 2026)", "",
          "*Geteilt TB-118 (27.09.2026, Fable 27b B2) aus `BACKLOG.md`; jede Zeile zeichengleich, Nachweis "
          "`docs/belege/TB-118/c2_zeilenmenge.txt`. Enthält Abschnitt 8 „Gestrichen“ vollständig — er wird nie "
          "gelöscht (DOKUMENTATIONSSTANDARD 9). Nur Repo, nicht in die Projektablage.*"],
    "S": ["# Backlog — Zeilen nach Register 27.1 (Sichtschutz)", "",
          "*Geteilt TB-118 (27.09.2026, Fable 27b B2, G5) aus `BACKLOG.md`; jede Zeile zeichengleich, Nachweis "
          "`docs/belege/TB-118/c2_zeilenmenge.txt`. ⛔ **Nur Repo, nie in die Projektablage, bis zum signierten "
          "Tag** — jede Zeile hier enthält eine Grösse oder Erwartung nach Register 27.1 (Kennzahl eines "
          "Parametersatzes, Aussage über den Ausgang). Offene Punkte darunter bleiben offen.*"],
}


def ist_struktur(zeilen, i):
    """Ueberschrift, Leerzeile, ---, Tabellenkopf (von einer Trennzeile gefolgt) oder Trennzeile."""
    z = zeilen[i]
    if z.strip() == "" or z.strip() == "---" or re.match(r"^#{1,6} ", z):
        return True
    if re.match(r"^\|(\s*:?-{3,}:?\s*\|)+\s*$", z):
        return True
    return z.startswith("|") and i + 1 < len(zeilen) and re.match(r"^\|(\s*:?-{3,}:?\s*\|)+\s*$", zeilen[i + 1])


def teilen(zeilen):
    """(Ausgabezeilen je Klasse, Fehler). Eine Leerzeile steht vor und nach jeder Ueberschrift und dort, wo in der
    alten Datei zwischen zwei Zeilen derselben Ausgabe etwas lag - ausser zwischen Zeilen derselben Tabelle."""
    aus = {k: [] for k in DATEIEN}
    zuletzt = {k: (None, None, None) for k in DATEIEN}     # (Zeilennummer, Art, Tabelle) der letzten Ausgabe
    uebs = {k: set() for k in DATEIEN}                     # schon geschriebene Ueberschriften (Zeilennummern)
    fehler, stapel, tabelle = [], [], None                 # stapel: offene Ueberschriften [(Ebene, Text, Nr)]

    def schreibe(k, text, n, art, tab=None):
        ln, la, lt = zuletzt[k]
        if aus[k]:
            in_tabelle = art == "t" and la == "t" and lt is tab
            if not in_tabelle and (art in ("h", "tk") or la == "h" or ln is None or n != ln + 1):
                aus[k].append("")
        aus[k].append(text)
        zuletzt[k] = (n, art, tab)

    for i, z in enumerate(zeilen):
        n = i + 1
        if ist_struktur(zeilen, i):
            if n in Z and z.strip() != "":      # Leerzeilen innerhalb eines Bereichs r(a, b) sind zulaessig
                fehler.append("Strukturzeile %d hat Klasse %s" % (n, Z[n]))
            m = re.match(r"^(#{1,6}) ", z)
            if m:
                ebene = len(m.group(1))
                stapel = [(e, t, nr) for e, t, nr in stapel if e < ebene] + [(ebene, z, n)]
                schreibe("O", z, n, "h")
                uebs["O"].add(n)
                if n == 1:
                    aus["O"].extend(KOPF["O"])
                tabelle = None
            elif z.startswith("|") and not re.match(r"^\|(\s*:?-{3,}:?\s*\|)+\s*$", z):
                tabelle = (z, zeilen[i + 1], n)
            elif z.strip() == "---":
                tabelle = None
            continue
        k = Z.get(n)
        if k is None:
            fehler.append("Inhaltszeile %d ohne Klasse: %s" % (n, z[:80]))
            continue
        for e, t, nr in stapel:
            if nr not in uebs[k]:
                schreibe(k, t if k == "O" else "#" + t, nr, "h")
                uebs[k].add(nr)
        if z.startswith("|") and tabelle:
            if zuletzt[k][2] is not tabelle:
                schreibe(k, tabelle[0], tabelle[2], "tk")
                aus[k].append(tabelle[1])
                zuletzt[k] = (tabelle[2] + 1, "t", tabelle)
            schreibe(k, z, n, "t", tabelle)
        else:
            schreibe(k, z, n, "p")
    return aus, fehler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--basis", default="HEAD")
    ap.add_argument("--ziel", default="docs/projektfuehrung")
    a = ap.parse_args()
    alt = subprocess.run(["git", "show", "%s:%s" % (a.basis, QUELLE)], stdout=subprocess.PIPE, check=True).stdout
    zeilen = alt.decode("utf-8").split("\n")
    if zeilen and zeilen[-1] == "":
        zeilen = zeilen[:-1]
    aus, fehler = teilen(zeilen)
    if fehler:
        print("\n".join(fehler))
        print("ABBRUCH: %d Fehler, nichts geschrieben" % len(fehler))
        return 2
    os.makedirs(a.ziel, exist_ok=True)
    for k in "OEDS":
        inhalt = aus[k] if k == "O" else KOPF[k] + [""] + aus[k]
        while inhalt and inhalt[-1] == "":
            inhalt.pop()
        pfad = os.path.join(a.ziel, DATEIEN[k])
        with open(pfad, "w", encoding="utf-8") as f:
            f.write("\n".join(inhalt) + "\n")
        print("%s  %-30s %4d Zeilen, %4d Inhaltszeilen aus der alten Datei"
              % (k, DATEIEN[k], len(inhalt), sum(1 for n, v in Z.items() if v == k and zeilen[n - 1].strip())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
