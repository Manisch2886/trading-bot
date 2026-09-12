"""
Auswertung: Was misst der kombinierte Drawdown von -1,43 %?
==============================================================================
Liest die von `bot_lauf.py` erzeugten Positionsverlaeufe und rechnet daraus
alle Zahlen des Berichts. Rechnet zusaetzlich die URSPRUENGLICHE Zahl aus den
im Repo abgelegten `results/*/equity_curve.csv` nach, nach der Methodik von
`strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py` - sonst
waere nicht belegt, dass hier ueberhaupt dieselbe Groesse untersucht wird.

    python3 auswertung.py

Schreibt nach `ergebnisse/` und gibt alles zusaetzlich auf der Konsole aus.
"""

import json
import os
import sys

import numpy as np
import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, _DIR)
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))

import exposure_kern as ek
from kursdaten import Zaehler, entferne_unvollstaendige

DATEN_DIR = os.path.join(_DIR, "daten")
ERGEBNIS_DIR = os.path.join(_DIR, "ergebnisse")
DATA_DIR = os.path.join(_REPO_ROOT, "data")
CONFIG_DIR = os.path.join(_REPO_ROOT, "config")
os.makedirs(ERGEBNIS_DIR, exist_ok=True)

STARTKAPITAL = 10_000.0

ALLE_BOTS = ["elliott_wave", "t3_supertrend", "elliott_wave_stocks", "rsi2_mean_reversion",
             "rsi2_crypto", "turtle_soup_crypto", "turtle_soup_stocks",
             "volatility_breakout", "volatility_breakout_crypto"]

# Die vier Bots der urspruenglichen Zahl (PROTOTYPE_FINDINGS.md, Abschnitt 5)
VIER_BOTS = ["elliott_wave", "t3_supertrend", "elliott_wave_stocks", "rsi2_mean_reversion"]

ANLAGEKLASSE = {
    "elliott_wave": "krypto", "t3_supertrend": "krypto", "rsi2_crypto": "krypto",
    "turtle_soup_crypto": "krypto", "volatility_breakout_crypto": "krypto",
    "elliott_wave_stocks": "aktien", "rsi2_mean_reversion": "aktien",
    "turtle_soup_stocks": "aktien", "volatility_breakout": "aktien",
}
AKTIEN_BOTS = [b for b in ALLE_BOTS if ANLAGEKLASSE[b] == "aktien"]

# Die urspruengliche Zahl stammt aus diesen vier Dateien. `elliott_wave`
# liegt historisch in der Wurzel von results/, nicht im Unterordner.
URSPRUNGS_KURVEN = {
    "elliott_wave": "results/equity_curve.csv",
    "t3_supertrend": "results/t3_supertrend/equity_curve.csv",
    "elliott_wave_stocks": "results/elliott_wave_stocks/equity_curve.csv",
    "rsi2_mean_reversion": "results/rsi2_mean_reversion/equity_curve.csv",
}

STRESS_FENSTER = {
    "Corona-Einbruch (Feb-Apr 2020)": ("2020-02-01", "2020-04-30"),
    "Gesamtjahr 2022": ("2022-01-01", "2022-12-31"),
}


# ---------------------------------------------------------------------------
# Einlesen
# ---------------------------------------------------------------------------

def lade_bot(bot):
    pos = pd.read_csv(os.path.join(DATEN_DIR, f"{bot}_positionen.csv"),
                       parse_dates=["entry_time", "exit_time"])
    with open(os.path.join(DATEN_DIR, f"{bot}_meta.json")) as f:
        meta = json.load(f)
    return pos, meta


def lade_kurse(symbole, melden=True):
    """Tages-Schlusskurse je Symbol aus data/, unvollstaendige Kerzen
    gestrichen (shared/kursdaten.py, PR #81)."""
    kurse, fehlend = {}, []
    zaehler = Zaehler()
    for sym in symbole:
        pfad = os.path.join(DATA_DIR, f"{sym}_1d.csv")
        if not os.path.exists(pfad):
            fehlend.append(sym)
            continue
        df = pd.read_csv(pfad, parse_dates=["open_time"])
        df, gestrichen = entferne_unvollstaendige(df, symbol=sym, melden=False)
        zaehler.erfasse(sym, gestrichen)
        if df.empty:
            fehlend.append(sym)
            continue
        kurse[sym] = df.set_index("open_time")["close"].sort_index()
    if melden:
        zaehler.melde()
    return kurse, fehlend


def symbolliste(datei):
    with open(os.path.join(CONFIG_DIR, datei)) as f:
        return [z.strip() for z in f if z.strip() and not z.startswith("#")]


# ---------------------------------------------------------------------------
# Teil 0: die urspruengliche Zahl und ihre Herkunft
# ---------------------------------------------------------------------------

def tageskurve_aus_datei(rel_pfad):
    df = pd.read_csv(os.path.join(_REPO_ROOT, rel_pfad), parse_dates=["time"]).sort_values("time")
    taeglich = df.groupby(df["time"].dt.normalize())["capital_after"].last()
    voll = pd.date_range(taeglich.index.min(), taeglich.index.max(), freq="D")
    return taeglich.reindex(voll).ffill()


def tageskurve_aus_positionen(pos):
    p = pos.sort_values("exit_time")
    taeglich = p.groupby(pd.to_datetime(p["exit_time"]).dt.normalize())["capital_after"].last()
    voll = pd.date_range(taeglich.index.min(), taeglich.index.max(), freq="D")
    return taeglich.reindex(voll).ffill()


def originale_formel(kurven):
    """Exakt die Rechnung aus `portfolio_correlation_analysis.py`:
    gemeinsames Fenster, jede Kurve auf 100 normiert, ungewichtetes Mittel."""
    start = max(s.index.min() for s in kurven.values())
    ende = min(s.index.max() for s in kurven.values())
    tage = pd.date_range(start, ende, freq="D")
    rahmen = pd.DataFrame({b: s.reindex(tage).ffill().bfill() for b, s in kurven.items()})
    normiert = rahmen / rahmen.iloc[0] * 100
    portfolio = normiert.mean(axis=1)
    return {
        "fenster": [str(start.date()), str(ende.date())],
        "max_dd_je_bot_pct": {b: round(ek.max_drawdown_pct(normiert[b]), 2) for b in normiert},
        "max_dd_kombiniert_pct": round(ek.max_drawdown_pct(portfolio), 2),
        "rendite_kombiniert_pct": round(float(portfolio.iloc[-1] / portfolio.iloc[0] - 1) * 100, 2),
        "korrelation": normiert.pct_change().dropna().corr().round(3).to_dict(),
    }


# ---------------------------------------------------------------------------
# Exposure und Drawdowns einer Bot-Gruppe
# ---------------------------------------------------------------------------

def werte_gruppe_aus(name, bots, reihen_je_bot, bh_renditen):
    kombi = ek.kombiniere({b: reihen_je_bot[b] for b in bots})
    kennzahlen = ek.exposure_kennzahlen(kombi["exposure"], kombi["n_offen"])
    invest = ek.drawdown_auf_investiertem_kapital(kombi)

    stress = {}
    for label, (von, bis) in STRESS_FENSTER.items():
        stress[label] = _stress_zeile(kombi.loc[(kombi.index >= von) & (kombi.index <= bis)])

    # Die 10 % schlechtesten Buy-and-Hold-Tage werden IM Messfenster bestimmt,
    # nicht ueber die gesamte verfuegbare Kurshistorie: ein Dezil aus sechzig
    # Jahren beschriebe eine andere Marktphase als die gemessene.
    for universum, renditen in bh_renditen.items():
        im_fenster = renditen.loc[(renditen.index >= kombi.index.min())
                                   & (renditen.index <= kombi.index.max())]
        if im_fenster.empty:
            continue
        tage = ek.schlechteste_tage(im_fenster, 0.10)
        stress[f"10 % schlechteste B&H-Tage ({universum})"] = _stress_zeile(
            kombi.loc[kombi.index.intersection(tage)])

    verteilung = kombi["n_offen"].value_counts(normalize=True).sort_index()
    kombi.to_csv(os.path.join(ERGEBNIS_DIR, f"zeitreihe_{name}.csv"))
    # Verdichteter Verlauf zum Nachlesen: Monatsmittel der Exposure.
    monat = (kombi["exposure"].resample("MS").mean() * 100).round(2)
    monat.to_frame("mittlere_exposure_pct").to_csv(
        os.path.join(ERGEBNIS_DIR, f"monatlich_{name}.csv"))

    return {
        "gruppe": name,
        "bots": bots,
        "fenster": [str(kombi.index.min().date()), str(kombi.index.max().date())],
        "exposure": kennzahlen,
        "max_dd_gesamtkapital_pct": round(ek.max_drawdown_pct(kombi["kapital_ende"]), 2),
        "max_dd_investiertes_kapital_pct": invest["max_drawdown_pct"],
        "aktive_tage": invest["aktive_tage"],
        "rendite_gesamtkapital_pct": round(float(kombi["kapital_ende"].iloc[-1]
                                                  / kombi["kapital_start"].iloc[0] - 1) * 100, 2),
        "stress": stress,
        "verteilung_offene_positionen": {int(k): round(float(v) * 100, 2)
                                          for k, v in verteilung.items()},
    }, kombi


def _stress_zeile(teil):
    if teil.empty:
        return {"tage": 0, "mittlere_exposure_pct": None, "anteil_tage_flach_pct": None}
    return {
        "tage": int(len(teil)),
        "mittlere_exposure_pct": round(float(teil["exposure"].mean()) * 100, 2),
        "anteil_tage_flach_pct": round(float((teil["n_offen"] == 0).mean()) * 100, 2),
    }


# ---------------------------------------------------------------------------
# Je Bot
# ---------------------------------------------------------------------------

def je_bot(bots, reihen_je_bot, fenster):
    tage = pd.date_range(fenster[0], fenster[1], freq="D")
    offen = pd.DataFrame({b: reihen_je_bot[b].reindex(tage)["n_offen"].fillna(0) for b in bots})

    zeilen = []
    for bot in bots:
        r = reihen_je_bot[bot].reindex(tage)
        n = r["n_offen"].fillna(0)
        gebunden = r["gebunden"].fillna(0.0)
        kapital = r["kapital_ende"].ffill().bfill()
        kapital_start = r["kapital_start"].ffill().bfill()

        hoch = kapital.cummax()
        dd = (kapital - hoch) / hoch
        tief = dd.idxmin()
        gipfel = kapital.loc[:tief].idxmax()
        in_dd = (kapital.index >= gipfel) & (kapital.index <= tief)

        andere_flach = (offen[[b for b in bots if b != bot]].sum(axis=1) == 0)
        veraenderung = kapital.diff().fillna(0.0)
        verlust = veraenderung[in_dd & (veraenderung < 0)]
        verlust_allein = veraenderung[in_dd & (veraenderung < 0) & andere_flach]
        anteil = (abs(float(verlust_allein.sum()) / float(verlust.sum())) * 100
                  if float(verlust.sum()) != 0 else None)

        zeilen.append({
            "bot": bot,
            "anlageklasse": ANLAGEKLASSE[bot],
            "zeit_im_markt_pct": round(float((n > 0).mean()) * 100, 2),
            "mittlere_exposure_pct": round(float((gebunden / kapital_start).mean()) * 100, 2),
            "mittlere_positionen_wenn_offen": round(float(n[n > 0].mean()), 2) if (n > 0).any() else 0.0,
            "max_positionen": int(n.max()),
            "max_dd_im_fenster_pct": round(float(dd.min()) * 100, 2),
            "dd_phase": f"{gipfel.date()} bis {tief.date()}",
            "dd_anteil_an_tagen_mit_allen_anderen_flach_pct": (round(anteil, 2)
                                                                if anteil is not None else None),
            "anteil_tage_alle_anderen_flach_pct": round(float(andere_flach.mean()) * 100, 2),
        })
    return pd.DataFrame(zeilen)


# ---------------------------------------------------------------------------
# Konzentration
# ---------------------------------------------------------------------------

def gehaltene_symbole(bots, positionen_je_bot, tage):
    lage = pd.Series(np.arange(len(tage)), index=tage)
    gehalten = {}
    for bot in bots:
        mengen = [set() for _ in range(len(tage))]
        for sym, a, b in zip(positionen_je_bot[bot]["symbol"],
                             pd.to_datetime(positionen_je_bot[bot]["entry_time"]).dt.normalize(),
                             pd.to_datetime(positionen_je_bot[bot]["exit_time"]).dt.normalize()):
            if b < tage[0] or a > tage[-1]:
                continue
            i = int(lage.get(a, 0))
            j = int(lage.get(b, len(tage) - 1))
            for t in range(i, j + 1):
                mengen[t].add(sym)
        gehalten[bot] = mengen
    return gehalten


def titelueberlappung(bots, positionen_je_bot, fenster):
    tage = pd.date_range(fenster[0], fenster[1], freq="D")
    gehalten = gehaltene_symbole(bots, positionen_je_bot, tage)

    paare = []
    for i, bot_a in enumerate(bots):
        for bot_b in bots[i + 1:]:
            u = np.array([len(gehalten[bot_a][t] & gehalten[bot_b][t]) for t in range(len(tage))])
            if u.max() == 0:
                continue
            paare.append({
                "bot_a": bot_a, "bot_b": bot_b,
                "max_gleiche_symbole": int(u.max()),
                "tage_mit_ueberlappung": int((u > 0).sum()),
                "anteil_tage_pct": round(float((u > 0).mean()) * 100, 2),
                "mittel_wenn_ueberlappung": round(float(u[u > 0].mean()), 2),
            })

    mehrfach = []
    for t in range(len(tage)):
        zaehler = {}
        for bot in bots:
            for sym in gehalten[bot][t]:
                zaehler[sym] = zaehler.get(sym, 0) + 1
        mehrfach.append(max(zaehler.values()) if zaehler else 0)
    mehrfach = np.array(mehrfach)

    return (pd.DataFrame(paare).sort_values("max_gleiche_symbole", ascending=False),
            {"max_bots_auf_demselben_symbol": int(mehrfach.max()),
             "anteil_tage_mit_doppelhaltung_pct": round(float((mehrfach > 1).mean()) * 100, 2)})


# ---------------------------------------------------------------------------
# Bewertung zu Marktpreisen (die Kapitalkurve der Bots kennt nur REALISIERTE
# Gewinne - offene Positionen stehen bis zum Ausstieg zum Einstandswert)
# ---------------------------------------------------------------------------

def mtm_reihen(bot, positionen, kurse, reihen):
    """Tageswert der offenen Positionen zu Schlusskursen.

    Naeherung, die im Bericht ausgewiesen wird: als Bezugspunkt dient der
    Schlusskurs des EINSTIEGSTAGES (Tagesaufloesung), auch bei den beiden
    Bots auf Stunden- bzw. 4-Stunden-Kerzen. Am Ausstiegstag wird der
    tatsaechlich realisierte Wert eingesetzt, nicht der Schlusskurs -
    dazwischen liegt die Abweichung, die `mtm_naht` beziffert.
    """
    tage = reihen.index
    lage = pd.Series(np.arange(len(tage)), index=tage)
    wert = np.zeros(len(tage))
    naht = []

    for sym, gruppe in positionen.groupby("symbol"):
        reihe = kurse.get(sym)
        if reihe is None:
            continue
        preis = reihe.reindex(tage.union(reihe.index)).ffill().reindex(tage).ffill().bfill()
        preis = preis.to_numpy()
        for a, b, betrag, pnl in zip(
                pd.to_datetime(gruppe["entry_time"]).dt.normalize(),
                pd.to_datetime(gruppe["exit_time"]).dt.normalize(),
                gruppe["allocation"], gruppe["pnl_pct"]):
            if b < tage[0] or a > tage[-1]:
                continue
            i = int(lage.get(a, 0))
            j = int(lage.get(b, len(tage) - 1))
            basis = preis[i]
            if not np.isfinite(basis) or basis == 0:
                continue
            wert[i:j] += betrag * preis[i:j] / basis          # offene Tage
            wert[j] += betrag * (1 + pnl / 100.0)             # Ausstiegstag: realisiert
            naht.append(float((preis[j] / basis - 1) * 100 - pnl))

    frei = reihen["kapital_ende"].to_numpy() - reihen["gebunden"].to_numpy()
    return pd.Series(frei + wert, index=tage), naht


def mtm_gruppe(bots, positionen_je_bot, reihen_je_bot, kurse, fenster):
    tage = pd.date_range(fenster[0], fenster[1], freq="D")
    gesamt = pd.Series(0.0, index=tage)
    je_bot_kurven, naht_alle = {}, []
    for bot in bots:
        kurve, naht = mtm_reihen(bot, positionen_je_bot[bot], kurse, reihen_je_bot[bot])
        naht_alle += naht
        teil = kurve.reindex(tage).ffill().bfill()
        je_bot_kurven[bot] = teil
        basis = reihen_je_bot[bot].reindex(tage)["kapital_start"].ffill().bfill().iloc[0]
        gesamt += teil * ((100.0 / len(bots)) / basis)
    naht_alle = np.array(naht_alle) if naht_alle else np.array([0.0])
    return gesamt, pd.DataFrame(je_bot_kurven), {
        "positionen_mit_kurs": int(len(naht_alle)),
        "naht_median_pp": round(float(np.median(np.abs(naht_alle))), 2),
        "naht_p90_pp": round(float(np.percentile(np.abs(naht_alle), 90)), 2),
    }


def korrelationen(mtm_je_bot, bh_renditen):
    """Korrelation der TAEGLICHEN Bewegungen - einmal so, wie sie das Projekt
    bisher misst (aus der realisierten Kapitalkurve), und einmal aus der
    Bewertung zu Marktpreisen.

    Der Unterschied ist der Kern des Einwands "negative Korrelation in dieser
    Groessenordnung ist unplausibel": eine Kurve, die sich nur an
    Ausstiegstagen bewegt, hat an den meisten Tagen die Rendite exakt 0 - und
    zwei ueberwiegend aus Nullen bestehende Reihen korrelieren mechanisch
    nahe null, egal was die Maerkte tun.
    """
    renditen = mtm_je_bot.pct_change().replace([np.inf, -np.inf], np.nan).dropna(how="all")
    matrix = renditen.corr()
    gegen_bh = {}
    for universum, bh in bh_renditen.items():
        gemeinsam = renditen.join(bh.rename("bh"), how="inner").dropna()
        if len(gemeinsam) > 30:
            gegen_bh[universum] = {b: round(float(gemeinsam[b].corr(gemeinsam["bh"])), 3)
                                    for b in renditen.columns}
    ausser_diagonale = matrix.where(~np.eye(len(matrix), dtype=bool)).stack()
    return {
        "matrix": matrix.round(3).to_dict(),
        "mittel_ausser_diagonale": round(float(ausser_diagonale.mean()), 3),
        "min": round(float(ausser_diagonale.min()), 3),
        "max": round(float(ausser_diagonale.max()), 3),
        "gegen_buy_and_hold": gegen_bh,
    }


# ---------------------------------------------------------------------------
def main():
    positionen_je_bot, meta_je_bot, reihen_je_bot = {}, {}, {}
    for bot in ALLE_BOTS:
        pos, meta = lade_bot(bot)
        positionen_je_bot[bot] = pos
        meta_je_bot[bot] = meta
        reihen_je_bot[bot] = ek.taegliche_reihen(pos, STARTKAPITAL)

    ausgabe = {}

    # --- 0. die urspruengliche Zahl -----------------------------------------
    print("=" * 78)
    print("0. DIE URSPRUENGLICHE ZAHL - nachgerechnet aus den abgelegten Kurven")
    print("=" * 78)
    abgelegt = {b: tageskurve_aus_datei(p) for b, p in URSPRUNGS_KURVEN.items()}
    frisch = {b: tageskurve_aus_positionen(positionen_je_bot[b]) for b in VIER_BOTS}

    original = originale_formel(abgelegt)
    heute = originale_formel(frisch)
    print(f"  Fenster: {original['fenster'][0]} bis {original['fenster'][1]}")
    for bot in VIER_BOTS:
        print(f"    {bot:<24} abgelegt {original['max_dd_je_bot_pct'][bot]:>8.2f} %   "
              f"heutige live_params {heute['max_dd_je_bot_pct'][bot]:>8.2f} %")
    print(f"  kombiniert (25/25/25/25):  abgelegt {original['max_dd_kombiniert_pct']:>8.2f} %   "
          f"heutige live_params {heute['max_dd_kombiniert_pct']:>8.2f} %")

    print("\n  Woher der Unterschied kommt - je ein Bot durch seine heutige Kurve ersetzt:")
    tausch = {}
    for bot in VIER_BOTS:
        gemischt = dict(abgelegt)
        gemischt[bot] = frisch[bot]
        tausch[bot] = originale_formel(gemischt)["max_dd_kombiniert_pct"]
        print(f"    nur {bot:<24} getauscht:  {tausch[bot]:>8.2f} %")
    ausgabe["urspruengliche_zahl"] = {"abgelegte_kurven": original,
                                       "heutige_live_params": heute,
                                       "einzeltausch_max_dd_pct": tausch}

    # --- Abgleich abgelegte Kurven ------------------------------------------
    print("\n" + "=" * 78)
    print("ABGLEICH: abgelegte results-Kurve gegen heutige live_params.py")
    print("=" * 78)
    abgleich = pd.DataFrame([{
        "bot": bot,
        "zeilen_abgelegt": meta_je_bot[bot]["abgleich_results_csv"].get("zeilen_repo"),
        "zeilen_neu": meta_je_bot[bot]["trades_ausgefuehrt"],
        "identisch": meta_je_bot[bot]["abgleich_results_csv"].get("identisch"),
        "allocation_pct": meta_je_bot[bot]["allocation_pct"],
        "max_concurrent": meta_je_bot[bot]["max_concurrent_positions"],
        "rendite_neu_pct": meta_je_bot[bot]["rendite_pct"],
        "max_dd_neu_pct": meta_je_bot[bot]["max_drawdown_pct_bot"],
    } for bot in ALLE_BOTS])
    abgleich.to_csv(os.path.join(ERGEBNIS_DIR, "abgleich_abgelegte_kurven.csv"), index=False)
    print(abgleich.to_string(index=False))
    ausgabe["abgleich"] = abgleich.to_dict("records")

    # --- Buy-and-Hold-Referenz ----------------------------------------------
    print("\n" + "=" * 78)
    print("BUY-AND-HOLD-REFERENZ je Universum")
    print("=" * 78)
    bh_renditen, bh_info, alle_kurse = {}, {}, {}
    for universum, datei in (("aktien", "sp500_top150.txt"), ("krypto", "top25_symbols.txt")):
        kurse, fehlend = lade_kurse(symbolliste(datei))
        alle_kurse.update(kurse)
        renditen = ek.bh_tagesrenditen(kurse)
        bh_renditen[universum] = renditen
        bh_info[universum] = {"symbole": len(kurse), "ohne_datei": len(fehlend),
                              "handelstage": int(len(renditen)),
                              "von": str(renditen.index.min().date()),
                              "bis": str(renditen.index.max().date())}
        print(f"  {universum}: {len(kurse)} Symbole ({len(fehlend)} ohne Datei), "
              f"{len(renditen)} Handelstage {bh_info[universum]['von']}..{bh_info[universum]['bis']}")
    ausgabe["buy_and_hold_referenz"] = bh_info

    # Symbole, die ein Bot handelt, aber in keiner Universumsliste stehen
    gehandelt = set().union(*[set(p["symbol"]) for p in positionen_je_bot.values()])
    nachzuladen = sorted(gehandelt - set(alle_kurse))
    if nachzuladen:
        nach, _ = lade_kurse(nachzuladen, melden=False)
        alle_kurse.update(nach)
        print(f"  zusaetzlich geladen (gehandelt, aber nicht in der Universumsliste): "
              f"{len(nach)} von {len(nachzuladen)}")

    # --- Gruppen ------------------------------------------------------------
    gruppen = (("vier_bots", VIER_BOTS), ("neun_bots", ALLE_BOTS), ("vier_aktien_bots", AKTIEN_BOTS))
    ergebnisse = {}
    for name, bots in gruppen:
        ergebnis, kombi = werte_gruppe_aus(name, bots, reihen_je_bot, bh_renditen)

        mtm, mtm_je_bot, naht = mtm_gruppe(bots, positionen_je_bot, reihen_je_bot,
                                            alle_kurse, ergebnis["fenster"])
        ergebnis["max_dd_zu_marktpreisen_pct"] = round(ek.max_drawdown_pct(mtm), 2)
        ergebnis["mtm_naht"] = naht
        ergebnis["korrelation_zu_marktpreisen"] = korrelationen(mtm_je_bot, bh_renditen)
        einzel = [z["max_dd_im_fenster_pct"] for z in je_bot(bots, reihen_je_bot,
                                                              ergebnis["fenster"]).to_dict("records")]
        ergebnis["mittlerer_einzel_dd_pct"] = round(float(np.mean(einzel)), 2)
        ergebnis["schlechtester_einzel_dd_pct"] = round(float(np.min(einzel)), 2)
        mtm.to_frame("kapital_zu_marktpreisen").to_csv(
            os.path.join(ERGEBNIS_DIR, f"mtm_{name}.csv"))
        ergebnisse[name] = ergebnis

        e = ergebnis["exposure"]
        print("\n" + "=" * 78)
        print(f"GRUPPE {name.upper()} ({len(bots)} Bots)")
        print("=" * 78)
        print(f"  gemeinsames Fenster: {ergebnis['fenster'][0]} bis {ergebnis['fenster'][1]} "
              f"({e['tage']} Kalendertage)")
        print(f"  Brutto-Exposure   Mittel {e['mittel_pct']:>6.2f} %   Median {e['median_pct']:>6.2f} %"
              f"   p10 {e['p10_pct']:>6.2f} %   p90 {e['p90_pct']:>6.2f} %   max {e['max_pct']:>6.2f} %")
        print(f"  Tage ohne jede Position: {e['anteil_tage_flach_pct']:.2f} %   "
              f"Tage ueber 50 % Exposure: {e['anteil_tage_ueber_50_pct']:.2f} %")
        print(f"  Max Drawdown  am Gesamtkapital       {ergebnis['max_dd_gesamtkapital_pct']:>8.2f} %")
        print(f"                am investierten Kapital{ergebnis['max_dd_investiertes_kapital_pct']:>8.2f} %")
        print(f"                zu Marktpreisen        {ergebnis['max_dd_zu_marktpreisen_pct']:>8.2f} %"
              f"   (Naht-Median {naht['naht_median_pp']} Pp.)")
        print(f"  zum Vergleich: mittlerer Einzel-Bot-DD {ergebnis['mittlerer_einzel_dd_pct']:>6.2f} %, "
              f"schlechtester {ergebnis['schlechtester_einzel_dd_pct']:.2f} %")
        kor = ergebnis["korrelation_zu_marktpreisen"]
        print(f"  Korrelation der Tagesbewegungen zu Marktpreisen: Mittel {kor['mittel_ausser_diagonale']:+.3f} "
              f"(min {kor['min']:+.3f}, max {kor['max']:+.3f})")
        for universum, werte in kor["gegen_buy_and_hold"].items():
            print(f"    gegen Buy-and-Hold {universum}: "
                  + ", ".join(f"{b}={v:+.2f}" for b, v in werte.items()))
        print("  Exposure unter Stress:")
        for label, wert in ergebnis["stress"].items():
            if wert["mittlere_exposure_pct"] is None:
                print(f"    {label:<42} keine Tage im Fenster")
            else:
                print(f"    {label:<42} {wert['mittlere_exposure_pct']:>6.2f} %   "
                      f"(flach an {wert['anteil_tage_flach_pct']:.1f} % der {wert['tage']} Tage)")

        tabelle = je_bot(bots, reihen_je_bot, ergebnis["fenster"])
        tabelle.to_csv(os.path.join(ERGEBNIS_DIR, f"je_bot_{name}.csv"), index=False)
        ergebnis["je_bot"] = tabelle.to_dict("records")
        print(f"\n  je Bot im Fenster dieser Gruppe:")
        print(tabelle.to_string(index=False))

    ausgabe["gruppen"] = ergebnisse

    # --- Konzentration ------------------------------------------------------
    print("\n" + "=" * 78)
    print("KONZENTRATION: gleichzeitig gehaltene Titel (Neuner-Buch)")
    print("=" * 78)
    paare, gesamt = titelueberlappung(ALLE_BOTS, positionen_je_bot,
                                       ergebnisse["neun_bots"]["fenster"])
    paare.to_csv(os.path.join(ERGEBNIS_DIR, "titelueberlappung.csv"), index=False)
    print(paare.to_string(index=False))
    print(f"\n  Hoechste Zahl Bots auf demselben Symbol am selben Tag: "
          f"{gesamt['max_bots_auf_demselben_symbol']}")
    print(f"  Anteil Tage mit mindestens einer Doppelhaltung: "
          f"{gesamt['anteil_tage_mit_doppelhaltung_pct']:.2f} %")
    ausgabe["titelueberlappung_gesamt"] = gesamt

    vert = ergebnisse["neun_bots"]["verteilung_offene_positionen"]
    print("\n  Verteilung gleichzeitig offener Positionen (Neuner-Buch), Quantile:")
    reihe = pd.Series({k: v for k, v in vert.items()})
    kum = reihe.sort_index().cumsum()
    for q in (10, 25, 50, 75, 90, 99):
        wert = int(kum.index[(kum >= q).argmax()])
        print(f"    {q:>2}. Perzentil: {wert:>3} Positionen")

    ausgabe["meta_je_bot"] = meta_je_bot
    with open(os.path.join(ERGEBNIS_DIR, "kennzahlen.json"), "w") as f:
        json.dump(ausgabe, f, indent=2, default=str)
    print(f"\nGeschrieben nach {os.path.relpath(ERGEBNIS_DIR, _REPO_ROOT)}/")


if __name__ == "__main__":
    main()
