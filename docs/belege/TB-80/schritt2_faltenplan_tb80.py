"""TB-80 Schritt 2: den Plan nach der Umstellung DANEBEN schreiben und mit dem
Ausgangsstand aus Schritt 0 vergleichen - berichten, nicht bewerten.

Schreibt research/vorregistrierung/ergebnisse/faltenplan_tb80.json mit
denselben json.dump-Einstellungen wie faltenplan.py::main, OHNE dessen main()
aufzurufen (das schreibt immer nach faltenplan.json - Sperrliste Punkt 2).
Vergleich je Bot gegen docs/belege/TB-80/faltenplan_stand_vor_tb80.json
(Schritt 0, byteweise = faltenplan_tb72.json): erste_falte_4a, erste_falte,
Zahl der Selektionsfalten, Falten einzeln; dazu die neuen Felder
horizontbeginn und erste_falte_4a_warm_ab und die Warm-Daten aus
schritt0_warm_ab.txt auf Tagesebene.

    trading-env/bin/python3 docs/belege/TB-80/schritt2_faltenplan_tb80.py
"""
import hashlib, json, os, re, sys, time
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
VR = os.path.join(BASE, "research", "vorregistrierung")
sys.path.insert(0, VR)
import faltenplan as vfp
import registerdaten as rd

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(VR, "ergebnisse", "faltenplan_tb80.json")
VORHER = os.path.join(HIER, "faltenplan_stand_vor_tb80.json")
assert os.path.basename(ZIEL) not in ("faltenplan.json", "faltenplan_tb72.json")


def sha(pfad):
    with open(pfad, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


print("TB-80 Schritt 2 - Wirkung der Umstellung, gemessen")
print(f"Python {sys.version.split()[0]}  ({sys.executable})")
print(f"Zeit (UTC): {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
print(f"HORIZONTBEGINN im Code: {vfp.HORIZONTBEGINN}\n")

t0 = time.time()
plan = vfp.faltenplan(rd._mess())
print(f"faltenplan() gerechnet in {time.time() - t0:.0f} s")
with open(ZIEL, "w", encoding="utf-8") as f:
    json.dump(plan, f, indent=2, ensure_ascii=False, sort_keys=True)
    f.write("\n")
print(f"Geschrieben: {os.path.relpath(ZIEL, BASE)}  SHA-256 {sha(ZIEL)}\n")

with open(VORHER, encoding="utf-8") as f:
    alt = json.load(f)
print(f"Vorher: {os.path.relpath(VORHER, BASE)}  SHA-256 {sha(VORHER)}")

# Warm-Daten aus Schritt 0 (Tagesebene)
warm_vorher = {}
with open(os.path.join(HIER, "schritt0_warm_ab.txt"), encoding="utf-8") as f:
    for z in f:
        m = re.match(r"^(\S+)\s+(\S+)\s+(\d{4}-\d{2}-\d{2})", z)
        if m:
            warm_vorher[m.group(1)] = (m.group(2), m.group(3))

print("\n| Bot | Markt | erste_falte_4a vorher | nachher | erste_falte vorher | nachher | Selektionsfalten vorher -> nachher |")
print("|---|---|---:|---:|---:|---:|---|")
geaendert_jahr, geaendert_falten = [], []
for bot, p in plan.items():
    a = alt[bot]
    print(f"| `{bot}` | {p['markt']} | {a['erste_falte_4a']} | {p['erste_falte_4a']} | "
          f"{a['erste_falte']} | {p['erste_falte']} | "
          f"{len(a['selektionsfalten'])} -> {len(p['selektionsfalten'])} |")
    if (a["erste_falte_4a"], a["erste_falte"], a["selektionsfalten"]) != \
            (p["erste_falte_4a"], p["erste_falte"], p["selektionsfalten"]):
        geaendert_jahr.append(bot)
    af = {f["name"]: f for f in a["falten"]}
    nf = {f["name"]: f for f in p["falten"]}
    for name in sorted(set(af) | set(nf)):
        if af.get(name) != nf.get(name):
            geaendert_falten.append((bot, name))

print("\n| Bot | Anker vorher (Datenuhr) | Horizontbeginn nachher | warm ab vorher | warm ab nachher | Verschiebung |")
print("|---|---|---|---|---|---:|")
import datetime as dt
for bot, p in plan.items():
    av, wv = warm_vorher[bot]
    wn = p["erste_falte_4a_warm_ab"]
    d = (dt.date.fromisoformat(wn) - dt.date.fromisoformat(wv)).days
    print(f"| `{bot}` | {av} | {p['horizontbeginn']} | {wv} | {wn} | {d:+d} Tage |")

neue_felder = sorted(set(plan["volatility_breakout"]) - set(alt["volatility_breakout"]))
print(f"\nBots mit Aenderung an erste_falte_4a / erste_falte / selektionsfalten: "
      f"{len(geaendert_jahr)} {geaendert_jahr}")
print(f"Geaenderte, neue oder entfallene Falten (Grenzen, Rolle, Training, Embargo): "
      f"{len(geaendert_falten)} {geaendert_falten}")
print(f"Neue Felder je Bot: {neue_felder}")
krypto = [b for b, p in plan.items() if p["markt"] == "krypto"]
# Was sich bei den Krypto-Bots ueberhaupt unterscheidet - Feld fuer Feld
for b in krypto:
    anders = sorted(k for k in set(plan[b]) | set(alt[b]) if plan[b].get(k) != alt[b].get(k))
    print(f"Krypto {b}: abweichende Felder gegen Schritt 0: {anders}")
gleich = all(json.dumps({k: v for k, v in plan[b].items()
                         if k not in neue_felder and k != "erste_falte_quelle"}, sort_keys=True)
             == json.dumps({k: v for k, v in alt[b].items() if k != "erste_falte_quelle"},
                           sort_keys=True) for b in krypto)
print(f"Fuenf Krypto-Bots ohne die zwei neuen Felder und ohne den Text erste_falte_quelle "
      f"zeichengleich mit Schritt 0: {gleich}")
print(f"Krypto horizontbeginn: {[plan[b]['horizontbeginn'] for b in krypto]}, "
      f"warm ab vorher = nachher: "
      f"{all(warm_vorher[b][1] == plan[b]['erste_falte_4a_warm_ab'] for b in krypto)}")
# Ohne die zwei neuen Felder: ist der ganze Plan zeichengleich mit Schritt 0?
ohne = {b: {k: v for k, v in p.items() if k not in neue_felder and k != "erste_falte_quelle"}
        for b, p in plan.items()}
alt_ohne = {b: {k: v for k, v in p.items() if k != "erste_falte_quelle"} for b, p in alt.items()}
print(f"Alle neun Bots ohne neue Felder und ohne erste_falte_quelle zeichengleich: "
      f"{json.dumps(ohne, sort_keys=True) == json.dumps(alt_ohne, sort_keys=True)}")
