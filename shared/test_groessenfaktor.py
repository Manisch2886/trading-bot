#!/usr/bin/env python3
"""
Selbsttests zu shared/groessenfaktor.py und den neun Bots (TB-42, Teil 2)
==============================================================================
Geprueft wird, was die Aufgabe als nicht verhandelbar nennt:

* Fehlt die Datei          -> 1,0, der Bot laeuft unveraendert weiter.
* Ist sie unlesbar         -> 1,0 UND eine Meldung.
* Fehlt der eigene Bot     -> 1,0 UND eine Meldung.
* Wert ausserhalb 0,25-4,0 -> 1,0 UND eine Meldung. NICHT Uebernahme.
* Der Wert wird je Lauf protokolliert.
* Ein gueltiger Wert wirkt GENAU an der Positionsgroesse und sonst nirgends.

WIE DER LETZTE PUNKT GEPRUEFT WIRD
------------------------------------------------------------------------------
Nicht am Quelltext, sondern am Ablauf: derselbe Forward-Test-Lauf wird ZWEIMAL
gestartet - einmal mit m_b = 1,0, einmal mit m_b = 0,5 -, auf denselben
erzeugten Kursdaten und mit je frischer Datenbank. Danach werden die beiden
Trade-Tabellen Spalte fuer Spalte verglichen: alles gleich, nur
`groessenfaktor` verschieden. Waere der Multiplikator irgendwo in ein Signal,
eine Schwelle oder eine Positionszahl geraten, stuenden hier andere Ein- oder
Ausstiegszeitpunkte.

Damit das etwas heisst, muss der Lauf ueberhaupt Trades erzeugen. Er tut es
gegen erzeugte Beispieldaten; **ein Lauf ohne Trade laesst diese Pruefung
fehlschlagen** statt sie leer bestehen zu lassen. Genau das ist die Falle
"eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
selbst" - hier wird der Ablauf beobachtet, nicht behauptet.

Die echten Bot-Datenbanken, die echten Kursdaten und die echte
`config/groessenfaktor.json` werden dabei NICHT angefasst: jeder Lauf bekommt
eigene Ordner unter /tmp, untergeschoben ueber ein `sitecustomize.py`, das nur
die EINGABEN ersetzt (Kursdatenordner, Datenbankpfad, Pfad der Faktordatei).
Kein Bot-Code wird veraendert.

Binance und yfinance sind aus der Cloud gesperrt - deshalb liegen fuer JEDES
Symbol des Bots Beispieldaten bereit, damit kein Live-Abruf versucht wird.

Nutzung:  python3 shared/test_groessenfaktor.py
          python3 shared/test_groessenfaktor.py --nur 1,2      (ohne Laeufe)
          python3 shared/test_groessenfaktor.py --bots t3_supertrend
"""

import argparse
import contextlib
import datetime as dt
import glob
import io
import json
import math
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

import groessenfaktor as gf                                     # noqa: E402

BOTS = sorted(os.path.basename(os.path.dirname(p)) for p in
              glob.glob(os.path.join(BASE_DIR, "strategies", "*", "forward_test.py")))

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
    else:
        FEHLER.append(f"{name}" + (f"  [{detail}]" if detail else ""))
    return bool(bedingung)


def schreibe_json(pfad, inhalt):
    with open(pfad, "w") as f:
        if isinstance(inhalt, str):
            f.write(inhalt)
        else:
            json.dump(inhalt, f)
    return pfad


# ===========================================================================
# 1. Die Leseseite
# ===========================================================================
def test_lesen():
    ordner = tempfile.mkdtemp(prefix="tb42_faktor_")
    try:
        fehlt = os.path.join(ordner, "gibt-es-nicht.json")

        wert, zeile, meldungen = gf.bestimme("t3_supertrend", fehlt)
        check("1.1 fehlende Datei -> 1,0", wert == 1.0, repr(wert))
        check("1.2 fehlende Datei ist keine Beanstandung", meldungen == [], str(meldungen))
        check("1.3 fehlende Datei wird trotzdem protokolliert",
              "1,0" in zeile and "fehlt" in zeile, zeile)

        kaputt = schreibe_json(os.path.join(ordner, "kaputt.json"), "{ das ist kein JSON")
        wert, zeile, meldungen = gf.bestimme("t3_supertrend", kaputt)
        check("1.4 unlesbare Datei -> 1,0", wert == 1.0, repr(wert))
        check("1.5 unlesbare Datei -> Meldung", len(meldungen) == 1, str(meldungen))

        for name, inhalt in (("ohne_bots", {"quartal": "2026Q4"}),
                              ("bots_keine_abbildung", {"bots": [1, 2, 3]}),
                              ("liste_statt_objekt", [1, 2, 3])):
            pfad = schreibe_json(os.path.join(ordner, name + ".json"), inhalt)
            wert, _z, meldungen = gf.bestimme("t3_supertrend", pfad)
            check(f"1.6 unvollstaendig ({name}) -> 1,0 und Meldung",
                  wert == 1.0 and len(meldungen) == 1, f"{wert} {meldungen}")

        fremd = schreibe_json(os.path.join(ordner, "fremd.json"),
                              {"bots": {"rsi2_crypto": 2.0}})
        wert, _z, meldungen = gf.bestimme("t3_supertrend", fremd)
        check("1.7 eigener Bot fehlt -> 1,0 und Meldung",
              wert == 1.0 and len(meldungen) == 1, f"{wert} {meldungen}")
        wert2, _z, meldungen2 = gf.bestimme("rsi2_crypto", fremd)
        check("1.8 der aufgefuehrte Bot bekommt seinen Wert",
              wert2 == 2.0 and meldungen2 == [], f"{wert2} {meldungen2}")

        for beschreibung, roh in (("Zeichenkette", "1.5"), ("null", None),
                                   ("Wahrheitswert", True), ("Liste", [1.0]),
                                   ("Objekt", {"wert": 1.0})):
            pfad = schreibe_json(os.path.join(ordner, "typ.json"),
                                 {"bots": {"t3_supertrend": roh}})
            wert, _z, meldungen = gf.bestimme("t3_supertrend", pfad)
            check(f"1.9 {beschreibung} ist keine Zahl -> 1,0 und Meldung",
                  wert == 1.0 and len(meldungen) == 1, f"{wert} {meldungen}")

        # Der Bereich. NaN und Unendlich gehoeren dazu: beide sind Zahlen und
        # muessen an DERSELBEN Wache scheitern - eine zweite daneben wuerde
        # nur verdecken, wenn diese verschwaende.
        aussen = [0, 0.0, -1.0, 0.24, 4.01, 50.0, 1e9, -0.5]
        for w in aussen:
            pfad = schreibe_json(os.path.join(ordner, "bereich.json"),
                                 {"bots": {"t3_supertrend": w}})
            wert, _z, meldungen = gf.bestimme("t3_supertrend", pfad)
            check(f"1.10 {w!r} liegt ausserhalb -> 1,0 und Meldung",
                  wert == 1.0 and len(meldungen) == 1, f"{wert} {meldungen}")

        for text, w in (("NaN", float("nan")), ("Unendlich", float("inf")),
                         ("minus Unendlich", float("-inf"))):
            pfad = os.path.join(ordner, "sonderzahl.json")
            with open(pfad, "w") as f:
                f.write('{"bots": {"t3_supertrend": %s}}'
                        % {"NaN": "NaN", "Unendlich": "Infinity",
                           "minus Unendlich": "-Infinity"}[text])
            wert, _z, meldungen = gf.bestimme("t3_supertrend", pfad)
            check(f"1.11 {text} -> 1,0 und Meldung",
                  wert == 1.0 and len(meldungen) == 1, f"{wert} {meldungen}")

        for w in (0.25, 0.5, 1.0, 2.0, 4.0, 3):
            pfad = schreibe_json(os.path.join(ordner, "gut.json"),
                                 {"quartal": "2026Q4", "bots": {"t3_supertrend": w}})
            wert, zeile, meldungen = gf.bestimme("t3_supertrend", pfad)
            check(f"1.12 {w!r} ist gueltig und wird uebernommen",
                  wert == float(w) and meldungen == [], f"{wert} {meldungen}")
            check(f"1.13 {w!r} wird protokolliert",
                  "2026Q4" in zeile, zeile)

        check("1.14 die Grenzen sind symmetrisch (4 = 1/0,25)",
              abs(gf.OBERGRENZE * gf.UNTERGRENZE - 1.0) < 1e-12,
              f"{gf.UNTERGRENZE} {gf.OBERGRENZE}")

        # lies() darf einen Bot-Lauf nie anhalten.
        for pfad in (fehlt, kaputt, ordner, os.path.join(ordner, "\0ungueltig")):
            puffer = io.StringIO()
            try:
                with contextlib.redirect_stdout(puffer):
                    wert = gf.lies("t3_supertrend", pfad)
                heil = wert == 1.0
            except Exception as fehler:                          # noqa: BLE001
                heil, wert = False, fehler
            check(f"1.15 lies() wirft nie ({os.path.basename(str(pfad))[:20]})",
                  heil, repr(wert))
            check("1.16 jeder Aufruf hinterlaesst genau eine Protokollzeile",
                  len([z for z in puffer.getvalue().splitlines()
                       if z.startswith("Groessenfaktor ")]) == 1,
                  puffer.getvalue())

        check("1.17 der Bot-Name wird aus __file__ abgeleitet",
              gf.botname(os.path.join(BASE_DIR, "strategies", "t3_supertrend",
                                       "forward_test.py")) == "t3_supertrend")
        check("1.18 der Standardpfad liegt in config/",
              gf.standardpfad() == os.path.join(BASE_DIR, "config",
                                                 "groessenfaktor.json"),
              gf.standardpfad())
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


# ===========================================================================
# 2. Die Spalte in der Datenbank
# ===========================================================================
def test_spalte():
    ordner = tempfile.mkdtemp(prefix="tb42_db_")
    try:
        pfad = os.path.join(ordner, "alt.db")
        conn = sqlite3.connect(pfad)
        # Eine Tabelle wie die der Bots VOR TB-42.
        conn.execute("CREATE TABLE trades (id INTEGER PRIMARY KEY, symbol TEXT, "
                     "pnl_pct REAL, status TEXT)")
        conn.execute("INSERT INTO trades (symbol, pnl_pct, status) "
                     "VALUES ('BTCUSDT', 1.5, 'closed')")
        conn.commit()

        spalten = lambda: {z[1] for z in conn.execute("PRAGMA table_info(trades)")}
        check("2.1 die Altbestand-Tabelle hat die Spalte nicht",
              "groessenfaktor" not in spalten())
        check("2.2 spalte_anlegen ergaenzt sie", gf.spalte_anlegen(conn) is True)
        check("2.3 danach ist sie da", "groessenfaktor" in spalten())
        check("2.4 ein zweiter Aufruf ist folgenlos",
              gf.spalte_anlegen(conn) is False and "groessenfaktor" in spalten())

        alt = conn.execute("SELECT groessenfaktor FROM trades").fetchone()
        check("2.5 alte Trades behalten NULL statt einer erfundenen 1,0",
              alt[0] is None, repr(alt))
        conn.close()

        leer = sqlite3.connect(os.path.join(ordner, "ohne.db"))
        check("2.6 ohne Tabelle: kein Fehler, nichts getan",
              gf.spalte_anlegen(leer) is False)
        leer.close()
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


# ===========================================================================
# 3. Der Multiplikator am laufenden Bot
# ===========================================================================
# Je Bot: Zeitrahmen, Kerzenzahl, Symbolquelle und die Datenformen, die bei
# diesem Bot ein Signal ausloesen. Die erste Form ist die gemessene; die
# weiteren sind Ausweichformen, falls der Boersenkalender die
# Entscheidungskerze an einem anderen Wochentag anders legt.
LAUFBOTS = {
    "elliott_wave":               ("1h", 2200, "shared"),
    "elliott_wave_stocks":        ("1d", 1500, "stocks"),
    "rsi2_crypto":                ("1d", 1200, "shared"),
    "rsi2_mean_reversion":        ("1d", 1500, "stocks"),
    "t3_supertrend":              ("4h", 1200, "shared"),
    "turtle_soup_crypto":         ("1d", 1200, "shared"),
    "turtle_soup_stocks":         ("1d", 1500, "stocks"),
    "volatility_breakout":        ("1d", 1500, "stocks"),
    "volatility_breakout_crypto": ("1d", 1200, "shared"),
}

# Eine Datenform ist ("schwingung", Periode, Phase) oder ("impuls", Beinlaenge, 0).
#
# "schwingung" ist eine ueberlagerte Sinuskurve; sie erzeugt Kreuzungen,
# Ausbrueche und Rueckschlaege und damit Signale fuer sieben der neun Bots.
#
# "impuls" ist eine bearische Fuenf-Wellen-Struktur mit fibonacci-nahen
# Verhaeltnissen - die beiden Elliott-Wave-Bots suchen genau das und finden in
# einer Sinuskurve nichts. Die Zwischenpunkte sind so gewaehlt, dass alle drei
# Elliott-Regeln erfuellt sind (Welle 2 faellt nicht unter den Start, Welle 3
# ist nicht die kuerzeste, Welle 4 dringt nicht in Welle 1 ein) und jedes Bein
# groesser ist als DEVIATION_PCT beider Bots, damit der Zigzag es als Pivot
# sieht. Der Anstieg davor und die Gegenbewegung danach sind noetig, damit der
# erste und der letzte Punkt ueberhaupt als Pivot bestaetigt werden.
IMPULS = [80.0, 100.0, 85.0, 94.27, 70.0, 79.27, 64.27, 74.5]

FORMEN = {
    "t3_supertrend":              [("schwingung", 90.0, 15), ("schwingung", 90.0, 36)],
    "rsi2_crypto":                [("schwingung", 40.0, 33), ("schwingung", 40.0, 36)],
    "turtle_soup_crypto":         [("schwingung", 40.0, 6), ("schwingung", 40.0, 12)],
    "volatility_breakout_crypto": [("schwingung", 40.0, 3), ("schwingung", 40.0, 9)],
    "elliott_wave":               [("impuls", n, 0) for n in (15, 20, 12, 25, 10)],
    "elliott_wave_stocks":        [("impuls", n, 0) for n in (4, 3, 5, 2)],
}
# Wird bei einem Bot keine der gemessenen Formen faellig - etwa weil der
# Boersenkalender die Entscheidungskerze an einem anderen Wochentag anders
# legt -, wird weitergesucht statt die Pruefung leer bestehen zu lassen.
AUSWEICH = ([("schwingung", 40.0, p) for p in range(0, 40, 3)] +
            [("schwingung", 17.0, p) for p in range(0, 40, 3)] +
            [("schwingung", 90.0, p) for p in range(0, 40, 3)] +
            [("impuls", n, 0) for n in (15, 20, 4, 3, 10, 30, 6)])

SITECUSTOMIZE = '''\
"""Ersetzt vor dem Bot-Lauf NUR dessen Eingaben. Kein Bot-Code wird veraendert."""
import os, sys
sys.path.insert(0, os.path.join(os.environ["TB42_BASIS"], "shared"))
try:
    import binance.client
    binance.client.Client.ping = lambda self, *a, **k: {}
except ImportError:
    pass
import entscheidungskerze
entscheidungskerze.STANDARD_DATENORDNER = os.environ["TB42_DATEN"]
import strategy_paths
_echt = strategy_paths.get_strategy_paths
def _neu(f):
    p = _echt(f)
    p["DB_FILE"] = os.path.join(os.environ["TB42_DB"], os.path.basename(p["DB_FILE"]))
    return p
strategy_paths.get_strategy_paths = _neu
import groessenfaktor
groessenfaktor.standardpfad = lambda: os.environ["TB42_FAKTORDATEI"]
'''


def _symbole(bot):
    quelle = LAUFBOTS[bot][2]
    if quelle == "shared":
        pfad = os.path.join(BASE_DIR, "shared", "symbols_config.py")
    else:
        pfad = os.path.join(BASE_DIR, "strategies", bot, "stocks_symbols_config.py")
    code = ("import sys; sys.path.insert(0, %r)\n"
            % os.path.join(BASE_DIR, "shared")) + open(pfad).read()
    ns = {"__file__": pfad, "__name__": "konfig"}
    exec(compile(code, pfad, "exec"), ns)                        # noqa: S102
    return list(ns["SYMBOLS"])


def _bahn_schwingung(n, periode, phase, k):
    return [100.0 * (1 + 0.30 * math.sin((i + phase + k * 7) / periode)
                     + 0.08 * math.sin((i + phase + k * 7) / (periode / 4.0))
                     + 0.02 * math.sin((i + phase + k * 7) / 2.3)
                     + i * 0.0010) for i in range(n)]


def _bahn_impuls(n, n_je, k):
    """Ruhiger Vorlauf, dann die Fuenf-Wellen-Struktur bis ans Ende."""
    massstab = 1.0 + 0.01 * k
    vorlauf = max(1, n - n_je * len(IMPULS))
    werte = [IMPULS[0] * massstab * (1 + 0.02 * math.sin((i + k) / 9.0))
             for i in range(vorlauf)]
    stand = werte[-1]
    for ziel in IMPULS:
        ziel *= massstab
        for j in range(n_je):
            werte.append(stand + (ziel - stand) * (j + 1) / n_je)
        stand = ziel
    return werte


def _schreibe_daten(ordner, symbole, intervall, n, form):
    art, a, b = form
    os.makedirs(ordner, exist_ok=True)
    schritt = {"1h": dt.timedelta(hours=1), "4h": dt.timedelta(hours=4),
               "1d": dt.timedelta(days=1)}[intervall]
    ende = dt.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    if intervall == "4h":
        ende = ende.replace(hour=(ende.hour // 4) * 4)
    elif intervall == "1d":
        ende = ende.replace(hour=0)
    for k, sym in enumerate(symbole):
        if art == "impuls":
            werte = _bahn_impuls(n, int(a), k)
        else:
            werte = _bahn_schwingung(n, a, b, k)
        anzahl = len(werte)
        with open(os.path.join(ordner, "%s_%s.csv" % (sym, intervall)), "w") as f:
            f.write("open_time,open,high,low,close,volume\n")
            for i, p in enumerate(werte):
                vorher = werte[i - 1] if i else p
                f.write("%s,%.6f,%.6f,%.6f,%.6f,%d\n"
                        % ((ende - schritt * (anzahl - 1 - i)).strftime("%Y-%m-%d %H:%M:%S"),
                           vorher, max(p, vorher) * 1.004, min(p, vorher) * 0.996,
                           p, 1000 + i))


def _lauf(bot, faktorinhalt, form, werkstatt, marke):
    """EIN echter Forward-Test-Lauf in eigenem Prozess. Gibt Trades und Ausgabe.

    Beispieldaten entstehen fuer JEDES Symbol des Bots, nicht nur fuer ein
    paar. Sonst faellt der Bot fuer den Rest auf den Live-Abruf zurueck - und
    der ist aus der Cloud gesperrt (403). Das kostet nicht nur Zeit: die
    beiden Elliott-Wave-Bots brechen bei einem leeren Kursrahmen mit
    IndexError ab (zigzag_indicator.calculate_zigzag, `highs[0]`), und dann
    misst der Lauf nicht mehr den Multiplikator, sondern die Sperre.
    """
    intervall, n, _q = LAUFBOTS[bot]
    arbeit = os.path.join(werkstatt, marke)
    d_daten, d_db = os.path.join(arbeit, "daten"), os.path.join(arbeit, "db")
    os.makedirs(d_db, exist_ok=True)
    _schreibe_daten(d_daten, _symbole(bot), intervall, n, form)

    fdatei = os.path.join(arbeit, "faktor.json")
    if faktorinhalt is not None:
        with open(fdatei, "w") as f:
            f.write(faktorinhalt if isinstance(faktorinhalt, str)
                    else json.dumps(faktorinhalt))

    harnisch = os.path.join(werkstatt, "_harness")
    # Fail closed. Ohne dieses sitecustomize.py laeuft der Bot NICHT gegen die
    # Wegwerf-Ordner, sondern gegen data/ und gegen die ECHTE Bot-Datenbank im
    # Projektordner. Gemessen: genau das ist einmal passiert, als der
    # Harnisch-Ordner waehrend eines Laufs von aussen geloescht wurde. Der Lauf
    # meldete danach nur "0 Trades" - still, wie die Loader vor Teil 1.
    if not os.path.exists(os.path.join(harnisch, "sitecustomize.py")):
        raise RuntimeError(
            "Der Testharnisch fehlt (%s). Ohne ihn wuerde der Bot in die ECHTE "
            "Datenbank schreiben - der Lauf wird abgebrochen." % harnisch)

    umgebung = dict(os.environ)
    umgebung.update({"TB42_BASIS": BASE_DIR, "TB42_DATEN": d_daten, "TB42_DB": d_db,
                     "TB42_FAKTORDATEI": fdatei,
                     "PYTHONPATH": harnisch})
    p = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "strategies", bot, "forward_test.py")],
        capture_output=True, text=True, env=umgebung, timeout=1800)

    db = os.path.join(d_db, "paper_trading_%s.db" % bot)
    # Und die Gegenprobe hinterher: liegt die Datenbank NICHT im Wegwerf-Ordner,
    # hat der Harnisch nicht gegriffen. Dann ist jede Zahl aus diesem Lauf
    # wertlos - und im Projektordner steht womoeglich eine neue Datei.
    if not os.path.exists(db):
        echte = os.path.join(BASE_DIR, "paper_trading_%s.db" % bot)
        raise RuntimeError(
            "Der Lauf hat keine Datenbank in %s angelegt - der Harnisch hat "
            "nicht gegriffen.%s\nAusgabe: %s" % (
                d_db,
                " ACHTUNG: %s existiert." % echte if os.path.exists(echte) else "",
                (p.stdout or "")[-500:]))
    trades, spalten = [], []
    if os.path.exists(db):
        c = sqlite3.connect(db)
        spalten = [z[1] for z in c.execute("PRAGMA table_info(trades)")]
        trades = [dict(zip(spalten, r)) for r in
                  c.execute("SELECT * FROM trades ORDER BY symbol, signal_time")]
        c.close()
    return {"trades": trades, "spalten": spalten, "ausgabe": p.stdout,
            "stderr": p.stderr, "rueckgabe": p.returncode}


def _finde_form(bot, werkstatt):
    """Sucht eine Datenform, bei der DIESER Bot einen Trade eroeffnet.

    Die gemessenen Formen stehen vorn; gefunden wird trotzdem durch Zusehen.
    """
    kandidaten = FORMEN.get(bot, []) + AUSWEICH
    gesehen = set()
    for i, form in enumerate(kandidaten):
        if form in gesehen:
            continue
        gesehen.add(form)
        e = _lauf(bot, {"quartal": "2026Q4", "bots": {bot: 1.0}}, form,
                  werkstatt, "suche%d" % i)
        if e["trades"]:
            return form, e
        shutil.rmtree(os.path.join(werkstatt, "suche%d" % i), ignore_errors=True)
    return None, None


def test_lauf(bots):
    for bot in bots:
        werkstatt = tempfile.mkdtemp(prefix="tb42_lauf_")
        try:
            os.makedirs(os.path.join(werkstatt, "_harness"), exist_ok=True)
            with open(os.path.join(werkstatt, "_harness", "sitecustomize.py"), "w") as f:
                f.write(SITECUSTOMIZE)

            form, eins = _finde_form(bot, werkstatt)
            if not check(f"3 {bot}: der Lauf erzeugt ueberhaupt einen Trade",
                         eins is not None,
                         "keine der geprueften Datenformen loest ein Signal aus - "
                         "diese Pruefung waere sonst leer bestanden"):
                continue

            # --- derselbe Lauf mit m_b = 0,5 ----------------------------------
            halb = _lauf(bot, {"quartal": "2026Q4", "bots": {bot: 0.5}}, form,
                         werkstatt, "halb")
            check(f"3 {bot}: beide Laeufe laufen durch",
                  eins["rueckgabe"] == 0 and halb["rueckgabe"] == 0,
                  f"{eins['rueckgabe']} / {halb['rueckgabe']}")
            check(f"3 {bot}: beide Laeufe erzeugen gleich viele Trades",
                  len(eins["trades"]) == len(halb["trades"]),
                  f"{len(eins['trades'])} / {len(halb['trades'])}")

            andere = [s for s in eins["spalten"] if s != "groessenfaktor"]
            gleich = all(a[s] == b[s] for a, b in zip(eins["trades"], halb["trades"])
                         for s in andere)
            check(f"3 {bot}: m_b=1,0 und m_b=0,5 erzeugen dieselben Ein- und "
                  f"Ausstiegszeitpunkte", gleich,
                  str([(a.get("symbol"), a.get("entry_time"), b.get("entry_time"))
                       for a, b in zip(eins["trades"], halb["trades"])
                       if any(a[s] != b[s] for s in andere)][:3]))
            check(f"3 {bot}: nur die Positionsgroesse unterscheidet sich",
                  all(a["groessenfaktor"] == 1.0 and b["groessenfaktor"] == 0.5
                      for a, b in zip(eins["trades"], halb["trades"])),
                  str([(a["groessenfaktor"], b["groessenfaktor"])
                       for a, b in zip(eins["trades"], halb["trades"])][:3]))

            # --- fehlende Datei -----------------------------------------------
            ohne = _lauf(bot, None, form, werkstatt, "ohne")
            check(f"3 {bot}: ohne Faktordatei laeuft der Bot weiter",
                  ohne["rueckgabe"] == 0 and len(ohne["trades"]) == len(eins["trades"]),
                  f"rc {ohne['rueckgabe']}, {len(ohne['trades'])} Trades")
            check(f"3 {bot}: ohne Faktordatei gilt 1,0",
                  all(t["groessenfaktor"] == 1.0 for t in ohne["trades"]),
                  str([t["groessenfaktor"] for t in ohne["trades"]][:3]))
            check(f"3 {bot}: der geltende Faktor steht im Lauf-Protokoll",
                  len([z for z in ohne["ausgabe"].splitlines()
                       if z.startswith("Groessenfaktor ")]) == 1,
                  ohne["ausgabe"][:300])

            # --- unlesbare Datei ----------------------------------------------
            kaputt = _lauf(bot, "{ kein JSON", form, werkstatt, "kaputt")
            check(f"3 {bot}: unlesbare Faktordatei haelt den Bot nicht an",
                  kaputt["rueckgabe"] == 0 and
                  len(kaputt["trades"]) == len(eins["trades"]),
                  f"rc {kaputt['rueckgabe']}")
            check(f"3 {bot}: unlesbare Faktordatei -> 1,0 UND Meldung",
                  all(t["groessenfaktor"] == 1.0 for t in kaputt["trades"]) and
                  "Warnung: Groessenfaktor" in kaputt["ausgabe"],
                  kaputt["ausgabe"][:300])

            # --- Wert ausserhalb des Bereichs ---------------------------------
            weit = _lauf(bot, {"bots": {bot: 50.0}}, form, werkstatt, "weit")
            check(f"3 {bot}: 50 wird NICHT uebernommen, es gilt 1,0",
                  all(t["groessenfaktor"] == 1.0 for t in weit["trades"]) and
                  "Warnung: Groessenfaktor" in weit["ausgabe"],
                  str([t["groessenfaktor"] for t in weit["trades"]][:3]))
            check(f"3 {bot}: auch mit 50 in der Datei entstehen dieselben Trades",
                  len(weit["trades"]) == len(eins["trades"]),
                  f"{len(weit['trades'])} / {len(eins['trades'])}")
        finally:
            shutil.rmtree(werkstatt, ignore_errors=True)


# ===========================================================================
# 4. Mutationsproben an der Leseseite
# ===========================================================================
def test_mutationen():
    """Jede entfernte Wache MUSS auffallen - und zwar jede FUER SICH.

    Genau hier sitzt die zweite wiederkehrende Falle: eine zweite Wache, die
    das Fehlen der ersten verdeckt. Deshalb wird je Mutation nur EINE Wache
    entfernt und dann geprueft, ob der Wert durchkommt.
    """
    quelle = open(os.path.join(_SHARED, "groessenfaktor.py")).read()

    mutationen = [
        ("Bereichswache entfernt",
         "    if not (UNTERGRENZE <= wert_roh <= OBERGRENZE):",
         "    if False:",
         [50.0, 0.0, -1.0], "die Bereichswache"),
        ("Typwache entfernt",
         "    if isinstance(roh, bool) or not isinstance(roh, (int, float)):",
         "    if False:",
         ["1.5"], "die Typwache"),
    ]

    for name, alt, neu, werte, was in mutationen:
        if not check(f"4 {name}: Ansatzpunkt eindeutig", quelle.count(alt) == 1,
                     str(quelle.count(alt))):
            continue
        ordner = tempfile.mkdtemp(prefix="tb42_mut_")
        try:
            pfad = os.path.join(ordner, "groessenfaktor.py")
            with open(pfad, "w") as f:
                f.write(quelle.replace(alt, neu))
            durchgekommen = []
            for w in werte:
                datei = schreibe_json(os.path.join(ordner, "f.json"),
                                      {"bots": {"t3_supertrend": w}})
                programm = (
                    "import sys; sys.path.insert(0, %r)\n"
                    "import groessenfaktor as g\n"
                    "print(g.bestimme('t3_supertrend', %r)[0])\n" % (ordner, datei))
                p = subprocess.run([sys.executable, "-c", programm],
                                   capture_output=True, text=True, timeout=120)
                if p.returncode == 0 and p.stdout.strip() not in ("1.0",):
                    durchgekommen.append((w, p.stdout.strip()))
            check(f"4 ohne {was} kommt ein unzulaessiger Wert durch - "
                  f"sie traegt also wirklich", bool(durchgekommen),
                  "nichts kam durch: eine ANDERE Wache verdeckt sie")
        finally:
            shutil.rmtree(ordner, ignore_errors=True)

    # Und die Gegenprobe am echten Modul: dieselben Werte muessen abprallen.
    ordner = tempfile.mkdtemp(prefix="tb42_gegen_")
    try:
        for w in (50.0, 0.0, -1.0, "1.5"):
            datei = schreibe_json(os.path.join(ordner, "f.json"),
                                  {"bots": {"t3_supertrend": w}})
            wert, _z, meldungen = gf.bestimme("t3_supertrend", datei)
            check(f"4 Gegenprobe: {w!r} prallt am echten Modul ab",
                  wert == 1.0 and len(meldungen) == 1, f"{wert} {meldungen}")
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


# ===========================================================================
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--nur", default="1,2,3,4")
    p.add_argument("--bots", default=",".join(BOTS))
    args = p.parse_args()
    gewaehlt = set(args.nur.split(","))

    print("=" * 78)
    print("Selbsttests shared/groessenfaktor.py und die neun Bots (TB-42, Teil 2)")
    print("=" * 78)
    if "1" in gewaehlt:
        print("\n1. Die Leseseite")
        test_lesen()
    if "2" in gewaehlt:
        print("2. Die Spalte in der Datenbank")
        test_spalte()
    if "3" in gewaehlt:
        print("3. Der Multiplikator am laufenden Bot (dauert)")
        test_lauf([b for b in args.bots.split(",") if b in LAUFBOTS])
    if "4" in gewaehlt:
        print("4. Mutationsproben an der Leseseite")
        test_mutationen()

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
