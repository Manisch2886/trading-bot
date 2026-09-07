"""
Bot-Umgebung fuer die 2025er-P&L-Auswertung
====================================================================
Setzt sys.path auf EINEN der neun Bots und legt Stubs fuer die Module
an, die in dieser Umgebung nicht installiert sind bzw. Zugangsdaten
enthalten (CLAUDE.md: config/email_config.py und
shared/fetch_binance_data.py sind bewusst nicht im Repo).

Die Stubs werden nie aufgerufen - gelesen werden ausschliesslich die
lokalen CSVs in data/. Damit das nicht nur behauptet ist, wirft jede
Stub-Funktion beim Aufruf eine AssertionError.

WICHTIG - ein Prozess je Bot: mehrere Bots haben gleichnamige,
inhaltlich verschiedene Module (`equity_simulation.py`,
`multi_symbol_optimise.py`, `indicators.py`, ...). Ein Import zweier
Bots im selben Prozess wuerde ueber sys.modules still den falschen
laden. Alle Skripte hier nehmen den Botnamen als Argument und werden
von run_all.py je einmal als eigener Prozess gestartet.
"""

import os
import sys
import types

DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(DIR))
RESULTS_DIR = os.path.join(DIR, "results")


def _boom(*_a, **_kw):
    raise AssertionError("Stub aufgerufen - dieses Skript darf nur lokale CSVs lesen.")


def setup(bot: str):
    """Bereitet den Prozess fuer genau einen Bot vor. Muss VOR jedem
    Import von Bot-Modulen laufen."""
    bot_dir = os.path.join(REPO_ROOT, "strategies", bot)
    if not os.path.isdir(bot_dir):
        raise SystemExit(f"Unbekannter Bot: {bot!r}")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    sys.path.insert(0, DIR)
    sys.path.insert(0, bot_dir)
    sys.path.insert(0, os.path.join(REPO_ROOT, "shared"))

    for name in ("fetch_binance_data", "fetch_stock_data", "yfinance",
                  "email_config", "notify", "anthropic"):
        mod = types.ModuleType(name)
        mod.INTERVAL = "1h" if bot == "elliott_wave" else "1d"
        for attr in ("fetch_historical_data", "download", "Ticker", "send_report"):
            setattr(mod, attr, _boom)
        sys.modules.setdefault(name, mod)

    binance = types.ModuleType("binance")
    client = types.ModuleType("binance.client")

    class _FakeClient:
        KLINE_INTERVAL_1HOUR = "1h"
        KLINE_INTERVAL_4HOUR = "4h"
        KLINE_INTERVAL_1DAY = "1d"

    client.Client = _FakeClient
    binance.client = client
    sys.modules.setdefault("binance", binance)
    sys.modules.setdefault("binance.client", client)
    return bot
