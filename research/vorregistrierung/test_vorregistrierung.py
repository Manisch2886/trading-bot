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

3. **Eine Mutationsprobe ohne Gegenprobe zaehlt nicht als Pruefung**
   (Register 40.7, Fable 24a). Seit TB-97 laeuft jede der sieben Proben
   H1-H7 ein zweites Mal OHNE ihre Mutation und muss dann scheitern
   (`<name>-G`, `_mit_gegenprobe`). Anlass: F4 hat mit `<=` bestanden, ohne
   je gemessen zu haben. Dieselbe Regel gilt fuer F4 und fuer die Stellen,
   die bis TB-97 Jahresliterale trugen (D1-G, D2-G, F1-G, F4-G, G11-G1/G2).
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


def _selektionsfalten(p):
    """Die Namen der Selektionsfalten eines Bots, in Planreihenfolge."""
    return [f["name"] for f in p["falten"] if f["rolle"] == "selektion"]


def _abgedeckte_jahre(falte):
    """Die Kalenderjahre, die eine Falte VOLL abdeckt - gerechnet aus ihren
    Grenzen, nicht aus ihrem Namen (`2020-2021` deckt 2020 und 2021 ab).
    Seit TB-97 in `beispieldaten.py`, das die Krisenfalten damit bildet."""
    return bd.abgedeckte_jahre(falte)


REGISTER = bd.REGISTER


def _testjahre_aus_register():
    """Register 5.1 Nr. 4: die Jahre, die Testfalten sind und keine
    Trainingsjahre. Aus dem Registertext gelesen, nicht als Literal (Fable 23a:
    ein Literal ist eine Kopie des Registers im Code, und Kopien altern).
    Genau ein Treffer, sonst None - dann scheitert G6 sichtbar.
    Seit TB-97 liest der Parser in `beispieldaten.py`: ein Leser fuer G6 und
    fuer die Krisenfalten der Beispieldaten, keine zweite Kopie des Musters."""
    return bd.jahre_aus_register_5_1_nr_4(REGISTER)


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
def _ruhig_und_krise(tab, sel, e):
    """Die ruhigste und die schwerste Selektionsfalte des HEUTIGEN Plans, nach
    dem Benchmark-Drawdown bei Exposure e - nicht nach Jahreszahl. Bis TB-97
    standen hier "2021" und "2020", die Beispieljahre aus Register 4.4 (Stand
    14.09.2026); Fable 24a: die Pruefung prueft die Regel, nicht das Beispiel."""
    dd = {f: bm.nachschlagen(tab["falten"][f]["dd_benchmark"], e) for f in sel}
    return max(sel, key=dd.get), min(sel, key=dd.get)


def _toleranz_rettet(tab, falte, e):
    """D1 als Aussage ueber eine Falte: dort setzt DD_Toleranz die Grenze."""
    dd_tol = bm.nachschlagen(tab["dd_toleranz"], e)
    dd = bm.nachschlagen(tab["falten"][falte]["dd_benchmark"], e)
    return (bm.erlaubt(dd, dd_tol) == dd_tol
            and dd_tol < rd.DD_RELATIVER_FAKTOR * dd)


def _relativ_bindet(tab, falte, e):
    """D2 als Aussage ueber eine Falte: dort setzt die relative Grenze sie."""
    dd_tol = bm.nachschlagen(tab["dd_toleranz"], e)
    dd = bm.nachschlagen(tab["falten"][falte]["dd_benchmark"], e)
    return (bm.erlaubt(dd, dd_tol) == rd.DD_RELATIVER_FAKTOR * dd
            and rd.DD_RELATIVER_FAKTOR * dd < dd_tol)


def teil_d():
    tab = _tabellen()[BOT]
    e = 0.50
    ruhig, krise = _ruhig_und_krise(tab, _selektionsfalten(_plan()[BOT]), e)
    dd_tol = bm.nachschlagen(tab["dd_toleranz"], e)
    dd_ruhig = bm.nachschlagen(tab["falten"][ruhig]["dd_benchmark"], e)
    dd_krise = bm.nachschlagen(tab["falten"][krise]["dd_benchmark"], e)
    grenze_ruhig = bm.erlaubt(dd_ruhig, dd_tol)
    grenze_krise = bm.erlaubt(dd_krise, dd_tol)

    pruefe("D1: in der ruhigen Falte rettet DD_Toleranz",
           _toleranz_rettet(tab, ruhig, e),
           f"ruhigste Falte {ruhig}: erlaubt {grenze_ruhig:.2f}, relativ "
           f"{rd.DD_RELATIVER_FAKTOR * dd_ruhig:.2f}, Toleranz {dd_tol:.2f}")
    pruefe("D2: in der Krisenfalte bindet die relative Grenze",
           _relativ_bindet(tab, krise, e),
           f"schwerste Falte {krise}: erlaubt {grenze_krise:.2f}, "
           f"Toleranz {dd_tol:.2f}")
    # Gegenproben (Block C, TB-97): die Aussagen unterscheiden die Falten -
    # umgewidmet, also die schwerste als ruhige gelesen und umgekehrt,
    # muessen D1 und D2 scheitern. Sonst waere die Falte aus dem Plan nur ein
    # Platzhalter fuer das alte Literal.
    pruefe("D1-G: Gegenprobe zu D1 - die schwerste Falte als ruhige gelesen, "
           "scheitert sie", not _toleranz_rettet(tab, krise, e), krise)
    pruefe("D2-G: Gegenprobe zu D2 - die ruhigste Falte als Krisenfalte "
           "gelesen, scheitert sie", not _relativ_bindet(tab, ruhig, e), ruhig)
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
def _f_lauf(ohne):
    """Beispieldaten, in denen die Falten `ohne` keinen Trade haben, und ihre
    Auswertung. Eigene Funktion, damit die Gegenproben denselben Weg gehen."""
    def keine_trades(werte, idx, falte, ach):
        return 0 if falte in ohne else 40

    def guter_sharpe(werte, idx, falte, ach):
        # In den Falten OHNE Trades steht absichtlich ein schoener Wert in der
        # Datei. Er darf nicht gelten.
        return 9.0 if falte in ohne else 0.10

    with tempfile.TemporaryDirectory() as d:
        return lauf(d, trades_fn=keine_trades, sharpe_fn=guter_sharpe)


def _f1(e, ohne):
    return bool(ohne) and all(f in e["beurteilung"]["falten_ohne_trade"]
                              for f in ohne)


def _f4_mediane(e, ohne):
    falten = e["beurteilung"]["falten_sharpe"]
    rest = [v for k, v in falten.items() if k not in ohne]
    return (float(np.median(list(falten.values()))),
            float(np.median(rest)) if rest else float("nan"))


def teil_f():
    plan = _plan()[BOT]
    sel = _selektionsfalten(plan)
    # Die Falten ohne Trade kommen aus dem Plan, nicht als Literal (bis TB-97
    # stand hier ohne = "2022", eine Falte). Und es ist eine STRIKTE MEHRHEIT
    # der Selektionsfalten, wie in H3: die Statistik ist ein Median, erst eine
    # strikte Mehrheit gesetzter Nullen verschiebt ihn - mit einer Null unter
    # neun lagen beide Mediane gleich, und F4 pruefte mit `<=` (TB-95/TB-97,
    # Register 40.4). Beim Plan von TB-97 fuer turtle_soup_stocks: fuenf von
    # neun Selektionsfalten (2017-2021).
    ohne = set(sel[:len(sel) // 2 + 1])
    e = _f_lauf(ohne)
    falten = e["beurteilung"]["falten_sharpe"]
    pruefe("F1: die Falten ohne Trade werden als solche erkannt",
           _f1(e, ohne), f"{sorted(ohne)} gegen {e['beurteilung']['falten_ohne_trade']}")
    pruefe("F2: sie zaehlen mit Sharpe 0 - nicht mit dem Wert aus der Datei",
           all(falten[f] == 0.0 for f in ohne),
           str({f: falten.get(f) for f in sorted(ohne)}))
    pruefe("F3: sie werden NICHT ausgelassen",
           len(falten) == len(e["selektionsfalten"]),
           f"{len(falten)} von {len(e['selektionsfalten'])}")
    # Und der Beleg, dass das Auslassen etwas anderes ergaebe - "unter" heisst
    # `<` (bis TB-97 `<=`: bei gleichen Medianen bestand F4, ohne zu messen).
    mit, ohne_sie = _f4_mediane(e, ohne)
    pruefe("F4: der Median mit der Null liegt unter dem Median ohne sie",
           mit < ohne_sie,
           f"{mit:.4f} / {ohne_sie:.4f} - ohne Trade: {sorted(ohne)} von {sel}")

    # Gegenproben (Block B/C, TB-97, Register 40.7). F4: leere Menge - keine
    # Falte ohne Trade - dann liegen beide Mediane gleich, F4 muss scheitern.
    mit, ohne_sie = _f4_mediane(_f_lauf(set()), set())
    pruefe("F4-G: Gegenprobe zu F4 - ohne Falte ohne Trade scheitert sie",
           not mit < ohne_sie, f"{mit:.4f} / {ohne_sie:.4f}")
    # F1: die Falte umgewidmet - die Bestaetigungsperiode statt einer
    # Selektionsfalte ohne Trade - dann darf F1 sie nicht finden.
    best = {f["name"] for f in plan["falten"] if f["rolle"] == "bestaetigung"}
    e_um = _f_lauf(best)
    pruefe("F1-G: Gegenprobe zu F1 - die Bestaetigungsperiode als Falte ohne "
           "Trade, scheitert sie", not _f1(e_um, best),
           f"{sorted(best)} gegen {e_um['beurteilung']['falten_ohne_trade']}")


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
    testjahre = _testjahre_aus_register()
    for bot, p in plan.items():
        if p["status"] != "endgueltig":
            pruefe(f"G5: {bot} steht als Platzhalter MIT REGEL da",
                   bool(p.get("regel")) and not p["falten"])
            continue
        # Die Sache aus Register 5.1 Nr. 4, gerechnet: jedes der Jahre liegt
        # in einer Falte der Rolle `selektion`. Die Bestaetigungsperiode zaehlt
        # nicht. Bis TB-95 stand hier `"2020" in namen` - seit den
        # Zweijahresfalten von elliott_wave (TB-61) traf das nichts mehr.
        namen = [f["name"] for f in p["falten"]]
        abgedeckt = set().union(*(_abgedeckte_jahre(f) for f in p["falten"]
                                  if f["rolle"] == "selektion"))
        pruefe(f"G6: {bot} - die Jahre aus Register 5.1 Nr. 4 {testjahre} liegen "
               f"in Selektionsfalten, sind keine Trainingsjahre",
               testjahre is not None and set(testjahre) <= abgedeckt,
               f"{namen}, abgedeckt {sorted(abgedeckt)}")
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

    # G11 (TB-97): die Krisenfalten der Beispieldaten (beispieldaten.py, bis
    # TB-97 das Literal ("2020", "2022")) - je Bot aus dem Plan und Register
    # 5.1 Nr. 4. Gemessen in TB-97 (A4): es braucht nicht irgendeine
    # Selektionsfalte, sondern eine mit tiefem Benchmark-Drawdown; das prueft
    # die zweite Haelfte der Bedingung.
    tabellen = _tabellen()
    for bot, p in plan.items():
        if p["status"] != "endgueltig":
            continue
        ok, zusatz = _g11(bot, p, tabellen,
                          bd.krisenfalten(p["falten"], testjahre))
        pruefe(f"G11: {bot} - die Beispieldaten haben Krisenfalten, eine nicht "
               f"konstante Exposure und bestehen die Drawdown-Bedingung", ok,
               zusatz)
    # Gegenproben (Block C): (1) der Plan verbogen - die Krisenfalten zu
    # Bestaetigungsfalten umgewidmet - dann gibt es keine Krise und die
    # Exposure ist konstant; (2) die Krise auf die ruhigste Falte verbogen -
    # dann reisst der Krisen-Drawdown die Grenze. Beides muss G11 scheitern.
    p = plan[BOT]
    krise = set(bd.krisenfalten(p["falten"], testjahre))
    verbogen = dict(p, falten=[dict(f, rolle="bestaetigung") if f["name"] in krise
                               else f for f in p["falten"]])
    ok, zusatz = _g11(BOT, verbogen, tabellen,
                      bd.krisenfalten(verbogen["falten"], testjahre))
    pruefe(f"G11-G1: Gegenprobe zu G11 - Krisenfalten umgewidmet, scheitert "
           f"sie ({BOT})", not ok, zusatz)
    ruhig, _ = _ruhig_und_krise(tabellen[BOT], _selektionsfalten(p), 0.60)
    ok, zusatz = _g11(BOT, p, tabellen, [ruhig])
    pruefe(f"G11-G2: Gegenprobe zu G11 - die ruhigste Falte als Krisenfalte, "
           f"scheitert sie ({BOT})", not ok, zusatz)


def _g11(bot, p, tabellen, krise):
    """Die Standard-Beispieldaten eines Bots, Falte fuer Falte: mindestens eine
    Krisenfalte unter den Selektionsfalten, nicht alle (sonst ist die
    Exposure konstant und der Zufalls-Timing-Test entartet), und der
    Standard-Drawdown besteht die Drawdown-Bedingung in jeder
    Selektionsfalte (sonst greift Abbruchkriterium (b) in jedem Lauf)."""
    sel = _selektionsfalten(p)
    if not krise or bot not in tabellen:
        return False, f"Krisenfalten {krise}, Tabelle {'da' if bot in tabellen else 'FEHLT'}"
    dd_fn, ex_fn = bd.standard_drawdown(krise), bd.standard_exposure(krise)
    expo = {f: ex_fn(None, None, f, None) for f in sel}
    reisst = []
    for f in sel:
        e = expo[f]
        grenze = bm.erlaubt(
            bm.nachschlagen(tabellen[bot]["falten"][f]["dd_benchmark"], e),
            bm.nachschlagen(tabellen[bot]["dd_toleranz"], e))
        if dd_fn(None, None, f, None) < grenze:
            reisst.append(f"{f} ({dd_fn(None, None, f, None):.2f} < {grenze:.2f})")
    ok = (set(krise) <= set(sel) and len(set(expo.values())) > 1
          and not reisst)
    return ok, f"Krisenfalten {krise}, Exposure {sorted(set(expo.values()))}, reisst {reisst}"


# ===========================================================================
# H  Mutationsproben - am Ablauf, nicht an einer gesetzten Variablen
# ===========================================================================
def _kopie(ziel):
    shutil.copytree(_HIER, ziel, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    return ziel


def _ersetze(pfad, alt, neu, mutieren=True):
    """Die Mutation. Mit `mutieren=False` die Gegenprobe (Register 40.7): die
    Stelle muss trotzdem existieren - sonst AssertionError wie bei der
    Mutation -, geschrieben wird aber nicht. So geht die Gegenprobe denselben
    Weg wie die Probe, nur ohne die Mutation."""
    with open(pfad, encoding="utf-8") as f:
        s = f.read()
    if alt not in s:
        raise AssertionError(f"Mutationsstelle nicht gefunden in {pfad}: {alt!r}")
    if not mutieren:
        return
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(s.replace(alt, neu, 1))


def _mit_gegenprobe(name, text, lauf, bedingung, zusatz=lambda r: ""):
    """Eine Mutationsprobe und ihre Gegenprobe (Register 40.7, Fable 24a):
    "Eine Mutationsprobe ohne Gegenprobe zaehlt nicht als Pruefung." Die Probe
    laeuft mit der Mutation und muss bestehen; dieselbe Probe laeuft ohne die
    Mutation und muss SCHEITERN - sonst besteht sie aus einem anderen Grund
    als der Mutation (wie F4 mit `<=`, bis TB-97). Bei jedem Lauf, nicht von
    Hand."""
    r = lauf(True)
    pruefe(f"{name}: {text}", bedingung(r), zusatz(r))
    g = lauf(False)
    pruefe(f"{name}-G: Gegenprobe zu {name} - ohne die Mutation scheitert sie",
           not bedingung(g), zusatz(g))


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


def _auswerten_in_kopie(roh, datei, alt, neu, mutieren):
    """Ordner kopieren, EINE Stelle mutieren (oder nicht), auswerten."""
    with tempfile.TemporaryDirectory() as m:
        _kopie(m)
        _ersetze(os.path.join(m, datei), alt, neu, mutieren)
        return _auswerten_in(m, roh)


def _grenzsaetze_in_kopie(mutationen):
    """Ordner kopieren, die Mutationen (datei, alt, neu, mutieren) anwenden,
    pruefe_grenzsaetze.py dort laufen lassen."""
    with tempfile.TemporaryDirectory() as m:
        _kopie(m)
        for datei, alt, neu, mutieren in mutationen:
            _ersetze(os.path.join(m, datei), alt, neu, mutieren)
        return subprocess.run([sys.executable, os.path.join(m, "pruefe_grenzsaetze.py")],
                              capture_output=True, text=True, env=_umgebung())


def _h3_lauf(mess, plan, ohne, mutieren=True):
    """Probe 3: dieselben Beispieldaten einmal mit, einmal ohne die Regel
    'Netto-Sharpe = 0 fuer Falten ohne Trade' auswerten. Eigene Funktion,
    damit die Gegenproben (ohne = leer; Mutation weggelassen) denselben Weg
    gehen."""
    with tempfile.TemporaryDirectory() as roh2, tempfile.TemporaryDirectory() as m:
        bd.erzeuge(roh2, BOT, mess=mess, plan=plan,
                   trades_fn=lambda w, i, f, a: 0 if f in ohne else 40,
                   sharpe_fn=lambda w, i, f, a: 9.0 if f in ohne else 0.10)
        vorher = _auswerten_in(_HIER, roh2)
        _kopie(m)
        _ersetze(os.path.join(m, "auswertung.py"),
                 'df["netto_sharpe"] = np.where(df["n_trades"].to_numpy() == 0, 0.0,\n'
                 '                                  df["netto_sharpe"].to_numpy(dtype=float))',
                 'df["netto_sharpe"] = df["netto_sharpe"].to_numpy(dtype=float)',
                 mutieren)
        nachher = _auswerten_in(m, roh2)
    return vorher, nachher


# Die Mutation von H5 ist Voraussetzung von H6: ohne die Live-Zahl im
# Grenzsatz waere "rc 0 ohne Wache 2" trivial (gemessen TB-97, A2).
_LIVE_ZAHL = ("registerdaten.py",
              '"Ein Stop enger als ein halbes Tages-Sigma des Universums wird vom "',
              '"Ein Stop enger als 8.0 Prozent wird vom "')
_OHNE_WACHE_2 = ("pruefe_grenzsaetze.py",
                 'treffer = zahlen_im_satz(g.get("satz")) & alle_live',
                 'treffer = set()')
_STUFUNG = ("registerdaten.py",
            '        "stufen": 4,\n        "unten": _grenze(\n'
            '            {"regel": "sigma_vielfaches", "zeitrahmen": zr, "faktor": 0.5},',
            '        "stufen": 3,\n        "unten": _grenze(\n'
            '            {"regel": "sigma_vielfaches", "zeitrahmen": zr, "faktor": 0.5},')


def teil_h():
    mess, plan = _mess(), _plan()
    achsen = aw.gitterachsen(BOT, mess)
    namen = sorted(achsen)
    spitze_idx = tuple(0 for _ in namen)

    def spitze_allein(werte, idx, falte, ach):
        return 3.0 if idx == spitze_idx else 0.30

    # Jede Probe steht mit ihrer Gegenprobe da (_mit_gegenprobe, Register
    # 40.7): mit der Mutation muss sie bestehen, ohne sie scheitern. Gemessen
    # in TB-97 (A1): sieben Code-Mutationen, H1-H7; H0 ist der Grundlauf.
    with tempfile.TemporaryDirectory() as roh:
        bd.erzeuge(roh, BOT, mess=mess, plan=plan, sharpe_fn=spitze_allein)
        original = _auswerten_in(_HIER, roh)
        pruefe("H0: der unveraenderte Ordner wertet aus",
               original.returncode == 0, original.stderr[-300:])

        # --- Probe 1: die Spitzen-Schwelle traegt wirklich ----------------
        _mit_gegenprobe(
            "H1", "eine verfaelschte Spitzen-Schwelle aendert das Urteil",
            lambda mut: _auswerten_in_kopie(
                roh, "registerdaten.py",
                "SPITZEN_SCHWELLE = 0.50", "SPITZEN_SCHWELLE = 99.0", mut),
            lambda r: r.returncode == 0 and ("Spitze" in original.stdout)
            != ("Spitze" in r.stdout))

        # --- Probe 2: das Plateau-Mittel zaehlt den Punkt mit -------------
        _mit_gegenprobe(
            "H2", "ohne den Punkt selbst faellt ein anderes Urteil",
            lambda mut: _auswerten_in_kopie(
                roh, "auswertung.py",
                'float(np.mean([s] + nachbar_werte))',
                'float(np.mean(nachbar_werte)) if nachbar_werte else float(s)', mut),
            lambda r: r.returncode == 0
            and _gewinnerzeile(r.stdout) != _gewinnerzeile(original.stdout),
            lambda r: f"{_gewinnerzeile(r.stdout)!r}")

        # --- Probe 3: die Null fuer Falten ohne Trade ist wirksam ---------
        # MEHR ALS DIE HAELFTE der Selektionsfalten ohne Trade, nicht eine:
        # die Selektionsstatistik ist ein MEDIAN und damit robust - erst eine
        # strikte Mehrheit gesetzter Nullen verschiebt ihn, bei gerader wie
        # ungerader Faltenzahl. Mit weniger aendert das Entfernen der Regel
        # nichts, und die Probe kann nicht zeigen, dass sie wirkt. (Dass der Median so
        # robust ist, steht auch im Register - es ist eine Eigenschaft von
        # Festlegung 2, kein Zufall dieses Tests.)
        # Namen UND Zahl kommen aus dem Plan des Bots (Fable 23a). Bis TB-95
        # standen hier vier Namen als Literale, begruendet mit "sieben Falten";
        # beim Plan von TB-95 (neun Selektionsfalten) sind es fuenf.
        sel = _selektionsfalten(plan[BOT])
        ohne = set(sel[:len(sel) // 2 + 1])

        def h3_bedingung(vn):
            vorher, nachher = vn
            return (vorher.returncode == 0 and nachher.returncode == 0
                    and _sharpezeile(vorher.stdout) != _sharpezeile(nachher.stdout))

        def h3_zusatz(vn):
            return (f"{_sharpezeile(vn[0].stdout)!r} / {_sharpezeile(vn[1].stdout)!r}"
                    f" - ohne Trade: {sorted(ohne)} von {sel}")

        _mit_gegenprobe(
            "H3", "ohne die gesetzte Null aendert sich die Statistik",
            lambda mut: _h3_lauf(mess, plan, ohne, mut), h3_bedingung, h3_zusatz)
        # Und die zweite Gegenprobe aus TB-95 (40.3), jetzt dauerhaft: mit
        # LEERER Menge - keine Falte ohne Trade - aendert die Mutation nichts.
        vn = _h3_lauf(mess, plan, set())
        pruefe("H3-L: Gegenprobe zu H3 - ohne Falte ohne Trade scheitert sie",
               not h3_bedingung(vn),
               f"{_sharpezeile(vn[0].stdout)!r} / {_sharpezeile(vn[1].stdout)!r}")

        # --- Probe 4: die Drawdown-Bedingung traegt ----------------------
        _mit_gegenprobe(
            "H4", "ein verfaelschter Drawdown-Faktor aendert die Zulaessigkeit",
            lambda mut: _auswerten_in_kopie(
                roh, "registerdaten.py",
                "DD_RELATIVER_FAKTOR = 1.25", "DD_RELATIVER_FAKTOR = 0.01", mut),
            lambda r: r.returncode == 0
            and _zulaessigzeile(r.stdout) != _zulaessigzeile(original.stdout),
            lambda r: f"{_zulaessigzeile(r.stdout)!r}")

    # --- Probe 5 und 6: die beiden Wachen decken sich NICHT gegenseitig --
    # 5a: ein Live-Wert im Grenzsatz wird gefunden ...
    _mit_gegenprobe(
        "H5", "eine Live-Zahl im Grenzsatz laesst die Pruefung scheitern",
        lambda mut: _grenzsaetze_in_kopie([_LIVE_ZAHL + (mut,)]),
        lambda r: r.returncode == 1 and "Live-Wert" in r.stdout,
        lambda r: r.stdout[-300:])
    # ... 5b: und ohne Wache 2 kaeme genau dieser Fehler DURCH. Die Live-Zahl
    # bleibt dabei immer eingesetzt; weggelassen wird nur H6s eigene Mutation.
    _mit_gegenprobe(
        "H6", "ohne Wache 2 bleibt derselbe Fehler unbemerkt - keine "
              "andere Wache faengt ihn auf",
        lambda mut: _grenzsaetze_in_kopie([_LIVE_ZAHL + (True,),
                                           _OHNE_WACHE_2 + (mut,)]),
        lambda r: r.returncode == 0,
        lambda r: r.stdout[-300:])

    # 6: eine verfaelschte Stufung wird von Wache 1/4 gefunden, und Wache 2
    #    faengt sie NICHT auf.
    _mit_gegenprobe(
        "H7", "eine Stufung ausserhalb 1,5 bis 2,0 faellt auf - und zwar "
              "mit genau dieser Begruendung",
        lambda mut: _grenzsaetze_in_kopie([_STUFUNG + (mut,)]),
        lambda r: r.returncode != 0
        and "ausserhalb 1,5 bis 2,0" in (r.stdout + r.stderr),
        lambda r: (r.stdout + r.stderr)[-300:])


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
