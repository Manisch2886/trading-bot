"""TB-98 A1, Nachmessung zum Abbruch "Kennzeichnung hat die Simulation
veraendert": welche Teilbedingung von positionen_holen.py Z. 214-222 kippt,
und haengt es am Zufallsschluessel der Stufe 4 (shared/zuteilung.py Z. 492-497,
der die Spalte `symbol` in den Fingerabdruck nimmt)?

Rechnet nur im Speicher, schreibt nichts. OHNE Selektionsmodus (die Frage ist,
ob der Erzeuger mit dem heutigen Code ueberhaupt laeuft). Keine Trade-Zahlen
in der Ausgabe (27.1) - nur gleich/verschieden je Teilbedingung.

Aufruf (Repo-Wurzel):  python3 docs/belege/TB-98/a1_kennzeichnung.py <bot>
"""
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
bot = sys.argv[1]
sys.argv = [os.path.join(_REPO, "research", "tb24_haltedauern", "positionen_holen.py"), bot]
sys.path.insert(0, os.path.join(_REPO, "research", "tb24_haltedauern"))
import positionen_holen as ph   # noqa: E402
import pandas as pd              # noqa: E402
import equity_simulation as es   # noqa: E402
import zuteilung                 # noqa: E402

all_data = es.load_all_symbol_data()
trades = ph.basis.hole_trades(es, all_data).copy()
trades["entry_time"] = pd.to_datetime(trades["entry_time"])
trades["exit_time"] = pd.to_datetime(trades["exit_time"])
hat_limit = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
mc = getattr(es, "MAX_CONCURRENT_POSITIONS", None) if hat_limit else ph.basis._KEIN_LIMIT_PARAMETER


def lauf(t):
    return ph.basis.simuliere(es, t, es.ALLOCATION_PCT, mc)


def vergleich(a, b):
    ea, eb = a["equity_curve"], b["equity_curve"]
    return {
        "Laenge Kapitalkurve": len(ea) == len(eb),
        "num_executed": a["num_executed"] == b["num_executed"],
        "num_skipped": a["num_skipped"] == b["num_skipped"],
        "capital_after": len(ea) == len(eb) and ea["capital_after"].reset_index(drop=True).equals(
            eb["capital_after"].reset_index(drop=True)),
        "allocation": len(ea) == len(eb) and ea["allocation"].reset_index(drop=True).equals(
            eb["allocation"].reset_index(drop=True)),
    }


r1 = lauf(trades)
markiert = trades.copy()
markiert["symbol"] = [f"{s}{ph.TRENNER}{i}" for i, s in zip(markiert.index, markiert["symbol"])]
r2 = lauf(markiert)
print(f"== {bot}: unveraendert gegen markiert (Erzeuger, heutiger Code)")
for k, v in vergleich(r1, r2).items():
    print(f"   {k:22s} {'gleich' if v else 'VERSCHIEDEN'}")

# Gegenprobe: derselbe markierte Lauf, aber der Zufallsschluessel der Stufe 4
# rechnet mit dem UNMARKIERTEN Symbol (Zeilenkennung vor dem Fingerabdruck
# abgeschnitten). Nur im Speicher, nur fuer diese Messung.
original = zuteilung.zufallsschluessel


def ohne_kennung(seed, werte):
    werte = list(werte)
    if werte and isinstance(werte[0], str) and ph.TRENNER in werte[0]:
        werte[0] = werte[0].rsplit(ph.TRENNER, 1)[0]
    return original(seed, werte)


zuteilung.zufallsschluessel = ohne_kennung
r3 = lauf(markiert)
zuteilung.zufallsschluessel = original
print(f"== {bot}: unveraendert gegen markiert, Stufe-4-Schluessel ohne Zeilenkennung (Gegenprobe)")
for k, v in vergleich(r1, r3).items():
    print(f"   {k:22s} {'gleich' if v else 'VERSCHIEDEN'}")
