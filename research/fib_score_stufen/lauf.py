"""
Messlauf je Bot - Muster, Stufen und tatsaechliche Bot-Trades
====================================================================
Erzeugt fuer EINEN der beiden Elliott-Wave-Bots eine Zeile je Muster,
das der Bot auf der Live-Parametrisierung tatsaechlich eroeffnet
haette, mit:

  * dem `fib_score`, den der Bot selbst vergeben hat,
  * der Stufe (Zahl erfuellter Bedingungen, 0-3),
  * welche der drei Bedingungen erfuellt ist,
  * den drei stetigen Verhaeltnissen darunter und ihren normierten
    Abstaenden,
  * dem Nettoergebnis des Trades nach den ECHTEN Ausstiegsregeln des
    Bots (Stop, Kursziel, Zeitausstieg) inklusive Gebuehren.

WAS AUS DEM BOT KOMMT (nicht nachgebaut)
--------------------------------------------------------------------
    multi_symbol_optimise.load_all_symbol_data      Kursdaten + Luecken
    zigzag_indicator.calculate_zigzag_with_confirmation
    elliott_wave_counter.find_causal_waves          kausale Auswahl
    backtest_elliott.run_backtest                   Trade-Simulation
    live_params                                     Parameter

Nachgebildet wird nur die ZERLEGUNG des Scores (bedingungen.py); sie
wird gegen die echte `fibonacci_score()` geprueft.

DIE SCHWELLE 0.0 STATT 0.3 - und warum das erlaubt ist
--------------------------------------------------------------------
Der Bot laeuft mit `min_fib_score = 0.3`; Stufe 0 kommt dort nie vor.
Der Auftrag verlangt Stufe 0 aber ausdruecklich als Vergleichspunkt -
ohne sie ist nicht zu beantworten, ob die Schwelle ueberhaupt etwas
abschneidet. Der Lauf setzt deshalb `min_fib_score = 0.0`.

Das ist kein harmloser Parameterwechsel: `remove_overlapping` bildet
Ueberlappungsgruppen GREEDY in chronologischer Reihenfolge. Zusaetzliche
Stufe-0-Kandidaten koennen die Gruppenbildung verschieben und damit
theoretisch auch die Menge der Muster oberhalb der Schwelle aendern.

Deshalb rechnet dieser Lauf BEIDE Varianten und vergleicht sie Zeile
fuer Zeile (`identitaet` in der JSON-Datei):

    Lauf A   min_fib_score = 0.3   - exakt der Bot
    Lauf B   min_fib_score = 0.0   - zusaetzlich Stufe 0

Nur wenn die Trades der Stufen 1-3 aus Lauf B Zeile fuer Zeile denen
aus Lauf A entsprechen, darf Lauf B als "der Bot plus Stufe 0" gelesen
werden. Stimmt es nicht, steht die Abweichung in der Ergebnisdatei und
im Bericht - dann ist Stufe 0 nur eingeschraenkt vergleichbar.

KEIN Parameter wird veraendert: `bt.STOP_LOSS_PCT` und
`bt.TAKE_PROFIT_FIB` sind Modulvariablen, die der Bot selbst von aussen
setzt (equity_simulation.py, multi_symbol_optimise.py tun genau das).
Hier werden sie auf die Werte aus `live_params.py` gesetzt - also auf
das, was live laeuft.

Aufruf:  python3 lauf.py <elliott_wave|elliott_wave_stocks>
"""

import inspect
import json
import os
import sys
import time

import botenv                                                     # noqa: E402

BOT = botenv.bot_from_argv() if __name__ == "__main__" else None

import numpy as np                                                # noqa: E402
import pandas as pd                                               # noqa: E402

import bedingungen as bd                                          # noqa: E402
import backtest_elliott as bt                                     # noqa: E402
import live_params as lp                                          # noqa: E402
import multi_symbol_optimise as mo                                # noqa: E402
from elliott_wave_counter import find_causal_waves                # noqa: E402
from zigzag_indicator import calculate_zigzag_with_confirmation   # noqa: E402

WELLENSPALTEN = ["wave0", "wave1", "wave2", "wave3", "wave4", "wave5"]
# Spalten, auf denen die Zeile-fuer-Zeile-Gleichheit von Lauf A und B
# geprueft wird. Alles, was einen Trade ausmacht.
VERGLEICHSSPALTEN = ["symbol", "signal_time", "entry_time", "entry_price",
                     "exit_time", "exit_price", "result", "pnl_pct", "fib_score"]


def _use_tp_kwargs():
    """`use_take_profit` gibt es nur im Aktien-Backtest (der Krypto-Bot
    kennt kein Abschalten des Kursziels). Wird uebergeben, wenn der Bot
    den Parameter hat - mit dem Wert aus live_params."""
    if "use_take_profit" in inspect.signature(bt.run_backtest).parameters:
        return {"use_take_profit": bool(getattr(lp, "USE_TAKE_PROFIT", True))}
    return {}


def trades_eines_laufs(data: dict, min_fib_score: float) -> pd.DataFrame:
    """Alle Trades beider Bots ueber alle Symbole - ausschliesslich mit
    Bot-Funktionen, nur die Score-Schwelle ist ein Parameter.

    Die Wellenspalten werden ueber `signal_time` an die Trades geheftet.
    `signal_time` ist das Wellenende und je Symbol eindeutig (TB-20:
    0 Dubletten in allen 173 Symbolen); die Eindeutigkeit wird hier
    trotzdem geprueft statt geglaubt."""
    bt.STOP_LOSS_PCT = float(lp.STOP_LOSS_PCT)
    bt.TAKE_PROFIT_FIB = float(lp.TAKE_PROFIT_FIB)
    kwargs = _use_tp_kwargs()

    bloecke, muster_gesamt, ohne_trade = [], 0, 0
    for symbol in sorted(data):
        price_df = data[symbol]
        zigzag = calculate_zigzag_with_confirmation(price_df, deviation_pct=float(lp.DEVIATION_PCT))
        if len(zigzag) < 6:
            continue
        wellen = find_causal_waves(zigzag, min_fib_score=min_fib_score,
                                    freshness_bars=bt.SIGNAL_FRESHNESS_BARS,
                                    direction="bearish")     # Long-only, wie im Bot
        if wellen.empty:
            continue
        muster_gesamt += len(wellen)

        trades = bt.run_backtest(price_df, wellen, **kwargs)
        if trades.empty:
            ohne_trade += len(wellen)
            continue
        ohne_trade += len(wellen) - len(trades)

        wellen = wellen.copy()
        wellen["signal_time"] = pd.to_datetime(wellen["end_time"])
        if wellen["signal_time"].duplicated().any():
            raise AssertionError(
                f"{symbol}: doppelte end_time in den Wellen - die Zuordnung "
                "Trade->Welle waere nicht eindeutig. TB-20 hat hier 0 Dubletten "
                "gemessen; diese Annahme gilt nicht mehr.")

        trades = trades.copy()
        trades["signal_time"] = pd.to_datetime(trades["signal_time"])
        vorher = len(trades)
        trades = trades.merge(
            wellen[["signal_time", "start_time"] + WELLENSPALTEN],
            on="signal_time", how="left", validate="one_to_one")
        if len(trades) != vorher or trades[WELLENSPALTEN].isna().any().any():
            raise AssertionError(f"{symbol}: Trade ohne zugehoerige Welle.")
        # Gegenprobe: der vom Bot in den Trade geschriebene fib_score muss
        # der derselben Welle sein.
        if not np.allclose(trades["fib_score"].astype(float),
                           [bd.score_nachbildung([r[c] for c in WELLENSPALTEN])
                            for _, r in trades.iterrows()]):
            raise AssertionError(f"{symbol}: fib_score des Trades passt nicht zur Welle.")

        trades["symbol"] = symbol
        bloecke.append(trades)

    out = pd.concat(bloecke, ignore_index=True) if bloecke else pd.DataFrame()
    out.attrs["muster_gesamt"] = muster_gesamt
    out.attrs["muster_ohne_trade"] = ohne_trade
    return out


def anreichern(trades: pd.DataFrame) -> pd.DataFrame:
    """Stufe, erfuellte Bedingungen, Verhaeltnisse und Abstaende je Zeile."""
    if trades.empty:
        return trades
    zeilen = []
    for _, r in trades.iterrows():
        punkte = [float(r[c]) for c in WELLENSPALTEN]
        verh = bd.verhaeltnisse(punkte) or {}
        abst = bd.abstaende(punkte) or {}
        abst_f = bd.abstaende_fib(punkte) or {}
        erf = bd.erfuellte(punkte)
        zeile = {
            "stufe": int(sum(erf)),
            "score_nachbildung": bd.score_nachbildung(punkte),
            "naehe": bd.naehe(punkte),
            "naehe_fib": bd.naehe_fib(punkte),
            "gesamtabstand": bd.gesamtabstand(punkte),
            "naehe_weich": bd.naehe_weich(punkte),
            "entartet": bd.verhaeltnisse(punkte) is None,
        }
        for i, name in enumerate(bd.NAMEN):
            zeile[f"erf_{name}"] = bool(erf[i])
            zeile[f"r_{name}"] = verh.get(name, float("nan"))
            zeile[f"d_{name}"] = abst.get(name, float("nan"))
            zeile[f"dfib_{name}"] = abst_f.get(name, float("nan"))
        # Welche Bedingungen erfuellt sind, als lesbares Kuerzel:
        # "-w3-" heisst "nur die Welle-3-Bedingung".
        zeile["muster_bedingungen"] = "".join(
            n.split("_")[0] if e else "-" for n, e in zip(("w2", "w3", "w4"), erf))
        zeilen.append(zeile)
    zusatz = pd.DataFrame(zeilen, index=trades.index)
    out = pd.concat([trades, zusatz], axis=1)

    if not np.allclose(out["fib_score"].astype(float), out["score_nachbildung"].astype(float)):
        raise AssertionError("Nachbildung weicht vom fib_score des Bots ab.")
    if not (out["stufe"] == out["fib_score"].map(bd.stufe_aus_score)).all():
        raise AssertionError("Stufe aus Punkten und Stufe aus Score widersprechen sich.")

    out["haltedauer_balken"] = _haltedauer(out)
    return out


def _haltedauer(trades: pd.DataFrame) -> pd.Series:
    """Haltedauer in Balken - bei Krypto Stunden, bei Aktien Handelstage.
    Aus den Zeitstempeln nicht exakt bestimmbar (Wochenenden), deshalb
    fuer Aktien als Kalendertage ausgewiesen; die Spalte dient nur der
    Beschreibung, in keine Kennzahl geht sie ein."""
    dauer = pd.to_datetime(trades["exit_time"]) - pd.to_datetime(trades["entry_time"])
    einheit = "h" if bt.MAX_HOLD_HOURS > 100 else "D"
    return (dauer / pd.Timedelta(1, einheit)).round(2)


def identitaet(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """Ist der Trade-Satz aus Lauf A (min_fib 0.3) Zeile fuer Zeile
    derselbe wie die Stufen 1-3 aus Lauf B (min_fib 0.0)?"""
    b_oberhalb = b[b["stufe"] >= 1]
    schluessel = ["symbol", "signal_time"]
    a_s = a.sort_values(schluessel, kind="stable").reset_index(drop=True)
    b_s = b_oberhalb.sort_values(schluessel, kind="stable").reset_index(drop=True)

    ergebnis = {
        "trades_lauf_a_min_fib_0_3": int(len(a_s)),
        "trades_lauf_b_stufe_ab_1": int(len(b_s)),
        "gleiche_anzahl": bool(len(a_s) == len(b_s)),
    }
    if len(a_s) != len(b_s):
        ergebnis["zeile_fuer_zeile_identisch"] = False
        ergebnis["hinweis"] = ("Die Schwellensenkung veraendert die Menge der Muster "
                               "oberhalb der Schwelle - Stufe 0 ist nur eingeschraenkt "
                               "vergleichbar. Siehe remove_overlapping im Modulkopf.")
        return ergebnis

    abweichungen = {}
    for spalte in VERGLEICHSSPALTEN:
        links, rechts = a_s[spalte], b_s[spalte]
        if pd.api.types.is_numeric_dtype(links):
            gleich = np.allclose(links.astype(float), rechts.astype(float),
                                 rtol=0, atol=1e-9, equal_nan=True)
        else:
            gleich = links.astype(str).equals(rechts.astype(str))
        if not gleich:
            abweichungen[spalte] = int((links.astype(str) != rechts.astype(str)).sum())
    ergebnis["zeile_fuer_zeile_identisch"] = not abweichungen
    ergebnis["geprueefte_spalten"] = VERGLEICHSSPALTEN
    ergebnis["abweichende_spalten"] = abweichungen
    return ergebnis


def datenbasis(data: dict) -> dict:
    starts = [df["open_time"].min() for df in data.values() if len(df)]
    enden = [df["open_time"].max() for df in data.values() if len(df)]
    return {
        "symbole": len(data),
        "symbolliste": sorted(data),
        "kerzen_gesamt": int(sum(len(df) for df in data.values())),
        "von": str(min(starts)) if starts else None,
        "bis": str(max(enden)) if enden else None,
    }


def main():
    botenv.print_hinweis()
    t0 = time.time()
    print(f"\n[{BOT}] Kursdaten laden ...")
    data = mo.load_all_symbol_data()
    if not data:
        raise SystemExit(f"{BOT}: keine Kursdaten in data/ gefunden.")

    parameter = {
        "deviation_pct": float(lp.DEVIATION_PCT),
        "stop_loss_pct": float(lp.STOP_LOSS_PCT),
        "take_profit_fib": float(lp.TAKE_PROFIT_FIB),
        "use_take_profit": bool(getattr(lp, "USE_TAKE_PROFIT", True)),
        "signal_freshness_bars": int(bt.SIGNAL_FRESHNESS_BARS),
        "max_hold_bars": int(bt.MAX_HOLD_HOURS),
        "trading_fee_pct": float(bt.TRADING_FEE_PCT),
        "slippage_pct": float(bt.SLIPPAGE_PCT),
        "live_params_last_updated": str(getattr(lp, "LAST_UPDATED", "")),
    }
    print(f"[{BOT}] {len(data)} Symbole, Parameter: {parameter}")

    print(f"[{BOT}] Lauf A (min_fib_score = 0.3, exakt der Bot) ...")
    a = anreichern(trades_eines_laufs(data, 0.3))
    print(f"[{BOT}]   {len(a)} Trades")

    print(f"[{BOT}] Lauf B (min_fib_score = 0.0, zusaetzlich Stufe 0) ...")
    b_roh = trades_eines_laufs(data, 0.0)
    b = anreichern(b_roh)
    print(f"[{BOT}]   {len(b)} Trades, davon Stufe 0: {int((b['stufe'] == 0).sum())}")

    ident = identitaet(a, b)
    print(f"[{BOT}] Zeile fuer Zeile identisch (Stufen 1-3): "
          f"{ident['zeile_fuer_zeile_identisch']}")

    csv_pfad = os.path.join(botenv.RESULTS_DIR, f"{BOT}_muster.csv")
    b.to_csv(csv_pfad, index=False)

    meta = {
        "hinweis": botenv.UNTERSUCHUNG_HINWEIS,
        "bot": BOT,
        "erzeugt": time.strftime("%Y-%m-%d %H:%M:%S"),
        "parameter": parameter,
        "datenbasis": datenbasis(data),
        "muster": {
            "lauf_b_muster_gesamt": int(b_roh.attrs.get("muster_gesamt", 0)),
            "lauf_b_muster_ohne_trade": int(b_roh.attrs.get("muster_ohne_trade", 0)),
            "lauf_b_trades": int(len(b)),
            "je_stufe": {str(k): int(v) for k, v in
                         sorted(b["stufe"].value_counts().items())},
            "je_fib_score": {str(k): int(v) for k, v in
                             sorted(b["fib_score"].value_counts().items())},
            "symbole_mit_trades": int(b["symbol"].nunique()),
        },
        "identitaet_lauf_a_gegen_b": ident,
        "kausalitaet": {
            "wellen_funktion": "elliott_wave_counter.find_causal_waves",
            "einstieg": "Schlusskurs des Bestaetigungsbalkens (entry_idx)",
            "bemerkung": ("Der seit PR #26 kausal korrigierte Pfad. run_backtest "
                          "verweigert den Dienst ohne die Spalte entry_idx - ein "
                          "Lauf mit Look-Ahead waere hier gar nicht moeglich."),
        },
        "dateien": {"muster_csv": os.path.basename(csv_pfad)},
    }
    json_pfad = os.path.join(botenv.RESULTS_DIR, f"{BOT}_lauf.json")
    with open(json_pfad, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)

    print(f"[{BOT}] geschrieben: {csv_pfad}")
    print(f"[{BOT}] geschrieben: {json_pfad}")
    print(f"[{BOT}] Dauer: {time.time() - t0:.1f}s")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()
