"""
Selbsttests: die Zuteilungskaskade (TB-26)
==============================================================================
Geprueft wird das VERHALTEN von `shared/zuteilung.py` - nicht sein Quelltext.
Keine Textsuche, kein Test-Framework (wie in allen uebrigen Selbsttests dieses
Projekts).

    python3 shared/test_zuteilung.py
    python3 shared/test_zuteilung.py --schnell   # ohne Abschnitt 8 und 9


DIE ZUSICHERUNGEN
------------------------------------------------------------------------------
1. Jede Stufe der Kaskade greift, und zwar an ihrer Stelle. Je Stufe gibt es
   einen Pruefall, in dem **nur diese Stufe** entscheiden kann.
2. Der seeded Zufall ist reproduzierbar: derselbe Startwert, dasselbe
   Ergebnis; ein anderer Startwert, ein anderes. Und der Startwert steht im
   Protokoll.
3. Fehlende Angaben werden nach der benannten Regel behandelt (Median der
   vorliegenden Werte), nicht stillschweigend ans Ende geschoben.
4. Das Ergebnis haengt nicht mehr an der Reihenfolge - weder an der der
   Trade-Zeilen noch an der der Symbole.
5. Wo nichts knapp wird, rechnet die neue Fassung wie die alte.


DIE BEIDEN WIEDERKEHRENDEN FALLEN (#73, #77, #78, #79, #81, #86, TB-15,
TB-20, TB-22)
------------------------------------------------------------------------------
**Falle 1 - die selbstbestaetigende Probe.** Kein Erwartungswert stammt aus
einem Lauf der geprueften Funktion. Die Gewinner der Abschnitte 1 bis 3 sind
aus der Konstruktion der Eingabe hergeleitet (staerkstes Signal / niedrigste
Korrelation / hoechste Liquiditaet), die Gegenprobe in Abschnitt 7 vergleicht
gegen eine im Test mitgefuehrte Kopie der Fassung VOR TB-26.

Und dass die Proben ueberhaupt unterscheiden, wird nicht vorausgesetzt,
sondern am ABLAUF nachgewiesen: Abschnitt 8 laesst dieselben Abschnitte gegen
mutierte Kopien von `shared/zuteilung.py` laufen, in denen je eine Wache
entfernt ist. Schlaegt eine Mutante nicht fehl, ist der Test durchgefallen -
nicht bestanden.

**Falle 2 - die zweite Wache verdeckt das Fehlen der ersten.** Vier Stufen
koennen nacheinander zugreifen; ein Pruefall, den mehrere loesen koennten,
sagt ueber keine von ihnen etwas. Die Faelle sind deshalb so gebaut, dass die
jeweils geprueften Stufe als einzige entscheiden KANN:

  * Abschnitt 1 (Signalstaerke): leeres Buch -> Stufe 2 entfaellt; keine
    Kursdaten -> Stufe 3 entfaellt. Bleiben Stufe 1 und der Zufall.
  * Abschnitt 2 (Diversifikation): kein Primaerschluessel -> Stufe 1
    entfaellt; die beiden Kandidaten haben ein IDENTISCHES Dollar-Volumen ->
    Stufe 3 kann nicht entscheiden.
  * Abschnitt 3 (Liquiditaet): kein Primaerschluessel; die beiden Kandidaten
    haben IDENTISCHE Renditereihen -> Stufe 2 kann nicht entscheiden.

Damit bliebe in jedem dieser Faelle noch der Zufall der letzten Stufe als
zweite Wache. Deshalb wird in jedem Abschnitt zusaetzlich festgestellt, wen
der Zufall gewaehlt HAETTE - und verlangt, dass es der andere ist. Faellt
beides zusammen, ist der Pruefall stumm; das meldet der Test als Fehler und
nicht als Erfolg.
"""

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)
ZUTEILUNG_PY = os.path.join(_SHARED_DIR, "zuteilung.py")

TAGE = pd.date_range("2024-01-01", periods=140, freq="D")


# ===========================================================================
# Protokoll (gleiche Form wie in den uebrigen Selbsttests)
# ===========================================================================
class Protokoll:
    """Sammelt Pruefungen, statt beim ersten Fehler abzubrechen."""

    def __init__(self, still=False):
        self.ok = 0
        self.fehler = []
        self.abschnitte = set()
        self.ausgelassen = []
        self.still = still

    def lasse_aus(self, text: str, grund: str):
        """Eine Pruefung, die in dieser Umgebung nicht laufen KANN - benannt,
        nicht verschwiegen. Vorbild: `dashboard/test_dashboard.py` meldet ohne
        `node` 780/780 statt 784 und sagt dazu, welche vier fehlen."""
        self.ausgelassen.append(f"{text} ({grund})")
        if not self.still:
            print(f"  AUS   {text}  [{grund}]")

    def pruefe(self, abschnitt: str, text: str, bedingung: bool, zusatz: str = ""):
        if bedingung:
            self.ok += 1
            if not self.still:
                print(f"  OK    {text}")
        else:
            self.fehler.append(f"{abschnitt}: {text}"
                               + (f" - {zusatz}" if zusatz else ""))
            self.abschnitte.add(abschnitt)
            if not self.still:
                print(f"  FEHLT {text}" + (f"  [{zusatz}]" if zusatz else ""))


def lade(pfad: str, name: str):
    spec = importlib.util.spec_from_file_location(name, pfad)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


# ===========================================================================
# Bausteine fuer die Pruefdaten
# ===========================================================================
def kursreihe(renditen, startkurs=100.0, volumen=1_000_000.0):
    """Ein Kursrahmen in der Form, die die Bots laden: open_time/close/volume.

    Die erste Zeile traegt den Startkurs, danach folgen die vorgegebenen
    Tagesrenditen - so ist die Renditereihe des Rahmens exakt bekannt und
    nicht aus der geprueften Funktion abgeleitet."""
    kurse = [startkurs]
    for r in renditen:
        kurse.append(kurse[-1] * (1 + r))
    n = len(kurse)
    return pd.DataFrame({
        "open_time": TAGE[:n],
        "open": kurse, "high": kurse, "low": kurse, "close": kurse,
        "volume": [volumen / k for k in kurse],   # -> close*volume = volumen
    })


def zufallsrenditen(startwert: int, anzahl: int = 139):
    return np.random.RandomState(startwert).normal(0, 0.01, anzahl)


def tabelle(zeilen: list) -> pd.DataFrame:
    """Eine Trade-Tabelle in der Form, die `collect_all_trades` liefert."""
    df = pd.DataFrame(zeilen)
    df["entry_time"] = pd.to_datetime(df["entry_time"])
    df["exit_time"] = pd.to_datetime(df["exit_time"])
    return df


def zufallsgewinner(modul, trades, kandidaten, zeit):
    """Wen HAETTE die letzte Stufe gewaehlt?

    Ohne Kursdaten und ohne Primaerschluessel kann nur der Zufall
    entscheiden - der Rueckgabewert ist also genau dessen Wahl. Gebraucht
    wird sie, um in den Abschnitten 1 bis 3 auszuschliessen, dass die
    geprueften Stufe nur zufaellig dasselbe Ergebnis liefert wie die letzte.
    """
    zuteiler = modul.Zuteiler(trades, None, None, modul.SEED)
    return zuteiler.waehle(list(kandidaten), [], zeit)


def zeile_von(trades, symbol) -> int:
    treffer = [i for i, s in enumerate(trades["symbol"]) if s == symbol]
    assert len(treffer) == 1, symbol
    return treffer[0]


def unterscheidender_fall(modul, bauer, gewinner: str, verlierer: str, zeit):
    """Sucht eine Trade-Tabelle, in der die letzte Stufe den VERLIERER
    gewaehlt haette.

    Ohne das waere ein Pruefall moeglicherweise stumm: kaeme der Zufall
    zufaellig auf denselben Kandidaten wie die geprueften Stufe, bestuende
    der Abschnitt auch dann, wenn die Stufe gar nicht greift (Falle 2 - die
    zweite Wache verdeckt das Fehlen der ersten).

    Gesucht wird ueber den Ausstiegstag der beiden Kandidaten - eine Groesse,
    die in den Fingerabdruck der letzten Stufe eingeht und sonst nichts
    bewirkt, weil beide Trades ohnehin nach dem Entscheidungszeitpunkt enden.
    Findet sich keiner, ist das ein Fehlschlag und kein stilles Ueberspringen.
    """
    for tag in range(12, 30):
        trades = bauer(tag)
        a, b = zeile_von(trades, gewinner), zeile_von(trades, verlierer)
        if zufallsgewinner(modul, trades, [a, b], zeit) == b:
            return trades, tag
    return None, None


# ===========================================================================
# Abschnitt 1 - Stufe 1 (Signalstaerke) entscheidet, und nur sie kann es
# ===========================================================================
def abschnitt1(modul, p: Protokoll):
    """Zwei Kandidaten, ein Platz, leeres Buch, KEINE Kursdaten.

    Stufe 2 entfaellt (leeres Buch), Stufe 3 entfaellt (keine Kursdaten).
    Entscheiden kann also nur die Signalstaerke - oder der Zufall. Der
    erwartete Gewinner ist der mit dem niedrigeren `staerke`-Wert (Richtung
    AUFSTEIGEND), und es wird verlangt, dass der Zufall den ANDEREN gewaehlt
    haette.
    """
    trades = tabelle([
        {"symbol": "STARK", "entry_time": "2024-03-01", "exit_time": "2024-03-10",
         "entry_price": 10.0, "exit_price": 11.0, "pnl_pct": 10.0, "staerke": 1.5},
        {"symbol": "SCHWACH", "entry_time": "2024-03-01", "exit_time": "2024-03-11",
         "entry_price": 20.0, "exit_price": 21.0, "pnl_pct": 5.0, "staerke": 4.5},
    ])
    zeit = pd.Timestamp("2024-03-01")
    stark, schwach = zeile_von(trades, "STARK"), zeile_von(trades, "SCHWACH")

    zufall = zufallsgewinner(modul, trades, [stark, schwach], zeit)
    p.pruefe("Abschnitt 1",
             "der Pruefall unterscheidet ueberhaupt (Zufall haette den anderen gewaehlt)",
             zufall == schwach,
             "Zufall und Signalstaerke waehlen denselben - der Fall ist stumm")

    erg = modul.simuliere_portfolio(
        trades, 10_000.0, 0.10, max_concurrent_positions=1,
        kursdaten=None, signalspalte=("staerke", modul.AUFSTEIGEND))
    gehandelt = set(erg["equity_curve"]["symbol"])
    p.pruefe("Abschnitt 1", "das staerkere Signal bekommt den Platz",
             gehandelt == {"STARK"}, f"gehandelt: {sorted(gehandelt)}")
    p.pruefe("Abschnitt 1", "das Protokoll schreibt die Entscheidung Stufe 1 zu",
             erg["zuteilung"]["entschieden_durch"][modul.STUFE_SIGNAL] == 1,
             str(erg["zuteilung"]["entschieden_durch"]))

    # Dieselbe Tabelle mit umgedrehter Richtung muss den anderen waehlen -
    # sonst waere nicht belegt, dass der WERT und nicht die Zeilenlage
    # entscheidet.
    erg_ab = modul.simuliere_portfolio(
        trades, 10_000.0, 0.10, max_concurrent_positions=1,
        kursdaten=None, signalspalte=("staerke", modul.ABSTEIGEND))
    p.pruefe("Abschnitt 1", "umgedrehte Richtung waehlt den anderen Kandidaten",
             set(erg_ab["equity_curve"]["symbol"]) == {"SCHWACH"},
             str(set(erg_ab["equity_curve"]["symbol"])))

    # Eine Spalte, die es nicht gibt, muss auffallen statt lautlos auf eine
    # Kaskade ohne Stufe 1 zu rutschen.
    try:
        modul.simuliere_portfolio(trades, 10_000.0, 0.10, 1, None,
                                  signalspalte=("gibtsnicht", modul.AUFSTEIGEND))
        laut = False
    except KeyError:
        laut = True
    p.pruefe("Abschnitt 1", "unbekannte SIGNALSPALTE bricht ab, statt still zu ruhen",
             laut)


# ===========================================================================
# Abschnitt 2 - Stufe 2 (Diversifikation) entscheidet, und nur sie kann es
# ===========================================================================
def _kursdaten_diversifikation():
    """BUCH liegt im Buch. GLEICHLAUF hat exakt dessen Renditen (Korrelation
    +1), GEGENLAUF genau die gespiegelten (Korrelation -1). Beide Kandidaten
    haben dasselbe Dollar-Volumen - Stufe 3 kann nicht entscheiden."""
    r = zufallsrenditen(7)
    return {
        "BUCH": kursreihe(r, volumen=5_000_000.0),
        "GLEICHLAUF": kursreihe(r, startkurs=50.0, volumen=1_000_000.0),
        "GEGENLAUF": kursreihe(-r, startkurs=80.0, volumen=1_000_000.0),
    }


def _trades_diversifikation(tag: int = 20):
    return tabelle([
        {"symbol": "BUCH", "entry_time": "2024-03-01", "exit_time": "2024-05-15",
         "entry_price": 10.0, "exit_price": 11.0, "pnl_pct": 1.0},
        {"symbol": "GLEICHLAUF", "entry_time": "2024-04-01",
         "exit_time": f"2024-04-{tag:02d}",
         "entry_price": 20.0, "exit_price": 21.0, "pnl_pct": 2.0},
        {"symbol": "GEGENLAUF", "entry_time": "2024-04-01",
         "exit_time": f"2024-04-{tag + 1:02d}",
         "entry_price": 30.0, "exit_price": 31.0, "pnl_pct": 3.0},
    ])


def abschnitt2(modul, p: Protokoll):
    kurse = _kursdaten_diversifikation()
    zeit = pd.Timestamp("2024-04-01")
    trades, tag = unterscheidender_fall(modul, _trades_diversifikation,
                                        "GEGENLAUF", "GLEICHLAUF", zeit)
    p.pruefe("Abschnitt 2",
             "der Pruefall unterscheidet ueberhaupt (Zufall haette den anderen gewaehlt)",
             trades is not None,
             "kein Ausstiegstag gefunden, bei dem Zufall und Diversifikation "
             "auseinanderfallen - der Fall waere stumm")
    if trades is None:
        return

    erg = modul.simuliere_portfolio(trades, 10_000.0, 0.10,
                                    max_concurrent_positions=2, kursdaten=kurse)
    gehandelt = set(erg["equity_curve"]["symbol"])
    p.pruefe("Abschnitt 2", "der unkorrelierteste Kandidat bekommt den Platz",
             gehandelt == {"BUCH", "GEGENLAUF"}, f"gehandelt: {sorted(gehandelt)}")
    p.pruefe("Abschnitt 2", "das Protokoll schreibt die Entscheidung Stufe 2 zu",
             erg["zuteilung"]["entschieden_durch"][modul.STUFE_DIVERSIFIKATION] == 1,
             str(erg["zuteilung"]["entschieden_durch"]))

    # Die gemessenen Korrelationen selbst - der Wert, auf dem die Stufe
    # beruht, wird nicht nur indirekt geprueft.
    vorrat = modul.Kursvorrat(kurse)
    ende = vorrat.fensterende(zeit)
    reihe = vorrat.buchreihe([("BUCH", 1000.0)], ende)
    k_gleich = vorrat.korrelation("GLEICHLAUF", reihe, ende)
    k_gegen = vorrat.korrelation("GEGENLAUF", reihe, ende)
    p.pruefe("Abschnitt 2", "Korrelation des Gleichlaeufers ist ~ +1",
             k_gleich is not None and abs(k_gleich - 1.0) < 1e-6, str(k_gleich))
    p.pruefe("Abschnitt 2", "Korrelation des Gegenlaeufers ist ~ -1",
             k_gegen is not None and abs(k_gegen + 1.0) < 1e-6, str(k_gegen))

    # Point-in-time: das Fenster endet VOR dem Einstiegstag.
    p.pruefe("Abschnitt 2", "das Fenster endet vor dem Kalendertag des Einstiegs",
             vorrat.fensterende(pd.Timestamp("2024-04-01 23:00")) ==
             vorrat.fensterende(pd.Timestamp("2024-04-01")),
             "eine Uhrzeit am Einstiegstag verschiebt das Fenster")
    p.pruefe("Abschnitt 2", "der Einstiegstag selbst zaehlt nicht mehr mit",
             vorrat.fensterende(pd.Timestamp("2024-04-02")) -
             vorrat.fensterende(pd.Timestamp("2024-04-01")) == 1)


# ===========================================================================
# Abschnitt 3 - Stufe 3 (Liquiditaet) entscheidet, und nur sie kann es
# ===========================================================================
def _kursdaten_liquiditaet():
    """Beide Kandidaten haben IDENTISCHE Renditereihen - ihre Korrelation mit
    jedem denkbaren Buch ist damit dieselbe, Stufe 2 kann nicht entscheiden.
    Sie unterscheiden sich ausschliesslich im Dollar-Volumen."""
    r_buch = zufallsrenditen(11)
    r_kand = zufallsrenditen(12)
    return {
        "BUCH": kursreihe(r_buch, volumen=5_000_000.0),
        "DUENN": kursreihe(r_kand, startkurs=50.0, volumen=200_000.0),
        "DICK": kursreihe(r_kand, startkurs=80.0, volumen=9_000_000.0),
    }


def _trades_liquiditaet(tag: int = 20):
    return tabelle([
        {"symbol": "BUCH", "entry_time": "2024-03-01", "exit_time": "2024-05-15",
         "entry_price": 10.0, "exit_price": 11.0, "pnl_pct": 1.0},
        {"symbol": "DUENN", "entry_time": "2024-04-01",
         "exit_time": f"2024-04-{tag:02d}",
         "entry_price": 20.0, "exit_price": 21.0, "pnl_pct": 2.0},
        {"symbol": "DICK", "entry_time": "2024-04-01",
         "exit_time": f"2024-04-{tag + 1:02d}",
         "entry_price": 30.0, "exit_price": 31.0, "pnl_pct": 3.0},
    ])


def abschnitt3(modul, p: Protokoll):
    kurse = _kursdaten_liquiditaet()
    zeit = pd.Timestamp("2024-04-01")
    trades, tag = unterscheidender_fall(modul, _trades_liquiditaet,
                                        "DICK", "DUENN", zeit)
    p.pruefe("Abschnitt 3",
             "der Pruefall unterscheidet ueberhaupt (Zufall haette den anderen gewaehlt)",
             trades is not None,
             "kein Ausstiegstag gefunden, bei dem Zufall und Liquiditaet "
             "auseinanderfallen - der Fall waere stumm")
    if trades is None:
        return

    erg = modul.simuliere_portfolio(trades, 10_000.0, 0.10,
                                    max_concurrent_positions=2, kursdaten=kurse)
    gehandelt = set(erg["equity_curve"]["symbol"])
    p.pruefe("Abschnitt 3", "der liquidere Kandidat bekommt den Platz",
             gehandelt == {"BUCH", "DICK"}, f"gehandelt: {sorted(gehandelt)}")
    p.pruefe("Abschnitt 3", "das Protokoll schreibt die Entscheidung Stufe 3 zu",
             erg["zuteilung"]["entschieden_durch"][modul.STUFE_LIQUIDITAET] == 1,
             str(erg["zuteilung"]["entschieden_durch"]))

    vorrat = modul.Kursvorrat(kurse)
    ende = vorrat.fensterende(zeit)
    p.pruefe("Abschnitt 3", "das Dollar-Volumen wird als close*volume gemessen",
             abs(vorrat.liquiditaet("DICK", ende) - 9_000_000.0) < 1.0,
             str(vorrat.liquiditaet("DICK", ende)))

    # Leeres Buch: Stufe 2 entfaellt und die Kaskade rueckt auf Stufe 3 vor.
    # Auch das muss deterministisch sein und darf nicht beim Zufall landen.
    ohne_buch = tabelle([
        {"symbol": "DUENN", "entry_time": "2024-04-01", "exit_time": "2024-04-20",
         "entry_price": 20.0, "exit_price": 21.0, "pnl_pct": 2.0},
        {"symbol": "DICK", "entry_time": "2024-04-01", "exit_time": "2024-04-21",
         "entry_price": 30.0, "exit_price": 31.0, "pnl_pct": 3.0},
    ])
    erg2 = modul.simuliere_portfolio(ohne_buch, 10_000.0, 0.10,
                                     max_concurrent_positions=1, kursdaten=kurse)
    p.pruefe("Abschnitt 3", "bei leerem Buch entfaellt Stufe 2 und Stufe 3 entscheidet",
             set(erg2["equity_curve"]["symbol"]) == {"DICK"}
             and erg2["zuteilung"]["entschieden_durch"][modul.STUFE_LIQUIDITAET] == 1,
             str(erg2["zuteilung"]["entschieden_durch"]))


# ===========================================================================
# Abschnitt 4 - Stufe 4: derselbe Startwert dasselbe Ergebnis, ein anderer
#               ein anderes - und der Startwert steht im Protokoll
# ===========================================================================
def _trades_zufall(anzahl: int = 12):
    return tabelle([
        {"symbol": f"S{i:02d}", "entry_time": "2024-04-01",
         "exit_time": f"2024-04-{10 + i:02d}",
         "entry_price": 10.0 + i, "exit_price": 11.0 + i, "pnl_pct": 1.0 + i}
        for i in range(anzahl)
    ])


def abschnitt4(modul, p: Protokoll):
    """Zwoelf gleichzeitige Kandidaten, drei Plaetze, keine Kursdaten, kein
    Primaerschluessel: allein der Zufall der letzten Stufe entscheidet."""
    trades = _trades_zufall()

    def lauf(seed):
        return modul.simuliere_portfolio(trades, 10_000.0, 0.10,
                                         max_concurrent_positions=3,
                                         kursdaten=None, seed=seed)

    a, b = lauf(modul.SEED), lauf(modul.SEED)
    p.pruefe("Abschnitt 4", "derselbe Startwert liefert dasselbe Ergebnis",
             list(a["equity_curve"]["symbol"]) == list(b["equity_curve"]["symbol"]))

    c = lauf(modul.SEED + 1)
    p.pruefe("Abschnitt 4", "ein anderer Startwert liefert ein anderes Ergebnis",
             set(a["equity_curve"]["symbol"]) != set(c["equity_curve"]["symbol"]),
             f"{sorted(a['equity_curve']['symbol'])} == "
             f"{sorted(c['equity_curve']['symbol'])}")

    p.pruefe("Abschnitt 4", "der Startwert steht im Protokoll",
             a["zuteilung"]["seed"] == modul.SEED
             and c["zuteilung"]["seed"] == modul.SEED + 1,
             str((a["zuteilung"]["seed"], c["zuteilung"]["seed"])))
    p.pruefe("Abschnitt 4", "der Startwert steht auch im Protokolltext",
             any(str(modul.SEED) in zeile
                 for zeile in modul.protokollzeilen(a["zuteilung"])))

    # Der Zufall darf nicht an PYTHONHASHSEED haengen: derselbe Aufruf in
    # einem FRISCHEN Prozess muss denselben Fingerabdruck liefern. Pythons
    # eingebautes hash() fuer Zeichenketten taete das nicht.
    skript = (
        "import importlib.util\n"
        "spec = importlib.util.spec_from_file_location('m', %r)\n"
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
        "print(m.zufallsschluessel(m.SEED, ['AAPL', '2024-04-01', '1.5']))"
        % os.path.abspath(modul.__file__))
    laeufe = set()
    for hashseed in ("0", "1", "12345"):
        umgebung = dict(os.environ, PYTHONHASHSEED=hashseed)
        laeufe.add(subprocess.run([sys.executable, "-c", skript], env=umgebung,
                                  capture_output=True, text=True).stdout.strip())
    p.pruefe("Abschnitt 4",
             "der Fingerabdruck haengt nicht an PYTHONHASHSEED (drei Prozesse)",
             len(laeufe) == 1 and "" not in laeufe, str(laeufe))


# ===========================================================================
# Abschnitt 5 - fehlende Angaben: Median statt "ans Ende"
# ===========================================================================
def abschnitt5(modul, p: Protokoll):
    """Vier Kandidaten, drei davon mit Korrelation (-1, ~+0,3, +1), einer ohne
    Vorgeschichte.

    Der Kandidat ohne Wert bekommt den Median der drei anderen (~+0,3) und
    steht damit WEDER vorn NOCH hinten. Genau das sind die beiden verworfenen
    Alternativen, und genau beide werden geprueft:

      * "ans Ende schieben"  -> JUNG waere Letzter.
      * "Korrelation 0 einsetzen" -> JUNG waere Erster (0 ist besser als
        +0,3 und als +1, nur nicht besser als -1 ... deshalb ist der
        Gegenlaeufer hier bewusst mit -1 dabei: er muss trotzdem gewinnen).

    Gemessen wird die RANGFOLGE, nicht der Ablauf einer Simulation: `waehle`
    wird mit unveraendertem Buch wiederholt aufgerufen und der Gewinner jedes
    Mal entfernt. Eine Simulation wuerde nach jeder Vergabe das Buch
    fortschreiben; dann haengt der zweite Rang nicht mehr an der Behandlung
    fehlender Werte, sondern am veraenderten Buch - und der Pruefall saehe
    etwas anderes, als er behauptet.
    """
    r = zufallsrenditen(21)
    kurse = {
        "BUCH": kursreihe(r, volumen=5_000_000.0),
        "GLEICHLAUF": kursreihe(r, startkurs=50.0, volumen=1_000_000.0),
        "MITTE": kursreihe(0.3 * r + 0.95 * zufallsrenditen(23), startkurs=60.0,
                           volumen=1_000_000.0),
        "GEGENLAUF": kursreihe(-r, startkurs=80.0, volumen=1_000_000.0),
        # Nur zehn Tage Vorgeschichte - weniger als MIN_KORRELATIONSTAGE.
        "JUNG": kursreihe(zufallsrenditen(22, 9), startkurs=30.0,
                          volumen=1_000_000.0),
    }
    kurse["JUNG"] = kurse["JUNG"].assign(
        open_time=pd.date_range("2024-03-22", periods=10, freq="D"))

    trades = tabelle([
        {"symbol": "BUCH", "entry_time": "2024-03-01", "exit_time": "2024-05-15",
         "entry_price": 10.0, "exit_price": 11.0, "pnl_pct": 1.0},
        {"symbol": "GLEICHLAUF", "entry_time": "2024-04-01", "exit_time": "2024-04-20",
         "entry_price": 20.0, "exit_price": 21.0, "pnl_pct": 2.0},
        {"symbol": "MITTE", "entry_time": "2024-04-01", "exit_time": "2024-04-23",
         "entry_price": 50.0, "exit_price": 51.0, "pnl_pct": 5.0},
        {"symbol": "GEGENLAUF", "entry_time": "2024-04-01", "exit_time": "2024-04-21",
         "entry_price": 30.0, "exit_price": 31.0, "pnl_pct": 3.0},
        {"symbol": "JUNG", "entry_time": "2024-04-01", "exit_time": "2024-04-22",
         "entry_price": 40.0, "exit_price": 41.0, "pnl_pct": 4.0},
    ])
    zeit = pd.Timestamp("2024-04-01")
    buch = [("BUCH", 1000.0)]

    vorrat = modul.Kursvorrat(kurse)
    ende = vorrat.fensterende(zeit)
    reihe = vorrat.buchreihe(buch, ende)
    p.pruefe("Abschnitt 5", "zu kurze Historie liefert keinen Korrelationswert",
             vorrat.korrelation("JUNG", reihe, ende) is None,
             str(vorrat.korrelation("JUNG", reihe, ende)))
    k_mitte = vorrat.korrelation("MITTE", reihe, ende)
    p.pruefe("Abschnitt 5",
             "der Pruefall ist brauchbar: der mittlere Wert liegt echt dazwischen",
             k_mitte is not None and -1.0 < k_mitte < 1.0, str(k_mitte))

    zuteiler = modul.Zuteiler(trades, kurse, None, modul.SEED)
    offen = [zeile_von(trades, s)
             for s in ("GLEICHLAUF", "MITTE", "GEGENLAUF", "JUNG")]
    erster = trades["symbol"].iloc[zuteiler.waehle(offen, buch, zeit)]
    p.pruefe("Abschnitt 5", "der Kandidat ohne Historie verdraengt den besseren nicht",
             erster == "GEGENLAUF", str(erster))

    # Die Rangregel selbst, mit vorgegebenen Werten statt gerechneten: nur so
    # laesst sich die Stellung des fehlenden Wertes IM FELD beobachten - ein
    # `waehle` gibt nur den Sieger zurueck, und bei einem Feld aus zwei
    # Kandidaten faellt der Median mit dem einen vorhandenen Wert zusammen.
    #
    # Feld: -1,0 / -0,2 / +0,4 / +1,0 -> Median +0,1. Der Kandidat ohne Wert
    # muss damit die schlechtere Haelfte schlagen und der besseren
    # unterliegen. "Ans Ende" verloere den ersten, "0 einsetzen" den zweiten
    # Teil.
    werte = {"a": -1.0, "b": -0.2, "c": 0.4, "d": 1.0, "x": None}
    p.pruefe("Abschnitt 5", "ohne Wert: schlaegt die ueberdurchschnittlich korrelierten",
             modul._beste(["d", "x"], werte, groesser_ist_besser=False) == ["x"],
             str(modul._beste(["d", "x"], werte, groesser_ist_besser=False)))
    p.pruefe("Abschnitt 5", "ohne Wert: unterliegt den unterdurchschnittlich korrelierten",
             modul._beste(["b", "x"], werte, groesser_ist_besser=False) == ["b"],
             str(modul._beste(["b", "x"], werte, groesser_ist_besser=False)))
    p.pruefe("Abschnitt 5", "kennt niemand einen Wert, entfaellt die Stufe ganz",
             modul._beste(["x", "y"], {"x": None, "y": None},
                          groesser_ist_besser=False) == ["x", "y"])


# ===========================================================================
# Abschnitt 6 - Reihenfolge-Invarianz, am Verhalten gemessen
# ===========================================================================
def abschnitt6(modul, p: Protokoll):
    """Dieselben Trades, zwanzig Permutationen der Zeilen- UND der
    Symbolreihenfolge. Verglichen wird die Kapitalkurve als FOLGE (die
    strengste der drei Ebenen aus shared/determinismus.py)."""
    r = zufallsrenditen(31)
    kurse = {}
    zeilen = []
    for i in range(10):
        symbol = f"S{i:02d}"
        # Teils gleichlaeufig, teils gegenlaeufig, unterschiedlich liquide -
        # damit alle Stufen der Kaskade etwas zu tun bekommen.
        eigen = zufallsrenditen(100 + i)
        mischung = r * (0.9 if i % 2 else -0.9) + eigen * 0.4
        kurse[symbol] = kursreihe(mischung, startkurs=10.0 + i,
                                  volumen=1_000_000.0 * (i + 1))
        for k in range(4):
            zeilen.append({
                "symbol": symbol,
                "entry_time": f"2024-04-{5 + 3 * k:02d}",
                "exit_time": f"2024-04-{7 + 3 * k:02d}",
                "entry_price": 10.0 + i, "exit_price": 11.0 + i + k,
                "pnl_pct": round(-3.0 + i + k, 2),
            })
    trades = tabelle(zeilen)

    def fingerabdruck(t, k):
        erg = modul.simuliere_portfolio(t, 10_000.0, 0.10,
                                        max_concurrent_positions=3, kursdaten=k)
        kurve = erg["equity_curve"]
        return (erg["final_capital"], erg["num_executed"], erg["num_skipped"],
                [] if kurve.empty else
                [tuple(z) for z in kurve[["symbol", "pnl_pct",
                                          "capital_after"]].itertuples(
                    index=False, name=None)])

    grund = fingerabdruck(trades, kurse)
    p.pruefe("Abschnitt 6", "der Pruefall ist ueberhaupt knapp (es wird abgelehnt)",
             grund[2] > 0, f"num_skipped={grund[2]}")

    wuerfel = np.random.RandomState(99)
    abweichungen = 0
    for _ in range(20):
        ordnung = wuerfel.permutation(len(trades))
        permutiert = trades.iloc[ordnung].reset_index(drop=True)
        symbolordnung = list(kurse)
        wuerfel.shuffle(symbolordnung)
        if fingerabdruck(permutiert, {s: kurse[s] for s in symbolordnung}) != grund:
            abweichungen += 1
    p.pruefe("Abschnitt 6",
             "20 Permutationen von Zeilen- und Symbolreihenfolge: identischer Kapitalpfad",
             abweichungen == 0, f"{abweichungen} Abweichungen")


# ===========================================================================
# Abschnitt 7 - Gegenprobe: wo nichts knapp wird, aendert sich nichts
# ===========================================================================
def alte_simulation(trades, starting_capital, allocation_pct,
                    max_concurrent_positions=None):
    """Die Fassung VOR TB-26, wortgleich aus `equity_simulation.py`.

    Sie steht hier als UNABHAENGIGER Erwartungswert. Wuerde die Gegenprobe
    gegen einen zweiten Lauf der neuen Fassung geprueft, bestaetigte sie sich
    selbst - genau die Falle, die dieser Test vermeiden soll.
    """
    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx))
        events.append((trade["exit_time"], "exit", idx))
    events.sort(key=lambda e: (e[0], e[1] != "exit"))

    capital = starting_capital
    open_positions = {}
    skipped_trades = []
    executed_trades = []
    equity_curve = []

    for time, event_type, idx in events:
        trade = trades.loc[idx]
        if event_type == "entry":
            if (max_concurrent_positions is not None
                    and len(open_positions) >= max_concurrent_positions):
                skipped_trades.append(idx)
                continue
            bound_capital = sum(open_positions.values())
            free_capital = capital - bound_capital
            allocation = capital * allocation_pct
            if allocation > free_capital:
                skipped_trades.append(idx)
                continue
            open_positions[idx] = allocation
            executed_trades.append(idx)
        elif event_type == "exit":
            if idx not in open_positions:
                continue
            allocation = open_positions.pop(idx)
            pnl_pct = trade["pnl_pct"]
            capital += (allocation * (1 + pnl_pct / 100) - allocation)
            equity_curve.append({
                "time": time, "symbol": trade["symbol"], "pnl_pct": pnl_pct,
                "allocation": round(allocation, 2),
                "capital_after": round(capital, 2)})

    return {"final_capital": round(capital, 2),
            "num_executed": len(executed_trades),
            "num_skipped": len(skipped_trades),
            "equity_curve": pd.DataFrame(equity_curve)}


def abschnitt7(modul, p: Protokoll):
    """Ein Trade-Satz ohne jede Knappheit: kein Limit, kleine Allokation,
    und KEINE zwei Ausstiege auf demselben Zeitstempel.

    Unter diesen Bedingungen darf die neue Fassung Zeile fuer Zeile dasselbe
    liefern wie die alte - das ist die Lage von `elliott_wave` (null
    abgelehnte Trades). Aendert sich hier etwas, greift die Kaskade an einer
    Stelle, an der sie nicht greifen soll.
    """
    zeilen = []
    for i in range(12):
        zeilen.append({
            "symbol": f"S{i:02d}",
            "entry_time": f"2024-04-{2 + i:02d}",
            "exit_time": f"2024-05-{2 + i:02d}",
            "entry_price": 10.0 + i, "exit_price": 11.0 + i,
            "pnl_pct": round(-4.0 + i, 2)})
    trades = tabelle(zeilen)

    alt = alte_simulation(trades, 10_000.0, 0.02, None)
    neu = modul.simuliere_portfolio(trades, 10_000.0, 0.02, None, kursdaten=None)

    p.pruefe("Abschnitt 7", "ohne Knappheit wird nichts abgelehnt",
             alt["num_skipped"] == 0 and neu["num_skipped"] == 0)
    p.pruefe("Abschnitt 7", "Endkapital wie vor TB-26",
             alt["final_capital"] == neu["final_capital"],
             f"{alt['final_capital']} != {neu['final_capital']}")
    p.pruefe("Abschnitt 7", "Zahl der ausgefuehrten Trades wie vor TB-26",
             alt["num_executed"] == neu["num_executed"])
    p.pruefe("Abschnitt 7", "die Kapitalkurve ist Zeile fuer Zeile dieselbe",
             alt["equity_curve"].equals(neu["equity_curve"]),
             "Kurven weichen ab")

    # Gleichzeitige Ausstiege: dieselben Zeilen, moeglicherweise in anderer
    # Folge - die MENGE und das Endkapital muessen gleich bleiben. Genau
    # hierin unterscheiden sich die beiden Fassungen bewusst.
    gleichzeitig = trades.assign(exit_time=pd.Timestamp("2024-06-01"))
    alt2 = alte_simulation(gleichzeitig, 10_000.0, 0.02, None)
    neu2 = modul.simuliere_portfolio(gleichzeitig, 10_000.0, 0.02, None, kursdaten=None)
    p.pruefe("Abschnitt 7", "bei gleichzeitigen Ausstiegen bleibt das Endkapital gleich",
             alt2["final_capital"] == neu2["final_capital"],
             f"{alt2['final_capital']} != {neu2['final_capital']}")
    p.pruefe("Abschnitt 7", "bei gleichzeitigen Ausstiegen bleibt die Zeilenmenge gleich",
             sorted(map(tuple, alt2["equity_curve"][["symbol", "pnl_pct"]].values)) ==
             sorted(map(tuple, neu2["equity_curve"][["symbol", "pnl_pct"]].values)))


# ===========================================================================
# Abschnitt 8 - Mutationsproben: schlaegt der Test ueberhaupt an?
# ===========================================================================
# Je Mutante: die eine Zeile, die ersetzt wird, und die Abschnitte, die
# daraufhin fehlschlagen MUESSEN - nicht mehr und nicht weniger. "Nicht mehr"
# ist der schaerfere Teil: er belegt, dass die Abschnitte voneinander
# unabhaengig sind und nicht einer fuer alle anderen mitbuergt.
MUTANTEN = [
    {
        "name": "stufe2_richtung_verdreht",
        "alt": "            gruppe = _beste(gruppe, werte, groesser_ist_besser=False)\n"
               "            if len(gruppe) == 1:\n"
               "                return self._fertig(gruppe[0], STUFE_DIVERSIFIKATION, begonnen)",
        "neu": "            gruppe = _beste(gruppe, werte, groesser_ist_besser=True)\n"
               "            if len(gruppe) == 1:\n"
               "                return self._fertig(gruppe[0], STUFE_DIVERSIFIKATION, begonnen)",
        # Abschnitt 6 steht bewusst NICHT hier: eine verdrehte Richtung ist
        # falsch, aber weiterhin reihenfolgeunabhaengig. Die Reihenfolge-
        # Invarianz kann diesen Fehler gar nicht sehen - und ein Test, der
        # ihn ihr zuschriebe, behauptete eine Wache, die es nicht gibt.
        "erwartet": {"Abschnitt 2", "Abschnitt 5"},
    },
    {
        "name": "stufe3_richtung_verdreht",
        "alt": "            werte = {i: self._liquiditaet(self._symbol[i], ende) for i in gruppe}\n"
               "            gruppe = _beste(gruppe, werte, groesser_ist_besser=True)",
        "neu": "            werte = {i: self._liquiditaet(self._symbol[i], ende) for i in gruppe}\n"
               "            gruppe = _beste(gruppe, werte, groesser_ist_besser=False)",
        "erwartet": {"Abschnitt 3"},
    },
    {
        "name": "zufall_ohne_startwert",
        "alt": '    roh = "|".join([str(seed)] + [str(f) for f in felder])',
        "neu": '    roh = "|".join([str(f) for f in felder])',
        "erwartet": {"Abschnitt 4"},
    },
    {
        "name": "ausstiege_wieder_in_dateireihenfolge",
        "alt": "        return sorted(positionen, key=lambda p: self._zufall[p])",
        "neu": "        return list(positionen)",
        "erwartet": {"Abschnitt 6"},
    },
    {
        "name": "fehlende_werte_ans_ende",
        "alt": "    gefuellt = {i: (werte[i] if werte[i] is not None else ersatz) for i in gruppe}",
        "neu": "    gefuellt = {i: (werte[i] if werte[i] is not None else\n"
               "                    (float('inf') if not groesser_ist_besser else float('-inf')))\n"
               "               for i in gruppe}",
        "erwartet": {"Abschnitt 5"},
    },
    {
        "name": "keine_kaskade_erster_der_liste",
        "alt": "            gewinner = (rest[0] if not umstritten\n"
               "                        else zuteiler.waehle(rest, _buch(open_positions, symbole), zeit))",
        "neu": "            gewinner = rest[0]",
        # Abschnitt 5 fehlt hier, weil er die Rangregel DIREKT prueft
        # (`waehle`/`_beste`) und nicht ueber die Simulation - diese Mutation
        # sitzt in der Simulation.
        #
        # Abschnitt 4 steht dagegen sehr wohl hier: wird gar nicht mehr
        # zugeteilt, aendert auch ein anderer Startwert nichts mehr. Dass die
        # Zusicherung "anderer Startwert, anderes Ergebnis" diesen Fall
        # mitfaengt, ist kein Zufall, sondern ihr eigentlicher Gehalt.
        "erwartet": {"Abschnitt 1", "Abschnitt 2", "Abschnitt 3", "Abschnitt 4",
                     "Abschnitt 6"},
    },
]

# Welche Abschnitte laufen gegen eine Mutante? Abschnitt 7 ist absichtlich
# dabei, obwohl keine Mutante ihn treffen soll: eine Mutation, die ihn
# umwirft, veraenderte etwas an einer Stelle ohne Knappheit - das waere ein
# Befund und kein Nebenbefund.
MUTANTEN_ABSCHNITTE = [
    ("Abschnitt 1", abschnitt1), ("Abschnitt 2", abschnitt2),
    ("Abschnitt 3", abschnitt3), ("Abschnitt 4", abschnitt4),
    ("Abschnitt 5", abschnitt5), ("Abschnitt 6", abschnitt6),
    ("Abschnitt 7", abschnitt7),
]


def abschnitt8(p: Protokoll, wurzel: str):
    for mutante in MUTANTEN:
        pfad = os.path.join(wurzel, mutante["name"] + ".py")
        shutil.copyfile(ZUTEILUNG_PY, pfad)
        text = open(pfad, encoding="utf-8").read()
        if text.count(mutante["alt"]) != 1:
            p.pruefe("Abschnitt 8",
                     f"{mutante['name']}: Zielstelle genau einmal gefunden", False,
                     f"{text.count(mutante['alt'])} Treffer - der Test hat die "
                     f"Datei nicht mehr verstanden")
            continue
        open(pfad, "w", encoding="utf-8").write(
            text.replace(mutante["alt"], mutante["neu"]))

        modul = lade(pfad, "zuteilung_" + mutante["name"])
        mp = Protokoll(still=True)
        for name, funktion in MUTANTEN_ABSCHNITTE:
            try:
                funktion(modul, mp)
            except Exception as fehler:                      # noqa: BLE001
                mp.pruefe(name, "Abschnitt lief durch", False, repr(fehler))
        p.pruefe("Abschnitt 8",
                 f"{mutante['name']}: genau die erwarteten Abschnitte schlagen an",
                 mp.abschnitte == mutante["erwartet"],
                 f"angeschlagen {sorted(mp.abschnitte)}, "
                 f"erwartet {sorted(mutante['erwartet'])}")


# ===========================================================================
# Abschnitt 9 - die neun Bots benutzen die Kaskade wirklich
# ===========================================================================
BOT_SKRIPT = """
import json, sys
import pandas as pd
import equity_simulation as es
import inspect

trades = pd.DataFrame({
    "symbol": ["AAA", "BBB", "CCC"],
    "entry_time": pd.to_datetime(["2024-04-01"] * 3),
    "exit_time": pd.to_datetime(["2024-04-10", "2024-04-11", "2024-04-12"]),
    "entry_price": [10.0, 20.0, 30.0], "exit_price": [11.0, 21.0, 31.0],
    "pnl_pct": [10.0, 5.0, 1.0]})
if es.SIGNALSPALTE is not None:
    trades[es.SIGNALSPALTE[0]] = [1.0, 2.0, 3.0]

nimmt_limit = "max_concurrent_positions" in inspect.signature(es.simulate_portfolio).parameters
args = [trades, 10_000.0, 0.5] + ([2] if nimmt_limit else [])
erg = es.simulate_portfolio(*args)
print("__BOT__" + json.dumps({
    "signalspalte": list(es.SIGNALSPALTE) if es.SIGNALSPALTE else None,
    "nimmt_limit": nimmt_limit,
    "seed": erg.get("zuteilung", {}).get("seed"),
    "umstritten": erg.get("zuteilung", {}).get("umstrittene_zuteilungen"),
    "ausgefuehrt": erg["num_executed"],
}))
"""


def _fehlendes_modul(stderr: str):
    """Der Name des fehlenden Moduls - oder None, wenn der Abbruch einen
    anderen Grund hatte."""
    for zeile in stderr.splitlines():
        if zeile.startswith("ModuleNotFoundError: No module named "):
            return zeile.split("named ", 1)[1].strip().strip("'\"")
    return None


def abschnitt9(p: Protokoll):
    """Je ein Subprozess - neun gleichnamige `equity_simulation.py` und
    `live_params.py` kollidieren in `sys.modules`, derselbe stille Bug, den
    `shared/portfolio_overview.py` schon einmal gefunden hat."""
    strategien = os.path.join(BASE_DIR, "strategies")
    bots = sorted(n for n in os.listdir(strategien)
                  if os.path.exists(os.path.join(strategien, n,
                                                 "equity_simulation.py")))
    p.pruefe("Abschnitt 9", "neun Bots gefunden", len(bots) == 9, str(len(bots)))

    for bot in bots:
        lauf = subprocess.run([sys.executable, "-c", BOT_SKRIPT],
                              cwd=os.path.join(strategien, bot),
                              capture_output=True, text=True)
        zeile = next((z for z in lauf.stdout.splitlines()
                      if z.startswith("__BOT__")), None)
        if zeile is None:
            fehlt = _fehlendes_modul(lauf.stderr)
            if fehlt:
                # Bot-Abhaengigkeiten, die in dieser Umgebung fehlen
                # (`binance`, `yfinance`, das gitignorete
                # `shared/fetch_binance_data.py`). Das ist eine Eigenschaft
                # der Umgebung und keine der Kaskade - aber es wird genannt,
                # nicht uebergangen.
                p.lasse_aus(f"{bot}: simulate_portfolio", f"Modul {fehlt} fehlt")
                continue
            p.pruefe("Abschnitt 9", f"{bot}: simulate_portfolio lief", False,
                     (lauf.stderr.strip() or lauf.stdout.strip())[-300:])
            continue
        bericht = json.loads(zeile[len("__BOT__"):])
        p.pruefe("Abschnitt 9", f"{bot}: benutzt die Kaskade (Startwert im Protokoll)",
                 bericht["seed"] is not None, str(bericht))
        p.pruefe("Abschnitt 9", f"{bot}: die Knappheit wurde als solche erkannt",
                 bericht["umstritten"] == 2 and bericht["ausgefuehrt"] == 2,
                 str(bericht))
        if bot == "elliott_wave":
            p.pruefe("Abschnitt 9",
                     "elliott_wave kennt weiterhin kein Positionslimit-Argument",
                     not bericht["nimmt_limit"], str(bericht))
        else:
            p.pruefe("Abschnitt 9", f"{bot}: Positionslimit-Argument erhalten",
                     bericht["nimmt_limit"], str(bericht))


# ===========================================================================
def git_zustand() -> str:
    lauf = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR,
                          capture_output=True, text=True)
    return lauf.stdout


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("--schnell", action="store_true",
                          help="ohne Mutationsproben und ohne die neun Bots")
    args = zerleger.parse_args(argv)

    vorher = git_zustand()
    modul = lade(ZUTEILUNG_PY, "zuteilung_unter_test")
    p = Protokoll()

    for name, funktion in [("Abschnitt 1 - Stufe 1: Signalstaerke", abschnitt1),
                           ("Abschnitt 2 - Stufe 2: Diversifikation", abschnitt2),
                           ("Abschnitt 3 - Stufe 3: Liquiditaet", abschnitt3),
                           ("Abschnitt 4 - Stufe 4: seeded Zufall", abschnitt4),
                           ("Abschnitt 5 - fehlende Angaben", abschnitt5),
                           ("Abschnitt 6 - Reihenfolge-Invarianz", abschnitt6),
                           ("Abschnitt 7 - Gegenprobe ohne Knappheit", abschnitt7)]:
        print(f"\n--- {name} ---")
        funktion(modul, p)

    if args.schnell:
        print("\n(Abschnitt 8 und 9 uebersprungen: --schnell)")
    else:
        print("\n--- Abschnitt 8 - Mutationsproben ---")
        with tempfile.TemporaryDirectory() as wurzel:
            abschnitt8(p, wurzel)
        print("\n--- Abschnitt 9 - die neun Bots ---")
        abschnitt9(p)

    print("\n--- der Test selbst ---")
    nachher = git_zustand()
    p.pruefe("Abschnitt 10", "git status unveraendert (der Test schreibt nicht ins Repo)",
             vorher == nachher, f"vorher:\n{vorher}\nnachher:\n{nachher}")

    print("\n" + "=" * 78)
    print(f"Ergebnis: {p.ok} bestanden, {len(p.fehler)} fehlgeschlagen"
          + (f", {len(p.ausgelassen)} ausgelassen" if p.ausgelassen else ""))
    for f in p.fehler:
        print(f"  - {f}")
    for a in p.ausgelassen:
        print(f"  ~ ausgelassen: {a}")
    print("=" * 78)
    return 1 if p.fehler else 0


if __name__ == "__main__":
    sys.exit(main())
