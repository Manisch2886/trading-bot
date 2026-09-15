"""
Tages-Datenabruf - Volatility Breakout Krypto
========================================================
Analog zu rsi2_crypto/fetch_1d_data.py bzw. t3_supertrend/fetch_4h_data.py
(Tageskerzen-Begruendung siehe backtest_breakout.py-Docstring). Nutzt
dasselbe Symbol-Universum UND denselben Zeitrahmen (Tageskerzen) wie
RSI-2 Krypto - eigenstaendige Kopie statt Cross-Strategy-Import
(Architektur-Prinzip), auch wenn beide Skripte de facto dieselben
BTCUSDT_1d.csv usw. befuellen (kein Konflikt: beide schreiben identische
Daten in denselben gemeinsamen data/-Ordner).

WICHTIG: In der Prototyp-Phase wurden die Tageskerzen mangels Sandbox-
Netzwerkzugriff aus vorhandenen 1h-Daten abgeleitet
(shared/build_daily_crypto_data.py). Dieses Skript ist der native Ersatz
dafuer auf der echten Maschine des Nutzers (mit Binance-API-Zugriff).

TB-35: Die laufende Kerze wird nicht mehr geschrieben
------------------------------------------------------------------------------
Der Endpunkt liefert den gerade angefangenen Zeitraum mit. Bis TB-35 landete
er in der CSV, und weil dieses Skript die Zieldatei vollstaendig
ueberschreibt, genuegte EIN Handstart, um eine Teilkerze in einen
Kursdatenbestand zurueckzuschreiben, der gerade sauber neu geladen worden war
(TB-34, 15.09.2026) - und damit den Datenstand-Hash der Vorregistrierung
unbemerkt zu aendern.

`abrufschutz.nur_abgeschlossene` verwirft sie, BEVOR geschrieben wird. Die
Zeile entsteht in der Datei also gar nicht erst; es wird nichts hinterher
herausgeschnitten.

Ueberschrieben wird weiterhin - absichtlich. Ein anhaengendes Werkzeug, das
sich irrt, laesst den Fehler dauerhaft stehen; ein ueberschreibendes ist beim
naechsten Lauf wieder in Ordnung. Ueberschreiben war nie das Problem, die
Teilkerze am Ende war es. Als Gegengewicht laeuft `abrufschutz.Wache` mit und
meldet, wenn ein Lauf eine Datei kuerzer zurueckgelassen hat als vorher. Sie
meldet nur - sie stoppt nichts.
"""

import os
import sys
import time
from binance.client import Client

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from fetch_binance_data import fetch_historical_data
from symbols_config import SYMBOLS
from paths import DATA_DIR

import abrufschutz

INTERVAL = Client.KLINE_INTERVAL_1DAY
LOOKBACK = "1 Jan, 2017"  # Binance-Start; festes Datum statt mitwanderndem
                          # Fenster. Vorher stand hier "3650 day ago UTC" mit
                          # der Begruendung, Binance liefere ohnehin nur die
                          # vorhandene Historie. Geprueft war das nie - es
                          # stimmte nur, solange 3650 Tage vor dem Abruftag
                          # noch vor dem Binance-Start lagen. Ab Sommer 2027
                          # haette das Fenster angefangen zu schneiden, und
                          # zwar leise: eine gekuerzte Datei sieht aus wie
                          # eine, die nie laenger war. Gleicher Stand wie
                          # t3_supertrend/fetch_4h_data.py und
                          # shared/fetch_multi_data.py (TB-31/TB-35).
PAUSE_BETWEEN_REQUESTS_SEC = 0.5

if __name__ == "__main__":
    print(f"Lade Tagesdaten fuer {len(SYMBOLS)} Symbole...\n")

    # Merkt sich VOR jedem Schreiben, wie die Zieldatei aussah, und meldet
    # hinterher, wenn dieser Lauf sie kuerzer zurueckgelassen hat. Melden,
    # nicht stoppen - siehe shared/abrufschutz.py.
    wache = abrufschutz.Wache()

    for i, symbol in enumerate(SYMBOLS, 1):
        print(f"[{i}/{len(SYMBOLS)}] Lade {symbol} ...")
        try:
            df = fetch_historical_data(symbol, INTERVAL, LOOKBACK)
            # Vor dem Schreiben, nicht danach: die laufende Kerze kommt gar
            # nicht erst in die Datei.
            df, _laufend = abrufschutz.nur_abgeschlossene(df, INTERVAL,
                                                          symbol=symbol)
            output_file = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL}.csv")
            if df is None or len(df) == 0:
                # Eine leere Tabelle zu schreiben hiesse, eine vorhandene
                # Datei auf ihre Kopfzeile zu verkuerzen. Dann lieber nichts.
                print(f"    Keine abgeschlossene Kerze fuer {symbol} - "
                      f"Datei bleibt unveraendert.")
            else:
                wache.vormerken(output_file)
                df.to_csv(output_file, index=False)
                wache.pruefe(output_file)
                print(f"    {len(df)} Kerzen gespeichert als {output_file}")
        except Exception as e:
            print(f"    Fehler bei {symbol}: {e}")

        time.sleep(PAUSE_BETWEEN_REQUESTS_SEC)

    print("\nFertig.")
    # Rueckgabewert 1 bei Befund der Wache: kein Fehler des Programms, aber
    # etwas, das ein Aufruf sichtbar machen soll (wie shared/kursdaten.py).
    sys.exit(1 if wache.melde() else 0)
