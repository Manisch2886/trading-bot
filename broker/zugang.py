"""
Zugangsdaten und Sicherheitsgrenzen der Testnet-Bruecke
==============================================================================
Diese Datei enthaelt KEINE Schluessel, sondern liest sie - bevorzugt aus
echten Umgebungsvariablen, sonst aus der .env im Projekt-Root. Gleiche
Grundregel wie bei notifications/telegram_config.py und config/email_config.py:
niemals im Code eintragen, niemals in Logs ausgeben, niemals committen
(.env steht in .gitignore).

.env-Format (je eine Zeile, Anfuehrungszeichen nicht noetig):

    BINANCE_TESTNET_API_KEY=...
    BINANCE_TESTNET_API_SECRET=...
    BINANCE_TESTNET_BETRAG_USDT=100        # optional, Standard 100

------------------------------------------------------------------------------
WARUM EIGENE VARIABLENNAMEN
------------------------------------------------------------------------------
Die bestehenden Schluessel fuer den Kursdatenabruf (shared/fetch_binance_data.py,
Variablen BINANCE_API_KEY / BINANCE_API_SECRET) gehoeren zu einem ECHTEN
Binance-Konto und werden hier nie gelesen. Mehr noch: `get_zugang()` bricht ab,
wenn der Testnet-Schluessel mit einem davon uebereinstimmt - dann liegt
eindeutig eine Verwechslung vor, und ein Handelsversuch mit einem echten
Schluessel ist genau das, was dieses Projekt nicht tun darf. Geprueft wird
ueber einen Vergleich in konstanter Zeit, damit die Pruefung selbst nichts
ueber die Schluessel verraet.

------------------------------------------------------------------------------
DIE ENDPUNKT-KONSTANTEN STEHEN HIER - UND ZWAR ALS LITERAL
------------------------------------------------------------------------------
`TESTNET_BASIS` und `TESTNET_HOST` sind feste Zeichenketten. Es gibt
ABSICHTLICH keinen Weg, sie ueber eine Umgebungsvariable zu setzen: eine
falsch gesetzte Variable waere der wahrscheinlichste Weg, versehentlich gegen
den echten Handelsendpunkt zu laufen. Wer den Endpunkt aendern will, aendert
Code - und das faellt in einem Diff auf. binance_testnet.py prueft zusaetzlich
bei JEDEM Aufruf den tatsaechlichen Host der Ziel-URL (nicht bloss deren
Anfang, siehe dortige Begruendung).

------------------------------------------------------------------------------
NOTBREMSE UND MENGENGRENZEN
------------------------------------------------------------------------------
Das Uebergabeprotokoll (Abschnitt 8) haelt fest, welche Voraussetzungen fuer
echten Handel vereinbart waren: Schluessel ohne Auszahlungsrecht,
Notausschalter, Tagesverlust-Limit, Monitoring, kleines Startkapital. Auch
wenn hier kein echtes Geld im Spiel ist, sind die billig umsetzbaren davon
schon eingebaut - eine Bruecke, die im Testnet ohne Bremse laeuft, waere eine
schlechte Vorlage fuer alles, was spaeter daraus wird:

  * NOTBREMSE: existiert die Datei broker/STOP, wird keine Order gesendet.
    Eine Datei und nicht eine Umgebungsvariable, weil sie sich im Cron-Betrieb
    ohne Eingriff in die crontab setzen und entfernen laesst:
        touch broker/STOP      # alles aus
        rm broker/STOP         # wieder frei
  * BETRAG je Order: Standard 100 USDT, harte Obergrenze 1000 USDT. Ein
    Tippfehler in der .env kann damit keine absurde Order ausloesen.
  * ANZAHL der Orders: hoechstens MAX_ORDERS_PRO_LAUF je Aufruf und
    MAX_ORDERS_PRO_TAG innerhalb von 24 Stunden (gezaehlt aus der eigenen
    Nachverfolgung). Eine Schleife, die durchdreht, kostet damit hoechstens
    ein paar Orders statt hunderte.
"""

import hmac
import os

_BROKER_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_BROKER_DIR)
ENV_FILE = os.path.join(BASE_DIR, ".env")

# --- Endpunkt: Literale, bewusst nicht konfigurierbar ----------------------
# Quelle: offizielle Binance-Dokumentation, Ordner testnet/ in
# github.com/binance/binance-spot-api-docs - Basis "https://testnet.binance.vision/api".
# Die Schluessel dafuer entstehen auf testnet.binance.vision (Anmeldung per
# GitHub), NICHT im echten Binance-Konto. Siehe broker/README.md, dort steht
# auch, was es mit dem neueren "Demo Mode" (demo-api.binance.com) zu tun hat
# und warum dieser hier NICHT eingebaut ist.
TESTNET_BASIS = "https://testnet.binance.vision"
TESTNET_HOST = "testnet.binance.vision"
TESTNET_PFAD_PRAEFIX = "/api/"

# Hosts des ECHTEN Handels. Sie stehen hier nicht, weil der Code sie kennen
# muesste, sondern damit eine Verwechslung namentlich auffliegt statt nur
# "irgendeine falsche URL" zu sein.
VERBOTENE_HOSTS = frozenset({
    "api.binance.com", "api1.binance.com", "api2.binance.com",
    "api3.binance.com", "api4.binance.com", "api-gcp.binance.com",
    "www.binance.com", "binance.com", "fapi.binance.com", "dapi.binance.com",
    # Der Demo-Mode-Endpunkt ist kein echter Handel, aber auch nicht das
    # Testnet dieser Aufgabe - er gehoert zu einem ECHTEN Binance-Konto und
    # wird deshalb hier ebenso abgelehnt, solange er nicht ausdruecklich
    # freigegeben ist (siehe README).
    "demo-api.binance.com",
})

# --- Schluessel -----------------------------------------------------------
SCHLUESSEL_VARIABLE = "BINANCE_TESTNET_API_KEY"
GEHEIMNIS_VARIABLE = "BINANCE_TESTNET_API_SECRET"
BETRAG_VARIABLE = "BINANCE_TESTNET_BETRAG_USDT"

# Die Variablen des bestehenden Kursdatenabrufs. Werden NIE gelesen, um etwas
# damit zu tun - nur um eine Verwechslung zu erkennen.
DATENABRUF_VARIABLEN = ("BINANCE_API_KEY", "BINANCE_API_SECRET")

# --- Grenzen --------------------------------------------------------------
BETRAG_USDT_STANDARD = 100.0
BETRAG_USDT_MAX = 1000.0
MAX_ORDERS_PRO_LAUF = 5
MAX_ORDERS_PRO_TAG = 20

NOTBREMSE_DATEI = os.path.join(_BROKER_DIR, "STOP")


class ZugangFehler(Exception):
    """Fachlicher Abbruch beim Ermitteln der Zugangsdaten oder Grenzen.
    Enthaelt nie einen Schluessel oder Teile davon."""


def _parse_env_file(pfad: str) -> dict:
    """Wie notifications/telegram_config.py - dieselbe Form der .env, damit es
    im Projekt nur EIN Dateiformat fuer Zugangsdaten gibt."""
    werte = {}
    if not os.path.exists(pfad):
        return werte
    with open(pfad, encoding="utf-8") as datei:
        for zeile in datei:
            zeile = zeile.strip()
            if not zeile or zeile.startswith("#") or "=" not in zeile:
                continue
            name, _, wert = zeile.partition("=")
            werte[name.strip()] = wert.strip().strip('"').strip("'")
    return werte


def _aus_umgebung(name: str, aus_datei: dict):
    return os.environ.get(name) or aus_datei.get(name)


def get_zugang(env_datei: str = None) -> dict:
    """{'key': str, 'secret': str} - oder None, wenn einer von beiden fehlt.

    Ein fehlender Schluessel ist KEIN Fehler, sondern der Normalzustand, solange
    der Nutzer noch kein Testnet-Konto eingerichtet hat: der Trockenlauf
    funktioniert ohne Zugangsdaten und soll das auch.

    Wirft ZugangFehler nur, wenn etwas eindeutig falsch ist - vor allem bei
    einer Verwechslung mit den Schluesseln des Kursdatenabrufs.
    """
    aus_datei = _parse_env_file(env_datei or ENV_FILE)
    key = _aus_umgebung(SCHLUESSEL_VARIABLE, aus_datei)
    secret = _aus_umgebung(GEHEIMNIS_VARIABLE, aus_datei)
    if not key or not secret:
        return None

    for name in DATENABRUF_VARIABLEN:
        fremd = _aus_umgebung(name, aus_datei)
        if not fremd:
            continue
        # compare_digest statt "==": der Vergleich soll ueber seine Laufzeit
        # nichts ueber die Schluessel verraten.
        if hmac.compare_digest(fremd, key) or hmac.compare_digest(fremd, secret):
            raise ZugangFehler(
                f"{SCHLUESSEL_VARIABLE}/{GEHEIMNIS_VARIABLE} stimmen mit {name} "
                f"ueberein - das sind die Schluessel des Kursdatenabrufs und "
                f"gehoeren zu einem ECHTEN Binance-Konto. Fuer das Testnet "
                f"braucht es eigene, auf testnet.binance.vision erzeugte "
                f"Schluessel. Es wurde nichts gesendet.")
    return {"key": key, "secret": secret}


def betrag_usdt(env_datei: str = None) -> float:
    """Der Gegenwert je Order in USDT. Standard 100, Obergrenze 1000."""
    aus_datei = _parse_env_file(env_datei or ENV_FILE)
    roh = _aus_umgebung(BETRAG_VARIABLE, aus_datei)
    if roh is None or roh == "":
        return BETRAG_USDT_STANDARD
    try:
        wert = float(roh)
    except ValueError:
        raise ZugangFehler(
            f"{BETRAG_VARIABLE}={roh!r} ist keine Zahl. Es wurde nichts gesendet.")
    if wert <= 0:
        raise ZugangFehler(f"{BETRAG_VARIABLE} muss groesser als 0 sein (ist {wert:g}).")
    if wert > BETRAG_USDT_MAX:
        raise ZugangFehler(
            f"{BETRAG_VARIABLE}={wert:g} liegt ueber der festen Obergrenze "
            f"{BETRAG_USDT_MAX:g} USDT. Diese Grenze steht im Code und nicht in "
            f"der .env, damit ein Tippfehler dort keine grosse Order ausloesen "
            f"kann. Es wurde nichts gesendet.")
    return wert


def notbremse_aktiv() -> bool:
    """True, solange die Datei broker/STOP existiert. Wird unmittelbar vor
    jeder Order erneut geprueft, nicht einmal beim Start."""
    return os.path.exists(NOTBREMSE_DATEI)
