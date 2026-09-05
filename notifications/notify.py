"""
Hilfsmodul: send_alert(text)
================================
Schickt eine einzelne Text-Nachricht an den in .env hinterlegten
TELEGRAM_USER_ID, ueber die offizielle Telegram-Bot-API (HTTPS POST,
reine Standardbibliothek - kein zusaetzlicher Dependency wie
python-telegram-bot noetig, damit dieses Modul auch von KUENFTIGEN,
einfachen Scripts importiert werden kann, ohne dass die dafuer erst
python-telegram-bot installieren muessten).

Nutzung aus einem beliebigen anderen Script:

    import os, sys
    sys.path.insert(0, os.path.join(BASE_DIR, "notifications"))
    from notify import send_alert
    send_alert("Testnachricht")

Gibt bei Erfolg True zurueck, sonst False - wirft NIE eine Exception
nach aussen (analog zu shared/claude_client.py: ein fehlgeschlagener
Alert darf nie das aufrufende Script zum Absturz bringen).

Sicherheit: Der Bot-Token taucht in der Ziel-URL auf - diese wird an
KEINER Stelle geloggt oder ausgegeben, nur der Erfolg/Fehlerstatus.
"""

import json
import logging
import urllib.request
import urllib.error

from telegram_config import get_credentials

logger = logging.getLogger("notifications.notify")

TELEGRAM_API_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"


def send_alert(text: str, parse_mode: str = "Markdown") -> bool:
    """
    parse_mode: "Markdown" (Standard, unveraendertes Verhalten fuer alle
    bestehenden Aufrufer - monitor.py:check_for_events() nutzt bewusst
    gesetzte *fette*/`code`-Markdown-Entities in seinen Alert-Texten) oder
    None, um die Nachricht KOMPLETT unformatiert (kein Markdown-Parsing
    durch Telegram) zu verschicken - siehe send_report() fuer den Grund.
    """
    creds = get_credentials()
    if not creds:
        logger.error(
            "Kein TELEGRAM_BOT_TOKEN/TELEGRAM_USER_ID in .env gefunden - "
            "Alert wird verworfen (Nachrichtentext wird hier bewusst NICHT "
            "geloggt, da er Handelsdaten enthalten kann)."
        )
        return False

    url = TELEGRAM_API_URL_TEMPLATE.format(token=creds["token"])
    payload_dict = {"chat_id": creds["user_id"], "text": text}
    if parse_mode:
        payload_dict["parse_mode"] = parse_mode
    payload = json.dumps(payload_dict).encode("utf-8")

    request = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status != 200:
                logger.error(f"Telegram-API antwortete mit Status {response.status}.")
                return False
        return True
    except urllib.error.URLError as e:
        logger.error(f"Telegram-Alert fehlgeschlagen (Netzwerk-/API-Fehler): {e}")
        return False
    except Exception as e:
        logger.error(f"Telegram-Alert fehlgeschlagen (unerwarteter Fehler): {e}")
        return False


# ---------------------------------------------------------------------------
# send_report(subject, body): fuer die ehemaligen E-Mail-Versandstellen
# (shared/weekly_portfolio_email.py, */daily_summary_email.py,
# */quarterly_review.py) - siehe Aufgabe "Bot-eigene E-Mails durch direkten
# Telegram-Versand ersetzen". Baut auf send_alert() auf, KEINE zweite,
# parallele Telegram-Anbindung.
# ---------------------------------------------------------------------------

# Telegram-Nachrichtenlimit ist 4096 Zeichen - dieselbe Sicherheitsmarge wie
# in notifications/monitor.py:MAX_MESSAGE_LENGTH fuer /status, damit
# Formatierungs-Overhead nicht ausversehen doch ueber das Limit rutscht.
MAX_MESSAGE_LENGTH = 3500


def _split_into_chunks(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> list:
    """
    Teilt einen langen Text an Zeilenumbruechen in mehrere Telegram-taugliche
    Chunks auf - adaptiert aus derselben Grundidee wie
    notifications/monitor.py:format_status_message() (dort pro Bot-Block,
    hier pro Zeile des Berichts), damit eine lange woechentliche/
    quartalsweise Zusammenfassung nicht am 4096-Zeichen-Limit einer
    einzelnen Telegram-Nachricht abgeschnitten wird.
    """
    lines = text.split("\n")
    chunks = []
    current = []
    for line in lines:
        candidate = "\n".join(current + [line])
        if current and len(candidate) > max_length:
            chunks.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        chunks.append("\n".join(current))
    return chunks


def send_report(subject: str, body: str) -> bool:
    """
    Verschickt einen laengeren Bericht (ehemals E-Mail-Betreff + -Body) als
    eine oder mehrere Telegram-Nachrichten:
      1. Betreff wird als reine Text-Zeile vorangestellt - Ersatz fuer den
         E-Mail-Betreff, den eine Telegram-Nachricht nicht kennt. BEWUSST
         OHNE Fettung/Markdown (siehe unten, Root Cause eines Live-Bugs).
      2. Bei Ueberschreiten von MAX_MESSAGE_LENGTH wird in mehrere
         Nachrichten aufgeteilt (siehe _split_into_chunks); jeder Chunk ab
         dem zweiten bekommt eine "(Fortsetzung)"-Markierung.
      3. Die gesamte Nachricht wird OHNE parse_mode (also als reiner,
         unformatierter Text) verschickt.

    ROOT CAUSE eines Live-Bugs (erste Version dieser Funktion): der erste
    Anlauf hat Betreff+Body vor dem Versand "Markdown-escaped" (Backslash
    vor _ * ` [) und den Betreff in *...* eingefasst, mit parse_mode=
    "Markdown" verschickt. Live-Test zeigte danach woertliche Backslashes
    in der Betreffzeile ("Trading Bot \\[elliott\\_wave] - ..."). Ursache:
    Telegrams LEGACY-Markdown-Modus (parse_mode="Markdown", im Unterschied
    zu "MarkdownV2") kennt laut offizieller Bot-API-Doku GAR KEIN
    Backslash-Escaping - dieser Mechanismus ist ausschliesslich fuer
    MarkdownV2 spezifiziert. Im Legacy-Modus wird ein Backslash einfach als
    gewoehnliches Zeichen durchgereicht, OHNE das nachfolgende
    Sonderzeichen zu neutralisieren - die eingefuegten Escape-Backslashes
    landeten deshalb woertlich sichtbar beim Nutzer, statt etwas zu
    bewirken. Der Bericht-Text selbst (E-Mail-Betreffs/Datei-Pfade mit "_"
    und "[") ist ohnehin reiner Inhaltstext ohne beabsichtigte
    Markdown-Formatierung - die robusteste Loesung ist deshalb, fuer
    send_report() komplett auf parse_mode zu verzichten (send_alert(...,
    parse_mode=None)) statt eine fehlerhafte Escape-Strategie zu
    reparieren: kein Formatierungsrisiko mehr durch IRGENDein
    Sonderzeichen in beliebigem Bot-/Datei-/Betreff-Text, dafuer keine
    Fettung der Ueberschrift - das wurde als klar vorzugswuerdig
    eingestuft gegenueber einem Umstieg auf MarkdownV2 (dort muessten
    praktisch alle Satzzeichen im gesamten Bericht escaped werden, u.a.
    Punkte in Prozentzahlen und Bindestriche in negativen Werten).

    Nutzt fuer den eigentlichen Versand ausschliesslich die bestehende
    send_alert() - dieselbe Funktion, die auch fuer die (weiterhin
    Markdown-formatierten) Event-Alerts aus notifications/monitor.py
    verwendet wird; send_report() ruft sie lediglich mit parse_mode=None
    auf, alle anderen Aufrufer sind unveraendert.

    Gibt True zurueck, wenn ALLE Chunks erfolgreich verschickt wurden, sonst
    False - bricht beim ersten fehlgeschlagenen Chunk ab (sendet keine
    spaeteren Chunks mehr, um keine Nachricht ausser Reihenfolge nach einem
    bereits sichtbaren Fehler zu verschicken).
    """
    full_text = f"{subject}\n\n{body}"

    chunks = _split_into_chunks(full_text)
    for i, chunk in enumerate(chunks):
        text = chunk if i == 0 else f"(Fortsetzung)\n\n{chunk}"
        if not send_alert(text, parse_mode=None):
            return False
    return True


if __name__ == "__main__":
    ok = send_alert("Testnachricht von notify.py - wenn du das siehst, funktioniert der Versand.")
    print("Erfolgreich versendet." if ok else "Versand fehlgeschlagen - siehe Log/Fehlermeldung oben.")
