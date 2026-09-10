"""
Zugang und Sicherheitsgrenzen der IBKR-Paper-Bruecke
==============================================================================
Gegenstueck zu broker/zugang.py, aber mit einem grundlegend anderen Weg nach
draussen: bei Binance ist es eine REST-URL, hier ein LOKALER Socket zu einer
Software, die auf demselben Rechner laeuft (Trader Workstation oder IB Gateway).
Der Unterschied verschiebt die Gefahr: nicht eine falsche URL fuehrt zum echten
Handel, sondern ein falscher PORT oder eine TWS-Sitzung, die am Live-Konto
angemeldet ist.

Deshalb gibt es hier ZWEI voneinander unabhaengige Absicherungen, und beide
muessen halten:

  1. PORT. Verbunden wird nur auf einem Port, der bei IBKR fuer Paper-Trading
     vorgesehen ist (TWS 7497, IB Gateway 4002). Die Live-Ports (TWS 7496,
     IB Gateway 4001) stehen namentlich auf einer Verbotsliste - damit eine
     Verwechslung als solche auffliegt und nicht bloss als "Verbindung
     fehlgeschlagen".
  2. KONTO. Nach dem Verbindungsaufbau meldet TWS die verwalteten Konten.
     Jedes davon muss ein Paper-Konto sein (Praefix DU bzw. DF; Live-Konten
     beginnen mit U ohne D), und das in der .env hinterlegte Konto muss
     darunter sein. Taucht ein Live-Konto auf, wird abgebrochen, BEVOR
     irgendeine Order entsteht - dann ist TWS am falschen Konto angemeldet,
     und daran aendert auch der richtige Port nichts.

Eine Absicherung allein reicht nicht: der Port sagt, welche Sitzung man
erwartet, das Konto sagt, welche man bekommen hat.

------------------------------------------------------------------------------
.env-Format (Projekt-Root, steht in .gitignore)
------------------------------------------------------------------------------
    IBKR_PAPER_KONTO=DU1234567        # Pflicht fuer echte Orders
    IBKR_PAPER_PORT=7497              # optional; nur 7497 oder 4002 erlaubt
    IBKR_PAPER_STUECK=1               # optional, Standard 1 Stueck je Order
    IBKR_PAPER_CLIENT_ID=42           # optional

Es gibt KEIN Passwort und keinen Schluessel: die Anmeldung passiert in TWS,
die API vertraut der lokalen Verbindung. Genau deshalb ist der Host hier ein
Literal (127.0.0.1) - eine Umgebungsvariable fuer den Host waere die Moeglichkeit,
sich mit einer TWS auf einem ANDEREN Rechner zu verbinden, von der niemand
weiss, an welchem Konto sie haengt.

------------------------------------------------------------------------------
WARUM STUECK UND NICHT GEGENWERT
------------------------------------------------------------------------------
Die Binance-Bruecke rechnet einen Gegenwert in USDT in eine Menge um. Das
braucht einen aktuellen Kurs - und bei IBKR braucht ein Kurs ein
Marktdaten-Abonnement, das ein Paper-Konto nicht zwangslaeufig hat. Ein
fehlender Kurs wuerde die Order scheitern lassen, obwohl sie ausfuehrbar waere.
Standard ist deshalb eine feste STUECKZAHL (1), die ohne Marktdaten auskommt.
Fuer den Erkenntnisgewinn dieser Anbindung - Vergleich der PREISE, nicht der
Groessen - genuegt ein Stueck vollkommen.
"""

import os

_BROKER_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_BROKER_DIR)
ENV_FILE = os.path.join(BASE_DIR, ".env")

# --- Verbindung: Literale, bewusst nicht frei konfigurierbar ---------------
# Quelle: IBKR-Dokumentation "TWS API v9.72+: Initial Setup" sowie die
# IBKR-Campus-Seite "Installing & Configuring TWS for the API" - Stand der
# Pruefung September 2026. Die Ports sind Standardwerte und in TWS
# aenderbar; wer sie dort verstellt, muss hier bewusst nachziehen.
HOST = "127.0.0.1"
PAPER_PORTS = {"TWS": 7497, "IB Gateway": 4002}
LIVE_PORTS = {"TWS": 7496, "IB Gateway": 4001}
ERLAUBTE_PORTS = tuple(sorted(PAPER_PORTS.values()))      # (4002, 7497)
STANDARD_PORT = PAPER_PORTS["TWS"]

# Paper-Konten beginnen mit DU (Einzelkonten) bzw. DF (institutionelle
# Paper-Konten). Live-Konten beginnen mit U. Quelle: IBKR-Dokumentation zu
# Paper-Trading-Konten ("wenn der Live-Benutzername U12345678 ist, lautet der
# Paper-Benutzername DU12345678").
PAPER_PRAEFIXE = ("DU", "DF")

KONTO_VARIABLE = "IBKR_PAPER_KONTO"
PORT_VARIABLE = "IBKR_PAPER_PORT"
STUECK_VARIABLE = "IBKR_PAPER_STUECK"
CLIENT_ID_VARIABLE = "IBKR_PAPER_CLIENT_ID"

# --- Grenzen --------------------------------------------------------------
STUECK_STANDARD = 1
STUECK_MAX = 50
MAX_ORDERS_PRO_LAUF = 5
MAX_ORDERS_PRO_TAG = 20
CLIENT_ID_STANDARD = 42

NOTBREMSE_DATEI = os.path.join(_BROKER_DIR, "STOP_IBKR")

# Die Bot-Symbole stammen aus config/sp500_top150.txt in Yahoo-Schreibweise.
# IBKR schreibt Aktienklassen mit LEERZEICHEN statt Bindestrich: BRK-B heisst
# dort "BRK B". Uebersetzt wird nur, was hier ausdruecklich steht - jedes
# andere Symbol mit Punkt oder Bindestrich wird ABGELEHNT statt geraten. Ein
# falsch geratenes Kuerzel kauft bei einem Broker das falsche Unternehmen,
# und das faellt erst im Depot auf.
SYMBOL_UEBERSETZUNG = {"BRK-B": "BRK B"}
BOERSE = "SMART"        # IBKRs Routing ueber alle US-Plaetze
WAEHRUNG = "USD"


class ZugangFehler(Exception):
    """Fachlicher Abbruch, bei dem nichts gesendet wurde."""


def _parse_env_file(pfad: str) -> dict:
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


def _wert(name: str, aus_datei: dict):
    return os.environ.get(name) or aus_datei.get(name)


def port(env_datei: str = None) -> int:
    """Der Verbindungsport - ausschliesslich aus der Paper-Liste.

    Anders als bei der Binance-Bruecke darf hier ueberhaupt eine
    Umgebungsvariable mitreden, und das hat einen Grund: TWS und IB Gateway
    sind beide legitime Gegenstellen mit VERSCHIEDENEN Paper-Ports, und welche
    der Nutzer laufen laesst, ist seine Entscheidung. Die Auswahl ist aber auf
    genau diese zwei Werte beschraenkt - eine freie Zahl waere der Weg zum
    Live-Port.
    """
    roh = _wert(PORT_VARIABLE, _parse_env_file(env_datei or ENV_FILE))
    if roh is None or roh == "":
        return STANDARD_PORT
    try:
        gewuenscht = int(roh)
    except ValueError:
        raise ZugangFehler(f"{PORT_VARIABLE}={roh!r} ist keine Zahl.")
    return pruefe_port(gewuenscht)


def pruefe_port(gewuenscht: int) -> int:
    """Die erste der beiden Absicherungen. Wird auch unmittelbar vor dem
    Verbindungsaufbau erneut aufgerufen, nicht nur hier."""
    for name, live in LIVE_PORTS.items():
        if gewuenscht == live:
            raise ZugangFehler(
                f"ABGEBROCHEN: Port {gewuenscht} ist der LIVE-Port von {name}. "
                f"Diese Bruecke verbindet ausschliesslich auf einen "
                f"Paper-Port ({', '.join(f'{n} {p}' for n, p in PAPER_PORTS.items())}). "
                f"Es wurde nichts gesendet.")
    if gewuenscht not in ERLAUBTE_PORTS:
        raise ZugangFehler(
            f"ABGEBROCHEN: Port {gewuenscht} ist keiner der Paper-Ports "
            f"{ERLAUBTE_PORTS}. Falls TWS bei dir auf einem anderen Port "
            f"horcht, muss das hier bewusst im Code nachgezogen werden - nicht "
            f"in der .env. Es wurde nichts gesendet.")
    return gewuenscht


def ist_paper_konto(konto: str) -> bool:
    return bool(konto) and konto.upper().startswith(PAPER_PRAEFIXE)


def pruefe_konten(gemeldete, erwartet: str = None) -> str:
    """Die zweite Absicherung, nach dem Verbindungsaufbau.

    `gemeldete` ist die Liste aus IBKRs managedAccounts(). Abgebrochen wird,
    wenn eines davon KEIN Paper-Konto ist (dann ist TWS am Live-Konto
    angemeldet - der richtige Port hilft dann nichts) oder wenn das erwartete
    Konto nicht darunter ist.
    """
    konten = [k.strip() for k in (gemeldete or []) if k and k.strip()]
    if not konten:
        raise ZugangFehler(
            "TWS hat kein Konto gemeldet. Ohne bestaetigte Konto-Kennung wird "
            "nichts gehandelt - laeuft die Anmeldung in TWS/Gateway wirklich?")
    fremd = [k for k in konten if not ist_paper_konto(k)]
    if fremd:
        raise ZugangFehler(
            f"ABGEBROCHEN: TWS meldet {fremd} - das ist kein Paper-Konto "
            f"(Paper beginnt mit {' oder '.join(PAPER_PRAEFIXE)}). Diese "
            f"Sitzung ist offenbar am ECHTEN Konto angemeldet. Es wurde nichts "
            f"gesendet.")
    if erwartet:
        if erwartet not in konten:
            raise ZugangFehler(
                f"ABGEBROCHEN: das erwartete Konto {erwartet} ({KONTO_VARIABLE} "
                f"in der .env) ist nicht unter den gemeldeten Konten {konten}. "
                f"Es wurde nichts gesendet.")
        return erwartet
    if len(konten) > 1:
        raise ZugangFehler(
            f"TWS meldet mehrere Konten {konten}. Dann muss {KONTO_VARIABLE} in "
            f"der .env sagen, welches gemeint ist - geraten wird hier nicht.")
    return konten[0]


def erwartetes_konto(env_datei: str = None):
    """Das Konto aus der .env - oder None. Fuer den Trockenlauf ist es nicht
    noetig; fuer echte Orders schon (siehe ibkr_spiegel.py)."""
    roh = _wert(KONTO_VARIABLE, _parse_env_file(env_datei or ENV_FILE))
    if not roh:
        return None
    roh = roh.strip()
    if not ist_paper_konto(roh):
        raise ZugangFehler(
            f"{KONTO_VARIABLE}={roh!r} sieht nicht wie ein Paper-Konto aus "
            f"(erwartet wird ein Praefix aus {PAPER_PRAEFIXE}). Ein Live-Konto "
            f"darf hier nicht stehen.")
    return roh


def stueck(env_datei: str = None) -> int:
    roh = _wert(STUECK_VARIABLE, _parse_env_file(env_datei or ENV_FILE))
    if roh is None or roh == "":
        return STUECK_STANDARD
    try:
        wert = int(roh)
    except ValueError:
        raise ZugangFehler(f"{STUECK_VARIABLE}={roh!r} ist keine ganze Zahl.")
    if wert <= 0:
        raise ZugangFehler(f"{STUECK_VARIABLE} muss groesser als 0 sein (ist {wert}).")
    if wert > STUECK_MAX:
        raise ZugangFehler(
            f"{STUECK_VARIABLE}={wert} liegt ueber der festen Obergrenze "
            f"{STUECK_MAX} Stueck. Diese Grenze steht im Code und nicht in der "
            f".env, damit ein Tippfehler dort keine grosse Order ausloesen kann.")
    return wert


def client_id(env_datei: str = None) -> int:
    roh = _wert(CLIENT_ID_VARIABLE, _parse_env_file(env_datei or ENV_FILE))
    if roh is None or roh == "":
        return CLIENT_ID_STANDARD
    try:
        return int(roh)
    except ValueError:
        raise ZugangFehler(f"{CLIENT_ID_VARIABLE}={roh!r} ist keine Zahl.")


def ibkr_symbol(symbol: str) -> str:
    """Das Boersenkuerzel in IBKR-Schreibweise - oder ein Abbruch."""
    if not symbol or not symbol.strip():
        raise ZugangFehler("Leeres Symbol.")
    symbol = symbol.strip().upper()
    if symbol in SYMBOL_UEBERSETZUNG:
        return SYMBOL_UEBERSETZUNG[symbol]
    if any(zeichen in symbol for zeichen in ".-/ "):
        raise ZugangFehler(
            f"Das Symbol {symbol!r} enthaelt ein Sonderzeichen und steht nicht in "
            f"SYMBOL_UEBERSETZUNG. IBKR schreibt Aktienklassen anders als die "
            f"Kursdatenquelle (BRK-B heisst dort 'BRK B'); geraten wird das "
            f"nicht, weil ein falsches Kuerzel das falsche Unternehmen kauft. "
            f"Bitte die Uebersetzung in broker/ibkr_zugang.py ergaenzen.")
    if not symbol.isalpha():
        raise ZugangFehler(f"Das Symbol {symbol!r} sieht nicht wie ein "
                            f"Aktienkuerzel aus.")
    return symbol


def notbremse_aktiv() -> bool:
    """True, solange broker/STOP_IBKR existiert. EIGENE Datei, nicht dieselbe
    wie bei Binance: die beiden Bruecken sollen sich getrennt anhalten lassen -
    ein Problem an einer Boerse ist kein Grund, die andere mitzustoppen."""
    return os.path.exists(NOTBREMSE_DATEI)
