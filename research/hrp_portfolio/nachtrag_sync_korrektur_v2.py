"""
Zweiter Nachtrag: HRP-Untersuchung auf dem HEUTIGEN Stand der Bots
====================================================================================
Der erste Nachtrag (`nachtrag_sync_korrektur.py`) hat die Kapitalkurven einmal
korrigiert: er bildete von Hand nach, wie die fuenf damals abweichenden Bots
MIT Live-Konfiguration gerechnet haetten.

Seither sind die Sync-Befunde selbst gemergt worden - die Nachbildung ist
damit ueberholt, und die Kurven sind ein ZWEITES Mal veraltet:

  PR #40-42  Allokation und Positionslimit direkt in equity_simulation.py
             nachgezogen (rsi2_mean_reversion, turtle_soup_stocks,
             volatility_breakout)
  PR #45     Funktions-Defaults synchronisiert (MAX_HOLD_DAYS, Squeeze-
             Parameter) bei fuenf Bots
  PR #51/#52 Backtest-Defaults von t3_supertrend und rsi2_crypto kommen
             jetzt aus live_params.py
  ausserdem  korrigierter ZigZag-Indikator bei beiden Elliott-Bots

Dieser zweite Nachtrag rechnet dieselbe Untersuchung auf Kurven, die die
HEUTIGE equity_simulation.py erzeugt - erzeugt durch AUSFUEHREN eben dieser
Datei (corrected_curves.generate_heute), nicht durch eine weitere Nachbildung.

**Nur die Kurven aendern sich.** Rebalancing-Intervall, Linkage-Verfahren,
Mindest-Datenbasis-Schwelle, Bootstrap-Fallback, Buy-and-Hold-Referenz und die
gesamte Auswertung werden unveraendert aus `run_walk_forward.py` importiert -
ueber `nachtrag_sync_korrektur.analyse()`, also woertlich dieselbe Funktion,
die schon die erste Korrektur benutzt hat. Es gibt hier keine zweite Umsetzung
derselben Rechnung.

Vier Grundlagen:

  original          die Kurven der Erstfassung
                    REGRESSIONSCHECK gegen results/hrp_summary.json
  korrigiert_v1     die erste Korrektur, aus den GESPEICHERTEN Kurven in
                    corrected_curves/ - nicht neu gerechnet
                    REGRESSIONSCHECK gegen results/nachtrag_sync_korrektur.json
  korrigiert_v1_stale  dieselbe, zusaetzlich mit elliott_wave (KNOWN_STALE_BOTS)
  korrigiert_v2     alle neun Bots mit dem heutigen Code (PRIMAER)

Zwei Regressionsanker statt einem: der erste zeigt, dass die Auswertung
unveraendert rechnet, der zweite, dass die alte Grundlage exakt reproduziert
wird. Ohne den zweiten waere ein Dreifach-Vergleich wertlos - man wuesste
nicht, ob eine Verschiebung von den neuen Kurven kommt oder davon, dass die
alte Spalte anders gerechnet wurde als damals.

Reine Backtest-Untersuchung. `shared/portfolio_overview.py`,
`results/*/equity_curve.csv`, `corrected_curves/` und jeder Bot-Code bleiben
unveraendert.

Nutzung:  python3 nachtrag_sync_korrektur_v2.py
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

CURVE_DIR_V1 = os.path.join(_DIR, "corrected_curves")
CURVE_DIR_V2 = os.path.join(_DIR, "corrected_curves_v2")
RESULTS_DIR = rwf.RESULTS_DIR
REFERENZ_ERSTFASSUNG = os.path.join(RESULTS_DIR, "hrp_summary.json")
REFERENZ_V1 = os.path.join(RESULTS_DIR, "nachtrag_sync_korrektur.json")
TOL = 0.011

BASES = ("original", "korrigiert_v1", "korrigiert_v1_stale", "korrigiert_v2")

BESTANDEN = 0
ABWEICHUNGEN = []


def check(label, ist, soll, tol=TOL):
    global BESTANDEN
    if ist is None or soll is None:
        ok = ist == soll
        gezeigt = str(ist)
    else:
        ok = abs(ist - soll) <= tol
        gezeigt = f"{ist:.4f}"
    if ok:
        BESTANDEN += 1
        print(f"  OK     {label:<54} {gezeigt:>12}")
    else:
        ABWEICHUNGEN.append(label)
        print(f"  FEHLER {label:<54} {gezeigt:>12}  erwartet {soll}")


def analysiere(generated, swap_bots, basis_name):
    """Die Auswertung der Erstfassung - woertlich v1.analyse(), nur mit
    freier Wahl der zu tauschenden Bots. v1.analyse() liest seine Tauschliste
    aus v1.SWAP_FOR; die wird dafuer kurzzeitig ergaenzt statt die Funktion
    zu kopieren."""
    v1.SWAP_FOR[basis_name] = tuple(swap_bots)
    try:
        return v1.analyse(basis_name, generated)
    finally:
        v1.SWAP_FOR.pop(basis_name, None)


def main():
    print("=" * 96)
    print("1) Kapitalkurven mit dem HEUTIGEN Bot-Code erzeugen")
    print("=" * 96)
    heute = cc.generate_heute(_REPO_ROOT, CURVE_DIR_V2, po)

    print("\n" + "=" * 96)
    print("2) Bestandsaufnahme: welche Kurve hat sich gegenueber der ersten Korrektur bewegt?")
    print("=" * 96)
    v1_kurven = cc.vorhandene_kurven(CURVE_DIR_V1)
    bestandsaufnahme = {}
    print(f"  {'Bot':<28}{'ggue. results/':<18}{'ggue. 1. Korrektur':<22}"
          f"{'ausgefuehrt':>12}{'Rendite %':>12}")
    for bot in cc.ALL_BOTS:
        neu_csv = heute[bot]["csv"]
        wie_results = "identisch" if heute[bot]["identical_to_original"] else "ANDERS"
        alt = v1_kurven.get(bot)
        wie_v1 = ("keine v1-Kurve" if alt is None
                  else ("identisch" if cc._sha256(alt["csv"]) == cc._sha256(neu_csv)
                        else "ANDERS"))
        s = heute[bot]["summary"]
        bestandsaufnahme[bot] = {
            "gegenueber_results": wie_results,
            "gegenueber_erster_korrektur": wie_v1,
            **s,
        }
        print(f"  {bot:<28}{wie_results:<18}{wie_v1:<22}"
              f"{s['executed']:>12}{s['return_pct']:>12.2f}")

    print("\n" + "=" * 96)
    print("3) Regressionscheck A - Basis 'original' gegen results/hrp_summary.json")
    print("=" * 96)
    with open(REFERENZ_ERSTFASSUNG) as handle:
        referenz = json.load(handle)
    ergebnisse = {"original": analysiere(heute, (), "original_v2")}
    basis = ergebnisse["original"]
    for block in ("hrp_walk_forward", "baseline_equal_weight", "buy_and_hold",
                   "robustness_check_ward_linkage"):
        for key in ("total_return_pct", "max_drawdown_pct", "calmar_ratio"):
            check(f"{block} / {key}", basis[block][key], referenz[block][key])

    print("\n" + "=" * 96)
    print("4) Regressionscheck B - die erste Korrektur exakt reproduzieren")
    print("=" * 96)
    with open(REFERENZ_V1) as handle:
        referenz_v1 = json.load(handle)["ergebnisse"]
    ergebnisse["korrigiert_v1"] = analysiere(v1_kurven, cc.SWAP_PRIMARY, "k_v1")
    ergebnisse["korrigiert_v1_stale"] = analysiere(v1_kurven, cc.SWAP_WITH_STALE, "k_v1s")
    for name, ref_name in (("korrigiert_v1", "korrigiert"),
                            ("korrigiert_v1_stale", "korrigiert_plus_veraltet")):
        for block in ("hrp_walk_forward", "baseline_equal_weight"):
            for key in ("total_return_pct", "max_drawdown_pct", "calmar_ratio"):
                check(f"{name} / {block} / {key}",
                      ergebnisse[name][block][key], referenz_v1[ref_name][block][key])

    if ABWEICHUNGEN:
        print(f"\n{len(ABWEICHUNGEN)} Abweichungen - der Nachtrag waere nicht "
              f"belastbar. Abbruch.")
        for label in ABWEICHUNGEN:
            print(f"  FEHLGESCHLAGEN: {label}")
        sys.exit(1)

    print("\n" + "=" * 96)
    print("5) Zweite Korrektur rechnen (alle neun Bots mit dem heutigen Code)")
    print("=" * 96)
    ergebnisse["korrigiert_v2"] = analysiere(heute, cc.ALL_BOTS, "k_v2")
    print("  gerechnet.")

    print("\n" + "=" * 96)
    print("6) Dreifach-Vergleich (Rendite % / Max Drawdown % / Calmar)")
    print("=" * 96)
    print(f"  {'Grundlage':<22}{'Fenster':<26}{'HRP':>28}{'Gleichgewichtung':>28}")
    for name in BASES:
        r = ergebnisse[name]
        h, b = r["hrp_walk_forward"], r["baseline_equal_weight"]
        fenster = f"{r['common_window']['start']}..{r['common_window']['end']}"
        print(f"  {name:<22}{fenster:<26}"
              f"{h['total_return_pct']:>10.2f}/{h['max_drawdown_pct']:>8.2f}/{str(h['calmar_ratio']):>8}"
              f"{b['total_return_pct']:>10.2f}/{b['max_drawdown_pct']:>8.2f}/{str(b['calmar_ratio']):>8}")

    print("\n" + "=" * 96)
    print("7) Kernaussage: 'HRP bringt keinen Vorteil gegenueber Gleichgewichtung'")
    print("=" * 96)
    print(f"  {'Grundlage':<22}{'HRP - Gleichgewichtung (Calmar)':>36}{'Kernaussage haelt?':>24}")
    for name in BASES:
        r = ergebnisse[name]
        diff = r["hrp_walk_forward"]["calmar_ratio"] - r["baseline_equal_weight"]["calmar_ratio"]
        haelt = diff <= 0
        r["hrp_minus_baseline_calmar"] = round(diff, 4)
        r["kernaussage_haelt"] = bool(haelt)
        print(f"  {name:<22}{diff:>36.4f}"
              f"{('ja' if haelt else 'NEIN - HRP waere besser'):>24}")

    stabil = all(ergebnisse[n]["kernaussage_haelt"] for n in BASES)
    print()
    print("  Ueber alle vier Grundlagen hinweg stabil: "
          + ("JA" if stabil else "NEIN - siehe Bericht"))

    print("\n  Buy-and-Hold-Referenz je Grundlage")
    for name in BASES:
        bh = ergebnisse[name]["buy_and_hold"]
        print(f"    {name:<22}{bh['total_return_pct']:>10.2f}%  DD {bh['max_drawdown_pct']:>8.2f}%  "
              f"Calmar {bh['calmar_ratio']}")

    ziel = os.path.join(RESULTS_DIR, "nachtrag_sync_korrektur_v2.json")
    with open(ziel, "w") as handle:
        json.dump({
            "hinweis": ("Zweiter Nachtrag. Nur die Kapitalkurven wurden erneuert - sie "
                        "stammen jetzt aus einem Lauf der heutigen equity_simulation.py. "
                        "Methodik, Annahmen und Auswertung stammen unveraendert aus "
                        "run_walk_forward.py."),
            "bestandsaufnahme": bestandsaufnahme,
            "regressionscheck_bestanden": BESTANDEN,
            "kernaussage_ueber_alle_grundlagen_stabil": bool(stabil),
            "ergebnisse": ergebnisse,
        }, handle, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {ziel}")
    print(f"{BESTANDEN} Referenzwerte bestaetigt, {len(ABWEICHUNGEN)} abweichend.")
    sys.exit(0)


if __name__ == "__main__":
    main()
