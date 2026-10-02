#!/usr/bin/env python3
"""TB-130 C2: REGISTER_INDEX.md nach Fable 02a nachziehen (nach c2_index_zeilen.py).

Bauart TB-129 c2_index_eintraege.py: jede Ersetzung hat einen Anker, der im Index genau einmal vorkommen muss,
sonst Abbruch ohne Schreiben. Inhalt: Kopf (Stand, Messhinweis, Verweis auf die Abschnittsdateien bis _52.md),
"Wie gemessen" (Zahlen je Art aus c1_marken.txt), Abschnittstabelle und Teilgrenzen aus den Koepfen der
Abschnittsdateien bzw. aus c1_registerkopie.txt, die 12 Marken aus 02a in Tabelle 2 (4.2) und Tabelle 4
(25, 47, 48, 50, 51), Zeile 52 in Tabelle 4, neuer Abschnitt 7 (Tabelle aus c2_index_02a_tabelle.md) und der
Pflegehinweis. Die Zeilen der Marken nachher kommen aus a4_eintrag_daten.json (Nummer der Marke -> Zeile) und
werden gegen die Tabelle aus c1_marken.txt geprueft.
Regel des Index: PRAEZISIERT und BERICHTIGT fett, ERGAENZT nicht.
Aufruf: trading-env/bin/python3 docs/belege/TB-130/c2_index_eintraege.py <S0> <commit_A>
"""
import glob
import json
import re
import sys

S0, CA = sys.argv[1], sys.argv[2]
I = "docs/projektfuehrung/REGISTER_INDEX.md"
BL = "docs/belege/TB-130/"
T7 = open(BL + "c2_index_02a_tabelle.md", encoding="utf-8").read().rstrip("\n")
Z = {m["nr"]: m["zeile_neu"] for m in json.load(open(BL + "a4_eintrag_daten.json", encoding="utf-8"))["marken"]}
assert sorted(Z) == list(range(1, 13))
for z in Z.values():
    assert ("| Z. %d |" % z) in T7, z

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
assert sorted(ab) == list(range(53)), sorted(ab)
commits = {v[2] for v in ab.values()}
shas = {v[3] for v in ab.values()}
assert len(commits) == 1 and len(shas) == 1
commit, sha = commits.pop(), shas.pop()
assert commit.startswith(CA), (commit, CA)
zeilen_reg = ab[52][1]
teile = []
for s in open(BL + "c1_registerkopie.txt", encoding="utf-8"):
    m = re.match(r"^geschrieben: \S+teil(\d+)\.md  Abschnitte (\d+)–(\d+) ", s)
    if m:
        teile.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
assert [t[0] for t in teile] == [1, 2, 3, 4], teile
vier = ", ".join("T%d = %d–%d (Z. %d–%d)" % (n, a, b, ab[a][0], ab[b][1]) for n, a, b in teile)
t52 = next(n for n, a, b in teile if a <= 52 <= b)

text = open(I, encoding="utf-8").read()
alt_tab = re.findall(r"^\| (\d+) \| `REGISTER_KOPIE_ABSCHNITT_\d\d\.md` \| \d+–\d+ \|$", text, re.M)
assert alt_tab == [str(n) for n in range(52)], alt_tab

E = [
# Kopf
("""am Commit `f63ad4c` (02.10.2026), Abschnitte 0–51,
11 225 Zeilen, sha256 `7f74b0e5…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2) und TB-129 (Fable 01a). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_51.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–4.md`).""",
 """am Commit `%s` (02.10.2026), Abschnitte 0–52,
%s Zeilen, sha256 `%s…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a) und TB-130 (Fable 02a). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_52.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–4.md`)."""
 % (commit[:7], "{:,}".format(zeilen_reg).replace(",", " "), sha[:8])),
# Wie gemessen
("(das Suchmuster des Auftrags, Art `MARKE`, 64 Zeilen)", "(das Suchmuster des Auftrags, Art `MARKE`, %d Zeilen)" % art["MARKE"]),
("(Art `MARKE+`, 104 Zeilen)", "(Art `MARKE+`, %d Zeilen)" % art["MARKE+"]),
("Art `UEBERSCHRIFT`, 80 Zeilen). Die\nAusgabe liegt in `docs/belege/TB-129/c1_marken.txt` (zuvor `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`).",
 "Art `UEBERSCHRIFT`, %d Zeilen). Die\nAusgabe liegt in `docs/belege/TB-130/c1_marken.txt` (zuvor `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`)."
 % art["UEBERSCHRIFT"]),
# Tabelle 2, 4.2
("**PRÄZISIERT durch R60 (51.5)** | 4.2 **mit** 48.16 R48 (d), (e) **und** 51.5 R60; dazu 48.19 R51 (T4) |",
 "**PRÄZISIERT durch R60 (51.5)**; Z. %d **PRÄZISIERT durch R64 (52.2)** | 4.2 **mit** 48.16 R48 (d), (e), 51.5 R60 **und** 52.2 R64 (a); dazu 48.19 R51 (T4) |" % Z[1]),
# Abschnitt 7 und Pflege
("\n\n---\n\n**Pflege:**",
 "\n\n## 7. Die Marken aus Fable 02a (TB-130)\n\n"
 "Alle 12 Marken, die TB-130 gesetzt hat (alle am alten Ort: fünf nach R65 (b), sieben vom steuernden Chat nach R65 (a)\n"
 "bestimmt; 51.5 trägt zwei), in der Reihenfolge des Registers. Erzeugt mit `docs/belege/TB-130/c2_index_02a.py` aus\n"
 "`docs/belege/TB-130/c1_marken.txt` (Zeile, Art, Teil) und Anhang A des Auftrags TB-130 (alter Ort), nicht abgetippt.\n"
 "In Tabelle 2 und 4 oben stehen sie zusätzlich an ihrer Stelle. Keine Marke tragen 7 (c) (52.5 Nr. 9), Abschnitt 9,\n"
 "Abschnitt 10 und der ERZEUGT-Block von Abschnitt 3 (R65 (d)).\n\n"
 + T7 + "\n\n---\n\n**Pflege:**"),
("Zuletzt nachgezogen in TB-129 (02.10.2026):", "In TB-129 (02.10.2026):"),
("Einträge mit `docs/belege/TB-129/c2_index_eintraege.py`.",
 "Einträge mit `docs/belege/TB-129/c2_index_eintraege.py`.\n"
 "Zuletzt nachgezogen in TB-130 (02.10.2026): Zeilenangaben mit `docs/belege/TB-130/c2_index_zeilen.py` vom Stand\n"
 "`f63ad4c` auf `%s` umgeschrieben (jede Zahl in Listen und Bereichen); 52 kommt zu T%d; Abschnittstabelle aus den\n"
 "Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-130/c2_index_eintraege.py`; in Abschnitt 6 die fünf\n"
 "Indexzeilen „Ohne Marke; an Fable (51.10 Nr. 7).“ auf die gesetzten Marken umgestellt (`c3_indexzeilen.py`)."
 % (commit[:7], t52)),
]
for a, b in E:
    n = text.count(a)
    if n != 1:
        sys.exit("Anker %dx: %r" % (n, a[:80]))
for a, b in E:
    text = text.replace(a, b)

# Tabelle 4: Zeilen an ihrem Anfang finden (genau eine), Zusatz vor dem Schluss ' |' bzw. statt '| – |'
ANH = [
("| 25 erste Falte, Konjunktion |", "anhaengen",
 "; 25.2 **BERICHTIGT durch R62 (51.7) und R65 (52.3)** (Z. %d, T4)" % Z[2]),
("| 47 aus 27c |", "ersetzen",
 "47.9 R26 **BERICHTIGT durch R61 (51.6)** (Z. %d); 47.13 R30 **BERICHTIGT durch R61 (51.6)** (Z. %d); beide nachgetragen nach R65 (b) (52.3)" % (Z[3], Z[4])),
("| 48 aus 29b |", "anhaengen",
 "; 48.16 R48 (d) **PRÄZISIERT durch R64 (52.2)** (Z. %d); 48.19 R51 **PRÄZISIERT durch R65 (52.3)** (Z. %d)" % (Z[5], Z[6])),
("| 50 Tatsachennotizen E-2 |", "anhaengen",
 "; 50.1, Zeile R48 (d) ERGÄNZT durch R60 (51.5) und 51.8 (Z. %d); 50.4, Schlusssatz ERGÄNZT durch R57 (51.2): bestätigt (Z. %d); beide nachgetragen nach R65 (b) (52.3)" % (Z[7], Z[8])),
("| 51 aus 01a |", "ersetzen",
 "51.5 R60 (a) **PRÄZISIERT durch R63 (52.1)** (Z. %d), R60 (b) und (c) **PRÄZISIERT durch R64 (52.2)** (Z. %d); 51.6 R61 (b) **PRÄZISIERT durch R65 (52.3)** (Z. %d); 51.9 ERGÄNZT durch R63 (52.1): die Lesart ist bestätigt (Z. %d)" % (Z[9], Z[10], Z[11], Z[12])),
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
    if prefix == "| 51 aus 01a |":
        zz[t[0]] += "\n| 52 aus 02a | %d | R63–R65 (52.1–52.3); 52.4 Voraussetzungen; 52.5 Offenes | – |" % t52

# Abschnittstabelle neu (alle Zeilen aus den Koepfen) und Zeile 52; Teilgrenzen
def tabzeile(n):
    return "| %d | `REGISTER_KOPIE_ABSCHNITT_%02d.md` | %d–%d |" % (n, n, ab[n][0], ab[n][1])
zz = "\n".join(zz).split("\n")
for k, s in enumerate(zz):
    m = re.match(r"^\| (\d+) \| `REGISTER_KOPIE_ABSCHNITT_\d\d\.md` \| \d+–\d+ \|$", s)
    if m:
        zz[k] = tabzeile(int(m.group(1)))
        if m.group(1) == "51":
            zz[k] += "\n" + tabzeile(52)
    elif s.startswith("*Frühere Vierteilung*"):
        kopf = s.split("):", 1)[0] + "):"
        zz[k] = kopf + " " + vier + "."
text = "\n".join(zz)
open(I, "w", encoding="utf-8").write(text)
print("Ersetzungen: %d, Tabellenzeilen: %d, je Anker genau 1; Abschnittstabelle 0-52 aus den Koepfen; Teile: %s; Arten %s"
      % (len(E), len(ANH), vier, art))
