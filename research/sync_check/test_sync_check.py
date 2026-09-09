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
# Diese Pruefung stand frueher umgekehrt hier: turtle_soup_stocks fuehrte
# live 2 % gegen 0.10 im Backtest - eine echte Abweichung. PR #42 hat sie
# geschlossen, der Backtest leitet die Allokation seither aus live_params ab.
# Dass ein ECHTER Einheitenunterschied weiterhin auffiele, prueft jetzt
# Abschnitt 7 an einem gebauten Fall, statt darauf zu bauen, dass ein
# Bot kaputt bleibt.
row = rows_of(st.compare_bot("turtle_soup_stocks"), "ALLOCATION_PCT")
check("turtle_soup_stocks leitet die Allokation seit PR #42 aus live_params ab",
      row["status"] == "aus live_params abgeleitet", str(row))

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
# Diese Pruefung stand frueher umgekehrt hier ("meldet den Regimefilter
# weiterhin als wirkungslos") und beschrieb damit die damals offene Luecke.
# Seit PR #57 wendet equity_simulation.py den Filter an; die Pruefung haelt
# jetzt fest, dass er angewendet BLEIBT - baut jemand ihn wieder aus, faellt
# genau hier auf, dass Backtest und Live auseinanderlaufen.
check("der echte Bot meldet den Regimefilter NICHT mehr als Abweichung",
      not any(d["groesse"] == "BTC_REGIME_FILTER_ENABLED"
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
# Dieser Abschnitt fuehrte BTC_REGIME_FILTER_ENABLED als Musterfall vor: ein
# Flag, das live Verhalten steuert und im Backtest nirgends vorkam. Seit
# PR #57 ist genau dieser Fall geschlossen - der Musterfall taugt dafuer also
# nicht mehr. Geprueft wird jetzt beides: dass das Flag im Backtest ankommt
# (die Korrektur) und dass die Erkennung von Verhaltens-Abweichungen
# weiterhin funktioniert - vorgefuehrt an MAX_HOLD_DAYS, das bei diesem Bot
# nach wie vor ohne Entsprechung ist.
entry = st.compare_bot("volatility_breakout_crypto")
row = rows_of(entry, "BTC_REGIME_FILTER_ENABLED")
check("BTC_REGIME_FILTER_ENABLED wird im Backtest referenziert",
      row is not None and "referenziert" in row["status"], str(row))
check("und taucht nicht mehr unter den Abweichungen auf",
      not any(d["groesse"] == "BTC_REGIME_FILTER_ENABLED"
              for d in entry["abweichungen"]), str(entry["abweichungen"]))
# Diese Pruefung fuehrte in PR #57 MAX_HOLD_DAYS als noch offenen Fall vor.
# Seit die Import-Aufloesung greift (PR #58), hat kein Bot mehr eine
# Verhaltens-Abweichung - der Vorfuehrfall ist weg. Dass die Erkennung
# trotzdem funktioniert, prueft Abschnitt 7 an einem gebauten Bot; sich auf
# einen dauerhaft kaputten echten Bot zu stuetzen, waere ohnehin die
# schlechtere Zusicherung gewesen.
check("MAX_HOLD_DAYS ist bei diesem Bot ebenfalls aufgeloest",
      not any(d["groesse"] == "MAX_HOLD_DAYS" for d in entry["abweichungen"]),
      str(entry["abweichungen"]))

# ---------------------------------------------------------------------------
print("\n6) Gesamtbild ueber alle 9 Bots")
# ---------------------------------------------------------------------------
report = [st.compare_bot(bot) for bot in st.BOTS]
check("alle 9 Bots werden geprueft", len(report) == 9)
divergent = {e["bot"] for e in report if not e["synchron"]}
# Endstand der Aufraeumreihe: alle neun Bots synchron. Der Weg dorthin -
# PR #31 (elliott_wave), #24/#38 (elliott_wave_stocks), #40-42 (Allokation
# und Limits), #45 (Backtest-Defaults), #51/#52 (Indikatorwerte und
# MAX_HOLD_DAYS), #57 (BTC-Regimefilter), #58 (Import-Aufloesung im Check
# selbst).
#
# Diese Pruefung ist bewusst hart formuliert: schleicht sich irgendwo wieder
# eine Doppelfuehrung ein, faellt sie hier auf, ohne dass jemand die Tabelle
# lesen muss.
check("kein Bot weicht mehr ab", divergent == set(), str(divergent))
check("alle neun sind synchron",
      {e["bot"] for e in report if e["synchron"]} == set(st.BOTS),
      str({e["bot"] for e in report if e["synchron"]}))
check("jede gemeldete Abweichung hat eine Art (Konstante, Backtest-Default oder Verhalten)",
      all(d["art"] in ("Konstante", "Backtest-Default", "Verhalten")
          for e in report for d in e["abweichungen"]))
check("kein Bot meldet eine Abweichung ohne konkrete Groesse",
      all(d.get("groesse") for e in report for d in e["abweichungen"]))

# ---------------------------------------------------------------------------
print("\n7) Gegenprobe: wuerde eine ECHTE Abweichung noch auffallen?")
# ---------------------------------------------------------------------------
# Seit Abschnitt 6 alle neun Bots als synchron meldet, hat der Check keinen
# echten Fall mehr, an dem sich zeigen liesse, dass er ueberhaupt noch
# etwas findet. "Alles gruen" ist ohne diese Gegenprobe wertlos - genau die
# Falle, in die eine reine Zustandspruefung laeuft.
#
# Deshalb hier ein GEBAUTER Bot mit vier Groessen, je eine pro Ausgang. Er
# haengt an keinem echten Bot; niemand muss also kaputt bleiben, damit diese
# Zusicherung etwas wert ist.
_fake_root = tempfile.mkdtemp()
_fake_bot = os.path.join(_fake_root, "probebot")
os.makedirs(_fake_bot)
with open(os.path.join(_fake_bot, "live_params.py"), "w") as fh:
    fh.write("GEKOPPELT = 10\n"          # kommt per Import in den Backtest
             "ABWEICHEND = 20\n"          # Backtest fuehrt eine andere Zahl
             "OHNE_ENTSPRECHUNG = 30\n"   # taucht im Backtest nirgends auf
             "ALLOCATION_PCT = 2\n")      # Prozent gegen Anteil
with open(os.path.join(_fake_bot, "backtest_probe.py"), "w") as fh:
    fh.write("from live_params import GEKOPPELT\n"
             "ABWEICHEND = 99\n")
with open(os.path.join(_fake_bot, "equity_simulation.py"), "w") as fh:
    fh.write("ALLOCATION_PCT = 0.10\n")

_echte_strategies = st.STRATEGIES
st.STRATEGIES = _fake_root
try:
    probe = st.compare_bot("probebot")
    _row = rows_of(probe, "GEKOPPELT")
    check("importierter Wert gilt als synchron",
          _row is not None and _row["status"] == "identisch", str(_row))
    check("und erscheint nicht unter den Abweichungen",
          not any(d["groesse"] == "GEKOPPELT" for d in probe["abweichungen"]))

    check("eine abweichende Zahl im Backtest wird gemeldet",
          any(d["groesse"] == "ABWEICHEND" for d in probe["abweichungen"]),
          str(probe["abweichungen"]))

    check("ein Wert ohne jede Entsprechung wird als Verhalten gemeldet",
          any(d["groesse"] == "OHNE_ENTSPRECHUNG" and d["art"] == "Verhalten"
              for d in probe["abweichungen"]), str(probe["abweichungen"]))

    check("ein echter Einheitenunterschied (2 gegen 0.10) faellt weiterhin auf",
          any(d["groesse"] == "ALLOCATION_PCT" for d in probe["abweichungen"]),
          str(probe["abweichungen"]))

    check("der gebaute Bot gilt insgesamt als NICHT synchron",
          not probe["synchron"])
finally:
    st.STRATEGIES = _echte_strategies


print("\n" + "=" * 60)
print(f"{PASSED} Checks bestanden, {FAILED} fehlgeschlagen.")


print("=" * 60)
sys.exit(1 if FAILED else 0)
