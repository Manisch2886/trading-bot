"""
Ein Bot, ein Prozess: die Ergebniskurve so erzeugen, wie der Bot sie erzeugt
==============================================================================
Hilfsprogramm von `shared/ergebniskurven.py`. Es wird nicht von Hand
aufgerufen, sondern je Bot als eigener Prozess gestartet:

    python3 shared/kurven_lauf.py <bot_name> <ziel_ordner>

Es fuehrt den `__main__`-Block von `strategies/<bot>/equity_simulation.py`
unveraendert aus und schreibt dessen `equity_curve.csv` nach `<ziel_ordner>`.

WARUM DER __main__-BLOCK UND NICHT DIE EINZELNEN FUNKTIONEN
------------------------------------------------------------------------------
`research/exposure_messung/bot_lauf.py` ruft `collect_all_trades()` je Bot mit
einer eigenen, dort hinterlegten Argumentliste auf. Das funktioniert, fuehrt
aber eine zweite Fassung der Frage "womit rechnet dieser Bot eigentlich"
ein - genau die Doppelfuehrung, an der dieses Projekt schon mehrfach
auseinandergelaufen ist (Protokoll 4.2 und Prinzip 7.11).

Der konkrete Beleg liegt bei `volatility_breakout_crypto`: dessen
BTC-Regimefilter wird bewusst **an der Aufrufstelle im `__main__`-Block**
angewendet und nicht in `collect_all_trades()` (PR #57, ausfuehrlich in der
dortigen Commit-Nachricht begruendet). Wer die Funktionen einzeln aufruft,
muss diesen Filter von Hand nachbilden - vergisst er ihn, rechnet er still
eine andere Strategie. Genau dieser Fehler hat den HRP-Bericht zweimal
gekippt.

Deshalb wird hier `runpy.run_path(..., run_name="__main__")` benutzt: die
Argumentzuordnung steht damit an genau **einer** Stelle, naemlich in der
Datei des Bots selbst.

WOHIN GESCHRIEBEN WIRD
------------------------------------------------------------------------------
`RESULTS_DIR` wird fuer die Dauer des Laufs auf `<ziel_ordner>` umgelenkt.
Das ist kein Komfort, sondern die Absicherung: dieses Programm kann
`results/` gar nicht ueberschreiben, auch nicht versehentlich. Ob eine
erzeugte Kurve die abgelegte ersetzt, entscheidet ausschliesslich
`ergebniskurven.py` - und nur bei ausdruecklichem `--erzeugen`.

Umgelenkt wird ueber ein Ersatzmodul `strategy_paths` in `sys.modules`, das
die echte Funktion aufruft und nur `RESULTS_DIR` austauscht. Die uebrigen
Pfade (DATA_DIR, CONFIG_DIR, DB_FILE) bleiben die echten - der Lauf soll
dieselben Kursdaten und dieselbe Konfiguration sehen wie der Bot.

WAS NICHT GELESEN WIRD
------------------------------------------------------------------------------
Die Bot-Datenbanken. Diese Kurve ist eine Backtest-Kurve; sie entsteht
ausschliesslich aus `data/` und den Strategie-Dateien. `forward_test.py`
wird nie importiert.

Unvollstaendige Kursbalken haelt `shared/kursdaten.py` fern - nicht von hier
aus, sondern dort, wo die Daten ins Programm kommen: alle neun
`multi_symbol_optimise.load_all_symbol_data()` rufen seit PR #81
`entferne_unvollstaendige()` auf, und `load_all_symbol_data()` ist der Weg,
ueber den jeder `__main__`-Block seine Daten holt. Eine zweite Filterung
hier waere eine zweite Wahrheit ueber dieselben Daten.

STUBS
------------------------------------------------------------------------------
Uebernommen aus `research/exposure_messung/bot_lauf.py` bzw.
`research/order_sensitivity/run_one_bot.py`: `shared/fetch_binance_data.py`
enthaelt Zugangsdaten und ist gitignored, `yfinance` und `python-binance`
sind nicht ueberall installiert. Gelesen werden ausschliesslich die bereits
vorhandenen CSVs unter `data/` - die Stubs wuerden, wenn sie je aufgerufen
wuerden, einen leeren DataFrame liefern und damit auffallen, statt still
Netzdaten nachzuladen.
"""

import json
import os
import runpy
import sys
import types

import pandas as pd

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)

# Markiert die Meldezeile an das aufrufende Programm. Eigener Praefix statt
# "die letzte Zeile nehmen": der __main__-Block des Bots gibt selbst reichlich
# aus, und die letzte Zeile ist dort der Speicherpfad.
META_PREFIX = "__KURVEN_META__ "


def _stubs_setzen():
    """Module, die in diesem Lauf nie gebraucht werden, aber importiert
    wuerden. `setdefault` statt Zuweisung: ist das echte Modul vorhanden,
    gewinnt es."""
    fake_fetch = types.ModuleType("fetch_binance_data")
    fake_fetch.fetch_historical_data = lambda *a, **kw: pd.DataFrame()
    sys.modules.setdefault("fetch_binance_data", fake_fetch)

    fake_binance = types.ModuleType("binance")
    fake_client = types.ModuleType("binance.client")

    class _FakeClient:
        KLINE_INTERVAL_1HOUR = "1h"
        KLINE_INTERVAL_4HOUR = "4h"
        KLINE_INTERVAL_1DAY = "1d"

    fake_client.Client = _FakeClient
    fake_binance.client = fake_client
    sys.modules.setdefault("binance", fake_binance)
    sys.modules.setdefault("binance.client", fake_client)

    fake_yf = types.ModuleType("yfinance")
    fake_yf.download = lambda *a, **kw: pd.DataFrame()
    fake_yf.Ticker = lambda *a, **kw: None
    sys.modules.setdefault("yfinance", fake_yf)


def _results_dir_umlenken(ziel: str):
    """Ersetzt `strategy_paths` durch eine Fassung, die alles an die echte
    Funktion weiterreicht und nur RESULTS_DIR austauscht."""
    import strategy_paths as echt

    ersatz = types.ModuleType("strategy_paths")
    ersatz.__doc__ = echt.__doc__
    ersatz._ECHT = echt

    def get_strategy_paths(caller_file):
        pfade = echt.get_strategy_paths(caller_file)
        pfade["RESULTS_DIR"] = ziel
        os.makedirs(ziel, exist_ok=True)
        return pfade

    ersatz.get_strategy_paths = get_strategy_paths
    sys.modules["strategy_paths"] = ersatz


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Aufruf: python3 shared/kurven_lauf.py <bot_name> <ziel_ordner>")

    bot = sys.argv[1]
    ziel = os.path.abspath(sys.argv[2])
    strategie_dir = os.path.join(BASE_DIR, "strategies", bot)
    skript = os.path.join(strategie_dir, "equity_simulation.py")
    if not os.path.exists(skript):
        raise SystemExit(f"{bot}: {skript} nicht gefunden.")

    sys.path.insert(0, strategie_dir)
    sys.path.insert(0, _SHARED_DIR)
    _stubs_setzen()
    _results_dir_umlenken(ziel)

    # Der __main__-Block einiger Bots ruft exit() auf, wenn keine Daten oder
    # keine Trades gefunden werden - das ist ein SystemExit und soll hier als
    # Fehlschlag durchschlagen, nicht als leere Kurve.
    os.chdir(strategie_dir)
    globalen = runpy.run_path(skript, run_name="__main__")

    kurve = os.path.join(ziel, "equity_curve.csv")
    if not os.path.exists(kurve):
        raise SystemExit(f"{bot}: der Lauf hat keine equity_curve.csv geschrieben.")

    df = pd.read_csv(kurve)

    # Die Kennzahlen stammen aus dem Lauf selbst, nicht aus einer zweiten
    # Rechnung hier: `runpy.run_path` gibt die Namensraum-Werte des
    # ausgefuehrten Blocks zurueck. Fehlt einer (elliott_wave hat kein
    # MAX_CONCURRENT_POSITIONS), bleibt er None statt erfunden zu werden.
    ergebnis = globalen.get("result") or {}
    meta = {
        "bot": bot,
        "kurve": kurve,
        "zeilen": int(len(df)),
        "startkapital": globalen.get("STARTING_CAPITAL"),
        "allocation_pct": globalen.get("ALLOCATION_PCT"),
        "max_concurrent_positions": globalen.get("MAX_CONCURRENT_POSITIONS"),
        "trades_gefunden": int(len(globalen["trades"])) if "trades" in globalen else None,
        "trades_ausgefuehrt": ergebnis.get("num_executed"),
        "trades_uebersprungen": ergebnis.get("num_skipped"),
        "endkapital": ergebnis.get("final_capital"),
        "max_drawdown_pct": globalen.get("max_dd"),
    }
    print(META_PREFIX + json.dumps(meta, default=str))


if __name__ == "__main__":
    main()
