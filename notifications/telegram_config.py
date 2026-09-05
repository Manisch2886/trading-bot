"""
Telegram-Zugangsdaten
=========================
Liest TELEGRAM_BOT_TOKEN und TELEGRAM_USER_ID - bevorzugt aus echten
Umgebungsvariablen, sonst aus einer .env-Datei im Projekt-Root. Gleiche
Grundregel wie bei config/email_config.py: niemals im Code eintragen,
niemals in Logs ausgeben, niemals committen (.env steht in .gitignore).

.env-Format (eine Zeile je Variable, keine Anfuehrungszeichen noetig):
    TELEGRAM_BOT_TOKEN=123456789:AAabcDEF...
    TELEGRAM_USER_ID=123456789

TELEGRAM_USER_ID ist die numerische Telegram-User-ID des Nutzers
(NICHT der @username) - nur diese ID darf Befehle an den Bot senden,
siehe telegram_bot.py. Herausfinden z.B. ueber @userinfobot in Telegram.
"""

import os

_NOTIF_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_NOTIF_DIR)
ENV_FILE = os.path.join(BASE_DIR, ".env")


def _parse_env_file(path: str) -> dict:
    values = {}
    if not os.path.exists(path):
        return values
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            values[key] = value
    return values


def get_credentials():
    """
    Gibt {'token': str, 'user_id': int} zurueck, oder None, falls Token
    oder User-ID fehlen bzw. TELEGRAM_USER_ID keine Zahl ist. Gibt in
    KEINEM Fall Details ueber den Token selbst preis - Aufrufer duerfen
    das Ergebnis nur auf None pruefen, nicht dessen Inhalt loggen.
    """
    env_values = _parse_env_file(ENV_FILE)

    token = os.environ.get("TELEGRAM_BOT_TOKEN") or env_values.get("TELEGRAM_BOT_TOKEN")
    raw_user_id = os.environ.get("TELEGRAM_USER_ID") or env_values.get("TELEGRAM_USER_ID")

    if not token or not raw_user_id:
        return None

    try:
        user_id = int(raw_user_id)
    except ValueError:
        return None

    return {"token": token, "user_id": user_id}
