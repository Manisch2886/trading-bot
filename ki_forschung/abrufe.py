"""Abruf- und Einfrierschicht der KI-Forschung (TB-177, BA1).

Jeder Abruf wird als Rohkopie mit sha256 und Abrufzeit (UTC) in abrufe.db
eingefroren. Die Abrufzeit ist der Vintage-Stempel und wird nur hier intern
gesetzt (kein Parameter des Aufrufers, keine Rueckdatierung); Format fest
JJJJ-MM-TTThh:mm:ss.ffffffZ (CHECK in der Tabelle). Ein spaeterer Prompt
liest nur, was zu seiner Zeit schon eingefroren war (stand()).
Die Tabelle ist nur anfuegend: UPDATE, DELETE und ein INSERT mit schon
vorhandener id (INSERT OR REPLACE, REPLACE) bricht SQLite per Trigger ab;
dazu recursive_triggers je Verbindung. Ein fehlgeschlagener Abruf wird als
Zeile 'ausgefallen' gebucht, nicht nachgeholt. Keine Websuche, kein
Modellaufruf hier.
"""
import datetime
import hashlib
import os
import re
import sqlite3
import sys
import urllib.request

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)
import pfade  # noqa: E402

QUELLEN = ("alfred", "fear_greed", "yfinance", "binance_spot", "rss")
ZEITFORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

SCHEMA = """
CREATE TABLE IF NOT EXISTS abrufe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quelle TEXT NOT NULL,
    schluessel TEXT NOT NULL,
    abgerufen_utc TEXT NOT NULL CHECK (abgerufen_utc GLOB
        '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]Z'),
    url TEXT,
    format TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('ok', 'ausgefallen')),
    bytes INTEGER NOT NULL,
    sha256 TEXT NOT NULL,
    roh BLOB NOT NULL,
    fehler TEXT
);
CREATE INDEX IF NOT EXISTS abrufe_stand ON abrufe (quelle, schluessel, abgerufen_utc);
CREATE TRIGGER IF NOT EXISTS abrufe_kein_update BEFORE UPDATE ON abrufe
BEGIN SELECT RAISE(ABORT, 'abrufe.db ist nur anfuegend'); END;
CREATE TRIGGER IF NOT EXISTS abrufe_kein_delete BEFORE DELETE ON abrufe
BEGIN SELECT RAISE(ABORT, 'abrufe.db ist nur anfuegend'); END;
CREATE TRIGGER IF NOT EXISTS abrufe_kein_ersetzen BEFORE INSERT ON abrufe
WHEN NEW.id IS NOT NULL AND EXISTS (SELECT 1 FROM abrufe WHERE id = NEW.id)
BEGIN SELECT RAISE(ABORT, 'abrufe.db ist nur anfuegend (id schon vorhanden)'); END;
"""

_ZEIT_RX = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(?:[.,](\d{1,6}))?(Z|[+-]\d{2}:\d{2})$")


class EinfrierFehler(Exception):
    """Eine eingefrorene Rohkopie passt nicht mehr zu ihrem sha256."""


def jetzt_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime(ZEITFORMAT)


def zeitpunkt(wert):
    """Ein Zeitpunkt mit Zeitzone (datetime oder ISO-Text mit 'Z' oder '+hh:mm',
    Bruchteile bis 6 Stellen, Punkt oder Komma) als UTC-Text im festen Format
    der Tabelle. Ohne Zeitzone: ValueError. Im festen Format (gleiche Breite,
    UTC) ist der Textvergleich in SQLite ein Zeitvergleich."""
    if isinstance(wert, datetime.datetime):
        d = wert
    else:
        m = _ZEIT_RX.match(str(wert).strip())
        if not m:
            raise ValueError("kein Zeitpunkt mit Zeitzone: %r" % (wert,))
        j, mo, t, h, mi, s, bruch, zone = m.groups()
        if zone == "Z":
            tz = datetime.timezone.utc
        else:
            vz = 1 if zone[0] == "+" else -1
            tz = datetime.timezone(vz * datetime.timedelta(hours=int(zone[1:3]), minutes=int(zone[4:6])))
        d = datetime.datetime(int(j), int(mo), int(t), int(h), int(mi), int(s), int((bruch or "0").ljust(6, "0")), tzinfo=tz)
    if d.tzinfo is None or d.utcoffset() is None:
        raise ValueError("Zeitpunkt ohne Zeitzone: %r" % (wert,))
    return d.astimezone(datetime.timezone.utc).strftime(ZEITFORMAT)


def verbinden(db=None):
    conn = sqlite3.connect(db or pfade.ABRUFE_DB)
    conn.execute("PRAGMA recursive_triggers = ON")
    conn.executescript(SCHEMA)
    return conn


def _quelle_pruefen(quelle):
    if quelle not in QUELLEN:
        raise ValueError("unbekannte Quelle %r (erlaubt: %s)" % (quelle, ", ".join(QUELLEN)))


def _einfrieren(quelle, schluessel, roh, format, url, zeit, db):
    _quelle_pruefen(quelle)
    if not isinstance(roh, bytes):
        raise TypeError("roh muss bytes sein")
    sha = hashlib.sha256(roh).hexdigest()
    conn = verbinden(db)
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO abrufe (quelle, schluessel, abgerufen_utc, url, format, status, bytes, sha256, roh)"
                " VALUES (?, ?, ?, ?, ?, 'ok', ?, ?, ?)",
                (quelle, schluessel, zeit, url, format, len(roh), sha, sqlite3.Binary(roh)))
        return {"id": cur.lastrowid, "sha256": sha, "abgerufen_utc": zeit, "status": "ok"}
    finally:
        conn.close()


def _ausfall(quelle, schluessel, fehler, format, url, zeit, db):
    _quelle_pruefen(quelle)
    conn = verbinden(db)
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO abrufe (quelle, schluessel, abgerufen_utc, url, format, status, bytes, sha256, roh, fehler)"
                " VALUES (?, ?, ?, ?, ?, 'ausgefallen', 0, ?, ?, ?)",
                (quelle, schluessel, zeit, url, format, hashlib.sha256(b"").hexdigest(),
                 sqlite3.Binary(b""), str(fehler)[:500]))
        return {"id": cur.lastrowid, "abgerufen_utc": zeit, "status": "ausgefallen"}
    finally:
        conn.close()


def einfrieren(quelle, schluessel, roh, format, url=None, db=None):
    """Friert eine Rohkopie ein (Abrufzeit = jetzt, intern) und gibt id, sha256 und Abrufzeit zurueck."""
    return _einfrieren(quelle, schluessel, roh, format, url, jetzt_utc(), db)


def ausfall(quelle, schluessel, fehler, format, url=None, db=None):
    """Bucht einen fehlgeschlagenen Abruf (Ausfalltag, Zeit = jetzt); er wird nicht nachgeholt."""
    return _ausfall(quelle, schluessel, fehler, format, url, jetzt_utc(), db)


def _http_holen(url):
    anfrage = urllib.request.Request(url, headers={"User-Agent": "trading-bot-ki-forschung/1"})
    with urllib.request.urlopen(anfrage, timeout=30) as antwort:
        return antwort.read()


def abrufen(quelle, schluessel, url, format, holer=None, db=None):
    """Holt url (oder ruft die Attrappe holer(url) auf) und friert das Ergebnis ein.
    Abrufzeit = Beginn des Abrufs (intern). Ein Fehler wird als Ausfall gebucht, nicht geworfen."""
    _quelle_pruefen(quelle)
    zeit = jetzt_utc()
    try:
        roh = (holer or _http_holen)(url)
    except Exception as e:  # Ausfall statt Absturz
        return _ausfall(quelle, schluessel, e, format, url, zeit, db)
    return _einfrieren(quelle, schluessel, roh, format, url, zeit, db)


def stand(quelle, schluessel, bis, db=None):
    """Die juengste gueltige Rohkopie mit abgerufen_utc <= bis (Vintage), sha256
    nachgerechnet. bis ist ein Zeitpunkt mit Zeitzone (siehe zeitpunkt()).
    None, wenn es keine gibt."""
    grenze = zeitpunkt(bis)
    conn = verbinden(db)
    try:
        z = conn.execute(
            "SELECT id, abgerufen_utc, format, sha256, roh FROM abrufe WHERE quelle = ? AND schluessel = ?"
            " AND status = 'ok' AND abgerufen_utc <= ? ORDER BY abgerufen_utc DESC, id DESC LIMIT 1",
            (quelle, schluessel, grenze)).fetchone()
    finally:
        conn.close()
    if z is None:
        return None
    roh = bytes(z[4])
    if hashlib.sha256(roh).hexdigest() != z[3]:
        raise EinfrierFehler("Abruf %d: sha256 passt nicht zur Rohkopie" % z[0])
    return {"id": z[0], "abgerufen_utc": z[1], "format": z[2], "sha256": z[3], "roh": roh}
