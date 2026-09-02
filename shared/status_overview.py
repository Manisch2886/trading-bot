"""
Status-Ueberblick aller Bots
================================
Zeigt auf einen Blick den aktuellen Stand aller drei Trading-Bots -
offene Positionen, geschlossene Trades, Win Rate. Liest nur die
lokalen Datenbanken, macht KEINE API-Aufrufe (kostenlos, sofort).

Aufruf von ueberall im trading-bot-Ordner:
    python3 shared/status_overview.py
"""

import os
import sqlite3
import pandas as pd

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)

STRATEGIES = ["elliott_wave", "t3_supertrend", "elliott_wave_stocks"]


def get_status(strategy_name: str) -> dict:
    db_file = os.path.join(BASE_DIR, f"paper_trading_{strategy_name}.db")

    if not os.path.exists(db_file):
        return {"error": f"Datenbank nicht gefunden: {db_file}"}

    conn = sqlite3.connect(db_file)
    open_trades = pd.read_sql("SELECT * FROM trades WHERE status='open'", conn)
    closed_trades = pd.read_sql("SELECT * FROM trades WHERE status='closed'", conn)
    conn.close()

    result = {
        "num_open": len(open_trades),
        "open_symbols": open_trades["symbol"].tolist() if not open_trades.empty else [],
        "num_closed": len(closed_trades),
    }

    if not closed_trades.empty:
        result["win_rate"] = round((closed_trades["pnl_pct"] > 0).mean() * 100, 1)
        result["avg_pnl"] = round(closed_trades["pnl_pct"].mean(), 2)
        result["total_pnl"] = round(closed_trades["pnl_pct"].sum(), 2)
        result["last_trade"] = closed_trades.iloc[-1][["symbol", "exit_time", "result", "pnl_pct"]].to_dict()

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("STATUS-UEBERBLICK ALLER BOTS")
    print("=" * 60)

    for strategy_name in STRATEGIES:
        print(f"\n[{strategy_name}]")
        status = get_status(strategy_name)

        if "error" in status:
            print(f"  {status['error']}")
            continue

        print(f"  Offene Positionen: {status['num_open']}", end="")
        if status["open_symbols"]:
            print(f" ({', '.join(status['open_symbols'])})")
        else:
            print()

        print(f"  Geschlossene Trades gesamt: {status['num_closed']}")

        if status["num_closed"] > 0:
            print(f"  Win Rate: {status['win_rate']}%  |  Ø PnL: {status['avg_pnl']}%  |  "
                  f"Summe: {status['total_pnl']}%")
            lt = status["last_trade"]
            print(f"  Letzter Trade: {lt['symbol']} ({lt['result']}, {lt['pnl_pct']}%) am {lt['exit_time']}")

    print("\n" + "=" * 60)
