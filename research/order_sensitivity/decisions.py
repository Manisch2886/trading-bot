"""
Halten die bereits getroffenen, dokumentierten Entscheidungen der
Reihenfolge-Willkuer stand?
==========================================================================
Punkt 4 der Aufgabenstellung. Fuer jede bereits umgesetzte Entscheidung
werden BEIDE verglichenen Konfigurationen ueber 500 Permutationen der
Verarbeitungsreihenfolge gerechnet und ausgezaehlt, in wie vielen davon
die tatsaechlich getroffene Wahl die bessere ist.

PAARUNG: wo sich die beiden Konfigurationen nur in Kapitalparametern
unterscheiden (Positionslimit, Allokation), liegt DERSELBE Trade-Satz
zugrunde und dieselbe Permutation wird auf beide angewendet - der
Vergleich ist dann echt gepaart und die Reihenfolge-Willkuer kuerzt sich
weitgehend heraus. Wo sich die Trade-SAETZE unterscheiden (Take-Profit an
oder aus), ist die Paarung nur nominell (gleicher Seed, aber
unterschiedlich lange Trade-Listen); das ist bei der jeweiligen
Entscheidung vermerkt.

Nutzung:
    python3 decisions.py <bot_name>
"""

import json
import os
import sys

import numpy as np

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import order_core as oc
import run_one_bot as rob   # bringt die Stubs und die Bot-Pfade mit

BOT = rob.BOT
RESULTS_DIR = rob.RESULTS_DIR
N_PERMUTATIONS = rob.N_PERMUTATIONS
SEED = rob.SEED

# Fuer jeden Bot: die dokumentierte Entscheidung, die Quelle, die tatsaechlich
# gewaehlte Variante und die Alternative, gegen die entschieden wurde.
DECISIONS = {
    "elliott_wave_stocks": [{
        "id": "take_profit_aus",
        "frage": "USE_TAKE_PROFIT = False statt True",
        "quelle": "results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md, Abschnitt 2/3; "
                  "live_params.py-Historie 2026-09-03",
        "gewaehlt": {"label": "ohne Take-Profit (live)", "use_take_profit": False},
        "alternative": {"label": "mit Take-Profit", "use_take_profit": True},
        "berichtet": {"ohne Take-Profit": "+3084,1 % / -9,79 %", "mit Take-Profit": "+1500,5 % / -1,90 %"},
        "paarung": "nominell - unterschiedliche Trade-Saetze",
    }],
    "rsi2_mean_reversion": [{
        "id": "allokation_5_limit_20",
        "frage": "5 % Allokation und Limit 20 statt 10 % und Limit 8",
        "quelle": "results/rsi2_mean_reversion/PROTOTYPE_FINDINGS.md, Abschnitt 6",
        "gewaehlt": {"label": "5 % / Limit 20 (live)", "allocation_pct": 0.05, "max_concurrent": 20},
        "alternative": {"label": "10 % / Limit 8", "allocation_pct": 0.10, "max_concurrent": 8},
        "berichtet": {"5 %/20": "+36,75 % / -21,05 %", "10 %/8": "+33,94 % / -28,46 %"},
        "paarung": "echt - identischer Trade-Satz",
    }],
    "t3_supertrend": [{
        "id": "limit_5",
        "frage": "MAX_CONCURRENT_POSITIONS = 5 statt 3, 8 oder unbegrenzt",
        "quelle": "Uebergabeprotokoll Abschnitt 3.2 (empirisch getestet: 3/5/8/unbegrenzt)",
        "gewaehlt": {"label": "Limit 5 (live)", "max_concurrent": 5},
        "alternative": {"label": "Limit 8", "max_concurrent": 8},
        "weitere": [{"label": "Limit 3", "max_concurrent": 3},
                     {"label": "unbegrenzt", "max_concurrent": None}],
        "berichtet": {"Limit 5": "102,7 % / -31,2 % (ohne Regimefilter)"},
        "paarung": "echt - identischer Trade-Satz",
    }],
    "volatility_breakout": [{
        "id": "limit_15",
        "frage": "MAX_CONCURRENT_POSITIONS = 15 statt 8",
        "quelle": "results/volatility_breakout/PROTOTYPE_FINDINGS.md, Abschnitt 11; "
                  "live_params.py-Historie 2026-09-03",
        "gewaehlt": {"label": "Limit 15 (live)", "max_concurrent": 15},
        "alternative": {"label": "Limit 8 (equity_simulation.py)", "max_concurrent": 8},
        "berichtet": {"Limit 15": "deutlich hoehere Rendite bei nur leicht hoeherem Drawdown"},
        "paarung": "echt - identischer Trade-Satz",
    }],
    "turtle_soup_stocks": [{
        "id": "allokation_2_unbegrenzt",
        "frage": "2 % Allokation und unbegrenztes Limit statt 10 % und Limit 8",
        "quelle": "results/turtle_soup_stocks/PROTOTYPE_FINDINGS.md, Abschnitt 8c; "
                  "live_params.py-Historie 2026-09-04",
        "gewaehlt": {"label": "2 % / unbegrenzt (live)", "allocation_pct": 0.02, "max_concurrent": None},
        "alternative": {"label": "10 % / Limit 8", "allocation_pct": 0.10, "max_concurrent": 8},
        "berichtet": {"2 %/unbegrenzt": "hoehere Rendite bei gleichzeitig niedrigerem Drawdown"},
        "paarung": "echt - identischer Trade-Satz",
    }],
    "turtle_soup_crypto": [{
        "id": "basiskonfiguration",
        "frage": "Kapitalmanagement unveraendert bei 10 % / Limit 8 belassen",
        "quelle": "results/turtle_soup_crypto/PROTOTYPE_FINDINGS.md, Abschnitt 8b/8c",
        "gewaehlt": {"label": "10 % / Limit 8 (live)", "allocation_pct": 0.10, "max_concurrent": 8},
        "alternative": {"label": "5 % / Limit 20", "allocation_pct": 0.05, "max_concurrent": 20},
        "berichtet": {"10 %/8": "jede getestete Lockerung verschlechterte Rendite UND Drawdown"},
        "paarung": "echt - identischer Trade-Satz",
    }],
}


def evaluate_config(trades, es, allocation_pct, max_concurrent, n_perm, seed) -> dict:
    """Punktschaetzer (Original-Reihenfolge) plus Permutations-Verteilung."""
    entry_ns, exit_ns, pnl = oc.as_arrays(trades)
    point = oc.simulate_fast(entry_ns, exit_ns, pnl, es.STARTING_CAPITAL,
                              allocation_pct, max_concurrent)
    perms = oc.run_permutations(trades, es.STARTING_CAPITAL, allocation_pct,
                                 max_concurrent, n_perm, seed)
    return {
        "point_total_return_pct": round(point["total_return_pct"], 2),
        "point_max_drawdown_pct": point["max_drawdown_pct"],
        "point_calmar": oc.calmar(point["total_return_pct"], point["max_drawdown_pct"]),
        "point_executed": int(point["executed"].sum()),
        "perms": perms,
    }


def compare(chosen: dict, alternative: dict) -> dict:
    """Wie oft ist die tatsaechlich gewaehlte Variante besser? Verglichen
    wird replikatweise (gleicher Permutations-Index)."""
    out = {}
    for key in ("calmar_ratio", "total_return_pct", "max_drawdown_pct"):
        a = chosen["perms"][key]
        b = alternative["perms"][key]
        if a is None or b is None:
            continue
        va, vb = a["values"], b["values"]
        length = min(len(va), len(vb))
        mask = np.isfinite(va[:length]) & np.isfinite(vb[:length])
        if not mask.any():
            continue
        diff = va[:length][mask] - vb[:length][mask]
        out[key] = {
            "share_chosen_better_pct": round(float((diff > 0).mean() * 100), 1),
            "median_difference": round(float(np.median(diff)), 3),
            "chosen_range": [a["min"], a["max"]],
            "alternative_range": [b["min"], b["max"]],
            "ranges_overlap": not (a["min"] > b["max"] or b["min"] > a["max"]),
        }
    return out


def main():
    if BOT not in DECISIONS:
        print(f"{BOT}: keine dokumentierte Kapitalmanagement-/Exit-Entscheidung hinterlegt.")
        return

    import equity_simulation as es

    all_data = es.load_all_symbol_data()
    results = []

    for decision in DECISIONS[BOT]:
        variants = [decision["gewaehlt"], decision["alternative"]] + decision.get("weitere", [])
        evaluated = {}
        for variant in variants:
            if "use_take_profit" in variant:
                trades = es.collect_all_trades(all_data, es.DEVIATION_PCT, es.STOP_LOSS_PCT,
                                                es.TAKE_PROFIT_FIB, variant["use_take_profit"])
                allocation = es.ALLOCATION_PCT
                limit = es.MAX_CONCURRENT_POSITIONS
            else:
                trades = rob.load_original_trades(es)
                allocation = variant.get("allocation_pct", es.ALLOCATION_PCT)
                limit = variant.get("max_concurrent", getattr(es, "MAX_CONCURRENT_POSITIONS", None))
            evaluated[variant["label"]] = evaluate_config(
                trades, es, allocation, limit, N_PERMUTATIONS, SEED)

        chosen_label = decision["gewaehlt"]["label"]
        alt_label = decision["alternative"]["label"]
        results.append({
            "id": decision["id"],
            "frage": decision["frage"],
            "quelle": decision["quelle"],
            "paarung": decision["paarung"],
            "berichtet": decision["berichtet"],
            "varianten": {label: oc.strip_values(data) for label, data in evaluated.items()},
            "vergleich_gewaehlt_vs_alternative": compare(evaluated[chosen_label],
                                                          evaluated[alt_label]),
        })

        print(f"\n{decision['id']}: {decision['frage']}")
        for label, data in evaluated.items():
            c = data["perms"]["calmar_ratio"]
            marker = " <- gewaehlt" if label == chosen_label else ""
            print(f"  {label:<34} Punktschaetzer Rendite {data['point_total_return_pct']:>9.2f}% "
                  f"DD {data['point_max_drawdown_pct']:>7.2f}% Calmar {str(data['point_calmar']):>8}"
                  f"  |  Permutationen Calmar {c['min']:>8.2f}..{c['max']:>8.2f}{marker}")
        for key, value in results[-1]["vergleich_gewaehlt_vs_alternative"].items():
            print(f"  -> {key:<20} gewaehlte Variante besser in {value['share_chosen_better_pct']:>5.1f} % "
                  f"der Permutationen  (Spannen ueberlappen: {'ja' if value['ranges_overlap'] else 'nein'})")

    with open(os.path.join(RESULTS_DIR, f"{BOT}_decisions.json"), "w") as f:
        json.dump({"bot": BOT, "n_permutations": N_PERMUTATIONS, "decisions": results},
                  f, indent=2, default=str)


if __name__ == "__main__":
    main()
