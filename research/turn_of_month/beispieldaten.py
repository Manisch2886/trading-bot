#!/usr/bin/env python3
"""
TB-33 - Erzeugte Beispieldaten
==============================================================================
Damit `auswertung.py` laufen und geprueft werden kann, BEVOR ein einziges
echtes Ergebnis existiert. Dieselbe Zusicherung wie in TB-30a: das
Auswertungsskript hat seinen Test bestanden, als es noch nichts zu deuten
gab.

WAS HIER GESETZT WIRD - UND WAS NICHT
------------------------------------------------------------------------------
Gesetzt werden **Kurse**. Nicht Ereignisse, nicht Mittelwerte, nicht Urteile.

Das ist der Unterschied, an dem sich in diesem Projekt schon mehrere Proben
blamiert haben: *eine Probe, deren Zustand der Test von Hand herstellt,
bestaetigt sich selbst.* Wer die Ereignisliste direkt setzt, prueft die
Handelstags-Regel nicht mehr - sie ist dann naemlich uebersprungen. Hier
entsteht eine Kursdatei, und alles Weitere - welcher Tag "-1" ist, wie
Feiertage wirken, was die Kosten abziehen, wie der Bootstrap streut - macht
die Auswertung selbst.

Steuerbar ist deshalb nur der KURSVERLAUF:

  kern_rendite_fn(jahr, monat) -> float
      die BRUTTO-Rendite, die das Kernfenster des Monatswechsels nach
      (jahr, monat) tragen soll. Verteilt wird sie gleichmaessig auf die
      Handelstage des Fensters. Was die Auswertung daraus macht - Kosten,
      Falte, Bootstrap - bleibt ihre Sache.

  tages_rendite_fn(datum) -> float
      die Brutto-Rendite aller uebrigen Handelstage.

FEIERTAGE UND VERKUERZTE TAGE
------------------------------------------------------------------------------
Feiertage werden aus der Reihe **weggelassen** - genauso, wie sie in echten
Kursdaten fehlen. Verkuerzte Tage stehen **drin** und sind von ganzen Tagen
nicht zu unterscheiden; die Liste `halbtage` gibt der Test nur zurueck, damit
er nachsehen kann, ob sie mitgezaehlt wurden.

Der erzeugte Kalender enthaelt ausdruecklich Monate, deren letzter
Wochentag ein Feiertag ist. Sonst liefe die Handelstags-Regel in der Probe
nie in den Fall, fuer den sie da ist.
"""

import os
import sys
from datetime import date, timedelta

import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)

import register as reg  # noqa: E402


def _n_ter_wochentag(jahr, monat, wochentag, n):
    d = date(jahr, monat, 1)
    d += timedelta(days=(wochentag - d.weekday()) % 7)
    return d + timedelta(days=7 * (n - 1))


def feiertagsplan(jahre):
    """Feiertage (fehlen in den Daten) und Halbtage (stehen drin).

    Bewusst enthalten: der **31. Dezember** und der **30. Juni** als
    Feiertage. Beide liegen am Monatsende - damit faellt "-1" nachweislich
    auf einen frueheren Handelstag, und die Regel wird wirklich geprueft
    statt nur mitgefuehrt.
    """
    feiertage, halbtage = set(), set()
    for j in jahre:
        feiertage |= {date(j, 1, 1), date(j, 7, 4), date(j, 12, 25),
                      date(j, 12, 31), date(j, 6, 30)}
        thanksgiving = _n_ter_wochentag(j, 11, 3, 4)          # 4. Donnerstag
        feiertage.add(thanksgiving)
        halbtage.add(thanksgiving + timedelta(days=1))        # Freitag danach
        halbtage.add(date(j, 12, 24))
    return feiertage, halbtage


def handelstagsreihe(von_jahr, bis_jahr):
    """Alle Handelstage: Wochentage ohne Feiertage. (Reihe, Halbtage)."""
    feiertage, halbtage = feiertagsplan(range(von_jahr, bis_jahr + 1))
    tage, d = [], date(von_jahr, 1, 1)
    ende = date(bis_jahr, 12, 31)
    while d <= ende:
        if d.weekday() < 5 and d not in feiertage:
            tage.append(d)
        d += timedelta(days=1)
    return tage, sorted(h for h in halbtage if h in set(tage))


def kernfenster_tage(tage, fenster=None):
    """Je Monatswechsel die Indexpositionen der Fenstertage.

    Benutzt DIESELBE Definition wie handelstage.ereignisse, aber unabhaengig
    davon nachgebaut - der Generator soll die Auswertung nicht bestaetigen,
    sondern nur Kurse setzen. Stimmen beide nicht ueberein, faellt das im
    Selbsttest auf, und das ist erwuenscht.
    """
    vor, nach = fenster or reg.KERNFENSTER
    anzahl_vor = -vor
    monate = {}
    for i, d in enumerate(tage):
        monate.setdefault((d.year, d.month), []).append(i)
    schluessel = sorted(monate)
    treffer = {}
    for a in range(len(schluessel) - 1):
        j, m = schluessel[a]
        folge = (j + 1, 1) if m == 12 else (j, m + 1)
        if schluessel[a + 1] != folge:
            continue
        idx_m, idx_n = monate[schluessel[a]], monate[folge]
        if len(idx_m) < anzahl_vor or len(idx_n) < nach:
            continue
        treffer[(j, m)] = idx_m[-anzahl_vor:] + idx_n[:nach]
    return treffer


def tagesrauschen(streuung, seed=0):
    """Ein reproduzierbares Tagesrauschen - aus dem Datum, nicht aus einem
    laufenden Zustand.

    Der Zufall haengt hier NUR am Datum. Damit liefert derselbe Tag in jedem
    Lauf denselben Wert, egal in welcher Reihenfolge die Lagen erzeugt
    werden - eine Voraussetzung dafuer, dass Teil E (Wiederholbarkeit)
    ueberhaupt etwas ueber die Auswertung aussagt und nicht bloss ueber den
    Generator.
    """
    import hashlib

    def f(d):
        roh = hashlib.sha256(f"{seed}:{d.isoformat()}".encode()).digest()
        # Zwei Bytes -> [0,1), dann auf [-1,1) zentriert.
        u = int.from_bytes(roh[:4], "big") / 2 ** 32
        return (u - 0.5) * 2.0 * streuung
    return f


def erzeuge(ziel_dir, symbol, von_jahr, bis_jahr,
            kern_rendite_fn=None, tages_rendite_fn=None,
            fenster=None, startkurs=100.0, luecken=0, sonder_tage=None,
            fehlende_monate=None):
    """Schreibt <ziel_dir>/<symbol>_1d.csv und gibt Begleitangaben zurueck.

    `luecken`: so viele Kerzen bekommen leere Kursspalten - der Fall, fuer
    den `shared/kursdaten` da ist. Sie muessen gestrichen UND gezaehlt
    werden.

    `fehlende_monate`: Liste von (jahr, monat), die ganz fehlen. Die daran
    haengenden Monatswechsel muessen ENTFALLEN und gezaehlt werden.
    """
    tage, halbtage = handelstagsreihe(von_jahr, bis_jahr)
    # Ganze Monate weglassen - der Fall, in dem aus zwei Monatswechseln
    # still einer wuerde, wenn die Luecke niemandem auffiele. Die Ereignisse
    # daran muessen ENTFALLEN und GEZAEHLT werden.
    if fehlende_monate:
        fehlt = set(fehlende_monate)
        tage = [d for d in tage if (d.year, d.month) not in fehlt]
        halbtage = [h for h in halbtage if (h.year, h.month) not in fehlt]
    fenster = fenster or reg.KERNFENSTER
    treffer = kernfenster_tage(tage, fenster)

    kern_pro_tag = {}
    for (j, m), positionen in treffer.items():
        ziel = (kern_rendite_fn(j, m) if kern_rendite_fn else 0.0)
        pro_tag = (1.0 + ziel) ** (1.0 / len(positionen)) - 1.0
        for p in positionen:
            kern_pro_tag[p] = pro_tag

    sonder_tage = sonder_tage or {}
    kurse, k = [], startkurs
    for i, d in enumerate(tage):
        r = kern_pro_tag.get(i)
        if r is None:
            r = (sonder_tage[d] if d in sonder_tage
                 else (tages_rendite_fn(d) if tages_rendite_fn else 0.0))
        k *= (1.0 + r)
        kurse.append(k)

    df = pd.DataFrame({
        "open_time": [d.isoformat() for d in tage],
        "open": kurse, "high": kurse, "low": kurse, "close": kurse,
        "volume": [1_000_000] * len(tage),
    })
    for n in range(luecken):
        # Kurse leer, Volumen gefuellt - genau der APH-Fall aus
        # research/elliott_wave_params/, auf den shared/kursdaten antwortet.
        zeile = len(df) // 2 + n
        df.loc[zeile, ["open", "high", "low", "close"]] = None

    os.makedirs(ziel_dir, exist_ok=True)
    pfad = os.path.join(ziel_dir, f"{symbol}_1d.csv")
    df.to_csv(pfad, index=False)
    return {"pfad": pfad, "tage": tage, "halbtage": halbtage,
            "kernfenster": treffer, "luecken": luecken}


# ---------------------------------------------------------------------------
# Vier benannte Lagen. Sie setzen KURSE, nicht Ergebnisse - welche Bedingung
# daran scheitert, entscheidet die Auswertung.
# ---------------------------------------------------------------------------
def lage(name):
    """(kern_rendite_fn, tages_rendite_fn) fuer eine benannte Lage.

    Jede Lage setzt KURSE. Welche Bedingung daran scheitert, entscheidet
    allein die Auswertung - hier steht kein Urteil, auch nicht als
    Erwartungswert.
    """
    ruhig = tagesrauschen(0.004, seed=1)
    # Ein Markt mit kraeftiger Drift: jedes beliebige Vier-Tage-Fenster
    # verdient hier gut. Genau der Fall, fuer den Test 2 da ist.
    def steil(d):
        return 0.002 + ruhig(d) * 0.25

    if name == "effekt_deutlich":
        # Der Effekt ist da: jedes Fenster traegt deutlich mehr als die
        # Kostenschranke, in jedem Jahr.
        return (lambda j, m: 0.012), ruhig

    if name == "kein_effekt":
        # Das Fenster ist wie jeder andere Tag. Netto zieht es damit die
        # Kosten - genau die Schranke, die der Effekt ueberspringen muss.
        return (lambda j, m: 0.0008), ruhig

    if name == "nur_b1_faellt":
        # Ein sehr gutes Jahr traegt den Mittelwert; die uebrigen liegen
        # knapp unter null. Der Falten-MEDIAN sieht das, der Mittelwert
        # nicht - dafuer ist B1 da.
        return (lambda j, m: 0.60 if j % 7 == 0 else 0.0018), ruhig

    if name == "nur_b2_faellt":
        # Meist knapp positiv, in jedem fuenften Jahr ein Einbruch. Median
        # und Perzentil bleiben oben, das Bootstrap-Intervall nicht -
        # dafuer ist B2 da.
        return (lambda j, m: -0.15 if (j % 4 == 0 and m == 5) else 0.0075), ruhig

    if name == "nur_b3_faellt":
        # Das Fenster ist netto positiv - aber JEDES andere Vier-Tage-
        # Fenster dieses Instruments auch, und die meisten mehr. Der Effekt
        # ist nur Beta. Genau das soll Test 2 zeigen.
        return (lambda j, m: 0.0055), steil

    if name == "kern_faellt_sweep_besteht":
        # Der Kern (-1/+3) traegt nichts und faellt an den Kosten. Der Tag
        # -2 traegt viel; die Sweep-Zelle -2/+3 besteht also. Was dann
        # passiert, ist die Sweep-Regel - und nur sie.
        return (lambda j, m: 0.0), ruhig

    raise ValueError(f"unbekannte Lage: {name}")


def zweitletzte_tage(von_jahr, bis_jahr):
    """Die Kalendertage, die im Fenster -2/+3, aber NICHT im Kern liegen.

    Gebraucht fuer die Lage `kern_faellt_sweep_besteht`: nur diese Tage
    bekommen ueber `sonder_tage` einen Aufschlag, und damit besteht genau
    die Sweep-Zelle -2/+3, ohne den Kern zu beruehren.
    """
    tage, _ = handelstagsreihe(von_jahr, bis_jahr)
    weit = kernfenster_tage(tage, (-2, 3))
    eng = kernfenster_tage(tage, (-1, 3))
    treffer = []
    for schluessel, positionen in weit.items():
        nur_weit = set(positionen) - set(eng.get(schluessel, []))
        treffer += [tage[p] for p in nur_weit]
    return sorted(treffer)
