#!/usr/bin/env python3
"""TB-88 M2b - die zwei Wege aus Anfrage 22h, NUR IM SPEICHER.

Nachtrag zur Probe m2: auswertung.py:177-182 vergleicht die Spalte `falte`
ausserdem gegen die Faltennamen des Plans. Das beruehrt Weg (B). Beide Wege
werden deshalb einmal durchgespielt - ohne eine Datei im Repo anzufassen:

  (A) die letzte Falte heisst die Spanne: plan[BOT]["falten"][-1]["name"] und
      plan[BOT]["bestaetigungsperiode"] = SPANNE (beides, wie Z. 338 es
      ableiten wuerde); Beispieldaten und Auswertung mit diesem Plan.
  (B) zwei Namen: Faltenname bleibt '2026', bestaetigungsperiode = SPANNE;
      in der erzeugten zellen.csv traegt die Bestaetigungszeile den
      Bezeichner (die Anforderung an den Erzeuger aus 22h, Weg B).
      (B') wie (B), aber zellen.csv unveraendert (= m2).

Tabellen aus benchmark_drawdowns_vt.json (nur gelesen), weil die registrierte
Datei schon die Kontrolle scheitern laesst (m2).
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

import pandas as pd              # noqa: E402
import auswertung as aw          # noqa: E402
import beispieldaten as bd       # noqa: E402
import faltenplan as fp          # noqa: E402
import registerdaten as rd       # noqa: E402

BOT = "turtle_soup_stocks"
SPANNE = "2026-01-01/2026-09-01"

mess = rd._mess()
plan = fp.faltenplan(mess)
with open(os.path.join(VR, "ergebnisse", "benchmark_drawdowns_vt.json"),
          encoding="utf-8") as f:
    tabellen = json.load(f)
alt = plan[BOT]["falten"][-1]["name"]


def versuch(titel, erzeuge_plan, auswerte_plan, csv_tausch=False):
    print("\n---", titel)
    with tempfile.TemporaryDirectory(prefix="tb88_m2b_") as d:
        bd.erzeuge(d, BOT, mess=mess, plan=erzeuge_plan)
        pfad = os.path.join(d, BOT, "zellen.csv")
        if csv_tausch:
            z = pd.read_csv(pfad, dtype=str)
            z.loc[z["falte"] == alt, "falte"] = SPANNE
            z.to_csv(pfad, index=False)
        z = pd.read_csv(pfad, dtype={"falte": str})
        print("falte-Werte in zellen.csv:", sorted(z["falte"].unique())[-2:], "...")
        try:
            e = aw.ein_bot(BOT, d, mess, auswerte_plan, tabellen)
            print("ERGEBNIS: LAEUFT DURCH - kein Abbruch.")
            print("bestaetigungsperiode:", {k: e["bestaetigungsperiode"].get(k)
                                            for k in ("bestimmt", "falte")})
        except BaseException as x:          # Abbruch erbt von SystemExit
            print("ERGEBNIS:", type(x).__module__ + "." + type(x).__name__)
            print("Wortlaut:", str(x)[:300])
            tb = traceback.extract_tb(x.__traceback__)[-1]
            print("Ort     :", os.path.relpath(tb.filename, REPO), "Z.",
                  tb.lineno, "in", tb.name)


# Weg A
plan_a = copy.deepcopy(plan)
plan_a[BOT]["falten"][-1]["name"] = SPANNE
plan_a[BOT]["bestaetigungsperiode"] = plan_a[BOT]["falten"][-1]["name"]
versuch("Weg (A): letzte Falte heisst die Spanne (Plan fuer Erzeugung UND Auswertung)",
        plan_a, plan_a)

# Weg B
plan_b = copy.deepcopy(plan)
plan_b[BOT]["bestaetigungsperiode"] = SPANNE
versuch("Weg (B): Faltenname bleibt, Bezeichner = Spanne, zellen.csv traegt den Bezeichner",
        plan, plan_b, csv_tausch=True)
versuch("Weg (B'): wie (B), zellen.csv traegt den Faltennamen (= Probe m2)",
        plan, plan_b, csv_tausch=False)
