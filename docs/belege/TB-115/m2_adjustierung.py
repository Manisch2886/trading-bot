#!/usr/bin/env python3
"""TB-115 M2 (a)/(b) - Herkunft und Adjustierungsstand der Aktienreihen im
Snapshot. Rein lesend; nur Kursdateien des Snapshots und Git-Objekte.
Keine Bot-Logik, kein Selektionsskript, kein Ergebniswert.

(a) Zaehlung: *_1d.csv im Snapshot, davon Krypto (Endung USDT) und Aktien;
    Abgleich mit config/sp500_top150.txt des Snapshots.
(b1) Spaltenkoepfe: gibt es 'Adj Close' neben 'close'?
(b2) Split-Stichprobe: Schlusskurs am Handelstag VOR und AM Split-Tag
     (erster Handelstag nach dem Split). Die Split-Tage und -Faktoren sind
     oeffentlich bekannt und stehen hier als Literal; sie stammen NICHT aus dem
     Repo. Unbereinigt waere der Quotient nahe 1/Faktor, bereinigt nahe 1.
(b3) Dividenden: yfinance liefert Kurse als float32; ein UNbereinigter Kurs
     ist dann float32(zweistelliger Dezimalwert) - "sauber". Ein mit einem
     Faktor multiplizierter Kurs ist das (bis auf Zufall) nicht mehr.
     Die LETZTE unsaubere Zeile markiert damit den letzten Bereinigungsschnitt:
       - nur Split-bereinigt  -> Schnitt am Tag vor dem letzten Split
       - auch Dividenden      -> Schnitt am Tag vor dem letzten Ex-Tag
     Gezaehlt wird je Datei: Datum der letzten unsauberen Zeile, Anteil
     sauberer Zeilen danach (Soll 100 %) und davor.

Aufruf aus der Repo-Wurzel: python3 docs/belege/TB-115/m2_adjustierung.py
"""
import collections
import csv
import os
import sys

SNAP = "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
EPS32 = 1.1920929e-07

# (Symbol, erster Handelstag nach dem Split, Faktor) - oeffentlich bekannt.
SPLITS = [("AAPL", "2020-08-31", 4), ("NVDA", "2024-06-10", 10),
          ("TSLA", "2022-08-25", 3), ("AMZN", "2022-06-06", 20),
          ("GOOGL", "2022-07-18", 20), ("WMT", "2024-02-26", 3),
          ("AVGO", "2024-07-15", 10), ("BRK-B", "2010-01-21", 50)]


def reihe(symbol):
    with open(os.path.join(SNAP, f"{symbol}_1d.csv"), newline="") as d:
        r = csv.reader(d)
        kopf = next(r)
        i_t, i_c = kopf.index("open_time"), kopf.index("close")
        zeilen = []
        for z in r:
            if z[i_c] == "":
                continue            # Kerze ohne Kurs (APH-Fall), zaehlt nicht
            zeilen.append((z[i_t][:10], float(z[i_c])))
    return kopf, zeilen


def sauber(x):
    return abs(x - round(x, 2)) <= 2 * EPS32 * max(abs(x), 1.0)


def main():
    namen = sorted(n for n in os.listdir(SNAP) if n.endswith("_1d.csv"))
    krypto = [n for n in namen if n[:-7].endswith("USDT")]
    aktien = [n[:-7] for n in namen if not n[:-7].endswith("USDT")]
    with open(os.path.join(SNAP, "config", "sp500_top150.txt")) as d:
        liste = [z.strip() for z in d if z.strip()]
    print("# TB-115 M2 (a)/(b) - Aktienreihen im Snapshot")
    print(f"(a) *_1d.csv: {len(namen)}, davon Krypto {len(krypto)}, Aktien "
          f"{len(aktien)}; config/sp500_top150.txt: {len(liste)} Zeilen; "
          f"Menge gleich: {set(aktien) == set(liste)}")

    koepfe = collections.Counter()
    for s in aktien:
        koepfe[",".join(reihe(s)[0])] += 1
    print(f"(b1) Spaltenkoepfe der {len(aktien)} Aktiendateien: {dict(koepfe)}")
    print(f"     'Adj Close' vorhanden: "
          f"{any('adj' in k.lower() for k in koepfe)}")

    print("(b2) Split-Stichprobe (Schluss am Vortag / am Split-Tag):")
    for s, tag, faktor in SPLITS:
        if s not in aktien:
            print(f"     {s:<6} nicht im Universum")
            continue
        _k, z = reihe(s)
        tage = [t for t, _c in z]
        if tag not in tage:
            print(f"     {s:<6} Split-Tag {tag} nicht in der Reihe")
            continue
        i = tage.index(tag)
        vor, am = z[i - 1], z[i]
        q = am[1] / vor[1]
        urteil = ("BEREINIGT" if abs(q - 1) < 0.25 else
                  "UNBEREINIGT" if abs(q * faktor - 1) < 0.25 else "unklar")
        print(f"     {s:<6} {faktor:>2}:1  {vor[0]} {vor[1]:>12.6f}  ->  "
              f"{am[0]} {am[1]:>12.6f}   Quotient {q:.4f}  "
              f"(unbereinigt erwartet ~{1 / faktor:.4f})  {urteil}")

    print("(b3) letzte unsaubere Zeile je Datei (= letzter Bereinigungsschnitt):")
    schnitte, ohne = collections.Counter(), []
    beispiel = {}
    danach_ok = vorher_sauber = vorher_n = 0
    for s in aktien:
        _k, z = reihe(s)
        flags = [sauber(c) for _t, c in z]
        unsauber = [i for i, f in enumerate(flags) if not f]
        if not unsauber:
            ohne.append(s)
            continue
        j = unsauber[-1]
        schnitte[z[j][0][:7]] += 1
        danach_ok += all(flags[j + 1:])
        vorher_sauber += sum(flags[:j + 1])
        vorher_n += j + 1
        beispiel[s] = z[j][0]
    print(f"     Dateien mit mindestens einer unsauberen Zeile: "
          f"{len(aktien) - len(ohne)}; ohne: {len(ohne)} {ohne}")
    print(f"     nach dem Schnitt 100 % sauber: {danach_ok} von "
          f"{len(aktien) - len(ohne)}")
    print(f"     vor dem Schnitt sauber: {vorher_sauber} von {vorher_n} Zeilen "
          f"({100 * vorher_sauber / max(vorher_n, 1):.2f} %)")
    print(f"     Monat der letzten unsauberen Zeile (Anzahl Dateien): "
          f"{dict(sorted(schnitte.items()))}")
    for s in [x for x, _t, _f in SPLITS] + ["BRK-B", "MSFT", "JPM", "KO"]:
        if s in beispiel:
            print(f"       {s:<6} letzte unsaubere Zeile {beispiel[s]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
