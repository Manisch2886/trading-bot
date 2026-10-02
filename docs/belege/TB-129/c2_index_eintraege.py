#!/usr/bin/env python3
"""TB-129 C2/C3: REGISTER_INDEX.md nach Fable 01a nachziehen (nach c2_index_zeilen.py).

Bauart TB-126 c2_index_eintraege.py: jede Ersetzung hat einen Anker, der im Index genau einmal vorkommen muss,
sonst Abbruch ohne Schreiben. Inhalt: Kopf (Stand, Messhinweis, Verweis auf die Abschnittsdateien),
Abschnittstabelle und Teilgrenzen aus den Koepfen der Abschnittsdateien bzw. aus c1_registerkopie.txt, die
14 Marken aus 01a in den Tabellen 1-4 (Zeilen aus c2_index_01a_tabelle.md, gemessen mit registerkopie.py
--marken), Zeile 51 in Tabelle 4, neuer Abschnitt 6 (Tabelle der 14 Marken und die sechs Indexzeilen aus C3,
gelesen aus dem Auftrag am Commit S0) und der Pflegehinweis.
Regel des Index: PRAEZISIERT gilt als Kette (Spalte "gilt"), ERGAENZT steht unter "dazu".
Die Zeilennummern unten (Marken) stehen auch in c2_index_01a_tabelle.md; das Skript prueft, dass jede dort steht.
Aufruf: trading-env/bin/python3 docs/belege/TB-129/c2_index_eintraege.py <S0>
"""
import glob
import re
import subprocess
import sys

S0 = sys.argv[1]
I = "docs/projektfuehrung/REGISTER_INDEX.md"
BL = "docs/belege/TB-129/"
T6 = open(BL + "c2_index_01a_tabelle.md", encoding="utf-8").read().rstrip("\n")
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-129_register_fable_01a.md" % S0],
                     capture_output=True, text=True, check=True).stdout
C3 = auf.split("**C3. Indexzeilen statt Marken**", 1)[1].split("\n```\n", 2)[1]
assert len(C3.split("\n")) == 6

# Marken-Zeilen, die unten genannt werden, muessen in der gemessenen Tabelle stehen
for z in (83, 522, 525, 816, 887, 890, 2232, 4675, 5190, 9702, 10883, 10933, 10936, 11113):
    assert ("| Z. %d |" % z) in T6, z

# Abschnittstabelle und Teilgrenzen aus den Koepfen der Abschnittsdateien
KOPF = re.compile(r"^# REGISTER-KOPIE Abschnitt (\d+) \(von 0–(\d+)\) — Register-Z\. (\d+)–(\d+) — Commit ([0-9a-f]{40}) — "
                  r"(\d{4}-\d\d-\d\d) — Original sha256 ([0-9a-f]{64}) — ")
ab = {}
for d in sorted(glob.glob("docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_*.md")):
    k = KOPF.match(open(d, encoding="utf-8").readline())
    ab[int(k.group(1))] = (int(k.group(3)), int(k.group(4)), k.group(5), k.group(7))
assert sorted(ab) == list(range(52)), sorted(ab)
commits = {v[2] for v in ab.values()}
shas = {v[3] for v in ab.values()}
assert len(commits) == 1 and len(shas) == 1
commit, sha = commits.pop(), shas.pop()
zeilen_reg = ab[51][1]
teile = []
for s in open(BL + "c1_registerkopie.txt", encoding="utf-8"):
    m = re.match(r"^geschrieben: \S+teil(\d+)\.md  Abschnitte (\d+)–(\d+) ", s)
    if m:
        teile.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
assert [t[0] for t in teile] == [1, 2, 3, 4], teile
vier = ", ".join("T%d = %d–%d (Z. %d–%d)" % (n, a, b, ab[a][0], ab[b][1]) for n, a, b in teile)

text = open(I, encoding="utf-8").read()
alt_tab = re.findall(r"^\| (\d+) \| `REGISTER_KOPIE_ABSCHNITT_\d\d\.md` \| \d+–\d+ \|$", text, re.M)
assert alt_tab == [str(n) for n in range(51)], alt_tab

E = [
# Kopf
("""am Commit `db108a6` (01.10.2026), Abschnitte 0–50,
11 094 Zeilen, sha256 `b5804659…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie `REGISTER_KOPIE_teil1–4.md`.""",
 """am Commit `%s` (02.10.2026), Abschnitte 0–51,
%s Zeilen, sha256 `%s…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2) und TB-129 (Fable 01a). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_51.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–4.md`)."""
 % (commit[:7], "{:,}".format(zeilen_reg).replace(",", " "), sha[:8])),
("(das Suchmuster des Auftrags, Art `MARKE`, 55 Zeilen)", "(das Suchmuster des Auftrags, Art `MARKE`, 64 Zeilen)"),
("(Art `MARKE+`, 98 Zeilen)", "(Art `MARKE+`, 104 Zeilen)"),
("Art `UEBERSCHRIFT`, 76 Zeilen). Die\nAusgabe liegt in `docs/belege/TB-126/c1_marken.txt` (zuvor `docs/belege/TB-118/a4_marken.txt`).",
 "Art `UEBERSCHRIFT`, 80 Zeilen). Die\nAusgabe liegt in `docs/belege/TB-129/c1_marken.txt` (zuvor `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`)."),
("geschnitten mit `docs/werkzeuge/registerkopie_abschnitte.py`,",
 "geschnitten seit TB-127 mit `docs/werkzeuge/registerkopie.py --abschnitte`, zuvor mit `registerkopie_abschnitte.py`;"),
# Tabelle 1
("| 3 Beurteilung | 1, T1 | Z. 77 **PRÄZISIERT durch R48 (48.16)** | 1 **mit** 48.16 R48 (j), T1+T4 | – |",
 "| 3 Beurteilung | 1, T1 | Z. 77 **PRÄZISIERT durch R48 (48.16)**; Z. 83 **PRÄZISIERT durch R36 (48.4)** | 1 **mit** 48.16 R48 (j) **und** 48.4 R36, T1+T4 | – |"),
# Tabelle 2
("| 4.2 | Z. 519 ERGÄNZT (Verweis) durch R51 (48.19) | am Ort; dazu 48.19 R51 (T4) |",
 "| 4.2 | Z. 519 ERGÄNZT (Verweis) durch R51 (48.19); Z. 522 **PRÄZISIERT durch R48 (48.16)**; Z. 525 **PRÄZISIERT durch R60 (51.5)** | 4.2 **mit** 48.16 R48 (d), (e) **und** 51.5 R60; dazu 48.19 R51 (T4) |"),
("| 7, Tabelle (a) und (d) | Z. 807 (d) **PRÄZISIERT durch R48 (48.16)**; Z. 810 (a) ERGÄNZT (Verweis) durch R51 (48.19); Z. 813 (d) ERGÄNZT durch R55 (49.3) | 7 (d) **mit** 48.16 R48 (c); dazu",
 "| 7, Tabelle (a), (b) und (d) | Z. 807 (d) **PRÄZISIERT durch R48 (48.16)**; Z. 810 (a) ERGÄNZT (Verweis) durch R51 (48.19); Z. 813 (d) ERGÄNZT durch R55 (49.3); Z. 816 (b) **PRÄZISIERT durch R37 (48.5)** | 7 (d) **mit** 48.16 R48 (c); 7 (b) **mit** 48.5 R37; dazu"),
("| 8.1 Zufalls-Timing-Test |",
 "| 8, Tabelle (Bericht je Bot) | Z. 887 **PRÄZISIERT durch R36 (48.4)**; Z. 890 ERGÄNZT durch R55 (49.3) | 8, Tabelle **mit** 48.4 R36; dazu 49.3 R55 (T4) |\n| 8.1 Zufalls-Timing-Test |"),
# Tabelle 3
("— Liste in Abschnitt 5 |",
 "— Liste in Abschnitt 5; „Prüfung vor dem Tag“: Z. 2232 **PRÄZISIERT durch R21 (47.4)** — Abschnitt 6 |"),
("für (a)–(d), (h)–(m) (T4) |",
 "für (a)–(d), (h)–(m); „Prüfung vor dem Tag“ **mit** 47.4 R21 (T4) |"),
# Tabelle 4
("25.2: Z. 4652 ERGÄNZT durch R53 (T4) |",
 "25.2: Z. 4652 ERGÄNZT durch R53 (T4); 25.3 (i) ERGÄNZT durch R58 (51.3) (Z. 4675, T4) |"),
("Z. 5187 ERGÄNZT durch R32 (47.15) (T4) |",
 "Z. 5187 ERGÄNZT durch R32 (47.15) (T4); Z. 5190 ERGÄNZT durch R56 (51.1) (T4) |"),
("43.3 → 45.1 R1 „Marke an 43.3 (Bestätigung)“ (T4) |",
 "43.3 → 45.1 R1 „Marke an 43.3 (Bestätigung)“ (T4); 43-7 **PRÄZISIERT durch R33 (48.1)** (Z. 9702, T4) |"),
("48.16 R48 (g) **BERICHTIGT durch R54 (49.2)** (Z. 10880) |",
 "48.16 R48 (g) **BERICHTIGT durch R54 (49.2)** (Z. 10880); 48.16 R48 (d) ERGÄNZT durch R60 (51.5) (Z. 10883) |"),
("| 49 aus 30a | 4 | R53–R55 (49.1–49.3) | – |",
 "| 49 aus 30a | 4 | R53–R55 (49.1–49.3) | 49.1 R53 **PRÄZISIERT durch R57 (51.2)** (Z. 10933), ERGÄNZT durch R59 (51.4) (Z. 10936) |"),
("50.5 Lesart Zählweise (vorläufig); 50.6 Entscheid R24; 50.7 Offenes | – |",
 "50.5 Lesart Zählweise (vorläufig); 50.6 Entscheid R24; 50.7 Offenes | 50.5 ERGÄNZT durch R57 (51.2): die Lesart ist bestätigt (Z. 11113) |\n"
 "| 51 aus 01a | 4 | R56–R62 (51.1–51.7); 51.8 Voraussetzungen; 51.9 Lesart, vorläufig; 51.10 Offenes | – |"),
# Abschnitt 6 und Pflege
("\n\n---\n\n**Pflege:**",
 "\n\n## 6. Die Marken aus Fable 01a (TB-129)\n\n"
 "Alle 14 Marken, die TB-129 gesetzt hat (alle am alten Ort: die zwölf Zeilen aus R61 (b), davon zwei Orte mit je zwei\n"
 "Blöcken), in der Reihenfolge des Registers. Erzeugt mit `docs/belege/TB-129/c2_index_01a.py` aus\n"
 "`docs/belege/TB-129/c1_marken.txt` (Zeile, Art, Teil) und Anhang A des Auftrags TB-129 (alter Ort), nicht abgetippt.\n"
 "In Tabelle 1–4 oben stehen sie zusätzlich an ihrer Stelle. Orte, die R61 (b) nicht aufzählt, tragen keine Marke;\n"
 "sie stehen als Indexzeilen darunter und gehen als Frage an Fable (51.10 Nr. 7).\n\n"
 + T6 + "\n\n### Indexzeilen aus Fable 01a\n\n" + C3 + "\n\n---\n\n**Pflege:**"),
("Zuletzt nachgezogen in TB-126 (01.10.2026):", "In TB-126 (01.10.2026):"),
("23 nach T2, 37 nach T3, 43 nach T4; Einträge mit `c2_index_eintraege.py`.",
 "23 nach T2, 37 nach T3, 43 nach T4; Einträge mit `c2_index_eintraege.py`.\n"
 "Zuletzt nachgezogen in TB-129 (02.10.2026): Zeilenangaben mit `docs/belege/TB-129/c2_index_zeilen.py` vom Stand\n"
 "`db108a6` auf `%s` umgeschrieben (jede Zahl in Listen und Bereichen); Zuschnitt der Teile unverändert, 51 kommt\n"
 "zu T4; Abschnittstabelle aus den Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-129/c2_index_eintraege.py`."
 % commit[:7]),
]
for a, b in E:
    n = text.count(a)
    if n != 1:
        sys.exit("Anker %dx: %r" % (n, a[:80]))
for a, b in E:
    text = text.replace(a, b)

# Abschnittstabelle neu (alle Zeilen aus den Koepfen) und Zeile 51
def tabzeile(n):
    return "| %d | `REGISTER_KOPIE_ABSCHNITT_%02d.md` | %d–%d |" % (n, n, ab[n][0], ab[n][1])
zz = text.split("\n")
for k, s in enumerate(zz):
    m = re.match(r"^\| (\d+) \| `REGISTER_KOPIE_ABSCHNITT_\d\d\.md` \| \d+–\d+ \|$", s)
    if m:
        zz[k] = tabzeile(int(m.group(1)))
        if m.group(1) == "50":
            zz[k] += "\n" + tabzeile(51)
    elif s.startswith("*Frühere Vierteilung*"):
        kopf = s.split("):", 1)[0] + "):"
        zz[k] = kopf + " " + vier + "."
text = "\n".join(zz)
open(I, "w", encoding="utf-8").write(text)
print("Ersetzungen: %d, je Anker genau 1; Abschnittstabelle 0-51 aus den Koepfen; Teile: %s" % (len(E), vier))
