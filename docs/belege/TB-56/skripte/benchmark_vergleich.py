#!/usr/bin/env python3
"""TB-56: gesperrte Benchmark-Tabelle gegen die neu gerechnete (eigene Datei).
    trading-env/bin/python3 docs/belege/TB-56/skripte/benchmark_vergleich.py
"""
import json, os
W = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
E = os.path.join(W, "research", "vorregistrierung", "ergebnisse")
alt = json.load(open(os.path.join(E, "benchmark_drawdowns.json"), encoding="utf-8"))
neu = json.load(open(os.path.join(E, "benchmark_drawdowns_ohne_schranke.json"), encoding="utf-8"))["bots"]
for bot in sorted(alt):
    a, n = alt[bot], neu[bot]
    if a["status"] != "endgueltig":
        print(f"{bot:<28}Platzhalter, unveraendert: {a == n}")
        continue
    gemeinsam = sorted(set(a["falten"]) & set(n["falten"]))
    hinzu = sorted(set(n["falten"]) - set(a["falten"]))
    gleich = all(a["falten"][f] == n["falten"][f] for f in gemeinsam)
    print(f"{bot:<28}gemeinsame Falten {gemeinsam[0]}..{gemeinsam[-1]} zeichengleich: {gleich}; "
          f"neu: {hinzu}; DD_Toleranz gleich: {a['dd_toleranz'] == n['dd_toleranz']} "
          f"(@0.50 {a['dd_toleranz']['0.50']} -> {n['dd_toleranz']['0.50']}, "
          f"@1.00 {a['dd_toleranz']['1.00']} -> {n['dd_toleranz']['1.00']})")
    for f in hinzu:
        x = n["falten"][f]
        print(f"{'':<28}  {f}: {x['symbole_point_in_time']} Titel, {x['handelstage']} Handelstage, "
              f"DD @0.25 {x['dd_benchmark']['0.25']} @0.50 {x['dd_benchmark']['0.50']} "
              f"@0.75 {x['dd_benchmark']['0.75']} @1.00 {x['dd_benchmark']['1.00']}")
