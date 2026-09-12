"""
Portfolio-Sicht fuer das Dashboard (rein lesend, mit Zwischenspeicher)
==============================================================================
Das Dashboard zeigt neun Bots nebeneinander und beantwortet damit "laeuft
Bot 7?" - nicht "laeuft das Portfolio?". Die Zahlen dafuer rechnet
`shared/portfolio_overview.py` bereits fuer die Montags-Mail; dieses Modul
macht sie maschinenlesbar und damit anzeigbar.

DREI DINGE, DIE HIER WICHTIGER SIND ALS DIE ZAHL SELBST
------------------------------------------------------------------------------
1. **Woher jede Zahl kommt.** `portfolio_overview` nutzt die Live-Datenbank
   eines Bots erst ab MIN_LIVE_CLOSED_TRADES geschlossenen Trades; darunter
   greift es auf die Backtest-Kurve `results/<bot>/equity_curve.csv` zurueck.
   Heute liegen mehrere Bots unter der Schwelle - die Portfolio-Zahl ist also
   teils real, teils Backtest, und das sieht man ihr nicht an. Dieses Modul
   liefert deshalb je Bot die Quelle mit und ZWEI Gruppenergebnisse
   (`nur_echte_trades`, `alle`), niemals eine einzelne Zahl ohne Herkunft.

   Achtung auf das Wort "live": `portfolio_overview.py` nennt seine erste
   Gruppe "LIVE-PORTFOLIO (nur aktivierte Bots)" und meint damit "hat eine
   live_params.py". Alle neun Bots haben eine - diese Zahl stammt heute
   also vollstaendig aus Backtest-Kurven, obwohl sie "live" heisst. Die
   Gruppen hier heissen deshalb `nur_echte_trades` und `alle`.

2. **Bots, die ausfallen, verschwinden nicht.** `load_all_curves()` faengt
   Lesefehler ab, gibt eine `print`-Warnung aus und laesst den Bot aus dem
   Ergebnis fallen. In einem Terminal sieht man das; in einer Oberflaeche
   waere es ein stiller Verlust - die Summe waere ueber weniger Bots gebildet,
   ohne Hinweis. Dieses Modul vergleicht deshalb `discover_bots()` mit
   `load_all_curves()` und fuehrt jeden fehlenden Bot ausdruecklich als
   `quelle="fehlt"` samt Grund.

3. **Kein Bot-Code im Dashboard-Prozess.** `equity_simulation.py` und
   `live_params.py` heissen bei allen neun Bots gleich; ein direkter Import
   mehrerer Bots im selben Prozess schiebt einem Bot lautlos die Funktionen
   eines anderen unter (sys.modules-Kollision). `portfolio_overview` loest das
   mit einem SUBPROZESS je Bot - dieses Modul ruft es deshalb auf, statt
   irgendetwas selbst zu importieren.

WARUM ZWISCHENGESPEICHERT WIRD
------------------------------------------------------------------------------
Gemessen am 12.09.2026 in der Cloud-Sitzung: `load_all_curves()` braucht mit
sieben Bots auf dem Live-Weg **2,9 s** (etwa 0,42 s je Bot, hochgerechnet
~3,8 s fuer neun), weil je Live-Bot ein Python-Subprozess startet. Der reine
Backtest-Weg (alle Bots unter der Schwelle) braucht 134 ms. Das Dashboard
aktualisiert alle 60 s - eine Rechnung im Ladepfad waere also dauerhaft
teuer, und der Notfallweg (Crash-Knopf) darf davon unter keinen Umstaenden
abhaengen.

Es gibt aber einen zweiten, schwerer wiegenden Grund: `portfolio_overview`
legt seine Zwischendateien unter einem FESTEN Namen in
`results/portfolio_overview/` ab (`_live_trades_cache.csv`). Zwei
gleichzeitige Rechnungen - etwa Dashboard und Montags-Mail - wuerden sich
gegenseitig die Datei unter den Fuessen wegschreiben. Dieses Modul lenkt
`RESULTS_DIR` deshalb fuer die Dauer seiner Rechnung auf einen EIGENEN
Ordner um (kein Umbau der Datei, nur ein anderer Wert von aussen) und
serialisiert sich zusaetzlich ueber eine Sperrdatei.

Das Dashboard liest daher nur den Zwischenspeicher und rechnet NIE von
selbst. Neu berechnet wird ausdruecklich: per Knopf im Dashboard, per
Aufruf dieses Skripts oder per Cronjob (Zeile im README, nicht eingetragen).
Das Alter des Zwischenspeichers ist Teil der Anzeige - eine Zahl ohne
Zeitpunkt waere genauso unehrlich wie eine ohne Quelle.

Aufruf:
    python3 dashboard/portfolio_sicht.py            # zeigt den Stand
    python3 dashboard/portfolio_sicht.py --berechnen # rechnet neu
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

_DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DASHBOARD_DIR)

SNAPSHOT_DATEI = os.path.join(BASE_DIR, "results", "portfolio_overview",
                              "dashboard_snapshot.json")
SPERRDATEI = SNAPSHOT_DATEI + ".lock"
# Eigener Ordner fuer die Zwischendateien der Rechnung - siehe Modulkopf.
ARBEITSORDNER = os.path.join(BASE_DIR, "results", "portfolio_overview",
                             "_dashboard_arbeit")

# Ab diesem Alter gilt der Zwischenspeicher als veraltet und wird in der
# Anzeige als solcher gekennzeichnet. 24 Stunden, weil die Bots mit der
# groebsten Taktung taeglich laufen: ein jüngerer Stand kann sich durch neue
# Trades ohnehin nicht geaendert haben, ein aelterer sehr wohl.
MAX_ALTER_SEKUNDEN = 24 * 3600

# Wie lange auf eine laufende Rechnung eines anderen Prozesses gewartet wird,
# bevor die Sperre als verwaist gilt.
SPERRE_GUELTIG_SEKUNDEN = 300

QUELLE_LIVE = "live"
QUELLE_BACKTEST = "backtest"
QUELLE_FEHLT = "fehlt"

# Die Gruppennamen meiden das Wort "live" bewusst.
#
# `portfolio_overview.py` nennt seine erste Gruppe "LIVE-PORTFOLIO (nur
# aktivierte Bots)" - dort heisst "live" aber "hat eine live_params.py", also
# AKTIVIERT. Alle neun Bots haben eine; die "LIVE-PORTFOLIO"-Zahl der
# Montags-Mail stammt daher heute zu 100 % aus Backtest-Kurven. Wer das Wort
# hier fuer "echte Live-Daten" wiederverwendet, baut genau die Verwechslung
# ein, die diese Anzeige verhindern soll.
GRUPPE_ECHT = "nur_echte_trades"
GRUPPE_ALLE = "alle"

GRUPPEN_TITEL = {
    GRUPPE_ECHT: "Nur echte Trades",
    GRUPPE_ALLE: "Alle Bots (teils Backtest)",
}


class RechnungLaeuft(Exception):
    """Eine andere Rechnung ist gerade unterwegs."""


def _jetzt_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _portfolio_overview():
    """Das gepruefte Rechenmodul aus shared/ - importiert, nicht nachgebaut.

    shared/ ist gemeinsame Infrastruktur, kein Bot-Ordner: hier gibt es die
    Namenskollision nicht, die einen Import von Bot-Dateien verbietet.
    """
    shared = os.path.join(BASE_DIR, "shared")
    if shared not in sys.path:
        sys.path.insert(0, shared)
    import portfolio_overview                                  # noqa: PLC0415
    return portfolio_overview


def _anzeigename(name: str) -> str:
    """Anzeigename aus monitor.py - der einzigen maschinenlesbaren Quelle des
    Projekts. portfolio_overview hat eine eigene, nur vierstellige
    DISPLAY_NAMES-Tabelle; die zu benutzen hiesse, im Dashboard andere
    Bot-Namen zu zeigen als auf jeder anderen Seite."""
    notifications = os.path.join(BASE_DIR, "notifications")
    if notifications not in sys.path:
        sys.path.insert(0, notifications)
    try:
        import monitor                                         # noqa: PLC0415
        return monitor.DISPLAY_NAMES.get(name, name)
    except Exception:                                          # noqa: BLE001
        return name


# ---------------------------------------------------------------------------
def _kennzahlen(po, curves: dict) -> dict:
    """Kombiniert die Kapitalkurven einer Gruppe - dieselbe Rechnung wie
    `run_analysis()` Teil 1 und 2, nur mit Rueckgabewert statt `print`.

    Gleiches Vorgehen heisst hier wirklich gleiches Vorgehen: gemeinsames
    Fenster als Schnittmenge aller Kurven, taeglich aufgefuellt, jede Kurve
    auf 100 normiert, Gewichte aus `resolve_weights`, Portfolio als
    gewichtete Summe. Der Selbsttest vergleicht das Ergebnis mit der
    Textausgabe von `portfolio_overview.py` - driftet eine der beiden
    Rechnungen, faellt es auf.
    """
    import pandas as pd                                        # noqa: PLC0415

    if not curves:
        return {"moeglich": False, "grund": "keine Bots mit Kurve in dieser Gruppe",
                "anzahl_bots": 0, "bots": []}

    beginn = max(d["series"].index.min() for d in curves.values())
    ende = min(d["series"].index.max() for d in curves.values())
    if beginn >= ende:
        return {"moeglich": False,
                "grund": "kein gemeinsames Zeitfenster - die Kurven ueberlappen nicht",
                "anzahl_bots": len(curves), "bots": sorted(curves)}

    tage = pd.date_range(beginn, ende, freq="D")
    gefuellt = {n: d["series"].reindex(tage).ffill().bfill() for n, d in curves.items()}
    normiert = pd.DataFrame({n: s / s.iloc[0] * 100 for n, s in gefuellt.items()})
    gewichte = po.resolve_weights(list(curves.keys()))

    je_bot = []
    for name in curves:
        rendite = round((normiert[name].iloc[-1] / normiert[name].iloc[0] - 1) * 100, 2)
        je_bot.append({
            "name": name,
            "gewicht_pct": round(gewichte[name] * 100, 1),
            "rendite_pct": rendite,
            "max_drawdown_pct": po.max_drawdown_pct(normiert[name]),
            # Beitrag in PROZENTPUNKTEN: Gewicht mal Rendite. Bewusst eine
            # eigene Einheit und nicht "Rendite", damit die Spalten nicht
            # verwechselt werden.
            "beitrag_pp": round(gewichte[name] * rendite, 2),
        })

    portfolio = sum(normiert[n] * gewichte[n] for n in curves)
    kurve = portfolio / portfolio.iloc[0] * 100
    schlechtester = min(b["max_drawdown_pct"] for b in je_bot)

    return {
        "moeglich": True,
        "grund": None,
        "anzahl_bots": len(curves),
        "bots": sorted(curves),
        "von": beginn.date().isoformat(),
        "bis": ende.date().isoformat(),
        "tage": int(len(tage)),
        "rendite_pct": round((kurve.iloc[-1] / kurve.iloc[0] - 1) * 100, 2),
        "max_drawdown_pct": po.max_drawdown_pct(kurve),
        "schlechtester_einzel_drawdown_pct": schlechtester,
        "je_bot": je_bot,
    }


def _offene_positionen() -> dict:
    """Offene Positionen ueber alle Bots - aus derselben Quelle wie die
    Uebersichtsseite, damit beide Seiten nicht verschiedene Zahlen zeigen."""
    if _DASHBOARD_DIR not in sys.path:
        sys.path.insert(0, _DASHBOARD_DIR)
    try:
        import datenquelle                                     # noqa: PLC0415
        uebersicht = datenquelle.portfolio_uebersicht()
        return {"gesamt": uebersicht["summe"]["offene_positionen"],
                "je_bot": {z["name"]: z["offene_positionen"]
                           for z in uebersicht["bots"]},
                "fehler": None}
    except Exception as fehler:                                # noqa: BLE001
        # Darf die Portfolio-Zahl nicht verhindern: die offenen Positionen
        # sind eine Zusatzangabe, keine Voraussetzung.
        return {"gesamt": None, "je_bot": {}, "fehler": str(fehler)}


def berechne() -> dict:
    """Rechnet die Portfolio-Sicht und gibt sie als JSON-taugliches dict
    zurueck. Schreibt nichts - das macht `schreibe_snapshot`."""
    t0 = time.perf_counter()
    po = _portfolio_overview()

    os.makedirs(ARBEITSORDNER, exist_ok=True)
    urspruenglich = po.RESULTS_DIR
    po.RESULTS_DIR = ARBEITSORDNER          # siehe Modulkopf: Kollisionsschutz
    try:
        bots = po.discover_bots()
        curves = po.load_all_curves(bots)
    finally:
        po.RESULTS_DIR = urspruenglich

    offen = _offene_positionen()

    zeilen = []
    for name in sorted(bots):
        quellen = bots[name]
        anzahl = quellen.get("live_closed_trades", 0)
        if name not in curves:
            quelle = QUELLE_FEHLT
            quelle_text = ("keine verwertbare Kurve - dieser Bot ist in KEINER "
                           "der Summen unten enthalten")
        elif quellen.get("using_live_data"):
            quelle = QUELLE_LIVE
            quelle_text = f"Live-Datenbank, {anzahl} geschlossene Trades"
        else:
            quelle = QUELLE_BACKTEST
            quelle_text = (f"Backtest-Kurve, erst {anzahl} von "
                           f"{po.MIN_LIVE_CLOSED_TRADES} Live-Trades")
        zeilen.append({
            "name": name,
            "anzeigename": _anzeigename(name),
            "quelle": quelle,
            "quelle_text": quelle_text,
            "quelle_roh": curves.get(name, {}).get("source"),
            "geschlossene_trades": anzahl,
            "fehlt_bis_schwelle": (max(po.MIN_LIVE_CLOSED_TRADES - anzahl, 0)
                                   if quelle == QUELLE_BACKTEST else None),
            "ist_live_bot": bool(quellen.get("is_live")),
            "grundlage_in_ueberarbeitung": quellen.get("basis_under_review"),
            "offene_positionen": offen["je_bot"].get(name),
        })

    aus_echten_trades = {n: d for n, d in curves.items()
                         if bots[n].get("using_live_data")}
    gruppen = {
        GRUPPE_ECHT: _kennzahlen(po, aus_echten_trades),
        GRUPPE_ALLE: _kennzahlen(po, curves),
    }
    for schluessel, gruppe in gruppen.items():
        gruppe["titel"] = GRUPPEN_TITEL[schluessel]
        gruppe["nur_echte_daten"] = (schluessel == GRUPPE_ECHT)
        gruppe["enthaelt_backtest"] = bool(
            [n for n in gruppe.get("bots", []) if not bots[n].get("using_live_data")])

    return {
        "berechnet_am": _jetzt_iso(),
        "dauer_sekunden": round(time.perf_counter() - t0, 2),
        "schwelle": po.MIN_LIVE_CLOSED_TRADES,
        "startkapital": po.STARTING_CAPITAL,
        "bots": zeilen,
        "gruppen": gruppen,
        "offene_positionen": offen["gesamt"],
        "offene_positionen_fehler": offen["fehler"],
        "anzahl_live_quellen": sum(1 for z in zeilen if z["quelle"] == QUELLE_LIVE),
        "anzahl_backtest_quellen": sum(1 for z in zeilen if z["quelle"] == QUELLE_BACKTEST),
        "anzahl_fehlt": sum(1 for z in zeilen if z["quelle"] == QUELLE_FEHLT),
    }


# ---------------------------------------------------------------------------
def _sperre_nehmen():
    """Verhindert zwei gleichzeitige Rechnungen. O_EXCL statt "existiert
    die Datei?" - eine Pruefung mit anschliessendem Anlegen hat genau die
    Luecke, um die es hier geht."""
    os.makedirs(os.path.dirname(SPERRDATEI), exist_ok=True)
    try:
        fd = os.open(SPERRDATEI, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            alter = time.time() - os.path.getmtime(SPERRDATEI)
        except OSError:
            alter = 0
        if alter < SPERRE_GUELTIG_SEKUNDEN:
            raise RechnungLaeuft(
                f"Es laeuft bereits eine Berechnung (seit {int(alter)} s).")
        os.remove(SPERRDATEI)
        fd = os.open(SPERRDATEI, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(fd, f"{os.getpid()} {_jetzt_iso()}\n".encode())
    os.close(fd)


def _sperre_freigeben():
    try:
        os.remove(SPERRDATEI)
    except OSError:
        pass


def schreibe_snapshot(daten: dict) -> str:
    """Schreibt den Zwischenspeicher atomar: erst eine Nebendatei, dann
    umbenennen. Ein abgebrochener Schreibvorgang hinterlaesst damit den ALTEN
    Stand und keine halbe Datei - die Anzeige wuerde sonst mitten in einer
    Zahl abbrechen."""
    os.makedirs(os.path.dirname(SNAPSHOT_DATEI), exist_ok=True)
    neben = SNAPSHOT_DATEI + ".neu"
    with open(neben, "w", encoding="utf-8") as datei:
        json.dump(daten, datei, ensure_ascii=False, indent=1)
        datei.flush()
        os.fsync(datei.fileno())
    os.replace(neben, SNAPSHOT_DATEI)
    return SNAPSHOT_DATEI


def berechne_und_speichere() -> dict:
    _sperre_nehmen()
    try:
        daten = berechne()
        schreibe_snapshot(daten)
        return daten
    finally:
        _sperre_freigeben()


def lese_snapshot():
    """(daten, alter_sekunden) oder (None, None). Eine unlesbare Datei gilt
    als "nicht vorhanden" statt die Seite zu sprengen."""
    try:
        with open(SNAPSHOT_DATEI, "r", encoding="utf-8") as datei:
            daten = json.load(datei)
        alter = time.time() - os.path.getmtime(SNAPSHOT_DATEI)
        return daten, alter
    except (OSError, ValueError):
        return None, None


def sicht() -> dict:
    """Was die Oberflaeche bekommt. Rechnet NIE - siehe Modulkopf."""
    daten, alter = lese_snapshot()
    if daten is None:
        return {"vorhanden": False,
                "hinweis": ("Noch nicht berechnet. Die Rechnung dauert einige "
                            "Sekunden und laeuft deshalb nicht bei jedem "
                            "Seitenaufruf mit."),
                "laeuft_gerade": os.path.exists(SPERRDATEI)}
    return {"vorhanden": True,
            "alter_sekunden": int(alter),
            "veraltet": alter > MAX_ALTER_SEKUNDEN,
            "max_alter_sekunden": MAX_ALTER_SEKUNDEN,
            "laeuft_gerade": os.path.exists(SPERRDATEI),
            "daten": daten}


# ---------------------------------------------------------------------------
def _zeige(daten: dict) -> None:
    print(f"Berechnet am {daten['berechnet_am']} in {daten['dauer_sekunden']} s")
    print(f"Schwelle fuer die Live-Datenbank: {daten['schwelle']} geschlossene Trades")
    print(f"Quellen: {daten['anzahl_live_quellen']} live, "
          f"{daten['anzahl_backtest_quellen']} Backtest, {daten['anzahl_fehlt']} ohne Kurve")
    print(f"Offene Positionen: {daten['offene_positionen']}")
    print("\nJe Bot:")
    for zeile in daten["bots"]:
        print(f"  {zeile['anzeigename']:38} {zeile['quelle']:9} {zeile['quelle_text']}")
    for schluessel, gruppe in daten["gruppen"].items():
        print(f"\nGruppe {schluessel}:")
        if not gruppe["moeglich"]:
            print(f"  keine Zahl - {gruppe['grund']}")
            continue
        print(f"  {gruppe['anzahl_bots']} Bots, {gruppe['von']} bis {gruppe['bis']}")
        print(f"  Rendite {gruppe['rendite_pct']:+.2f} %   "
              f"max. Drawdown {gruppe['max_drawdown_pct']:.2f} %")


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Portfolio-Sicht des Dashboards: Stand zeigen oder neu berechnen.")
    zerleger.add_argument("--berechnen", action="store_true",
                          help="rechnet neu und schreibt den Zwischenspeicher")
    argumente = zerleger.parse_args(argv)

    if argumente.berechnen:
        try:
            daten = berechne_und_speichere()
        except RechnungLaeuft as fehler:
            print(f"Nichts getan: {fehler}")
            return 1
        print(f"Zwischenspeicher geschrieben: {SNAPSHOT_DATEI}\n")
        _zeige(daten)
        return 0

    stand = sicht()
    if not stand["vorhanden"]:
        print(stand["hinweis"])
        print("Mit --berechnen einmal rechnen lassen.")
        return 0
    print(f"Stand ist {stand['alter_sekunden'] // 60} Minuten alt"
          f"{' - VERALTET' if stand['veraltet'] else ''}\n")
    _zeige(stand["daten"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
