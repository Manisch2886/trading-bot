#!/usr/bin/env python3
"""
S-B1 - Erzeugte Beispieldaten (TB-39)
==============================================================================
Aus der Cloud sind Binance und yfinance gesperrt (403). Die Werkzeuge dieses
Ordners werden deshalb gegen **erzeugte** Daten geprueft - genau die
Zusicherung, die dieses Projekt seit TB-30a verlangt: das Werkzeug hat seinen
Test bestanden, als es noch nichts zu deuten gab.

WAS DIESE DATEN SIND - UND WAS SIE AUSDRUECKLICH NICHT SIND
------------------------------------------------------------------------------
Sie sind ein **Kalender mit Zahlen daran**. Geprueft wird an ihnen, ob die
Werkzeuge das erste Datum richtig finden, den Vorlauf richtig abzaehlen, die
Untergrenze richtig beurteilen und die beiden Wachen tatsaechlich durchlaufen.

Sie sind **keine Marktdaten**. Aus ihnen darf keine Aussage ueber S-B1
folgen - kein Ertrag, kein Sharpe, keine Korrelation. Wer das versuchte,
beobachtete den Zufallsgenerator, nicht den Markt.

Reine Standardbibliothek, deterministisch (derselbe Startwert, dieselbe
Reihe): ein Test, der bei jedem Lauf andere Zahlen sieht, prueft nichts.
"""

import argparse
import datetime as dt
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)

import register as reg                                      # noqa: E402

SPALTEN = ["open_time", "open", "high", "low", "close", "volume"]

# Fester Startwert. Ohne ihn gibt es keine Wiederholbarkeit, und ohne
# Wiederholbarkeit keinen Test.
STARTWERT = 20260916


class _Zufall:
    """Ein linearer Kongruenzgenerator. Absichtlich schlicht: er soll
    reproduzierbar sein, nicht statistisch gut - es werden keine Ertraege
    daraus gerechnet."""

    def __init__(self, startwert):
        self.z = startwert % (2 ** 31 - 1) or 1

    def naechste(self):
        self.z = (self.z * 48271) % (2 ** 31 - 1)
        return self.z / (2 ** 31 - 1)


def handelstage(von, bis):
    """Alle Montage bis Freitage im Zeitraum, einschliesslich.

    KEIN Boersenkalender: Feiertage fehlen hier absichtlich. Die Werkzeuge
    dieses Ordners zaehlen Zeilen, nicht Kalendertage - ein Feiertag mehr
    oder weniger aendert an dem, was geprueft wird, nichts, und ein zweiter
    Kalender waere eine zweite Quelle fuer dieselbe Zahl.
    """
    a = dt.date.fromisoformat(von)
    b = dt.date.fromisoformat(bis)
    tage = []
    while a <= b:
        if a.weekday() < 5:
            tage.append(a.isoformat())
        a += dt.timedelta(days=1)
    return tage


def reihe(symbol, von, bis, startwert=STARTWERT):
    """Eine Kursreihe als Liste von Zeilen (dict je Zeile)."""
    z = _Zufall(startwert + sum(ord(c) for c in symbol))
    kurs = 100.0
    zeilen = []
    for tag in handelstage(von, bis):
        schritt = (z.naechste() - 0.5) * 2.0
        eroeffnung = kurs
        kurs = max(1.0, kurs + schritt)
        hoch = max(eroeffnung, kurs) + z.naechste() * 0.5
        tief = min(eroeffnung, kurs) - z.naechste() * 0.5
        zeilen.append({
            "open_time": tag,
            "open": round(eroeffnung, 4),
            "high": round(hoch, 4),
            "low": round(max(0.01, tief), 4),
            "close": round(kurs, 4),
            "volume": int(1_000_000 + z.naechste() * 500_000),
        })
    return zeilen


def schreibe_reihe(zeilen, pfad):
    os.makedirs(os.path.dirname(os.path.abspath(pfad)), exist_ok=True)
    with open(pfad, "w", encoding="utf-8", newline="") as fh:
        fh.write(",".join(SPALTEN) + "\n")
        for z in zeilen:
            fh.write(",".join(str(z[s]) for s in SPALTEN) + "\n")
    return pfad


def erzeuge_bestand(ziel_dir, bis="2026-09-01", von_je_symbol=None,
                    nur=None, startwert=STARTWERT):
    """Einen vollstaendigen Beispielbestand anlegen.

    `von_je_symbol` setzt den Anfang je Symbol. Ohne Angabe wird die
    `erwartete_auflage` aus dem Register benutzt - AUSDRUECKLICH als
    Beispiel, nicht als Messung: was zaehlt, misst `historie.py` an den
    echten Dateien.
    """
    von_je_symbol = von_je_symbol or {}
    geschrieben = []
    for k in reg.KANDIDATEN:
        symbol = k["symbol"]
        if nur is not None and symbol not in nur:
            continue
        von = von_je_symbol.get(symbol, k["erwartete_auflage"])
        pfad = os.path.join(ziel_dir, f"{symbol}_1d.csv")
        schreibe_reihe(reihe(symbol, von, bis, startwert), pfad)
        geschrieben.append(pfad)
    return geschrieben


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--ziel", required=True,
                   help="Zielordner - NICHT data/ und NICHT daten/")
    p.add_argument("--bis", default="2026-09-01")
    args = p.parse_args(argv)

    import datenstand                                       # noqa: PLC0415
    draussen, grund = datenstand.ziel_liegt_ausserhalb(args.ziel)
    if not draussen:
        print(f"ABBRUCH: {grund}")
        return 1
    if os.path.realpath(args.ziel) == os.path.realpath(reg.DATEN_DIR):
        print("ABBRUCH: Beispieldaten gehoeren nicht in den Ordner der "
              "echten Kursdateien. Sie waeren dort von ihnen nicht zu "
              "unterscheiden.")
        return 1

    pfade = erzeuge_bestand(args.ziel, args.bis)
    for pfad in pfade:
        print(f"  {os.path.basename(pfad)}")
    print(f"\n  {len(pfade)} Beispieldateien in {args.ziel}")
    print("  ERZEUGT, NICHT GEMESSEN - aus ihnen folgt keine Aussage "
          "ueber S-B1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
