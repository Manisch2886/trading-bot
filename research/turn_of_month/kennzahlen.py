#!/usr/bin/env python3
"""
TB-33 - Bootstrap und Platzhalter-Verteilung
==============================================================================
Zwei Verfahren, beide mit festem Startwert aus dem Register. Der feste
Startwert ist kein Detail: ohne ihn gibt es keine Wiederholbarkeit, und
Wiederholbarkeit ist Pfadkriterium **P7**.

OHNE scipy
------------------------------------------------------------------------------
Beides ist mit numpy allein gerechnet. Das ist Absicht: `scipy` fehlt in
manchen Umgebungen (auch in der, in der dieser Lauf entstanden ist), und ein
Nulltest des Weges sollte nicht an einer Abhaengigkeit scheitern, die er
nicht braucht. Perzentilmethode statt t-Verteilung - fuer einen
Ereignis-Mittelwert ist sie ohnehin die ehrlichere Wahl, weil sie keine
Normalverteilung unterstellt.

TEST 2 - WAS DIE PLATZHALTER-VERTEILUNG IST
------------------------------------------------------------------------------
Nicht "investiert gegen nicht investiert", sondern **"genauso oft und
genauso lange investiert, nur an anderen Tagen"**. Je Ziehung werden genauso
viele Fenster derselben Laenge gezogen, wie es Kernereignisse gibt,
ueberschneidungsfrei innerhalb der Ziehung, mit denselben Kosten.

Das IST die Beta-Bereinigung. Wenn das Turn-of-Month-Fenster nur deshalb
positiv ist, weil das Instrument ueber zwanzig Jahre gestiegen ist, liegt sein
Mittelwert mitten in dieser Verteilung - und der Effekt ist nichts.
"""

import numpy as np


def bootstrap_intervall(werte, ziehungen, seed, niveau):
    """(unten, oben, mittelwert) - Perzentilmethode auf EREIGNISEBENE.

    Gezogen werden die Ereignisse mit Zuruecklegen, nicht die Tage: ein
    Ereignis ist die Beobachtungseinheit, und ein Bootstrap auf Tagesebene
    wuerde die vier Tage eines Fensters auseinanderreissen.
    """
    x = np.asarray(werte, dtype=float)
    if len(x) == 0:
        return None, None, None
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(ziehungen, len(x)))
    mittel = x[idx].mean(axis=1)
    rand = (1.0 - niveau) / 2.0 * 100.0
    return (float(np.percentile(mittel, rand)),
            float(np.percentile(mittel, 100.0 - rand)),
            float(x.mean()))


def platzhalter_verteilung(alle_renditen, n_ereignisse, laenge, ziehungen, seed):
    """Die Mittelwerte von `ziehungen` Zufallsauswahlen gleicher Groesse.

    `alle_renditen` ist die Netto-Rendite JEDES moeglichen Fensters dieser
    Laenge, indiziert nach Startposition. Innerhalb einer Ziehung duerfen
    sich die Fenster nicht ueberschneiden - sonst waere die Verteilung
    kuenstlich eng, und das Perzentil des Kernfensters kaeme zu hoch heraus.

    WIE UEBERSCHNEIDUNGSFREI GEZOGEN WIRD
    -----------------------------------------------------------------------
    Nicht durch Ablehnen und Neuziehen. Eine Ablehnungsschleife ist bei
    dichter Belegung langsam und - schlimmer - nicht gleichverteilt: sie
    bevorzugt die Lagen, die eine gierige Auswahl zuerst findet.

    Stattdessen die exakte Konstruktion: n Startpunkte ohne Zuruecklegen aus
    einem um (n-1)*(laenge-1) verkuerzten Indexraum ziehen, sortieren, und
    auf den i-ten Punkt (i-1)*(laenge-1) addieren. Das bildet die verkuerzten
    Auswahlen **eineindeutig** auf die ueberschneidungsfreien Lagen ab - jede
    gueltige Lage bekommt dieselbe Wahrscheinlichkeit, und es gibt keinen
    Fall, in dem weniger als n Fenster herauskommen.
    """
    starts = np.asarray(alle_renditen["start"], dtype=int)
    werte = np.asarray(alle_renditen["netto_rendite"], dtype=float)
    m, n = len(starts), int(n_ereignisse)
    if m == 0 or n <= 0:
        return np.array([])
    # So viele ueberschneidungsfreie Fenster passen ueberhaupt hinein?
    frei = m - (n - 1) * (laenge - 1)
    if frei < n:
        # Mehr Ereignisse als Platz - dann gibt es keine Vergleichsverteilung,
        # und eine erfundene waere schlimmer als keine.
        return np.array([])
    rng = np.random.default_rng(seed)
    versatz = np.arange(n) * (laenge - 1)
    mittel = np.empty(ziehungen, dtype=float)
    for z in range(ziehungen):
        roh = np.sort(rng.choice(frei, size=n, replace=False))
        mittel[z] = werte[roh + versatz].mean()
    return mittel


def perzentil_von(wert, verteilung):
    """Auf welchem Perzentil der Verteilung liegt `wert`?"""
    v = np.asarray(verteilung, dtype=float)
    if len(v) == 0:
        return None
    return float((v < wert).mean() * 100.0)


def median(werte):
    x = np.asarray(werte, dtype=float)
    return float(np.median(x)) if len(x) else None
