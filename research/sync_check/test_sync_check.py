"""
Sanity-Checks fuer den Sync-Check
======================================
Ohne Test-Framework, wie in allen Untersuchungen dieses Projekts.

Schwerpunkt liegt auf den drei Stellen, an denen ein naiver Vergleich
falsche Befunde erzeugt haette: Einheiten (Prozent vs. Anteil), Namens-
Aliase und Werte, die erst ueber den Default eines backtest_*.py-Moduls
wirksam werden.

Nutzung:  python3 test_sync_check.py
"""

import os
import sys
import tempfile

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import sync_table as st

PASSED = FAILED = 0


def check(label, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  OK    {label}")
    else:
        FAILED += 1
        print(f"  FEHLER {label}   {detail}")


def rows_of(entry, name):
    return next((r for r in entry["zeilen"] if r["groesse"] == name), None)


# ---------------------------------------------------------------------------
print("\n1) constants(): liest nur echte Konfigurationswerte")
# ---------------------------------------------------------------------------
with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
    f.write('"""Doku."""\nimport os\nA_VALUE = 3\nklein = 5\n_PRIVAT = 1\n'
            'LAST_UPDATED = "2026-01-01"\nBERECHNET = os.getcwd()\n')
    tmp = f.name
values = st.constants(tmp)
os.unlink(tmp)
check("Grossbuchstaben-Konstanten werden gelesen", values.get("A_VALUE") == 3)
check("kleingeschriebene Namen werden ignoriert", "klein" not in values)
check("private Namen werden ignoriert", "_PRIVAT" not in values)
check("LAST_UPDATED wird als rein dokumentarisch ignoriert", "LAST_UPDATED" not in values)
check("nicht literal auswertbare Ausdruecke stuerzen nicht ab",
      values.get("BERECHNET") == "<nicht literal auswertbar>", str(values))

# ---------------------------------------------------------------------------
print("\n2) Einheiten: Prozent (live) gegen Anteil (Backtest)")
# ---------------------------------------------------------------------------
# rsi2_crypto fuehrt live 10 % und im Backtest 0.10 - dieselbe Konfiguration.
entry = st.compare_bot("rsi2_crypto")
row = rows_of(entry, "ALLOCATION_PCT")
check("10 % (live) und 0.10 (Backtest) gelten als identisch",
      row["status"] == "identisch", str(row))
check("der Einheitenunterschied wird im Hinweis genannt",
      "Prozent" in row.get("hinweis", ""), str(row.get("hinweis")))
# turtle_soup_stocks fuehrt live 2 % gegen 0.10 - echte Abweichung.
row = rows_of(st.compare_bot("turtle_soup_stocks"), "ALLOCATION_PCT")
check("2 % (live) gegen 0.10 (Backtest) wird als Abweichung erkannt",
      row["status"] == "ABWEICHUNG", str(row))

# ---------------------------------------------------------------------------
print("\n3) Namens-Aliase")
# ---------------------------------------------------------------------------
row = rows_of(st.compare_bot("t3_supertrend"), "T3_FAST")
check("T3_FAST (Backtest) wird gegen T3_FAST_LENGTH (live) geprueft",
      row is not None and row["status"] == "identisch"
      and "T3_FAST_LENGTH" in row.get("hinweis", ""), str(row))
row = rows_of(st.compare_bot("rsi2_crypto"), "SMA_TREND_PERIOD")
check("SMA_TREND_PERIOD wird gegen SMA_TREND_FILTER geprueft",
      row is not None and row["status"] == "identisch", str(row))

# ---------------------------------------------------------------------------
print("\n4) Werte, die erst ueber den backtest_*.py-Default wirksam werden")
# ---------------------------------------------------------------------------
entry = st.compare_bot("volatility_breakout")
for name in ("MAX_HOLD_DAYS", "BB_LOOKBACK", "BB_SQUEEZE_PERCENTILE"):
    row = rows_of(entry, name)
    check(f"{name} wird ueber den Backtest-Default aufgeloest, nicht als wirkungslos gemeldet",
          row is not None and row["status"] == "identisch"
          and "Default" in row.get("hinweis", ""), str(row))
check("der abweichende Name SQUEEZE_LOOKBACK_DAYS wird im Hinweis genannt",
      "SQUEEZE_LOOKBACK_DAYS" in rows_of(entry, "BB_LOOKBACK").get("hinweis", ""))

# ---------------------------------------------------------------------------
print("\n5) Verhaltens-Abweichung: ein Flag ohne jede Entsprechung")
# ---------------------------------------------------------------------------
entry = st.compare_bot("volatility_breakout_crypto")
row = rows_of(entry, "BTC_REGIME_FILTER_ENABLED")
check("BTC_REGIME_FILTER_ENABLED wird als im Backtest wirkungslos erkannt",
      row is not None and "WIRKUNGSLOS" in row["status"], str(row))
check("und als Abweichung der Art 'Verhalten' gefuehrt",
      any(d["groesse"] == "BTC_REGIME_FILTER_ENABLED" and d["art"] == "Verhalten"
          for d in entry["abweichungen"]), str(entry["abweichungen"]))

# ---------------------------------------------------------------------------
print("\n6) Gesamtbild ueber alle 9 Bots")
# ---------------------------------------------------------------------------
report = [st.compare_bot(bot) for bot in st.BOTS]
check("alle 9 Bots werden geprueft", len(report) == 9)
divergent = {e["bot"] for e in report if not e["synchron"]}
check("genau die fuenf bekannten Bots weichen ab",
      divergent == {"elliott_wave_stocks", "rsi2_mean_reversion", "turtle_soup_stocks",
                     "volatility_breakout", "volatility_breakout_crypto"}, str(divergent))
check("die uebrigen vier sind synchron",
      {e["bot"] for e in report if e["synchron"]}
      == {"elliott_wave", "t3_supertrend", "rsi2_crypto", "turtle_soup_crypto"})
check("jede gemeldete Abweichung hat eine Art (Konstante, Backtest-Default oder Verhalten)",
      all(d["art"] in ("Konstante", "Backtest-Default", "Verhalten")
          for e in report for d in e["abweichungen"]))
check("kein Bot meldet eine Abweichung ohne konkrete Groesse",
      all(d.get("groesse") for e in report for d in e["abweichungen"]))

print("\n" + "=" * 60)
print(f"{PASSED} Checks bestanden, {FAILED} fehlgeschlagen.")
print("=" * 60)
sys.exit(1 if FAILED else 0)
