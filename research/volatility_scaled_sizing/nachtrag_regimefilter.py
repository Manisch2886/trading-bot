"""
Nachtrag: volatility_breakout_crypto mit aktiviertem BTC-Regimefilter
====================================================================================
PUNKTUELLE KORREKTUR EINER EINZIGEN ZEILE DIESER STUDIE.

Der Sync-Check (PR #24) hat belegt: `equity_simulation.py` von
volatility_breakout_crypto wendet den in `live_params.py` aktivierten
`BTC_REGIME_FILTER_ENABLED = True` nicht an. Diese Studie hat ihre Trades
ueber genau diese Funktion bezogen - die hier berichteten Zahlen fuer
volatility_breakout_crypto beruhen also auf einer Trade-Grundlage, die der
Live-Bot nie handelt.

Betroffen ist NUR dieser eine Bot. Die uebrigen acht werden hier bewusst
nicht angefasst: bei ihnen gibt es keinen Regimefilter, der im Backtest
fehlt (siehe research/sync_check/BERICHT.md, Schritt 1). Auch die Methodik
dieser Studie bleibt unveraendert - es wird ausschliesslich die
Trade-Grundlage ausgetauscht.

Verwendet werden:
  * die UNVERAENDERTEN Funktionen dieser Studie (`run_one_bot.load_bot_data`,
    `run_one_bot.analyze_period`, `vol_sizing_core`) - damit ist die
    Vergleichbarkeit zur Erstfassung konstruktiv gesichert, nicht behauptet;
  * die UNVERAENDERTEN Regimefilter-Funktionen des Bots
    (`regime_filter.compute_btc_regime` / `filter_trades_by_regime`) -
    dieselben, die `forward_test.py` live benutzt.

Regressionscheck vorweg: der ungefilterte Lauf muss die bereits
veroeffentlichten Werte aus results/volatility_breakout_crypto.json exakt
reproduzieren. Erst dann zaehlt der gefilterte Lauf.

Reine Backtest-Untersuchung. Keine Datei ausserhalb dieses Verzeichnisses
wird veraendert, keine Aktivierungsempfehlung.

Nutzung:  python3 nachtrag_regimefilter.py
"""

import json
import os
import sys

BOT = "volatility_breakout_crypto"
_DIR = os.path.dirname(os.path.abspath(__file__))

# run_one_bot.py liest den Bot-Namen aus sys.argv - hier gesetzt, damit
# dieselbe, unveraenderte Ladelogik benutzt werden kann.
sys.argv = [sys.argv[0], BOT]
sys.path.insert(0, _DIR)

import pandas as pd                                    # noqa: E402
import run_one_bot as rob                              # noqa: E402

RESULTS_DIR = rob.RESULTS_DIR
REFERENCE_PATH = os.path.join(RESULTS_DIR, f"{BOT}.json")
TOL = 0.011           # veroeffentlichte Werte sind auf 2 Stellen gerundet

PASSED = FAILED = 0


def check(label, actual, expected, tol=TOL):
    global PASSED, FAILED
    ok = abs(actual - expected) <= tol
    if ok:
        PASSED += 1
        print(f"  OK     {label:<52} {actual:>10.2f}")
    else:
        FAILED += 1
        print(f"  FEHLER {label:<52} {actual:>10.2f}  erwartet {expected:>10.2f}")


def calmar(total_return_pct, max_drawdown_pct):
    """Calmar-Konvention aller bisherigen Studien: Gesamtrendite / |Max DD|."""
    if max_drawdown_pct is None or abs(max_drawdown_pct) < 1e-12:
        return None
    return round(total_return_pct / abs(max_drawdown_pct), 2)


def with_calmar(period: dict) -> dict:
    out = dict(period)
    for variant in ("fixed", "vol_scaled"):
        row = dict(out[variant])
        row["calmar_ratio"] = calmar(row["total_return_pct"], row["max_drawdown_pct"])
        out[variant] = row
    return out


def main():
    if not os.path.exists(REFERENCE_PATH):
        raise SystemExit(f"{REFERENCE_PATH} fehlt - bitte zuerst run_all.py laufen lassen.")
    with open(REFERENCE_PATH) as handle:
        reference = json.load(handle)

    window = rob.VOL_WINDOW_BARS[BOT]
    trades, price_by_symbol, allocation, max_concurrent, train_ratio = rob.load_bot_data()

    entry_min, entry_max = trades["entry_time"].min(), trades["entry_time"].max()
    split_time = entry_min + (entry_max - entry_min) * train_ratio

    def periods_for(trade_set: pd.DataFrame) -> dict:
        return {
            "in_sample": rob.analyze_period(trade_set[trade_set["entry_time"] < split_time],
                                             price_by_symbol, window, allocation, max_concurrent),
            "out_of_sample": rob.analyze_period(trade_set[trade_set["entry_time"] >= split_time],
                                                 price_by_symbol, window, allocation, max_concurrent),
        }

    print("=" * 84)
    print("1) Regressionscheck - ungefiltert gegen die veroeffentlichten Werte dieser Studie")
    print("=" * 84)
    base = periods_for(trades)
    check("Trades gesamt", float(len(trades)), float(reference["total_trades"]), 0)
    for period in ("in_sample", "out_of_sample"):
        for variant in ("fixed", "vol_scaled"):
            for key in ("total_return_pct", "max_drawdown_pct"):
                check(f"{period} / {variant} / {key}",
                      base[period][variant][key], reference[period][variant][key])
        check(f"{period} / ausgefuehrte Trades",
              float(base[period]["fixed"]["num_executed"]),
              float(reference[period]["fixed"]["num_executed"]), 0)

    if FAILED:
        print(f"\n{FAILED} Abweichungen - der Nachtrag waere nicht belastbar. Abbruch.")
        sys.exit(1)

    print("\n" + "=" * 84)
    print("2) Gefilterte Trade-Grundlage (BTC_REGIME_FILTER_ENABLED = True)")
    print("=" * 84)
    # Die unveraenderten Bot-Funktionen - dieselben, die forward_test.py nutzt.
    from regime_filter import compute_btc_regime, filter_trades_by_regime
    import equity_simulation as es

    btc = es.load_all_symbol_data().get("BTCUSDT")
    if btc is None:
        raise SystemExit("BTCUSDT fehlt in den Kursdaten - Filter nicht anwendbar.")
    filtered = filter_trades_by_regime(trades, compute_btc_regime(btc))
    filtered = filtered.sort_values("entry_time", kind="stable").reset_index(drop=True)

    print(f"  Trades {len(trades)} -> {len(filtered)} "
          f"({round((1 - len(filtered) / len(trades)) * 100, 1)} % gestrichen)")
    filt = periods_for(filtered)

    print("\n" + "=" * 84)
    print("3) Gegenueberstellung (Rendite % / Max Drawdown % / Calmar)")
    print("=" * 84)
    print(f"  {'Periode':<15}{'Grundlage':<14}{'Variante':<13}{'ausgef.':>9}"
          f"{'Rendite':>10}{'Max DD':>10}{'Calmar':>9}")
    table = {}
    for period in ("in_sample", "out_of_sample"):
        table[period] = {"ohne_filter": with_calmar(base[period]),
                         "mit_filter": with_calmar(filt[period])}
        for label, block in (("ohne Filter", table[period]["ohne_filter"]),
                              ("MIT Filter", table[period]["mit_filter"])):
            for variant in ("fixed", "vol_scaled"):
                row = block[variant]
                print(f"  {period:<15}{label:<14}{variant:<13}{row['num_executed']:>9}"
                      f"{row['total_return_pct']:>9.2f}%{row['max_drawdown_pct']:>9.2f}%"
                      f"{str(row['calmar_ratio']):>9}")

    print("\n" + "=" * 84)
    print("4) Bewertung des urspruenglichen Befunds fuer diesen Bot")
    print("=" * 84)
    verdict = {}
    for period in ("in_sample", "out_of_sample"):
        for basis in ("ohne_filter", "mit_filter"):
            block = table[period][basis]
            fixed_c, scaled_c = block["fixed"]["calmar_ratio"], block["vol_scaled"]["calmar_ratio"]
            better = None if fixed_c is None or scaled_c is None else scaled_c > fixed_c
            verdict[f"{period}/{basis}"] = {
                "calmar_fixed": fixed_c, "calmar_vol_scaled": scaled_c,
                "calmar_diff": None if better is None else round(scaled_c - fixed_c, 2),
                "vol_sizing_besser": better,
            }
    for key, value in verdict.items():
        mark = "besser" if value["vol_sizing_besser"] else "schlechter"
        print(f"  {key:<30} Calmar {value['calmar_fixed']} -> {value['calmar_vol_scaled']} "
              f"({value['calmar_diff']:+.2f})  Vol-Sizing {mark}")

    both_before = (verdict["in_sample/ohne_filter"]["vol_sizing_besser"]
                   and verdict["out_of_sample/ohne_filter"]["vol_sizing_besser"])
    both_after = (verdict["in_sample/mit_filter"]["vol_sizing_besser"]
                  and verdict["out_of_sample/mit_filter"]["vol_sizing_besser"])
    print(f"\n  Urspruengliches Kriterium der Studie (Verbesserung IN-SAMPLE UND OUT-OF-SAMPLE):")
    print(f"    ohne Filter: {'erfuellt' if both_before else 'NICHT erfuellt'}"
          f"   |   mit Filter: {'erfuellt' if both_after else 'NICHT erfuellt'}")

    out = {
        "bot": BOT,
        "hinweis": ("Punktuelle Korrektur nur fuer diesen Bot. Die uebrigen acht Bots "
                    "dieser Studie sind nicht betroffen und wurden nicht neu gerechnet."),
        "regressionscheck_bestanden": PASSED,
        "trades": {"ohne_filter": int(len(trades)), "mit_filter": int(len(filtered)),
                   "gestrichen_pct": round((1 - len(filtered) / len(trades)) * 100, 1)},
        "split_time": str(split_time),
        "perioden": table,
        "bewertung": verdict,
        "kriterium_is_und_oos_besser": {"ohne_filter": both_before, "mit_filter": both_after},
    }
    out_path = os.path.join(RESULTS_DIR, f"{BOT}_regimefilter_nachtrag.json")
    with open(out_path, "w") as handle:
        json.dump(out, handle, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {out_path}")
    print(f"{PASSED} Referenzwerte bestaetigt, {FAILED} abweichend.")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
