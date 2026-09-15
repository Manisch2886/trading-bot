#!/usr/bin/env python3
"""
Das Embargo je Bot - Registertext 2d (TB-36)
==============================================================================
Rein lesend, reine Standardbibliothek. `live_params.py`, `forward_test.py` und
die Backtest-Dateien werden als **Text gelesen**, nie importiert - neun
gleichnamige Module kollidieren in `sys.modules`, und ein Import fuehrte
ausserdem Bot-Code aus, wo nur eine Zahl gebraucht wird.

DIE REGEL (Registertext 2d)
------------------------------------------------------------------------------
    Embargo = laengste Zeitbremse des Bots in Handelstagen + 1
    Bots ohne Zeitbremse: 95. Perzentil der Haltedauer + 1

"Handelstage" heisst bei Krypto Kalendertage - der Markt laeuft durch. Bei
Aktien ist ein Handelstag ein Boersentag; wo eine Zeitbremse in KALENDERtagen
notiert ist, wird die Umrechnung **an der Kursreihe gemessen**, nicht mit
5/7 geschaetzt (Feiertage).

WAS EINE ZEITBREMSE IST - UND WELCHER BOT KEINE HAT
------------------------------------------------------------------------------
Eine Zeitbremse ist der Notausstieg nach fester Zeit: `MAX_HOLD_DAYS` bzw.
`MAX_HOLD_HOURS`. **Acht der neun Bots haben eine**, und das ist nicht
geraten: TB-24 hat es gemessen (`research/tb24_haltedauern/BERICHT.md`,
Abschnitt 1) - "bei jedem der acht Bots mit Zeitausstieg liegt der Median der
Zeitausstiege exakt auf `MAX_HOLD_DAYS` bzw. `MAX_HOLD_HOURS`".

**Ohne Zeitbremse ist genau `t3_supertrend`.** Seine drei Ausstiegsarten sind
`stop_loss`, `trend_flip` und `t3_crossunder` (TB-24,
`daten/t3_supertrend_meta.json`) - keine davon ist eine Uhr. Fuer ihn gilt der
zweite Halbsatz der Regel.

DAS 95. PERZENTIL
------------------------------------------------------------------------------
Gerechnet auf denselben Positionen wie TB-24 (`daten/<bot>_positionen.csv`,
ausgefuehrte Positionen), Haltedauer als exakte Differenz
`exit_time - entry_time` in Tagen. Die Perzentilrechnung ist die lineare
Interpolation, die auch `pandas.Series.quantile` verwendet; dass sie
zeichengleich rechnet, prueft `test_faltenplan_neun.py` an den in TB-24
veroeffentlichten P90-Werten aller neun Bots nach.

Ein Embargo ist eine Zahl von Tagen. Ein gebrochenes Perzentil wird deshalb
**aufgerundet** - abrunden hiesse, den Rand kuerzer zu machen, als die
Messung ihn ausweist.

    python3 research/faltenplan_neun/embargo_neun.py
    python3 research/faltenplan_neun/embargo_neun.py --json bericht.json
"""

import argparse
import csv
import datetime as dt
import json
import math
import os
import re
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB36_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))

sys.path.insert(0, _HIER)

from faltenplan_neun import (BOTS, fensteranker, kursdatei,  # noqa: E402
                             symbole)

TB24_DATEN = os.path.join("research", "tb24_haltedauern", "daten")

# Wo die Zeitbremse jedes Bots steht. Ein Bot kann mehrere haben (Backtest und
# Live-Lauf getrennt notiert); die Regel verlangt die LAENGSTE, also werden
# alle gelesen und verglichen.
#
#   einheit "balken"       -> Balken des Bot-Zeitrahmens
#   einheit "kalendertage" -> echte Kalendertage (nur elliott_wave_stocks)
ZEITBREMSEN = {
    "elliott_wave": [
        ("strategies/elliott_wave/backtest_elliott.py", "MAX_HOLD_HOURS",
         "balken"),
        ("strategies/elliott_wave/forward_test.py", "MAX_HOLD_HOURS",
         "balken"),
    ],
    "t3_supertrend": [],
    "rsi2_crypto": [
        ("strategies/rsi2_crypto/live_params.py", "MAX_HOLD_DAYS", "balken"),
    ],
    "turtle_soup_crypto": [
        ("strategies/turtle_soup_crypto/live_params.py", "MAX_HOLD_DAYS",
         "balken"),
    ],
    "volatility_breakout_crypto": [
        ("strategies/volatility_breakout_crypto/live_params.py",
         "MAX_HOLD_DAYS", "balken"),
    ],
    "elliott_wave_stocks": [
        ("strategies/elliott_wave_stocks/backtest_elliott.py",
         "MAX_HOLD_HOURS", "balken"),
        ("strategies/elliott_wave_stocks/forward_test.py", "MAX_HOLD_DAYS",
         "kalendertage"),
    ],
    "rsi2_mean_reversion": [
        ("strategies/rsi2_mean_reversion/live_params.py", "MAX_HOLD_DAYS",
         "balken"),
    ],
    "turtle_soup_stocks": [
        ("strategies/turtle_soup_stocks/live_params.py", "MAX_HOLD_DAYS",
         "balken"),
    ],
    "volatility_breakout": [
        ("strategies/volatility_breakout/live_params.py", "MAX_HOLD_DAYS",
         "balken"),
    ],
}

# Stunden je Balken - nur zur Umrechnung von Balken in Tage bei Krypto.
BALKENSTUNDEN = {"1h": 1, "4h": 4, "1d": 24}


# ==============================================================================
# 1. Zahlen aus Bot-Dateien lesen (nie importieren)
# ==============================================================================
def lies_konstante(relpfad: str, name: str, basis: str = None):
    """Den Wert einer Modulkonstanten aus dem QUELLTEXT lesen.

    Gesucht wird eine Zuweisung auf oberster Ebene - `NAME = 123`. Zeilen mit
    Einrueckung zaehlen nicht (das waere eine lokale Variable), Kommentare
    hinter dem Wert werden abgeschnitten. Gibt None, wenn es die Zuweisung
    nicht gibt.
    """
    pfad = os.path.join(basis or BASE_DIR, relpfad)
    muster = re.compile(r"^" + re.escape(name) + r"\s*=\s*([0-9]+(?:\.[0-9]+)?)")
    with open(pfad, "r", encoding="utf-8") as datei:
        for nummer, zeile in enumerate(datei, start=1):
            treffer = muster.match(zeile)
            if treffer:
                roh = treffer.group(1)
                wert = float(roh) if "." in roh else int(roh)
                return wert, f"{relpfad}:{nummer}"
    return None, None


# ==============================================================================
# 2. Handelstage - gemessen, nicht geschaetzt
# ==============================================================================
def handelstage(markt: str, basis: str = None) -> list:
    """Die Boersentage des Marktes, aus den Kursdateien gesammelt.

    Krypto laeuft durch; dort ist jeder Kalendertag ein Handelstag. Bei Aktien
    ist es der Kalender, den die Kursdateien tatsaechlich zeigen - mit
    Feiertagen, ohne Annahme.
    """
    tage = set()
    for symbol in symbole(markt, basis):
        pfad = kursdatei(symbol, "1d", basis)
        if not os.path.exists(pfad):
            continue
        with open(pfad, "r", encoding="utf-8") as datei:
            datei.readline()
            for zeile in datei:
                zeile = zeile.strip()
                if zeile:
                    tage.add(zeile.split(",")[0][:10])
    return sorted(dt.date.fromisoformat(t) for t in tage)


def kalendertage_in_handelstagen(kalendertage: int, markt: str,
                                 basis: str = None) -> float:
    """Wie viele Handelstage in `kalendertage` Kalendertagen liegen (Median).

    Gemessen ueber alle Startpunkte im Auswertungsfenster: fuer jeden
    Handelstag d die Zahl der Handelstage in (d, d + n Kalendertage].
    """
    if markt == "krypto":
        return float(kalendertage)
    tage = handelstage(markt, basis)
    anker = fensteranker(markt, basis)
    if anker is not None:
        tage = [t for t in tage if t >= anker]
    if not tage:
        return float(kalendertage)
    zahlen = []
    j = 0
    for i, start in enumerate(tage):
        grenze = start + dt.timedelta(days=kalendertage)
        j = max(j, i + 1)
        while j < len(tage) and tage[j] <= grenze:
            j += 1
        if tage[-1] >= grenze:                 # nur vollstaendige Fenster
            zahlen.append(j - i - 1)
    if not zahlen:
        return float(kalendertage)
    zahlen.sort()
    mitte = len(zahlen) // 2
    return (float(zahlen[mitte]) if len(zahlen) % 2
            else (zahlen[mitte - 1] + zahlen[mitte]) / 2.0)


def balken_in_handelstagen(balken: int, bot: str, basis: str = None) -> float:
    """Balken des Bot-Zeitrahmens in Handelstagen.

    Tagesbalken sind Handelstage - eins zu eins, in beiden Maerkten. Stunden-
    und Vier-Stunden-Balken gibt es nur bei Krypto, dort ist ein Kalendertag
    ein Handelstag.
    """
    zeitrahmen = BOTS[bot]["zeitrahmen"]
    if zeitrahmen == "1d":
        return float(balken)
    return balken * BALKENSTUNDEN[zeitrahmen] / 24.0


# ==============================================================================
# 3. Das 95. Perzentil der Haltedauer
# ==============================================================================
def perzentil(werte, q: float):
    """Lineare Interpolation - zeichengleich zu `pandas.Series.quantile`."""
    s = sorted(werte)
    n = len(s)
    if n == 0:
        return None
    if n == 1:
        return float(s[0])
    pos = q * (n - 1)
    unten = math.floor(pos)
    oben = math.ceil(pos)
    if unten == oben:
        return float(s[unten])
    return float(s[unten] + (pos - unten) * (s[oben] - s[unten]))


def haltedauern_tage(bot: str, basis: str = None) -> list:
    """Haltedauer je ausgefuehrter Position in Tagen, aus den TB-24-Daten."""
    pfad = os.path.join(basis or BASE_DIR, TB24_DATEN, f"{bot}_positionen.csv")
    werte = []
    with open(pfad, "r", encoding="utf-8") as datei:
        for zeile in csv.DictReader(datei):
            ein = dt.datetime.fromisoformat(zeile["entry_time"])
            aus = dt.datetime.fromisoformat(zeile["exit_time"])
            werte.append((aus - ein).total_seconds() / 86400.0)
    return werte


# ==============================================================================
# 4. Das Embargo
# ==============================================================================
def embargo_fuer_bot(bot: str, basis: str = None) -> dict:
    markt = BOTS[bot]["markt"]
    bremsen = []
    for relpfad, name, einheit in ZEITBREMSEN[bot]:
        wert, herkunft = lies_konstante(relpfad, name, basis)
        if wert is None:
            continue
        if einheit == "balken":
            in_handelstagen = balken_in_handelstagen(wert, bot, basis)
        else:
            in_handelstagen = kalendertage_in_handelstagen(int(wert), markt,
                                                           basis)
        bremsen.append({
            "konstante": name, "wert": wert, "einheit": einheit,
            "herkunft": herkunft,
            "handelstage": round(in_handelstagen, 4),
        })

    if bremsen:
        laengste = max(bremsen, key=lambda b: b["handelstage"])
        grundlage = laengste["handelstage"]
        embargo = int(math.ceil(grundlage)) + 1
        art = "zeitbremse"
        p95 = None
    else:
        werte = haltedauern_tage(bot, basis)
        p95_roh = perzentil(werte, 0.95)
        # Bei Krypto ist ein Kalendertag ein Handelstag; t3_supertrend - der
        # einzige Bot ohne Zeitbremse - ist ein Krypto-Bot.
        grundlage = (p95_roh if markt == "krypto"
                     else kalendertage_in_handelstagen(int(math.ceil(p95_roh)),
                                                       markt, basis))
        embargo = int(math.ceil(grundlage)) + 1
        art = "perzentil"
        laengste = None
        p95 = {"p95_tage": round(p95_roh, 4), "n_positionen": len(werte),
               "herkunft": f"{TB24_DATEN}/{bot}_positionen.csv"}

    return {
        "bot": bot, "markt": markt, "zeitrahmen": BOTS[bot]["zeitrahmen"],
        "art": art,
        "zeitbremsen": bremsen,
        "laengste_zeitbremse": laengste,
        "perzentil95": p95,
        "grundlage_handelstage": round(grundlage, 4),
        "embargo_handelstage": embargo,
    }


def embargos(basis: str = None) -> dict:
    return {bot: embargo_fuer_bot(bot, basis) for bot in BOTS}


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Das Embargo je Bot nach Registertext 2d.")
    zerleger.add_argument("--json", default=None)
    argumente = zerleger.parse_args(argv)

    print("=" * 78)
    print("Embargo je Bot - Registertext 2d (TB-36)")
    print("Zeitbremse in Handelstagen + 1; ohne Zeitbremse: P95 + 1")
    print("=" * 78)
    ergebnis = embargos()

    print(f"\n{'Bot':<28}{'Art':<11}{'Grundlage':<30}{'Handelstage':>12}"
          f"{'Embargo':>9}")
    print("-" * 92)
    for bot, e in ergebnis.items():
        if e["art"] == "zeitbremse":
            b = e["laengste_zeitbremse"]
            grundlage = f"{b['konstante']} = {b['wert']:g} ({b['einheit']})"
        else:
            grundlage = f"P95 = {e['perzentil95']['p95_tage']:.2f} Tage"
        print(f"{bot:<28}{e['art']:<11}{grundlage:<30}"
              f"{e['grundlage_handelstage']:>12.2f}{e['embargo_handelstage']:>9}")

    print("\nHerkunft je Zahl")
    print("-" * 92)
    for bot, e in ergebnis.items():
        if e["art"] == "zeitbremse":
            for b in e["zeitbremsen"]:
                markierung = ("  <- laengste"
                              if b is e["laengste_zeitbremse"] else "")
                print(f"  {bot:<28}{b['konstante']} = {b['wert']:g} "
                      f"({b['einheit']}, {b['handelstage']:g} Handelstage)"
                      f"  aus {b['herkunft']}{markierung}")
        else:
            p = e["perzentil95"]
            print(f"  {bot:<28}keine Zeitbremse - P95 = {p['p95_tage']:.4f} "
                  f"Tage aus {p['n_positionen']} Positionen, {p['herkunft']}")

    if argumente.json:
        with open(argumente.json, "w", encoding="utf-8") as datei:
            json.dump(ergebnis, datei, indent=2, ensure_ascii=False,
                      sort_keys=True)
        print(f"\nBericht: {argumente.json}")

    print("\nRein lesend - es wurde nichts geaendert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
