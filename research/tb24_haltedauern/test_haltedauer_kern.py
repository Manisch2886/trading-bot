"""
Selbsttests des Rechenkerns - mit Gegenproben UND Mutationsproben
==============================================================================
Nach Prinzip 12 des Uebergabeprotokolls ("eine gruene Pruefung ist erst dann
etwas wert, wenn belegt ist, dass sie auch rot werden kann") steht hier
zweierlei:

* **Gegenproben** - zu jeder Behauptung ein zweiter Fall, in dem dieselbe
  Pruefung anschlagen MUSS: zur getrennten Verteilung die ueberlappende, zum
  Treffer am Fensterrand der Nicht-Treffer einen Tag daneben, zur Ueberlappung
  im selben Titel die Ueberlappung ohne gemeinsamen Titel.
* **Mutationsproben** - der Quelltext des Rechenkerns wird gezielt an EINER
  Stelle verfaelscht, das veraenderte Modul frisch geladen und dieselbe
  Pruefungsreihe darauf laufen gelassen. Sie MUSS dann fehlschlagen. Damit ist
  belegt, dass die Pruefungen die jeweilige Rechenregel wirklich festhalten
  und nicht bloss daneben herlaufen. Jede Textersetzung wird vorher darauf
  geprueft, dass sie genau einmal zutrifft - eine Mutation, die nichts
  veraendert, wuerde sonst als bestandene Probe durchgehen.

Alle Erwartungswerte sind von Hand nachrechenbar konstruiert; keiner ist aus
einem Lauf des Kerns uebernommen und wiedererkannt.

    python3 test_haltedauer_kern.py
"""

import os
import subprocess
import sys
import types

import numpy as np
import pandas as pd

import haltedauer_kern

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
KERN_PFAD = os.path.join(_DIR, "haltedauer_kern.py")

FEHLER = []
LEISE = False
GEZAEHLT = [0]


def pruefe(bedingung, text):
    GEZAEHLT[0] += 1
    if bedingung:
        if not LEISE:
            print(f"  ok    {text}")
    else:
        if not LEISE:
            print(f"  FEHLT {text}")
        FEHLER.append(text)


def pos(zeilen):
    """zeilen: (symbol, entry, exit, result). pnl_pct/kerzen werden nicht
    gebraucht und deshalb nicht erfunden."""
    df = pd.DataFrame(zeilen, columns=["symbol", "entry_time", "exit_time", "result"])
    df["entry_time"] = pd.to_datetime(df["entry_time"])
    df["exit_time"] = pd.to_datetime(df["exit_time"])
    return df


def tag(n, basis="2020-01-01"):
    return str((pd.Timestamp(basis) + pd.Timedelta(days=n)).date())


# ===========================================================================
# Die Pruefungsreihe. Sie bekommt das zu pruefende Modul uebergeben, damit
# dieselbe Reihe auch auf ein mutiertes Modul angewandt werden kann.
# ===========================================================================

def pruefungsreihe(k):

    # -- 1. Haltedauer in Kalendertagen -----------------------------------
    p = pos([("A", "2020-01-01", "2020-01-04", "time_exit")])
    pruefe(float(k.haltedauer_tage(p).iloc[0]) == 3.0,
           "1.1 Einstieg 01., Ausstieg 04. -> 3 Kalendertage")

    p_stunden = pos([("A", "2020-01-01 07:00", "2020-01-03 11:00", "time_exit")])
    pruefe(abs(float(k.haltedauer_tage(p_stunden).iloc[0]) - (2 + 4 / 24)) < 1e-9,
           "1.2 Stundenkerzen: 2 Tage 4 Stunden -> 2,1667 Tage (nicht 2, nicht 3)")

    p_null = pos([("A", "2020-01-01", "2020-01-01", "stop_loss")])
    pruefe(float(k.haltedauer_tage(p_null).iloc[0]) == 0.0,
           "1.3 Gegenprobe: Ein- und Ausstieg am selben Tag -> 0 Tage")

    # -- 2. Verteilungs-Kennzahlen ---------------------------------------
    kz = k.kennzahlen(list(range(1, 11)))
    pruefe(kz["n"] == 10 and kz["median"] == 5.5 and kz["mittel"] == 5.5,
           "2.1 n=10, Median 5,5, Mittel 5,5 bei 1..10")
    pruefe(kz["q1"] == 3.25 and kz["q3"] == 7.75,
           "2.2 Quartile 3,25 / 7,75 (lineare Interpolation)")
    pruefe(abs(kz["p10"] - 1.9) < 1e-9 and abs(kz["p90"] - 9.1) < 1e-9,
           "2.3 10./90. Perzentil 1,9 / 9,1")

    schief = k.kennzahlen([1, 1, 1, 1, 1, 1, 1, 1, 1, 100])
    pruefe(schief["median"] == 1.0 and schief["mittel"] == 10.9,
           "2.4 Gegenprobe: ein Ausreisser zieht den Mittelwert (10,9), nicht den Median (1,0)")
    pruefe(k.kennzahlen([])["n"] == 0, "2.5 leere Reihe -> n = 0, kein Absturz")

    # -- 3. Histogramm: links geschlossen, rechts offen -------------------
    h = k.histogramm([0.0, 2.9, 3.0, 9.99, 10.0, 100.0], [0, 3, 10])
    pruefe(list(h) == [2, 2, 2],
           "3.1 Klassen [0,3) [3,10) [10,inf) zaehlen 2 / 2 / 2")
    h_rand = k.histogramm([3.0], [0, 3, 10])
    pruefe(list(h_rand) == [0, 1, 0],
           "3.2 Gegenprobe Klassengrenze: 3,0 gehoert in [3,10), nicht in [0,3)")

    # -- 4. Zweigipfligkeit ueber die Ausstiegsart ------------------------
    getrennt = pos([("A", tag(i), tag(i + 1), "stop_loss") for i in range(10)]
                    + [("A", tag(i), tag(i + 10), "time_exit") for i in range(10)])
    z = k.zweigipfligkeit(getrennt)
    pruefe(z["zwei_gruppen"] is True,
           "4.1 Stop nach 1 Tag gegen Zeitausstieg nach 10 Tagen -> zwei Gruppen")

    vermischt = pos([("A", tag(i), tag(i + 1 + (i % 9)), "stop_loss") for i in range(10)]
                     + [("A", tag(i), tag(i + 1 + (i % 9)), "time_exit") for i in range(10)])
    z2 = k.zweigipfligkeit(vermischt)
    pruefe(z2["zwei_gruppen"] is False,
           "4.2 Gegenprobe: gleiche Streuung in beiden Arten -> KEINE zwei Gruppen")

    eine_art = pos([("A", tag(i), tag(i + 3), "time_exit") for i in range(10)])
    pruefe(k.zweigipfligkeit(eine_art)["zwei_gruppen"] is False,
           "4.3 nur eine Ausstiegsart -> keine zwei Gruppen (und kein Absturz)")

    # -- 5. Positionstage: Ein- und Ausstiegstag eingeschlossen -----------
    drei = pos([("X", "2020-01-01", "2020-01-03", "time_exit")])
    pruefe(len(k.positionstage(drei)) == 3,
           "5.1 Position vom 01. bis 03. belegt drei Kalendertage")
    pruefe(len(k.positionstage(p_null)) == 1,
           "5.2 Gegenprobe: Ein-Tages-Position belegt genau einen Tag")

    wochenende = pos([("X", "2020-01-03", "2020-01-06", "time_exit")])   # Fr bis Mo
    pruefe(len(k.positionstage(wochenende)) == 4,
           "5.3 Freitag bis Montag sind vier Kalendertage - das Wochenende zaehlt mit")

    zwei_titel = pos([("X", "2020-01-01", "2020-01-03", "time_exit"),
                       ("Y", "2020-01-01", "2020-01-03", "time_exit")])
    pruefe(len(k.positionstage(zwei_titel)) == 3
           and len(k.positionstage_je_titel(zwei_titel)) == 6,
           "5.4 zwei Titel an denselben drei Tagen: 3 Positionstage, 6 Titeltage")

    # -- 6. Gemeinsames Fenster ------------------------------------------
    frueh = pos([("X", "2020-01-01", "2020-01-05", "time_exit")])
    spaet = pos([("X", "2020-02-01", "2020-02-05", "time_exit")])
    pruefe(k.gemeinsames_fenster(frueh, spaet) == (None, None),
           "6.1 Gegenprobe: Zeitraeume ohne Ueberschneidung -> kein gemeinsames Fenster")
    von, bis = k.gemeinsames_fenster(frueh, pos([("X", "2020-01-03", "2020-01-09", "x")]))
    pruefe(str(von.date()) == "2020-01-03" and str(bis.date()) == "2020-01-05",
           "6.2 Fenster ist die Schnittmenge (03. bis 05.)")

    # -- 7. Ueberlappung: nicht symmetrisch, Titel getrennt von Tagen -----
    a = pos([("X", "2020-01-01", "2020-01-10", "time_exit")])
    b = pos([("X", "2020-01-01", "2020-01-02", "time_exit"),
              ("X", "2020-01-09", "2020-01-10", "time_exit")])
    u_ab = k.ueberlappung(a, b)
    u_ba = k.ueberlappung(b, a)
    pruefe(u_ab["tage_a"] == 10 and u_ab["anteil_tage"] == 0.4,
           "7.1 A haelt 10 Tage, an 4 davon haelt auch B -> 40 %")
    pruefe(u_ba["anteil_tage"] == 1.0,
           "7.2 Gegenprobe zur Richtung: umgekehrt sind es 100 % - die Zahl ist nicht symmetrisch")

    fremder_titel = pos([("Y", "2020-01-01", "2020-01-10", "time_exit")])
    u_fremd = k.ueberlappung(a, fremder_titel)
    pruefe(u_fremd["anteil_tage"] == 1.0 and u_fremd["anteil_titel"] == 0.0,
           "7.3 Gegenprobe Titel gegen Tage: dieselben Tage, anderer Titel -> 100 % / 0 %")

    # -- 8. Naehe der Einstiege ------------------------------------------
    # Eine lange Fuellposition je Bot haelt das gemeinsame Fenster offen,
    # damit die zu pruefenden Einstiege hineinfallen.
    a_naehe = pos([("X", tag(0), tag(31), "time_exit"),
                    ("X", tag(10), tag(11), "stop_loss")])
    b_treffer = pos([("X", tag(0), tag(31), "time_exit"),
                      ("X", tag(13), tag(14), "stop_loss")])
    b_daneben = pos([("X", tag(0), tag(31), "time_exit"),
                      ("X", tag(14), tag(15), "stop_loss")])

    n_treffer = k.naehe(a_naehe, b_treffer, zufallslaeufe=0)
    pruefe(n_treffer["einstiege_a"] == 2 and n_treffer["treffer"] == 2,
           "8.1 Abstand genau 3 Tage liegt NOCH im Fenster -> 2 von 2 Einstiegen")
    n_daneben = k.naehe(a_naehe, b_daneben, zufallslaeufe=0)
    pruefe(n_daneben["treffer"] == 1,
           "8.2 Gegenprobe Fensterrand: Abstand 4 Tage liegt NICHT mehr drin -> 1 von 2")

    kein_titel = pos([("Z", tag(0), tag(31), "time_exit"),
                       ("Z", tag(10), tag(11), "stop_loss")])
    pruefe(k.naehe(a_naehe, kein_titel, zufallslaeufe=0)["treffer"] == 0,
           "8.3 Gegenprobe: gleiche Tage, aber kein gemeinsamer Titel -> 0 Treffer")

    # -- 9. Versatz: Vorzeichen und Deckung mit der Naehe-Zahl ------------
    v = k.versatz_verteilung(a_naehe, b_treffer)
    pruefe(v["n"] == 2 and v["median_versatz"] == 1.5,
           "9.1 Versatz 0 und +3 Tage -> Median 1,5")
    pruefe(v["histogramm"]["0 bis < 3"] == 1 and v["histogramm"]["3 bis < 10"] == 1,
           "9.2 Vorzeichen: B steigt SPAETER ein -> positiver Versatz")
    pruefe(abs(v["anteil_bis_3_tage"] - n_treffer["anteil"]) < 1e-12,
           "9.3 Deckung: 'Anteil bis 3 Tage' aus der Versatzrechnung gleicht dem "
           "Anteil aus der Fenstersuche")

    v_um = k.versatz_verteilung(b_treffer, a_naehe)
    pruefe(v_um["median_versatz"] == -1.5,
           "9.4 Gegenprobe Vorzeichen: umgekehrte Richtung -> Median -1,5")

    # -- 10. Zufallsvergleich: Ziehung gegen geschlossene Form ------------
    # 50 A-Einstiege und 20 B-Einstiege auf 1000 Tagen. Der erwartete Anteil
    # haengt nur von den ANZAHLEN ab: 1 - (1 - 7/1000)**20 = 0,1314.
    lang_a = pos([("X", tag(0), tag(999), "time_exit")]
                  + [("X", tag(i), tag(i + 1), "stop_loss") for i in range(0, 1000, 20)])
    lang_b = pos([("X", tag(0), tag(999), "time_exit")]
                  + [("X", tag(i + 7), tag(i + 8), "stop_loss") for i in range(0, 1000, 50)])
    erwartet = k.naehe_erwartet_analytisch(lang_a, lang_b)
    gezogen = k.naehe(lang_a, lang_b, zufallslaeufe=200)["anteil_zufall"]
    pruefe(abs(gezogen - erwartet) < 0.03,
           f"10.1 Ziehung ({gezogen:.3f}) und geschlossene Form ({erwartet:.3f}) "
           "liegen weniger als 3 Prozentpunkte auseinander")
    pruefe(gezogen <= erwartet + 1e-9,
           "10.2 die Ziehung liegt nicht ueber der geschlossenen Form - diese "
           "vernachlaessigt die Randeffekte und ist deshalb die obere Schranke")

    # -- 11. Horizont-Klassen --------------------------------------------
    pruefe(k.horizont_klasse(2.99) == "bis 2 Tage",
           "11.1 Median 2,99 Tage -> 'bis 2 Tage'")
    pruefe(k.horizont_klasse(3.0) == "3 bis 10 Tage" and k.horizont_klasse(10.0) == "3 bis 10 Tage",
           "11.2 Gegenprobe Klassengrenze: 3,0 und 10,0 liegen im Fenster der Vermutung")
    pruefe(k.horizont_klasse(10.5) == "11 bis 30 Tage" and k.horizont_klasse(21.0) == "11 bis 30 Tage",
           "11.3 10,5 und 21,0 liegen darueber")
    pruefe(k.horizont_klasse(200.0) == "ueber 90 Tage", "11.4 200 Tage -> 'ueber 90 Tage'")


# ===========================================================================
# Mutationsproben
# ===========================================================================

MUTATIONEN = [
    ("Haltedauer in Stunden statt Tagen",
     "return (aus - ein) / pd.Timedelta(days=1)",
     "return (aus - ein) / pd.Timedelta(hours=1)"),
    ("Ausstiegstag nicht mehr als Positionstag gezaehlt",
     'for tag in pd.date_range(a, b, freq="D"):',
     'for tag in pd.date_range(a, b, freq="D")[:-1]:'),
    ("Naehe-Fenster um einen Tag zu eng",
     'spanne = np.timedelta64(fenster_tage, "D")',
     'spanne = np.timedelta64(fenster_tage - 1, "D")'),
    ("Vorzeichen des Versatzes gedreht",
     "versatz.append(float(abstand[np.argmin(np.abs(abstand))]))",
     "versatz.append(float(-abstand[np.argmin(np.abs(abstand))]))"),
    ("Histogramm-Klassen rechts geschlossen statt links",
     "zaehler = [int(((s >= grenzen[i]) & (s < grenzen[i + 1])).sum())",
     "zaehler = [int(((s > grenzen[i]) & (s <= grenzen[i + 1])).sum())"),
    ("Zweigipfligkeit immer bejaht",
     'getrennt = bool(a["q3"] < b["q1"] or b["q3"] < a["q1"])',
     "getrennt = True"),
    ("Grenze der Horizont-Klasse verschoben",
     '("bis 2 Tage", 0.0, 3.0),',
     '("bis 2 Tage", 0.0, 4.0),'),
    ("Ueberlappung auf B statt auf A bezogen",
     '"anteil_tage": (len(tage_a & tage_b) / len(tage_a)) if tage_a else None,',
     '"anteil_tage": (len(tage_a & tage_b) / len(tage_b)) if tage_b else None,'),
    ("Titel-Ueberlappung rechnet mit Tagen statt mit Titeln",
     '"anteil_titel": (len(titel_a & titel_b) / len(titel_a)) if titel_a else None,',
     '"anteil_titel": (len(tage_a & tage_b) / len(tage_a)) if tage_a else None,'),
    ("getrennte Zeitraeume gelten als ueberlappend",
     "if von > bis:\n        return None, None",
     "if False:\n        return None, None"),
]


def mutiertes_modul(alt: str, neu: str):
    with open(KERN_PFAD) as f:
        quelle = f.read()
    treffer = quelle.count(alt)
    if treffer != 1:
        raise AssertionError(
            f"Mutation trifft {treffer}-mal statt genau einmal: {alt!r}")
    modul = types.ModuleType("haltedauer_kern_mutiert")
    modul.__file__ = KERN_PFAD
    exec(compile(quelle.replace(alt, neu), "<mutiert>", "exec"), modul.__dict__)
    return modul


def mutationsproben():
    global FEHLER, LEISE
    print("\n12. Mutationsproben - jede Verfaelschung des Kerns muss auffallen")
    bestanden = 0
    for name, alt, neu in MUTATIONEN:
        modul = mutiertes_modul(alt, neu)
        gemerkt, FEHLER, LEISE = FEHLER, [], True
        try:
            try:
                pruefungsreihe(modul)
            except Exception as fehler:               # Absturz zaehlt als erkannt
                FEHLER.append(f"Absturz: {type(fehler).__name__}")
            erkannt, anzahl = bool(FEHLER), len(FEHLER)
        finally:
            FEHLER, LEISE = gemerkt, False
        if erkannt:
            print(f"  ok    {name} -> {anzahl} Pruefung(en) schlagen an")
            bestanden += 1
        else:
            print(f"  FEHLT {name} -> KEINE Pruefung schlaegt an")
            FEHLER.append(f"Mutation unerkannt: {name}")
    print(f"  {bestanden} von {len(MUTATIONEN)} Mutationen erkannt")


# ===========================================================================
# Wache: die Untersuchung fasst nichts aussehalb ihres Ordners an
# ===========================================================================

_PRODUKTIVORDNER = ("strategies", "shared", "results", "broker", "config",
                    "dashboard", "notifications", "system")


def _arbeitsbaum():
    """Zustand des Arbeitsbaums - Namen UND Inhalt der Aenderungen."""
    status = subprocess.run(["git", "--no-optional-locks", "status", "--porcelain"], cwd=_REPO_ROOT,
                            capture_output=True, text=True)
    diff = subprocess.run(["git", "--no-optional-locks", "diff", "--", *_PRODUKTIVORDNER],
                          cwd=_REPO_ROOT, capture_output=True, text=True)
    return status.stdout + "\n---\n" + diff.stdout


# Beim Laden dieses Tests aufgenommen, damit die Wache am Ende auch das
# sieht, was der TEST selbst angerichtet haben koennte - etwa eine
# Mutationsprobe, die versehentlich neben das Wegwerf-Verzeichnis schreibt.
_ARBEITSBAUM_ZU_BEGINN = None


# ---------------------------------------------------------------------------
# 13 (b) Schreibziele - je Schreibaufruf, ueber den Syntaxbaum (TB-175)
# ---------------------------------------------------------------------------
# Bis TB-175 galt: wer schreibt (open mit w/a/x oder JEDER to_csv/to_json-
# Aufruf), muss irgendwo im Quelltext ERGEBNIS_DIR, DATEN_DIR oder
# TemporaryDirectory nennen. Seit TB-98 (46e3ed0) schreibt
# positionen_holen.py in den Ordner aus dem Pflichtargument --ziel, ueber
# _schreibe_einmal (O_EXCL); die alte Fassung war damit rot, ohne dass falsch
# geschrieben wurde (`alle.to_csv(index=False)` liefert nur Text). Jetzt gilt
# je Schreibaufruf:
#   * allgemein: der Aufruf bildet sein Ziel aus ERGEBNIS_DIR oder DATEN_DIR
#     (beide genau einmal auf Modulebene aus `_DIR`), oder er liegt in einem
#     `with ...TemporaryDirectory()`-Block;
#   * positionen_holen.py (Register 36.1): ZIEL_DIR genau einmal, nur aus
#     `--ziel` (required=True, keine Voreinstellung, kein set_defaults), und
#     geschrieben wird nur in `_schreibe_einmal`, das mit O_CREAT|O_EXCL
#     (ohne O_TRUNC) in ZIEL_DIR oeffnet.

import ast as _ast

_ERLAUBTE_ORTE = ("ERGEBNIS_DIR", "DATEN_DIR")
_SCHREIBMODUS = ("w", "a", "x", "+")
_METHODE_ZIEL = {"to_csv": "path_or_buf", "to_json": "path_or_buf",
                 "to_excel": "excel_writer", "to_parquet": "path",
                 "to_pickle": "path", "to_feather": "path", "to_html": "buf",
                 "to_string": "buf", "to_markdown": "buf", "savefig": "fname"}
_OS_SCHREIBT = ("makedirs", "mkdir", "replace", "rename", "remove", "unlink",
                "rmdir", "symlink", "link", "truncate")
_SHUTIL_SCHREIBT = ("copy", "copy2", "copyfile", "copytree", "move", "rmtree")
_NP_SCHREIBT = ("save", "savetxt", "savez", "savez_compressed")
_OS_SCHREIBFLAGS = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_APPEND", "O_TRUNC")


def _namen(knoten):
    return {k.id for k in _ast.walk(knoten) if isinstance(k, _ast.Name)}


def _attrs(knoten):
    return {k.attr for k in _ast.walk(knoten) if isinstance(k, _ast.Attribute)}


def _modus(knoten, stelle):
    werte = list(knoten.args[stelle:stelle + 1]) + [
        k.value for k in knoten.keywords if k.arg == "mode"]
    if not werte:
        return False
    w = werte[0]
    if not (isinstance(w, _ast.Constant) and isinstance(w.value, str)):
        return True                     # Modus nicht ablesbar: gilt als schreibend
    return any(z in w.value for z in _SCHREIBMODUS)


def _schreibart(knoten):
    """Name der Schreibart, wenn der Aufruf schreibt, sonst None."""
    f = knoten.func
    basis = f.value.id if (isinstance(f, _ast.Attribute)
                           and isinstance(f.value, _ast.Name)) else None
    name = f.id if isinstance(f, _ast.Name) else getattr(f, "attr", None)
    if name == "open" and basis in (None, "io", "codecs", "builtins"):
        return "open" if _modus(knoten, 1) else None
    if name == "open" and basis == "os":
        return "os.open" if _attrs(knoten) & set(_OS_SCHREIBFLAGS) else None
    if name == "fdopen":
        return "os.fdopen" if _modus(knoten, 1) else None
    if basis == "os" and name in _OS_SCHREIBT:
        return "os." + name
    if basis == "shutil" and name in _SHUTIL_SCHREIBT:
        return "shutil." + name
    if basis in ("np", "numpy") and name in _NP_SCHREIBT:
        return "np." + name
    if name in ("write_text", "write_bytes"):
        return name
    if name in _METHODE_ZIEL and isinstance(f, _ast.Attribute):
        if knoten.args or any(k.arg == _METHODE_ZIEL[name] for k in knoten.keywords):
            return name                 # mit Ziel; ohne Ziel liefert es nur Text
    return None


def _schreibaufrufe(baum):
    """(Aufruf, Schreibart, umgebende Funktion, in TemporaryDirectory-Block)."""
    gefunden = []

    def gehe(knoten, funktion, temp):
        if isinstance(knoten, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
            funktion = knoten.name
        if isinstance(knoten, (_ast.With, _ast.AsyncWith)) and any(
                isinstance(p.context_expr, _ast.Call) and "TemporaryDirectory" in (
                    {getattr(p.context_expr.func, "id", None),
                     getattr(p.context_expr.func, "attr", None)})
                for p in knoten.items):
            temp = True
        if isinstance(knoten, _ast.Call):
            art = _schreibart(knoten)
            if art:
                gefunden.append((knoten, art, funktion, temp))
        for kind in _ast.iter_child_nodes(knoten):
            gehe(kind, funktion, temp)

    gehe(baum, None, False)
    return gefunden


def _zuweisungen(baum, name):
    """Alle Zuweisungen an `name` (auch in Funktionen), als (Knoten, Wert, Modulebene)."""
    oben = set(id(k) for k in baum.body)
    gef = []
    for k in _ast.walk(baum):
        ziele = (k.targets if isinstance(k, _ast.Assign) else
                 [k.target] if isinstance(k, (_ast.AnnAssign, _ast.AugAssign)) else [])
        for z in ziele:
            if name in {t.id for t in _ast.walk(z) if isinstance(t, _ast.Name)}:
                gef.append((k, getattr(k, "value", None), id(k) in oben))
        if isinstance(k, _ast.Global) and name in k.names:
            gef.append((k, None, False))
    return gef


def _regel_allgemein(baum, aufrufe):
    grund = []
    for ort in _ERLAUBTE_ORTE:
        z = _zuweisungen(baum, ort)
        if z and not (len(z) == 1 and z[0][2] and "_DIR" in _namen(z[0][1])):
            grund.append(f"{ort} nicht genau einmal auf Modulebene aus _DIR")
    for knoten, art, _funktion, temp in aufrufe:
        if temp:
            continue
        if not (_namen(knoten) & set(_ERLAUBTE_ORTE)) or not any(
                _zuweisungen(baum, o) for o in _namen(knoten) & set(_ERLAUBTE_ORTE)):
            grund.append(f"Z. {knoten.lineno} {art} ohne ERGEBNIS_DIR/DATEN_DIR")
    return grund


def _regel_positionen_holen(baum, aufrufe):
    """Register 36.1: Ziel nur aus --ziel, Schreiben nur ueber _schreibe_einmal."""
    grund = []
    ziel_arg = [k for k in _ast.walk(baum) if isinstance(k, _ast.Call)
                and getattr(k.func, "attr", None) == "add_argument"
                and any(isinstance(a, _ast.Constant) and a.value == "--ziel"
                        for a in k.args)]
    if len(ziel_arg) != 1:
        grund.append(f"--ziel {len(ziel_arg)}-mal statt genau einmal")
    else:
        kw = {k.arg: k.value for k in ziel_arg[0].keywords}
        if not (isinstance(kw.get("required"), _ast.Constant)
                and kw["required"].value is True):
            grund.append("--ziel nicht required=True")
        if "default" in kw:
            grund.append("--ziel mit Voreinstellung (default)")
    if any(isinstance(k, _ast.Call) and getattr(k.func, "attr", None) == "set_defaults"
           for k in _ast.walk(baum)):
        grund.append("set_defaults vorhanden")
    leser = {z.id for k in _ast.walk(baum) if isinstance(k, _ast.Assign)
             and isinstance(k.value, _ast.Call)
             and getattr(k.value.func, "attr", None) == "parse_args"
             for z in k.targets if isinstance(z, _ast.Name)}
    erlaubt = {_ast.dump(_ast.parse(f"os.path.abspath({n}.ziel)", mode="eval").body)
               for n in leser} | {_ast.dump(_ast.parse(f"{n}.ziel", mode="eval").body)
                                  for n in leser}
    z = _zuweisungen(baum, "ZIEL_DIR")
    if not (len(z) == 1 and z[0][2] and z[0][1] is not None
            and _ast.dump(z[0][1]) in erlaubt):
        grund.append("ZIEL_DIR nicht genau einmal, nur aus --ziel")
    defs = [k for k in baum.body if isinstance(k, _ast.FunctionDef)
            and k.name == "_schreibe_einmal"]
    if len(defs) != 1:
        grund.append("_schreibe_einmal nicht genau einmal auf Modulebene")
    for knoten, art, funktion, _temp in aufrufe:
        if funktion != "_schreibe_einmal":
            grund.append(f"Z. {knoten.lineno} {art} ausserhalb von _schreibe_einmal")
        elif art == "os.open":
            fl = set().union(*(_attrs(a) for a in knoten.args[1:2]))
            pfad = knoten.args[0] if knoten.args else None
            aus_ziel = pfad is not None and ("ZIEL_DIR" in _namen(pfad) or any(
                "ZIEL_DIR" in _namen(w) for _k, w, _o in (
                    _zuweisungen(defs[0], pfad.id) if defs and isinstance(pfad, _ast.Name)
                    else []) if w is not None))
            if not ({"O_CREAT", "O_EXCL"} <= fl) or "O_TRUNC" in fl:
                grund.append(f"Z. {knoten.lineno} os.open ohne O_CREAT|O_EXCL")
            if not aus_ziel:
                grund.append(f"Z. {knoten.lineno} os.open nicht in ZIEL_DIR")
        elif art != "os.fdopen":
            grund.append(f"Z. {knoten.lineno} {art} in _schreibe_einmal")
    if defs and not any(art == "os.open" and f == "_schreibe_einmal"
                        for _k, art, f, _t in aufrufe):
        grund.append("_schreibe_einmal ohne os.open")
    return grund


_SONDERREGELN = {"positionen_holen.py": _regel_positionen_holen}


def schreibziele_aus_quellen(quellen):
    """quellen: {Dateiname: Quelltext}. Liefert [(Datei, Grund)] - leer = gut."""
    befund = []
    for name in sorted(quellen):
        baum = _ast.parse(quellen[name])
        aufrufe = _schreibaufrufe(baum)
        regel = _SONDERREGELN.get(name)
        if regel is None and not aufrufe:
            continue
        for g in (regel or _regel_allgemein)(baum, aufrufe):
            befund.append((name, g))
    return befund


def _gruppe(ordner):
    return {n: open(os.path.join(ordner, n), encoding="utf-8").read()
            for n in sorted(os.listdir(ordner))
            if n.endswith(".py") and not n.startswith("test_")}


# Gegenproben zu 13 (b) (Prinzip 12): je EINE Stelle im Quelltext verfaelscht,
# nur im Speicher; jede muss genau einmal treffen und die Datei rot machen.
GEGENPROBEN_13 = [
    ("--ziel mit Voreinstellung", "positionen_holen.py",
     '_aufruf.add_argument("--ziel", required=True,',
     '_aufruf.add_argument("--ziel", required=True, default=".",'),
    ("--ziel nicht Pflicht", "positionen_holen.py",
     '_aufruf.add_argument("--ziel", required=True,',
     '_aufruf.add_argument("--ziel", required=False,'),
    ("ZIEL_DIR nicht aus --ziel", "positionen_holen.py",
     "ZIEL_DIR = os.path.abspath(_args.ziel)",
     'ZIEL_DIR = os.path.join(_DIR, "daten")'),
    ("O_EXCL durch O_TRUNC ersetzt", "positionen_holen.py",
     "os.O_WRONLY | os.O_CREAT | os.O_EXCL",
     "os.O_WRONLY | os.O_CREAT | os.O_TRUNC"),
    ('open(..., "w") statt _schreibe_einmal', "positionen_holen.py",
     'hashes[f"{BOT}_alle_trades.csv"] = _schreibe_einmal(\n'
     '        f"{BOT}_alle_trades.csv", alle.to_csv(index=False))',
     'open(os.path.join(ZIEL_DIR, f"{BOT}_alle_trades.csv"), "w").write(\n'
     '        alle.to_csv(index=False))'),
    ("auswertung.py schreibt neben ERGEBNIS_DIR", "auswertung.py",
     'open(os.path.join(ERGEBNIS_DIR, "zusammenfassung.json"), "w")',
     'open(os.path.join(_DIR, "..", "zusammenfassung.json"), "w")'),
]


def wache_repo_unveraendert(ordner=None):
    """Die Untersuchung fasst nichts ausserhalb ihres Ordners an.

    Bis TB-30a stand hier eine andere Pruefung: `git status` durfte nichts
    ausserhalb von `research/tb24_haltedauern/` und `docs/` melden. Die war
    falsch gebaut, und zwar so, dass es erst auffiel, als sie zum ersten Mal
    anschlug.

    Sie prueft naemlich nicht diese Untersuchung, sondern den ARBEITSBAUM -
    und der enthaelt alles, woran gerade sonst noch gearbeitet wird. TB-30a
    aendert `shared/` und legt `research/vorregistrierung/` an, beides
    ausdruecklich beauftragt und mit TB-24 nicht verwandt. Die alte Fassung
    meldete das als Verstoss von TB-24. Ein Waechter, der bei fremder Arbeit
    rot wird, wird abgeschaltet - und dann faengt er auch den Fall nicht
    mehr, fuer den er da ist. (Dieselbe Falle steckte in
    `research/versuchsregister/test_versuchsregister.py`; sie ist dort in
    derselben Aenderung behoben.)

    An ihre Stelle treten zwei Zusicherungen, die beide diese Untersuchung
    betreffen und beide rot werden koennen:

      1. **Dieser Testlauf veraendert nichts.** Aufgenommen beim Laden,
         verglichen am Ende - inklusive der zehn Mutationsproben, die
         dazwischen laufen.
      2. **Wer schreibt, schreibt in den eigenen Ordner.** Ueber den
         Syntaxbaum geprueft, nicht ueber eine Textsuche: ein Kommentar mit
         `open(..., "w")` soll nicht anschlagen. Seit TB-175 je
         Schreibaufruf: Ziel aus ERGEBNIS_DIR/DATEN_DIR, bei
         `positionen_holen.py` nur aus `--ziel` ueber `_schreibe_einmal`
         (O_EXCL); dazu sechs Gegenproben im Speicher (GEGENPROBEN_13).

    Was hier bewusst NICHT geschieht: `auswertung.py` starten. Es wuerde die
    abgelegten Ergebnisdateien neu schreiben - eine Wache, die den Zustand
    veraendert, den sie prueft, ist keine.
    """
    print("\n13. Wache: die Untersuchung fasst nichts ausserhalb ihres "
          "Ordners an")
    ausgabe = subprocess.run(["git", "--no-optional-locks", "status", "--porcelain"], cwd=_REPO_ROOT,
                              capture_output=True, text=True)
    if ausgabe.returncode != 0:
        pruefe(False, "git status nicht ausfuehrbar")
        return

    pruefe(_ARBEITSBAUM_ZU_BEGINN == _arbeitsbaum(),
           "dieser Testlauf hat den Arbeitsbaum nicht veraendert")

    # (b) TB-175: jeder Schreibaufruf an einen erlaubten Ort (Regeln oben).
    quellen = _gruppe(ordner or _DIR)
    befund = schreibziele_aus_quellen(quellen)
    pruefe(not befund,
           f"wer schreibt, schreibt nur an einen erlaubten Ort "
           f"(aussen vor: {befund or 'keine'})")
    for titel, datei, alt, neu in GEGENPROBEN_13:
        treffer = quellen.get(datei, "").count(alt)
        rot = treffer == 1 and any(
            d == datei for d, _g in schreibziele_aus_quellen(
                dict(quellen, **{datei: quellen[datei].replace(alt, neu)})))
        pruefe(rot, f"Gegenprobe 13: {titel} -> {datei} faellt auf"
                    + ("" if treffer == 1 else f" (trifft {treffer}-mal)"))


# ===========================================================================
# Der Live-Weg: dass er "keine Datenbank gefunden" meldet, beweist nichts
# ===========================================================================

def pruefe_live_weg():
    """`live_haltedauern.py` findet in dieser Umgebung keine Datenbank. Eine
    Meldung "nichts gefunden" ist aber kein Beleg dafuer, dass der Weg
    funktionieren WUERDE - genau die Falle aus Prinzip 12. Hier wird deshalb
    eine Datenbank mit dem echten Schema aufgebaut, mit von Hand
    nachrechenbaren Trades gefuellt und ausgelesen.
    """
    import shutil
    import sqlite3
    import tempfile

    print("\n14. Live-Weg gegen eine gebaute Datenbank (Gegenprobe zu 'nichts gefunden')")
    import live_haltedauern as lh

    ordner = tempfile.mkdtemp(prefix="tb24_live_")
    try:
        pfad = os.path.join(ordner, "paper_trading_elliott_wave.db")
        conn = sqlite3.connect(pfad)
        conn.execute("CREATE TABLE trades (symbol TEXT, entry_time TEXT, "
                      "exit_time TEXT, result TEXT, pnl_pct REAL, status TEXT)")
        conn.executemany("INSERT INTO trades VALUES (?,?,?,?,?,?)", [
            # 3 Tage, Strategie-Ausstieg
            ("BTCUSDT", "2026-09-01 07:00:00", "2026-09-04 07:00:00", "stop_loss", -6.0, "closed"),
            # 10 Tage, Strategie-Ausstieg
            ("ETHUSDT", "2026-09-02 07:00:00", "2026-09-12 07:00:00", "time_exit", 2.0, "closed"),
            # 2 Tage, aber vom Nutzer geschlossen - darf NICHT in den Median
            ("XRPUSDT", "2026-09-03 07:00:00", "2026-09-05 07:00:00", "manual_close", 1.0, "closed"),
            # offen - darf gar nicht gelesen werden
            ("ADAUSDT", "2026-09-10 07:00:00", None, None, None, "open"),
        ])
        conn.commit()
        conn.close()

        gemerkt = lh._REPO_ROOT
        lh._REPO_ROOT = ordner
        try:
            df = lh.lese_trades("elliott_wave")
            fehlt = lh.lese_trades("t3_supertrend")
        finally:
            lh._REPO_ROOT = gemerkt

        pruefe(df is not None and len(df) == 3,
               "14.1 drei geschlossene Trades gelesen, der offene nicht")
        pruefe(fehlt is None,
               "14.2 Gegenprobe: fehlende Datenbank gibt None, nicht einen leeren Satz - "
               "'nicht nachgesehen' und 'nichts da' bleiben unterscheidbar")

        strategie = df[df["result"] != lh.MANUELL]
        tage = sorted(haltedauer_kern.haltedauer_tage(strategie))
        pruefe(tage == [3.0, 10.0],
               "14.3 Haltedauern 3 und 10 Tage - der manuelle Ausstieg (2 Tage) "
               "bleibt aussen vor")
        pruefe(haltedauer_kern.kennzahlen(tage)["median"] == 6.5,
               "14.4 Median daraus 6,5 Tage")

        # Gegenprobe zum Schreibschutz: mode=ro muss einen Schreibversuch
        # abweisen. Sonst waere "liest nur" eine Behauptung, keine Eigenschaft.
        verweigert = False
        try:
            with sqlite3.connect(f"file:{pfad}?mode=ro", uri=True) as c:
                c.execute("DELETE FROM trades")
        except sqlite3.OperationalError:
            verweigert = True
        pruefe(verweigert,
               "14.5 mode=ro verweigert einen Schreibversuch auf dieselbe Datei")
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


if __name__ == "__main__":
    # Vor allem anderen: der Ausgangszustand des Arbeitsbaums. Die Wache in
    # Abschnitt 13 vergleicht ihn am Ende mit dem dann erreichten - so sieht
    # sie auch, was dieser Test selbst angerichtet haette.
    _ARBEITSBAUM_ZU_BEGINN = _arbeitsbaum()

    print("1.-11. Gegenproben auf dem echten Rechenkern")
    pruefungsreihe(haltedauer_kern)
    print(f"  {GEZAEHLT[0] - len(FEHLER)} von {GEZAEHLT[0]} Gegenproben bestanden")

    pruefe_live_weg()
    mutationsproben()
    wache_repo_unveraendert()

    print()
    if FEHLER:
        print(f"{len(FEHLER)} Pruefung(en) fehlgeschlagen:")
        for f in FEHLER:
            print(f"  - {f}")
        sys.exit(1)
    print("Alle Pruefungen bestanden.")
