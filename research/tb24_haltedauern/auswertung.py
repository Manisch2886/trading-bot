"""
Auswertung: Haltedauern, Ueberlappungsmatrix, Einordnung (TB-24)
==============================================================================
Liest die Positionsdateien aus `daten/` (erzeugt von `positionen_holen.py`)
und schreibt alle Tabellen des Berichts nach `ergebnisse/`. Rechnet
ausschliesslich mit den Funktionen aus `haltedauer_kern.py`.

**Liest nur.** Es wird keine Bot-Datei und nichts unter `results/` angefasst.

Nutzung:
    python3 auswertung.py
"""

import itertools
import json
import os

import pandas as pd

import haltedauer_kern as k

_DIR = os.path.dirname(os.path.abspath(__file__))
DATEN_DIR = os.path.join(_DIR, "daten")
ERGEBNIS_DIR = os.path.join(_DIR, "ergebnisse")
os.makedirs(ERGEBNIS_DIR, exist_ok=True)

BOTS = [
    "elliott_wave",
    "t3_supertrend",
    "rsi2_crypto",
    "turtle_soup_crypto",
    "volatility_breakout_crypto",
    "elliott_wave_stocks",
    "rsi2_mean_reversion",
    "turtle_soup_stocks",
    "volatility_breakout",
]

# Zuordnung Bot -> Ertragsquelle. Das ist eine LESART, keine Messung, und
# deshalb hier offen hingeschrieben statt im Text versteckt. Grundlage sind
# die Einstiegsregeln aus Uebergabeprotokoll Abschnitt 3:
#   trend      - handelt die Fortsetzung einer Bewegung (T3-Crossover,
#                Bollinger-Ausbruch)
#   umkehr     - handelt die Rueckkehr zu einem Mittelwert bzw. das
#                Scheitern eines Ausbruchs (RSI-2 unter Schwelle,
#                False-Breakout an Donchian-Extremen)
#   muster     - handelt ein abgeschlossenes Wellenmuster und erwartet die
#                Gegenbewegung. Das ist der Sache nach gegen den vorherigen
#                Trend gerichtet, aber weder ein Mittelwert-Ruecklauf noch
#                eine Ausbruchsfortsetzung; die externe Analyse mit ihrer
#                Zaehlung "vier Trendfolge, vier Mean-Reversion" muss einen
#                der beiden Elliott-Bots anders eingeordnet haben als hier.
#                Die Abweichung ist benannt, nicht aufgeloest.
ERTRAGSQUELLE = {
    "elliott_wave": "muster",
    "t3_supertrend": "trend",
    "rsi2_crypto": "umkehr",
    "turtle_soup_crypto": "umkehr",
    "volatility_breakout_crypto": "trend",
    "elliott_wave_stocks": "muster",
    "rsi2_mean_reversion": "umkehr",
    "turtle_soup_stocks": "umkehr",
    "volatility_breakout": "trend",
}

HIST_KANTEN = [0, 1, 2, 3, 5, 8, 11, 16, 21, 31, 61, 91]


def lade(bot: str, nur_ausgefuehrt: bool = True) -> pd.DataFrame:
    if nur_ausgefuehrt:
        pfad = os.path.join(DATEN_DIR, f"{bot}_positionen.csv")
    else:
        pfad = os.path.join(DATEN_DIR, f"{bot}_alle_trades.csv")
    return pd.read_csv(pfad, parse_dates=["entry_time", "exit_time"])


def lade_meta(bot: str) -> dict:
    with open(os.path.join(DATEN_DIR, f"{bot}_meta.json")) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 1. Haltedauern je Bot
# ---------------------------------------------------------------------------

def tabelle_haltedauern(positionen: dict, meta: dict) -> pd.DataFrame:
    zeilen = []
    for bot in BOTS:
        p = positionen[bot]
        kz = k.kennzahlen(k.haltedauer_tage(p))
        ker = k.kennzahlen(p["kerzen"])
        zeilen.append({
            "bot": bot,
            "anlageklasse": meta[bot]["anlageklasse"],
            "zeitrahmen": meta[bot]["zeitrahmen"],
            "ertragsquelle": ERTRAGSQUELLE[bot],
            "n": kz["n"],
            "tage_min": round(kz["min"], 2),
            "tage_p10": round(kz["p10"], 2),
            "tage_q1": round(kz["q1"], 2),
            "tage_median": round(kz["median"], 2),
            "tage_q3": round(kz["q3"], 2),
            "tage_p90": round(kz["p90"], 2),
            "tage_max": round(kz["max"], 2),
            "tage_mittel": round(kz["mittel"], 2),
            "kerzen_median": round(ker["median"], 1),
            "kerzen_q1": round(ker["q1"], 1),
            "kerzen_q3": round(ker["q3"], 1),
            "horizont_klasse": k.horizont_klasse(kz["median"]),
        })
    return pd.DataFrame(zeilen)


def tabelle_ausstiegsarten(positionen: dict) -> pd.DataFrame:
    zeilen = []
    for bot in BOTS:
        p = positionen[bot]
        gesamt = len(p)
        for art, kz in sorted(k.kennzahlen_je_ausstiegsart(p).items(),
                               key=lambda kv: -kv[1]["n"]):
            zeilen.append({
                "bot": bot, "ausstiegsart": art, "n": kz["n"],
                "anteil_pct": round(100 * kz["n"] / gesamt, 1),
                "tage_p10": round(kz["p10"], 2), "tage_q1": round(kz["q1"], 2),
                "tage_median": round(kz["median"], 2), "tage_q3": round(kz["q3"], 2),
                "tage_p90": round(kz["p90"], 2), "tage_max": round(kz["max"], 2),
            })
    return pd.DataFrame(zeilen)


def tabelle_histogramm(positionen: dict) -> pd.DataFrame:
    spalten = {}
    for bot in BOTS:
        spalten[bot] = k.histogramm(k.haltedauer_tage(positionen[bot]), HIST_KANTEN)
    return pd.DataFrame(spalten)


def tabelle_zweigipfligkeit(positionen: dict) -> pd.DataFrame:
    zeilen = []
    for bot in BOTS:
        z = k.zweigipfligkeit(positionen[bot])
        zeilen.append({
            "bot": bot,
            "ausstiegsarten": len(z["arten"]),
            "zwei_gruppen": z["zwei_gruppen"],
            "verglichen": " / ".join(z.get("vergleich", [])),
            "begruendung": z["begruendung"],
        })
    return pd.DataFrame(zeilen)


def tabelle_limit_vergleich(meta: dict) -> pd.DataFrame:
    """Gegenprobe: haengt der Median an der Positionslimit-Auswahl?

    Gemessen wird derselbe Median einmal ueber die AUSGEFUEHRTEN Positionen
    (das reale Buch) und einmal ueber ALLE gefundenen Trades (also auch die,
    die `simulate_portfolio()` wegen `MAX_CONCURRENT_POSITIONS` oder
    fehlendem freien Kapital uebersprungen hat). Waeren die Zahlen weit
    auseinander, haenge der Befund an einer Kapitalmanagement-Einstellung
    statt an der Ausstiegsregel.
    """
    zeilen = []
    for bot in BOTS:
        ausgefuehrt = lade(bot, nur_ausgefuehrt=True)
        alle = lade(bot, nur_ausgefuehrt=False)
        a = k.kennzahlen(k.haltedauer_tage(ausgefuehrt))
        b = k.kennzahlen(k.haltedauer_tage(alle))
        zeilen.append({
            "bot": bot,
            "n_ausgefuehrt": a["n"], "median_ausgefuehrt": round(a["median"], 2),
            "n_alle": b["n"], "median_alle": round(b["median"], 2),
            "differenz_tage": round(a["median"] - b["median"], 2),
            "uebersprungen": meta[bot]["trades_uebersprungen"],
        })
    return pd.DataFrame(zeilen)


# ---------------------------------------------------------------------------
# 2. Ueberlappung
# ---------------------------------------------------------------------------

def tabelle_ueberlappung(positionen: dict, meta: dict) -> pd.DataFrame:
    zeilen = []
    for a, b in itertools.permutations(BOTS, 2):
        u = k.ueberlappung(positionen[a], positionen[b])
        zeilen.append({
            "bot_a": a, "bot_b": b,
            "gleiche_anlageklasse": meta[a]["anlageklasse"] == meta[b]["anlageklasse"],
            "fenster_von": u["gemeinsames_fenster"][0] if u["gemeinsames_fenster"] else None,
            "fenster_bis": u["gemeinsames_fenster"][1] if u["gemeinsames_fenster"] else None,
            "positionstage_a": u["tage_a"], "positionstage_b": u.get("tage_b"),
            "titeltage_a": u["titeltage_a"],
            "anteil_tage_pct": None if u["anteil_tage"] is None else round(100 * u["anteil_tage"], 1),
            "anteil_titel_pct": None if u["anteil_titel"] is None else round(100 * u["anteil_titel"], 2),
        })
    return pd.DataFrame(zeilen)


def tabelle_naehe(positionen: dict, meta: dict, zufallslaeufe: int = 200) -> pd.DataFrame:
    """Nur Paare derselben Anlageklasse: ueber Anlageklassen hinweg gibt es
    kein gemeinsames Symbol, die Zahl waere per Konstruktion 0."""
    zeilen = []
    for a, b in itertools.permutations(BOTS, 2):
        if meta[a]["anlageklasse"] != meta[b]["anlageklasse"]:
            continue
        n = k.naehe(positionen[a], positionen[b], zufallslaeufe=zufallslaeufe)
        analytisch = k.naehe_erwartet_analytisch(positionen[a], positionen[b])
        zeilen.append({
            "bot_a": a, "bot_b": b,
            "einstiege_a": n["einstiege_a"], "einstiege_b": n["einstiege_b"],
            "gemeinsame_symbole": n["gemeinsame_symbole"],
            "treffer": n["treffer"],
            "anteil_pct": None if n["anteil"] is None else round(100 * n["anteil"], 1),
            "zufall_pct": None if n["anteil_zufall"] is None else round(100 * n["anteil_zufall"], 1),
            "zufall_analytisch_pct": round(100 * analytisch, 1) if analytisch == analytisch else None,
            "ueberschuss": None if n["ueberschuss"] is None else round(n["ueberschuss"], 2),
        })
    return pd.DataFrame(zeilen)


def tabelle_versatz(positionen: dict, meta: dict) -> pd.DataFrame:
    """Verteilung des Versatzes zwischen den Einstiegen zweier Bots im selben
    Titel. Nur Paare derselben Anlageklasse (sonst kein gemeinsames Symbol)."""
    zeilen = []
    for a, b in itertools.permutations(BOTS, 2):
        if meta[a]["anlageklasse"] != meta[b]["anlageklasse"]:
            continue
        v = k.versatz_verteilung(positionen[a], positionen[b])
        if v["n"] == 0:
            continue
        zeile = {
            "bot_a": a, "bot_b": b,
            "einstiege_a": v["einstiege_a"], "mit_b_im_titel": v["n"],
            "median_versatz_tage": round(v["median_versatz"], 1),
            "median_versatz_bis_30_tage": round(v["median_versatz_bis_30_tage"], 1),
            "anteil_bis_3_tage_pct": round(100 * v["anteil_bis_3_tage"], 1),
        }
        zeile.update({f"n[{name}]": anzahl for name, anzahl in v["histogramm"].items()})
        zeile["n[< -30]"] = v["unter_minus_30"]
        zeile["n[>= 30]"] = v["ueber_plus_30"]
        zeilen.append(zeile)
    return pd.DataFrame(zeilen)


# ---------------------------------------------------------------------------
# 3. Einordnung
# ---------------------------------------------------------------------------

def einordnung(haltedauern: pd.DataFrame, ueber: pd.DataFrame, naehe_df: pd.DataFrame,
                versatz: pd.DataFrame) -> dict:
    klassen = {}
    for name, _von, _bis in k.HORIZONT_KLASSEN:
        teil = haltedauern[haltedauern["horizont_klasse"] == name]
        klassen[name] = {
            "bots": list(teil["bot"]),
            "anzahl": int(len(teil)),
            "ertragsquellen": sorted(set(teil["ertragsquelle"])),
        }

    fenster_3_10 = klassen["3 bis 10 Tage"]
    gleiche_klasse = ueber.merge(
        haltedauern[["bot", "horizont_klasse"]].rename(
            columns={"bot": "bot_a", "horizont_klasse": "klasse_a"}), on="bot_a")
    gleiche_klasse = gleiche_klasse.merge(
        haltedauern[["bot", "horizont_klasse"]].rename(
            columns={"bot": "bot_b", "horizont_klasse": "klasse_b"}), on="bot_b")

    return {
        "vermutung": {
            "wortlaut": ("Sechs der neun haben Median-Haltedauern zwischen drei und "
                          "zehn Tagen und bespielen ein Fenster."),
            "bots_im_fenster_3_bis_10": fenster_3_10["bots"],
            "anzahl": fenster_3_10["anzahl"],
            "trifft_zu": fenster_3_10["anzahl"] == 6,
        },
        "horizont_klassen": klassen,
        "median_spanne_tage": [float(haltedauern["tage_median"].min()),
                                float(haltedauern["tage_median"].max())],
        "staerkstes_paar_titeltage": ueber.sort_values("anteil_titel_pct", ascending=False)
            .head(1).to_dict("records"),
        "staerkstes_paar_naehe": naehe_df.sort_values("ueberschuss", ascending=False)
            .head(1).to_dict("records"),
        "schwaechstes_paar_naehe": naehe_df[naehe_df["ueberschuss"].notna()]
            .sort_values("ueberschuss").head(1).to_dict("records"),
        "paare_gleiche_klasse_und_quelle": int(len(gleiche_klasse[
            (gleiche_klasse["klasse_a"] == gleiche_klasse["klasse_b"])
            & (gleiche_klasse["bot_a"].map(ERTRAGSQUELLE)
               == gleiche_klasse["bot_b"].map(ERTRAGSQUELLE))])),
        "groesster_versatz": versatz.reindex(
            versatz["median_versatz_bis_30_tage"].abs().sort_values(ascending=False).index
        ).head(3).to_dict("records"),
    }


def main():
    positionen = {bot: lade(bot) for bot in BOTS}
    meta = {bot: lade_meta(bot) for bot in BOTS}

    haltedauern = tabelle_haltedauern(positionen, meta)
    ausstiegsarten = tabelle_ausstiegsarten(positionen)
    hist = tabelle_histogramm(positionen)
    zwei = tabelle_zweigipfligkeit(positionen)
    limit = tabelle_limit_vergleich(meta)
    print("Ueberlappungsmatrix (72 geordnete Paare) - das dauert etwa eine Minute ...",
          flush=True)
    ueber = tabelle_ueberlappung(positionen, meta)
    naehe_df = tabelle_naehe(positionen, meta)
    versatz = tabelle_versatz(positionen, meta)

    haltedauern.to_csv(os.path.join(ERGEBNIS_DIR, "haltedauern_je_bot.csv"), index=False)
    ausstiegsarten.to_csv(os.path.join(ERGEBNIS_DIR, "haltedauern_je_ausstiegsart.csv"), index=False)
    hist.to_csv(os.path.join(ERGEBNIS_DIR, "haltedauern_histogramm.csv"))
    zwei.to_csv(os.path.join(ERGEBNIS_DIR, "verteilungsform.csv"), index=False)
    limit.to_csv(os.path.join(ERGEBNIS_DIR, "gegenprobe_positionslimit.csv"), index=False)
    ueber.to_csv(os.path.join(ERGEBNIS_DIR, "ueberlappungsmatrix.csv"), index=False)
    naehe_df.to_csv(os.path.join(ERGEBNIS_DIR, "naehe_der_einstiege.csv"), index=False)
    versatz.to_csv(os.path.join(ERGEBNIS_DIR, "versatz_der_einstiege.csv"), index=False)

    zusammenfassung = einordnung(haltedauern, ueber, naehe_df, versatz)
    zusammenfassung["datenbasis"] = {
        bot: {
            "zeitrahmen": meta[bot]["zeitrahmen"],
            "anlageklasse": meta[bot]["anlageklasse"],
            "trades_gefunden": meta[bot]["trades_gefunden"],
            "trades_ausgefuehrt": meta[bot]["trades_ausgefuehrt"],
            "symbole_ausgefuehrt": meta[bot]["symbole_ausgefuehrt"],
            "erster_einstieg": meta[bot]["erster_einstieg"][:10],
            "letzter_ausstieg": meta[bot]["letzter_ausstieg"][:10],
            "abgleich_exposure_messung_identisch":
                meta[bot]["abgleich_exposure_messung"].get("identisch"),
        } for bot in BOTS
    }
    with open(os.path.join(ERGEBNIS_DIR, "zusammenfassung.json"), "w") as f:
        json.dump(zusammenfassung, f, indent=2, ensure_ascii=False)

    print("\n--- Haltedauern (Kalendertage, ausgefuehrte Positionen) ---")
    print(haltedauern[["bot", "zeitrahmen", "n", "tage_p10", "tage_q1", "tage_median",
                        "tage_q3", "tage_p90", "kerzen_median",
                        "horizont_klasse"]].to_string(index=False))
    v = zusammenfassung["vermutung"]
    print(f"\nVermutung '{v['wortlaut']}'")
    print(f"  -> {v['anzahl']} Bots im Fenster 3 bis 10 Tage: {', '.join(v['bots_im_fenster_3_bis_10'])}")
    print(f"  -> trifft_zu = {v['trifft_zu']}")
    print(f"\nMedian-Spanne aller neun Bots: "
          f"{zusammenfassung['median_spanne_tage'][0]:.2f} bis "
          f"{zusammenfassung['median_spanne_tage'][1]:.2f} Kalendertage")
    print(f"\n{len(os.listdir(ERGEBNIS_DIR))} Dateien in ergebnisse/ geschrieben.")


if __name__ == "__main__":
    main()
