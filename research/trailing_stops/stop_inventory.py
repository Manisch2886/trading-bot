"""
Schritt 1: Bestandsaufnahme der Stop-Mechanismen aller 9 Bots
==================================================================
ZWINGEND VOR jeder weiteren Umsetzung auszufuehren (Aufgabenstellung,
Schritt 1). Liest AUSSCHLIESSLICH die 9 strategies/<bot>/live_params.py
(rein lesend, per Text-Parsing statt Import - so kann kein Bot-Modul
versehentlich Seiteneffekte ausloesen und es braucht keine
sys.modules-Isolation) und klassifiziert jeden Bot in genau eine von
drei Kategorien:

  "fixed_pct"   - fester Prozent-Stop-Loss (STOP_LOSS_PCT = Zahl).
                  NUR diese Bots sind Gegenstand der Untersuchung.
  "structural"  - struktureller/musterspezifischer Stop (STOP_MODE mit
                  einem Wert != None, z. B. "structural" = Stop auf dem
                  Tagestief des Setup-Tags). Konzeptionell etwas
                  ANDERES als ein fester Prozentsatz: die Stop-Distanz
                  ergibt sich bereits heute aus der Marktstruktur und
                  ist damit implizit volatilitaets-abhaengig. Wird
                  dokumentiert, aber NICHT angefasst.
  "none"        - bewusst kein Stop-Loss (STOP_LOSS_PCT = None bzw.
                  STOP_MODE = None). Laut Projekt-Historie in
                  live_params.py jeweils EMPIRISCH als beste Variante
                  validiert ("ein harter Stop senkt den Erwartungswert").
                  Hier wird NACHTRAEGLICH KEINER eingefuehrt - das waere
                  eine eigenstaendige Design-Frage und ausdruecklich
                  nicht Teil dieser Aufgabe.

Nutzung:
    python3 stop_inventory.py            # Tabelle auf stdout
    python3 stop_inventory.py --json     # zusaetzlich results/stop_inventory.json
"""

import ast
import json
import os
import sys

_RESEARCH_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_RESEARCH_DIR))
STRATEGIES_DIR = os.path.join(_REPO_ROOT, "strategies")
RESULTS_DIR = os.path.join(_RESEARCH_DIR, "results")

# Alle im Projekt vorhandenen Bots - die Liste wird zur Laufzeit gegen die
# tatsaechlich vorhandenen Ordner geprueft, damit ein spaeter ergaenzter
# 10. Bot hier nicht still uebersehen wird (siehe check_completeness()).
KNOWN_BOTS = [
    "elliott_wave", "elliott_wave_stocks", "t3_supertrend",
    "rsi2_crypto", "rsi2_mean_reversion",
    "turtle_soup_crypto", "turtle_soup_stocks",
    "volatility_breakout", "volatility_breakout_crypto",
]

MARKET = {
    "elliott_wave": ("Krypto", "1h"),
    "elliott_wave_stocks": ("Aktien", "1d"),
    "t3_supertrend": ("Krypto", "4h"),
    "rsi2_crypto": ("Krypto", "1d"),
    "rsi2_mean_reversion": ("Aktien", "1d"),
    "turtle_soup_crypto": ("Krypto", "1d"),
    "turtle_soup_stocks": ("Aktien", "1d"),
    "volatility_breakout": ("Aktien", "1d"),
    "volatility_breakout_crypto": ("Krypto", "1d"),
}


def read_live_params(bot: str) -> dict:
    """Liest die Top-Level-Zuweisungen einer live_params.py per AST aus -
    ohne das Modul zu importieren (kein Ausfuehren von Bot-Code)."""
    path = os.path.join(STRATEGIES_DIR, bot, "live_params.py")
    with open(path) as f:
        source = f.read()

    values = {}
    for node in ast.parse(source).body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                try:
                    values[target.id] = ast.literal_eval(node.value)
                except ValueError:
                    values[target.id] = "<nicht literal auswertbar>"
    return values


def classify(bot: str, params: dict) -> dict:
    """Ordnet einen Bot genau einer der drei Kategorien zu (siehe Modul-Docstring)."""
    has_stop_loss_pct = "STOP_LOSS_PCT" in params
    stop_loss_pct = params.get("STOP_LOSS_PCT")
    has_stop_mode = "STOP_MODE" in params
    stop_mode = params.get("STOP_MODE")

    if has_stop_loss_pct and isinstance(stop_loss_pct, (int, float)):
        category = "fixed_pct"
        mechanism = f"fester Stop-Loss {float(stop_loss_pct):.1f} % unter Einstieg"
    elif has_stop_mode and stop_mode is not None:
        category = "structural"
        mechanism = f'struktureller Stop (STOP_MODE = "{stop_mode}")'
    elif (has_stop_loss_pct and stop_loss_pct is None) or (has_stop_mode and stop_mode is None):
        category = "none"
        mechanism = "kein Stop-Loss (bewusste, empirisch validierte Designentscheidung)"
    else:
        # Kein bekanntes Stop-Feld gefunden - NICHT stillschweigend als
        # "kein Stop" verbuchen, sondern als offener Fall melden.
        category = "unknown"
        mechanism = "kein bekanntes Stop-Feld in live_params.py gefunden - manuell pruefen"

    market, timeframe = MARKET.get(bot, ("?", "?"))
    return {
        "bot": bot,
        "market": market,
        "timeframe": timeframe,
        "category": category,
        "mechanism": mechanism,
        "stop_loss_pct": stop_loss_pct if isinstance(stop_loss_pct, (int, float)) else None,
        "stop_mode": stop_mode if has_stop_mode else None,
        "max_hold_days": params.get("MAX_HOLD_DAYS"),
        "allocation_pct": params.get("ALLOCATION_PCT"),
        "max_concurrent_positions": params.get("MAX_CONCURRENT_POSITIONS", "<nicht dokumentiert>"),
        "in_scope": category == "fixed_pct",
    }


def check_completeness() -> list:
    """Meldet Bot-Ordner mit live_params.py, die nicht in KNOWN_BOTS stehen -
    verhindert, dass ein spaeter ergaenzter Bot stillschweigend aus der
    Bestandsaufnahme faellt."""
    on_disk = sorted(
        d for d in os.listdir(STRATEGIES_DIR)
        if os.path.isfile(os.path.join(STRATEGIES_DIR, d, "live_params.py"))
    )
    return [b for b in on_disk if b not in KNOWN_BOTS]


def build_inventory() -> dict:
    rows = [classify(bot, read_live_params(bot)) for bot in KNOWN_BOTS]
    unexpected = check_completeness()
    return {
        "bots": rows,
        "in_scope": [r["bot"] for r in rows if r["in_scope"]],
        "out_of_scope_structural": [r["bot"] for r in rows if r["category"] == "structural"],
        "out_of_scope_no_stop": [r["bot"] for r in rows if r["category"] == "none"],
        "unclassified": [r["bot"] for r in rows if r["category"] == "unknown"],
        "unexpected_bot_dirs": unexpected,
    }


def main():
    inv = build_inventory()

    header = f"{'Bot':<28} {'Markt':<7} {'TF':<4} {'Kategorie':<12} Mechanismus"
    print(header)
    print("-" * len(header))
    for row in inv["bots"]:
        print(f"{row['bot']:<28} {row['market']:<7} {row['timeframe']:<4} "
              f"{row['category']:<12} {row['mechanism']}")

    print()
    print(f"UNTERSUCHT (fester %-Stop):        {len(inv['in_scope'])} Bots - {', '.join(inv['in_scope'])}")
    print(f"NICHT untersucht (struktureller Stop): {len(inv['out_of_scope_structural'])} Bots - "
          f"{', '.join(inv['out_of_scope_structural']) or '-'}")
    print(f"NICHT untersucht (kein Stop):      {len(inv['out_of_scope_no_stop'])} Bots - "
          f"{', '.join(inv['out_of_scope_no_stop']) or '-'}")
    if inv["unclassified"]:
        print(f"WARNUNG - nicht klassifizierbar:   {', '.join(inv['unclassified'])}")
    if inv["unexpected_bot_dirs"]:
        print(f"WARNUNG - unbekannte Bot-Ordner:   {', '.join(inv['unexpected_bot_dirs'])}")

    if "--json" in sys.argv:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        out_path = os.path.join(RESULTS_DIR, "stop_inventory.json")
        with open(out_path, "w") as f:
            json.dump(inv, f, indent=2)
        print(f"\nGespeichert: {out_path}")


if __name__ == "__main__":
    main()
