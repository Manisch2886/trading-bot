"""
Vierteljaehrliches Strategie-Review - T3/ADX/SuperTrend (Krypto)
======================================================================
Automatisierter, aber bewusst NICHT selbst-aendernder Review-Prozess:

1. Agent 2 sucht eine neue, potenziell bessere Parameter-Kombination
   (dieselbe Logik wie agent_optimise.py)
2. Sowohl die AKTUELLE (live_params.py) als auch die NEU gefundene
   Kombination werden per Walk-Forward-Analyse verglichen
   (In-Sample vs. Out-of-Sample) - fairer Vergleich, keine Bevorzugung
3. Die ECHTEN, bisher aufgelaufenen Forward-Test-Ergebnisse (aus der
   Datenbank) werden als unabhaengige Realitaets-Pruefung gegenueber-
   gestellt - das ist die wertvollste Kontrolle, da diese Trades
   garantiert nicht ueberoptimiert sein koennen (sie sind bereits
   passiert, bevor dieser Bericht existierte)
4. Ein Bericht wird per E-Mail verschickt.

WICHTIG: Es wird NIEMALS automatisch etwas an live_params.py geaendert.
Eine Uebernahme des Vorschlags bleibt immer ein bewusster, manueller
Schritt.

Gedacht fuer einen VIERTELJAEHRLICHEN Cronjob (nicht monatlich - siehe
Begruendung: der Forward-Test braucht Zeit, um genug echte Trades fuer
einen aussagekraeftigen Realdaten-Abgleich zu sammeln).
"""

import os
import sys
import smtplib
import sqlite3
from datetime import datetime
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

_NOTIF_DIR = os.path.join(_P["BASE_DIR"], "notifications")
sys.path.insert(0, _NOTIF_DIR)
from notify import send_report

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

from param_search_agent import run_agent_search
from quarterly_interpreter import generate_recommendation
from multi_symbol_optimise import load_all_symbol_data, evaluate_combination_multi
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from live_params import T3_FAST_LENGTH, T3_SLOW_LENGTH, ADX_THRESHOLD, STOP_LOSS_PCT

CURRENT_PARAMS = {
    "t3_fast": T3_FAST_LENGTH,
    "t3_slow": T3_SLOW_LENGTH,
    "adx_threshold": ADX_THRESHOLD,
    "stop_loss_pct": STOP_LOSS_PCT,
}

PARAM_SPEC = {
    "t3_fast": {"type": "int", "range": [8, 16], "step": 4},
    "t3_slow": {"type": "int", "range": [21, 30], "step": 4},
    "adx_threshold": {"type": "float", "range": [20.0, 30.0], "step": 5.0},
    "stop_loss_pct": {"type": "float", "range": [2.0, 4.0], "step": 1.0},
}


def evaluate_params(all_data: dict, params: dict):
    return evaluate_combination_multi(
        all_data,
        t3_fast=int(params["t3_fast"]),
        t3_slow=int(params["t3_slow"]),
        adx_threshold=params["adx_threshold"],
        stop_loss_pct=params["stop_loss_pct"],
    )


def walk_forward_for_params(all_data: dict, params: dict) -> dict:
    """Testet eine SPEZIFISCHE Parameter-Kombination getrennt auf
    In-Sample- und Out-of-Sample-Zeitraum (kein Suchen, nur Bewerten -
    fuer einen fairen Vergleich zwischen aktuellen und neuen Parametern)."""
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)
    return {
        "in_sample": evaluate_params(train_data, params),
        "out_of_sample": evaluate_params(test_data, params),
    }


def get_real_trade_stats() -> dict:
    """Liest die tatsaechlich aufgelaufenen Forward-Test-Ergebnisse aus
    der Datenbank - unabhaengige Realitaets-Pruefung, kann nicht
    ueberoptimiert sein, da diese Trades bereits in der Vergangenheit
    liegen."""
    conn = sqlite3.connect(DB_FILE)
    closed_trades = pd.read_sql("SELECT * FROM trades WHERE status='closed'", conn)
    conn.close()

    if closed_trades.empty:
        return {"num_trades": 0}

    return {
        "num_trades": len(closed_trades),
        "win_rate": round((closed_trades["pnl_pct"] > 0).mean() * 100, 1),
        "avg_pnl": round(closed_trades["pnl_pct"].mean(), 2),
        "total_pnl": round(closed_trades["pnl_pct"].sum(), 2),
    }


def format_wf_result(label: str, wf: dict) -> str:
    lines = [f"{label}:"]
    for period in ("in_sample", "out_of_sample"):
        r = wf.get(period)
        period_label = "In-Sample" if period == "in_sample" else "Out-of-Sample"
        if r is None:
            lines.append(f"  {period_label}: Mindestkriterien nicht erfuellt (zu wenige Trades)")
        else:
            lines.append(f"  {period_label}: {r['num_trades']} Trades, {r['win_rate']}% Win Rate, "
                          f"Ø {r['avg_return_pct']}% PnL, Score {r['robustness_score']}")
    return "\n".join(lines)


def build_report(current_wf: dict, proposed_params: dict, proposed_wf: dict, real_stats: dict,
                  recommendation: str = "") -> str:
    lines = []
    lines.append(f"Vierteljaehrliches Strategie-Review [{STRATEGY_NAME}]")
    lines.append(f"{datetime.utcnow().strftime('%d.%m.%Y %H:%M')} UTC")
    lines.append("=" * 60)
    lines.append("")

    lines.append("AKTUELLE LIVE-PARAMETER:")
    lines.append(f"  {CURRENT_PARAMS}")
    lines.append("")
    lines.append(format_wf_result("Walk-Forward (aktuelle Parameter)", current_wf))
    lines.append("")

    lines.append("-" * 60)
    lines.append("")

    if proposed_params is None:
        lines.append("AGENT-VORSCHLAG: nicht verfuegbar (API-Fehler oder kein Key gesetzt)")
    else:
        lines.append("VON AGENT 2 VORGESCHLAGENE NEUE PARAMETER:")
        lines.append(f"  {proposed_params}")
        lines.append("")
        lines.append(format_wf_result("Walk-Forward (vorgeschlagene Parameter)", proposed_wf))

    lines.append("")
    lines.append("-" * 60)
    lines.append("")
    lines.append("ECHTE FORWARD-TEST-ERGEBNISSE (seit Start, unabhaengige Realitaets-Pruefung):")
    if real_stats["num_trades"] == 0:
        lines.append("  Noch keine geschlossenen Trades.")
    else:
        lines.append(f"  {real_stats['num_trades']} Trades, {real_stats['win_rate']}% Win Rate, "
                      f"Ø {real_stats['avg_pnl']}% PnL, Summe {real_stats['total_pnl']}%")

    if recommendation:
        lines.append("")
        lines.append("-" * 60)
        lines.append("")
        lines.append("KI-EMPFEHLUNG:")
        lines.append(recommendation)

    lines.append("")
    lines.append("=" * 60)
    lines.append("WICHTIG: Es wurde NICHTS automatisch geaendert.")
    lines.append(f"Falls du die neuen Parameter uebernehmen moechtest, bearbeite manuell:")
    lines.append(f"  strategies/{STRATEGY_NAME}/live_params.py")
    lines.append("=" * 60)

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
    print(f"Vierteljaehrliches Review [{STRATEGY_NAME}] - {datetime.utcnow().isoformat()}\n")

    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden. Abbruch.")
        exit()

    print("Validiere aktuelle Live-Parameter per Walk-Forward...")
    current_wf = walk_forward_for_params(all_data, CURRENT_PARAMS)
    print(format_wf_result("Aktuelle Parameter", current_wf))

    print("\nStarte Agent-2-Suche nach besserer Kombination...")
    seed_combos = [CURRENT_PARAMS]
    search_result = run_agent_search(
        lambda p: evaluate_params(all_data, p), PARAM_SPEC, seed_combos=seed_combos, max_iterations=10,
    )

    proposed_params = None
    proposed_wf = None
    if search_result["best"]:
        best = search_result["best"]
        proposed_params = {k: best[k] for k in CURRENT_PARAMS.keys()}
        print(f"\nAgent-Vorschlag: {proposed_params}")
        print("Validiere Vorschlag per Walk-Forward...")
        proposed_wf = walk_forward_for_params(all_data, proposed_params)
        print(format_wf_result("Vorgeschlagene Parameter", proposed_wf))

    print("\nLese echte Forward-Test-Ergebnisse aus der Datenbank...")
    real_stats = get_real_trade_stats()
    print(f"  {real_stats}")

    print("\nHole KI-Empfehlung...")
    recommendation = generate_recommendation(
        STRATEGY_NAME, CURRENT_PARAMS, current_wf, proposed_params, proposed_wf, real_stats,
    )
    if recommendation:
        print(f"Empfehlung: {recommendation}")
    else:
        print("(Keine Empfehlung erhalten - API-Key gesetzt?)")

    report = build_report(current_wf, proposed_params, proposed_wf, real_stats, recommendation)
    print("\n" + report)

    subject = f"Quartals-Review [{STRATEGY_NAME}] - Parameter-Vorschlag"
    try:
        if SEND_VIA_EMAIL:
            send_email(subject, report)
            print("\nE-Mail erfolgreich verschickt.")
        elif send_report(subject, report):
            print("\nTelegram-Nachricht(en) erfolgreich verschickt.")
        else:
            print("\nTelegram-Versand fehlgeschlagen - siehe Log/Fehlermeldung von notify.py.")
    except Exception as e:
        print(f"\nFehler beim Versand: {e}")
