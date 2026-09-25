#!/usr/bin/env python3
"""
TB-30a - Vorab-Berechnung: Benchmark-Drawdowns je Falte, DD_Toleranz je Bot
==============================================================================
Die Drawdown-Bedingung der Vorregistrierung lautet (Festlegung 4):

    erlaubt(f) = min(1,25 x DD_Benchmark(f), DD_Toleranz)

Beide Werte sind negativ; `min` ist der TIEFERE und damit die grosszuegigere
Grenze. Ein Parametersatz besteht eine Falte, wenn sein Kapital-Drawdown in
dieser Falte nicht tiefer liegt als `erlaubt(f)`.

WAS HIER VORAB BERECHNET WIRD - UND WAS NICHT
------------------------------------------------------------------------------
Der Benchmark ist eine **statische Position** in Hoehe der mittleren Exposure
im gleichgewichteten point-in-time-Universum. Seine Exposure ist damit erst im
Lauf bekannt: es gilt die mittlere Exposure des JEWEILIGEN Parametersatzes in
der JEWEILIGEN Falte, nicht die heute gemessene des Bots. Vorab berechenbar
ist deshalb nicht EINE Zahl je Falte, sondern die **Funktion**:

    DD_Benchmark(f, e)   fuer e = 1 %, 2 %, ..., 100 %

Diese Tabelle steht auf der Sperrliste. Im Lauf wird darin nachgeschlagen -
linear zwischen den beiden benachbarten Stuetzstellen interpoliert -, nichts
neu gerechnet. So verweist keine Zahl des Registers auf den Live-Zustand, und
die satzweise Verfeinerung geschieht trotzdem im Lauf.

DD_TOLERANZ - WARUM SIE EBENFALLS EIN EXPOSURE-ARGUMENT TRAEGT
------------------------------------------------------------------------------
Festlegung 5 sagt: DD_Toleranz ist der **Median der Benchmark-Drawdowns ueber
alle Selektionsfalten, je Bot**. Da der Benchmark-Drawdown nach Festlegung 4
selbst von der Exposure abhaengt, erbt der Median dieses Argument:

    DD_Toleranz(e) = Median ueber die Selektionsfalten von DD_Benchmark(f, e)

Das ist keine zusaetzliche Entscheidung, sondern die einzige Lesart, die mit
Festlegung 4 zusammenpasst - und sie erfuellt genau das, was Festlegung 5
bezweckt: "Je Bot, zwingend - ein Bot mit 21 % Zeit im Markt liegt auf einer
anderen Skala als einer mit 100 %." Die Skala kommt jetzt aus der Exposure
selbst statt aus einem heute gemessenen Live-Zustand, und die ruhige Falte
wird trotzdem gerettet:

    ruhige Falte: DD_Benchmark = -2 %, 1,25 x = -2,5 %, DD_Toleranz = -8 %
                  -> erlaubt = -8 %, ein Satz mit -4 % besteht
    Krisenfalte:  DD_Benchmark = -35 %, 1,25 x = -43,75 %, DD_Toleranz = -8 %
                  -> erlaubt = -43,75 %, die relative Grenze bindet

DAS UNIVERSUM - TAGESGENAU NACH DEM LOADER DES BOTS (Registertext 3b (c))
------------------------------------------------------------------------------
Der Benchmark einer Falte wird **tagesgenau** aus den Symbolen gebildet, die
der Loader des Bots an diesem Tag handelbar macht (Registertext 3b (c) in der
Fassung der Berichtigung TB-66, 20.09.2026; Lesart VT). Handelbar ist ein
Symbol ab dem Tag, an dem seine Historie die registrierte Loader-Schranke
erreicht (Registertext 3b (b): `MIN_HISTORY_DAYS` 500 / 730 / 1 825 als
Zeitspanne, bei `elliott_wave` `MIN_HISTORY_HOURS` 17 520 als Kerzenzahl).
Dieses Datum wird NICHT hier nachgebaut, sondern ueber
`research/faltenplan_neun/faltenschranke_messung.py::loader_lesart` gelesen -
dem TB-56-Werkzeug, dessen Mengen TB-65 in 78 von 78 Falten gegen den
Trockenlauf des Laufcodes bestaetigt hat. Die Schranke selbst liest es aus
der Bot-Datei; hier steht keine Kopie davon.

Jede Kursreihe beginnt fuer den Benchmark an ihrem Handelbar-Tag; ihre erste
Tagesrendite ist die vom Handelbar-Tag auf den Folgetag (frueher haette der
Bot das Symbol nicht halten koennen). Innerhalb einer Falte wechselt die Menge
deshalb von Tag zu Tag: gleichgewichtet, taeglich rebalanciert ueber die an
diesem Tag handelbaren Symbole. Bot und Benchmark leben an jedem Tag in
derselben Menge.

⚠️ Bis TB-66 stand hier der Vierjahresfilter `point_in_time(...,
MINDESTTRAINING_JAHRE)` - ein Symbol ging fuer die GANZE Falte ein, wenn seine
Kursdaten vier Jahre vor Faltenbeginn einsetzten. Das war das Verfahren-A-
Artefakt, das mit `MINDESTTRAINING` schon aus dem Faltenplan gegangen ist
(Register 15.1, Sperrliste Punkt 8 Vermerk); in den Krypto-Falten 2018-2021
liess es den Benchmark leer und die Drawdown-Nebenbedingung damit wirkungslos
(docs/ERGEBNIS_TB-61_benchmark_neun.md, docs/ERGEBNIS_TB-65_benchmarkschranke.md).

Gemittelt werden Tagesrenditen, nicht Kurse - die Summe roher Schlusskurse
ist genau der Fehler, der beim APH-Vorfall die gesamte Portfoliosumme zu NaN
gemacht hat (Protokoll 3.3).
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
# TB30A_BASE_DIR ersetzt die Repo-Wurzel fuer Mutationsproben (Kopien dieses
# Ordners finden so `shared/` und `research/faltenplan_neun/`) - KEIN Weg zum
# Snapshot (TB-104). Kurs- und Universumspfade: unten, ueber den Resolver.
BASE_DIR = os.environ.get("TB30A_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))

import faltenplan as fp  # noqa: E402
import registerdaten as rd  # noqa: E402

# Das Handelbar-Datum je Symbol kommt aus dem TB-56-Werkzeug (siehe Kopf).
sys.path.insert(0, os.path.join(BASE_DIR, "research", "faltenplan_neun"))
import faltenschranke_messung as fsm  # noqa: E402

# --- Pfade der Kurs- und Universumsdateien: der Resolver (TB-104) -----------
# ⚠️ Fable 24c Abschnitt 2 / 25a (C): Jedes Modul des Laufbereichs, das Kurs-
# oder Universumsdateien liest, bezieht seine Pfade ueber `shared/paths.py` -
# direkt wie `messgroessen.py` (TB-103), nicht ueber
# `strategy_paths.get_strategy_paths()` (legt `results/<name>/` und
# `logs/<name>/` an). Ohne Modus `data/` und `config/` der Repo-Wurzel wie
# vorher, unter dem Modus der Snapshot (Kurse flach, Universum unter
# `config/`). Bis TB-104 stand hier `DATA_DIR = os.path.join(BASE_DIR, "data")`
# und das Universum kam aus `BASE_DIR + registerdaten.UNIVERSUM` - der Modus
# war unbekannt. Der Dateiname kommt weiter aus `registerdaten.UNIVERSUM`
# (`os.path.basename`), keine zweite Namensliste.
sys.path.insert(0, os.path.join(BASE_DIR, "shared"))
import paths  # noqa: E402

DATA_DIR = paths.DATA_DIR
CONFIG_DIR = paths.CONFIG_DIR


def _abbruch_2(stelle: str, text: str):
    """TB-106 (Fable 24b A2, 25a Rang 3): ein fehlender Wert ist ein
    Widerspruch zwischen Register und Eingabe, kein Laufzustand. Meldung auf
    stderr, dann `SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)` -
    unabhaengig vom Modus."""
    print(f"ABBRUCH (benchmark.py::{stelle}): {text}", file=sys.stderr)
    raise SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)

# Stuetzstellen der Exposure-Achse: 1 % bis 100 % in Schritten von 1 %.
# Feiner waere Genauigkeit ohne Aussage - die Kapitalpfade selbst sind auf
# zwei Nachkommastellen ausgewiesen.
EXPOSURE_STUFEN = [round(0.01 * k, 2) for k in range(1, 101)]


def universumsdatei(markt: str) -> str:
    return os.path.join(CONFIG_DIR, os.path.basename(rd.UNIVERSUM[markt]))


def symbole(markt: str) -> list:
    with open(universumsdatei(markt), encoding="utf-8") as f:
        s = [z.strip() for z in f if z.strip()]
    return [x for x in s if x not in {"XAUTUSDT", "PAXGUSDT"}]


def tagesschluss(markt: str) -> dict:
    """Schlusskurs-Reihen je Symbol, Tagesaufloesung."""
    reihen = {}
    for s in sorted(symbole(markt)):
        pfad = os.path.join(DATA_DIR, f"{s}_1d.csv")
        if not os.path.exists(pfad):
            continue
        df = pd.read_csv(pfad, parse_dates=["open_time"])
        df = df.dropna(subset=["close"])
        if df.empty:
            continue
        reihen[s] = pd.Series(df["close"].to_numpy(dtype=float),
                              index=pd.DatetimeIndex(df["open_time"]))
    return reihen


def tagesgenau(reihen: dict, handelbar: dict) -> dict:
    """Lesart VT: jede Reihe beginnt an ihrem Handelbar-Tag.

    `handelbar` ist je Symbol der erste Tag, an dem der Loader des Bots es
    handelbar macht - gelesen ueber `faltenschranke_messung.loader_lesart`
    (Registertext 3b (b): erster Kurstag + MIN_HISTORY_DAYS; `elliott_wave`:
    Tag der 17 520. 1h-Kerze).

    Die Reihe behaelt den Schlusskurs des Handelbar-Tags, damit die erste
    Tagesrendite die vom Handelbar-Tag auf den Folgetag ist - `pct_change`
    liefert fuer den ersten Punkt NaN, und `bh_tagesrenditen` mittelt an jedem
    Tag nur ueber die Symbole, die dort eine Rendite haben. So wechselt die
    Menge innerhalb der Falte, ohne dass die Rechenfunktion etwas davon weiss.
    Symbole ohne Handelbar-Tag (keine Kursdatei, Schranke nie erreicht) fallen
    weg - sie sind an keinem Tag handelbar.
    """
    aus = {}
    for s, r in reihen.items():
        ab = handelbar.get(s)
        if ab is None:
            continue
        r = r[r.index >= ab]
        if not r.empty:
            aus[s] = r
    return aus


def bh_tagesrenditen(reihen: dict) -> pd.Series:
    """Gleichgewichtet, taeglich rebalanciert: Mittel der Tagesrenditen.

    An jedem Tag der Mittelwert der Tagesrenditen aller Symbole, die dort eine
    Rendite haben - das ist ein taeglich auf Gleichgewicht zurueckgesetztes
    Portfolio, KEIN Buy-and-Hold (dessen Gewichte drifteten mit den Kursen).
    Bis TB-66 hiess es hier "Gleichgewichteter Buy-and-Hold"; der Name
    versprach etwas anderes als die Rechnung tut (Fable, 20.09.2026).

    Zeichengleich zu research/exposure_messung/exposure_kern.py - dieselbe
    Rechnung, damit die Benchmark-Definition im Repo nicht zweimal
    auseinanderlaufen kann.
    """
    rahmen = pd.DataFrame(reihen).sort_index()
    return rahmen.pct_change().mean(axis=1, skipna=True).dropna()


def drawdown_bei_exposure(renditen: pd.Series, exposure: float) -> float:
    """Max Drawdown einer statischen Position der Groesse `exposure`.

    Die Position ist taeglich gleichgewichtet; das Kapital waechst mit
    `1 + exposure * r`. Gerundet wird auf zwei Nachkommastellen, wie ueberall
    in der Messkette (shared/messkette.py).
    """
    if renditen.empty:
        _abbruch_2("drawdown_bei_exposure",
                   "leere Renditereihe - kein Drawdown bestimmbar; bis TB-106 "
                   "stand hier still 0.0")
    kapital = np.cumprod(1.0 + exposure * renditen.to_numpy(dtype=float))
    hoch = np.maximum.accumulate(np.concatenate(([1.0], kapital)))[1:]
    return round(float(np.min(kapital / hoch - 1.0) * 100.0), 2)


def nachschlagen(tabelle: dict, exposure: float) -> float:
    """Der Benchmark-Drawdown bei beliebiger Exposure - lineare Interpolation.

    Diese Funktion ist die EINZIGE Art, wie im Lauf auf die Tabelle
    zugegriffen wird. Sie steht hier, damit die Interpolationsregel mit der
    Tabelle zusammen auf der Sperrliste steht.
    """
    e = max(0.0, min(1.0, float(exposure)))
    if e <= 0:
        return 0.0
    stufen = sorted(float(k) for k in tabelle)
    if e <= stufen[0]:
        return float(tabelle[_schluessel(stufen[0])]) * e / stufen[0]
    for a, b in zip(stufen, stufen[1:]):
        if a <= e <= b:
            ya = float(tabelle[_schluessel(a)])
            yb = float(tabelle[_schluessel(b)])
            if b == a:
                return ya
            return ya + (yb - ya) * (e - a) / (b - a)
    return float(tabelle[_schluessel(stufen[-1])])


def _schluessel(e: float) -> str:
    return f"{e:.2f}"


def je_bot(mess: dict) -> dict:
    plan = fp.faltenplan(mess)
    kurse = {markt: tagesschluss(markt) for markt in ("aktien", "krypto")}
    aus = {}
    for bot, eig in rd.BOTS.items():
        p = plan[bot]
        eintrag = {
            "markt": eig["markt"],
            "status": p["status"],
            "universumsdatei": rd.UNIVERSUM[eig["markt"]],
            "falten": {},
            "dd_toleranz": {},
        }
        # Lesart VT (Registertext 3b (c), TB-66): die Menge haengt am Tag,
        # nicht an der Falte. Die Renditereihe des Bots wird deshalb EINMAL
        # ueber die tagesgenau beginnenden Kursreihen gebildet und je Falte
        # nur noch ausgeschnitten.
        lesart = fsm.loader_lesart(bot)
        handelbar = {s: pd.Timestamp(d)
                     for s, d in lesart["handelbar_ab"].items() if d}
        reihen = tagesgenau(kurse[eig["markt"]], handelbar)
        renditen = bh_tagesrenditen(reihen)
        eintrag["benchmark"] = ("tagesgenau nach dem Loader des Bots "
                                "(Registertext 3b (c), Lesart VT, TB-66)")
        eintrag["loader_schranke"] = f"{lesart['schranke']} = {lesart['wert']}"
        eintrag["handelbar_ab"] = dict(sorted(lesart["handelbar_ab"].items()))
        sel = []
        for f in p["falten"]:
            von = pd.Timestamp(f["von"])
            bis = pd.Timestamp(f["bis_ausschliesslich"])
            # Bot ohne ein einziges handelbares Symbol: die leere Reihe traegt
            # keinen Zeitindex und liesse sich nicht filtern (Wache aus TB-61).
            # Sie geht unveraendert weiter; drawdown_bei_exposure() bricht
            # dafuer seit TB-106 mit 2 ab (bis dahin 0.0). Eine Falte VOR dem
            # ersten Handelbar-Tag ergibt ein leeres Fenster mit demselben
            # Ergebnis.
            if renditen.empty:
                fenster = renditen
            else:
                fenster = renditen[(renditen.index >= von) & (renditen.index < bis)]
            tab = {_schluessel(e): drawdown_bei_exposure(fenster, e)
                   for e in EXPOSURE_STUFEN}
            # Symbole, die in dieser Falte an mindestens einem Tag eine
            # Rendite beitragen: ein Kurstag im Fenster, der nicht der erste
            # Punkt der (am Handelbar-Tag beginnenden) Reihe ist.
            in_falte = sum(
                1 for r in reihen.values()
                if ((r.index >= von) & (r.index < bis) & (r.index != r.index[0])).any())
            eintrag["falten"][f["name"]] = {
                "rolle": f["rolle"],
                "von": f["von"],
                "bis_ausschliesslich": f["bis_ausschliesslich"],
                "symbole_handelbar_in_falte": int(in_falte),
                "handelstage": int(len(fenster)),
                "dd_benchmark": tab,
            }
            if f["rolle"] == "selektion":
                sel.append(tab)

        # DD_Toleranz: Median ueber die SELEKTIONSFALTEN, je Exposure-Stufe.
        # Ohne Selektionsfalte ist er nicht definiert (TB-106; bis dahin 0.0).
        if not sel:
            _abbruch_2("je_bot",
                       f"{bot}: keine Selektionsfalte - DD_Toleranz ist der Median "
                       f"ueber die Selektionsfalten; bis TB-106 stand hier still 0.0")
        for e in EXPOSURE_STUFEN:
            k = _schluessel(e)
            werte = [t[k] for t in sel]
            eintrag["dd_toleranz"][k] = round(float(np.median(werte)), 2)
        aus[bot] = eintrag
    return aus


def erlaubt(dd_benchmark: float, dd_toleranz: float) -> float:
    """Festlegung 4 - die Grenze selbst, an einer Stelle.

    Beide Werte sind negativ (oder 0). `min` liefert den TIEFEREN und damit
    die grosszuegigere Grenze.
    """
    return min(rd.DD_RELATIVER_FAKTOR * dd_benchmark, dd_toleranz)


def _sha256_datei(pfad: str) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def voreinstellung_ziel() -> str:
    """Das voreingestellte Schreibziel - Registertext 36.1 (3), (4).

    ⚠️ Bis TB-91 (23.09.2026) war die Voreinstellung von `--ziel`
    `ergebnisse/benchmark_drawdowns.json` - Sperrlistenpunkt 4. Ein einziger
    Aufruf ohne Argument haette die gesperrte Tabelle ueberschrieben, und der
    Kommentar an der Stelle sagte es selbst: *"ohne diesen Schalter
    ueberschriebe jeder Lauf sie"*. 36.1 (3): die Voreinstellung eines
    Erzeugers ist nie ein Pfad, der auf der Sperrliste steht; der gesperrte
    Pfad ist seither nur noch ueber `--ziel` erreichbar, wo die Sperre aus
    36.1 (2) dann zuschlaegt.

    ⭐ Gleichartig zu `faltenplan.voreinstellung_ziel` (TB-86, `4daa254`),
    nicht neu erfunden. Der Zeitstempel (UTC) ist kein Schmuck: Die
    Einmal-Schreibsperre bricht ab, sobald die Zieldatei existiert - bei einem
    FESTEN Voreinstellungsnamen liesse sich `main()` nach dem ersten Lauf nie
    wieder aufrufen.
    """
    stempel = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    return os.path.join(_HIER, "ergebnisse", f"benchmark_drawdowns_{stempel}.json")


def schreibe_tabellen(tabellen: dict, ziel: str):
    """Schreibt die Tabellen GENAU EINMAL. Liefert (rueckgabewert, text).

    Registertext 36.1 (2), zeichengleich: *"Jeder Erzeuger einer solchen Datei
    schreibt einmalig: Existiert die Zieldatei bereits, bricht er ab
    (Rueckgabewert != 0), nennt Pfad und Hash der vorhandenen Datei und
    schreibt nichts. Er ueberschreibt nie, auch nicht mit identischem
    Inhalt."* Nach 36.5 endet der Erzeuger, der wegen vorhandener Zieldatei
    nicht schreibt, mit **1** - er hat geprueft und einen Befund.

    ⚠️ `indent=1` und `sort_keys=True` sind die Formatierung seit TB-61
    und bleiben unveraendert: Eine Neurechnung muss mit den vorhandenen
    Tabellen vergleichbar bleiben (Fable 23b, Determinismusnachweis).
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
        json.dump(tabellen, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    return 0, f"\nGeschrieben: {ziel}"


def main(argv=None):
    # --ziel (TB-61): wohin die Tabelle geschrieben wird.
    #
    # ⚠️ BERICHTIGT in TB-91 (23.09.2026): Die Voreinstellung war bis dahin
    # `ergebnisse/benchmark_drawdowns.json` - Sperrlistenpunkt 4 - und der
    # Kommentar an dieser Stelle beschrieb die Gefahr, ohne sie abzustellen
    # ("ohne diesen Schalter ueberschriebe jeder Lauf sie"). Registertext
    # 36.1 (3) verlangt das Gegenteil: Die Voreinstellung eines Erzeugers ist
    # nie ein Pfad, der auf der Sperrliste steht. Seither ist sie ein Name mit
    # Zeitstempel; der gesperrte Pfad ist nur noch ueber `--ziel` erreichbar,
    # und dort greift die Einmal-Schreibsperre aus 36.1 (2).
    zerleger = argparse.ArgumentParser(
        description="Benchmark-Drawdowns je Falte, DD_Toleranz je Bot. "
                    "Schreibt einmalig; Voreinstellung ist ein Name mit "
                    "Zeitstempel (36.1 (3)). Kurs- und Universumsdateien ueber "
                    "shared/paths.py (unter dem Selektionsmodus aus dem "
                    "Snapshot); TB30A_BASE_DIR ist KEIN Weg zum Snapshot "
                    "(TB-104).")
    zerleger.add_argument(
        "--ziel", default=None,
        help="Ausgabedatei (Standard: ergebnisse/benchmark_drawdowns_"
             "<UTC-Zeitstempel>.json). Ein vorhandenes Ziel wird NIE "
             "ueberschrieben - der Lauf endet dann mit 1.")
    ziel = zerleger.parse_args(argv).ziel or voreinstellung_ziel()

    # ⚠️ Die Sperre greift VOR der Rechnung, wenn das Ziel schon da ist:
    # eine halbe Stunde rechnen und dann abbrechen waere Verschwendung.
    if os.path.exists(ziel):
        rc, text = schreibe_tabellen(None, ziel)
        print(text)
        return rc

    mess = rd._mess()
    tabellen = je_bot(mess)
    rc, text = schreibe_tabellen(tabellen, ziel)
    if rc != 0:
        print(text)
        return rc

    print(__doc__.strip().split("\n")[0])
    for bot, e in tabellen.items():
        print(f"\n{bot}  ({e['markt']})")
        print(f"    {e['benchmark']}; {e['loader_schranke']}")
        print(f"    {'Falte':12s} {'Rolle':12s} {'Symb.':>6s} {'Tage':>5s} "
              f"{'DD@25%':>8s} {'DD@50%':>8s} {'DD@100%':>8s}")
        for name, f in e["falten"].items():
            print(f"    {name:12s} {f['rolle']:12s} "
                  f"{f['symbole_handelbar_in_falte']:6d} {f['handelstage']:5d} "
                  f"{f['dd_benchmark']['0.25']:7.2f}% "
                  f"{f['dd_benchmark']['0.50']:7.2f}% "
                  f"{f['dd_benchmark']['1.00']:7.2f}%")
        print(f"    {'DD_Toleranz':12s} {'':12s} {'':6s} {'':5s} "
              f"{e['dd_toleranz']['0.25']:7.2f}% "
              f"{e['dd_toleranz']['0.50']:7.2f}% "
              f"{e['dd_toleranz']['1.00']:7.2f}%")
    print(f"\nGeschrieben: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
