#!/usr/bin/env python3
"""TB-132 C2: REGISTER_INDEX.md nach Fable 02c nachziehen (nach c2_index_zeilen.py).

Vorlage docs/belege/TB-130/c2_index_eintraege.py (dort Bauart TB-129): jede Ersetzung hat einen Anker, der im Index
genau einmal vorkommen muss, sonst Abbruch ohne Schreiben. Inhalt: Kopf (Stand, Messhinweis, Verweis auf die
Abschnittsdateien bis _53.md), "Wie gemessen" (Zahlen je Art aus c1_marken.txt), Abschnittstabelle und Teilgrenzen
aus den Koepfen der Abschnittsdateien bzw. aus c1_registerkopie.txt, die 21 Marken aus 02c in Tabelle 3 (15.3 (a),
15.3 (c)) und Tabelle 4 (23, 27, 48, 51, 52), Zeile 53 in Tabelle 4, neuer Abschnitt 8 (Tabelle aus
c2_index_02c_tabelle.md) und der Pflegehinweis. Die Indexzeilen aus Fable 02c setzt c3_indexzeilen.py (C3).
Die Zeilen der Marken nachher kommen aus a4_eintrag_daten.json (Nummer der Marke -> Zeile) und werden gegen die
Tabelle aus c1_marken.txt geprueft.
Regel des Index: PRAEZISIERT und BERICHTIGT fett, ERGAENZT nicht.
Aufruf: trading-env/bin/python3 docs/belege/TB-132/c2_index_eintraege.py <S0> <commit_A>
"""
import glob
import json
import re
import sys

S0, CA = sys.argv[1], sys.argv[2]
I = "docs/projektfuehrung/REGISTER_INDEX.md"
BL = "docs/belege/TB-132/"
T8 = open(BL + "c2_index_02c_tabelle.md", encoding="utf-8").read().rstrip("\n")
Z = {m["nr"]: m["zeile_neu"] for m in json.load(open(BL + "a4_eintrag_daten.json", encoding="utf-8"))["marken"]}
assert sorted(Z) == list(range(1, 22))
for z in Z.values():
    assert ("| Z. %d |" % z) in T8, z

# Zahlen je Art aus registerkopie.py --marken
c1m = open(BL + "c1_marken.txt", encoding="utf-8").read()
art = {a: len(re.findall(r"^\s*\d+ \| [^|]+ \| [^|]+ \| %s \|" % re.escape(a), c1m, re.M)) for a in ("MARKE", "MARKE+", "UEBERSCHRIFT")}

# Abschnittstabelle und Teilgrenzen aus den Koepfen der Abschnittsdateien
KOPF = re.compile(r"^# REGISTER-KOPIE Abschnitt (\d+) \(von 0–(\d+)\) — Register-Z\. (\d+)–(\d+) — Commit ([0-9a-f]{40}) — "
                  r"(\d{4}-\d\d-\d\d) — Original sha256 ([0-9a-f]{64}) — ")
ab = {}
for d in sorted(glob.glob("docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_*.md")):
    k = KOPF.match(open(d, encoding="utf-8").readline())
    ab[int(k.group(1))] = (int(k.group(3)), int(k.group(4)), k.group(5), k.group(7))
assert sorted(ab) == list(range(54)), sorted(ab)
commits = {v[2] for v in ab.values()}
shas = {v[3] for v in ab.values()}
assert len(commits) == 1 and len(shas) == 1
commit, sha = commits.pop(), shas.pop()
assert commit.startswith(CA), (commit, CA)
zeilen_reg = ab[53][1]
teile = []
for s in open(BL + "c1_registerkopie.txt", encoding="utf-8"):
    m = re.match(r"^geschrieben: \S+teil(\d+)\.md  Abschnitte (\d+)–(\d+) ", s)
    if m:
        teile.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
assert [t[0] for t in teile] == list(range(1, len(teile) + 1)), teile
vier = ", ".join("T%d = %d–%d (Z. %d–%d)" % (n, a, b, ab[a][0], ab[b][1]) for n, a, b in teile)
t53 = next(n for n, a, b in teile if a <= 53 <= b)
T = "T%d" % t53

text = open(I, encoding="utf-8").read()
alt_tab = re.findall(r"^\| (\d+) \| `REGISTER_KOPIE_ABSCHNITT_\d\d\.md` \| \d+–\d+ \|$", text, re.M)
assert alt_tab == [str(n) for n in range(53)], alt_tab

E = [
# Kopf
("""am Commit `ad351d5` (02.10.2026), Abschnitte 0–52,
11 313 Zeilen, sha256 `a7496780…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a) und TB-130 (Fable 02a). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_52.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–4.md`).""",
 """am Commit `%s` (04.10.2026), Abschnitte 0–53,
%s Zeilen, sha256 `%s…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a) und TB-132 (Fable 02c). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_53.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–%d.md`)."""
 % (commit[:7], "{:,}".format(zeilen_reg).replace(",", " "), sha[:8], len(teile))),
# Wie gemessen
("(das Suchmuster des Auftrags, Art `MARKE`, 70 Zeilen)", "(das Suchmuster des Auftrags, Art `MARKE`, %d Zeilen)" % art["MARKE"]),
("(Art `MARKE+`, 111 Zeilen)", "(Art `MARKE+`, %d Zeilen)" % art["MARKE+"]),
("Art `UEBERSCHRIFT`, 82 Zeilen). Die\nAusgabe liegt in `docs/belege/TB-130/c1_marken.txt` (zuvor `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`).",
 "Art `UEBERSCHRIFT`, %d Zeilen). Die\nAusgabe liegt in `docs/belege/TB-132/c1_marken.txt` (zuvor `docs/belege/TB-130/c1_marken.txt`, `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`)."
 % art["UEBERSCHRIFT"]),
# Tabelle 3, 15.3 (a) und 15.3 (c)
("| **1a** Bootstrap (a) | 15.3 (a) | – | **15.3 (a)** |",
 "| **1a** Bootstrap (a) | 15.3 (a) | Z. %d **PRÄZISIERT durch R66 (53.1)** | **15.3 (a)** **mit** 53.1 R66 (a), (b) (%s) |" % (Z[1], T)),
("| **1c** | 15.3 (c) | – | **15.3 (c)** |",
 "| **1c** | 15.3 (c) | Z. %d **PRÄZISIERT durch R66 (53.1)** | **15.3 (c)** **mit** 53.1 R66 (c) (%s) |" % (Z[2], T)),
# Abschnitt 8 und Pflege
("\n\n---\n\n**Pflege:**",
 "\n\n## 8. Die Marken aus Fable 02c (TB-132)\n\n"
 "Alle 21 Marken, die TB-132 gesetzt hat (alle am alten Ort: 20 nach R70 (c), eine an 23.3, Registertext 3b (c), vom\n"
 "steuernden Chat nach R65 (a) bestimmt; 52.2 trägt fünf), in der Reihenfolge des Registers. Erzeugt mit\n"
 "`docs/belege/TB-132/c2_index_02c.py` aus `docs/belege/TB-132/c1_marken.txt` (Zeile, Art, Teil) und Anhang A des\n"
 "Auftrags TB-132 (alter Ort), nicht abgetippt. In Tabelle 3 und 4 oben stehen sie zusätzlich an ihrer Stelle. Keine\n"
 "Marke tragen Abschnitt 9, Abschnitt 10 und der ERZEUGT-Block von Abschnitt 3; ohne Marke bleiben 7 (c), 17.5 und\n"
 "50.7 Nr. 3 (R70 (b), Indexzeilen darunter) sowie 24.2 und 29.3 (R70 (c)).\n\n"
 + T8 + "\n\n---\n\n**Pflege:**"),
("Zuletzt nachgezogen in TB-130 (02.10.2026):", "In TB-130 (02.10.2026):"),
("Indexzeilen ohne Marke auf die in TB-130 gesetzten Marken umgestellt (`c3_indexzeilen.py`).",
 "Indexzeilen ohne Marke auf die in TB-130 gesetzten Marken umgestellt (`c3_indexzeilen.py`).\n"
 "Zuletzt nachgezogen in TB-132 (04.10.2026): Zeilenangaben mit `docs/belege/TB-132/c2_index_zeilen.py` vom Stand\n"
 "`ad351d5` auf `%s` umgeschrieben (jede Zahl in Listen und Bereichen); 53 kommt zu %s; Abschnittstabelle aus den\n"
 "Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-132/c2_index_eintraege.py`; neuer Abschnitt 8 mit den\n"
 "21 Marken und den drei Indexzeilen nach R70 (b) (`c3_indexzeilen.py`)."
 % (commit[:7], T)),
]
for a, b in E:
    n = text.count(a)
    if n != 1:
        sys.exit("Anker %dx: %r" % (n, a[:80]))
for a, b in E:
    text = text.replace(a, b)

# Tabelle 4: Zeilen an ihrem Anfang finden (genau eine), Zusatz vor dem Schluss ' |' bzw. statt '| – |'
ANH = [
("| 23 Benchmark tagesgenau |", "anhaengen",
 "; 23.3, Registertext 3b (c) **PRÄZISIERT durch R72 (53.7)** (Z. %d, vom steuernden Chat nach R65 (a) bestimmt, %s); "
 "23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse **BERICHTIGT durch R71 (53.6)** (Z. %d), ERGÄNZT durch R72 (53.7) (Z. %d) (%s)"
 % (Z[3], T, Z[4], Z[5], T)),
("| 27 Sichtschutz |", "anhaengen",
 "; Z. %d ERGÄNZT durch R73 (53.8) (%s)" % (Z[6], T)),
("| 48 aus 29b |", "anhaengen",
 "; 48.1 R33 **PRÄZISIERT durch R68 (53.3)** (Z. %d); 48.5 R37 **PRÄZISIERT durch R68 (53.3)** (Z. %d); "
 "48.7 R39 ERGÄNZT durch R67 (53.2) (Z. %d) und durch R69 (53.4): R39 ist bestätigt (Z. %d); 48.16 R48 (d) ERGÄNZT durch R72 (53.7) (Z. %d)"
 % (Z[7], Z[8], Z[9], Z[10], Z[11])),
("| 51 aus 01a |", "anhaengen",
 "; 51.5 R60 **PRÄZISIERT durch R69 (53.4)** (Z. %d); 51.6 R61 **PRÄZISIERT durch R70 (53.5)** (Z. %d)" % (Z[12], Z[13])),
("| 52 aus 02a |", "ersetzen",
 "52.2 R64 ERGÄNZT durch R66 (53.1), zu (e) (Z. %d); 52.2 R64 **PRÄZISIERT durch R68 (53.3)** (Z. %d), **durch R69 (53.4)** (Z. %d), "
 "**durch R71 (53.6): erster Kurstag** (Z. %d) und **durch R72 (53.7): Benchmark-Tag** (Z. %d); 52.3 R65 **PRÄZISIERT durch R70 (53.5)** (Z. %d); "
 "52.4, Zeile „R64 (52.2), zweite“ ERGÄNZT durch R66 (53.1) (Z. %d); 52.4, Zeile „R64 (52.2) (a)“ **BERICHTIGT durch R69 (53.4)** (Z. %d)"
 % (Z[14], Z[15], Z[16], Z[17], Z[18], Z[19], Z[20], Z[21])),
]
zz = text.split("\n")
for prefix, wie, zus in ANH:
    t = [k for k, s in enumerate(zz) if s.startswith(prefix)]
    if len(t) != 1:
        sys.exit("Tabellenzeile %dx: %r" % (len(t), prefix))
    s = zz[t[0]]
    assert s.endswith(" |"), prefix
    if wie == "ersetzen":
        assert s.endswith("| – |"), (prefix, s[-20:])
        zz[t[0]] = s[:-len("– |")] + zus + " |"
    else:
        assert not s.endswith("| – |"), prefix
        zz[t[0]] = s[:-2] + zus + " |"
    if prefix == "| 52 aus 02a |":
        zz[t[0]] += "\n| 53 aus 02c | %d | R66–R73 (53.1–53.8); 53.9 Voraussetzungen und Befunde; 53.10 Offenes | – |" % t53

# Abschnittstabelle neu (alle Zeilen aus den Koepfen) und Zeile 53; Teilgrenzen
def tabzeile(n):
    return "| %d | `REGISTER_KOPIE_ABSCHNITT_%02d.md` | %d–%d |" % (n, n, ab[n][0], ab[n][1])
zz = "\n".join(zz).split("\n")
for k, s in enumerate(zz):
    m = re.match(r"^\| (\d+) \| `REGISTER_KOPIE_ABSCHNITT_\d\d\.md` \| \d+–\d+ \|$", s)
    if m:
        zz[k] = tabzeile(int(m.group(1)))
        if m.group(1) == "52":
            zz[k] += "\n" + tabzeile(53)
    elif s.startswith("*Frühere Vierteilung*"):
        kopf = s.split("):", 1)[0] + "):"
        zz[k] = kopf + " " + vier + "."
text = "\n".join(zz)
open(I, "w", encoding="utf-8").write(text)
print("Ersetzungen: %d, Tabellenzeilen: %d, je Anker genau 1; Abschnittstabelle 0-53 aus den Koepfen; Teile: %s; Arten %s"
      % (len(E), len(ANH), vier, art))
