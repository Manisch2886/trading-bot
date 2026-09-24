"""TB-96 D2: jedes eingesetzte Fable-Zitat im Register gegen seine Quelle (diff).

Liest zitate.json (vom Einsetzskript). Zeilenzitat: im Register wird die Zeile
gesucht, die nach Abzug des Blockzitat-Praefixes "> " der Quellzeile (ebenfalls
ohne "> ") entspricht; Quellzeile und Registerzeile werden unabhaengig aus den
Dateien gelesen und mit `diff` verglichen. Teilzitat: es muss wortgleich in der
Quellzeile UND in einer Registerzeile am richtigen Ort stehen; verglichen wird
der Ausschnitt der Quellzeile mit dem Ausschnitt der Registerzeile an der
Fundstelle. Aufruf aus der Repo-Wurzel.
"""
import json
import os
import subprocess
import tempfile

REG = "docs/VORREGISTRIERUNG_neuselektion.md"
QUELLE = "docs/projektfuehrung/FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md"
reg = open(REG, encoding="utf-8").read().split("\n")
q = open(QUELLE, encoding="utf-8").read().split("\n")
zitate = json.load(open("docs/belege/TB-96/zitate.json", encoding="utf-8"))
START40 = next(i for i, r in enumerate(reg) if r.startswith("## 40. "))


def im_ort(i, wo):
    return (i >= START40) == (wo == "Abschnitt 40")


def ohne_praefix(s):
    return s[2:] if s.startswith("> ") else s


def diff(a, b):
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as fa, \
         tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as fb:
        fa.write(a + "\n"); fb.write(b + "\n")
    r = subprocess.run(["diff", fa.name, fb.name], capture_output=True, text=True)
    os.unlink(fa.name); os.unlink(fb.name)
    return r.returncode, r.stdout


fehler = 0
for z in zitate:
    quelle = ohne_praefix(q[z["zeile"] - 1])
    if z["art"] == "zeile":
        soll = quelle
        treffer = [i for i, r in enumerate(reg)
                   if r.startswith("> ") and r[2:] == soll and im_ort(i, z["wo"])]
        wo = treffer[0] + 1 if treffer else 0
        ist = reg[treffer[0]][2:] if treffer else ""
    else:
        soll = z["text"]
        k = quelle.find(soll)
        soll_q = quelle[k:k + len(soll)] if k >= 0 else ""
        treffer = [i for i, r in enumerate(reg) if soll in r and im_ort(i, z["wo"])]
        # zuerst die eigene Fundstelle, nicht ein Vollzitat derselben Quellzeile
        treffer = sorted(treffer, key=lambda i: reg[i].startswith("> ") and reg[i][2:] == quelle)
        wo = treffer[0] + 1 if treffer else 0
        ist = ""
        if treffer:
            j = reg[treffer[0]].find(soll)
            ist = reg[treffer[0]][j:j + len(soll)]
        soll = soll_q
    rc, out = diff(soll, ist)
    fehler += rc != 0
    print("%-5s Fable 24a Z. %2d  -> Register Z. %4d  %4d Zeichen  diff rc %d  (%s)"
          % (z["art"], z["zeile"], wo, len(soll), rc, z["wo"]))
    if rc:
        print(out)
print("Zitate: %d (Zeilen %d, Teile %d), diff rc 0: %d, Abweichungen: %d"
      % (len(zitate), sum(z["art"] == "zeile" for z in zitate),
         sum(z["art"] == "teil" for z in zitate), len(zitate) - fehler, fehler))
raise SystemExit(1 if fehler else 0)
