"""
Regressions-Check: reproduziert diese Untersuchung die Bot-Baseline exakt?
==============================================================================
Die drei Stop-Varianten werden hier NICHT mit den bot-eigenen
backtest_*.py-Schleifen gerechnet, sondern mit einer gemeinsamen,
parametrisierten Ausstiegs-Simulation (atr_core.simulate_exit) - anders
liesse sich die Ausstiegsregel nicht sauber austauschen, ohne fuenf
Live-Backtest-Dateien anzufassen (was diese Untersuchung ausdruecklich
nicht darf).

Damit steht und faellt die Aussagekraft der Untersuchung mit EINER Frage:
liefert diese Nachbildung mit der Variante "fixed_static" (= der
bestehende feste Prozent-Stop) EXAKT dieselben Trades wie der Bot selbst?

Dieses Skript prueft genau das - es vergleicht die Baseline-Trades dieser
Untersuchung mit dem Ergebnis der bot-eigenen, unveraenderten
`equity_simulation.collect_all_trades()`. Verglichen werden Trade-Anzahl,
Summe und Mittelwert der PnL sowie die Zeitpunkte des ersten und letzten
Trades. Abweichung = die Untersuchung ist NICHT belastbar.

Nutzung:
    python3 verify_baseline.py <bot_name>     # ein Bot
    python3 run_all.py --verify               # alle betroffenen Bots
"""

import sys

import pandas as pd

# run_one_bot liest den Bot-Namen aus sys.argv[1] - dieses Skript wird mit
# derselben Signatur aufgerufen, der Import uebernimmt also automatisch
# denselben Bot (inkl. der dort noetigen Stub-Injektion fuer binance/yfinance).
import run_one_bot as rob
from atr_core import STOP_FIXED_STATIC

BOT = rob.BOT


def bot_own_trades(cfg: dict) -> pd.DataFrame:
    """Ruft die UNVERAENDERTE collect_all_trades() des jeweiligen Bots auf -
    mit exakt den Parametern aus dessen live_params.py. Die Signaturen
    unterscheiden sich je Bot, deshalb die Fallunterscheidung."""
    import equity_simulation as es
    import live_params as lp

    all_data = es.load_all_symbol_data()

    if BOT == "elliott_wave":
        return es.collect_all_trades(all_data, deviation_pct=lp.DEVIATION_PCT,
                                      stop_loss_pct=lp.STOP_LOSS_PCT,
                                      take_profit_fib=lp.TAKE_PROFIT_FIB)
    if BOT == "elliott_wave_stocks":
        return es.collect_all_trades(all_data, deviation_pct=lp.DEVIATION_PCT,
                                      stop_loss_pct=lp.STOP_LOSS_PCT,
                                      take_profit_fib=lp.TAKE_PROFIT_FIB,
                                      use_take_profit=lp.USE_TAKE_PROFIT)
    if BOT == "t3_supertrend":
        return es.collect_all_trades(all_data, t3_fast=lp.T3_FAST_LENGTH, t3_slow=lp.T3_SLOW_LENGTH,
                                      adx_threshold=lp.ADX_THRESHOLD, stop_loss_pct=lp.STOP_LOSS_PCT)
    if BOT in ("volatility_breakout", "volatility_breakout_crypto"):
        return es.collect_all_trades(all_data, stop_loss_pct=lp.STOP_LOSS_PCT,
                                      max_hold_days=getattr(lp, "MAX_HOLD_DAYS", None))
    raise ValueError(f"Kein Baseline-Vergleich fuer {BOT} definiert")


def main():
    prepared, cfg = rob.prepare()
    mine = rob.collect_trades(prepared, cfg, STOP_FIXED_STATIC, k=None)
    theirs = bot_own_trades(cfg)

    checks = [
        ("Anzahl Trades", len(mine), len(theirs), 0),
        ("Summe PnL (%)", round(float(mine["pnl_pct"].sum()), 2),
         round(float(theirs["pnl_pct"].sum()), 2), 0.01),
        ("Mittelwert PnL (%)", round(float(mine["pnl_pct"].mean()), 4),
         round(float(theirs["pnl_pct"].mean()), 4), 0.0001),
    ]

    print(f"Baseline-Regressionscheck: {BOT}")
    print(f"{'Kennzahl':<22} {'diese Untersuchung':>20} {'Bot-eigener Code':>20}  Status")
    ok = True
    for name, a, b, tol in checks:
        passed = abs(a - b) <= tol
        ok &= passed
        print(f"{name:<22} {a:>20} {b:>20}  {'OK' if passed else 'ABWEICHUNG'}")

    for label, col in (("erster Entry", "entry_time"), ("letzter Exit", "exit_time")):
        a = mine[col].min() if col == "entry_time" else mine[col].max()
        b = theirs[col].min() if col == "entry_time" else theirs[col].max()
        passed = pd.Timestamp(a) == pd.Timestamp(b)
        ok &= passed
        print(f"{label:<22} {str(a):>20} {str(b):>20}  {'OK' if passed else 'ABWEICHUNG'}")

    print("\nERGEBNIS:", "Baseline exakt reproduziert." if ok
          else "ABWEICHUNG - Ergebnisse dieses Bots sind NICHT belastbar.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
