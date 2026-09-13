"""
Bot-Umgebung fuer TB-25 (Fib-Score-Stufen)
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

Der Aufbau ist woertlich der von research/elliott_wave_params/botenv.py
bzw. research/drawdown_reihenfolge/botenv.py - beide Untersuchungen
fuehren dieselbe Datei je einmal mit. Das ist im Projekt die etablierte
Form; eine gemeinsame Kopie ueber Ordnergrenzen hinweg wuerde eine
abgeschlossene Untersuchung nachtraeglich von einer spaeteren abhaengig
machen.

ZUM UMGANG MIT BOT-CODE (Auftrag, Randbedingungen): Bot-Dateien werden
hier ausschliesslich GELESEN. Sie werden als Bibliothek eingebunden
(`import backtest_elliott`), nie als Programm ausgefuehrt - der
`__main__`-Block, der Dateien unter results/ ueberschreiben wuerde,
laeuft dabei nicht.
"""

import os
import sys
import types

DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(DIR))
RESULTS_DIR = os.path.join(DIR, "results")

BOTS = ("elliott_wave", "elliott_wave_stocks")

# --------------------------------------------------------------------
# Fester Hinweis - steht in jeder Ausgabe und in jeder Ergebnisdatei
# --------------------------------------------------------------------
# TB-25 ist eine Untersuchung, keine Aenderung. Damit daraus nicht
# unbemerkt eine Parametrisierung wird, traegt jede Ausgabe denselben
# Hinweis - in der Konsole und in jeder JSON-Datei (Schluessel
# "hinweis"). Konvention aus research/elliott_wave_params/botenv.py.
UNTERSUCHUNG_HINWEIS = (
    "TB-25 IST EINE MESSUNG, KEINE EMPFEHLUNG UND KEINE AENDERUNG. "
    "Es wurde NICHTS am Bot-Code geaendert - live_params.py, "
    "forward_test.py, elliott_wave_counter.py und zigzag_indicator.py "
    "bleiben unangetastet. Was aus dem Ergebnis folgt (Schwelle, "
    "Auswahlregel, Fortbestand des Bots), entscheidet der Nutzer."
)


def print_hinweis():
    line = "!" * 70
    print(line)
    for chunk in _wrap(UNTERSUCHUNG_HINWEIS, 68):
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
