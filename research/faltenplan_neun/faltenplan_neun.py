#!/usr/bin/env python3
"""
Faltenplan fuer alle NEUN Bots - Verfahren B (TB-36)
==============================================================================
Rein lesend. Fasst keinen Bot-Code, keine Parametrisierung und keine Kursdatei
an; Bot-Dateien werden **gelesen, nie importiert** (neun gleichnamige
`equity_simulation.py` kollidieren in `sys.modules`). Reine Standardbibliothek
- kein pandas, kein numpy: dasselbe Werkzeug laeuft in der Cloud und auf dem
Rechner des Nutzers.

WARUM ES DIESES WERKZEUG GIBT
------------------------------------------------------------------------------
Registertext 4d verlangt die Faltenliste **je Bot**, Registertext 3b die
**Symbolzahl je Falte**. Beides gibt es heute fuer die vier Aktien-Bots
nirgends:

* `research/krypto_historie/faltenplan.py` (TB-31) rechnet Falten UND Symbole
  je Falte, aber nur fuer die fuenf Krypto-Bots und nach Verfahren A
  (Argument `--mindesttraining`, point-in-time-Ausschluss).
* `research/vorregistrierung/faltenplan.py` (TB-30a) deckt alle neun Bots ab,
  kennt aber keine Symbolzahl je Falte, traegt Trainingsfenster, Purge und
  Embargo ZWISCHEN den Falten - alles Verfahren A - und fuehrt Krypto als
  Platzhalter.

WARUM EIN DRITTES WERKZEUG UND KEINE ERWEITERUNG - DIE ENTSCHEIDUNG
------------------------------------------------------------------------------
Die Aufgabe stellt die Frage ausdruecklich: erweitern oder neu? Entschieden
ist: **neu, und die beiden alten bleiben unangetastet.** Drei Gruende, und der
dritte ist der, der den Ausschlag gibt:

1. Beide vorhandenen Werkzeuge sind **Belege abgeschlossener Untersuchungen**
   (`research/krypto_historie/BERICHT.md`, `research/vorregistrierung/`). Wer
   sie umschreibt, aendert rueckwirkend, womit damals gerechnet wurde. Der
   Faltenplan aus TB-31 ist genau die Zahlenreihe, an der dieses Werkzeug
   gemessen wird - er muss stehen bleiben, sonst misst die Gegenprobe sich
   selbst.
2. Beide sprechen **Verfahren A**: `--mindesttraining`, Trainingsfenster,
   Purge/Embargo zwischen Falten. Unter Verfahren B gibt es davon nichts mehr.
   Eine Erweiterung haette beide Sprachen gleichzeitig tragen muessen.
3. Die Faltenlogik soll **genau einmal** existieren - das ist der Einwand
   gegen ein drittes Werkzeug, und er ist berechtigt. Er wird hier nicht durch
   ein Versprechen eingeloest, sondern durch eine **Messung**:
   `test_faltenplan_neun.py` rechnet die fuenf Krypto-Bots mit BEIDEN
   Werkzeugen und vergleicht Falte fuer Falte und Symbol fuer Symbol. Laufen
   sie auseinander, faellt der Test. Nach TB-30b, wenn die sechs bot-eigenen
   Walk-Forward-Rechner ersetzt sind, bleibt dieses Werkzeug uebrig und die
   beiden alten sind Archiv.

DIE REGELN (Verfahren B, Registernachtrag TB-36)
------------------------------------------------------------------------------
* **Kein Mindesttraining.** Eine Falte beginnt, sobald Universum und
  Indikator-Vorlauf vorliegen. Es gibt kein Trainingsfenster; die
  Selektionsfalten sind keine OOS-Falten und brauchen untereinander keine
  Purge.
* **Falten sind Kalenderjahre**, bzw. Doppeljahre fuer die Bots, die nach der
  bestehenden Registerregel Doppeljahre bekommen. Diese Regel wird hier
  **nachgerechnet, nicht abgeschrieben**: Abschnitt 5.1 Nr. 6 des Registers
  ("ein Jahr, zwei Jahre bei unter 30 gefundenen Trades je Jahr", Festlegung
  7) auf den gefundenen Trades aus `research/tb24_haltedauern/`, angeschnittene
  Randjahre ausgenommen (Abschnitt 5.4).
* **Frueheste Falte 2019** (`ERSTE_MOEGLICHE_FALTE` im Register). Diese
  Schranke ist Teil des Registers und wird hier nicht neu erfunden; ohne sie
  laege die erste Falte bei Krypto auf 2018.
* **Bis zum letzten vollstaendigen Jahr vor Go-Live.** Go-Live-Schnitt
  `2026-09-01`, ausschliesslich - wie im vorhandenen Werkzeug. Die letzte,
  angeschnittene Falte ist die Bestaetigungsperiode (Registerregel 5.1 Nr. 7).
* **Aktien:** Universum ist die heutige Symbolliste des Bots, Zeitfenster
  `RECENT_YEARS_ONLY = 10` - gemessen vom letzten Kurstag der Daten.
* **Symbole ohne Historie in einer Falte** tragen 0 Trades und 0 Rendite bei;
  sie werden **nicht** ausgeschlossen. Die "Symbolzahl je Falte" ist deshalb
  eine Berichtszahl - wie viele Symbole in dieser Falte ueberhaupt Evidenz
  liefern koennen -, keine Auswahl.

ZWEI LESARTEN DER SYMBOLZAHL - UND WELCHE EINGETRAGEN WIRD
------------------------------------------------------------------------------
Registertext 3a sagt: Symbole, "fuer die am 1. Januar der Falte Kursdaten
**einschliesslich Indikator-Vorlauf** vorliegen". Das laesst zwei Lesarten zu,
und sie ergeben verschiedene Zahlen:

  **A (eingetragen)** Kursdaten liegen am 1. Januar vor. Der Indikator-Vorlauf
      wird aus der eigenen Historie des Symbols gespeist und laeuft, wo er noch
      nicht voll ist, in die Falte hinein: das Symbol handelt dort ein paar
      Tage spaeter, traegt also fuer diese Tage 0 bei - genau die Behandlung,
      die der naechste Satz des Registertexts vorschreibt.
  **B (nachrichtlich)** Kursdaten UND voller Indikator-Vorlauf liegen am 1.
      Januar vor. Ein Symbol, dessen Vorlauf noch laeuft, zaehlt nicht mit.

Lesart A gilt, aus zwei Gruenden, die beide im Register stehen und nicht in
diesem Werkzeug: Registertext 3b nennt **eine** Zahlenreihe fuer **alle**
Krypto-Tagesbots - haenge die Zahl am Vorlauf, haette jeder Bot seine eigene
(`rsi2_crypto` 150 Balken, `turtle_soup_crypto` 30, `volatility_breakout_crypto`
127). Und die Gegenprobe aus TB-31 ist "nicht verhandelbar": 6/9/13/13/13/17/18,
Bestaetigung 23 - das sind die Zahlen der Lesart A.

Lesart B wird trotzdem gerechnet und ausgewiesen, je Bot. Sie ist der Preis der
Lesart A, und er gehoert sichtbar neben die Zahl, nicht in eine Fussnote.

    python3 research/faltenplan_neun/faltenplan_neun.py
    python3 research/faltenplan_neun/faltenplan_neun.py --json bericht.json
"""

import argparse
import csv
import datetime as dt
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HIER))
# ⚠️ TB36_BASE_DIR ist eine ERSATZWURZEL - ein Messwerkzeug fuer Tests und
# Mutationsproben (Wegwerf-Universum mit eigenem `data/` und `config/`), KEIN
# Modus-Lauf und kein Weg zum Snapshot (Fable 24d Abschnitt 3, TB-104). Unter
# dem Selektionsmodus bricht jede Nutzung einer Ersatzwurzel mit 2 ab
# (`_ersatzwurzel` unten); ohne Ersatzwurzel kommen Kurs- und Universumspfade
# ueber den Resolver.
ERSATZWURZEL = os.environ.get("TB36_BASE_DIR") or None
BASE_DIR = ERSATZWURZEL or _REPO

# --- Pfade der Kurs- und Universumsdateien: der Resolver (TB-104) -----------
# Fable 24c Abschnitt 2 / 25a (C): Jedes Modul des Laufbereichs, das Kurs- oder
# Universumsdateien liest, bezieht seine Pfade ueber `shared/paths.py` -
# direkt, nicht ueber `strategy_paths.get_strategy_paths()` (legt
# `results/<name>/` und `logs/<name>/` an, TB-103 Abschnitt 5 (5)). Ohne Modus
# sind das `data/` und `config/` der Repo-Wurzel wie vorher, unter dem Modus
# der Snapshot (Kurse flach, Universum unter `config/`). Bis TB-104 baute diese
# Datei beide Pfade selbst aus `BASE_DIR` und kannte den Modus nicht. Die
# Standardbibliothek genuegt weiter: `paths.py` importiert nichts anderes.
sys.path.insert(0, os.path.join(_REPO, "shared"))
import paths  # noqa: E402

RUECKGABEWERT_ERSATZWURZEL_IM_MODUS = paths.RUECKGABEWERT_STARTPRUEFUNG

# ==============================================================================
# Festlegungen aus dem Register - nicht hier erfunden
# ==============================================================================
# docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 5.2 bzw.
# research/vorregistrierung/registerdaten.py::GO_LIVE_SCHNITT
GO_LIVE = dt.date(2026, 9, 1)             # ausschliesslich
# registerdaten.py::ERSTE_MOEGLICHE_FALTE
FRUEHESTE_FALTE = 2019
# registerdaten.py::ZWEIJAHRES_SCHWELLE_TRADES (Festlegung 7)
ZWEIJAHRES_SCHWELLE_TRADES = 30

# strategies/*/multi_symbol_optimise.py::RECENT_YEARS_ONLY (alle vier
# Aktien-Bots: 10). Krypto kennt kein solches Fenster.
RECENT_YEARS_ONLY = {"aktien": 10, "krypto": None}

# shared/symbols_config.py::EXCLUDE_SYMBOLS
KRYPTO_AUSSCHLUSS = {"XAUTUSDT", "PAXGUSDT"}

UNIVERSUM = {
    # registerdaten.py::UNIVERSUM; identisch zu shared/symbols_config.py bzw.
    # strategies/<aktien-bot>/stocks_symbols_config.py (alle vier Aktien-Bots
    # lesen dieselbe Datei).
    "krypto": os.path.join("config", "top25_symbols.txt"),
    "aktien": os.path.join("config", "sp500_top150.txt"),
}

# ==============================================================================
# Die neun Bots
# ==============================================================================
# `vorlauf_balken`: der Indikator-Vorlauf in BALKEN des jeweiligen Zeitrahmens,
# so wie er im Backtest des Bots steht - GELESEN, nicht geschaetzt. Die Quelle
# steht je Bot daneben; `vorlauf_quelle` wird mit ausgegeben, damit jede Zahl
# nachschlagbar bleibt.
#
# Zwei Bots haben keinen festen Vorlauf, und das ist kein Versehen:
# die Elliott-Wave-Bots arbeiten auf einem Zigzag, der kein Fenster hat - ihr
# erstes Signal haengt an den gefundenen Pivots, nicht an einer Balkenzahl.
# `t3_supertrend` rechnet mit `ewm()` ohne Mindestfenster; seine Schleife
# beginnt bei Balken 1.
BOTS = {
    "elliott_wave": {
        "markt": "krypto", "zeitrahmen": "1h", "vorlauf_balken": 0,
        "vorlauf_quelle": "strategies/elliott_wave/backtest_elliott.py - "
                          "Zigzag ohne Fenster, kein start_i",
    },
    "t3_supertrend": {
        "markt": "krypto", "zeitrahmen": "4h", "vorlauf_balken": 1,
        "vorlauf_quelle": "strategies/t3_supertrend/backtest_trend.py:97 "
                          "'for i in range(1, len(data))'; ewm() ohne "
                          "Mindestfenster",
    },
    "rsi2_crypto": {
        "markt": "krypto", "zeitrahmen": "1d", "vorlauf_balken": 150,
        "vorlauf_quelle": "strategies/rsi2_crypto/backtest_rsi2.py:81 "
                          "'start_i = sma_trend_period'; live_params.py "
                          "SMA_TREND_FILTER = 150",
    },
    "turtle_soup_crypto": {
        "markt": "krypto", "zeitrahmen": "1d", "vorlauf_balken": 30,
        "vorlauf_quelle": "strategies/turtle_soup_crypto/"
                          "backtest_turtle_soup.py:119 'start_i = "
                          "WARMUP_PERIOD + donchian_period' = 20 + 10",
    },
    "volatility_breakout_crypto": {
        "markt": "krypto", "zeitrahmen": "1d", "vorlauf_balken": 127,
        "vorlauf_quelle": "strategies/volatility_breakout_crypto/"
                          "backtest_breakout.py:109 'start_i = WARMUP_PERIOD "
                          "+ 1' = max(20, 126, 20) + 1",
    },
    "elliott_wave_stocks": {
        "markt": "aktien", "zeitrahmen": "1d", "vorlauf_balken": 0,
        "vorlauf_quelle": "strategies/elliott_wave_stocks/"
                          "backtest_elliott.py - Zigzag ohne Fenster, kein "
                          "start_i",
    },
    "rsi2_mean_reversion": {
        "markt": "aktien", "zeitrahmen": "1d", "vorlauf_balken": 200,
        "vorlauf_quelle": "strategies/rsi2_mean_reversion/backtest_rsi2.py:117 "
                          "'start_i = SMA_TREND_PERIOD' = 200",
    },
    "turtle_soup_stocks": {
        "markt": "aktien", "zeitrahmen": "1d", "vorlauf_balken": 30,
        "vorlauf_quelle": "strategies/turtle_soup_stocks/"
                          "backtest_turtle_soup.py:115 'start_i = "
                          "WARMUP_PERIOD + donchian_period' = 20 + 10",
    },
    "volatility_breakout": {
        "markt": "aktien", "zeitrahmen": "1d", "vorlauf_balken": 127,
        "vorlauf_quelle": "strategies/volatility_breakout/"
                          "backtest_breakout.py:150 'start_i = WARMUP_PERIOD "
                          "+ 1' = max(20, 126, 20) + 1",
    },
}

TB24_DATEN = os.path.join("research", "tb24_haltedauern", "daten")


# ==============================================================================
# 1. Universum und Kursdaten - gelesen, nicht angenommen
# ==============================================================================
def _ersatzwurzel(basis: str = None):
    """Die Ersatzwurzel (Argument `basis` oder TB36_BASE_DIR) - oder None.

    Unter dem Selektionsmodus ist eine Ersatzwurzel ein Widerspruch: sie waere
    ein Weg an den Snapshot vorbei. Dann Abbruch mit 2 (36.5), vor jedem
    Lesen - nicht still ignoriert und nicht still benutzt.
    """
    wurzel = basis or ERSATZWURZEL
    if wurzel is not None and paths.selektionsmodus() is not None:
        sys.stderr.write(
            "[faltenplan_neun] ABBRUCH: Ersatzwurzel %s unter dem "
            "Selektionsmodus (%s). Eine Ersatzwurzel ist ein Messwerkzeug, "
            "kein Modus-Lauf (Fable 24d Abschnitt 3); Kurs- und "
            "Universumsdateien kommen im Modus nur ueber shared/paths.py.\n"
            % (wurzel, paths.selektionsmodus()[0]))
        raise SystemExit(RUECKGABEWERT_ERSATZWURZEL_IM_MODUS)
    return wurzel


def universumsdatei(markt: str, basis: str = None) -> str:
    """Pfad der Universumsdatei: ueber den Resolver, bei Ersatzwurzel dort."""
    wurzel = _ersatzwurzel(basis)
    if wurzel is None:
        return os.path.join(paths.CONFIG_DIR, os.path.basename(UNIVERSUM[markt]))
    return os.path.join(wurzel, UNIVERSUM[markt])


def symbole(markt: str, basis: str = None) -> list:
    """Die heutige Symbolliste des Marktes, in Dateireihenfolge."""
    pfad = universumsdatei(markt, basis)
    with open(pfad, "r", encoding="utf-8") as datei:
        liste = [zeile.strip() for zeile in datei if zeile.strip()]
    if markt == "krypto":
        liste = [s for s in liste if s not in KRYPTO_AUSSCHLUSS]
    return liste


def kursdatei(symbol: str, zeitrahmen: str, basis: str = None) -> str:
    """Pfad der Kursdatei: ueber den Resolver, bei Ersatzwurzel dort."""
    wurzel = _ersatzwurzel(basis)
    ordner = paths.DATA_DIR if wurzel is None else os.path.join(wurzel, "data")
    return os.path.join(ordner, f"{symbol}_{zeitrahmen}.csv")


def _zeitstempel(zeile: str):
    """Das Datum der ersten Spalte einer Kursdatei-Zeile, oder None."""
    zeile = zeile.strip()
    if not zeile:
        return None
    return dt.date.fromisoformat(zeile.split(",")[0][:10])


def erster_und_letzter_tag(pfad: str):
    """(erster, letzter) Kurstag einer Datei - ohne sie ganz einzulesen."""
    erster = letzter = None
    with open(pfad, "r", encoding="utf-8") as datei:
        datei.readline()                       # Kopfzeile
        for zeile in datei:
            tag = _zeitstempel(zeile)
            if tag is None:
                continue
            if erster is None:
                erster = tag
            letzter = tag
    return erster, letzter


def balken_datum(pfad: str, nummer: int, anker=None):
    """Das Datum des `nummer`-ten Balkens (0-basiert) ab `anker`.

    Streamt und bricht ab, sobald der Balken erreicht ist - die
    Stundendateien haben rund 78.000 Zeilen, und gebraucht wird meist die
    erste. Gibt None, wenn die Datei so weit nicht reicht.
    """
    gezaehlt = 0
    with open(pfad, "r", encoding="utf-8") as datei:
        datei.readline()
        for zeile in datei:
            tag = _zeitstempel(zeile)
            if tag is None or (anker is not None and tag < anker):
                continue
            if gezaehlt == nummer:
                return tag
            gezaehlt += 1
    return None


def fensteranker(markt: str, basis: str = None):
    """Der Beginn des Auswertungsfensters, gemessen statt angenommen.

    Aktien: `RECENT_YEARS_ONLY = 10` Jahre vor dem letzten Kurstag - so
    rechnen die vier Aktien-Bots selbst (`entry_cutoff = df['open_time'].max()
    - pd.DateOffset(years=RECENT_YEARS_ONLY)`). Genommen wird der SPAETESTE
    letzte Kurstag des Marktes, damit alle Symbole desselben Bots auf
    demselben Fenster liegen. Krypto: kein Fenster.
    """
    jahre = RECENT_YEARS_ONLY[markt]
    if jahre is None:
        return None
    letzte = []
    for symbol in symbole(markt, basis):
        pfad = kursdatei(symbol, "1d", basis)
        if os.path.exists(pfad):
            _, letzter = erster_und_letzter_tag(pfad)
            if letzter is not None:
                letzte.append(letzter)
    if not letzte:
        return None
    ende = max(letzte)
    try:
        return ende.replace(year=ende.year - jahre)
    except ValueError:                                    # 29.02.
        return ende.replace(year=ende.year - jahre, day=28)


# ==============================================================================
# 2. Faltenlaenge - die bestehende Registerregel, nachgerechnet
# ==============================================================================
def gefundene_trades_je_jahr(bot: str, basis: str = None) -> dict:
    """Gefundene (nicht ausgefuehrte) Trades je Kalenderjahr aus TB-24."""
    pfad = os.path.join(basis or BASE_DIR, TB24_DATEN, f"{bot}_alle_trades.csv")
    zaehlung = {}
    with open(pfad, "r", encoding="utf-8") as datei:
        for zeile in csv.DictReader(datei):
            jahr = int(zeile["entry_time"][:4])
            zaehlung[jahr] = zaehlung.get(jahr, 0) + 1
    return dict(sorted(zaehlung.items()))


def _abbruch_2(stelle: str, text: str):
    """Laut abbrechen statt still einen Ersatzwert zu nehmen (TB-107, Bauart
    TB-106 B1 in `research/vorregistrierung/faltenplan.py`). Unabhaengig vom
    Modus."""
    print(f"ABBRUCH (faltenplan_neun.py::{stelle}): {text}", file=sys.stderr)
    raise SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)


def volle_jahre(zaehlung: dict) -> dict:
    """Ohne die angeschnittenen Randjahre (Register, Abschnitt 5.4).

    Sie zoegen die Trades je Jahr nach unten und schoeben einen Bot faelschlich
    in die Doppeljahre.
    """
    if not zaehlung:
        return {}
    jahre = sorted(zaehlung)
    innen = {j: zaehlung[j] for j in jahre[1:-1]}
    if not innen:
        _abbruch_2("volle_jahre",
                   f"kein volles Kalenderjahr unter {jahre} - bis TB-107 stand "
                   f"hier still das erste, angeschnittene Jahr als Ersatz")
    return innen


def faltenlaenge(bot: str, basis: str = None) -> tuple:
    """(Laenge in Jahren, Trades je Jahr) nach Registerregel 5.1 Nr. 6."""
    zaehlung = volle_jahre(gefundene_trades_je_jahr(bot, basis))
    if not zaehlung:
        _abbruch_2("faltenlaenge",
                   f"{bot}: keine gefundenen Trades in der TB-24-Zaehlung - bis "
                   f"TB-107 stand hier still die Faltenlaenge 2 mit 0.0 Trades je Jahr")
    mittel = sum(zaehlung.values()) / len(zaehlung)
    return (2 if mittel < ZWEIJAHRES_SCHWELLE_TRADES else 1), mittel


# ==============================================================================
# 3. Der Faltenplan
# ==============================================================================
def warm_ab(bot: str, symbol: str, anker, basis: str = None):
    """Ab wann das Symbol fuer diesen Bot handelbar ist (Lesart B).

    Das Datum des Balkens, ab dem der Indikator-Vorlauf des Bots voll ist.
    Bei Vorlauf 0 ist das der erste Kurstag - Lesart A.
    """
    eig = BOTS[bot]
    pfad = kursdatei(symbol, eig["zeitrahmen"], basis)
    if not os.path.exists(pfad):
        return None
    return balken_datum(pfad, eig["vorlauf_balken"], anker)


def symbolbeginn(bot: str, anker, basis: str = None) -> dict:
    """{Symbol -> (erster Kurstag, warm ab)} fuer beide Lesarten."""
    eig = BOTS[bot]
    ergebnis = {}
    for symbol in symbole(eig["markt"], basis):
        pfad = kursdatei(symbol, eig["zeitrahmen"], basis)
        if not os.path.exists(pfad):
            ergebnis[symbol] = (None, None)
            continue
        erster = balken_datum(pfad, 0, anker)
        warm = (erster if eig["vorlauf_balken"] == 0
                else warm_ab(bot, symbol, anker, basis))
        ergebnis[symbol] = (erster, warm)
    return ergebnis


def erstes_faltenjahr(beginn: dict) -> int:
    """Das erste Kalenderjahr, in dem Universum UND Indikator-Vorlauf vorliegen.

    Vorliegen heisst: mindestens ein Symbol des Universums ist am 1. Januar
    handelbar. Untergrenze ist die Registerschranke FRUEHESTE_FALTE; welche
    der beiden bindet, weist `plan_fuer_bot` getrennt aus.
    """
    warme = [w for _, w in beginn.values() if w is not None]
    if not warme:
        return None
    frueheste = min(warme)
    jahr = max(FRUEHESTE_FALTE, frueheste.year + (0 if frueheste == dt.date(
        frueheste.year, 1, 1) else 1))
    return jahr if jahr <= GO_LIVE.year else None


def _ungebremstes_faltenjahr(beginn: dict):
    """Dasselbe ohne die Registerschranke - nur zum Ausweisen."""
    warme = [w for _, w in beginn.values() if w is not None]
    if not warme:
        return None
    frueheste = min(warme)
    return frueheste.year + (0 if frueheste == dt.date(frueheste.year, 1, 1)
                             else 1)


def falten(erstes_jahr: int, laenge: int) -> list:
    """Lueckenlose Falten der Laenge `laenge` bis zum Go-Live-Schnitt.

    Die letzte ist die Bestaetigungsperiode (Registerregel 5.1 Nr. 7); sie
    darf angeschnitten sein und waechst jeden Monat.
    """
    if erstes_jahr is None:
        return []
    bloecke, jahr = [], erstes_jahr
    while jahr <= GO_LIVE.year:
        ende = min(dt.date(jahr + laenge, 1, 1), GO_LIVE)
        bloecke.append({
            "von": dt.date(jahr, 1, 1),
            "bis_ausschliesslich": ende,
            "jahre": list(range(jahr, min(jahr + laenge, GO_LIVE.year + 1))),
            "angeschnitten": dt.date(jahr + laenge, 1, 1) > GO_LIVE,
        })
        jahr += laenge
    return bloecke


def plan_fuer_bot(bot: str, basis: str = None) -> dict:
    eig = BOTS[bot]
    anker = fensteranker(eig["markt"], basis)
    beginn = symbolbeginn(bot, anker, basis)
    laenge, trades = faltenlaenge(bot, basis)
    erstes = erstes_faltenjahr(beginn)
    bloecke = falten(erstes, laenge)

    for block in bloecke:
        grenze = block["von"]
        block["symbole_a"] = sorted(s for s, (e, _) in beginn.items()
                                    if e is not None and e <= grenze)
        block["symbole_b"] = sorted(s for s, (_, w) in beginn.items()
                                    if w is not None and w <= grenze)
        # Kein Symbol verlaesst das Universum: was in dieser Falte keine
        # Historie hat, steht hier - und traegt dort 0 Trades und 0 Rendite
        # bei, statt ausgeschlossen zu werden. Die Summe aus beiden Listen
        # ist in jeder Falte die volle Symbolliste; `test_faltenplan_neun.py`
        # Teil C prueft das am Ablauf.
        block["symbole_ohne_historie"] = sorted(set(beginn) - set(block["symbole_a"]))

    selektion = bloecke[:-1] if bloecke else []
    bestaetigung = bloecke[-1] if bloecke else None
    in_selektion = {s for b in selektion for s in b["symbole_a"]}
    ohne_datei = sorted(s for s, (e, _) in beginn.items() if e is None)

    return {
        "bot": bot,
        "markt": eig["markt"],
        "zeitrahmen": eig["zeitrahmen"],
        "vorlauf_balken": eig["vorlauf_balken"],
        "vorlauf_quelle": eig["vorlauf_quelle"],
        "fensteranker": anker.isoformat() if anker else None,
        "recent_years_only": RECENT_YEARS_ONLY[eig["markt"]],
        "faltenlaenge_jahre": laenge,
        "gefundene_trades_je_jahr": round(trades, 1),
        "symbole_gesamt": len(beginn),
        "ohne_kursdatei": ohne_datei,
        "erstes_faltenjahr": erstes,
        "erstes_faltenjahr_ohne_schranke": _ungebremstes_faltenjahr(beginn),
        "schranke_bindet": (erstes is not None
                            and _ungebremstes_faltenjahr(beginn) is not None
                            and _ungebremstes_faltenjahr(beginn)
                            < FRUEHESTE_FALTE),
        "selektionsfalten": selektion,
        "bestaetigungsperiode": bestaetigung,
        "anzahl_selektionsfalten": len(selektion),
        "symbolzahl_je_selektionsfalte": [len(b["symbole_a"])
                                          for b in selektion],
        "symbolzahl_je_selektionsfalte_lesart_b": [len(b["symbole_b"])
                                                   for b in selektion],
        "symbolzahl_bestaetigung": (len(bestaetigung["symbole_a"])
                                    if bestaetigung else 0),
        "symbolzahl_bestaetigung_lesart_b": (len(bestaetigung["symbole_b"])
                                             if bestaetigung else 0),
        "nie_in_einer_selektionsfalte": sorted(
            s for s, (e, _) in beginn.items() if s not in in_selektion),
        "symbolbeginn": {s: (e.isoformat() if e else None)
                         for s, (e, _) in sorted(beginn.items())},
    }


def faltenplan(basis: str = None) -> dict:
    return {bot: plan_fuer_bot(bot, basis) for bot in BOTS}


# ==============================================================================
# 4. Ausgabe
# ==============================================================================
def faltenname(block: dict) -> str:
    jahre = block["jahre"]
    name = str(jahre[0]) if len(jahre) == 1 else f"{jahre[0]}-{jahre[-1]}"
    return name + (" (bis Go-Live)" if block["angeschnitten"] else "")


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Faltenplan fuer alle neun Bots nach Verfahren B. "
                    "Kurs- und Universumsdateien ueber shared/paths.py (unter "
                    "dem Selektionsmodus aus dem Snapshot). TB36_BASE_DIR ist "
                    "eine Ersatzwurzel fuer Tests - ein Messwerkzeug, kein "
                    "Modus-Lauf; unter dem Modus bricht sie mit 2 ab (TB-104).")
    zerleger.add_argument("--json", default=None,
                          help="Bericht als JSON zusaetzlich hierhin schreiben")
    argumente = zerleger.parse_args(argv)

    print("=" * 78)
    print("Faltenplan fuer alle NEUN Bots - Verfahren B (TB-36)")
    print(f"Go-Live-Schnitt {GO_LIVE.isoformat()} (ausschliesslich), "
          f"frueheste Falte {FRUEHESTE_FALTE}, kein Mindesttraining")
    print("=" * 78)

    plaene = faltenplan()

    print(f"\n{'Bot':<28}{'Markt':<8}{'ZR':<4}{'Laenge':<8}{'Vorlauf':<9}"
          f"{'1. Falte':<10}{'#Sel':<6}Falten")
    print("-" * 118)
    for bot, plan in plaene.items():
        namen = ", ".join(faltenname(b) for b in plan["selektionsfalten"])
        best = (faltenname(plan["bestaetigungsperiode"])
                if plan["bestaetigungsperiode"] else "-")
        print(f"{bot:<28}{plan['markt']:<8}{plan['zeitrahmen']:<4}"
              f"{str(plan['faltenlaenge_jahre']) + ' J':<8}"
              f"{str(plan['vorlauf_balken']) + ' B':<9}"
              f"{str(plan['erstes_faltenjahr'] or '-'):<10}"
              f"{plan['anzahl_selektionsfalten']:<6}{namen}  |  Best.: {best}")

    print("\nSymbolzahl je Falte (Lesart A - Kursdaten liegen am 1. Januar vor)")
    print("-" * 118)
    for bot, plan in plaene.items():
        reihe = " / ".join(str(n) for n in plan["symbolzahl_je_selektionsfalte"])
        print(f"{bot:<28}{reihe}   |  Bestaetigung: "
              f"{plan['symbolzahl_bestaetigung']}  "
              f"(von {plan['symbole_gesamt']})")

    print("\nNachrichtlich, Lesart B - voller Indikator-Vorlauf am 1. Januar")
    print("-" * 118)
    for bot, plan in plaene.items():
        a = plan["symbolzahl_je_selektionsfalte"]
        b = plan["symbolzahl_je_selektionsfalte_lesart_b"]
        reihe = " / ".join(str(n) for n in b)
        gleich = "gleich" if a == b else "ABWEICHEND"
        print(f"{bot:<28}{reihe}   |  Bestaetigung: "
              f"{plan['symbolzahl_bestaetigung_lesart_b']}   [{gleich}]")

    print("\nWelche Schranke bindet die erste Falte?")
    print("-" * 118)
    for bot, plan in plaene.items():
        quelle = ("Registerschranke " + str(FRUEHESTE_FALTE)
                  if plan["schranke_bindet"] else "Daten/Indikator-Vorlauf")
        print(f"{bot:<28}erste Falte {plan['erstes_faltenjahr']}, "
              f"ohne Schranke {plan['erstes_faltenjahr_ohne_schranke']}  "
              f"-> {quelle}")

    beispiel = plaene["rsi2_crypto"]
    nie = beispiel["nie_in_einer_selektionsfalte"]
    if nie:
        print(f"\n{len(nie)} Krypto-Symbole kommen in KEINER Selektionsfalte "
              f"vor (Beispiel {beispiel['bot']}):")
        for symbol in nie:
            print(f"  {symbol:<12} ab {beispiel['symbolbeginn'][symbol]}")

    if argumente.json:
        with open(argumente.json, "w", encoding="utf-8") as datei:
            json.dump({"go_live": GO_LIVE.isoformat(),
                       "frueheste_falte": FRUEHESTE_FALTE,
                       "plaene": plaene},
                      datei, indent=2, ensure_ascii=False, sort_keys=True,
                      default=str)
        print(f"\nBericht: {argumente.json}")

    print("\nRein lesend - es wurde nichts geaendert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
