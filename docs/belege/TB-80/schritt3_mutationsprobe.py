"""TB-80 Schritt 3: Mutationsprobe in beide Richtungen - IM SPEICHER, nichts
wird committet, faltenplan.py bleibt unveraendert (git diff vorher/nachher).

Richtung 1 - die Datenuhr wieder einsetzen: HORIZONTBEGINN wird im Speicher
  durch {markt: fn.fensteranker(markt)} ersetzt (aktien 2016-09-01, krypto
  None). Erwartet: der Plan liefert Bot fuer Bot den ALTEN Stand aus Schritt 0
  - erste_falte_4a, erste_falte, Selektionsfalten UND die Warm-Daten auf
  Tagesebene (schritt0_warm_ab.txt) - und weicht von faltenplan_tb80.json in
  den Feldern horizontbeginn / erste_falte_4a_warm_ab der Aktien-Bots ab.
  (Auf Jahresebene sind alter und neuer Stand gleich; dort kann diese
  Richtung nicht beissen. Sie beisst auf Tagesebene.)
Richtung 2 - den Horizontbeginn ein Jahr nach hinten: aktien 2017-09-19.
  Erwartet: mindestens eine erste Falte bewegt sich (erste_falte_4a und,
  ueber die Konjunktion mit dem Trockenlauf, erste_falte).
Danach wird das Original wiederhergestellt und gegen faltenplan_tb80.json
nachgemessen.

    trading-env/bin/python3 docs/belege/TB-80/schritt3_mutationsprobe.py
"""
import datetime as dt, json, os, re, sys, time
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
VR = os.path.join(BASE, "research", "vorregistrierung")
sys.path.insert(0, VR)
import faltenplan as vfp
import registerdaten as rd
fn = vfp.fn
HIER = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HIER, "faltenplan_stand_vor_tb80.json"), encoding="utf-8") as f:
    alt = json.load(f)
with open(os.path.join(VR, "ergebnisse", "faltenplan_tb80.json"), encoding="utf-8") as f:
    neu = json.load(f)
warm_alt = {}
with open(os.path.join(HIER, "schritt0_warm_ab.txt"), encoding="utf-8") as f:
    for z in f:
        m = re.match(r"^(\S+)\s+(\S+)\s+(\d{4}-\d{2}-\d{2})", z)
        if m:
            warm_alt[m.group(1)] = m.group(3)

ORIGINAL = dict(vfp.HORIZONTBEGINN)
befund = []


def melde(name, ok, zusatz=""):
    befund.append((name, ok))
    print(f"  [{'OK' if ok else 'FEHL'}] {name}{(' - ' + zusatz) if zusatz else ''}")


print("TB-80 Schritt 3 - Mutationsprobe im Speicher")
print(f"Python {sys.version.split()[0]}  ({sys.executable})")
print(f"Zeit (UTC): {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
print(f"Original HORIZONTBEGINN: {ORIGINAL}\n")

# ---------------------------------------------------------------- Richtung 1
datenuhr = {m: fn.fensteranker(m) for m in ("aktien", "krypto")}
print(f"Richtung 1: Datenuhr wieder eingesetzt -> {datenuhr}")
vfp.HORIZONTBEGINN.clear(); vfp.HORIZONTBEGINN.update(datenuhr)
t0 = time.time()
plan_uhr = vfp.faltenplan(rd._mess())
print(f"  faltenplan() unter der Datenuhr in {time.time() - t0:.0f} s")
print(f"\n  {'Bot':28s} {'4a alt/uhr/neu':16s} {'erste alt/uhr/neu':19s} {'warm alt':11s} {'warm uhr':11s} {'warm neu':11s} horizont uhr/neu")
for bot in rd.BOTS:
    a, u, n = alt[bot], plan_uhr[bot], neu[bot]
    print(f"  {bot:28s} {a['erste_falte_4a']}/{u['erste_falte_4a']}/{n['erste_falte_4a']:<6} "
          f"{a['erste_falte']}/{u['erste_falte']}/{n['erste_falte']:<9} "
          f"{warm_alt[bot]:11s} {u['erste_falte_4a_warm_ab']:11s} {n['erste_falte_4a_warm_ab']:11s} "
          f"{u['horizontbeginn']}/{n['horizontbeginn']}")
    melde(f"R1 {bot}: erste_falte_4a / erste_falte / Selektionsfalten = Schritt 0",
          (u["erste_falte_4a"], u["erste_falte"], u["selektionsfalten"])
          == (a["erste_falte_4a"], a["erste_falte"], a["selektionsfalten"]))
    melde(f"R1 {bot}: Warm-Datum (Tagesebene) = Schritt 0",
          u["erste_falte_4a_warm_ab"] == warm_alt[bot],
          f"{u['erste_falte_4a_warm_ab']} gegen {warm_alt[bot]}")
    melde(f"R1 {bot}: Falten (Grenzen/Rolle/Training/Embargo) = Schritt 0",
          u["falten"] == a["falten"])
aktien = [b for b in rd.BOTS if rd.BOTS[b]["markt"] == "aktien"]
krypto = [b for b in rd.BOTS if rd.BOTS[b]["markt"] == "krypto"]
melde("R1 beisst: alle vier Aktien-Bots weichen unter der Datenuhr von faltenplan_tb80.json "
      "in horizontbeginn UND erste_falte_4a_warm_ab ab",
      all(plan_uhr[b]["horizontbeginn"] != neu[b]["horizontbeginn"]
          and plan_uhr[b]["erste_falte_4a_warm_ab"] != neu[b]["erste_falte_4a_warm_ab"]
          for b in aktien),
      str({b: (plan_uhr[b]["horizontbeginn"], plan_uhr[b]["erste_falte_4a_warm_ab"]) for b in aktien}))
melde("R1: die fuenf Krypto-Bots sind unter der Datenuhr zeichengleich mit faltenplan_tb80.json",
      all(plan_uhr[b] == neu[b] for b in krypto))
melde("R1 (Jahresebene, zur Kenntnis): unter der Datenuhr = neuer Plan in erste_falte_4a/erste_falte "
      "bei allen neun - die Richtung beisst NUR auf Tagesebene",
      all((plan_uhr[b]["erste_falte_4a"], plan_uhr[b]["erste_falte"])
          == (neu[b]["erste_falte_4a"], neu[b]["erste_falte"]) for b in rd.BOTS))

# ---------------------------------------------------------------- Richtung 2
spaeter = {"aktien": dt.date(2017, 9, 19), "krypto": None}
print(f"\nRichtung 2: Horizontbeginn ein Jahr nach hinten -> {spaeter}")
vfp.HORIZONTBEGINN.clear(); vfp.HORIZONTBEGINN.update(spaeter)
bewegt = []
print(f"  {'Bot':28s} {'4a neu -> +1J':14s} {'erste neu -> +1J':17s} {'warm +1J':11s} H je Kandidat")
for bot in aktien:
    m = vfp.erste_falte_4a_messung(bot)
    laenge = neu[bot]["faltenlaenge_jahre"]
    jahr, herkunft = vfp.erste_falte(bot, laenge, dt.date.fromisoformat(rd.GO_LIVE_SCHNITT))
    print(f"  {bot:28s} {neu[bot]['erste_falte_4a']} -> {m['erste_falte_4a']:<7} "
          f"{neu[bot]['erste_falte']} -> {jahr:<10} {m['warm_ab_fruehestes']:11s} "
          f"{[h['H'] for h in herkunft['H_je_gepruefter_falte']]}")
    if m["erste_falte_4a"] != neu[bot]["erste_falte_4a"] or jahr != neu[bot]["erste_falte"]:
        bewegt.append((bot, neu[bot]["erste_falte_4a"], m["erste_falte_4a"], neu[bot]["erste_falte"], jahr))
    melde(f"R2 {bot}: Konjunktion haelt, erste_falte >= erste_falte_4a", jahr >= m["erste_falte_4a"])
for bot in krypto:
    m = vfp.erste_falte_4a_messung(bot)
    melde(f"R2 {bot}: Krypto unveraendert (kein Horizont)",
          m["erste_falte_4a"] == neu[bot]["erste_falte_4a"]
          and m["warm_ab_fruehestes"] == neu[bot]["erste_falte_4a_warm_ab"])
melde("R2 beisst: mindestens eine erste Falte bewegt sich", bool(bewegt), str(bewegt))

# ---------------------------------------------------------------- Original
vfp.HORIZONTBEGINN.clear(); vfp.HORIZONTBEGINN.update(ORIGINAL)
print(f"\nOriginal wiederhergestellt: {vfp.HORIZONTBEGINN}")
for bot in rd.BOTS:
    m = vfp.erste_falte_4a_messung(bot)
    melde(f"Orig {bot}: erste_falte_4a_messung = faltenplan_tb80.json",
          (m["erste_falte_4a"], m["horizontbeginn"], m["warm_ab_fruehestes"])
          == (neu[bot]["erste_falte_4a"], neu[bot]["horizontbeginn"], neu[bot]["erste_falte_4a_warm_ab"]))

fehl = [n for n, ok in befund if not ok]
print(f"\n{len(befund) - len(fehl)}/{len(befund)} Proben wie erwartet"
      + (f"; FEHL: {fehl}" if fehl else "."))
sys.exit(1 if fehl else 0)
