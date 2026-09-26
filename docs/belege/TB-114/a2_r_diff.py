"""TB-114 A2: je R-Baustein (R1-R8) ein `diff` zwischen dem Codeblock der Fable-Antwort 26a und dem Blockzitat in
Registerabschnitt 45. Liest beide Dateien UNABHAENGIG vom Einsetzskript: in der Fable-Datei die Zeilen von
"**R<n> —" bis zur naechsten Leerzeile bzw. dem Ende des Codeblocks; im Register (nur ab "## 45. ") die Zeilen ab
"> **R<n> —" bis zur ersten Zeile ohne "> ", ohne das Praefix "> ". Aufruf aus der Repo-Wurzel; TB114_PROBE=<pfad>.
"""
import os
import subprocess
import tempfile

REG = os.environ.get("TB114_PROBE") or "docs/VORREGISTRIERUNG_neuselektion.md"
FAB = "docs/projektfuehrung/FABLE_ANTWORT_2026-09-26a_dreizehn_fragen_nullbefund_registerblock.md"
fab = open(FAB, encoding="utf-8").read().split("\n")
reg = open(REG, encoding="utf-8").read().split("\n")
a = fab.index("```markdown")
e = next(i for i in range(a + 1, len(fab)) if fab[i] == "```")
k45 = next(i for i, z in enumerate(reg) if z.startswith("## 45. "))
fehler = 0
for n in range(1, 9):
    kopf = "**R%d — " % n
    s = [i for i in range(a + 1, e) if fab[i].startswith(kopf)]
    assert len(s) == 1, (n, s)
    quelle = []
    for i in range(s[0], e):
        if not fab[i]:
            break
        quelle.append(fab[i])
    r = [i for i in range(k45, len(reg)) if reg[i].startswith("> " + kopf)]
    assert len(r) == 1, (n, r)
    im_register = []
    for i in range(r[0], len(reg)):
        if not reg[i].startswith("> "):
            break
        im_register.append(reg[i][2:])
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as fa, \
         tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as fb:
        fa.write("\n".join(quelle) + "\n"); fb.write("\n".join(im_register) + "\n")
    p = subprocess.run(["diff", fa.name, fb.name], capture_output=True, text=True)
    os.unlink(fa.name); os.unlink(fb.name)
    fehler += p.returncode != 0
    print("R%d  Fable Z. %d-%d (%d Zeilen, %d Zeichen)  Register Z. %d-%d (%d Zeilen)  diff rc %d"
          % (n, s[0] + 1, s[0] + len(quelle), len(quelle), len("\n".join(quelle)),
             r[0] + 1, r[0] + len(im_register), len(im_register), p.returncode))
    if p.returncode:
        print(p.stdout)
print("R-Bausteine: 8, diff rc 0: %d, Abweichungen: %d" % (8 - fehler, fehler))
raise SystemExit(1 if fehler else 0)
