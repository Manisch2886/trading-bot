"""
Rechenkern der Haltedauer- und Ueberlappungsmessung (TB-24)
==============================================================================
Reine Funktionen, kein Dateizugriff. Der Bot-Code wird hier NICHT nachgebaut -
die Positionen kommen fertig aus `positionen_holen.py`, das die
Original-Funktionen der Bots aufruft. Gegenproben zu jeder Behauptung:
`test_haltedauer_kern.py` (Uebergabeprotokoll Prinzip 12).

DIE DREI FESTLEGUNGEN, DIE MAN KENNEN MUSS
------------------------------------------------------------------------------
1. **Haltedauer in Kalendertagen**, als exakte Differenz
   `exit_time - entry_time` in Tagen (mit Bruchteil). Die neun Bots laufen auf
   drei Zeitrahmen (1h, 4h, 1d); nur eine Kalenderangabe ist zwischen ihnen
   vergleichbar. Fuer die sieben Tages-Bots sind die Werte ganzzahlig, weil
   dort beide Zeitstempel auf Mitternacht liegen.
   Die **Kerzenzahl** steht als eigene Spalte daneben - sie wird in
   `positionen_holen.py` aus der Kursreihe GEZAEHLT, nicht hier umgerechnet.
   Wochenenden und Feiertage stecken damit in den Kalendertagen der
   Aktien-Bots, aber nicht in ihrer Kerzenzahl. Das ist der Unterschied
   zwischen "wie lange im Markt" und "wie viele Entscheidungen des Bots".

2. **Eine Position gilt vom Einstiegstag bis zum Ausstiegstag als offen,
   beide Tage eingeschlossen** - dieselbe Festlegung wie in
   `research/exposure_messung/exposure_kern.py`. Wer Wochenenden
   herausrechnet, misst die Ueberlappung der Aktien-Bots zu niedrig.

3. **Jede Paarzahl gilt nur im gemeinsamen Fenster beider Bots.** Die neun
   Bots haben verschieden lange Historien (2016 bis 2022 als Startjahre).
   Ohne Fensterschnitt wuerde ein spaeter startender Bot als "ueberlappt
   selten" erscheinen, obwohl er zu seiner Zeit staendig ueberlappt.
"""

import numpy as np
import pandas as pd

# Fuer die Frage "reagieren zwei Bots auf dasselbe Ereignis": Fenster in
# Kalendertagen, in dem zwei Einstiege im selben Titel als "nacheinander"
# gelten. Aus der Aufgabenstellung uebernommen (drei Tage), nicht gewaehlt.
NAEHE_TAGE = 3


# ---------------------------------------------------------------------------
# 1. Haltedauern
# ---------------------------------------------------------------------------

def haltedauer_tage(positionen: pd.DataFrame) -> pd.Series:
    """Haltedauer je Position in Kalendertagen (exakt, mit Bruchteil)."""
    ein = pd.to_datetime(positionen["entry_time"])
    aus = pd.to_datetime(positionen["exit_time"])
    return (aus - ein) / pd.Timedelta(days=1)


def kennzahlen(werte) -> dict:
    """Verteilungs-Kennzahlen einer Haltedauer-Reihe.

    Median und Perzentile statt nur des Mittelwerts, weil die Verteilungen
    hier schief sind: ein einzelner sehr langer Trade zieht den Mittelwert,
    nicht den Median.
    """
    s = pd.Series(werte, dtype="float64").dropna()
    if s.empty:
        return {"n": 0}
    return {
        "n": int(s.size),
        "min": float(s.min()),
        "p10": float(s.quantile(0.10)),
        "q1": float(s.quantile(0.25)),
        "median": float(s.median()),
        "q3": float(s.quantile(0.75)),
        "p90": float(s.quantile(0.90)),
        "max": float(s.max()),
        "mittel": float(s.mean()),
    }


def kennzahlen_je_ausstiegsart(positionen: pd.DataFrame) -> dict:
    """Dieselben Kennzahlen, getrennt nach der Ausstiegsart des Bots
    (`result`: stop_loss, take_profit, time_exit, sma_exit, trend_flip,
    t3_crossunder). Ein Stop-Loss nach zwei Tagen sagt etwas anderes als ein
    Zeitausstieg nach fuenfzehn."""
    if "result" not in positionen.columns:
        return {}
    tage = haltedauer_tage(positionen)
    ergebnis = {}
    for art, teil in positionen.groupby(positionen["result"].astype(str)).groups.items():
        ergebnis[str(art)] = kennzahlen(tage.loc[teil])
    return ergebnis


def histogramm(werte, kanten) -> pd.Series:
    """Anzahl je Haltedauer-Klasse. `kanten` sind die linken Grenzen; die
    letzte Klasse ist nach oben offen. Klassen sind links geschlossen,
    rechts offen."""
    s = pd.Series(werte, dtype="float64").dropna()
    grenzen = list(kanten) + [np.inf]
    namen = []
    for i, links in enumerate(kanten):
        rechts = grenzen[i + 1]
        namen.append(f">= {links:g}" if np.isinf(rechts) else f"{links:g} bis < {rechts:g}")
    zaehler = [int(((s >= grenzen[i]) & (s < grenzen[i + 1])).sum()) for i in range(len(kanten))]
    return pd.Series(zaehler, index=namen)


def zweigipfligkeit(positionen: pd.DataFrame) -> dict:
    """Hat die Verteilung zwei Gruppen, und trennen die Ausstiegsarten sie?

    Gemessen ohne Verteilungsannahme und ohne scipy (in dieser Umgebung nicht
    installiert): je Ausstiegsart der Median, dazu die Frage, ob sich die
    Quartilsbereiche (Q1..Q3) der beiden haeufigsten Arten ueberhaupt
    ueberschneiden. Keine Ueberschneidung heisst: die Ausstiegsart ist die
    Trennlinie, die Verteilung ist zweigipflig. Ueberschneidung heisst: der
    Unterschied der Mediane liegt innerhalb der Streuung, die Verteilung ist
    nicht in zwei Gruppen zerlegbar.
    """
    je_art = kennzahlen_je_ausstiegsart(positionen)
    if len(je_art) < 2:
        return {"arten": je_art, "zwei_gruppen": False,
                "begruendung": "nur eine Ausstiegsart"}

    haeufigste = sorted(je_art.items(), key=lambda kv: -kv[1]["n"])[:2]
    (name_a, a), (name_b, b) = haeufigste
    getrennt = bool(a["q3"] < b["q1"] or b["q3"] < a["q1"])
    return {
        "arten": je_art,
        "vergleich": [name_a, name_b],
        "zwei_gruppen": getrennt,
        "begruendung": (
            f"{name_a} Q1..Q3 = {a['q1']:.2f}..{a['q3']:.2f} Tage, "
            f"{name_b} Q1..Q3 = {b['q1']:.2f}..{b['q3']:.2f} Tage - "
            + ("keine Ueberschneidung" if getrennt else "Ueberschneidung")
        ),
    }


# ---------------------------------------------------------------------------
# 2. Tageskalender je Bot
# ---------------------------------------------------------------------------

def positionstage(positionen: pd.DataFrame) -> pd.DatetimeIndex:
    """Alle Kalendertage, an denen der Bot mindestens eine Position haelt."""
    tage = _tage_je_position(positionen)
    if not tage:
        return pd.DatetimeIndex([])
    return pd.DatetimeIndex(sorted({t for _symbol, t in tage}))


def positionstage_je_titel(positionen: pd.DataFrame) -> set:
    """Menge der Paare (Symbol, Kalendertag) mit offener Position."""
    return set(_tage_je_position(positionen))


def _tage_je_position(positionen: pd.DataFrame) -> list:
    if positionen.empty:
        return []
    ein = pd.to_datetime(positionen["entry_time"]).dt.normalize()
    aus = pd.to_datetime(positionen["exit_time"]).dt.normalize()
    paare = []
    for symbol, a, b in zip(positionen["symbol"].astype(str), ein, aus):
        for tag in pd.date_range(a, b, freq="D"):
            paare.append((symbol, tag))
    return paare


def fenster(positionen: pd.DataFrame):
    """Erster Einstiegstag und letzter Ausstiegstag eines Bots."""
    ein = pd.to_datetime(positionen["entry_time"]).dt.normalize()
    aus = pd.to_datetime(positionen["exit_time"]).dt.normalize()
    return ein.min(), aus.max()


def gemeinsames_fenster(pos_a: pd.DataFrame, pos_b: pd.DataFrame):
    """Schnittmenge der beiden Zeitraeume - dieselbe Vorgehensweise wie in
    `research/exposure_messung/exposure_kern.py`. Gibt (None, None) zurueck,
    wenn sich die Zeitraeume nicht ueberschneiden."""
    a_von, a_bis = fenster(pos_a)
    b_von, b_bis = fenster(pos_b)
    von, bis = max(a_von, b_von), min(a_bis, b_bis)
    if von > bis:
        return None, None
    return von, bis


# ---------------------------------------------------------------------------
# 3. Ueberlappung je Bot-Paar
# ---------------------------------------------------------------------------

def ueberlappung(pos_a: pd.DataFrame, pos_b: pd.DataFrame) -> dict:
    """Zwei Anteile, beide im gemeinsamen Fenster und beide aus Sicht von A:

    `anteil_tage`  - Anteil der Tage, an denen A eine Position haelt, an denen
                     auch B irgendeine Position haelt. Fuer Paare aus
                     verschiedenen Anlageklassen ist das die einzige
                     sinnvolle Zahl ("gleichzeitig im Markt").
    `anteil_titel` - Anteil der (Symbol, Tag)-Paare von A, die auch B haelt.
                     Fuer Paare aus verschiedenen Anlageklassen ist er
                     zwangslaeufig 0 - es gibt kein gemeinsames Symbol.

    Die Zahl ist NICHT symmetrisch: ein Bot mit wenigen Positionstagen kann zu
    100 % in den Tagen eines Dauer-Investierten liegen, umgekehrt nicht.
    """
    von, bis = gemeinsames_fenster(pos_a, pos_b)
    if von is None:
        return {"gemeinsames_fenster": None, "tage_a": 0, "anteil_tage": None,
                "anteil_titel": None, "titeltage_a": 0}

    def im_fenster(paare):
        return {(s, t) for s, t in paare if von <= t <= bis}

    titel_a, titel_b = im_fenster(positionstage_je_titel(pos_a)), im_fenster(positionstage_je_titel(pos_b))
    tage_a = {t for _s, t in titel_a}
    tage_b = {t for _s, t in titel_b}

    return {
        "gemeinsames_fenster": (str(von.date()), str(bis.date())),
        "tage_im_fenster": int((bis - von).days + 1),
        "tage_a": len(tage_a),
        "tage_b": len(tage_b),
        "titeltage_a": len(titel_a),
        "anteil_tage": (len(tage_a & tage_b) / len(tage_a)) if tage_a else None,
        "anteil_titel": (len(titel_a & titel_b) / len(titel_a)) if titel_a else None,
    }


# ---------------------------------------------------------------------------
# 4. Naehe der Einstiege - reagieren zwei Bots auf dasselbe Ereignis?
# ---------------------------------------------------------------------------

def _einstiege_je_symbol(positionen: pd.DataFrame, von, bis) -> dict:
    ein = pd.to_datetime(positionen["entry_time"]).dt.normalize()
    maske = (ein >= von) & (ein <= bis)
    teil = pd.DataFrame({"symbol": positionen["symbol"].astype(str)[maske],
                          "tag": ein[maske]})
    return {s: np.sort(g["tag"].to_numpy()) for s, g in teil.groupby("symbol")}


def _treffer(a_tage: np.ndarray, b_tage: np.ndarray, fenster_tage: int) -> int:
    """Anzahl der Einstiege aus `a_tage`, zu denen mindestens ein Einstieg aus
    `b_tage` im Abstand von hoechstens `fenster_tage` Kalendertagen liegt
    (beide Richtungen)."""
    if a_tage.size == 0 or b_tage.size == 0:
        return 0
    spanne = np.timedelta64(fenster_tage, "D")
    links = np.searchsorted(b_tage, a_tage - spanne, side="left")
    rechts = np.searchsorted(b_tage, a_tage + spanne, side="right")
    return int((rechts > links).sum())


def naehe(pos_a: pd.DataFrame, pos_b: pd.DataFrame, fenster_tage: int = NAEHE_TAGE,
           zufallslaeufe: int = 200, saat: int = 20260913) -> dict:
    """Wie oft oeffnen A und B im selben Titel innerhalb von `fenster_tage`
    Tagen eine Position - und wie oft waere das bei zufaelliger Lage von B zu
    erwarten?

    Der Vergleichswert ist nicht Zierde, sondern notwendig: ein Bot mit
    tausenden Einstiegen in denselben Titeln trifft ein Drei-Tage-Fenster auch
    ohne jeden Zusammenhang haeufig. Gemessen wird deshalb zusaetzlich, was
    passiert, wenn die Einstiegstage von B je Symbol auf zufaellige Tage im
    gemeinsamen Fenster gelegt werden (Anzahl und Symbol-Verteilung bleiben
    gleich, nur die Lage wird zerstoert). `ueberschuss` ist das Verhaeltnis
    aus gemessenem und zufaelligem Anteil: 1,0 heisst "nicht mehr als
    Zufall", 2,0 heisst "doppelt so oft wie Zufall".
    """
    von, bis = gemeinsames_fenster(pos_a, pos_b)
    if von is None:
        return {"gemeinsames_fenster": None, "einstiege_a": 0, "treffer": 0,
                "anteil": None, "anteil_zufall": None, "ueberschuss": None}

    a_je_symbol = _einstiege_je_symbol(pos_a, von, bis)
    b_je_symbol = _einstiege_je_symbol(pos_b, von, bis)

    einstiege_a = sum(v.size for v in a_je_symbol.values())
    gemeinsame_symbole = sorted(set(a_je_symbol) & set(b_je_symbol))
    treffer = sum(_treffer(a_je_symbol[s], b_je_symbol[s], fenster_tage)
                  for s in gemeinsame_symbole)

    # Zufallsvergleich: B je Symbol auf zufaellige Tage im Fenster legen.
    anteil_zufall = None
    if einstiege_a and gemeinsame_symbole and zufallslaeufe > 0:
        rng = np.random.default_rng(saat)
        spanne = int((bis - von).days) + 1
        summe = 0
        for _ in range(zufallslaeufe):
            lauf = 0
            for s in gemeinsame_symbole:
                anzahl = b_je_symbol[s].size
                versatz = np.sort(rng.integers(0, spanne, size=anzahl))
                zufalls_tage = np.datetime64(von.date()) + versatz.astype("timedelta64[D]")
                lauf += _treffer(a_je_symbol[s], zufalls_tage, fenster_tage)
            summe += lauf
        anteil_zufall = summe / (zufallslaeufe * einstiege_a)

    anteil = (treffer / einstiege_a) if einstiege_a else None
    ueberschuss = None
    if anteil is not None and anteil_zufall:
        ueberschuss = anteil / anteil_zufall

    return {
        "gemeinsames_fenster": (str(von.date()), str(bis.date())),
        "einstiege_a": einstiege_a,
        "einstiege_b": sum(v.size for v in b_je_symbol.values()),
        "gemeinsame_symbole": len(gemeinsame_symbole),
        "treffer": treffer,
        "anteil": anteil,
        "anteil_zufall": anteil_zufall,
        "ueberschuss": ueberschuss,
        "zufallslaeufe": zufallslaeufe,
    }


VERSATZ_KANTEN = [-30, -20, -10, -3, 0, 3, 10, 20, 30]


def versatz_verteilung(pos_a: pd.DataFrame, pos_b: pd.DataFrame,
                        kanten=VERSATZ_KANTEN) -> dict:
    """Mit welchem VERSATZ oeffnen zwei Bots im selben Titel?

    Je Einstieg von A der vorzeichenbehaftete Abstand zum naechstgelegenen
    Einstieg von B im selben Titel, in Kalendertagen. Positiv heisst: B
    steigt spaeter ein. Bei Gleichstand (zwei B-Einstiege gleich weit weg)
    gewinnt der frueheste - eine Festlegung, keine Rundung.

    Warum diese Verteilung und nicht nur der Anteil aus `naehe()`: ein
    Drei-Tage-Fenster beantwortet "gleichzeitig ja/nein". Es zeigt nicht, ob
    zwei Bots dasselbe Ereignis mit festem Abstand handeln - zwei Bots, von
    denen einer immer zwei Wochen nach dem anderen einsteigt, sehen im
    Drei-Tage-Fenster wie voellig unabhaengige Bots aus.

    `anteil_bis_3_tage` muss dem `anteil` aus `naehe()` gleichen (dort ueber
    Fenstersuche, hier ueber den naechsten Nachbarn gerechnet) - geprueft in
    `test_haltedauer_kern.py`.
    """
    von, bis = gemeinsames_fenster(pos_a, pos_b)
    if von is None:
        return {"n": 0, "gemeinsames_fenster": None}

    a_je_symbol = _einstiege_je_symbol(pos_a, von, bis)
    b_je_symbol = _einstiege_je_symbol(pos_b, von, bis)
    einstiege_a = sum(v.size for v in a_je_symbol.values())

    versatz = []
    for symbol, a_tage in a_je_symbol.items():
        b_tage = b_je_symbol.get(symbol)
        if b_tage is None or b_tage.size == 0:
            continue
        for x in a_tage:
            abstand = (b_tage - x) / np.timedelta64(1, "D")
            # argmin nimmt bei Gleichstand den ersten Eintrag; b_tage ist
            # aufsteigend sortiert, also den frueheren B-Einstieg.
            versatz.append(float(abstand[np.argmin(np.abs(abstand))]))

    v = np.array(versatz, dtype="float64")
    grenzen = list(kanten)
    namen = [f"{grenzen[i]:g} bis < {grenzen[i + 1]:g}" for i in range(len(grenzen) - 1)]
    hist = {namen[i]: int(((v >= grenzen[i]) & (v < grenzen[i + 1])).sum())
            for i in range(len(grenzen) - 1)}

    nah = v[np.abs(v) <= 30]
    return {
        "gemeinsames_fenster": (str(von.date()), str(bis.date())),
        "einstiege_a": einstiege_a,
        "n": int(v.size),                      # A-Einstiege mit einem B-Einstieg im selben Titel
        "median_versatz": float(np.median(v)) if v.size else None,
        "median_versatz_bis_30_tage": float(np.median(nah)) if nah.size else None,
        "anteil_bis_3_tage": (float((np.abs(v) <= 3).sum()) / einstiege_a) if einstiege_a else None,
        "histogramm": hist,
        "unter_minus_30": int((v < grenzen[0]).sum()),
        "ueber_plus_30": int((v >= grenzen[-1]).sum()),
    }


def naehe_erwartet_analytisch(pos_a: pd.DataFrame, pos_b: pd.DataFrame,
                               fenster_tage: int = NAEHE_TAGE) -> float:
    """Derselbe Zufallsvergleich in geschlossener Form, als Gegenprobe zur
    Zufallsziehung in `naehe()`.

    Liegen `b` Einstiege eines Symbols gleichverteilt und unabhaengig auf `D`
    Tagen, so trifft ein gegebener A-Einstieg mit Wahrscheinlichkeit
    `1 - (1 - w/D)**b` mindestens einen davon, wobei `w = 2*fenster_tage + 1`
    die Fensterbreite in Tagen ist. Randeffekte (ein Fenster, das ueber den
    Fensteranfang oder das Fensterende hinausragt, ist kleiner) sind hier
    NICHT beruecksichtigt - der Wert liegt deshalb leicht ueber dem der
    Ziehung. Genau dafuer ist er da: als groessenordnungsmaessige
    Gegenprobe, nicht als zweite Messung.
    """
    von, bis = gemeinsames_fenster(pos_a, pos_b)
    if von is None:
        return float("nan")
    a_je_symbol = _einstiege_je_symbol(pos_a, von, bis)
    b_je_symbol = _einstiege_je_symbol(pos_b, von, bis)
    einstiege_a = sum(v.size for v in a_je_symbol.values())
    if not einstiege_a:
        return float("nan")
    D = int((bis - von).days) + 1
    w = min(2 * fenster_tage + 1, D)
    erwartet = 0.0
    for s, a_tage in a_je_symbol.items():
        b = b_je_symbol.get(s)
        if b is None or b.size == 0:
            continue
        erwartet += a_tage.size * (1 - (1 - w / D) ** b.size)
    return erwartet / einstiege_a


# ---------------------------------------------------------------------------
# 5. Einordnung: wie viele unterscheidbare Zeitfenster?
# ---------------------------------------------------------------------------
# Die Klassengrenzen sind VORAB festgelegt und nicht aus den Daten gewonnen.
# Die Klasse "3 bis 10 Tage" stammt woertlich aus der zu pruefenden Vermutung
# der Aufgabenstellung; die uebrigen Grenzen setzen sie fort. Eine aus den
# gemessenen Medianen gebildete Klassierung wuerde die Vermutung an sich
# selbst pruefen.
HORIZONT_KLASSEN = [
    ("bis 2 Tage", 0.0, 3.0),
    ("3 bis 10 Tage", 3.0, 10.5),
    ("11 bis 30 Tage", 10.5, 30.5),
    ("31 bis 90 Tage", 30.5, 90.5),
    ("ueber 90 Tage", 90.5, float("inf")),
]


def horizont_klasse(median_tage: float) -> str:
    for name, von, bis in HORIZONT_KLASSEN:
        if von <= median_tage < bis:
            return name
    raise ValueError(f"kein Horizont fuer Median {median_tage}")
