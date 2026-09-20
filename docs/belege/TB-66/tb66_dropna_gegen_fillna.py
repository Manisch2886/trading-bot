#!/usr/bin/env python3
"""
TB-66, Abschnitt 1 - die Messung, die vor der Formulierungsentscheidung steht:
`.dropna()` (Fassung W, so rechnet benchmark.py) gegen `.fillna(0)` (Fassung C,
Code an den Wortlaut "Tage, an denen kein Symbol handelbar ist, tragen
Rendite 0"). Rein lesend; benchmark.py wird importiert, nicht veraendert;
geschrieben wird nur in das per --ziel genannte Verzeichnis.

DREI FASSUNGEN JE BOT UND FALTE
------------------------------------------------------------------------------
W       benchmark.py::bh_tagesrenditen, unveraendert: Tage ohne Rendite
        (alle Symbole NaN) fallen weg.
C_lit   dieselbe Rechnung, `.dropna()` durch `.fillna(0)` ersetzt - woertlich
        die Fassung C des Auftrags. ⚠️ Der Rahmen kennt nur Tage, an denen
        mindestens ein Symbol einen KURS hat (Vereinigung der ab dem
        Handelbar-Tag beginnenden Reihen). Tage VOR dem ersten Handelbar-Tag
        eines Bots stehen gar nicht im Rahmen; C_lit setzt nur die Tage auf 0,
        an denen ein Kurs, aber keine Rendite vorliegt (erster Punkt der
        Vereinigung, Tage an denen jedes handelbare Symbol NaN liefert).
C_voll  der Wortlaut vollstaendig: die Renditereihe wird auf den KALENDER der
        Falte gesetzt und jeder fehlende Tag traegt 0. Kalender = alle Tage,
        an denen irgendein Symbol des Universums (ungekuerzt) einen Schlusskurs
        hat - Krypto jeder Kalendertag, Aktien jeder Boersentag.

Berichtet je Falte: DD auf allen 100 Exposure-Stufen (Zahl der abweichenden
Stufen, groesste Abweichung), `handelstage` in allen drei Fassungen; je Bot
die DD_Toleranz-Stufen, die sich unterscheiden.
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(WURZEL, "research", "vorregistrierung"))
import benchmark as bm  # noqa: E402
import faltenplan as fp  # noqa: E402
import registerdaten as rd  # noqa: E402
import faltenschranke_messung as fsm  # noqa: E402


def c_lit(reihen: dict) -> pd.Series:
    """Fassung C woertlich: .dropna() -> .fillna(0), sonst bh_tagesrenditen."""
    rahmen = pd.DataFrame(reihen).sort_index()
    return rahmen.pct_change().mean(axis=1, skipna=True).fillna(0)


def _tab(fenster):
    return {bm._schluessel(e): bm.drawdown_bei_exposure(fenster, e)
            for e in bm.EXPOSURE_STUFEN}


def _fenster(r, von, bis):
    if r.empty:
        return r
    return r[(r.index >= von) & (r.index < bis)]


def _median(sel):
    aus = {}
    for e in bm.EXPOSURE_STUFEN:
        k = bm._schluessel(e)
        w = [t[k] for t in sel]
        aus[k] = round(float(np.median(w)), 2) if w else 0.0
    return aus


def _diff(a, b):
    stufen = [k for k in a if a[k] != b[k]]
    groesste = max((abs(a[k] - b[k]) for k in stufen), default=0.0)
    return len(stufen), round(groesste, 2)


def main(argv=None):
    z = argparse.ArgumentParser()
    z.add_argument("--ziel", required=True)
    ziel = z.parse_args(argv).ziel
    os.makedirs(ziel, exist_ok=True)

    plan = fp.faltenplan(rd._mess())
    kurse = {m: bm.tagesschluss(m) for m in ("aktien", "krypto")}
    kalender = {m: pd.DataFrame(kurse[m]).sort_index().index for m in kurse}

    aus = {}
    zeilen = []
    for bot, eig in rd.BOTS.items():
        markt = eig["markt"]
        lesart = fsm.loader_lesart(bot)
        hab = {s: pd.Timestamp(d) for s, d in lesart["handelbar_ab"].items() if d}
        reihen = bm.tagesgenau(kurse[markt], hab)
        r_w = bm.bh_tagesrenditen(reihen)
        r_c = c_lit(reihen)
        e = {"markt": markt, "falten": {}, "dd_toleranz": {}}
        sel = {"W": [], "C_lit": [], "C_voll": []}
        for f in plan[bot]["falten"]:
            von, bis = pd.Timestamp(f["von"]), pd.Timestamp(f["bis_ausschliesslich"])
            w = _fenster(r_w, von, bis)
            cl = _fenster(r_c, von, bis)
            kal = kalender[markt][(kalender[markt] >= von) & (kalender[markt] < bis)]
            cv = r_c.reindex(kal).fillna(0) if not r_c.empty else pd.Series(0.0, index=kal)
            t = {"W": _tab(w), "C_lit": _tab(cl), "C_voll": _tab(cv)}
            n_cl, g_cl = _diff(t["W"], t["C_lit"])
            n_cv, g_cv = _diff(t["W"], t["C_voll"])
            e["falten"][f["name"]] = {
                "rolle": f["rolle"],
                "handelstage": {"W": int(len(w)), "C_lit": int(len(cl)), "C_voll": int(len(cv))},
                "dd_stufen_verschieden_W_C_lit": n_cl, "groesste_abweichung_W_C_lit": g_cl,
                "dd_stufen_verschieden_W_C_voll": n_cv, "groesste_abweichung_W_C_voll": g_cv,
                "dd_100": {k: t[k]["1.00"] for k in t},
            }
            zeilen.append((bot, f["name"], f["rolle"], len(w), len(cl), len(cv), n_cl, g_cl, n_cv, g_cv,
                           t["W"]["1.00"], t["C_lit"]["1.00"], t["C_voll"]["1.00"]))
            if f["rolle"] == "selektion":
                for k in sel:
                    sel[k].append(t[k])
        for k in sel:
            e["dd_toleranz"][k] = _median(sel[k])
        e["dd_toleranz_stufen_verschieden"] = {
            "W_C_lit": _diff(e["dd_toleranz"]["W"], e["dd_toleranz"]["C_lit"])[0],
            "W_C_voll": _diff(e["dd_toleranz"]["W"], e["dd_toleranz"]["C_voll"])[0],
        }
        aus[bot] = e

    with open(os.path.join(ziel, "schritt3_dropna_gegen_fillna.json"), "w", encoding="utf-8") as f:
        json.dump(aus, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    print(__doc__.strip().split("\n")[0])
    print(f"\n{'Bot':28s} {'Falte':10s} {'Rolle':12s} {'Tage W':>6s} {'C_lit':>6s} {'C_voll':>6s} "
          f"{'DD-Stufen W!=C_lit':>18s} {'max':>6s} {'DD-Stufen W!=C_voll':>19s} {'max':>6s} "
          f"{'DD@100 W':>9s} {'C_lit':>8s} {'C_voll':>8s}")
    for r in zeilen:
        print(f"{r[0]:28s} {r[1]:10s} {r[2]:12s} {r[3]:6d} {r[4]:6d} {r[5]:6d} "
              f"{r[6]:18d} {r[7]:6.2f} {r[8]:19d} {r[9]:6.2f} {r[10]:9.2f} {r[11]:8.2f} {r[12]:8.2f}")
    print()
    for bot, e in aus.items():
        v = e["dd_toleranz_stufen_verschieden"]
        print(f"{bot:28s} DD_Toleranz-Stufen verschieden: W gegen C_lit {v['W_C_lit']:3d}, "
              f"W gegen C_voll {v['W_C_voll']:3d}")
    n_dd_lit = sum(r[6] for r in zeilen); n_dd_voll = sum(r[8] for r in zeilen)
    n_tage_lit = sum(1 for r in zeilen if r[3] != r[4]); n_tage_voll = sum(1 for r in zeilen if r[3] != r[5])
    print(f"\nSumme ueber {len(zeilen)} Falten: DD-Stufen verschieden W/C_lit = {n_dd_lit}, W/C_voll = {n_dd_voll}; "
          f"Falten mit anderer handelstage-Zahl: C_lit {n_tage_lit}, C_voll {n_tage_voll}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
