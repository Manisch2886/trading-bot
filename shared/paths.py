"""
Pfad-Konfiguration fuer gemeinsam genutzte Skripte
======================================================
Fuer Skripte, die in shared/ liegen und von JEDER Strategie genutzt
werden koennen (Datenabruf, Symbol-Liste). Diese Skripte kennen keine
einzelne Strategie, daher gibt es hier nur die projektweiten,
gemeinsamen Ordner - keine strategie-spezifischen Pfade.

---------------------------------------------------------------------------
Der Selektionsmodus (TB-52, Backlog T46.3 Schicht 1)
---------------------------------------------------------------------------
⚠️ **Ohne gesetzten Modus verhaelt sich dieses Modul Zeile fuer Zeile wie
vorher.** Diese Bedingung ist gemessen, nicht behauptet - siehe
`shared/test_paths.py`, Probe A, und `docs/ERGEBNIS_TB-52_resolver.md`:
**99 Pfade ueber neun Bots, 0 Unterschiede.**

⚠️ **Wie weit dieses Modul reicht - drei Zahlen, drei Fragen** (Prueffrage C7;
am Syntaxbaum nachgemessen 18.09.2026, TB-52):

    10   Module importieren `paths` DIREKT - es sind die Abruf- und
         Symbolskripte (`fetch_*`, `get_top_symbols`, `symbols_config`, ...),
         also die SCHREIBENDE Seite. Sie laufen im Cron.
   163   Module sind TRANSITIV betroffen, ganz ueberwiegend ueber
         `shared/symbols_config.py`.
   145   ist die Zahl aus `research/datenordner_schnitt`
         (`beziehen_zentral`) - ⚠️ sie zaehlt Module, die ihre Pfade aus
         EINER der beiden zentralen Quellen beziehen, also weit ueberwiegend
         aus `strategy_paths.py`. Sie ist **nicht** die Zahl der Importe
         dieses Moduls.

⚠️ Mehrere stehende Texte (`CLAUDE.md`, `ARBEITSWEISE.md` §7, Backlog T46.3)
sagen *"von 145 Modulen importiert"*. **Das ist eine Verwechslung dieser drei
Fragen.** Die Vorsicht bleibt berechtigt - 163 transitiv Betroffene und der
Cron sind Grund genug -, aber die Begruendung gehoert berichtigt.

**Wozu der Modus da ist.** Ein Selektionslauf soll aus einem eingefrorenen
Snapshot lesen, nicht aus dem lebenden Bestand. Der naheliegende Weg - jedes
lesende Modul eine Wurzel uebergeben zu lassen - hat ein Loch:

    "Die Wache prueft die Eingabe, nicht das Verhalten."
    Ein Modul, das seinen Pfad selbst baut, sieht eine uebergebene Wurzel nie.

Der Modus schliesst dieses Loch an der Quelle: wer `DATA_DIR` erfragt,
bekommt unter dem Modus die Snapshot-Wurzel - ohne etwas davon zu wissen.

**Wie er gesetzt wird: ueber zwei Umgebungsvariablen.**

    TB_SELEKTIONSWURZEL   absoluter Pfad zur Snapshot-Wurzel
    TB_SELEKTIONSHASH     der erwartete `snapshot_hash` aus deren MANIFEST.json

⚠️ **Warum Umgebungsvariablen und nicht ein Aufruf im Prozess.** Der
Selektionslauf startet **einen Prozess je Bot** (TB-40: neun gleichnamige
`equity_simulation.py` verdecken sich sonst in `sys.modules`). Ein
prozesslokaler Modus wird nicht vererbt - ein Kindprozess, der ihn nicht
erbt, liest **still** aus dem Live-Bestand. Das waere genau die Ausfallform,
gegen die diese Schicht gebaut wird, nur eine Ebene tiefer. Die
Umgebungsvariable wird von Kindprozessen von sich aus geerbt.

⚠️ **Der Preis dieses Wegs: der Modus kann aus einer frueheren Shell
uebrigbleiben.** Drei Dinge halten dagegen - keines davon ist eine
Umgehungsflagge:

  1. **Der Modus traegt den Snapshot-Hash, nicht nur "an/aus".** Ein
     uebriggebliebener Modus zeigt damit auf einen *benannten* Zustand. Ein
     Kindprozess, der einen **anderen** Hash erbt als der Snapshot traegt,
     wirft - statt still danebenzugreifen.
  2. **Zeigt der Modus ins Leere, wirft er sofort beim Import.** Ein Modus,
     der auf einen fehlenden Snapshot zeigt, ist schlimmer als keiner.
  3. ⭐ **Ein Lauf unter dem Modus SAGT es** - eine Zeile auf `stderr`, bei
     jedem Import (Prueffrage D1: *"Ein Lauf, der ein Symbol auslaesst, sagt
     es. Immer."*). Ein uebriggebliebener Modus in einem Cron-Lauf
     hinterlaesst damit eine Spur im Bot-Protokoll, statt stumm zu bleiben.

⚠️ **Was dennoch offen bleibt, benannt statt verschwiegen:** Steht der Modus
in einer Datei, die ein Cron-Lauf selbst einliest (Crontab-Zeile, ein von
dort gesourctes Profil), dann rechnet dieser Lauf gegen den Snapshot. Er
sagt es dann (Punkt 3), aber niemand wird gehindert. Der Nachweis, dass der
echte Cron den Modus nicht traegt, gehoert auf den Betriebsrechner und steht
im Mac-Testauftrag zu TB-52.

**Die beiden Namen fuer die beiden Fragen** (Prueffrage C7):

    DATA_DIR        Kursdaten. Ohne Modus: der Live-Bestand. Mit Modus: die
                    Snapshot-Wurzel.
    LIVE_DATA_DIR   ausdruecklich der Live-Bestand. Ohne Modus derselbe Wert.
                    ⚠️ **Mit Modus wirft er** - mit einer Meldung, die sagt,
                    welches Modul gefragt hat und was es haette fragen sollen.

Dasselbe Paar fuer `CONFIG_DIR` / `LIVE_CONFIG_DIR`. Die Snapshot-Wurzel ist
flach: die Symbollisten (`top25_symbols.txt`, `sp500_top150.txt`) liegen dort
neben den Kursdateien, deshalb zeigen unter dem Modus beide dorthin.

`SHARED_DIR` und `BASE_DIR` bezeichnen **Code**, nicht Daten, und aendern
sich unter dem Modus nicht.
"""

import os

SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SHARED_DIR)

_LIVE_DATA_DIR = os.path.join(BASE_DIR, "data")      # Kursdaten - von allen Strategien nutzbar
_LIVE_CONFIG_DIR = os.path.join(BASE_DIR, "config")  # Symbol-Liste, E-Mail-Zugangsdaten

# ⚠️ T46.8: Frueher standen hier zwei `os.makedirs(..., exist_ok=True)`. Sie
# waren heute harmlos und **still im Fehlerfall**: zeigte die Wurzel
# irgendwann woandershin, entstand dort immer wieder ein leerer `data/`, und
# nichts sagte etwas. Ein Import ist keine Leseoperation (Prueffrage B6) -
# und erst recht keine Schreiboperation. Beide Ordner sind versioniert und
# liegen im Checkout; wer einen davon anlegen muss, tut das ausdruecklich.

# Die Namen der beiden Umgebungsvariablen stehen genau einmal.
UMGEBUNG_WURZEL = "TB_SELEKTIONSWURZEL"
UMGEBUNG_HASH = "TB_SELEKTIONSHASH"

MANIFEST = "MANIFEST.json"


class Selektionsfehler(RuntimeError):
    """Der Selektionsmodus ist gesetzt und die Anfrage passt nicht dazu.

    ⚠️ Eigener Typ, damit ein Aufrufer ihn von einem `OSError` beim Lesen
    unterscheiden kann. Er wird **nicht** abgefangen und in einen
    Rueckfallwert verwandelt - das waere der stille Ausfall, den der Modus
    verhindern soll (Prueffrage D1).
    """


def _fragendes_modul():
    """Datei und Zeile des ersten Rahmens ausserhalb dieses Moduls.

    ⚠️ Ohne diese Angabe waere die Meldung wertlos: Der Modus wirft an einer
    Stelle, die viele Module gemeinsam benutzen - die Meldung muss sagen,
    **wer** gefragt hat, sonst sucht jemand im falschen Modul.
    """
    import sys
    rahmen = sys._getframe(1)
    hier = os.path.abspath(__file__)
    while rahmen is not None:
        datei = rahmen.f_code.co_filename
        if os.path.abspath(datei) != hier and "importlib" not in datei:
            return "%s:%d" % (datei, rahmen.f_lineno)
        rahmen = rahmen.f_back
    return "unbekannt"


def _lies_snapshot_hash(wurzel):
    """Den `snapshot_hash` aus dem Manifest der Wurzel - oder werfen.

    ⚠️ Hier wird **nicht** `shared/snapshot.py` importiert. Der Modus muss in
    jedem importierenden Modul tragen, auch in denen, die `snapshot`
    nie laden; eine zusaetzliche Abhaengigkeit an dieser Stelle waere ein
    neuer Weg, auf dem der Import fehlschlagen kann.
    """
    import json
    pfad = os.path.join(wurzel, MANIFEST)
    if not os.path.isdir(wurzel):
        raise Selektionsfehler(
            "%s ist auf %s gesetzt, aber das ist kein Verzeichnis. Ein Modus, "
            "der auf einen fehlenden Snapshot zeigt, ist schlimmer als keiner."
            % (UMGEBUNG_WURZEL, wurzel))
    if not os.path.exists(pfad):
        raise Selektionsfehler(
            "%s fehlt - %s ist kein Snapshot. Ein Modus, der auf einen "
            "fehlenden Snapshot zeigt, ist schlimmer als keiner."
            % (pfad, wurzel))
    try:
        with open(pfad, "r", encoding="utf-8") as datei:
            manifest = json.load(datei)
    except (OSError, ValueError) as fehler:
        raise Selektionsfehler(
            "%s ist nicht lesbar oder beschaedigt: %s" % (pfad, fehler))
    if not isinstance(manifest, dict) or "snapshot_hash" not in manifest:
        raise Selektionsfehler(
            "%s traegt keinen `snapshot_hash`. Der Modus kann den Snapshot "
            "dann nicht benennen und rechnet nicht blind weiter." % pfad)
    return manifest["snapshot_hash"]


def _modus_aus_umgebung(umgebung=None):
    """(wurzel, hash) - oder None, wenn kein Modus gesetzt ist.

    ⚠️ **Beide** Variablen muessen stehen. Eine allein ist kein halber Modus,
    sondern ein Fehler: die Wurzel ohne Hash koennte auf irgendeinen Ordner
    zeigen, der Hash ohne Wurzel bezeichnet nichts.
    """
    umg = os.environ if umgebung is None else umgebung
    wurzel = (umg.get(UMGEBUNG_WURZEL) or "").strip()
    erwartet = (umg.get(UMGEBUNG_HASH) or "").strip()
    if not wurzel and not erwartet:
        return None
    if not wurzel or not erwartet:
        fehlt = UMGEBUNG_WURZEL if not wurzel else UMGEBUNG_HASH
        gesetzt = UMGEBUNG_HASH if not wurzel else UMGEBUNG_WURZEL
        raise Selektionsfehler(
            "%s ist gesetzt, %s fehlt. Der Selektionsmodus braucht beide: die "
            "Wurzel sagt WO, der Hash sagt WELCHER Snapshot. Eine allein ist "
            "kein halber Modus." % (gesetzt, fehlt))
    wurzel = os.path.abspath(wurzel)
    gefunden = _lies_snapshot_hash(wurzel)
    if gefunden != erwartet:
        raise Selektionsfehler(
            "Der Snapshot in %s traegt den Hash %s, %s nennt aber %s. Das ist "
            "ein anderer Eingabesatz als der verlangte - hier wird nicht "
            "weitergerechnet."
            % (wurzel, gefunden, UMGEBUNG_HASH, erwartet))
    return wurzel, erwartet


def selektionsmodus():
    """(wurzel, hash) des aktiven Modus, sonst None. Nur zum Nachsehen."""
    return _MODUS


_MODUS = _modus_aus_umgebung()

if _MODUS is None:
    # ⭐ Der Regelfall, und der Cron-Fall. Vier gewoehnliche Modulglobale,
    # genau die Werte von vorher. `__getattr__` unten wird nie erreicht.
    DATA_DIR = _LIVE_DATA_DIR
    CONFIG_DIR = _LIVE_CONFIG_DIR
    LIVE_DATA_DIR = _LIVE_DATA_DIR
    LIVE_CONFIG_DIR = _LIVE_CONFIG_DIR
else:
    # Unter dem Modus zeigen die beiden gewoehnlichen Namen in den Snapshot.
    DATA_DIR = _MODUS[0]
    CONFIG_DIR = _MODUS[0]
    # ⚠️ `LIVE_DATA_DIR` und `LIVE_CONFIG_DIR` werden hier **nicht** gesetzt.
    # Genau dadurch greift `__getattr__` (PEP 562) und die Anfrage nach dem
    # Live-Bestand wirft, statt einen Pfad zu liefern.
    import sys as _sys
    _sys.stderr.write(
        "[paths] SELEKTIONSMODUS AKTIV - Kursdaten kommen aus %s "
        "(snapshot_hash %s), nicht aus %s.\n"
        % (_MODUS[0], _MODUS[1], _LIVE_DATA_DIR))
    del _sys


_LIVE_NAMEN = {
    "LIVE_DATA_DIR": ("DATA_DIR", _LIVE_DATA_DIR),
    "LIVE_CONFIG_DIR": ("CONFIG_DIR", _LIVE_CONFIG_DIR),
}


def __getattr__(name):
    """Greift nur unter dem Modus, und nur fuer die beiden LIVE_-Namen.

    ⚠️ PEP 562: Python ruft diese Funktion erst, wenn der Name als Modulglobal
    **nicht** gefunden wurde. Ohne Modus sind alle vier Namen gewoehnliche
    Globale - dieser Zweig wird dort nie betreten. Das ist der Grund, warum
    der Modus den Regelfall nicht anfasst.
    """
    if name in _LIVE_NAMEN and _MODUS is not None:
        stattdessen, wert = _LIVE_NAMEN[name]
        raise Selektionsfehler(
            "%s fragte nach `%s` (%s), waehrend der Selektionsmodus auf den "
            "Snapshot %s zeigt. Unter dem Modus wird nicht aus dem "
            "Live-Bestand gelesen - gefragt werden sollte `%s`, das hier auf "
            "den Snapshot aufloest."
            % (_fragendes_modul(), name, wert, _MODUS[0], stattdessen))
    raise AttributeError("module %r has no attribute %r" % (__name__, name))
