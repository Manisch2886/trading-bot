"""
Korrigierte Kapitalkurven-Grundlage (Nachtrag zum Sync-Check)
====================================================================================
Der Sync-Check (PR #24) hat belegt: bei 5 der 9 Bots weicht die Konfiguration
in `equity_simulation.py` von der tatsaechlichen Live-Konfiguration in
`live_params.py` ab. Die Dateien `results/<bot>/equity_curve.csv` sind die
Ausgabe genau dieser `equity_simulation.py`-Laeufe - sie beruhen also bei
fuenf Bots nicht auf der Live-Konfiguration.

Diese Studie baut ihre Portfolio-Kurve ueber die unveraenderten Funktionen
`shared/portfolio_overview.py::discover_bots` / `load_all_curves` auf eben
diesen CSVs auf und ist damit betroffen. Dieses Modul erzeugt eine
KORRIGIERTE Kopie aller neun Kurven und stellt sie der Studie bereit.

--------------------------------------------------------------------
Was NICHT veraendert wird
--------------------------------------------------------------------
* `shared/portfolio_overview.py` bleibt unangetastet. Die Kurven werden ueber
  seine UNVERAENDERTEN Funktionen geladen - nur die Pfade, aus denen es
  liest, werden vorher umgebogen (`load_corrected_curves`).
* `results/<bot>/equity_curve.csv` bleibt unangetastet. Die korrigierten
  Kurven landen in einem eigenen Unterverzeichnis dieser Studie.
* Kein Bot-Code wird veraendert. Jede Kurve entsteht aus einem Aufruf der
  bot-eigenen, unveraenderten `collect_all_trades` / `simulate_portfolio`
  (und bei volatility_breakout_crypto zusaetzlich `regime_filter`) - nur mit
  den Werten aus `live_params.py` statt denen aus `equity_simulation.py`.

--------------------------------------------------------------------
Herkunft der Fallunterscheidung
--------------------------------------------------------------------
Die Variantenbildung je Bot ist eine dokumentierte UEBERNAHME aus
`research/sync_check/impact.py::build` (PR #24). Sie wird hier nicht neu
erfunden, weil sonst still eine zweite, abweichende Definition von
"Live-Konfiguration" entstuende.

Dass die Uebernahme stimmt, wird geprueft statt behauptet - zweifach:

  1. Die VIER synchronen Bots werden mitgerechnet, obwohl sich bei ihnen
     nichts aendern kann. Ihre erzeugte Kurve muss der bestehenden
     `results/`-Datei BYTEWEISE entsprechen. Faellt dieser Vergleich durch,
     ist der Erzeuger falsch - und nicht etwa die Korrektur wirksam.
  2. Die FUENF abweichenden Bots muessen die im Sync-Check
     veroeffentlichten Kennzahlen der Live-Variante exakt treffen.

Ein eigener Subprozess je Bot: alle 9 Bots haben gleichnamige, inhaltlich
verschiedene Module (`equity_simulation.py`, `live_params.py`); ein direkter
Import mehrerer Bots im selben Prozess wuerde ueber `sys.modules` still den
falschen Bot laden.
"""

import hashlib
import json
import os
import subprocess
import sys

import pandas as pd

# Die fuenf Bots, deren equity_simulation.py von live_params.py abweicht
# (research/sync_check/BERICHT.md, Schritt 1).
DIVERGENT_BOTS = (
    "elliott_wave_stocks",         # USE_TAKE_PROFIT True vs. live False
    "rsi2_mean_reversion",         # 10 % / 8  vs. live 5 % / 20
    "turtle_soup_stocks",          # 10 % / 8  vs. live 2 % / unbegrenzt
    "volatility_breakout",         # Limit 8   vs. live 15
    "volatility_breakout_crypto",  # BTC-Regimefilter fehlt im Backtest
)

# Die vier synchronen Bots - Regressionsprobe, siehe Modul-Kopf.
CLEAN_BOTS = ("elliott_wave", "t3_supertrend", "rsi2_crypto", "turtle_soup_crypto")

ALL_BOTS = tuple(sorted(DIVERGENT_BOTS + CLEAN_BOTS))

# --- Eigenstaendiger Nebenfund dieses Nachtrags -----------------------------
# `elliott_wave` ist konfigurationsseitig SYNCHRON, seine gespeicherte Kurve
# stimmt trotzdem nicht mit dem heutigen Code ueberein: results/equity_curve.csv
# stammt aus dem Initial Commit und deckt 5 Symbole / 144 Trades ab, waehrend
# die heutige equity_simulation.py auf demselben Universum 782 ausgefuehrte
# Trades ueber 18 Symbole erzeugt (und bis 2026-08-26 statt 2026-06-27 reicht).
# Das ist KEINE Folge der Sync-Abweichung, sondern eine davon unabhaengige
# Veralterung - und sie trifft dieselbe Datengrundlage.
#
# Deshalb wird dieser Bot NICHT stillschweigend mitkorrigiert: die primaere
# Auswertung tauscht auftragsgemaess nur die fuenf abweichenden Bots
# (siehe SWAP_PRIMARY), eine zweite Auswertung nimmt ihn zusaetzlich dazu
# (SWAP_WITH_STALE). So bleibt trennbar, welcher Effekt woher kommt.
KNOWN_STALE_BOTS = ("elliott_wave",)

SWAP_PRIMARY = DIVERGENT_BOTS
SWAP_WITH_STALE = tuple(sorted(DIVERGENT_BOTS + KNOWN_STALE_BOTS))

# Im Sync-Check (PR #24) veroeffentlichte Kennzahlen der LIVE-Variante.
SYNC_CHECK_REFERENCE = {
    "elliott_wave_stocks":        {"executed": 288,  "return_pct": 3084.09, "drawdown_pct": -9.79},
    "volatility_breakout":        {"executed": 1454, "return_pct": 224.41,  "drawdown_pct": -23.97},
    "turtle_soup_stocks":         {"executed": 8915, "return_pct": 145.59,  "drawdown_pct": -29.91},
    "rsi2_mean_reversion":        {"executed": 4232, "return_pct": 36.75,   "drawdown_pct": -21.05},
    "volatility_breakout_crypto": {"executed": 207,  "return_pct": 49.03,   "drawdown_pct": -16.29},
}

TOL = 0.011   # veroeffentlichte Werte sind auf 2 Nachkommastellen gerundet


# --- Der je Bot in einem eigenen Prozess ausgefuehrte Erzeuger ---------------
_WORKER = r'''
import json, sys, types
import pandas as pd

# Stubs fuer nicht installierte bzw. zugangsdatenbehaftete Importe (CLAUDE.md).
# Werden nie aufgerufen - gelesen werden ausschliesslich die lokalen CSVs in data/.
for _name in ("fetch_binance_data", "yfinance"):
    _m = types.ModuleType(_name)
    _m.fetch_historical_data = lambda *a, **kw: pd.DataFrame()
    _m.download = lambda *a, **kw: pd.DataFrame()
    _m.Ticker = lambda *a, **kw: None
    sys.modules.setdefault(_name, _m)
_b, _c = types.ModuleType("binance"), types.ModuleType("binance.client")
class _FakeClient:
    KLINE_INTERVAL_1HOUR = "1h"; KLINE_INTERVAL_4HOUR = "4h"; KLINE_INTERVAL_1DAY = "1d"
_c.Client = _FakeClient; _b.client = _c
sys.modules.setdefault("binance", _b); sys.modules.setdefault("binance.client", _c)

BOT, OUT_CSV, OUT_JSON = sys.argv[1], sys.argv[2], sys.argv[3]

import equity_simulation as es
import live_params as lp

all_data = es.load_all_symbol_data()
note = {}

# ---------------------------------------------------------------------------
# ABWEICHENDE BOTS: Trade-Satz und/oder Kapitalparameter aus live_params.py.
# Woertliche Uebernahme aus research/sync_check/impact.py::build (Variante
# "live"). ALLOCATION_PCT steht live in PROZENT, im Backtest als ANTEIL.
# ---------------------------------------------------------------------------
if BOT == "elliott_wave_stocks":
    trades = es.collect_all_trades(all_data, es.DEVIATION_PCT, es.STOP_LOSS_PCT,
                                    es.TAKE_PROFIT_FIB, lp.USE_TAKE_PROFIT)
    allocation = es.ALLOCATION_PCT   # live_params.py dokumentiert hier keine Allokation
    limit = lp.MAX_CONCURRENT_POSITIONS
    note = {"USE_TAKE_PROFIT": lp.USE_TAKE_PROFIT}

elif BOT == "volatility_breakout_crypto":
    trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT)
    note = {"BTC_REGIME_FILTER_ENABLED": False}
    if getattr(lp, "BTC_REGIME_FILTER_ENABLED", False):
        # Die unveraenderten Regimefilter-Funktionen des Bots - dieselben,
        # die forward_test.py live benutzt.
        from regime_filter import compute_btc_regime, filter_trades_by_regime
        btc = all_data.get("BTCUSDT")
        if btc is None:
            raise SystemExit("BTCUSDT fehlt - Regimefilter nicht anwendbar")
        trades = filter_trades_by_regime(trades, compute_btc_regime(btc))
        note = {"BTC_REGIME_FILTER_ENABLED": True}
    allocation = lp.ALLOCATION_PCT / 100.0
    limit = lp.MAX_CONCURRENT_POSITIONS

elif BOT == "rsi2_mean_reversion":
    trades = es.collect_all_trades(all_data, es.RSI_THRESHOLD, es.STOP_LOSS_PCT)
    allocation = lp.ALLOCATION_PCT / 100.0
    limit = lp.MAX_CONCURRENT_POSITIONS

elif BOT == "turtle_soup_stocks":
    trades = es.collect_all_trades(all_data, es.DONCHIAN_PERIOD, es.STOP_MODE)
    allocation = lp.ALLOCATION_PCT / 100.0
    limit = lp.MAX_CONCURRENT_POSITIONS

elif BOT == "volatility_breakout":
    trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT)
    allocation = lp.ALLOCATION_PCT / 100.0
    limit = lp.MAX_CONCURRENT_POSITIONS

# ---------------------------------------------------------------------------
# SYNCHRONE BOTS: es gibt keine abweichende Live-Konfiguration. Sie werden
# mit den Modul-Konstanten ihrer EIGENEN equity_simulation.py gerechnet -
# also woertlich so, wie deren __main__-Block die bestehende results/-Kurve
# erzeugt hat. Genau deshalb taugen sie als Regressionsprobe.
# ---------------------------------------------------------------------------
elif BOT == "elliott_wave":
    trades = es.collect_all_trades(all_data, es.DEVIATION_PCT, es.STOP_LOSS_PCT, es.TAKE_PROFIT_FIB)
    allocation, limit = es.ALLOCATION_PCT, None

elif BOT == "t3_supertrend":
    trades = es.collect_all_trades(all_data, es.T3_FAST, es.T3_SLOW, es.ADX_THRESHOLD, es.STOP_LOSS_PCT)
    allocation, limit = es.ALLOCATION_PCT, es.MAX_CONCURRENT_POSITIONS

elif BOT == "rsi2_crypto":
    trades = es.collect_all_trades(all_data, es.RSI_THRESHOLD, es.SMA_TREND_PERIOD, es.STOP_LOSS_PCT)
    allocation, limit = es.ALLOCATION_PCT, es.MAX_CONCURRENT_POSITIONS

elif BOT == "turtle_soup_crypto":
    trades = es.collect_all_trades(all_data, es.DONCHIAN_PERIOD, es.STOP_MODE)
    allocation, limit = es.ALLOCATION_PCT, es.MAX_CONCURRENT_POSITIONS

else:
    raise SystemExit(f"unbekannter Bot: {BOT}")

supports_limit = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
if supports_limit:
    result = es.simulate_portfolio(trades, es.STARTING_CAPITAL, allocation, limit)
else:
    result = es.simulate_portfolio(trades, es.STARTING_CAPITAL, allocation)

result["equity_curve"].to_csv(OUT_CSV, index=False)
total_return = round((result["final_capital"] / es.STARTING_CAPITAL - 1) * 100, 2)
summary = {"bot": BOT, "trades_found": int(len(trades)),
           "executed": result["num_executed"], "skipped": result["num_skipped"],
           "return_pct": total_return,
           "drawdown_pct": es.calculate_max_drawdown(result["equity_curve"], es.STARTING_CAPITAL),
           "allocation_pct": round(allocation * 100, 2),
           "max_concurrent_positions": limit}
summary.update(note)
with open(OUT_JSON, "w") as fh:
    json.dump(summary, fh, indent=2)
'''


def _sha256(path: str) -> str:
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def original_csv_path(repo_root: str, bot: str, portfolio_overview) -> str:
    """Pfad der BESTEHENDEN Kurve. elliott_wave liegt aus historischen
    Gruenden unter results/equity_curve.csv statt results/elliott_wave/ -
    dieselbe Sonderbehandlung wie in portfolio_overview.LEGACY_EQUITY_CSV_PATHS,
    hier nicht neu definiert, sondern von dort gelesen."""
    standard = os.path.join(repo_root, "results", bot, "equity_curve.csv")
    if os.path.exists(standard):
        return standard
    return portfolio_overview.LEGACY_EQUITY_CSV_PATHS.get(bot, standard)


def generate(repo_root: str, out_dir: str, portfolio_overview, verbose: bool = True) -> dict:
    """Erzeugt alle neun korrigierten Kurven und prueft sie.

    Rueckgabe: {bot: {"csv": pfad, "summary": {...}, "identical_to_original": bool}}
    Wirft SystemExit, wenn eine der beiden Proben aus dem Modul-Kopf
    fehlschlaegt - eine stillschweigend falsche Kurvenbasis waere schlimmer
    als gar keine.
    """
    os.makedirs(out_dir, exist_ok=True)
    out = {}
    problems = []

    for bot in ALL_BOTS:
        strategy_dir = os.path.join(repo_root, "strategies", bot)
        csv_path = os.path.join(out_dir, f"{bot}_equity_curve.csv")
        json_path = os.path.join(out_dir, f"{bot}_summary.json")

        proc = subprocess.run(
            [sys.executable, "-c", _WORKER, bot, csv_path, json_path],
            cwd=strategy_dir, capture_output=True, text=True,
            env={**os.environ, "PYTHONPATH": os.path.join(repo_root, "shared")})
        if proc.returncode != 0:
            raise SystemExit(f"Erzeugung fuer {bot} fehlgeschlagen:\n{proc.stderr[-2000:]}")

        with open(json_path) as handle:
            summary = json.load(handle)

        original = original_csv_path(repo_root, bot, portfolio_overview)
        identical = os.path.exists(original) and _sha256(original) == _sha256(csv_path)
        out[bot] = {"csv": csv_path, "summary": summary,
                    "identical_to_original": identical, "original_csv": original}

        # --- Probe 1: synchrone Bots muessen byteweise identisch sein -------
        # Ausnahme: der dokumentierte Veralterungs-Fall (KNOWN_STALE_BOTS).
        # Dort wird die Abweichung nicht durchgewunken, sondern umgekehrt
        # VERLANGT - waere die Kurve dort ploetzlich identisch, waere die
        # Begruendung fuer die Sonderbehandlung entfallen und der Bericht
        # falsch.
        if bot in CLEAN_BOTS and bot not in KNOWN_STALE_BOTS and not identical:
            problems.append(f"{bot}: synchroner Bot, aber erzeugte Kurve weicht von {original} ab")
        if bot in KNOWN_STALE_BOTS and identical:
            problems.append(f"{bot}: als veraltet dokumentiert, erzeugte Kurve ist aber "
                             f"identisch mit {original} - die Dokumentation stimmt nicht mehr")
        # --- Probe 2: abweichende Bots muessen den Sync-Check treffen -------
        if bot in SYNC_CHECK_REFERENCE:
            ref = SYNC_CHECK_REFERENCE[bot]
            if summary["executed"] != ref["executed"]:
                problems.append(f"{bot}: ausgefuehrte Trades {summary['executed']} "
                                 f"statt {ref['executed']} (Sync-Check)")
            for key in ("return_pct", "drawdown_pct"):
                if abs(summary[key] - ref[key]) > TOL:
                    problems.append(f"{bot}: {key} {summary[key]} statt {ref[key]} (Sync-Check)")

        if verbose:
            mark = "unveraendert" if identical else "KORRIGIERT"
            print(f"  {bot:<28}{mark:<14}{summary['executed']:>6} ausgefuehrt  "
                  f"{summary['return_pct']:>10.2f}%  DD {summary['drawdown_pct']:>7.2f}%")

    if problems:
        raise SystemExit("Kurvenerzeugung nicht belastbar:\n  - " + "\n  - ".join(problems))
    return out


def load_corrected_curves(portfolio_overview, generated: dict, swap_bots=None):
    """Laedt die Kurven ueber die UNVERAENDERTEN Funktionen von
    portfolio_overview - nur die Quellpfade der in `swap_bots` genannten
    Bots werden vorher auf die korrigierten Dateien umgebogen. Alle uebrigen
    Bots lesen weiterhin exakt die Datei, die auch die Erstfassung gelesen
    hat.

    `swap_bots=None` bedeutet SWAP_PRIMARY (die fuenf abweichenden Bots) -
    die auftragsgemaesse Korrektur.

    `discover_bots()` liest keine Kursdaten, es sammelt nur Pfade; die
    eigentliche Kurvenkonstruktion (Tagesraster, ffill, Startkapital)
    bleibt damit Wort fuer Wort dieselbe wie in der Erstfassung. Das ist
    der Grund, hier NICHT selbst zu lesen: jeder eigene Leser waere eine
    zweite, potenziell abweichende Definition derselben Kurve.
    """
    swap = SWAP_PRIMARY if swap_bots is None else tuple(swap_bots)
    bots = portfolio_overview.discover_bots()
    for bot in swap:
        if bot not in generated:
            raise SystemExit(f"{bot} steht nicht in den erzeugten Kurven zur Verfuegung")
        if bot in bots:
            bots[bot]["equity_csv"] = generated[bot]["csv"]
    curves = portfolio_overview.load_all_curves(bots)
    return bots, curves
