"""
Aktienkurs-Datenabruf (taeglich) via yfinance
==================================================
Laedt die maximal verfuegbare Historie an Tages-Kerzen fuer jede
Aktie in der Symbol-Liste. Landet im selben gemeinsamen data/-Ordner
wie die Krypto-Daten, aber unter eigenem Dateinamen (z.B. AAPL_1d.csv)
- kein Konflikt mit den Krypto-Strategien.

HINWEIS: yfinance ist eine inoffizielle Bibliothek, die Yahoo Finance
im Hintergrund abfragt. Sie ist kostenlos und weit verbreitet, aber
nicht so verlaesslich wie eine offizielle Broker-API - bei
Verbindungsfehlern bei einzelnen Aktien ist das normal, das Skript
faehrt einfach mit der naechsten fort.

TB-35: Die laufende Kerze wird nicht mehr geschrieben
------------------------------------------------------------------------------
yfinance liefert am laufenden Handelstag eine Tageszeile mit, die noch nicht
fertig ist. Bis TB-35 landete sie in der CSV, und weil dieses Skript die
Zieldatei vollstaendig ueberschreibt, genuegte EIN Handstart, um eine
Teilkerze in einen frisch geladenen Kursdatenbestand zurueckzuschreiben - und
damit den Datenstand-Hash der Vorregistrierung unbemerkt zu aendern.

`abrufschutz.nur_abgeschlossene` verwirft sie, BEVOR geschrieben wird. Sie
verlangt fuer eine Tageszeile mit dem Datum D den Stand `D 23:59:59` UTC und
wartet damit bewusst drei bis vier Stunden laenger als noetig (die NYSE
schliesst um 20:00 bzw. 21:00 UTC). Warum das hier ohne Boersenkalender
richtig ist - anders als in `notifications/boersenkalender.py` - steht
ausfuehrlich im Kopf von `shared/abrufschutz.py`: die Frage "ist dieser
Zeitraum SICHER vorbei?" hat nur eine teure Fehlerrichtung, und eine
einseitige Frage braucht keine genaue Antwort, sondern eine sichere Schranke.

WO die Absicherung sitzt, ist Absicht: im `__main__`-Teil, NICHT in
`fetch_historical_data`. Diese Funktion versorgt naemlich auch `forward_test.py`
mit Live-Daten (siehe den Hinweis weiter unten). Der Filter dort haette die
Signallogik der laufenden Bots veraendert - eine Aenderung am Handelsverhalten,
die nach Abschnitt 7 des Uebergabeprotokolls durch Backtest, Walk-Forward und
Equity-Simulation muss und ausdruecklich nicht Gegenstand von TB-35 ist. Die
CSV bekommt die Zeile so oder so nie zu sehen.

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

import pandas as pd
import yfinance as yf

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
from kursdaten import entferne_unvollstaendige
import abrufschutz
_P = get_strategy_paths(__file__)
DATA_DIR = _P["DATA_DIR"]

from stocks_symbols_config import SYMBOLS

INTERVAL = "1d"
PERIOD = "max"  # laengstmoegliche verfuegbare Historie je Aktie
PAUSE_BETWEEN_REQUESTS_SEC = 0.3


def fetch_historical_data(ticker: str, period: str = PERIOD, interval: str = INTERVAL) -> pd.DataFrame:
    """Laedt historische Kursdaten fuer eine einzelne Aktie und bringt sie
    ins selbe Format wie die Krypto-Daten (open_time/open/high/low/close/volume)."""
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)

    if df.empty:
        return pd.DataFrame(columns=["open_time", "open", "high", "low", "close", "volume"])

    # yfinance liefert bei manchen Versionen MultiIndex-Spalten - absichern
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()
    date_col = "Date" if "Date" in df.columns else "Datetime"

    df = df.rename(columns={
        date_col: "open_time",
        "Open": "open", "High": "high", "Low": "low",
        "Close": "close", "Volume": "volume",
    })

    df = df[["open_time", "open", "high", "low", "close", "volume"]]

    # Kerzen ohne Kurse hier streichen - an der fruehesten Stelle, an der sie
    # ins Projekt kommen. yfinance liefert gelegentlich eine Zeile mit Datum
    # und Volumen, aber leeren OHLC-Werten (gemessen: APH, 2026-09-01). Ein
    # Trade, der auf so einer Kerze per Zeitausstieg endet, bekommt
    # exit_price = NaN; daraus wird pnl_pct = NaN, und das vergiftet in
    # equity_simulation.simulate_portfolio jede danach berechnete
    # Kapitalzeile - ohne Fehlermeldung.
    #
    # Diese Funktion schreibt die CSVs UND versorgt forward_test.py mit
    # Live-Daten. Die Absicherung wirkt damit auf beiden Wegen, ohne dass
    # forward_test.py angefasst werden muss.
    df, _gestrichen = entferne_unvollstaendige(df, symbol=ticker)
    return df.reset_index(drop=True)


if __name__ == "__main__":
    print(f"Lade taegliche Kursdaten fuer {len(SYMBOLS)} Aktien...\n")

    # Merkt sich VOR jedem Schreiben, wie die Zieldatei aussah, und meldet
    # hinterher, wenn dieser Lauf sie kuerzer zurueckgelassen hat. Melden,
    # nicht stoppen - siehe shared/abrufschutz.py.
    wache = abrufschutz.Wache()

    for i, ticker in enumerate(SYMBOLS, 1):
        print(f"[{i}/{len(SYMBOLS)}] Lade {ticker} ...")
        try:
            df = fetch_historical_data(ticker)
            # Vor dem Schreiben, nicht danach: die laufende Tageszeile kommt
            # gar nicht erst in die Datei.
            df, _laufend = abrufschutz.nur_abgeschlossene(df, INTERVAL,
                                                          symbol=ticker)
            if df is None or df.empty:
                # Deckt beides ab: yfinance hat nichts geliefert, oder das
                # Gelieferte war ausschliesslich die laufende Zeile. Eine
                # leere Tabelle zu schreiben hiesse, eine vorhandene Datei
                # auf ihre Kopfzeile zu verkuerzen. Dann lieber nichts.
                print(f"    Keine abgeschlossene Kerze fuer {ticker} - "
                      f"Datei bleibt unveraendert.")
            else:
                output_file = os.path.join(DATA_DIR, f"{ticker}_{INTERVAL}.csv")
                wache.vormerken(output_file)
                df.to_csv(output_file, index=False)
                wache.pruefe(output_file)
                print(f"    {len(df)} Kerzen gespeichert als {output_file}")
        except Exception as e:
            print(f"    Fehler bei {ticker}: {e}")

        time.sleep(PAUSE_BETWEEN_REQUESTS_SEC)

    print("\nFertig.")
    # Rueckgabewert 1 bei Befund der Wache: kein Fehler des Programms, aber
    # etwas, das ein Aufruf sichtbar machen soll (wie shared/kursdaten.py).
    sys.exit(1 if wache.melde() else 0)
