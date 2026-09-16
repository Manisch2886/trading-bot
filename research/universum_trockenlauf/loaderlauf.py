#!/usr/bin/env python3
"""
Kindprozess des Universum-Trockenlaufs - fuehrt EINEN Bot-Loader aus
==============================================================================
Dieses Programm wird nicht von Hand aufgerufen, sondern von
`universum_trockenlauf.py` je Bot einmal als eigener Prozess gestartet.

WARUM EIN EIGENER PROZESS - UND WARUM DAS DER BEFUND IST
------------------------------------------------------------------------------
Die Aufgabe verlangt: "Der Laufcode entscheidet. Die Antwort kommt aus dem
Loader des Bots, nicht aus einer Nachbildung." Und sie verlangt zugleich:
"Bot-Dateien werden gelesen, nie importiert."

Beides zusammen geht nicht. `load_all_symbol_data()` ist eine **Funktion in
einem Modul**; sie laesst sich nur ausfuehren, wenn dieses Modul geladen wird.
Wer sie nachbaut, hat die dritte Implementierung derselben Frage - genau das,
wogegen die Festlegung gerichtet ist.

**Das ist der gemeldete Befund**, und so wird er aufgeloest: der Import findet
statt, aber in einem **eigenen Prozess je Bot**. Damit kann keine der neun
gleichnamigen Dateien eine andere in `sys.modules` verdraengen - nicht weil wir
aufpassen, sondern weil jeder Prozess seinen eigenen `sys.modules` hat. Das ist
strenger als jede Namensvergabe im selben Prozess.

WAS DIESER PROZESS AM LAUFCODE AENDERT - UND WAS NICHT
------------------------------------------------------------------------------
Genau zwei Eingriffe, beide an der **Eingabe**, keiner an der Entscheidung:

1. `pandas.read_csv` liefert die Datei **bis zum Stichtag**. Das ist die
   Uebersetzung von "je Falte, nicht nur heute": ein Lauf am 1. Januar 2019
   sieht keine Kerze von 2024. Die Datei auf der Platte bleibt unberuehrt; es
   wird nur weniger davon durchgereicht. Die Schranke selbst
   (`MIN_HISTORY_DAYS` bzw. `MIN_HISTORY_HOURS`), der Leerlauf-Test, die
   Streichung unvollstaendiger Kerzen und alles weitere laufen unveraendert im
   Bot-Code.
2. `binance.client.Client.ping` wird stillgelegt. Grund: `shared/
   fetch_multi_data.py` legt auf Modulebene ein `client = Client()` an, und
   python-binance pingt im Konstruktor die Binance-API an. `strategies/
   elliott_wave/multi_symbol_optimise.py` importiert aus dieser Datei nur die
   Konstante `INTERVAL` - ohne den Eingriff braucht der Trockenlauf dieses
   einen Bots Netz, und in der Cloud scheitert er (403). Die Konstanten der
   Klasse bleiben unangetastet.

Zusaetzlich laeuft ein **Schreibschutz**: jeder Schreibversuch auf eine Datei
ausserhalb der ausdruecklich erlaubten Ausgabedatei bricht den Lauf ab.
`os.makedirs` wird dabei nicht abgebrochen, sondern folgenlos gemacht - die
Pfad-Hilfe `shared/strategy_paths.py` legt beim Import `results/<bot>/` und
`logs/<bot>/` an, und ein harter Abbruch dort wuerde den Loader gar nicht erst
starten lassen. Angelegt wird trotzdem nichts.

AUFRUF
------------------------------------------------------------------------------
    python3 loaderlauf.py --bot rsi2_crypto \
        --stichtage 2019-01-01T00:00:00,2019-12-31T23:59:59 \
        --aus /pfad/ergebnis.json

`--daten ORDNER` ersetzt den Kursdatenordner des Bots (nur fuer die
Probelaeufe der Tests und fuer `--stille-filter`). `TB40_BASE_DIR` verschiebt
die Repo-Wurzel - die Mutationsproben brauchen das, um auf einem Wegwerf-Repo
zu laufen.
"""

import argparse
import contextlib
import importlib.util
import io
import json
import os
import sys
import traceback


BASIS = os.environ.get("TB40_BASE_DIR") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Schreibschutz
# ---------------------------------------------------------------------------
class Schreibversuch(RuntimeError):
    """Der Trockenlauf hat versucht zu schreiben. Das ist ein Fehler."""


_ERLAUBT = []
_MAKEDIRS_VERSUCHE = []


def _ist_erlaubt(pfad):
    try:
        voll = os.path.abspath(os.fspath(pfad))
    except TypeError:
        # Dateideskriptor oder aehnliches - nicht beurteilbar, also erlauben.
        return True
    return any(voll == e or voll.startswith(e + os.sep) for e in _ERLAUBT)


def schreibschutz_an(erlaubte_pfade):
    """Macht jeden Schreibzugriff ausserhalb `erlaubte_pfade` zum Fehler.

    Rein defensiv: der Trockenlauf soll nichts schreiben, und das soll nicht
    von der Sorgfalt des Lesers abhaengen, sondern auffliegen.
    """
    import builtins
    import shutil

    for p in erlaubte_pfade:
        _ERLAUBT.append(os.path.abspath(p))

    echtes_open = builtins.open

    def wach_open(datei, modus="r", *a, **k):
        if any(z in str(modus) for z in ("w", "a", "x", "+")) and not _ist_erlaubt(datei):
            raise Schreibversuch("Schreibversuch auf %r (Modus %r)" % (datei, modus))
        return echtes_open(datei, modus, *a, **k)

    builtins.open = wach_open

    echtes_makedirs = os.makedirs
    echtes_mkdir = os.mkdir

    def wach_makedirs(name, *a, **k):
        if _ist_erlaubt(name):
            return echtes_makedirs(name, *a, **k)
        _MAKEDIRS_VERSUCHE.append(os.path.abspath(name))
        return None                      # folgenlos, aber kein Abbruch

    def wach_mkdir(name, *a, **k):
        if _ist_erlaubt(name):
            return echtes_mkdir(name, *a, **k)
        _MAKEDIRS_VERSUCHE.append(os.path.abspath(name))
        return None

    os.makedirs = wach_makedirs
    os.mkdir = wach_mkdir

    def _verboten(was):
        def f(*a, **k):
            raise Schreibversuch("Verbotener Aufruf %s%r" % (was, a[:2]))
        return f

    os.remove = _verboten("os.remove")
    os.unlink = _verboten("os.unlink")
    os.rename = _verboten("os.rename")
    os.replace = _verboten("os.replace")
    os.rmdir = _verboten("os.rmdir")
    shutil.rmtree = _verboten("shutil.rmtree")
    shutil.copy = _verboten("shutil.copy")
    shutil.copyfile = _verboten("shutil.copyfile")
    shutil.move = _verboten("shutil.move")


# ---------------------------------------------------------------------------
# Stichtag-Sicht auf die Kursdaten
# ---------------------------------------------------------------------------
_STICHTAG = [None]        # veraenderlich, damit der Patch sie sieht
_CACHE = {}


def stichtagssicht_an():
    """`read_csv` liefert nur, was bis zum Stichtag bekannt war.

    Der Cache ist kein Beiwerk: ohne ihn liest derselbe Bot dieselbe Datei
    einmal je Stichtag neu, bei 150 Aktien und 16 Stichtagen also 2400 Mal.
    Zurueckgegeben wird immer eine Kopie - der Loader darf seinen DataFrame
    veraendern, ohne den naechsten Stichtag zu vergiften.
    """
    import pandas as pd

    echtes_read_csv = pd.read_csv

    def wach_read_csv(pfad, *a, **k):
        schluessel = None
        try:
            schluessel = os.path.abspath(os.fspath(pfad))
        except TypeError:
            pass
        if schluessel is None:
            return echtes_read_csv(pfad, *a, **k)
        if schluessel not in _CACHE:
            _CACHE[schluessel] = echtes_read_csv(pfad, *a, **k)
        df = _CACHE[schluessel]
        stichtag = _STICHTAG[0]
        if stichtag is not None and "open_time" in df.columns:
            df = df[df["open_time"] <= stichtag]
        return df.copy().reset_index(drop=True)

    pd.read_csv = wach_read_csv


# ---------------------------------------------------------------------------
# Bot-Modul laden
# ---------------------------------------------------------------------------
def lade_botmodul(bot, datenordner=None):
    """Laedt `strategies/<bot>/multi_symbol_optimise.py` in DIESEN Prozess.

    Der Strategie-Ordner kommt an `sys.path[0]` - genauso, wie es beim
    normalen Aufruf `python3 strategies/<bot>/multi_symbol_optimise.py`
    passiert. Sonst faende das Modul seine Nachbarn (`backtest_*.py`,
    `stocks_symbols_config.py`) nicht.
    """
    strategie_dir = os.path.join(BASIS, "strategies", bot)
    datei = os.path.join(strategie_dir, "multi_symbol_optimise.py")
    if not os.path.exists(datei):
        raise FileNotFoundError(datei)
    sys.path.insert(0, strategie_dir)

    # Netz stilllegen, bevor irgendein Bot-Modul importiert wird.
    try:
        import binance.client
        binance.client.Client.ping = lambda self, *a, **k: {}
    except ImportError:
        pass

    spec = importlib.util.spec_from_file_location("botmodul_" + bot, datei)
    modul = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = modul
    spec.loader.exec_module(modul)

    if datenordner is not None:
        # DATA_DIR ist in jedem der neun Loader eine Modulvariable, die die
        # Ladeschleife bei jedem Aufruf frisch liest. Sie umzusetzen ist kein
        # Eingriff in die Entscheidung, sondern die Antwort auf die Frage
        # "welcher Kursdatenordner" - genau das, was die Probelaeufe brauchen.
        modul.DATA_DIR = os.path.abspath(datenordner)
    return modul


def schranken(modul):
    """Liest die Schranken des Bots AUS DEM GELADENEN MODUL - gemessen, nicht
    angenommen. Die Aufgabe verlangt das ausdruecklich."""
    ergebnis = {}
    for name in ("MIN_HISTORY_DAYS", "MIN_HISTORY_HOURS", "RECENT_YEARS_ONLY",
                 "INTERVAL", "MIN_TRADES", "MIN_SYMBOLS_CONTRIBUTING"):
        if hasattr(modul, name):
            ergebnis[name] = getattr(modul, name)
    ergebnis["SYMBOLE"] = list(getattr(modul, "SYMBOLS", []))
    ergebnis["DATA_DIR"] = getattr(modul, "DATA_DIR", None)
    return ergebnis


# ---------------------------------------------------------------------------
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bot", required=True)
    p.add_argument("--stichtage", default="",
                   help="Komma-Liste ISO-Zeitpunkte; leer = voller Datenstand")
    p.add_argument("--aus", required=True, help="Zieldatei fuer das JSON-Ergebnis")
    p.add_argument("--daten", default=None, help="Ersatz-Kursdatenordner")
    p.add_argument("--ohne-schreibschutz", action="store_true",
                   help="Schreibschutz abschalten. NUR fuer die Mutationsprobe, "
                        "die zeigt, dass der Datenstand-Hash auch ohne ihn "
                        "greift - im Trockenlauf selbst nie benutzt.")
    args = p.parse_args(argv)

    erlaubt = [os.path.dirname(os.path.abspath(args.aus))]
    if not args.ohne_schreibschutz:
        schreibschutz_an(erlaubt)
    stichtagssicht_an()

    ergebnis = {"bot": args.bot, "laeufe": [], "fehler": None}
    try:
        import pandas as pd
        modul = lade_botmodul(args.bot, args.daten)
        ergebnis["schranken"] = schranken(modul)

        stichtage = [s for s in args.stichtage.split(",") if s.strip()]
        if not stichtage:
            stichtage = [""]
        for s in stichtage:
            _STICHTAG[0] = pd.Timestamp(s) if s else None
            # Die eigene Ausgabe des Loaders wird mitgeschrieben. Sie ist
            # selbst ein Messwert: ob ein Symbol STILL verschwindet oder mit
            # Hinweiszeile, steht damit nicht im Quelltext, sondern im
            # beobachteten Ablauf.
            gemerkt = io.StringIO()
            with contextlib.redirect_stdout(gemerkt):
                geladen = modul.load_all_symbol_data()
            sys.stdout.write(gemerkt.getvalue())
            ergebnis["laeufe"].append({"stichtag": s or None,
                                       "symbole": sorted(geladen.keys()),
                                       "ausgabe": gemerkt.getvalue()})
    except Schreibversuch as e:
        ergebnis["fehler"] = "SCHREIBVERSUCH: %s" % e
    except Exception as e:                                   # noqa: BLE001
        ergebnis["fehler"] = "%s: %s" % (type(e).__name__, e)
        ergebnis["spur"] = traceback.format_exc()

    ergebnis["makedirs_unterdrueckt"] = sorted(set(_MAKEDIRS_VERSUCHE))

    with open(args.aus, "w") as f:                 # in `erlaubt`, also zulaessig
        json.dump(ergebnis, f, ensure_ascii=False, indent=1, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
