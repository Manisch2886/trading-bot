"""
Selbsttests der Portfolio-Sicht
==============================================================================
Geprueft wird das VERHALTEN: was `portfolio_sicht.berechne()` aus einer
Datenlage macht, was die beiden Endpunkte liefern, und was die
Anzeige-Funktionen aus app.js daraus ERZEUGEN.

Die eigentliche Zusicherung dieser Aenderung ist die Kennzeichnung
live/Backtest. Sie wird deshalb an drei Stellen getrennt geprueft:

  * Abschnitt 2 - ob die Daten sie tragen (alle fuenf Datenlagen),
  * Abschnitt 6 - ob die Endpunkte sie durchlassen,
  * test_portfolio_anzeige.js - ob sie in der AUSGABE landet, je Funktion
    einzeln. Eine Suche ueber das ganze Dokument war in PR #62, #66, #67, #73
    und #77 jedes Mal gruen, obwohl eine Ansicht die Angabe nicht zeigte.

Die Datenlagen kommen aus einer Attrappe von `shared/portfolio_overview.py`.
Nur so lassen sich "alle Bots ueber der Schwelle" und "ein Bot ohne
Datenbank" ueberhaupt herstellen - die echten Live-Datenbanken liegen auf dem
Rechner des Nutzers und sind (zu Recht) nicht im Repo. Die RECHNUNG selbst
laeuft dabei echt: _kennzahlen() benutzt pandas wie im Original.

Abschnitt 8 schliesst die Luecke, die eine Attrappe offen laesst: er ruft das
ECHTE shared/portfolio_overview.py auf und vergleicht dessen Textausgabe Zahl
fuer Zahl mit dem, was dieses Modul berechnet.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:  python3 dashboard/test_portfolio_sicht.py
"""

import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)
sys.path.insert(0, _DIR)
# Die Attrappe unten benutzt absichtlich die ECHTEN Rechenfunktionen aus
# shared/ - ersetzt werden soll die Datenlage, nicht die Mathematik.
sys.path.insert(0, os.path.join(BASE_DIR, "shared"))

import pandas as pd                                            # noqa: E402

import portfolio_sicht as ps                                   # noqa: E402

TEST_TOKEN = "test-token-portfolio"

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        FEHLER.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


# ---------------------------------------------------------------------------
def _kurve(startwert=100.0, tage=400, steigung=0.05, beginn="2025-01-01"):
    """Eine Kapitalkurve wie portfolio_overview sie liefert: taeglicher
    Index, Kapital als Wert."""
    index = pd.date_range(beginn, periods=tage, freq="D")
    werte = [startwert * (1 + steigung * i / tage) for i in range(tage)]
    return pd.Series(werte, index=index)


class Attrappe:
    """Ein Ersatz fuer shared/portfolio_overview mit vorgegebener Datenlage.

    Enthaelt ABSICHTLICH die echten Rechenfunktionen (resolve_weights,
    max_drawdown_pct) - es soll die DATENLAGE ersetzt werden, nicht die
    Mathematik.
    """

    MIN_LIVE_CLOSED_TRADES = 10
    STARTING_CAPITAL = 10_000.0

    def __init__(self, bots, curves, results_dir=None):
        self._bots = bots
        self._curves = curves
        self.RESULTS_DIR = results_dir or tempfile.mkdtemp(prefix="ps_attrappe_")
        self.load_all_curves_aufrufe = 0
        self.results_dir_beim_rechnen = None

    def discover_bots(self):
        return {n: dict(d) for n, d in self._bots.items()}

    def load_all_curves(self, bots):
        self.load_all_curves_aufrufe += 1
        self.results_dir_beim_rechnen = self.RESULTS_DIR
        for name, quellen in bots.items():
            vorgabe = self._bots[name]
            quellen["live_closed_trades"] = vorgabe.get("live_closed_trades", 0)
            quellen["using_live_data"] = vorgabe.get("using_live_data", False)
            if vorgabe.get("basis_under_review"):
                quellen["basis_under_review"] = vorgabe["basis_under_review"]
        return {n: dict(d) for n, d in self._curves.items()}

    @staticmethod
    def resolve_weights(namen):
        import portfolio_overview as echt                      # noqa: PLC0415
        return echt.resolve_weights(namen)

    @staticmethod
    def max_drawdown_pct(serie):
        import portfolio_overview as echt                      # noqa: PLC0415
        return echt.max_drawdown_pct(serie)


class MitAttrappe:
    """Setzt _portfolio_overview und _offene_positionen fuer die Dauer eines
    Tests um und stellt danach den Urzustand her."""

    def __init__(self, attrappe, offen=None):
        self.attrappe = attrappe
        self.offen = offen if offen is not None else {
            "gesamt": 0, "je_bot": {}, "fehler": None}

    def __enter__(self):
        self._po = ps._portfolio_overview
        self._offen = ps._offene_positionen
        ps._portfolio_overview = lambda: self.attrappe
        ps._offene_positionen = lambda: self.offen
        return self.attrappe

    def __exit__(self, *_):
        ps._portfolio_overview = self._po
        ps._offene_positionen = self._offen


class EigenerSpeicher:
    """Lenkt Zwischenspeicher, Sperre und Arbeitsordner in einen
    Wegwerf-Ordner - kein Test fasst den echten Stand an."""

    def __enter__(self):
        self.ordner = tempfile.mkdtemp(prefix="ps_speicher_")
        self._alt = (ps.SNAPSHOT_DATEI, ps.SPERRDATEI, ps.ARBEITSORDNER)
        ps.SNAPSHOT_DATEI = os.path.join(self.ordner, "snapshot.json")
        ps.SPERRDATEI = ps.SNAPSHOT_DATEI + ".lock"
        ps.ARBEITSORDNER = os.path.join(self.ordner, "arbeit")
        return self

    def __exit__(self, *_):
        ps.SNAPSHOT_DATEI, ps.SPERRDATEI, ps.ARBEITSORDNER = self._alt
        shutil.rmtree(self.ordner, ignore_errors=True)


def _lage(*eintraege):
    """(bots, curves) aus Kurzbeschreibungen bauen.

    Jeder Eintrag: (name, trades, using_live, hat_kurve, extra)
    """
    bots, curves = {}, {}
    for name, trades, using_live, hat_kurve, extra in eintraege:
        bots[name] = {
            "equity_csv": f"/results/{name}/equity_curve.csv",
            "db_file": f"/paper_trading_{name}.db" if trades is not None else None,
            "is_live": True,
            "live_closed_trades": trades or 0,
            "using_live_data": using_live,
        }
        bots[name].update(extra or {})
        if hat_kurve:
            # Backtest-Kurven steigen hier ABSICHTLICH deutlich steiler als
            # Live-Kurven. Nicht zur Zierde: mit gleichmaessig verteilten
            # Steigungen kommen "nur echte Trades" und "alle Bots" durch
            # Symmetrie auf denselben Mittelwert, und ein Test, der beide
            # vergleicht, kann dann nichts mehr unterscheiden. Genau dieser
            # Fixture-Fehler ist hier zuerst passiert. Nebenbei entspricht es
            # der Wirklichkeit: der Backtest sieht besser aus als der Live-Lauf.
            steigung = 0.04 + 0.01 * len(curves) if using_live else 0.45
            curves[name] = {"series": _kurve(steigung=steigung),
                            "source": "Live-DB" if using_live else "equity_curve.csv"}
    return bots, curves


# ---------------------------------------------------------------------------
def test_grundsatz_kein_botcode():
    print("\n1) Der Projektgrundsatz: kein Bot-Code im Dashboard-Prozess")
    with open(os.path.join(_DIR, "portfolio_sicht.py"), "r", encoding="utf-8") as d:
        quelle = d.read()
    baum = ast.parse(quelle)
    importe = set()
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            importe |= {a.name.split(".")[0] for a in knoten.names}
        elif isinstance(knoten, ast.ImportFrom) and knoten.module:
            importe.add(knoten.module.split(".")[0])
    for verboten in ("equity_simulation", "live_params", "forward_test"):
        check(f"importiert kein {verboten}", verboten not in importe, sorted(importe))
    check("importiert portfolio_overview (die gepruefte Rechnung)",
          "portfolio_overview" in importe, sorted(importe))

    # Die Rechnung MUSS ueber Subprozesse laufen - das ist der einzige Grund,
    # warum ein Aufruf von portfolio_overview zulaessig ist. Faellt der
    # Subprozess dort je weg, gilt diese Begruendung nicht mehr.
    with open(os.path.join(BASE_DIR, "shared", "portfolio_overview.py"),
              "r", encoding="utf-8") as d:
        fremd = d.read()
    check("portfolio_overview startet Bot-Code weiterhin im Subprozess",
          "subprocess.run" in fremd and "cwd=strategy_dir" in fremd)

    # shared/portfolio_overview.py darf nicht umgebaut werden - daran haengt
    # die Montags-Mail. Verglichen mit dem Stand in git, nicht mit einem
    # Gedaechtniswert.
    lauf = subprocess.run(["git", "diff", "--name-only", "origin/main", "--",
                           "shared/portfolio_overview.py"],
                          cwd=BASE_DIR, capture_output=True, text=True)
    check("shared/portfolio_overview.py ist unveraendert",
          lauf.returncode != 0 or not lauf.stdout.strip(),
          lauf.stdout.strip() or "keine Abweichung")


def test_datenlagen():
    print("\n2) Alle fuenf Datenlagen")

    # (a) Alle Bots ueber der Schwelle
    bots, curves = _lage(("a", 25, True, True, None), ("b", 40, True, True, None))
    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves)):
        daten = ps.berechne()
    check("alle ueber der Schwelle: jede Quelle ist 'live'",
          all(z["quelle"] == "live" for z in daten["bots"]),
          [z["quelle"] for z in daten["bots"]])
    check("alle ueber der Schwelle: Gruppe 'nur echte Trades' ist moeglich",
          daten["gruppen"][ps.GRUPPE_ECHT]["moeglich"])
    check("alle ueber der Schwelle: diese Gruppe enthaelt keinen Backtest",
          not daten["gruppen"][ps.GRUPPE_ECHT]["enthaelt_backtest"])
    check("Zaehler stimmt", daten["anzahl_live_quellen"] == 2
          and daten["anzahl_backtest_quellen"] == 0, daten["anzahl_live_quellen"])

    # (b) Alle Bots darunter - der Fall, in dem eine einzelne Zahl luegen wuerde
    bots, curves = _lage(("a", 3, False, True, None), ("b", 0, False, True, None))
    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves)):
        daten = ps.berechne()
    check("alle darunter: jede Quelle ist 'backtest'",
          all(z["quelle"] == "backtest" for z in daten["bots"]))
    check("alle darunter: Gruppe 'nur echte Trades' ist NICHT moeglich",
          not daten["gruppen"][ps.GRUPPE_ECHT]["moeglich"])
    check("alle darunter: mit Begruendung statt stiller Null",
          bool(daten["gruppen"][ps.GRUPPE_ECHT]["grund"]),
          daten["gruppen"][ps.GRUPPE_ECHT]["grund"])
    check("alle darunter: Gruppe 'alle' ist als Backtest gekennzeichnet",
          daten["gruppen"][ps.GRUPPE_ALLE]["enthaelt_backtest"])
    check("je Bot steht, wie weit die Schwelle entfernt ist",
          [z["fehlt_bis_schwelle"] for z in daten["bots"]] == [7, 10],
          [z["fehlt_bis_schwelle"] for z in daten["bots"]])

    # (c) Gemischt - die Lage vom 12.09.2026
    bots, curves = _lage(("a", 25, True, True, None), ("b", 4, False, True, None),
                         ("c", 30, True, True, None))
    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves)):
        daten = ps.berechne()
    echt = daten["gruppen"][ps.GRUPPE_ECHT]
    alle = daten["gruppen"][ps.GRUPPE_ALLE]
    check("gemischt: 'nur echte Trades' enthaelt genau die zwei Live-Bots",
          echt["bots"] == ["a", "c"], echt["bots"])
    check("gemischt: 'alle' enthaelt alle drei", alle["bots"] == ["a", "b", "c"])
    check("gemischt: die Zahl mit Backtest liegt deutlich hoeher als die "
          "aus echten Trades - zwei Zahlen, nicht eine",
          alle["rendite_pct"] > echt["rendite_pct"] + 1.0,
          f"nur echte Trades {echt['rendite_pct']} vs alle {alle['rendite_pct']}")
    check("gemischt: 'alle' ist als teilweise Backtest gekennzeichnet",
          alle["enthaelt_backtest"] and not echt["enthaelt_backtest"])

    # (d) Ein Bot ohne geschlossene Trades
    bots, curves = _lage(("a", 25, True, True, None), ("leer", 0, False, True, None))
    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves)):
        daten = ps.berechne()
    leer = [z for z in daten["bots"] if z["name"] == "leer"][0]
    check("Bot ohne geschlossene Trades: Quelle 'backtest', 0 Trades",
          leer["quelle"] == "backtest" and leer["geschlossene_trades"] == 0)
    check("Bot ohne geschlossene Trades: erscheint trotzdem in der Liste",
          len(daten["bots"]) == 2)

    # (e) Ein Bot ohne Datenbank
    bots, curves = _lage(("a", 25, True, True, None), ("ohnedb", None, False, True, None))
    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves)):
        daten = ps.berechne()
    ohne = [z for z in daten["bots"] if z["name"] == "ohnedb"][0]
    check("Bot ohne Datenbank: Quelle 'backtest', kein Absturz",
          ohne["quelle"] == "backtest", ohne["quelle_text"])


def test_stiller_ausfall():
    print("\n3) Ein Bot, dessen Kurve fehlt, verschwindet NICHT stillschweigend")
    # Genau der Fall, der in der Cloud-Sitzung am 12.09. auftrat: der
    # Live-Subprozess scheiterte (fehlendes Paket), load_all_curves fing das
    # ab, gab eine print-Warnung aus und liess den Bot fallen.
    bots, curves = _lage(("a", 25, True, True, None), ("b", 25, True, True, None),
                         ("kaputt", 25, True, False, None))
    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves)):
        daten = ps.berechne()
    kaputt = [z for z in daten["bots"] if z["name"] == "kaputt"][0]
    check("der ausgefallene Bot steht in der Liste", kaputt is not None)
    check("seine Quelle ist 'fehlt'", kaputt["quelle"] == "fehlt", kaputt["quelle"])
    check("der Text sagt, dass er in KEINER Summe ist",
          "KEINER" in kaputt["quelle_text"], kaputt["quelle_text"])
    check("er ist in keiner Gruppe enthalten",
          "kaputt" not in daten["gruppen"][ps.GRUPPE_ALLE]["bots"]
          and "kaputt" not in daten["gruppen"][ps.GRUPPE_ECHT]["bots"])
    check("die Summe laeuft ueber die uebrigen zwei",
          daten["gruppen"][ps.GRUPPE_ALLE]["anzahl_bots"] == 2)
    check("der Zaehler fuer fehlende Bots stimmt", daten["anzahl_fehlt"] == 1)


def test_kennzahlen_rechnung():
    print("\n4) Die Rechnung selbst")
    # Zwei Kurven mit UNTERSCHIEDLICHEN Zeitraeumen: das gemeinsame Fenster
    # ist die Schnittmenge, nicht die Vereinigung. Ein Bot mit kurzer
    # Historie verkuerzt das Fenster fuer alle - das muss die Anzeige zeigen
    # koennen, also muss es in den Daten stehen.
    kurz = _kurve(tage=40, beginn="2026-01-01")
    lang = _kurve(tage=800, beginn="2024-01-01")
    bots = {"kurz": {"is_live": True, "live_closed_trades": 20, "using_live_data": True},
            "lang": {"is_live": True, "live_closed_trades": 20, "using_live_data": True}}
    curves = {"kurz": {"series": kurz, "source": "Live-DB"},
              "lang": {"series": lang, "source": "Live-DB"}}
    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves)):
        daten = ps.berechne()
    gruppe = daten["gruppen"][ps.GRUPPE_ALLE]
    check("Fensterbeginn ist der SPAETERE der beiden Anfaenge",
          gruppe["von"] == "2026-01-01", gruppe["von"])
    check("Fensterende ist das FRUEHERE der beiden Enden",
          gruppe["bis"] == kurz.index.max().date().isoformat(), gruppe["bis"])
    check("die Tageszahl wird mitgeliefert", gruppe["tage"] == 40, gruppe["tage"])
    check("je Bot steht ein Beitrag in Prozentpunkten",
          all("beitrag_pp" in b for b in gruppe["je_bot"]))
    summe = round(sum(b["beitrag_pp"] for b in gruppe["je_bot"]), 1)
    check("die Beitraege summieren sich auf die Gruppenrendite",
          abs(summe - gruppe["rendite_pct"]) < 0.3,
          f"Summe {summe} vs Rendite {gruppe['rendite_pct']}")

    # Kurven ohne Ueberlappung
    a = _kurve(tage=30, beginn="2024-01-01")
    b = _kurve(tage=30, beginn="2026-01-01")
    with EigenerSpeicher(), MitAttrappe(Attrappe(
            {"a": {"using_live_data": True, "live_closed_trades": 20, "is_live": True},
             "b": {"using_live_data": True, "live_closed_trades": 20, "is_live": True}},
            {"a": {"series": a, "source": "x"}, "b": {"series": b, "source": "x"}})):
        daten = ps.berechne()
    gruppe = daten["gruppen"][ps.GRUPPE_ALLE]
    check("ohne gemeinsames Fenster: keine Zahl, sondern eine Begruendung",
          not gruppe["moeglich"] and "Zeitfenster" in gruppe["grund"],
          gruppe.get("grund"))

    # Ein einzelner Bot ist kein Portfolio - die Zahl gibt es, aber sie muss
    # erkennbar bleiben.
    with EigenerSpeicher(), MitAttrappe(Attrappe(
            {"a": {"using_live_data": True, "live_closed_trades": 20, "is_live": True}},
            {"a": {"series": _kurve(), "source": "x"}})):
        daten = ps.berechne()
    check("ein einzelner Bot: Gruppe hat anzahl_bots == 1",
          daten["gruppen"][ps.GRUPPE_ALLE]["anzahl_bots"] == 1)


def test_zwischenspeicher():
    print("\n5) Zwischenspeicher, Sperre, Alter")
    bots, curves = _lage(("a", 25, True, True, None), ("b", 25, True, True, None))
    with EigenerSpeicher() as speicher, MitAttrappe(Attrappe(bots, curves)) as attrappe:
        stand = ps.sicht()
        check("ohne Zwischenspeicher: vorhanden=False mit Hinweis",
              stand["vorhanden"] is False and bool(stand["hinweis"]))
        check("sicht() rechnet dabei NICHT", attrappe.load_all_curves_aufrufe == 0,
              attrappe.load_all_curves_aufrufe)

        ps.berechne_und_speichere()
        check("nach dem Rechnen liegt der Zwischenspeicher",
              os.path.exists(ps.SNAPSHOT_DATEI))
        check("die Sperre ist wieder weg", not os.path.exists(ps.SPERRDATEI))

        vorher = attrappe.load_all_curves_aufrufe
        stand = ps.sicht()
        check("sicht() liest nur - keine weitere Rechnung",
              attrappe.load_all_curves_aufrufe == vorher, attrappe.load_all_curves_aufrufe)
        check("das Alter wird mitgeliefert", stand["alter_sekunden"] is not None)
        check("frisch = nicht veraltet", stand["veraltet"] is False)

        # Alter kuenstlich hochsetzen
        alt = time.time() - (ps.MAX_ALTER_SEKUNDEN + 60)
        os.utime(ps.SNAPSHOT_DATEI, (alt, alt))
        check("ueber der Altersgrenze: veraltet=True", ps.sicht()["veraltet"] is True)

        # Eine kaputte Datei ist "nicht vorhanden", kein Absturz
        with open(ps.SNAPSHOT_DATEI, "w", encoding="utf-8") as d:
            d.write("{kein json")
        check("unlesbarer Zwischenspeicher gilt als nicht vorhanden",
              ps.sicht()["vorhanden"] is False)

        # Sperre: eine zweite Rechnung laeuft nicht an
        ps._sperre_nehmen()
        try:
            gescheitert = False
            try:
                ps.berechne_und_speichere()
            except ps.RechnungLaeuft:
                gescheitert = True
            check("zwei gleichzeitige Rechnungen: die zweite bricht ab", gescheitert)
            check("sicht() meldet die laufende Rechnung",
                  ps.sicht()["laeuft_gerade"] is True)
        finally:
            ps._sperre_freigeben()

        # Verwaiste Sperre wird nach Ablauf uebernommen
        ps._sperre_nehmen()
        alt = time.time() - (ps.SPERRE_GUELTIG_SEKUNDEN + 10)
        os.utime(ps.SPERRDATEI, (alt, alt))
        try:
            ps.berechne_und_speichere()
            check("verwaiste Sperre wird uebernommen", True)
        except ps.RechnungLaeuft:
            check("verwaiste Sperre wird uebernommen", False)
        finally:
            ps._sperre_freigeben()

        # Atomar: kein halber Stand. Geprueft am VERHALTEN - ein Schreibvorgang
        # bricht mitten drin ab, und danach muss der ALTE Stand noch
        # vollstaendig lesbar sein. "Es liegt keine Nebendatei herum" allein
        # wuerde auch ein direktes Schreiben in die Zieldatei durchlassen,
        # und genau das ist der Fehler, um den es hier geht.
        inhalt = json.load(open(ps.SNAPSHOT_DATEI, encoding="utf-8"))
        check("der geschriebene Stand ist vollstaendiges JSON", "gruppen" in inhalt)
        check("keine Nebendatei liegt herum",
              not os.path.exists(ps.SNAPSHOT_DATEI + ".neu"))

        alter_stand = open(ps.SNAPSHOT_DATEI, encoding="utf-8").read()
        echtes_dump = json.dump

        def dump_bricht_ab(daten, datei, **rest):
            datei.write('{"halb": ')
            datei.flush()
            raise OSError("Schreibvorgang abgebrochen (Test)")

        json.dump = dump_bricht_ab
        try:
            abgebrochen = False
            try:
                ps.schreibe_snapshot({"neu": True})
            except OSError:
                abgebrochen = True
            check("ein abgebrochener Schreibvorgang wird gemeldet", abgebrochen)
        finally:
            json.dump = echtes_dump
        check("der ALTE Stand ist danach unveraendert vollstaendig",
              open(ps.SNAPSHOT_DATEI, encoding="utf-8").read() == alter_stand)
        check("und weiterhin lesbar", ps.sicht()["vorhanden"] is True)

        # Der Arbeitsordner der Rechnung ist ein EIGENER - sonst kollidiert
        # die Rechnung mit der Montags-Mail auf _live_trades_cache.csv.
        check("die Rechnung arbeitet im eigenen Ordner",
              attrappe.results_dir_beim_rechnen == ps.ARBEITSORDNER,
              attrappe.results_dir_beim_rechnen)
        check("RESULTS_DIR ist danach zurueckgesetzt",
              attrappe.RESULTS_DIR != ps.ARBEITSORDNER, attrappe.RESULTS_DIR)
        check("der Wegwerf-Speicher liegt nicht im echten results/",
              speicher.ordner not in os.path.join(BASE_DIR, "results"))


def test_offene_positionen():
    print("\n6) Offene Positionen sind Zusatz, nicht Voraussetzung")
    bots, curves = _lage(("a", 25, True, True, None), ("b", 25, True, True, None))
    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves),
                                        offen={"gesamt": 7, "je_bot": {"a": 5, "b": 2},
                                               "fehler": None}):
        daten = ps.berechne()
    check("die Gesamtzahl wird uebernommen", daten["offene_positionen"] == 7)
    check("je Bot ebenfalls",
          [z["offene_positionen"] for z in daten["bots"]] == [5, 2])

    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves),
                                        offen={"gesamt": None, "je_bot": {},
                                               "fehler": "DB nicht lesbar"}):
        daten = ps.berechne()
    check("faellt die Quelle aus, bleibt die Portfolio-Zahl da",
          daten["gruppen"][ps.GRUPPE_ALLE]["moeglich"])
    check("der Fehler wird benannt statt verschwiegen",
          daten["offene_positionen_fehler"] == "DB nicht lesbar")

    # Die echte Funktion gegen die echten (hier leeren) Datenbanken
    echt = ps._offene_positionen()
    check("die echte Abfrage laeuft ohne Ausnahme",
          isinstance(echt, dict) and "gesamt" in echt, echt.get("fehler"))


# ---------------------------------------------------------------------------
def _freier_port():
    import socket
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Testserver:
    """Derselbe Aufbau wie in test_dashboard.py."""

    def __init__(self, app):
        import uvicorn
        self.port = _freier_port()
        self.basis = f"http://127.0.0.1:{self.port}"
        konfiguration = uvicorn.Config(app, host="127.0.0.1", port=self.port,
                                       log_level="warning", access_log=False)
        self.server = uvicorn.Server(konfiguration)
        self.thread = threading.Thread(target=self.server.run, daemon=True)

    def __enter__(self):
        self.thread.start()
        for _ in range(100):
            if getattr(self.server, "started", False):
                return self
            time.sleep(0.05)
        raise RuntimeError("Testserver ist nicht gestartet")

    def __exit__(self, *_):
        self.server.should_exit = True
        self.thread.join(timeout=10)


def _get(basis, pfad):
    import requests
    return requests.get(basis + pfad, headers={"X-Dashboard-Token": TEST_TOKEN},
                        timeout=60, allow_redirects=False)


def _post(basis, pfad, koerper=None):
    import requests
    return requests.post(basis + pfad, json=koerper or {},
                         headers={"X-Dashboard-Token": TEST_TOKEN},
                         timeout=120, allow_redirects=False)


class ImportBlockiert:
    """Entfernt ein Modul WIRKLICH: ein Finder in sys.meta_path laesst den
    Import scheitern. Eine Attrappe wuerde nur behaupten, dass der Fall
    behandelt ist."""

    def __init__(self, name):
        self.name = name

    def find_module(self, fullname, path=None):
        return self if fullname == self.name else None

    def find_spec(self, fullname, path=None, target=None):
        if fullname == self.name:
            raise ImportError(f"{fullname} ist fuer diesen Test blockiert")
        return None

    def __enter__(self):
        sys.modules.pop(self.name, None)
        sys.meta_path.insert(0, self)
        return self

    def __exit__(self, *_):
        sys.meta_path.remove(self)
        sys.modules.pop(self.name, None)


def test_endpunkte():
    print("\n7) Die beiden Endpunkte")
    import app as dashboard_app
    anwendung = dashboard_app.erzeuge_app(TEST_TOKEN)
    bots, curves = _lage(("a", 25, True, True, None), ("b", 3, False, True, None))

    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves)) as attrappe:
        with Testserver(anwendung) as server:
            antwort = _get(server.basis, "/api/portfolio-sicht")
            check("GET liefert 200, auch ohne Zwischenspeicher",
                  antwort.status_code == 200, antwort.status_code)
            check("GET meldet 'noch nicht vorhanden'",
                  antwort.json()["vorhanden"] is False)
            check("GET rechnet NICHT - kein Aufruf von load_all_curves",
                  attrappe.load_all_curves_aufrufe == 0,
                  attrappe.load_all_curves_aufrufe)

            antwort = _post(server.basis, "/api/portfolio-sicht/berechnen")
            check("POST rechnet und liefert 200", antwort.status_code == 200,
                  antwort.text[:200])
            check("POST hat genau einmal gerechnet",
                  attrappe.load_all_curves_aufrufe == 1,
                  attrappe.load_all_curves_aufrufe)

            antwort = _get(server.basis, "/api/portfolio-sicht")
            daten = antwort.json()
            check("GET liefert danach den Stand", daten["vorhanden"] is True)
            check("die Quellen kommen bis zur Schnittstelle durch",
                  sorted(z["quelle"] for z in daten["daten"]["bots"])
                  == ["backtest", "live"],
                  [z["quelle"] for z in daten["daten"]["bots"]])
            check("beide Gruppen sind enthalten",
                  set(daten["daten"]["gruppen"]) == {ps.GRUPPE_ECHT, ps.GRUPPE_ALLE})
            check("GET rechnet weiterhin nicht nach",
                  attrappe.load_all_curves_aufrufe == 1)

            # Sperre: der zweite POST bekommt 409, nicht 500
            ps._sperre_nehmen()
            try:
                antwort = _post(server.basis, "/api/portfolio-sicht/berechnen")
                check("POST bei laufender Rechnung: 409 (Zustand, kein Fehler)",
                      antwort.status_code == 409, antwort.status_code)
            finally:
                ps._sperre_freigeben()

            antwort = _get(server.basis, "/portfolio")
            check("die Seite /portfolio wird ausgeliefert",
                  antwort.status_code == 200 and "Portfolio" in antwort.text,
                  antwort.status_code)

            antwort = _get(server.basis, "/")
            check("die Uebersicht verlinkt die Portfolio-Sicht",
                  'href="/portfolio"' in antwort.text)

    # Ohne Token bleibt alles verschlossen - der neue Endpunkt darf keine
    # Ausnahme sein.
    with EigenerSpeicher(), MitAttrappe(Attrappe(bots, curves)):
        with Testserver(anwendung) as server:
            import requests
            for pfad, methode in (("/api/portfolio-sicht", requests.get),
                                  ("/api/portfolio-sicht/berechnen", requests.post),
                                  ("/portfolio", requests.get)):
                antwort = methode(server.basis + pfad, timeout=30,
                                  allow_redirects=False)
                check(f"ohne Token kein Zugriff auf {pfad}",
                      antwort.status_code in (302, 303, 401, 403),
                      antwort.status_code)


def test_notfallweg():
    print("\n8) Der Notfallweg bleibt frei - mit wirklich entfernter Abhaengigkeit")
    import app as dashboard_app

    # (a) Der Import von portfolio_sicht in app.py darf das Dashboard nicht
    #     mitreissen koennen. Deshalb muss das Modul auf Modulebene NUR
    #     Standardbibliothek importieren - pandas und portfolio_overview erst
    #     innerhalb der Funktionen.
    with open(os.path.join(_DIR, "portfolio_sicht.py"), "r", encoding="utf-8") as d:
        baum = ast.parse(d.read())
    oben = set()
    for knoten in baum.body:
        if isinstance(knoten, ast.Import):
            oben |= {a.name.split(".")[0] for a in knoten.names}
        elif isinstance(knoten, ast.ImportFrom) and knoten.module:
            oben.add(knoten.module.split(".")[0])
    erlaubt = {"argparse", "json", "os", "sys", "time", "datetime"}
    check("auf Modulebene nur Standardbibliothek - ein fehlendes pandas kann "
          "das Dashboard nicht am Start hindern",
          oben <= erlaubt, sorted(oben))

    # (b) portfolio_overview wirklich blockieren: die Rechnung muss scheitern,
    #     die Uebersicht und der Crash-Weg muessen weiterlaufen.
    anwendung = dashboard_app.erzeuge_app(TEST_TOKEN)
    with EigenerSpeicher():
        with ImportBlockiert("portfolio_overview"):
            with Testserver(anwendung) as server:
                antwort = _post(server.basis, "/api/portfolio-sicht/berechnen")
                check("bei blockierter Abhaengigkeit: POST meldet 503",
                      antwort.status_code == 503, antwort.status_code)
                antwort = _get(server.basis, "/api/portfolio-sicht")
                check("GET bleibt trotzdem beantwortbar",
                      antwort.status_code == 200, antwort.status_code)
                antwort = _get(server.basis, "/")
                check("die Uebersichtsseite laedt weiter",
                      antwort.status_code == 200, antwort.status_code)
                antwort = _get(server.basis, "/api/portfolio")
                check("die Bot-Uebersicht antwortet weiter",
                      antwort.status_code == 200, antwort.status_code)
                antwort = _post(server.basis,
                                "/api/alle-bots-schliessen/vorbereiten")
                check("der Crash-Weg antwortet weiter (kein 500)",
                      antwort.status_code in (200, 409), antwort.status_code)

    # (c) Auch eine Ausnahme im Lesen darf die Seite nicht mitnehmen.
    alt = ps.sicht
    ps.sicht = lambda: (_ for _ in ()).throw(RuntimeError("kaputt"))
    try:
        with Testserver(anwendung) as server:
            antwort = _get(server.basis, "/api/portfolio-sicht")
            check("kaputter Leseweg: 500 nur auf DIESEM Endpunkt",
                  antwort.status_code == 500, antwort.status_code)
            check("die Uebersicht ist davon unberuehrt",
                  _get(server.basis, "/api/portfolio").status_code == 200)
            check("die Uebersichtsseite ebenfalls",
                  _get(server.basis, "/").status_code == 200)
    finally:
        ps.sicht = alt


def test_abgleich_mit_der_quelle():
    print("\n9) Abgleich mit dem echten shared/portfolio_overview.py")
    # Die Attrappe oben kann nur pruefen, was dieses Modul mit einer Datenlage
    # macht - nicht, ob es dieselbe Rechnung wie die gepruefte Quelle anstellt.
    # Hier laeuft beides auf DENSELBEN echten Daten des Repos.
    # Nicht "python3 shared/portfolio_overview.py": dessen main() schreibt
    # seine Kurven-CSVs nach results/portfolio_overview/, und die sind im Repo
    # eingecheckt. Ein Selbsttest, der bei jedem Lauf eine versionierte Datei
    # veraendert, hinterlaesst eine schmutzige Arbeitskopie - genau das ist
    # hier zuerst passiert. Deshalb dasselbe Programm, aber mit umgelenktem
    # Ausgabeordner.
    ausgabe = tempfile.mkdtemp(prefix="ps_abgleich_")
    try:
        lauf = subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.path.insert(0, 'shared');"
             " import portfolio_overview as po;"
             f" po.RESULTS_DIR = {ausgabe!r}; po.main()"],
            cwd=BASE_DIR, capture_output=True, text=True, timeout=900)
    finally:
        shutil.rmtree(ausgabe, ignore_errors=True)
    check("das Original laeuft durch", lauf.returncode == 0, lauf.stderr[-200:])
    if lauf.returncode != 0:
        return

    rendite = drawdown = fenster = None
    for zeile in lauf.stdout.splitlines():
        if "Rendite im Fenster" in zeile and rendite is None:
            rendite = float(zeile.split(":")[1].strip().rstrip("%"))
        elif "Max Drawdown kombiniert" in zeile and drawdown is None:
            drawdown = float(zeile.split(":")[1].strip().rstrip("%"))
        elif "Gemeinsames Vergleichsfenster" in zeile and fenster is None:
            fenster = zeile.split(":", 1)[1].strip()
    check("die Kennzahlen liessen sich aus der Ausgabe lesen",
          None not in (rendite, drawdown, fenster),
          f"{rendite} / {drawdown} / {fenster}")
    if None in (rendite, drawdown, fenster):
        return

    with EigenerSpeicher():
        daten = ps.berechne()
    # Das Original nennt seine erste Gruppe "LIVE-PORTFOLIO", meint damit aber
    # "Bots mit live_params.py". Alle neun haben eine - die Entsprechung hier
    # ist deshalb die Gruppe "alle", nicht "nur echte Trades". Genau diese
    # Doppelbedeutung von "live" ist der Grund fuer die Umbenennung.
    gruppe = daten["gruppen"][ps.GRUPPE_ALLE]
    check(f"Rendite stimmt mit der Quelle ueberein ({rendite} %)",
          abs(gruppe["rendite_pct"] - rendite) < 0.01,
          f"eigene {gruppe['rendite_pct']} vs Quelle {rendite}")
    check(f"max. Drawdown stimmt ueberein ({drawdown} %)",
          abs(gruppe["max_drawdown_pct"] - drawdown) < 0.01,
          f"eigene {gruppe['max_drawdown_pct']} vs Quelle {drawdown}")
    check("das gemeinsame Fenster stimmt ueberein",
          fenster == f"{gruppe['von']} bis {gruppe['bis']}",
          f"eigene {gruppe['von']} bis {gruppe['bis']} vs Quelle {fenster}")


def test_frontend():
    print("\n10) Die Anzeige (node)")
    if not shutil.which("node"):
        check("node vorhanden - Frontend-Pruefungen werden SONST UEBERSPRUNGEN",
              False, "node fehlt: die 40+ Pruefungen in test_portfolio_anzeige.js "
                     "laufen nicht. Das ist kein gruenes Ergebnis, sondern ein "
                     "fehlendes.")
        return
    skript = os.path.join(_DIR, "test_portfolio_anzeige.js")
    lauf = subprocess.run(["node", skript], capture_output=True, text=True, timeout=180)
    for zeile in lauf.stdout.splitlines():
        if zeile.strip().startswith("[OK ]") or zeile.strip().startswith("[FEHLER]"):
            print("  " + zeile.strip())
    check("Verhaltenstest der Portfolio-Anzeige (test_portfolio_anzeige.js)",
          lauf.returncode == 0, lauf.stdout.splitlines()[-1] if lauf.stdout else lauf.stderr[-200:])


def main():
    print("=" * 78)
    print("Selbsttests der Portfolio-Sicht")
    print("=" * 78)
    tests = [test_grundsatz_kein_botcode, test_datenlagen, test_stiller_ausfall,
             test_kennzahlen_rechnung, test_zwischenspeicher,
             test_offene_positionen, test_endpunkte, test_notfallweg,
             test_abgleich_mit_der_quelle, test_frontend]
    for test in tests:
        try:
            test()
        except Exception as fehler:                            # noqa: BLE001
            import traceback
            FEHLER.append(f"{test.__name__} (Ausnahme)")
            print(f"  [FEHLER] {test.__name__} warf eine Ausnahme: {fehler}")
            traceback.print_exc()

    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print(f"{BESTANDEN} von {gesamt} Pruefungen bestanden, {len(FEHLER)} fehlgeschlagen.")
    for name in FEHLER:
        print(f"  - {name}")
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
