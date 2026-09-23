"""TB-89: Zeichenvergleich je Blockzitat in Abschnitt 38 gegen die Quelldatei (diff)."""
import re, subprocess, tempfile, os
REG = "docs/VORREGISTRIERUNG_neuselektion.md"
QUELLE = "docs/projektfuehrung/FABLE_ANTWORT_2026-09-22h_schluessel_und_vollzug.md"
VORLAGE = "docs/belege/TB-89/abschnitt38_vorlage.md"
q = open(QUELLE, encoding="utf-8").read().split("\n")
reg = open(REG, encoding="utf-8").read().split("\n")
start = next(i for i, z in enumerate(reg) if z.startswith("## 38. "))
abschnitt = reg[start:]
vorlage = open(VORLAGE, encoding="utf-8").read().split("\n")
# Reihenfolge der Platzhalter in der Vorlage = Reihenfolge der Zitate im Register
nummern = [int(m) for z in vorlage for m in re.findall(r"«Q:(\d+)»", z)]
# Zitatzeilen im Abschnitt: Zeilen, die als Platzhalter-Ersatz stehen -> ueber Position
pos = [i for i, z in enumerate(vorlage) if re.fullmatch(r"«Q:\d+»", z)]
# Vorlage beginnt mit Leerzeile, die beim Anhaengen entfernt wurde
versatz = 1
fehler = 0
for n, p in zip(nummern, pos):
    im_register = abschnitt[p - versatz]
    ohne = im_register[2:] if not q[n - 1].startswith("> ") else im_register
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as a, \
         tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as b:
        a.write(q[n - 1] + "\n"); b.write(ohne + "\n")
    r = subprocess.run(["diff", a.name, b.name], capture_output=True, text=True)
    os.unlink(a.name); os.unlink(b.name)
    ergebnis = "gleich" if r.returncode == 0 else "ABWEICHUNG"
    fehler += r.returncode != 0
    print("Quelle Z. %3d  Register Z. %4d  %4d Zeichen  diff rc %d  %s"
          % (n, start + p - versatz + 1, len(q[n - 1]), r.returncode, ergebnis))
    if r.returncode: print(r.stdout)
print("Zitate: %d, Abweichungen: %d" % (len(nummern), fehler))
