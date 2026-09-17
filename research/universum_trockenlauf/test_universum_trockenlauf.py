#!/usr/bin/env python3
"""
Selbsttest des Universum-Trockenlaufs (TB-40)
==============================================================================
Geprueft wird, was die Aufgabenstellung ausdruecklich verlangt:

  A  Der ausloesende Befund wird reproduziert: `rsi2_crypto` laedt heute
     20 von 24 Symbolen, und es sind namentlich dieselben vier, die auf dem
     Mac fehlten.
  B  **Der Datenstand-Hash ist vor und nach dem Lauf identisch** - am
     Verhalten geprueft, nicht am Vorsatz.
  C  **Der Trockenlauf ist wiederholbar** - zweiter Lauf, gleiche Listen,
     Symbol fuer Symbol.
  D  **Ein kuenstlich verkuerztes Symbol faellt heraus**, und ein Symbol
     **genau an der Grenze** wird eindeutig behandelt - gegen erzeugte
     Beispieldaten, am Ablauf, an zwei Bots mit VERSCHIEDENER Schranke
     (Tagesspanne und Kerzenzahl).
  E  **Der Vergleich meldet eine Abweichung**, wenn eine eingetragene Zahl
     veraendert wird - sonst prueft er nichts.
  F-H  Mutationsproben.
  I  Monotonie: Lesart H am Faltenende ist gleichbedeutend mit "an mindestens
     einem Handelstag der Falte" - oder der Lauf meldet es.
  J  **TB-43 Fehler 3:** verglichen wird gegen die GUELTIGE Tabelle 16.1.1,
     nicht gegen die historische 15.5 - in BEIDE Richtungen geprueft, und das
     Werkzeug sagt, gegen welche es vergleicht.
  K  **TB-43 Fehler 1:** der Schreibschutz kennt jeden Aufrufweg. `open(pfad,
     mode="rb")` liest wieder, und ein Schreibversuch wird auf JEDEM Weg
     abgefangen - `builtins.open` positional wie benannt, `io.open`,
     `pathlib.Path.open`, `Path.write_text`, `os.open`.
  M  **TB-44 Mutationsproben:** die zwei Wachen aus L werden EINZELN
     entfernt. Jede muss fuer sich fehlen duerfen, ohne dass die andere es
     verdeckt - sonst belegt L nur, dass irgendeine von beiden da ist.
  L  **TB-44:** derselbe Schreibschutz haelt auf JEDER Python-Fassung und in
     BEIDER Import-Reihenfolge. `pathlib` bindet sich beim Import eine eigene
     Kopie der Oeffnungsfunktion; je nachdem, ob das vor oder nach der Wache
     passiert, war der Schutz vorher entweder loechrig oder er brach sogar
     LESENDE Zugriffe ab. **Teil K sieht das nicht** - dort ist `pathlib`
     schon geladen, bevor die Wache angeht. L faehrt beide Reihenfolgen ab,
     unter jeder Python-Fassung, die auf dem Rechner liegt.

ZU DEN MUTATIONSPROBEN - DIE ZWEI WIEDERKEHRENDEN FALLEN
------------------------------------------------------------------------------
1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst.** Deshalb wird hier keine Variable im laufenden Prozess umgebogen.
   Jede Probe kopiert das Werkzeug in ein Wegwerf-Verzeichnis, aendert dort
   **eine** Zeile und startet es als **eigenen Prozess** auf denselben Daten.
   Beobachtet wird der **Ablauf**: kommt etwas anderes heraus? Und jede Probe
   zeigt zuerst, dass sie ohne Mutation das Richtige sieht - sonst belegte ein
   rotes Ergebnis nichts.
2. **Eine zweite Wache verdeckt das Fehlen der ersten.** Der Trockenlauf hat
   zwei Wachen gegen dieselbe Gefahr - den Schreibschutz im Kindprozess und
   den Datenstand-Hash. Sie werden deshalb **einzeln** geprueft:

   * **F** macht den Stichtag wirkungslos. Faellt er aus, misst jede Falte
     stillschweigend den **heutigen** Stand - und sieht dabei sogar besser
     aus, weil jede Falte dann mehr Symbole hat. Keine andere Wache schlaegt
     dabei an: der Datenstand bleibt gleich, geschrieben wird nichts, die
     Monotonie gilt trivial.
   * **G** laesst den Trockenlauf schreiben, **mit** Schreibschutz. Der
     Schreibschutz allein muss den Lauf abbrechen - ohne dass ein
     Datenstand-Hash gefragt wird.
   * **H** laesst ihn dasselbe tun, **ohne** Schreibschutz. Jetzt laeuft er
     ohne Klage durch, und der Datenstand-Hash allein muss es finden. Damit
     ist gezeigt, dass jede der beiden Wachen fuer sich greift.

    python3 research/universum_trockenlauf/test_universum_trockenlauf.py

Rueckgabewert 0, wenn alle Pruefungen bestehen, sonst 1.
"""

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, _HIER)
sys.path.insert(0, os.path.join(BASE_DIR, "research", "vorregistrierung"))

import herkunft                                                  # noqa: E402
import universum_trockenlauf as ut                               # noqa: E402

WERKZEUG = os.path.join(_HIER, "universum_trockenlauf.py")
LOADERLAUF = os.path.join(_HIER, "loaderlauf.py")
LOADER_DIR = _HIER
# Irgendeine Datei, die es sicher gibt und die nur GELESEN wird. Teil K prueft
# an ihr, dass beide Aufrufformen von open() dasselbe liefern.
LESEQUELLE = LOADERLAUF

bestanden = 0
gescheitert = []

# Einmal gerechnet, von mehreren Teilen benutzt - der Faltenplan ist der
# Vergleichsgegenstand und aendert sich waehrend des Tests nicht.
_FALTENPLAN = [None]


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print("    ok   %s" % name)
    else:
        gescheitert.append(("%s %s" % (name, zusatz)).strip())
        print(("    FEHL %s %s" % (name, zusatz)).rstrip())


def _lauf(argv, umgebung=None):
    return subprocess.run([sys.executable] + argv, capture_output=True,
                          text=True, env=umgebung or os.environ.copy())


def _faltenplan():
    if _FALTENPLAN[0] is None:
        ordner = tempfile.mkdtemp(prefix="tb40_test_fp_")
        ziel = os.path.join(ordner, "fp.json")
        r = _lauf([os.path.join(BASE_DIR, "research", "faltenplan_neun",
                                "faltenplan_neun.py"), "--json", ziel])
        if not os.path.exists(ziel):
            raise RuntimeError("faltenplan_neun.py lief nicht:\n%s" % r.stdout[-2000:])
        _FALTENPLAN[0] = ziel
    return _FALTENPLAN[0]


def _trockenlauf_json(bots, register=None, werkzeug=WERKZEUG, umgebung=None,
                      extra=None):
    """Das Werkzeug als eigener Prozess; sein JSON-Bericht zurueck."""
    ordner = tempfile.mkdtemp(prefix="tb40_test_")
    ziel = os.path.join(ordner, "bericht.json")
    argv = [werkzeug, "--nur-universum", "--json", ziel,
            "--faltenplan-json", _faltenplan()]
    for b in bots:
        argv += ["--bot", b]
    if register:
        argv += ["--register", register]
    argv += list(extra or [])
    r = _lauf(argv, umgebung)
    if not os.path.exists(ziel):
        return None, r
    with open(ziel, encoding="utf-8") as f:
        return json.load(f), r


def _ersetze(pfad, alt, neu):
    with open(pfad, encoding="utf-8") as f:
        s = f.read()
    if alt not in s:
        raise AssertionError("Mutationsstelle nicht gefunden in %s: %r" % (pfad, alt))
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(s.replace(alt, neu, 1))


def _werkzeugkopie(ziel):
    shutil.copytree(_HIER, ziel, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    return ziel


def _umgebung_der_kopie():
    """Die Repo-Wurzel wandert mit. Sonst suchte die Kopie ihre Kursdateien und
    das Register neben dem Wegwerf-Ordner, und die Probe scheiterte am
    fehlenden Pfad statt an der Mutation - eine Probe, die aus dem falschen
    Grund scheitert, belegt nichts."""
    u = os.environ.copy()
    u["TB40_BASE_DIR"] = BASE_DIR
    return u


# ===========================================================================
# Wegwerf-Kursdaten
# ===========================================================================
def _schreibe_reihe(pfad, anzahl, schritt, ende=dt.datetime(2026, 9, 1)):
    """Eine Kursdatei mit genau `anzahl` vollstaendigen Kerzen im Abstand
    `schritt`, endend am 1. September 2026."""
    with open(pfad, "w", encoding="utf-8") as f:
        f.write("open_time,open,high,low,close,volume\n")
        for i in range(anzahl):
            zeit = ende - schritt * (anzahl - 1 - i)
            f.write("%s,100,101,99,100,1\n" % zeit.strftime("%Y-%m-%d %H:%M:%S"))


def _loaderlauf_json(bot, datenordner=None, werkzeug=LOADERLAUF, extra=None,
                     umgebung=None):
    ordner = tempfile.mkdtemp(prefix="tb40_test_ll_")
    ziel = os.path.join(ordner, "l.json")
    argv = [werkzeug, "--bot", bot, "--aus", ziel]
    if datenordner:
        argv += ["--daten", datenordner]
    argv += extra or []
    r = _lauf(argv, umgebung)
    if not os.path.exists(ziel):
        return None, r
    with open(ziel, encoding="utf-8") as f:
        return json.load(f), r


# ===========================================================================
# A  Der ausloesende Befund
# ===========================================================================
def teil_a():
    stand = herkunft.datenstand()
    pruefe("A0: der Datenstand ist der registrierte (223 Dateien, d9449faf...)",
           stand["dateien"] == 223 and stand["datenstand"].startswith("d9449faf"),
           "%s / %d" % (stand["datenstand"][:12], stand["dateien"]))

    bericht, r = _trockenlauf_json(["rsi2_crypto"])
    pruefe("A1: das Werkzeug laeuft", bericht is not None,
           (r.stdout + r.stderr)[-500:])
    if bericht is None:
        return
    e = bericht["bots"]["rsi2_crypto"]
    pruefe("A2: der Loader laedt heute 20 von 24 Symbolen - der Befund vom Mac",
           len(e["heute_geladen"]) == 20 and e["universum"] == 24,
           "%d von %d" % (len(e["heute_geladen"]), e["universum"]))
    fehlen = sorted({"ENSOUSDT", "PUMPUSDT", "ZKCUSDT", "UUSDT"}
                    - set(e["heute_geladen"]))
    pruefe("A3: und es sind namentlich dieselben vier",
           fehlen == ["ENSOUSDT", "PUMPUSDT", "UUSDT", "ZKCUSDT"], str(fehlen))
    pruefe("A4: die eingetragene Zahl fuer die Bestaetigungsperiode ist 20 - "
           "der Wert aus der GUELTIGEN Tabelle 16.1.1 (die historische in "
           "15.5 sagt 23)",
           [f for f in e["falten"] if f["bestaetigung"]][0]["register"] == 20,
           str([f for f in e["falten"] if f["bestaetigung"]][0]["register"]))


# ===========================================================================
# B  Der Datenstand-Hash - am Verhalten
# ===========================================================================
def _baum(ordner):
    """Alle Pfade unterhalb eines Ordners - oder None, wenn es ihn nicht gibt."""
    if not os.path.exists(ordner):
        return None
    return sorted(os.path.join(w, n) for w, _d, ns in os.walk(ordner) for n in ns) \
        + sorted(os.path.join(w, d) for w, ds, _n in os.walk(ordner) for d in ds)


def teil_b():
    vorher = herkunft.datenstand()
    logs_vorher = _baum(os.path.join(BASE_DIR, "logs"))
    ergebnisse_vorher = _baum(os.path.join(BASE_DIR, "results"))
    bericht, r = _trockenlauf_json(["rsi2_crypto", "elliott_wave_stocks"])
    nachher = herkunft.datenstand()
    pruefe("B0: der Lauf kommt durch", bericht is not None,
           (r.stdout + r.stderr)[-500:])
    pruefe("B1: der Datenstand-Hash ist vor und nach dem Lauf identisch",
           vorher == nachher, "%s -> %s" % (vorher["datenstand"][:12],
                                            nachher["datenstand"][:12]))
    # Dass der Schreibschutz waehrend des Laufs WIRKLICH aktiv war, zeigt
    # sich daran, dass er etwas zu tun hatte: shared/strategy_paths.py will
    # beim Import results/<bot> und logs/<bot> anlegen, und genau diese
    # Versuche stehen im Bericht. Ohne diesen Nachweis koennte B1 auch dann
    # gruen sein, wenn gar keine Wache liefe.
    pruefe("B2: der Schreibschutz war waehrend des Laufs nachweislich aktiv",
           bericht is not None
           and any("makedirs_unterdrueckt" in e for e in bericht["bots"].values()),
           str(list(bericht["bots"].values())[0].keys()) if bericht else "")
    # results/<bot> und logs/<bot> legt shared/strategy_paths.py beim Import an.
    # Der Schreibschutz macht das folgenlos; hier wird nachgesehen, dass es
    # wirklich folgenlos blieb.
    # Nicht "logs/ existiert nicht" - das waere eine Aussage ueber das ganze
    # Repo, und andere Tests legen den Ordner an. Geprueft wird, was dieser
    # Lauf hinterlassen hat: nichts.
    pruefe("B3: der Lauf hat unter logs/ nichts angelegt",
           _baum(os.path.join(BASE_DIR, "logs")) == logs_vorher,
           str(set(_baum(os.path.join(BASE_DIR, "logs")) or [])
               - set(logs_vorher or []))[:200])
    pruefe("B4: und unter results/ ebenfalls nichts",
           _baum(os.path.join(BASE_DIR, "results")) == ergebnisse_vorher,
           str(set(_baum(os.path.join(BASE_DIR, "results")) or [])
               - set(ergebnisse_vorher or []))[:200])


# ===========================================================================
# C  Wiederholbarkeit
# ===========================================================================
def teil_c():
    erst, _ = _trockenlauf_json(["turtle_soup_crypto"])
    zweit, _ = _trockenlauf_json(["turtle_soup_crypto"])
    pruefe("C0: beide Laeufe kommen durch", erst is not None and zweit is not None)
    if erst is None or zweit is None:
        return
    a = erst["bots"]["turtle_soup_crypto"]["falten"]
    b = zweit["bots"]["turtle_soup_crypto"]["falten"]
    gleich = all(x["gemessen_H"] == y["gemessen_H"]
                 and x["gemessen_F"] == y["gemessen_F"] for x, y in zip(a, b))
    pruefe("C1: zweiter Lauf, gleiche Listen - Symbol fuer Symbol, nicht nur "
           "gleiche Anzahl", gleich)
    pruefe("C2: und es sind ueberhaupt Symbole drin (sonst waere C1 leer wahr)",
           sum(len(x["gemessen_H"]) for x in a) > 0)


# ===========================================================================
# D  Die Grenze - gegen erzeugte Beispieldaten, am Ablauf
# ===========================================================================
def teil_d():
    # --- D1-D4: Spannen-Schranke (500 Tage, turtle_soup_crypto) -------------
    # 501 Tageskerzen ergeben eine Spanne von 500 Tagen - genau die Schranke.
    with tempfile.TemporaryDirectory() as tmp:
        tag = dt.timedelta(days=1)
        _schreibe_reihe(os.path.join(tmp, "BTCUSDT_1d.csv"), 900, tag)
        _schreibe_reihe(os.path.join(tmp, "ETHUSDT_1d.csv"), 501, tag)
        _schreibe_reihe(os.path.join(tmp, "XRPUSDT_1d.csv"), 500, tag)
        lauf, r = _loaderlauf_json("turtle_soup_crypto", tmp)
        pruefe("D0: der Loader laeuft auf den Beispieldaten",
               lauf is not None and not lauf["fehler"],
               (lauf or {}).get("fehler") or (r.stdout + r.stderr)[-400:])
        if lauf is None or lauf["fehler"]:
            return
        geladen = set(lauf["laeufe"][0]["symbole"])
        pruefe("D1: das lange Symbol wird geladen", "BTCUSDT" in geladen)
        pruefe("D2: das kuenstlich verkuerzte Symbol faellt heraus "
               "(499 Tage < 500)", "XRPUSDT" not in geladen)
        pruefe("D3: genau an der Grenze (exakt 500 Tage) wird GELADEN - die "
               "Schranke ist einschliesslich",
               "ETHUSDT" in geladen, str(sorted(geladen)))
        pruefe("D4: die Schranke, gegen die geprueft wurde, ist die des Bots "
               "(500), nicht eine Zahl im Werkzeug",
               lauf["schranken"].get("MIN_HISTORY_DAYS") == 500,
               str(lauf["schranken"].get("MIN_HISTORY_DAYS")))

    # --- D5-D7: Kerzenzahl-Schranke (17520 Kerzen, elliott_wave) -----------
    # Derselbe Test an einem Bot, dessen Schranke eine ANDERE Groesse misst.
    # Waere sie ueberall dieselbe, koennte das Werkzeug sie abschreiben.
    with tempfile.TemporaryDirectory() as tmp:
        stunde = dt.timedelta(hours=1)
        _schreibe_reihe(os.path.join(tmp, "BTCUSDT_1h.csv"), 17520, stunde)
        _schreibe_reihe(os.path.join(tmp, "ETHUSDT_1h.csv"), 17519, stunde)
        # Gleiche Zeitspanne wie BTCUSDT, aber nur jede zehnte Kerze: eine
        # Spannen-Schranke wuerde das durchlassen, eine Kerzenzahl-Schranke
        # nicht. Das trennt die beiden Arten am Verhalten.
        _schreibe_reihe(os.path.join(tmp, "XRPUSDT_1h.csv"), 1752,
                        stunde * 10)
        lauf, r = _loaderlauf_json("elliott_wave", tmp)
        pruefe("D5: der Loader von elliott_wave laeuft auf den Beispieldaten",
               lauf is not None and not lauf["fehler"],
               (lauf or {}).get("fehler") or (r.stdout + r.stderr)[-400:])
        if lauf is None or lauf["fehler"]:
            return
        geladen = set(lauf["laeufe"][0]["symbole"])
        pruefe("D6: genau an der Grenze (exakt 17520 Kerzen) wird geladen, "
               "eine Kerze weniger nicht",
               "BTCUSDT" in geladen and "ETHUSDT" not in geladen,
               str(sorted(geladen)))
        pruefe("D7: dieselbe Zeitspanne mit zu wenig Kerzen faellt heraus - "
               "dieser Bot misst Kerzen, nicht Tage",
               "XRPUSDT" not in geladen)
        pruefe("D8: und seine Schranke heisst auch anders",
               "MIN_HISTORY_HOURS" in lauf["schranken"]
               and "MIN_HISTORY_DAYS" not in lauf["schranken"],
               str(sorted(lauf["schranken"])))


# ===========================================================================
# E  Der Vergleich meldet eine Abweichung
# ===========================================================================
def _registerkopie(ziel, alt, neu):
    shutil.copy2(ut.REGISTER, ziel)
    _ersetze(ziel, alt, neu)
    return ziel


def teil_e():
    original, _ = _trockenlauf_json(["rsi2_crypto"])
    pruefe("E0: unmutiert liest das Werkzeug die eingetragene Reihe "
           "6 / 9 / 10 / 13 / 13 / 17 / 18 - aus der gueltigen Tabelle 16.1.1",
           original is not None
           and original["bots"]["rsi2_crypto"]["register"]["falten"]
           == [6, 9, 10, 13, 13, 17, 18],
           str((original or {}).get("bots", {}).get("rsi2_crypto", {}).get("register")))
    if original is None:
        return
    vorher = original["bots"]["rsi2_crypto"]["falten"][0]["differenz_H"]

    with tempfile.TemporaryDirectory() as tmp:
        pfad = _registerkopie(
            os.path.join(tmp, "REG.md"),
            "> | `rsi2_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |",
            "> | `rsi2_crypto` | 5 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |")
        mutiert, r = _trockenlauf_json(["rsi2_crypto"], register=pfad)
        pruefe("E1: das Werkzeug laeuft auf dem veraenderten Register",
               mutiert is not None, (r.stdout + r.stderr)[-400:])
        if mutiert is None:
            return
        nachher = mutiert["bots"]["rsi2_crypto"]["falten"][0]["differenz_H"]
        pruefe("E2: eine veraenderte eingetragene Zahl aendert die gemeldete "
               "Differenz - der Vergleich prueft wirklich gegen das Register",
               nachher == vorher + 1, "%s -> %s" % (vorher, nachher))
        pruefe("E3: die GEMESSENE Liste bleibt dabei gleich - es hat sich nur "
               "die eingetragene Zahl bewegt, nicht die Messung",
               mutiert["bots"]["rsi2_crypto"]["falten"][0]["gemessen_H"]
               == original["bots"]["rsi2_crypto"]["falten"][0]["gemessen_H"])


# ===========================================================================
# F  Mutationsprobe: der Stichtag wird wirkungslos
# ===========================================================================
def teil_f():
    original, _ = _trockenlauf_json(["rsi2_crypto"])
    pruefe("F0: unmutiert misst die erste Falte WENIGER als heute",
           original is not None
           and len(original["bots"]["rsi2_crypto"]["falten"][0]["gemessen_H"])
           < len(original["bots"]["rsi2_crypto"]["heute_geladen"]))
    if original is None:
        return

    with tempfile.TemporaryDirectory() as tmp:
        ordner = _werkzeugkopie(os.path.join(tmp, "werkzeug"))
        _ersetze(os.path.join(ordner, "loaderlauf.py"),
                 '            df = df[df["open_time"] <= stichtag]',
                 '            pass  # Mutationsprobe: Stichtag wirkungslos')
        mutiert, r = _trockenlauf_json(
            ["rsi2_crypto"],
            werkzeug=os.path.join(ordner, "universum_trockenlauf.py"),
            umgebung=_umgebung_der_kopie())
        pruefe("F1: das mutierte Werkzeug laeuft (sonst belegte F2 nichts)",
               mutiert is not None, (r.stdout + r.stderr)[-400:])
        if mutiert is None:
            return
        m = mutiert["bots"]["rsi2_crypto"]
        pruefe("F2: ohne wirksamen Stichtag misst JEDE Falte den heutigen "
               "Stand - und das faellt auf",
               all(f["gemessen_H"] == m["heute_geladen"] for f in m["falten"]),
               str([len(f["gemessen_H"]) for f in m["falten"]]))
        pruefe("F3: die Mutation macht die Zahlen GROESSER, nicht kleiner - "
               "sie sieht also besser aus als das Richtige",
               sum(len(f["gemessen_H"]) for f in m["falten"])
               > sum(len(f["gemessen_H"])
                     for f in original["bots"]["rsi2_crypto"]["falten"]))
        pruefe("F4: keine andere Wache schlaegt dabei an - die Monotonie gilt "
               "trivial weiter, also braucht es genau diese Probe",
               mutiert["monotonie_verletzt"] == [])


# ===========================================================================
# G/H  Mutationsproben: die beiden Wachen gegen das Schreiben, einzeln
# ===========================================================================
_SCHREIB_ANKER = "    return modul\n"
_SCHREIB_MUTATION = (
    '    with open(os.path.join(modul.DATA_DIR, "_mutationsprobe.csv"), "w") as _f:\n'
    '        _f.write("open_time,open,high,low,close,volume\\n")\n'
    "    return modul\n")


def _wegwerf_repo(ordner):
    """Ein Wegwerf-Repo: alles verlinkt, nur `data/` ist eine echte Kopie mit
    drei Kursdateien.

    Warum nicht einfach `--daten`: Teil H schaltet den Schreibschutz ab. Alles,
    was der Loader dann anlegen will - `shared/strategy_paths.py` will beim
    Import `results/<bot>` und `logs/<bot>` - soll im Wegwerf-Ordner landen und
    nicht im Repo. Die Probe darf das Repo auch dann nicht anfassen, wenn sie
    gelingt."""
    os.makedirs(ordner)
    for name in ("config", "shared", "docs", "research", "strategies"):
        os.symlink(os.path.join(BASE_DIR, name), os.path.join(ordner, name))
    daten = os.path.join(ordner, "data")
    os.makedirs(daten)
    for symbol in ("BTCUSDT", "ETHUSDT", "XRPUSDT"):
        shutil.copy2(os.path.join(BASE_DIR, "data", "%s_1d.csv" % symbol), daten)
    return daten


def teil_g():
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "repo")
        daten = _wegwerf_repo(repo)
        umgebung = os.environ.copy()
        umgebung["TB40_BASE_DIR"] = repo
        vorher = herkunft.datenstand(daten)

        sauber, _ = _loaderlauf_json("turtle_soup_crypto", umgebung=umgebung)
        pruefe("G0: unmutiert laeuft der Kindprozess ohne Fehler",
               sauber is not None and not sauber["fehler"],
               (sauber or {}).get("fehler"))

        ordner = _werkzeugkopie(os.path.join(tmp, "werkzeug"))
        _ersetze(os.path.join(ordner, "loaderlauf.py"),
                 _SCHREIB_ANKER, _SCHREIB_MUTATION)
        lauf, r = _loaderlauf_json(
            "turtle_soup_crypto",
            werkzeug=os.path.join(ordner, "loaderlauf.py"),
            umgebung=umgebung)
        pruefe("G1: der Schreibschutz ALLEIN bricht den Lauf ab - ohne dass "
               "ein Datenstand-Hash gefragt wurde",
               lauf is not None and lauf["fehler"]
               and "SCHREIBVERSUCH" in lauf["fehler"],
               str((lauf or {}).get("fehler"))[:200] or (r.stdout + r.stderr)[-300:])
        pruefe("G2: und die Datei ist gar nicht erst entstanden",
               not os.path.exists(os.path.join(daten, "_mutationsprobe.csv")))
        pruefe("G3: der Datenstand des Wegwerf-Ordners steht unveraendert",
               herkunft.datenstand(daten) == vorher)


def teil_h():
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "repo")
        daten = _wegwerf_repo(repo)
        umgebung = os.environ.copy()
        umgebung["TB40_BASE_DIR"] = repo
        vorher = herkunft.datenstand(daten)

        ordner = _werkzeugkopie(os.path.join(tmp, "werkzeug"))
        _ersetze(os.path.join(ordner, "loaderlauf.py"),
                 _SCHREIB_ANKER, _SCHREIB_MUTATION)
        lauf, r = _loaderlauf_json(
            "turtle_soup_crypto",
            werkzeug=os.path.join(ordner, "loaderlauf.py"),
            extra=["--ohne-schreibschutz"],
            umgebung=umgebung)
        pruefe("H1: ohne Schreibschutz laeuft derselbe Defekt OHNE Klage durch "
               "- die erste Wache fehlt wirklich",
               lauf is not None and not lauf["fehler"],
               str((lauf or {}).get("fehler"))[:200] or (r.stdout + r.stderr)[-300:])
        pruefe("H2: die Datei ist jetzt da",
               os.path.exists(os.path.join(daten, "_mutationsprobe.csv")))
        nachher = herkunft.datenstand(daten)
        pruefe("H3: der Datenstand-Hash ALLEIN findet es - die zweite Wache "
               "greift fuer sich",
               nachher != vorher, "%s -> %s" % (vorher["datenstand"][:12],
                                                nachher["datenstand"][:12]))
        pruefe("H4: und zwar an der Dateizahl wie am Inhalt",
               nachher["dateien"] == vorher["dateien"] + 1)


# ===========================================================================
# I  Monotonie
# ===========================================================================
def teil_i():
    bericht, r = _trockenlauf_json(["rsi2_crypto", "elliott_wave",
                                    "volatility_breakout"])
    pruefe("I0: der Lauf kommt durch", bericht is not None,
           (r.stdout + r.stderr)[-400:])
    if bericht is None:
        return
    pruefe("I1: ueber alle Stichtage waechst die Menge der handelbaren "
           "Symbole nur - Lesart H am Faltenende ist damit gleichbedeutend "
           "mit 'an mindestens einem Handelstag der Falte'",
           bericht["monotonie_verletzt"] == [],
           str(bericht["monotonie_verletzt"])[:300])
    e = bericht["bots"]["rsi2_crypto"]
    pruefe("I2: und die Pruefung ist nicht leer - F ist echt strenger als H",
           any(len(f["gemessen_F"]) < len(f["gemessen_H"]) for f in e["falten"]))



# ===========================================================================
# J  TB-43 Fehler 3: gegen WELCHE Tabelle wird verglichen?
# ===========================================================================
def teil_j():
    """Seit dem Registernachtrag TB-41 gibt es ZWEI Tabellen mit derselben
    Kopfzeile. Geprueft wird in BEIDE Richtungen - sonst belegt ein "kein
    Befund" nur, dass das Werkzeug schweigt, nicht dass es die Tabelle
    wechselt."""
    gueltig = ut.lies_register(abschnitt=ut.TABELLE_GUELTIG)
    historisch = ut.lies_register(abschnitt=ut.TABELLE_HISTORISCH)

    pruefe("J0: der Standard ist die GUELTIGE Tabelle 16.1.1",
           ut.TABELLE_GUELTIG == "16.1.1"
           and ut.lies_register() == gueltig, ut.TABELLE_GUELTIG)
    pruefe("J1: beide Tabellen werden ueberhaupt gefunden - je neun Bots",
           len(gueltig) == 9 and len(historisch) == 9,
           "%d / %d" % (len(gueltig), len(historisch)))

    abweichend = [b for b in gueltig
                  if (gueltig[b]["falten"], gueltig[b]["bestaetigung"])
                  != (historisch[b]["falten"], historisch[b]["bestaetigung"])]
    pruefe("J2: die beiden Tabellen sind wirklich verschieden - und zwar in "
           "acht der neun Reihen", len(abweichend) == 8, str(sorted(abweichend)))
    pruefe("J3: genau elliott_wave stimmt in beiden ueberein - der neunte Bot",
           "elliott_wave" not in abweichend)

    # Die Gegenprobe zur wichtigsten Falle: liest es WIRKLICH 16.1.1, oder
    # schweigt es nur? Die Zahl, an der sich die beiden Tabellen fuer
    # t3_supertrend unterscheiden, ist namentlich bekannt.
    pruefe("J4: aus 16.1.1 kommt t3_supertrend = 3 / 6 / 9 / 13 / 13 / 13 / 17",
           gueltig["t3_supertrend"]["falten"] == [3, 6, 9, 13, 13, 13, 17],
           str(gueltig["t3_supertrend"]["falten"]))
    pruefe("J5: aus 15.5 kommt dieselbe Zeile als 6 / 9 / 13 / 13 / 13 / 17 / 18",
           historisch["t3_supertrend"]["falten"] == [6, 9, 13, 13, 13, 17, 18],
           str(historisch["t3_supertrend"]["falten"]))

    # Und das Werkzeug SAGT, gegen welche es vergleicht - im Bericht wie in
    # der Ausgabe.
    for abschnitt in (ut.TABELLE_GUELTIG, ut.TABELLE_HISTORISCH):
        bericht, r = _trockenlauf_json(["rsi2_crypto"],
                                       extra=["--register-abschnitt", abschnitt])
        pruefe("J6-%s: der Lauf gegen %s kommt durch" % (abschnitt, abschnitt),
               bericht is not None, (r.stdout + r.stderr)[-300:])
        if bericht is None:
            continue
        pruefe("J7-%s: der Bericht nennt den benutzten Abschnitt" % abschnitt,
               bericht.get("register_abschnitt") == abschnitt,
               str(bericht.get("register_abschnitt")))
        pruefe("J8-%s: und die Ausgabe nennt ihn auch" % abschnitt,
               ("Abschnitt %s" % abschnitt) in r.stdout,
               r.stdout[:200])
        erwartet = (gueltig if abschnitt == ut.TABELLE_GUELTIG
                    else historisch)["rsi2_crypto"]["falten"]
        pruefe("J9-%s: und die eingetragene Reihe stammt aus dieser Tabelle"
               % abschnitt,
               bericht["bots"]["rsi2_crypto"]["register"]["falten"] == erwartet,
               str(bericht["bots"]["rsi2_crypto"]["register"]["falten"]))

    # Gegen 15.5 muss das Werkzeug ausserdem WARNEN - sonst liest jemand die
    # acht Abweichungen als Registerfehler und "korrigiert" sie ein zweites Mal.
    _, r155 = _trockenlauf_json(["rsi2_crypto"],
                                extra=["--register-abschnitt",
                                       ut.TABELLE_HISTORISCH])
    pruefe("J10: gegen die historische Tabelle warnt das Werkzeug ausdruecklich",
           "ACHTUNG" in r155.stdout and "NICHT die gueltige" in r155.stdout,
           r155.stdout[:400])


# ===========================================================================
# K  TB-43 Fehler 1: der Schreibschutz kennt JEDEN Aufrufweg
# ===========================================================================
def teil_k():
    """`open(pfad, mode="rb")` brach den Trockenlauf mit einem TypeError ab -
    der Schreibschutz scheiterte an einem LESEversuch. Beim Reparieren des
    Durchgriffs darf der Schutz nicht loechrig werden; deshalb wird beides
    geprueft, und zwar am ABLAUF in einem eigenen Prozess.

    Der Aufrufweg wird DIREKT geprueft, nicht ueber `python-binance`: in der
    Cloud kommt dessen Import ohnehin nicht durch, und neuere
    `dateparser`-Fassungen nehmen den Weg gar nicht mehr. Ein Test, der den
    Fehler nur auf einem Rechner finden kann, findet ihn meistens nicht.
    """
    programm = r"""
import io, json, os, pathlib, sys

ordner, loader_dir, lesequelle = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, loader_dir)
import loaderlauf

erlaubt = os.path.join(ordner, "erlaubt")
os.makedirs(erlaubt, exist_ok=True)
loaderlauf.schreibschutz_an([erlaubt])

ziel = os.path.join(ordner, "verboten.txt")
erg = {}

def probe(name, f):
    try:
        f()
        erg[name] = "durchgelassen"
    except loaderlauf.Schreibversuch:
        erg[name] = "abgefangen"
    except Exception as e:
        erg[name] = type(e).__name__ + ": " + str(e)

# 1. LESEN muss in beiden Aufrufformen gehen - und dasselbe liefern.
a = b = None
try:
    a = open(lesequelle, "rb").read()
    erg["lesen_positional"] = "ok"
except Exception as e:
    erg["lesen_positional"] = type(e).__name__ + ": " + str(e)
try:
    b = open(lesequelle, mode="rb").read()
    erg["lesen_benannt"] = "ok"
except Exception as e:
    erg["lesen_benannt"] = type(e).__name__ + ": " + str(e)
erg["lesen_gleich"] = bool(a is not None and a == b)

# 2. SCHREIBEN muss auf JEDEM Weg abgefangen werden.
probe("schreiben_positional", lambda: open(ziel + "1", "w"))
probe("schreiben_benannt", lambda: open(ziel + "2", mode="w"))
probe("schreiben_vollbenannt", lambda: open(file=ziel + "3", mode="w"))
probe("io_open", lambda: io.open(ziel + "4", "w"))
probe("pathlib_open", lambda: pathlib.Path(ziel + "5").open("w"))
probe("pathlib_write_text", lambda: pathlib.Path(ziel + "6").write_text("x"))
probe("os_open", lambda: os.close(os.open(ziel + "7", os.O_WRONLY | os.O_CREAT)))

# 3. Erlaubtes Schreiben geht weiter.
probe("erlaubt", lambda: open(os.path.join(erlaubt, "ok.txt"), "w").close())

erg["angelegt"] = sorted(n for n in os.listdir(ordner)
                         if n.startswith("verboten"))
print(json.dumps(erg))
"""

    with tempfile.TemporaryDirectory() as tmp:
        skript = os.path.join(tmp, "probe.py")
        with open(skript, "w", encoding="utf-8") as f:
            f.write(programm)
        r = subprocess.run([sys.executable, skript, tmp, LOADER_DIR, LESEQUELLE],
                           capture_output=True, text=True)
        pruefe("K0: die Probe laeuft ueberhaupt durch",
               r.returncode == 0, (r.stdout + r.stderr)[-500:])
        if r.returncode != 0:
            return
        erg = json.loads(r.stdout.strip().splitlines()[-1])

    # --- der eigentliche TB-43-Fehler ---
    pruefe("K1: open(pfad, \"rb\") - positional - liest",
           erg["lesen_positional"] == "ok", str(erg["lesen_positional"]))
    pruefe("K2: open(pfad, mode=\"rb\") - benannt - liest AUCH "
           "(vorher: TypeError)",
           erg["lesen_benannt"] == "ok", str(erg["lesen_benannt"]))
    pruefe("K3: und beide liefern dasselbe Ergebnis", erg["lesen_gleich"] is True,
           str(erg["lesen_gleich"]))

    # --- und der Schutz ist dabei nicht loechrig geworden ---
    for name, text in (("schreiben_positional", "open(pfad, \"w\")"),
                       ("schreiben_benannt", "open(pfad, mode=\"w\")"),
                       ("schreiben_vollbenannt", "open(file=…, mode=\"w\")"),
                       ("io_open", "io.open(pfad, \"w\")"),
                       ("pathlib_open", "pathlib.Path(pfad).open(\"w\")"),
                       ("pathlib_write_text", "Path(pfad).write_text(…)"),
                       ("os_open", "os.open(pfad, O_WRONLY|O_CREAT)")):
        pruefe("K4 %-22s wird abgefangen" % text,
               erg[name] == "abgefangen", str(erg[name]))

    pruefe("K5: erlaubtes Schreiben geht weiter - der Schutz ist nicht bloss "
           "ein Totalverbot", erg["erlaubt"] == "durchgelassen",
           str(erg["erlaubt"]))
    pruefe("K6: und es ist wirklich keine verbotene Datei entstanden - am "
           "Dateibestand geprueft, nicht an der Ausnahme",
           erg["angelegt"] == [], str(erg["angelegt"]))


# ===========================================================================
# L  TB-44: die Wache haelt auf JEDER Python-Fassung und in BEIDER
#    Import-Reihenfolge
# ===========================================================================
# Laeuft als eigener Prozess - einmal je Python-Fassung auf dem Rechner, und
# je Fassung einmal fuer jede Reihenfolge.
_L_PROGRAMM = r'''
import io, json, os, sys

loader_dir, ordner, reihenfolge, lesequelle = sys.argv[1:5]
sys.path.insert(0, loader_dir)
import loaderlauf

# --- Reihenfolge herstellen, ausdruecklich und nachpruefbar ----------------
if reihenfolge == "frueh":
    import pathlib
else:
    for _m in [n for n in list(sys.modules)
               if n == "pathlib" or n.startswith("pathlib.")]:
        del sys.modules[_m]
    assert "pathlib" not in sys.modules, "pathlib liess sich nicht entladen"

# --- Nachstellung, Haelfte 1: gebunden VOR der Wache ----------------------
# Das sind woertlich die Zeilen, die CPython in den Rumpf von
# `pathlib._NormalAccessor` schreibt - 3.9 nimmt `os.open`, 3.10 `io.open`.
# Hier stehen beide, damit die Probe auf jeder Fassung dieselbe ist.
class AccessorVorher:
    oeffnen_os = os.open
    oeffnen_io = io.open
    entfernen = os.unlink

# Ein Opfer zum Loeschen - angelegt, SOLANGE es noch erlaubt ist. Auf keinen
# Fall eine Datei des Repos: faellt die Wache aus, ist sie danach weg.
opfer = os.path.join(ordner, "opfer.txt")
with open(opfer, "w") as _f:
    _f.write("x")

erlaubt = os.path.join(ordner, "erlaubt")
os.makedirs(erlaubt, exist_ok=True)
loaderlauf.schreibschutz_an([erlaubt])

# --- Nachstellung, Haelfte 2: gebunden NACH der Wache ---------------------
class AccessorNachher:
    oeffnen_os = os.open
    oeffnen_io = io.open
    entfernen = os.unlink

if reihenfolge == "spaet":
    import pathlib                      # <-- ERST JETZT

erg = {"py": "%d.%d.%d" % sys.version_info[:3], "reihenfolge": reihenfolge,
       "pathlib_hat_accessor": hasattr(pathlib, "_NormalAccessor"),
       "nachgezogen": sorted(set(getattr(loaderlauf,
                                         "_BINDUNGEN_NACHGEZOGEN", [])))}

def probe(name, f):
    try:
        f()
        erg[name] = "durchgelassen"
    except loaderlauf.Schreibversuch:
        erg[name] = "abgefangen"
    except Exception as e:
        erg[name] = type(e).__name__ + ": " + str(e)[:140]

def zu(fd):
    os.close(fd)

ziel = os.path.join(ordner, "verbotenL")

for marke, zugriff in (("vor", AccessorVorher()), ("nach", AccessorNachher())):
    probe(marke + "_lesen_os",
          lambda a=zugriff: zu(a.oeffnen_os(lesequelle, os.O_RDONLY)))
    probe(marke + "_lesen_io",
          lambda a=zugriff: a.oeffnen_io(lesequelle, "rb").close())
    probe(marke + "_schreiben_os",
          lambda a=zugriff, m=marke: zu(a.oeffnen_os(ziel + m + "1",
                                                     os.O_WRONLY | os.O_CREAT)))
    probe(marke + "_schreiben_io",
          lambda a=zugriff, m=marke: a.oeffnen_io(ziel + m + "2", "w").close())
    probe(marke + "_loeschen", lambda a=zugriff: a.entfernen(opfer))

# --- und dasselbe am ECHTEN pathlib ---------------------------------------
probe("pathlib_lesen_read_text", lambda: pathlib.Path(lesequelle).read_text())
probe("pathlib_lesen_open", lambda: pathlib.Path(lesequelle).open("r").close())
probe("pathlib_schreiben_write_text",
      lambda: pathlib.Path(ziel + "p1").write_text("x"))
probe("pathlib_schreiben_open",
      lambda: pathlib.Path(ziel + "p2").open("w").close())
probe("pathlib_schreiben_touch", lambda: pathlib.Path(ziel + "p3").touch())
probe("pathlib_schreiben_mkdir", lambda: pathlib.Path(ziel + "p4").mkdir())
probe("pathlib_loeschen", lambda: pathlib.Path(opfer).unlink())

# --- Zeichengeraete bleiben ausgenommen -----------------------------------
# `python-binance` und `yfinance` oeffnen /dev/null beim Import
# lesend-schreibend. Bricht die Wache daran ab, faellt der echte Trockenlauf
# aus - und zwar erst im Kindprozess, also schwer zu sehen.
probe("devnull_builtins", lambda: open(os.devnull, "r+").close())
probe("devnull_io", lambda: io.open(os.devnull, "w").close())
probe("devnull_os", lambda: zu(os.open(os.devnull, os.O_RDWR)))
probe("devnull_pathlib", lambda: pathlib.Path(os.devnull).open("r+").close())

# --- erlaubtes Schreiben geht weiter --------------------------------------
probe("erlaubt", lambda: open(os.path.join(erlaubt, "ok.txt"), "w").close())
probe("erlaubt_pathlib",
      lambda: pathlib.Path(erlaubt, "ok2.txt").write_text("x"))

erg["angelegt"] = sorted(n for n in os.listdir(ordner)
                         if n.startswith("verbotenL"))
erg["opfer_lebt"] = os.path.exists(opfer)
print(json.dumps(erg))
'''


def _fassung(python):
    """Die Fassungsnummer eines Interpreters - gefragt, nicht aus dem Namen
    geraten. `python3.9` kann alles Moegliche sein."""
    try:
        r = subprocess.run([python, "-c",
                            "import sys;print('%d %d' % sys.version_info[:2])"],
                           capture_output=True, text=True, timeout=60)
        return tuple(int(x) for x in r.stdout.split())
    except Exception:                                            # noqa: BLE001
        return None


def _pythons():
    """Jede Python-Fassung, die auf diesem Rechner erreichbar ist.

    Der Befund von TB-44 ist auf 3.11 und neuer **strukturell unsichtbar**:
    dort gibt es `pathlib._NormalAccessor` nicht mehr. Ein Test, der nur unter
    `sys.executable` laeuft, sieht ihn auf einem 3.11-Rechner also nie - und
    genau das ist in TB-43 passiert. Deshalb wird jede gefundene Fassung
    abgefahren, und der Bericht nennt sie.
    """
    gesehen, gefunden = set(), []
    for pfad in [sys.executable] + [shutil.which("python3.%d" % m)
                                    for m in range(8, 15)]:
        if not pfad:
            continue
        echt = os.path.realpath(pfad)
        if echt in gesehen:
            continue
        gesehen.add(echt)
        gefunden.append(pfad)
    return gefunden


def _l_lauf(python, reihenfolge, loader_dir=None):
    tmp = tempfile.mkdtemp(prefix="tb44_l_")
    try:
        skript = os.path.join(tmp, "probe_l.py")
        with open(skript, "w", encoding="utf-8") as f:
            f.write(_L_PROGRAMM)
        try:
            # Mit Frist: `_pythons()` nimmt, was auf dem Rechner liegt, und
            # darunter kann eine kaputte oder haengende Fassung sein. Ohne
            # Frist haengt dann der ganze Selbsttest - auf einem fremden
            # Rechner, an einer Stelle, die niemand vermutet.
            r = subprocess.run([python, skript, loader_dir or LOADER_DIR, tmp,
                                reihenfolge, LESEQUELLE],
                               capture_output=True, text=True, timeout=600)
        except subprocess.TimeoutExpired:
            return None, "Zeitueberschreitung nach 600 s: %s" % python
        uebrig = sorted(n for n in os.listdir(tmp) if n.startswith("verbotenL"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if r.returncode != 0 or not r.stdout.strip():
        return None, (r.stdout + r.stderr)[-600:]
    erg = json.loads(r.stdout.strip().splitlines()[-1])
    erg["uebrig_nach_abbau"] = uebrig
    return erg, ""


def teil_l():
    """Der Schreibschutz haengt nicht mehr an der Python-Fassung.

    Der Befund, auf dem unveraenderten TB-43-Stand gemessen:

      | Fassung | pathlib VOR der Wache        | pathlib NACH der Wache      |
      |---------|------------------------------|-----------------------------|
      | 3.9     | `Path.touch`/`mkdir`         | JEDER Zugriff bricht ab,    |
      |         | schrieben **wirklich**       | auch ein LESENDER           |
      | 3.10    | `Path.open("w")`/`write_text`| JEDER Zugriff bricht ab     |
      |         | schrieben **wirklich**       |                             |
      | 3.11+   | in Ordnung                   | in Ordnung                  |

    Beides ist derselbe Fehler: `pathlib` legt sich beim Import eine **eigene
    Kopie** der Oeffnungsfunktion in den Rumpf einer Klasse. Liegt die Kopie
    vor der Wache, kennt sie den Schutz nicht; liegt sie danach, wird aus der
    Python-Funktion eine gebundene Methode, und die Argumente verrutschen.

    Geprueft wird dreifach - und getrennt, damit nicht eine Wache das Fehlen
    der anderen verdeckt:

    * **L1 gebunden NACH der Wache.** Eine Klasse mit `open = os.open` bzw.
      `open = io.open` im Rumpf - woertlich die Zeile aus `pathlib`. Das
      prueft allein die nicht-bindende Huelle `_Wache`.
    * **L2 gebunden VOR der Wache.** Dieselbe Klasse, vor `schreibschutz_an`
      angelegt. Das prueft allein `_bindungen_nachziehen`.
      *L1 und L2 laufen auf JEDER Fassung und fallen auf dem alten Stand auf
      jeder Fassung durch - sie brauchen kein altes Python.*
    * **L3 am echten pathlib**, in beiden Reihenfolgen. Das ist der Nachweis,
      dass L1/L2 die richtige Stelle nachstellen. Auf 3.9/3.10 faellt L3 auf
      dem alten Stand durch; auf 3.11+ kann er es nicht - dort gibt es die
      Stelle nicht.

    Dazu L4 (Zeichengeraete und Erlaubtes bleiben offen), L5 (am
    Dateibestand: es ist wirklich nichts entstanden und nichts verschwunden)
    und L6 (es lief wirklich eine Fassung mit, die die Stelle noch hat).
    """
    pythons = _pythons()
    fassungen = [(p, _fassung(p)) for p in pythons]
    alte = [p for p, v in fassungen if v is not None and v < (3, 11)]
    print("      Python-Fassungen: %s"
          % ", ".join("%s=%s" % (os.path.basename(p),
                                 ".".join(map(str, v)) if v else "?")
                      for p, v in fassungen))
    for python in pythons:
        for reihenfolge in ("frueh", "spaet"):
            erg, fehler = _l_lauf(python, reihenfolge)
            pruefe("L0 %-22s die Probe laeuft durch"
                   % ("%s/%s" % (os.path.basename(python), reihenfolge)),
                   erg is not None, fehler)
            if erg is None:
                continue
            m = "%s %s" % (erg["py"], reihenfolge)

            # --- L1: Kopie NACH der Wache - die nicht-bindende Huelle ------
            pruefe("L1 %-16s Kopie NACH der Wache: os.open LIEST" % m,
                   erg["nach_lesen_os"] == "durchgelassen",
                   str(erg["nach_lesen_os"]))
            pruefe("L1 %-16s Kopie NACH der Wache: io.open LIEST" % m,
                   erg["nach_lesen_io"] == "durchgelassen",
                   str(erg["nach_lesen_io"]))
            pruefe("L1 %-16s und os.open SCHREIBT trotzdem nicht" % m,
                   erg["nach_schreiben_os"] == "abgefangen",
                   str(erg["nach_schreiben_os"]))
            pruefe("L1 %-16s und io.open SCHREIBT trotzdem nicht" % m,
                   erg["nach_schreiben_io"] == "abgefangen",
                   str(erg["nach_schreiben_io"]))
            pruefe("L1 %-16s und os.unlink loescht nicht" % m,
                   erg["nach_loeschen"] == "abgefangen",
                   str(erg["nach_loeschen"]))

            # --- L2: Kopie VOR der Wache - das Nachziehen ------------------
            pruefe("L2 %-16s Kopie VOR der Wache: LESEN geht durch" % m,
                   erg["vor_lesen_os"] == "durchgelassen"
                   and erg["vor_lesen_io"] == "durchgelassen",
                   "%s / %s" % (erg["vor_lesen_os"], erg["vor_lesen_io"]))
            pruefe("L2 %-16s und os.open SCHREIBT nicht - nachgezogen" % m,
                   erg["vor_schreiben_os"] == "abgefangen",
                   str(erg["vor_schreiben_os"]))
            pruefe("L2 %-16s und io.open SCHREIBT nicht - nachgezogen" % m,
                   erg["vor_schreiben_io"] == "abgefangen",
                   str(erg["vor_schreiben_io"]))
            pruefe("L2 %-16s und os.unlink loescht nicht" % m,
                   erg["vor_loeschen"] == "abgefangen",
                   str(erg["vor_loeschen"]))
            # Wie B2: dass die Wache etwas zu TUN hatte, ist beobachtbar.
            pruefe("L2 %-16s das Nachziehen ist nachweislich passiert" % m,
                   any(e.endswith("AccessorVorher.oeffnen_os")
                       for e in erg["nachgezogen"]),
                   str(erg["nachgezogen"])[:160])

            # --- L3: am ECHTEN pathlib, beide Reihenfolgen -----------------
            pruefe("L3 %-16s pathlib: read_text() liest" % m,
                   erg["pathlib_lesen_read_text"] == "durchgelassen",
                   str(erg["pathlib_lesen_read_text"]))
            pruefe("L3 %-16s pathlib: Path().open(\"r\") liest" % m,
                   erg["pathlib_lesen_open"] == "durchgelassen",
                   str(erg["pathlib_lesen_open"]))
            for schluessel, text in (("pathlib_schreiben_write_text",
                                      "write_text()"),
                                     ("pathlib_schreiben_open", "open(\"w\")"),
                                     ("pathlib_schreiben_touch", "touch()"),
                                     ("pathlib_loeschen", "unlink()")):
                pruefe("L3 %-16s pathlib: %-12s abgefangen" % (m, text),
                       erg[schluessel] == "abgefangen", str(erg[schluessel]))
            # `mkdir` bricht absichtlich NICHT ab, sondern bleibt folgenlos -
            # sonst kaeme `shared/strategy_paths.py` beim Import nicht durch.
            # Geprueft wird deshalb am Dateibestand (L5), nicht an der Ausnahme.
            pruefe("L3 %-16s pathlib: mkdir() bleibt folgenlos" % m,
                   erg["pathlib_schreiben_mkdir"] == "durchgelassen",
                   str(erg["pathlib_schreiben_mkdir"]))

            # --- L4: Zeichengeraete und Erlaubtes bleiben offen ------------
            for schluessel, text in (("devnull_builtins", "open(devnull,r+)"),
                                     ("devnull_io", "io.open(devnull,w)"),
                                     ("devnull_os", "os.open(devnull,RDWR)"),
                                     ("devnull_pathlib", "Path(devnull).open")):
                pruefe("L4 %-16s %-22s ausgenommen" % (m, text),
                       erg[schluessel] == "durchgelassen", str(erg[schluessel]))
            pruefe("L4 %-16s erlaubtes Schreiben geht weiter" % m,
                   erg["erlaubt"] == "durchgelassen"
                   and erg["erlaubt_pathlib"] == "durchgelassen",
                   "%s / %s" % (erg["erlaubt"], erg["erlaubt_pathlib"]))

            # --- L5: am Dateibestand, nicht an der Ausnahme ----------------
            pruefe("L5 %-16s keine verbotene Datei entstanden" % m,
                   erg["angelegt"] == [] and erg["uebrig_nach_abbau"] == [],
                   "%s / %s" % (erg["angelegt"], erg["uebrig_nach_abbau"]))
            pruefe("L5 %-16s und keine Datei verschwunden" % m,
                   erg["opfer_lebt"] is True, str(erg["opfer_lebt"]))

    pruefe("L6: es lief eine Fassung mit, die `pathlib._NormalAccessor` noch "
           "hat (3.9/3.10) - sonst sagt L3 auf diesem Rechner nichts ueber "
           "den Befund",
           bool(alte),
           "gefunden: %s" % ", ".join("%s" % os.path.basename(p)
                                      for p in pythons))


# ===========================================================================
# M  TB-44 Mutationsproben: die zwei Wachen werden EINZELN geprueft
# ===========================================================================
# Gegen den Schaden aus TB-44 stehen zwei Wachen, und sie decken
# verschiedene Faelle:
#
#   * `_huelle`/`_Wache`  - fuer Kopien, die NACH `schreibschutz_an` entstehen
#   * `_bindungen_nachziehen` - fuer Kopien, die VORHER schon dastanden
#
# Zusammen sind sie dicht. Genau deshalb koennte eine von beiden fehlen, ohne
# dass Teil L rot wird - **die zweite verdeckt das Fehlen der ersten**. Diese
# Falle ist in diesem Projekt schon zweimal zugeschlagen. Deshalb wird jede
# Wache einzeln entfernt, an einer Kopie, in einem eigenen Prozess, und
# beobachtet wird der ABLAUF: welcher Zugriff geht jetzt durch, der vorher
# nicht durchging - und welcher NICHT, weil die andere Wache noch steht.
_M1_ALT = "    return _Wache(funktion, name)"
_M1_NEU = "    return funktion"
_M2_ALT = "    for modulname, modul in list(sys.modules.items()):"
_M2_NEU = "    for modulname, modul in []:"


def _m_kopie(tmp, alt, neu):
    """Eine Kopie des Werkzeugs mit GENAU EINER geaenderten Zeile."""
    ziel = _werkzeugkopie(os.path.join(tmp, "kopie"))
    _ersetze(os.path.join(ziel, "loaderlauf.py"), alt, neu)
    return ziel


def teil_m():
    """Jede der beiden TB-44-Wachen fuer sich.

    M0 ist die Gegenprobe: **ohne** Mutation sieht die Probe das Richtige.
    Ohne sie belegte ein rotes Ergebnis nichts - es koennte auch am
    Wegwerf-Ordner liegen.
    """
    erg0, fehler = _l_lauf(sys.executable, "spaet")
    pruefe("M0: die Probe laeuft unmutiert durch", erg0 is not None, fehler)
    if erg0 is None:
        return
    pruefe("M0a: unmutiert liest eine NACH der Wache gebundene Kopie - und "
           "schreibt nicht",
           erg0["nach_lesen_os"] == "durchgelassen"
           and erg0["nach_schreiben_os"] == "abgefangen",
           "%s / %s" % (erg0["nach_lesen_os"], erg0["nach_schreiben_os"]))
    pruefe("M0b: unmutiert schreibt eine VOR der Wache gebundene Kopie "
           "ebenfalls nicht",
           erg0["vor_schreiben_os"] == "abgefangen",
           str(erg0["vor_schreiben_os"]))

    # --- M1: die nicht-bindende Huelle faellt weg -------------------------
    with tempfile.TemporaryDirectory() as tmp:
        kopie = _m_kopie(tmp, _M1_ALT, _M1_NEU)
        erg1, fehler = _l_lauf(sys.executable, "spaet", kopie)
    pruefe("M1: die Probe laeuft auch mit der Mutation durch",
           erg1 is not None, fehler)
    if erg1 is not None:
        pruefe("M1a: ohne die Huelle bricht eine NACH der Wache gebundene "
               "Kopie ab - auch beim LESEN. Das ist der TB-44-Befund",
               erg1["nach_lesen_os"] != "durchgelassen",
               str(erg1["nach_lesen_os"]))
        # GEMESSEN, nicht angenommen: das Nachziehen allein haelt zwar den
        # Schreibversuch auf (es wird nichts angelegt), arbeitet aber
        # ebenfalls falsch - es setzt ja dieselbe nackte Python-Funktion in
        # die Klasse. Die beiden Wachen sind also NICHT unabhaengig: das
        # Nachziehen SETZT die Huelle VORAUS. Das steht hier als Pruefung,
        # damit es nicht in Vergessenheit geraet.
        pruefe("M1b: ohne die Huelle schreibt die VOR der Wache gebundene "
               "Kopie zwar immer noch nicht - das Nachziehen greift -, ...",
               erg1["vor_schreiben_os"] != "durchgelassen"
               and erg1["uebrig_nach_abbau"] == [],
               "%s / %s" % (erg1["vor_schreiben_os"],
                            erg1["uebrig_nach_abbau"]))
        pruefe("M1c: ... aber sie bricht jetzt AUCH beim Lesen ab. Die zwei "
               "Wachen sind nicht unabhaengig: das Nachziehen setzt die "
               "Huelle voraus, die Huelle nicht das Nachziehen (M2b)",
               erg1["vor_lesen_os"] != "durchgelassen",
               str(erg1["vor_lesen_os"]))

    # --- M2: das Nachziehen faellt weg ------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        kopie = _m_kopie(tmp, _M2_ALT, _M2_NEU)
        erg2, fehler = _l_lauf(sys.executable, "spaet", kopie)
    pruefe("M2: die Probe laeuft auch mit der Mutation durch",
           erg2 is not None, fehler)
    if erg2 is not None:
        pruefe("M2a: ohne das Nachziehen SCHREIBT eine VOR der Wache "
               "gebundene Kopie wieder - das Loch ist wieder offen",
               erg2["vor_schreiben_os"] == "durchgelassen",
               str(erg2["vor_schreiben_os"]))
        pruefe("M2b: und die ANDERE Wache steht dabei noch - eine NACH der "
               "Wache gebundene Kopie liest und schreibt weiterhin richtig",
               erg2["nach_lesen_os"] == "durchgelassen"
               and erg2["nach_schreiben_os"] == "abgefangen",
               "%s / %s" % (erg2["nach_lesen_os"], erg2["nach_schreiben_os"]))
        pruefe("M2c: und es ist dabei wirklich eine verbotene Datei "
               "entstanden - am Dateibestand, nicht an der Ausnahme",
               erg2["uebrig_nach_abbau"] != [],
               str(erg2["uebrig_nach_abbau"]))


# ===========================================================================
def main():
    print(__doc__.strip().split("\n")[0])
    print("=" * 78)
    for name, teil in (("A", teil_a), ("B", teil_b), ("C", teil_c),
                       ("D", teil_d), ("E", teil_e), ("F", teil_f),
                       ("G", teil_g), ("H", teil_h), ("I", teil_i),
                       ("J", teil_j), ("K", teil_k), ("L", teil_l),
                          ("M", teil_m)):
        print("  Teil %s ..." % name, flush=True)
        try:
            teil()
        except Exception as e:                                   # noqa: BLE001
            # Ein Teil, der abstuerzt, ist ein Fehlschlag - aber er darf die
            # uebrigen nicht verschlucken. Sonst belegt ein Lauf auf einem
            # unveraenderten Stand nur den ERSTEN fehlenden Befund.
            pruefe("Teil %s stuerzt ab: %s: %s" % (name, type(e).__name__, e),
                   False)
    print("\n" + "=" * 78)
    if gescheitert:
        print("%d bestanden, %d GESCHEITERT:" % (bestanden, len(gescheitert)))
        for g in gescheitert:
            print("  - %s" % g)
        return 1
    print("%d/%d Pruefungen bestanden." % (bestanden, bestanden))
    return 0


if __name__ == "__main__":
    sys.exit(main())
