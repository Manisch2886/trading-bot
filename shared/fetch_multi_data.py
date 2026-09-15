"""
Phase 3c - Multi-Symbol Datenabruf
=====================================
Laedt historische Daten fuer viele Coins statt nur einer Handvoll.
Ziel: mehr unabhaengige Marktereignisse -> mehr Elliott-Wave-Signale
insgesamt -> statistisch belastbarere Backtests und Optimierung.

Nutzt die zentrale Symbol-Liste aus symbols_config.py (Top 100 nach
Volumen, falls zuvor 'python3 get_top_symbols.py' ausgefuehrt wurde).

WICHTIG: Bei sehr vielen Symbolen dauert dieser Abruf entsprechend
laenger. Kleine Pausen zwischen Anfragen schuetzen vor Binance's
Rate-Limits.

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
from fetch_binance_data import fetch_historical_data
from symbols_config import SYMBOLS
from paths import DATA_DIR

import abrufschutz

client = Client()

INTERVAL = Client.KLINE_INTERVAL_1HOUR
LOOKBACK = "1 Jan, 2017"  # Binance-Start; frueher 1825 Tage, siehe TB-31
PAUSE_BETWEEN_REQUESTS_SEC = 0.5  # schont Binance's Rate-Limit bei vielen Symbolen


if __name__ == "__main__":
    print(f"Lade Daten fuer {len(SYMBOLS)} Symbole...\n")

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

    print("\nFertig. Alle verfuegbaren Symbole geladen.")
    # Rueckgabewert 1 bei Befund der Wache: kein Fehler des Programms, aber
    # etwas, das ein Aufruf sichtbar machen soll (wie shared/kursdaten.py).
    sys.exit(1 if wache.melde() else 0)
