"""Attrappe fuer yfinance im Sandbox-Lauf (Aktien-Bots).

fetch_stock_data.py bindet yfinance auf Modulebene ein; equity_simulation.py
importiert diese Datei nur wegen der Konstante INTERVAL mit. Ein echter
Abruf findet im Vergleichslauf nicht statt - die Kursdaten kommen aus den
vorhandenen CSV-Dateien unter data/.

download() wirft deshalb, statt leere Daten zu liefern. Ein leerer
DataFrame waere hier die gefaehrlichere Attrappe: der Lauf liefe weiter,
faende null Trades und meldete "identisch" - ein Ergebnis, das nichts
belegt. Ohne diese Attrappe scheitert der Lauf am fehlenden Modul, und in
der ersten Fassung von backtest_regression.py fiel das nicht einmal auf
(siehe dortigen Hinweis zum Abbruch).
"""


def download(*args, **kwargs):
    raise AssertionError("Im Vergleichslauf darf kein Kursabruf stattfinden - "
                         "die Daten kommen aus den vorhandenen CSV-Dateien.")


class Ticker:
    def __init__(self, *args, **kwargs):
        raise AssertionError("Im Vergleichslauf darf kein Kursabruf "
                             "stattfinden.")
