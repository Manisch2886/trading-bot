"""
Zigzag mit Bestaetigungszeitpunkt
====================================================================
Der Zigzag-Indikator des Projekts (`strategies/*/zigzag_indicator.py`)
gibt je Pivot NUR dessen eigenen Zeitstempel zurueck. Genau dort sitzt
der Look-Ahead: ein Pivot IST erst dann ein Pivot, wenn sich der Kurs
danach um `deviation_pct` in die Gegenrichtung bewegt hat. Der
Zeitstempel des Pivots liegt also VOR dem Zeitpunkt, zu dem man ihn
ueberhaupt erkennen konnte.

Dieses Modul ist eine WOERTLICHE UEBERNAHME von
`zigzag_indicator.calculate_zigzag` - Zeile fuer Zeile dieselbe Logik,
ergaenzt um genau eine zusaetzliche Ausgabe: den Balken-Index `i`, an
dem der Pivot fixiert (`pivots.append(...)`) wurde. Das ist der
frueheste Zeitpunkt, zu dem ein live laufendes Skript diesen Pivot
haette sehen koennen.

Dass die Uebernahme verhaltensgleich ist, wird NICHT behauptet, sondern
geprueft: `verify_baseline.py` vergleicht die Pivot-Liste dieses Moduls
Zeile fuer Zeile mit der der unveraenderten Bot-Funktion, auf den
echten Daten beider Bots.

Reine Backtest-Untersuchung: wird von keinem Live-Skript importiert.
"""

import pandas as pd


def calculate_zigzag_with_confirmation(df: pd.DataFrame, deviation_pct: float = 3.0) -> pd.DataFrame:
    """
    Wie `zigzag_indicator.calculate_zigzag`, gibt aber je Pivot zusaetzlich
    zurueck, WANN er erkennbar wurde.

    Spalten:
      time             Zeitstempel des Pivots selbst (wie im Original)
      price            Pivot-Preis (wie im Original)
      type             "high" / "low" (wie im Original)
      confirm_idx      Balken-Index, an dem der Pivot fixiert wurde
      confirm_time     Zeitstempel dieses Balkens
      pivot_idx        Balken-Index des Pivots selbst

    `confirm_idx` ist immer >= `pivot_idx`; die Differenz ist genau die
    Anzahl Balken, die der Backtest im Voraus weiss.
    """
    highs = df["high"].values
    lows = df["low"].values
    times = df["open_time"].values

    pivots = []

    # Startpunkt: erste Kerze als vorlaeufiger Pivot
    last_pivot_price = highs[0]
    last_pivot_idx = 0
    trend = None  # "up" oder "down" - wird beim ersten klaren Ausschlag gesetzt

    for i in range(1, len(df)):
        move_up_pct = (highs[i] - last_pivot_price) / last_pivot_price * 100
        move_down_pct = (last_pivot_price - lows[i]) / last_pivot_price * 100

        if trend is None:
            if move_up_pct >= deviation_pct:
                trend = "up"
                last_pivot_price = lows[last_pivot_idx]
                last_pivot_idx = i
            elif move_down_pct >= deviation_pct:
                trend = "down"
                last_pivot_price = highs[last_pivot_idx]
                last_pivot_idx = i
            continue

        if trend == "up":
            if highs[i] > last_pivot_price:
                last_pivot_price = highs[i]
                last_pivot_idx = i
            elif (last_pivot_price - lows[i]) / last_pivot_price * 100 >= deviation_pct:
                # HIER wird der Pivot fixiert - Balken i ist der frueheste
                # Zeitpunkt, zu dem er ueberhaupt erkennbar war.
                pivots.append((times[last_pivot_idx], last_pivot_price, "high",
                                i, times[i], last_pivot_idx))
                trend = "down"
                last_pivot_price = lows[i]
                last_pivot_idx = i

        elif trend == "down":
            if lows[i] < last_pivot_price:
                last_pivot_price = lows[i]
                last_pivot_idx = i
            elif (highs[i] - last_pivot_price) / last_pivot_price * 100 >= deviation_pct:
                pivots.append((times[last_pivot_idx], last_pivot_price, "low",
                                i, times[i], last_pivot_idx))
                trend = "up"
                last_pivot_price = highs[i]
                last_pivot_idx = i

    return pd.DataFrame(pivots, columns=["time", "price", "type",
                                          "confirm_idx", "confirm_time", "pivot_idx"])
