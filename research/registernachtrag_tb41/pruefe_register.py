#!/usr/bin/env python3
"""
TB-41 - Pruefwerkzeug fuer den Registernachtrag
==============================================================================
Der Registernachtrag traegt Zahlen ein, die woanders gemessen wurden. Genau da
geht so etwas kaputt: jemand tippt 137 als 173, und niemand merkt es, weil die
Quelle in einem anderen Dokument steht.

Dieses Werkzeug tippt nichts ab. Es liest die Zahlen aus dem Register, liest
sie ein zweites Mal aus ihrer Quelle und vergleicht sie maschinell.

  symbolzahl            Tabelle 16.1.1 gegen den TB-40-Trockenlauf
  faltenevidenz         Tabelle 16.1.2 gegen den TB-40-Trockenlauf
  min_history           Tabelle 16.7 (b) gegen die neun Bot-Dateien
  umstellungstag        Registertext 7 gegen umstellungstag_entscheidungskerze.json
  universumsdatei       der korrigierte Rechenweg 16.1.3 gegen config/ und shared/
  datenstand            SHA-256 ueber data/ gegen den registrierten Wert
  daten_unberuehrt      git: keine Datei unter data/ veraendert
  null_entfernte_zeilen git: null entfernte Zeilen im Register
  ersetzt_gekennzeichnet jede ersetzte Fassung steht noch da UND traegt den Verweis

ZWEI BELEGQUELLEN FUER DIESELBE ZAHL
------------------------------------------------------------------------------
Die Messung selbst ist TB-40. Wo deren Werkzeug laufen kann (Bot-Abhaengigkeiten
vorhanden), wird es aufgerufen und sein JSON gelesen - das ist die harte Form.
Wo es das nicht kann (Cloud: kein pandas, Binance gesperrt), wird das
committete Ergebnisdokument von TB-40 geparst. Welche Quelle benutzt wurde,
steht im Bericht; geraten wird nichts.

WOGEGEN VERGLICHEN WIRD - UND WARUM DAS IM BERICHT STEHT
------------------------------------------------------------------------------
Die beiden git-Pruefungen brauchen eine Vergleichsbasis. Bis TB-43 war das
fest `origin/main`, mit zwei Folgen: nach einem Merge war der Diff leer und
`null_entfernte_zeilen` meldete Erfolg, ohne irgendetwas geprueft zu haben
(dreimal aufgetreten - TB-36, TB-40, TB-41).

Beides ist jetzt getrennt behandelt:

* Die Basis ist standardmaessig `git merge-base HEAD origin/main`, nicht
  `origin/main` selbst - damit schleppt der Diff keine fremden Commits mit
  herein, wenn `main` weitergelaufen ist.
* Ein LEERER Vergleich ist ein BEFUND, kein Erfolg. `merge-base` hilft dagegen
  naemlich gerade nicht: ist der Zweig schon gemergt, ist die Basis der eigene
  Commit und der Diff bleibt leer.
* Welche Basis benutzt wurde und woher sie kommt, steht als `Quelle basis:`
  in der Ausgabe.

DIESES WERKZEUG SCHREIBT NICHTS ausser der optionalen --json-Datei. Es fasst
weder data/ noch strategies/ noch research/universum_trockenlauf/ an.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))

REGISTER = os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_neuselektion.md")
BELEG_TB40 = os.path.join(BASE_DIR, "docs", "ERGEBNIS_TB-40_universum_trockenlauf.md")
TROCKENLAUF = os.path.join(BASE_DIR, "research", "universum_trockenlauf",
                           "universum_trockenlauf.py")
UMSTELLUNGSTAG = os.path.join(BASE_DIR, "docs", "umstellungstag_entscheidungskerze.json")

BOTS = [
    "elliott_wave", "t3_supertrend", "rsi2_crypto", "turtle_soup_crypto",
    "volatility_breakout_crypto", "elliott_wave_stocks", "rsi2_mean_reversion",
    "turtle_soup_stocks", "volatility_breakout",
]
KRYPTO_TAGESBOTS = ["rsi2_crypto", "turtle_soup_crypto", "volatility_breakout_crypto"]
AKTIEN_BOTS = ["elliott_wave_stocks", "rsi2_mean_reversion", "turtle_soup_stocks",
               "volatility_breakout"]

# Registrierter Datenstand - steht so im Register (Abschnitt 15.0/16.0).
DATENSTAND_PRAEFIX = "d9449faf51bffaaa"
DATENSTAND_DATEIEN = 223

# Der Zweig, gegen den verglichen wird, wenn --basis nichts sagt. Nicht
# direkt als Basis benutzt - siehe bestimme_basis().
STANDARD_ZWEIG = "origin/main"

# Der Umstellungstag der Entscheidungskerze, Registertext 7.
UMSTELLUNGSTAG_ERWARTET = "2026-09-16T04:42:24Z"

# Die Passagen, die der Nachtrag ersetzt: (Suchtext, der stehenbleiben MUSS,
# Verweis, der danach stehen MUSS).
ERSETZT = [
    ("Registertext 2d (Embargo, 15.4)",
     "> **(d)** Die Bestätigungsperiode beginnt am Go-Live-Tag plus Embargo",
     "16.6"),
    ("Tatsachennotiz Symbolzahl je Falte (15.5)",
     "| `volatility_breakout` | 140 / 142 / 145 / 147 / 148 / 148 / 149 | 150 | 150 |",
     "16.1.1"),
    ("Tatsachennotiz Symbole ohne Faltenevidenz (15.5)",
     "* **aktien (1 von 150):** `SNDK` (ab 13.02.2025).",
     "16.1.2"),
    ("Klammer hinter der Universumsgroesse (15.5)",
     "| 24 (26 Zeilen abzüglich `XAUTUSDT`, `PAXGUSDT`) |",
     "16.1.3"),
    ("Registertext 5 (Datenstand, 15.7)",
     "> Ein Aktien-Abruf zwischen Registereintrag und Selektionslauf ändert den Hash",
     "16.3"),
]


# ---------------------------------------------------------------------------
# 1. Kleinkram
# ---------------------------------------------------------------------------
def _lies(pfad):
    with open(pfad, encoding="utf-8") as f:
        return f.read()


def _zelle(text):
    """Markdown aus einer Tabellenzelle entfernen."""
    text = re.sub(r"\*\(.*?\)\*", "", text)      # kursive Randbemerkung
    text = text.replace("**", "").replace("`", "").replace("*", "")
    return text.strip()


def _zahl(text):
    """'17 520' und '1 825' sind Zahlen, keine Paare."""
    roh = re.sub(r"[\s  .]", "", _zelle(text))
    return int(roh)


def _tabelle_nach(text, ueberschrift, spalten):
    """Die erste Markdown-Tabelle nach einer Ueberschrift, Zeilen als Listen.
    Blockzitat-Praefixe ('> ') werden abgestreift."""
    i = text.index(ueberschrift)
    zeilen = text[i:].splitlines()
    gefunden = []
    in_tabelle = False
    for z in zeilen[1:]:
        z = z.strip()
        if z.startswith(">"):
            z = z[1:].strip()
        if z.startswith("|"):
            felder = [f for f in z.strip("|").split("|")]
            if len(felder) != spalten:
                if in_tabelle:
                    break
                continue
            if set(_zelle("".join(felder))) <= set("-: "):
                in_tabelle = True
                continue
            if not in_tabelle:
                continue
            gefunden.append(felder)
        elif in_tabelle and z == "":
            break
    return gefunden


def _reihe(text):
    """'6 / 9 / 10' -> [6, 9, 10]"""
    return [int(_zelle(t)) for t in _zelle(text).split("/")]


def _symbole(text):
    return sorted(s for s in (_zelle(t) for t in _zelle(text).split(",")) if s)


# ---------------------------------------------------------------------------
# 2. Das Register lesen
# ---------------------------------------------------------------------------
def register_symbolzahl(register_text):
    zeilen = _tabelle_nach(
        register_text,
        "> **Die Symbolzahl je Falte** (Tatsachennotiz zu 3b, **ersetzt die Fassung aus",
        4)
    raus = {}
    for bot, falten, best, univ in zeilen:
        raus[_zelle(bot)] = {"falten": _reihe(falten),
                             "bestaetigung": _zahl(best),
                             "universum": _zahl(univ)}
    return raus


def register_faltenevidenz(register_text):
    zeilen = _tabelle_nach(
        register_text,
        "> **Symbole ohne Faltenevidenz** (Tatsachennotiz zu 3b, **ersetzt die Fassung",
        3)
    raus = {}
    for bot, anzahl, syms in zeilen:
        raus[_zelle(bot)] = {"anzahl": _zahl(anzahl), "symbole": _symbole(syms)}
    return raus


def register_min_history(register_text):
    zeilen = _tabelle_nach(
        register_text,
        "> **(b)** `MIN_HISTORY_*` ist **je Bot mit seinem Namen und seiner Einheit**",
        4)
    raus = {}
    for bot, name, wert, misst in zeilen:
        raus[_zelle(bot)] = {"name": _zelle(name), "wert": _zahl(wert),
                             "misst": _zelle(misst)}
    return raus


# ---------------------------------------------------------------------------
# 3. Der Beleg: TB-40
# ---------------------------------------------------------------------------
def beleg_aus_trockenlauf(json_pfad, python=None):
    """Ruft research/universum_trockenlauf/universum_trockenlauf.py auf und
    liest dessen JSON. Der Aufruf ist rein lesend; das Werkzeug selbst wird
    nicht veraendert."""
    befehl = [python or sys.executable, TROCKENLAUF, "--nur-universum",
              "--json", json_pfad]
    lauf = subprocess.run(befehl, cwd=BASE_DIR, capture_output=True, text=True)
    if lauf.returncode not in (0, 1) or not os.path.exists(json_pfad):
        raise RuntimeError("Trockenlauf nicht lauffaehig: %s"
                           % (lauf.stderr.strip().splitlines() or ["?"])[-1])
    with open(json_pfad, encoding="utf-8") as f:
        bericht = json.load(f)
    zahlen, evidenz = {}, {}
    for bot, e in bericht["bots"].items():
        sel = [f for f in e["falten"] if not f["bestaetigung"]]
        best = [f for f in e["falten"] if f["bestaetigung"]][0]
        zahlen[bot] = {"falten": [len(f["gemessen_H"]) for f in sel],
                       "bestaetigung": len(best["gemessen_H"]),
                       "universum": e["universum"]}
        evidenz[bot] = sorted(e["ohne_faltenevidenz_H"])
    return zahlen, evidenz


def beleg_aus_dokument(pfad):
    """Faellt das Werkzeug aus (Cloud), gilt das committete Ergebnisdokument
    von TB-40 als Beleg. Geparst, nicht abgetippt."""
    text = _lies(pfad)

    # a) Die Zahlenreihen: der Codeblock 'Lesart H ... zum Kopieren'.
    marke = "Die korrigierte Tabelle unter **Lesart H**"
    block = text.index(marke)
    anfang = text.index("```", block) + 3
    ende = text.index("```", anfang)
    zahlen = {}
    for z in text[anfang:ende].splitlines():
        z = z.strip()
        if not z.startswith("|"):
            continue
        felder = z.strip("|").split("|")
        if len(felder) != 4 or set(_zelle("".join(felder))) <= set("-: "):
            continue
        bot = _zelle(felder[0])
        if bot not in BOTS:
            continue
        zahlen[bot] = {"falten": _reihe(felder[1]),
                       "bestaetigung": _zahl(felder[2]),
                       "universum": _zahl(felder[3])}

    # b) Die Listen: die Tabelle 'Symbole ohne Faltenevidenz (Lesart H)'.
    zeilen = _tabelle_nach(text, "| Bot | Symbole ohne Faltenevidenz (Lesart H) |", 2)
    evidenz = {}
    for bot_zelle, inhalt in zeilen:
        etikett = _zelle(bot_zelle)
        if etikett in BOTS:
            ziele = [etikett]
        elif "Krypto-Tagesbots" in etikett:
            ziele = list(KRYPTO_TAGESBOTS)
        elif "Aktien-Bots" in etikett:
            ziele = list(AKTIEN_BOTS)
        else:
            continue
        roh = _zelle(inhalt)
        anzahl, _, rest = roh.partition(":")
        symbole = _symbole(rest)
        if len(symbole) != int(anzahl.strip()):
            raise RuntimeError("Beleg widerspricht sich selbst bei %s" % etikett)
        for b in ziele:
            evidenz[b] = symbole
    return zahlen, evidenz


def hole_beleg(modus, arbeitsverzeichnis, beleg_dokument):
    """modus: 'auto' | 'trockenlauf' | 'dokument'."""
    if modus in ("auto", "trockenlauf"):
        try:
            jp = os.path.join(arbeitsverzeichnis, "trockenlauf.json")
            zahlen, evidenz = beleg_aus_trockenlauf(jp)
            return "trockenlauf", zahlen, evidenz
        except Exception as fehler:
            if modus == "trockenlauf":
                raise
            grund = str(fehler)
    else:
        grund = None
    zahlen, evidenz = beleg_aus_dokument(beleg_dokument)
    return ("dokument" if grund is None
            else "dokument (Trockenlauf nicht lauffaehig: %s)" % grund), zahlen, evidenz


# ---------------------------------------------------------------------------
# 4. Die Bot-Dateien: gelesen, nicht importiert
# ---------------------------------------------------------------------------
def bot_min_history(basis=None):
    basis = basis or BASE_DIR
    raus = {}
    for bot in BOTS:
        pfad = os.path.join(basis, "strategies", bot, "multi_symbol_optimise.py")
        treffer = re.findall(r"^(MIN_HISTORY_[A-Z]+)\s*=\s*(\d+)",
                             _lies(pfad), re.MULTILINE)
        if len(treffer) != 1:
            raise RuntimeError("%s: %d Schranken gefunden, erwartet 1"
                               % (bot, len(treffer)))
        raus[bot] = {"name": treffer[0][0], "wert": int(treffer[0][1])}
    return raus


# ---------------------------------------------------------------------------
# 5. Datenstand
# ---------------------------------------------------------------------------
def datenstand(daten_dir):
    h = hashlib.sha256()
    dateien = sorted(f for f in os.listdir(daten_dir) if f.endswith(".csv"))
    for name in dateien:
        pfad = os.path.join(daten_dir, name)
        h.update(name.encode("utf-8"))
        h.update(str(os.path.getsize(pfad)).encode("utf-8"))
        with open(pfad, "rb") as f:
            d = hashlib.sha256()
            for brocken in iter(lambda: f.read(1 << 20), b""):
                d.update(brocken)
        h.update(d.hexdigest().encode("utf-8"))
    return h.hexdigest(), len(dateien)


def _git(repo, *args):
    lauf = subprocess.run(["git"] + list(args), cwd=repo,
                          capture_output=True, text=True)
    if lauf.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), lauf.stderr.strip()))
    return lauf.stdout


def bestimme_basis(repo, angabe, zweig=STANDARD_ZWEIG):
    """Wogegen wird verglichen - und woher kommt diese Antwort?

    Bis TB-43 stand hier schlicht `origin/main`. Das hat zwei verschiedene
    Fehler, die man nicht verwechseln darf:

    * Ist `main` weitergelaufen, schleppt der Diff die Aenderungen ANDERER
      Leute mit herein - das war die Verwirrung aus TB-34. Dagegen hilft
      `git merge-base`, und deshalb ist es jetzt der Standard.
    * Ist der eigene Zweig bereits GEMERGT, ist der Diff leer. Dagegen hilft
      `merge-base` NICHT (die Basis ist dann der eigene Commit selbst, der
      Diff bleibt leer) - dagegen hilft nur, den leeren Vergleich zu melden.
      Das tut `null_entfernte_zeilen` weiter unten.

    Zurueck kommt (Basis, Herkunft); die Herkunft steht im Bericht, damit
    nicht geraten werden muss, wogegen geprueft wurde.
    """
    if angabe:
        return angabe, "ausdruecklich angegeben (--basis)"
    try:
        gefunden = _git(repo, "merge-base", "HEAD", zweig).strip()
    except RuntimeError as fehler:
        return zweig, "Rueckfall auf %s - merge-base nicht ermittelbar (%s)" % (
            zweig, fehler)
    if not gefunden:
        return zweig, "Rueckfall auf %s - merge-base lieferte nichts" % zweig
    return gefunden, "git merge-base HEAD %s" % zweig


# ---------------------------------------------------------------------------
# 6. Die Pruefungen
# ---------------------------------------------------------------------------
def pruefe(auswahl, register_pfad, beleg_pfad, beleg_modus, arbeitsverzeichnis,
           repo, basis, daten_dir, erwarteter_datenstand, erwartete_dateien,
           strategien_basis, basis_zweig=STANDARD_ZWEIG):
    bericht = {"befunde": [], "geprueft": [], "uebersprungen": [], "quellen": {}}

    def an(name):
        return auswahl is None or name in auswahl

    def befund(pruefung, text):
        bericht["befunde"].append({"pruefung": pruefung, "befund": text})

    register_text = _lies(register_pfad)

    # Wogegen verglichen wird, steht ab jetzt IM BERICHT - nicht nur im
    # Quelltext. Ein Werkzeug, das gegen eine von mehreren moeglichen Basen
    # prueft, ohne zu sagen gegen welche, ist die naechste blinde Wache.
    if an("daten_unberuehrt") or an("null_entfernte_zeilen"):
        basis, basis_herkunft = bestimme_basis(repo, basis, basis_zweig)
        bericht["quellen"]["basis"] = {"commit": basis,
                                       "herkunft": basis_herkunft}

    braucht_beleg = an("symbolzahl") or an("faltenevidenz")
    beleg_zahlen = beleg_evidenz = None
    if braucht_beleg:
        quelle, beleg_zahlen, beleg_evidenz = hole_beleg(
            beleg_modus, arbeitsverzeichnis, beleg_pfad)
        bericht["quellen"]["beleg"] = quelle

    if an("symbolzahl"):
        bericht["geprueft"].append("symbolzahl")
        eingetragen = register_symbolzahl(register_text)
        for bot in BOTS:
            if bot not in eingetragen:
                befund("symbolzahl", "%s fehlt in der Registertabelle 16.1.1" % bot)
                continue
            if bot not in beleg_zahlen:
                befund("symbolzahl", "%s fehlt im Beleg" % bot)
                continue
            e, g = eingetragen[bot], beleg_zahlen[bot]
            for schluessel in ("falten", "bestaetigung", "universum"):
                if e[schluessel] != g[schluessel]:
                    befund("symbolzahl",
                           "%s %s: Register %s, gemessen %s"
                           % (bot, schluessel, e[schluessel], g[schluessel]))
        fremd = set(eingetragen) - set(BOTS)
        if fremd:
            befund("symbolzahl", "unbekannte Zeile(n) in 16.1.1: %s" % sorted(fremd))

    if an("faltenevidenz"):
        bericht["geprueft"].append("faltenevidenz")
        eingetragen = register_faltenevidenz(register_text)
        for bot in BOTS:
            if bot not in eingetragen:
                befund("faltenevidenz", "%s fehlt in der Registertabelle 16.1.2" % bot)
                continue
            e, g = eingetragen[bot], beleg_evidenz.get(bot)
            if g is None:
                befund("faltenevidenz", "%s fehlt im Beleg" % bot)
                continue
            if e["symbole"] != sorted(g):
                befund("faltenevidenz",
                       "%s: Register %s, gemessen %s" % (bot, e["symbole"], sorted(g)))
            if e["anzahl"] != len(e["symbole"]):
                befund("faltenevidenz",
                       "%s: eingetragene Anzahl %d, aber %d Symbole aufgezaehlt"
                       % (bot, e["anzahl"], len(e["symbole"])))

    if an("min_history"):
        bericht["geprueft"].append("min_history")
        eingetragen = register_min_history(register_text)
        gelesen = bot_min_history(strategien_basis)
        for bot in BOTS:
            if bot not in eingetragen:
                befund("min_history", "%s fehlt in der Registertabelle 16.7 (b)" % bot)
                continue
            e, g = eingetragen[bot], gelesen[bot]
            if e["name"] != g["name"]:
                befund("min_history", "%s: Register nennt %s, die Bot-Datei %s"
                       % (bot, e["name"], g["name"]))
            if e["wert"] != g["wert"]:
                befund("min_history", "%s %s: Register %d, Bot-Datei %d"
                       % (bot, g["name"], e["wert"], g["wert"]))
        # Der Wortlaut von 3b (b) sagt "die fuenf Werte" - gezaehlt sind es
        # vier Zahlenwerte in zwei Einheiten. Die Tatsachennotiz dazu steht im
        # Register; hier wird nachgezaehlt, nicht geglaettet.
        werte = {(v["name"], v["wert"]) for v in gelesen.values()}
        einheiten = {v["name"] for v in gelesen.values()}
        if len(werte) != 4:
            befund("min_history",
                   "gezaehlt %d verschiedene Schrankenwerte, die Tatsachennotiz "
                   "zu 3b (b) nennt 4" % len(werte))
        if len(einheiten) != 2:
            befund("min_history",
                   "gezaehlt %d Einheiten, die Tatsachennotiz zu 3b (b) nennt 2"
                   % len(einheiten))
        if "vier verschiedene\nZahlenwerte" not in register_text:
            befund("min_history",
                   "Die Tatsachennotiz zu 3b (b) (vier Werte, zwei Einheiten) "
                   "fehlt im Register")

    if an("umstellungstag"):
        bericht["geprueft"].append("umstellungstag")
        if UMSTELLUNGSTAG_ERWARTET not in register_text:
            befund("umstellungstag",
                   "Der Umstellungstag %s steht nicht im Register"
                   % UMSTELLUNGSTAG_ERWARTET)
        with open(UMSTELLUNGSTAG, encoding="utf-8") as f:
            daten = json.load(f)["bots"]
        if sorted(daten) != sorted(BOTS):
            befund("umstellungstag", "umstellungstag_entscheidungskerze.json fuehrt "
                                     "%d Bots, erwartet 9" % len(daten))
        abweichend = {b: v["umgestellt_am"] for b, v in daten.items()
                      if v["umgestellt_am"] != UMSTELLUNGSTAG_ERWARTET}
        if abweichend:
            befund("umstellungstag", "abweichende Umstellungszeitpunkte: %s" % abweichend)

    if an("universumsdatei"):
        bericht["geprueft"].append("universumsdatei")
        pfad = os.path.join(BASE_DIR, "config", "top25_symbols.txt")
        roh = _lies(pfad)
        zeilen = [z.strip() for z in roh.splitlines() if z.strip()]
        sha = hashlib.sha256(roh.encode("utf-8")).hexdigest()
        erwartet_hash = ("3afc95a4f6b5ebc3a8f7bb7854b5dd59"
                         "c4ecc4e3d86aa7b93c08066a3fccf810")
        if sha != erwartet_hash:
            befund("universumsdatei",
                   "top25_symbols.txt hat den Hash %s, registriert ist %s"
                   % (sha[:16], erwartet_hash[:16]))
        if len(zeilen) != 25:
            befund("universumsdatei",
                   "top25_symbols.txt hat %d nichtleere Zeilen, der korrigierte "
                   "Rechenweg nennt 25" % len(zeilen))
        if "PAXGUSDT" in zeilen:
            befund("universumsdatei",
                   "PAXGUSDT steht doch in der Datei - dann war die alte Klammer richtig")
        if "XAUTUSDT" not in zeilen:
            befund("universumsdatei", "XAUTUSDT steht nicht in der Datei")
        if len(zeilen) - 1 != 24:
            befund("universumsdatei", "25 abzueglich XAUTUSDT ist nicht 24")
        if "**24 (25 Zeilen abzüglich `XAUTUSDT`)**" not in register_text:
            befund("universumsdatei",
                   "Der korrigierte Rechenweg steht nicht im Register (16.1.3)")

    if an("datenstand"):
        bericht["geprueft"].append("datenstand")
        sha, anzahl = datenstand(daten_dir)
        bericht["quellen"]["datenstand"] = {"sha256": sha, "dateien": anzahl}
        if not sha.startswith(erwarteter_datenstand):
            befund("datenstand", "Datenstand %s..., registriert ist %s..."
                   % (sha[:16], erwarteter_datenstand))
        if anzahl != erwartete_dateien:
            befund("datenstand", "%d Kursdateien, registriert sind %d"
                   % (anzahl, erwartete_dateien))

    if an("daten_unberuehrt"):
        bericht["geprueft"].append("daten_unberuehrt")
        try:
            veraendert = _git(repo, "diff", "--name-only", basis, "--", "data").split()
            offen = [z[3:] for z in _git(repo, "status", "--porcelain",
                                         "--", "data").splitlines()]
        except RuntimeError as fehler:
            befund("daten_unberuehrt", "git nicht auswertbar: %s" % fehler)
        else:
            for name in sorted(set(veraendert) | set(offen)):
                befund("daten_unberuehrt", "unter data/ veraendert: %s" % name)

    if an("null_entfernte_zeilen"):
        bericht["geprueft"].append("null_entfernte_zeilen")
        try:
            roh = _git(repo, "diff", "--numstat", basis, "--",
                       "docs/VORREGISTRIERUNG_neuselektion.md",
                       "docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md")
        except RuntimeError as fehler:
            befund("null_entfernte_zeilen", "git nicht auswertbar: %s" % fehler)
        else:
            zeilen = roh.strip().splitlines()
            bericht["quellen"]["numstat"] = zeilen
            if not zeilen:
                # DAS ist der TB-43-Fehler: ohne diese Meldung war die
                # Pruefung nach jedem Merge trivial gruen. Ein leerer
                # Vergleich ist kein Nachweis, dass nichts entfernt wurde -
                # er ist gar kein Nachweis. Ein Werkzeug, das nicht mehr
                # misst, sagt es.
                befund("null_entfernte_zeilen",
                       "LEERER VERGLEICH gegen %s: keine der beiden "
                       "Registerdateien steht im Diff. Diese Pruefung hat "
                       "damit NICHTS geprueft - das ist kein Erfolg. "
                       "Haeufigster Grund: der Zweig ist bereits gemergt. "
                       "Abhilfe: --basis <Commit vor dem Eintrag> angeben."
                       % basis)
            for zeile in zeilen:
                dazu, weg, datei = zeile.split("\t")
                if weg != "0":
                    befund("null_entfernte_zeilen",
                           "%s: %s entfernte Zeile(n) - erlaubt sind 0" % (datei, weg))

    if an("ersetzt_gekennzeichnet"):
        bericht["geprueft"].append("ersetzt_gekennzeichnet")
        for name, alttext, verweis in ERSETZT:
            if alttext not in register_text:
                befund("ersetzt_gekennzeichnet",
                       "%s: die ersetzte Fassung steht nicht mehr da" % name)
                continue
            i = register_text.index(alttext)
            fenster = register_text[i:i + 1400]
            if "ERSETZT durch Abschnitt 16" not in fenster and \
               "KORRIGIERT in" not in fenster:
                befund("ersetzt_gekennzeichnet",
                       "%s: kein Verweis auf den Nachtrag in der Naehe" % name)
            elif verweis not in fenster:
                befund("ersetzt_gekennzeichnet",
                       "%s: der Verweis nennt %s nicht" % (name, verweis))

    if auswahl:
        bericht["uebersprungen"] = [n for n in (
            "symbolzahl", "faltenevidenz", "min_history", "umstellungstag",
            "universumsdatei", "datenstand", "daten_unberuehrt",
            "null_entfernte_zeilen", "ersetzt_gekennzeichnet")
            if n not in auswahl]
    return bericht


# ---------------------------------------------------------------------------
# 7. Ausgabe
# ---------------------------------------------------------------------------
def drucke(bericht):
    br = "=" * 78
    print(br)
    print("TB-41 REGISTERNACHTRAG - Pruefung der eingetragenen Zahlen")
    print(br)
    for schluessel, wert in bericht["quellen"].items():
        print("  Quelle %-12s %s" % (schluessel + ":", wert))
    print()
    print("  geprueft:      %s" % ", ".join(bericht["geprueft"]))
    if bericht["uebersprungen"]:
        print("  uebersprungen: %s" % ", ".join(bericht["uebersprungen"]))
    print()
    if not bericht["befunde"]:
        print("  KEIN BEFUND - jede eingetragene Zahl stimmt mit ihrer Quelle ueberein.")
    else:
        print("  %d BEFUND(E):" % len(bericht["befunde"]))
        for b in bericht["befunde"]:
            print("    [%s] %s" % (b["pruefung"], b["befund"]))
    print(br)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--nur", action="append", default=None,
                   help="nur diese Pruefung (mehrfach moeglich)")
    p.add_argument("--register", default=REGISTER)
    p.add_argument("--beleg", default=BELEG_TB40)
    p.add_argument("--beleg-modus", default="auto",
                   choices=["auto", "trockenlauf", "dokument"])
    p.add_argument("--repo", default=BASE_DIR)
    p.add_argument("--basis", default=None,
                   help="Vergleichsbasis. Standard: git merge-base HEAD gegen "
                        "--basis-zweig")
    p.add_argument("--basis-zweig", default=STANDARD_ZWEIG,
                   help="Zweig, gegen den die Basis bestimmt wird")
    p.add_argument("--daten", default=os.path.join(BASE_DIR, "data"))
    p.add_argument("--strategien", default=BASE_DIR,
                   help="Wurzel, unter der strategies/<bot>/ liegt")
    p.add_argument("--erwarteter-datenstand", default=DATENSTAND_PRAEFIX)
    p.add_argument("--erwartete-dateien", type=int, default=DATENSTAND_DATEIEN)
    p.add_argument("--arbeitsverzeichnis", default=None)
    p.add_argument("--json", default=None)
    a = p.parse_args(argv)

    arbeit = a.arbeitsverzeichnis or os.environ.get("TMPDIR") or "/tmp"
    bericht = pruefe(set(a.nur) if a.nur else None, a.register, a.beleg,
                     a.beleg_modus, arbeit, a.repo, a.basis, a.daten,
                     a.erwarteter_datenstand, a.erwartete_dateien, a.strategien,
                     a.basis_zweig)
    drucke(bericht)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(bericht, f, ensure_ascii=False, indent=1)
    return 1 if bericht["befunde"] else 0


if __name__ == "__main__":
    sys.exit(main())
