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

2. **Testfalten sind Kalenderjahre ab der ersten Falte nach Registertext
   4a bis zum Go-Live-Schnitt - fuer alle neun Bots nach derselben Regel.**
   Die erste Falte ist das erste Kalenderjahr, in dem am 1. Januar Universum
   und Indikator-Vorlauf vorliegen - JE BOT aus der Datenlage gerechnet
   (`erste_falte()`, mit der Regel aus `research/faltenplan_neun/`), nicht
   aus einer Konstante.
   ⚠️ Bis TB-56 (19.09.2026) stand hier `ERSTE_MOEGLICHE_FALTE = 2019`. Die
   Schranke stand in keinem Registertext; die Tatsachennotiz 15.6 Punkt 2
   hatte den Code-Zustand als Registerregel ausgegeben. Gemessen vor der
   Entfernung (docs/ERGEBNIS_TB-56_faltenschranke.md): ohne Schranke beginnen
   die Aktienplaene 2017 (elliott_wave_stocks, turtle_soup_stocks) bzw. 2018
   (rsi2_mean_reversion, volatility_breakout) - nicht in einem gemeinsamen
   Jahr, weil der Indikator-Vorlauf je Bot verschieden ist.
   Vor der ersten Falte stehen mindestens vier Jahre Training (Verfahren A);
   die Kursdateien reichen fuer die Aktien Jahrzehnte zurueck, das
   Mindesttraining bindet dort nicht.

3. **Krypto rechnet seit TB-61 (20.09.2026) nach derselben Regel wie
   Aktien.** Bis dahin stand hier ein Platzhalter ohne Jahreszahlen: die
   Kursdaten begannen zur Zeit von TB-30a erst 09/2021, und der Platzhalter
   wartete auf TB-31. TB-31 hat die Historie ueber /api/v3/klines
   zurueckgeladen (Kursdaten ab 2017-08-17), TB-34 hat den Kursbestand neu
   aufgebaut; der Krypto-Faltenplan steht gemessen in Register Abschnitt 21.
   ⚠️ Diese Regel ist Registertext 4a allein. Register 21.3 (b) laesst bei
   Abweichung 3b (a) binden (Trockenlauf des Laufcodes); das rechnet dieses
   Modul nicht, und fuer `t3_supertrend` weichen beide ab (4a: 2018,
   3b (a): 2019, weil `MIN_HISTORY_DAYS = 730` in der Falte 2018 kein Symbol
   handelbar macht) - siehe docs/ERGEBNIS_TB-61_benchmark_neun.md.

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

# Die Regel fuer die erste Falte (Registertext 4a) steht GENAU EINMAL - in
# research/faltenplan_neun/faltenplan_neun.py (reine Standardbibliothek).
# Sie wird ueber den Pfad importiert, nicht abgeschrieben.
sys.path.insert(0, os.path.join(BASE_DIR, "research", "faltenplan_neun"))
import faltenplan_neun as fn  # noqa: E402

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


def erste_falte(bot: str) -> int:
    """Das erste Kalenderjahr, in dem am 1. Januar Universum und
    Indikator-Vorlauf vorliegen - Registertext 4a, je Bot aus der Datenlage.

    Gerechnet mit der Regel aus `faltenplan_neun` (Kursdaten am 1. Januar,
    Zehnjahresfenster der Aktien-Bots, Indikator-Vorlauf in Balken). Bis zur
    Registerberichtigung TB-56b traegt `faltenplan_neun.erstes_faltenjahr`
    selbst noch die Schranke `FRUEHESTE_FALTE`; deshalb wird hier die
    ungebremste Fassung derselben Regel aufgerufen. Sobald TB-56b die
    Schranke dort entfernt hat, ist `erstes_faltenjahr` diese Funktion, und
    der Aufruf wechselt dorthin.
    """
    eig = fn.BOTS[bot]
    beginn = fn.symbolbeginn(bot, fn.fensteranker(eig["markt"]))
    jahr = fn._ungebremstes_faltenjahr(beginn)
    if jahr is None:
        raise ValueError(f"{bot}: kein Symbol mit Kursdaten - keine erste Falte")
    return jahr


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


def _plan(bot: str, mess: dict, markt: str) -> dict:
    """Der Faltenplan eines Bots - eine Regel fuer beide Maerkte (Regel 2)."""
    laenge, trades, begruendung = faltenlaenge_jahre(bot)
    schnitt = date.fromisoformat(rd.GO_LIVE_SCHNITT)
    erste = erste_falte(bot)
    falten = _jahresfalten(erste, schnitt, laenge)
    purge = purge_tage(bot, mess)
    for i, f in enumerate(falten):
        von = date.fromisoformat(f["von"])
        f["rolle"] = "bestaetigung" if i == len(falten) - 1 else "selektion"
        f["training_bis_ausschliesslich"] = (von - timedelta(days=purge)).isoformat()
        f["embargo_nach_falten"] = [g["name"] for g in falten[:i]]
    return {
        "markt": markt,
        "status": "endgueltig",
        "faltenlaenge_jahre": laenge,
        "trades_je_jahr": round(trades, 1),
        "faltenlaenge_begruendung": begruendung,
        "purge_tage": purge,
        "embargo_tage": purge,
        "mindesttraining_jahre": rd.MINDESTTRAINING_JAHRE,
        "go_live_schnitt": rd.GO_LIVE_SCHNITT,
        "erste_falte": erste,
        "erste_falte_quelle": ("Datenlage nach Registertext 4a: erstes Kalenderjahr, "
                               "in dem am 1. Januar Universum und Indikator-Vorlauf "
                               "vorliegen (research/faltenplan_neun); keine Konstante"),
        "falten": falten,
        "selektionsfalten": [f["name"] for f in falten if f["rolle"] == "selektion"],
        "bestaetigungsperiode": falten[-1]["name"] if falten else None,
    }


def plan_aktien(bot: str, mess: dict) -> dict:
    return _plan(bot, mess, "aktien")


def plan_krypto(bot: str, mess: dict) -> dict:
    """Seit TB-61 (20.09.2026) derselbe Plan wie bei Aktien, `status`
    `endgueltig`. Bis dahin ein Platzhalter mit Regel, der auf TB-31 wartete;
    TB-31 und TB-34 sind erledigt, der Plan kommt jetzt aus der Datenlage
    (Regel 3 im Modulkopf)."""
    return _plan(bot, mess, "krypto")


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
        sel = ", ".join(p["selektionsfalten"])
        best = p["bestaetigungsperiode"]
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
