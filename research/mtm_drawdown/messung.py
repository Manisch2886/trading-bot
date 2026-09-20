#!/usr/bin/env python3
"""
TB-73 Schritt 3 - Die Messung: E gegen M, je Bot und je Falte
==============================================================================
Ein Bot, ein Prozess (die neun Bots haben gleichnamige, inhaltlich
verschiedene Module - ein zweiter Bot im selben Prozess laedt still den
falschen):

    trading-env/bin/python3 research/mtm_drawdown/messung.py <bot>

Was importiert wird - und warum hier keine Zahl steht (Auftrag: keine
Konstantenkopie, T56b.6):

  * `equity_simulation` des Bots: `STARTING_CAPITAL`, `ALLOCATION_PCT`,
    `MAX_CONCURRENT_POSITIONS` - zum Abgleich mit dem TB-24-Meta, das die
    Trade-Liste beschreibt.
  * das Backtest-Modul des Bots: `TRADING_FEE_PCT`, `SLIPPAGE_PCT` - die
    Kosten, die der Backtest beim Ausstieg von `pnl_pct` abzieht. Die
    Bewertung offener Positionen zieht die Einstiegsseite davon ab
    (mtm_kern, Abschnitt "Die Kosten"). Gegengeprueft an der Liste selbst:
    pnl_pct = (exit/entry - 1) * 100 - 2 * (Gebuehr + Slippage), gerundet.
  * `shared/messkette.py`: `max_drawdown_ungerundet` (die Drawdown-Rechnung
    der neun Bots) und `calculate_max_drawdown` (Gegenprobe ueber den
    ganzen Zeitraum).
  * `shared/zuteilung.py`: `SEED` - nur protokolliert. Zugeteilt wird hier
    nichts: E und M rechnen auf DENSELBEN ausgefuehrten Positionen, die die
    Kaskade in TB-24 vergeben hat (Liste `<bot>_positionen.csv`,
    `kennzeichnung_neutral` und Abgleich mit der Exposure-Messung dort).
  * `research/exposure_messung/exposure_kern.py`: `taegliche_reihen` und
    `exposure_reihe` - die Exposure-Definition des Projekts (Brutto,
    Kalendertage, Nenner Kapital zu Tagesbeginn), je Falte gemittelt. Sie
    ist das Exposure-Argument, das der Benchmark tragen wuerde - berichtet,
    nicht nachgeschlagen: `benchmark.py` wird hier nicht aufgerufen, keine
    Grenze steht neben den Zahlen (Register 24.3).

Die Bot-Umgebung (sys.path, Stubs fuer Abrufmodule) kommt aus
`research/drawdown_reihenfolge/botenv.py` - dem Muster, nach dem dieser
Ordner gebaut ist; nichts davon wird hier ein zweites Mal geschrieben. Die
Stubs werden nie aufgerufen; gelesen werden nur die CSVs in data/.

Die Falten kommen aus `research/vorregistrierung/ergebnisse/faltenplan_tb72.json`
(TB-72); `faltenplan.json` auf der Platte ist TB-30a-Stand (K4k).

Geschrieben wird nur unter research/mtm_drawdown/ergebnisse/:
  <bot>.json           Messung je Falte, Mediane, Nachweise, Laufzeit
  <bot>_tagespfad.csv  die Tagesreihe (buch = E_tag, mtm = M, n_offen, ...)
"""

import json
import os
import sys
import time

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(_HIER))
ERGEBNISSE = os.path.join(_HIER, "ergebnisse")

sys.path.insert(0, _HIER)
sys.path.insert(0, os.path.join(REPO_ROOT, "research", "drawdown_reihenfolge"))
sys.path.insert(0, os.path.join(REPO_ROOT, "research", "exposure_messung"))

import botenv                                   # noqa: E402  (drawdown_reihenfolge)
import mtm_kern                                 # noqa: E402
import grundlage                                # noqa: E402

# Welches Modul des Bots die Kosten traegt (Name, keine Zahl). Dieselben zwei
# Konstanten stehen je Bot auch in forward_test.py; die Trade-Listen aus TB-24
# entstanden aus dem Backtest-Modul (collect_all_trades -> get_trades_for_symbol).
BACKTEST_MODUL = {
    "elliott_wave": "backtest_elliott",
    "elliott_wave_stocks": "backtest_elliott",
    "t3_supertrend": "backtest_trend",
    "rsi2_crypto": "backtest_rsi2",
    "rsi2_mean_reversion": "backtest_rsi2",
    "turtle_soup_crypto": "backtest_turtle_soup",
    "turtle_soup_stocks": "backtest_turtle_soup",
    "volatility_breakout": "backtest_breakout",
    "volatility_breakout_crypto": "backtest_breakout",
}


def kosten_gegen_liste(pos: pd.DataFrame, kosten_rundreise_pct: float) -> dict:
    """pnl_pct der Liste gegen (exit/entry - 1) * 100 - Kosten, auf zwei
    Stellen gerundet wie im Backtest. Groesste Abweichung in Prozentpunkten;
    sie muss innerhalb der Rundung liegen (0,005 + Rechenrauschen)."""
    roh = (pos["exit_price"] / pos["entry_price"] - 1.0) * 100.0 - kosten_rundreise_pct
    abw = (pos["pnl_pct"] - roh).abs()
    return {"max_abweichung_pp": float(abw.max()), "innerhalb_rundung": bool(abw.max() <= 0.005 + 1e-6)}


def exposure_je_falte(pos: pd.DataFrame, startkapital: float, falten: list, ek) -> dict:
    """Mittlere Brutto-Exposure je Falte nach exposure_kern (Kalendertage)."""
    reihen = ek.taegliche_reihen(pos, startkapital)
    expo = ek.exposure_reihe(reihen)
    aus = {}
    for f in falten:
        von, bis = pd.Timestamp(f["von"]), pd.Timestamp(f["bis_ausschliesslich"])
        e = expo[(expo.index >= von) & (expo.index < bis)]
        aus[f["name"]] = (round(float(e.mean()), 4) if len(e) else None)
    return aus


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit(f"Aufruf: python3 {os.path.basename(__file__)} <bot>")
    bot = botenv.setup(argv[0])
    t0 = time.time()

    import equity_simulation as es                                   # noqa: E402
    import importlib
    bt = importlib.import_module(BACKTEST_MODUL[bot])
    from messkette import max_drawdown_ungerundet, calculate_max_drawdown   # noqa: E402
    from zuteilung import SEED                                       # noqa: E402
    import exposure_kern as ek                                       # noqa: E402

    kosten_seite = float(bt.TRADING_FEE_PCT) + float(bt.SLIPPAGE_PCT)
    startkapital = float(es.STARTING_CAPITAL)

    pos, meta, grund = grundlage.lade_positionen(bot)
    if pos is None:
        raise SystemExit(f"{bot}: keine Grundlage - {grund}")
    falten = grundlage.lade_falten(bot)

    abgleich_meta = {
        "startkapital": {"es": startkapital, "meta": meta.get("startkapital"),
                         "gleich": float(meta.get("startkapital")) == startkapital},
        "allocation_pct": {"es": float(es.ALLOCATION_PCT), "meta": meta.get("allocation_pct"),
                           "gleich": abs(float(meta.get("allocation_pct")) - float(es.ALLOCATION_PCT)) < 1e-12},
        "positionslimit": {"es": getattr(es, "MAX_CONCURRENT_POSITIONS", None),
                           "meta": meta.get("max_concurrent_positions")},
    }
    kosten = {"modul": BACKTEST_MODUL[bot], "TRADING_FEE_PCT": float(bt.TRADING_FEE_PCT),
              "SLIPPAGE_PCT": float(bt.SLIPPAGE_PCT), "je_seite_pct": kosten_seite,
              "rundreise_pct": 2 * kosten_seite,
              "gegen_liste": kosten_gegen_liste(pos, 2 * kosten_seite)}

    # --- E: die Ereigniskurve in Kurvenreihenfolge ---------------------------
    ereignisse = mtm_kern.ereignisreihenfolge(pos, startkapital)
    kurve = mtm_kern.ereigniskurve(ereignisse)
    dd_gesamt_bot = calculate_max_drawdown(pd.DataFrame({"capital_after": kurve.to_numpy()}), startkapital)

    # --- M: Tagesraster aus den 1d-Dateien der gehandelten Symbole -----------
    tages = grundlage.lade_schlusskurse(pos["symbol"].unique(), "1d")
    fehlend = sorted(set(pos["symbol"].unique()) - set(tages))
    if fehlend:
        raise SystemExit(f"{bot}: 1d-Kursdatei fehlt fuer {fehlend}")
    plan_von = min(pd.Timestamp(f["von"]) for f in falten)
    plan_bis = max(pd.Timestamp(f["bis_ausschliesslich"]) for f in falten)
    tage = mtm_kern.tagesraster(
        tages,
        von=min(plan_von, ereignisse["entry_time"].min().normalize()),
        bis=max(plan_bis, ereignisse["exit_time"].max().normalize() + mtm_kern.EIN_TAG))
    kurse, fort = mtm_kern.kurse_auf_raster(tages, tage)
    pfad = mtm_kern.mtm_pfad(ereignisse, kurse, fort, startkapital, kosten_seite)
    dd_gesamt_m = mtm_kern.drawdown_falte(pfad["mtm"], startkapital, max_drawdown_ungerundet)
    dd_gesamt_e_tag = mtm_kern.drawdown_falte(pfad["buch"], startkapital, max_drawdown_ungerundet)

    # --- je Falte -------------------------------------------------------------
    messung = mtm_kern.messe_falten(kurve, pfad, falten, startkapital, max_drawdown_ungerundet)
    grund_je_falte = {g["falte"]: g for g in grundlage.falten_grundlage(pos, falten)}
    expo = exposure_je_falte(pos, startkapital, falten, ek)
    for z in messung:
        g = grund_je_falte[z["falte"]]
        z["grundlage"] = g["grundlage"]
        z["liste_ab"] = g["liste_ab"]
        z["exposure_mittel"] = expo.get(z["falte"])
        if z["grundlage"] == "keine":
            # keine erfundene Zahl: Werte auf None, Falte bleibt in der Liste
            for k in ("E", "E_tag", "M", "M_minus_E_pp", "faktor_M_zu_E", "exposure_mittel"):
                z[k] = None
            z["M_flacher_als_E"] = None
            z["M_flacher_als_E_tag"] = None

    richtung = {
        "faelle_M_flacher_als_E": [z["falte"] for z in messung if z["M_flacher_als_E"]],
        "faelle_M_flacher_als_E_tag": [z["falte"] for z in messung if z["M_flacher_als_E_tag"]],
        "faelle_E_flacher_als_E_tag": [z["falte"] for z in messung
                                       if z["E"] is not None and z["E"] > z["E_tag"] + 1e-9],
    }

    laufzeit = round(time.time() - t0, 1)
    aus = {
        "bot": bot,
        "zeitrahmen": meta.get("zeitrahmen"),
        "anlageklasse": meta.get("anlageklasse"),
        "quelle_positionen": os.path.relpath(os.path.join(grundlage.TB24_DIR, f"{bot}_positionen.csv"), REPO_ROOT),
        "quelle_falten": os.path.relpath(grundlage.FALTENPLAN, REPO_ROOT),
        "positionen": int(len(pos)),
        "erster_einstieg": str(pos["entry_time"].min()),
        "letzter_ausstieg": str(pos["exit_time"].max()),
        "startkapital": startkapital,
        "abgleich_meta": abgleich_meta,
        "kosten": kosten,
        "zuteilung_seed_protokolliert": int(SEED),
        "raster": {"von": str(tage[0].date()), "bis_einschliesslich": str(tage[-1].date()),
                   "tage": int(len(tage)), "fortgeschriebene_kurstage": int(pfad["fortgeschrieben"].sum())},
        "gesamt": {"E_calculate_max_drawdown": dd_gesamt_bot, "E_tag": dd_gesamt_e_tag, "M": dd_gesamt_m},
        "falten": messung,
        "median_selektion": {
            "E": mtm_kern.median_selektion(messung, "E"),
            "E_tag": mtm_kern.median_selektion(messung, "E_tag"),
            "M": mtm_kern.median_selektion(messung, "M"),
            "M_minus_E_pp": mtm_kern.median_selektion(messung, "M_minus_E_pp"),
            "selektionsfalten_mit_grundlage": [z["falte"] for z in messung
                                               if z["rolle"] == "selektion" and z["grundlage"] != "keine"],
        },
        "richtungsprobe": richtung,
        "laufzeit_s": laufzeit,
        "interpreter": sys.version.split()[0],
    }

    os.makedirs(ERGEBNISSE, exist_ok=True)
    with open(os.path.join(ERGEBNISSE, f"{bot}.json"), "w", encoding="utf-8") as f:
        json.dump(aus, f, indent=1, ensure_ascii=False, default=str)
    pfad.round(4).to_csv(os.path.join(ERGEBNISSE, f"{bot}_tagespfad.csv"), index_label="tag")

    print(f"{bot}: {len(pos)} Positionen, Raster {aus['raster']['tage']} Tage, "
          f"Kosten je Seite {kosten_seite:.4g} % ({kosten['modul']}), "
          f"Kostenabgleich {kosten['gegen_liste']}")
    print(f"  gesamt: E {dd_gesamt_bot}  E_tag {dd_gesamt_e_tag}  M {dd_gesamt_m}")
    for z in messung:
        if z["grundlage"] == "keine":
            print(f"  {z['falte']:>9} {z['rolle'][:3]}  keine Grundlage")
            continue
        print(f"  {z['falte']:>9} {z['rolle'][:3]}  E {z['E']:>7.2f}  E_tag {z['E_tag']:>7.2f}  "
              f"M {z['M']:>7.2f}  dM-E {z['M_minus_E_pp']:>6.2f} pp  x{z['faktor_M_zu_E'] or '-'}  "
              f"expo {z['exposure_mittel']:.3f}  offen@Start {z['offen_am_faltenbeginn']}"
              f"{'  TEILWEISE ab ' + z['liste_ab'] if z['grundlage'] == 'teilweise' else ''}"
              f"{'  M FLACHER ALS E' if z['M_flacher_als_E'] else ''}")
    print(f"  Median Selektion: E {aus['median_selektion']['E']}  M {aus['median_selektion']['M']}  "
          f"Richtung: {richtung}  Laufzeit {laufzeit} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
