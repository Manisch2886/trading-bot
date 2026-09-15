#!/usr/bin/env python3
"""
Wie viele Testfalten sind je Krypto-Bot moeglich? (TB-31)
==============================================================================
Rein lesend. Fasst keinen Bot-Code, keine Parametrisierung und keine
Kursdatei an - es rechnet nur nach, was aus der vorhandenen Historie folgt.

Die Regel ist nicht erfunden, sie steht in
`docs/VORREGISTRIERUNG_neuselektion.md`, Abschnitt 5.3:

  > Erste Testfalte ist das erste volle Kalenderjahr, vor dem **je Symbol**
  > mindestens vier Jahre Kursdaten liegen, fruehestens 2019. Danach
  > lueckenlose Falten der jeweiligen Laenge bis zum Go-Live-Schnitt; die
  > letzte Falte ist die Bestaetigungsperiode. Ein Symbol geht in eine Falte
  > nur ein, wenn seine Kursdaten mindestens vier Jahre vor Faltenbeginn
  > einsetzen (point-in-time).

Zwei Lesarten - und warum hier die erste gilt
------------------------------------------------------------------------------
"vor dem **je Symbol** mindestens vier Jahre Kursdaten liegen" laesst offen,
ob das fuer **ein** Symbol oder fuer **alle** gelten muss.

* **Alle Symbole:** das juengste Paar des Universums (`UUSDT`, gelistet
  2026-01-13) wuerde die erste Falte auf **2031** schieben. Es gaebe keine
  Selektion, nie.
* **Mindestens ein Symbol**, zusammen mit dem point-in-time-Satz im letzten
  Satz der Regel: der Faltenplan beginnt, sobald das erste Paar so weit
  zurueckreicht, und jedes Symbol tritt dann ein, sobald es selbst die vier
  Jahre erfuellt.

Nur die zweite Lesart ergibt einen Plan. Dieses Werkzeug rechnet mit ihr und
weist die erste in der Ausgabe mit aus, damit die Festlegung sichtbar
getroffen und nicht stillschweigend unterstellt wird.

Der Punkt, um den es eigentlich geht
------------------------------------------------------------------------------
Nicht die Zahl der Falten, sondern **wer in ihnen vorkommt**. Der
point-in-time-Satz schliesst jedes spaet gelistete Paar aus jeder frueheren
Falte aus. Uebrig bleiben die Paare, die am laengsten am Markt sind - und das
sind per Konstruktion die, die den Zyklus 2018 und den Baerenmarkt 2022
**ueberlebt** haben. Die Selektion wird also auf einer Teilmenge entschieden,
die der Bot spaeter gar nicht handelt. Dieses Werkzeug weist diese Teilmenge
je Falte aus; gluetten laesst sich das nicht, benennen schon.

    python3 research/krypto_historie/faltenplan.py
    python3 research/krypto_historie/faltenplan.py --mindesttraining 2
    python3 research/krypto_historie/faltenplan.py --json bericht.json
"""

import argparse
import datetime as dt
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))
_SHARED_DIR = os.path.join(BASE_DIR, "shared")
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

# Festlegungen aus docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 5.1/5.2/5.3
GO_LIVE = dt.date(2026, 9, 1)           # ausschliesslich
FRUEHESTE_FALTE = 2019
MINDESTTRAINING_JAHRE = 4

# Bot -> (Zeitrahmen, Faltenlaenge in Jahren). Die Faltenlaengen stehen in
# Abschnitt 5.4 des Registers: ein Jahr, zwei Jahre bei unter 30 gefundenen
# Trades je Jahr - was genau einen Bot trifft.
KRYPTO_BOTS = {
    "elliott_wave":                ("1h", 2),
    "t3_supertrend":               ("4h", 1),
    "rsi2_crypto":                 ("1d", 1),
    "turtle_soup_crypto":          ("1d", 1),
    "volatility_breakout_crypto":  ("1d", 1),
}

# Die Marktphasen, nach denen der Auftrag ausdruecklich fragt.
MARKTPHASEN = [
    ("Zyklus 2018 (Hoch 2017-12, Baerenmarkt 2018)", dt.date(2017, 12, 1), dt.date(2018, 12, 31)),
    ("Einbruch Maerz 2020",                          dt.date(2020, 2, 20), dt.date(2020, 4, 30)),
    ("Baerenmarkt 2022",                             dt.date(2022, 1, 1),  dt.date(2022, 12, 31)),
]


def minus_jahre(datum, jahre):
    """Datum minus n Jahre, schaltjahrfest (29.02. -> 28.02.)."""
    try:
        return datum.replace(year=datum.year - jahre)
    except ValueError:
        return datum.replace(year=datum.year - jahre, day=28)


def symbol_beginn(datenordner, symbole, zeitrahmen):
    """{Symbol -> Datum} des ersten Zeitstempels der jeweiligen Kursdatei.

    Gemessen, nicht angenommen: gelesen wird die erste Datenzeile der Datei.
    Symbole ohne Datei fehlen im Ergebnis und werden getrennt gemeldet.
    """
    beginn, ohne_datei = {}, []
    for symbol in symbole:
        pfad = os.path.join(datenordner, f"{symbol}_{zeitrahmen}.csv")
        if not os.path.exists(pfad):
            ohne_datei.append(symbol)
            continue
        with open(pfad, "r", encoding="utf-8") as datei:
            datei.readline()
            erste = datei.readline().strip()
        if not erste:
            ohne_datei.append(symbol)
            continue
        beginn[symbol] = dt.date.fromisoformat(erste.split(",")[0][:10])
    return beginn, ohne_datei


def erste_faltenjahr(beginn, mindesttraining=MINDESTTRAINING_JAHRE,
                     fruehestens=FRUEHESTE_FALTE):
    """Das erste volle Kalenderjahr, vor dem MINDESTENS EIN Symbol die
    geforderte Vorlaufzeit hat. Gibt None, wenn kein Jahr vor dem
    Go-Live-Schnitt liegt."""
    if not beginn:
        return None
    frueheste_daten = min(beginn.values())
    jahr = max(fruehestens, frueheste_daten.year)
    while jahr <= GO_LIVE.year:
        if minus_jahre(dt.date(jahr, 1, 1), mindesttraining) >= frueheste_daten:
            return jahr
        jahr += 1
    return None


def falten(erstes_jahr, laenge):
    """Lueckenlose Falten der Laenge `laenge` ab `erstes_jahr` bis zum
    Go-Live-Schnitt. Die letzte ist die Bestaetigungsperiode (Regel 7)."""
    if erstes_jahr is None:
        return []
    bloecke = []
    jahr = erstes_jahr
    while jahr <= GO_LIVE.year:
        beginn = dt.date(jahr, 1, 1)
        ende = min(dt.date(jahr + laenge, 1, 1), GO_LIVE)
        bloecke.append({"von": beginn, "bis_ausschliesslich": ende,
                        "jahre": list(range(jahr, min(jahr + laenge, GO_LIVE.year + 1)))})
        jahr += laenge
    return bloecke


def symbole_in_falte(beginn, faltenbeginn, mindesttraining=MINDESTTRAINING_JAHRE):
    """Die Symbole, deren Kursdaten mindestens `mindesttraining` Jahre vor
    Faltenbeginn einsetzen (point-in-time)."""
    grenze = minus_jahre(faltenbeginn, mindesttraining)
    return sorted(s for s, d in beginn.items() if d <= grenze)


def beginn_aus_messung(pfad, symbole, zeitrahmen):
    """{Symbol -> Datum} aus dem JSON-Bericht von
    `shared/binance_historie.py --messen`.

    Damit rechnet dasselbe Werkzeug den Faltenplan wahlweise aus den Dateien
    im Repo **oder** aus der frisch gemessenen Reichweite des Endpunkts -
    ohne dass dafuer eine einzige Kursdatei angefasst werden muesste.
    """
    with open(pfad, "r", encoding="utf-8") as datei:
        bericht = json.load(datei)
    messung = bericht.get("messung", bericht)
    beginn, ohne_datei = {}, []
    for symbol in symbole:
        eintrag = (messung.get(symbol) or {}).get(zeitrahmen) or {}
        tag = eintrag.get("beginn_tag") or (eintrag.get("beginn") or "")[:10]
        if not tag:
            ohne_datei.append(symbol)
            continue
        beginn[symbol] = dt.date.fromisoformat(tag)
    return beginn, ohne_datei


def plan_fuer_bot(bot, datenordner, symbole, mindesttraining=MINDESTTRAINING_JAHRE,
                  messung=None):
    zeitrahmen, laenge = KRYPTO_BOTS[bot]
    if messung:
        beginn, ohne_datei = beginn_aus_messung(messung, symbole, zeitrahmen)
    else:
        beginn, ohne_datei = symbol_beginn(datenordner, symbole, zeitrahmen)
    erstes = erste_faltenjahr(beginn, mindesttraining)
    bloecke = falten(erstes, laenge)
    for block in bloecke:
        block["symbole"] = symbole_in_falte(beginn, block["von"], mindesttraining)
    selektion = bloecke[:-1] if bloecke else []
    bestaetigung = bloecke[-1] if bloecke else None
    return {
        "bot": bot, "zeitrahmen": zeitrahmen, "faltenlaenge": laenge,
        "symbole_gesamt": len(beginn), "ohne_datei": ohne_datei,
        "datenbeginn_frueheste": min(beginn.values()).isoformat() if beginn else None,
        "datenbeginn_spaeteste": max(beginn.values()).isoformat() if beginn else None,
        "erstes_faltenjahr": erstes,
        "selektionsfalten": selektion,
        "bestaetigungsperiode": bestaetigung,
        "anzahl_selektionsfalten": len(selektion),
        "symbole_je_beginn": {s: d.isoformat() for s, d in sorted(beginn.items())},
    }


def marktphasen_abgedeckt(datenbeginn):
    """Welche der drei interessanten Phasen die Historie ueberhaupt enthaelt."""
    abdeckung = []
    for name, von, bis in MARKTPHASEN:
        if datenbeginn is None:
            zustand = "unbekannt"
        elif datenbeginn <= von:
            zustand = "vollstaendig"
        elif datenbeginn <= bis:
            zustand = "teilweise"
        else:
            zustand = "fehlt"
        abdeckung.append({"phase": name, "von": von.isoformat(), "bis": bis.isoformat(),
                          "zustand": zustand})
    return abdeckung


# ---------------------------------------------------------------------------
def _block_text(block):
    jahre = block["jahre"]
    spanne = str(jahre[0]) if len(jahre) == 1 else f"{jahre[0]}-{jahre[-1]}"
    angeschnitten = "" if block["bis_ausschliesslich"] != GO_LIVE else " (bis Go-Live-Schnitt)"
    return f"{spanne}{angeschnitten}"


def main(argv=None) -> int:
    from paths import DATA_DIR                             # noqa: PLC0415
    from symbols_config import SYMBOLS                     # noqa: PLC0415

    zerleger = argparse.ArgumentParser(
        description="Rechnet den Krypto-Faltenplan aus der vorhandenen Historie nach.")
    zerleger.add_argument("--ordner", default=DATA_DIR)
    zerleger.add_argument("--mindesttraining", type=int, default=MINDESTTRAINING_JAHRE,
                          help="Jahre Mindesttraining vor der ersten Falte "
                               "(Register: 4)")
    zerleger.add_argument("--messung", default=None,
                          help="JSON-Bericht von 'binance_historie.py --messen' "
                               "statt der Dateien unter --ordner")
    zerleger.add_argument("--json", default=None)
    argumente = zerleger.parse_args(argv)

    symbole = list(SYMBOLS)
    print("=" * 78)
    print("Krypto-Faltenplan aus der Historie unter "
          + (argumente.messung or argumente.ordner))
    if argumente.messung:
        print(f"Quelle: gemessene Reichweite des Endpunkts aus {argumente.messung}")
    print(f"Go-Live-Schnitt {GO_LIVE.isoformat()} (ausschliesslich), "
          f"Mindesttraining {argumente.mindesttraining} Jahr(e), "
          f"frueheste Falte {FRUEHESTE_FALTE}")
    print("=" * 78)

    plaene = {}
    for bot in sorted(KRYPTO_BOTS):
        plaene[bot] = plan_fuer_bot(bot, argumente.ordner, symbole,
                                    argumente.mindesttraining,
                                    messung=argumente.messung)

    print(f"\n{'Bot':<28}{'ZR':<4}{'Laenge':<8}{'Datenbeginn':<13}"
          f"{'1. Falte':<10}{'#Sel':<6}Selektionsfalten / Bestaetigung")
    print("-" * 110)
    for bot in sorted(plaene):
        p = plaene[bot]
        bestaetigung = (_block_text(p["bestaetigungsperiode"])
                        if p["bestaetigungsperiode"] else "-")
        falten_text = ", ".join(_block_text(b) for b in p["selektionsfalten"]) or "KEINE"
        print(f"{bot:<28}{p['zeitrahmen']:<4}{str(p['faltenlaenge']) + ' J':<8}"
              f"{str(p['datenbeginn_frueheste']):<13}"
              f"{str(p['erstes_faltenjahr'] or '-'):<10}"
              f"{p['anzahl_selektionsfalten']:<6}"
              f"{falten_text}  |  Best.: {bestaetigung}")

    if all(p["anzahl_selektionsfalten"] == 0 for p in plaene.values()):
        print("\n!! KEIN Bot hat eine einzige Selektionsfalte. Nach Regel 7 ist die")
        print("   letzte Falte die Bestaetigungsperiode - bleibt nur eine, ist sie es,")
        print("   und es wird nichts selektiert. Ein Median ueber null Falten existiert")
        print("   nicht; `auswertung.py` verweigert hier zu Recht die Auswertung.")

    # Wer kommt in welcher Falte ueberhaupt vor?
    beispiel = plaene["rsi2_crypto"]
    if beispiel["selektionsfalten"]:
        print(f"\nSymbole je Falte (Beispiel {beispiel['bot']}, Zeitrahmen "
              f"{beispiel['zeitrahmen']}, point-in-time-Regel):")
        for block in beispiel["selektionsfalten"] + [beispiel["bestaetigungsperiode"]]:
            rolle = ("Bestaetigung" if block is beispiel["bestaetigungsperiode"]
                     else "Selektion")
            print(f"  {_block_text(block):<22} {rolle:<13} "
                  f"{len(block['symbole']):>2} von {beispiel['symbole_gesamt']} Symbolen")
    nie_dabei = sorted(set(beispiel["symbole_je_beginn"]) - {
        s for block in beispiel["selektionsfalten"] for s in block["symbole"]})
    if nie_dabei and beispiel["selektionsfalten"]:
        print(f"\n{len(nie_dabei)} von {beispiel['symbole_gesamt']} Symbolen kommen in "
              f"KEINER Selektionsfalte vor:")
        for symbol in nie_dabei:
            print(f"  {symbol:<12} ab {beispiel['symbole_je_beginn'][symbol]}")
        print("  Die Selektion entscheidet damit auf einer Teilmenge, die der Bot")
        print("  spaeter nicht allein handelt - und es ist die Teilmenge der")
        print("  laengstlebenden Paare. Das ist die survivorship-nahe Verzerrung.")

    datenbeginn = (dt.date.fromisoformat(beispiel["datenbeginn_frueheste"])
                   if beispiel["datenbeginn_frueheste"] else None)
    print("\nMarktphasen in der Historie:")
    for eintrag in marktphasen_abgedeckt(datenbeginn):
        print(f"  {eintrag['zustand']:<14} {eintrag['phase']}")

    if argumente.json:
        with open(argumente.json, "w", encoding="utf-8") as datei:
            json.dump({"mindesttraining": argumente.mindesttraining,
                       "go_live": GO_LIVE.isoformat(),
                       "plaene": plaene,
                       "marktphasen": marktphasen_abgedeckt(datenbeginn)},
                      datei, indent=2, sort_keys=True, default=str)
        print(f"\nBericht: {argumente.json}")

    print("\nRein lesend - es wurde nichts geaendert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
