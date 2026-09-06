"""
Gemeinsame Buy-and-Hold-Referenz fuer das KOMBINIERTE 9-Bot-Portfolio
==========================================================================
Analog zur buy_and_hold_reference() aus der vorherigen Vol-Sizing-
Untersuchung (research/volatility_scaled_sizing/run_one_bot.py) - dort
wurde je Bot eine gleichgewichtete Buy-and-Hold-Kurve ueber DESSEN eigenes
Symbol-Universum gebildet. Hier, auf Portfolio-Ebene, braucht es EINE
EINZIGE ("gemeinsame") Referenz ueber alle 9 Bots hinweg statt 9 einzelner -
sonst waere kein einheitlicher Vergleichspunkt fuer das kombinierte
Portfolio moeglich.

Gewaehlte Definition (Annahme, siehe BERICHT.md): gleichgewichtetes
Buy-and-Hold ueber die UNION der beiden im Projekt bereits etablierten
Symbol-Universen:
  - config/top25_symbols.txt  (Krypto-Universum, von allen Krypto-Bots
    ueber shared/symbols_config.py gemeinsam genutzt)
  - config/sp500_top150.txt   (Aktien-Universum, von den Aktien-Bots
    gemeinsam genutzt, siehe CLAUDE.md: "Top 150 S&P-500-Werte")
Bewusst NICHT 9 einzelne, bot-spezifische Buy-and-Hold-Kurven gemittelt -
das wuerde Symbole, die von mehreren Bots gleichzeitig gehandelt werden
(alle Krypto-Bots teilen sich dasselbe 25er-Universum, alle Aktien-Bots
dasselbe 150er-Universum), mehrfach werten und so implizit staerker
gewichten als Symbole, die nur in einem Universum vorkommen.

Kein Bezug zu strategies/-Code - liest ausschliesslich direkt aus den
bereits vorhandenen, committeten Tagesdaten in data/<SYMBOL>_1d.csv.
"""
import os

import numpy as np
import pandas as pd

_RESEARCH_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_RESEARCH_DIR))
CONFIG_DIR = os.path.join(_REPO_ROOT, "config")
DATA_DIR = os.path.join(_REPO_ROOT, "data")

CRYPTO_SYMBOLS_FILE = os.path.join(CONFIG_DIR, "top25_symbols.txt")
STOCK_SYMBOLS_FILE = os.path.join(CONFIG_DIR, "sp500_top150.txt")


def _read_symbol_list(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def combined_symbol_universe() -> list:
    """Union aus Krypto- und Aktien-Universum, dedupliziert, Reihenfolge
    stabil (Krypto zuerst, dann Aktien) - fuer Reproduzierbarkeit."""
    crypto = _read_symbol_list(CRYPTO_SYMBOLS_FILE)
    stocks = _read_symbol_list(STOCK_SYMBOLS_FILE)
    seen = set()
    universe = []
    for sym in crypto + stocks:
        if sym not in seen:
            seen.add(sym)
            universe.append(sym)
    return universe


def load_symbol_close_series(symbol: str) -> pd.Series:
    """Taeglicher Schlusskurs eines Symbols aus data/<SYMBOL>_1d.csv -
    leere Series, falls die Datei fehlt (z.B. ein Symbol aus der
    Universums-Liste ohne heruntergeladene Kursdaten in dieser Sandbox)."""
    path = os.path.join(DATA_DIR, f"{symbol}_1d.csv")
    if not os.path.exists(path):
        return pd.Series(dtype=float)
    df = pd.read_csv(path, parse_dates=["open_time"])
    df = df.dropna(subset=["close"])
    if df.empty:
        return pd.Series(dtype=float)
    series = df.set_index("open_time")["close"].sort_index()
    return series[~series.index.duplicated(keep="last")]


def buy_and_hold_curve(date_range: pd.DatetimeIndex) -> tuple:
    """Gleichgewichtete, NICHT rebalancierte Buy-and-Hold-Kurve (Kauf am
    ersten Tag von date_range, halten bis zum letzten Tag) ueber alle
    Symbole der kombinierten Universums-Liste, die in diesem Fenster
    Kursdaten haben. Normiert auf Start=100 (identische Konvention wie die
    Bot-Kapitalkurven in shared/portfolio_overview.py) - "nicht
    rebalanciert" bedeutet hier konkret: die normierten Einzelkurven werden
    OHNE taegliche Neugewichtung gemittelt, ihr eigenes Gewicht im Portfolio
    drieftet also mit der individuellen Performance auseinander, exakt wie
    bei einem einmal gekauften und nie wieder angefassten Depot.

    Symbole ohne durchgehende Kursdaten fuer das GESAMTE Fenster werden
    ausgeschlossen (kein Forward-Fill ueber grosse Luecken hinweg, um eine
    kuenstlich geglaettete Referenzkurve zu vermeiden) - kleinere Luecken
    (z.B. Feiertage bei Aktien) werden befuellt (ffill/bfill), damit Kurven
    unterschiedlicher Handelskalender (Krypto 24/7 vs. Aktien-Boersentage)
    ueberhaupt auf ein gemeinsames taegliches Raster gebracht werden koennen.

    Rueckgabe: (kurve, anzahl_verwendeter_symbole)."""
    universe = combined_symbol_universe()
    normalised_series = []
    used_symbols = []
    for symbol in universe:
        series = load_symbol_close_series(symbol)
        if series.empty:
            continue
        if series.index.min() > date_range.min() or series.index.max() < date_range.max():
            continue
        aligned = series.reindex(date_range).ffill().bfill()
        if aligned.isna().any() or aligned.iloc[0] <= 0:
            continue
        normalised_series.append(aligned / aligned.iloc[0] * 100.0)
        used_symbols.append(symbol)

    if not normalised_series:
        return pd.Series(dtype=float, index=date_range), 0

    combined = sum(normalised_series) / len(normalised_series)
    return combined, len(used_symbols)
