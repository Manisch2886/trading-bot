#!/usr/bin/env python3
"""
TB-65 - Frage C, nachrichtlich: die Benchmark-Tabelle aus TB-61 mit der
Loader-Schranke je Bot statt vier Jahren. Laeuft NUR in der Wegwerf-Kopie
research/_tb65_kopie/ (zwei Ebenen unter der Repo-Wurzel, sonst zeigt
BASE_DIR ins Leere). Fasst keine Datei im Repo an; schreibt ausschliesslich
in das per --ziel genannte Verzeichnis.

WAS GERECHNET WIRD - JE BOT UND FALTE, VIER FASSUNGEN
------------------------------------------------------------------------------
V0  "vorher": point_in_time(..., MINDESTTRAINING_JAHRE = 4) - exakt die
    Rechnung aus benchmark.py::je_bot. Muss benchmark_drawdowns_neu.json
    (TB-61) zeichengleich reproduzieren, sonst misst diese Kopie etwas
    anderes als TB-61.
VH  "geladen, ganze Falte": das Symbol geht fuer die GANZE Falte ein, wenn es
    in der Falte nach Lesart H (Register 16.2) an mindestens einem Handelstag
    geladen ist. Die Menge je Falte ist NICHT nachgebaut, sondern GELESEN aus
    dem Trockenlauf des Laufcodes (TB-56, Spalte H:
    research/faltenplan_neun/daten/faltenplan_ohne_schranke.json,
    trockenlauf_3b.je_bot.<bot>.falten[].H_symbole).
VT  "geladen, taeglich": das Symbol geht ab dem Tag NACH seinem
    Handelbar-Datum ein (erster Kurstag + MIN_HISTORY_DAYS; elliott_wave:
    Datum der 17 520. 1h-Kerze) - nachgerechnet mit
    research/faltenplan_neun/faltenschranke_messung.py::loader_lesart, dem
    Werkzeug aus TB-56. Innerhalb einer Falte wechselt die Menge also.
VF  "Loader-Schranke am Faltenbeginn": point_in_time mit MIN_HISTORY_* statt
    vier Jahren - das Symbol zaehlt fuer die ganze Falte, wenn sein
    Handelbar-Datum <= Faltenbeginn ist. Das ist die mechanische Lesart
    "vier Jahre durch die Loader-Schranke ersetzen"; sie entspricht Lesart F,
    die das Register NICHT gewaehlt hat (16.2). Nur zur Einordnung.

Die vier gesperrten Rechenfunktionen (bh_tagesrenditen, drawdown_bei_exposure,
nachschlagen, erlaubt) werden unveraendert aus benchmark.py importiert; die
Medianbildung ist dieselbe wie in je_bot (Median ueber ALLE Selektionsfalten,
leere Falte = 0.0).
"""

import argparse
import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)
import benchmark as bm  # noqa: E402  (aus der Kopie)
import faltenplan as fp  # noqa: E402
import registerdaten as rd  # noqa: E402

sys.path.insert(0, os.path.join(bm.BASE_DIR, "research", "faltenplan_neun"))
import faltenschranke_messung as fsm  # noqa: E402

TROCKENLAUF = os.path.join(bm.BASE_DIR, "research", "faltenplan_neun", "daten",
                           "faltenplan_ohne_schranke.json")
NEU = os.path.join(bm.BASE_DIR, "research", "vorregistrierung", "ergebnisse",
                   "benchmark_drawdowns_neu.json")
STUFEN = ("0.25", "0.50", "1.00")


def _tab(fenster):
    return {bm._schluessel(e): bm.drawdown_bei_exposure(fenster, e)
            for e in bm.EXPOSURE_STUFEN}


def _fenster(renditen, von, bis):
    if renditen.empty:
        return renditen
    return renditen[(renditen.index >= von) & (renditen.index < bis)]


def _median(sel):
    aus = {}
    for e in bm.EXPOSURE_STUFEN:
        k = bm._schluessel(e)
        werte = [t[k] for t in sel]
        aus[k] = round(float(np.median(werte)), 2) if werte else 0.0
    return aus


def handelbar_ab(bot):
    """Handelbar-Datum je Symbol, GELESEN ueber das TB-56-Werkzeug."""
    l = fsm.loader_lesart(bot)
    return ({s: pd.Timestamp(d) for s, d in l["handelbar_ab"].items() if d},
            l["schranke"], l["wert"])


def rechne(bot, eig, plan, kurse, h_falten):
    markt = eig["markt"]
    reihen_alle = kurse[markt]
    hab, schranke_name, schranke_wert = handelbar_ab(bot)
    # Tagesrenditen je Symbol, dieselbe Rechnung wie bh_tagesrenditen, nur
    # VOR der Mittelung - damit die Menge je Tag wechseln kann (VT).
    rahmen = pd.DataFrame(reihen_alle).sort_index().pct_change()
    aus = {"markt": markt, "schranke": f"{schranke_name} = {schranke_wert}",
           "falten": {}, "dd_toleranz": {}}
    sel = {"V0": [], "VH": [], "VT": [], "VF": []}
    for f in plan["falten"]:
        von = pd.Timestamp(f["von"])
        bis = pd.Timestamp(f["bis_ausschliesslich"])
        eintrag = {"rolle": f["rolle"], "von": f["von"],
                   "bis_ausschliesslich": f["bis_ausschliesslich"]}

        # V0 - exakt benchmark.py::je_bot
        r0 = bm.point_in_time(reihen_alle, dt.date.fromisoformat(f["von"]),
                              rd.MINDESTTRAINING_JAHRE)
        w0 = _fenster(bm.bh_tagesrenditen(r0), von, bis)
        eintrag["V0"] = {"symbole": len(r0), "handelstage": int(len(w0)),
                         "dd": _tab(w0)}

        # VH - H_symbole aus dem Trockenlauf, ganze Falte
        h = (h_falten.get("Bestaetigung") if f["rolle"] == "bestaetigung"
             else h_falten.get(f["name"]))
        if h is None:
            eintrag["VH"] = {"symbole": None, "handelstage": None, "dd": None,
                             "hinweis": "Falte nicht im Trockenlauf TB-56"}
        else:
            rh = {s: reihen_alle[s] for s in h["H_symbole"] if s in reihen_alle}
            wh = _fenster(bm.bh_tagesrenditen(rh), von, bis)
            eintrag["VH"] = {"symbole": len(rh), "handelstage": int(len(wh)),
                             "dd": _tab(wh), "H_trockenlauf": h["H"],
                             "F_trockenlauf": h["F"]}

        # VT - taeglich ab dem Tag nach dem Handelbar-Datum
        maske = pd.DataFrame(False, index=rahmen.index, columns=rahmen.columns)
        for s in rahmen.columns:
            if s in hab:
                maske[s] = rahmen.index > hab[s]
        rt = rahmen.where(maske)
        mt = rt.mean(axis=1, skipna=True).dropna()
        wt = _fenster(mt, von, bis)
        aktiv = [s for s in rahmen.columns
                 if s in hab and hab[s] < bis - pd.Timedelta(days=1)]
        eintrag["VT"] = {"symbole_irgendwann_in_falte": len(aktiv),
                         "handelstage": int(len(wt)), "dd": _tab(wt)}

        # VF - Loader-Schranke am Faltenbeginn (Lesart F, zur Einordnung)
        rf = {s: reihen_alle[s] for s in reihen_alle
              if s in hab and hab[s] <= von}
        wf = _fenster(bm.bh_tagesrenditen(rf), von, bis)
        eintrag["VF"] = {"symbole": len(rf), "handelstage": int(len(wf)),
                         "dd": _tab(wf)}

        aus["falten"][f["name"]] = eintrag
        if f["rolle"] == "selektion":
            sel["V0"].append(eintrag["V0"]["dd"])
            if eintrag["VH"]["dd"] is not None:
                sel["VH"].append(eintrag["VH"]["dd"])
            sel["VT"].append(eintrag["VT"]["dd"])
            sel["VF"].append(eintrag["VF"]["dd"])
    for v in ("V0", "VH", "VT", "VF"):
        aus["dd_toleranz"][v] = _median(sel[v])
        aus["dd_toleranz"][v + "_n_selektionsfalten"] = len(sel[v])
    # t3_supertrend: Register 21.4 laesst 3b (a) binden (erste Falte 2019);
    # die Falte 2018 des 4a-Plans faellt dort weg. Nachrichtlich der Median
    # ohne sie.
    if bot == "t3_supertrend":
        for v in ("V0", "VH", "VT", "VF"):
            ohne = [aus["falten"][n][v]["dd"] for n in aus["falten"]
                    if aus["falten"][n]["rolle"] == "selektion" and n != "2018"
                    and aus["falten"][n][v]["dd"] is not None]
            aus["dd_toleranz"][v + "_ohne_2018_nach_21_4"] = _median(ohne)
    return aus


def main(argv=None):
    z = argparse.ArgumentParser()
    z.add_argument("--ziel", required=True, help="Ausgabeverzeichnis (Belege)")
    ziel = z.parse_args(argv).ziel
    os.makedirs(ziel, exist_ok=True)

    mess = rd._mess()
    plan = fp.faltenplan(mess)
    kurse = {m: bm.tagesschluss(m) for m in ("aktien", "krypto")}
    tl = json.load(open(TROCKENLAUF, encoding="utf-8"))["trockenlauf_3b"]["je_bot"]
    neu = json.load(open(NEU, encoding="utf-8"))

    ergebnis = {}
    for bot, eig in rd.BOTS.items():
        h_falten = {f["falte"]: f for f in tl[bot]["falten"]}
        ergebnis[bot] = rechne(bot, eig, plan[bot], kurse, h_falten)

    # Gegenprobe 1: V0 zeichengleich mit benchmark_drawdowns_neu.json?
    abw = 0
    for bot, e in ergebnis.items():
        for name, f in e["falten"].items():
            alt = neu[bot]["falten"][name]
            if (alt["symbole_point_in_time"] != f["V0"]["symbole"]
                    or alt["handelstage"] != f["V0"]["handelstage"]
                    or alt["dd_benchmark"] != f["V0"]["dd"]):
                abw += 1
        if neu[bot]["dd_toleranz"] != e["dd_toleranz"]["V0"]:
            abw += 1
    ergebnis["_gegenprobe_V0_gegen_benchmark_drawdowns_neu"] = {
        "abweichungen": abw, "sha256_neu_geprueft_von": NEU}

    # Gegenprobe 2: Symbolzahl VH gegen die Trockenlauf-Spalte H und VT
    # (irgendwann in Falte) gegen H - misst, ob die nachgerechneten
    # Handelbar-Daten dieselbe Menge ergeben wie der Loader selbst.
    g2 = {"VH_gleich_H": 0, "VH_ungleich_H": 0, "VT_gleich_H": 0,
          "VT_ungleich_H": [], "VF_gleich_F": 0, "VF_ungleich_F": []}
    for bot, e in ergebnis.items():
        if bot.startswith("_"):
            continue
        for name, f in e["falten"].items():
            if f["VH"]["dd"] is None:
                continue
            if f["VH"]["symbole"] == f["VH"]["H_trockenlauf"]:
                g2["VH_gleich_H"] += 1
            else:
                g2["VH_ungleich_H"] += 1
            if f["VT"]["symbole_irgendwann_in_falte"] == f["VH"]["H_trockenlauf"]:
                g2["VT_gleich_H"] += 1
            else:
                g2["VT_ungleich_H"].append(
                    (bot, name, f["VT"]["symbole_irgendwann_in_falte"],
                     f["VH"]["H_trockenlauf"]))
            if f["VF"]["symbole"] == f["VH"]["F_trockenlauf"]:
                g2["VF_gleich_F"] += 1
            else:
                g2["VF_ungleich_F"].append(
                    (bot, name, f["VF"]["symbole"], f["VH"]["F_trockenlauf"]))
    ergebnis["_gegenprobe_mengen_gegen_trockenlauf"] = g2

    with open(os.path.join(ziel, "frage_c_rechnung.json"), "w",
              encoding="utf-8") as f:
        json.dump(ergebnis, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    # Kurzbericht
    print("TB-65 Frage C - nachrichtlich, Kopie:", _HIER)
    print("Gegenprobe V0 gegen benchmark_drawdowns_neu.json: "
          f"{abw} Abweichungen")
    print("Gegenprobe Mengen:", json.dumps(g2))
    for bot, e in ergebnis.items():
        if bot.startswith("_"):
            continue
        print(f"\n{bot} ({e['markt']}, {e['schranke']})")
        print(f"  {'Falte':10s} {'Rolle':4s} | {'V0 sym/tage':>12s} | "
              f"{'VH sym/tage (H/F tl)':>22s} | {'VT sym/tage':>12s} | "
              f"{'VF sym/tage':>12s} | DD@100%: V0 / VH / VT / VF")
        for name, f in e["falten"].items():
            vh = f["VH"]
            vhs = (f"{vh['symbole']}/{vh['handelstage']} ({vh['H_trockenlauf']}/"
                   f"{vh['F_trockenlauf']})" if vh["dd"] is not None else "-")
            dd = lambda v: (f"{f[v]['dd']['1.00']:7.2f}" if f[v]["dd"] is not None
                            else "      -")
            print(f"  {name:10s} {f['rolle'][:4]:4s} | "
                  f"{f['V0']['symbole']:>4d}/{f['V0']['handelstage']:<7d} | "
                  f"{vhs:>22s} | "
                  f"{f['VT']['symbole_irgendwann_in_falte']:>4d}/{f['VT']['handelstage']:<7d} | "
                  f"{f['VF']['symbole']:>4d}/{f['VF']['handelstage']:<7d} | "
                  f"{dd('V0')} / {dd('VH')} / {dd('VT')} / {dd('VF')}")
        for v in ("V0", "VH", "VT", "VF"):
            t = e["dd_toleranz"][v]
            n = e["dd_toleranz"][v + "_n_selektionsfalten"]
            print(f"  DD_Toleranz {v} ({n} Sel.-Falten): "
                  f"{t['0.25']:7.2f} / {t['0.50']:7.2f} / {t['1.00']:7.2f}")
        if bot == "t3_supertrend":
            for v in ("V0", "VH", "VT", "VF"):
                t = e["dd_toleranz"][v + "_ohne_2018_nach_21_4"]
                print(f"  DD_Toleranz {v} ohne 2018 (21.4, 7 Falten): "
                      f"{t['0.25']:7.2f} / {t['0.50']:7.2f} / {t['1.00']:7.2f}")
    print(f"\nGeschrieben: {os.path.join(ziel, 'frage_c_rechnung.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
