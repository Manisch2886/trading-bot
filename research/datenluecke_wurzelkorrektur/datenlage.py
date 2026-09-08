"""
Wie oft ist der letzte Balken tatsaechlich unvollstaendig?
==============================================================
Durchsucht alle gespeicherten Aktien-Tagesdateien nach Balken mit
fehlenden OHLC-Werten und prueft ausserdem, ob der jeweils letzte Balken
ueberhaupt nach einem ABGESCHLOSSENEN Handelstag aussieht.

Der zweite Teil ist der eigentliche Trick dieser Untersuchung: ob ein
gespeicherter Balken ein noch laufender Handelstag war, sieht man ihm
nicht direkt an - wohl aber seinem VOLUMEN. Ein waehrend der Sitzung
abgerufener Balken traegt nur einen Bruchteil des Tagesvolumens. Liegt das
Volumen des letzten Balkens dagegen im ueblichen Bereich der Vortage, war
der Handelstag beim Abruf abgeschlossen.

Rein lesend; veraendert keine Datei ausserhalb dieses Verzeichnisses.

Nutzung:  python3 datenlage.py
"""

import glob
import json
import os

import numpy as np
import pandas as pd

DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(DIR))
DATA_DIR = os.path.join(REPO, "data")
RESULTS_DIR = os.path.join(DIR, "results")

PREIS = ["open", "high", "low", "close"]
VERGLEICHSTAGE = 20   # Median der Vortage als Massstab fuer "uebliches Volumen"


def aktien_dateien() -> list:
    """Alle Tages-CSVs ausser den Krypto-Paaren (die tragen USDT im Namen
    und handeln ohnehin rund um die Uhr - die Frage nach dem Boersenschluss
    stellt sich dort nicht)."""
    return [f for f in sorted(glob.glob(os.path.join(DATA_DIR, "*_1d.csv")))
            if "USDT" not in os.path.basename(f)]


def auswerten() -> dict:
    luecken = []
    letzte_daten = {}
    volumen_verhaeltnis = {}
    balken_gesamt = 0

    for pfad in aktien_dateien():
        symbol = os.path.basename(pfad).replace("_1d.csv", "")
        df = pd.read_csv(pfad, parse_dates=["open_time"])
        if df.empty:
            continue
        balken_gesamt += len(df)

        letzter = df["open_time"].max()
        letzte_daten[str(letzter.date())] = letzte_daten.get(str(letzter.date()), 0) + 1

        fehlend = df[df[PREIS].isna().any(axis=1)]
        for _, zeile in fehlend.iterrows():
            luecken.append({
                "symbol": symbol,
                "datum": str(zeile["open_time"].date()),
                "ist_letzter_balken": bool(zeile["open_time"] == letzter),
                "alle_preise_fehlen": bool(df.loc[zeile.name, PREIS].isna().all()),
                "volumen": None if pd.isna(zeile["volume"]) else float(zeile["volume"]),
            })

        if len(df) > VERGLEICHSTAGE + 1:
            median_vortage = df["volume"].iloc[-(VERGLEICHSTAGE + 1):-1].median()
            if median_vortage and median_vortage > 0:
                volumen_verhaeltnis[symbol] = float(df["volume"].iloc[-1] / median_vortage)

    werte = np.array(list(volumen_verhaeltnis.values()))
    return {
        "dateien": len(aktien_dateien()),
        "balken_gesamt": balken_gesamt,
        "luecken": luecken,
        "luecken_anteil_prozent": round(len(luecken) / max(balken_gesamt, 1) * 100, 6),
        "letzter_balken_je_datum": letzte_daten,
        "volumen_des_letzten_balkens_zum_median_der_vortage": {
            "symbole": int(werte.size),
            "median": round(float(np.median(werte)), 3),
            "p05": round(float(np.percentile(werte, 5)), 3),
            "p95": round(float(np.percentile(werte, 95)), 3),
            "minimum": round(float(werte.min()), 3),
            "anteil_unter_0_5": round(float((werte < 0.5).mean() * 100), 2),
        },
    }


if __name__ == "__main__":
    e = auswerten()
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "datenlage.json"), "w") as fh:
        json.dump(e, fh, indent=1, ensure_ascii=False)

    print(f"Aktien-Tagesdateien: {e['dateien']}, Balken insgesamt: {e['balken_gesamt']:,}\n")

    print(f"Balken mit fehlenden Preisen: {len(e['luecken'])} "
          f"({e['luecken_anteil_prozent']} % aller Balken)")
    for l in e["luecken"]:
        print(f"  {l['symbol']:6} {l['datum']}  letzter Balken: {l['ist_letzter_balken']}, "
              f"alle Preise fehlen: {l['alle_preise_fehlen']}, Volumen: {l['volumen']:,.0f}")

    print("\nLetzter Balken je Datei:")
    for datum, n in sorted(e["letzter_balken_je_datum"].items()):
        print(f"  {datum}: {n} Dateien")

    v = e["volumen_des_letzten_balkens_zum_median_der_vortage"]
    print(f"\nVolumen des letzten Balkens im Verhaeltnis zum Median der {VERGLEICHSTAGE} Vortage:")
    print(f"  Median ueber {v['symbole']} Symbole: {v['median']}   "
          f"(5 %-Quantil {v['p05']}, 95 %-Quantil {v['p95']}, Minimum {v['minimum']})")
    print(f"  Anteil unter 0,5: {v['anteil_unter_0_5']} %")
    print("\n  Lesart: Werte um 1,0 bedeuten volles Tagesvolumen - der Handelstag war")
    print("  beim Abruf abgeschlossen. Ein waehrend der Sitzung abgerufener Balken")
    print("  laege deutlich darunter.")
