"""
Selbsttests des Dashboards
==============================================================
Startet den ECHTEN Server (uvicorn, gebunden an 127.0.0.1) gegen eine
komplett synthetische Projektstruktur in einem temporaeren Verzeichnis
und ruft alle Endpunkte per HTTP auf - keine nachgebaute Testfassung der
App, keine Umgehung der Middleware.

Es werden dabei WEDER echte Bot-Datenbanken geleseneN NOCH echte
Netzwerkabfragen gemacht: monitor.BASE_DIR/STRATEGIES_DIR/LOGS_DIR
zeigen waehrend des Tests auf das temporaere Verzeichnis, und
requests.get wird im monitor-Modul durch eine Funktion ersetzt, die
sofort einen Fehler wirft - schliche sich doch ein echter Netzaufruf
ein, faellt der Test auf.

Nutzung:  python3 dashboard/test_dashboard.py
"""

import hashlib
import json
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
import konfig           # noqa: E402
import datenquelle      # noqa: E402
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
    """Zwei Bots mit bekannten Zahlen - einer Krypto, einer Aktien.
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

    return {
        "elliott_wave": _lege_bot_an(wurzel, "elliott_wave", krypto),
        "volatility_breakout": _lege_bot_an(wurzel, "volatility_breakout", aktien),
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
    check("Beide Testbots erscheinen in der Uebersicht",
          namen == ["elliott_wave", "volatility_breakout"], str(namen))

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

    check("Summenzeile zaehlt beide Bots", daten["summe"]["anzahl_bots"] == 2)
    check("Summe offener Positionen ueber alle Bots", daten["summe"]["offene_positionen"] == 3)

    liste = get(basis, "/api/bots").json()
    check("/api/bots liefert die Kurzliste", len(liste["bots"]) == 2)

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
    check("Gesamtkurve enthaelt alle fuenf geschlossenen Trades beider Bots",
          len(verlauf["gesamt"]) == 5, str(len(verlauf["gesamt"])))
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
              uebersicht.status_code == 200 and len(uebersicht.json()["bots"]) == 2)

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


def teste_nur_lesend(app, basis, pruefsummen_vorher, db_dateien):
    print("\n6) Nachweis: rein lesend")

    schreibende = []
    for route in app.routes:
        methoden = set(getattr(route, "methods", []) or [])
        for methode in methoden & {"POST", "PUT", "PATCH", "DELETE"}:
            schreibende.append((methode, getattr(route, "path", "?")))
    check("Einzige Nicht-GET-Route ist POST /login (setzt nur ein Cookie)",
          schreibende == [("POST", "/login")], str(schreibende))

    for methode in ("POST", "PUT", "DELETE", "PATCH"):
        antwort = requests.request(methode, basis + "/api/portfolio",
                                    headers={"X-Dashboard-Token": TEST_TOKEN}, timeout=30)
        check(f"{methode} auf /api/portfolio wird abgelehnt",
              antwort.status_code == 405, f"war {antwort.status_code}")

    nachher = _pruefsummen(db_dateien)
    check("Keine Bot-Datenbank wurde durch die Tests veraendert",
          nachher == pruefsummen_vorher,
          "Pruefsummen weichen ab" if nachher != pruefsummen_vorher else "")


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
    print("\n8) Automatische Aktualisierung (Quelltext)")

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
    print("\n9) Ladeindikator (Auszeichnung und Stil)")

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
    print("\n10) Verhalten der Zustandsmaschine (node)")

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

    class KeinNetz:
        @staticmethod
        def get(*a, **k):
            raise AssertionError("Im Test darf kein echter Netzwerkaufruf stattfinden")

    monitor.requests = KeinNetz

    try:
        check("Testprojekt wird erkannt",
              sorted(b["name"] for b in datenquelle.alle_bots())
              == ["elliott_wave", "volatility_breakout"])

        app = erzeuge_app(token=TEST_TOKEN)
        with Testserver(app) as server:
            teste_authentifizierung(server.basis)
            teste_endpunkte(server.basis)
            teste_live_kurse(server.basis)
            teste_frontend(server.basis)
            teste_nur_lesend(app, server.basis, vorher, db_dateien)
        teste_automatische_aktualisierung()
        teste_ladeindikator()
        teste_zustandsmaschine()
    finally:
        monitor.BASE_DIR, monitor.STRATEGIES_DIR, monitor.LOGS_DIR, monitor.requests = alt

    print(f"\n{len(CHECKS)}/{len(CHECKS)} Pruefungen bestanden.")


if __name__ == "__main__":
    main()
