#!/usr/bin/env python3
"""
TB-162 - Rekonstruktion der ausgefuehrten Positionen aus Trade-Liste und equity_curve
==============================================================================
Entscheid F9, Register R97 (b) zweiter Satz (Fable 14.10.b): ein Lauf mit
UNVERAENDERTEN Trades (kein Feld beschrieben, auch nicht im Speicher; A9, 41.1),
die Zuordnung aus Trade-Liste und equity_curve. Das ist eine REKONSTRUKTION,
kein Nachweis, keine Probe, keine Definition (R95 (b), (c)).
positionen_holen.py (Doppellauf, verstoesst gegen A9, R97 (a)) wird weder
ausgefuehrt noch eingebunden.

Zuordnungsregel (je Zeile der equity_curve, in ihrer Reihenfolge):
  Z1 Kandidaten: noch nicht zugeordnete Trade-Zeilen mit gleichem Symbol (als Text),
     gleichem Ausstiegszeitpunkt (exit_time = time, in UTC) und gleichem pnl_pct
     (Abweichung <= TOL_PNL).
  Z2 Mehr als ein Kandidat: Kapitalprobe - allocation der Kurvenzeile gegen
     allocation_pct x Kapital beim Einstieg (capital_after der letzten Kurvenzeile
     mit time <= entry_time, sonst Startkapital); Abweichung <= TOL_GELD.
  Z3 Bleiben mehrere, die in symbol, entry_time, exit_time, entry_price,
     exit_price und pnl_pct gleich sind: die mit der kleinsten Zeilennummer
     (inhaltsgleich; gezaehlt).
  Z4 Sonst (kein Kandidat, oder mehrere verschiedene): NICHT ZUORDENBAR - gezaehlt
     und mit Kurvenzeile gemeldet; die Position fehlt in der Liste.
Toleranz: TOL_PNL = 1e-9 Prozentpunkte (die Kurve traegt den pnl_pct der Trade-
Zeile); TOL_GELD = 0.01 (allocation und capital_after sind auf 2 Stellen gerundet).
Ausgabe in der Buchungsreihenfolge der equity_curve (Spalte kurvenzeile).
Reine Funktionen; die Trade-Liste wird nur gelesen.
"""
import numpy as np
import pandas as pd

TOL_PNL = 1e-9
TOL_GELD = 0.01
REGEL = ("Z1 gleiches Symbol, exit_time = time (UTC), |pnl_pct-Diff| <= %g; Z2 bei mehreren: Kapitalprobe "
         "|allocation - allocation_pct x Kapital beim Einstieg| <= %g; Z3 inhaltsgleiche Kandidaten: kleinste Zeile; "
         "Z4 sonst nicht zuordenbar (gemeldet)" % (TOL_PNL, TOL_GELD))
_INHALT = ("symbol", "entry_time", "exit_time", "entry_price", "exit_price", "pnl_pct")
_NULL = pd.Timestamp("1970-01-01", tz="UTC")


def ns_utc(werte) -> np.ndarray:
    """Zeitpunkte als ganze Nanosekunden seit 1970 (UTC); naive Werte gelten als UTC."""
    t = pd.Series(pd.to_datetime(pd.Series(list(werte)), utc=True))
    return ((t - _NULL) // pd.Timedelta(1, "ns")).to_numpy(dtype="int64")


def zuordnen(trades: pd.DataFrame, kurve: pd.DataFrame, startkapital: float, allocation_pct: float):
    """-> (positionen, bericht). positionen: neue Tabelle (trade_zeile = Position in trades)."""
    n = len(trades)
    sym = trades["symbol"].astype(str).to_numpy()
    ein = ns_utc(trades["entry_time"]) if n else np.zeros(0, "int64")
    aus = ns_utc(trades["exit_time"]) if n else np.zeros(0, "int64")
    pnl = trades["pnl_pct"].astype(float).to_numpy()
    nach_schluessel = {}
    for i in range(n):
        nach_schluessel.setdefault((sym[i], int(aus[i])), []).append(i)
    k_sym = kurve["symbol"].astype(str).to_numpy() if len(kurve) else np.zeros(0, object)
    k_zeit = ns_utc(kurve["time"]) if len(kurve) else np.zeros(0, "int64")
    k_pnl = kurve["pnl_pct"].astype(float).to_numpy() if len(kurve) else np.zeros(0)
    k_alloc = kurve["allocation"].astype(float).to_numpy() if len(kurve) else np.zeros(0)
    k_kap = kurve["capital_after"].astype(float).to_numpy() if len(kurve) else np.zeros(0)

    def kapital_beim_einstieg(t):
        j = int(np.searchsorted(k_zeit, t, side="right")) - 1
        return float(startkapital) if j < 0 else float(k_kap[j])

    def inhalt(i):
        return tuple(str(trades[s].iloc[i]) if s in trades.columns else None for s in _INHALT)

    benutzt, paare, fehl = set(), [], []
    zaehl = {"eindeutig": 0, "durch_kapitalprobe": 0, "inhaltsgleich": 0}
    for k in range(len(kurve)):
        kand = [i for i in nach_schluessel.get((str(k_sym[k]), int(k_zeit[k])), ())
                if i not in benutzt and abs(pnl[i] - k_pnl[k]) <= TOL_PNL]
        art = "eindeutig"
        if len(kand) > 1:
            kand = [i for i in kand if abs(k_alloc[k] - allocation_pct * kapital_beim_einstieg(ein[i])) <= TOL_GELD]
            art = "durch_kapitalprobe"
        if len(kand) > 1 and len(set(inhalt(i) for i in kand)) == 1:
            kand = [min(kand)]
            art = "inhaltsgleich"
        if len(kand) != 1:
            fehl.append({"kurvenzeile": k, "symbol": str(k_sym[k]), "time": str(pd.Timestamp(int(k_zeit[k]), tz="UTC")),
                         "kandidaten": len(kand)})
            continue
        benutzt.add(kand[0]); paare.append((k, kand[0])); zaehl[art] += 1

    spalten = [s for s in ("symbol", "entry_time", "exit_time", "result", "pnl_pct", "entry_price", "exit_price")
               if s in trades.columns]
    zeilen = [i for _, i in paare]
    pos = trades.iloc[zeilen][spalten].copy().reset_index(drop=True)
    pos.insert(0, "trade_zeile", zeilen)
    pos["allocation"] = [float(k_alloc[k]) for k, _ in paare]
    pos["capital_after"] = [float(k_kap[k]) for k, _ in paare]
    pos["kurvenzeile"] = [k for k, _ in paare]
    # Reihenfolge = Buchungsreihenfolge der Simulation (kurvenzeile). Nach entry_time sortiert waehlt
    # mtm_kern.ereignisreihenfolge bei Gleichstand im Ausstieg mit Nullschritt (pnl_pct 0) die falsche
    # Zeile und die Kette schliesst nicht (Befund TB-162 Bau, rsi2_mean_reversion an der Kopie).
    bericht = {"art": "Rekonstruktion", "regel": REGEL, "toleranz": {"pnl_pct": TOL_PNL, "geld": TOL_GELD},
               "trades_gefunden": n, "kurvenzeilen": int(len(kurve)), "zugeordnet": len(paare),
               "nicht_zuordenbar": len(fehl), "nicht_zuordenbar_zeilen": fehl[:50], **zaehl}
    return pos, bericht
