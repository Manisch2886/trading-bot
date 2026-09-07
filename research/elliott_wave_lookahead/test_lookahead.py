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


def _raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


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

print("\n5) Kausale Wellenerkennung (elliott_wave_counter.find_causal_waves)")
import elliott_wave_counter as counter

# Acht Pivots, abwechselnd Hoch/Tief. Fenster 0-5 (Welle A) und Fenster 2-7
# (Welle B) sind BEIDE gueltige baerische Impulse und ueberlappen sich - und
# B hat den besseren Fibonacci-Score. Genau diese Konstellation loest den
# Look-Ahead aus: rueckblickend verdraengt B die frueher gehandelte Welle A.
PIVOT_PRICES = [100.0, 89.561, 95.94, 80.818, 89.023, 63.77, 70.041, 63.551]
PIVOT_TYPES = ["high", "low", "high", "low", "high", "low", "high", "low"]
# Bestaetigung jeweils zwei Balken nach dem Pivot; Pivots liegen 10 Balken auseinander.
PIVOT_IDX = [10 * i for i in range(8)]
CONFIRM_IDX = [idx + 2 for idx in PIVOT_IDX]
zz = pd.DataFrame({
    "time": pd.to_datetime([f"2024-01-01" for _ in PIVOT_IDX]) + pd.to_timedelta(PIVOT_IDX, unit="h"),
    "price": PIVOT_PRICES, "type": PIVOT_TYPES,
    "confirm_idx": CONFIRM_IDX, "pivot_idx": PIVOT_IDX,
    "confirm_time": pd.to_datetime(["2024-01-01"] * 8) + pd.to_timedelta(CONFIRM_IDX, unit="h"),
})

plain = counter.find_impulse_waves(zz[["time", "price", "type"]], min_fib_score=0.3)
bearish_plain = plain[plain["direction"] == "bearish"]
check("die Testreihe enthaelt zwei gueltige, ueberlappende baerische Wellen",
      len(bearish_plain) == 2, str(len(bearish_plain)))
scores = sorted(bearish_plain["fib_score"])
check("die spaetere der beiden hat den besseren Fibonacci-Score",
      scores == [0.67, 1.0], str(scores))

retro = counter.remove_overlapping(plain)
retro_bearish = retro[retro["direction"] == "bearish"]
check("rueckblickend bleibt nur EINE der beiden uebrig - die frueher gehandelte "
      "wird nachtraeglich verdraengt (das ist der Look-Ahead)",
      len(retro_bearish) == 1, str(len(retro_bearish)))
check("und zwar bleibt die spaetere, besser bewertete uebrig",
      float(retro_bearish.iloc[0]["fib_score"]) == 1.0)

causal = counter.find_causal_waves(zz, min_fib_score=0.3, freshness_bars=None, direction="bearish")
check("kausal bleiben BEIDE erhalten - die frueher gehandelte kann nicht mehr "
      "rueckwirkend gestrichen werden",
      len(causal) == 2, str(len(causal)))
check("beide Einstiege liegen NACH ihrer jeweiligen Bestaetigung",
      bool((causal["entry_idx"] >= causal["confirm_idx"]).all()),
      str(causal[["entry_idx", "confirm_idx"]].to_dict("records")))
check("jedes Wellenende loest hoechstens einen Trade aus",
      causal["end_time"].is_unique)
check("die Reihenfolge ist chronologisch nach Einstiegsbalken",
      list(causal["entry_idx"]) == sorted(causal["entry_idx"]))

# Frische-Fenster: die Bestaetigung liegt hier 2 Balken nach dem Pivot.
tight = counter.find_causal_waves(zz, min_fib_score=0.3, freshness_bars=1, direction="bearish")
check("ein zu enges Frische-Fenster verwirft beide Wellen (Bestaetigung kaeme zu spaet)",
      len(tight) == 0, str(len(tight)))
wide = counter.find_causal_waves(zz, min_fib_score=0.3, freshness_bars=2, direction="bearish")
check("ein Frische-Fenster von genau der Verzoegerung laesst beide zu",
      len(wide) == 2, str(len(wide)))

check("die Richtungsfilterung wirkt (bullische Wellen kommen nicht durch)",
      set(counter.find_causal_waves(zz, 0.3, None, "bearish")["direction"]) == {"bearish"})
both_dirs = counter.find_causal_waves(zz, 0.3, None, None)
check("ohne Richtungsfilter kommen mehr Wellen durch als mit",
      len(both_dirs) >= len(causal), f"{len(both_dirs)} vs {len(causal)}")

check("ohne Bestaetigungsspalte bricht find_causal_waves ab, statt still "
      "auf den alten Pfad zurueckzufallen",
      _raises(lambda: counter.find_causal_waves(zz[["time", "price", "type"]], 0.3), ValueError))
check("eine zu kurze Zigzag-Liste ergibt ein leeres, aber wohlgeformtes Ergebnis",
      counter.find_causal_waves(zz.head(3), 0.3).empty)

print("\n" + "=" * 60)
print(f"{PASSED} Checks bestanden, {FAILED} fehlgeschlagen.")
print("=" * 60)
sys.exit(1 if FAILED else 0)
