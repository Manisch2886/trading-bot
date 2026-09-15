#!/usr/bin/env python3
"""
TB-33 - Der Datenlauf: Kursdaten holen
==============================================================================
Holt SPY, QQQ, IWM und EFA ueber yfinance und legt sie unter
`research/turn_of_month/daten/` ab - **nicht** unter `data/`.

WARUM EIN EIGENER DATENORDNER
------------------------------------------------------------------------------
TB-31 aendert `data/` parallel. Zwei Gruende, dem aus dem Weg zu gehen:

  * Beruehrungspunkte vermeiden heisst hier getrennt ablegen, nicht
    vorsichtig sein.
  * Der Datenstand-Hash in `herkunft.py` soll sich aendern, wenn SICH DIESE
    DATEN aendern - und sonst nie. Liefe er ueber `data/`, aenderte er sich
    aus fremdem Grund und beantwortete die Frage nicht mehr, fuer die er da
    ist.

DIESER SCHRITT LAEUFT AUF DEM RECHNER DES BETREIBERS
------------------------------------------------------------------------------
In der Cloud-Umgebung, in der TB-33 entstanden ist, ist Yahoo nicht
erreichbar (der Proxy antwortet mit 403) und `yfinance` ist nicht
installiert. Die Auswertung wurde deshalb gegen **erzeugte Beispieldaten**
gefuehrt - genau die Zusicherung aus TB-30a: das Auswertungsskript hat seinen
Test bestanden, als es noch nichts zu deuten gab.

Der Datenlauf ist der erste Schritt fuer den Mac; er steht als Schritt 6 im
Testdokument.

    python3 research/turn_of_month/datenlauf.py
    python3 research/turn_of_month/auswertung.py --json ergebnisse/lauf.json

`shared/kursdaten` laeuft danach ueber die Dateien - siehe `--pruefen`.
"""

import argparse
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)

import register as reg  # noqa: E402

sys.path.insert(0, os.path.join(reg.BASE_DIR, "shared"))

# Der frueheste sinnvolle Anfang. McConnell/Xu enden mit ihrer Stichprobe
# 2005; alles ab 2006 ist echte Out-of-Sample-Zeit. Geholt wird trotzdem,
# was da ist - abgeschnitten wird erst in der Auswertung, damit der
# Datenstand-Hash nicht von einer Wahl abhaengt.
START = "1993-01-01"


def hole(symbol, ziel_dir, start=START, ende=None):
    """Eine Kursdatei. Gibt (Pfad, Zeilen, gestrichene Kerzen) zurueck."""
    import yfinance as yf                                    # noqa: PLC0415
    import kursdaten                                         # noqa: PLC0415

    df = yf.download(symbol, start=start, end=ende, progress=False,
                     auto_adjust=True)
    if df is None or len(df) == 0:
        raise SystemExit(f"{symbol}: yfinance liefert nichts. Netz? "
                         f"Symbol richtig geschrieben?")
    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)
    df = df.reset_index()
    df.columns = [str(c).lower() for c in df.columns]
    df = df.rename(columns={"date": "open_time"})
    df["open_time"] = df["open_time"].astype(str).str.slice(0, 10)
    spalten = ["open_time", "open", "high", "low", "close", "volume"]
    fehlend = [s for s in spalten if s not in df.columns]
    if fehlend:
        raise SystemExit(f"{symbol}: Spalten fehlen: {fehlend}")
    df = df[spalten]

    # Streichen UND zaehlen - an der fruehestmoeglichen Stelle, damit keine
    # nachgelagerte Rechnung die Luecke je zu sehen bekommt.
    df, gestrichen = kursdaten.entferne_unvollstaendige(df, symbol=symbol,
                                                        melden=True)
    os.makedirs(ziel_dir, exist_ok=True)
    pfad = os.path.join(ziel_dir, f"{symbol}_1d.csv")
    df.to_csv(pfad, index=False)
    return pfad, len(df), gestrichen


def main():
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--ziel", default=reg.DATEN_DIR)
    p.add_argument("--start", default=START)
    p.add_argument("--ende", default=None,
                   help="JJJJ-MM-TT, ausschliesslich (Vorgabe: bis heute)")
    p.add_argument("--pruefen", action="store_true",
                   help="nur nachsehen, was schon da ist")
    args = p.parse_args()

    symbole = [reg.KERNINSTRUMENT] + reg.SWEEP_INSTRUMENTE

    if args.pruefen:
        for s in symbole:
            pfad = os.path.join(args.ziel, f"{s}_1d.csv")
            if os.path.exists(pfad):
                n = sum(1 for _ in open(pfad, encoding="utf-8")) - 1
                print(f"  {s:5s} {n:6d} Zeilen  {pfad}")
            else:
                print(f"  {s:5s}      -  fehlt ({pfad})")
        return 0

    for s in symbole:
        pfad, n, gestrichen = hole(s, args.ziel, args.start, args.ende)
        print(f"  {s:5s} {n:6d} Handelstage  "
              f"({gestrichen} unvollstaendige Kerze(n) gestrichen)  {pfad}")
    print("\nDer Sweep braucht QQQ, IWM und EFA. Fehlt eines, laeuft die "
          "Auswertung trotzdem\ndurch und weist die Zelle als fehlend aus - "
          "ein fehlendes Bild macht aus einem\nErgebnis kein anderes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
