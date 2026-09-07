"""
Was bringt die zweite Korrektur? (Teil 3 der Backtest-Korrektur)
====================================================================================
Stellt drei Stufen gegenueber:

  baseline      der urspruengliche Backtest, beide Look-Ahead-Kanaele offen.
                Quelle: die eingefrorenen Trade-Saetze aus PR #26
                (results/frozen_pr26/) - im Bot-Code existiert dieses
                Verhalten nicht mehr.
  kanal1        nur der Einstiegszeitpunkt korrigiert (Einstieg zum
                Bestaetigungskurs). Das war die "korrigierte Variante" aus
                PR #26; sie wurde dort ausdruecklich als OBERGRENZE
                bezeichnet, weil die Wellenauswahl noch rueckblickend lief.
  beide         zusaetzlich die kausale Wellenauswahl. Das ist der Stand,
                den strategies/<bot>/ jetzt tatsaechlich rechnet - hier
                direkt ueber die bot-eigene collect_all_trades geholt, nicht
                nachgebaut.

Reine Auswertung, kein neuer Backtest-Entwurf: Kanal-1-Zahlen kommen aus
results/<bot>.json (PR #26), die Zahlen mit beiden Korrekturen aus dem
laufenden Bot-Code.

Nutzung:  python3 compare_channels.py <bot_name>
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
PR26_PATH = os.path.join(RESULTS_DIR, f"{BOT}.json")


def main():
    import equity_simulation as es
    import live_params as lp
    import backtest_elliott as bt

    cfg = {
        "deviation_pct": float(lp.DEVIATION_PCT),
        "stop_loss_pct": float(lp.STOP_LOSS_PCT),
        "take_profit_fib": float(lp.TAKE_PROFIT_FIB),
        "max_hold_bars": int(bt.MAX_HOLD_HOURS),
        "cost_pct": 2 * (bt.TRADING_FEE_PCT + bt.SLIPPAGE_PCT),
        "max_concurrent": getattr(es, "MAX_CONCURRENT_POSITIONS", None),
        "freshness_bars": bt.SIGNAL_FRESHNESS_BARS,
    }

    if not os.path.exists(PR26_PATH):
        raise SystemExit(f"{PR26_PATH} fehlt - bitte zuerst run_one_bot.py laufen lassen.")
    with open(PR26_PATH) as fh:
        pr26 = json.load(fh)

    all_data = es.load_all_symbol_data()
    if BOT == "elliott_wave_stocks":
        trades = es.collect_all_trades(all_data, cfg["deviation_pct"], cfg["stop_loss_pct"],
                                        cfg["take_profit_fib"], lp.USE_TAKE_PROFIT)
    else:
        trades = es.collect_all_trades(all_data, cfg["deviation_pct"], cfg["stop_loss_pct"],
                                        cfg["take_profit_fib"])
    both = rob.evaluate(trades, es, cfg)

    stages = {
        "baseline (kein Kanal korrigiert)": pr26["variants"]["baseline"],
        "nur Kanal 1 (Einstiegskurs)": pr26["variants"]["korrigiert"],
        "beide Kanaele (Bot-Stand heute)": both,
    }

    print(f"\n{BOT}")
    print(f"  {'Stufe':<36}{'Trades':>8}{'ausgef.':>9}{'Rendite':>12}{'Max DD':>10}"
          f"{'Calmar':>10}{'Gewinnrate':>12}")
    for label, r in stages.items():
        print(f"  {label:<36}{r['num_trades']:>8}{r['num_executed']:>9}"
              f"{r['total_return_pct']:>11.2f}%{r['max_drawdown_pct']:>9.2f}%"
              f"{str(r['calmar_ratio']):>10}{r['win_rate_pct']:>11.1f}%")

    k1 = pr26["variants"]["korrigiert"]
    delta = {
        "trades": both["num_trades"] - k1["num_trades"],
        "rendite_pp": round(both["total_return_pct"] - k1["total_return_pct"], 2),
        "drawdown_pp": round(both["max_drawdown_pct"] - k1["max_drawdown_pct"], 2),
        "calmar": (None if both["calmar_ratio"] is None or k1["calmar_ratio"] is None
                   else round(both["calmar_ratio"] - k1["calmar_ratio"], 2)),
    }
    print(f"\n  Wirkung der zweiten Korrektur (Kanal 2) gegenueber Kanal 1 allein:")
    print(f"    Trades      {delta['trades']:+d}")
    print(f"    Rendite     {delta['rendite_pp']:+.2f} pp")
    print(f"    Max DD      {delta['drawdown_pp']:+.2f} pp")
    print(f"    Calmar      {delta['calmar']:+.2f}" if delta["calmar"] is not None else "    Calmar      -")

    # PR #26 hatte erwartet, dass die Zahlen mit beiden Korrekturen NIEDRIGER
    # ausfallen ("Obergrenze"). Ob das zutrifft, wird hier gemessen statt
    # angenommen - die Richtung ist nicht durch die Art des Bias festgelegt.
    lowered = both["total_return_pct"] < k1["total_return_pct"]
    print(f"\n  Erwartung aus PR #26 (Kanal-1-Zahlen sind eine Obergrenze): "
          f"{'bestaetigt' if lowered else 'NICHT bestaetigt'}")
    print(f"    Die kausale Auswahl streicht keine Welle mehr rueckwirkend, es kommen also")
    print(f"    MEHR Trades zustande ({delta['trades']:+d}). Ob das hilft oder schadet, ist")
    print(f"    nicht durch die Richtung des Bias festgelegt: der Fibonacci-Score, nach dem")
    print(f"    rueckblickend ausgewaehlt wurde, ist ein Formmass, kein Gewinnmass.")

    out = {"bot": BOT, "stufen": stages, "wirkung_kanal2": delta,
           "erwartung_obergrenze_bestaetigt": bool(lowered)}
    path = os.path.join(RESULTS_DIR, f"{BOT}_channel_comparison.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {path}")


if __name__ == "__main__":
    main()
