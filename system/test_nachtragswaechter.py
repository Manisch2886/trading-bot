"""
Selbsttests des Nachtragswaechters (TB-64)
==============================================================================
Pruefprinzip B1 und K3g: jede Probe wird an einem bekannt kaputten Gegenstand
validiert, bevor sie an einen echten darf. Ein Waechter, der nichts findet,
weil er nicht hinsehen kann, ist schlimmer als keiner.

Jeder Fall baut in einem WEGWERF-VERZEICHNIS (tempfile.mkdtemp, also unter
$TMPDIR - nie unter docs/) einen kleinen Nachtragsordner samt BACKLOG.md,
BACKLOG_ARCHIV.md (im Kopf von BACKLOG.md genannt, wie im echten Bestand) und
JOURNAL.md, laesst den Waechter darueber laufen und prueft Rueckgabewert und
Meldung. Das Verzeichnis wird am Ende entfernt; der
letzte Test prueft, dass nichts uebrigblieb.

Die sieben Faelle aus dem Auftrag (Abschnitt 3):
  1  Nachtrag mit einer Nummer, die im Ziel steht          -> kein Befund
  2  Nachtrag mit einer Nummer, die NICHT im Ziel steht    -> Befund, rc 1
  3  Nummer im Ziel nur als Vergabevermerk                 -> kein Befund
  4  Zielzeile MIT Vergabevermerk in der Nummernzelle      -> kein Befund
     (der Fall, an dem das Muster mit schliessendem Balken am 20.09.
      gescheitert ist)
  5  zwei gleiche Nummern im Ziel                          -> Doppelbelegung
     (der Fall, den `sort -u` verschluckt hat)
  6  Journal-Nachtrag ohne Quellenvermerk im Journal       -> Befund
  7  Datei in _eingearbeitet/, deren Nummern nicht im Ziel -> Befund
     (Pruefung B, die Wache gegen falsches Verschieben)
Dazu:
  8  Nummer im Ziel, aber mit FREMDEM Inhalt (der Fall (m)) -> Befund
  9  frischer offener Nachtrag innerhalb der Frist        -> kein Befund
 10  Quellenzeile ueber den Dateinamen, *Messprotokoll: zaehlt nicht
 11  Rueckgabewert im echten Unterprozess (rc 1 erreicht die Shell)
 12  Werkzeugfehler (Ziel fehlt) -> rc 2, nicht 1
Die Zielmenge wird gelesen, nicht aufgezaehlt (TB-76, Abschnitt 3 des Auftrags):
 13  Inhalt in einer ausgelagerten Datei angekommen, die BACKLOG.md nennt
                                                          -> kein Befund
 14  Inhalt NIRGENDS angekommen, auch nicht in der ausgelagerten -> Befund
 15  eine WEITERE ausgelagerte Datei kommt dazu, deren Name im Waechter
     nicht vorkommt                                       -> kein Befund
     dazu: nicht genannte Datei ist kein Ziel; genannter Nachtrag ist kein
     Ziel; genannte, aber fehlende Datei -> rc 2

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:  python3 system/test_nachtragswaechter.py
"""

import io
import os
import shutil
import subprocess
import sys
import tempfile
import time
from contextlib import redirect_stderr, redirect_stdout

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import nachtragswaechter as nw                                # noqa: E402

BESTANDEN = 0
FEHLER = []
ANGELEGT = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        FEHLER.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


# ---------------------------------------------------------------------------
ZIEL_GRUND = """# Backlog

> Rückblicke stehen in `BACKLOG_ARCHIV.md` (angelegt 20.09.2026, TB-60).

## 4 — Laufend, klein

| # | Punkt |
|---|---|
| **K9a** | ⭐ **Die erste Regel im Ziel** — sie steht hier seit Tagen |
| **K9b** *(im Nachtrag (x) als `K9z` vorgeschlagen; `K9z` war nicht die naechste freie — vergeben als `K9b`, gemessen)* | ⚠️ **Die zweite Regel, mit Vergabevermerk in der Nummernzelle** |
"""

JOURNAL_GRUND = """# Journal

## AA — Ein alter Block

*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-01a.md`*

Text.

## AB — Ein Block mit Messprotokoll

*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-01b.md`*

*Messprotokoll: `docs/projektfuehrung/nachtraege/BACKLOG_NACHTRAG_2026-09-01m.md`, Block `2s`*

## Wiederkehrende Lehren
"""


class Wegwerf:
    """Ein Nachtragsordner samt Zielen unter $TMPDIR. Die Tests fassen das
    echte docs/ nie an."""

    def __enter__(self):
        self.wurzel = tempfile.mkdtemp(prefix="nachtragswaechter_")
        ANGELEGT.append(self.wurzel)
        self.nachtraege = os.path.join(self.wurzel, "nachtraege")
        self.eingearbeitet = os.path.join(self.nachtraege, nw.EINGEARBEITET)
        os.makedirs(self.eingearbeitet)
        self.backlog = os.path.join(self.wurzel, "BACKLOG.md")
        self.archiv = os.path.join(self.wurzel, "BACKLOG_ARCHIV.md")
        self.journal = os.path.join(self.wurzel, "JOURNAL.md")
        self.schreibe(self.backlog, ZIEL_GRUND)
        self.schreibe(self.archiv, "# Archiv\n")
        self.schreibe(self.journal, JOURNAL_GRUND)
        return self

    def __exit__(self, *_):
        shutil.rmtree(self.wurzel, ignore_errors=True)

    @staticmethod
    def schreibe(pfad, text, alter_tage=None):
        with open(pfad, "w", encoding="utf-8") as f:
            f.write(text)
        if alter_tage is not None:
            t = time.time() - alter_tage * 86400
            os.utime(pfad, (t, t))

    def nachtrag(self, name, text, alter_tage=3, verschoben=False):
        ordner = self.eingearbeitet if verschoben else self.nachtraege
        pfad = os.path.join(ordner, name)
        self.schreibe(pfad, text, alter_tage)
        return pfad

    def ziel_anhaengen(self, text):
        with open(self.backlog, "a", encoding="utf-8") as f:
            f.write(text)

    def ziel(self):
        """Das Ziel, wie main() es baut: aus BACKLOG.md gelesen."""
        return nw.Ziel(nw.zieldateien(self.backlog)[0], self.journal)

    def lauf(self, *extra):
        """(rc, ausgabe) des Waechters im Prozess."""
        puffer = io.StringIO()
        argv = ["--nachtraege", self.nachtraege, "--backlog", self.backlog,
                "--journal", self.journal] + list(extra)
        with redirect_stdout(puffer):
            rc = nw.main(argv)
        return rc, puffer.getvalue()


def _befundzeile(ausgabe):
    return next((z for z in ausgabe.splitlines() if z.startswith("BEFUND:")), "")


# ---------------------------------------------------------------------------
def test_fall_1_nummer_im_ziel():
    print("\nFall 1 - Nachtrag mit einer Nummer, die im Ziel steht -> kein Befund")
    with Wegwerf() as w:
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01y.md",
                   "# Nachtrag (y)\n\n| # | Punkt |\n|---|---|\n"
                   "| **K9a** | ⭐ **Die erste Regel im Ziel** — sie steht hier seit Tagen |\n",
                   verschoben=True)
        rc, aus = w.lauf()
        check("rc 0", rc == 0, f"rc={rc}")
        check("keine BEFUND-Zeile", "BEFUND:" not in aus)
        check("Datei als eingearbeitet gefuehrt",
              "OK  BACKLOG_NACHTRAG_2026-09-01y.md" in aus)
        check("Zusammenfassung ohne Befundzahlen",
              "0x FALSCH VERSCHOBEN" in aus and "0x DOPPELBELEGUNG" in aus)


def test_fall_2_nummer_nicht_im_ziel():
    print("\nFall 2 - Nachtrag mit einer Nummer, die NICHT im Ziel steht -> Befund, rc 1")
    with Wegwerf() as w:
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01y.md",
                   "# Nachtrag (y)\n\n| # | Punkt |\n|---|---|\n"
                   "| **K9c** | ⭐ **Eine Regel, die nie angekommen ist** |\n",
                   alter_tage=3)
        rc, aus = w.lauf()
        check("rc 1", rc == 1, f"rc={rc}")
        check("BEFUND nennt den Nachtrag", "B-09-01y" in _befundzeile(aus), _befundzeile(aus))
        check("Zeile nennt Alter in Tagen und nicht angekommene Nummern",
              "Alter   3.0 d" in aus and "nicht angekommen 1" in aus)
        check("die Nummer steht als FEHLT", "K9c      FEHLT" in aus)
        check("Rat lautet: einarbeiten", "-> einarbeiten" in aus)


def test_fall_3_nur_vergabevermerk():
    print("\nFall 3 - Nummer im Ziel nur als Vergabevermerk -> kein Befund")
    with Wegwerf() as w:
        # Der Nachtrag (x) schlug K9z vor; im Ziel steht nur der Vermerk an K9b,
        # und K9b traegt einen ANDEREN Kern als der Nachtrag.
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01x.md",
                   "# Nachtrag (x)\n\n| # | Punkt |\n|---|---|\n"
                   "| **K9z** | Ein Text, der so im Ziel nicht steht |\n",
                   verschoben=True)
        rc, aus = w.lauf()
        check("rc 0", rc == 0, f"rc={rc}")
        check("Nummer ueber den Vermerk angekommen", "K9z      Vermerk" in aus or "FEHLT" not in aus)
        check("kein FEHLT", "FEHLT" not in aus)

        # Gegenprobe: derselbe Vermerk, aber fuer einen ANDEREN Nachtrag (w)
        # ist er keiner - die Bindung an den Nachtrag muss greifen.
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01w.md",
                   "# Nachtrag (w)\n\n| # | Punkt |\n|---|---|\n"
                   "| **K9z** | Ein anderer Text, der so im Ziel nicht steht |\n",
                   verschoben=True)
        rc, aus = w.lauf()
        check("Gegenprobe: Vermerk fuer (x) gilt nicht fuer (w) -> rc 1", rc == 1, f"rc={rc}")
        check("Gegenprobe: (w) falsch verschoben",
              "[!!]BACKLOG_NACHTRAG_2026-09-01w.md" in aus)


def test_fall_4_zielzeile_mit_vermerk():
    print("\nFall 4 - Zielzeile MIT Vergabevermerk in der Nummernzelle -> kein Befund")
    with Wegwerf() as w:
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01y.md",
                   "# Nachtrag (y)\n\n| # | Punkt |\n|---|---|\n"
                   "| **K9b** | ⚠️ **Die zweite Regel, mit Vergabevermerk in der Nummernzelle** |\n",
                   verschoben=True)
        rc, aus = w.lauf()
        check("rc 0", rc == 0, f"rc={rc}")
        check("kein FEHLT", "FEHLT" not in aus)
        # Mutationsprobe: ein Muster MIT schliessendem Balken uebersieht die Zeile.
        import re
        mit_balken = re.compile(r"^\| \*\*(K\d[a-z])\*\* \|")
        zeilen = nw.lies_zeilen(w.backlog)
        check("Mutationsprobe: das Muster mit `\\|` am Ende uebersieht K9b",
              not any(mit_balken.match(z) and "K9b" in z for z in zeilen)
              and any(nw.RE_K.match(z) and "K9b" in z for z in zeilen))
        check("das Waechter-Muster endet nicht mit einem Balken",
              not nw.RE_K.pattern.endswith("\\|"), nw.RE_K.pattern)
        ziel = w.ziel()
        zeile = "| **K9b** | ⚠️ **Die zweite Regel, mit Vergabevermerk in der Nummernzelle** |"
        check("K9b ist als ZIELZEILE gefunden, nicht erst ueber den Kern anderswo",
              ziel.pruefe_nummer(nw.ART_K, "K9b", nw.kern(zeile), ("(y)",))[0] == nw.ZEILE
              and "K9b" in ziel.nummern[nw.ART_K])


def test_fall_5_doppelbelegung():
    print("\nFall 5 - zwei gleiche Nummern im Ziel -> Befund Doppelbelegung")
    with Wegwerf() as w:
        w.ziel_anhaengen("| **K9a** | *(unveraendert)* dieselbe Nummer ein zweites Mal |\n")
        rc, aus = w.lauf()
        check("rc 1", rc == 1, f"rc={rc}")
        check("BEFUND nennt Doppelbelegung K K9a 2x", "Doppelbelegung K K9a 2x" in _befundzeile(aus),
              _befundzeile(aus))
        check("Abschnitt C zaehlt 1", "DOPPELBELEGUNG im Ziel (ohne sort -u): 1" in aus)
        # Mutationsprobe: `sort -u` haette die Doppelung entfernt.
        nummern = w.ziel().nummern[nw.ART_K]
        check("Mutationsprobe: die Liste traegt K9a zweimal, die Menge einmal",
              nummern.count("K9a") == 2 and len(set(nummern)) == len(nummern) - 1)

        # Kettenzeilen: die abgeloeste Fassung mit 'alter Wortlaut' zaehlt NICHT.
        w.ziel_anhaengen("| **0,90** | **Ein Schritt** | offen |\n"
                         "| **0,90** *(alter Wortlaut — ersetzt 19.09.2026)* | **Ein Schritt** | offen |\n")
        rc, aus = w.lauf()
        check("Kette mit 'alter Wortlaut' ist keine Doppelbelegung",
              "Kette 0,90" not in aus)
        w.ziel_anhaengen("| **0,90** | **Ein zweiter Schritt unter derselben Nummer** | offen |\n")
        rc, aus = w.lauf()
        check("zwei zaehlende Kettenzeilen 0,90 sind eine Doppelbelegung",
              "Kette 0,90: 2x" in aus)

        # Journal-Blockbuchstaben doppelt.
        with open(w.journal, "a", encoding="utf-8") as f:
            f.write("\n## AB — noch einmal AB\n")
        rc, aus = w.lauf()
        check("doppelter Journalblock AB gemeldet", "Journalblock AB: 2x" in aus)


def test_fall_6_journal_ohne_quelle():
    print("\nFall 6 - Journal-Nachtrag ohne Quellenvermerk im Journal -> Befund")
    with Wegwerf() as w:
        w.nachtrag("JOURNAL_NACHTRAG_2026-09-01c.md", "# Journal-Nachtrag (c)\n\nText.\n",
                   verschoben=True)
        rc, aus = w.lauf()
        check("rc 1", rc == 1, f"rc={rc}")
        check("falsch verschoben gemeldet", "[!!]JOURNAL_NACHTRAG_2026-09-01c.md" in aus)
        check("Grund: Quellenzeile fehlt", "Quellenzeile FEHLT im Journal" in aus)
        # Offen und ueber der Frist: ebenfalls Befund, anders begruendet.
        os.remove(os.path.join(w.eingearbeitet, "JOURNAL_NACHTRAG_2026-09-01c.md"))
        w.nachtrag("JOURNAL_NACHTRAG_2026-09-01c.md", "# Journal-Nachtrag (c)\n", alter_tage=2)
        rc, aus = w.lauf()
        check("offen ueber der Frist: rc 1", rc == 1, f"rc={rc}")
        check("BEFUND nennt J-09-01c", "J-09-01c" in _befundzeile(aus))


def test_fall_7_falsch_verschoben():
    print("\nFall 7 - Datei in _eingearbeitet/, deren Nummern nicht im Ziel stehen -> Befund")
    with Wegwerf() as w:
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01y.md",
                   "# Nachtrag (y)\n\n### 2q — Ein Block, der nie ankam\n\n| # | Punkt |\n|---|---|\n"
                   "| **K9c** | ⭐ **Eine Regel, die nie angekommen ist** |\n"
                   "| **K9a** | ⭐ **Die erste Regel im Ziel** — sie steht hier seit Tagen |\n",
                   verschoben=True)
        rc, aus = w.lauf()
        check("rc 1", rc == 1, f"rc={rc}")
        check("FALSCH VERSCHOBEN in der Zusammenfassung", "1x FALSCH VERSCHOBEN" in aus)
        check("BEFUND nennt die Datei", "falsch verschoben (B-09-01y)" in _befundzeile(aus))
        check("Nummern 3, nicht angekommen 2", "Nummern 3, nicht angekommen 2" in aus)
        check("Block 2q als FEHLT", "Block 2q       FEHLT" in aus)


def test_fall_8_nummer_mit_fremdem_inhalt():
    print("\nFall 8 - Nummer im Ziel, aber mit fremdem Inhalt (der Fall (m)) -> Befund")
    with Wegwerf() as w:
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01m.md",
                   "# Nachtrag (m)\n\n| # | Punkt |\n|---|---|\n"
                   "| **K9a** | ⭐ **Jede Rueckfrage an den Betreiber kommt woertlich in den Bericht** |\n",
                   verschoben=True)
        rc, aus = w.lauf()
        check("rc 1 - die Nummer steht im Ziel, der Inhalt nicht", rc == 1, f"rc={rc}")
        check("Beleg nennt den fremden Inhalt",
              "Nummer im Ziel 1x vergeben, aber mit anderem Inhalt" in aus)
        # Mutationsprobe: ohne Kernpruefung waere die Nummer 'angekommen'.
        ziel = w.ziel()
        check("Mutationsprobe: ohne Kern meldet die Nummernpruefung Zeile",
              ziel.pruefe_nummer(nw.ART_K, "K9a", "", ("(m)",))[0] == nw.FEHLT
              and "K9a" in ziel.nummern[nw.ART_K])
        # Ein Abschlussvermerk, der (m) und die Nummer nennt, heilt es.
        w.ziel_anhaengen("| **K9d** | ⭐ **NACHTRAG (m) GEPRUEFT UND ABGESCHLOSSEN** — seine Nummer `K9a` war an (y) vergeben und bleibt dort |\n")
        rc, aus = w.lauf()
        check("mit Vermerk, der (m) und `K9a` nennt: rc 0", rc == 0, f"rc={rc}")
        # Derselbe Vermerk mit (y) statt (m) heilt NICHT.
        with open(w.backlog, encoding="utf-8") as f:
            text = f.read().replace("NACHTRAG (m) GEPRUEFT", "NACHTRAG (y) GEPRUEFT")
        w.schreibe(w.backlog, text)
        rc, aus = w.lauf()
        check("Vermerk fuer (y) heilt (m) nicht: rc 1", rc == 1, f"rc={rc}")


def test_fall_9_frist():
    print("\nFall 9 - frischer offener Nachtrag innerhalb der Frist -> kein Befund")
    with Wegwerf() as w:
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01y.md",
                   "# Nachtrag (y)\n\n| # | Punkt |\n|---|---|\n"
                   "| **K9c** | ⭐ **Eine Regel, die noch nicht angekommen ist** |\n",
                   alter_tage=0.2)
        rc, aus = w.lauf()
        check("rc 0 (0,2 Tage < Frist 1)", rc == 0, f"rc={rc}")
        check("als offen in der Frist gezaehlt", "1x offen in der Frist" in aus)
        rc, aus = w.lauf("--frist-tage", "0.1")
        check("mit --frist-tage 0.1: rc 1", rc == 1, f"rc={rc}")
        # Alles angekommen, aber liegengelassen: ueber der Frist ein Befund mit Rat.
        os.remove(os.path.join(w.nachtraege, "BACKLOG_NACHTRAG_2026-09-01y.md"))
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01y.md",
                   "# Nachtrag (y)\n\n| # | Punkt |\n|---|---|\n"
                   "| **K9a** | ⭐ **Die erste Regel im Ziel** — sie steht hier seit Tagen |\n",
                   alter_tage=4)
        rc, aus = w.lauf()
        check("angekommen, aber offen ueber der Frist: rc 1", rc == 1, f"rc={rc}")
        check("Rat: verschieben", "nach _eingearbeitet/ verschieben" in aus)
        # Nicht pruefbar: offen, ueber der Frist -> Befund als offen, [?] markiert.
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01z.md", "# Nachtrag (z)\n\nnur Prosa\n", alter_tage=4)
        rc, aus = w.lauf()
        check("nicht pruefbar getrennt gemeldet", "[?] BACKLOG_NACHTRAG_2026-09-01z.md" in aus
              and "1x NICHT PRUEFBAR" in aus)
        check("Zusammenfassung und BEFUND nennen kein Alter",
              " d " not in _befundzeile(aus) and "Alter" not in _befundzeile(aus))


def test_fall_10_quelle_ueber_dateinamen():
    print("\nFall 10 - Quellenzeile ueber den Dateinamen; *Messprotokoll: zaehlt nicht")
    with Wegwerf() as w:
        w.nachtrag("JOURNAL_NACHTRAG_2026-09-01a.md", "# (a)\n", verschoben=True)
        w.nachtrag("JOURNAL_NACHTRAG_2026-09-01b.md", "# (b)\n", verschoben=True)
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01m.md", "# (m)\n\nnur Prosa\n", verschoben=True)
        rc, aus = w.lauf()
        check("rc 0", rc == 0, f"rc={rc}")
        check("(a) und (b) ueber den Dateinamen gefunden, obwohl die Quellenzeile "
              "den Hauptordner nennt",
              "OK  JOURNAL_NACHTRAG_2026-09-01a.md" in aus and "OK  JOURNAL_NACHTRAG_2026-09-01b.md" in aus)
        ziel = w.ziel()
        check("*Messprotokoll: ist keine Quelle fuer (m)",
              ziel.quellenzeilen("BACKLOG_NACHTRAG_2026-09-01m.md") == [])
        check("(m) ohne Nummer in _eingearbeitet/: nicht pruefbar, kein Befund",
              "[?] BACKLOG_NACHTRAG_2026-09-01m.md" in aus and rc == 0)


def test_fall_11_unterprozess():
    print("\nFall 11 - Rueckgabewert im echten Unterprozess")
    with Wegwerf() as w:
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01y.md",
                   "# (y)\n\n| # | Punkt |\n|---|---|\n| **K9c** | nie angekommen |\n", alter_tage=3)
        cmd = [sys.executable, os.path.join(_DIR, "nachtragswaechter.py"),
               "--nachtraege", w.nachtraege, "--backlog", w.backlog,
               "--journal", w.journal]
        p = subprocess.run(cmd, capture_output=True, text=True)
        check("rc 1 im Unterprozess", p.returncode == 1, f"rc={p.returncode}")
        check("BEFUND auf stdout", "BEFUND:" in p.stdout)
        check("stderr leer", p.stderr.strip() == "", p.stderr[:120])
        check("Marken fuer waechter_melden vorhanden",
              "Zusammenfassung:" in p.stdout and "BEFUND:" in p.stdout)
        # Ohne Befund: rc 0 und keine BEFUND-Zeile.
        os.remove(os.path.join(w.nachtraege, "BACKLOG_NACHTRAG_2026-09-01y.md"))
        p = subprocess.run(cmd, capture_output=True, text=True)
        check("rc 0 im Unterprozess ohne Befund", p.returncode == 0, f"rc={p.returncode}")
        check("keine BEFUND-Zeile ohne Befund", "BEFUND:" not in p.stdout)


def test_fall_12_werkzeugfehler():
    print("\nFall 12 - Werkzeugfehler: fehlendes Ziel -> rc 2, nicht 1")
    with Wegwerf() as w:
        os.remove(w.journal)
        puffer, fehler = io.StringIO(), io.StringIO()
        with redirect_stdout(puffer), redirect_stderr(fehler):
            rc = nw.main(["--nachtraege", w.nachtraege, "--backlog", w.backlog,
                          "--journal", w.journal])
        check("rc 2", rc == 2, f"rc={rc}")
        check("Fehlermeldung nennt die fehlende Datei auf stderr",
              "JOURNAL.md" in fehler.getvalue())


# ---------------------------------------------------------------------------
# TB-76: die Zielmenge wird aus BACKLOG.md gelesen, nicht im Code aufgezaehlt.
# ---------------------------------------------------------------------------
NACHTRAG_EPIC = ("# Nachtrag (n)\n\n### 2t — Epic AF: Autonome Strategie-Forschungspipeline\n\n"
                 "Text des Epics.\n")
ZIEL_EPIC = "## 2t — Epic AF: Autonome Strategie-Forschungspipeline\n\nText des Epics.\n"


def test_fall_13_in_ausgelagerter_datei_angekommen():
    print("\nFall 13 - Inhalt in der ausgelagerten Datei angekommen, die BACKLOG.md nennt -> kein Befund")
    with Wegwerf() as w:
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01n.md", NACHTRAG_EPIC, verschoben=True)
        w.ziel_anhaengen("\n## Die Epics — nach `BACKLOG_EPICS.md` verschoben\n")
        w.schreibe(os.path.join(w.wurzel, "BACKLOG_EPICS.md"), "# Epics\n\n" + ZIEL_EPIC)
        rc, aus = w.lauf()
        check("rc 0", rc == 0, f"rc={rc}")
        check("Block 2t ist angekommen (kein FEHLT)", "FEHLT" not in aus)
        check("Kopfzeile nennt alle drei Zieldateien in dieser Reihenfolge",
              "BACKLOG.md " in aus and aus.find("BACKLOG_ARCHIV.md") < aus.find("BACKLOG_EPICS.md")
              and "aus BACKLOG.md gelesen" in aus)
        vorhanden, fehlend = nw.zieldateien(w.backlog)
        check("zieldateien(): BACKLOG.md, BACKLOG_ARCHIV.md, BACKLOG_EPICS.md; nichts fehlt",
              [os.path.basename(p) for p in vorhanden]
              == ["BACKLOG.md", "BACKLOG_ARCHIV.md", "BACKLOG_EPICS.md"] and fehlend == [])
        # Der Vergleich, an dem der alte Waechter scheiterte: ohne die
        # ausgelagerte Datei im Ziel ist derselbe Block FEHLT.
        ohne = nw.Ziel([w.backlog, w.archiv], w.journal)
        check("Gegenprobe: ohne BACKLOG_EPICS.md im Ziel waere 2t FEHLT",
              ohne.pruefe_nummer(nw.ART_BLOCK, "2t", nw.kern(ZIEL_EPIC.splitlines()[0]),
                                 ("(n)",))[0] == nw.FEHLT)


def test_fall_14_nirgends_angekommen():
    print("\nFall 14 - Inhalt NIRGENDS angekommen, auch nicht in der ausgelagerten Datei -> Befund")
    with Wegwerf() as w:
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01n.md", NACHTRAG_EPIC, verschoben=True)
        w.ziel_anhaengen("\n## Die Epics — nach `BACKLOG_EPICS.md` verschoben\n")
        w.schreibe(os.path.join(w.wurzel, "BACKLOG_EPICS.md"),
                   "# Epics\n\n## 2u — Ein anderer Block\n\nAnderer Text.\n")
        rc, aus = w.lauf()
        check("rc 1", rc == 1, f"rc={rc}")
        check("Block 2t als FEHLT", "Block 2t       FEHLT" in aus)
        check("Kern nirgends - auch nicht in der ausgelagerten Datei",
              "Kern 'Epic AF: Autonome Strategie-Forschungspi' nirgends" in aus)
        check("die ausgelagerte Datei war im Ziel (also wurde dort gesucht)",
              "BACKLOG_EPICS.md 5" in aus)
        check("BEFUND nennt (n)", "falsch verschoben (B-09-01n)" in _befundzeile(aus))


def test_fall_15_weitere_datei_ohne_codeaenderung():
    print("\nFall 15 - eine WEITERE ausgelagerte Datei kommt dazu -> kein Befund, ohne Codeaenderung")
    with Wegwerf() as w:
        name = "BACKLOG_ZUKUNFT.md"
        with open(os.path.join(_DIR, "nachtragswaechter.py"), encoding="utf-8") as f:
            quelle = f.read()
        check(f"der Waechter kennt den Namen {name} nicht (0 Treffer im Quelltext)",
              name not in quelle and "ZUKUNFT" not in quelle)
        # Auch die heutigen Namen stehen nur in der Erklaerung, nicht im Code:
        # alles nach dem Modul-Docstring, ohne Kommentarzeilen.
        import ast
        ende_docstring = ast.parse(quelle).body[0].end_lineno
        code = [z for z in quelle.splitlines()[ende_docstring:] if not z.lstrip().startswith("#")]
        check("BACKLOG_ARCHIV.md und BACKLOG_EPICS.md kommen im Code nicht vor (nur im Docstring)",
              not any("BACKLOG_ARCHIV" in z or "BACKLOG_EPICS" in z for z in code))
        w.nachtrag("BACKLOG_NACHTRAG_2026-09-01n.md", NACHTRAG_EPIC, verschoben=True)
        # 1. Datei existiert, ist aber NICHT genannt: kein Ziel -> rc 1.
        w.schreibe(os.path.join(w.wurzel, name), "# Zukunft\n\n" + ZIEL_EPIC)
        rc, aus = w.lauf()
        check("Datei vorhanden, aber in BACKLOG.md nicht genannt: kein Ziel, rc 1", rc == 1, f"rc={rc}")
        check("Kopfzeile nennt sie nicht", name not in aus)
        # 2. BACKLOG.md nennt sie (ohne Backticks genuegt): Ziel -> rc 0.
        w.ziel_anhaengen(f"\nVerschoben nach {name} (Abschnitt 2t).\n")
        rc, aus = w.lauf()
        check("in BACKLOG.md genannt: rc 0 ohne Codeaenderung", rc == 0, f"rc={rc}")
        check("Kopfzeile nennt sie mit Zeilenzahl", f"{name} 5" in aus)
        # 3. Ein genannter NACHTRAG ist kein Ziel - sonst pruefte er sich selbst.
        w.ziel_anhaengen("\nNachtrag `BACKLOG_NACHTRAG_2026-09-01n.md` abgeschlossen.\n")
        vorhanden, fehlend = nw.zieldateien(w.backlog)
        check("genannter Nachtrag ist kein Ziel",
              not any("NACHTRAG" in p for p in vorhanden + fehlend))
        # 4. Ein Pfadbestandteil ist keine Nennung; ein laengerer Name auch nicht.
        w.ziel_anhaengen("\nsiehe alt/BACKLOG_ALT.md und XBACKLOG_X.md\n")
        vorhanden, fehlend = nw.zieldateien(w.backlog)
        check("Pfad- und Wortbestandteile zaehlen nicht als Nennung",
              not any(os.path.basename(p) in ("BACKLOG_ALT.md", "XBACKLOG_X.md")
                      for p in vorhanden + fehlend))
        # 5. Genannt, aber nicht vorhanden: Werkzeugfehler rc 2, nicht rc 0/1.
        w.ziel_anhaengen("\nund `BACKLOG_FEHLT.md`\n")
        puffer, fehler = io.StringIO(), io.StringIO()
        with redirect_stdout(puffer), redirect_stderr(fehler):
            rc = nw.main(["--nachtraege", w.nachtraege, "--backlog", w.backlog,
                          "--journal", w.journal])
        check("genannt, aber fehlend: rc 2", rc == 2, f"rc={rc}")
        check("stderr nennt die fehlende Datei", "BACKLOG_FEHLT.md" in fehler.getvalue())


def test_nichts_uebrig():
    print("\nAbschluss - kein Wegwerf-Rest")
    check("alle Wegwerf-Verzeichnisse entfernt",
          not any(os.path.exists(p) for p in ANGELEGT), f"{len(ANGELEGT)} angelegt")
    check("Wegwerf-Verzeichnisse lagen nicht unter docs/",
          not any("/docs/" in p for p in ANGELEGT))


# ---------------------------------------------------------------------------
def main():
    start = time.time()
    print("Selbsttests des Nachtragswaechters")
    print(f"Interpreter: {sys.version.split()[0]} ({sys.executable})")
    for test in (test_fall_1_nummer_im_ziel, test_fall_2_nummer_nicht_im_ziel,
                 test_fall_3_nur_vergabevermerk, test_fall_4_zielzeile_mit_vermerk,
                 test_fall_5_doppelbelegung, test_fall_6_journal_ohne_quelle,
                 test_fall_7_falsch_verschoben, test_fall_8_nummer_mit_fremdem_inhalt,
                 test_fall_9_frist, test_fall_10_quelle_ueber_dateinamen,
                 test_fall_11_unterprozess, test_fall_12_werkzeugfehler,
                 test_fall_13_in_ausgelagerter_datei_angekommen,
                 test_fall_14_nirgends_angekommen,
                 test_fall_15_weitere_datei_ohne_codeaenderung,
                 test_nichts_uebrig):
        try:
            test()
        except Exception as e:                                # noqa: BLE001
            FEHLER.append(f"{test.__name__}: {type(e).__name__}: {e}")
            print(f"  [FEHLER] {test.__name__} abgebrochen: {type(e).__name__}: {e}")
    print("\n" + "=" * 78)
    print(f"{BESTANDEN} bestanden, {len(FEHLER)} fehlgeschlagen, "
          f"{time.time() - start:.1f}s")
    for f in FEHLER:
        print(f"  FEHLGESCHLAGEN: {f}")
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
