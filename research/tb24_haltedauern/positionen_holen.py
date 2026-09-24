"""
Ein Bot, ein Prozess: Positionen MIT Ausstiegsart und Kerzenzahl herausholen
==============================================================================
Untersuchung TB-24 (Haltedauern und Zeithorizonte). **Liest nur.** An
Bot-, Backtest- oder Live-Dateien wird nichts geaendert; geschrieben wird
ausschliesslich in den Ordner, den `--ziel` nennt.

ZIEL UND EINMAL-SCHREIBSPERRE (TB-98, Register 36.1 und 40.6)
------------------------------------------------------------------------------
Bis TB-98 schrieb dieses Skript fest nach `research/tb24_haltedauern/daten/`.
Die neun `<bot>_alle_trades.csv` dort sind seit Register 40.6 Eingabedateien
einer Herleitung von Registertext (33.2) und bleiben als historischer Stand
(`78e2bc6`) liegen - ein Aufruf haette sie ueberschrieben. Seitdem:

  (3)  `--ziel ORDNER` ist **Pflicht**, es gibt **keine Voreinstellung**. Ohne
       Argument endet der Aufruf mit 2, bevor irgendetwas geladen wird. Der
       Ordner muss bestehen; er wird nicht angelegt (sonst 2).
  (2)  **Einmal-Schreibsperre, vor der Rechnung:** Besteht eine der vier
       Zieldateien des Bots schon, endet der Aufruf mit 1, nennt Pfad und
       SHA-256 der vorhandenen Datei(en) und hat weder gerechnet noch
       geschrieben. Geschrieben wird mit `O_CREAT|O_EXCL`; entsteht eine Datei
       waehrend des Laufs, ebenfalls 1. Nie ueberschreiben, auch nicht mit
       identischem Inhalt (36.1: "Die Sperre ist staerker, wenn sie duemmer ist").
  B5   Neben die drei Dateien kommt `<bot>_herkunft.json`: Erzeuger, Zeit,
       Code-Commit, Selektionsmodus (Audit aus `shared/paths.py`, sonst null)
       und je geschriebener Datei der SHA-256. **Keine Trade-Zahlen** (27.1).

⚠️ Die Rechenwege sind unveraendert (TB-98 B3, AST-Vergleich gegen
`e87b06f`): anders sind nur die Zielbestimmung und die Schreibaufrufe. Das
Ausgabeformat ist bytegleich - `to_csv(index=False)` und
`json.dumps(indent=2, default=str)` erzeugen denselben Text wie vorher der
Aufruf mit Dateipfad bzw. Dateiobjekt.

WAS DIESES SKRIPT ANDERS MACHT ALS `research/exposure_messung/bot_lauf.py`
------------------------------------------------------------------------------
Die Exposure-Messung brauchte je Position `allocation` und `capital_after`.
Fuer Haltedauern kommen drei Angaben hinzu, die dort weggefallen sind:

* `result`  - die Ausstiegsart des Bots selbst (`stop_loss`, `take_profit`,
              `time_exit`, `sma_exit`, `trend_flip`). Sie steht in den
              Trade-Tabellen der Backtests und ueberlebt
              `collect_all_trades()`, weil das die Spalten unveraendert
              durchreicht. Ohne sie laesst sich ein Stop-Loss nach zwei Tagen
              nicht von einem Zeitausstieg nach fuenfzehn unterscheiden -
              genau die Trennung, die die Aufgabe verlangt.
* `kerzen`  - Anzahl der Kerzen zwischen Einstieg und Ausstieg, aus der
              Kursreihe des jeweiligen Symbols GEZAEHLT (nicht aus
              Kalendertagen umgerechnet). Die neun Bots laufen auf drei
              Zeitrahmen; nur so ist "Haltedauer" zwischen 1h, 4h und 1d
              vergleichbar.
* `entry_price` / `exit_price` - nur zur Nachvollziehbarkeit im Datensatz.

DIE BOT-SPEZIFISCHEN AUFRUFE WERDEN NICHT NEU GESCHRIEBEN
------------------------------------------------------------------------------
`hole_trades()` und `simuliere()` kommen per Import aus
`research/exposure_messung/bot_lauf.py`. Dort steht, mit welchen Argumenten
`collect_all_trades()` je Bot aufzurufen ist - inklusive des
BTC-Regimefilters, den `volatility_breakout_crypto` bewusst erst danach
anwendet. Diese Zuordnung ein zweites Mal hinzuschreiben waere genau die
Doppelfuehrung, an der dieses Projekt schon einmal unbemerkt auseinander-
gelaufen ist (Uebergabeprotokoll Prinzip 11). Mitimportiert werden dabei
auch die Stubs fuer `binance`, `yfinance` und `fetch_binance_data`, die in
dieser Umgebung fehlen bzw. Zugangsdaten enthalten.

Der Import fuehrt den Modulkopf von `bot_lauf.py` aus. Der liest `sys.argv[1]`
(darum steht der Bot-Name auch hier an erster Stelle) und legt
`research/exposure_messung/daten/` an, falls es fehlt - geschrieben wird dort
nichts, `bot_lauf.main()` wird nie aufgerufen.

DIE ZUORDNUNG "WELCHER TRADE WURDE AUSGEFUEHRT"
------------------------------------------------------------------------------
Uebernommen aus `bot_lauf.py`, weil es keinen zweiten korrekten Weg gibt:
`simulate_portfolio()` gibt seine Liste der offenen Positionen nicht heraus.
Sie wird deshalb zweimal mit demselben Trade-Satz aufgerufen - einmal
unveraendert, einmal mit einer Zeilenkennung in der `symbol`-Spalte
(`AAPL#417`), die dort reine Beschriftung ist. Dass die Kennzeichnung die
Simulation nicht veraendert hat, wird geprueft, nicht angenommen.

Nutzung:
    python3 positionen_holen.py <bot_name> --ziel <ordner>

Rueckgabewerte (Register 36.5): 0 geschrieben, 1 Ziel existiert (Befund),
2 Aufruf unvollstaendig oder Zielordner fehlt.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
_EXPOSURE_DIR = os.path.join(_REPO_ROOT, "research", "exposure_messung")

if len(sys.argv) < 2:
    raise SystemExit("Aufruf: python3 positionen_holen.py <bot_name> --ziel <ordner>")
BOT = sys.argv[1]

# Rueckgabewerte nach 36.5. BEFUND: das Ziel existiert; NICHT_MOEGLICH: ohne
# Ziel oder ohne Zielordner laesst sich nicht erzeugen.
BEFUND = 1
NICHT_MOEGLICH = 2

# ⚠️ 36.1 (3): das Ziel nur durch ausdrueckliches Argument, KEINE
# Voreinstellung. Geprueft wird hier, vor dem Import von bot_lauf.py und vor
# jedem Laden - ein Aufruf ohne Ziel verbraucht nichts.
_aufruf = argparse.ArgumentParser(
    description="Positionen und alle gefundenen Trades eines Bots (TB-24). "
                "Schreibt einmalig in den Ordner aus --ziel (Register 36.1).")
_aufruf.add_argument("bot")
_aufruf.add_argument("--ziel", required=True, metavar="ORDNER",
                     help="bestehender Ordner; vorhandene Zieldateien werden NIE "
                          "ueberschrieben - der Lauf endet dann mit 1")
_args = _aufruf.parse_args(sys.argv[1:])
if _args.bot != BOT:
    # bot_lauf.py liest den Bot-Namen fest aus sys.argv[1].
    sys.stderr.write("ABBRUCH: der Bot-Name muss das erste Argument sein.\n")
    sys.exit(NICHT_MOEGLICH)
ZIEL_DIR = os.path.abspath(_args.ziel)
if not os.path.isdir(ZIEL_DIR):
    sys.stderr.write("ABBRUCH: Zielordner fehlt: %s - er wird nicht angelegt.\n" % ZIEL_DIR)
    sys.exit(NICHT_MOEGLICH)

ZIELDATEIEN = [f"{BOT}_positionen.csv", f"{BOT}_alle_trades.csv",
               f"{BOT}_meta.json", f"{BOT}_herkunft.json"]

# Der Modulkopf von bot_lauf.py setzt sys.path fuer strategies/<BOT> und
# shared/ und legt die Stubs an; er liest den Bot-Namen aus sys.argv[1].
sys.path.insert(0, _EXPOSURE_DIR)
import bot_lauf as basis                                    # noqa: E402

assert basis.BOT == BOT, f"bot_lauf.py hat '{basis.BOT}' gelesen, erwartet '{BOT}'"

TRENNER = basis.TRENNER

# Zeitrahmen je Bot - nur als Beschriftung der Ausgabe. Die Kerzenzahl wird
# gezaehlt, nicht daraus berechnet; eine falsche Angabe hier veraendert also
# keine Messung. Quelle: Uebergabeprotokoll Abschnitt 2.
ZEITRAHMEN = {
    "elliott_wave": "1h",
    "t3_supertrend": "4h",
    "rsi2_crypto": "1d",
    "turtle_soup_crypto": "1d",
    "volatility_breakout_crypto": "1d",
    "elliott_wave_stocks": "1d",
    "rsi2_mean_reversion": "1d",
    "turtle_soup_stocks": "1d",
    "volatility_breakout": "1d",
}

ANLAGEKLASSE = {
    "elliott_wave": "krypto",
    "t3_supertrend": "krypto",
    "rsi2_crypto": "krypto",
    "turtle_soup_crypto": "krypto",
    "volatility_breakout_crypto": "krypto",
    "elliott_wave_stocks": "aktien",
    "rsi2_mean_reversion": "aktien",
    "turtle_soup_stocks": "aktien",
    "volatility_breakout": "aktien",
}


def _sha256(pfad):
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sperre_vor_der_rechnung() -> bool:
    """36.1 (2), vor der Rechnung: True (und Meldung), wenn eine Zieldatei
    schon besteht. Dann wird nichts geladen, gerechnet oder geschrieben."""
    vorhanden = [os.path.join(ZIEL_DIR, n) for n in ZIELDATEIEN
                 if os.path.lexists(os.path.join(ZIEL_DIR, n))]
    for pfad in vorhanden:
        print("ABBRUCH (36.1 (2)): Ziel existiert, nichts gerechnet, nichts geschrieben."
              "\n  Pfad:    %s\n  SHA-256: %s" % (pfad, _sha256(pfad)))
    return bool(vorhanden)


def _schreibe_einmal(name: str, inhalt: str) -> str:
    """Genau einmal schreiben (`O_CREAT|O_EXCL`); SHA-256 des Geschriebenen.

    `newline=""`: kein Uebersetzen von Zeilenenden - der Text geht so auf die
    Platte, wie `to_csv`/`json.dumps` ihn liefern."""
    pfad = os.path.join(ZIEL_DIR, name)
    try:
        fd = os.open(pfad, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        print("ABBRUCH (36.1 (2)): Ziel entstand waehrend des Laufs, nichts "
              "ueberschrieben.\n  Pfad:    %s\n  SHA-256: %s" % (pfad, _sha256(pfad)))
        sys.exit(BEFUND)
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        f.write(inhalt)
    return _sha256(pfad)


def _schreibe_herkunft(hashes: dict):
    """B5: die Herkunftsnotiz neben den Listen. Keine Trade-Zahlen (27.1)."""
    import paths
    audit = paths.startpruefung()
    lauf = subprocess.run(["git", "-C", _REPO_ROOT, "rev-parse", "HEAD"],
                          capture_output=True, text=True)
    notiz = {
        "erzeuger": "research/tb24_haltedauern/positionen_holen.py",
        "bot": BOT,
        "zeit_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "code_commit": lauf.stdout.strip() if lauf.returncode == 0 else None,
        "selektionsmodus": audit,
        "dateien_sha256": hashes,
    }
    _schreibe_einmal(f"{BOT}_herkunft.json",
                     json.dumps(notiz, indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def kursreihe(eintrag):
    """`load_all_symbol_data()` liefert je Bot entweder den DataFrame direkt
    oder das Paar (DataFrame, entry_cutoff) - beides kommt vor (Aktien-Bots
    mit RECENT_YEARS_ONLY liefern das Paar)."""
    if isinstance(eintrag, tuple):
        return eintrag[0]
    return eintrag


def kerzen_je_trade(trades: pd.DataFrame, all_data: dict) -> pd.Series:
    """Anzahl der Kerzen von Einstieg bis Ausstieg, je Trade aus der
    Kursreihe des Symbols GEZAEHLT: Kerzen mit
    entry_time <= open_time <= exit_time, beide Enden eingeschlossen.

    Eine Position, die auf derselben Kerze eroeffnet und geschlossen wuerde,
    ergibt damit 1. Fehlt die Kursreihe (kann nicht vorkommen, weil die
    Trades daraus entstanden sind), bleibt der Wert leer statt geraten.
    """
    zeiten = {}
    for symbol, eintrag in all_data.items():
        df = kursreihe(eintrag)
        zeiten[symbol] = pd.to_datetime(df["open_time"]).sort_values().to_numpy()

    werte = []
    for symbol, ein, aus in zip(trades["symbol"], trades["entry_time"], trades["exit_time"]):
        reihe = zeiten.get(symbol)
        if reihe is None:
            werte.append(pd.NA)
            continue
        links = reihe.searchsorted(pd.Timestamp(ein), side="left")
        rechts = reihe.searchsorted(pd.Timestamp(aus), side="right")
        werte.append(int(rechts - links))
    return pd.Series(werte, index=trades.index, dtype="Int64")


def abgleich_exposure_messung(positionen: pd.DataFrame) -> dict:
    """Pflicht-Gegencheck: dieselben ausgefuehrten Positionen wie in
    `research/exposure_messung/daten/<bot>_positionen.csv`?

    Diese Untersuchung rechnet auf demselben Trade-Satz wie die
    Exposure-Messung. Waeren die Positionen verschieden, wuerde hier etwas
    anderes gemessen als dort - eine Abweichung ist deshalb ein Befund und
    kein Abbruchgrund (gemeldet wird sie in jedem Fall).
    """
    pfad = os.path.join(_EXPOSURE_DIR, "daten", f"{BOT}_positionen.csv")
    if not os.path.exists(pfad):
        return {"datei": os.path.relpath(pfad, _REPO_ROOT), "vorhanden": False}

    alt = pd.read_csv(pfad, parse_dates=["entry_time", "exit_time"])
    spalten = ["symbol", "entry_time", "exit_time", "pnl_pct", "allocation"]
    zahlenspalten = ["pnl_pct", "allocation"]
    gleich_lang = len(alt) == len(positionen)
    abweichende = None
    if gleich_lang:
        def ordne(df):
            df = df[spalten].sort_values(spalten, kind="stable").reset_index(drop=True)
            df[zahlenspalten] = df[zahlenspalten].round(6)
            return df
        a, b = ordne(alt.copy()), ordne(positionen.copy())
        abweichende = int((a != b).any(axis=1).sum())
    return {
        "datei": os.path.relpath(pfad, _REPO_ROOT),
        "vorhanden": True,
        "zeilen_dort": int(len(alt)),
        "zeilen_hier": int(len(positionen)),
        "identisch": bool(gleich_lang and abweichende == 0),
        "abweichende_zeilen": abweichende,
    }


def main():
    import equity_simulation as es

    all_data = es.load_all_symbol_data()
    if not all_data:
        raise SystemExit(f"{BOT}: keine Kursdaten gefunden.")

    trades = basis.hole_trades(es, all_data)
    if trades is None or trades.empty:
        raise SystemExit(f"{BOT}: keine Trades.")

    trades = trades.copy()
    trades["entry_time"] = pd.to_datetime(trades["entry_time"])
    trades["exit_time"] = pd.to_datetime(trades["exit_time"])
    if trades["symbol"].astype(str).str.contains(TRENNER).any():
        raise SystemExit(f"{BOT}: Symbol enthaelt '{TRENNER}' - Kennzeichnung nicht eindeutig.")

    allocation_pct = es.ALLOCATION_PCT
    hat_limit = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
    max_concurrent = (getattr(es, "MAX_CONCURRENT_POSITIONS", None) if hat_limit
                      else basis._KEIN_LIMIT_PARAMETER)
    limit_wert = None if max_concurrent is basis._KEIN_LIMIT_PARAMETER else max_concurrent

    # --- Lauf 1: unveraendert -----------------------------------------------
    ergebnis = basis.simuliere(es, trades, allocation_pct, max_concurrent)
    equity = ergebnis["equity_curve"]

    # --- Lauf 2: mit Zeilenkennung im Symbol --------------------------------
    markiert = trades.copy()
    markiert["symbol"] = [f"{s}{TRENNER}{i}" for i, s in zip(markiert.index, markiert["symbol"])]
    ergebnis_markiert = basis.simuliere(es, markiert, allocation_pct, max_concurrent)
    equity_markiert = ergebnis_markiert["equity_curve"]

    kennzeichnung_neutral = bool(
        len(equity) == len(equity_markiert)
        and ergebnis["num_executed"] == ergebnis_markiert["num_executed"]
        and ergebnis["num_skipped"] == ergebnis_markiert["num_skipped"]
        and equity["capital_after"].reset_index(drop=True).equals(
            equity_markiert["capital_after"].reset_index(drop=True))
        and equity["allocation"].reset_index(drop=True).equals(
            equity_markiert["allocation"].reset_index(drop=True))
    )
    if not kennzeichnung_neutral:
        raise SystemExit(f"{BOT}: Kennzeichnung hat die Simulation veraendert - Abbruch.")

    kennungen = equity_markiert["symbol"].astype(str).str.rsplit(TRENNER, n=1).str[-1].astype(int)
    if kennungen.duplicated().any():
        raise SystemExit(f"{BOT}: dieselbe Trade-Zeile doppelt ausgefuehrt - Abbruch.")

    # --- Alle gefundenen Trades, mit Kerzenzahl und Ausstiegsart ------------
    trades["kerzen"] = kerzen_je_trade(trades, all_data)
    trades["ausgefuehrt"] = False
    trades.loc[kennungen.values, "ausgefuehrt"] = True

    ausgabespalten = [s for s in ("symbol", "entry_time", "exit_time", "result",
                                   "pnl_pct", "entry_price", "exit_price", "kerzen",
                                   "ausgefuehrt")
                      if s in trades.columns]
    alle = trades[ausgabespalten].copy()
    alle.insert(0, "trade_zeile", trades.index)

    positionen = trades.loc[kennungen.values, ausgabespalten].copy()
    positionen.insert(0, "trade_zeile", kennungen.values)
    positionen["allocation"] = equity["allocation"].values
    positionen["capital_after"] = equity["capital_after"].values

    # Gegenproben (Prinzip 12): die Ausstiegszeit aus der Trade-Tabelle muss
    # die der Kapitalkurve sein, und kein Einstieg darf nach seinem Ausstieg
    # liegen. Beide Pruefungen stammen aus bot_lauf.py.
    if not (positionen["exit_time"].to_numpy() == pd.to_datetime(equity["time"]).to_numpy()).all():
        raise SystemExit(f"{BOT}: Ausstiegszeiten passen nicht zusammen - Abbruch.")
    if (positionen["entry_time"] > positionen["exit_time"]).any():
        raise SystemExit(f"{BOT}: Einstieg nach Ausstieg - Abbruch.")

    positionen = positionen.sort_values("entry_time", kind="stable").reset_index(drop=True)
    alle = alle.sort_values("entry_time", kind="stable").reset_index(drop=True)
    hashes = {}
    hashes[f"{BOT}_positionen.csv"] = _schreibe_einmal(
        f"{BOT}_positionen.csv", positionen.to_csv(index=False))
    hashes[f"{BOT}_alle_trades.csv"] = _schreibe_einmal(
        f"{BOT}_alle_trades.csv", alle.to_csv(index=False))

    fehlende_kerzen = int(alle["kerzen"].isna().sum())
    ohne_result = "result" not in trades.columns

    meta = {
        "bot": BOT,
        "zeitrahmen": ZEITRAHMEN.get(BOT),
        "anlageklasse": ANLAGEKLASSE.get(BOT),
        "startkapital": es.STARTING_CAPITAL,
        "allocation_pct": allocation_pct,
        "max_concurrent_positions": limit_wert,
        "bot_hat_limit_parameter": hat_limit,
        "trades_gefunden": int(len(trades)),
        "trades_ausgefuehrt": int(ergebnis["num_executed"]),
        "trades_uebersprungen": int(ergebnis["num_skipped"]),
        "symbole_gefunden": int(trades["symbol"].nunique()),
        "symbole_ausgefuehrt": int(positionen["symbol"].nunique()),
        "erster_einstieg": str(positionen["entry_time"].min()),
        "letzter_ausstieg": str(positionen["exit_time"].max()),
        "ausstiegsarten": (None if ohne_result
                            else {str(k): int(v) for k, v
                                  in positionen["result"].value_counts().items()}),
        "spalte_result_vorhanden": not ohne_result,
        "kerzen_ohne_wert": fehlende_kerzen,
        "kennzeichnung_neutral": kennzeichnung_neutral,
        "abgleich_exposure_messung": abgleich_exposure_messung(positionen),
    }
    hashes[f"{BOT}_meta.json"] = _schreibe_einmal(
        f"{BOT}_meta.json", json.dumps(meta, indent=2, default=str))
    _schreibe_herkunft(hashes)

    abgleich = meta["abgleich_exposure_messung"]
    marke = "identisch" if abgleich.get("identisch") else f"ABWEICHEND ({abgleich})"
    print(f"{BOT}: {meta['trades_ausgefuehrt']} ausgefuehrt / "
          f"{meta['trades_uebersprungen']} uebersprungen, "
          f"Ausstiegsarten: {meta['ausstiegsarten']}, "
          f"Kerzen ohne Wert: {fehlende_kerzen}, "
          f"Abgleich Exposure-Messung: {marke}")


if __name__ == "__main__":
    if sperre_vor_der_rechnung():
        sys.exit(BEFUND)
    main()
