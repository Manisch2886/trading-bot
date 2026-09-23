#!/usr/bin/env python3
"""
TB-30a - Das eingefrorene Auswertungsskript
==============================================================================
Dieses Programm liest die ROHERGEBNISSE eines Selektionslaufs und gibt aus:

  * den Plateau-Gewinner je Bot,
  * seine Markierungen (Spitze, Kante),
  * die Bleibt-Geht-Liste nach den Abbruchkriterien (a) bis (d),
  * die drei DSR-Werte (bei N_eff, bei N_nominal, bei 2 x N_nominal),
  * alle Kennzahlen der Beurteilung, die unangenehmen eingeschlossen,
  * und zuletzt die Bestaetigungsperiode.

**Es gibt keine Stelle, an der ein Mensch entscheidet.** Wo dieses Programm
eine Wahl offen liesse, waere die Vorregistrierung unvollstaendig - das ist
der Test, den es zu bestehen hatte, und es ist der Grund, warum es VOR dem
Lauf geschrieben und eingefroren wurde.

Es laeuft, bevor irgendein Ergebnis existiert: `beispieldaten.py` erzeugt
Rohergebnisse mit frei erfundenen Werten, gegen die `test_vorregistrierung.py`
jede Regel einzeln prueft.

DIE REIHENFOLGE - SIE IST TEIL DER FESTLEGUNG
------------------------------------------------------------------------------
  1. Einlesen und pruefen. Fehlt eine Falte, eine Zelle oder eine Tagesreihe,
     BRICHT das Programm ab. Es fuellt nichts auf, es ueberspringt nichts.
  2. Selektionsstatistik je Zelle (Median des Netto-Sharpe ueber die
     Selektionsfalten; Falten ohne Trade zaehlen mit Sharpe 0).
  3. Zulaessigkeit je Zelle ueber die Drawdown-Bedingung.
  4. Plateau-Mittel, Gewinner, Markierungen.
  5. Abbruchkriterien (a) bis (d), einschliesslich Beta-Bereinigung.
  6. DSR (Bericht, nicht Tor) und N-Buchfuehrung.
  7. ERST DANACH die Bestaetigungsperiode.
  8. Bericht.

DIE ROHERGEBNISSE - DER VERTRAG
------------------------------------------------------------------------------
    <wurzel>/<bot>/zellen.csv
        zelle_id, <je Rasterachse eine Spalte>, falte, rolle, n_trades,
        netto_sharpe, netto_rendite_pct, kapital_drawdown_pct,
        mittlere_exposure
        -> genau eine Zeile je (Zelle x Falte), fuer ALLE Falten des
           Faltenplans, Bestaetigungsperiode eingeschlossen.

    <wurzel>/<bot>/tagesreihen/<zelle_id>.csv
        datum, netto_rendite, exposure
        -> Tagesreihe ueber alle Falten. Verlangt wird sie fuer jede
           ZULAESSIGE Zelle; gelesen wird sie nur fuer die Zellen, die das
           Programm braucht (Gewinner, bester Nicht-Spitzen-Punkt).

    <wurzel>/<bot>/herkunft.json
        Commit-Hash, Datenstand-Hash, Register-Hash - siehe herkunft.py.

    <wurzel>/benchmark_tagesreihen/<markt>.csv
        datum, netto_rendite
        -> das gleichgewichtete point-in-time-Universum, taeglich. Grundlage
           der Beta-Bereinigung und des Zufalls-Timing-Tests.

ZWEI DEFINITIONEN, DIE SONST SCHWEIGEND AUSEINANDERLAUFEN
------------------------------------------------------------------------------
**Nachbarschaft und Plateau-Mittel.** Die Nachbarschaft N(x) sind die
vorhandenen Rasterpunkte, die sich von x in genau EINER Achse um genau EINE
Stufe unterscheiden. Das Plateau-Mittel ist der Mittelwert der
Selektionsstatistik ueber {x} UND N(x) - der Punkt zaehlt mit, weil er der
Punkt ist, der gespielt wird: ein Punkt mit hervorragenden Nachbarn und
katastrophalem eigenem Wert darf nicht gewinnen.

**Die Spitze.** Der Spitzentest vergleicht x mit dem Mittel ueber N(x) OHNE
x: die Frage ist, ob der Punkt aus seiner Umgebung herausragt, und ein Punkt,
der in seiner eigenen Vergleichsgrundlage steckt, daempft genau das, was
gemessen werden soll. Formal ist x eine Spitze, wenn

        S(x) - M > 0,5 * |M|        mit M = Mittel ueber N(x) ohne x

Fuer M > 0 ist das woertlich "mehr als 50 % ueber dem Nachbarschaftsmittel".
Fuer M <= 0 ist es dieselbe Bedingung, weiterhin monoton und definiert - die
Formel hat keinen undefinierten Fall. Ist N(x) leer, ist x keine Spitze: aus
nichts kann nichts herausragen.
"""

import argparse
import json
import math
import os
import sys
from itertools import product

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB30A_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))

# Die Tabelle der Benchmark-Drawdowns, die der Lauf liest - Sperrlistenpunkt 4
# in Form (ii), vollzogen in TB-92 (Register 39, Fable 23c/23d). Eine
# Konstante, KEIN Schalter (Abschnitt 12); `registerbericht.py` und
# `test_vorregistrierung.py` lesen dieselbe. `ergebnisse/benchmark_drawdowns.json`
# bleibt als registrierter historischer Stand liegen und wird nicht gelesen.
BENCHMARK_TABELLE = os.path.join(_HIER, "ergebnisse",
                                 "benchmark_drawdowns_2026-09-23_nach_wegA.json")

import benchmark as bm  # noqa: E402
import faltenplan as fp  # noqa: E402
import kennzahlen as kz  # noqa: E402
import registerdaten as rd  # noqa: E402

PFLICHTSPALTEN = ["zelle_id", "falte", "rolle", "n_trades", "netto_sharpe",
                  "netto_rendite_pct", "kapital_drawdown_pct", "mittlere_exposure"]


class Abbruch(SystemExit):
    """Ein Vertragsbruch in den Rohergebnissen. Nie eine stille Annahme."""


# ---------------------------------------------------------------------------
# 1. Einlesen und pruefen
# ---------------------------------------------------------------------------
def perioden_je_jahr(bot: str) -> int:
    return (rd.HANDELSTAGE_JE_JAHR if rd.BOTS[bot]["markt"] == "aktien" else 365)


def gitterachsen(bot: str, mess: dict) -> dict:
    return rd.raster(mess)[bot]


def zelle_id(achsen: dict, werte: dict) -> str:
    """Der kanonische Name einer Rasterzelle - Achsen alphabetisch."""
    return "|".join(f"{a}={_wert_text(werte[a])}" for a in sorted(achsen))


def _wert_text(w):
    if w is None:
        return "None"
    if isinstance(w, float):
        return f"{w:g}"
    return str(w)


def alle_zellen(achsen: dict, bedingung=None):
    """Alle vorhandenen Rasterpunkte als (Indextupel, Werte-Dict).

    Zellen, in denen die Strategie nicht definiert ist, EXISTIEREN NICHT:
    sie koennen weder gewinnen noch in ein Nachbarschaftsmittel eingehen.
    """
    namen = sorted(achsen)
    for idx in product(*[range(len(achsen[n])) for n in namen]):
        werte = {n: achsen[n][i] for n, i in zip(namen, idx)}
        if bedingung and not bedingung(werte):
            continue
        yield idx, werte


def bedingung_fuer(bot: str):
    definition = rd.raster_definition()[bot]
    if definition.get("_bedingung") == "t3_fast_length < t3_slow_length":
        return lambda w: w["t3_fast_length"] < w["t3_slow_length"]
    return None


def lies_zellen(bot: str, wurzel: str, mess: dict, plan: dict) -> pd.DataFrame:
    pfad = os.path.join(wurzel, bot, "zellen.csv")
    if not os.path.exists(pfad):
        raise Abbruch(f"{bot}: {pfad} fehlt - der Lauf ist unvollstaendig.")
    # Faltennamen sind Namen, keine Zahlen: "2019" darf nicht als 2019
    # eingelesen werden, sonst passt es nie zum Faltenplan.
    df = pd.read_csv(pfad, dtype={"falte": str, "zelle_id": str, "rolle": str})
    fehlend = [s for s in PFLICHTSPALTEN if s not in df.columns]
    if fehlend:
        raise Abbruch(f"{bot}: Spalten fehlen in zellen.csv: {fehlend}")

    achsen = gitterachsen(bot, mess)
    erwartet = {zelle_id(achsen, w) for _, w in
                alle_zellen(achsen, bedingung_fuer(bot))}
    gefunden = set(df["zelle_id"])
    if gefunden - erwartet:
        raise Abbruch(f"{bot}: {len(gefunden - erwartet)} Zelle(n) in den "
                      f"Rohergebnissen liegen nicht im Raster, z. B. "
                      f"{sorted(gefunden - erwartet)[0]}")
    if erwartet - gefunden:
        raise Abbruch(f"{bot}: {len(erwartet - gefunden)} Rasterzelle(n) fehlen "
                      f"in den Rohergebnissen, z. B. "
                      f"{sorted(erwartet - gefunden)[0]}")

    falten = [f["name"] for f in plan[bot]["falten"]]
    for name, gruppe in df.groupby("zelle_id"):
        if sorted(gruppe["falte"]) != sorted(falten):
            raise Abbruch(f"{bot}/{name}: Falten stimmen nicht mit dem "
                          f"Faltenplan ueberein ({sorted(gruppe['falte'])} "
                          f"statt {sorted(falten)})")

    # Festlegung: Falten OHNE TRADE zaehlen mit Sharpe 0 - gesetzt, nicht
    # geglaubt. Was in der Datei steht, ist dort ohne Bedeutung.
    df["netto_sharpe"] = np.where(df["n_trades"].to_numpy() == 0, 0.0,
                                  df["netto_sharpe"].to_numpy(dtype=float))
    if df["netto_sharpe"].isna().any():
        raise Abbruch(f"{bot}: netto_sharpe enthaelt Leerwerte in Falten MIT "
                      f"Trades - das waere eine stille Null.")
    return df


def lies_tagesreihe(bot: str, wurzel: str, zid: str) -> pd.DataFrame:
    pfad = os.path.join(wurzel, bot, "tagesreihen", f"{_dateiname(zid)}.csv")
    if not os.path.exists(pfad):
        raise Abbruch(f"{bot}: Tagesreihe fuer '{zid}' fehlt ({pfad}). Der "
                      f"Vertrag verlangt sie fuer jede zulaessige Zelle.")
    df = pd.read_csv(pfad, parse_dates=["datum"])
    for s in ("netto_rendite", "exposure"):
        if s not in df.columns:
            raise Abbruch(f"{bot}/{zid}: Spalte '{s}' fehlt in der Tagesreihe")
    return df.sort_values("datum").reset_index(drop=True)


def _dateiname(zid: str) -> str:
    """Zellenname als Dateiname - '|' und '=' sind nicht ueberall erlaubt."""
    return zid.replace("|", "~").replace("=", "-")


def lies_benchmark(wurzel: str, markt: str) -> pd.DataFrame:
    pfad = os.path.join(wurzel, "benchmark_tagesreihen", f"{markt}.csv")
    if not os.path.exists(pfad):
        raise Abbruch(f"Benchmark-Tagesreihe fuer {markt} fehlt ({pfad}). Ohne "
                      f"sie ist Abbruchkriterium (c) nicht entscheidbar.")
    df = pd.read_csv(pfad, parse_dates=["datum"])
    if "netto_rendite" not in df.columns:
        raise Abbruch(f"Benchmark {markt}: Spalte 'netto_rendite' fehlt")
    return df.sort_values("datum").reset_index(drop=True)


# ---------------------------------------------------------------------------
# 2. bis 4. Selektionsstatistik, Zulaessigkeit, Plateau
# ---------------------------------------------------------------------------
def selektionsstatistik(df: pd.DataFrame, selektionsfalten: list) -> pd.Series:
    """Festlegung 2: Median des Netto-Sharpe ueber die Selektionsfalten."""
    teil = df[df["falte"].isin(selektionsfalten)]
    return teil.groupby("zelle_id")["netto_sharpe"].median()


def zulaessigkeit(bot: str, df: pd.DataFrame, selektionsfalten: list,
                  tabellen: dict) -> pd.DataFrame:
    """Festlegung 4 und 5: die Drawdown-Bedingung, Falte fuer Falte."""
    eintrag = tabellen[bot]
    zeilen = []
    for _, z in df[df["falte"].isin(selektionsfalten)].iterrows():
        falte = eintrag["falten"][z["falte"]]
        e = float(z["mittlere_exposure"])
        dd_bench = bm.nachschlagen(falte["dd_benchmark"], e)
        dd_tol = bm.nachschlagen(eintrag["dd_toleranz"], e)
        grenze = bm.erlaubt(dd_bench, dd_tol)
        zeilen.append({
            "zelle_id": z["zelle_id"], "falte": z["falte"],
            "exposure": e, "dd_benchmark": dd_bench, "dd_toleranz": dd_tol,
            "erlaubt": grenze,
            "dd_satz": float(z["kapital_drawdown_pct"]),
            "bestanden": float(z["kapital_drawdown_pct"]) >= grenze,
            "bindet": (rd.DD_RELATIVER_FAKTOR * dd_bench) <= dd_tol,
        })
    return pd.DataFrame(zeilen)


def nachbarschaften(achsen: dict, bedingung) -> dict:
    """Zu jedem vorhandenen Rasterpunkt die vorhandenen Nachbarn."""
    namen = sorted(achsen)
    vorhanden = {idx: werte for idx, werte in alle_zellen(achsen, bedingung)}
    nachbarn = {}
    for idx in vorhanden:
        liste = []
        for achse in range(len(namen)):
            for schritt in (-1, 1):
                nidx = list(idx)
                nidx[achse] += schritt
                nidx = tuple(nidx)
                if 0 <= nidx[achse] < len(achsen[namen[achse]]) and nidx in vorhanden:
                    liste.append(nidx)
        nachbarn[idx] = liste
    return vorhanden, nachbarn


def plateau(achsen: dict, bedingung, statistik: pd.Series) -> pd.DataFrame:
    vorhanden, nachbarn = nachbarschaften(achsen, bedingung)
    zeilen = []
    for idx, werte in vorhanden.items():
        zid = zelle_id(achsen, werte)
        s = float(statistik.get(zid, 0.0))
        nachbar_ids = [zelle_id(achsen, vorhanden[n]) for n in nachbarn[idx]]
        nachbar_werte = [float(statistik.get(n, 0.0)) for n in nachbar_ids]
        mittel_ohne = float(np.mean(nachbar_werte)) if nachbar_werte else float("nan")
        zeilen.append({
            "zelle_id": zid,
            "statistik": s,
            "n_nachbarn": len(nachbar_ids),
            "plateau_mittel": float(np.mean([s] + nachbar_werte)),
            "nachbarmittel_ohne": mittel_ohne,
            "spitze": bool(nachbar_werte) and (s - mittel_ohne
                                               > rd.SPITZEN_SCHWELLE * abs(mittel_ohne)),
            "kante": any(i in (0, len(achsen[a]) - 1)
                         for a, i in zip(sorted(achsen), idx)),
        })
    return pd.DataFrame(zeilen)


def gewinner(tafel: pd.DataFrame) -> dict:
    """Der Gewinner: hoechstes Plateau-Mittel.

    Gleichstand wird reproduzierbar aufgeloest - erst hoehere eigene
    Statistik, dann der alphabetisch erste Zellenname. Ein Zufall waere hier
    eine Wahl, die in keinem N auftaucht.
    """
    if tafel.empty:
        return None
    sortiert = tafel.sort_values(
        ["plateau_mittel", "statistik", "zelle_id"],
        ascending=[False, False, True])
    return sortiert.iloc[0].to_dict()


# ---------------------------------------------------------------------------
# 5. Abbruchkriterien
# ---------------------------------------------------------------------------
def beta_bereinigung(bot: str, wurzel: str, zid: str, plan: dict,
                     selektionsfalten: list) -> dict:
    """Abbruchkriterium (c) - und der Zufalls-Timing-Test dazu.

    Beides gehoert in dieses Skript, nicht in eine spaetere Aufgabe: ohne sie
    liesse (c) eine Entscheidung offen, und der Vollstaendigkeitstest waere
    nicht bestanden.
    """
    markt = rd.BOTS[bot]["markt"]
    reihe = lies_tagesreihe(bot, wurzel, zid)
    bench = lies_benchmark(wurzel, markt)

    fenster = [(pd.Timestamp(f["von"]), pd.Timestamp(f["bis_ausschliesslich"]))
               for f in plan[bot]["falten"] if f["name"] in selektionsfalten]
    if not fenster:
        return {"bestimmt": False, "grund": "keine Selektionsfalten (Platzhalter)"}

    def im_fenster(d):
        return any((d >= a) & (d < b) for a, b in fenster)

    maske_s = reihe["datum"].map(im_fenster)
    maske_b = bench["datum"].map(im_fenster)
    s = reihe[maske_s].set_index("datum")
    b = bench[maske_b].set_index("datum")
    gemeinsam = s.index.intersection(b.index)
    if len(gemeinsam) < 3:
        raise Abbruch(f"{bot}/{zid}: weniger als drei gemeinsame Tage mit der "
                      f"Benchmark - die Beta-Bereinigung ist so nicht "
                      f"entscheidbar.")
    sr = s.loc[gemeinsam, "netto_rendite"].to_numpy(dtype=float)
    se = s.loc[gemeinsam, "exposure"].to_numpy(dtype=float)
    br = b.loc[gemeinsam, "netto_rendite"].to_numpy(dtype=float)

    pj = perioden_je_jahr(bot)
    ab = kz.alpha_beta(sr, br, pj)
    exposure_mittel = float(np.mean(se))
    konstant = kz.konstante_exposure_calmar(br, exposure_mittel)
    rendite = kz.gesamtrendite_pct(sr)
    dd = kz.max_drawdown_pct(sr)
    return {
        "bestimmt": True,
        "tage": int(len(gemeinsam)),
        "alpha_pct_pa": ab["alpha_pct_pa"],
        "beta": ab["beta"],
        "mittlere_exposure": exposure_mittel,
        "strategie_rendite_pct": rendite,
        "strategie_drawdown_pct": dd,
        "strategie_calmar": kz.calmar(rendite, dd),
        "konstante_exposure": konstant,
        "zufalls_timing": kz.zufalls_timing(se, br, 95.0),
        "renditen": sr,
    }


def abbruchkriterien(bot: str, gew: dict, tafel: pd.DataFrame,
                     zulaessige: set, zul: pd.DataFrame, bereinigung: dict,
                     bester_nicht_spitze: dict) -> dict:
    """Die vier Kriterien, jedes einzeln ausgewiesen."""
    a = gew is not None and gew["statistik"] <= 0.0
    b = len(zulaessige) == 0
    if bereinigung.get("bestimmt"):
        c = (bereinigung["alpha_pct_pa"] <= 0.0
             and bereinigung["strategie_calmar"]
             < bereinigung["konstante_exposure"]["calmar"])
    else:
        c = False
    d = bool(gew is not None and gew["spitze"]
             and bester_nicht_spitze is not None
             and bester_nicht_spitze["statistik"] <= 0.0)
    return {
        "a_median_sharpe_nicht_positiv": bool(a),
        "b_kein_satz_besteht_die_drawdown_bedingung": bool(b),
        "c_beta_bereinigung": bool(c),
        "d_spitze_ohne_tragfaehige_alternative": bool(d),
        "bleibt": not (a or b or c or d),
    }


# ---------------------------------------------------------------------------
# 6. DSR und N-Buchfuehrung
# ---------------------------------------------------------------------------
def n_buchfuehrung(bot: str, tafel: pd.DataFrame, statistik: pd.Series,
                   df: pd.DataFrame, selektionsfalten: list) -> dict:
    n_hist = rd.N_HISTORISCH_JE_BOT[bot]
    n_lauf = int(len(tafel))
    matrix = (df[df["falte"].isin(selektionsfalten)]
              .pivot_table(index="zelle_id", columns="falte",
                           values="netto_sharpe", aggfunc="first")
              .sort_index())
    cluster = kz.cluster_anzahl(matrix.to_numpy(dtype=float), rd.CLUSTER_SCHWELLE)
    return {
        "n_historisch": n_hist,
        "n_zellen_dieser_lauf": n_lauf,
        "n_nominal": n_hist + n_lauf,
        "cluster_dieser_lauf": int(cluster),
        "n_eff": n_hist + int(cluster),
        "n_sicherheitsabstand": 2 * (n_hist + n_lauf),
        "sharpe_varianz_ueber_die_zellen": float(np.var(
            statistik.to_numpy(dtype=float), ddof=1)) if len(statistik) > 1 else 0.0,
    }


def dsr_drei_werte(renditen, buch: dict) -> dict:
    v = buch["sharpe_varianz_ueber_die_zellen"]
    return {
        "bei_n_eff": kz.deflated_sharpe(renditen, buch["n_eff"], v),
        "bei_n_nominal": kz.deflated_sharpe(renditen, buch["n_nominal"], v),
        "bei_2x_n_nominal": kz.deflated_sharpe(renditen,
                                               buch["n_sicherheitsabstand"], v),
        "hinweis_2x": ("Der Wert bei 2 x N_nominal ist ein SICHERHEITSABSTAND, "
                       "kein Wissen: er behauptet nicht, dass doppelt so viele "
                       "Versuche stattgefunden haetten."),
    }


# ---------------------------------------------------------------------------
# 7. Bestaetigungsperiode
# ---------------------------------------------------------------------------
def bestaetigungsperiode(bot: str, df: pd.DataFrame, zid: str, plan: dict) -> dict:
    """Einmal ausgewertet, NACHDEM die Auswahl steht. Kein Veto."""
    name = plan[bot]["bestaetigungsperiode"]
    if name is None:
        return {"bestimmt": False, "grund": "Faltenplan ist Platzhalter (TB-31)"}
    zeile = df[(df["zelle_id"] == zid) & (df["falte"] == name)]
    if zeile.empty:
        raise Abbruch(f"{bot}: die Bestaetigungsperiode '{name}' fehlt fuer den "
                      f"Gewinner.")
    z = zeile.iloc[0]
    return {
        "bestimmt": True,
        "falte": name,
        "n_trades": int(z["n_trades"]),
        "netto_sharpe": (0.0 if int(z["n_trades"]) == 0
                         else float(z["netto_sharpe"])),
        "netto_rendite_pct": float(z["netto_rendite_pct"]),
        "kapital_drawdown_pct": float(z["kapital_drawdown_pct"]),
        "mittlere_exposure": float(z["mittlere_exposure"]),
        "hinweis": ("Die Bestaetigungsperiode ist die einzige Zahl ohne "
                    "Selektion. Sie hat kein Veto und sie waechst jeden Monat."),
    }


# ---------------------------------------------------------------------------
# Der Durchlauf je Bot
# ---------------------------------------------------------------------------
def ein_bot(bot: str, wurzel: str, mess: dict, plan: dict, tabellen: dict) -> dict:
    if plan[bot]["status"] != "endgueltig":
        return {"bot": bot, "auswertbar": False,
                "grund": ("Der Faltenplan dieses Marktes ist ein Platzhalter "
                          "(TB-31). Ohne Falten gibt es keine Selektion - und "
                          "keine Zahl, die so tut als gaebe es eine.")}

    sel = plan[bot]["selektionsfalten"]
    df = lies_zellen(bot, wurzel, mess, plan)
    achsen = gitterachsen(bot, mess)
    bedingung = bedingung_fuer(bot)

    statistik = selektionsstatistik(df, sel)
    zul = zulaessigkeit(bot, df, sel, tabellen)
    bestanden = zul.groupby("zelle_id")["bestanden"].all()
    zulaessige = set(bestanden[bestanden].index)

    tafel = plateau(achsen, bedingung, statistik)
    tafel_zulaessig = tafel[tafel["zelle_id"].isin(zulaessige)]

    # Der Gewinner MUSS zulaessig sein. Ist keine Zelle zulaessig, greift
    # Kriterium (b); berichtet wird dann der Plateau-Gewinner ueber ALLE
    # Zellen, ausdruecklich als "nicht zulaessig" markiert.
    gew = gewinner(tafel_zulaessig if not tafel_zulaessig.empty else tafel)
    gewinner_zulaessig = bool(gew and gew["zelle_id"] in zulaessige)

    grundlage = tafel_zulaessig if not tafel_zulaessig.empty else tafel
    ohne_spitzen = grundlage[~grundlage["spitze"]]
    bester_nicht_spitze = gewinner(ohne_spitzen) if not ohne_spitzen.empty else None

    bereinigung = beta_bereinigung(bot, wurzel, gew["zelle_id"], plan, sel)
    kriterien = abbruchkriterien(bot, gew, tafel, zulaessige, zul, bereinigung,
                                 bester_nicht_spitze)

    buch = n_buchfuehrung(bot, tafel, statistik, df, sel)
    dsr = dsr_drei_werte(bereinigung.get("renditen", []), buch)

    gew_falten = df[(df["zelle_id"] == gew["zelle_id"]) & (df["falte"].isin(sel))]
    beurteilung = {
        "netto_sharpe_median": float(gew["statistik"]),
        "netto_rendite_pct_ueber_selektionsfalten":
            bereinigung.get("strategie_rendite_pct"),
        "netto_drawdown_pct_ueber_selektionsfalten":
            bereinigung.get("strategie_drawdown_pct"),
        "netto_calmar": bereinigung.get("strategie_calmar"),
        "mittel_der_drei_tiefsten_falten_drawdowns":
            kz.drei_tiefste_drawdowns(gew_falten["kapital_drawdown_pct"]),
        "falten_drawdowns": {r["falte"]: float(r["kapital_drawdown_pct"])
                             for _, r in gew_falten.iterrows()},
        "falten_sharpe": {r["falte"]: float(r["netto_sharpe"])
                          for _, r in gew_falten.iterrows()},
        "falten_ohne_trade": [r["falte"] for _, r in gew_falten.iterrows()
                              if int(r["n_trades"]) == 0],
        "alpha_pct_pa": bereinigung.get("alpha_pct_pa"),
        "beta": bereinigung.get("beta"),
        "konstante_exposure": bereinigung.get("konstante_exposure"),
        "zufalls_timing": bereinigung.get("zufalls_timing"),
    }

    # Die berichtete Zeile zum Risikoappetit (Festlegung 6): keine Grenze,
    # aber eine Meldung. Sie steht hier, damit sie nicht vergessen wird.
    risiko = [
        {"falte": r["falte"], "drawdown_pct": r["dd_satz"], "erlaubt_pct": r["erlaubt"]}
        for _, r in zul[(zul["zelle_id"] == gew["zelle_id"])
                        & (zul["dd_satz"] <= -30.0)].iterrows()
    ]

    return {
        "bot": bot,
        "auswertbar": True,
        "selektionsfalten": sel,
        "zellen_im_raster": int(len(tafel)),
        "zellen_zulaessig": int(len(zulaessige)),
        "gewinner": {
            "zelle_id": gew["zelle_id"],
            "plateau_mittel": float(gew["plateau_mittel"]),
            "statistik": float(gew["statistik"]),
            "n_nachbarn": int(gew["n_nachbarn"]),
            "zulaessig": gewinner_zulaessig,
            "markierungen": (["Spitze"] if gew["spitze"] else [])
                            + (["Kante"] if gew["kante"] else [])
                            + ([] if gewinner_zulaessig else ["nicht zulaessig"]),
        },
        "bester_nicht_spitzen_punkt": (
            None if bester_nicht_spitze is None else {
                "zelle_id": bester_nicht_spitze["zelle_id"],
                "statistik": float(bester_nicht_spitze["statistik"]),
                "plateau_mittel": float(bester_nicht_spitze["plateau_mittel"])}),
        "abbruchkriterien": kriterien,
        "beurteilung": beurteilung,
        "risikoappetit_verletzungen": risiko,
        "n_buchfuehrung": buch,
        "dsr": {k: v for k, v in dsr.items()},
        "bestaetigungsperiode": bestaetigungsperiode(bot, df, gew["zelle_id"], plan),
    }


def kapitalregel(ergebnisse: list) -> dict:
    """Was mit dem Kapital eines ausscheidenden Bots geschieht - im Code.

    Die Regel steht hier und nicht nur in der Prosa, weil genau an dieser
    Stelle nach dem Lauf der Druck am groessten wird.
    """
    geht = [e["bot"] for e in ergebnisse
            if e.get("auswertbar") and not e["abbruchkriterien"]["bleibt"]]
    return {
        "ausscheidende_bots": geht,
        "anzahl": len(geht),
        "kapitalregel": ("Das Kapital eines ausscheidenden Bots geht in eine "
                         "STATISCHE BENCHMARK-POSITION in Hoehe seiner "
                         "mittleren Exposure - nicht in Kasse und nicht zu "
                         "den Ueberlebenden."),
        "schattenregel": ("Der Bot laeuft als Schatten weiter. Er kehrt nur "
                          "ueber einen NEUEN vorregistrierten Lauf mit "
                          "VERAENDERTER Hypothese zurueck. Kein 'vorerst "
                          "behalten'."),
        "schwellenregel": ("Die Anzahl ausscheidender Bots ist KEIN Grund, "
                           "eine Schwelle zu aendern."),
        "zulaessiges_ergebnis": rd.FESTLEGUNGEN[12][1],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--rohergebnisse", required=True,
                   help="Wurzelverzeichnis der Rohergebnisse")
    p.add_argument("--json", help="Bericht zusaetzlich als JSON hierhin schreiben")
    p.add_argument("--bot", action="append",
                   help="nur diese Bots auswerten (mehrfach angebbar)")
    args = p.parse_args()

    mess = rd._mess()
    plan = fp.faltenplan(mess)
    with open(BENCHMARK_TABELLE, encoding="utf-8") as f:
        tabellen = json.load(f)

    bots = args.bot or list(rd.BOTS)
    ergebnisse = [ein_bot(b, args.rohergebnisse, mess, plan, tabellen) for b in bots]

    print("=" * 78)
    print("TB-30a - AUSWERTUNG DES SELEKTIONSLAUFS")
    print("=" * 78)
    for e in ergebnisse:
        print(f"\n{'-' * 78}\n{e['bot']}")
        if not e["auswertbar"]:
            print(f"  nicht auswertbar: {e['grund']}")
            continue
        g = e["gewinner"]
        print(f"  Gewinner            {g['zelle_id']}")
        print(f"  Plateau-Mittel      {g['plateau_mittel']:.4f}   "
              f"eigene Statistik {g['statistik']:.4f}   "
              f"Nachbarn {g['n_nachbarn']}")
        print(f"  Markierungen        {', '.join(g['markierungen']) or '(keine)'}")
        print(f"  Zellen              {e['zellen_im_raster']} im Raster, "
              f"{e['zellen_zulaessig']} zulaessig")
        k = e["abbruchkriterien"]
        print(f"  Abbruchkriterien    (a) {k['a_median_sharpe_nicht_positiv']}  "
              f"(b) {k['b_kein_satz_besteht_die_drawdown_bedingung']}  "
              f"(c) {k['c_beta_bereinigung']}  "
              f"(d) {k['d_spitze_ohne_tragfaehige_alternative']}")
        print(f"  ERGEBNIS            {'BLEIBT' if k['bleibt'] else 'GEHT'}")
        b = e["beurteilung"]
        print(f"  Netto-Sharpe (Med.) {b['netto_sharpe_median']:.4f}")
        print(f"  Netto-Calmar        {_z(b['netto_calmar'])}")
        print(f"  3 tiefste DD (Mit.) {b['mittel_der_drei_tiefsten_falten_drawdowns']:.2f} %")
        print(f"  Alpha / Beta        {_z(b['alpha_pct_pa'])} % p.a. / {_z(b['beta'])}")
        if b["zufalls_timing"] and b["zufalls_timing"].get("bestimmt"):
            print(f"  Zufalls-Timing      95. Perzentil "
                  f"{b['zufalls_timing']['wert_pct']:.2f} % gegen "
                  f"{_z(b['netto_rendite_pct_ueber_selektionsfalten'])} % des Satzes")
        n = e["n_buchfuehrung"]
        d = e["dsr"]
        print(f"  N                   eff {n['n_eff']}  nominal {n['n_nominal']}  "
              f"2x {n['n_sicherheitsabstand']}")
        print(f"  DSR                 {d['bei_n_eff']['dsr']:.4f} / "
              f"{d['bei_n_nominal']['dsr']:.4f} / "
              f"{d['bei_2x_n_nominal']['dsr']:.4f}   (Bericht, nicht Tor)")
        for v in e["risikoappetit_verletzungen"]:
            print(f"  ! Risikoappetit     Parametersatz verletzt -30 % in Falte "
                  f"{v['falte']} ({v['drawdown_pct']:.2f} %)")
        bp = e["bestaetigungsperiode"]
        if bp["bestimmt"]:
            print(f"  Bestaetigungsperiode {bp['falte']}: "
                  f"Sharpe {bp['netto_sharpe']:.3f}, "
                  f"Rendite {bp['netto_rendite_pct']:.2f} %, "
                  f"DD {bp['kapital_drawdown_pct']:.2f} %, "
                  f"{bp['n_trades']} Trades")

    kr = kapitalregel(ergebnisse)
    print(f"\n{'=' * 78}\nBLEIBT-GEHT")
    for e in ergebnisse:
        if e.get("auswertbar"):
            print(f"  {e['bot']:28s} "
                  f"{'BLEIBT' if e['abbruchkriterien']['bleibt'] else 'GEHT'}")
        else:
            print(f"  {e['bot']:28s} nicht auswertbar")
    print(f"\n  {kr['kapitalregel']}")
    print(f"  {kr['schattenregel']}")
    print(f"  {kr['schwellenregel']}")
    print(f"  {kr['zulaessiges_ergebnis']}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"bots": [_ohne_arrays(e) for e in ergebnisse],
                       "bleibt_geht": kr}, f, indent=2, ensure_ascii=False,
                      sort_keys=True, default=float)
            f.write("\n")
        print(f"\nJSON geschrieben: {args.json}")
    return 0


def _z(x):
    return "-" if x is None else f"{x:.4f}"


def _ohne_arrays(e):
    return json.loads(json.dumps(e, default=lambda o: None))


if __name__ == "__main__":
    sys.exit(main())
