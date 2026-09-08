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
# rsi2_crypto berechnet die Allokation seit der Import-Umstellung aus
# live_params.ALLOCATION_PCT (10 %) - der Backtest rechnet weiter mit dem
# Anteil 0.10. Genau dieser Fall wurde vom Check zunaechst falsch als
# Abweichung gemeldet, weil ast.literal_eval eine Division nicht auswerten
# kann; er muss als abgeleitet und damit synchron gelten.
entry = st.compare_bot("rsi2_crypto")
row = rows_of(entry, "ALLOCATION_PCT")
check("aus live_params berechnete Allokation gilt als synchron, nicht als Abweichung",
      row["status"] == "aus live_params abgeleitet", str(row))
check("der Einheitenunterschied wird im Hinweis genannt",
      "Prozent" in row.get("hinweis", ""), str(row.get("hinweis")))
check("und der Bot erscheint deswegen nicht als abweichend",
      not any(d["groesse"] == "ALLOCATION_PCT" for d in entry["abweichungen"]),
      str(entry["abweichungen"]))
# turtle_soup_stocks fuehrt live 2 % gegen 0.10 - echte Abweichung.
row = rows_of(st.compare_bot("turtle_soup_stocks"), "ALLOCATION_PCT")
check("2 % (live) gegen 0.10 (Backtest) wird als Abweichung erkannt",
      row["status"] == "ABWEICHUNG", str(row))

# ---------------------------------------------------------------------------
print("\n3) Namens-Aliase")
# ---------------------------------------------------------------------------
# Seit der Import-Umstellung kommen diese Groessen per Alias-Import herein
# (`from live_params import T3_FAST_LENGTH as T3_FAST`) - sie stehen also
# nicht mehr als eigene Konstante im Backtest-Skript. Geprueft wird deshalb
# beides: dass der Import samt Alias aufgeloest wird, und dass die Groesse
# unter ihrem LIVE-Namen als referenziert gemeldet wird.
importiert = st.live_import_namen(
    os.path.join(st.STRATEGIES, "t3_supertrend", "equity_simulation.py"))
check("Alias-Import T3_FAST_LENGTH as T3_FAST wird aufgeloest",
      importiert.get("T3_FAST") == "T3_FAST_LENGTH", str(importiert))
row = rows_of(st.compare_bot("t3_supertrend"), "T3_FAST_LENGTH")
check("T3_FAST_LENGTH wird als im Backtest referenziert gemeldet",
      row is not None and row["status"] == "im Backtest referenziert", str(row))
importiert = st.live_import_namen(
    os.path.join(st.STRATEGIES, "rsi2_crypto", "equity_simulation.py"))
check("Alias-Import SMA_TREND_FILTER as SMA_TREND_PERIOD wird aufgeloest",
      importiert.get("SMA_TREND_PERIOD") == "SMA_TREND_FILTER", str(importiert))

# ---------------------------------------------------------------------------
print("\n3b) Referenz-Pruefung per AST statt Textsuche")
# ---------------------------------------------------------------------------
# Regressionstest fuer einen konkret aufgetretenen Fehlbefund: nachdem
# equity_simulation.py von volatility_breakout_crypto einen Kommentar bekam,
# der BTC_REGIME_FILTER_ENABLED erwaehnt, meldete die damalige Textsuche den
# Bot als synchron - und verschluckte damit die wichtigste Abweichung des
# ganzen Berichts. Ueber den AST darf das nicht passieren.
_tmp = os.path.join(tempfile.mkdtemp(), "beispiel.py")
with open(_tmp, "w") as fh:
    fh.write("# BTC_REGIME_FILTER_ENABLED wird hier nur erwaehnt\n"
             '"""auch im Docstring: BTC_REGIME_FILTER_ENABLED"""\n'
             "X = 1\n")
check("ein nur in Kommentar/Docstring erwaehnter Name gilt NICHT als referenziert",
      "BTC_REGIME_FILTER_ENABLED" not in st.referenzierte_namen(_tmp))
with open(_tmp, "w") as fh:
    fh.write("Y = BTC_REGIME_FILTER_ENABLED\n")
check("ein im Code benutzter Name gilt als referenziert",
      "BTC_REGIME_FILTER_ENABLED" in st.referenzierte_namen(_tmp))
check("und der echte Bot meldet den Regimefilter weiterhin als wirkungslos",
      any(d["groesse"] == "BTC_REGIME_FILTER_ENABLED"
          for d in st.compare_bot("volatility_breakout_crypto")["abweichungen"]))

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
# Stand nach der Import-Umstellung (PR #31 fuer elliott_wave, danach die
# uebrigen): elliott_wave_stocks ist synchron, seit sein Backtest
# USE_TAKE_PROFIT aus live_params.py liest. Offen sind noch die drei Bots
# mit ECHTEN Wertunterschieden, ueber die der Nutzer entscheiden muss, plus
# der Regimefilter bei volatility_breakout_crypto (fehlendes Verhalten, kein
# Konstanten-Problem).
check("genau die vier noch offenen Bots weichen ab",
      divergent == {"rsi2_mean_reversion", "turtle_soup_stocks",
                     "volatility_breakout", "volatility_breakout_crypto"}, str(divergent))
check("die uebrigen fuenf sind synchron",
      {e["bot"] for e in report if e["synchron"]}
      == {"elliott_wave", "elliott_wave_stocks", "t3_supertrend",
          "rsi2_crypto", "turtle_soup_crypto"},
      str({e["bot"] for e in report if e["synchron"]}))
check("jede gemeldete Abweichung hat eine Art (Konstante, Backtest-Default oder Verhalten)",
      all(d["art"] in ("Konstante", "Backtest-Default", "Verhalten")
          for e in report for d in e["abweichungen"]))
check("kein Bot meldet eine Abweichung ohne konkrete Groesse",
      all(d.get("groesse") for e in report for d in e["abweichungen"]))

print("\n" + "=" * 60)
print(f"{PASSED} Checks bestanden, {FAILED} fehlgeschlagen.")
print("=" * 60)
sys.exit(1 if FAILED else 0)
