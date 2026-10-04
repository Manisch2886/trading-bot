#!/usr/bin/env python3
"""
TB-132 / R71 - Probe am Code: welche Tage laesst `benchmark.py::bh_tagesrenditen` aus?
==============================================================================
Geprueft wird die Voraussetzung aus R71 durch einen TEST, nicht durch Lesen:

    AUSSAGE: Ausser dem ersten Kurstag ab dem fruehesten Handelbar-Tag wird
    kein Tag weggelassen, an dem mindestens ein Symbol handelbar ist und einen
    Kurs traegt.

Aufruf (aus dem Repo-Wurzelverzeichnis; schreibt nichts ins Repo):

    PYTHONDONTWRITEBYTECODE=1 python3 <pfad>/r71_probe.py [pfad/zu/benchmark.py]

Ohne Argument: research/vorregistrierung/benchmark.py relativ zum Arbeitsordner
(oder die Umgebungsvariable R71_BENCHMARK).

Was laeuft - und was ersetzt ist
------------------------------------------------------------------------------
Geladen wird die ECHTE Datei benchmark.py (ihr SHA-256 steht im Kopf der
Ausgabe). Je Fall laeuft der echte Weg `je_bot` (Z. 251-321): `tagesschluss`
liest synthetische Kursdateien `<symbol>_1d.csv` aus einem Wegwerfordner,
`tagesgenau` schneidet auf den Handelbar-Tag, `bh_tagesrenditen` bildet die
Reihe, `je_bot` schneidet sie je Falte aus. `bh_tagesrenditen` ist dabei nur
mit einem Mitschnitt umhuellt (das Original rechnet).

Ersetzt (Monkeypatch im Prozess, keine Repo-Datei wird geaendert):
  * die vier Importe faltenplan / registerdaten / faltenschranke_messung /
    paths durch Attrappen - sie liefern nur: den synthetischen Faltenplan, den
    synthetischen Bot, die synthetischen Handelbar-Tage (statt
    `fsm.loader_lesart`) und die Pfade des Wegwerfordners;
  * sonst nichts. Echte Kurs- oder Ergebnisdaten werden nicht gelesen.

Zwei Gruppen, sauber getrennt
------------------------------------------------------------------------------
  A  Faelle, die die AUSSAGE pruefen. Nur sie bestimmen den Rueckgabewert:
     0, wenn alle sie bestaetigen, sonst 1.
     (i), (ii), (iv), (v) sind die verlangten Faelle; (vi) bis (viii) sind
     Zusatzfaelle des Pruefhelfers (Zusammentreffen von Luecke/Ende und
     Handelbar-Tag) - an ihnen haengt die Aussage am Auffuellen von
     `pct_change`.
  B  Faelle, die nur das VERHALTEN zeigen (Beitrag eines Symbols ohne Kurs,
     Tag ohne jeden Kurs). Ohne Einfluss auf den Rueckgabewert.

Nebenpruefung (ohne Einfluss auf den Rueckgabewert): ueber alle Laeufe wird
gezaehlt, ob in der Reihe ein Tag steht, an dem KEIN handelbares Symbol einen
Kurs traegt (R66 (a): jeder Benchmark-Tag ist ein Kurstag).

Eine Kursluecke wird in A/B je zweimal gebaut: als fehlende Zeile der
Kursdatei und als Zeile mit leerem `close` (`tagesschluss` verwirft sie mit
`dropna`). Beide muessen dieselbe Reihe ergeben.
"""

import hashlib
import importlib.util
import os
import sys
import tempfile
import types
import warnings

sys.dont_write_bytecode = True          # nie ein __pycache__ neben benchmark.py

import numpy as np                       # noqa: E402
import pandas as pd                      # noqa: E402

BOT = "probe_bot"
MARKT = "aktien"

# Ueber alle Laeufe gesammelt (Nebenpruefung zu R66 (a), Wortlaut der Warnung).
SAMMLER = {"laeufe": 0, "zusaetzliche_tage": 0, "warnungstexte": set()}

# 20 synthetische Handelstage ueber einen Jahreswechsel: T[0..9] im Dezember
# 2021, T[10..19] im Januar 2022. Zwei Falten, halboffen wie im Faltenplan.
T = list(pd.bdate_range("2021-12-20", periods=20))
FALTEN = [
    {"name": "2021", "rolle": "selektion",
     "von": "2021-01-01", "bis_ausschliesslich": "2022-01-01"},
    {"name": "2022", "rolle": "bestaetigung",
     "von": "2022-01-01", "bis_ausschliesslich": "2023-01-01"},
]
# Variante fuer (i-b): die erste Falte beginnt NACH dem ersten Kurstag.
FALTEN_SPAET = [
    {"name": "A", "rolle": "selektion",
     "von": "2021-12-21", "bis_ausschliesslich": "2022-01-01"},
    {"name": "B", "rolle": "bestaetigung",
     "von": "2022-01-01", "bis_ausschliesslich": "2023-01-01"},
]


def kurs_x(t: int) -> float:
    return 100.0 + 1.7 * t + (t % 4) * 0.9


def kurs_y(t: int) -> float:
    return 40.0 + 0.6 * t + ((3 * t) % 5) * 0.7


KURS = {"X": kurs_x, "Y": kurs_y}


# ---------------------------------------------------------------------------
# benchmark.py laden - die echte Datei, die vier Importe als Attrappen
# ---------------------------------------------------------------------------
def lade_benchmark(pfad: str):
    attrappen = {}
    for name in ("faltenplan", "registerdaten", "faltenschranke_messung", "paths"):
        attrappen[name] = types.ModuleType(name)
    attrappen["paths"].DATA_DIR = "/nicht/gesetzt"
    attrappen["paths"].CONFIG_DIR = "/nicht/gesetzt"
    attrappen["paths"].RUECKGABEWERT_STARTPRUEFUNG = 2
    attrappen["registerdaten"].UNIVERSUM = {}
    attrappen["registerdaten"].BOTS = {}
    attrappen["registerdaten"].DD_RELATIVER_FAKTOR = 1.25
    vorher = {n: sys.modules.get(n) for n in attrappen}
    pfad_vorher = list(sys.path)
    sys.modules.update(attrappen)
    try:
        spec = importlib.util.spec_from_file_location("benchmark_unter_probe", pfad)
        modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modul)
    finally:
        for n, alt in vorher.items():
            if alt is None:
                sys.modules.pop(n, None)
            else:
                sys.modules[n] = alt
        sys.path[:] = pfad_vorher
    return modul


def sha256(pfad: str) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Ein Lauf: Kursdateien schreiben (Wegwerfordner), je_bot rufen, mitschneiden
# ---------------------------------------------------------------------------
def lauf(bm, kurstage: dict, handelbar: dict, falten=None, luecke="zeile_fehlt"):
    """`kurstage`: {symbol: Menge der Tagesnummern MIT Kurs}; `handelbar`:
    {symbol: Tagesnummer | None}. Liefert die mitgeschnittene Benchmark-Reihe,
    die Handelstage je Falte nach `je_bot`, die Soll-Menge und die Warnungen."""
    falten = falten or FALTEN
    with tempfile.TemporaryDirectory(prefix="r71_probe_") as ordner:
        os.makedirs(os.path.join(ordner, "config"))
        with open(os.path.join(ordner, "config", "probe_aktien.txt"), "w") as f:
            f.write("\n".join(sorted(kurstage)) + "\n")
        with open(os.path.join(ordner, "config", "probe_krypto.txt"), "w") as f:
            f.write("")
        for s, tage in kurstage.items():
            zeilen = ["open_time,open,high,low,close,volume"]
            for t, tag in enumerate(T):
                k = KURS[s](t)
                if t in tage:
                    zeilen.append(f"{tag.date().isoformat()},{k},{k},{k},{k},1000")
                elif luecke == "close_leer":
                    zeilen.append(f"{tag.date().isoformat()},,,,,")
                # luecke == "zeile_fehlt": die Zeile gibt es nicht
            with open(os.path.join(ordner, f"{s}_1d.csv"), "w") as f:
                f.write("\n".join(zeilen) + "\n")

        bm.DATA_DIR = ordner
        bm.CONFIG_DIR = os.path.join(ordner, "config")
        bm.rd.UNIVERSUM = {"aktien": "config/probe_aktien.txt",
                           "krypto": "config/probe_krypto.txt"}
        bm.rd.BOTS = {BOT: {"markt": MARKT, "zeitrahmen": "1d"}}
        bm.fp.faltenplan = lambda mess: {BOT: {"status": "endgueltig",
                                               "falten": falten}}
        bm.fsm.loader_lesart = lambda bot: {
            "schranke": "MIN_HISTORY_DAYS", "wert": 0,
            "handelbar_ab": {s: (None if h is None else T[h].date().isoformat())
                             for s, h in handelbar.items()}}

        original = bm.bh_tagesrenditen
        mitschnitt = {}

        def umhuellt(reihen):
            serie = original(reihen)
            mitschnitt["serie"] = serie
            return serie

        bm.bh_tagesrenditen = umhuellt
        try:
            with warnings.catch_warnings(record=True) as gefangen:
                warnings.simplefilter("always")
                tabellen = bm.je_bot({})
        finally:
            bm.bh_tagesrenditen = original

    serie = mitschnitt["serie"]
    soll = {t for s, tage in kurstage.items() if handelbar.get(s) is not None
            for t in tage if t >= handelbar[s]}
    ist = {T.index(pd.Timestamp(d)) for d in serie.index}
    SAMMLER["laeufe"] += 1
    SAMMLER["zusaetzliche_tage"] += len(ist - soll)
    SAMMLER["warnungstexte"] |= {str(w.message) for w in gefangen
                                 if issubclass(w.category, FutureWarning)}
    return {
        "serie": {T.index(pd.Timestamp(d)): float(v) for d, v in serie.items()},
        "ist": ist,
        "soll": soll,
        "erster": min(soll),
        "fehlend": sorted((soll - {min(soll)}) - ist),
        "zusaetzlich": sorted(ist - soll),
        "handelstage": {n: f["handelstage"]
                        for n, f in tabellen[BOT]["falten"].items()},
        "fill_warnung": sorted({str(w.message)[:60] for w in gefangen
                                if issubclass(w.category, FutureWarning)
                                and "fill_method" in str(w.message)}),
        "andere_warnungen": sorted({f"{w.category.__name__}: {str(w.message)[:60]}"
                                    for w in gefangen
                                    if "fill_method" not in str(w.message)}),
    }


def beide_darstellungen(bm, kurstage, handelbar, falten=None):
    a = lauf(bm, kurstage, handelbar, falten, "zeile_fehlt")
    b = lauf(bm, kurstage, handelbar, falten, "close_leer")
    gleich = (a["ist"] == b["ist"]
              and all(np.isclose(a["serie"][t], b["serie"][t], rtol=1e-12, atol=1e-15)
                      for t in a["ist"]))
    return a, gleich


def tag(t: int) -> str:
    return f"T{t}={T[t].date().isoformat()}"


def rendite(s: str, t: int, zurueck: int = 1) -> float:
    return KURS[s](t) / KURS[s](t - zurueck) - 1.0


def gleich(a: float, b: float) -> bool:
    return bool(np.isclose(a, b, rtol=1e-10, atol=1e-13))


def beitrag(wert, ohne_x: float, mit_null: float, mit_rendite=None) -> str:
    """Welchen Beitrag hat X zum Mittel geleistet? Gelesen am Wert der Reihe."""
    if wert is None:
        return "Tag fehlt in der Reihe"
    if gleich(wert, ohne_x):
        return "X ausgelassen (Mittel nur ueber Y)"
    if gleich(wert, mit_null):
        return "X traegt 0 bei (aufgefuellt; Mittel ueber X und Y)"
    if mit_rendite is not None and gleich(wert, mit_rendite):
        return "X traegt die Rendite ueber die Luecke bei (letzter Kurs vor der Luecke -> heute)"
    return f"anderer Wert ({wert:.6f})"


def warn(e) -> str:
    return "FutureWarning fill_method: " + ("ja" if e["fill_warnung"] else "nein")


ALLE = set(range(20))


# ---------------------------------------------------------------------------
# A - Faelle, die die Aussage pruefen
# ---------------------------------------------------------------------------
def fall_i(bm):
    """Erster Kurstag ab dem fruehesten Handelbar-Tag: fehlt er, und nur einmal?"""
    e = lauf(bm, {"X": ALLE, "Y": ALLE}, {"X": 0, "Y": 12})
    spaet = lauf(bm, {"X": ALLE, "Y": ALLE}, {"X": 0, "Y": 12}, FALTEN_SPAET)
    ok = (not e["fehlend"] and e["erster"] not in e["ist"]
          and len(e["ist"]) == len(e["soll"]) - 1
          and e["handelstage"] == {"2021": 9, "2022": 10}
          and 10 in e["ist"]
          and spaet["handelstage"] == {"A": 9, "B": 10} and not spaet["fehlend"])
    return ok, (f"erster Kurstag {tag(e['erster'])} fehlt: {e['erster'] not in e['ist']}; "
                f"weitere fehlende Tage: {len(e['fehlend'])}; Handelstage je Falte nach je_bot "
                f"{e['handelstage']} bei 10/10 Kurstagen (also einmal, nicht je Falte; erster "
                f"Tag der Falte 2022 {tag(10)} steht in der Reihe: {10 in e['ist']}); "
                f"(i-b) erste Falte beginnt nach dem ersten Kurstag: {spaet['handelstage']} bei "
                f"9/10 Kurstagen, in keiner Falte fehlt ein Tag; {warn(e)}")


def fall_ii(bm):
    """Kursluecke bei X (T6), Y hat an dem Tag einen Kurs."""
    e, g = beide_darstellungen(bm, {"X": ALLE - {6}, "Y": ALLE}, {"X": 0, "Y": 3})
    ok = not e["fehlend"] and 6 in e["ist"] and 7 in e["ist"] and g
    return ok, (f"Lueckentag {tag(6)} in der Reihe: {6 in e['ist']}; Folgetag {tag(7)} in der "
                f"Reihe: {7 in e['ist']}; fehlende Tage ausser dem ersten: {len(e['fehlend'])}; "
                f"beide Darstellungen der Luecke gleich: {g}; {warn(e)}")


def fall_iv(bm):
    """Nach dem letzten Kurs von X (T11), Y laeuft weiter."""
    e = lauf(bm, {"X": set(range(12)), "Y": ALLE}, {"X": 0, "Y": 3})
    danach = set(range(12, 20))
    ok = not e["fehlend"] and danach <= e["ist"]
    return ok, (f"Tage nach dem letzten Kurs von X ({tag(12)} bis {tag(19)}) in der Reihe: "
                f"{len(danach & e['ist'])} von 8; fehlende Tage ausser dem ersten: "
                f"{len(e['fehlend'])}; {warn(e)}")


def fall_v(bm):
    """Handelbar-Tag von Y (T8) mitten in der Reihe."""
    e = lauf(bm, {"X": ALLE, "Y": ALLE}, {"X": 0, "Y": 8})
    ok = not e["fehlend"] and 8 in e["ist"]
    return ok, (f"Handelbar-Tag von Y {tag(8)} in der Reihe: {8 in e['ist']}; fehlende Tage "
                f"ausser dem ersten: {len(e['fehlend'])}; {warn(e)}")


def fall_vi(bm):
    """ZUSATZ: Handelbar-Tag von Y (T8) faellt auf eine Kursluecke von X (T8)."""
    e, g = beide_darstellungen(bm, {"X": ALLE - {8}, "Y": ALLE}, {"X": 0, "Y": 8})
    ok = not e["fehlend"] and g
    w = e["serie"].get(8)
    return ok, (f"{tag(8)} (Y handelbar mit Kurs, X ohne Kurs) in der Reihe: {8 in e['ist']}"
                + ("" if w is None else f", Wert {w:.6f}")
                + f"; fehlende Tage ausser dem ersten: {[tag(t) for t in e['fehlend']]}; "
                  f"beide Darstellungen gleich: {g}; {warn(e)}")


def fall_vii(bm):
    """ZUSATZ: Y wird handelbar (T8), nachdem X seinen letzten Kurs hatte (T5)."""
    e = lauf(bm, {"X": set(range(6)), "Y": ALLE}, {"X": 0, "Y": 8})
    ok = not e["fehlend"]
    w = e["serie"].get(8)
    return ok, (f"{tag(8)} (erster Kurstag von Y ab Handelbar-Tag, X seit {tag(5)} ohne Kurs) "
                f"in der Reihe: {8 in e['ist']}" + ("" if w is None else f", Wert {w:.6f}")
                + f"; fehlende Tage ausser dem ersten: {[tag(t) for t in e['fehlend']]}; {warn(e)}")


def fall_viii(bm):
    """ZUSATZ: versetzte Luecken - X ohne Kurs an T6, Y ohne Kurs an T7."""
    e, g = beide_darstellungen(bm, {"X": ALLE - {6}, "Y": ALLE - {7}}, {"X": 0, "Y": 3})
    ok = not e["fehlend"] and g
    return ok, (f"{tag(6)} (nur Y mit Kurs) in der Reihe: {6 in e['ist']}; {tag(7)} (nur X mit "
                f"Kurs, X kommt aus der Luecke) in der Reihe: {7 in e['ist']}; fehlende Tage "
                f"ausser dem ersten: {[tag(t) for t in e['fehlend']]}; beide Darstellungen "
                f"gleich: {g}; {warn(e)}")


# ---------------------------------------------------------------------------
# B - Faelle, die nur das Verhalten zeigen
# ---------------------------------------------------------------------------
def verhalten_ii(bm):
    e = lauf(bm, {"X": ALLE - {6}, "Y": ALLE}, {"X": 0, "Y": 3})
    ry6, ry7 = rendite("Y", 6), rendite("Y", 7)
    am = beitrag(e["serie"].get(6), ry6, ry6 / 2.0)
    nach = beitrag(e["serie"].get(7), ry7, ry7 / 2.0, (rendite("X", 7, 2) + ry7) / 2.0)
    return f"Lueckentag {tag(6)}: {am}. Folgetag {tag(7)}: {nach}."


def verhalten_iii(bm):
    e, g = beide_darstellungen(bm, {"X": ALLE - {6}}, {"X": 0})
    w = e["serie"].get(7)
    if w is None:
        folge = "fehlt ebenfalls"
    elif gleich(w, rendite("X", 7, 2)):
        folge = "traegt die Rendite ueber die Luecke (T5 -> T7)"
    else:
        folge = f"anderer Wert ({w:.6f})"
    return (f"einziges Symbol X ohne Kurs an {tag(6)}: Tag in der Reihe: {6 in e['ist']} "
            f"(kein Symbol traegt einen Kurs - die Aussage ist nicht beruehrt); Folgetag "
            f"{tag(7)} {folge}; beide Darstellungen gleich: {g}; {warn(e)}")


def verhalten_iii_b(bm):
    e = lauf(bm, {"X": ALLE - {6}, "Y": ALLE}, {"X": 0, "Y": 15})
    return (f"X ohne Kurs an {tag(6)}, Y steht in der Universumsdatei und traegt dort einen "
            f"Kurs, ist aber erst ab {tag(15)} handelbar: Tag in der Reihe: {6 in e['ist']} "
            f"(ein Kurstag des Marktes nach R66 (a), aber kein Benchmark-Tag); {warn(e)}")


def verhalten_iv(bm):
    e = lauf(bm, {"X": set(range(12)), "Y": ALLE}, {"X": 0, "Y": 3})
    arten = sorted({beitrag(e["serie"].get(t), rendite("Y", t), rendite("Y", t) / 2.0)
                    for t in range(12, 20)})
    return (f"nach dem letzten Kurs von X ({tag(11)}), an den 8 Folgetagen: "
            + " / ".join(arten) + ".")


def verhalten_v(bm):
    e = lauf(bm, {"X": ALLE, "Y": ALLE}, {"X": 0, "Y": 8})
    w8, w9 = e["serie"].get(8), e["serie"].get(9)
    a = ("nur X (Y hat an seinem Handelbar-Tag noch keine Rendite)"
         if w8 is not None and gleich(w8, rendite("X", 8)) else f"anderer Wert ({w8})")
    b = ("Mittel ueber X und Y"
         if w9 is not None and gleich(w9, (rendite("X", 9) + rendite("Y", 9)) / 2.0)
         else f"anderer Wert ({w9})")
    return f"Handelbar-Tag von Y {tag(8)}: {a}; Folgetag {tag(9)}: {b}."


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    pfad = (argv[0] if argv else os.environ.get("R71_BENCHMARK")
            or os.path.join("research", "vorregistrierung", "benchmark.py"))
    if not os.path.isfile(pfad):
        print(f"NICHT PRUEFBAR: {pfad} fehlt (aus dem Repo-Wurzelverzeichnis starten "
              f"oder den Pfad als Argument geben).", file=sys.stderr)
        return 2
    bm = lade_benchmark(pfad)
    print(f"R71-Probe: {os.path.abspath(pfad)}")
    print(f"  SHA-256 {sha256(pfad)}")
    print(f"  pandas {pd.__version__}, numpy {np.__version__}, "
          f"Python {sys.version.split()[0]}")
    print("  Weg: je_bot -> tagesschluss (synthetische CSV) -> tagesgenau -> "
          "bh_tagesrenditen; Importe faltenplan/registerdaten/"
          "faltenschranke_messung/paths sind Attrappen.")

    print("\nA - Faelle, die die Aussage pruefen (bestimmen den Rueckgabewert)")
    alle_ok = True
    for name, fn in (("(i)", fall_i), ("(ii)", fall_ii), ("(iv)", fall_iv),
                     ("(v)", fall_v), ("(vi)", fall_vi), ("(vii)", fall_vii),
                     ("(viii)", fall_viii)):
        ok, text = fn(bm)
        alle_ok = alle_ok and ok
        print(f"Fall {name}: {'OK' if ok else 'ABWEICHUNG'} — {text}")

    print("\nB - Faelle, die nur das Verhalten zeigen (ohne Einfluss auf den Rueckgabewert)")
    for name, fn in (("(ii)", verhalten_ii), ("(iii)", verhalten_iii),
                     ("(iii-b)", verhalten_iii_b), ("(iv)", verhalten_iv),
                     ("(v)", verhalten_v)):
        print(f"Fall {name}: VERHALTEN — {fn(bm)}")

    print("\nNebenpruefung (R66 (a), ohne Einfluss auf den Rueckgabewert): in "
          f"{SAMMLER['laeufe']} Laeufen stehen {SAMMLER['zusaetzliche_tage']} Tage in "
          "der Reihe, an denen kein handelbares Symbol einen Kurs traegt.")
    if SAMMLER["warnungstexte"]:
        for text in sorted(SAMMLER["warnungstexte"]):
            print(f"FutureWarning (Wortlaut): {text}")
    else:
        print("FutureWarning: keine.")
    print(f"\nERGEBNIS: Aussage {'bestaetigt' if alle_ok else 'NICHT bestaetigt'} "
          f"unter pandas {pd.__version__} -> Rueckgabewert {0 if alle_ok else 1}")
    return 0 if alle_ok else 1


if __name__ == "__main__":
    sys.exit(main())
