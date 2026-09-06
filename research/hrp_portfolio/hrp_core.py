"""
Hierarchical Risk Parity (HRP) - Kernmodul
==========================================================================
Implementiert den Standard-HRP-Algorithmus (Lopez de Prado, "Building
Diversified Portfolios that Outperform Out of Sample", Journal of
Portfolio Management, 2016): hierarchisches Clustering nach
Korrelations-Distanz, Quasi-Diagonalisierung, rekursive Bisektion der
Kapitalzuteilung. Deterministisch - kein trainiertes/lernendes Modell,
keine Zufallskomponente (passt zum regelbasierten "kein ML"-Grundsatz
des Projekts, siehe CLAUDE.md).

Reines Algorithmus-Modul - kennt NICHTS von Bots, Trades oder Datenquellen.
Nimmt ausschliesslich eine Renditen-Matrix (Spalten = Assets/Bots,
Zeilen = Perioden) entgegen und liefert Portfolio-Gewichte zurueck.

Zusaetzlich: Fallback-Logik fuer den Fall, dass die Korrelation fuer
einzelne Paare NICHT belastbar berechnet werden kann (Datenbasis-Vorbehalt,
siehe shared/portfolio_overview.py: mindestens MIN_COMMON_TRADING_DAYS
gemeinsame Handelstage) - HRP wird dann nur auf dem groessten Teil-
Universum angewendet, in dem ALLE Paare eine ausreichende Datenbasis haben;
die restlichen Bots werden zu ihrem normalen 1/N-Anteil gleichgewichtet
beigemischt (siehe blend_with_fallback fuer die genaue Begruendung).
"""
import itertools

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform


def correlation_to_distance(corr: pd.DataFrame) -> pd.DataFrame:
    """Standard-HRP-Distanzmass: dist_ij = sqrt(0.5 * (1 - corr_ij)),
    liegt in [0, 1] - 0 fuer perfekt positiv korrelierte, 1 fuer perfekt
    negativ korrelierte Assets. Symmetrisierung + Clipping gegen
    Gleitkomma-Rauschen (corr sollte exakt symmetrisch sein und Diagonale
    exakt 1.0, kann durch Rundungsfehler minimal abweichen)."""
    dist = np.sqrt(0.5 * (1.0 - corr.clip(-1.0, 1.0)))
    dist = (dist + dist.T) / 2.0
    values = dist.values.copy()
    np.fill_diagonal(values, 0.0)
    return pd.DataFrame(values, index=dist.index, columns=dist.columns)


def get_quasi_diag(link: np.ndarray) -> list:
    """Liefert die Reihenfolge der urspruenglichen Item-Indizes (0..n-1)
    so, wie sie im Dendrogramm nebeneinander liegen wuerden (aehnliche
    Items sind benachbart) - rekursiver Abstieg durch den Merge-Baum der
    scipy-linkage-Matrix, ausgehend von der Wurzel (letzte Zeile =
    letzter/oberster Merge)."""
    link = link.astype(int)
    num_items = link.shape[0] + 1

    def _expand(node_id):
        if node_id < num_items:
            return [node_id]
        row = link[node_id - num_items]
        left, right = int(row[0]), int(row[1])
        return _expand(left) + _expand(right)

    root_id = num_items + link.shape[0] - 1
    return _expand(root_id)


def get_inverse_variance_weights(cov: pd.DataFrame) -> pd.Series:
    """Inverse-Varianz-Gewichtung innerhalb eines Clusters (Standard-
    Baustein von HRP fuer die Cluster-interne Verteilung)."""
    inv_var = 1.0 / np.diag(cov.values)
    return pd.Series(inv_var / inv_var.sum(), index=cov.index)


def get_cluster_variance(cov: pd.DataFrame, items: list) -> float:
    """Varianz eines Clusters UNTER inverse-Varianz-Gewichtung seiner
    Mitglieder - das Mass, mit dem die rekursive Bisektion entscheidet,
    wie das Kapital zwischen zwei Sub-Clustern aufgeteilt wird (weniger
    Kapital fuer den riskanteren/staerker gekoppelten Zweig)."""
    sub_cov = cov.loc[items, items]
    w = get_inverse_variance_weights(sub_cov).values.reshape(-1, 1)
    return (w.T @ sub_cov.values @ w).item()


def recursive_bisection(cov: pd.DataFrame, sorted_items: list) -> pd.Series:
    """Rekursive Bisektion (Kernstueck von HRP): teilt die (durch
    Quasi-Diagonalisierung sortierte) Item-Liste rekursiv in Haelften,
    verteilt das Kapital zwischen den beiden Haelften umgekehrt proportional
    zu deren Cluster-Varianz, bis jedes Item sein Einzelgewicht hat. Anders
    als bei Markowitz-Optimierung wird NIE eine volle Kovarianzmatrix
    invertiert - das macht HRP robust gegenueber (hier bei nur 9 Bots
    ohnehin schon knappen) kleinen Stichproben und singulaeren/instabilen
    Kovarianzmatrizen."""
    weights = pd.Series(1.0, index=sorted_items)
    clusters = [sorted_items]
    while clusters:
        next_clusters = []
        for cluster in clusters:
            if len(cluster) <= 1:
                continue
            mid = len(cluster) // 2
            next_clusters.append(cluster[:mid])
            next_clusters.append(cluster[mid:])
        for i in range(0, len(next_clusters), 2):
            left, right = next_clusters[i], next_clusters[i + 1]
            var_left = get_cluster_variance(cov, left)
            var_right = get_cluster_variance(cov, right)
            total = var_left + var_right
            alpha = 0.5 if total <= 0 else 1.0 - var_left / total
            weights[left] *= alpha
            weights[right] *= (1.0 - alpha)
        clusters = next_clusters
    return weights


def hrp_weights(returns: pd.DataFrame, linkage_method: str = "single") -> pd.Series:
    """Haupteinstiegspunkt: Renditen-Matrix (Spalten = Assets/Bots) ->
    HRP-Gewichte (Series, Summe exakt 1.0, gleiche Reihenfolge wie
    returns.columns). linkage_method='single' ist die im Original-Paper
    (Lopez de Prado 2016) verwendete Methode - siehe BERICHT.md fuer die
    Begruendung dieser Wahl und einen Robustheits-Vergleich mit 'ward'."""
    items = list(returns.columns)
    if len(items) == 1:
        return pd.Series([1.0], index=items)

    corr = returns.corr()
    cov = returns.cov()
    dist = correlation_to_distance(corr)
    condensed = squareform(dist.values, checks=False)
    link = linkage(condensed, method=linkage_method)
    sorted_idx = get_quasi_diag(link)
    sorted_items = [items[i] for i in sorted_idx]

    weights = recursive_bisection(cov, sorted_items)
    return weights.reindex(items)


def find_max_reliable_subset(sufficient_pairs: pd.DataFrame, items: list) -> list:
    """Groesste Teilmenge von 'items', in der JEDES Paar eine ausreichende
    Datenbasis hat (sufficient_pairs.loc[a, b] == True fuer alle Paare a,b
    der Teilmenge) - Brute-Force ueber alle 2^n Teilmengen. Bei bis zu 9
    Bots (2^9 = 512 Teilmengen) voellig unkritisch in der Laufzeit; fuer
    deutlich mehr Bots waere ein Clique-Suchalgorithmus noetig, hier bewusst
    nicht vorgesehen (Scope: aktuell 9 Bots).

    Liefert hoechstens eine Ein-Element-Liste, falls KEIN Paar ausreichend
    Datenbasis hat (ein einzelnes Item erfuellt die Paar-Bedingung
    trivialerweise, da es gar kein Paar bildet) - ein Aufrufer MUSS ein
    Ergebnis mit weniger als 2 Elementen als "kein sinnvolles HRP-
    Teil-Universum" behandeln. Wird ein solches Ein-Element-Ergebnis
    trotzdem an blend_with_fallback() durchgereicht, ist das UNSCHAEDLICH:
    hrp_weights() liefert fuer ein einzelnes Item automatisch Gewicht 1.0,
    blend_with_fallback() skaliert das auf genau 1/N herunter - identisch
    zum normalen Gleichgewichtungs-Fallback, siehe Testfall."""
    n = len(items)
    best = []
    for mask in range(1, 1 << n):
        if bin(mask).count("1") <= len(best):
            continue
        subset = [items[i] for i in range(n) if mask & (1 << i)]
        ok = all(bool(sufficient_pairs.loc[a, b]) for a, b in itertools.combinations(subset, 2))
        if ok:
            best = subset
    return best


def blend_with_fallback(hrp_subset_weights: pd.Series, all_items: list) -> pd.Series:
    """Fallback-Regel fuer Bot-Paare unter der Datenbasis-Schwelle (siehe
    Aufgabenstellung: 'HRP nur auf dem Teil-Universum mit ausreichender
    Datenbasis anwenden, restliche Bots gleichgewichtet beimischen').

    Begruendung der gewaehlten Variante: Bots AUSSERHALB des verlaesslichen
    Teil-Universums behalten GENAU ihr normales 1/N-Gewicht (dieselbe
    Gleichgewichtung wie im bestehenden shared/portfolio_overview.py) -
    es gibt schlicht keine belastbare Grundlage, sie anders zu behandeln,
    und ein Abweichen davon waere eine unbegruendete Vermutung. Das
    verbleibende Kapital (Anteil = Anzahl eingeschlossener Bots / N) wird
    NUR innerhalb des verlaesslichen Teil-Universums gemaess HRP verteilt.
    Das ist die vorsichtigere, methodisch sauberere Variante gegenueber
    z.B. einer Neuverteilung des GESAMTEN Kapitals unter Ignorieren der
    ausgeschlossenen Bots (das wuerde deren Startgewicht implizit
    veraendern, obwohl ueber sie gar keine zusaetzliche Information vorliegt).

    Ergebnis summiert sich exakt auf 1.0, unabhaengig davon, wie viele Bots
    ausgeschlossen wurden."""
    n = len(all_items)
    if n == 0:
        return pd.Series(dtype=float)
    included = list(hrp_subset_weights.index)
    weights = pd.Series(1.0 / n, index=all_items)
    if included:
        scale = len(included) / n
        for b in included:
            weights[b] = float(hrp_subset_weights[b]) * scale
    return weights
