"""
Phase 4b - Taegliche E-Mail-Zusammenfassung: Turtle Soup (Aktien)
================================================================================
Analog zu volatility_breakout/daily_summary_email.py.
"""

import os
import sys
import smtplib
import sqlite3
from datetime import datetime, timedelta
from email.mime.text import MIMEText

import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
DB_FILE = _P["DB_FILE"]
STRATEGY_NAME = _P["STRATEGY_NAME"]
CONFIG_DIR = _P["CONFIG_DIR"]

sys.path.insert(0, CONFIG_DIR)
import email_config as cfg

from daily_interpreter import generate_interpretation
from market_context_agent import get_market_context

USE_INTERPRETATION_AGENT = True
USE_MARKET_CONTEXT_AGENT = True


def load_data() -> tuple:
    conn = sqlite3.connect(DB_FILE)
    open_trades = pd.read_sql("SELECT * FROM trades WHERE status='open'", conn)
    closed_trades = pd.read_sql("SELECT * FROM trades WHERE status='closed'", conn)
    conn.close()
    return open_trades, closed_trades


def format_stop(stop_price) -> str:
    if stop_price is None or (isinstance(stop_price, float) and pd.isna(stop_price)):
        return "kein Stop"
    return f"{stop_price:.2f}"


def build_summary_text(open_trades: pd.DataFrame, closed_trades: pd.DataFrame) -> str:
    now = datetime.utcnow()
    yesterday = now - timedelta(hours=24)

    lines = []
    lines.append(f"Forward-Test-Uebersicht - {now.strftime('%d.%m.%Y %H:%M')} UTC")
    lines.append("=" * 50)
    lines.append("")

    if not open_trades.empty:
        open_trades = open_trades.copy()
        open_trades["entry_time"] = pd.to_datetime(open_trades["entry_time"])
        new_positions = open_trades[open_trades["entry_time"] >= yesterday]
    else:
        new_positions = pd.DataFrame()

    lines.append(f"NEUE POSITIONEN (letzte 24h): {len(new_positions)}")
    if not new_positions.empty:
        for _, t in new_positions.iterrows():
            lines.append(f"  - {t['symbol']}: Entry {t['entry_price']:.2f}, "
                          f"Stop {format_stop(t['stop_price'])}")
    lines.append("")

    if not closed_trades.empty:
        closed_trades = closed_trades.copy()
        closed_trades["exit_time"] = pd.to_datetime(closed_trades["exit_time"])
        recent_closed = closed_trades[closed_trades["exit_time"] >= yesterday]
    else:
        recent_closed = pd.DataFrame()

    lines.append(f"GESCHLOSSENE TRADES (letzte 24h): {len(recent_closed)}")
    if not recent_closed.empty:
        for _, t in recent_closed.iterrows():
            lines.append(f"  - {t['symbol']}: {t['result']}, PnL {t['pnl_pct']:.2f}%")
    lines.append("")

    lines.append(f"OFFENE POSITIONEN INSGESAMT: {len(open_trades)}")
    if not open_trades.empty:
        for _, t in open_trades.iterrows():
            lines.append(f"  - {t['symbol']}: Entry {t['entry_price']:.2f} "
                          f"(seit {t['entry_time']}), Stop {format_stop(t['stop_price'])}")
    lines.append("")

    lines.append("GESAMT-PERFORMANCE (seit Start des Forward Tests)")
    if not closed_trades.empty:
        win_rate = (closed_trades["pnl_pct"] > 0).mean() * 100
        total_pnl = closed_trades["pnl_pct"].sum()
        avg_pnl = closed_trades["pnl_pct"].mean()
        lines.append(f"  Geschlossene Trades gesamt: {len(closed_trades)}")
        lines.append(f"  Win Rate: {win_rate:.1f}%")
        lines.append(f"  Summe PnL: {total_pnl:.2f}%")
        lines.append(f"  Ø PnL pro Trade: {avg_pnl:.2f}%")
    else:
        lines.append("  Noch keine geschlossenen Trades.")

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
    open_trades, closed_trades = load_data()
    summary = build_summary_text(open_trades, closed_trades)

    print(summary)

    email_body = summary

    if USE_INTERPRETATION_AGENT:
        print("\nHole KI-Einordnung des Tages...")
        interpretation = generate_interpretation(STRATEGY_NAME, summary)
        if interpretation:
            print(f"Einordnung: {interpretation}")
            email_body += f"\n\n{'=' * 50}\nKI-EINORDNUNG DES TAGES\n{'=' * 50}\n{interpretation}"
        else:
            print("(Keine Einordnung erhalten - API-Key gesetzt? Siehe shared/claude_client.py)")

    if USE_MARKET_CONTEXT_AGENT and not open_trades.empty:
        print("\nHole Marktkontext fuer offene Positionen...")
        symbols_with_positions = open_trades["symbol"].unique().tolist()
        context = get_market_context(symbols_with_positions, context_label=STRATEGY_NAME)
        if context:
            print(f"Marktkontext: {context}")
            email_body += f"\n\n{'=' * 50}\nMARKTKONTEXT (offene Positionen)\n{'=' * 50}\n{context}"
        else:
            print("(Kein Marktkontext erhalten - API-Key gesetzt? Siehe shared/claude_client.py)")

    try:
        send_email(f"Trading Bot [{STRATEGY_NAME}] - Taegliche Uebersicht", email_body)
        print("\nE-Mail erfolgreich verschickt.")
    except Exception as e:
        print(f"\nFehler beim E-Mail-Versand: {e}")
        print("Pruefe deine Angaben in email_config.py.")
