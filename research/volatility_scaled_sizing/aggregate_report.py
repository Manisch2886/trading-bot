"""
Aggregiert die 9 pro-Bot results/<bot>.json-Dateien (erzeugt von
run_one_bot.py / run_all.py) zu einer uebergreifenden Zusammenfassungs-
Tabelle (siehe Aufgabenstellung, "Deliverable am Ende").

Reine Lese-/Auswertungs-Logik - fuehrt selbst KEINE Backtests aus,
importiert NICHTS aus strategies/.

Bewertungsmethodik (siehe auch Abschlussbericht, Abschnitt "Methodik der
Bewertung 'Verbesserung ja/nein/unklar'"):

  - Als Risikomass zum Vergleich von Rendite UND Drawdown gemeinsam wird
    eine einfache Calmar-Ratio (total_return_pct / abs(max_drawdown_pct))
    verwendet - bewusst NICHT Sharpe/Sortino, da keiner der 9 Bots diese
    Kennzahlen bereits verwendet (siehe Aufgaben-Vorgabe: nur einfuehren,
    wenn ein Bot es schon nutzt - das ist bei keinem der Fall).
  - "Verbesserung": vol-skaliert hat eine hoehere Calmar-Ratio als fix
    SOWOHL In-Sample ALS AUCH Out-of-Sample -> "ja". Fix hat in BEIDEN
    Perioden die hoehere Calmar-Ratio -> "nein". Widerspruechliche
    Richtung zwischen In-Sample und Out-of-Sample -> "unklar".
  - "Walk-Forward-Stabilitaet": Richtung des Calmar-Ratio-Vorteils
    (vol-skaliert besser / fix besser) wird pro Stabilitaets-Fenster
    bestimmt. Stimmt die Richtung in mindestens 3 der 4 Fenster ueberein
    -> "ja" (stabil). Sonst -> "nein" (Hinweis auf Parameter-Instabilitaet/
    Overfitting-Risiko, siehe Aufgaben-Vorgabe).

Nutzung:
    python3 aggregate_report.py
Schreibt summary_table.json und druckt eine lesbare Tabelle nach stdout.
"""
import os
import json

_RESEARCH_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(_RESEARCH_DIR, "results")

BOTS = [
    "elliott_wave",
    "elliott_wave_stocks",
    "t3_supertrend",
    "rsi2_crypto",
    "rsi2_mean_reversion",
    "turtle_soup_crypto",
    "turtle_soup_stocks",
    "volatility_breakout",
    "volatility_breakout_crypto",
]


def calmar(period_result: dict) -> float:
    """total_return_pct / abs(max_drawdown_pct). None bei Drawdown 0
    (kein sinnvoller Ratio moeglich) oder fehlenden Daten."""
    ret = period_result["total_return_pct"]
    dd = period_result["max_drawdown_pct"]
    if dd == 0:
        return None
    return ret / abs(dd)


def classify_improvement(data: dict) -> str:
    is_fixed = calmar(data["in_sample"]["fixed"])
    is_scaled = calmar(data["in_sample"]["vol_scaled"])
    oos_fixed = calmar(data["out_of_sample"]["fixed"])
    oos_scaled = calmar(data["out_of_sample"]["vol_scaled"])
    if None in (is_fixed, is_scaled, oos_fixed, oos_scaled):
        return "unklar"

    is_better = is_scaled > is_fixed
    oos_better = oos_scaled > oos_fixed

    if is_better and oos_better:
        return "ja"
    if not is_better and not oos_better:
        return "nein"
    return "unklar"


def classify_stability(data: dict) -> str:
    directions = []
    for window in data["stability_windows"]:
        res = window["result"]
        fixed_c = calmar(res["fixed"])
        scaled_c = calmar(res["vol_scaled"])
        if fixed_c is None or scaled_c is None:
            continue
        directions.append(scaled_c > fixed_c)

    if len(directions) < 3:
        return "unklar (zu wenige auswertbare Fenster)"

    agree_true = sum(directions)
    agree_false = len(directions) - agree_true
    majority = max(agree_true, agree_false)
    return "ja" if majority >= 3 else "nein"


def build_row(bot: str) -> dict:
    path = os.path.join(RESULTS_DIR, f"{bot}.json")
    with open(path) as f:
        data = json.load(f)

    return {
        "bot": bot,
        "assumptions": data["assumptions"],
        "total_trades": data["total_trades"],
        "in_sample_fixed_return_pct": data["in_sample"]["fixed"]["total_return_pct"],
        "in_sample_fixed_drawdown_pct": data["in_sample"]["fixed"]["max_drawdown_pct"],
        "in_sample_scaled_return_pct": data["in_sample"]["vol_scaled"]["total_return_pct"],
        "in_sample_scaled_drawdown_pct": data["in_sample"]["vol_scaled"]["max_drawdown_pct"],
        "out_of_sample_fixed_return_pct": data["out_of_sample"]["fixed"]["total_return_pct"],
        "out_of_sample_fixed_drawdown_pct": data["out_of_sample"]["fixed"]["max_drawdown_pct"],
        "out_of_sample_scaled_return_pct": data["out_of_sample"]["vol_scaled"]["total_return_pct"],
        "out_of_sample_scaled_drawdown_pct": data["out_of_sample"]["vol_scaled"]["max_drawdown_pct"],
        "out_of_sample_buy_and_hold_pct": data["out_of_sample"]["buy_and_hold"]["total_return_pct"],
        "improvement": classify_improvement(data),
        "walk_forward_stable": classify_stability(data),
    }


def main():
    rows = [build_row(bot) for bot in BOTS]

    out_path = os.path.join(_RESEARCH_DIR, "summary_table.json")
    with open(out_path, "w") as f:
        json.dump(rows, f, indent=2)

    header = (f"{'Bot':<28} {'IS fix':>8} {'IS vol':>8} {'OOS fix':>8} {'OOS vol':>8} "
              f"{'OOS DD fix':>11} {'OOS DD vol':>11} {'Verbess.':>9} {'WF stabil':>10}")
    print(header)
    print("-" * len(header))
    for row in rows:
        print(f"{row['bot']:<28} "
              f"{row['in_sample_fixed_return_pct']:>7.1f}% "
              f"{row['in_sample_scaled_return_pct']:>7.1f}% "
              f"{row['out_of_sample_fixed_return_pct']:>7.1f}% "
              f"{row['out_of_sample_scaled_return_pct']:>7.1f}% "
              f"{row['out_of_sample_fixed_drawdown_pct']:>10.1f}% "
              f"{row['out_of_sample_scaled_drawdown_pct']:>10.1f}% "
              f"{row['improvement']:>9} "
              f"{row['walk_forward_stable']:>10}")

    print(f"\nGeschrieben: {out_path}")


if __name__ == "__main__":
    main()
