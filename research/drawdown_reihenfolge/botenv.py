"""
Bot-Umgebung fuer die Untersuchung der Drawdown-Reihenfolge
====================================================================
Setzt sys.path auf GENAU EINEN der neun Bots und legt Stubs fuer die
Module an, die in dieser Umgebung nicht vorhanden sind bzw.
Zugangsdaten enthalten (CLAUDE.md: config/email_config.py und
shared/fetch_binance_data.py liegen bewusst nicht im Repo).

Die Stubs werden NIE aufgerufen - gelesen werden ausschliesslich die
lokalen CSVs in data/. Damit das nicht nur behauptet ist, wirft jede
Stub-Funktion beim Aufruf eine AssertionError.

WICHTIG - ein Prozess je Bot: die neun Bots haben gleichnamige,
inhaltlich verschiedene Module (`backtest_elliott.py`,
`backtest_rsi2.py`, `multi_symbol_optimise.py`, ...). Ein Import
zweier Bots im selben Prozess wuerde ueber sys.modules still den
falschen Bot laden. Alle Skripte hier nehmen den Botnamen als
Argument und werden von run_all.py je einmal als eigener Prozess
gestartet.

ZUM UMGANG MIT BOT-CODE (Auftrag, Randbedingungen): Bot-Dateien
werden hier ausschliesslich GELESEN. Sie werden als Bibliothek
eingebunden (`import multi_symbol_optimise`), nie als Programm
ausgefuehrt - der `__main__`-Block, der
results/<bot>/multi_symbol_optimisation_results.csv ueberschreiben
wuerde, laeuft dabei nicht. Genau das ist der Grund fuer diese
Trennung: die historischen Ergebnisdateien sind hier Beweismittel
(Frage 2) und muessen unangetastet bleiben. Dass dieser Ordner
keinen Bot-Code und keine Ergebnisdatei veraendert, weist
test_drawdown.py per `git status` nach.
"""

import os
import sys
import types

DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(DIR))
RESULTS_DIR = os.path.join(DIR, "results")

# Reihenfolge wie in CLAUDE.md (Krypto zuerst, dann Aktien)
BOTS = (
    "elliott_wave",
    "t3_supertrend",
    "rsi2_crypto",
    "turtle_soup_crypto",
    "volatility_breakout_crypto",
    "elliott_wave_stocks",
    "rsi2_mean_reversion",
    "turtle_soup_stocks",
    "volatility_breakout",
)

KRYPTO = {"elliott_wave", "t3_supertrend", "rsi2_crypto",
          "turtle_soup_crypto", "volatility_breakout_crypto"}

# Kerzen-Intervall der jeweiligen Bot-CSV-Dateien in data/.
INTERVAL = {
    "elliott_wave": "1h",
    "t3_supertrend": "4h",
    "rsi2_crypto": "1d",
    "turtle_soup_crypto": "1d",
    "volatility_breakout_crypto": "1d",
    "elliott_wave_stocks": "1d",
    "rsi2_mean_reversion": "1d",
    "turtle_soup_stocks": "1d",
    "volatility_breakout": "1d",
}

HINWEIS = (
    "DIES IST EINE UNTERSUCHUNG, KEINE KORREKTUR. Es wurde NICHTS "
    "geaendert - kein live_params.py, kein forward_test.py, kein "
    "equity_simulation.py, kein multi_symbol_optimise.py und keine "
    "Ergebnisdatei eines Bots. Ob aus den hier gezeigten Zahlen eine "
    "Aenderung folgt, entscheidet der Nutzer."
)


def print_hinweis():
    line = "!" * 70
    print(line)
    for chunk in _wrap(HINWEIS, 68):
        print(chunk)
    print(line)


def _wrap(text: str, width: int) -> list:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def _boom(*_a, **_kw):
    raise AssertionError("Stub aufgerufen - dieses Skript darf nur lokale CSVs lesen.")


def setup(bot: str) -> str:
    """Bereitet den Prozess fuer genau einen Bot vor. Muss VOR jedem
    Import von Bot-Modulen laufen."""
    if bot not in BOTS:
        raise SystemExit(f"Unbekannter Bot: {bot!r} - erlaubt: {', '.join(BOTS)}")

    os.makedirs(RESULTS_DIR, exist_ok=True)

    sys.path.insert(0, DIR)
    sys.path.insert(0, os.path.join(REPO_ROOT, "strategies", bot))
    sys.path.insert(0, os.path.join(REPO_ROOT, "shared"))

    for name in ("fetch_binance_data", "fetch_stock_data", "fetch_multi_data",
                 "fetch_4h_data", "yfinance"):
        mod = types.ModuleType(name)
        mod.INTERVAL = INTERVAL[bot]
        mod.fetch_historical_data = _boom
        mod.fetch_all_symbols = _boom
        mod.download = _boom
        mod.Ticker = _boom
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


def bot_from_argv() -> str:
    if len(sys.argv) < 2:
        raise SystemExit(f"Nutzung: python3 {os.path.basename(sys.argv[0])} <bot>\n"
                         f"Bots: {', '.join(BOTS)}")
    return setup(sys.argv[1])
