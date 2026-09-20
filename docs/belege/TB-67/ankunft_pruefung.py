"""TB-67 Nachweis: jede Zeile jedes Journal-Nachtrags steht im Journal
(Ueberschriften um eine Stufe abgesenkt); die T-Zeilen aus Nachtrag (m)
zeichengleich; die B-Zeilen absichtlich NICHT. Aufruf aus der Repo-Wurzel."""
import re, pathlib
J = pathlib.Path("docs/projektfuehrung/JOURNAL.md").read_text(encoding="utf-8")
N = pathlib.Path("docs/projektfuehrung/nachtraege")
koepfe = re.findall(r"(?m)^## ([A-Z]{1,2}) — ", J)
print("Bloecke:", len(koepfe), "letzter:", koepfe[-1], "doppelt:", [k for k in set(koepfe) if koepfe.count(k) > 1])
for f in sorted(list(N.glob("JOURNAL_NACHTRAG_*.md")) + list((N / "_eingearbeitet").glob("JOURNAL_NACHTRAG_*.md"))):
    lines = f.read_text(encoding="utf-8").split("\n")[1:]
    fehl = []
    for l in lines:
        if not l.strip() or l.startswith("## Block ⟨"):
            continue
        cands = {l, re.sub(r"^### ", "#### ", l), re.sub(r"^## ", "### ", l)}
        if not any(c in J for c in cands):
            fehl.append(l)
    print(f.name, "Zeilen:", sum(1 for l in lines if l.strip()), "fehlend:", len(fehl))
    for x in fehl:
        print("   ", x[:110])
m = N / "BACKLOG_NACHTRAG_2026-09-19m.md"
if not m.exists():
    m = N / "_eingearbeitet" / m.name
M = m.read_text(encoding="utf-8")
tz = [l for l in M.split("\n") if re.match(r"^\| \*\*T5", l)]
bz = [l for l in M.split("\n") if re.match(r"^\| \*\*B\d\*\*", l)]
print("T-Zeilen in (m):", len(tz), "im Journal zeichengleich:", sum(l in J for l in tz))
print("B-Zeilen in (m):", len(bz), "im Journal zeichengleich:", sum(l in J for l in bz), "(Soll 0: nicht als Regel eingetragen)")
print("Quellenzeilen:", len(re.findall(r"(?m)^\*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_", J)))
