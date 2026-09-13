"""
Statistik ohne scipy
====================================================================
`scipy` ist in der Cloud-Umgebung dieses Projekts nicht installiert
(Hinweis im Auftrag), und das Projekt fuehrt es auch nicht in
requirements.txt. Alles hier Benoetigte ist mit numpy in wenigen
Zeilen zu haben - und hat den Vorteil, dass es keine Verteilungs-
annahme mitbringt.

Alle Verfahren sind bewusst VERTEILUNGSFREI. Trade-Renditen sind
schief (begrenzter Verlust durch den Stop, offenes Gewinnende) und
je Bot nur wenige Dutzend bis wenige Hundert Beobachtungen - ein
t-Test waere hier die falsche Zusicherung.

ZUFALLSZAHLEN: jede Funktion nimmt einen `seed` und benutzt einen
EIGENEN Generator (`numpy.random.default_rng`). Kein globaler Zustand,
keine Abhaengigkeit von der Aufrufreihenfolge - derselbe Aufruf
liefert immer dieselbe Zahl.

CLUSTER: Trades desselben Symbols sind nicht unabhaengig (ein
Marktereignis kann mehrere erzeugen, und beim Aktien-Bot bewegen sich
147 Werte gemeinsam mit dem Markt). `bootstrap_mittelwert` kann
deshalb wahlweise ueber SYMBOLE ziehen statt ueber Trades
(Cluster-Bootstrap). Das Intervall wird dadurch breiter - es ist das
ehrlichere.
"""

import numpy as np

BOOTSTRAP_ZIEHUNGEN = 10000
# Cluster-Ziehungen laufen in Python statt in numpy (je Ziehung werden
# ganze Symbolbloecke zusammengesetzt) und sind entsprechend teurer.
# 2 000 Ziehungen reichen fuer ein 95-%-Perzentilintervall: die
# Perzentilgrenzen schwanken dabei um deutlich weniger als die zweite
# Nachkommastelle, auf die hier gerundet wird.
BOOTSTRAP_CLUSTER_ZIEHUNGEN = 2000
SEED = 20260913          # Datum des Datenstands - feste, nachvollziehbare Wahl


def _rng(seed):
    return np.random.default_rng(SEED if seed is None else seed)


def bootstrap_mittelwert(werte, cluster=None, ziehungen=None,
                         alpha=0.05, seed=None):
    """Perzentil-Bootstrap fuer den Mittelwert.

    cluster=None  -> ueber einzelne Beobachtungen
    cluster=array -> ueber Cluster (z.B. Symbole): es werden ganze
                     Cluster mit Zuruecklegen gezogen.
    """
    werte = np.asarray(werte, dtype=float)
    n = len(werte)
    if n == 0:
        return None
    if n == 1:
        return {"n": 1, "mittelwert": float(werte[0]), "ci_low": None, "ci_high": None,
                "ziehungen": 0, "art": "cluster" if cluster is not None else "trades"}
    if ziehungen is None:
        ziehungen = BOOTSTRAP_ZIEHUNGEN if cluster is None else BOOTSTRAP_CLUSTER_ZIEHUNGEN
    rng = _rng(seed)

    if cluster is None:
        idx = rng.integers(0, n, size=(ziehungen, n))
        mittel = werte[idx].mean(axis=1)
        art = "trades"
    else:
        cluster = np.asarray(cluster)
        gruppen = [werte[cluster == c] for c in np.unique(cluster)]
        k = len(gruppen)
        mittel = np.empty(ziehungen)
        for i in range(ziehungen):
            wahl = rng.integers(0, k, size=k)
            mittel[i] = np.concatenate([gruppen[j] for j in wahl]).mean()
        art = "cluster"

    lo, hi = np.percentile(mittel, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"n": int(n), "mittelwert": float(werte.mean()),
            "ci_low": float(lo), "ci_high": float(hi),
            "ziehungen": int(ziehungen), "art": art}


def bootstrap_differenz(a, b, ziehungen=BOOTSTRAP_ZIEHUNGEN, alpha=0.05, seed=None):
    """Bootstrap-Intervall fuer mean(a) - mean(b), beide Gruppen
    unabhaengig neu gezogen."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if len(a) < 2 or len(b) < 2:
        return None
    rng = _rng(seed)
    ma = a[rng.integers(0, len(a), size=(ziehungen, len(a)))].mean(axis=1)
    mb = b[rng.integers(0, len(b), size=(ziehungen, len(b)))].mean(axis=1)
    diff = ma - mb
    lo, hi = np.percentile(diff, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"n_a": int(len(a)), "n_b": int(len(b)),
            "differenz": float(a.mean() - b.mean()),
            "ci_low": float(lo), "ci_high": float(hi),
            "schliesst_null_ein": bool(lo <= 0.0 <= hi)}


def bootstrap_differenz_cluster(werte_a, cluster_a, werte_b, cluster_b,
                                ziehungen=BOOTSTRAP_CLUSTER_ZIEHUNGEN, alpha=0.05, seed=None):
    """Wie bootstrap_differenz, aber es werden ganze SYMBOLE gezogen.

    Gezogen wird EINE gemeinsame Symbolliste, und aus jedem gezogenen
    Symbol gehen dessen Trades in beide Gruppen ein. Das ist der Punkt:
    haengt der Unterschied an einem einzelnen Symbol, faellt er in den
    Ziehungen, in denen dieses Symbol fehlt, zusammen - und das
    Intervall wird breit."""
    werte_a, werte_b = np.asarray(werte_a, dtype=float), np.asarray(werte_b, dtype=float)
    cluster_a, cluster_b = np.asarray(cluster_a), np.asarray(cluster_b)
    symbole = np.unique(np.concatenate([cluster_a, cluster_b]))
    k = len(symbole)
    if k < 2:
        return None
    je_a = {s: werte_a[cluster_a == s] for s in symbole}
    je_b = {s: werte_b[cluster_b == s] for s in symbole}
    rng = _rng(seed)
    diff = []
    for _ in range(ziehungen):
        wahl = symbole[rng.integers(0, k, size=k)]
        a = np.concatenate([je_a[s] for s in wahl])
        b = np.concatenate([je_b[s] for s in wahl])
        if len(a) == 0 or len(b) == 0:
            continue
        diff.append(a.mean() - b.mean())
    if len(diff) < ziehungen // 2:
        return None
    diff = np.asarray(diff)
    lo, hi = np.percentile(diff, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"differenz": float(werte_a.mean() - werte_b.mean()),
            "ci_low": float(lo), "ci_high": float(hi),
            "schliesst_null_ein": bool(lo <= 0.0 <= hi),
            "symbole": int(k), "gueltige_ziehungen": int(len(diff))}


def weglassprobe(werte_a, cluster_a, werte_b, cluster_b):
    """Jedes Symbol einmal weglassen - bleibt der Unterschied stehen?

    Die direkteste Antwort auf "haengt das an einem einzigen Wert?".
    Liefert die Spanne der Differenz ueber alle Weglassungen und das
    Symbol, dessen Fehlen am meisten ausmacht."""
    werte_a, werte_b = np.asarray(werte_a, dtype=float), np.asarray(werte_b, dtype=float)
    cluster_a, cluster_b = np.asarray(cluster_a), np.asarray(cluster_b)
    symbole = np.unique(np.concatenate([cluster_a, cluster_b]))
    voll = werte_a.mean() - werte_b.mean()
    ergebnisse = {}
    for s in symbole:
        a, b = werte_a[cluster_a != s], werte_b[cluster_b != s]
        if len(a) == 0 or len(b) == 0:
            continue
        ergebnisse[str(s)] = float(a.mean() - b.mean())
    if not ergebnisse:
        return None
    werte = np.asarray(list(ergebnisse.values()))
    kippt_am_meisten = max(ergebnisse, key=lambda s: abs(ergebnisse[s] - voll))
    return {"differenz_voll": float(voll),
            "min": float(werte.min()), "max": float(werte.max()),
            "vorzeichen_bleibt": bool(np.all(np.sign(werte) == np.sign(voll))),
            "weggelassene_symbole": int(len(ergebnisse)),
            "symbol_mit_groesstem_einfluss": kippt_am_meisten,
            "differenz_ohne_dieses_symbol": float(ergebnisse[kippt_am_meisten])}


def permutation_differenz(a, b, ziehungen=BOOTSTRAP_ZIEHUNGEN, seed=None):
    """Zweiseitiger Permutationstest auf Mittelwertunterschied.

    p ist der Anteil der Vertauschungen, deren Unterschied mindestens so
    gross ist wie der beobachtete. Die +1 im Zaehler und Nenner ist die
    uebliche Korrektur - sie verhindert ein p von exakt 0, das es bei
    endlich vielen Ziehungen nicht geben kann."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if len(a) == 0 or len(b) == 0:
        return None
    beobachtet = abs(a.mean() - b.mean())
    alle = np.concatenate([a, b])
    n_a = len(a)
    rng = _rng(seed)
    treffer = 0
    for _ in range(ziehungen):
        rng.shuffle(alle)
        if abs(alle[:n_a].mean() - alle[n_a:].mean()) >= beobachtet - 1e-12:
            treffer += 1
    return {"differenz": float(a.mean() - b.mean()),
            "p_wert": float((treffer + 1) / (ziehungen + 1)),
            "ziehungen": int(ziehungen)}


def _raenge(x):
    """Durchschnittsraenge (Bindungen bekommen den Mittelwert ihrer Raenge)."""
    x = np.asarray(x, dtype=float)
    ordnung = np.argsort(x, kind="stable")
    raenge = np.empty(len(x), dtype=float)
    sortiert = x[ordnung]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and sortiert[j + 1] == sortiert[i]:
            j += 1
        raenge[ordnung[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return raenge


def spearman(x, y):
    """Rangkorrelation nach Spearman, bindungsfest (Pearson auf Raengen).

    Bindungen sind hier der Normalfall - die Stufe nimmt nur vier Werte
    an -, deshalb NICHT die 6*d^2-Kurzformel, die Bindungen nicht
    vertraegt."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if len(x) < 3:
        return None
    rx, ry = _raenge(x), _raenge(y)
    sx, sy = rx.std(), ry.std()
    if sx == 0 or sy == 0:
        return None
    return float(((rx - rx.mean()) * (ry - ry.mean())).mean() / (sx * sy))


def spearman_permutation(x, y, ziehungen=BOOTSTRAP_ZIEHUNGEN, seed=None):
    """Spearman-rho mit zweiseitigem Permutations-p-Wert."""
    rho = spearman(x, y)
    if rho is None:
        return None
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float).copy()
    rng = _rng(seed)
    treffer = 0
    for _ in range(ziehungen):
        rng.shuffle(y)
        r = spearman(x, y)
        if r is not None and abs(r) >= abs(rho) - 1e-12:
            treffer += 1
    return {"rho": float(rho), "p_wert": float((treffer + 1) / (ziehungen + 1)),
            "n": int(len(x)), "ziehungen": int(ziehungen)}


def benoetigte_stichprobe(differenz_pct, streuung_pct, alpha=0.05, macht=0.8):
    """Grobe Faustzahl: wie viele Trades JE GRUPPE braeuchte es, um einen
    Unterschied dieser Groesse mit 80 % Wahrscheinlichkeit zu finden?

    Normalapproximation (n = 2*(z_a/2 + z_b)^2 * s^2 / d^2) - bewusst nur
    als Groessenordnung ausgewiesen, nicht als exakte Planungszahl. Sie
    beantwortet die Frage, die bei einem Nicht-Ergebnis sofort kommt:
    war die Messung ueberhaupt in der Lage, etwas zu finden?"""
    if differenz_pct == 0:
        return None
    z = {0.05: 1.959963985, 0.10: 1.644853627}.get(round(alpha, 2), 1.959963985)
    z_macht = {0.8: 0.841621234, 0.9: 1.281551566}.get(round(macht, 2), 0.841621234)
    return int(np.ceil(2 * (z + z_macht) ** 2 * streuung_pct ** 2 / differenz_pct ** 2))
