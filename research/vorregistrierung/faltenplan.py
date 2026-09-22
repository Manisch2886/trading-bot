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
   Die erste Falte ist seit TB-72 (20.09.2026) das erste Kalenderjahr, das
   ZWEI Bedingungen erfuellt (Neufassung von 4a / 21.3 (b) als Konjunktion,
   Fable, docs/projektfuehrung/FABLE_ANTWORT_2026-09-20e_konjunktion.md):
   (i) es liegt im Datenhorizont des Bots und am 1. Januar ist der
   Indikator-Vorlauf erfuellt - JE BOT aus der Datenlage gerechnet
   (`erste_falte_4a()`, mit der Regel aus `research/faltenplan_neun/`),
   nicht aus einer Konstante; der Datenhorizont ist seit TB-80
   (21.09.2026) das absolute Datum je Bot aus Register 26.2 / 28.4
   (`HORIZONTBEGINN`, unten), nicht mehr die Datenuhr; UND (ii) der
   Loader des Bots macht in ihm an
   mindestens einem Handelstag mindestens ein Symbol handelbar - gemessen
   im Trockenlauf des Laufcodes (Registertext 3b (a), Lesart H;
   `research/faltenplan_neun/erste_falte_trockenlauf.py`), nicht
   nachgerechnet. `erste_falte()` fuehrt beide zusammen: 4a bleibt die
   Regel, der Trockenlauf ist ihre operative Form, der Plan ist eine
   Ableitung daraus und keine Parallelrechnung - er kann in keiner
   Richtung abweichen. (ii) kann den Beginn nie vorziehen, weil (i) weiter
   gelten muss; (i) nie, weil (ii) weiter gelten muss.
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
   ⚠️ Bis TB-72 (20.09.2026) stand hier: "Diese Regel ist Registertext 4a
   allein. Register 21.3 (b) laesst bei Abweichung 3b (a) binden
   (Trockenlauf des Laufcodes); das rechnet dieses Modul nicht, und fuer
   `t3_supertrend` weichen beide ab (4a: 2018, 3b (a): 2019, weil
   `MIN_HISTORY_DAYS = 730` in der Falte 2018 kein Symbol handelbar macht)"
   - siehe docs/ERGEBNIS_TB-61_benchmark_neun.md. Seit TB-72 rechnet
   `erste_falte()` Bedingung (ii) mit (Regel 2); `t3_supertrend` beginnt
   damit 2019, mit sieben Selektionsfalten statt acht. Gemessen in beide
   Richtungen (docs/ERGEBNIS_TB-72_schritt1_erste_falte.md): bei den acht
   anderen Bots liegt (ii) nicht spaeter als (i), ihr Plan aendert sich nicht.

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

import argparse
import hashlib
import json
import math
import os
import sys
from datetime import date, datetime, timedelta, timezone

import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB30A_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))

import registerdaten as rd  # noqa: E402

# Die Regel fuer die erste Falte (Registertext 4a) steht GENAU EINMAL - in
# research/faltenplan_neun/faltenplan_neun.py (reine Standardbibliothek).
# Sie wird ueber den Pfad importiert, nicht abgeschrieben. Dasselbe gilt seit
# TB-72 fuer Bedingung (ii), den Trockenlauf des Laufcodes (Registertext
# 3b (a)): research/faltenplan_neun/erste_falte_trockenlauf.py ruft den
# Loader jedes Bots im Kindprozess des TB-40-Werkzeugs auf; die Schranke
# MIN_HISTORY_* wirkt dort im Bot-Code und steht hier nirgends.
sys.path.insert(0, os.path.join(BASE_DIR, "research", "faltenplan_neun"))
import faltenplan_neun as fn  # noqa: E402
import erste_falte_trockenlauf as eft  # noqa: E402

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


# ==============================================================================
# Der Horizontbeginn - Bedingung (i), "im registrierten Datenhorizont des Bots"
# ==============================================================================
# Register 26.2 (TB-77, 21.09.2026), Registertext 4a, Praezisierung: "Der
# Datenhorizont eines Bots ist ein absolutes Datum je Bot: Horizontbeginn =
# asof (5a) minus RECENT_YEARS_ONLY des Bots; Bots ohne diese Konstante haben
# keinen Horizont (Krypto). [...] Es gilt fuer alle Symbole des Bots gleich."
# Der Wert steht in Register 28.4 (TB-78, gueltige Fassung der Tatsachennotiz
# zu 4d; asof = 2026-09-19 nach 28.3): elliott_wave_stocks, rsi2_mean_reversion,
# turtle_soup_stocks, volatility_breakout -> 2016-09-19; die fuenf Krypto-Bots
# -> kein Horizont.
#
# Er steht hier so, wie 28.4 ihn fuehrt - als absolutes Datum. NICHT als
# `asof - RECENT_YEARS_ONLY` gerechnet und NICHT aus
# strategies/*/multi_symbol_optimise.py gelesen: die vier Dateien stehen auf
# der Sperrliste, und eine Kopie ihrer Konstante waere der Fehler aus T56b.6
# (Konstantenkopien). Eine Quelle, keine Kopie.
#
# Bis TB-80 (21.09.2026) nahm `erste_falte_4a()` hier
# `fn.fensteranker(markt)`: zehn Jahre vor dem SPAETESTEN letzten Kurstag des
# Marktes - die Datenuhr, 2016-09-01 am Stand vom 21.09.2026 (Messung
# docs/belege/TB-80/schritt0_ausgangsstand.txt). Das ist genau der Bezug, den
# 26.2 abloest (28.4, "Abgegrenzt, damit es niemand verwechselt").
# `fensteranker` bleibt in faltenplan_neun bestehen; andere Stellen benutzen
# ihn (embargo_neun.py, faltenschranke_messung.py, plan_fuer_bot).
#
# ⚠️ Zwischenstand: ein benanntes Literal mit Registerfundstelle. Wo der
# Horizontbeginn dauerhaft lebt (registerdaten.py als registrierte Groesse,
# Register 26.6 letzte Zeilen / 28.7; aus dem Registertext gelesen; Literal
# mit Test gegen das Register), ist Entscheidungsvorlage in Register 32.5.
# research/faltenplan_neun/test_horizontbeginn.py liest den Wert aus dem
# Registertext 28.4 und vergleicht ihn mit diesem Literal.
HORIZONTBEGINN = {"aktien": date(2016, 9, 19), "krypto": None}


def horizontbeginn(bot: str):
    """Der Horizontbeginn des Bots (Register 26.2 / 28.4): ein absolutes
    Datum je Bot; None fuer Bots ohne Horizont (Krypto)."""
    return HORIZONTBEGINN[fn.BOTS[bot]["markt"]]


def erste_falte_4a_messung(bot: str) -> dict:
    """Bedingung (i) mit ihrer Messung: {horizontbeginn, warm_ab_fruehestes,
    erste_falte_4a} - damit im Plan steht, gegen welches Datum (i) gerechnet
    wurde und ab welchem Tag das erste Symbol warm ist, nicht nur das Jahr."""
    horizont = horizontbeginn(bot)
    beginn = fn.symbolbeginn(bot, horizont)
    jahr = fn._ungebremstes_faltenjahr(beginn)
    if jahr is None:
        raise ValueError(f"{bot}: kein Symbol mit Kursdaten - keine erste Falte")
    warm = min(w for _, w in beginn.values() if w is not None)
    return {"horizontbeginn": horizont.isoformat() if horizont else None,
            "warm_ab_fruehestes": warm.isoformat(),
            "erste_falte_4a": jahr}


def erste_falte_4a(bot: str) -> int:
    """Bedingung (i): das erste Kalenderjahr, in dem am 1. Januar Universum
    und Indikator-Vorlauf vorliegen - Registertext 4a, je Bot aus der
    Datenlage. Bis TB-72 hiess diese Funktion `erste_falte`.

    Gerechnet mit der Regel aus `faltenplan_neun` (Kursdaten am 1. Januar,
    Indikator-Vorlauf in Balken) ab dem Horizontbeginn des Bots
    (`HORIZONTBEGINN`, Register 26.2 / 28.4 - seit TB-80; bis dahin ab der
    Datenuhr `fn.fensteranker`, dem Zehnjahresfenster vor dem letzten
    Kurstag). Bis zur Registerberichtigung TB-56b traegt
    `faltenplan_neun.erstes_faltenjahr` selbst noch die Schranke
    `FRUEHESTE_FALTE`; deshalb wird hier die ungebremste Fassung derselben
    Regel aufgerufen. Sobald TB-56b die Schranke dort entfernt hat, ist
    `erstes_faltenjahr` diese Funktion, und der Aufruf wechselt dorthin.
    """
    return erste_falte_4a_messung(bot)["erste_falte_4a"]


def erste_falte(bot: str, laenge: int = None, schnitt: date = None) -> tuple:
    """(erste Falte, Messung) - die Konjunktion aus Regel 2.

    Die Kandidaten sind die Falten ab `erste_falte_4a` (Bedingung (i), die
    ab dort fuer jedes spaetere Jahr weiter gilt) bis zum Go-Live-Schnitt, im
    Raster der Faltenlaenge des Bots. Bedingung (ii) entscheidet ueber den
    Trockenlauf des Laufcodes (`erste_falte_trockenlauf.erste_falte_nach_3b`,
    Registertext 3b (a), Lesart H): die erste Kandidatenfalte, in der der
    Loader mindestens ein Symbol handelbar macht, ist die erste Falte. Die
    Messung nennt je gepruefter Falte die Menge H - damit steht im Plan, WARUM
    er dort beginnt, nicht nur dass.
    """
    if laenge is None:
        laenge = faltenlaenge_jahre(bot)[0]
    if schnitt is None:
        schnitt = date.fromisoformat(rd.GO_LIVE_SCHNITT)
    m4a = erste_falte_4a_messung(bot)
    erste_4a = m4a["erste_falte_4a"]
    kandidaten = _jahresfalten(erste_4a, schnitt, laenge)
    jahr, messung = eft.erste_falte_nach_3b(bot, kandidaten)
    if jahr is None:
        raise ValueError(f"{bot}: der Loader macht in keiner Falte ab {erste_4a} "
                         f"ein Symbol handelbar - keine erste Falte")
    return jahr, {"erste_falte_4a": erste_4a,
                  "horizontbeginn": m4a["horizontbeginn"],
                  "erste_falte_4a_warm_ab": m4a["warm_ab_fruehestes"],
                  "H_je_gepruefter_falte": [{"falte": f["name"], "H": f["H"]}
                                            for f in messung]}


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
    erste, herkunft = erste_falte(bot, laenge, schnitt)
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
        "erste_falte_quelle": ("Registertext 4a in der Neufassung als Konjunktion "
                               "(TB-72, 20.09.2026): erstes Kalenderjahr, das (i) im "
                               "Datenhorizont liegt - dem absoluten Datum je Bot aus "
                               "Register 26.2 / 28.4 (TB-80, 21.09.2026) - und am "
                               "1. Januar den Indikator-Vorlauf erfuellt (Datenlage, "
                               "research/faltenplan_neun; keine Konstante) UND (ii) in "
                               "dem der Loader des Bots mindestens ein Symbol "
                               "handelbar macht - Trockenlauf des Laufcodes, "
                               "Registertext 3b (a), Register 21.3 (b); 4a ist die "
                               "Regel, der Trockenlauf ihre operative Form, der Plan "
                               "eine Ableitung daraus"),
        "erste_falte_4a": herkunft["erste_falte_4a"],
        "horizontbeginn": herkunft["horizontbeginn"],
        "erste_falte_4a_warm_ab": herkunft["erste_falte_4a_warm_ab"],
        "erste_falte_trockenlauf_H": herkunft["H_je_gepruefter_falte"],
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


def _sha256_datei(pfad: str) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def voreinstellung_ziel() -> str:
    """Das voreingestellte Schreibziel - Registertext 36.1 (3), (4).

    ⚠️ Bis TB-86 (22.09.2026) schrieb `main()` fest verdrahtet nach
    `ergebnisse/faltenplan.json` - Sperrlistenpunkt 2. Ein einziger Aufruf
    ohne Argument haette die gesperrte Datei ueberschrieben. 36.1 (3): die
    Voreinstellung eines Erzeugers ist nie ein Pfad, der auf der Sperrliste
    steht; der gesperrte Pfad ist seither nur noch ueber `--ziel` erreichbar,
    wo die Sperre aus 36.1 (2) dann zuschlaegt.

    ⭐ Der Zeitstempel (UTC) ist kein Schmuck: Die Einmal-Schreibsperre bricht
    ab, sobald die Zieldatei existiert. Bei einem FESTEN Voreinstellungsnamen
    liesse sich `main()` nach dem ersten Lauf nie wieder aufrufen - die Sperre
    machte das Werkzeug unbrauchbar, statt es zu schuetzen. So ist jeder Lauf
    ein neuer Name.
    """
    stempel = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    return os.path.join(_HIER, "ergebnisse", f"faltenplan_{stempel}.json")


def schreibe_plan(plan: dict, ziel: str):
    """Schreibt den Plan GENAU EINMAL. Liefert (rueckgabewert, text).

    Registertext 36.1 (2), zeichengleich: *"Jeder Erzeuger einer solchen Datei
    schreibt einmalig: Existiert die Zieldatei bereits, bricht er ab
    (Rueckgabewert != 0), nennt Pfad und Hash der vorhandenen Datei und
    schreibt nichts. Er ueberschreibt nie, auch nicht mit identischem
    Inhalt."* Berichtigt durch 36.5 (Fable 22c): der Erzeuger, der wegen
    vorhandener Zieldatei nicht schreibt, endet mit **1** - er hat geprueft
    und einen Befund, nicht mit 2.

    ⛔ Kein Inhaltsvergleich. Fable, zeichengleich: *"Eine Sperre, die bei
    gleichem Inhalt durchlaesst, muss den Inhalt vergleichen - und wer den
    Vergleich programmiert, entscheidet, was 'gleich' heisst … Die Sperre ist
    staerker, wenn sie duemmer ist."*

        0   geschrieben, das Ziel existierte nicht
        1   BEFUND: Ziel existiert - Pfad und Hash genannt, nichts geschrieben
        2   NICHT PRUEFBAR: Zielordner fehlt, Ziel nicht anlegbar
    """
    if os.path.exists(ziel):
        try:
            h = _sha256_datei(ziel)
        except OSError:
            h = "(nicht lesbar)"
        return 1, (f"\nABBRUCH (36.1 (2)): Ziel existiert, nichts geschrieben."
                   f"\n  Pfad:    {ziel}\n  SHA-256: {h}")
    ordner = os.path.dirname(os.path.abspath(ziel))
    if not os.path.isdir(ordner):
        return 2, f"\nABBRUCH: Zielordner fehlt: {ordner}"
    try:
        # O_EXCL statt open(..., "w"): faengt auch ein Ziel ab, das zwischen
        # der Pruefung oben und dem Schreiben entsteht.
        fd = os.open(ziel, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        return 1, (f"\nABBRUCH (36.1 (2)): Ziel entstand waehrend des Laufs, "
                   f"nichts geschrieben.\n  Pfad:    {ziel}"
                   f"\n  SHA-256: {_sha256_datei(ziel)}")
    except OSError as e:
        return 2, f"\nABBRUCH: Ziel nicht anlegbar: {ziel} ({e})"
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    return 0, f"\nGeschrieben: {ziel}"


def main(argv=None):
    z = argparse.ArgumentParser(
        description="Rechnet den Faltenplan und schreibt ihn einmalig. "
                    "Voreinstellung ist ein Name mit Zeitstempel (36.1 (3)); "
                    "ein vorhandenes Ziel wird nie ueberschrieben (36.1 (2)).")
    z.add_argument("--ziel", default=None, metavar="PFAD",
                   help="Schreibziel (Standard: ergebnisse/faltenplan_<UTC-Stempel>.json). "
                        "⚠️ Auch mit --ziel gilt die Sperre: ein ausdrueckliches "
                        "Argument erlaubt einen ANDEREN Pfad, nicht das Ueberschreiben.")
    a = z.parse_args(argv)
    try:
        mess = rd._mess()
        plan = faltenplan(mess)
    except Exception:                       # nicht berechenbar ist 2, nie 0
        import traceback
        traceback.print_exc()
        print("\nABBRUCH: Plan nicht berechenbar - nichts geschrieben.",
              file=sys.stderr)
        return 2
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
    ziel = a.ziel or voreinstellung_ziel()
    rc, text = schreibe_plan(plan, ziel)
    print(text, file=sys.stderr if rc else sys.stdout)
    return rc


if __name__ == "__main__":
    sys.exit(main())
