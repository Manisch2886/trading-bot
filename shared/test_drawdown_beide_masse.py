"""
Selbsttests: beide Drawdown-Masse in multi_symbol_optimise.py
==============================================================================
Geprueft wird das VERHALTEN der neun `multi_symbol_optimise.py`, nicht das
Vorhandensein von Codestuecken.

DIE EIGENTLICHE ZUSICHERUNG (Abschnitt 1)
------------------------------------------------------------------------------
`evaluate_combination_multi` weist seit TB-18 zusaetzlich den Drawdown auf der
CHRONOLOGISCHEN Reihenfolge aus (`max_drawdown_chronologisch_pct`). Der
bisherige Wert (`max_drawdown_pct`, gerechnet auf der Reihenfolge der
aneinandergehaengten Symbol-Bloecke), der `robustness_score` und die Rangfolge
duerfen sich dadurch NICHT aendern - sonst waeren alle frueheren Scores
untereinander unvergleichbar (research/drawdown_reihenfolge/BERICHT.md).

Der Nachweis laeuft ueber den ABLAUF, nicht ueber den Diff und nicht ueber
eine von Hand hingeschriebene Erwartung: derselbe Bot bewertet zweimal
dieselbe Trade-Menge - einmal mit den urspruenglichen `entry_time`-Werten,
einmal mit denselben Zeitstempeln, nur anders auf die Zeilen verteilt. PnL,
Zeilenreihenfolge und Trade-Zahl sind in beiden Laeufen identisch. Das alte
Mass hat `entry_time` nie gesehen; also muessen `robustness_score`,
`max_drawdown_pct` und die gesamte Rangfolge in beiden Laeufen Zeile fuer
Zeile gleich sein - waehrend sich der neue Wert nachweislich unterscheidet.
Das laeuft fuer ALLE NEUN Bots.

Zwei wiederkehrende Fallen aus #73, #77, #78, #79, #81, #86 und TB-15 sind
bewusst umgangen:

**Falle 1 - die selbstbestaetigende Probe.** Nirgends wird ein Ergebnis von
Hand hingeschrieben und anschliessend wiedererkannt. Die Vergleichswerte
entstehen entweder aus einem ZWEITEN Lauf desselben Bots (Abschnitt 1), aus
einer unabhaengigen Gegenrechnung in reinem Python ohne pandas
(`drawdown_referenz`, Abschnitt 2/3), aus einer von Hand herleitbaren
Konstruktion (Abschnitt 2: -14 gegen -24) oder aus den fertigen
Ergebnisdateien von `research/drawdown_reihenfolge/` (Abschnitt 5, echte
Kursdaten). Abschnitt 4 geht einen Schritt weiter und beobachtet den Ablauf
an MUTIERTEN Kopien der neun Dateien: jede Wache wird einzeln entfernt, und
die zugehoerige Pruefung MUSS dann anschlagen.

**Falle 2 - die zweite Wache verdeckt das Fehlen der ersten.** Die drei
Zusicherungen sind so getrennt, dass je nur eine greifen kann:
  * Abschnitt 2 (Gleichstaende ausgeschlossen, Zeiten quer zur
    Blockreihenfolge) faellt schon dann durch, wenn gar nicht sortiert wird -
    er sagt aber nichts ueber Gleichstaende.
  * Abschnitt 3 (ALLE Trades auf demselben Zeitstempel) kann nur ueber die
    stabile Sortierung bestehen; eine Sortierung ohne `kind="stable"`
    vertauscht die Gleichstaende und liefert einen anderen Wert. Dass die
    Reihenfolge innerhalb der Gleichstaende ueberhaupt etwas aendert, weist
    die Pruefung selbst nach, statt es vorauszusetzen.
  * Abschnitt 1 faellt nur durch, wenn der bestehende Wert an `entry_time`
    haengt - die Falle, um die es in TB-18 geht.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Ein Prozess je Bot: die neun Bots haben gleichnamige, inhaltlich verschiedene
Module (`multi_symbol_optimise.py`, `backtest_elliott.py`, ...). Zwei davon im
selben Prozess zu importieren, wuerde ueber `sys.modules` still den falschen
Bot laden.

Dieser Test veraendert nichts im Repo: die Bot-Dateien werden als BIBLIOTHEK
eingebunden (der `__main__`-Block, der
`results/<bot>/multi_symbol_optimisation_results.csv` ueberschreiben wuerde,
laeuft nie), die Mutationen entstehen ausschliesslich in Kopien unter
`/tmp`. Abschnitt 6 weist das per `git status` nach.

Nutzung:
    python3 shared/test_drawdown_beide_masse.py               # alles
    python3 shared/test_drawdown_beide_masse.py --ohne-kursdaten
    python3 shared/test_drawdown_beide_masse.py --bot <name>  # ein Bot (intern)
"""

import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import types
import zlib

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)
RESEARCH_RESULTS = os.path.join(BASE_DIR, "research", "drawdown_reihenfolge", "results")

# Reihenfolge wie in CLAUDE.md (Krypto zuerst, dann Aktien)
BOTS = (
    "elliott_wave",
    "t3_supertrend",
    "rsi2_crypto",
    "turtle_soup_crypto",
    "volatility_breakout_crypto",
    "elliott_wave_stocks",
    "rsi2_mean_reversion",
    "turtle_soup_stocks",
    "volatility_breakout",
)

# Kerzen-Intervall der jeweiligen Bot-CSV-Dateien in data/ (fuer die Stubs der
# Abruf-Module, die in dieser Umgebung nicht vorhanden sind).
INTERVAL = {
    "elliott_wave": "1h",
    "t3_supertrend": "4h",
    "rsi2_crypto": "1d",
    "turtle_soup_crypto": "1d",
    "volatility_breakout_crypto": "1d",
    "elliott_wave_stocks": "1d",
    "rsi2_mean_reversion": "1d",
    "turtle_soup_stocks": "1d",
    "volatility_breakout": "1d",
}

# Die Ankerkombination der Untersuchung (BERICHT.md, Frage 1): -82,50 %
# Blockreihenfolge gegen -259,86 % chronologisch. Fuer die uebrigen Bots
# waehlt der Test die erste Kombination des Rasters, die den Mindestfilter
# des Bots besteht - eine feste Wahl, aber keine abgeschriebene Zahl.
ANKER_LABEL = {"elliott_wave_stocks": "dev 5.0 % / Stop 3.0 % / kein Ziel"}

NEUE_SPALTE = "max_drawdown_chronologisch_pct"


# ===========================================================================
# Unabhaengige Gegenrechnung - bewusst ohne pandas
# ===========================================================================
def drawdown_referenz(pnls) -> float:
    """Groesster Rueckgang der kumulierten PnL-Summe, in reinem Python.

    Bewusst NICHT ueber cumsum()/cummax() - sonst waere die Gegenprobe
    dieselbe Kette, die geprueft werden soll."""
    lauf = 0.0
    hoch = None
    tief = 0.0
    for p in pnls:
        lauf += p
        if hoch is None or lauf > hoch:
            hoch = lauf
        if lauf - hoch < tief:
            tief = lauf - hoch
    return tief


def chronologisch_stabil(zeiten, pnls) -> list:
    """PnL-Werte in chronologischer Reihenfolge; bei gleichen Zeitstempeln
    bleibt die urspruengliche Reihenfolge erhalten (das ist genau die
    Bedeutung von kind="stable")."""
    ordnung = sorted(range(len(pnls)), key=lambda i: (zeiten[i], i))
    return [pnls[i] for i in ordnung]


# ===========================================================================
# Kindprozess: Umgebung fuer GENAU EINEN Bot
# ===========================================================================
def _boom(*_a, **_kw):
    raise AssertionError("Stub aufgerufen - dieser Test darf keine Kursdaten abrufen.")


def bot_umgebung(bot: str, botdir: str):
    """Setzt sys.path auf genau einen Bot, legt Stubs fuer die Module an, die
    hier nicht vorhanden sind bzw. Zugangsdaten enthalten (CLAUDE.md:
    config/email_config.py und shared/fetch_binance_data.py liegen bewusst
    nicht im Repo), und liefert das importierte multi_symbol_optimise."""
    sys.path.insert(0, _SHARED)
    sys.path.insert(0, botdir)

    for name in ("fetch_binance_data", "fetch_stock_data", "fetch_multi_data",
                 "fetch_4h_data", "yfinance"):
        mod = types.ModuleType(name)
        mod.INTERVAL = INTERVAL[bot]
        mod.fetch_historical_data = _boom
        mod.fetch_all_symbols = _boom
        mod.download = _boom
        mod.Ticker = _boom
        sys.modules.setdefault(name, mod)

    binance = types.ModuleType("binance")
    client = types.ModuleType("binance.client")

    class _FakeClient:
        KLINE_INTERVAL_1HOUR = "1h"
        KLINE_INTERVAL_4HOUR = "4h"
        KLINE_INTERVAL_1DAY = "1d"

    client.Client = _FakeClient
    binance.client = client
    sys.modules.setdefault("binance", binance)
    sys.modules.setdefault("binance.client", client)

    import importlib
    mo = importlib.import_module("multi_symbol_optimise")
    # Fuer die Rueckkehr zur echten Trade-Quelle nach den synthetischen
    # Abschnitten - Abschnitt 5 rechnet mit echten Kursdaten und darf den
    # untergeschobenen Stub nicht mehr sehen.
    mo._echte_trade_quelle = mo.get_trades_for_symbol
    return mo


# ---------------------------------------------------------------------------
# Synthetische Trade-Mengen
# ---------------------------------------------------------------------------
def _erwartet_tupel(mo) -> bool:
    """Drei Aktien-Bots reichen ihre Daten als (df_ind, entry_cutoff) durch.
    Aus dem Quelltext des Bots gelesen statt in einer Tabelle gefuehrt - ein
    Wert, eine Quelle."""
    import inspect
    return "for symbol, (" in inspect.getsource(mo.evaluate_combination_multi)


def probe_daten(mo, symbole: list) -> dict:
    """all_data in der Form, die der jeweilige Bot erwartet. Der Wert ist nur
    eine Marke: die Trades kommen aus dem untergeschobenen
    get_trades_for_symbol, nicht aus Kursdaten."""
    if _erwartet_tupel(mo):
        return {s: (s, None) for s in symbole}
    return {s: s for s in symbole}


def _marke_zu_symbol(marke):
    return marke[0] if isinstance(marke, tuple) else marke


def stub_setzen(mo, bauen):
    """Ersetzt die Trade-Quelle des Bots. `bauen(symbol, kombi_schluessel)`
    liefert den DataFrame. Alles andere - Zusammenfuegen, Mindestfilter,
    Kennzahlen, Score, Rangfolge - bleibt der Code des Bots."""
    def stub(marke, *rest, **kw):
        return bauen(_marke_zu_symbol(marke), repr(rest) + repr(sorted(kw.items())))
    mo.get_trades_for_symbol = stub
    # TB-105 (Register 11.1): bis dahin hielten die Proben den Regimefilter von
    # t3_supertrend fern, indem BTCUSDT in den Probedaten FEHLTE - der Bot
    # uebersprang ihn dann still. Seit dem Einbau der Regimewache bricht er
    # dort ab. Der Filter wird fuer die konstruierten Probedaten deshalb
    # AUSDRUECKLICH neutralisiert (Wache, Regime, Filter), statt sich auf das
    # stille Ueberspringen zu verlassen; `stub_loesen` stellt alle drei wieder
    # her, bevor Abschnitt 5 auf echten Kursdaten (mit BTCUSDT) rechnet.
    if hasattr(mo, "btc_daten"):
        if not hasattr(mo, "_echter_regimeteil"):
            mo._echter_regimeteil = (mo.btc_daten, mo.compute_btc_regime,
                                     mo.filter_trades_by_regime)
        mo.btc_daten = lambda *a, **kw: None
        mo.compute_btc_regime = lambda btc: None
        mo.filter_trades_by_regime = lambda trades, regime: trades


def stub_loesen(mo):
    """Stellt die echte Trade-Quelle des Bots wieder her (und, seit TB-105,
    den echten Regimeteil)."""
    mo.get_trades_for_symbol = mo._echte_trade_quelle
    if hasattr(mo, "_echter_regimeteil"):
        (mo.btc_daten, mo.compute_btc_regime,
         mo.filter_trades_by_regime) = mo._echter_regimeteil


def _frame(pd, zeiten, pnls, symbol):
    """Eine Trade-Menge mit den Spalten, die die neun Bots anfassen."""
    zt = pd.to_datetime(zeiten)
    return pd.DataFrame({
        "symbol": symbol,
        "entry_time": zt,
        "exit_time": zt,
        "entry_price": 100.0,
        "exit_price": 100.0,
        "pnl_pct": pnls,
        "holding_days": 3,
        "result": ["take_profit" if p > 0 else "stop_loss" for p in pnls],
    })


def breite_probe(pd, mo, zeiten_vertauscht: bool):
    """Eine realistisch grosse Trade-Menge: 25 Symbole, 12 Trades je Symbol,
    Zeitstempel ueber denselben Zeitraum - die Bloecke liegen also ineinander,
    genau der Fall, in dem sich beide Masse unterscheiden. Gross genug, um die
    Mindestfilter ALLER neun Bots ohne Zutun zu bestehen (bis zu 150 Trades,
    22 Symbole, 2,0 % Durchschnittsertrag); die Filter bleiben damit
    unangetastet."""
    symbole = [f"PROBE{i:02d}" for i in range(1, 26)]      # nie "BTCUSDT":
    # der Regimefilter von t3_supertrend wuerde die Trade-Menge selbst
    # veraendern und damit die Frage dieses Abschnitts ueberdecken. Seit
    # TB-105 haelt ihn `stub_setzen` ausdruecklich fern (die Regimewache
    # bricht bei fehlendem BTCUSDT ab, statt still zu ueberspringen).

    def bauen(symbol, kombi):
        rng = random.Random(zlib.crc32(f"{symbol}|{kombi}".encode()))
        n = 12
        pnls = [round(rng.uniform(-9.0, 15.0), 2) for _ in range(n)]
        pnls[0] = round(abs(pnls[0]) + 12.0, 2)            # Mittelwert sicher
        pnls[1] = round(abs(pnls[1]) + 12.0, 2)            # ueber 2,0 %
        tage = [rng.randrange(0, 900) for _ in range(n)]
        zeiten = [pd.Timestamp("2022-01-01") + pd.Timedelta(days=t) for t in tage]
        if zeiten_vertauscht:
            # DIESELBEN Zeitstempel, nur anders auf die Zeilen verteilt:
            # PnL, Reihenfolge und Anzahl bleiben Zeile fuer Zeile gleich.
            zeiten = zeiten[n // 2:] + zeiten[:n // 2]
        return _frame(pd, zeiten, pnls, symbol)

    stub_setzen(mo, bauen)
    return probe_daten(mo, symbole)


def _gelockert(mo):
    """Setzt NUR die Mindestfilter ausser Kraft - fuer die kleinen,
    konstruierten Faelle der Abschnitte 2 und 3, deren Trade-Zahl bewusst
    klein und deren Durchschnittsertrag bewusst negativ ist. An der
    Berechnung aendert das nichts; die Werte werden am Ende wieder
    zurueckgesetzt."""
    alt = {name: getattr(mo, name) for name in
           ("MIN_TRADES", "MIN_AVG_RETURN_PCT", "MIN_SYMBOLS_CONTRIBUTING")
           if hasattr(mo, name)}
    for name in alt:
        setattr(mo, name, -1_000_000 if name == "MIN_AVG_RETURN_PCT" else 0)
    return alt


def _zuruecksetzen(mo, alt: dict):
    for name, wert in alt.items():
        setattr(mo, name, wert)


def erste_zeile(mo, all_data):
    """Der Bot bewertet sein eigenes Raster; die untergeschobene Trade-Quelle
    liefert fuer jede Kombination dieselbe Menge, also ist jede Zeile
    dieselbe. Genommen wird die erste - so braucht dieser Test die
    Aufrufsignatur von evaluate_combination_multi nirgends nachzubilden."""
    df = mo.run_multi_optimisation(all_data)
    if df is None or df.empty:
        return None
    return df.iloc[0]


# ===========================================================================
# Die Pruefungen je Bot (laufen im Kindprozess)
# ===========================================================================
class Protokoll:
    def __init__(self, bot):
        self.bot = bot
        self.ok = 0
        self.fehler = []

    def pruefe(self, name, bedingung, hinweis=""):
        if bedingung:
            self.ok += 1
            print(f"  [OK ] {name}")
        else:
            self.fehler.append(name)
            print(f"  [FEHLER] {name}{(' - ' + hinweis) if hinweis else ''}")
        return bool(bedingung)


def _rangliste(df) -> list:
    """Die Rangfolge als Liste von Zeilen (ohne den neuen Wert). Fehlende
    Eintraege - `take_profit_fib` ist bei "kein Ziel" leer - werden zu einer
    Marke: NaN ist nie gleich NaN, der Vergleich schluege sonst auch bei zwei
    identischen Tabellen fehl."""
    spalten = [s for s in df.columns if s != NEUE_SPALTE]
    return [tuple("(leer)" if (isinstance(w, float) and w != w) else w for w in zeile)
            for zeile in df[spalten].itertuples(index=False, name=None)]


def abschnitt1_rangfolge(pd, mo, p: Protokoll):
    """Die eigentliche Zusicherung: der bestehende Wert und die Rangfolge
    haengen nicht an entry_time."""
    a = mo.run_multi_optimisation(breite_probe(pd, mo, False))
    b = mo.run_multi_optimisation(breite_probe(pd, mo, True))

    if not p.pruefe("Abschnitt 1: das Raster liefert ueberhaupt Ergebnisse",
                    a is not None and not a.empty and len(a) >= 3,
                    "Mindestfilter nicht bestanden - die Probe waere leer"):
        return
    if not p.pruefe("Abschnitt 1: die Rangfolge ist ueberhaupt unterscheidbar",
                    a["robustness_score"].nunique() >= 2,
                    "alle Scores gleich - ein Rangfolgevergleich sagte nichts"):
        return

    p.pruefe("Abschnitt 1: der neue Wert steht in der Ergebnistabelle",
             NEUE_SPALTE in a.columns)
    p.pruefe("Abschnitt 1: beide Masse unterscheiden sich hier ueberhaupt",
             NEUE_SPALTE in a.columns
             and bool((a[NEUE_SPALTE] != a["max_drawdown_pct"]).any()),
             "sonst koennte der neue Wert eine Kopie des alten sein")
    p.pruefe("Abschnitt 1: die vertauschten Zeitstempel aendern den neuen Wert",
             NEUE_SPALTE in a.columns
             and bool((a[NEUE_SPALTE].values != b[NEUE_SPALTE].values).any()),
             "sonst pruefte der Vergleich unten nichts")

    gemeinsam = [s for s in a.columns if s != NEUE_SPALTE]
    gleich = (list(a.columns) == list(b.columns)
              and a[gemeinsam].equals(b[gemeinsam]))
    p.pruefe("Abschnitt 1: robustness_score, max_drawdown_pct und JEDE andere "
             "Spalte sind in beiden Laeufen Zeile fuer Zeile gleich", gleich)

    p.pruefe("Abschnitt 1: die Rangfolge (Reihenfolge der Zeilen) ist identisch",
             _rangliste(a) == _rangliste(b))


# Der konstruierte Fall: zwei Symbole, je +10 / -6 / -6, die Zeiten der beiden
# Bloecke greifen ineinander.
#   Blockreihenfolge  : +10 -6 -6 | +10 -6 -6  -> kumuliert 10 4 -2 8 2 -4
#                       Hoechststand 10, tiefster Abstand  -> -14
#   chronologisch     : +10 +10 -6 -6 -6 -6     -> kumuliert 10 20 14 8 2 -4
#                       Hoechststand 20, tiefster Abstand  -> -24
KONSTRUIERT_BLOCK = -14.0
KONSTRUIERT_CHRONO = -24.0


def _konstruierte_probe(pd, mo, gleiche_zeit: bool, wiederholungen: int = 1):
    """Beide Symbole handeln abwechselnd (Symbol A am 1., 3., 5. Tag, Symbol B
    am 2., 4., 6.). `gleiche_zeit=True` setzt stattdessen ALLE Trades auf
    denselben Zeitstempel."""
    muster = [10.0, -6.0, -6.0] * wiederholungen
    # Symbol A handelt an ungeraden, Symbol B an geraden Tagen - die beiden
    # Bloecke greifen also ineinander, statt hintereinander zu liegen.
    tage = {"PROBE_A": [1 + 6 * k + 2 * i for k in range(wiederholungen) for i in range(3)],
            "PROBE_B": [2 + 6 * k + 2 * i for k in range(wiederholungen) for i in range(3)]}

    def bauen(symbol, _kombi):
        if gleiche_zeit:
            zeiten = [pd.Timestamp("2023-05-05 12:00:00")] * len(muster)
        else:
            zeiten = [pd.Timestamp("2023-05-01") + pd.Timedelta(days=t) for t in tage[symbol]]
        return _frame(pd, zeiten, list(muster), symbol)

    stub_setzen(mo, bauen)
    return probe_daten(mo, ["PROBE_A", "PROBE_B"]), muster, tage


def abschnitt2_wert(pd, mo, p: Protokoll):
    """Der neue Wert IST der Drawdown der chronologischen Reihenfolge."""
    all_data, muster, tage = _konstruierte_probe(pd, mo, gleiche_zeit=False)
    alt = _gelockert(mo)
    try:
        zeile = erste_zeile(mo, all_data)
    finally:
        _zuruecksetzen(mo, alt)

    if not p.pruefe("Abschnitt 2: der konstruierte Fall wird bewertet", zeile is not None):
        return

    # Unabhaengige Gegenrechnung in reinem Python, zusaetzlich zur von Hand
    # hergeleiteten Erwartung oben.
    block_pnls = list(muster) + list(muster)
    block_zeiten = tage["PROBE_A"] + tage["PROBE_B"]
    ref_block = round(drawdown_referenz(block_pnls), 2)
    ref_chrono = round(drawdown_referenz(chronologisch_stabil(block_zeiten, block_pnls)), 2)

    p.pruefe("Abschnitt 2: Gegenrechnung und Handrechnung stimmen ueberein",
             (ref_block, ref_chrono) == (KONSTRUIERT_BLOCK, KONSTRUIERT_CHRONO),
             f"{ref_block} / {ref_chrono}")
    p.pruefe("Abschnitt 2: beide Masse sind hier deutlich verschieden",
             abs(ref_block - ref_chrono) > 5.0)
    p.pruefe("Abschnitt 2: max_drawdown_pct ist weiterhin die Blockreihenfolge "
             f"({KONSTRUIERT_BLOCK})",
             float(zeile["max_drawdown_pct"]) == KONSTRUIERT_BLOCK,
             str(zeile["max_drawdown_pct"]))
    p.pruefe("Abschnitt 2: der neue Wert ist die chronologische Reihenfolge "
             f"({KONSTRUIERT_CHRONO})",
             NEUE_SPALTE in zeile.index
             and float(zeile[NEUE_SPALTE]) == KONSTRUIERT_CHRONO,
             str(zeile.get(NEUE_SPALTE)))


# Zweiter Gleichstand-Fall: drei Zeitstempel, davon zwei mehrfach belegt -
# die stabile Sortierung muss die Zeilen innerhalb jedes Zeitstempels in der
# Blockreihenfolge lassen.
GEMISCHT_TAGE = [3, 1, 1, 1, 2, 2] * 20
GEMISCHT_PNL = [4.0, -9.0, 6.0, -7.0, 3.0, -5.0] * 20


def abschnitt3_stabil(pd, mo, p: Protokoll):
    """Gleiche Zeitstempel: die Blockreihenfolge muss erhalten bleiben."""
    # 60 Trades je Symbol - deutlich mehr als die Schwelle, unterhalb derer
    # numpys Quicksort auf ein (stabiles) Einfuegeverfahren umschaltet. Sonst
    # koennte eine unstabile Sortierung hier zufaellig richtig liegen.
    all_data, muster, _ = _konstruierte_probe(pd, mo, gleiche_zeit=True,
                                              wiederholungen=20)
    alt = _gelockert(mo)
    try:
        zeilen = [erste_zeile(mo, all_data) for _ in range(3)]
    finally:
        _zuruecksetzen(mo, alt)

    if not p.pruefe("Abschnitt 3: der Gleichstand-Fall wird bewertet",
                    all(z is not None for z in zeilen)):
        return
    zeile = zeilen[0]

    # Nachweis, dass dieser Fall ueberhaupt unterscheidet: waere die
    # Reihenfolge innerhalb der Gleichstaende egal, pruefte der Vergleich
    # unten nichts.
    block_pnls = list(muster) + list(muster)
    andere = block_pnls[::2] + block_pnls[1::2]
    p.pruefe("Abschnitt 3: die Reihenfolge innerhalb der Gleichstaende "
             "aendert den Wert ueberhaupt",
             round(drawdown_referenz(block_pnls), 2)
             != round(drawdown_referenz(andere), 2))

    p.pruefe("Abschnitt 3: bei lauter gleichen Zeitstempeln bleibt die "
             "Blockreihenfolge erhalten (neuer Wert == alter Wert)",
             NEUE_SPALTE in zeile.index
             and float(zeile[NEUE_SPALTE]) == float(zeile["max_drawdown_pct"]),
             f"{zeile.get(NEUE_SPALTE)} gegen {zeile['max_drawdown_pct']}")
    p.pruefe("Abschnitt 3: wiederholte Laeufe liefern denselben Wert",
             len({float(z[NEUE_SPALTE]) for z in zeilen
                  if NEUE_SPALTE in z.index}) == 1)

    # Teilweise gleiche Zeitstempel: hier muss der Wert der Sortierung
    # entsprechen, die bei Gleichstand die urspruengliche Reihenfolge behaelt.
    # Tage und PnL stehen genau einmal (GEMISCHT_*): der Prueffall und seine
    # Erwartung duerfen nicht aus zwei getrennt gepflegten Listen kommen.
    def bauen(symbol, _kombi):
        zeiten = [pd.Timestamp("2023-05-01") + pd.Timedelta(days=t)
                  for t in GEMISCHT_TAGE]
        return _frame(pd, zeiten, list(GEMISCHT_PNL), symbol)

    stub_setzen(mo, bauen)
    all_data = probe_daten(mo, ["PROBE_A", "PROBE_B"])
    alt = _gelockert(mo)
    try:
        zeile = erste_zeile(mo, all_data)
    finally:
        _zuruecksetzen(mo, alt)

    # zwei Symbole, also zweimal derselbe Block hintereinander
    erwartet = round(drawdown_referenz(
        chronologisch_stabil(GEMISCHT_TAGE * 2, GEMISCHT_PNL * 2)), 2)
    p.pruefe("Abschnitt 3: teils gleiche Zeitstempel - der Wert entspricht der "
             "stabilen Sortierung",
             zeile is not None and NEUE_SPALTE in zeile.index
             and float(zeile[NEUE_SPALTE]) == erwartet,
             f"erwartet {erwartet}, erhalten {None if zeile is None else zeile.get(NEUE_SPALTE)}")


# ===========================================================================
# Abschnitt 5: Gegenprobe an echten Kursdaten
# ===========================================================================
def raster_kombinationen(bot: str, mo) -> list:
    """(Kombination, Beschriftung) - abgeleitet aus den RANGE-Konstanten des
    Bots selbst (ein Wert, eine Quelle) und beschriftet wie in
    research/drawdown_reihenfolge/adapters.py, damit sich die Zeilen der
    dortigen Ergebnisdateien zuordnen lassen."""
    out = []
    if bot == "elliott_wave":
        for d in mo.DEVIATION_RANGE:
            for s in mo.STOP_LOSS_RANGE:
                for f in mo.TAKE_PROFIT_FIB_RANGE:
                    out.append(((d, s, f), f"dev {d} % / Stop {s} % / Fib {f}"))
    elif bot == "elliott_wave_stocks":
        for d in mo.DEVIATION_RANGE:
            for s in mo.STOP_LOSS_RANGE:
                for f in mo.TAKE_PROFIT_FIB_RANGE:
                    out.append(((d, s, f, True), f"dev {d} % / Stop {s} % / Fib {f}"))
                out.append(((d, s, None, False), f"dev {d} % / Stop {s} % / kein Ziel"))
    elif bot == "t3_supertrend":
        for a in mo.T3_FAST_RANGE:
            for b in mo.T3_SLOW_RANGE:
                for c in mo.ADX_THRESHOLD_RANGE:
                    for d in mo.STOP_LOSS_RANGE:
                        if a < b:
                            out.append(((a, b, c, d), f"T3 {a}/{b} / ADX {c} / Stop {d} %"))
    elif bot == "rsi2_crypto":
        for sma in mo.SMA_TREND_RANGE:
            for rsi in mo.RSI_THRESHOLD_RANGE:
                for stop in mo.STOP_LOSS_RANGE:
                    out.append(((rsi, sma, stop), f"SMA {sma} / RSI {rsi} / Stop "
                                                  f"{stop if stop is not None else 'kein Stop'}"))
    elif bot == "rsi2_mean_reversion":
        for rsi in mo.RSI_THRESHOLD_RANGE:
            for stop in mo.STOP_LOSS_RANGE:
                out.append(((rsi, stop), f"RSI {rsi} / Stop "
                                         f"{stop if stop is not None else 'kein Stop'}"))
    elif bot in ("turtle_soup_crypto", "turtle_soup_stocks"):
        for periode in mo.DONCHIAN_PERIOD_RANGE:
            for modus in mo.STOP_MODE_RANGE:
                out.append(((periode, modus), f"Donchian {periode} / Stop "
                                              f"{modus if modus is not None else 'kein Stop'}"))
    elif bot in ("volatility_breakout", "volatility_breakout_crypto"):
        for stop in mo.STOP_LOSS_RANGE:
            out.append(((stop,), f"Stop {stop if stop is not None else 'kein Stop'}"))
    return out


def abschnitt5_kursdaten(pd, bot: str, mo, p: Protokoll):
    """Ein Wert je Bot gegen research/drawdown_reihenfolge/results/*.csv:
    dort steht `dd_bot` (das Mass, das der Bot heute rechnet), `score_bot`
    und `dd_entry` (chronologisch). Die Datei ist VOR dieser Aenderung
    entstanden - sie ist damit der Beleg, dass der alte Wert derselbe
    geblieben ist, und zugleich die Sollquelle fuer den neuen."""
    import csv
    pfad = os.path.join(RESEARCH_RESULTS, f"{bot}_raster.csv")
    if not os.path.exists(pfad):
        p.pruefe(f"Abschnitt 5: Ergebnisdatei {os.path.basename(pfad)} vorhanden", False)
        return
    raster = {z["label"]: z for z in csv.DictReader(open(pfad))}

    kombis = raster_kombinationen(bot, mo)
    p.pruefe("Abschnitt 5: das Raster des Bots deckt sich mit dem der "
             "Untersuchung", len(kombis) == len(raster),
             f"{len(kombis)} gegen {len(raster)}")

    gewaehlt = None
    if bot in ANKER_LABEL:
        gewaehlt = next((k for k in kombis if k[1] == ANKER_LABEL[bot]), None)
    if gewaehlt is None:
        gewaehlt = next((k for k in kombis
                         if raster.get(k[1], {}).get("besteht_mindestfilter") == "True"),
                        kombis[0] if kombis else None)
    if gewaehlt is None:
        p.pruefe("Abschnitt 5: eine Kombination gefunden", False)
        return

    combo, label = gewaehlt
    soll = raster[label]
    all_data = mo.load_all_symbol_data()
    p.pruefe(f"Abschnitt 5: Kursdaten geladen ({len(all_data)} Symbole)", bool(all_data))
    if not all_data:
        return

    res = mo.evaluate_combination_multi(all_data, *combo)
    if res is None:
        # Kombinationen, die den Mindestfilter des Bots nicht bestehen,
        # liefern None. Der Filter - und NUR er - wird dafuer kurz
        # ausgesetzt; gerechnet wird unveraendert.
        alt = _gelockert(mo)
        try:
            res = mo.evaluate_combination_multi(all_data, *combo)
        finally:
            _zuruecksetzen(mo, alt)
        print(f"  (Hinweis: {label} besteht den Mindestfilter nicht - "
              f"fuer den Zahlenvergleich kurz ausgesetzt)")

    if not p.pruefe(f"Abschnitt 5: {label} liefert ein Ergebnis", res is not None):
        return

    p.pruefe(f"Abschnitt 5: Trade-Zahl wie in der Untersuchung ({soll['num_trades']})",
             int(res["num_trades"]) == int(soll["num_trades"]), str(res["num_trades"]))
    p.pruefe(f"Abschnitt 5: max_drawdown_pct unveraendert ({soll['dd_bot']})",
             float(res["max_drawdown_pct"]) == float(soll["dd_bot"]),
             str(res["max_drawdown_pct"]))
    p.pruefe(f"Abschnitt 5: robustness_score unveraendert ({soll['score_bot']})",
             float(res["robustness_score"]) == float(soll["score_bot"]),
             str(res["robustness_score"]))
    p.pruefe(f"Abschnitt 5: neuer Wert wie die Untersuchung ihn ausweist "
             f"({soll['dd_entry']})",
             NEUE_SPALTE in res and float(res[NEUE_SPALTE]) == float(soll["dd_entry"]),
             str(res.get(NEUE_SPALTE)))


# ===========================================================================
# Kindprozess
# ===========================================================================
def kind(bot: str, botdir: str, mit_kursdaten: bool) -> int:
    mo = bot_umgebung(bot, botdir)
    import pandas as pd
    p = Protokoll(bot)
    print(f"\n--- {bot} ---")
    abschnitt1_rangfolge(pd, mo, p)
    abschnitt2_wert(pd, mo, p)
    abschnitt3_stabil(pd, mo, p)
    if mit_kursdaten:
        stub_loesen(mo)
        p.pruefe("Abschnitt 5: die echte Trade-Quelle des Bots ist wieder aktiv",
                 mo.get_trades_for_symbol is mo._echte_trade_quelle)
        abschnitt5_kursdaten(pd, bot, mo, p)
    print(f"ERGEBNIS {json.dumps({'bot': bot, 'ok': p.ok, 'fehler': p.fehler})}")
    return 1 if p.fehler else 0


# ===========================================================================
# Abschnitt 4: Mutationsproben
# ===========================================================================
# Jede Mutation entfernt genau eine Wache. Dahinter steht, welche Pruefung
# dann anschlagen MUSS - und zwar genau die, die diese Wache absichert.
MUTATIONEN = (
    ("ohne stabile Sortierung",
     'combined.sort_values("entry_time", kind="stable")',
     'combined.sort_values("entry_time")',
     "Abschnitt 3"),
    ("Score am chronologischen Wert",
     '"max_drawdown_pct": round(max_drawdown, 2),',
     '"max_drawdown_pct": round(max_drawdown_chrono, 2),',
     "Abschnitt 1"),
    ("bestehendes Mass still chronologisch sortiert",
     '    cum_returns = combined["pnl_pct"].cumsum()',
     '    combined = combined.sort_values("entry_time", kind="stable")\n'
     '    cum_returns = combined["pnl_pct"].cumsum()',
     "Abschnitt 1"),
)


def mutierter_botdir(bot: str, alt: str, neu: str, wurzel: str):
    """Kopiert den Bot-Ordner nach /tmp und veraendert dort - und nur dort -
    multi_symbol_optimise.py. Das Repo bleibt unberuehrt; die Kopie liegt
    unter <tmp>/strategies/<bot>, damit der Bot seine results/- und logs/-
    Ordner ebenfalls in /tmp anlegt."""
    ziel = os.path.join(wurzel, "strategies", bot)
    if os.path.exists(ziel):
        shutil.rmtree(ziel)
    shutil.copytree(os.path.join(BASE_DIR, "strategies", bot), ziel)
    pfad = os.path.join(ziel, "multi_symbol_optimise.py")
    text = open(pfad).read()
    if text.count(alt) != 1:
        return None
    open(pfad, "w").write(text.replace(alt, neu))
    return ziel


# ===========================================================================
# Hauptprozess
# ===========================================================================
def kurzfassung(getroffen: list) -> str:
    return getroffen[0][:60] + ("..." if len(getroffen[0]) > 60 else "")


def kind_starten(bot: str, botdir: str, mit_kursdaten: bool):
    ruf = [sys.executable, os.path.abspath(__file__), "--bot", bot, "--botdir", botdir]
    if not mit_kursdaten:
        ruf.append("--ohne-kursdaten")
    lauf = subprocess.run(ruf, capture_output=True, text=True)
    ergebnis = {"ok": 0, "fehler": ["Kindprozess ohne Ergebniszeile"]}
    for zeile in lauf.stdout.splitlines():
        if zeile.startswith("ERGEBNIS "):
            ergebnis = json.loads(zeile[len("ERGEBNIS "):])
    return lauf, ergebnis


# Was ein Testlauf ueberhaupt anfassen koennte: Bot-Code, Ergebnisdateien,
# Kursdaten, Logs und die Trade-Datenbanken.
BEOBACHTET = ("strategies/", "results/", "data/", "logs/", "paper_trading_")


def git_zustand() -> str:
    """`git status`, eingeschraenkt auf BEOBACHTET. Die Einschraenkung ist
    nicht Bequemlichkeit: ohne sie schlaegt die Pruefung auch an, wenn
    waehrend des Laufs anderswo im Repo eine Datei entsteht (etwa ein
    Dokument) - und behauptete damit etwas, das sie nicht gemessen hat."""
    lauf = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR,
                          capture_output=True, text=True)
    zeilen = [z for z in lauf.stdout.splitlines()
              if z[3:].strip('"').startswith(BEOBACHTET)]
    return "\n".join(sorted(zeilen))


def main(mit_kursdaten: bool) -> int:
    print("=" * 78)
    print("Selbsttests: beide Drawdown-Masse in multi_symbol_optimise.py")
    print("=" * 78)
    vorher = git_zustand()

    ok_gesamt = 0
    fehler_gesamt = []

    for bot in BOTS:
        lauf, ergebnis = kind_starten(bot, os.path.join(BASE_DIR, "strategies", bot),
                                      mit_kursdaten)
        for zeile in lauf.stdout.splitlines():
            if not zeile.startswith("ERGEBNIS "):
                print(zeile)
        if lauf.returncode != 0:
            print(lauf.stderr[-2000:])
            if not ergebnis["fehler"]:
                ergebnis["fehler"] = ["Kindprozess brach ab"]
        ok_gesamt += ergebnis["ok"]
        fehler_gesamt += [f"{bot}: {n}" for n in ergebnis["fehler"]]

    # --- Abschnitt 4: Mutationsproben --------------------------------------
    print("\n--- Abschnitt 4: Mutationsproben (je Bot, in Kopien unter /tmp) ---")
    with tempfile.TemporaryDirectory(prefix="drawdown_mutation_") as wurzel:
        for bot in BOTS:
            for name, alt, neu, erwartet in MUTATIONEN:
                ziel = mutierter_botdir(bot, alt, neu, wurzel)
                if ziel is None:
                    fehler_gesamt.append(f"{bot}: Mutation '{name}' nicht anwendbar")
                    print(f"  [FEHLER] {bot}: Mutation '{name}' liess sich nicht "
                          f"anwenden - steht die Wache hier ueberhaupt?")
                    continue
                _lauf, ergebnis = kind_starten(bot, ziel, False)
                getroffen = [f for f in ergebnis["fehler"] if f.startswith(erwartet)]
                if getroffen:
                    ok_gesamt += 1
                    print(f"  [OK ] {bot}: Mutation '{name}' -> {kurzfassung(getroffen)}")
                else:
                    fehler_gesamt.append(f"{bot}: Mutation '{name}' blieb unbemerkt")
                    print(f"  [FEHLER] {bot}: Mutation '{name}' blieb unbemerkt "
                          f"(erwartet war ein Fehlschlag in {erwartet})")

    # --- Abschnitt 6: der Test veraendert nichts ---------------------------
    print("\n--- Abschnitt 6: Folgenlosigkeit ---")
    if vorher == git_zustand():
        ok_gesamt += 1
        print("  [OK ] Bot-Code, Ergebnisdateien, Kursdaten, Logs und "
              "Datenbanken sind unveraendert")
    else:
        fehler_gesamt.append("der Testlauf hat Dateien im Repo veraendert")
        print("  [FEHLER] der Testlauf hat Dateien im Repo veraendert")

    print("\n" + "=" * 78)
    gesamt = ok_gesamt + len(fehler_gesamt)
    print(f"{ok_gesamt} von {gesamt} Pruefungen bestanden, {len(fehler_gesamt)} fehlgeschlagen.")
    for name in fehler_gesamt:
        print(f"  - {name}")
    return 1 if fehler_gesamt else 0


if __name__ == "__main__":
    argumente = sys.argv[1:]
    mit_kursdaten = "--ohne-kursdaten" not in argumente
    if "--bot" in argumente:
        bot = argumente[argumente.index("--bot") + 1]
        botdir = (argumente[argumente.index("--botdir") + 1] if "--botdir" in argumente
                  else os.path.join(BASE_DIR, "strategies", bot))
        sys.exit(kind(bot, botdir, mit_kursdaten))
    sys.exit(main(mit_kursdaten))
