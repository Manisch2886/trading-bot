"""
Die Live-Seite: Haltedauern aus den echten Bot-Datenbanken
==============================================================================
Untersuchung TB-24. **Liest nur**, und zwar ausschliesslich lesend:
jede Datenbank wird ueber `file:...?mode=ro` geoeffnet - dieselbe
Betriebsart, die `notifications/monitor.py` und `broker/bot_db.py` benutzen.
SQLite verweigert in diesem Modus jeden Schreibversuch, auch einen
versehentlichen.

WARUM DIESES SKRIPT SEPARAT STEHT UND IN DER CLOUD-SITZUNG NICHTS LIEFERT
------------------------------------------------------------------------------
Die neun `paper_trading_<bot>.db` sind laut `.gitignore` nicht im Repo; sie
liegen nur auf dem Rechner des Nutzers. Eine Cloud-Sitzung sieht sie nicht.
Das Skript meldet das dann ausdruecklich als Befund ("keine Datenbank
gefunden") statt eine leere Tabelle zu liefern, die wie "keine Trades"
aussieht - genau die Verwechslung, gegen die `docs/DATENLUECKEN.md`
geschrieben wurde.

Auf dem Rechner des Nutzers ist es ohne Vorbereitung lauffaehig und
beantwortet dieselbe Frage wie `auswertung.py`, nur auf der echten Historie:
Median, Quartile und Perzentile der Haltedauern je Bot, getrennt nach
Ausstiegsart.

WAS DIE LIVE-SEITE TRAGEN KANN UND WAS NICHT
------------------------------------------------------------------------------
Stand des Uebergabeprotokolls (Abschnitt 4.3b, Punkt 15 in Abschnitt 9):
**kein** Bot erreicht `MIN_LIVE_CLOSED_TRADES = 10` geschlossene Trades.
Bei rund zwei Dutzend geschlossenen Trades ueber neun Bots ist ein Median je
Bot eine Zahl aus zwei bis vier Werten. Sie taugt als **Plausibilitaets-
abgleich** gegen die Backtest-Medianwerte, nicht als eigene Messung. Das
Skript schreibt diesen Vorbehalt in seine Ausgabe, damit die Zahl nicht
irgendwann ohne ihn weiterwandert.

Manuelle Ausstiege (`result = 'manual_close'`, siehe Protokoll 4.3) werden
gesondert ausgewiesen: ihre Haltedauer ist eine Entscheidung des Nutzers,
keine Eigenschaft der Strategie.

Nutzung (auf dem Rechner des Nutzers, im Projektordner):
    python3 research/tb24_haltedauern/live_haltedauern.py
"""

import json
import os
import sqlite3
import sys

import pandas as pd

import haltedauer_kern as k

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
ERGEBNIS_DIR = os.path.join(_DIR, "ergebnisse")

BOTS = [
    "elliott_wave", "t3_supertrend", "rsi2_crypto", "turtle_soup_crypto",
    "volatility_breakout_crypto", "elliott_wave_stocks", "rsi2_mean_reversion",
    "turtle_soup_stocks", "volatility_breakout",
]

MANUELL = "manual_close"


def db_pfad(bot: str) -> str:
    return os.path.join(_REPO_ROOT, f"paper_trading_{bot}.db")


def lese_trades(bot: str):
    """Geschlossene Trades eines Bots, oder None, wenn die Datenbank fehlt.

    Rueckgabe None und leerer DataFrame sind AUSDRUECKLICH verschiedene
    Faelle: "nicht nachgesehen" gegen "nachgesehen, nichts da".
    """
    pfad = db_pfad(bot)
    if not os.path.exists(pfad):
        return None
    with sqlite3.connect(f"file:{pfad}?mode=ro", uri=True) as conn:
        df = pd.read_sql(
            "SELECT symbol, entry_time, exit_time, result, pnl_pct, status "
            "FROM trades WHERE status != 'open'", conn)
    df["entry_time"] = pd.to_datetime(df["entry_time"])
    df["exit_time"] = pd.to_datetime(df["exit_time"])
    return df.dropna(subset=["entry_time", "exit_time"])


def main():
    zeilen = []
    fehlend = []
    for bot in BOTS:
        df = lese_trades(bot)
        if df is None:
            fehlend.append(bot)
            continue
        strategie = df[df["result"] != MANUELL]
        manuell = int((df["result"] == MANUELL).sum())
        kz = k.kennzahlen(k.haltedauer_tage(strategie)) if not strategie.empty else {"n": 0}
        zeile = {"bot": bot, "geschlossen_gesamt": int(len(df)),
                 "davon_manuell": manuell, "n": kz["n"]}
        for feld in ("p10", "q1", "median", "q3", "p90", "mittel"):
            zeile[f"tage_{feld}"] = round(kz[feld], 2) if kz["n"] else None
        zeile["ausstiegsarten"] = (
            "; ".join(f"{a}:{n}" for a, n in df["result"].value_counts().items()))
        zeilen.append(zeile)

    tabelle = pd.DataFrame(zeilen)

    print("Live-Haltedauern aus den Bot-Datenbanken (schreibgeschuetzt gelesen)")
    print("=" * 78)
    if fehlend:
        print(f"KEINE DATENBANK GEFUNDEN fuer {len(fehlend)} von {len(BOTS)} Bots:")
        for bot in fehlend:
            print(f"  - {os.path.relpath(db_pfad(bot), _REPO_ROOT)}")
        print("Die neun paper_trading_<bot>.db sind gitignored und liegen nur auf dem")
        print("Rechner des Nutzers. In einer Cloud-Sitzung ist das der erwartete Fall")
        print("und KEIN Fehler - es heisst nur, dass die Live-Seite hier nicht")
        print("gemessen werden kann.")
        print()

    if tabelle.empty:
        print("Keine Live-Daten auswertbar. Die Backtest-Seite steht in")
        print("ergebnisse/haltedauern_je_bot.csv und traegt den Befund allein.")
        return 0

    print(tabelle.to_string(index=False))
    print()
    gesamt = int(tabelle["n"].sum())
    print(f"Insgesamt {gesamt} geschlossene Strategie-Trades ueber "
          f"{len(tabelle)} Bots.")
    print("VORBEHALT: kein Bot erreicht MIN_LIVE_CLOSED_TRADES = 10 "
          "(Uebergabeprotokoll 4.3b).")
    print("Diese Medianwerte taugen als Plausibilitaetsabgleich gegen die "
          "Backtest-Seite,")
    print("nicht als eigene Messung.")

    os.makedirs(ERGEBNIS_DIR, exist_ok=True)
    tabelle.to_csv(os.path.join(ERGEBNIS_DIR, "live_haltedauern.csv"), index=False)
    with open(os.path.join(ERGEBNIS_DIR, "live_haltedauern_lage.json"), "w") as f:
        json.dump({"datenbanken_gefunden": [b for b in BOTS if b not in fehlend],
                    "datenbanken_fehlend": fehlend,
                    "geschlossene_strategie_trades": gesamt}, f, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
