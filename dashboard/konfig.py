"""
Konfiguration des Dashboards (Token, Bindung, Zeitlimits)
==============================================================
Liest die wenigen Einstellungen des Dashboards - bevorzugt aus echten
Umgebungsvariablen, sonst aus der .env-Datei im Projekt-Root. Gleiche
Grundregel wie bei notifications/telegram_config.py und
config/email_config.py: das Zugriffs-Token steht NIE im Code, NIE in
einem Log und NIE im Repo (.env steht in .gitignore).

.env-Eintrag (neu fuer dieses Dashboard):
    DASHBOARD_ACCESS_TOKEN=<langes, zufaelliges Token>

Erzeugen laesst sich ein geeignetes Token z.B. mit
    python3 -c "import secrets; print(secrets.token_urlsafe(32))"

BEWUSSTE ENTSCHEIDUNG - FAIL CLOSED: Fehlt das Token oder ist es zu
kurz, startet das Dashboard GAR NICHT (siehe lade_token()), statt
ersatzweise ungeschuetzt zu laufen. Ein Dashboard, das versehentlich
ohne Authentifizierung startet, waere genau der Fehler, den die
Token-Pruefung verhindern soll - und man wuerde es im Betrieb nicht
bemerken, weil alles "funktioniert".
"""

import os
import sys

_DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DASHBOARD_DIR)
NOTIFICATIONS_DIR = os.path.join(BASE_DIR, "notifications")
STATIC_DIR = os.path.join(_DASHBOARD_DIR, "static")
ENV_FILE = os.path.join(BASE_DIR, ".env")

if NOTIFICATIONS_DIR not in sys.path:
    sys.path.insert(0, NOTIFICATIONS_DIR)

# Der .env-Parser wird bewusst NICHT ein zweites Mal geschrieben, sondern
# aus telegram_config.py wiederverwendet: es gibt genau EINE .env in
# diesem Projekt, und zwei Parser wuerden frueher oder spaeter
# unterschiedlich mit Anfuehrungszeichen/Kommentaren umgehen. Dass die
# Funktion dort mit Unterstrich beginnt, ist der einzige Wermutstropfen -
# eine Kopie waere die schlechtere Wahl (siehe README, Annahmen).
from telegram_config import _parse_env_file  # noqa: E402

TOKEN_VARIABLE = "DASHBOARD_ACCESS_TOKEN"

# Ein zu kurzes Token laesst sich erraten. 16 Zeichen sind die
# Untergrenze, ab der ein zufaelliges Token praktisch nicht mehr
# durchprobierbar ist; empfohlen wird oben deutlich mehr.
MIN_TOKEN_LAENGE = 16

# Nur localhost - bewusste Grundeinstellung, siehe server.py. Das
# Dashboard ist damit von anderen Geraeten im WLAN zunaechst NICHT
# erreichbar; das ist beabsichtigt, solange die Fernerreichbarkeit
# (Tailscale/SSH) noch nicht eingerichtet ist.
STANDARD_HOST = "127.0.0.1"
STANDARD_PORT = 8787

# Harte Obergrenze fuer die gebuendelte Binance-/yfinance-Kursabfrage -
# derselbe Wert und derselbe Grund wie LIVE_PRICE_TIMEOUT_SECONDS in
# notifications/telegram_bot.py: lieber eine Antwort ohne Live-Kurse als
# eine Anfrage, die beliebig lange haengt.
LIVE_KURS_TIMEOUT_SEKUNDEN = 12

# Name des Cookies, in dem der Browser das Token nach dem Login haelt.
COOKIE_NAME = "dashboard_token"


def _wert(name: str, standard=None):
    env_werte = _parse_env_file(ENV_FILE)
    return os.environ.get(name) or env_werte.get(name) or standard


def lade_token() -> str:
    """
    Gibt das konfigurierte Zugriffs-Token zurueck.

    Wirft RuntimeError, wenn keines gesetzt oder es zu kurz ist - der
    Server startet dann nicht (fail closed, siehe Modul-Docstring). Die
    Fehlermeldung nennt NIE den Token-Wert selbst, nur den Namen der
    fehlenden Variable.
    """
    token = _wert(TOKEN_VARIABLE)
    if not token:
        raise RuntimeError(
            f"{TOKEN_VARIABLE} ist weder als Umgebungsvariable noch in {ENV_FILE} "
            f"gesetzt. Das Dashboard startet ohne Zugriffsschutz NICHT. "
            f"Token erzeugen mit: python3 -c \"import secrets; print(secrets.token_urlsafe(32))\""
        )
    if len(token) < MIN_TOKEN_LAENGE:
        raise RuntimeError(
            f"{TOKEN_VARIABLE} ist kuerzer als {MIN_TOKEN_LAENGE} Zeichen und damit zu "
            f"leicht zu erraten - bitte ein laengeres, zufaelliges Token setzen."
        )
    return token


def host() -> str:
    """Bindung des Servers. Standard 127.0.0.1 (siehe STANDARD_HOST).
    Ueber DASHBOARD_HOST bewusst uebersteuerbar - wer das tut, macht das
    Dashboard im lokalen Netz erreichbar und sollte den Warnhinweis in
    server.py gelesen haben."""
    return _wert("DASHBOARD_HOST", STANDARD_HOST)


def port() -> int:
    roh = _wert("DASHBOARD_PORT", str(STANDARD_PORT))
    try:
        return int(roh)
    except (TypeError, ValueError):
        return STANDARD_PORT
