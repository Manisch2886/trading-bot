"""TB-80 Schritt 0: den Ausgangsstand messen, BEVOR eine Zeile geaendert wird.

Rechnet aus dem heutigen Code (nicht aus faltenplan_tb72.json gelesen):
  - fn.fensteranker(markt) je Markt (die Datenuhr, die Bedingung (i) heute traegt)
  - erste_falte_4a(bot) und erste_falte(bot) je Bot (Konjunktion, mit Trockenlauf)
  - den ganzen Plan faltenplan() als Speicherstand daneben
    (docs/belege/TB-80/faltenplan_stand_vor_tb80.json) - fuer den Vergleich
    in Schritt 2 mit denselben json.dump-Einstellungen wie faltenplan.py::main,
    OHNE dessen main() aufzurufen (das schreibt immer nach faltenplan.json).
Dazu die SHA-256 der drei Sperrlisten-Dateien und von faltenplan_tb72.json,
mit vollem Pfad.

    trading-env/bin/python3 docs/belege/TB-80/schritt0_ausgangsstand.py
"""
import hashlib, json, os, sys, time
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))  # docs/belege/TB-80 -> Repo-Wurzel
VR = os.path.join(BASE, "research", "vorregistrierung")
sys.path.insert(0, VR)
import faltenplan as vfp
import registerdaten as rd
fn = vfp.fn

HIER = os.path.dirname(os.path.abspath(__file__))
STAND = os.path.join(HIER, "faltenplan_stand_vor_tb80.json")
assert os.path.basename(STAND) != "faltenplan.json"

GESPERRT = ["research/vorregistrierung/ergebnisse/benchmark_drawdowns.json",
            "research/vorregistrierung/ergebnisse/faltenplan.json",
            "research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json",
            "research/vorregistrierung/ergebnisse/faltenplan_tb72.json"]


def sha(rel):
    with open(os.path.join(BASE, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


print("TB-80 Schritt 0 - Ausgangsstand, gerechnet aus dem heutigen Code")
print(f"Python {sys.version.split()[0]}  ({sys.executable})")
print(f"Zeit (UTC): {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")

print("SHA-256 (voller Pfad ab Repo-Wurzel):")
for rel in GESPERRT:
    print(f"  {sha(rel)}  {rel}")

print("\nfn.fensteranker(markt) je Markt (Datenuhr, heutiger Bezug von Bedingung (i)):")
anker = {}
for markt in ("aktien", "krypto"):
    a = fn.fensteranker(markt)
    anker[markt] = a.isoformat() if a else None
    print(f"  {markt:8s} {anker[markt]}")

print("\nerste_falte_4a(bot) je Bot (Bedingung (i) allein):")
e4a = {}
for bot in rd.BOTS:
    e4a[bot] = vfp.erste_falte_4a(bot)
    print(f"  {bot:28s} {e4a[bot]}")

print("\nfaltenplan() - Konjunktion mit Trockenlauf (9 Kindprozesse) ...", flush=True)
t0 = time.time()
plan = vfp.faltenplan(rd._mess())
print(f"  gerechnet in {time.time() - t0:.0f} s\n")
with open(STAND, "w", encoding="utf-8") as f:
    json.dump(plan, f, indent=2, ensure_ascii=False, sort_keys=True)
    f.write("\n")

print(f"{'Bot':28s} {'Markt':7s} {'4a':>5s} {'erste':>6s} {'#Sel':>5s}  Selektionsfalten")
for bot, p in plan.items():
    assert p["erste_falte_4a"] == e4a[bot]
    print(f"{bot:28s} {p['markt']:7s} {p['erste_falte_4a']:5d} {p['erste_falte']:6d} "
          f"{len(p['selektionsfalten']):5d}  {', '.join(p['selektionsfalten'])}")

print(f"\nSpeicherstand geschrieben: {os.path.relpath(STAND, BASE)}")
print(f"  SHA-256 {sha(os.path.relpath(STAND, BASE))}")
