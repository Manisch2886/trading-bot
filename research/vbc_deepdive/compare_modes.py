"""
Gegenueberstellung der drei Regimefilter-Modi
====================================================================
Liest die Ergebnis-JSONs der drei Laeufe von `run_deepdive.py` und
beantwortet die zentrale Frage der Nachtrags-Aufgabe:

  Bleibt die Wirkung des ATR-Trailing-Stops bestehen, wenn der
  BTC-Regimefilter - wie live - aktiv ist, oder vermeidet der Filter
  bereits einen Grossteil derselben Verlustphasen?

Kernstueck ist die ZERLEGUNG der Drawdown-Reduktion. Beide Mechanismen
sind Schutzmassnahmen gegen dieselbe Sorte Ereignis. Ob sie sich addieren
oder ueberlappen, laesst sich direkt ausrechnen, weil alle vier Zellen
vorliegen:

           |      ohne Filter      |       mit Filter
  ---------|-----------------------|------------------------
  Baseline |  DD(A)                |  DD(A|F)
  Trailing |  DD(C)                |  DD(C|F)

  Beitrag Filter allein   = DD(A)   - DD(A|F)
  Beitrag Trailing allein = DD(A)   - DD(C)
  Beitrag beider          = DD(A)   - DD(C|F)
  Ueberlappung            = (Filter allein + Trailing allein) - beide

Eine Ueberlappung nahe 0 heisst: die Mechanismen schuetzen vor
unterschiedlichen Ereignissen. Eine Ueberlappung in der Groessenordnung
des kleineren Einzelbeitrags heisst: sie schuetzen vor demselben, und man
bezahlt zweimal fuer denselben Schutz.

Reine Auswertung bereits gerechneter Ergebnisse - kein neuer Backtest.

Nutzung:  python3 compare_modes.py
"""

import json
import os
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(_DIR, "results")

MODES = {
    "off": "vbc_deepdive.json",
    "posthoc": "vbc_deepdive_posthoc.json",
    "sequential": "vbc_deepdive_sequential.json",
}
MODE_LABEL = {"off": "ohne Filter", "posthoc": "Filter (posthoc)",
              "sequential": "Filter (sequential)"}
PERIODS = ("full", "in_sample", "out_of_sample")
VARIANTS = ("baseline", "vol_sizing", "trailing", "combined")


def load():
    data = {}
    for mode, name in MODES.items():
        path = os.path.join(RESULTS_DIR, name)
        if not os.path.exists(path):
            raise SystemExit(
                f"{name} fehlt - bitte zuerst laufen lassen:\n"
                f"  python3 run_deepdive.py" + ("" if mode == "off" else f" --regime {mode}"))
        with open(path) as handle:
            data[mode] = json.load(handle)
    return data


def drawdown_decomposition(data) -> dict:
    """Zerlegung der Drawdown-Reduktion (siehe Modul-Kopf).

    Alle Werte in Prozentpunkten, positiv = Drawdown verringert. Gerechnet
    wird gegen die ungefilterte Baseline als gemeinsamen Nullpunkt.
    """
    out = {}
    for mode in ("posthoc", "sequential"):
        out[mode] = {}
        for period in PERIODS:
            dd_a = data["off"]["periods"][period]["baseline"]["max_drawdown_pct"]
            dd_c = data["off"]["periods"][period]["trailing"]["max_drawdown_pct"]
            dd_af = data[mode]["periods"][period]["baseline"]["max_drawdown_pct"]
            dd_cf = data[mode]["periods"][period]["trailing"]["max_drawdown_pct"]
            filter_only = abs(dd_a) - abs(dd_af)
            trailing_only = abs(dd_a) - abs(dd_c)
            both = abs(dd_a) - abs(dd_cf)
            overlap = filter_only + trailing_only - both
            smaller = min(filter_only, trailing_only)
            out[mode][period] = {
                "dd_baseline_unfiltered_pct": dd_a,
                "dd_baseline_filtered_pct": dd_af,
                "dd_trailing_unfiltered_pct": dd_c,
                "dd_trailing_filtered_pct": dd_cf,
                "filter_only_pp": round(filter_only, 2),
                "trailing_only_pp": round(trailing_only, 2),
                "both_pp": round(both, 2),
                "overlap_pp": round(overlap, 2),
                # Anteil der Ueberlappung am KLEINEREN der beiden Einzelbeitraege:
                # 0 % = unabhaengig, 100 % = der schwaechere Mechanismus liefert
                # neben dem staerkeren gar nichts Eigenes mehr. UEBER 100 % ist
                # kein Rechenfehler, sondern Gegenlaeufigkeit: beide zusammen
                # schuetzen dann sogar schlechter als der staerkere allein. Das
                # tritt im sequential-Modus auf, weil dort blockierte Einstiege
                # das Symbol freigeben und spaetere Ersatz-Trades entstehen, die
                # es ohne Filter nie gegeben haette.
                "overlap_share_of_weaker_pct": (round(overlap / smaller * 100, 1)
                                                if smaller > 1e-9 else None),
            }
    return out


def main():
    data = load()

    print("=" * 96)
    print("PUNKTSCHAETZER - Rendite % / Max Drawdown % / Calmar")
    print("=" * 96)
    for period in PERIODS:
        print(f"\n{period}")
        print(f"  {'Modus':<20}" + "".join(f"{v:>19}" for v in VARIANTS))
        for mode in MODES:
            cells = ""
            for v in VARIANTS:
                r = data[mode]["periods"][period][v]
                cells += f"{r['total_return_pct']:>7.2f}/{r['max_drawdown_pct']:>6.2f}/{str(r['calmar_ratio']):>4}"
            print(f"  {MODE_LABEL[mode]:<20}{cells}")

    print("\n" + "=" * 96)
    print("BELASTBARKEIT - P(Effekt > 0) in %, Block-Bootstrap, gepaart")
    print("=" * 96)
    for metric, title in (("calmar_ratio", "Calmar-Ratio"),
                           ("max_drawdown_pct", "Max Drawdown (positiv = Drawdown gesenkt)")):
        print(f"\n{title}")
        print(f"  {'Kontrast':<28}{'Periode':<16}" + "".join(f"{MODE_LABEL[m]:>21}" for m in MODES))
        for contrast in ("trailing_minus_baseline", "vol_sizing_minus_baseline",
                          "combined_minus_baseline", "combined_minus_trailing"):
            for period in PERIODS:
                cells = "".join(
                    f"{data[m]['bootstrap'][period]['differences'][contrast][metric]['share_above_zero_pct']:>21.1f}"
                    for m in MODES)
                print(f"  {contrast:<28}{period:<16}{cells}")

    decomposition = drawdown_decomposition(data)
    print("\n" + "=" * 96)
    print("ZERLEGUNG DER DRAWDOWN-REDUKTION (Prozentpunkte, positiv = Drawdown gesenkt)")
    print("=" * 96)
    for mode in ("posthoc", "sequential"):
        print(f"\n{MODE_LABEL[mode]}")
        print(f"  {'Periode':<16}{'Filter allein':>15}{'Trailing allein':>17}"
              f"{'beide':>10}{'Ueberlappung':>14}{'Anteil am Schwaecheren':>24}")
        for period in PERIODS:
            d = decomposition[mode][period]
            share = "-" if d["overlap_share_of_weaker_pct"] is None else f"{d['overlap_share_of_weaker_pct']:.1f} %"
            print(f"  {period:<16}{d['filter_only_pp']:>15.2f}{d['trailing_only_pp']:>17.2f}"
                  f"{d['both_pp']:>10.2f}{d['overlap_pp']:>14.2f}{share:>24}")

    print("\n" + "=" * 96)
    print("REIHENFOLGE-EMPFINDLICHKEIT - Lage des berichteten Calmar-Werts (Gesamtzeitraum)")
    print("=" * 96)
    print(f"  {'Modus':<20}{'Variante':<12}{'berichtet':>11}{'min':>8}{'Median':>9}{'max':>8}{'Perzentil':>11}")
    for mode in MODES:
        for v in VARIANTS:
            c = data[mode]["tie_order_sensitivity"]["full"][v]["calmar_ratio"]
            print(f"  {MODE_LABEL[mode]:<20}{v:<12}{c['reported']:>11}{c['min']:>8}"
                  f"{c['median']:>9}{c['max']:>8}{c['reported_percentile']:>10}.")

    out_path = os.path.join(RESULTS_DIR, "mode_comparison.json")
    with open(out_path, "w") as handle:
        json.dump({
            "modes": {m: {"regime_filter": data[m]["regime_filter"],
                          "periods": data[m]["periods"],
                          "trade_counts": data[m]["trade_counts"]} for m in MODES},
            "drawdown_decomposition": decomposition,
        }, handle, indent=2, default=str)
    print(f"\nGespeichert: {out_path}")


if __name__ == "__main__":
    main()
