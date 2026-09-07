"""
Symbol-Auswahl: bringt eine andere Auswahl etwas?
====================================================================
Die Aufgabe nennt ausdruecklich "ggf. andere Symbol-Auswahl" als
Richtung des erweiterten Suchraums. Das ist heikel: Symbole nach ihrem
Ergebnis auszuwaehlen ist die schnellste Art, sich einen Backtest
schoenzurechnen. Deshalb wird hier nicht optimiert, sondern gemessen:

1) Beitragsverteilung - wie viel des Ergebnisses haengt an wie wenigen
   Symbolen? Ein Kandidat, dessen gesamter Gewinn aus zwei von
   achtzehn Maerkten kommt, ist kein breit tragfaehiges Muster.

2) Ehrlicher Auswahltest - die Symbole werden AUSSCHLIESSLICH nach
   ihrem In-Sample-Ergebnis ausgewaehlt (positiver Ø PnL) und
   anschliessend unveraendert auf dem Out-of-Sample-Fenster
   ausgewertet. Bleibt der Vorteil dort bestehen, war die Auswahl
   echt; verschwindet er, war sie Rueckschau. Das ist derselbe
   IS/OOS-Trennstrich wie bei den Parametern.

Nutzung:  python3 symbols.py <elliott_wave|elliott_wave_stocks>
"""

import json
import os

import pandas as pd

import botenv

BOT = botenv.bot_from_argv()

import engine        # noqa: E402
import walkforward as wf   # noqa: E402


def per_symbol(trades: pd.DataFrame) -> pd.DataFrame:
    if trades is None or trades.empty:
        return pd.DataFrame()
    g = trades.groupby("symbol")["pnl_pct"]
    out = pd.DataFrame({"trades": g.size(), "summe_pnl_pct": g.sum().round(2),
                         "avg_pnl_pct": g.mean().round(2)})
    return out.sort_values("summe_pnl_pct", ascending=False)


def trades_for(all_data, window, key):
    waves = engine.waves_for(window, all_data, key[0])
    return engine.collect_trades(all_data, waves, key[1], key[2], key[3])


def main():
    botenv.print_hinweis()
    windows = engine.load_windows()
    candidates = wf.load_candidates()
    out = {"hinweis": botenv.UNVALIDIERT_HINWEIS, "bot": BOT, "kandidaten": []}

    for cand in candidates:
        key = cand["key"]
        name = wf.label(key)
        print(f"\n{'=' * 74}\n{name}   ({cand['herkunft']})\n{'=' * 74}")

        tr_full = trades_for(windows[engine.WINDOW_FULL], engine.WINDOW_FULL, key)
        tr_is = trades_for(windows[engine.WINDOW_IS], engine.WINDOW_IS, key)
        tr_oos = trades_for(windows[engine.WINDOW_OOS], engine.WINDOW_OOS, key)

        entry = {"kombination": name, "key": list(key), "herkunft": cand["herkunft"]}

        # --- 1) Beitragsverteilung auf dem Gesamtfenster --------------
        table = per_symbol(tr_full)
        if table.empty:
            print("  keine Trades")
            out["kandidaten"].append(entry)
            continue
        total = float(table["summe_pnl_pct"].sum())
        positive = table[table["summe_pnl_pct"] > 0]
        top3 = float(table["summe_pnl_pct"].head(3).sum())
        entry["beitrag"] = {
            "symbole_mit_trades": int(len(table)),
            "symbole_positiv": int(len(positive)),
            "summe_pnl_pct": round(total, 2),
            "top3_summe_pnl_pct": round(top3, 2),
            "top3_anteil_pct": (round(top3 / total * 100, 1) if abs(total) > 1e-9 else None),
            "bestes_symbol": table.index[0],
            "schlechtestes_symbol": table.index[-1],
            "tabelle": table.reset_index().to_dict("records"),
        }
        b = entry["beitrag"]
        print(f"  Beitrag (gesamt): {b['symbole_positiv']}/{b['symbole_mit_trades']} Symbole positiv, "
              f"Summe {b['summe_pnl_pct']} %, davon Top 3: {b['top3_summe_pnl_pct']} % "
              f"({b['top3_anteil_pct']} %)")

        # --- 2) ehrlicher Auswahltest --------------------------------
        is_table = per_symbol(tr_is)
        chosen = sorted(is_table[is_table["avg_pnl_pct"] > 0].index) if not is_table.empty else []
        entry["auswahl_nach_in_sample"] = {"anzahl": len(chosen), "symbole": chosen}
        if chosen and not tr_oos.empty:
            sub = tr_oos[tr_oos["symbol"].isin(chosen)]
            full_oos = engine.score_trades(tr_oos)
            sel_oos = engine.score_trades(sub)
            pf_full = engine.portfolio(tr_oos)
            pf_sel = engine.portfolio(sub)
            entry["auswahl_nach_in_sample"].update({
                "oos_alle_symbole": {**full_oos, **{f"pf_{k}": v for k, v in (pf_full or {}).items()}},
                "oos_nur_auswahl": {**sel_oos, **{f"pf_{k}": v for k, v in (pf_sel or {}).items()}},
            })
            print(f"  Auswahl nach In-Sample ({len(chosen)} Symbole) im Out-of-Sample:")
            print(f"    alle Symbole : {full_oos['num_trades']:>4} Trades, "
                  f"Ø PnL {full_oos['avg_return_pct']:>7.2f} %, Calmar {pf_full['calmar_ratio']}")
            print(f"    nur Auswahl  : {sel_oos['num_trades']:>4} Trades, "
                  f"Ø PnL {sel_oos['avg_return_pct']:>7.2f} %, Calmar {pf_sel['calmar_ratio']}")
        else:
            print("  Auswahl nach In-Sample: keine Symbole bzw. keine Out-of-Sample-Trades")

        out["kandidaten"].append(entry)

    path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_symbols.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {path}")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()
