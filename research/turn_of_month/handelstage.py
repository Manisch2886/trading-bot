#!/usr/bin/env python3
"""
TB-33 - Handelstage, nicht Kalendertage
==============================================================================
"-1" ist der LETZTE HANDELSTAG des Monats, nicht der 30. oder 31. Dieses
Modul ist die einzige Stelle, an der aus einer Kursreihe Ereignisse werden.

WARUM KEIN ZWEITER KALENDER
------------------------------------------------------------------------------
Es gibt einen Boersenkalender im Projekt (dashboard/boersenkalender.py). Er
wird hier ABSICHTLICH nicht benutzt. Die Handelstage stammen aus der
Kursreihe selbst - aus den Tagen, an denen das Instrument eine vollstaendige
Kerze traegt.

Der Grund steht in CLAUDE.md: jeder Handelsparameter steht genau einmal, und
doppelt gefuehrte Zahlen sind in diesem Projekt schon unbemerkt
auseinandergelaufen. Ein zweiter Kalender waere eine zweite Quelle fuer
dieselbe Zahl. Faellt ein Feiertag im Kalender anders als in den Daten, ist
nicht klar, welcher recht hat - und das Ergebnis haengt still an dieser
Frage.

Als Nebenwirkung braucht dieses Modul keine Feiertagstabelle und keine
Zeitzone: ein Feiertag steht gar nicht erst in der Reihe. Das ist auch der
Grund, warum es ohne die Zeitzone `US/Eastern` laeuft, die in manchen
Umgebungen fehlt.

VERKUERZTE HANDELSTAGE
------------------------------------------------------------------------------
Ein Halbtag (etwa der Tag nach Thanksgiving) ist ein VOLLER Handelstag und
zaehlt als einer. Die Strategie handelt zum Schluss, und ein verkuerzter Tag
hat einen Schluss. In den Daten ist er nicht von einem ganzen Tag zu
unterscheiden - genau deshalb steht die Regel im Register, BEVOR sie
gebraucht wird, und nicht erst, wenn jemand sie im Ergebnis vermisst.

STREICHEN UND ZAEHLEN
------------------------------------------------------------------------------
Ein Ereignis, dessen Fenster nicht vollstaendig in den Daten liegt, entfaellt
- und wird GEZAEHLT. Die Zahl steht in der Ergebnisdatei. Ein still
gestrichener Datenpunkt ist dasselbe Problem in Gruen.
"""

import os
import sys

import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)

import register as reg  # noqa: E402

sys.path.insert(0, os.path.join(reg.BASE_DIR, "shared"))
import kursdaten  # noqa: E402


class Abbruch(SystemExit):
    """Ein Vertragsbruch in den Eingangsdaten. Nie eine stille Annahme."""


def lies_kursreihe(pfad: str, melden: bool = False):
    """(DataFrame mit datum/close, Zahl der gestrichenen Kerzen).

    Die Bereinigung laeuft ueber shared/kursdaten - dieselbe Stelle wie bei
    den Bots, damit keine unvollstaendige Kerze ein Ergebnis vergiftet.
    """
    if not os.path.exists(pfad):
        raise Abbruch(f"Kursdatei fehlt: {pfad}")
    df = pd.read_csv(pfad)
    spalte = "open_time" if "open_time" in df.columns else "date"
    if spalte not in df.columns or "close" not in df.columns:
        raise Abbruch(f"{pfad}: Spalten 'open_time'/'date' und 'close' "
                      f"werden gebraucht, gefunden {list(df.columns)}")
    df, gestrichen = kursdaten.entferne_unvollstaendige(
        df, symbol=os.path.basename(pfad), melden=melden)
    df = df.rename(columns={spalte: "datum"})
    df["datum"] = pd.to_datetime(df["datum"])
    df = df.sort_values("datum").drop_duplicates("datum").reset_index(drop=True)
    if len(df) < 2:
        raise Abbruch(f"{pfad}: weniger als zwei Handelstage.")
    return df[["datum", "close"]], gestrichen


def monatsgrenzen(datum: pd.Series):
    """Je Kalendermonat die Indexpositionen seiner Handelstage.

    Rueckgabe: Liste von (jahr, monat, [indexpositionen]) in Zeitordnung.
    """
    schluessel = list(zip(datum.dt.year, datum.dt.month))
    gruppen = []
    for i, s in enumerate(schluessel):
        if gruppen and gruppen[-1][0] == s:
            gruppen[-1][1].append(i)
        else:
            gruppen.append((s, [i]))
    return [(j, m, idx) for (j, m), idx in gruppen]


def ereignisse(df: pd.DataFrame, fenster=None):
    """Die Ereignisse eines Fensters - je Monatswechsel eines.

    fenster = (vor, nach): `vor` ist negativ und nennt die Zahl der LETZTEN
    Handelstage des Monats (-1 = nur der letzte), `nach` die Zahl der ERSTEN
    Handelstage des Folgemonats. Gehalten werden |vor| + nach Handelstage.

    Rueckgabe: (DataFrame mit datum_einstieg/datum_ausstieg/jahr/
    brutto_rendite/netto_rendite, Zahl der entfallenen Ereignisse).
    """
    vor, nach = fenster or reg.KERNFENSTER
    if vor >= 0 or nach <= 0:
        raise Abbruch(f"Fenster {fenster!r}: 'vor' muss negativ, 'nach' "
                      f"positiv sein.")
    anzahl_vor = -vor
    close = df["close"].to_numpy(dtype=float)
    monate = monatsgrenzen(df["datum"])

    zeilen, entfallen = [], 0
    for a in range(len(monate) - 1):
        jahr_m, monat_m, idx_m = monate[a]
        jahr_n, monat_n, idx_n = monate[a + 1]

        # Der Folgemonat muss WIRKLICH der Folgemonat sein. Eine Luecke von
        # einem ganzen Monat in den Daten macht sonst still aus zwei
        # Monatswechseln einen.
        if (jahr_n, monat_n) != ((jahr_m + 1, 1) if monat_m == 12
                                 else (jahr_m, monat_m + 1)):
            entfallen += 1
            continue
        # Und er muss LUECKENLOS anschliessen: der erste Handelstag des
        # Folgemonats steht unmittelbar hinter dem letzten des Vormonats.
        if idx_n[0] != idx_m[-1] + 1:
            entfallen += 1
            continue
        # Genug Handelstage auf beiden Seiten?
        if len(idx_m) < anzahl_vor or len(idx_n) < nach:
            entfallen += 1
            continue

        erster = idx_m[-anzahl_vor]
        letzter = idx_n[nach - 1]
        # Die Einstiegsrendite misst gegen den Schluss des DAVORLIEGENDEN
        # Handelstags - den es geben muss.
        if erster - 1 < 0:
            entfallen += 1
            continue

        brutto = close[letzter] / close[erster - 1] - 1.0
        netto = (1.0 + brutto) * (1.0 - reg.KOSTEN_JE_ROUNDTRIP_PCT / 100.0) - 1.0
        zeilen.append({
            "datum_einstieg": df["datum"].iloc[erster],
            "datum_ausstieg": df["datum"].iloc[letzter],
            # Zuordnung zur Falte ueber den EINSTIEGSTAG - siehe
            # register.EREIGNIS_ZUORDNUNG.
            "jahr": int(df["datum"].iloc[erster].year),
            "gehaltene_tage": anzahl_vor + nach,
            "brutto_rendite": brutto,
            "netto_rendite": netto,
        })

    return pd.DataFrame(zeilen), entfallen


def vergleichsfenster(df: pd.DataFrame, laenge: int):
    """Die Netto-Renditen ALLER Fenster dieser Laenge - jedes moegliche
    Startdatum, gleiche Kosten.

    Grundlage von Test 2. Enthaelt die Kernfenster mit; sie herauszunehmen
    waere eine Wahl, und Wahlen gibt es hier nicht.
    """
    close = df["close"].to_numpy(dtype=float)
    if len(close) < laenge + 1:
        return pd.DataFrame(columns=["start", "netto_rendite"])
    start = range(1, len(close) - laenge + 1)
    brutto = [close[s + laenge - 1] / close[s - 1] - 1.0 for s in start]
    faktor = 1.0 - reg.KOSTEN_JE_ROUNDTRIP_PCT / 100.0
    return pd.DataFrame({
        "start": list(start),
        "netto_rendite": [(1.0 + b) * faktor - 1.0 for b in brutto],
    })
