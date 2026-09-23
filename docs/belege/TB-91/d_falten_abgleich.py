#!/usr/bin/env python3
"""TB-91 Block D (Kopie von TB-90 Block C) - Faltenmenge je Bot in den Benchmark-Tabellen gegen den
gerechneten Plan (33.2 plus Bestaetigungsperiode 35.1). NUR LESEND.

Nach dem Muster von docs/belege/TB-88/m5_falten_abgleich.py. Der Plan wird
nur im Speicher gerechnet (faltenplan.faltenplan(), nie main()); die Tabellen
werden nur gelesen. Je Bot und Tabelle zwei Vergleiche:
  alle   - Faltennamen des Plans (Selektion + Bestaetigung) gegen die
           Schluessel von tabelle[bot]["falten"]
  sel    - nur die Selektionsfalten gegen die Tabellenfalten mit rolle
           "selektion"
Einstufung aus Sicht der TABELLE: gleich / Uebermenge (Tabelle hat mehr) /
Teilmenge (Tabelle hat weniger) / verschieden (beides).
"""
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
VR = os.path.join(REPO, "research", "vorregistrierung")
sys.path.insert(0, VR)

import faltenplan as fp  # noqa: E402

# TB-91: nur die Neurechnung (Kopie von docs/belege/TB-90/c_falten_abgleich.py, sonst unveraendert)
TABELLEN = ("benchmark_drawdowns_2026-09-23_nach_wegA.json",)


def einstufung(tab, plan):
    tab, plan = set(tab), set(plan)
    if tab == plan:
        return "gleich"
    if tab > plan:
        return "Uebermenge"
    if tab < plan:
        return "Teilmenge"
    return "verschieden"


plan = fp.faltenplan()
tab = {}
for q in TABELLEN:
    with open(os.path.join(VR, "ergebnisse", q), encoding="utf-8") as f:
        tab[q] = json.load(f)

print("| Bot | Tabelle | alle: Einstufung | fehlt in Tabelle | nur in Tabelle "
      "| sel: Einstufung | Bestaetigung Plan | Bestaetigung Tabelle |")
print("|---|---|---|---|---|---|---|---|")
for bot, p in plan.items():
    namen = [f["name"] for f in p["falten"]]
    sel = list(p["selektionsfalten"])
    for q in TABELLEN:
        tf = tab[q][bot]["falten"]
        t_sel = [n for n, v in tf.items() if v.get("rolle") == "selektion"]
        t_best = [n for n, v in tf.items() if v.get("rolle") == "bestaetigung"]
        fehlt = [n for n in namen if n not in tf]
        extra = [n for n in tf if n not in namen]
        print("| `%s` | `%s` | %s | %s | %s | %s | `%s` | %s |" % (
            bot, q.replace("benchmark_drawdowns", "bd"),
            einstufung(tf, namen), ", ".join(fehlt) or "-",
            ", ".join(extra) or "-", einstufung(t_sel, sel),
            p["bestaetigungsperiode"],
            ", ".join("`%s`" % n for n in t_best) or "-"))
