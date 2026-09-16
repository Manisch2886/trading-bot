#!/usr/bin/env python3
"""
S-B1 - Wie weit reicht die Historie, und traegt sie die Untergrenze? (TB-39)
==============================================================================
Die harte Frage zuerst, weil sie alles andere bestimmt: **Fuer welche ETFs
reicht die Historie tatsaechlich bis 2007 zurueck?** Viele ETFs sind juenger,
und ohne 2008 hat eine Trendfolgestrategie nie einen echten Baerenmarkt
gesehen.

Dieses Werkzeug MISST das - es schaetzt nicht. Es liest die Kursdateien unter
`research/etf_trendfolge/daten/`, nimmt je Kandidat das erste und das letzte
Datum und rechnet daraus, ab wann das Instrument ein Signal tragen kann.

DREI DATEN, DIE NICHT DASSELBE SIND
------------------------------------------------------------------------------
  erstes Datum   Die erste Kerze der Reihe. Was yfinance ausliefert.
  Signal ab      Das Datum der VORLAUF_TAGE-ten Kerze. Vorher gibt es kein
                 Zwoelf-Monats-Fenster und keinen Volatilitaets-Rueckblick,
                 also auch kein Signal. Das sind rund zwoelf Monate NACH der
                 Auflage - der Unterschied ist genau der Grund, warum die
                 Datenanforderung auf 2007 lautet und nicht auf 2008.
  im Universum   Ab dem ersten Umschichtungstag nach "Signal ab".

DIE UNTERGRENZE WIRD GEPRUEFT, NICHT ANGENOMMEN
------------------------------------------------------------------------------
**Acht Instrumente ueber mindestens vier Anlageklassen.** Darunter
degeneriert S-B1 zu Aktien-Timing mit Beiwerk - dann wird sie NICHT gebaut,
und das ist ein zulaessiges Ergebnis dieser Aufgabe.

Wird sie am Stichtag nicht erreicht, meldet dieses Werkzeug
**Rueckgabewert 1**. Die beiden Bedingungen werden GETRENNT gefuehrt und
getrennt gemeldet: "acht Instrumente, aber nur drei Klassen" ist ein anderer
Befund als "vier Klassen, aber nur sieben Instrumente", und eine Wache, die
beide zu einer verschmilzt, kann das Fehlen der einen hinter der anderen
verstecken.

WAS DIESES WERKZEUG NICHT TUT
------------------------------------------------------------------------------
Es waehlt nicht aus. Es rechnet keinen Ertrag, kein Sharpe, keine Rendite.
Es sagt, welche Instrumente wann DA sind - eine Eigenschaft des Kalenders,
nicht des Ergebnisses.

Reine Standardbibliothek: dasselbe Werkzeug laeuft in der Cloud gegen
erzeugte Beispieldaten und am Mac gegen die echten.
"""

import argparse
import csv
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)

import register as reg                                      # noqa: E402

ZEITSPALTE = "open_time"


# ---------------------------------------------------------------------------
# Lesen
# ---------------------------------------------------------------------------
def dateiname(symbol):
    return f"{symbol}_1d.csv"


def lies_tage(pfad):
    """Die Datumsspalte einer Kursdatei, aufsteigend, ohne Doppelte.

    Gelesen wird NUR die Zeitspalte. Kurse braucht dieses Werkzeug nicht -
    und was es nicht liest, kann es auch nicht versehentlich auswerten.
    """
    tage = []
    with open(pfad, newline="", encoding="utf-8") as fh:
        leser = csv.DictReader(fh)
        if leser.fieldnames is None or ZEITSPALTE not in leser.fieldnames:
            raise SystemExit(
                f"{pfad}: Spalte {ZEITSPALTE!r} fehlt (gefunden: "
                f"{leser.fieldnames}).")
        for zeile in leser:
            wert = (zeile.get(ZEITSPALTE) or "").strip()
            if not wert:
                continue
            tage.append(wert[:10])
    tage = sorted(set(tage))
    return tage


def messe(symbol, daten_dir):
    """Ein Kandidat: gemessene Daten - oder der Vermerk, dass die Datei
    fehlt."""
    pfad = os.path.join(daten_dir, dateiname(symbol))
    eintrag = {
        "symbol": symbol,
        "klasse": reg.klasse_von(symbol),
        "datei": pfad,
        "vorhanden": os.path.exists(pfad),
        "erstes_datum": None,
        "letztes_datum": None,
        "handelstage": 0,
        "signal_ab": None,
        "erwartete_auflage": None,
        "abweichung_zur_erwartung": None,
    }
    for k in reg.KANDIDATEN:
        if k["symbol"] == symbol:
            eintrag["erwartete_auflage"] = k["erwartete_auflage"]
    if not eintrag["vorhanden"]:
        return eintrag

    tage = lies_tage(pfad)
    eintrag["handelstage"] = len(tage)
    if not tage:
        return eintrag
    eintrag["erstes_datum"] = tage[0]
    eintrag["letztes_datum"] = tage[-1]
    # Das Signal steht ab der VORLAUF_TAGE-ten Kerze. Index VORLAUF_TAGE - 1
    # ist die Kerze, mit der der Vorlauf voll ist.
    if len(tage) >= reg.VORLAUF_TAGE:
        eintrag["signal_ab"] = tage[reg.VORLAUF_TAGE - 1]
    # Die Erwartung ist KEINE Messung - sie ist die Wache gegen ein
    # stillschweigend falsches Symbol. Weicht sie ab, wird das gemeldet und
    # die MESSUNG gilt.
    if eintrag["erwartete_auflage"] and eintrag["erstes_datum"]:
        if eintrag["erstes_datum"][:7] != eintrag["erwartete_auflage"][:7]:
            eintrag["abweichung_zur_erwartung"] = (
                f"gemessen {eintrag['erstes_datum']}, erwartet "
                f"{eintrag['erwartete_auflage']}")
    return eintrag


def messe_alle(daten_dir=None):
    daten_dir = daten_dir or reg.DATEN_DIR
    return [messe(s, daten_dir) for s in reg.symbole()]


# ---------------------------------------------------------------------------
# Die Untergrenze - zwei Bedingungen, getrennt gefuehrt
# ---------------------------------------------------------------------------
def verfuegbar_am(messungen, stichtag):
    """Die Symbole, die am Stichtag ein Signal tragen koennen."""
    return [m["symbol"] for m in messungen
            if m["signal_ab"] and m["signal_ab"] <= stichtag]


def untergrenze(messungen, stichtag):
    """Der Befund zur Untergrenze am Stichtag.

    `instrumente_erfuellt` und `klassen_erfuellt` stehen GETRENNT im
    Ergebnis. Sie werden nicht zu einer Zahl verrechnet: sonst koennte die
    eine Bedingung das Fehlen der anderen verdecken.
    """
    symbole = verfuegbar_am(messungen, stichtag)
    klassen = sorted({reg.klasse_von(s) for s in symbole})
    instrumente_erfuellt = len(symbole) >= reg.UNTERGRENZE_INSTRUMENTE
    klassen_erfuellt = len(klassen) >= reg.UNTERGRENZE_KLASSEN
    gruende = []
    if not instrumente_erfuellt:
        gruende.append(
            f"nur {len(symbole)} Instrument(e), verlangt sind "
            f"{reg.UNTERGRENZE_INSTRUMENTE}")
    if not klassen_erfuellt:
        gruende.append(
            f"nur {len(klassen)} Anlageklasse(n), verlangt sind "
            f"{reg.UNTERGRENZE_KLASSEN}")
    return {
        "stichtag": stichtag,
        "symbole": symbole,
        "anzahl_instrumente": len(symbole),
        "klassen": klassen,
        "anzahl_klassen": len(klassen),
        "instrumente_erfuellt": instrumente_erfuellt,
        "klassen_erfuellt": klassen_erfuellt,
        "erfuellt": instrumente_erfuellt and klassen_erfuellt,
        "gruende": gruende,
    }


def je_falte(messungen, bis_jahr=None):
    """Die Untergrenze Jahr fuer Jahr - die Grundlage des Faltenplans.

    Eine Selektionsfalte ist ein Kalenderjahr (Verfahren B). Gezaehlt wird,
    was am 1. Januar des Jahres schon ein Signal tragen kann.
    """
    bis_jahr = bis_jahr or reg.SELEKTIONSFALTEN_BIS
    aus = []
    for jahr in range(reg.ERSTE_SELEKTIONSFALTE, bis_jahr + 1):
        aus.append(untergrenze(messungen, f"{jahr}-01-01"))
    return aus


def bericht(daten_dir=None, stichtag=None, bis_jahr=None):
    messungen = messe_alle(daten_dir)
    stichtag = stichtag or reg.UNTERGRENZE_STICHTAG
    falten = je_falte(messungen, bis_jahr)
    tragende = [f for f in falten if f["erfuellt"]]
    return {
        "daten_dir": daten_dir or reg.DATEN_DIR,
        "vorlauf_tage": reg.VORLAUF_TAGE,
        "historie_ab": reg.HISTORIE_AB,
        "messungen": messungen,
        "fehlende_dateien": [m["symbol"] for m in messungen
                             if not m["vorhanden"]],
        "abweichungen_zur_erwartung": [
            {"symbol": m["symbol"], "was": m["abweichung_zur_erwartung"]}
            for m in messungen if m["abweichung_zur_erwartung"]],
        "untergrenze": untergrenze(messungen, stichtag),
        "je_falte": falten,
        "tragende_falten": len(tragende),
        "faltenmindestzahl": reg.FALTEN_MINDESTZAHL,
        "faltenmindestzahl_erfuellt": len(tragende) >= reg.FALTEN_MINDESTZAHL,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--daten", default=None, help="Ordner mit den Kursdateien")
    p.add_argument("--stichtag", default=None,
                   help=f"Vorgabe: {reg.UNTERGRENZE_STICHTAG}")
    p.add_argument("--bis-jahr", type=int, default=None)
    p.add_argument("--json", metavar="PFAD", default=None)
    args = p.parse_args(argv)

    b = bericht(args.daten, args.stichtag, args.bis_jahr)

    print("S-B1 - Historie der Kandidaten\n")
    print(f"  Datenordner  {b['daten_dir']}")
    print(f"  Vorlauf      {b['vorlauf_tage']} Handelstage "
          f"(laengstes Signalfenster bzw. Vol-Rueckblick)\n")
    print(f"  {'Symbol':7s}{'Klasse':12s}{'erstes Datum':14s}"
          f"{'Signal ab':13s}{'Tage':>7s}   Erwartung")
    print("  " + "-" * 72)
    for m in b["messungen"]:
        if not m["vorhanden"]:
            print(f"  {m['symbol']:7s}{m['klasse']:12s}"
                  f"{'DATEI FEHLT':14s}{'-':13s}{0:>7d}   "
                  f"{m['erwartete_auflage']}")
            continue
        print(f"  {m['symbol']:7s}{m['klasse']:12s}"
              f"{m['erstes_datum'] or '-':14s}"
              f"{m['signal_ab'] or 'nie':13s}{m['handelstage']:>7d}   "
              f"{m['erwartete_auflage']}")

    if b["abweichungen_zur_erwartung"]:
        print("\n  Abweichungen zur Erwartung (die MESSUNG gilt):")
        for a in b["abweichungen_zur_erwartung"]:
            print(f"    {a['symbol']}: {a['was']}")

    u = b["untergrenze"]
    print(f"\n  Untergrenze am {u['stichtag']}:")
    print(f"    Instrumente   {u['anzahl_instrumente']:>3d} von "
          f"{reg.UNTERGRENZE_INSTRUMENTE} verlangt   "
          f"{'erfuellt' if u['instrumente_erfuellt'] else 'NICHT ERFUELLT'}")
    print(f"    Anlageklassen {u['anzahl_klassen']:>3d} von "
          f"{reg.UNTERGRENZE_KLASSEN} verlangt   "
          f"{'erfuellt' if u['klassen_erfuellt'] else 'NICHT ERFUELLT'}")
    if u["symbole"]:
        print(f"    dabei: {', '.join(u['symbole'])}")
        print(f"    Klassen: {', '.join(u['klassen'])}")

    print(f"\n  Selektionsfalten, die die Untergrenze tragen: "
          f"{b['tragende_falten']} (Mindestzahl {b['faltenmindestzahl']})")
    print(f"  {'Jahr':6s}{'Instrumente':>13s}{'Klassen':>9s}   traegt")
    for f in b["je_falte"]:
        print(f"  {f['stichtag'][:4]:6s}{f['anzahl_instrumente']:>13d}"
              f"{f['anzahl_klassen']:>9d}   "
              f"{'ja' if f['erfuellt'] else 'nein'}")

    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(b, fh, indent=2, ensure_ascii=False)
        print(f"\n  geschrieben: {args.json}")

    if not u["erfuellt"]:
        print("\n  BEFUND: Die Untergrenze ist am Stichtag NICHT erfuellt - "
              + "; ".join(u["gruende"]) + ".")
        print("  S-B1 wird dann NICHT gebaut. Das ist ein zulaessiges "
              "Ergebnis, kein Fehler.")
        print("  Ob stattdessen ein spaeterer Start oder ein Verzicht auf "
              "einzelne Anlageklassen")
        print("  richtig ist, entscheidet der Betreiber.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
