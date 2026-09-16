#!/usr/bin/env python3
"""
S-B1 - Das Raster, und N wird GEZAEHLT (TB-39)
==============================================================================
Die Zahl der Rasterzellen entsteht hier aus der LISTE der Zellen, nicht aus
einer Angabe im Text. Das ist der Unterschied, auf den es ankommt: eine
abgetippte Zellenzahl kann stillschweigend falsch sein, eine gezaehlte nicht.

    N = len(zellen())

Jede Zelle erhoeht die Schwelle, ab der ein Ergebnis vom Besten-von-N-
Rauschen unterscheidbar ist. Die Zellen dieses Laufs kommen zu den 653 der
Neuselektion hinzu (`research/versuchsregister/REGISTER.md`, Stand
13.09.2026) - sie werden nicht dagegen aufgerechnet.

WARUM NUR EINE ACHSE
------------------------------------------------------------------------------
Die Beschreibung von S-B1 legt fast alles fest: die Instrumente, die drei
Signalfenster, den Mehrheitsentscheid, die inverse Volatilitaetsgewichtung,
"Kasse als Rest", die monatliche Umschichtung. Was sie NICHT festlegt, ist
eine einzige Zahl: ueber welchen Rueckblick die Volatilitaet gemessen wird.

Genau diese eine Zahl steht im Raster. Alles andere stuende dort nur, weil es
sich rastern LIESSE - und das ist in diesem Projekt ausdruecklich kein Grund
(Vorregistrierung Abschnitt 2.6: "Der Grund ist nicht Bequemlichkeit,
sondern N").

`--was-waere-wenn` rechnet vor, was zusaetzliche Achsen kosten wuerden.
Die Zahlen sind ein Bild fuer den Betreiber, KEINE Alternative: eine andere
Achsenwahl ist ein neuer vorregistrierter Lauf mit eigenem N.
"""

import argparse
import itertools
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)

import register as reg                                      # noqa: E402

# Die historische Zellenzahl, zu der die Zellen dieses Laufs hinzukommen.
# Quelle: Vorregistrierung Abschnitt 9.
N_HISTORISCH = 653


# ---------------------------------------------------------------------------
# Die Achsen. EINE Liste - wer eine Achse hinzufuegt, aendert N automatisch.
# ---------------------------------------------------------------------------
def achsen():
    """[(Name, (Werte...)), ...] - die Achsen des Rasters, in fester Folge."""
    return [
        ("vol_rueckblick_tage", tuple(reg.VOL_RUECKBLICK_TAGE)),
    ]


def feste_werte():
    """Was NICHT im Raster steht - und deshalb nicht zu N zaehlt.

    Ausdruecklich aufgezaehlt, damit der Unterschied zwischen "festgelegt"
    und "vergessen" nachlesbar ist.
    """
    return {
        "signalfenster_monate": reg.SIGNALFENSTER_MONATE,
        "signal_mehrheit": reg.SIGNAL_MEHRHEIT,
        "signalmass": reg.SIGNALMASS,
        "gewichtung": reg.GEWICHTUNG,
        "volatilitaetsmass": reg.VOLATILITAETSMASS,
        "gewichtsdeckel": reg.GEWICHTSDECKEL,
        "kasse_verzinst": reg.KASSE_VERZINST,
        "umschichtung": reg.UMSCHICHTUNG,
        "umschichtung_entscheidungstag": reg.UMSCHICHTUNG_ENTSCHEIDUNGSTAG,
        "umschichtung_ausfuehrung": reg.UMSCHICHTUNG_AUSFUEHRUNG,
        "kosten_je_roundtrip_pct": reg.KOSTEN_JE_ROUNDTRIP_PCT,
    }


def zellen():
    """Die vollstaendige Liste der Rasterzellen. N ist ihre Laenge."""
    namen = [n for n, _ in achsen()]
    werte = [w for _, w in achsen()]
    return [dict(zip(namen, komb)) for komb in itertools.product(*werte)]


def n():
    """Die Zahl der Rasterzellen - GEZAEHLT, nicht angegeben."""
    return len(zellen())


def zellenname(zelle):
    """Reproduzierbarer Name einer Zelle. Gleichstand wird alphabetisch
    aufgeloest (Vorregistrierung Abschnitt 6), also braucht jede Zelle einen
    Namen, der nicht von der Reihenfolge des Aufzaehlens abhaengt."""
    return "|".join(f"{k}={zelle[k]}" for k in sorted(zelle))


def nachbarn(zelle):
    """Die Nachbarschaft der Plateau-Regel: Punkte, die sich in GENAU EINER
    Dimension um EINE Stufe unterscheiden.

    Geometrisch, nicht zulaessigkeitsgefiltert - die Plateau-Regel misst die
    Glattheit der Flaeche, nicht die Zulaessigkeit.
    """
    aus = []
    for name, werte in achsen():
        i = list(werte).index(zelle[name])
        for j in (i - 1, i + 1):
            if 0 <= j < len(werte):
                nachbar = dict(zelle)
                nachbar[name] = werte[j]
                aus.append(nachbar)
    return aus


# ---------------------------------------------------------------------------
# Was zusaetzliche Achsen kosten wuerden - ein Bild, keine Alternative
# ---------------------------------------------------------------------------
def was_waere_wenn():
    """[(Beschreibung, N), ...] - der Preis weiterer Achsen, vorgerechnet."""
    grund = n()
    faelle = []
    # Die drei Signalfenster je vierstufig, unabhaengig voneinander.
    faelle.append((
        "die drei Signalfenster je vierstufig im Raster (statt fest)",
        grund * 4 ** len(reg.SIGNALFENSTER_MONATE)))
    # Ein Gewichtsdeckel mit drei Stufen.
    faelle.append((
        "zusaetzlich ein Gewichtsdeckel mit drei Stufen",
        grund * 3))
    # Der Umschichtungstag als Achse (Anfang, Mitte, Ende des Monats).
    faelle.append((
        "zusaetzlich der Umschichtungstag mit drei Stufen",
        grund * 3))
    # Das Signalmass als Achse (Fensterrendite gegen gleitenden Durchschnitt).
    faelle.append((
        "zusaetzlich das Signalmass mit zwei Stufen",
        grund * 2))
    faelle.append((
        "alles davon zusammen",
        grund * 4 ** len(reg.SIGNALFENSTER_MONATE) * 3 * 3 * 2))
    return faelle


def bericht():
    """Alles, was ins Register gehoert - als Datenstruktur, nicht als Text."""
    ax = achsen()
    return {
        "achsen": [{"name": name, "stufen": list(werte),
                    "anzahl": len(werte)} for name, werte in ax],
        "grenzsatz_vol_rueckblick": reg.VOL_RUECKBLICK_GRENZSATZ,
        "feste_werte": feste_werte(),
        "zellen": [zellenname(z) for z in zellen()],
        "N": n(),
        "N_historisch": N_HISTORISCH,
        "N_gesamt_nominal": N_HISTORISCH + n(),
        "was_waere_wenn": [{"fall": f, "N": v} for f, v in was_waere_wenn()],
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--json", metavar="PFAD", default=None,
                   help="den Bericht zusaetzlich als JSON ablegen")
    p.add_argument("--was-waere-wenn", action="store_true",
                   help="vorrechnen, was weitere Achsen kosten wuerden")
    args = p.parse_args(argv)

    b = bericht()
    print("S-B1 - das Raster\n")
    for a in b["achsen"]:
        print(f"  Achse  {a['name']:22s} {a['anzahl']} Stufen: "
              f"{a['stufen']}")
    print("\n  Fest (zaehlt NICHT zu N):")
    for k, v in b["feste_werte"].items():
        print(f"    {k:32s} {v}")
    print(f"\n  Zellen ({b['N']}), gezaehlt aus der Liste:")
    for name in b["zellen"]:
        print(f"    {name}")
    print(f"\n  N                  {b['N']}")
    print(f"  N_historisch       {b['N_historisch']}  "
          f"(Neuselektion, Vorregistrierung Abschnitt 9)")
    print(f"  N gesamt, nominal  {b['N_gesamt_nominal']}")

    if args.was_waere_wenn:
        print("\n  Was weitere Achsen kosten wuerden (Bild, keine "
              "Alternative):")
        for f in b["was_waere_wenn"]:
            print(f"    {f['N']:6d}  {f['fall']}")

    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(b, fh, indent=2, ensure_ascii=False, sort_keys=False)
        print(f"\n  geschrieben: {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
