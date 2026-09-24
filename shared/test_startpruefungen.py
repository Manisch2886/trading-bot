#!/usr/bin/env python3
"""
Selbsttests zu shared/paths.py - die Startpruefungen des Selektionsmodus (TB-58)
==============================================================================
    "Der Lese-Audit beweist, welche DATEN gelesen wurden. Er sagt nichts
     darueber, welcher CODE gelesen hat."

Seit TB-58 prueft `shared/paths.py` beim Import **unter dem Modus** die
Codeherkunft (derselbe Git-Baum, erwarteter Commit, sauberer Arbeitsbaum) und
den Lock (`requirements.lock` gegen `sys.version`, `platform.platform()` und
`importlib.metadata`). Bei Verletzung: Abbruch mit Rueckgabewert **2**.
Bestanden: acht Auditzeilen auf `stderr`, abrufbar ueber `startpruefung()`
und `audit_zeilen()`. Diese Datei ist die Wache dafuer.

⚠️⚠️ **Die wichtigste Bedingung steht zuerst (Probe N):** ohne Modus tut
das Modul davon **nichts** - kein `git`-Aufruf, keine Paketabfrage, kein
Import von `subprocess`/`importlib.metadata`/`platform`/`hashlib`. Gemessen
mit einer zaehlenden Attrappe **vor** dem Import (N1) und am Syntaxbaum (N3,
Prueffrage B5), und dazu die Zeichengleichheit aller Pfade gegen den Stand
**vor** TB-58 (N4, Bezugscommit festgenagelt, Prueffrage A7/B3).

**Wie geprueft wird.** Jede Probe baut ein **eigenes Git-Repo** in einem
Wegwerfordner (`shared/paths.py` = die Fassung unter Pruefung, die echte
`requirements.lock`, ein Einstiegspunkt `strategies/probe/lauf.py`, ein
Commit) und startet **einen eigenen Prozess** aus dieser Datei heraus
(TB-40; `python -c` hat keinen `__file__` und ist selbst ein Pruefall, S3).
Der Arbeitsbaum des Projekts wird **nicht** angefasst - auch nicht fuer den
"schmutzigen Arbeitsbaum": der wird im Wegwerf-Repo hergestellt.

⚠️ **Jede Probe hat ihre Mutationsgegenprobe** (Prueffrage B1): dieselbe Probe
gegen eine Fassung, der **genau die eine Bedingung fehlt**, muss dort
**durchgehen**. Eine Mutation, die nicht greift, ist **NICHT PRUEFBAR**
(Prueffrage A2), nicht gruen.

Nutzung:  python3 shared/test_startpruefungen.py
"""

import ast
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
_PFADVERGLEICH = os.path.join(_WURZEL, "research", "resolver_selektion",
                              "pfadvergleich.py")

# ⚠️ Festgenagelt (Prueffrage B3): der letzte Commit VOR TB-58 - die Fassung
# von `paths.py` ohne Startpruefungen. Gegen sie wird die Zeichengleichheit
# aller Pfade ohne Modus gemessen (Prueffrage A7).
BEZUGSCOMMIT = "624853bde3ac8ca362f4f43aa86a2ae0c7d30741"

ATTRAPPEN_HASH = "attrappe000000000000000000000000"

# TB-103: die Universumsdateien der Attrappe, Anordnung wie im echten Snapshot
# (`config/` unter der Wurzel, im MANIFEST unter `dateien` genannt).
UNIVERSUM = {"config/top25_symbols.txt": "AAAUSDT\nBBBUSDT\nCCCUSDT\n",
             "config/sp500_top150.txt": "AAA\nBBB\n"}
RC_ERWARTET = 2
AUDIT_SCHLUESSEL = ("codewurzel", "commit", "arbeitsbaum", "lock_sha256",
                    "interpreter", "plattform", "snapshot_wurzel",
                    "snapshot_hash")

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
    """Eine Mutation anbringen - oder sagen, dass sie nicht gegriffen hat."""
    if text.count(alt) != 1:
        print("  [NICHT PRUEFBAR] Mutation %s griff nicht: %r kommt %d-mal vor."
              % (marke, alt[:60], text.count(alt)))
        return text, False
    return text.replace(alt, neu), True


def kurz(text, n=160):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n] + "..."


# ---------------------------------------------------------------------------
# Wegwerf-Repo, Attrappe, Probeprozess
# ---------------------------------------------------------------------------

def _git(wurzel, *argumente):
    lauf = subprocess.run(["git", "-C", wurzel] + list(argumente),
                          capture_output=True, text=True)
    if lauf.returncode != 0:
        raise RuntimeError("git %s in %s: rc %d, %s"
                           % (" ".join(argumente), wurzel, lauf.returncode,
                              lauf.stderr.strip()))
    return lauf.stdout.strip()


def commit(wurzel, meldung="Wegwerfbaum"):
    _git(wurzel, "add", "-A")
    _git(wurzel, "-c", "user.name=tb58_test", "-c", "user.email=tb58@test",
         "commit", "-q", "--allow-empty", "-m", meldung)
    return _git(wurzel, "rev-parse", "HEAD")


# Der Einstiegspunkt: eine Datei unter strategies/, wie jede Bot-Datei.
_LAUF = r'''
import json, os, sys
_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(_HIER)), "shared"))
import paths
json.dump({"DATA_DIR": paths.DATA_DIR,
           "startpruefung": paths.startpruefung(),
           "audit_zeilen": paths.audit_zeilen()}, sys.stdout)
'''


def baue_repo(paths_quelle, lock_quelle=None):
    """Ein Git-Repo in der Form des Projekts, mit genau einem Commit.

    `lock_quelle`: Text der Lock-Datei; ohne Angabe die echte. `None` als
    Text ist erlaubt, wenn `lock_quelle=""` uebergeben wird - dann fehlt sie.
    """
    wurzel = tempfile.mkdtemp(prefix="tb58_repo_")
    os.makedirs(os.path.join(wurzel, "shared"))
    os.makedirs(os.path.join(wurzel, "strategies", "probe"))
    os.makedirs(os.path.join(wurzel, "data"))
    os.makedirs(os.path.join(wurzel, "config"))
    with open(os.path.join(wurzel, "shared", "paths.py"), "w",
              encoding="utf-8") as datei:
        datei.write(paths_quelle)
    with open(os.path.join(wurzel, "strategies", "probe", "lauf.py"), "w",
              encoding="utf-8") as datei:
        datei.write(_LAUF)
    if lock_quelle is None:
        shutil.copy2(_ECHTER_LOCK, os.path.join(wurzel, "requirements.lock"))
    elif lock_quelle != "":
        with open(os.path.join(wurzel, "requirements.lock"), "w",
                  encoding="utf-8") as datei:
            datei.write(lock_quelle)
    _git(wurzel, "init", "-q")
    return wurzel, commit(wurzel)


def baue_attrappe(hash_=ATTRAPPEN_HASH):
    """⚠️ KEIN Snapshot von `data/` - ein Wegwerf-Ordner mit Manifest."""
    ordner = tempfile.mkdtemp(prefix="tb58_attrappe_")
    with open(os.path.join(ordner, "XXXTEST_1d.csv"), "w") as datei:
        datei.write("timestamp,close\n2020-01-01,1.0\n")
    with open(os.path.join(ordner, "MANIFEST.json"), "w") as datei:
        json.dump({"snapshot_hash": hash_, "datenstand_hash": "egal",
                   "kursdateien": 1,
                   "dateien": dict({"XXXTEST_1d.csv": {}},
                                   **{name: {} for name in UNIVERSUM})}, datei)
    # TB-103: seit dem Resolver-Fix verlangt der Modus die Universumsdateien
    # unter <snapshot>/config/, wie sie das MANIFEST nennt - sonst rc 2.
    os.makedirs(os.path.join(ordner, "config"))
    for name, text in UNIVERSUM.items():
        with open(os.path.join(ordner, name), "w") as datei:
            datei.write(text)
    return ordner


def umgebung_ohne_modus():
    umgebung = dict(os.environ)
    for name in ("TB_SELEKTIONSWURZEL", "TB_SELEKTIONSHASH",
                 "TB_SELEKTIONSCOMMIT"):
        umgebung.pop(name, None)
    return umgebung


def lauf(einstieg, attrappe=None, hash_=ATTRAPPEN_HASH, commit_=None,
         python=None):
    """Einen Probeprozess aus `einstieg` starten; Ergebnis als dict.

    Ohne `attrappe` laeuft er ohne Modus. `commit_=None` bei gesetztem
    Modus heisst: TB_SELEKTIONSCOMMIT wird NICHT gesetzt.
    """
    umgebung = umgebung_ohne_modus()
    if attrappe is not None:
        umgebung["TB_SELEKTIONSWURZEL"] = attrappe
        umgebung["TB_SELEKTIONSHASH"] = hash_
        if commit_ is not None:
            umgebung["TB_SELEKTIONSCOMMIT"] = commit_
    befehl = [sys.executable] + (einstieg if isinstance(einstieg, list)
                                 else [einstieg])
    ergebnis = subprocess.run(befehl, capture_output=True, text=True,
                              env=umgebung)
    werte = {}
    if ergebnis.stdout.strip():
        try:
            werte = json.loads(ergebnis.stdout)
        except ValueError:
            werte = {"_stdout": ergebnis.stdout}
    werte["_rc"] = ergebnis.returncode
    werte["_stderr"] = ergebnis.stderr
    return werte


def lauf_im_repo(wurzel, **argumente):
    return lauf(os.path.join(wurzel, "strategies", "probe", "lauf.py"),
                **argumente)


def verletzt(w):
    return "STARTPRUEFUNG VERLETZT" in w.get("_stderr", "")


def raeume(*ordner):
    for o in ordner:
        if o:
            shutil.rmtree(o, ignore_errors=True)


# ===========================================================================
# Probe N - ohne Modus: NICHTS (Nachweis 1 und 2)
# ===========================================================================

_ATTRAPPE_ZAEHLER = r'''
import json, os, sys, subprocess, platform, hashlib
from importlib import metadata
zaehler = {"subprocess": 0, "metadata": 0, "os_prozess": 0}
def zaehle(schluessel, original):
    def ersatz(*a, **k):
        zaehler[schluessel] += 1
        return original(*a, **k)
    return ersatz
for name in ("run", "Popen", "call", "check_call", "check_output"):
    setattr(subprocess, name, zaehle("subprocess", getattr(subprocess, name)))
for name in ("version", "distribution", "distributions", "metadata"):
    setattr(metadata, name, zaehle("metadata", getattr(metadata, name)))
for name in ("system", "popen"):
    setattr(os, name, zaehle("os_prozess", getattr(os, name)))
sys.path.insert(0, sys.argv[1])
import paths
zaehler["DATA_DIR"] = paths.DATA_DIR
zaehler["startpruefung"] = paths.startpruefung()
zaehler["audit_zeilen"] = paths.audit_zeilen()
zaehler["modulnamen"] = sorted(n for n in ("subprocess", "platform", "hashlib",
                                           "metadata") if hasattr(paths, n))
json.dump(zaehler, sys.stdout)
'''


def probe_n_ohne_modus_nichts():
    print("\nProbe N - ohne Modus: kein git-Aufruf, keine Paketabfrage, "
          "alle Pfade wie vor TB-58")
    wurzel, _ = baue_repo(quelle())
    attrappe_datei = os.path.join(wurzel, "zaehler.py")
    with open(attrappe_datei, "w", encoding="utf-8") as datei:
        datei.write(_ATTRAPPE_ZAEHLER)
    try:
        w = lauf([attrappe_datei, os.path.join(wurzel, "shared")])
        if w["_rc"] != 0 or "subprocess" not in w:
            check("N1 NICHT PRUEFBAR", False,
                  "die Attrappe lieferte nichts (rc=%d): %s"
                  % (w["_rc"], kurz(w.get("_stderr", ""))))
        else:
            check("N1 ohne Modus: 0 subprocess-Aufrufe, 0 Paketabfragen",
                  w["subprocess"] == 0 and w["metadata"] == 0
                  and w["os_prozess"] == 0,
                  "subprocess %d / importlib.metadata %d / os.system,popen %d"
                  % (w["subprocess"], w["metadata"], w["os_prozess"]))
            check("N2 ohne Modus: startpruefung() ist None, audit_zeilen() leer, "
                  "kein subprocess/platform/hashlib/metadata im Modul",
                  w["startpruefung"] is None and w["audit_zeilen"] == []
                  and w["modulnamen"] == [],
                  "Modulnamen im Namensraum: %s" % (w["modulnamen"] or "keine"))

        # --- N3: am Syntaxbaum - die Importe stehen NUR in Funktionen ------
        baum = ast.parse(quelle())
        oben = []
        for knoten in baum.body:
            if isinstance(knoten, (ast.Import, ast.ImportFrom)):
                namen = [a.name for a in knoten.names]
                modul = getattr(knoten, "module", None) or ""
                for name in namen + [modul]:
                    wurzelname = name.split(".")[0]
                    if wurzelname in ("subprocess", "importlib", "platform",
                                      "hashlib"):
                        oben.append(name)
        check("N3 Syntaxbaum: subprocess/importlib/platform/hashlib werden auf "
              "Modulebene nicht importiert", not oben,
              "auf Modulebene: %s" % (oben or "keiner"))

        # --- Mutation N: ein git-Aufruf und eine Paketabfrage beim Import --
        mutiert, griff = mutiere(
            quelle(), "_MODUS = _modus_aus_umgebung()\n",
            "import subprocess as _sp\n"
            "_sp.run(['git', '-C', BASE_DIR, 'rev-parse', 'HEAD'], "
            "capture_output=True)\n"
            "from importlib import metadata as _md\n"
            "_md.version('pip')\n"
            "_MODUS = _modus_aus_umgebung()\n", "N")
        if griff:
            wurzel_m, _ = baue_repo(mutiert)
            datei_m = os.path.join(wurzel_m, "zaehler.py")
            with open(datei_m, "w", encoding="utf-8") as datei:
                datei.write(_ATTRAPPE_ZAEHLER)
            try:
                wm = lauf([datei_m, os.path.join(wurzel_m, "shared")])
                check("N1/N2 Mutationsprobe beisst",
                      wm.get("subprocess", 0) >= 1 and wm.get("metadata", 0) >= 1,
                      "mit einem git-Aufruf und einer Paketabfrage im Import "
                      "zaehlt die Attrappe %s / %s"
                      % (wm.get("subprocess"), wm.get("metadata")))
                oben_m = [k for k in ast.parse(mutiert).body
                          if isinstance(k, (ast.Import, ast.ImportFrom))
                          and any(a.name.split(".")[0] in ("subprocess",
                                                            "importlib")
                                  or (getattr(k, "module", "") or "")
                                  .startswith("importlib")
                                  for a in k.names)]
                check("N3 Mutationsprobe beisst", len(oben_m) >= 1,
                      "%d Import(e) auf Modulebene gefunden" % len(oben_m))
            finally:
                raeume(wurzel_m)
        else:
            check("N Mutationsprobe", False, "Mutation griff nicht")

        # --- N4: Zeichengleichheit aller Pfade gegen den Bezugscommit -------
        if not os.path.exists(_PFADVERGLEICH):
            check("N4 NICHT PRUEFBAR", False, "%s fehlt" % _PFADVERGLEICH)
            return
        spec = importlib.util.spec_from_file_location("tb58_pfadvergleich",
                                                      _PFADVERGLEICH)
        modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modul)
        alt = subprocess.run(
            ["git", "-C", _WURZEL, "show", "%s:shared/paths.py" % BEZUGSCOMMIT],
            capture_output=True, text=True)
        if alt.returncode != 0 or not alt.stdout.strip():
            check("N4 NICHT PRUEFBAR", False,
                  "Bezugscommit %s nicht auffindbar" % BEZUGSCOMMIT[:8])
            return
        ergebnis = modul.vergleiche(alt.stdout, quelle())
        check("N4 ohne Modus: alle Pfade zeichengleich wie in %s"
              % BEZUGSCOMMIT[:8], not ergebnis["unterschiede"],
              "%d Pfade verglichen (%d Bots), %d Unterschiede"
              % (ergebnis["verglichen"], len(modul.BOTS),
                 len(ergebnis["unterschiede"])))
        for u in ergebnis["unterschiede"][:5]:
            print("       ⚠️ %s / %s: %r -> %r"
                  % (u["bot"], u["name"], u["alt"], u["neu"]))
        verstellt, griff = mutiere(quelle(), 'os.path.join(BASE_DIR, "data")',
                                   'os.path.join(BASE_DIR, "daten_verstellt")',
                                   "N4")
        if griff:
            gegen = modul.vergleiche(alt.stdout, verstellt)
            check("N4 Mutationsprobe beisst", bool(gegen["unterschiede"]),
                  "verstellte Fassung -> %d Unterschiede"
                  % len(gegen["unterschiede"]))
        else:
            check("N4 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        raeume(wurzel)


# ===========================================================================
# Probe S - mit vollstaendigem, richtigem Modus: geht durch, Audit erscheint
# ===========================================================================

def probe_s_vollstaendig():
    print("\nProbe S - vollstaendiger, richtiger Modus: rc 0, Auditzeilen")
    wurzel, head = baue_repo(quelle())
    attrappe = baue_attrappe()
    try:
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("S1 Lauf geht durch (rc 0), DATA_DIR im Snapshot",
              w["_rc"] == 0 and w.get("DATA_DIR") == attrappe,
              "rc=%d, DATA_DIR=%s" % (w["_rc"], w.get("DATA_DIR")))
        start = w.get("startpruefung") or {}
        check("S2 startpruefung() traegt alle acht Schluessel",
              tuple(sorted(start)) == tuple(sorted(AUDIT_SCHLUESSEL)),
              ", ".join(sorted(start)))
        check("S3 Werte stimmen: codewurzel, commit, arbeitsbaum, snapshot",
              os.path.realpath(start.get("codewurzel", "")) ==
              os.path.realpath(wurzel)
              and start.get("commit") == head
              and start.get("arbeitsbaum") == "sauber"
              and start.get("snapshot_wurzel") == attrappe
              and start.get("snapshot_hash") == ATTRAPPEN_HASH,
              "commit %s, arbeitsbaum %s" % (start.get("commit", "")[:8],
                                             start.get("arbeitsbaum")))
        import hashlib
        with open(_ECHTER_LOCK, "rb") as datei:
            soll_sha = hashlib.sha256(datei.read()).hexdigest()
        check("S4 lock_sha256 ist der SHA-256 der Lock-Datei",
              start.get("lock_sha256") == soll_sha, soll_sha[:16] + "...")
        check("S5 interpreter und plattform sind gemessen, nicht leer",
              start.get("interpreter", "").startswith(
                  "%d.%d" % sys.version_info[:2])
              and bool(start.get("plattform")),
              kurz(start.get("interpreter", ""), 60))
        stderr_zeilen = [z[len("[paths] "):] for z in
                         w["_stderr"].splitlines() if z.startswith("[paths] ")]
        audit_im_stderr = [z for z in stderr_zeilen
                           if z.split()[0] in AUDIT_SCHLUESSEL]
        check("S6 dieselben acht Zeilen stehen auf stderr in der [paths]-Form",
              audit_im_stderr == w.get("audit_zeilen")
              and len(audit_im_stderr) == 8
              and [z.split()[0] for z in audit_im_stderr]
              == list(AUDIT_SCHLUESSEL),
              "%d Auditzeilen, Reihenfolge fest" % len(audit_im_stderr))
        check("S7 der Lauf SAGT weiterhin, dass er im Modus ist",
              "SELEKTIONSMODUS AKTIV" in w["_stderr"], "Prueffrage D1")

        # --- ein Kindprozess erbt alle drei und geht ebenso durch ------------
        kind_datei = os.path.join(wurzel, "strategies", "probe", "eltern.py")
        with open(kind_datei, "w", encoding="utf-8") as datei:
            datei.write("import subprocess, sys, os\n"
                        "l = subprocess.run([sys.executable, os.path.join("
                        "os.path.dirname(os.path.abspath(__file__)), 'lauf.py')],"
                        " capture_output=True, text=True)\n"
                        "sys.stdout.write(l.stdout); sys.stderr.write(l.stderr)\n"
                        "sys.exit(l.returncode)\n")
        head2 = commit(wurzel, "Elternprozess")
        wk = lauf(kind_datei, attrappe=attrappe, commit_=head2)
        check("S8 ein Kindprozess erbt alle drei Variablen und geht durch",
              wk["_rc"] == 0 and (wk.get("startpruefung") or {}).get("commit")
              == head2, "rc=%d" % wk["_rc"])

        # --- S9: `python -c` hat keinen Einstiegspunkt -> rc 2 -------------
        wc = lauf(["-c", "import sys; sys.path.insert(0, %r); import paths"
                   % os.path.join(wurzel, "shared")],
                  attrappe=attrappe, commit_=head2)
        check("S9 `python -c` (kein __file__) -> rc 2, Meldung nennt den Grund",
              wc["_rc"] == RC_ERWARTET and "Einstiegspunkt" in wc["_stderr"],
              "rc=%d" % wc["_rc"])

        # --- Mutation S: die Auditzeilen werden nicht geschrieben -----------
        mutiert, griff = mutiere(
            quelle(), "for _z in audit_zeilen()))", "for _z in []))", "S")
        if griff:
            wurzel_m, head_m = baue_repo(mutiert)
            try:
                wm = lauf_im_repo(wurzel_m, attrappe=attrappe, commit_=head_m)
                zeilen_m = [z for z in wm["_stderr"].splitlines()
                            if z.startswith("[paths] ") and
                            z.split()[1] in AUDIT_SCHLUESSEL]
                check("S6 Mutationsprobe beisst",
                      wm["_rc"] == 0 and not zeilen_m,
                      "ohne die Schleife: rc %d, %d Auditzeilen auf stderr"
                      % (wm["_rc"], len(zeilen_m)))
            finally:
                raeume(wurzel_m)
        else:
            check("S Mutationsprobe", False, "Mutation griff nicht")
    finally:
        raeume(wurzel, attrappe)


# ===========================================================================
# Probe C - Commit: falsch, fehlend, Zweigname, allein
# ===========================================================================

def probe_c_commit():
    print("\nProbe C - falscher, fehlender, beweglicher Commit")
    wurzel, head = baue_repo(quelle())
    attrappe = baue_attrappe()
    try:
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_="0123456789abcdef")
        check("C1 falscher Commit -> rc 2, Meldung nennt HEAD und Soll",
              w["_rc"] == RC_ERWARTET and verletzt(w)
              and head in w["_stderr"] and "0123456789abcdef" in w["_stderr"],
              "rc=%d, kein stdout: %s" % (w["_rc"], "DATA_DIR" not in w))
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=None)
        check("C2 TB_SELEKTIONSCOMMIT fehlt bei gesetzten anderen beiden -> rc 2",
              w["_rc"] == RC_ERWARTET and verletzt(w)
              and "TB_SELEKTIONSCOMMIT fehlt" in w["_stderr"],
              "rc=%d" % w["_rc"])
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_="master")
        check("C3 Zweigname statt Commit -> rc 2 (bewegliche Referenz, B3)",
              w["_rc"] == RC_ERWARTET and verletzt(w)
              and "kein Commit-Bezeichner" in w["_stderr"], "rc=%d" % w["_rc"])
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head[:7])
        check("C4 abgekuerzter Commit (7 Zeichen) wird angenommen",
              w["_rc"] == 0 and (w.get("startpruefung") or {}).get("commit")
              == head, "rc=%d" % w["_rc"])
        # der Commit allein, ohne Wurzel und Hash: der halbe Modus wirft
        umgebung = umgebung_ohne_modus()
        umgebung["TB_SELEKTIONSCOMMIT"] = head
        allein = subprocess.run(
            [sys.executable, os.path.join(wurzel, "strategies", "probe",
                                          "lauf.py")],
            capture_output=True, text=True, env=umgebung)
        check("C5 TB_SELEKTIONSCOMMIT allein -> Selektionsfehler, rc != 0",
              allein.returncode != 0 and "Selektionsfehler" in allein.stderr
              and "allein" in allein.stderr, "rc=%d" % allein.returncode)

        # --- Mutation C1: die HEAD-Pruefung fehlt ---------------------------
        mutiert, griff = mutiere(
            quelle(), "    if not head.lower().startswith(soll):",
            "    if False:", "C1")
        if griff:
            wurzel_m, head_m = baue_repo(mutiert)
            try:
                wm = lauf_im_repo(wurzel_m, attrappe=attrappe,
                                  commit_="0123456789abcdef")
                check("C1 Mutationsprobe beisst",
                      wm["_rc"] == 0 and wm.get("DATA_DIR") == attrappe,
                      "ohne die Pruefung laeuft der falsche Commit durch: rc %d"
                      % wm["_rc"])
            finally:
                raeume(wurzel_m)
        else:
            check("C1 Mutationsprobe", False, "Mutation griff nicht")

        # --- Mutation C2: fehlt die Variable, nimmt der Lauf still HEAD -----
        mutiert, griff = mutiere(
            quelle(),
            '    erwartet = (umg.get(UMGEBUNG_COMMIT) or "").strip()\n'
            "    if not erwartet:\n",
            '    erwartet = (umg.get(UMGEBUNG_COMMIT) or "").strip() or _git(\n'
            "        _git_wurzel(os.path.realpath(__file__ if hier is None "
            "else hier)),\n"
            '        "rev-parse", "HEAD").strip()\n'
            "    if False:\n", "C2")
        if griff:
            wurzel_m, head_m = baue_repo(mutiert)
            try:
                wm = lauf_im_repo(wurzel_m, attrappe=attrappe, commit_=None)
                check("C2 Mutationsprobe beisst",
                      wm["_rc"] == 0 and wm.get("DATA_DIR") == attrappe,
                      "mit stillem HEAD-Rueckfall laeuft der halbe Modus "
                      "durch: rc %d" % wm["_rc"])
            finally:
                raeume(wurzel_m)
        else:
            check("C2 Mutationsprobe", False, "Mutation griff nicht")
    finally:
        raeume(wurzel, attrappe)


# ===========================================================================
# Probe G - der gespaltene Baum (Nachweis 6)
# ===========================================================================

def probe_g_gespaltener_baum():
    print("\nProbe G - gespaltener Baum: Aufrufer woanders, shared/ hier")
    wurzel, head = baue_repo(quelle())
    attrappe = baue_attrappe()
    fremd_repo = tempfile.mkdtemp(prefix="tb58_fremdrepo_")
    fremd_ohne = tempfile.mkdtemp(prefix="tb58_fremdordner_")
    try:
        # Der Aufrufer zeigt fest auf das shared/ des Repos unter Pruefung.
        aufrufer = ("import json, sys\nsys.path.insert(0, %r)\nimport paths\n"
                    "json.dump({'DATA_DIR': paths.DATA_DIR}, sys.stdout)\n"
                    % os.path.join(wurzel, "shared"))
        for ordner in (fremd_repo, fremd_ohne):
            with open(os.path.join(ordner, "lauf.py"), "w",
                      encoding="utf-8") as datei:
                datei.write(aufrufer)
        _git(fremd_repo, "init", "-q")
        commit(fremd_repo, "fremder Baum")

        w = lauf(os.path.join(fremd_repo, "lauf.py"), attrappe=attrappe,
                 commit_=head)
        check("G1 Aufrufer aus einem ANDEREN Git-Baum -> rc 2, Meldung nennt "
              "beide Wurzeln",
              w["_rc"] == RC_ERWARTET and verletzt(w)
              and "Gespaltener Baum" in w["_stderr"]
              and os.path.realpath(fremd_repo) in w["_stderr"]
              and os.path.realpath(wurzel) in w["_stderr"],
              "rc=%d, kein stdout: %s" % (w["_rc"], "DATA_DIR" not in w))
        w = lauf(os.path.join(fremd_ohne, "lauf.py"), attrappe=attrappe,
                 commit_=head)
        check("G2 Aufrufer aus einem Ordner OHNE Git -> rc 2",
              w["_rc"] == RC_ERWARTET and verletzt(w)
              and "keinem Git-Arbeitsbaum" in w["_stderr"],
              "rc=%d" % w["_rc"])
        # Gegenprobe: derselbe Aufrufer, in das Repo gelegt, geht durch.
        drin = os.path.join(wurzel, "strategies", "probe", "drin.py")
        with open(drin, "w", encoding="utf-8") as datei:
            datei.write(aufrufer)
        head2 = commit(wurzel, "Aufrufer im Baum")
        w = lauf(drin, attrappe=attrappe, commit_=head2)
        check("G3 derselbe Aufrufer im selben Baum -> rc 0",
              w["_rc"] == 0 and w.get("DATA_DIR") == attrappe, "rc=%d" % w["_rc"])

        # --- Mutation G: Bedingung 1 fehlt -----------------------------------
        mutiert, griff = mutiere(
            quelle(), "    if wurzel_code != wurzel_einstieg:",
            "    if False:", "G")
        if griff:
            wurzel_m, head_m = baue_repo(mutiert)
            aufrufer_m = aufrufer.replace(os.path.join(wurzel, "shared"),
                                          os.path.join(wurzel_m, "shared"))
            with open(os.path.join(fremd_repo, "lauf_m.py"), "w",
                      encoding="utf-8") as datei:
                datei.write(aufrufer_m)
            try:
                wm = lauf(os.path.join(fremd_repo, "lauf_m.py"),
                          attrappe=attrappe, commit_=head_m)
                check("G1 Mutationsprobe beisst",
                      wm["_rc"] == 0 and wm.get("DATA_DIR") == attrappe,
                      "ohne Bedingung 1 rechnet der gespaltene Baum still "
                      "weiter: rc %d" % wm["_rc"])
            finally:
                raeume(wurzel_m)
        else:
            check("G Mutationsprobe", False, "Mutation griff nicht")
    finally:
        raeume(wurzel, attrappe, fremd_repo, fremd_ohne)


# ===========================================================================
# Probe A - der schmutzige Arbeitsbaum (Nachweis 7)
# ===========================================================================

def probe_a_arbeitsbaum():
    print("\nProbe A - schmutziger Arbeitsbaum ueber shared/, strategies/, Lock")
    wurzel, head = baue_repo(quelle())
    attrappe = baue_attrappe()
    try:
        # (a) eine Datei unter shared/ veraendert
        pfad = os.path.join(wurzel, "shared", "paths.py")
        with open(pfad, "a", encoding="utf-8") as datei:
            datei.write("\n# angefasst\n")
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("A1 veraenderte Datei unter shared/ -> rc 2, Meldung nennt sie",
              w["_rc"] == RC_ERWARTET and verletzt(w)
              and "nicht sauber" in w["_stderr"]
              and "shared/paths.py" in w["_stderr"],
              "rc=%d" % w["_rc"])
        _git(wurzel, "checkout", "--", "shared/paths.py")
        # (b) eine neue, nicht eingecheckte Datei unter strategies/
        neu = os.path.join(wurzel, "strategies", "probe", "unfertig.py")
        with open(neu, "w") as datei:
            datei.write("# liegt herum\n")
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("A2 neue Datei unter strategies/ -> rc 2 (?? zaehlt)",
              w["_rc"] == RC_ERWARTET and verletzt(w)
              and "unfertig.py" in w["_stderr"], "rc=%d" % w["_rc"])
        os.remove(neu)
        # (c) die Lock-Datei veraendert, nicht eingecheckt
        with open(os.path.join(wurzel, "requirements.lock"), "a") as datei:
            datei.write("# nachtraeglich\n")
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("A3 veraenderte Lock-Datei -> rc 2",
              w["_rc"] == RC_ERWARTET and verletzt(w)
              and "requirements.lock" in w["_stderr"], "rc=%d" % w["_rc"])
        _git(wurzel, "checkout", "--", "requirements.lock")
        # (d) eine Datei AUSSERHALB der gepruefteten Pfade darf herumliegen
        with open(os.path.join(wurzel, "data", "XXX_1d.csv"), "w") as datei:
            datei.write("timestamp,close\n")
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("A4 neue Datei unter data/ stoert nicht (data/ ist nicht Code)",
              w["_rc"] == 0 and w.get("DATA_DIR") == attrappe, "rc=%d" % w["_rc"])
        # (e) wieder sauber -> rc 0, arbeitsbaum "sauber"
        os.remove(os.path.join(wurzel, "data", "XXX_1d.csv"))
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("A5 zurueckgesetzt -> rc 0, arbeitsbaum sauber",
              w["_rc"] == 0 and (w.get("startpruefung") or {}).get("arbeitsbaum")
              == "sauber", "rc=%d" % w["_rc"])

        # --- Mutation A: Bedingung 3 fehlt -----------------------------------
        mutiert, griff = mutiere(quelle(), "    if zeilen:", "    if False:", "A")
        if griff:
            wurzel_m, head_m = baue_repo(mutiert)
            try:
                with open(os.path.join(wurzel_m, "shared", "paths.py"), "a",
                          encoding="utf-8") as datei:
                    datei.write("\n# angefasst\n")
                wm = lauf_im_repo(wurzel_m, attrappe=attrappe, commit_=head_m)
                check("A1 Mutationsprobe beisst",
                      wm["_rc"] == 0 and wm.get("DATA_DIR") == attrappe,
                      "ohne Bedingung 3 rechnet der schmutzige Baum still "
                      "weiter: rc %d" % wm["_rc"])
            finally:
                raeume(wurzel_m)
        else:
            check("A Mutationsprobe", False, "Mutation griff nicht")
    finally:
        raeume(wurzel, attrappe)


# ===========================================================================
# Probe L - der Lock (Nachweis 8)
# ===========================================================================

def lock_text():
    with open(_ECHTER_LOCK, encoding="utf-8") as datei:
        return datei.read()


def probe_l_lock():
    print("\nProbe L - Lock: abweichendes Paket, fehlendes Paket, Interpreter, "
          "fehlende Datei")
    attrappe = baue_attrappe()
    text = lock_text()
    pandas_zeile = [z for z in text.splitlines() if z.startswith("pandas==")]
    if len(pandas_zeile) != 1:
        check("L NICHT PRUEFBAR", False, "keine eindeutige pandas-Zeile im Lock")
        raeume(attrappe)
        return
    try:
        # (a) ein Paket in anderer Fassung
        wurzel, head = baue_repo(quelle(), text.replace(pandas_zeile[0],
                                                        "pandas==0.0.1"))
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("L1 abweichendes Paket -> rc 2, Meldung nennt das Paket",
              w["_rc"] == RC_ERWARTET and verletzt(w)
              and "pandas: Lock 0.0.1" in w["_stderr"],
              "rc=%d" % w["_rc"])
        raeume(wurzel)
        # (b) ein Paket, das es nicht gibt
        wurzel, head = baue_repo(quelle(), text + "tb58-gibt-es-nicht==1.0\n")
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("L2 nicht installiertes Paket -> rc 2, 'NICHT' in der Meldung",
              w["_rc"] == RC_ERWARTET and verletzt(w)
              and "tb58-gibt-es-nicht: Lock 1.0, installiert NICHT"
              in w["_stderr"], "rc=%d" % w["_rc"])
        raeume(wurzel)
        # (c) vier abweichende Pakete -> genau drei genannt, Zahl stimmt
        vier = text
        for z in [z for z in text.splitlines()
                  if "==" in z and not z.startswith("#")][:4]:
            vier = vier.replace(z, z.split("==")[0] + "==0.0.0")
        wurzel, head = baue_repo(quelle(), vier)
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("L3 vier Abweichungen -> Zahl 4 und die ersten drei genannt",
              w["_rc"] == RC_ERWARTET and "(4 Abweichung/en" in w["_stderr"]
              and w["_stderr"].count("Lock 0.0.0") == 3, "rc=%d" % w["_rc"])
        raeume(wurzel)
        # (d) der Interpreter in der Kopfzeile passt nicht
        kopf_alt = [z for z in text.splitlines()
                    if z.startswith("# interpreter_voll")][0]
        wurzel, head = baue_repo(quelle(), text.replace(
            kopf_alt, "# interpreter_voll  2.7.18 (irgendwann)"))
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("L4 Interpreter weicht von der Kopfzeile ab -> rc 2",
              w["_rc"] == RC_ERWARTET and "Interpreter: Lock" in w["_stderr"],
              "rc=%d" % w["_rc"])
        raeume(wurzel)
        # (e) die Lock-Datei fehlt
        wurzel, head = baue_repo(quelle(), "")
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("L5 Lock-Datei fehlt -> rc 2 (nicht pruefbar ist nicht gruen)",
              w["_rc"] == RC_ERWARTET and "requirements.lock fehlt" in w["_stderr"],
              "rc=%d" % w["_rc"])
        raeume(wurzel)
        # (f) eine >=-Zeile ist kein Lock
        wurzel, head = baue_repo(quelle(), text.replace(pandas_zeile[0],
                                                        "pandas>=2.0"))
        w = lauf_im_repo(wurzel, attrappe=attrappe, commit_=head)
        check("L6 `>=`-Zeile -> rc 2 ('ist kein Lock')",
              w["_rc"] == RC_ERWARTET and "ist kein Lock" in w["_stderr"],
              "rc=%d" % w["_rc"])
        raeume(wurzel)
        wurzel = None

        # --- Mutation L: die Abweichungen werden nicht geworfen -------------
        mutiert, griff = mutiere(quelle(), "    if abweichungen:",
                                 "    if False:", "L")
        if griff:
            wurzel_m, head_m = baue_repo(mutiert, text.replace(pandas_zeile[0],
                                                               "pandas==0.0.1"))
            try:
                wm = lauf_im_repo(wurzel_m, attrappe=attrappe, commit_=head_m)
                check("L1 Mutationsprobe beisst",
                      wm["_rc"] == 0 and wm.get("DATA_DIR") == attrappe,
                      "ohne die Pruefung laeuft das abweichende Paket durch: "
                      "rc %d" % wm["_rc"])
            finally:
                raeume(wurzel_m)
        else:
            check("L Mutationsprobe", False, "Mutation griff nicht")
    finally:
        raeume(attrappe)


# ===========================================================================
# Probe R - der Rueckgabewert steht genau einmal, und er ist 2
# ===========================================================================

def probe_r_rueckgabewert():
    print("\nProbe R - Rueckgabewert 2, genau einmal im Modul")
    baum = ast.parse(quelle())
    werte = [k.value.value for k in baum.body if isinstance(k, ast.Assign)
             and any(isinstance(z, ast.Name)
                     and z.id == "RUECKGABEWERT_STARTPRUEFUNG"
                     for z in k.targets)
             and isinstance(k.value, ast.Constant)]
    check("R1 RUECKGABEWERT_STARTPRUEFUNG == 2, genau einmal zugewiesen",
          werte == [RC_ERWARTET], str(werte))
    # kein `SystemExit(<Zahl>)` mit Literal - der Wert kommt aus der Konstante
    literale = [k for k in ast.walk(baum) if isinstance(k, ast.Call)
                and isinstance(k.func, ast.Name) and k.func.id == "SystemExit"
                and k.args and isinstance(k.args[0], ast.Constant)]
    check("R2 kein SystemExit mit Zahl-Literal - der Wert kommt aus der "
          "Konstante", not literale, "%d Literal(e)" % len(literale))
    mutiert, griff = mutiere(quelle(), "raise SystemExit(RUECKGABEWERT_STARTPRUEFUNG)",
                             "raise SystemExit(1)", "R")
    if griff:
        lit_m = [k for k in ast.walk(ast.parse(mutiert)) if isinstance(k, ast.Call)
                 and isinstance(k.func, ast.Name) and k.func.id == "SystemExit"
                 and k.args and isinstance(k.args[0], ast.Constant)]
        check("R2 Mutationsprobe beisst", len(lit_m) == 1, "%d Literal" % len(lit_m))
    else:
        check("R Mutationsprobe", False, "Mutation griff nicht")


def main():
    print("=" * 78)
    print("Selbsttests zu shared/paths.py - die Startpruefungen (TB-58)")
    print("=" * 78)
    for name in ("TB_SELEKTIONSWURZEL", "TB_SELEKTIONSHASH", "TB_SELEKTIONSCOMMIT"):
        if os.environ.pop(name, None) is not None:
            print("  ⚠️ %s war in der Umgebung gesetzt - fuer diese Proben "
                  "entfernt." % name)
    if not os.path.exists(_ECHTER_LOCK):
        print("  [NICHT PRUEFBAR] %s fehlt - die Modus-Proben brauchen die "
              "echte Lock-Datei." % _ECHTER_LOCK)
        return 2
    for name, probe in (("N", probe_n_ohne_modus_nichts),
                        ("S", probe_s_vollstaendig),
                        ("C", probe_c_commit),
                        ("G", probe_g_gespaltener_baum),
                        ("A", probe_a_arbeitsbaum),
                        ("L", probe_l_lock),
                        ("R", probe_r_rueckgabewert)):
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
