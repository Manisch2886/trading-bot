#!/usr/bin/env python3
"""
S-B1 - Was von den Ertraegen nach 0,30 Prozentpunkten je Round Trip bleibt
==============================================================================
Bei `S-E2` war genau diese Rechnung der Grund, die Strategie zu verwerfen.
Sie wird deshalb hier gefuehrt, BEVOR gerechnet wird - und zwar so, dass sie
KEINE Kursdaten braucht: sie folgt allein aus der Bauart der Strategie.

DER SCHRITT, DER DIE ANGST NIMMT
------------------------------------------------------------------------------
Die naheliegende Sorge lautet: "monatliche Umschichtung von 8 bis 14
Positionen, das sind 12 x 14 Round Trips im Jahr, also 50 Prozentpunkte
Kosten." Das waere richtig, wenn jeden Monat das ganze Buch umgeschlagen
wuerde. Wird es nicht:

  * Umgeschlagen wird nur, was sich AENDERT. Ein Instrument, dessen Signal
    zwei Jahre lang positiv bleibt, wird einmal gekauft und einmal verkauft -
    nicht 24 mal.
  * Die Groesse, auf die es ankommt, ist der EINSEITIGE UMSCHLAG je
    Umschichtung: die Summe der absoluten Gewichtsaenderungen.

    Kosten je Umschichtung = Umschlag x 0,15 Prozentpunkte
    (0,15 = TRADING_FEE_PCT 0,1 + SLIPPAGE_PCT 0,05 je Order; ein Round Trip
    sind zwei Orders und damit 0,30.)

DIE RECHNUNG, UND IHR UEBERRASCHENDES ERGEBNIS
------------------------------------------------------------------------------
Kippt ein Instrument, aendert sich sein Gewicht um seinen vollen Anteil, im
Mittel 1/n. Kippen die n Instrumente im Jahr je w mal, sind das n*w Kippungen
im Jahr, jede mit Umschlag 1/n:

    Jahresumschlag  =  n * w * (1/n)  =  w
    Jahreskosten    =  w * 0,15 Prozentpunkte

**Die Zahl der Instrumente kuerzt sich heraus.** Ob acht oder vierzehn ETFs
im Buch liegen, aendert die Kostenlast nicht - es aendert nur, in wie viele
Stuecke sie zerfaellt. Das ist der Grund, warum die Untergrenze von acht
Instrumenten keine Kostenfrage ist, sondern eine Frage der Streuung.

Dazu kommt der **Drift**: die inversen Volatilitaetsgewichte verschieben sich
auch dann, wenn kein Signal kippt. Dieser Anteil wird getrennt gefuehrt, weil
er eine andere Groessenordnung hat und eine andere Abhilfe haette
(Umschichtungsbaender).

WAS HIER KEINE MESSUNG IST - UND ES AUCH NICHT WERDEN DARF
------------------------------------------------------------------------------
`w` (Kippungen je Instrument und Jahr) und `d` (Drift je Umschichtung) sind
EIGENSCHAFTEN DER KURSREIHEN. Sie zu messen hiesse, den Backtest zu rechnen -
und der gehoert hinter Rang 1. Dieses Modul rechnet deshalb eine TABELLE ueber
beide Groessen und laesst die Felder offen, die der Lauf spaeter fuellt.

Dasselbe gilt fuer den Bruttoertrag: die Tabelle am Ende zeigt, was von einem
ANGENOMMENEN Bruttoertrag bleibt. Die Annahme ist die des Lesers, nicht eine
Zahl dieses Projekts.
"""

import argparse
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)

import register as reg                                      # noqa: E402

# Die Kippraten, ueber die die Tabelle laeuft: Kippungen je Instrument und
# Jahr. Die Spanne umfasst, was ein Trendsignal ueberhaupt tun kann - von
# "einmal im Jahr" bis "jeden zweiten Monat".
KIPPRATEN = (1, 2, 3, 4, 6)

# Der Drift je Umschichtung, als Anteil des Buches. 0 heisst: Gewichte
# werden nur bei einer Kippung angefasst (Umschichtungsbaender).
DRIFTRATEN = (0.0, 0.005, 0.010, 0.020)

# Bruttoertraege, gegen die abgerechnet wird. ANNAHME DES LESERS, keine
# Messung und keine Erwartung dieses Projekts.
ANGENOMMENE_BRUTTOERTRAEGE_PCT = (2.0, 4.0, 6.0, 8.0)


def jahreskosten_pct(kippungen_je_instrument_und_jahr, drift_je_umschichtung):
    """Jahreskosten in Prozentpunkten des Buches.

    Der erste Summand kuerzt die Instrumentenzahl heraus (siehe Modulkopf);
    der zweite nicht - er haengt am Umschichtungsabstand.
    """
    aus_kippungen = (kippungen_je_instrument_und_jahr
                     * reg.KOSTEN_JE_ORDER_PCT)
    aus_drift = (reg.UMSCHICHTUNGEN_JE_JAHR * drift_je_umschichtung * 100.0
                 * reg.KOSTEN_JE_ORDER_PCT / 100.0)
    return aus_kippungen + aus_drift


def vollumschlag_jahreskosten_pct():
    """Die obere Schranke: jeden Monat kippt ALLES.

    Der Umschlag ist dann 1 je Umschichtung, unabhaengig von n. Das ist die
    Zahl, die in der naheliegenden Sorge steckt - und sie ist die Obergrenze,
    nicht die Erwartung.
    """
    return (reg.UMSCHICHTUNGEN_JE_JAHR * 1.0 * reg.KOSTEN_JE_ORDER_PCT)


def vergleichszahl_se1_pct():
    """Zum Groessenvergleich: ein VOLLER Round Trip je Monat.

    Das ist die Kostenschranke, die S-E1 ueberspringen musste (zwoelf Runden
    im Jahr, jede ueber das ganze Buch). Sie steht hier nur als Massstab.
    """
    return reg.UMSCHICHTUNGEN_JE_JAHR * reg.KOSTEN_JE_ROUNDTRIP_PCT


def tabelle():
    """[(w, {d: Jahreskosten}), ...] - die Kostenlast, vollstaendig."""
    aus = []
    for w in KIPPRATEN:
        zeile = {d: jahreskosten_pct(w, d) for d in DRIFTRATEN}
        aus.append((w, zeile))
    return aus


def nach_abzug(brutto_pct, kosten_pct):
    """Was von einem ANGENOMMENEN Bruttoertrag bleibt - und welcher Anteil
    des Ertrags in die Kosten geht."""
    netto = brutto_pct - kosten_pct
    anteil = (kosten_pct / brutto_pct * 100.0) if brutto_pct else float("inf")
    return netto, anteil


def bericht():
    t = tabelle()
    return {
        "kosten_je_order_pct": reg.KOSTEN_JE_ORDER_PCT,
        "kosten_je_roundtrip_pct": reg.KOSTEN_JE_ROUNDTRIP_PCT,
        "umschichtungen_je_jahr": reg.UMSCHICHTUNGEN_JE_JAHR,
        "formel": ("Jahreskosten in Prozentpunkten = w * 0,15 + "
                   "12 * d * 0,15 ; w = Kippungen je Instrument und Jahr, "
                   "d = Drift je Umschichtung als Anteil des Buches"),
        "instrumentenzahl_kuerzt_sich_heraus": True,
        "obere_schranke_pct": vollumschlag_jahreskosten_pct(),
        "massstab_voller_roundtrip_je_monat_pct": vergleichszahl_se1_pct(),
        "tabelle": [{"kippungen_je_instrument_und_jahr": w,
                     "jahreskosten_pct": {str(d): round(v, 4)
                                          for d, v in zeile.items()}}
                    for w, zeile in t],
        "was_bleibt": [
            {"angenommener_bruttoertrag_pct": b,
             "je_kipprate": [
                 {"kippungen_je_instrument_und_jahr": w,
                  "kosten_pct": round(jahreskosten_pct(w, 0.005), 4),
                  "netto_pct": round(nach_abzug(
                      b, jahreskosten_pct(w, 0.005))[0], 4),
                  "anteil_des_ertrags_pct": round(nach_abzug(
                      b, jahreskosten_pct(w, 0.005))[1], 1)}
                 for w in KIPPRATEN]}
            for b in ANGENOMMENE_BRUTTOERTRAEGE_PCT],
        "offen_bis_rang_1": [
            "w - die Kipprate je Instrument und Jahr",
            "d - der Drift der inversen Volatilitaetsgewichte",
            "der Bruttoertrag selbst",
        ],
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--json", metavar="PFAD", default=None)
    args = p.parse_args(argv)

    b = bericht()
    print("S-B1 - Kosten bei 0,30 Prozentpunkten je Round Trip\n")
    print(f"  {b['formel']}\n")
    kopf = "  w \\ d  " + "".join(f"{d:>10.3f}" for d in DRIFTRATEN)
    print(kopf)
    print("  " + "-" * (len(kopf) - 2))
    for zeile in b["tabelle"]:
        w = zeile["kippungen_je_instrument_und_jahr"]
        werte = "".join(f"{zeile['jahreskosten_pct'][str(d)]:>10.3f}"
                        for d in DRIFTRATEN)
        print(f"  {w:>3d}    {werte}")
    print("\n  (Prozentpunkte je Jahr, auf das ganze Buch)")
    print(f"\n  Obere Schranke (jeden Monat kippt alles): "
          f"{b['obere_schranke_pct']:.2f} Prozentpunkte je Jahr")
    print(f"  Massstab, ein VOLLER Round Trip je Monat:  "
          f"{b['massstab_voller_roundtrip_je_monat_pct']:.2f} Prozentpunkte "
          f"je Jahr")

    print("\n  Was von einem ANGENOMMENEN Bruttoertrag bleibt "
          "(Annahme des Lesers, keine Messung):\n")
    print("    brutto   w=1      w=2      w=3      w=4      w=6")
    for eintrag in b["was_bleibt"]:
        felder = "".join(f"{e['netto_pct']:>9.2f}"
                         for e in eintrag["je_kipprate"])
        print(f"    {eintrag['angenommener_bruttoertrag_pct']:>5.1f} %"
              f"{felder}")
    print("\n    (Nettoertrag in Prozent, bei Drift d = 0,005)")

    print("\n  Offen bis Rang 1 - diese Groessen sind KEINE Annahme, "
          "sondern Messungen,\n  die erst der Backtest liefern darf:")
    for z in b["offen_bis_rang_1"]:
        print(f"    - {z}")

    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(b, fh, indent=2, ensure_ascii=False)
        print(f"\n  geschrieben: {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
