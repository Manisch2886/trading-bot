"""Attrappe fuer yfinance im Sandbox-Lauf.

fetch_stock_data.py importiert yfinance auf Modulebene, obwohl der
OOS-Lauf ausschliesslich die Konstante INTERVAL daraus braucht und seine
Kursdaten aus den bereits vorhandenen CSV-Dateien in data/ liest. Ohne
diese Attrappe scheitert der Import, mit ihr wird kein einziger
Netzwerkaufruf moeglich: download() wirft, statt still leere Daten zu
liefern - ein versehentlicher echter Abruf faellt damit sofort auf.
"""


def download(*args, **kwargs):
    raise AssertionError(
        "Im OOS-Lauf darf kein Kursabruf stattfinden - die Daten kommen "
        "aus den vorhandenen CSV-Dateien.")


class Ticker:
    def __init__(self, *args, **kwargs):
        raise AssertionError("Im OOS-Lauf darf kein Kursabruf stattfinden.")
