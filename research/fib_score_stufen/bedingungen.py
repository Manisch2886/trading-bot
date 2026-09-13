"""
Die drei Bedingungen unter dem `fib_score` - einzeln und stetig
====================================================================
`elliott_wave_counter.fibonacci_score()` addiert drei feste Teilpunkte
(0.34 / 0.33 / 0.33) und rundet auf zwei Stellen:

    score = 0.0
    if 0.5   <= wave2/wave1 <= 0.618: score += 0.34
    if 1.4   <= wave3/wave1 <= 1.8:   score += 0.33
    if 0.236 <= wave4/wave3 <= 0.382: score += 0.33
    return round(score, 2)

Dieses Modul rechnet DIESELBE Bewertung noch einmal, aber offen: es
gibt je Muster die drei Verhaeltnisse, die drei Ja/Nein-Entscheidungen,
die Stufe (0-3) und einen stetigen Abstand zurueck.

WARUM EINE NACHBILDUNG - und warum sie hier erlaubt ist
--------------------------------------------------------------------
Die Randbedingung des Auftrags lautet: die echten Bot-Funktionen
aufrufen, nicht nachbauen. Sie gilt hier unveraendert - Zigzag,
Wellensuche und Trade-Simulation kommen aus dem Bot
(`calculate_zigzag_with_confirmation`, `find_causal_waves`,
`run_backtest`), und der `fib_score` jedes Musters ist der vom Bot
berechnete Wert aus der Spalte `fib_score`.

Nachgebildet wird ausschliesslich die ZERLEGUNG, die der Bot gar nicht
ausgibt: welche der drei Bedingungen erfuellt ist. `fibonacci_score()`
liefert nur die Summe; aus 0,33 laesst sich nicht ablesen, ob die
Welle-3- oder die Welle-4-Bedingung dahintersteht - und genau das ist
die Frage aus Punkt 3 des Auftrags.

Damit die Nachbildung nicht unbemerkt abdriften kann, prueft
`test_stufen.py` sie gegen die echte `fibonacci_score()` des Bots:
auf jedem einzelnen gemessenen Muster beider Bots UND auf
Zufallspunkten. Weicht sie je ab, faellt der Selbsttest.

WAS UNTER DEM SCORE LIEGT (Nebenfrage des Auftrags)
--------------------------------------------------------------------
Alle drei Bedingungen sind Schwellen auf einer STETIGEN Groesse - dem
Verhaeltnis zweier Wellenlaengen. Es sind allerdings INTERVALLE, nicht
"±x % um ein Zielverhaeltnis": `0.5 <= r <= 0.618` hat keinen
ausgezeichneten Mittelpunkt, den der Code als Ziel benennen wuerde.
Die kanonischen Fibonacci-Werte liegen sogar auf den RAENDERN
(0,618 bei Welle 2; 0,382 bei Welle 4) oder unsymmetrisch im Inneren
(1,618 bei Welle 3).

Deshalb wird der Abstand hier auf das Intervall selbst normiert und
nicht auf einen erfundenen Zielwert:

    m = (lo + hi) / 2        Intervallmitte
    h = (hi - lo) / 2        halbe Intervallbreite
    d = |r - m| / h          normierter Abstand

`d <= 1` ist damit gleichbedeutend mit "Bedingung erfuellt", `d = 0`
bedeutet "genau in der Mitte des Intervalls". Aus den drei Abstaenden
ergibt sich die stetige Entsprechung des Scores:

    naehe = ( max(0, 1-d1) + max(0, 1-d2) + max(0, 1-d3) ) / 3

`naehe` liegt in [0, 1], ist 0 genau dann, wenn keine Bedingung
erfuellt ist (Stufe 0), und 1 nur, wenn alle drei Verhaeltnisse exakt
in der Intervallmitte liegen. Die Gewichtung ist bewusst GLEICH
(1/3 je Bedingung) und nicht 0.34/0.33/0.33 - der Unterschied dieser
drei Teilpunkte ist gerade der Gegenstand von Punkt 3 und darf nicht
schon in das stetige Mass eingebaut werden.

Die Alternative - Abstand zum kanonischen Fibonacci-Wert (0,618 /
1,618 / 0,382) - wird in `naehe_fib` zusaetzlich mitgerechnet, damit
die Antwort auf die Nebenfrage nicht an dieser einen Festlegung
haengt. Sie ist normiert auf dieselbe halbe Intervallbreite.
"""

# (Name, Teilpunkte im Bot, Intervall lo, Intervall hi, kanonischer
#  Fibonacci-Wert, Zaehler/Nenner in Wellen)
BEDINGUNGEN = (
    ("w2_w1", 0.34, 0.5,   0.618, 0.618, "Welle 2 / Welle 1"),
    ("w3_w1", 0.33, 1.4,   1.8,   1.618, "Welle 3 / Welle 1"),
    ("w4_w3", 0.33, 0.236, 0.382, 0.382, "Welle 4 / Welle 3"),
)

NAMEN = tuple(b[0] for b in BEDINGUNGEN)

# Die sechs ueberhaupt moeglichen Werte von fibonacci_score(), je Stufe.
# 0.34 kann nur von der ERSTEN Bedingung kommen - daher die Tie-Break-
# Wirkung, die Punkt 3 des Auftrags prueft.
WERTE_JE_STUFE = {0: (0.0,), 1: (0.33, 0.34), 2: (0.66, 0.67), 3: (1.0,)}


def wellenlaengen(points):
    """points = [P0, P1, P2, P3, P4, P5] -> (wave1, wave2, wave3, wave4).

    Identisch zu fibonacci_score(): Welle 5 geht in die Bewertung NICHT
    ein (sie wird dort berechnet, aber nie benutzt)."""
    p0, p1, p2, p3, p4, _p5 = points
    return (abs(p1 - p0), abs(p2 - p1), abs(p3 - p2), abs(p4 - p3))


def verhaeltnisse(points):
    """Die drei stetigen Groessen unter dem Score - oder None, wenn der
    Bot vorzeitig mit 0.0 aussteigt (wave1 == 0 oder wave3 == 0)."""
    wave1, wave2, wave3, wave4 = wellenlaengen(points)
    if wave1 == 0 or wave3 == 0:
        return None
    return {"w2_w1": wave2 / wave1, "w3_w1": wave3 / wave1, "w4_w3": wave4 / wave3}


def erfuellte(points):
    """(bool, bool, bool) - welche der drei Bedingungen gilt."""
    r = verhaeltnisse(points)
    if r is None:
        return (False, False, False)
    return tuple(lo <= r[name] <= hi for name, _p, lo, hi, _f, _t in BEDINGUNGEN)


def stufe(points) -> int:
    """Zahl der erfuellten Bedingungen: 0, 1, 2 oder 3."""
    return int(sum(erfuellte(points)))


def score_nachbildung(points) -> float:
    """Muss auf jedem Punkt exakt das liefern, was der Bot liefert.
    test_stufen.py prueft das gegen die echte fibonacci_score()."""
    r = verhaeltnisse(points)
    if r is None:
        return 0.0
    score = 0.0
    for name, punkte, lo, hi, _f, _t in BEDINGUNGEN:
        if lo <= r[name] <= hi:
            score += punkte
    return round(score, 2)


def stufe_aus_score(score) -> int:
    """Stufe aus dem fertigen `fib_score` - ohne die Wellenpunkte.

    Eindeutig, weil der Wertebereich abgeschlossen ist (TB-20):
    0.0 | 0.33, 0.34 | 0.66, 0.67 | 1.0.
    """
    wert = round(float(score), 2)
    for s, werte in WERTE_JE_STUFE.items():
        if wert in werte:
            return s
    raise ValueError(f"{wert!r} ist kein moeglicher fib_score - "
                     "fibonacci_score() kann nur 0.0/0.33/0.34/0.66/0.67/1.0 liefern.")


def abstaende(points):
    """Normierter Abstand je Bedingung: d <= 1 heisst erfuellt.

    None, wenn der Bot vorzeitig mit 0.0 aussteigt - dort GIBT es keine
    stetige Groesse, auf der ein Abstand definiert waere."""
    r = verhaeltnisse(points)
    if r is None:
        return None
    out = {}
    for name, _p, lo, hi, _f, _t in BEDINGUNGEN:
        m, h = (lo + hi) / 2.0, (hi - lo) / 2.0
        out[name] = abs(r[name] - m) / h
    return out


def abstaende_fib(points):
    """Dasselbe, aber gemessen zum kanonischen Fibonacci-Wert statt zur
    Intervallmitte. Gleiche Normierung (halbe Intervallbreite), damit
    die Groessenordnung vergleichbar bleibt."""
    r = verhaeltnisse(points)
    if r is None:
        return None
    out = {}
    for name, _p, lo, hi, fib, _t in BEDINGUNGEN:
        h = (hi - lo) / 2.0
        out[name] = abs(r[name] - fib) / h
    return out


def _naehe(d):
    if d is None:
        return 0.0
    return sum(max(0.0, 1.0 - d[name]) for name in NAMEN) / 3.0


def naehe(points) -> float:
    """Stetige Entsprechung des Scores, [0, 1] - Intervallmitte als Anker."""
    return _naehe(abstaende(points))


def naehe_fib(points) -> float:
    """Dieselbe Groesse mit dem kanonischen Fibonacci-Wert als Anker."""
    return _naehe(abstaende_fib(points))


# --------------------------------------------------------------------
# Zwei Masse, die NICHT saettigen
# --------------------------------------------------------------------
# `naehe` hat einen Haken, der erst beim Messen auffaellt: `max(0, 1-d)`
# ist fuer JEDES d > 1 gleich null. Alle Muster, bei denen keine der drei
# Bedingungen greift (Stufe 0), bekommen damit denselben Wert 0 - und das
# sind bei beiden Bots 37 % bzw. 42 % aller Muster. Als stetiger
# PRIMAERSCHLUESSEL fuer eine Zuteilungsregel taugt `naehe` deshalb nicht:
# genau dort, wo die Stufe nichts mehr unterscheidet, unterscheidet sie
# auch nichts mehr.
#
# Die beiden folgenden Masse haben diese Stelle nicht:
#
#   gesamtabstand   Mittel der drei normierten Abstaende. Unbeschraenkt
#                   nach oben und damit von der Welle-3-Bedingung
#                   dominiert - w3/w1 kann beliebig gross werden,
#                   w2/w1 und w4/w3 sind faktisch begrenzt.
#   naehe_weich     Mittel von 1/(1+d). Streng fallend in jedem d, immer
#                   in (0, 1], und kein einzelner Ausreisser kann die
#                   Rangfolge an sich reissen. Das ist die Fassung, die
#                   als Primaerschluessel in Frage kaeme.
#
# Beide werden mitgerechnet, damit die Antwort auf die Nebenfrage nicht
# an einer einzigen Formelwahl haengt.

def gesamtabstand(points) -> float:
    """Mittlerer normierter Abstand ueber die drei Bedingungen.
    Klein = nah an allen drei Intervallen. NaN bei entarteten Mustern."""
    d = abstaende(points)
    if d is None:
        return float("nan")
    return sum(d[name] for name in NAMEN) / 3.0


def naehe_weich(points) -> float:
    """Beschraenkte, nirgends saettigende Entsprechung des Scores, (0, 1]."""
    d = abstaende(points)
    if d is None:
        return float("nan")
    return sum(1.0 / (1.0 + d[name]) for name in NAMEN) / 3.0
