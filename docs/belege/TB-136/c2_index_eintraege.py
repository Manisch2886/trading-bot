#!/usr/bin/env python3
"""TB-136 C2: REGISTER_INDEX.md nach Fable 04a nachziehen (nach c2_index_zeilen.py).

Vorlage docs/belege/TB-132/c2_index_eintraege.py (dort nach TB-130 und Bauart TB-129): jede Ersetzung hat einen
Anker, der im Index genau einmal vorkommen muss, sonst Abbruch ohne Schreiben. Inhalt: Kopf (Stand, Messhinweis,
Verweis auf die Abschnittsdateien bis _54.md, Zahl der Teile), "Wie gemessen" (Zahlen je Art aus c1_marken.txt),
Abschnittstabelle und Teilgrenzen aus den Koepfen der Abschnittsdateien bzw. aus c1_registerkopie.txt, die Eintraege
der Liste Nr. 1 bis 9 aus C2 des Auftrags (Tabelle 3: 2d, 5f; Tabelle 4: 48, 51, 52, 53, neue Zeile 54; neuer
Abschnitt 9 mit der Tabelle aus c2_index_04a_tabelle.md; Pflegeblock). Die Indexzeilen aus Fable 04a setzt
c3_indexzeilen.py (C3).
Anders als die Vorlage: die neuen Texte der Liste Nr. 1 bis 7 und der Vorspann von Abschnitt 9 werden aus dem
Auftrag am Commit S0 gelesen (Codespannen der Listenpunkte bzw. der Codeblock nach "Vorspann von Abschnitt 9"),
nicht abgetippt; eingesetzt werden nur {Zn} (Zeile der Marke Nr. n nachher, a4_eintrag_daten.json) und {T} (Teil
von Abschnitt 54 aus c1_registerkopie.txt; in Nr. 7 die Nummer ohne "T", wie in den Zeilen darueber). Der
Vorspann wird wie in Abschnitt 8 umbrochen (Breite 118, nur an Leerzeichen).
Regel des Index: PRAEZISIERT und BERICHTIGT fett, ERGAENZT nicht.
Aufruf: trading-env/bin/python3 docs/belege/TB-136/c2_index_eintraege.py <S0> <commit_A> <datum>
"""
import glob
import json
import re
import subprocess
import sys
import textwrap

S0, CA, DATUM = sys.argv[1], sys.argv[2], sys.argv[3]
I = "docs/projektfuehrung/REGISTER_INDEX.md"
BL = "docs/belege/TB-136/"
T9 = open(BL + "c2_index_04a_tabelle.md", encoding="utf-8").read().rstrip("\n")
Z = {m["nr"]: m["zeile_neu"] for m in json.load(open(BL + "a4_eintrag_daten.json", encoding="utf-8"))["marken"]}
assert sorted(Z) == list(range(1, 16))
for z in Z.values():
    assert ("| Z. %d |" % z) in T9, z

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
assert sorted(ab) == list(range(55)), sorted(ab)
commits = {v[2] for v in ab.values()}
shas = {v[3] for v in ab.values()}
assert len(commits) == 1 and len(shas) == 1
commit, sha = commits.pop(), shas.pop()
assert commit.startswith(CA), (commit, CA)
zeilen_reg = ab[54][1]
teile = []
for s in open(BL + "c1_registerkopie.txt", encoding="utf-8"):
    m = re.match(r"^geschrieben: \S+teil(\d+)\.md  Abschnitte (\d+)–(\d+) ", s)
    if m:
        teile.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
assert [t[0] for t in teile] == list(range(1, len(teile) + 1)), teile
vier = ", ".join("T%d = %d–%d (Z. %d–%d)" % (n, a, b, ab[a][0], ab[b][1]) for n, a, b in teile)
t54 = next(n for n, a, b in teile if a <= 54 <= b)
T = "T%d" % t54

# Texte aus C2 des Auftrags am Commit S0
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-136_register_fable_04a.md" % S0],
                     capture_output=True, text=True, check=True).stdout
c2 = auf.split("\n**C2. ", 1)[1].split("\n**C3. ", 1)[0]
punkte = {}
for s in c2.split("\n"):
    m = re.match(r"^(\d)\. \*\*", s)
    if m:
        punkte[int(m.group(1))] = re.findall(r"`([^`]+)`", s)
assert sorted(punkte) == list(range(1, 10)), sorted(punkte)
vorspann = c2.split("Vorspann von Abschnitt 9 des Index", 1)[1].split("\n```\n", 2)[1]
assert "\n" not in vorspann and vorspann.startswith("Alle 15 Marken, die TB-136 gesetzt hat"), vorspann[:60]
vorspann = textwrap.fill(vorspann, width=118, break_long_words=False, break_on_hyphens=False)


def setze(t, ohne_t=False):
    for n in range(15, 0, -1):
        t = t.replace("{Z%d}" % n, str(Z[n]))
    t = t.replace("{T}", str(t54) if ohne_t else T)
    assert "{" not in t and "}" not in t, t
    return t


p1_alt, p1_neu = punkte[1][0], setze(punkte[1][1])
p2_alt, p2_neu = punkte[2][0], setze(punkte[2][1])
assert punkte[3][0] == "| 48 aus 29b |" and punkte[4][0] == "| 51 aus 01a |" and punkte[5][0] == "| 52 aus 02a |"
assert punkte[6][0] == "| 53 aus 02c |" and punkte[6][1] == "| – |" and punkte[6][2] == "–"
neue_zeile = setze(punkte[7][0], ohne_t=True)
assert neue_zeile.startswith("| 54 aus 04a | %d |" % t54), neue_zeile
assert punkte[9][:2] == ["Zuletzt nachgezogen in TB-132 (04.10.2026):", "In TB-132 (04.10.2026):"], punkte[9][:2]

text = open(I, encoding="utf-8").read()
alt_tab = re.findall(r"^\| (\d+) \| `REGISTER_KOPIE_ABSCHNITT_\d\d\.md` \| \d+–\d+ \|$", text, re.M)
assert alt_tab == [str(n) for n in range(54)], alt_tab

E = [
# Kopf (Index Z. 3-5)
("""am Commit `ee43f5f` (04.10.2026), Abschnitte 0–53,
11 471 Zeilen, sha256 `9a2cefb7…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a) und TB-132 (Fable 02c). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_53.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–4.md`).""",
 """am Commit `%s` (%s), Abschnitte 0–54,
%s Zeilen, sha256 `%s…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a), TB-132 (Fable 02c) und TB-136 (Fable 04a). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_54.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–%d.md`)."""
 % (commit[:7], DATUM, "{:,}".format(zeilen_reg).replace(",", " "), sha[:8], len(teile))),
# Wie gemessen
("(das Suchmuster des Auftrags, Art `MARKE`, 84 Zeilen)", "(das Suchmuster des Auftrags, Art `MARKE`, %d Zeilen)" % art["MARKE"]),
("(Art `MARKE+`, 121 Zeilen)", "(Art `MARKE+`, %d Zeilen)" % art["MARKE+"]),
("Art `UEBERSCHRIFT`, 88 Zeilen). Die\nAusgabe liegt in `docs/belege/TB-132/c1_marken.txt` (zuvor `docs/belege/TB-130/c1_marken.txt`, `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`).",
 "Art `UEBERSCHRIFT`, %d Zeilen). Die\nAusgabe liegt in `docs/belege/TB-136/c1_marken.txt` (zuvor `docs/belege/TB-132/c1_marken.txt`, `docs/belege/TB-130/c1_marken.txt`, `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`)."
 % art["UEBERSCHRIFT"]),
# Liste Nr. 1 und 2: Tabelle 3, Zeilen 2d und 5f
(p1_alt, p1_neu),
(p2_alt, p2_neu),
# Liste Nr. 8: Abschnitt 9, vor dem Pflegeblock
("\n\n---\n\n**Pflege:**",
 "\n\n## 9. Die Marken aus Fable 04a (TB-136)\n\n" + vorspann + "\n\n" + T9 + "\n\n---\n\n**Pflege:**"),
# Liste Nr. 9: Pflegeblock
(punkte[9][0], punkte[9][1]),
("21 Marken und den drei Indexzeilen nach R70 (b) (`c3_indexzeilen.py`).",
 "21 Marken und den drei Indexzeilen nach R70 (b) (`c3_indexzeilen.py`).\n"
 "Zuletzt nachgezogen in TB-136 (%s): Zeilenangaben mit `docs/belege/TB-136/c2_index_zeilen.py` vom Stand\n"
 "`ee43f5f` auf `%s` umgeschrieben (jede Zahl in Listen und Bereichen); 54 kommt zu %s; Abschnittstabelle aus den\n"
 "Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-136/c2_index_eintraege.py`; neuer Abschnitt 9 mit den\n"
 "15 Marken und zwei Indexzeilen nach R77 (b) und (c) (`c3_indexzeilen.py`)."
 % (DATUM, commit[:7], T)),
]
for a, b in E:
    n = text.count(a)
    if n != 1:
        sys.exit("Anker %dx: %r" % (n, a[:80]))
for a, b in E:
    text = text.replace(a, b)

# Liste Nr. 3 bis 7: Tabelle 4, Zeilen an ihrem Anfang finden (genau eine), Zusatz vor dem Schluss ' |' bzw. statt '– |'
ANH = [
("| 48 aus 29b |", "anhaengen", setze(punkte[3][2])),
("| 51 aus 01a |", "anhaengen", setze(punkte[4][1])),
("| 52 aus 02a |", "anhaengen", setze(punkte[5][1])),
("| 53 aus 02c |", "ersetzen", setze(punkte[6][3])),
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
    if prefix == "| 53 aus 02c |":
        zz[t[0]] += "\n" + neue_zeile

# Abschnittstabelle neu (alle Zeilen aus den Koepfen) und Zeile 54; Teilgrenzen
def tabzeile(n):
    return "| %d | `REGISTER_KOPIE_ABSCHNITT_%02d.md` | %d–%d |" % (n, n, ab[n][0], ab[n][1])
zz = "\n".join(zz).split("\n")
for k, s in enumerate(zz):
    m = re.match(r"^\| (\d+) \| `REGISTER_KOPIE_ABSCHNITT_\d\d\.md` \| \d+–\d+ \|$", s)
    if m:
        zz[k] = tabzeile(int(m.group(1)))
        if m.group(1) == "53":
            zz[k] += "\n" + tabzeile(54)
    elif s.startswith("*Frühere Vierteilung*"):
        kopf = s.split("):", 1)[0] + "):"
        zz[k] = kopf + " " + vier + "."
text = "\n".join(zz)
open(I, "w", encoding="utf-8").write(text)
print("Ersetzungen: %d, Tabellenzeilen: %d und neue Zeile 54, je Anker genau 1; Abschnittstabelle 0-54 aus den Koepfen; Teile: %s; Arten %s"
      % (len(E), len(ANH), vier, art))
