"""
Selbsttests: Rangfolge der Wellenauswahl (TB-20)
==============================================================================
Geprueft wird das VERHALTEN von

    strategies/elliott_wave/elliott_wave_counter.py
    strategies/elliott_wave_stocks/elliott_wave_counter.py
        -> nach_rangfolge()      die Rangfolge selbst
        -> remove_overlapping()  Ueberlappungs-Durchlauf + Rueckgabe-Rangfolge
        -> find_impulse_waves()  Erkennung + Rangfolge
        -> find_causal_waves()   speist Backtest, Optimierung, Kapitalkurven

nicht das Vorhandensein von `kind="stable"` oder von `RANGFOLGE` im Quelltext.
Eine Textsuche waere hier besonders wertlos: sie prueft genau das, was der Diff
ohnehin zeigt, und sagt nichts darueber, ob die Zusicherung traegt.


WORUM ES GEHT
------------------------------------------------------------------------------
`fib_score` ist eine Summe aus drei festen Teilpunkten (0.34/0.33/0.33), auf
zwei Stellen gerundet. Er kann nur SECHS Werte annehmen, davon FUENF oberhalb
von `min_fib_score=0.3`. Gleichstaende sind damit der Regelfall, nicht die
Ausnahme - gemessen 87 % (Krypto) bzw. 99 % (Aktien) aller erkannten Muster.

Vorher entschied bei Gleichstand die Sortierimplementierung, welches Muster
oben steht. Jetzt entscheidet eine benannte Rangfolge:

    fib_score absteigend, dann end_time absteigend (das JUENGERE Muster),
    dann start_time absteigend (bei gleichem Ende das KUERZERE).

Begruendung siehe Kommentarblock in `elliott_wave_counter.py`.


DIE VIER TRENNBAREN ZUSICHERUNGEN
------------------------------------------------------------------------------
In `nach_rangfolge` stecken vier Wachen in einer Zeile. Die Abschnitte sind so
gewaehlt, dass je nur EINE greifen kann (Falle 2, s. u.):

  Z1  es wird ueberhaupt nach `fib_score` sortiert       -> Abschnitt 2
  Z2  Gleichstand im fib_score: `end_time` entscheidet   -> Abschnitt 1
  Z3  Gleichstand auch im end_time: `start_time`         -> Abschnitt 3
  Z4  Gleichstand im GANZEN Schluessel: Eingabereihenfolge -> Abschnitt 4

Dazu im Ueberlappungs-Durchlauf von `remove_overlapping`:

  Z5  der Durchlauf ist chronologisch                    -> Abschnitt 5a
  Z6  er ist stabil (doppelter start_time)               -> Abschnitt 5b


DIE BEIDEN WIEDERKEHRENDEN FALLEN
------------------------------------------------------------------------------
**Falle 1 - die selbstbestaetigende Probe.** Nirgends stellt der Test den
Zustand her, den er anschliessend wiedererkennt. Kein Erwartungswert stammt
aus einem Lauf der geprueften Funktion; jeder folgt aus der Konstruktion der
Eingabe und der oben genannten Regel. Und dass die Proben ueberhaupt
unterscheiden, wird nicht vorausgesetzt, sondern am ABLAUF nachgewiesen:
Abschnitt 9 laesst jeden Abschnitt zusaetzlich gegen MUTIERTE Kopien der
echten Dateien laufen, in denen je genau eine Wache entfernt ist. Schlaegt
eine Mutante nicht fehl, ist der Test selbst durchgefallen - nicht bestanden.

**Falle 2 - die zweite Wache verdeckt das Fehlen der ersten.** Deshalb die
Trennung oben. Sie wird nicht als Absicht behauptet, sondern in Abschnitt 9
gemessen: je Mutante wird festgehalten, welche Abschnitte anschlagen, und
genau die erwarteten muessen es sein - nicht mehr und nicht weniger.

Zwei Punkte, die diese Trennung ehrlich halten:

  * Abschnitt 4 (Gleichstand im ganzen Schluessel) BESTEHT weiterhin, wenn man
    die Sortierung ersatzlos entfernt - ohne Sortierung bleibt die
    Eingabereihenfolge trivial erhalten. Abschnitt 4 sagt also nichts darueber,
    ob sortiert wird. Genau das haelt die Mutante "Sortierung ersatzlos
    entfernt" fest: sie muss 1, 2 und 3 fehlschlagen lassen und 4 NICHT.
  * Umgekehrt sagen die Abschnitte 1 bis 3 nichts ueber die Stabilitaet: ihre
    Schluessel sind eindeutig, stabil und unstabil sind dort gleichwertig.

**Und ein drittes, unbequemes Ergebnis dieser Buchhaltung:** `kind="stable"`
in `nach_rangfolge` traegt heute nichts. pandas wertet `kind` bei einer
MEHRSPALTIGEN `sort_values` nicht aus - dieser Pfad laeuft ueber `lexsort`
und ist ohnehin stabil. Abschnitt 9 haelt das fest, statt es zu verschweigen:
die Mutante "nur kind=quicksort" darf KEINEN Abschnitt zum Anschlagen
bringen. Was Abschnitt 4 tatsaechlich bewacht, ist der Rueckschritt auf einen
EINSPALTIGEN Schluessel (Mutante "wie main") - dort wird `kind` wirksam.


WARUM DIE ABSCHNITTE 1 BIS 4 `nach_rangfolge` DIREKT AUFRUFEN
------------------------------------------------------------------------------
Weil nur so je eine Wache isoliert werden kann. Abschnitt 1 braucht Muster,
deren `start_time` GEGEN ihre `end_time` laeuft - sonst wuerde die Probe auch
ohne `end_time` im Schluessel bestehen, und sie wuerde Z2 nicht pruefen.
Solche Muster ueberlappen sich zwangslaeufig, `remove_overlapping` wuerde
sie also vorher zusammenstreichen.

`nach_rangfolge` ist keine Hilfskonstruktion des Tests, sondern die Stelle, an
der die Regel genau einmal steht; `find_impulse_waves` und
`remove_overlapping` rufen ausschliesslich sie auf. Dass die
Eingabe-DataFrames dieser Abschnitte dieselbe Gestalt haben wie das, was
`find_impulse_waves` wirklich liefert, prueft Abschnitt 8 an echten Daten.
Die echten Einstiegspunkte laufen in den Abschnitten 5 bis 8.


WAS DIESER TEST NICHT VERAENDERT
------------------------------------------------------------------------------
Die geprueften Dateien werden als BIBLIOTHEK eingebunden, ihr
`__main__`-Block laeuft nie - insbesondere wird keine
`*_impulse_waves.csv` neu geschrieben. Mutationen entstehen ausschliesslich in
Kopien unter einem temporaeren Ordner AUSSERHALB des Repos - `mutiere()`
sagt, warum "irgendwo im Repo" hier nicht genuegt. Abschnitt 11 weist per
`git status` UND per Ordnerliste nach, dass im Repo nichts entstanden oder
veraendert ist; git allein meldet einen leeren Ordner nicht.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:
    python3 shared/test_wellenauswahl.py
    python3 shared/test_wellenauswahl.py --schnell   # ohne Abschnitt 8b/10
"""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)

# Die beiden geprueften Dateien. `rangfolge_zeile` und `durchlauf_zeile` sind
# NICHT die Zusicherung - sie sind der Angriffspunkt der Mutationen in
# Abschnitt 9.
RANGFOLGE_ZEILE = ('    return waves.sort_values(RANGFOLGE, ascending=RANGFOLGE_AUFSTEIGEND,\n'
                   '                             kind="stable").reset_index(drop=True)')
DURCHLAUF_ZEILE = '    sorted_df = impulses.sort_values("start_time", kind="stable").reset_index(drop=True)'

ZIELE = {
    "elliott_wave": {
        "pfad": os.path.join(BASE_DIR, "strategies", "elliott_wave",
                             "elliott_wave_counter.py"),
        "deviation_pct": 10.0,      # live_params.py dieses Bots
        "freshness_bars": 48,       # backtest_elliott.SIGNAL_FRESHNESS_BARS
        "endung": "1h",
        "symbolliste": os.path.join(BASE_DIR, "config", "top25_symbols.txt"),
    },
    "elliott_wave_stocks": {
        "pfad": os.path.join(BASE_DIR, "strategies", "elliott_wave_stocks",
                             "elliott_wave_counter.py"),
        "deviation_pct": 5.0,
        "freshness_bars": 5,
        "endung": "1d",
        "symbolliste": os.path.join(BASE_DIR, "config", "sp500_top150.txt"),
    },
}

# Mutationen: je Schluessel der Ersatz fuer die jeweilige Zeile.
MUTATIONEN = {
    # Der Stand von `main`: eine nackte, unstabile fib_score-Sortierung.
    "wie_main": (RANGFOLGE_ZEILE,
                 '    return waves.sort_values("fib_score", ascending=False).reset_index(drop=True)'),
    "ohne_end_time": ('RANGFOLGE = ["fib_score", "end_time", "start_time"]\n'
                      'RANGFOLGE_AUFSTEIGEND = [False, False, False]',
                      'RANGFOLGE = ["fib_score", "start_time"]\n'
                      'RANGFOLGE_AUFSTEIGEND = [False, False]'),
    "ohne_start_time": ('RANGFOLGE = ["fib_score", "end_time", "start_time"]\n'
                        'RANGFOLGE_AUFSTEIGEND = [False, False, False]',
                        'RANGFOLGE = ["fib_score", "end_time"]\n'
                        'RANGFOLGE_AUFSTEIGEND = [False, False]'),
    "ohne_fib_score": ('RANGFOLGE = ["fib_score", "end_time", "start_time"]\n'
                       'RANGFOLGE_AUFSTEIGEND = [False, False, False]',
                       'RANGFOLGE = ["end_time", "start_time"]\n'
                       'RANGFOLGE_AUFSTEIGEND = [False, False]'),
    # Nur `kind` verbogen, Schluessel unveraendert. Das MUSS folgenlos sein -
    # pandas wertet `kind` auf dem mehrspaltigen Pfad nicht aus. Die Mutante
    # steht hier nicht als Wache, sondern als Messung genau dieser Tatsache.
    "kind_quicksort": (RANGFOLGE_ZEILE,
                       '    return waves.sort_values(RANGFOLGE, ascending=RANGFOLGE_AUFSTEIGEND,\n'
                       '                             kind="quicksort").reset_index(drop=True)'),
    # Nur EINE Spalte, aber stabil. Reproduzierbar - und trotzdem unbegruendet:
    # die Rangfolge bei Gleichstand ist dann die zufaellige Eingabereihenfolge.
    "nur_fib_score_stabil": ('RANGFOLGE = ["fib_score", "end_time", "start_time"]\n'
                             'RANGFOLGE_AUFSTEIGEND = [False, False, False]',
                             'RANGFOLGE = ["fib_score"]\n'
                             'RANGFOLGE_AUFSTEIGEND = [False]'),
    "ohne_sortierung": (RANGFOLGE_ZEILE,
                        '    return waves.reset_index(drop=True)'),
    "durchlauf_umgekehrt": (DURCHLAUF_ZEILE,
                            '    sorted_df = impulses.sort_values("start_time", ascending=False, '
                            'kind="stable").reset_index(drop=True)'),
    "durchlauf_ohne_stable": (DURCHLAUF_ZEILE,
                              '    sorted_df = impulses.sort_values("start_time").reset_index(drop=True)'),
}

# Je Mutante die Abschnitte, die anschlagen MUESSEN - genau diese.
ERWARTETE_BEFUNDE = (
    ("wie main (einspaltig und unstabil)", "wie_main",
     {"Abschnitt 1", "Abschnitt 3", "Abschnitt 4"}),
    ("nur fib_score, aber stabil", "nur_fib_score_stabil",
     {"Abschnitt 1", "Abschnitt 3"}),
    ("end_time nicht im Schluessel", "ohne_end_time", {"Abschnitt 1"}),
    ("start_time nicht im Schluessel", "ohne_start_time", {"Abschnitt 3"}),
    ("fib_score nicht im Schluessel", "ohne_fib_score", {"Abschnitt 2"}),
    ("Rangfolge ersatzlos entfernt", "ohne_sortierung",
     {"Abschnitt 1", "Abschnitt 2", "Abschnitt 3"}),
    # Erwartung LEER, und das ist der Befund: `kind` traegt auf dem
    # mehrspaltigen Pfad nichts. Schlaegt hier je ein Abschnitt an, hat pandas
    # sein Verhalten geaendert - dann ist der Kommentar im Quelltext zu
    # berichtigen, nicht dieser Test.
    ("nur kind=quicksort (muss folgenlos sein)", "kind_quicksort", set()),
    ("Durchlauf ruecklaeufig", "durchlauf_umgekehrt", {"Abschnitt 5a"}),
    ("Durchlauf ohne stabile Sortierung", "durchlauf_ohne_stable", {"Abschnitt 5b"}),
)


class Protokoll:
    """Sammelt Pruefungen, statt beim ersten Fehler abzubrechen - ein
    einzelner Fehlschlag soll nicht verbergen, was die uebrigen Abschnitte
    gesagt haetten."""

    def __init__(self, still: bool = False):
        self.ok = 0
        self.fehler = []
        self.abschnitte = set()
        self.still = still

    def pruefe(self, abschnitt: str, text: str, bedingung: bool, zusatz: str = ""):
        if bedingung:
            self.ok += 1
            if not self.still:
                print(f"  OK    {text}")
        else:
            self.fehler.append(f"{abschnitt}: {text}{(' - ' + zusatz) if zusatz else ''}")
            self.abschnitte.add(abschnitt)
            if not self.still:
                print(f"  FEHLT {text}" + (f"  [{zusatz}]" if zusatz else ""))


# ===========================================================================
# Module laden - Original wie Mutante ueber denselben Weg
# ===========================================================================
def lade(pfad: str, name: str):
    """Laedt die Datei als Modul. `strategies/<bot>/` kommt VORUEBERGEHEND in
    den Suchpfad, weil `elliott_wave_counter.py` `strategy_paths` aus
    `shared/` importiert - der `__main__`-Block laeuft dabei nicht."""
    ordner = os.path.dirname(os.path.abspath(pfad))
    sys.path.insert(0, _SHARED)
    sys.path.insert(0, ordner)
    try:
        spec = importlib.util.spec_from_file_location(name, pfad)
        modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modul)
        return modul
    finally:
        sys.path.remove(ordner)
        sys.path.remove(_SHARED)


def mutiere(pfad: str, alt: str, neu: str, wurzel: str, name: str):
    """Kopiert die echte Datei in den temporaeren Ordner und ersetzt dort -
    und nur dort - genau eine Stelle. Gibt None zurueck, wenn die Stelle
    nicht genau einmal vorkommt: dann hat der Test die Datei nicht mehr
    verstanden, und das ist ein Befund, kein stilles Ueberspringen.

    Die Kopie liegt AUSSERHALB des Repos, und zwar bewusst in einem
    nachgebauten `<wurzel>/strategies/<name>/`. Grund: die Datei ruft beim
    Import `get_strategy_paths(__file__)` auf, und diese Funktion LEGT Ordner
    an - `<zwei Ebenen ueber der Datei>/results/<Ordnername>` und dasselbe
    fuer `logs`. Lag die Kopie im Strategie-Ordner, entstanden dadurch
    `strategies/results/` und `strategies/logs/` IM REPO. Genau das ist beim
    Bau dieses Tests passiert; `git status` sah es nicht, weil git leere
    Ordner nicht kennt. Aufgefallen ist es erst
    `research/trend_overlay/test_corrected_curves.py`, das die Bot-Ordner
    auszaehlt. Abschnitt 11 prueft seitdem auch die Ordnerliste."""
    nachbau = os.path.join(wurzel, "strategies", name)
    os.makedirs(nachbau, exist_ok=True)
    kopie = os.path.join(nachbau, name + ".py")
    shutil.copyfile(pfad, kopie)
    text = open(kopie, encoding="utf-8").read()
    if text.count(alt) != 1:
        return None
    open(kopie, "w", encoding="utf-8").write(text.replace(alt, neu))
    return lade(kopie, name)


# ===========================================================================
# Die Faelle. Jeder Fall liefert Eingabezeilen; die erwartete Reihenfolge
# folgt aus der KONSTRUKTION, nicht aus einem Lauf.
# ===========================================================================
T0 = pd.Timestamp("2024-01-01")


def _muster(marke, start_tage, end_tage, fib_score):
    """Eine Zeile in der Gestalt, die find_impulse_waves liefert."""
    return {
        "marke": marke,
        "start_time": np.datetime64(T0 + pd.Timedelta(days=start_tage)),
        "end_time": np.datetime64(T0 + pd.Timedelta(days=end_tage)),
        "direction": "bearish",
        "wave0": 100.0, "wave1": 90.0, "wave2": 94.0,
        "wave3": 80.0, "wave4": 84.0, "wave5": 78.0,
        "fib_score": fib_score,
    }


def fall_gleichstand_fib(anzahl: int):
    """Abschnitt 1 (Z2): alle Muster tragen DENSELBEN fib_score.

    `end_time` waechst mit dem Index, `start_time` FAELLT mit dem Index. Das
    ist der Kern der Probe: waere `end_time` nicht im Schluessel und nur
    `start_time`, laege die Reihenfolge genau umgekehrt. Die Probe kann
    deshalb nicht bestehen, wenn Z2 fehlt.

    Erwartet: end_time absteigend, also der letzte Eintrag zuerst."""
    zeilen = [_muster(f"M{k}", start_tage=100 - k, end_tage=200 + k, fib_score=0.33)
              for k in range(anzahl)]
    erwartet = [f"M{k}" for k in range(anzahl - 1, -1, -1)]
    return zeilen, erwartet


def fall_verschiedene_fib(anzahl: int):
    """Abschnitt 2 (Z1): verschiedene fib_scores, und `end_time` laeuft
    ABSICHTLICH dagegen - das best bewertete Muster ist das AELTESTE.

    Erwartet: fib_score absteigend. Ohne `fib_score` im Schluessel wuerde
    `end_time` entscheiden und die Reihenfolge waere genau umgekehrt.
    Gleichstaende gibt es hier keine; stabil und unstabil sind gleichwertig,
    dieser Abschnitt sagt also nichts ueber Z4."""
    werte = [1.0, 0.67, 0.66, 0.34, 0.33]
    zeilen = [_muster(f"S{k}", start_tage=10 + k, end_tage=100 + k,
                      fib_score=werte[k % len(werte)])
              for k in range(anzahl)]
    zeilen = zeilen[:len(werte)]
    erwartet = [f"S{k}" for k in range(len(zeilen))]
    return zeilen, erwartet


def fall_gleichstand_fib_und_ende(anzahl: int):
    """Abschnitt 3 (Z3): fib_score UND end_time gleich, `start_time`
    verschieden.

    Erwartet: start_time absteigend - bei gleichem Ende das KUERZERE Muster
    zuerst. Das ist die Probe darauf, dass die fachliche Regel bei
    Gleichstand IM ENTSCHEIDUNGSKRITERIUM nicht willkuerlich wird."""
    zeilen = [_muster(f"E{k}", start_tage=50 + k, end_tage=300, fib_score=0.33)
              for k in range(anzahl)]
    erwartet = [f"E{k}" for k in range(anzahl - 1, -1, -1)]
    return zeilen, erwartet


def fall_gleichstand_ueberall(anzahl: int, fremdzeilen: int = 12):
    """Abschnitt 4 (Z4): fib_score, end_time UND start_time gleich - der
    GANZE Schluessel ist ein Gleichstand. Unterscheidbar sind die Zeilen nur
    noch an einer Spalte, die nicht sortiert wird.

    Erwartet: die Eingabereihenfolge der Gruppe bleibt. Das ist die ehrlich
    willkuerliche Rueckfallebene, und sie ist als solche benannt: keine
    fachliche Regel kann hier noch etwas entscheiden.

    Die `fremdzeilen` tragen einen HOEHEREN fib_score. Sie koennen die
    Reihenfolge innerhalb der Gruppe inhaltlich nicht beruehren - sie stehen
    alle davor. Sie veraendern aber Laenge und Inhalt des zu sortierenden
    Feldes, und genau daran haengt die Vertauschung von Gleichstaenden unter
    Quicksort: auf einem KONSTANTEN Feld vertauscht auch Quicksort nichts
    (nachgemessen), die Probe waere ohne sie blind.

    Innerhalb eines Symbols ist dieser Fall unerreichbar (start_time und
    end_time sind dort eindeutig - Abschnitt 8 misst das). Er ist erreichbar,
    sobald Muster mehrerer Symbole gemeinsam sortiert werden."""
    zeilen = [_muster(f"G{k}", start_tage=70, end_tage=400, fib_score=0.33)
              for k in range(anzahl)]
    for k in range(fremdzeilen):
        zeilen.append(_muster(f"F{k}", start_tage=10 + k, end_tage=100 + k,
                              fib_score=1.0 if k % 2 else 0.67))
    erwartet = [f"G{k}" for k in range(anzahl)]
    return zeilen, erwartet


# Wie viele Zeilen im Spiel sind, darf inhaltlich nichts aendern. Die Spanne
# ist bewusst breit: numpy wechselt unterhalb einer Feldlaenge von 16 auf
# Insertion Sort (die zufaellig stabil ist), darueber auf Introsort. Eine
# schmale Spanne koennte an dieser Schwelle vorbeilaufen.
LAENGEN = (2, 3, 5, 9, 17, 33, 40)

# Eingabereihenfolgen, die alle dasselbe Ergebnis liefern muessen.
def _reihenfolgen(n: int):
    rng = np.random.default_rng(20260913 + n)
    yield "wie gebaut", list(range(n))
    yield "umgekehrt", list(range(n - 1, -1, -1))
    if n > 2:
        yield "rotiert", list(range(1, n)) + [0]
    for i in range(3):
        yield f"gemischt {i}", list(rng.permutation(n))


def _sortiere(modul, zeilen: list) -> list:
    df = pd.DataFrame(zeilen)
    return list(modul.nach_rangfolge(df)["marke"])


# ===========================================================================
# Abschnitt 1 - der Kernfall: Gleichstand im fib_score
# ===========================================================================
def abschnitt1(modul, p, praefix=""):
    for n in LAENGEN:
        zeilen, erwartet = fall_gleichstand_fib(n)
        ergebnisse = {}
        for name, folge in _reihenfolgen(n):
            ergebnisse[name] = _sortiere(modul, [zeilen[i] for i in folge])
        einheitlich = len({tuple(v) for v in ergebnisse.values()}) == 1
        richtig = all(v == erwartet for v in ergebnisse.values())
        abweichend = {k: v for k, v in ergebnisse.items() if v != erwartet}
        p.pruefe("Abschnitt 1",
                 f"{praefix}{n} Muster mit gleichem fib_score: juengstes zuerst, "
                 f"unabhaengig von der Eingabereihenfolge",
                 einheitlich and richtig,
                 "" if (einheitlich and richtig) else f"erwartet {erwartet}, erhalten {abweichend}")


# ===========================================================================
# Abschnitt 2 - es wird ueberhaupt nach fib_score sortiert
# ===========================================================================
def abschnitt2(modul, p, praefix=""):
    for n in LAENGEN:
        zeilen, erwartet = fall_verschiedene_fib(n)
        ergebnisse = {}
        for name, folge in _reihenfolgen(len(zeilen)):
            ergebnisse[name] = _sortiere(modul, [zeilen[i] for i in folge])
        richtig = all(v == erwartet for v in ergebnisse.values())
        abweichend = {k: v for k, v in ergebnisse.items() if v != erwartet}
        p.pruefe("Abschnitt 2",
                 f"{praefix}verschiedene fib_scores (end_time laeuft dagegen, "
                 f"Feldlaenge {n}): bester zuerst",
                 richtig, "" if richtig else f"erwartet {erwartet}, erhalten {abweichend}")


# ===========================================================================
# Abschnitt 3 - Gleichstand auch im end_time
# ===========================================================================
def abschnitt3(modul, p, praefix=""):
    for n in LAENGEN:
        zeilen, erwartet = fall_gleichstand_fib_und_ende(n)
        ergebnisse = {}
        for name, folge in _reihenfolgen(n):
            ergebnisse[name] = _sortiere(modul, [zeilen[i] for i in folge])
        richtig = all(v == erwartet for v in ergebnisse.values())
        abweichend = {k: v for k, v in ergebnisse.items() if v != erwartet}
        p.pruefe("Abschnitt 3",
                 f"{praefix}{n} Muster mit gleichem fib_score UND gleichem "
                 f"end_time: kuerzestes zuerst",
                 richtig, "" if richtig else f"erwartet {erwartet}, erhalten {abweichend}")


# ===========================================================================
# Abschnitt 4 - Gleichstand im ganzen Schluessel
# ===========================================================================
def abschnitt4(modul, p, praefix=""):
    for n in LAENGEN:
        for fremd in (0, 3, 12):
            zeilen, erwartet = fall_gleichstand_ueberall(n, fremd)
            erhalten = [m for m in _sortiere(modul, zeilen) if m.startswith("G")]
            p.pruefe("Abschnitt 4",
                     f"{praefix}{n} Muster mit Gleichstand im GANZEN Schluessel "
                     f"({fremd} Fremdzeilen): Eingabereihenfolge bleibt",
                     erhalten == erwartet,
                     "" if erhalten == erwartet else f"erhalten {erhalten}")


# ===========================================================================
# Abschnitt 5 - der Ueberlappungs-Durchlauf in remove_overlapping
# ===========================================================================
def fall_kette(glieder: int, fib_score: float = 0.33):
    """Eine Kette: jedes Muster ueberlappt nur seinen direkten Nachbarn, alle
    tragen denselben fib_score.

    Der Durchlauf ist gierig und behaelt bei Gleichstand den bereits
    aufgenommenen Kandidaten (`>`, nicht `>=`). Chronologisch durchlaufen
    bleibt deshalb JEDES ZWEITE Glied stehen, beginnend beim fruehesten.
    Ruecklaeufig durchlaufen bleibt jedes zweite vom SPAETESTEN aus - bei
    einer geraden Gliederzahl eine andere Menge."""
    zeilen = [_muster(f"K{k}", start_tage=10 * k, end_tage=10 * k + 13,
                      fib_score=fib_score)
              for k in range(glieder)]
    erwartet = {f"K{k}" for k in range(0, glieder, 2)}
    return zeilen, erwartet


def abschnitt5a(modul, p, praefix=""):
    """Z5: der Durchlauf ist chronologisch. Alle start_time sind verschieden -
    stabil und unstabil sind hier gleichwertig, dieser Abschnitt sagt also
    nichts ueber Z6."""
    for glieder in (4, 6, 8, 10, 18, 34):
        zeilen, erwartet = fall_kette(glieder)
        for name, folge in _reihenfolgen(glieder):
            df = pd.DataFrame([zeilen[i] for i in folge])
            erhalten = set(modul.remove_overlapping(df)["marke"])
            p.pruefe("Abschnitt 5a",
                     f"{praefix}Kette aus {glieder} Gliedern ({name}): "
                     f"chronologisch gieriger Durchlauf behaelt {sorted(erwartet)}",
                     erhalten == erwartet,
                     "" if erhalten == erwartet else f"erhalten {sorted(erhalten)}")


def fall_doppelter_start(dubletten: int, davor: int, danach: int):
    """Z6: mehrere Muster mit IDENTISCHEM start_time. Sie ueberlappen sich
    damit zwangslaeufig alle (gleicher Beginn, echte Dauer) und tragen
    denselben fib_score - es bleibt genau eines stehen, und zwar das in der
    DURCHLAUFREIHENFOLGE erste.

    `davor` und `danach` sind voneinander und von der Gruppe unabhaengige
    Muster. Sie koennen inhaltlich nicht mitentscheiden, veraendern aber
    Laenge und Lage des zu sortierenden Feldes - und genau daran haengt die
    Vertauschung der Gleichstaende unter Quicksort."""
    zeilen = []
    for k in range(davor):
        zeilen.append(_muster(f"V{k}", start_tage=1 + 3 * k, end_tage=3 + 3 * k,
                              fib_score=0.33))
    for k in range(dubletten):
        zeilen.append(_muster(f"D{k}", start_tage=500, end_tage=520 + k,
                              fib_score=0.33))
    for k in range(danach):
        zeilen.append(_muster(f"N{k}", start_tage=1000 + 3 * k,
                              end_tage=1002 + 3 * k, fib_score=0.33))
    return zeilen, "D0"


def abschnitt5b(modul, p, praefix=""):
    """Z6: doppelter start_time. Der fib_score ist ueberall gleich und
    end_time entscheidet hier nichts (die Gruppe wird zusammengestrichen,
    bevor die Rangfolge greift) - es haengt allein an der Stabilitaet des
    Durchlaufs."""
    for dubletten in (3, 5, 9, 17, 33):
        ueberlebende = set()
        for davor in (0, 2, 5, 7):
            for danach in (0, 2, 5, 7):
                zeilen, erwartet = fall_doppelter_start(dubletten, davor, danach)
                df = pd.DataFrame(zeilen)
                behalten = [m for m in modul.remove_overlapping(df)["marke"]
                            if m.startswith("D")]
                ueberlebende.add(tuple(behalten))
        p.pruefe("Abschnitt 5b",
                 f"{praefix}{dubletten} Muster mit gleichem start_time: es bleibt "
                 f"das in der Eingabe erste ('D0'), unabhaengig von Fremdzeilen",
                 ueberlebende == {("D0",)},
                 "" if ueberlebende == {("D0",)} else f"erhalten {sorted(ueberlebende)}")


# ===========================================================================
# Abschnitt 6 - Gegenprobe: ohne Gleichstand aendert sich nichts
# ===========================================================================
def abschnitt6(modul, wie_main, p):
    """Die Gegenprobe vergleicht nicht gegen eine hingeschriebene Reihenfolge,
    sondern gegen den LAUF der Fassung von `main`: dieselbe Eingabe, einmal
    durch die heutige Datei, einmal durch die nackte fib_score-Sortierung.
    Ohne Gleichstand im fib_score muessen beide dasselbe liefern - die
    Umstellung darf dort nichts bewegen."""
    for n in LAENGEN:
        zeilen, _ = fall_verschiedene_fib(n)
        for name, folge in _reihenfolgen(len(zeilen)):
            eingabe = [zeilen[i] for i in folge]
            a = _sortiere(modul, eingabe)
            b = _sortiere(wie_main, eingabe)
            p.pruefe("Abschnitt 6",
                     f"ohne Gleichstand ({len(zeilen)} Muster, {name}): heute und "
                     f"main liefern dieselbe Reihenfolge",
                     a == b, "" if a == b else f"heute {a}, main {b}")


# ===========================================================================
# Abschnitt 7 - Wiederholbarkeit
# ===========================================================================
def abschnitt7(modul, p):
    """Derselbe Lauf zweimal muss dasselbe liefern - und zwar bei JEDER
    Eingabereihenfolge dieselbe Ausgabe. Das ist die Zusicherung, die
    `kind="stable"` allein nicht gibt: sie haelt nur die zufaellige
    Eingabereihenfolge fest, eine benannte Rangfolge macht die Ausgabe davon
    unabhaengig."""
    for bauer in (fall_gleichstand_fib, fall_gleichstand_fib_und_ende,
                  fall_verschiedene_fib):
        for n in LAENGEN:
            zeilen, _ = bauer(n)
            ausgaben = set()
            for _name, folge in _reihenfolgen(len(zeilen)):
                eingabe = [zeilen[i] for i in folge]
                ausgaben.add(tuple(_sortiere(modul, eingabe)))
                ausgaben.add(tuple(_sortiere(modul, eingabe)))   # zweiter Lauf
            p.pruefe("Abschnitt 7",
                     f"{bauer.__name__} ({len(zeilen)} Muster): alle Eingabe"
                     f"reihenfolgen und zwei Laeufe liefern genau eine Ausgabe",
                     len(ausgaben) == 1, f"erhalten {len(ausgaben)} verschiedene")


# ===========================================================================
# Abschnitt 8 - echte Daten
# ===========================================================================
def _symbole(ziel: dict, anzahl: int) -> list:
    if not os.path.exists(ziel["symbolliste"]):
        return []
    ausschluss = {"XAUTUSDT", "PAXGUSDT"}
    raus = []
    for zeile in open(ziel["symbolliste"]):
        s = zeile.strip()
        if not s or s in ausschluss:
            continue
        pfad = os.path.join(BASE_DIR, "data", f"{s}_{ziel['endung']}.csv")
        if os.path.exists(pfad):
            raus.append((s, pfad))
        if len(raus) >= anzahl:
            break
    return raus


def abschnitt8(modul, wie_main, ziel: dict, name: str, anzahl: int, p):
    """An echten Kursdaten, ueber die ECHTEN Einstiegspunkte:

    a) Gleichstaende kommen wirklich vor - die Abschnitte 1, 3 und 4 sind
       keine Laborfaelle.
    b) `start_time` und `end_time` sind je Symbol eindeutig. Das ist die
       Messung, auf die sich die Begruendung im Quelltext beruft (Abschnitt 4
       ist innerhalb eines Symbols unerreichbar).
    c) Die MENGE der Muster nach `remove_overlapping` ist dieselbe wie auf
       `main`. Die Umstellung sortiert um, sie streicht nichts anders.
    d) `find_causal_waves` liefert Zeile fuer Zeile dasselbe wie auf `main`.
       Das ist die Funktion, die Backtest, Optimierung und Kapitalkurven
       speist - hier haengt daran, dass sich kein Trade verschiebt.
    """
    ordner = os.path.dirname(ziel["pfad"])
    sys.path.insert(0, _SHARED)
    sys.path.insert(0, ordner)
    try:
        zz = lade(os.path.join(ordner, "zigzag_indicator.py"), f"zz_{name}")
    finally:
        sys.path.remove(ordner)
        sys.path.remove(_SHARED)

    symbole = _symbole(ziel, anzahl)
    p.pruefe("Abschnitt 8", f"{name}: Kursdaten fuer {anzahl} Symbole vorhanden",
             len(symbole) == anzahl, f"gefunden: {len(symbole)}")

    mit_gleichstand = eindeutig = menge_gleich = causal_gleich = 0
    geprueft = trades = 0
    for sym, pfad in symbole:
        df = pd.read_csv(pfad, parse_dates=["open_time"])
        zigzag = zz.calculate_zigzag(df, deviation_pct=ziel["deviation_pct"])
        if len(zigzag) < 6:
            continue
        kandidaten = modul.find_impulse_waves(zigzag, min_fib_score=0.3)
        if kandidaten.empty:
            continue
        geprueft += 1

        anzahlen = kandidaten["fib_score"].value_counts()
        mit_gleichstand += bool((anzahlen > 1).any())
        eindeutig += not (kandidaten["start_time"].duplicated().any()
                          or kandidaten["end_time"].duplicated().any())

        schluessel = ["start_time", "end_time"]
        heute = modul.remove_overlapping(kandidaten)
        alt_kandidaten = wie_main.find_impulse_waves(zigzag, min_fib_score=0.3)
        alt = wie_main.remove_overlapping(alt_kandidaten)
        menge_gleich += (set(map(tuple, heute[schluessel].values))
                         == set(map(tuple, alt[schluessel].values)))

        zc = zz.calculate_zigzag_with_confirmation(df, deviation_pct=ziel["deviation_pct"])
        a = modul.find_causal_waves(zc, 0.3, freshness_bars=ziel["freshness_bars"],
                                    direction="bearish")
        b = wie_main.find_causal_waves(zc, 0.3, freshness_bars=ziel["freshness_bars"],
                                       direction="bearish")
        trades += len(a)
        causal_gleich += a.reset_index(drop=True).equals(b.reset_index(drop=True))

    p.pruefe("Abschnitt 8", f"{name}: Symbole mit Kandidaten", geprueft > 0,
             f"geprueft: {geprueft}")
    p.pruefe("Abschnitt 8",
             f"{name}: jedes Symbol hat Gleichstaende im fib_score "
             f"(der geprueften Fall kommt in echten Daten vor)",
             mit_gleichstand == geprueft, f"{mit_gleichstand} von {geprueft}")
    p.pruefe("Abschnitt 8",
             f"{name}: start_time und end_time je Symbol eindeutig",
             eindeutig == geprueft, f"{eindeutig} von {geprueft}")
    p.pruefe("Abschnitt 8",
             f"{name}: MENGE nach remove_overlapping wie auf main",
             menge_gleich == geprueft, f"{menge_gleich} von {geprueft}")
    p.pruefe("Abschnitt 8",
             f"{name}: find_causal_waves Zeile fuer Zeile wie auf main "
             f"({trades} Trades)",
             causal_gleich == geprueft, f"{causal_gleich} von {geprueft}")


# ===========================================================================
# Abschnitt 9 - Mutationsproben
# ===========================================================================
def abschnitt9(ziel: dict, name: str, wurzel: str, p):
    for titel, schluessel, erwartete_abschnitte in ERWARTETE_BEFUNDE:
        alt, neu = MUTATIONEN[schluessel]
        mutant = mutiere(ziel["pfad"], alt, neu, wurzel, f"mutante_{name}_{schluessel}")
        if mutant is None:
            p.pruefe("Abschnitt 9", f"Mutante '{titel}' liess sich erzeugen", False,
                     "Stelle nicht genau einmal gefunden")
            continue

        mp = Protokoll(still=True)
        try:
            abschnitt1(mutant, mp)
            abschnitt2(mutant, mp)
            abschnitt3(mutant, mp)
            abschnitt4(mutant, mp)
            abschnitt5a(mutant, mp)
            abschnitt5b(mutant, mp)
        except Exception as fehler:
            # Eine Mutante, die abstuerzt statt falsch zu rechnen, beweist
            # nichts ueber die geprueften Wachen - sie ist ein Fehler im Test.
            p.pruefe("Abschnitt 9", f"{name}, Mutante '{titel}': laeuft durch",
                     False, f"{type(fehler).__name__}: {fehler}")
            continue
        p.pruefe("Abschnitt 9",
                 f"{name}, Mutante '{titel}': genau "
                 f"{sorted(erwartete_abschnitte)} schlaegt an",
                 mp.abschnitte == erwartete_abschnitte,
                 f"angeschlagen: {sorted(mp.abschnitte) or 'nichts'}")


# ===========================================================================
# Abschnitt 10 - die abgelegten Kurven bleiben unberuehrt
# ===========================================================================
def abschnitt10(p):
    lauf = subprocess.run([sys.executable, os.path.join(BASE_DIR, "shared", "ergebniskurven.py")],
                          cwd=BASE_DIR, capture_output=True, text=True)
    treffer = "Zusammenfassung: 9x AKTUELL" in lauf.stdout
    letzte = (lauf.stdout.strip().splitlines() or [lauf.stderr[-200:]])[-1]
    p.pruefe("Abschnitt 10", "shared/ergebniskurven.py meldet '9x AKTUELL'",
             treffer and lauf.returncode == 0, "" if treffer else str(letzte))


# ===========================================================================
# Abschnitt 11 - der Test selbst veraendert nichts
# ===========================================================================
BEOBACHTET = ("strategies/", "results/", "data/", "shared/", "logs/", "paper_trading_")


def ordner_zustand() -> str:
    """`git status` allein genuegt hier NICHT: git kennt keine leeren Ordner.
    Beim Bau dieses Tests sind so unbemerkt `strategies/results/` und
    `strategies/logs/` entstanden - angelegt von `get_strategy_paths` beim
    Import einer Mutantenkopie, die im Strategie-Ordner lag. Deshalb wird hier
    die Ordnerliste selbst festgehalten, nicht nur der git-Zustand."""
    zeilen = []
    for wurzel in ("strategies", "results", "shared", "logs"):
        pfad = os.path.join(BASE_DIR, wurzel)
        if not os.path.isdir(pfad):
            continue
        for eintrag in sorted(os.listdir(pfad)):
            if os.path.isdir(os.path.join(pfad, eintrag)) and eintrag != "__pycache__":
                zeilen.append(wurzel + "/" + eintrag)
    return "\n".join(zeilen)


def git_zustand() -> str:
    lauf = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR,
                          capture_output=True, text=True)
    return "\n".join(sorted(z for z in lauf.stdout.splitlines()
                            if z[3:].strip('"').startswith(BEOBACHTET)))


# ===========================================================================
def main() -> int:
    schnell = "--schnell" in sys.argv
    vorher = git_zustand()
    vorher_ordner = ordner_zustand()
    p = Protokoll()

    for name, ziel in ZIELE.items():
        print(f"\n--- {os.path.relpath(ziel['pfad'], BASE_DIR)} ---")
        ordner = os.path.dirname(ziel["pfad"])
        wurzel = tempfile.mkdtemp(prefix="tb20_")
        try:
            modul = lade(ziel["pfad"], f"geprueft_{name}")
            abschnitt1(modul, p)
            abschnitt2(modul, p)
            abschnitt3(modul, p)
            abschnitt4(modul, p)
            abschnitt5a(modul, p)
            abschnitt5b(modul, p)

            alt, neu = MUTATIONEN["wie_main"]
            wie_main = mutiere(ziel["pfad"], alt, neu, wurzel, f"wie_main_{name}")
            if wie_main is None:
                p.pruefe("Abschnitt 6", "Vergleichsfassung 'wie main' erzeugt", False,
                         "Sortierzeile nicht genau einmal gefunden")
            else:
                abschnitt6(modul, wie_main, p)
                print("\n  --- echte Daten ---")
                abschnitt8(modul, wie_main, ziel, name, 4 if schnell else 12, p)

            abschnitt7(modul, p)
            print("\n  --- Mutationsproben ---")
            abschnitt9(ziel, name, wurzel, p)
        finally:
            shutil.rmtree(wurzel, ignore_errors=True)

    if not schnell:
        print("\n--- abgelegte Ergebniskurven ---")
        abschnitt10(p)
    else:
        print("\n  (Abschnitt 10 uebersprungen, Abschnitt 8 verkuerzt: --schnell)")

    print("\n--- der Test selbst ---")
    nachher = git_zustand()
    p.pruefe("Abschnitt 11", "git status unveraendert (der Test schreibt nicht ins Repo)",
             vorher == nachher, f"vorher:\n{vorher}\nnachher:\n{nachher}")
    nachher_ordner = ordner_zustand()
    neu = sorted(set(nachher_ordner.splitlines()) - set(vorher_ordner.splitlines()))
    weg = sorted(set(vorher_ordner.splitlines()) - set(nachher_ordner.splitlines()))
    p.pruefe("Abschnitt 11", "Ordnerliste unveraendert (git meldet leere Ordner nicht)",
             vorher_ordner == nachher_ordner, f"neu: {neu}, verschwunden: {weg}")

    print("\n" + "=" * 78)
    print(f"Ergebnis: {p.ok} bestanden, {len(p.fehler)} fehlgeschlagen")
    for f in p.fehler:
        print(f"  - {f}")
    print("=" * 78)
    return 1 if p.fehler else 0


if __name__ == "__main__":
    sys.exit(main())
