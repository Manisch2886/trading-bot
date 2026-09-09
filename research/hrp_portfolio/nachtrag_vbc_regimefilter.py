"""
Nachprüfung: hält der HRP-Vorteil mit live-konformem volatility_breakout_crypto?
====================================================================================
Der zweite Nachtrag (PR #55) hat die HRP-Kernaussage kippen sehen: HRP liegt
dort erstmals vor der Gleichgewichtung (+0,1424 Calmar). Er hat aber selbst
eine Einschraenkung benannt: die v2-Kurve von `volatility_breakout_crypto` ist
die einzige der neun, die NICHT live-konform ist - der BTC-Regimefilter ist
live aktiv, im Backtest aber bewusst nicht eingebaut (PR #45).

Der HRP-Vorsprung betraegt nur gut 2 %. Dieser Nachtrag beantwortet deshalb
die eine offene Frage: **haelt der Vorsprung, wenn genau dieser Bot mit
korrekt angewendetem Filter einfliesst?**

Untersucht wird NUR dieser eine Faktor. Acht Kurven werden unveraendert aus
`corrected_curves_v2/` uebernommen, die neunte kommt aus
`corrected_curves_v2_regimefilter/` (siehe `vbc_regimefilter.py`, inklusive
der dort erzwungenen Leerprobe). Keine erneute Bestandsaufnahme, keine
weiteren Varianten.

**Nur die eine Kurve aendert sich.** Rebalancing-Intervall, Linkage-Verfahren,
Schwellen, Bootstrap-Fallback, Buy-and-Hold-Referenz und die gesamte
Auswertung kommen unveraendert aus `run_walk_forward.py` - aufgerufen ueber
`nachtrag_sync_korrektur.analyse()`, also woertlich dieselbe Funktion wie in
beiden vorangegangenen Nachtraegen.

DREI Regressionsanker, einer mehr als in PR #55:

  original        trifft results/hrp_summary.json                (Erstfassung)
  korrigiert_v1   trifft results/nachtrag_sync_korrektur.json    (1. Korrektur)
  korrigiert_v2   trifft results/nachtrag_sync_korrektur_v2.json (2. Korrektur)

Der dritte ist hier der wichtigste: er belegt, dass die acht unveraendert
uebernommenen Kurven wirklich dieselbe Rechnung ergeben wie in PR #55 - und
damit, dass ein Unterschied zur neuen Grundlage ausschliesslich von der einen
getauschten Kurve kommt.

Reine Backtest-Untersuchung. Kein Bot-Code, keine Live-Datei, weder
`corrected_curves/` noch `corrected_curves_v2/` werden veraendert.

Nutzung:  python3 nachtrag_vbc_regimefilter.py
"""

import json
import os
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, _DIR)
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))

import corrected_curves as cc                      # noqa: E402
import portfolio_overview as po                    # noqa: E402
import run_walk_forward as rwf                     # noqa: E402
import nachtrag_sync_korrektur as v1               # noqa: E402
import vbc_regimefilter as vbc                     # noqa: E402

RESULTS_DIR = rwf.RESULTS_DIR
REFERENZ_ERSTFASSUNG = os.path.join(RESULTS_DIR, "hrp_summary.json")
REFERENZ_V1 = os.path.join(RESULTS_DIR, "nachtrag_sync_korrektur.json")
REFERENZ_V2 = os.path.join(RESULTS_DIR, "nachtrag_sync_korrektur_v2.json")
TOL = 0.011

BASES = ("original", "korrigiert_v1", "korrigiert_v2", "v2_mit_regimefilter")

BESTANDEN = 0
ABWEICHUNGEN = []


def check(label, ist, soll, tol=TOL):
    global BESTANDEN
    ok = ist is not None and soll is not None and abs(ist - soll) <= tol
    if ok:
        BESTANDEN += 1
        print(f"  OK     {label:<58} {ist:>12.4f}")
    else:
        ABWEICHUNGEN.append(label)
        print(f"  FEHLER {label:<58} {ist!s:>12}  erwartet {soll}")


def analysiere(generated, swap_bots, basis_name):
    """Woertlich v1.analyse(), nur mit freier Wahl der zu tauschenden Bots."""
    v1.SWAP_FOR[basis_name] = tuple(swap_bots)
    try:
        return v1.analyse(basis_name, generated)
    finally:
        v1.SWAP_FOR.pop(basis_name, None)


def vergleich_block(name, ergebnis):
    h = ergebnis["hrp_walk_forward"]
    b = ergebnis["baseline_equal_weight"]
    w = ergebnis["robustness_check_ward_linkage"]
    return {
        "hrp": h, "baseline": b, "ward": w,
        "hrp_minus_baseline_calmar": round(h["calmar_ratio"] - b["calmar_ratio"], 4),
        "ward_minus_baseline_calmar": round(w["calmar_ratio"] - b["calmar_ratio"], 4),
    }


def main():
    print("=" * 96)
    print("1) Die eine getauschte Kurve erzeugen (inkl. erzwungener Leerprobe)")
    print("=" * 96)
    kurve = vbc.erzeuge()

    print("\n" + "=" * 96)
    print("2) Regressionsanker - alle drei frueheren Fassungen reproduzieren")
    print("=" * 96)
    v1_kurven = cc.vorhandene_kurven(vbc.CURVE_DIR_V2.replace("corrected_curves_v2",
                                                               "corrected_curves"))
    v2_kurven = cc.vorhandene_kurven(vbc.CURVE_DIR_V2)

    ergebnisse = {
        "original": analysiere(v2_kurven, (), "o"),
        "korrigiert_v1": analysiere(v1_kurven, cc.SWAP_PRIMARY, "k1"),
        "korrigiert_v2": analysiere(v2_kurven, cc.ALL_BOTS, "k2"),
    }

    with open(REFERENZ_ERSTFASSUNG) as handle:
        ref0 = json.load(handle)
    with open(REFERENZ_V1) as handle:
        ref1 = json.load(handle)["ergebnisse"]["korrigiert"]
    with open(REFERENZ_V2) as handle:
        ref2 = json.load(handle)["ergebnisse"]["korrigiert_v2"]

    for name, referenz in (("original", ref0), ("korrigiert_v1", ref1),
                            ("korrigiert_v2", ref2)):
        for block in ("hrp_walk_forward", "baseline_equal_weight",
                       "robustness_check_ward_linkage"):
            for key in ("total_return_pct", "max_drawdown_pct", "calmar_ratio"):
                check(f"{name} / {block} / {key}",
                      ergebnisse[name][block][key], referenz[block][key])

    if ABWEICHUNGEN:
        print(f"\n{len(ABWEICHUNGEN)} Abweichungen - der Vergleich waere nicht "
              f"belastbar. Abbruch.")
        for label in ABWEICHUNGEN:
            print(f"  FEHLGESCHLAGEN: {label}")
        sys.exit(1)

    print("\n" + "=" * 96)
    print("3) Neue Grundlage: 8 Kurven aus corrected_curves_v2/ + 1 gefilterte")
    print("=" * 96)
    gemischt = vbc.gemischte_grundlage()
    ergebnisse["v2_mit_regimefilter"] = analysiere(gemischt, cc.ALL_BOTS, "v3")
    print("  gerechnet.")

    print("\n" + "=" * 96)
    print("4) Gegenueberstellung (Rendite % / Max Drawdown % / Calmar)")
    print("=" * 96)
    print(f"  {'Grundlage':<24}{'Fenster':<26}{'HRP':>28}{'Gleichgewichtung':>28}")
    for name in BASES:
        r = ergebnisse[name]
        h, b = r["hrp_walk_forward"], r["baseline_equal_weight"]
        fenster = f"{r['common_window']['start']}..{r['common_window']['end']}"
        print(f"  {name:<24}{fenster:<26}"
              f"{h['total_return_pct']:>10.2f}/{h['max_drawdown_pct']:>8.2f}/{str(h['calmar_ratio']):>8}"
              f"{b['total_return_pct']:>10.2f}/{b['max_drawdown_pct']:>8.2f}/{str(b['calmar_ratio']):>8}")

    print("\n" + "=" * 96)
    print("5) Die Antwort: haelt der HRP-Vorteil?")
    print("=" * 96)
    print(f"  {'Grundlage':<24}{'HRP - Gleichgew.':>20}{'Ward - Gleichgew.':>21}"
          f"{'HRP besser?':>16}")
    for name in BASES:
        v = vergleich_block(name, ergebnisse[name])
        ergebnisse[name]["vergleich"] = {
            "hrp_minus_baseline_calmar": v["hrp_minus_baseline_calmar"],
            "ward_minus_baseline_calmar": v["ward_minus_baseline_calmar"],
            "hrp_besser": bool(v["hrp_minus_baseline_calmar"] > 0),
        }
        print(f"  {name:<24}{v['hrp_minus_baseline_calmar']:>+20.4f}"
              f"{v['ward_minus_baseline_calmar']:>+21.4f}"
              f"{('ja' if v['hrp_minus_baseline_calmar'] > 0 else 'nein'):>16}")

    v2 = ergebnisse["korrigiert_v2"]["vergleich"]
    v3 = ergebnisse["v2_mit_regimefilter"]["vergleich"]
    print()
    print(f"  2. Korrektur (v2):            HRP {v2['hrp_minus_baseline_calmar']:+.4f}  "
          f"Ward {v2['ward_minus_baseline_calmar']:+.4f}")
    print(f"  dieselbe, VBC live-konform:   HRP {v3['hrp_minus_baseline_calmar']:+.4f}  "
          f"Ward {v3['ward_minus_baseline_calmar']:+.4f}")
    print(f"  Veraenderung durch den Filter: "
          f"{v3['hrp_minus_baseline_calmar'] - v2['hrp_minus_baseline_calmar']:+.4f}")
    print()
    if v3["hrp_besser"] and v2["hrp_besser"]:
        antwort = ("Der HRP-Vorteil HAELT - auch mit live-konformem "
                   "volatility_breakout_crypto liegt HRP vorn.")
    elif not v3["hrp_besser"] and v2["hrp_besser"]:
        antwort = ("Der HRP-Vorteil KIPPT ZURUECK - mit live-konformem "
                   "volatility_breakout_crypto liegt HRP wieder hinten.")
    else:
        antwort = "Unerwartete Konstellation - siehe Zahlen oben."
    print(f"  ANTWORT: {antwort}")

    ziel = os.path.join(RESULTS_DIR, "nachtrag_vbc_regimefilter.json")
    with open(ziel, "w") as handle:
        json.dump({
            "hinweis": ("Prueft NUR den in PR #55 benannten Unsicherheitsfaktor: "
                        "volatility_breakout_crypto mit korrekt angewendetem "
                        "BTC-Regimefilter. Acht Kurven unveraendert aus "
                        "corrected_curves_v2/, Methodik unveraendert aus "
                        "run_walk_forward.py."),
            "getauschte_kurve": {
                "bot": vbc.BOT,
                "ohne_filter": kurve["ohne_filter"],
                "mit_filter": kurve["mit_filter"],
                "leerprobe_byteweise_identisch_mit_v2": kurve["leerprobe_identisch"],
            },
            "regressionsanker_bestanden": BESTANDEN,
            "antwort": antwort,
            "ergebnisse": ergebnisse,
        }, handle, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {ziel}")
    print(f"{BESTANDEN} Referenzwerte bestaetigt, {len(ABWEICHUNGEN)} abweichend.")
    sys.exit(0)


if __name__ == "__main__":
    main()
