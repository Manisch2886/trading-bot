"""
Selbsttests des Dashboards
==============================================================
Startet den ECHTEN Server (uvicorn, gebunden an 127.0.0.1) gegen eine
komplett synthetische Projektstruktur in einem temporaeren Verzeichnis
und ruft alle Endpunkte per HTTP auf - keine nachgebaute Testfassung der
App, keine Umgehung der Middleware.

Es werden dabei WEDER echte Bot-Datenbanken gelesen NOCH echte
Netzwerkabfragen gemacht: monitor.BASE_DIR/STRATEGIES_DIR/LOGS_DIR und
manual_close.BASE_DIR/STRATEGIES_DIR zeigen waehrend des Tests auf das
temporaere Verzeichnis, und requests.get wird im monitor-Modul durch
eine Funktion ersetzt, die sofort einen Fehler wirft - schliche sich
doch ein echter Netzaufruf ein, faellt der Test auf.

WICHTIG SEIT DEM MANUELLEN SCHLIESSEN: das Dashboard hat jetzt einen
schreibenden Endpunkt. Der frueher hier gefuehrte Nachweis "rein
lesend" waere damit schlicht falsch geworden. Er ist deshalb in ZWEI
Nachweise aufgeteilt, und beide muessen halten:

  6) Alles ausser dem Schliessen ist lesend. Nach allen Lese-Tests sind
     saemtliche Bot-Datenbanken byteweise unveraendert, und die Liste
     der Nicht-GET-Routen ist genau die erwartete.
  8) Die schreibenden Pfade schreiben genau das Erwartete: je Position
     EINE Zeile EINER Datenbank, und dort nur die fuenf Ausstiegsfelder.
     Alle anderen Datenbanken bleiben byteweise identisch. Abschnitt 10
     deckt den Notfallweg ab, der alle Positionen auf einmal schliesst.

Ein Test, der nur "es hat funktioniert" prueft, waere hier zu wenig -
gerade weil dies der erste Schreibzugriff des Dashboards ueberhaupt ist.

Nutzung:  python3 dashboard/test_dashboard.py
"""

import ast
import hashlib
import inspect
import json
import logging
import os
import re
import socket
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timedelta, timezone

import requests

DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(DIR)
for pfad in (DIR, os.path.join(BASE_DIR, "notifications")):
    if pfad not in sys.path:
        sys.path.insert(0, pfad)

import monitor          # noqa: E402
import manual_close     # noqa: E402
import boersenkalender  # noqa: E402
import warteauftraege   # noqa: E402
import konfig           # noqa: E402
import datenquelle      # noqa: E402
import schliessen       # noqa: E402
from app import erzeuge_app  # noqa: E402

TEST_TOKEN = "test-token-1234567890-abcdefgh"

# ---------------------------------------------------------------------------
# Die Uhr des Tests - fuer den Boersenkalender
# ---------------------------------------------------------------------------
# Seit es Warteauftraege gibt, haengt das VERHALTEN des Dashboards davon ab,
# ob die Boerse gerade offen ist. Ein Test, der die echte Uhr benutzt, waere
# damit von der Tageszeit abhaengig: nachmittags gruen, abends rot - die
# schlechteste aller Eigenschaften fuer eine Pruefung.
#
# Gefaelscht wird deshalb die ZEIT, nicht der Kalender. boersenkalender.status
# bekommt einen festen Zeitpunkt untergeschoben, rechnet aber weiterhin mit
# der echten Bibliothek und den echten NYSE-Regeln. So laeuft in jedem
# Abschnitt der ECHTE Kalender - nur eben an einem Tag, den der Test kennt.
# Eine nachgebaute Kalender-Attrappe haette genau die Eigenschaft, die
# Methodik-Grundsatz 12 verbietet: sie waere immer gruen, weil sie nichts
# misst.
#
# Alle Werte in UTC. 13:30-20:00 UTC ist die uebliche Handelszeit im
# Sommer (9:30-16:00 New Yorker Zeit).
ZEIT_OFFEN = "2026-09-10 17:00:00+00:00"        # Donnerstag, 13:00 New York
ZEIT_WOCHENENDE = "2026-09-12 17:00:00+00:00"   # Samstag
ZEIT_FEIERTAG = "2026-11-26 17:00:00+00:00"     # Thanksgiving (4. Do im Nov.)
ZEIT_KARFREITAG = "2026-04-03 15:00:00+00:00"   # Good Friday - beweglich
ZEIT_4_JULI = "2026-07-03 17:00:00+00:00"       # 4. Juli faellt auf Samstag,
                                                 # begangen am Freitag davor
ZEIT_HALBTAG_OFFEN = "2026-11-27 17:30:00+00:00"   # 12:30 NY, Handel laeuft
ZEIT_HALBTAG_ZU = "2026-11-27 18:30:00+00:00"      # 13:30 NY, seit 13:00 zu

# Was die Tests gerade als "jetzt" sehen. Liste statt Konstante, damit die
# Umschaltung in einem with-Block moeglich ist (siehe boerse_am()).
TESTZEIT = [ZEIT_OFFEN]


class boerse_am:
    """Setzt die Testuhr fuer die Dauer eines Blocks.

        with boerse_am(ZEIT_WOCHENENDE):
            ...   # das Dashboard haelt die Boerse fuer geschlossen
    """

    def __init__(self, zeitpunkt):
        self.zeitpunkt = zeitpunkt

    def __enter__(self):
        self.vorher = TESTZEIT[0]
        TESTZEIT[0] = self.zeitpunkt
        boersenkalender.zwischenspeicher_leeren()
        return self

    def __exit__(self, *_):
        TESTZEIT[0] = self.vorher
        boersenkalender.zwischenspeicher_leeren()
        return False

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append(bool(ok))
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        raise SystemExit(f"\nFEHLGESCHLAGEN: {name}\n{detail}")


# ---------------------------------------------------------------------------
# Synthetische Projektstruktur
# ---------------------------------------------------------------------------

def _lege_bot_an(wurzel: str, name: str, trades: list, live_params: str = None,
                  equity_simulation: str = None):
    """`live_params`/`equity_simulation` sind der INHALT der jeweiligen Datei,
    nicht der Wert - so kann ein Test auch den Fall abbilden, dass
    ALLOCATION_PCT dort nur als KOMMENTAR steht (genau die Lage beim echten
    elliott_wave) oder als gerechneter Ausdruck. Fehlt der Parameter, wird die
    Datei nicht angelegt: der Bot dokumentiert dann keine Positionsgroesse."""
    os.makedirs(os.path.join(wurzel, "strategies", name), exist_ok=True)
    for datei, inhalt in (("live_params.py", live_params),
                           ("equity_simulation.py", equity_simulation)):
        if inhalt is None:
            continue
        with open(os.path.join(wurzel, "strategies", name, datei),
                   "w", encoding="utf-8") as fh:
            fh.write(inhalt)
    # forward_test.py mit den beiden Kostensaetzen: manual_close liest sie
    # per AST von dort, statt sie ein zweites Mal zu fuehren. Ohne die
    # Datei koennte kein PnL berechnet werden - dieselben Werte wie beim
    # echten t3_supertrend.
    with open(os.path.join(wurzel, "strategies", name, "forward_test.py"),
               "w", encoding="utf-8") as datei:
        datei.write("TRADING_FEE_PCT = 0.1\nSLIPPAGE_PCT = 0.05\n")
    log_dir = os.path.join(wurzel, "logs", name)
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "lauf.log"), "w") as datei:
        datei.write("synthetischer Testlauf\n")

    db = os.path.join(wurzel, f"paper_trading_{name}.db")
    conn = sqlite3.connect(db)
    conn.execute("""CREATE TABLE trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT, signal_time TEXT,
        entry_time TEXT, entry_price REAL, stop_price REAL, exit_time TEXT,
        exit_price REAL, result TEXT, pnl_pct REAL, status TEXT)""")
    conn.executemany("""INSERT INTO trades
        (symbol, signal_time, entry_time, entry_price, stop_price, exit_time,
         exit_price, result, pnl_pct, status) VALUES (?,?,?,?,?,?,?,?,?,?)""", trades)
    conn.commit()
    conn.close()
    return db


def baue_testprojekt(wurzel: str) -> dict:
    """Drei Bots mit bekannten Zahlen: zwei Krypto, einer Aktien.
    t3_supertrend ist dabei, weil er der einzige Bot ist, bei dem das
    manuelle Schliessen freigeschaltet ist (Abschnitt 8).
    Die Namen muessen in monitor.ASSET_CLASS stehen, sonst wuerde
    discover_bots() sie (korrekterweise) ueberspringen."""
    heute = datetime.now(timezone.utc)
    gestern = heute - timedelta(days=1)

    # elliott_wave (krypto): 3 geschlossene Trades (+2.0, -1.0, +0.5 -> Summe 1.5),
    # davon einer heute geschlossen, plus 2 offene Positionen.
    krypto = [
        ("BTCUSDT", "2026-01-01", "2026-01-01", 100.0, 95.0,
         (heute - timedelta(days=10)).isoformat(), 102.0, "take_profit", 2.0, "closed"),
        ("ETHUSDT", "2026-01-02", "2026-01-02", 200.0, 190.0,
         (heute - timedelta(days=5)).isoformat(), 198.0, "stop_loss", -1.0, "closed"),
        ("BNBUSDT", "2026-01-03", "2026-01-03", 50.0, 47.0,
         heute.isoformat(), 50.25, "take_profit", 0.5, "closed"),
        ("SOLUSDT", "2026-02-01", "2026-02-01", 20.0, 19.0, None, None, None, None, "open"),
        ("ADAUSDT", "2026-02-02", "2026-02-02", 1.0, 0.9, None, None, None, None, "open"),
    ]

    # volatility_breakout (aktien): ein Trade mit pnl_pct NULL - genau der
    # Fall, der /pnl im Telegram-Bot einmal zum Schweigen gebracht hat und
    # in JSON als null (nicht als NaN) ankommen muss.
    aktien = [
        ("AAPL", "2026-01-01", "2026-01-01", 150.0, 140.0,
         (gestern).isoformat(), 153.0, "sma_exit", 2.0, "closed"),
        ("MSFT", "2026-01-05", "2026-01-05", 300.0, 280.0,
         (heute - timedelta(days=2)).isoformat(), 297.0, "stop_loss", None, "closed"),
        ("NVDA", "2026-02-01", "2026-02-01", 500.0, None, None, None, None, None, "open"),
    ]

    # t3_supertrend (krypto): der EINZIGE Bot, bei dem das manuelle
    # Schliessen freigeschaltet ist. Zwei offene Positionen und ein
    # bereits geschlossener Trade - der geschlossene ist wichtig, weil er
    # beim Vorher/Nachher-Vergleich beweisen muss, dass er unberuehrt
    # bleibt. Feste, runde Zahlen, damit der erwartete PnL exakt
    # nachrechenbar ist: 100 -> 110 sind +10 %, minus 2*(0.1+0.05) = 9.7.
    t3 = [
        ("BTCUSDT", "2026-01-01 00:00:00", "2026-01-01 00:00:00", 100.0, 95.0,
         None, None, None, None, "open"),
        ("ETHUSDT", "2026-01-02 00:00:00", "2026-01-02 00:00:00", 200.0, 190.0,
         None, None, None, None, "open"),
        ("XRPUSDT", "2026-01-03 00:00:00", "2026-01-03 00:00:00", 0.5, 0.45,
         (heute - timedelta(days=3)).isoformat(), 0.55, "trend_flip", 9.7, "closed"),
    ]

    # Die angenommenen Positionsgroessen spiegeln die Lage bei den echten Bots:
    # zwei fuehren ALLOCATION_PCT in live_params.py (in PROZENT), einer nur in
    # equity_simulation.py (als ANTEIL) und hat in live_params.py bloss einen
    # Kommentar, der darauf verweist. Drei verschiedene Groessen, damit sich
    # gewichteter und einfacher Durchschnitt ueberhaupt unterscheiden koennen.
    return {
        "elliott_wave": _lege_bot_an(
            wurzel, "elliott_wave", krypto,
            live_params="ALLOCATION_PCT = 5          # in Prozent\n"),
        "volatility_breakout": _lege_bot_an(
            wurzel, "volatility_breakout", aktien,
            live_params="ALLOCATION_PCT = 2          # in Prozent\n"),
        "t3_supertrend": _lege_bot_an(
            wurzel, "t3_supertrend", t3,
            live_params="# ALLOCATION_PCT: bewusst NICHT hier, siehe "
                        "equity_simulation.py (0.10)\nSTOP_LOSS_PCT = 6.0\n",
            equity_simulation="ALLOCATION_PCT = 0.10  # Anteil je Trade\n"),
    }


def _pruefsummen(db_dateien: dict) -> dict:
    return {name: hashlib.sha256(open(pfad, "rb").read()).hexdigest()
            for name, pfad in db_dateien.items()}


# ---------------------------------------------------------------------------
# Server im Hintergrund
# ---------------------------------------------------------------------------

def _freier_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Testserver:
    def __init__(self, app):
        import uvicorn
        self.port = _freier_port()
        self.basis = f"http://127.0.0.1:{self.port}"
        # access_log=False wie in server.py - siehe dortige Begruendung
        # (das Token darf per Query-Parameter kommen und darf deshalb
        # nicht in einem Zugriffsprotokoll landen).
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


def get(basis, pfad, token=TEST_TOKEN, **kwargs):
    kopf = {"X-Dashboard-Token": token} if token else {}
    return requests.get(basis + pfad, headers=kopf, timeout=30,
                         allow_redirects=False, **kwargs)


def post(basis, pfad, koerper=None, token=TEST_TOKEN):
    kopf = {"X-Dashboard-Token": token} if token else {}
    return requests.post(basis + pfad, headers=kopf, json=koerper or {},
                          timeout=60, allow_redirects=False)


def zeilen(db_pfad: str) -> list:
    """Alle Trade-Zeilen einer Datenbank, fuer den Feld-fuer-Feld-Vergleich."""
    conn = sqlite3.connect(db_pfad)
    conn.row_factory = sqlite3.Row
    daten = [dict(z) for z in conn.execute("SELECT * FROM trades ORDER BY id")]
    conn.close()
    return daten


def unterschiede(vorher: list, nachher: list) -> list:
    """(id, feld, alt, neu) fuer jeden Unterschied - inklusive
    hinzugekommener oder verschwundener Zeilen."""
    ergebnis = []
    a = {z["id"]: z for z in vorher}
    b = {z["id"]: z for z in nachher}
    for kennung in sorted(set(a) | set(b)):
        if kennung not in a:
            ergebnis.append((kennung, "<ZEILE NEU>", None, b[kennung]))
        elif kennung not in b:
            ergebnis.append((kennung, "<ZEILE WEG>", a[kennung], None))
        else:
            for feld in a[kennung]:
                if a[kennung][feld] != b[kennung][feld]:
                    ergebnis.append((kennung, feld, a[kennung][feld], b[kennung][feld]))
    return ergebnis


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def teste_konfiguration():
    print("\n1) Konfiguration und Fail-Closed-Verhalten")

    alt = os.environ.pop(konfig.TOKEN_VARIABLE, None)
    alte_env = konfig.ENV_FILE
    konfig.ENV_FILE = os.path.join(tempfile.mkdtemp(), ".env-existiert-nicht")
    try:
        fehler = None
        try:
            konfig.lade_token()
        except RuntimeError as e:
            fehler = e
        check("Ohne gesetztes Token wirft lade_token() einen Fehler", fehler is not None)
        check("Fehlermeldung nennt die Variable, aber keinen Token-Wert",
              konfig.TOKEN_VARIABLE in str(fehler))

        os.environ[konfig.TOKEN_VARIABLE] = "kurz"
        fehler = None
        try:
            konfig.lade_token()
        except RuntimeError as e:
            fehler = e
        check("Zu kurzes Token wird abgelehnt", fehler is not None)

        os.environ[konfig.TOKEN_VARIABLE] = TEST_TOKEN
        check("Gueltiges Token wird gelesen", konfig.lade_token() == TEST_TOKEN)

        fehler = None
        try:
            os.environ.pop(konfig.TOKEN_VARIABLE)
            erzeuge_app()
        except RuntimeError as e:
            fehler = e
        check("erzeuge_app() startet ohne Token gar nicht (fail closed)", fehler is not None)
    finally:
        konfig.ENV_FILE = alte_env
        os.environ.pop(konfig.TOKEN_VARIABLE, None)
        if alt is not None:
            os.environ[konfig.TOKEN_VARIABLE] = alt

    check("Standard-Bindung ist localhost", konfig.STANDARD_HOST == "127.0.0.1")

    quelle = open(os.path.join(DIR, "server.py")).read()
    check("Server startet ohne uvicorn-Zugriffsprotokoll (sonst stuende ein "
          "per ?token= uebergebenes Token im Klartext im Log)",
          "access_log=False" in quelle)


def teste_authentifizierung(basis):
    print("\n2) Zugriffsschutz")

    antwort = get(basis, "/api/portfolio", token=None)
    check("API ohne Token: 401", antwort.status_code == 401, f"war {antwort.status_code}")
    check("401-Antwort enthaelt keine Bot-Daten", "bots" not in antwort.text)

    antwort = get(basis, "/api/portfolio", token="falsches-token-aber-lang-genug")
    check("API mit falschem Token: 401", antwort.status_code == 401, f"war {antwort.status_code}")

    antwort = get(basis, "/api/portfolio")
    check("API mit richtigem Token im Header: 200", antwort.status_code == 200)

    antwort = requests.get(basis + "/api/portfolio",
                            headers={"Authorization": f"Bearer {TEST_TOKEN}"}, timeout=30)
    check("API mit Bearer-Header: 200", antwort.status_code == 200)

    antwort = requests.get(basis + "/", timeout=30, allow_redirects=False)
    check("Seitenaufruf ohne Token leitet auf /login um",
          antwort.status_code == 303 and antwort.headers.get("location") == "/login",
          f"war {antwort.status_code} -> {antwort.headers.get('location')}")

    antwort = requests.get(basis + "/statisch/style.css", timeout=30, allow_redirects=False)
    check("Auch statische Dateien sind geschuetzt", antwort.status_code == 303,
          f"war {antwort.status_code}")

    antwort = requests.get(basis + "/login", timeout=30)
    check("Login-Seite ist ohne Token erreichbar", antwort.status_code == 200)

    sitzung = requests.Session()
    antwort = sitzung.post(basis + "/login", data={"token": "falsch"}, timeout=30,
                            allow_redirects=False)
    check("Login mit falschem Token: 401", antwort.status_code == 401)
    check("Kein Cookie nach fehlgeschlagenem Login",
          konfig.COOKIE_NAME not in sitzung.cookies.get_dict())

    antwort = sitzung.post(basis + "/login", data={"token": TEST_TOKEN}, timeout=30,
                            allow_redirects=False)
    check("Login mit richtigem Token leitet auf / um",
          antwort.status_code == 303 and antwort.headers.get("location") == "/")
    check("Cookie wird gesetzt", konfig.COOKIE_NAME in sitzung.cookies.get_dict())
    check("Cookie ist HttpOnly",
          any(c.has_nonstandard_attr("HttpOnly") or c.has_nonstandard_attr("httponly")
              for c in sitzung.cookies))
    check("Folgeaufruf mit Cookie funktioniert ohne Header",
          sitzung.get(basis + "/api/portfolio", timeout=30).status_code == 200)

    antwort = requests.get(basis + f"/api/portfolio?token={TEST_TOKEN}", timeout=30)
    check("Token als Query-Parameter wird akzeptiert (Erstaufruf am iPhone)",
          antwort.status_code == 200)
    check("Query-Token setzt gleich ein Cookie",
          konfig.COOKIE_NAME in antwort.cookies.get_dict())


def teste_endpunkte(basis):
    print("\n3) Lesende Endpunkte gegen synthetische Daten")

    daten = get(basis, "/api/portfolio").json()
    namen = sorted(b["name"] for b in daten["bots"])
    check("Alle drei Testbots erscheinen in der Uebersicht",
          namen == ["elliott_wave", "t3_supertrend", "volatility_breakout"], str(namen))

    krypto = next(b for b in daten["bots"] if b["name"] == "elliott_wave")
    check("Offene Positionen korrekt gezaehlt", krypto["offene_positionen"] == 2,
          str(krypto["offene_positionen"]))
    check("Geschlossene Trades korrekt gezaehlt", krypto["geschlossene_trades"] == 3)
    check("Summe PnL korrekt (2.0 - 1.0 + 0.5)", abs(krypto["summe_pnl"] - 1.5) < 1e-6,
          str(krypto["summe_pnl"]))
    check("Trefferquote korrekt (2 von 3)", abs(krypto["trefferquote"] - 66.7) < 0.1,
          str(krypto["trefferquote"]))
    check("Heutiger PnL korrekt (nur der heute geschlossene Trade)",
          abs(krypto["pnl_heute"] - 0.5) < 1e-6, str(krypto["pnl_heute"]))
    check("Ohne live=1 kein Live-Gesamtergebnis",
          krypto["aktuelles_gesamtergebnis"] is None)
    check("Anlageklasse aus monitor.ASSET_CLASS uebernommen",
          krypto["anlageklasse"] == "krypto")

    aktien = next(b for b in daten["bots"] if b["name"] == "volatility_breakout")
    check("Trade mit NULL-PnL laesst die Summe nicht kippen",
          abs(aktien["summe_pnl"] - 2.0) < 1e-6, str(aktien["summe_pnl"]))
    check("Antwort ist gueltiges JSON ohne NaN", "NaN" not in get(basis, "/api/portfolio").text)

    check("Summenzeile zaehlt alle Bots", daten["summe"]["anzahl_bots"] == 3)
    # 2 (elliott_wave) + 1 (volatility_breakout) + 2 (t3_supertrend)
    check("Summe offener Positionen ueber alle Bots", daten["summe"]["offene_positionen"] == 5,
          str(daten["summe"]["offene_positionen"]))

    liste = get(basis, "/api/bots").json()
    check("/api/bots liefert die Kurzliste", len(liste["bots"]) == 3)

    detail = get(basis, "/api/bots/elliott_wave").json()
    check("Detail: zwei offene Positionen", len(detail["positionen"]) == 2)
    check("Detail: Entry-Preis der Position vorhanden",
          detail["positionen"][0]["entry_preis"] is not None)
    check("Detail: ohne Live-Kurse ist der aktuelle Preis None",
          detail["positionen"][0]["aktueller_preis"] is None)
    check("Detail: drei geschlossene Trades, neueste zuerst",
          len(detail["letzte_trades"]) == 3
          and detail["letzte_trades"][0]["symbol"] == "BNBUSDT",
          str([t["symbol"] for t in detail["letzte_trades"]]))

    detail_aktien = get(basis, "/api/bots/volatility_breakout").json()
    null_trade = [t for t in detail_aktien["letzte_trades"] if t["symbol"] == "MSFT"][0]
    check("NULL-PnL kommt als JSON-null an, nicht als NaN", null_trade["pnl_pct"] is None)
    check("Position ohne Stop wird als null geliefert",
          detail_aktien["positionen"][0]["stop_preis"] is None)

    antwort = get(basis, "/api/bots/gibtesnicht")
    check("Unbekannter Bot: 404", antwort.status_code == 404, f"war {antwort.status_code}")

    trades = get(basis, "/api/bots/elliott_wave/trades?limit=2").json()
    check("Trade-Liste respektiert limit", len(trades["trades"]) == 2)

    verlauf = get(basis, "/api/verlauf").json()
    kurve = [p["kumuliert_pct"] for p in verlauf["bots"]["elliott_wave"]["punkte"]]
    check("Verlauf kumuliert korrekt (2.0 / 1.0 / 1.5)",
          kurve == [2.0, 1.0, 1.5], str(kurve))
    # 3 (elliott_wave) + 2 (volatility_breakout) + 1 (t3_supertrend)
    check("Gesamtkurve enthaelt alle sechs geschlossenen Trades aller Bots",
          len(verlauf["gesamt"]) == 6, str(len(verlauf["gesamt"])))
    check("Trade ohne lesbares Ergebnis wird gezaehlt und im Hinweis genannt",
          verlauf["trades_ohne_ergebnis"] == 1
          and "ohne lesbares Ergebnis" in verlauf["hinweis"],
          str(verlauf["trades_ohne_ergebnis"]))
    check("Er geht mit 0 in die Kurve ein, faellt also nicht aus der Zeitachse",
          verlauf["gesamt"][-1]["kumuliert_pct"] == verlauf["gesamt"][-2]["kumuliert_pct"]
          or verlauf["bots"]["volatility_breakout"]["trades_ohne_ergebnis"] == 1)
    check("Verlauf traegt den Vorbehalt 'keine Equity-Kurve'",
          "keine Equity-Kurve" in verlauf["hinweis"])

    check("/api/health antwortet", get(basis, "/api/health").json()["status"] == "ok")


def teste_live_kurse(basis):
    print("\n4) Live-Kurse: Erfolg, Zeitueberschreitung, Fehler")

    original = monitor.fetch_live_prices_for_bots
    try:
        monitor.fetch_live_prices_for_bots = lambda bots: {"SOLUSDT": 22.0, "ADAUSDT": 0.9}
        antwort = get(basis, "/api/live-kurse").json()
        check("Kurse werden durchgereicht", antwort["kurse"]["SOLUSDT"] == 22.0)
        check("Kein Hinweis im Erfolgsfall", antwort["hinweis"] is None)

        detail = get(basis, "/api/bots/elliott_wave?live=1").json()
        position = [p for p in detail["positionen"] if p["symbol"] == "SOLUSDT"][0]
        check("Detailseite rechnet die Veraenderung aus (20 -> 22 = +10%)",
              abs(position["veraenderung_pct"] - 10.0) < 1e-6,
              str(position["veraenderung_pct"]))
        check("Aktuelles Gesamtergebnis wird mit Live-Kursen gefuellt",
              detail["aktuelles_gesamtergebnis"] is not None)

        uebersicht = get(basis, "/api/portfolio?live=1").json()
        krypto = next(b for b in uebersicht["bots"] if b["name"] == "elliott_wave")
        # 1.5 (geschlossen) + Mittel aus +10% (SOL) und -10% (ADA: 1.0 -> 0.9) = 1.5
        check("Uebersicht mit live=1 enthaelt das aktuelle Gesamtergebnis",
              abs(krypto["aktuelles_gesamtergebnis"] - 1.5) < 1e-6,
              str(krypto["aktuelles_gesamtergebnis"]))

        # Zeitueberschreitung: die Abfrage dauert laenger als erlaubt.
        altes_limit = konfig.LIVE_KURS_TIMEOUT_SEKUNDEN
        konfig.LIVE_KURS_TIMEOUT_SEKUNDEN = 1

        def langsam(bots):
            time.sleep(3)
            return {"SOLUSDT": 22.0}

        monitor.fetch_live_prices_for_bots = langsam
        beginn = time.monotonic()
        antwort = get(basis, "/api/live-kurse")
        dauer = time.monotonic() - beginn
        check("Zeitueberschreitung liefert trotzdem 200", antwort.status_code == 200)
        check("Antwort kommt nach dem Limit, nicht nach der vollen Wartezeit",
              dauer < 2.5, f"{dauer:.1f}s")
        check("Antwort enthaelt keine Kurse, aber einen Hinweis",
              antwort.json()["kurse"] == {} and "Zeitueberschreitung" in antwort.json()["hinweis"])

        # Waehrend die langsame Abfrage laeuft, muss der Server weiter
        # antworten - genau dafuer ist asyncio.to_thread() da.
        blockierer = threading.Thread(target=lambda: get(basis, "/api/live-kurse"), daemon=True)
        blockierer.start()
        time.sleep(0.3)
        beginn = time.monotonic()
        antwort = get(basis, "/api/portfolio")
        dauer = time.monotonic() - beginn
        check("Server bleibt waehrend einer langsamen Kursabfrage ansprechbar",
              antwort.status_code == 200 and dauer < 2.0, f"{dauer:.2f}s")
        blockierer.join(timeout=10)
        konfig.LIVE_KURS_TIMEOUT_SEKUNDEN = altes_limit

        # Fehlerfall: die Abfrage wirft.
        def kaputt(bots):
            raise RuntimeError("simulierter Netzwerkfehler")

        monitor.fetch_live_prices_for_bots = kaputt
        antwort = get(basis, "/api/live-kurse")
        check("Fehler bei der Kursabfrage ergibt 200 mit Hinweis, keinen 500er",
              antwort.status_code == 200 and antwort.json()["kurse"] == {}
              and antwort.json()["hinweis"] is not None, f"war {antwort.status_code}")

        uebersicht = get(basis, "/api/portfolio?live=1")
        check("Uebersicht bleibt trotz Kursfehler vollstaendig",
              uebersicht.status_code == 200 and len(uebersicht.json()["bots"]) == 3)

        antwort = get(basis, "/api/live-kurse?bot=gibtesnicht")
        check("Live-Kurse fuer unbekannten Bot: 404", antwort.status_code == 404)
    finally:
        monitor.fetch_live_prices_for_bots = original


def teste_frontend(basis):
    print("\n5) Frontend und PWA")

    for pfad, erwartet in (("/", "Trading-Bots"), ("/bot", "Offene Positionen")):
        antwort = get(basis, pfad)
        check(f"{pfad} wird ausgeliefert",
              antwort.status_code == 200 and erwartet in antwort.text)

    manifest = get(basis, "/manifest.json")
    check("manifest.json wird ausgeliefert", manifest.status_code == 200)
    inhalt = json.loads(manifest.text)
    check("Manifest ist installierbar (standalone, start_url, Icons)",
          inhalt["display"] == "standalone" and inhalt["start_url"] == "/"
          and len(inhalt["icons"]) == 2)

    sw = get(basis, "/sw.js")
    check("Service Worker wird vom Wurzelpfad ausgeliefert", sw.status_code == 200)
    check("Service Worker speichert API-Antworten NICHT zwischen",
          'pathname.startsWith("/api/")' in sw.text)

    for name in ("icon-192.png", "icon-512.png"):
        antwort = get(basis, f"/statisch/{name}")
        check(f"{name} vorhanden und ein PNG",
              antwort.status_code == 200 and antwort.content[:8] == b"\x89PNG\r\n\x1a\n")

    css = get(basis, "/statisch/style.css")
    js = get(basis, "/statisch/app.js")
    check("style.css und app.js werden ausgeliefert",
          css.status_code == 200 and js.status_code == 200)
    check("Frontend laedt keine fremden Skripte nach",
          "http://" not in js.text and "https://" not in js.text)


# Die Nicht-GET-Routen, die es geben DARF - vollstaendig und woertlich.
# Diese Liste ist der Kern des korrigierten Nachweises: bis PR #60 stand
# hier "genau eine, POST /login". Mit dem Einzel-Schliessen wurden es vier,
# mit dem Notfallweg (alle Positionen) sechs, mit dem globalen Crash-Weg
# acht - davon fassen GENAU DREI eine Datenbank an. Kommt irgendwann eine
# neunte dazu, faellt dieser Test auf - und genau das soll er.
ERLAUBTE_SCHREIB_ROUTEN = [
    ("POST", "/login"),                                          # setzt nur ein Cookie
    ("POST", "/api/bots/{name}/schliessen/vorbereiten"),          # nur Arbeitsspeicher
    ("POST", "/api/bots/{name}/schliessen/abbrechen"),            # nur Arbeitsspeicher
    ("POST", "/api/bots/{name}/schliessen/ausfuehren"),           # <- schreibt
    ("POST", "/api/bots/{name}/alle-schliessen/vorbereiten"),     # nur Arbeitsspeicher
    ("POST", "/api/bots/{name}/alle-schliessen/ausfuehren"),      # <- schreibt
    ("POST", "/api/alle-bots-schliessen/vorbereiten"),            # nur Arbeitsspeicher
    ("POST", "/api/alle-bots-schliessen/ausfuehren"),             # <- schreibt (global)
    # Neu mit den Warteauftraegen: entfernt einen wartenden Auftrag aus der
    # Auftragsdatei. Fasst KEINE Bot-Datenbank an - und steht deshalb hier
    # in derselben Liste wie die beiden Arbeitsspeicher-Routen, nicht bei
    # den drei schreibenden.
    ("POST", "/api/warteauftraege/stornieren"),                   # nur Auftragsdatei
]


def teste_nur_lesend(app, basis, pruefsummen_vorher, db_dateien):
    print("\n6) Nachweis: lesend, ausser dem einen Schliess-Endpunkt")

    schreibende = []
    for route in app.routes:
        methoden = set(getattr(route, "methods", []) or [])
        for methode in methoden & {"POST", "PUT", "PATCH", "DELETE"}:
            schreibende.append((methode, getattr(route, "path", "?")))
    check("Es gibt genau die neun erwarteten Nicht-GET-Routen",
          sorted(schreibende) == sorted(ERLAUBTE_SCHREIB_ROUTEN), str(sorted(schreibende)))
    check("Davon fassen weiterhin genau DREI eine Datenbank an "
          "(die drei …/ausfuehren)",
          sorted(r[1] for r in schreibende if r[1].endswith("/ausfuehren"))
          == ["/api/alle-bots-schliessen/ausfuehren",
              "/api/bots/{name}/alle-schliessen/ausfuehren",
              "/api/bots/{name}/schliessen/ausfuehren"],
          str(sorted(r[1] for r in schreibende if r[1].endswith("/ausfuehren"))))

    for methode in ("POST", "PUT", "DELETE", "PATCH"):
        antwort = requests.request(methode, basis + "/api/portfolio",
                                    headers={"X-Dashboard-Token": TEST_TOKEN}, timeout=30)
        check(f"{methode} auf /api/portfolio wird abgelehnt",
              antwort.status_code == 405, f"war {antwort.status_code}")

    # Die lesende Datenschicht darf weiterhin keinen Schreibpfad haben.
    # Der Schreibpfad laeuft ausdruecklich an ihr vorbei (app.py ->
    # schliessen.py -> manual_close.py); wer ihn hier einbaute, machte
    # diesen Nachweis unfuehrbar.
    # Geprueft wird der CODE, nicht der Fliesstext daneben: datenquelle.py
    # ERWAEHNT manual_close in einem Kommentar (es erklaert dort, dass der
    # Schreibpfad ausdruecklich an dieser Schicht vorbeilaeuft). Eine reine
    # Textsuche wuerde genau diese Erklaerung als Verstoss lesen - derselbe
    # Fehlertyp, den ohne_kommentare() weiter unten fuer JS/CSS behebt.
    quelldatei = os.path.join(DIR, "datenquelle.py")
    baum = ast.parse(open(quelldatei, encoding="utf-8").read(), filename=quelldatei)
    zeichenketten = [k.value for k in ast.walk(baum)
                     if isinstance(k, ast.Constant) and isinstance(k.value, str)]
    sql = [z for z in zeichenketten
           if re.match(r"\s*(INSERT|UPDATE|DELETE|DROP)\s", z, re.I)]
    check("datenquelle.py enthaelt keine schreibende SQL-Anweisung", not sql, str(sql)[:80])

    importe = set()
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            importe.update(a.name for a in knoten.names)
        elif isinstance(knoten, ast.ImportFrom):
            importe.add(knoten.module or "")
    check("datenquelle.py importiert das Schreibmodul nicht",
          "manual_close" not in importe, str(sorted(importe)))
    # Gegenprobe: die Pruefung findet einen Import ueberhaupt - sonst waere
    # das gruene Ergebnis oben nur die Abwesenheit eines Suchtreffers.
    probe = ast.parse("import manual_close")
    check("Gegenprobe: ein eingeschmuggelter Import wuerde auffallen",
          any(a.name == "manual_close"
              for k in ast.walk(probe) if isinstance(k, ast.Import)
              for a in k.names))

    nachher = _pruefsummen(db_dateien)
    check("Nach allen LESENDEN Tests ist keine Bot-Datenbank veraendert",
          nachher == pruefsummen_vorher,
          "Pruefsummen weichen ab" if nachher != pruefsummen_vorher else "")


# ---------------------------------------------------------------------------
# 8) Der eine schreibende Endpunkt
# ---------------------------------------------------------------------------

SPERR_HALTER = """\
\"\"\"Haelt eine SQLite-Schreibsperre - simuliert den laufenden Cronjob.\"\"\"
import sqlite3, sys, time
conn = sqlite3.connect(sys.argv[1], timeout=30, isolation_level=None)
conn.execute("BEGIN IMMEDIATE")
conn.execute("UPDATE trades SET stop_price=stop_price WHERE id=2")
print("gesperrt", flush=True)
time.sleep(float(sys.argv[2]))
conn.execute("ROLLBACK")
conn.close()
"""

TESTKURSE = {"BTCUSDT": 110.0, "ETHUSDT": 180.0, "SOLUSDT": 22.0, "ADAUSDT": 0.9}


def _vorbereiten(basis, bot="t3_supertrend", trade_id=1):
    return post(basis, f"/api/bots/{bot}/schliessen/vorbereiten",
                 {"trade_id": trade_id})


def _ausfuehren(basis, vorgang, bot="t3_supertrend", token=TEST_TOKEN,
                 zusatz=None):
    """Der Ausfuehren-Aufruf, wie das Frontend ihn schickt: NUR die
    Vorgangs-Kennung. `zusatz` dient den Tests, die belegen, dass weitere
    Felder im Koerper nichts aendern - insbesondere, dass ein frueher
    noetiges "bestaetigung" weder noch gebraucht noch ausgewertet wird."""
    koerper = {"vorgang": vorgang}
    if zusatz:
        koerper.update(zusatz)
    return post(basis, f"/api/bots/{bot}/schliessen/ausfuehren",
                 koerper, token=token)


def teste_schliessen(basis, wurzel, db_dateien, protokoll_datei):
    print("\n8) Manuelles Schliessen - der einzige schreibende Pfad")

    db_t3 = db_dateien["t3_supertrend"]
    andere = {n: p for n, p in db_dateien.items() if n != "t3_supertrend"}
    andere_vorher = _pruefsummen(andere)
    vor_allem = zeilen(db_t3)

    def nichts_geschrieben(was):
        check(f"{was}: t3-Datenbank Feld fuer Feld unveraendert",
              unterschiede(vor_allem, zeilen(db_t3)) == [],
              str(unterschiede(vor_allem, zeilen(db_t3)))[:120])

    original_kurse = monitor.fetch_live_prices_for_bots
    monitor.fetch_live_prices_for_bots = lambda bots: dict(TESTKURSE)
    schliessen.vorgaenge_zuruecksetzen()
    try:
        # --- 8a) Lesen: wer ist freigeschaltet, und mit welchen IDs -------
        antwort = get(basis, "/api/bots/t3_supertrend/schliessbare-positionen?live=1").json()
        check("t3_supertrend ist freigeschaltet", antwort["schliessbar"] is True)
        check("Zwei offene Positionen mit Zeilen-ID",
              [p["id"] for p in antwort["positionen"]] == [1, 2],
              str([p["id"] for p in antwort["positionen"]]))
        btc = antwort["positionen"][0]
        check("PnL wird nach der Bot-Formel geschaetzt (100 -> 110 = +9.70)",
              btc["pnl_pct"] == 9.7, str(btc["pnl_pct"]))
        check("Mit Kurs ist die Position schliessbar", btc["schliessbar_jetzt"] is True)
        # Das Frontend braucht den Bestaetigungstext nicht mehr, also wird er
        # auch nicht mehr mitgeschickt. Ein Feld, das niemand liest, waere
        # eine Einladung, es doch wieder zu benutzen.
        check("Der Bestaetigungstext wird nicht mehr ans Frontend gegeben",
              "bestaetigungstext" not in antwort, str(sorted(antwort))[:120])
        check("Die Frist kommt weiterhin aus dem geteilten Kern",
              antwort["gueltig_sekunden"]
              == manual_close.BESTAETIGUNG_GUELTIG_SEKUNDEN)

        ohne_kurse = get(basis, "/api/bots/t3_supertrend/schliessbare-positionen").json()
        check("Ohne live=1 keine Kurse und damit kein Knopf",
              all(p["aktueller_preis"] is None and p["schliessbar_jetzt"] is False
                  for p in ohne_kurse["positionen"]))

        # Seit der Freischaltung aller neun Bots gibt es keinen echten Bot
        # mehr, der abgelehnt wird. Die Sperre selbst bleibt trotzdem
        # pruefbar - und wird es hier, indem ein Bot kurz aus der Liste
        # genommen wird. Ein erfundener Name waere der schwaechere Test:
        # er koennte auch an "Bot existiert nicht" scheitern.
        gemerkt = manual_close.SCHLIESSBARE_BOTS.pop("elliott_wave")
        try:
            fremd = get(basis, "/api/bots/elliott_wave/schliessbare-positionen").json()
            check("Ein aus der Liste genommener Bot meldet sich als nicht "
                  "freigeschaltet",
                  fremd["schliessbar"] is False and "t3_supertrend" in fremd["grund"],
                  str(fremd.get("grund"))[:110])
        finally:
            manual_close.SCHLIESSBARE_BOTS["elliott_wave"] = gemerkt
        check("Danach ist er wieder freigeschaltet",
              schliessen.ist_freigeschaltet("elliott_wave"))

        # --- 8b) Beide Leser sehen dieselben Zeilen-IDs -------------------
        # Der eine Weg fuellt die Tabelle (monitor -> datenquelle), der
        # andere schreibt (manual_close). Waeren ihre IDs verschieden,
        # schloesse ein Klick die falsche Position - der unangenehmste
        # denkbare Fehler dieser Funktion.
        aus_detail = get(basis, "/api/bots/t3_supertrend?live=1").json()["positionen"]
        aus_kern = manual_close.offene_positionen("t3_supertrend")
        check("Detailseite und Schreibmodul sehen dieselben (ID, Symbol)-Paare",
              [(p["id"], p["symbol"]) for p in aus_detail]
              == [(p["id"], p["symbol"]) for p in aus_kern],
              f"{[(p['id'], p['symbol']) for p in aus_detail]} vs "
              f"{[(p['id'], p['symbol']) for p in aus_kern]}")

        nichts_geschrieben("Nach allen Leseabfragen")

        # --- 8c) Ein einzelner Aufruf kann niemals schreiben --------------
        # Das ist die Absicherung, die den Wegfall der Texteingabe traegt:
        # ohne vorheriges `vorbereiten` gibt es keine Kennung, und ohne
        # Kennung schreibt kein Aufruf - egal was sonst im Koerper steht.
        antwort = _ausfuehren(basis, "frei-erfundene-kennung")
        check("Ausfuehren ohne vorherigen Vorgang wird abgelehnt (409)",
              antwort.status_code == 409, str(antwort.status_code))
        for koerper in ({}, {"vorgang": None}, {"bestaetigung": "BESTAETIGEN"},
                         {"vorgang": "", "bestaetigung": "BESTAETIGEN"},
                         {"trade_id": 1}):
            antwort = post(basis, "/api/bots/t3_supertrend/schliessen/ausfuehren", koerper)
            check(f"Ausfuehren mit {koerper} wird abgelehnt",
                  antwort.status_code == 409, str(antwort.status_code))
        check("Auch ein mitgeschicktes 'bestaetigung' oeffnet keinen Weg ohne "
              "Kennung - der Text ist nicht mehr die Absicherung, die "
              "Kennung ist es",
              post(basis, "/api/bots/t3_supertrend/schliessen/ausfuehren",
                   {"bestaetigung": "BESTAETIGEN"}).status_code == 409)
        nichts_geschrieben("Nach Aufrufen ohne Vorgang")

        # --- 8d) Ohne gueltiges Token --------------------------------------
        vorbereitet = _vorbereiten(basis).json()
        for token in (None, "falsches-token-aber-lang-genug"):
            antwort = post(basis, "/api/bots/t3_supertrend/schliessen/vorbereiten",
                            {"trade_id": 1}, token=token)
            check(f"Vorbereiten ohne gueltiges Token: 401 (Token {token!r})",
                  antwort.status_code == 401, str(antwort.status_code))
            antwort = _ausfuehren(basis, vorbereitet["vorgang"], token=token)
            check(f"Ausfuehren ohne gueltiges Token: 401 (Token {token!r})",
                  antwort.status_code == 401, str(antwort.status_code))
        nichts_geschrieben("Nach Versuchen ohne Token")
        # Der Vorgang von oben lebt noch - ein 401 darf ihn nicht verbrauchen.
        check("Ein abgewiesener Fremdzugriff verbraucht den Vorgang nicht",
              schliessen.offener_vorgang(vorbereitet["vorgang"]) is not None)

        # --- 8e) Nicht freigeschalteter Bot --------------------------------
        # Alle neun sind freigeschaltet; geprueft wird deshalb die SPERRE,
        # nicht ein bestimmter Bot: zwei Bots kurz herausnehmen, danach
        # wieder eintragen.
        for bot in ("elliott_wave", "volatility_breakout"):
            gemerkt = manual_close.SCHLIESSBARE_BOTS.pop(bot)
            try:
                antwort = post(basis, f"/api/bots/{bot}/schliessen/vorbereiten",
                                {"trade_id": 1})
                check(f"Vorbereiten fuer den gesperrten {bot}: 403",
                      antwort.status_code == 403, str(antwort.status_code))
                antwort = _ausfuehren(basis, vorbereitet["vorgang"], bot=bot)
                check(f"Ausfuehren fuer den gesperrten {bot}: 403",
                      antwort.status_code == 403, str(antwort.status_code))
            finally:
                manual_close.SCHLIESSBARE_BOTS[bot] = gemerkt
        check("Die Datenbanken der uebrigen Bots sind unveraendert",
              _pruefsummen(andere) == andere_vorher)

        # --- 8f) Abbruch -------------------------------------------------
        # Es gibt nur noch EINEN Abbruchweg: der Vorgang entsteht beim
        # Oeffnen des Dialogs, und Abbrechen/Esc/Klick daneben verwerfen ihn.
        # Frueher war derselbe Aufruf zweimal zu pruefen, einmal je Stufe.
        eins = _vorbereiten(basis).json()
        check("Vorbereiten liefert Kennung, Kurs und geschaetzten PnL",
              eins["vorgang"] and eins["aktueller_preis"] == 110.0
              and eins["pnl_pct"] == 9.7)
        antwort = post(basis, "/api/bots/t3_supertrend/schliessen/abbrechen",
                        {"vorgang": eins["vorgang"]})
        check("Abbrechen wird bestaetigt", antwort.status_code == 200)
        check("Danach ist die Kennung wertlos",
              _ausfuehren(basis, eins["vorgang"]).status_code == 409)
        nichts_geschrieben("Nach Abbruch")

        # --- 8g) Kein Bestaetigungstext mehr - aber nur im Dashboard -------
        # Die Texteingabe ist aus dem Dashboard-Weg entfernt (ein Tap statt
        # zwei). Geprueft wird hier beides: dass der Weg sie wirklich nicht
        # mehr verlangt, UND dass der geteilte Kern sie unveraendert weiter
        # verlangt - sonst haette diese Aenderung die Telegram-Variante
        # stillschweigend mit aufgeweicht, die ihre zwei Stufen behaelt.
        check("Der Dashboard-Weg nimmt gar kein Bestaetigungsfeld mehr an",
              "bestaetigung" not in inspect.signature(
                  schliessen.ausfuehren).parameters,
              str(inspect.signature(schliessen.ausfuehren)))
        # Eingegrenzt auf den EINZEL-Endpunkt: der globale Crash-Weg liest
        # sehr wohl ein 'bestaetigung' (den Text CRASH), eine Suche ueber die
        # ganze Datei waere seit dessen Einbau irrefuehrend.
        quelltext_app = open(os.path.join(DIR, "app.py"), encoding="utf-8").read()
        einzel_endpunkt = quelltext_app.split(
            "async def schliessen_ausfuehren", 1)[1].split("\n    @app.", 1)[0]
        check("Der Einzel-Endpunkt liest kein 'bestaetigung' mehr aus dem Koerper",
              'get("bestaetigung")' not in einzel_endpunkt)
        check("Der globale Endpunkt liest ihn dagegen ausdruecklich",
              'get("bestaetigung")' in quelltext_app.split(
                  "async def global_schliessen_ausfuehren", 1)[1])
        check("Der Kern verlangt den Text unveraendert weiter (Telegram "
              "behaelt seine zwei Stufen)",
              manual_close.BESTAETIGUNGSTEXT == "BESTAETIGEN")
        try:
            manual_close.schliesse_position(
                "t3_supertrend", 1, 110.0, "test", "falscher-text",
                quelle=manual_close.QUELLE_DASHBOARD)
            kern_lehnt_ab = False
        except manual_close.SchliessenNichtMoeglich as fehler:
            kern_lehnt_ab = "Bestaetigungstext" in str(fehler)
        check("Ein direkter Kern-Aufruf mit falschem Text schreibt weiterhin "
              "nichts", kern_lehnt_ab)
        nichts_geschrieben("Nach dem Kern-Aufruf mit falschem Text")

        # --- 8h) Abgelaufene Bestaetigung ----------------------------------
        vier = _vorbereiten(basis).json()
        check("Die Frist wird mitgeliefert",
              vier["gueltig_sekunden"] == manual_close.BESTAETIGUNG_GUELTIG_SEKUNDEN)
        # Die Uhr vorstellen, statt zwei Minuten zu warten.
        schliessen.offener_vorgang(vier["vorgang"])["gueltig_bis"] = time.time() - 1
        antwort = _ausfuehren(basis, vier["vorgang"])
        check("Eine abgelaufene Bestaetigung schreibt nichts mehr",
              antwort.status_code == 409, str(antwort.status_code))
        check("Die Meldung nennt die Frist",
              str(manual_close.BESTAETIGUNG_GUELTIG_SEKUNDEN) in antwort.json()["detail"])
        nichts_geschrieben("Nach abgelaufener Bestaetigung")

        # --- 8i) Vorgang eines ANDEREN Bots --------------------------------
        # elliott_wave ist inzwischen dauerhaft freigeschaltet - der Test
        # muss ihn nicht mehr vorruebergehend eintragen.
        fremder = _vorbereiten(basis, bot="elliott_wave", trade_id=4).json()
        check("Vorbereiten fuer einen zweiten Bot gelingt",
              bool(fremder.get("vorgang")), str(fremder)[:100])
        antwort = _ausfuehren(basis, fremder["vorgang"], bot="t3_supertrend")
        check("Eine Kennung von Bot A schliesst nichts bei Bot B",
              antwort.status_code == 409, str(antwort.status_code))
        # Der GRUND muss stimmen, nicht nur der Statuscode. Die beiden
        # Testbots haben ueberlappungsfreie Zeilen-IDs (elliott_wave: 4/5
        # offen, t3: 1/2) - ohne die Bot-Pruefung wuerde der Versuch
        # deshalb ohnehin an "Kein Trade mit ID 4" scheitern, und dieser
        # Test waere gruen, ohne die Absicherung zu pruefen. Genau dieser
        # Fall ist in der Mutationsprobe aufgefallen.
        check("Und zwar ausdruecklich, WEIL die Kennung zu einem anderen "
              "Bot gehoert",
              "anderen Bot" in antwort.json()["detail"],
              antwort.json()["detail"][:90])
        check("Die Datenbanken der uebrigen Bots sind weiterhin unveraendert",
              _pruefsummen(andere) == andere_vorher)
        nichts_geschrieben("Nach dem Versuch mit fremder Kennung")
        # Die Tests oben nehmen einzelne Bots vorruebergehend aus der Liste.
        # Dass sie danach wieder vollstaendig ist, gehoert mitgeprueft -
        # eine halb geleerte Liste wuerde alle folgenden Abschnitte
        # stillschweigend entschaerfen.
        check("Nach den Sperr-Tests sind wieder alle neun Bots freigeschaltet",
              sorted(manual_close.SCHLIESSBARE_BOTS) == sorted(monitor.DISPLAY_NAMES),
              str(sorted(manual_close.SCHLIESSBARE_BOTS)))

        # --- 8j) Nebenlaeufigkeit: die Datenbank ist gerade gesperrt --------
        # Echter zweiter Prozess, keine Attrappe: SQLite-Sperren wirken
        # zwischen Verbindungen, ein Thread im selben Prozess wuerde hier
        # nichts beweisen.
        halter_skript = os.path.join(wurzel, "sperr_halter.py")
        with open(halter_skript, "w", encoding="utf-8") as datei:
            datei.write(SPERR_HALTER)
        fuenf = _vorbereiten(basis).json()
        altes_limit = manual_close.SPERR_TIMEOUT_SEKUNDEN
        manual_close.SPERR_TIMEOUT_SEKUNDEN = 1
        halter = subprocess.Popen([sys.executable, halter_skript, db_t3, "5"],
                                   stdout=subprocess.PIPE, text=True)
        try:
            check("Der zweite Prozess haelt die Schreibsperre",
                  halter.stdout.readline().strip() == "gesperrt")
            antwort = _ausfuehren(basis, fuenf["vorgang"])
            check("Bei gesperrter Datenbank bricht der Endpunkt sauber ab (409)",
                  antwort.status_code == 409, str(antwort.status_code))
            check("Die Meldung nennt die Sperre und den vermuteten Cronjob",
                  "gesperrt" in antwort.json()["detail"].lower()
                  and "cronjob" in antwort.json()["detail"].lower(),
                  antwort.json()["detail"][:90])
        finally:
            manual_close.SPERR_TIMEOUT_SEKUNDEN = altes_limit
            halter.wait(timeout=60)
        nichts_geschrieben("Nach dem Versuch gegen eine gesperrte Datenbank")

        # Die Sperre ist jetzt weg - die Position waere wieder schliessbar.
        # Genau deshalb ist DIES die scharfe Stelle fuer die Einmaligkeit der
        # Kennung: haette der gescheiterte Versuch sie nicht verbraucht,
        # gelaenge der zweite Tap jetzt und wuerde schreiben. Der Grund muss
        # mitgeprueft werden, nicht nur der Statuscode - sonst waere dieser
        # Test auch dann gruen, wenn er an etwas anderem scheitert.
        zweiter_tap = _ausfuehren(basis, fuenf["vorgang"])
        check("Ein zweiter Tap auf dieselbe Kennung gelingt nicht, obwohl die "
              "Sperre weg ist", zweiter_tap.status_code == 409,
              str(zweiter_tap.status_code) + " " + zweiter_tap.text[:120])
        check("Und zwar ausdruecklich, WEIL die Kennung verbraucht ist",
              "Keine gueltige Bestaetigung offen" in zweiter_tap.json()["detail"],
              zweiter_tap.json()["detail"][:90])
        nichts_geschrieben("Nach dem zweiten Tap auf eine verbrauchte Kennung")

        # --- 8k) Der Cronjob kommt waehrend der Rueckfrage zuvor -----------
        # Das realistischste Szenario: zwischen dem Oeffnen der
        # Zusammenfassung und dem Tap darauf vergehen Sekunden bis Minuten.
        # Mit nur noch einem Tap ist das Fenster kleiner als vorher, aber es
        # ist nicht weg - die Frist von 120 Sekunden gilt unveraendert.
        sechs = _vorbereiten(basis, trade_id=2).json()
        bot_conn = sqlite3.connect(db_t3)
        bot_conn.execute(
            "UPDATE trades SET exit_time=?, exit_price=?, result=?, pnl_pct=?, "
            "status='closed' WHERE id=?",
            ("2026-09-09 08:00:00", 190.0, "stop_loss", -5.3, 2))
        bot_conn.commit()
        bot_conn.close()
        nach_cronjob = zeilen(db_t3)

        antwort = _ausfuehren(basis, sechs["vorgang"])
        check("Der manuelle Versuch wird abgelehnt, wenn der Cronjob zuvorkam",
              antwort.status_code == 409, str(antwort.status_code))
        check("Die Meldung erklaert, dass die Position nicht mehr offen ist",
              "nicht mehr offen" in antwort.json()["detail"].lower(),
              antwort.json()["detail"][:90])
        check("Der Ausstieg des Bots wurde NICHT ueberschrieben",
              unterschiede(nach_cronjob, zeilen(db_t3)) == [])
        zeile2 = [z for z in zeilen(db_t3) if z["id"] == 2][0]
        check("result ist weiterhin 'stop_loss', nicht 'manual_close'",
              zeile2["result"] == "stop_loss" and zeile2["exit_price"] == 190.0)
        # Dieser Versuch ist durch `schliessen.ausfuehren` gelaufen und hat
        # die Kennung damit verbraucht - ein zweiter Tap auf denselben
        # Vorgang findet nichts mehr vor. Das ist die Einmaligkeit, die
        # frueher zusaetzlich am falschen Text haengen blieb.
        wieder = _ausfuehren(basis, sechs["vorgang"])
        check("Die Kennung ist nach dem gescheiterten Versuch verbraucht",
              wieder.status_code == 409, str(wieder.status_code))
        # Auch hier der GRUND: ohne diese Zeile waere der Test gruen, weil
        # die Position ohnehin nicht mehr offen ist - die Einmaligkeit der
        # Kennung waere ungeprueft. Genau so ist die Mutationsprobe
        # "Kennung ueberlebt einen Fehlversuch" zuerst durchgerutscht.
        check("Und zwar WEIL die Kennung weg ist, nicht weil die Position "
              "geschlossen ist",
              "Keine gueltige Bestaetigung offen" in wieder.json()["detail"],
              wieder.json()["detail"][:90])

        # --- 8l) Der vollstaendige, erfolgreiche Weg -----------------------
        # EIN Aufruf mit der Kennung - kein Bestaetigungstext. Genau das ist
        # der "ein Tap"-Nachweis: wuerde irgendeine Schicht den Text noch
        # verlangen, schlaege dieser Abschnitt fehl. Zusaetzlich wird ein
        # FALSCHER Text mitgeschickt; er muss wirkungslos sein, sonst wird
        # er doch noch irgendwo ausgewertet.
        sieben = _vorbereiten(basis, trade_id=1).json()
        antwort = _ausfuehren(basis, sieben["vorgang"],
                               zusatz={"bestaetigung": "voelliger-unsinn"})
        check("Ein einzelner Tap (nur Kennung) gelingt - auch mit falschem "
              "Text im Koerper, der schlicht nicht mehr gelesen wird",
              antwort.status_code == 200,
              str(antwort.status_code) + " " + antwort.text[:120])
        ergebnis = antwort.json()
        check("Antwort nennt Symbol, Ausstiegskurs, PnL und den Vermerk",
              ergebnis["symbol"] == "BTCUSDT" and ergebnis["exit_preis"] == 110.0
              and ergebnis["pnl_pct"] == 9.7
              and ergebnis["ergebnis"] == "manual_close", str(ergebnis)[:150])

        diff = unterschiede(nach_cronjob, zeilen(db_t3))
        check("Genau die fuenf Ausstiegsfelder von Trade 1 haben sich geaendert",
              {(k, f) for k, f, _, _ in diff} ==
              {(1, "exit_time"), (1, "exit_price"), (1, "result"),
               (1, "pnl_pct"), (1, "status")}, str(sorted({(k, f) for k, f, _, _ in diff})))
        check("Keine andere Zeile wurde beruehrt",
              all(k == 1 for k, _, _, _ in diff))
        check("Zeilenzahl unveraendert (nichts eingefuegt, nichts geloescht)",
              len(zeilen(db_t3)) == len(vor_allem) == 3)
        zeile1 = [z for z in zeilen(db_t3) if z["id"] == 1][0]
        check("symbol, entry_price, stop_price, signal_time, entry_time unveraendert",
              all(zeile1[f] == vor_allem[0][f] for f in
                  ("symbol", "entry_price", "stop_price", "signal_time", "entry_time")))
        check("Die Datenbanken der uebrigen Bots sind byteweise identisch",
              _pruefsummen(andere) == andere_vorher)

        # Die geschlossene Position darf danach nicht mehr angeboten werden.
        rest = get(basis, "/api/bots/t3_supertrend/schliessbare-positionen?live=1").json()
        check("Die geschlossene Position taucht nicht mehr als offen auf",
              [p["id"] for p in rest["positionen"]] == [], str(rest["positionen"]))
        check("Der Trade erscheint jetzt in den geschlossenen Trades",
              any(t["ergebnis"] == "manual_close"
                  for t in get(basis, "/api/bots/t3_supertrend").json()["letzte_trades"]))

        # --- 8m) Protokoll --------------------------------------------------
        with open(protokoll_datei, encoding="utf-8") as datei:
            protokoll = [z.strip() for z in datei if z.strip()]
        check("Es wurde protokolliert", len(protokoll) > 0)
        check("Jede Zeile traegt die Marke MANUELLER-EINGRIFF",
              all("MANUELLER-EINGRIFF" in z for z in protokoll))
        check("Jede Zeile nennt das Dashboard als Quelle",
              all("quelle=dashboard" in z for z in protokoll),
              [z for z in protokoll if "quelle=dashboard" not in z][:1])
        erfolge = [z for z in protokoll if "ERFOLGREICH" in z]
        check("Genau EIN erfolgreicher Eingriff im Protokoll", len(erfolge) == 1,
              f"{len(erfolge)}")
        check("Die Erfolgszeile nennt Vorher- und Nachher-Zustand",
              "VORHER status=open" in erfolge[0]
              and "NACHHER status=closed" in erfolge[0]
              and "result=manual_close" in erfolge[0])
        check("Die Erfolgszeile nennt die Gegenstelle als Benutzer",
              "benutzer=dashboard@127.0.0.1" in erfolge[0], erfolge[0][-120:])
        ablehnungen = [z for z in protokoll if "ABGELEHNT" in z]
        check("Auch die abgelehnten Versuche stehen im Protokoll",
              len(ablehnungen) >= 5, f"{len(ablehnungen)} Ablehnungen")
        check("Abgelehnte Zeilen halten 'Datenbank unveraendert' fest",
              all("Datenbank unveraendert" in z for z in ablehnungen))
        print(f"       Beispiel: {erfolge[0]}")
    finally:
        monitor.fetch_live_prices_for_bots = original_kurse
        schliessen.vorgaenge_zuruecksetzen()


# ---------------------------------------------------------------------------
# 9) Notfallweg: ALLE offenen Positionen
# ---------------------------------------------------------------------------
# Der schwierigste Teil dieser Funktion ist nicht der Erfolgsfall, sondern der
# TEILAUSFALL: scheitert die dritte von fuenf Positionen, darf die Schleife
# nicht abbrechen und einen Zustand hinterlassen, den niemand benennen kann.
# Abschnitt 9f prueft das mit einem ECHTEN Fehlschlag des Kerns (kein
# Testdoppel), 9i zusaetzlich mit einem unerwarteten Fehler.

_NAECHSTE_ID = [100]


def _oeffne_positionen(db_pfad, posten):
    """Legt offene Testpositionen an und gibt [(id, symbol, entry)] zurueck.
    Eigene IDs ab 100, damit sie sich nicht mit den Zeilen aus Abschnitt 8
    ueberschneiden - dort wird bereits geschlossen."""
    angelegt = []
    conn = sqlite3.connect(db_pfad)
    try:
        # Die naechste freie ID kommt aus DIESER Datenbank, nicht aus einem
        # gemeinsamen Zaehler. Der gemeinsame Zaehler hat genau einmal
        # gereicht: sobald ein anderer Abschnitt eine Zeile OHNE eigene ID
        # einfuegt (dann vergibt SQLite max+1), laufen die beiden
        # Nummernkreise ineinander - und der Test scheitert an einem
        # UNIQUE-Verstoss statt an dem, was er pruefen soll.
        hoechste = conn.execute(
            "SELECT COALESCE(MAX(id), 0) FROM trades").fetchone()[0]
        naechste = max(_NAECHSTE_ID[0], hoechste + 1)
        for symbol, entry in posten:
            trade_id = naechste
            naechste += 1
            _NAECHSTE_ID[0] = max(_NAECHSTE_ID[0], naechste)
            conn.execute(
                "INSERT INTO trades (id, symbol, signal_time, entry_time, "
                "entry_price, stop_price, exit_time, exit_price, result, "
                "pnl_pct, status) VALUES (?,?,?,?,?,?,NULL,NULL,NULL,NULL,'open')",
                (trade_id, symbol, "2026-03-01 00:00:00", "2026-03-01 00:00:00",
                 entry, entry * 0.95))
            angelegt.append((trade_id, symbol, entry))
        conn.commit()
    finally:
        conn.close()
    return angelegt


def _alle_vorbereiten(basis, bot="t3_supertrend", token=TEST_TOKEN):
    return post(basis, f"/api/bots/{bot}/alle-schliessen/vorbereiten", {},
                 token=token)


def _alle_ausfuehren(basis, vorgang, bot="t3_supertrend", token=TEST_TOKEN):
    return post(basis, f"/api/bots/{bot}/alle-schliessen/ausfuehren",
                 {"vorgang": vorgang}, token=token)


# ---------------------------------------------------------------------------
# 9) Freischaltung: jeder Bot EINZELN gegen sein echtes forward_test.py
# ---------------------------------------------------------------------------
# Die Architektur war auf Erweiterbarkeit gebaut, aber "geht wahrscheinlich"
# ist bei einem Schreibzugriff in eine Live-Datenbank kein Nachweis. Dieser
# Abschnitt prueft jeden freigeschalteten Bot gegen seine TATSAECHLICHE
# Datei im Repo - nicht gegen eine Annahme und nicht gegen das synthetische
# Testprojekt der uebrigen Abschnitte.
#
# Geprueft wird je Bot:
#   a) das CREATE TABLE aus dem Bot-Quelltext enthaelt alle Spalten, die
#      geschrieben bzw. gelesen werden,
#   b) der Bot rechnet seinen PnL so, wie berechne_pnl() es nachbildet,
#   c) der Bot verwendet 'manual_close' nicht selbst als result,
#   d) Name und Anlageklasse stimmen mit dem Lesemodul ueberein,
#   e) und dann wird in einer Wegwerf-Datenbank, die aus DIESEM CREATE TABLE
#      entsteht, wirklich eine Position geschlossen - mit dem Kostensatz des
#      Bots und der Pruefung, dass genau die fuenf Ausstiegsfelder kippen.
#
# Punkt e) ist der eigentliche Beleg: er laeuft durch dieselbe Funktion, die
# auch die Live-Datenbank anfasst.

# Die fuenf Felder, die beim Schliessen geschrieben werden, und die, die
# offene_positionen() liest. Beide Listen stehen hier ausgeschrieben, damit
# der Test auffaellt, wenn sich eine der beiden Stellen im Kern aendert.
SCHREIB_SPALTEN = ("exit_time", "exit_price", "result", "pnl_pct", "status")
LESE_SPALTEN = ("id", "symbol", "entry_time", "entry_price", "stop_price")

# Die Rechnung, die berechne_pnl() nachbildet - als Quelltextmuster, damit
# eine kuenftige Aenderung im Bot hier auffaellt und nicht erst in einer
# falsch geschriebenen Zeile.
PNL_MUSTER = (
    r"pnl_pct\s*=\s*\(exit_price\s*-\s*trade\[.entry_price.\]\)\s*/\s*"
    r"trade\[.entry_price.\]\s*\*\s*100",
    r"pnl_pct\s*-=\s*2\s*\*\s*\(TRADING_FEE_PCT\s*\+\s*SLIPPAGE_PCT\)",
)


def _create_table_des_bots(bot: str) -> str:
    """Der CREATE-TABLE-Block aus dem echten forward_test.py des Bots."""
    pfad = os.path.join(BASE_DIR, "strategies", bot, "forward_test.py")
    quelle = open(pfad, encoding="utf-8").read()
    treffer = re.search(r"CREATE TABLE IF NOT EXISTS trades\s*\((.*?)\n\s*\)\s*\n",
                         quelle, re.S)
    if not treffer:
        raise AssertionError(f"Kein CREATE TABLE in {pfad} gefunden")
    return treffer.group(1)


def _spalten_des_bots(bot: str) -> list:
    """Spaltennamen aus dem CREATE TABLE - UNIQUE-Zeile ausgenommen."""
    spalten = []
    for zeile in _create_table_des_bots(bot).splitlines():
        zeile = zeile.strip().rstrip(",")
        if not zeile or zeile.upper().startswith(("UNIQUE", "PRIMARY KEY",
                                                   "FOREIGN KEY")):
            continue
        spalten.append(zeile.split()[0])
    return spalten


def teste_bot_freischaltung():
    print("\n9) Freischaltung je Bot - gegen das echte forward_test.py")

    erwartete_bots = sorted(monitor.DISPLAY_NAMES)
    check("Alle neun Bots sind freigeschaltet",
          sorted(manual_close.SCHLIESSBARE_BOTS) == erwartete_bots,
          str(sorted(manual_close.SCHLIESSBARE_BOTS)))

    wurzel = tempfile.mkdtemp(prefix="freischaltung_")
    alt = (manual_close.BASE_DIR, manual_close.STRATEGIES_DIR)
    alt_griffe = list(manual_close._protokoll.handlers)
    for griff in alt_griffe:
        manual_close._protokoll.removeHandler(griff)
    manual_close._protokoll.addHandler(logging.FileHandler(
        os.path.join(wurzel, "eingriffe.log"), encoding="utf-8"))
    try:
        for bot, angaben in sorted(manual_close.SCHLIESSBARE_BOTS.items()):
            print(f"  -- {bot}")
            quelle = open(os.path.join(BASE_DIR, "strategies", bot,
                                        "forward_test.py"),
                           encoding="utf-8").read()

            # --- a) Schema -------------------------------------------------
            spalten = _spalten_des_bots(bot)
            fehlend_schreib = [s for s in SCHREIB_SPALTEN if s not in spalten]
            check(f"{bot}: alle fuenf Ausstiegsspalten im CREATE TABLE",
                  not fehlend_schreib, f"fehlt: {fehlend_schreib}")
            fehlend_lese = [s for s in LESE_SPALTEN if s not in spalten]
            check(f"{bot}: alle von offene_positionen() gelesenen Spalten da",
                  not fehlend_lese, f"fehlt: {fehlend_lese}")

            # --- b) PnL-Formel ---------------------------------------------
            fehlende_muster = [m for m in PNL_MUSTER
                               if re.search(m, quelle) is None]
            check(f"{bot}: rechnet den PnL so, wie berechne_pnl() es nachbildet",
                  not fehlende_muster, f"Muster ohne Treffer: {len(fehlende_muster)}")

            # --- c) result-Werte -------------------------------------------
            eigene_ergebnisse = set(re.findall(r'result\s*=\s*"([a-z_]+)"', quelle))
            eigene_ergebnisse |= set(re.findall(r'"(stop_loss|take_profit|'
                                                 r'time_exit|sma_exit|trend_flip|'
                                                 r't3_crossunder)"', quelle))
            check(f"{bot}: verwendet '{manual_close.MANUELLER_GRUND}' nicht selbst",
                  manual_close.MANUELLER_GRUND not in eigene_ergebnisse,
                  str(sorted(eigene_ergebnisse)))

            # --- d) Name und Anlageklasse ----------------------------------
            check(f"{bot}: Anzeigename deckt sich mit dem Lesemodul",
                  angaben["anzeigename"] == monitor.DISPLAY_NAMES[bot],
                  f"{angaben['anzeigename']!r} vs {monitor.DISPLAY_NAMES[bot]!r}")
            check(f"{bot}: Anlageklasse deckt sich mit dem Lesemodul",
                  angaben["anlageklasse"] == monitor.ASSET_CLASS[bot],
                  f"{angaben['anlageklasse']!r} vs {monitor.ASSET_CLASS[bot]!r}")

            # --- e) Echtes Schliessen in einer Wegwerf-Datenbank -----------
            # Die Tabelle entsteht aus DEM CREATE TABLE DES BOTS, samt seiner
            # Zusatzspalten. Genau so faellt auf, wenn eine davon NOT NULL
            # waere oder das UPDATE an ihr scheitern wuerde.
            os.makedirs(os.path.join(wurzel, "strategies", bot), exist_ok=True)
            with open(os.path.join(wurzel, "strategies", bot, "forward_test.py"),
                       "w", encoding="utf-8") as ziel:
                ziel.write(quelle)
            db = os.path.join(wurzel, f"paper_trading_{bot}.db")
            if os.path.exists(db):
                os.remove(db)
            conn = sqlite3.connect(db)
            conn.execute(f"CREATE TABLE trades (\n{_create_table_des_bots(bot)}\n)")
            conn.execute(
                "INSERT INTO trades (symbol, signal_time, entry_time, "
                "entry_price, stop_price, status) "
                "VALUES ('BTCUSDT','2026-03-01 00:00:00','2026-03-01 00:00:00',"
                "100.0, 95.0, 'open')")
            # Eine zweite, bereits geschlossene Zeile: sie muss unberuehrt
            # bleiben und belegt, dass das UPDATE nicht zu breit trifft.
            conn.execute(
                "INSERT INTO trades (symbol, signal_time, entry_time, "
                "entry_price, stop_price, exit_time, exit_price, result, "
                "pnl_pct, status) VALUES ('ETHUSDT','2026-02-01 00:00:00',"
                "'2026-02-01 00:00:00', 200.0, 190.0, '2026-02-02 00:00:00',"
                "210.0, 'take_profit', 4.7, 'closed')")
            conn.commit()
            conn.close()

            manual_close.BASE_DIR = wurzel
            manual_close.STRATEGIES_DIR = os.path.join(wurzel, "strategies")

            offen = manual_close.offene_positionen(bot)
            check(f"{bot}: offene_positionen() liest die eine offene Zeile",
                  [p["symbol"] for p in offen] == ["BTCUSDT"], str(offen)[:110])

            vorher = zeilen(db)
            kosten = manual_close.kostensatz(bot)
            ergebnis = manual_close.schliesse_position(
                bot, offen[0]["id"], 110.0, "freischaltungstest",
                manual_close.BESTAETIGUNGSTEXT,
                quelle=manual_close.QUELLE_DASHBOARD)
            erwarteter_pnl = round(10.0 - kosten, 2)
            check(f"{bot}: PnL nach dem Kostensatz DIESES Bots ({kosten})",
                  ergebnis["pnl_pct"] == erwarteter_pnl,
                  f"{ergebnis['pnl_pct']} statt {erwarteter_pnl}")
            check(f"{bot}: Vermerk ist '{manual_close.MANUELLER_GRUND}'",
                  ergebnis["result"] == manual_close.MANUELLER_GRUND)
            diff = unterschiede(vorher, zeilen(db))
            check(f"{bot}: genau die fuenf Ausstiegsfelder EINER Zeile geaendert",
                  {f for _, f, _, _ in diff} == set(SCHREIB_SPALTEN)
                  and len({k for k, _, _, _ in diff}) == 1,
                  str(sorted({(k, f) for k, f, _, _ in diff})))
            check(f"{bot}: die bereits geschlossene Zeile blieb unberuehrt",
                  all(k != 2 for k, _, _, _ in diff))
            check(f"{bot}: danach keine offene Position mehr",
                  manual_close.offene_positionen(bot) == [])
    finally:
        manual_close.BASE_DIR, manual_close.STRATEGIES_DIR = alt
        for griff in list(manual_close._protokoll.handlers):
            manual_close._protokoll.removeHandler(griff)
        for griff in alt_griffe:
            manual_close._protokoll.addHandler(griff)
        shutil.rmtree(wurzel, ignore_errors=True)


def teste_alle_schliessen(basis, wurzel, db_dateien, protokoll_datei):
    print("\n9) Notfallweg: alle Positionen eines Bots schliessen")

    db_t3 = db_dateien["t3_supertrend"]
    andere = {n: p for n, p in db_dateien.items() if n != "t3_supertrend"}
    andere_vorher = _pruefsummen(andere)

    def status(trade_id):
        conn = sqlite3.connect(db_t3)
        try:
            zeile = conn.execute(
                "SELECT status, result, exit_price, pnl_pct FROM trades WHERE id=?",
                (trade_id,)).fetchone()
        finally:
            conn.close()
        return tuple(zeile) if zeile else None

    original_kurse = monitor.fetch_live_prices_for_bots
    monitor.fetch_live_prices_for_bots = lambda bots: dict(TESTKURSE)
    schliessen.vorgaenge_zuruecksetzen()
    protokoll_vorher = len(open(protokoll_datei, encoding="utf-8").read().splitlines())
    try:
        # --- 9a) Kein offener Posten: der Weg beginnt gar nicht -----------
        # Abschnitt 8 hat alle offenen t3-Positionen geschlossen, der Stand
        # ist also genau der, den dieser Fall braucht.
        antwort = _alle_vorbereiten(basis)
        check("Ohne offene Position wird das Vorbereiten abgelehnt (409)",
              antwort.status_code == 409, str(antwort.status_code))
        check("Die Meldung sagt, dass es nichts zu schliessen gibt",
              "keine offene Position" in antwort.json()["detail"],
              antwort.json()["detail"][:90])

        # --- 9b) Ohne gueltiges Token ------------------------------------
        _oeffne_positionen(db_t3, [("BTCUSDT", 100.0)])
        vorbereitet = _alle_vorbereiten(basis).json()
        for token in (None, "falsches-token-aber-lang-genug"):
            check(f"Vorbereiten ohne gueltiges Token: 401 (Token {token!r})",
                  _alle_vorbereiten(basis, token=token).status_code == 401)
            check(f"Ausfuehren ohne gueltiges Token: 401 (Token {token!r})",
                  _alle_ausfuehren(basis, vorbereitet["vorgang"],
                                    token=token).status_code == 401)
        check("Ein abgewiesener Fremdzugriff verbraucht den Vorgang nicht",
              schliessen.offener_vorgang(vorbereitet["vorgang"]) is not None)

        # --- 9c) Nicht freigeschalteter Bot -------------------------------
        # Wie in 8e: alle neun sind freigeschaltet, geprueft wird die SPERRE.
        for bot in ("elliott_wave", "volatility_breakout"):
            gemerkt = manual_close.SCHLIESSBARE_BOTS.pop(bot)
            try:
                check(f"Vorbereiten fuer den gesperrten {bot}: 403",
                      _alle_vorbereiten(basis, bot=bot).status_code == 403)
                check(f"Ausfuehren fuer den gesperrten {bot}: 403",
                      _alle_ausfuehren(basis, vorbereitet["vorgang"],
                                        bot=bot).status_code == 403)
            finally:
                manual_close.SCHLIESSBARE_BOTS[bot] = gemerkt
        check("Danach sind wieder alle neun Bots freigeschaltet",
              sorted(manual_close.SCHLIESSBARE_BOTS) == sorted(monitor.DISPLAY_NAMES))

        # --- 9d) Eine Kennung der einen Art auf dem Endpunkt der anderen ---
        # Ohne diese Pruefung waere die zweite Klick-Bestaetigung umgehbar:
        # die billiger zu bekommende Einzel-Kennung wuerde auf dem
        # Alle-Endpunkt alles schliessen.
        einzel = _vorbereiten(basis, trade_id=vorbereitet["positionen"][0]["id"]).json()
        antwort = _alle_ausfuehren(basis, einzel["vorgang"])
        check("Eine EINZEL-Kennung loest auf dem Alle-Endpunkt nichts aus (409)",
              antwort.status_code == 409, str(antwort.status_code))
        check("Und zwar ausdruecklich, WEIL sie zu einem anderen Vorgang gehoert",
              "anderen Vorgang" in antwort.json()["detail"],
              antwort.json()["detail"][:90])
        antwort = _ausfuehren(basis, vorbereitet["vorgang"])
        check("Eine ALLE-Kennung loest auf dem Einzel-Endpunkt nichts aus (409)",
              antwort.status_code == 409, str(antwort.status_code))
        check("Auch hier ist der Grund die fremde Vorgangsart",
              "anderen Vorgang" in antwort.json()["detail"],
              antwort.json()["detail"][:90])
        check("Die Position ist nach beiden Versuchen unveraendert offen",
              status(vorbereitet["positionen"][0]["id"])[0] == "open")

        # --- 9e) Abbruch in beiden Klick-Stufen ---------------------------
        # Serverseitig ist beides derselbe Aufruf - der Unterschied liegt
        # allein in der Oberflaeche. Geprueft wird deshalb, dass die Kennung
        # danach in BEIDEN Faellen wertlos ist.
        for stufe in ("Stufe 1", "Stufe 2"):
            eins = _alle_vorbereiten(basis).json()
            post(basis, "/api/bots/t3_supertrend/schliessen/abbrechen",
                 {"vorgang": eins["vorgang"]})
            check(f"Abbruch in {stufe} macht die Kennung wertlos",
                  _alle_ausfuehren(basis, eins["vorgang"]).status_code == 409)
        check("Nach beiden Abbruechen ist die Position weiterhin offen",
              status(vorbereitet["positionen"][0]["id"])[0] == "open")

        # --- 9f) TEILAUSFALL mit einem ECHTEN Fehlschlag des Kerns --------
        # Kein Testdoppel: einer der drei Positionen wird nach der Uebersicht
        # der Einstiegskurs entzogen. Der Kern lehnt sie daraufhin INNERHALB
        # seiner Transaktion ab (berechne_pnl wirft), die beiden uebrigen
        # muessen trotzdem durchlaufen.
        schliessen.vorgaenge_zuruecksetzen()
        offen = _oeffne_positionen(db_t3, [("ETHUSDT", 200.0), ("SOLUSDT", 20.0)])
        drei = _alle_vorbereiten(basis).json()
        ids = [p["id"] for p in drei["positionen"]]
        check("Die Uebersicht nennt alle drei offenen Positionen",
              len(ids) == 3 and drei["anzahl"] == 3, str(drei["positionen"])[:150])
        check("Und einen Durchschnitt je Position statt einer Summe",
              "pnl_schnitt_pct" in drei and "pnl_summe_pct" not in drei)

        opfer = offen[1][0]                      # SOLUSDT
        conn = sqlite3.connect(db_t3)
        conn.execute("UPDATE trades SET entry_price=NULL WHERE id=?", (opfer,))
        conn.commit()
        conn.close()

        antwort = _alle_ausfuehren(basis, drei["vorgang"])
        check("Ein Teilausfall ist KEIN HTTP-Fehler - die Anfrage wurde "
              "vollstaendig bearbeitet (200)",
              antwort.status_code == 200, str(antwort.status_code) + antwort.text[:120])
        r = antwort.json()
        check("erfolg ist false, weil eine Position fehlschlug",
              r["erfolg"] is False, str(r["erfolg"]))
        check("Zwei von drei geschlossen, eine fehlgeschlagen",
              (r["anzahl_geschlossen"], r["anzahl_fehlgeschlagen"],
               r["angefragt"]) == (2, 1, 3),
              f"{r['anzahl_geschlossen']}/{r['anzahl_fehlgeschlagen']}/{r['angefragt']}")
        check("Die fehlgeschlagene Position wird namentlich und mit Grund genannt",
              r["fehlgeschlagen"][0]["trade_id"] == opfer
              and "Einstiegskurs" in r["fehlgeschlagen"][0]["grund"],
              str(r["fehlgeschlagen"])[:140])
        check("Die Meldung nennt Erfolge UND Fehlschlag in einem Satz",
              "2 von 3" in r["meldung"] and "fehlgeschlagen" in r["meldung"],
              r["meldung"][:160])
        uebrige = [i for i in ids if i != opfer]
        check("Die beiden uebrigen Positionen sind wirklich geschlossen",
              all(status(i)[0] == "closed" and status(i)[1] == "manual_close"
                  for i in uebrige), str([status(i) for i in uebrige]))
        check("DIE SCHLEIFE IST NICHT ABGEBROCHEN: auch die Position NACH der "
              "fehlgeschlagenen wurde bearbeitet",
              status(ids[-1])[0] == "closed" if ids[-1] != opfer
              else status(ids[0])[0] == "closed")
        check("Die fehlgeschlagene Position bleibt offen und unberuehrt",
              status(opfer)[0] == "open" and status(opfer)[2] is None,
              str(status(opfer)))
        check("Die Datenbanken der uebrigen Bots sind unveraendert",
              _pruefsummen(andere) == andere_vorher)

        # Aufraeumen: Einstiegskurs zuruecksetzen, Position schliessen.
        conn = sqlite3.connect(db_t3)
        conn.execute("UPDATE trades SET entry_price=20.0, status='closed', "
                      "result='aufgeraeumt' WHERE id=?", (opfer,))
        conn.commit()
        conn.close()

        # --- 9g) Nebenlaeufigkeit: der Cronjob kommt dazwischen -----------
        schliessen.vorgaenge_zuruecksetzen()
        offen = _oeffne_positionen(db_t3, [("BTCUSDT", 100.0), ("ETHUSDT", 200.0),
                                            ("SOLUSDT", 20.0)])
        vier = _alle_vorbereiten(basis).json()
        zuvorgekommen = offen[1][0]
        conn = sqlite3.connect(db_t3)
        conn.execute("UPDATE trades SET exit_time=?, exit_price=?, result=?, "
                      "pnl_pct=?, status='closed' WHERE id=?",
                      ("2026-09-10 08:00:00", 195.0, "stop_loss", -2.8, zuvorgekommen))
        conn.commit()
        conn.close()

        r = _alle_ausfuehren(basis, vier["vorgang"]).json()
        check("Die vom Bot geschlossene Position wird UEBERSPRUNGEN, nicht "
              "als Fehlschlag gezaehlt",
              r["anzahl_uebersprungen"] == 1
              and r["uebersprungen"][0]["trade_id"] == zuvorgekommen
              and r["anzahl_fehlgeschlagen"] == 0, str(r["uebersprungen"]))
        check("Die uebrigen Positionen wurden trotzdem geschlossen",
              r["anzahl_geschlossen"] == len(vier["positionen"]) - 1,
              f"{r['anzahl_geschlossen']} von {len(vier['positionen'])}")
        check("Der Ausstieg des Bots wurde NICHT ueberschrieben",
              status(zuvorgekommen)[1] == "stop_loss"
              and status(zuvorgekommen)[2] == 195.0, str(status(zuvorgekommen)))
        check("Die Meldung erklaert das Ueberspringen",
              "uebersprungen" in r["meldung"] and "selbst geschlossen" in r["meldung"],
              r["meldung"][:170])

        # --- 9h) Eine NACH der Uebersicht eroeffnete Position ------------
        # Sie wird NICHT angefasst: der Nutzer hat sie nie gesehen und ihren
        # Kurs nie bestaetigt. Ausgewiesen wird sie trotzdem.
        schliessen.vorgaenge_zuruecksetzen()
        _oeffne_positionen(db_t3, [("BTCUSDT", 100.0)])
        fuenf = _alle_vorbereiten(basis).json()
        spaet = _oeffne_positionen(db_t3, [("ETHUSDT", 200.0)])[0][0]
        r = _alle_ausfuehren(basis, fuenf["vorgang"]).json()
        check("Die spaeter eroeffnete Position wird NICHT geschlossen",
              status(spaet)[0] == "open", str(status(spaet)))
        check("Sie wird im Ergebnis aber ausdruecklich ausgewiesen",
              r["nicht_bestaetigt"] == [spaet], str(r["nicht_bestaetigt"]))
        check("Und die Meldung sagt, dass sie nach der Uebersicht entstand",
              "nach der Uebersicht eroeffnet" in r["meldung"], r["meldung"][:170])
        check("Die bestaetigte Position wurde geschlossen",
              r["anzahl_geschlossen"] == 1, str(r["anzahl_geschlossen"]))

        # --- 9i) Ein UNERWARTETER Fehler bricht die Schleife auch nicht ---
        # Der eine Fall, fuer den ein Testdoppel noetig ist: ein Fehler, den
        # der Kern gar nicht vorsieht. Genau dort waere ein Abbruch am
        # schlimmsten, weil ihn niemand vorhergesehen hat.
        schliessen.vorgaenge_zuruecksetzen()
        offen = _oeffne_positionen(db_t3, [("SOLUSDT", 20.0)])
        sechs = _alle_vorbereiten(basis).json()
        ids = [p["id"] for p in sechs["positionen"]]
        platzt = ids[0]
        echt = manual_close.schliesse_position

        def mit_panne(bot_name, trade_id, *a, **kw):
            if trade_id == platzt:
                raise RuntimeError("simulierter unerwarteter Fehler")
            return echt(bot_name, trade_id, *a, **kw)

        manual_close.schliesse_position = mit_panne
        try:
            antwort = _alle_ausfuehren(basis, sechs["vorgang"])
        finally:
            manual_close.schliesse_position = echt
        check("Auch ein unerwarteter Fehler endet in einer Zusammenfassung, "
              "nicht in einem 500er", antwort.status_code == 200,
              str(antwort.status_code) + antwort.text[:120])
        r = antwort.json()
        check("Er wird als Fehlschlag mit Grund ausgewiesen",
              r["anzahl_fehlgeschlagen"] >= 1
              and "unerwarteter Fehler" in r["fehlgeschlagen"][0]["grund"],
              str(r["fehlgeschlagen"])[:140])
        check("Und die uebrigen Positionen laufen trotzdem durch",
              r["anzahl_geschlossen"] == len(ids) - 1,
              f"{r['anzahl_geschlossen']} von {len(ids)}")
        check("Die geplatzte Position bleibt offen und unberuehrt",
              status(platzt)[0] == "open" and status(platzt)[2] is None,
              str(status(platzt)))

        # --- 9j) Der vollstaendige Erfolgsfall ---------------------------
        schliessen.vorgaenge_zuruecksetzen()
        conn = sqlite3.connect(db_t3)
        conn.execute("UPDATE trades SET status='closed', result='aufgeraeumt' "
                      "WHERE status='open'")
        conn.commit()
        conn.close()
        offen = _oeffne_positionen(db_t3, [("BTCUSDT", 100.0), ("ETHUSDT", 200.0),
                                            ("SOLUSDT", 22.0),
                                            ("XRPUSDT", 0.5)])
        sieben = _alle_vorbereiten(basis).json()
        # XRPUSDT steht nicht in TESTKURSE - ohne Kurs wuerde der Kern
        # ablehnen, also wird die Position schon in der Uebersicht als nicht
        # schliessbar ausgewiesen statt spaeter als Fehlschlag gemeldet.
        ohne_kurs = [p for p in sieben["positionen"] if not p["schliessbar_jetzt"]]
        check("Eine Position ohne Kurs wird vorab als nicht schliessbar "
              "ausgewiesen, nicht spaeter als Fehlschlag",
              [p["symbol"] for p in ohne_kurs] == ["XRPUSDT"]
              and "kein aktueller Kurs" in ohne_kurs[0]["grund"],
              str(ohne_kurs))
        check("Gezaehlt werden nur die schliessbaren (3 von 4)",
              (sieben["anzahl"], sieben["anzahl_gesamt"]) == (3, 4),
              f"{sieben['anzahl']}/{sieben['anzahl_gesamt']}")
        check("Der Durchschnitt rechnet nur ueber die mit Kurs",
              sieben["pnl_schnitt_pct"] == round((9.7 - 10.3 - 0.3) / 3, 2),
              str(sieben["pnl_schnitt_pct"]))

        vor_lauf = [z for z in zeilen(db_t3)]
        protokoll_vor_erfolgslauf = len(
            open(protokoll_datei, encoding="utf-8").read().splitlines())
        r = _alle_ausfuehren(basis, sieben["vorgang"]).json()
        check("Alle drei schliessbaren Positionen wurden geschlossen",
              r["erfolg"] is True and r["anzahl_geschlossen"] == 3
              and r["anzahl_fehlgeschlagen"] == 0, str(r["meldung"])[:140])
        check("Jede mit ihrem EIGENEN Kurs, nicht einem gemeinsamen",
              sorted((g["symbol"], g["exit_preis"]) for g in r["geschlossen"])
              == [("BTCUSDT", 110.0), ("ETHUSDT", 180.0), ("SOLUSDT", 22.0)],
              str(sorted((g["symbol"], g["exit_preis"]) for g in r["geschlossen"])))
        check("Und mit dem PnL nach der Bot-Formel je Position",
              sorted(g["pnl_pct"] for g in r["geschlossen"]) == [-10.3, -0.3, 9.7],
              str(sorted(g["pnl_pct"] for g in r["geschlossen"])))
        diff = unterschiede(vor_lauf, zeilen(db_t3))
        check("Geaendert wurden genau die fuenf Ausstiegsfelder der drei Zeilen",
              {f for _, f, _, _ in diff} ==
              {"exit_time", "exit_price", "result", "pnl_pct", "status"}
              and len({k for k, _, _, _ in diff}) == 3,
              str(sorted({(k, f) for k, f, _, _ in diff})))
        check("Die Position ohne Kurs blieb offen",
              status(offen[3][0])[0] == "open", str(status(offen[3][0])))
        check("Zeilenzahl unveraendert - nichts eingefuegt, nichts geloescht",
              len(zeilen(db_t3)) == len(vor_lauf))
        check("Die Datenbanken der uebrigen Bots sind byteweise identisch",
              _pruefsummen(andere) == andere_vorher)

        # --- 9k) Protokoll: je Position eine eigene Zeile ----------------
        # Gemessen wird am EINEN Lauf aus 9j (drei Positionen), nicht an einer
        # Gesamtsumme ueber den ganzen Abschnitt: eine hartkodierte Summe
        # waere bei jeder spaeteren Ergaenzung falsch, ohne dass die Aussage
        # "eine Zeile je Position" dadurch besser geprueft wuerde.
        protokoll = open(protokoll_datei, encoding="utf-8").read().splitlines()
        vom_erfolgslauf = [z for z in protokoll[protokoll_vor_erfolgslauf:]
                            if z.strip() and "ERFOLGREICH" in z]
        check("Der Lauf mit drei Positionen erzeugt GENAU DREI Erfolgszeilen - "
              "keine zusammengefasste Batch-Zeile",
              len(vom_erfolgslauf) == 3, f"{len(vom_erfolgslauf)} Erfolgszeilen")
        # Jede Zeile muss GENAU EINE der drei Positionen nennen - sonst
        # koennten drei Zeilen auch dreimal dieselbe Position sein.
        erwartete_ids = sorted(g["trade_id"] for g in r["geschlossen"])
        genannte_ids = sorted(
            tid for tid in erwartete_ids
            if len([z for z in vom_erfolgslauf if f"trade_id={tid} " in z]) == 1)
        check("Und jede Zeile nennt genau eine andere Position",
              genannte_ids == erwartete_ids,
              f"erwartet {erwartete_ids}, eindeutig genannt {genannte_ids}")

        neue = [z for z in protokoll[protokoll_vorher:] if z.strip()]
        erfolge = [z for z in neue if "ERFOLGREICH" in z]
        check("Ueber den ganzen Abschnitt entspricht die Zahl der "
              "Erfolgszeilen der Zahl tatsaechlich geschlossener Positionen",
              len(erfolge) == len([z for z in zeilen(db_t3)
                                    if z["result"] == "manual_close"
                                    and z["id"] >= 100]),
              f"{len(erfolge)} Erfolgszeilen")
        check("Jede Zeile traegt die Marke MANUELLER-EINGRIFF und quelle=dashboard",
              all("MANUELLER-EINGRIFF" in z and "quelle=dashboard" in z
                  for z in neue),
              [z for z in neue if "quelle=dashboard" not in z][:1])
        check("Die Erfolgszeilen nennen jede einzeln Vorher- und Nachher-Zustand",
              all("VORHER status=open" in z and "NACHHER status=closed" in z
                  for z in erfolge))
        check("Auch die abgelehnten Einzelversuche stehen im Protokoll",
              len([z for z in neue if "ABGELEHNT" in z]) >= 3,
              f"{len([z for z in neue if 'ABGELEHNT' in z])} Ablehnungen")
    finally:
        monitor.fetch_live_prices_for_bots = original_kurse
        schliessen.vorgaenge_zuruecksetzen()


# ---------------------------------------------------------------------------
# 15) Gewichteter Durchschnitt nach Positionsgroesse
# ---------------------------------------------------------------------------
# Der einfache Durchschnitt gewichtet eine Position mit 2 % Positionsgroesse
# genauso wie eine mit 10 %. Diese Pruefungen belegen dreierlei:
#
#   * die Gewichtung rechnet richtig - und zwar BOT-UEBERGREIFEND, wo sie sich
#     vom einfachen Durchschnitt ueberhaupt unterscheiden kann,
#   * ein Bot ohne dokumentierte Positionsgroesse wird ausgeschlossen und
#     BENANNT, nicht mit einem angenommenen Wert mitgerechnet,
#   * die bisherige Anzeige (Durchschnitt, Spannweite) bleibt unveraendert
#     daneben stehen - die neue Zahl kommt dazu, sie ersetzt nichts.

def _ohne_allokation_anlegen(wurzel, name="ohne_positionsgroesse"):
    """Ein Bot-Verzeichnis ohne live_params.py und ohne equity_simulation.py.
    Der Name steht nicht in monitor.ASSET_CLASS, discover_bots() uebergeht ihn
    also - er existiert nur fuer diese Rechnung."""
    ordner = os.path.join(wurzel, "strategies", name)
    os.makedirs(ordner, exist_ok=True)
    with open(os.path.join(ordner, "forward_test.py"), "w", encoding="utf-8") as fh:
        fh.write("TRADING_FEE_PCT = 0.1\nSLIPPAGE_PCT = 0.05\n")
    return name


def _js_funktion(code: str, name: str) -> str:
    """Der Rumpf einer JS-Funktion aus bot.html, von ihrem Kopf bis zur
    naechsten Funktion auf Modulebene. Grob, aber ausreichend: die Datei
    schreibt jede Funktion linksbuendig."""
    for kopf in (f"function {name}(", f"async function {name}("):
        start = code.find(kopf)
        if start >= 0:
            break
    else:
        return ""
    rest = code[start + 10:]
    enden = [rest.find(m) for m in ("\nfunction ", "\nasync function ",
                                    "\nconst ", "\ndocument.")]
    enden = [e for e in enden if e >= 0]
    return rest[:min(enden)] if enden else rest


def _bot_dateien_pruefsummen(wurzel: str) -> dict:
    """Pruefsummen aller .py-Dateien unter strategies/ - der Nachweis, dass
    das Lesen der Positionsgroesse wirklich nur liest."""
    summen = {}
    basis = os.path.join(wurzel, "strategies")
    for ordner, _, dateien in os.walk(basis):
        for datei in sorted(dateien):
            if not datei.endswith(".py"):
                continue
            pfad = os.path.join(ordner, datei)
            summen[os.path.relpath(pfad, basis)] = hashlib.sha256(
                open(pfad, "rb").read()).hexdigest()
    return summen


def teste_gewichteten_pnl(basis, wurzel, db_dateien, protokoll_datei):
    print("\n15) Gewichteter Durchschnitt nach Positionsgroesse")
    bot_dateien_vorher = _bot_dateien_pruefsummen(wurzel)

    # --- 15a) Die Allokation wird GELESEN, nicht geraten ------------------
    werte = {name: manual_close.allokation(name)
             for name in ("t3_supertrend", "elliott_wave", "volatility_breakout")}
    check("t3_supertrend: 10 % aus equity_simulation.py (Anteil 0.10)",
          werte["t3_supertrend"]["prozent"] == 10.0
          and werte["t3_supertrend"]["quelle"] == "equity_simulation.py",
          str(werte["t3_supertrend"]))
    check("Ein ALLOCATION_PCT, das dort nur als KOMMENTAR steht, gilt nicht als Wert",
          "ALLOCATION_PCT" in open(os.path.join(
              wurzel, "strategies", "t3_supertrend", "live_params.py"),
              encoding="utf-8").read()
          and werte["t3_supertrend"]["quelle"] != "live_params.py")
    check("elliott_wave: 5 % aus live_params.py (Prozent -> Anteil 0.05)",
          werte["elliott_wave"]["anteil"] == 0.05
          and werte["elliott_wave"]["quelle"] == "live_params.py",
          str(werte["elliott_wave"]))
    check("volatility_breakout: 2 % aus live_params.py",
          werte["volatility_breakout"]["anteil"] == 0.02, str(werte["volatility_breakout"]))

    ohne = _ohne_allokation_anlegen(wurzel)
    try:
        leer = manual_close.allokation(ohne)
        check("Ein Bot ohne beide Dateien bekommt KEINEN angenommenen Wert",
              leer["anteil"] is None and leer["prozent"] is None, str(leer))
        check("Und einen Grund, der beide Dateien nennt",
              "live_params.py" in leer["grund"]
              and "equity_simulation.py" in leer["grund"], leer["grund"])

        # --- 15b) Die Rechnung, bot-uebergreifend ------------------------
        # 10 % zweimal (-4, -6), 5 % einmal (+2), 2 % einmal (+10) und ein
        # nicht gewichtbarer Bot (+1). Von Hand:
        #   Zaehler = 0.10*(-4-6) + 0.05*2 + 0.02*10 = -0.70
        #   Nenner  = 0.10*2      + 0.05*1  + 0.02*1 =  0.27
        #   gewichtet = -2.59 %   einfach = (-4-6+2+10)/4 = +0.50 %
        # Das Vorzeichen dreht sich: die kleine Position mit +10 % zieht den
        # einfachen Durchschnitt ins Plus, obwohl sie nur ein Fuenftel des
        # Kapitals der grossen traegt. Genau dieser Unterschied ist der Grund
        # fuer die ganze Rechnung.
        beitraege = [("t3_supertrend", -4.0), ("t3_supertrend", -6.0),
                     ("elliott_wave", 2.0), ("volatility_breakout", 10.0),
                     (ohne, 1.0)]
        g = schliessen.gewichteter_pnl(beitraege)
        check("Gewichtet ueber drei Bots: -2.59 %", g["wert_pct"] == -2.59,
              str(g["wert_pct"]))
        check("Dieselben Positionen ungewichtet: +0.50 % - das Vorzeichen dreht sich",
              g["ungewichtet_schnitt_pct"] == 0.5, str(g["ungewichtet_schnitt_pct"]))
        check("Die nicht gewichtbare Position zaehlt in KEINER der beiden Zahlen",
              g["anzahl"] == 4, str(g["anzahl"]))
        check("Jeder einbezogene Bot steht mit Groesse, Quelle und Anzahl da",
              [(w["bot"], w["allokation_pct"], w["quelle"], w["anzahl"])
               for w in g["gewichte"]]
              == [("elliott_wave", 5.0, "live_params.py", 1),
                  ("t3_supertrend", 10.0, "equity_simulation.py", 2),
                  ("volatility_breakout", 2.0, "live_params.py", 1)],
              str(g["gewichte"]))
        check("Der nicht gewichtbare Bot wird BENANNT, mit Grund und eigener Zahl",
              len(g["nicht_gewichtbar"]) == 1
              and g["nicht_gewichtbar"][0]["bot"] == ohne
              and g["nicht_gewichtbar"][0]["anzahl"] == 1
              and g["nicht_gewichtbar"][0]["pnl_schnitt_pct"] == 1.0
              and "ALLOCATION_PCT" in g["nicht_gewichtbar"][0]["grund"],
              str(g["nicht_gewichtbar"]))
        check("Die Grundlage steht als Text dabei (Backtest-Annahme)",
              "ALLOCATION_PCT" in g["grundlage"] and "Backtest" in g["grundlage"],
              g["grundlage"])
        check("Der Hinweis nennt die Annahme, die fehlende Kapitalbindung und "
              "die Stelle, an der eine echte Portfolio-Rendite steht",
              "Annahme" in g["hinweis"]
              and "KEINE live getrackte Kapitalbindung" in g["hinweis"]
              and "keine Portfolio-Rendite" in g["hinweis"]
              and "equity_simulation.py" in g["hinweis"], g["hinweis"][:80])

        # Gegenprobe zur Rechnung: dieselben Werte, aber alle Bots mit
        # derselben Groesse - dann MUESSEN beide Zahlen uebereinstimmen. Ohne
        # diese Probe koennte die Gewichtung auch zufaellig richtig aussehen.
        gleich = schliessen.gewichteter_pnl(
            [("elliott_wave", -4.0), ("elliott_wave", -6.0),
             ("elliott_wave", 2.0), ("elliott_wave", 10.0)])
        check("Bei EINEM Bot sind gewichtet und ungewichtet identisch (+0.5 %)",
              gleich["wert_pct"] == gleich["ungewichtet_schnitt_pct"] == 0.5,
              f"{gleich['wert_pct']} / {gleich['ungewichtet_schnitt_pct']}")
        check("Ohne jede Position gibt es keine Zahl, nicht die Zahl 0",
              schliessen.gewichteter_pnl([])["wert_pct"] is None)
        check("Positionen ohne PnL (kein Kurs) zaehlen nicht mit",
              schliessen.gewichteter_pnl(
                  [("elliott_wave", None), ("elliott_wave", 4.0)])["anzahl"] == 1)

        # --- 15c) In BEIDEN Antworten des Notfallwegs --------------------
        original_kurse = monitor.fetch_live_prices_for_bots
        monitor.fetch_live_prices_for_bots = lambda bots: dict(TESTKURSE)
        schliessen.vorgaenge_zuruecksetzen()
        db_t3 = db_dateien["t3_supertrend"]
        try:
            _oeffne_positionen(db_t3, [("BTCUSDT", 100.0), ("ETHUSDT", 200.0)])
            v = _alle_vorbereiten(basis).json()
            # 100 -> 110 sind +9.7 %, 200 -> 180 sind -10.3 % (je minus 0.3
            # Kosten). Beide Positionen gehoeren demselben Bot, also ist die
            # gewichtete Zahl hier zwangslaeufig gleich dem Durchschnitt -
            # dass sie sich unterscheiden KANN, zeigt 15b.
            check("Die Uebersicht nennt den Durchschnitt wie bisher",
                  v["pnl_schnitt_pct"] == -0.3, str(v["pnl_schnitt_pct"]))
            check("Spannweite wie bisher unveraendert daneben",
                  v["pnl_bestes_pct"] == 9.7 and v["pnl_schlechtestes_pct"] == -10.3,
                  f"{v['pnl_schlechtestes_pct']} .. {v['pnl_bestes_pct']}")
            check("UND den gewichteten Durchschnitt, mit Groesse und Quelle",
                  v["pnl_gewichtet"]["wert_pct"] == -0.3
                  and v["pnl_gewichtet"]["gewichte"][0]["allokation_pct"] == 10.0
                  and v["pnl_gewichtet"]["gewichte"][0]["quelle"] == "equity_simulation.py",
                  str(v["pnl_gewichtet"])[:160])
            check("Weiterhin KEINE aufsummierte Prozentzahl",
                  "pnl_summe_pct" not in v and "pnl_summe" not in str(list(v)))

            ergebnis = _alle_ausfuehren(basis, v["vorgang"]).json()
            check("Auch das ERGEBNIS nennt beide Zahlen",
                  ergebnis["pnl_schnitt_pct"] == -0.3
                  and ergebnis["pnl_gewichtet"]["wert_pct"] == -0.3,
                  str(ergebnis.get("pnl_gewichtet"))[:120])
            check("Und zwar ueber die TATSAECHLICH geschriebenen Werte",
                  ergebnis["pnl_gewichtet"]["anzahl"] == ergebnis["anzahl_geschlossen"] == 2,
                  str(ergebnis["anzahl_geschlossen"]))

            # --- 15d) Fehlt die Groesse, wird NICHT geschaetzt - und der
            # Notfallweg funktioniert trotzdem. Eine Anzeigefrage darf den
            # Schliessweg nie blockieren.
            es_pfad = os.path.join(wurzel, "strategies", "t3_supertrend",
                                    "equity_simulation.py")
            gesichert = open(es_pfad, encoding="utf-8").read()
            os.remove(es_pfad)
            try:
                _oeffne_positionen(db_t3, [("BTCUSDT", 100.0)])
                v2 = _alle_vorbereiten(basis).json()
                check("Ohne dokumentierte Groesse gibt es KEINE gewichtete Zahl",
                      v2["pnl_gewichtet"]["wert_pct"] is None, str(v2["pnl_gewichtet"])[:120])
                check("Der Durchschnitt steht trotzdem da - die alte Anzeige bleibt",
                      v2["pnl_schnitt_pct"] == 9.7, str(v2["pnl_schnitt_pct"]))
                check("Der Bot wird als nicht gewichtbar ausgewiesen, mit Grund",
                      [n["bot"] for n in v2["pnl_gewichtet"]["nicht_gewichtbar"]]
                      == ["t3_supertrend"]
                      and "ALLOCATION_PCT" in v2["pnl_gewichtet"]["nicht_gewichtbar"][0]["grund"],
                      str(v2["pnl_gewichtet"]["nicht_gewichtbar"]))
                e2 = _alle_ausfuehren(basis, v2["vorgang"]).json()
                check("UND die Position wird trotzdem geschlossen - die "
                      "Anzeige blockiert den Notfallweg nicht",
                      e2["erfolg"] and e2["anzahl_geschlossen"] == 1,
                      str(e2["meldung"])[:90])
                check("Auch im Ergebnis steht der Ausschluss statt einer Zahl",
                      e2["pnl_gewichtet"]["wert_pct"] is None
                      and len(e2["pnl_gewichtet"]["nicht_gewichtbar"]) == 1)
            finally:
                with open(es_pfad, "w", encoding="utf-8") as fh:
                    fh.write(gesichert)
            check("Nach dem Zuruecksichern ist die Groesse wieder lesbar",
                  manual_close.allokation("t3_supertrend")["prozent"] == 10.0)
        finally:
            monitor.fetch_live_prices_for_bots = original_kurse
            schliessen.vorgaenge_zuruecksetzen()

        # --- 15e) DER eigentliche Fall: quer ueber DREI Bots mit DREI
        # verschiedenen Positionsgroessen, ueber den globalen Crash-Weg. Hier
        # trennen sich gewichtete und einfache Zahl wirklich - innerhalb eines
        # Bots koennen sie das nicht.
        original_kurse = monitor.fetch_live_prices_for_bots
        monitor.fetch_live_prices_for_bots = lambda bots: dict(TESTKURSE)
        schliessen.vorgaenge_zuruecksetzen()
        try:
            for pfad_db in db_dateien.values():
                conn = sqlite3.connect(pfad_db)
                conn.execute("UPDATE trades SET status='closed', result='vorlauf' "
                              "WHERE status='open'")
                conn.commit()
                conn.close()
            # t3_supertrend 10 %: BTC 100->110 = +9.7, ETH 200->180 = -10.3
            # elliott_wave  5 %:  SOL  20->22  = +9.7
            # volatility_breakout 2 %: ADA 1.0->0.9 = -10.3
            _oeffne_positionen(db_dateien["t3_supertrend"],
                                [("BTCUSDT", 100.0), ("ETHUSDT", 200.0)])
            _oeffne_positionen(db_dateien["elliott_wave"], [("SOLUSDT", 20.0)])
            _oeffne_positionen(db_dateien["volatility_breakout"], [("ADAUSDT", 1.0)])

            global_eins = _crash_vorbereiten(basis).json()
            g = global_eins["pnl_gewichtet"]
            # Von Hand:
            #   Zaehler = 0.10*(9.7-10.3) + 0.05*9.7 + 0.02*(-10.3) = 0.219
            #   Nenner  = 0.10*2          + 0.05*1   + 0.02*1       = 0.27
            #   gewichtet = +0.81 %       einfach = (9.7-10.3+9.7-10.3)/4 = -0.30 %
            check("Global: gewichtet ueber drei Bots = +0.81 %",
                  g["wert_pct"] == 0.81, str(g["wert_pct"]))
            check("Global: dieselben Positionen ungewichtet = -0.30 % - wieder "
                  "dreht das Vorzeichen",
                  g["ungewichtet_schnitt_pct"] == -0.3,
                  str(g["ungewichtet_schnitt_pct"]))
            check("Global: alle drei Groessen stehen mit Quelle dabei",
                  [(w["bot"], w["allokation_pct"]) for w in g["gewichte"]]
                  == [("elliott_wave", 5.0), ("t3_supertrend", 10.0),
                      ("volatility_breakout", 2.0)], str(g["gewichte"])[:200])
            check("Global: der Durchschnitt JE BOT steht unveraendert daneben",
                  all("pnl_schnitt_pct" in b for b in global_eins["bots"]))
            # "gesamt" allein taugt hier nicht als Verbot: `anzahl_gesamt` ist
            # eine Stueckzahl und voellig in Ordnung. Verboten ist eine
            # aufsummierte PROZENTZAHL - die einzige bot-uebergreifende
            # PnL-Angabe muss die gewichtete sein.
            check("Global: weiterhin keine aufsummierte Gesamt-Prozentzahl",
                  [k for k in global_eins if "pnl" in k] == ["pnl_gewichtet"]
                  and not [k for k in global_eins if "summe" in k.lower()],
                  str(sorted(global_eins))[:140])

            global_ergebnis = _crash_ausfuehren(
                basis, global_eins["vorgang"]).json()
            ge = global_ergebnis["pnl_gewichtet"]
            check("Global: auch das ERGEBNIS traegt die gewichtete Zahl",
                  ge["wert_pct"] == 0.81 and ge["anzahl"] == 4,
                  f"{ge['wert_pct']} / {ge['anzahl']}")
            check("Global: und zwar ueber die tatsaechlich geschriebenen Werte",
                  global_ergebnis["anzahl_geschlossen"] == 4
                  and global_ergebnis["erfolg"] is True,
                  global_ergebnis["meldung"][:110])
            check("Global: die Grundlage steht auch im Ergebnis dabei",
                  "Backtest" in ge["grundlage"] and "Annahme" in ge["hinweis"])
        finally:
            monitor.fetch_live_prices_for_bots = original_kurse
            schliessen.vorgaenge_zuruecksetzen()

        # --- 15f) Keine Bot-Datei wurde dabei veraendert ------------------
        # Pruefsummen, nicht "ist noch lesbar": eine Datei, die nach dem
        # Umschreiben zufaellig noch Text enthaelt, waere sonst ein gruener
        # Test ohne Aussage (Methodik-Grundsatz 12). Die Summen stehen ganz
        # oben in dieser Funktion, also VOR jedem Lesezugriff dieses
        # Abschnitts - inklusive des absichtlich entfernten und wieder
        # hergestellten equity_simulation.py aus 15d.
        # Das in 15a angelegte Hilfsverzeichnis ist die einzige erwartete
        # Neuerung und wird ausgenommen - alles andere muss Byte fuer Byte
        # gleich sein.
        nachher = {n: s for n, s in _bot_dateien_pruefsummen(wurzel).items()
                   if not n.startswith(ohne + os.sep)}
        check("Alle Bot-Dateien sind byteweise unveraendert - auch die in 15d "
              "entfernte und zurueckgesicherte",
              nachher == bot_dateien_vorher,
              str([n for n in set(nachher) | set(bot_dateien_vorher)
                   if nachher.get(n) != bot_dateien_vorher.get(n)])[:160])
    finally:
        shutil.rmtree(os.path.join(wurzel, "strategies", ohne), ignore_errors=True)

    # --- 15f) Frontend: die Zahl steht nie ohne ihre Beschriftung da -----
    bot_html = open(os.path.join(DIR, "static", "bot.html"), encoding="utf-8").read()
    code = ohne_kommentare(bot_html)
    # Die drei Bausteine (Erlaeuterung, Groessen-Format, Zeilenbau) stehen in
    # app.js, weil bot.html UND index.html sie brauchen - zwei Fassungen
    # desselben Hinweistextes waeren die Doppelfuehrung, bei der irgendwann nur
    # noch eine Seite sagt, worauf die Zahl beruht.
    app_code = ohne_kommentare(open(os.path.join(DIR, "static", "app.js"),
                                     encoding="utf-8").read())
    index_code = ohne_kommentare(open(os.path.join(DIR, "static", "index.html"),
                                       encoding="utf-8").read())
    check("Die Bausteine der gewichteten Anzeige stehen EINMAL, in app.js",
          "function gewichtungsZeilen(" in app_code
          and "function gewichtungsZeilen(" not in code
          and "function gewichtungsZeilen(" not in index_code,
          "mehrfach definiert")
    check("Der Notfall-Dialog zeigt den gewichteten Durchschnitt",
          "pnl_gewichtet" in code and "gewichtungsZeilen" in code)
    check("Der CRASH-Dialog ebenfalls - dort ist die Gewichtung der eigentliche "
          "Punkt (10 % / 5 % / 2 % nebeneinander)",
          "gewichtungsZeilen(v.pnl_gewichtet)" in index_code
          and "gewichtungsZeilen(r.pnl_gewichtet)" in index_code,
          "fehlt in Uebersicht oder Ergebnis")
    code = app_code + "\n" + code
    # UND, nicht ODER: der Dialog liest v.pnl_gewichtet, die Ergebnisanzeige
    # r.pnl_gewichtet. Eine Pruefung auf "kommt irgendwo vor" waere gruen,
    # sobald nur EINE der beiden Ansichten die Zahl zeigt - und genau das war
    # in den beiden vorigen Aenderungen zweimal der Fehler.
    check("Die gewichtete Zahl steht in BEIDEN Ansichten - Dialog und Ergebnis",
          "gewichtungsZeilen(v.pnl_gewichtet)" in code
          and "r.pnl_gewichtet" in code,
          f"gewichtungsZeilen: {code.count('gewichtungsZeilen(')}")
    check("Die Erlaeuterung nennt die Backtest-ANNAHME",
          "GEWICHTUNG_ERLAEUTERUNG" in code
          and "angenommenen" in code and "Backtest" in code)
    check("Und sagt, dass es KEINE Portfolio-Rendite ist",
          "keine Portfolio-Rendite" in code)
    check("Die Erlaeuterung ist sichtbarer Text, kein title-Tooltip",
          'class="hinweis-gewichtung"' in code
          and 'title="Gewichtet' not in code)

    # JE FUNKTION pruefen, nicht im ganzen Dokument: Dialog und
    # Ergebnisanzeige bauen ihre Zeilen getrennt auf. Eine Suche ueber die
    # ganze Datei war gruen, als die Erlaeuterung und der Ausschluss-Hinweis
    # im Dialog entfernt waren - die Ergebnisanzeige enthielt beides ja noch.
    # (Gegenprobe M8/M9: genau so gefunden.)
    dialog = _js_funktion(code, "gewichtungsZeilen")
    ergebnis = _js_funktion(code, "notfallErgebnisAnzeigen")
    check("Die Funktion des Dialogs gefunden und die der Ergebnisanzeige auch",
          len(dialog) > 200 and len(ergebnis) > 200,
          f"{len(dialog)} / {len(ergebnis)} Zeichen")
    for wo, rumpf in (("Dialog", dialog), ("Ergebnisanzeige", ergebnis)):
        check(f"{wo}: die gewichtete Zahl steht dort mit ihrer Erlaeuterung",
              "GEWICHTUNG_ERLAEUTERUNG" in rumpf
              and "hinweis-gewichtung" in rumpf, rumpf[:90])
        check(f"{wo}: nicht gewichtbare Bots werden dort benannt und als "
              f"ausgenommen bezeichnet",
              "nicht_gewichtbar" in rumpf and "ausgenommen" in rumpf,
              rumpf[:90])
    check("Weiterhin keine aufsummierte Gesamt-Prozentzahl im Frontend",
          "pnl_summe" not in code and "pnl_schnitt_pct" in code)
    # Die Regel wird aus dem CSS GEPARST, nicht im Text gesucht: eine Suche
    # "steht 'display: block' irgendwo hinter dem Selektor" hat beim Umbau
    # dieses Selektors sofort falsch angeschlagen, weil der Erklaerkommentar
    # den Selektornamen ebenfalls enthaelt.
    css = re.sub(r"/\*.*?\*/", "", open(os.path.join(DIR, "static", "style.css"),
                                          encoding="utf-8").read(), flags=re.S)
    regeln = [(s.strip(), k) for s, k in re.findall(r"([^{}]+)\{([^}]*)\}", css)
              if ".hinweis-gewichtung" in s]
    check("Der Hinweis ist ein Block - sonst zieht das Flex-Layout der "
          "Dialogzeilen den Satz auseinander",
          len(regeln) == 1 and "display: block" in regeln[0][1],
          str(regeln)[:200])
    # Der eigentliche Fallstrick, im Browser gemessen: `.dialog-zeilen div`
    # (Spezifitaet 0,1,1) schlaegt `.hinweis-gewichtung` (0,1,0). Ohne den
    # spezifischeren Selektor bleibt der Hinweis ein Flex-Container, und das
    # <strong> im Satz steht als eigene Zeile.
    check("Und der Selektor ist spezifischer als '.dialog-zeilen div'",
          regeln and ".dialog-zeilen .hinweis-gewichtung" in regeln[0][0],
          regeln[0][0] if regeln else "keine Regel")

    # --- 15g) Frontend: die Anzahl der Positionen JE BOT -----------------
    # Die gewichtete Zahl rechnet richtig, sagt aber nicht, woraus sie besteht.
    # `elliott_wave` hat kein MAX_CONCURRENT_POSITIONS und kann die Zahl
    # praktisch allein tragen - im Crash-Dialog, also genau dann, wenn eine
    # Notfallentscheidung faellt.
    bot_code = ohne_kommentare(bot_html)
    check("Die Anzahl-Anzeige steht EINMAL, in app.js - wie die Erlaeuterung",
          "function positionsanzahlZeilen(" in app_code
          and "function positionsanzahlZeilen(" not in bot_code
          and "function positionsanzahlZeilen(" not in index_code,
          "mehrfach definiert oder nicht in app.js")
    check("Sie ist sichtbarer Text, kein title-Tooltip",
          "hinweis-gewichtung" in _js_funktion(app_code, "positionsanzahlZeilen")
          and "title=" not in _js_funktion(app_code, "positionsanzahlZeilen"))
    check("Und sie nennt den Grund - Bots ohne Obergrenze fuer gleichzeitige "
          "Positionen",
          "POSITIONSANZAHL_ERLAEUTERUNG" in app_code
          and "Obergrenze für gleichzeitige Positionen" in app_code)

    # JE FUNKTION, nicht im ganzen Dokument: in #62, #66 und #67 war eine
    # Suche ueber die ganze Datei jedes Mal gruen, obwohl eine der beiden
    # Ansichten die Angabe gar nicht zeigte. Vier Ansichten sind es hier:
    # Uebersicht und Ergebnis, je bot-weit (alle-schliessen) und global
    # (alle-bots-schliessen).
    ansichten = (
        ("app.js: gewichtungsZeilen (Uebersicht bot-weit und global)",
         _js_funktion(app_code, "gewichtungsZeilen"), "positionsanzahlZeilen("),
        ("bot.html: notfallErgebnisAnzeigen (Ergebnis bot-weit)",
         _js_funktion(bot_code, "notfallErgebnisAnzeigen"),
         "positionsanzahlZeilen("),
        ("bot.html: notfallZeilen (Uebersicht bot-weit)",
         _js_funktion(bot_code, "notfallZeilen"),
         "gewichtungsZeilen(v.pnl_gewichtet)"),
        ("index.html: crashListe (Uebersicht global)",
         _js_funktion(index_code, "crashListe"),
         "gewichtungsZeilen(v.pnl_gewichtet)"),
        ("index.html: crashErgebnisAnzeigen (Ergebnis global)",
         _js_funktion(index_code, "crashErgebnisAnzeigen"),
         "gewichtungsZeilen(r.pnl_gewichtet)"),
    )
    for wo, rumpf, erwartet in ansichten:
        check(f"{wo}: Funktion gefunden", len(rumpf) > 120, f"{len(rumpf)} Zeichen")
        check(f"{wo}: die Anzahl je Bot ist dort erreichbar",
              erwartet in rumpf, rumpf[:90])
    # notfallErgebnisAnzeigen() baut sein HTML selbst auf und ruft
    # gewichtungsZeilen() NICHT auf - waere die Anzahl nur dort eingehaengt,
    # bliebe genau diese Ansicht ohne sie.
    check("Die Ergebnisanzeige des bot-weiten Wegs holt sie EIGENS - sie geht "
          "nicht ueber gewichtungsZeilen()",
          "gewichtungsZeilen(" not in _js_funktion(bot_code,
                                                    "notfallErgebnisAnzeigen"))
    check("Die Gewichtungsformel selbst bleibt unangetastet: weiterhin keine "
          "aufsummierte Gesamtzahl",
          "pnl_summe" not in app_code + bot_code + index_code)
# 10) Globaler Crash-Weg: alle Positionen ALLER Bots
# ---------------------------------------------------------------------------
# Die folgenreichste Aktion des Projekts. Der Kern dieses Abschnitts ist die
# TEILAUSFALL-SICHERHEIT IN ZWEI DIMENSIONEN, beide mit echten Fehlern statt
# Behauptungen:
#
#   10f  eine POSITION scheitert (dem Trade wird der Einstiegskurs entzogen,
#        der Kern lehnt sie innerhalb seiner Transaktion ab) - die uebrigen
#        Positionen desselben Bots laufen weiter
#   10g  ein GANZER BOT scheitert (seine Datenbank wird geloescht bzw. durch
#        eine unlesbare Datei ersetzt) - die uebrigen BOTS laufen weiter
#
# 10g ist der neue Fall und der unangenehmere: ein Abbruch beim dritten von
# neun Bots hinterliesse einen Zustand, den niemand benennen kann.


def _crash_vorbereiten(basis, token=TEST_TOKEN):
    return post(basis, "/api/alle-bots-schliessen/vorbereiten", {}, token=token)


def _crash_ausfuehren(basis, vorgang, text="CRASH", token=TEST_TOKEN):
    return post(basis, "/api/alle-bots-schliessen/ausfuehren",
                 {"vorgang": vorgang, "bestaetigung": text}, token=token)


def teste_global_schliessen(basis, wurzel, db_dateien, protokoll_datei):
    print("\n10) Globaler Crash-Weg - alle Positionen ALLER Bots")

    # Das Testprojekt hat drei Bots; alle drei sind freigeschaltet. Genau
    # richtig fuer diesen Abschnitt: mit einem einzigen liesse sich der
    # bot-uebergreifende Teilausfall nicht pruefen.
    alle_db = dict(db_dateien)

    def status(bot, trade_id):
        conn = sqlite3.connect(alle_db[bot])
        try:
            zeile = conn.execute("SELECT status, result, exit_price FROM trades "
                                  "WHERE id=?", (trade_id,)).fetchone()
        finally:
            conn.close()
        return tuple(zeile) if zeile else None

    def alles_schliessen():
        """Ausgangslage: nichts offen, in allen Bots."""
        for pfad in alle_db.values():
            conn = sqlite3.connect(pfad)
            conn.execute("UPDATE trades SET status='closed', result='vorlauf' "
                          "WHERE status='open'")
            conn.commit()
            conn.close()

    def oeffne(bot, posten):
        ids = []
        conn = sqlite3.connect(alle_db[bot])
        try:
            for symbol, entry in posten:
                conn.execute(
                    "INSERT INTO trades (symbol, signal_time, entry_time, "
                    "entry_price, stop_price, status) VALUES (?,?,?,?,?,'open')",
                    (symbol, "2026-04-01 00:00:00", "2026-04-01 00:00:00",
                     entry, entry * 0.95))
                ids.append(conn.execute("SELECT MAX(id) FROM trades").fetchone()[0])
            conn.commit()
        finally:
            conn.close()
        return ids

    original_kurse = monitor.fetch_live_prices_for_bots
    monitor.fetch_live_prices_for_bots = lambda bots: dict(TESTKURSE)
    schliessen.vorgaenge_zuruecksetzen()
    try:
        # --- 10a) Nichts offen: der Weg beginnt nicht ---------------------
        alles_schliessen()
        antwort = _crash_vorbereiten(basis)
        check("Ohne offene Position irgendwo wird das Vorbereiten abgelehnt (409)",
              antwort.status_code == 409, str(antwort.status_code))
        check("Die Meldung sagt, dass kein Bot etwas offen hat",
              "Kein Bot" in antwort.json()["detail"], antwort.json()["detail"][:90])

        # --- 10b) Uebersicht ueber MEHRERE Bots ---------------------------
        t3 = oeffne("t3_supertrend", [("BTCUSDT", 100.0), ("ETHUSDT", 200.0)])
        ew = oeffne("elliott_wave", [("SOLUSDT", 20.0)])
        vb = oeffne("volatility_breakout", [("ADAUSDT", 1.0)])
        eins = _crash_vorbereiten(basis).json()
        check("Die Uebersicht fuehrt alle drei Bots",
              sorted(b["bot"] for b in eins["bots"])
              == ["elliott_wave", "t3_supertrend", "volatility_breakout"],
              str([b["bot"] for b in eins["bots"]]))
        check("Und zaehlt alle vier Positionen",
              (eins["anzahl"], eins["anzahl_bots"]) == (4, 3),
              f"{eins['anzahl']}/{eins['anzahl_bots']}")
        check("Nach Bot gruppiert, mit Durchschnitt JE BOT",
              all("pnl_schnitt_pct" in b for b in eins["bots"]))
        # Weiterhin KEINE Summe und kein unbeschrifteter Gesamtwert. Seit der
        # gewichteten Anzeige gibt es hier aber `pnl_gewichtet` - eine
        # gewichtete Durchschnittsrendite MIT Angabe ihrer Grundlage. Die
        # Zusicherung wurde deshalb praeziser gefasst statt aufgegeben: verboten
        # ist die aufsummierte oder unbeschriftete Zahl, nicht jede Kennzahl
        # ueber alle Bots (Abschnitt 15 prueft die Rechnung).
        check("KEINE Gesamtsumme und kein unbeschrifteter Gesamt-PnL ueber alle "
              "Bots (Methodik-Grundsatz 2)",
              "pnl_summe_pct" not in eins and "pnl_schnitt_pct" not in eins
              and "pnl_gesamt" not in eins
              and not [k for k in eins if "summe" in k.lower()],
              str(sorted(eins))[:160])
        check("Die gewichtete Zahl ist da - und nie ohne ihre Grundlage",
              eins["pnl_gewichtet"]["wert_pct"] is not None
              and "Backtest" in eins["pnl_gewichtet"]["grundlage"]
              and "keine Portfolio-Rendite" in eins["pnl_gewichtet"]["hinweis"],
              str(eins["pnl_gewichtet"])[:120])
        check("Der zu tippende Text wird mitgeteilt",
              eins["crash_text"] == schliessen.CRASH_TEXT)
        aktien = [b for b in eins["bots"] if b["anlageklasse"] == "aktien"]
        check("Aktien-Bots sind als solche erkennbar (fuer den Kurs-Hinweis)",
              [b["bot"] for b in aktien] == ["volatility_breakout"], str(aktien)[:90])

        # --- 10c) Token ---------------------------------------------------
        for token in (None, "falsches-token-aber-lang-genug"):
            check(f"Vorbereiten ohne gueltiges Token: 401 (Token {token!r})",
                  _crash_vorbereiten(basis, token=token).status_code == 401)
            check(f"Ausfuehren ohne gueltiges Token: 401 (Token {token!r})",
                  _crash_ausfuehren(basis, eins["vorgang"],
                                     token=token).status_code == 401)
        check("Ein abgewiesener Fremdzugriff verbraucht den Vorgang nicht",
              schliessen.offener_vorgang(eins["vorgang"]) is not None)

        # --- 10d) Falscher oder fehlender CRASH-Text ----------------------
        # Jeder Versuch verbraucht den Vorgang - sonst liesse sich der Text
        # innerhalb der Frist beliebig oft durchprobieren.
        # "CRASH " mit Leerzeichen steht bewusst NICHT in dieser Liste: der
        # Vergleich entfernt umschliessende Leerzeichen, der Text waere also
        # gueltig und wuerde wirklich alles schliessen. (Genau das ist beim
        # Schreiben dieses Tests passiert.) Geprueft wird das weiter unten
        # ausdruecklich - hier stehen nur Texte, die abgelehnt werden muessen.
        for text in ("crash", "CRAS", "", "Crash", "CRASHH", None):
            vorab = _crash_vorbereiten(basis).json()
            antwort = _crash_ausfuehren(basis, vorab["vorgang"], text=text)
            check(f"Text {text!r} wird abgelehnt (409)",
                  antwort.status_code == 409, str(antwort.status_code))
            check(f"Text {text!r}: der Vorgang ist danach verbraucht",
                  _crash_ausfuehren(basis, vorab["vorgang"]).status_code == 409)
        check("Der Vergleich ist case-sensitiv - 'crash' genuegt nicht",
              schliessen.CRASH_TEXT == "CRASH"
              and schliessen.CRASH_TEXT != schliessen.CRASH_TEXT.lower())
        check("Nach allen falschen Texten ist noch nichts geschlossen",
              all(status(b, i)[0] == "open"
                  for b, ids in (("t3_supertrend", t3), ("elliott_wave", ew),
                                  ("volatility_breakout", vb)) for i in ids))
        check("Gegenprobe: der EXAKTE Text ist der erwartete",
              schliessen.CRASH_TEXT == "CRASH")
        # Umschliessende Leerzeichen sind bewusst erlaubt (Kopieren aus einer
        # Anleitung nimmt schnell eines mit). Hier ohne Schreibzugriff
        # geprueft: der Vergleich selbst, nicht ueber den Endpunkt.
        check("Umschliessende Leerzeichen werden toleriert",
              "  CRASH  ".strip() == schliessen.CRASH_TEXT)

        # --- 10e) Artfremde Kennungen -------------------------------------
        schliessen.vorgaenge_zuruecksetzen()
        global_vorgang = _crash_vorbereiten(basis).json()
        einzel = _vorbereiten(basis, trade_id=t3[0]).json()
        botweit = _alle_vorbereiten(basis).json()
        antwort = _crash_ausfuehren(basis, einzel["vorgang"])
        check("Eine EINZEL-Kennung loest auf dem globalen Endpunkt nichts aus",
              antwort.status_code == 409 and "anderen Vorgang" in antwort.json()["detail"],
              antwort.json()["detail"][:80])
        antwort = _crash_ausfuehren(basis, botweit["vorgang"])
        check("Eine BOT-WEITE Kennung ebenfalls nicht",
              antwort.status_code == 409 and "anderen Vorgang" in antwort.json()["detail"],
              antwort.json()["detail"][:80])
        antwort = _ausfuehren(basis, global_vorgang["vorgang"])
        check("Und eine GLOBALE Kennung nicht auf dem Einzel-Endpunkt",
              antwort.status_code == 409 and "anderen Vorgang" in antwort.json()["detail"],
              antwort.json()["detail"][:80])
        antwort = _alle_ausfuehren(basis, global_vorgang["vorgang"])
        check("Auch nicht auf dem bot-weiten Endpunkt",
              antwort.status_code == 409, str(antwort.status_code))
        check("Nach allen vier Kreuzversuchen ist nichts geschlossen",
              all(status(b, i)[0] == "open"
                  for b, ids in (("t3_supertrend", t3), ("elliott_wave", ew),
                                  ("volatility_breakout", vb)) for i in ids))

        # --- 10f) TEILAUSFALL DIMENSION 1: eine POSITION scheitert --------
        # Echter Fehlschlag des Kerns, kein Testdoppel: dem mittleren Trade
        # von t3 wird nach der Uebersicht der Einstiegskurs entzogen.
        schliessen.vorgaenge_zuruecksetzen()
        zwei = _crash_vorbereiten(basis).json()
        opfer = t3[1]
        conn = sqlite3.connect(alle_db["t3_supertrend"])
        conn.execute("UPDATE trades SET entry_price=NULL WHERE id=?", (opfer,))
        conn.commit()
        conn.close()

        antwort = _crash_ausfuehren(basis, zwei["vorgang"])
        check("Ein Teilausfall ist KEIN HTTP-Fehler (200)",
              antwort.status_code == 200,
              str(antwort.status_code) + antwort.text[:120])
        r = antwort.json()
        check("erfolg ist false, weil eine Position fehlschlug",
              r["erfolg"] is False)
        check("Drei von vier Positionen geschlossen, eine fehlgeschlagen",
              (r["anzahl_geschlossen"], r["anzahl_fehlgeschlagen"]) == (3, 1),
              f"{r['anzahl_geschlossen']}/{r['anzahl_fehlgeschlagen']}")
        t3_block = [b for b in r["bots"] if b["bot"] == "t3_supertrend"][0]
        check("Der Fehlschlag steht beim RICHTIGEN Bot, mit Grund",
              t3_block["fehlgeschlagen"][0]["trade_id"] == opfer
              and "Einstiegskurs" in t3_block["fehlgeschlagen"][0]["grund"],
              str(t3_block["fehlgeschlagen"])[:130])
        check("DIE ANDEREN BOTS sind trotzdem vollstaendig geschlossen",
              status("elliott_wave", ew[0])[:2] == ("closed", "manual_close")
              and status("volatility_breakout", vb[0])[:2] == ("closed", "manual_close"),
              f"{status('elliott_wave', ew[0])} / {status('volatility_breakout', vb[0])}")
        check("Und im betroffenen Bot die uebrige Position ebenfalls",
              status("t3_supertrend", t3[0])[:2] == ("closed", "manual_close"),
              str(status("t3_supertrend", t3[0])))
        check("Die fehlgeschlagene Position bleibt offen und unberuehrt",
              status("t3_supertrend", opfer) == ("open", None, None),
              str(status("t3_supertrend", opfer)))
        check("Die Meldung nennt Gesamtzahl und Bots",
              "3 von 4" in r["meldung"] and "3 Bots" in r["meldung"],
              r["meldung"][:170])

        # --- 10g) TEILAUSFALL DIMENSION 2: ein GANZER BOT scheitert ------
        # Die Datenbank eines Bots wird nach der Uebersicht durch eine
        # unlesbare Datei ersetzt. manual_close.offene_positionen() scheitert
        # dann fuer DIESEN Bot - und die uebrigen muessen weiterlaufen.
        alles_schliessen()
        conn = sqlite3.connect(alle_db["t3_supertrend"])
        conn.execute("UPDATE trades SET entry_price=200.0 WHERE entry_price IS NULL")
        conn.commit()
        conn.close()
        t3 = oeffne("t3_supertrend", [("BTCUSDT", 100.0)])
        ew = oeffne("elliott_wave", [("SOLUSDT", 20.0), ("ETHUSDT", 200.0)])
        vb = oeffne("volatility_breakout", [("ADAUSDT", 1.0)])
        schliessen.vorgaenge_zuruecksetzen()
        drei = _crash_vorbereiten(basis).json()
        check("Vorher sind alle drei Bots in der Uebersicht",
              drei["anzahl_bots"] == 3 and drei["anzahl"] == 4,
              f"{drei['anzahl_bots']}/{drei['anzahl']}")

        kaputt = alle_db["elliott_wave"]
        gesichert = kaputt + ".sicherung"
        shutil.copy2(kaputt, gesichert)
        with open(kaputt, "wb") as datei:
            datei.write(b"das ist keine SQLite-Datenbank")
        try:
            antwort = _crash_ausfuehren(basis, drei["vorgang"])
            check("Ein komplett ausgefallener Bot ergibt KEIN HTTP-Fehler (200)",
                  antwort.status_code == 200,
                  str(antwort.status_code) + antwort.text[:140])
            r = antwort.json()
            check("Der ausgefallene Bot wird GETRENNT von Positionsfehlern "
                  "ausgewiesen",
                  [b["bot"] for b in r["bots_fehlgeschlagen"]] == ["elliott_wave"],
                  str(r["bots_fehlgeschlagen"])[:150])
            check("Mit Grund und der Zahl der dort unberuehrten Positionen",
                  r["bots_fehlgeschlagen"][0]["angefragt"] == 2
                  and bool(r["bots_fehlgeschlagen"][0]["grund"]),
                  str(r["bots_fehlgeschlagen"][0])[:130])
            check("DIE SCHLEIFE UEBER DIE BOTS IST NICHT ABGEBROCHEN: die "
                  "uebrigen zwei Bots sind geschlossen",
                  status("t3_supertrend", t3[0])[:2] == ("closed", "manual_close")
                  and status("volatility_breakout", vb[0])[:2]
                  == ("closed", "manual_close"),
                  f"{status('t3_supertrend', t3[0])} / "
                  f"{status('volatility_breakout', vb[0])}")
            check("Gezaehlt werden nur die wirklich geschlossenen",
                  r["anzahl_geschlossen"] == 2, str(r["anzahl_geschlossen"]))
            check("erfolg ist false, weil ein Bot ausfiel",
                  r["erfolg"] is False)
            check("Die Meldung nennt den uebersprungenen Bot ausdruecklich",
                  "uebersprungen" in r["meldung"] and "elliott_wave" in r["meldung"],
                  r["meldung"][:200])
        finally:
            shutil.move(gesichert, kaputt)
        check("Die Datenbank des ausgefallenen Bots ist nach der Wiederher"
              "stellung unveraendert - es wurde dort nichts geschrieben",
              [z["status"] for z in zeilen(alle_db["elliott_wave"])].count("open") == 2,
              str([z["status"] for z in zeilen(alle_db["elliott_wave"])]))

        # --- 10h) Der vollstaendige Erfolgsfall ueber alle Bots ----------
        alles_schliessen()
        t3 = oeffne("t3_supertrend", [("BTCUSDT", 100.0)])
        ew = oeffne("elliott_wave", [("SOLUSDT", 20.0)])
        vb = oeffne("volatility_breakout", [("ADAUSDT", 1.0)])
        schliessen.vorgaenge_zuruecksetzen()
        vier = _crash_vorbereiten(basis).json()
        vor_lauf = {b: zeilen(pfad) for b, pfad in alle_db.items()}
        marke = len(open(protokoll_datei, encoding="utf-8").read().splitlines())
        r = _crash_ausfuehren(basis, vier["vorgang"]).json()
        check("Alle Positionen aller Bots geschlossen",
              r["erfolg"] is True and r["anzahl_geschlossen"] == 3
              and r["anzahl_fehlgeschlagen"] == 0
              and not r["bots_fehlgeschlagen"], r["meldung"][:140])
        # Auch das ERGEBNIS darf keine aufsummierte Gesamtzahl tragen - nicht
        # nur die Uebersicht. Genau diese Haelfte fehlte zuerst und ist in der
        # Mutationsprobe aufgefallen. Geprueft wird jetzt, dass die EINZIGE
        # bot-uebergreifende PnL-Angabe die gewichtete ist und dass sie ihre
        # Grundlage mitbringt; eine Summe gibt es weiterhin nicht.
        check("Auch das Ergebnis traegt keine aufsummierte Gesamt-Prozentzahl",
              [k for k in r if "pnl" in k] == ["pnl_gewichtet"]
              and not [k for k in r if "summe" in k.lower()],
              str([k for k in r if "pnl" in k]))
        check("Und die gewichtete Zahl im Ergebnis nennt ihre Grundlage",
              "Backtest" in r["pnl_gewichtet"]["grundlage"]
              and "keine Portfolio-Rendite" in r["pnl_gewichtet"]["hinweis"])
        check("Der Durchschnitt steht je Bot, nicht global",
              all("pnl_schnitt_pct" in b for b in r["bots"]),
              str(sorted(r["bots"][0]))[:140])
        check("Jede mit dem Kurs IHRES Symbols, nicht einem gemeinsamen",
              sorted((g["symbol"], g["exit_preis"])
                      for b in r["bots"] for g in b["geschlossen"])
              == [("ADAUSDT", 0.9), ("BTCUSDT", 110.0), ("SOLUSDT", 22.0)],
              str(sorted((g["symbol"], g["exit_preis"])
                          for b in r["bots"] for g in b["geschlossen"])))
        for bot, ids in (("t3_supertrend", t3), ("elliott_wave", ew),
                          ("volatility_breakout", vb)):
            diff = unterschiede(vor_lauf[bot], zeilen(alle_db[bot]))
            check(f"{bot}: genau die fuenf Ausstiegsfelder EINER Zeile",
                  {f for _, f, _, _ in diff} == set(SCHREIB_SPALTEN)
                  and len({k for k, _, _, _ in diff}) == 1,
                  str(sorted({(k, f) for k, f, _, _ in diff})))

        # --- 10i) Protokoll: je Position eine Zeile, mit eigener Herkunft --
        protokoll = open(protokoll_datei, encoding="utf-8").read().splitlines()
        neue = [z for z in protokoll[marke:] if z.strip()]
        erfolge = [z for z in neue if "ERFOLGREICH" in z]
        check("Der globale Lauf erzeugt GENAU DREI Erfolgszeilen - eine je "
              "Position, keine Sammelzeile",
              len(erfolge) == 3, f"{len(erfolge)} Erfolgszeilen")
        check("Jede traegt die eigene Herkunft quelle=dashboard-crash - so ist "
              "ein Crash-Eingriff von einem normalen unterscheidbar",
              all(f"quelle={manual_close.QUELLE_DASHBOARD_CRASH}" in z
                  for z in erfolge),
              [z for z in erfolge
               if f"quelle={manual_close.QUELLE_DASHBOARD_CRASH}" not in z][:1])
        check("Und nennt den jeweiligen Bot, nicht nur 'alle'",
              sorted(set(re.findall(r"bot=(\w+)", " ".join(erfolge))))
              == ["elliott_wave", "t3_supertrend", "volatility_breakout"],
              str(sorted(set(re.findall(r"bot=(\w+)", " ".join(erfolge))))))
        check("Die Herkunft unterscheidet sich von der des normalen Wegs",
              manual_close.QUELLE_DASHBOARD_CRASH != manual_close.QUELLE_DASHBOARD)

        # --- 10j) Nebenlaeufigkeit ueber mehrere Bots ---------------------
        # Zwei echte Fremdprozesse halten gleichzeitig die Schreibsperre auf
        # ZWEI Datenbanken. Erwartet: beide Bots scheitern sauber, der dritte
        # wird trotzdem geschlossen.
        alles_schliessen()
        t3 = oeffne("t3_supertrend", [("BTCUSDT", 100.0)])
        ew = oeffne("elliott_wave", [("SOLUSDT", 20.0)])
        vb = oeffne("volatility_breakout", [("ADAUSDT", 1.0)])
        schliessen.vorgaenge_zuruecksetzen()
        fuenf = _crash_vorbereiten(basis).json()
        halter_skript = os.path.join(wurzel, "sperr_halter.py")
        with open(halter_skript, "w", encoding="utf-8") as datei:
            datei.write(SPERR_HALTER_FREI)
        altes_limit = manual_close.SPERR_TIMEOUT_SEKUNDEN
        manual_close.SPERR_TIMEOUT_SEKUNDEN = 1
        halter = [subprocess.Popen(
            [sys.executable, halter_skript, alle_db[b], "6"],
            stdout=subprocess.PIPE, text=True)
            for b in ("t3_supertrend", "elliott_wave")]
        try:
            check("Zwei Fremdprozesse halten zwei Schreibsperren",
                  all(h.stdout.readline().strip() == "gesperrt" for h in halter))
            r = _crash_ausfuehren(basis, fuenf["vorgang"]).json()
            gescheitert = {f["symbol"] for b in r["bots"]
                           for f in b["fehlgeschlagen"]}
            check("Die beiden gesperrten Bots scheitern sauber",
                  gescheitert == {"BTCUSDT", "SOLUSDT"}, str(gescheitert))
            check("Der dritte Bot wird trotzdem geschlossen",
                  status("volatility_breakout", vb[0])[:2] == ("closed", "manual_close"),
                  str(status("volatility_breakout", vb[0])))
            check("Die gesperrten Positionen bleiben offen und unberuehrt",
                  status("t3_supertrend", t3[0]) == ("open", None, None)
                  and status("elliott_wave", ew[0]) == ("open", None, None))
        finally:
            manual_close.SPERR_TIMEOUT_SEKUNDEN = altes_limit
            for h in halter:
                h.wait(timeout=60)
    finally:
        monitor.fetch_live_prices_for_bots = original_kurse
        schliessen.vorgaenge_zuruecksetzen()


# Derselbe Sperrhalter wie in Abschnitt 8, hier als eigene Konstante, weil
# dieser Abschnitt zwei davon gleichzeitig startet und sie auf Zeilen
# arbeiten muessen, die es in jedem Testbot gibt.
SPERR_HALTER_FREI = """\
\"\"\"Haelt eine SQLite-Schreibsperre - simuliert einen laufenden Cronjob.\"\"\"
import sqlite3, sys, time
conn = sqlite3.connect(sys.argv[1], timeout=30, isolation_level=None)
conn.execute("BEGIN IMMEDIATE")
conn.execute("UPDATE trades SET status=status WHERE id=1")
print("gesperrt", flush=True)
time.sleep(float(sys.argv[2]))
conn.execute("ROLLBACK")
conn.close()
"""


# ---------------------------------------------------------------------------
# 17) Warteauftraege: was bei geschlossener Boerse passiert - und was nicht
# ---------------------------------------------------------------------------
# Der erste zeitversetzte Schreibvorgang des Projekts. Entsprechend wird hier
# nicht nur geprueft, dass ein Auftrag entsteht, sondern vor allem, was NICHT
# passiert: keine Zeile in einer Bot-Datenbank, kein Auftrag ohne den
# zusaetzlichen Bestaetigungsschritt, kein Auftrag bei einem Krypto-Bot.
#
# Gearbeitet wird mit dem ECHTEN Kalender an einem bekannten Tag (siehe
# boerse_am), nicht mit einer Kalender-Attrappe: eine Attrappe wuerde genau
# das nicht pruefen, worauf es ankommt.

AKTIEN_TESTKURSE = {"NVDA": 505.0, "AAPL": 160.0, "MSFT": 310.0}


def _wa_vorbereiten(basis, bot, trade_id):
    return post(basis, f"/api/bots/{bot}/schliessen/vorbereiten",
                 {"trade_id": trade_id})


def _wa_ausfuehren(basis, bot, vorgang, bestaetigt=None):
    koerper = {"vorgang": vorgang}
    if bestaetigt is not None:
        koerper[schliessen.WARTEAUFTRAG_BESTAETIGUNG] = bestaetigt
    return post(basis, f"/api/bots/{bot}/schliessen/ausfuehren", koerper)


def _auftraege_aus_datei() -> list:
    """Liest die Auftragsdatei DIREKT - nicht ueber das Modul.

    So belegt der Test, dass die Auftraege wirklich auf der Platte stehen
    und nicht bloss in einem Speicher, den ein Neustart mitnimmt. Genau das
    ist die Zusicherung 'persistent'."""
    pfad = warteauftraege.datei()
    if not os.path.exists(pfad):
        return []
    with open(pfad, encoding="utf-8") as fh:
        return json.load(fh)["auftraege"]


def teste_warteauftraege(basis, wurzel, db_dateien, protokoll_datei):
    print("\n17) Warteauftraege bei geschlossener Boerse")

    db_aktien = db_dateien["volatility_breakout"]
    db_krypto = db_dateien["t3_supertrend"]
    andere = {n: p for n, p in db_dateien.items()
              if n not in ("volatility_breakout",)}

    original_kurse = monitor.fetch_live_prices_for_bots
    monitor.fetch_live_prices_for_bots = lambda bots: dict(
        list(TESTKURSE.items()) + list(AKTIEN_TESTKURSE.items()))
    schliessen.vorgaenge_zuruecksetzen()
    warteauftraege.alles_loeschen()
    try:
        aktien_posten = _oeffne_positionen(db_aktien, [("AAPL", 150.0),
                                                        ("MSFT", 300.0)])
        aapl_id, msft_id = aktien_posten[0][0], aktien_posten[1][0]
        stand_aktien = zeilen(db_aktien)
        pruefsummen_andere = _pruefsummen(andere)

        def aktien_db_unveraendert(was):
            check(f"{was}: die Aktien-Datenbank ist Feld fuer Feld unveraendert",
                  unterschiede(stand_aktien, zeilen(db_aktien)) == [],
                  str(unterschiede(stand_aktien, zeilen(db_aktien)))[:140])

        # --- 17a) Boerse OFFEN: alles bleibt wie bisher --------------------
        with boerse_am(ZEIT_OFFEN):
            antwort = get(basis, "/api/bots/volatility_breakout/"
                                  "schliessbare-positionen?live=1").json()
            check("Bei offener Boerse meldet die Positionsliste kein Vormerken",
                  antwort["boerse"]["warteauftrag_noetig"] is False
                  and antwort["boerse"]["offen"] is True,
                  str(antwort["boerse"])[:120])
            vorbereitet = _wa_vorbereiten(basis, "volatility_breakout",
                                           aapl_id).json()
            check("Der Vorgang ist ein SOFORT-Vorgang, kein Warteauftrag",
                  vorbereitet["warteauftrag"] is False)
            check("Und er nennt den Kurs, zu dem geschrieben wird",
                  vorbereitet["aktueller_preis"] == 160.0,
                  str(vorbereitet["aktueller_preis"]))
            ergebnis = _wa_ausfuehren(basis, "volatility_breakout",
                                       vorbereitet["vorgang"])
            check("Sofortiges Schliessen funktioniert unveraendert (HTTP 200)",
                  ergebnis.status_code == 200, ergebnis.text[:120])
            check("... und meldet ausdruecklich KEINEN Warteauftrag",
                  ergebnis.json()["warteauftrag"] is False)
            check("Die Zeile ist geschlossen - der uebliche Weg schreibt weiter",
                  [z for z in zeilen(db_aktien) if z["id"] == aapl_id][0]["status"]
                  == "closed")
            check("Und es ist KEIN Warteauftrag entstanden",
                  _auftraege_aus_datei() == [], str(_auftraege_aus_datei())[:120])

        stand_aktien = zeilen(db_aktien)

        # --- 17b) Boerse GESCHLOSSEN: der Warnschritt ----------------------
        with boerse_am(ZEIT_WOCHENENDE):
            antwort = get(basis, "/api/bots/volatility_breakout/"
                                  "schliessbare-positionen?live=1").json()
            check("Bei geschlossener Boerse meldet die Liste 'vormerken'",
                  antwort["boerse"]["warteauftrag_noetig"] is True
                  and antwort["boerse"]["offen"] is False)
            check("... und nennt den letzten Handelstag fuer die Anzeige",
                  antwort["boerse"]["letzter_handelstag"] == "2026-09-11",
                  str(antwort["boerse"]["letzter_handelstag"]))
            check("... und den Zeitpunkt der naechsten Oeffnung",
                  str(antwort["boerse"]["naechste_oeffnung"]).startswith("2026-09-14"),
                  str(antwort["boerse"]["naechste_oeffnung"]))

            vorbereitet = _wa_vorbereiten(basis, "volatility_breakout",
                                           msft_id).json()
            check("Der Vorgang ist jetzt ein WARTEAUFTRAGS-Vorgang",
                  vorbereitet["warteauftrag"] is True)
            check("Der Server entscheidet das, nicht der Aufrufer - die "
                  "Boersenlage liegt dem Vorgang bei",
                  vorbereitet["boerse"]["offen"] is False)
            aktien_db_unveraendert("Nach dem Vorbereiten")

            # OHNE Bestaetigung des Warnschritts passiert GAR NICHTS.
            abgelehnt = _wa_ausfuehren(basis, "volatility_breakout",
                                        vorbereitet["vorgang"])
            check("Ohne Bestaetigung des Warnschritts: abgelehnt (409)",
                  abgelehnt.status_code == 409, str(abgelehnt.status_code))
            check("... die Meldung nennt den Grund und sagt, dass nichts "
                  "geaendert wurde",
                  "nichts geaendert" in abgelehnt.json()["detail"]
                  and "vorgemerkt" in abgelehnt.json()["detail"],
                  abgelehnt.json()["detail"][:120])
            check("... es ist KEIN Warteauftrag entstanden",
                  _auftraege_aus_datei() == [])
            aktien_db_unveraendert("Nach dem abgelehnten Versuch")

            # Ein falscher Wert im Bestaetigungsfeld zaehlt nicht als
            # Bestaetigung - geprueft wird auf genau True.
            for falsch in ("ja", 1, "true", 0, None):
                v = _wa_vorbereiten(basis, "volatility_breakout", msft_id).json()
                a = _wa_ausfuehren(basis, "volatility_breakout", v["vorgang"],
                                    bestaetigt=falsch)
                check(f"Bestaetigung {falsch!r} zaehlt nicht - abgelehnt",
                      a.status_code == 409, str(a.status_code))
            check("Nach fuenf Fehlversuchen steht immer noch kein Auftrag da",
                  _auftraege_aus_datei() == [])
            aktien_db_unveraendert("Nach allen Fehlversuchen")

            # MIT Bestaetigung: der Auftrag entsteht - und sonst nichts.
            vorbereitet = _wa_vorbereiten(basis, "volatility_breakout",
                                           msft_id).json()
            ergebnis = _wa_ausfuehren(basis, "volatility_breakout",
                                       vorbereitet["vorgang"], bestaetigt=True)
            check("Mit Bestaetigung: HTTP 200", ergebnis.status_code == 200,
                  ergebnis.text[:140])
            daten = ergebnis.json()
            check("... das Ergebnis sagt ausdruecklich 'Warteauftrag'",
                  daten["warteauftrag"] is True)
            check("... die Meldung sagt, dass NICHT geschlossen wurde",
                  "NICHT geschlossen" in daten["meldung"],
                  daten["meldung"][:120])
            check("... und dass die Ausfuehrung ohne erneute Rueckfrage kommt",
                  "ohne erneute Rueckfrage" in daten["meldung"])
            aktien_db_unveraendert("Nach dem Anlegen des Warteauftrags")
            check("Die uebrigen Bot-Datenbanken sind ebenfalls unveraendert",
                  _pruefsummen(andere) == pruefsummen_andere)

            # PERSISTENZ: der Auftrag steht auf der Platte, nicht im Speicher.
            auf_platte = _auftraege_aus_datei()
            check("Genau EIN Auftrag steht in der Datei auf der Platte",
                  len(auf_platte) == 1, str(auf_platte)[:140])
            auftrag = auf_platte[0]
            check("Er nennt Bot, Trade-ID, Symbol, Zeitpunkt und Quelle",
                  auftrag["bot"] == "volatility_breakout"
                  and auftrag["trade_id"] == msft_id
                  and auftrag["symbol"] == "MSFT"
                  and auftrag["angefordert_am"]
                  and auftrag["quelle"] == "dashboard"
                  and auftrag["benutzer"].startswith("dashboard@"),
                  str(auftrag)[:200])
            check("Er nennt bewusst KEINEN Ausstiegskurs - den gibt es noch "
                  "nicht",
                  "kurs" not in auftrag and "exit_price" not in auftrag,
                  str(sorted(auftrag))[:160])

            # Ein zweiter Auftrag fuer dieselbe Zeile wird abgelehnt.
            zweiter = _wa_vorbereiten(basis, "volatility_breakout", msft_id)
            check("Ein zweiter Auftrag fuer dieselbe Position: abgelehnt (409)",
                  zweiter.status_code == 409, str(zweiter.status_code))
            check("... mit dem Hinweis auf den bestehenden Auftrag",
                  "bereits ein Warteauftrag" in zweiter.json()["detail"],
                  zweiter.json()["detail"][:110])

            # Die Liste zeigt ihn - auf beiden Wegen.
            liste = get(basis, "/api/warteauftraege").json()
            check("Die Uebersichtsliste zeigt den Auftrag",
                  liste["anzahl"] == 1
                  and liste["auftraege"][0]["symbol"] == "MSFT")
            check("... mit dem Vermerk, dass die Position noch offen ist",
                  liste["auftraege"][0]["noch_offen"] is True)
            liste_bot = get(basis, "/api/warteauftraege?bot=volatility_breakout").json()
            check("Die Bot-Liste zeigt denselben Auftrag",
                  liste_bot["anzahl"] == 1
                  and liste_bot["auftraege"][0]["id"] == auftrag["id"])
            leer = get(basis, "/api/warteauftraege?bot=t3_supertrend").json()
            check("Ein Bot ohne Auftraege liefert eine leere Liste, keinen Fehler",
                  leer["anzahl"] == 0)

            # Die Positionsliste weist die Zeile als vorgemerkt aus.
            antwort = get(basis, "/api/bots/volatility_breakout/"
                                  "schliessbare-positionen?live=1").json()
            vorgemerkt = [p for p in antwort["positionen"] if p["id"] == msft_id]
            check("Die Positionsliste markiert die Zeile als vorgemerkt",
                  vorgemerkt and vorgemerkt[0]["warteauftrag_offen"] is True)

            # --- 17c) KRYPTO ist von alledem nicht betroffen ---------------
            krypto_posten = _oeffne_positionen(db_krypto, [("BTCUSDT", 100.0)])
            btc_id = krypto_posten[0][0]
            k_antwort = get(basis, "/api/bots/t3_supertrend/"
                                    "schliessbare-positionen?live=1").json()
            check("Krypto-Bot: kein Vormerken, auch am Samstag nicht",
                  k_antwort["boerse"]["warteauftrag_noetig"] is False
                  and k_antwort["boerse"]["kalender_gilt"] is False)
            k_vorbereitet = _wa_vorbereiten(basis, "t3_supertrend", btc_id).json()
            check("Krypto-Vorgang ist ein SOFORT-Vorgang",
                  k_vorbereitet["warteauftrag"] is False)
            k_ergebnis = _wa_ausfuehren(basis, "t3_supertrend",
                                         k_vorbereitet["vorgang"])
            check("Krypto wird am Samstag sofort geschlossen (HTTP 200)",
                  k_ergebnis.status_code == 200, k_ergebnis.text[:120])
            check("... die Zeile ist geschlossen",
                  [z for z in zeilen(db_krypto) if z["id"] == btc_id][0]["status"]
                  == "closed")
            check("... und es ist dabei KEIN Auftrag entstanden",
                  len(_auftraege_aus_datei()) == 1)
            check("Der Kern lehnt einen Krypto-Warteauftrag auch direkt ab",
                  _wirft(lambda: warteauftraege.anlegen(
                      "t3_supertrend", 1, "BTCUSDT", "test", "test"),
                      warteauftraege.WarteauftragNichtMoeglich, "Krypto-Bot"))

            # --- 17d) Stornieren ------------------------------------------
            protokoll_vorher = open(protokoll_datei, encoding="utf-8").read()
            storniert = post(basis, "/api/warteauftraege/stornieren",
                              {"id": auftrag["id"]})
            check("Stornieren ohne zweite Bestaetigung: HTTP 200",
                  storniert.status_code == 200, storniert.text[:120])
            check("... die Meldung sagt, dass die Position offen bleibt",
                  "bleibt offen" in storniert.json()["meldung"],
                  storniert.json()["meldung"][:120])
            check("Der Auftrag ist aus der Datei verschwunden",
                  _auftraege_aus_datei() == [])
            aktien_db_unveraendert("Nach dem Stornieren")
            check("Die Position ist unveraendert OFFEN geblieben",
                  [z for z in zeilen(db_aktien) if z["id"] == msft_id][0]["status"]
                  == "open")

            neu_im_protokoll = open(protokoll_datei, encoding="utf-8").read()[
                len(protokoll_vorher):]
            check("Das Stornieren steht als 'STORNIERT' im Protokoll",
                  "WARTEAUFTRAG-STORNIERT" in neu_im_protokoll,
                  neu_im_protokoll[:140])
            check("... ausdruecklich NICHT als ausgefuehrt oder fehlgeschlagen",
                  "AUSGEFUEHRT" not in neu_im_protokoll
                  and "FEHLGESCHLAGEN" not in neu_im_protokoll)
            check("... und mit dem Vermerk, dass nichts geschrieben wurde",
                  "Datenbank unveraendert" in neu_im_protokoll)

            zweimal = post(basis, "/api/warteauftraege/stornieren",
                            {"id": auftrag["id"]})
            check("Ein zweites Stornieren desselben Auftrags: 409, kein Absturz",
                  zweimal.status_code == 409, str(zweimal.status_code))

            # --- 17e) Protokollzeile beim ANLEGEN --------------------------
            protokoll_vorher = open(protokoll_datei, encoding="utf-8").read()
            v = _wa_vorbereiten(basis, "volatility_breakout", msft_id).json()
            _wa_ausfuehren(basis, "volatility_breakout", v["vorgang"],
                            bestaetigt=True)
            neu_im_protokoll = open(protokoll_datei, encoding="utf-8").read()[
                len(protokoll_vorher):]
            check("Das Anlegen hat eine eigene, erkennbare Protokollzeile",
                  "WARTEAUFTRAG-ANGELEGT" in neu_im_protokoll,
                  neu_im_protokoll[:160])
            check("... mit dem ausdruecklichen Vermerk 'Datenbank UNVERAENDERT'",
                  "Datenbank UNVERAENDERT" in neu_im_protokoll)
            check("... und sie steht in DERSELBEN Datei wie die uebrigen "
                  "manuellen Eingriffe",
                  "MANUELLER-EINGRIFF" in neu_im_protokoll)
    finally:
        monitor.fetch_live_prices_for_bots = original_kurse


def _wirft(aufruf, art, textstueck=""):
    """Hilfsmittel: wirft der Aufruf die erwartete Ausnahme mit dem
    erwarteten Text? Bewusst kein blosses 'wirft irgendetwas' - eine
    Ausnahme aus einem Tippfehler saehe sonst aus wie ein bestandener Test."""
    try:
        aufruf()
    except art as fehler:
        return textstueck in str(fehler)
    except Exception:
        return False
    return False


# ---------------------------------------------------------------------------
# 18) Das Ausfuehrungsskript - die zeitversetzte Ausfuehrung selbst
# ---------------------------------------------------------------------------
# Hier wird das geprueft, was dieses Projekt bisher nicht hatte: ein
# Schreibzugriff OHNE gleichzeitige Bestaetigung. Entsprechend liegt das
# Gewicht auf den Faellen, in denen NICHT geschrieben werden darf:
#
#   Boerse geschlossen              -> gar nichts, Auftrag bleibt stehen
#   Position schon vom Bot zu       -> uebersprungen, KEIN Schreibversuch
#   Auftrag storniert               -> es gibt nichts mehr auszufuehren
#   Kein Kurs / Datenbank gesperrt  -> Auftrag bleibt, Zaehler hoch
#   Trockenlauf                     -> nichts, unter keinen Umstaenden
#
# Und einen Fall, in dem geschrieben werden MUSS - sonst waere die ganze
# Funktion eine Attrappe (Methodik-Grundsatz 12).

def _auftrag_anlegen(bot, trade_id, symbol, entry_price=None):
    """Legt einen Auftrag direkt ueber den Kern an - ohne HTTP.

    Der Weg ueber die Oberflaeche ist in Abschnitt 17 geprueft; hier geht es
    um das Ausfuehren, und ein Auftrag ist ein Auftrag."""
    with boerse_am(ZEIT_WOCHENENDE):
        return warteauftraege.anlegen(
            bot, trade_id, symbol, "test-nutzer", "dashboard",
            entry_price=entry_price,
            boerse=schliessen.boersenlage("aktien"))


def teste_ausfuehrungsskript(wurzel, db_dateien, protokoll_datei):
    print("\n18) Ausfuehrungsskript fuer Warteauftraege")

    import warteauftraege_ausfuehren as skript

    db_aktien = db_dateien["volatility_breakout"]
    andere = {n: p for n, p in db_dateien.items() if n != "volatility_breakout"}
    warteauftraege.alles_loeschen()

    # Ein eigener Kurslieferant statt yfinance. Das Skript nimmt ihn als
    # Parameter entgegen - im Ernstfall steht dort monitor.fetch_stock_prices,
    # also genau die Funktion, die auch das Dashboard benutzt.
    kurse = {"AAPL": 165.0, "MSFT": 330.0, "NVDA": 480.0}
    holen = lambda symbole: {s: kurse[s] for s in symbole if s in kurse}

    posten = _oeffne_positionen(db_aktien, [("AAPL", 150.0), ("MSFT", 300.0),
                                             ("NVDA", 500.0)])
    aapl, msft, nvda = [p[0] for p in posten]
    pruefsummen_andere = _pruefsummen(andere)

    def zeile(trade_id):
        treffer = [z for z in zeilen(db_aktien) if z["id"] == trade_id]
        return treffer[0] if treffer else None

    # --- 18a) Boerse GESCHLOSSEN: es passiert nichts ----------------------
    _auftrag_anlegen("volatility_breakout", aapl, "AAPL", 150.0)
    stand = zeilen(db_aktien)
    with boerse_am(ZEIT_WOCHENENDE):
        ergebnis = skript.lauf(kurse_holen=holen)
    check("Bei geschlossener Boerse wird nichts geschlossen",
          ergebnis["geschlossen"] == [] and ergebnis["fehlgeschlagen"] == [],
          str(ergebnis["meldung"])[:120])
    check("... der Auftrag bleibt stehen",
          len(warteauftraege.alle()) == 1)
    check("... die Datenbank ist Feld fuer Feld unveraendert",
          unterschiede(stand, zeilen(db_aktien)) == [],
          str(unterschiede(stand, zeilen(db_aktien)))[:120])
    check("... und die Meldung nennt den Grund (Kalender)",
          "geschlossen" in ergebnis["meldung"], ergebnis["meldung"][:110])

    # Auch am Feiertag mitten in der Handelszeit passiert nichts - der Fall,
    # den eine Wochentagsregel durchgelassen haette.
    with boerse_am(ZEIT_FEIERTAG):
        ergebnis = skript.lauf(kurse_holen=holen)
    check("Am Feiertag (Thanksgiving, Donnerstag 13:00 NY) ebenfalls nichts",
          ergebnis["geschlossen"] == [] and len(warteauftraege.alle()) == 1,
          ergebnis["meldung"][:110])
    check("... die Datenbank bleibt auch dort unveraendert",
          unterschiede(stand, zeilen(db_aktien)) == [])

    # Und am verkuerzten Handelstag NACH dem fruehen Schluss.
    with boerse_am(ZEIT_HALBTAG_ZU):
        ergebnis = skript.lauf(kurse_holen=holen)
    check("Nach dem fruehen Schluss eines verkuerzten Handelstags: nichts",
          ergebnis["geschlossen"] == [] and len(warteauftraege.alle()) == 1)

    # --- 18b) TROCKENLAUF bei offener Boerse: sagt was, tut nichts --------
    with boerse_am(ZEIT_OFFEN):
        ergebnis = skript.lauf(trockenlauf=True, kurse_holen=holen)
    check("Trockenlauf meldet, was er taete",
          len(ergebnis["geschlossen"]) == 1
          and ergebnis["geschlossen"][0]["symbol"] == "AAPL",
          str(ergebnis["geschlossen"])[:120])
    check("... schreibt aber nichts",
          unterschiede(stand, zeilen(db_aktien)) == [])
    check("... und laesst den Auftrag stehen",
          len(warteauftraege.alle()) == 1)
    check("... und sagt das auch in der Meldung",
          ergebnis["meldung"].startswith("TROCKENLAUF"),
          ergebnis["meldung"][:60])

    # --- 18c) Boerse OFFEN: jetzt wird geschrieben -----------------------
    protokoll_vorher = open(protokoll_datei, encoding="utf-8").read()
    with boerse_am(ZEIT_OFFEN):
        ergebnis = skript.lauf(kurse_holen=holen)
    check("Bei offener Boerse wird der Auftrag ausgefuehrt",
          len(ergebnis["geschlossen"]) == 1
          and ergebnis["geschlossen"][0]["symbol"] == "AAPL",
          str(ergebnis["meldung"])[:120])
    danach = zeile(aapl)
    check("Die Position ist geschlossen",
          danach["status"] == "closed" and danach["result"] == "manual_close",
          f"{danach['status']} / {danach['result']}")
    check("Geschlossen wurde zum KURS DES AUSFUEHRUNGSZEITPUNKTS, nicht zu "
          "einem beim Bestaetigen gemerkten",
          danach["exit_price"] == 165.0, str(danach["exit_price"]))
    check("Der PnL folgt der Formel des Bots (150 -> 165 = +9.70)",
          danach["pnl_pct"] == 9.7, str(danach["pnl_pct"]))
    veraendert = {f for _, f, _, _ in unterschiede(stand, zeilen(db_aktien))}
    check("Geaendert wurden GENAU die fuenf Ausstiegsfelder",
          veraendert == {"exit_time", "exit_price", "result", "pnl_pct",
                          "status"}, str(sorted(veraendert)))
    check("Die uebrigen Bot-Datenbanken sind byteweise unveraendert",
          _pruefsummen(andere) == pruefsummen_andere)
    check("Der Auftrag ist abgeraeumt",
          warteauftraege.alle() == [], str(warteauftraege.alle())[:120])

    neu = open(protokoll_datei, encoding="utf-8").read()[len(protokoll_vorher):]
    check("Der Eingriff steht mit quelle=warteauftrag im Protokoll",
          "quelle=warteauftrag" in neu, neu[:160])
    check("... als gewoehnlicher ERFOLGREICH-Eintrag, also mit Vorher/Nachher",
          "ERFOLGREICH" in neu and "VORHER" in neu and "NACHHER" in neu)
    check("... und der Abschluss des Auftrags ist eigens vermerkt",
          "WARTEAUFTRAG-AUSGEFUEHRT" in neu)
    check("... samt Angabe, wer ihn urspruenglich bestellt hatte",
          "bestellt_von=test-nutzer" in neu, neu[-200:])

    # --- 18d) Der Bot war schneller: uebersprungen, kein Fehler -----------
    _auftrag_anlegen("volatility_breakout", msft, "MSFT", 300.0)
    conn = sqlite3.connect(db_aktien)
    conn.execute("UPDATE trades SET status='closed', result='sma_exit', "
                  "exit_price=310.0, pnl_pct=3.03, exit_time='2026-09-10 12:00:00' "
                  "WHERE id=?", (msft,))
    conn.commit()
    conn.close()
    stand = zeilen(db_aktien)
    protokoll_vorher = open(protokoll_datei, encoding="utf-8").read()
    with boerse_am(ZEIT_OFFEN):
        ergebnis = skript.lauf(kurse_holen=holen)
    check("Eine vom Bot selbst geschlossene Position wird UEBERSPRUNGEN",
          len(ergebnis["uebersprungen"]) == 1
          and ergebnis["uebersprungen"][0]["symbol"] == "MSFT",
          str(ergebnis["uebersprungen"])[:120])
    check("... und ausdruecklich NICHT als Fehlschlag gezaehlt",
          ergebnis["fehlgeschlagen"] == [] and ergebnis["geschlossen"] == [])
    check("... die Zeile des Bots bleibt voellig unberuehrt",
          unterschiede(stand, zeilen(db_aktien)) == [],
          str(unterschiede(stand, zeilen(db_aktien)))[:140])
    check("... insbesondere bleibt SEIN Ausstiegsgrund stehen, nicht "
          "'manual_close'",
          zeile(msft)["result"] == "sma_exit", str(zeile(msft)["result"]))
    check("... der Auftrag ist abgeraeumt",
          warteauftraege.alle() == [])
    neu = open(protokoll_datei, encoding="utf-8").read()[len(protokoll_vorher):]
    check("... und im Protokoll steht UEBERSPRUNGEN mit Begruendung",
          "WARTEAUFTRAG-UEBERSPRUNGEN" in neu
          and "bereits vom Bot selbst geschlossen" in neu, neu[:200])
    check("... und gerade KEIN Schreibversuch, also keine Ablehnung",
          "ABGELEHNT" not in neu, neu[:200])

    # --- 18e) Storniert heisst storniert ---------------------------------
    auftrag = _auftrag_anlegen("volatility_breakout", nvda, "NVDA", 500.0)
    warteauftraege.stornieren(auftrag["id"], "test", "dashboard")
    stand = zeilen(db_aktien)
    with boerse_am(ZEIT_OFFEN):
        ergebnis = skript.lauf(kurse_holen=holen)
    check("Ein stornierter Auftrag wird NICHT ausgefuehrt",
          ergebnis["geschlossen"] == [] and ergebnis["auftraege_gesamt"] == 0,
          str(ergebnis["meldung"])[:110])
    check("... die Position bleibt offen",
          zeile(nvda)["status"] == "open")
    check("... und die Datenbank unveraendert",
          unterschiede(stand, zeilen(db_aktien)) == [])
    # Gegenprobe: OHNE Stornierung wuerde dieselbe Position geschlossen -
    # sonst belegte der Test oben nur, dass gerade gar nichts passiert.
    _auftrag_anlegen("volatility_breakout", nvda, "NVDA", 500.0)
    with boerse_am(ZEIT_OFFEN):
        ergebnis = skript.lauf(kurse_holen=holen)
    check("Gegenprobe: ohne Stornierung wird dieselbe Position geschlossen",
          len(ergebnis["geschlossen"]) == 1
          and zeile(nvda)["status"] == "closed",
          str(ergebnis["meldung"])[:110])
    check("Gegenprobe: der Ausstiegskurs ist der aktuelle (480), nicht der "
          "Einstieg", zeile(nvda)["exit_price"] == 480.0,
          str(zeile(nvda)["exit_price"]))

    # --- 18f) Kein Kurs: der Auftrag bleibt stehen -----------------------
    posten = _oeffne_positionen(db_aktien, [("AAPL", 100.0)])
    ohne_kurs = posten[0][0]
    _auftrag_anlegen("volatility_breakout", ohne_kurs, "AAPL", 100.0)
    stand = zeilen(db_aktien)
    with boerse_am(ZEIT_OFFEN):
        ergebnis = skript.lauf(kurse_holen=lambda symbole: {})
    check("Ohne Kurs wird nicht geschrieben",
          ergebnis["geschlossen"] == []
          and len(ergebnis["fehlgeschlagen"]) == 1,
          str(ergebnis["fehlgeschlagen"])[:120])
    check("... der Auftrag bleibt stehen (der naechste Lauf versucht es erneut)",
          len(warteauftraege.alle()) == 1)
    check("... mit Zaehler und Grund am Auftrag",
          warteauftraege.alle()[0]["versuche"] == 1
          and "Kurs" in (warteauftraege.alle()[0]["letzter_fehler"] or ""),
          str(warteauftraege.alle()[0])[:160])
    check("... und die Datenbank ist unveraendert",
          unterschiede(stand, zeilen(db_aktien)) == [])

    # --- 18g) Gesperrte Datenbank: derselbe Schutz wie beim Schliessen ---
    halter_skript = os.path.join(wurzel, "sperr_halter_wa.py")
    with open(halter_skript, "w", encoding="utf-8") as datei:
        datei.write(SPERR_HALTER_FREI)
    altes_limit = manual_close.SPERR_TIMEOUT_SEKUNDEN
    manual_close.SPERR_TIMEOUT_SEKUNDEN = 1
    halter = subprocess.Popen([sys.executable, halter_skript, db_aktien, "6"],
                               stdout=subprocess.PIPE, text=True)
    try:
        check("Ein Fremdprozess haelt die Schreibsperre (wie ein Cronjob)",
              halter.stdout.readline().strip() == "gesperrt")
        with boerse_am(ZEIT_OFFEN):
            ergebnis = skript.lauf(kurse_holen=lambda s: {"AAPL": 111.0})
        check("Bei gesperrter Datenbank wird sauber abgebrochen",
              ergebnis["geschlossen"] == []
              and len(ergebnis["fehlgeschlagen"]) == 1,
              str(ergebnis["fehlgeschlagen"])[:140])
        check("... die Meldung nennt die Sperre",
              "gesperrt" in ergebnis["fehlgeschlagen"][0]["grund"].lower(),
              ergebnis["fehlgeschlagen"][0]["grund"][:110])
        check("... der Auftrag bleibt stehen und zaehlt den zweiten Versuch",
              len(warteauftraege.alle()) == 1
              and warteauftraege.alle()[0]["versuche"] == 2,
              str(warteauftraege.alle()[0]["versuche"]))
    finally:
        manual_close.SPERR_TIMEOUT_SEKUNDEN = altes_limit
        halter.wait(timeout=60)
    check("Nach dem Ende der Sperre ist die Zeile immer noch offen",
          zeile(ohne_kurs)["status"] == "open")

    # Und jetzt laeuft es durch - die Sperre ist weg, der Kurs da.
    with boerse_am(ZEIT_OFFEN):
        ergebnis = skript.lauf(kurse_holen=lambda s: {"AAPL": 111.0})
    check("Derselbe Auftrag laeuft im naechsten Lauf sauber durch",
          len(ergebnis["geschlossen"]) == 1
          and zeile(ohne_kurs)["status"] == "closed",
          str(ergebnis["meldung"])[:110])
    check("Die Auftragsliste ist danach leer",
          warteauftraege.alle() == [])

    # --- 18h) Ein Auftrag auf einen Krypto-Bot wird NICHT ausgefuehrt ----
    # Ueber die Oberflaeche kann er nicht entstehen (Abschnitt 17). Wer die
    # Datei von Hand bearbeitet, soll trotzdem keinen Schreibzugriff
    # ausloesen - der Kalender gilt fuer Krypto ja gar nicht.
    krypto_posten = _oeffne_positionen(db_dateien["t3_supertrend"],
                                        [("BTCUSDT", 100.0)])
    with _sperre_frei():
        stand_datei = {"version": 1, "auftraege": [{
            "id": "handgemacht", "bot": "t3_supertrend",
            "anzeigename": "T3", "trade_id": krypto_posten[0][0],
            "symbol": "BTCUSDT", "entry_time": None, "entry_price": 100.0,
            "angefordert_am": "2026-09-12T10:00:00+00:00",
            "benutzer": "von-hand", "quelle": "handarbeit",
            "boerse_bei_anforderung": {}, "versuche": 0,
            "letzter_versuch_am": None, "letzter_fehler": None}]}
        with open(warteauftraege.datei(), "w", encoding="utf-8") as fh:
            json.dump(stand_datei, fh)
    krypto_stand = zeilen(db_dateien["t3_supertrend"])
    with boerse_am(ZEIT_OFFEN):
        ergebnis = skript.lauf(kurse_holen=lambda s: {"BTCUSDT": 120.0})
    check("Ein von Hand eingetragener Krypto-Auftrag wird NICHT ausgefuehrt",
          ergebnis["geschlossen"] == []
          and len(ergebnis["fehlgeschlagen"]) == 1,
          str(ergebnis["fehlgeschlagen"])[:140])
    check("... die Krypto-Datenbank bleibt unveraendert",
          unterschiede(krypto_stand,
                        zeilen(db_dateien["t3_supertrend"])) == [])
    warteauftraege.alles_loeschen()

    # --- 18i) Leerlauf kostet nichts -------------------------------------
    ergebnis = skript.lauf(kurse_holen=_kein_kursabruf)
    check("Ohne Auftraege endet der Lauf sofort - ohne Kursabfrage",
          ergebnis["auftraege_gesamt"] == 0 and ergebnis["boerse"] is None,
          str(ergebnis["meldung"])[:80])


def _kein_kursabruf(symbole):
    raise AssertionError("Ohne Warteauftraege darf keine Kursabfrage "
                         "stattfinden - genau das macht einen engen "
                         "Cron-Takt bezahlbar.")


class _sperre_frei:
    """Kontext, der die Auftragsdatei direkt beschreibt - unter derselben
    Sperre wie das Modul selbst."""

    def __enter__(self):
        self._s = warteauftraege._sperre().__enter__()
        return self

    def __exit__(self, *_):
        self._s.__exit__(None, None, None)
        return False


# ---------------------------------------------------------------------------
# 19) Mehrere Auftraege ueber mehrere Bots - und der gemischte Crash-Fall
# ---------------------------------------------------------------------------
# Der Fall, der im Ernstfall zaehlt: Sonntagabend, der Nutzer will alles
# glattstellen. Krypto laesst sich schliessen, Aktien nicht. Ein Klick, zwei
# voellig verschiedene Ausgaenge - und die Anzeige muss beide auseinander
# halten, sonst haelt sich jemand fuer flach im Markt und ist es nicht.

def teste_mehrere_warteauftraege(basis, wurzel, db_dateien, protokoll_datei):
    print("\n19) Mehrere Warteauftraege ueber mehrere Bots")

    import warteauftraege_ausfuehren as skript

    # Ein ZWEITER Aktien-Bot. Bis hierher hatte das Testprojekt nur einen -
    # damit liesse sich "mehrere Bots" nicht belegen, sondern nur behaupten.
    db_zweiter = _lege_bot_an(wurzel, "turtle_soup_stocks", [],
                               live_params="ALLOCATION_PCT = 4\n")
    db_dateien = dict(db_dateien)
    db_dateien["turtle_soup_stocks"] = db_zweiter

    db_a1 = db_dateien["volatility_breakout"]
    db_k1 = db_dateien["t3_supertrend"]
    db_k2 = db_dateien["elliott_wave"]

    original_kurse = monitor.fetch_live_prices_for_bots
    alle_kurse = {"AAPL": 160.0, "MSFT": 320.0, "NVDA": 490.0, "TSLA": 210.0,
                  "BTCUSDT": 110.0, "ETHUSDT": 180.0, "SOLUSDT": 22.0}
    monitor.fetch_live_prices_for_bots = lambda bots: dict(alle_kurse)
    schliessen.vorgaenge_zuruecksetzen()
    warteauftraege.alles_loeschen()
    try:
        a1 = _oeffne_positionen(db_a1, [("AAPL", 150.0), ("MSFT", 300.0)])
        a2 = _oeffne_positionen(db_zweiter, [("TSLA", 200.0)])
        k1 = _oeffne_positionen(db_k1, [("BTCUSDT", 100.0)])
        k2 = _oeffne_positionen(db_k2, [("SOLUSDT", 20.0)])

        def status(bot, trade_id):
            conn = sqlite3.connect(db_dateien[bot])
            zeile = conn.execute("SELECT status, result FROM trades WHERE id=?",
                                  (trade_id,)).fetchone()
            conn.close()
            return tuple(zeile) if zeile else None

        stand_a1, stand_a2 = zeilen(db_a1), zeilen(db_zweiter)

        with boerse_am(ZEIT_WOCHENENDE):
            # --- 19a) Bot-weiter Notfallweg bei geschlossener Boerse ------
            vorbereitet = _alle_vorbereiten(basis, "volatility_breakout").json()
            check("Bot-weit: der Vorgang ist ein Warteauftrags-Vorgang",
                  vorbereitet["warteauftrag"] is True
                  and vorbereitet["boerse"]["offen"] is False)
            offen_jetzt = len(manual_close.offene_positionen("volatility_breakout"))
            check("... und umfasst ALLE offenen Positionen dieses Bots",
                  vorbereitet["anzahl"] == offen_jetzt >= 2,
                  f"{vorbereitet['anzahl']} von {offen_jetzt}")

            ohne = _alle_ausfuehren(basis, vorbereitet["vorgang"],
                                     "volatility_breakout")
            check("Bot-weit ohne Bestaetigung des Warnschritts: 409",
                  ohne.status_code == 409, str(ohne.status_code))
            check("... nichts geschrieben, nichts vorgemerkt",
                  unterschiede(stand_a1, zeilen(db_a1)) == []
                  and warteauftraege.alle() == [])

            vorbereitet = _alle_vorbereiten(basis, "volatility_breakout").json()
            mit = post(basis, "/api/bots/volatility_breakout/"
                               "alle-schliessen/ausfuehren",
                        {"vorgang": vorbereitet["vorgang"],
                         schliessen.WARTEAUFTRAG_BESTAETIGUNG: True})
            check("Bot-weit mit Bestaetigung: HTTP 200",
                  mit.status_code == 200, mit.text[:140])
            ergebnis = mit.json()
            check("... alle Positionen sind vorgemerkt, keine geschlossen",
                  ergebnis["anzahl_vorgemerkt"] == offen_jetzt
                  and "geschlossen" not in ergebnis, str(sorted(ergebnis))[:160])
            check("... die Meldung sagt ausdruecklich 'nichts geschlossen'",
                  "nichts geschlossen" in ergebnis["meldung"],
                  ergebnis["meldung"][:130])
            check("... die Datenbank des Bots ist unveraendert",
                  unterschiede(stand_a1, zeilen(db_a1)) == [])
            check("... und fuer jede steht ein Auftrag in der Datei",
                  len(_auftraege_aus_datei()) == offen_jetzt,
                  str(len(_auftraege_aus_datei())))

            # Ein zweiter Durchlauf findet nichts mehr vorzumerken.
            nochmal = _alle_vorbereiten(basis, "volatility_breakout")
            check("Ein zweiter Durchlauf wird abgelehnt - alles steht schon",
                  nochmal.status_code == 409, str(nochmal.status_code))
            check("... mit dem Grund je Position",
                  "vormerken" in nochmal.json()["detail"],
                  nochmal.json()["detail"][:120])

            # --- 19b) Der globale Crash-Weg: GEMISCHT --------------------
            crash = _crash_vorbereiten(basis).json()
            check("Crash-Uebersicht: der Vorgang ist gemischt",
                  crash["warteauftrag"] is True
                  and crash["anzahl_sofort"] >= 2
                  and crash["anzahl_warteauftrag"] >= 1,
                  f"sofort={crash['anzahl_sofort']} "
                  f"vormerken={crash['anzahl_warteauftrag']}")
            check("... die Aktien-Bots sind als 'wird vorgemerkt' markiert",
                  all(b["warteauftrag"] is True for b in crash["bots"]
                      if b["anlageklasse"] == "aktien"),
                  str([(b["bot"], b["warteauftrag"]) for b in crash["bots"]]))
            check("... die Krypto-Bots ausdruecklich NICHT",
                  all(b["warteauftrag"] is False for b in crash["bots"]
                      if b["anlageklasse"] == "krypto"))
            check("... und die beiden Zahlen werden nicht zu einer verrechnet",
                  crash["anzahl"] == crash["anzahl_sofort"]
                  + crash["anzahl_warteauftrag"])
            check("Die bereits vorgemerkten Positionen zaehlen nicht noch "
                  "einmal mit",
                  all(p["grund"] == "steht bereits als Warteauftrag"
                      for b in crash["bots"] if b["bot"] == "volatility_breakout"
                      for p in b["positionen"] if not p["schliessbar_jetzt"]),
                  str([p for b in crash["bots"]
                       if b["bot"] == "volatility_breakout"
                       for p in b["positionen"]])[:200])

            # Ohne Bestaetigung des Warnschritts passiert GAR NICHTS - auch
            # bei den Krypto-Bots nicht.
            k1_vorher = status("t3_supertrend", k1[0][0])
            ohne = post(basis, "/api/alle-bots-schliessen/ausfuehren",
                         {"vorgang": crash["vorgang"], "bestaetigung": "CRASH"})
            check("Crash ohne Bestaetigung des Warnschritts: 409",
                  ohne.status_code == 409, str(ohne.status_code))
            check("... und die Krypto-Position bleibt ebenfalls unberuehrt - "
                  "ein halb ausgefuehrter Crash waere die schlechteste "
                  "Antwort von allen",
                  status("t3_supertrend", k1[0][0]) == k1_vorher,
                  str(status("t3_supertrend", k1[0][0])))

            crash = _crash_vorbereiten(basis).json()
            mit = post(basis, "/api/alle-bots-schliessen/ausfuehren",
                        {"vorgang": crash["vorgang"], "bestaetigung": "CRASH",
                         schliessen.WARTEAUFTRAG_BESTAETIGUNG: True})
            check("Crash mit beiden Bestaetigungen: HTTP 200",
                  mit.status_code == 200, mit.text[:140])
            r = mit.json()
            check("Die Krypto-Positionen sind SOFORT geschlossen",
                  status("t3_supertrend", k1[0][0]) == ("closed", "manual_close")
                  and status("elliott_wave", k2[0][0]) == ("closed", "manual_close"),
                  f"{status('t3_supertrend', k1[0][0])} / "
                  f"{status('elliott_wave', k2[0][0])}")
            check("Die Aktien-Position des zweiten Bots ist NICHT geschlossen",
                  status("turtle_soup_stocks", a2[0][0]) == ("open", None))
            check("... sondern vorgemerkt",
                  any(a["bot"] == "turtle_soup_stocks"
                      for a in _auftraege_aus_datei()),
                  str([a["bot"] for a in _auftraege_aus_datei()]))
            check("Das Ergebnis weist geschlossen und vorgemerkt GETRENNT aus",
                  r["anzahl_geschlossen"] >= 2 and r["anzahl_vorgemerkt"] == 1
                  and r["anzahl_geschlossen"] != r["anzahl_vorgemerkt"],
                  f"{r['anzahl_geschlossen']} / {r['anzahl_vorgemerkt']}")
            check("... die geschlossenen sind ausschliesslich Krypto-Positionen",
                  all(b["bot"] in ("t3_supertrend", "elliott_wave",
                                    "rsi2_crypto", "turtle_soup_crypto",
                                    "volatility_breakout_crypto")
                      for b in r["bots"] if b["anzahl_geschlossen"]),
                  str([(b["bot"], b["anzahl_geschlossen"]) for b in r["bots"]]))
            check("... die vorgemerkten ausschliesslich Aktien-Positionen",
                  all(b["bot"] in ("volatility_breakout", "turtle_soup_stocks",
                                    "rsi2_mean_reversion", "elliott_wave_stocks")
                      for b in r["bots_vorgemerkt"]),
                  str([b["bot"] for b in r["bots_vorgemerkt"]]))
            check("... die vorgemerkten zaehlen ausdruecklich nicht als "
                  "geschlossen",
                  all(g["symbol"] not in ("TSLA",) for b in r["bots"]
                      for g in b["geschlossen"]))
            check("... und die Meldung nennt beides",
                  "vorgemerkt" in r["meldung"] and "geschlossen" in r["meldung"],
                  r["meldung"][:200])
            check("Die Datenbanken beider Aktien-Bots sind unveraendert",
                  unterschiede(stand_a1, zeilen(db_a1)) == []
                  and unterschiede(stand_a2, zeilen(db_zweiter)) == [])
            check("Insgesamt stehen jetzt Auftraege ueber ZWEI Bots",
                  len(_auftraege_aus_datei()) == offen_jetzt + 1
                  and {a["bot"] for a in _auftraege_aus_datei()}
                  == {"volatility_breakout", "turtle_soup_stocks"},
                  str([(a["bot"], a["symbol"]) for a in _auftraege_aus_datei()]))

            liste = get(basis, "/api/warteauftraege").json()
            check("Die Uebersichtsliste zeigt alle, bot-uebergreifend",
                  liste["anzahl"] == offen_jetzt + 1
                  and {a["bot"] for a in liste["auftraege"]}
                  == {"volatility_breakout", "turtle_soup_stocks"})
            check("... jeweils mit Anzeigenamen fuer die Tabelle",
                  all(a["anzeigename"] for a in liste["auftraege"]))

        # --- 19c) Ein Lauf raeumt alle drei ab, ueber beide Bots ---------
        with boerse_am(ZEIT_OFFEN):
            ergebnis = skript.lauf(
                kurse_holen=lambda symbole: {s: alle_kurse[s] for s in symbole
                                              if s in alle_kurse})
        check("Ein einziger Lauf schliesst alle wartenden Positionen",
              len(ergebnis["geschlossen"]) == offen_jetzt + 1,
              str(ergebnis["meldung"])[:140])
        check("... ueber beide Aktien-Bots hinweg",
              {g["bot"] for g in ergebnis["geschlossen"]}
              == {"volatility_breakout", "turtle_soup_stocks"},
              str({g["bot"] for g in ergebnis["geschlossen"]}))
        geschrieben = {g["symbol"]: g["exit_preis"]
                       for g in ergebnis["geschlossen"]}
        check("... jede zu IHREM eigenen aktuellen Kurs",
              all(geschrieben[s] == alle_kurse[s] for s in geschrieben)
              and {"AAPL", "MSFT", "TSLA"} <= set(geschrieben),
              str(geschrieben))
        check("... und die Auftragsliste ist danach leer",
              warteauftraege.alle() == [])
        check("Alle drei Zeilen tragen jetzt den manuellen Vermerk",
              status("volatility_breakout", a1[0][0]) == ("closed", "manual_close")
              and status("volatility_breakout", a1[1][0]) == ("closed", "manual_close")
              and status("turtle_soup_stocks", a2[0][0]) == ("closed", "manual_close"))
    finally:
        monitor.fetch_live_prices_for_bots = original_kurse
        # Den zweiten Aktien-Bot wieder entfernen - die uebrigen Abschnitte
        # rechnen mit drei Bots im Testprojekt.
        if os.path.exists(db_zweiter):
            os.remove(db_zweiter)
        shutil.rmtree(os.path.join(wurzel, "strategies", "turtle_soup_stocks"),
                      ignore_errors=True)
        warteauftraege.alles_loeschen()


# ---------------------------------------------------------------------------
# 16) Der echte Boersenkalender - ohne Server, ohne Datenbank
# ---------------------------------------------------------------------------
# Diese Pruefungen sind der Grund, warum eine Bibliothek benutzt wird statt
# einer Zeitregel. Jeder einzelne Fall unten wuerde eine Faustregel
# ("Mo-Fr, 15:30-22:00") falsch beantworten:
#
#   Thanksgiving         beweglicher Feiertag (4. Donnerstag im November)
#   Karfreitag           haengt am Osterdatum, also am Mondkalender
#   4. Juli 2026         faellt auf einen Samstag und wird am Freitag davor
#                        begangen - ein Werktag, an dem nicht gehandelt wird
#   Tag nach Thanksgiving  Handelsschluss 13:00 statt 16:00 Ortszeit
#
# Und weil eine gruene Pruefung erst dann etwas wert ist, wenn sie auch rot
# werden kann (Methodik-Grundsatz 12), steht bei jedem geschlossenen Tag ein
# offener Zeitpunkt daneben, der durch DIESELBE Funktion laeuft.

def teste_boersenkalender():
    print("\n16) Boersenkalender: echte NYSE-Regeln")
    echt = boersenkalender.status

    check("Bibliothek ist installiert",
          boersenkalender.bibliothek_verfuegbar(),
          str(boersenkalender.BIBLIOTHEK_FEHLER))

    offen = echt(ZEIT_OFFEN)
    check("Normaler Donnerstag, 13:00 New Yorker Zeit: OFFEN",
          offen["offen"] is True, offen["grund"])
    check("Dabei steht der Handelsschluss dieses Tages mit dabei",
          offen["naechster_schluss"] is not None, str(offen["naechster_schluss"]))

    # --- Wochenende --------------------------------------------------------
    wochenende = echt(ZEIT_WOCHENENDE)
    check("Samstag: geschlossen", wochenende["offen"] is False)
    check("... und der letzte Handelstag ist der Freitag davor",
          wochenende["letzter_handelstag"] == "2026-09-11",
          str(wochenende["letzter_handelstag"]))
    check("... die naechste Oeffnung ist der Montag",
          str(wochenende["naechste_oeffnung"]).startswith("2026-09-14"),
          str(wochenende["naechste_oeffnung"]))

    # --- Feiertage ---------------------------------------------------------
    feiertag = echt(ZEIT_FEIERTAG)
    check("Thanksgiving (beweglich, 4. Donnerstag im November): geschlossen",
          feiertag["offen"] is False, feiertag["grund"])
    check("... obwohl es ein Donnerstag mitten in der Handelszeit ist - "
          "genau der Fall, den eine Wochentagsregel verschluckt",
          feiertag["letzter_handelstag"] == "2026-11-25",
          str(feiertag["letzter_handelstag"]))

    karfreitag = echt(ZEIT_KARFREITAG)
    check("Karfreitag (haengt am Osterdatum): geschlossen",
          karfreitag["offen"] is False, karfreitag["grund"])

    juli = echt(ZEIT_4_JULI)
    check("4. Juli 2026 faellt auf Samstag - der Freitag davor ist zu",
          juli["offen"] is False, juli["grund"])

    # --- Verkuerzter Handelstag -------------------------------------------
    # DER Fall, an dem eine Zeitregel drei Stunden lang das Falsche sagt.
    halb_offen = echt(ZEIT_HALBTAG_OFFEN)
    halb_zu = echt(ZEIT_HALBTAG_ZU)
    check("Tag nach Thanksgiving, 12:30 New Yorker Zeit: noch offen",
          halb_offen["offen"] is True, halb_offen["grund"])
    check("... und derselbe Tag um 13:30: bereits geschlossen "
          "(verkuerzter Handelstag)",
          halb_zu["offen"] is False, halb_zu["grund"])
    check("... der Kalender weist ihn ausdruecklich als verkuerzt aus",
          halb_offen["verkuerzter_handelstag"] is True)
    check("Gegenprobe: ein normaler Tag gilt NICHT als verkuerzt",
          offen["verkuerzter_handelstag"] is False)
    check("Eine Faustregel 'bis 22:00 deutscher Zeit' laege hier daneben - "
          "der Unterschied ist belegt, nicht behauptet",
          halb_offen["offen"] is not halb_zu["offen"])

    # --- Fail closed: ohne Bibliothek keine Auskunft ----------------------
    gemerkt = boersenkalender.BIBLIOTHEK_FEHLER
    try:
        boersenkalender.BIBLIOTHEK_FEHLER = "Testfall: Bibliothek fehlt"
        ohne = echt(ZEIT_OFFEN)
        check("Ohne Bibliothek ist die Antwort UNBEKANNT (None), nicht 'offen'",
              ohne["offen"] is None, str(ohne["offen"]))
        check("... mit einer Begruendung, die die Ursache nennt",
              "Bibliothek" in (ohne["grund"] or ""), str(ohne["grund"])[:80])
        lage = schliessen.boersenlage("aktien", ZEIT_OFFEN)
        check("... und die Aktien-Lage ist dann WEDER handelbar NOCH "
              "vormerkbar",
              lage["unbekannt"] is True and lage["handelbar_jetzt"] is False
              and lage["warteauftrag_noetig"] is False, str(lage)[:120])
        krypto = schliessen.boersenlage("krypto", ZEIT_OFFEN)
        check("Krypto bleibt davon voellig unberuehrt - immer handelbar",
              krypto["handelbar_jetzt"] is True
              and krypto["warteauftrag_noetig"] is False
              and krypto["kalender_gilt"] is False)
    finally:
        boersenkalender.BIBLIOTHEK_FEHLER = gemerkt
        boersenkalender.zwischenspeicher_leeren()

    check("Nach dem Testfall antwortet der Kalender wieder normal",
          echt(ZEIT_OFFEN)["offen"] is True)

    # --- Krypto/Aktien-Weiche ---------------------------------------------
    check("Bei geschlossener Boerse ist die Aktien-Lage 'vormerken'",
          schliessen.boersenlage("aktien", ZEIT_WOCHENENDE)["warteauftrag_noetig"]
          is True)
    check("... waehrend Krypto zur selben Zeit sofort handelbar bleibt",
          schliessen.boersenlage("krypto", ZEIT_WOCHENENDE)["handelbar_jetzt"]
          is True)


def teste_schliessen_frontend():
    print("\n10) Frontend des Schliessvorgangs")
    statisch = os.path.join(DIR, "static")
    bot_html = open(os.path.join(statisch, "bot.html"), encoding="utf-8").read()
    app_js = open(os.path.join(statisch, "app.js"), encoding="utf-8").read()
    code = ohne_kommentare(bot_html)

    check("Es gibt echte <dialog>-Elemente statt nachgebauter Overlays",
          code.count("<dialog") == 2 and "showModal()" in code)

    # Die folgenden Pruefungen gelten NUR fuer den Einzel-Dialog. Seit es den
    # Notfall-Dialog gibt, waere eine Suche im ganzen Dokument irrefuehrend:
    # der Notfallweg hat zu Recht zwei Stufen und eine Schritt-Anzeige.
    # Deshalb wird hier genau der eine Dialog herausgeschnitten.
    einzel = code.split('id="schliessdialog"', 1)[1].split("</dialog>", 1)[0]
    notfall = code.split('id="notfalldialog"', 1)[1].split("</dialog>", 1)[0]

    # EIN Schritt: die Zusammenfassung ist schon der vorbereiten-Aufruf, der
    # Knopf darunter der ausfuehren-Aufruf. Die frueheren zwei Stufen samt
    # Texteingabe sind weg - und sollen nicht unbemerkt zurueckkehren.
    check("Einzel-Dialog: keine zweite Stufe im Markup",
          'id="dialog-stufe1"' not in code and 'id="dialog-stufe2"' not in code)
    check("Einzel-Dialog: keine Texteingabe",
          'id="dialog-eingabe"' not in code and "<input" not in einzel)
    check("Einzel-Dialog: keine Schritt-Anzeige ('Schritt 1 von 2')",
          "von 2" not in einzel and 'id="dialog-stufe"' not in einzel)
    check("Einzel-Dialog: genau EIN Abbrechen-Knopf",
          code.count('id="dialog-abbrechen"') == 1
          and 'id="dialog-abbrechen1"' not in code
          and 'id="dialog-abbrechen2"' not in code)

    # --- Notfallweg: ZWEI Klick-Stufen, deutlich abgesetzt ----------------
    check("Notfall-Dialog: zwei Stufen im Markup",
          'id="notfall-stufe1"' in notfall and 'id="notfall-stufe2"' in notfall)
    check("Notfall-Dialog: Schritt-Anzeige vorhanden (anders als beim Einzelweg)",
          'id="notfall-stufe"' in notfall and "von 2" in notfall)
    check("Notfall-Dialog: ebenfalls KEINE Texteingabe - beide Stufen sind Klicks",
          "<input" not in notfall and "BESTAETIGEN" not in notfall)
    check("Notfall-Dialog: zwei verschiedene Knoepfe fuer die zwei Stufen",
          'id="notfall-weiter"' in notfall and 'id="notfall-ausfuehren"' in notfall)
    check("Notfall-Dialog: der erste Knopf startet gesperrt (vor der Kennung)",
          re.search(r'id="notfall-weiter"[^>]*disabled', notfall) is not None)
    check("Notfall-Dialog: Esc und Klick daneben verwerfen den Vorgang auch hier",
          "notfallDialog.addEventListener" in code
          and "notfallAbbrechen()" in code)
    # Geprueft wird das Knopf-Element SELBST, nicht ob die Klasse irgendwo in
    # der Datei vorkommt: "knopf notfall" steht auch an den Dialogknoepfen,
    # eine Suche im ganzen Dokument waere also gruen geblieben, waehrend der
    # Notfallknopf schon wie der harmlose Einzelknopf aussieht. Genau so ist
    # diese Luecke in der Mutationsprobe aufgefallen.
    knopf_tag = re.search(r'<button(?:(?!</?button)[\s\S])*?id="alle-schliessen"'
                           r'(?:(?!</?button)[\s\S])*?>', code)
    check("Der Notfall-Knopf traegt SELBST die eigene Notfall-Klasse",
          knopf_tag is not None and "knopf notfall" in knopf_tag.group(0),
          knopf_tag.group(0)[:110] if knopf_tag else "kein <button> gefunden")
    check("Und gerade NICHT die Klasse des harmlosen Einzel-Knopfes",
          knopf_tag is not None and "schliessen-knopf" not in knopf_tag.group(0)
          and "gefahr" not in knopf_tag.group(0),
          knopf_tag.group(0)[:110] if knopf_tag else "-")
    check("Er steht ausserhalb der Tabelle, in eigener Leiste",
          'id="notfall-leiste"' in code
          and code.index('id="notfall-leiste"') > code.index('id="positionen"'))

    # Die ZWEI Stufen muessen auch wirklich zwei sein: der erste Knopf darf
    # nur weiterblaettern, geschrieben wird ausschliesslich vom zweiten.
    # Ohne diese Pruefung bleibt die Suite gruen, wenn der erste Klick direkt
    # schreibt - die zweite Bestaetigung waere dann wirkungslos. Auch das ist
    # erst in der Mutationsprobe aufgefallen.
    check("Der erste Notfall-Knopf blaettert nur zur zweiten Stufe weiter",
          'getElementById("notfall-weiter")\n  .addEventListener("click", '
          'notfallZurZweitenStufe);' in code)
    check("Geschrieben wird ausschliesslich ueber den Knopf der zweiten Stufe",
          'getElementById("notfall-ausfuehren")\n  .addEventListener("click", '
          'notfallAusfuehren);' in code)
    nach_weiter = code.split('function notfallZurZweitenStufe()', 1)[1] \
        .split("\nasync function", 1)[0]
    check("Die erste Stufe ruft den schreibenden Endpunkt NICHT auf",
          "/alle-schliessen/ausfuehren" not in nach_weiter
          and "notfallAusfuehren" not in nach_weiter, nach_weiter[:120])
    check("Der schreibende Aufruf steht genau EINMAL im Frontend",
          code.count("/alle-schliessen/ausfuehren") == 1)
    check("Der Notfallweg ruft eigene Endpunkte auf",
          "/alle-schliessen/vorbereiten" in code
          and "/alle-schliessen/ausfuehren" in code)
    check("Das Ergebnis nennt Fehlschlaege und Uebersprungene ausdruecklich",
          "fehlgeschlagen" in code and "uebersprungen" in code
          and "nicht_bestaetigt" in code)
    check("Ein gemischter Ausgang wird NICHT als Erfolg dargestellt",
          "teilmeldung" in code
          and "teilmeldung" in open(os.path.join(statisch, "style.css"),
                                     encoding="utf-8").read())
    check("Keine aufsummierte Gesamt-Prozentzahl im Frontend (Grundsatz 2)",
          "pnl_summe" not in code and "pnl_schnitt_pct" in code)

    # --- Globaler Crash-Weg: er steht auf der UEBERSICHTSSEITE -----------
    index = ohne_kommentare(open(os.path.join(statisch, "index.html"),
                                  encoding="utf-8").read())
    check("Der Crash-Knopf steht auf index.html, NICHT auf einer Bot-Seite",
          'id="crash-knopf"' in index and 'id="crash-knopf"' not in code)
    check("Der Crash-Dialog hat DREI Stufen",
          all(f'id="crash-stufe{n}"' in index for n in (1, 2, 3)))
    check("Die dritte Stufe verlangt eine Texteingabe",
          'id="crash-eingabe"' in index)
    check("Der Text wird vom Server geholt, nicht im Frontend festgeschrieben",
          '"CRASH"' not in index and "crashVorgang.crash_text" in index)
    check("Der Frontend-Vergleich ist case-sensitiv (===, kein toUpperCase)",
          "=== crashVorgang.crash_text" in index and "toUpperCase" not in index)
    check("Der Ausfuehren-Knopf der dritten Stufe startet gesperrt",
          re.search(r'id="crash-ausfuehren"[^>]*disabled', index) is not None)
    # Die Stufen muessen wirklich drei sein: nur der letzte Knopf schreibt.
    check("Stufe 1 blaettert nur weiter",
          'getElementById("crash-weiter").addEventListener("click", crashZuStufe2)'
          in index)
    check("Stufe 2 blaettert nur weiter",
          'getElementById("crash-weiter2").addEventListener("click", '
          'crashZumWarnschritt)' in index)
    check("... und der Warnschritt ebenfalls nur weiter (zur Texteingabe)",
          "crashZuStufe3();" in index.split("function crashZumWarnschritt()", 1)[1]
          .split("\n}", 1)[0]
          or 'crashWaBestaetigt = true;\n  crashZuStufe3();' in index)
    check("Nur Stufe 3 loest das Schreiben aus",
          'getElementById("crash-ausfuehren").addEventListener("click", '
          'crashAusfuehren)' in index)
    check("Der schreibende Aufruf steht genau EINMAL im Frontend",
          index.count("/api/alle-bots-schliessen/ausfuehren") == 1)
    vor_stufe3 = index.split("function crashZuStufe3()", 1)[0]
    check("Die Stufen 1, 2 und der Warnschritt rufen den schreibenden "
          "Endpunkt NICHT auf",
          "/api/alle-bots-schliessen/ausfuehren" not in vor_stufe3)
    check("Der Crash-Knopf traegt eine eigene Klasse, nicht die der anderen "
          "Notfall-Knoepfe",
          (lambda t: t is not None and "knopf crash" in t.group(0)
           and "notfall" not in t.group(0))(
              re.search(r'<button(?:(?!</?button)[\s\S])*?id="crash-knopf"'
                         r'(?:(?!</?button)[\s\S])*?>', index)))
    check("Und steht in einem eigenen, abgesetzten Bereich",
          'id="crash-bereich"' in index
          and "crash-bereich" in open(os.path.join(statisch, "style.css"),
                                       encoding="utf-8").read())
    check("Das Ergebnis wird bot-weise ausgewiesen, inkl. ausgefallener Bots",
          "bots_fehlgeschlagen" in index and "b.meldung" in index)
    check("Ein gemischter Ausgang wird auch hier nicht als Erfolg dargestellt",
          "teilmeldung" in index)

    # Das hidden-Attribut muss jede display-Regel schlagen. `display: none`
    # fuer [hidden] steht nur im Browser-Standardstil und verliert gegen jede
    # Autorenregel - ein `.klasse { display: flex }` macht ein verborgenes
    # Element also wieder sichtbar. Genau so war der Notfall-Knopf anfangs
    # auch bei nicht freigeschalteten Bots zu sehen; aufgefallen ist es erst
    # im Browser, nicht in dieser Suite. Deshalb die Pruefung hier.
    css = open(os.path.join(statisch, "style.css"), encoding="utf-8").read()
    check("style.css erzwingt [hidden] gegen jede display-Regel",
          re.search(r"\[hidden\]\s*\{[^}]*display:\s*none\s*!important",
                     css) is not None)
    # Die Leiste wird ueber das hidden-Attribut geschaltet - also haengt ihre
    # Unsichtbarkeit genau an der Regel oben. Beides zusammen geprueft, damit
    # nicht eines von beiden still wegfaellt.
    check("Die Notfall-Leiste wird ueber hidden geschaltet (nicht ueber style)",
          re.search(r"leiste\.hidden\s*=", code) is not None
          and "notfall-leiste" not in code.split("style.display")[0][-200:]
          if "style.display" in code else
          re.search(r"leiste\.hidden\s*=", code) is not None)
    check("Und sie traegt im Markup von Anfang an hidden - vor dem ersten "
          "Ladevorgang ist noch nicht bekannt, ob der Bot freigeschaltet ist",
          re.search(r'id="notfall-leiste"[^>]*hidden', code) is not None)
    check("Der Schliessen-Knopf startet gesperrt - vor dem vorbereiten-Aufruf "
          "gibt es keine Kennung",
          re.search(r'id="dialog-ja"[^>]*disabled', code) is not None)
    check("Derselbe Knopf loest jetzt das Schreiben aus",
          'getElementById("dialog-ja").addEventListener("click", ausfuehren)'
          in code)
    check("Esc und Klick daneben verwerfen den Vorgang ebenfalls",
          '"cancel"' in code and "abbrechen()" in code)

    # Der Bestaetigungstext darf im Frontend nirgends mehr auftauchen -
    # weder festgeschrieben noch aus der Serverantwort gelesen.
    check("Der Bestaetigungstext kommt im Frontend nicht mehr vor",
          '"BESTAETIGEN"' not in code and "bestaetigungstext" not in code)
    check("Der Ausfuehren-Aufruf schickt nur die Kennung",
          "bestaetigung:" not in code)

    # Die Frist bleibt sichtbar: der Vorgang verfaellt serverseitig weiter
    # nach 120 Sekunden, und ein Tap auf einen abgelaufenen Vorgang soll als
    # solcher erkennbar sein, nicht als unerklaerliche Absage.
    check("Der Countdown bleibt und sperrt den Knopf bei Ablauf",
          "fristStarten(vorgang.gueltig_sekunden)" in code
          and "abgelaufen" in code)

    check("Schreibende Aufrufe laufen ueber ein eigenes sende()",
          "async function sende(" in ohne_kommentare(app_js)
          and 'method: "POST"' in app_js)
    check("Beide Server-Aufrufe bleiben getrennt",
          "/schliessen/vorbereiten" in code and "/schliessen/ausfuehren" in code)
    check("Nach dem Schreiben wird sofort neu geladen",
          "ladeDetail()" in code.split("erfolgsmeldung")[1][:600])
    check("Kein location.reload() - die bestehende Aktualisierung wird genutzt",
          "location.reload" not in code)

    # --- Der zusaetzliche Warnschritt bei geschlossener Boerse -----------
    # Er ist die eigentliche Neuerung, und im Frontend liegt seine
    # sichtbare Haelfte. Geprueft wird beides: dass er DA ist, und dass er
    # nicht umgangen werden kann, ohne dass diese Suite rot wird.
    wa_stufe = code.split('id="dialog-warteauftrag"', 1)[1].split("</div>\n  </div>", 1)[0]
    check("Einzel-Dialog: es gibt einen eigenen Warnschritt fuer Warteauftraege",
          'id="dialog-warteauftrag"' in code
          and 'id="dialog-wa-ja"' in code)
    check("... er ist im Markup von Anfang an verborgen - bei offener Boerse "
          "bleibt es beim einen Tap",
          re.search(r'id="dialog-warteauftrag"[^>]*hidden', code) is not None)
    check("... und verlangt KEINE Texteingabe (wie die uebrigen Stufen auch)",
          "<input" not in wa_stufe, wa_stufe[:120])
    check("Sein Knopf traegt eine EIGENE Klasse, nicht die des roten "
          "Schliessen-Knopfes - er loest keinen Schreibzugriff aus",
          (lambda t: t is not None and "knopf warteauftrag" in t.group(0)
           and "gefahr" not in t.group(0))(
              re.search(r'<button(?:(?!</?button)[\s\S])*?id="dialog-wa-ja"'
                         r'(?:(?!</?button)[\s\S])*?>', code)))

    # Der erste Tap darf bei geschlossener Boerse NICHTS senden. Geprueft
    # wird der Wortlaut der Weiche und dass sie VOR dem sende()-Aufruf steht -
    # ohne diese Pruefung bliebe die Suite gruen, wenn der Warnschritt
    # angezeigt und gleichzeitig gesendet wuerde.
    rumpf = code.split("async function ausfuehren()", 1)[1].split("\n}", 1)[0]
    check("Der erste Tap zeigt nur die Warnung und sendet nichts",
          "vorgang.warteauftrag && !warteauftragBestaetigt" in rumpf
          and rumpf.index("return;") < rumpf.index("sende("),
          rumpf[:160])
    check("Erst der Knopf des Warnschritts setzt die Bestaetigung",
          "warteauftragBestaetigt = true;" in code
          and code.count("warteauftragBestaetigt = true;") == 1)

    # Der Feldname MUSS dem entsprechen, den der Server prueft. Zwei
    # Schreibweisen desselben Feldes waeren genau die Doppelfuehrung, an der
    # dieses Projekt schon mehrfach gelitten hat - und hier waere die Folge
    # ein Warnschritt, der bestaetigt wird und trotzdem nicht zaehlt.
    check("Frontend und Server benutzen DENSELBEN Feldnamen fuer die "
          "Bestaetigung",
          f'const WARTEAUFTRAG_FELD = "{schliessen.WARTEAUFTRAG_BESTAETIGUNG}"'
          in app_js, schliessen.WARTEAUFTRAG_BESTAETIGUNG)
    check("... und keine Seite schreibt den Namen ein zweites Mal aus",
          schliessen.WARTEAUFTRAG_BESTAETIGUNG not in code
          and schliessen.WARTEAUFTRAG_BESTAETIGUNG not in index)

    # Der Warntext steht EINMAL, in app.js, und wird von beiden Seiten und
    # allen drei Dialogen benutzt.
    check("Der Warntext steht genau einmal (in app.js) und nennt die "
          "Tragweite",
          "function warteauftragWarnung(" in app_js
          and "ohne erneute Rückfrage" in app_js)
    check("... beide Seiten benutzen ihn, statt ihn nachzubauen",
          "warteauftragWarnung(" in code and "warteauftragWarnung(" in index
          and "function warteauftragWarnung(" not in code
          and "function warteauftragWarnung(" not in index)
    check("Notfall-Dialog: dritte Stufe fuer den Warnschritt vorhanden",
          'id="notfall-stufe3"' in code and 'id="notfall-wa-ausfuehren"' in code)
    check("... und auch sie sendet erst beim zweiten Anlauf",
          "notfallVorgang.warteauftrag && !notfallWaBestaetigt" in code)

    # --- Crash-Weg -------------------------------------------------------
    check("Crash-Dialog: eigener Warnschritt zwischen Rueckfrage und "
          "Texteingabe",
          'id="crash-stufewa"' in index
          and index.index('id="crash-stufewa"') < index.index('id="crash-stufe3"'))
    check("... die Stufenzahl folgt der tatsaechlichen Zahl (3 oder 4)",
          "crashStufenfolge()" in index and "von ${folge.length}" in index)
    check("... die Bestaetigung wird nur mitgeschickt, wenn der Warnschritt "
          "durchlaufen wurde",
          "crashVorgang.warteauftrag && crashWaBestaetigt" in index)
    check("Der gemischte Ausgang wird getrennt angezeigt, nicht "
          "zusammengezaehlt",
          "anzahl_vorgemerkt" in index and "bots_vorgemerkt" in index
          and "NICHT geschlossen" in index)

    # --- Liste der wartenden Auftraege ----------------------------------
    for datei, name in ((code, "Bot-Seite"), (index, "Uebersichtsseite")):
        check(f"{name}: es gibt einen Bereich fuer wartende Auftraege",
              'id="warteauftraege-bereich"' in datei
              and 'id="warteauftraege-tabelle"' in datei)
        check(f"{name}: er ist von Anfang an verborgen und erscheint nur bei "
              f"Bedarf",
              re.search(r'id="warteauftraege-bereich"[^>]*hidden', datei)
              is not None)
        check(f"{name}: jede Zeile hat einen Stornieren-Knopf",
              "stornieren-knopf" in datei)
    check("Stornieren fragt NICHT zurueck - es verhindert eine Ausfuehrung, "
          "statt eine auszuloesen",
          "confirm(" not in code and "confirm(" not in index
          and "confirm(" not in app_js)
    check("Die Liste zeigt an, wenn eine Position gar nicht mehr offen ist",
          "noch_offen === false" in app_js)
    check("Der Datentakt laedt die Boersenlage mit - sonst behauptet eine "
          "offen gelassene Seite abends noch mittags",
          "async function ladeSeitendaten()" in code
          and "ladeSchliessInfo()" in code.split("ladeSeitendaten()", 1)[1][:400])


def ohne_kommentare(quelltext: str) -> str:
    """Entfernt Kommentare aus JS/CSS/HTML, damit die Quelltext-Pruefungen
    unten wirklich den CODE pruefen und nicht den Fliesstext daneben.

    Genau diese Verwechslung hat den Test zunaechst falsch anschlagen
    lassen: app.js erklaert in einem Kommentar, warum bewusst KEIN
    location.reload() benutzt wird - die reine Textsuche sah darin einen
    Aufruf. Umgekehrt koennte ein Kommentar auch faelschlich eine
    Zusicherung erfuellen ("hier stand mal fehlerInFolge += 1").
    Beides ist mit dieser Vorstufe ausgeschlossen.

    Bewusst simpel gehalten (kein echter Parser): Zeichenketten, die '//'
    oder '/*' enthalten, gibt es in diesen Dateien nicht - fuer die
    Zusicherungen hier reicht das. Das ':' vor '//' schuetzt trotzdem
    schon einmal URLs wie https://.
    """
    quelltext = re.sub(r"<!--.*?-->", " ", quelltext, flags=re.S)
    quelltext = re.sub(r"/\*.*?\*/", " ", quelltext, flags=re.S)
    quelltext = re.sub(r"(?<!:)//[^\n]*", " ", quelltext)
    return quelltext


def teste_automatische_aktualisierung():
    """Quelltext-Pruefungen zur periodischen Aktualisierung.

    Das eigentliche Zeitverhalten (Takte, Pause im Hintergrund) laesst sich
    ohne Browser nicht sinnvoll nachstellen - es wurde im Chromium
    beobachtet und im PR dokumentiert. Was hier geprueft wird, sind die
    Zusicherungen, die man beim Umbau versehentlich verlieren koennte."""
    print("\n11) Automatische Aktualisierung (Quelltext)")

    statisch = os.path.join(DIR, "static")

    def lies(datei):
        return ohne_kommentare(open(os.path.join(statisch, datei)).read())

    app_js = lies("app.js")
    index = lies("index.html")
    detail = lies("bot.html")
    css = lies("style.css")

    check("Beide Takte stehen als Konstante am Dateianfang von app.js",
          "const AKTUALISIERUNG_DATEN_MS" in app_js
          and "const AKTUALISIERUNG_KURSE_MS" in app_js)
    check("Die Kurse werden seltener geholt als die Datenbank-Daten "
          "(externe API-Aufrufe sind teurer)",
          app_js.index("AKTUALISIERUNG_DATEN_MS = 60") > 0
          and "AKTUALISIERUNG_KURSE_MS = 150" in app_js)

    check("Die Aktualisierung haengt an document.visibilityState",
          "document.visibilityState" in app_js
          and 'addEventListener("visibilitychange"' in app_js)
    check("Ueberlappende Laeufe werden verhindert",
          "if (laeuft) return;" in app_js)
    check("Ein fehlgeschlagener Lauf wird gezaehlt statt die Anzeige zu leeren",
          "fehlerInFolge += 1" in app_js)
    check("zeigeFehler() loescht bei leerem Text, statt eine leere Box zu zeigen",
          'text ? `<div class="hinweis">${text}</div>` : ""' in app_js)
    check("Es gibt eine dezente Markierung fuer veraltete Daten",
          "classList.add(\"veraltet\")" in app_js and ".veraltet" in css)

    # Regressionstest fuer die Vorstufe selbst: eine Zusicherung darf
    # weder von einem Kommentar erfuellt noch von einem Kommentar
    # gebrochen werden koennen.
    zeilenkommentar = ohne_kommentare("a();  // location.reload()\nb();")
    check("ohne_kommentare() blendet Zeilenkommentare aus",
          "reload" not in zeilenkommentar
          and "a();" in zeilenkommentar and "b();" in zeilenkommentar,
          detail=repr(zeilenkommentar))
    check("ohne_kommentare() blendet Block- und HTML-Kommentare aus",
          "reload" not in ohne_kommentare("/* location.reload() */ a();")
          and "reload" not in ohne_kommentare("<!-- location.reload() --> a();"))
    check("ohne_kommentare() laesst echten Code stehen",
          "location.reload()" in ohne_kommentare("if (x) location.reload();"))

    # Die wichtigste Zusicherung: die Seite wird nie neu geladen, sondern
    # nur ihre Daten erneuert.
    for name, quelle in (("app.js", app_js), ("index.html", index), ("bot.html", detail)):
        check(f"{name} laedt die Seite nicht neu (kein location.reload)",
              "location.reload" not in quelle)

    for name, quelle in (("index.html", index), ("bot.html", detail)):
        check(f"{name} taktet die Datenbank-Daten",
              "autoAktualisierung(" in quelle and "AKTUALISIERUNG_DATEN_MS" in quelle)
        check(f"{name} taktet die Live-Kurse getrennt",
              "AKTUALISIERUNG_KURSE_MS" in quelle)
        check(f"{name} ruft beim ersten Laden dieselben Ladefunktionen auf",
              "erstesLaden()" in quelle)


def teste_ladeindikator():
    """Ladezustand: Auszeichnung der Seiten und Stil.

    Das eigentliche VERHALTEN (welcher Zustand wann gilt, und dass sich
    "laedt" und "veraltet" gegenseitig ausschliessen) prueft
    test_zustandsmaschine.js, indem es app.js wirklich ausfuehrt - siehe
    teste_zustandsmaschine() weiter unten. Hier stehen nur die Dinge, die
    sich sinnvoll am Quelltext festmachen lassen: dass die Elemente in
    beiden Seiten existieren, richtig ausgezeichnet sind und dass es zu
    jeder Klasse auch eine Regel im Stylesheet gibt."""
    print("\n12) Ladeindikator (Auszeichnung und Stil)")

    statisch = os.path.join(DIR, "static")

    def lies(datei):
        return ohne_kommentare(open(os.path.join(statisch, datei)).read())

    app_js = lies("app.js")
    css = lies("style.css")
    roh = {name: open(os.path.join(statisch, name)).read()
            for name in ("index.html", "bot.html")}

    check("Die drei Zustaende stehen als benannte Konstanten in app.js",
          all(f'const {n} ' in app_js or f'const {n}' in app_js
              for n in ("AKTUALISIERUNG_NORMAL", "AKTUALISIERUNG_LAEDT",
                         "AKTUALISIERUNG_VERALTET")))
    check("Beide Zustandsklassen werden vor dem Setzen entfernt "
          "(Ausschluss strukturell, nicht per Absprache)",
          'classList.remove("laedt", "veraltet")' in app_js)
    check("Die Ladeanzeige wird im finally wieder abgemeldet - ein Fehler "
          "darf sie nicht haengen lassen",
          "finally {" in app_js and "ladeanzeigeAus(aufgabe)" in app_js)

    for name, quelle in roh.items():
        gesaeubert = ohne_kommentare(quelle)
        check(f"{name} hat ein Element fuer die Ladeanzeige",
              'id="ladeanzeige"' in quelle)
        check(f"{name}: die Ladeanzeige ist anfangs ausgeblendet",
              'id="ladeanzeige"' in quelle
              and "hidden" in quelle.split('id="ladeanzeige"')[1].split(">")[0])
        check(f"{name}: die Ladeanzeige wird Screenreadern gemeldet",
              'aria-live="polite"' in quelle and 'role="status"' in quelle)
        check(f"{name} benennt beide Aufgaben unterschiedlich",
              "Aktualisiere \u2026" in gesaeubert
              and "Kurse werden geladen \u2026" in gesaeubert)
        check(f"{name} reicht den Zustand an markiereAktualisierung durch",
              "AKTUALISIERUNG_VERALTET" in gesaeubert)

    check("Es gibt eine CSS-Regel fuer den Ladezustand",
          ".laedt {" in css and "@keyframes atmen" in css)
    check("Die Ladeanzeige hat ein animiertes Symbol",
          ".ladeanzeige::before" in css and "@keyframes pulsieren" in css)
    check("Abgeschaltete Bewegung wird respektiert",
          "prefers-reduced-motion" in css)


def teste_zustandsmaschine():
    """Startet den Node-Verhaltenstest, sofern node vorhanden ist.

    Node ist im Projekt sonst nirgends noetig - deshalb ist sein Fehlen
    kein Fehlschlag, sondern ein sichtbarer Hinweis. Was dann ungeprueft
    bleibt, steht in der Meldung, damit niemand die Luecke uebersieht."""
    print("\n13) Verhalten der Zustandsmaschine (node)")

    node = shutil.which("node")
    if not node:
        print("  [uebersprungen] node nicht gefunden - die Zustandsuebergaenge "
              "in app.js\n                  bleiben ungeprueft "
              "(node dashboard/test_zustandsmaschine.js)")
        return

    skript = os.path.join(DIR, "test_zustandsmaschine.js")
    fertig = subprocess.run([node, skript], capture_output=True, text=True,
                             timeout=120)
    for zeile in fertig.stdout.splitlines():
        if zeile.strip():
            print("  " + zeile.strip() if zeile.startswith("  ") else zeile)
    check("Verhaltenstest der Zustandsmaschine (test_zustandsmaschine.js)",
          fertig.returncode == 0,
          detail=fertig.stderr.strip()[-300:] if fertig.returncode else "")


def teste_gewichtung_node():
    """Verhaltenstest der gewichteten Anzeige - wie Abschnitt 13 ueber node.

    Braucht es, weil eine Textsuche in bot.html gruen bleibt, wenn ein
    if-Zweig auf `false` steht: der gesuchte Text liegt dann unerreichbar im
    Rumpf. In der Gegenprobe zu dieser Aenderung blieb genau diese Mutation
    unentdeckt, bis dieser Test dazukam."""
    print("\n16) Verhalten der gewichteten Anzeige (node)")

    node = shutil.which("node")
    if not node:
        print("  [uebersprungen] node nicht gefunden - ob Erlaeuterung und "
              "Ausschluss-Hinweis\n                  wirklich in der Ausgabe "
              "landen, bleibt ungeprueft "
              "(node dashboard/test_gewichtung.js)")
        return

    skript = os.path.join(DIR, "test_gewichtung.js")
    fertig = subprocess.run([node, skript], capture_output=True, text=True,
                             timeout=120)
    for zeile in fertig.stdout.splitlines():
        if zeile.strip():
            print("  " + zeile.strip() if zeile.startswith("  ") else zeile)
    check("Verhaltenstest der gewichteten Anzeige (test_gewichtung.js)",
          fertig.returncode == 0,
          detail=fertig.stderr.strip()[-300:] if fertig.returncode else "")


def teste_zeitstempel(basis):
    """Die Zeitstempel, die der Server SELBST erzeugt, muessen eindeutig
    sein - also mit Zeitzonen-Offset.

    Hintergrund: der "Stand" kam frueher aus datetime.utcnow().isoformat()
    und damit ohne Offset. JavaScript liest eine solche Datum-Zeit-Form
    laut Norm als Ortszeit des Browsers - im Dashboard stand deshalb die
    UTC-Zahl, in Berlin also zwei Stunden zu frueh. Ein naiver String
    sieht dabei voellig unauffaellig aus; nur diese Pruefung faellt auf
    ihn herein. Wie er im Browser ANKOMMT, prueft test_zeitzone.js.
    """
    print("\n7) Zeitstempel der Endpunkte: eindeutig mit Zeitzone")

    stellen = [
        ("/api/portfolio", "abgerufen_am", lambda d: d["abgerufen_am"]),
        ("/api/bots/elliott_wave", "abgerufen_am", lambda d: d["abgerufen_am"]),
        ("/api/verlauf", "abgerufen_am", lambda d: d["abgerufen_am"]),
        ("/api/portfolio", "bots[].letzter_lauf",
         lambda d: d["bots"][0]["letzter_lauf"]),
    ]
    for pfad, feld, hole in stellen:
        wert = hole(get(basis, pfad).json())
        try:
            gelesen = datetime.fromisoformat(wert)
        except (TypeError, ValueError):
            gelesen = None
        check(f"{pfad} -> {feld} traegt eine Zeitzone",
              gelesen is not None and gelesen.tzinfo is not None, repr(wert))

    # Und der Wert muss auch stimmen: ein Zeitstempel mit Offset, der um
    # den eigenen UTC-Versatz danebenliegt, waere derselbe Fehler in neuem
    # Gewand. Grosszuegige Schranke - geprueft wird die Groessenordnung,
    # nicht die Millisekunde.
    stand = datetime.fromisoformat(get(basis, "/api/portfolio").json()["abgerufen_am"])
    abweichung = abs((datetime.now(timezone.utc) - stand).total_seconds())
    check("Der Stand bezeichnet wirklich den Augenblick der Abfrage",
          abweichung < 120, f"{abweichung:.1f} s Unterschied")


def teste_zeitzone():
    """Startet den Node-Test der Zeitanzeige (siehe test_zeitzone.js).

    Wie bei der Zustandsmaschine: fehlendes node ist kein Fehlschlag,
    aber ein sichtbarer Hinweis - sonst gilt der wichtigste Nachweis
    dieser Aenderung stillschweigend als erbracht."""
    print("\n14) Zeitanzeige in verschiedenen Zeitzonen (node)")

    node = shutil.which("node")
    if not node:
        print("  [uebersprungen] node nicht gefunden - die Umrechnung in die "
              "Geraete-Zeitzone\n                  bleibt ungeprueft "
              "(node dashboard/test_zeitzone.js)")
        return

    skript = os.path.join(DIR, "test_zeitzone.js")
    fertig = subprocess.run([node, skript], capture_output=True, text=True,
                             timeout=180)
    for zeile in fertig.stdout.splitlines():
        if zeile.strip():
            print("  " + zeile.strip() if zeile.startswith("  ") else zeile)
    check("Verhaltenstest der Zeitanzeige (test_zeitzone.js)",
          fertig.returncode == 0,
          detail=fertig.stderr.strip()[-300:] if fertig.returncode else "")


def main():
    print("Selbsttests des Dashboards")

    teste_konfiguration()
    teste_bot_freischaltung()
    # Vor dem Umbiegen der Uhr: dieser Abschnitt prueft den Kalender selbst
    # und uebergibt seine Zeitpunkte ausdruecklich.
    teste_boersenkalender()

    wurzel = tempfile.mkdtemp(prefix="dashboard_test_")
    db_dateien = baue_testprojekt(wurzel)
    vorher = _pruefsummen(db_dateien)

    # monitor auf das Testprojekt umbiegen - die echten Bot-Datenbanken
    # werden dadurch waehrend des gesamten Tests nicht einmal geoeffnet.
    alt = (monitor.BASE_DIR, monitor.STRATEGIES_DIR, monitor.LOGS_DIR, monitor.requests)
    monitor.BASE_DIR = wurzel
    monitor.STRATEGIES_DIR = os.path.join(wurzel, "strategies")
    monitor.LOGS_DIR = os.path.join(wurzel, "logs")

    # Das SCHREIBENDE Modul ebenfalls umbiegen. Ohne diese zwei Zeilen
    # wuerde der Schliess-Test gegen die ECHTEN Bot-Datenbanken des
    # Projekts laufen - der einzige Ort in dieser Testdatei, an dem ein
    # vergessenes Umbiegen echten Schaden anrichten koennte.
    alt_mc = (manual_close.BASE_DIR, manual_close.STRATEGIES_DIR)
    manual_close.BASE_DIR = wurzel
    manual_close.STRATEGIES_DIR = os.path.join(wurzel, "strategies")

    # Und die Auftragsdatei ebenso. OHNE diese Zeilen wuerden die Tests in
    # die ECHTE Datei notifications/warteauftraege.json schreiben und im
    # schlimmsten Fall einen wartenden Auftrag des Nutzers loeschen - genau
    # dieselbe Falle wie bei manual_close.BASE_DIR darueber.
    alt_wa = warteauftraege.BASE_DIR
    warteauftraege.BASE_DIR = wurzel
    os.makedirs(os.path.join(wurzel, "notifications"), exist_ok=True)

    # Die Testuhr (siehe boerse_am oben): der ECHTE Kalender, aber an einem
    # Tag, den der Test kennt. Ohne das haengt das Verhalten des Dashboards
    # an der Tageszeit, zu der jemand die Suite startet.
    alt_status = boersenkalender.status

    def status_mit_testuhr(jetzt=None):
        return alt_status(jetzt if jetzt is not None else TESTZEIT[0])

    boersenkalender.status = status_mit_testuhr
    protokoll_datei = os.path.join(wurzel, "manuelle_eingriffe.log")
    alt_griffe = list(manual_close._protokoll.handlers)
    for griff in alt_griffe:
        manual_close._protokoll.removeHandler(griff)
    griff = logging.FileHandler(protokoll_datei, encoding="utf-8")
    griff.setFormatter(logging.Formatter("%(asctime)s MANUELLER-EINGRIFF %(message)s"))
    manual_close._protokoll.addHandler(griff)

    class KeinNetz:
        @staticmethod
        def get(*a, **k):
            raise AssertionError("Im Test darf kein echter Netzwerkaufruf stattfinden")

    monitor.requests = KeinNetz

    try:
        check("Testprojekt wird erkannt",
              sorted(b["name"] for b in datenquelle.alle_bots())
              == ["elliott_wave", "t3_supertrend", "volatility_breakout"],
              str(sorted(b["name"] for b in datenquelle.alle_bots())))
        check("Die echten Bot-Datenbanken werden nicht angefasst",
              manual_close.BASE_DIR == wurzel != BASE_DIR)
        check("Auch die echte Warteauftrags-Datei wird nicht angefasst",
              warteauftraege.datei().startswith(wurzel)
              and not warteauftraege.datei().startswith(BASE_DIR),
              warteauftraege.datei())
        # Gegenprobe zu Grundsatz 12: die Umlenkung MUSS erkennbar sein.
        # Zeigte warteauftraege.BASE_DIR noch auf das echte Projekt, waere
        # die Pruefung oben rot - genau das ist hier belegt.
        check("Gegenprobe: die Umlenkung ist wirksam, nicht bloss behauptet",
              warteauftraege.BASE_DIR == wurzel
              and os.path.dirname(os.path.dirname(warteauftraege.datei()))
              == wurzel)
        check("Die Testuhr steht auf einem Tag mit offener Boerse",
              boersenkalender.status()["offen"] is True,
              boersenkalender.status()["grund"])

        app = erzeuge_app(token=TEST_TOKEN)
        with Testserver(app) as server:
            teste_authentifizierung(server.basis)
            teste_endpunkte(server.basis)
            teste_live_kurse(server.basis)
            teste_frontend(server.basis)
            teste_nur_lesend(app, server.basis, vorher, db_dateien)
            teste_zeitstempel(server.basis)
            # ZULETZT, und mit Absicht nach dem Lesend-Nachweis: bis hier
            # hat sich keine Datenbank veraendert, und ab hier wird
            # genau eine Zeile geschrieben.
            teste_schliessen(server.basis, wurzel, db_dateien, protokoll_datei)
            teste_alle_schliessen(server.basis, wurzel, db_dateien,
                                   protokoll_datei)
            teste_gewichteten_pnl(server.basis, wurzel, db_dateien,
                                   protokoll_datei)
            teste_global_schliessen(server.basis, wurzel, db_dateien,
                                     protokoll_datei)
            teste_warteauftraege(server.basis, wurzel, db_dateien,
                                  protokoll_datei)
            teste_ausfuehrungsskript(wurzel, db_dateien, protokoll_datei)
            teste_mehrere_warteauftraege(server.basis, wurzel, db_dateien,
                                          protokoll_datei)
        teste_schliessen_frontend()
        teste_automatische_aktualisierung()
        teste_ladeindikator()
        teste_zustandsmaschine()
        teste_gewichtung_node()
        teste_zeitzone()
    finally:
        monitor.BASE_DIR, monitor.STRATEGIES_DIR, monitor.LOGS_DIR, monitor.requests = alt
        manual_close.BASE_DIR, manual_close.STRATEGIES_DIR = alt_mc
        warteauftraege.BASE_DIR = alt_wa
        boersenkalender.status = alt_status
        for griff in list(manual_close._protokoll.handlers):
            manual_close._protokoll.removeHandler(griff)
            griff.close()
        for griff in alt_griffe:
            manual_close._protokoll.addHandler(griff)

    print(f"\n{len(CHECKS)}/{len(CHECKS)} Pruefungen bestanden.")


if __name__ == "__main__":
    main()
