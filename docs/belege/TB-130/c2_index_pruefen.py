#!/usr/bin/env python3
"""TB-130 C2/C3 Gegenprobe (Bauart TB-129 c2_index_pruefen.py): jede Angabe 'Z. <n>' (auch Listen 'Z. a, b' und
Bereiche 'Z. a–b' an jeder Zahl) in REGISTER_INDEX.md zeigt im Register am HEAD auf eine Zeile mit einem
Markenwort (ERSETZT, PRÄZISIERT, BERICHTIGT, ERGÄNZT, KORRIGIERT); die Zeile '*Frühere Vierteilung*'
(Teilgrenzen) ist ausgenommen. Dazu: die 14 Marken aus 01a stehen weiter mit ihrer Zeile in Abschnitt 6, die 12
Marken aus 02a mit ihrer Zeile in Abschnitt 7; im Block '### Indexzeilen aus Fable 01a' tragen fuenf Zeilen den
Schluss aus C3 des Auftrags (am Commit S0) und keine mehr den alten; die Abschnittstabelle nennt 0-52 mit den
Zeilen aus den Koepfen der Abschnittsdateien; die Indexzeilen E-2 zaehlen weiter 6.
Aufruf: trading-env/bin/python3 docs/belege/TB-130/c2_index_pruefen.py <S0>
"""
import glob
import re
import subprocess
import sys

S0 = sys.argv[1]
I = open("docs/projektfuehrung/REGISTER_INDEX.md", encoding="utf-8").read()
L = open("docs/VORREGISTRIERUNG_neuselektion.md", encoding="utf-8").read().split("\n")
W = re.compile(r"ERSETZT|PRÄZISIERT|BERICHTIGT|ERGÄNZT|KORRIGIERT")
fehler = []
nummern = []
for s in I.split("\n"):
    if s.startswith("*Frühere Vierteilung*"):
        continue
    for m in re.finditer(r"Z\. (\d+(?:(?:, |–)\d+)*)", s):
        nummern += [int(x) for x in re.split(r", |–", m.group(1))]
ohne = [n for n in nummern if not W.search(L[n - 1])]
print("Zeilenangaben im Index: %d; mit Markenwort: %d" % (len(nummern), len(nummern) - len(ohne)))
for n in ohne:
    print("  ohne Markenwort: Z. %d: %s" % (n, L[n - 1][:100]))
if ohne:
    fehler.append("Zeilenangaben ohne Markenwort")
print("Indexzeilen E-2: %d (Soll 6)" % I.count("**Indexzeile E-2**"))
if I.count("**Indexzeile E-2**") != 6:
    fehler.append("Indexzeilen E-2")


def abschnitt(kopf):
    return I.split(kopf, 1)[1].split("\n---\n", 1)[0].split("\n## ", 1)[0]


for tb, kopf, soll in (("TB-129", "## 6. Die Marken aus Fable 01a (TB-129)", 14),
                       ("TB-130", "## 7. Die Marken aus Fable 02a (TB-130)", 12)):
    M = re.compile(r"^> ⭐ \*\*.*" + tb + r", 02\.10\.2026\)\.$")
    mz = [i + 1 for i, s in enumerate(L) if M.match(s)]
    a = abschnitt(kopf) if kopf in I else ""
    drin = [z for z in mz if ("| Z. %d |" % z) in a]
    print("Marken %s im Register: %d; mit ihrer Zeile in '%s': %d (Soll %d/%d)" % (tb, len(mz), kopf[3:], len(drin), soll, soll))
    if len(mz) != soll or len(drin) != soll:
        fehler.append("Marken %s" % tb)

# C3: fuenf Zeilen mit neuem Schluss
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-130_register_fable_02a.md" % S0],
                     capture_output=True, text=True, check=True).stdout
c3 = auf.split("**C3. Indexzeilen aus Fable 01a anpassen:**", 1)[1].split("\n\n", 1)[0]
alt, neu = re.findall(r"`([^`]+)`", c3)[1:3]
a6 = abschnitt("## 6. Die Marken aus Fable 01a (TB-129)")
blk = a6.split("### Indexzeilen aus Fable 01a\n\n", 1)[1].split("\n")
n_neu = sum(1 for s in blk if s.endswith(" " + neu))
print("C3 (aus dem Auftrag): alt %r, neu %r; im Block: neu %d (Soll 5), alt im Index %d (Soll 0), Tag-Vorbedingungen erste Zeile: %s"
      % (alt, neu, n_neu, I.count(alt), "ja" if blk[0].startswith("- **Tag-Vorbedingungen**") else "NEIN"))
if n_neu != 5 or I.count(alt) != 0 or not blk[0].startswith("- **Tag-Vorbedingungen**"):
    fehler.append("C3")

# Abschnittstabelle gegen die Koepfe
KOPF = re.compile(r"^# REGISTER-KOPIE Abschnitt (\d+) \(von 0–(\d+)\) — Register-Z\. (\d+)–(\d+) — ")
gut = 0
dateien = sorted(glob.glob("docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_*.md"))
for d in dateien:
    k = KOPF.match(open(d, encoding="utf-8").readline())
    zeile = "| %s | `%s` | %s–%s |" % (k.group(1), d.rsplit("/", 1)[1], k.group(3), k.group(4))
    gut += I.count(zeile) == 1
print("Abschnittstabelle: %d/%d Zeilen gleich den Koepfen der Abschnittsdateien" % (gut, len(dateien)))
if gut != len(dateien) or len(dateien) != 53:
    fehler.append("Abschnittstabelle")
if fehler:
    print("ABWEICHUNG:", fehler)
    sys.exit(1)
print("rc 0")
