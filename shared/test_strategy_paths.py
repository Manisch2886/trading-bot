#!/usr/bin/env python3
"""
Selbsttests zu shared/strategy_paths.py - DATA_DIR aus dem Resolver (TB-53b)
==============================================================================
⚠️ **Ueber `get_strategy_paths()` laufen alle 90 Selektionsmodule** - 71 direkt,
19 ueber `multi_symbol_optimise` (gemessen 19.09.2026, TB-53a). Bis TB-53b hat
die Funktion `DATA_DIR` selbst gebaut und `shared/paths.py` nie beruehrt; der
Selektionsmodus aus TB-52 erreichte damit keines der 90. Seit TB-53b fragt sie
`paths.py`. Diese Datei ist die Wache dafuer.

Geprueft wird das **Verhalten**, nicht das Vorhandensein von Codestuecken.
Jede Probe laeuft gegen eine `strategy_paths.py`, die zusammen mit der
**echten** `paths.py` in einen **Wegwerfbaum** in der Form des Projekts gelegt
wird (`<wurzel>/shared/`, `<wurzel>/strategies/<bot>/`) - der Arbeitsbaum wird
nicht angefasst, `data/` nicht beruehrt. Je Bot und je Frage **ein eigener
Prozess** (TB-40: neun gleichnamige Module verdecken sich in `sys.modules`).

⚠️ **Jede Probe hat ihre Mutationsgegenprobe** (Prueffrage B1): dieselbe Probe
laeuft ein zweites Mal gegen eine Fassung, der **genau die eine Bedingung
fehlt**, die sie finden soll. Eine Mutation, die nicht greift, ist
**NICHT PRUEFBAR** (Prueffrage A2), nicht gruen.

⚠️ **Die Vorher-Messung (Probe A) ist inhaltsadressiert** (Prueffrage A7):
die alte Fassung kommt aus `git show <BEZUGSCOMMIT>:shared/strategy_paths.py`,
nicht aus dem Gedaechtnis. Ist der Commit nicht zu finden, wird nichts
behauptet.

⚠️ **Seit TB-58 traegt der Modus drei Variablen und prueft beim Start die
Codeherkunft.** Die Aufrufumgebung der Modus-Proben ist deshalb angepasst -
nur die Aufrufumgebung, die Prueflogik nicht: der Wegwerfbaum ist ein
Git-Repo mit einem Commit (`baue_baum`), der Probeprozess startet aus einer
Datei statt mit `python -c` (die Startpruefung braucht einen Einstiegspunkt
mit `__file__`), `TB_SELEKTIONSCOMMIT` nennt den Commit des Baums, und die
echte `requirements.lock` liegt daneben. Die Startpruefungen selbst prueft
`shared/test_startpruefungen.py`.

Nutzung:  python3 shared/test_strategy_paths.py
"""

import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(_HIER)
_QUELLE = os.path.join(_HIER, "strategy_paths.py")
_PATHS_QUELLE = os.path.join(_HIER, "paths.py")
_ECHTER_LOCK = os.path.join(_WURZEL, "requirements.lock")

# ⚠️ Festgenagelt (Prueffrage B3): der letzte Commit VOR TB-53b, in dem
# `strategy_paths.py` den Datenpfad noch selbst gebaut hat.
BEZUGSCOMMIT = "eaf25728dc1e9bb1de7463334b78490b6b7ea827"

BOTS = (
    "elliott_wave",
    "elliott_wave_stocks",
    "rsi2_crypto",
    "rsi2_mean_reversion",
    "t3_supertrend",
    "turtle_soup_crypto",
    "turtle_soup_stocks",
    "volatility_breakout",
    "volatility_breakout_crypto",
)
SCHLUESSEL = ("BASE_DIR", "STRATEGY_NAME", "DATA_DIR", "CONFIG_DIR",
              "RESULTS_DIR", "LOGS_DIR", "DB_FILE")
# Die drei, die auf den Betrieb zeigen und nie in den Snapshot duerfen.
BETRIEB = ("RESULTS_DIR", "LOGS_DIR", "DB_FILE")

ATTRAPPEN_HASH = "attrappe000000000000000000000000"

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
    with open(_QUELLE, encoding="utf-8") as datei:
        return datei.read()


def mutiere(text, alt, neu, marke):
    """Eine Mutation anbringen - oder sagen, dass sie nicht gegriffen hat."""
    if alt not in text:
        print("  [NICHT PRUEFBAR] Mutation %s griff nicht: %r kommt nicht vor."
              % (marke, alt[:60]))
        return text, False
    return text.replace(alt, neu), True


# ---------------------------------------------------------------------------
# Wegwerfbaum und Attrappe
# ---------------------------------------------------------------------------

def baue_baum(strategy_paths_quelle, mit_paths=True):
    """Ein Baum in der Form des Projekts. `paths.py` ist die ECHTE."""
    wurzel = tempfile.mkdtemp(prefix="tb53b_test_")
    shared = os.path.join(wurzel, "shared")
    os.makedirs(shared)
    with open(os.path.join(shared, "strategy_paths.py"), "w",
              encoding="utf-8") as datei:
        datei.write(strategy_paths_quelle)
    if mit_paths:
        shutil.copy2(_PATHS_QUELLE, os.path.join(shared, "paths.py"))
    for bot in BOTS:
        os.makedirs(os.path.join(wurzel, "strategies", bot))
    os.makedirs(os.path.join(wurzel, "data"))
    os.makedirs(os.path.join(wurzel, "config"))
    # TB-58: der Baum ist ein Git-Repo mit genau einem Commit, traegt die
    # echte Lock-Datei und die Abfrage als Einstiegsdatei.
    with open(os.path.join(wurzel, "abfrage.py"), "w", encoding="utf-8") as datei:
        datei.write(_ABFRAGE)
    if os.path.exists(_ECHTER_LOCK):
        shutil.copy2(_ECHTER_LOCK, os.path.join(wurzel, "requirements.lock"))
    _git(wurzel, "init", "-q")
    _git(wurzel, "add", "-A")
    _git(wurzel, "-c", "user.name=tb53b_test", "-c", "user.email=tb53b@test",
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
    """HEAD des Baums - der Wert fuer TB_SELEKTIONSCOMMIT."""
    return _git(wurzel, "rev-parse", "HEAD")


def _einstiegsdatei(caller):
    """Die Abfrage als Datei: im Wegwerfbaum liegt sie an dessen Wurzel;
    fuer den echten Baum (nur ohne Modus gefragt) eine Wegwerfdatei."""
    wurzel = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(caller))))
    im_baum = os.path.join(wurzel, "abfrage.py")
    if os.path.exists(im_baum):
        return im_baum
    return _ABFRAGE_DATEI


_ABFRAGE_DATEI = os.path.join(tempfile.mkdtemp(prefix="tb53b_abfrage_"),
                              "abfrage.py")


def baue_attrappe(hash_=ATTRAPPEN_HASH):
    """⚠️ KEIN Snapshot von `data/` - ein Wegwerf-Ordner mit Manifest."""
    ordner = tempfile.mkdtemp(prefix="tb53b_attrappe_")
    with open(os.path.join(ordner, "XXXTEST_1d.csv"), "w") as datei:
        datei.write("timestamp,close\n2020-01-01,1.0\n")
    with open(os.path.join(ordner, "MANIFEST.json"), "w") as datei:
        json.dump({"snapshot_hash": hash_, "datenstand_hash": "egal",
                   "kursdateien": 1, "dateien": {"XXXTEST_1d.csv": {}}}, datei)
    return ordner


# Der Probeprozess: die Sicht EINES Bots, genau mit dem Vorspann, den jede
# Bot-Datei traegt. Er ruft die ECHTE Funktion mit dem Pfad, den
# `multi_symbol_optimise.py` dieses Bots haette.
_ABFRAGE = r'''
import json, os, sys
caller = sys.argv[1]
_STRATEGY_DIR = os.path.dirname(os.path.abspath(caller))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)
ergebnis = {}
try:
    from strategy_paths import get_strategy_paths
    ergebnis["pfade"] = get_strategy_paths(caller)
except Exception as fehler:
    ergebnis["fehler"] = "%s: %s" % (type(fehler).__name__, fehler)
    json.dump(ergebnis, sys.stdout); sys.exit(0)
import paths
ergebnis["paths.BASE_DIR"] = paths.BASE_DIR
try:
    ergebnis["LIVE_DATA_DIR"] = paths.LIVE_DATA_DIR
except Exception as fehler:
    ergebnis["live_fehler"] = "%s: %s" % (type(fehler).__name__, fehler)
json.dump(ergebnis, sys.stdout)
'''


def frage(caller, wurzel_env=None, hash_env=None):
    """Die Pfade aus einem eigenen Prozess erfragen (B6, TB-40)."""
    umgebung = dict(os.environ)
    umgebung.pop("TB_SELEKTIONSWURZEL", None)
    umgebung.pop("TB_SELEKTIONSHASH", None)
    umgebung.pop("TB_SELEKTIONSCOMMIT", None)
    if wurzel_env is not None:
        umgebung["TB_SELEKTIONSWURZEL"] = wurzel_env
    if hash_env is not None:
        umgebung["TB_SELEKTIONSHASH"] = hash_env
    einstieg = _einstiegsdatei(caller)
    if wurzel_env is not None and hash_env is not None:
        # TB-58: der vollstaendige Modus traegt den Commit des Baums.
        umgebung["TB_SELEKTIONSCOMMIT"] = commit_von(os.path.dirname(einstieg))
    if not os.path.exists(einstieg):
        with open(einstieg, "w", encoding="utf-8") as datei:
            datei.write(_ABFRAGE)
    lauf = subprocess.run([sys.executable, einstieg, caller],
                          capture_output=True, text=True, env=umgebung)
    try:
        werte = json.loads(lauf.stdout) if lauf.stdout.strip() else {}
    except ValueError:
        werte = {}
    werte["_rc"] = lauf.returncode
    werte["_stderr"] = lauf.stderr
    return werte


def frage_alle(baum, **umgebung):
    """Je Bot ein Prozess; (bot -> Antwort)."""
    return {bot: frage(os.path.join(baum, "strategies", bot,
                                    "multi_symbol_optimise.py"), **umgebung)
            for bot in BOTS}


def _neutral(werte, baum):
    return {k: (v.replace(baum, "<WURZEL>") if isinstance(v, str) else v)
            for k, v in werte.items()}


def alte_fassung():
    lauf = subprocess.run(
        ["git", "-C", _WURZEL, "show",
         "%s:shared/strategy_paths.py" % BEZUGSCOMMIT],
        capture_output=True, text=True)
    if lauf.returncode != 0 or not lauf.stdout.strip():
        return None
    return lauf.stdout


def vergleiche(alt_quelle, neu_quelle):
    """Alle sieben Schluessel, alle neun Bots, alt gegen neu, ohne Modus."""
    baum_alt = baue_baum(alt_quelle)
    baum_neu = baue_baum(neu_quelle)
    try:
        unterschiede = []
        verglichen = 0
        alt_alle = frage_alle(baum_alt)
        neu_alle = frage_alle(baum_neu)
        for bot in BOTS:
            alt, neu = alt_alle[bot], neu_alle[bot]
            if "pfade" not in alt or "pfade" not in neu:
                # A1: gescheitert ist nicht "gleich".
                unterschiede.append({"bot": bot, "name": "<LAUF>",
                                     "alt": alt.get("fehler", alt["_stderr"][-200:]),
                                     "neu": neu.get("fehler", neu["_stderr"][-200:])})
                continue
            a = _neutral(alt["pfade"], baum_alt)
            n = _neutral(neu["pfade"], baum_neu)
            for name in SCHLUESSEL:
                verglichen += 1
                if a.get(name) != n.get(name):
                    unterschiede.append({"bot": bot, "name": name,
                                         "alt": a.get(name), "neu": n.get(name)})
        return {"verglichen": verglichen, "unterschiede": unterschiede}
    finally:
        shutil.rmtree(baum_alt, ignore_errors=True)
        shutil.rmtree(baum_neu, ignore_errors=True)


# ===========================================================================
# Probe A - ohne Modus: alle sieben Pfade je Bot zeichengleich wie vorher
# ===========================================================================

def probe_a_ohne_modus():
    print("\nProbe A - ohne Modus liefert get_strategy_paths() je Bot dieselben "
          "Zeichenketten wie im Bezugscommit")
    alt = alte_fassung()
    if alt is None:
        check("A NICHT PRUEFBAR", False,
              "Bezugscommit %s nicht auffindbar" % BEZUGSCOMMIT[:8])
        return
    ergebnis = vergleiche(alt, quelle())
    check("A1 null Unterschiede", not ergebnis["unterschiede"],
          "%d Pfade verglichen (%d Bots x %d Schluessel), %d Unterschiede"
          % (ergebnis["verglichen"], len(BOTS), len(SCHLUESSEL),
             len(ergebnis["unterschiede"])))
    for u in ergebnis["unterschiede"]:
        print("       ⚠️ %s / %s: %r -> %r" % (u["bot"], u["name"], u["alt"], u["neu"]))

    # ⭐ Und im ECHTEN Baum, je Bot ein Prozess: DATA_DIR ist der Live-Bestand.
    # (Das legt `results/<bot>` und `logs/<bot>` nicht neu an - sie existieren.)
    echt = frage_alle(_WURZEL)
    soll = os.path.join(_WURZEL, "data")
    gleich = [b for b in BOTS if echt[b].get("pfade", {}).get("DATA_DIR") == soll]
    check("A2 im Arbeitsbaum zeigt DATA_DIR bei allen Bots auf data/",
          len(gleich) == len(BOTS), "%d von %d: %s" % (len(gleich), len(BOTS), soll))

    # Mutation: der Datenpfad wird wieder selbst gebaut - und zwar falsch.
    verstellt, griff = mutiere(quelle(), '"DATA_DIR": paths.DATA_DIR',
                               '"DATA_DIR": os.path.join(base_dir, "daten_verstellt")', "A")
    if griff:
        gegen = vergleiche(alt, verstellt)
        check("A3 Mutationsprobe beisst", bool(gegen["unterschiede"]),
              "verstellte Fassung -> %d Unterschiede (ohne die Mutation: %d)"
              % (len(gegen["unterschiede"]), len(ergebnis["unterschiede"])))
    else:
        check("A3 Mutationsprobe", False, "Mutation griff nicht")


# ===========================================================================
# Probe B - mit Modus zeigt DATA_DIR je Bot in den Snapshot, der Betrieb nicht
# ===========================================================================

def probe_b_modus():
    print("\nProbe B - mit Modus zeigt DATA_DIR je Bot in den Snapshot, "
          "RESULTS_DIR/LOGS_DIR/DB_FILE nicht")
    attrappe = baue_attrappe()
    baum = baue_baum(quelle())
    try:
        alle = frage_alle(baum, wurzel_env=attrappe, hash_env=ATTRAPPEN_HASH)
        im_snapshot = [b for b in BOTS
                       if alle[b].get("pfade", {}).get("DATA_DIR") == attrappe]
        check("B1 DATA_DIR zeigt bei allen Bots in den Snapshot",
              len(im_snapshot) == len(BOTS),
              "%d von %d" % (len(im_snapshot), len(BOTS)))
        config = [b for b in BOTS
                  if alle[b].get("pfade", {}).get("CONFIG_DIR") == attrappe]
        check("B2 CONFIG_DIR zeigt bei allen Bots in den Snapshot",
              len(config) == len(BOTS), "%d von %d" % (len(config), len(BOTS)))
        # ⚠️ Der Betrieb bleibt im Baum: kein Ergebnis, kein Log, keine
        # Datenbank darf in den Snapshot zeigen.
        betrieb_ok = all(
            alle[b].get("pfade", {}).get(k, "").startswith(baum)
            and not alle[b]["pfade"][k].startswith(attrappe)
            for b in BOTS for k in BETRIEB)
        check("B3 RESULTS_DIR, LOGS_DIR, DB_FILE bleiben im Betrieb",
              betrieb_ok, "%d Werte, keiner im Snapshot" % (len(BOTS) * len(BETRIEB)))
        check("B4 der Lauf SAGT, dass er im Modus ist",
              all("SELEKTIONSMODUS AKTIV" in alle[b]["_stderr"] for b in BOTS),
              "Prueffrage D1, bei jedem der %d Prozesse" % len(BOTS))

        # Mutation: DATA_DIR wird wieder selbst gebaut - der Modus wird gelesen
        # (paths.py wirft ja nicht), aber nicht angewandt.
        mutiert, griff = mutiere(quelle(), '"DATA_DIR": paths.DATA_DIR',
                                 '"DATA_DIR": os.path.join(base_dir, "data")', "B")
        if griff:
            baum_m = baue_baum(mutiert)
            try:
                wm = frage(os.path.join(baum_m, "strategies", BOTS[0],
                                        "multi_symbol_optimise.py"),
                           wurzel_env=attrappe, hash_env=ATTRAPPEN_HASH)
                check("B5 Mutationsprobe beisst",
                      wm.get("pfade", {}).get("DATA_DIR") != attrappe,
                      "selbst gebaut zeigt DATA_DIR auf %s - die Probe faellt "
                      "dort durch, wie sie soll" % wm.get("pfade", {}).get("DATA_DIR"))
            finally:
                shutil.rmtree(baum_m, ignore_errors=True)
        else:
            check("B5 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        shutil.rmtree(baum, ignore_errors=True)
        shutil.rmtree(attrappe, ignore_errors=True)


# ===========================================================================
# Probe C - falscher Hash: der Import wirft, rc != 0 (Nachweis 3)
# ===========================================================================

def probe_c_falscher_hash():
    print("\nProbe C - mit FALSCHEM Hash wirft schon der Import von "
          "strategy_paths, rc != 0")
    attrappe = baue_attrappe()
    baum = baue_baum(quelle())
    try:
        # ⚠️ Der Probeprozess faengt hier NICHT ab - geprueft wird der
        # Rueckgabewert des Prozesses (TB-52, Messung 5: ein Probeprozess, der
        # die Ausnahme selbst faengt, liefert immer rc=0).
        umgebung = dict(os.environ)
        umgebung["TB_SELEKTIONSWURZEL"] = attrappe
        umgebung["TB_SELEKTIONSHASH"] = "ein_ganz_anderer_hash"
        lauf = subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.path.insert(0, sys.argv[1]); "
             "from strategy_paths import get_strategy_paths; "
             "print(get_strategy_paths(sys.argv[2])['DATA_DIR'])",
             os.path.join(baum, "shared"),
             os.path.join(baum, "strategies", BOTS[0], "multi_symbol_optimise.py")],
            capture_output=True, text=True, env=umgebung)
        check("C1 rc != 0", lauf.returncode != 0, "rc=%d" % lauf.returncode)
        check("C2 es ist der Selektionsfehler aus paths.py",
              "Selektionsfehler" in lauf.stderr and "ein_ganz_anderer_hash" in lauf.stderr,
              lauf.stderr.strip().splitlines()[-1][:100] if lauf.stderr.strip() else "(leer)")
        check("C3 nichts auf stdout - kein Pfad wurde geliefert",
              not lauf.stdout.strip(), repr(lauf.stdout[:60]))

        # Mutation: der zweite Resolver. strategy_paths baut sich sein eigenes
        # `paths` - ohne Hashpruefung. Der falsche Hash faellt dann nicht auf.
        mutiert, griff = mutiere(
            quelle(), "\nimport paths\n",
            "\nimport types as _t\n"
            "paths = _t.SimpleNamespace(\n"
            "    __file__=__file__,\n"
            "    BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n"
            "paths.DATA_DIR = os.path.join(paths.BASE_DIR, 'data')\n"
            "paths.CONFIG_DIR = os.path.join(paths.BASE_DIR, 'config')\n", "C")
        if griff:
            baum_m = baue_baum(mutiert)
            try:
                lauf_m = subprocess.run(
                    [sys.executable, "-c",
                     "import sys; sys.path.insert(0, sys.argv[1]); "
                     "from strategy_paths import get_strategy_paths; "
                     "print(get_strategy_paths(sys.argv[2])['DATA_DIR'])",
                     os.path.join(baum_m, "shared"),
                     os.path.join(baum_m, "strategies", BOTS[0],
                                  "multi_symbol_optimise.py")],
                    capture_output=True, text=True, env=umgebung)
                check("C4 Mutationsprobe beisst",
                      lauf_m.returncode == 0 and lauf_m.stdout.strip(),
                      "mit eigenem Resolver geht der falsche Hash still durch "
                      "(rc=%d, DATA_DIR=%s)" % (lauf_m.returncode, lauf_m.stdout.strip()))
            finally:
                shutil.rmtree(baum_m, ignore_errors=True)
        else:
            check("C4 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        shutil.rmtree(baum, ignore_errors=True)
        shutil.rmtree(attrappe, ignore_errors=True)


# ===========================================================================
# Probe D - mit Modus wirft LIVE_DATA_DIR, und strategy_paths verraet den
#           Live-Pfad nicht auf anderem Weg (Nachweis 4)
# ===========================================================================

def probe_d_live_wirft():
    print("\nProbe D - mit Modus wirft die Anfrage nach LIVE_DATA_DIR "
          "(unveraendert aus TB-52), und get_strategy_paths() verraet den "
          "Live-Pfad nicht")
    attrappe = baue_attrappe()
    baum = baue_baum(quelle())
    try:
        alle = frage_alle(baum, wurzel_env=attrappe, hash_env=ATTRAPPEN_HASH)
        wirft = [b for b in BOTS if "Selektionsfehler" in alle[b].get("live_fehler", "")]
        check("D1 LIVE_DATA_DIR wirft Selektionsfehler - bei allen Bots",
              len(wirft) == len(BOTS), "%d von %d" % (len(wirft), len(BOTS)))
        live = os.path.join(baum, "data")
        leck = [(b, k) for b in BOTS
                for k, v in alle[b].get("pfade", {}).items()
                if isinstance(v, str) and (v == live or v.startswith(live + os.sep))]
        check("D2 kein Wert aus get_strategy_paths() zeigt unter dem Modus "
              "auf den Live-Bestand", not leck, "%d Lecks" % len(leck))

        # Mutation: strategy_paths gibt den Live-Pfad unter einem eigenen
        # Namen mit - am `__getattr__` von paths.py vorbei.
        mutiert, griff = mutiere(
            quelle(), '        "DB_FILE": db_file,\n',
            '        "DB_FILE": db_file,\n'
            '        "LIVE_DATA_DIR": os.path.join(base_dir, "data"),\n', "D")
        if griff:
            baum_m = baue_baum(mutiert)
            try:
                wm = frage(os.path.join(baum_m, "strategies", BOTS[0],
                                        "multi_symbol_optimise.py"),
                           wurzel_env=attrappe, hash_env=ATTRAPPEN_HASH)
                live_m = os.path.join(baum_m, "data")
                check("D3 Mutationsprobe beisst",
                      any(v == live_m for v in wm.get("pfade", {}).values()),
                      "mit dem Zusatzschluessel steht der Live-Pfad im Ergebnis")
            finally:
                shutil.rmtree(baum_m, ignore_errors=True)
        else:
            check("D3 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        shutil.rmtree(baum, ignore_errors=True)
        shutil.rmtree(attrappe, ignore_errors=True)


# ===========================================================================
# Probe E - die Wurzeln der neun Bots (gemessen) und der Nachbar-Resolver
#           (zugesichert) - Schritt 1 / Bedingung 3
# ===========================================================================

def probe_e_wurzel_und_nachbar():
    print("\nProbe E - die Wurzel jedes echten Bots ist die Wurzel von paths.py "
          "(gemessen), und ein fremdes paths wirft (zugesichert)")
    # E1: im ECHTEN Baum, je Bot ein Prozess, aus der Sicht dieses Bots.
    # ⚠️ Das ist die Messung aus TB-53b Schritt 1 - sie steht hier, nicht im
    # Quelltext von strategy_paths.py (Entscheidung des Betreibers 19.09.2026:
    # Werkzeuge laden absichtlich Bot-Kopien aus Wegwerfbaeumen mit der
    # echten shared/).
    echt = frage_alle(_WURZEL)
    gleich = [b for b in BOTS if "pfade" in echt[b]
              and echt[b]["pfade"]["BASE_DIR"] == echt[b].get("paths.BASE_DIR")]
    check("E1 alle echten Bots: base_dir zeichengleich mit paths.BASE_DIR",
          len(gleich) == len(BOTS),
          "%d von %d, Wurzel %s" % (len(gleich), len(BOTS),
                                     echt[BOTS[0]].get("paths.BASE_DIR")))

    baum = baue_baum(quelle(), mit_paths=False)
    fremd = tempfile.mkdtemp(prefix="tb53b_fremd_")
    kopie = tempfile.mkdtemp(prefix="tb53b_kopie_")
    try:
        # E2: ein FREMDES paths.py - gleicher Inhalt, anderer Ort - liegt vor
        # der shared/ des Baums auf sys.path. strategy_paths muss es ablehnen.
        os.makedirs(os.path.join(fremd, "shared"))
        shutil.copy2(_PATHS_QUELLE, os.path.join(fremd, "shared", "paths.py"))
        programm = ("import sys; sys.path.insert(0, sys.argv[1]); "
                    "sys.path.insert(0, sys.argv[2]); "
                    "from strategy_paths import get_strategy_paths; "
                    "print(get_strategy_paths(sys.argv[3])['DATA_DIR'])")
        caller = os.path.join(baum, "strategies", BOTS[0], "multi_symbol_optimise.py")
        lauf = subprocess.run([sys.executable, "-c", programm,
                               os.path.join(baum, "shared"), os.path.join(fremd, "shared"), caller],
                              capture_output=True, text=True)
        check("E2 fremdes paths -> Resolverfehler, rc != 0",
              lauf.returncode != 0 and "Resolverfehler" in lauf.stderr,
              "rc=%d" % lauf.returncode)
        check("E3 die Meldung nennt das fremde und das erwartete paths.py",
              fremd in lauf.stderr and os.path.join(baum, "shared") in lauf.stderr,
              "beide Orte")

        # E4: das Werkzeugmuster - eine Bot-Kopie in einem Wegwerfbaum, geladen
        # mit der shared/ des Projekts (hier: des Baums). KEIN Fehler; die
        # Kursdaten kommen aus dem Resolver, Ergebnisse und Datenbank bleiben
        # in der Kopie. So arbeiten determinismus_lauf.py --basis,
        # test_ladeprotokoll.py und test_wellenauswahl.py.
        shutil.copy2(_PATHS_QUELLE, os.path.join(baum, "shared", "paths.py"))
        os.makedirs(os.path.join(kopie, "strategies", BOTS[0]))
        # ⚠️ frage() baut sys.path aus der Lage des Aufrufers - fuer die Kopie
        # gaebe es dort keine shared/. Deshalb ausdruecklich mit der shared/
        # des Baums:
        lauf_k = subprocess.run(
            [sys.executable, "-c",
             "import sys, json; sys.path.insert(0, sys.argv[1]); "
             "from strategy_paths import get_strategy_paths; "
             "json.dump(get_strategy_paths(sys.argv[2]), sys.stdout)",
             os.path.join(baum, "shared"),
             os.path.join(kopie, "strategies", BOTS[0], "x.py")],
            capture_output=True, text=True)
        pk = json.loads(lauf_k.stdout) if lauf_k.returncode == 0 else {}
        check("E4 Werkzeugmuster (Bot-Kopie, echte shared/) laeuft durch",
              lauf_k.returncode == 0
              and pk.get("DATA_DIR") == os.path.join(baum, "data")
              and pk.get("DB_FILE", "").startswith(kopie),
              "DATA_DIR aus dem Resolver, DB_FILE in der Kopie"
              if lauf_k.returncode == 0 else lauf_k.stderr.strip()[-200:])

        # Mutation: ohne die Zusicherung liefert ein fremdes paths STILL.
        mutiert, griff = mutiere(quelle(), "    if not _resolver_ist_nachbar():\n        raise",
                                 "    if False:\n        raise", "E")
        if griff:
            baum_m = baue_baum(mutiert, mit_paths=False)
            try:
                lauf_m = subprocess.run(
                    [sys.executable, "-c", programm, os.path.join(baum_m, "shared"),
                     os.path.join(fremd, "shared"),
                     os.path.join(baum_m, "strategies", BOTS[0],
                                         "multi_symbol_optimise.py")],
                    capture_output=True, text=True)
                check("E5 Mutationsprobe beisst",
                      lauf_m.returncode == 0
                      and lauf_m.stdout.strip() == os.path.join(fremd, "data"),
                      "ohne Zusicherung: DATA_DIR still aus dem fremden Resolver (%s)"
                      % lauf_m.stdout.strip())
            finally:
                shutil.rmtree(baum_m, ignore_errors=True)
        else:
            check("E5 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        shutil.rmtree(baum, ignore_errors=True)
        shutil.rmtree(fremd, ignore_errors=True)
        shutil.rmtree(kopie, ignore_errors=True)


# ===========================================================================
# Probe F - kein zweiter Resolver (T55.8, T54.3), am Syntaxbaum gemessen
# ===========================================================================

_VERBOTENE_KONSTANTEN = ("TB_SELEKTIONSWURZEL", "TB_SELEKTIONSHASH",
                         "MANIFEST.json", "snapshot_hash")


def _zweiter_resolver(text):
    """Was im Quelltext nach einem eigenen Resolver aussieht (B5)."""
    baum = ast.parse(text)
    funde = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Constant) and knoten.value in _VERBOTENE_KONSTANTEN:
            funde.append("Konstante %r (Zeile %d)" % (knoten.value, knoten.lineno))
        elif isinstance(knoten, ast.Attribute) and knoten.attr == "environ":
            funde.append("os.environ (Zeile %d)" % knoten.lineno)
        elif isinstance(knoten, ast.ClassDef) and knoten.name == "Selektionsfehler":
            funde.append("class Selektionsfehler (Zeile %d)" % knoten.lineno)
        elif isinstance(knoten, ast.Import) and any(a.name == "json" for a in knoten.names):
            funde.append("import json (Zeile %d)" % knoten.lineno)
    return funde


def probe_f_kein_zweiter_resolver():
    print("\nProbe F - strategy_paths.py traegt keinen zweiten Resolver")
    funde = _zweiter_resolver(quelle())
    check("F1 keine Umgebungsvariable, kein Manifest, kein eigener "
          "Selektionsfehler", not funde, "; ".join(funde) or "0 Funde")
    check("F2 paths.py wird importiert, nicht nachgebaut",
          any(isinstance(k, ast.Import) and any(a.name == "paths" for a in k.names)
              for k in ast.walk(ast.parse(quelle()))), "import paths")

    mutiert, griff = mutiere(
        quelle(), "\nimport paths\n",
        "\nimport paths\n_EIGEN = os.environ.get(\"TB_SELEKTIONSHASH\")\n", "F")
    if griff:
        check("F3 Mutationsprobe beisst", bool(_zweiter_resolver(mutiert)),
              "%d Funde in der Fassung mit eigener Umgebungslese"
              % len(_zweiter_resolver(mutiert)))
    else:
        check("F3 Mutationsprobe", False, "Mutation griff nicht")


def main():
    print("=" * 78)
    print("Selbsttests zu shared/strategy_paths.py - DATA_DIR aus dem Resolver (TB-53b)")
    print("=" * 78)
    for name, probe in (("A", probe_a_ohne_modus),
                        ("B", probe_b_modus),
                        ("C", probe_c_falscher_hash),
                        ("D", probe_d_live_wirft),
                        ("E", probe_e_wurzel_und_nachbar),
                        ("F", probe_f_kein_zweiter_resolver)):
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
