#!/usr/bin/env python3
"""TB-130 C3: im Block '### Indexzeilen aus Fable 01a' (Abschnitt 6 von REGISTER_INDEX.md) den Schluss
'Ohne Marke; an Fable (51.10 Nr. 7).' je Zeile durch 'Marke gesetzt in TB-130 (R65 (b), 52.3).' ersetzen.
Vorher zaehlen (Soll 5, im ganzen Index und im Block); weicht es ab: nicht ersetzen, vermerken.
Die Zeile 'Tag-Vorbedingungen' bleibt. Aufruf: trading-env/bin/python3 docs/belege/TB-130/c3_indexzeilen.py
"""
import sys

I = "docs/projektfuehrung/REGISTER_INDEX.md"
ALT = "Ohne Marke; an Fable (51.10 Nr. 7)."
NEU = "Marke gesetzt in TB-130 (R65 (b), 52.3)."
text = open(I, encoding="utf-8").read()
kopf = "### Indexzeilen aus Fable 01a\n\n"
assert text.count(kopf) == 1
a = text.index(kopf) + len(kopf)
b = text.index("\n\n", a)
block = text[a:b].split("\n")
gesamt = text.count(ALT)
im_block = sum(1 for s in block if s.endswith(" " + ALT))
print("# TB-130 C3: Indexzeilen aus Fable 01a")
print("vorher: '%s' im Index %dx, als Zeilenschluss im Block %dx (Soll je 5); Zeilen im Block: %d" % (ALT, gesamt, im_block, len(block)))
if gesamt != 5 or im_block != 5:
    print("NICHT ersetzt (Zaehlung weicht ab)")
    sys.exit(1)
neu = [s[:-len(ALT)] + NEU if s.endswith(" " + ALT) else s for s in block]
text = text[:a] + "\n".join(neu) + text[b:]
open(I, "w", encoding="utf-8").write(text)
print("nachher: '%s' %dx (Soll 0), '%s' %dx (Soll 5); Tag-Vorbedingungen unveraendert: %s"
      % (ALT, text.count(ALT), NEU, text.count(NEU), "ja" if block[0] == neu[0] and block[0].startswith("- **Tag-Vorbedingungen**") else "NEIN"))
for s in neu:
    print("  " + s)
