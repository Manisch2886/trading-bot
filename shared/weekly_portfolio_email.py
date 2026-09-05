"""
Woechentliche Portfolio-E-Mail
================================================
Orchestriert Agent 4 (portfolio_interpreter_agent.py) rund um
portfolio_overview.py: fuehrt die bestehende, unveraenderte
Portfolio-Uebersicht aus, fasst ihre Textausgabe zusammen, laesst Claude
das einordnen, und verschickt beides als eine E-Mail - im selben
Format/Design wie die bestehenden daily_summary_email.py-Skripte der
einzelnen Bots (gleicher SMTP-Versand ueber config/email_config.py, IONOS).

WICHTIG: portfolio_overview.py selbst wird NICHT veraendert (bleibt rein
lesend, wie es sein docstring schon festhaelt) - dieses Skript ruft nur
seine main()-Funktion auf und faengt deren print()-Ausgabe per
contextlib.redirect_stdout ab, um denselben Text zu bekommen, den ein
manueller Aufruf auf der Konsole sehen wuerde. Kein Duplizieren der
Analyse-Logik.

Gedacht fuer einen WOECHENTLICHEN Cronjob, kurz NACH dem bestehenden
woechentlichen portfolio_overview.py-Lauf (siehe Cronjob-Vorschlag in der
PR-Beschreibung) - absichtlich getrennte Skripte/Cronjob-Zeilen, damit ein
Fehler in der E-Mail/Agent-Stufe niemals die reine Datenerhebung
(CSV-Speicherung) verhindert.
"""

import os
import sys
import io
import contextlib
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
_BASE_DIR = os.path.dirname(_SHARED_DIR)
_CONFIG_DIR = os.path.join(_BASE_DIR, "config")
sys.path.insert(0, _CONFIG_DIR)
import email_config as cfg

_NOTIF_DIR = os.path.join(_BASE_DIR, "notifications")
sys.path.insert(0, _NOTIF_DIR)
from notify import send_report

import portfolio_overview
from portfolio_interpreter_agent import generate_portfolio_interpretation

USE_INTERPRETATION_AGENT = True

# E-Mail-Versand deaktiviert (siehe Aufgabe "Bot-eigene E-Mails durch
# direkten Telegram-Versand ersetzen") - Telegram (send_report(), siehe
# notifications/notify.py) ist jetzt der primaere Versandweg. Der
# SMTP-Code (send_email() unten) bleibt bewusst UNVERAENDERT bestehen,
# nur ueber diesen Flag deaktiviert - falls sich Telegram in der Praxis
# doch als unzuverlaessig erweisen sollte, kann hier schnell zurueck-
# geschaltet werden, ohne den alten Code neu schreiben zu muessen.
# Vollstaendiges Entfernen ist fuer eine spaetere, separate Aufgabe
# vorgesehen.
SEND_VIA_EMAIL = False


def run_portfolio_overview_and_capture() -> str:
    """Fuehrt portfolio_overview.main() aus und gibt dessen komplette
    print()-Ausgabe als String zurueck - identisch zu dem, was ein
    manueller Konsolen-Aufruf zeigen wuerde."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        portfolio_overview.main()
    return buffer.getvalue()


def build_email_body(overview_text: str, interpretation: str) -> str:
    """Baut den E-Mail-Text. Reihenfolge bewusst so gewaehlt, dass die
    verstaendliche Handlungsempfehlung (Teil A von Agent 4, "WAS DAS FUER
    DICH BEDEUTET") ganz oben steht, VOR den Rohdaten-Tabellen von
    portfolio_overview.py - damit das Wichtigste zuerst kommt und nicht
    erst nach mehreren Bildschirmseiten Tabellen. Die Rohdaten bleiben
    vollstaendig erhalten, nur weiter unten fuer den Detailblick."""
    now = datetime.utcnow()
    lines = []
    lines.append(f"Woechentliche Portfolio-Uebersicht - {now.strftime('%d.%m.%Y %H:%M')} UTC")
    lines.append("=" * 60)

    if interpretation:
        lines.append("")
        lines.append("KI-EINORDNUNG DER WOCHE")
        lines.append("=" * 60)
        lines.append("")
        lines.append(interpretation)
        lines.append("")
        lines.append("=" * 60)
        lines.append("ROHDATEN (Tabellen, Korrelationswerte, Einzel-Bot-Drawdowns)")
        lines.append("=" * 60)

    lines.append("")
    lines.append(overview_text.rstrip())

    return "\n".join(lines)


def send_email(subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = cfg.EMAIL_ADDRESS
    msg["To"] = cfg.RECIPIENT_EMAIL

    if cfg.USE_SSL:
        server = smtplib.SMTP_SSL(cfg.SMTP_SERVER, cfg.SMTP_PORT)
    else:
        server = smtplib.SMTP(cfg.SMTP_SERVER, cfg.SMTP_PORT)
        server.starttls()

    server.login(cfg.EMAIL_ADDRESS, cfg.EMAIL_PASSWORD)
    server.sendmail(cfg.EMAIL_ADDRESS, cfg.RECIPIENT_EMAIL, msg.as_string())
    server.quit()


if __name__ == "__main__":
    print("Fuehre portfolio_overview.py aus und fasse die Ausgabe zusammen...\n")
    overview_text = run_portfolio_overview_and_capture()
    print(overview_text)

    interpretation = ""
    if USE_INTERPRETATION_AGENT:
        print("\nHole KI-Einordnung der Woche (Agent 4)...")
        interpretation = generate_portfolio_interpretation(overview_text)
        if interpretation:
            print(f"Einordnung: {interpretation}")
        else:
            print("(Keine Einordnung erhalten - API-Key gesetzt? Siehe shared/claude_client.py)")

    email_body = build_email_body(overview_text, interpretation)

    subject = "Trading Bot [Portfolio-Uebersicht] - Woechentliche Zusammenfassung"
    try:
        if SEND_VIA_EMAIL:
            send_email(subject, email_body)
            print("\nE-Mail erfolgreich verschickt.")
        elif send_report(subject, email_body):
            print("\nTelegram-Nachricht(en) erfolgreich verschickt.")
        else:
            print("\nTelegram-Versand fehlgeschlagen - siehe Log/Fehlermeldung von notify.py.")
    except Exception as e:
        print(f"\nFehler beim Versand: {e}")
        print("Pruefe deine Angaben in email_config.py bzw. .env (Telegram).")
