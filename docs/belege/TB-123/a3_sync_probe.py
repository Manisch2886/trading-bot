# TB-123: Status der drei Zeilen aus test_sync_check Abschnitt 4 (nur Konfigurationsvergleich, keine Backtest-Ausgabe)
import os, sys
wurzel = sys.argv[1]
sys.path.insert(0, os.path.join(wurzel, "research", "sync_check"))
import sync_table as st
print("wurzel", wurzel, "STRATEGIES", st.STRATEGIES)
e = st.compare_bot("volatility_breakout")
for name in ("MAX_HOLD_DAYS", "BB_LOOKBACK", "BB_SQUEEZE_PERCENTILE"):
    r = next((r for r in e["zeilen"] if r["groesse"] == name), None)
    print(name, "| status:", r and r["status"], "| hinweis:", r and r.get("hinweis"))
