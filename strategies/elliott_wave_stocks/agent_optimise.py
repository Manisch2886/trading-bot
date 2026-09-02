"""
Agentenbasierte Parameter-Suche - Elliott-Wave-Strategie (Aktien)
=======================================================================
Analog zu den beiden Krypto-Bots. Bei diesem Bot besonders nuetzlich,
da der Parameterraum durch die use_take_profit-Dimension (64
Kombinationen) groesser ist - der Agent kann hier potenziell mehr Zeit
sparen als bei den kleineren Raeumen der Krypto-Bots.

Braucht einen ANTHROPIC_API_KEY (siehe shared/claude_client.py).
"""

import os
import sys

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from param_search_agent import run_agent_search
from multi_symbol_optimise import load_all_symbol_data, evaluate_combination_multi

PARAM_SPEC = {
    "deviation_pct": {"type": "float", "range": [2.0, 5.0], "step": 1.0},
    "stop_loss_pct": {"type": "float", "range": [2.0, 8.0], "step": 1.0},
    "take_profit_fib": {"type": "float", "options": [0.236, 0.382, 0.5]},
    "use_take_profit": {"type": "bool", "options": [True, False]},
}

SEED_COMBOS = [
    {"deviation_pct": 5.0, "stop_loss_pct": 2.0, "take_profit_fib": 0.236, "use_take_profit": True},  # validierte Referenz
    {"deviation_pct": 3.0, "stop_loss_pct": 5.0, "take_profit_fib": 0.236, "use_take_profit": False},
]


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden. Erst 'python3 fetch_stock_data.py' ausfuehren.")
        exit()

    def evaluate(params: dict):
        return evaluate_combination_multi(
            all_data,
            deviation_pct=params["deviation_pct"],
            stop_loss_pct=params["stop_loss_pct"],
            take_profit_fib=params.get("take_profit_fib", 0.236),
            use_take_profit=params.get("use_take_profit", True),
        )

    result = run_agent_search(evaluate, PARAM_SPEC, seed_combos=SEED_COMBOS, max_iterations=15)

    print("\n" + "=" * 55)
    print("AGENT-SUCHE ABGESCHLOSSEN")
    print("=" * 55)
    print(f"Getestete Kombinationen: {len(result['history'])}")
    if result["best"]:
        print(f"\nBestes gefundenes Ergebnis:")
        for k, v in result["best"].items():
            print(f"  {k}: {v}")
        print("\nEmpfehlung: diese Kombination zusaetzlich mit multi_symbol_walk_forward.py")
        print("validieren, bevor du ihr vertraust.")
    else:
        print("Keine gueltige Kombination gefunden.")
