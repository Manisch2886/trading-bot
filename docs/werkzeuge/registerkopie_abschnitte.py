#!/usr/bin/env python3
"""registerkopie_abschnitte.py - Registerkopie je Abschnitt (F1, Betreiberentscheid 01.10.2026, ca. 21:25).

Schneidet das Register am HEAD an jeder Zeile `^## <n>\\.` in eine Datei je Abschnitt:
    <ziel>/REGISTER_KOPIE_ABSCHNITT_<nn>.md     (nn zweistellig, 00 .. letzter Abschnitt)
Zeile 1 Kopf, Zeile 2 leer, ab Zeile 3 der Body unveraendert (bytegleich). Die Vorrede vor Abschnitt 0
gehoert zu Abschnitt 00. Kopf:
    # REGISTER-KOPIE Abschnitt <n> (von 0–<m>) — Register-Z. <a>–<b> — Commit <hash> — <Datum> — Original sha256 <…> — KOPIE, nicht das Register
<hash>/<Datum>: letzter Commit, der das Register geaendert hat. Prueft danach: Bodies aneinandergehaengt ==
Original (bytegleich), Abschnittsnummern fortlaufend. Rueckgabe 0 gut, 1 Pruefung gescheitert, 2 Eingabe
unbrauchbar (Arbeitsbaum != HEAD). Loescht nichts. Spaeter in registerkopie.py aufzunehmen (TB-127).
Aufruf aus der Repo-Wurzel: python3 docs/werkzeuge/registerkopie_abschnitte.py <ziel>
"""
import hashlib, os, re, subprocess, sys

REG = "docs/VORREGISTRIERUNG_neuselektion.md"
ziel = sys.argv[1]
git = lambda *a: subprocess.run(["git", "--no-optional-locks", *a], capture_output=True, check=True).stdout
orig = git("show", "HEAD:" + REG)
if open(REG, "rb").read() != orig:
    print("Arbeitsbaum != HEAD"); sys.exit(2)
commit, datum = git("log", "-1", "--format=%H %cs", "--", REG).decode().split()
sha = hashlib.sha256(orig).hexdigest()
zeilen = orig.splitlines(keepends=True)
starts = [i for i, z in enumerate(zeilen) if re.match(rb"^## (\d+)\.", z)]
nums = [int(re.match(rb"^## (\d+)\.", zeilen[i]).group(1)) for i in starts]
if nums != list(range(len(nums))):
    print("Abschnittsnummern nicht fortlaufend"); sys.exit(2)
starts[0] = 0
grenzen = starts + [len(zeilen)]
os.makedirs(ziel, exist_ok=True)
body_alle = b""
for k, n in enumerate(nums):
    a, b = grenzen[k], grenzen[k + 1]
    body = b"".join(zeilen[a:b])
    body_alle += body
    kopf = (f"# REGISTER-KOPIE Abschnitt {n} (von 0–{nums[-1]}) — Register-Z. {a + 1}–{b} — Commit {commit} — "
            f"{datum} — Original sha256 {sha} — KOPIE, nicht das Register\n\n").encode()
    with open(os.path.join(ziel, f"REGISTER_KOPIE_ABSCHNITT_{n:02d}.md"), "wb") as f:
        f.write(kopf + body)
    print(f"{n:02d} Z. {a + 1}-{b} {len(kopf) + len(body)} B")
# Pruefung aus den geschriebenen Dateien
neu = b""
for n in nums:
    d = open(os.path.join(ziel, f"REGISTER_KOPIE_ABSCHNITT_{n:02d}.md"), "rb").read()
    neu += d.split(b"\n", 2)[2]
ok = neu == orig and body_alle == orig
print("PRUEFUNG", "BYTEGLEICH" if ok else "UNGLEICH", len(nums), "Dateien, sha256", sha[:16])
sys.exit(0 if ok else 1)
