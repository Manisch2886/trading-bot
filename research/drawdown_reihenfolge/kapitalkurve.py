"""
Frage 5: Welcher Drawdown ist der richtige? Der Gegencheck.
====================================================================
Aufruf:  python3 kapitalkurve.py <bot>

Beide Masse des Rasters - Blockreihenfolge und chronologisch - rechnen
auf der SUMME der Einzeltrade-Prozente. Das ist in beiden Faellen kein
Kapitalverlauf: jeder Trade zaehlt mit einer ganzen Einheit, obwohl der
Bot mit einem Kapitalanteil je Trade und (meist) einem Positionslimit
arbeitet. Ein Wert wie -2135 % ist als Kapital-Drawdown unmoeglich.

Den erlebbaren Verlauf hat das Projekt schon: `equity_simulation.py`
jedes Bots. Dieses Skript laesst je Rasterkombination die ECHTE
`simulate_portfolio` / `calculate_max_drawdown` des Bots mitlaufen -
auf der chronologisch sortierten Trade-Menge, so wie
`collect_all_trades` sie dem Bot uebergibt - und vergleicht dann die
RANGFOLGEN:

  * Welches der beiden Rastermasse ordnet die Kombinationen so, wie der
    Kapitalkurven-Calmar sie ordnet?
  * Wie weit liegen die drei Drawdown-Begriffe ueberhaupt auseinander?

Damit ist die Empfehlung am Ende keine Geschmacksfrage, sondern eine
gemessene.

Kein Bot-Code wird veraendert; `equity_simulation` wird als Bibliothek
gelesen, sein `__main__`-Block laeuft nicht (er wuerde
results/<bot>/equity_curve.csv ueberschreiben).
"""

import json
import os
import sys

import pandas as pd

import botenv


def rangkorrelation(a: pd.Series, b: pd.Series):
    """Spearman ohne scipy: Pearson auf den Raengen."""
    if len(a) < 3:
        return None
    return round(float(a.rank().corr(b.rank())), 3)


def main():
    botenv.print_hinweis()
    bot = botenv.bot_from_argv()

    import multi_symbol_optimise as mo
    import equity_simulation as es
    import adapters
    import engine

    ad = adapters.build(bot, mo)
    limit = getattr(es, "MAX_CONCURRENT_POSITIONS", None)
    print(f"\n=== {bot} ===")
    print(f"Kapitalsimulation des Bots: Startkapital {es.STARTING_CAPITAL}, "
          f"Allokation {es.ALLOCATION_PCT}, Positionslimit {limit}")

    data = mo.load_all_symbol_data()
    combos = ad.combinations()
    zeilen = []
    for i, combo in enumerate(combos, 1):
        trades, n_sym = ad.collect(data, combo)
        if trades is None:
            continue
        k = engine.kennzahlen(trades, n_sym, mo.calculate_robustness_score)
        if not ad.besteht_mindestfilter(trades, n_sym):
            continue

        # genau wie equity_simulation.collect_all_trades: chronologisch
        chrono = trades.sort_values("entry_time", kind="stable").reset_index(drop=True)
        res = es.simulate_portfolio(chrono, es.STARTING_CAPITAL, es.ALLOCATION_PCT, limit)
        kapital_dd = es.calculate_max_drawdown(res["equity_curve"], es.STARTING_CAPITAL)
        rendite = round((res["final_capital"] / es.STARTING_CAPITAL - 1) * 100, 2)
        calmar = round(rendite / abs(kapital_dd), 2) if abs(kapital_dd) > 1e-9 else None

        zeilen.append({
            "label": ad.label(combo), **ad.params(combo),
            "num_trades": k["num_trades"],
            "dd_block": k["dd_block"], "dd_entry": k["dd_entry"],
            "score_block": k["score_block"], "score_entry": k["score_entry"],
            "kapital_rendite_pct": rendite,
            "kapital_dd_pct": round(float(kapital_dd), 2),
            "kapital_calmar": calmar,
            "ausgefuehrt": int(res["num_executed"]),
            "uebersprungen": int(res["num_skipped"]),
        })
        z = zeilen[-1]
        print(f"[{i:>3}/{len(combos)}] {z['label']:<38} "
              f"DD Block {z['dd_block']:>9.2f} | chrono {z['dd_entry']:>9.2f} | "
              f"Kapital {z['kapital_dd_pct']:>7.2f} %  Calmar {z['kapital_calmar']}")

    if len(zeilen) < 3:
        print("\nZu wenige Kombinationen fuer eine Rangkorrelation.")
        return

    df = pd.DataFrame(zeilen)
    csv_path = os.path.join(botenv.RESULTS_DIR, f"{bot}_kapitalkurve.csv")
    df.to_csv(csv_path, index=False)

    erg = {
        "hinweis": botenv.HINWEIS, "bot": bot,
        "startkapital": es.STARTING_CAPITAL, "allocation_pct": es.ALLOCATION_PCT,
        "positionslimit": limit,
        "kombinationen": len(df),
        "spanne_dd_block": [float(df.dd_block.min()), float(df.dd_block.max())],
        "spanne_dd_entry": [float(df.dd_entry.min()), float(df.dd_entry.max())],
        "spanne_dd_kapital": [float(df.kapital_dd_pct.min()), float(df.kapital_dd_pct.max())],
        "rangkorr_score_block_vs_kapital_calmar":
            rangkorrelation(df.score_block, df.kapital_calmar),
        "rangkorr_score_entry_vs_kapital_calmar":
            rangkorrelation(df.score_entry, df.kapital_calmar),
        "rangkorr_ddblock_vs_ddkapital":
            rangkorrelation(df.dd_block.abs(), df.kapital_dd_pct.abs()),
        "rangkorr_ddentry_vs_ddkapital":
            rangkorrelation(df.dd_entry.abs(), df.kapital_dd_pct.abs()),
        "sieger_score_block": df.sort_values("score_block", ascending=False).iloc[0]["label"],
        "sieger_score_entry": df.sort_values("score_entry", ascending=False).iloc[0]["label"],
        "sieger_kapital_calmar": df.sort_values("kapital_calmar", ascending=False).iloc[0]["label"],
    }
    json_path = os.path.join(botenv.RESULTS_DIR, f"{bot}_kapitalkurve.json")
    with open(json_path, "w") as f:
        json.dump(erg, f, indent=2, default=str)

    print(f"\nSpanne Drawdown Blockreihenfolge : "
          f"{erg['spanne_dd_block'][0]} .. {erg['spanne_dd_block'][1]}")
    print(f"Spanne Drawdown chronologisch    : "
          f"{erg['spanne_dd_entry'][0]} .. {erg['spanne_dd_entry'][1]}")
    print(f"Spanne Drawdown Kapitalkurve     : "
          f"{erg['spanne_dd_kapital'][0]} .. {erg['spanne_dd_kapital'][1]}")
    print(f"\nRangkorrelation zum Kapitalkurven-Calmar:")
    print(f"  Block-Score        {erg['rangkorr_score_block_vs_kapital_calmar']}")
    print(f"  chronologisch      {erg['rangkorr_score_entry_vs_kapital_calmar']}")
    print(f"Rangkorrelation |Drawdown| zum Kapital-Drawdown:")
    print(f"  Blockreihenfolge   {erg['rangkorr_ddblock_vs_ddkapital']}")
    print(f"  chronologisch      {erg['rangkorr_ddentry_vs_ddkapital']}")
    print(f"\nSieger Block-Score      : {erg['sieger_score_block']}")
    print(f"Sieger chronologisch    : {erg['sieger_score_entry']}")
    print(f"Sieger Kapital-Calmar   : {erg['sieger_kapital_calmar']}")
    print(f"\nGeschrieben: {csv_path}\n             {json_path}")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()
