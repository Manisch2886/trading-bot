"""
Dritte Kurvenvariante: volatility_breakout_crypto MIT BTC-Regimefilter
====================================================================================
Der zweite Nachtrag (PR #55) hat eine Einschraenkung offengelassen und selbst
benannt: bei `volatility_breakout_crypto` fallen "heutiger Backtest-Stand" und
"Live-Konfiguration" auseinander. `live_params.py` setzt
`BTC_REGIME_FILTER_ENABLED = True`, `equity_simulation.py` wendet den Filter
aber bewusst nicht an (dokumentiert im Kopf jener Datei, PR #45). Die v2-Kurve
dieses Bots ist deshalb die einzige der neun, die NICHT live-konform ist.

Das ist keine Kleinigkeit, weil der HRP-Vorteil in der zweiten Korrektur nur
+0,14 Calmar-Punkte betraegt. Dieses Modul erzeugt die eine fehlende Variante:
dieselbe Rechnung wie im heutigen `__main__`-Block, nur mit dem Regimefilter
zwischen Trade-Erzeugung und Portfolio-Simulation.

--------------------------------------------------------------------
Warum hier nachgebildet statt ausgefuehrt wird
--------------------------------------------------------------------
`generate_heute()` fuehrt den `__main__`-Block per runpy aus - genau deshalb
ist es dort nicht moeglich, zwischen `collect_all_trades()` und
`simulate_portfolio()` einzugreifen: beide Namen werden im ausgefuehrten
Skript selbst gebunden, ein Monkey-Patch von aussen erreicht sie nicht.

Diese Variante bildet die vier Zeilen des `__main__`-Blocks deshalb nach. Das
ist derselbe Weg, den `corrected_curves._WORKER` (erste Korrektur) fuer diesen
Bot schon gegangen ist - inklusive `compute_btc_regime` /
`filter_trades_by_regime` aus dem unveraenderten `regime_filter.py` des Bots,
also den Funktionen, die auch `forward_test.py` live benutzt. Neu erfunden
wird hier nichts.

Eine Nachbildung ist aber immer eine zweite Fassung derselben Rechnung und
kann still abweichen. Deshalb laeuft sie IMMER zweimal:

  1. OHNE Filter - das Ergebnis muss die v2-Kurve aus `corrected_curves_v2/`
     BYTEWEISE treffen. Tut es das nicht, ist die Nachbildung falsch und der
     ganze Vergleich wertlos; das Modul bricht dann ab.
  2. MIT Filter - die gesuchte dritte Variante.

Ohne Schritt 1 waere ein Unterschied zwischen v2 und dieser Variante nicht
dem Filter zuzurechnen, sondern koennte ebenso gut aus der Nachbildung
stammen.

Rein lesend gegenueber dem Bot: kein Bot-Code wird veraendert, der
Regimefilter wird NICHT in `equity_simulation.py` eingebaut.

Nutzung:  python3 vbc_regimefilter.py     (nur die Kurve + Leerprobe)
"""

import json
import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, _DIR)

import corrected_curves as cc   # noqa: E402

BOT = "volatility_breakout_crypto"
CURVE_DIR_V2 = os.path.join(_DIR, "corrected_curves_v2")
CURVE_DIR_V3 = os.path.join(_DIR, "corrected_curves_v2_regimefilter")

# Die Attrappen werden aus dem bestehenden Laeufer UEBERNOMMEN, nicht kopiert.
# corrected_curves.py bleibt dafuer voellig unveraendert (es liegt dort und in
# research/trend_overlay/ als byteweise identische Kopie; eine Aenderung
# muesste beide treffen und faellt damit aus dem Auftragsumfang).
#
# Der Vorspann von _WORKER_HEUTE endet genau vor dessen argv-Zeile. Steht die
# Marke eines Tages nicht mehr da, schlaegt das assert sofort zu - besser als
# eine dritte Kopie der Attrappen, die still von den anderen abweicht.
_MARKE = "BOT, OUT_JSON, RESULTS = sys.argv[1], sys.argv[2], sys.argv[3]"
assert _MARKE in cc._WORKER_HEUTE, (
    "corrected_curves._WORKER_HEUTE hat seine argv-Zeile geaendert - der "
    "Attrappen-Vorspann laesst sich nicht mehr sicher abtrennen.")
ATTRAPPEN_VORSPANN = cc._WORKER_HEUTE.split(_MARKE)[0]

# Der Laeufer bildet die vier wirksamen Zeilen des __main__-Blocks nach.
# MIT_FILTER schiebt genau einen Schritt dazwischen - sonst ist alles gleich.
_WORKER = ATTRAPPEN_VORSPANN + r'''
OUT_CSV, OUT_JSON, MIT_FILTER = sys.argv[1], sys.argv[2], sys.argv[3] == "1"

import equity_simulation as es

# --- die vier Zeilen aus dem __main__-Block von equity_simulation.py -------
all_data = es.load_all_symbol_data()
trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT)
if trades.empty:
    raise SystemExit("keine Trades - der Lauf belegt nichts")

gefiltert_weg = 0
if MIT_FILTER:
    # Die unveraenderten Funktionen des Bots - dieselben, die forward_test.py
    # live benutzt. compute_btc_regime() wird ohne Argumente aufgerufen, damit
    # die Literale aus regime_filter.py wirken (atr_length=22, atr_mult=3.0) -
    # genau wie live.
    from regime_filter import compute_btc_regime, filter_trades_by_regime
    btc = all_data.get("BTCUSDT")
    if btc is None:
        raise SystemExit("BTCUSDT fehlt - der Regimefilter ist nicht anwendbar")
    vorher = len(trades)
    trades = filter_trades_by_regime(trades, compute_btc_regime(btc))
    gefiltert_weg = vorher - len(trades)

result = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT,
                                es.MAX_CONCURRENT_POSITIONS)
# --------------------------------------------------------------------------

result["equity_curve"].to_csv(OUT_CSV, index=False)
zusammenfassung = {
    "bot": "volatility_breakout_crypto",
    "mit_regimefilter": MIT_FILTER,
    "trades_found": int(len(trades)),
    "vom_filter_entfernt": gefiltert_weg,
    "executed": result["num_executed"],
    "skipped": result["num_skipped"],
    "return_pct": round((result["final_capital"] / es.STARTING_CAPITAL - 1) * 100, 2),
    "drawdown_pct": es.calculate_max_drawdown(result["equity_curve"], es.STARTING_CAPITAL),
    "allocation_pct": round(es.ALLOCATION_PCT * 100, 2),
    "max_concurrent_positions": es.MAX_CONCURRENT_POSITIONS,
}
with open(OUT_JSON, "w") as fh:
    json.dump(zusammenfassung, fh, indent=2)
'''


def _lauf(out_csv: str, out_json: str, mit_filter: bool) -> dict:
    strategy_dir = os.path.join(_REPO_ROOT, "strategies", BOT)
    proc = subprocess.run(
        [sys.executable, "-c", _WORKER, out_csv, out_json, "1" if mit_filter else "0"],
        cwd=strategy_dir, capture_output=True, text=True,
        env={**os.environ, "PYTHONPATH": os.path.join(_REPO_ROOT, "shared")})
    if proc.returncode != 0:
        raise SystemExit(f"Lauf (Filter={mit_filter}) fehlgeschlagen:\n{proc.stderr[-3000:]}")
    with open(out_json) as handle:
        return json.load(handle)


def erzeuge(verbose: bool = True) -> dict:
    """Erzeugt die gefilterte Kurve - und beweist vorher, dass die
    Nachbildung stimmt."""
    os.makedirs(CURVE_DIR_V3, exist_ok=True)
    v2_csv = os.path.join(CURVE_DIR_V2, f"{BOT}_equity_curve.csv")
    if not os.path.exists(v2_csv):
        raise SystemExit(f"{v2_csv} fehlt - erst nachtrag_sync_korrektur_v2.py laufen lassen.")

    probe_csv = os.path.join(CURVE_DIR_V3, "_leerprobe_ohne_filter.csv")
    probe_json = os.path.join(CURVE_DIR_V3, "_leerprobe_ohne_filter.json")
    ohne = _lauf(probe_csv, probe_json, mit_filter=False)

    gleich = cc._sha256(probe_csv) == cc._sha256(v2_csv)
    if verbose:
        print("  Leerprobe (Nachbildung OHNE Filter) gegen corrected_curves_v2/:")
        print(f"    {ohne['executed']:>5} ausgefuehrt  {ohne['return_pct']:>8.2f}%  "
              f"DD {ohne['drawdown_pct']:>7.2f}%   -> "
              + ("BYTEWEISE IDENTISCH" if gleich else "ABWEICHUNG"))
    if not gleich:
        raise SystemExit(
            "Die Nachbildung trifft die v2-Kurve nicht. Ein Vergleich mit der\n"
            "gefilterten Variante waere dann nicht dem Filter zuzurechnen.\n"
            f"  Nachbildung: {probe_csv}\n  v2-Kurve:    {v2_csv}")
    os.remove(probe_csv)
    os.remove(probe_json)

    ziel_csv = os.path.join(CURVE_DIR_V3, f"{BOT}_equity_curve.csv")
    ziel_json = os.path.join(CURVE_DIR_V3, f"{BOT}_summary.json")
    mit = _lauf(ziel_csv, ziel_json, mit_filter=True)
    if verbose:
        print("  Variante MIT BTC-Regimefilter:")
        print(f"    {mit['executed']:>5} ausgefuehrt  {mit['return_pct']:>8.2f}%  "
              f"DD {mit['drawdown_pct']:>7.2f}%   "
              f"({mit['vom_filter_entfernt']} Trades vom Filter entfernt)")
    return {"ohne_filter": ohne, "mit_filter": mit, "csv": ziel_csv,
             "leerprobe_identisch": gleich}


def gemischte_grundlage() -> dict:
    """Acht Kurven unveraendert aus corrected_curves_v2/, die neunte gefiltert.
    Rueckgabe im `generated`-Format von corrected_curves.load_corrected_curves."""
    basis = cc.vorhandene_kurven(CURVE_DIR_V2)
    basis[BOT] = {"csv": os.path.join(CURVE_DIR_V3, f"{BOT}_equity_curve.csv")}
    return basis


if __name__ == "__main__":
    print("Dritte Kurvenvariante: volatility_breakout_crypto mit BTC-Regimefilter\n")
    erzeuge()
    print(f"\nGeschrieben nach: {CURVE_DIR_V3}")
