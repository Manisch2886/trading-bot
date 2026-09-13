"""
Phase 3e - Equity-Kurven-Simulation (realistisches Portfolio)
================================================================
Bisher haben wir Trades isoliert bewertet und ihre Prozentwerte
einfach aufsummiert. Das ignoriert eine wichtige Realitaet: Du hast
nur EIN Kapital, das sich auf mehrere, teils gleichzeitig offene
Positionen (verschiedene Coins) aufteilen muss.

Diese Simulation:
- startet mit einem virtuellen Kapital (Standard: 10.000)
- allokiert pro Trade einen festen Anteil des AKTUELLEN Kapitals
  (Standard: 10%)
- verarbeitet alle Trades ueber alle Symbole chronologisch
- blockiert neue Trades, wenn nicht genug freies (nicht bereits
  gebundenes) Kapital verfuegbar ist
- gibt eine echte Equity-Kurve, finales Kapital und einen
  Kapital-basierten Max Drawdown zurueck

WICHTIG: Vereinfachungen gegenueber der Realitaet:
- Keine Transaktionsgebuehren oder Slippage
- Offene Positionen werden nicht "mark-to-market" bewertet,
  Kapital aktualisiert sich erst beim Trade-Ausstieg
- Gleichzeitige Signale werden in der Reihenfolge verarbeitet, in
  der die zugrunde liegenden Wellen abgeschlossen wurden
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
import backtest_elliott

# Die Strategie-Parameter kommen DIREKT aus live_params.py - derselben Datei,
# aus der auch forward_test.py liest (Muster aus PR #31). Vorher standen sie
# hier ein zweites Mal als eigene Konstanten, und genau bei diesem Bot ist die
# Doppelfuehrung bereits auseinandergelaufen: USE_TAKE_PROFIT wurde am
# 2026-09-03 live auf False gesetzt ("Gewinne laufen lassen"), hier blieb es
# auf True stehen. Ein Backtest von hier beschrieb damit eine Strategie, die
# so nicht mehr laeuft (Sync-Check, PR #24). Der Import schliesst das
# strukturell: es gibt nur noch EINE Quelle. live_params.py importiert selbst
# nichts, ein Importzyklus ist ausgeschlossen.
#
# MAX_CONCURRENT_POSITIONS = 8 begrenzt das Klumpenrisiko bei breiten
# Marktbewegungen - bei 150 Aktien steigt die Chance auf viele gleichzeitige
# Signale deutlich (siehe Diskussion beim T3/SuperTrend-Bot).
from live_params import (DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB,
                          USE_TAKE_PROFIT, MAX_CONCURRENT_POSITIONS)

STARTING_CAPITAL = 10_000.0
# ALLOCATION_PCT steht bei diesem Bot NICHT in live_params.py - eine
# dokumentierte Luecke (Sync-Check, PR #24), kein Versehen dieser Aenderung.
ALLOCATION_PCT = 0.10  # Anteil des aktuellen Kapitals pro Trade


def collect_all_trades(all_data: dict, deviation_pct: float, stop_loss_pct: float,
                        take_profit_fib: float, use_take_profit: bool = True) -> pd.DataFrame:
    """Sammelt alle Trades ueber alle Symbole fuer eine gegebene Parameter-Kombination."""
    backtest_elliott.STOP_LOSS_PCT = stop_loss_pct
    backtest_elliott.TAKE_PROFIT_FIB = take_profit_fib

    all_trades = []
    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol(price_df, deviation_pct, use_take_profit)
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
# Wie beim Krypto-Zwilling: `fib_score` nimmt oberhalb der Schwelle nur
# fuenf Werte an. Gemessen auf den 510 Trades dieses Bots bleiben 218
# Trades (72,7 % der gleichzeitigen) darauf gleichauf; TB-23 hat denselben
# Befund mit 144 Trades (48,0 %) an der Limit-Kante beziffert. Eigenschaft 2
# der Pruefliste ist damit verfehlt - kein Primaerschluessel, die Kaskade
# beginnt bei Stufe 2. TB-25 prueft, ob unter dem Score stetige Abstaende
# liegen; erst danach waere ein Primaerschluessel hier ueberhaupt zu
# erwaegen.
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
        print("Keine Daten gefunden. Erst 'python3 fetch_multi_data.py' ausfuehren.")
        exit()

    trades = collect_all_trades(all_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, USE_TAKE_PROFIT)

    if trades.empty:
        print("Keine Trades fuer diese Parameter-Kombination gefunden.")
        exit()

    print(f"{len(trades)} Trades ueber alle Symbole gefunden (unsortiert nach Kapital-Verfuegbarkeit).\n")

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
    # Der Klammerzusatz nannte frueher pauschal "nicht genug freies Kapital".
    # Das ist die falsche Haelfte der Wahrheit: simulate_portfolio()
    # ueberspringt einen Trade entweder, weil MAX_CONCURRENT_POSITIONS
    # erreicht ist, ODER weil das freie Kapital nicht reicht. Beide landen in
    # derselben Liste, die Funktion gibt nur deren Laenge zurueck - eine
    # Aufschluesselung ist von hier aus gar nicht moeglich.
    #
    # Der Zusatz war nicht nur ungenau, sondern in der Sache falsch: im
    # gemessenen Lauf gingen ALLE 115 uebersprungenen Trades auf das Limit
    # zurueck und keiner auf fehlendes Kapital. Bei 10 % Allokation und
    # hoechstens 8 gleichzeitigen Positionen sind nie mehr als rund 80 % des
    # Kapitals gebunden - das Limit greift praktisch immer zuerst.
    #
    # Gleicher Wortlaut wie in oos_equity_simulation.py (PR #48), damit die
    # beiden Skripte nicht wieder Verschiedenes ueber dieselbe Zahl sagen.
    print(f"Uebersprungene Trades:   {result['num_skipped']} "
          f"(Positionslimit {MAX_CONCURRENT_POSITIONS} erreicht oder zu wenig freies Kapital)")

    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    print(f"Max Drawdown (Kapital):  {max_dd:.2f}%")

    # Der Startwert des Zufalls gehoert ins Protokoll: ein Zufall, den
    # niemand aufschreibt, ist kein reproduzierbarer.
    for zeile in protokollzeilen(result["zuteilung"]):
        print(zeile)

    if not result["equity_curve"].empty:
        print("\nLetzte 10 abgeschlossene Trades:")
        print(result["equity_curve"].tail(10).to_string(index=False))

        output_path = os.path.join(RESULTS_DIR, "equity_curve.csv")
        result["equity_curve"].to_csv(output_path, index=False)
        print(f"\nGespeichert als: {output_path}")
