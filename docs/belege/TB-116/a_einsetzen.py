"""TB-116 A: setzt in a_regeln.md jeden Platzhalter ⟦Z:a-b⟧ durch die Registerzeilen a..b.

Bauart TB-108/TB-110 (Einsetzskript mit Platzhaltern). Laeuft nur, solange noch
Platzhalter stehen; eine zweite Ausfuehrung aendert nichts. Aufruf aus der Repo-Wurzel.
"""
import re

REG = "docs/VORREGISTRIERUNG_neuselektion.md"
ZIEL = "docs/belege/TB-116/a_regeln.md"
reg = open(REG, encoding="utf-8").read().split("\n")
text = open(ZIEL, encoding="utf-8").read()
assert len(reg) == 10035 and reg[-1] == "", "Eingangswache: Register hat nicht 10034 Zeilen"


def ersetze(m):
    a, b = int(m.group(1)), int(m.group(2))
    return "\n".join(reg[a - 1:b])


neu, n = re.subn(r"⟦Z:(\d+)-(\d+)⟧", ersetze, text)
open(ZIEL, "w", encoding="utf-8").write(neu)
print("eingesetzt:", n)
