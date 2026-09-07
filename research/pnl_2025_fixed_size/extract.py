"""
2025er-Trades eines Bots mit der LIVE gueltigen Konfiguration
====================================================================
Nutzung:  python3 extract.py <schluessel>

<schluessel> ist einer aus konfiguration.REIHENFOLGE - also ein
Botname, oder bei elliott_wave einer der beiden Staende
(elliott_wave_alt / elliott_wave_neu).

--------------------------------------------------------------------
Was hier bewusst nicht passiert
--------------------------------------------------------------------
Es wird KEIN Backtest nachgebaut. Trades kommen aus
`equity_simulation.collect_all_trades` des jeweiligen Bots, also aus
demselben Code, den auch die bisherigen Auswertungen benutzen. Diese
Datei entscheidet nur, MIT WELCHEN PARAMETERN er aufgerufen wird -
und das ist der eigentliche Punkt der Aufgabe:

* Parameter kommen aus `live_params.py`, nicht aus den gleichnamigen
  Konstanten in `equity_simulation.py` (Sync-Check, PR #24).
* Was sich nicht als Argument durchreichen laesst, wird als
  Modulkonstante gesetzt - VOR dem Laden der Daten, weil manche Bots
  ihre Indikatoren schon beim Laden berechnen. Jede Abweichung
  zwischen Modulkonstante und Live-Wert wird protokolliert.
* Bei volatility_breakout_crypto wird der BTC-Regimefilter nachgezogen:
  `live_params.BTC_REGIME_FILTER_ENABLED` ist True, aber
  `collect_all_trades` wendet ihn nicht an (PR #22-Nachtrag). Bei
  t3_supertrend tut collect_all_trades das bereits selbst - dort wird
  nichts nachgezogen, sonst waere er doppelt drin.

--------------------------------------------------------------------
Die Rechnung
--------------------------------------------------------------------
P&L je Trade = 1000 USD x (exit_price - entry_price) / entry_price

So in der Aufgabe vorgegeben: BRUTTO, also ohne Gebuehren und
Slippage. Mehrere Bots modellieren Kosten in ihrer eigenen Spalte
`pnl_pct`; deren Ergebnis wird als zweite Spalte mitgefuehrt, damit
der Unterschied sichtbar ist statt unterzugehen.

1000 USD wird vereinfachend mit 1000 USDT gleichgesetzt - keine
EUR-Umrechnung, keine Wechselkursdaten. Bei den Aktien-Bots sind die
Kurse ohnehin USD.
"""

import json
import os
import sys

import pandas as pd

import botenv
import konfiguration as cfg

SCHLUESSEL = sys.argv[1] if len(sys.argv) > 1 else None
if SCHLUESSEL not in cfg.REIHENFOLGE:
    raise SystemExit(f"Nutzung: python3 extract.py <{'|'.join(cfg.REIHENFOLGE)}>")

IST_ELLIOTT = SCHLUESSEL in cfg.ELLIOTT
BOT = cfg.ELLIOTT[SCHLUESSEL]["bot"] if IST_ELLIOTT else SCHLUESSEL
botenv.setup(BOT)

import live_params as lp                 # noqa: E402
import multi_symbol_optimise as mo       # noqa: E402
import equity_simulation as es           # noqa: E402


def stumm(fn, *args, **kwargs):
    """Die Lade-Funktionen der Bots schreiben Hinweise auf stdout."""
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return fn(*args, **kwargs)


def konstanten_angleichen(eintraege: list) -> list:
    """Setzt Modulkonstanten auf den Live-Wert und meldet Abweichungen."""
    protokoll = []
    for modulname, attr, lp_name in eintraege:
        modul = __import__(modulname)
        ist = getattr(modul, attr, None)
        soll = getattr(lp, lp_name)
        protokoll.append({"modul": modulname, "konstante": attr,
                           "live_params": lp_name, "wert_im_modul": ist,
                           "wert_live": soll, "abweichung": ist != soll})
        setattr(modul, attr, soll)
    return protokoll


def trades_holen():
    """Liefert (trades, verwendete_konfiguration, protokoll)."""
    protokoll = {"konstanten": [], "regimefilter": None}

    if IST_ELLIOTT:
        eintrag = cfg.ELLIOTT[SCHLUESSEL]
        kwargs = eintrag["kwargs"]
        if kwargs is None:      # elliott_wave_stocks - aus live_params
            kwargs = {"deviation_pct": float(lp.DEVIATION_PCT),
                       "stop_loss_pct": float(lp.STOP_LOSS_PCT),
                       "take_profit_fib": float(lp.TAKE_PROFIT_FIB)}
        kwargs = dict(kwargs)
        if "use_take_profit" in es.collect_all_trades.__code__.co_varnames:
            kwargs["use_take_profit"] = bool(getattr(lp, "USE_TAKE_PROFIT", True))
        all_data = stumm(mo.load_all_symbol_data)
        trades = es.collect_all_trades(all_data, **kwargs)
        limit_name = eintrag["limit"]
        limit = getattr(lp, limit_name, None) if isinstance(limit_name, str) else limit_name
        return trades, kwargs, limit, all_data, protokoll

    eintrag = cfg.STANDARD[SCHLUESSEL]
    # ZUERST die Konstanten, DANN laden - manche Bots berechnen ihre
    # Indikatoren bereits in load_all_symbol_data.
    protokoll["konstanten"] = konstanten_angleichen(eintrag["konstanten"])
    all_data = stumm(mo.load_all_symbol_data)
    kwargs = {arg: getattr(lp, lp_name) for arg, lp_name in eintrag["kwargs"].items()}
    trades = es.collect_all_trades(all_data, **kwargs)

    if eintrag["regimefilter"]:
        aktiv = bool(getattr(lp, "BTC_REGIME_FILTER_ENABLED", False))
        vorher = len(trades)
        if aktiv:
            from regime_filter import compute_btc_regime, filter_trades_by_regime
            if "BTCUSDT" not in all_data:
                raise SystemExit("BTCUSDT fehlt - der Regimefilter braucht die BTC-Kurse.")
            trades = filter_trades_by_regime(trades, compute_btc_regime(all_data["BTCUSDT"]))
        protokoll["regimefilter"] = {
            "live_aktiv": aktiv, "trades_vorher": vorher, "trades_nachher": int(len(trades)),
            "geblockt": int(vorher - len(trades)),
            "hinweis": "collect_all_trades wendet den Filter nicht selbst an - "
                       "hier nachgezogen (PR #22-Nachtrag)"}

    limit = getattr(lp, eintrag["limit"], None)
    return trades, kwargs, limit, all_data, protokoll


def gleichzeitigkeit(trades: pd.DataFrame, limit) -> dict:
    """Beantwortet die Frage aus PR #23 fuer das Jahr 2025: gab es
    Momente, in denen mehr Signale auftraten als Positionsplaetze frei
    waren? Nur dann haengt die Trade-Auswahl von der
    Verarbeitungsreihenfolge ab.

    Simuliert wird chronologisch ueber ALLE Trades, nicht nur die von
    2025 - eine Ende 2024 eroeffnete Position belegt im Januar 2025
    noch einen Platz. Uebersprungene Trades belegen keinen Platz."""
    if trades.empty or limit is None:
        return {"limit": limit, "relevant_2025": False,
                 "grund": "kein Positionslimit" if limit is None else "keine Trades"}

    df = trades.sort_values("entry_time", kind="stable").reset_index(drop=True)
    offen = []              # exit_times der tatsaechlich eroeffneten Positionen
    geblockt_2025 = 0
    geblockte_zeitpunkte = set()
    for _, t in df.iterrows():
        jetzt = t["entry_time"]
        offen = [e for e in offen if e > jetzt]
        im_jahr = jetzt.year == cfg.JAHR
        if len(offen) >= limit:
            if im_jahr:
                geblockt_2025 += 1
                geblockte_zeitpunkte.add(jetzt)
            continue
        offen.append(t["exit_time"])

    # Wie viele Trades teilen sich einen dieser Zeitpunkte? Genau dort
    # entscheidet die Zeilenreihenfolge, wer den letzten Platz bekommt.
    im_jahr = df[df["entry_time"].dt.year == cfg.JAHR]
    gleichzeitig = int(im_jahr[im_jahr["entry_time"].isin(geblockte_zeitpunkte)]
                       .groupby("entry_time").size().gt(1).sum())
    return {
        "limit": int(limit),
        "relevant_2025": geblockt_2025 > 0,
        "geblockte_trades_2025": geblockt_2025,
        "zeitpunkte_am_limit_2025": len(geblockte_zeitpunkte),
        "davon_mit_mehreren_signalen_gleichzeitig": gleichzeitig,
        "hinweis": ("Die Zeilenreihenfolge entscheidet nur dort, wo mehrere "
                     "Signale denselben Einstiegszeitpunkt teilen und das Limit "
                     "bereits ausgeschoepft ist."),
    }


def main():
    trades, kwargs, limit, all_data, protokoll = trades_holen()
    eintrag = cfg.ELLIOTT.get(SCHLUESSEL) or cfg.STANDARD[SCHLUESSEL]

    ergebnis = {
        "schluessel": SCHLUESSEL, "bot": BOT,
        "beschreibung": eintrag.get("beschreibung", "Live-Konfiguration aus live_params.py"),
        "parameterquelle": eintrag.get("quelle", "live_params.py"),
        "verwendete_parameter": {k: (None if v is None else v) for k, v in kwargs.items()},
        "live_params_stand": getattr(lp, "LAST_UPDATED", None),
        "positionslimit_live": (None if limit is None else int(limit)),
        "symbole_geladen": len(all_data),
        "trades_gesamt": int(len(trades)),
        "konstanten_angeglichen": protokoll["konstanten"],
        "regimefilter": protokoll["regimefilter"],
        "positionsgroesse_usd": cfg.POSITIONSGROESSE_USD,
        "jahr": cfg.JAHR,
    }

    if trades.empty:
        ergebnis.update({"trades_2025": 0, "pnl_usd": 0.0, "gewinnrate_pct": None})
    else:
        for spalte in ("entry_price", "exit_price", "entry_time", "exit_time"):
            if spalte not in trades.columns:
                raise SystemExit(f"{BOT}: Spalte {spalte} fehlt im Trade-Satz.")
        trades = trades.copy()
        trades["entry_time"] = pd.to_datetime(trades["entry_time"])
        trades["exit_time"] = pd.to_datetime(trades["exit_time"])

        # Kursluecken: ein fehlender Ausstiegskurs macht die Summe unbrauchbar
        # (dasselbe Problem wie in research/elliott_wave_params/). Betroffene
        # Trades werden gestrichen und gezaehlt, nicht stillschweigend
        # mitgerechnet.
        luecke = trades[["entry_price", "exit_price"]].isna().any(axis=1)
        ergebnis["gestrichen_wegen_kursluecke"] = int(luecke.sum())
        if luecke.any():
            ergebnis["kursluecke_symbole"] = sorted(set(trades.loc[luecke, "symbol"]))
            trades = trades[~luecke].reset_index(drop=True)

        ergebnis["gleichzeitigkeit"] = gleichzeitigkeit(trades, limit)

        jahr = trades[trades["entry_time"].dt.year == cfg.JAHR].copy()
        jahr["pnl_usd"] = (cfg.POSITIONSGROESSE_USD
                            * (jahr["exit_price"] - jahr["entry_price"]) / jahr["entry_price"])
        ergebnis["trades_2025"] = int(len(jahr))
        ergebnis["pnl_usd"] = round(float(jahr["pnl_usd"].sum()), 2)
        ergebnis["gewinnrate_pct"] = (round(float((jahr["pnl_usd"] > 0).mean() * 100), 1)
                                       if len(jahr) else None)
        ergebnis["bester_trade_usd"] = (round(float(jahr["pnl_usd"].max()), 2) if len(jahr) else None)
        ergebnis["schlechtester_trade_usd"] = (round(float(jahr["pnl_usd"].min()), 2) if len(jahr) else None)
        ergebnis["symbole_2025"] = int(jahr["symbol"].nunique()) if len(jahr) else 0

        # Zweite Spalte: die Bot-eigene pnl_pct, die bei mehreren Bots
        # Gebuehren und Slippage enthaelt.
        if "pnl_pct" in jahr.columns and len(jahr):
            jahr["pnl_usd_netto"] = cfg.POSITIONSGROESSE_USD * jahr["pnl_pct"] / 100.0
            ergebnis["pnl_usd_netto_laut_bot"] = round(float(jahr["pnl_usd_netto"].sum()), 2)
            ergebnis["kostenmodell_im_bot"] = bool(
                abs(float((jahr["pnl_usd"] - jahr["pnl_usd_netto"]).abs().sum())) > 0.01)
        else:
            ergebnis["pnl_usd_netto_laut_bot"] = None
            ergebnis["kostenmodell_im_bot"] = None

        pfad = os.path.join(botenv.RESULTS_DIR, f"{SCHLUESSEL}_trades_2025.csv")
        spalten = [c for c in ("symbol", "entry_time", "entry_price", "exit_time",
                                "exit_price", "result", "pnl_pct", "pnl_usd", "pnl_usd_netto")
                   if c in jahr.columns]
        jahr[spalten].to_csv(pfad, index=False)
        ergebnis["trades_datei"] = os.path.basename(pfad)

    pfad = os.path.join(botenv.RESULTS_DIR, f"{SCHLUESSEL}_pnl.json")
    with open(pfad, "w") as fh:
        json.dump(ergebnis, fh, indent=2, default=str, ensure_ascii=False)

    print(f"{SCHLUESSEL}: {ergebnis['trades_2025']} Trades 2025, "
          f"P&L {ergebnis['pnl_usd']:+.2f} USD, "
          f"Gewinnrate {ergebnis['gewinnrate_pct']} %")
    if ergebnis.get("regimefilter"):
        r = ergebnis["regimefilter"]
        print(f"  BTC-Regimefilter: {r['geblockt']} von {r['trades_vorher']} Trades geblockt")
    for k in ergebnis["konstanten_angeglichen"]:
        if k["abweichung"]:
            print(f"  ABWEICHUNG angeglichen: {k['modul']}.{k['konstante']} "
                  f"{k['wert_im_modul']} -> {k['wert_live']} (live_params.{k['live_params']})")
    g = ergebnis.get("gleichzeitigkeit")
    if g and g.get("relevant_2025"):
        print(f"  Positionslimit {g['limit']} war 2025 bindend: "
              f"{g['geblockte_trades_2025']} Trades haetten keinen Platz gefunden")
    print(f"  Gespeichert: {pfad}")


if __name__ == "__main__":
    main()
