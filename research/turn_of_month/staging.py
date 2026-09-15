#!/usr/bin/env python3
"""
TB-33 - Die Staging-Ebene (I19), minimal
==============================================================================
Eine Signalerzeugung, die **laeuft und protokolliert**, aber in **keine**
Portfolio-Zahl eingeht und **nicht** im Crash-Knopf auftaucht.

WARUM SIE HIER LIEGT UND NICHT UNTER strategies/
------------------------------------------------------------------------------
Das ist keine Geschmacksfrage, sondern der ganze Mechanismus:

  * `shared/ergebniskurven.finde_bots()` zaehlt die Ordner unter
    `strategies/` mit einer `equity_simulation.py`. Ein Ordner dort WAERE
    ein zehnter Bot - Flagge hin oder her.
  * `notifications/manual_close.SCHLIESSBARE_BOTS` ist die Liste, aus der
    `dashboard/schliessen.py` den Crash-Knopf speist. Sie ist hart
    geschrieben und wird hier NICHT angefasst.
  * `strategy_paths.get_strategy_paths()` legt `paper_trading_<name>.db`
    und `results/<name>/` an. Dieses Modul ruft es nicht auf und legt
    beides nicht an.

S-E1 ist also nicht deshalb unsichtbar, weil eine Flagge es versteckt,
sondern weil es in keiner der Listen steht, aus denen Portfolio-Zahlen und
Crash-Knopf gebildet werden. Eine Flagge im Quelltext waere eine Behauptung;
das hier ist eine Eigenschaft. Der Selbsttest prueft sie am **Verhalten**:
er laesst diesen Lauf wirklich laufen und sieht danach nach, ob sich an
Bot-Liste, Crash-Knopf-Liste, Datenbanken und `results/` etwas geaendert hat.

FRIST UND ENTSCHEIDUNGSKRITERIUM - BEIM ANLEGEN, NICHT DANACH
------------------------------------------------------------------------------
Beides steht in `register.py` und damit im Herkunfts-Hash. Eine Frist, die
erst festgelegt wird, wenn die Zahlen da sind, ist keine.

  Frist       12 protokollierte Monatswechsel ab dem ersten Signal,
              spaetestens bis 2027-09-30. Was zuerst eintritt.
  Kriterium   S1 Rang 3 hat ueber die neun Bots entschieden
              S2 der Backtest hat bestanden (B1, B2, B3)
              S3 mindestens 12 Forward-Ereignisse UND untere Grenze des
                 95-%-Bootstrap-Intervalls > 0

Trifft eines nicht zu, wird der Eintrag GESCHLOSSEN. Kein "vorerst
behalten" - dieselbe Schattenregel wie bei den neun Bots.

Nutzung:
    python3 research/turn_of_month/staging.py --lauf
    python3 research/turn_of_month/staging.py --status
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timezone

import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)

import handelstage as ht  # noqa: E402
import herkunft as hk  # noqa: E402
import kennzahlen as kz  # noqa: E402
import register as reg  # noqa: E402

STAGING_DIR = os.path.join(_HIER, "staging")
SIGNALE = os.path.join(STAGING_DIR, "signale.jsonl")

# Die Zusicherung in einer Zeile - sie steht in JEDEM Signal, damit sie
# nicht nur in diesem Docstring steht.
ZUSICHERUNG = ("Staging: kein Portfoliogewicht, kein Crash-Knopf, keine "
               "Datenbank, kein Eintrag unter results/.")


def fenstertage(daten_dir, symbol=None, fenster=None):
    """Je Monatswechsel die Kalendertage, an denen die Position offen ist.

    Dieselbe Quelle wie der Backtest: `handelstage`. Ein zweiter Weg, an
    dem zu entscheiden waere, was "-1" ist, waere genau die Art Wahl, die
    dieser Nulltest ausschliessen soll.
    """
    symbol = symbol or reg.KERNINSTRUMENT
    fenster = fenster or reg.KERNFENSTER
    df, _ = ht.lies_kursreihe(os.path.join(daten_dir, f"{symbol}_1d.csv"))
    ereignisse, _ = ht.ereignisse(df, fenster)
    tage = {}
    for _, e in ereignisse.iterrows():
        offen = df[(df["datum"] >= e["datum_einstieg"])
                   & (df["datum"] <= e["datum_ausstieg"])]["datum"]
        for d in offen:
            tage[d.date()] = {
                "einstieg": e["datum_einstieg"].date().isoformat(),
                "ausstieg": e["datum_ausstieg"].date().isoformat(),
                # Die Netto-Rendite steht erst am AUSSTIEGSTAG fest. An
                # jedem frueheren Tag ist sie None - und nicht etwa ein
                # Zwischenstand, der spaeter wie ein Ergebnis aussaehe.
                "netto_rendite": (float(e["netto_rendite"])
                                  if d == e["datum_ausstieg"] else None),
            }
    return tage


def signal(daten_dir, stand=None):
    """Das Signal fuer einen Stichtag. Schreibt nichts."""
    stand = stand or date.today()
    if isinstance(stand, str):
        stand = date.fromisoformat(stand)
    tage = fenstertage(daten_dir)
    treffer = tage.get(stand)
    return {
        "stand": stand.isoformat(),
        "zeitpunkt_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "instrument": reg.KERNINSTRUMENT,
        "fenster": f"{reg.KERNFENSTER[0]:+d}/{reg.KERNFENSTER[1]:+d}",
        "position": "long" if treffer else "flat",
        "ereignis": treffer,
        # Nur am Ausstiegstag gefuellt: vorher gibt es kein Ergebnis, und
        # eine Zahl, die es vorher gaebe, waere erfunden.
        "netto_rendite": (treffer or {}).get("netto_rendite"),
        # Nicht verhandelbar und deshalb konstant: ein Staging-Signal, das
        # sich ein Gewicht nehmen koennte, waere kein Staging-Signal.
        "portfoliogewicht": 0.0,
        "im_crash_knopf": False,
        "zusicherung": ZUSICHERUNG,
        "frist_ereignisse": reg.STAGING_FRIST_EREIGNISSE,
        "frist_datum": reg.STAGING_FRIST_DATUM,
        "kriterien": reg.STAGING_KRITERIEN,
        "herkunft": hk.block("staging", daten_dir),
    }


def protokolliere(daten_dir, stand=None):
    """Eine Zeile ans Signalprotokoll. Append-only, wie die Herkunft."""
    s = signal(daten_dir, stand)
    os.makedirs(STAGING_DIR, exist_ok=True)
    with open(SIGNALE, "a", encoding="utf-8") as f:
        f.write(json.dumps(s, ensure_ascii=False, sort_keys=True, default=str)
                + "\n")
    return s


def gelesene_signale():
    if not os.path.exists(SIGNALE):
        return []
    with open(SIGNALE, encoding="utf-8") as f:
        return [json.loads(z) for z in f.read().splitlines() if z.strip()]


def status(daten_dir=None):
    """Wo steht die Bestaetigungsperiode - und ist die Frist abgelaufen?"""
    zeilen = gelesene_signale()
    ereignisse = sorted({z["ereignis"]["einstieg"] for z in zeilen
                         if z.get("ereignis")
                         and z.get("netto_rendite") is not None})
    erstes = zeilen[0]["stand"] if zeilen else None
    heute = date.today().isoformat()
    frist_datum_erreicht = heute >= reg.STAGING_FRIST_DATUM
    frist_anzahl_erreicht = len(ereignisse) >= reg.STAGING_FRIST_EREIGNISSE
    return {
        "signale_protokolliert": len(zeilen),
        "erstes_signal": erstes,
        "vollstaendige_ereignisse": len(ereignisse),
        "frist_ereignisse": reg.STAGING_FRIST_EREIGNISSE,
        "frist_datum": reg.STAGING_FRIST_DATUM,
        "frist_abgelaufen": bool(frist_datum_erreicht or frist_anzahl_erreicht),
        "kriterien": reg.STAGING_KRITERIEN,
        # S1 und S2 kann dieses Modul nicht selbst feststellen - und es
        # behauptet es deshalb auch nicht. Ein Staging-Modul, das sich
        # seine eigene Freigabe ausstellt, waere der Fehler, den die
        # Trennung verhindern soll.
        "s1_rang3_entschieden": None,
        "s2_backtest_bestanden": None,
        "s3_forward": _s3(zeilen),
        "portfoliogewicht": 0.0,
    }


def _s3(zeilen):
    """S3 rechnet dieses Modul selbst - es hat die Ereignisse ja."""
    # Gezaehlt werden ABGESCHLOSSENE Ereignisse: eines, dessen Ausstiegstag
    # noch aussteht, hat keine Rendite, und es als Ereignis mitzuzaehlen
    # wuerde die Frist zu frueh ablaufen lassen.
    renditen = {}
    for z in zeilen:
        e = z.get("ereignis")
        if not e or z.get("netto_rendite") is None:
            continue
        renditen[e["einstieg"]] = float(z["netto_rendite"])
    if len(renditen) < reg.STAGING_FRIST_EREIGNISSE:
        return {"bestimmt": False,
                "grund": f"{len(renditen)} von "
                         f"{reg.STAGING_FRIST_EREIGNISSE} abgeschlossenen "
                         f"Ereignissen"}
    renditen = list(renditen.values())
    unten, oben, mittel = kz.bootstrap_intervall(
        renditen, reg.BOOTSTRAP_ZIEHUNGEN, reg.BOOTSTRAP_SEED,
        reg.BOOTSTRAP_NIVEAU)
    return {"bestimmt": True, "n": len(renditen),
            "mittel_pct": mittel * 100, "unten_pct": unten * 100,
            "oben_pct": oben * 100, "erfuellt": bool(unten > 0)}


def main():
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--daten", default=reg.DATEN_DIR)
    p.add_argument("--lauf", action="store_true",
                   help="Signal bestimmen und protokollieren")
    p.add_argument("--stand", help="Stichtag JJJJ-MM-TT (Vorgabe: heute)")
    p.add_argument("--status", action="store_true")
    args = p.parse_args()

    if args.status:
        print(json.dumps(status(args.daten), indent=2, ensure_ascii=False,
                         sort_keys=True))
        return 0
    if args.lauf:
        s = protokolliere(args.daten, args.stand)
        print(f"{s['stand']}  {s['instrument']} {s['fenster']}  "
              f"Position {s['position'].upper()}  "
              f"Portfoliogewicht {s['portfoliogewicht']:.1f}")
        print(f"  {ZUSICHERUNG}")
        print(f"  Frist: {reg.STAGING_FRIST_EREIGNISSE} Ereignisse, "
              f"spaetestens {reg.STAGING_FRIST_DATUM}")
        return 0

    print(__doc__.strip().split("\n")[0])
    print(f"\n  {ZUSICHERUNG}")
    print(f"  Signalprotokoll: {SIGNALE}")
    print(f"  --lauf protokolliert ein Signal, --status zeigt die Frist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
