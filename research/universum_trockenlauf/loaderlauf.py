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
ausserhalb der ausdruecklich erlaubten Ausgabedatei bricht den Lauf ab. Bewacht
werden seit TB-43 **alle drei Ebenen**, ueber die in Python eine Datei zum
Schreiben aufgeht - `builtins.open`, `io.open` (und damit `pathlib.Path.open`,
`Path.write_text`, `Path.write_bytes`) und `os.open` -, und zwar unabhaengig
davon, ob Datei und Modus positional oder benannt uebergeben werden.
*Ein Schreibschutz, der einen Aufrufweg nicht kennt, ist an diesem Weg kein
Schreibschutz.*

Seit TB-44 gilt das auch **unabhaengig von der Python-Fassung und von der
Reihenfolge der Importe**. Der Grund steht ausfuehrlich bei `_Wache` und
`_bindungen_nachziehen`; kurz: `pathlib` legt sich beim Import eine **eigene
Kopie** der Oeffnungsfunktion in den Rumpf einer Klasse (`_NormalAccessor`,
Python 3.9 und 3.10). Je nachdem, ob dieser Import vor oder nach der Wache
passiert, war der Schutz vorher entweder **loechrig** (`Path.touch`,
`Path.mkdir` auf 3.9; `Path.open("w")`, `Path.write_text` auf 3.10 schrieben
wirklich) oder er brach sogar **lesende** Zugriffe ab (3.9 und 3.10). Gemessen,
nicht vermutet - `Teil L` des Selbsttests faehrt beide Reihenfolgen auf jeder
Python-Fassung ab, die auf dem Rechner liegt.
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
# Wohin die Wache sich nachtraeglich setzen musste, weil eine schon geladene
# Klasse sich vorher eine eigene Kopie gebunden hatte. Der Trockenlauf gibt
# diese Liste mit aus - sie ist ein Messwert, kein Protokoll.
_BINDUNGEN_NACHGEZOGEN = []


class _Wache:
    """Eine Wache, die sich **genauso bindet wie die Funktion, die sie ersetzt** -
    naemlich gar nicht.

    WARUM ES DIESE KLASSE GIBT
    ----------------------------------------------------------------------
    `os.open`, `io.open` und `builtins.open` sind in C geschrieben. Ihr Typ
    ist `builtin_function_or_method`, und der ist **kein Deskriptor**: steht
    so eine Funktion im Rumpf einer Klasse, kommt sie beim Zugriff ueber eine
    Instanz **unveraendert** zurueck.

    Eine Python-Funktion ist ein Deskriptor. An derselben Stelle wird aus ihr
    eine **gebundene Methode**, und die schiebt allen Argumenten die Instanz
    voran. Eine Wache, die eine C-Funktion durch eine Python-Funktion ersetzt,
    aendert damit etwas, das mit dem Schreibschutz nichts zu tun hat: das
    Bindungsverhalten.

    WO DAS ZUSCHLAEGT
    ----------------------------------------------------------------------
    `pathlib` schreibt beim Import in den Rumpf der Klasse `_NormalAccessor`:

        open = os.open        # CPython 3.9,  pathlib.py Z. 405
        open = io.open        # CPython 3.10, dieselbe Stelle
        mkdir = os.mkdir      # und ebenso unlink, rename, replace, rmdir

    Ab 3.11 gibt es `_NormalAccessor` nicht mehr; `Path.open` ruft `io.open`
    direkt. **Deshalb ist der Fehler auf 3.11 strukturell unsichtbar.**

    Passiert dieser Import **nach** der Wache, steht in der Klasse die Wache -
    und war sie eine Python-Funktion, verrutschten die Argumente
    (`pfad` = Accessor, `flags` = Path). Dann brach **sogar Lesen** ab.

    Eine Instanz mit `__call__` ist aufrufbar, aber kein Deskriptor. Sie
    bindet sich also wie das C-Original. Das ist **keine Sonderbehandlung fuer
    pathlib**, sondern die Wiederherstellung einer Eigenschaft, die das
    Original hatte und die die Wache verloren hatte - und sie gilt deshalb
    auch fuer jede andere Klasse, die sich dieselbe Kopie zieht.

    Die andere Reihenfolge - `pathlib` **vor** der Wache - deckt diese Klasse
    nicht ab; dafuer gibt es `_bindungen_nachziehen`.
    """

    def __init__(self, funktion, name):
        self._f = funktion
        self.__name__ = name
        self.__qualname__ = name
        self.__doc__ = getattr(funktion, "__doc__", None)
        self.__wrapped__ = funktion

    def __call__(self, *a, **k):
        return self._f(*a, **k)

    def __repr__(self):
        return "<Trockenlauf-Wache fuer %s>" % self.__name__


def _huelle(funktion, name):
    """Setzt eine Wache ein - **die einzige Stelle**, an der das passiert.

    Steht hier `return funktion`, ist die Wache wieder eine Python-Funktion
    und damit ein Deskriptor; genau das war der TB-44-Fehler. Die
    Mutationsprobe M1 aendert diese eine Zeile und muss den Fehler
    zurueckholen - sonst prueft Teil L an dieser Wache nichts.
    """
    return _Wache(funktion, name)


# Module, deren Inhalt NICHT nachgezogen wird: dort stehen die Originale, die
# die Wachen selbst noch brauchen, bzw. die Namen, die schon ersetzt wurden.
_NICHT_NACHZIEHEN = frozenset(("builtins", "io", "_io", "os", "posix", "nt",
                               "shutil", "sys", __name__))


def _bindungen_nachziehen(paare):
    """Ersetzt Kopien, die **vor** der Wache gebunden wurden.

    `_Wache` hilft nur, wenn die Kopie **nach** der Wache entsteht. War
    `pathlib` schon geladen, steht in `_NormalAccessor` die **echte**
    Funktion - und die kennt keinen Schreibschutz. Gemessen auf dem
    TB-43-Stand, mit `pathlib` vor der Wache:

      * Python 3.9:  `Path.touch()` legte die Datei wirklich an,
                     `Path.mkdir()` das Verzeichnis wirklich.
      * Python 3.10: `Path.open("w")` und `Path.write_text()` schrieben
                     wirklich - der Accessor hielt dort das echte `io.open`.

    Das ist die zweite Haelfte desselben Befunds, und sie ist die
    gefaehrlichere: ein Abbruch faellt auf, ein stilles Schreiben nicht.

    Gesucht wird nach **Identitaet**, nicht nach Namen: jede Stelle in einem
    schon geladenen Modul - auf Modulebene oder im Rumpf einer dort
    definierten Klasse -, die genau eines der uebergebenen Originale haelt,
    bekommt die zugehoerige Wache. Klassen werden nur ueber ihr eigenes Modul
    besucht (`__module__`), damit ein zweiter Name auf dieselbe Klasse sie
    nicht ein zweites Mal meldet.

    Zurueck kommt die Liste der Stellen. Sie steht im Bericht des Laufs: dass
    die Wache etwas zu tun hatte, ist beobachtbar und nicht nur behauptet.
    """
    nachgezogen = []

    def ersatz_fuer(wert):
        for alt, wache in paare:
            if wert is alt:
                return wache
        return None

    for modulname, modul in list(sys.modules.items()):
        if modul is None or modulname.split(".")[0] in _NICHT_NACHZIEHEN:
            continue
        try:
            eintraege = list(vars(modul).items())
        except TypeError:                     # Modul ohne __dict__
            continue
        for name, wert in eintraege:
            wache = ersatz_fuer(wert)
            if wache is not None:
                try:
                    setattr(modul, name, wache)
                except Exception:             # noqa: BLE001  schreibgeschuetzt
                    continue
                nachgezogen.append("%s.%s" % (modulname, name))
                continue
            if not isinstance(wert, type):
                continue
            if getattr(wert, "__module__", None) != modulname:
                continue
            for kname, kwert in list(vars(wert).items()):
                kwache = ersatz_fuer(kwert)
                if kwache is None:
                    continue
                try:
                    setattr(wert, kname, kwache)
                except Exception:             # noqa: BLE001
                    continue
                nachgezogen.append("%s.%s.%s" % (modulname, name, kname))
    return nachgezogen


def _ist_geraet(pfad):
    """Zeigt der Pfad auf etwas, das gar keine Datei auf der Platte ist?

    `/dev/null` und Konsorten sind Zeichengeraete: darauf zu schreiben
    veraendert nichts, was der Datenstand-Hash je sehen koennte. Der
    Schreibschutz bewacht den Platteninhalt, nicht den Systemaufruf an sich -
    und `python-binance` bzw. `yfinance` oeffnen `/dev/null` beim Import
    lesend-schreibend. Ein Pfad, den es noch nicht gibt, faellt hier
    ausdruecklich NICHT heraus: der wuerde ja gerade angelegt.
    """
    try:
        import stat
        return not stat.S_ISREG(os.stat(pfad).st_mode)
    except (OSError, ValueError, TypeError):
        return False


def _ist_erlaubt(pfad):
    if _ist_geraet(pfad):
        return True
    try:
        voll = os.path.abspath(os.fspath(pfad))
    except TypeError:
        # Dateideskriptor oder aehnliches - nicht beurteilbar, also erlauben.
        # Das bleibt vertretbar, WEIL `os.open` mitbewacht wird: ein
        # Schreib-Deskriptor kann gar nicht erst entstehen, ohne vorher an
        # der Wache vorbeizumuessen.
        return True
    return any(voll == e or voll.startswith(e + os.sep) for e in _ERLAUBT)


def _ist_schreibend(modus):
    """Ist das ein Schreibmodus? Gleiche Lesart wie zuvor - Zeichen im String."""
    return any(z in str(modus) for z in ("w", "a", "x", "+"))


def _open_argumente(a, k):
    """Liest Datei und Modus aus einem `open()`-Aufruf heraus - EGAL, ob sie
    positional oder benannt uebergeben wurden.

    Der Grund steht in TB-43: `open(pfad, mode="rb")` landete frueher mit
    `mode` in `**k`, der Durchgriff reichte den Modus dann ein zweites Mal
    positional weiter, und Python brach mit
    `argument for open() given by name ('mode') and position (2)` ab. Ein
    Schreibschutz, der einen Aufrufweg nicht kennt, ist an diesem Weg kein
    Schreibschutz - also wird hier nur GELESEN, was der Aufrufer meinte;
    weitergereicht wird der Aufruf danach unveraendert.

    Fehlt die Datei ganz (kaputter Aufruf), kommt `None` zurueck; der Aufruf
    laeuft dann durch, damit Python selbst den richtigen TypeError wirft.
    """
    datei = a[0] if a else k.get("file")
    modus = a[1] if len(a) >= 2 else k.get("mode", "r")
    return datei, modus


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

    def wach_open(*a, **k):
        # Die Argumente werden NUR GELESEN und danach unveraendert
        # weitergereicht - so kann der Modus nicht doppelt ankommen, gleich
        # wie der Aufrufer ihn uebergeben hat.
        datei, modus = _open_argumente(a, k)
        if _ist_schreibend(modus) and not _ist_erlaubt(datei):
            raise Schreibversuch("Schreibversuch auf %r (Modus %r)" % (datei, modus))
        return echtes_open(*a, **k)

    # TB-44: die Wache wird in eine `_Wache` gehuellt, BEVOR sie irgendwo
    # eingesetzt wird. Sonst ist sie eine Python-Funktion - also ein
    # Deskriptor -, und in einer Klasse, die sich davon eine Kopie zieht,
    # verrutschen die Argumente. Begruendung bei `_Wache`.
    wach_open = _huelle(wach_open, "open")

    builtins.open = wach_open
    # `builtins.open is io.open` ist wahr, aber es sind ZWEI Namen fuer
    # dasselbe Objekt: `builtins.open` zu ersetzen laesst `io.open`
    # unberuehrt. Und `pathlib.Path.open` - und damit `Path.write_text`,
    # `Path.write_bytes` - geht ueber `io.open`, nicht ueber `builtins.open`.
    # Ohne diese Zeile schreibt der Trockenlauf an der Wache vorbei.
    # Beide Namen bekommen DASSELBE Objekt, so wie vorher auch.
    io.open = wach_open

    echtes_os_open = os.open
    _SCHREIBFLAGS = 0
    for _name in ("O_WRONLY", "O_RDWR", "O_APPEND", "O_CREAT", "O_TRUNC"):
        _SCHREIBFLAGS |= getattr(os, _name, 0)

    def wach_os_open(pfad, flags, *a, **k):
        # `os.open` ist der unterste Weg: wer ihn hat, braucht weder
        # `builtins.open` noch `io.open`. `O_RDONLY` ist 0, ein reines Lesen
        # faellt also durch die Maske.
        if (flags & _SCHREIBFLAGS) and not _ist_erlaubt(pfad):
            raise Schreibversuch("Schreibversuch auf %r (os.open, Flags %d)"
                                 % (pfad, flags))
        return echtes_os_open(pfad, flags, *a, **k)

    wach_os_open = _huelle(wach_os_open, "open")
    os.open = wach_os_open

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

    wach_makedirs = _huelle(wach_makedirs, "makedirs")
    wach_mkdir = _huelle(wach_mkdir, "mkdir")
    os.makedirs = wach_makedirs
    os.mkdir = wach_mkdir

    def _verboten(was):
        def f(*a, **k):
            raise Schreibversuch("Verbotener Aufruf %s%r" % (was, a[:2]))
        # Auch hier eine `_Wache`: `pathlib._NormalAccessor` bindet auf 3.9
        # und 3.10 nicht nur `open`, sondern ebenso `unlink`, `rename`,
        # `replace` und `rmdir`. Ohne die Huelle wuerde aus `Path.unlink()`
        # ein Aufruf mit verschobenen Argumenten - der zwar auch abbricht,
        # aber mit dem falschen Fehler und aus dem falschen Grund.
        return _huelle(f, was.split(".")[-1])

    echte_verbotene = [(os.remove, "os.remove"), (os.unlink, "os.unlink"),
                       (os.rename, "os.rename"), (os.replace, "os.replace"),
                       (os.rmdir, "os.rmdir"), (shutil.rmtree, "shutil.rmtree"),
                       (shutil.copy, "shutil.copy"),
                       (shutil.copyfile, "shutil.copyfile"),
                       (shutil.move, "shutil.move")]
    wachen_verboten = [(f, _verboten(n)) for f, n in echte_verbotene]

    os.remove, os.unlink, os.rename, os.replace, os.rmdir = \
        [w for _f, w in wachen_verboten[:5]]
    shutil.rmtree, shutil.copy, shutil.copyfile, shutil.move = \
        [w for _f, w in wachen_verboten[5:]]

    # TB-44, zweite Haelfte: war `pathlib` (oder sonst jemand) schon VOR
    # dieser Zeile geladen, steht dort noch die echte Funktion. Die wird
    # jetzt nachgezogen. Begruendung und Messwerte bei
    # `_bindungen_nachziehen`.
    _BINDUNGEN_NACHGEZOGEN.extend(_bindungen_nachziehen(
        [(echtes_open, wach_open), (echtes_os_open, wach_os_open),
         (echtes_makedirs, wach_makedirs), (echtes_mkdir, wach_mkdir)]
        + wachen_verboten))


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
    ergebnis["bindungen_nachgezogen"] = sorted(set(_BINDUNGEN_NACHGEZOGEN))

    with open(args.aus, "w") as f:                 # in `erlaubt`, also zulaessig
        json.dump(ergebnis, f, ensure_ascii=False, indent=1, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
