"""
Portfolioweiter Trend-Overlay - Kernmodul
==========================================================================
Reines Signal-/Rechen-Modul - kennt NICHTS von Bots, Datenquellen oder
Dateipfaden. Nimmt Kurs- bzw. Renditen-Serien entgegen und liefert
Trend-Signale bzw. eine Overlay-angepasste Renditenserie zurueck.

Kein Look-Ahead-Bias: compute_moving_average() nutzt pandas' rolling()
mit ausschliesslich BACKWARD-schauendem Fenster - der Wert an Position T
haengt nur von Kursen bis EINSCHLIESSLICH T ab, nie von spaeteren Werten
(siehe test_trend_core.py, expliziter Regressionstest: eine Aenderung
zukuenftiger Kurse darf vergangene MA-/Signal-Werte nicht veraendern).
"""
import numpy as np
import pandas as pd


def compute_moving_average(price: pd.Series, window: int) -> pd.Series:
    """Einfacher gleitender Durchschnitt (SMA) - rolling() ist in pandas
    IMMER backward-schauend (der Wert bei Index i nutzt price[i-window+1:i+1]),
    kein Look-Ahead. min_periods=window (nicht kleiner) ist bewusst: ein
    "gleitender Durchschnitt" aus z.B. nur 50 von 200 noetigen Tagen waere
    kein valider 200-Tage-Trend-Indikator, sondern eine irrefuehrende
    Naeherung - lieber ehrlich NaN (= Signal noch nicht definierbar) als
    ein verzerrter Fruehwert (konsistent mit dem in der Aufgabenstellung
    geforderten "im Zweifel die vorsichtigere Variante")."""
    return price.rolling(window=window, min_periods=window).mean()


def compute_downtrend_signal(price: pd.Series, window: int) -> pd.Series:
    """True an Tagen, an denen der Kurs UNTER seinem eigenen N-Tage-
    gleitenden-Durchschnitt liegt ("Abwaertstrend"). Tage vor Ablauf des
    Anlauffensters (MA noch nicht definiert) werden ALS NICHT-Abwaertstrend
    behandelt (False, nicht NaN/True) - ANNAHME (siehe BERICHT.md):
    ohne einen belastbaren gleitenden Durchschnitt gibt es keine
    Grundlage, einen Abwaertstrend zu behaupten; die vorsichtigere Wahl
    ist, in dieser Anlaufphase KEINE Reduktion vorzunehmen (volle
    Exponierung), nicht implizit eine zu unterstellen."""
    ma = compute_moving_average(price, window)
    signal = price < ma
    return signal.fillna(False)


def combine_signals_and(signal_a: pd.Series, signal_b: pd.Series) -> pd.Series:
    """Aggregiertes 'BEIDE Maerkte im Abwaertstrend'-Signal - logisches
    UND, exakt wie in der Aufgabenstellung gefordert (nicht ODER: ein
    isolierter Abwaertstrend in nur einem Markt soll NICHT auslösen)."""
    aligned_a, aligned_b = signal_a.align(signal_b, join="outer", fill_value=False)
    return aligned_a & aligned_b


def apply_overlay_to_returns(daily_returns: pd.Series, signal: pd.Series,
                              exposure_during_signal: float) -> pd.Series:
    """Skaliert die taeglichen Portfolio-Renditen an Tagen, an denen das
    Signal aktiv ist, um den Faktor exposure_during_signal (z.B. 0.5 fuer
    "auf 50% Kapitaleinsatz reduziert", 0.0 fuer "komplett pausiert") -
    dieselbe lineare Skalierungs-Annahme wie bei der Positionsgroessen-
    Skalierung in der vorherigen Vol-Sizing-Untersuchung (kleinere
    Exponierung -> proportional kleinere taegliche Rendite, sowohl bei
    Gewinn- als auch bei Verlusttagen). An Tagen ohne aktives Signal bleibt
    die Rendite unveraendert (Faktor 1.0)."""
    signal_aligned = signal.reindex(daily_returns.index).fillna(False)
    factor = np.where(signal_aligned.values, exposure_during_signal, 1.0)
    return daily_returns * factor


def signal_active_stats(signal: pd.Series) -> dict:
    """Deskriptive Kennzahlen zur Aktivitaet des Signals - wie oft/wie
    lange war es historisch aktiv (Aufgaben-Vorgabe Punkt 3)."""
    total_days = len(signal)
    active_days = int(signal.sum())
    if total_days == 0:
        return {"total_days": 0, "active_days": 0, "active_pct": 0.0, "num_episodes": 0,
                "longest_episode_days": 0}

    # Episoden = zusammenhaengende Bloecke von True-Werten
    active_int = signal.astype(int)
    changes = active_int.diff().fillna(active_int.iloc[0])
    episode_starts = changes[changes == 1].index
    num_episodes = len(episode_starts)

    longest = 0
    current = 0
    for v in active_int.values:
        if v:
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    return {
        "total_days": total_days,
        "active_days": active_days,
        "active_pct": round(100.0 * active_days / total_days, 2),
        "num_episodes": int(num_episodes),
        "longest_episode_days": int(longest),
    }
