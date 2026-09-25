"""
Equity-Kurven-Simulation - T3/ADX/SuperTrend-Strategie
============================================================
Identisches Prinzip wie bei der Elliott-Wave-Strategie: statt Trade-
Prozente einfach zu addieren, wird ein echtes Portfolio simuliert -
begrenztes Kapital, feste Positionsgroesse, chronologische Verarbeitung.
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

# Die Zuteilungskaskade und die Kapitalsimulation - seit TB-26 an einer
# einzigen Stelle fuer alle neun Bots (siehe dortigen Kopfkommentar).
from zuteilung import simuliere_portfolio, protokollzeilen

# Die Messkette - Rendite und Max Drawdown - steht seit TB-28 ebenfalls an
# einer einzigen Stelle: shared/messkette.py. Bis dahin stand
# `calculate_max_drawdown()` neunmal ZEICHENGLEICH in genau dieser Datei
# (nachgewiesen in TB-27), und die Renditeformel ebenso. Der englische Name
# bleibt, weil ueber dreissig Stellen im Repo ihn als Attribut dieses Moduls
# aufrufen; durch den Import bleibt er genau das.
from messkette import calculate_max_drawdown, rendite_pct

from multi_symbol_optimise import load_all_symbol_data, get_trades_for_symbol
import backtest_trend
from regime_filter import compute_btc_regime, filter_trades_by_regime
# Register 11.1 (TB-105): die Wache vor dem Regimefilter, einmal in shared/.
# Fehlt BTCUSDT, bricht sie ab, statt den Filter still zu ueberspringen.
from regimewache import btc_daten

# Die Strategie-Parameter kommen DIREKT aus live_params.py - derselben Datei,
# aus der auch forward_test.py liest (Muster aus PR #31). Vorher standen sie
# hier ein zweites Mal als eigene Konstanten. Dass beide Seiten denselben Wert
# trugen, war kein Schutz, sondern Zufall: die Doppelfuehrung faellt erst bei
# der ersten Parameter-Aenderung auf, die nur eine Seite erreicht - genau so
# ist die USE_TAKE_PROFIT-Abweichung beim Aktien-Elliott-Bot entstanden
# (Sync-Check, PR #24). live_params.py importiert selbst nichts, ein
# Importzyklus ist damit ausgeschlossen.
# Die beiden T3-Laengen heissen dort T3_FAST_LENGTH/T3_SLOW_LENGTH.
# MAX_CONCURRENT_POSITIONS = 5 begrenzt das Klumpenrisiko bei korrelierten
# Krypto-Trends (bei 18 handelbaren Coins: max. ~28% gleichzeitig offen).
from live_params import (T3_FAST_LENGTH as T3_FAST, T3_SLOW_LENGTH as T3_SLOW,
                          ADX_THRESHOLD, STOP_LOSS_PCT, MAX_CONCURRENT_POSITIONS)

STARTING_CAPITAL = 10_000.0
# ALLOCATION_PCT steht bei diesem Bot NICHT in live_params.py - eine
# dokumentierte Luecke (Sync-Check, PR #24), kein Versehen dieser Aenderung.
# Der Wert bleibt deshalb hier.
ALLOCATION_PCT = 0.10


def collect_all_trades(all_data: dict, t3_fast: int, t3_slow: int,
                        adx_threshold: float, stop_loss_pct: float) -> pd.DataFrame:
    all_trades = []
    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol(price_df, t3_fast, t3_slow, adx_threshold, stop_loss_pct)
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)

    if not all_trades:
        return pd.DataFrame()

    combined = pd.concat(all_trades, ignore_index=True)
    combined["entry_time"] = pd.to_datetime(combined["entry_time"])
    combined["exit_time"] = pd.to_datetime(combined["exit_time"])

    # Markt-Regime-Filter: nur Trades behalten, die waehrend eines
    # BTC-Aufwaertstrends eroeffnet wurden. Bis TB-105 stand hier
    # `if "BTCUSDT" in all_data:` ohne else - fehlte BTCUSDT, rechnete der
    # Bot still ohne Filter, also als ein anderer Bot (Register 11.1).
    btc = btc_daten(all_data, bot="t3_supertrend",
                    holen="python3 fetch_4h_data.py")
    btc_regime = compute_btc_regime(btc)
    combined = filter_trades_by_regime(combined, btc_regime)

    return combined.sort_values("entry_time").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Stufe 1 der Zuteilungskaskade (shared/zuteilung.py)
# ---------------------------------------------------------------------------
# Welche STETIGE, zum Signalzeitpunkt bekannte Groesse drueckt bei diesem Bot
# die Signalstaerke aus? Sie entscheidet als erste, wenn mehrere Signale
# desselben Zeitpunkts um einen knappen Platz konkurrieren. `None` heisst:
# dieser Bot fuehrt keine, und die Kaskade beginnt beim Diversifikations-
# beitrag. Diese Zeile ist der EINZIGE Ort, an dem das je Bot steht.
# Dieser Bot fuehrt kein Mass fuer Signalstaerke: seine Trade-Tabelle
# enthaelt ausser Zeiten, Kursen und Ergebnis nichts. Der ADX-Wert zum
# Einstieg waere ein Kandidat, wird aber nicht mitgeschrieben - ihn hier
# nachzurechnen waere eine neue Groesse und damit eine Strategieaenderung,
# keine Rangregel. Die Kaskade beginnt beim Diversifikationsbeitrag.
SIGNALSPALTE = None


def simulate_portfolio(trades: pd.DataFrame, starting_capital: float,
                        allocation_pct: float, max_concurrent_positions: int = None,
                        kursdaten=None, signalspalte=SIGNALSPALTE) -> dict:
    """Kapitalsimulation mit Zuteilungskaskade.

    Die Rechnung selbst steht seit TB-26 an EINER Stelle fuer alle neun Bots:
    `shared/zuteilung.py`. Vorher stand sie neunmal fast wortgleich hier - und
    mit ihr neunmal derselbe Befund aus TB-23: wurde ein Platz knapp, entschied
    die Zeilenreihenfolge des Trade-DataFrames, also die Symbolreihenfolge der
    Konfigurationsdatei. Ein Zweitkriterium gab es nicht.

    Was hier bleibt, ist das Bot-Eigene: der Primaerschluessel `SIGNALSPALTE`.

    `kursdaten` ist die `load_all_symbol_data()`-Rueckgabe. Sie wird fuer die
    Stufen 2 (Korrelation) und 3 (Liquiditaet) gebraucht; ohne sie ruhen die
    beiden, das Ergebnis bleibt reproduzierbar und das Protokoll weist es aus.

    `signalspalte` ist nur zu setzen, wenn die uebergebene Trade-Tabelle die
    Spalte gar nicht fuehren KANN - so bei den Live-Trades aus der Bot-
    Datenbank (`shared/portfolio_overview.py`), die Zeiten, Symbol und
    Ergebnis enthalten und sonst nichts. Bleibt sie auf ihrer Vorbelegung und
    fehlt die Spalte, bricht `shared/zuteilung.py` ab, statt lautlos ohne
    Stufe 1 weiterzurechnen.
    """
    return simuliere_portfolio(trades, starting_capital, allocation_pct,
                                max_concurrent_positions, kursdaten,
                                signalspalte=signalspalte)


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        # TB-105 Block C (Fable 24b A2): unter dem Selektionsmodus ist das ein
        # Abbruch mit Rueckgabewert 2, kein exit() mit 0. Ohne Modus wie bisher.
        import paths
        if paths.selektionsmodus() is not None:
            sys.stderr.write("Keine Daten gefunden." + "\n")
            raise SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)
        print("Keine Daten gefunden.")
        exit()

    trades = collect_all_trades(all_data, T3_FAST, T3_SLOW, ADX_THRESHOLD, STOP_LOSS_PCT)

    if trades.empty:
        print("Keine Trades fuer diese Parameter-Kombination gefunden.")
        exit()

    print(f"{len(trades)} Trades ueber alle Symbole gefunden.\n")

    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT,
                                MAX_CONCURRENT_POSITIONS, all_data)

    print("=" * 55)
    print("PORTFOLIO-SIMULATION")
    print("=" * 55)
    print(f"Startkapital:            {STARTING_CAPITAL:,.2f}")
    print(f"Endkapital:              {result['final_capital']:,.2f}")

    total_return_pct = rendite_pct(result["final_capital"], STARTING_CAPITAL)
    print(f"Gesamtrendite:           {total_return_pct:.2f}%")
    print(f"Ausgefuehrte Trades:     {result['num_executed']}")
    print(f"Uebersprungene Trades:   {result['num_skipped']}")

    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    print(f"Max Drawdown (Kapital):  {max_dd:.2f}%")

    # Der Startwert des Zufalls gehoert ins Protokoll: ein Zufall, den
    # niemand aufschreibt, ist kein reproduzierbarer.
    for zeile in protokollzeilen(result["zuteilung"]):
        print(zeile)

    if not result["equity_curve"].empty:
        output_path = os.path.join(RESULTS_DIR, "equity_curve.csv")
        result["equity_curve"].to_csv(output_path, index=False)
        print(f"\nGespeichert als: {output_path}")
