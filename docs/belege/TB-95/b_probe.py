#!/usr/bin/env python3
"""TB-95 Block B - Nachweis, dass G6 und H3 nach der Anpassung beissen, und aus dem richtigen Grund.

Aufruf (Repo-Wurzel): trading-env/bin/python3 -W ignore docs/belege/TB-95/b_probe.py > docs/belege/TB-95/b_probe.txt
Benutzt die Funktionen des Tests selbst (teil_g, _h3_lauf), keine Nachbauten.
"""
import copy
import datetime as dt
import os
import subprocess
import sys
import tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.abspath(os.path.join(HIER, "..", "..", ".."))
sys.path.insert(0, os.path.join(WURZEL, "research", "vorregistrierung"))
import test_vorregistrierung as t  # noqa: E402

print(f"# TB-95 Block B - HEAD {subprocess.run(['git', '-C', WURZEL, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()}"
      f" + Arbeitsbaum (test_vorregistrierung.py geaendert), {dt.datetime.now().astimezone():%Y-%m-%d %H:%M:%S %z}")
mess, plan = t._mess(), t._plan()


def g6_lauf(plan_fn, titel):
    t.gescheitert.clear()
    t.bestanden = 0
    alt = t._plan
    t._plan = plan_fn
    try:
        t.teil_g()
    finally:
        t._plan = alt
    g6 = [g for g in t.gescheitert if g.startswith("G6")]
    andere = [g for g in t.gescheitert if not g.startswith("G6")]
    print(f"\n## {titel}\n   Teil G: {t.bestanden} bestanden, {len(t.gescheitert)} gescheitert; davon G6: {len(g6)}")
    for g in g6:
        print(f"   - {g[:220]}")
    for g in andere:
        print(f"   (anderes) {g[:200]}")
    return g6


print("\n# B1 - G6")
print(f"   Jahre aus dem Register: {t._testjahre_aus_register()}  (Register: {os.path.relpath(t.REGISTER, WURZEL)})")
r = g6_lauf(lambda: plan, "B1-a echter Plan: erwartet 0 G6 rot")

p2 = copy.deepcopy(plan)
for f in p2["elliott_wave"]["falten"]:
    if f["name"] == "2020-2021":
        f["rolle"] = "bestaetigung"
g6_lauf(lambda: p2, "B1-b Gegenprobe: elliott_wave '2020-2021' als Rolle bestaetigung -> erwartet genau 1 G6 rot (elliott_wave)")

p3 = copy.deepcopy(plan)
p3["turtle_soup_stocks"]["falten"] = [f for f in p3["turtle_soup_stocks"]["falten"] if f["name"] != "2022"]
g6_lauf(lambda: p3, "B1-c Gegenprobe: turtle_soup_stocks ohne Falte 2022 -> erwartet genau 1 G6 rot (turtle_soup_stocks)")

with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tmp:
    tmp.write(open(t.REGISTER, encoding="utf-8").read().replace(
        "4. **2020 und 2022 sind Testfalten", "4. **2020 und 2022 sind Pruefjahre"))
alt_reg = t.REGISTER
t.REGISTER = tmp.name
g6_lauf(lambda: plan, "B1-d Gegenprobe: Registersatz 5.1 Nr. 4 fehlt (Kopie) -> erwartet 9 G6 rot, Jahre None")
t.REGISTER = alt_reg
os.unlink(tmp.name)

print("\n# B2 - H3")
sel = t._selektionsfalten(plan[t.BOT])
for titel, ohne in (("B2-a neue Menge aus dem Plan (strikte Mehrheit) - muss BEISSEN", set(sel[:len(sel) // 2 + 1])),
                    ("B2-b Gegenprobe ohne = leer - darf NICHT beissen (H3 muesste scheitern)", set()),
                    ("B2-c alte Menge {2019..2022} - Vergleich, beisst nicht", {"2019", "2020", "2021", "2022"})):
    vorher, nachher = t._h3_lauf(mess, plan, ohne)
    a, b = t._sharpezeile(vorher.stdout), t._sharpezeile(nachher.stdout)
    h3 = vorher.returncode == 0 and nachher.returncode == 0 and a != b
    print(f"\n## {titel}\n   ohne = {sorted(ohne)} ({len(ohne)} von {len(sel)} Selektionsfalten)")
    print(f"   mit Regel:  rc {vorher.returncode}  {a!r}")
    print(f"   ohne Regel: rc {nachher.returncode}  {b!r}")
    print(f"   H3-Bedingung: {'BESTANDEN' if h3 else 'GESCHEITERT'}")
