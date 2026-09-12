"""
Die eine Tabelle: kippt die Rangfolge, und bei welchem Bot?
====================================================================
Aufruf:  python3 uebersicht.py

Liest alle results/*_ergebnis.json, die analyse.py erzeugt hat, und
baut daraus die Uebersicht fuer den Bericht. Rechnet selbst nichts nach
- es fasst nur zusammen. Braucht keine Bot-Umgebung und laeuft deshalb
in einem einzigen Prozess ueber alle Bots.

Die Tabellen sind Markdown und lassen sich direkt in den Bericht kopieren.
"""

import glob
import json
import os

DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(DIR, "results")

# Die aktuell live genutzte Kombination je Bot, in der Sprache des
# jeweiligen Rasters (Quelle: strategies/<bot>/live_params.py).
LIVE_LABEL = {
    "elliott_wave": "dev 10.0 % / Stop 6.0 % / Fib 0.618",
    "elliott_wave_stocks": "dev 5.0 % / Stop 3.0 % / kein Ziel",
    "t3_supertrend": "T3 16/30 / ADX 20.0 / Stop 4.0 %",
    "rsi2_crypto": "SMA 150 / RSI 10.0 / Stop kein Stop",
    "rsi2_mean_reversion": "RSI 5.0 / Stop kein Stop",
    "turtle_soup_crypto": "Donchian 10 / Stop structural",
    "turtle_soup_stocks": "Donchian 10 / Stop kein Stop",
    "volatility_breakout": "Stop 8.0",
    "volatility_breakout_crypto": "Stop 5.0",
}

REIHENFOLGE = ["elliott_wave", "t3_supertrend", "rsi2_crypto", "turtle_soup_crypto",
               "volatility_breakout_crypto", "elliott_wave_stocks",
               "rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout"]


def laden() -> list:
    out = []
    for pfad in sorted(glob.glob(os.path.join(RESULTS, "*_ergebnis.json"))):
        with open(pfad) as f:
            out.append((os.path.basename(pfad)[:-len("_ergebnis.json")], json.load(f)))

    def schluessel(eintrag):
        name, j = eintrag
        bot = j["bot"]
        return (REIHENFOLGE.index(bot) if bot in REIHENFOLGE else 99,
                1 if j.get("ohne_regimefilter") else 0,
                0 if j.get("fenster", "gesamt") == "gesamt" else 1,
                name)
    return sorted(out, key=schluessel)


def rang_von(j, label, order):
    for r in j.get("rangwechsel", []):
        if r["label"] == label:
            return r.get(f"rang_{order}")
    return None


def main():
    eintraege = laden()
    kopf = ("Bot / Fenster", "Kombis", "Sieger Block-Mass", "Sieger chronologisch",
            "kippt?", "Block-Sieger stabil")
    zeilen = []
    for name, j in eintraege:
        fenster = j.get("fenster", "gesamt")
        if j.get("ohne_regimefilter"):
            fenster += " (vor Regimefilter)"
        zeilen.append((
            f"{j['bot']} / {fenster}",
            str(j["num_besteht_mindestfilter"]) + f" von {j['kombinationen']}",
            str(j["sieger"]["block"]),
            str(j["sieger"]["entry"]),
            {None: "entfaellt", True: "nein", False: "JA"}[
                j["urteil"]["sieger_identisch"]],
            f"{j['urteil'].get('block_sieger_stabil_pct')} %",
        ))

    breiten = [max(len(str(z[i])) for z in ([kopf] + zeilen)) for i in range(len(kopf))]
    trenn = "|" + "|".join("-" * (b + 2) for b in breiten) + "|"
    def zeile(z):
        return "| " + " | ".join(str(z[i]).ljust(breiten[i]) for i in range(len(z))) + " |"
    print("\n## Sieger je Mass\n")
    print(zeile(kopf))
    print(trenn)
    for z in zeilen:
        print(zeile(z))

    print("\n## Die Live-Kombination in beiden Rangfolgen\n")
    k2 = ("Bot / Fenster", "Live-Kombination", "Rang Block", "Rang chrono", "Rang exit")
    z2 = []
    for name, j in eintraege:
        lab = LIVE_LABEL.get(j["bot"])
        fenster = j.get("fenster", "gesamt")
        if j.get("ohne_regimefilter"):
            fenster += " (vor Regimefilter)"
        rb, re_, rx = (rang_von(j, lab, "block"), rang_von(j, lab, "entry"),
                       rang_von(j, lab, "exit"))
        n = j["num_besteht_mindestfilter"]
        z2.append((f"{j['bot']} / {fenster}", lab,
                   f"{rb} von {n}" if rb else "nicht im Raster",
                   f"{re_} von {n}" if re_ else "-",
                   f"{rx} von {n}" if rx else "-"))
    breiten = [max(len(str(z[i])) for z in ([k2] + z2)) for i in range(len(k2))]
    trenn = "|" + "|".join("-" * (b + 2) for b in breiten) + "|"
    print("| " + " | ".join(str(k2[i]).ljust(breiten[i]) for i in range(len(k2))) + " |")
    print(trenn)
    for z in z2:
        print("| " + " | ".join(str(z[i]).ljust(breiten[i]) for i in range(len(z))) + " |")

    print("\n## Groessenordnung des Unterschieds (Sieger je Fenster)\n")
    for name, j in eintraege:
        s = j.get("streuung", [])
        if not s:
            continue
        # die Zeile des Block-Siegers
        z = next((x for x in s if x["label"] == j["sieger"]["block"]), s[0])
        print(f"{j['bot']} / {j.get('fenster', 'gesamt')}"
              f"{' (vor Regimefilter)' if j.get('ohne_regimefilter') else ''}: "
              f"{z['label']}")
        print(f"    DD Block {z['dd_block']:>10}  chronologisch {z['dd_entry']:>10}  "
              f"exit {z['dd_exit']:>10}   Faktor {z['faktor_entry_zu_block']}")
        pb, pt = z["perm_block_dd"], z["perm_tie_dd"]
        print(f"    Streuung ueber {pb.get('n')} Blockreihenfolgen: "
              f"{pb.get('min')} .. {pb.get('max')} ({pb.get('spanne_pp')} pp)")
        print(f"    Streuung ueber {pt.get('n')} Vertauschungen gleichzeitiger "
              f"Einstiege: {pt.get('min')} .. {pt.get('max')} ({pt.get('spanne_pp')} pp)")
        print(f"    chronologischer Wert liegt in der Block-Spanne: "
              f"{'ja' if z['dd_entry_in_block_spanne'] else 'NEIN'}")
        print()


if __name__ == "__main__":
    main()
