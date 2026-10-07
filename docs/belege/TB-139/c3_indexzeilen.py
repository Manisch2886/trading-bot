#!/usr/bin/env python3
"""TB-139 C3: im neuen Abschnitt 10 von REGISTER_INDEX.md den Block '### Indexzeilen aus Fable 07a' mit genau den drei
Zeilen aus C3 des Auftrags (am Commit S0, erster ```-Codeblock nach '**C3. Indexzeilen aus Fable 07a (R80 (b)).**')
einsetzen, nach der Markentabelle von Abschnitt 10, vor der Trennlinie '---' und dem Pflegeblock (Bauart TB-129:
Block unter der Tabelle des neuen Abschnitts). Vorher zaehlen: 'Indexzeilen aus Fable 07a' Soll 0; weicht es ab,
nicht einsetzen, vermerken.
Aufruf: trading-env/bin/python3 docs/belege/TB-139/c3_indexzeilen.py <S0>
"""
import subprocess
import sys

S0 = sys.argv[1]
I = "docs/projektfuehrung/REGISTER_INDEX.md"
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-139_register_fable_07a.md" % S0],
                     capture_output=True, text=True, check=True).stdout
C3 = auf.split("**C3. Indexzeilen aus Fable 07a (R80 (b)).**", 1)[1].split("\n```\n", 2)[1]
zeilen = C3.split("\n")
assert len(zeilen) == 3 and all(s.startswith("- **") for s in zeilen), zeilen
text = open(I, encoding="utf-8").read()
KOPF8 = "## 10. Die Marken aus Fable 07a (TB-139)"
SCHLUSS = "\n\n---\n\n**Pflege:**"
print("# TB-139 C3: Indexzeilen aus Fable 07a (Auftrag am Commit %s)" % S0)
vorher = text.count("Indexzeilen aus Fable 07a")
print("vorher: 'Indexzeilen aus Fable 07a' %dx (Soll 0); Abschnitt 10 %dx (Soll 1); Schluss vor Pflege %dx (Soll 1)"
      % (vorher, text.count(KOPF8), text.count(SCHLUSS)))
if vorher != 0 or text.count(KOPF8) != 1 or text.count(SCHLUSS) != 1:
    print("NICHT eingesetzt (Zaehlung weicht ab)")
    sys.exit(1)
assert text.index(KOPF8) < text.index(SCHLUSS)
text = text.replace(SCHLUSS, "\n\n### Indexzeilen aus Fable 07a\n\n" + C3 + SCHLUSS)
open(I, "w", encoding="utf-8").write(text)
print("nachher: '### Indexzeilen aus Fable 07a' %dx (Soll 1); Zeilen zeichengleich im Index: %d/3"
      % (text.count("### Indexzeilen aus Fable 07a"), sum(text.count("\n" + s + "\n") == 1 for s in zeilen)))
for s in zeilen:
    print("  " + s)
