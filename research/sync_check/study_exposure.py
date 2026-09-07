"""
Schritt 3: Rueckwirkung auf die fuenf bisherigen Profitabilitaets-Studien
==============================================================================
Die Aufgabenstellung geht davon aus, dass alle fuenf Studien auf den
Backtest-Daten von `equity_simulation.py` aufbauen und damit von den
Konfigurations-Abweichungen betroffen sind. Das trifft nur zum Teil zu -
die Studien nutzen UNTERSCHIEDLICHE Konfigurationsquellen. Diese Datei
haelt fest, welche das jeweils ist, mit Beleg, und leitet daraus die
Betroffenheit ab.

Die Belege stammen aus den Studien-Branches (PR #18-#22). Sie sind hier
als Zitat hinterlegt, damit der Befund auch nachvollziehbar bleibt, wenn
die Branches spaeter gemergt oder geloescht sind; `--verify` prueft sie
gegen die Branches nach, sofern diese lokal vorliegen.

Nutzung:  python3 study_exposure.py [--verify]
"""

import json
import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
RESULTS_DIR = os.path.join(_DIR, "results")

STUDIES = [
    {
        "pr": 18, "name": "Volatilitaets-skalierte Positionsgroessen",
        "branch": "origin/claude/vol-scaled-sizing-research",
        "datei": "research/volatility_scaled_sizing/run_one_bot.py",
        "quelle": "live_params.py",
        "beleg": "allocation_pct = lp.ALLOCATION_PCT",
        "erlaeuterung": (
            "Nutzt es.collect_all_trades() nur als Trade-Generator, alle Parameter "
            "aber aus live_params.py (Stop-Loss, Allokation, Positionslimit, "
            "USE_TAKE_PROFIT). Die Konstanten-Abweichungen wirken sich daher NICHT aus."),
        "bots": "alle 9",
    },
    {
        "pr": 19, "name": "Hierarchical Risk Parity",
        "branch": "origin/claude/hrp-portfolio-research",
        "datei": "research/hrp_portfolio/run_walk_forward.py",
        "quelle": "results/<bot>/equity_curve.csv ueber shared/portfolio_overview.py",
        "beleg": "import portfolio_overview as po",
        "erlaeuterung": (
            "Baut auf den gespeicherten Kapitalkurven auf. portfolio_overview.py "
            "bevorzugt die Live-DB, faellt aber auf results/<bot>/equity_curve.csv "
            "zurueck - und diese CSVs stammen aus Laeufen von equity_simulation.py, "
            "also aus der BACKTEST-Konfiguration. In dieser Sandbox sind keine "
            "Live-DBs vorhanden, der Fallback greift also durchgaengig."),
        "bots": "8 Bots mit equity_curve.csv",
    },
    {
        "pr": 20, "name": "Portfolioweiter Trend-Overlay",
        "branch": "origin/claude/trend-overlay-research",
        "datei": "research/trend_overlay/run_overlay_analysis.py",
        "quelle": "results/<bot>/equity_curve.csv ueber shared/portfolio_overview.py",
        "beleg": "import portfolio_overview as po",
        "erlaeuterung": "Dieselbe Datenquelle wie die HRP-Untersuchung.",
        "bots": "8 Bots mit equity_curve.csv",
    },
    {
        "pr": 21, "name": "Volatilitaets-kalibrierte Trailing-Stops",
        "branch": "origin/claude/new-session-sipd5l",
        "datei": "research/trailing_stops/run_one_bot.py",
        "quelle": "live_params.py",
        "beleg": "import live_params as lp",
        "erlaeuterung": (
            "Alle Parameter aus live_params.py. Der BTC-Regimefilter wird nur dort "
            "angewendet, wo die bot-eigene equity_simulation.py ihn anwendet "
            "(t3_supertrend) - bei volatility_breakout_crypto also nicht; das ist "
            "dort als Annahme 8 dokumentiert."),
        "bots": "5 Bots mit festem %-Stop",
    },
    {
        "pr": 22, "name": "Vertiefungsstudie volatility_breakout_crypto",
        "branch": "origin/claude/vbc-deepdive",
        "datei": "research/vbc_deepdive/run_deepdive.py",
        "quelle": "live_params.py",
        "beleg": "import live_params as lp",
        "erlaeuterung": (
            "Alle Parameter aus live_params.py, BTC-Regimefilter bewusst nicht "
            "angewendet (dort Annahme 8)."),
        "bots": "nur volatility_breakout_crypto",
    },
]

# Aus sync_table.py; die einzige Abweichung, die auch bei
# live_params.py-basierten Studien durchschlaegt, ist der BTC-Regimefilter -
# er ist kein Parameter, sondern fehlendes VERHALTEN in equity_simulation.py.
KONSTANTEN_ABWEICHEND = ["elliott_wave_stocks", "rsi2_mean_reversion",
                          "turtle_soup_stocks", "volatility_breakout"]
VERHALTEN_ABWEICHEND = ["volatility_breakout_crypto"]


def betroffenheit(study: dict) -> dict:
    if study["quelle"].startswith("live_params"):
        return {
            "stufe": "gering",
            "betroffene_bots": VERHALTEN_ABWEICHEND,
            "begruendung": ("Konstanten stammen aus live_params.py, die Abweichungen "
                             "wirken sich nicht aus. Betroffen bleibt allein der "
                             "BTC-Regimefilter bei volatility_breakout_crypto, weil "
                             "equity_simulation.py ihn gar nicht kennt."),
        }
    return {
        "stufe": "hoch",
        "betroffene_bots": KONSTANTEN_ABWEICHEND + VERHALTEN_ABWEICHEND,
        "begruendung": ("Baut auf den gespeicherten Kapitalkurven auf, die aus der "
                         "Backtest-Konfiguration stammen. Alle fuenf abweichenden Bots "
                         "gehen mit der falschen Konfiguration in die Analyse ein."),
    }


def verify(study: dict) -> str:
    """Prueft das Beleg-Zitat gegen den Studien-Branch, sofern lokal vorhanden."""
    ref = f"{study['branch']}:{study['datei']}"
    try:
        source = subprocess.check_output(["git", "show", ref], cwd=_REPO_ROOT,
                                          stderr=subprocess.DEVNULL, text=True)
    except subprocess.CalledProcessError:
        return "Branch nicht lokal vorhanden - nicht nachgeprueft"
    return "Beleg bestaetigt" if study["beleg"] in source else "BELEG NICHT GEFUNDEN"


def main():
    do_verify = "--verify" in sys.argv
    rows = []
    for study in STUDIES:
        row = dict(study)
        row["betroffenheit"] = betroffenheit(study)
        if do_verify:
            row["nachpruefung"] = verify(study)
        rows.append(row)

    print(f"{'PR':<5}{'Studie':<44}{'Konfigurationsquelle':<48}{'Betroffenheit':<10}")
    for row in rows:
        print(f"#{row['pr']:<4}{row['name'][:43]:<44}{row['quelle'][:47]:<48}"
              f"{row['betroffenheit']['stufe']:<10}")
        if do_verify:
            print(f"     Beleg `{row['beleg']}`: {row['nachpruefung']}")

    print("\nBetroffene Bots je Studie:")
    for row in rows:
        print(f"  #{row['pr']}: {', '.join(row['betroffenheit']['betroffene_bots'])}")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, "study_exposure.json")
    with open(path, "w") as f:
        json.dump({"studien": rows}, f, indent=2, ensure_ascii=False)
    print(f"\nGespeichert: {path}")


if __name__ == "__main__":
    main()
