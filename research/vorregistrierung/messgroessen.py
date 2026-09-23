#!/usr/bin/env python3
"""
TB-30a - Messgroessen: die Zahlen, auf denen die Rastergrenzen ruhen
==============================================================================
Jede Rastergrenze der Vorregistrierung ist eine **Rechnung** auf einer hier
gemessenen Groesse, kein von Hand getippter Wert. Das ist der Kern der
Zusicherung "kein Grenzsatz erwaehnt einen Live-Wert": ein Wert, der aus
Kursdaten und Handelskosten berechnet wird, kann einen Live-Parameter nur
durch Zufall treffen - und genau darauf prueft `pruefe_grenzsaetze.py`.

Gemessen wird ausschliesslich auf **Nicht-Bot-Daten**:

  * `data/*.csv`      - Kurse der beiden Universen
  * `config/*.txt`    - die Universumsdateien
  * Handelskosten     - `TRADING_FEE_PCT` + `SLIPPAGE_PCT` aus dem Bot-Code,
                        als **Kostenkonvention**, nicht als Handelsparameter

Kein Backtest laeuft, kein Bot-Ergebnis wird gelesen, keine Datenbank
angefasst. Die Ausgabe (`ergebnisse/messgroessen.json`) ist Eingabe fuer
`registerdaten.py`.

DIE VIER ZULAESSIGEN GRUNDLAGEN
------------------------------------------------------------------------------
Die Vorregistrierung laesst genau vier Begruendungsgrundlagen fuer eine
Rastergrenze zu. Jede hier gemessene Groesse gehoert zu genau einer davon:

  kosten          Round-Trip-Kosten (2 x (Gebuehr + Slippage))
  datenfrequenz   Balken je Kalenderjahr, Balken je Handelswoche
  volatilitaet    Balken-Sigma, Median der 20-Balken-Spanne, ATR-Median,
                  Verteilungsquantile von RSI(2) und ADX
  haltedauer      Median-Haltedauer in Balken (aus research/tb24_haltedauern/)

Die Haltedauern stammen aus TB-24 und sind dort auf den Bot-Trades gemessen.
Sie sind die einzige Groesse mit Bot-Bezug; sie geht ausschliesslich in
Purge-Laengen und in die Donchian-Untergrenze ein, beides Groessen, die die
Aufgabenstellung ausdruecklich aus `research/tb24_haltedauern/` verlangt.
"""

import argparse
import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

BASE_DIR = os.environ.get("TB30A_BASE_DIR") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
ERGEBNISSE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ergebnisse")

# --- Kostenkonvention ---------------------------------------------------------
# 0,1 % Gebuehr + 0,05 % Slippage je Order, Ein- und Ausstieg: 0,30 % je
# Round-Trip. Der Wert steht in allen neun Bots zeichengleich; er ist eine
# Konvention der Messkette, kein Handelsparameter, und deshalb als Grundlage
# einer Rastergrenze zugelassen.
GEBUEHR_PCT = 0.1
SLIPPAGE_PCT = 0.05
ROUND_TRIP_KOSTEN_PCT = 2 * (GEBUEHR_PCT + SLIPPAGE_PCT)

# --- Zeitrahmen ---------------------------------------------------------------
# Balken je Kalenderjahr: Krypto handelt an allen Kalendertagen, Aktien an
# rund 252 Handelstagen. Aus diesen beiden Zahlen folgen alle uebrigen.
BALKEN_JE_JAHR = {
    ("krypto", "1d"): 365,
    ("krypto", "4h"): 365 * 6,
    ("krypto", "1h"): 365 * 24,
    ("aktien", "1d"): 252,
}
BALKEN_JE_HANDELSWOCHE = {
    ("krypto", "1d"): 7,
    ("krypto", "4h"): 7 * 6,
    ("krypto", "1h"): 7 * 24,
    ("aktien", "1d"): 5,
}

# Symbole, die das Volumen-Ranking zwar besteht, die aber keine eigenstaendige
# Krypto-Volatilitaet haben (an Gold gekoppelte Token) - dieselbe Liste wie in
# shared/symbols_config.py.
AUSGESCHLOSSEN = {"XAUTUSDT", "PAXGUSDT"}

MIN_BALKEN = 300  # ein Symbol mit weniger Balken traegt kein Quantil


def universum(datei: str) -> list:
    pfad = os.path.join(CONFIG_DIR, datei)
    with open(pfad, encoding="utf-8") as f:
        symbole = [z.strip() for z in f if z.strip()]
    return [s for s in symbole if s not in AUSGESCHLOSSEN]


def lies(symbol: str, suffix: str):
    pfad = os.path.join(DATA_DIR, f"{symbol}_{suffix}.csv")
    if not os.path.exists(pfad):
        return None
    df = pd.read_csv(pfad, parse_dates=["open_time"])
    df = df.dropna(subset=["open", "high", "low", "close"])
    if len(df) < MIN_BALKEN:
        return None
    return df


def rsi(close: np.ndarray, periode: int = 2) -> np.ndarray:
    """Wilder-RSI, zeichengleich zur Fassung in den Bot-Indikatoren."""
    delta = np.diff(close, prepend=close[0])
    gewinn = np.where(delta > 0, delta, 0.0)
    verlust = np.where(delta < 0, -delta, 0.0)
    ag = pd.Series(gewinn).ewm(alpha=1.0 / periode, adjust=False).mean().to_numpy()
    av = pd.Series(verlust).ewm(alpha=1.0 / periode, adjust=False).mean().to_numpy()
    rs = np.divide(ag, av, out=np.full_like(ag, np.inf), where=av > 0)
    return 100.0 - 100.0 / (1.0 + rs)


def adx(high, low, close, laenge: int = 14) -> np.ndarray:
    """Wilder-ADX - dieselbe Formel wie strategies/t3_supertrend/indicators.py."""
    auf = high[1:] - high[:-1]
    ab = low[:-1] - low[1:]
    plus_dm = np.where((auf > ab) & (auf > 0), auf, 0.0)
    minus_dm = np.where((ab > auf) & (ab > 0), ab, 0.0)
    tr = np.maximum(high[1:] - low[1:],
                    np.maximum(np.abs(high[1:] - close[:-1]),
                               np.abs(low[1:] - close[:-1])))
    def rma(x):
        return pd.Series(x).ewm(alpha=1.0 / laenge, adjust=False).mean().to_numpy()
    atr = rma(tr)
    with np.errstate(divide="ignore", invalid="ignore"):
        plus_di = 100.0 * np.where(atr > 0, rma(plus_dm) / atr, np.nan)
        minus_di = 100.0 * np.where(atr > 0, rma(minus_dm) / atr, np.nan)
        summe = plus_di + minus_di
        dx = 100.0 * np.where(summe > 0, np.abs(plus_di - minus_di) / summe, np.nan)
    return rma(np.nan_to_num(dx, nan=0.0))


def je_zeitrahmen(symbole: list, suffix: str) -> dict:
    """Volatilitaets- und Verteilungskennzahlen eines Universums je Zeitrahmen.

    Alle Kennzahlen sind **Mediane ueber die Symbole** von symbolweisen
    Medianen: ein einzelnes Symbol mit ausserordentlicher Historie verschiebt
    damit keine Rastergrenze.
    """
    sigmas, spannen, atrs, tiefabstand = [], [], [], []
    rsi_quantile = {q: [] for q in (1, 2, 5, 10)}
    adx_quantile = {q: [] for q in (50, 60, 70, 80, 90)}
    benutzt = []

    for s in sorted(symbole):
        df = lies(s, suffix)
        if df is None:
            continue
        benutzt.append(s)
        c = df["close"].to_numpy(dtype=float)
        h = df["high"].to_numpy(dtype=float)
        l = df["low"].to_numpy(dtype=float)

        # Balken-Sigma: Standardabweichung der logarithmischen Balkenrenditen
        sigmas.append(float(np.std(np.diff(np.log(c)), ddof=1)) * 100.0)

        # Median der 20-Balken-Spanne, in Prozent des Schlusskurses
        hoch = pd.Series(h).rolling(20).max().to_numpy()
        tief = pd.Series(l).rolling(20).min().to_numpy()
        spannen.append(float(np.nanmedian((hoch - tief) / c * 100.0)))

        # ATR(14) in Prozent - nur als Berichtsgroesse
        tr = np.maximum(h[1:] - l[1:],
                        np.maximum(np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])))
        atrs.append(float(np.nanmedian(
            pd.Series(tr).rolling(14).mean().to_numpy() / c[1:] * 100.0)))

        # Abstand Schluss -> Tagestief desselben Balkens, in Prozent.
        # Das ist die Weite des "structural"-Stops der beiden Turtle-Soup-Bots.
        tiefabstand.append(float(np.nanmedian((c - l) / c * 100.0)))

        r = rsi(c, 2)[200:]
        for q in rsi_quantile:
            rsi_quantile[q].append(float(np.nanpercentile(r, q)))
        a = adx(h, l, c, 14)[200:]
        for q in adx_quantile:
            adx_quantile[q].append(float(np.nanpercentile(a, q)))

    if not benutzt:
        raise SystemExit(f"Keine Kursdaten fuer Suffix {suffix} gefunden.")

    return {
        "symbole_gemessen": len(benutzt),
        "balken_sigma_pct": round(float(np.median(sigmas)), 4),
        "spanne20_median_pct": round(float(np.median(spannen)), 4),
        "atr14_median_pct": round(float(np.median(atrs)), 4),
        "tiefabstand_median_pct": round(float(np.median(tiefabstand)), 4),
        "rsi2_quantile": {str(q): round(float(np.median(v)), 4)
                          for q, v in rsi_quantile.items()},
        "adx_quantile": {str(q): round(float(np.median(v)), 4)
                         for q, v in adx_quantile.items()},
    }


def haltedauern() -> dict:
    """Median- und Maximal-Haltedauern je Bot aus TB-24.

    Gelesen, nicht neu gerechnet: die Zahlen sind dort gegen einen eigenen
    Test abgesichert, und eine zweite Messung derselben Groesse waere genau
    die doppelt gefuehrte Zahl, vor der das Protokoll warnt.
    """
    pfad = os.path.join(BASE_DIR, "research", "tb24_haltedauern",
                        "ergebnisse", "haltedauern_je_bot.csv")
    df = pd.read_csv(pfad)
    out = {}
    for _, z in df.iterrows():
        out[z["bot"]] = {
            "median_tage": float(z["tage_median"]),
            "max_tage": float(z["tage_max"]),
            "median_balken": float(z["kerzen_median"]),
            "n_positionen": int(z["n"]),
        }
    return out


def datenbereiche() -> dict:
    """Erster und letzter Balken je Universum und Zeitrahmen.

    Legt fest, welche Kalenderjahre ueberhaupt als Falte in Frage kommen -
    und belegt den Grund, aus dem der Krypto-Faltenplan bis TB-31 ein
    Platzhalter bleibt.
    """
    out = {}
    for markt, datei, suffixe in (
        ("krypto", "top25_symbols.txt", ("1d", "4h", "1h")),
        ("aktien", "sp500_top150.txt", ("1d",)),
    ):
        symbole = universum(datei)
        for suffix in suffixe:
            erste, letzte, n = [], [], 0
            for s in symbole:
                df = lies(s, suffix)
                if df is None:
                    continue
                n += 1
                erste.append(df["open_time"].iloc[0])
                letzte.append(df["open_time"].iloc[-1])
            if not erste:
                continue
            out[f"{markt}_{suffix}"] = {
                "symbole": n,
                "frueheste": str(pd.Timestamp(min(erste)).date()),
                "median_beginn": str(pd.Timestamp(pd.Series(erste).median()).date()),
                "spaeteste_beginn": str(pd.Timestamp(max(erste)).date()),
                "letzter_balken": str(pd.Timestamp(max(letzte)).date()),
            }
    return out


def _sha256_datei(pfad: str) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for stueck in iter(lambda: f.read(65536), b""):
            h.update(stueck)
    return h.hexdigest()


def voreinstellung_ziel() -> str:
    """36.1 (3): nie ein Sperrlistenpfad als Voreinstellung.

    `ergebnisse/messgroessen.json` steht in `herkunft.py::EINGEFROREN`; sein
    Hash wird am Tag bezeugt. Nach Fables Praezisierung zu 36.1 (1) (Antwort
    23c) ist es damit gesperrt, gleich unter welchem Namen die Liste laeuft.
    """
    stempel = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    return os.path.join(ERGEBNISSE, f"messgroessen_{stempel}.json")


def schreibe_messgroessen(mess: dict, ziel: str):
    """36.1 (2): Einmal-Schreibsperre. Rueckgabe 1, wenn das Ziel existiert.

    ⚠️ Das Ausgabeformat ist UNVERAENDERT: indent=2, ensure_ascii=False,
    sort_keys=True, abschliessender Zeilenumbruch. Jede Abweichung hier
    entwertete Fables Determinismusnachweis (Antwort 23c: der Lauf auf einen
    neuen Pfad muss `ergebnisse/messgroessen.json` BYTEGLEICH reproduzieren).
    """
    if os.path.exists(ziel):
        return 1, ("\nABBRUCH (36.1 (2)): Ziel existiert, nichts geschrieben."
                   "\n  Pfad:    %s\n  SHA-256: %s"
                   % (os.path.relpath(ziel), _sha256_datei(ziel)))
    fd = os.open(ziel, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(mess, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    return 0, "\nGeschrieben: %s\n  SHA-256: %s" % (ziel, _sha256_datei(ziel))


def main(argv=None):
    p = argparse.ArgumentParser(
        description=("Messgroessen des Vorregistrierungslaufs. Schreibt einmalig; "
                     "Voreinstellung ist ein Name mit Zeitstempel (36.1 (3))."))
    p.add_argument("--ziel", default=None,
                   help=("Ausgabedatei (Standard: ergebnisse/messgroessen_"
                         "<UTC-Zeitstempel>.json). Ein vorhandenes Ziel wird NIE "
                         "ueberschrieben - der Lauf endet dann mit 1."))
    args = p.parse_args(argv)
    ziel = args.ziel or voreinstellung_ziel()

    os.makedirs(ERGEBNISSE, exist_ok=True)

    # ⚠️ Die Sperre greift VOR der Rechnung. `je_zeitrahmen` laeuft ueber alle
    #    Symbole; ein Lauf gegen ein vorhandenes Ziel soll nichts verbrauchen.
    if os.path.exists(ziel):
        print("\nABBRUCH (36.1 (2)): Ziel existiert, nichts gerechnet, nichts geschrieben."
              "\n  Pfad:    %s\n  SHA-256: %s"
              % (os.path.relpath(ziel), _sha256_datei(ziel)))
        return 1

    krypto = universum("top25_symbols.txt")
    aktien = universum("sp500_top150.txt")

    mess = {
        "kosten": {
            "gebuehr_pct_je_order": GEBUEHR_PCT,
            "slippage_pct_je_order": SLIPPAGE_PCT,
            "round_trip_pct": ROUND_TRIP_KOSTEN_PCT,
        },
        "datenfrequenz": {
            "balken_je_jahr": {f"{m}_{t}": v for (m, t), v in BALKEN_JE_JAHR.items()},
            "balken_je_handelswoche": {f"{m}_{t}": v
                                       for (m, t), v in BALKEN_JE_HANDELSWOCHE.items()},
        },
        "volatilitaet": {},
        "haltedauer": haltedauern(),
        "datenbereiche": datenbereiche(),
        "universum": {
            "krypto": {"datei": "config/top25_symbols.txt", "symbole": len(krypto)},
            "aktien": {"datei": "config/sp500_top150.txt", "symbole": len(aktien)},
        },
    }

    for markt, symbole, suffixe in (("krypto", krypto, ("1d", "4h", "1h")),
                                    ("aktien", aktien, ("1d",))):
        for suffix in suffixe:
            mess["volatilitaet"][f"{markt}_{suffix}"] = je_zeitrahmen(symbole, suffix)

    rc, meldung = schreibe_messgroessen(mess, ziel)
    if rc != 0:
        print(meldung)
        return rc

    print(__doc__.strip().split("\n")[0])
    print(f"\nRound-Trip-Kosten: {ROUND_TRIP_KOSTEN_PCT:.2f} %")
    print(f"\n{'Zeitrahmen':14s} {'n':>4s} {'Sigma/Balken':>13s} "
          f"{'Spanne20':>10s} {'ATR14':>8s} {'Schluss-Tief':>13s}")
    for k, v in sorted(mess["volatilitaet"].items()):
        print(f"{k:14s} {v['symbole_gemessen']:4d} {v['balken_sigma_pct']:12.3f}% "
              f"{v['spanne20_median_pct']:9.2f}% {v['atr14_median_pct']:7.2f}% "
              f"{v['tiefabstand_median_pct']:12.2f}%")
    print(meldung)
    return 0


if __name__ == "__main__":
    sys.exit(main())
