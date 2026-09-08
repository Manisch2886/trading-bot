"""
Warum werden Trades uebersprungen - Limit oder Kapital?
================================================================================
`equity_simulation.py` des Aktien-Elliott-Bots meldete jahrelang
"Uebersprungene Trades: N (nicht genug freies Kapital)". `simulate_portfolio()`
kennt aber ZWEI Abbruchgruende und wirft beide in dieselbe Liste:

    1. MAX_CONCURRENT_POSITIONS erreicht
    2. freies Kapital reicht fuer die Allokation nicht

Zurueck kommt nur `num_skipped` - die Aufschluesselung ist von der Aufrufstelle
aus gar nicht zu bekommen. Die Ausgabezeile nennt seit dieser Aenderung deshalb
beide Gruende (gleicher Wortlaut wie in `oos_equity_simulation.py`, PR #48).

Dieses Skript beantwortet die Frage, die dahinter steht: WELCHER der beiden
Gruende greift eigentlich? Ergebnis am 2026-09-08: alle 115 uebersprungenen
Trades gehen auf das Positionslimit zurueck, KEINER auf fehlendes Kapital. Der
alte Klammerzusatz war also nicht bloss ungenau, sondern nannte ausgerechnet
den Grund, der nie zutraf.

Das ist kein Zufall: bei ALLOCATION_PCT = 10 % und hoechstens 8 gleichzeitigen
Positionen sind nie mehr als rund 80 % des Kapitals gebunden - das Limit greift
praktisch immer zuerst.

Dass der zweite Zaehler deshalb nicht bloss tot ist, zeigt eine Gegenprobe mit
zaehle_getrennt() bei anderen Limits (derselbe Datenstand):

    Limit    8:  ausgefuehrt 395   wegen Limit 115   wegen Kapital   0
    Limit   20:  ausgefuehrt 425   wegen Limit   0   wegen Kapital  85
    Limit None:  ausgefuehrt 425   wegen Limit   0   wegen Kapital  85

Ohne Limit scheitern also sehr wohl 85 Trades am Kapital - beim Live-Wert 8
kommt es dazu nur nie, weil vorher das Limit greift. Ohne diese Gegenprobe
waere "0 wegen Kapital" auch mit einem kaputten Zaehler zu bekommen gewesen.

METHODE: der Bot wird NICHT veraendert. Die Ereignisschleife aus
simulate_portfolio() ist hier nachgebaut, nur mit zwei getrennten Zaehlern
statt einer gemeinsamen Liste. Damit der Nachbau nicht heimlich etwas anderes
misst, muessen seine Summen die des Originals exakt treffen - genau das prueft
der Schluss des Skripts, und ohne diese Uebereinstimmung ist das Ergebnis
wertlos.

Rein lesend. Kursdaten aus data/, Ergebnisse landen in einem temporaeren
Verzeichnis.

Nutzung:  python3 research/uebersprungene_trades/aufschluesselung.py
"""

import importlib.util
import os
import sys
import tempfile

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
BOT = os.path.join(_REPO_ROOT, "strategies", "elliott_wave_stocks")
STUBS = os.path.join(_REPO_ROOT, "research", "forward_test_sync", "stubs")

sys.path.insert(0, BOT)
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))
sys.path.append(STUBS)   # yfinance-Attrappe: wirft bei echtem Abruf

_TEMP = tempfile.mkdtemp(prefix="aufschluesselung_")

import strategy_paths  # noqa: E402

_echt = strategy_paths.get_strategy_paths


def _umgeleitet(caller_file):
    """Ergebnisse ins temporaere Verzeichnis - der Lauf darf results/ des
    Bots nicht anfassen."""
    p = dict(_echt(caller_file))
    p["RESULTS_DIR"] = os.path.join(_TEMP, "results")
    p["LOGS_DIR"] = os.path.join(_TEMP, "logs")
    os.makedirs(p["RESULTS_DIR"], exist_ok=True)
    os.makedirs(p["LOGS_DIR"], exist_ok=True)
    return p


strategy_paths.get_strategy_paths = _umgeleitet


def lade_bot_modul():
    """equity_simulation.py als Modul laden, ohne seinen __main__-Zweig."""
    spec = importlib.util.spec_from_file_location(
        "equity_simulation_messung", os.path.join(BOT, "equity_simulation.py"))
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def zaehle_getrennt(es, trades):
    """Nachbau der Ereignisschleife aus simulate_portfolio() mit zwei
    getrennten Zaehlern. Bewusst Zeile fuer Zeile dieselbe Logik - jede
    Abweichung wuerde die Summenpruefung unten reissen."""
    ereignisse = []
    for idx, t in trades.iterrows():
        ereignisse.append((t["entry_time"], "entry", idx))
        ereignisse.append((t["exit_time"], "exit", idx))
    ereignisse.sort(key=lambda e: (e[0], e[1] != "exit"))

    kapital = es.STARTING_CAPITAL
    offen = {}
    wegen_limit = wegen_kapital = ausgefuehrt = 0

    for _zeit, art, idx in ereignisse:
        t = trades.loc[idx]
        if art == "entry":
            if (es.MAX_CONCURRENT_POSITIONS is not None
                    and len(offen) >= es.MAX_CONCURRENT_POSITIONS):
                wegen_limit += 1
                continue
            frei = kapital - sum(offen.values())
            anteil = kapital * es.ALLOCATION_PCT
            if anteil > frei:
                wegen_kapital += 1
                continue
            offen[idx] = anteil
            ausgefuehrt += 1
        else:
            if idx not in offen:
                continue
            anteil = offen.pop(idx)
            kapital += anteil * t["pnl_pct"] / 100

    return wegen_limit, wegen_kapital, ausgefuehrt


def main():
    es = lade_bot_modul()
    from multi_symbol_optimise import load_all_symbol_data

    daten = load_all_symbol_data()
    trades = es.collect_all_trades(daten, es.DEVIATION_PCT, es.STOP_LOSS_PCT,
                                    es.TAKE_PROFIT_FIB, es.USE_TAKE_PROFIT)
    echt = es.simulate_portfolio(trades, es.STARTING_CAPITAL,
                                  es.ALLOCATION_PCT, es.MAX_CONCURRENT_POSITIONS)
    limit, kapital, ausgefuehrt = zaehle_getrennt(es, trades)

    print("\n" + "=" * 60)
    print("UEBERSPRUNGENE TRADES - AUFSCHLUESSELUNG")
    print("=" * 60)
    print(f"Positionslimit:                  {es.MAX_CONCURRENT_POSITIONS}")
    print(f"Allokation je Trade:             {es.ALLOCATION_PCT:.0%}")
    print(f"Trades insgesamt:                {len(trades)}")
    print()
    print(f"  ausgefuehrt:                   {echt['num_executed']}")
    print(f"  uebersprungen:                 {echt['num_skipped']}")
    print(f"    davon Positionslimit:        {limit}")
    print(f"    davon zu wenig Kapital:      {kapital}")
    print()

    stimmt = (echt["num_skipped"] == limit + kapital
              and echt["num_executed"] == ausgefuehrt)
    print("Nachbau trifft das Original:", "JA" if stimmt else
          "NEIN - die Messung ist unbrauchbar")
    if not stimmt:
        print(f"  Original {echt['num_executed']}/{echt['num_skipped']}, "
              f"Nachbau {ausgefuehrt}/{limit + kapital}")
    sys.exit(0 if stimmt else 1)


if __name__ == "__main__":
    main()
