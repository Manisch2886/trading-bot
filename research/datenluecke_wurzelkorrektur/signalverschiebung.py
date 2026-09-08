"""
Vergleichslauf: Signalzeitpunkte mit und ohne Wurzelkorrektur
==================================================================
Spielt die LIVE-Signalregel der drei regelbasierten Aktien-Bots ueber die
gesamte gespeicherte Historie aller Symbole nach - einmal so, wie
forward_test.py heute rechnet (juengster Balken = "heute"), und einmal so,
wie es mit der Wurzelkorrektur waere (juengster Balken wird verworfen, weil
er ein noch laufender Handelstag sein koennte).

WICHTIG - rein lesend: dieses Skript veraendert keine Datei ausserhalb von
research/datenluecke_wurzelkorrektur/ und ruft keinen Bot-Code auf, der
schreibt. Die Indikator-Berechnung wird NICHT nachgebaut, sondern direkt
aus dem jeweiligen forward_test.py des Bots importiert (compute_indicators)
- so kann die Auswertung nicht von der echten Logik abweichen. Nachgebildet
ist ausschliesslich die eine Signal-Bedingung; sie steht im Bericht woertlich
neben dem Original.

Was gemessen wird - und was NICHT gemessen werden muss:

  Die Menge der Signal-Balken ist in beiden Varianten IDENTISCH. Das ist
  keine Messung, sondern folgt aus der Konstruktion: heute wird an Tag D der
  Balken D geprueft, mit Wurzelkorrektur an Tag D der Balken D-1 - jeder
  Balken wird in beiden Varianten genau einmal geprueft. Verschoben wird
  also nicht OB, sondern WANN gehandelt wird und ZU WELCHEM PREIS.

  Gemessen wird deshalb:
    1. die Zahl der Signal-Balken je Bot (Groessenordnung des Betroffenen),
    2. der Unterschied im Einstiegspreis: forward_test.py bucht
       entry_price = Schlusskurs des juengsten Balkens. Mit Wurzelkorrektur
       waere das der Schlusskurs des VORTAGS.

Nutzung:  python3 signalverschiebung.py [--json]
"""

import json
import os
import sys
import types

import numpy as np
import pandas as pd

DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(DIR))
DATA_DIR = os.path.join(REPO, "data")
RESULTS_DIR = os.path.join(DIR, "results")

# Die drei Bots mit einer Signalregel, die sich exakt auf genau einem Balken
# entscheiden laesst. elliott_wave_stocks fehlt hier bewusst - seine Regel
# haengt an einer Zigzag-Wellenerkennung ueber die gesamte Historie und an
# einem Frischefenster; siehe BERICHT.md, Abschnitt zur Reichweite.
BOTS = ["rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout"]


def _stubs_setzen():
    """yfinance/fetch_stock_data werden beim Import von forward_test.py
    gebraucht, duerfen hier aber nie aufgerufen werden - dieses Skript
    arbeitet ausschliesslich auf den bereits gespeicherten CSVs."""
    for name in ("yfinance", "fetch_stock_data"):
        if name in sys.modules:
            continue
        modul = types.ModuleType(name)
        for attr in ("download", "fetch_historical_data", "Ticker"):
            setattr(modul, attr, lambda *a, **k: (_ for _ in ()).throw(
                AssertionError("Stub: dieses Skript laedt keine Kursdaten nach")))
        sys.modules[name] = modul


def bot_modul(bot: str):
    """Importiert forward_test.py EINES Bots. Wird je Bot in einem eigenen
    Prozess aufgerufen (siehe __main__), weil die Bots gleichnamige Module
    haben (indicators, stocks_symbols_config) und sich sonst gegenseitig
    aus sys.modules verdraengen wuerden."""
    sys.path.insert(0, os.path.join(REPO, "shared"))
    sys.path.insert(0, os.path.join(REPO, "strategies", bot))
    _stubs_setzen()
    import forward_test
    return forward_test


def signal_maske(bot: str, df: pd.DataFrame) -> pd.Series:
    """True fuer jeden Balken, auf dem die Live-Regel des Bots ein neues
    Einstiegssignal ergeben wuerde. Die Bedingungen sind woertlich aus
    find_new_signals() des jeweiligen forward_test.py uebernommen (siehe
    BERICHT.md fuer die Gegenueberstellung).

    Bewusst NICHT nachgebildet: Positionslimit, Pyramiding-Sperre und
    Datenbank-Zustand. Sie entscheiden, ob ein Signal auch AUSGEFUEHRT
    wird - fuer die Frage, WANN und zu welchem Preis ein Signal entsteht,
    sind sie ohne Belang, und sie haengen vom Live-Zustand ab, den dieses
    Skript nicht kennt.
    """
    if bot == "rsi2_mean_reversion":
        from forward_test import RSI_THRESHOLD
        gueltig = df["sma_trend"].notna() & df["rsi"].notna()
        return gueltig & (df["close"] > df["sma_trend"]) & (df["rsi"] < RSI_THRESHOLD)

    if bot == "turtle_soup_stocks":
        gueltig = df["donchian_low"].notna() & df["low"].notna() & df["close"].notna()
        return gueltig & (df["low"] < df["donchian_low"]) & (df["close"] > df["donchian_low"])

    if bot == "volatility_breakout":
        squeeze_gestern = df["is_squeeze"].shift(1)
        gueltig = df["bb_upper"].notna() & df["close"].notna() & squeeze_gestern.notna()
        return gueltig & squeeze_gestern.astype("boolean").fillna(False) & (df["close"] > df["bb_upper"])

    raise ValueError(bot)


def auswerten(bot: str) -> dict:
    ft = bot_modul(bot)
    from stocks_symbols_config import SYMBOLS

    signale = 0
    balken = 0
    symbole_mit_daten = 0
    abweichungen = []          # relativer Preisunterschied je Signal
    signal_am_letzten_balken = 0

    for symbol in SYMBOLS:
        pfad = os.path.join(DATA_DIR, f"{symbol}_1d.csv")
        if not os.path.exists(pfad):
            continue
        roh = pd.read_csv(pfad, parse_dates=["open_time"])
        if roh.empty:
            continue
        symbole_mit_daten += 1

        df = ft.compute_indicators(roh)
        maske = signal_maske(bot, df).fillna(False)
        balken += len(df)
        signale += int(maske.sum())

        # Einstiegspreis heute (Schluss des Signalbalkens) gegen den Preis,
        # den die Wurzelkorrektur buchen wuerde (Schluss des Vortags).
        heute = df["close"]
        vortag = df["close"].shift(1)
        treffer = maske & vortag.notna() & (heute > 0)
        if treffer.any():
            abweichungen.extend(((vortag[treffer] - heute[treffer]) / heute[treffer] * 100).tolist())

        if bool(maske.iloc[-1]):
            signal_am_letzten_balken += 1

    a = np.array(abweichungen)
    return {
        "bot": bot,
        "symbole_mit_daten": symbole_mit_daten,
        "geprüfte_balken": balken,
        "signal_balken": signale,
        "signale_je_symbol_und_jahr": round(signale / max(symbole_mit_daten, 1)
                                             / max(balken / max(symbole_mit_daten, 1) / 252, 1e-9), 2),
        "symbole_mit_signal_am_letzten_balken": signal_am_letzten_balken,
        "preisunterschied_prozentpunkte": {
            "n": int(a.size),
            "median_absolut": round(float(np.median(np.abs(a))), 3) if a.size else None,
            "mittelwert": round(float(a.mean()), 3) if a.size else None,
            "p90_absolut": round(float(np.percentile(np.abs(a), 90)), 3) if a.size else None,
            "maximum_absolut": round(float(np.abs(a).max()), 3) if a.size else None,
            "anteil_ueber_1pp": round(float((np.abs(a) > 1).mean() * 100), 1) if a.size else None,
            "anteil_ueber_3pp": round(float((np.abs(a) > 3).mean() * 100), 1) if a.size else None,
        },
    }


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in BOTS:
        print(json.dumps(auswerten(sys.argv[1]), ensure_ascii=False))
        raise SystemExit

    import subprocess
    os.makedirs(RESULTS_DIR, exist_ok=True)
    alle = []
    for bot in BOTS:
        ergebnis = subprocess.run([sys.executable, __file__, bot], capture_output=True, text=True)
        if ergebnis.returncode != 0:
            print(f"FEHLER bei {bot}:\n{ergebnis.stderr[-1500:]}", file=sys.stderr)
            raise SystemExit(1)
        alle.append(json.loads(ergebnis.stdout.strip().splitlines()[-1]))

    with open(os.path.join(RESULTS_DIR, "signalverschiebung.json"), "w") as fh:
        json.dump(alle, fh, indent=1, ensure_ascii=False)

    print("Signalverschiebung durch die Wurzelkorrektur (juengster Balken verworfen)\n")
    print(f"{'Bot':22} {'Symbole':>8} {'Balken':>9} {'Signale':>8} "
          f"{'|Δ Preis| Median':>16} {'p90':>7} {'>1pp':>7} {'>3pp':>7}")
    print("-" * 92)
    for e in alle:
        p = e["preisunterschied_prozentpunkte"]
        print(f"{e['bot']:22} {e['symbole_mit_daten']:>8} {e['geprüfte_balken']:>9} "
              f"{e['signal_balken']:>8} {str(p['median_absolut']) + ' pp':>16} "
              f"{str(p['p90_absolut']):>7} {str(p['anteil_ueber_1pp']) + '%':>7} "
              f"{str(p['anteil_ueber_3pp']) + '%':>7}")
    print("\nDie Menge der Signal-Balken ist in beiden Varianten identisch (siehe")
    print("Modul-Docstring). Verschoben wird der Handelstag um genau einen")
    print("Boersentag und der gebuchte Einstiegspreis um die oben gemessene Spanne.")
