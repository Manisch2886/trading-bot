#!/usr/bin/env python3
"""
TB-46b - Was tun die neun Bots mit offenen Positionen, wenn Kursdaten fehlen?
==============================================================================
Diese Probe beantwortet EINE Frage am Verhalten, nicht am Quelltext:

    Gibt es bei irgendeinem der neun Bots einen Weg, auf dem FEHLENDE oder
    VERALTETE Kursdaten eine OFFENE Position SCHLIESSEN?

TB-45 hat berichtet, ein Bot ohne bestimmbare Entscheidungskerze habe am Ende
"Offene Papier-Positionen: 0". Diese Zahl wurde gemeldet, ohne zu fragen, wie
sie zustande kommt. Sie hat zwei voellig verschiedene Lesarten:

    (a) Der Bot eroeffnet keine NEUEN Positionen - harmlos.
    (b) Der Bot SCHLIESST offene, weil er sie ohne Kerze nicht bewerten kann -
        dann macht ein Parsing-Fehler einen Trade.

Der Unterschied ist an der Bildschirmausgabe nicht zu sehen. Er ist nur am
Zustand der Datenbank VORHER und NACHHER zu sehen. Genau das misst diese Probe.

Wie gemessen wird - und warum so
------------------------------------------------------------------------------
* **Ein Wegwerf-Verzeichnis je Bot**, ausserhalb des Arbeitsbaums. Es traegt
  eine Teilkopie des Projekts (shared/, config/, notifications/ und den einen
  Strategieordner). Weil `strategy_paths.get_strategy_paths()` die Datenbank
  aus dem Wurzelverzeichnis ableitet, zeigt damit ALLES - Datenbank, Kursordner,
  Protokolle - in die Kopie. Kein Bot sieht je eine echte `*.db`.
  ⚠️ Die neun echten `*.db` sind die einzige OOS-Evidenz des Projekts und nicht
  neu berechenbar. Diese Probe fasst sie nicht an; in der Cloud gibt es sie
  ohnehin nicht.
* **Ein eigener Prozess je Bot** (TB-40). Neun gleichnamige `indicators.py`,
  `equity_simulation.py` und `live_params.py` wuerden sich in `sys.modules`
  gegenseitig ueberschreiben. Die Bot-Dateien werden hier GELESEN und
  AUSGEFUEHRT, nie importiert.
* **Das Schema kommt aus dem Quelltext**, nicht aus dem Gedaechtnis: die
  `CREATE TABLE`-Anweisung wird per Syntaxbaum aus `init_db()` der jeweiligen
  `forward_test.py` gelesen und unveraendert ausgefuehrt.
* **Gemessen wird die Datenbank**, nicht die Ausgabe. Vor dem Lauf und nach dem
  Lauf, Zeile fuer Zeile.

Was die Probe am Bot aendert: NICHTS
------------------------------------------------------------------------------
`forward_test.py`, `live_params.py`, `indicators.py` und alles andere liegen in
der Kopie BYTEGLEICH wie im Repo - die Probe weist das je Lauf mit sha256 nach
(`bot_dateien_unveraendert` im JSON).

Ausgetauscht wird genau EINE Sache, und die ist nicht der Bot, sondern die
**Gegenstelle**: an `fetch_binance_data.py` bzw. `fetch_stock_data.py` wird ein
Block ANGEHAENGT, der `fetch_historical_data` neu belegt. Binance und yfinance
sind aus der Cloud gesperrt (403); ohne diesen Austausch waere jede Lage
dieselbe Lage - "Abruf gescheitert". Der angehaengte Block macht das
Verhalten der Gegenstelle zum EINSTELLBAREN Teil des Versuchs, und nur das.

Die fuenf Lagen
------------------------------------------------------------------------------
| A   | Kursdatei fehlt ganz; der Abruf scheitert                            |
| B   | Kursdatei vorhanden, aber LEERER Rahmen; der Abruf liefert einen
|     | leeren Rahmen  -> so, und nur so, kommt ein LEERER Kursrahmen beim
|     | Bot an                                                                |
| C1  | Kursdatei vorhanden, Rahmen VERALTET; der Abruf scheitert             |
| C2  | Kursdatei veraltet UND der Abruf liefert denselben veralteten Rahmen  |
| D   | Kontrolle: alles in Ordnung                                           |

⚠️ **C2 steht nicht im Auftrag und ist trotzdem noetig.** Der Auftrag fragt
ausdruecklich nach einem Pfad, "auf dem ein ALTER Kurs verwendet wird". Mit
Lage C1 allein ist diese Frage nicht zu beantworten: `entscheidungskerze.lade()`
VERWIRFT eine veraltete `data/`-Datei vollstaendig und ruft `abruf()`. Ein
veralteter Kursrahmen aus `data/` erreicht den Bot also nie. Erreichbar ist er
nur ueber die zweite Quelle - und genau die prueft `lade()` NICHT auf Frische
(Zeile 666-671: nach `df = abruf()` folgt `entferne_unvollstaendige` und
`nur_entscheidbar`, aber kein zweites `ist_frisch`). C2 misst diesen Weg.

⚠️ **Lage D ist nicht optional.** Ohne sie koennte jede andere Lage "Position
unveraendert" melden, weil der Bot gar nicht erst bis zur Positionspruefung
kommt. D traegt deshalb ZWEI offene Positionen:

    P1  ohne Stop, ohne Ziel   -> MUSS in jeder Lage offen bleiben
    P2  mit Stop, der auf den Kursen greift
        -> MUSS in D schliessen. Erst das beweist, dass der Bot die
           Positionspruefung ueberhaupt erreicht und schliessen KANN.

Beides zusammen: schliesst P2 in D und bleibt P1 in A/B/C1 offen, dann misst die
Probe wirklich den Ausstiegspfad und nicht die Frage, ob der Bot laeuft.

Aufruf
------------------------------------------------------------------------------
    python3 research/ausstiegspfade/probe.py
    python3 research/ausstiegspfade/probe.py --nur t3_supertrend
    python3 research/ausstiegspfade/probe.py --json ergebnisse/probe.json

Rueckgabewert 0, wenn gemessen wurde; **1, wenn nicht gemessen werden konnte**.
Ein leeres Ergebnis ist hier kein Erfolg - das ist die Lehre aus TB-45.
"""

import argparse
import ast
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import datetime as dt

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, os.path.join(_WURZEL, "shared"))

# Die neun Bots, mit dem, was die Probe von ihnen wissen muss. Markt und
# Intervall stehen als Literal in der jeweiligen forward_test.py; die Probe
# liest sie unten aus dem Quelltext nach und BRICHT AB, wenn sie abweichen -
# eine Tabelle, die still altert, ist in diesem Projekt schon einmal teuer
# gewesen.
BOTS = [
    # (Ordner,                     Markt,    Intervall, Symbol,   Kursquelle)
    ("elliott_wave",               "krypto", "1h",  "BTCUSDT", "binance"),
    ("t3_supertrend",              "krypto", "4h",  "BTCUSDT", "binance"),
    ("rsi2_crypto",                "krypto", "1d",  "BTCUSDT", "binance"),
    ("turtle_soup_crypto",         "krypto", "1d",  "BTCUSDT", "binance"),
    ("volatility_breakout_crypto", "krypto", "1d",  "BTCUSDT", "binance"),
    ("elliott_wave_stocks",        "aktien", "1d",  "AAPL",    "yfinance"),
    ("rsi2_mean_reversion",        "aktien", "1d",  "AAPL",    "yfinance"),
    ("turtle_soup_stocks",         "aktien", "1d",  "AAPL",    "yfinance"),
    ("volatility_breakout",        "aktien", "1d",  "AAPL",    "yfinance"),
]

LAGEN = ["A", "B", "C1", "C2", "D"]

LAGE_TEXT = {
    "A":  "Kursdatei fehlt ganz, Abruf scheitert",
    "B":  "Kursdatei vorhanden aber leer, Abruf liefert leeren Rahmen",
    "C1": "Kursdatei veraltet, Abruf scheitert",
    "C2": "Kursdatei veraltet, Abruf liefert denselben veralteten Rahmen",
    "D":  "Kontrolle - alles in Ordnung",
}

# Was aus dem Repo in die Kopie wandert. `data/` wird je Lage NEU gebaut und
# nie aus dem Repo uebernommen.
KOPIERT = ["shared", "config", "notifications"]

SPALTEN = ["open_time", "open", "high", "low", "close", "volume"]

# Der angehaengte Block, der die Gegenstelle einstellbar macht. Er ersetzt
# `fetch_historical_data` und sonst nichts.
GEGENSTELLE = '''

# ===========================================================================
# TB-46b, research/ausstiegspfade/probe.py - ANGEHAENGT VON DER PROBE
# ---------------------------------------------------------------------------
# Binance und yfinance sind aus der Cloud gesperrt (403). Ohne diesen Block
# waere jede Lage dieselbe Lage: "Abruf gescheitert". Er macht das Verhalten
# der GEGENSTELLE zum einstellbaren Teil des Versuchs - am Bot selbst aendert
# er nichts. Er steht nur in der Wegwerf-Kopie, nie im Repo.
# ===========================================================================
def fetch_historical_data(*_a, **_k):                        # noqa: F811
    import os as _os
    import pandas as _pd
    modus = _os.environ.get("PROBE_ABRUF", "scheitert")
    if modus == "leer":
        return _pd.DataFrame(columns=%(spalten)r)
    if modus == "rahmen":
        return _pd.read_csv(_os.environ["PROBE_ABRUF_CSV"],
                            parse_dates=["open_time"])
    raise ConnectionError(
        "TB-46b-Probe: die Kursquelle ist nicht erreichbar "
        "(HTTPSConnectionPool: 403 - so verhaelt sich die Cloud wirklich).")
''' % {"spalten": SPALTEN}


# ===========================================================================
# Teil 1 - Was der Quelltext sagt (gelesen, nicht geraten)
# ===========================================================================
def schema_aus_quelltext(pfad):
    """Die CREATE-TABLE-Anweisung aus `init_db()` - ueber den Syntaxbaum.

    Eine Textsuche wuerde hier genuegen und waere trotzdem falsch: sie
    faende auch ein CREATE TABLE in einem Kommentar oder in einer zweiten,
    laengst toten Funktion.
    """
    with open(pfad, "r", encoding="utf-8") as f:
        baum = ast.parse(f.read(), filename=pfad)
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.FunctionDef) and knoten.name == "init_db":
            for teil in ast.walk(knoten):
                if isinstance(teil, ast.Constant) and isinstance(teil.value, str) \
                        and "CREATE TABLE" in teil.value.upper():
                    return teil.value
    return None


def zuordnung_aus_quelltext(pfad):
    """(Intervall, Markt) so, wie sie in `forward_test.py` als Literal stehen.

    Gesucht sind `INTERVAL = ...` und der Marktname im `entscheidungskerze.lade`-
    Aufruf (`entscheidungskerze.KRYPTO` / `.AKTIEN`). Findet die Probe etwas
    anderes als in BOTS steht, bricht sie ab.
    """
    with open(pfad, "r", encoding="utf-8") as f:
        quelle = f.read()
    baum = ast.parse(quelle, filename=pfad)

    intervall = None
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign):
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Name) and ziel.id == "INTERVAL":
                    wert = knoten.value
                    if isinstance(wert, ast.Constant):
                        intervall = wert.value
                    elif isinstance(wert, ast.Attribute):
                        # Client.KLINE_INTERVAL_1HOUR usw.
                        intervall = {
                            "KLINE_INTERVAL_1HOUR": "1h",
                            "KLINE_INTERVAL_4HOUR": "4h",
                            "KLINE_INTERVAL_1DAY": "1d",
                        }.get(wert.attr)

    markt = None
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Attribute) and knoten.attr in ("KRYPTO", "AKTIEN"):
            markt = {"KRYPTO": "krypto", "AKTIEN": "aktien"}[knoten.attr]
    return intervall, markt


def sha256(pfad):
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for stueck in iter(lambda: f.read(65536), b""):
            h.update(stueck)
    return h.hexdigest()


# ===========================================================================
# Teil 2 - Die Wegwerf-Kopie
# ===========================================================================
def _ohne_beiwerk(_ordner, namen):
    return [n for n in namen
            if n == "__pycache__" or n.endswith(".pyc") or n.endswith(".db")]


def baue_kopie(bot, ziel):
    """Teilkopie des Projekts. Gibt die Liste der angefassten Dateien zurueck."""
    os.makedirs(ziel, exist_ok=True)
    for ordner in KOPIERT:
        quelle = os.path.join(_WURZEL, ordner)
        if os.path.isdir(quelle):
            shutil.copytree(quelle, os.path.join(ziel, ordner),
                            ignore=_ohne_beiwerk, dirs_exist_ok=True)
    os.makedirs(os.path.join(ziel, "strategies"), exist_ok=True)
    shutil.copytree(os.path.join(_WURZEL, "strategies", bot),
                    os.path.join(ziel, "strategies", bot),
                    ignore=_ohne_beiwerk, dirs_exist_ok=True)
    os.makedirs(os.path.join(ziel, "data"), exist_ok=True)

    angefasst = []
    for kandidat in (os.path.join(ziel, "shared", "fetch_binance_data.py"),
                     os.path.join(ziel, "strategies", bot, "fetch_stock_data.py")):
        if os.path.exists(kandidat):
            with open(kandidat, "a", encoding="utf-8") as f:
                f.write(GEGENSTELLE)
            angefasst.append(os.path.relpath(kandidat, ziel))
    return angefasst


def unveraendert(bot, ziel):
    """sha256-Vergleich der Bot-Dateien Repo <-> Kopie. Ohne die Gegenstelle."""
    ergebnis = {}
    for name in sorted(os.listdir(os.path.join(_WURZEL, "strategies", bot))):
        if not name.endswith(".py") or name == "fetch_stock_data.py":
            continue
        a = os.path.join(_WURZEL, "strategies", bot, name)
        b = os.path.join(ziel, "strategies", bot, name)
        ergebnis[name] = os.path.exists(b) and sha256(a) == sha256(b)
    for name in ("entscheidungskerze.py", "ladeprotokoll.py", "kursdaten.py",
                 "strategy_paths.py", "data_quality.py"):
        a = os.path.join(_WURZEL, "shared", name)
        b = os.path.join(ziel, "shared", name)
        if os.path.exists(a):
            ergebnis["shared/" + name] = os.path.exists(b) and sha256(a) == sha256(b)
    return ergebnis


# ===========================================================================
# Teil 3 - Die Kursreihe
# ===========================================================================
def erwartete_kerze(intervall, markt, startzeit=None):
    """Die `open_time`, die `entscheidungskerze.ist_frisch` erwartet - in ms.

    Bewusst ueber das Modul des Projekts selbst und nicht nachgerechnet:
    haette die Probe eine eigene Rechnung, pruefte Lage D die Probe und nicht
    den Bot.
    """
    import entscheidungskerze as ek
    ms, grund = ek.erwartete_letzte_oeffnung(intervall, markt, startzeit)
    if ms is None:
        raise RuntimeError(f"Die erwartete Entscheidungskerze ist nicht "
                           f"bestimmbar: {grund}")
    return ms


def _schritte(intervall, markt, bis_ms, anzahl, extra):
    """Die `open_time`-Folge: `anzahl` Kerzen bis `bis_ms`, dann `extra` weiter.

    Die `extra` Kerzen liegen NACH der Entscheidungskerze. Sie werden vom Bot
    verworfen (`nur_entscheidbar`) - sie stehen nur da, damit die Probe nicht
    daran scheitert, dass zwischen dem Bauen der Datei und dem Start des
    Kindprozesses eine Kerzengrenze faellt.
    """
    import pandas as pd
    bis = pd.Timestamp(bis_ms, unit="ms")
    if markt == "krypto":
        dauer = {"1h": "1h", "4h": "4h", "1d": "1D"}[intervall]
        zeiten = pd.date_range(end=bis, periods=anzahl, freq=dauer)
        weiter = pd.date_range(start=bis, periods=extra + 1, freq=dauer)[1:]
    else:
        zeiten = pd.bdate_range(end=bis, periods=anzahl)
        weiter = pd.bdate_range(start=bis, periods=extra + 1)[1:]
    return list(zeiten) + list(weiter)


def kursreihe(intervall, markt, bis_ms, anzahl=400, extra=3):
    """Eine fallende Reihe - und jede Eigenschaft hat ihren Grund.

    Fallend, weil das bei ALLEN NEUN Bots "kein Ausstieg" bedeutet:
    `close < SMA(5)` (kein sma_exit), `close < SMA(150/200)` und
    `close < bb_upper` (kein Einstieg), `t3_fast < t3_slow` durchgehend
    (kein Crossunder, kein Trendwechsel), und der Tagesrueckgang ist groesser
    als die Balkenspanne, also `close_t < low_{t-1}` (keine Turtle-Soup-
    Bestaetigung). So haengt das Ergebnis der Probe am Ausstiegspfad und
    nicht daran, dass die erfundene Reihe zufaellig ein Signal ergibt.
    """
    import pandas as pd
    zeiten = _schritte(intervall, markt, bis_ms, anzahl, extra)
    zeilen = []
    kurs = 200.0
    vorher = kurs
    for zeit in zeiten:
        zeilen.append({
            "open_time": zeit,
            "open": round(vorher, 6),
            "high": round(kurs * 1.0005, 6),
            "low": round(kurs * 0.9995, 6),
            "close": round(kurs, 6),
            "volume": 1000.0,
        })
        vorher = kurs
        kurs *= 0.997
    return pd.DataFrame(zeilen, columns=SPALTEN)


def veralte(df, markt, intervall, tage=7):
    """Dieselbe Reihe, nur `tage` Tage frueher zu Ende."""
    import pandas as pd
    alt = df.copy()
    alt["open_time"] = alt["open_time"] - pd.Timedelta(days=tage)
    # Die Kerzen, die durch das Verschieben ueber das Ende hinausragen
    # wuerden, gibt es dann eben nicht mehr - genau das heisst "veraltet".
    grenze = df["open_time"].max() - pd.Timedelta(days=tage)
    return alt[alt["open_time"] <= grenze].reset_index(drop=True)


# ===========================================================================
# Teil 4 - Die Datenbank
# ===========================================================================
def lege_db_an(pfad, schema, symbol, reihe, entscheidungs_ms):
    """Datenbank mit ZWEI offenen Positionen - P1 unerreichbar, P2 am Stop.

    Der Einstieg liegt auf der viertletzten ENTSCHEIDBAREN Kerze. Danach
    bleiben drei Kerzen, auf denen der Bot die Position bewerten kann - genug,
    damit P2 am Stop schliesst, und zu wenig fuer jeden Zeitausstieg (der
    kuerzeste im Projekt ist MAX_HOLD_DAYS = 10).

    ⚠️ Stop und Ziel stehen als ZAHL da, nicht als NULL. Ein NULL-Ziel waere
    keine bessere Probe, sondern eine andere: `elliott_wave/forward_test.py`
    Zeile 129 vergleicht `row["high"] >= trade["target_price"]` ohne
    None-Absicherung und bricht dann mit einem TypeError ab - dieser Bot
    schreibt aber immer beide Werte, also waere das ein Zustand, den er selbst
    nie erzeugt. Unerreichbar weit weg ist dasselbe "loest nicht aus" und
    bleibt im Rahmen dessen, was die Bots wirklich in die Datenbank schreiben.
    """
    import pandas as pd
    entscheidbar = reihe[reihe["open_time"] <= pd.Timestamp(entscheidungs_ms, unit="ms")]
    if len(entscheidbar) < 8:
        raise RuntimeError("Zu wenige entscheidbare Kerzen fuer die Probe.")
    einstieg = entscheidbar.iloc[-4]
    einstiegskurs = float(einstieg["close"])
    einstiegszeit = str(einstieg["open_time"])

    conn = sqlite3.connect(pfad)
    conn.execute(schema)
    spalten = {z[1] for z in conn.execute("PRAGMA table_info(trades)")}

    def _einfuegen(kennung, stop):
        felder = ["symbol", "signal_time", "entry_time", "entry_price",
                  "stop_price", "status"]
        werte = [symbol, einstiegszeit + kennung, einstiegszeit,
                 einstiegskurs, stop, "open"]
        if "target_price" in spalten:
            felder.insert(5, "target_price")
            werte.insert(5, einstiegskurs * 100)   # unerreichbar hoch
        conn.execute(f"INSERT INTO trades ({', '.join(felder)}) VALUES "
                     f"({', '.join('?' * len(felder))})", werte)

    # P1: Stop unerreichbar tief, Ziel unerreichbar hoch. Sie kann strukturell
    # nur am Zeitausstieg schliessen - und der ist hier ausser Reichweite.
    _einfuegen("#P1", einstiegskurs * 0.01)
    # P2: Stop genau auf dem Einstiegskurs. Die Reihe faellt, also liegt das
    # Tief der naechsten Kerze darunter - P2 MUSS schliessen, sobald der Bot
    # ueberhaupt Kurse sieht. Das ist die Gegenprobe zu P1.
    _einfuegen("#P2", einstiegskurs)
    conn.commit()
    conn.close()
    return {"einstiegszeit": einstiegszeit, "einstiegskurs": einstiegskurs,
            "P1_stop": einstiegskurs * 0.01, "P2_stop": einstiegskurs}


def zustand(pfad):
    """Der Zustand der Datenbank - Zeile fuer Zeile, plus sha256 der Datei."""
    conn = sqlite3.connect(f"file:{pfad}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    zeilen = [dict(r) for r in conn.execute(
        "SELECT id, symbol, signal_time, entry_time, entry_price, stop_price, "
        "exit_time, exit_price, result, pnl_pct, status FROM trades ORDER BY id")]
    conn.close()
    return {
        "zeilen": zeilen,
        "offen": sum(1 for z in zeilen if z["status"] == "open"),
        "geschlossen": sum(1 for z in zeilen if z["status"] == "closed"),
        "sha256": sha256(pfad),
    }


# ===========================================================================
# Teil 5 - Ein Lauf
# ===========================================================================
def lauf(bot, markt, intervall, symbol, ziel, lage, zeitgrenze=900):
    import pandas as pd

    datenordner = os.path.join(ziel, "data")
    for name in os.listdir(datenordner):
        os.remove(os.path.join(datenordner, name))
    csv_pfad = os.path.join(datenordner, f"{symbol}_{intervall}.csv")

    entscheidungs_ms = erwartete_kerze(intervall, markt)
    frisch = kursreihe(intervall, markt, entscheidungs_ms)
    alt = veralte(frisch, markt, intervall)

    umgebung = dict(os.environ)
    umgebung["PYTHONDONTWRITEBYTECODE"] = "1"
    rahmen_pfad = os.path.join(ziel, "abruf_rahmen.csv")

    if lage == "A":
        umgebung["PROBE_ABRUF"] = "scheitert"
        seed_reihe, seed_ms = frisch, entscheidungs_ms
    elif lage == "B":
        pd.DataFrame(columns=SPALTEN).to_csv(csv_pfad, index=False)
        umgebung["PROBE_ABRUF"] = "leer"
        seed_reihe, seed_ms = frisch, entscheidungs_ms
    elif lage == "C1":
        alt.to_csv(csv_pfad, index=False)
        umgebung["PROBE_ABRUF"] = "scheitert"
        seed_reihe, seed_ms = alt, int(alt["open_time"].max().value // 10**6)
    elif lage == "C2":
        alt.to_csv(csv_pfad, index=False)
        alt.to_csv(rahmen_pfad, index=False)
        umgebung["PROBE_ABRUF"] = "rahmen"
        umgebung["PROBE_ABRUF_CSV"] = rahmen_pfad
        seed_reihe, seed_ms = alt, int(alt["open_time"].max().value // 10**6)
    elif lage == "D":
        frisch.to_csv(csv_pfad, index=False)
        umgebung["PROBE_ABRUF"] = "scheitert"   # darf gar nicht gerufen werden
        seed_reihe, seed_ms = frisch, entscheidungs_ms
    else:
        raise ValueError(lage)

    db_pfad = os.path.join(ziel, f"paper_trading_{bot}.db")
    if os.path.exists(db_pfad):
        os.remove(db_pfad)
    schema = schema_aus_quelltext(
        os.path.join(_WURZEL, "strategies", bot, "forward_test.py"))
    if schema is None:
        raise RuntimeError(f"{bot}: CREATE TABLE in init_db() nicht gefunden.")
    saat = lege_db_an(db_pfad, schema, symbol, seed_reihe, seed_ms)

    vorher = zustand(db_pfad)
    begonnen = dt.datetime.utcnow()
    skript = os.path.join(ziel, "strategies", bot, "forward_test.py")
    try:
        fertig = subprocess.run([sys.executable, skript], cwd=ziel, env=umgebung,
                                capture_output=True, text=True,
                                timeout=zeitgrenze)
        rc, ausgabe, fehlerausgabe = fertig.returncode, fertig.stdout, fertig.stderr
        zeitgrenze_erreicht = False
    except subprocess.TimeoutExpired as abbruch:
        rc, zeitgrenze_erreicht = None, True
        ausgabe = (abbruch.stdout or b"").decode("utf-8", "replace") \
            if isinstance(abbruch.stdout, bytes) else (abbruch.stdout or "")
        fehlerausgabe = (abbruch.stderr or b"").decode("utf-8", "replace") \
            if isinstance(abbruch.stderr, bytes) else (abbruch.stderr or "")
    nachher = zustand(db_pfad)

    geschlossen = [
        {"signal_time": n["signal_time"], "result": n["result"],
         "exit_time": n["exit_time"], "exit_price": n["exit_price"],
         "pnl_pct": n["pnl_pct"]}
        for v, n in zip(vorher["zeilen"], nachher["zeilen"])
        if v["status"] == "open" and n["status"] == "closed"]

    for eintrag in geschlossen:
        eintrag["alter_des_ausstiegskurses_in_tagen"] = _alter(
            eintrag["exit_time"], begonnen)

    return {
        "lage": lage,
        "lage_text": LAGE_TEXT[lage],
        "einstieg": saat,
        "kursdatei": os.path.basename(csv_pfad) if os.path.exists(csv_pfad) else None,
        "kursdatei_zeilen": (0 if lage == "B"
                             else (len(alt) if lage in ("C1", "C2")
                                   else (len(frisch) if lage == "D" else None))),
        "rc": rc,
        "zeitgrenze_erreicht": zeitgrenze_erreicht,
        "offen_vorher": vorher["offen"],
        "offen_nachher": nachher["offen"],
        "geschlossen_vorher": vorher["geschlossen"],
        "geschlossen_nachher": nachher["geschlossen"],
        "db_sha256_vorher": vorher["sha256"],
        "db_sha256_nachher": nachher["sha256"],
        "db_unveraendert": vorher["sha256"] == nachher["sha256"],
        "in_diesem_lauf_geschlossen": geschlossen,
        "positionspruefung_erreicht": "Pruefe offene Positionen" in ausgabe,
        "zusammenfassung_erreicht": "FORWARD-TEST STATUS" in ausgabe,
        # Die Zeilen, die der Lauf ZU DIESEM Symbol geschrieben hat. Sie sagen,
        # AUF WELCHEM WEG das Symbol ausgelassen (oder benutzt) wurde - und
        # genau diese Unterscheidung ist die Frage von Teil 1.
        "zeilen_zum_symbol": [z for z in ausgabe.splitlines() if symbol in z],
        "ausgabe_letzte_zeilen": ausgabe.strip().splitlines()[-25:],
        "fehlerausgabe": fehlerausgabe.strip().splitlines()[-25:],
    }


def _alter(exit_time, begonnen):
    if not exit_time:
        return None
    for form in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            zeit = dt.datetime.strptime(str(exit_time)[:19], form)
        except ValueError:
            continue
        return round((begonnen - zeit).total_seconds() / 86400.0, 2)
    return None


# ===========================================================================
def einstufung(lagen):
    """sicher / unklar / handelnd - aus dem GEMESSENEN Verhalten."""
    nach_lage = {l["lage"]: l for l in lagen}
    d = nach_lage.get("D")
    if d is None or d["offen_nachher"] < 1 or d["geschlossen_nachher"] < 1:
        return "unklar", ("Die Kontrolle D hat nicht beides gezeigt "
                          "(P1 offen UND P2 geschlossen) - die Probe misst "
                          "hier nichts.")
    for name in ("A", "B", "C1"):
        lage = nach_lage.get(name)
        if lage is None:
            return "unklar", f"Lage {name} fehlt."
        if lage["geschlossen_nachher"] > lage["geschlossen_vorher"]:
            return "handelnd", (f"Lage {name} ({LAGE_TEXT[name]}) hat eine "
                                f"offene Position GESCHLOSSEN.")
        if not lage["db_unveraendert"]:
            return "unklar", (f"Lage {name}: die Datenbank hat sich geaendert, "
                              f"ohne dass eine Position geschlossen wurde.")
    c2 = nach_lage.get("C2")
    if c2 is not None and c2["geschlossen_nachher"] > c2["geschlossen_vorher"]:
        alter = [g.get("alter_des_ausstiegskurses_in_tagen")
                 for g in c2["in_diesem_lauf_geschlossen"]]
        return "sicher, aber mit altem Kurs handelnd", (
            f"Fehlende Kurse schliessen nichts (A/B/C1 unveraendert). Ein "
            f"VERALTETER Rahmen aus der zweiten Quelle wird jedoch ohne "
            f"Frischepruefung verwendet: Lage C2 hat geschlossen, "
            f"Ausstiegskurs {alter} Tage alt.")
    return "sicher", ("Fehlende oder veraltete Kurse lassen die offenen "
                      "Positionen unberuehrt; die Kontrolle D zeigt, dass der "
                      "Bot schliessen koennte.")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--nur", action="append", default=None,
                   help="nur diese(n) Bot messen (mehrfach erlaubt)")
    p.add_argument("--lage", action="append", default=None,
                   help=f"nur diese Lage(n): {', '.join(LAGEN)}")
    p.add_argument("--json", default=None, help="Ergebnis als JSON ablegen")
    p.add_argument("--arbeitswurzel", default=None,
                   help="Wurzel der Wegwerf-Verzeichnisse (Standard: Systemtemp)")
    p.add_argument("--behalten", action="store_true",
                   help="Wegwerf-Verzeichnisse nicht loeschen")
    p.add_argument("--zeitgrenze", type=int, default=900)
    args = p.parse_args(argv)

    bots = [b for b in BOTS if args.nur is None or b[0] in args.nur]
    lagen = [l for l in LAGEN if args.lage is None or l in args.lage]
    if not bots or not lagen:
        print("Nichts zu messen - kein Bot bzw. keine Lage ausgewaehlt.",
              file=sys.stderr)
        return 1

    ergebnis = {
        "werkzeug": "research/ausstiegspfade/probe.py",
        "gemessen_am": dt.datetime.utcnow().isoformat() + "Z",
        "python": sys.version.split()[0],
        "lagen": LAGE_TEXT,
        "bots": {},
    }

    for bot, markt, intervall, symbol, quelle in bots:
        print(f"=== {bot} ({markt}, {intervall}, {symbol}) ===", flush=True)
        ft = os.path.join(_WURZEL, "strategies", bot, "forward_test.py")
        gelesen_intervall, gelesen_markt = zuordnung_aus_quelltext(ft)
        if (gelesen_intervall, gelesen_markt) != (intervall, markt):
            print(f"  ABBRUCH: forward_test.py sagt "
                  f"({gelesen_intervall!r}, {gelesen_markt!r}), die Probe "
                  f"rechnet mit ({intervall!r}, {markt!r}).", file=sys.stderr)
            return 1

        ziel = tempfile.mkdtemp(prefix=f"tb46b_{bot}_", dir=args.arbeitswurzel)
        try:
            angefasst = baue_kopie(bot, ziel)
            eintrag = {
                "markt": markt, "intervall": intervall, "symbol": symbol,
                "kursquelle": quelle,
                "wegwerf_verzeichnis": ziel,
                "gegenstelle_ersetzt_in": angefasst,
                "bot_dateien_unveraendert": unveraendert(bot, ziel),
                "laeufe": [],
            }
            for lage in lagen:
                print(f"  Lage {lage}: {LAGE_TEXT[lage]}", flush=True)
                eintrag["laeufe"].append(
                    lauf(bot, markt, intervall, symbol, ziel, lage,
                         args.zeitgrenze))
                letzter = eintrag["laeufe"][-1]
                print(f"    offen {letzter['offen_vorher']} -> "
                      f"{letzter['offen_nachher']}, geschlossen "
                      f"{letzter['geschlossen_vorher']} -> "
                      f"{letzter['geschlossen_nachher']}, rc={letzter['rc']}",
                      flush=True)
            eintrag["einstufung"], eintrag["begruendung"] = einstufung(eintrag["laeufe"])
            print(f"  => {eintrag['einstufung']}: {eintrag['begruendung']}",
                  flush=True)
            ergebnis["bots"][bot] = eintrag
        finally:
            if not args.behalten:
                shutil.rmtree(ziel, ignore_errors=True)

    if args.json:
        pfad = args.json if os.path.isabs(args.json) else os.path.join(_HIER, args.json)
        os.makedirs(os.path.dirname(pfad), exist_ok=True)
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump(ergebnis, f, indent=2, ensure_ascii=False)
        print(f"\nJSON: {pfad}")

    if not ergebnis["bots"]:
        print("Nichts gemessen.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
