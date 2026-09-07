"""
Sanity-Checks fuer zigzag_confirm.py und die Ausstiegslogik
====================================================================
Bewusst ohne Test-Framework, wie in allen Vorgaenger-Untersuchungen.
Auf konstruierten Kursreihen, damit jeder erwartete Wert von Hand
nachrechenbar ist. Ob der Nachbau auf den ECHTEN Daten mit dem Bot
uebereinstimmt, prueft verify_baseline.py - hier geht es um die Logik.

Nutzung:  python3 test_lookahead.py
"""

import os
import sys

import numpy as np
import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from zigzag_confirm import calculate_zigzag_with_confirmation

PASSED = FAILED = 0


def check(label, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  OK    {label}")
    else:
        FAILED += 1
        print(f"  FEHLER {label}   {detail}")


def frame(prices):
    """Kursreihe ohne Intrabar-Spanne: high = low = close = der Wert.
    So ist jeder Zigzag-Schritt von Hand nachvollziehbar."""
    n = len(prices)
    return pd.DataFrame({
        "open_time": pd.date_range("2024-01-01", periods=n, freq="h"),
        "high": prices, "low": prices, "close": prices,
    })


print("\n1) Bestaetigungszeitpunkt")
# 100 -> 90 (Tief bei Index 2) -> 100. Bei 5 % Schwelle wird das Tief
# fixiert, sobald der Kurs 5 % darueber steigt: 90 * 1.05 = 94.5, das ist
# erstmals bei Index 4 (95) der Fall.
df = frame([100.0, 95.0, 90.0, 92.0, 95.0, 100.0, 105.0])
z = calculate_zigzag_with_confirmation(df, deviation_pct=5.0)
low = z[z["type"] == "low"]
check("das Tief wird als Pivot erkannt", len(low) == 1, str(z.to_dict("records")))
check("Pivot-Index zeigt auf das tatsaechliche Tief",
      int(low.iloc[0]["pivot_idx"]) == 2, str(low.iloc[0].to_dict()))
check("Bestaetigung erst beim Ueberschreiten der 5-%-Schwelle (Index 4)",
      int(low.iloc[0]["confirm_idx"]) == 4, str(low.iloc[0]["confirm_idx"]))
check("der Backtest kennt hier 2 Balken im Voraus",
      int(low.iloc[0]["confirm_idx"]) - int(low.iloc[0]["pivot_idx"]) == 2)
check("Bestaetigungszeit ist die Zeit des Bestaetigungsbalkens",
      pd.Timestamp(low.iloc[0]["confirm_time"]) == df["open_time"].iloc[4])

print("\n2) Die Kernaussage des Mechanismus")
# Zwischen Pivot und Bestaetigung kann der Kurs per Konstruktion nicht
# unter den Pivot fallen - der Pivot IST das Tief des Schenkels. Ein Stop
# unterhalb des Pivots ist in diesem Fenster daher unerreichbar.
pivot_price = float(low.iloc[0]["price"])
window = df["low"].values[int(low.iloc[0]["pivot_idx"]) + 1:int(low.iloc[0]["confirm_idx"]) + 1]
check("kein Kurs zwischen Pivot und Bestaetigung liegt unter dem Pivot",
      float(np.min(window)) >= pivot_price, f"{float(np.min(window))} < {pivot_price}")
check("bis zur Bestaetigung ist die Gegenbewegung mindestens so gross wie die Schwelle",
      (float(np.max(df['high'].values[2:5])) - pivot_price) / pivot_price * 100 >= 5.0)

print("\n3) Pivots identisch zur Originalfunktion (dieselbe Logik, nur mehr Spalten)")
# Nachbildung der Originalfunktion aus zigzag_indicator.py - hier lokal,
# damit der Test ohne Bot-Pfade laeuft.
def original_zigzag(df_, deviation_pct):
    highs, lows, times = df_["high"].values, df_["low"].values, df_["open_time"].values
    pivots, last_price, last_idx, trend = [], highs[0], 0, None
    for i in range(1, len(df_)):
        up = (highs[i] - last_price) / last_price * 100
        down = (last_price - lows[i]) / last_price * 100
        if trend is None:
            if up >= deviation_pct:
                trend, last_price, last_idx = "up", lows[last_idx], i
            elif down >= deviation_pct:
                trend, last_price, last_idx = "down", highs[last_idx], i
            continue
        if trend == "up":
            if highs[i] > last_price:
                last_price, last_idx = highs[i], i
            elif (last_price - lows[i]) / last_price * 100 >= deviation_pct:
                pivots.append((times[last_idx], last_price, "high"))
                trend, last_price, last_idx = "down", lows[i], i
        else:
            if lows[i] < last_price:
                last_price, last_idx = lows[i], i
            elif (highs[i] - last_price) / last_price * 100 >= deviation_pct:
                pivots.append((times[last_idx], last_price, "low"))
                trend, last_price, last_idx = "up", highs[i], i
    return pd.DataFrame(pivots, columns=["time", "price", "type"])

rng = np.random.default_rng(20260907)
noisy = frame(list(100 * np.cumprod(1 + rng.normal(0, 0.02, 800))))
for dev in (2.0, 4.0, 5.0):
    a = original_zigzag(noisy, dev)
    b = calculate_zigzag_with_confirmation(noisy, dev)
    check(f"deviation {dev} %: gleiche Pivot-Anzahl", len(a) == len(b), f"{len(a)} vs {len(b)}")
    check(f"deviation {dev} %: gleiche Preise und Typen",
          list(a["price"]) == list(b["price"]) and list(a["type"]) == list(b["type"]))
    check(f"deviation {dev} %: Bestaetigung nie vor dem Pivot",
          bool((b["confirm_idx"] >= b["pivot_idx"]).all()))

print("\n4) Ausstiegslogik (run_one_bot.simulate_exit)")
sys.argv = [sys.argv[0], "elliott_wave"]   # nur fuer den Modul-Import noetig
import run_one_bot as rob

# Stop und Ziel im selben Balken erreichbar -> der Stop gewinnt, wie im
# Original (backtest_elliott.simulate_trade prueft den Stop zuerst).
both = frame([100.0, 100.0, 100.0])
both.loc[1, "low"] = 90.0
both.loc[1, "high"] = 120.0
out = rob.simulate_exit(both, 0, 100.0, target_price=110.0, stop_price=95.0,
                        max_hold_bars=10, use_take_profit=True)
check("bei Stop UND Ziel im selben Balken gewinnt der Stop",
      out["result"] == "stop_loss", str(out))

# Der Einstiegsbalken selbst wird nie geprueft (Original: open_time > entry_time).
entry_bar = frame([100.0, 100.0, 100.0])
entry_bar.loc[0, "low"] = 50.0
out = rob.simulate_exit(entry_bar, 0, 100.0, 110.0, 95.0, 10, True)
check("der Einstiegsbalken loest keinen Stop aus (Pruefung ab dem Folgebalken)",
      out["result"] == "time_exit", str(out))

# max_hold begrenzt die Anzahl gepruefter Balken.
flat = frame([100.0] * 20)
out = rob.simulate_exit(flat, 0, 100.0, 999.0, 1.0, 5, True)
check("max_hold begrenzt die Haltedauer auf die vorgegebene Balkenzahl",
      out["exit_idx"] == 5, str(out))

check("ohne Folgebalken gibt es keinen Trade",
      rob.simulate_exit(frame([100.0]), 0, 100.0, 110.0, 95.0, 10, True) is None)

# Ohne Take-Profit darf das Ziel nie greifen.
rally = frame([100.0, 100.0, 100.0, 100.0])
rally.loc[1, "high"] = 500.0
out = rob.simulate_exit(rally, 0, 100.0, target_price=110.0, stop_price=1.0,
                        max_hold_bars=10, use_take_profit=False)
check("bei ausgeschaltetem Take-Profit wird das Ziel ignoriert",
      out["result"] == "time_exit", str(out))

print("\n" + "=" * 60)
print(f"{PASSED} Checks bestanden, {FAILED} fehlgeschlagen.")
print("=" * 60)
sys.exit(1 if FAILED else 0)
