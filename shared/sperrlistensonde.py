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
eine Tatsachennotiz. `SPERRLISTE_DATEIEN` in `herkunft.py` kennt sie nicht
(toter Code, 37.4).

Die drei Gruppen kommen AUS DEM ABBILD (40.8 (e), TB-97)
------------------------------------------------------------------------------
Fable 24a: "Eine Gruppe, die im Code der Sonde steht, ist ein Literal in einer
Wache." Bis TB-97 stand die Gruppe "bestimmt" hier als Konstante
(`BESTIMMT_NICHT_EINGETRAGEN`, nur genannt, nicht geprueft). Seit TB-97 liest
die Sonde alle drei Gruppen aus dem Abbild und prueft sie gleich (Hash gegen
Abbild, 37.2):

  punkte       die Punkte des Abschnitts 10 (36.6)
  bestimmt     Pfade, die das Register fuer die Sperrliste vorsieht, deren
               Vollzug aussteht (37.2); am Tag leer. Je Eintrag pfad, sha256,
               grund.
  eingefroren  `herkunft.py::EINGEFROREN`, die Abschnitt-0-Menge, ueber die
               `register()` hasht (39.7, Fable 23c: "dritte Gruppe"). Je
               Eintrag pfad, sha256; der Erzeuger liest die Liste mit
               `lies_eingefroren` (ast, ohne `herkunft.py` auszufuehren).

Fuehrt ein Abbild eine Gruppe NICHT (Abbilder vor TB-97), ist sie nicht
pruefbar (2) und wird so genannt - eine leere Gruppe (`[]`) ist dagegen
gemessen und 0. Leer und fehlend sind verschiedene Aussagen.

Die Schlusszeilen trennen Pfad- und Regel-Bestandteile (40.8 (d), Fable 24a);
der Gesamtwert bleibt, wie 36.5 ihn definiert. Ein Punkt kann im Abbild ein
Feld `tatsachennotiz` tragen - den Verweis, den die Regelzeile je Punkt nennt;
fehlt es, sagt die Zeile "keine im Abbild" (Tag-Vorbedingung 23c).

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

HERKUNFT = os.path.join(CODEORDNER, "herkunft.py")

# Die zwei Gruppen neben den Punkten - Schluessel im Abbild und Name im Bericht
# (37.2, 39.7). Die INHALTE stehen im Abbild, nicht hier.
GRUPPEN = (("bestimmt", "bestimmt (37.2)"),
           ("eingefroren", "Abschnitt 0 - herkunft.py::EINGEFROREN (39.7)"))

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


def lies_eingefroren(wurzel):
    """Die Liste `EINGEFROREN` aus `herkunft.py` - mit `ast` gelesen, nicht
    importiert (herkunft.py steht auf der Sperrliste, Punkte 11/12; gelesen
    wird, ausgefuehrt nicht). Aufgeloest nach R5. Wirft Sondenfehler, wenn die
    Datei fehlt oder die Liste nicht als Liste von Zeichenketten dasteht."""
    import ast
    pfad = os.path.join(wurzel, HERKUNFT)
    try:
        with open(pfad, encoding="utf-8") as f:
            baum = ast.parse(f.read())
    except (OSError, SyntaxError) as e:
        raise Sondenfehler("herkunft.py nicht lesbar: %s (%s)" % (pfad, e))
    for knoten in baum.body:
        if (isinstance(knoten, ast.Assign) and len(knoten.targets) == 1
                and getattr(knoten.targets[0], "id", None) == "EINGEFROREN"):
            try:
                werte = ast.literal_eval(knoten.value)
            except ValueError:
                break
            if isinstance(werte, list) and all(isinstance(w, str) for w in werte):
                return [_aufloesen(w) for w in werte]
            break
    raise Sondenfehler("EINGEFROREN in %s nicht als Liste von Pfaden lesbar" % pfad)


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


def _hash_oder_fehler(wurzel, rel, wer):
    voll = os.path.join(wurzel, rel)
    if not os.path.isfile(voll):
        raise Sondenfehler("%s nennt %s - Datei fehlt unter %s" % (wer, rel, wurzel))
    return sha256_datei(voll)


def bilde_abbild(register_pfad, wurzel, erzeuger="?", bestimmt=()):
    """Das Abbild als Datenstruktur: die Punkte des Abschnitts 10 und die zwei
    Gruppen `bestimmt` und `eingefroren`, je mit frisch gemessenen Hashes.
    `bestimmt` ist eine Folge (pfad, grund) - Handwerk des Aufrufers, weil das
    Register die Gruppe nicht als Liste fuehrt; leer heisst leer (37.2: am Tag
    leer). Fehlt eine genannte Datei, ist das Abbild nicht bildbar
    (Sondenfehler) - ein Abbild mit Luecke ist keins."""
    punkte, (von, bis), listentext = lies_abschnitt_10(register_pfad)
    for p in punkte:
        p["hashes"] = {rel: _hash_oder_fehler(wurzel, rel, "Punkt %d" % p["punkt"])
                       for rel in p["pfade"]}
    gruppe_bestimmt = [{"pfad": rel, "grund": grund,
                        "sha256": _hash_oder_fehler(wurzel, rel, "Gruppe bestimmt")}
                       for rel, grund in bestimmt]
    gruppe_eingefroren = [{"pfad": rel,
                           "sha256": _hash_oder_fehler(wurzel, rel, "EINGEFROREN")}
                          for rel in lies_eingefroren(wurzel)]
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
        "bestimmt": gruppe_bestimmt,
        "eingefroren": gruppe_eingefroren,
        "gruppenquelle": {
            "bestimmt": "Aufruf des Erzeugers (--bestimmt), Register 37.2/39.3",
            "eingefroren": "%s::EINGEFROREN, gelesen mit lies_eingefroren (ast)" % HERKUNFT,
        },
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


def _pruefe_gruppe(abbild, schluessel, wurzel):
    """Eine der zwei Gruppen neben den Punkten, gleich geprueft (37.2): Hash
    gegen Abbild. Fehlt die Gruppe im Abbild, ist sie nicht pruefbar (2) -
    nie 0. Liefert dict mit ausgang, im_abbild, dateien, gruende."""
    if schluessel not in abbild:
        return {"ausgang": NICHT_PRUEFBAR, "im_abbild": False, "dateien": [],
                "gruende": ["Gruppe nicht im Abbild gefuehrt - nicht pruefbar "
                            "(Abbild vor TB-97 erzeugt, oder Feld fehlt)"]}
    eintraege = abbild[schluessel]
    if not isinstance(eintraege, list):
        return {"ausgang": NICHT_PRUEFBAR, "im_abbild": True, "dateien": [],
                "gruende": ["Gruppe im Abbild keine Liste: %r" % (eintraege,)]}
    ausgang, dateien, gruende = OK, [], []
    for e in eintraege:
        rel = e.get("pfad") if isinstance(e, dict) else None
        soll = e.get("sha256") if isinstance(e, dict) else None
        if not rel or not soll:
            gruende.append("Eintrag ohne pfad oder sha256: %r" % (e,))
            ausgang = max(ausgang, NICHT_PRUEFBAR)
            continue
        voll = os.path.join(wurzel, rel)
        if not os.path.isfile(voll):
            dateien.append({"pfad": rel, "stand": "FEHLT", "sha256": None,
                            "grund": e.get("grund")})
            gruende.append("Datei fehlt: %s" % rel)
            ausgang = max(ausgang, NICHT_PRUEFBAR)
            continue
        try:
            ist = sha256_datei(voll)
        except OSError as fehler:
            dateien.append({"pfad": rel, "stand": "nicht lesbar", "sha256": None,
                            "grund": e.get("grund")})
            gruende.append("Datei nicht lesbar: %s (%s)" % (rel, fehler))
            ausgang = max(ausgang, NICHT_PRUEFBAR)
            continue
        if ist == soll:
            dateien.append({"pfad": rel, "stand": "gleich", "sha256": ist,
                            "grund": e.get("grund")})
        else:
            dateien.append({"pfad": rel, "stand": "ABWEICHUNG", "sha256": ist,
                            "grund": e.get("grund")})
            gruende.append("Hash weicht ab: %s soll %s… ist %s…"
                           % (rel, soll[:12], ist[:12]))
            ausgang = BEFUND
    return {"ausgang": ausgang, "im_abbild": True, "dateien": dateien,
            "gruende": gruende}


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
               "wurzel": wurzel, "punkte": [], "ii": {}, "gruppen": {},
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
            # Regel-Bestandteil: der Punkt nennt Nicht-Dateibezogenes oder
            # gar keinen Pfad (R6) - getrennt vom Pfad-Bestandteil (40.8 (d))
            "regel_bestandteil": bool(p["nicht_dateibezogen"] or not p["pfade"]),
            "tatsachennotiz": p.get("tatsachennotiz"),
            "dateien": [{"pfad": rel, "stand": stand, "sha256": h}
                        for rel, stand, h in dateien]})

    # (ii)
    ausgang_ii, befunde, notiz = _vergleiche_mit_register(abbild, register_pfad)
    bericht["ii"] = {"ausgang": ausgang_ii, "befunde": befunde, **notiz}

    # die zwei Gruppen neben den Punkten - aus dem Abbild (40.8 (e))
    for schluessel, _ in GRUPPEN:
        bericht["gruppen"][schluessel] = _pruefe_gruppe(abbild, schluessel, wurzel)
    bericht["bilanz"] = _bilanz(bericht)

    gruppen = bericht["gruppen"]
    ausgaenge = ([p["ausgang"] for p in bericht["punkte"]] + [ausgang_ii]
                 + [g["ausgang"] for g in gruppen.values()])

    def _gruppen_mit(wert):
        namen = [k for k, g in gruppen.items() if g["ausgang"] == wert]
        return (" und in Gruppe(n) %s" % namen) if namen else ""

    if BEFUND in ausgaenge:
        bericht["ausgang"] = BEFUND
        bericht["grund"] = ("BEFUND in Punkt(en) %s%s%s" % (
            [p["punkt"] for p in bericht["punkte"] if p["ausgang"] == BEFUND],
            " und in (ii) Abbild/Registertext" if ausgang_ii == BEFUND else "",
            _gruppen_mit(BEFUND)))
    elif NICHT_PRUEFBAR in ausgaenge:
        bericht["ausgang"] = NICHT_PRUEFBAR
        bericht["grund"] = ("NICHT PRUEFBAR: Punkt(e) %s%s%s" % (
            [p["punkt"] for p in bericht["punkte"] if p["ausgang"] == NICHT_PRUEFBAR],
            " und (ii) Registertext nicht lesbar" if ausgang_ii == NICHT_PRUEFBAR else "",
            _gruppen_mit(NICHT_PRUEFBAR)))
    else:
        bericht["ausgang"] = OK
        bericht["grund"] = "alle Punkte gemessen und gleich, Abbild = Registertext"
    return bericht


def _bilanz(b):
    """Die zwei Schlusszeilen als Zahlen (40.8 (d)): Pfad-Bestandteile je Datei
    ueber alle drei Gruppen, Regel-Bestandteile je Punkt. Aendert den
    Gesamtwert nicht - der bleibt, wie 36.5 ihn definiert."""
    stand_zu_wert = {"gleich": OK, "ABWEICHUNG": BEFUND}
    pfad = {OK: 0, BEFUND: 0, NICHT_PRUEFBAR: 0}
    je_gruppe = {"punkte": 0}
    for p in b["punkte"]:
        for d in p["dateien"]:
            pfad[stand_zu_wert.get(d["stand"], NICHT_PRUEFBAR)] += 1
            je_gruppe["punkte"] += 1
    fehlende = []
    for k, g in b["gruppen"].items():
        if not g["im_abbild"]:
            fehlende.append(k)
            continue
        je_gruppe[k] = len(g["dateien"])
        for d in g["dateien"]:
            pfad[stand_zu_wert.get(d["stand"], NICHT_PRUEFBAR)] += 1
    regel = [{"punkt": p["punkt"], "tatsachennotiz": p.get("tatsachennotiz")}
             for p in b["punkte"] if p.get("regel_bestandteil")]
    return {"pfad": {"geprueft": sum(pfad.values()), "0": pfad[OK],
                     "1": pfad[BEFUND], "2": pfad[NICHT_PRUEFBAR],
                     "je_gruppe": je_gruppe, "gruppen_nicht_im_abbild": fehlende},
            "regel": regel}


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
    for schluessel, name in GRUPPEN:
        g = b["gruppen"][schluessel]
        print("\nGruppe %s:  [%s]" % (name, _WORT[g["ausgang"]]))
        if g["im_abbild"] and not g["dateien"] and not g["gruende"]:
            print("  leer (im Abbild gefuehrt, kein Eintrag)")
        for d in g["dateien"]:
            print("  %-64s %-10s %s%s" % (d["pfad"], d["stand"], (d["sha256"] or "")[:16],
                                          ("  (%s)" % d["grund"]) if d.get("grund") else ""))
        for grund in g["gruende"]:
            print("  -> %s" % grund)

    # Die zwei Schlusszeilen (40.8 (d), Fable 24a): Pfad- und Regel-
    # Bestandteile getrennt, damit "kein Pfad-Bestandteil 1, jede 2 mit
    # Notiz" (22d) ablesbar ist, ohne zu rechnen.
    pf, rg = b["bilanz"]["pfad"], b["bilanz"]["regel"]
    teile = ", ".join("%s %d" % (k, n) for k, n in pf["je_gruppe"].items())
    if pf["gruppen_nicht_im_abbild"]:
        teile += "; nicht im Abbild (2): %s" % ", ".join(pf["gruppen_nicht_im_abbild"])
    print("\nPfad-Bestandteile: %d geprueft, davon %d mit 0 / %d mit 1 / %d mit 2  (%s)"
          % (pf["geprueft"], pf["0"], pf["1"], pf["2"], teile))
    print("Regel-Bestandteile: %d nicht pruefbar (2), je mit Verweis auf die Tatsachennotiz: %s"
          % (len(rg), "; ".join("Punkt %d -> %s" % (r["punkt"], r["tatsachennotiz"] or "keine im Abbild")
                                for r in rg) or "-"))
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
