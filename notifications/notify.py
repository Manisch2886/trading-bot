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


def send_alert(text: str) -> bool:
    creds = get_credentials()
    if not creds:
        logger.error(
            "Kein TELEGRAM_BOT_TOKEN/TELEGRAM_USER_ID in .env gefunden - "
            "Alert wird verworfen (Nachrichtentext wird hier bewusst NICHT "
            "geloggt, da er Handelsdaten enthalten kann)."
        )
        return False

    url = TELEGRAM_API_URL_TEMPLATE.format(token=creds["token"])
    payload = json.dumps({
        "chat_id": creds["user_id"],
        "text": text,
        "parse_mode": "Markdown",
    }).encode("utf-8")

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

# Die vier in Telegrams LEGACY-Markdown-Modus (parse_mode="Markdown", siehe
# send_alert()) reservierten Zeichen.
_MARKDOWN_SPECIAL_CHARS = "_*`["


def _escape_markdown(text: str) -> str:
    """
    Escaped die vier Markdown-Sonderzeichen in beliebigem Freitext. Noetig,
    weil die Berichte (ehemalige E-Mail-Bodies) Datei-Pfade mit Unterstrichen
    (z.B. "strategies/t3_supertrend/live_params.py") und E-Mail-Betreffs mit
    eckigen Klammern (z.B. "Trading Bot [rsi2_crypto] - ...") enthalten -
    unescaped wuerde Telegrams Markdown-Parser das als (moeglicherweise
    unvollstaendige) Formatierung interpretieren und mit BadRequest
    fehlschlagen. Exakt dieselbe Fehlerklasse, die bereits in
    telegram_bot.py zu einem BadRequest-Bug fuehrte (siehe dortige
    _send_reply()-Historie) - hier von vornherein vermieden statt erst
    nachtraeglich abgefangen.
    """
    for ch in _MARKDOWN_SPECIAL_CHARS:
        text = text.replace(ch, f"\\{ch}")
    return text


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
      1. Betreff wird als fette erste Zeile vorangestellt - Ersatz fuer den
         E-Mail-Betreff, den eine Telegram-Nachricht nicht kennt.
      2. Betreff UND Body werden vor dem Versand Markdown-escaped (siehe
         _escape_markdown) - der Bericht ist inhaltlich reiner Text, keine
         beabsichtigte Markdown-Formatierung, daher wird alles ausser der
         bewusst gesetzten fetten Ueberschrift als Literal behandelt.
      3. Bei Ueberschreiten von MAX_MESSAGE_LENGTH wird in mehrere
         Nachrichten aufgeteilt (siehe _split_into_chunks); jeder Chunk ab
         dem zweiten bekommt eine "(Fortsetzung)"-Markierung.

    Nutzt fuer den eigentlichen Versand ausschliesslich die bestehende
    send_alert() - dieselbe Funktion, die auch fuer die Event-Alerts aus
    notifications/monitor.py verwendet wird.

    Gibt True zurueck, wenn ALLE Chunks erfolgreich verschickt wurden, sonst
    False - bricht beim ersten fehlgeschlagenen Chunk ab (sendet keine
    spaeteren Chunks mehr, um keine Nachricht ausser Reihenfolge nach einem
    bereits sichtbaren Fehler zu verschicken).
    """
    header = f"*{_escape_markdown(subject)}*"
    full_text = f"{header}\n\n{_escape_markdown(body)}"

    chunks = _split_into_chunks(full_text)
    for i, chunk in enumerate(chunks):
        text = chunk if i == 0 else f"(Fortsetzung)\n\n{chunk}"
        if not send_alert(text):
            return False
    return True


if __name__ == "__main__":
    ok = send_alert("Testnachricht von notify.py - wenn du das siehst, funktioniert der Versand.")
    print("Erfolgreich versendet." if ok else "Versand fehlgeschlagen - siehe Log/Fehlermeldung oben.")
