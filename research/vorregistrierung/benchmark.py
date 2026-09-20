#!/usr/bin/env python3
"""
TB-30a - Vorab-Berechnung: Benchmark-Drawdowns je Falte, DD_Toleranz je Bot
==============================================================================
Die Drawdown-Bedingung der Vorregistrierung lautet (Festlegung 4):

    erlaubt(f) = min(1,25 x DD_Benchmark(f), DD_Toleranz)

Beide Werte sind negativ; `min` ist der TIEFERE und damit die grosszuegigere
Grenze. Ein Parametersatz besteht eine Falte, wenn sein Kapital-Drawdown in
dieser Falte nicht tiefer liegt als `erlaubt(f)`.

WAS HIER VORAB BERECHNET WIRD - UND WAS NICHT
------------------------------------------------------------------------------
Der Benchmark ist eine **statische Position** in Hoehe der mittleren Exposure
im gleichgewichteten point-in-time-Universum. Seine Exposure ist damit erst im
Lauf bekannt: es gilt die mittlere Exposure des JEWEILIGEN Parametersatzes in
der JEWEILIGEN Falte, nicht die heute gemessene des Bots. Vorab berechenbar
ist deshalb nicht EINE Zahl je Falte, sondern die **Funktion**:

    DD_Benchmark(f, e)   fuer e = 1 %, 2 %, ..., 100 %

Diese Tabelle steht auf der Sperrliste. Im Lauf wird darin nachgeschlagen -
linear zwischen den beiden benachbarten Stuetzstellen interpoliert -, nichts
neu gerechnet. So verweist keine Zahl des Registers auf den Live-Zustand, und
die satzweise Verfeinerung geschieht trotzdem im Lauf.

DD_TOLERANZ - WARUM SIE EBENFALLS EIN EXPOSURE-ARGUMENT TRAEGT
------------------------------------------------------------------------------
Festlegung 5 sagt: DD_Toleranz ist der **Median der Benchmark-Drawdowns ueber
alle Selektionsfalten, je Bot**. Da der Benchmark-Drawdown nach Festlegung 4
selbst von der Exposure abhaengt, erbt der Median dieses Argument:

    DD_Toleranz(e) = Median ueber die Selektionsfalten von DD_Benchmark(f, e)

Das ist keine zusaetzliche Entscheidung, sondern die einzige Lesart, die mit
Festlegung 4 zusammenpasst - und sie erfuellt genau das, was Festlegung 5
bezweckt: "Je Bot, zwingend - ein Bot mit 21 % Zeit im Markt liegt auf einer
anderen Skala als einer mit 100 %." Die Skala kommt jetzt aus der Exposure
selbst statt aus einem heute gemessenen Live-Zustand, und die ruhige Falte
wird trotzdem gerettet:

    ruhige Falte: DD_Benchmark = -2 %, 1,25 x = -2,5 %, DD_Toleranz = -8 %
                  -> erlaubt = -8 %, ein Satz mit -4 % besteht
    Krisenfalte:  DD_Benchmark = -35 %, 1,25 x = -43,75 %, DD_Toleranz = -8 %
                  -> erlaubt = -43,75 %, die relative Grenze bindet

DAS UNIVERSUM
------------------------------------------------------------------------------
Gleichgewichtet, taeglich, **point-in-time**: ein Symbol geht in eine Falte
nur ein, wenn seine Kursdaten mindestens `MINDESTTRAINING_JAHRE` vor dem
Faltenbeginn einsetzen. Gemittelt werden Tagesrenditen, nicht Kurse - die
Summe roher Schlusskurse ist genau der Fehler, der beim APH-Vorfall die
gesamte Portfoliosumme zu NaN gemacht hat (Protokoll 3.3).
"""

import argparse
import json
import os
import sys
from datetime import date

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB30A_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))
DATA_DIR = os.path.join(BASE_DIR, "data")

import faltenplan as fp  # noqa: E402
import registerdaten as rd  # noqa: E402

# Stuetzstellen der Exposure-Achse: 1 % bis 100 % in Schritten von 1 %.
# Feiner waere Genauigkeit ohne Aussage - die Kapitalpfade selbst sind auf
# zwei Nachkommastellen ausgewiesen.
EXPOSURE_STUFEN = [round(0.01 * k, 2) for k in range(1, 101)]


def universumsdatei(markt: str) -> str:
    return os.path.join(BASE_DIR, rd.UNIVERSUM[markt])


def symbole(markt: str) -> list:
    with open(universumsdatei(markt), encoding="utf-8") as f:
        s = [z.strip() for z in f if z.strip()]
    return [x for x in s if x not in {"XAUTUSDT", "PAXGUSDT"}]


def tagesschluss(markt: str) -> dict:
    """Schlusskurs-Reihen je Symbol, Tagesaufloesung."""
    reihen = {}
    for s in sorted(symbole(markt)):
        pfad = os.path.join(DATA_DIR, f"{s}_1d.csv")
        if not os.path.exists(pfad):
            continue
        df = pd.read_csv(pfad, parse_dates=["open_time"])
        df = df.dropna(subset=["close"])
        if df.empty:
            continue
        reihen[s] = pd.Series(df["close"].to_numpy(dtype=float),
                              index=pd.DatetimeIndex(df["open_time"]))
    return reihen


def point_in_time(reihen: dict, faltenbeginn: date, jahre: int) -> dict:
    """Nur Symbole, deren Kursdaten `jahre` Jahre vor Faltenbeginn einsetzen."""
    schranke = pd.Timestamp(faltenbeginn) - pd.DateOffset(years=jahre)
    return {s: r for s, r in reihen.items() if r.index[0] <= schranke}


def bh_tagesrenditen(reihen: dict) -> pd.Series:
    """Gleichgewichteter Buy-and-Hold: Mittel der Tagesrenditen.

    Zeichengleich zu research/exposure_messung/exposure_kern.py - dieselbe
    Rechnung, damit die Benchmark-Definition im Repo nicht zweimal
    auseinanderlaufen kann.
    """
    rahmen = pd.DataFrame(reihen).sort_index()
    return rahmen.pct_change().mean(axis=1, skipna=True).dropna()


def drawdown_bei_exposure(renditen: pd.Series, exposure: float) -> float:
    """Max Drawdown einer statischen Position der Groesse `exposure`.

    Die Position ist taeglich gleichgewichtet; das Kapital waechst mit
    `1 + exposure * r`. Gerundet wird auf zwei Nachkommastellen, wie ueberall
    in der Messkette (shared/messkette.py).
    """
    if renditen.empty:
        return 0.0
    kapital = np.cumprod(1.0 + exposure * renditen.to_numpy(dtype=float))
    hoch = np.maximum.accumulate(np.concatenate(([1.0], kapital)))[1:]
    return round(float(np.min(kapital / hoch - 1.0) * 100.0), 2)


def nachschlagen(tabelle: dict, exposure: float) -> float:
    """Der Benchmark-Drawdown bei beliebiger Exposure - lineare Interpolation.

    Diese Funktion ist die EINZIGE Art, wie im Lauf auf die Tabelle
    zugegriffen wird. Sie steht hier, damit die Interpolationsregel mit der
    Tabelle zusammen auf der Sperrliste steht.
    """
    e = max(0.0, min(1.0, float(exposure)))
    if e <= 0:
        return 0.0
    stufen = sorted(float(k) for k in tabelle)
    if e <= stufen[0]:
        return float(tabelle[_schluessel(stufen[0])]) * e / stufen[0]
    for a, b in zip(stufen, stufen[1:]):
        if a <= e <= b:
            ya = float(tabelle[_schluessel(a)])
            yb = float(tabelle[_schluessel(b)])
            if b == a:
                return ya
            return ya + (yb - ya) * (e - a) / (b - a)
    return float(tabelle[_schluessel(stufen[-1])])


def _schluessel(e: float) -> str:
    return f"{e:.2f}"


def je_bot(mess: dict) -> dict:
    plan = fp.faltenplan(mess)
    kurse = {markt: tagesschluss(markt) for markt in ("aktien", "krypto")}
    aus = {}
    for bot, eig in rd.BOTS.items():
        p = plan[bot]
        eintrag = {
            "markt": eig["markt"],
            "status": p["status"],
            "universumsdatei": rd.UNIVERSUM[eig["markt"]],
            "falten": {},
            "dd_toleranz": {},
        }
        sel = []
        for f in p["falten"]:
            von = pd.Timestamp(f["von"])
            bis = pd.Timestamp(f["bis_ausschliesslich"])
            reihen = point_in_time(kurse[eig["markt"]],
                                   date.fromisoformat(f["von"]),
                                   rd.MINDESTTRAINING_JAHRE)
            renditen = bh_tagesrenditen(reihen)
            fenster = renditen[(renditen.index >= von) & (renditen.index < bis)]
            tab = {_schluessel(e): drawdown_bei_exposure(fenster, e)
                   for e in EXPOSURE_STUFEN}
            eintrag["falten"][f["name"]] = {
                "rolle": f["rolle"],
                "von": f["von"],
                "bis_ausschliesslich": f["bis_ausschliesslich"],
                "symbole_point_in_time": len(reihen),
                "handelstage": int(len(fenster)),
                "dd_benchmark": tab,
            }
            if f["rolle"] == "selektion":
                sel.append(tab)

        # DD_Toleranz: Median ueber die SELEKTIONSFALTEN, je Exposure-Stufe.
        for e in EXPOSURE_STUFEN:
            k = _schluessel(e)
            werte = [t[k] for t in sel]
            eintrag["dd_toleranz"][k] = round(float(np.median(werte)), 2) if werte else 0.0
        aus[bot] = eintrag
    return aus


def erlaubt(dd_benchmark: float, dd_toleranz: float) -> float:
    """Festlegung 4 - die Grenze selbst, an einer Stelle.

    Beide Werte sind negativ (oder 0). `min` liefert den TIEFEREN und damit
    die grosszuegigere Grenze.
    """
    return min(rd.DD_RELATIVER_FAKTOR * dd_benchmark, dd_toleranz)


def main(argv=None):
    # --ziel (TB-61): wohin die Tabelle geschrieben wird. Ohne Angabe die
    # registrierte Datei - unveraendertes Verhalten. Mit Angabe eine Datei
    # DANEBEN: Register 21.9 haelt benchmark_drawdowns.json bis zum Amendment
    # byteweise fest, und ohne diesen Schalter ueberschriebe jeder Lauf sie.
    zerleger = argparse.ArgumentParser(
        description="Benchmark-Drawdowns je Falte, DD_Toleranz je Bot.")
    zerleger.add_argument(
        "--ziel", default=os.path.join(_HIER, "ergebnisse",
                                       "benchmark_drawdowns.json"),
        help="Ausgabedatei (Standard: ergebnisse/benchmark_drawdowns.json)")
    ziel = zerleger.parse_args(argv).ziel

    mess = rd._mess()
    tabellen = je_bot(mess)
    with open(ziel, "w", encoding="utf-8") as f:
        json.dump(tabellen, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    print(__doc__.strip().split("\n")[0])
    for bot, e in tabellen.items():
        print(f"\n{bot}  ({e['markt']})")
        print(f"    {'Falte':12s} {'Rolle':12s} {'Titel':>6s} {'Tage':>5s} "
              f"{'DD@25%':>8s} {'DD@50%':>8s} {'DD@100%':>8s}")
        for name, f in e["falten"].items():
            print(f"    {name:12s} {f['rolle']:12s} "
                  f"{f['symbole_point_in_time']:6d} {f['handelstage']:5d} "
                  f"{f['dd_benchmark']['0.25']:7.2f}% "
                  f"{f['dd_benchmark']['0.50']:7.2f}% "
                  f"{f['dd_benchmark']['1.00']:7.2f}%")
        print(f"    {'DD_Toleranz':12s} {'':12s} {'':6s} {'':5s} "
              f"{e['dd_toleranz']['0.25']:7.2f}% "
              f"{e['dd_toleranz']['0.50']:7.2f}% "
              f"{e['dd_toleranz']['1.00']:7.2f}%")
    print(f"\nGeschrieben: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
