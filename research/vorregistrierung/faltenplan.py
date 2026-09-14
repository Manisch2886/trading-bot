#!/usr/bin/env python3
"""
TB-30a - Faltenplan: verankert, expandierend, mit Purge und Embargo
==============================================================================
Der Faltenplan ist die zweite Haelfte der Vorregistrierung: er legt fest,
WORAUF die Selektionsstatistik gerechnet wird, bevor eine Zahl existiert.

DIE REGELN (eingefroren)
------------------------------------------------------------------------------
1. **Verankert, expandierend.** Das Training beginnt immer am Datenbeginn des
   jeweiligen Symbols und endet am Rand der Falte, abzueglich der Purge-Laenge.
   Nicht rollierend: ein Verfahren, das alte Jahre vergisst, waehlt im
   Zweifel die Parameter des letzten Marktzustands.

2. **Aktien: Testfalten sind Kalenderjahre 2019 bis zum Go-Live-Schnitt.**
   Vor der ersten Falte stehen mindestens vier Jahre Training. Die
   Kursdateien reichen fuer die Aktien Jahrzehnte zurueck; die Schranke
   bindet dort nicht, sie ist die Regel, die auch fuer Krypto gelten wird.

3. **Krypto: Platzhalter mit Regel, keine Jahreszahlen.** Die Kursdaten
   beginnen heute erst 09/2021. Nach dem Mindesttraining blieben ZWEI
   Testfalten - zu wenig fuer einen Median ueber Falten. TB-31 laedt die
   Historie ueber /api/v3/klines zurueck. Der Krypto-Faltenplan wird
   geschrieben, sobald TB-31 gemeldet hat, ab wann die Daten JE SYMBOL
   reichen; bis dahin steht hier die Regel und der Platzhalter, den sie
   erzeugt.

4. **2020 und 2022 sind Testfalten, keine Trainingsjahre.** Das steht hier,
   weil es die einzige Stelle ist, an der die Versuchung entstehen koennte,
   ein schweres Jahr ins Training zu schieben.

5. **Purge und Embargo** in Hoehe der MAXIMALEN gemessenen Haltedauer des
   Bots (aus research/tb24_haltedauern/). Purge: der Rand vor der Falte
   faellt aus dem Training. Embargo: nach dem Ende einer Falte faellt
   dieselbe Laenge aus dem Training aller SPAETEREN Falten - sonst lernt
   Falte f+1 auf Positionen, die in Falte f noch offen waren.

6. **Faltenlaenge ein Jahr, zwei Jahre bei unter 30 gefundenen Trades je
   Jahr.** Welche Bots das trifft, steht VOR dem Lauf fest und wird hier aus
   den TB-24-Trades gerechnet, nicht geschaetzt.

7. **Die letzte Falte wird NICHT selektiert.** Sie ist die
   Bestaetigungsperiode: einmal ausgewertet, nachdem die Auswahl steht, und
   berichtet wie sie ausfaellt. Kein Veto. Sie waechst jeden Monat.

8. **Falten ohne Trade zaehlen mit Sharpe 0** - das steht in der Auswertung,
   nicht hier, gehoert aber zur selben Festlegung: Auslassen belohnt Saetze,
   die in schweren Jahren nicht handeln.

ZUM GO-LIVE-SCHNITT
------------------------------------------------------------------------------
Alle neun Bots laufen seit Anfang September 2026 im Paper-Trading; die
Kursdateien dieses Repos enden am 2026-09-01 (Aktien) bzw. 2026-08-31
(Krypto). Der Schnitt liegt deshalb auf **2026-09-01**, ausschliesslich:
alles davor ist Backtest-Material, alles ab diesem Tag ist Forward-Test und
geht in KEINE Selektion ein - auch nicht in die Bestaetigungsperiode.
"""

import json
import math
import os
import sys
from datetime import date, timedelta

import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB30A_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))

import registerdaten as rd  # noqa: E402

TB24_DATEN = os.path.join(BASE_DIR, "research", "tb24_haltedauern", "daten")


def gefundene_trades_je_jahr(bot: str) -> dict:
    """Gefundene (nicht: ausgefuehrte) Trades je Kalenderjahr aus TB-24.

    Gezaehlt werden die GEFUNDENEN Trades: ob ein Trade ausgefuehrt wird,
    haengt am Positionslimit - und das ist in diesem Lauf ein Rasterparameter.
    Eine Faltenlaenge, die vom Positionslimit abhinge, waere keine Festlegung
    vor dem Lauf.
    """
    pfad = os.path.join(TB24_DATEN, f"{bot}_alle_trades.csv")
    df = pd.read_csv(pfad, parse_dates=["entry_time"])
    jahre = df["entry_time"].dt.year
    return {int(j): int(n) for j, n in jahre.value_counts().sort_index().items()}


def volle_jahre(zaehlung: dict) -> dict:
    """Nur Kalenderjahre, die ueber die ganze Laenge belegt sind.

    Das erste und das letzte Jahr einer Messung sind angeschnitten; sie
    wuerden die Trades je Jahr nach unten ziehen und einen Bot faelschlich
    in die Zweijahres-Falten schieben.
    """
    if not zaehlung:
        return {}
    jahre = sorted(zaehlung)
    return {j: zaehlung[j] for j in jahre[1:-1]} or {jahre[0]: zaehlung[jahre[0]]}


def faltenlaenge_jahre(bot: str) -> tuple:
    """(Laenge in Jahren, Trades je Jahr, Begruendung) - Festlegung 7."""
    zaehlung = volle_jahre(gefundene_trades_je_jahr(bot))
    if not zaehlung:
        return 2, 0.0, "keine vollen Kalenderjahre gemessen"
    mittel = sum(zaehlung.values()) / len(zaehlung)
    if mittel < rd.ZWEIJAHRES_SCHWELLE_TRADES:
        return 2, mittel, (f"{mittel:.1f} gefundene Trades je vollem Kalenderjahr "
                           f"liegen unter der Schwelle von "
                           f"{rd.ZWEIJAHRES_SCHWELLE_TRADES}")
    return 1, mittel, (f"{mittel:.1f} gefundene Trades je vollem Kalenderjahr "
                       f"liegen ueber der Schwelle von "
                       f"{rd.ZWEIJAHRES_SCHWELLE_TRADES}")


def purge_tage(bot: str, mess: dict) -> int:
    """Purge- und Embargo-Laenge: die maximale gemessene Haltedauer, aufgerundet."""
    return int(math.ceil(mess["haltedauer"][bot]["max_tage"]))


def _jahresfalten(von_jahr: int, bis_ausschliesslich: date, laenge: int) -> list:
    """Kalenderjahr-Falten der gegebenen Laenge, aufsteigend.

    Die letzte Falte darf angeschnitten sein - sie ist die
    Bestaetigungsperiode und waechst jeden Monat.
    """
    falten = []
    jahr = von_jahr
    while date(jahr, 1, 1) < bis_ausschliesslich:
        ende = date(jahr + laenge, 1, 1)
        angeschnitten = ende > bis_ausschliesslich
        if angeschnitten:
            ende = bis_ausschliesslich
        falten.append({
            "von": date(jahr, 1, 1).isoformat(),
            "bis_ausschliesslich": ende.isoformat(),
            "name": (f"{jahr}" if laenge == 1 else f"{jahr}-{jahr + laenge - 1}"),
            "angeschnitten": angeschnitten,
        })
        jahr += laenge
    return falten


def plan_aktien(bot: str, mess: dict) -> dict:
    laenge, trades, begruendung = faltenlaenge_jahre(bot)
    schnitt = date.fromisoformat(rd.GO_LIVE_SCHNITT)
    falten = _jahresfalten(rd.ERSTE_MOEGLICHE_FALTE, schnitt, laenge)
    purge = purge_tage(bot, mess)
    for i, f in enumerate(falten):
        von = date.fromisoformat(f["von"])
        f["rolle"] = "bestaetigung" if i == len(falten) - 1 else "selektion"
        f["training_bis_ausschliesslich"] = (von - timedelta(days=purge)).isoformat()
        f["embargo_nach_falten"] = [g["name"] for g in falten[:i]]
    return {
        "markt": "aktien",
        "status": "endgueltig",
        "faltenlaenge_jahre": laenge,
        "trades_je_jahr": round(trades, 1),
        "faltenlaenge_begruendung": begruendung,
        "purge_tage": purge,
        "embargo_tage": purge,
        "mindesttraining_jahre": rd.MINDESTTRAINING_JAHRE,
        "go_live_schnitt": rd.GO_LIVE_SCHNITT,
        "falten": falten,
        "selektionsfalten": [f["name"] for f in falten if f["rolle"] == "selektion"],
        "bestaetigungsperiode": falten[-1]["name"] if falten else None,
    }


def plan_krypto(bot: str, mess: dict) -> dict:
    """Platzhalter MIT REGEL - keine Jahreszahlen bis TB-31 gemeldet hat."""
    laenge, trades, begruendung = faltenlaenge_jahre(bot)
    purge = purge_tage(bot, mess)
    bereich = mess["datenbereiche"].get(f"krypto_{rd.BOTS[bot]['zeitrahmen']}", {})
    heute_beginn = bereich.get("frueheste")
    return {
        "markt": "krypto",
        "status": "platzhalter",
        "faltenlaenge_jahre": laenge,
        "trades_je_jahr": round(trades, 1),
        "faltenlaenge_begruendung": begruendung,
        "purge_tage": purge,
        "embargo_tage": purge,
        "mindesttraining_jahre": rd.MINDESTTRAINING_JAHRE,
        "go_live_schnitt": rd.GO_LIVE_SCHNITT,
        "datenbeginn_heute": heute_beginn,
        "regel": (
            "Erste Testfalte ist das erste volle Kalenderjahr, vor dem JE "
            "SYMBOL mindestens {n} Jahre Kursdaten liegen, fruehestens {e}. "
            "Danach lueckenlose Falten der Laenge {l} Jahr(e) bis zum "
            "Go-Live-Schnitt {s}; die letzte Falte ist die "
            "Bestaetigungsperiode. Ein Symbol geht in eine Falte nur ein, "
            "wenn seine Kursdaten mindestens {n} Jahre vor Faltenbeginn "
            "einsetzen (point-in-time)."
        ).format(n=rd.MINDESTTRAINING_JAHRE, e=rd.ERSTE_MOEGLICHE_FALTE,
                 l=laenge, s=rd.GO_LIVE_SCHNITT),
        "warum_platzhalter": (
            f"Die Kursdaten dieses Repos beginnen fuer Krypto am "
            f"{heute_beginn}. Nach {rd.MINDESTTRAINING_JAHRE} Jahren "
            f"Mindesttraining blieben zwei Testfalten - zu wenig fuer einen "
            f"Median ueber Falten. TB-31 laedt die Historie zurueck; erst "
            f"dann steht fest, ab welchem Jahr die Regel greift."),
        "falten": [],
        "selektionsfalten": [],
        "bestaetigungsperiode": None,
    }


def faltenplan(mess=None) -> dict:
    mess = mess or rd._mess()
    return {bot: (plan_aktien(bot, mess) if eig["markt"] == "aktien"
                  else plan_krypto(bot, mess))
            for bot, eig in rd.BOTS.items()}


def main():
    mess = rd._mess()
    plan = faltenplan(mess)
    print(__doc__.strip().split("\n")[0])
    print(f"\nGo-Live-Schnitt: {rd.GO_LIVE_SCHNITT} (ausschliesslich)\n")
    print(f"{'Bot':28s} {'Markt':7s} {'Laenge':>7s} {'Trades/J':>9s} "
          f"{'Purge':>6s} {'Selektionsfalten':>17s} {'Bestaetigung':>13s}")
    for bot, p in plan.items():
        sel = ", ".join(p["selektionsfalten"]) or "(TB-31)"
        best = p["bestaetigungsperiode"] or "(TB-31)"
        print(f"{bot:28s} {p['markt']:7s} {p['faltenlaenge_jahre']:6d}J "
              f"{p['trades_je_jahr']:9.1f} {p['purge_tage']:5d}T  "
              f"{sel[:40]:40s} {best}")
    ziel = os.path.join(_HIER, "ergebnisse", "faltenplan.json")
    with open(ziel, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    print(f"\nGeschrieben: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
