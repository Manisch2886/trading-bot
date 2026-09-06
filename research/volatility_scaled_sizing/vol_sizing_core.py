"""
Kern-Modul: volatilitaets-skalierte Positionsgroessen
============================================================
Reine, strategie-unabhaengige Berechnungslogik - kein Bezug zu einem
bestimmten Bot. Wird von run_one_bot.py fuer alle 9 Bots gleichermassen
genutzt, damit die Methodik ueber den gesamten Vergleich hinweg IDENTISCH
ist (nicht neu erfunden pro Bot).

WICHTIG - reine Backtest-/Recherche-Untersuchung: dieses Modul wird von
KEINEM Live-Skript importiert und aendert nichts an strategies/. Siehe
Aufgabenbeschreibung "Volatilitaets-skalierte Positionsgroessen".

Methodik in Kuerze:
1. Fuer jeden Trade wird die REALISIERTE VOLATILITAET des zugehoerigen
   Symbols AM EINSTIEGSZEITPUNKT geschaetzt (rollierende Standard-
   abweichung der Log-Returns ueber ein festes Fenster VOR dem Einstieg,
   siehe compute_realized_volatility()).
2. Aus der inversen Volatilitaet wird ein Positionsgroessen-GEWICHT pro
   Trade abgeleitet (compute_inverse_vol_weights()) - NIEDRIGE Volatilitaet
   -> GROESSERES Gewicht (groessere Position), HOHE Volatilitaet ->
   kleineres Gewicht. Das Gewicht wird auf Mittelwert EXAKT 1.0
   normalisiert, damit die vol-skalierte Variante im Durchschnitt exakt
   dieselbe Positionsgroesse wie die fixe Baseline nutzt (fairer
   Vergleich, siehe Aufgabenstellung) - eine absolute "Zielvolatilitaet"
   im klassischen Sinn (Risk-Parity-/Vol-Targeting-Literatur) ist dafuer
   NICHT explizit noetig, da sie sich beim Normalisieren auf Mittelwert 1
   rechnerisch ohnehin herauskuerzen wuerde. Nur das VERHAELTNIS der
   Trades zueinander zaehlt.
3. simulate_weighted_portfolio() ist eine Verallgemeinerung der in allen
   9 Bots BYTEGLEICH vorkommenden simulate_portfolio()-Funktion
   (event-basierte Kapital-Simulation, siehe z.B.
   strategies/volatility_breakout/equity_simulation.py) - mit
   weights ≡ 1.0 fuer jeden Trade ist das Verhalten IDENTISCH zur
   bestehenden Funktion (siehe test_vol_sizing_core.py, Regressionstest
   gegen ein Beispiel aus der bestehenden Codebase).
"""

import numpy as np
import pandas as pd


def compute_realized_volatility(price_df: pd.DataFrame, window: int, price_col: str = "close") -> pd.Series:
    """
    Rollierende realisierte Volatilitaet (Standardabweichung der
    Bar-zu-Bar-LOG-Returns) ueber `window` Bars.

    Bewusst NICHT annualisiert - wir brauchen nur eine RELATIVE Kennzahl
    zur Gewichtung zwischen Zeitpunkten/Symbolen, keine absolute,
    jahresbezogene Vergleichsgroesse wie in der klassischen
    Risikoparitaet-Literatur ueblich. Eine Annualisierung wuerde das
    Ergebnis nur mit einem konstanten Faktor (sqrt(Perioden/Jahr))
    skalieren, der sich beim spaeteren Normalisieren auf Mittelwert 1
    (siehe compute_inverse_vol_weights) ohnehin wieder herauskuerzt -
    ausser bei Vergleichen ZWISCHEN unterschiedlichen Bar-Frequenzen
    (z.B. 1h vs. 4h vs. 1d), die hier aber nie auftreten: die
    Volatilitaet wird immer NUR innerhalb einer Zeitreihe fuer EIN
    Symbol verglichen, nie bar-frequenz-uebergreifend gemischt.

    LOG-Returns (nicht einfache prozentuale Returns) - Standard in der
    Volatilitaets-Literatur, symmetrisch fuer Gewinne/Verluste
    (ln(1.10) != -ln(1/1.10), waehrend eine einfache prozentuale
    Betrachtung diese Asymmetrie nicht hat).

    `window` ist die BAR-ANZAHL, nicht Kalendertage - der Aufrufer
    (run_one_bot.py) rechnet die gewuenschte Kalenderzeit (siehe
    WICHTIGE ANNAHME zur Fenstergrösse im Abschlussbericht) je nach
    Bar-Frequenz des jeweiligen Bots (1h/4h/1d) in eine Bar-Anzahl um.

    min_periods = window // 3 (mindestens 5) - liefert bereits fuer die
    ERSTEN Trades einer Zeitreihe einen Wert, statt die kompletten ersten
    `window` Bars komplett zu verwerfen; Trades ohne jede brauchbare
    Vorgeschichte (leerer Wert) werden von compute_inverse_vol_weights()
    ohnehin neutral (Gewicht = Durchschnitt) behandelt.
    """
    log_returns = np.log(price_df[price_col] / price_df[price_col].shift(1))
    min_periods = max(5, window // 3)
    return log_returns.rolling(window=window, min_periods=min_periods).std()


def volatility_at_entry(price_df: pd.DataFrame, entry_time, window: int, price_col: str = "close"):
    """
    Realisierte Volatilitaet AM LETZTEN BAR VOR (oder exakt bei) `entry_time`
    - verhindert Look-Ahead-Bias (die Volatilitaet, die die Positionsgroesse
    bestimmt, darf nur auf Informationen basieren, die zum Einstiegs-
    zeitpunkt bereits bekannt waren). Gibt None zurueck, wenn `entry_time`
    vor dem ersten verfuegbaren Bar liegt oder keine gueltige Vorgeschichte
    existiert.
    """
    vol_series = compute_realized_volatility(price_df, window, price_col)
    mask = price_df["open_time"] <= entry_time
    if not mask.any():
        return None
    idx = price_df.index[mask][-1]
    value = vol_series.loc[idx]
    return float(value) if pd.notna(value) else None


def compute_inverse_vol_weights(vols_at_entry: pd.Series, clip_factor: float = 4.0) -> pd.Series:
    """
    Baut normalisierte inverse-Volatilitaets-Gewichte (Mittelwert EXAKT
    1.0) aus einer Serie realisierter Volatilitaeten je Trade.

    Robustheit gegen Ausreisser: die rohen 1/vol-Werte werden VOR der
    Normalisierung auf [median/clip_factor, median*clip_factor] IHRER
    EIGENEN Verteilung geclippt - MEDIAN-RELATIV, NICHT perzentil-basiert.
    Ein Perzentil-Clip (z.B. [5.,95.]) wurde zunaechst probiert, erwies
    sich aber als NICHT stichprobengroessen-robust: bei einer kleinen
    Stichprobe (z.B. ein einzelnes Walk-Forward-Fenster mit nur wenigen
    Dutzend Trades) liegt der 95.-Perzentilwert selbst schon sehr nah am
    Maximum und schwaecht einen einzelnen Ausreisser kaum ab (siehe
    test_vol_sizing_core.py, das dieses Problem urspruenglich als
    fehlgeschlagenen Sanity-Check aufgedeckt hat - deshalb die Aenderung
    auf einen median-relativen Clip, der unabhaengig von der
    Stichprobengroesse funktioniert). clip_factor=4.0 (Standardwert) ist
    eine dokumentierte, aber letztlich willkuerliche Wahl - siehe
    Abschlussbericht, Abschnitt "Getroffene Annahmen".

    Fehlende Vol-Werte (None/NaN - z.B. ein Trade so frueh in der
    Zeitreihe, dass noch nicht genug Vorgeschichte fuer das
    Volatilitaets-Fenster existiert) bekommen NACH dem Clipping den
    Mittelwert der gueltigen Gewichte zugewiesen - neutral, weder
    bevorzugt noch benachteiligt, analog zur fixen Baseline (Gewicht 1).

    Gibt bei komplett fehlenden/ungueltigen Daten eine Serie von lauter
    1.0 zurueck (degeneriert zur fixen Baseline) statt abzustuerzen.
    """
    inv_vol = 1.0 / vols_at_entry.replace(0, np.nan)
    inv_vol = inv_vol.replace([np.inf, -np.inf], np.nan)

    valid = inv_vol.dropna()
    if valid.empty:
        return pd.Series(1.0, index=vols_at_entry.index)

    median_val = valid.median()
    lo, hi = median_val / clip_factor, median_val * clip_factor
    clipped = inv_vol.clip(lower=lo, upper=hi)
    clipped = clipped.fillna(clipped.mean())

    mean_val = clipped.mean()
    if not np.isfinite(mean_val) or mean_val <= 0:
        return pd.Series(1.0, index=vols_at_entry.index)
    return clipped / mean_val


def simulate_weighted_portfolio(trades: pd.DataFrame, starting_capital: float,
                                 allocation_pct: float, weights: pd.Series = None,
                                 max_concurrent_positions: int = None) -> dict:
    """
    Verallgemeinerte Version der in allen 9 Bots BYTEGLEICH vorkommenden
    simulate_portfolio()-Funktion (siehe z.B.
    strategies/volatility_breakout/equity_simulation.py) - identische
    event-basierte Logik (Ereignisse nach Zeit sortiert, Exits vor
    Entries bei Gleichstand, Kapitalbindungs-/Positionslimit-Pruefung),
    nur um einen `weights`-Parameter erweitert: die Positionsgroesse pro
    Trade ist `capital * allocation_pct * weights[idx]` statt einheitlich
    `capital * allocation_pct`.

    weights=None (oder eine Serie von lauter 1.0) reproduziert das
    Verhalten der bestehenden simulate_portfolio()-Funktionen EXAKT -
    das ist der eingebaute Konsistenz-Check dieses Moduls (siehe
    test_vol_sizing_core.py), der beweist, dass diese Verallgemeinerung
    die bestehende, bereits validierte Baseline-Methodik nicht
    versehentlich veraendert.
    """
    if weights is None:
        weights = pd.Series(1.0, index=trades.index)

    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx))
        events.append((trade["exit_time"], "exit", idx))
    events.sort(key=lambda e: (e[0], e[1] != "exit"))

    capital = starting_capital
    open_positions = {}
    skipped_trades = []
    executed_trades = []
    equity_curve = []

    for time, event_type, idx in events:
        trade = trades.loc[idx]

        if event_type == "entry":
            if max_concurrent_positions is not None and len(open_positions) >= max_concurrent_positions:
                skipped_trades.append(idx)
                continue

            bound_capital = sum(open_positions.values())
            free_capital = capital - bound_capital
            weight = weights.loc[idx] if idx in weights.index else 1.0
            allocation = capital * allocation_pct * weight

            if allocation > free_capital:
                skipped_trades.append(idx)
                continue

            open_positions[idx] = allocation
            executed_trades.append(idx)

        elif event_type == "exit":
            if idx not in open_positions:
                continue
            allocation = open_positions.pop(idx)
            pnl_pct = trade["pnl_pct"]
            result_value = allocation * (1 + pnl_pct / 100)
            capital += (result_value - allocation)

            equity_curve.append({
                "time": time, "symbol": trade["symbol"], "pnl_pct": pnl_pct,
                "allocation": round(allocation, 2), "capital_after": round(capital, 2),
            })

    equity_df = pd.DataFrame(equity_curve)
    return {
        "final_capital": round(capital, 2),
        "num_executed": len(executed_trades),
        "num_skipped": len(skipped_trades),
        "equity_curve": equity_df,
    }


def calculate_max_drawdown(equity_df: pd.DataFrame, starting_capital: float) -> float:
    """Identisch zur bestehenden Hilfsfunktion in jedem Bot-eigenen
    equity_simulation.py (z.B. strategies/volatility_breakout/
    equity_simulation.py:calculate_max_drawdown)."""
    if equity_df.empty:
        return 0.0
    capital_series = pd.concat([pd.Series([starting_capital]), equity_df["capital_after"]], ignore_index=True)
    running_max = capital_series.cummax()
    drawdown_pct = (capital_series - running_max) / running_max * 100
    return round(drawdown_pct.min(), 2)


def average_bound_capital_fraction(equity_df: pd.DataFrame, trades: pd.DataFrame,
                                    weights: pd.Series, allocation_pct: float) -> float:
    """
    Kapitaleffizienz-Nebeneffekt (Aufgaben-Punkt 5): mittlerer Anteil des
    Kapitals, der ueber alle AUSGEFUEHRTEN Trades hinweg pro Position
    gebunden war, relativ zur fixen Baseline-Allokation (allocation_pct).
    Ein Wert > 1.0 bedeutet: die vol-skalierte Variante bindet im
    Durchschnitt MEHR Kapital pro Position als die fixe Baseline (z.B. in
    ruhigen Marktphasen) - relevant fuer die Frage, ob das bestehende
    MAX_CONCURRENT_POSITIONS-Limit dadurch frueher erreicht werden
    koennte. Reine Beobachtung, keine Grenzwert-Pruefung.
    """
    if weights.empty:
        return 1.0
    return round(float(weights.mean()), 4)


if __name__ == "__main__":
    print("Dies ist ein reines Bibliotheksmodul ohne eigenstaendigen Lauf - "
          "siehe test_vol_sizing_core.py fuer Sanity-Checks und "
          "run_one_bot.py <bot_name> fuer die eigentliche Analyse.")
