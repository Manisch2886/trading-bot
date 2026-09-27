#!/usr/bin/env python3
"""
dialog_index.py - FABLE_DIALOG_INDEX.md: je Fable-Antwort eine Zeile (TB-118, Fable 27b G4/B6, Teil D B1-B3)
============================================================================================================
Der Index ist die Verdichtung des Dialogs neben dem Register (27b G4): je `FABLE_ANTWORT_*.md` eine Zeile.
Das Skript erzeugt die Felder, die sich messen lassen, und uebernimmt die Handfelder aus dem vorhandenen Index:

  gemessen    Antwort (Datum/Buchstabe), Stichwort (aus dem Dateinamen), Repo-Pfad,
              Register: "registriert", wenn der Dateiname ohne .md im Register vorkommt (grep -F), sonst "–",
              Fundstelle: die Abschnittsnummern der Treffer,
              Anfrage: die FABLE_ANFRAGE, die die Antwort in ihren ersten 12 Zeilen nennt (Bezug); nennt sie
              keine, die Anfrage mit demselben Datum und Buchstaben ("gleicher Buchstabe"), sonst "–"
  von Hand    Frage (ein Satz), Entscheidung (ein Satz) - aus dem Block **Kurz:** der Antwort, lesend;
              offen (ja/nein) - ja, wenn die Antwort Fragen an den Betreiber oder Messbitten stellt, die in keiner
              spaeteren Anfrage als beantwortet erscheinen
  abgeleitet  Status: "offen" wenn offen = ja, sonst "registriert" oder "ohne Registertext"

Aufrufe (aus der Repo-Wurzel):
    python3 docs/werkzeuge/dialog_index.py                          Index neu schreiben, Handfelder behalten
    python3 docs/werkzeuge/dialog_index.py --handfelder <json>      dazu Handfelder aus JSON setzen
                                                                     ({"<Buchstabe>": {"frage", "entscheidung", "offen"}})
    python3 docs/werkzeuge/dialog_index.py --pruefen                nur pruefen (rc 0/1): Zeilenzahl = Zahl der
                                                                     Antworten, in jeder Zeile die sechs Felder aus
                                                                     27b G4 gefuellt (Antwort, Frage, Entscheidung,
                                                                     Fundstelle, Status, Pfad), offen in {ja, nein}
Eine neue Antwort bekommt beim naechsten Lauf ihre Zeile mit "?" in den Handfeldern; --pruefen gibt dann 1,
bis sie gefuellt sind. Handfelder duerfen kein "|" enthalten. Reine Standardbibliothek, Python 3.9.
Rueckgabewert: 0 in Ordnung, 1 Pruefung gescheitert, 2 Eingabe unbrauchbar.
"""
import argparse
import glob
import json
import os
import re
import sys

ORDNER = "docs/projektfuehrung"
INDEX = os.path.join(ORDNER, "FABLE_DIALOG_INDEX.md")
REGISTER = "docs/VORREGISTRIERUNG_neuselektion.md"
NAME = re.compile(r"^FABLE_(ANTWORT|ANFRAGE)_2026-(\d\d)-(\d\d)([a-z]?)_(.+)\.md$")
SPALTEN = ["Antwort", "Stichwort", "Frage", "Entscheidung", "Status", "Fundstelle", "offen", "Anfrage", "Pfad"]
PFLICHT = ["Antwort", "Frage", "Entscheidung", "Fundstelle", "Status", "Pfad"]
KOPF = """# FABLE_DIALOG_INDEX — je Fable-Antwort eine Zeile

**Erzeugt von** `docs/werkzeuge/dialog_index.py` (TB-118, Fable 27b G4). Der Volltext jeder Antwort liegt im Repo unter
dem genannten Pfad; der Registertext steht im Register. Diese Zeile ist die dritte Stelle, **nicht** eine dritte Fassung:
Frage und Entscheidung stehen hier nur, um die Antwort zu finden.

**Spalten:** *Frage*, *Entscheidung* und *offen* sind von Hand gelesen (Block **Kurz:** der Antwort). *Fundstelle* nennt
die Registerabschnitte, in denen der Dateiname vorkommt (`grep -F`, gemessen); „–“ heisst: der Dateiname steht nicht im
Register. Eine Antwort, die dort nur als „Fable 24b“ zitiert ist, zählt nicht mit. *Status*: „offen“, wenn *offen* = ja;
sonst „registriert“ oder „ohne Registertext“. *Anfrage*: der Bezug, den die Antwort selbst nennt, sonst die Anfrage mit
gleichem Buchstaben. Pfade relativ zu `docs/projektfuehrung/`.

"""


def zerlege(pfad):
    m = NAME.match(os.path.basename(pfad))
    return None if not m else {"art": m.group(1), "monat": m.group(2), "tag": m.group(3), "bst": m.group(4),
                               "stichwort": m.group(5), "name": os.path.basename(pfad)}


def abschnitte_mit(register_zeilen, wort):
    treffer, abschnitt = [], None
    for z in register_zeilen:
        m = re.match(r"^## (\d+)\.", z)
        if m:
            abschnitt = int(m.group(1))
        if wort in z and abschnitt is not None and abschnitt not in treffer:
            treffer.append(abschnitt)
    return treffer


def lies_index():
    """Handfelder aus dem vorhandenen Index: {Antwort: {frage, entscheidung, offen}}."""
    felder = {}
    if not os.path.exists(INDEX):
        return felder
    with open(INDEX, encoding="utf-8") as f:
        for z in f:
            if not z.startswith("| ") or z.startswith("| Antwort") or z.startswith("|---"):
                continue
            teile = [t.strip() for t in z.strip().strip("|").split("|")]
            if len(teile) != len(SPALTEN):
                continue
            w = dict(zip(SPALTEN, teile))
            felder[w["Antwort"]] = {"frage": w["Frage"], "entscheidung": w["Entscheidung"], "offen": w["offen"]}
    return felder


def zeilen(handfelder):
    antworten = sorted(filter(None, map(zerlege, glob.glob(os.path.join(ORDNER, "FABLE_ANTWORT_*.md")))),
                       key=lambda d: (d["monat"], d["tag"], d["bst"]))
    anfragen = list(filter(None, map(zerlege, glob.glob(os.path.join(ORDNER, "FABLE_ANFRAGE_*.md")))))
    with open(REGISTER, encoding="utf-8") as f:
        reg = f.read().split("\n")
    vorhanden = lies_index()
    aus = []
    for a in antworten:
        schluessel = "%s%s" % (a["tag"], a["bst"])
        with open(os.path.join(ORDNER, a["name"]), encoding="utf-8") as f:
            kopf = "".join(f.readlines()[:12])
        bezug = sorted(set(re.findall(r"FABLE_ANFRAGE_2026-\d\d-(\d\d[a-z]?)_", kopf)))
        gleich = [q for q in anfragen if (q["monat"], q["tag"], q["bst"]) == (a["monat"], a["tag"], a["bst"])]
        if bezug:
            anfrage = ", ".join(bezug) + " (Bezug)"
            if gleich and "%s%s" % (gleich[0]["tag"], gleich[0]["bst"]) not in bezug:
                anfrage += "; gleicher Buchstabe: %s%s" % (gleich[0]["tag"], gleich[0]["bst"])
        elif gleich:
            anfrage = "%s%s (gleicher Buchstabe)" % (gleich[0]["tag"], gleich[0]["bst"])
        else:
            anfrage = "–"
        fund = abschnitte_mit(reg, a["name"][:-3])
        h = dict(vorhanden.get(schluessel, {}))
        h.update(handfelder.get(schluessel, {}))
        offen = h.get("offen", "?")
        status = "offen" if offen == "ja" else ("registriert" if fund else "ohne Registertext")
        w = {"Antwort": schluessel, "Stichwort": a["stichwort"].replace("_", " "),
             "Frage": h.get("frage", "?"), "Entscheidung": h.get("entscheidung", "?"), "Status": status,
             "Fundstelle": ", ".join(map(str, fund)) if fund else "–", "offen": offen, "Anfrage": anfrage,
             "Pfad": "`%s`" % a["name"]}
        for k in ("Frage", "Entscheidung"):
            if "|" in w[k]:
                print("ABBRUCH: '|' im Handfeld %s von %s" % (k, schluessel))
                sys.exit(2)
        aus.append(w)
    return aus


def schreiben(z):
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(KOPF)
        f.write("| " + " | ".join(SPALTEN) + " |\n|" + "---|" * len(SPALTEN) + "\n")
        for w in z:
            f.write("| " + " | ".join(w[s] for s in SPALTEN) + " |\n")
        f.write("\n%d Antworten. Pflege: nach jeder angenommenen Antwort das Skript laufen lassen, die neue Zeile von "
                "Hand füllen, `--pruefen`.\n" % len(z))


def pruefen():
    n_dateien = len(glob.glob(os.path.join(ORDNER, "FABLE_ANTWORT_*.md")))
    felder, fehler, n = {}, 0, 0
    with open(INDEX, encoding="utf-8") as f:
        for z in f:
            if not z.startswith("| ") or z.startswith("| Antwort") or z.startswith("|---"):
                continue
            teile = [t.strip() for t in z.strip().strip("|").split("|")]
            n += 1
            if len(teile) != len(SPALTEN):
                print("Zeile %d: %d statt %d Felder" % (n, len(teile), len(SPALTEN)))
                fehler += 1
                continue
            w = dict(zip(SPALTEN, teile))
            leer = [s for s in PFLICHT if w[s] in ("", "?")]
            if leer or w["offen"] not in ("ja", "nein"):
                print("Zeile %s: nicht gefuellt: %s%s" % (w["Antwort"], ", ".join(leer),
                                                           " offen=%r" % w["offen"] if w["offen"] not in ("ja", "nein") else ""))
                fehler += 1
            felder[w["Antwort"]] = w
    print("Zeilen im Index: %d, FABLE_ANTWORT_*.md: %d - %s" % (n, n_dateien, "gleich" if n == n_dateien else "UNGLEICH"))
    print("Zeilen mit allen sechs Feldern (27b G4) und offen in {ja, nein}: %d von %d" % (n - fehler, n))
    stat = {}
    for w in felder.values():
        stat[w["Status"]] = stat.get(w["Status"], 0) + 1
    print("Status: " + ", ".join("%s %d" % kv for kv in sorted(stat.items())))
    return 0 if fehler == 0 and n == n_dateien else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--pruefen", action="store_true")
    ap.add_argument("--handfelder")
    a = ap.parse_args()
    if a.pruefen:
        return pruefen()
    hand = {}
    if a.handfelder:
        with open(a.handfelder, encoding="utf-8") as f:
            hand = {k: v for k, v in json.load(f).items() if not k.startswith("_")}
    z = zeilen(hand)
    schreiben(z)
    print("geschrieben: %s, %d Zeilen" % (INDEX, len(z)))
    return pruefen()


if __name__ == "__main__":
    sys.exit(main())
