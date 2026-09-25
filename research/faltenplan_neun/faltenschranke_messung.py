#!/usr/bin/env python3
"""
TB-56 - Die Faltenschranke messen: erste Falte je Bot MIT und OHNE Schranke
==============================================================================
Rein lesend. Reine Standardbibliothek. Fasst keine Quelldatei an: die
Schranke wird **im Speicher** ueber das Modulattribut `FRUEHESTE_FALTE` von
`faltenplan_neun.py` ausgeschaltet, die Datei auf der Platte bleibt, wie sie
ist (Teil A des Auftrags: "Wegwerf-Kopie oder Parameter").

WORUM ES GEHT
------------------------------------------------------------------------------
Registertext 4a (Abschnitt 15.6) leitet den Faltenbeginn aus der Datenlage
ab: "vom ersten Jahr, in dem am 1. Januar Daten fuer Universum und
Indikator-Vorlauf vorliegen". Er kennt keine Schranke. Der Code kennt eine:
`ERSTE_MOEGLICHE_FALTE = 2019` in `research/vorregistrierung/registerdaten.py`
und - als **Kopie** - `FRUEHESTE_FALTE = 2019` in `faltenplan_neun.py`. Die
Tatsachennotiz in 15.6 Punkt 2 hat diesen Code-Zustand als Registerregel
ausgegeben. Bevor die Schranke entfernt wird, wird gemessen, was sie tut.

WAS GEMESSEN WIRD - JE BOT
------------------------------------------------------------------------------
1. Der Plan **mit** Schranke, so wie das Werkzeug heute rechnet - und ob er
   mit der festgehaltenen Messung `daten/faltenplan.json` uebereinstimmt.
   (Stimmt er nicht, misst dieses Skript ein anderes Werkzeug als das, das
   die Tatsachennotiz erzeugt hat - dann ist alles Weitere wertlos.)
2. Der Plan **ohne** Schranke: erste Falte, Zahl der Selektionsfalten,
   Bestaetigungsperiode, Symbolzahl je Falte (Lesart A und B).
3. Die **Zulassung nach 4b** (mindestens 3 Selektionsfalten), mit und ohne.
4. `elliott_wave` **ausdruecklich**: sein Loader zaehlt KERZEN
   (`MIN_HISTORY_HOURS = 17520`, Registertext 3b (b)) statt Tage. Je Symbol:
   Kerzenzahl, Datum der 17 520. Kerze, dasselbe Datum bei lueckenloser Reihe
   (erster Tag + 730 Tage), und die Luecke dazwischen.
5. Die **Loader-Lesart** je Bot, nachgerechnet aus `MIN_HISTORY_*`
   (Registertext 3b (b)): das erste Kalenderjahr, in dem der Loader mindestens
   ein Symbol handelbar macht. ⚠️ Das ist eine Nachrechnung; massgeblich ist
   der Trockenlauf des Laufcodes (`research/universum_trockenlauf/`), der mit
   `--faltenplan-json` auf den Plan ohne Schranke angesetzt wird.

MUTATIONSGEGENPROBE (Prueffrage B1)
------------------------------------------------------------------------------
`--mutation JAHR` setzt die Schranke kuenstlich wieder ein und zaehlt, bei
wie vielen Bots sich der Plan gegenueber "ohne Schranke" aendert. Beisst die
Probe nicht, misst dieses Skript die Schranke nicht.

    python3 research/faltenplan_neun/faltenschranke_messung.py
    python3 research/faltenplan_neun/faltenschranke_messung.py \\
        --json messung.json --plan-ohne-schranke plan_ohne_schranke.json
    python3 research/faltenplan_neun/faltenschranke_messung.py --mutation 2019
    python3 research/faltenplan_neun/faltenschranke_messung.py --trockenlauf tl.json

`--trockenlauf` setzt den Trockenlauf des Laufcodes (TB-40, Registertext 3b:
"ein anderes Werkzeug ist dafuer nicht zulaessig") auf den Plan OHNE Schranke
an und weist je Bot die erste Falte aus, in der der Loader mindestens ein
Symbol handelbar macht (3b (a), Lesart H). ⚠️ Dessen Druckfunktion kennt nur
Falten, die im Register stehen; deshalb wird hier `trockenlauf()` direkt
aufgerufen und der Bericht selbst geschrieben - das Werkzeug bleibt unveraendert.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)
import faltenplan_neun as fp  # noqa: E402

BASE_DIR = fp.BASE_DIR
FESTGEHALTEN = os.path.join(_HIER, "daten", "faltenplan.json")
MINDESTZAHL_4B = 3        # Registertext 4b: mindestens 3 Selektionsfalten
KERZEN_JE_TAG_1H = 24

# ==============================================================================
# 1. Plan mit und ohne Schranke - im Speicher, nicht auf der Platte
# ==============================================================================
def _roundtrip(plan: dict) -> dict:
    """JSON-Rundreise wie in `faltenplan_neun.main` (date -> str)."""
    return json.loads(json.dumps(plan, sort_keys=True, default=str))


def plan_mit_schranke() -> dict:
    return _roundtrip(fp.faltenplan())


def plan_ohne_schranke() -> dict:
    """Die Schranke ausschalten: Modulattribut, kein Dateizugriff.

    `erstes_faltenjahr` rechnet `max(FRUEHESTE_FALTE, jahr_aus_daten)`; mit 0
    bindet die Schranke nie. Der alte Wert wird hinterher zurueckgesetzt.
    """
    alt = fp.FRUEHESTE_FALTE
    fp.FRUEHESTE_FALTE = 0
    try:
        return _roundtrip(fp.faltenplan())
    finally:
        fp.FRUEHESTE_FALTE = alt


def plan_mit_schranke_bei(jahr: int) -> dict:
    alt = fp.FRUEHESTE_FALTE
    fp.FRUEHESTE_FALTE = jahr
    try:
        return _roundtrip(fp.faltenplan())
    finally:
        fp.FRUEHESTE_FALTE = alt


def festgehaltener_plan() -> dict:
    with open(FESTGEHALTEN, encoding="utf-8") as f:
        return json.load(f)


def _kern(p: dict) -> dict:
    """Die Felder, an denen sich ein Plan aendert - fuer Vergleiche."""
    return {
        "erstes_faltenjahr": p["erstes_faltenjahr"],
        "faltenlaenge_jahre": p["faltenlaenge_jahre"],
        "anzahl_selektionsfalten": p["anzahl_selektionsfalten"],
        "selektionsfalten": [fp.faltenname(b) for b in p["selektionsfalten"]],
        "bestaetigungsperiode": (fp.faltenname(p["bestaetigungsperiode"])
                                 if p["bestaetigungsperiode"] else None),
        "bestaetigung_von": (p["bestaetigungsperiode"]["von"]
                             if p["bestaetigungsperiode"] else None),
        "symbolzahl_je_selektionsfalte": p["symbolzahl_je_selektionsfalte"],
        "symbolzahl_je_selektionsfalte_lesart_b":
            p["symbolzahl_je_selektionsfalte_lesart_b"],
        "symbolzahl_bestaetigung": p["symbolzahl_bestaetigung"],
        "zulassung_4b": p["anzahl_selektionsfalten"] >= MINDESTZAHL_4B,
    }


# ==============================================================================
# 2. elliott_wave: Kerzen zaehlen, nicht Tage
# ==============================================================================
def _abbruch_2(stelle: str, text: str):
    """Laut abbrechen statt still weiterzurechnen (TB-107, Fable 25c 4 (2)).

    Unabhaengig vom Modus: ein Widerspruch zwischen Bot-Datei und Messung ist
    kein Laufzustand. `paths` ist das, das `faltenplan_neun` schon geladen hat.
    """
    print(f"ABBRUCH (faltenschranke_messung.py::{stelle}): {text}", file=sys.stderr)
    raise SystemExit(fp.paths.RUECKGABEWERT_STARTPRUEFUNG)


def _min_history(bot: str):
    """(Name, Wert) der Loader-Schranke, GELESEN aus multi_symbol_optimise.py.

    Genau ein Treffer, sonst 2. Bis TB-107 nahm hier `re.search` still den
    ersten Treffer, und ohne Treffer ging `(None, None)` weiter.
    """
    pfad = os.path.join(BASE_DIR, "strategies", bot, "multi_symbol_optimise.py")
    with open(pfad, encoding="utf-8") as f:
        quelle = f.read()
    treffer = re.findall(r"^(MIN_HISTORY_(?:DAYS|HOURS))\s*=\s*(\d+)", quelle, re.M)
    if len(treffer) != 1:
        _abbruch_2("_min_history",
                   f"{pfad}: {len(treffer)} Treffer fuer MIN_HISTORY_DAYS/"
                   f"MIN_HISTORY_HOURS {[n for n, _ in treffer]}, erwartet genau einer")
    name, wert = treffer[0]
    return name, int(wert)


def kerzen_elliott_wave() -> dict:
    """Je 1h-Symbol: Kerzenzahl, Datum der N-ten Kerze, Soll bei Lueckenlosigkeit."""
    name, n = _min_history("elliott_wave")
    ergebnis = {"schranke": name, "wert": n, "symbole": {}}
    if name != "MIN_HISTORY_HOURS":
        _abbruch_2("kerzen_elliott_wave",
                   f"elliott_wave traegt {name} = {n} statt MIN_HISTORY_HOURS - "
                   f"bis TB-107 stand hier still ein Hinweis statt der Kerzen")
    for symbol in fp.symbole("krypto"):
        pfad = fp.kursdatei(symbol, "1h")
        if not os.path.exists(pfad):
            ergebnis["symbole"][symbol] = None
            continue
        erster = letzter = None
        zahl = 0
        nte = None
        with open(pfad, encoding="utf-8") as f:
            f.readline()
            for zeile in f:
                tag = fp._zeitstempel(zeile)
                if tag is None:
                    continue
                if erster is None:
                    erster = tag
                letzter = tag
                zahl += 1
                if zahl == n:
                    nte = tag
        if erster is None:
            ergebnis["symbole"][symbol] = None
            continue
        spanne_tage = (letzter - erster).days + 1
        soll_kerzen = spanne_tage * KERZEN_JE_TAG_1H
        lueckenlos_ab = erster + dt.timedelta(days=n // KERZEN_JE_TAG_1H)
        ergebnis["symbole"][symbol] = {
            "erster_tag": erster.isoformat(),
            "letzter_tag": letzter.isoformat(),
            "kerzen": zahl,
            "spanne_tage": spanne_tage,
            "fehlende_kerzen": max(0, soll_kerzen - zahl),
            "n_te_kerze_am": nte.isoformat() if nte else None,
            "n_te_kerze_bei_lueckenloser_reihe": lueckenlos_ab.isoformat(),
            "verzoegerung_durch_luecken_tage":
                ((nte - lueckenlos_ab).days if nte else None),
            "schranke_erreicht": nte is not None,
        }
    erreicht = [s["n_te_kerze_am"] for s in ergebnis["symbole"].values()
                if s and s["n_te_kerze_am"]]
    ergebnis["fruehestes_symbol_handelbar_ab"] = min(erreicht) if erreicht else None
    ergebnis["erstes_jahr_loader"] = (int(min(erreicht)[:4]) if erreicht else None)
    ergebnis["symbole_unter_der_schranke"] = sorted(
        s for s, w in ergebnis["symbole"].items() if w and not w["schranke_erreicht"])
    return ergebnis


# ==============================================================================
# 3. Loader-Lesart je Bot, nachgerechnet (Registertext 3b (b))
# ==============================================================================
def loader_lesart(bot: str) -> dict:
    """Erstes Kalenderjahr, in dem der Loader mindestens ein Symbol laedt.

    Zeitspannen-Bots: erster Kurstag + MIN_HISTORY_DAYS. Kerzen-Bot: Datum der
    N-ten Kerze. ⚠️ Nachrechnung nach dem Wortlaut der Loader; die Messung am
    Laufcode selbst macht `universum_trockenlauf.py`.
    """
    eig = fp.BOTS[bot]
    name, n = _min_history(bot)
    aus = {"schranke": name, "wert": n, "handelbar_ab": {}}
    if name == "MIN_HISTORY_HOURS":
        k = kerzen_elliott_wave()
        aus["handelbar_ab"] = {s: (w["n_te_kerze_am"] if w else None)
                               for s, w in k["symbole"].items()}
    else:
        anker = fp.fensteranker(eig["markt"])
        for symbol in fp.symbole(eig["markt"]):
            pfad = fp.kursdatei(symbol, eig["zeitrahmen"])
            if not os.path.exists(pfad):
                aus["handelbar_ab"][symbol] = None
                continue
            erster, _ = fp.erster_und_letzter_tag(pfad)
            if erster is None:
                aus["handelbar_ab"][symbol] = None
                continue
            # Aktien: der Loader schneidet auf RECENT_YEARS_ONLY, gemessen am
            # letzten Tag der DURCHGEREICHTEN Daten (im Trockenlauf: am
            # Stichtag). Fuer "ab wann handelbar" zaehlt deshalb der erste
            # Kurstag der Datei, nicht der Fensteranker - der Anker wird nur
            # ausgewiesen.
            aus["handelbar_ab"][symbol] = (erster + dt.timedelta(days=n)).isoformat()
        aus["fensteranker"] = anker.isoformat() if anker else None
    daten = [d for d in aus["handelbar_ab"].values() if d]
    aus["fruehestes_symbol_handelbar_ab"] = min(daten) if daten else None
    aus["erstes_jahr_loader"] = int(min(daten)[:4]) if daten else None
    return aus


# ==============================================================================
# 4. Die Messung
# ==============================================================================
def messung() -> dict:
    mit = plan_mit_schranke()
    ohne = plan_ohne_schranke()
    fest = festgehaltener_plan()

    # Werkzeugstand gegen die festgehaltene Messung
    gleich = {bot: _kern(mit[bot]) == _kern(fest["plaene"][bot]) for bot in fp.BOTS}
    fest_schranke = fest.get("frueheste_falte")

    je_bot = {}
    for bot in fp.BOTS:
        km, ko = _kern(mit[bot]), _kern(ohne[bot])
        je_bot[bot] = {
            "markt": fp.BOTS[bot]["markt"],
            "zeitrahmen": fp.BOTS[bot]["zeitrahmen"],
            "vorlauf_balken": fp.BOTS[bot]["vorlauf_balken"],
            "mit_schranke": km,
            "ohne_schranke": ko,
            "erste_falte_verschiebt_sich": km["erstes_faltenjahr"] != ko["erstes_faltenjahr"],
            "faltenzahl_aendert_sich": (km["anzahl_selektionsfalten"]
                                        != ko["anzahl_selektionsfalten"]),
            "zulassung_4b_aendert_sich": km["zulassung_4b"] != ko["zulassung_4b"],
            "bestaetigung_aendert_sich": km["bestaetigung_von"] != ko["bestaetigung_von"],
            "loader_lesart": loader_lesart(bot),
        }

    jahre_ohne = sorted({je_bot[b]["ohne_schranke"]["erstes_faltenjahr"] for b in fp.BOTS})
    return {
        "aufgabe": "TB-56 Teil A - Faltenschranke messen (rein lesend)",
        "werkzeug": "research/faltenplan_neun/faltenplan_neun.py, Schranke im Speicher ausgeschaltet",
        "schranke_im_werkzeug": fp.FRUEHESTE_FALTE,
        "schranke_in_festgehaltener_messung": fest_schranke,
        "werkzeug_stimmt_mit_festgehaltener_messung": all(gleich.values()),
        "werkzeug_stimmt_je_bot": gleich,
        "go_live": fp.GO_LIVE.isoformat(),
        "mindestzahl_4b": MINDESTZAHL_4B,
        "je_bot": je_bot,
        "erste_faltenjahre_ohne_schranke": jahre_ohne,
        "dasselbe_jahr_fuer_alle": len(jahre_ohne) == 1,
        "bots_bei_denen_die_schranke_bindet": sorted(
            b for b in fp.BOTS if je_bot[b]["erste_falte_verschiebt_sich"]),
        "bots_mit_geaenderter_faltenzahl": sorted(
            b for b in fp.BOTS if je_bot[b]["faltenzahl_aendert_sich"]),
        "bots_mit_geaenderter_zulassung_4b": sorted(
            b for b in fp.BOTS if je_bot[b]["zulassung_4b_aendert_sich"]),
        "bots_mit_geaenderter_bestaetigung": sorted(
            b for b in fp.BOTS if je_bot[b]["bestaetigung_aendert_sich"]),
        "elliott_wave_kerzen": kerzen_elliott_wave(),
    }


def mutation(jahr: int) -> dict:
    """Schranke kuenstlich bei `jahr` - was aendert sich gegen 'ohne'?"""
    ohne = plan_ohne_schranke()
    mut = plan_mit_schranke_bei(jahr)
    geaendert = sorted(b for b in fp.BOTS if _kern(ohne[b]) != _kern(mut[b]))
    return {
        "schranke": jahr,
        "bots_geaendert": geaendert,
        "anzahl_geaendert": len(geaendert),
        "beisst": bool(geaendert),
        "erste_falte": {b: {"ohne": ohne[b]["erstes_faltenjahr"],
                            "mit": mut[b]["erstes_faltenjahr"]} for b in fp.BOTS},
    }


# ==============================================================================
# 4b. Der Trockenlauf des Laufcodes auf dem Plan ohne Schranke
# ==============================================================================
def trockenlauf_ohne_schranke(bots=None) -> dict:
    """Je Bot und Falte die Loader-Mengen H und F; erste Falte nach 3b (a)."""
    import tempfile
    sys.path.insert(0, os.path.join(BASE_DIR, "research", "universum_trockenlauf"))
    import universum_trockenlauf as ut  # noqa: E402
    ordner = tempfile.mkdtemp(prefix="tb56_plan_")
    plan_pfad = os.path.join(ordner, "plan_ohne_schranke.json")
    with open(plan_pfad, "w", encoding="utf-8") as f:
        json.dump({"go_live": fp.GO_LIVE.isoformat(), "frueheste_falte": None,
                   "plaene": plan_ohne_schranke()},
                  f, indent=2, ensure_ascii=False, sort_keys=True, default=str)

    def melde(bot):
        sys.stderr.write("  ... Trockenlauf %s\n" % bot)
        sys.stderr.flush()

    roh = ut.trockenlauf(faltenplan_json=plan_pfad, bots=bots or list(fp.BOTS),
                         fortschritt=melde)
    aus = {"werkzeug": "research/universum_trockenlauf/universum_trockenlauf.py::trockenlauf",
           "plan": "ohne Schranke (faltenplan_neun, FRUEHESTE_FALTE im Speicher = 0)",
           "monotonie_verletzt": roh["monotonie_verletzt"],
           "schreibversuche": roh["schreibversuche"],
           "je_bot": {}}
    for bot, e in roh["bots"].items():
        falten = []
        for f in e["falten"]:
            falten.append({"falte": f["falte"], "von": f["von"],
                           "bis_ausschliesslich": f["bis_ausschliesslich"],
                           "bestaetigung": f["bestaetigung"],
                           "lesart_a": len(f["lesart_a_faltenplan"]),
                           "H": len(f["gemessen_H"]), "F": len(f["gemessen_F"]),
                           "H_symbole": f["gemessen_H"]})
        sel = [f for f in falten if not f["bestaetigung"]]
        mit_h = [f for f in sel if f["H"] >= 1]
        leer_h = [f["falte"] for f in sel if f["H"] == 0]
        aus["je_bot"][bot] = {
            "schranken": e["schranken"],
            "universum": e["universum"],
            "falten": falten,
            "erste_falte_lesart_a": sel[0]["falte"] if sel else None,
            "erste_falte_mit_loader_symbol_H": mit_h[0]["falte"] if mit_h else None,
            "selektionsfalten_lesart_a": len(sel),
            "selektionsfalten_mit_loader_symbol_H": len(mit_h),
            "leere_selektionsfalten_H": leer_h,
            "zulassung_4b_nach_H": len(mit_h) >= MINDESTZAHL_4B,
        }
    return aus


def drucke_trockenlauf(t: dict) -> None:
    print("\nTrockenlauf des Laufcodes auf dem Plan OHNE Schranke (Registertext 3b, Lesart H)")
    print("-" * 96)
    print(f"{'Bot':<28}{'1.Falte 4a':<12}{'1.Falte H':<12}{'#Sel 4a':>8}{'#Sel H':>8}"
          f"{'4b(H)':>7}  H je Falte (Bestaetigung zuletzt)")
    for bot, e in t["je_bot"].items():
        reihe = " / ".join(str(f["H"]) for f in e["falten"])
        print(f"{bot:<28}{str(e['erste_falte_lesart_a']):<12}"
              f"{str(e['erste_falte_mit_loader_symbol_H']):<12}"
              f"{e['selektionsfalten_lesart_a']:>8}{e['selektionsfalten_mit_loader_symbol_H']:>8}"
              f"{_ja(e['zulassung_4b_nach_H']):>7}  {reihe}")
        if e["leere_selektionsfalten_H"]:
            print(f"{'':<28}leer nach H: {e['leere_selektionsfalten_H']}")
    print(f"Monotonie verletzt: {t['monotonie_verletzt'] or 'nein'}; "
          f"Schreibversuche: {t['schreibversuche'] or 'keine'}")


# ==============================================================================
# 5. Ausgabe
# ==============================================================================
def _ja(w) -> str:
    return "ja" if w else "nein"


def drucke(m: dict) -> None:
    print("=" * 96)
    print("TB-56 Teil A - Die Faltenschranke, gemessen (rein lesend)")
    print(f"Werkzeug-Schranke heute: {m['schranke_im_werkzeug']}  |  "
          f"festgehaltene Messung: {m['schranke_in_festgehaltener_messung']}  |  "
          f"Werkzeug = festgehaltene Messung: "
          f"{_ja(m['werkzeug_stimmt_mit_festgehaltener_messung'])}")
    print("=" * 96)
    kopf = (f"{'Bot':<28}{'1.Falte':>8}{'':>2}{'':<8}{'#Sel':>5}{'':>2}{'':<5}"
            f"{'4b':>4}{'':>2}{'':<5}  {'Bestaetigung ab':<26}Loader-Jahr")
    print(f"{'':<28}{'mit':>8}  {'ohne':<8}{'mit':>5}  {'ohne':<5}"
          f"{'mit':>4}  {'ohne':<5}  {'mit -> ohne':<26}(3b b)")
    print("-" * 96)
    for bot, e in m["je_bot"].items():
        km, ko = e["mit_schranke"], e["ohne_schranke"]
        print(f"{bot:<28}{str(km['erstes_faltenjahr']):>8}  "
              f"{str(ko['erstes_faltenjahr']):<8}"
              f"{km['anzahl_selektionsfalten']:>5}  {ko['anzahl_selektionsfalten']:<5}"
              f"{_ja(km['zulassung_4b']):>4}  {_ja(ko['zulassung_4b']):<5}  "
              f"{str(km['bestaetigung_von']) + ' -> ' + str(ko['bestaetigung_von']):<26}"
              f"{e['loader_lesart']['erstes_jahr_loader']} "
              f"({e['loader_lesart']['schranke']} {e['loader_lesart']['wert']})")
    print("-" * 96)
    print(f"Erste Faltenjahre ohne Schranke: {m['erste_faltenjahre_ohne_schranke']}  "
          f"-> dasselbe Jahr fuer alle: {_ja(m['dasselbe_jahr_fuer_alle'])}")
    print(f"Schranke bindet bei: {len(m['bots_bei_denen_die_schranke_bindet'])} Bots "
          f"{m['bots_bei_denen_die_schranke_bindet']}")
    print(f"Faltenzahl aendert sich bei: {m['bots_mit_geaenderter_faltenzahl']}")
    print(f"Bestaetigungsperiode aendert sich bei: {m['bots_mit_geaenderter_bestaetigung']}")
    print(f"Zulassung nach 4b aendert sich bei: {m['bots_mit_geaenderter_zulassung_4b']}")

    print("\nSelektionsfalten und Symbolzahl je Falte (Lesart A), ohne Schranke")
    print("-" * 96)
    for bot, e in m["je_bot"].items():
        ko = e["ohne_schranke"]
        print(f"{bot:<28}{', '.join(ko['selektionsfalten'])}  |  Best.: "
              f"{ko['bestaetigungsperiode']}")
        print(f"{'':<28}A: {' / '.join(str(n) for n in ko['symbolzahl_je_selektionsfalte'])}"
              f"  B: {' / '.join(str(n) for n in ko['symbolzahl_je_selektionsfalte_lesart_b'])}")

    k = m["elliott_wave_kerzen"]
    print(f"\nelliott_wave ausdruecklich - {k['schranke']} = {k['wert']} Kerzen (1h)")
    print("-" * 96)
    print(f"{'Symbol':<12}{'erster Tag':<12}{'Kerzen':>8}{'fehlend':>8}"
          f"{'N-te Kerze am':>15}{'lueckenlos ab':>15}{'Verzug (Tage)':>15}")
    for symbol, w in k["symbole"].items():
        if not w:
            print(f"{symbol:<12}(keine Kursdatei)")
            continue
        print(f"{symbol:<12}{w['erster_tag']:<12}{w['kerzen']:>8}{w['fehlende_kerzen']:>8}"
              f"{str(w['n_te_kerze_am']):>15}{w['n_te_kerze_bei_lueckenloser_reihe']:>15}"
              f"{str(w['verzoegerung_durch_luecken_tage']):>15}")
    print(f"fruehestes Symbol handelbar ab {k['fruehestes_symbol_handelbar_ab']} "
          f"-> Loader-Jahr {k['erstes_jahr_loader']}; unter der Schranke: "
          f"{k['symbole_unter_der_schranke']}")
    print("\nRein lesend - es wurde nichts geaendert.")


def main(argv=None) -> int:
    z = argparse.ArgumentParser(description="TB-56: Faltenschranke messen.")
    z.add_argument("--json", default=None, help="Messung als JSON ablegen")
    z.add_argument("--plan-ohne-schranke", default=None,
                   help="den Plan ohne Schranke im Format von faltenplan_neun --json ablegen")
    z.add_argument("--mit-trockenlauf", action="store_true",
                   help="dem Plan ohne Schranke das Ergebnis des Loader-Trockenlaufs "
                        "(Registertext 3b, Lesart H) je Bot beilegen")
    z.add_argument("--mutation", type=int, default=None, metavar="JAHR",
                   help="Gegenprobe: Schranke kuenstlich bei JAHR wieder einsetzen")
    z.add_argument("--trockenlauf", default=None, metavar="AUS.json",
                   help="den Loader-Trockenlauf (TB-40) auf den Plan ohne Schranke ansetzen")
    z.add_argument("--bot", action="append", default=None,
                   help="Trockenlauf nur fuer diesen Bot (mehrfach moeglich)")
    a = z.parse_args(argv)

    if a.trockenlauf:
        t = trockenlauf_ohne_schranke(a.bot)
        drucke_trockenlauf(t)
        with open(a.trockenlauf, "w", encoding="utf-8") as f:
            json.dump(t, f, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"Trockenlauf: {a.trockenlauf}")
        return 0

    if a.mutation is not None:
        r = mutation(a.mutation)
        print(f"Mutationsgegenprobe: Schranke bei {r['schranke']} -> "
              f"{r['anzahl_geaendert']} von {len(fp.BOTS)} Plaenen aendern sich: "
              f"{r['bots_geaendert']}  =>  {'BEISST' if r['beisst'] else 'BEISST NICHT'}")
        for bot, w in r["erste_falte"].items():
            print(f"  {bot:<28}ohne {w['ohne']}  mit {w['mit']}")
        if a.json:
            with open(a.json, "w", encoding="utf-8") as f:
                json.dump(r, f, indent=2, ensure_ascii=False, sort_keys=True)
        return 0 if r["beisst"] else 1

    m = messung()
    drucke(m)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(m, f, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"Messung: {a.json}")
    if a.plan_ohne_schranke:
        datei = {"go_live": fp.GO_LIVE.isoformat(),
                 "frueheste_falte": None,
                 "schranke": "keine - Registertext 4a (TB-56)",
                 "herkunft": ("research/faltenplan_neun/faltenschranke_messung.py: "
                              "faltenplan_neun.py mit FRUEHESTE_FALTE im Speicher = 0; "
                              "Falten nach Lesart A (Kursdaten am 1. Januar), "
                              "Symbolzahlen nach Lesart A und B wie in faltenplan.json"),
                 "plaene": plan_ohne_schranke()}
        if a.mit_trockenlauf:
            t = trockenlauf_ohne_schranke()
            drucke_trockenlauf(t)
            datei["trockenlauf_3b"] = {
                "werkzeug": t["werkzeug"],
                "lesart": "H - handelbar an mindestens einem Handelstag der Falte "
                          "(Registertext 3b (a)); F - am Faltenbeginn",
                "monotonie_verletzt": t["monotonie_verletzt"],
                "schreibversuche": t["schreibversuche"],
                "je_bot": t["je_bot"],
            }
        with open(a.plan_ohne_schranke, "w", encoding="utf-8") as f:
            json.dump(datei, f, indent=2, ensure_ascii=False, sort_keys=True, default=str)
        print(f"Plan ohne Schranke: {a.plan_ohne_schranke}")
    return 0 if m["werkzeug_stimmt_mit_festgehaltener_messung"] else 1


if __name__ == "__main__":
    sys.exit(main())
