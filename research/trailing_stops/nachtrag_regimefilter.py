"""
Nachtrag: volatility_breakout_crypto mit aktiviertem BTC-Regimefilter
====================================================================================
PUNKTUELLE KORREKTUR EINES EINZIGEN BOTS DIESER STUDIE.

Der Sync-Check (PR #24) hat belegt: `equity_simulation.py` von
volatility_breakout_crypto wendet den in `live_params.py` aktivierten
`BTC_REGIME_FILTER_ENABLED = True` nicht an. Diese Studie hat die
Einstiegssignale dieses Bots aus derselben Quelle abgeleitet - die hier
berichteten Zahlen beruhen also auf einer Trade-Grundlage, die der
Live-Bot nie handelt.

Betroffen ist NUR dieser Bot. Die Befunde zu `t3_supertrend` und
`volatility_breakout` bleiben unveraendert gueltig; bei ihnen fehlt im
Backtest kein Regimefilter (siehe research/sync_check/BERICHT.md,
Schritt 1). Die beiden Elliott-Wave-Bots waren schon in der Erstfassung
als nicht auswertbar eingestuft (Zigzag-Look-Ahead) - daran aendert der
Filter nichts.

Verwendet werden:
  * die UNVERAENDERTEN Funktionen dieser Studie (`run_one_bot.prepare`,
    `collect_trades`, `evaluate`, `slice_period`, `decision_basis`),
  * die UNVERAENDERTEN Regimefilter-Funktionen des Bots
    (`regime_filter.compute_btc_regime` / `filter_trades_by_regime`).

Damit ist dieser Nachtrag zugleich eine UNABHAENGIGE ZWEITE RECHNUNG zu
PR #22 (Vertiefungsstudie, Nachtrag N): dort laeuft dieselbe Frage ueber
ein anderes, eigenstaendiges Kernmodul. Stimmen beide ueberein, ist das
ein echter Gegencheck und keine Wiederholung derselben Zeile Code.

Regressionscheck vorweg: der ungefilterte Lauf muss die veroeffentlichten
Werte aus results/volatility_breakout_crypto_atr14.json exakt
reproduzieren. Erst dann zaehlt der gefilterte Lauf.

Reine Backtest-Untersuchung. Keine Datei ausserhalb dieses Verzeichnisses
wird veraendert, keine Aktivierungsempfehlung.

Nutzung:  python3 nachtrag_regimefilter.py
"""

import json
import os
import sys

BOT = "volatility_breakout_crypto"
ATR_WINDOW = 14
_DIR = os.path.dirname(os.path.abspath(__file__))

# run_one_bot.py liest Bot und ATR-Fenster aus sys.argv - hier gesetzt, damit
# dieselbe, unveraenderte Lade- und Auswertungslogik benutzt werden kann.
sys.argv = [sys.argv[0], BOT, str(ATR_WINDOW)]
sys.path.insert(0, _DIR)

import pandas as pd                                            # noqa: E402
import decision_basis as db                                    # noqa: E402
import run_one_bot as rob                                      # noqa: E402
from atr_core import calibrate_atr_multiplier                  # noqa: E402

STATIC = rob.STOP_FIXED_STATIC
FIXED_TRAILING = rob.STOP_FIXED_TRAILING
ATR_TRAILING = rob.STOP_ATR_TRAILING
VARIANTS = rob.VARIANTS

REFERENCE_PATH = os.path.join(rob.RESULTS_DIR, f"{BOT}_atr{ATR_WINDOW}.json")
TOL = 0.011

PASSED = FAILED = 0


def check(label, actual, expected, tol=TOL):
    global PASSED, FAILED
    if abs(actual - expected) <= tol:
        PASSED += 1
        print(f"  OK     {label:<56} {actual:>10.2f}")
    else:
        FAILED += 1
        print(f"  FEHLER {label:<56} {actual:>10.2f}  erwartet {expected:>10.2f}")


def main():
    if not os.path.exists(REFERENCE_PATH):
        raise SystemExit(f"{REFERENCE_PATH} fehlt - bitte zuerst run_all.py laufen lassen.")
    with open(REFERENCE_PATH) as handle:
        reference = json.load(handle)

    prepared, cfg = rob.prepare()
    baseline = rob.collect_trades(prepared, cfg, STATIC, k=None)

    # Bezugsgroessen bewusst aus dem UNGEFILTERTEN Satz: Trennzeitpunkt und
    # ATR-Multiplikator bleiben exakt die der Erstfassung. Sonst aenderten
    # sich Trade-Satz, Periodengrenzen und Stop-Distanz gleichzeitig und der
    # Unterschied waere keiner Ursache mehr zuzuordnen.
    entry_min, entry_max = baseline["entry_time"].min(), baseline["entry_time"].max()
    split_time = entry_min + (entry_max - entry_min) * cfg["train_split_ratio"]
    is_baseline = baseline[baseline["entry_time"] < split_time]
    k = calibrate_atr_multiplier(is_baseline["atr_at_entry"].to_numpy(),
                                  is_baseline["entry_price"].to_numpy(), cfg["stop_loss_pct"])

    unfiltered = {
        STATIC: baseline,
        FIXED_TRAILING: rob.collect_trades(prepared, cfg, FIXED_TRAILING, k=None),
        ATR_TRAILING: rob.collect_trades(prepared, cfg, ATR_TRAILING, k=k),
    }

    period_bounds = {
        "full": (entry_min, entry_max, True),
        "in_sample": (entry_min, split_time, False),
        "out_of_sample": (split_time, entry_max, True),
    }

    def periods_for(sets: dict) -> dict:
        return {name: {v: rob.evaluate(rob.slice_period(sets[v], lo, hi, inc), cfg)
                       for v in VARIANTS}
                for name, (lo, hi, inc) in period_bounds.items()}

    print("=" * 88)
    print("1) Regressionscheck - ungefiltert gegen die veroeffentlichten Werte dieser Studie")
    print("=" * 88)
    base_periods = periods_for(unfiltered)
    check("ATR-Multiplikator k", round(k, 4), reference["assumptions"]["atr_multiplier_k"], 0.0005)
    for name in period_bounds:
        for variant in VARIANTS:
            for key in ("total_return_pct", "max_drawdown_pct"):
                check(f"{name} / {variant} / {key}",
                      base_periods[name][variant][key], reference["periods"][name][variant][key])
            check(f"{name} / {variant} / ausgefuehrt",
                  float(base_periods[name][variant]["num_executed"]),
                  float(reference["periods"][name][variant]["num_executed"]), 0)

    if FAILED:
        print(f"\n{FAILED} Abweichungen - der Nachtrag waere nicht belastbar. Abbruch.")
        sys.exit(1)

    print("\n" + "=" * 88)
    print("2) Gefilterte Trade-Grundlage (BTC_REGIME_FILTER_ENABLED = True)")
    print("=" * 88)
    from regime_filter import compute_btc_regime, filter_trades_by_regime
    import equity_simulation as es

    btc = es.load_all_symbol_data().get("BTCUSDT")
    if btc is None:
        raise SystemExit("BTCUSDT fehlt in den Kursdaten - Filter nicht anwendbar.")
    regime = compute_btc_regime(btc)

    filtered = {}
    for variant, trades in unfiltered.items():
        kept = filter_trades_by_regime(trades, regime)
        filtered[variant] = kept.sort_values("entry_time", kind="stable").reset_index(drop=True)
        print(f"  {variant:<16} {len(trades):>4} -> {len(filtered[variant]):>4} Trades "
              f"({round((1 - len(filtered[variant]) / len(trades)) * 100, 1)} % gestrichen)")

    filt_periods = periods_for(filtered)

    print("\n" + "=" * 88)
    print("3) Gegenueberstellung (Rendite % / Max Drawdown % / Calmar)")
    print("=" * 88)
    print(f"  {'Periode':<15}{'Grundlage':<14}{'Variante':<17}{'ausgef.':>9}"
          f"{'Rendite':>10}{'Max DD':>10}{'Calmar':>9}")
    for name in period_bounds:
        for label, block in (("ohne Filter", base_periods[name]), ("MIT Filter", filt_periods[name])):
            for variant in VARIANTS:
                row = block[variant]
                print(f"  {name:<15}{label:<14}{variant:<17}{row['num_executed']:>9}"
                      f"{row['total_return_pct']:>9.2f}%{row['max_drawdown_pct']:>9.2f}%"
                      f"{str(row['calmar_ratio']):>9}")

    print("\n" + "=" * 88)
    print("4) Belastbarkeit auf gefilterter Grundlage - studieneigener Bootstrap und")
    print("   Reihenfolge-Permutationen (identische Einstellungen wie in der Erstfassung)")
    print("=" * 88)
    comparisons = [(FIXED_TRAILING, STATIC), (ATR_TRAILING, STATIC), (ATR_TRAILING, FIXED_TRAILING)]
    alloc_frac = cfg["allocation_pct"] / 100.0
    boot, ties = {}, {}
    for name, (lo, hi, inc) in period_bounds.items():
        sliced = {v: rob.slice_period(t, lo, hi, inc) for v, t in filtered.items()}
        ties[name] = db.tie_order_sensitivity(
            sliced, alloc_frac, cfg["max_concurrent_positions"], rob.STARTING_CAPITAL,
            rob.TIE_ORDER_PERMUTATIONS, rob.BOOTSTRAP_SEED)
        boot[name] = db.block_bootstrap(
            sliced, alloc_frac, cfg["max_concurrent_positions"], rob.STARTING_CAPITAL,
            rob.BOOTSTRAP_REPLICATES, rob.BOOTSTRAP_BLOCK_MONTHS, rob.BOOTSTRAP_SEED, comparisons)

    key = f"{ATR_TRAILING}_minus_{STATIC}"
    print(f"  P(ATR-Trailing besser als Baseline) in %   {'Calmar':>22}{'Max Drawdown':>18}")
    for name in period_bounds:
        ref_b = reference["bootstrap"].get(name, {}).get("differences", {}).get(key, {})
        new_b = boot[name].get("differences", {}).get(key, {})
        def share(block, metric):
            value = block.get(metric, {}).get("share_above_zero_pct")
            return "-" if value is None else f"{value:.1f}"
        print(f"    {name:<16} ohne Filter {share(ref_b,'calmar_ratio'):>10}"
              f"{share(ref_b,'max_drawdown_pct'):>18}")
        print(f"    {'':<16} MIT Filter  {share(new_b,'calmar_ratio'):>10}"
              f"{share(new_b,'max_drawdown_pct'):>18}")

    print("\n  Streuung allein durch die Reihenfolge gleichzeitiger Einstiege "
          "(Calmar, Gesamtzeitraum)")
    for variant in VARIANTS:
        block = ties["full"].get(variant, {}).get("calmar_ratio")
        if block:
            print(f"    {variant:<17} {block['min']:>7} .. {block['max']:>7}  "
                  f"(Median {block['median']}, berichtet "
                  f"{filt_periods['full'][variant]['calmar_ratio']})")

    out = {
        "bot": BOT,
        "atr_window_bars": ATR_WINDOW,
        "hinweis": ("Punktuelle Korrektur nur fuer diesen Bot. t3_supertrend und "
                    "volatility_breakout sind nicht betroffen und wurden nicht neu gerechnet."),
        "regressionscheck_bestanden": PASSED,
        "atr_multiplier_k": round(k, 4),
        "split_time": str(split_time),
        "trade_counts": {
            "ohne_filter": {v: int(len(t)) for v, t in unfiltered.items()},
            "mit_filter": {v: int(len(t)) for v, t in filtered.items()},
        },
        "periods_ohne_filter": base_periods,
        "periods_mit_filter": filt_periods,
        "bootstrap_mit_filter": boot,
        "tie_order_mit_filter": ties,
        "buy_and_hold": reference.get("buy_and_hold"),
    }
    out_path = os.path.join(rob.RESULTS_DIR, f"{BOT}_atr{ATR_WINDOW}_regimefilter_nachtrag.json")
    with open(out_path, "w") as handle:
        json.dump(out, handle, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {out_path}")
    print(f"{PASSED} Referenzwerte bestaetigt, {FAILED} abweichend.")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
