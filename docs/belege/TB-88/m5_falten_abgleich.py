"""TB-88 M5 Zusatz: Faltennamen/Rollen des Plans (nur im Speicher berechnet)
gegen die Falten der beiden Benchmark-Tabellen. Nur lesend."""
import json, os, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
VR = os.path.join(REPO, "research", "vorregistrierung")
sys.path.insert(0, VR)
import faltenplan as fp, registerdaten as rd
plan = fp.faltenplan(rd._mess())
tab = {q: json.load(open(os.path.join(VR, "ergebnisse", q), encoding="utf-8"))
       for q in ("benchmark_drawdowns.json", "benchmark_drawdowns_vt.json")}
for bot, p in plan.items():
    namen = [f["name"] for f in p["falten"]]
    rollen = {f["name"]: f["rolle"] for f in p["falten"]}
    print(f"{bot}: Plan {namen[0]}..{namen[-1]} ({len(namen)}), bestaetigungsperiode={p['bestaetigungsperiode']!r}")
    for q, t in tab.items():
        tf = t[bot]["falten"]
        fehlt = [n for n in namen if n not in tf]
        extra = [n for n in tf if n not in namen]
        rolle_ab = [n for n in namen if n in tf and tf[n]["rolle"] != rollen[n]]
        print(f"   {q:30s} fehlt={fehlt} zusaetzlich={extra} rolle_abweichend={rolle_ab}")
