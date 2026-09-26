"""TB-116 A: jedes Zitat in a_regeln.md gegen das Register (diff), Bauart TB-110 d2_zitate.py.

Liest a_regeln.md und das Register UNABHAENGIG vom Einsetzskript: die Kopfzeile
'### Zn — ... · Register Z. a–b' nennt die Fundstelle, der folgende ~~~~text-Block
ist das Zitat. Die Registerzeilen a..b holt `sed -n`, verglichen wird mit `diff`.
Aufruf aus der Repo-Wurzel; TB116_REGELN=<pfad> prueft eine andere Datei (Mutationsprobe).
"""
import os
import re
import subprocess
import tempfile

REG = "docs/VORREGISTRIERUNG_neuselektion.md"
REGELN = os.environ.get("TB116_REGELN") or "docs/belege/TB-116/a_regeln.md"
zeilen = open(REGELN, encoding="utf-8").read().split("\n")
kopf = re.compile(r"^### (Z\d+) — .* · Register Z\. (\d+)–(\d+)$")

fehler = gesamt = 0
for i, z in enumerate(zeilen):
    m = kopf.match(z)
    if not m:
        continue
    start = zeilen.index("~~~~text", i) + 1
    ende = zeilen.index("~~~~", start)
    zitat = "\n".join(zeilen[start:ende]) + "\n"
    a, b = int(m.group(2)), int(m.group(3))
    soll = subprocess.run(["sed", "-n", "%d,%dp" % (a, b), REG], capture_output=True, text=True).stdout
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
        f.write(zitat)
    r = subprocess.run(["diff", f.name, "-"], input=soll, capture_output=True, text=True)
    os.unlink(f.name)
    gesamt += 1
    fehler += r.returncode != 0
    print("%-4s Register Z. %4d-%4d  %2d Zeilen  %5d Zeichen  diff rc %d" % (
        m.group(1), a, b, b - a + 1, len(zitat), r.returncode))
    if r.returncode:
        print(r.stdout)
print("Zitate: %d, diff rc 0: %d, Abweichungen: %d" % (gesamt, gesamt - fehler, fehler))
raise SystemExit(1 if fehler or gesamt == 0 else 0)
