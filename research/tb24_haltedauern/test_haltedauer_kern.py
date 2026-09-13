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

def wache_repo_unveraendert():
    print("\n13. Wache: keine Aenderung ausserhalb von research/tb24_haltedauern/ und docs/")
    ausgabe = subprocess.run(["git", "status", "--porcelain"], cwd=_REPO_ROOT,
                              capture_output=True, text=True)
    if ausgabe.returncode != 0:
        pruefe(False, "git status nicht ausfuehrbar")
        return
    fremd = []
    for zeile in ausgabe.stdout.splitlines():
        pfad = zeile[3:].strip().strip('"')
        if " -> " in pfad:
            pfad = pfad.split(" -> ")[-1]
        if not (pfad.startswith("research/tb24_haltedauern/") or pfad.startswith("docs/")):
            fremd.append(pfad)
    pruefe(not fremd, f"keine fremden Pfade geaendert (gefunden: {fremd or 'keine'})")


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
