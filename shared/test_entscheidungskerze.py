#!/usr/bin/env python3
"""
Selbsttests zu shared/entscheidungskerze.py (TB-38)
==============================================================================
Geprueft wird das VERHALTEN, nicht das Vorhandensein von Codestuecken.

Der Kern sind die Abschnitte 5 und 6: drei der neun `forward_test.py` werden
**tatsaechlich ausgefuehrt**, gegen erzeugte Beispieldaten, in einem
Miniatur-Abbild des Projekts unter /tmp - und beobachtet wird, was danach in
ihrer Datenbank steht. Ein Bot, der `entscheidungskerze` zwar einbindet, aber
die laufende Kerze trotzdem benutzt, faellt hier durch.

Die zwei wiederkehrenden Fallen dieses Projekts sind ausdruecklich adressiert:

* **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
  selbst.** Deshalb wird der Zustand nirgends gesetzt, sondern erzeugt: die
  Kursreihe traegt eine laufende Kerze mit einem Tief, das einen Stop
  ausloesen WUERDE, und ein Signal, das ein Bot eroeffnen WUERDE. Ob beides
  passiert, entscheidet der Ablauf - nicht der Test. Abschnitt 8 schaltet die
  Absicherungen einzeln ab und sieht nach, ob die zugehoerige Pruefung
  daraufhin auch wirklich FEHLSCHLAEGT. Eine Pruefung, die ohne ihre
  Absicherung gruen bleibt, prueft nichts.
* **Eine zweite Wache verdeckt das Fehlen der ersten.** Der Filter greift an
  zwei Stellen (Normalfall aus `data/` UND Rueckfall-Abruf), die Meldung
  haengt an zwei Bedingungen (es gab einen Rueckfall UND die Daempfung laesst
  durch). Abschnitt 8 schaltet jede einzeln ab und prueft nach, dass dann
  genau die eine zugehoerige Pruefung verlorengeht - und die anderen nicht.

Ohne Netz. Binance und yfinance sind aus der Cloud gesperrt; hier laeuft
nichts gegen einen Endpunkt, sondern gegen Attrappen, die dieselbe
Schnittstelle bedienen. Der Boersenkalender wird ebenfalls als Attrappe
uebergeben, damit die Regelpruefungen nicht davon abhaengen, ob
`pandas_market_calendars` auf dem pruefenden Rechner liegt - und zusaetzlich,
wenn die Bibliothek DA ist, gegen den echten Kalender gehalten.

Nutzung:  python3 shared/test_entscheidungskerze.py
"""

import ast
import datetime as dt
import glob
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

import pandas as pd                                            # noqa: E402

import abrufschutz                                             # noqa: E402
import entscheidungskerze as ek                                # noqa: E402

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
    else:
        FEHLER.append(f"{name}" + (f"  [{detail}]" if detail else ""))


def abschnitt(titel):
    print(f"\n--- {titel} " + "-" * max(0, 74 - len(titel)))


# ===========================================================================
# Beispieldaten
# ===========================================================================
def reihe(erste_oeffnung, anzahl, intervall, tief=None, hoch=None,
          schluss=None):
    """Eine Kursreihe auf dem Zeitraster des Intervalls.

    `tief`/`hoch`/`schluss` sind Abbildungen Index -> Wert und setzen einzelne
    Kerzen ab; alles andere bleibt flach. Flach ist Absicht: jede Abweichung
    in einer Kennzahl ist danach auf genau eine gesetzte Kerze
    zurueckfuehrbar.
    """
    laenge = abrufschutz.INTERVALL_MS[intervall]
    start = abrufschutz.als_ms(ek._als_zeitpunkt(erste_oeffnung))
    zeiten = [start + i * laenge for i in range(anzahl)]
    df = pd.DataFrame({
        "open_time": pd.to_datetime(zeiten, unit="ms"),
        "open": [100.0] * anzahl,
        "high": [101.0] * anzahl,
        "low": [99.0] * anzahl,
        "close": [100.0] * anzahl,
        "volume": [10.0] * anzahl,
    })
    for spalte, werte in (("low", tief), ("high", hoch), ("close", schluss)):
        for i, wert in (werte or {}).items():
            df.loc[i, spalte] = wert
    return df


def handelstage(erster, anzahl):
    """`anzahl` aufeinanderfolgende Werktage ab `erster` (Mo-Fr).

    Bewusst ohne Feiertage: diese Reihe dient den Regelpruefungen, und der
    Kalender wird dort als Attrappe uebergeben. Die Feiertage prueft der
    echte Kalender in Abschnitt 4.
    """
    tag = dt.date.fromisoformat(erster)
    tage = []
    while len(tage) < anzahl:
        if tag.weekday() < 5:
            tage.append(tag)
        tag += dt.timedelta(days=1)
    return tage


def aktienreihe(erster, anzahl, tief=None):
    tage = handelstage(erster, anzahl)
    df = pd.DataFrame({
        "open_time": pd.to_datetime([t.isoformat() for t in tage]),
        "open": [100.0] * anzahl,
        "high": [101.0] * anzahl,
        "low": [99.0] * anzahl,
        "close": [100.0] * anzahl,
        "volume": [10.0] * anzahl,
    })
    for i, wert in (tief or {}).items():
        df.loc[i, "low"] = wert
    return df


class KalenderAttrappe:
    """Dieselbe Schnittstelle wie `notifications/boersenkalender`.

    Sie kennt nur `status(jetzt)` und liefert `letzter_handelstag` - genau
    das, was die Schicht abfragt. Der Schluss liegt bei 20:00 UTC, wie bei
    der NYSE in der US-Sommerzeit.
    """

    def __init__(self, tage, schluss_utc=dt.time(20, 0), fehler=None):
        self.tage = [dt.date.fromisoformat(t) if isinstance(t, str) else t
                     for t in tage]
        self.schluss = schluss_utc
        self.fehler = fehler
        self.abfragen = 0

    def status(self, jetzt=None):
        self.abfragen += 1
        if self.fehler:
            raise RuntimeError(self.fehler)
        marke = ek._als_zeitpunkt(jetzt)
        vergangen = [t for t in self.tage
                     if dt.datetime.combine(t, self.schluss) <= marke]
        return {"offen": False,
                "grund": "Attrappe",
                "letzter_handelstag": (vergangen[-1].isoformat()
                                       if vergangen else None)}


class KalenderStumm:
    """Ein Kalender, der nicht antworten kann - die Bibliothek fehlt."""

    def status(self, jetzt=None):
        return {"offen": None,
                "grund": "Die Bibliothek pandas_market_calendars fehlt.",
                "letzter_handelstag": None}


# ===========================================================================
# 1 - Die Regel: die Entscheidungskerze ist nie die laufende
# ===========================================================================
def test_regel_krypto():
    abschnitt("1  Die Regel, alle drei Intervalle, Krypto")

    faelle = [
        # (Intervall, erste Oeffnung, Anzahl, Startzeit, erwartete Kerze)
        ("1h", "2026-09-15 00:00:00", 13, "2026-09-15 12:00:00",
         "2026-09-15 11:00:00"),
        ("1h", "2026-09-15 00:00:00", 13, "2026-09-15 12:34:56",
         "2026-09-15 11:00:00"),
        ("4h", "2026-09-14 00:00:00", 10, "2026-09-15 12:00:00",
         "2026-09-15 08:00:00"),
        ("4h", "2026-09-14 00:00:00", 10, "2026-09-15 12:05:00",
         "2026-09-15 08:00:00"),
        ("1d", "2026-09-01 00:00:00", 16, "2026-09-15 23:20:00",
         "2026-09-14 00:00:00"),
        ("1d", "2026-09-01 00:00:00", 16, "2026-09-16 00:00:00",
         "2026-09-15 00:00:00"),
    ]
    for intervall, erste, anzahl, startzeit, erwartet in faelle:
        df = reihe(erste, anzahl, intervall)
        zeile = ek.entscheidungskerze(df, intervall, ek.KRYPTO, startzeit)
        gewaehlt = str(zeile["open_time"]) if zeile is not None else "keine"
        check(f"1.1 {intervall} @ {startzeit} -> {erwartet}",
              gewaehlt == erwartet, f"gewaehlt: {gewaehlt}")

        # Und die entscheidende Verneinung, getrennt geprueft: die Kerze, die
        # zur Startzeit LAEUFT, ist nie die gewaehlte.
        laenge = abrufschutz.INTERVALL_MS[intervall]
        stand = abrufschutz.als_ms(ek._als_zeitpunkt(startzeit))
        laufend_ms = (stand // laenge) * laenge
        laufend = str(pd.to_datetime(laufend_ms, unit="ms"))
        check(f"1.2 {intervall} @ {startzeit}: nicht die laufende ({laufend})",
              gewaehlt != laufend, f"gewaehlt: {gewaehlt}")


def test_regel_aktien():
    abschnitt("2  Die Regel, Aktien (Tageskerzen, Sitzungsschluss)")

    tage = handelstage("2026-09-01", 12)
    df = aktienreihe("2026-09-01", 12)
    kalender = KalenderAttrappe(tage)

    # 20:15 UTC - der echte Cron-Zeitpunkt (22:15 Ortszeit im Sommer), also
    # 15 Minuten nach Handelsschluss. Die Kerze von HEUTE muss genommen
    # werden; sonst waere jedes Signal einen Handelstag zu spaet.
    heute = tage[-1]
    zeile = ek.entscheidungskerze(df, "1d", ek.AKTIEN,
                                  f"{heute} 20:15:00", kalender=kalender)
    check("2.1 15 Minuten nach Schluss -> die Kerze von heute",
          zeile is not None and str(zeile["open_time"]).startswith(str(heute)),
          f"gewaehlt: {zeile['open_time'] if zeile is not None else None}")

    # Waehrend der Sitzung ist die Tageskerze eine Teilkerze - sie darf nicht
    # genommen werden.
    zeile = ek.entscheidungskerze(df, "1d", ek.AKTIEN,
                                  f"{heute} 17:30:00", kalender=kalender)
    gestern = tage[-2]
    check("2.2 waehrend der Sitzung -> die Kerze von gestern",
          zeile is not None and str(zeile["open_time"]).startswith(str(gestern)),
          f"gewaehlt: {zeile['open_time'] if zeile is not None else None}")

    # Am Wochenende bleibt es bei der Kerze vom Freitag - ohne dass jemand
    # eine Wochenendregel geschrieben haette.
    samstag = tage[-1] + dt.timedelta(days=1)
    while samstag.weekday() != 5:
        samstag += dt.timedelta(days=1)
    zeile = ek.entscheidungskerze(df, "1d", ek.AKTIEN,
                                  f"{samstag} 20:15:00", kalender=kalender)
    check("2.3 Samstag -> weiter die Kerze des letzten Handelstags",
          zeile is not None and str(zeile["open_time"]).startswith(str(tage[-1])),
          f"gewaehlt: {zeile['open_time'] if zeile is not None else None}")

    # Genau EINE Kalenderabfrage je Aufruf, nicht eine je Zeile.
    kalender.abfragen = 0
    ek.entscheidungskerze(df, "1d", ek.AKTIEN, f"{heute} 20:15:00",
                          kalender=kalender)
    check("2.4 eine Kalenderabfrage je Aufruf, nicht eine je Zeile",
          kalender.abfragen == 1, f"Abfragen: {kalender.abfragen}")

    # Ein anderes Intervall hat bei Aktien keinen Sitzungsschluss, an dem
    # sich etwas festmachen liesse - das muss auffallen, nicht raten.
    try:
        ek.entscheidbar_maske(reihe("2026-09-15 00:00:00", 5, "1h"), "1h",
                              ek.AKTIEN, "2026-09-15 12:00:00",
                              kalender=kalender)
        check("2.5 Aktien mit Stundenintervall wird abgelehnt", False,
              "kein Fehler geworfen")
    except ValueError:
        check("2.5 Aktien mit Stundenintervall wird abgelehnt", True)


def test_regel_grenze():
    abschnitt("3  Die Grenze: close_time GENAU auf der Startzeit")

    # Die 08:00-Kerze eines 4h-Charts endet um 11:59:59.999 (Binance-Lesart,
    # siehe Modulkopf). Genau dort darf sie noch NICHT genommen werden.
    df = reihe("2026-09-14 00:00:00", 10, "4h")
    genau = "2026-09-15 11:59:59.999000"
    zeile = ek.entscheidungskerze(df, "4h", ek.KRYPTO, genau)
    check("3.1 4h: close_time == Startzeit -> die Kerze wird NICHT genommen",
          zeile is not None and str(zeile["open_time"]) == "2026-09-15 04:00:00",
          f"gewaehlt: {zeile['open_time'] if zeile is not None else None}")

    eine_ms_spaeter = "2026-09-15 12:00:00"
    zeile = ek.entscheidungskerze(df, "4h", ek.KRYPTO, eine_ms_spaeter)
    check("3.2 4h: eine Millisekunde spaeter -> sie wird genommen",
          zeile is not None and str(zeile["open_time"]) == "2026-09-15 08:00:00",
          f"gewaehlt: {zeile['open_time'] if zeile is not None else None}")

    for intervall, erste, genau, davor, danach in [
        ("1h", "2026-09-15 00:00:00", "2026-09-15 10:59:59.999000",
         "2026-09-15 09:00:00", "2026-09-15 10:00:00"),
        ("1d", "2026-09-01 00:00:00", "2026-09-14 23:59:59.999000",
         "2026-09-13 00:00:00", "2026-09-14 00:00:00"),
    ]:
        df2 = reihe(erste, 16, intervall)
        a = ek.entscheidungskerze(df2, intervall, ek.KRYPTO, genau)
        b = ek.entscheidungskerze(
            df2, intervall, ek.KRYPTO,
            ek._als_zeitpunkt(genau) + dt.timedelta(milliseconds=1))
        check(f"3.3 {intervall}: auf der Grenze -> {davor}",
              a is not None and str(a["open_time"]) == davor,
              f"gewaehlt: {a['open_time'] if a is not None else None}")
        check(f"3.4 {intervall}: eine Millisekunde danach -> {danach}",
              b is not None and str(b["open_time"]) == danach,
              f"gewaehlt: {b['open_time'] if b is not None else None}")

    # Aktien: der Sitzungsschluss ist die Grenze.
    tage = handelstage("2026-09-01", 12)
    df3 = aktienreihe("2026-09-01", 12)
    kalender = KalenderAttrappe(tage)
    heute = tage[-1]
    auf_der_grenze = ek.entscheidungskerze(df3, "1d", ek.AKTIEN,
                                           f"{heute} 20:00:00",
                                           kalender=kalender)
    knapp_davor = ek.entscheidungskerze(df3, "1d", ek.AKTIEN,
                                        f"{heute} 19:59:59.999000",
                                        kalender=kalender)
    check("3.5 Aktien: zum Sitzungsschluss ist die Tageskerze fertig",
          auf_der_grenze is not None
          and str(auf_der_grenze["open_time"]).startswith(str(heute)))
    check("3.6 Aktien: eine Millisekunde vor Schluss noch nicht",
          knapp_davor is not None
          and str(knapp_davor["open_time"]).startswith(str(tage[-2])))


def test_echter_kalender():
    abschnitt("4  Gegen den ECHTEN Boersenkalender (wenn vorhanden)")

    kalender = ek._boersenkalender()
    if kalender is None or not getattr(kalender, "bibliothek_verfuegbar",
                                       lambda: False)():
        print("    uebersprungen: pandas_market_calendars ist hier nicht "
              "installiert (der Rest dieser Datei laeuft ohne).")
        return

    # 2026-09-15 ist ein Dienstag in der US-Sommerzeit: Schluss 20:00 UTC.
    tag, grund = ek.letzter_handelstag("2026-09-15 20:15:00", kalender)
    check("4.1 20:15 UTC: der letzte Handelstag ist derselbe Tag",
          tag == "2026-09-15", f"{tag} / {grund}")
    tag, grund = ek.letzter_handelstag("2026-09-15 19:00:00", kalender)
    check("4.2 19:00 UTC (Boerse offen): der Vortag",
          tag == "2026-09-14", f"{tag} / {grund}")

    # Ein Wochenende ohne eigene Wochenendregel.
    tag, _g = ek.letzter_handelstag("2026-09-19 20:15:00", kalender)
    check("4.3 Samstag: der Freitag davor", tag == "2026-09-18", f"{tag}")

    # Der Cron-Zeitpunkt der vier Aktien-Bots (22:15 Ortszeit) liegt in
    # BEIDEN Zeitzonenlagen nach Handelsschluss. Im Winter ist das 21:15 UTC.
    tag, _g = ek.letzter_handelstag("2026-01-06 21:15:00", kalender)
    check("4.4 Winter, 21:15 UTC: derselbe Tag", tag == "2026-01-06", f"{tag}")
    tag, _g = ek.letzter_handelstag("2026-01-06 20:15:00", kalender)
    check("4.5 Winter, 20:15 UTC (Boerse noch offen): der Vortag",
          tag == "2026-01-05", f"{tag}")


def test_zwei_wege_ein_ergebnis():
    abschnitt("5  Erwartung und Maske sind derselbe Zeitpunkt")

    # `erwartete_letzte_oeffnung` (Frischepruefung) und `entscheidbar_maske`
    # (Filter) rechnen auf verschiedenen Wegen. Sie muessen dasselbe sagen -
    # sonst faellt ein Bot auf den Live-Abruf zurueck und filtert danach
    # etwas anderes weg, als er erwartet hat.
    for intervall, erste, anzahl in [("1h", "2026-09-15 00:00:00", 25),
                                     ("4h", "2026-09-13 00:00:00", 25),
                                     ("1d", "2026-08-20 00:00:00", 30)]:
        df = reihe(erste, anzahl, intervall)
        for minute in (0, 1, 7, 59):
            startzeit = f"2026-09-15 12:{minute:02d}:00"
            erwartet, _g = ek.erwartete_letzte_oeffnung(intervall, ek.KRYPTO,
                                                        startzeit)
            zeile = ek.entscheidungskerze(df, intervall, ek.KRYPTO, startzeit)
            gewaehlt = abrufschutz.als_ms(
                zeile["open_time"].to_pydatetime()) if zeile is not None else None
            check(f"5.1 {intervall} @ {startzeit}: Erwartung == Maske",
                  gewaehlt == erwartet, f"{gewaehlt} vs {erwartet}")


# ===========================================================================
# 6 - Der Rueckfall
# ===========================================================================
class Abrufattrappe:
    """Der Live-Abruf eines Bots - sie zaehlt, wie oft sie gerufen wurde."""

    def __init__(self, df):
        self.df = df
        self.aufrufe = 0

    def __call__(self):
        self.aufrufe += 1
        return self.df.copy()


def _ordner_mit(df, symbol, intervall, ordner):
    os.makedirs(ordner, exist_ok=True)
    df.to_csv(os.path.join(ordner, f"{symbol}_{intervall}.csv"), index=False)
    return ordner


def test_rueckfall():
    abschnitt("6  Der Rueckfall auf den Live-Abruf")

    startzeit = "2026-09-15 12:05:00"
    # data/ ist frisch: die letzte abgeschlossene 4h-Kerze (08:00) steht drin
    # und keine weitere - so, wie fetch_*.py sie seit TB-35 schreibt.
    frisch = reihe("2026-09-14 00:00:00", 9, "4h")       # bis 2026-09-15 08:00
    # Der Endpunkt liefert dieselbe Reihe PLUS die laufende Kerze (12:00),
    # und die traegt ein Tief, das unuebersehbar ist, wenn es durchkommt.
    live = reihe("2026-09-14 00:00:00", 10, "4h", tief={9: 1.0})

    with tempfile.TemporaryDirectory() as tmp:
        ordner = _ordner_mit(frisch, "TESTUSDT", "4h",
                             os.path.join(tmp, "data"))
        abruf = Abrufattrappe(live)
        sammler = ek.Sammler()
        df = ek.lade("TESTUSDT", "4h", ek.KRYPTO, abruf, datenordner=ordner,
                     startzeit=startzeit, sammler=sammler, melden=False)
        check("6.1 frisches data/: kein Live-Abruf", abruf.aufrufe == 0,
              f"Aufrufe: {abruf.aufrufe}")
        check("6.2 frisches data/: kein Rueckfall vermerkt", sammler.leer)
        check("6.3 frisches data/: Entscheidungskerze ist 08:00",
              str(df.iloc[-1]["open_time"]) == "2026-09-15 08:00:00",
              str(df.iloc[-1]["open_time"]))

    # data/ ist veraltet: die 08:00-Kerze fehlt.
    veraltet = reihe("2026-09-14 00:00:00", 8, "4h")     # bis 2026-09-15 04:00
    with tempfile.TemporaryDirectory() as tmp:
        ordner = _ordner_mit(veraltet, "TESTUSDT", "4h",
                             os.path.join(tmp, "data"))
        abruf = Abrufattrappe(live)
        sammler = ek.Sammler()
        df = ek.lade("TESTUSDT", "4h", ek.KRYPTO, abruf, datenordner=ordner,
                     startzeit=startzeit, sammler=sammler, melden=False)
        check("6.4 veraltetes data/: der Live-Abruf greift",
              abruf.aufrufe == 1, f"Aufrufe: {abruf.aufrufe}")
        check("6.5 veraltetes data/: als 'veraltet' vermerkt",
              sammler.je_symbol.get("TESTUSDT", (None,))[0] == ek.VERALTET,
              str(sammler.je_symbol))
        # DIE Pruefung dieses Abschnitts: der Ausnahmefall verhaelt sich NICHT
        # anders als der Normalfall. Die laufende Kerze aus dem Live-Abruf ist
        # weg - obwohl sie mit einem Tief von 1.0 unuebersehbar waere.
        check("6.6 der zurueckgefallene Abruf wendet denselben Filter an",
              str(df.iloc[-1]["open_time"]) == "2026-09-15 08:00:00",
              str(df.iloc[-1]["open_time"]))
        check("6.7 das Tief der laufenden Kerze ist nicht in den Daten",
              float(df["low"].min()) > 1.5, str(df["low"].min()))

    # Die Datei fehlt ganz.
    with tempfile.TemporaryDirectory() as tmp:
        ordner = os.path.join(tmp, "data")
        os.makedirs(ordner)
        abruf = Abrufattrappe(live)
        sammler = ek.Sammler()
        df = ek.lade("TESTUSDT", "4h", ek.KRYPTO, abruf, datenordner=ordner,
                     startzeit=startzeit, sammler=sammler, melden=False)
        check("6.8 fehlende Kursdatei: der Live-Abruf greift",
              abruf.aufrufe == 1)
        check("6.9 fehlende Kursdatei: eigener Grund, nicht 'veraltet'",
              sammler.je_symbol.get("TESTUSDT", (None,))[0] == ek.FEHLT,
              str(sammler.je_symbol))

    # Aktien, Kalender stumm: die Frische ist nicht feststellbar. Dann wird
    # nicht geraten, sondern die sichere Schranke benutzt UND gemeldet.
    tage = handelstage("2026-09-01", 12)
    heute = tage[-1]
    aktien_frisch = aktienreihe("2026-09-01", 12)
    with tempfile.TemporaryDirectory() as tmp:
        ordner = _ordner_mit(aktien_frisch, "TESTAG", "1d",
                             os.path.join(tmp, "data"))
        abruf = Abrufattrappe(aktien_frisch)
        sammler = ek.Sammler()
        df = ek.lade("TESTAG", "1d", ek.AKTIEN, abruf, datenordner=ordner,
                     startzeit=f"{heute} 20:15:00", sammler=sammler,
                     melden=False, kalender=KalenderStumm())
        check("6.10 stummer Kalender: als 'Frische unklar' vermerkt",
              sammler.je_symbol.get("TESTAG", (None,))[0] == ek.UNKLAR,
              str(sammler.je_symbol))
        check("6.11 stummer Kalender: die sichere Schranke gilt "
              "(Kerze von gestern, nicht von heute)",
              str(df.iloc[-1]["open_time"]).startswith(str(tage[-2])),
              str(df.iloc[-1]["open_time"]))
        check("6.12 stummer Kalender: es wird nicht geraten, sondern gemeldet",
              bool(sammler.kernzeilen()), str(sammler.kernzeilen()))


# ===========================================================================
# 7 - Die Meldung
# ===========================================================================
class Sendeattrappe:
    def __init__(self, erfolg=True, wirft=None):
        self.texte = []
        self.erfolg = erfolg
        self.wirft = wirft

    def __call__(self, text):
        if self.wirft:
            raise RuntimeError(self.wirft)
        self.texte.append(text)
        return self.erfolg


def test_meldung():
    abschnitt("7  Die Meldung: genau einmal je Lauf, gedaempft, nie fatal")

    startzeit = "2026-09-15 12:05:00"
    veraltet = reihe("2026-09-14 00:00:00", 8, "4h")     # bis 2026-09-15 04:00
    live = reihe("2026-09-14 00:00:00", 10, "4h")        # bis 2026-09-15 12:00

    with tempfile.TemporaryDirectory() as tmp:
        ordner = os.path.join(tmp, "data")
        for symbol in ("AAAUSDT", "BBBUSDT", "CCCUSDT"):
            _ordner_mit(veraltet, symbol, "4h", ordner)
        zustand = os.path.join(tmp, "zustand.json")

        sammler = ek.Sammler()
        for symbol in ("AAAUSDT", "BBBUSDT", "CCCUSDT"):
            ek.lade(symbol, "4h", ek.KRYPTO, Abrufattrappe(live),
                    datenordner=ordner, startzeit=startzeit, sammler=sammler,
                    melden=False)

        senden = Sendeattrappe()
        anlass = ek.melde("testbot", sammler, senden, zustand,
                          jetzt=dt.datetime(2026, 9, 15, 12, 5))
        check("7.1 drei Rueckfaelle -> GENAU EINE Nachricht",
              len(senden.texte) == 1, f"{len(senden.texte)} Nachrichten")
        check("7.2 Anlass beim ersten Mal: neu", anlass == "neu", str(anlass))
        check("7.3 die Nachricht nennt alle drei Symbole",
              all(s in senden.texte[0] for s in
                  ("AAAUSDT", "BBBUSDT", "CCCUSDT")), senden.texte[0][:200])

        # Derselbe Befund im naechsten Lauf: geschwiegen wird.
        senden2 = Sendeattrappe()
        anlass = ek.melde("testbot", sammler, senden2, zustand,
                          jetzt=dt.datetime(2026, 9, 15, 16, 5))
        check("7.4 unveraenderter Befund -> gedaempft, keine Nachricht",
              anlass == "gedaempft" and not senden2.texte,
              f"{anlass}, {len(senden2.texte)}")

        # Ein anderes Symbol kommt dazu: das liest sich anders, also melden.
        sammler.erfasse("DDDUSDT", ek.VERALTET, "Grund")
        senden3 = Sendeattrappe()
        anlass = ek.melde("testbot", sammler, senden3, zustand,
                          jetzt=dt.datetime(2026, 9, 15, 20, 5))
        check("7.5 geaenderter Befund -> gemeldet",
              anlass == "geaendert" and len(senden3.texte) == 1,
              f"{anlass}, {len(senden3.texte)}")

        # Erinnerung nach sieben Tagen.
        senden4 = Sendeattrappe()
        anlass = ek.melde("testbot", sammler, senden4, zustand,
                          jetzt=dt.datetime(2026, 9, 23, 0, 5))
        check("7.6 unveraendert, aber sieben Tage her -> Erinnerung",
              anlass == "erinnerung" and len(senden4.texte) == 1,
              f"{anlass}, {len(senden4.texte)}")

        # Kein Rueckfall mehr: geschwiegen, und der Vermerk wird geraeumt.
        leer = ek.Sammler()
        senden5 = Sendeattrappe()
        anlass = ek.melde("testbot", leer, senden5, zustand,
                          jetzt=dt.datetime(2026, 9, 23, 4, 5))
        check("7.7 kein Rueckfall -> Schweigen",
              anlass == "still" and not senden5.texte,
              f"{anlass}, {len(senden5.texte)}")
        vermerke = json.load(open(zustand, encoding="utf-8"))["waechter"]
        check("7.8 der Vermerk wird geraeumt, damit ein Rueckkehrer wieder "
              "'neu' ist", "testbot" not in vermerke, str(list(vermerke)))

    # Ein fehlgeschlagener Versand gilt als NICHT zugestellt.
    with tempfile.TemporaryDirectory() as tmp:
        zustand = os.path.join(tmp, "zustand.json")
        sammler = ek.Sammler()
        sammler.erfasse("AAAUSDT", ek.VERALTET, "Grund")
        ek.melde("testbot", sammler, Sendeattrappe(erfolg=False), zustand,
                 jetzt=dt.datetime(2026, 9, 15, 12, 5))
        senden = Sendeattrappe()
        anlass = ek.melde("testbot", sammler, senden, zustand,
                          jetzt=dt.datetime(2026, 9, 15, 16, 5))
        check("7.9 Versand gescheitert -> beim naechsten Lauf Nachholung",
              anlass == "nachholung" and len(senden.texte) == 1,
              f"{anlass}, {len(senden.texte)}")

    # Der Meldeteil bringt den Lauf nie zum Scheitern.
    with tempfile.TemporaryDirectory() as tmp:
        zustand = os.path.join(tmp, "zustand.json")
        sammler = ek.Sammler()
        sammler.erfasse("AAAUSDT", ek.VERALTET, "Grund")
        try:
            ek.melde("testbot", sammler, Sendeattrappe(wirft="Netz weg"),
                     zustand, jetzt=dt.datetime(2026, 9, 15, 12, 5))
            check("7.10 ein werfender Versand reicht nichts nach aussen durch",
                  True)
        except Exception as fehler:                         # noqa: BLE001
            check("7.10 ein werfender Versand reicht nichts nach aussen durch",
                  False, f"{type(fehler).__name__}: {fehler}")

        # Auch ein kaputter Zustandspfad darf den Bot nicht anhalten.
        try:
            ek.melde("testbot", sammler, Sendeattrappe(),
                     os.path.join(tmp, "nicht", "\0", "geht"),
                     jetzt=dt.datetime(2026, 9, 15, 12, 5))
            check("7.11 ein unbrauchbarer Zustandspfad haelt den Bot nicht an",
                  True)
        except Exception as fehler:                         # noqa: BLE001
            check("7.11 ein unbrauchbarer Zustandspfad haelt den Bot nicht an",
                  False, f"{type(fehler).__name__}: {fehler}")


# ===========================================================================
# Das Miniatur-Abbild des Projekts
# ===========================================================================
STUB_FETCH_BINANCE = '''
"""Attrappe: liefert die vorbereitete Reihe INKLUSIVE laufender Kerze."""
import os
import pandas as pd


class AbrufLeer(RuntimeError):
    pass


def fetch_historical_data(symbol, interval, lookback, client=None):
    with open(os.environ["STUB_PROTOKOLL"], "a") as p:
        p.write(f"binance {symbol} {interval}\\n")
    return pd.read_csv(os.environ["STUB_LIVE_CSV"], parse_dates=["open_time"])
'''

STUB_FETCH_STOCK = '''
"""Attrappe: liefert die vorbereitete Reihe INKLUSIVE laufender Tageszeile."""
import os
import pandas as pd

INTERVAL = "1d"
PERIOD = "max"


def fetch_historical_data(ticker, period=PERIOD, interval=INTERVAL):
    with open(os.environ["STUB_PROTOKOLL"], "a") as p:
        p.write(f"yfinance {ticker} {interval}\\n")
    return pd.read_csv(os.environ["STUB_LIVE_CSV"], parse_dates=["open_time"])
'''

STUB_BINANCE_CLIENT = '''
class Client:
    KLINE_INTERVAL_1HOUR = "1h"
    KLINE_INTERVAL_4HOUR = "4h"
    KLINE_INTERVAL_1DAY = "1d"

    def __init__(self, *a, **k):
        raise AssertionError("In diesem Test wird nichts abgerufen.")
'''

STUB_NOTIFY = '''
import os


def send_alert(text, parse_mode="Markdown"):
    with open(os.environ["STUB_MELDUNGEN"], "a") as p:
        p.write(text.replace("\\n", " | ") + "\\n")
    return True
'''

# Die neun Bots ziehen ihre Symbolliste aus shared/. Hier genau eines.
STUB_SYMBOLS = 'SYMBOLS = ["TESTUSDT"]\n'
STUB_SYMBOLS_AKTIEN = 'SYMBOLS = ["TESTAG"]\n'


def baue_abbild(wurzel, bot, live_csv_quelle):
    """Ein Miniatur-Projekt mit EINEM echten Bot darin.

    Der Bot rechnet seinen `shared/`-Ordner aus der eigenen Lage aus
    (`dirname(dirname(_STRATEGY_DIR)) + "/shared"`). Genau das wird hier
    ausgenutzt: im nachgebauten Baum findet er die Attrappen statt der echten
    Module - und ein `data/`, das NICHT auf `data/` dieses Repos zeigt. Kein
    Test dieser Datei fasst den echten Kursdatenbestand an.
    """
    shared = os.path.join(wurzel, "shared")
    notif = os.path.join(wurzel, "notifications")
    stubs = os.path.join(wurzel, "stubs")
    daten = os.path.join(wurzel, "data")
    strategie = os.path.join(wurzel, "strategies", bot)
    for ordner in (shared, notif, stubs, daten, strategie,
                   os.path.join(stubs, "binance")):
        os.makedirs(ordner, exist_ok=True)

    # ECHTE Module - unveraendert uebernommen, damit hier geprueft wird, was
    # spaeter auch laeuft.
    for name in ("entscheidungskerze.py", "abrufschutz.py", "kursdaten.py",
                 "binance_historie.py", "strategy_paths.py",
                 "data_quality.py"):
        shutil.copy2(os.path.join(_SHARED, name), os.path.join(shared, name))
    for name in ("waechter_melden.py", "boersenkalender.py"):
        quelle = os.path.join(BASE_DIR, "notifications", name)
        if os.path.exists(quelle):
            shutil.copy2(quelle, os.path.join(notif, name))

    def schreibe(pfad, inhalt):
        with open(pfad, "w", encoding="utf-8") as datei:
            datei.write(inhalt)

    schreibe(os.path.join(shared, "symbols_config.py"), STUB_SYMBOLS)
    schreibe(os.path.join(shared, "stocks_symbols_config.py"),
             STUB_SYMBOLS_AKTIEN)
    schreibe(os.path.join(shared, "fetch_binance_data.py"), STUB_FETCH_BINANCE)
    schreibe(os.path.join(notif, "notify.py"), STUB_NOTIFY)
    schreibe(os.path.join(stubs, "binance", "__init__.py"), "")
    schreibe(os.path.join(stubs, "binance", "client.py"), STUB_BINANCE_CLIENT)

    # Der Bot selbst, seine Indikatoren und seine Parameter - echt.
    for name in os.listdir(os.path.join(BASE_DIR, "strategies", bot)):
        if name in ("forward_test.py", "indicators.py", "live_params.py",
                    "regime_filter.py", "zigzag_indicator.py",
                    "elliott_wave_counter.py"):
            shutil.copy2(os.path.join(BASE_DIR, "strategies", bot, name),
                         os.path.join(strategie, name))
    if os.path.exists(os.path.join(BASE_DIR, "strategies", bot,
                                   "fetch_stock_data.py")):
        schreibe(os.path.join(strategie, "fetch_stock_data.py"),
                 STUB_FETCH_STOCK)

    shutil.copy2(live_csv_quelle, os.path.join(wurzel, "live.csv"))
    return {"wurzel": wurzel, "shared": shared, "daten": daten,
            "strategie": strategie, "stubs": stubs,
            "live": os.path.join(wurzel, "live.csv"),
            "db": os.path.join(wurzel, f"paper_trading_{bot}.db")}


def starte_bot(abbild, protokoll, meldungen):
    """Den echten forward_test.py wirklich laufen lassen."""
    umgebung = os.environ.copy()
    umgebung["PYTHONPATH"] = abbild["stubs"]
    umgebung["STUB_PROTOKOLL"] = protokoll
    umgebung["STUB_LIVE_CSV"] = abbild["live"]
    umgebung["STUB_MELDUNGEN"] = meldungen
    skript = os.path.join(abbild["strategie"], "forward_test.py")
    lauf = subprocess.run([sys.executable, "forward_test.py"],
                          cwd=abbild["strategie"], env=umgebung,
                          capture_output=True, text=True, timeout=300)
    return lauf.returncode, lauf.stdout + lauf.stderr


def trades(db):
    if not os.path.exists(db):
        return []
    verbindung = sqlite3.connect(db)
    try:
        return verbindung.execute(
            "SELECT symbol, entry_time, exit_time, result, status "
            "FROM trades ORDER BY id").fetchall()
    finally:
        verbindung.close()


def lege_offene_position(db, symbol, entry_time, entry_price, stop_price):
    """Eine offene Position anlegen - mit demselben Schema, das der Bot
    anlegt. Angelegt wird sie VOR dem Lauf; ob sie geschlossen wird,
    entscheidet danach der Ablauf."""
    verbindung = sqlite3.connect(db)
    verbindung.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT,
            signal_time TEXT, entry_time TEXT, entry_price REAL,
            stop_price REAL, exit_time TEXT, exit_price REAL, result TEXT,
            pnl_pct REAL, status TEXT, UNIQUE(symbol, signal_time))
    """)
    verbindung.execute(
        "INSERT INTO trades (symbol, signal_time, entry_time, entry_price, "
        "stop_price, status) VALUES (?, ?, ?, ?, ?, 'open')",
        (symbol, entry_time, entry_time, entry_price, stop_price))
    verbindung.commit()
    verbindung.close()


# ===========================================================================
# 8 - Die echten Bots, wirklich ausgefuehrt
# ===========================================================================
def _welt_krypto(intervall, anzahl, bis_ende):
    """Eine Reihe, deren LETZTE Kerze zur Laufzeit noch laeuft.

    Sie wird relativ zu `jetzt` gebaut, damit der Lauf keine vorgegebene
    Startzeit braucht: was hier "laufende Kerze" heisst, ist es auch dann
    noch, wenn der Test in einer Stunde noch einmal laeuft.
    """
    laenge = abrufschutz.INTERVALL_MS[intervall]
    jetzt = abrufschutz.als_ms(abrufschutz.jetzt_utc())
    laufend = (jetzt // laenge) * laenge
    erste = laufend - (anzahl - 1) * laenge
    df = reihe(str(pd.to_datetime(erste, unit="ms")), anzahl, intervall)
    if not bis_ende:
        df = df.iloc[:-1].reset_index(drop=True)
    return df


def test_bot_t3_supertrend():
    abschnitt("8  strategies/t3_supertrend/forward_test.py, wirklich gestartet")

    # 220 Vier-Stunden-Kerzen; die letzte laeuft gerade. Nur sie hat ein
    # Tief, das den Stop der offenen Position reisst.
    welt = _welt_krypto("4h", 220, bis_ende=True)
    welt.loc[len(welt) - 1, "low"] = 1.0          # nur die LAUFENDE Kerze
    frisch = welt.iloc[:-1].reset_index(drop=True)

    with tempfile.TemporaryDirectory() as tmp:
        live_csv = os.path.join(tmp, "welt.csv")
        welt.to_csv(live_csv, index=False)
        abbild = baue_abbild(os.path.join(tmp, "repo"), "t3_supertrend",
                             live_csv)
        frisch.to_csv(os.path.join(abbild["daten"], "TESTUSDT_4h.csv"),
                      index=False)
        einstieg = str(welt.iloc[100]["open_time"])
        lege_offene_position(abbild["db"], "TESTUSDT", einstieg, 100.0, 50.0)

        protokoll = os.path.join(tmp, "abrufe.txt")
        meldungen = os.path.join(tmp, "meldungen.txt")
        rc, ausgabe = starte_bot(abbild, protokoll, meldungen)
        check("8.1 der Lauf geht durch", rc == 0, ausgabe[-1500:])
        check("8.2 frisches data/: der Bot ruft NICHT live ab",
              not os.path.exists(protokoll),
              open(protokoll).read() if os.path.exists(protokoll) else "")

        zeilen = trades(abbild["db"])
        check("8.3 die Position bleibt offen - das Tief der laufenden Kerze "
              "ist keine Entscheidungsgrundlage",
              len(zeilen) == 1 and zeilen[0][4] == "open", str(zeilen))
        check("8.4 nichts gemeldet, weil nichts zurueckgefallen ist",
              not os.path.exists(meldungen))


def test_bot_turtle_soup_crypto():
    abschnitt("9  strategies/turtle_soup_crypto/forward_test.py, "
              "wirklich gestartet")

    # Turtle Soup eroeffnet, wenn das Tief unter das Donchian-Tief faellt UND
    # der Schluss darueber zurueckkehrt. Genau das steht hier NUR in der
    # laufenden Kerze. Entscheidet der Bot auf ihr, entsteht ein Trade.
    welt = _welt_krypto("1d", 60, bis_ende=True)
    letzte = len(welt) - 1
    welt.loc[letzte, "low"] = 80.0
    welt.loc[letzte, "close"] = 100.0
    frisch = welt.iloc[:-1].reset_index(drop=True)

    with tempfile.TemporaryDirectory() as tmp:
        live_csv = os.path.join(tmp, "welt.csv")
        welt.to_csv(live_csv, index=False)
        abbild = baue_abbild(os.path.join(tmp, "repo"), "turtle_soup_crypto",
                             live_csv)
        frisch.to_csv(os.path.join(abbild["daten"], "TESTUSDT_1d.csv"),
                      index=False)

        protokoll = os.path.join(tmp, "abrufe.txt")
        meldungen = os.path.join(tmp, "meldungen.txt")
        rc, ausgabe = starte_bot(abbild, protokoll, meldungen)
        check("9.1 der Lauf geht durch", rc == 0, ausgabe[-1500:])
        check("9.2 kein Trade aus der laufenden Kerze",
              trades(abbild["db"]) == [], str(trades(abbild["db"])))

        # Und jetzt mit VERALTETEM data/: der Rueckfall greift, der Live-Abruf
        # liefert dieselbe Reihe INKLUSIVE laufender Kerze - und trotzdem darf
        # kein Trade entstehen. Das ist die Pruefung, dass der Ausnahmefall
        # nicht anders rechnet als der Normalfall.
        os.remove(os.path.join(abbild["daten"], "TESTUSDT_1d.csv"))
        welt.iloc[:-5].to_csv(
            os.path.join(abbild["daten"], "TESTUSDT_1d.csv"), index=False)
        os.remove(abbild["db"])
        rc, ausgabe = starte_bot(abbild, protokoll, meldungen)
        check("9.3 veraltetes data/: der Lauf geht durch", rc == 0,
              ausgabe[-1500:])
        check("9.4 veraltetes data/: der Live-Abruf wurde benutzt",
              os.path.exists(protokoll) and "TESTUSDT" in open(protokoll).read())
        check("9.5 veraltetes data/: trotzdem kein Trade aus der laufenden "
              "Kerze", trades(abbild["db"]) == [],
              str(trades(abbild["db"])))
        check("9.6 veraltetes data/: es wurde GENAU EINMAL gemeldet",
              os.path.exists(meldungen)
              and len(open(meldungen).read().strip().splitlines()) == 1,
              open(meldungen).read() if os.path.exists(meldungen) else "keine")


def test_bot_turtle_soup_stocks():
    abschnitt("10 strategies/turtle_soup_stocks/forward_test.py, "
              "wirklich gestartet")

    kalender = ek._boersenkalender()
    if kalender is None or not getattr(kalender, "bibliothek_verfuegbar",
                                       lambda: False)():
        print("    uebersprungen: ohne pandas_market_calendars kann der "
              "Aktien-Bot seine Entscheidungskerze nicht am Sitzungsschluss "
              "festmachen (er faellt dann auf die sichere Schranke zurueck - "
              "geprueft in 6.10 bis 6.12).")
        return

    # Die Reihe endet am letzten geschlossenen Handelstag; die Zeile danach
    # ist die laufende Tageszeile. Nur sie traegt das Turtle-Soup-Signal.
    jetzt = abrufschutz.jetzt_utc()
    letzter, _g = ek.letzter_handelstag(jetzt, kalender)
    if letzter is None:
        print("    uebersprungen: der Kalender nennt keinen letzten "
              "Handelstag.")
        return

    tage = pd.bdate_range(end=letzter, periods=60).to_pydatetime()
    df = pd.DataFrame({
        "open_time": pd.to_datetime([t.date().isoformat() for t in tage]),
        "open": [100.0] * 60, "high": [101.0] * 60, "low": [99.0] * 60,
        "close": [100.0] * 60, "volume": [10.0] * 60,
    })
    laufend = pd.DataFrame({
        "open_time": [pd.Timestamp(
            (dt.date.fromisoformat(letzter) + dt.timedelta(days=1)).isoformat())],
        "open": [100.0], "high": [101.0], "low": [80.0], "close": [100.0],
        "volume": [10.0]})
    welt = pd.concat([df, laufend], ignore_index=True)

    with tempfile.TemporaryDirectory() as tmp:
        live_csv = os.path.join(tmp, "welt.csv")
        welt.to_csv(live_csv, index=False)
        abbild = baue_abbild(os.path.join(tmp, "repo"), "turtle_soup_stocks",
                             live_csv)
        df.to_csv(os.path.join(abbild["daten"], "TESTAG_1d.csv"), index=False)

        protokoll = os.path.join(tmp, "abrufe.txt")
        meldungen = os.path.join(tmp, "meldungen.txt")
        rc, ausgabe = starte_bot(abbild, protokoll, meldungen)
        check("10.1 der Lauf geht durch", rc == 0, ausgabe[-1500:])
        check("10.2 frisches data/: kein Live-Abruf",
              not os.path.exists(protokoll))
        check("10.3 kein Trade aus der laufenden Tageszeile",
              trades(abbild["db"]) == [], str(trades(abbild["db"])))


# ===========================================================================
# 11 - Backtest und Forward-Test waehlen dieselbe Kerze
# ===========================================================================
def test_gleiche_kerze_wie_backtest():
    abschnitt("11 Backtest und Forward-Test waehlen dieselbe Kerze")

    # Die eigentliche Zusicherung dieser Aufgabe, und sie wird NICHT gegen
    # eine nachgebaute Backtest-Regel geprueft, sondern gegen den ECHTEN
    # Schreibweg des Projekts:
    #
    #   Was der Backtest sieht, ist die CSV, die `fetch_*.py` geschrieben hat.
    #   Die schreibt seit TB-35 genau das, was `abrufschutz.nur_abgeschlossene`
    #   durchlaesst - eine Regel, die UNABHAENGIG von dieser Schicht
    #   geschrieben wurde und sie nicht kennt.
    #
    # Geprueft wird also: liefert `abrufschutz` (Schreibpfad, `<=`) dieselbe
    # letzte Kerze wie `entscheidungskerze` (Lesepfad, `<`)? Ueberall ausser
    # auf der Millisekunde der Grenze muessen beide dieselbe nennen.
    fehlgriffe = []
    for intervall, erste, anzahl in [("1h", "2026-09-10 00:00:00", 200),
                                     ("4h", "2026-09-01 00:00:00", 100),
                                     ("1d", "2026-06-01 00:00:00", 120)]:
        laenge = abrufschutz.INTERVALL_MS[intervall]
        welt = reihe(erste, anzahl, intervall)
        basis = abrufschutz.als_ms(ek._als_zeitpunkt(erste))
        # `laenge - 1` waere genau die Millisekunde der Grenze - der eine
        # Zeitpunkt, an dem sich beide Wege unterscheiden MUESSEN. Er wird
        # weiter unten getrennt geprueft, nicht hier uebergangen.
        for schritt in range(5, anzahl):
            for versatz in (1, laenge // 3, laenge // 2, laenge - 2):
                stand_ms = basis + schritt * laenge + versatz
                startzeit = pd.to_datetime(stand_ms, unit="ms").to_pydatetime()

                # Backtest-Seite: die CSV, wie `fetch_*.py` sie zu diesem
                # Zeitpunkt schriebe. Deren letzte Zeile ist die letzte Kerze,
                # auf der ein Backtest entscheidet.
                geschrieben, _v = abrufschutz.nur_abgeschlossene(
                    welt, intervall, stand=startzeit, melden=False)
                backtest = str(geschrieben.iloc[-1]["open_time"])

                # Forward-Seite: dieselbe Welt, dieselbe Startzeit.
                zeile = ek.entscheidungskerze(welt, intervall, ek.KRYPTO,
                                              startzeit)
                forward = str(zeile["open_time"]) if zeile is not None else None
                if backtest != forward:
                    fehlgriffe.append((intervall, str(startzeit), backtest,
                                       forward))

    check("11.1 ueber alle Zeitpunkte: Schreibpfad und Lesepfad nennen "
          "dieselbe letzte Kerze", not fehlgriffe,
          f"{len(fehlgriffe)} Abweichung(en), z.B. {fehlgriffe[:3]}")

    # Und der eine Zeitpunkt, an dem sie sich UNTERSCHEIDEN muessen: genau
    # auf der Grenze. Das ist keine Panne, sondern die Vorgabe (eine Kerze,
    # deren close_time GENAU auf der Startzeit liegt, wird nicht genommen) -
    # und es wird hier festgehalten, damit es niemand fuer einen Fehler haelt.
    for intervall, erste, anzahl in [("1h", "2026-09-10 00:00:00", 200),
                                     ("4h", "2026-09-01 00:00:00", 100),
                                     ("1d", "2026-06-01 00:00:00", 120)]:
        laenge = abrufschutz.INTERVALL_MS[intervall]
        welt = reihe(erste, anzahl, intervall)
        basis = abrufschutz.als_ms(ek._als_zeitpunkt(erste))
        schritt = 40
        grenze_ms = basis + schritt * laenge + (laenge - 1)
        grenze = pd.to_datetime(grenze_ms, unit="ms").to_pydatetime()
        geschrieben, _v = abrufschutz.nur_abgeschlossene(
            welt, intervall, stand=grenze, melden=False)
        zeile = ek.entscheidungskerze(welt, intervall, ek.KRYPTO, grenze)
        schreib = abrufschutz.als_ms(
            geschrieben.iloc[-1]["open_time"].to_pydatetime())
        lese = abrufschutz.als_ms(zeile["open_time"].to_pydatetime())
        check(f"11.2 {intervall}: genau auf der Grenze nimmt der Schreibpfad "
              f"die Kerze, der Lesepfad nicht",
              schreib == basis + schritt * laenge
              and lese == basis + (schritt - 1) * laenge,
              f"{geschrieben.iloc[-1]['open_time']} / {zeile['open_time']}")

    # Der Backtest-Lader des Projekts liest die CSV unveraendert ein. Ist
    # data/ frisch, ist die letzte Zeile der CSV die Entscheidungskerze -
    # und die Schicht gibt die CSV dann unveraendert weiter.
    with tempfile.TemporaryDirectory() as tmp:
        ordner = os.path.join(tmp, "data")
        startzeit = "2026-09-15 12:05:00"
        frisch = reihe("2026-09-14 00:00:00", 9, "4h")
        _ordner_mit(frisch, "TESTUSDT", "4h", ordner)
        aus_schicht = ek.lade("TESTUSDT", "4h", ek.KRYPTO,
                              Abrufattrappe(frisch), datenordner=ordner,
                              startzeit=startzeit, sammler=ek.Sammler(),
                              melden=False)
        wie_backtest = pd.read_csv(
            os.path.join(ordner, "TESTUSDT_4h.csv"), parse_dates=["open_time"])
        check("11.3 frisches data/: die Schicht gibt dieselbe Tabelle weiter, "
              "die der Backtest-Lader liest",
              aus_schicht.reset_index(drop=True).equals(wie_backtest),
              f"{len(aus_schicht)} vs {len(wie_backtest)} Zeilen")


# ===========================================================================
# 12 - Mutationsproben
# ===========================================================================
def _mit_mutation(setzen, zuruecksetzen, probe):
    """Eine Absicherung abschalten, die Probe laufen lassen, zurueckstellen.

    Zurueck kommt True, wenn die Probe FEHLSCHLAEGT - das ist hier das
    gewuenschte Ergebnis: eine Pruefung, die ohne ihre Absicherung gruen
    bleibt, prueft nichts.
    """
    setzen()
    try:
        return not probe()
    except Exception:                                       # noqa: BLE001
        return True
    finally:
        zuruecksetzen()


def test_mutationsproben():
    abschnitt("12 Mutationsproben: was faellt aus, wenn die Wache fehlt?")

    startzeit = "2026-09-15 12:05:00"
    veraltet = reihe("2026-09-14 00:00:00", 8, "4h")     # bis 2026-09-15 04:00
    live = reihe("2026-09-14 00:00:00", 10, "4h", tief={9: 1.0})

    def probe_normalfall():
        """Aus frischem data/ darf nie eine laufende Kerze kommen."""
        with tempfile.TemporaryDirectory() as tmp:
            # Eine Kursdatei, in der (wie in Altbestaenden) noch die
            # laufende Kerze steht. Der Filter muss sie abschneiden.
            ordner = _ordner_mit(reihe("2026-09-14 00:00:00", 10, "4h"),
                                 "TESTUSDT", "4h", os.path.join(tmp, "data"))
            df = ek.lade("TESTUSDT", "4h", ek.KRYPTO, Abrufattrappe(live),
                         datenordner=ordner, startzeit=startzeit,
                         sammler=ek.Sammler(), melden=False)
            return str(df.iloc[-1]["open_time"]) == "2026-09-15 08:00:00"

    def probe_rueckfall():
        """Aus dem Rueckfall-Abruf darf nie eine laufende Kerze kommen."""
        with tempfile.TemporaryDirectory() as tmp:
            ordner = _ordner_mit(veraltet, "TESTUSDT", "4h",
                                 os.path.join(tmp, "data"))
            abruf = Abrufattrappe(live)
            df = ek.lade("TESTUSDT", "4h", ek.KRYPTO, abruf,
                         datenordner=ordner, startzeit=startzeit,
                         sammler=ek.Sammler(), melden=False)
            return (abruf.aufrufe == 1
                    and str(df.iloc[-1]["open_time"]) == "2026-09-15 08:00:00")

    def probe_frische():
        """Veraltetes data/ muss den Live-Abruf ausloesen."""
        with tempfile.TemporaryDirectory() as tmp:
            ordner = _ordner_mit(veraltet, "TESTUSDT", "4h",
                                 os.path.join(tmp, "data"))
            abruf = Abrufattrappe(live)
            ek.lade("TESTUSDT", "4h", ek.KRYPTO, abruf, datenordner=ordner,
                    startzeit=startzeit, sammler=ek.Sammler(), melden=False)
            return abruf.aufrufe == 1

    def probe_grenze():
        """Auf der Grenze wird die Kerze NICHT genommen."""
        df = reihe("2026-09-14 00:00:00", 10, "4h")
        zeile = ek.entscheidungskerze(df, "4h", ek.KRYPTO,
                                      "2026-09-15 11:59:59.999000")
        return str(zeile["open_time"]) == "2026-09-15 04:00:00"

    def probe_daempfung():
        """Ein unveraenderter Befund wird beim zweiten Mal nicht gemeldet."""
        with tempfile.TemporaryDirectory() as tmp:
            zustand = os.path.join(tmp, "z.json")
            sammler = ek.Sammler()
            sammler.erfasse("AAAUSDT", ek.VERALTET, "Grund")
            ek.melde("b", sammler, Sendeattrappe(), zustand,
                     jetzt=dt.datetime(2026, 9, 15, 12, 0))
            zweiter = Sendeattrappe()
            ek.melde("b", sammler, zweiter, zustand,
                     jetzt=dt.datetime(2026, 9, 15, 16, 0))
            return not zweiter.texte

    def probe_schweigen():
        """Ohne Rueckfall wird geschwiegen - und zwar WEIL die Daempfung das
        sagt, nicht wegen einer zweiten Abfrage daneben."""
        with tempfile.TemporaryDirectory() as tmp:
            senden = Sendeattrappe()
            ek.melde("b", ek.Sammler(), senden, os.path.join(tmp, "z.json"),
                     jetzt=dt.datetime(2026, 9, 15, 12, 0))
            return not senden.texte

    # Die Proben muessen zunaechst alle GRUEN sein - sonst sagt eine rote
    # Mutationsprobe unten nichts aus.
    for name, probe in [("Normalfall", probe_normalfall),
                        ("Rueckfall", probe_rueckfall),
                        ("Frische", probe_frische),
                        ("Grenze", probe_grenze),
                        ("Daempfung", probe_daempfung),
                        ("Schweigen", probe_schweigen)]:
        check(f"12.0 Probe '{name}' ist ohne Mutation gruen", probe())

    # --- Mutation 1: der Filter wird ganz ausgeschaltet ------------------
    echt_nur_entscheidbar = ek.nur_entscheidbar

    def ohne_filter(df, *a, **k):
        return df, 0, None

    check("12.1 ohne den Filter faellt der Normalfall durch",
          _mit_mutation(
              lambda: setattr(ek, "nur_entscheidbar", ohne_filter),
              lambda: setattr(ek, "nur_entscheidbar", echt_nur_entscheidbar),
              probe_normalfall))
    check("12.2 ohne den Filter faellt auch der Rueckfall durch",
          _mit_mutation(
              lambda: setattr(ek, "nur_entscheidbar", ohne_filter),
              lambda: setattr(ek, "nur_entscheidbar", echt_nur_entscheidbar),
              probe_rueckfall))

    # --- Mutation 2: der Filter greift NUR im Normalfall -----------------
    # Die zweite wiederkehrende Falle: eine Wache verdeckt das Fehlen der
    # anderen. Hier wird der Filter nur fuer den Rueckfallweg abgeschaltet -
    # der Normalfall bleibt gruen, der Rueckfall MUSS durchfallen.
    echt_lade = ek.lade

    def lade_ohne_filter_im_rueckfall(symbol, intervall, markt, abruf,
                                      datenordner=None, startzeit=None,
                                      sammler=None, melden=True,
                                      kalender=None):
        sammler = ek.SAMMLER if sammler is None else sammler
        pfad = os.path.join(datenordner or ek.STANDARD_DATENORDNER,
                            f"{symbol}_{intervall}.csv")
        df, art, grund = ek._aus_datei(pfad, symbol, intervall, markt,
                                       startzeit, False, kalender)
        if art is not None:
            sammler.erfasse(symbol, art, grund)
            return abruf()                      # <- ungefiltert
        gefiltert, _v, _h = ek.nur_entscheidbar(df, intervall, markt,
                                                startzeit, melden=False,
                                                kalender=kalender)
        return gefiltert

    check("12.3 Filter nur im Normalfall: der Normalfall bleibt gruen",
          not _mit_mutation(
              lambda: setattr(ek, "lade", lade_ohne_filter_im_rueckfall),
              lambda: setattr(ek, "lade", echt_lade),
              probe_normalfall))
    check("12.4 Filter nur im Normalfall: der Rueckfall faellt durch - "
          "die eine Wache verdeckt das Fehlen der anderen NICHT",
          _mit_mutation(
              lambda: setattr(ek, "lade", lade_ohne_filter_im_rueckfall),
              lambda: setattr(ek, "lade", echt_lade),
              probe_rueckfall))

    # --- Mutation 3: die Frischepruefung sagt immer "frisch" -------------
    echt_ist_frisch = ek.ist_frisch
    check("12.5 ohne Frischepruefung faellt der Rueckfall durch",
          _mit_mutation(
              lambda: setattr(ek, "ist_frisch",
                              lambda *a, **k: (True, None)),
              lambda: setattr(ek, "ist_frisch", echt_ist_frisch),
              probe_frische))

    # --- Mutation 4: aus dem strikten `<` wird ein `<=` ------------------
    echt_stand = ek._stand_fuer_abrufschutz
    check("12.6 aus '<' ein '<=': die Grenzpruefung faellt durch",
          _mit_mutation(
              lambda: setattr(ek, "_stand_fuer_abrufschutz", lambda z: z),
              lambda: setattr(ek, "_stand_fuer_abrufschutz", echt_stand),
              probe_grenze))

    # --- Mutation 5: die Daempfung faellt weg ---------------------------
    echt_waechter = ek._waechter_melden
    check("12.7 ohne die Daempfung faellt die Daempfungspruefung durch",
          _mit_mutation(
              lambda: setattr(ek, "_waechter_melden", lambda: None),
              lambda: setattr(ek, "_waechter_melden", echt_waechter),
              probe_daempfung))

    # --- Mutation 6: die Entscheidung sagt immer "melden" ---------------
    # Wenn das Schweigen trotzdem bliebe, gaebe es eine ZWEITE Abfrage
    # daneben - und `entscheidung()` waere gar nicht die wirksame Wache.
    wm = ek._waechter_melden()
    if wm is None:
        check("12.8 waechter_melden ist einbindbar", False,
              "Modul nicht gefunden")
    else:
        echt_entscheidung = wm.entscheidung
        check("12.8 sagt die Daempfung 'melden', wird auch bei leerem "
              "Sammler gemeldet - es gibt keine zweite Wache daneben",
              _mit_mutation(
                  lambda: setattr(wm, "entscheidung",
                                  lambda *a, **k: (True, "neu")),
                  lambda: setattr(wm, "entscheidung", echt_entscheidung),
                  probe_schweigen))


# ===========================================================================
# 13 - Die neun Bots sind wirklich umgestellt
# ===========================================================================
def test_alle_neun_umgestellt():
    abschnitt("13 Alle neun forward_test.py gehen durch die Schicht")

    for pfad in sorted(glob.glob(os.path.join(BASE_DIR, "strategies", "*",
                                              "forward_test.py"))):
        bot = os.path.basename(os.path.dirname(pfad))
        with open(pfad, encoding="utf-8") as datei:
            quelle = datei.read()
        baum = ast.parse(quelle)

        # `entscheidungskerze.lade(...)` und `.melde()` kommen vor.
        aufrufe = [k for k in ast.walk(baum) if isinstance(k, ast.Call)
                   and isinstance(k.func, ast.Attribute)
                   and isinstance(k.func.value, ast.Name)
                   and k.func.value.id == "entscheidungskerze"]
        namen = {k.func.attr for k in aufrufe}
        check(f"13.1 {bot}: benutzt entscheidungskerze.lade",
              "lade" in namen, str(sorted(namen)))
        check(f"13.2 {bot}: meldet einmal je Lauf",
              "melde" in namen, str(sorted(namen)))

        # `fetch_historical_data` wird NUR noch innerhalb des `abruf`-Lambdas
        # gerufen - ein uebersehener Direktaufruf waere ein Bot, der an der
        # Schicht vorbei entscheidet.
        in_lambda = set()
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.Lambda):
                for unten in ast.walk(knoten):
                    if isinstance(unten, ast.Call):
                        in_lambda.add(id(unten))
        direkt = [k for k in ast.walk(baum) if isinstance(k, ast.Call)
                  and isinstance(k.func, ast.Name)
                  and k.func.id == "fetch_historical_data"
                  and id(k) not in in_lambda]
        check(f"13.3 {bot}: kein Direktaufruf von fetch_historical_data mehr",
              not direkt,
              f"{len(direkt)} Aufruf(e), Zeile(n) "
              f"{[k.lineno for k in direkt]}")

        # Und: `df.iloc[-1]` darf ruhig stehenbleiben - es bedeutet jetzt die
        # Entscheidungskerze. Geprueft wird deshalb NICHT der Quelltext,
        # sondern in Abschnitt 8 bis 10 der Ablauf.
    check("13.4 es sind neun Bots",
          len(glob.glob(os.path.join(BASE_DIR, "strategies", "*",
                                     "forward_test.py"))) == 9)


# ===========================================================================
# 14 - Was unberuehrt bleiben musste
# ===========================================================================
def test_unberuehrt():
    abschnitt("14 Was unberuehrt bleiben musste")

    check("14.1 abrufschutz: der neue Name ist derselbe Weg wie der alte",
          abrufschutz.oeffnungszeiten_ms is not None
          and list(abrufschutz.oeffnungszeiten_ms(
              pd.Series(pd.to_datetime(["2026-09-15 00:00:00"]))))
          == list(abrufschutz._oeffnungszeiten_ms(
              pd.Series(pd.to_datetime(["2026-09-15 00:00:00"])))))

    # Der Schreibpfad von TB-35 rechnet unveraendert mit `<=`.
    welt = reihe("2026-09-14 00:00:00", 10, "4h")   # bis 2026-09-15 12:00
    behalten, verworfen = abrufschutz.nur_abgeschlossene(
        welt, "4h", stand=ek._als_zeitpunkt("2026-09-15 11:59:59.999000"),
        melden=False)
    check("14.2 abrufschutz.nur_abgeschlossene verhaelt sich unveraendert: "
          "`<=` behaelt die 08:00-Kerze, verwirft die laufende 12:00-Kerze",
          verworfen == 1 and len(behalten) == 9
          and str(behalten.iloc[-1]["open_time"]) == "2026-09-15 08:00:00",
          f"verworfen={verworfen}, behalten={len(behalten)}")

    # Der Laufbeginn friert EINMAL ein.
    ek.laufbeginn_zuruecksetzen()
    erster = ek.laufbeginn()
    zweiter = ek.laufbeginn()
    check("14.3 der Laufbeginn ist innerhalb eines Prozesses derselbe Wert",
          erster == zweiter, f"{erster} vs {zweiter}")
    check("14.4 eine uebergebene Startzeit aendert den gemerkten Wert nicht",
          ek.laufbeginn("2020-01-01 00:00:00") != ek.laufbeginn()
          and ek.laufbeginn() == erster)

    # Keine Umgebungsvariable soll den Laufbeginn setzen koennen - eine
    # vergessene `export`-Zeile wuerde neun Bots lautlos einfrieren.
    quelle = open(os.path.join(_SHARED, "entscheidungskerze.py"),
                  encoding="utf-8").read()
    baum = ast.parse(quelle)
    umgebungszugriffe = [k for k in ast.walk(baum) if isinstance(k, ast.Call)
                         and isinstance(k.func, ast.Attribute)
                         and k.func.attr in ("getenv",)]
    check("14.5 der Laufbeginn kommt nie aus der Umgebung",
          not umgebungszugriffe, f"{len(umgebungszugriffe)} Zugriff(e)")


# ===========================================================================
def main():
    print("=" * 78)
    print("Selbsttests shared/entscheidungskerze.py (TB-38)")
    print("=" * 78)

    test_regel_krypto()
    test_regel_aktien()
    test_regel_grenze()
    test_echter_kalender()
    test_zwei_wege_ein_ergebnis()
    test_rueckfall()
    test_meldung()
    test_bot_t3_supertrend()
    test_bot_turtle_soup_crypto()
    test_bot_turtle_soup_stocks()
    test_gleiche_kerze_wie_backtest()
    test_mutationsproben()
    test_alle_neun_umgestellt()
    test_unberuehrt()

    print("\n" + "=" * 78)
    if FEHLER:
        print(f"{len(FEHLER)} FEHLER von {BESTANDEN + len(FEHLER)} Pruefungen:")
        for zeile in FEHLER:
            print(f"  - {zeile}")
        return 1
    print(f"Alle {BESTANDEN} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
