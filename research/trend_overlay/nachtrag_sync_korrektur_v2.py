"""
Zweiter Nachtrag: Trend-Overlay auf dem HEUTIGEN Stand der Bots
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

**Nur die Kurven aendern sich.** Signal-Konstruktion (200-Tage-MA, logisches
UND beider Maerkte), Marktreferenzen, Fenstergroessen, Exponierungs-Varianten,
IS/OOS-Split und die 2022-Stressperiode kommen unveraendert aus
`run_overlay_analysis.py` bzw. `trend_core.py` - hier ueber
`nachtrag_sync_korrektur.analyse()`, also woertlich dieselbe Funktion, die
schon die erste Korrektur benutzt hat.

Vier Grundlagen:

  original             die Kurven der Erstfassung
                       REGRESSIONSCHECK gegen results/trend_overlay_summary.json
  korrigiert_v1        die erste Korrektur, aus den GESPEICHERTEN Kurven in
                       corrected_curves/ - nicht neu gerechnet
                       REGRESSIONSCHECK gegen results/nachtrag_sync_korrektur.json
  korrigiert_v1_stale  dieselbe, zusaetzlich mit elliott_wave
  korrigiert_v2        alle neun Bots mit dem heutigen Code (PRIMAER)

Zwei Regressionsanker statt einem: der erste zeigt, dass die Auswertung
unveraendert rechnet, der zweite, dass die alte Grundlage exakt reproduziert
wird. Ohne den zweiten waere der Dreifach-Vergleich wertlos.

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
import run_overlay_analysis as roa                 # noqa: E402
import nachtrag_sync_korrektur as v1               # noqa: E402

CURVE_DIR_V1 = os.path.join(_DIR, "corrected_curves")
CURVE_DIR_V2 = os.path.join(_DIR, "corrected_curves_v2")
RESULTS_DIR = roa.RESULTS_DIR
REFERENZ_ERSTFASSUNG = os.path.join(RESULTS_DIR, "trend_overlay_summary.json")
REFERENZ_V1 = os.path.join(RESULTS_DIR, "nachtrag_sync_korrektur.json")
TOL = 0.011

BASES = ("original", "korrigiert_v1", "korrigiert_v1_stale", "korrigiert_v2")
VARIANTS = v1.VARIANTS

BESTANDEN = 0
ABWEICHUNGEN = []


def check(label, ist, soll, tol=TOL):
    global BESTANDEN
    ok = abs(ist - soll) <= tol
    if ok:
        BESTANDEN += 1
        print(f"  OK     {label:<58} {ist:>12.4f}")
    else:
        ABWEICHUNGEN.append(label)
        print(f"  FEHLER {label:<58} {ist:>12.4f}  erwartet {soll}")


def analysiere(generated, swap_bots, basis_name):
    """Woertlich v1.analyse(), nur mit freier Wahl der zu tauschenden Bots.
    v1.analyse() liest seine Tauschliste aus v1.SWAP_FOR; die wird dafuer
    kurzzeitig ergaenzt, statt die Funktion zu kopieren."""
    v1.SWAP_FOR[basis_name] = tuple(swap_bots)
    try:
        return v1.analyse(basis_name, generated)
    finally:
        v1.SWAP_FOR.pop(basis_name, None)


def kernaussage(r):
    """Die drei Teilaussagen der Erstfassung, unveraendert uebernommen aus
    nachtrag_sync_korrektur.py - bewusst NICHT zu einem einzigen Ja/Nein
    verrechnet, weil sie sich unterschiedlich verhalten koennen."""
    full_gain = (r["full_period"]["pausiert_0pct"]["calmar_ratio"]
                 - r["full_period"]["baseline"]["calmar_ratio"])
    oos_gain = (r["out_of_sample"]["pausiert_0pct"]["calmar_ratio"]
                - r["out_of_sample"]["baseline"]["calmar_ratio"])
    oos_dds = {v: r["out_of_sample"][v]["max_drawdown_pct"] for v in VARIANTS}
    oos_dd_gleich = len(set(oos_dds.values())) == 1
    stress = r["stress_period_2022"]["stats"]
    anteil = round(stress["active_days"]
                   / r["signal_stats_primary_window"]["active_days"] * 100, 1)
    return {
        "T1_full_period_calmar_gain": round(full_gain, 4),
        "T1_haelt": bool(full_gain > 0),
        "T2_out_of_sample_drawdowns": oos_dds,
        "T2_haelt": bool(oos_dd_gleich),
        "out_of_sample_calmar_gain": round(oos_gain, 4),
        "out_of_sample_calmar_richtung_wie_erstfassung": bool(oos_gain <= 0),
        "T3_anteil_signaltage_in_2022_pct": anteil,
        "T3_laengste_episode_tage": r["signal_stats_primary_window"]["longest_episode_days"],
        "T3_haelt": bool(anteil > 60),
    }


def main():
    print("=" * 100)
    print("1) Kapitalkurven mit dem HEUTIGEN Bot-Code erzeugen")
    print("=" * 100)
    heute = cc.generate_heute(_REPO_ROOT, CURVE_DIR_V2, po)

    print("\n" + "=" * 100)
    print("2) Bestandsaufnahme: welche Kurve hat sich gegenueber der ersten Korrektur bewegt?")
    print("=" * 100)
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
        bestandsaufnahme[bot] = {"gegenueber_results": wie_results,
                                  "gegenueber_erster_korrektur": wie_v1, **s}
        print(f"  {bot:<28}{wie_results:<18}{wie_v1:<22}"
              f"{s['executed']:>12}{s['return_pct']:>12.2f}")

    print("\n" + "=" * 100)
    print("3) Regressionscheck A - Basis 'original' gegen results/trend_overlay_summary.json")
    print("=" * 100)
    with open(REFERENZ_ERSTFASSUNG) as handle:
        referenz = json.load(handle)
    ergebnisse = {"original": analysiere(heute, (), "original_v2")}
    basis = ergebnisse["original"]
    for periode in ("full_period", "in_sample", "out_of_sample",
                     "robustness_check_150day_window"):
        for variante in VARIANTS:
            for key in ("total_return_pct", "max_drawdown_pct", "calmar_ratio"):
                check(f"{periode} / {variante} / {key}",
                      basis[periode][variante][key], referenz[periode][variante][key])
    check("Signal aktive Tage (200)",
          float(basis["signal_stats_primary_window"]["active_days"]),
          float(referenz["signal_stats_primary_window"]["active_days"]), 0)

    print("\n" + "=" * 100)
    print("4) Regressionscheck B - die erste Korrektur exakt reproduzieren")
    print("=" * 100)
    with open(REFERENZ_V1) as handle:
        referenz_v1 = json.load(handle)["ergebnisse"]
    ergebnisse["korrigiert_v1"] = analysiere(v1_kurven, cc.SWAP_PRIMARY, "k_v1")
    ergebnisse["korrigiert_v1_stale"] = analysiere(v1_kurven, cc.SWAP_WITH_STALE, "k_v1s")
    for name, ref_name in (("korrigiert_v1", "korrigiert"),
                            ("korrigiert_v1_stale", "korrigiert_plus_veraltet")):
        for periode in ("full_period", "in_sample", "out_of_sample"):
            for variante in VARIANTS:
                for key in ("total_return_pct", "max_drawdown_pct", "calmar_ratio"):
                    check(f"{name} / {periode} / {variante} / {key}",
                          ergebnisse[name][periode][variante][key],
                          referenz_v1[ref_name][periode][variante][key])

    if ABWEICHUNGEN:
        print(f"\n{len(ABWEICHUNGEN)} Abweichungen - der Nachtrag waere nicht "
              f"belastbar. Abbruch.")
        for label in ABWEICHUNGEN[:20]:
            print(f"  FEHLGESCHLAGEN: {label}")
        sys.exit(1)

    print("\n" + "=" * 100)
    print("5) Zweite Korrektur rechnen (alle neun Bots mit dem heutigen Code)")
    print("=" * 100)
    ergebnisse["korrigiert_v2"] = analysiere(heute, cc.ALL_BOTS, "k_v2")
    print("  gerechnet.")

    print("\n" + "=" * 100)
    print("6) Dreifach-Vergleich (Rendite % / Max Drawdown % / Calmar)")
    print("=" * 100)
    for periode in ("full_period", "in_sample", "out_of_sample"):
        print(f"\n  {periode}")
        print(f"    {'Grundlage':<22}" + "".join(f"{v:>30}" for v in VARIANTS))
        for name in BASES:
            zellen = ""
            for v in VARIANTS:
                r = ergebnisse[name][periode][v]
                zellen += (f"{r['total_return_pct']:>11.2f}/{r['max_drawdown_pct']:>8.2f}/"
                           f"{str(r['calmar_ratio']):>9}")
            print(f"    {name:<22}{zellen}")

    print("\n" + "=" * 100)
    print("7) Die drei Teilaussagen der Kernaussage - einzeln geprueft")
    print("=" * 100)
    print("   T1  Gesamtzeitraum: der Overlay verbessert die Calmar-Ratio")
    print("   T2  Out-of-Sample:  der Overlay bringt KEINE Drawdown-Verbesserung")
    print("   T3  Die Wirkung ist auf die eine 2022-Episode konzentriert")
    print()
    print(f"  {'Grundlage':<22}{'T1 Calmar-Gewinn':>19}{'T2 OOS-Drawdown':>28}"
          f"{'OOS-Calmar':>14}{'T3 Signaltage 2022':>21}")
    for name in BASES:
        r = ergebnisse[name]
        k = kernaussage(r)
        r["kernaussage"] = k
        dd = k["T2_out_of_sample_drawdowns"]
        dd_text = (f"identisch ({dd['baseline']:.2f} %)" if k["T2_haelt"]
                   else "unterschiedlich")
        print(f"  {name:<22}{k['T1_full_period_calmar_gain']:>+19.4f}{dd_text:>28}"
              f"{k['out_of_sample_calmar_gain']:>+14.4f}"
              f"{k['T3_anteil_signaltage_in_2022_pct']:>20.1f} %")

    stabil = {
        "T1": all(ergebnisse[n]["kernaussage"]["T1_haelt"] for n in BASES),
        "T2": all(ergebnisse[n]["kernaussage"]["T2_haelt"] for n in BASES),
        "T3": all(ergebnisse[n]["kernaussage"]["T3_haelt"] for n in BASES),
        "OOS_Richtung": all(
            ergebnisse[n]["kernaussage"]["out_of_sample_calmar_richtung_wie_erstfassung"]
            for n in BASES),
    }
    print()
    for name, wert in stabil.items():
        print(f"  {name:<14} ueber alle vier Grundlagen stabil: "
              + ("JA" if wert else "NEIN - siehe Bericht"))
    print()
    print("  Das Signal selbst haengt NICHT von den Bot-Kurven ab (es kommt aus BTC und")
    print("  dem Aktien-Proxy) - T3 ist deshalb in allen Grundlagen zahlengleich.")

    ziel = os.path.join(RESULTS_DIR, "nachtrag_sync_korrektur_v2.json")
    with open(ziel, "w") as handle:
        json.dump({
            "hinweis": ("Zweiter Nachtrag. Nur die Kapitalkurven wurden erneuert - sie "
                        "stammen jetzt aus einem Lauf der heutigen equity_simulation.py. "
                        "Signal-Konstruktion, Fenster und Auswertung stammen unveraendert "
                        "aus run_overlay_analysis.py / trend_core.py."),
            "bestandsaufnahme": bestandsaufnahme,
            "regressionscheck_bestanden": BESTANDEN,
            "teilaussagen_stabil": stabil,
            "ergebnisse": ergebnisse,
        }, handle, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {ziel}")
    print(f"{BESTANDEN} Referenzwerte bestaetigt, {len(ABWEICHUNGEN)} abweichend.")
    sys.exit(0)


if __name__ == "__main__":
    main()
