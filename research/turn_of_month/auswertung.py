#!/usr/bin/env python3
"""
TB-33 - Das Auswertungsskript. Eingefroren vor dem Lauf.
==============================================================================
Liest Kursreihen und gibt aus:

  * Test 1 - mittlere Netto-Rendite des Kernfensters, Bootstrap-Intervall,
    Zahl der Ereignisse, Falten-Median,
  * Test 2 - das Perzentil des Kernfensters in der Platzhalter-Verteilung
    (die eingebaute Beta-Bereinigung),
  * Test 3 - den Sweep, ausdruecklich als Bild,
  * das Urteil nach den drei Bedingungen B1, B2, B3,
  * und die Bestaetigungsperiode, getrennt ausgewiesen.

**Es gibt keine Stelle, an der ein Mensch entscheidet.** Wo dieses Programm
eine Wahl offen liesse, waere die Vorregistrierung unvollstaendig - das ist
Pfadkriterium P1, und es ist der Grund, warum das Skript VOR dem Lauf
geschrieben und gegen erzeugte Beispieldaten geprueft wurde.

DIE SWEEP-REGEL IST KEINE ABSICHTSERKLAERUNG, SONDERN EINE STRUKTUR
------------------------------------------------------------------------------
`urteil()` bekommt die Sweep-Ergebnisse **gar nicht erst uebergeben**. Es
gibt keinen Parameter, ueber den eine Sweep-Zelle ins Urteil kaeme, und
deshalb auch keinen Weg, auf dem sie versehentlich hineinrutscht. Eine Regel,
die nur im Kommentar steht, waere bei der naechsten Aenderung weg; eine, die
in der Signatur steht, muss jemand ausdruecklich aufbrechen. Der Selbsttest
bricht sie genau deshalb einmal auf und zeigt, dass das Urteil dann kippt.

DREI URTEILE, NICHT ZWEI
------------------------------------------------------------------------------
  BESTANDEN          B1 und B2 und B3.
  DURCHGEFALLEN      mindestens eine der drei faellt.
  NICHT AUSWERTBAR   weniger als MINDEST_EREIGNISSE Ereignisse.

Das dritte ist kein Sonderfall der ersten beiden: "zu wenig Daten" ist keine
Aussage ueber den Effekt, und wer es als "durchgefallen" verbucht, hat eine
Aussage erfunden.
"""

import argparse
import json
import os
import sys

import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)

import handelstage as ht  # noqa: E402
import herkunft as hk  # noqa: E402
import kennzahlen as kz  # noqa: E402
import register as reg  # noqa: E402

Abbruch = ht.Abbruch


# ---------------------------------------------------------------------------
# 1. Ein Fenster auf einem Instrument
# ---------------------------------------------------------------------------
def eine_zelle(daten_dir, symbol, fenster, bis_jahr=None, ab_datum=None,
               bis_datum=None):
    """Alle Kennzahlen einer (Instrument x Fenster)-Zelle.

    `bis_jahr` schneidet auf die Selektionsfalten, `ab_datum`/`bis_datum`
    auf die Bestaetigungsperiode. Genau eine der beiden Begrenzungen wird
    benutzt - welche, entscheidet der Aufrufer, nicht dieses Modul.
    """
    pfad = os.path.join(daten_dir, f"{symbol}_1d.csv")
    df, gestrichen = ht.lies_kursreihe(pfad)
    alle, entfallen = ht.ereignisse(df, fenster)

    if len(alle):
        if bis_jahr is not None:
            ereignisse = alle[alle["jahr"] <= bis_jahr].reset_index(drop=True)
        elif ab_datum is not None:
            ereignisse = alle[
                (alle["datum_einstieg"] >= pd.Timestamp(ab_datum))
                & (alle["datum_einstieg"] < pd.Timestamp(bis_datum))
            ].reset_index(drop=True)
        else:
            ereignisse = alle
    else:
        ereignisse = alle

    n = len(ereignisse)
    laenge = (-fenster[0]) + fenster[1]
    werte = ereignisse["netto_rendite"].to_numpy() if n else []

    unten, oben, mittel = kz.bootstrap_intervall(
        werte, reg.BOOTSTRAP_ZIEHUNGEN, reg.BOOTSTRAP_SEED,
        reg.BOOTSTRAP_NIVEAU)

    # Falten-Median: je Kalenderjahr die mittlere Netto-Rendite, davon der
    # Median ueber die Falten. NICHT der Median aller Ereignisse - eine
    # Falte ist die Einheit, in der dieses Projekt rechnet.
    if n:
        je_falte = ereignisse.groupby("jahr")["netto_rendite"].mean()
        falten_median = kz.median(je_falte.to_numpy())
        je_falte_dict = {str(j): float(v) * 100 for j, v in je_falte.items()}
    else:
        falten_median, je_falte_dict = None, {}

    # Test 2 - die Platzhalter-Verteilung auf DERSELBEN Kursreihe.
    vergleich = ht.vergleichsfenster(df, laenge)
    verteilung = kz.platzhalter_verteilung(
        vergleich, n, laenge, reg.PLATZHALTER_ZIEHUNGEN, reg.PLATZHALTER_SEED)
    perzentil = kz.perzentil_von(mittel, verteilung) if n else None

    return {
        "instrument": symbol,
        "fenster": f"{fenster[0]:+d}/{fenster[1]:+d}",
        "gehaltene_tage": laenge,
        "n_ereignisse": n,
        "n_ereignisse_entfallen": entfallen,
        "n_kerzen_gestrichen": gestrichen,
        "n_handelstage": len(df),
        "mittlere_netto_rendite_pct": None if mittel is None else mittel * 100,
        "bootstrap_unten_pct": None if unten is None else unten * 100,
        "bootstrap_oben_pct": None if oben is None else oben * 100,
        "falten_median_pct": None if falten_median is None else falten_median * 100,
        "je_falte_pct": je_falte_dict,
        "perzentil": perzentil,
        "n_vergleichsfenster": len(vergleich),
    }


# ---------------------------------------------------------------------------
# 2. Das Urteil - bekommt den Sweep NICHT
# ---------------------------------------------------------------------------
def urteil(kern: dict) -> dict:
    """Die drei Bedingungen, einzeln ausgewiesen.

    Das Argument ist der KERN. Es gibt keinen zweiten Parameter, und das ist
    der ganze Punkt: eine Sweep-Zelle kann hier nicht ankommen.
    """
    if kern["n_ereignisse"] < reg.MINDEST_EREIGNISSE:
        return {
            "urteil": reg.URTEIL_NICHT_AUSWERTBAR,
            "grund": (f"{kern['n_ereignisse']} Ereignisse, verlangt sind "
                      f"{reg.MINDEST_EREIGNISSE}. Zu wenig Daten ist KEINE "
                      f"Aussage ueber den Effekt."),
            "b1": None, "b2": None, "b3": None,
        }
    b1 = kern["falten_median_pct"] is not None and kern["falten_median_pct"] > 0
    b2 = kern["bootstrap_unten_pct"] is not None and kern["bootstrap_unten_pct"] > 0
    b3 = kern["perzentil"] is not None and kern["perzentil"] > reg.PERZENTIL_SCHWELLE
    bestanden = bool(b1 and b2 and b3)
    return {
        "urteil": reg.URTEIL_BESTANDEN if bestanden else reg.URTEIL_DURCHGEFALLEN,
        "grund": "" if bestanden else "gefallen: " + ", ".join(
            k for k, v in (("B1", b1), ("B2", b2), ("B3", b3)) if not v),
        "b1": bool(b1), "b2": bool(b2), "b3": bool(b3),
    }


# ---------------------------------------------------------------------------
# 3. Der Sweep - ein Bild, keine Kandidatenliste
# ---------------------------------------------------------------------------
def sweep(daten_dir, bis_jahr):
    """Alle Sweep-Zellen. Sie bekommen KEIN Urteil - nur Zahlen.

    Fehlt eine Kursdatei, steht das in der Zelle. Fehlende Sweep-Daten sind
    kein Abbruchgrund: der Sweep ist Robustheit, und ein fehlendes Bild
    macht aus einem Ergebnis kein anderes.
    """
    zellen = []
    for f in reg.SWEEP_FENSTER:
        try:
            z = eine_zelle(daten_dir, reg.KERNINSTRUMENT, f, bis_jahr=bis_jahr)
        except Abbruch as e:
            z = {"instrument": reg.KERNINSTRUMENT,
                 "fenster": f"{f[0]:+d}/{f[1]:+d}", "fehlt": str(e)}
        z["art"] = "fenster"
        zellen.append(z)
    for s in reg.SWEEP_INSTRUMENTE:
        try:
            z = eine_zelle(daten_dir, s, reg.KERNFENSTER, bis_jahr=bis_jahr)
        except Abbruch as e:
            z = {"instrument": s,
                 "fenster": f"{reg.KERNFENSTER[0]:+d}/{reg.KERNFENSTER[1]:+d}",
                 "fehlt": str(e)}
        z["art"] = "instrument"
        zellen.append(z)
    return zellen


# ---------------------------------------------------------------------------
# 4. Der ganze Lauf
# ---------------------------------------------------------------------------
def lauf(daten_dir):
    kern = eine_zelle(daten_dir, reg.KERNINSTRUMENT, reg.KERNFENSTER,
                      bis_jahr=reg.SELEKTIONSFALTEN_BIS)
    u = urteil(kern)                      # <- nur der Kern. Siehe Docstring.
    zellen = sweep(daten_dir, reg.SELEKTIONSFALTEN_BIS)

    try:
        bestaetigung = eine_zelle(daten_dir, reg.KERNINSTRUMENT,
                                  reg.KERNFENSTER,
                                  ab_datum=reg.BESTAETIGUNG_VON,
                                  bis_datum=reg.BESTAETIGUNG_BIS)
    except Abbruch as e:
        bestaetigung = {"fehlt": str(e)}

    return {
        "herkunft": hk.block("auswertung", daten_dir),
        "register": {
            "kerninstrument": reg.KERNINSTRUMENT,
            "kernfenster": list(reg.KERNFENSTER),
            "kosten_je_roundtrip_pct": reg.KOSTEN_JE_ROUNDTRIP_PCT,
            "kostenschranke_pct_pa": reg.KOSTENSCHRANKE_PCT_PA,
            "bootstrap_ziehungen": reg.BOOTSTRAP_ZIEHUNGEN,
            "bootstrap_seed": reg.BOOTSTRAP_SEED,
            "bootstrap_niveau": reg.BOOTSTRAP_NIVEAU,
            "platzhalter_ziehungen": reg.PLATZHALTER_ZIEHUNGEN,
            "platzhalter_seed": reg.PLATZHALTER_SEED,
            "perzentil_schwelle": reg.PERZENTIL_SCHWELLE,
            "mindest_ereignisse": reg.MINDEST_EREIGNISSE,
            "selektionsfalten_bis": reg.SELEKTIONSFALTEN_BIS,
            "bedingungen": reg.BEDINGUNGEN,
            "sweep_regel": reg.SWEEP_REGEL,
            "ereignis_zuordnung": reg.EREIGNIS_ZUORDNUNG,
            "n_versuchsregister": reg.N_VERSUCHSREGISTER,
            "n_dsr": reg.N_DSR,
        },
        "test1_test2_kern": kern,
        "urteil": u,
        "test3_sweep": zellen,
        "bestaetigungsperiode": bestaetigung,
    }


def _z(x, nach=4):
    return "-" if x is None else f"{x:.{nach}f}"


def bericht(e: dict) -> str:
    k, u = e["test1_test2_kern"], e["urteil"]
    z = []
    z.append("=" * 78)
    z.append("TB-33 - NULLTEST S-E1 TURN-OF-MONTH")
    z.append("=" * 78)
    h = e["herkunft"]
    z.append(f"Herkunft   Commit {h['commit'][:12]} "
             f"({'sauber' if h['arbeitsbaum_sauber'] else 'GEAENDERT'})  "
             f"Daten {h['datenstand'][:12]}  Register {h['register'][:12]}")
    z.append("")
    z.append(f"TEST 1 - der Effekt selbst   {k['instrument']} {k['fenster']}, "
             f"{k['gehaltene_tage']} Handelstage")
    z.append(f"  Ereignisse                 {k['n_ereignisse']}   "
             f"(entfallen {k['n_ereignisse_entfallen']}, "
             f"unvollstaendige Kerzen gestrichen {k['n_kerzen_gestrichen']})")
    z.append(f"  Mittlere NETTO-Rendite     {_z(k['mittlere_netto_rendite_pct'])} % "
             f"je Ereignis")
    z.append(f"  Bootstrap {int(e['register']['bootstrap_niveau'] * 100)} %          "
             f"[{_z(k['bootstrap_unten_pct'])} % ; "
             f"{_z(k['bootstrap_oben_pct'])} %]   "
             f"({e['register']['bootstrap_ziehungen']} Ziehungen, "
             f"Seed {e['register']['bootstrap_seed']})")
    z.append(f"  Falten-Median              {_z(k['falten_median_pct'])} %")
    z.append("")
    z.append("TEST 2 - die eingebaute Kontrolle (Beta-Bereinigung)")
    z.append(f"  Vergleichsfenster          {k['n_vergleichsfenster']} moegliche "
             f"Startdaten, je {k['gehaltene_tage']} Handelstage, gleiche Kosten")
    z.append(f"  Perzentil des Kernfensters {_z(k['perzentil'], 2)}   "
             f"(Schwelle {e['register']['perzentil_schwelle']})")
    z.append("")
    z.append("DIE DREI BEDINGUNGEN")
    for b in ("b1", "b2", "b3"):
        marke = {True: "erfuellt", False: "GEFALLEN", None: "-"}[u[b]]
        z.append(f"  {b.upper()}  {marke:9s} {e['register']['bedingungen'][b.upper()]}")
    z.append("")
    z.append(f"  URTEIL                     {u['urteil']}"
             + (f"   ({u['grund']})" if u["grund"] else ""))
    z.append("")
    z.append("TEST 3 - SWEEP (Robustheit, NICHT Auswahl)")
    z.append("  Diese Zellen gehen in KEIN Urteil ein. Sie sind ein Bild.")
    z.append(f"  {'Zelle':22s} {'N':>5s} {'Mittel %':>10s} "
             f"{'Bootstrap unten %':>18s} {'Perzentil':>10s}")
    for c in e["test3_sweep"]:
        name = f"{c['instrument']} {c['fenster']}"
        if "fehlt" in c:
            z.append(f"  {name:22s} {'-':>5s} {'(keine Kursdatei)':>10s}")
            continue
        z.append(f"  {name:22s} {c['n_ereignisse']:5d} "
                 f"{_z(c['mittlere_netto_rendite_pct']):>10s} "
                 f"{_z(c['bootstrap_unten_pct']):>18s} "
                 f"{_z(c['perzentil'], 2):>10s}")
    z.append(f"  {e['register']['sweep_regel']}")
    z.append("")
    b = e["bestaetigungsperiode"]
    z.append("BESTAETIGUNGSPERIODE (getrennt ausgewiesen, einmal)")
    if "fehlt" in b:
        z.append(f"  {b['fehlt']}")
    else:
        z.append(f"  Ereignisse {b['n_ereignisse']}   "
                 f"Mittel {_z(b['mittlere_netto_rendite_pct'])} %   "
                 f"Bootstrap [{_z(b['bootstrap_unten_pct'])} % ; "
                 f"{_z(b['bootstrap_oben_pct'])} %]")
    return "\n".join(z)


def main():
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--daten", default=reg.DATEN_DIR,
                   help="Ordner mit <SYMBOL>_1d.csv")
    p.add_argument("--json", help="Ergebnis zusaetzlich hierhin schreiben")
    p.add_argument("--protokollieren", action="store_true",
                   help="eine Zeile ans append-only-Herkunftsprotokoll")
    args = p.parse_args()

    e = lauf(args.daten)
    print(bericht(e))

    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(e, f, indent=2, ensure_ascii=False, sort_keys=True,
                      default=str)
            f.write("\n")
        print(f"\nJSON geschrieben: {args.json}")
    if args.protokollieren:
        hk.anhaengen("auswertung")
    return 0


if __name__ == "__main__":
    sys.exit(main())
