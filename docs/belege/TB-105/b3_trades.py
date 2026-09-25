"""TB-105 B3 - Trade-Listen der drei Einbaustellen auf data/ im Speicher, als Hash (Sichtschutz 27.1: keine Zahl
ausser Hashes und Zeilenzahl-freien Merkmalen). Schreibt nichts ausser auf stdout.

Aufruf aus der Repo-Wurzel, OHNE Modus:
  trading-env/bin/python3 -W ignore docs/belege/TB-105/b3_trades.py <bot> [--ohne-btc]
  bot = t3_supertrend | volatility_breakout_crypto
Ausgabe je Stelle: <stelle> sha256(JSON, sort_keys) - oder bei --ohne-btc die Abbruchart und der Anfang der Meldung."""
import contextlib, hashlib, io, json, os, sys
bot = sys.argv[1]
ohne = "--ohne-btc" in sys.argv
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(_REPO, "strategies", bot))
sys.path.insert(0, os.path.join(_REPO, "shared"))
with contextlib.redirect_stdout(io.StringIO()):
    import equity_simulation as es
    import multi_symbol_optimise as mso
    all_data = es.load_all_symbol_data() if hasattr(es, "load_all_symbol_data") else mso.load_all_symbol_data()
print("# %s, BTCUSDT in all_data: %s, Symbole geladen: %s" % (bot, "BTCUSDT" in all_data, "ja" if all_data else "nein"))
if ohne:
    all_data = {k: v for k, v in all_data.items() if k != "BTCUSDT"}
    print("# --ohne-btc: BTCUSDT aus all_data entfernt")

def h(obj):
    if hasattr(obj, "to_json"):
        text = obj.to_json(orient="records", date_format="iso", double_precision=15)
        obj = json.loads(text)
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode("utf-8")).hexdigest()

def lauf(name, f):
    puffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(puffer):
            r = f()
        print("%-60s sha256 %s" % (name, h(r)))
        return r
    except SystemExit as e:
        print("%-60s ABBRUCH %s (%s): %s" % (name, type(e).__name__, "SystemExit" if isinstance(e, SystemExit) else "",
                                             str(e.code)[:160]))
        return None

if bot == "t3_supertrend":
    lauf("equity_simulation.collect_all_trades", lambda: es.collect_all_trades(
        all_data, es.T3_FAST, es.T3_SLOW, es.ADX_THRESHOLD, es.STOP_LOSS_PCT))
    lauf("multi_symbol_optimise.evaluate_combination_multi(live)", lambda: mso.evaluate_combination_multi(
        all_data, es.T3_FAST, es.T3_SLOW, es.ADX_THRESHOLD, es.STOP_LOSS_PCT))
elif bot == "volatility_breakout_crypto":
    t = lauf("equity_simulation.collect_all_trades", lambda: es.collect_all_trades(all_data, es.STOP_LOSS_PCT))
    if t is not None:
        lauf("equity_simulation.apply_btc_regime_filter", lambda: es.apply_btc_regime_filter(t, all_data))
else:
    raise SystemExit("unbekannter Bot")
