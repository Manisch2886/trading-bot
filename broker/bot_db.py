"""
Der EINE lesende Zugang zu einer Bot-Datenbank
==============================================================================
Beide Broker-Bruecken (Binance-Testnet und IBKR-Paper) lesen denselben
Datenbestand auf dieselbe Weise: schreibgeschuetzt. Diese Datei ist deshalb die
einzige Stelle im Projekt, die eine `paper_trading_*.db` oeffnet, um sie zu
spiegeln - eine zweite Fassung waere die Doppelfuehrung, bei der irgendwann nur
noch eine der beiden Bruecken wirklich nur liest.

`mode=ro` ist kein Vorsatz, den ein spaeterer Fehler brechen koennte: SQLite
verweigert in diesem Modus JEDEN Schreibversuch, auch einen versehentlichen.
"""

import os
import sqlite3


class BotDbFehler(Exception):
    """Die Datenbank des Bots ist nicht lesbar. Es wurde nichts gesendet."""


def pfad(bot: str, base_dir: str) -> str:
    """Dieselbe Namensregel wie shared/strategy_paths.py - hier nachgebildet
    statt importiert, weil get_strategy_paths() Verzeichnisse ANLEGT und eine
    Datei innerhalb von strategies/ als Aufrufer erwartet. Eine Bruecke soll
    beim blossen Nachsehen nichts anlegen."""
    return os.path.join(base_dir, f"paper_trading_{bot}.db")


def lies_trades(bot: str, base_dir: str) -> list:
    """Alle Trades des Bots, schreibgeschuetzt gelesen."""
    datei = pfad(bot, base_dir)
    if not os.path.exists(datei):
        raise BotDbFehler(
            f"Die Datenbank des Bots fehlt: {datei}. Laeuft {bot} auf dieser "
            f"Maschine? Es wurde nichts gesendet.")
    conn = sqlite3.connect(f"file:{datei}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        zeilen = conn.execute(
            "SELECT id, symbol, entry_time, entry_price, exit_time, exit_price, "
            "result, pnl_pct, status FROM trades ORDER BY id").fetchall()
    finally:
        conn.close()
    return [dict(z) for z in zeilen]
