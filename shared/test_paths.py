#!/usr/bin/env python3
"""
Selbsttests zu shared/paths.py - der Selektionsmodus (TB-52)
==============================================================================
⚠️ **Es gab bis TB-52 keine Wache fuer `shared/paths.py`** - nachgesehen, nicht
angenommen. Das Modul wird direkt von **10** Modulen importiert - den Abruf-
und Symbolskripten, die im Cron laufen - und **163** Module haengen transitiv
daran (gemessen TB-52; ⚠️ die vielzitierte Zahl **145** beantwortet eine andere
Frage, siehe den Kopf von `shared/paths.py`). Diese Datei ist die erste Wache.

Geprueft wird das **Verhalten**, nicht das Vorhandensein von Codestuecken.
Jede Probe laeuft gegen eine `paths.py`, die in einen **Wegwerfbaum** gelegt
wird - der Arbeitsbaum wird nicht angefasst und `data/` nicht beruehrt.

⚠️ **Jede Probe hat ihre Mutationsgegenprobe** (Prueffrage B1): dieselbe Probe
laeuft ein zweites Mal gegen eine Fassung, der **genau die eine Bedingung
fehlt**, die sie finden soll. Uebersieht die Probe den Fall dort **nicht**,
prueft sie etwas anderes als angenommen - **und das waere ein Befund ueber den
Test**, nicht ueber das Modul. Eine Mutation, die gar nicht greift (weil der
gesuchte Text sich geaendert hat), ist **NICHT PRUEFBAR** (Prueffrage A2),
nicht gruen.

⚠️ **Seit TB-58 traegt der Modus drei Variablen und prueft beim Start die
Codeherkunft.** Die Aufrufumgebung dieser Proben ist deshalb angepasst -
nur die Aufrufumgebung, die Prueflogik nicht: der Wegwerfbaum ist ein
Git-Repo mit einem Commit (`baue_baum`), der Probeprozess startet aus einer
Datei darin statt mit `python -c` (die Startpruefung braucht einen
Einstiegspunkt mit `__file__`), `TB_SELEKTIONSCOMMIT` nennt den Commit des
Baums, und die echte `requirements.lock` liegt daneben. Die Startpruefungen
selbst prueft `shared/test_startpruefungen.py`.

Nutzung:  python3 shared/test_paths.py
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(_HIER)
_ECHTE_QUELLE = os.path.join(_HIER, "paths.py")
_ECHTER_LOCK = os.path.join(_WURZEL, "requirements.lock")
_ECHTE_SYMBOLE = os.path.join(_HIER, "symbols_config.py")

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print("  [ok]     %s%s" % (name, (" - " + detail) if detail else ""))
    else:
        FEHLER.append(name)
        print("  [FEHLER] %s%s" % (name, (" - " + detail) if detail else ""))


def quelle():
    with open(_ECHTE_QUELLE, encoding="utf-8") as datei:
        return datei.read()


def mutiere(text, alt, neu, marke):
    """Eine Mutation anbringen - oder sagen, dass sie nicht gegriffen hat.

    ⚠️ Gibt `(text, True)` nur zurueck, wenn der gesuchte Text wirklich
    vorkam. Eine Mutation, die ins Leere greift, macht die Gegenprobe
    bedeutungslos - und das muss auffallen, nicht durchgehen.
    """
    if alt not in text:
        print("  [NICHT PRUEFBAR] Mutation %s griff nicht: %r kommt nicht vor."
              % (marke, alt[:60]))
        return text, False
    return text.replace(alt, neu), True


# ---------------------------------------------------------------------------
# Wegwerfbaum und Attrappe
# ---------------------------------------------------------------------------

def baue_baum(paths_quelle, mit_ordnern=True):
    wurzel = tempfile.mkdtemp(prefix="tb52_test_")
    os.makedirs(os.path.join(wurzel, "shared"))
    with open(os.path.join(wurzel, "shared", "paths.py"), "w",
              encoding="utf-8") as datei:
        datei.write(paths_quelle)
    if mit_ordnern:
        os.makedirs(os.path.join(wurzel, "data"))
        os.makedirs(os.path.join(wurzel, "config"))
    # TB-58: der Baum ist ein Git-Repo mit genau einem Commit, traegt die
    # echte Lock-Datei und die Abfrage als Einstiegsdatei.
    with open(os.path.join(wurzel, "abfrage.py"), "w", encoding="utf-8") as datei:
        datei.write(_ABFRAGE)
    # TB-103: die ECHTE `symbols_config.py` (unveraendert kopiert) und eine
    # zweite Abfrage, die sie laedt - damit Probe G am wirklichen Rueckfall
    # misst, ob die Standardliste unter dem Modus noch erreichbar ist.
    shutil.copy2(_ECHTE_SYMBOLE, os.path.join(wurzel, "shared",
                                              "symbols_config.py"))
    with open(os.path.join(wurzel, "abfrage_symbole.py"), "w",
              encoding="utf-8") as datei:
        datei.write(_ABFRAGE_SYMBOLE)
    if os.path.exists(_ECHTER_LOCK):
        shutil.copy2(_ECHTER_LOCK, os.path.join(wurzel, "requirements.lock"))
    _git(wurzel, "init", "-q")
    _git(wurzel, "add", "-A")
    _git(wurzel, "-c", "user.name=tb52_test", "-c", "user.email=tb52@test",
         "commit", "-q", "-m", "Wegwerfbaum")
    return wurzel


def _git(wurzel, *argumente):
    lauf = subprocess.run(["git", "-C", wurzel] + list(argumente),
                          capture_output=True, text=True)
    if lauf.returncode != 0:
        raise RuntimeError("git %s in %s: rc %d, %s"
                           % (" ".join(argumente), wurzel, lauf.returncode,
                              lauf.stderr.strip()))
    return lauf.stdout.strip()


def commit_von(wurzel):
    """HEAD des Wegwerfbaums - der Wert fuer TB_SELEKTIONSCOMMIT."""
    return _git(wurzel, "rev-parse", "HEAD")


# TB-103: die Universumsdateien der Attrappe - Anordnung wie im echten Snapshot
# (`config/` unter der Wurzel, im MANIFEST unter `dateien` genannt). Erfundene
# Symbole; drei Krypto-Zeilen, zwei Aktien-Zeilen.
UNIVERSUM = {"config/top25_symbols.txt": "AAAUSDT\nBBBUSDT\nCCCUSDT\n",
             "config/sp500_top150.txt": "AAA\nBBB\n"}


def baue_attrappe(hash_="attrappe000000000000000000000000",
                  mit_manifest=True, mit_hashfeld=True, mit_config=True,
                  fehlend=(), inhalt_ersatz=None, manifest_universum=True,
                  zusatz_config=None):
    """⚠️ **KEIN Snapshot von `data/`.**

    Nach Registertext 5 / F1a wird der Snapshot erst am Tag des signierten
    Tags gezogen. Hier liegt ein Wegwerf-Ordner mit einer erfundenen Datei -
    er beantwortet jede Frage dieser Datei genauso gut.

    TB-103: seit dem Resolver-Fix traegt die Attrappe auch `config/` mit den
    Universumsdateien aus `UNIVERSUM`, und das MANIFEST nennt sie. Die
    Schalter stoeren genau eine Sache: `mit_config=False` (Ordner fehlt),
    `fehlend` (diese Dateien nicht anlegen), `inhalt_ersatz` ({name: text}),
    `manifest_universum=False` (MANIFEST nennt keine), `zusatz_config`
    ({name: text}, liegt im Ordner, MANIFEST nennt sie NICHT).
    """
    ordner = tempfile.mkdtemp(prefix="tb52_attrappe_")
    with open(os.path.join(ordner, "XXXTEST_1d.csv"), "w") as datei:
        datei.write("timestamp,close\n2020-01-01,1.0\n")
    if mit_config:
        os.makedirs(os.path.join(ordner, "config"))
        texte = dict(UNIVERSUM)
        texte.update(inhalt_ersatz or {})
        for name, text in texte.items():
            if name not in fehlend:
                with open(os.path.join(ordner, name), "w") as datei:
                    datei.write(text)
        for name, text in (zusatz_config or {}).items():
            with open(os.path.join(ordner, name), "w") as datei:
                datei.write(text)
    if mit_manifest:
        dateien = {"XXXTEST_1d.csv": {}}
        if manifest_universum:
            dateien.update({name: {} for name in UNIVERSUM})
        inhalt = {"datenstand_hash": "egal", "kursdateien": 1,
                  "dateien": dateien}
        if mit_hashfeld:
            inhalt["snapshot_hash"] = hash_
        with open(os.path.join(ordner, "MANIFEST.json"), "w") as datei:
            json.dump(inhalt, datei)
    return ordner


_ABFRAGE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
ergebnis = {}
try:
    import paths
    ergebnis["DATA_DIR"] = paths.DATA_DIR
    ergebnis["CONFIG_DIR"] = paths.CONFIG_DIR
    ergebnis["modus"] = paths.selektionsmodus()
except Exception as fehler:
    ergebnis["import_fehler"] = "%s: %s" % (type(fehler).__name__, fehler)
    json.dump(ergebnis, sys.stdout); sys.exit(0)
try:
    ergebnis["LIVE_DATA_DIR"] = paths.LIVE_DATA_DIR
except Exception as fehler:
    ergebnis["live_fehler"] = "%s: %s" % (type(fehler).__name__, fehler)
json.dump(ergebnis, sys.stdout)
'''

# TB-103: laedt nach `paths` die echte `symbols_config` und haelt fest, was sie
# auf stdout sagt (die Warnzeile der Standardliste) und was sie geladen hat.
# ⚠️ Scheitert schon der Import von `paths` mit SystemExit, endet der Prozess
# mit dessen Rueckgabewert und schreibt nichts auf stdout - das ist der Fall,
# den Probe G erwartet.
_ABFRAGE_SYMBOLE = r'''
import contextlib, io, json, sys
sys.path.insert(0, sys.argv[1])
import paths
puffer = io.StringIO()
with contextlib.redirect_stdout(puffer):
    import symbols_config
json.dump({"CONFIG_DIR": paths.CONFIG_DIR,
           "SYMBOLS_FILE": symbols_config.SYMBOLS_FILE,
           "SYMBOLS": list(symbols_config.SYMBOLS),
           "ausgabe": puffer.getvalue()}, sys.stdout)
'''


def frage(wurzel, wurzel_env=None, hash_env=None, umgebung_zusatz=None,
          abfrage="abfrage.py"):
    """Die Pfade aus einem eigenen Prozess erfragen.

    ⚠️ Eigener Prozess je Frage: zwei Fassungen desselben Moduls verdecken
    sich sonst in `sys.modules` (Prueffrage B6, TB-40).
    """
    umgebung = dict(os.environ)
    umgebung.pop("TB_SELEKTIONSWURZEL", None)
    umgebung.pop("TB_SELEKTIONSHASH", None)
    umgebung.pop("TB_SELEKTIONSCOMMIT", None)
    if wurzel_env is not None:
        umgebung["TB_SELEKTIONSWURZEL"] = wurzel_env
    if hash_env is not None:
        umgebung["TB_SELEKTIONSHASH"] = hash_env
    if wurzel_env is not None and hash_env is not None:
        # TB-58: der vollstaendige Modus traegt den Commit des Baums.
        umgebung["TB_SELEKTIONSCOMMIT"] = commit_von(wurzel)
    if umgebung_zusatz:
        umgebung.update(umgebung_zusatz)
    lauf = subprocess.run(
        [sys.executable, os.path.join(wurzel, abfrage),
         os.path.join(wurzel, "shared")],
        capture_output=True, text=True, env=umgebung)
    try:
        werte = json.loads(lauf.stdout) if lauf.stdout.strip() else {}
    except ValueError:
        werte = {}
    werte["_rc"] = lauf.returncode
    werte["_stderr"] = lauf.stderr
    return werte


# ===========================================================================
# Probe A - ohne Modus: jeder Pfad wie vorher, mit Zahl
# ===========================================================================

def probe_a_ohne_modus():
    """Die Bedingung, an der die Freigabe haengt.

    ⚠️ Der Vergleich selbst steht **nicht** hier noch einmal, sondern in
    `research/resolver_selektion/pfadvergleich.py` und wird von dort
    importiert. Zwei Fassungen derselben Rechnung laufen in diesem Projekt
    schon einmal unbemerkt auseinander.
    """
    print("\nProbe A - ohne Modus verhaelt sich paths.py wie im Bezugscommit")
    pfad = os.path.join(_WURZEL, "research", "resolver_selektion",
                        "pfadvergleich.py")
    if not os.path.exists(pfad):
        check("A NICHT PRUEFBAR", False, "%s fehlt" % pfad)
        return
    spec = importlib.util.spec_from_file_location("tb52_pfadvergleich", pfad)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)

    alt = modul.alte_fassung()
    if alt is None:
        # Prueffrage A2/B3: ohne den festgenagelten Bezug wird nichts behauptet.
        check("A NICHT PRUEFBAR", False,
              "Bezugscommit %s nicht auffindbar" % modul.BEZUGSCOMMIT[:8])
        return
    # TB-107 (Fable 25c 4 (3)(b)): `strategy_paths` fragt
    # `paths.selektionsmodus()` direkt, ohne Ersatz. Die Fassung aus TB-52
    # kennt die Funktion nicht; sie bekommt hier eine, die `None` liefert
    # (kein Modus). Verglichen werden weiter nur Zeichenketten - eine Funktion
    # ist keine, die Zahl der Pfade bleibt.
    alt = alt + "\n\ndef selektionsmodus():\n    return None\n"
    ergebnis = modul.vergleiche(alt, quelle())
    check("A1 null Unterschiede", not ergebnis["unterschiede"],
          "%d Pfade verglichen (%d Bots), %d Unterschiede"
          % (ergebnis["verglichen"], len(modul.BOTS),
             len(ergebnis["unterschiede"])))
    for u in ergebnis["unterschiede"]:
        print("       ⚠️ %s / %s: %r -> %r"
              % (u["bot"], u["name"], u["alt"], u["neu"]))

    # --- Mutation: waere ein Unterschied ueberhaupt sichtbar? --------------
    verstellt, griff = mutiere(quelle(), 'os.path.join(BASE_DIR, "data")',
                               'os.path.join(BASE_DIR, "daten_verstellt")', "A")
    if griff:
        gegen = modul.vergleiche(alt, verstellt)
        check("A2 Mutationsprobe beisst", bool(gegen["unterschiede"]),
              "verstellte Fassung -> %d Unterschiede (ohne die Mutation: 0)"
              % len(gegen["unterschiede"]))
    else:
        check("A2 Mutationsprobe", False, "Mutation griff nicht")


# ===========================================================================
# Probe B - mit Modus zeigt der Kursdatenpfad in den Snapshot
# ===========================================================================

def probe_b_modus_zeigt_in_snapshot():
    print("\nProbe B - mit Modus zeigt der Kursdatenpfad in den Snapshot")
    attrappe = baue_attrappe()
    baum = baue_baum(quelle())
    try:
        w = frage(baum, attrappe, "attrappe000000000000000000000000")
        check("B1 DATA_DIR zeigt in den Snapshot",
              w.get("DATA_DIR") == attrappe, str(w.get("DATA_DIR")))
        # ⚠️ TB-103 umgeschrieben: bis dahin pruefte B2 `CONFIG_DIR ==
        # attrappe` - also die falsche, flache Anordnung (TB-98 Befund 1).
        check("B2 CONFIG_DIR zeigt in den Snapshot-Unterordner config/",
              w.get("CONFIG_DIR") == os.path.join(attrappe, "config"),
              str(w.get("CONFIG_DIR")))
        check("B3 der Lauf SAGT, dass er im Modus ist",
              "SELEKTIONSMODUS AKTIV" in w.get("_stderr", ""),
              "Prueffrage D1")

        # Mutation: der Modus wird gelesen, aber nicht angewandt.
        mutiert, griff = mutiere(quelle(), "    DATA_DIR = _MODUS[0]",
                                 "    DATA_DIR = _LIVE_DATA_DIR", "B")
        if griff:
            baum_m = baue_baum(mutiert)
            try:
                wm = frage(baum_m, attrappe, "attrappe000000000000000000000000")
                check("B4 Mutationsprobe beisst",
                      wm.get("DATA_DIR") != attrappe,
                      "ohne die Zuweisung zeigt DATA_DIR auf %s - die Probe "
                      "faellt dort durch, wie sie soll" % wm.get("DATA_DIR"))
            finally:
                shutil.rmtree(baum_m, ignore_errors=True)
        else:
            check("B4 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        shutil.rmtree(baum, ignore_errors=True)
        shutil.rmtree(attrappe, ignore_errors=True)


# ===========================================================================
# Probe C - mit Modus wirft die Anfrage nach dem Live-Bestand
# ===========================================================================

def probe_c_live_wirft():
    print("\nProbe C - mit Modus wirft die Anfrage nach dem Live-Bestand")
    attrappe = baue_attrappe()
    baum = baue_baum(quelle())
    try:
        w = frage(baum, attrappe, "attrappe000000000000000000000000")
        meldung = w.get("live_fehler", "")
        check("C1 LIVE_DATA_DIR wirft", "Selektionsfehler" in meldung,
              meldung[:80] or "(nichts geworfen)")
        # ⚠️ Die Meldung muss zwei Dinge nennen, sonst ist sie wertlos:
        #    wer gefragt hat, und was er haette fragen sollen.
        check("C2 die Meldung nennt das fragende Modul",
              ".py:" in meldung or "<string>:" in meldung,
              "Fundstelle in der Meldung")
        check("C3 die Meldung nennt die Alternative",
              "`DATA_DIR`" in meldung, "Verweis auf DATA_DIR")

        # Mutation: LIVE_DATA_DIR wird auch unter dem Modus als Modulglobal
        # gesetzt - dann greift `__getattr__` nie und nichts wirft.
        mutiert, griff = mutiere(
            quelle(), "    import sys as _sys",
            "    LIVE_DATA_DIR = _LIVE_DATA_DIR\n"
            "    LIVE_CONFIG_DIR = _LIVE_CONFIG_DIR\n"
            "    import sys as _sys", "C")
        if griff:
            baum_m = baue_baum(mutiert)
            try:
                wm = frage(baum_m, attrappe, "attrappe000000000000000000000000")
                check("C4 Mutationsprobe beisst",
                      "live_fehler" not in wm,
                      "ohne die Auslassung liefert LIVE_DATA_DIR still %s"
                      % wm.get("LIVE_DATA_DIR"))
            finally:
                shutil.rmtree(baum_m, ignore_errors=True)
        else:
            check("C4 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        shutil.rmtree(baum, ignore_errors=True)
        shutil.rmtree(attrappe, ignore_errors=True)


# ===========================================================================
# Probe D - Modus gesetzt, Snapshot fehlt oder Hash passt nicht
# ===========================================================================

def probe_d_fehlender_snapshot():
    print("\nProbe D - Modus gesetzt, Snapshot fehlt / Hash passt nicht")
    baum = baue_baum(quelle())
    attrappe = baue_attrappe()
    ohne_manifest = baue_attrappe(mit_manifest=False)
    ohne_feld = baue_attrappe(mit_hashfeld=False)
    try:
        w = frage(baum, os.path.join(attrappe, "gibt_es_nicht"), "egal")
        check("D1 Wurzel existiert nicht -> wirft",
              "Selektionsfehler" in w.get("import_fehler", ""),
              w.get("import_fehler", "(nichts)")[:80])

        w = frage(baum, ohne_manifest, "egal")
        check("D2 kein MANIFEST.json -> wirft",
              "Selektionsfehler" in w.get("import_fehler", ""),
              w.get("import_fehler", "(nichts)")[:80])

        w = frage(baum, ohne_feld, "egal")
        check("D3 Manifest ohne snapshot_hash -> wirft",
              "Selektionsfehler" in w.get("import_fehler", ""),
              w.get("import_fehler", "(nichts)")[:80])

        w = frage(baum, attrappe, "ein_ganz_anderer_hash")
        check("D4 falscher Hash -> wirft",
              "Selektionsfehler" in w.get("import_fehler", ""),
              w.get("import_fehler", "(nichts)")[:80])

        w = frage(baum, attrappe, None)
        check("D5 nur eine der beiden Variablen -> wirft",
              "Selektionsfehler" in w.get("import_fehler", ""),
              w.get("import_fehler", "(nichts)")[:80])

        # Mutation: der stille Rueckfall. Statt zu werfen, schaltet die
        # Pruefung den Modus einfach ab - der Lauf rechnet dann gegen den
        # Live-Bestand, ohne es zu sagen. ⚠️ Genau die Ausfallform D1.
        mutiert, griff = mutiere(
            quelle(),
            "    wurzel = os.path.abspath(wurzel)\n"
            "    gefunden = _lies_snapshot_hash(wurzel)",
            "    wurzel = os.path.abspath(wurzel)\n"
            "    try:\n"
            "        gefunden = _lies_snapshot_hash(wurzel)\n"
            "    except Selektionsfehler:\n"
            "        return None", "D")
        if griff:
            baum_m = baue_baum(mutiert)
            try:
                wm = frage(baum_m, os.path.join(attrappe, "gibt_es_nicht"),
                           "egal")
                check("D6 Mutationsprobe beisst",
                      "import_fehler" not in wm,
                      "mit stillem Rueckfall zeigt DATA_DIR auf %s statt zu "
                      "werfen" % wm.get("DATA_DIR"))
            finally:
                shutil.rmtree(baum_m, ignore_errors=True)
        else:
            check("D6 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        for o in (baum, attrappe, ohne_manifest, ohne_feld):
            shutil.rmtree(o, ignore_errors=True)


# ===========================================================================
# Probe E - der Kindprozess, festgeschrieben
# ===========================================================================

def probe_e_kindprozess():
    """Das unter TB-52/1.2 gemessene Verhalten, als Wache festgehalten."""
    print("\nProbe E - der Kindprozess")
    attrappe = baue_attrappe()
    baum = baue_baum(quelle())
    shared = os.path.join(baum, "shared")
    # ⚠️ Der Quelltext des Kindes wird HIER gebaut und dann als Literal in den
    # Enkel eingesetzt. Ein Vorlagentext, der beide Ebenen in einem Durchgang
    # formatiert, hat im ersten Entwurf dieser Datei zweimal ersetzt - der
    # Enkel brach mit einem TypeError ab, lieferte eine leere Ausgabe, und die
    # Probe las das als "erbt den Modus nicht". ⭐ Ein gescheiterter Aufruf und
    # ein leeres Ergebnis sehen gleich aus (Prueffrage A1) - gefunden nur, weil
    # `research/resolver_selektion/kindprozess.py` das Gegenteil gemessen hatte.
    kind_quelle = (
        "import json,sys;sys.path.insert(0,%r);import paths;"
        "json.dump({'DATA_DIR':paths.DATA_DIR},sys.stdout)" % shared)
    # TB-58: das Kind startet aus einer Datei im Baum (Einstiegspunkt).
    kind_datei = os.path.join(baum, "kind.py")
    with open(kind_datei, "w", encoding="utf-8") as datei:
        datei.write(kind_quelle + "\n")
    enkel = (
        "import subprocess, sys\n"
        "lauf = subprocess.run([sys.executable, %r],"
        " capture_output=True, text=True)\n"
        "sys.stdout.write(lauf.stdout)\n"
        "sys.stderr.write(lauf.stderr)\n" % kind_datei)
    try:
        umgebung = dict(os.environ)
        umgebung["TB_SELEKTIONSWURZEL"] = attrappe
        umgebung["TB_SELEKTIONSHASH"] = "attrappe000000000000000000000000"
        umgebung["TB_SELEKTIONSCOMMIT"] = commit_von(baum)
        lauf = subprocess.run([sys.executable, "-c", enkel],
                              capture_output=True, text=True, env=umgebung)
        try:
            werte = json.loads(lauf.stdout)
        except ValueError:
            werte = {}
        if lauf.returncode != 0 or not lauf.stdout.strip():
            # Prueffrage A1: kein Ergebnis ist hier NICHT "erbt nicht".
            check("E1 NICHT PRUEFBAR", False,
                  "der Enkel lieferte nichts (rc=%d): %s"
                  % (lauf.returncode, lauf.stderr.strip()[-200:]))
        else:
            check("E1 der Enkelprozess erbt den Modus",
                  werte.get("DATA_DIR") == attrappe,
                  "zwei Ebenen tief: %s" % werte.get("DATA_DIR"))

        # ⚠️ Der Cron-Fall: eine minimale Umgebung traegt den Modus nicht.
        mager = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                 "HOME": os.environ.get("HOME", "/tmp")}
        w = frage(baum, umgebung_zusatz=mager)
        check("E2 magere Umgebung (Cron-Nachbildung) -> Live-Bestand",
              w.get("DATA_DIR") == os.path.join(baum, "data"),
              str(w.get("DATA_DIR")))

        # Mutation: ein prozesslokaler Modus. Er wird nicht vererbt - das
        # Kind liest dann STILL aus dem Live-Bestand.
        mutiert, griff = mutiere(quelle(), "_MODUS = _modus_aus_umgebung()",
                                 "_MODUS = None  # prozesslokal gedacht", "E")
        if griff:
            baum_m = baue_baum(mutiert)
            try:
                wm = frage(baum_m, attrappe,
                           "attrappe000000000000000000000000")
                check("E3 Mutationsprobe beisst",
                      wm.get("DATA_DIR") == os.path.join(baum_m, "data"),
                      "ohne Vererbung ueber die Umgebung liest das Kind STILL "
                      "den Live-Bestand: %s" % wm.get("DATA_DIR"))
            finally:
                shutil.rmtree(baum_m, ignore_errors=True)
        else:
            check("E3 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        shutil.rmtree(baum, ignore_errors=True)
        shutil.rmtree(attrappe, ignore_errors=True)


# ===========================================================================
# Probe F - T46.8: der Import legt kein Verzeichnis mehr an
# ===========================================================================

def probe_f_kein_verzeichnis():
    """Gemessen an einem Wegwerf-Ordner, der vorher nicht existiert.

    ⚠️ Der Baum wird hier **ohne** `data/` und `config/` gebaut. Existierten
    sie schon, sagte die Probe nichts: `exist_ok=True` liesse sie einfach
    stehen, und die Probe waere gruen, ohne etwas zu messen (Prueffrage A1).
    """
    print("\nProbe F - T46.8: der Import legt kein Verzeichnis an")
    baum = baue_baum(quelle(), mit_ordnern=False)
    try:
        data = os.path.join(baum, "data")
        config = os.path.join(baum, "config")
        check("F1 vorher existiert data/ nicht", not os.path.exists(data),
              data)
        w = frage(baum)
        check("F2 der Import gelingt", "import_fehler" not in w,
              w.get("import_fehler", "ohne Fehler"))
        check("F3 nachher existiert data/ IMMER NOCH nicht",
              not os.path.exists(data), "nicht angelegt")
        check("F4 nachher existiert config/ immer noch nicht",
              not os.path.exists(config), "nicht angelegt")

        # Mutation: die beiden alten `makedirs`-Zeilen zurueck.
        mutiert, griff = mutiere(
            quelle(), "# Die Namen der beiden Umgebungsvariablen",
            "os.makedirs(_LIVE_DATA_DIR, exist_ok=True)\n"
            "os.makedirs(_LIVE_CONFIG_DIR, exist_ok=True)\n\n"
            "# Die Namen der beiden Umgebungsvariablen", "F")
        if griff:
            baum_m = baue_baum(mutiert, mit_ordnern=False)
            try:
                frage(baum_m)
                check("F5 Mutationsprobe beisst",
                      os.path.exists(os.path.join(baum_m, "data")),
                      "mit den makedirs-Zeilen entsteht data/ beim Import - "
                      "die Probe faellt dort durch, wie sie soll")
            finally:
                shutil.rmtree(baum_m, ignore_errors=True)
        else:
            check("F5 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        shutil.rmtree(baum, ignore_errors=True)


# ===========================================================================
# Probe G - TB-103: Universumsdateien unter <snapshot>/config/, kein Rueckfall
# ===========================================================================

_FUENFERLISTE = "Standardliste"      # die Warnzeile der Symboldateien


def _g_lauf(attrappe, quelle_text):
    """Ein Lauf der Symbol-Abfrage im Modus gegen `quelle_text` als paths.py."""
    baum = baue_baum(quelle_text)
    try:
        return frage(baum, attrappe, "attrappe000000000000000000000000",
                     abfrage="abfrage_symbole.py")
    finally:
        shutil.rmtree(baum, ignore_errors=True)


def _g_abbruch(w):
    """rc 2, Meldung der Startpruefung, keine Standardliste - Soll fuer G1-G4."""
    text = w.get("_stderr", "") + w.get("ausgabe", "")
    return (w["_rc"] == 2 and "STARTPRUEFUNG VERLETZT" in w.get("_stderr", "")
            and _FUENFERLISTE not in text)


def _g_kurz(w):
    zeilen = [z for z in w.get("_stderr", "").splitlines()
              if "STARTPRUEFUNG" in z]
    return "rc=%d, %s, Standardliste %s" % (
        w["_rc"], (zeilen[0][:110] if zeilen else "keine Startpruefungszeile"),
        "JA" if _FUENFERLISTE in (w.get("_stderr", "") + w.get("ausgabe", ""))
        else "nein")


# Die Faelle, in denen etwas passieren MUSS (G1-G4), und die, in denen nichts
# passieren darf (G5, G6) - Stoerproben in beide Richtungen (Fable 24b C2).
_G_FAELLE = (
    ("G1", "Modus, config/ fehlt in der Attrappe",
     dict(mit_config=False)),
    ("G2", "Modus, config/ da, eine Universumsdatei fehlt",
     dict(fehlend=("config/top25_symbols.txt",))),
    ("G3", "Modus, eine Universumsdatei leer (0 Bytes)",
     dict(inhalt_ersatz={"config/sp500_top150.txt": ""})),
    ("G3b", "Modus, eine Universumsdatei nur aus Leerzeilen",
     dict(inhalt_ersatz={"config/top25_symbols.txt": "\n  \n\n"})),
    ("G4", "Modus, das MANIFEST nennt keine Datei unter config/",
     dict(manifest_universum=False)),
)


def probe_g_universum():
    print("\nProbe G - TB-103: Universumsdateien unter <snapshot>/config/, "
          "kein Rueckfall unter dem Modus")
    attrappen = {}
    try:
        for marke, _, schalter in _G_FAELLE:
            attrappen[marke] = baue_attrappe(**schalter)
        attrappen["G5"] = baue_attrappe()
        attrappen["G6"] = baue_attrappe(
            zusatz_config={"config/nicht_im_manifest.txt": ""})

        ergebnisse = {}
        for marke, text, _ in _G_FAELLE:
            w = _g_lauf(attrappen[marke], quelle())
            ergebnisse[marke] = w
            check("%s %s -> rc 2, keine Standardliste" % (marke, text),
                  _g_abbruch(w), _g_kurz(w))

        # --- nichts darf passieren -----------------------------------------
        erwartet = UNIVERSUM["config/top25_symbols.txt"].split()

        def g5_gruen(w):
            return (w["_rc"] == 0
                    and w.get("CONFIG_DIR", "").endswith(os.sep + "config")
                    and w.get("SYMBOLS_FILE") == os.path.join(
                        attrappen["G5"], "config", "top25_symbols.txt")
                    and w.get("SYMBOLS") == erwartet
                    and _FUENFERLISTE not in w.get("ausgabe", ""))

        w = _g_lauf(attrappen["G5"], quelle())
        check("G5 Modus, alles da -> rc 0, CONFIG_DIR endet auf /config, "
              "Liste aus dem Snapshot", g5_gruen(w),
              "rc=%d, CONFIG_DIR=%s, %d Symbole aus %s"
              % (w["_rc"], w.get("CONFIG_DIR"), len(w.get("SYMBOLS", [])),
                 w.get("SYMBOLS_FILE")))
        w = _g_lauf(attrappen["G6"], quelle())
        check("G6 Modus, leere Zusatzdatei in config/, vom MANIFEST nicht "
              "genannt -> rc 0 (Stoerprobe: darf nichts ausloesen)",
              w["_rc"] == 0 and w.get("SYMBOLS") == erwartet,
              "rc=%d" % w["_rc"])

        # --- Mutationsproben, jede allein gegen den Grundzustand ----------
        # M1: der Fix zurueckgenommen - CONFIG_DIR wieder die flache Wurzel.
        mutiert, griff = mutiere(
            quelle(),
            "    CONFIG_DIR = os.path.join(_MODUS[0], CONFIG_UNTERORDNER)",
            "    CONFIG_DIR = _MODUS[0]", "G-M1")
        if griff:
            wm = _g_lauf(attrappen["G5"], mutiert)
            check("G7 Mutationsprobe M1 (Fix zurueckgenommen) beisst: G5 rot",
                  not g5_gruen(wm),
                  "mutiert: rc=%d, CONFIG_DIR=%s, Standardliste %s"
                  % (wm["_rc"], wm.get("CONFIG_DIR"),
                     "JA" if _FUENFERLISTE in wm.get("ausgabe", "") else "nein"))
        else:
            check("G7 Mutationsprobe M1", False, "Mutation griff nicht")

        # M2: die Existenzpruefung entfernt - der Aufruf beim Import faellt weg.
        mutiert, griff = mutiere(
            quelle(), "        _pruefe_universum(_MODUS[0])\n", "", "G-M2")
        if griff:
            rot = []
            for marke in ("G1", "G2", "G3", "G3b", "G4"):
                wm = _g_lauf(attrappen[marke], mutiert)
                if not _g_abbruch(wm):
                    rot.append("%s(rc=%d%s)" % (
                        marke, wm["_rc"],
                        ", Standardliste" if _FUENFERLISTE in wm.get("ausgabe", "")
                        else ""))
            check("G8 Mutationsprobe M2 (Existenzpruefung entfernt) beisst: "
                  "G1-G4 alle rot", len(rot) == 5,
                  "rot unter der Mutation: %s" % ", ".join(rot))
        else:
            check("G8 Mutationsprobe M2", False, "Mutation griff nicht")

        # M3: nur die Leer-Pruefung entfernt - allein G3/G3b muessen rot werden.
        mutiert, griff = mutiere(
            quelle(),
            "            if not any(zeile.strip() for zeile in inhalt):",
            "            if False:", "G-M3")
        if griff:
            w3 = _g_lauf(attrappen["G3"], mutiert)
            w3b = _g_lauf(attrappen["G3b"], mutiert)
            w2 = _g_lauf(attrappen["G2"], mutiert)
            check("G9 Mutationsprobe M3 (Leer-Pruefung entfernt) beisst: G3 und "
                  "G3b rot, G2 bleibt gruen",
                  not _g_abbruch(w3) and not _g_abbruch(w3b) and _g_abbruch(w2),
                  "G3 %s / G3b %s / G2 %s" % (_g_kurz(w3), _g_kurz(w3b),
                                              _g_kurz(w2)))
        else:
            check("G9 Mutationsprobe M3", False, "Mutation griff nicht")

        # M4: nur die Pruefung "MANIFEST nennt keine" entfernt - allein G4 rot.
        mutiert, griff = mutiere(
            quelle(), "    if not namen:\n", "    if False:\n", "G-M4")
        if griff:
            w4 = _g_lauf(attrappen["G4"], mutiert)
            w2 = _g_lauf(attrappen["G2"], mutiert)
            check("G10 Mutationsprobe M4 (leere Namensmenge zugelassen) beisst: "
                  "G4 rot, G2 bleibt gruen",
                  not _g_abbruch(w4) and _g_abbruch(w2),
                  "G4 %s / G2 %s" % (_g_kurz(w4), _g_kurz(w2)))
        else:
            check("G10 Mutationsprobe M4", False, "Mutation griff nicht")
    finally:
        for o in attrappen.values():
            shutil.rmtree(o, ignore_errors=True)


def main():
    print("=" * 78)
    print("Selbsttests zu shared/paths.py - der Selektionsmodus (TB-52)")
    print("=" * 78)
    for name, probe in (("A", probe_a_ohne_modus),
                        ("B", probe_b_modus_zeigt_in_snapshot),
                        ("C", probe_c_live_wirft),
                        ("D", probe_d_fehlender_snapshot),
                        ("E", probe_e_kindprozess),
                        ("F", probe_f_kein_verzeichnis),
                        ("G", probe_g_universum)):
        try:
            probe()
        except Exception as fehler:                            # noqa: BLE001
            import traceback
            FEHLER.append("Probe %s (Ausnahme)" % name)
            print("  [FEHLER] Probe %s warf eine Ausnahme: %s" % (name, fehler))
            traceback.print_exc()

    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print("%d von %d Pruefungen bestanden, %d fehlgeschlagen."
          % (BESTANDEN, gesamt, len(FEHLER)))
    for name in FEHLER:
        print("  - %s" % name)
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
