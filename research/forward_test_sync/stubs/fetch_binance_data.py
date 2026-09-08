"""Attrappe fuer shared/fetch_binance_data.py.

Die echte Datei enthaelt Zugangsdaten und steht in .gitignore. Sie wird
hier nur importiert, weil forward_test.py sie auf Modulebene einbindet -
der Vergleichslauf ruft fetch_historical_data() nie auf, sondern reicht
die Kursdaten direkt hinein.
"""


def fetch_historical_data(*args, **kwargs):
    raise AssertionError("Im Vergleichslauf darf kein Kursabruf stattfinden - "
                         "die Daten kommen aus den vorhandenen CSV-Dateien.")
