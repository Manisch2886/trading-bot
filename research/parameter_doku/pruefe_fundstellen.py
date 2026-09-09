"""
Halten die dokumentierten Fundstellen noch?
================================================================================
PR #45, Befund 7.2: mehrere Parameter bestimmen den Live-Betrieb, stehen aber
nicht in live_params.py. Sie wurden dort dokumentiert - mit Wert UND exakter
Fundstelle (Datei + Zeile).

Genau daran liegt das Problem dieser Art von Dokumentation: Zeilennummern
verrutschen bei der naechsten Aenderung, und ein Kommentar, der auf die
falsche Zeile zeigt, ist schlimmer als keiner - er sieht praezise aus und ist
es nicht. Beim Schreiben der Blocks waren zwei von zwanzig Angaben bereits
falsch (die use_volume_filter-Signaturen beider Breakout-Bots), nur durch
diese Pruefung aufgefallen.

Das Skript haelt deshalb jede dokumentierte Angabe gegen die Wirklichkeit:

  1. FUNDSTELLEN - zeigt "datei.py:ZEILE" noch auf den genannten Namen?
  2. WERTE - stimmt die dokumentierte Zahl noch mit der echten Konstante?

Rein lesend, veraendert nichts.

Nutzung:  python3 pruefe_fundstellen.py
"""

import ast
import os
import re
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
STRATEGIES = os.path.join(_REPO_ROOT, "strategies")

_bestanden = 0
_fehler = []


def check(name, ok, detail=""):
    global _bestanden
    if ok:
        _bestanden += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        _fehler.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


# Was in den live_params.py-Dokublocken behauptet wird:
# (Bot, Datei, Zeile, erwarteter Name in dieser Zeile)
FUNDSTELLEN = [
    # Seit PR #51 stehen die fuenf Indikator-Parameter in live_params.py
    # selbst; backtest_trend.py und forward_test.py importieren sie von dort.
    # Die frueheren Eintraege zeigten auf ihre alten Definitionsstellen in
    # jenen beiden Dateien - die es nicht mehr gibt. Geprueft wird jetzt der
    # heutige Weg: Quelle in live_params.py, Import in beiden Verbrauchern.
    ("t3_supertrend", "live_params.py", 17, "T3_FACTOR"),
    ("t3_supertrend", "live_params.py", 21, "ATR_MULT"),
    ("t3_supertrend", "backtest_trend.py", 59, "T3_FACTOR"),
    ("t3_supertrend", "backtest_trend.py", 66, "use_vwap_filter"),
    ("t3_supertrend", "forward_test.py", 39, "T3_FACTOR"),
    ("t3_supertrend", "indicators.py", 128, "bars_per_day"),
    ("t3_supertrend", "regime_filter.py", 19, "atr_length"),
    ("t3_supertrend", "equity_simulation.py", 66, "compute_btc_regime"),
    ("volatility_breakout", "backtest_breakout.py", 97, "VOLUME_AVG_PERIOD"),
    ("volatility_breakout", "backtest_breakout.py", 103, "VOLUME_FILTER_MULTIPLIER"),
    ("volatility_breakout", "backtest_breakout.py", 134, "use_volume_filter"),
    ("volatility_breakout", "equity_simulation.py", 160, "collect_all_trades"),
    ("volatility_breakout_crypto", "regime_filter.py", 16, "BTC_ATR_LENGTH"),
    ("volatility_breakout_crypto", "regime_filter.py", 17, "BTC_ATR_MULT"),
    ("volatility_breakout_crypto", "backtest_breakout.py", 65, "VOLUME_AVG_PERIOD"),
    ("volatility_breakout_crypto", "backtest_breakout.py", 71, "VOLUME_FILTER_MULTIPLIER"),
    ("volatility_breakout_crypto", "backtest_breakout.py", 97, "use_volume_filter"),
    ("volatility_breakout_crypto", "equity_simulation.py", 176, "collect_all_trades"),
    ("volatility_breakout_crypto", "forward_test.py", 256, "compute_btc_regime"),
]

# (Bot, Datei, Konstante, dokumentierter Wert)
WERTE = [
    # Frueher standen diese zehn Zeilen hier zweimal - je einmal fuer
    # backtest_trend.py und forward_test.py, die die Werte damals unabhaengig
    # fuehrten. Seit PR #51 gibt es nur noch EINE Quelle; die Zeilen sind
    # entsprechend auf live_params.py zusammengefuehrt.
    ("t3_supertrend", "live_params.py", "T3_FACTOR", 0.7),
    ("t3_supertrend", "live_params.py", "DI_LENGTH", 14),
    ("t3_supertrend", "live_params.py", "ADX_LENGTH", 14),
    ("t3_supertrend", "live_params.py", "ATR_LENGTH", 22),
    ("t3_supertrend", "live_params.py", "ATR_MULT", 3.0),
    ("volatility_breakout", "backtest_breakout.py", "VOLUME_FILTER_MULTIPLIER", 1.5),
    ("volatility_breakout", "backtest_breakout.py", "VOLUME_AVG_PERIOD", 20),
    ("volatility_breakout_crypto", "backtest_breakout.py", "VOLUME_FILTER_MULTIPLIER", 1.5),
    ("volatility_breakout_crypto", "backtest_breakout.py", "VOLUME_AVG_PERIOD", 20),
    ("volatility_breakout_crypto", "regime_filter.py", "BTC_ATR_LENGTH", 22),
    ("volatility_breakout_crypto", "regime_filter.py", "BTC_ATR_MULT", 3.0),
]

# Die fuenf Groessen, die t3_supertrend DOPPELT fuehrt. Der Dokublock sagt
# "Stand 2026-09-08 identisch" - genau das wird hier nachgehalten.
DOPPELT_GEFUEHRT = ["T3_FACTOR", "DI_LENGTH", "ADX_LENGTH", "ATR_LENGTH", "ATR_MULT"]


def konstanten(bot: str, datei: str) -> dict:
    pfad = os.path.join(STRATEGIES, bot, datei)
    with open(pfad, encoding="utf-8") as f:
        baum = ast.parse(f.read(), filename=pfad)
    werte = {}
    for knoten in baum.body:
        if not isinstance(knoten, ast.Assign):
            continue
        try:
            wert = ast.literal_eval(knoten.value)
        except (ValueError, SyntaxError):
            continue
        for ziel in knoten.targets:
            if isinstance(ziel, ast.Name):
                werte[ziel.id] = wert
    return werte


def teste_fundstellen():
    print("\n1) Zeigen die dokumentierten Zeilennummern noch richtig?")
    for bot, datei, zeile, name in FUNDSTELLEN:
        pfad = os.path.join(STRATEGIES, bot, datei)
        with open(pfad, encoding="utf-8") as f:
            zeilen = f.read().splitlines()
        ist = zeilen[zeile - 1] if zeile <= len(zeilen) else "<ausserhalb der Datei>"
        gefunden = name in ist
        hinweis = ""
        if not gefunden:
            # Beim Fehlschlag gleich die richtige Zeile nennen, damit die
            # Korrektur nicht erst gesucht werden muss.
            treffer = [i for i, z in enumerate(zeilen, 1) if name in z]
            hinweis = (f"steht jetzt in Zeile {treffer[0]}" if treffer
                        else "kommt in der Datei gar nicht mehr vor")
        check(f"{bot}/{datei}:{zeile} nennt {name}", gefunden,
              hinweis or "")


def teste_werte():
    print("\n2) Stimmen die dokumentierten Werte noch?")
    for bot, datei, name, soll in WERTE:
        ist = konstanten(bot, datei).get(name, "<fehlt>")
        check(f"{bot}/{datei}: {name} = {soll}", ist == soll,
              f"tatsaechlich {ist}" if ist != soll else "")


def live_importe(bot: str, datei: str) -> set:
    """Namen, die eine Datei per `from live_params import ...` hereinholt."""
    pfad = os.path.join(STRATEGIES, bot, datei)
    with open(pfad, encoding="utf-8") as f:
        baum = ast.parse(f.read(), filename=pfad)
    return {a.name for k in ast.walk(baum)
            if isinstance(k, ast.ImportFrom) and k.module == "live_params"
            for a in k.names}


def teste_doppelfuehrung():
    """Frueher stand hier ein WERTVERGLEICH: fuehren backtest_trend.py und
    forward_test.py dieselben fuenf Zahlen?

    Seit PR #51 fuehrt keine der beiden Dateien sie mehr - beide importieren
    aus live_params.py. Der alte Vergleich lief damit ins Leere und meldete
    `<fehlt> vs. <fehlt>`, also GLEICH, und galt als bestanden. Eine Pruefung,
    die gruen wird, weil sie nichts mehr findet, ist schlimmer als keine.

    Geprueft wird deshalb jetzt die Struktur statt der Zahlen: beide Dateien
    muessen die fuenf Groessen aus live_params.py importieren. Faengt eine von
    ihnen wieder an, eine eigene Zahl zu fuehren, faellt das hier auf - und
    zwar bevor die beiden auseinanderlaufen koennen."""
    print("\n3) t3_supertrend: gibt es wieder eine zweite Quelle?")
    bt = live_importe("t3_supertrend", "backtest_trend.py")
    ft = live_importe("t3_supertrend", "forward_test.py")
    bt_konst = konstanten("t3_supertrend", "backtest_trend.py")
    ft_konst = konstanten("t3_supertrend", "forward_test.py")
    for name in DOPPELT_GEFUEHRT:
        importiert = name in bt and name in ft
        eigene_zahl = [d for d, k in (("backtest_trend.py", bt_konst),
                                       ("forward_test.py", ft_konst)) if name in k]
        check(f"{name}: beide Dateien lesen aus live_params.py",
              importiert and not eigene_zahl,
              ("fuehrt wieder eine eigene Zahl in " + ", ".join(eigene_zahl))
              if eigene_zahl else
              ("" if importiert else f"Import fehlt (backtest={name in bt}, "
                                      f"forward={name in ft})"))


def teste_nur_dokumentation():
    """Die Dokublocks duerfen keinen Wert definieren - sonst waere aus der
    Dokumentation eine zweite Quelle geworden, genau das Gegenteil der
    Absicht."""
    print("\n4) Die Dokublocks definieren selbst keine Werte")
    erwartet = {
        # Die fuenf Indikator-Parameter sind seit PR #51 ABSICHTLICH hier -
        # sie waren der Gegenstand jener Umstellung. Sie als "neu
        # hinzugekommen" zu melden war die Folge davon, dass diese Liste
        # seither nicht nachgezogen wurde.
        "t3_supertrend": {"T3_FAST_LENGTH", "T3_SLOW_LENGTH", "ADX_THRESHOLD",
                           "STOP_LOSS_PCT", "MAX_CONCURRENT_POSITIONS", "LAST_UPDATED",
                           "T3_FACTOR", "DI_LENGTH", "ADX_LENGTH", "ATR_LENGTH",
                           "ATR_MULT"},
        "volatility_breakout": {"BB_SQUEEZE_PERCENTILE", "BB_LOOKBACK",
                                 "STOP_LOSS_PCT", "MAX_HOLD_DAYS", "ALLOCATION_PCT",
                                 "MAX_CONCURRENT_POSITIONS", "LAST_UPDATED"},
        "volatility_breakout_crypto": {"BB_SQUEEZE_PERCENTILE", "BB_LOOKBACK",
                                        "STOP_LOSS_PCT", "MAX_HOLD_DAYS",
                                        "BTC_REGIME_FILTER_ENABLED", "ALLOCATION_PCT",
                                        "MAX_CONCURRENT_POSITIONS", "LAST_UPDATED"},
    }
    for bot, soll in erwartet.items():
        ist = set(konstanten(bot, "live_params.py"))
        zuviel = ist - soll
        check(f"{bot}/live_params.py definiert nur die bisherigen Konstanten",
              not zuviel, f"neu hinzugekommen: {sorted(zuviel)}" if zuviel else "")


def main():
    print("Pruefung der dokumentierten Fundstellen (PR #45, Befund 7.2)")
    teste_fundstellen()
    teste_werte()
    teste_doppelfuehrung()
    teste_nur_dokumentation()

    print(f"\n{_bestanden}/{_bestanden + len(_fehler)} Pruefungen bestanden.")
    for name in _fehler:
        print(f"FEHLGESCHLAGEN: {name}")
    sys.exit(1 if _fehler else 0)


if __name__ == "__main__":
    main()
