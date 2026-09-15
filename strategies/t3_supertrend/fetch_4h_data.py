"""
4-Stunden Datenabruf - T3/ADX/SuperTrend-Strategie
========================================================
Nachdem sich sowohl 1h als auch 15m als ungeeignet erwiesen haben
(1h: zu viel Whipsaw, 15m: unpraktikabel fuer ein Cronjob-basiertes
Setup und zu gebuehrenempfindlich bei kurzen Haltezeiten), testen
wir jetzt 4h - der klassische Zeitrahmen fuer T3/ADX/SuperTrend als
Trendfolge-Indikatoren.

Die 4h-Daten landen im selben gemeinsamen data/-Ordner wie die
1h-Daten des Elliott-Wave-Bots, aber unter eigenem Dateinamen
(BTCUSDT_4h.csv statt BTCUSDT_1h.csv) - kein Konflikt zwischen den
Strategien.

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

INTERVAL = Client.KLINE_INTERVAL_4HOUR
LOOKBACK = "1 Jan, 2017"  # Binance-Start; frueher 1825 Tage, siehe TB-31
PAUSE_BETWEEN_REQUESTS_SEC = 0.5

if __name__ == "__main__":
    print(f"Lade 4-Stunden-Daten fuer {len(SYMBOLS)} Symbole...\n")

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
