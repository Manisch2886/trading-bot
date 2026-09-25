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

# Die drei Strategie-Parameter kommen DIREKT aus live_params.py - derselben
# Datei, aus der auch forward_test.py liest. Vorher standen sie hier ein
# zweites Mal als eigene Konstanten, was zwangslaeufig auseinanderlief:
# nach der Parameter-Umstellung (PR #30) rechnete dieses Skript noch mit
# 4 % / 2 % / 0.236, waehrend der Bot bereits mit 10 % / 6 % / 0.618 lief.
# Ein Backtest von hier beschrieb damit eine Strategie, die es nicht mehr
# gab (Sync-Check, PR #24). Der Import schliesst diese Luecke strukturell:
# es gibt nur noch EINE Quelle, eine kuenftige Aenderung wirkt automatisch
# auch hier. live_params.py importiert selbst nichts, ein Importzyklus ist
# also ausgeschlossen.
from live_params import DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB

STARTING_CAPITAL = 10_000.0
ALLOCATION_PCT = 0.10  # Anteil des aktuellen Kapitals pro Trade


def collect_all_trades(all_data: dict, deviation_pct: float,
                        stop_loss_pct: float, take_profit_fib: float) -> pd.DataFrame:
    """Sammelt alle Trades ueber alle Symbole fuer eine gegebene Parameter-Kombination."""
    backtest_elliott.STOP_LOSS_PCT = stop_loss_pct
    backtest_elliott.TAKE_PROFIT_FIB = take_profit_fib

    all_trades = []
    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol(price_df, deviation_pct)
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
# Elliott Wave fuehrt mit `fib_score` zwar ein Guetemass der Welle, aber
# kein STETIGES: oberhalb der Schwelle nimmt er nur fuenf Werte an. Gemessen
# auf den 130 Trades dieses Bots bleiben danach 38,6 % der gleichzeitigen
# Trades gleichauf - Eigenschaft 2 der Pruefliste (hoechstens 2 %
# Gleichstaende an der Kante) ist damit verfehlt, und zwar um Groessen-
# ordnungen. Die Kaskade beginnt deshalb beim Diversifikationsbeitrag.
# Ob unter dem Score stetige Abstaende liegen (Retracement gegen
# Zielverhaeltnis), untersucht TB-25; bis dahin wird hier nichts erfunden.
SIGNALSPALTE = None


def simulate_portfolio(trades: pd.DataFrame, starting_capital: float,
                        allocation_pct: float, kursdaten=None,
                        signalspalte=SIGNALSPALTE) -> dict:
    """Kapitalsimulation mit Zuteilungskaskade.

    Die Rechnung selbst steht seit TB-26 an EINER Stelle fuer alle neun Bots:
    `shared/zuteilung.py`. Vorher stand sie neunmal fast wortgleich in den
    equity_simulation.py - und mit ihr neunmal derselbe Befund aus TB-23: wurde
    ein Platz knapp, entschied die Zeilenreihenfolge des Trade-DataFrames, also
    die Symbolreihenfolge der Konfigurationsdatei.

    DIESER Bot kennt bewusst KEIN Positionslimit - deshalb fehlt das Argument
    hier weiterhin. `shared/portfolio_overview.py` und
    `research/order_sensitivity/run_one_bot.py` fragen genau danach
    (`inspect.signature` bzw. `co_varnames`), um zu erkennen, welcher Bot eins
    hat; ein Limit-Argument mit Vorbelegung None waere fuer beide eine stille
    Falschauskunft. An `shared/zuteilung.py` wird deshalb None durchgereicht.

    `signalspalte` ist nur zu setzen, wenn die uebergebene Trade-Tabelle die
    Spalte gar nicht fuehren KANN - so bei den Live-Trades aus der Bot-
    Datenbank (`shared/portfolio_overview.py`), die Zeiten, Symbol und
    Ergebnis enthalten und sonst nichts. Bleibt sie auf ihrer Vorbelegung und
    fehlt die Spalte, bricht `shared/zuteilung.py` ab, statt lautlos ohne
    Stufe 1 weiterzurechnen.
    """
    return simuliere_portfolio(trades, starting_capital, allocation_pct,
                                None, kursdaten, signalspalte=signalspalte)


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        # TB-105 Block C (Fable 24b A2): unter dem Selektionsmodus ist das ein
        # Abbruch mit Rueckgabewert 2, kein exit() mit 0. Ohne Modus wie bisher.
        import paths
        if paths.selektionsmodus() is not None:
            sys.stderr.write("Keine Daten gefunden. Erst 'python3 fetch_multi_data.py' ausfuehren." + "\n")
            raise SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)
        print("Keine Daten gefunden. Erst 'python3 fetch_multi_data.py' ausfuehren.")
        exit()

    trades = collect_all_trades(all_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB)

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

    print(f"{len(trades)} Trades ueber alle Symbole gefunden (unsortiert nach Kapital-Verfuegbarkeit).\n")

    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, all_data)

    print("=" * 55)
    print("PORTFOLIO-SIMULATION")
    print("=" * 55)
    print(f"Startkapital:            {STARTING_CAPITAL:,.2f}")
    print(f"Endkapital:              {result['final_capital']:,.2f}")

    total_return_pct = rendite_pct(result["final_capital"], STARTING_CAPITAL)
    print(f"Gesamtrendite:           {total_return_pct:.2f}%")
    print(f"Ausgefuehrte Trades:     {result['num_executed']}")
    print(f"Uebersprungene Trades:   {result['num_skipped']} (nicht genug freies Kapital)")

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
