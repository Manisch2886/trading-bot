#!/usr/bin/env python3
"""TB-88 M2 - Ist der Bezeichner der Bestaetigungsperiode ein Schluessel?

Probe NUR IM SPEICHER. faltenplan.py wird nicht geaendert, nicht als Skript
aufgerufen (main() wird nie beruehrt), in ergebnisse/ wird nichts geschrieben.

Ablauf, wie test_vorregistrierung.lauf(), mit einem einzigen Unterschied:
  1. Beispieldaten mit dem UNVERAENDERTEN Plan erzeugen (Spalte `falte`
     traegt den Faltennamen) - in ein Wegwerf-Verzeichnis.
  2. aw.ein_bot einmal mit dem unveraenderten Plan (Kontrolle) und einmal
     mit einer tiefen Kopie, in der NUR plan[BOT]["bestaetigungsperiode"]
     auf eine Spanne gesetzt ist - die Lage nach einer Aenderung von
     faltenplan.py:338 allein.
"""

import copy
import json
import os
import sys
import tempfile
import traceback

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
VR = os.path.join(REPO, "research", "vorregistrierung")
sys.path.insert(0, VR)

import auswertung as aw          # noqa: E402
import beispieldaten as bd       # noqa: E402
import faltenplan as fp          # noqa: E402
import registerdaten as rd       # noqa: E402

BOT = "turtle_soup_stocks"       # derselbe Bot wie test_vorregistrierung.py
SPANNE = "2026-01-01/2026-09-01"

mess = rd._mess()
plan = fp.faltenplan(mess)


def lies(name):
    with open(os.path.join(VR, "ergebnisse", name), encoding="utf-8") as f:
        return json.load(f)


# Zwei Tabellenquellen, beide nur gelesen: die heute registrierte Datei (die
# test_vorregistrierung.py liest) und _vt.json (die Punkt 8 eintragen wuerde).
# Nachtrag nach dem ersten Lauf: mit der registrierten Datei scheitert schon
# die Kontrolle in zulaessigkeit() - die Probe braucht deshalb beide.
QUELLEN = ["benchmark_drawdowns.json", "benchmark_drawdowns_vt.json"]

print("Bot:", BOT)
print("falten[-1]['name']        :", repr(plan[BOT]["falten"][-1]["name"]))
print("falten[-1]['rolle']       :", repr(plan[BOT]["falten"][-1]["rolle"]))
print("bestaetigungsperiode (Plan):", repr(plan[BOT]["bestaetigungsperiode"]))
print("gleicher String?          :",
      plan[BOT]["falten"][-1]["name"] == plan[BOT]["bestaetigungsperiode"])

geaendert = copy.deepcopy(plan)
geaendert[BOT]["bestaetigungsperiode"] = SPANNE   # nur im Speicher

with tempfile.TemporaryDirectory(prefix="tb88_m2_") as d:
    bd.erzeuge(d, BOT, mess=mess, plan=plan)       # UNVERAENDERTER Plan
    import pandas as pd
    z = pd.read_csv(os.path.join(d, BOT, "zellen.csv"), dtype={"falte": str})
    print("Spalte falte, Werte       :", sorted(z["falte"].unique()))

    def versuch(titel, p, tabellen):
        print("\n---", titel)
        try:
            e = aw.ein_bot(BOT, d, mess, p, tabellen)
            print("ERGEBNIS: LAEUFT DURCH - kein Abbruch.")
            print("bestaetigungsperiode:", {k: e["bestaetigungsperiode"].get(k)
                                            for k in ("bestimmt", "falte")})
        except BaseException as x:          # Abbruch erbt von SystemExit
            print("ERGEBNIS:", type(x).__module__ + "." + type(x).__name__)
            print("Wortlaut:", str(x))
            tb = traceback.extract_tb(x.__traceback__)[-1]
            print("Ort     :", os.path.relpath(tb.filename, REPO), "Z.",
                  tb.lineno, "in", tb.name)

    for q in QUELLEN:
        tabellen = lies(q)
        print("\n========== Tabellen aus ergebnisse/" + q)
        versuch("Kontrolle: UNVERAENDERTER Plan", plan, tabellen)
        versuch("Probe: bestaetigungsperiode = %r" % SPANNE, geaendert, tabellen)
