"""
Rechenkern der MtM-Messung - reine Funktionen, ohne Dateizugriff (TB-73)
==============================================================================
Zwei Bewertungen DESSELBEN Kapitalpfads, je Falte:

  E  ereignisindiziert - der heutige Weg. Die Kurve bewegt sich nur an den
     Ausstiegen (`capital_after` aus `shared/zuteilung.py::simuliere_portfolio`);
     offene Positionen stehen zum Einstandswert im Buch. Der Drawdown darauf
     ist `shared/messkette.py::max_drawdown_ungerundet` - importiert, nicht
     nachgebaut.

  M  Mark-to-Market, taeglich - was Registertext 1a verlangt (Register 24.2).
     An JEDEM Handelstag des Rasters wird das Kapital bewertet: offene
     Positionen zum Tagesschlusskurs, Tage ohne Position tragen 0. Die
     Ausstiege selbst gehen mit dem realisierten Ergebnis ein (`pnl_pct` der
     Trade-Liste, das die Kosten schon traegt) - der Stop-Kurs eines
     Stop-Loss ist nicht der Tagesschluss, und die Bewertung soll den
     Ereignispfad an den Ausstiegen nicht verfaelschen.

  E_tag  dazwischen, als Erklaerungshilfe: die Ereigniskurve auf dem
     Tagesraster (Buchwert am Tagesende, offene Positionen zum Einstand).
     E gegen E_tag ist der reine Raster-Effekt (mehrere Ausstiege an einem
     Tag, Reihenfolge der Ausstiege bei gleichem Zeitstempel - die
     `zuteilung.py` per gesaetem Zufall festlegt); E_tag gegen M der reine
     Bewertungs-Effekt (unrealisierter Gewinn und Verlust). Beide zusammen
     sind E gegen M.

DIE TAGESGRENZE
------------------------------------------------------------------------------
Zeitstempel der Trade-Listen sind `open_time` der Ein- bzw. Ausstiegskerze
(Tagesbots: das Datum; 1h/4h-Bots: Kerzenbeginn). Der Tagesschluss des Tages
`d` ist der Schluss der 1d-Kerze mit `open_time = d`. Eine Position ist am
Tagesschluss `d` offen, wenn

    entry_time < d + 1 Tag   und   exit_time >= d + 1 Tag

- eingestiegen vor Tagesende, ausgestiegen in einer Kerze, die an oder nach
dem Tagesende beginnt. Eine Position, die am Tag `d` ein- UND aussteigt, ist
an keinem Tagesschluss offen und geht nur realisiert ein - das ist Probe 1.

DIE KOSTEN
------------------------------------------------------------------------------
Im Original zieht der Backtest `2 x (TRADING_FEE_PCT + SLIPPAGE_PCT)` beim
Ausstieg von `pnl_pct` ab. Die Bewertung zeigt eine offene Position so, wie
das Konto sie zeigt: Einstiegsseite (eine Seite Gebuehr + Slippage) ab dem
Einstiegstag abgezogen, Ausstiegsseite erst beim Ausstieg. Die Zahl je Seite
kommt als Argument `kosten_seite_pct` herein - der Aufrufer importiert sie aus
dem Backtest-Modul des Bots, hier steht keine Kopie.

WAS DIESER KERN NICHT TUT
------------------------------------------------------------------------------
* Er zuteilt nichts. Welche Trades Kapital bekamen, steht in der Trade-Liste
  (TB-24, aus `simuliere_portfolio` mit der Kaskade). E und M rechnen auf
  DENSELBEN ausgefuehrten Positionen.
* Er liest und schreibt keine Datei.
* Er vergleicht mit nichts - keine Benchmark-Grenze, kein `erlaubt(f)`.
  Register 24.3: die Groesse der Abweichung ist fuer die Entscheidung ohne
  Belang; sie wird gemessen und berichtet.
"""

import numpy as np
import pandas as pd

EIN_TAG = pd.Timedelta(days=1)

# Toleranz beim Schliessen der Kapitalkette: `capital_after` und `allocation`
# stehen in der Trade-Liste auf zwei Nachkommastellen gerundet, das Kapital
# lief in `simuliere_portfolio` ungerundet weiter. Ein Schritt kann sich
# deshalb um bis zu 0,005 (Rundung des Kapitals) plus 0,005 x |pnl_pct|/100
# (Rundung der Allokation) verschieben; 0,02 laesst dafuer Luft und faengt
# jede echte Vertauschung (Betraege im Bereich von Euro, nicht Cent).
KETTEN_TOLERANZ = 0.02


# ---------------------------------------------------------------------------
# Die Ereigniskurve: Reihenfolge der Ausstiege aus der Kapitalkette
# ---------------------------------------------------------------------------

def ereignisreihenfolge(positionen: pd.DataFrame, startkapital: float) -> pd.DataFrame:
    """Die ausgefuehrten Positionen in der Reihenfolge, in der
    `simuliere_portfolio` ihre Ausstiege verbucht hat.

    Die TB-24-Liste ist nach `entry_time` sortiert; die Kurvenreihenfolge ist
    die nach `exit_time`, und bei gleichem Zeitstempel die aus
    `zuteilung.Zuteiler.ausstiegsreihenfolge` (gesaeter Zufall). Die ist in
    der Liste nicht vermerkt - aber die Kette

        capital_after[k] = capital_after[k-1] + allocation[k] * pnl_pct[k] / 100

    laesst sie rekonstruieren: innerhalb eines Zeitstempels wird jeweils die
    Position genommen, deren Schritt an den bisherigen Stand anschliesst.
    Sind zwei Schritte gleich gross, ist die Wahl fuer die Kurve bedeutungslos.
    Schliesst die Kette nicht, ist die Liste nicht die einer Kapitalsimulation
    - dann ValueError, nicht raten.
    """
    pos = positionen.copy()
    pos["entry_time"] = pd.to_datetime(pos["entry_time"])
    pos["exit_time"] = pd.to_datetime(pos["exit_time"])
    pos = pos.sort_values("exit_time", kind="stable").reset_index(drop=True)

    reihenfolge = []
    kapital = float(startkapital)
    for _, gruppe in pos.groupby("exit_time", sort=True):
        rest = list(gruppe.index)
        while rest:
            treffer = None
            for i in rest:
                schritt = pos.at[i, "allocation"] * pos.at[i, "pnl_pct"] / 100.0
                if abs(kapital + schritt - pos.at[i, "capital_after"]) <= KETTEN_TOLERANZ:
                    treffer = i
                    break
            if treffer is None:
                raise ValueError(
                    f"Kapitalkette schliesst nicht bei exit_time "
                    f"{gruppe['exit_time'].iloc[0]}: Stand {kapital:.2f}, "
                    f"Kandidaten {[round(pos.at[i, 'capital_after'], 2) for i in rest]}")
            rest.remove(treffer)
            reihenfolge.append(treffer)
            kapital = float(pos.at[treffer, "capital_after"])
    return pos.loc[reihenfolge].reset_index(drop=True)


def ereigniskurve(ereignisse: pd.DataFrame) -> pd.Series:
    """`capital_after` je Ausstieg, indiziert mit `exit_time` (Duplikate
    erlaubt), in Kurvenreihenfolge - das Objekt, auf dem
    `calculate_max_drawdown` heute rechnet."""
    return pd.Series(ereignisse["capital_after"].to_numpy(dtype=float),
                     index=pd.DatetimeIndex(ereignisse["exit_time"]), name="capital_after")


# ---------------------------------------------------------------------------
# Das Tagesraster und die Schlusskurse darauf
# ---------------------------------------------------------------------------

def tagesraster(schlusskurse: dict, von=None, bis=None) -> pd.DatetimeIndex:
    """Vereinigung der Kurstage aller Symbole (normalisiert auf das Datum) -
    bei Krypto jeder Kalendertag, bei Aktien die Boersentage. Dieselben Tage,
    auf denen `research/vorregistrierung/benchmark.py` den Benchmark bewertet
    (Registertext 3b (c)): die 1d-Kursdateien in data/."""
    tage = pd.DatetimeIndex([])
    for reihe in schlusskurse.values():
        tage = tage.union(pd.DatetimeIndex(reihe.index).normalize())
    tage = tage.sort_values()
    if von is not None:
        tage = tage[tage >= pd.Timestamp(von)]
    if bis is not None:
        tage = tage[tage < pd.Timestamp(bis)]
    return tage


def kurse_auf_raster(schlusskurse: dict, tage: pd.DatetimeIndex):
    """Schlusskurs je Symbol auf dem Raster, fehlende Tage fortgeschrieben.

    Liefert (kurse: DataFrame Tage x Symbole, fortgeschrieben: DataFrame bool
    derselben Form - True, wo kein eigener Kurs des Tages vorlag und der
    letzte bekannte genommen wurde). Vor dem ersten Kurs eines Symbols bleibt
    NaN; eine Position dort ist ein Datenfehler und wird gemeldet, nicht
    geraten (`mtm_pfad` bricht ab).
    """
    spalten = {}
    fort = {}
    for symbol, reihe in schlusskurse.items():
        r = pd.Series(reihe.to_numpy(dtype=float),
                      index=pd.DatetimeIndex(reihe.index).normalize())
        r = r[~r.index.duplicated(keep="last")].sort_index()
        eigene = r.reindex(tage)
        spalten[symbol] = eigene.ffill()
        fort[symbol] = eigene.isna() & spalten[symbol].notna()
    return pd.DataFrame(spalten, index=tage), pd.DataFrame(fort, index=tage)


# ---------------------------------------------------------------------------
# Der taegliche Mark-to-Market-Pfad
# ---------------------------------------------------------------------------

def mtm_pfad(ereignisse: pd.DataFrame, kurse: pd.DataFrame, fortgeschrieben: pd.DataFrame,
             startkapital: float, kosten_seite_pct: float) -> pd.DataFrame:
    """Tagesreihe des Kapitals in drei Lesarten, auf dem Raster von `kurse`.

    Spalten:
      buch        E_tag - Buchwert am Tagesende: `capital_after` des letzten
                  Ausstiegs mit exit_time < d + 1 Tag, davor `startkapital`.
                  Offene Positionen stehen darin zum Einstand.
      mtm         M - buch + Summe ueber die am Tagesschluss offenen
                  Positionen von
                      allocation * (close_d / entry_price - 1 - kosten_seite_pct/100)
      n_offen     Anzahl am Tagesschluss offener Positionen
      gebunden    Summe ihrer Allokationen (Einstand)
      unrealisiert  mtm - buch
      fortgeschrieben  Anzahl offener Positionen, deren Kurs an diesem Tag
                  fortgeschrieben ist (kein eigener Tagesschluss des Symbols)

    `ereignisse` ist die Rueckgabe von `ereignisreihenfolge` (Spalten
    entry_time, exit_time, symbol, entry_price, allocation, capital_after).
    """
    tage = kurse.index
    if not tage.is_monotonic_increasing or tage.has_duplicates:
        raise ValueError("Raster muss aufsteigend und duplikatfrei sein")
    n = len(tage)
    tagesende = (tage + EIN_TAG).to_numpy()

    exit_np = pd.to_datetime(ereignisse["exit_time"]).to_numpy()
    entry_np = pd.to_datetime(ereignisse["entry_time"]).to_numpy()
    if not (np.diff(exit_np) >= np.timedelta64(0)).all():
        raise ValueError("Ereignisse muessen in Kurvenreihenfolge (exit_time aufsteigend) sein")

    # E_tag: letzter Ausstieg mit exit_time < tagesende
    k = np.searchsorted(exit_np, tagesende, side="left")  # Anzahl Ausstiege vor Tagesende
    kapital_after = ereignisse["capital_after"].to_numpy(dtype=float)
    buch = np.where(k > 0, kapital_after[np.maximum(k - 1, 0)], float(startkapital))

    # M: offene Positionen je Tag. Offen am Schluss d <=> entry < d+1 <= exit.
    # Erster offener Tag: kleinstes d mit entry < d+1  -> d >= entry - 1 Tag
    #   -> Index = searchsorted(tage, entry - 1 Tag, 'right')... genauer ueber
    #   tagesende: erster Index i mit tagesende[i] > entry.
    # Letzter offener Tag: groesstes d mit d+1 <= exit -> letzter i mit
    #   tagesende[i] <= exit -> Index = searchsorted(tagesende, exit, 'right') - 1.
    erster = np.searchsorted(tagesende, entry_np, side="right")
    letzter = np.searchsorted(tagesende, exit_np, side="right") - 1

    unreal = np.zeros(n)
    n_offen = np.zeros(n, dtype=int)
    gebunden = np.zeros(n)
    fort_zaehler = np.zeros(n, dtype=int)
    faktor_kosten = 1.0 + kosten_seite_pct / 100.0

    symbole = ereignisse["symbol"].astype(str).to_numpy()
    allokation = ereignisse["allocation"].to_numpy(dtype=float)
    einstand = ereignisse["entry_price"].to_numpy(dtype=float)
    kurs_np = {s: kurse[s].to_numpy(dtype=float) for s in kurse.columns}
    fort_np = {s: fortgeschrieben[s].to_numpy() for s in fortgeschrieben.columns}

    for i in range(len(ereignisse)):
        a, b = int(erster[i]), int(letzter[i])
        if b < a:
            continue  # kein Tagesschluss zwischen Einstieg und Ausstieg
        s = symbole[i]
        if s not in kurs_np:
            raise ValueError(f"Kein Kurs fuer {s}")
        schluss = kurs_np[s][a:b + 1]
        if np.isnan(schluss).any():
            raise ValueError(f"{s}: Kurs fehlt zwischen {tage[a].date()} und {tage[b].date()} "
                             f"(Position {i}, Einstieg {pd.Timestamp(entry_np[i])})")
        unreal[a:b + 1] += allokation[i] * (schluss / einstand[i] - faktor_kosten)
        n_offen[a:b + 1] += 1
        gebunden[a:b + 1] += allokation[i]
        fort_zaehler[a:b + 1] += fort_np[s][a:b + 1].astype(int)

    return pd.DataFrame({
        "buch": buch,
        "mtm": buch + unreal,
        "n_offen": n_offen,
        "gebunden": gebunden,
        "unrealisiert": unreal,
        "fortgeschrieben": fort_zaehler,
    }, index=tage)


# ---------------------------------------------------------------------------
# Drawdown je Falte - mit der importierten Rechnung aus shared/messkette.py
# ---------------------------------------------------------------------------

def drawdown_falte(reihe: pd.Series, basis: float, max_drawdown_ungerundet) -> float:
    """Drawdown einer Reihe innerhalb einer Falte, ausgehend vom Stand
    `basis` am Faltenbeginn - gerechnet mit
    `shared/messkette.py::max_drawdown_ungerundet(kapital_nach_trade,
    startkapital)`, das die Basis der Reihe voranstellt; gerundet auf zwei
    Stellen wie `calculate_max_drawdown`. Leere Reihe: 0.0 (wie dort)."""
    if len(reihe) == 0:
        return 0.0
    return round(float(max_drawdown_ungerundet(pd.Series(reihe.to_numpy(dtype=float)),
                                               float(basis))), 2)


def messe_falten(ereignis: pd.Series, pfad: pd.DataFrame, falten, startkapital: float,
                 max_drawdown_ungerundet) -> list:
    """E, E_tag und M je Falte.

    `falten`: Liste von dicts mit `name`, `von`, `bis_ausschliesslich`,
    `rolle` (Form von research/vorregistrierung/ergebnisse/faltenplan_*.json).

    Basis am Faltenbeginn: fuer E der `capital_after` des letzten Ausstiegs vor
    `von` (sonst startkapital); fuer E_tag und M der jeweilige Wert am letzten
    Rastertag vor `von` (sonst startkapital). Innerhalb der Falte zaehlen fuer
    E die Ausstiege mit von <= exit_time < bis, fuer E_tag und M die Rastertage
    mit von <= d < bis.
    """
    aus = []
    for f in falten:
        von = pd.Timestamp(f["von"])
        bis = pd.Timestamp(f["bis_ausschliesslich"])

        davor = ereignis[ereignis.index < von]
        basis_e = float(davor.iloc[-1]) if len(davor) else float(startkapital)
        in_e = ereignis[(ereignis.index >= von) & (ereignis.index < bis)]

        pfad_davor = pfad[pfad.index < von]
        tage_in = pfad[(pfad.index >= von) & (pfad.index < bis)]
        basis_buch = float(pfad_davor["buch"].iloc[-1]) if len(pfad_davor) else float(startkapital)
        basis_mtm = float(pfad_davor["mtm"].iloc[-1]) if len(pfad_davor) else float(startkapital)

        e = drawdown_falte(in_e, basis_e, max_drawdown_ungerundet)
        e_tag = drawdown_falte(tage_in["buch"], basis_buch, max_drawdown_ungerundet)
        m = drawdown_falte(tage_in["mtm"], basis_mtm, max_drawdown_ungerundet)

        aus.append({
            "falte": f["name"],
            "rolle": f.get("rolle"),
            "von": str(von.date()),
            "bis_ausschliesslich": str(bis.date()),
            "E": e,
            "E_tag": e_tag,
            "M": m,
            "M_minus_E_pp": round(m - e, 2),
            "faktor_M_zu_E": (round(m / e, 3) if abs(e) > 1e-9 else None),
            "M_flacher_als_E": bool(m > e + 1e-9),
            "M_flacher_als_E_tag": bool(m > e_tag + 1e-9),
            "n_ausstiege": int(len(in_e)),
            "n_rastertage": int(len(tage_in)),
            "n_tage_mit_position": int((tage_in["n_offen"] > 0).sum()),
            "offen_am_faltenbeginn": int(pfad_davor["n_offen"].iloc[-1]) if len(pfad_davor) else 0,
            "max_unrealisiert_minus": (round(float(tage_in["unrealisiert"].min()), 2)
                                       if len(tage_in) else 0.0),
            "fortgeschriebene_kurse": int(tage_in["fortgeschrieben"].sum()),
            "basis_E": round(basis_e, 2),
            "basis_M": round(basis_mtm, 2),
        })
    return aus


def median_selektion(messungen: list, schluessel: str):
    """Median einer Groesse ueber die Selektionsfalten, die eine Grundlage
    haben (`grundlage` != 'keine'). Ohne solche Falten None."""
    werte = [m[schluessel] for m in messungen
             if m.get("rolle") == "selektion" and m.get("grundlage") != "keine"
             and m.get(schluessel) is not None]
    if not werte:
        return None
    return round(float(np.median(werte)), 2)
