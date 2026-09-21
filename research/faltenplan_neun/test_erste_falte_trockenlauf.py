#!/usr/bin/env python3
"""
TB-72 - Der Neun-Zahlen-Vergleich: erste Falte laut Plan gegen Trockenlauf
==============================================================================
Geprueft wird je Bot, dass `research/vorregistrierung/faltenplan.py` als erste
Falte das Jahr fuehrt, das die Neufassung von Registertext 4a / 21.3 (b) als
Konjunktion verlangt (Fable, docs/projektfuehrung/
FABLE_ANTWORT_2026-09-20e_konjunktion.md): das erste Kalenderjahr, das (i) im
Datenhorizont liegt und am 1. Januar den Indikator-Vorlauf erfuellt UND (ii)
in dem der Loader des Bots mindestens ein Symbol handelbar macht.

WAS DIESER TEST IST - UND WAS ER SEIT TB-72 SCHRITT 2 NICHT MEHR IST
------------------------------------------------------------------------------
Bis TB-72 rechnete `faltenplan.py` die erste Falte allein nach 4a nach, und
fuer `t3_supertrend` wich sie vom Trockenlauf ab (4a: 2018, 3b (a): 2019).
Ein Test, der Plan und Trockenlauf vergleicht, war damals eine Wache gegen
diese Abweichung. Seit Schritt 2 bezieht der Plan Bedingung (ii) selbst aus
dem Trockenlauf (`erste_falte_trockenlauf.erste_falte_nach_3b`). Fable dazu:
der Test ist damit *"nicht mehr eine Wache gegen Abweichung, sondern der
Nachweis, dass die Ableitung nicht regrediert."* Genau das prueft er: dass
niemand die Ableitung wieder durch die 4a-Nachrechnung ersetzt, ohne dass es
auffaellt.

Damit der Nachweis etwas wert ist, misst der Test Bedingung (ii) NICHT ueber
`erste_falte_trockenlauf`, sondern ruft das registrierte Werkzeug selbst auf
(`universum_trockenlauf.messe_bot`, TB-40; Registertext 3b: "ein anderes
Werkzeug ist dafuer nicht zulaessig") - ein Kindprozess je Bot ueber alle
4a-Kandidatenfalten, und rechnet die erste Falte mit H >= 1 hier nach.
Bedingung (i) kommt aus `faltenplan.erste_falte_4a` - der Rechnung, die auch
der Plan benutzt; sie ist nicht Gegenstand dieses Tests (TB-74).

  A  Die neun Zahlen: erste Falte laut Plan = erste 4a-Kandidatenfalte mit
     H >= 1 laut Trockenlauf - je Bot, und die Falten davor haben H = 0.
  B  Die Konjunktion kann den Beginn nicht vorziehen: erste Falte >= 4a.
  C  Die neun Zahlen stimmen mit der registrierten Tatsachennotiz 21.4
     ueberein (Register, Tabelle "erste Falte" - dort steht t3_supertrend
     seit TB-56b bei 2019; der Code hinkte bis TB-72 hinterher).
  D  Mutationsprobe (Prueffrage B1): eine Wegwerf-Kopie von
     research/vorregistrierung/, in der `_plan` die erste Falte wieder aus
     der 4a-Nachrechnung nimmt, laeuft als eigener Prozess - und ihre neun
     Zahlen weichen bei mindestens einem Bot vom Trockenlauf ab (heute:
     t3_supertrend 2018 statt 2019). Vorher zeigt die unveraenderte Kopie im
     eigenen Prozess dieselben neun Zahlen wie der Trockenlauf - sonst
     belegte die rote Probe nichts.

    trading-env/bin/python3 research/faltenplan_neun/test_erste_falte_trockenlauf.py

Braucht pandas (faltenplan.py importiert es), laeuft deshalb mit
trading-env/bin/python3. Laufzeit rund drei Minuten: 9 Kindprozesse fuer die
unabhaengige Messung, der Plan selbst, zwei Kopien im eigenen Prozess.
Rueckgabewert 0, wenn alle Pruefungen bestehen, sonst 1.
"""

import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)
import faltenplan_neun as fn  # noqa: E402

BASE_DIR = fn.BASE_DIR
VORREG = os.path.join(BASE_DIR, "research", "vorregistrierung")
sys.path.insert(0, VORREG)
sys.path.insert(0, os.path.join(BASE_DIR, "research", "universum_trockenlauf"))
import faltenplan as vfp  # noqa: E402
import registerdaten as rd  # noqa: E402
import universum_trockenlauf as ut  # noqa: E402

REGISTER = os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_neuselektion.md")

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


# ==============================================================================
# Die unabhaengige Messung von Bedingung (ii) - messe_bot direkt
# ==============================================================================
def kandidaten_4a(bot):
    laenge = vfp.faltenlaenge_jahre(bot)[0]
    schnitt = dt.date.fromisoformat(rd.GO_LIVE_SCHNITT)
    return vfp._jahresfalten(vfp.erste_falte_4a(bot), schnitt, laenge)


def trockenlauf_ab_4a(bot, kandidaten):
    """[(Faltenname, H)] ueber alle Kandidaten - ein Kindprozess."""
    stichtage = [ut.stichtage_der_falte(f["von"], f["bis_ausschliesslich"])[1]
                 for f in kandidaten]
    roh = ut.messe_bot(bot, stichtage)
    if roh["fehler"]:
        raise RuntimeError("Loader %s: %s" % (bot, roh["fehler"]))
    h = {l["stichtag"]: len(l["symbole"]) for l in roh["laeufe"]}
    return [(f["name"], h[s]) for f, s in zip(kandidaten, stichtage)]


def erste_mit_h(messung):
    for name, h in messung:
        if h >= 1:
            return int(name[:4])
    return None


# ==============================================================================
# Register 21.4 lesen - die Tatsachennotiz, nicht die ersetzte Tabelle in 15.6
# ==============================================================================
def register_21_4():
    with open(REGISTER, encoding="utf-8") as f:
        zeilen = f.read().splitlines()
    start = next((i for i, z in enumerate(zeilen) if z.startswith("### 21.4")), None)
    if start is None:
        return {}
    aus = {}
    kopf_gesehen = False
    for z in zeilen[start + 1:]:
        if z.startswith("### ") or z.startswith("## "):
            break
        if z.startswith("| Bot") and "erste Falte" in z:
            kopf_gesehen = True
            continue
        m = re.match(r"^\|\s*`([a-z0-9_]+)`\s*\|", z)
        if kopf_gesehen and m:
            felder = [t.strip().strip("*") for t in z.strip().strip("|").split("|")]
            aus[m.group(1)] = int(re.findall(r"\d{4}", felder[3])[0])
        elif kopf_gesehen and not z.startswith("|") and aus:
            break
    return aus


# ==============================================================================
# Die Wegwerf-Kopie im eigenen Prozess
# ==============================================================================
MUTATIONSSTELLE = "    erste, herkunft = erste_falte(bot, laenge, schnitt)\n"
# Seit TB-80 (21.09.2026) traegt `herkunft` auch horizontbeginn und
# erste_falte_4a_warm_ab; die Mutation fuellt sie aus erste_falte_4a_messung,
# damit die Kopie an der Mutation scheitert und nicht an einem KeyError in _plan.
MUTATION = ('    m4a = erste_falte_4a_messung(bot)  # MUTATION: 4a allein, wie vor TB-72\n'
            '    erste = m4a["erste_falte_4a"]\n'
            '    herkunft = {"erste_falte_4a": erste, "horizontbeginn": m4a["horizontbeginn"],\n'
            '                "erste_falte_4a_warm_ab": m4a["warm_ab_fruehestes"],\n'
            '                "H_je_gepruefter_falte": []}\n')


def _kopie(ziel):
    shutil.copytree(VORREG, ziel, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))


def _ersetze(pfad, alt, neu):
    with open(pfad, encoding="utf-8") as f:
        s = f.read()
    if alt not in s:
        raise AssertionError(f"Mutationsstelle nicht gefunden in {pfad}: {alt!r}")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(s.replace(alt, neu, 1))


def erste_falten_der_kopie(ordner):
    """faltenplan() der Kopie im EIGENEN Prozess - {bot: erste_falte}."""
    u = dict(os.environ)
    u["TB30A_BASE_DIR"] = BASE_DIR
    code = ("import json, faltenplan as fp\n"
            "print(json.dumps({b: p['erste_falte'] for b, p in fp.faltenplan().items()}))\n")
    r = subprocess.run([sys.executable, "-c", code], cwd=ordner, env=u,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("Kopie %s scheitert:\n%s" % (ordner, r.stderr[-2000:]))
    return json.loads(r.stdout.strip().splitlines()[-1])


# ==============================================================================
def main():
    print(__doc__.strip().split("\n")[0])
    print("  Trockenlauf je Bot (unabhaengig, messe_bot) ...", flush=True)
    messung = {}
    for bot in fn.BOTS:
        messung[bot] = trockenlauf_ab_4a(bot, kandidaten_4a(bot))
    trockenlauf = {bot: erste_mit_h(m) for bot, m in messung.items()}

    print("  Plan (faltenplan.faltenplan) ...", flush=True)
    plan = vfp.faltenplan(rd._mess())

    print(f"\n{'Bot':<28}{'4a':>6}{'Trockenl.':>10}{'Plan':>6}{'21.4':>6}  H je Kandidat ab 4a")
    print("-" * 96)
    reg = register_21_4()
    for bot in fn.BOTS:
        p = plan[bot]
        print(f"{bot:<28}{p['erste_falte_4a']:>6}{str(trockenlauf[bot]):>10}"
              f"{p['erste_falte']:>6}{str(reg.get(bot)):>6}  "
              f"{' / '.join(str(h) for _, h in messung[bot])}")
        # A - die neun Zahlen
        pruefe(f"A: {bot} - erste Falte laut Plan = erste Kandidatenfalte mit H >= 1",
               p["erste_falte"] == trockenlauf[bot],
               f"Plan {p['erste_falte']}, Trockenlauf {trockenlauf[bot]}")
        davor = [h for name, h in messung[bot] if int(name[:4]) < p["erste_falte"]]
        pruefe(f"A: {bot} - alle 4a-Kandidaten vor der ersten Falte haben H = 0",
               all(h == 0 for h in davor), str(davor))
        pruefe(f"A: {bot} - der Plan fuehrt die Messung mit (erste_falte_trockenlauf_H)",
               p["erste_falte_trockenlauf_H"]
               and p["erste_falte_trockenlauf_H"][-1]["H"] >= 1
               and all(e["H"] == 0 for e in p["erste_falte_trockenlauf_H"][:-1])
               and [e["H"] for e in p["erste_falte_trockenlauf_H"]]
               == [h for _, h in messung[bot][:len(p["erste_falte_trockenlauf_H"])]],
               str(p.get("erste_falte_trockenlauf_H")))
        # B - nie vorgezogen
        pruefe(f"B: {bot} - erste Falte >= 4a", p["erste_falte"] >= p["erste_falte_4a"])
        # C - Register 21.4
        pruefe(f"C: {bot} - erste Falte = Register 21.4",
               reg.get(bot) == p["erste_falte"], f"Register {reg.get(bot)}")
    pruefe("C0: Register 21.4 hat neun Zeilen", len(reg) == 9, str(sorted(reg)))
    pruefe("A0: genau ein Bot hat vor seiner ersten Falte einen 4a-Kandidaten mit H = 0 "
           "(t3_supertrend, 2018) - die bekannte Instanz",
           [b for b in fn.BOTS if trockenlauf[b] != plan[b]["erste_falte_4a"]]
           == ["t3_supertrend"],
           str({b: (plan[b]["erste_falte_4a"], trockenlauf[b]) for b in fn.BOTS}))

    teil_d(trockenlauf)

    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    return 0


def teil_d(trockenlauf):
    """D - Mutationsprobe im eigenen Prozess (Prueffrage B1)."""
    print("\n  Teil D: Wegwerf-Kopie ohne und mit Mutation ...", flush=True)
    with tempfile.TemporaryDirectory() as m:
        _kopie(m)
        kontrolle = erste_falten_der_kopie(m)
        pruefe("D0: die unveraenderte Kopie sieht im eigenen Prozess die neun Zahlen "
               "des Trockenlaufs", kontrolle == trockenlauf, str(kontrolle))
        try:
            _ersetze(os.path.join(m, "faltenplan.py"), MUTATIONSSTELLE, MUTATION)
        except AssertionError as e:
            # Die Ableitungszeile fehlt schon im Original - dann ist die
            # Ableitung bereits ersetzt worden, und die Probe meldet das
            # statt abzubrechen.
            pruefe("D1: die Ableitungszeile `erste, herkunft = erste_falte(...)` "
                   "steht in faltenplan.py", False, str(e))
            return
        mutiert = erste_falten_der_kopie(m)
        weicht_ab = sorted(b for b in fn.BOTS if mutiert[b] != trockenlauf[b])
        pruefe("D1: mit der 4a-Nachrechnung statt der Ableitung weicht mindestens ein "
               "Bot vom Trockenlauf ab - die Probe beisst",
               bool(weicht_ab), str(mutiert))
        pruefe("D2: es ist t3_supertrend, 2018 statt 2019",
               weicht_ab == ["t3_supertrend"] and mutiert["t3_supertrend"] == 2018
               and trockenlauf["t3_supertrend"] == 2019,
               f"{weicht_ab} {mutiert.get('t3_supertrend')}")
        print(f"  D: Kopie ohne Mutation = Trockenlauf: {kontrolle == trockenlauf}; "
              f"mit Mutation abweichend bei {weicht_ab} "
              f"(t3_supertrend: {mutiert.get('t3_supertrend')})")


if __name__ == "__main__":
    sys.exit(main())
