#!/usr/bin/env python3
"""
TB-73 Schritt 1 - Die Grundlage pruefen, bevor gebaut wird
==============================================================================
Fuer jeden der neun Bots: Gibt es eine Trade-Liste mit Einstiegs- und
Ausstiegszeitpunkt je ausgefuehrter Position? Decken die Kursdateien die
Haltedauern ab? Welche Falten des Plans liegen ueberhaupt im Zeitraum der
Liste?

    trading-env/bin/python3 research/mtm_drawdown/grundlage.py [--json PFAD]

Liest nur: research/tb24_haltedauern/daten/<bot>_positionen.csv und
_meta.json, data/<symbol>_<zeitrahmen>.csv, data/<symbol>_1d.csv,
research/vorregistrierung/ergebnisse/faltenplan_tb72.json. Schreibt nur die
JSON-Datei, die --json nennt (Standard: ergebnisse/grundlage.json neben
diesem Skript). Kein Bot-Modul wird importiert; die Zahlen hier sind
Bestandsaufnahme, keine Messung.

Nichts wird geschaetzt: fehlt etwas, steht es so in der Tabelle, und der Bot
bzw. die Falte fehlt spaeter in der Messung statt mit einer erfundenen Zahl
darin (Auftrag, Schritt 1).
"""

import argparse
import json
import os
import sys
import time

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(_HIER))
DATA_DIR = os.path.join(REPO_ROOT, "data")
TB24_DIR = os.path.join(REPO_ROOT, "research", "tb24_haltedauern", "daten")
FALTENPLAN = os.path.join(REPO_ROOT, "research", "vorregistrierung", "ergebnisse",
                          "faltenplan_tb72.json")
ERGEBNISSE = os.path.join(_HIER, "ergebnisse")

sys.path.insert(0, _HIER)
import mtm_kern  # noqa: E402

# Reihenfolge wie in CLAUDE.md (Krypto zuerst, dann Aktien); der Zeitrahmen je
# Bot steht im TB-24-Meta (`zeitrahmen`) und wird von dort gelesen.
BOTS = (
    "elliott_wave",
    "t3_supertrend",
    "rsi2_crypto",
    "turtle_soup_crypto",
    "volatility_breakout_crypto",
    "elliott_wave_stocks",
    "rsi2_mean_reversion",
    "turtle_soup_stocks",
    "volatility_breakout",
)

PFLICHTSPALTEN = ("symbol", "entry_time", "exit_time", "entry_price", "exit_price",
                  "pnl_pct", "allocation", "capital_after")


def lade_positionen(bot: str):
    """Trade-Liste und Meta eines Bots aus TB-24. (None, None, grund) wenn
    etwas fehlt."""
    pfad = os.path.join(TB24_DIR, f"{bot}_positionen.csv")
    meta_pfad = os.path.join(TB24_DIR, f"{bot}_meta.json")
    if not os.path.exists(pfad):
        return None, None, f"fehlt: {os.path.relpath(pfad, REPO_ROOT)}"
    if not os.path.exists(meta_pfad):
        return None, None, f"fehlt: {os.path.relpath(meta_pfad, REPO_ROOT)}"
    pos = pd.read_csv(pfad, parse_dates=["entry_time", "exit_time"])
    fehlend = [s for s in PFLICHTSPALTEN if s not in pos.columns]
    if fehlend:
        return None, None, f"Spalten fehlen: {fehlend}"
    with open(meta_pfad, encoding="utf-8") as f:
        meta = json.load(f)
    if "ausgefuehrt" in pos.columns and not pos["ausgefuehrt"].astype(bool).all():
        return None, None, "Liste enthaelt nicht ausgefuehrte Zeilen"
    return pos, meta, None


def lade_schlusskurse(symbole, zeitrahmen="1d") -> dict:
    """Schlusskurse je Symbol aus data/<symbol>_<zeitrahmen>.csv, indiziert mit
    open_time. Symbole ohne Datei fehlen im Ergebnis."""
    reihen = {}
    for s in sorted(set(symbole)):
        pfad = os.path.join(DATA_DIR, f"{s}_{zeitrahmen}.csv")
        if not os.path.exists(pfad):
            continue
        df = pd.read_csv(pfad, parse_dates=["open_time"]).dropna(subset=["close"])
        reihen[s] = pd.Series(df["close"].to_numpy(dtype=float),
                              index=pd.DatetimeIndex(df["open_time"]))
    return reihen


def lade_falten(bot: str) -> list:
    with open(FALTENPLAN, encoding="utf-8") as f:
        plan = json.load(f)
    return plan[bot]["falten"]


def einstand_gegen_kerze(pos: pd.DataFrame, kerzen: dict) -> dict:
    """`entry_price` gegen den Schlusskurs der Einstiegskerze im Zeitrahmen
    des Bots - so entstand er im Backtest. Groesste relative Abweichung und
    Anzahl der Positionen ohne Kerze zum Einstiegszeitpunkt."""
    abw = []
    ohne = 0
    for s, t, p in zip(pos["symbol"], pos["entry_time"], pos["entry_price"]):
        r = kerzen.get(s)
        if r is None or t not in r.index:
            ohne += 1
            continue
        c = r.loc[t]
        if isinstance(c, pd.Series):
            c = c.iloc[-1]
        abw.append(abs(p / c - 1.0))
    return {
        "max_rel_abweichung": (float(max(abw)) if abw else None),
        "positionen_ohne_kerze": int(ohne),
        "geprueft": int(len(abw)),
    }


def abdeckung_haltedauern(ereignisse: pd.DataFrame, tages: dict) -> dict:
    """Hat jede Position an jedem Tagesschluss, an dem sie offen ist, einen
    Schlusskurs (eigener oder fortgeschriebener)? Gezaehlt wird ueber
    `mtm_kern.mtm_pfad` selbst - dieselbe Rechnung, die spaeter misst."""
    tage = mtm_kern.tagesraster(tages, von=ereignisse["entry_time"].min().normalize(),
                                bis=ereignisse["exit_time"].max().normalize() + mtm_kern.EIN_TAG)
    kurse, fort = mtm_kern.kurse_auf_raster(tages, tage)
    try:
        pfad = mtm_kern.mtm_pfad(ereignisse, kurse, fort, 10_000.0, 0.0)
    except ValueError as e:
        return {"vollstaendig": False, "fehler": str(e)}
    return {
        "vollstaendig": True,
        "rastertage": int(len(tage)),
        "tage_mit_position": int((pfad["n_offen"] > 0).sum()),
        "fortgeschriebene_kurstage": int(pfad["fortgeschrieben"].sum()),
        "positionstage_gesamt": int(pfad["n_offen"].sum()),
    }


def falten_grundlage(pos: pd.DataFrame, falten: list) -> list:
    """Je Falte: liegt sie im Zeitraum der Liste - ganz, teilweise, gar nicht?
    Massstab ist der erste Einstieg und der letzte Ausstieg der Liste; ein
    Bot ohne Signal in den ersten Monaten seiner Daten faellt damit als
    'teilweise' auf - das ist der vorsichtigere Fehler."""
    erster = pos["entry_time"].min()
    letzter = pos["exit_time"].max()
    aus = []
    for f in falten:
        von = pd.Timestamp(f["von"])
        bis = pd.Timestamp(f["bis_ausschliesslich"])
        if erster >= bis or letzter < von:
            grundlage = "keine"
        elif erster > von:
            grundlage = "teilweise"
        else:
            grundlage = "vollstaendig"
        in_falte = pos[(pos["exit_time"] >= von) & (pos["exit_time"] < bis)]
        offen_ueber_beginn = pos[(pos["entry_time"] < von) & (pos["exit_time"] >= von)]
        aus.append({
            "falte": f["name"], "rolle": f["rolle"],
            "von": str(von.date()), "bis_ausschliesslich": str(bis.date()),
            "grundlage": grundlage,
            "liste_ab": (str(erster.date()) if grundlage == "teilweise" else None),
            "ausstiege_in_falte": int(len(in_falte)),
            "offen_ueber_faltenbeginn": int(len(offen_ueber_beginn)),
        })
    return aus


def pruefe_bot(bot: str) -> dict:
    t0 = time.time()
    pos, meta, grund = lade_positionen(bot)
    if pos is None:
        return {"bot": bot, "trade_liste": False, "grund": grund}

    aus = {
        "bot": bot,
        "trade_liste": True,
        "zeitrahmen": meta.get("zeitrahmen"),
        "anlageklasse": meta.get("anlageklasse"),
        "positionen": int(len(pos)),
        "symbole": int(pos["symbol"].nunique()),
        "erster_einstieg": str(pos["entry_time"].min()),
        "letzter_ausstieg": str(pos["exit_time"].max()),
        "startkapital_meta": meta.get("startkapital"),
        "allocation_pct_meta": meta.get("allocation_pct"),
        "positionslimit_meta": meta.get("max_concurrent_positions"),
        "abgleich_exposure_messung_identisch": (meta.get("abgleich_exposure_messung") or {}).get("identisch"),
    }

    # Kette der Kapitalstaende - schliesst sie, ist die Liste die einer
    # Kapitalsimulation und die Kurvenreihenfolge rekonstruierbar.
    try:
        ereignisse = mtm_kern.ereignisreihenfolge(pos, float(meta["startkapital"]))
        aus["kapitalkette_schliesst"] = True
        aus["endkapital"] = float(ereignisse["capital_after"].iloc[-1])
        aus["ausstiegs_zeitstempel_mit_mehreren_ausstiegen"] = int(
            (ereignisse.groupby("exit_time").size() > 1).sum())
    except ValueError as e:
        aus["kapitalkette_schliesst"] = False
        aus["kapitalkette_fehler"] = str(e)
        ereignisse = None

    # Kursdateien: Zeitrahmen des Bots (fuer den Einstand) und 1d (fuer den
    # Tagesschluss).
    symbole = sorted(pos["symbol"].unique())
    kerzen = lade_schlusskurse(symbole, meta.get("zeitrahmen", "1d"))
    tages = lade_schlusskurse(symbole, "1d")
    aus["symbole_ohne_kerzendatei"] = sorted(set(symbole) - set(kerzen))
    aus["symbole_ohne_1d_datei"] = sorted(set(symbole) - set(tages))
    aus["einstand_gegen_einstiegskerze"] = einstand_gegen_kerze(pos, kerzen)
    if ereignisse is not None and not aus["symbole_ohne_1d_datei"]:
        aus["abdeckung_haltedauern_1d"] = abdeckung_haltedauern(ereignisse, tages)
    else:
        aus["abdeckung_haltedauern_1d"] = {"vollstaendig": False,
                                          "fehler": "Kette oder 1d-Dateien fehlen"}

    aus["falten"] = falten_grundlage(pos, lade_falten(bot))
    aus["laufzeit_s"] = round(time.time() - t0, 1)
    return aus


def tabelle(ergebnisse: list) -> str:
    z = ["| Bot | Liste | Positionen | erster Einstieg | letzter Ausstieg | Kette | Einstand = Kerzenschluss | 1d-Abdeckung | Falten ohne Grundlage | Falten teilweise |",
         "|---|---|---:|---|---|---|---|---|---|---|"]
    for e in ergebnisse:
        if not e.get("trade_liste"):
            z.append(f"| `{e['bot']}` | **fehlt** ({e['grund']}) | | | | | | | | |")
            continue
        eg = e["einstand_gegen_einstiegskerze"]
        ab = e["abdeckung_haltedauern_1d"]
        keine = [f["falte"] for f in e["falten"] if f["grundlage"] == "keine"]
        teil = [f"{f['falte']} (ab {f['liste_ab']})" for f in e["falten"] if f["grundlage"] == "teilweise"]
        einstand = (f"max {eg['max_rel_abweichung']:.1e}, {eg['positionen_ohne_kerze']} ohne Kerze"
                    if eg["max_rel_abweichung"] is not None else "nicht pruefbar")
        abdeckung = (f"ja ({ab['fortgeschriebene_kurstage']} fortgeschrieben von {ab['positionstage_gesamt']} Positionstagen)"
                     if ab.get("vollstaendig") else f"**nein**: {ab.get('fehler')}")
        z.append(f"| `{e['bot']}` | ja | {e['positionen']} | {e['erster_einstieg'][:10]} | "
                 f"{e['letzter_ausstieg'][:10]} | {'schliesst' if e['kapitalkette_schliesst'] else '**offen**'} | "
                 f"{einstand} | {abdeckung} | {', '.join(keine) or '—'} | {', '.join(teil) or '—'} |")
    return "\n".join(z)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(ERGEBNISSE, "grundlage.json"))
    ap.add_argument("--bots", nargs="*", default=list(BOTS))
    a = ap.parse_args(argv)

    ergebnisse = [pruefe_bot(b) for b in a.bots]
    os.makedirs(os.path.dirname(a.json), exist_ok=True)
    with open(a.json, "w", encoding="utf-8") as f:
        json.dump(ergebnisse, f, indent=1, ensure_ascii=False, default=str)
    print(tabelle(ergebnisse))
    print()
    for e in ergebnisse:
        if not e.get("trade_liste"):
            continue
        print(f"{e['bot']}: Falten -", ", ".join(
            f"{f['falte']}={f['grundlage'][0].upper()}({f['ausstiege_in_falte']}/{f['offen_ueber_faltenbeginn']})"
            for f in e["falten"]), f"- {e['laufzeit_s']} s")
    print("\n(Klammer: Ausstiege in der Falte / Positionen, die ueber den Faltenbeginn offen sind; "
          "V = vollstaendig, T = teilweise, K = keine Grundlage)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
