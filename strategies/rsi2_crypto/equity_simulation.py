"""
Phase 3 - Equity-Kurven-Simulation (realistisches Portfolio): RSI-2 Krypto
================================================================================
Identisches Prinzip wie bei den bestehenden Bots: event-basierte Simulation
mit festem Startkapital, prozentualer Positionsgroesse und Positionslimit.
Eigenstaendige Kopie (Architektur-Prinzip). Startwerte wie angefragt: 10%
Allokation, Limit 8 - Kapitaleffizienz-Tuning kommt (wie bei den
Aktien-Versionen) erst NACH validiertem Trade-Level-Edge.
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
from zuteilung import simuliere_portfolio, protokollzeilen, AUFSTEIGEND

# Die Messkette - Rendite und Max Drawdown - steht seit TB-28 ebenfalls an
# einer einzigen Stelle: shared/messkette.py. Bis dahin stand
# `calculate_max_drawdown()` neunmal ZEICHENGLEICH in genau dieser Datei
# (nachgewiesen in TB-27), und die Renditeformel ebenso. Der englische Name
# bleibt, weil ueber dreissig Stellen im Repo ihn als Attribut dieses Moduls
# aufrufen; durch den Import bleibt er genau das.
from messkette import calculate_max_drawdown, rendite_pct

from multi_symbol_optimise import load_all_symbol_data, get_trades_for_symbol

# Die Strategie-Parameter kommen DIREKT aus live_params.py - derselben Datei,
# aus der auch forward_test.py liest (Muster aus PR #31). Vorher standen sie
# hier ein zweites Mal als eigene Konstanten. Dass beide Seiten denselben Wert
# trugen, war kein Schutz, sondern Zufall: die Doppelfuehrung faellt erst bei
# der ersten Parameter-Aenderung auf, die nur eine Seite erreicht - genau so
# ist die USE_TAKE_PROFIT-Abweichung beim Aktien-Elliott-Bot entstanden
# (Sync-Check, PR #24). live_params.py importiert selbst nichts, ein
# Importzyklus ist damit ausgeschlossen.
# Der Trendfilter heisst dort SMA_TREND_FILTER. STOP_LOSS_PCT ist None -
# "kein Stop" ist die validierte Kombination, kein fehlender Wert.
from live_params import (RSI_THRESHOLD, SMA_TREND_FILTER as SMA_TREND_PERIOD,
                          STOP_LOSS_PCT, MAX_CONCURRENT_POSITIONS,
                          ALLOCATION_PCT as _ALLOCATION_PCT_PROZENT)

STARTING_CAPITAL = 10_000.0
# EINHEITEN: live_params.py notiert die Allokation in PROZENT (10), dieses
# Skript rechnet mit dem ANTEIL (0.10). Deshalb die Umrechnung statt eines
# direkten Imports - dieselbe Falle, die auch der Sync-Check (PR #24)
# normalisieren musste, um keine falschen Abweichungen zu melden.
ALLOCATION_PCT = _ALLOCATION_PCT_PROZENT / 100


def collect_all_trades(all_data: dict, rsi_threshold: float, sma_trend_period: int,
                        stop_loss_pct: float = None) -> pd.DataFrame:
    all_trades = []
    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol(price_df, rsi_threshold, sma_trend_period, stop_loss_pct)
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)
    if not all_trades:
        return pd.DataFrame()
    combined = pd.concat(all_trades, ignore_index=True)
    combined["entry_time"] = pd.to_datetime(combined["entry_time"])
    combined["exit_time"] = pd.to_datetime(combined["exit_time"])
    return combined.sort_values("entry_time").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Stufe 1 der Zuteilungskaskade (shared/zuteilung.py)
# ---------------------------------------------------------------------------
# Welche STETIGE, zum Signalzeitpunkt bekannte Groesse drueckt bei diesem Bot
# die Signalstaerke aus? Sie entscheidet als erste, wenn mehrere Signale
# desselben Zeitpunkts um einen knappen Platz konkurrieren. `None` heisst:
# dieser Bot fuehrt keine, und die Kaskade beginnt beim Diversifikations-
# beitrag. Diese Zeile ist der EINZIGE Ort, an dem das je Bot steht.
# Der RSI(2) zum Einstieg IST die Signalstaerke dieser Strategie: sie
# steigt ein, weil er unter die Schwelle gefallen ist, und je tiefer er
# steht, desto ueberverkaufter ist der Titel - deshalb AUFSTEIGEND, also
# der niedrigste zuerst. Die Richtung kommt aus der Strategielogik und
# NICHT aus dem Backtest-Ergebnis; sie nach dem Ergebnis zu waehlen waere
# eine Anpassung an die Stichprobe.
#
# Eigenschaft 2 gemessen: 330 verschiedene Werte auf 439 Trades, 0,0 % der
# gleichzeitigen Trades bleiben darauf gleichauf.
#
# Das ist KEINE neue Groesse: die Spalte schreibt backtest_rsi2.py seit
# jeher mit. Wer sie nicht als Primaerschluessel will, setzt hier None -
# dann beginnt die Kaskade bei Stufe 2, und sonst aendert sich nichts.
SIGNALSPALTE = ("rsi_at_entry", AUFSTEIGEND)


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

    trades = collect_all_trades(all_data, RSI_THRESHOLD, SMA_TREND_PERIOD, STOP_LOSS_PCT)
    if trades.empty:
        # TB-109 Block B (Fable 25e (2)): null Trades ist ein Wert (5.1 Nr. 8,
        # 1c) - unter dem Selektionsmodus endet ein exit() ohne geschriebenes
        # Ergebnis mit Rueckgabewert 2, nicht mit 0. Ohne Modus wie bisher.
        import paths
        if paths.selektionsmodus() is not None:
            sys.stderr.write("Keine Trades fuer diese Parameter-Kombination gefunden." + "\n")
            raise SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)
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
