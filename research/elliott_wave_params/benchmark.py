"""
Buy-and-Hold-Referenz fuer jedes Fenster
====================================================================
Pflichtreferenz des Projekts: gleichgewichtetes Kaufen-und-Halten
derselben Symbole ueber genau denselben Zeitraum. Ohne sie sagt eine
Renditezahl nichts - besonders bei Aktien, wo die Auswahl aus den
heutigen groessten S&P-500-Werten besteht (Survivorship Bias) und ein
Grossteil der Bewegung schlicht Marktrendite ist.

Berechnet wird die Referenz fuer alle Fenster, die in dieser
Untersuchung vorkommen: gesamt, In-Sample, Out-of-Sample und die drei
Walk-Forward-Testfenster.

Nutzung:  python3 benchmark.py <elliott_wave|elliott_wave_stocks>
"""

import json
import os

import botenv

BOT = botenv.bot_from_argv()

import engine        # noqa: E402
import walkforward as wf   # noqa: E402


def main():
    botenv.print_hinweis()
    windows = engine.load_windows()
    base = windows[engine.WINDOW_FULL]
    fold_windows, folds = wf.build_folds(base)
    windows.update({f["test"]: fold_windows[f["test"]] for f in folds})

    out = {"hinweis": botenv.UNVALIDIERT_HINWEIS, "bot": BOT, "startkapital": float(__import__("equity_simulation").STARTING_CAPITAL),
           "fenster": {}}
    print(f"{BOT}: gleichgewichtetes Buy-and-Hold je Fenster\n")
    print(f"  {'Fenster':<12}{'Symbole':>8}{'Rendite %':>12}{'Max DD %':>11}{'Calmar':>9}   Zeitraum")
    for name, data in windows.items():
        res = engine.buy_and_hold(data)
        start, end = engine.window_span(data)
        if res is None:
            continue
        res["zeitraum"] = {"von": start, "bis": end}
        out["fenster"][name] = res
        cal = "-" if res["calmar_ratio"] is None else f"{res['calmar_ratio']:.2f}"
        print(f"  {name:<12}{res['num_symbols']:>8}{res['total_return_pct']:>12.2f}"
              f"{res['max_drawdown_pct']:>11.2f}{cal:>9}   {start} .. {end}")

    path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_buyhold.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {path}")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()
