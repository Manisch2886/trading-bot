"""
Ein Bot, ein Prozess: Positionsverlauf aus dem ECHTEN Bot-Code holen
==============================================================================
Ruft die UNVERAENDERTEN Original-Funktionen des jeweiligen Bots auf
(`equity_simulation.py`: `load_all_symbol_data`, `collect_all_trades`,
`simulate_portfolio`, `calculate_max_drawdown`) und schreibt daraus den
Verlauf der TATSAECHLICH AUSGEFUEHRTEN Positionen heraus. An den
Original-Dateien wird nichts geaendert, es wird auch nichts unter `results/`
ueberschrieben - der schreibende Teil steckt in deren `__main__`-Block, und
der laeuft hier nie.

Ein eigener Prozess je Bot, weil alle neun Bots gleichnamige, aber inhaltlich
verschiedene Module haben (`equity_simulation.py`, `live_params.py`, ...) -
im selben Prozess wuerde sys.modules-Caching fuer den zweiten Bot die falsche
Version liefern. Vorbild: `shared/portfolio_overview.py` und
`research/order_sensitivity/run_one_bot.py`, von dem auch das Stubben der
nicht installierten bzw. zugangsdaten-behafteten Importe uebernommen ist.

DAS KERNPROBLEM UND SEINE LOESUNG
------------------------------------------------------------------------------
Fuer eine Exposure-Messung braucht man je Zeitpunkt die Menge der OFFENEN
Positionen samt gebundenem Kapital. `simulate_portfolio()` fuehrt diese Menge
intern (`open_positions`), gibt sie aber nicht heraus: zurueck kommen nur
Endkapital, Anzahl ausgefuehrt/uebersprungen und die Equity-Kurve, die je
Zeile einen ABGESCHLOSSENEN Trade beschreibt.

Statt die Funktion nachzubauen (was die Frage nicht beantworten wuerde, siehe
Aufgabenstellung), wird sie ZWEIMAL mit demselben Trade-Satz aufgerufen:

1. unveraendert - das Ergebnis muss Zeile fuer Zeile der im Repo liegenden
   `results/<bot>/equity_curve.csv` entsprechen;
2. mit einer Trade-Tabelle, deren `symbol`-Spalte um die Zeilenkennung
   ergaenzt ist (`AAPL#417`). `simulate_portfolio()` benutzt `symbol`
   ausschliesslich als Beschriftung der Ausgabezeile - jede Rechnung haengt
   an `pnl_pct`. Die Equity-Kurve des zweiten Laufs ist deshalb bis auf die
   Beschriftung identisch (wird geprueft), verraet aber zusaetzlich, WELCHE
   Zeile der Trade-Tabelle den Trade geliefert hat.

Damit ist die Zuordnung "welcher Trade wurde ausgefuehrt" exakt und nicht
geraten - ein blosser Rueckabgleich ueber (Ausstiegszeit, Symbol, PnL) waere
bei gleichen Werten mehrdeutig. Gegenprobe zu beiden Pruefungen:
`test_exposure_kern.py`.

Nutzung:
    python3 bot_lauf.py <bot_name>
"""

import json
import os
import sys
import types

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))

BOT = sys.argv[1]
sys.path.insert(0, os.path.join(_REPO_ROOT, "strategies", BOT))
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))

DATEN_DIR = os.path.join(_DIR, "daten")
os.makedirs(DATEN_DIR, exist_ok=True)

TRENNER = "#"   # kommt in keinem Symbol dieses Projekts vor (geprueft, s.u.)

# --- Stubs fuer Module, die hier nie aufgerufen werden -----------------------
# shared/fetch_binance_data.py enthaelt laut CLAUDE.md Zugangsdaten und ist
# gitignored; yfinance und python-binance sind in dieser Umgebung nicht
# installiert. Gelesen werden ausschliesslich die vorhandenen CSVs unter data/.
_fake_fetch = types.ModuleType("fetch_binance_data")
_fake_fetch.fetch_historical_data = lambda *a, **kw: pd.DataFrame()
sys.modules.setdefault("fetch_binance_data", _fake_fetch)

_fake_binance = types.ModuleType("binance")
_fake_client = types.ModuleType("binance.client")


class _FakeClient:
    KLINE_INTERVAL_1HOUR = "1h"
    KLINE_INTERVAL_4HOUR = "4h"
    KLINE_INTERVAL_1DAY = "1d"


_fake_client.Client = _FakeClient
_fake_binance.client = _fake_client
sys.modules.setdefault("binance", _fake_binance)
sys.modules.setdefault("binance.client", _fake_client)

_fake_yf = types.ModuleType("yfinance")
_fake_yf.download = lambda *a, **kw: pd.DataFrame()
_fake_yf.Ticker = lambda *a, **kw: None
sys.modules.setdefault("yfinance", _fake_yf)

_KEIN_LIMIT_PARAMETER = object()   # elliott_wave kennt gar keinen Limit-Parameter


def hole_trades(es, all_data):
    """Ruft `collect_all_trades()` mit GENAU den Argumenten auf, die der
    `__main__`-Block des jeweiligen Bots verwendet - inklusive des
    BTC-Regimefilters, den `volatility_breakout_crypto` bewusst erst danach
    anwendet (`apply_btc_regime_filter`, eigener Kommentarblock dort)."""
    if BOT == "elliott_wave":
        return es.collect_all_trades(all_data, es.DEVIATION_PCT, es.STOP_LOSS_PCT,
                                      es.TAKE_PROFIT_FIB)
    if BOT == "elliott_wave_stocks":
        return es.collect_all_trades(all_data, es.DEVIATION_PCT, es.STOP_LOSS_PCT,
                                      es.TAKE_PROFIT_FIB, es.USE_TAKE_PROFIT)
    if BOT == "t3_supertrend":
        # Der BTC-Regimefilter steckt bei diesem Bot IN collect_all_trades().
        return es.collect_all_trades(all_data, es.T3_FAST, es.T3_SLOW,
                                      es.ADX_THRESHOLD, es.STOP_LOSS_PCT)
    if BOT == "rsi2_crypto":
        return es.collect_all_trades(all_data, es.RSI_THRESHOLD, es.SMA_TREND_PERIOD,
                                      es.STOP_LOSS_PCT)
    if BOT == "rsi2_mean_reversion":
        return es.collect_all_trades(all_data, es.RSI_THRESHOLD, es.STOP_LOSS_PCT)
    if BOT in ("turtle_soup_crypto", "turtle_soup_stocks"):
        return es.collect_all_trades(all_data, es.DONCHIAN_PERIOD, es.STOP_MODE)
    if BOT == "volatility_breakout":
        return es.collect_all_trades(all_data, es.STOP_LOSS_PCT)
    if BOT == "volatility_breakout_crypto":
        trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT)
        return es.apply_btc_regime_filter(trades, all_data)
    raise ValueError(f"Unbekannter Bot: {BOT}")


def simuliere(es, trades, allocation_pct, max_concurrent):
    if max_concurrent is _KEIN_LIMIT_PARAMETER:
        return es.simulate_portfolio(trades, es.STARTING_CAPITAL, allocation_pct)
    return es.simulate_portfolio(trades, es.STARTING_CAPITAL, allocation_pct, max_concurrent)


def vergleiche_mit_repo(es, equity_df):
    """Zeile-fuer-Zeile-Abgleich mit der im Repo liegenden Kurve desselben
    Bots. Eine Abweichung ist kein Abbruchgrund, sondern ein Befund: sie
    hiesse, dass die abgelegte Kurve nicht mehr zu den heutigen
    live_params.py passt."""
    pfad = os.path.join(es.RESULTS_DIR, "equity_curve.csv")
    if not os.path.exists(pfad) and BOT == "elliott_wave":
        # Historische Ablage: die Kurve dieses Bots liegt in der Wurzel von
        # results/, nicht im Unterordner - so liest sie auch
        # portfolio_correlation_analysis.py, aus dem die -1,43 % stammen.
        pfad = os.path.join(_REPO_ROOT, "results", "equity_curve.csv")
    if not os.path.exists(pfad):
        return {"datei": pfad, "vorhanden": False}

    repo = pd.read_csv(pfad)
    eigen = equity_df.copy()
    eigen["time"] = pd.to_datetime(eigen["time"]).astype(str)
    repo["time"] = pd.to_datetime(repo["time"]).astype(str)

    spalten = ["time", "symbol", "pnl_pct", "allocation", "capital_after"]
    gleich_lang = len(repo) == len(eigen)
    abweichende_zeilen = None
    if gleich_lang:
        a = eigen[spalten].round(6).reset_index(drop=True)
        b = repo[spalten].round(6).reset_index(drop=True)
        abweichende_zeilen = int((a != b).any(axis=1).sum())

    return {
        "datei": os.path.relpath(pfad, _REPO_ROOT),
        "vorhanden": True,
        "zeilen_repo": len(repo),
        "zeilen_eigen": len(eigen),
        "identisch": bool(gleich_lang and abweichende_zeilen == 0),
        "abweichende_zeilen": abweichende_zeilen,
    }


def main():
    import equity_simulation as es

    all_data = es.load_all_symbol_data()
    if not all_data:
        raise SystemExit(f"{BOT}: keine Kursdaten gefunden.")

    trades = hole_trades(es, all_data)
    if trades is None or trades.empty:
        raise SystemExit(f"{BOT}: keine Trades.")

    trades = trades.copy()
    trades["entry_time"] = pd.to_datetime(trades["entry_time"])
    trades["exit_time"] = pd.to_datetime(trades["exit_time"])

    if trades["symbol"].astype(str).str.contains(TRENNER).any():
        raise SystemExit(f"{BOT}: Symbol enthaelt '{TRENNER}' - Kennzeichnung nicht eindeutig.")

    allocation_pct = es.ALLOCATION_PCT
    hat_limit = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
    max_concurrent = getattr(es, "MAX_CONCURRENT_POSITIONS", None) if hat_limit else _KEIN_LIMIT_PARAMETER
    limit_wert = None if max_concurrent is _KEIN_LIMIT_PARAMETER else max_concurrent

    # --- Lauf 1: unveraendert ------------------------------------------------
    ergebnis = simuliere(es, trades, allocation_pct, max_concurrent)
    equity = ergebnis["equity_curve"]

    # --- Lauf 2: mit Zeilenkennung im Symbol ---------------------------------
    markiert = trades.copy()
    markiert["symbol"] = [f"{s}{TRENNER}{i}" for i, s in zip(markiert.index, markiert["symbol"])]
    ergebnis_markiert = simuliere(es, markiert, allocation_pct, max_concurrent)
    equity_markiert = ergebnis_markiert["equity_curve"]

    # Die Kennzeichnung darf die Simulation NICHT veraendert haben.
    kennzeichnung_neutral = bool(
        len(equity) == len(equity_markiert)
        and ergebnis["num_executed"] == ergebnis_markiert["num_executed"]
        and ergebnis["num_skipped"] == ergebnis_markiert["num_skipped"]
        and equity["capital_after"].reset_index(drop=True).equals(
            equity_markiert["capital_after"].reset_index(drop=True))
        and equity["allocation"].reset_index(drop=True).equals(
            equity_markiert["allocation"].reset_index(drop=True))
    )
    if not kennzeichnung_neutral:
        raise SystemExit(f"{BOT}: Kennzeichnung hat die Simulation veraendert - Abbruch.")

    # --- Ausgefuehrte Positionen zusammensetzen ------------------------------
    kennungen = equity_markiert["symbol"].astype(str).str.rsplit(TRENNER, n=1).str[-1].astype(int)
    if kennungen.duplicated().any():
        raise SystemExit(f"{BOT}: dieselbe Trade-Zeile doppelt ausgefuehrt - Abbruch.")

    positionen = trades.loc[kennungen.values, ["symbol", "entry_time", "exit_time", "pnl_pct"]].copy()
    positionen = positionen.reset_index().rename(columns={"index": "trade_zeile"})
    positionen["allocation"] = equity["allocation"].values
    positionen["capital_after"] = equity["capital_after"].values
    positionen["exit_time_equity"] = pd.to_datetime(equity["time"].values)

    # Gegenprobe: die aus der Trade-Tabelle geholte Ausstiegszeit muss die der
    # Equity-Kurve sein, und kein Einstieg darf nach seinem Ausstieg liegen.
    if not (positionen["exit_time"] == positionen["exit_time_equity"]).all():
        raise SystemExit(f"{BOT}: Ausstiegszeiten passen nicht zusammen - Abbruch.")
    if (positionen["entry_time"] > positionen["exit_time"]).any():
        raise SystemExit(f"{BOT}: Einstieg nach Ausstieg - Abbruch.")

    positionen = positionen.drop(columns=["exit_time_equity"])
    positionen = positionen.sort_values("entry_time").reset_index(drop=True)
    positionen.to_csv(os.path.join(DATEN_DIR, f"{BOT}_positionen.csv"), index=False)

    meta = {
        "bot": BOT,
        "startkapital": es.STARTING_CAPITAL,
        "allocation_pct": allocation_pct,
        "max_concurrent_positions": limit_wert,
        "bot_hat_limit_parameter": hat_limit,
        "trades_gefunden": int(len(trades)),
        "trades_ausgefuehrt": int(ergebnis["num_executed"]),
        "trades_uebersprungen": int(ergebnis["num_skipped"]),
        "endkapital": ergebnis["final_capital"],
        "rendite_pct": round((ergebnis["final_capital"] / es.STARTING_CAPITAL - 1) * 100, 2),
        "max_drawdown_pct_bot": es.calculate_max_drawdown(equity, es.STARTING_CAPITAL),
        "erster_einstieg": str(positionen["entry_time"].min()),
        "letzter_ausstieg": str(positionen["exit_time"].max()),
        "symbole": int(positionen["symbol"].nunique()),
        "kennzeichnung_neutral": kennzeichnung_neutral,
        "abgleich_results_csv": vergleiche_mit_repo(es, equity),
    }
    with open(os.path.join(DATEN_DIR, f"{BOT}_meta.json"), "w") as f:
        json.dump(meta, f, indent=2, default=str)

    abgleich = meta["abgleich_results_csv"]
    marke = "identisch" if abgleich.get("identisch") else f"ABWEICHEND ({abgleich})"
    print(f"{BOT}: {meta['trades_ausgefuehrt']} ausgefuehrt / {meta['trades_uebersprungen']} "
          f"uebersprungen, Rendite {meta['rendite_pct']:.2f}%, "
          f"DD {meta['max_drawdown_pct_bot']:.2f}%, results-Abgleich: {marke}")


if __name__ == "__main__":
    main()
