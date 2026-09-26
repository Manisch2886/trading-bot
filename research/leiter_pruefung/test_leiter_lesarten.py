"""
Selbsttests zu leiter_lesarten.py (TB-116)
================================================================================
Jede Probe ist ein Hand-Beispiel mit vorher ausgerechneter Antwort (die
Rechnung steht im Kommentar der Probe). Zu jeder Probe gehoert eine
MUTATIONSGEGENPROBE: der Quelltext des Werkzeugs wird an genau einer Stelle
veraendert, als eigenes Modul geladen, und dieselbe Probe muss dort
SCHEITERN. Eine Probe, die auch die Mutante besteht, prueft nichts.

Nutzung (aus der Repo-Wurzel):
    trading-env/bin/python3 research/leiter_pruefung/test_leiter_lesarten.py
"""

import os
import sys
import types
from fractions import Fraction as F

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, _DIR)

import leiter_lesarten as L  # noqa: E402

QUELLE = open(os.path.join(_DIR, "leiter_lesarten.py"), encoding="utf-8").read()
REGISTER = os.path.join(_REPO, "docs", "VORREGISTRIERUNG_neuselektion.md")

_bestanden = 0
_fehler = []


def check(name, ok, detail=""):
    global _bestanden
    if ok:
        _bestanden += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        _fehler.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


def mutante(alt, neu):
    """Das Werkzeug mit genau einer Textersetzung, als eigenes Modul."""
    assert QUELLE.count(alt) == 1, "Mutationsstelle nicht eindeutig: %r" % alt
    mod = types.ModuleType("leiter_lesarten_mutante")
    exec(compile(QUELLE.replace(alt, neu), "leiter_lesarten_mutante", "exec"), mod.__dict__)
    return mod


def lesart(l1="L1b", l2="L2b", l3="L3a", l4="L4a", l5="L5a"):
    return {"L1": l1, "L2": l2, "L3": l3, "L4": l4, "L5": l5}


def m_von(mod, text, **kw):
    e = mod.rechne(mod.tabelle_aus_text(text), lesart(**kw))
    return e


def probe(name, fn, alt, neu):
    """fn(mod) -> (ok, detail). Muss am Werkzeug bestehen und an der Mutante scheitern."""
    try:
        ok, detail = fn(L)
    except Exception as ex:  # noqa: BLE001
        ok, detail = False, "Ausnahme %r" % ex
    check(name, ok, detail)
    try:
        ok_m, _ = fn(mutante(alt, neu))
    except Exception as ex:  # noqa: BLE001
        ok_m = False
    check(name + " - Mutationsgegenprobe scheitert", not ok_m, "Mutation: %r -> %r" % (alt[:50], neu[:50]))


ALLE_G = "FA:G UA:GGG FK:GG UK:GGG"
ALLE_S = "FA:S UA:SSS FK:SS UK:SSS"
NUR_K = "FA:S UA:SSS FK:GG UK:GGG"
S_UND_B = "FA:G UA:GGG FK:SB UK:GGG"
S_UND_G = "FA:G UA:GGG FK:SG UK:GGG"
UNGLEICH = "FA:G UA:SSS FK:GG UK:GGG"


# ---------------------------------------------------------------------------
# P1 alle Grundbudget, L1a: w(Aktien-Zelle) = 0,8/4 = 1/5, w(Krypto-Zelle) = 0,2/4 = 1/20.
#    m(VB) = 1/5*9 = 9/5; m(UA) = 1/5/3*9 = 3/5; m(FK) = 1/20/2*9 = 9/40; m(UK) = 1/20/3*9 = 3/20.
#    Buchsumme = 2/5 + 2/5 ... = 1/5+1/5+1/20+1/20 = 1/2; Rest 1/2.
# ---------------------------------------------------------------------------
def p1(mod):
    soll = (F(9, 5),) + (F(3, 5),) * 3 + (F(9, 40),) * 2 + (F(3, 20),) * 3
    ist = [m_von(mod, ALLE_G, l1="L1a", l2=l2) for l2 in ("L2a", "L2b", "L2c")]
    ok = all(e["antwort"] and e["m"] == soll and e["buchsumme"] == F(1, 2) for e in ist)
    return ok, "m=%s Summe=%s" % ([L.bruch(x) for x in ist[0]["m"]], ist[0]["buchsumme"])


# P2 alle Grundbudget, L1b (und L1c, weil beide Klassen zwei Zellen haben):
#    w(Aktien) = 0,8/2 = 2/5, w(Krypto) = 0,2/2 = 1/10.
#    m(VB) = 18/5; m(UA) = 6/5; m(FK) = 9/20; m(UK) = 3/10; Summe 1.
def p2(mod):
    soll = (F(18, 5),) + (F(6, 5),) * 3 + (F(9, 20),) * 2 + (F(3, 10),) * 3
    ist = [m_von(mod, ALLE_G, l1=l1, l2=l2) for l1 in ("L1b", "L1c") for l2 in ("L2a", "L2b", "L2c")]
    ok = all(e["antwort"] and e["m"] == soll and e["buchsumme"] == 1 for e in ist)
    return ok, "m=%s" % [L.bruch(x) for x in ist[0]["m"]]


# P3 alle Schatten: m = 0 ueberall.
#    L1b/L2a: keine Zelle in R -> Schluessel je Klasse in ihre Benchmark: 4/5, 1/5.
#    L1b/L2b: vier inaktive Zellen in R -> (j): Aktien 2/5+2/5, Krypto 1/10+1/10.
#    L1a/L2a: R leer -> nichts, Buchsumme 0.   L1a/L2b: 1/5+1/5 und 1/20+1/20 -> Summe 1/2.
#    L1a/L2c: m eindeutig (0), Benchmark haengt an R -> keine Antwort, Klasse L2c-benchmark.
def p3(mod):
    null = (F(0),) * 9
    a = m_von(mod, ALLE_S, l1="L1b", l2="L2a")
    b = m_von(mod, ALLE_S, l1="L1b", l2="L2b")
    c = m_von(mod, ALLE_S, l1="L1a", l2="L2a")
    d = m_von(mod, ALLE_S, l1="L1a", l2="L2b")
    e = m_von(mod, ALLE_S, l1="L1a", l2="L2c")
    ok = (a["m"] == null and a["benchmark"] == (F(4, 5), F(1, 5))
          and b["m"] == null and b["benchmark"] == (F(4, 5), F(1, 5))
          and c["m"] == null and c["buchsumme"] == 0
          and d["benchmark"] == (F(2, 5), F(1, 10)) and d["buchsumme"] == F(1, 2)
          and not e["antwort"] and e["fehlt"] == ["L2c-benchmark"])
    return ok, "L1b/L2b Benchmark %s, L1a/L2a Summe %s, L1a/L2c %s" % (
        [L.bruch(x) for x in b["benchmark"]], c.get("buchsumme"), e["fehlt"])


# P4 nur Krypto aktiv, L1b:
#    L3a: Aktien-Schluessel 4/5 in die Aktien-Benchmark; FK 1/10 -> m = 9/20 je Bot; UK 1/10/3*9 = 3/10.
#    L3b: Krypto-Schluessel 1 -> FK 1/2 -> m = 9/4; UK 1/2/3*9 = 3/2; keine Benchmark.
def p4(mod):
    null4 = (F(0),) * 4
    a = m_von(mod, NUR_K, l2="L2a", l3="L3a")
    b = m_von(mod, NUR_K, l2="L2a", l3="L3b")
    c = m_von(mod, NUR_K, l2="L2b", l3="L3b")
    ok = (a["m"] == null4 + (F(9, 20),) * 2 + (F(3, 10),) * 3 and a["benchmark"] == (F(4, 5), 0)
          and b["m"] == null4 + (F(9, 4),) * 2 + (F(3, 2),) * 3 and b["benchmark"] == (0, 0)
          and c["m"] == b["m"] and a["buchsumme"] == b["buchsumme"] == 1)
    return ok, "L3a m(FK)=%s, L3b m(FK)=%s" % (L.bruch(a["m"][4]), L.bruch(b["m"][4]))


# P5 nur Krypto aktiv, L2c: mit L1b antwortet es (Krypto-Zellen sind beide in jedem R, die
#    Aktien-Zellen sind entweder ausserhalb R -> Schluessel in Benchmark, oder inaktiv in R ->
#    (j) Benchmark); mit L1a haengt 1/|R| an der Vorgeschichte -> keine Antwort (L2c).
def p5(mod):
    a = m_von(mod, NUR_K, l1="L1b", l2="L2c")
    b = m_von(mod, NUR_K, l1="L1a", l2="L2c")
    ok = a["antwort"] and a["m"][4] == F(9, 20) and not b["antwort"] and b["fehlt"] == ["L2c"]
    return ok, "L1b/L2c Antwort %s, L1a/L2c fehlt %s" % (a["antwort"], b["fehlt"])


# P6 Schatten + Bestaetigt in FK (t3 Schatten, vbc Bestaetigt), L1b/L2b/L3a, w(FK) = 1/10:
#    L4a: vbc allein -> m = 1/10*9 = 9/10; keine Benchmark; Summe 1.
#    L4b: Summe Faktoren 1+2 = 3 -> vbc 1/10*2/3*9 = 3/5; Benchmark Krypto 1/30; Summe 1.
#    L4c: vbc 9/10; Benchmark Krypto 1/9; Summe 10/9.
#    L4d: Bestaetigt in der Tabelle -> wie L4a.
def p6_l4a(mod):
    e = m_von(mod, S_UND_B, l4="L4a")
    return e["m"][4] == 0 and e["m"][5] == F(9, 10) and e["benchmark"] == (0, 0), "vbc %s" % L.bruch(e["m"][5])


def p6_l4b(mod):
    e = m_von(mod, S_UND_B, l4="L4b")
    return (e["m"][5] == F(3, 5) and e["benchmark"] == (0, F(1, 30)) and e["buchsumme"] == 1,
            "vbc %s, Benchmark K %s" % (L.bruch(e["m"][5]), L.bruch(e["benchmark"][1])))


def p6_l4c(mod):
    e = m_von(mod, S_UND_B, l4="L4c")
    return (e["m"][5] == F(9, 10) and e["benchmark"] == (0, F(1, 9)) and e["buchsumme"] == F(10, 9),
            "Summe %s" % L.bruch(e["buchsumme"]))


def p6_l4d(mod):
    e = m_von(mod, S_UND_B, l4="L4d")
    return e["antwort"] and e["m"][5] == F(9, 10), "vbc %s" % (L.bruch(e["m"][5]) if e["antwort"] else e["fehlt"])


# P7 Schatten + Grundbudget in FK, kein Bestaetigt: L4a gibt vbc 9/10, L4b 9/20 -> L4d ohne Antwort.
def p7(mod):
    e = m_von(mod, S_UND_G, l4="L4d")
    return (not e["antwort"]) and e["fehlt"] == ["L4d"], "fehlt %s" % e.get("fehlt")


# P8 L5b: Bestaetigt zaehlt 1. In FK mit L4b: Faktoren 1+1 -> vbc 1/10*1/2*9 = 9/20, Benchmark 1/20.
def p8(mod):
    e = m_von(mod, S_UND_B, l4="L4b", l5="L5b")
    return e["m"][5] == F(9, 20) and e["benchmark"] == (0, F(1, 20)), "vbc %s" % L.bruch(e["m"][5])


# P9 L1c ungleich L1b, wenn R die Klassen ungleich besetzt: FA, FK, UK aktiv (L2a).
#    L1b: FA 4/5 -> m(VB) = 36/5; FK 1/10 -> 9/20; UK 1/10 -> 3/10.
#    L1c: Nenner 4/5+1/5+1/5 = 6/5 -> FA 2/3 -> m(VB) = 6; FK 1/6 -> 3/4; UK 1/6/3*9 = 1/2.
def p9(mod):
    b = m_von(mod, UNGLEICH, l1="L1b", l2="L2a")
    c = m_von(mod, UNGLEICH, l1="L1c", l2="L2a")
    ok = (b["m"][0] == F(36, 5) and b["m"][4] == F(9, 20)
          and c["m"][0] == F(6) and c["m"][4] == F(3, 4) and c["m"][6] == F(1, 2) and c["buchsumme"] == 1)
    return ok, "m(VB) L1b %s, L1c %s" % (L.bruch(b["m"][0]), L.bruch(c["m"][0]))


# P10 Aufzaehlung: genau 3^9 = 19 683 Tabellen, alle verschieden, je 9 Stufen.
def p10(mod):
    t = mod.alle_tabellen()
    ok = len(t) == 19683 and len(set(t)) == 19683 and all(len(x) == 9 and set(x) <= set(mod.STUFEN) for x in t)
    return ok, "%d Tabellen, %d verschieden" % (len(t), len(set(t)))


# P11 Schreibweise hin und zurueck fuer alle Tabellen.
def p11(mod):
    t = mod.alle_tabellen()
    return all(mod.tabelle_aus_text(mod.tabelle_text(x)) == x for x in t), "Beispiel %s" % mod.tabelle_text(t[1234])


# P12 Die Zellenzuordnung im Werkzeug ist die Tabelle aus 16.4 (g), Register Z. 1972-1975.
def p12(mod):
    zeilen = open(REGISTER, encoding="utf-8").read().split("\n")[1971:1975]
    reg = []
    for z in zeilen:
        teile = [x.strip() for x in z[2:].strip().strip("|").split("|")]
        reg.append((teile[0], tuple(b.strip().strip("`") for b in teile[1].split(","))))
    werk = [(name, bots) for name, _, bots in mod.ZELLEN]
    return reg == werk, "Register %s" % [r[0] for r in reg]


# P13 Pruefung ueber einen Ausschnitt: Zahl der Tabellen und die L1-Unterschiede bei ALLE_G.
def p13(mod):
    t = [mod.tabelle_aus_text(x) for x in (ALLE_G, ALLE_S)]
    p = mod.pruefung(t, [lesart(l1=x, l2="L2b") for x in ("L1a", "L1b", "L1c")])
    klassen = p["unterschiede"]["L1"]
    ok = (p["tabellen"] == 2 and p["stelle_tabellen"]["L1"] == 1
          and sorted(k.split(" | ")[0] for k in klassen) == ["L1a≠L1b", "L1a≠L1c"])
    return ok, "L1-Klassen %s" % sorted(klassen)


# P14 Ausgabe: Text und JSON aus derselben Pruefung wie P13; die Zahl der Tabellen je
#     Unterschiedsklasse steht im Text, das JSON ist serialisierbar und traegt dieselbe Zahl.
def p14(mod):
    import json
    t = [mod.tabelle_aus_text(x) for x in (ALLE_G, ALLE_S)]
    p = mod.pruefung(t, [lesart(l1=x, l2="L2b") for x in ("L1a", "L1b", "L1c")])
    text = mod.als_text(p)
    js = json.loads(json.dumps(mod.als_json(p), ensure_ascii=False))
    zeile = "  L1a≠L1b | aktiv A2/K2, Schatten in aktiver Zelle nein, Bestaetigt nein: 1"
    ok = (zeile in text.split("\n") and js["tabellen_mit_unterschied_je_stelle"]["L1"] == 1
          and js["tabellen"] == 2 and len(js["je_lesart"]) == 3)
    return ok, "Textzeile %s, JSON L1 %s" % (zeile in text.split("\n"), js["tabellen_mit_unterschied_je_stelle"]["L1"])


def main():
    print("== Hand-Beispiele je Lesart, mit Mutationsgegenprobe")
    probe("P1 alle Grundbudget, L1a (L2a/L2b/L2c)", p1,
          'SCHLUESSEL = {"aktien": F(80, 100), "krypto": F(20, 100)}',
          'SCHLUESSEL = {"aktien": F(75, 100), "krypto": F(25, 100)}')
    probe("P2 alle Grundbudget, L1b und L1c", p2,
          "w[c] = K[a] / len(RK)", "w[c] = K[a] / len(R)")
    probe("P3 alle Schatten, Benchmark je Lesart", p3,
          "bench[a] += w[c]                      # (j)", "bench[a] += 0 * w[c]                  # (j)")
    probe("P4 nur Krypto aktiv, L3a/L3b", p4,
          'if l3 == "L3b" and len(klassen_aktiv) == 1:', "if False:")
    probe("P5 nur Krypto aktiv, L2c", p5,
          "bezuege = [aktiv | frozenset(t) for r in", "bezuege = [aktiv][:1] or [aktiv | frozenset(t) for r in")
    probe("P6a Schatten+Bestaetigt, L4a", p6_l4a,
          "summe = sum(faktor[s] for _, s in inhalt)\n", "summe = sum(faktor[s] for _, s in inhalt) + 1\n")
    probe("P6b Schatten+Bestaetigt, L4b", p6_l4b,
          'faktor[s] if s != "schatten" else 1', 'faktor[s] if s != "schatten" else 0')
    probe("P6c Schatten+Bestaetigt, L4c", p6_l4c,
          "bench[a] += NENNER * n_schatten", "bench[a] += 0 * n_schatten")
    probe("P6d Schatten+Bestaetigt, L4d", p6_l4d,
          'if "bestaetigt" in tab:', "if False:")
    probe("P7 Schatten+Grundbudget, L4d ohne Antwort", p7,
          "if e_a != e_b:", "if False:")
    probe("P8 Bestaetigt Faktor 1 (L5b)", p8,
          'faktor["bestaetigt"] = 1', 'faktor["bestaetigt"] = 2')
    probe("P9 L1c ungleich L1b", p9,
          "nenner = sum((K[ANLAGE_VON_ZELLE[c]] for c in R), F(0))", "nenner = F(1)")
    probe("P10 Aufzaehlung 19 683 verschiedene Tabellen", p10,
          "return list(itertools.product(STUFEN, repeat=len(BOTS)))",
          "return list(itertools.product(STUFEN, repeat=len(BOTS))) + [(\"grund\",) * 9]")
    probe("P11 Schreibweise hin und zurueck", p11,
          '"bestaetigt": "B"}', '"bestaetigt": "G"}')
    probe("P12 Zellenzuordnung = Register 16.4 (g)", p12,
          '("t3_supertrend", "volatility_breakout_crypto")', '("volatility_breakout_crypto", "t3_supertrend")')
    probe("P13 Pruefung ueber einen Ausschnitt", p13,
          "if k1 == k2:\n                        continue", "if True:\n                        continue")
    probe("P14 Ausgabe Text und JSON", p14,
          'a("  %s: %d" % (k, v["tabellen"]))', 'a("  %s: %d" % (k, v["tabellen"] + 1))')

    print()
    print("Ergebnis: %d bestanden, %d Fehler" % (_bestanden, len(_fehler)))
    for f in _fehler:
        print("  FEHLER:", f)
    return 1 if _fehler else 0


if __name__ == "__main__":
    sys.exit(main())
