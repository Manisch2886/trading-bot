#!/usr/bin/env python3
"""
TB-73 - Die Tabellen aus den neun Messungen (erzeugt, nicht abgetippt)
==============================================================================
    trading-env/bin/python3 research/mtm_drawdown/auswertung.py

Liest ergebnisse/<bot>.json (aus messung.py) und schreibt
ergebnisse/messung.md sowie ergebnisse/zusammenfassung.json. Jede Zahl in
BERICHT.md, die aus der Messung stammt, steht hier zuerst.

Berichtet wird je Falte, nicht nur im Mittel (Fables Warnung, Register 24.3):
2020 und 2022 sind hervorgehoben; der Median ueber die Selektionsfalten steht
NUR neben den Faltenwerten, nie allein (Auftrag, Abschnitt 5).

Was hier NICHT steht: keine Benchmark-Grenze, kein `erlaubt(f)`, kein
"besteht/besteht nicht". Register 24.3 - die Groesse der Abweichung ist fuer
die Entscheidung ohne Belang; sie wird gemessen und berichtet.
"""

import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)
from grundlage import BOTS, ERGEBNISSE  # noqa: E402

HERVORGEHOBEN = ("2020", "2022")   # Falten, die 2020 bzw. 2022 enthalten


def f2(x, einheit=""):
    return "—" if x is None else f"{x:.2f}{einheit}".replace(".", ",")


def f3(x):
    return "—" if x is None else f"{x:.3f}".replace(".", ",")


def hervor(falte: str) -> bool:
    return any(j in falte for j in HERVORGEHOBEN)


def fett(text: str, ja: bool) -> str:
    return f"**{text}**" if ja else text


def lade():
    aus = {}
    for bot in BOTS:
        pfad = os.path.join(ERGEBNISSE, f"{bot}.json")
        if os.path.exists(pfad):
            with open(pfad, encoding="utf-8") as f:
                aus[bot] = json.load(f)
    return aus


def falte_mit_jahr(falten, jahr):
    """Die Falte, die das Jahr enthaelt (bei Zweijahres-Falten '2020-2021')."""
    for z in falten:
        if jahr in z["falte"]:
            return z
    return None


def uebersicht(daten: dict) -> list:
    z = ["| Bot | Selektionsfalten mit Grundlage | Median E | Median M | Median der Differenzen M−E | 2020: E → M | 2022: E → M | M flacher als E (Falten) |",
         "|---|---|---:|---:|---:|---|---|---|"]
    for bot in BOTS:
        d = daten.get(bot)
        if d is None:
            z.append(f"| `{bot}` | **keine Messung** | | | | | | |")
            continue
        ms = d["median_selektion"]
        f20 = falte_mit_jahr(d["falten"], "2020")
        f22 = falte_mit_jahr(d["falten"], "2022")

        def paar(f):
            if f is None:
                return "—"
            if f["grundlage"] == "keine":
                return f"{f['falte']}: keine Grundlage"
            teil = f" (ab {f['liste_ab']})" if f["grundlage"] == "teilweise" else ""
            return f"{f['falte']}{teil}: {f2(f['E'])} → **{f2(f['M'])}** ({f2(f['M_minus_E_pp'])} pp, ×{f3(f['faktor_M_zu_E'])})"

        richtung = d["richtungsprobe"]["faelle_M_flacher_als_E"]
        z.append(f"| `{bot}` | {len(ms['selektionsfalten_mit_grundlage'])} von "
                 f"{sum(1 for f in d['falten'] if f['rolle'] == 'selektion')} | "
                 f"{f2(ms['E'])} | **{f2(ms['M'])}** | {f2(ms['M_minus_E_pp'])} pp | "
                 f"{paar(f20)} | {paar(f22)} | {', '.join(richtung) if richtung else 'keine'} |")
    return z


def bot_tabelle(d: dict) -> list:
    z = [f"### `{d['bot']}` — {d['zeitrahmen']}, {d['anlageklasse']}, {d['positionen']} Positionen "
         f"({d['erster_einstieg'][:10]} … {d['letzter_ausstieg'][:10]})",
         "",
         f"Kosten je Seite {f2(d['kosten']['je_seite_pct'])} % aus `{d['kosten']['modul']}` "
         f"(Abgleich mit der Liste: max {d['kosten']['gegen_liste']['max_abweichung_pp']:.4f} pp, "
         f"{'innerhalb' if d['kosten']['gegen_liste']['innerhalb_rundung'] else 'AUSSERHALB'} der Rundung). "
         f"Raster {d['raster']['tage']} Tage ({d['raster']['von']} … {d['raster']['bis_einschliesslich']}), "
         f"{d['raster']['fortgeschriebene_kurstage']} fortgeschriebene Kurstage. "
         f"Gesamter Zeitraum: E {f2(d['gesamt']['E_calculate_max_drawdown'])} % "
         f"(`calculate_max_drawdown`), E_tag {f2(d['gesamt']['E_tag'])} %, M {f2(d['gesamt']['M'])} %. "
         f"Laufzeit {d['laufzeit_s']} s.",
         "",
         "| Falte | Rolle | Grundlage | Exposure Ø | E | E_tag | **M** | M − E | Faktor M/E | offen am Faltenbeginn | Ausstiege | Richtung |",
         "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for f in d["falten"]:
        h = hervor(f["falte"])
        name = fett(f["falte"], h)
        if f["grundlage"] == "keine":
            z.append(f"| {name} | {f['rolle']} | **keine** | — | — | — | — | — | — | — | 0 | — |")
            continue
        grund = "vollständig" if f["grundlage"] == "vollstaendig" else f"teilweise, Liste ab {f['liste_ab']}"
        richtung = ("⚠️ M flacher als E" if f["M_flacher_als_E"] else
                    ("M flacher als E_tag" if f["M_flacher_als_E_tag"] else "M ≤ E"))
        z.append(f"| {name} | {f['rolle']} | {grund} | {f3(f['exposure_mittel'])} | "
                 f"{fett(f2(f['E']), h)} | {f2(f['E_tag'])} | **{f2(f['M'])}** | "
                 f"{fett(f2(f['M_minus_E_pp']) + ' pp', h)} | {f3(f['faktor_M_zu_E'])} | "
                 f"{f['offen_am_faltenbeginn']} | {f['n_ausstiege']} | {richtung} |")
    ms = d["median_selektion"]
    z.append(f"| *Median über die Selektionsfalten mit Grundlage ({len(ms['selektionsfalten_mit_grundlage'])}); letzte Spalte: Median der Differenzen* | | | | "
             f"*{f2(ms['E'])}* | *{f2(ms['E_tag'])}* | ***{f2(ms['M'])}*** | *{f2(ms['M_minus_E_pp'])} pp* | | | | |")
    z.append("")
    return z


def richtungsprobe(daten: dict) -> list:
    z = ["| Bot | Falte | Rolle | E | E_tag | M | M − E | Mechanismus (gemessen) |",
         "|---|---|---|---:|---:|---:|---:|---|"]
    n = 0
    for bot in BOTS:
        d = daten.get(bot)
        if d is None:
            continue
        for f in d["falten"]:
            if f["M_flacher_als_E"]:
                n += 1
                if f["E"] < f["E_tag"] - 1e-9 and f["M"] <= f["E_tag"] + 1e-9:
                    mech = "Raster: E tiefer als E_tag, M nicht flacher als E_tag (Probe 1b)"
                elif f["M"] > f["E_tag"] + 1e-9:
                    mech = "Bewertung: M flacher als E_tag (Probe 3 — unrealisierter Gewinn hebt Hoch- und Tiefpunkt)"
                else:
                    mech = "?"
                z.append(f"| `{bot}` | {f['falte']} | {f['rolle']} | {f2(f['E'])} | {f2(f['E_tag'])} | "
                         f"{f2(f['M'])} | {f2(f['M_minus_E_pp'])} pp | {mech} |")
    if n == 0:
        z.append("| *keine* | | | | | | | |")
    return z


def laufzeiten(daten: dict) -> list:
    z = ["| Bot | Positionen | Rastertage | Laufzeit `messung.py` |", "|---|---:|---:|---:|"]
    for bot in BOTS:
        d = daten.get(bot)
        if d is None:
            z.append(f"| `{bot}` | — | — | keine Messung |")
        else:
            z.append(f"| `{bot}` | {d['positionen']} | {d['raster']['tage']} | {d['laufzeit_s']} s |")
    return z


def main():
    daten = lade()
    if not daten:
        raise SystemExit("keine Messungen unter ergebnisse/ gefunden")
    zeilen = ["# TB-73 — E gegen M, je Bot und je Falte (erzeugt von `auswertung.py`)",
              "",
              "E = ereignisindizierter Drawdown (`capital_after` je Ausstieg, `shared/messkette.py`), "
              "E_tag = dieselbe Kurve am Tagesende (Erklärungshilfe), "
              "M = täglicher Mark-to-Market-Drawdown (offene Positionen zum Tagesschluss). "
              "Alle Werte in Prozent, negativ; M − E in Prozentpunkten (negativ = M tiefer). "
              "Falten aus `research/vorregistrierung/ergebnisse/faltenplan_tb72.json`. "
              "**Fett: die Falten mit 2020 und 2022.** Kein Wert steht ohne die Faltenwerte daneben; "
              "keine Grenze, kein Vergleich mit dem Benchmark (Register 24.3).",
              "",
              "## Übersicht",
              ""] + uebersicht(daten) + ["", "## Je Bot", ""]
    for bot in BOTS:
        if bot in daten:
            zeilen += bot_tabelle(daten[bot])
    zeilen += ["## Richtungsprobe — Falten, in denen M flacher ist als E", ""] + richtungsprobe(daten)
    zeilen += ["", "## Laufzeiten", ""] + laufzeiten(daten)

    pfad = os.path.join(ERGEBNISSE, "messung.md")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write("\n".join(zeilen) + "\n")

    zusammen = {bot: {
        "median_selektion": d["median_selektion"],
        "falten": {f["falte"]: {k: f[k] for k in ("rolle", "grundlage", "E", "E_tag", "M", "M_minus_E_pp",
                                                "faktor_M_zu_E", "exposure_mittel", "M_flacher_als_E")}
                   for f in d["falten"]},
        "richtungsprobe": d["richtungsprobe"],
        "laufzeit_s": d["laufzeit_s"],
    } for bot, d in daten.items()}
    with open(os.path.join(ERGEBNISSE, "zusammenfassung.json"), "w", encoding="utf-8") as f:
        json.dump(zusammen, f, indent=1, ensure_ascii=False)
    print(f"{len(daten)} Bots ausgewertet -> {os.path.relpath(pfad)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
