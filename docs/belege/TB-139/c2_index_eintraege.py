#!/usr/bin/env python3
"""TB-139 C2: REGISTER_INDEX.md nach Fable 07a nachziehen (nach c2_index_zeilen.py).

Vorlage docs/belege/TB-136/c2_index_eintraege.py (dort nach TB-132, TB-130 und Bauart TB-129): jede Ersetzung hat einen
Anker, der im Index genau einmal vorkommen muss, sonst Abbruch ohne Schreiben. Inhalt: Kopf (Stand, Messhinweis,
Verweis auf die Abschnittsdateien bis _55.md, Zahl der Teile), "Wie gemessen" (Zahlen je Art aus c1_marken.txt),
Abschnittstabelle und Teilgrenzen aus den Koepfen der Abschnittsdateien bzw. aus c1_registerkopie.txt, die Eintraege
der Liste Nr. 1 bis 9 aus C2 des Auftrags (Tabelle 2: neue Zeile 5.2; Tabelle 4: 42, 46, 48, 53, 54, neue Zeile 55; neuer
Abschnitt 10 mit der Tabelle aus c2_index_07a_tabelle.md; Pflegeblock). Die Indexzeilen aus Fable 07a setzt
c3_indexzeilen.py (C3).
Wie die Vorlage: die neuen Texte der Liste Nr. 1 bis 7 und der Vorspann von Abschnitt 10 werden aus dem
Auftrag am Commit S0 gelesen (Codespannen der Listenpunkte bzw. der Codeblock nach "Vorspann von Abschnitt 10"),
nicht abgetippt; eingesetzt werden nur {Zn} (Zeile der Marke Nr. n nachher, a4_eintrag_daten.json) und {T} (Teil
von Abschnitt 55 aus c1_registerkopie.txt; in Nr. 7 die Nummer ohne "T", wie in den Zeilen darueber; in Nr. 1 kommt die neue Zeile
vor die Zeile 5.3). Der Vorspann wird wie in Abschnitt 9 umbrochen (Breite 118, nur an Leerzeichen).
Regel des Index: PRAEZISIERT und BERICHTIGT fett, ERGAENZT nicht.
Aufruf: trading-env/bin/python3 docs/belege/TB-139/c2_index_eintraege.py <S0> <commit_A> <datum>
"""
import glob
import json
import re
import subprocess
import sys
import textwrap

S0, CA, DATUM = sys.argv[1], sys.argv[2], sys.argv[3]
I = "docs/projektfuehrung/REGISTER_INDEX.md"
BL = "docs/belege/TB-139/"
T9 = open(BL + "c2_index_07a_tabelle.md", encoding="utf-8").read().rstrip("\n")
Z = {m["nr"]: m["zeile_neu"] for m in json.load(open(BL + "a4_eintrag_daten.json", encoding="utf-8"))["marken"]}
assert sorted(Z) == list(range(1, 21))
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
assert sorted(ab) == list(range(56)), sorted(ab)
commits = {v[2] for v in ab.values()}
shas = {v[3] for v in ab.values()}
assert len(commits) == 1 and len(shas) == 1
commit, sha = commits.pop(), shas.pop()
assert commit.startswith(CA), (commit, CA)
zeilen_reg = ab[55][1]
teile = []
for s in open(BL + "c1_registerkopie.txt", encoding="utf-8"):
    m = re.match(r"^geschrieben: \S+teil(\d+)\.md  Abschnitte (\d+)–(\d+) ", s)
    if m:
        teile.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
assert [t[0] for t in teile] == list(range(1, len(teile) + 1)), teile
vier = ", ".join("T%d = %d–%d (Z. %d–%d)" % (n, a, b, ab[a][0], ab[b][1]) for n, a, b in teile)
t54 = next(n for n, a, b in teile if a <= 55 <= b)
T = "T%d" % t54

# Texte aus C2 des Auftrags am Commit S0
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-139_register_fable_07a.md" % S0],
                     capture_output=True, text=True, check=True).stdout
c2 = auf.split("\n**C2. ", 1)[1].split("\n**C3. ", 1)[0]
punkte = {}
for s in c2.split("\n"):
    m = re.match(r"^(\d)\. \*\*", s)
    if m:
        punkte[int(m.group(1))] = re.findall(r"`([^`]+)`", s)
assert sorted(punkte) == list(range(1, 10)), sorted(punkte)
vorspann = c2.split("Vorspann von Abschnitt 10 des Index", 1)[1].split("\n```\n", 2)[1]
assert "\n" not in vorspann and vorspann.startswith("Alle 20 Marken, die TB-139 gesetzt hat"), vorspann[:60]
vorspann = textwrap.fill(vorspann, width=118, break_long_words=False, break_on_hyphens=False)


def setze(t, ohne_t=False):
    for n in range(20, 0, -1):
        t = t.replace("{Z%d}" % n, str(Z[n]))
    t = t.replace("{T}", str(t54) if ohne_t else T)
    assert "{" not in t and "}" not in t, t
    return t


p1_alt = punkte[1][0]
p1_neu = setze(punkte[1][1]) + "\n" + p1_alt
assert p1_alt == "| 5.3 „Krypto: Platzhalter mit Regel“ |" and punkte[1][1].startswith("| 5.2 „Der Go-Live-Schnitt“ | "), punkte[1]
assert [punkte[k][0] for k in (2, 3, 4, 5)] == ["| 42 aus 25a/25b/25c |", "| 46 aus 27a |", "| 48 aus 29b |", "| 53 aus 02c |"]
assert all(punkte[k][1] == " |" for k in (2, 3, 4, 5))
assert punkte[6][0] == "| 54 aus 04a |" and punkte[6][1] == "| – |" and punkte[6][2] == "–"
neue_zeile = setze(punkte[7][0], ohne_t=True)
assert neue_zeile.startswith("| 55 aus 07a | %d |" % t54), neue_zeile
assert punkte[9][:2] == ["Zuletzt nachgezogen in TB-136 (05.10.2026):", "In TB-136 (05.10.2026):"], punkte[9][:2]

text = open(I, encoding="utf-8").read()
alt_tab = re.findall(r"^\| (\d+) \| `REGISTER_KOPIE_ABSCHNITT_\d\d\.md` \| \d+–\d+ \|$", text, re.M)
assert alt_tab == [str(n) for n in range(55)], alt_tab

E = [
# Kopf (Index Z. 3-5)
("""am Commit `9b7b060` (05.10.2026), Abschnitte 0–54,
11 581 Zeilen, sha256 `8d505a38…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a), TB-132 (Fable 02c) und TB-136 (Fable 04a). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_54.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–5.md`).""",
 """am Commit `%s` (%s), Abschnitte 0–55,
%s Zeilen, sha256 `%s…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a), TB-132 (Fable 02c), TB-136 (Fable 04a) und TB-139 (Fable 07a). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_55.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–%d.md`)."""
 % (commit[:7], DATUM, "{:,}".format(zeilen_reg).replace(",", " "), sha[:8], len(teile))),
# Wie gemessen
("(das Suchmuster des Auftrags, Art `MARKE`, 95 Zeilen)", "(das Suchmuster des Auftrags, Art `MARKE`, %d Zeilen)" % art["MARKE"]),
("(Art `MARKE+`, 128 Zeilen)", "(Art `MARKE+`, %d Zeilen)" % art["MARKE+"]),
("Art `UEBERSCHRIFT`, 91 Zeilen). Die\nAusgabe liegt in `docs/belege/TB-136/c1_marken.txt` (zuvor `docs/belege/TB-132/c1_marken.txt`, `docs/belege/TB-130/c1_marken.txt`, `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`).",
 "Art `UEBERSCHRIFT`, %d Zeilen). Die\nAusgabe liegt in `docs/belege/TB-139/c1_marken.txt` (zuvor `docs/belege/TB-136/c1_marken.txt`, `docs/belege/TB-132/c1_marken.txt`, `docs/belege/TB-130/c1_marken.txt`, `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`)."
 % art["UEBERSCHRIFT"]),
# Liste Nr. 1: Tabelle 2, neue Zeile 5.2 vor der Zeile 5.3
(p1_alt, p1_neu),
# Liste Nr. 8: Abschnitt 10, vor dem Pflegeblock
("\n\n---\n\n**Pflege:**",
 "\n\n## 10. Die Marken aus Fable 07a (TB-139)\n\n" + vorspann + "\n\n" + T9 + "\n\n---\n\n**Pflege:**"),
# Liste Nr. 9: Pflegeblock
(punkte[9][0], punkte[9][1]),
("15 Marken und zwei Indexzeilen nach R77 (b) und (c) (`c3_indexzeilen.py`).",
 "15 Marken und zwei Indexzeilen nach R77 (b) und (c) (`c3_indexzeilen.py`).\n"
 "Zuletzt nachgezogen in TB-139 (%s): Zeilenangaben mit `docs/belege/TB-139/c2_index_zeilen.py` vom Stand\n"
 "`9b7b060` auf `%s` umgeschrieben (jede Zahl in Listen und Bereichen); 55 kommt zu %s; Abschnittstabelle aus den\n"
 "Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-139/c2_index_eintraege.py`; neuer Abschnitt 10 mit den\n"
 "20 Marken und drei Indexzeilen nach R80 (b) (`c3_indexzeilen.py`)."
 % (DATUM, commit[:7], T)),
]
for a, b in E:
    n = text.count(a)
    if n != 1:
        sys.exit("Anker %dx: %r" % (n, a[:80]))
for a, b in E:
    text = text.replace(a, b)

# Liste Nr. 2 bis 7: Tabelle 4, Zeilen an ihrem Anfang finden (genau eine), Zusatz vor dem Schluss ' |' bzw. statt '– |'
ANH = [
("| 42 aus 25a/25b/25c |", "anhaengen", setze(punkte[2][2])),
("| 46 aus 27a |", "anhaengen", setze(punkte[3][2])),
("| 48 aus 29b |", "anhaengen", setze(punkte[4][2])),
("| 53 aus 02c |", "anhaengen", setze(punkte[5][2])),
("| 54 aus 04a |", "ersetzen", setze(punkte[6][3])),
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
    if prefix == "| 54 aus 04a |":
        zz[t[0]] += "\n" + neue_zeile

# Abschnittstabelle neu (alle Zeilen aus den Koepfen) und Zeile 55; Teilgrenzen
def tabzeile(n):
    return "| %d | `REGISTER_KOPIE_ABSCHNITT_%02d.md` | %d–%d |" % (n, n, ab[n][0], ab[n][1])
zz = "\n".join(zz).split("\n")
for k, s in enumerate(zz):
    m = re.match(r"^\| (\d+) \| `REGISTER_KOPIE_ABSCHNITT_\d\d\.md` \| \d+–\d+ \|$", s)
    if m:
        zz[k] = tabzeile(int(m.group(1)))
        if m.group(1) == "54":
            zz[k] += "\n" + tabzeile(55)
    elif s.startswith("*Frühere Vierteilung*"):
        kopf = s.split("):", 1)[0] + "):"
        zz[k] = kopf + " " + vier + "."
text = "\n".join(zz)
open(I, "w", encoding="utf-8").write(text)
print("Ersetzungen: %d, Tabellenzeilen: %d und neue Zeile 55, je Anker genau 1; Abschnittstabelle 0-55 aus den Koepfen; Teile: %s; Arten %s"
      % (len(E), len(ANH), vier, art))
