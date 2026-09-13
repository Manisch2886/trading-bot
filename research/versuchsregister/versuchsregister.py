#!/usr/bin/env python3
"""
TB-29 - Versuchsregister: die zaehlbaren Teile mechanisch erheben
==================================================================
Wie viele Parameter-Kombinationen sind in diesem Projekt geprueft worden?
Die Zahl wird gebraucht, sobald nach der Mass-Reparatur neu selektiert
wird: die Deflated Sharpe Ratio korrigiert fuer Selektionsverzerrung und
verlangt als Eingabe genau diese Zahl.

Dieses Programm erhebt die drei Teile, die sich **zaehlen** lassen:

  1. **Rastergroessen** - aus dem Quelltext der 21 Optimierungsstellen
     (9x `multi_symbol_optimise.py`, 9x `multi_symbol_walk_forward.py`,
     3x `optimise_*.py`), mechanisch ueber den AST (`raster.py`).
  2. **Abgelegte Ergebnisdateien** - eine Zeile je tatsaechlich
     gerechneter Kombination. Belastbarer als die Rastergroesse, weil
     dort steht, was gerechnet wurde, nicht was gerechnet werden sollte.
  3. **Forschungsraster** - dieselbe Zeilenzaehlung fuer die Rasterlaeufe
     unter `research/`.

Was es NICHT tut: schaetzen. Wo eine Zahl nicht aus Code oder Datei
folgt, steht `unklar` samt Grund - und im Register eine Luecke. Die
Wertung, was die Zahl bedeutet, steht in `BERICHT.md`, nicht hier.

Aufrufe
-------
    python3 research/versuchsregister/versuchsregister.py
    python3 research/versuchsregister/versuchsregister.py --pruefen
    python3 research/versuchsregister/versuchsregister.py --historie
    python3 research/versuchsregister/versuchsregister.py --dsr 3000

`--pruefen` ist der Waechter: er vergleicht den heutigen Stand gegen
`STAND` weiter unten und gibt **1** zurueck, sobald eine Rastergroesse
oder eine Ergebnisdatei sich geaendert hat, ohne dass das Register
nachgezogen wurde. Ohne Befund **0**.

Laeuft ohne pandas, ohne Kursdaten und ohne Netz. `--historie` braucht
zusaetzlich ein `git`-Arbeitsverzeichnis mit vollstaendiger Historie.
"""

import argparse
import csv
import math
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raster import raster                                   # noqa: E402

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_DIR))
STRATEGIES_DIR = os.path.join(BASE_DIR, "strategies")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
RESEARCH_DIR = os.path.join(BASE_DIR, "research")

BOTS = [
    "elliott_wave",
    "elliott_wave_stocks",
    "rsi2_crypto",
    "rsi2_mean_reversion",
    "t3_supertrend",
    "turtle_soup_crypto",
    "turtle_soup_stocks",
    "volatility_breakout",
    "volatility_breakout_crypto",
]

# Die drei Dateiarten, in denen das Projekt Parameter sucht. Die Liste
# stammt aus research/tb27_kapitalsimulation/BERICHT.md Abschnitt 5
# (9 + 6 + 3 Stellen); die `optimise_*.py` heissen je Bot anders.
RASTERDATEIEN = (
    [(bot, "multi_symbol_optimise.py") for bot in BOTS]
    + [(bot, "multi_symbol_walk_forward.py") for bot in BOTS]
    + [("elliott_wave", "optimise_elliott.py"),
       ("elliott_wave_stocks", "optimise_elliott.py"),
       ("t3_supertrend", "optimise_trend.py")]
)

# Der Krypto-Elliott-Bot legt seine Ergebnisse historisch in der Wurzel
# von results/ ab statt im Unterordner - Relikt aus der Zeit vor
# strategy_paths.py. Dieselbe Aufloesung wie shared/ergebniskurven.py:
# der Standardpfad gewinnt, WENN es ihn gibt, sonst der historische.
HISTORISCHE_PFADE = {
    "elliott_wave": os.path.join(RESULTS_DIR, "multi_symbol_optimisation_results.csv"),
}

# Einzelsymbol-Lauf aus der Zeit vor der Multi-Symbol-Optimierung. Gehoert
# zu elliott_wave, steht aber nicht unter seinem Namen und wird deshalb
# getrennt gefuehrt statt stillschweigend zugeschlagen.
EINZELSYMBOL_DATEI = ("elliott_wave (Einzelsymbol, BTCUSDT)",
                      os.path.join(RESULTS_DIR, "BTCUSDT_optimisation_results.csv"))

# Rasterlaeufe unter research/: eine Zeile je Kombination, ungefiltert.
FORSCHUNGSDATEIEN = [
    ("elliott_wave_params", "elliott_wave_grid_gesamt.csv"),
    ("elliott_wave_params", "elliott_wave_grid_is.csv"),
    ("elliott_wave_params", "elliott_wave_grid_oos.csv"),
    ("elliott_wave_params", "elliott_wave_stocks_grid_gesamt.csv"),
    ("elliott_wave_params", "elliott_wave_stocks_grid_is.csv"),
    ("elliott_wave_params", "elliott_wave_stocks_grid_oos.csv"),
    ("drawdown_reihenfolge", "elliott_wave_raster.csv"),
    ("drawdown_reihenfolge", "elliott_wave_stocks_raster.csv"),
    ("drawdown_reihenfolge", "rsi2_crypto_raster.csv"),
    ("drawdown_reihenfolge", "rsi2_crypto_is_raster.csv"),
    ("drawdown_reihenfolge", "rsi2_mean_reversion_raster.csv"),
    ("drawdown_reihenfolge", "rsi2_mean_reversion_is_raster.csv"),
    ("drawdown_reihenfolge", "t3_supertrend_raster.csv"),
    ("drawdown_reihenfolge", "t3_supertrend_ohne_regimefilter_raster.csv"),
    ("drawdown_reihenfolge", "turtle_soup_crypto_raster.csv"),
    ("drawdown_reihenfolge", "turtle_soup_crypto_is_raster.csv"),
    ("drawdown_reihenfolge", "turtle_soup_stocks_raster.csv"),
    ("drawdown_reihenfolge", "turtle_soup_stocks_is_raster.csv"),
    ("drawdown_reihenfolge", "volatility_breakout_raster.csv"),
    ("drawdown_reihenfolge", "volatility_breakout_is_raster.csv"),
    ("drawdown_reihenfolge", "volatility_breakout_crypto_raster.csv"),
    ("drawdown_reihenfolge", "volatility_breakout_crypto_is_raster.csv"),
]


# ===========================================================================
# STAND - der im Register festgehaltene Zustand vom 13.09.2026
# ===========================================================================
# Der Waechter vergleicht gegen diese Tabelle. Wer ein Raster erweitert
# oder einen Rasterlauf neu ablegt, muss sie hier UND im Register
# nachziehen - sonst schlaegt --pruefen an. Das ist der Zweck.
#
# Vorbild: ERWARTUNG in research/tb27_kapitalsimulation/vergleich.py.
STAND_DATUM = "13.09.2026"

STAND_RASTER = {
    ("elliott_wave", "multi_symbol_optimise.py"): 36,
    ("elliott_wave_stocks", "multi_symbol_optimise.py"): 64,
    ("rsi2_crypto", "multi_symbol_optimise.py"): 18,
    ("rsi2_mean_reversion", "multi_symbol_optimise.py"): 6,
    ("t3_supertrend", "multi_symbol_optimise.py"): 81,
    ("turtle_soup_crypto", "multi_symbol_optimise.py"): 12,
    ("turtle_soup_stocks", "multi_symbol_optimise.py"): 12,
    ("volatility_breakout", "multi_symbol_optimise.py"): 4,
    ("volatility_breakout_crypto", "multi_symbol_optimise.py"): 4,
    ("elliott_wave", "multi_symbol_walk_forward.py"): 37,
    ("elliott_wave_stocks", "multi_symbol_walk_forward.py"): 65,
    ("rsi2_crypto", "multi_symbol_walk_forward.py"): 19,
    ("rsi2_mean_reversion", "multi_symbol_walk_forward.py"): 7,
    ("t3_supertrend", "multi_symbol_walk_forward.py"): 82,
    ("turtle_soup_crypto", "multi_symbol_walk_forward.py"): 13,
    ("turtle_soup_stocks", "multi_symbol_walk_forward.py"): 13,
    ("volatility_breakout", "multi_symbol_walk_forward.py"): 5,
    ("volatility_breakout_crypto", "multi_symbol_walk_forward.py"): 5,
    ("elliott_wave", "optimise_elliott.py"): 36,
    ("elliott_wave_stocks", "optimise_elliott.py"): 36,
    ("t3_supertrend", "optimise_trend.py"): 81,
}

STAND_ERGEBNISZEILEN = {
    "elliott_wave": 36,
    "elliott_wave_stocks": 64,
    "rsi2_crypto": 6,
    "rsi2_mean_reversion": 6,
    "t3_supertrend": 23,
    "turtle_soup_crypto": 8,
    "turtle_soup_stocks": 12,
    "volatility_breakout": 4,
    "volatility_breakout_crypto": 4,
    EINZELSYMBOL_DATEI[0]: 30,
}

STAND_FORSCHUNGSZEILEN = {
    ("elliott_wave_params", "elliott_wave_grid_gesamt.csv"): 252,
    ("elliott_wave_params", "elliott_wave_grid_is.csv"): 252,
    ("elliott_wave_params", "elliott_wave_grid_oos.csv"): 252,
    ("elliott_wave_params", "elliott_wave_stocks_grid_gesamt.csv"): 252,
    ("elliott_wave_params", "elliott_wave_stocks_grid_is.csv"): 252,
    ("elliott_wave_params", "elliott_wave_stocks_grid_oos.csv"): 252,
    ("drawdown_reihenfolge", "elliott_wave_raster.csv"): 36,
    ("drawdown_reihenfolge", "elliott_wave_stocks_raster.csv"): 64,
    ("drawdown_reihenfolge", "rsi2_crypto_raster.csv"): 18,
    ("drawdown_reihenfolge", "rsi2_crypto_is_raster.csv"): 18,
    ("drawdown_reihenfolge", "rsi2_mean_reversion_raster.csv"): 6,
    ("drawdown_reihenfolge", "rsi2_mean_reversion_is_raster.csv"): 6,
    ("drawdown_reihenfolge", "t3_supertrend_raster.csv"): 81,
    ("drawdown_reihenfolge", "t3_supertrend_ohne_regimefilter_raster.csv"): 81,
    ("drawdown_reihenfolge", "turtle_soup_crypto_raster.csv"): 12,
    ("drawdown_reihenfolge", "turtle_soup_crypto_is_raster.csv"): 12,
    ("drawdown_reihenfolge", "turtle_soup_stocks_raster.csv"): 12,
    ("drawdown_reihenfolge", "turtle_soup_stocks_is_raster.csv"): 12,
    ("drawdown_reihenfolge", "volatility_breakout_raster.csv"): 4,
    ("drawdown_reihenfolge", "volatility_breakout_is_raster.csv"): 4,
    ("drawdown_reihenfolge", "volatility_breakout_crypto_raster.csv"): 4,
    ("drawdown_reihenfolge", "volatility_breakout_crypto_is_raster.csv"): 4,
}

# Befundarten des Waechters. Jede Abweichung bekommt genau eine - damit
# ein Test auf GENAU die Zusicherung pruefen kann, die er meint, und
# nicht versehentlich von einer zweiten Wache mitgetragen wird.
RASTER_GEAENDERT = "RASTER GEAENDERT"
RASTER_UNKLAR = "RASTER UNKLAR"
RASTER_FEHLT = "RASTERSTELLE FEHLT"
RASTER_NEU = "RASTERSTELLE NEU"
ZEILEN_GEAENDERT = "ZEILEN GEAENDERT"
ZEILEN_FEHLT = "ERGEBNISDATEI FEHLT"
ZEILEN_NEU = "ERGEBNISDATEI NEU"


class Befund:
    def __init__(self, art, gegenstand, text):
        self.art = art
        self.gegenstand = gegenstand
        self.text = text

    def __str__(self):
        return f"{self.art:<20} {self.gegenstand}: {self.text}"


# ===========================================================================
# Erhebung
# ===========================================================================
def zaehle_zeilen(pfad):
    """Datenzeilen einer CSV - ohne pandas, tolerant gegen Zeilenumbrueche
    in Feldern. Rueckgabe None, wenn es die Datei nicht gibt."""
    if not os.path.exists(pfad):
        return None
    with open(pfad, newline="", encoding="utf-8") as fh:
        leser = csv.reader(fh)
        try:
            next(leser)               # Kopfzeile
        except StopIteration:
            return 0
        return sum(1 for zeile in leser if zeile)


def ergebnisdatei(bot, wurzel=None):
    """Pfad der abgelegten Optimierungsergebnisse eines Bots."""
    wurzel = wurzel or RESULTS_DIR
    standard = os.path.join(wurzel, bot, "multi_symbol_optimisation_results.csv")
    if os.path.exists(standard):
        return standard
    if bot in HISTORISCHE_PFADE:
        return os.path.join(wurzel, os.path.basename(HISTORISCHE_PFADE[bot]))
    return standard


def erhebe_raster(wurzel=None):
    """(bot, datei) -> (kombinationen | None, grund | None)."""
    wurzel = wurzel or STRATEGIES_DIR
    erhoben = {}
    for bot, datei in RASTERDATEIEN:
        pfad = os.path.join(wurzel, bot, datei)
        if not os.path.exists(pfad):
            erhoben[(bot, datei)] = (None, "Datei nicht vorhanden")
            continue
        erhoben[(bot, datei)] = raster(pfad)
    return erhoben


def erhebe_ergebniszeilen(wurzel=None):
    """Bot -> Zeilenzahl der abgelegten Optimierungsergebnisse."""
    wurzel = wurzel or RESULTS_DIR
    erhoben = {bot: zaehle_zeilen(ergebnisdatei(bot, wurzel)) for bot in BOTS}
    erhoben[EINZELSYMBOL_DATEI[0]] = zaehle_zeilen(
        os.path.join(wurzel, os.path.basename(EINZELSYMBOL_DATEI[1])))
    return erhoben


def erhebe_forschungszeilen(wurzel=None):
    """(ordner, datei) -> Zeilenzahl der Rasterlaeufe unter research/."""
    wurzel = wurzel or RESEARCH_DIR
    return {(ordner, datei): zaehle_zeilen(
                os.path.join(wurzel, ordner, "results", datei))
            for ordner, datei in FORSCHUNGSDATEIEN}


# ===========================================================================
# Ausgabe
# ===========================================================================
def _zahl(wert):
    return "unklar" if wert is None else f"{wert}"


def uebersicht():
    raster_ist = erhebe_raster()
    zeilen_ist = erhebe_ergebniszeilen()
    forschung_ist = erhebe_forschungszeilen()

    print("=" * 78)
    print("1. RASTERGROESSEN AUS DEM QUELLTEXT (Kombinationen je vollstaendigem Lauf)")
    print("=" * 78)
    print(f"{'Bot':<28}{'Datei':<32}{'Komb.':>8}")
    for bot, datei in RASTERDATEIEN:
        wert, grund = raster_ist[(bot, datei)]
        print(f"{bot:<28}{datei:<32}{_zahl(wert):>8}"
              + (f"   ({grund})" if wert is None else ""))
    summe = sum(w for w, _ in raster_ist.values() if w is not None)
    unklar = sum(1 for w, _ in raster_ist.values() if w is None)
    print(f"{'SUMME':<60}{summe:>8}"
          + (f"   ({unklar} Stellen unklar)" if unklar else ""))

    print()
    print("=" * 78)
    print("2. ABGELEGTE ERGEBNISDATEIEN (eine Zeile je gerechneter Kombination)")
    print("=" * 78)
    print(f"{'Bot':<40}{'Raster':>8}{'Zeilen':>8}{'Differenz':>11}")
    for bot in BOTS:
        wert, _ = raster_ist[(bot, "multi_symbol_optimise.py")]
        zeilen = zeilen_ist[bot]
        diff = ("-" if wert is None or zeilen is None
                else ("0" if zeilen == wert else f"{zeilen - wert:+d}"))
        print(f"{bot:<40}{_zahl(wert):>8}{_zahl(zeilen):>8}{diff:>11}")
    name, _pfad = EINZELSYMBOL_DATEI
    print(f"{name:<40}{'36':>8}{_zahl(zeilen_ist[name]):>8}"
          f"{zeilen_ist[name] - 36:+11d}")
    print()
    print("  Eine Differenz ist kein Fehler, sondern ein Befund: die Bots legen nur")
    print("  Kombinationen ab, die MIN_TRADES / MIN_SYMBOLS_CONTRIBUTING /")
    print("  MIN_AVG_RETURN_PCT bestehen. Gerechnet wurde die Rastergroesse,")
    print("  abgelegt die gefilterte Teilmenge.")

    print()
    print("=" * 78)
    print("3. RASTERLAEUFE UNTER research/ (ungefiltert abgelegt)")
    print("=" * 78)
    print(f"{'Ordner':<26}{'Datei':<46}{'Zeilen':>6}")
    for ordner, datei in FORSCHUNGSDATEIEN:
        print(f"{ordner:<26}{datei:<46}{_zahl(forschung_ist[(ordner, datei)]):>6}")
    summe_f = sum(v for v in forschung_ist.values() if v is not None)
    print(f"{'SUMME':<72}{summe_f:>6}")

    print()
    print("=" * 78)
    print("Das Register mit den Summen je Bot steht in REGISTER.md, die Einordnung")
    print("in BERICHT.md. Beide Zahlen sind UNTERGRENZEN - was nicht abgelegt und")
    print("nicht im Code steht, kann dieses Programm nicht sehen.")
    return 0


# ===========================================================================
# Waechter
# ===========================================================================
def pruefen(strategien=None, ergebnisse=None, forschung=None):
    """Heutigen Stand gegen STAND vergleichen. Rueckgabewert 1 bei Befund.

    Die drei Wurzeln sind nur fuer die Tests da: so kann eine Probe GENAU
    eine der drei Wachen ansprechen und die anderen beiden nachweislich
    ruhig lassen. Waeren sie fest verdrahtet, koennte eine zweite Wache
    das Fehlen der ersten verdecken - und der Test merkte es nicht.
    """
    befunde = []

    raster_ist = erhebe_raster(strategien)
    for schluessel in sorted(set(raster_ist) | set(STAND_RASTER)):
        bot, datei = schluessel
        gegenstand = f"{bot}/{datei}"
        soll = STAND_RASTER.get(schluessel)
        eintrag = raster_ist.get(schluessel)
        if eintrag is None:
            befunde.append(Befund(RASTER_FEHLT, gegenstand,
                                  f"steht mit {soll} im Register, wird nicht mehr gefunden"))
            continue
        ist, grund = eintrag
        if soll is None:
            befunde.append(Befund(RASTER_NEU, gegenstand,
                                  f"{_zahl(ist)} Kombinationen, steht nicht im Register"))
        elif ist is None:
            befunde.append(Befund(RASTER_UNKLAR, gegenstand,
                                  f"Register {soll}, heute nicht zaehlbar - {grund}"))
        elif ist != soll:
            befunde.append(Befund(RASTER_GEAENDERT, gegenstand,
                                  f"Register {soll}, heute {ist} ({ist - soll:+d})"))

    zeilen_ist = erhebe_ergebniszeilen(ergebnisse)
    for name in sorted(set(zeilen_ist) | set(STAND_ERGEBNISZEILEN)):
        soll = STAND_ERGEBNISZEILEN.get(name)
        ist = zeilen_ist.get(name)
        if ist is None:
            befunde.append(Befund(ZEILEN_FEHLT, name,
                                  f"Register {soll} Zeilen, Datei nicht vorhanden"))
        elif soll is None:
            befunde.append(Befund(ZEILEN_NEU, name,
                                  f"{ist} Zeilen, steht nicht im Register"))
        elif ist != soll:
            befunde.append(Befund(ZEILEN_GEAENDERT, name,
                                  f"Register {soll} Zeilen, heute {ist} ({ist - soll:+d})"))

    forschung_ist = erhebe_forschungszeilen(forschung)
    for schluessel in sorted(set(forschung_ist) | set(STAND_FORSCHUNGSZEILEN)):
        gegenstand = "research/%s/results/%s" % schluessel
        soll = STAND_FORSCHUNGSZEILEN.get(schluessel)
        ist = forschung_ist.get(schluessel)
        if ist is None:
            befunde.append(Befund(ZEILEN_FEHLT, gegenstand,
                                  f"Register {soll} Zeilen, Datei nicht vorhanden"))
        elif soll is None:
            befunde.append(Befund(ZEILEN_NEU, gegenstand,
                                  f"{ist} Zeilen, steht nicht im Register"))
        elif ist != soll:
            befunde.append(Befund(ZEILEN_GEAENDERT, gegenstand,
                                  f"Register {soll} Zeilen, heute {ist} ({ist - soll:+d})"))

    if befunde:
        print(f"ABWEICHUNG gegenueber dem Register (Stand {STAND_DATUM}):\n")
        for b in befunde:
            print("  " + str(b))
        print("\nEntweder ist ein Versuchsblock dazugekommen, der noch nicht im")
        print("Register steht - dann gehoert er hinein -, oder eine Zahl ist")
        print("unbeabsichtigt gewandert. Beides ist zu klaeren, bevor die")
        print("Gesamtsumme weiterverwendet wird: eine Untergrenze, die leise")
        print("nicht mehr stimmt, ist schlechter als gar keine.")
        return 1

    geprueft = len(STAND_RASTER) + len(STAND_ERGEBNISZEILEN) + len(STAND_FORSCHUNGSZEILEN)
    print(f"UNVERAENDERT gegenueber dem Register (Stand {STAND_DATUM}). "
          f"{geprueft} Angaben geprueft:")
    print(f"  {len(STAND_RASTER)} Rastergroessen, "
          f"{len(STAND_ERGEBNISZEILEN)} Ergebnisdateien, "
          f"{len(STAND_FORSCHUNGSZEILEN)} Rasterlaeufe unter research/.")
    return 0


def pruefe_befunde(strategien=None, ergebnisse=None, forschung=None):
    """Wie `pruefen`, gibt aber die Befundliste zurueck - fuer die Tests."""
    ausgabe = []
    import io
    from contextlib import redirect_stdout
    puffer = io.StringIO()
    with redirect_stdout(puffer):
        code = pruefen(strategien, ergebnisse, forschung)
    for zeile in puffer.getvalue().splitlines():
        for art in (RASTER_GEAENDERT, RASTER_UNKLAR, RASTER_FEHLT, RASTER_NEU,
                    ZEILEN_GEAENDERT, ZEILEN_FEHLT, ZEILEN_NEU):
            if zeile.strip().startswith(art):
                ausgabe.append((art, zeile.strip()))
                break
    return code, ausgabe, puffer.getvalue()


# ===========================================================================
# Historie - wie oft wurde ein Raster geaendert?
# ===========================================================================
def historie():
    """Rastergroesse je Commit. Zeigt, wie viele RUNDEN es gab.

    Ausgewertet wird nicht der Diff, sondern die gezaehlte Groesse: eine
    verschobene Rastergrenze bei gleicher Groesse (4 Werte bleiben 4
    Werte) faellt hier bewusst NICHT als Rasteraenderung auf, sondern in
    der Spalte `Grenzen`. Wer das Raster verschiebt, weil das Ergebnis
    nicht gefiel, hat ebenfalls selektiert - das steht im Register.
    """
    if subprocess.call(["git", "rev-parse", "--git-dir"], cwd=BASE_DIR,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        print("Kein git-Arbeitsverzeichnis - --historie nicht moeglich.")
        return 1
    flach = subprocess.run(["git", "rev-parse", "--is-shallow-repository"],
                           cwd=BASE_DIR, capture_output=True, text=True).stdout.strip()
    if flach == "true":
        print("WARNUNG: flacher Klon (shallow). Die Historie ist abgeschnitten,")
        print("         die Rundenzahl waere zu niedrig. `git fetch --unshallow`")
        print("         ausfuehren und erneut starten.")
        return 1

    gesamt_runden = 0
    for bot, datei in RASTERDATEIEN:
        pfad = os.path.join("strategies", bot, datei)
        roh = subprocess.run(
            ["git", "log", "--follow", "--reverse", "--format=%h\t%ad\t%s",
             "--date=short", "--", pfad],
            cwd=BASE_DIR, capture_output=True, text=True).stdout.strip()
        if not roh:
            continue
        verlauf = []
        for zeile in roh.splitlines():
            kurz, datum, betreff = zeile.split("\t", 2)
            wert = _raster_bei_commit(kurz, bot, datei)
            verlauf.append((kurz, datum, wert, betreff))
        aenderungen = sum(1 for i in range(1, len(verlauf))
                          if verlauf[i][2] != verlauf[i - 1][2])
        gesamt_runden += aenderungen
        print(f"\n{bot}/{datei}   Commits: {len(verlauf)}   "
              f"Rasteraenderungen: {aenderungen}")
        for i, (kurz, datum, wert, betreff) in enumerate(verlauf):
            marke = "*" if i == 0 or wert != verlauf[i - 1][2] else " "
            print(f"  {marke} {kurz}  {datum}  {_zahl(wert):>6}  {betreff[:52]}")

    print(f"\nUeber alle {len(RASTERDATEIEN)} Stellen: {gesamt_runden} "
          f"Rasteraenderungen in der Git-Historie.")
    aeltester = subprocess.run(["git", "log", "--reverse", "--format=%ad", "--date=short"],
                               cwd=BASE_DIR, capture_output=True,
                               text=True).stdout.splitlines()
    if aeltester:
        print(f"Aeltester Commit des Repos: {aeltester[0]}. Alles, was davor "
              f"probiert wurde,\nist hier nicht sichtbar - siehe REGISTER.md, "
              f"Abschnitt 'Was fehlt'.")
    return 0


def _raster_bei_commit(commit, bot, datei):
    """Rastergroesse eines Bots zu einem Commit.

    Der ganze Strategieordner wird ausgecheckt, nicht nur die eine Datei:
    `multi_symbol_walk_forward.py` holt seine Raster per Import aus dem
    Nachbarmodul. Wer nur die Einzeldatei auspackt, bekommt fuer sechs
    von neun Bots `unklar` - und haelt das womoeglich fuer einen Befund.
    """
    with tempfile.TemporaryDirectory() as ordner:
        archiv = subprocess.run(
            ["git", "archive", commit, f"strategies/{bot}"],
            cwd=BASE_DIR, capture_output=True)
        if archiv.returncode != 0:
            return None
        entpacken = subprocess.run(["tar", "-x", "-C", ordner],
                                   input=archiv.stdout, capture_output=True)
        if entpacken.returncode != 0:
            return None
        pfad = os.path.join(ordner, "strategies", bot, datei)
        if not os.path.exists(pfad):
            return None
        wert, _grund = raster(pfad)
        return wert


# ===========================================================================
# Einordnung - was bedeutet N fuer die Deflated Sharpe Ratio?
# ===========================================================================
def dsr(n_werte, beobachtungen=None, perioden_pro_jahr=252):
    """Erwartetes Maximum reinen Rauschens bei N unabhaengigen Versuchen.

    Bei N Versuchen mit reinem Rauschen liegt das erwartete Maximum der
    standardisierten Kennzahl bei etwa

        E[max] ~ sqrt(2 * ln N)       Standardabweichungen

    (fuehrender Term der Extremwertnaeherung; Bailey/Lopez de Prado nutzen
    ihn als Kern der Deflated Sharpe Ratio). Die Umrechnung in einen Sharpe
    haengt an der Laenge der Reihe: der Schaetzfehler des Sharpe aus T
    Beobachtungen ist etwa 1/sqrt(T), die Rauschschwelle also

        sqrt(2 ln N) / sqrt(T)        je Periode
        sqrt(2 ln N) / sqrt(T) * sqrt(P)   auf ein Jahr hochgerechnet

    mit P Perioden je Jahr (Tagesdaten: 252). Die Jahres-Spalte ist die,
    die mit veroeffentlichten Sharpe-Zahlen vergleichbar ist.

    **Nur ausgerechnet, nicht bewertet.** Ob daraus etwas folgt, entscheidet
    der Nutzer.
    """
    beobachtungen = beobachtungen or [252, 1260]
    print("Erwartetes Maximum reinen Rauschens bei N Versuchen")
    print("  E[max] = sqrt(2 * ln N) Standardabweichungen;")
    print(f"  Sharpe-Schwelle = E[max] / sqrt(T) * sqrt({perioden_pro_jahr}) "
          f"(auf ein Jahr hochgerechnet)\n")
    print(f"{'N':>10}{'sqrt(2 ln N)':>16}", end="")
    for t in beobachtungen:
        print(f"{'T=' + str(t):>14}", end="")
    print()
    for n in n_werte:
        if n < 2:
            print(f"{n:>10}{'-':>16}")
            continue
        wert = math.sqrt(2.0 * math.log(n))
        print(f"{n:>10}{wert:>16.3f}", end="")
        for t in beobachtungen:
            print(f"{wert / math.sqrt(t) * math.sqrt(perioden_pro_jahr):>14.2f}", end="")
        print()
    print("\nLesehilfe: eine Strategie, die nach N Versuchen als beste aus dem")
    print("Raster faellt, muesste einen Jahres-Sharpe OBERHALB der Schwelle")
    print("zeigen, um sich von der besten reinen Zufallsziehung desselben")
    print("Rasters zu unterscheiden. Die Naeherung setzt unabhaengige Versuche")
    print("voraus; benachbarte Rasterpunkte sind es nicht - die Schwelle ist")
    print("damit eher zu hoch als zu niedrig angesetzt.")
    return 0


# ===========================================================================
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    p.add_argument("--pruefen", action="store_true",
                   help="Waechter-Betrieb, Rueckgabewert 1 bei Abweichung")
    p.add_argument("--historie", action="store_true",
                   help="Rastergroesse je Commit - wie viele Runden gab es?")
    p.add_argument("--dsr", nargs="*", type=int, metavar="N",
                   help="sqrt(2 ln N) fuer diese Versuchszahlen ausrechnen")
    p.add_argument("--beobachtungen", nargs="*", type=int, default=[252, 1260],
                   metavar="T", help="Reihenlaengen fuer die Sharpe-Umrechnung")
    p.add_argument("--perioden-pro-jahr", type=int, default=252, metavar="P",
                   help="Perioden je Jahr fuer die Hochrechnung (Vorgabe 252)")
    args = p.parse_args(argv)

    if args.pruefen:
        return pruefen()
    if args.historie:
        return historie()
    if args.dsr is not None:
        return dsr(args.dsr or [653, 2798], args.beobachtungen,
                   args.perioden_pro_jahr)
    return uebersicht()


if __name__ == "__main__":
    sys.exit(main())
