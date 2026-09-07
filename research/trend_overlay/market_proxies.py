"""
Referenzwerte fuer den portfolioweiten Trend-Overlay
==========================================================================
Liefert die zwei breiten Marktreferenzen, aus denen das aggregierte
"beide Maerkte im Abwaertstrend"-Signal gebildet wird:

- Krypto: BTC/USDT-Schlusskurs. Dieselbe Wahl wie im bereits bestehenden
  BTC-Regimefilter von t3_supertrend (strategies/t3_supertrend/
  regime_filter.py) - Bitcoin ist im Projekt bereits als Krypto-Markt-
  Referenz etabliert. Bewusst NICHT dessen SuperTrend-Indikator
  uebernommen (das waere eine Wiederholung eines bereits existierenden,
  bot-spezifischen Filters), sondern der in der Aufgabenstellung
  vorgeschlagene einfachere, portfolioweite gleitende Durchschnitt -
  ein bewusst eigenstaendiges, einfacheres Signal auf Portfolio-Ebene.
- Aktien: kein Marktindex-Proxy (z.B. SPY) ist im Projekt bereits
  vorhanden (data/ enthaelt keine Index-Kursdatei) - daher wird, wie von
  der Aufgabenstellung als Fallback vorgeschlagen, ein gleichgewichteter,
  NICHT rebalancierter Durchschnitt aus den bestehenden 150 S&P-500-
  Symbolen (config/sp500_top150.txt) gebildet. Dieselbe Konstruktions-
  Methode wie die gemeinsame Buy-and-Hold-Referenz der vorherigen HRP-
  Untersuchung (research/hrp_portfolio/bh_reference.py) - fuer
  Konsistenz zwischen den drei research/-Untersuchungen.
"""
import os

import pandas as pd

_RESEARCH_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_RESEARCH_DIR))
CONFIG_DIR = os.path.join(_REPO_ROOT, "config")
DATA_DIR = os.path.join(_REPO_ROOT, "data")

CRYPTO_REFERENCE_SYMBOL = "BTCUSDT"
STOCK_SYMBOLS_FILE = os.path.join(CONFIG_DIR, "sp500_top150.txt")

# ANNAHME (siehe BERICHT.md): dieselbe RECENT_YEARS_ONLY=10-Konvention wie
# in den bestehenden Aktien-Bots (z.B. elliott_wave_stocks/
# multi_symbol_optimise.py) - vor 10+ Jahren waren die heutigen Top-150-
# S&P-500-Werte grossteils noch nicht die groessten Firmen der Welt
# (Survivorship Bias). Zusaetzlicher, hier spezifischer Grund: nur so hat
# der Aktien-Proxy einen stabilen, nahezu vollzaehligen Symbol-Bestand ab
# einem FESTEN Ankerdatum - waeren aeltere Jahrzehnte mit einbezogen,
# wuerden neu hinzukommende Boersengaenge ueber die Jahre einzeln in den
# gleichgewichteten Durchschnitt eintreten und dabei je nach ihrem
# eigenen Kursniveau kuenstliche Spruenge im Proxy-Niveau erzeugen (ein
# reines Kompositions-Artefakt, keine echte Marktbewegung) - das waere
# fuer einen TREND-Indikator (der genau auf solche Niveau-Spruenge
# reagieren wuerde) besonders verzerrend.
RECENT_YEARS_ONLY = 10


def _read_symbol_list(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def load_symbol_close_series(symbol: str) -> pd.Series:
    path = os.path.join(DATA_DIR, f"{symbol}_1d.csv")
    if not os.path.exists(path):
        return pd.Series(dtype=float)
    df = pd.read_csv(path, parse_dates=["open_time"])
    df = df.dropna(subset=["close"])
    if df.empty:
        return pd.Series(dtype=float)
    series = df.set_index("open_time")["close"].sort_index()
    return series[~series.index.duplicated(keep="last")]


def load_crypto_reference() -> pd.Series:
    """BTC/USDT-Tagesschlusskurs, ungefiltert ueber die gesamte
    verfuegbare Historie (kein Zuschnitt auf ein bestimmtes Fenster hier -
    das macht der Aufrufer, damit vor Beginn des eigentlichen
    Analysefensters genug Vorlauf fuer die gleitende-Durchschnitt-
    Anlaufphase existiert)."""
    return load_symbol_close_series(CRYPTO_REFERENCE_SYMBOL)


def load_stock_market_proxy() -> pd.Series:
    """Gleichgewichteter, NICHT rebalancierter Index-Proxy aus den S&P-500-
    Symbolen, die bereits am FESTEN Ankerdatum (heute - RECENT_YEARS_ONLY
    Jahre, gerundet auf den naechsten verfuegbaren Handelstag) Kursdaten
    haben - jedes dieser Symbole wird auf SEIN Kursniveau an genau diesem
    gemeinsamen Ankerdatum normiert (Wert 100), erst danach gleichgewichtet
    gemittelt. Anders als eine Normierung auf den jeweils EIGENEN ersten
    Handelstag (das waere fuer eine reine Gesamtrendite-Kennzahl wie in der
    HRP-Buy-and-Hold-Referenz unproblematisch) ist ein GEMEINSAMES
    Ankerdatum hier noetig, weil sonst spaeter hinzukommende Boersengaenge
    einzeln in den Durchschnitt eintreten wuerden und dabei - je nach ihrem
    eigenen Kursniveau bei Eintritt - kuenstliche Niveau-Spruenge erzeugen
    koennten (reines Kompositions-Artefakt, siehe RECENT_YEARS_ONLY-
    Kommentar oben). Symbole, die erst NACH dem Ankerdatum an die Boerse
    gingen, werden komplett ausgeschlossen (nicht partiell ab ihrem
    IPO-Datum aufgenommen) - die konservativere Wahl."""
    symbols = _read_symbol_list(STOCK_SYMBOLS_FILE)
    raw_series = {}
    latest_date = None
    for symbol in symbols:
        series = load_symbol_close_series(symbol)
        if series.empty:
            continue
        raw_series[symbol] = series
        if latest_date is None or series.index.max() > latest_date:
            latest_date = series.index.max()

    if not raw_series or latest_date is None:
        return pd.Series(dtype=float)

    anchor_date = latest_date - pd.DateOffset(years=RECENT_YEARS_ONLY)

    normalised_series = []
    for symbol, series in raw_series.items():
        on_or_after_anchor = series[series.index >= anchor_date]
        if on_or_after_anchor.empty:
            continue
        anchor_price = on_or_after_anchor.iloc[0]
        if anchor_price <= 0:
            continue
        normalised_series.append(on_or_after_anchor / anchor_price * 100.0)

    if not normalised_series:
        return pd.Series(dtype=float)

    combined = pd.concat(normalised_series, axis=1)
    return combined.mean(axis=1, skipna=True).dropna().sort_index()
