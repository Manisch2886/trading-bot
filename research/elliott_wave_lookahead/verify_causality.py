"""
Kausalitaets-Nachweis fuer den korrigierten Backtest
====================================================================================
Prueft fuer JEDEN Trade, den `equity_simulation.collect_all_trades` erzeugt,
ob er ausschliesslich Informationen benutzt, die zu seinem
Einstiegszeitpunkt bereits verfuegbar waren. Nicht stichprobenartig -
jeder einzelne Trade.

--------------------------------------------------------------------
Wie geprueft wird
--------------------------------------------------------------------
Der entscheidende Punkt ist, dass die Gegenrechnung auf einem ECHT
ABGESCHNITTENEN Kurs-DataFrame laeuft (`price_df.iloc[:entry_idx + 1]`) -
nicht auf der vollen Historie mit nachtraeglichem Filter. Was dort nicht
sichtbar ist, kann auch nicht versehentlich einfliessen.

Fuenf Pruefungen je Trade:

  P1  Der Zigzag auf den abgeschnittenen Daten stimmt mit dem Zigzag auf der
      vollen Historie ueberein, sobald man diesen auf die bis dahin
      bestaetigten Pivots einschraenkt. Das ist die Grundlage von allem
      Weiteren: nur wenn der Indikator praefix-stabil ist, bedeutet
      "confirm_idx <= T" auch wirklich "war zu T bekannt".
  P2  Die gehandelte Welle ist in der Auswahl, die man zum Einstiegszeitpunkt
      allein aus den abgeschnittenen Daten getroffen haette
      (find_impulse_waves + die unveraenderte remove_overlapping auf dem
      Praefix). Das ist die eigentliche Kausalitaets-Pruefung: die Welle
      musste zu diesem Zeitpunkt schon ausgewaehlt worden sein - eine
      spaetere, besser bewertete Welle kann sie nicht mehr verdraengt haben.
  P3  Der Einstiegskurs ist der Schlusskurs des Einstiegsbalkens - ein Kurs,
      der zu diesem Zeitpunkt tatsaechlich am Markt stand.
  P4  Das Frische-Fenster aus forward_test.py ist eingehalten.
  P5  Der Ausstieg liegt NACH dem Einstieg, und jedes Wellenende loest
      hoechstens einen Trade aus (wie UNIQUE(symbol, signal_time) in der
      Live-Datenbank).

Nutzung:  python3 verify_causality.py <bot_name>
"""

import os
import sys

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import run_one_bot as rob   # noqa: E402  - bringt Pfade und Import-Stubs mit

BOT = rob.BOT

PASSED = FAILED = 0
FAILURES = []


def check(label, ok, detail=""):
    global PASSED, FAILED
    if ok:
        PASSED += 1
        print(f"  OK     {label}")
    else:
        FAILED += 1
        FAILURES.append(f"{label}: {detail}")
        print(f"  FEHLER {label}   {detail}")


def main():
    import equity_simulation as es
    import live_params as lp
    import backtest_elliott as bt
    import elliott_wave_counter as counter
    from zigzag_indicator import calculate_zigzag, calculate_zigzag_with_confirmation

    deviation_pct = float(lp.DEVIATION_PCT)
    freshness = bt.SIGNAL_FRESHNESS_BARS
    all_data = es.load_all_symbol_data()

    if BOT == "elliott_wave_stocks":
        trades = es.collect_all_trades(all_data, deviation_pct, lp.STOP_LOSS_PCT,
                                        lp.TAKE_PROFIT_FIB, lp.USE_TAKE_PROFIT)
    else:
        trades = es.collect_all_trades(all_data, deviation_pct, lp.STOP_LOSS_PCT,
                                        lp.TAKE_PROFIT_FIB)

    print(f"\n{BOT}: {len(trades)} Trades werden einzeln geprueft "
          f"(Frische-Fenster {freshness} Balken)\n")

    checked = 0
    v_prefix = v_selection = v_price = v_fresh = v_order = v_unique = 0

    for symbol, group in trades.groupby("symbol"):
        price_df = all_data[symbol]
        times = price_df["open_time"].to_numpy()
        closes = price_df["close"].to_numpy()
        time_to_idx = {pd.Timestamp(t): i for i, t in enumerate(times)}

        full_zigzag = calculate_zigzag_with_confirmation(price_df, deviation_pct=deviation_pct)
        pivot_by_time = dict(zip(pd.to_datetime(full_zigzag["time"]), full_zigzag["pivot_idx"]))

        seen_signals = set()
        for _, trade in group.iterrows():
            checked += 1
            entry_time = pd.Timestamp(trade["entry_time"])
            signal_time = pd.Timestamp(trade["signal_time"])
            entry_idx = time_to_idx.get(entry_time)
            if entry_idx is None:
                v_price += 1
                continue

            # --- Die Sicht des Bots zum Einstiegszeitpunkt: ECHT abgeschnitten
            prefix = price_df.iloc[:entry_idx + 1]
            prefix_zigzag = calculate_zigzag(prefix, deviation_pct=deviation_pct)

            # P1 - Praefix-Stabilitaet des Indikators
            known = full_zigzag[full_zigzag["confirm_idx"] <= entry_idx]
            same = (len(prefix_zigzag) == len(known)
                    and list(pd.to_datetime(prefix_zigzag["time"])) == list(pd.to_datetime(known["time"]))
                    and list(prefix_zigzag["price"]) == list(known["price"])
                    and list(prefix_zigzag["type"]) == list(known["type"]))
            if not same:
                v_prefix += 1

            # P2 - war die Welle zu diesem Zeitpunkt ausgewaehlt?
            if len(prefix_zigzag) >= 6:
                cand = counter.find_impulse_waves(prefix_zigzag, min_fib_score=0.3)
                kept = counter.remove_overlapping(cand) if not cand.empty else cand
                selected = (set(pd.to_datetime(kept[kept["direction"] == "bearish"]["end_time"]))
                            if not kept.empty else set())
            else:
                selected = set()
            if signal_time not in selected:
                v_selection += 1

            # P3 - Einstiegskurs ist der Schlusskurs des Einstiegsbalkens
            if abs(float(trade["entry_price"]) - float(closes[entry_idx])) > 1e-9:
                v_price += 1

            # P4 - Frische-Fenster
            pivot_idx = pivot_by_time.get(signal_time)
            if pivot_idx is None or entry_idx - int(pivot_idx) > freshness:
                v_fresh += 1

            # P5 - Reihenfolge und Eindeutigkeit
            exit_idx = time_to_idx.get(pd.Timestamp(trade["exit_time"]))
            if exit_idx is None or exit_idx <= entry_idx:
                v_order += 1
            if signal_time in seen_signals:
                v_unique += 1
            seen_signals.add(signal_time)

    print(f"Geprueft: {checked} von {len(trades)} Trades\n")
    check(f"P1  Zigzag ist praefix-stabil (abgeschnittene Daten = volle Daten bis confirm_idx)",
          v_prefix == 0, f"{v_prefix} Verletzungen")
    check(f"P2  jede gehandelte Welle war zum Einstieg bereits ausgewaehlt",
          v_selection == 0, f"{v_selection} Verletzungen")
    check(f"P3  Einstiegskurs = Schlusskurs des Einstiegsbalkens",
          v_price == 0, f"{v_price} Verletzungen")
    check(f"P4  Frische-Fenster ({freshness} Balken) eingehalten",
          v_fresh == 0, f"{v_fresh} Verletzungen")
    check(f"P5a Ausstieg liegt nach dem Einstieg", v_order == 0, f"{v_order} Verletzungen")
    check(f"P5b jedes Wellenende loest hoechstens einen Trade aus",
          v_unique == 0, f"{v_unique} Verletzungen")
    check(f"alle {len(trades)} Trades tatsaechlich geprueft (keiner uebersprungen)",
          checked == len(trades), f"{checked} von {len(trades)}")

    print("\n" + "=" * 72)
    print(f"{PASSED} Pruefungen bestanden, {FAILED} fehlgeschlagen "
          f"({checked} Trades einzeln geprueft).")
    print("KAUSAL SAUBER - kein Trade nutzt Informationen von nach seinem Einstieg."
          if not FAILED else "KAUSALITAETSVERLETZUNG:\n  - " + "\n  - ".join(FAILURES))
    print("=" * 72)
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
