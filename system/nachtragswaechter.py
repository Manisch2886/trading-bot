"""
Nachtragswaechter - die Bringschuld der Nachtraege (TB-64)
==============================================================================
Notizen an Backlog und Journal entstehen zuerst als eigene Datei unter
docs/projektfuehrung/nachtraege/ und werden IRGENDWANN eingearbeitet. Der
zweite Schritt kann ausfallen, ohne dass es jemand merkt: Nachtrag (m) vom
19.09.2026 wurde uebersprungen, seine Nummern wurden an andere Inhalte
vergeben, und aufgefallen ist es zwei Tage spaeter durch Zufall.

Dieses Skript ist rein lesend. Es meldet, es aendert nichts - weder eine
Nachtragsdatei noch eine Zieldatei (BACKLOG.md, die aus ihm ausgelagerten
Dateien, JOURNAL.md).

Der Zustand wird durch den Ort ausgedrueckt
------------------------------------------------------------------------------
Ein eingearbeiteter Nachtrag liegt unter nachtraege/_eingearbeitet/. Was im
Hauptverzeichnis liegt, ist offen. Der Ort allein genuegt nicht - jemand
koennte verschieben, ohne einzuarbeiten. Deshalb zwei Pruefungen:

  A  Was liegt offen?      Dateien im Hauptverzeichnis, mit Alter in Tagen.
                           Ein Nachtrag, der laenger als die Frist liegt,
                           ist ein Befund.
  B  Ist von den verschobenen wirklich alles angekommen?
                           Jede Datei in _eingearbeitet/ wird ueber ihre
                           Nummern gegen das Ziel geprueft. Eine Nummer, die
                           nicht angekommen ist, ist ein Befund
                           ("falsch verschoben").

Was als Nummer gilt (BACKLOG_NACHTRAG_*.md)
------------------------------------------------------------------------------
  K-Nummer       ^\| \*\*(K\d[a-z])\*\*
  Blockbezeichner  ^#{2,3} (2[a-z]+)\b  im Nachtrag, ^## (2[a-z]+)\b im Ziel
  Kettenzeile    ^\| (\*\*|~~)?(\d+,\d+[a-z]?)(\*\*|~~)?

Die Muster haben KEINEN schliessenden Balken. Im Backlog steht
`| **K2p** *(im Nachtrag (n) als `K2r` vorgeschlagen ...)* |`, und ein Muster
mit `\|` am Ende uebersieht jede Zeile mit Vergabevermerk - am 20.09.2026 hat
genau das eine Zaehlung von 64 auf 43 verfaelscht.

Wann eine Nummer als angekommen gilt
------------------------------------------------------------------------------
Dass die Nummer im Ziel STEHT, genuegt nicht: bei Nachtrag (m) standen alle
sechs Nummern im Backlog - mit fremdem Inhalt. Deshalb dreistufig:

  1. Zeile derselben Form mit derselben Nummer im Ziel, und ihr Text enthaelt
     den KERN des Nachtragstexts (die ersten 40 Zeichen nach der Nummernzelle,
     ohne Markdown-Auszeichnung und Whitespace)          -> angekommen
  2. sonst: der Kern steht in irgendeiner Zielzeile - die Nummer wurde bei der
     Einarbeitung geaendert (TB-59-Form)                 -> angekommen
  3. sonst: ein VERGABEVERMERK - eine Zielzeile, die die Nummer als Wort in
     Backticks (`K2r`) oder Anfuehrungszeichen nennt, dazu "vorgeschlagen"
     oder "vergeben", UND den Nachtrag selbst (sein Kuerzel "(m)" bzw. "(19m)"
     oder seinen Dateinamen)                             -> angekommen
  4. sonst                                               -> NICHT angekommen

Stufe 3 ist absichtlich an den Nachtrag gebunden: "Nummer `2s` im Nachtrag (s)
vorgeschlagen" ist ein Vermerk fuer (s), nicht fuer jeden Nachtrag, der einen
Block 2s vorschlaegt.

Das Ziel fuer Backlog-Nachtraege wird GELESEN, nicht aufgezaehlt (TB-76)
------------------------------------------------------------------------------
Bis zum 21.09.2026 stand das Ziel fest im Code: BACKLOG.md + BACKLOG_ARCHIV.md.
Am selben Tag hat TB-63 die Epics nach BACKLOG_EPICS.md ausgelagert, und der
Waechter meldete drei Nachtraege als "falsch verschoben", deren Inhalt laengst
angekommen war - nur eben in einer Datei, die er nicht kannte. Die naechste
Auslagerung haette dasselbe getan. Deshalb:

  Zieldatei ist BACKLOG.md selbst und jede Datei BACKLOG_<name>.md, die
  BACKLOG.md mit blossem Dateinamen nennt, die neben BACKLOG.md liegt und
  die keine Nachtragsdatei ist (kein "_NACHTRAG_" im Namen).

Begruendung: Wer etwas aus dem Backlog auslagert, laesst dort einen Verweis
auf die neue Datei zurueck (TB-60 und TB-63 haben das beide getan: Kopf und
Verweistabelle). Das Backlog ist damit das Verzeichnis seiner eigenen
Auslagerungen, und der Waechter liest es. Ein blosses Namensmuster
(BACKLOG*.md im Ordner) wuerde heute vier alte Nachtragsdateien im
Wurzelordner mit einsammeln - eine davon, BACKLOG_NACHTRAG_2026-09-18.md ohne
Buchstaben, erkennt RE_DATEINAME nicht -, und eine fremde Datei mit passendem
Namen wuerde still zum Ziel. Ueber die Nennung kann das nicht passieren.

Was der Weg kostet: Die naechste ausgelagerte Datei muss BACKLOG_<name>.md
heissen und in BACKLOG.md mit Namen stehen - beides tut eine Auslagerung nach
dem bisherigen Muster ohnehin. Fehlt die Nennung, meldet der Waechter die
verschobenen Nummern als nicht angekommen (rc 1) und zeigt damit auf den
fehlenden Verweis. Eine genannte Datei, die nicht existiert, ist ein
Werkzeugfehler (rc 2) wie ein fehlendes Journal - der Verweis zeigt ins Leere.
Genannt wird nur gelesen, was in BACKLOG.md steht, nicht, was die
ausgelagerten Dateien ihrerseits nennen.

Journal-Nachtraege (JOURNAL_NACHTRAG_*.md)
------------------------------------------------------------------------------
Kennung ist der Dateiname. Ein Journalblock, der aus einem Nachtrag entstanden
ist, nennt seine Quelldatei in einer Zeile der Form
    *Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_<datum><buchstabe>.md`*
Geprueft wird ueber den DATEINAMEN, nicht den Pfad - nach dem Verschieben
liegt die Datei unter _eingearbeitet/, die Quellenzeile nennt weiter den
Hauptordner. Zeilen `*Messprotokoll: ...*` zaehlen nicht als Quelle.

Nicht pruefbar (Pruefprinzip A2 - nicht gruen, nicht rot)
------------------------------------------------------------------------------
Ein Backlog-Nachtrag ohne eine einzige Nummer der drei Formen (die
Epic-Nachtraege (q) und (r) nennen nach Regel K2i bewusst keine) kann ueber
Nummern nicht geprueft werden. Er wird GETRENNT gemeldet - im Hauptverzeichnis
zaehlt er trotzdem als offen (Pruefung A), in _eingearbeitet/ ist er weder
Befund noch Bestaetigung.

Doppelbelegung
------------------------------------------------------------------------------
Eine Nummer, die im Ziel mehr als einmal vergeben ist, ist ein Befund. Gezaehlt
wird OHNE `sort -u` - `-u` entfernt genau die Duplikate, die gesucht werden;
dieser Fehler hat am 20.09.2026 "keine Doppelbelegung" gemeldet, es gab zwei.
Bei Kettenzeilen zaehlen Zeilen mit "alter Wortlaut" oder "Vermerk" in der
Nummernzelle nicht mit: nach DOKUMENTATIONSSTANDARD.md Regel 4 bleibt die
abgeloeste Fassung als gekennzeichnete Zeile darunter stehen. Journal-
Blockbuchstaben (`## BT — ...`) werden mitgezaehlt.

Rueckgabewert und Meldung
------------------------------------------------------------------------------
  0  kein Befund, keine Meldung
  1  Befund - offener Nachtrag ueber der Frist, falsch verschobene Datei oder
     Doppelbelegung
  2  Werkzeugfehler (Ziel- oder Nachtragsordner fehlt, oder BACKLOG.md nennt
     eine ausgelagerte Datei, die es neben ihr nicht gibt)

Die Meldung geht denselben Weg wie bei den vier anderen Cron-Waechtern:
notifications/waechter_melden.py fuehrt dieses Skript aus, reicht die Ausgabe
ins Log durch und schickt bei Rueckgabewert 1 die Zeilen "Zusammenfassung:"
und "BEFUND:" per Telegram. Diese beiden Zeilen nennen absichtlich KEIN
Alter in Tagen: der Wrapper daempft Wiederholungen ueber den Fingerabdruck
der gesendeten Zeilen, und ein Alter, das taeglich um eins waechst, wuerde
jeden Tag als "geaenderter Befund" gelten. Das Alter je Datei steht in den
Zeilen darueber, die vollstaendig im Log landen.

Nutzung:
    python3 system/nachtragswaechter.py                 # gegen das Repo
    python3 system/nachtragswaechter.py --frist-tage 2  # mildere Frist
    python3 system/nachtragswaechter.py --json PFAD     # Befund auch als JSON
    (Selbsttest: python3 system/test_nachtragswaechter.py)
"""

import argparse
import json
import os
import re
import sys
import time

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)
PROJEKTFUEHRUNG = os.path.join(BASE_DIR, "docs", "projektfuehrung")
STANDARD_NACHTRAEGE = os.path.join(PROJEKTFUEHRUNG, "nachtraege")
STANDARD_BACKLOG = os.path.join(PROJEKTFUEHRUNG, "BACKLOG.md")
STANDARD_JOURNAL = os.path.join(PROJEKTFUEHRUNG, "JOURNAL.md")
EINGEARBEITET = "_eingearbeitet"
FRIST_TAGE = 1.0
KERNLAENGE = 40

# Die Muster - alle OHNE schliessenden Balken (siehe Kopf).
RE_K = re.compile(r"^\| \*\*(K\d[a-z])\*\*")
RE_BLOCK_NACHTRAG = re.compile(r"^#{2,3} (2[a-z]+)\b")
RE_BLOCK_ZIEL = re.compile(r"^## (2[a-z]+)\b")
RE_KETTE = re.compile(r"^\| (?:\*\*|~~)?(\d+,\d+[a-z]?)(?:\*\*|~~)?")
RE_JOURNALBLOCK = re.compile(r"^## ([A-Z]{1,2}) — ")
RE_DATEINAME = re.compile(
    r"^(BACKLOG|JOURNAL)_NACHTRAG_(\d{4})-(\d{2})-(\d{2})([A-Za-z0-9_]+)\.md$")
# Eine in BACKLOG.md genannte Datei BACKLOG_<name>.md - blosser Dateiname, mit
# oder ohne Backticks, nicht als Teil eines Pfads oder eines laengeren Worts.
RE_ZIELNENNUNG = re.compile(r"(?<![\w/])(BACKLOG_[\w.-]+\.md)\b")
NACHTRAGSKENNUNG = "_NACHTRAG_"

ART_K, ART_BLOCK, ART_KETTE = "K", "Block", "Kette"
ZIELMUSTER = {ART_K: RE_K, ART_BLOCK: RE_BLOCK_ZIEL, ART_KETTE: RE_KETTE}
NACHTRAGSMUSTER = ((ART_K, RE_K), (ART_BLOCK, RE_BLOCK_NACHTRAG),
                   (ART_KETTE, RE_KETTE))

# Zustaende einer Nummer
ZEILE, ANDERSWO, VERMERK, FEHLT = "Zeile", "anderswo", "Vermerk", "FEHLT"

# Zustaende einer Datei
OFFEN_FRIST = "OFFEN UEBER DER FRIST"
OFFEN = "offen"
NICHT_PRUEFBAR = "NICHT PRUEFBAR"
FALSCH_VERSCHOBEN = "FALSCH VERSCHOBEN"
EINGEARBEITET_OK = "eingearbeitet"


# ---------------------------------------------------------------------------
# Lesen und Normieren
# ---------------------------------------------------------------------------
def lies_zeilen(pfad):
    with open(pfad, encoding="utf-8") as f:
        return f.read().splitlines()


def normiere(text):
    """Ohne Markdown-Auszeichnung, Whitespace auf ein Leerzeichen."""
    text = re.sub(r"[*_~`]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def inhalt_nach_nummer(zeile):
    """Der Text hinter der Nummernzelle einer Tabellenzeile bzw. hinter
    `X — ` einer Ueberschrift. Ein Vergabevermerk in der Nummernzelle
    (`| **K2p** *(...)* |`) wird dabei uebersprungen."""
    if zeile.startswith("|"):
        rest = zeile[1:]
        pos = rest.find(" | ")
        return rest[pos + 3:] if pos >= 0 else ""
    m = re.match(r"^#+ \S+\s*[—\-]\s*(.*)$", zeile)
    return m.group(1) if m else ""


def kern(zeile):
    """Die ersten KERNLAENGE Zeichen des normierten Inhalts, ohne Emoji und
    Pfeile am Anfang. Leer, wenn die Zeile ausser der Nummer nichts traegt."""
    text = normiere(inhalt_nach_nummer(zeile))
    text = re.sub(r"^[^\w(„\"]+", "", text)
    return text[:KERNLAENGE]


def nummernzelle(zeile):
    """Die erste Zelle einer Tabellenzeile, ohne die fuehrenden `| `."""
    return zeile[1:].split(" | ", 1)[0] if zeile.startswith("|") else ""


def kennungen(zeilen):
    """[(art, nummer, kern)] eines Backlog-Nachtrags, in Dateireihenfolge.
    Mehrfachnennungen bleiben - keine Vereinheitlichung."""
    gefunden = []
    for zeile in zeilen:
        for art, muster in NACHTRAGSMUSTER:
            m = muster.match(zeile)
            if m:
                gefunden.append((art, m.group(1), kern(zeile)))
                break
    return gefunden


def kuerzel(dateiname):
    """Die Kennzeichen, unter denen ein Vermerk den Nachtrag nennt:
    'BACKLOG_NACHTRAG_2026-09-19m.md' -> ('(m)', '(19m)', der Dateiname)."""
    m = RE_DATEINAME.match(dateiname)
    if not m:
        return (dateiname,)
    tag, rest = m.group(4), m.group(5)
    return (f"({rest})", f"({int(tag)}{rest})", f"({tag}{rest})", dateiname)


# ---------------------------------------------------------------------------
# Das Ziel
# ---------------------------------------------------------------------------
def zieldateien(backlog):
    """Die Zieldateien fuer Backlog-Nachtraege, aus BACKLOG.md GELESEN:
    BACKLOG.md selbst, dann jede dort genannte BACKLOG_<name>.md, die neben
    ihr liegt und keine Nachtragsdatei ist - alphabetisch, damit die Reihen-
    folge nicht von der Stelle der Nennung abhaengt.
    Rueckgabe (vorhanden, fehlend): fehlend sind genannte Dateien, die es
    neben BACKLOG.md nicht gibt - ein Werkzeugfehler fuer main()."""
    ordner = os.path.dirname(os.path.abspath(backlog))
    eigener_name = os.path.basename(backlog)
    genannt = set()
    for zeile in lies_zeilen(backlog):
        genannt.update(RE_ZIELNENNUNG.findall(zeile))
    genannt.discard(eigener_name)
    vorhanden, fehlend = [backlog], []
    for name in sorted(genannt):
        if NACHTRAGSKENNUNG in name:
            continue
        pfad = os.path.join(ordner, name)
        (vorhanden if os.path.isfile(pfad) else fehlend).append(pfad)
    return vorhanden, fehlend


class Ziel:
    """Die Zieldateien (Nummern; siehe zieldateien()) und JOURNAL.md (Quellen)."""

    def __init__(self, ziele, journal):
        self.backlog_zeilen = []
        self.umfang = {"ziel": {}}
        for pfad in ziele:
            zeilen = lies_zeilen(pfad)
            self.backlog_zeilen += zeilen
            self.umfang["ziel"][os.path.basename(pfad)] = len(zeilen)
        self.journal_zeilen = lies_zeilen(journal)
        self.umfang["journal"] = len(self.journal_zeilen)
        self.umfang["quellenzeilen"] = sum(1 for z in self.journal_zeilen
                                           if z.startswith("*Quelle:"))
        # Alle Nummern des Ziels je Art, als Liste - Duplikate bleiben.
        self.nummern = {art: [] for art in ZIELMUSTER}
        self.zeilen_je_nummer = {}
        for zeile in self.backlog_zeilen:
            for art, muster in ZIELMUSTER.items():
                m = muster.match(zeile)
                if m:
                    self.nummern[art].append(m.group(1))
                    self.zeilen_je_nummer.setdefault((art, m.group(1)), []).append(zeile)
        self.journalbloecke = [m.group(1) for m in
                               (RE_JOURNALBLOCK.match(z) for z in self.journal_zeilen) if m]

    def pruefe_nummer(self, art, nummer, kerntext, kennzeichen):
        """(zustand, beleg) fuer eine Nummer eines Nachtrags."""
        gleiche = self.zeilen_je_nummer.get((art, nummer), [])
        if kerntext and any(kerntext in normiere(z) for z in gleiche):
            return ZEILE, f"{len(gleiche)} Zielzeile(n) mit dieser Nummer, Kern bestaetigt"
        if kerntext:
            for zeile in self.backlog_zeilen:
                if kerntext in normiere(zeile):
                    return ANDERSWO, "Kern in: " + zeile[:80]
        vermerk = self.vergabevermerk(nummer, kennzeichen)
        if vermerk:
            return VERMERK, vermerk[:80]
        if gleiche:
            return FEHLT, (f"Nummer im Ziel {len(gleiche)}x vergeben, "
                           f"aber mit anderem Inhalt; Kern '{kerntext}' nirgends")
        if not kerntext:
            return FEHLT, "Nummer nicht im Ziel (Zeile traegt keinen Text)"
        return FEHLT, f"Nummer nicht im Ziel, Kern '{kerntext}' nirgends"

    def vergabevermerk(self, nummer, kennzeichen):
        """Eine Zielzeile, die die Nummer (`X` oder „X") zusammen mit
        'vorgeschlagen'/'vergeben' UND einem Kennzeichen des Nachtrags nennt.
        Kettennummern duerfen auch nackt stehen ("als 0,87 vergeben")."""
        formen = [f"`{nummer}`", f"„{nummer}\"", f"„{nummer}“"]
        nackt = re.compile(r"(?<![\w,])" + re.escape(nummer) + r"(?![\w,])") \
            if re.match(r"^\d+,\d+", nummer) else None
        for zeile in self.backlog_zeilen:
            if "vorgeschlagen" not in zeile and "vergeben" not in zeile:
                continue
            if not any(k in zeile for k in kennzeichen):
                continue
            if any(f in zeile for f in formen) or (nackt and nackt.search(zeile)):
                return zeile
        return None

    def quellenzeilen(self, dateiname):
        return [z for z in self.journal_zeilen
                if z.startswith("*Quelle:") and dateiname in z]

    def doppelbelegungen(self):
        """[(art, nummer, anzahl)] - ohne sort -u."""
        zaehler = {}
        for art, liste in self.nummern.items():
            for nummer in liste:
                if art == ART_KETTE:
                    zellen = [nummernzelle(z) for z in self.zeilen_je_nummer[(art, nummer)]]
                    zaehlend = [z for z in zellen
                                if "alter Wortlaut" not in z and "Vermerk" not in z]
                    zaehler[(art, nummer)] = len(zaehlend)
                else:
                    zaehler[(art, nummer)] = zaehler.get((art, nummer), 0) + 1
        for buchstabe in self.journalbloecke:
            zaehler[("Journalblock", buchstabe)] = \
                zaehler.get(("Journalblock", buchstabe), 0) + 1
        return sorted((a, n, c) for (a, n), c in zaehler.items() if c > 1)


# ---------------------------------------------------------------------------
# Die Nachtraege
# ---------------------------------------------------------------------------
def alter_in_tagen(pfad, jetzt=None):
    jetzt = time.time() if jetzt is None else jetzt
    return max(0.0, (jetzt - os.path.getmtime(pfad)) / 86400.0)


def pruefe_datei(pfad, ziel, jetzt=None):
    """Ein Befund je Datei: Art, Alter, Nummern mit Zustand, Zusammenfassung."""
    name = os.path.basename(pfad)
    befund = {"datei": name, "alter_tage": alter_in_tagen(pfad, jetzt),
              "art": None, "nummern": [], "nicht_angekommen": 0,
              "pruefbar": True, "hinweis": ""}
    m = RE_DATEINAME.match(name)
    if m and m.group(1) == "BACKLOG":
        befund["art"] = "Backlog"
        kennzeichen = kuerzel(name)
        for art, nummer, kerntext in kennungen(lies_zeilen(pfad)):
            zustand, beleg = ziel.pruefe_nummer(art, nummer, kerntext, kennzeichen)
            befund["nummern"].append({"art": art, "nummer": nummer,
                                      "zustand": zustand, "beleg": beleg})
        if not befund["nummern"]:
            befund["pruefbar"] = False
            befund["hinweis"] = "keine Nummer der drei Formen (K, Block, Kette)"
    elif m and m.group(1) == "JOURNAL":
        befund["art"] = "Journal"
        treffer = ziel.quellenzeilen(name)
        befund["nummern"].append({"art": "Quelle", "nummer": name,
                                  "zustand": ZEILE if treffer else FEHLT,
                                  "beleg": f"{len(treffer)} *Quelle:-Zeile(n) im Journal"})
    else:
        befund["art"] = "unbekannt"
        befund["pruefbar"] = False
        befund["hinweis"] = "Dateiname passt zu keiner der zwei Nachtragsarten"
    befund["nicht_angekommen"] = sum(1 for n in befund["nummern"] if n["zustand"] == FEHLT)
    return befund


def nachtragsdateien(ordner):
    return sorted(n for n in os.listdir(ordner)
                  if n.endswith(".md") and os.path.isfile(os.path.join(ordner, n)))


def pruefe_alles(nachtraege, ziel, frist_tage=FRIST_TAGE, jetzt=None):
    """Der ganze Lauf als Datenstruktur; berichte() macht Text daraus."""
    eingearbeitet = os.path.join(nachtraege, EINGEARBEITET)
    offen, verschoben = [], []
    for name in nachtragsdateien(nachtraege):
        b = pruefe_datei(os.path.join(nachtraege, name), ziel, jetzt)
        b["zustand"] = OFFEN_FRIST if b["alter_tage"] >= frist_tage else OFFEN
        offen.append(b)
    if os.path.isdir(eingearbeitet):
        for name in nachtragsdateien(eingearbeitet):
            b = pruefe_datei(os.path.join(eingearbeitet, name), ziel, jetzt)
            if not b["pruefbar"]:
                b["zustand"] = NICHT_PRUEFBAR
            elif b["nicht_angekommen"]:
                b["zustand"] = FALSCH_VERSCHOBEN
            else:
                b["zustand"] = EINGEARBEITET_OK
            verschoben.append(b)
    return {"frist_tage": frist_tage, "umfang": ziel.umfang,
            "offen": offen, "eingearbeitet": verschoben,
            "doppelbelegungen": ziel.doppelbelegungen()}


# ---------------------------------------------------------------------------
# Bericht
# ---------------------------------------------------------------------------
def _dateizeile(b):
    if b["art"] == "Journal":
        stand = ("Quellenzeile im Journal" if b["nicht_angekommen"] == 0
                 else "Quellenzeile FEHLT im Journal")
    elif not b["pruefbar"]:
        stand = f"nicht pruefbar - {b['hinweis']}"
    else:
        stand = (f"Nummern {len(b['nummern'])}, nicht angekommen "
                 f"{b['nicht_angekommen']}")
    return f"{b['datei']:48} Alter {b['alter_tage']:5.1f} d   {stand}"


def berichte(ergebnis, ausfuehrlich=True):
    offen, verschoben = ergebnis["offen"], ergebnis["eingearbeitet"]
    u = ergebnis["umfang"]
    print("=" * 78)
    print("NACHTRAGSWAECHTER - die Bringschuld der Nachtraege")
    print("=" * 78)
    ziele = ", ".join(f"{name} {n}" for name, n in u["ziel"].items())
    print(f"Ziel (aus BACKLOG.md gelesen): {ziele} Zeilen; "
          f"JOURNAL.md {u['journal']} ({u['quellenzeilen']} Quellenzeilen)")
    print(f"Frist: {ergebnis['frist_tage']:g} Tag(e), Alter aus der Aenderungszeit der Datei")

    print(f"\nA - OFFEN im Hauptverzeichnis: {len(offen)} Datei(en)")
    for b in offen:
        marke = {OFFEN_FRIST: "[!] ", OFFEN: "    "}[b["zustand"]]
        if not b["pruefbar"]:
            marke = "[?] "
        rat = ""
        if b["zustand"] == OFFEN_FRIST and b["pruefbar"]:
            rat = ("  -> alles angekommen: nach _eingearbeitet/ verschieben"
                   if b["nicht_angekommen"] == 0 else "  -> einarbeiten")
        print(f"  {marke}{_dateizeile(b)}{rat}")
        if ausfuehrlich:
            for n in b["nummern"]:
                if n["zustand"] != ZEILE:
                    print(f"          {n['art']:5} {n['nummer']:8} {n['zustand']:8} {n['beleg']}")

    print(f"\nB - EINGEARBEITET ({EINGEARBEITET}/): {len(verschoben)} Datei(en)")
    for b in verschoben:
        marke = {FALSCH_VERSCHOBEN: "[!!]", NICHT_PRUEFBAR: "[?] ",
                 EINGEARBEITET_OK: "OK  "}[b["zustand"]]
        print(f"  {marke}{_dateizeile(b)}")
        if ausfuehrlich:
            for n in b["nummern"]:
                if n["zustand"] == FEHLT:
                    print(f"          {n['art']:5} {n['nummer']:8} {n['zustand']:8} {n['beleg']}")

    doppelt = ergebnis["doppelbelegungen"]
    print(f"\nC - DOPPELBELEGUNG im Ziel (ohne sort -u): "
          f"{len(doppelt) if doppelt else 'keine'}")
    for art, nummer, anzahl in doppelt:
        print(f"  [!!] {art} {nummer}: {anzahl}x")


def zusammenfassung(ergebnis):
    """Die zwei Zeilen, die per Telegram gehen - ohne Alter, damit der
    Fingerabdruck von Tag zu Tag stabil bleibt."""
    offen, verschoben = ergebnis["offen"], ergebnis["eingearbeitet"]
    ueber = [b for b in offen if b["zustand"] == OFFEN_FRIST]
    in_frist = [b for b in offen if b["zustand"] == OFFEN]
    unpruefbar = [b for b in offen + verschoben if not b["pruefbar"]]
    falsch = [b for b in verschoben if b["zustand"] == FALSCH_VERSCHOBEN]
    doppelt = ergebnis["doppelbelegungen"]

    teile = [f"{len(ueber)}x OFFEN UEBER DER FRIST", f"{len(in_frist)}x offen in der Frist",
             f"{len(unpruefbar)}x NICHT PRUEFBAR", f"{len(falsch)}x FALSCH VERSCHOBEN",
             f"{len(doppelt)}x DOPPELBELEGUNG"]
    zeile1 = "Zusammenfassung: " + ", ".join(teile)

    befunde = []
    if ueber:
        befunde.append(f"{len(ueber)} Nachtrag/Nachtraege ueber der Frist offen "
                       f"({_namen(ueber)})")
    if falsch:
        befunde.append(f"{len(falsch)} falsch verschoben ({_namen(falsch)})")
    if doppelt:
        befunde.append("Doppelbelegung " + ", ".join(f"{a} {n} {c}x" for a, n, c in doppelt))
    zeile2 = ("BEFUND: " + "; ".join(befunde) + ".") if befunde else ""
    return zeile1, zeile2, bool(befunde)


def _namen(befunde, hoechstens=3):
    namen = [_kurzname(b["datei"]) for b in befunde]
    if len(namen) > hoechstens:
        return ", ".join(namen[:hoechstens]) + f" +{len(namen) - hoechstens} weitere"
    return ", ".join(namen)


def _kurzname(dateiname):
    m = RE_DATEINAME.match(dateiname)
    if not m:
        return dateiname
    return f"{m.group(1)[0]}-{m.group(3)}-{m.group(4)}{m.group(5)}"


# ---------------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Prueft, welche Nachtraege offen sind und ob verschobene "
                    "wirklich eingearbeitet wurden. Rein lesend.")
    parser.add_argument("--nachtraege", default=STANDARD_NACHTRAEGE,
                        help="Ordner der Nachtraege (mit Unterordner _eingearbeitet/)")
    parser.add_argument("--backlog", default=STANDARD_BACKLOG,
                        help="BACKLOG.md; die weiteren Zieldateien werden daraus gelesen")
    parser.add_argument("--journal", default=STANDARD_JOURNAL)
    parser.add_argument("--frist-tage", type=float, default=FRIST_TAGE,
                        help=f"ab diesem Alter ist ein offener Nachtrag ein Befund "
                             f"(Standard {FRIST_TAGE:g})")
    parser.add_argument("--json", metavar="PFAD", default=None,
                        help="das Ergebnis zusaetzlich als JSON ablegen")
    parser.add_argument("--knapp", action="store_true",
                        help="ohne die Einzelzeilen je Nummer")
    args = parser.parse_args(argv)

    fehlend = [p for p in (args.nachtraege, args.backlog, args.journal)
               if not os.path.exists(p)]
    if fehlend:
        print("Fehlt: " + ", ".join(fehlend), file=sys.stderr)
        return 2
    ziele, fehlend = zieldateien(args.backlog)
    if fehlend:
        print("In BACKLOG.md genannt, aber nicht vorhanden: " + ", ".join(fehlend),
              file=sys.stderr)
        return 2

    start = time.time()
    ziel = Ziel(ziele, args.journal)
    ergebnis = pruefe_alles(args.nachtraege, ziel, args.frist_tage)
    berichte(ergebnis, ausfuehrlich=not args.knapp)
    zeile1, zeile2, befund = zusammenfassung(ergebnis)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(ergebnis, f, indent=2, ensure_ascii=False)
        print(f"\nErgebnis als JSON: {args.json}")

    print(f"\nLaufzeit: {time.time() - start:.2f}s")
    print("\n" + "=" * 78)
    print(zeile1)
    if befund:
        print(zeile2)
        print("Nachsehen: python3 system/nachtragswaechter.py")
        return 1
    print("Kein Befund: nichts liegt ueber der Frist, nichts ist falsch verschoben, "
          "keine Nummer doppelt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
