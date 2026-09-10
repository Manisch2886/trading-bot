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
  8) Der eine schreibende Pfad schreibt genau das Erwartete: EINE Zeile
     EINER Datenbank, und dort nur die fuenf Ausstiegsfelder. Alle
     anderen Datenbanken bleiben byteweise identisch.

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
import konfig           # noqa: E402
import datenquelle      # noqa: E402
import schliessen       # noqa: E402
from app import erzeuge_app  # noqa: E402

TEST_TOKEN = "test-token-1234567890-abcdefgh"

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append(bool(ok))
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        raise SystemExit(f"\nFEHLGESCHLAGEN: {name}\n{detail}")


# ---------------------------------------------------------------------------
# Synthetische Projektstruktur
# ---------------------------------------------------------------------------

def _lege_bot_an(wurzel: str, name: str, trades: list):
    os.makedirs(os.path.join(wurzel, "strategies", name), exist_ok=True)
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

    return {
        "elliott_wave": _lege_bot_an(wurzel, "elliott_wave", krypto),
        "volatility_breakout": _lege_bot_an(wurzel, "volatility_breakout", aktien),
        "t3_supertrend": _lege_bot_an(wurzel, "t3_supertrend", t3),
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
# hier "genau eine, POST /login". Seit dem manuellen Schliessen sind es
# vier, und nur EINE davon fasst eine Datenbank an. Kommt irgendwann eine
# fuenfte dazu, faellt dieser Test auf - und genau das soll er.
ERLAUBTE_SCHREIB_ROUTEN = [
    ("POST", "/login"),                                        # setzt nur ein Cookie
    ("POST", "/api/bots/{name}/schliessen/vorbereiten"),        # nur Arbeitsspeicher
    ("POST", "/api/bots/{name}/schliessen/abbrechen"),          # nur Arbeitsspeicher
    ("POST", "/api/bots/{name}/schliessen/ausfuehren"),         # <- schreibt
]


def teste_nur_lesend(app, basis, pruefsummen_vorher, db_dateien):
    print("\n6) Nachweis: lesend, ausser dem einen Schliess-Endpunkt")

    schreibende = []
    for route in app.routes:
        methoden = set(getattr(route, "methods", []) or [])
        for methode in methoden & {"POST", "PUT", "PATCH", "DELETE"}:
            schreibende.append((methode, getattr(route, "path", "?")))
    check("Es gibt genau die vier erwarteten Nicht-GET-Routen",
          sorted(schreibende) == sorted(ERLAUBTE_SCHREIB_ROUTEN), str(sorted(schreibende)))
    check("Davon fasst genau EINE eine Datenbank an (…/schliessen/ausfuehren)",
          len([r for r in schreibende if r[1].endswith("/ausfuehren")]) == 1)

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

        fremd = get(basis, "/api/bots/elliott_wave/schliessbare-positionen").json()
        check("elliott_wave meldet sich als nicht freigeschaltet",
              fremd["schliessbar"] is False and "t3_supertrend" in fremd["grund"])

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
        for bot in ("elliott_wave", "volatility_breakout"):
            antwort = post(basis, f"/api/bots/{bot}/schliessen/vorbereiten",
                            {"trade_id": 1})
            check(f"Vorbereiten fuer {bot}: 403", antwort.status_code == 403,
                  str(antwort.status_code))
            antwort = _ausfuehren(basis, vorbereitet["vorgang"], bot=bot)
            check(f"Ausfuehren fuer {bot}: 403", antwort.status_code == 403,
                  str(antwort.status_code))
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
        quelltext_app = open(os.path.join(DIR, "app.py"), encoding="utf-8").read()
        check("Der Endpunkt liest kein 'bestaetigung' mehr aus dem Koerper",
              'get("bestaetigung")' not in quelltext_app)
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
        manual_close.SCHLIESSBARE_BOTS["elliott_wave"] = {
            "anzeigename": "Elliott Wave (Krypto)", "anlageklasse": "krypto"}
        try:
            fremder = _vorbereiten(basis, bot="elliott_wave", trade_id=4).json()
            check("Vorbereiten fuer den zweiten Bot gelingt (Erweiterbarkeit)",
                  bool(fremder.get("vorgang")), str(fremder)[:100])
        finally:
            manual_close.SCHLIESSBARE_BOTS.pop("elliott_wave", None)
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
        check("Nach dem Test ist wieder genau ein Bot freigeschaltet",
              list(manual_close.SCHLIESSBARE_BOTS) == ["t3_supertrend"])

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


def teste_schliessen_frontend():
    print("\n9) Frontend des Schliessvorgangs")
    statisch = os.path.join(DIR, "static")
    bot_html = open(os.path.join(statisch, "bot.html"), encoding="utf-8").read()
    app_js = open(os.path.join(statisch, "app.js"), encoding="utf-8").read()
    code = ohne_kommentare(bot_html)

    check("Es gibt einen echten <dialog> statt eines nachgebauten Overlays",
          "<dialog" in code and "showModal()" in code)

    # EIN Schritt: die Zusammenfassung ist schon der vorbereiten-Aufruf, der
    # Knopf darunter der ausfuehren-Aufruf. Die frueheren zwei Stufen samt
    # Texteingabe sind weg - und sollen nicht unbemerkt zurueckkehren.
    check("Keine zweite Stufe mehr im Markup",
          'id="dialog-stufe1"' not in code and 'id="dialog-stufe2"' not in code)
    check("Keine Texteingabe mehr im Dialog",
          'id="dialog-eingabe"' not in code and "<input" not in code)
    check("Keine Schritt-Anzeige mehr ('Schritt 1 von 2')",
          "von 2" not in code and 'id="dialog-stufe"' not in code)
    check("Genau EIN Abbrechen-Knopf",
          code.count('id="dialog-abbrechen"') == 1
          and 'id="dialog-abbrechen1"' not in code
          and 'id="dialog-abbrechen2"' not in code)
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
    print("\n10) Automatische Aktualisierung (Quelltext)")

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
    print("\n11) Ladeindikator (Auszeichnung und Stil)")

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
    print("\n12) Verhalten der Zustandsmaschine (node)")

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
    print("\n13) Zeitanzeige in verschiedenen Zeitzonen (node)")

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
        teste_schliessen_frontend()
        teste_automatische_aktualisierung()
        teste_ladeindikator()
        teste_zustandsmaschine()
        teste_zeitzone()
    finally:
        monitor.BASE_DIR, monitor.STRATEGIES_DIR, monitor.LOGS_DIR, monitor.requests = alt
        manual_close.BASE_DIR, manual_close.STRATEGIES_DIR = alt_mc
        for griff in list(manual_close._protokoll.handlers):
            manual_close._protokoll.removeHandler(griff)
            griff.close()
        for griff in alt_griffe:
            manual_close._protokoll.addHandler(griff)

    print(f"\n{len(CHECKS)}/{len(CHECKS)} Pruefungen bestanden.")


if __name__ == "__main__":
    main()
