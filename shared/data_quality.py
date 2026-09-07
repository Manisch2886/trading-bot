"""
Unvollstaendige Kursbalken erkennen - gemeinsam fuer alle Bots
==========================================================================
Warum es das gibt
--------------------------------------------------------------------------
Am 2026-09-01 trug `data/APH_1d.csv` einen Balken mit Volumen, aber ohne
Kurse: open/high/low/close waren alle leer. So sieht bei yfinance ein
Handelstag aus, der noch laeuft oder dessen Kurse beim Abruf noch nicht
feststanden. Der Balken ist damit der LETZTE der Datei - und genau den
schauen sich `find_new_signals` und `check_open_trades` an.

Was so ein Balken im Live-Betrieb anrichtet, ist nachgemessen und nicht
vermutet (Reproduktion in der PR-Beschreibung):

* Ein Stop-Loss loest NICHT aus. `NaN <= stop_price` ist False - die
  Position bleibt offen, obwohl der Stop haette greifen muessen.
* Ein Zeit-Ausstieg, der auf diesen Balken faellt, SCHLIESST den Trade mit
  `exit_price = NaN` und schreibt NaN als PnL in die Live-Datenbank.
* Bei elliott_wave_stocks nimmt `find_new_signals` den letzten Schlusskurs
  als Einstiegspreis - also NaN. Der Trade wuerde mit leerem Einstiegskurs
  eroeffnet, und jede spaetere Kennzahl daraus waere NaN.

Auffaellig wird davon nichts: pandas ueberspringt NaN beim Mitteln, ein
NaN-Vergleich ist stillschweigend False. Der Fehler verschwindet also in
den Kennzahlen, statt sich zu melden.

Wie damit umgegangen wird
--------------------------------------------------------------------------
Dieselbe Linie, die `buy_and_hold_benchmark.py` fuer dasselbe Problem
schon faehrt: **betroffene Daten sauber ueberspringen statt die Rechnung
still zu vergiften** - und die Streichung sichtbar machen.

Bewusst NICHT gewaehlt: den letzten gueltigen Kurs einsetzen. Das waere
eine erfundene Zahl an genau der Stelle, an der ueber einen echten
Ausstieg entschieden wird. Ein Balken ohne Kurse ist kein Balken mit
Kurs 0 und auch keiner mit dem Kurs von gestern - er ist schlicht noch
nicht da. Der Bot wartet deshalb auf den naechsten Balken, der wirklich
existiert; Stop und Ziel werden dort ausgewertet. Das verschiebt einen
Ausstieg im Extremfall um einen Balken - aber es erfindet keinen Preis
und schreibt kein NaN in die Datenbank.

Aktueller Bestand (alle 242 Kursdateien geprueft): betroffen ist genau
`APH_1d.csv`. Die Krypto-Dateien (Binance) haben keine Luecken - dort
liefert die Quelle nur abgeschlossene Kerzen. Strukturell anfaellig sind
also die vier Aktien-Bots, und zwar fuer jedes ihrer 147 Symbole an jedem
Tag, an dem der Abruf einen noch offenen Handelstag erwischt.
"""

PREISSPALTEN = ("open", "high", "low", "close")


def balken_unvollstaendig(row, spalten=PREISSPALTEN) -> bool:
    """True, wenn dem Balken mindestens einer der Kurse fehlt.

    `row` ist eine pandas-Series (eine Zeile aus dem Kurs-DataFrame).
    Spalten, die es gar nicht gibt, werden ignoriert - nicht jeder
    Bot fuehrt alle vier."""
    import pandas as pd

    for spalte in spalten:
        if spalte in row.index and pd.isna(row[spalte]):
            return True
    return False


def melde_uebersprungene_balken(symbol: str, anzahl: int, kontext: str = "") -> None:
    """Macht eine Streichung sichtbar. Bewusst eine gewoehnliche
    Konsolenausgabe: die Bots laufen per Cronjob und schreiben ihr Log
    ohnehin ueber print()."""
    if anzahl <= 0:
        return
    zusatz = f" ({kontext})" if kontext else ""
    print(f"  [DATENLUECKE] {symbol}: {anzahl} Kursbalken ohne Kurse "
          f"uebersprungen{zusatz}")


def zaehle_luecken(df, spalten=PREISSPALTEN) -> int:
    """Anzahl der Zeilen eines Kurs-DataFrames, denen ein Kurs fehlt."""
    vorhandene = [s for s in spalten if s in df.columns]
    if not vorhandene:
        return 0
    return int(df[vorhandene].isna().any(axis=1).sum())
