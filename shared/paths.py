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

**Wie er gesetzt wird: ueber Umgebungsvariablen** - zwei seit TB-52, eine
dritte seit TB-58 (Codeherkunft, siehe den Abschnitt unten).

    TB_SELEKTIONSWURZEL   absoluter Pfad zur Snapshot-Wurzel
    TB_SELEKTIONSHASH     der erwartete `snapshot_hash` aus deren MANIFEST.json
    TB_SELEKTIONSCOMMIT   der erwartete Commit der Codewurzel (TB-58)

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

---------------------------------------------------------------------------
Die Startpruefungen (TB-58, Schicht 3)
---------------------------------------------------------------------------
    "Der Lese-Audit beweist, welche DATEN gelesen wurden. Er sagt nichts
     darueber, welcher CODE gelesen hat."

Ein Selektionslauf mit gespaltenem Baum - Aufrufer aus einem Ordner, `shared/`
aus einem anderen - haette ein sauberes Lese-Audit und waere trotzdem nicht
reproduzierbar: kein einzelner Commit beschreibt, was gelaufen ist. Neben der
Datenherkunft (Snapshot-Hash) fehlten die **Codeherkunft** und der **Lock**
(die Umgebung). Beide prueft dieses Modul jetzt - hier, weil der Resolver die
eine Stelle ist, die jeder Prozess durchlaeuft (`basislauf.py` startet einen
Prozess je Bot; die Pruefung greift neunmal).

⚠️⚠️ **Ohne Selektionsmodus passiert davon NICHTS.** Kein `git`-Aufruf, keine
Paketabfrage, kein zusaetzlicher Dateizugriff - `subprocess`,
`importlib.metadata`, `platform` und `hashlib` werden erst **innerhalb** der
Prueffunktionen importiert, und die laufen nur im `else`-Zweig unten. Das ist
gemessen (`shared/test_startpruefungen.py`, Probe N1: eine zaehlende Attrappe
vor dem Import, 0 / 0), nicht behauptet.

**Die dritte Umgebungsvariable:**

    TB_SELEKTIONSCOMMIT   der erwartete Commit der Codewurzel (7-40 Hex-Zeichen)

Dieselbe Bauart wie der Hash: der Modus **traegt** den erwarteten Wert, statt
ihn irgendwo zu suchen; ein Kindprozess erbt ihn und bricht bei Abweichung ab.
⚠️ **Fehlt sie, waehrend die anderen beiden gesetzt sind: Abbruch.** Ein halb
gesetzter Modus ist gefaehrlicher als keiner. ⚠️ Zweignamen (`main`) sind
**nicht** zugelassen - eine bewegliche Referenz beschreibt keinen Zustand
(Prueffrage B3).

**Drei Bedingungen zur Codeherkunft, alle beim Start, alle blockierend:**

  1. Einstiegspunkt (`sys.modules["__main__"].__file__`, ueber `realpath`) und
     diese Datei liegen unter **derselben Git-Wurzel** (`git rev-parse
     --show-toplevel`, beide Seiten ueber `realpath`).
  2. `HEAD` dieser Wurzel **ist** der erwartete Commit.
  3. Der Arbeitsbaum ist **sauber** - `git status --porcelain` ueber
     `ARBEITSBAUM_PFADE` (`shared/`, `strategies/`, die Lock-Datei). *"Ein
     sauberer Commit ueber einem schmutzigen Arbeitsbaum beschreibt den Code so
     wenig wie ein gespaltener Baum."* ⚠️ Nicht der ganze Baum: `data/` ist
     versioniert und wird vom Abruf-Cron laufend veraendert - ein Lauf, der
     aus dem Snapshot liest, darf daran nicht scheitern.

**Die Lock-Pruefung** (`requirements.lock` im Projektwurzelverzeichnis):
`sys.version` und `platform.platform()` gegen die Kopfzeilen, jede
`name==version`-Zeile gegen `importlib.metadata` (nicht `pip`). Bei Abweichung
Abbruch mit den ersten drei abweichenden Paketen. ⚠️ **Nichts wird installiert,
nachgezogen oder repariert** - der Lauf meldet und bricht ab.

**Rueckgabewert bei Verletzung: 2** (`SystemExit`, nicht `Exception` - ein
`except Exception` im Aufrufer faengt ihn nicht, das ist Absicht). Der
`Selektionsfehler` fuer Wurzel/Hash (rc 1, Traceback) bleibt, wie er war.

**Was ein bestandener Lauf hinterlaesst** - "eine Messung, die nur abbricht,
aber nichts hinterlaesst, ist keine Zusicherung": acht Auditzeilen auf
`stderr` in der Form der `[paths] SELEKTIONSMODUS AKTIV`-Zeile, und dieselben
Werte ueber `startpruefung()` (dict) bzw. `audit_zeilen()` (Textzeilen) fuer
das spaetere Lese-Audit.

    codewurzel  commit  arbeitsbaum  lock_sha256  interpreter  plattform
    snapshot_wurzel  snapshot_hash
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
# Die dritte (TB-58): der erwartete Commit der Codewurzel.
UMGEBUNG_COMMIT = "TB_SELEKTIONSCOMMIT"

MANIFEST = "MANIFEST.json"
LOCK = "requirements.lock"

# Rueckgabewert einer gescheiterten Startpruefung. ⚠️ Nicht 1: der ist der
# gewoehnliche Traceback (auch der `Selektionsfehler`), nicht 0: das ist
# "durchgelaufen". Wie bei `snapshot.py` steht der Wert genau einmal.
RUECKGABEWERT_STARTPRUEFUNG = 2

# Worueber der Arbeitsbaum sauber sein muss (Bedingung 3). Der Auftrag sagt
# "mindestens `shared/` und `strategies/`"; die Lock-Datei kommt dazu, weil
# ein veraenderter, nicht eingecheckter Lock genau die Umgebung beschreibt,
# gegen die gleich geprueft wird. ⚠️ `data/` steht absichtlich nicht hier -
# siehe Kopf.
ARBEITSBAUM_PFADE = ("shared", "strategies", LOCK)

# Die Reihenfolge der Auditzeilen (Teil D). Sie steht genau einmal.
AUDIT_SCHLUESSEL = ("codewurzel", "commit", "arbeitsbaum", "lock_sha256",
                    "interpreter", "plattform", "snapshot_wurzel",
                    "snapshot_hash")


class Selektionsfehler(RuntimeError):
    """Der Selektionsmodus ist gesetzt und die Anfrage passt nicht dazu.

    ⚠️ Eigener Typ, damit ein Aufrufer ihn von einem `OSError` beim Lesen
    unterscheiden kann. Er wird **nicht** abgefangen und in einen
    Rueckfallwert verwandelt - das waere der stille Ausfall, den der Modus
    verhindern soll (Prueffrage D1).
    """


class Startpruefungsfehler(Selektionsfehler):
    """Eine der Startpruefungen (Codeherkunft, Lock) ist verletzt (TB-58).

    Die Pruefunktionen werfen diesen Typ; **beim Import** wird er in
    `SystemExit(RUECKGABEWERT_STARTPRUEFUNG)` verwandelt, nachdem die
    Meldung auf `stderr` steht. Wer die Funktionen direkt aufruft (Tests,
    das spaetere Lese-Audit), bekommt den Fehler als Ausnahme.
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
        if (umg.get(UMGEBUNG_COMMIT) or "").strip():
            # ⚠️ TB-58: der Commit allein ist derselbe halbe Modus wie die
            # Wurzel allein - er wird nicht still ignoriert.
            raise Selektionsfehler(
                "%s ist gesetzt, %s und %s fehlen. Ein Commit allein "
                "bezeichnet keinen Snapshot - ein halber Modus ist "
                "gefaehrlicher als keiner."
                % (UMGEBUNG_COMMIT, UMGEBUNG_WURZEL, UMGEBUNG_HASH))
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


# ---------------------------------------------------------------------------
# Die Startpruefungen (TB-58). ⚠️ Nichts hiervon wird ohne Modus aufgerufen;
# alle Importe stehen INNERHALB der Funktionen, damit der Regelfall auch
# keinen Import bezahlt.
# ---------------------------------------------------------------------------

def _git(ordner, *argumente):
    """Ein git-Aufruf in `ordner`; stdout - oder `Startpruefungsfehler`.

    ⚠️ Ein gescheiterter Aufruf ist kein leeres Ergebnis (Prueffrage A1):
    `rc != 0` wird geworfen, nicht als "" weitergereicht.
    """
    import subprocess
    befehl = ["git", "-C", ordner] + list(argumente)
    try:
        lauf = subprocess.run(befehl, capture_output=True, text=True)
    except OSError as fehler:
        raise Startpruefungsfehler(
            "git ist nicht aufrufbar (%s). Ohne git ist die Codeherkunft "
            "nicht pruefbar - und `nicht pruefbar` ist nicht gruen." % fehler)
    if lauf.returncode != 0:
        raise Startpruefungsfehler(
            "`%s` scheiterte (rc %d): %s"
            % (" ".join(befehl), lauf.returncode,
               lauf.stderr.strip() or "keine Meldung"))
    return lauf.stdout


def _einstiegspunkt():
    """Die Datei, mit der dieser Prozess gestartet wurde, ueber `realpath`."""
    import sys
    datei = getattr(sys.modules.get("__main__"), "__file__", None)
    if not datei:
        raise Startpruefungsfehler(
            "Der Einstiegspunkt hat keine Datei (`python -c`, interaktiv oder "
            "Standardeingabe). Ohne Datei gibt es keine Codewurzel, die sich "
            "pruefen liesse - ein Selektionslauf startet aus einer Datei.")
    return os.path.realpath(datei)


def _git_wurzel(pfad):
    """Die Git-Wurzel, unter der `pfad` liegt, ueber `realpath`."""
    ordner = os.path.dirname(pfad) if os.path.isfile(pfad) else pfad
    try:
        wurzel = _git(ordner, "rev-parse", "--show-toplevel")
    except Startpruefungsfehler as fehler:
        raise Startpruefungsfehler(
            "%s liegt in keinem Git-Arbeitsbaum - ohne Wurzel keine "
            "Codeherkunft. (%s)" % (pfad, fehler))
    return os.path.realpath(wurzel.strip())


def _commit_bezeichner(erwartet):
    """Den erwarteten Commit pruefen: 7-40 Hex-Zeichen, kleingeschrieben."""
    wert = erwartet.strip().lower()
    hex_zeichen = set("0123456789abcdef")
    if not (7 <= len(wert) <= 40) or any(z not in hex_zeichen for z in wert):
        raise Startpruefungsfehler(
            "%s=%r ist kein Commit-Bezeichner (7-40 Hex-Zeichen). Zweignamen "
            "und Tags sind bewegliche Referenzen und beschreiben keinen "
            "Zustand (Prueffrage B3)." % (UMGEBUNG_COMMIT, erwartet))
    return wert


def _pruefe_codeherkunft(erwartet, einstiegspunkt=None, hier=None):
    """Die drei Bedingungen aus Teil B; (codewurzel, commit, "sauber").

    ⚠️ Die Reihenfolge ist Absicht: erst der gespaltene Baum (die Meldung
    nennt dann beide Wurzeln), dann der Commit, dann der Arbeitsbaum.
    """
    hier = os.path.realpath(__file__ if hier is None else hier)
    einstieg = _einstiegspunkt() if einstiegspunkt is None else \
        os.path.realpath(einstiegspunkt)
    wurzel_code = _git_wurzel(hier)
    wurzel_einstieg = _git_wurzel(einstieg)
    if wurzel_code != wurzel_einstieg:                      # Bedingung 1
        raise Startpruefungsfehler(
            "Gespaltener Baum: der Einstiegspunkt %s liegt unter %s, dieses "
            "`paths.py` (%s) unter %s. Kein einzelner Commit beschreibt, was "
            "hier laufen wuerde." % (einstieg, wurzel_einstieg, hier, wurzel_code))
    soll = _commit_bezeichner(erwartet)
    head = _git(wurzel_code, "rev-parse", "HEAD").strip()
    if not head.lower().startswith(soll):                   # Bedingung 2
        raise Startpruefungsfehler(
            "HEAD von %s ist %s, %s nennt aber %s. Das ist ein anderer Code "
            "als der verlangte - hier wird nicht weitergerechnet."
            % (wurzel_code, head, UMGEBUNG_COMMIT, erwartet))
    status = _git(wurzel_code, "status", "--porcelain", "--",
                  *ARBEITSBAUM_PFADE)
    zeilen = [z for z in status.splitlines() if z.strip()]
    if zeilen:                                              # Bedingung 3
        raise Startpruefungsfehler(
            "Der Arbeitsbaum von %s ist ueber %s nicht sauber (%d Eintrag/"
            "Eintraege, die ersten: %s). Ein sauberer Commit ueber einem "
            "schmutzigen Arbeitsbaum beschreibt den Code so wenig wie ein "
            "gespaltener Baum."
            % (wurzel_code, ", ".join(ARBEITSBAUM_PFADE), len(zeilen),
               "; ".join(zeilen[:3])))
    return wurzel_code, head, "sauber"


def _normalisiert(name):
    """Paketnamen wie `pip` vergleichen: klein, `_` wie `-`."""
    return name.strip().lower().replace("_", "-")


def _lies_lock(pfad):
    """(kopf, pakete) aus der Lock-Datei - oder `Startpruefungsfehler`.

    Kopfzeilen sind `# schluessel  wert ...`; `pakete` ist eine Liste von
    `(name, version)` aus den `name==version`-Zeilen.
    """
    if not os.path.isfile(pfad):
        raise Startpruefungsfehler(
            "%s fehlt. Ohne Lock ist die Umgebung nicht pruefbar - und "
            "`nicht pruefbar` ist nicht gruen." % pfad)
    kopf, pakete = {}, []
    with open(pfad, "r", encoding="utf-8") as datei:
        for nummer, zeile in enumerate(datei, 1):
            zeile = zeile.strip()
            if not zeile:
                continue
            if zeile.startswith("#"):
                teile = zeile[1:].split()
                if len(teile) >= 2:
                    kopf.setdefault(teile[0], " ".join(teile[1:]))
                continue
            if "==" not in zeile:
                raise Startpruefungsfehler(
                    "%s, Zeile %d: %r ist keine `name==version`-Zeile. Ein "
                    "Lock, der `>=` sagt, ist kein Lock." % (pfad, nummer, zeile))
            name, version = zeile.split("==", 1)
            pakete.append((name.strip(), version.strip()))
    return kopf, pakete


def _pruefe_lock(pfad):
    """Teil C; (lock_sha256, interpreter, plattform) - oder werfen.

    ⚠️ `importlib.metadata`, nicht `pip`: kein Kindprozess, keine
    Netzverbindung, und dieselbe Frage, die ein `import` stellt.
    """
    import hashlib
    import platform
    import sys
    from importlib import metadata
    kopf, pakete = _lies_lock(pfad)
    interpreter = " ".join(sys.version.split())
    plattform = platform.platform()
    for schluessel in ("interpreter_voll", "plattform"):
        if schluessel not in kopf:
            raise Startpruefungsfehler(
                "%s traegt keine Kopfzeile `# %s ...`. Ohne sie ist die "
                "Umgebung nur zur Haelfte beschrieben." % (pfad, schluessel))
    abweichungen = []
    if kopf["interpreter_voll"] != interpreter:
        abweichungen.append("Interpreter: Lock %r, hier %r"
                            % (kopf["interpreter_voll"], interpreter))
    if kopf["plattform"] != plattform:
        abweichungen.append("Plattform: Lock %r, hier %r"
                            % (kopf["plattform"], plattform))
    for name, soll in pakete:
        try:
            ist = metadata.version(name)
        except metadata.PackageNotFoundError:
            ist = None
        if ist != soll:
            abweichungen.append("%s: Lock %s, installiert %s"
                                % (_normalisiert(name), soll,
                                   ist if ist is not None else "NICHT"))
    if abweichungen:
        raise Startpruefungsfehler(
            "Die Umgebung weicht von %s ab (%d Abweichung/en, die ersten "
            "drei: %s). Hier wird nichts installiert und nichts repariert - "
            "der Lauf bricht ab."
            % (pfad, len(abweichungen), " | ".join(abweichungen[:3])))
    with open(pfad, "rb") as datei:
        lock_sha256 = hashlib.sha256(datei.read()).hexdigest()
    return lock_sha256, interpreter, plattform


def _startpruefungen(modus, umgebung=None, einstiegspunkt=None,
                     lock_pfad=None, hier=None):
    """Alle Startpruefungen (Teile B und C); das Audit-dict (Teil D).

    `modus` ist das `(wurzel, hash)`-Paar aus `_modus_aus_umgebung`. Die
    weiteren Parameter gibt es fuer Proben, die eine Bedingung einzeln
    treffen wollen; im Betrieb bleiben sie leer.
    """
    umg = os.environ if umgebung is None else umgebung
    erwartet = (umg.get(UMGEBUNG_COMMIT) or "").strip()
    if not erwartet:
        raise Startpruefungsfehler(
            "%s und %s sind gesetzt, %s fehlt. Der Modus braucht alle drei: "
            "Wurzel und Hash sagen, welche DATEN, der Commit sagt, welcher "
            "CODE. Ein halb gesetzter Modus ist gefaehrlicher als keiner."
            % (UMGEBUNG_WURZEL, UMGEBUNG_HASH, UMGEBUNG_COMMIT))
    hier = os.path.realpath(__file__ if hier is None else hier)
    wurzel_code, commit, arbeitsbaum = _pruefe_codeherkunft(
        erwartet, einstiegspunkt, hier)
    if lock_pfad is None:
        lock_pfad = os.path.join(os.path.dirname(os.path.dirname(hier)), LOCK)
    lock_sha256, interpreter, plattform = _pruefe_lock(lock_pfad)
    return {
        "codewurzel": wurzel_code,
        "commit": commit,
        "arbeitsbaum": arbeitsbaum,
        "lock_sha256": lock_sha256,
        "interpreter": interpreter,
        "plattform": plattform,
        "snapshot_wurzel": modus[0],
        "snapshot_hash": modus[1],
    }


def startpruefung():
    """Das Audit-dict des bestandenen Starts (Teil D), sonst None.

    Ohne Modus None; mit Modus gibt es dieses Modul nur, wenn die
    Pruefungen bestanden sind - sonst hat der Import mit
    `RUECKGABEWERT_STARTPRUEFUNG` abgebrochen.
    """
    return None if _STARTPRUEFUNG is None else dict(_STARTPRUEFUNG)


def audit_zeilen(werte=None):
    """Die Auditzeilen als Text, in fester Reihenfolge; leer ohne Modus.

    ⭐ Dieselbe Funktion schreibt die `stderr`-Zeilen beim Import und ist
    fuer das spaetere Lese-Audit abrufbar - eine Fassung, nicht zwei.
    """
    werte = _STARTPRUEFUNG if werte is None else werte
    if werte is None:
        return []
    return ["%-19s %s" % (schluessel, werte[schluessel])
            for schluessel in AUDIT_SCHLUESSEL]


_MODUS = _modus_aus_umgebung()
_STARTPRUEFUNG = None

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
    # ⚠️ TB-58: Codeherkunft und Lock, blockierend. `SystemExit` statt einer
    # Exception, damit kein `except Exception` im Aufrufer den Abbruch in
    # einen stillen Weiterlauf verwandelt (Prueffrage D1).
    try:
        _STARTPRUEFUNG = _startpruefungen(_MODUS)
    except Startpruefungsfehler as _fehler:
        _sys.stderr.write(
            "[paths] STARTPRUEFUNG VERLETZT - %s\n"
            "[paths] Abbruch mit Rueckgabewert %d.\n"
            % (_fehler, RUECKGABEWERT_STARTPRUEFUNG))
        raise SystemExit(RUECKGABEWERT_STARTPRUEFUNG)
    _sys.stderr.write("".join("[paths] %s\n" % _z for _z in audit_zeilen()))
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
