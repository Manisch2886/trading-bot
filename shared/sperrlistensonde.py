#!/usr/bin/env python3
"""
Die Sperrlisten-Sonde (TB-85, Schritt 1 von Fables Reihenfolge 36.3)
==============================================================================
Registertext 36.2 verlangt ein Pruefskript, das **fuer jeden Sperrlistenpunkt
Pfad und Hash gegen den Registertext prueft**; 36.5 gibt ihm drei Ausgaenge,
36.6 seinen Gegenstand: das **Abbild der Sperrliste**, eine eigene Datei, die
genau die Punkte des Registerabschnitts 10 mit Pfad und Hash traegt.

Die Sonde prueft zwei Dinge (36.6):

  (i)   jeden Punkt des Abbilds gegen die Datei im Repo - Hash neu gemessen;
  (ii)  das Abbild gegen den Registertext von Abschnitt 10 - Punktzahl,
        Titel, Pfade und der nicht dateibezogene Wortlaut je Punkt.

⚠️ **Was der Registertext hergibt, und was nicht.** Abschnitt 10 nennt bei
den meisten Punkten nicht nur Dateien: Konstanten (`SEED = 20260913`),
Funktionen (`herkunft.py::register()`), einen Docstring, einen Repo-Commit
oder schlicht einen anderen Registerabschnitt. Eine Datei kann die Sonde
hashen; eine Konstante, eine Funktion oder einen Registerverweis kann sie
**nicht** messen, ohne etwas zu erfinden. Solche Punkte werden **einzeln mit
2 gemeldet und benannt** - nie uebersprungen, nie als geprueft gefuehrt.
Ein Punkt, der Dateien UND Nicht-Messbares nennt, ist damit ebenfalls 2:
seine Dateien sind gemessen (und stehen im Bericht), der Punkt als Ganzes
nicht. ⭐ Das ist der Vorschlag des steuernden Chats an Fable (Anfrage 22c,
Abschnitt 4); seine Antwort steht aus. Die Sonde ist neu und nicht gesperrt -
entscheidet er anders, ist sie aenderbar.

Rueckgabewerte - Bauart `shared/snapshot.py --pruefen` (36.5)
------------------------------------------------------------------------------
    0   geprueft und in Ordnung
    1   geprueft und BEFUND - Abweichung, der Punkt wird genannt
    2   NICHT PRUEFBAR - Eingabe fehlt, Quelle nicht lesbar, Aufruf gescheitert,
        oder ein Punkt, fuer den der Registertext nichts Messbares hergibt

Gesamtwert: 1, wenn irgendein Punkt oder die Pruefung (ii) einen Befund hat;
sonst 2, wenn irgendein Punkt nicht pruefbar war; sonst 0. ⛔ **Ein 1 schlaegt
ein 2** - ein Befund ist wichtiger als eine Luecke. Und: **kein Aufruf endet
mit 0, ohne dass gemessen wurde** (36.5). Der Grund fuer die 2 steht im Kopf
von `snapshot.py` (Vorfall TB-45: zwei Wachen meldeten "bestanden", ohne
gemessen zu haben).

Wie der Registertext gelesen wird (der Parser - genau EINMAL, hier)
------------------------------------------------------------------------------
Der Erzeuger des Abbilds (`research/vorregistrierung/sperrliste_abbild.py`)
und die Pruefung (ii) lesen Abschnitt 10 mit **derselben** Funktion
`lies_abschnitt_10`. Ein Parserfehler waere fuer (ii) deshalb unsichtbar;
dagegen stehen die von Hand gemessene Klassifikation
(`docs/belege/TB-85/schritt1_klassifikation.txt`) und die Mutationsproben in
`shared/test_sperrlistensonde.py`.

  R1  Ein Punkt beginnt mit `<n>. **` in Spalte 0; eingerueckte Folgezeilen
      gehoeren dazu.
  R2  Eingerueckte Blockquote-Zeilen (`   > ...`) sind Tatsachennotizen und
      Marken am alten Ort - nicht der Punkt.
  R3  Der Titel ist der erste `**...**`-Block, auch wenn er umbrochen ist.
  R4  Ein Dateipfad ist ein `...`-Token mit Dateiendung, gegebenenfalls vor
      `::`. `datei::funktion` nennt die Datei (Pfad) UND die Funktion (nicht
      dateibezogen). `modul.KONSTANTE` ist kein Pfad.
  R5  Aufloesung: kein `/` oder Praefix `ergebnisse/` -> relativ zu
      `research/vorregistrierung/` (dem Code-Ordner des Registers); sonst
      repo-relativ. Die Regel haengt NICHT davon ab, ob die Datei existiert.
  R6  `nicht_dateibezogen` ist der Wortlaut nach dem Titel, sobald er mehr als
      Dateipfade und Trennzeichen enthaelt; sonst leer.

Was die Sonde NICHT tut
------------------------------------------------------------------------------
Sie schreibt nichts. Sie repariert nichts - ein Sperrlistenbruch ist nach 36.2
eine Tatsachennotiz. Sie kennt `herkunft.py` `EINGEFROREN` und
`SPERRLISTE_DATEIEN` nicht (36.6: die sind nicht das Abbild). Und sie prueft
`ergebnisse/benchmark_drawdowns_vt.json` **nicht** - die Datei ist kein Punkt
des Abschnitts 10, sondern "fuer die Sperrliste bestimmt" (21.9/23.7); ob die
Sonde sie pruefen soll, liegt bei Fable (Anfrage 22c). Bis dahin nennt der
Bericht sie in einem eigenen Abschnitt mit ihrem heutigen Hash, ohne Wertung.

Nutzung
------------------------------------------------------------------------------
    python3 shared/sperrlistensonde.py --abbild <pfad> [--json]
    python3 shared/sperrlistensonde.py --abbild <pfad> --register <md> --wurzel <dir>
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_HIER)

OK = 0
BEFUND = 1
NICHT_PRUEFBAR = 2

REGISTER = os.path.join("docs", "VORREGISTRIERUNG_neuselektion.md")
ABSCHNITT_UEBERSCHRIFT = "## 10. Die Sperrliste"
CODEORDNER = os.path.join("research", "vorregistrierung")

# Fuer die Sperrliste bestimmt, aber kein Punkt des Abschnitts 10 (21.9/23.7):
# im Bericht genannt, nicht geprueft - Entscheidung bei Fable (Anfrage 22c).
BESTIMMT_NICHT_EINGETRAGEN = (
    (os.path.join(CODEORDNER, "ergebnisse", "benchmark_drawdowns_vt.json"),
     "Register 21.9/23.7 - fuer die Sperrliste bestimmt, Vollzug steht aus"),
)

_RE_PUNKT = re.compile(r"^(\d{1,2})\. \*\*")
_RE_TITEL = re.compile(r"^(\d{1,2})\. \*\*(.+?)\*\*(.*)$")
_RE_TOKEN = re.compile(r"`([^`]+)`")
_RE_DATEI = re.compile(r"^[\w./-]+\.(py|json|txt|csv|md|jsonl)$")
_TRENNER = re.compile(r"[\s—,;]+|\bund\b")


class Sondenfehler(Exception):
    """Etwas liess sich nicht pruefen - Ausgang 2, nie 0."""


def sha256_datei(pfad):
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Der Parser (R1-R6)
# ---------------------------------------------------------------------------

def _aufloesen(pfad):
    """R5: Ort im Repo, aus dem Wortlaut allein - ohne Blick auf die Platte."""
    if "/" not in pfad or pfad.startswith("ergebnisse/"):
        return os.path.join(CODEORDNER, pfad).replace(os.sep, "/")
    return pfad


def _zerlege_punkt(nummer, text):
    """Aus dem zusammengefuegten Wortlaut eines Punktes: Titel, Pfade, Rest."""
    m = _RE_TITEL.match(text)
    if not m or int(m.group(1)) != nummer:
        raise Sondenfehler("Punkt %d ohne lesbaren Titel: %r" % (nummer, text))
    titel = " ".join(m.group(2).split())
    rest = " ".join(m.group(3).split())

    pfade, reine_pfade = [], []
    for token in _RE_TOKEN.findall(rest):
        datei = token.split("::", 1)[0] if "::" in token else token
        if _RE_DATEI.match(datei):
            p = _aufloesen(datei)
            if p not in pfade:
                pfade.append(p)
            if "::" not in token:
                reine_pfade.append(token)

    # R6: bleibt nach Abzug der reinen Dateipfade und Trennzeichen etwas
    # uebrig, nennt der Punkt mehr als Dateien.
    probe = rest
    for token in reine_pfade:
        probe = probe.replace("`%s`" % token, " ")
    probe = _TRENNER.sub(" ", probe).strip()
    nicht_dateibezogen = rest.lstrip("— ").strip() if probe else ""

    return {"punkt": nummer, "titel": titel, "pfade": pfade,
            "nicht_dateibezogen": nicht_dateibezogen,
            "quelle": "Registerabschnitt 10, Punkt %d" % nummer}


def lies_abschnitt_10(register_pfad):
    """Liest die nummerierte Liste des Abschnitts 10 aus dem Register.

    Liefert (punkte, zeilen, listentext): die Punkte ohne Hashes, das
    Zeilenintervall (1-basiert, einschliesslich) und den Wortlaut der
    Punktzeilen ohne Blockquotes (fuer einen Informations-Hash).
    Wirft Sondenfehler, wenn das Register nicht lesbar ist oder die Liste
    nicht die erwartete Form hat.
    """
    try:
        with open(register_pfad, encoding="utf-8") as f:
            zeilen = f.read().split("\n")
    except OSError as e:
        raise Sondenfehler("Register nicht lesbar: %s (%s)" % (register_pfad, e))

    try:
        start = next(i for i, z in enumerate(zeilen)
                     if z.startswith(ABSCHNITT_UEBERSCHRIFT))
    except StopIteration:
        raise Sondenfehler("Ueberschrift %r nicht im Register %s"
                           % (ABSCHNITT_UEBERSCHRIFT, register_pfad))

    punkte_roh = []      # [(nummer, [zeilen]), ...]
    aktuell = None
    von = bis = None
    for i in range(start + 1, len(zeilen)):
        z = zeilen[i]
        if z.startswith("## ") or z.startswith("### "):
            break
        m = _RE_PUNKT.match(z)
        if m:
            aktuell = (int(m.group(1)), [z])
            punkte_roh.append(aktuell)
            von = von if von is not None else i + 1
            bis = i + 1
        elif aktuell is not None and z.startswith("   "):
            if z.strip().startswith(">"):
                continue                       # R2: Notiz, nicht der Punkt
            aktuell[1].append(z)
            bis = i + 1
        elif z.strip() == "":
            aktuell = None
        else:
            if punkte_roh:
                break                          # Liste zu Ende
            # Einleitung vor der Liste - weiterlesen

    if not punkte_roh:
        raise Sondenfehler("Abschnitt 10 enthaelt keine nummerierte Liste")
    nummern = [n for n, _ in punkte_roh]
    if nummern != list(range(1, len(nummern) + 1)):
        raise Sondenfehler("Punktnummern nicht lueckenlos 1..n: %s" % nummern)

    punkte = []
    listentext = []
    for nummer, roh in punkte_roh:
        text = " ".join(" ".join(roh).split())
        listentext.append(text)
        punkte.append(_zerlege_punkt(nummer, text))
    return punkte, (von, bis), "\n".join(listentext)


# ---------------------------------------------------------------------------
# Das Abbild bilden (fuer den Erzeuger - der schreibt, diese Datei nicht)
# ---------------------------------------------------------------------------

def _head(wurzel):
    try:
        return subprocess.run(["git", "-C", wurzel, "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True,
                              timeout=10).stdout.strip()
    except Exception:
        return "unbekannt"


def bilde_abbild(register_pfad, wurzel, erzeuger="?"):
    """Das Abbild als Datenstruktur: die Punkte des Abschnitts 10, je mit
    frisch gemessenen Hashes. Fehlt eine genannte Datei, ist das Abbild nicht
    bildbar (Sondenfehler) - ein Abbild mit Luecke ist keins."""
    punkte, (von, bis), listentext = lies_abschnitt_10(register_pfad)
    for p in punkte:
        hashes = {}
        for rel in p["pfade"]:
            voll = os.path.join(wurzel, rel)
            if not os.path.isfile(voll):
                raise Sondenfehler("Punkt %d nennt %s - Datei fehlt unter %s"
                                   % (p["punkt"], rel, wurzel))
            hashes[rel] = sha256_datei(voll)
        p["hashes"] = hashes
    return {
        "art": "Abbild der Sperrliste - Registerabschnitt 10 (Registertext 36.6)",
        "erzeugt": {
            "zeitpunkt_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "head": _head(wurzel),
            "erzeuger": erzeuger,
            "parser": "shared/sperrlistensonde.py::lies_abschnitt_10",
        },
        "quelle": {
            "register": os.path.relpath(register_pfad, wurzel).replace(os.sep, "/"),
            "abschnitt": "10",
            "zeilen": [von, bis],
            "sha256_listentext": sha256_text(listentext),
        },
        "pfadregel": ("kein '/' oder Praefix 'ergebnisse/' -> relativ zu "
                      "research/vorregistrierung/; sonst repo-relativ"),
        "punkte": punkte,
    }


# ---------------------------------------------------------------------------
# Die Pruefung
# ---------------------------------------------------------------------------

_FELDER = ("punkt", "titel", "pfade", "hashes", "nicht_dateibezogen", "quelle")


def _lade_abbild(abbild_pfad):
    try:
        with open(abbild_pfad, encoding="utf-8") as f:
            abbild = json.load(f)
    except OSError as e:
        raise Sondenfehler("Abbild nicht lesbar: %s (%s)" % (abbild_pfad, e))
    except ValueError as e:
        raise Sondenfehler("Abbild kein gueltiges JSON: %s (%s)" % (abbild_pfad, e))
    punkte = abbild.get("punkte")
    if not isinstance(punkte, list) or not punkte:
        raise Sondenfehler("Abbild ohne Punkte: %s" % abbild_pfad)
    for p in punkte:
        fehlend = [f for f in _FELDER if f not in p]
        if fehlend:
            raise Sondenfehler("Abbild-Punkt %r ohne Felder %s"
                               % (p.get("punkt"), fehlend))
    return abbild


def _pruefe_punkt(p, wurzel):
    """(i) fuer einen Punkt: Hashes neu messen. Liefert (ausgang, gruende, dateien)."""
    gruende, dateien = [], []
    ausgang = OK
    for rel in p["pfade"]:
        voll = os.path.join(wurzel, rel)
        soll = p["hashes"].get(rel)
        if soll is None:
            dateien.append((rel, "kein Hash im Abbild", None))
            gruende.append("Abbild nennt %s ohne Hash" % rel)
            ausgang = max(ausgang, NICHT_PRUEFBAR)
            continue
        if not os.path.isfile(voll):
            dateien.append((rel, "FEHLT", None))
            gruende.append("Datei fehlt: %s" % rel)
            ausgang = max(ausgang, NICHT_PRUEFBAR)
            continue
        try:
            ist = sha256_datei(voll)
        except OSError as e:
            dateien.append((rel, "nicht lesbar", None))
            gruende.append("Datei nicht lesbar: %s (%s)" % (rel, e))
            ausgang = max(ausgang, NICHT_PRUEFBAR)
            continue
        if ist == soll:
            dateien.append((rel, "gleich", ist))
        else:
            dateien.append((rel, "ABWEICHUNG", ist))
            gruende.append("Hash weicht ab: %s soll %s… ist %s…"
                           % (rel, soll[:12], ist[:12]))
            ausgang = BEFUND
    if ausgang == BEFUND:
        return BEFUND, gruende, dateien
    if not p["pfade"]:
        gruende.append("kein Dateipfad im Registertext - nicht messbar: %s"
                       % (p["nicht_dateibezogen"] or "(nichts genannt)"))
        return NICHT_PRUEFBAR, gruende, dateien
    if p["nicht_dateibezogen"]:
        gruende.append("nennt Nicht-Dateibezogenes - nicht messbar: %s"
                       % p["nicht_dateibezogen"])
        return NICHT_PRUEFBAR, gruende, dateien
    if ausgang == NICHT_PRUEFBAR:
        return NICHT_PRUEFBAR, gruende, dateien
    return OK, gruende, dateien


def _vergleiche_mit_register(abbild, register_pfad):
    """(ii): Abbild gegen den Registertext. Liefert (ausgang, befunde, notiz)."""
    try:
        punkte_reg, (von, bis), listentext = lies_abschnitt_10(register_pfad)
    except Sondenfehler as e:
        return NICHT_PRUEFBAR, [str(e)], {}
    befunde = []
    ab = abbild["punkte"]
    if len(ab) != len(punkte_reg):
        befunde.append("Punktzahl: Abbild %d, Registertext %d"
                       % (len(ab), len(punkte_reg)))
    for a, r in zip(ab, punkte_reg):
        for feld in ("punkt", "titel", "pfade", "nicht_dateibezogen"):
            if a[feld] != r[feld]:
                befunde.append("Punkt %s, Feld %s: Abbild %r, Registertext %r"
                               % (a["punkt"], feld, a[feld], r[feld]))
    notiz = {"zeilen": [von, bis], "punkte": len(punkte_reg),
             "sha256_listentext": sha256_text(listentext),
             "listentext_wie_bei_erzeugung":
                 sha256_text(listentext) == abbild.get("quelle", {}).get("sha256_listentext")}
    return (BEFUND if befunde else OK), befunde, notiz


def pruefen(abbild_pfad, register_pfad, wurzel):
    """Die ganze Sonde. Liefert den Bericht als dict; ["ausgang"] ist 0/1/2."""
    bericht = {"abbild": abbild_pfad, "register": register_pfad,
               "wurzel": wurzel, "punkte": [], "ii": {}, "bestimmt": [],
               "ausgang": None, "grund": None}
    try:
        abbild = _lade_abbild(abbild_pfad)
    except Sondenfehler as e:
        bericht["ausgang"] = NICHT_PRUEFBAR
        bericht["grund"] = str(e)
        return bericht
    bericht["abbild_sha256"] = sha256_datei(abbild_pfad)
    bericht["abbild_erzeugt"] = abbild.get("erzeugt", {})

    # (i)
    for p in abbild["punkte"]:
        ausgang, gruende, dateien = _pruefe_punkt(p, wurzel)
        bericht["punkte"].append({
            "punkt": p["punkt"], "titel": p["titel"], "ausgang": ausgang,
            "gruende": gruende,
            "dateien": [{"pfad": rel, "stand": stand, "sha256": h}
                        for rel, stand, h in dateien]})

    # (ii)
    ausgang_ii, befunde, notiz = _vergleiche_mit_register(abbild, register_pfad)
    bericht["ii"] = {"ausgang": ausgang_ii, "befunde": befunde, **notiz}

    # bestimmt, nicht eingetragen - ohne Wertung
    for rel, warum in BESTIMMT_NICHT_EINGETRAGEN:
        voll = os.path.join(wurzel, rel)
        bericht["bestimmt"].append({
            "pfad": rel, "warum": warum,
            "sha256": sha256_datei(voll) if os.path.isfile(voll) else None})

    ausgaenge = [p["ausgang"] for p in bericht["punkte"]] + [ausgang_ii]
    if BEFUND in ausgaenge:
        bericht["ausgang"] = BEFUND
        bericht["grund"] = ("BEFUND in Punkt(en) %s%s" % (
            [p["punkt"] for p in bericht["punkte"] if p["ausgang"] == BEFUND],
            " und in (ii) Abbild/Registertext" if ausgang_ii == BEFUND else ""))
    elif NICHT_PRUEFBAR in ausgaenge:
        bericht["ausgang"] = NICHT_PRUEFBAR
        bericht["grund"] = ("NICHT PRUEFBAR: Punkt(e) %s%s" % (
            [p["punkt"] for p in bericht["punkte"] if p["ausgang"] == NICHT_PRUEFBAR],
            " und (ii) Registertext nicht lesbar" if ausgang_ii == NICHT_PRUEFBAR else ""))
    else:
        bericht["ausgang"] = OK
        bericht["grund"] = "alle Punkte gemessen und gleich, Abbild = Registertext"
    return bericht


# ---------------------------------------------------------------------------
# Ausgabe
# ---------------------------------------------------------------------------

_WORT = {OK: "0 in Ordnung", BEFUND: "1 BEFUND", NICHT_PRUEFBAR: "2 NICHT PRUEFBAR"}


def _drucke(b):
    print("Sperrlisten-Sonde (Register 36.2/36.5/36.6)")
    print("  Abbild:   %s" % b["abbild"])
    print("  Register: %s" % b["register"])
    print("  Wurzel:   %s" % b["wurzel"])
    if b["grund"] and not b["punkte"]:
        print("\nABBRUCH: %s" % b["grund"])
        print("\nRUECKGABEWERT %s" % _WORT[b["ausgang"]])
        return
    print("  Abbild-Hash: %s" % b["abbild_sha256"])
    e = b["abbild_erzeugt"]
    print("  erzeugt: %s  HEAD %s  von %s" % (e.get("zeitpunkt_utc"),
                                              (e.get("head") or "?")[:12],
                                              e.get("erzeuger")))
    print("\n(i) Jeder Punkt des Abbilds gegen die Datei im Repo:")
    for p in b["punkte"]:
        print("  Punkt %2d  [%s]  %s" % (p["punkt"], _WORT[p["ausgang"]], p["titel"]))
        for d in p["dateien"]:
            print("            %-62s %-10s %s" % (d["pfad"], d["stand"],
                                                  (d["sha256"] or "")[:16]))
        for g in p["gruende"]:
            print("            -> %s" % g)
    ii = b["ii"]
    print("\n(ii) Abbild gegen den Registertext von Abschnitt 10:  [%s]" % _WORT[ii["ausgang"]])
    if ii.get("punkte") is not None:
        print("  Registertext: %d Punkte, Z. %d-%d, Listentext wie bei Erzeugung: %s"
              % (ii["punkte"], ii["zeilen"][0], ii["zeilen"][1],
                 "ja" if ii["listentext_wie_bei_erzeugung"] else "NEIN (nur Hinweis)"))
    for f in ii["befunde"]:
        print("  -> %s" % f)
    print("\nBestimmt, nicht eingetragen (kein Punkt des Abschnitts 10; nicht geprueft, nur genannt):")
    for d in b["bestimmt"]:
        print("  %s  %s  (%s)" % (d["pfad"], d["sha256"] or "FEHLT", d["warum"]))
    n = {k: sum(1 for p in b["punkte"] if p["ausgang"] == k) for k in (OK, BEFUND, NICHT_PRUEFBAR)}
    print("\nBilanz: %d Punkte in Ordnung (0), %d mit Befund (1), %d nicht pruefbar (2); (ii) %s"
          % (n[OK], n[BEFUND], n[NICHT_PRUEFBAR], _WORT[ii["ausgang"]]))
    print("RUECKGABEWERT %s - %s" % (_WORT[b["ausgang"]], b["grund"]))


def main(argv=None):
    z = argparse.ArgumentParser(
        description="Prueft das Abbild der Sperrliste gegen das Repo und "
                    "gegen Registerabschnitt 10 (36.2/36.5/36.6). Schreibt nichts.")
    z.add_argument("--abbild", required=True, metavar="PFAD",
                   help="die Abbild-Datei (JSON, 36.6)")
    z.add_argument("--register", default=None, metavar="PFAD",
                   help="das Register (Standard: <wurzel>/%s)" % REGISTER)
    z.add_argument("--wurzel", default=BASE_DIR,
                   help="Repo-Wurzel, auf die sich die Pfade beziehen")
    z.add_argument("--json", action="store_true",
                   help="den Bericht als JSON ausgeben statt als Text")
    a = z.parse_args(argv)
    register = a.register or os.path.join(a.wurzel, REGISTER)
    try:
        bericht = pruefen(a.abbild, register, a.wurzel)
    except Exception as e:          # ein gescheiterter Aufruf ist 2, nie 0
        print("ABBRUCH: Sonde gescheitert: %r" % (e,), file=sys.stderr)
        return NICHT_PRUEFBAR
    if a.json:
        print(json.dumps(bericht, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        _drucke(bericht)
    return bericht["ausgang"]


if __name__ == "__main__":
    sys.exit(main())
