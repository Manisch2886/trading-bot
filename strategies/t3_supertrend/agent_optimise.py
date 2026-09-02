"""
Agentenbasierte Parameter-Suche - T3/ADX/SuperTrend-Strategie (Krypto)
============================================================================
Analog zu elliott_wave/agent_optimise.py: Claude erkundet gezielt den
Parameterraum statt alle 81 Kombinationen stur durchzuprobieren. Fuer
die finale Validierung bleibt multi_symbol_optimise.py + 
multi_symbol_walk_forward.py der Goldstandard.

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
    "t3_fast": {"type": "int", "range": [8, 16], "step": 4},
    "t3_slow": {"type": "int", "range": [21, 30], "step": 4},
    "adx_threshold": {"type": "float", "range": [20.0, 30.0], "step": 5.0},
    "stop_loss_pct": {"type": "float", "range": [2.0, 4.0], "step": 1.0},
}

SEED_COMBOS = [
    {"t3_fast": 16, "t3_slow": 30, "adx_threshold": 20.0, "stop_loss_pct": 4.0},  # validierte Referenz
    {"t3_fast": 12, "t3_slow": 25, "adx_threshold": 25.0, "stop_loss_pct": 3.0},
]


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden. Erst 'python3 fetch_4h_data.py' ausfuehren.")
        exit()

    def evaluate(params: dict):
        return evaluate_combination_multi(
            all_data,
            t3_fast=int(params["t3_fast"]),
            t3_slow=int(params["t3_slow"]),
            adx_threshold=params["adx_threshold"],
            stop_loss_pct=params["stop_loss_pct"],
        )

    result = run_agent_search(evaluate, PARAM_SPEC, seed_combos=SEED_COMBOS, max_iterations=12)

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
