"""
Bot-Umgebung fuer die Parameter-Neubestimmung
====================================================================
Setzt sys.path auf EINEN der beiden Elliott-Wave-Bots und legt Stubs
fuer die Module an, die in dieser Umgebung nicht installiert sind bzw.
Zugangsdaten enthalten (CLAUDE.md: config/email_config.py und
shared/fetch_binance_data.py sind bewusst nicht im Repo).

Die Stubs werden NIE aufgerufen - gelesen werden ausschliesslich die
lokalen CSVs in data/. Damit das nicht nur behauptet ist, wirft jede
Stub-Funktion beim Aufruf eine AssertionError.

WICHTIG - ein Prozess je Bot: beide Bots haben gleichnamige, inhaltlich
verschiedene Module (`backtest_elliott.py`, `zigzag_indicator.py`, ...).
Ein Import beider im selben Prozess wuerde ueber sys.modules still den
falschen Bot laden. Alle Skripte hier nehmen den Botnamen als Argument
und werden von run_all.py je einmal als eigener Prozess gestartet.
"""

import os
import sys
import types

import pandas as pd

DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(DIR))
RESULTS_DIR = os.path.join(DIR, "results")
CACHE_DIR = os.path.join(RESULTS_DIR, "_cache")

BOTS = ("elliott_wave", "elliott_wave_stocks")

# --------------------------------------------------------------------
# Fester Hinweis - steht in jeder Ausgabe und in jeder Ergebnisdatei
# --------------------------------------------------------------------
# Diese Untersuchung ist die erste im Projekt, die tatsaechlich nach
# neuen Parametern sucht. Damit daraus nicht unbemerkt eine
# Aktivierung wird, traegt jede Ausgabe denselben Hinweis - in der
# Konsole, in jeder JSON-Datei (Schluessel "hinweis") und im Bericht.
# Er folgt der Konvention aus quarterly_review.py ("Es wurde NICHTS
# automatisch geaendert") und ist bewusst nicht abschaltbar.
UNVALIDIERT_HINWEIS = (
    "ALLE HIER GENANNTEN PARAMETER SIND UNVALIDIERTE VORSCHLAEGE. "
    "Es wurde NICHTS automatisch geaendert - live_params.py und "
    "forward_test.py bleiben unangetastet. Eine Uebernahme erfolgt "
    "ausschliesslich manuell und erst nach eigener Pruefung und "
    "ausdruecklicher Zustimmung des Auftraggebers."
)


def print_hinweis():
    """Wird von jedem Skript am Anfang und am Ende ausgegeben."""
    line = "!" * 70
    print(line)
    for chunk in _wrap(UNVALIDIERT_HINWEIS, 68):
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


def setup(bot: str):
    """Bereitet den Prozess fuer genau einen Bot vor. Muss VOR jedem
    Import von Bot-Modulen laufen."""
    if bot not in BOTS:
        raise SystemExit(f"Unbekannter Bot: {bot!r} - erlaubt: {BOTS}")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    sys.path.insert(0, DIR)
    sys.path.insert(0, os.path.join(REPO_ROOT, "strategies", bot))
    sys.path.insert(0, os.path.join(REPO_ROOT, "shared"))

    for name in ("fetch_binance_data", "fetch_stock_data", "yfinance"):
        mod = types.ModuleType(name)
        mod.INTERVAL = "1h" if bot == "elliott_wave" else "1d"
        mod.fetch_historical_data = _boom
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
        raise SystemExit(f"Nutzung: python3 {os.path.basename(sys.argv[0])} <{'|'.join(BOTS)}>")
    return setup(sys.argv[1])
