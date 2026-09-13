"""
Ein Bot, ein Prozess: derselbe Backtest unter permutierter Symbolreihenfolge
==============================================================================
Hilfsprogramm von `shared/determinismus.py`. Es wird nicht von Hand
aufgerufen, sondern je Bot als eigener Prozess gestartet:

    python3 shared/determinismus_lauf.py <bot_name> [Optionen]

Es fuehrt den `__main__`-Block von `strategies/<bot>/equity_simulation.py`
N-mal aus und aendert zwischen den Laeufen **ausschliesslich die Reihenfolge
der Symbolliste**. Kursdaten, Parameter und Code bleiben identisch. Was sich
danach noch unterscheidet, ist versteckter Zustand.

WARUM DER __main__-BLOCK UND NICHT DIE EINZELNEN FUNKTIONEN
------------------------------------------------------------------------------
Dieselbe Begruendung wie in `shared/kurven_lauf.py`: wer
`collect_all_trades()` selbst aufruft, fuehrt eine zweite Fassung der Frage
"womit rechnet dieser Bot eigentlich" ein - und genau daran ist der
HRP-Bericht zweimal gekippt (`volatility_breakout_crypto` wendet seinen
BTC-Regimefilter an der Aufrufstelle im `__main__`-Block an, nicht in
`collect_all_trades()`). `runpy.run_path(..., run_name="__main__")` haelt die
Argumentzuordnung an genau einer Stelle: in der Datei des Bots.

WIE PERMUTIERT WIRD - UND WAS DABEI NICHT ANGEFASST WIRD
------------------------------------------------------------------------------
`config/sp500_top150.txt` und `config/top25_symbols.txt` werden **gelesen und
nicht geschrieben**. Ihre heutige Sortierung (absteigend nach Marktkapitali-
sierung bzw. Volumen) ist eine bewusste Ordnung und bleibt unberuehrt.

Die Permutation geschieht im Speicher, an genau der Stelle, an der die Liste
in den Bot eintritt: `multi_symbol_optimise.SYMBOLS`. Das ist der Name, den
`load_all_symbol_data()` in allen neun Bots liest (`for symbol in SYMBOLS`).
Der Bot sieht dadurch exakt das, was er saehe, wenn die Datei anders sortiert
waere.

Damit das keine stille Annahme bleibt, prueft `_ladeordnung_pruefen()` nach
**jedem** Lauf, dass die tatsaechlich geladene Symbolfolge der angeforderten
Permutation entspricht. Eine Permutation, die gar nicht ankommt, wuerde sonst
neun deterministische Bots melden - der teuerste Fehler, den dieses Programm
machen koennte.

DER ZWISCHENSPEICHER - UND WARUM ER SICH ZUERST BEWEISEN MUSS
------------------------------------------------------------------------------
Der teure Teil (Wellenerkennung, Indikatoren) laeuft je Symbol unabhaengig.
Ein Zwischenspeicher darueber macht die Laeufe 2..N fast kostenlos - setzt
aber genau das voraus, was hier gemessen werden soll. Deshalb rechnet der
Speicher die ersten `--pruef-laeufe` Permutationen **trotzdem voll durch** und
vergleicht jedes Symbolergebnis mit dem gespeicherten. Weicht eines ab, ist
das ein Befund ("Signalerzeugung reihenfolgeabhaengig") und kein
Speicherfehler.

`--voll` schaltet den Speicher ganz ab: jede Permutation rechnet komplett neu.
Das ist der Modus fuer die Bestandsaufnahme; der Speicher ist fuer die
regelmaessige Pruefung da.

WOHIN GESCHRIEBEN WIRD
------------------------------------------------------------------------------
`RESULTS_DIR` wird fuer die Dauer der Laeufe in einen temporaeren Ordner
umgelenkt - wie in `kurven_lauf.py`. Dieses Programm kann
`results/<bot>/equity_curve.csv` gar nicht ueberschreiben, auch nicht
versehentlich. Es schreibt ueberhaupt nichts ins Repo; die Ergebnisse gehen
als JSON auf die Standardausgabe bzw. in den mit `--json` genannten Pfad.

Unvollstaendige Kursbalken haelt `shared/kursdaten.py` fern - nicht von hier
aus, sondern dort, wo die Daten ins Programm kommen: alle neun
`multi_symbol_optimise.load_all_symbol_data()` rufen seit PR #81
`entferne_unvollstaendige()` auf. Eine zweite Filterung hier waere eine
zweite Wahrheit ueber dieselben Daten.
"""

import argparse
import contextlib
import hashlib
import io
import json
import os
import random
import runpy
import sys
import tempfile
import time
import types

import pandas as pd

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)

# Die Renditeformel steht seit TB-28 an einer Stelle (shared/messkette.py).
# Vorher stand sie hier ein zweites Mal ausgeschrieben. Der Max Drawdown wird
# hier NICHT nachgerechnet - er kommt als Variable `max_dd` aus den
# __main__-Globalen des Bots, also aus dessen eigener Rechnung (siehe
# `auswerten()`); das bleibt so.
#
# Der sys.path-Eintrag ist noetig, weil dieses Modul auch als Unterprozess
# mit anderem Arbeitsverzeichnis startet.
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)
from messkette import rendite_pct

# Markiert die Meldezeile an das aufrufende Programm. Eigener Praefix statt
# "die letzte Zeile nehmen": der __main__-Block des Bots gibt selbst reichlich
# aus.
META_PREFIX = "__DETERMINISMUS__ "

# Auf so viele Nachkommastellen werden Geldbetraege und Prozentwerte gebracht,
# bevor daraus ein Fingerabdruck wird. Neun Stellen sind weit jenseits jeder
# inhaltlichen Aussage und zugleich robust gegen die letzte Bitstelle einer
# Gleitkommazahl. Gerundet wird, weil sonst eine reine Summationsreihenfolge
# als "Befund" erschiene - und ein Test, der immer rot ist, wird abgeschaltet.
RUNDUNG = 9


# ---------------------------------------------------------------------------
# Umgebung: Stubs und Pfadumlenkung (uebernommen aus shared/kurven_lauf.py)
# ---------------------------------------------------------------------------
def _stubs_setzen():
    """Module, die in diesem Lauf nie gebraucht werden, aber importiert
    wuerden. `setdefault` statt Zuweisung: ist das echte Modul vorhanden,
    gewinnt es. `shared/fetch_binance_data.py` enthaelt Zugangsdaten und ist
    gitignored; yfinance und python-binance sind nicht ueberall installiert.
    Gelesen werden ausschliesslich die vorhandenen CSVs unter `data/`."""
    fake_fetch = types.ModuleType("fetch_binance_data")
    fake_fetch.fetch_historical_data = lambda *a, **kw: pd.DataFrame()
    sys.modules.setdefault("fetch_binance_data", fake_fetch)

    fake_binance = types.ModuleType("binance")
    fake_client = types.ModuleType("binance.client")

    class _FakeClient:
        KLINE_INTERVAL_1HOUR = "1h"
        KLINE_INTERVAL_4HOUR = "4h"
        KLINE_INTERVAL_1DAY = "1d"

    fake_client.Client = _FakeClient
    fake_binance.client = fake_client
    sys.modules.setdefault("binance", fake_binance)
    sys.modules.setdefault("binance.client", fake_client)

    fake_yf = types.ModuleType("yfinance")
    fake_yf.download = lambda *a, **kw: pd.DataFrame()
    fake_yf.Ticker = lambda *a, **kw: None
    sys.modules.setdefault("yfinance", fake_yf)


def _results_dir_umlenken(ziel: str):
    """Ersetzt `strategy_paths` durch eine Fassung, die alles an die echte
    Funktion weiterreicht und nur RESULTS_DIR austauscht."""
    import strategy_paths as echt

    ersatz = types.ModuleType("strategy_paths")
    ersatz.__doc__ = echt.__doc__
    ersatz._ECHT = echt

    def get_strategy_paths(caller_file):
        pfade = echt.get_strategy_paths(caller_file)
        pfade["RESULTS_DIR"] = ziel
        os.makedirs(ziel, exist_ok=True)
        return pfade

    ersatz.get_strategy_paths = get_strategy_paths
    sys.modules["strategy_paths"] = ersatz


# ---------------------------------------------------------------------------
# Fingerabdruecke - WAS genau verglichen wird
# ---------------------------------------------------------------------------
# Verglichen wird auf drei Ebenen, absichtlich nicht nur auf einer:
#
#   1. signalmenge   - alle erzeugten Trades, BEVOR das Kapital darueber
#                      entscheidet. Reihenfolgeunabhaengig verglichen (als
#                      Multimenge), denn die Zeilenreihenfolge des
#                      zusammengehaengten DataFrames ist ein Nebenprodukt der
#                      Symbolbloecke und beschreibt keinen Verlauf, den jemand
#                      erlebt haette (dieselbe Begruendung steht bereits in
#                      multi_symbol_optimise.py). Weicht SIE ab, hat die
#                      Signalerzeugung selbst versteckten Zustand - der
#                      schwerste denkbare Befund.
#   2. ausgefuehrt   - welche Trades tatsaechlich Kapital bekommen haben,
#                      ebenfalls als Multimenge. DAS ist das Leitkriterium:
#                      hier schlaegt die Zuteilung bei bindendem Positions-
#                      limit durch.
#   3. kapitalpfad   - die Ereigniszeilen der Kapitalkurve IN IHRER
#                      REIHENFOLGE, mit Allokation und Kapitalstand. Strengste
#                      Ebene; sie kann auch dann abweichen, wenn dieselben
#                      Trades nur in anderer Reihenfolge abgerechnet werden.
#
# Die Kennzahlen (Rendite, Drawdown, Trade-Zahl) werden zusaetzlich gefuehrt,
# aber NICHT als Kriterium: ein Vergleich der Kennzahlen allein wuerde genau
# die Unterschiede verdecken, die sich herausmitteln.
def _iso(spalte: pd.Series) -> pd.Series:
    return pd.to_datetime(spalte).astype("datetime64[ns]").astype(str)


def _fingerabdruck(zeilen) -> str:
    h = hashlib.sha256()
    for zeile in zeilen:
        h.update(repr(zeile).encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()


def handelsschluessel(trades: pd.DataFrame) -> list:
    """Der Schluessel, unter dem ein Trade in beiden Welten wiedererkennbar
    ist: in der Trade-Liste und in der Kapitalkurve.

    Die Kapitalkurve fuehrt je ausgefuehrten Trade genau eine Zeile mit
    `time` = Ausstiegszeitpunkt, `symbol` und `pnl_pct`. Mehr steht dort nicht
    ueber den Trade selbst; `allocation` und `capital_after` haengen vom
    Verlauf ab und taugen nicht zur Identifikation. Deshalb (symbol, Ausstieg,
    Ergebnis) - und verglichen wird als MULTImenge, damit zwei zufaellig
    gleiche Trades desselben Symbols nicht zu einem verschmelzen.
    """
    if trades.empty:
        return []
    zeit = _iso(trades["exit_time"])
    pnl = pd.to_numeric(trades["pnl_pct"], errors="coerce").round(RUNDUNG)
    return list(zip(trades["symbol"].astype(str), zeit, pnl))


def kurvenschluessel(kurve: pd.DataFrame) -> list:
    if kurve.empty:
        return []
    zeit = _iso(kurve["time"])
    pnl = pd.to_numeric(kurve["pnl_pct"], errors="coerce").round(RUNDUNG)
    return list(zip(kurve["symbol"].astype(str), zeit, pnl))


SIGNAL_SPALTEN = ["symbol", "entry_time", "exit_time", "entry_price",
                  "exit_price", "pnl_pct", "exit_reason"]


def signalzeilen(trades: pd.DataFrame) -> list:
    """Die vollstaendige Beschreibung jedes erzeugten Trades, so weit der Bot
    sie liefert. Fehlende Spalten werden uebergangen statt erfunden; welche
    benutzt wurden, steht im Bericht."""
    if trades.empty:
        return []
    vorhanden = [s for s in SIGNAL_SPALTEN if s in trades.columns]
    form = trades[vorhanden].copy()
    for spalte in ("entry_time", "exit_time"):
        if spalte in form.columns:
            form[spalte] = _iso(form[spalte])
    for spalte in ("entry_price", "exit_price", "pnl_pct"):
        if spalte in form.columns:
            form[spalte] = pd.to_numeric(form[spalte], errors="coerce").round(RUNDUNG)
    return [tuple(z) for z in form.itertuples(index=False, name=None)]


def kapitalpfadzeilen(kurve: pd.DataFrame) -> list:
    """Die Kapitalkurve IN IHRER REIHENFOLGE - dieselben Spalten, an denen
    shared/ergebniskurven.py zwei Kurven misst."""
    if kurve.empty:
        return []
    form = kurve[["time", "symbol", "pnl_pct", "allocation", "capital_after"]].copy()
    form["time"] = _iso(form["time"])
    form["symbol"] = form["symbol"].astype(str)
    for spalte in ("pnl_pct", "allocation", "capital_after"):
        form[spalte] = pd.to_numeric(form[spalte], errors="coerce").round(RUNDUNG)
    return [tuple(z) for z in form.itertuples(index=False, name=None)]


def zaehlwerk(schluessel: list) -> dict:
    zaehler = {}
    for k in schluessel:
        zaehler[k] = zaehler.get(k, 0) + 1
    return zaehler


def zeitfenster(trades: pd.DataFrame) -> list:
    """(Schluessel, Einstieg, Ausstieg) je erzeugtem Trade - die Grundlage der
    Limit-Analyse. Die Reihenfolge dieser Liste spielt keine Rolle."""
    if trades.empty:
        return []
    ein = pd.to_datetime(trades["entry_time"]).astype("int64").tolist()
    aus = pd.to_datetime(trades["exit_time"]).astype("int64").tolist()
    return list(zip(handelsschluessel(trades), ein, aus))


def limitanalyse(fenster: list, ausgefuehrt: dict, limit) -> dict:
    """Bindet das Positionslimit ueberhaupt?

    Gezaehlt wird auf den TATSAECHLICH ausgefuehrten Positionen - nur die
    binden Kapital und belegen einen Platz. Die Belegung wird nach derselben
    Regel fortgeschrieben, die `simulate_portfolio()` benutzt: bei gleichem
    Zeitpunkt zuerst die Ausstiege, dann die Einstiege. Der Hoechststand ist
    damit eindeutig - er haengt NICHT davon ab, in welcher Reihenfolge die
    Einstiege desselben Zeitpunkts abgearbeitet werden.

    Liegt der Hoechststand unter dem Limit, hat das Limit in diesem Lauf nie
    gebunden; dann kann es auch nicht zugeteilt haben.
    """
    offen = dict(ausgefuehrt)
    ereignisse = []
    for schluessel, ein, aus in fenster:
        if offen.get(schluessel, 0) > 0:
            offen[schluessel] -= 1
            ereignisse.append((ein, 1))
            ereignisse.append((aus, 0))
    # 0 vor 1: Ausstiege zuerst, genau wie im Bot.
    ereignisse.sort()

    stand = hoechststand = 0
    am_limit = set()
    for zeit, art in ereignisse:
        stand += 1 if art else -1
        hoechststand = max(hoechststand, stand)
        if limit is not None and stand >= limit:
            am_limit.add(zeit)

    return {
        "limit": limit,
        "gleichzeitig_offen_max": hoechststand,
        "limit_erreicht": limit is not None and hoechststand >= limit,
        "zeitpunkte_am_limit": len(am_limit),
    }


def kapitalschranke(allocation_pct, limit) -> dict:
    """Die zweite Schranke, die Trades ablehnt: zu wenig freies Kapital.
    `simulate_portfolio()` wirft beide in dieselbe Zaehlung, gibt aber nur
    deren Summe zurueck - eine Aufschluesselung ist von aussen nicht moeglich
    (so steht es auch im Kommentar der Bots selbst). Rechnerisch laesst sich
    aber sagen, ob sie ueberhaupt vor dem Limit greifen KANN: bei einer
    Allokation von a sind hoechstens 1/a Positionen finanzierbar."""
    if not allocation_pct:
        return {"max_finanzierbar": None, "greift_vor_dem_limit": None}
    max_finanzierbar = int(1 / allocation_pct)
    return {
        "max_finanzierbar": max_finanzierbar,
        "greift_vor_dem_limit": (limit is None or max_finanzierbar < limit),
    }


# ---------------------------------------------------------------------------
# Der Zwischenspeicher je Symbol (siehe Kopfkommentar)
# ---------------------------------------------------------------------------
class Symbolspeicher:
    """Memoisiert die beiden teuren, je Symbol unabhaengigen Schritte:
    `load_all_symbol_data` (CSV einlesen und beschneiden) und
    `get_trades_for_symbol` (Indikatoren, Wellenerkennung, Backtest).

    Die ersten `pruef_laeufe` Wiederholungen werden trotzdem gerechnet und
    Symbol fuer Symbol gegen den gespeicherten Wert gehalten. Ein Unterschied
    ist ein Befund, kein Speicherfehler - deshalb wird er gesammelt und nicht
    verschluckt. Das Nachrechnen faengt zugleich den anderen denkbaren Fehler
    ab: einen Bot, der einen gespeicherten Kurs-DataFrame veraendert. Waere das
    so, wuerde der frisch geladene beim naechsten Vergleich abweichen.

    Der Speicher darf die Reihenfolge NICHT konservieren: `daten_huelle` baut
    den zurueckgegebenen Datensatz jedes Mal in der GERADE gesetzten
    Symbolreihenfolge neu auf. Sonst wuerde dieses Programm N-mal dasselbe
    rechnen und neun deterministische Bots melden. `_ladeordnung_pruefen()`
    haelt genau darauf die Hand.
    """

    def __init__(self, pruef_laeufe: int, aktiv: bool = True):
        self.aktiv = aktiv
        self.pruef_laeufe = pruef_laeufe
        self.lauf = 0
        self.speicher = {}
        self.daten = None
        self.id_zu_symbol = {}
        self.abweichungen = []
        self.daten_abweichungen = []
        self.berechnet = 0
        self.geliefert = 0
        self.nachgerechnet = 0
        self.daten_geladen = 0

    def neuer_lauf(self, nummer: int):
        self.lauf = nummer

    def _nachrechnen_faellig(self) -> bool:
        # Lauf 0 fuellt den Speicher. Danach wird noch `pruef_laeufe` mal
        # nachgerechnet; ohne Speicher (--voll) immer.
        if not self.aktiv:
            return True
        return self.lauf <= self.pruef_laeufe

    # -- Kursdaten ----------------------------------------------------------
    def daten_umhuellen(self, echt, reihenfolge):
        """`reihenfolge()` liefert die gerade gueltige Symbolreihenfolge.

        Ein frisch geladener Datensatz wird **unveraendert** durchgereicht -
        genau so, wie der Bot ihn selbst aufgebaut hat. Das ist wichtig: nur
        dann sieht `_ladeordnung_pruefen()` die echte Ladereihenfolge und kann
        einen Bot erkennen, der die Permutation gar nicht durchlaufen laesst.
        Wuerde diese Huelle den Datensatz immer in die angeforderte
        Reihenfolge bringen, haette sie die Wache selbst blind gemacht.

        Nur der Weg aus dem Speicher baut die Reihenfolge nach - und der wird
        erst beschritten, nachdem mindestens ein echter Ladevorgang belegt
        hat, dass der Bot die Liste in genau dieser Reihenfolge durchlaeuft.
        """
        def huelle(*args, **kwargs):
            if self.daten is None or self._nachrechnen_faellig():
                frisch = echt(*args, **kwargs)
                self.daten_geladen += 1
                if self.daten is not None:
                    if set(frisch) != set(self.daten):
                        self.daten_abweichungen.append({
                            "lauf": self.lauf, "grund": "andere Symbolauswahl",
                            "vorher": len(self.daten), "jetzt": len(frisch)})
                    for symbol, df in frisch.items():
                        if symbol in self.daten and not self._gleich(self.daten[symbol], df):
                            self.daten_abweichungen.append({
                                "lauf": self.lauf, "symbol": symbol,
                                "grund": "Kursdaten weichen ab"})
                self.daten = frisch
                self._id_tabelle(frisch)
                return frisch
            return self._in_reihenfolge(reihenfolge())
        return huelle

    def _id_tabelle(self, daten: dict):
        """get_trades_for_symbol bekommt nur den DataFrame, nicht den
        Symbolnamen - hier entsteht die Zuordnung zurueck."""
        self.id_zu_symbol = {}
        for symbol, wert in daten.items():
            # Drei der neun Bots legen (df, entry_cutoff) statt df ab und
            # reichen den DataFrame einzeln an get_trades_for_symbol weiter -
            # deshalb wird auch jedes Tupel-Element eingetragen.
            self.id_zu_symbol[id(wert)] = symbol
            if isinstance(wert, tuple):
                for teil in wert:
                    self.id_zu_symbol[id(teil)] = symbol

    def _in_reihenfolge(self, ordnung: list) -> dict:
        geladen = self.daten
        neu = {s: geladen[s] for s in ordnung if s in geladen}
        # Symbole, die geladen wurden, aber nicht in der Reihenfolge stehen,
        # duerfen nicht verschwinden - sonst rechnete der Bot mit weniger
        # Daten, statt mit denselben in anderer Reihenfolge.
        for symbol, wert in geladen.items():
            if symbol not in neu:
                neu[symbol] = wert
        self._id_tabelle(neu)
        return neu

    # -- Signale je Symbol --------------------------------------------------
    def umhuellen(self, echt):
        def huelle(price_df, *args, **kwargs):
            symbol = self.id_zu_symbol.get(id(price_df))
            if symbol is None:
                # Kein Symbol zuordenbar (sollte nicht vorkommen) - dann lieber
                # rechnen als raten.
                return echt(price_df, *args, **kwargs)

            schluessel = (symbol, repr(args), repr(sorted(kwargs.items())))
            bekannt = schluessel in self.speicher

            if not bekannt or self._nachrechnen_faellig():
                frisch = echt(price_df, *args, **kwargs)
                self.berechnet += 1
                if bekannt:
                    self.nachgerechnet += 1
                    if not self._gleich(self.speicher[schluessel], frisch):
                        self.abweichungen.append({
                            "symbol": symbol, "lauf": self.lauf,
                            "zeilen_gespeichert": int(len(self.speicher[schluessel])),
                            "zeilen_jetzt": int(len(frisch)),
                        })
                self.speicher[schluessel] = frisch
                return frisch

            self.geliefert += 1
            return self.speicher[schluessel]

        return huelle

    @classmethod
    def _gleich(cls, a, b) -> bool:
        """Vergleicht, was die Bots tatsaechlich ablegen: einen DataFrame oder
        ein Tupel (DataFrame, Stichtag) - drei der neun Bots tun Letzteres."""
        if a is None or b is None:
            return a is None and b is None
        if isinstance(a, tuple) or isinstance(b, tuple):
            if not (isinstance(a, tuple) and isinstance(b, tuple)) or len(a) != len(b):
                return False
            return all(cls._gleich(x, y) for x, y in zip(a, b))
        if isinstance(a, pd.DataFrame) or isinstance(b, pd.DataFrame):
            if not (isinstance(a, pd.DataFrame) and isinstance(b, pd.DataFrame)):
                return False
            if len(a) != len(b) or list(a.columns) != list(b.columns):
                return False
            if a.empty:
                return True
            return a.reset_index(drop=True).equals(b.reset_index(drop=True))
        if a is b:
            return True
        # Skalare (z.B. der Stichtag): NaT/NaN gelten als gleich, wenn beide
        # fehlen - sonst waere jeder Vergleich eines Bots ohne RECENT_YEARS_ONLY
        # grundlos ein Befund.
        if pd.isna(a) and pd.isna(b):
            return True
        return bool(a == b)


# ---------------------------------------------------------------------------
def _ladeordnung_pruefen(erwartet: list, beobachtet: list) -> str:
    """Die Permutation muss im Bot ANKOMMEN. Sonst meldet dieses Programm
    neun deterministische Bots, weil es neunmal dasselbe gerechnet hat.

    `beobachtet` ist die Einfuegereihenfolge von `all_data` - also genau die
    Reihenfolge, in der `load_all_symbol_data()` die Symbole durchlaufen hat.
    Symbole ohne Datei oder mit zu kurzer Historie fallen dabei heraus; darum
    wird `erwartet` auf die geladenen gefiltert statt beide gleich lang
    erwartet.
    """
    gefiltert = [s for s in erwartet if s in set(beobachtet)]
    if gefiltert != list(beobachtet):
        return (f"Die permutierte Reihenfolge ist nicht im Bot angekommen. "
                f"erwartet {gefiltert[:6]}..., geladen {list(beobachtet)[:6]}...")
    return ""


def permutationen(basis: list, anzahl: int, seed: int) -> list:
    """Lauf 0 ist IMMER die Originalreihenfolge - der Bezugspunkt, gegen den
    alles verglichen wird. Die uebrigen sind echte Zufallspermutationen aus
    einem festen Startwert; derselbe Startwert liefert dieselbe Folge."""
    rng = random.Random(seed)
    folge = [list(basis)]
    for _ in range(max(0, anzahl - 1)):
        kandidat = list(basis)
        rng.shuffle(kandidat)
        folge.append(kandidat)
    return folge


def _spanne(werte: list) -> dict:
    sauber = [w for w in werte if w is not None and w == w]
    if not sauber:
        return {"min": None, "max": None, "spanne": None, "verschiedene_werte": 0}
    return {
        "min": round(min(sauber), 2),
        "max": round(max(sauber), 2),
        "spanne": round(max(sauber) - min(sauber), 2),
        "verschiedene_werte": len(set(round(w, 6) for w in sauber)),
    }


# ---------------------------------------------------------------------------
def lauf(bot: str, anzahl: int, seed: int, pruef_laeufe: int, voll: bool,
         ziel: str, basis: str = None) -> dict:
    # `basis` ist die Projektwurzel. Voreinstellung ist die echte; die
    # Selbsttests zeigen damit einen eigenen, wegwerfbaren Kunstbot auf,
    # ohne einen Ordner im Repo anzulegen.
    strategie_dir = os.path.join(basis or BASE_DIR, "strategies", bot)
    skript = os.path.join(strategie_dir, "equity_simulation.py")
    if not os.path.exists(skript):
        raise SystemExit(f"{bot}: {skript} nicht gefunden.")

    sys.path.insert(0, strategie_dir)
    sys.path.insert(0, _SHARED_DIR)
    _stubs_setzen()
    _results_dir_umlenken(ziel)
    os.chdir(strategie_dir)

    import multi_symbol_optimise as mso

    basis = list(mso.SYMBOLS)
    if len(basis) < 2:
        raise SystemExit(f"{bot}: nur {len(basis)} Symbol(e) - nichts zu permutieren.")

    # Mindestens eine echte Wiederholung. Sie ist nicht nur die Probe auf den
    # Zwischenspeicher, sondern auch der einzige Lauf, in dem
    # `_ladeordnung_pruefen()` die ECHTE Ladereihenfolge des Bots zu sehen
    # bekommt (Lauf 0 laeuft ohnehin in der Originalreihenfolge und wuerde die
    # Wache nie ausloesen). Ohne ihn koennte ein Bot, der sein Universum
    # selbst sortiert, als "deterministisch" durchgehen.
    pruef_laeufe = max(1, pruef_laeufe)
    speicher = Symbolspeicher(pruef_laeufe=pruef_laeufe, aktiv=not voll)
    echt_trades = mso.get_trades_for_symbol
    echt_laden = mso.load_all_symbol_data
    mso.get_trades_for_symbol = speicher.umhuellen(echt_trades)

    beobachtete_ordnung = {}
    gepuffert = speicher.daten_umhuellen(echt_laden, lambda: list(mso.SYMBOLS))

    def laden_huelle(*args, **kwargs):
        daten = gepuffert(*args, **kwargs)
        beobachtete_ordnung["letzte"] = list(daten.keys())
        return daten

    mso.load_all_symbol_data = laden_huelle

    folge = permutationen(basis, anzahl, seed)
    laeufe = []
    fehler = []
    globalen = {}

    for nummer, ordnung in enumerate(folge):
        speicher.neuer_lauf(nummer)
        mso.SYMBOLS = list(ordnung)
        beobachtete_ordnung.pop("letzte", None)

        begonnen = time.time()
        puffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(puffer):
                globalen = runpy.run_path(skript, run_name="__main__")
        except SystemExit as ende:
            fehler.append(f"Lauf {nummer}: Bot hat abgebrochen ({ende}). "
                          f"Ausgabe: {puffer.getvalue()[-400:]}")
            break
        dauer = time.time() - begonnen

        meldung = _ladeordnung_pruefen(ordnung, beobachtete_ordnung.get("letzte", []))
        if meldung:
            fehler.append(f"Lauf {nummer}: {meldung}")
            break

        trades = globalen.get("trades")
        ergebnis = globalen.get("result") or {}
        kurve = ergebnis.get("equity_curve")
        if trades is None or kurve is None:
            fehler.append(f"Lauf {nummer}: der Bot hat kein Ergebnis hinterlassen.")
            break

        laeufe.append({
            "nummer": nummer,
            "dauer_s": round(dauer, 2),
            "symbole_geladen": len(beobachtete_ordnung.get("letzte", [])),
            "erste_symbole": list(beobachtete_ordnung.get("letzte", []))[:5],
            "signal_fp": _fingerabdruck(sorted(signalzeilen(trades))),
            "signal_spalten": [s for s in SIGNAL_SPALTEN if s in trades.columns],
            "signal_zahl": int(len(trades)),
            "signal_schluessel": handelsschluessel(trades),
            "zeitfenster": zeitfenster(trades),
            "ausgefuehrt_fp": _fingerabdruck(sorted(kurvenschluessel(kurve))),
            "ausgefuehrt_schluessel": kurvenschluessel(kurve),
            "kapitalpfad_fp": _fingerabdruck(kapitalpfadzeilen(kurve)),
            "endkapital": ergebnis.get("final_capital"),
            "rendite_pct": (round(rendite_pct(ergebnis["final_capital"],
                                              globalen["STARTING_CAPITAL"]), 2)
                            if ergebnis.get("final_capital") is not None else None),
            "max_drawdown_pct": globalen.get("max_dd"),
            "trades_ausgefuehrt": ergebnis.get("num_executed"),
            "trades_uebersprungen": ergebnis.get("num_skipped"),
        })

    mso.get_trades_for_symbol = echt_trades
    mso.load_all_symbol_data = echt_laden

    return auswerten(bot, basis, folge, laeufe, fehler, speicher, globalen, seed,
                     voll, pruef_laeufe)


def auswerten(bot, basis, folge, laeufe, fehler, speicher, globalen, seed,
              voll, pruef_laeufe) -> dict:
    bericht = {
        "bot": bot,
        "seed": seed,
        "permutationen_angefordert": len(folge),
        "permutationen_gelaufen": len(laeufe),
        "voll_modus": voll,
        "pruef_laeufe": None if voll else pruef_laeufe,
        "symbole_in_datei": len(basis),
        "konfiguration": {
            "startkapital": globalen.get("STARTING_CAPITAL"),
            "allocation_pct": globalen.get("ALLOCATION_PCT"),
            "max_concurrent_positions": globalen.get("MAX_CONCURRENT_POSITIONS"),
            "bot_hat_limit_parameter": "max_concurrent_positions" in (
                globalen["simulate_portfolio"].__code__.co_varnames
                if "simulate_portfolio" in globalen else ()),
        },
        "fehler": fehler,
        "zwischenspeicher": {
            "aktiv": speicher.aktiv,
            "symbolrechnungen": speicher.berechnet,
            "aus_speicher": speicher.geliefert,
            "nachgerechnet_und_verglichen": speicher.nachgerechnet,
            "abweichungen": speicher.abweichungen,
            "kursdaten_ladevorgaenge": speicher.daten_geladen,
            "kursdaten_abweichungen": speicher.daten_abweichungen,
        },
    }

    if fehler or len(laeufe) < 2:
        bericht["urteil"] = "UNKLAR"
        bericht["laeufe"] = [{k: v for k, v in lauf_.items()
                              if not k.endswith("_schluessel") and k != "zeitfenster"} for lauf_ in laeufe]
        return bericht

    # --- die drei Vergleichsebenen
    signal_gleich = len({l["signal_fp"] for l in laeufe}) == 1
    ausgefuehrt_gleich = len({l["ausgefuehrt_fp"] for l in laeufe}) == 1
    pfad_gleich = len({l["kapitalpfad_fp"] for l in laeufe}) == 1

    # --- umstrittene Trades: dieselbe Definition wie in
    #     research/order_sensitivity (always/never/contested), nur ueber
    #     Multimengen statt Zeilenindizes, weil der Trade-Satz je Permutation
    #     neu entsteht.
    signal_zaehler = zaehlwerk(laeufe[0]["signal_schluessel"])
    ausgefuehrt_je_lauf = [zaehlwerk(l["ausgefuehrt_schluessel"]) for l in laeufe]

    immer = nie = umstritten = 0
    for schluessel, vorhanden in signal_zaehler.items():
        counts = [z.get(schluessel, 0) for z in ausgefuehrt_je_lauf]
        kleinste, groesste = min(counts), max(counts)
        immer += kleinste
        nie += vorhanden - groesste
        umstritten += groesste - kleinste
    gesamt = sum(signal_zaehler.values())

    bericht["vergleich"] = {
        "signalmenge_identisch": signal_gleich,
        "ausgefuehrte_trades_identisch": ausgefuehrt_gleich,
        "kapitalpfad_identisch": pfad_gleich,
        "verschiedene_signalmengen": len({l["signal_fp"] for l in laeufe}),
        "verschiedene_ausfuehrungsmengen": len({l["ausgefuehrt_fp"] for l in laeufe}),
        "verschiedene_kapitalpfade": len({l["kapitalpfad_fp"] for l in laeufe}),
    }
    bericht["umstrittene_trades"] = {
        "trades_gesamt": gesamt,
        "immer_ausgefuehrt": immer,
        "nie_ausgefuehrt": nie,
        "umstritten": umstritten,
        "anteil_pct": round(umstritten / gesamt * 100, 1) if gesamt else 0.0,
        "hinweis": ("nur aussagekraeftig, solange die Signalmenge identisch ist"
                    if signal_gleich else
                    "die Signalmenge selbst schwankt - diese Zahl unterschaetzt den Effekt"),
    }
    bericht["streuung"] = {
        "rendite_pct": _spanne([l["rendite_pct"] for l in laeufe]),
        "max_drawdown_pct": _spanne([l["max_drawdown_pct"] for l in laeufe]),
        "trades_ausgefuehrt": _spanne([float(l["trades_ausgefuehrt"])
                                        for l in laeufe if l["trades_ausgefuehrt"] is not None]),
        "trades_uebersprungen": _spanne([float(l["trades_uebersprungen"])
                                          for l in laeufe if l["trades_uebersprungen"] is not None]),
    }
    bericht["laufzeit"] = {
        "erster_lauf_s": laeufe[0]["dauer_s"],
        "gesamt_s": round(sum(l["dauer_s"] for l in laeufe), 1),
    }

    # --- Bindet das Positionslimit ueberhaupt? Ein Bot, bei dem es nie
    #     bindet, kann diesen Fehler aus dieser Quelle gar nicht haben.
    limit = bericht["konfiguration"]["max_concurrent_positions"]
    fenster = laeufe[0]["zeitfenster"]
    analysen = [limitanalyse(fenster, z, limit) for z in ausgefuehrt_je_lauf]
    bericht["positionslimit"] = {
        "limit": limit,
        "gleichzeitig_offen_max": max(a["gleichzeitig_offen_max"] for a in analysen),
        "gleichzeitig_offen_min": min(a["gleichzeitig_offen_max"] for a in analysen),
        "limit_erreicht_in_laeufen": sum(1 for a in analysen if a["limit_erreicht"]),
        "laeufe": len(analysen),
        "zeitpunkte_am_limit_min": min(a["zeitpunkte_am_limit"] for a in analysen),
        "zeitpunkte_am_limit_max": max(a["zeitpunkte_am_limit"] for a in analysen),
        "kapitalschranke": kapitalschranke(
            bericht["konfiguration"]["allocation_pct"], limit),
    }

    # --- Urteil. Leitkriterium ist die Menge der ausgefuehrten Trades.
    #     Ein reiner Reihenfolgeunterschied im Kapitalpfad bei identischer
    #     Ausfuehrungsmenge ist ein eigener, schwaecherer Befund: dieselben
    #     Trades, nur anders abgerechnet - das aendert die Zwischenstaende der
    #     Kurve und damit den Drawdown, nicht aber, WER gehandelt wurde.
    if not signal_gleich:
        bericht["urteil"] = "NICHT DETERMINISTISCH"
        bericht["ursache"] = "Signalerzeugung (symboluebergreifender Zustand)"
    elif not ausgefuehrt_gleich:
        bericht["urteil"] = "NICHT DETERMINISTISCH"
        bericht["ursache"] = "Zuteilung: andere Trades bekommen das Kapital"
    elif not pfad_gleich:
        bericht["urteil"] = "NUR REIHENFOLGE"
        bericht["ursache"] = ("dieselben Trades, andere Abrechnungsreihenfolge "
                              "bei gleichem Zeitstempel")
    else:
        bericht["urteil"] = "DETERMINISTISCH"
        bericht["ursache"] = None

    bericht["laeufe"] = [{k: v for k, v in l.items()
                          if not k.endswith("_schluessel") and k != "zeitfenster"} for l in laeufe]
    return bericht


# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Permutiert die Symbolreihenfolge EINES Bots und "
                    "vergleicht die Backtest-Ergebnisse.")
    zerleger.add_argument("bot")
    zerleger.add_argument("--perms", type=int, default=20)
    zerleger.add_argument("--seed", type=int, default=20260913)
    zerleger.add_argument("--pruef-laeufe", type=int, default=2,
                          help="so viele Wiederholungen werden trotz "
                               "Zwischenspeicher voll nachgerechnet")
    zerleger.add_argument("--voll", action="store_true",
                          help="Zwischenspeicher ganz abschalten")
    zerleger.add_argument("--json", metavar="PFAD", default=None)
    zerleger.add_argument("--basis", metavar="ORDNER", default=None,
                          help="andere Projektwurzel (fuer die Selbsttests)")
    args = zerleger.parse_args(argv)

    ziel = tempfile.mkdtemp(prefix=f"determinismus_{args.bot}_")
    bericht = lauf(args.bot, args.perms, args.seed, args.pruef_laeufe,
                   args.voll, ziel, args.basis)

    if args.json:
        with open(args.json, "w") as f:
            json.dump(bericht, f, indent=2, default=str)

    print(META_PREFIX + json.dumps(bericht, default=str))
    return 0 if bericht.get("urteil") == "DETERMINISTISCH" else 1


if __name__ == "__main__":
    sys.exit(main())
