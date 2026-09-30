# TB-124 A4: Status und Hinweis der BB-Zeilen und MAX_HOLD_DAYS (research/sync_check/sync_table.compare_bot) fuer
# beide Breakout-Bots, dazu die volle Tabelle aller neun Bots als Hash (Konfigurationsvergleich, keine Backtest-Ausgabe).
# Bauart docs/belege/TB-123/a3_sync_probe.py. Aufruf: trading-env/bin/python3 docs/belege/TB-124/a_sync_probe.py <wurzel>
import hashlib, os, sys
wurzel = sys.argv[1]
sys.path.insert(0, os.path.join(wurzel, "research", "sync_check"))
import sync_table as st
print("wurzel", wurzel)
tabelle = []
for bot in st.BOTS:
    e = st.compare_bot(bot)
    for r in e["zeilen"]:
        tabelle.append("%s %s | %s | %s" % (bot, r["groesse"], r["status"], r.get("hinweis")))
    tabelle.append("%s synchron %s %s" % (bot, e["synchron"], e["abweichungen"]))
    if bot.startswith("volatility_breakout"):
        for name in ("MAX_HOLD_DAYS", "BB_LOOKBACK", "BB_SQUEEZE_PERCENTILE"):
            r = next((r for r in e["zeilen"] if r["groesse"] == name), None)
            print(bot, name, "| status:", r and r["status"], "| hinweis:", r and r.get("hinweis"))
print("Tabelle aller neun Bots: %d Zeilen, sha256 %s" % (len(tabelle), hashlib.sha256("\n".join(tabelle).encode()).hexdigest()))
if len(sys.argv) > 2:
    open(sys.argv[2], "w").write("\n".join(tabelle) + "\n")
