"""
Rechenkern der Exposure-Messung - reine Funktionen, ohne Dateizugriff
==============================================================================
Alles, was hier steht, ist absichtlich klein und einzeln pruefbar
(`test_exposure_kern.py`, mit Gegenproben nach Prinzip 12 des
Uebergabeprotokolls). Der Bot-Code wird hier NICHT nachgebaut - die
Positionen kommen fertig aus `bot_lauf.py`, das die Original-Funktionen der
Bots aufruft.

WAS HIER "EXPOSURE" HEISST
------------------------------------------------------------------------------
    Brutto-Exposure(Tag) = Summe der Positionsgroessen aller an diesem
                           Kalendertag offenen Positionen
                           ---------------------------------------------
                           angenommenes Gesamtkapital zu Beginn des Tages

Drei Festlegungen, die man kennen muss, um die Zahl richtig zu lesen:

1. **Die Positionsgroessen sind Backtest-Annahmen, kein getracktes Kapital.**
   Sie entstehen in `equity_simulation.simulate_portfolio()` als
   `kapital * ALLOCATION_PCT` (2 % bis 10 % je Bot, aus `live_params.py`).
   Es gibt im Projekt bewusst kein gemeinsames Kapitalkonto
   (Uebergabeprotokoll Abschnitt 2 und 8) - "Gesamtkapital" ist deshalb
   ebenfalls eine Annahme, naemlich die hypothetische Gleichgewichtung.
2. **Kalendertage, nicht Handelstage.** Eine Position, die Freitag offen ist
   und Montag geschlossen wird, ist am Wochenende weiter im Markt. Wer
   Wochenenden herausrechnet, misst die Exposure der Aktien-Bots zu hoch.
   Eine Position gilt vom Einstiegstag bis zum Ausstiegstag als offen,
   beide Tage eingeschlossen.
3. **Der Nenner ist das Kapital zu TAGESBEGINN**, also der Stand nach dem
   letzten Ausstieg VOR diesem Tag. Sonst teilte man die am Morgen
   eingegangene Bindung durch ein Kapital, das die Gewinne desselben Tages
   schon enthaelt.
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Tagesreihen je Bot
# ---------------------------------------------------------------------------

def taegliche_reihen(positionen: pd.DataFrame, startkapital: float) -> pd.DataFrame:
    """Tagesreihe eines Bots: gebundenes Kapital, Anzahl offener Positionen,
    Kapitalstand zu Tagesbeginn und zu Tagesende.

    Erwartet die Spalten aus `bot_lauf.py`: entry_time, exit_time, allocation,
    pnl_pct, capital_after (Kapital NACH diesem Ausstieg).
    """
    if positionen.empty:
        return pd.DataFrame(columns=["gebunden", "n_offen", "kapital_start", "kapital_ende"])

    pos = positionen.copy()
    pos["entry_tag"] = pd.to_datetime(pos["entry_time"]).dt.normalize()
    pos["exit_tag"] = pd.to_datetime(pos["exit_time"]).dt.normalize()

    tage = pd.date_range(pos["entry_tag"].min(), pos["exit_tag"].max(), freq="D")
    lage = pd.Series(np.arange(len(tage)), index=tage)

    gebunden = np.zeros(len(tage))
    n_offen = np.zeros(len(tage))
    von = lage.reindex(pos["entry_tag"]).to_numpy()
    bis = lage.reindex(pos["exit_tag"]).to_numpy()
    for a, b, betrag in zip(von, bis, pos["allocation"].to_numpy()):
        gebunden[a:b + 1] += betrag
        n_offen[a:b + 1] += 1

    # Kapitalstand zu Tagesende: letzter `capital_after` des Tages, sonst
    # fortgeschrieben. Vor dem ersten Ausstieg gilt das Startkapital.
    nach_ausstieg = (pos.sort_values("exit_time")
                        .groupby("exit_tag")["capital_after"].last()
                        .reindex(tage))
    kapital_ende = nach_ausstieg.ffill().fillna(startkapital)
    kapital_start = kapital_ende.shift(1).fillna(startkapital)

    return pd.DataFrame({
        "gebunden": gebunden,
        "n_offen": n_offen.astype(int),
        "kapital_start": kapital_start.to_numpy(),
        "kapital_ende": kapital_ende.to_numpy(),
    }, index=tage)


def exposure_reihe(reihen: pd.DataFrame) -> pd.Series:
    """Brutto-Exposure eines einzelnen Bots als Anteil (1.0 = 100 %)."""
    return reihen["gebunden"] / reihen["kapital_start"]


# ---------------------------------------------------------------------------
# Zusammenfassung mehrerer Bots zu einem gemeinsamen Buch
# ---------------------------------------------------------------------------

def gemeinsames_fenster(reihen_je_bot: dict):
    """Schnittmenge der Zeitraeume - dasselbe Vorgehen wie in
    `strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py`,
    aus dem die urspruengliche -1,43-%-Zahl stammt."""
    start = max(r.index.min() for r in reihen_je_bot.values())
    ende = min(r.index.max() for r in reihen_je_bot.values())
    return start, ende


def kombiniere(reihen_je_bot: dict) -> pd.DataFrame:
    """Gleichgewichtetes Gesamtbuch ueber das gemeinsame Fenster.

    Jeder Bot bekommt zu Fensterbeginn denselben Kapitalanteil (1/N). Danach
    wird NICHT umgeschichtet - genau wie in der urspruenglichen Rechnung, die
    die normierten Kurven schlicht mittelt. Beides ist dieselbe Groesse:
    jede Bot-Reihe wird auf ihren Kapitalstand zu Fensterbeginn normiert und
    mit 1/N gewichtet.

    Ergebnis je Tag:
      kapital   - Kapital des Gesamtbuchs (Fensterbeginn = 100)
      gebunden  - gebundenes Kapital des Gesamtbuchs in denselben Einheiten
      exposure  - gebunden / kapital_start
      n_offen   - Anzahl offener Positionen ueber alle Bots
    """
    start, ende = gemeinsames_fenster(reihen_je_bot)
    tage = pd.date_range(start, ende, freq="D")
    n = len(reihen_je_bot)

    kapital_start = pd.Series(0.0, index=tage)
    kapital_ende = pd.Series(0.0, index=tage)
    gebunden = pd.Series(0.0, index=tage)
    n_offen = pd.Series(0, index=tage)

    for reihen in reihen_je_bot.values():
        teil = reihen.reindex(tage).ffill()
        basis = teil["kapital_start"].iloc[0]
        gewicht = (100.0 / n) / basis
        kapital_start += teil["kapital_start"] * gewicht
        kapital_ende += teil["kapital_ende"] * gewicht
        # gebunden/n_offen werden NICHT fortgeschrieben: ausserhalb der
        # eigenen Historie eines Bots ist sein Buch leer, nicht "wie zuletzt".
        # Im gemeinsamen Fenster kann dieser Fall nicht auftreten (es ist die
        # Schnittmenge), die Unterscheidung steht hier als Absicherung fuer
        # jede andere Verwendung der Funktion.
        roh = reihen.reindex(tage)
        gebunden += roh["gebunden"].fillna(0.0) * gewicht
        n_offen += roh["n_offen"].fillna(0).astype(int)

    return pd.DataFrame({
        "kapital_start": kapital_start,
        "kapital_ende": kapital_ende,
        "gebunden": gebunden,
        "exposure": gebunden / kapital_start,
        "n_offen": n_offen,
    })


# ---------------------------------------------------------------------------
# Kennzahlen
# ---------------------------------------------------------------------------

def max_drawdown_pct(kurve: pd.Series) -> float:
    """Groesster Rueckgang vom laufenden Hoechststand, in Prozent (negativ)."""
    if len(kurve) == 0:
        return 0.0
    hoch = kurve.cummax()
    return float(((kurve - hoch) / hoch * 100).min())


def exposure_kennzahlen(exposure: pd.Series, n_offen: pd.Series) -> dict:
    """Verdichtung der Exposure-Zeitreihe - Mittel, Median, Perzentile und
    die beiden Anteile, die in der Entscheidungsschwelle der Aufgabe stehen."""
    return {
        "tage": int(len(exposure)),
        "mittel_pct": round(float(exposure.mean()) * 100, 2),
        "median_pct": round(float(exposure.median()) * 100, 2),
        "p10_pct": round(float(exposure.quantile(0.10)) * 100, 2),
        "p90_pct": round(float(exposure.quantile(0.90)) * 100, 2),
        "max_pct": round(float(exposure.max()) * 100, 2),
        "anteil_tage_flach_pct": round(float((n_offen == 0).mean()) * 100, 2),
        "anteil_tage_ueber_50_pct": round(float((exposure > 0.50).mean()) * 100, 2),
    }


def drawdown_auf_investiertem_kapital(kombi: pd.DataFrame) -> dict:
    """Zweite Kapitalkurve: nur Tage mit offenen Positionen, normiert auf das
    jeweils EINGESETZTE Kapital.

    Die uebliche Kurve misst den Gewinn eines Tages am Gesamtkapital - also
    auch an dem Teil, der als Kasse danebenliegt. Hier wird er am
    tatsaechlich gebundenen Kapital gemessen:

        r(Tag) = Kapitalveraenderung(Tag) / gebundenes Kapital(Tag)

    und diese Tagesrenditen werden verkettet. Tage ohne offene Position
    kommen gar nicht vor - sie koennen weder Gewinn noch Verlust erzeugen
    und wuerden die Kurve nur strecken.
    """
    veraenderung = kombi["kapital_ende"] - kombi["kapital_start"]
    investiert = kombi["gebunden"]
    aktiv = investiert > 0

    renditen = (veraenderung[aktiv] / investiert[aktiv]).fillna(0.0)
    kurve = (1.0 + renditen).cumprod() * 100

    return {
        "aktive_tage": int(aktiv.sum()),
        "max_drawdown_pct": round(max_drawdown_pct(kurve), 2),
        "endwert": round(float(kurve.iloc[-1]), 2) if len(kurve) else 100.0,
        "kurve": kurve,
    }


# ---------------------------------------------------------------------------
# Gleichgewichteter Buy-and-Hold eines Universums (fuer die Stresstage)
# ---------------------------------------------------------------------------

def bh_tagesrenditen(kurse_je_symbol: dict) -> pd.Series:
    """Gleichgewichteter Buy-and-Hold: Mittel der Tagesrenditen aller Symbole,
    die an diesem Tag einen Kurs haben.

    Bewusst der Mittelwert der Renditen (taeglich gleichgewichtet), nicht die
    Summe der Kurse - die Summe roher Schlusskurse ist genau der Fehler, der
    beim APH-Vorfall die gesamte Portfolio-Summe zu NaN gemacht hat
    (Uebergabeprotokoll 3.3).
    """
    rahmen = pd.DataFrame(kurse_je_symbol).sort_index()
    renditen = rahmen.pct_change()
    return renditen.mean(axis=1, skipna=True).dropna()


def schlechteste_tage(renditen: pd.Series, anteil: float = 0.10) -> pd.DatetimeIndex:
    """Die `anteil` schlechtesten Tage einer Renditereihe."""
    schwelle = renditen.quantile(anteil)
    return renditen.index[renditen <= schwelle]
