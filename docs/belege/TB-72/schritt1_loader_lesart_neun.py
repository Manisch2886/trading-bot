"""TB-72 Schritt 1, zweite Methode: loader_lesart (Nachrechnung nach MIN_HISTORY_*)
je Bot - unabhaengig vom Trockenlauf-Kindprozess. Rein lesend.

    trading-env/bin/python3 docs/belege/TB-72/schritt1_loader_lesart_neun.py aus.json
"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))  # docs/belege/TB-72 -> Repo-Wurzel
sys.path.insert(0, os.path.join(BASE, "research", "faltenplan_neun"))
import faltenschranke_messung as fsm
import faltenplan_neun as fn
aus = {}
print(f"{'Bot':<28}{'Schranke':<20}{'Wert':>6}  {'fruehestes Symbol handelbar ab':<32}{'Jahr':>6}  Fensteranker")
for bot in fn.BOTS:
    l = fsm.loader_lesart(bot)
    aus[bot] = {k: v for k, v in l.items() if k != "handelbar_ab"}
    aus[bot]["symbole_handelbar"] = sum(1 for d in l["handelbar_ab"].values() if d)
    aus[bot]["symbole_ohne_datei"] = sum(1 for d in l["handelbar_ab"].values() if not d)
    print(f"{bot:<28}{l['schranke']:<20}{l['wert']:>6}  {str(l['fruehestes_symbol_handelbar_ab']):<32}"
          f"{str(l['erstes_jahr_loader']):>6}  {l.get('fensteranker')}")
with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(aus, f, indent=2, ensure_ascii=False, sort_keys=True)
