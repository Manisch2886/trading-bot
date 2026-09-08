"""Attrappe fuer binance.client im Sandbox-Lauf.

forward_test.py importiert Client nur, um daraus die Intervall-Konstante
zu lesen (INTERVAL = Client.KLINE_INTERVAL_1DAY). Die Konstanten muessen
deshalb die ECHTEN Werte tragen - eine Attrappe, die hier etwas anderes
liefert, wuerde den Vergleich verfaelschen, ohne dass es auffiele.
Ein Verbindungsversuch wirft dagegen sofort.
"""


class Client:
    KLINE_INTERVAL_1MINUTE = "1m"
    KLINE_INTERVAL_15MINUTE = "15m"
    KLINE_INTERVAL_1HOUR = "1h"
    KLINE_INTERVAL_4HOUR = "4h"
    KLINE_INTERVAL_1DAY = "1d"

    def __init__(self, *args, **kwargs):
        raise AssertionError("Im Vergleichslauf darf keine Binance-Verbindung "
                             "aufgebaut werden.")
