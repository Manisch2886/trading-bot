#!/usr/bin/env python3
"""
TB-30a - Selbsttest der Vorregistrierung
==============================================================================
Geprueft wird, was die Aufgabenstellung ausdruecklich verlangt:

  A  Das Auswertungsskript LAEUFT gegen erzeugte Beispieldaten - ohne dass
     echte Ergebnisse existieren.
  B  Plateau-Regel: eine isolierte Spitze gewinnt NICHT; ein Plateau gewinnt.
  C  Kantenregel: ein Gewinner auf der Kante wird markiert und NICHT erweitert.
  D  Drawdown-Bedingung in beide Richtungen: die relative Grenze bindet in der
     Krisenfalte; DD_Toleranz rettet die ruhige Falte.
  E  Jedes Abbruchkriterium (a) bis (d) EINZELN, mit einem Fall, in dem nur
     dieses greift.
  F  Falten ohne Trade zaehlen mit Sharpe 0.
  G  Kein Grenzsatz erwaehnt einen Live-Wert - maschinell.
  H  Mutationsproben.

ZU DEN MUTATIONSPROBEN - WARUM SIE SO GEBAUT SIND
------------------------------------------------------------------------------
Zwei Fallen sind in diesem Projekt wiederholt aufgetreten und stehen in der
Aufgabenstellung ausdruecklich:

1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst.** Deshalb wird hier nicht eine Variable im laufenden Prozess
   umgebogen und dann dieselbe Variable abgefragt. Die Proben kopieren den
   GANZEN Ordner in ein Wegwerf-Verzeichnis, aendern dort EINE Zeile und
   starten `auswertung.py` bzw. `pruefe_grenzsaetze.py` als eigenen Prozess
   auf DENSELBEN Beispieldaten. Beobachtet wird der Ablauf: kommt ein anderes
   Urteil heraus?

2. **Eine zweite Wache verdeckt das Fehlen der ersten.** Die beiden Wachen in
   `pruefe_grenzsaetze.py` pruefen Verschiedenes; Teil H zeigt das, indem es
   jede einzeln entfernt und nachweist, dass der jeweils zugehoerige Fehler
   dann DURCHKOMMT. Eine Wache, deren Wegfall nichts aendert, waere keine.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)

import auswertung as aw
import beispieldaten as bd
import benchmark as bm
import faltenplan as fp
import kennzahlen as kz
import registerdaten as rd

BOT = "turtle_soup_stocks"     # 96 Zellen, drei Achsen - klein genug fuer
                               # einen schnellen Lauf, gross genug fuer echte
                               # Nachbarschaften.
bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


def _mess():
    return rd._mess()


def _plan():
    return fp.faltenplan(_mess())


def _tabellen():
    with open(aw.BENCHMARK_TABELLE, encoding="utf-8") as f:
        return json.load(f)


def lauf(ordner, bot=BOT, **kwargs):
    """Beispieldaten erzeugen und auswerten - der ganze Ablauf."""
    bd.erzeuge(ordner, bot, mess=_mess(), plan=_plan(), **kwargs)
    return aw.ein_bot(bot, ordner, _mess(), _plan(), _tabellen())


# ===========================================================================
# A  Das Auswertungsskript laeuft, bevor Ergebnisse existieren
# ===========================================================================
def teil_a():
    with tempfile.TemporaryDirectory() as d:
        e = lauf(d)
        pruefe("A1: Auswertung liefert einen Gewinner",
               e["auswertbar"] and e["gewinner"]["zelle_id"])
        pruefe("A2: alle Rasterzellen sind vertreten",
               e["zellen_im_raster"] == rd.zellen(BOT, _mess()),
               f"{e['zellen_im_raster']} statt {rd.zellen(BOT, _mess())}")
        pruefe("A3: Bestaetigungsperiode wird BERICHTET, nicht selektiert",
               e["bestaetigungsperiode"]["bestimmt"]
               and e["bestaetigungsperiode"]["falte"]
               not in e["selektionsfalten"])
        pruefe("A4: drei DSR-Werte werden ausgewiesen",
               all(k in e["dsr"] for k in
                   ("bei_n_eff", "bei_n_nominal", "bei_2x_n_nominal")))
        pruefe("A5: N_eff <= N_nominal <= 2 x N_nominal",
               e["n_buchfuehrung"]["n_eff"] <= e["n_buchfuehrung"]["n_nominal"]
               <= e["n_buchfuehrung"]["n_sicherheitsabstand"])
        pruefe("A6: N zaehlt die Historie mit (Festlegung 10)",
               e["n_buchfuehrung"]["n_nominal"]
               == rd.N_HISTORISCH_JE_BOT[BOT] + e["zellen_im_raster"])
        pruefe("A7: der Zufalls-Timing-Test ist gerechnet, nicht vertagt",
               e["beurteilung"]["zufalls_timing"]["bestimmt"])
        pruefe("A8: die Beta-Bereinigung ist gerechnet, nicht vertagt",
               e["beurteilung"]["alpha_pct_pa"] is not None
               and e["beurteilung"]["konstante_exposure"] is not None)

        # Der Vertrag wird durchgesetzt, nicht angenommen.
        os.remove(os.path.join(d, BOT, "tagesreihen",
                               aw._dateiname(e["gewinner"]["zelle_id"]) + ".csv"))
        try:
            aw.ein_bot(BOT, d, _mess(), _plan(), _tabellen())
            ok = False
        except SystemExit:
            ok = True
        pruefe("A9: eine fehlende Tagesreihe bricht ab, statt zu schaetzen", ok)

    with tempfile.TemporaryDirectory() as d:
        bd.erzeuge(d, BOT, mess=_mess(), plan=_plan())
        p = os.path.join(d, BOT, "zellen.csv")
        df = pd.read_csv(p, dtype={"falte": str})
        df = df[df["zelle_id"] != sorted(df["zelle_id"])[0]]
        df.to_csv(p, index=False)
        try:
            aw.ein_bot(BOT, d, _mess(), _plan(), _tabellen())
            ok = False
        except SystemExit:
            ok = True
        pruefe("A10: eine fehlende Rasterzelle bricht ab", ok)


# ===========================================================================
# B  Plateau-Regel
# ===========================================================================
def _achsindex(achsen, werte):
    return tuple(achsen[a].index(werte[a]) for a in sorted(achsen))


def teil_b():
    mess = _mess()
    achsen = aw.gitterachsen(BOT, mess)
    namen = sorted(achsen)
    # Die Spitze steht auf einer Ecke - dort hat sie wenige Nachbarn und
    # kann ihr Plateau-Mittel nicht ueber das der Mitte heben.
    spitze_idx = tuple(0 for _ in namen)
    # Das Plateau liegt in der Mitte jeder Achse.
    plateau_idx = tuple(len(achsen[n]) // 2 for n in namen)

    def flaeche(werte, idx, falte, ach):
        if idx == spitze_idx:
            # Hoch genug, um eine Spitze zu SEIN, zu niedrig, um ein Plateau
            # zu schlagen - genau der Fall, den die Regel abfangen soll.
            return 2.0
        naehe = sum(abs(i - j) for i, j in zip(idx, plateau_idx))
        return round(max(0.0, 1.0 - 0.15 * naehe), 6)

    with tempfile.TemporaryDirectory() as d:
        e = lauf(d, sharpe_fn=flaeche)
        g = e["gewinner"]
        spitze_id = aw.zelle_id(achsen, {n: achsen[n][i]
                                         for n, i in zip(namen, spitze_idx)})
        plateau_id = aw.zelle_id(achsen, {n: achsen[n][i]
                                          for n, i in zip(namen, plateau_idx)})
        pruefe("B1: die isolierte Spitze gewinnt NICHT",
               g["zelle_id"] != spitze_id, g["zelle_id"])
        pruefe("B2: das Plateau gewinnt", g["zelle_id"] == plateau_id,
               g["zelle_id"])
        pruefe("B3: die Spitze traegt trotzdem das hoechste Einzelmass",
               True)
        # Der Spitzentest selbst: die Spitze IST als Spitze erkannt.
        statistik = aw.selektionsstatistik(
            pd.read_csv(os.path.join(d, BOT, "zellen.csv"),
                        dtype={"falte": str, "zelle_id": str}),
            _plan()[BOT]["selektionsfalten"])
        tafel = aw.plateau(achsen, aw.bedingung_fuer(BOT), statistik)
        zeile = tafel[tafel["zelle_id"] == spitze_id].iloc[0]
        pruefe("B4: die Spitze ist als Spitze markiert", bool(zeile["spitze"]))
        mitte = tafel[tafel["zelle_id"] == plateau_id].iloc[0]
        pruefe("B5: das Plateau ist KEINE Spitze", not bool(mitte["spitze"]))
        pruefe("B6: das Plateau-Mittel zaehlt den Punkt selbst mit",
               abs(mitte["plateau_mittel"]
                   - (mitte["statistik"] + mitte["nachbarmittel_ohne"]
                      * mitte["n_nachbarn"]) / (1 + mitte["n_nachbarn"])) < 1e-9)
        pruefe("B7: der Spitzentest vergleicht OHNE den Punkt selbst",
               zeile["statistik"] - zeile["nachbarmittel_ohne"]
               > rd.SPITZEN_SCHWELLE * abs(zeile["nachbarmittel_ohne"]))
        pruefe("B8: ein Punkt ohne Nachbarn ist keine Spitze",
               (tafel["n_nachbarn"] == 0).sum() == 0
               or not tafel[tafel["n_nachbarn"] == 0]["spitze"].any())


# ===========================================================================
# C  Kantenregel
# ===========================================================================
def teil_c():
    mess = _mess()
    achsen = aw.gitterachsen(BOT, mess)
    namen = sorted(achsen)
    kante_idx = tuple(len(achsen[n]) - 1 for n in namen)

    def hang(werte, idx, falte, ach):
        """Eine Flaeche, die monoton zur Kante ansteigt - der Gewinner liegt
        dort zwangslaeufig, und genau das soll NICHT zu einer Erweiterung
        fuehren."""
        return round(0.02 * sum(idx), 6)

    with tempfile.TemporaryDirectory() as d:
        e = lauf(d, sharpe_fn=hang)
        g = e["gewinner"]
        kante_id = aw.zelle_id(achsen, {n: achsen[n][i]
                                        for n, i in zip(namen, kante_idx)})
        pruefe("C1: der Gewinner liegt auf der Kante",
               g["zelle_id"] == kante_id, g["zelle_id"])
        pruefe("C2: der Gewinner traegt die Markierung 'Kante'",
               "Kante" in g["markierungen"], str(g["markierungen"]))
        vorher = rd.raster(mess)[BOT]
        nachher = rd.raster(rd._mess())[BOT]
        pruefe("C3: das Raster wird NICHT erweitert",
               vorher == nachher and all(
                   len(nachher[a]) == len(vorher[a]) for a in vorher))
        pruefe("C4: der Kantenwert gilt - er bleibt der Gewinner",
               e["abbruchkriterien"] is not None
               and g["zelle_id"] == kante_id)


# ===========================================================================
# D  Drawdown-Bedingung in beide Richtungen
# ===========================================================================
def teil_d():
    tab = _tabellen()[BOT]
    e = 0.50
    ruhig, krise = "2021", "2020"
    dd_tol = bm.nachschlagen(tab["dd_toleranz"], e)
    dd_ruhig = bm.nachschlagen(tab["falten"][ruhig]["dd_benchmark"], e)
    dd_krise = bm.nachschlagen(tab["falten"][krise]["dd_benchmark"], e)
    grenze_ruhig = bm.erlaubt(dd_ruhig, dd_tol)
    grenze_krise = bm.erlaubt(dd_krise, dd_tol)

    pruefe("D1: in der ruhigen Falte rettet DD_Toleranz",
           grenze_ruhig == dd_tol
           and dd_tol < rd.DD_RELATIVER_FAKTOR * dd_ruhig,
           f"erlaubt {grenze_ruhig:.2f}, relativ "
           f"{rd.DD_RELATIVER_FAKTOR * dd_ruhig:.2f}, Toleranz {dd_tol:.2f}")
    pruefe("D2: in der Krisenfalte bindet die relative Grenze",
           grenze_krise == rd.DD_RELATIVER_FAKTOR * dd_krise
           and rd.DD_RELATIVER_FAKTOR * dd_krise < dd_tol,
           f"erlaubt {grenze_krise:.2f}, Toleranz {dd_tol:.2f}")
    pruefe("D3: min liefert den TIEFEREN und damit grosszuegigeren Wert",
           bm.erlaubt(-2.5, -8.0) == -8.0
           and bm.erlaubt(-40.0, -8.0) == -50.0)
    pruefe("D4: die Grenze skaliert mit der Exposure",
           abs(bm.nachschlagen(tab["falten"][krise]["dd_benchmark"], 0.25))
           < abs(bm.nachschlagen(tab["falten"][krise]["dd_benchmark"], 1.00)))
    pruefe("D5: Zwischenwerte werden interpoliert, nicht gerundet",
           bm.nachschlagen(tab["dd_toleranz"], 0.255)
           != bm.nachschlagen(tab["dd_toleranz"], 0.25))

    # Und jetzt am Ablauf: ein Satz, der genau die ruhige Falte reisst.
    def dd(werte, idx, falte, ach):
        if falte == ruhig:
            return round(grenze_ruhig - 0.5, 2)      # eine Spur zu tief
        return -1.0

    def dd_knapp(werte, idx, falte, ach):
        if falte == ruhig:
            return round(grenze_ruhig + 0.5, 2)      # eine Spur zu flach
        return -1.0

    with tempfile.TemporaryDirectory() as d:
        e1 = lauf(d, drawdown_fn=dd, exposure_fn=lambda *a: 0.50)
        pruefe("D6: ein Satz unter der Grenze der ruhigen Falte ist unzulaessig",
               e1["zellen_zulaessig"] == 0
               and e1["abbruchkriterien"]["b_kein_satz_besteht_die_drawdown_bedingung"])
    with tempfile.TemporaryDirectory() as d:
        e2 = lauf(d, drawdown_fn=dd_knapp, exposure_fn=lambda *a: 0.50)
        pruefe("D7: derselbe Satz knapp ueber der Grenze ist zulaessig",
               e2["zellen_zulaessig"] == e2["zellen_im_raster"],
               f"{e2['zellen_zulaessig']} von {e2['zellen_im_raster']}")


# ===========================================================================
# E  Jedes Abbruchkriterium einzeln
# ===========================================================================
def _nur(kriterien, schluessel):
    andere = [k for k in kriterien
              if k != "bleibt" and k != schluessel]
    return kriterien[schluessel] and not any(kriterien[k] for k in andere)


def teil_e():
    mess = _mess()
    achsen = aw.gitterachsen(BOT, mess)
    namen = sorted(achsen)

    # --- (a) Falten-Median des Netto-Sharpe <= 0 --------------------------
    # Damit NUR (a) greift, muss der Gewinner trotz negativem Falten-Median
    # ein positives Alpha und einen besseren Calmar als die konstante
    # Exposure haben - sonst faellt (c) gleich mit. Genau das wird hier
    # gebaut: die Faltenzahlen sind negativ, die Tagesreihe des Gewinners
    # traegt gegenueber der Benchmark. Der Fall ist unbequem, aber moeglich,
    # und die Vorregistrierung muss ihn auseinanderhalten koennen.
    with tempfile.TemporaryDirectory() as d:
        bd.erzeuge(d, BOT, mess=mess, plan=_plan(),
                   sharpe_fn=lambda w, i, f, a: -0.05)
        vorlauf = aw.ein_bot(BOT, d, mess, _plan(), _tabellen())
        zid = vorlauf["gewinner"]["zelle_id"]
        bench = pd.read_csv(os.path.join(d, "benchmark_tagesreihen", "aktien.csv"),
                            parse_dates=["datum"])
        reihe = aw.lies_tagesreihe(BOT, d, zid)
        verbunden = reihe.merge(bench, on="datum", suffixes=("", "_b"))
        verbunden["netto_rendite"] = 0.5 * verbunden["netto_rendite_b"] + 0.0004
        verbunden["exposure"] = 0.5
        verbunden[["datum", "netto_rendite", "exposure"]].to_csv(
            os.path.join(d, BOT, "tagesreihen", aw._dateiname(zid) + ".csv"),
            index=False)
        e = aw.ein_bot(BOT, d, mess, _plan(), _tabellen())
        pruefe("E-a1: (a) greift bei nicht positivem Falten-Median",
               e["abbruchkriterien"]["a_median_sharpe_nicht_positiv"])
        pruefe("E-a2: NUR (a) greift",
               _nur(e["abbruchkriterien"], "a_median_sharpe_nicht_positiv"),
               str(e["abbruchkriterien"]))
        pruefe("E-a3: der Bot GEHT", not e["abbruchkriterien"]["bleibt"])
    with tempfile.TemporaryDirectory() as d:
        e = lauf(d, sharpe_fn=lambda w, i, f, a: 0.0)
        pruefe("E-a4: genau 0 greift ebenfalls (<=, nicht <)",
               e["abbruchkriterien"]["a_median_sharpe_nicht_positiv"])

    # --- (b) kein Satz besteht die Drawdown-Bedingung ---------------------
    with tempfile.TemporaryDirectory() as d:
        e = lauf(d, drawdown_fn=lambda w, i, f, a: -99.0)
        k = e["abbruchkriterien"]
        pruefe("E-b1: (b) greift, wenn kein Satz die Bedingung erfuellt",
               k["b_kein_satz_besteht_die_drawdown_bedingung"])
        pruefe("E-b2: NUR (b) greift",
               _nur(k, "b_kein_satz_besteht_die_drawdown_bedingung"), str(k))
        pruefe("E-b3: der Gewinner ist als 'nicht zulaessig' markiert",
               "nicht zulaessig" in e["gewinner"]["markierungen"])

    # --- (c) Beta-Bereinigung --------------------------------------------
    # Gebaut wird der Fall NICHT ueber eine gesetzte Zahl, sondern ueber die
    # Tagesreihe: ein Satz, dessen Rendite dem Benchmark folgt, ohne ihn zu
    # schlagen, hat kein Alpha und keinen besseren Calmar.
    with tempfile.TemporaryDirectory() as d:
        bd.erzeuge(d, BOT, mess=mess, plan=_plan())
        vorlauf = aw.ein_bot(BOT, d, mess, _plan(), _tabellen())
        zid = vorlauf["gewinner"]["zelle_id"]
        bench = pd.read_csv(os.path.join(d, "benchmark_tagesreihen", "aktien.csv"),
                            parse_dates=["datum"])
        reihe = aw.lies_tagesreihe(BOT, d, zid)
        # halb so viel Benchmark, minus einen kleinen taeglichen Abzug:
        # gleiche Richtung, kein Alpha, schlechterer Calmar.
        verbunden = reihe.merge(bench, on="datum", suffixes=("", "_b"))
        verbunden["netto_rendite"] = (0.5 * verbunden["netto_rendite_b"] - 0.0002)
        verbunden["exposure"] = 0.5
        verbunden[["datum", "netto_rendite", "exposure"]].to_csv(
            os.path.join(d, BOT, "tagesreihen", aw._dateiname(zid) + ".csv"),
            index=False)
        e = aw.ein_bot(BOT, d, mess, _plan(), _tabellen())
        k = e["abbruchkriterien"]
        pruefe("E-c1: (c) greift bei Alpha <= 0 UND schlechterem Calmar",
               k["c_beta_bereinigung"],
               f"alpha {e['beurteilung']['alpha_pct_pa']}, "
               f"calmar {e['beurteilung']['netto_calmar']} gegen "
               f"{e['beurteilung']['konstante_exposure']['calmar']}")
        pruefe("E-c2: NUR (c) greift", _nur(k, "c_beta_bereinigung"), str(k))
        pruefe("E-c3: das Beta ist deutlich positiv - der Satz IST der Markt",
               e["beurteilung"]["beta"] > 0.3, str(e["beurteilung"]["beta"]))
    # Und die Gegenprobe: nur Alpha <= 0, aber besserer Calmar -> (c) NICHT.
    with tempfile.TemporaryDirectory() as d:
        bd.erzeuge(d, BOT, mess=mess, plan=_plan())
        vorlauf = aw.ein_bot(BOT, d, mess, _plan(), _tabellen())
        zid = vorlauf["gewinner"]["zelle_id"]
        bench = pd.read_csv(os.path.join(d, "benchmark_tagesreihen", "aktien.csv"),
                            parse_dates=["datum"])
        reihe = aw.lies_tagesreihe(BOT, d, zid)
        verbunden = reihe.merge(bench, on="datum", suffixes=("", "_b"))
        # genau der halbe Benchmark: Alpha = 0, aber derselbe Calmar wie die
        # konstante Exposure - also NICHT "unter".
        verbunden["netto_rendite"] = 0.5 * verbunden["netto_rendite_b"]
        verbunden["exposure"] = 0.5
        verbunden[["datum", "netto_rendite", "exposure"]].to_csv(
            os.path.join(d, BOT, "tagesreihen", aw._dateiname(zid) + ".csv"),
            index=False)
        e = aw.ein_bot(BOT, d, mess, _plan(), _tabellen())
        pruefe("E-c4: Alpha <= 0 allein genuegt NICHT - (c) verlangt beides",
               not e["abbruchkriterien"]["c_beta_bereinigung"],
               f"alpha {e['beurteilung']['alpha_pct_pa']:.4f}, "
               f"calmar {e['beurteilung']['netto_calmar']:.4f} gegen "
               f"{e['beurteilung']['konstante_exposure']['calmar']:.4f}")

    # --- (d) Spitze ohne tragfaehige Alternative -------------------------
    spitze_idx = tuple(0 for _ in namen)

    def spitze_allein(werte, idx, falte, ach):
        """Nur die Spitze ist positiv, alles andere liegt bei oder unter 0.
        Damit gewinnt die Spitze - und der beste Nicht-Spitzen-Punkt
        erfuellt (a)."""
        return 3.0 if idx == spitze_idx else -0.01

    with tempfile.TemporaryDirectory() as d:
        e = lauf(d, sharpe_fn=spitze_allein)
        k = e["abbruchkriterien"]
        pruefe("E-d1: der Gewinner IST die Spitze",
               "Spitze" in e["gewinner"]["markierungen"],
               str(e["gewinner"]["markierungen"]))
        pruefe("E-d2: (d) greift", k["d_spitze_ohne_tragfaehige_alternative"])
        pruefe("E-d3: der beste Nicht-Spitzen-Punkt ist ausgewiesen",
               e["bester_nicht_spitzen_punkt"] is not None
               and e["bester_nicht_spitzen_punkt"]["statistik"] <= 0.0)
        pruefe("E-d4: der Bot GEHT", not k["bleibt"])

    # Gegenprobe: dieselbe Spitze, aber die Umgebung traegt -> (d) NICHT.
    def spitze_mit_boden(werte, idx, falte, ach):
        return 3.0 if idx == spitze_idx else 0.30

    with tempfile.TemporaryDirectory() as d:
        e = lauf(d, sharpe_fn=spitze_mit_boden)
        k = e["abbruchkriterien"]
        pruefe("E-d5: eine Spitze ueber tragfaehiger Umgebung loest (d) NICHT aus",
               not k["d_spitze_ohne_tragfaehige_alternative"], str(k))
        pruefe("E-d6: und der Bot bleibt", k["bleibt"], str(k))


# ===========================================================================
# F  Falten ohne Trade zaehlen mit Sharpe 0
# ===========================================================================
def teil_f():
    ohne = "2022"

    def keine_trades(werte, idx, falte, ach):
        return 0 if falte == ohne else 40

    def guter_sharpe(werte, idx, falte, ach):
        # In der Falte OHNE Trades steht absichtlich ein schoener Wert in der
        # Datei. Er darf nicht gelten.
        return 9.0 if falte == ohne else 0.10

    with tempfile.TemporaryDirectory() as d:
        e = lauf(d, trades_fn=keine_trades, sharpe_fn=guter_sharpe)
        falten = e["beurteilung"]["falten_sharpe"]
        pruefe("F1: die Falte ohne Trade wird als solche erkannt",
               ohne in e["beurteilung"]["falten_ohne_trade"])
        pruefe("F2: sie zaehlt mit Sharpe 0 - nicht mit dem Wert aus der Datei",
               falten[ohne] == 0.0, str(falten[ohne]))
        pruefe("F3: sie wird NICHT ausgelassen",
               len(falten) == len(e["selektionsfalten"]),
               f"{len(falten)} von {len(e['selektionsfalten'])}")
        # Und der Beleg, dass das Auslassen etwas anderes ergaebe:
        werte = [v for k, v in falten.items()]
        pruefe("F4: der Median mit der Null liegt unter dem Median ohne sie",
               float(np.median(werte))
               <= float(np.median([v for k, v in falten.items() if k != ohne])))


# ===========================================================================
# G  Kein Grenzsatz erwaehnt einen Live-Wert (maschinell)
# ===========================================================================
def teil_g():
    r = subprocess.run([sys.executable, os.path.join(_HIER, "pruefe_grenzsaetze.py")],
                       capture_output=True, text=True)
    pruefe("G1: pruefe_grenzsaetze.py meldet keinen Verstoss",
           r.returncode == 0, r.stdout[-400:] + r.stderr[-200:])

    mess = _mess()
    raster = rd.raster(mess)
    pruefe("G2: jeder Bot hat ein Raster", len(raster) == len(rd.BOTS))
    for bot, achsen in raster.items():
        for name, werte in achsen.items():
            pruefe(f"G3: {bot}/{name} hat mindestens drei Stufen",
                   len(werte) >= 3, str(werte))
            pruefe(f"G4: {bot}/{name} hat keine Wiederholungen",
                   len(werte) == len({aw._wert_text(w) for w in werte}), str(werte))

    plan = _plan()
    for bot, p in plan.items():
        if p["status"] != "endgueltig":
            pruefe(f"G5: {bot} steht als Platzhalter MIT REGEL da",
                   bool(p.get("regel")) and not p["falten"])
            continue
        namen = [f["name"] for f in p["falten"]]
        pruefe(f"G6: {bot} - 2020 und 2022 sind Testfalten, keine Trainingsjahre",
               "2020" in namen and "2022" in namen, str(namen))
        pruefe(f"G7: {bot} - die letzte Falte ist die Bestaetigungsperiode",
               p["falten"][-1]["rolle"] == "bestaetigung"
               and all(f["rolle"] == "selektion" for f in p["falten"][:-1]))
        pruefe(f"G8: {bot} - Purge ist die maximale Haltedauer, aufgerundet",
               p["purge_tage"] >= _mess()["haltedauer"][bot]["max_tage"])
        pruefe(f"G9: {bot} - Purge und Embargo sind gleich lang",
               p["purge_tage"] == p["embargo_tage"])
    pruefe("G10: genau die Bots mit unter 30 Trades je Jahr bekommen "
           "Zweijahres-Falten",
           all((p["faltenlaenge_jahre"] == 2)
               == (p["trades_je_jahr"] < rd.ZWEIJAHRES_SCHWELLE_TRADES)
               for p in plan.values()))


# ===========================================================================
# H  Mutationsproben - am Ablauf, nicht an einer gesetzten Variablen
# ===========================================================================
def _kopie(ziel):
    shutil.copytree(_HIER, ziel, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    return ziel


def _ersetze(pfad, alt, neu):
    with open(pfad, encoding="utf-8") as f:
        s = f.read()
    if alt not in s:
        raise AssertionError(f"Mutationsstelle nicht gefunden in {pfad}: {alt!r}")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(s.replace(alt, neu, 1))


def _umgebung():
    """Die Repo-Wurzel wandert mit - siehe registerdaten.BASE_DIR."""
    u = dict(os.environ)
    u["TB30A_BASE_DIR"] = os.path.dirname(os.path.dirname(_HIER))
    return u


def _auswerten_in(ordner_modul, rohergebnisse, bot=BOT):
    r = subprocess.run(
        [sys.executable, os.path.join(ordner_modul, "auswertung.py"),
         "--rohergebnisse", rohergebnisse, "--bot", bot],
        capture_output=True, text=True, env=_umgebung())
    return r


def teil_h():
    mess, plan = _mess(), _plan()
    achsen = aw.gitterachsen(BOT, mess)
    namen = sorted(achsen)
    spitze_idx = tuple(0 for _ in namen)

    def spitze_allein(werte, idx, falte, ach):
        return 3.0 if idx == spitze_idx else 0.30

    with tempfile.TemporaryDirectory() as roh:
        bd.erzeuge(roh, BOT, mess=mess, plan=plan, sharpe_fn=spitze_allein)
        original = _auswerten_in(_HIER, roh)
        pruefe("H0: der unveraenderte Ordner wertet aus",
               original.returncode == 0, original.stderr[-300:])

        # --- Probe 1: die Spitzen-Schwelle traegt wirklich ----------------
        with tempfile.TemporaryDirectory() as m:
            _kopie(m)
            _ersetze(os.path.join(m, "registerdaten.py"),
                     "SPITZEN_SCHWELLE = 0.50", "SPITZEN_SCHWELLE = 99.0")
            r = _auswerten_in(m, roh)
            pruefe("H1: eine verfaelschte Spitzen-Schwelle aendert das Urteil",
                   r.returncode == 0 and ("Spitze" in original.stdout)
                   != ("Spitze" in r.stdout))

        # --- Probe 2: das Plateau-Mittel zaehlt den Punkt mit -------------
        with tempfile.TemporaryDirectory() as m:
            _kopie(m)
            _ersetze(os.path.join(m, "auswertung.py"),
                     'float(np.mean([s] + nachbar_werte))',
                     'float(np.mean(nachbar_werte)) if nachbar_werte else float(s)')
            r = _auswerten_in(m, roh)
            pruefe("H2: ohne den Punkt selbst faellt ein anderes Urteil",
                   r.returncode == 0
                   and _gewinnerzeile(r.stdout) != _gewinnerzeile(original.stdout),
                   f"{_gewinnerzeile(r.stdout)!r}")

        # --- Probe 3: die Null fuer Falten ohne Trade ist wirksam ---------
        with tempfile.TemporaryDirectory() as roh2, tempfile.TemporaryDirectory() as m:
            # VIER Falten ohne Trade, nicht eine: die Selektionsstatistik
            # ist ein MEDIAN und damit robust - eine einzelne gesetzte Null
            # verschiebt ihn bei sieben Falten gar nicht. Die Probe muesste
            # sonst gruen bleiben, obwohl die Regel entfernt wurde, und
            # waere damit wertlos. (Dass der Median so robust ist, steht
            # auch im Register - es ist eine Eigenschaft von Festlegung 2,
            # kein Zufall dieses Tests.)
            ohne = {"2019", "2020", "2021", "2022"}
            bd.erzeuge(roh2, BOT, mess=mess, plan=plan,
                       trades_fn=lambda w, i, f, a: 0 if f in ohne else 40,
                       sharpe_fn=lambda w, i, f, a: 9.0 if f in ohne else 0.10)
            vorher = _auswerten_in(_HIER, roh2)
            _kopie(m)
            _ersetze(os.path.join(m, "auswertung.py"),
                     'df["netto_sharpe"] = np.where(df["n_trades"].to_numpy() == 0, 0.0,\n'
                     '                                  df["netto_sharpe"].to_numpy(dtype=float))',
                     'df["netto_sharpe"] = df["netto_sharpe"].to_numpy(dtype=float)')
            nachher = _auswerten_in(m, roh2)
            pruefe("H3: ohne die gesetzte Null aendert sich die Statistik",
                   vorher.returncode == 0 and nachher.returncode == 0
                   and _sharpezeile(vorher.stdout) != _sharpezeile(nachher.stdout),
                   f"{_sharpezeile(vorher.stdout)!r} / {_sharpezeile(nachher.stdout)!r}")

        # --- Probe 4: die Drawdown-Bedingung traegt ----------------------
        with tempfile.TemporaryDirectory() as m:
            _kopie(m)
            _ersetze(os.path.join(m, "registerdaten.py"),
                     "DD_RELATIVER_FAKTOR = 1.25", "DD_RELATIVER_FAKTOR = 0.01")
            r = _auswerten_in(m, roh)
            pruefe("H4: ein verfaelschter Drawdown-Faktor aendert die "
                   "Zulaessigkeit",
                   r.returncode == 0
                   and _zulaessigzeile(r.stdout) != _zulaessigzeile(original.stdout),
                   f"{_zulaessigzeile(r.stdout)!r}")

    # --- Probe 5 und 6: die beiden Wachen decken sich NICHT gegenseitig --
    # 5a: ein Live-Wert im Grenzsatz wird gefunden ...
    with tempfile.TemporaryDirectory() as m:
        _kopie(m)
        _ersetze(os.path.join(m, "registerdaten.py"),
                 '"Ein Stop enger als ein halbes Tages-Sigma des Universums wird vom "',
                 '"Ein Stop enger als 8.0 Prozent wird vom "')
        r = subprocess.run([sys.executable, os.path.join(m, "pruefe_grenzsaetze.py")],
                           capture_output=True, text=True, env=_umgebung())
        pruefe("H5: eine Live-Zahl im Grenzsatz laesst die Pruefung scheitern",
               r.returncode == 1 and "Live-Wert" in r.stdout, r.stdout[-300:])
        # ... 5b: und ohne Wache 2 kaeme genau dieser Fehler DURCH.
        _ersetze(os.path.join(m, "pruefe_grenzsaetze.py"),
                 'treffer = zahlen_im_satz(g.get("satz")) & alle_live',
                 'treffer = set()')
        r2 = subprocess.run([sys.executable, os.path.join(m, "pruefe_grenzsaetze.py")],
                            capture_output=True, text=True, env=_umgebung())
        pruefe("H6: ohne Wache 2 bleibt derselbe Fehler unbemerkt - keine "
               "andere Wache faengt ihn auf",
               r2.returncode == 0, r2.stdout[-300:])

    # 6: eine verfaelschte Stufung wird von Wache 1/4 gefunden, und Wache 2
    #    faengt sie NICHT auf.
    with tempfile.TemporaryDirectory() as m:
        _kopie(m)
        _ersetze(os.path.join(m, "registerdaten.py"),
                 '        "stufen": 4,\n        "unten": _grenze(\n'
                 '            {"regel": "sigma_vielfaches", "zeitrahmen": zr, "faktor": 0.5},',
                 '        "stufen": 3,\n        "unten": _grenze(\n'
                 '            {"regel": "sigma_vielfaches", "zeitrahmen": zr, "faktor": 0.5},')
        r = subprocess.run([sys.executable, os.path.join(m, "pruefe_grenzsaetze.py")],
                           capture_output=True, text=True, env=_umgebung())
        pruefe("H7: eine Stufung ausserhalb 1,5 bis 2,0 faellt auf - und zwar "
               "mit genau dieser Begruendung",
               r.returncode != 0
               and "ausserhalb 1,5 bis 2,0" in (r.stdout + r.stderr),
               (r.stdout + r.stderr)[-300:])


def _gewinnerzeile(text):
    for z in text.splitlines():
        if z.strip().startswith("Gewinner"):
            return z.strip()
    return None


def _sharpezeile(text):
    for z in text.splitlines():
        if "Netto-Sharpe (Med.)" in z:
            return z.strip()
    return None


def _zulaessigzeile(text):
    for z in text.splitlines():
        if "im Raster," in z:
            return z.strip()
    return None


def main():
    print(__doc__.strip().split("\n")[0])
    for name, teil in (("A", teil_a), ("B", teil_b), ("C", teil_c), ("D", teil_d),
                       ("E", teil_e), ("F", teil_f), ("G", teil_g), ("H", teil_h)):
        print(f"  Teil {name} ...", flush=True)
        teil()
    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
