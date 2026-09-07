"""
Beobachtung: in welcher Reihenfolge verarbeiten die LIVE-Bots ihre Symbole?
================================================================================
Punkt 5 der Aufgabenstellung - ausdruecklich NUR beschreiben, nicht
bewerten und nicht beheben.

Ermittelt rein lesend, (a) ob `forward_test.py` des jeweiligen Bots ein
Positionslimit ueberhaupt durchsetzt, (b) woher die Symbolliste stammt und
(c) wonach diese Liste sortiert ist.

Nutzung:  python3 live_order_observation.py
"""

import json
import os
import re

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
RESULTS_DIR = os.path.join(_DIR, "results")

BOTS = ["elliott_wave", "elliott_wave_stocks", "t3_supertrend",
        "rsi2_crypto", "rsi2_mean_reversion",
        "turtle_soup_crypto", "turtle_soup_stocks",
        "volatility_breakout", "volatility_breakout_crypto"]

# Woher die Symbollisten stammen und wonach sie sortiert sind - aus den
# Generator-Skripten abgelesen, nicht geraten.
SYMBOL_SOURCES = {
    "symbols_config": {
        "datei": "config/top25_symbols.txt",
        "erzeugt_von": "shared/get_top_symbols.py",
        "sortierung": "absteigend nach 24-Stunden-Handelsvolumen",
    },
    "stocks_symbols_config": {
        "datei": "config/sp500_top150.txt",
        "erzeugt_von": "strategies/elliott_wave_stocks/get_top_stocks.py",
        "sortierung": "absteigend nach Marktkapitalisierung",
    },
}


def inspect(bot: str) -> dict:
    path = os.path.join(_REPO_ROOT, "strategies", bot, "forward_test.py")
    if not os.path.exists(path):
        return {"bot": bot, "forward_test_vorhanden": False}
    source = open(path).read()

    import_match = re.search(r"from\s+(\w*symbols_config)\s+import\s+SYMBOLS", source)
    config_module = import_match.group(1) if import_match else None

    return {
        "bot": bot,
        "forward_test_vorhanden": True,
        "iteriert_ueber_symbols_liste": bool(re.search(r"for\s+symbol\s+in\s+SYMBOLS", source)),
        "sortiert_die_liste_selbst": bool(re.search(r"sorted\(\s*SYMBOLS", source)),
        "setzt_positionslimit_durch": "MAX_CONCURRENT_POSITIONS" in source
                                       and bool(re.search(r"open_count\s*>=\s*MAX_CONCURRENT_POSITIONS", source)),
        "symbol_konfiguration": config_module,
        "symbol_quelle": SYMBOL_SOURCES.get(config_module),
    }


def head_of(path: str, n: int = 8) -> list:
    full = os.path.join(_REPO_ROOT, path)
    if not os.path.exists(full):
        return []
    return [line.strip() for line in open(full) if line.strip()][:n]


def main():
    rows = [inspect(bot) for bot in BOTS]
    output = {
        "beobachtung": (
            "Die Live-Bots verarbeiten ihre Symbole in einer FESTEN, "
            "deterministischen Reihenfolge: der Reihenfolge der Symbolliste in "
            "der jeweiligen Konfigurationsdatei. Diese Listen sind nach "
            "Marktkapitalisierung (Aktien) bzw. 24-Stunden-Volumen (Krypto) "
            "absteigend sortiert. Wird das Positionslimit erreicht, erhalten "
            "damit systematisch die Symbole am Listenanfang den freien Platz."
        ),
        "listen_anfang": {
            "config/sp500_top150.txt": head_of("config/sp500_top150.txt"),
            "config/top25_symbols.txt": head_of("config/top25_symbols.txt"),
        },
        "bots": rows,
    }

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "live_order_observation.json"), "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"{'Bot':<28}{'iteriert SYMBOLS':>18}{'Limit durchgesetzt':>20}  Symbolliste")
    for row in rows:
        if not row["forward_test_vorhanden"]:
            print(f"{row['bot']:<28}{'kein forward_test.py':>38}")
            continue
        source = row["symbol_quelle"]
        print(f"{row['bot']:<28}{'ja' if row['iteriert_ueber_symbols_liste'] else 'nein':>18}"
              f"{'ja' if row['setzt_positionslimit_durch'] else 'nein':>20}  "
              f"{source['datei'] if source else '?'}")

    print("\nSortierung der Listen:")
    for name, info in SYMBOL_SOURCES.items():
        print(f"  {info['datei']:<28} {info['sortierung']}  (erzeugt von {info['erzeugt_von']})")
    print("\nAnfang der Listen:")
    for path, head in output["listen_anfang"].items():
        print(f"  {path:<28} {', '.join(head)}")


if __name__ == "__main__":
    main()
