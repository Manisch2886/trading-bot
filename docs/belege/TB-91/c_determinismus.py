#!/usr/bin/env python3
"""TB-91 Block C - Determinismusnachweis (Fable 23b). NUR LESEND.

Laedt benchmark_drawdowns_tb72.json (alt) und die Neurechnung (neu) und
vergleicht je Bot und je Falte JEDEN Wert, rekursiv bis zu den Blaettern.
Einzige zulaessige Abweichung: der Name der Bestaetigungszeile
(alt `2026` bzw. bei elliott_wave `2026-2027`, neu `2026-01-01/2026-09-01`).
Die Zuordnung wird nicht geraten, sondern ueber rolle == "bestaetigung"
bestimmt und dann geprueft, dass alt und neu je GENAU eine solche Falte haben.

Aufruf: python3 c_determinismus.py <alt.json> <neu.json>
Rueckgabe 0 = keine Abweichung ausser dem Namen, 1 = Befund.
"""
import json
import sys

alt = json.load(open(sys.argv[1], encoding="utf-8"))
neu = json.load(open(sys.argv[2], encoding="utf-8"))

ZULAESSIG_ALT = {"2026", "2026-2027"}
ZULAESSIG_NEU = "2026-01-01/2026-09-01"

abweichungen = []   # (bot, ort, feld, alt, neu)
zaehl = {"bots": 0, "falten": 0, "blaetter": 0, "botfelder": 0}
umbenennungen = []


def vergleiche(a, b, bot, ort, pfad):
    """Rekursiver Blattvergleich; zaehlt jedes verglichene Blatt."""
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                abweichungen.append((bot, ort, pfad + [k], "(fehlt)", repr(b[k])[:80]))
            elif k not in b:
                abweichungen.append((bot, ort, pfad + [k], repr(a[k])[:80], "(fehlt)"))
            else:
                vergleiche(a[k], b[k], bot, ort, pfad + [k])
        return
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            abweichungen.append((bot, ort, pfad + ["len"], len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            vergleiche(x, y, bot, ort, pfad + [i])
        return
    zaehl["blaetter"] += 1
    # Typ UND Wert muessen gleich sein (1 == 1.0 zaehlt nicht als gleich)
    if type(a) is not type(b) or a != b:
        abweichungen.append((bot, ort, pfad, repr(a), repr(b)))


if sorted(alt) != sorted(neu):
    abweichungen.append(("-", "Botmenge", [], sorted(alt), sorted(neu)))

for bot in sorted(set(alt) & set(neu)):
    zaehl["bots"] += 1
    a, b = alt[bot], neu[bot]
    # Botfelder ausser falten
    for k in sorted((set(a) | set(b)) - {"falten"}):
        zaehl["botfelder"] += 1
        if k not in a or k not in b:
            abweichungen.append((bot, "Bot", [k], repr(a.get(k, "(fehlt)")), repr(b.get(k, "(fehlt)"))))
        else:
            vergleiche(a[k], b[k], bot, "Bot", [k])
    fa, fb = a["falten"], b["falten"]
    best_a = [n for n, v in fa.items() if v.get("rolle") == "bestaetigung"]
    best_b = [n for n, v in fb.items() if v.get("rolle") == "bestaetigung"]
    zuordnung = {}
    if len(best_a) == 1 and len(best_b) == 1:
        na, nb = best_a[0], best_b[0]
        if na in ZULAESSIG_ALT and nb == ZULAESSIG_NEU:
            zuordnung[na] = nb
            umbenennungen.append((bot, na, nb))
        elif na != nb:
            abweichungen.append((bot, "Bestaetigungsname", [], na, nb))
    else:
        abweichungen.append((bot, "Bestaetigungszahl", [], best_a, best_b))
    namen_b = set(fb)
    for na in fa:
        nb = zuordnung.get(na, na)
        if nb not in fb:
            abweichungen.append((bot, "Falte", [na], "(da)", "(fehlt)"))
            continue
        namen_b.discard(nb)
        zaehl["falten"] += 1
        vergleiche(fa[na], fb[nb], bot, f"Falte {na}->{nb}" if na != nb else f"Falte {na}", [])
    for nb in sorted(namen_b):
        abweichungen.append((bot, "Falte", [nb], "(fehlt)", "(da)"))

print("C1 Zaehlung des Verglichenen:")
print(f"  Bots: {zaehl['bots']}   Falten: {zaehl['falten']}   Botfelder (ohne falten): "
      f"{zaehl['botfelder']}   Blattwerte gesamt: {zaehl['blaetter']}")
print("\nZulaessige Umbenennung der Bestaetigungszeile:")
for bot, na, nb in umbenennungen:
    print(f"  {bot:28s} {na!r:14s} -> {nb!r}")
print(f"  ({len(umbenennungen)} von {zaehl['bots']})")

print("\nC2 Abweichungen ausser dem Namen:", len(abweichungen))
for bot, ort, feld, x, y in abweichungen[:500]:
    print(f"  {bot} | {ort} | {'/'.join(map(str, feld))} | alt {x} | neu {y}")
if len(abweichungen) > 500:
    print(f"  ... {len(abweichungen) - 500} weitere")

print("\nC3 dd_toleranz je Bot:")
for bot in sorted(set(alt) & set(neu)):
    ta, tb = alt[bot]["dd_toleranz"], neu[bot]["dd_toleranz"]
    print(f"  {bot:28s} {'gleich' if ta == tb else 'VERSCHIEDEN'}  ({len(ta)} Stufen; "
          f"0.25/0.50/1.00 alt {ta.get('0.25')}/{ta.get('0.50')}/{ta.get('1.00')} "
          f"neu {tb.get('0.25')}/{tb.get('0.50')}/{tb.get('1.00')})")

print("\nC4 status:")
st = {bot: neu[bot].get("status") for bot in neu}
for bot, s in sorted(st.items()):
    print(f"  {bot:28s} neu {s}   alt {alt.get(bot, {}).get('status')}")
print(f"  endgueltig: {sum(s == 'endgueltig' for s in st.values())} von {len(st)}")

print("\nERGEBNIS:", "REPRODUZIERT - einzige Abweichung der Name der Bestaetigungszeile"
      if not abweichungen else "BEFUND - Abweichungen ausser dem Namen")
sys.exit(0 if not abweichungen else 1)
