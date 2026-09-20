#!/usr/bin/env python3
"""
TB-72 - Die erste Falte aus dem Trockenlauf des Laufcodes (Registertext 3b (a))
==============================================================================
Reine Standardbibliothek. Rein lesend: der Loader jedes Bots laeuft im
Kindprozess des Universum-Trockenlaufs (TB-40, `loaderlauf.py`, mit
Schreibschutz) und sieht die Kursdatei bis zum letzten Zeitpunkt der Falte.

WORUM ES GEHT
------------------------------------------------------------------------------
Registertext 4a (Abschnitt 15.6) sagt, wann die erste Falte ist: das erste
Kalenderjahr, in dem am 1. Januar Universum und Indikator-Vorlauf vorliegen.
Registertext 3b (a) (Abschnitt 16.7) sagt, wann eine Falte zaehlt: wenn der
Loader des Bots in ihr mindestens ein Symbol an mindestens einem Handelstag
handelbar macht. Register 21.3 (b): ergeben beide verschiedene erste Falten,
bindet 3b (a).

Bis TB-72 rechnete `research/vorregistrierung/faltenplan.py` die erste Falte
allein nach 4a nach (`erste_falte_quelle`: "Datenlage nach Registertext 4a")
und sagte in seinem Modulkopf selbst, dass es 21.3 (b) nicht umsetzt. Fable
(FABLE_ANTWORT_2026-09-20d_mtm_messung.md, Abschnitt 2): "faltenplan.py
sollte die erste Falte aus dem Trockenlauf beziehen, nicht aus 4a
nachrechnen. 4a bleibt die Regel; 3b (a) ueber den Trockenlauf ist ihre
operative Form; der Plan ist eine Ableitung daraus, keine Parallelrechnung."

WAS DIESES MODUL TUT
------------------------------------------------------------------------------
`erste_falte_nach_3b(bot, kandidaten)` bekommt die Kalenderjahr-Falten, die
Registertext 4a fuer den Bot ergibt (von seiner ersten Falte bis zum
Go-Live-Schnitt), laesst den Loader des Bots am letzten Zeitpunkt jeder
Falte laufen (Lesart H, Abschnitt 16.2 - genau die Stichtage, die
`universum_trockenlauf.trockenlauf` fuer H benutzt) und gibt das Jahr der
ersten Falte zurueck, in der der Loader mindestens ein Symbol handelbar
macht. Der Loader wird ueber `universum_trockenlauf.messe_bot` aufgerufen -
der Funktion, die der TB-40-Bericht ausdruecklich als Import-Stelle nennt
("... importiert messe_bot(), statt die Frage ein viertes Mal zu
beantworten"). Die Schranke `MIN_HISTORY_*` steht nirgends hier: sie wirkt
im Bot-Code, im Kindprozess.

Die Messung `main()` (TB-72 Schritt 1) weist je Bot BEIDE Richtungen aus:

* **spaeter** als 4a: die erste 4a-Falte, in der H >= 1 ist (das ist die
  Ableitung oben);
* **frueher** als 4a: die Falten gleicher Laenge VOR der ersten 4a-Falte,
  zurueck bis zum ersten Kurstag des Marktes im Zeitrahmen des Bots - und
  ob der Loader dort ein Symbol handelbar macht. Das ist der blinde Fleck
  der Vormessung aus `benchmark_drawdowns_vt.json`: die kennt nur Falten,
  die im Plan stehen.

Dazu die Gegenprobe gegen `faltenschranke_messung.trockenlauf_ohne_schranke`
(TB-56, Spalte "erste_falte_mit_loader_symbol_H"): dieselbe Frage mit dem
vollen Trockenlauf auf dem Plan ohne Schranke; beide muessen je Bot dasselbe
Jahr nennen.

    python3 research/faltenplan_neun/erste_falte_trockenlauf.py
    python3 research/faltenplan_neun/erste_falte_trockenlauf.py --json aus.json
    python3 research/faltenplan_neun/erste_falte_trockenlauf.py --ohne-gegenprobe
"""

import argparse
import datetime as dt
import functools
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)
import faltenplan_neun as fn  # noqa: E402

BASE_DIR = fn.BASE_DIR
sys.path.insert(0, os.path.join(BASE_DIR, "research", "universum_trockenlauf"))
import universum_trockenlauf as ut  # noqa: E402


# ==============================================================================
# 1. Der Loader am Faltenende - je Falte die Menge H
# ==============================================================================
def _stichtag_faltenende(bis_ausschliesslich: str) -> str:
    """Der letzte Zeitpunkt der halboffenen Falte [von, bis) - eine Sekunde
    vor `bis`, wie in `universum_trockenlauf.stichtage_der_falte`."""
    return ut.stichtage_der_falte("1970-01-01", bis_ausschliesslich)[1]


@functools.lru_cache(maxsize=None)
def _handelbar_am_faltenende(bot: str, faltenenden: tuple) -> dict:
    """{bis_ausschliesslich -> sortierte Symbolliste H} - EIN Kindprozess je
    Bot fuer alle Stichtage; das Ergebnis wird je Prozess gemerkt, weil
    `faltenplan()` in Tests und Berichten viele Male aufgerufen wird."""
    stichtage = [_stichtag_faltenende(b) for b in faltenenden]
    roh = ut.messe_bot(bot, stichtage)
    if roh["fehler"]:
        raise RuntimeError("Loader %s: %s\n%s" % (bot, roh["fehler"],
                                                  roh.get("spur", "")))
    gemessen = {l["stichtag"]: sorted(l["symbole"]) for l in roh["laeufe"]}
    return {b: gemessen[s] for b, s in zip(faltenenden, stichtage)}


def handelbar_am_faltenende(bot: str, falten: list) -> list:
    """Je Falte `{name, von, bis_ausschliesslich, H, H_symbole}`.

    `falten` ist eine Liste von Abbildungen mit `name`, `von` und
    `bis_ausschliesslich` (ISO-Datum) - das Format von
    `research/vorregistrierung/faltenplan.py::_jahresfalten`.
    """
    enden = tuple(f["bis_ausschliesslich"] for f in falten)
    mengen = _handelbar_am_faltenende(bot, enden)
    return [{"name": f["name"], "von": f["von"],
             "bis_ausschliesslich": f["bis_ausschliesslich"],
             "H": len(mengen[f["bis_ausschliesslich"]]),
             "H_symbole": mengen[f["bis_ausschliesslich"]]}
            for f in falten]


# ==============================================================================
# 2. Die Ableitung - Registertext 4a als Kandidatenliste, 3b (a) entscheidet
# ==============================================================================
def erste_falte_nach_3b(bot: str, kandidaten: list):
    """(Jahr der ersten Falte mit H >= 1 oder None, Messung je Kandidat).

    `kandidaten` sind die Falten nach Registertext 4a, aufsteigend. Zurueck
    kommt das Jahr, in dem die erste Falte beginnt, in der der Loader des
    Bots mindestens ein Symbol handelbar macht (3b (a), Lesart H). None,
    wenn er das in keiner Kandidatenfalte tut.
    """
    messung = handelbar_am_faltenende(bot, kandidaten)
    for f in messung:
        if f["H"] >= 1:
            return int(f["von"][:4]), messung
    return None, messung


# ==============================================================================
# 3. Die Messung (TB-72 Schritt 1) - neun Zahlen, beide Richtungen
# ==============================================================================
def _falten_zurueck(erstes_jahr_4a: int, laenge: int, bis_jahr: int) -> list:
    """Falten der Laenge `laenge` VOR der ersten 4a-Falte, aufsteigend, so
    weit zurueck, dass die frueheste noch `bis_jahr` (erster Kurstag des
    Marktes) enthaelt. Gleiches Raster wie der Plan, nur nach hinten."""
    falten = []
    jahr = erstes_jahr_4a - laenge
    while jahr + laenge - 1 >= bis_jahr:
        falten.append({
            "von": dt.date(jahr, 1, 1).isoformat(),
            "bis_ausschliesslich": dt.date(jahr + laenge, 1, 1).isoformat(),
            "name": (f"{jahr}" if laenge == 1 else f"{jahr}-{jahr + laenge - 1}"),
        })
        jahr -= laenge
    return list(reversed(falten))


def erster_kurstag_des_marktes(bot: str):
    """Der frueheste erste Kurstag ueber das Universum im Zeitrahmen des Bots."""
    eig = fn.BOTS[bot]
    tage = []
    for symbol in fn.symbole(eig["markt"]):
        pfad = fn.kursdatei(symbol, eig["zeitrahmen"])
        if os.path.exists(pfad):
            erster, _ = fn.erster_und_letzter_tag(pfad)
            if erster is not None:
                tage.append(erster)
    return min(tage) if tage else None


def messung(gegenprobe: bool = True, fortschritt=None) -> dict:
    """Je Bot: erste Falte laut Plan (faltenplan.py, Stand vor der Aenderung
    oder danach - der Plan wird gelesen, nicht nachgebaut), erste Falte laut
    Trockenlauf in beiden Richtungen, und die Gegenprobe gegen TB-56."""
    sys.path.insert(0, os.path.join(BASE_DIR, "research", "vorregistrierung"))
    import faltenplan as vfp  # noqa: E402
    import registerdaten as rd  # noqa: E402

    plan = vfp.faltenplan()
    schnitt = dt.date.fromisoformat(rd.GO_LIVE_SCHNITT)
    aus = {"aufgabe": "TB-72 Schritt 1 - erste Falte je Bot: Plan gegen Trockenlauf, "
                      "beide Richtungen (rein lesend)",
           "werkzeug": "research/universum_trockenlauf/universum_trockenlauf.py::messe_bot "
                       "am letzten Zeitpunkt jeder Falte (Lesart H)",
           "go_live_schnitt": rd.GO_LIVE_SCHNITT,
           "je_bot": {}}
    for bot in fn.BOTS:
        if fortschritt:
            fortschritt(bot)
        p = plan[bot]
        laenge = p["faltenlaenge_jahre"]
        erste_plan = p["erste_falte"]
        # 4a, unabhaengig vom Stand des Plans: die Nachrechnung aus der
        # Datenlage, damit die Messung auch NACH der Umstellung von
        # faltenplan.py noch beide Groessen nennt.
        erste_4a = vfp.erste_falte_4a(bot) if hasattr(vfp, "erste_falte_4a") \
            else vfp.erste_falte(bot)
        kandidaten = vfp._jahresfalten(erste_4a, schnitt, laenge)
        spaeter_jahr, spaeter = erste_falte_nach_3b(bot, kandidaten)

        beginn = erster_kurstag_des_marktes(bot)
        frueher = []
        if beginn is not None:
            frueher = handelbar_am_faltenende(
                bot, _falten_zurueck(erste_4a, laenge, beginn.year))
        frueher_mit_h = [f for f in frueher if f["H"] >= 1]

        erste_trockenlauf = (int(frueher_mit_h[0]["von"][:4]) if frueher_mit_h
                             else spaeter_jahr)
        aus["je_bot"][bot] = {
            "markt": fn.BOTS[bot]["markt"],
            "faltenlaenge_jahre": laenge,
            "erste_falte_plan": erste_plan,
            "erste_falte_4a": erste_4a,
            "erste_falte_trockenlauf_ab_4a": spaeter_jahr,
            "erster_kurstag_markt": beginn.isoformat() if beginn else None,
            "falten_vor_4a_gemessen": len(frueher),
            "falten_vor_4a_mit_H": [f["name"] for f in frueher_mit_h],
            "frueheste_falte_vor_4a_mit_H": (frueher_mit_h[0]["name"]
                                             if frueher_mit_h else None),
            "erste_falte_trockenlauf": erste_trockenlauf,
            "abweichung_spaeter": spaeter_jahr != erste_plan,
            "abweichung_frueher": bool(frueher_mit_h),
            "H_je_kandidat_ab_4a": [{"falte": f["name"], "H": f["H"]} for f in spaeter],
            "H_je_falte_vor_4a": [{"falte": f["name"], "H": f["H"]} for f in frueher],
            "H_symbole_erste_falte": next(
                (f["H_symbole"] for f in spaeter if f["H"] >= 1), []),
        }
    aus["bots_spaeter_als_plan"] = sorted(
        b for b, e in aus["je_bot"].items() if e["abweichung_spaeter"])
    aus["bots_frueher_als_plan"] = sorted(
        b for b, e in aus["je_bot"].items() if e["abweichung_frueher"])

    if gegenprobe:
        import faltenschranke_messung as fsm  # noqa: E402
        t = fsm.trockenlauf_ohne_schranke()
        aus["gegenprobe_tb56"] = {
            "werkzeug": t["werkzeug"],
            "je_bot": {b: {"erste_falte_mit_loader_symbol_H":
                           e["erste_falte_mit_loader_symbol_H"],
                           "gleich": _jahr(e["erste_falte_mit_loader_symbol_H"])
                           == aus["je_bot"][b]["erste_falte_trockenlauf_ab_4a"]}
                       for b, e in t["je_bot"].items()},
            "monotonie_verletzt": t["monotonie_verletzt"],
            "schreibversuche": t["schreibversuche"],
        }
        aus["gegenprobe_tb56"]["alle_gleich"] = all(
            e["gleich"] for e in aus["gegenprobe_tb56"]["je_bot"].values())
    return aus


def _jahr(faltenname):
    return int(str(faltenname)[:4]) if faltenname else None


def _ja(w) -> str:
    return "ja" if w else "nein"


def drucke(m: dict) -> None:
    print("=" * 100)
    print(m["aufgabe"])
    print(m["werkzeug"])
    print("=" * 100)
    print(f"{'Bot':<28}{'Plan':>6}{'4a':>6}{'TL ab 4a':>10}{'vor 4a':>8}"
          f"{'davon H>=1':>12}{'frueheste':>11}{'TL':>6}  H je Kandidat ab 4a")
    print("-" * 100)
    for bot, e in m["je_bot"].items():
        reihe = " / ".join(str(k["H"]) for k in e["H_je_kandidat_ab_4a"])
        print(f"{bot:<28}{str(e['erste_falte_plan']):>6}{str(e['erste_falte_4a']):>6}"
              f"{str(e['erste_falte_trockenlauf_ab_4a']):>10}"
              f"{e['falten_vor_4a_gemessen']:>8}{len(e['falten_vor_4a_mit_H']):>12}"
              f"{str(e['frueheste_falte_vor_4a_mit_H']):>11}"
              f"{str(e['erste_falte_trockenlauf']):>6}  {reihe}")
        if e["falten_vor_4a_mit_H"]:
            vor = " / ".join(f"{k['falte']}:{k['H']}" for k in e["H_je_falte_vor_4a"])
            print(f"{'':<28}H vor 4a (ab erstem Kurstag {e['erster_kurstag_markt']}): {vor}")
    print("-" * 100)
    print(f"spaeter als der Plan: {m['bots_spaeter_als_plan']}")
    print(f"frueher als der Plan: {m['bots_frueher_als_plan']}")
    if "gegenprobe_tb56" in m:
        g = m["gegenprobe_tb56"]
        print(f"Gegenprobe TB-56 (trockenlauf_ohne_schranke): alle gleich: "
              f"{_ja(g['alle_gleich'])}; Monotonie verletzt: "
              f"{g['monotonie_verletzt'] or 'nein'}; Schreibversuche: "
              f"{g['schreibversuche'] or 'keine'}")
        for b, e in g["je_bot"].items():
            print(f"  {b:<28}TB-56: {str(e['erste_falte_mit_loader_symbol_H']):<10}"
                  f"gleich: {_ja(e['gleich'])}")
    print("\nRein lesend - es wurde nichts geaendert.")


def main(argv=None) -> int:
    z = argparse.ArgumentParser(description="TB-72: erste Falte aus dem Trockenlauf.")
    z.add_argument("--json", default=None, help="Messung als JSON ablegen")
    z.add_argument("--ohne-gegenprobe", action="store_true",
                   help="die Gegenprobe gegen TB-56 (voller Trockenlauf) auslassen")
    a = z.parse_args(argv)

    def melde(bot):
        sys.stderr.write("  ... Trockenlauf %s\n" % bot)
        sys.stderr.flush()

    m = messung(gegenprobe=not a.ohne_gegenprobe, fortschritt=melde)
    drucke(m)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(m, f, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"Messung: {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
