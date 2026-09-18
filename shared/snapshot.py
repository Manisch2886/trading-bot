#!/usr/bin/env python3
"""
Der unveraenderliche Kursdaten-Snapshot (TB-46, Teil 3)
==============================================================================
Registertext 5 (Abschnitt 16.3 der Vorregistrierung) verlangt **zwei**
Kursdatenbestaende:

  * einen **Live-Bestand**, taeglich fortgeschrieben, aus dem die neun
    `forward_test.py` und die Backtester-Pruefung nach Registertext 7 lesen;
  * einen **Snapshot** `<hash>/`, einmal gezogen und danach unveraenderlich,
    aus dem **ausschliesslich der Selektionslauf** liest.

Der Grund steht in Registertext 7: solange die Bots live abrufen, existiert
von ihrer Eingabe **keine Kopie**. Ein Vergleich gegen etwas, das nicht mehr
nachsehbar ist, ist kein Vergleich. Dieses Modul zieht die Kopie.

⚠️ **Was dieses Modul NICHT tut.** Es benennt `data/` nicht um, verschiebt
nichts, stellt kein Modul auf einen neuen Pfad um und entscheidet nicht,
welcher der beiden Ordnerentwuerfe gilt. Es ist das Werkzeug; der Schnitt ist
eine eigene Aufgabe und die Entscheidung darueber trifft der Betreiber.

Der Hash wird nicht neu erfunden
------------------------------------------------------------------------------
Der registrierte Datenstand-Hash entsteht in **einer** Funktion:

    research/vorregistrierung/herkunft.py :: datenstand(daten_dir)

SHA-256 ueber die `*.csv` **direkt** im Ordner, in sortierter
Dateinamenfolge, je Datei **Name + Groesse + SHA-256 des Inhalts**. Diese
Funktion hat den registrierten Wert
`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` bei 223
Dateien erzeugt, und dieses Modul **benutzt sie**, statt sie abzuschreiben.

⚠️ Eine zweite Berechnung koennte dieselbe Zahl liefern und trotzdem eine
andere Frage beantworten - andere Reihenfolge, andere Dateiauswahl. Genau
dieses Muster hat das Projekt bei der Messkette (TB-27/TB-28) und bei den
Ergebniskurven schon eingesammelt. `research/etf_trendfolge/datenstand.py`
hat sich aus demselben Grund geweigert, den Hash selbst zu rechnen.

⚠️ **Befund am Rande, gehoert in den Bericht:** die Berechnung steht
**trotzdem zweimal** im Repo - ein zeichengleiches Duplikat liegt in
`research/registernachtrag_tb41/pruefe_register.py:319`. Heute liefern beide
dasselbe. Wer eines von beiden aendert, merkt den Unterschied nicht.

Drei Eigenschaften der Berechnung, die den Zuschnitt betreffen
------------------------------------------------------------------------------
1. **Sie ist NICHT rekursiv.** `os.listdir` + `endswith(".csv")` sieht
   Unterordner nicht. Ein `data/snapshots/` **innerhalb** von `data/` wuerde
   den registrierten Hash also **nicht** mitzaehlen.
2. **Sie zaehlt nur `*.csv`.** Das `MANIFEST.json`, das dieses Modul in den
   Snapshot legt, aendert den Hash des Snapshots deshalb nicht - der Ordner
   traegt zu Recht den Namen des Bestandes, den er enthaelt.
3. **Sie haengt am uebergebenen Ordner.** Wird `data/` zu `data/live/`, zeigt
   die Voreinstellung von `datenstand()` auf einen Ordner ohne eine einzige
   `.csv` - der Hash wird dann der der **leeren** Menge, und das sieht wie
   eine Datenaenderung aus, obwohl nur der Ordner umgezogen ist.

Die Voreinstellung ist der Trockenlauf
------------------------------------------------------------------------------
Kopiert wird nur mit `--ziehen`. 202 MB zu kopieren gehoert nicht in die
Voreinstellung - dieselbe Abwaegung wie bei `kursdaten_neuaufbau.py`
(`--schreiben`) und bei den Broker-Bruecken (`--echt`).

Was ausdruecklich zum Abbruch fuehrt
------------------------------------------------------------------------------
⚠️ Keiner dieser Faelle laeuft still weiter:

  * **Das Ziel `<hash>/` existiert schon.** Es wird **nie** ueberschrieben -
    ein zweiter Snapshot ist ein neuer Lauf (Registertext 5c).
  * **Die Quelle ist leer.** Ein Snapshot ohne Kursdatei ist kein Snapshot;
    er traegt sogar einen gueltig aussehenden Namen (den Hash der leeren
    Menge). Das ist die gefaehrlichste Form von "erfolgreich".
  * **Eine Quersumme laesst sich nicht bilden** (Datei unlesbar, verschwindet
    mitten im Lauf).
  * **Eine Kopie weicht byteweise von der Quelle ab.** Dann wird der
    angelegte Ordner wieder entfernt und die Datei genannt.
  * **Die Quelle enthaelt Unterordner.** Die Hash-Berechnung ist nicht
    rekursiv (siehe 1.): ein Snapshot eines Baums traegt einen Namen, der
    nur seine oberste Ebene beschreibt. "Vollstaendig" waere dann eine
    Behauptung, die der Name nicht deckt.
  * **Das Ziel liegt innerhalb der Quelle.** Dann kopierte der Lauf in den
    Bestand, den er beschreibt.
  * **Die Quelle enthaelt schon eine Datei `MANIFEST.json`.** Sie wuerde vom
    Manifest des Snapshots ueberschrieben - und weil das Manifest sich selbst
    nicht auffuehrt, faellt das beim Nachpruefen nicht auf.

⚠️ TB-47 legt **drei weitere** daneben. Die acht oben bleiben unveraendert:

  * **Eine Eingabedatei aus der Liste fehlt in der Quelle.** Sie wird
    namentlich genannt. Ein Snapshot ohne eine Eingabe, die der Lauf liest,
    ist kein Snapshot des Laufs.
  * **Die Quelle enthaelt eine Datei, die nicht in der Liste steht.**
    ⭐ **Entschieden wurde: ABBRUCH, nicht Meldung.** Begruendung: der Name
    des Ordners ist der Hash ueber **genau die Dateien der Liste**. Eine
    Datei daneben hat nur zwei moegliche Ausgaenge, und beide sind still -
    entweder sie wird nicht mitkopiert, dann ist der Snapshot unvollstaendig
    und sieht vollstaendig aus; oder sie wird mitkopiert, dann luegt die
    Liste im Manifest. Genau dieses "sieht gueltig aus" ist die Bauform, die
    dieses Modul an allen anderen Stellen schon abbricht (leere Quelle,
    Unterordner, vorhandenes `MANIFEST.json`). Eine blosse Meldung waere hier
    die einzige Ausnahme - und sie stuende im Manifest neben einem Hash, der
    sie nicht deckt.
  * **Die Teilkerzen-Pruefung findet etwas** - oder sie ist nicht
    ausfuehrbar. Im ersten Fall wird nicht gezogen; im zweiten ist der
    Ausgang **2**, nie 0. ⚠️ **Seit TB-49 mit genau einer Ausnahme, siehe
    unten** - der zweite Fall bleibt unveraendert die **2**.

⚠️ Ausserdem bricht `--ziehen` ab, wenn `datenstand_hash` **nicht** den
verankerten Wert `d9449faf…` ergibt (abschaltbar mit `--kein-anker`, denn
Wegwerf-Verzeichnisse in Selbsttests koennen ihn naturgemaess nicht treffen).

TB-47: DIE SNAPSHOT-GRENZE - alle Eingaben, zwei Hashes
------------------------------------------------------------------------------
⚠️ Dieses Modul ist in TB-46 gebaut worden - **vor** dem Registernachtrag.
Registertext 5a verlangt seither drei Dinge, die es bis TB-47 nicht konnte:

**1. Der Snapshot enthaelt ALLE Eingaben des Laufs**, die nicht Code unter
dem registrierten Commit sind - nicht nur `data/*.csv`. TB-47 hat diese Menge
ueber den Syntaxbaum **bestimmt statt geraten**
(`research/snapshotgrenze/erhebung_eingaben.py`, ausgehend von den 90
Selektionsmodulen aus TB-46). Ergebnis: neben den Kursdateien sind es genau
**zwei** Dateien, beide versioniert, beide Symbollisten - siehe `EINGABEN`.

⚠️ **Welche Dateien aufgenommen werden, steht in einer LISTE, die im Manifest
mitgefuehrt wird** - nicht in einer Regel, die spaeter jemand anders auslegt.
Eine Regel ("alles unter `config/`") haette beim naechsten hinzugefuegten
Konfigurationsschnipsel stillschweigend ihren Umfang geaendert; eine Liste
kann das nicht.

⭐ **Der Handelskalender ist KEINE Eingabe.** Er kommt aus
`pandas_market_calendars` (`mcal.get_calendar`), nicht aus einer Datei - er
ist **Umgebung** und gehoert ins Lock. Damit haengt das Ergebnis an einer
Paketfassung, und **ein Snapshot kann das nicht einfangen**. Das ist eine
Eigenschaft des Aufbaus, keine Luecke dieses Moduls.

**2. Zwei Hashes, zwei Funktionen, zwei Felder.**

    snapshot_hash    ueber die sortierten (Pfad, Inhalts-Hash)-Paare DER
                     DATEIEN. Er ist der **Name** des Ordners und beantwortet:
                     *"ist das derselbe Eingabesatz?"*
    datenstand_hash  ⚠️ **unveraendert** das registrierte Verfahren: `*.csv`
                     auf der obersten Ebene, Name + Groesse + SHA-256,
                     sortiert. Er beantwortet die **Herkunftsfrage**: *"sind
                     das dieselben Kursdateien?"* - und muss weiterhin
                     `d9449faf…` ergeben.

⚠️ **Der Snapshot-Hash laeuft ueber die DATEIEN, nicht ueber das Manifest.**
Liefe er ueber das Manifest, haenge der Name an der Metadaten-Formatierung,
und ein zusaetzliches Feld ergaebe einen **anderen Namen fuer denselben
Inhalt**. Deshalb fuehrt das Manifest sich selbst auch nicht in der Liste.

**3. Die Teilkerzen-Pruefung steht im Manifest.** Vor dem Ziehen laeuft
`shared/zeitabdeckung.py` ueber die **Quelle** (nicht ueber die Kopie), und
ihr Ergebnis wird festgehalten. ⚠️ **Findet sie etwas, wird nicht gezogen.**
Ist sie nicht ausfuehrbar, ist das **2**, nie 0.

TB-49: DIE AUSNAHME `rand_erste` - als REGEL, nicht als Liste
------------------------------------------------------------------------------
Registertext 5a, Zusatz (Vorregistrierung, **Abschnitt 17.3**, beschlossen am
18.09.2026) laesst eine Befundart ausdruecklich zu. Bis TB-48 kannte dieses
Modul die Ausnahme nicht und brach bei **jedem** Befund ab - an `data/` also
immer, denn dort stehen 36.

**Zugelassen ist ein Befund genau dann, wenn ALLE DREI zutreffen:**

    (a) die Art ist `rand_erste`
    (b) er betrifft die **erste** Kerze der Datei - eigens nachgestellt,
        nicht aus dem Namen der Art gefolgert
    (c) die Kerze ist nachweislich **das Aggregat genau der vorhandenen
        feineren Kerzen** (Urteil `ABGELEITETE_TEILKERZE`, `aggregat_passt`)

⚠️ **Warum eine Regel und keine Liste der 36 Dateien.** Eine Liste veraltet.
Jedes neu gelistete Symbol bringt denselben Befund mit; eine ungepflegte Liste
blockiert dann entweder zu Unrecht oder - schlimmer - laesst zu Unrecht durch.
Die Regel deckt den kuenftigen Fall mit ab.

⚠️ **Was sich NICHT geaendert hat:**

  * Die Pruefung **schlaegt weiter an** und meldet weiter **jeden** Befund.
    `teilkerzen()["befunde"]` fuehrt an `data/` unveraendert 36 Eintraege.
  * **`rand_letzte` bricht ab** - ohne Ausnahme, auch bei einer einzigen
    Datei. Das ist der Rand, in den ein Abruf mitten hineingeschrieben haben
    koennte.
  * Ein `rand_erste`, der **nicht** abgeleitet ist, und ein Befund an einer
    **spaeteren** Kerze brechen ab, und die Datei wird genannt.
  * Eine Datei **ohne feineren Zeugen** kann Bedingung (c) nicht belegen.
    ⭐ **Entschieden: nicht belegbar ist nicht zugelassen.** An `data/` ist
    das folgenlos - die 175 Dateien mit `kein_zeuge` tragen **keinen**
    Befund, weil `pruefe_datei` die Deckungspruefung dort gar nicht erreicht.
    Die Regel greift dort also nie; sie waere nur dann streng, wenn ein
    kuenftiger Zeuge verschwindet - und genau dann soll sie es sein.
  * ⚠️ **Es gibt KEINE Uebergehen-Flagge.** Keine Option der Befehlszeile,
    kein Schalter, kein Umgebungsvorbehalt. Wer sie einbaut, hat die Ausnahme
    in ihr Gegenteil verkehrt.

**Das Manifest fuehrt die zugelassenen Befunde auf** - je Datei Name, Art und
erste Kerze, dazu die Gesamtzahl (`zugelassene_befunde`,
`zugelassene_befunde_anzahl`) und die **Herkunft der Erlaubnis**
(`zugelassene_befunde_herkunft` -> Registertext 5a, Abschnitt 17.3).
⭐ Der Snapshot dokumentiert damit selbst, was bei seiner Erzeugung erlaubt
wurde, und ein Pruefer kann die Grundlage nachlesen, ohne diesen Code zu
kennen.

Der Ordneraufbau eines Snapshots
------------------------------------------------------------------------------
    <snapshot_hash>/
        AAPL_1d.csv            die Kursdateien - flach, wie bisher
        BTCUSDT_1h.csv         ⭐ damit bleibt `datenstand_hash` rechenbar:
        ...                       das Verfahren ist NICHT rekursiv und sieht
        config/                   genau diese oberste Ebene
            top25_symbols.txt  die uebrigen Eingaben, mit ihrer
            sp500_top150.txt   Ordnerstruktur
        MANIFEST.json

Rueckgabewerte - "konnte nicht messen" ist ein eigener, roter Ausgang
------------------------------------------------------------------------------
    0   in Ordnung: gezogen, oder `--pruefen` findet den Stand unveraendert
    1   Befund: `--pruefen` findet den Snapshot VERAENDERT
    2   NICHT PRUEFBAR / abgebrochen

⚠️ Die 2 ist der Grund, warum es sie gibt. In TB-45 haben zwei Wachen
"bestanden" gemeldet, ohne etwas gemessen zu haben - ein gescheiterter Aufruf
und ein leeres Ergebnis sahen gleich aus. Hier nicht: wer nicht messen
konnte, sagt es mit einem eigenen Wert.

Nutzung
------------------------------------------------------------------------------
    python3 shared/snapshot.py --quelle data --ziel snapshots        # Trockenlauf
    python3 shared/snapshot.py --quelle data --ziel snapshots --ziehen
    python3 shared/snapshot.py --pruefen snapshots/<hash>
    python3 shared/snapshot.py --quelle data --nur-hash
"""

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys
from datetime import datetime, timezone

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)

MANIFEST = "MANIFEST.json"
WERKZEUG = "shared/snapshot.py"

# Wo das registrierte Hash-Verfahren steht. Ein Pfad, keine Abschrift.
HERKUNFT_PFAD = os.path.join(BASE_DIR, "research", "vorregistrierung",
                             "herkunft.py")

# Wo die Teilkerzen-Pruefung steht. Auch hier: ein Pfad, keine zweite
# Fassung der Pruefung.
ZEITABDECKUNG_PFAD = os.path.join(_SHARED_DIR, "zeitabdeckung.py")

# ⚠️ Der verankerte Datenstand vom 15.09.2026 (Tatsachennotiz, 223 Dateien).
# Er steht hier als **Pruefwert**, nicht als Rechenweg: gerechnet wird
# weiterhin ausschliesslich von `herkunft.datenstand`.
VERANKERTER_DATENSTAND = (
    "d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84")
VERANKERTE_KURSDATEIEN = 223


# ===========================================================================
# Die Snapshot-Grenze (TB-47, Teil 1)
# ===========================================================================
#
# ⚠️ Eine **Liste**, keine Regel. Wer hier etwas ergaenzt, aendert den
# `snapshot_hash` - und das ist genau richtig so: ein anderer Eingabesatz
# bekommt einen anderen Namen.
#
# Erhoben in TB-47 ueber den Syntaxbaum, ausgehend von den 90
# Selektionsmodulen aus TB-46 und transitiv ueber alles, was sie importieren
# (142 Module). Die Rohdaten stehen in
# `research/snapshotgrenze/ergebnisse/eingaben.json`.

EINGABEN = (
    {
        "pfad": "config/top25_symbols.txt",
        "rolle": "Symbolliste Krypto - welche 25 Maerkte gehandelt werden",
        "leser": "shared/symbols_config.py:28",
    },
    {
        "pfad": "config/sp500_top150.txt",
        "rolle": "Symbolliste Aktien - die S&P-500-Auswahl",
        "leser": ("strategies/{elliott_wave_stocks,rsi2_mean_reversion,"
                  "turtle_soup_stocks,volatility_breakout}/"
                  "stocks_symbols_config.py"),
    },
)

# Rueckgabewerte
OK = 0
BEFUND = 1
NICHT_PRUEFBAR = 2

# Die drei Ausgaenge von `--pruefen`
UNVERAENDERT = "unveraendert"
VERAENDERT = "veraendert"
UNPRUEFBAR = "nicht pruefbar"


class Snapshotfehler(Exception):
    """Ein Lauf, der nicht zu Ende gebracht werden darf.

    Jede Stelle, die still weiterlaufen koennte, wirft stattdessen diese
    Ausnahme. `main` faengt sie und gibt 2 zurueck.
    """


# ===========================================================================
# Teil 1 - Das Hash-Verfahren, geliehen statt abgeschrieben
# ===========================================================================

def lade_herkunft(pfad=None):
    """Das Modul mit dem registrierten Hash-Verfahren laden.

    Ueber den Dateipfad, nicht ueber `sys.path`: der fremde Ordner
    `research/vorregistrierung/` bringt ein eigenes `beispieldaten.py` mit,
    das bei einem Import ueber den Suchpfad hiesige Namen verdecken kann.
    Denselben Weg geht `research/etf_trendfolge/register.py`.

    ⚠️ Faellt das Laden aus, wird **nicht** auf eine eigene Berechnung
    ausgewichen. Eine Ersatzberechnung waere genau die Doppelfuehrung, gegen
    die dieses Modul geschrieben ist - und sie waere unsichtbar.
    """
    pfad = pfad or HERKUNFT_PFAD
    if not os.path.exists(pfad):
        raise Snapshotfehler(
            "Das registrierte Hash-Verfahren ist nicht auffindbar: %s fehlt. "
            "Ohne es wird KEIN Hash gebildet - eine eigene Berechnung waere "
            "eine zweite Wahrheit." % pfad)
    spez = importlib.util.spec_from_file_location("tb46_herkunft", pfad)
    if spez is None or spez.loader is None:
        raise Snapshotfehler("%s ist nicht als Modul ladbar." % pfad)
    modul = importlib.util.module_from_spec(spez)
    try:
        spez.loader.exec_module(modul)
    except Exception as fehler:                       # noqa: BLE001
        raise Snapshotfehler("%s laesst sich nicht laden: %s" % (pfad, fehler))
    if not hasattr(modul, "datenstand"):
        raise Snapshotfehler(
            "%s kennt kein `datenstand()` mehr. Das Verfahren ist umgezogen - "
            "dieses Modul darf dann nicht weiterrechnen." % pfad)
    return modul


def gesamthash(ordner, herkunft=None):
    """(hash, dateizahl) - nach dem registrierten Verfahren.

    Gerechnet wird von `herkunft.datenstand`, nicht hier.
    """
    if not os.path.isdir(ordner):
        raise Snapshotfehler("%s ist kein Verzeichnis." % ordner)
    h = herkunft or lade_herkunft()
    try:
        stand = h.datenstand(ordner)
    except OSError as fehler:
        raise Snapshotfehler(
            "Der Hash ueber %s laesst sich nicht bilden: %s" % (ordner, fehler))
    return stand["datenstand"], stand["dateien"]


def quersumme(pfad):
    """SHA-256 einer einzelnen Datei - dieselbe Rechnung wie im Gesamthash.

    ⚠️ Ein `IOError` wird **nicht** zu "keine Quersumme" verschluckt. Eine
    Datei, deren Quersumme sich nicht bilden laesst, ist kein Eintrag mit
    leerem Feld, sondern ein Abbruchgrund.
    """
    hasher = hashlib.sha256()
    try:
        with open(pfad, "rb") as datei:
            for block in iter(lambda: datei.read(1 << 20), b""):
                hasher.update(block)
    except OSError as fehler:
        raise Snapshotfehler(
            "Quersumme von %s nicht bildbar: %s" % (pfad, fehler))
    return hasher.hexdigest()


# ===========================================================================
# Teil 1b - Der zweite Hash: der Name (TB-47)
# ===========================================================================

def snapshot_hash(paare):
    """SHA-256 ueber die sortierten (Pfad, Inhalts-Hash)-Paare.

    `paare` ist eine Abbildung `{pfad_im_snapshot: sha256}`. Der Pfad ist
    relativ zur Wurzel des Snapshots und benutzt **immer** `/`, nie `os.sep` -
    sonst hiesse derselbe Eingabesatz auf zwei Rechnern verschieden.

    ⚠️ **Dieser Hash laeuft ueber die DATEIEN, nicht ueber das Manifest.**
    Das ist der Grund, warum ein zusaetzliches Manifestfeld den Namen des
    Snapshots nicht aendert - und warum `MANIFEST.json` selbst nicht eingeht.

    ⚠️ Er ist bewusst **nicht** dasselbe Verfahren wie `datenstand`. Dort geht
    die Dateigroesse mit ein und es zaehlen nur `*.csv`; hier zaehlt jede
    Datei der Liste, und der Pfad steht mit seinem Ordner darin. Zwei Fragen,
    zwei Rechnungen, zwei Felder.
    """
    if not paare:
        raise Snapshotfehler(
            "Der Snapshot-Hash soll ueber null Dateien gebildet werden. Der "
            "Hash der leeren Menge sieht gueltig aus und ist es nicht.")
    h = hashlib.sha256()
    for pfad in sorted(paare):
        if os.sep != "/" and os.sep in pfad:
            raise Snapshotfehler(
                "Der Pfad %r enthaelt einen Trenner dieses Betriebssystems. "
                "Im Snapshot-Hash stehen Pfade immer mit `/`, sonst haengt "
                "der Name des Snapshots am Rechner." % pfad)
        h.update(pfad.encode("utf-8"))
        h.update(b"\0")
        h.update(paare[pfad].encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


# ===========================================================================
# Teil 1c - Die Eingabeliste (TB-47)
# ===========================================================================

def eingabeliste(quelle, wurzel=None, eingaben=EINGABEN):
    """Was in den Snapshot geht - als Liste, nicht als Regel.

    Rueckgabe: Liste von Eintraegen

        {"im_snapshot": "config/top25_symbols.txt",   # Pfad IM Snapshot
         "herkunft":    "/…/trading-bot/config/top25_symbols.txt",
         "art":         "Eingabe" | "Kursdatei",
         "rolle":       "…", "leser": "…"}

    ⚠️ Fehlt eine Datei der Liste, wird **abgebrochen und sie genannt**. Ein
    Snapshot ohne eine Eingabe, die der Lauf liest, beschreibt den Lauf nicht.
    """
    wurzel = wurzel or BASE_DIR
    liste = []

    try:
        vorhanden = sorted(os.listdir(quelle))
    except OSError as fehler:
        raise Snapshotfehler("Die Quelle %s ist nicht lesbar: %s"
                             % (quelle, fehler))

    for name in vorhanden:
        if not os.path.isfile(os.path.join(quelle, name)):
            continue
        if not name.endswith(".csv"):
            # ⚠️ Kein stilles Mitnehmen und kein stilles Weglassen - siehe
            # die Begruendung im Modulkopf.
            raise Snapshotfehler(
                "Die Quelle %s enthaelt `%s` - eine Datei, die weder eine "
                "Kursdatei noch ein Eintrag der Eingabeliste ist. Der Name "
                "des Snapshots ist der Hash ueber genau die Dateien der "
                "Liste; eine Datei daneben macht ihn zu einer Behauptung."
                % (quelle, name))
        liste.append({"im_snapshot": name,
                      "herkunft": os.path.join(quelle, name),
                      "art": "Kursdatei",
                      "rolle": "Kursdaten des Laufs",
                      "leser": "die neun Bots und der Selektionslauf"})

    fehlend = []
    for eintrag in eingaben:
        pfad = os.path.join(wurzel, eintrag["pfad"].replace("/", os.sep))
        if not os.path.isfile(pfad):
            fehlend.append(eintrag["pfad"])
            continue
        liste.append({"im_snapshot": eintrag["pfad"],
                      "herkunft": pfad,
                      "art": "Eingabe",
                      "rolle": eintrag["rolle"],
                      "leser": eintrag["leser"]})

    if fehlend:
        raise Snapshotfehler(
            "Diese Eingabedatei(en) der Liste fehlen unter %s: %s. Ein "
            "Snapshot ohne eine Eingabe, die der Lauf liest, ist kein "
            "Snapshot des Laufs." % (wurzel, ", ".join(fehlend)))
    return liste


# ===========================================================================
# Teil 1d - Die Teilkerzen-Pruefung (TB-47) und ihre Ausnahme (TB-49)
# ===========================================================================
#
# ⚠️ **Die Ausnahme ist eine REGEL, keine Liste von Dateien.** Eine Liste
# veraltet: jedes neu gelistete Symbol bringt denselben Befund mit, und eine
# ungepflegte Liste blockiert dann entweder zu Unrecht oder laesst zu Unrecht
# durch. Die Regel deckt den kuenftigen Fall mit ab.
#
# ⚠️ **Und es gibt keine Uebergehen-Flagge.** Registertext 5a, Zusatz sagt
# ausdruecklich: *"Die Pruefung selbst wird nicht abgeschwaecht."* Sie schlaegt
# weiter an, meldet weiter ihre 36 Befunde und liefert allein weiter
# Rueckgabewert 1. Gezogen wird gegen den **Registereintrag**, nicht gegen ein
# Schweigen der Pruefung und nicht gegen eine Befehlszeilenoption.

# Wohin ein Pruefer sehen muss, der wissen will, worauf die Zulassung sich
# stuetzt - ohne diesen Code zu kennen. Steht so im Manifest.
REGISTERVERWEIS = {
    "registertext": "5a, Zusatz - Ausnahme `rand_erste`",
    "fundstelle": "docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3",
    "beschlossen": "18.09.2026",
    "wortlaut": ("Diese Befundart ist fuer das Ziehen eines Snapshots "
                 "zugelassen, wenn alle drei Bedingungen erfuellt sind: "
                 "(a) der Befund betrifft ausschliesslich die erste Kerze der "
                 "Datei - fuer `rand_letzte` gilt die Ausnahme nicht; "
                 "(b) die Kerze ist nachweislich das Aggregat genau der "
                 "vorhandenen feineren Kerzen; "
                 "(c) die Ausnahme wird im Manifest des Snapshots je Datei "
                 "aufgefuehrt, mit Art und erster Kerze."),
    "umgesetzt_in": "shared/snapshot.py::_zulassung (TB-49)",
}

# Die eine zugelassene Befundart. ⚠️ `rand_letzte` steht hier NICHT und darf
# hier nie stehen: das ist der Rand, in den ein Abruf mitten hineingeschrieben
# haben koennte.
ZUGELASSENE_ART = "rand_erste"


def _zulassung(eintrag, befund, abgeleitet):
    """Die drei Bedingungen der Ausnahme an EINEM Befund pruefen.

    Rueckgabe: `(True, None)` oder `(False, "Grund")`. Der Grund geht
    woertlich in die Abbruchmeldung - wer abbricht, sagt warum.

    `eintrag` ist der Datei-Eintrag aus `pruefe_ordner`, `befund` einer seiner
    Befunde, `abgeleitet` das Urteil `ABGELEITETE_TEILKERZE` **aus dem
    geladenen Modul** - nicht als Abschrift hier.

    ⚠️ (b) wird eigens nachgestellt, obwohl die Art `rand_erste` heute nur an
    der ersten Kerze entstehen kann. Die Bedingung des Registers lautet "die
    erste Kerze der Datei", nicht "ein Befund, der sich so nennt"; wer die
    Herkunft des Namens fuer den Nachweis nimmt, prueft nichts.
    """
    art = befund.get("art")
    # --- (a) Art ---------------------------------------------------------
    if art != ZUGELASSENE_ART:
        return False, ("Art `%s` - zugelassen ist allein `%s`"
                       % (art, ZUGELASSENE_ART))

    # --- (b) Es ist die erste Kerze der Datei ----------------------------
    erste = eintrag.get("erste")
    deckung = (eintrag.get("deckung") or {}).get("erste")
    if deckung is None:
        return False, ("fuer diese Datei liegt keine Deckungspruefung der "
                       "ersten Kerze vor (kein feinerer Zeuge) - Bedingung "
                       "(b)/(c) ist hier nicht belegbar, und nicht belegbar "
                       "ist nicht zugelassen")
    if not erste or deckung.get("kerze") != erste:
        return False, ("der Befund sitzt auf Kerze %r, die erste Kerze der "
                       "Datei ist %r" % (deckung.get("kerze"), erste))

    # --- (c) Die Kerze ist das Aggregat genau der feineren Kerzen --------
    urteil = befund.get("urteil") or deckung.get("urteil")
    if urteil != abgeleitet or deckung.get("aggregat_passt") is not True:
        return False, ("Urteil `%s` - zugelassen ist allein `%s`: die Kerze "
                       "muss nachweislich das Aggregat genau der vorhandenen "
                       "feineren Kerzen sein" % (urteil, abgeleitet))
    return True, None


def lade_zeitabdeckung(pfad=None):
    """Die bestehende Teilkerzen-Pruefung laden - ueber den Dateipfad.

    Derselbe Weg wie bei `lade_herkunft`, aus demselben Grund (TB-40:
    gleichnamige Module werden nicht ueber den Suchpfad importiert).

    ⚠️ Faellt das Laden aus, wird **keine** Ersatzpruefung gebaut. Der
    Aufrufer macht daraus "nicht pruefbar" - und das ist die **2**.
    """
    pfad = pfad or ZEITABDECKUNG_PFAD
    if not os.path.exists(pfad):
        raise Snapshotfehler(
            "Die Teilkerzen-Pruefung ist nicht auffindbar: %s fehlt. Ohne sie "
            "wird NICHT gezogen - eine Ersatzpruefung waere eine zweite "
            "Wahrheit." % pfad)
    spez = importlib.util.spec_from_file_location("tb47_zeitabdeckung", pfad)
    if spez is None or spez.loader is None:
        raise Snapshotfehler("%s ist nicht als Modul ladbar." % pfad)
    modul = importlib.util.module_from_spec(spez)
    try:
        spez.loader.exec_module(modul)
    except Exception as fehler:                       # noqa: BLE001
        raise Snapshotfehler("%s laesst sich nicht laden: %s" % (pfad, fehler))
    if not hasattr(modul, "pruefe_ordner"):
        raise Snapshotfehler(
            "%s kennt kein `pruefe_ordner()` mehr. Die Pruefung ist umgezogen "
            "- dieses Modul darf dann nicht weiterziehen." % pfad)
    # ⚠️ TB-49: Bedingung (c) der Ausnahme haengt am Urteil
    # `ABGELEITETE_TEILKERZE`. Es wird von dort **geholt**, nicht hier
    # abgeschrieben - sonst liefe die Zulassung eines Tages gegen einen Namen,
    # den die Pruefung nicht mehr vergibt, und liesse **nichts** mehr durch
    # oder, schlimmer, alles.
    if not hasattr(modul, "ABGELEITETE_TEILKERZE"):
        raise Snapshotfehler(
            "%s kennt kein `ABGELEITETE_TEILKERZE` mehr. Daran haengt "
            "Bedingung (c) der Ausnahme aus Registertext 5a, Zusatz - ohne "
            "sie wird NICHT gezogen." % pfad)
    return modul


def teilkerzen(quelle, zeitabdeckung=None):
    """Die Teilkerzen-Pruefung ueber die QUELLE. Ergebnis fuers Manifest.

    ⚠️ Ueber die Quelle, nicht ueber die Kopie: gefragt ist, ob der **Bestand**
    frei von Teilkerzen ist. Eine Kopie zu pruefen beantwortete nur, ob das
    Kopieren funktioniert hat - und das prueft dieses Modul schon zweimal.

    ⚠️ **TB-49: die Pruefung wird nicht abgeschwaecht.** `befunde` fuehrt
    weiterhin **jeden** Befund - an `data/` sind das unveraendert 36. Was
    dazukommt, ist die Einordnung je Befund nach Registertext 5a, Zusatz
    (Abschnitt 17.3): `zugelassen` oder `nicht_zugelassen`. **Nur letzteres
    verhindert das Ziehen.**

    Rueckgabe:
        {"ausfuehrbar": True, "befunde": [...], "dateien_geprueft": 223,
         "zugelassen": [...], "nicht_zugelassen": [...], "stand": "…"}

    Ein Eintrag in `nicht_zugelassen` heisst: **es wird nicht gezogen.**
    """
    modul = zeitabdeckung or lade_zeitabdeckung()
    abgeleitet = getattr(modul, "ABGELEITETE_TEILKERZE", None)
    if not abgeleitet:
        raise Snapshotfehler(
            "Die Teilkerzen-Pruefung kennt kein `ABGELEITETE_TEILKERZE`. "
            "Daran haengt Bedingung (c) der Ausnahme - ohne sie wird NICHT "
            "gezogen.")
    try:
        stand = modul.jetzt_utc()
        rohbefunde = modul.pruefe_ordner(quelle, stand=stand)
    except Exception as fehler:                       # noqa: BLE001
        raise Snapshotfehler(
            "Die Teilkerzen-Pruefung ueber %s liess sich nicht ausfuehren: "
            "%s. Das ist NICHT PRUEFBAR, nicht 'in Ordnung'."
            % (quelle, fehler))

    befunde = []
    zugelassen = []
    abgelehnt = []
    for eintrag in rohbefunde:
        if not eintrag.get("befunde"):
            continue
        datei = eintrag.get("datei")
        erste = eintrag.get("erste")
        gruende = []
        for roh in eintrag["befunde"]:
            b = roh if isinstance(roh, dict) else {"art": str(roh),
                                                   "text": str(roh)}
            passt, grund = _zulassung(eintrag, b, abgeleitet)
            if passt:
                # ⚠️ Genau das verlangt Bedingung (c) des Registereintrags:
                # je Datei Name, Art und erste Kerze.
                zugelassen.append({
                    "datei": datei,
                    "art": b.get("art"),
                    "erste_kerze": erste,
                    "urteil": b.get("urteil") or abgeleitet,
                    "text": b.get("text"),
                })
            else:
                gruende.append({"art": b.get("art"), "grund": grund,
                                "text": b.get("text")})
        if gruende:
            abgelehnt.append({"datei": datei, "erste_kerze": erste,
                              "gruende": gruende})
        befunde.append({
            "datei": datei,
            "erste_kerze": erste,
            "arten": sorted({b.get("art") if isinstance(b, dict) else str(b)
                             for b in eintrag["befunde"]}),
            "texte": [b.get("text") if isinstance(b, dict) else str(b)
                      for b in eintrag["befunde"]][:4],
            "zugelassen": not gruende,
        })
    return {
        "ausfuehrbar": True,
        "werkzeug": "shared/zeitabdeckung.py::pruefe_ordner",
        "stand": stand.isoformat() if hasattr(stand, "isoformat") else str(stand),
        "dateien_geprueft": len(rohbefunde),
        "befunde": befunde,
        "frei_von_teilkerzen": not befunde,
        # --- TB-49: die Ausnahme, und woher sie kommt ---------------------
        "ausnahme": REGISTERVERWEIS,
        "zugelassen": zugelassen,
        "zugelassen_anzahl": len(zugelassen),
        "zugelassen_dateien": len({z["datei"] for z in zugelassen}),
        "nicht_zugelassen": abgelehnt,
        "zieht_trotz_befunden": bool(befunde) and not abgelehnt,
    }


# ===========================================================================
# Teil 2 - Ziehen
# ===========================================================================

def _pruefe_quelle(quelle):
    """Die Quelle, bevor irgendetwas kopiert wird. Wirft, statt zu warnen."""
    if not os.path.isdir(quelle):
        raise Snapshotfehler("Die Quelle %s ist kein Verzeichnis." % quelle)
    try:
        eintraege = sorted(os.listdir(quelle))
    except OSError as fehler:
        raise Snapshotfehler("Die Quelle %s ist nicht lesbar: %s"
                             % (quelle, fehler))

    unterordner = [e for e in eintraege
                   if os.path.isdir(os.path.join(quelle, e))]
    if unterordner:
        raise Snapshotfehler(
            "Die Quelle %s enthaelt Unterordner (%s). Das registrierte "
            "Hash-Verfahren ist NICHT rekursiv - ein Snapshot dieses Baums "
            "traege einen Namen, der nur seine oberste Ebene beschreibt."
            % (quelle, ", ".join(unterordner)))

    dateien = [e for e in eintraege
               if os.path.isfile(os.path.join(quelle, e))]

    # ⚠️ Eine Quelldatei, die schon `MANIFEST.json` heisst, wuerde beim
    # Schreiben des Manifests **ueberschrieben** - der Snapshot waere dann
    # unvollstaendig und saehe vollstaendig aus. Beim Nachpruefen faellt es
    # nicht auf, weil das Manifest sich selbst nicht auffuehrt.
    if MANIFEST in dateien:
        raise Snapshotfehler(
            "Die Quelle %s enthaelt schon eine Datei namens %s. Das Manifest "
            "des Snapshots wuerde sie ueberschreiben, und der Snapshot waere "
            "unvollstaendig, ohne es zu sagen." % (quelle, MANIFEST))

    kursdateien = [e for e in dateien if e.endswith(".csv")]
    if not kursdateien:
        raise Snapshotfehler(
            "Die Quelle %s enthaelt keine einzige `.csv`. Ein leerer Snapshot "
            "traegt den Hash der leeren Menge und sieht dabei gueltig aus - "
            "das ist kein Erfolg." % quelle)
    return dateien, kursdateien


def _relativ(pfad, wurzel):
    """Ein Pfad im Snapshot - immer mit `/`, nie mit `os.sep`."""
    return os.path.relpath(pfad, wurzel).replace(os.sep, "/")


def _pruefe_ziel(quelle, ziel_basis, hash_):
    """Der Zielordner, bevor er angelegt wird."""
    q = os.path.realpath(quelle)
    z = os.path.realpath(ziel_basis)
    if z == q or z.startswith(q + os.sep):
        raise Snapshotfehler(
            "Das Ziel %s liegt innerhalb der Quelle %s. Der Lauf kopierte in "
            "den Bestand, den er beschreibt." % (z, q))
    ziel = os.path.join(ziel_basis, hash_)
    if os.path.exists(ziel):
        raise Snapshotfehler(
            "%s existiert bereits. Ein bestehender Snapshot wird NIE "
            "ueberschrieben - ein zweiter Snapshot ist ein neuer Lauf "
            "(Registertext 5c)." % ziel)
    return ziel


def ziehen(quelle, ziel_basis, wirklich=False, herkunft=None, wurzel=None,
           eingaben=EINGABEN, anker=True, zeitabdeckung=None):
    """Alle Eingaben des Laufs nach `<ziel_basis>/<snapshot_hash>/` kopieren.

    Die Reihenfolge ist nicht beliebig:

      1. Quelle pruefen (leer? Unterordner? fremdes `MANIFEST.json`?)
      2. **Eingabeliste** bilden - Kursdateien plus die Liste (TB-47)
      3. **Teilkerzen-Pruefung ueber die QUELLE** - findet sie etwas, ist
         hier Schluss (TB-47)
      4. `datenstand_hash` bilden und gegen den verankerten Wert stellen
      5. Inhalts-Hashes der Eingaben bilden -> `snapshot_hash`, der **Name**
      6. Ziel pruefen (existiert? liegt es in der Quelle?)
      7. kopieren, Zeitstempel erhalten
      8. **jede Datei byteweise** gegen ihre Herkunft
      9. `datenstand_hash` der Kopie gegen den der Quelle
     10. Manifest schreiben

    ⚠️ Schritt 3 und 4 stehen **vor** Schritt 7. Ein Snapshot, der erst
    gezogen und dann verworfen wird, hat den Ordner schon angelegt; ein
    Snapshot, der gar nicht erst beginnt, hinterlaesst nichts.

    Schritt 8 und 9 sind nicht dasselbe. Schritt 9 vergleicht den
    **registrierten** Hash, und der zaehlt nur `*.csv` auf der obersten Ebene -
    eine beschaedigt angekommene Symbolliste geht dort nicht ein. Schritt 8
    prueft **jede** Datei, unabhaengig von Endung und Ordner, und zwar
    zweimal: ueber die Quersumme und byteweise.
    """
    wurzel = wurzel or BASE_DIR
    dateien, kursdateien = _pruefe_quelle(quelle)
    liste = eingabeliste(quelle, wurzel, eingaben)

    # ⚠️ Vor allem anderen: findet die Teilkerzen-Pruefung einen Befund, der
    # NICHT unter die Ausnahme aus Registertext 5a, Zusatz faellt, wird nicht
    # gezogen. Sie laeuft ueber die Quelle, nicht ueber die Kopie.
    #
    # ⚠️ TB-49: geprueft wird `nicht_zugelassen`, nicht `befunde`. Die
    # Pruefung schlaegt weiterhin an und meldet weiterhin jeden Befund; was
    # sich geaendert hat, ist allein, welcher Befund das Ziehen verhindert.
    # Es gibt **keine** Option, die diese Stelle uebergeht.
    kerzen = teilkerzen(quelle, zeitabdeckung)
    if kerzen["nicht_zugelassen"]:
        offen = kerzen["nicht_zugelassen"]
        zeilen = []
        for eintrag in offen[:8]:
            zeilen.append("%s (%s)" % (
                eintrag["datei"],
                "; ".join(g["grund"] for g in eintrag["gruende"][:2])))
        namen = ", ".join(zeilen)
        if len(offen) > 8:
            namen += " und %d weitere" % (len(offen) - 8)
        raise Snapshotfehler(
            "Die Teilkerzen-Pruefung hat %d Datei(en) mit einem Befund "
            "gefunden, den Registertext 5a, Zusatz (%s) NICHT zulaesst: %s. "
            "Es wird NICHT gezogen - ein Snapshot haelt einen Bestand fest, "
            "und ein Bestand mit unvollstaendigen Kerzen ist nicht der, den "
            "er zu sein scheint. (Zugelassen waren daneben %d Befund(e).)"
            % (len(offen), REGISTERVERWEIS["fundstelle"], namen,
               kerzen["zugelassen_anzahl"]))

    hash_, anzahl = gesamthash(quelle, herkunft)

    if anzahl != len(kursdateien):
        # Kann nur eintreten, wenn sich der Ordner zwischen zwei Blicken
        # aendert. Dann ist der Hash nicht der des kopierten Bestandes.
        raise Snapshotfehler(
            "Die Quelle hat sich waehrend des Laufs geaendert: %d Kursdateien "
            "gezaehlt, %d im Hash." % (len(kursdateien), anzahl))

    if anker and (hash_ != VERANKERTER_DATENSTAND
                  or anzahl != VERANKERTE_KURSDATEIEN):
        raise Snapshotfehler(
            "Der datenstand_hash der Quelle weicht vom verankerten Wert ab: "
            "%s... / %d statt %s... / %d. Das ist die Tatsachennotiz vom "
            "15.09.2026 - ein Snapshot auf einem anderen Bestand ist ein "
            "anderer Lauf. (Mit --kein-anker fuer Wegwerf-Verzeichnisse.)"
            % (hash_[:16], anzahl, VERANKERTER_DATENSTAND[:16],
               VERANKERTE_KURSDATEIEN))

    # Der zweite Hash: er laeuft ueber die DATEIEN und ist der Name.
    paare = {}
    for eintrag in liste:
        paare[eintrag["im_snapshot"]] = quersumme(eintrag["herkunft"])
    name_ = snapshot_hash(paare)

    ziel = _pruefe_ziel(quelle, ziel_basis, name_)

    bericht = {
        "werkzeug": WERKZEUG,
        "zeitpunkt_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "quelle": os.path.realpath(quelle),
        "wurzel": os.path.realpath(wurzel),
        "ziel": os.path.realpath(ziel) if wirklich else ziel,
        "snapshot_hash": name_,
        "datenstand_hash": hash_,
        "kursdateien": anzahl,
        "dateien_gesamt": len(liste),
        "eingaben": sorted(e["im_snapshot"] for e in liste
                           if e["art"] == "Eingabe"),
        "eingabeliste": liste,
        "teilkerzen": kerzen,
        "gezogen": False,
        "trockenlauf": not wirklich,
    }

    if not wirklich:
        bericht["hinweis"] = ("Trockenlauf - es wurde nichts kopiert. "
                              "Mit --ziehen wird wirklich gezogen.")
        return bericht

    os.makedirs(ziel, exist_ok=False)
    eintraege = {}
    try:
        for eintrag in sorted(liste, key=lambda e: e["im_snapshot"]):
            name = eintrag["im_snapshot"]
            q_pfad = eintrag["herkunft"]
            z_pfad = os.path.join(ziel, name.replace("/", os.sep))
            unterordner = os.path.dirname(z_pfad)
            if unterordner and not os.path.isdir(unterordner):
                os.makedirs(unterordner, exist_ok=True)
            try:
                shutil.copy2(q_pfad, z_pfad)      # copy2: Zeitstempel bleiben
            except OSError as fehler:
                raise Snapshotfehler("%s laesst sich nicht kopieren: %s"
                                     % (name, fehler))
            summe_quelle = quersumme(q_pfad)
            summe_kopie = quersumme(z_pfad)
            if summe_quelle != summe_kopie:
                raise Snapshotfehler(
                    "ABWEICHUNG bei %s: die Kopie stimmt nicht mit der Quelle "
                    "ueberein (%s gegen %s)."
                    % (name, summe_quelle[:16], summe_kopie[:16]))
            if not _byteweise_gleich(q_pfad, z_pfad):
                raise Snapshotfehler(
                    "ABWEICHUNG bei %s: byteweiser Vergleich mit der Quelle "
                    "fehlgeschlagen." % name)
            eintraege[name] = {
                "sha256": summe_kopie,
                "bytes": os.path.getsize(z_pfad),
                "im_datenstand": name.endswith(".csv") and "/" not in name,
                "art": eintrag["art"],
            }

        kopie_hash, kopie_anzahl = gesamthash(ziel, herkunft)
        if kopie_hash != hash_ or kopie_anzahl != anzahl:
            raise Snapshotfehler(
                "Der datenstand_hash der Kopie weicht vom Hash der Quelle ab "
                "(%s... / %d gegen %s... / %d)."
                % (kopie_hash[:16], kopie_anzahl, hash_[:16], anzahl))

        # ⚠️ Und der Name gegen die Kopie: der Ordner muss heissen, was in
        # ihm liegt.
        kopie_paare = {n: e["sha256"] for n, e in eintraege.items()}
        if snapshot_hash(kopie_paare) != name_:
            raise Snapshotfehler(
                "Der snapshot_hash der Kopie weicht vom Namen des Ordners ab.")

        bericht["dateien"] = eintraege
        bericht["bytes_gesamt"] = sum(e["bytes"] for e in eintraege.values())
        schreibe_manifest(ziel, bericht)
        bericht["gezogen"] = True
    except Exception:
        # ⚠️ Ein halb gezogener Snapshot ist schlimmer als keiner: er sieht
        # wie ein Snapshot aus und traegt einen Hash, den sein Inhalt nicht
        # erfuellt. Er wird entfernt - und zwar nur er, nie die Quelle.
        shutil.rmtree(ziel, ignore_errors=True)
        raise
    return bericht


def _byteweise_gleich(a, b, block=1 << 20):
    """Zwei Dateien Block fuer Block vergleichen.

    Zusaetzlich zur Quersumme, nicht an ihrer Stelle: die Quersumme prueft,
    ob der Inhalt derselbe ist, dieser Vergleich prueft es ein zweites Mal
    auf einem anderen Weg. Bei 202 MB kostet das wenig und ist der einzige
    Schritt, der ohne die Annahme auskommt, dass SHA-256 hier stimmt.
    """
    try:
        with open(a, "rb") as fa, open(b, "rb") as fb:
            while True:
                ba, bb = fa.read(block), fb.read(block)
                if ba != bb:
                    return False
                if not ba:
                    return True
    except OSError as fehler:
        raise Snapshotfehler("Vergleich %s / %s nicht moeglich: %s"
                             % (a, b, fehler))


def schreibe_manifest(ordner, bericht):
    """Das Manifest in den Snapshot legen - erst vorlaeufig, dann umbenannt.

    `os.replace` ist atomar: es gibt kein halb geschriebenes Manifest, das
    beim Nachpruefen als "beschaedigt" erscheint, obwohl nur der Schreibvorgang
    unterbrochen wurde.
    """
    inhalt = {
        "werkzeug": bericht["werkzeug"],
        "zeitpunkt_utc": bericht["zeitpunkt_utc"],
        "quelle": bericht["quelle"],
        "wurzel": bericht.get("wurzel"),
        # ⚠️ Zwei Hashes, zwei unverwechselbare Feldnamen. Das frueher
        # einzelne Feld `datenstand` hiess wie die Sache, die es misst, und
        # nicht wie die Frage, die es beantwortet - neben einem zweiten Hash
        # waere das nicht mehr unterscheidbar gewesen.
        "snapshot_hash": bericht["snapshot_hash"],
        "datenstand_hash": bericht["datenstand_hash"],
        "kursdateien": bericht["kursdateien"],
        "dateien_gesamt": bericht["dateien_gesamt"],
        "bytes_gesamt": bericht.get("bytes_gesamt"),
        "verfahren": {
            "snapshot_hash": (
                "shared/snapshot.py::snapshot_hash - SHA-256 ueber die "
                "sortierten (Pfad, Inhalts-Hash)-Paare DER DATEIEN. Laeuft "
                "NICHT ueber das Manifest: ein zusaetzliches Feld ergaebe "
                "sonst einen anderen Namen fuer denselben Inhalt."),
            "datenstand_hash": (
                "research/vorregistrierung/herkunft.py::datenstand - "
                "SHA-256 ueber die *.csv direkt im Ordner, sortiert, "
                "je Datei Name + Groesse + SHA-256 des Inhalts"),
        },
        # ⚠️ Die Liste, nach der aufgenommen wurde - mitgefuehrt, damit
        # spaeter niemand eine Regel auslegen muss.
        "eingabeliste": bericht["eingabeliste"],
        "teilkerzen": bericht["teilkerzen"],
        # ⭐ TB-49: Der Snapshot dokumentiert selbst, was bei seiner Erzeugung
        # erlaubt wurde - und worauf sich die Erlaubnis stuetzt. Ein Pruefer
        # muss das lesen koennen, ohne `snapshot.py` zu kennen. Die Felder
        # stehen eigens auf oberster Ebene und nicht nur im Ergebnis der
        # Pruefung: was erlaubt wurde, ist eine Aussage des Snapshots, nicht
        # eine Beobachtung der Pruefung.
        "zugelassene_befunde": bericht["teilkerzen"].get("zugelassen", []),
        "zugelassene_befunde_anzahl": bericht["teilkerzen"].get(
            "zugelassen_anzahl", 0),
        "zugelassene_befunde_herkunft": REGISTERVERWEIS,
        "dateien": bericht["dateien"],
    }
    pfad = os.path.join(ordner, MANIFEST)
    vorlaeufig = pfad + ".neu"
    try:
        with open(vorlaeufig, "w", encoding="utf-8") as datei:
            json.dump(inhalt, datei, indent=2, ensure_ascii=False,
                      sort_keys=True)
            datei.write("\n")
        os.replace(vorlaeufig, pfad)
    except OSError as fehler:
        raise Snapshotfehler("Manifest %s nicht schreibbar: %s"
                             % (pfad, fehler))
    return pfad


# ===========================================================================
# Teil 3 - Nachpruefen
# ===========================================================================

def _lies_manifest(ordner):
    """Das Manifest lesen - oder sagen, warum es nicht geht."""
    pfad = os.path.join(ordner, MANIFEST)
    if not os.path.isdir(ordner):
        return None, "%s ist kein Verzeichnis." % ordner
    if not os.path.exists(pfad):
        return None, ("%s fehlt - dieser Ordner ist kein Snapshot dieses "
                      "Werkzeugs." % pfad)
    try:
        with open(pfad, "r", encoding="utf-8") as datei:
            manifest = json.load(datei)
    except (OSError, ValueError) as fehler:
        return None, "%s ist nicht lesbar oder beschaedigt: %s" % (pfad, fehler)
    if not isinstance(manifest, dict):
        return None, "%s enthaelt kein Manifest-Objekt." % pfad
    for schluessel in ("dateien", "datenstand_hash", "snapshot_hash",
                       "kursdateien"):
        if schluessel not in manifest:
            return None, ("%s ist beschaedigt: der Eintrag `%s` fehlt."
                          % (pfad, schluessel))
    if not isinstance(manifest["dateien"], dict) or not manifest["dateien"]:
        return None, ("%s ist beschaedigt: `dateien` ist leer oder kein "
                      "Objekt." % pfad)
    return manifest, None


def pruefen(ordner, herkunft=None):
    """Manifest gegen Ordner. Drei Ausgaenge, nie zwei.

    ⚠️ Geprueft wird in **beide** Richtungen. Nur die Manifesteintraege
    durchzugehen wuerde eine **hinzugefuegte** Datei nie finden - und genau
    eine hinzugefuegte Datei ist es, die den Datenstand-Hash aendert, ohne
    dass eine bekannte Datei sich ruehrt. Das ist der Fall, gegen den
    `research/etf_trendfolge/datenstand.py` Wache haelt.
    """
    manifest, grund = _lies_manifest(ordner)
    if manifest is None:
        return {"ausgang": UNPRUEFBAR, "grund": grund, "ordner": ordner,
                "abweichungen": []}

    abweichungen = []
    erwartet = manifest["dateien"]

    # ⚠️ `os.walk`, nicht `os.listdir`: seit TB-47 liegen Eingaben in
    # Unterordnern (`config/…`). Ein `listdir` sieht sie nicht - und eine
    # dort veraenderte Datei fiele damit durch beide Richtungen.
    try:
        vorhanden = []
        for wurzel_, unter, dateien_ in os.walk(ordner):
            for d in dateien_:
                vorhanden.append(_relativ(os.path.join(wurzel_, d), ordner))
        vorhanden.sort()
    except OSError as fehler:
        return {"ausgang": UNPRUEFBAR, "ordner": ordner, "abweichungen": [],
                "grund": "%s ist nicht lesbar: %s" % (ordner, fehler)}

    # Richtung 1: was das Manifest kennt
    for name in sorted(erwartet):
        eintrag = erwartet[name]
        pfad = os.path.join(ordner, name.replace("/", os.sep))
        if not os.path.exists(pfad):
            abweichungen.append({"datei": name, "art": "entfernt"})
            continue
        try:
            ist = quersumme(pfad)
        except Snapshotfehler as fehler:
            # Nicht als "veraendert" verbuchen: ob sie sich geaendert hat,
            # ist gerade NICHT feststellbar.
            return {"ausgang": UNPRUEFBAR, "ordner": ordner,
                    "abweichungen": abweichungen, "grund": str(fehler)}
        if ist != eintrag.get("sha256"):
            abweichungen.append({"datei": name, "art": "veraendert",
                                 "soll": eintrag.get("sha256"), "ist": ist})
            continue
        groesse = os.path.getsize(pfad)
        if eintrag.get("bytes") is not None and groesse != eintrag["bytes"]:
            abweichungen.append({"datei": name, "art": "andere Groesse",
                                 "soll": eintrag["bytes"], "ist": groesse})

    # Richtung 2: was im Ordner liegt, aber nicht im Manifest steht
    for name in vorhanden:
        if name == MANIFEST or name == MANIFEST + ".neu":
            continue
        if name not in erwartet:
            abweichungen.append({"datei": name, "art": "hinzugefuegt"})

    # Der Gesamthash zum Schluss - er ist die Aussage, auf die es ankommt.
    try:
        ist_hash, ist_anzahl = gesamthash(ordner, herkunft)
    except Snapshotfehler as fehler:
        return {"ausgang": UNPRUEFBAR, "ordner": ordner,
                "abweichungen": abweichungen, "grund": str(fehler)}

    if ist_hash != manifest["datenstand_hash"]:
        abweichungen.append({"datei": "(datenstand_hash)", "art": "veraendert",
                             "soll": manifest["datenstand_hash"],
                             "ist": ist_hash})
    if ist_anzahl != manifest["kursdateien"]:
        abweichungen.append({"datei": "(Dateizahl)", "art": "veraendert",
                             "soll": manifest["kursdateien"],
                             "ist": ist_anzahl})

    # ⚠️ Und der zweite Hash - der ueber die Dateien. Er ist die Aussage
    # "derselbe Eingabesatz", und er faellt bei einer veraenderten
    # Nicht-Kursdatei an, wo der datenstand_hash schweigt.
    ist_snapshot = None
    try:
        paare = {}
        for name in sorted(erwartet):
            pfad = os.path.join(ordner, name.replace("/", os.sep))
            if os.path.exists(pfad):
                paare[name] = quersumme(pfad)
        for name in vorhanden:
            if name in (MANIFEST, MANIFEST + ".neu") or name in erwartet:
                continue
            paare[name] = quersumme(os.path.join(ordner,
                                                 name.replace("/", os.sep)))
        ist_snapshot = snapshot_hash(paare) if paare else None
    except Snapshotfehler as fehler:
        return {"ausgang": UNPRUEFBAR, "ordner": ordner,
                "abweichungen": abweichungen, "grund": str(fehler)}

    if ist_snapshot != manifest["snapshot_hash"]:
        abweichungen.append({"datei": "(snapshot_hash)", "art": "veraendert",
                             "soll": manifest["snapshot_hash"],
                             "ist": ist_snapshot})

    return {
        "ausgang": VERAENDERT if abweichungen else UNVERAENDERT,
        "ordner": ordner,
        "grund": None,
        "snapshot_soll": manifest["snapshot_hash"],
        "snapshot_ist": ist_snapshot,
        "datenstand_soll": manifest["datenstand_hash"],
        "datenstand_ist": ist_hash,
        "kursdateien_soll": manifest["kursdateien"],
        "kursdateien_ist": ist_anzahl,
        "abweichungen": abweichungen,
    }


# ===========================================================================
# Teil 4 - Befehlszeile
# ===========================================================================

def _drucke_pruefung(b):
    print("Snapshot nachpruefen: %s\n" % b["ordner"])
    if b["ausgang"] == UNPRUEFBAR:
        print("  NICHT PRUEFBAR")
        print("  %s" % b["grund"])
        return
    print("  snapshot_hash    Soll %s" % b["snapshot_soll"])
    print("                   Ist  %s" % b["snapshot_ist"])
    print("  datenstand_hash  Soll %s  (%d Kursdateien)"
          % (b["datenstand_soll"], b["kursdateien_soll"]))
    print("                   Ist  %s  (%d Kursdateien)"
          % (b["datenstand_ist"], b["kursdateien_ist"]))
    if b["ausgang"] == UNVERAENDERT:
        print("\n  UNVERAENDERT")
        return
    print("\n  VERAENDERT - %d Abweichung(en):" % len(b["abweichungen"]))
    for a in b["abweichungen"]:
        zusatz = ""
        if a.get("soll") is not None:
            zusatz = "  (soll %s, ist %s)" % (str(a["soll"])[:16],
                                              str(a["ist"])[:16])
        print("    %-40s %s%s" % (a["datei"], a["art"], zusatz))


def _drucke_ziehen(b):
    print("Snapshot ziehen\n")
    print("  Quelle           %s" % b["quelle"])
    print("  Wurzel           %s" % b.get("wurzel"))
    print("  snapshot_hash    %s   ⭐ der Name" % b["snapshot_hash"])
    print("  datenstand_hash  %s" % b["datenstand_hash"])
    print("  Kursdateien      %d   (Dateien gesamt: %d)"
          % (b["kursdateien"], b["dateien_gesamt"]))
    if b["eingaben"]:
        print("  Weitere Eingaben (aus der Liste im Manifest):")
        for e in b["eingaben"]:
            print("      %s" % e)
    else:
        print("  ⚠️ Die Eingabeliste ist leer - nur Kursdateien.")
    k = b["teilkerzen"]
    if k["frei_von_teilkerzen"]:
        print("  Teilkerzen       keine (%d Datei(en) geprueft)"
              % k["dateien_geprueft"])
    else:
        print("  ⚠️ Teilkerzen     %d Datei(en) mit Befund (%d Datei(en) "
              "geprueft)" % (len(k["befunde"]), k["dateien_geprueft"]))
        print("      davon zugelassen   %d Befund(e) in %d Datei(en) - %s"
              % (k.get("zugelassen_anzahl", 0),
                 k.get("zugelassen_dateien", 0),
                 k.get("ausnahme", {}).get("fundstelle", "?")))
        offen = k.get("nicht_zugelassen") or []
        if offen:
            print("      ⚠️ NICHT zugelassen %d Datei(en):" % len(offen))
            for eintrag in offen[:8]:
                print("          %s - %s" % (
                    eintrag["datei"],
                    "; ".join(g["grund"] for g in eintrag["gruende"][:2])))
        else:
            print("      ⚠️ Die Pruefung schlaegt weiter an - gezogen wird "
                  "gegen den Registereintrag, nicht gegen ihr Schweigen.")
    print("  Ziel             %s" % b["ziel"])
    if b["gezogen"]:
        print("\n  GEZOGEN - %d Datei(en), %.1f MB, jede byteweise gegen die "
              "Quelle geprueft." % (len(b["dateien"]),
                                    b["bytes_gesamt"] / 1e6))
        print("  Manifest    %s" % os.path.join(b["ziel"], MANIFEST))
    else:
        print("\n  TROCKENLAUF - nichts kopiert. Mit --ziehen wirklich ziehen.")


def main(argv=None) -> int:
    z = argparse.ArgumentParser(
        description="Zieht einen unveraenderlichen Kursdaten-Snapshot und "
                    "prueft ihn nach (TB-46, Registertext 5).")
    z.add_argument("--quelle", default=os.path.join(BASE_DIR, "data"),
                   help="der Bestand, der kopiert wird (Standard: data/)")
    z.add_argument("--ziel", default=os.path.join(BASE_DIR, "snapshots"),
                   help="der Ordner, in dem <hash>/ entsteht")
    z.add_argument("--ziehen", action="store_true",
                   help="wirklich kopieren (ohne dies: Trockenlauf)")
    z.add_argument("--pruefen", metavar="ORDNER", default=None,
                   help="einen vorhandenen Snapshot gegen sein Manifest pruefen")
    z.add_argument("--nur-hash", action="store_true",
                   help="nur den Datenstand-Hash der Quelle ausgeben")
    z.add_argument("--wurzel", default=BASE_DIR,
                   help="Wurzel, auf die sich die Eingabeliste bezieht "
                        "(Standard: das Projektverzeichnis)")
    z.add_argument("--eingabe", action="append", default=None, metavar="PFAD",
                   help="ein Eintrag der Eingabeliste, relativ zur Wurzel "
                        "(mehrfach angebbar). Ohne Angabe gilt die in "
                        "snapshot.py hinterlegte Liste EINGABEN.")
    z.add_argument("--kein-anker", action="store_true",
                   help="den verankerten datenstand_hash NICHT erzwingen - "
                        "nur fuer Wegwerf-Verzeichnisse in Selbsttests")
    z.add_argument("--json", metavar="PFAD", default=None)
    a = z.parse_args(argv)

    if a.eingabe is None:
        eingaben = EINGABEN
    else:
        eingaben = tuple({"pfad": p, "rolle": "per --eingabe angegeben",
                          "leser": "(Befehlszeile)"} for p in a.eingabe)

    try:
        if a.pruefen:
            bericht = pruefen(a.pruefen)
            _drucke_pruefung(bericht)
            rueckgabe = {UNVERAENDERT: OK, VERAENDERT: BEFUND,
                         UNPRUEFBAR: NICHT_PRUEFBAR}[bericht["ausgang"]]
        elif a.nur_hash:
            hash_, anzahl = gesamthash(a.quelle)
            bericht = {"quelle": os.path.realpath(a.quelle),
                       "datenstand": hash_, "kursdateien": anzahl}
            print("%s  (%d Kursdateien)  %s" % (hash_, anzahl, a.quelle))
            rueckgabe = OK
        else:
            bericht = ziehen(a.quelle, a.ziel, wirklich=a.ziehen,
                             wurzel=a.wurzel, eingaben=eingaben,
                             anker=not a.kein_anker)
            _drucke_ziehen(bericht)
            rueckgabe = OK
    except Snapshotfehler as fehler:
        print("ABBRUCH: %s" % fehler, file=sys.stderr)
        if a.json:
            _schreibe_json(a.json, {"abgebrochen": True, "grund": str(fehler)})
        return NICHT_PRUEFBAR

    if a.json:
        _schreibe_json(a.json, bericht)
        print("\nJSON: %s" % a.json)
    return rueckgabe


def _schreibe_json(pfad, inhalt):
    ordner = os.path.dirname(os.path.abspath(pfad))
    if ordner:
        os.makedirs(ordner, exist_ok=True)
    with open(pfad, "w", encoding="utf-8") as datei:
        json.dump(inhalt, datei, indent=2, ensure_ascii=False, sort_keys=True)
        datei.write("\n")


if __name__ == "__main__":
    sys.exit(main())
