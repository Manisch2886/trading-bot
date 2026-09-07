"""
Regressionscheck gegen BEIDE Vorgänger-Studien
====================================================
Diese Studie rechnet mit einem eigenen, aus zwei Branches
zusammengeführten Kernmodul (`vbc_core.py`). Bevor irgendein neues
Ergebnis als vertrauenswürdig gilt, muss dieses Modul die bereits
veröffentlichten Kennzahlen für volatility_breakout_crypto exakt
reproduzieren - und zwar aus DREI unabhängigen Richtungen:

  1. Baseline (fester 5 %-Stop, feste Positionsgrösse) - in BEIDEN
     Vorgänger-Studien identisch berichtet und dort jeweils gegen die
     unveränderte strategies/volatility_breakout_crypto/
     equity_simulation.py geprüft.
  2. Nur Vol-Sizing  -> research/volatility_scaled_sizing/ (PR #18)
  3. Nur ATR-Trailing -> research/trailing_stops/ (PR #21)

Zusätzlich wird die Baseline HIER noch einmal direkt gegen die
bot-eigene `equity_simulation.collect_all_trades()` geprüft - damit hängt
die Kette nicht allein an den Zahlen der Vorgänger-Berichte.

Die Referenzwerte unten sind wörtlich aus den Ergebnis-JSONs der beiden
Studien übernommen (nicht aus deren Fliesstext gerundet).

Nutzung:  python3 verify_reference.py
"""

import os
import sys

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import run_deepdive as rd
from vbc_core import (
    calibrate_atr_multiplier, STOP_FIXED_STATIC, STOP_ATR_TRAILING,
    VARIANT_BASELINE, VARIANT_VOL_SIZING, VARIANT_TRAILING,
)

# --- Referenzwerte: research/volatility_scaled_sizing/results/
#     volatility_breakout_crypto.json (PR #18) --------------------------------
VOLSIZING_REF = {
    "in_sample": {VARIANT_BASELINE: (40.89, -16.77), VARIANT_VOL_SIZING: (37.86, -15.17)},
    "out_of_sample": {VARIANT_BASELINE: (20.23, -11.33), VARIANT_VOL_SIZING: (16.20, -8.04)},
}
VOLSIZING_WINDOWS_REF = {
    1: {VARIANT_BASELINE: (-3.28, -16.77), VARIANT_VOL_SIZING: (-3.60, -15.63)},
    2: {VARIANT_BASELINE: (25.73, -6.68), VARIANT_VOL_SIZING: (21.22, -6.44)},
    3: {VARIANT_BASELINE: (38.12, -11.48), VARIANT_VOL_SIZING: (39.80, -10.35)},
    4: {VARIANT_BASELINE: (1.97, -11.33), VARIANT_VOL_SIZING: (0.00, -7.83)},
}

# --- Referenzwerte: research/trailing_stops/results/
#     volatility_breakout_crypto_atr14.json (PR #21) ---------------------------
TRAILING_REF = {
    "full": {VARIANT_BASELINE: (71.26, -16.77), VARIANT_TRAILING: (45.65, -5.76)},
    "in_sample": {VARIANT_BASELINE: (40.89, -16.77), VARIANT_TRAILING: (12.96, -5.76)},
    "out_of_sample": {VARIANT_BASELINE: (20.23, -11.33), VARIANT_TRAILING: (28.12, -5.58)},
}
TRAILING_WINDOWS_REF = {
    1: {VARIANT_TRAILING: (3.45, -4.87)},
    2: {VARIANT_TRAILING: (0.23, -5.43)},
    3: {VARIANT_TRAILING: (19.52, -3.20)},
    4: {VARIANT_TRAILING: (17.53, -5.58)},
}
TRAILING_K_REF = 0.8956
TRADE_COUNT_REF = {"static_stop": 359, "atr_trailing": 396}

TOL = 0.011   # Referenzwerte sind auf 2 Nachkommastellen gerundet gespeichert

PASSED = FAILED = 0


def check(label, actual, expected, tol=TOL):
    global PASSED, FAILED
    ok = abs(actual - expected) <= tol
    if ok:
        PASSED += 1
        print(f"  OK     {label:<62} {actual:>9.2f}")
    else:
        FAILED += 1
        print(f"  FEHLER {label:<62} {actual:>9.2f}  erwartet {expected:>9.2f}")


def main():
    import live_params as lp
    import multi_symbol_walk_forward as mswf

    cfg = {
        "allocation_pct": float(lp.ALLOCATION_PCT),
        "max_concurrent": lp.MAX_CONCURRENT_POSITIONS,
        "stop_loss_pct": float(lp.STOP_LOSS_PCT),
        "max_hold": int(lp.MAX_HOLD_DAYS),
        "train_split_ratio": mswf.TRAIN_SPLIT_RATIO,
    }

    prepared, warmup, _raw = rd.load_symbols()
    static = rd.collect_trades(prepared, warmup, STOP_FIXED_STATIC, cfg["stop_loss_pct"],
                                None, cfg["max_hold"])

    entry_min, entry_max = static["entry_time"].min(), static["entry_time"].max()
    split = entry_min + (entry_max - entry_min) * cfg["train_split_ratio"]
    is_static = static[static["entry_time"] < split]
    k = calibrate_atr_multiplier(is_static["atr_at_entry"].to_numpy(),
                                  is_static["entry_price"].to_numpy(), cfg["stop_loss_pct"])
    trailing = rd.collect_trades(prepared, warmup, STOP_ATR_TRAILING, cfg["stop_loss_pct"],
                                  k, cfg["max_hold"])
    sets = {False: static, True: trailing}

    print("\n0) Baseline direkt gegen den unveraenderten Bot-Code")
    import equity_simulation as es
    theirs = es.collect_all_trades(es.load_all_symbol_data(), stop_loss_pct=lp.STOP_LOSS_PCT,
                                    max_hold_days=lp.MAX_HOLD_DAYS)
    check("Anzahl Trades (Bot-eigene collect_all_trades)", float(len(static)), float(len(theirs)), 0)
    check("Summe PnL % (Bot-eigene collect_all_trades)",
          float(static["pnl_pct"].sum()), float(theirs["pnl_pct"].sum()))
    same_times = (pd.Timestamp(static["entry_time"].min()) == pd.Timestamp(theirs["entry_time"].min())
                  and pd.Timestamp(static["exit_time"].max()) == pd.Timestamp(theirs["exit_time"].max()))
    check("erster Entry / letzter Exit identisch", 1.0 if same_times else 0.0, 1.0, 0)

    print("\n1) Trade-Anzahlen und ATR-Multiplikator")
    check("Trades fester Stop", float(len(static)), float(TRADE_COUNT_REF["static_stop"]), 0)
    check("Trades ATR-Trailing", float(len(trailing)), float(TRADE_COUNT_REF["atr_trailing"]), 0)
    check("ATR-Multiplikator k", round(k, 4), TRAILING_K_REF, 0.0005)

    periods = {
        "full": rd.all_four(sets, cfg, entry_min, entry_max, include_hi=True),
        "in_sample": rd.all_four(sets, cfg, entry_min, split),
        "out_of_sample": rd.all_four(sets, cfg, split, entry_max, include_hi=True),
    }

    print("\n2) Referenzwerte der Vol-Sizing-Studie (PR #18)")
    for period, expectations in VOLSIZING_REF.items():
        for variant, (ret, dd) in expectations.items():
            row = periods[period][variant]
            check(f"{period} / {variant} / Rendite %", row["total_return_pct"], ret)
            check(f"{period} / {variant} / Max Drawdown %", row["max_drawdown_pct"], dd)

    print("\n3) Referenzwerte der Trailing-Stop-Studie (PR #21)")
    for period, expectations in TRAILING_REF.items():
        for variant, (ret, dd) in expectations.items():
            row = periods[period][variant]
            check(f"{period} / {variant} / Rendite %", row["total_return_pct"], ret)
            check(f"{period} / {variant} / Max Drawdown %", row["max_drawdown_pct"], dd)

    print("\n4) Walk-Forward-Fenster beider Studien (identische Fenstergrenzen)")
    edges = pd.date_range(entry_min, entry_max, periods=rd.NUM_STABILITY_WINDOWS + 1)
    for i in range(rd.NUM_STABILITY_WINDOWS):
        variants = rd.all_four(sets, cfg, edges[i], edges[i + 1],
                                include_hi=(i == rd.NUM_STABILITY_WINDOWS - 1))
        for source in (VOLSIZING_WINDOWS_REF, TRAILING_WINDOWS_REF):
            for variant, (ret, dd) in source.get(i + 1, {}).items():
                check(f"W{i + 1} / {variant} / Rendite %", variants[variant]["total_return_pct"], ret)
                check(f"W{i + 1} / {variant} / Max Drawdown %", variants[variant]["max_drawdown_pct"], dd)

    print("\n" + "=" * 78)
    print(f"{PASSED} Referenzwerte bestaetigt, {FAILED} abweichend.")
    print("Beide Vorgaenger-Studien exakt reproduziert." if not FAILED
          else "ABWEICHUNG - Ergebnisse dieser Studie sind NICHT belastbar.")
    print("=" * 78)
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
