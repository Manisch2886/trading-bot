"""
Haupt-Script: Telegram-Bot fuer das Trading-System (Phase 1 - Lesen +
Benachrichtigungen)
======================================================================
Eigenstaendiger, rein lesender Dienst. Fasst KEINE der neun bestehenden
Bot-Scripts an, veraendert keine live_params.py und schliesst/eroeffnet
keine Positionen - siehe monitor.py fuer die eigentliche
Lese-/Erkennungslogik. Dieses Script ist nur die duenne Telegram-Schicht
darueber: Befehle entgegennehmen und periodisch monitor.py nach neuen
Ereignissen fragen.

Nur der in .env hinterlegte TELEGRAM_USER_ID darf Befehle senden - jeder
andere Absender wird ignoriert und geloggt (siehe restricted()).

Phase 3 (spaeter, NICHT Teil dieses Scripts): schreibender Zugriff, z.B.
Positionen ueber Telegram schliessen. Bewusst nicht vorbereitet, um
keine falsche Erwartung zu wecken, dass das schon moeglich waere.

Start (Test, im Vordergrund):
    python3 notifications/telegram_bot.py

Dauerhafter Betrieb: siehe notifications/README.md (launchd-Dienst).

Abhaengigkeit: python-telegram-bot (mit "job-queue"-Extra fuer die
periodische Ueberwachung) - siehe notifications/requirements.txt:
    pip3 install -r notifications/requirements.txt
"""

import os
import sys
import logging
from functools import wraps
from logging.handlers import RotatingFileHandler

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, ContextTypes

import telegram_config
import monitor
import notify

_NOTIF_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_NOTIF_DIR)
LOG_DIR = os.path.join(BASE_DIR, "logs", "notifications")
os.makedirs(LOG_DIR, exist_ok=True)

POLL_INTERVAL_SECONDS = int(os.environ.get("TELEGRAM_POLL_INTERVAL_SECONDS", "300"))

# WICHTIG (Root Cause eines vorherigen Diagnose-Versuchs): dieser Logger
# bekam bisher NUR einen RotatingFileHandler - beim manuellen Start im
# Vordergrund (siehe Docstring oben: "Start (Test, im Vordergrund)")
# erschien dadurch NICHTS im Terminal, nicht einmal die Start-Meldung
# "Telegram-Bot gestartet...", geschweige denn ein Fehler aus
# error_handler(). Alles landete ausschliesslich in
# logs/notifications/telegram_bot.log. Jetzt: BEIDES - Konsole (fuer den
# manuellen Live-Test) UND Datei (fuer den dauerhaften launchd-Betrieb,
# wo niemand ein Terminal offen haelt).
_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

_file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "telegram_bot.log"), maxBytes=2_000_000, backupCount=3
)
_file_handler.setFormatter(_formatter)

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setFormatter(_formatter)

logger = logging.getLogger("notifications.telegram_bot")
logger.setLevel(logging.INFO)
logger.addHandler(_file_handler)
logger.addHandler(_console_handler)

logging.getLogger("notifications.notify").setLevel(logging.INFO)
logging.getLogger("notifications.notify").addHandler(_file_handler)
logging.getLogger("notifications.notify").addHandler(_console_handler)

_CREDS = telegram_config.get_credentials()
AUTHORIZED_USER_ID = _CREDS["user_id"] if _CREDS else None


def restricted(handler):
    """Laesst nur Befehle von AUTHORIZED_USER_ID durch - jeder andere
    Absender wird stillschweigend (fuer den Absender) ignoriert, aber
    mit seiner Telegram-User-ID geloggt."""
    @wraps(handler)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id if update.effective_user else None
        if user_id != AUTHORIZED_USER_ID:
            logger.warning(f"Unautorisierter Zugriffsversuch von Telegram-User-ID {user_id}.")
            return
        return await handler(update, context)
    return wrapper


def _selector_from_args(context: ContextTypes.DEFAULT_TYPE) -> str:
    return " ".join(context.args).strip() if context.args else None


async def _reply_for_selector(update: Update, selector: str, formatter) -> None:
    bots = monitor.filter_bots(monitor.discover_bots(), selector)
    if not bots:
        known = ", ".join(sorted(monitor.ASSET_CLASS.keys()))
        text = (
            f"Kein Bot fuer Filter '{selector}' gefunden."
            if selector else "Keine Bots mit Live-Datenbank gefunden."
        )
        text += f"\n\nGueltige Filter: krypto, aktien, oder einer von: {known}"
        await update.message.reply_text(text)
        return

    try:
        text = formatter(bots)
    except Exception:
        # WICHTIG: vorher lag dieser Aufruf AUSSERHALB jeder
        # Fehlerbehandlung in dieser Funktion - eine Exception beim
        # Formatieren (z.B. durch eine Eigenheit in den echten Live-Daten,
        # die die synthetischen Sandbox-Testdaten nicht abbilden) fuehrte
        # zu KEINER Antwort in Telegram. Sie haette zwar den globalen
        # error_handler() in main() erreichen sollen, aber dessen Log
        # landete bisher NUR in der Datei, nie im Terminal (siehe Fix oben
        # bei der Logger-Konfiguration) - dadurch wirkte es wie ein
        # kompletter Blackout. Jetzt: hier direkt und sichtbar loggen
        # (Konsole + Datei) UND dem Nutzer trotzdem eine Antwort geben,
        # statt auf den globalen Handler zu vertrauen.
        logger.exception(f"Fehler beim Formatieren der Antwort (Selektor: {selector!r}).")
        await update.message.reply_text(
            "Fehler beim Abrufen der Daten - Details siehe "
            "logs/notifications/telegram_bot.log (und Terminal, falls im Vordergrund gestartet)."
        )
        return

    try:
        await update.message.reply_text(text, parse_mode="Markdown")
    except BadRequest:
        # Telegrams (legacy) Markdown-Parser lehnt eine Nachricht ab, statt
        # sie unformatiert zuzustellen, sobald er auf ein Sonderzeichen-Muster
        # trifft, das er nicht als gueltige Formatierung lesen kann (z.B.
        # durch reale Live-Daten wie Bot-/Symbolnamen oder Zahlenformate, die
        # in den synthetischen Sandbox-Testdaten so nicht vorkamen). Bisher
        # fuehrte das zu KEINER Antwort in Telegram, obwohl der Bot-Prozess
        # weiterlief - lieber unformatiert antworten als stillschweigend gar
        # nichts zu schicken. Siehe auch error_handler() in main() fuer alle
        # sonstigen unerwarteten Fehler.
        logger.warning(
            f"Markdown-Formatierung von Telegram abgelehnt, sende unformatiert erneut "
            f"(Selektor: {selector!r})."
        )
        await update.message.reply_text(text, parse_mode=None)


@restricted
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    known = ", ".join(sorted(monitor.ASSET_CLASS.keys()))
    await update.message.reply_text(
        "Trading-Bot-Ueberwachung (Phase 1 - nur lesend)\n\n"
        "/status [filter] - Kurzueberblick aller Bots\n"
        "/positions [filter] - offene Positionen, gruppiert nach Krypto/Aktien\n"
        "/pnl [filter] - Performance-Zusammenfassung\n\n"
        "filter (optional): 'krypto', 'aktien', oder ein Bot-Name:\n"
        f"{known}\n\n"
        "Automatische Push-Benachrichtigungen (neuer Trade, Stop-Loss, "
        "Cronjob-Fehler) laufen im Hintergrund, ohne dass du etwas tun musst."
    )


@restricted
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _reply_for_selector(update, _selector_from_args(context), monitor.format_status_message)


@restricted
async def positions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _reply_for_selector(update, _selector_from_args(context), monitor.format_positions_message)


@restricted
async def pnl_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _reply_for_selector(update, _selector_from_args(context), monitor.format_pnl_message)


async def poll_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Periodischer Job (siehe run_repeating in main()): fragt monitor.py
    nach neuen Ereignissen und verschickt jedes einzeln ueber
    notify.send_alert(). notify.send_alert() ist ein blockierender
    HTTP-Aufruf (siehe dortiger Kommentar) - bei der hier genutzten
    niedrigen Frequenz (alle paar Minuten, wenige Nachrichten) bewusst
    in Kauf genommen, statt eine zweite asynchrone Sende-Implementierung
    nur fuer diesen Job zu pflegen.
    """
    try:
        events = monitor.check_for_events()
    except Exception:
        logger.exception("Fehler beim periodischen Ueberwachungs-Check.")
        return

    for event_text in events:
        notify.send_alert(event_text)
    if events:
        logger.info(f"{len(events)} neue(s) Ereignis(se) verschickt.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Globaler Fallback fuer JEDE unerwartete Exception in einem Handler oder
    Job (registriert unten via add_error_handler). Vorher gab es das nicht -
    ein Fehler wie der urspruengliche /pnl-Bug (Exception beim Formatieren
    der Antwort) fiel dadurch nur als "keine Antwort in Telegram" auf, ohne
    dass im Log/Terminal etwas Konkretes dazu stand. Loest das Problem
    selbst nicht, macht ein kuenftiges aehnliches Verhalten aber sofort
    sichtbar statt nur stumm zu bleiben.
    """
    logger.error("Unerwarteter Fehler im Telegram-Bot:", exc_info=context.error)


def main():
    if AUTHORIZED_USER_ID is None:
        logger.error(
            "TELEGRAM_BOT_TOKEN/TELEGRAM_USER_ID fehlen oder sind ungueltig - "
            "siehe .env im Projekt-Root. Beende, ohne zu starten."
        )
        print(
            "Fehler: TELEGRAM_BOT_TOKEN/TELEGRAM_USER_ID fehlen oder sind ungueltig. "
            "Siehe notifications/README.md.",
            file=sys.stderr,
        )
        sys.exit(1)

    application = Application.builder().token(_CREDS["token"]).build()

    application.add_handler(CommandHandler("start", help_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("positions", positions_command))
    application.add_handler(CommandHandler("pnl", pnl_command))
    application.add_error_handler(error_handler)

    application.job_queue.run_repeating(poll_job, interval=POLL_INTERVAL_SECONDS, first=15)

    logger.info(f"Telegram-Bot gestartet (Poll-Intervall {POLL_INTERVAL_SECONDS}s).")
    application.run_polling()


if __name__ == "__main__":
    main()
