"""
Selbsttests des Rechenkerns - mit Gegenproben
==============================================================================
Nach Prinzip 12 des Uebergabeprotokolls ("eine gruene Pruefung ist erst dann
etwas wert, wenn belegt ist, dass sie auch rot werden kann") steht zu jeder
Behauptung eine Gegenprobe: ein zweiter Fall, in dem dieselbe Pruefung
anschlagen MUSS. Wo eine Kennzahl den Verdacht der Untersuchung traegt,
gibt es beide Richtungen - ein flaches Buch UND ein dauerhaft volles.

    python3 test_exposure_kern.py
"""

import sys

import pandas as pd

import exposure_kern as ek

FEHLER = []


def pruefe(bedingung, text):
    if bedingung:
        print(f"  ok    {text}")
    else:
        print(f"  FEHLT {text}")
        FEHLER.append(text)


def positionen(zeilen):
    """zeilen: (entry, exit, allocation, pnl_pct, capital_after)"""
    return pd.DataFrame(zeilen, columns=["entry_time", "exit_time", "allocation",
                                          "pnl_pct", "capital_after"])


# ---------------------------------------------------------------------------
print("\n1. Tagesreihe: offene Tage einschliesslich Ein- und Ausstiegstag")
# ---------------------------------------------------------------------------
p = positionen([("2020-01-01", "2020-01-03", 1000.0, 10.0, 10100.0)])
r = ek.taegliche_reihen(p, 10_000.0)

pruefe(list(r["n_offen"]) == [1, 1, 1], "drei Tage offen (01., 02., 03.)")
pruefe(list(r["gebunden"]) == [1000.0, 1000.0, 1000.0], "je 1000 gebunden")
pruefe(list(ek.exposure_reihe(r).round(4)) == [0.1, 0.1, 0.1],
       "Exposure 10 % an allen drei Tagen")
pruefe(list(r["kapital_start"]) == [10_000.0, 10_000.0, 10_000.0],
       "Nenner ist das Kapital zu Tagesbeginn, nicht der Stand nach dem Ausstieg")
pruefe(r["kapital_ende"].iloc[-1] == 10_100.0, "Tagesende des Ausstiegstags ist 10.100")

# Gegenprobe: eine Position, die an EINEM Tag ein- und aussteigt, darf nicht
# als zwei Tage zaehlen - und eine laengere nicht als kuerzere.
r1 = ek.taegliche_reihen(positionen([("2020-01-01", "2020-01-01", 500.0, 0.0, 10_000.0)]),
                          10_000.0)
pruefe(list(r1["n_offen"]) == [1], "Gegenprobe: Ein-Tages-Position zaehlt genau einen Tag")
r5 = ek.taegliche_reihen(positionen([("2020-01-01", "2020-01-05", 500.0, 0.0, 10_000.0)]),
                          10_000.0)
pruefe(int(r5["n_offen"].sum()) == 5, "Gegenprobe: Fuenf-Tages-Position zaehlt fuenf Tage")

# ---------------------------------------------------------------------------
print("\n2. Gleichgewichtung: ein flacher Bot halbiert die Exposure")
# ---------------------------------------------------------------------------
aktiv = ek.taegliche_reihen(
    positionen([("2020-01-01", "2020-01-10", 10_000.0, 0.0, 10_000.0)]), 10_000.0)
flach = ek.taegliche_reihen(
    positionen([("2020-01-01", "2020-01-01", 0.0, 0.0, 10_000.0),
                ("2020-01-10", "2020-01-10", 0.0, 0.0, 10_000.0)]), 10_000.0)

einzeln = ek.kombiniere({"a": aktiv})
zusammen = ek.kombiniere({"a": aktiv, "b": flach})
pruefe(round(einzeln["exposure"].mean(), 6) == 1.0, "ein voll investierter Bot: 100 %")
pruefe(round(zusammen["exposure"].mean(), 6) == 0.5,
       "Gegenprobe: derselbe Bot neben einem flachen: 50 %")

# Das gemeinsame Fenster ist die SCHNITTMENGE - ein Bot mit kurzer Historie
# verkuerzt die Messung fuer alle. Diese Eigenschaft ist im Bericht eine der
# genannten Grenzen und wird deshalb hier festgehalten.
frueh = ek.taegliche_reihen(
    positionen([("2020-01-01", "2020-01-10", 1000.0, 0.0, 10_000.0)]), 10_000.0)
spaet = ek.taegliche_reihen(
    positionen([("2020-01-05", "2020-01-20", 1000.0, 0.0, 10_000.0)]), 10_000.0)
gemischt = ek.kombiniere({"frueh": frueh, "spaet": spaet})
pruefe(str(gemischt.index.min().date()) == "2020-01-05"
       and str(gemischt.index.max().date()) == "2020-01-10",
       "gemeinsames Fenster ist die Schnittmenge (05.-10.), nicht die Vereinigung")

# ---------------------------------------------------------------------------
print("\n3. Max Drawdown")
# ---------------------------------------------------------------------------
pruefe(round(ek.max_drawdown_pct(pd.Series([100, 110, 88, 120])), 2) == -20.0,
       "110 -> 88 sind -20 %")
pruefe(ek.max_drawdown_pct(pd.Series([100, 101, 102])) == 0.0,
       "Gegenprobe: eine nur steigende Kurve hat keinen Drawdown")

# ---------------------------------------------------------------------------
print("\n4. Der Kern der Untersuchung: Gesamtkapital gegen investiertes Kapital")
# ---------------------------------------------------------------------------
# Ein Buch, das zu 10 % investiert ist und auf diesen 10 % ein Fuenftel
# verliert: am Gesamtkapital sind das -2 %, am eingesetzten Kapital -20 %.
kombi = pd.DataFrame({
    "kapital_start": [100.0, 100.0, 98.0],
    "kapital_ende": [100.0, 98.0, 98.0],
    "gebunden": [10.0, 10.0, 0.0],
    "n_offen": [1, 1, 0],
}, index=pd.date_range("2020-01-01", periods=3, freq="D"))
kombi["exposure"] = kombi["gebunden"] / kombi["kapital_start"]

gesamt_dd = ek.max_drawdown_pct(kombi["kapital_ende"])
invest = ek.drawdown_auf_investiertem_kapital(kombi)
pruefe(round(gesamt_dd, 2) == -2.0, "am Gesamtkapital gemessen: -2 %")
pruefe(invest["max_drawdown_pct"] == -20.0, "am eingesetzten Kapital gemessen: -20 %")
pruefe(invest["aktive_tage"] == 2, "der flache Tag kommt in der zweiten Kurve nicht vor")

# Gegenprobe - genau der Fall, den die Untersuchung NICHT findet, wenn der
# Verdacht falsch ist: ein dauerhaft voll investiertes Buch. Dann muessen
# beide Zahlen zusammenfallen.
voll = pd.DataFrame({
    "kapital_start": [100.0, 100.0, 80.0],
    "kapital_ende": [100.0, 80.0, 80.0],
    "gebunden": [100.0, 100.0, 80.0],
    "n_offen": [1, 1, 1],
}, index=pd.date_range("2020-01-01", periods=3, freq="D"))
voll["exposure"] = voll["gebunden"] / voll["kapital_start"]
pruefe(round(ek.max_drawdown_pct(voll["kapital_ende"]), 2) == -20.0
       and ek.drawdown_auf_investiertem_kapital(voll)["max_drawdown_pct"] == -20.0,
       "Gegenprobe: bei 100 % Exposure sagen beide Masse dasselbe")

# ---------------------------------------------------------------------------
print("\n5. Exposure-Kennzahlen")
# ---------------------------------------------------------------------------
exp = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.8])
off = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
k = ek.exposure_kennzahlen(exp, off)
pruefe(k["mittel_pct"] == 14.0, "Mittel 14 %")
pruefe(k["median_pct"] == 0.0, "Median 0 % - ein flaches Buch faellt im Mittel nicht auf")
pruefe(k["anteil_tage_flach_pct"] == 80.0, "80 % der Tage ohne Position")
pruefe(k["anteil_tage_ueber_50_pct"] == 20.0, "20 % der Tage ueber 50 %")

# ---------------------------------------------------------------------------
print("\n6. Buy-and-Hold-Referenz vertraegt Kursluecken")
# ---------------------------------------------------------------------------
tage = pd.date_range("2020-01-01", periods=4, freq="D")
kurse = {
    "GUT": pd.Series([100.0, 110.0, 99.0, 99.0], index=tage),
    "LUECKE": pd.Series([100.0, float("nan"), 100.0, 100.0], index=tage),
}
r_bh = ek.bh_tagesrenditen(kurse)
pruefe(not r_bh.isna().any(), "eine Luecke macht die Gesamtreihe nicht zu NaN")
pruefe(round(float(r_bh.iloc[0]), 4) == 0.10,
       "am Tag mit nur einem gueltigen Kurs zaehlt dieser allein (+10 %)")

schlecht = ek.schlechteste_tage(pd.Series([0.05, -0.10, 0.01, 0.02, 0.0,
                                            0.03, -0.02, 0.04, 0.06, 0.07]), 0.10)
pruefe(len(schlecht) == 1 and schlecht[0] == 1,
       "die 10 % schlechtesten Tage von zehn Tagen sind genau einer")

# ---------------------------------------------------------------------------
print()
if FEHLER:
    print(f"{len(FEHLER)} Pruefung(en) fehlgeschlagen.")
    sys.exit(1)
print("Alle Pruefungen bestanden.")
