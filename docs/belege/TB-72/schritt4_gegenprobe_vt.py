"""TB-72 Schritt 4: benchmark_drawdowns_tb72.json gegen benchmark_drawdowns_vt.json.

Acht Bots muessen zeichengleich sein (alle Falten, alle 100 Stufen,
handelstage, Symbolzahlen, dd_toleranz); t3_supertrend wird Falte fuer Falte
und in DD_Toleranz dreispaltig gegen die Erwartung aus TB-65 (C1, 'ohne 2018')
gestellt. Rein lesend.

    trading-env/bin/python3 docs/belege/TB-72/schritt4_gegenprobe_vt.py
"""
import json, os
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
E = os.path.join(BASE, "research", "vorregistrierung", "ergebnisse")
vt = json.load(open(os.path.join(E, "benchmark_drawdowns_vt.json"), encoding="utf-8"))
neu = json.load(open(os.path.join(E, "benchmark_drawdowns_tb72.json"), encoding="utf-8"))
assert sorted(vt) == sorted(neu), (sorted(vt), sorted(neu))

print("Gegenprobe der acht anderen Bots: benchmark_drawdowns_tb72.json gegen _vt.json")
print("-" * 100)
print(f"{'Bot':<28}{'Falten':>7}{'Stufen':>8}{'Tage':>6}{'Symb.':>6}{'Tol.':>6}  Ergebnis")
gesamt_falten = gesamt_stufen = 0
abweichend = []
for bot in vt:
    if bot == "t3_supertrend":
        continue
    a, b = vt[bot], neu[bot]
    falten = sorted(a["falten"])
    gleich_falten = falten == sorted(b["falten"])
    n_stufen = n_tage = n_symb = 0
    diff = []
    for f in falten:
        fa, fb = a["falten"][f], b["falten"].get(f, {})
        for k in fa["dd_benchmark"]:
            n_stufen += 1
            if fa["dd_benchmark"][k] != fb.get("dd_benchmark", {}).get(k):
                diff.append((f, k))
        n_tage += 1
        if fa["handelstage"] != fb.get("handelstage"):
            diff.append((f, "handelstage"))
        n_symb += 1
        if fa["symbole_handelbar_in_falte"] != fb.get("symbole_handelbar_in_falte"):
            diff.append((f, "symbole"))
        for k in ("rolle", "von", "bis_ausschliesslich"):
            if fa[k] != fb.get(k):
                diff.append((f, k))
    tol = sum(1 for k in a["dd_toleranz"] if a["dd_toleranz"][k] != b["dd_toleranz"].get(k))
    rest = {k: (a.get(k) == b.get(k)) for k in ("handelbar_ab", "loader_schranke", "status", "markt", "benchmark")}
    ganz = json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    gesamt_falten += len(falten); gesamt_stufen += n_stufen
    print(f"{bot:<28}{len(falten):>7}{n_stufen:>8}{n_tage:>6}{n_symb:>6}{len(a['dd_toleranz']):>6}  "
          f"{'zeichengleich (json.dumps sort_keys identisch)' if ganz and gleich_falten and not diff and tol == 0 and all(rest.values()) else 'ABWEICHUNG ' + str(diff[:5]) + ' tol=' + str(tol) + ' ' + str(rest)}")
    if not (ganz and not diff and tol == 0):
        abweichend.append(bot)
print("-" * 100)
print(f"acht Bots: {gesamt_falten} Falten x 100 Stufen = {gesamt_stufen} Stufen, dazu handelstage und Symbolzahl je Falte, "
      f"DD_Toleranz 8 x 100; abweichend: {abweichend or 'keiner'}")

print("\nt3_supertrend: Falten vorher (_vt.json) / nachher (_tb72.json)")
print("-" * 100)
a, b = vt["t3_supertrend"], neu["t3_supertrend"]
print(f"{'Falte':<12}{'Rolle vt':<14}{'Rolle tb72':<14}{'Tage vt':>8}{'Tage tb72':>10}{'Symb vt':>8}{'Symb tb72':>10}  gleich (100 Stufen)")
for f in sorted(set(a["falten"]) | set(b["falten"])):
    fa, fb = a["falten"].get(f), b["falten"].get(f)
    if fa and fb:
        gl = fa["dd_benchmark"] == fb["dd_benchmark"] and fa["handelstage"] == fb["handelstage"] and fa["symbole_handelbar_in_falte"] == fb["symbole_handelbar_in_falte"]
        print(f"{f:<12}{fa['rolle']:<14}{fb['rolle']:<14}{fa['handelstage']:>8}{fb['handelstage']:>10}{fa['symbole_handelbar_in_falte']:>8}{fb['symbole_handelbar_in_falte']:>10}  {'ja' if gl else 'NEIN'}")
    elif fa:
        print(f"{f:<12}{fa['rolle']:<14}{'- entfaellt':<14}{fa['handelstage']:>8}{'-':>10}{fa['symbole_handelbar_in_falte']:>8}{'-':>10}  (DD alle Stufen: {set(fa['dd_benchmark'].values())})")
    else:
        print(f"{f:<12}{'-':<14}{fb['rolle']:<14}{'-':>8}{fb['handelstage']:>10}{'-':>8}{fb['symbole_handelbar_in_falte']:>10}  neu")
print(f"Selektionsfalten vt: {[f for f in a['falten'] if a['falten'][f]['rolle']=='selektion']}")
print(f"Selektionsfalten tb72: {[f for f in b['falten'] if b['falten'][f]['rolle']=='selektion']}")
erw = {"0.25": -13.90, "0.50": -26.57, "1.00": -48.10}
print(f"\n{'Stufe':<8}{'DD_Toleranz vt':>16}{'DD_Toleranz tb72':>18}{'Erwartung TB-65 C1':>20}  trifft")
for k in ("0.25", "0.50", "1.00"):
    print(f"{k:<8}{a['dd_toleranz'][k]:>16.2f}{b['dd_toleranz'][k]:>18.2f}{erw[k]:>20.2f}  {'ja' if abs(b['dd_toleranz'][k]-erw[k]) < 0.005 else 'NEIN'}")
n_tol = sum(1 for k in a["dd_toleranz"] if a["dd_toleranz"][k] != b["dd_toleranz"][k])
print(f"DD_Toleranz t3_supertrend: {n_tol} von 100 Stufen verschieden gegen _vt.json")
