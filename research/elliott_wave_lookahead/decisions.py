"""
Halten die getroffenen Entscheidungen ohne den Look-Ahead? (Frage 4)
====================================================================================
Die live gesetzten Parameter beider Elliott-Wave-Bots wurden auf dem
BACKTEST entschieden - also auf der Datengrundlage, die den Zigzag-
Look-Ahead enthaelt. Dieses Skript wiederholt die dokumentierten
Vergleiche einmal auf der Baseline und einmal auf der korrigierten
Grundlage, mit identischer Methodik.

Geprueft werden fuer elliott_wave_stocks:
  * USE_TAKE_PROFIT = False  ("Gewinne laufen lassen")
  * MAX_CONCURRENT_POSITIONS = 8
Beide stammen aus derselben 2x4-Matrix in
`strategies/elliott_wave_stocks/experiment_combined.py`; die Matrix wird
hier Zelle fuer Zelle nachgebaut, Gesamtzeitraum UND Out-of-Sample
(TRAIN_SPLIT_RATIO = 0.7, symbolweise geteilt - dieselbe Funktion
`split_all_symbols`, die das Original benutzt).

Fuer elliott_wave (Krypto) gibt es keine vergleichbare dokumentierte
Matrix-Entscheidung; dort werden Take-Profit an/aus und die
Positionslimits derselben Matrix zur Einordnung mitgerechnet, aber
ausdruecklich NICHT als "Entscheidung" bewertet.

Reine Untersuchung: keine Empfehlung, keine Aenderung an live_params.py.

Nutzung:  python3 decisions.py <bot_name>
"""

import json
import os
import sys

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import run_one_bot as rob   # noqa: E402

BOT = rob.BOT
RESULTS_DIR = rob.RESULTS_DIR

# Woertlich aus experiment_combined.py
POSITION_LIMITS = [3, 5, 8, None]
TP_VARIANTS = [("mit Take-Profit", True), ("ohne Take-Profit", False)]

BASES = (rob.VARIANT_BASELINE, rob.VARIANT_CORRECTED)

# Die dokumentierte Entscheidungszahl aus EXPERIMENT_FINDINGS.md, Abschnitt 3.
# Wird als Regressionscheck der Baseline-Matrix benutzt.
PUBLISHED_CELLS = {
    "elliott_wave_stocks": {
        ("mit Take-Profit", 8): {"return_pct": 1500.53, "drawdown_pct": -1.90,
                                  "executed": 469, "skipped": 50},
        ("ohne Take-Profit", 8): {"return_pct": 3084.09, "drawdown_pct": -9.79,
                                   "executed": 288, "skipped": 231},
        ("mit Take-Profit", None): {"return_pct": 1675.56, "drawdown_pct": -2.52},
        ("ohne Take-Profit", None): {"return_pct": 4422.02, "drawdown_pct": -10.71},
    },
}
TOL = 0.02   # veroeffentlichte Werte sind auf 1-2 Nachkommastellen gerundet

PASSED = FAILED = 0


def check(label, actual, expected, tol=TOL):
    global PASSED, FAILED
    ok = actual is not None and abs(actual - expected) <= tol
    if ok:
        PASSED += 1
        print(f"  OK     {label:<54} {actual:>10.2f}")
    else:
        FAILED += 1
        print(f"  FEHLER {label:<54} {actual}  erwartet {expected}")


def cell(trades, es, limit) -> dict:
    """Eine Zelle der Matrix - ueber die UNVERAENDERTE simulate_portfolio des Bots."""
    if trades is None or trades.empty:
        return None
    supports_limit = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
    if supports_limit:
        res = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT, limit)
    else:
        res = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT)
    total_return = round((res["final_capital"] / es.STARTING_CAPITAL - 1) * 100, 2)
    max_dd = es.calculate_max_drawdown(res["equity_curve"], es.STARTING_CAPITAL)
    return {"total_return_pct": total_return, "max_drawdown_pct": max_dd,
            "calmar_ratio": rob.calmar(total_return, max_dd),
            "executed": res["num_executed"], "skipped": res["num_skipped"]}


FROZEN_DIR = os.path.join(RESULTS_DIR, "frozen_pr26")


def trades_for(all_data, cfg, basis, counter, es, use_tp):
    """Baseline aus dem eingefrorenen Bot-Stand, korrigiert aus dem Nachbau.

    Die Baseline kann nicht mehr aus der bot-eigenen collect_all_trades kommen:
    der Bot ist inzwischen korrigiert, das alte Verhalten existiert dort nicht
    mehr. Sie stammt deshalb aus results/frozen_pr26/ - den Trade-Saetzen, die
    der damals noch unkorrigierte Bot erzeugt hat.

    Wichtig ist dabei nicht nur der Trade-SATZ, sondern auch die
    ZEILENREIHENFOLGE: die Portfolio-Simulation vergibt Kapital in
    Ereignisreihenfolge, und bei gleichzeitigen Einstiegen entscheidet die
    Reihenfolge, wer den freien Platz bekommt (siehe
    research/order_sensitivity). Der Nachbau erzeugt dieselben Trades, aber in
    anderer Reihenfolge - bei Limit 8 verschiebt das die Rendite um ueber
    100 Prozentpunkte. Fuer einen Regressionscheck gegen die veroeffentlichten
    Zellen taugt deshalb nur die eingefrorene Originaldatei."""
    if basis == rob.VARIANT_BASELINE:
        tag = "mit_tp" if use_tp else "ohne_tp"
        name = (f"{BOT}_trades_baseline_bot.csv" if not use_tp
                else f"{BOT}_trades_baseline_bot_{tag}.csv")
        path = os.path.join(FROZEN_DIR, name)
        if not os.path.exists(path):
            raise SystemExit(f"{path} fehlt - ohne den eingefrorenen Bot-Stand laesst "
                              "sich die Baseline-Matrix nicht mehr reproduzieren.")
        return pd.read_csv(path, parse_dates=["entry_time", "exit_time"])
    return rob.collect(all_data, cfg, basis, counter, use_tp)


def build_matrix(all_data, cfg, basis, counter, es) -> dict:
    out = {}
    for tp_label, use_tp in TP_VARIANTS:
        trades = trades_for(all_data, cfg, basis, counter, es, use_tp)
        for limit in POSITION_LIMITS:
            key = f"{tp_label} | Limit {'unbegrenzt' if limit is None else limit}"
            out[key] = cell(trades, es, limit)
    return out


def main():
    import equity_simulation as es
    import live_params as lp
    import elliott_wave_counter as counter
    import backtest_elliott as bt
    from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO

    cfg = {
        "deviation_pct": float(lp.DEVIATION_PCT),
        "stop_loss_pct": float(lp.STOP_LOSS_PCT),
        "take_profit_fib": float(lp.TAKE_PROFIT_FIB),
        "max_hold_bars": int(bt.MAX_HOLD_HOURS),
        "cost_pct": 2 * (bt.TRADING_FEE_PCT + bt.SLIPPAGE_PCT),
        "max_concurrent": getattr(es, "MAX_CONCURRENT_POSITIONS", None),
        "freshness_bars": rob.FRESHNESS_BARS[BOT],
    }

    if BOT != "elliott_wave_stocks":
        # Bei elliott_wave (Krypto) gibt es keine Take-Profit-/Positionslimit-
        # Entscheidung dieser Art: equity_simulation.collect_all_trades kennt
        # dort gar keinen use_take_profit-Schalter und simulate_portfolio kein
        # Positionslimit. Die dortige dokumentierte Entscheidung ist die
        # Rasteroptimierung - die prueft grid.py. Ein Lauf hier wuerde eine
        # Matrix erzeugen, in der die "ohne Take-Profit"-Zeilen still mit
        # aktivem Take-Profit gerechnet waeren; deshalb Abbruch statt
        # irrefuehrender Ausgabe.
        raise SystemExit(
            f"{BOT} hat keine Take-Profit-/Positionslimit-Matrix - "
            "fuer diesen Bot ist grid.py das zustaendige Skript.")

    all_data = es.load_all_symbol_data()
    _train, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    matrices = {}
    for period, data in (("gesamt", all_data), ("out_of_sample", test_data)):
        matrices[period] = {basis: build_matrix(data, cfg, basis, counter, es)
                            for basis in BASES}

    if BOT in PUBLISHED_CELLS:
        print("\n1) Regressionscheck der Baseline-Matrix gegen EXPERIMENT_FINDINGS.md")
        for (tp_label, limit), ref in PUBLISHED_CELLS[BOT].items():
            key = f"{tp_label} | Limit {'unbegrenzt' if limit is None else limit}"
            got = matrices["gesamt"][rob.VARIANT_BASELINE][key]
            check(f"{key} / Rendite", got["total_return_pct"], ref["return_pct"])
            check(f"{key} / Max Drawdown", got["max_drawdown_pct"], ref["drawdown_pct"])
            if "executed" in ref:
                check(f"{key} / ausgefuehrt", float(got["executed"]), float(ref["executed"]), 0)
        if FAILED:
            print(f"\n{FAILED} Abweichungen - Entscheidungsanalyse waere nicht belastbar. Abbruch.")
            sys.exit(1)

    print("\n2) Die 2x4-Matrix auf beiden Grundlagen "
          "(Rendite % / Max Drawdown % / Calmar)")
    for period in ("gesamt", "out_of_sample"):
        print(f"\n  === {period} ===")
        print(f"  {'Zelle':<36}{'baseline':>28}{'korrigiert':>28}")
        for key in matrices[period][rob.VARIANT_BASELINE]:
            cells = ""
            for basis in BASES:
                c = matrices[period][basis][key]
                cells += ("".rjust(28) if c is None else
                          f"{c['total_return_pct']:>12.2f}/{c['max_drawdown_pct']:>7.2f}/"
                          f"{str(c['calmar_ratio']):>7}")
            print(f"  {key:<36}{cells}")

    print("\n3) Die dokumentierten Entscheidungen")
    verdicts = {}
    for period in ("gesamt", "out_of_sample"):
        for basis in BASES:
            m = matrices[period][basis]
            tp_on = m["mit Take-Profit | Limit 8"]
            tp_off = m["ohne Take-Profit | Limit 8"]
            if tp_on is None or tp_off is None:
                continue
            verdicts[f"USE_TAKE_PROFIT / {period} / {basis}"] = {
                "mit_take_profit": tp_on, "ohne_take_profit": tp_off,
                "ohne_besser_rendite": tp_off["total_return_pct"] > tp_on["total_return_pct"],
                "ohne_besser_calmar": (tp_off["calmar_ratio"] is not None
                                       and tp_on["calmar_ratio"] is not None
                                       and tp_off["calmar_ratio"] > tp_on["calmar_ratio"]),
            }
            limits = {lim: m[f"ohne Take-Profit | Limit "
                             f"{'unbegrenzt' if lim is None else lim}"]
                      for lim in POSITION_LIMITS}
            best_calmar = max((lim for lim, c in limits.items() if c and c["calmar_ratio"] is not None),
                              key=lambda lim: limits[lim]["calmar_ratio"], default=None)
            best_return = max((lim for lim, c in limits.items() if c),
                              key=lambda lim: limits[lim]["total_return_pct"], default=None)
            verdicts[f"MAX_CONCURRENT_POSITIONS / {period} / {basis}"] = {
                "gewaehlt": 8,
                "bestes_limit_nach_calmar": "unbegrenzt" if best_calmar is None else best_calmar,
                "bestes_limit_nach_rendite": "unbegrenzt" if best_return is None else best_return,
                "calmar_je_limit": {("unbegrenzt" if lim is None else str(lim)):
                                    (c["calmar_ratio"] if c else None) for lim, c in limits.items()},
            }

    for key, v in verdicts.items():
        if key.startswith("USE_TAKE_PROFIT"):
            print(f"  {key:<52} ohne TP besser: Rendite "
                  f"{'ja' if v['ohne_besser_rendite'] else 'NEIN':<5} | Calmar "
                  f"{'ja' if v['ohne_besser_calmar'] else 'NEIN'}")
        else:
            print(f"  {key:<52} bestes Limit: Calmar {v['bestes_limit_nach_calmar']}, "
                  f"Rendite {v['bestes_limit_nach_rendite']}  (gewaehlt: 8)")

    out_path = os.path.join(RESULTS_DIR, f"{BOT}_decisions.json")
    with open(out_path, "w") as fh:
        json.dump({"bot": BOT, "regressionscheck_bestanden": PASSED,
                   "train_split_ratio": TRAIN_SPLIT_RATIO,
                   "matrix": matrices, "entscheidungen": verdicts},
                  fh, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {out_path}")


if __name__ == "__main__":
    main()
