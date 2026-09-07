"""
Kern-Modul der Vertiefungsstudie zu volatility_breakout_crypto
====================================================================
Diese Studie kombiniert ZWEI bereits abgeschlossene Untersuchungen:

  * volatilitäts-skalierte Positionsgrössen  -> research/volatility_scaled_sizing/
  * ATR-Trailing-Stops                       -> research/trailing_stops/

Beide liegen zum Zeitpunkt dieser Studie in noch NICHT gemergten Branches
(PR #18 bzw. PR #21). Dieses Modul importiert sie deshalb nicht, sondern
enthält die benötigten Funktionen als DOKUMENTIERTE ÜBERNAHME - jede
Funktion nennt unten ihre Herkunft. Ein Import über Branch-Grenzen hinweg
wäre nicht reproduzierbar; eine eigene, leicht abweichende Neufassung wäre
schlimmer, weil sie die Vergleichbarkeit zu den Vorgänger-Studien still
zerstören würde.

Dass die Übernahme verhaltensgleich ist, wird NICHT behauptet, sondern
geprüft: `verify_reference.py` rechnet mit diesem Modul die in beiden
Vorgänger-Studien veröffentlichten Kennzahlen für diesen Bot nach
(Baseline, nur Vol-Sizing, nur Trailing-Stop) und vergleicht sie Zahl für
Zahl. Erst wenn das durchläuft, ist irgendein neues Ergebnis dieser Studie
vertrauenswürdig.

WICHTIG - reine Backtest-Untersuchung: dieses Modul wird von KEINEM
Live-Skript importiert und ändert nichts an strategies/.

--------------------------------------------------------------------
Die vier untersuchten Varianten (2x2)
--------------------------------------------------------------------
                     | feste Positionsgrösse | vol-skalierte Grösse
  fester 5 %-Stop    | A  baseline           | B  vol_sizing
  ATR-Trailing-Stop  | C  trailing           | D  combined

Die beiden Mechanismen greifen an unterschiedlichen Stellen an und sind
technisch unabhängig kombinierbar:
  * der Stop bestimmt, WANN eine Position geschlossen wird (und damit
    auch, welche Folgesignale überhaupt entstehen - der Bot kennt kein
    Pyramiding, der nächste Scan startet erst nach dem Ausstieg),
  * die Gewichtung bestimmt, WIE GROSS sie war.
Es gibt daher genau ZWEI Trade-Sätze (fester Stop / ATR-Trailing), auf die
jeweils zwei Gewichtungen gelegt werden.
"""

import numpy as np
import pandas as pd

VARIANT_BASELINE = "baseline"
VARIANT_VOL_SIZING = "vol_sizing"
VARIANT_TRAILING = "trailing"
VARIANT_COMBINED = "combined"
VARIANTS = [VARIANT_BASELINE, VARIANT_VOL_SIZING, VARIANT_TRAILING, VARIANT_COMBINED]

# Welche Variante nutzt welchen Trade-Satz bzw. welche Gewichtung
USES_TRAILING = {VARIANT_BASELINE: False, VARIANT_VOL_SIZING: False,
                 VARIANT_TRAILING: True, VARIANT_COMBINED: True}
USES_VOL_WEIGHTS = {VARIANT_BASELINE: False, VARIANT_VOL_SIZING: True,
                    VARIANT_TRAILING: False, VARIANT_COMBINED: True}

STOP_FIXED_STATIC = "fixed_static"
STOP_ATR_TRAILING = "atr_trailing"


# ===========================================================================
# Teil 1 - ATR und Trailing-Stop
# Übernommen aus research/trailing_stops/atr_core.py (PR #21).
# ===========================================================================
def true_range(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
    """Übernommen aus atr_core.true_range. True Range nach Wilder; für den
    ersten Balken bleibt mangels Vorschlusskurs nur Hoch-Tief."""
    prev_close = np.empty_like(close)
    prev_close[0] = np.nan
    prev_close[1:] = close[:-1]
    return np.fmax(high - low, np.fmax(np.abs(high - prev_close), np.abs(low - prev_close)))


def wilder_atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, length: int) -> np.ndarray:
    """Übernommen aus atr_core.wilder_atr. Methodisch identisch zur
    bestehenden strategies/t3_supertrend/indicators.py::calculate_atr
    (RMA-Glättung, alpha = 1/length, Rekursion ab Balken 0)."""
    tr = true_range(high, low, close)
    atr = np.empty_like(tr, dtype=float)
    alpha = 1.0 / length
    atr[0] = tr[0]
    for i in range(1, len(tr)):
        prev, cur = atr[i - 1], tr[i]
        if not np.isfinite(cur):
            atr[i] = prev
            continue
        atr[i] = prev + alpha * (cur - prev) if np.isfinite(prev) else cur
    return atr


def calibrate_atr_multiplier(atr_at_entry: np.ndarray, entry_price: np.ndarray,
                              target_stop_pct: float):
    """Übernommen aus atr_core.calibrate_atr_multiplier. k so bestimmen, dass
    die MEDIANE anfängliche Stop-Distanz dem bestehenden STOP_LOSS_PCT
    entspricht - k ist damit kein freier Parameter, sondern eine Umrechnung
    des bereits validierten Bot-Werts in die ATR-Skala."""
    if len(atr_at_entry) == 0:
        return None
    ratio = np.asarray(atr_at_entry, dtype=float) / np.asarray(entry_price, dtype=float)
    ratio = ratio[np.isfinite(ratio) & (ratio > 0)]
    if ratio.size == 0:
        return None
    median_ratio = float(np.median(ratio))
    if not np.isfinite(median_ratio) or median_ratio <= 0:
        return None
    return (target_stop_pct / 100.0) / median_ratio


def initial_stop_price(kind: str, entry_price: float, stop_loss_pct: float, k, atr_at_entry):
    """Übernommen aus atr_core.initial_stop_price. Bei ungültigem ATR fällt
    die Trailing-Variante auf die feste Prozent-Distanz zurück, statt den
    Trade still ohne Stop laufen zu lassen."""
    if kind == STOP_ATR_TRAILING and k is not None and atr_at_entry is not None \
            and np.isfinite(atr_at_entry) and atr_at_entry > 0:
        return entry_price - k * atr_at_entry
    return entry_price * (1 - stop_loss_pct / 100.0)


def update_trailing_stop(current_stop: float, running_high: float, kind: str,
                          stop_loss_pct: float, k, atr_now) -> float:
    """Übernommen aus atr_core.update_trailing_stop. RATSCHEN-REGEL: der Stop
    bewegt sich ausschliesslich nach oben - ein Volatilitätsanstieg im
    laufenden Trade darf einen bereits nachgezogenen Stop nicht wieder
    lockern."""
    if kind == STOP_FIXED_STATIC:
        return current_stop
    if atr_now is None or not np.isfinite(atr_now) or atr_now <= 0 or k is None:
        return current_stop
    candidate = running_high - k * atr_now
    return candidate if candidate > current_stop else current_stop


def simulate_exit(high, low, close, atr, entry_idx: int, entry_price: float, kind: str,
                   stop_loss_pct: float, k, max_hold_bars: int) -> dict:
    """
    Übernommen aus atr_core.simulate_exit, reduziert auf die bei
    volatility_breakout_crypto tatsächlich auftretenden Fälle: Stop-Loss
    oder Zeit-Exit exakt nach max_hold_bars Balken (kein Kursziel, kein
    strategie-eigenes Ausstiegssignal). Reicht die Resthistorie für den
    Zeit-Exit nicht, gilt der Trade als nicht abschliessbar - im Original
    bricht der Symbol-Scan dann ab.

    Zwei Festlegungen, die den Vergleich sauber halten (beide aus der
    Trailing-Stop-Studie unverändert übernommen):
      * das laufende Hoch startet beim EINSTIEGSKURS, nicht beim Hoch des
        Einstiegsbalkens (sonst läge der Stop auf einem Kursniveau, das die
        Position nie gesehen hat),
      * der Stop wird erst NACH der Stop-Prüfung desselben Balkens
        nachgezogen (sonst unterstellte man Kenntnis der Reihenfolge von
        Hoch und Tief innerhalb des Balkens).
    """
    n = len(close)
    initial_stop = initial_stop_price(kind, entry_price, stop_loss_pct, k, atr[entry_idx])
    stop_price = initial_stop
    running_high = entry_price
    max_offset = min(max_hold_bars, n - 1 - entry_idx)

    for offset in range(1, max_offset + 1):
        idx = entry_idx + offset

        if low[idx] <= stop_price:
            result = "stop_loss" if stop_price <= initial_stop else "trailing_stop"
            return {"exit_idx": idx, "exit_price": stop_price, "result": result}

        if offset == max_hold_bars:
            return {"exit_idx": idx, "exit_price": close[idx], "result": "time_exit"}

        if high[idx] > running_high:
            running_high = high[idx]
        stop_price = update_trailing_stop(stop_price, running_high, kind, stop_loss_pct, k, atr[idx])

    return {"exit_idx": None, "exit_price": None, "result": "unclosed"}


# ===========================================================================
# Teil 2 - realisierte Volatilität und inverse Vol-Gewichte
# Übernommen aus research/volatility_scaled_sizing/vol_sizing_core.py (PR #18).
# ===========================================================================
def compute_realized_volatility(close: np.ndarray, window: int) -> np.ndarray:
    """
    Übernommen aus vol_sizing_core.compute_realized_volatility, auf NumPy
    umgestellt: rollierende Standardabweichung der Log-Returns über `window`
    Balken, bewusst NICHT annualisiert (der konstante Faktor kürzt sich beim
    späteren Normalisieren auf Mittelwert 1 ohnehin heraus).

    min_periods = max(5, window // 3) - identisch zum Original, damit auch
    die ersten Trades einer Zeitreihe einen Wert bekommen statt verworfen zu
    werden. pandas übernimmt hier die Randbehandlung unverändert.
    """
    series = pd.Series(close)
    log_returns = np.log(series / series.shift(1))
    min_periods = max(5, window // 3)
    return log_returns.rolling(window=window, min_periods=min_periods).std().to_numpy()


def compute_inverse_vol_weights(vols_at_entry: pd.Series, clip_factor: float = 4.0) -> pd.Series:
    """
    Übernommen aus vol_sizing_core.compute_inverse_vol_weights, unverändert.

    Niedrige Volatilität -> grösseres Gewicht. Die rohen 1/vol-Werte werden
    MEDIAN-RELATIV auf [median/clip_factor, median*clip_factor] geclippt
    (nicht perzentil-basiert - das war in der Vorgänger-Studie nicht
    stichprobengrössen-robust), anschliessend auf Mittelwert EXAKT 1.0
    normalisiert. Damit ist die DURCHSCHNITTLICHE Positionsgrösse identisch
    zur festen Allokation - der Vergleich misst die Umverteilung zwischen
    Trades, kein anderes Gesamtrisiko-Niveau.
    """
    inv_vol = 1.0 / vols_at_entry.replace(0, np.nan)
    inv_vol = inv_vol.replace([np.inf, -np.inf], np.nan)

    valid = inv_vol.dropna()
    if valid.empty:
        return pd.Series(1.0, index=vols_at_entry.index)

    median_val = valid.median()
    clipped = inv_vol.clip(lower=median_val / clip_factor, upper=median_val * clip_factor)
    clipped = clipped.fillna(clipped.mean())

    mean_val = clipped.mean()
    if not np.isfinite(mean_val) or mean_val <= 0:
        return pd.Series(1.0, index=vols_at_entry.index)
    return clipped / mean_val


# ===========================================================================
# Teil 3 - Portfolio-Simulation und Kennzahlen
# Übernommen aus vol_sizing_core.simulate_weighted_portfolio (PR #18), das
# seinerseits die in allen 9 Bots gleichlautende simulate_portfolio() um
# einen weights-Parameter erweitert. Mit weights = 1.0 ist das Verhalten
# identisch zur bot-eigenen Funktion.
# ===========================================================================
def simulate_weighted_portfolio(trades: pd.DataFrame, starting_capital: float,
                                 allocation_pct: float, weights: pd.Series = None,
                                 max_concurrent_positions: int = None) -> dict:
    """Ereignisbasierte Kapital-Simulation. Positionsgrösse pro Trade ist
    `capital * allocation_pct * weights[idx]`. allocation_pct ist ein ANTEIL
    (0.10 = 10 %), wie in den Bot-eigenen equity_simulation.py-Skripten."""
    if weights is None:
        weights = pd.Series(1.0, index=trades.index)

    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx))
        events.append((trade["exit_time"], "exit", idx))
    events.sort(key=lambda e: (e[0], e[1] != "exit"))

    capital = starting_capital
    open_positions = {}
    skipped, executed, equity_curve = [], [], []

    for time, event_type, idx in events:
        trade = trades.loc[idx]

        if event_type == "entry":
            if max_concurrent_positions is not None and len(open_positions) >= max_concurrent_positions:
                skipped.append(idx)
                continue
            free_capital = capital - sum(open_positions.values())
            weight = weights.loc[idx] if idx in weights.index else 1.0
            allocation = capital * allocation_pct * weight
            if allocation > free_capital:
                skipped.append(idx)
                continue
            open_positions[idx] = allocation
            executed.append(idx)

        elif event_type == "exit":
            if idx not in open_positions:
                continue
            allocation = open_positions.pop(idx)
            capital += allocation * (trade["pnl_pct"] / 100)
            equity_curve.append({
                "time": time, "symbol": trade["symbol"], "pnl_pct": trade["pnl_pct"],
                "allocation": round(allocation, 2), "capital_after": round(capital, 2),
            })

    return {
        "final_capital": round(capital, 2),
        "num_executed": len(executed),
        "num_skipped": len(skipped),
        "executed_idx": executed,
        "equity_curve": pd.DataFrame(equity_curve),
    }


def calculate_max_drawdown(equity_df: pd.DataFrame, starting_capital: float) -> float:
    """Identisch zur Hilfsfunktion in jedem Bot-eigenen equity_simulation.py."""
    if equity_df.empty:
        return 0.0
    capital_series = pd.concat([pd.Series([starting_capital]), equity_df["capital_after"]], ignore_index=True)
    running_max = capital_series.cummax()
    return round(float(((capital_series - running_max) / running_max * 100).min()), 2)


def calmar_ratio(total_return_pct: float, max_drawdown_pct: float):
    """Calmar-Konvention aller vier Vorgänger-Untersuchungen: Gesamtrendite %
    geteilt durch den Betrag des Max Drawdown % (82,43 / 6,33 = 13,02).
    None bei Drawdown 0 - dort ist die Kennzahl nicht definiert."""
    if max_drawdown_pct is None or abs(max_drawdown_pct) < 1e-12:
        return None
    return round(total_return_pct / abs(max_drawdown_pct), 2)


if __name__ == "__main__":
    print("Reines Bibliotheksmodul - siehe test_vbc_core.py (Sanity-Checks), "
          "verify_reference.py (Regressionscheck gegen beide Vorgänger-Studien) "
          "und run_deepdive.py (eigentliche Analyse).")
