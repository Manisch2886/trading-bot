import re, pathlib, sys
N = pathlib.Path("docs/projektfuehrung/nachtraege")
JP = pathlib.Path("docs/projektfuehrung/JOURNAL.md")
J = JP.read_text(encoding="utf-8")
ANKER = "## Wiederkehrende Lehren\n"
assert J.count(ANKER) == 1, "Anker nicht genau einmal"

def quelle(name): return f"*Quelle: `docs/projektfuehrung/nachtraege/{name}`*"
def demote(body):
    body = re.sub(r"(?m)^### ", "#### ", body)
    body = re.sub(r"(?m)^## ", "### ", body)
    return body
def nach_titel(txt):
    lines = txt.split("\n"); assert lines[0].startswith("# ")
    return "\n".join(lines[1:]).lstrip("\n")

# --- (m): T-Zeilen zeichengleich
M = (N/"BACKLOG_NACHTRAG_2026-09-19m.md").read_text(encoding="utf-8")
def tzeilen(prefix):
    z = [l for l in M.split("\n") if re.match(r"^\| \*\*"+prefix+r"\d\*\* \|", l)]
    return z
T53, T58, T58b = tzeilen("T53\\."), tzeilen("T58\\."), tzeilen("T58b\\.")
assert (len(T53),len(T58),len(T58b)) == (4,6,3), (len(T53),len(T58),len(T58b))
def ttab(z, tb):
    return ("#### Das Messprotokoll aus Nachtrag (m), Block `2s` — zeichengleich übernommen\n\n"
            f"*{len(z)} Zeilen zu {tb}, gemessen am 19.09.2026; sie standen bis TB-67 in keinem Führungsdokument.*\n\n"
            "| # | Punkt |\n|---|---|\n" + "\n".join(z) + "\n")

bloecke = []  # (buchstabe, text)
# --- (f)
F = (N/"JOURNAL_NACHTRAG_2026-09-19f.md").read_text(encoding="utf-8")
teile = F.split("\n---\n")
# teile[0] Kopf, dann Bloecke getrennt durch ---
assert teile[1].lstrip().startswith("## Block ⟨nächster⟩ — TB-53b"), teile[1][:60]
assert teile[2].lstrip().startswith("## Block ⟨danach⟩ — TB-58:"), teile[2][:60]
assert teile[3].lstrip().startswith("## Block ⟨danach⟩ — TB-58b"), teile[3][:60]
assert teile[4].lstrip().startswith("## Was der Nachmittag"), teile[4][:60]
assert len(teile) == 7, len(teile)
QF = quelle("JOURNAL_NACHTRAG_2026-09-19f.md") + "\n" + "*Messprotokoll: `docs/projektfuehrung/nachtraege/BACKLOG_NACHTRAG_2026-09-19m.md`, Block `2s`*"
def fblock(buch, kopf, teil, ttext, extra=""):
    body = teil.strip("\n")
    body = re.sub(r"^## Block ⟨[^⟩]+⟩ — ", "", body)
    first, rest = body.split("\n", 1)
    return f"## {buch} — {kopf}\n\n{QF}\n\n{rest.strip()}\n\n{ttext}{extra}"
bk = fblock("BK", "TB-53b: der Resolver erreicht die Selektionsseite (19.09.2026)", teile[1], ttab(T53, "TB-53b"))
bl = fblock("BL", "TB-58: Codeherkunft und Lock (19.09.2026)", teile[2], ttab(T58, "TB-58"))
nachmittag = "\n---\n".join(teile[4:]).strip("\n")
nachmittag = re.sub(r"(?m)^## Was der Nachmittag", "### Was der Nachmittag", nachmittag)
bm = fblock("BM", "TB-58b: Abschnitte 19 und 20 — und was der Nachmittag des 19.09. über die Arbeitsweise ergab", teile[3], ttab(T58b, "TB-58b"), "\n---\n\n" + nachmittag)
bloecke += [("BK", bk), ("BL", bl), ("BM", bm)]

# --- die uebrigen sieben
plan = [
 ("BN", "JOURNAL_NACHTRAG_2026-09-19g.md", "TB-59: die Backlog-Einarbeitung (19./20.09.2026, nachgeholt)"),
 ("BO", "JOURNAL_NACHTRAG_2026-09-20a.md", "TB-60: das Backlog-Archiv (20.09.2026, nachgeholt)"),
 ("BP", "JOURNAL_NACHTRAG_2026-09-20b.md", "Die Beauftragung von TB-61 und TB-62 (Chat-Sitzung, 20.09.2026, Mittag)"),
 ("BQ", "JOURNAL_NACHTRAG_2026-09-20c.md", "TB-61: die Benchmark-Tabelle für neun Bots, und drei Befunde, die keiner bestellt hat (20.09.2026)"),
 ("BR", "JOURNAL_NACHTRAG_2026-09-20d.md", "TB-65: welche Schranke für den Benchmark gilt — und was das Register dazu wirklich sagt (20.09.2026)"),
 ("BS", "JOURNAL_NACHTRAG_2026-09-20e.md", "TB-62: die Nachträge (m) und (v), und das Ende der ZIP-Pflicht (20.09.2026)"),
 ("BT", "JOURNAL_NACHTRAG_2026-09-20f.md", "TB-66: der Benchmark wird tagesgenau — Fables Festlegung VT im Register, im Code und im Lauf (20.09.2026)"),
]
for buch, name, kopf in plan:
    txt = (N/name).read_text(encoding="utf-8")
    body = demote(nach_titel(txt)).strip("\n")
    bloecke.append((buch, f"## {buch} — {kopf}\n\n{quelle(name)}\n\n{body}\n"))

neu = "\n---\n\n".join(t.rstrip("\n") + "\n" for _, t in bloecke) + "\n---\n\n"
# --- Quellenzeilen bei BG-BJ nachtragen (nur Einfuegen)
nachtraege_alt = {
 "## BG — TB-55: die Sitzung, deren Ergebnis ein Nichthandeln ist\n": "JOURNAL_NACHTRAG_2026-09-19c.md",
 "## BH — TB-55: der Eingabezustand existiert\n": "JOURNAL_NACHTRAG_2026-09-19d.md",
 "## BI — TB-55b: der Snapshot steht im Register\n": "JOURNAL_NACHTRAG_2026-09-19e.md",
 "## BJ — TB-54: acht Nachträge, eine Rückfrage\n": "JOURNAL_NACHTRAG_2026-09-19e.md",
}
for kopf, name in nachtraege_alt.items():
    assert J.count(kopf) == 1, kopf
    J = J.replace(kopf, kopf + "\n" + quelle(name) + "\n")
J = J.replace(ANKER, neu + ANKER)
JP.write_text(J, encoding="utf-8")
print("Bloecke:", [b for b,_ in bloecke])
