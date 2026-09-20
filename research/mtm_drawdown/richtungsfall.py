#!/usr/bin/env python3
"""
TB-73 - Die Richtungsprobe, Fall fuer Fall: WARUM ist M hier flacher als E?
==============================================================================
    trading-env/bin/python3 research/mtm_drawdown/richtungsfall.py

Der Auftrag sagt: M darf nie flacher sein als E; wo doch, ist der Pfad
falsch - melden, nicht glaetten. Probe 3 (test_mtm_kern.py) zeigt, dass der
Satz kein Satz der Rechnung ist: ein unrealisierter Gewinn in einer anderen
offenen Position hebt Hoechststand und Tiefpunkt von M zugleich. Dieses
Skript nimmt jeden gemessenen Fall aus ergebnisse/<bot>.json und legt die
Zerlegung daneben, damit niemand raten muss:

  * Tag und Stand des E_tag-Tiefpunkts der Falte (Buchwert) und des
    M-Tiefpunkts; die jeweiligen Hoechststaende davor.
  * Am E_tag-Tiefpunkt: welche Positionen offen sind, wie viel unrealisierter
    Gewinn/Verlust in ihnen steckt - das ist der Betrag, um den M dort ueber
    oder unter E liegt.
  * Positionen, die VOR der Falte eingestiegen und IN der Falte ausgestiegen
    sind, mit ihrem Ergebnis: E bucht ihren ganzen Verlust in die Falte, M nur
    den Teil ab Faltenbeginn (der Rest steckt schon in der Basis von M).

Liest nur; schreibt ergebnisse/richtungsfaelle.md. Kein Bot-Modul wird
importiert (die Kosten je Seite stehen im <bot>.json der Messung).
"""

import json
import os
import sys

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, _HIER)
sys.path.insert(0, os.path.join(REPO_ROOT, "shared"))

import mtm_kern     # noqa: E402
import grundlage    # noqa: E402
from messkette import max_drawdown_ungerundet  # noqa: E402


def f2(x):
    return f"{x:,.2f}".replace(",", " ").replace(".", ",")


def tief_und_hoch(reihe: pd.Series, basis: float):
    """Tag des Tiefpunkts (groesster Abstand vom laufenden Hoechststand), der
    Stand dort, der Hoechststand davor und sein Tag."""
    voll = pd.concat([pd.Series([basis], index=[pd.NaT]), reihe])
    hoch = voll.cummax()
    dd = (voll - hoch) / hoch
    i = int(np.argmin(dd.to_numpy()))
    tag_tief = voll.index[i]
    hoch_wert = float(hoch.iloc[i])
    j = int(np.argmax(voll.to_numpy()[:i + 1]))
    return tag_tief, float(voll.iloc[i]), hoch_wert, voll.index[j], float(dd.iloc[i] * 100)


def fall(bot: str, d: dict, z: dict, pos: pd.DataFrame, pfad: pd.DataFrame, tages: dict) -> list:
    von, bis = pd.Timestamp(z["von"]), pd.Timestamp(z["bis_ausschliesslich"])
    kosten_seite = float(d["kosten"]["je_seite_pct"])
    startkapital = float(d["startkapital"])
    ereignisse = mtm_kern.ereignisreihenfolge(pos, startkapital)
    in_falte = pfad[(pfad.index >= von) & (pfad.index < bis)]
    davor = pfad[pfad.index < von]
    basis_buch = float(davor["buch"].iloc[-1]) if len(davor) else startkapital
    basis_mtm = float(davor["mtm"].iloc[-1]) if len(davor) else startkapital

    t_e, w_e, h_e, th_e, dd_e = tief_und_hoch(in_falte["buch"], basis_buch)
    t_m, w_m, h_m, th_m, dd_m = tief_und_hoch(in_falte["mtm"], basis_mtm)

    aus = [f"### `{bot}` — Falte {z['falte']} ({z['rolle']}): E {f2(z['E'])} %, E_tag {f2(z['E_tag'])} %, "
           f"M {f2(z['M'])} % — M um {f2(z['M_minus_E_pp'])} pp flacher", ""]
    aus.append(f"- Basis am Faltenbeginn: Buch {f2(basis_buch)}, MtM {f2(basis_mtm)} "
               f"(unrealisiert am {str(davor.index[-1].date()) if len(davor) else '—'}: "
               f"{f2(basis_mtm - basis_buch)}; offen: {z['offen_am_faltenbeginn']})")
    aus.append(f"- **E_tag**: Hoch {f2(h_e)} am {str(th_e.date()) if pd.notna(th_e) else 'Faltenbeginn'}, "
               f"Tief {f2(w_e)} am {str(t_e.date()) if pd.notna(t_e) else 'Faltenbeginn'} → {f2(dd_e)} %")
    aus.append(f"- **M**: Hoch {f2(h_m)} am {str(th_m.date()) if pd.notna(th_m) else 'Faltenbeginn'}, "
               f"Tief {f2(w_m)} am {str(t_m.date()) if pd.notna(t_m) else 'Faltenbeginn'} → {f2(dd_m)} %")

    # Am E_tag-Tiefpunkt: offene Positionen und ihr unrealisierter Stand
    if pd.notna(t_e):
        zeile = pfad.loc[t_e]
        aus.append(f"- Am E_tag-Tief ({t_e.date()}): Buch {f2(zeile['buch'])}, MtM {f2(zeile['mtm'])}, "
                   f"unrealisiert **{f2(zeile['unrealisiert'])}** in {int(zeile['n_offen'])} offenen Positionen "
                   f"— M steht dort um {f2(zeile['mtm'] / h_m * 100 - 100)} % unter seinem Hoch, "
                   f"E_tag um {f2(dd_e)} %")
        tagesende = t_e + mtm_kern.EIN_TAG
        offen = ereignisse[(ereignisse["entry_time"] < tagesende) & (ereignisse["exit_time"] >= tagesende)]
        if len(offen):
            aus.append("")
            aus.append("  | Symbol | Einstieg | Ausstieg | Allokation | Schluss am Tief / Einstand | unrealisiert | realisiert später (pnl_pct) |")
            aus.append("  |---|---|---|---:|---:|---:|---:|")
            for _, p in offen.sort_values("entry_time").iterrows():
                r = tages[p["symbol"]]
                r = r[pd.DatetimeIndex(r.index).normalize() <= t_e]
                schluss = float(r.iloc[-1])
                unreal = p["allocation"] * (schluss / p["entry_price"] - 1 - kosten_seite / 100)
                aus.append(f"  | {p['symbol']} | {str(p['entry_time'])[:10]} | {str(p['exit_time'])[:10]} | "
                           f"{f2(p['allocation'])} | {schluss / p['entry_price']:.4f} | {f2(unreal)} | {p['pnl_pct']:+.2f} % |")
    # Positionen ueber den Faltenbeginn
    ueber = ereignisse[(ereignisse["entry_time"] < von) & (ereignisse["exit_time"] >= von) & (ereignisse["exit_time"] < bis)]
    if len(ueber):
        aus.append("")
        aus.append(f"- Über den Faltenbeginn offene, in der Falte geschlossene Positionen ({len(ueber)}): "
                   + "; ".join(f"{p['symbol']} {str(p['entry_time'])[:10]}→{str(p['exit_time'])[:10]} {p['pnl_pct']:+.2f} %"
                               for _, p in ueber.iterrows())
                   + f". Ihr realisiertes Ergebnis zusammen: {f2(float((ueber['allocation'] * ueber['pnl_pct'] / 100).sum()))}; "
                   f"davon steckte am Faltenbeginn schon {f2(basis_mtm - basis_buch)} unrealisiert in der M-Basis")
    aus.append("")
    return aus


def main():
    zeilen = ["# TB-73 — Richtungsprobe, Fall für Fall (erzeugt von `richtungsfall.py`)", "",
              "Jeder Fall, in dem M flacher ist als E, mit der Zerlegung: wo liegen Hoch und Tief beider Reihen, "
              "wie viel unrealisierter Gewinn steckt am E-Tief in offenen Positionen, welche Positionen tragen "
              "Verluste aus der Vorfalte in die Falte. Mechanismus wie Probe 3 in `test_mtm_kern.py`.", ""]
    n = 0
    for bot in grundlage.BOTS:
        pfad_json = os.path.join(grundlage.ERGEBNISSE, f"{bot}.json")
        if not os.path.exists(pfad_json):
            continue
        with open(pfad_json, encoding="utf-8") as f:
            d = json.load(f)
        faelle = [z for z in d["falten"] if z.get("M_flacher_als_E")]
        if not faelle:
            continue
        pos, meta, _ = grundlage.lade_positionen(bot)
        pfad = pd.read_csv(os.path.join(grundlage.ERGEBNISSE, f"{bot}_tagespfad.csv"),
                           parse_dates=["tag"], index_col="tag")
        tages = grundlage.lade_schlusskurse(pos["symbol"].unique(), "1d")
        for z in faelle:
            n += 1
            zeilen += fall(bot, d, z, pos, pfad, tages)
    if n == 0:
        zeilen.append("*Kein Fall.*")
    ziel = os.path.join(grundlage.ERGEBNISSE, "richtungsfaelle.md")
    with open(ziel, "w", encoding="utf-8") as f:
        f.write("\n".join(zeilen) + "\n")
    print("\n".join(zeilen))
    print(f"\n{n} Faelle -> {os.path.relpath(ziel)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
