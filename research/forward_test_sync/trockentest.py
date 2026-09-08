"""Trockentest: laeuft forward_test.py bis zur Signal-Erzeugung durch?

Kein Netzabruf (Attrappe wirft), keine echte Datenbank (Temp-Datei), keine
echten Trades - aber derselbe Modulimport, dieselbe init_db(), dieselbe
compute_indicators/check_open_trades/find_new_signals-Kette wie im Cronjob.
Zweck: sicherstellen, dass der neue Import zur LAUFZEIT keinen Fehler wirft,
nicht nur beim py_compile.
"""
import importlib.util, os, sys, tempfile
import pandas as pd

BOT = sys.argv[1]
R = "/home/user/trading-bot"
sys.path[:0] = [f"{R}/strategies/{BOT}", f"{R}/shared",
                f"{R}/research/forward_test_sync/stubs"]

temp = tempfile.mkdtemp(prefix="trocken_")
import strategy_paths
echt = strategy_paths.get_strategy_paths
strategy_paths.get_strategy_paths = lambda f: {
    **echt(f), "DB_FILE": os.path.join(temp, "t.db"),
    "RESULTS_DIR": temp, "LOGS_DIR": temp}

spec = importlib.util.spec_from_file_location(
    "ft", f"{R}/strategies/{BOT}/forward_test.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print(f"Modulimport OK. MAX_HOLD_DAYS={getattr(m,'MAX_HOLD_DAYS','-')}, "
      f"RSI_THRESHOLD={getattr(m,'RSI_THRESHOLD','-')}")

conn = m.init_db()
print("init_db() OK - Tabellen angelegt")

daten = {}
for s in m.SYMBOLS[:5]:
    p = f"{R}/data/{s}_1d.csv"
    if os.path.exists(p):
        daten[s] = m.compute_indicators(pd.read_csv(p, parse_dates=["open_time"]))
print(f"compute_indicators() OK fuer {len(daten)} Symbole")

m.check_open_trades(conn, daten)
print("check_open_trades() OK")
m.find_new_signals(conn, daten)
print("find_new_signals() OK")
m.print_summary(conn)
print("\nTROCKENTEST DURCHGELAUFEN - kein Laufzeitfehler durch den Import.")
