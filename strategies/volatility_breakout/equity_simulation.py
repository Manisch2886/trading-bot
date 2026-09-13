"""
Phase 3 - Equity-Kurven-Simulation (realistisches Portfolio): Volatility Breakout
======================================================================================
Identisches Prinzip wie bei den anderen Aktien-Bots: event-basierte
Simulation mit festem Startkapital, prozentualer Positionsgroesse und
Positionslimit. Eigenstaendige Kopie (Architektur-Prinzip: jede Strategie
unabhaengig, kein Cross-Strategy-Import).
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
from data_quality import melde_uebersprungene_balken
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

# Die Parameter kommen DIREKT aus live_params.py - derselben Datei, aus der
# auch forward_test.py liest (Muster aus PR #31/#38/#39). Vorher standen sie
# hier ein zweites Mal als eigene Konstanten, und einer davon war
# auseinandergelaufen (Sync-Check, PR #24):
#   MAX_CONCURRENT_POSITIONS  8 hier gegen 15 live
#
# AUFGEGEBENE BEGRUENDUNG - bitte nicht versehentlich zurueckdrehen: das
# Limit 8 stand hier als "Startwert, identisch zu den anderen Aktien-Bots",
# also aus Gruenden der Vergleichbarkeit zwischen den Bots. Diese Motivation
# gilt ab jetzt nicht mehr; massgeblich ist der tatsaechliche Live-Wert. Ein
# Backtest, der eine andere Konfiguration rechnet als der laufende Bot, ist
# die teurere Ungenauigkeit als eine eingeschraenkte Vergleichbarkeit
# zwischen Bots.
#
# ALLOCATION_PCT und STOP_LOSS_PCT waren bereits identisch (10 % bzw. 8.0);
# sie werden mit umgestellt, damit die Doppelfuehrung vollstaendig
# verschwindet. live_params.py importiert selbst nichts, ein Importzyklus ist
# ausgeschlossen.
from live_params import (STOP_LOSS_PCT, MAX_CONCURRENT_POSITIONS,
                          ALLOCATION_PCT as _ALLOCATION_PCT_PROZENT)

STARTING_CAPITAL = 10_000.0
# EINHEITEN: live_params.py notiert die Allokation in PROZENT (10), dieses
# Skript rechnet mit dem ANTEIL (0.10) - deshalb die Umrechnung statt eines
# direkten Imports. shared/portfolio_overview.py liest ALLOCATION_PCT von hier
# und erwartet ebenfalls den Anteil.
ALLOCATION_PCT = _ALLOCATION_PCT_PROZENT / 100


def collect_all_trades(all_data: dict, stop_loss_pct: float, max_hold_days: int = None,
                        use_volume_filter: bool = False) -> pd.DataFrame:
    all_trades = []
    for symbol, (df_ind, entry_cutoff) in all_data.items():
        trades = get_trades_for_symbol(df_ind, entry_cutoff, stop_loss_pct, max_hold_days, use_volume_filter)
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)

    if not all_trades:
        return pd.DataFrame()

    combined = pd.concat(all_trades, ignore_index=True)
    combined["entry_time"] = pd.to_datetime(combined["entry_time"])
    combined["exit_time"] = pd.to_datetime(combined["exit_time"])

    # Trades ohne Ein- oder Ausstiegskurs streichen und die Streichung
    # MELDEN. Ein einziger fehlender Kurs macht sonst die gesamte
    # Kapitalkurve unbrauchbar (simulate_portfolio rechnet ihn ins
    # Kapital, ab da ist jede Folgezahl NaN) - und der Projekt-Score
    # merkt nichts davon, weil pandas beim Mitteln NaN ueberspringt.
    # Genau so ist es beim leeren letzten Balken von APH passiert.
    # Siehe shared/data_quality.py.
    preisspalten = [s for s in ("entry_price", "exit_price") if s in combined.columns]
    if preisspalten:
        luecke = combined[preisspalten].isna().any(axis=1)
        if luecke.any():
            for symbol, anzahl in combined.loc[luecke, "symbol"].value_counts().items():
                melde_uebersprungene_balken(symbol, int(anzahl), "Trade ohne Kurs gestrichen")
            combined = combined[~luecke]

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
# enthaelt ausser Zeiten, Kursen, Ergebnis und Haltedauer nichts. Die
# Bandbreite zum Ausbruch waere ein Kandidat, wird aber nicht
# mitgeschrieben. Die Kaskade beginnt beim Diversifikationsbeitrag.
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
        print("Keine Daten gefunden.")
        exit()

    trades = collect_all_trades(all_data, STOP_LOSS_PCT)
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
