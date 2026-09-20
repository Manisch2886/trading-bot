#!/usr/bin/env python3
"""
TB-73 Schritt 2 - Die Proben, die beissen koennen (Prueffrage B1)
==============================================================================
Bevor irgendeine Zahl aus Schritt 3 gilt, muss der Pfad zwei Proben bestehen
(Auftrag, Schritt 2). Schlaegt eine fehl, ist der Pfad falsch.

  Probe 1  Ein Bot, dessen Positionen ALLE innerhalb eines Tages geschlossen
           werden: E und M muessen gleich sein - gibt es keinen
           unrealisierten Verlust, gibt es keinen Unterschied.
           Genommen wird die echte TB-24-Liste von `t3_supertrend` (4h-Bot,
           656 Positionen, Kerzenbeginn 00/04/.../20 Uhr), jeder Ausstieg auf
           Einstieg + 1 h gesetzt, `pnl_pct` unveraendert, Kapitalkette neu
           in Ausstiegsreihenfolge geschlossen.
             1a  hoechstens EIN Ausstieg je Tag (Liste ausgeduennt):
                 E = E_tag = M in jeder Falte, auf die zweite Stelle genau.
             1b  alle 656 Positionen (mehrere Ausstiege je Tag):
                 E_tag = M in jeder Falte (kein unrealisierter Wert),
                 und E ist nie flacher als E_tag - E hat die feineren
                 Stuetzstellen, jeder Tagesendwert ist auch ein E-Punkt.
                 Der Unterschied E gegen E_tag ist der Raster-Effekt allein.

  Probe 2  Eine einzelne Position von Hand: Einstand 100, Tagesschluesse
           100 / 90 / 80 / 95, Ausstieg am fuenften Tag zu 105, Allokation
           2000 auf 10 000, Kosten 0,15 % je Seite (pnl_pct = 5 - 0,3 = 4,7).
           M muss den Zwischenverlust zeigen, E nicht:
             Tagespfad M: 9 997 / 9 797 / 9 597 / 9 897 / 10 094
             E = 0,00 (10 000 -> 10 094), E_tag = 0,00, M = -4,03.

  Probe 3  (Zusatz dieser Sitzung, nicht im Auftrag) Zwei Positionen von
           Hand, die zeigen, dass "M nie flacher als E" KEIN Satz der
           Rechnung ist: A liegt mit +20 % unrealisiert im Buch, waehrend B
           mit -10 % realisiert schliesst. E faellt von 10 000 auf 9 900
           (-1,00 %); M faellt von 10 200 auf 10 100 (-0,98 %) - der
           unrealisierte Gewinn in A hebt den Hoechststand UND den Tiefpunkt.
           Findet Schritt 3 Falten, in denen M flacher ist als E, ist das
           dieser Mechanismus (oder Probe 1b's Raster-Effekt) - und wird als
           Fall benannt, nicht geglaettet (Auftrag, Schritt 3).

Dazu zwei Gegenproben am Kern selbst (Prinzip 12):
  K1  `ereignisreihenfolge` rekonstruiert eine bekannte, absichtlich
      vertauschte Reihenfolge bei gleichem Zeitstempel und bricht ab, wenn
      die Kette nicht schliesst.
  K2  `mtm_pfad` bricht ab, wenn einer offenen Position der Kurs fehlt -
      statt zu raten.

    trading-env/bin/python3 research/mtm_drawdown/test_mtm_kern.py

Liest research/tb24_haltedauern/daten/t3_supertrend_*.{csv,json} und
data/*USDT_1d.csv; schreibt nichts. Rueckgabewert 0, wenn alle Proben
bestehen, sonst 1.
"""

import json
import os
import sys
import time

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, _HIER)
sys.path.insert(0, os.path.join(REPO_ROOT, "shared"))

import mtm_kern                                            # noqa: E402
import grundlage                                           # noqa: E402
from messkette import max_drawdown_ungerundet, calculate_max_drawdown  # noqa: E402

BEFUNDE = []


def pruefe(bedingung: bool, text: str):
    marke = "bestanden " if bedingung else "GESCHEITERT"
    print(f"  [{marke}] {text}")
    BEFUNDE.append(bool(bedingung))


def kette_schliessen(pos: pd.DataFrame, startkapital: float) -> pd.DataFrame:
    """Kapitalkette in Ausstiegsreihenfolge neu schliessen (fuer synthetische
    Listen, deren Ausstiege verschoben wurden). Bei gleichem Zeitstempel gilt
    die Zeilenreihenfolge - fuer Probe 1 ist sie bedeutungslos, weil dort nur
    E_tag/M verglichen werden, die die Reihenfolge nicht sehen (1b), bzw. es
    nur einen Ausstieg je Tag gibt (1a)."""
    pos = pos.sort_values("exit_time", kind="stable").reset_index(drop=True)
    kapital = float(startkapital)
    stand = []
    for a, p in zip(pos["allocation"], pos["pnl_pct"]):
        kapital += a * p / 100.0
        stand.append(round(kapital, 2))
    pos["capital_after"] = stand
    return pos


def falten_von(bot: str):
    return grundlage.lade_falten(bot)


def messe(pos: pd.DataFrame, kurse_je_symbol: dict, falten, startkapital, kosten_seite):
    ereignisse = mtm_kern.ereignisreihenfolge(pos, startkapital)
    kurve = mtm_kern.ereigniskurve(ereignisse)
    von = min(pd.Timestamp(f["von"]) for f in falten)
    bis = max(pd.Timestamp(f["bis_ausschliesslich"]) for f in falten)
    tage = mtm_kern.tagesraster(kurse_je_symbol, von=min(von, ereignisse["entry_time"].min().normalize()),
                                bis=max(bis, ereignisse["exit_time"].max().normalize() + mtm_kern.EIN_TAG))
    kurse, fort = mtm_kern.kurse_auf_raster(kurse_je_symbol, tage)
    pfad = mtm_kern.mtm_pfad(ereignisse, kurse, fort, startkapital, kosten_seite)
    return mtm_kern.messe_falten(kurve, pfad, falten, startkapital, max_drawdown_ungerundet), pfad, kurve


# ---------------------------------------------------------------------------
# Probe 1
# ---------------------------------------------------------------------------

def probe_1():
    print("Probe 1 - alle Positionen innerhalb eines Tages geschlossen (t3_supertrend, Ausstieg = Einstieg + 1 h)")
    pos, meta, grund = grundlage.lade_positionen("t3_supertrend")
    assert pos is not None, grund
    startkapital = float(meta["startkapital"])
    kurse = grundlage.lade_schlusskurse(pos["symbol"].unique(), "1d")
    falten = [f for f in falten_von("t3_supertrend")]

    synth = pos.copy()
    synth["exit_time"] = synth["entry_time"] + pd.Timedelta(hours=1)
    pruefe((synth["exit_time"].dt.normalize() == synth["entry_time"].dt.normalize()).all(),
           "Vorbedingung: jeder Ausstieg liegt am Tag seines Einstiegs")

    # 1a - hoechstens ein Ausstieg je Tag
    einer = synth.loc[~synth["exit_time"].dt.normalize().duplicated(keep="first")].copy()
    einer = kette_schliessen(einer, startkapital)
    m1a, pfad1a, kurve1a = messe(einer, kurse, falten, startkapital, kosten_seite=0.15)
    print(f"  1a: {len(einer)} Positionen an {einer['exit_time'].dt.normalize().nunique()} Tagen")
    for z in m1a:
        print(f"      {z['falte']:>9}  E {z['E']:>7.2f}  E_tag {z['E_tag']:>7.2f}  M {z['M']:>7.2f}  "
              f"(Ausstiege {z['n_ausstiege']})")
    pruefe(all(abs(z["E"] - z["M"]) < 1e-9 for z in m1a), "1a: E = M in jeder Falte")
    pruefe(all(abs(z["E_tag"] - z["M"]) < 1e-9 for z in m1a), "1a: E_tag = M in jeder Falte")
    pruefe((pfad1a["n_offen"] == 0).all(), "1a: an keinem Tagesschluss eine offene Position")
    pruefe(any(z["E"] < 0 for z in m1a), "1a: die Probe ist nicht leer - mindestens eine Falte mit Drawdown < 0")
    # Der Gesamt-Drawdown der Ereigniskurve ueber die importierte Bot-Funktion
    ges_e = calculate_max_drawdown(pd.DataFrame({"capital_after": kurve1a.to_numpy()}), startkapital)
    ges_m = mtm_kern.drawdown_falte(pfad1a["mtm"], startkapital, max_drawdown_ungerundet)
    pruefe(abs(ges_e - ges_m) < 1e-9, f"1a: Gesamt-Drawdown E (calculate_max_drawdown) {ges_e} = M {ges_m}")

    # 1b - alle Positionen, mehrere Ausstiege je Tag
    alle = kette_schliessen(synth, startkapital)
    m1b, pfad1b, kurve1b = messe(alle, kurse, falten, startkapital, kosten_seite=0.15)
    print(f"  1b: {len(alle)} Positionen an {alle['exit_time'].dt.normalize().nunique()} Tagen")
    for z in m1b:
        print(f"      {z['falte']:>9}  E {z['E']:>7.2f}  E_tag {z['E_tag']:>7.2f}  M {z['M']:>7.2f}  "
              f"(Ausstiege {z['n_ausstiege']})")
    pruefe(all(abs(z["E_tag"] - z["M"]) < 1e-9 for z in m1b), "1b: E_tag = M in jeder Falte")
    pruefe((pfad1b["n_offen"] == 0).all(), "1b: an keinem Tagesschluss eine offene Position")
    pruefe(all(z["E"] <= z["E_tag"] + 1e-9 for z in m1b), "1b: E nie flacher als E_tag (feineres Raster)")
    pruefe(any(z["E"] < z["E_tag"] - 1e-9 for z in m1b),
           "1b: der Raster-Effekt ist sichtbar - mindestens eine Falte mit E tiefer als E_tag")


# ---------------------------------------------------------------------------
# Probe 2
# ---------------------------------------------------------------------------

def probe_2():
    print("Probe 2 - eine Position von Hand")
    tage = pd.date_range("2020-01-01", periods=5, freq="D")
    kurse = {"X": pd.Series([100.0, 90.0, 80.0, 95.0, 105.0], index=tage)}
    kosten_seite = 0.15
    pnl = (105.0 / 100.0 - 1.0) * 100.0 - 2 * kosten_seite      # 4.7
    pos = pd.DataFrame([{
        "symbol": "X", "entry_time": tage[0], "exit_time": tage[4],
        "entry_price": 100.0, "exit_price": 105.0, "pnl_pct": pnl,
        "allocation": 2000.0, "capital_after": 10_000.0 + 2000.0 * pnl / 100.0,
    }])
    falten = [{"name": "2020", "rolle": "selektion", "von": "2020-01-01", "bis_ausschliesslich": "2021-01-01"}]
    m, pfad, kurve = messe(pos, kurse, falten, 10_000.0, kosten_seite)
    erwartet = [9997.0, 9797.0, 9597.0, 9897.0, 10094.0]
    print("  Tagespfad M:", [round(x, 2) for x in pfad["mtm"].tolist()], "erwartet", erwartet)
    print("  Tagespfad E_tag:", [round(x, 2) for x in pfad["buch"].tolist()])
    z = m[0]
    print(f"  E {z['E']}  E_tag {z['E_tag']}  M {z['M']}")
    pruefe(np.allclose(pfad["mtm"].to_numpy(), erwartet, atol=1e-9), "2: Tagespfad M = Handrechnung")
    pruefe(np.allclose(pfad["buch"].to_numpy(), [10000.0] * 4 + [10094.0], atol=1e-9), "2: Tagespfad E_tag = Handrechnung")
    pruefe(z["E"] == 0.0, "2: E = 0,00 - die Ereigniskurve sieht den Zwischenverlust nicht")
    pruefe(z["E_tag"] == 0.0, "2: E_tag = 0,00")
    pruefe(z["M"] == -4.03, f"2: M = -4,03 (gemessen {z['M']}) - der bekannte Zwischenverlust")
    pruefe(pfad["n_offen"].tolist() == [1, 1, 1, 1, 0], "2: offen an den Schluessen der Tage 1-4, nicht am Ausstiegstag")
    pruefe(z["max_unrealisiert_minus"] == -403.0, "2: groesster unrealisierter Verlust -403")


# ---------------------------------------------------------------------------
# Probe 3 (Zusatz)
# ---------------------------------------------------------------------------

def probe_3():
    print("Probe 3 (Zusatz) - unrealisierter Gewinn in A, realisierter Verlust in B")
    tage = pd.date_range("2020-01-01", periods=5, freq="D")
    kurse = {"A": pd.Series([100.0, 120.0, 120.0, 120.0, 120.0], index=tage),
             "B": pd.Series([50.0, 50.0, 45.0, 45.0, 45.0], index=tage)}
    pos = pd.DataFrame([
        {"symbol": "A", "entry_time": tage[0], "exit_time": tage[4], "entry_price": 100.0,
         "exit_price": 120.0, "pnl_pct": 20.0, "allocation": 1000.0, "capital_after": 10_100.0},
        {"symbol": "B", "entry_time": tage[1], "exit_time": tage[2], "entry_price": 50.0,
         "exit_price": 45.0, "pnl_pct": -10.0, "allocation": 1000.0, "capital_after": 9_900.0},
    ])
    falten = [{"name": "2020", "rolle": "selektion", "von": "2020-01-01", "bis_ausschliesslich": "2021-01-01"}]
    m, pfad, kurve = messe(pos, kurse, falten, 10_000.0, 0.0)
    z = m[0]
    print("  Tagespfad M:", [round(x, 2) for x in pfad["mtm"].tolist()], "erwartet [10000, 10200, 10100, 10100, 10100]")
    print(f"  E {z['E']}  E_tag {z['E_tag']}  M {z['M']}  M_flacher_als_E {z['M_flacher_als_E']}")
    pruefe(np.allclose(pfad["mtm"].to_numpy(), [10000.0, 10200.0, 10100.0, 10100.0, 10100.0]), "3: Tagespfad M = Handrechnung")
    pruefe(z["E"] == -1.0 and z["E_tag"] == -1.0, "3: E = E_tag = -1,00")
    pruefe(z["M"] == -0.98, f"3: M = -0,98 (gemessen {z['M']}) - flacher als E, wie von Hand gerechnet")
    pruefe(z["M_flacher_als_E"] is True, "3: der Kern meldet den Fall (M_flacher_als_E)")


# ---------------------------------------------------------------------------
# Gegenproben am Kern
# ---------------------------------------------------------------------------

def gegenproben():
    print("Gegenproben am Kern")
    t = pd.Timestamp("2020-03-03")
    # Zwei Ausstiege zum selben Zeitstempel; die Kette sagt: erst -5 %, dann +2 %.
    pos = pd.DataFrame([
        {"symbol": "P", "entry_time": t - pd.Timedelta(days=2), "exit_time": t, "entry_price": 1.0,
         "exit_price": 1.0, "pnl_pct": 2.0, "allocation": 1000.0, "capital_after": 9970.0},
        {"symbol": "Q", "entry_time": t - pd.Timedelta(days=1), "exit_time": t, "entry_price": 1.0,
         "exit_price": 1.0, "pnl_pct": -5.0, "allocation": 1000.0, "capital_after": 9950.0},
    ])
    e = mtm_kern.ereignisreihenfolge(pos, 10_000.0)
    pruefe(e["symbol"].tolist() == ["Q", "P"], "K1: Reihenfolge aus der Kette rekonstruiert (Q vor P)")
    kaputt = pos.copy()
    kaputt.loc[0, "capital_after"] = 9971.0   # schliesst nicht mehr (Toleranz 0,02)
    try:
        mtm_kern.ereignisreihenfolge(kaputt, 10_000.0)
        pruefe(False, "K1: Kette, die nicht schliesst, wird erkannt")
    except ValueError:
        pruefe(True, "K1: Kette, die nicht schliesst, wird erkannt (ValueError)")

    tage = pd.date_range("2020-03-01", periods=4, freq="D")
    kurse = {"P": pd.Series([1.0, 1.0, 1.0, 1.0], index=tage),
             "Q": pd.Series([np.nan, np.nan, 1.0, 1.0], index=tage)}   # Q hat vor dem 3.3. keinen Kurs
    k, f = mtm_kern.kurse_auf_raster(kurse, tage)
    try:
        mtm_kern.mtm_pfad(e, k, f, 10_000.0, 0.0)
        pruefe(False, "K2: fehlender Kurs einer offenen Position bricht ab")
    except ValueError:
        pruefe(True, "K2: fehlender Kurs einer offenen Position bricht ab (ValueError)")


def main():
    t0 = time.time()
    for probe in (probe_1, probe_2, probe_3, gegenproben):
        probe()
        print()
    n = len(BEFUNDE)
    ok = sum(BEFUNDE)
    print(f"{ok} von {n} Pruefungen bestanden, {n - ok} gescheitert, Laufzeit {time.time() - t0:.1f} s")
    return 0 if ok == n else 1


if __name__ == "__main__":
    sys.exit(main())
