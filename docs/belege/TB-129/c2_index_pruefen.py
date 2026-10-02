#!/usr/bin/env python3
"""TB-129 C2 Gegenprobe (Bauart TB-126 c2_index_pruefen.py): jede Angabe 'Z. <n>' (auch Listen 'Z. a, b' und
Bereiche 'Z. a–b' an jeder Zahl) in REGISTER_INDEX.md zeigt im Register am HEAD auf eine Zeile mit einem
Markenwort (ERSETZT, PRÄZISIERT, BERICHTIGT, ERGÄNZT, KORRIGIERT) oder wird mit ihrem Text gezeigt; die Zeile
'*Frühere Vierteilung*' (Teilgrenzen) ist ausgenommen. Dazu: die 14 Marken aus Fable 01a stehen mit ihrer
Zeile im Index; der Block '### Indexzeilen aus Fable 01a' traegt genau die sechs Zeilen aus C3 des Auftrags
(Auftrag am Commit S0, Bytevergleich); die Abschnittstabelle nennt 0-51 mit den Zeilen aus den Koepfen
der Abschnittsdateien.
Aufruf: trading-env/bin/python3 docs/belege/TB-129/c2_index_pruefen.py <S0>
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

# 14 Marken aus 01a: Zeile im Register und im Abschnitt 6 des Index
M = re.compile(r"^> ⭐ \*\*.*TB-129, 02\.10\.2026\)\.$")
mz = [i + 1 for i, s in enumerate(L) if M.match(s)]
a6 = I.split("## 6. Die Marken aus Fable 01a (TB-129)", 1)[1].split("\n---\n", 1)[0]
drin = [z for z in mz if ("| Z. %d |" % z) in a6]
print("Marken TB-129 im Register: %d; mit ihrer Zeile in Index-Abschnitt 6: %d (Soll 14/14)" % (len(mz), len(drin)))
if len(mz) != 14 or len(drin) != 14:
    fehler.append("Marken in Abschnitt 6")

# C3: sechs Zeilen zeichengleich
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-129_register_fable_01a.md" % S0],
                     capture_output=True, text=True, check=True).stdout
c3 = auf.split("**C3. Indexzeilen statt Marken**", 1)[1].split("\n```\n", 2)[1]
n6 = len(c3.split("\n"))
blk = a6.split("### Indexzeilen aus Fable 01a\n\n", 1)[1] if "### Indexzeilen aus Fable 01a\n\n" in a6 else ""
ok = blk.startswith(c3 + "\n") and I.count(c3) == 1
print("C3: %d Zeilen aus dem Auftrag; im Block '### Indexzeilen aus Fable 01a' zeichengleich: %s" % (n6, "ja" if ok else "NEIN"))
if not ok or n6 != 6:
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
if gut != len(dateien) or len(dateien) != 52:
    fehler.append("Abschnittstabelle")
if fehler:
    print("ABWEICHUNG:", fehler)
    sys.exit(1)
print("rc 0")
