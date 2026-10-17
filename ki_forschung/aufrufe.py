"""Aufrufbuch und Kostenbremse der KI-Forschung (TB-177, BA1).

Jeder Modellaufruf geht ueber aufrufen(). Vor dem Aufruf rechnet die Bremse
die Monatssumme des Deckel-Topfs (UTC-Monat) plus den hoechstmoeglichen
Preis dieses Aufrufs; wuerde das den Deckel ueberschreiten, wird NICHT
aufgerufen (Zeile 'gebremst'). Sonst wird der Hoechstpreis als Zeile
'reserviert' gebucht, dann aufgerufen, dann eine Zeile 'abgerechnet' mit dem
echten Preis aus usage; sie ersetzt in der Monatssumme die Reservierung.
max_tokens muss eine ganze Zahl >= 1 sein, alle Betraege sind >= 0 (Pruefung
im Code und CHECK in der Tabelle). Stuerzt der Lauf dazwischen ab, bleibt
die Reservierung stehen: die Bremse rechnet zu viel, nie zu wenig.
Pruefung und Reservierung laufen in einer Transaktion (BEGIN IMMEDIATE).
Die Tabelle ist nur anfuegend: UPDATE, DELETE und ein INSERT mit schon
vorhandener id (INSERT OR REPLACE) bricht ein Trigger ab; dazu
recursive_triggers je Verbindung. Die Buchungszeit (und damit der Monat)
wird nur intern gesetzt, kein Parameter des Aufrufers.

Zwei Toepfe, getrennt gebucht (Betreiberentscheid 17.10.2026): 'sammler'
und 'bots' (die KI-Bots), je 3 $ im Monat. Nur Haiku, keine Werkzeuge (keine
Websuche). shared/claude_client.py wird nur importiert, nicht geaendert;
Schluessel ANTHROPIC_API_KEY liest claude_client selbst (Umgebung oder
config/email_config.py), dieses Modul liest keinen Schluessel.
Notschalter: steht 'ki_<topf>' in config/agenten_aus.txt, wird nicht
aufgerufen (Zeile 'abgeschaltet').
"""
import datetime
import hashlib
import os
import sqlite3
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)
import pfade  # noqa: E402
if pfade.SHARED_DIR not in sys.path:
    sys.path.append(pfade.SHARED_DIR)  # nur fuer den Import von claude_client

DECKEL_USD = {"sammler": 3.0, "bots": 3.0}
# Preis je Million Token (USD) fuer das eine erlaubte Modell. Aus der
# Preisliste des Anbieters, nicht im Repo gemessen; der Betreiber bestaetigt
# ihn vor dem Erstlauf (BA7). Steht hier ein Modell nicht, wird nicht aufgerufen.
PREIS_JE_MTOK = {"claude-haiku-4-5-20251001": {"ein": 1.0, "aus": 5.0}}

SCHEMA = """
CREATE TABLE IF NOT EXISTS aufrufe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zeit_utc TEXT NOT NULL,
    monat TEXT NOT NULL,
    topf TEXT NOT NULL,
    verbraucher TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('reserviert', 'abgerechnet', 'gebremst', 'abgeschaltet', 'abgelehnt')),
    bezug INTEGER,
    modell_angefordert TEXT NOT NULL,
    modell_geliefert TEXT,
    prompt_hash TEXT NOT NULL,
    eingabe_hash TEXT,
    katalogversion TEXT,
    max_tokens INTEGER NOT NULL CHECK (typeof(max_tokens) = 'integer' AND max_tokens >= 1),
    tokens_ein INTEGER CHECK (tokens_ein IS NULL OR tokens_ein >= 0),
    tokens_aus INTEGER CHECK (tokens_aus IS NULL OR tokens_aus >= 0),
    kosten_usd REAL NOT NULL CHECK (kosten_usd >= 0),
    summe_vorher_usd REAL,
    deckel_usd REAL,
    erfolg INTEGER,
    fehler TEXT
);
CREATE INDEX IF NOT EXISTS aufrufe_monat ON aufrufe (topf, monat);
CREATE TRIGGER IF NOT EXISTS aufrufe_kein_update BEFORE UPDATE ON aufrufe
BEGIN SELECT RAISE(ABORT, 'aufrufe.db ist nur anfuegend'); END;
CREATE TRIGGER IF NOT EXISTS aufrufe_kein_delete BEFORE DELETE ON aufrufe
BEGIN SELECT RAISE(ABORT, 'aufrufe.db ist nur anfuegend'); END;
CREATE TRIGGER IF NOT EXISTS aufrufe_kein_ersetzen BEFORE INSERT ON aufrufe
WHEN NEW.id IS NOT NULL AND EXISTS (SELECT 1 FROM aufrufe WHERE id = NEW.id)
BEGIN SELECT RAISE(ABORT, 'aufrufe.db ist nur anfuegend (id schon vorhanden)'); END;
"""


def _jetzt():
    return datetime.datetime.now(datetime.timezone.utc)


def verbinden(db=None):
    conn = sqlite3.connect(db or pfade.AUFRUFE_DB, isolation_level=None, timeout=30)
    conn.execute("PRAGMA recursive_triggers = ON")
    conn.executescript(SCHEMA)
    return conn


def prompt_hash(system_prompt, user_message):
    return hashlib.sha256(("%s\x00%s" % (system_prompt, user_message)).encode("utf-8")).hexdigest()


# Zuschlag fuer den Formatierungs-Overhead der API (Rollen, Nachrichtenrahmen,
# Systemteil), der nicht in den Bytes von Prompt und Nachricht steckt.
# Gewaehlt, nicht gemessen (Gegenleser GEGEN177 F1); BA7 misst ihn am Erstlauf
# (usage.input_tokens gegen Bytes) und bestaetigt ihn.
FORMAT_ZUSCHLAG_TOKEN = 500


def _ganz(wert):
    """True fuer eine ganze Zahl (int, nicht bool)."""
    return isinstance(wert, int) and not isinstance(wert, bool)


def eingabe_pruefen(system_prompt, user_message, max_tokens):
    """Vor jeder Buchung: Texte sind str, max_tokens ganze Zahl >= 1. Sonst ValueError."""
    if not isinstance(system_prompt, str) or not isinstance(user_message, str):
        raise ValueError("system_prompt und user_message muessen Text (str) sein")
    if not _ganz(max_tokens) or max_tokens < 1:
        raise ValueError("max_tokens muss eine ganze Zahl >= 1 sein, nicht %r" % (max_tokens,))


def hoechstpreis(modell, system_prompt, user_message, max_tokens):
    """Obergrenze des Preises vor dem Aufruf: Eingabe-Token hoechstens so viele
    wie Bytes (jedes Token deckt mindestens ein Byte) plus FORMAT_ZUSCHLAG_TOKEN
    fuer den Formatierungs-Overhead, Ausgabe hoechstens max_tokens. Nie negativ."""
    eingabe_pruefen(system_prompt, user_message, max_tokens)
    p = PREIS_JE_MTOK[modell]
    ein = len(system_prompt.encode("utf-8")) + len(user_message.encode("utf-8")) + FORMAT_ZUSCHLAG_TOKEN
    reserve = (ein * p["ein"] + max_tokens * p["aus"]) / 1e6
    if not (0 <= reserve < float("inf")):
        raise ValueError("Reserve %r nicht im Bereich [0, inf)" % (reserve,))
    return reserve


def preis(modell, tokens_ein, tokens_aus):
    """Echter Preis aus usage; Token muessen ganze Zahlen >= 0 sein, sonst ValueError."""
    if not (_ganz(tokens_ein) and _ganz(tokens_aus) and tokens_ein >= 0 and tokens_aus >= 0):
        raise ValueError("Token muessen ganze Zahlen >= 0 sein: %r, %r" % (tokens_ein, tokens_aus))
    p = PREIS_JE_MTOK[modell]
    return (tokens_ein * p["ein"] + tokens_aus * p["aus"]) / 1e6


def monatssumme(topf, monat, db=None, conn=None):
    eigene = conn is None
    conn = conn or verbinden(db)
    try:
        # Je Aufruf zaehlt die Abrechnung (echter Preis), solange keine da ist die
        # Reservierung (Hoechstpreis). Alle Betraege >= 0 (CHECK).
        s = conn.execute("SELECT COALESCE(SUM(kosten_usd), 0) FROM aufrufe a WHERE topf = ? AND monat = ?"
                         " AND (status = 'abgerechnet' OR (status = 'reserviert' AND NOT EXISTS"
                         " (SELECT 1 FROM aufrufe b WHERE b.status = 'abgerechnet' AND b.bezug = a.id)))",
                         (topf, monat)).fetchone()[0]
        return float(s)
    finally:
        if eigene:
            conn.close()


def _zeile(conn, **w):
    spalten = sorted(w)
    cur = conn.execute("INSERT INTO aufrufe (%s) VALUES (%s)" % (", ".join(spalten), ", ".join("?" * len(spalten))),
                       [w[k] for k in spalten])
    return cur.lastrowid


def aufrufen(topf, verbraucher, system_prompt, user_message, max_tokens=600, eingabe_hash=None,
             katalogversion=None, db=None, aufruf=None, schalter=None):
    """Ein Modellaufruf unter der Bremse. aufruf: Attrappe fuer Tests
    (Signatur wie claude_client.call_claude); ohne sie der echte Aufruf.
    Gibt {'success', 'text', 'gebremst', 'id', ...} zurueck. Gebremst,
    abgeschaltet und ein fehlgeschlagener Modellaufruf werfen nicht.
    Es wirft: ValueError bei unbekanntem Topf (nichts gebucht); ein
    Datenbankfehler vor der Reservierung (z. B. Zeitueberschreitung bei
    BEGIN IMMEDIATE; nichts gebucht, kein Aufruf); ein Datenbankfehler beim
    Buchen der Abrechnung nach dem Aufruf - dann bleibt die Reservierung
    (Hoechstpreis) stehen: zu viel gebucht, nie zu wenig."""
    import claude_client  # shared/, nur importiert
    if topf not in DECKEL_USD:
        raise ValueError("unbekannter Topf %r" % topf)
    eingabe_pruefen(system_prompt, user_message, max_tokens)
    modell = claude_client.MODEL_HAIKU
    zeit = _jetzt()
    zeit_s, monat = zeit.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), zeit.strftime("%Y-%m")
    ph = prompt_hash(system_prompt, user_message)
    basis = dict(zeit_utc=zeit_s, monat=monat, topf=topf, verbraucher=verbraucher, modell_angefordert=modell,
                 prompt_hash=ph, eingabe_hash=eingabe_hash, katalogversion=katalogversion, max_tokens=int(max_tokens),
                 deckel_usd=DECKEL_USD[topf])
    conn = verbinden(db)
    try:
        if modell not in PREIS_JE_MTOK:
            _zeile(conn, status="abgelehnt", kosten_usd=0.0, fehler="kein Preis fuer %s" % modell, **basis)
            return {"success": False, "gebremst": True, "error": "kein Preis fuer Modell %s" % modell}
        if claude_client.agent_abgeschaltet("ki_" + topf, schalter):
            _zeile(conn, status="abgeschaltet", kosten_usd=0.0, **basis)
            return {"success": False, "gebremst": True, "error": "ki_%s abgeschaltet" % topf}
        reserve = hoechstpreis(modell, system_prompt, user_message, max_tokens)
        conn.execute("BEGIN IMMEDIATE")
        try:
            summe = monatssumme(topf, monat, conn=conn)
            if summe + reserve > DECKEL_USD[topf]:
                rid = _zeile(conn, status="gebremst", kosten_usd=0.0, summe_vorher_usd=summe,
                             fehler="Deckel: %.6f + %.6f > %.2f" % (summe, reserve, DECKEL_USD[topf]), **basis)
                conn.execute("COMMIT")
                return {"success": False, "gebremst": True, "id": rid,
                        "error": "Monatsdeckel %s erreicht (%.4f + %.4f > %.2f $)" % (topf, summe, reserve, DECKEL_USD[topf])}
            rid = _zeile(conn, status="reserviert", kosten_usd=reserve, summe_vorher_usd=summe, **basis)
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
        erg = (aufruf or claude_client.call_claude)(system_prompt, user_message, max_tokens=int(max_tokens),
                                                      tools=None, model=modell)
        raw = erg.get("raw")
        usage = getattr(raw, "usage", None)
        t_ein = getattr(usage, "input_tokens", None)
        t_aus = getattr(usage, "output_tokens", None)
        geliefert = getattr(raw, "model", None)
        try:
            kosten = preis(modell, t_ein, t_aus) if erg.get("success") else reserve
        except ValueError:
            kosten = reserve  # usage fehlt oder unbrauchbar: Hoechstpreis (zu viel, nie zu wenig)
        _zeile(conn, status="abgerechnet", bezug=rid, kosten_usd=kosten, modell_geliefert=geliefert,
               tokens_ein=t_ein, tokens_aus=t_aus, erfolg=1 if erg.get("success") else 0,
               fehler=None if erg.get("success") else str(erg.get("error"))[:500],
               **dict(basis, zeit_utc=_jetzt().strftime("%Y-%m-%dT%H:%M:%S.%fZ")))
        return {"success": bool(erg.get("success")), "gebremst": False, "id": rid, "text": erg.get("text", ""),
                "error": erg.get("error"), "modell_geliefert": geliefert, "tokens_ein": t_ein, "tokens_aus": t_aus}
    finally:
        conn.close()
