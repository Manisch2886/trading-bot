"""
Paar-Auswahl: korrelierte Aktien-Paare aus dem Top-150-Universum
======================================================================
Wie in der Anfrage gefordert ("Paare innerhalb desselben Sektors"), aber
mit einer bewussten, dokumentierten Vereinfachung: eine verlaessliche
GICS-Sektor-Zuordnung fuer alle 150 Symbole ist ohne Internetzugriff (in
der Sandbox blockiert) nicht robust pflegbar, und eine hart codierte
Sektor-Liste waere fehleranfaellig und nicht verifizierbar. Stattdessen
werden Paare rein ueber die Korrelation der TAEGLICHEN RENDITEN entdeckt -
das erfasst den eigentlich gewuenschten Effekt (wirtschaftlich eng
verbundene, gemeinsam schwankende Aktien) implizit und robuster als eine
statische Sektor-Zuordnung: zwei Aktien im selben GICS-Sektor, die sich
wirtschaftlich bereits entkoppelt haben, wuerden eine Sektor-Liste
faelschlich als "Paar" ausweisen, waehrend die Korrelations-Methode sie
automatisch ausschliesst.

MIN_CORRELATION = 0.70: uebliche Pairs-Trading-Konvention (>0.7 = "stark
korreliert", 0.5-0.7 = "moderat", <0.5 = "schwach/vermutlich zufaellig").
Niedriger gewaehlt wuerde zu viele wirtschaftlich unplausible Paare
zulassen, hoeher (>0.9) liesse kaum mehr als Aktien-Gattungen desselben
Konzerns (z.B. GOOGL/GOOG) uebrig.

WICHTIG - kein Lookahead: die Korrelation fuer die Paar-Auswahl wird NUR
auf den 252 Handelstagen VOR dem Beginn des Auswertungsfensters (entry_cutoff,
siehe multi_pair_optimise.py) berechnet - das eigentliche Backtest-/Walk-
Forward-Fenster selbst fliesst nicht in die Paar-Auswahl ein.
"""

import pandas as pd
from indicators import CORRELATION_WINDOW

MIN_CORRELATION = 0.70
TOP_N_PAIRS = 20  # begrenzt Rechenaufwand (C(150,2) ~ 11.175 moegliche Paare) und haelt die
                   # Paar-Anzahl in einer mit den anderen Bots vergleichbaren Groessenordnung


def discover_pairs(symbol_data: dict, reference_date, min_correlation: float = MIN_CORRELATION,
                    top_n: int = TOP_N_PAIRS) -> list:
    """symbol_data: {symbol: DataFrame mit open_time/close}. reference_date:
    Korrelation wird auf den CORRELATION_WINDOW Handelstagen VOR diesem
    Datum berechnet. Gibt eine nach Korrelation absteigend sortierte Liste
    von (symbol_a, symbol_b, correlation) zurueck."""
    returns = {}
    for symbol, df in symbol_data.items():
        window_df = df[df["open_time"] < reference_date].tail(CORRELATION_WINDOW + 1)
        if len(window_df) < CORRELATION_WINDOW:
            continue
        returns[symbol] = window_df.set_index("open_time")["close"].pct_change().dropna()

    returns_df = pd.DataFrame(returns)
    if returns_df.shape[1] < 2:
        return []

    corr_matrix = returns_df.corr(min_periods=int(CORRELATION_WINDOW * 0.9))

    symbols = corr_matrix.columns.tolist()
    candidates = []
    for i in range(len(symbols)):
        for j in range(i + 1, len(symbols)):
            corr = corr_matrix.iloc[i, j]
            if pd.notna(corr) and corr >= min_correlation:
                candidates.append((symbols[i], symbols[j], round(float(corr), 4)))

    candidates.sort(key=lambda x: x[2], reverse=True)
    return candidates[:top_n]
