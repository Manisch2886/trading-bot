#!/usr/bin/env python3
"""TB-136 C3: im neuen Abschnitt 9 von REGISTER_INDEX.md den Block '### Indexzeilen aus Fable 04a' mit genau den zwei
Zeilen aus C3 des Auftrags (am Commit S0, erster ```-Codeblock nach '**C3. Indexzeilen aus Fable 04a (R77 (b) und (c)).**')
einsetzen, nach der Markentabelle von Abschnitt 9, vor der Trennlinie '---' und dem Pflegeblock (Bauart TB-129:
Block unter der Tabelle des neuen Abschnitts). Vorher zaehlen: 'Indexzeilen aus Fable 04a' Soll 0; weicht es ab,
nicht einsetzen, vermerken.
Aufruf: trading-env/bin/python3 docs/belege/TB-136/c3_indexzeilen.py <S0>
"""
import subprocess
import sys

S0 = sys.argv[1]
I = "docs/projektfuehrung/REGISTER_INDEX.md"
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-136_register_fable_04a.md" % S0],
                     capture_output=True, text=True, check=True).stdout
C3 = auf.split("**C3. Indexzeilen aus Fable 04a (R77 (b) und (c)).**", 1)[1].split("\n```\n", 2)[1]
zeilen = C3.split("\n")
assert len(zeilen) == 2 and all(s.startswith("- **") for s in zeilen), zeilen
text = open(I, encoding="utf-8").read()
KOPF8 = "## 9. Die Marken aus Fable 04a (TB-136)"
SCHLUSS = "\n\n---\n\n**Pflege:**"
print("# TB-136 C3: Indexzeilen aus Fable 04a (Auftrag am Commit %s)" % S0)
vorher = text.count("Indexzeilen aus Fable 04a")
print("vorher: 'Indexzeilen aus Fable 04a' %dx (Soll 0); Abschnitt 9 %dx (Soll 1); Schluss vor Pflege %dx (Soll 1)"
      % (vorher, text.count(KOPF8), text.count(SCHLUSS)))
if vorher != 0 or text.count(KOPF8) != 1 or text.count(SCHLUSS) != 1:
    print("NICHT eingesetzt (Zaehlung weicht ab)")
    sys.exit(1)
assert text.index(KOPF8) < text.index(SCHLUSS)
text = text.replace(SCHLUSS, "\n\n### Indexzeilen aus Fable 04a\n\n" + C3 + SCHLUSS)
open(I, "w", encoding="utf-8").write(text)
print("nachher: '### Indexzeilen aus Fable 04a' %dx (Soll 1); Zeilen zeichengleich im Index: %d/2"
      % (text.count("### Indexzeilen aus Fable 04a"), sum(text.count("\n" + s + "\n") == 1 for s in zeilen)))
for s in zeilen:
    print("  " + s)
