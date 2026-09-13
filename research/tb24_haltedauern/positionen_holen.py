"""
Ein Bot, ein Prozess: Positionen MIT Ausstiegsart und Kerzenzahl herausholen
==============================================================================
Untersuchung TB-24 (Haltedauern und Zeithorizonte). **Liest nur.** An
Bot-, Backtest- oder Live-Dateien wird nichts geaendert; geschrieben wird
ausschliesslich unter `research/tb24_haltedauern/daten/`.

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
    python3 positionen_holen.py <bot_name>
"""

import json
import os
import sys

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
_EXPOSURE_DIR = os.path.join(_REPO_ROOT, "research", "exposure_messung")

if len(sys.argv) < 2:
    raise SystemExit("Aufruf: python3 positionen_holen.py <bot_name>")
BOT = sys.argv[1]

# Der Modulkopf von bot_lauf.py setzt sys.path fuer strategies/<BOT> und
# shared/ und legt die Stubs an; er liest den Bot-Namen aus sys.argv[1].
sys.path.insert(0, _EXPOSURE_DIR)
import bot_lauf as basis                                    # noqa: E402

assert basis.BOT == BOT, f"bot_lauf.py hat '{basis.BOT}' gelesen, erwartet '{BOT}'"

DATEN_DIR = os.path.join(_DIR, "daten")
os.makedirs(DATEN_DIR, exist_ok=True)

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
    positionen.to_csv(os.path.join(DATEN_DIR, f"{BOT}_positionen.csv"), index=False)
    alle.to_csv(os.path.join(DATEN_DIR, f"{BOT}_alle_trades.csv"), index=False)

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
    with open(os.path.join(DATEN_DIR, f"{BOT}_meta.json"), "w") as f:
        json.dump(meta, f, indent=2, default=str)

    abgleich = meta["abgleich_exposure_messung"]
    marke = "identisch" if abgleich.get("identisch") else f"ABWEICHEND ({abgleich})"
    print(f"{BOT}: {meta['trades_ausgefuehrt']} ausgefuehrt / "
          f"{meta['trades_uebersprungen']} uebersprungen, "
          f"Ausstiegsarten: {meta['ausstiegsarten']}, "
          f"Kerzen ohne Wert: {fehlende_kerzen}, "
          f"Abgleich Exposure-Messung: {marke}")


if __name__ == "__main__":
    main()
