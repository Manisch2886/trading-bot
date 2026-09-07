"""
Kern-Modul: volatilitaets-kalibrierte (ATR-)Trailing-Stops
================================================================
Reine, strategie-unabhaengige Berechnungslogik - kein Bezug zu einem
bestimmten Bot. Wird von run_one_bot.py fuer ALLE betroffenen Bots
gleichermassen genutzt, damit die Methodik ueber den gesamten Vergleich
hinweg IDENTISCH ist (nicht pro Bot neu erfunden) - dieselbe Aufteilung
wie research/volatility_scaled_sizing/vol_sizing_core.py.

WICHTIG - reine Backtest-/Recherche-Untersuchung: dieses Modul wird von
KEINEM Live-Skript importiert und aendert nichts an strategies/.

--------------------------------------------------------------------
Die drei verglichenen Stop-Varianten
--------------------------------------------------------------------
A) "fixed_static"  - BASELINE. Fester Prozent-Stop, EINMALIG beim
   Einstieg gesetzt und danach unveraendert - exakt das, was die
   betroffenen Bots heute in live_params.py als STOP_LOSS_PCT fahren.

B) "fixed_trailing" - KONTROLL-/ZERLEGUNGSVARIANTE (keine
   Untersuchungs-Kandidatin). Dieselbe FESTE Prozent-Distanz wie die
   Baseline, aber vom laufenden Hoch nachgezogen. Existiert nur, um den
   Gesamteffekt von C in seine zwei Bestandteile zu zerlegen:
   "nachziehen" (B gegenueber A) und "volatilitaets-kalibrierte
   Distanz statt fester Prozentsatz" (C gegenueber B). Ohne diese
   Zerlegung waere ein Unterschied zwischen A und C nicht eindeutig
   einer der beiden Aenderungen zuzuordnen. Dies ist KEINE
   Parameter-Optimierung - B fuehrt keinen neuen freien Parameter ein,
   sondern nutzt exakt den bestehenden STOP_LOSS_PCT-Wert.

C) "atr_trailing" - die eigentlich untersuchte Variante. Stop-Distanz
   = k * ATR(Fenster) des jeweils AKTUELLEN Balkens, nachgezogen vom
   laufenden Hoch seit Einstieg.

--------------------------------------------------------------------
Zwei bewusste Festlegungen, die den Vergleich fair halten
--------------------------------------------------------------------
1. KALIBRIERUNG DES ATR-MULTIPLIKATORS k (calibrate_atr_multiplier):
   k wird NICHT frei gewaehlt/optimiert, sondern so bestimmt, dass die
   MEDIANE anfaengliche Stop-Distanz der ATR-Variante (in % vom
   Einstiegskurs) exakt dem bestehenden festen STOP_LOSS_PCT des
   jeweiligen Bots entspricht. Damit unterscheidet sich C von A/B
   ausschliesslich in der FORM (volatilitaets-abhaengige Streuung der
   Distanz ueber die Trades hinweg + Nachziehen), nicht im mittleren
   NIVEAU der Stop-Weite. Das ist exakt dieselbe Fairness-Konvention
   wie in der Vol-Sizing-Untersuchung, die die inversen
   Volatilitaets-Gewichte auf Mittelwert exakt 1.0 normalisiert hat
   (research/volatility_scaled_sizing/vol_sizing_core.py) - dort wie
   hier soll ein reiner Niveau-Effekt ("insgesamt weitere Stops") das
   eigentlich interessierende Struktur-Signal nicht ueberdecken.
   MEDIAN statt Mittelwert, weil die Verteilung von ATR/Kurs
   rechtsschief ist (einzelne extreme Volatilitaetsphasen) - der
   Mittelwert wuerde von wenigen Ausreissern nach oben gezogen und
   damit die typische Stop-Weite systematisch zu weit einstellen.

2. RATSCHEN-REGEL (update_trailing_stop): der nachgezogene Stop kann
   sich NUR nach oben bewegen, nie nach unten. Ohne diese Regel wuerde
   ein Volatilitaets-Anstieg WAEHREND eines laufenden Trades den Stop
   wieder nach unten verschieben - das waere per Definition kein
   Trailing-Stop mehr, sondern ein beidseitig beweglicher Stop, der im
   Verlustfall nachgibt. Die Ratschen-Regel ist Standard bei
   Trailing-Stops (u.a. Chandelier Exit) und die klar konservativere
   Variante. Konsequenz fuer die Auswertung, im Bericht aufgegriffen:
   die Volatilitaet wirkt dadurch primaer ueber die Stop-Weite ZUM
   EINSTIEGSZEITPUNKT, waehrend eine Volatilitaets-Ausweitung im
   laufenden Trade den Stop nur noch verlangsamt nachziehen, aber
   nicht mehr lockern kann.
"""

import numpy as np
import pandas as pd

# Erkennungs-Strings der drei Varianten (siehe Modul-Docstring)
STOP_FIXED_STATIC = "fixed_static"
STOP_FIXED_TRAILING = "fixed_trailing"
STOP_ATR_TRAILING = "atr_trailing"


def true_range(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
    """
    True Range nach Wilder: max(Hoch-Tief, |Hoch-Vorschluss|, |Tief-Vorschluss|).

    Fuer den ERSTEN Balken existiert kein Vorschlusskurs - dort bleibt
    nur Hoch-Tief uebrig (die beiden anderen Terme sind undefiniert und
    werden uebersprungen, nicht als 0 gewertet). Das ist exakt das
    Verhalten der bereits im Projekt vorhandenen ATR-Implementierung
    strategies/t3_supertrend/indicators.py::calculate_atr, die dafuer
    pandas' NaN-ueberspringendes DataFrame.max(axis=1) nutzt -
    test_atr_core.py prueft die Uebereinstimmung numerisch gegen genau
    diese bestehende Funktion.
    """
    prev_close = np.empty_like(close)
    prev_close[0] = np.nan
    prev_close[1:] = close[:-1]

    hl = high - low
    hc = np.abs(high - prev_close)
    lc = np.abs(low - prev_close)

    tr = np.fmax(hl, np.fmax(hc, lc))  # fmax ignoriert NaN, solange ein Wert gueltig ist
    return tr


def wilder_atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, length: int) -> np.ndarray:
    """
    Average True Range mit Wilder-Glaettung (RMA, alpha = 1/length),
    rekursiv ab dem ersten Balken gestartet - METHODISCH IDENTISCH zur
    bestehenden Projekt-Implementierung
    strategies/t3_supertrend/indicators.py::calculate_atr
    (`tr.ewm(alpha=1/length, adjust=False).mean()`), hier nur auf
    NumPy-Arrays statt pandas, weil sie in dieser Untersuchung pro
    Symbol und pro Balken in einer Schleife abgefragt wird
    (Performance-Lehre aus backtest_trend.py).

    Bewusst KEINE eigene, abweichende ATR-Definition: die Codebase hat
    bereits eine etablierte Konvention, und eine zweite, leicht andere
    ATR-Variante einzufuehren waere genau die Art von stiller
    Methodik-Divergenz, die in diesem Projekt schon einmal als Bug
    aufgefallen ist (doppelte SuperTrend-Implementierung im
    urspruenglichen Pine-Script).

    Rekursion ab Balken 0 heisst: die ersten ~length Balken sind ein
    noch nicht eingeschwungener Schaetzer. Das ist die bestehende
    Projekt-Konvention (auch SuperTrend/ADX starten so) und wird
    deshalb NICHT durch ein kuenstliches NaN-Warmup ersetzt; in der
    Praxis liegt der Einstieg ohnehin weit hinter dem Serienanfang, da
    alle betroffenen Bots eigene, deutlich laengere Indikator-Vorlaeufe
    haben (z. B. 126 Balken Squeeze-Vorlauf, T3/ADX-Glaettung,
    Zigzag-Historie).
    """
    tr = true_range(high, low, close)
    atr = np.empty_like(tr, dtype=float)
    alpha = 1.0 / length

    atr[0] = tr[0]
    for i in range(1, len(tr)):
        prev = atr[i - 1]
        cur = tr[i]
        if not np.isfinite(cur):
            atr[i] = prev
            continue
        atr[i] = prev + alpha * (cur - prev) if np.isfinite(prev) else cur
    return atr


def calibrate_atr_multiplier(atr_at_entry: np.ndarray, entry_price: np.ndarray,
                              target_stop_pct: float) -> float:
    """
    Bestimmt den ATR-Multiplikator k so, dass die MEDIANE anfaengliche
    Stop-Distanz der ATR-Variante (k * ATR / Einstiegskurs, in Prozent)
    exakt dem bestehenden festen STOP_LOSS_PCT des Bots entspricht:

        k = (target_stop_pct / 100) / median(ATR_entry / entry_price)

    Damit ist k KEIN frei gewaehlter, potenziell ueberangepasster
    Parameter, sondern eine reine Umrechnung des bereits validierten
    Bot-Parameters in die ATR-Skala (siehe Modul-Docstring, Punkt 1).

    Gibt None zurueck, wenn keine gueltigen Eingangsdaten vorliegen -
    der Aufrufer behandelt die ATR-Variante dann als nicht auswertbar,
    statt still auf einen Ersatzwert auszuweichen.
    """
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


def initial_stop_price(kind: str, entry_price: float, stop_loss_pct: float,
                        k: float, atr_at_entry: float):
    """
    Stop-Kurs unmittelbar nach Einstieg (long-only - alle betroffenen
    Bots handeln ausschliesslich long).

    Bei "atr_trailing" faellt der Stop auf die feste Prozent-Distanz
    zurueck, falls am Einstiegsbalken kein gueltiger ATR-Wert vorliegt -
    ein Trade ohne jeden Stop waere eine stille, unbeabsichtigte
    Regel-Aenderung und damit die methodisch schlechtere Wahl.
    """
    if kind == STOP_ATR_TRAILING:
        if atr_at_entry is not None and np.isfinite(atr_at_entry) and atr_at_entry > 0 and k is not None:
            return entry_price - k * atr_at_entry
        return entry_price * (1 - stop_loss_pct / 100.0)
    return entry_price * (1 - stop_loss_pct / 100.0)


def update_trailing_stop(current_stop: float, running_high: float, kind: str,
                          stop_loss_pct: float, k: float, atr_now: float) -> float:
    """
    Zieht den Stop nach - nur nach OBEN (Ratschen-Regel, siehe
    Modul-Docstring Punkt 2). Bei "fixed_static" passiert nichts.

    Kandidat:
      fixed_trailing : running_high * (1 - stop_loss_pct/100)
      atr_trailing   : running_high - k * ATR(aktueller Balken)
    """
    if kind == STOP_FIXED_STATIC:
        return current_stop

    if kind == STOP_FIXED_TRAILING:
        candidate = running_high * (1 - stop_loss_pct / 100.0)
    else:
        if atr_now is None or not np.isfinite(atr_now) or atr_now <= 0 or k is None:
            return current_stop
        candidate = running_high - k * atr_now

    return candidate if candidate > current_stop else current_stop


def simulate_exit(high: np.ndarray, low: np.ndarray, close: np.ndarray, atr: np.ndarray,
                   entry_idx: int, entry_price: float, kind: str, stop_loss_pct: float,
                   k: float, max_hold_bars: int, target_price: float = None,
                   extra_exit: np.ndarray = None, time_exit_mode: str = "at_max_offset_only") -> dict:
    """
    Simuliert EINEN long-Trade ab entry_idx auf den nachfolgenden Balken.

    PRIORITAET INNERHALB EINES BALKENS (bewusst identisch zur bereits
    bestehenden Backtest-Logik der betroffenen Bots, damit die Baseline
    dieser Untersuchung deren Ergebnis exakt reproduziert):
      1. Stop-Loss  - Tagestief/Balkentief <= Stop-Kurs, Ausstieg ZUM
         Stop-Kurs (nicht zum Tief - konservative Projekt-Konvention).
      2. Take-Profit (nur Elliott-Wave-Bots) - Balkenhoch >= Zielkurs.
      3. Strategie-eigenes Ausstiegssignal (nur T3/SuperTrend:
         SuperTrend-Drehung oder T3-Crossunder) - Ausstieg zum Schluss.
      4. Zeit-Exit - Ausstieg zum Schlusskurs.

    NACHZIEHEN DES STOPS erst NACH der Stop-Pruefung desselben Balkens.
    Das ist keine Feinheit, sondern verhindert einen Look-Ahead-Fehler
    innerhalb des Balkens: wuerde der Stop zuerst am Hoch DIESES Balkens
    nachgezogen und dann gegen das Tief DESSELBEN Balkens geprueft,
    unterstellte man Kenntnis der Reihenfolge von Hoch und Tief
    innerhalb des Balkens. Exakt dieselbe Reihenfolge nutzt bereits
    strategies/volatility_breakout/experiment_trailing_stop.py.

    time_exit_mode - bildet die drei UNTERSCHIEDLICHEN Zeit-Exit-
    Konventionen der betroffenen Bots ab (nicht vereinheitlicht,
    sondern je Bot originalgetreu):
      "at_max_offset_only" : Zeit-Exit exakt bei Offset == max_hold_bars;
            reicht die Resthistorie dafuer nicht, gilt der Trade als
            nicht abschliessbar (Rueckgabe result="unclosed") - Verhalten
            der beiden Volatility-Breakout-Bots (dort bricht der Scan ab).
      "at_last_available"  : kein Treffer -> Ausstieg zum Schlusskurs des
            LETZTEN verfuegbaren Balkens im Fenster - Verhalten beider
            Elliott-Wave-Bots (.head(max_hold_hours)).
      "none"               : kein Zeit-Exit; ohne Ausstiegssignal bleibt
            der Trade offen und wird verworfen - Verhalten von
            T3/SuperTrend.
    """
    n = len(close)
    initial_stop = initial_stop_price(kind, entry_price, stop_loss_pct, k,
                                       atr[entry_idx] if atr is not None else None)
    stop_price = initial_stop
    # Das laufende Hoch startet beim EINSTIEGSKURS, NICHT beim Hoch des
    # Einstiegsbalkens. Andernfalls wuerde der nachgezogene Stop sich auf
    # ein Kursniveau beziehen, das die Position nie gesehen hat: der
    # Einstieg erfolgt innerhalb/am Ende des Balkens (Wellen-Tiefpunkt bei
    # den Elliott-Bots, Schlusskurs bei den uebrigen), waehrend das
    # Balkenhoch typischerweise VOR dem Einstieg lag. Bei den
    # Elliott-Wave-Bots (Einstieg am Tief des Balkens) laege der
    # anfaengliche Trailing-Stop sonst sogar OBERHALB des Einstiegskurses -
    # ein garantierter, frei erfundener Gewinn. Konservative und einzig
    # korrekte Wahl.
    running_high = entry_price

    if time_exit_mode == "none":
        max_offset = n - 1 - entry_idx
    else:
        max_offset = min(max_hold_bars, n - 1 - entry_idx)

    for offset in range(1, max_offset + 1):
        idx = entry_idx + offset

        if low[idx] <= stop_price:
            # "stop_loss" = der Stop stand noch auf seinem Anfangswert (der
            # Trade lief nie ins Plus), "trailing_stop" = er war bereits
            # nachgezogen. Nur eine Diagnose-Bezeichnung fuer die
            # Ergebnis-Aufschluesselung, ohne Einfluss auf den PnL.
            result = "stop_loss" if stop_price <= initial_stop else "trailing_stop"
            return {"exit_idx": idx, "exit_price": stop_price, "result": result}

        if target_price is not None and high[idx] >= target_price:
            return {"exit_idx": idx, "exit_price": target_price, "result": "take_profit"}

        if extra_exit is not None and extra_exit[idx]:
            return {"exit_idx": idx, "exit_price": close[idx], "result": "signal_exit"}

        if time_exit_mode == "at_max_offset_only" and offset == max_hold_bars:
            return {"exit_idx": idx, "exit_price": close[idx], "result": "time_exit"}

        # Stop erst JETZT nachziehen (siehe Docstring)
        if high[idx] > running_high:
            running_high = high[idx]
        stop_price = update_trailing_stop(stop_price, running_high, kind, stop_loss_pct, k,
                                           atr[idx] if atr is not None else None)

    if time_exit_mode == "at_last_available" and max_offset > 0:
        idx = entry_idx + max_offset
        return {"exit_idx": idx, "exit_price": close[idx], "result": "time_exit"}

    return {"exit_idx": None, "exit_price": None, "result": "unclosed"}


# ---------------------------------------------------------------------------
# Portfolio-Simulation und Kennzahlen
# ---------------------------------------------------------------------------
def simulate_portfolio(trades: pd.DataFrame, starting_capital: float, allocation_pct: float,
                        max_concurrent_positions: int = None) -> dict:
    """
    Ereignisbasierte Kapital-Simulation - UNVERAENDERT uebernommen aus der
    in allen betroffenen Bots gleichlautenden simulate_portfolio()
    (z. B. strategies/t3_supertrend/equity_simulation.py). Bewusst nicht
    neu erfunden: diese Untersuchung veraendert die AUSSTIEGSREGEL, nicht
    das Kapitalmanagement - jede Abweichung hier wuerde den Vergleich
    verfaelschen.

    allocation_pct ist ein ANTEIL (0.10 = 10%), wie in den Bot-eigenen
    equity_simulation.py-Skripten.
    """
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
            allocation = capital * allocation_pct

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

    return {
        "final_capital": round(capital, 2),
        "num_executed": len(executed_trades),
        "num_skipped": len(skipped_trades),
        "equity_curve": pd.DataFrame(equity_curve),
    }


def calculate_max_drawdown(equity_df: pd.DataFrame, starting_capital: float) -> float:
    """Identisch zur bestehenden Hilfsfunktion in jedem Bot-eigenen
    equity_simulation.py."""
    if equity_df.empty:
        return 0.0
    capital_series = pd.concat([pd.Series([starting_capital]), equity_df["capital_after"]], ignore_index=True)
    running_max = capital_series.cummax()
    drawdown_pct = (capital_series - running_max) / running_max * 100
    return round(float(drawdown_pct.min()), 2)


def calmar_ratio(total_return_pct: float, max_drawdown_pct: float):
    """
    Calmar-Ratio in DERSELBEN Konvention wie in den drei bereits
    abgeschlossenen Untersuchungen (Vol-Sizing, HRP, Trend-Overlay):
    Gesamtrendite in % geteilt durch den BETRAG des maximalen
    Drawdowns in % (z. B. 82,43 % / 6,33 % = 13,02).

    Rueckgabe None bei einem Drawdown von exakt 0 - die Kennzahl ist
    dort nicht definiert und wird im Bericht als "n/a" gefuehrt, statt
    sie durch einen Ersatz-Nenner kuenstlich endlich zu machen.
    """
    if max_drawdown_pct is None or abs(max_drawdown_pct) < 1e-12:
        return None
    return round(total_return_pct / abs(max_drawdown_pct), 2)


if __name__ == "__main__":
    print("Reines Bibliotheksmodul - siehe test_atr_core.py fuer die Sanity-Checks "
          "und run_one_bot.py <bot_name> fuer die eigentliche Analyse.")
