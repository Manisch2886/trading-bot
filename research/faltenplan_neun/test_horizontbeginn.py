#!/usr/bin/env python3
"""
TB-80 - Bedingung (i) rechnet gegen den Horizontbeginn aus dem Register
==============================================================================
Geprueft wird, dass `research/vorregistrierung/faltenplan.py` Bedingung (i)
der Neufassung 4a (Register 25.3, praezisiert in 26.2) gegen das absolute
Datum je Bot aus Register 28.4 rechnet - und nicht mehr gegen die Datenuhr
(`faltenplan_neun.fensteranker`: zehn Jahre vor dem letzten Kurstag des
Marktes).

  1  Jeder Aktien-Bot rechnet gegen 2016-09-19: `erste_falte_4a_messung`
     nennt diesen Horizontbeginn, das frueheste Warm-Datum liegt nicht davor,
     und der Anker ist nicht die Datenuhr - im Speicher nachgewiesen: mit der
     Datenuhr als Anker aendert sich das Warm-Datum jedes Aktien-Bots (solange
     Datenuhr und Horizontbeginn verschieden sind; sind sie es an einem
     kuenftigen Datenstand zufaellig nicht, meldet der Test das statt zu raten).
     Dazu: der Quelltext von `erste_falte_4a_messung` ruft `fensteranker`
     nicht auf.
  2  Die fuenf Krypto-Bots sind unveraendert gegenueber dem Ausgangsstand aus
     TB-80 Schritt 0 (docs/belege/TB-80/faltenplan_stand_vor_tb80.json und
     schritt0_warm_ab.txt): erste_falte_4a und Warm-Datum auf Tagesebene, und
     ihr Horizontbeginn ist None.
  3  Die Konjunktion gilt weiter: erste_falte >= erste_falte_4a bei allen neun
     (der Plan wird dafuer gerechnet, mit Trockenlauf - rund 35 s).
  4  Das Literal stimmt mit dem Register ueberein: der Test liest die Tabelle
     in Register 28.4 (Spalte "Horizontbeginn") je Bot aus dem Registertext
     und vergleicht sie mit `faltenplan.horizontbeginn(bot)` - Aktien-Bots
     ein Datum, Krypto-Bots "kein Horizont" = None. Dazu, in Gegenrichtung:
     der Horizontbeginn ein Jahr spaeter bewegt mindestens eine erste Falte
     (Prueffrage B1: eine Probe, die nichts verwerfen kann, ist keine Probe).

    trading-env/bin/python3 research/faltenplan_neun/test_horizontbeginn.py

Braucht pandas (faltenplan.py importiert es), laeuft deshalb mit
trading-env/bin/python3. Rueckgabewert 0, wenn alle Pruefungen bestehen,
sonst 1. Eigener Test neben test_erste_falte_trockenlauf.py, weil der dort
gepruefte Gegenstand (Bedingung (ii), die Ableitung aus dem Trockenlauf) ein
anderer ist und drei Minuten laeuft; dieser hier prueft Bedingung (i).
"""

import datetime as dt
import inspect
import json
import os
import re
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)
import faltenplan_neun as fn  # noqa: E402

BASE_DIR = fn.BASE_DIR
VORREG = os.path.join(BASE_DIR, "research", "vorregistrierung")
sys.path.insert(0, VORREG)
import faltenplan as vfp  # noqa: E402
import registerdaten as rd  # noqa: E402

REGISTER = os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_neuselektion.md")
BELEGE = os.path.join(BASE_DIR, "docs", "belege", "TB-80")

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


def register_28_4():
    """{bot: date | None} aus der Tabelle in Register 28.4, Spalte Horizontbeginn."""
    with open(REGISTER, encoding="utf-8") as f:
        zeilen = f.read().splitlines()
    start = next((i for i, z in enumerate(zeilen) if z.startswith("### 28.4")), None)
    if start is None:
        return {}
    aus = {}
    kopf_gesehen = False
    for z in zeilen[start + 1:]:
        if z.startswith("### ") or z.startswith("## "):
            break
        if z.startswith("| Bot") and "Horizontbeginn" in z:
            kopf_gesehen = True
            continue
        m = re.match(r"^\|\s*`([a-z0-9_]+)`\s*\|", z)
        if kopf_gesehen and m:
            felder = [t.strip() for t in z.strip().strip("|").split("|")]
            datum = re.search(r"\d{4}-\d{2}-\d{2}", felder[3])
            if datum:
                aus[m.group(1)] = dt.date.fromisoformat(datum.group(0))
            elif "kein Horizont" in felder[3]:
                aus[m.group(1)] = None
        elif kopf_gesehen and not z.startswith("|") and aus:
            break
    return aus


def schritt0():
    """Ausgangsstand aus TB-80 Schritt 0: {bot: (erste_falte_4a, warm ab)}."""
    with open(os.path.join(BELEGE, "faltenplan_stand_vor_tb80.json"), encoding="utf-8") as f:
        plan = json.load(f)
    warm = {}
    with open(os.path.join(BELEGE, "schritt0_warm_ab.txt"), encoding="utf-8") as f:
        for z in f:
            m = re.match(r"^(\S+)\s+(\S+)\s+(\d{4}-\d{2}-\d{2})", z)
            if m:
                warm[m.group(1)] = m.group(3)
    return {b: (plan[b]["erste_falte_4a"], warm[b]) for b in plan}


def mit_anker(anker: dict):
    """erste_falte_4a_messung je Bot unter einem anderen HORIZONTBEGINN - im
    Speicher, danach wiederhergestellt."""
    original = dict(vfp.HORIZONTBEGINN)
    vfp.HORIZONTBEGINN.clear()
    vfp.HORIZONTBEGINN.update(anker)
    try:
        return {b: vfp.erste_falte_4a_messung(b) for b in fn.BOTS}
    finally:
        vfp.HORIZONTBEGINN.clear()
        vfp.HORIZONTBEGINN.update(original)


def main():
    print(__doc__.strip().split("\n")[0])
    print(f"  Python {sys.version.split()[0]} ({sys.executable})")
    aktien = [b for b, e in fn.BOTS.items() if e["markt"] == "aktien"]
    krypto = [b for b, e in fn.BOTS.items() if e["markt"] == "krypto"]
    heute = {b: vfp.erste_falte_4a_messung(b) for b in fn.BOTS}
    datenuhr = {m: fn.fensteranker(m) for m in ("aktien", "krypto")}
    unter_uhr = mit_anker(datenuhr)
    reg = register_28_4()
    alt = schritt0()

    print(f"\n{'Bot':<28}{'Horizont':<12}{'warm ab':<12}{'4a':>5}  {'Reg. 28.4':<12}{'Datenuhr':<12}{'warm (Uhr)':<12}")
    print("-" * 96)
    for b in fn.BOTS:
        h = heute[b]
        print(f"{b:<28}{str(h['horizontbeginn']):<12}{h['warm_ab_fruehestes']:<12}"
              f"{h['erste_falte_4a']:>5}  {str(reg.get(b, '?')):<12}"
              f"{str(datenuhr[fn.BOTS[b]['markt']]):<12}{unter_uhr[b]['warm_ab_fruehestes']:<12}")

    # 1 - Aktien-Bots gegen 2016-09-19, nicht gegen die Datenuhr
    for b in aktien:
        h = heute[b]
        pruefe(f"1: {b} - Horizontbeginn 2016-09-19", h["horizontbeginn"] == "2016-09-19",
               str(h["horizontbeginn"]))
        pruefe(f"1: {b} - fruehestes Warm-Datum nicht vor dem Horizontbeginn",
               h["warm_ab_fruehestes"] >= "2016-09-19", h["warm_ab_fruehestes"])
        if datenuhr["aktien"] != dt.date(2016, 9, 19):
            pruefe(f"1: {b} - mit der Datenuhr ({datenuhr['aktien']}) als Anker aendert sich "
                   f"das Warm-Datum: der Anker ist nicht die Datenuhr",
                   unter_uhr[b]["warm_ab_fruehestes"] != h["warm_ab_fruehestes"],
                   f"{unter_uhr[b]['warm_ab_fruehestes']} = {h['warm_ab_fruehestes']}")
        else:
            pruefe(f"1: {b} - Datenuhr und Horizontbeginn fallen an diesem Datenstand zusammen; "
                   f"die Unterscheidung ist heute nicht messbar (gemeldet, nicht geraten)", False)
    quelle = inspect.getsource(vfp.erste_falte_4a_messung)
    pruefe("1: erste_falte_4a_messung ruft fensteranker nicht auf (Quelltext der Funktion)",
           "fensteranker" not in quelle and "horizontbeginn(" in quelle)
    pruefe("1: HORIZONTBEGINN['aktien'] ist ein date-Literal, kein gerechneter Wert",
           isinstance(vfp.HORIZONTBEGINN["aktien"], dt.date)
           and re.search(r'^HORIZONTBEGINN\s*=\s*\{"aktien":\s*date\(2016,\s*9,\s*19\)',
                         inspect.getsource(vfp), re.M) is not None)

    # 2 - Krypto unveraendert gegenueber Schritt 0
    for b in krypto:
        h = heute[b]
        pruefe(f"2: {b} - kein Horizont (None)", h["horizontbeginn"] is None)
        pruefe(f"2: {b} - erste_falte_4a = Schritt 0", h["erste_falte_4a"] == alt[b][0],
               f"{h['erste_falte_4a']} gegen {alt[b][0]}")
        pruefe(f"2: {b} - Warm-Datum = Schritt 0 (Tagesebene)",
               h["warm_ab_fruehestes"] == alt[b][1], f"{h['warm_ab_fruehestes']} gegen {alt[b][1]}")
    pruefe("2: Schritt-0-Beleg hat neun Bots", sorted(alt) == sorted(fn.BOTS), str(sorted(alt)))

    # 4 - das Literal gegen den Registertext 28.4
    pruefe("4: Register 28.4 hat neun Zeilen mit Horizontbeginn", sorted(reg) == sorted(fn.BOTS),
           str(sorted(reg)))
    for b in fn.BOTS:
        pruefe(f"4: {b} - Literal im Faltenplan = Register 28.4",
               b in reg and vfp.horizontbeginn(b) == reg[b],
               f"Code {vfp.horizontbeginn(b)}, Register {reg.get(b, '?')}")
    spaeter = {"aktien": dt.date(2016 + 1, 9, 19), "krypto": None}
    unter_spaeter = mit_anker(spaeter)
    bewegt = [b for b in aktien if unter_spaeter[b]["erste_falte_4a"] != heute[b]["erste_falte_4a"]]
    pruefe("4: Gegenrichtung - Horizontbeginn ein Jahr spaeter bewegt mindestens eine erste Falte",
           bool(bewegt), str({b: unter_spaeter[b]["erste_falte_4a"] for b in aktien}))
    pruefe("4: Gegenrichtung - Krypto bewegt sich dabei nicht",
           all(unter_spaeter[b] == heute[b] for b in krypto))
    pruefe("4: nach den Proben ist das Original wiederhergestellt",
           vfp.HORIZONTBEGINN == {"aktien": dt.date(2016, 9, 19), "krypto": None},
           str(vfp.HORIZONTBEGINN))

    # 3 - die Konjunktion, mit Trockenlauf
    print("\n  Plan mit Trockenlauf (faltenplan.faltenplan) ...", flush=True)
    plan = vfp.faltenplan(rd._mess())
    for b in fn.BOTS:
        p = plan[b]
        pruefe(f"3: {b} - erste_falte >= erste_falte_4a", p["erste_falte"] >= p["erste_falte_4a"],
               f"{p['erste_falte']} < {p['erste_falte_4a']}")
        pruefe(f"3: {b} - der Plan traegt denselben Horizontbeginn und dasselbe Warm-Datum",
               p["horizontbeginn"] == heute[b]["horizontbeginn"]
               and p["erste_falte_4a_warm_ab"] == heute[b]["warm_ab_fruehestes"])
    erste = ", ".join("%s: %s" % (b, plan[b]["erste_falte"]) for b in fn.BOTS)
    print("  erste_falte je Bot: {%s}" % erste)

    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
