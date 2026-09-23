#!/usr/bin/env python3
"""TB-90 A1-A4 - Nachmessung auf dem Mac (trading-env). NUR LESEND.

Vergleicht a2_plan_vorher.json (vor Block A, 53b35ce) mit dem Plan nach
Block A (argv[1], von plan_dump.py im Speicher gerechnet, nie main()).
"""
import json
import sys

SOLL = "2026-01-01/2026-09-01"
vorher = json.load(open("a2_plan_vorher.json", encoding="utf-8"))
nachher = json.load(open(sys.argv[1], encoding="utf-8"))
fehler = 0

print("A1 - Bezeichner je Bot (Soll: %s bei allen neun)" % SOLL)
n = 0
for bot in sorted(nachher):
    b = nachher[bot]["bestaetigungsperiode"]
    n += b == SOLL
    print("   %-26s %s" % (bot, b))
print("   A1: %s (%d/%d)" % ("BESTANDEN" if n == len(nachher) == 9 else "NICHT BESTANDEN", n, len(nachher)))
fehler += n != 9

print("\nA2 - je Bot: veraenderte Strings (Faltennamen und Plan-Felder)")
for bot in sorted(nachher):
    fv = {f["name"]: f for f in vorher[bot]["falten"]}
    fn = {f["name"]: f for f in nachher[bot]["falten"]}
    weg = [k for k in fv if k not in fn]
    neu = [k for k in fn if k not in fv]
    ungleich = [k for k in fv if k in fn and fv[k] != fn[k]]
    # uebrige Felder des Plans ausser falten/bestaetigungsperiode
    rest = [k for k in set(vorher[bot]) | set(nachher[bot])
            if k not in ("falten", "bestaetigungsperiode")
            and vorher[bot].get(k) != nachher[bot].get(k)]
    # die umbenannte Falte: ausser dem Namen alles gleich?
    feld = []
    if len(weg) == 1 and len(neu) == 1:
        a, b = dict(fv[weg[0]]), dict(fn[neu[0]])
        a.pop("name"); b.pop("name")
        feld = [k for k in set(a) | set(b) if a.get(k) != b.get(k)]
    ok = len(weg) == 1 and len(neu) == 1 and not ungleich and not rest and not feld
    fehler += not ok
    print("   %-26s weg:%s neu:%s gemeinsame ungleich:%d uebrige Planfelder ungleich:%s "
          "Bestaetigungsfalte sonst ungleich:%s -> %s" % (
              bot, weg, neu, len(ungleich), rest or 0, feld or 0, "ok" if ok else "BEFUND"))

print("\nA3 - selektionsfalten ohne Spanne (Schraegstrich)")
for bot in sorted(nachher):
    s = nachher[bot]["selektionsfalten"]
    m = [x for x in s if "/" in x]
    fehler += bool(m) or s != vorher[bot]["selektionsfalten"]
    print("   %-26s %d Falten, mit Schraegstrich: %s, gleich vorher: %s" % (
        bot, len(s), m or "keine", s == vorher[bot]["selektionsfalten"]))

print("\nA4 - embargo_nach_falten der Selektionsfalten")
for bot in sorted(nachher):
    ev = {f["name"]: f["embargo_nach_falten"] for f in vorher[bot]["falten"] if f["rolle"] == "selektion"}
    en = {f["name"]: f["embargo_nach_falten"] for f in nachher[bot]["falten"] if f["rolle"] == "selektion"}
    best = [f["name"] for f in nachher[bot]["falten"] if f["rolle"] == "bestaetigung"]
    in_embargo = any(b in e for e in en.values() for b in best)
    ok = ev == en and not in_embargo
    fehler += not ok
    print("   %-26s %d Selektionsfalten, gleich: %s, Bestaetigungsfalte in einer Embargo-Liste: %s" % (
        bot, len(en), ev == en, in_embargo))

print("\nGESAMT:", "BESTANDEN" if not fehler else "%d BEFUNDE" % fehler)
sys.exit(1 if fehler else 0)
