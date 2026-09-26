"""
TB-116 - Pruefung vor dem Tag zu Register 16.4 (Registertext 6): ergibt das
Regelwerk fuer jede der 3^9 = 19 683 Stufentabellen genau einen
Multiplikatorvektor?
================================================================================
Das ist ein PRUEFWERKZEUG, nicht das Leiter-Skript. Es legt keine Lesart fest,
wird von keinem Lauf geladen und schreibt nichts ausser seinen beiden
Ergebnisdateien (nur mit --aus).

Register 16.4, Absatz "Pruefung vor dem Tag" (Register Z. 2038-2042):
"Das Leiter-Skript muss aus jeder moeglichen Stufentabelle - 3^9 = 19 683,
trivial aufzaehlbar - einen eindeutigen Multiplikatorvektor erzeugen, ohne
Eingabe des Betreibers."

Jede Regel, die dieses Modul anwendet, steht zeichengleich mit Fundstelle in
`docs/belege/TB-116/a_regeln.md`. Was es tut und NICHT im Zitat steht, ist eine
Lesart mit Namen:

  L0.1-L0.9  Rechenvereinbarungen (nicht variiert, je eine Zeile unten)
  L1  Zellenanteil und Klassenschluessel      L1a / L1b / L1c
  L2  Bezugsmenge der Zellen (Nenner in (h))  L2a / L2b / L2c
  L3  Klasse ohne aktive Zelle                L3a / L3b
  L4  Schatten-Bot in einer aktiven Zelle     L4a / L4b / L4c / L4d
  L5  Faktor "Bestaetigt" vor Netting         L5a / L5b

Keine Lesart ist die "richtige". Das Werkzeug rechnet alle 3*3*2*4*2 = 144
Kombinationen und meldet.

Stufentabellen sind HYPOTHETISCH (aufgezaehlt), nicht aus einem Lauf. Das
Werkzeug liest keine Datei des Selektionsraums und keine Ergebnisgroesse; die
"statische Benchmark-Position in Hoehe des mittleren Exposures" wird nur als
BUDGETANTEIL gefuehrt, die Exposure-Hoehe nicht berechnet (L0.1).

Nutzung (aus der Repo-Wurzel):
    trading-env/bin/python3 research/leiter_pruefung/leiter_lesarten.py \
        [--aus docs/belege/TB-116]
"""

import argparse
import itertools
import json
import os
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from fractions import Fraction as F

# ---------------------------------------------------------------------------
# Literale aus dem Register (Fundstellen: docs/VORREGISTRIERUNG_neuselektion.md)
# ---------------------------------------------------------------------------

# 16.4 (g), Register Z. 1968-1978: "Zellen sind Quelle x Anlage." Reihenfolge
# der Zeilen und der Bots wie in der Tabelle dort.
ZELLEN = (
    ("Fortsetzung × Aktien", "aktien", ("volatility_breakout",)),
    ("Umkehr × Aktien", "aktien", ("rsi2_mean_reversion", "turtle_soup_stocks", "elliott_wave_stocks")),
    ("Fortsetzung × Krypto", "krypto", ("t3_supertrend", "volatility_breakout_crypto")),
    ("Umkehr × Krypto", "krypto", ("rsi2_crypto", "turtle_soup_crypto", "elliott_wave")),
)
KURZ = ("FA", "UA", "FK", "UK")

# 16.4 (a), Register Z. 1934-1937: drei Stufen.
STUFEN = ("schatten", "grund", "bestaetigt")
STUFE_KURZ = {"schatten": "S", "grund": "G", "bestaetigt": "B"}

# 16.4 (i), Register Z. 1985-1987: "Schatten 0, Grundbudget 1, Bestaetigt 2".
FAKTOR = {"schatten": 0, "grund": 1, "bestaetigt": 2}

# 16.4 (l), Register Z. 1998-2000: "Aktien 80 / Krypto 20".
SCHLUESSEL = {"aktien": F(80, 100), "krypto": F(20, 100)}

# 16.4 (m), Register Z. 2006: "... / (1/9)" - die heutige statische Groesse.
NENNER = F(1, 9)

ANLAGEN = ("aktien", "krypto")
BOTS = tuple(b for _, _, bots in ZELLEN for b in bots)
ZELLE_VON = {b: i for i, (_, _, bots) in enumerate(ZELLEN) for b in bots}
ANLAGE_VON_ZELLE = tuple(a for _, a, _ in ZELLEN)

LESARTEN = {
    "L1": ("L1a", "L1b", "L1c"),
    "L2": ("L2a", "L2b", "L2c"),
    "L3": ("L3a", "L3b"),
    "L4": ("L4a", "L4b", "L4c", "L4d"),
    "L5": ("L5a", "L5b"),
}
STELLEN = tuple(LESARTEN)

BESCHREIBUNG = {
    "L0.1": "Benchmark-Position als Budgetanteil des Buchs; 'in Hoehe des mittleren Exposures' "
            "wird nicht gerechnet (Ergebnisgroesse des Selektionsraums, 27.1).",
    "L0.2": "Exakte Brueche; 'eindeutig' heisst gleich als Bruch.",
    "L0.3": "Heutige statische Positionsgroesse = 1/9 des Buchs (Nenner aus (m)); m_b = 1 heisst 'wie heute'.",
    "L0.4": "Anlage einer Zelle aus ihrem Namen in (g); Schluessel aus (l).",
    "L0.5": "Aktiv nach (h): mindestens ein Bot der Zelle auf Grundbudget oder Bestaetigt.",
    "L0.6": "Schatten hat m_b = 0 ((a): kein Portfoliogewicht), auch wo (i) in einer inaktiven Zelle 0/0 ergaebe.",
    "L0.7": "Eingabe ist nur die Stufentabelle: keine Vorgeschichte, keine Herkunft einer Stufe, kein Netting.",
    "L0.8": "Buchsumme = Summe m_b x (1/9) + Benchmark-Anteile (Formel des Auftrags); Rest = 1 - Buchsumme, "
            "keinem Ort zugeordnet (der Text nennt keinen).",
    "L0.9": "Schatten in einer Zelle ausserhalb der Bezugsmenge (L2) erhaelt keinen Anteil; (b) nennt fuer "
            "ihn einen Budgetanteil, (h) gibt der Zelle keinen - nicht variiert, im Ergebnis als Stelle gefuehrt.",
    "L1a": "Zellenanteil = 1/|R| ueber alle Zellen der Bezugsmenge; Klassenschluessel multipliziert danach "
           "((h) 'teilen das Buch', (m) woertlich).",
    "L1b": "Das Buch wird zuerst 80/20 geteilt; Zellenanteil = 1/|R_Klasse| innerhalb der Anlage ((l) "
           "'skaliert die Zellen einer Anlage gemeinsam'). Klasse ohne Zelle in R: Schluessel in ihre Benchmark.",
    "L1c": "Gleiche Teile ueber alle Zellen, mit dem Schluessel gewichtet und auf das Buch normiert: "
           "w = K_Klasse / Summe K ueber R (Sitzung ergaenzt).",
    "L2a": "R = die jetzt aktiven Zellen ((h)/(k) woertlich: Zahl aktiver Zellen).",
    "L2b": "R = alle vier Zellen aus (g); eine inaktive Zelle in R gibt ihr Budget in die Benchmark ihrer "
           "Anlage ((j)) (Sitzung ergaenzt).",
    "L2c": "R = die seit der letzten Zulassung aktiven Zellen ((j): Inaktivwerden verteilt nicht um; (k): nur "
           "Zulassung aendert die Zahl). R steht nicht in der Tabelle: Antwort nur, wenn jede moegliche "
           "Vorgeschichte (aktiv <= R <= alle) denselben Vektor ergibt (Sitzung ergaenzt).",
    "L3a": "Klasse ohne aktive Zelle: ihr Anteil geht in die Benchmark ihrer Anlage ((j), zellenweise gelesen).",
    "L3b": "Klasse ohne aktive Zelle: ihr Schluessel geht an die andere Klasse (Schluessel 1/0), sofern diese "
           "eine aktive Zelle hat.",
    "L4a": "Schatten in aktiver Zelle: (i)/(j) gelten immer - Faktor 0, die uebrigen teilen, keine Benchmark "
           "aus diesem Bot.",
    "L4b": "(b) gilt immer: der Schatten zaehlt beim Teilen wie Grundbudget (Faktor 1); sein Anteil haelt "
           "die Benchmark seiner Anlage.",
    "L4c": "(b) gilt immer: sein Budgetanteil ist die heutige Groesse 1/9 und haelt zusaetzlich die Benchmark; "
           "das Zellenbudget teilen die uebrigen nach (i).",
    "L4d": "(b) gilt nur direkt nach dem Lauf (vor der ersten Quartalspruefung), danach (i)/(j). Steht ein "
           "Bestaetigt in der Tabelle, ist mindestens eine Quartalspruefung vorbei ((c)) -> wie L4a; sonst "
           "Antwort nur, wenn L4a und L4b dasselbe ergeben.",
    "L5a": "Bestaetigt hat Faktor 2 ((i), ohne Bedingung).",
    "L5b": "Bestaetigt hat bis Netting Faktor 1 ((a): 'Rang-5-Gewichtung, sobald Netting existiert') "
           "(Sitzung ergaenzt).",
}

FEHLT = {
    "L2c": "Welche Zellen seit der letzten Zulassung aktiv waren: (j) verbietet, dass der Nenner beim "
           "Inaktivwerden faellt, (h) zaehlt nur die aktiven Zellen - die Tabelle traegt die Vorgeschichte nicht.",
    "L4d": "Ob die Tabelle der Stand direkt nach dem Selektionslauf ist, und damit ob (b) oder (i)/(j) fuer den "
           "Schatten in der aktiven Zelle gilt - die Tabelle traegt Zeitpunkt und Herkunft der Stufe nicht "
           "(Lauf (b), Abstieg (d), Notbremse (e)/22.4, 16.5).",
}


# ---------------------------------------------------------------------------
# Aufzaehlung und Darstellung
# ---------------------------------------------------------------------------

def alle_tabellen():
    """Alle 3^9 Stufentabellen, je ein Tupel in der Bot-Reihenfolge von BOTS."""
    return list(itertools.product(STUFEN, repeat=len(BOTS)))


def alle_lesarten():
    """Alle Kombinationen, je ein dict {Stelle: Option}."""
    return [dict(zip(STELLEN, k)) for k in itertools.product(*(LESARTEN[s] for s in STELLEN))]


def lesart_name(lesart):
    return "-".join(lesart[s] for s in STELLEN)


def tabelle_text(tab):
    """Kurzform je Zelle, z. B. 'FA:G UA:GGS FK:GS UK:SSS'."""
    teile, i = [], 0
    for kurz, (_, _, bots) in zip(KURZ, ZELLEN):
        teile.append(kurz + ":" + "".join(STUFE_KURZ[s] for s in tab[i:i + len(bots)]))
        i += len(bots)
    return " ".join(teile)


def tabelle_aus_text(text):
    """Umkehrung von tabelle_text (fuer Tests und Beispiele)."""
    rueck = {v: k for k, v in STUFE_KURZ.items()}
    zeichen = "".join(t.split(":")[1] for t in text.split())
    assert len(zeichen) == len(BOTS), text
    return tuple(rueck[z] for z in zeichen)


def bruch(x):
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


# ---------------------------------------------------------------------------
# Rechnung
# ---------------------------------------------------------------------------

def _zellen_von(tab):
    """Je Zelle das Tupel (Bot-Index, Stufe)."""
    z = [[] for _ in ZELLEN]
    for i, (b, s) in enumerate(zip(BOTS, tab)):
        z[ZELLE_VON[b]].append((i, s))
    return tuple(tuple(x) for x in z)


def _aktiv(zellen):
    return frozenset(c for c, inhalt in enumerate(zellen) if any(s != "schatten" for _, s in inhalt))


@lru_cache(maxsize=8192)
def _mit_bezug(zellen, aktiv, R, l1, l3, l4, l5):
    """Ergebnis fuer eine feste Bezugsmenge R und L4 in {L4a, L4b, L4c}."""
    klassen_aktiv = {ANLAGE_VON_ZELLE[c] for c in aktiv}
    K = dict(SCHLUESSEL)
    if l3 == "L3b" and len(klassen_aktiv) == 1:
        (k,) = klassen_aktiv
        K = {a: F(1) if a == k else F(0) for a in ANLAGEN}

    bench = {a: F(0) for a in ANLAGEN}
    w = {}
    if l1 == "L1a":
        for c in R:
            w[c] = K[ANLAGE_VON_ZELLE[c]] / len(R)
    elif l1 == "L1b":
        for a in ANLAGEN:
            RK = [c for c in R if ANLAGE_VON_ZELLE[c] == a]
            if RK:
                for c in RK:
                    w[c] = K[a] / len(RK)
            else:
                bench[a] += K[a]
    else:  # L1c
        nenner = sum((K[ANLAGE_VON_ZELLE[c]] for c in R), F(0))
        if nenner > 0:
            for c in R:
                w[c] = K[ANLAGE_VON_ZELLE[c]] / nenner

    faktor = dict(FAKTOR)
    if l5 == "L5b":
        faktor["bestaetigt"] = 1

    m = [F(0)] * len(BOTS)
    for c in R:
        a = ANLAGE_VON_ZELLE[c]
        if c not in aktiv:
            bench[a] += w[c]                      # (j): inaktive Zelle -> Benchmark ihrer Anlage
            continue
        inhalt = zellen[c]
        n_schatten = sum(s == "schatten" for _, s in inhalt)
        if l4 == "L4b":
            summe = sum(faktor[s] if s != "schatten" else 1 for _, s in inhalt)
            bench[a] += w[c] * n_schatten / summe
        else:
            summe = sum(faktor[s] for _, s in inhalt)
            if l4 == "L4c":
                bench[a] += NENNER * n_schatten
        for i, s in inhalt:
            if s != "schatten":
                m[i] = w[c] * faktor[s] / summe / NENNER
    return tuple(m), (bench["aktien"], bench["krypto"])


def _schluessel(werte):
    """Brueche als Paare ganzer Zahlen - gleich genau, aber billig zu vergleichen."""
    return tuple((x.numerator, x.denominator) for x in werte)


def rechne(tab, lesart):
    """Ergebnis einer Stufentabelle unter einer Lesart-Kombination.

    Rueckgabe: dict mit antwort (bool), m (Tupel, nur mit Antwort),
    benchmark (aktien, krypto), buchsumme, rest, fehlt (Liste der Stellen ohne
    Antwort: 'L2c' und/oder 'L4d').
    """
    zellen = _zellen_von(tab)
    aktiv = _aktiv(zellen)
    l1, l2, l3, l4, l5 = (lesart[s] for s in STELLEN)
    alle = frozenset(range(len(ZELLEN)))

    if l2 == "L2a":
        bezuege = [aktiv]
    elif l2 == "L2b":
        bezuege = [alle]
    else:
        frei = sorted(alle - aktiv)
        bezuege = [aktiv | frozenset(t) for r in range(len(frei) + 1) for t in itertools.combinations(frei, r)]

    fehlt = set()
    ergebnisse = {}                              # Schluessel (ganze Zahlen) -> Ergebnis
    for R in bezuege:
        if l4 == "L4d":
            e_a = _mit_bezug(zellen, aktiv, R, l1, l3, "L4a", l5)
            if "bestaetigt" in tab:
                e = e_a
            else:
                e_b = _mit_bezug(zellen, aktiv, R, l1, l3, "L4b", l5)
                if e_a != e_b:
                    fehlt.add("L4d")
                    continue
                e = e_a
        else:
            e = _mit_bezug(zellen, aktiv, R, l1, l3, l4, l5)
        ergebnisse[_schluessel(e[0]), _schluessel(e[1])] = e

    if not fehlt and len({m for m, _ in ergebnisse}) > 1:
        fehlt.add("L2c")
    if fehlt:
        return {"antwort": False, "fehlt": sorted(fehlt)}
    if len(ergebnisse) > 1:
        # m eindeutig, aber Benchmark-Anteile nicht: als eigene Klasse melden.
        return {"antwort": False, "fehlt": ["L2c-benchmark"]}
    ((schl, _), (m, bench)), = ergebnisse.items()
    summe = sum(m, F(0)) * NENNER + bench[0] + bench[1]
    return {"antwort": True, "m": m, "schluessel": schl, "benchmark": bench, "buchsumme": summe,
            "rest": 1 - summe, "fehlt": []}


# ---------------------------------------------------------------------------
# Pruefung ueber alle Tabellen
# ---------------------------------------------------------------------------

def merkmal(tab):
    """Unterschiedsklasse einer Tabelle: aktive Zellen je Anlage, Schatten in
    aktiver Zelle, Bestaetigt vorhanden."""
    zellen = _zellen_von(tab)
    aktiv = _aktiv(zellen)
    na = sum(ANLAGE_VON_ZELLE[c] == "aktien" for c in aktiv)
    nk = sum(ANLAGE_VON_ZELLE[c] == "krypto" for c in aktiv)
    sch = any(s == "schatten" for c in aktiv for _, s in zellen[c])
    return "aktiv A%d/K%d, Schatten in aktiver Zelle %s, Bestaetigt %s" % (
        na, nk, "ja" if sch else "nein", "ja" if "bestaetigt" in tab else "nein")


def pruefung(tabellen=None, lesarten=None, beispiele=3):
    tabellen = alle_tabellen() if tabellen is None else tabellen
    lesarten = alle_lesarten() if lesarten is None else lesarten
    namen = [lesart_name(l) for l in lesarten]

    je_lesart = {n: {"antwort": 0, "keine_antwort": Counter(), "keine_antwort_beispiel": {},
                     "summe_ungleich_1": 0, "summe_min": None, "summe_max": None,
                     "summe_min_tabelle": None, "summe_max_tabelle": None,
                     "max_m": None, "max_m_tabelle": None, "max_m_bot": None}
                 for n in namen}
    # Stelle -> Unterschiedsklasse -> {"tabellen": set, "beispiele": [...]}
    unterschiede = {s: defaultdict(lambda: {"tabellen": set(), "beispiele": []}) for s in STELLEN}
    stelle_tabellen = {s: set() for s in STELLEN}
    verschiedene_vektoren = Counter()      # Zahl verschiedener m je Tabelle (ueber alle Kombinationen)
    ohne_jede_antwort = 0

    for tab in tabellen:
        erg = {}
        for l, n in zip(lesarten, namen):
            e = rechne(tab, l)
            erg[n] = e
            s = je_lesart[n]
            if not e["antwort"]:
                klasse = "+".join(e["fehlt"])
                s["keine_antwort"][klasse] += 1
                s["keine_antwort_beispiel"].setdefault(klasse, tabelle_text(tab))
                continue
            s["antwort"] += 1
            su = e["buchsumme"]
            if su != 1:
                s["summe_ungleich_1"] += 1
            if s["summe_min"] is None or su < s["summe_min"]:
                s["summe_min"], s["summe_min_tabelle"] = su, tabelle_text(tab)
            if s["summe_max"] is None or su > s["summe_max"]:
                s["summe_max"], s["summe_max_tabelle"] = su, tabelle_text(tab)
            mx = max(e["m"])
            if s["max_m"] is None or mx > s["max_m"]:
                s["max_m"], s["max_m_tabelle"], s["max_m_bot"] = mx, tabelle_text(tab), BOTS[e["m"].index(mx)]

        vektoren = {e["schluessel"] for e in erg.values() if e["antwort"]}
        verschiedene_vektoren[len(vektoren)] += 1
        ohne_jede_antwort += not vektoren

        mk = None
        for stelle in STELLEN:
            andere = [x for x in STELLEN if x != stelle]
            gruppen = defaultdict(list)
            for l, n in zip(lesarten, namen):
                gruppen[tuple(l[x] for x in andere)].append((l[stelle], erg[n]))
            for rest, glieder in gruppen.items():
                beantwortet = [(o, e["schluessel"], e["m"]) for o, e in glieder if e["antwort"]]
                for (o1, k1, m1), (o2, k2, m2) in itertools.combinations(beantwortet, 2):
                    if k1 == k2:
                        continue
                    mk = mk or merkmal(tab)
                    klasse = "%s≠%s | %s" % (o1, o2, mk)
                    u = unterschiede[stelle][klasse]
                    if tab not in u["tabellen"] and len(u["beispiele"]) < beispiele:
                        u["beispiele"].append({
                            "tabelle": tabelle_text(tab),
                            "uebrige_lesarten": "-".join(rest),
                            o1: [bruch(x) for x in m1], o2: [bruch(x) for x in m2]})
                    u["tabellen"].add(tab)
                    stelle_tabellen[stelle].add(tab)

    return {
        "tabellen": len(tabellen),
        "verschiedene_tabellen": len(set(tabellen)),
        "lesarten": len(lesarten),
        "je_lesart": je_lesart,
        "unterschiede": {s: {k: {"tabellen": len(v["tabellen"]), "beispiele": v["beispiele"]}
                             for k, v in sorted(unterschiede[s].items())} for s in STELLEN},
        "stelle_tabellen": {s: len(v) for s, v in stelle_tabellen.items()},
        "verschiedene_vektoren": dict(sorted(verschiedene_vektoren.items())),
        "ohne_jede_antwort": ohne_jede_antwort,
    }


# ---------------------------------------------------------------------------
# Ausgabe
# ---------------------------------------------------------------------------

def _f(x):
    return None if x is None else {"bruch": bruch(x), "wert": round(float(x), 6)}


def als_json(p):
    je = {}
    for n, s in p["je_lesart"].items():
        je[n] = {
            "tabellen_mit_eindeutigem_vektor": s["antwort"],
            "tabellen_ohne_antwort": sum(s["keine_antwort"].values()),
            "ohne_antwort_klassen": dict(s["keine_antwort"]),
            "ohne_antwort_beispiel": {k: {"tabelle": v, "fehlender_satz": " / ".join(
                FEHLT.get(x.split("-")[0], x) for x in k.split("+"))} for k, v in s["keine_antwort_beispiel"].items()},
            "buchsumme_ungleich_1": s["summe_ungleich_1"],
            "buchsumme_min": _f(s["summe_min"]), "buchsumme_min_tabelle": s["summe_min_tabelle"],
            "buchsumme_max": _f(s["summe_max"]), "buchsumme_max_tabelle": s["summe_max_tabelle"],
            "max_m": _f(s["max_m"]), "max_m_tabelle": s["max_m_tabelle"], "max_m_bot": s["max_m_bot"],
        }
    return {
        "werkzeug": "research/leiter_pruefung/leiter_lesarten.py (TB-116)",
        "grundlage": "Register 16.4 (Registertext 6), docs/belege/TB-116/a_regeln.md",
        "bots": list(BOTS),
        "zellen": [{"kurz": k, "zelle": z, "anlage": a, "bots": list(b)} for k, (z, a, b) in zip(KURZ, ZELLEN)],
        "tabellen": p["tabellen"], "verschiedene_tabellen": p["verschiedene_tabellen"],
        "lesart_kombinationen": p["lesarten"],
        "lesarten": BESCHREIBUNG,
        "fehlende_saetze": FEHLT,
        "je_lesart": je,
        "unterschiede_je_stelle": p["unterschiede"],
        "tabellen_mit_unterschied_je_stelle": p["stelle_tabellen"],
        "verschiedene_vektoren_je_tabelle": {str(k): v for k, v in p["verschiedene_vektoren"].items()},
        "tabellen_ohne_jede_antwort": p["ohne_jede_antwort"],
    }


def als_text(p):
    z = []
    a = z.append
    a("TB-116 c_pruefung - Register 16.4, alle Stufentabellen x alle Lesart-Kombinationen")
    a("Tabellen: %d (verschieden: %d), Lesart-Kombinationen: %d" % (
        p["tabellen"], p["verschiedene_tabellen"], p["lesarten"]))
    a("Tabellenschreibweise: FA/UA/FK/UK = Fortsetzung/Umkehr x Aktien/Krypto; S/G/B = Schatten/Grund/Bestaetigt;")
    a("  Bots je Zelle in der Reihenfolge von 16.4 (g): " + "; ".join(
        "%s=%s" % (k, ",".join(b)) for k, (_, _, b) in zip(KURZ, ZELLEN)))
    a("")
    a("== Lesarten")
    for k, v in BESCHREIBUNG.items():
        a("  %-5s %s" % (k, v))
    a("")
    a("== Je Lesart-Kombination (Reihenfolge L1-L2-L3-L4-L5)")
    a("  %-24s %6s %6s  %-26s %6s  %-22s %s" % (
        "Kombination", "eindt.", "ohne", "ohne-Klassen", "S!=1", "Summe min..max", "max m_b (Bot, Tabelle)"))
    for n, s in p["je_lesart"].items():
        kl = ",".join("%s:%d" % kv for kv in sorted(s["keine_antwort"].items())) or "-"
        spanne = "-" if s["summe_min"] is None else "%.4f..%.4f" % (s["summe_min"], s["summe_max"])
        mx = "-" if s["max_m"] is None else "%s=%.3f (%s, %s)" % (
            bruch(s["max_m"]), s["max_m"], s["max_m_bot"], s["max_m_tabelle"])
        a("  %-24s %6d %6d  %-26s %6d  %-22s %s" % (
            n, s["antwort"], sum(s["keine_antwort"].values()), kl, s["summe_ungleich_1"], spanne, mx))
    a("")
    a("== Ohne Antwort: je Klasse ein Beispiel mit dem fehlenden Satz")
    gesehen = {}
    for n, s in p["je_lesart"].items():
        for k, t in s["keine_antwort_beispiel"].items():
            gesehen.setdefault(k, (n, t))
    for k, (n, t) in sorted(gesehen.items()):
        a("  Klasse %s - Beispiel %s unter %s" % (k, t, n))
        for x in k.split("+"):
            a("    fehlt: " + FEHLT.get(x.split("-")[0], x) + (
                " (hier: m eindeutig, Benchmark-Anteile nicht)" if x.endswith("-benchmark") else ""))
    a("")
    a("== Verschiedene Vektoren je Tabelle ueber alle %d Kombinationen (nur beantwortete)" % p["lesarten"])
    for k, v in p["verschiedene_vektoren"].items():
        a("  %3d verschiedene Vektoren: %5d Tabellen" % (k, v))
    a("  Tabellen, die unter keiner Kombination beantwortet werden: %d" % p["ohne_jede_antwort"])
    a("")
    a("== Je Stelle: Tabellen, in denen die Optionen (uebrige Stellen fest) verschiedene Vektoren ergeben")
    for st in STELLEN:
        a("  %s: %d Tabellen" % (st, p["stelle_tabellen"][st]))
    for st in STELLEN:
        a("")
        a("-- %s: Unterschiedsklassen (Optionspaar | Merkmal der Tabelle): Tabellen, 3 Beispiele" % st)
        for k, v in sorted(p["unterschiede"][st].items()):
            a("  %s: %d" % (k, len(v["tabellen"])))
            for b in v["beispiele"]:
                o1, o2 = k.split(" | ")[0].split("≠")
                a("      %s  [uebrige %s]  %s=(%s)  %s=(%s)" % (
                    b["tabelle"], b["uebrige_lesarten"], o1, " ".join(b[o1]), o2, " ".join(b[o2])))
    return "\n".join(z) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--aus", help="Ordner fuer c_pruefung.txt und c_pruefung.json (ohne: nur Kurzfassung)")
    args = ap.parse_args(argv)
    p = pruefung()
    if args.aus:
        with open(os.path.join(args.aus, "c_pruefung.txt"), "w", encoding="utf-8") as f:
            f.write(als_text(p))
        with open(os.path.join(args.aus, "c_pruefung.json"), "w", encoding="utf-8") as f:
            json.dump(als_json(p), f, ensure_ascii=False, indent=1, sort_keys=False)
            f.write("\n")
    print("Tabellen %d (verschieden %d), Kombinationen %d" % (
        p["tabellen"], p["verschiedene_tabellen"], p["lesarten"]))
    for st in STELLEN:
        print("  %s: Unterschied in %d Tabellen" % (st, p["stelle_tabellen"][st]))
    print("  verschiedene Vektoren je Tabelle:", p["verschiedene_vektoren"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
