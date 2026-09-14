#!/usr/bin/env python3
"""
TB-30a - Kennzahlen der Vorregistrierung
==============================================================================
Alle Rechnungen, die das eingefrorene Auswertungsskript braucht, an einer
Stelle: Netto-Sharpe, Netto-Calmar, die drei tiefsten Drawdowns, die
Beta-Bereinigung (Alpha gegen das gleichgewichtete point-in-time-Universum),
der Zufalls-Timing-Test, die Deflated Sharpe Ratio und das Clustering fuer
N_eff.

KEINE ABHAENGIGKEIT AUSSER numpy/pandas
------------------------------------------------------------------------------
`scipy` ist auf dem Rechner des Nutzers nicht in jeder Umgebung vorhanden
(`research/hrp_portfolio/test_hrp_core.py` scheitert daran). Normalverteilung
und ihre Umkehrung sind deshalb hier ausgerechnet - die Umkehrung nach
Acklam, Genauigkeit rund 1e-9, fuer diesen Zweck weit mehr als noetig.

WAS "NETTO" HEISST
------------------------------------------------------------------------------
Netto heisst: nach Handelskosten. Die Kostenkonvention des Projekts ist
0,30 % je Round-Trip (0,1 % Gebuehr + 0,05 % Slippage je Order, Ein- und
Ausstieg). Die Rohergebnisse liefern bereits Netto-Renditen; diese Datei
zieht nichts zusaetzlich ab. Wer das aendert, aendert die Messkette - und
das ist ein Amendment.
"""

import math

import numpy as np

EULER_MASCHERONI = 0.5772156649015329


# ---------------------------------------------------------------------------
# Normalverteilung ohne scipy
# ---------------------------------------------------------------------------
def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(float(x) / math.sqrt(2.0)))


_A = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
      1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
_B = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
      6.680131188771972e+01, -1.328068155288572e+01]
_C = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
      -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
_D = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
      3.754408661907416e+00]


def norm_ppf(p: float) -> float:
    """Umkehrung der Standardnormalverteilung (Acklam)."""
    p = float(p)
    if not (0.0 < p < 1.0):
        raise ValueError(f"norm_ppf verlangt 0 < p < 1, nicht {p}")
    pl, ph = 0.02425, 1 - 0.02425
    if p < pl:
        q = math.sqrt(-2 * math.log(p))
        return (((((_C[0] * q + _C[1]) * q + _C[2]) * q + _C[3]) * q + _C[4]) * q
                + _C[5]) / ((((_D[0] * q + _D[1]) * q + _D[2]) * q + _D[3]) * q + 1)
    if p > ph:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((_C[0] * q + _C[1]) * q + _C[2]) * q + _C[3]) * q + _C[4]) * q
                 + _C[5]) / ((((_D[0] * q + _D[1]) * q + _D[2]) * q + _D[3]) * q + 1)
    q = p - 0.5
    r = q * q
    return (((((_A[0] * r + _A[1]) * r + _A[2]) * r + _A[3]) * r + _A[4]) * r
            + _A[5]) * q / (((((_B[0] * r + _B[1]) * r + _B[2]) * r + _B[3]) * r
                             + _B[4]) * r + 1)


# ---------------------------------------------------------------------------
# Kapitalpfad-Kennzahlen
# ---------------------------------------------------------------------------
def max_drawdown_pct(renditen) -> float:
    """Max Drawdown eines Kapitalpfades aus Periodenrenditen, in Prozent.

    Gerundet auf zwei Nachkommastellen - wie shared/messkette.py.
    """
    r = np.asarray(renditen, dtype=float)
    if r.size == 0:
        return 0.0
    kapital = np.cumprod(1.0 + r)
    hoch = np.maximum.accumulate(np.concatenate(([1.0], kapital)))[1:]
    return round(float(np.min(kapital / hoch - 1.0) * 100.0), 2)


def gesamtrendite_pct(renditen) -> float:
    r = np.asarray(renditen, dtype=float)
    if r.size == 0:
        return 0.0
    return float(np.prod(1.0 + r) - 1.0) * 100.0


def sharpe(renditen, perioden_je_jahr: int) -> float:
    """Annualisierter Sharpe ohne Zinsabzug.

    Ohne Zinsabzug, weil eine Zinsannahme eine weitere Wahl waere - und die
    Vorregistrierung will genau die nicht. Eine Reihe ohne Streuung hat
    keinen Sharpe; sie liefert 0,0, nicht unendlich.
    """
    r = np.asarray(renditen, dtype=float)
    if r.size < 2:
        return 0.0
    s = float(np.std(r, ddof=1))
    if s == 0.0 or not np.isfinite(s):
        return 0.0
    return float(np.mean(r)) / s * math.sqrt(perioden_je_jahr)


def calmar(rendite_pct: float, drawdown_pct: float) -> float:
    """Calmar = Rendite / |Drawdown|.

    Ein Drawdown von genau 0 kommt nur vor, wenn die Kurve nie gefallen ist.
    Der Calmar ist dort nicht definiert; er liefert 0,0 statt unendlich -
    sonst gewaenne ein Satz, der gar nicht handelt.
    """
    if drawdown_pct == 0.0:
        return 0.0
    return rendite_pct / abs(drawdown_pct)


def drei_tiefste_drawdowns(drawdowns_je_falte) -> float:
    """Mittelwert der drei tiefsten Falten-Drawdowns (Festlegung 3).

    Bei weniger als drei Falten der Mittelwert ueber alle vorhandenen - die
    Zahl heisst dann weiterhin so und wird mit ihrer Faltenzahl berichtet.
    """
    werte = sorted(float(x) for x in drawdowns_je_falte)
    if not werte:
        return 0.0
    return float(np.mean(werte[:3]))


# ---------------------------------------------------------------------------
# Beta-Bereinigung (Abbruchkriterium c)
# ---------------------------------------------------------------------------
def alpha_beta(strategie_renditen, benchmark_renditen, perioden_je_jahr: int) -> dict:
    """Kleinste Quadrate: r_strat = alpha + beta * r_bench.

    `alpha` kommt annualisiert zurueck (Achsenabschnitt x Perioden je Jahr).
    Beide Reihen muessen dieselbe Laenge haben; sie werden vom Aufrufer auf
    gemeinsame Tage gebracht.
    """
    x = np.asarray(benchmark_renditen, dtype=float)
    y = np.asarray(strategie_renditen, dtype=float)
    if x.size != y.size:
        raise ValueError(f"Reihen verschieden lang: {y.size} gegen {x.size}")
    if x.size < 3 or float(np.var(x)) == 0.0:
        return {"alpha_pct_pa": 0.0, "beta": 0.0, "n": int(x.size),
                "bestimmt": False}
    beta = float(np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1))
    alpha = float(np.mean(y) - beta * np.mean(x))
    return {"alpha_pct_pa": alpha * perioden_je_jahr * 100.0,
            "beta": beta, "n": int(x.size), "bestimmt": True}


def konstante_exposure_calmar(benchmark_renditen, exposure: float) -> dict:
    """Rendite, Drawdown und Calmar einer statischen Position gleicher Groesse.

    Das ist die Vergleichsgroesse der zweiten Haelfte von Abbruchkriterium (c):
    "Calmar unter dem der konstanten Exposure".
    """
    r = np.asarray(benchmark_renditen, dtype=float) * float(exposure)
    rendite = gesamtrendite_pct(r)
    dd = max_drawdown_pct(r)
    return {"rendite_pct": rendite, "drawdown_pct": dd,
            "calmar": calmar(rendite, dd)}


# ---------------------------------------------------------------------------
# Zufalls-Timing-Test
# ---------------------------------------------------------------------------
def zufalls_timing(exposure_reihe, benchmark_renditen, perzentil: float = 95.0) -> dict:
    """Dieselbe Zeit im Markt, anderes Timing.

    Die Exposure-Reihe des Parametersatzes wird zyklisch verschoben und auf
    die Benchmark-Renditen gelegt: Zeit im Markt, Exposure-Verteilung und
    Zahl der Positionstage bleiben Balken fuer Balken erhalten, allein die
    LAGE aendert sich. Gerechnet werden ALLE nichttrivialen Verschiebungen -
    kein Ziehen, kein Startwert, keine Wahl. Zurueck kommt das gewuenschte
    Perzentil der so erzeugten Renditen.

    Warum kein Ziehen mit Startwert: ein Startwert ist eine Festlegung mehr,
    die jemand nach dem Lauf noch aendern koennte. Alle Verschiebungen sind
    erschoepfend und damit unstrittig.
    """
    e = np.asarray(exposure_reihe, dtype=float)
    r = np.asarray(benchmark_renditen, dtype=float)
    if e.size != r.size:
        raise ValueError(f"Reihen verschieden lang: {e.size} gegen {r.size}")
    n = e.size
    if n < 3:
        return {"perzentil": perzentil, "wert_pct": 0.0, "verschiebungen": 0,
                "bestimmt": False}
    # Alle Verschiebungen auf einmal: Zeile k ist die um k verschobene Reihe.
    k = np.arange(1, n)
    index = (np.arange(n)[None, :] + k[:, None]) % n
    renditen = np.prod(1.0 + e[index] * r[None, :], axis=1) - 1.0
    return {"perzentil": perzentil,
            "wert_pct": float(np.percentile(renditen * 100.0, perzentil)),
            "median_pct": float(np.median(renditen * 100.0)),
            "verschiebungen": int(n - 1), "bestimmt": True}


# ---------------------------------------------------------------------------
# Deflated Sharpe Ratio
# ---------------------------------------------------------------------------
def erwarteter_maximaler_sharpe(n_versuche: int, sharpe_varianz: float) -> float:
    """E[max SR] unter N unabhaengigen Versuchen (Bailey/Lopez de Prado)."""
    if n_versuche < 2 or sharpe_varianz <= 0:
        return 0.0
    g = EULER_MASCHERONI
    return math.sqrt(sharpe_varianz) * (
        (1 - g) * norm_ppf(1 - 1.0 / n_versuche)
        + g * norm_ppf(1 - 1.0 / (n_versuche * math.e)))


def deflated_sharpe(renditen, n_versuche: int, sharpe_varianz: float) -> dict:
    """DSR des Gewinners bei N Versuchen.

    `renditen` sind die Perioden-Netto-Renditen des Gewinners ueber die
    Selektionsfalten; SR wird NICHT annualisiert, weil die DSR-Formel auf dem
    Sharpe je Beobachtung und der Zahl der Beobachtungen ruht.
    """
    r = np.asarray(renditen, dtype=float)
    if r.size < 4:
        return {"dsr": 0.0, "sr_je_beobachtung": 0.0, "sr_null": 0.0,
                "n_versuche": int(n_versuche), "t": int(r.size), "bestimmt": False}
    s = float(np.std(r, ddof=1))
    if s == 0.0:
        return {"dsr": 0.0, "sr_je_beobachtung": 0.0, "sr_null": 0.0,
                "n_versuche": int(n_versuche), "t": int(r.size), "bestimmt": False}
    sr = float(np.mean(r)) / s
    z = (r - np.mean(r)) / s
    schiefe = float(np.mean(z ** 3))
    woelbung = float(np.mean(z ** 4))
    sr0 = erwarteter_maximaler_sharpe(n_versuche, sharpe_varianz)
    nenner = 1.0 - schiefe * sr + (woelbung - 1.0) / 4.0 * sr * sr
    if nenner <= 0:
        return {"dsr": 0.0, "sr_je_beobachtung": sr, "sr_null": sr0,
                "n_versuche": int(n_versuche), "t": int(r.size), "bestimmt": False}
    stat = (sr - sr0) * math.sqrt(r.size - 1) / math.sqrt(nenner)
    return {"dsr": norm_cdf(stat), "sr_je_beobachtung": sr, "sr_null": sr0,
            "schiefe": schiefe, "woelbung": woelbung,
            "n_versuche": int(n_versuche), "t": int(r.size), "bestimmt": True}


# ---------------------------------------------------------------------------
# Clustering fuer N_eff
# ---------------------------------------------------------------------------
def cluster_anzahl(matrix, schwelle: float = 0.90) -> int:
    """Zahl der Cluster bei Einfachverkettung ueber die Korrelation.

    `matrix` ist eine (Zellen x Falten)-Matrix der Falten-Sharpes. Zwei
    Zellen liegen im selben Cluster, wenn ihre Korrelation ueber die Falten
    mindestens `schwelle` betraegt - transitiv fortgesetzt (Einfachverkettung).

    Zellen ohne Streuung ueber die Falten (alle Werte gleich) haben keine
    definierte Korrelation. Sie bilden EINEN gemeinsamen Cluster: sie sind
    ununterscheidbar, und jede von ihnen einzeln zu zaehlen wuerde N_eff
    aufblaehen - also genau in die falsche Richtung.
    """
    m = np.asarray(matrix, dtype=float)
    if m.ndim != 2 or m.shape[0] == 0:
        return 0
    n = m.shape[0]
    if m.shape[1] < 2:
        return 1
    std = m.std(axis=1)
    beweglich = std > 0
    eltern = list(range(n))

    def wurzel(i):
        while eltern[i] != i:
            eltern[i] = eltern[eltern[i]]
            i = eltern[i]
        return i

    def vereinen(i, j):
        wi, wj = wurzel(i), wurzel(j)
        if wi != wj:
            eltern[max(wi, wj)] = min(wi, wj)

    starre = np.where(~beweglich)[0]
    for i in starre[1:]:
        vereinen(int(starre[0]), int(i))

    idx = np.where(beweglich)[0]
    if idx.size > 1:
        z = (m[idx] - m[idx].mean(axis=1, keepdims=True)) / std[idx][:, None]
        korr = z @ z.T / (m.shape[1] - 1)
        oben = np.triu(korr >= schwelle, k=1)
        for a, b in zip(*np.where(oben)):
            vereinen(int(idx[a]), int(idx[b]))

    return len({wurzel(i) for i in range(n)})
