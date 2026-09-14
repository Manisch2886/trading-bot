#!/usr/bin/env python3
"""
TB-30a - Beispieldaten: Rohergebnisse mit frei erfundenen Werten
==============================================================================
Das eingefrorene Auswertungsskript muss laufen, BEVOR ein Ergebnis existiert -
sonst waere "eingefroren" eine Absichtserklaerung. Dieses Modul erzeugt dafuer
vollstaendige Rohergebnisse nach dem Vertrag aus `auswertung.py`, mit **frei
erfundenen** Zahlen.

**Diese Zahlen sind keine Messung und sagen ueber keinen Bot etwas aus.** Sie
sind Eingaben, an denen sich das Verhalten des Auswertungsskripts pruefen
laesst - so, wie man eine Waage mit einem Pruefgewicht prueft und nicht mit
einem Sack Mehl.

WIE DIE FLAECHE ENTSTEHT
------------------------------------------------------------------------------
Die Selektionsstatistik ueber dem Raster ist keine Zufallswolke, sondern eine
steuerbare Flaeche: eine glatte Grundform (ein Plateau) plus die Aufschlaege,
die ein Test gerade braucht (eine isolierte Spitze, eine tiefe Delle, ein
Rand, der gewinnt). Dadurch laesst sich JEDE Regel einzeln pruefen - und zwar
am Ablauf des Skripts, nicht an einem von Hand hingelegten Ergebnis.

Die Tagesreihen werden aus den Faltenzielen erzeugt und sind mit ihnen
vertraeglich, aber nicht identisch: der Kapital-Drawdown einer Falte steht in
`zellen.csv`, weil er im echten Lauf aus `equity_simulation.py` kommt, und
nicht aus der Tagesreihe nachgerechnet wird. Das ist auch im echten Lauf so.
"""

import argparse
import json
import math
import os
import sys

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))

import auswertung as aw  # noqa: E402
import faltenplan as fp  # noqa: E402
import registerdaten as rd  # noqa: E402


def _fingerabdruck(text: str) -> int:
    """Stabil ueber Prozesse hinweg - `hash()` ist es nicht (PYTHONHASHSEED)."""
    import hashlib
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)


def standard_sharpe(werte, idx, falte, achsen):
    """Eine glatte Plateau-Flaeche: Mitte hoch, Raender niedriger."""
    namen = sorted(achsen)
    s = 0.0
    for name, i in zip(namen, idx):
        n = len(achsen[name])
        mitte = (n - 1) / 2.0
        s += 1.0 - (abs(i - mitte) / max(mitte, 1.0)) ** 2
    return round(0.20 * s / len(namen), 6)


def standard_drawdown(werte, idx, falte, achsen):
    """Ein Drawdown, der in den Krisenfalten tiefer liegt als sonst.

    Die Werte sind so gewaehlt, dass die Standard-Beispieldaten die
    Drawdown-Bedingung BESTEHEN - sonst liefe jeder Test gegen
    Abbruchkriterium (b) und die uebrigen Regeln kaemen nie dran.
    """
    schwer = falte in ("2020", "2022")
    return round(-3.0 - (8.0 if schwer else 0.0), 2)


def standard_exposure(werte, idx, falte, achsen):
    """Nicht ueber alle Falten gleich - sonst waere der Zufalls-Timing-Test
    entartet: bei konstanter Exposure liefert jede Verschiebung denselben
    Wert, und das Perzentil ist keine Verteilung mehr."""
    return 0.60 if falte in ("2020", "2022") else 0.40


def standard_trades(werte, idx, falte, achsen):
    return 40


def erzeuge(wurzel: str, bot: str, *, mess=None, plan=None,
            sharpe_fn=standard_sharpe, drawdown_fn=standard_drawdown,
            exposure_fn=standard_exposure, trades_fn=standard_trades,
            tagesreihen_fuer=None) -> dict:
    """Schreibt vollstaendige Rohergebnisse fuer einen Bot.

    `tagesreihen_fuer` begrenzt, fuer welche Zellen eine Tagesreihe
    geschrieben wird (None = alle). Der Vertrag verlangt sie fuer jede
    ZULAESSIGE Zelle; das Auswertungsskript liest nur die des Gewinners.
    """
    mess = mess or rd._mess()
    plan = plan or fp.faltenplan(mess)
    achsen = aw.gitterachsen(bot, mess)
    bedingung = aw.bedingung_fuer(bot)
    falten = plan[bot]["falten"]
    if not falten:
        raise SystemExit(f"{bot}: Faltenplan ist ein Platzhalter - "
                         f"Beispieldaten waeren sinnlos.")

    ordner = os.path.join(wurzel, bot)
    os.makedirs(os.path.join(ordner, "tagesreihen"), exist_ok=True)
    os.makedirs(os.path.join(wurzel, "benchmark_tagesreihen"), exist_ok=True)

    zeilen = []
    for idx, werte in aw.alle_zellen(achsen, bedingung):
        zid = aw.zelle_id(achsen, werte)
        for f in falten:
            n = int(trades_fn(werte, idx, f["name"], achsen))
            s = float(sharpe_fn(werte, idx, f["name"], achsen))
            zeile = {"zelle_id": zid}
            for a in sorted(achsen):
                zeile[a] = aw._wert_text(werte[a])
            zeile.update({
                "falte": f["name"], "rolle": f["rolle"], "n_trades": n,
                # Der ROHE Wert, auch in Falten ohne Trade. Wuerde dieses
                # Modul die Null selbst setzen, pruefte der Test hinterher
                # seine eigene Vorarbeit - die Festlegung "Falten ohne Trade
                # zaehlen mit Sharpe 0" gehoert ins Auswertungsskript, und
                # nur dort darf sie wirken.
                "netto_sharpe": s,
                "netto_rendite_pct": round(s * 12.0, 4),
                "kapital_drawdown_pct": float(
                    drawdown_fn(werte, idx, f["name"], achsen)),
                "mittlere_exposure": float(
                    exposure_fn(werte, idx, f["name"], achsen)),
            })
            zeilen.append(zeile)
    df = pd.DataFrame(zeilen)
    df.to_csv(os.path.join(ordner, "zellen.csv"), index=False)

    tage = _handelstage(bot, falten)
    _benchmark(wurzel, rd.BOTS[bot]["markt"], tage)

    gewuenscht = set(df["zelle_id"]) if tagesreihen_fuer is None else set(tagesreihen_fuer)
    for zid in sorted(gewuenscht):
        teil = df[(df["zelle_id"] == zid)]
        _tagesreihe(ordner, zid, bot, falten, teil, tage)

    with open(os.path.join(ordner, "herkunft.json"), "w", encoding="utf-8") as f:
        json.dump({"hinweis": "Beispieldaten - frei erfundene Werte, keine "
                              "Messung. Im echten Lauf steht hier die Herkunft "
                              "aus herkunft.py.",
                   "commit": "0" * 40, "datenstand": "0" * 64,
                   "register": "0" * 64}, f, indent=2, ensure_ascii=False)
    return {"bot": bot, "zeilen": len(df), "tagesreihen": len(gewuenscht)}


def _handelstage(bot: str, falten: list) -> pd.DatetimeIndex:
    frequenz = "B" if rd.BOTS[bot]["markt"] == "aktien" else "D"
    stuecke = [pd.date_range(f["von"],
                             pd.Timestamp(f["bis_ausschliesslich"])
                             - pd.Timedelta(days=1), freq=frequenz)
               for f in falten]
    return pd.DatetimeIndex(np.concatenate([s.values for s in stuecke]))


def _benchmark(wurzel: str, markt: str, tage: pd.DatetimeIndex):
    """Eine erfundene, aber gutartige Benchmark-Reihe: leichte Drift, Rauschen."""
    rng = np.random.default_rng(_fingerabdruck(f"benchmark|{markt}"))
    r = rng.normal(0.0003, 0.010, size=len(tage))
    pd.DataFrame({"datum": tage, "netto_rendite": np.round(r, 8)}).to_csv(
        os.path.join(wurzel, "benchmark_tagesreihen", f"{markt}.csv"), index=False)


def _tagesreihe(ordner: str, zid: str, bot: str, falten: list,
                teil: pd.DataFrame, tage: pd.DatetimeIndex):
    """Tagesreihe, die zu den Faltenzielen dieser Zelle passt.

    Je Falte wird eine Reihe mit dem gewuenschten Sharpe erzeugt: Streuung
    fest, Mittelwert daraus abgeleitet. Die Exposure ist die der Falte.
    """
    pj = aw.perioden_je_jahr(bot)
    rng = np.random.default_rng(_fingerabdruck(zid))
    datum, rend, expo = [], [], []
    for f in falten:
        z = teil[teil["falte"] == f["name"]].iloc[0]
        ziel_sharpe = 0.0 if int(z["n_trades"]) == 0 else float(z["netto_sharpe"])
        maske = ((tage >= pd.Timestamp(f["von"]))
                 & (tage < pd.Timestamp(f["bis_ausschliesslich"])))
        n = int(maske.sum())
        if n == 0:
            continue
        sigma = 0.008
        mu = ziel_sharpe * sigma / math.sqrt(pj)
        roh = rng.normal(0.0, sigma, size=n)
        roh = roh - roh.mean() + mu
        datum.append(tage[maske])
        rend.append(roh)
        expo.append(np.full(n, float(z["mittlere_exposure"])))
    pd.DataFrame({
        "datum": pd.DatetimeIndex(np.concatenate([d.values for d in datum])),
        "netto_rendite": np.round(np.concatenate(rend), 8),
        "exposure": np.round(np.concatenate(expo), 4),
    }).to_csv(os.path.join(ordner, "tagesreihen", f"{aw._dateiname(zid)}.csv"),
              index=False)


def main():
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--ziel", required=True)
    p.add_argument("--bot", action="append",
                   help="nur diese Bots (Standard: alle mit endgueltigem Faltenplan)")
    args = p.parse_args()
    mess = rd._mess()
    plan = fp.faltenplan(mess)
    bots = args.bot or [b for b in rd.BOTS if plan[b]["status"] == "endgueltig"]
    print(__doc__.strip().split("\n")[0])
    print("\n*** Frei erfundene Werte. Keine Messung. ***\n")
    for b in bots:
        info = erzeuge(args.ziel, b, mess=mess, plan=plan)
        print(f"  {b:28s} {info['zeilen']:6d} Zeilen, "
              f"{info['tagesreihen']:5d} Tagesreihen")
    print(f"\nGeschrieben nach: {args.ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
