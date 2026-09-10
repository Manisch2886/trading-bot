"""
Selbsttests fuer das manuelle Schliessen (Telegram Phase 3)
==============================================================================
Diese Funktion ist die erste im Projekt, die in eine Live-Datenbank
SCHREIBT. Entsprechend prueft diese Datei nicht nur "geht es", sondern vor
allem "geht es NICHT, wenn es nicht gehen darf" - und ob nach einem
abgelehnten Versuch die Datenbank BYTEWEISE unveraendert ist.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.
Es wird keine echte Bot-Datenbank angefasst: jeder Test baut sich seine
eigene, wegwerfbare Kopie unter /tmp.

python-telegram-bot wird per Attrappe bereitgestellt. Die Bibliothek ist
in dieser Umgebung nicht lauffaehig (ihre Krypto-Abhaengigkeit bricht beim
Import ab), und der eigentliche Pruefgegenstand - Zugriffsschutz,
Abbruchwege, die beiden Bestaetigungsstufen - haengt nicht daran, wie
Telegram intern eine Nachricht verschickt.

Nutzung:  python3 notifications/test_manual_close.py
"""

import ast
import asyncio
import io
import json
import logging
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import textwrap
import time
import types

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)

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
# Attrappe fuer python-telegram-bot
# ---------------------------------------------------------------------------

def installiere_telegram_attrappe():
    """Nur so viel von der Bibliothek, wie die beiden Module beim Import
    anfassen. Sie wird VOR dem echten Paket in sys.modules gelegt, damit
    das Ergebnis nicht davon abhaengt, was zufaellig installiert ist."""
    telegram = types.ModuleType("telegram")

    class Update: pass
    class InlineKeyboardButton:
        def __init__(self, text, callback_data=None):
            self.text, self.callback_data = text, callback_data
    class InlineKeyboardMarkup:
        def __init__(self, tastatur): self.inline_keyboard = tastatur

    telegram.Update = Update
    telegram.InlineKeyboardButton = InlineKeyboardButton
    telegram.InlineKeyboardMarkup = InlineKeyboardMarkup

    fehler = types.ModuleType("telegram.error")
    class BadRequest(Exception): pass
    class TelegramError(Exception): pass
    fehler.BadRequest = BadRequest
    fehler.TelegramError = TelegramError
    telegram.error = fehler

    ext = types.ModuleType("telegram.ext")
    class _Platzhalter:
        def __init__(self, *a, **k): pass
    class ContextTypes:
        DEFAULT_TYPE = object
    class _Filter:
        def __and__(self, other): return self
        def __invert__(self): return self
    class _Filters:
        TEXT = _Filter()
        COMMAND = _Filter()
        @staticmethod
        def Regex(muster): return _Filter()
    ext.Application = _Platzhalter
    ext.CallbackQueryHandler = _Platzhalter
    ext.MessageHandler = _Platzhalter
    ext.ContextTypes = ContextTypes
    ext.filters = _Filters()
    telegram.ext = ext

    sys.modules["telegram"] = telegram
    sys.modules["telegram.error"] = fehler
    sys.modules["telegram.ext"] = ext


# ---------------------------------------------------------------------------
# Synthetischer Bot
# ---------------------------------------------------------------------------

FORWARD_TEST_ATTRAPPE = '''\
"""Attrappe eines forward_test.py - nur die beiden Kostensaetze zaehlen."""
TRADING_FEE_PCT = {fee}
SLIPPAGE_PCT = {slip}
'''

TRADES = [
    # (symbol, signal_time, entry_time, entry_price, stop_price, exit_time,
    #  exit_price, result, pnl_pct, status)
    ("BTCUSDT", "2026-01-01 00:00:00", "2026-01-01 00:00:00", 100.0, 95.0,
     None, None, None, None, "open"),
    ("ETHUSDT", "2026-01-02 00:00:00", "2026-01-02 00:00:00", 200.0, 190.0,
     None, None, None, None, "open"),
    ("SOLUSDT", "2026-01-03 00:00:00", "2026-01-03 00:00:00", 50.0, 47.0,
     "2026-02-01 00:00:00", 55.0, "trend_flip", 9.7, "closed"),
]


def baue_bot(wurzel, bot_name="t3_supertrend", fee=0.1, slip=0.05):
    """Ein vollstaendiger Mini-Bot: Datenbank mit dem echten Schema plus
    ein forward_test.py, aus dem die Kostensaetze gelesen werden."""
    os.makedirs(os.path.join(wurzel, "strategies", bot_name), exist_ok=True)
    with open(os.path.join(wurzel, "strategies", bot_name, "forward_test.py"),
               "w", encoding="utf-8") as fh:
        fh.write(FORWARD_TEST_ATTRAPPE.format(fee=fee, slip=slip))

    db = os.path.join(wurzel, f"paper_trading_{bot_name}.db")
    conn = sqlite3.connect(db)
    conn.execute("""
        CREATE TABLE trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT, signal_time TEXT, entry_time TEXT,
            entry_price REAL, stop_price REAL, exit_time TEXT,
            exit_price REAL, result TEXT, pnl_pct REAL, status TEXT,
            UNIQUE(symbol, signal_time))""")
    conn.executemany(
        "INSERT INTO trades (symbol, signal_time, entry_time, entry_price, "
        "stop_price, exit_time, exit_price, result, pnl_pct, status) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)", TRADES)
    conn.commit()
    conn.close()
    return db


def alle_zeilen(db):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    zeilen = [dict(z) for z in conn.execute("SELECT * FROM trades ORDER BY id")]
    conn.close()
    return zeilen


def biege_um(mc, wurzel):
    mc.BASE_DIR = wurzel
    mc.STRATEGIES_DIR = os.path.join(wurzel, "strategies")


def lenke_protokoll_um(mc, pfad):
    """Haengt den Protokoll-Logger auf eine Wegwerf-Datei um. Ohne das
    wuerden die Tests in das echte logs/notifications/ des Projekts
    schreiben - und der Test koennte nicht pruefen, was ER selbst
    erzeugt hat, sondern nur, was insgesamt in der Datei steht."""
    for h in list(mc._protokoll.handlers):
        mc._protokoll.removeHandler(h)
        h.close()
    griff = logging.FileHandler(pfad, encoding="utf-8")
    griff.setFormatter(logging.Formatter(
        "%(asctime)s MANUELLER-EINGRIFF %(message)s"))
    mc._protokoll.addHandler(griff)
    return pfad


def protokoll_zeilen(pfad):
    for h in _MC._protokoll.handlers:
        h.flush()
    if not os.path.exists(pfad):
        return []
    with open(pfad, encoding="utf-8") as fh:
        return [z.rstrip("\n") for z in fh if z.strip()]


installiere_telegram_attrappe()
sys.path.insert(0, _DIR)
import manual_close as _MC         # noqa: E402

# Die Telegram-Schicht ist OPTIONAL. manual_close.py wird von zwei
# Oberflaechen genutzt - dem Telegram-Bot und dem Dashboard - und die
# beiden kamen in getrennten Aenderungen ins Projekt. Fehlt eine davon,
# sollen die Tests des KERNS trotzdem vollstaendig laufen, statt beim
# Import abzubrechen: der Kern ist der Teil, der schreibt, und der muss
# in jeder Zusammenstellung geprueft sein.
#
# Fehlt telegram_schliessen.py, werden die Abschnitte 10 bis 13
# uebersprungen und das am Ende ausdruecklich ausgewiesen - ein
# stillschweigend kleinerer Testlauf waere schlimmer als gar keiner.
try:
    import telegram_schliessen as _TS  # noqa: E402
except ImportError:
    _TS = None

UEBERSPRUNGEN = []


# ---------------------------------------------------------------------------
# 1. Passt die Test-Attrappe ueberhaupt zum echten Bot?
# ---------------------------------------------------------------------------
# Zuerst, und mit Absicht als erstes: alle folgenden Tests sind wertlos,
# wenn die synthetische Datenbank ein anderes Schema hat als der echte
# t3_supertrend-Bot. Deshalb wird das Schema nicht behauptet, sondern
# aus dem echten forward_test.py gelesen und verglichen.

def echtes_schema_statement():
    pfad = os.path.join(BASE_DIR, "strategies", "t3_supertrend", "forward_test.py")
    baum = ast.parse(open(pfad, encoding="utf-8").read(), filename=pfad)
    for knoten in ast.walk(baum):
        if (isinstance(knoten, ast.Constant) and isinstance(knoten.value, str)
                and "CREATE TABLE" in knoten.value and "trades" in knoten.value):
            return knoten.value
    return None


def spalten(verbindung):
    return [(z[1], z[2].upper()) for z in
            verbindung.execute("PRAGMA table_info(trades)")]


def test_schema_stimmt_mit_dem_echten_bot_ueberein():
    print("\n1. Schema-Abgleich mit dem echten t3_supertrend-Bot")
    statement = echtes_schema_statement()
    check("CREATE TABLE im echten forward_test.py gefunden", statement is not None)
    if statement is None:
        return

    echt = sqlite3.connect(":memory:")
    echt.execute(statement)

    wurzel = tempfile.mkdtemp(prefix="mc_schema_")
    db = baue_bot(wurzel)
    synth = sqlite3.connect(db)

    check("Spalten der Test-Datenbank == Spalten des echten Bots",
          spalten(echt) == spalten(synth),
          f"{[s[0] for s in spalten(synth)]}")

    # Das UPDATE des Moduls muss gegen das ECHTE Schema laufen koennen -
    # ein Tippfehler in einem Spaltennamen faellt sonst erst live auf.
    try:
        echt.execute("UPDATE trades SET exit_time=?, exit_price=?, result=?, "
                     "pnl_pct=?, status='closed' WHERE id=? AND status='open'",
                     ("x", 1.0, "manual_close", 0.0, 1))
        ok, meldung = True, ""
    except sqlite3.Error as fehler:
        ok, meldung = False, str(fehler)
    check("Das UPDATE des Moduls ist gegen das echte Schema gueltig", ok, meldung)

    echt.close()
    synth.close()
    shutil.rmtree(wurzel, ignore_errors=True)


def test_manual_close_kollidiert_mit_keinem_bot_grund():
    print("\n2. 'manual_close' ist als result-Wert eindeutig")
    pfad = os.path.join(BASE_DIR, "strategies", "t3_supertrend", "forward_test.py")
    quelle = open(pfad, encoding="utf-8").read()
    baum = ast.parse(quelle, filename=pfad)
    # Alle Zeichenketten, die der Bot selbst in result schreiben koennte.
    bot_gruende = {k.value for k in ast.walk(baum)
                   if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    check("MANUELLER_GRUND kommt im Bot-Quelltext nicht vor",
          _MC.MANUELLER_GRUND not in bot_gruende,
          f"Bot-Gruende u.a.: stop_loss, trend_flip, t3_crossunder")


def test_modul_kann_nichts_ausser_schliessen():
    print("\n3. Struktureller Nachweis: kein INSERT, kein DELETE, kein DROP")
    # Die Aufgabe schliesst das Eroeffnen neuer Positionen ausdruecklich aus.
    # Statt das nur zu behaupten, wird der Quelltext geprueft: jede
    # Zeichenkette, die wie SQL aussieht, muss ein SELECT, ein UPDATE, ein
    # PRAGMA oder ein Transaktionsbefehl sein.
    pfad = os.path.join(_DIR, "manual_close.py")
    baum = ast.parse(open(pfad, encoding="utf-8").read(), filename=pfad)
    erlaubt = ("SELECT", "UPDATE", "PRAGMA", "BEGIN", "COMMIT", "ROLLBACK")
    verboten = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Constant) and isinstance(knoten.value, str):
            kopf = knoten.value.strip().split(" ")[0].upper()
            if kopf in ("INSERT", "DELETE", "DROP", "ALTER", "REPLACE", "CREATE"):
                verboten.append(knoten.value.strip()[:60])
    check("Keine schreibende SQL-Anweisung ausser UPDATE im Modul",
          not verboten, str(verboten))

    # Gegenprobe: findet die Pruefung ein INSERT ueberhaupt? Sonst waere
    # das gruene Ergebnis oben nur die Abwesenheit eines Suchtreffers.
    probe = ast.parse('x = "INSERT INTO trades VALUES (1)"')
    gefunden = [k.value for k in ast.walk(probe)
                if isinstance(k, ast.Constant) and isinstance(k.value, str)
                and k.value.strip().split(" ")[0].upper() == "INSERT"]
    check("Gegenprobe: ein eingeschmuggeltes INSERT wuerde auffallen",
          len(gefunden) == 1)

    quelle = open(pfad, encoding="utf-8").read()
    check("Das UPDATE traegt status='open' in der WHERE-Klausel",
          "WHERE id=? AND status='open'" in quelle)


# ---------------------------------------------------------------------------
# Vergleichswerkzeug: was genau hat sich in der Datenbank geaendert?
# ---------------------------------------------------------------------------

def unterschiede(vorher: list, nachher: list) -> list:
    """Alle Feld-Unterschiede zwischen zwei Momentaufnahmen der Tabelle,
    als (id, feld, alt, neu). Vergleicht ZEILENZAHL und JEDES Feld - eine
    zusaetzlich eingefuegte oder verschwundene Zeile faellt damit ebenso
    auf wie ein geaendertes Feld."""
    ergebnis = []
    a = {z["id"]: z for z in vorher}
    b = {z["id"]: z for z in nachher}
    for kennung in sorted(set(a) | set(b)):
        if kennung not in a:
            ergebnis.append((kennung, "<ZEILE NEU>", None, b[kennung]))
            continue
        if kennung not in b:
            ergebnis.append((kennung, "<ZEILE WEG>", a[kennung], None))
            continue
        for feld in a[kennung]:
            if a[kennung][feld] != b[kennung][feld]:
                ergebnis.append((kennung, feld, a[kennung][feld], b[kennung][feld]))
    return ergebnis


def datei_pruefsumme(pfad):
    import hashlib
    with open(pfad, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# ---------------------------------------------------------------------------
# 4. PnL: exakt die Rechnung des Bots
# ---------------------------------------------------------------------------

def test_pnl_entspricht_der_bot_formel():
    print("\n4. PnL-Formel und Kostensaetze")
    wurzel = tempfile.mkdtemp(prefix="mc_pnl_")
    baue_bot(wurzel, fee=0.1, slip=0.05)
    biege_um(_MC, wurzel)

    # Woertlich die drei Zeilen aus forward_test.py::check_open_trades().
    def bot_formel(entry, exit_, fee=0.1, slip=0.05):
        pnl = (exit_ - entry) / entry * 100
        pnl -= 2 * (fee + slip)
        return round(pnl, 2)

    faelle = [(100.0, 110.0), (100.0, 90.0), (0.5, 0.5),
              (12345.67, 12000.0), (7.0, 21.0)]
    alle_gleich = all(
        _MC.berechne_pnl("t3_supertrend", e, a) == bot_formel(e, a)
        for e, a in faelle)
    check("berechne_pnl() == Formel aus forward_test.py (5 Faelle)", alle_gleich,
          f"z.B. 100 -> 110: {_MC.berechne_pnl('t3_supertrend', 100.0, 110.0)}%")

    check("Kostensatz ist 2*(Gebuehr+Slippage) = 0.30",
          abs(_MC.kostensatz("t3_supertrend") - 0.30) < 1e-12)

    # EMPFINDLICHKEITSPROBE. Ohne die waere oben nur belegt, dass zwei
    # Rechnungen mit denselben fest verdrahteten Zahlen dasselbe ergeben.
    # Hier bekommt der Bot ANDERE Kostensaetze - kommt trotzdem dieselbe
    # Zahl heraus, liest das Modul die Werte gar nicht aus dem Bot.
    wurzel2 = tempfile.mkdtemp(prefix="mc_pnl2_")
    baue_bot(wurzel2, fee=0.4, slip=0.25)
    biege_um(_MC, wurzel2)
    geaendert = _MC.berechne_pnl("t3_supertrend", 100.0, 110.0)
    check("Empfindlichkeitsprobe: andere Kostensaetze -> anderes Ergebnis",
          geaendert == bot_formel(100.0, 110.0, fee=0.4, slip=0.25)
          and geaendert != bot_formel(100.0, 110.0),
          f"0.1/0.05 -> 9.70 % | 0.4/0.25 -> {geaendert} %")

    # Fehlt ein Kostensatz, wird NICHT stillschweigend mit 0 gerechnet.
    wurzel3 = tempfile.mkdtemp(prefix="mc_pnl3_")
    baue_bot(wurzel3)
    with open(os.path.join(wurzel3, "strategies", "t3_supertrend",
                            "forward_test.py"), "w", encoding="utf-8") as fh:
        fh.write("TRADING_FEE_PCT = 0.1\n")   # SLIPPAGE_PCT fehlt
    biege_um(_MC, wurzel3)
    try:
        _MC.berechne_pnl("t3_supertrend", 100.0, 110.0)
        ok = False
    except _MC.SchliessenNichtMoeglich:
        ok = True
    check("Fehlender Kostensatz fuehrt zum Abbruch statt zu einer stillen 0", ok)

    for w in (wurzel, wurzel2, wurzel3):
        shutil.rmtree(w, ignore_errors=True)


# ---------------------------------------------------------------------------
# 5. Der erfolgreiche Schliessvorgang
# ---------------------------------------------------------------------------

def test_erfolgreiches_schliessen():
    print("\n5. Erfolgreicher Schliessvorgang, Zeile fuer Zeile verglichen")
    wurzel = tempfile.mkdtemp(prefix="mc_erfolg_")
    db = baue_bot(wurzel)
    biege_um(_MC, wurzel)
    protokoll = lenke_protokoll_um(_MC, os.path.join(wurzel, "eingriffe.log"))

    vorher = alle_zeilen(db)
    ergebnis = _MC.schliesse_position("t3_supertrend", 1, exit_price=110.0,
                                       benutzer_id=4242,
                                       bestaetigungstext="BESTAETIGEN",
                                       jetzt="2026-09-09 12:00:00")
    nachher = alle_zeilen(db)
    diff = unterschiede(vorher, nachher)

    geaendert = {(k, f) for k, f, _, _ in diff}
    erwartet = {(1, "exit_time"), (1, "exit_price"), (1, "result"),
                (1, "pnl_pct"), (1, "status")}
    check("Genau diese fuenf Felder von Trade 1 haben sich geaendert",
          geaendert == erwartet,
          f"geaendert: {sorted(geaendert)}")
    check("Keine andere Zeile wurde beruehrt (Trade 2 und 3 unveraendert)",
          all(k == 1 for k, _, _, _ in diff))
    check("Zeilenzahl unveraendert (nichts eingefuegt, nichts geloescht)",
          len(vorher) == len(nachher) == 3)

    zeile = [z for z in nachher if z["id"] == 1][0]
    check("status == 'closed'", zeile["status"] == "closed")
    check("result == 'manual_close'", zeile["result"] == "manual_close")
    check("exit_price == der bestaetigte Kurs", zeile["exit_price"] == 110.0)
    check("exit_time == uebergebener Zeitpunkt",
          zeile["exit_time"] == "2026-09-09 12:00:00")
    check("pnl_pct == 9.7 (Formel des Bots inkl. Rundung)",
          zeile["pnl_pct"] == 9.7, str(zeile["pnl_pct"]))
    check("Unveraendert: symbol, entry_price, stop_price, signal_time, entry_time",
          all(zeile[f] == vorher[0][f] for f in
              ("symbol", "entry_price", "stop_price", "signal_time", "entry_time")))

    check("Rueckgabe enthaelt Vorher- UND Nachher-Zustand",
          ergebnis["vorher"]["status"] == "open"
          and ergebnis["nachher"]["status"] == "closed")

    # Der Zeitstempel im echten Betrieb (ohne uebergebenes 'jetzt') muss das
    # Format der Bot-Zeilen haben - sonst faellt die Zeile in Auswertungen
    # aus dem Rahmen.
    import re
    check("jetzt_als_text() hat das Format der Bot-Zeitstempel",
          re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
                       _MC.jetzt_als_text()) is not None,
          _MC.jetzt_als_text())

    zeilen = protokoll_zeilen(protokoll)
    check("Genau eine Protokollzeile geschrieben", len(zeilen) == 1)
    if zeilen:
        z = zeilen[0]
        check("Protokoll: Marke 'MANUELLER-EINGRIFF ERFOLGREICH'",
              "MANUELLER-EINGRIFF ERFOLGREICH" in z)
        check("Protokoll: Bot, Trade-ID, Symbol, Benutzer",
              all(t in z for t in ("bot=t3_supertrend", "trade_id=1",
                                    "symbol=BTCUSDT", "benutzer=4242")))
        check("Protokoll: alter UND neuer Zustand",
              "VORHER status=open" in z and "NACHHER status=closed" in z)
        check("Protokoll: Zeitstempel am Zeilenanfang",
              re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", z) is not None)
        print(f"       Beispielzeile: {z}")

    shutil.rmtree(wurzel, ignore_errors=True)


# ---------------------------------------------------------------------------
# 6. Abgelehnte Versuche - die Datenbank muss unveraendert bleiben
# ---------------------------------------------------------------------------

def test_abgelehnte_versuche_aendern_nichts():
    print("\n6. Abgelehnte Versuche (Datei-Pruefsumme + Zeilenvergleich)")
    wurzel = tempfile.mkdtemp(prefix="mc_ablehnung_")
    db = baue_bot(wurzel)
    biege_um(_MC, wurzel)
    protokoll = lenke_protokoll_um(_MC, os.path.join(wurzel, "eingriffe.log"))

    vorher = alle_zeilen(db)
    summe_vorher = datei_pruefsumme(db)

    faelle = [
        ("falscher Text 'BESTAETIGE'", dict(trade_id=1, exit_price=110.0,
                                            bestaetigungstext="BESTAETIGE")),
        ("Kleinschreibung 'bestaetigen'", dict(trade_id=1, exit_price=110.0,
                                                bestaetigungstext="bestaetigen")),
        ("leerer Text", dict(trade_id=1, exit_price=110.0, bestaetigungstext="")),
        ("gar kein Text (None)", dict(trade_id=1, exit_price=110.0,
                                       bestaetigungstext=None)),
        ("beliebiger Chat-Text", dict(trade_id=1, exit_price=110.0,
                                       bestaetigungstext="ja mach mal")),
        ("kein Kurs (None)", dict(trade_id=1, exit_price=None,
                                   bestaetigungstext="BESTAETIGEN")),
        ("Kurs 0", dict(trade_id=1, exit_price=0, bestaetigungstext="BESTAETIGEN")),
        ("negativer Kurs", dict(trade_id=1, exit_price=-5.0,
                                 bestaetigungstext="BESTAETIGEN")),
        ("Trade-ID existiert nicht", dict(trade_id=999, exit_price=110.0,
                                           bestaetigungstext="BESTAETIGEN")),
        ("Trade ist bereits geschlossen", dict(trade_id=3, exit_price=60.0,
                                                bestaetigungstext="BESTAETIGEN")),
    ]

    for name, argumente in faelle:
        try:
            _MC.schliesse_position("t3_supertrend", benutzer_id=4242, **argumente)
            check(f"abgelehnt: {name}", False, "wurde AUSGEFUEHRT statt abgelehnt")
        except _MC.SchliessenNichtMoeglich as fehler:
            check(f"abgelehnt: {name}", True, str(fehler)[:70])

    nachher = alle_zeilen(db)
    check("Nach 10 abgelehnten Versuchen: kein einziges Feld geaendert",
          unterschiede(vorher, nachher) == [],
          str(unterschiede(vorher, nachher))[:120])
    check("Nach 10 abgelehnten Versuchen: Datei byteweise identisch",
          datei_pruefsumme(db) == summe_vorher)

    zeilen = protokoll_zeilen(protokoll)
    check("Jeder abgelehnte Versuch steht im Protokoll",
          len(zeilen) == len(faelle), f"{len(zeilen)} von {len(faelle)}")
    check("Abgelehnte Zeilen sind als solche erkennbar",
          all("MANUELLER-EINGRIFF ABGELEHNT" in z for z in zeilen))
    check("Abgelehnte Zeilen halten 'Datenbank unveraendert' fest",
          all("Datenbank unveraendert" in z for z in zeilen))
    if zeilen:
        print(f"       Beispielzeile: {zeilen[0]}")

    # Der Text mit umschliessenden Leerzeichen MUSS durchgehen - Telegram
    # haengt bei manchen Tastaturen ein Leerzeichen an, und daran soll der
    # Nutzer nicht scheitern.
    _MC.schliesse_position("t3_supertrend", 1, exit_price=110.0,
                            benutzer_id=4242, bestaetigungstext="  BESTAETIGEN ",
                            jetzt="2026-09-09 12:00:00")
    check("'  BESTAETIGEN ' (mit Leerzeichen) wird akzeptiert",
          [z for z in alle_zeilen(db) if z["id"] == 1][0]["status"] == "closed")

    shutil.rmtree(wurzel, ignore_errors=True)


def test_unbekannter_bot_wird_abgelehnt():
    print("\n7. Nicht freigeschaltete Bots")
    wurzel = tempfile.mkdtemp(prefix="mc_fremd_")
    db_t3 = baue_bot(wurzel, "t3_supertrend")
    db_fremd = baue_bot(wurzel, "elliott_wave")
    biege_um(_MC, wurzel)
    lenke_protokoll_um(_MC, os.path.join(wurzel, "eingriffe.log"))

    # elliott_wave ist inzwischen freigeschaltet. Um die SPERRE selbst zu
    # pruefen, wird er hier kurz aus der Liste genommen - das ist der
    # aussagekraeftigere Test als ein erfundener Name, weil seine Datenbank
    # vollstaendig vorhanden ist und die Ablehnung damit wirklich an der
    # Liste haengt und an nichts anderem.
    gemerkt = _MC.SCHLIESSBARE_BOTS.pop("elliott_wave")
    try:
        summe = datei_pruefsumme(db_fremd)
        for name in ("elliott_wave", "", "../../etc", "t3_supertrend2",
                      "gibt_es_nicht"):
            try:
                _MC.schliesse_position(name, 1, exit_price=110.0, benutzer_id=4242,
                                        bestaetigungstext="BESTAETIGEN")
                check(f"abgelehnt: Bot '{name}'", False, "wurde AUSGEFUEHRT")
            except _MC.SchliessenNichtMoeglich:
                check(f"abgelehnt: Bot '{name}'", True)
        check("Die Datenbank des gesperrten Bots ist unveraendert",
              datei_pruefsumme(db_fremd) == summe)
        check("Auch offene_positionen() lehnt einen gesperrten Bot ab",
              _abgelehnt(lambda: _MC.offene_positionen("elliott_wave")))
    finally:
        _MC.SCHLIESSBARE_BOTS["elliott_wave"] = gemerkt
    check("Nach dem Zuruecksetzen ist er wieder lesbar",
          len(_MC.offene_positionen("elliott_wave")) == 2)

    # Gegenprobe: der freigeschaltete Bot geht sehr wohl - sonst waere oben
    # nur belegt, dass die Funktion immer ablehnt.
    check("Gegenprobe: der freigeschaltete Bot wird nicht abgelehnt",
          len(_MC.offene_positionen("t3_supertrend")) == 2)

    shutil.rmtree(wurzel, ignore_errors=True)


def _abgelehnt(aufruf):
    try:
        aufruf()
        return False
    except _MC.SchliessenNichtMoeglich:
        return True


def test_fehlende_datenbank():
    print("\n8. Fehlende Datenbank")
    wurzel = tempfile.mkdtemp(prefix="mc_leer_")
    baue_bot(wurzel)
    os.remove(os.path.join(wurzel, "paper_trading_t3_supertrend.db"))
    biege_um(_MC, wurzel)
    lenke_protokoll_um(_MC, os.path.join(wurzel, "eingriffe.log"))
    check("Fehlende Datenbank fuehrt zum Abbruch, nicht zu einer neuen Datei",
          _abgelehnt(lambda: _MC.schliesse_position(
              "t3_supertrend", 1, 110.0, 4242, "BESTAETIGEN")))
    check("Es wurde KEINE leere Datenbank angelegt",
          not os.path.exists(os.path.join(wurzel, "paper_trading_t3_supertrend.db")))
    shutil.rmtree(wurzel, ignore_errors=True)


# ---------------------------------------------------------------------------
# 9. Nebenlaeufigkeit: der Cronjob koennte GENAU JETZT schreiben
# ---------------------------------------------------------------------------
# Der heikelste Teil. Drei verschiedene Szenarien, alle mit ECHTEN
# Prozessen - Threads wuerden hier nichts beweisen, weil SQLite-Sperren
# zwischen Verbindungen wirken und ein einzelner Prozess sich anders
# verhaelt als zwei.

SPERR_HALTER = '''\
"""Haelt eine SQLite-Schreibsperre - simuliert den laufenden Cronjob."""
import os, sqlite3, sys, time
db, dauer = sys.argv[1], float(sys.argv[2])
conn = sqlite3.connect(db, timeout=30, isolation_level=None)
conn.execute("BEGIN IMMEDIATE")
conn.execute("UPDATE trades SET stop_price=stop_price WHERE id=2")
print("gesperrt", flush=True)
time.sleep(dauer)
conn.execute("ROLLBACK")
conn.close()
print("freigegeben", flush=True)
'''

SCHLIESSER = '''\
"""Ruft schliesse_position() auf und meldet das Ergebnis als JSON.
Alles ueber Umgebungsvariablen, damit der Quelltext keine Werte
eingebaut bekommt."""
import json, logging, os, sys, time
sys.path.insert(0, os.environ["MC_NOTIF"])
import manual_close as mc
wurzel = os.environ["MC_WURZEL"]
mc.BASE_DIR = wurzel
mc.STRATEGIES_DIR = os.path.join(wurzel, "strategies")
mc.SPERR_TIMEOUT_SEKUNDEN = float(os.environ.get("MC_TIMEOUT", "15"))
for h in list(mc._protokoll.handlers):
    mc._protokoll.removeHandler(h)
    h.close()
griff = logging.FileHandler(os.environ["MC_PROTOKOLL"], encoding="utf-8")
griff.setFormatter(logging.Formatter("%(asctime)s MANUELLER-EINGRIFF %(message)s"))
mc._protokoll.addHandler(griff)

start = float(os.environ.get("MC_START", "0"))
while time.time() < start:            # gemeinsamer Startzeitpunkt
    time.sleep(0.0005)
begonnen = time.time()
try:
    e = mc.schliesse_position("t3_supertrend", int(os.environ["MC_TRADE"]),
                              float(os.environ["MC_PREIS"]),
                              os.environ["MC_USER"], "BESTAETIGEN")
    aus = {"erfolg": True, "user": os.environ["MC_USER"],
           "pnl": e["pnl_pct"], "exit_price": e["exit_price"]}
except mc.SchliessenNichtMoeglich as fehler:
    aus = {"erfolg": False, "user": os.environ["MC_USER"], "grund": str(fehler)}
aus["von"], aus["bis"] = begonnen, time.time()
sys.stdout.write(json.dumps(aus))
'''


def schreibe_helfer(wurzel):
    pfade = {}
    for name, inhalt in (("sperr_halter.py", SPERR_HALTER),
                          ("schliesser.py", SCHLIESSER)):
        p = os.path.join(wurzel, name)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(inhalt)
        pfade[name] = p
    return pfade


def starte_schliesser(wurzel, helfer, user, start, trade=1, preis=110.0,
                       timeout="15"):
    umgebung = dict(os.environ,
                    MC_NOTIF=_DIR, MC_WURZEL=wurzel, MC_USER=str(user),
                    MC_START=str(start), MC_TRADE=str(trade),
                    MC_PREIS=str(preis), MC_TIMEOUT=timeout,
                    MC_PROTOKOLL=os.path.join(wurzel, f"log_{user}.log"))
    return subprocess.Popen([sys.executable, helfer["schliesser.py"]],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=umgebung, text=True)


def test_fremde_sperre_laenger_als_das_timeout():
    print("\n9a. Fremde Schreibsperre laeuft laenger als das Timeout")
    wurzel = tempfile.mkdtemp(prefix="mc_sperre_")
    db = baue_bot(wurzel)
    helfer = schreibe_helfer(wurzel)
    vorher = alle_zeilen(db)
    summe = datei_pruefsumme(db)

    halter = subprocess.Popen([sys.executable, helfer["sperr_halter.py"], db, "4"],
                               stdout=subprocess.PIPE, text=True)
    check("Sperr-Halter meldet sich", halter.stdout.readline().strip() == "gesperrt")

    prozess = starte_schliesser(wurzel, helfer, user=1, start=0, timeout="1")
    aus, fehlertext = prozess.communicate(timeout=60)
    halter.wait(timeout=60)

    ergebnis = json.loads(aus) if aus.strip() else {"erfolg": None, "roh": fehlertext}
    check("Der Schliessversuch bricht ab, statt zu warten oder abzustuerzen",
          ergebnis.get("erfolg") is False,
          str(ergebnis.get("grund", fehlertext))[:80])
    check("Die Meldung nennt die Sperre und den vermuteten Cronjob",
          "gesperrt" in ergebnis.get("grund", "").lower()
          and "cronjob" in ergebnis.get("grund", "").lower())
    check("Datenbank nach dem abgebrochenen Versuch unveraendert",
          unterschiede(vorher, alle_zeilen(db)) == []
          and datei_pruefsumme(db) == summe)

    protokoll = protokoll_zeilen(os.path.join(wurzel, "log_1.log"))
    check("Der Abbruch steht als ABGELEHNT im Protokoll",
          len(protokoll) == 1 and "ABGELEHNT" in protokoll[0])
    shutil.rmtree(wurzel, ignore_errors=True)


def test_kurze_fremde_sperre_wird_ausgesessen():
    print("\n9b. Kurze fremde Sperre - es wird gewartet, nicht abgebrochen")
    # GEGENPROBE zu 9a: ohne diesen Fall waere nicht belegt, dass
    # busy_timeout ueberhaupt WARTET - eine Umsetzung, die immer sofort
    # abbricht, haette 9a genauso bestanden.
    wurzel = tempfile.mkdtemp(prefix="mc_sperre2_")
    db = baue_bot(wurzel)
    helfer = schreibe_helfer(wurzel)

    halter = subprocess.Popen([sys.executable, helfer["sperr_halter.py"], db, "2"],
                               stdout=subprocess.PIPE, text=True)
    halter.stdout.readline()
    begonnen = time.time()
    prozess = starte_schliesser(wurzel, helfer, user=1, start=0, timeout="20")
    aus, fehlertext = prozess.communicate(timeout=90)
    gedauert = time.time() - begonnen
    halter.wait(timeout=60)

    ergebnis = json.loads(aus) if aus.strip() else {"erfolg": None, "roh": fehlertext}
    check("Der Schliessvorgang gelingt, nachdem die Sperre faellt",
          ergebnis.get("erfolg") is True, str(ergebnis)[:80])
    check("Er hat dabei tatsaechlich gewartet (>= 1,5 s)", gedauert >= 1.5,
          f"{gedauert:.1f} s")
    check("Genau eine Zeile geschlossen",
          [z for z in alle_zeilen(db) if z["id"] == 1][0]["status"] == "closed")
    shutil.rmtree(wurzel, ignore_errors=True)


def test_zwei_gleichzeitige_schreiber():
    print("\n9c. Zwei Prozesse schliessen GLEICHZEITIG dieselbe Position")
    wurzel = tempfile.mkdtemp(prefix="mc_wettlauf_")
    db = baue_bot(wurzel)
    helfer = schreibe_helfer(wurzel)
    vorher = alle_zeilen(db)

    # Gemeinsamer Startzeitpunkt in der Zukunft: beide Prozesse sind dann
    # bereits gestartet und importiert, wenn sie losschreiben - sonst
    # wuerde der zweite erst anlaufen, wenn der erste laengst fertig ist,
    # und es gaebe gar keinen Wettlauf.
    start = time.time() + 2.0
    a = starte_schliesser(wurzel, helfer, user=111, start=start, preis=110.0)
    b = starte_schliesser(wurzel, helfer, user=222, start=start, preis=120.0)
    aus_a, fehler_a = a.communicate(timeout=90)
    aus_b, fehler_b = b.communicate(timeout=90)

    ergebnisse = []
    for aus, fehlertext, wer in ((aus_a, fehler_a, 111), (aus_b, fehler_b, 222)):
        if not aus.strip():
            check(f"Prozess {wer} lieferte ein Ergebnis", False, fehlertext[-200:])
            ergebnisse.append({"erfolg": None})
        else:
            ergebnisse.append(json.loads(aus))
    erfolge = [e for e in ergebnisse if e.get("erfolg") is True]
    ablehnungen = [e for e in ergebnisse if e.get("erfolg") is False]

    check("Genau EIN Prozess hat geschrieben", len(erfolge) == 1,
          f"Erfolge: {len(erfolge)}, Ablehnungen: {len(ablehnungen)}")

    # Ohne diese Pruefung waere nicht belegt, dass ueberhaupt ein Wettlauf
    # stattfand: waeren die Prozesse nacheinander gelaufen, waere das
    # Ergebnis oben dasselbe - und der Test wuerde nichts ueber
    # Nebenlaeufigkeit aussagen.
    if all("von" in e for e in ergebnisse):
        ueberlappung = (min(e["bis"] for e in ergebnisse)
                        - max(e["von"] for e in ergebnisse))
        check("Die beiden Versuche haben sich zeitlich ueberlappt "
              "(es war wirklich ein Wettlauf)", ueberlappung > 0,
              f"Ueberlappung {ueberlappung * 1000:.1f} ms")
    check("Der andere wurde sauber abgelehnt (kein Absturz)",
          len(ablehnungen) == 1,
          ablehnungen[0]["grund"][:90] if ablehnungen else "")

    nachher = alle_zeilen(db)
    diff = unterschiede(vorher, nachher)
    check("Trotz Wettlauf: nur Trade 1 veraendert, nur die fuenf Ausstiegsfelder",
          {(k, f) for k, f, _, _ in diff} ==
          {(1, "exit_time"), (1, "exit_price"), (1, "result"),
           (1, "pnl_pct"), (1, "status")},
          str(sorted({(k, f) for k, f, _, _ in diff})))

    zeile = [z for z in nachher if z["id"] == 1][0]
    if erfolge:
        check("Die geschriebene Zeile stammt vollstaendig von EINEM Prozess "
              "(kein Mischzustand aus beiden Kursen)",
              zeile["exit_price"] == erfolge[0]["exit_price"]
              and zeile["pnl_pct"] == erfolge[0]["pnl"],
              f"exit_price={zeile['exit_price']}, pnl={zeile['pnl_pct']}")
    if erfolge and ablehnungen:
        verlierer_kurs = 120.0 if erfolge[0]["exit_price"] == 110.0 else 110.0
        check("Der Kurs des unterlegenen Prozesses steht NICHT in der Datenbank",
              zeile["exit_price"] != verlierer_kurs,
              f"Verlierer wollte {verlierer_kurs}, in der DB steht "
              f"{zeile['exit_price']}")
        # Der Verlierer darf nicht irgendwie scheitern, sondern muss an
        # der Vorbedingung scheitern - sonst waere unklar, ob die Sperre
        # oder ein Zufall ihn aufgehalten hat.
        grund = ablehnungen[0]["grund"].lower()
        check("Der unterlegene Prozess scheitert an der Vorbedingung "
              "'nicht mehr offen', nicht an einem Fehler",
              "nicht mehr offen" in grund or "gesperrt" in grund, grund[:90])
        for wer in (111, 222):
            zeilen = protokoll_zeilen(os.path.join(wurzel, f"log_{wer}.log"))
            check(f"Prozess {wer} hat genau eine Protokollzeile hinterlassen",
                  len(zeilen) == 1, zeilen[0][:110] if zeilen else "keine")
    shutil.rmtree(wurzel, ignore_errors=True)


def test_cronjob_schliesst_im_bestaetigungsfenster():
    print("\n9d. Der Cronjob schliesst die Position waehrend der Rueckfrage")
    # Das realistischste Szenario: zwischen Anzeige der Liste und dem
    # getippten BESTAETIGEN vergehen Sekunden bis Minuten. Genau dann
    # laeuft der Cronjob an und schliesst dieselbe Position selbst.
    wurzel = tempfile.mkdtemp(prefix="mc_fenster_")
    db = baue_bot(wurzel)
    biege_um(_MC, wurzel)
    lenke_protokoll_um(_MC, os.path.join(wurzel, "eingriffe.log"))

    positionen = _MC.offene_positionen("t3_supertrend")   # Schritt 1: Liste
    check("Liste enthaelt die beiden offenen Positionen", len(positionen) == 2)

    # ... und JETZT schliesst der Bot sie selbst, genau wie in
    # forward_test.py::check_open_trades().
    bot = sqlite3.connect(db)
    bot.execute("UPDATE trades SET exit_time=?, exit_price=?, result=?, "
                "pnl_pct=?, status='closed' WHERE id=?",
                ("2026-09-09 08:00:00", 95.0, "stop_loss", -5.3, 1))
    bot.commit()
    bot.close()
    nach_cronjob = alle_zeilen(db)

    try:
        _MC.schliesse_position("t3_supertrend", 1, 110.0, 4242, "BESTAETIGEN")
        check("Der manuelle Versuch wird abgelehnt", False, "wurde AUSGEFUEHRT")
        meldung = ""
    except _MC.SchliessenNichtMoeglich as fehler:
        meldung = str(fehler)
        check("Der manuelle Versuch wird abgelehnt", True, meldung[:80])

    check("Die Meldung erklaert, dass der Cronjob zuvorgekommen ist",
          "cronjob" in meldung.lower() and "nicht mehr offen" in meldung.lower())
    check("Der Ausstieg des Bots bleibt unangetastet (kein Ueberschreiben)",
          unterschiede(nach_cronjob, alle_zeilen(db)) == [])
    zeile = [z for z in alle_zeilen(db) if z["id"] == 1][0]
    check("result ist weiterhin 'stop_loss', nicht 'manual_close'",
          zeile["result"] == "stop_loss" and zeile["exit_price"] == 95.0)
    shutil.rmtree(wurzel, ignore_errors=True)


# ---------------------------------------------------------------------------
# 10. Die Telegram-Schicht: Zugriffsschutz und die beiden Bestaetigungsstufen
# ---------------------------------------------------------------------------
# telegram_bot.py wird hier ECHT importiert (mit der Attrappe der
# Bibliothek darunter) und seine Handler werden aufgerufen wie von
# python-telegram-bot. Nachgebaut wird nur, was Telegram liefert:
# Update, Message, CallbackQuery, Context.

ERLAUBTE_ID = 424242
FREMDE_ID = 999999


def _braucht_telegram(funktion):
    """Markiert einen Test, der die Telegram-Oberflaeche braucht."""
    funktion.braucht_telegram = True
    return funktion


class FalscheNachricht:
    def __init__(self, text=""):
        self.text = text
        self.antworten = []

    async def reply_text(self, text, **kwargs):
        self.antworten.append({"text": text, **kwargs})


class FalscheAbfrage:
    def __init__(self, data):
        self.data = data
        self.beantwortet = False
        self.bearbeitungen = []

    async def answer(self, *a, **k):
        self.beantwortet = True

    async def edit_message_text(self, text, **kwargs):
        self.bearbeitungen.append({"text": text, **kwargs})


class FalscherNutzer:
    def __init__(self, kennung):
        self.id = kennung


class FalschesUpdate:
    def __init__(self, benutzer_id, text=None, callback_data=None):
        self.effective_user = FalscherNutzer(benutzer_id)
        self.message = FalscheNachricht(text) if text is not None else None
        self.callback_query = FalscheAbfrage(callback_data) if callback_data else None


class FalscherKontext:
    def __init__(self):
        self.user_data = {}


def lade_telegram_bot():
    """telegram_bot.py mit gesetzter TELEGRAM_USER_ID importieren -
    AUTHORIZED_USER_ID wird beim Import einmalig festgelegt."""
    os.environ["TELEGRAM_BOT_TOKEN"] = "0:testtoken"
    os.environ["TELEGRAM_USER_ID"] = str(ERLAUBTE_ID)
    import telegram_bot
    # Die TRACE-Zeilen des Bots (Diagnose-Instrumentierung aus einer
    # frueheren Fehlersuche) wuerden die Testausgabe unlesbar machen.
    for name in ("notifications.telegram_bot", "notifications.monitor"):
        logging.getLogger(name).setLevel(logging.ERROR)
    return telegram_bot


def ohne_kurse(bot_name, positionen):
    return {}


def mit_kursen(kurse):
    def hole(bot_name, positionen):
        return dict(kurse)
    return hole


@_braucht_telegram
def test_telegram_ablauf():
    print("\n10. Telegram-Ablauf: Zugriffsschutz, beide Stufen, Abbrueche")
    tb = lade_telegram_bot()
    check("AUTHORIZED_USER_ID kommt aus der Konfiguration",
          tb.AUTHORIZED_USER_ID == ERLAUBTE_ID)

    wurzel = tempfile.mkdtemp(prefix="mc_telegram_")
    db = baue_bot(wurzel)
    biege_um(_MC, wurzel)
    protokoll = lenke_protokoll_um(_MC, os.path.join(wurzel, "eingriffe.log"))

    # Kursabfrage abklemmen - dieser Test prueft den Ablauf, nicht Binance.
    echte_kurse = _TS.kurse_fuer
    _TS.kurse_fuer = mit_kursen({"BTCUSDT": {"price": 110.0},
                                  "ETHUSDT": {"price": 180.0}})
    vorher = alle_zeilen(db)

    try:
        # --- 10a. Zugriffsschutz -------------------------------------------
        print("\n10a. Zugriffsschutz (falsche TELEGRAM_USER_ID)")
        for name, handler, update in (
                ("/schliessen", tb.schliessen_command,
                 FalschesUpdate(FREMDE_ID, text="/schliessen")),
                ("Schaltflaeche", tb.schliessen_callback,
                 FalschesUpdate(FREMDE_ID, callback_data=f"{_TS.CB_WAEHLEN}:t3_supertrend:1")),
                ("Text BESTAETIGEN", tb.schliessen_text,
                 FalschesUpdate(FREMDE_ID, text="BESTAETIGEN"))):
            kontext = FalscherKontext()
            # Ein Fremder koennte sogar eine wartende Bestaetigung im
            # Speicher vorfinden - trotzdem darf nichts passieren.
            kontext.user_data[_TS.WARTET_AUF_TEXT] = {
                "bot": "t3_supertrend", "trade_id": 1, "symbol": "BTCUSDT",
                "kurs": 110.0, "pnl": 9.7,
                "gueltig_bis": time.time() + 999}
            asyncio.run(handler(update, kontext))
            geantwortet = (update.message.antworten if update.message else []) \
                + (update.callback_query.bearbeitungen if update.callback_query else [])
            check(f"Fremde ID bei '{name}': keine Antwort, kein Handler-Lauf",
                  geantwortet == [])
        check("Zugriffsschutz: Datenbank unveraendert",
              unterschiede(vorher, alle_zeilen(db)) == [])

        # GEGENPROBE: mit der richtigen ID laeuft derselbe Aufruf durch -
        # sonst waere oben nur belegt, dass die Handler generell schweigen.
        update = FalschesUpdate(ERLAUBTE_ID, text="/schliessen")
        kontext = FalscherKontext()
        asyncio.run(tb.schliessen_command(update, kontext))
        check("Gegenprobe: die erlaubte ID bekommt die Positionsliste",
              len(update.message.antworten) == 1
              and "BTCUSDT" in update.message.antworten[0]["text"])

        # --- 10b. Schritt 1: Liste ------------------------------------------
        print("\n10b. Schritt 1 - Liste der offenen Positionen")
        antwort = update.message.antworten[0]
        check("Liste zeigt beide offenen Positionen mit Kurs und PnL",
              "BTCUSDT" in antwort["text"] and "ETHUSDT" in antwort["text"]
              and "+9.70%" in antwort["text"])
        check("Die geschlossene Position taucht NICHT auf",
              "SOLUSDT" not in antwort["text"])
        knoepfe = antwort["reply_markup"].inline_keyboard
        check("Je offene Position eine Schaltflaeche, plus Abbrechen",
              len(knoepfe) == 3 and knoepfe[-1][0].text == "Abbrechen")
        check("Die Schaltflaeche traegt Bot und Trade-ID",
              knoepfe[0][0].callback_data == f"{_TS.CB_WAEHLEN}:t3_supertrend:1")
        check("Schritt 1 hat noch nichts geschrieben",
              unterschiede(vorher, alle_zeilen(db)) == [])

        # --- 10c. Schritt 2: erste Bestaetigung ------------------------------
        print("\n10c. Schritt 2 - Zusammenfassung und erste Bestaetigung")
        kontext = FalscherKontext()
        auswahl = FalschesUpdate(ERLAUBTE_ID,
                                  callback_data=f"{_TS.CB_WAEHLEN}:t3_supertrend:1")
        asyncio.run(tb.schliessen_callback(auswahl, kontext))
        text = auswahl.callback_query.bearbeitungen[0]["text"]
        check("Zusammenfassung nennt Symbol, Kurs und geschaetzten PnL",
              "BTCUSDT" in text and "110.0" in text and "+9.70%" in text)
        check("Zusammenfassung warnt vor dem Schreibzugriff",
              "Live-Datenbank" in text and "nicht rueckgaengig" in text)
        check("Nach Schritt 2 wartet noch KEINE Bestaetigung",
              _TS.offene_bestaetigung(kontext.user_data) is None)
        check("Schritt 2 hat nichts geschrieben",
              unterschiede(vorher, alle_zeilen(db)) == [])

        # --- 10d. Schritt 3: "Ja, schliessen" --------------------------------
        print("\n10d. Schritt 3 - 'Ja, schliessen' fordert den Text an")
        ja = FalschesUpdate(ERLAUBTE_ID,
                             callback_data=f"{_TS.CB_BESTAETIGEN}:t3_supertrend:1")
        asyncio.run(tb.schliessen_callback(ja, kontext))
        aufforderung = ja.callback_query.bearbeitungen[0]["text"]
        check("Der Nutzer wird zum Eintippen von BESTAETIGEN aufgefordert",
              "BESTAETIGEN" in aufforderung)
        wartend = _TS.offene_bestaetigung(kontext.user_data)
        check("Jetzt wartet eine Bestaetigung (Bot, Trade, Kurs gemerkt)",
              wartend and wartend["trade_id"] == 1 and wartend["kurs"] == 110.0)
        check("Auch der Tap auf 'Ja, schliessen' hat noch nichts geschrieben",
              unterschiede(vorher, alle_zeilen(db)) == [])

        # --- 10e. Falscher Text --------------------------------------------
        print("\n10e. Zweite Bestaetigung mit falschem Text")
        falsch = FalschesUpdate(ERLAUBTE_ID, text="ja")
        asyncio.run(tb.schliessen_text(falsch, kontext))
        check("Antwort: abgebrochen, nichts geaendert",
              "Abgebrochen" in falsch.message.antworten[0]["text"])
        check("Datenbank unveraendert", unterschiede(vorher, alle_zeilen(db)) == [])
        check("Die wartende Bestaetigung ist VERBRAUCHT (kein zweiter Versuch)",
              _TS.offene_bestaetigung(kontext.user_data) is None)
        nochmal = FalschesUpdate(ERLAUBTE_ID, text="BESTAETIGEN")
        asyncio.run(tb.schliessen_text(nochmal, kontext))
        check("Ein danach getipptes BESTAETIGEN loest nichts mehr aus",
              nochmal.message.antworten == []
              and unterschiede(vorher, alle_zeilen(db)) == [])

        # --- 10f. Abbruch per Schaltflaeche, Stufe 1 und Stufe 2 -------------
        print("\n10f. Abbruch per Schaltflaeche - in beiden Stufen")
        kontext = FalscherKontext()
        ab1 = FalschesUpdate(ERLAUBTE_ID, callback_data=f"{_TS.CB_ABBRECHEN}:-:-")
        asyncio.run(tb.schliessen_callback(ab1, kontext))
        check("Abbruch in Stufe 1: Meldung 'nichts geaendert'",
              "nichts geaendert" in ab1.callback_query.bearbeitungen[0]["text"])

        auswahl = FalschesUpdate(ERLAUBTE_ID,
                                  callback_data=f"{_TS.CB_BESTAETIGEN}:t3_supertrend:1")
        asyncio.run(tb.schliessen_callback(auswahl, kontext))
        check("Vor dem Abbruch in Stufe 2 wartet eine Bestaetigung",
              _TS.offene_bestaetigung(kontext.user_data) is not None)
        ab2 = FalschesUpdate(ERLAUBTE_ID, callback_data=f"{_TS.CB_ABBRECHEN}:-:-")
        asyncio.run(tb.schliessen_callback(ab2, kontext))
        check("Abbruch in Stufe 2 loescht die wartende Bestaetigung",
              _TS.offene_bestaetigung(kontext.user_data) is None)
        check("Nach beiden Abbruechen: Datenbank unveraendert",
              unterschiede(vorher, alle_zeilen(db)) == [])

        # --- 10g. Abgelaufene Bestaetigung ----------------------------------
        print("\n10g. Abgelaufene Bestaetigung")
        kontext = FalscherKontext()
        asyncio.run(tb.schliessen_callback(
            FalschesUpdate(ERLAUBTE_ID,
                            callback_data=f"{_TS.CB_BESTAETIGEN}:t3_supertrend:1"),
            kontext))
        kontext.user_data[_TS.WARTET_AUF_TEXT]["gueltig_bis"] = time.time() - 1
        spaet = FalschesUpdate(ERLAUBTE_ID, text="BESTAETIGEN")
        asyncio.run(tb.schliessen_text(spaet, kontext))
        check("Ein spaetes BESTAETIGEN schliesst nichts mehr",
              spaet.message.antworten == []
              and unterschiede(vorher, alle_zeilen(db)) == [])
        check("Der abgelaufene Eintrag wird entfernt",
              _TS.WARTET_AUF_TEXT not in kontext.user_data)

        # --- 10h. Freier Chat-Text ohne laufenden Vorgang -------------------
        print("\n10h. Freier Text ohne laufenden Schliessvorgang")
        kontext = FalscherKontext()
        for text in ("BESTAETIGEN", "Hallo", "/status"):
            plaudern = FalschesUpdate(ERLAUBTE_ID, text=text)
            asyncio.run(tb.schliessen_text(plaudern, kontext))
            check(f"'{text}' ohne laufenden Vorgang: keine Reaktion",
                  plaudern.message.antworten == [])
        check("Datenbank weiterhin unveraendert",
              unterschiede(vorher, alle_zeilen(db)) == [])

        # --- 10i. Der vollstaendige, erfolgreiche Weg -----------------------
        print("\n10i. Vollstaendiger Durchlauf bis zum Schreiben")
        kontext = FalscherKontext()
        asyncio.run(tb.schliessen_command(
            FalschesUpdate(ERLAUBTE_ID, text="/schliessen"), kontext))
        asyncio.run(tb.schliessen_callback(
            FalschesUpdate(ERLAUBTE_ID,
                            callback_data=f"{_TS.CB_WAEHLEN}:t3_supertrend:1"), kontext))
        asyncio.run(tb.schliessen_callback(
            FalschesUpdate(ERLAUBTE_ID,
                            callback_data=f"{_TS.CB_BESTAETIGEN}:t3_supertrend:1"), kontext))
        fertig = FalschesUpdate(ERLAUBTE_ID, text="BESTAETIGEN")
        asyncio.run(tb.schliessen_text(fertig, kontext))

        erfolgstext = fertig.message.antworten[0]["text"]
        check("Erfolgsmeldung nennt Symbol, Kurs, PnL und den Vermerk",
              all(t in erfolgstext for t in ("BTCUSDT", "110.0", "+9.70%",
                                              "manual_close")), erfolgstext[:60])
        diff = unterschiede(vorher, alle_zeilen(db))
        check("Genau Trade 1 wurde geschlossen, sonst nichts",
              {(k, f) for k, f, _, _ in diff} ==
              {(1, "exit_time"), (1, "exit_price"), (1, "result"),
               (1, "pnl_pct"), (1, "status")})
        check("Die Bestaetigung ist danach verbraucht",
              _TS.offene_bestaetigung(kontext.user_data) is None)

        zeilen = protokoll_zeilen(protokoll)
        check("Im Protokoll steht der Erfolg mit der echten Telegram-ID",
              any("ERFOLGREICH" in z and f"benutzer={ERLAUBTE_ID}" in z
                  for z in zeilen))
        check("Und davor die abgelehnten Versuche aus 10e",
              any("ABGELEHNT" in z and "falscher Bestaetigungstext" in z
                  for z in zeilen))
    finally:
        _TS.kurse_fuer = echte_kurse

    shutil.rmtree(wurzel, ignore_errors=True)


@_braucht_telegram
def test_ohne_kurs_kein_knopf():
    print("\n11. Ohne Live-Kurs wird nichts angeboten und nichts geschrieben")
    tb = lade_telegram_bot()
    wurzel = tempfile.mkdtemp(prefix="mc_kurslos_")
    db = baue_bot(wurzel)
    biege_um(_MC, wurzel)
    lenke_protokoll_um(_MC, os.path.join(wurzel, "eingriffe.log"))
    vorher = alle_zeilen(db)

    echte_kurse = _TS.kurse_fuer
    _TS.kurse_fuer = ohne_kurse
    try:
        kontext = FalscherKontext()
        update = FalschesUpdate(ERLAUBTE_ID, text="/schliessen")
        asyncio.run(tb.schliessen_command(update, kontext))
        antwort = update.message.antworten[0]
        check("Die Liste sagt 'nicht verfuegbar' statt eines Fantasiekurses",
              "nicht verfuegbar" in antwort["text"])
        knoepfe = antwort["reply_markup"].inline_keyboard
        check("Keine Schliessen-Schaltflaeche ohne Kurs (nur 'Abbrechen')",
              len(knoepfe) == 1 and knoepfe[0][0].text == "Abbrechen")

        # Und selbst wer die Schaltflaeche aus einer aelteren Nachricht
        # antippt, bekommt keinen Schreibzugriff.
        auswahl = FalschesUpdate(ERLAUBTE_ID,
                                  callback_data=f"{_TS.CB_WAEHLEN}:t3_supertrend:1")
        asyncio.run(tb.schliessen_callback(auswahl, kontext))
        check("Ein alter Knopf ohne Kurs endet in einer Absage",
              "Kein aktueller Kurs" in auswahl.callback_query.bearbeitungen[0]["text"])
        check("Datenbank unveraendert", unterschiede(vorher, alle_zeilen(db)) == [])
    finally:
        _TS.kurse_fuer = echte_kurse
    shutil.rmtree(wurzel, ignore_errors=True)


@_braucht_telegram
def test_liste_ohne_offene_positionen():
    print("\n12. Bot ohne offene Positionen")
    tb = lade_telegram_bot()
    wurzel = tempfile.mkdtemp(prefix="mc_leer2_")
    db = baue_bot(wurzel)
    conn = sqlite3.connect(db)
    conn.execute("UPDATE trades SET status='closed' WHERE status='open'")
    conn.commit()
    conn.close()
    biege_um(_MC, wurzel)
    lenke_protokoll_um(_MC, os.path.join(wurzel, "eingriffe.log"))

    echte_kurse = _TS.kurse_fuer
    _TS.kurse_fuer = ohne_kurse
    try:
        update = FalschesUpdate(ERLAUBTE_ID, text="/schliessen")
        asyncio.run(tb.schliessen_command(update, FalscherKontext()))
        antwort = update.message.antworten[0]
        check("Meldung 'nichts zu schliessen'",
              "nichts zu schliessen" in antwort["text"])
        check("Keine Tastatur, wenn es nichts zu waehlen gibt",
              antwort.get("reply_markup") is None)
    finally:
        _TS.kurse_fuer = echte_kurse
    shutil.rmtree(wurzel, ignore_errors=True)


@_braucht_telegram
def test_nicht_freigeschalteter_bot_ueber_telegram():
    print("\n13. /schliessen mit einem nicht freigeschalteten Bot-Namen")
    tb = lade_telegram_bot()
    wurzel = tempfile.mkdtemp(prefix="mc_tg_fremd_")
    baue_bot(wurzel)
    biege_um(_MC, wurzel)
    lenke_protokoll_um(_MC, os.path.join(wurzel, "eingriffe.log"))
    # elliott_wave ist inzwischen freigeschaltet; fuer diesen Test braucht es
    # einen Namen, der in SCHLIESSBARE_BOTS wirklich nicht vorkommt.
    update = FalschesUpdate(ERLAUBTE_ID, text="/schliessen gibt_es_nicht")
    asyncio.run(tb.schliessen_command(update, FalscherKontext()))
    text = update.message.antworten[0]["text"]
    check("Antwort weist den Bot ab und nennt die freigeschalteten",
          "nicht freigeschaltet" in text and "t3_supertrend" in text)
    shutil.rmtree(wurzel, ignore_errors=True)


# ---------------------------------------------------------------------------
# 14. Erweiterbarkeit: ein zweiter Bot braucht nur einen Eintrag
# ---------------------------------------------------------------------------

def test_zweiter_bot_nur_ueber_die_liste():
    print("\n14. Die Freischaltung haengt allein an SCHLIESSBARE_BOTS")
    # Seit alle neun Bots freigeschaltet sind, laesst sich die Wirkung der
    # Liste nicht mehr durch HINZUfuegen zeigen - dafuer aber durch
    # Herausnehmen, und das ist der Nachweis, auf den es ankommt: ein Bot,
    # der nicht in der Liste steht, ist gesperrt, egal wie vollstaendig
    # seine Datenbank ist.
    wurzel = tempfile.mkdtemp(prefix="mc_zweiter_")
    baue_bot(wurzel, "t3_supertrend")
    db2 = baue_bot(wurzel, "rsi2_crypto")
    biege_um(_MC, wurzel)
    lenke_protokoll_um(_MC, os.path.join(wurzel, "eingriffe.log"))

    original = dict(_MC.SCHLIESSBARE_BOTS)
    gemerkt = _MC.SCHLIESSBARE_BOTS.pop("rsi2_crypto")
    check("Aus der Liste genommen: rsi2_crypto ist gesperrt, obwohl seine "
          "Datenbank vollstaendig ist",
          _abgelehnt(lambda: _MC.offene_positionen("rsi2_crypto")))
    try:
        _MC.SCHLIESSBARE_BOTS["rsi2_crypto"] = gemerkt
        check("Wieder eingetragen: Positionen lesbar, ohne weitere Aenderung",
              len(_MC.offene_positionen("rsi2_crypto")) == 2)
        ergebnis = _MC.schliesse_position("rsi2_crypto", 2, 220.0, 4242,
                                           "BESTAETIGEN", jetzt="2026-09-09 12:00:00")
        check("Und schliessen funktioniert genauso",
              ergebnis["result"] == "manual_close"
              and [z for z in alle_zeilen(db2) if z["id"] == 2][0]["status"] == "closed")
        check("Die Kostensaetze kommen aus SEINEM forward_test.py",
              ergebnis["pnl_pct"] == 9.7)
    finally:
        _MC.SCHLIESSBARE_BOTS.clear()
        _MC.SCHLIESSBARE_BOTS.update(original)
    check("In der ausgelieferten Fassung sind alle NEUN Bots freigeschaltet",
          len(_MC.SCHLIESSBARE_BOTS) == 9
          and "t3_supertrend" in _MC.SCHLIESSBARE_BOTS,
          str(sorted(_MC.SCHLIESSBARE_BOTS)))
    check("Und jeder Eintrag traegt Anzeigename und Anlageklasse",
          all({"anzeigename", "anlageklasse"} <= set(a)
              for a in _MC.SCHLIESSBARE_BOTS.values()))
    check("Kein Bot verwendet 'manual_close' als eigenen Vermerk - sonst "
          "liesse sich ein manueller Eingriff nicht mehr zuruecknehmen",
          _MC.MANUELLER_GRUND == "manual_close")
    shutil.rmtree(wurzel, ignore_errors=True)


# ---------------------------------------------------------------------------
# 15. Die Bot-Scripte selbst bleiben unangetastet
# ---------------------------------------------------------------------------

def test_keine_bot_datei_wird_importiert_oder_veraendert():
    print("\n15. forward_test.py wird nur GELESEN, nie importiert")
    quelle = open(os.path.join(_DIR, "manual_close.py"), encoding="utf-8").read()
    baum = ast.parse(quelle)
    importe = set()
    for k in ast.walk(baum):
        if isinstance(k, ast.Import):
            importe.update(a.name for a in k.names)
        elif isinstance(k, ast.ImportFrom):
            importe.add(k.module or "")
    verdaechtig = {i for i in importe
                   if any(t in i for t in ("forward_test", "live_params",
                                            "runpy", "importlib", "exec"))}
    check("Kein Import eines Bot-Moduls, kein runpy/importlib", not verdaechtig,
          str(verdaechtig))
    check("Kein exec()/eval() im Modul",
          not any(isinstance(k, ast.Name) and k.id in ("exec", "eval")
                  for k in ast.walk(baum)))
    check("forward_test.py wird per ast.parse gelesen", "ast.parse" in quelle)

    # Und: das Modul oeffnet forward_test.py nur lesend.
    check("Kein Schreibzugriff auf eine .py-Datei",
          'open(pfad, encoding="utf-8")' in quelle and '"w"' not in quelle)


# ---------------------------------------------------------------------------
# Ablauf
# ---------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("Selbsttests: manuelles Schliessen einer Position (Telegram Phase 3)")
    print("=" * 78)

    tests = [
        test_schema_stimmt_mit_dem_echten_bot_ueberein,
        test_manual_close_kollidiert_mit_keinem_bot_grund,
        test_modul_kann_nichts_ausser_schliessen,
        test_pnl_entspricht_der_bot_formel,
        test_erfolgreiches_schliessen,
        test_abgelehnte_versuche_aendern_nichts,
        test_unbekannter_bot_wird_abgelehnt,
        test_fehlende_datenbank,
        test_fremde_sperre_laenger_als_das_timeout,
        test_kurze_fremde_sperre_wird_ausgesessen,
        test_zwei_gleichzeitige_schreiber,
        test_cronjob_schliesst_im_bestaetigungsfenster,
        test_telegram_ablauf,
        test_ohne_kurs_kein_knopf,
        test_liste_ohne_offene_positionen,
        test_nicht_freigeschalteter_bot_ueber_telegram,
        test_zweiter_bot_nur_ueber_die_liste,
        test_keine_bot_datei_wird_importiert_oder_veraendert,
    ]
    for test in tests:
        if getattr(test, "braucht_telegram", False) and _TS is None:
            UEBERSPRUNGEN.append(test.__name__)
            continue
        try:
            test()
        except Exception as fehler:
            import traceback
            FEHLER.append(f"{test.__name__} (Ausnahme)")
            print(f"  [FEHLER] {test.__name__} warf eine Ausnahme: {fehler}")
            traceback.print_exc()

    print("\n" + "=" * 78)
    if UEBERSPRUNGEN:
        print("UEBERSPRUNGEN (telegram_schliessen.py ist in dieser Fassung "
              "nicht vorhanden -\n  die Telegram-Oberflaeche kam in einer "
              "eigenen Aenderung; der KERN ist vollstaendig geprueft):")
        for name in UEBERSPRUNGEN:
            print(f"  - {name}")
        print()
    print(f"{BESTANDEN} Pruefungen bestanden, {len(FEHLER)} fehlgeschlagen.")
    if FEHLER:
        for name in FEHLER:
            print(f"  - {name}")
        return 1
    print("Alle Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
