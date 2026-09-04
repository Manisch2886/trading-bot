"""
Paar-Auswahl: korrelierte Krypto-Paare aus dem 25-Coin-Universum
======================================================================
Analog zu pair_rotation_stocks/pair_discovery.py - rein korrelationsbasiert
(Korrelation der taeglichen Renditen ueber die 252 Handelstage VOR dem
Auswertungsfenster). Bei Krypto entfaellt die "Sektor vs. Korrelation"-
Abwaegung der Aktien-Version ohnehin - ein plausibles Ankerpaar wie BTC/ETH
(siehe Anfrage) ist selbst schon "korrelationsbasiert" gedacht, keine
Sektor-Taxonomie fuer Krypto-Coins etabliert.

MIN_CORRELATION = 0.70 (identisch zur Aktien-Version, fuer Vergleichbarkeit).
WICHTIG: Krypto-Coins sind untereinander tendenziell hoeher korreliert als
Aktien (systematisches Beta zu Bitcoin) - das kann dazu fuehren, dass mehr
Coins ueber der Schwelle liegen als bei Aktien. TOP_N_PAIRS begrenzt das
weiterhin auf eine handhabbare, vergleichbare Groessenordnung.
"""

import pandas as pd
from indicators import CORRELATION_WINDOW

MIN_CORRELATION = 0.70
TOP_N_PAIRS = 20


def discover_pairs(symbol_data: dict, reference_date, min_correlation: float = MIN_CORRELATION,
                    top_n: int = TOP_N_PAIRS) -> list:
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
