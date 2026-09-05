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


if __name__ == "__main__":
    ok = send_alert("Testnachricht von notify.py - wenn du das siehst, funktioniert der Versand.")
    print("Erfolgreich versendet." if ok else "Versand fehlgeschlagen - siehe Log/Fehlermeldung oben.")
