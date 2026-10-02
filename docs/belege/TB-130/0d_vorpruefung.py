#!/usr/bin/env python3
"""TB-130 0d - Vorpruefung vor jedem Registereintrag, alles am Commit S0 (Bauart TB-129 0d_vorpruefung.py).

Aufruf aus der Repo-Wurzel:  trading-env/bin/python3 docs/belege/TB-130/0d_vorpruefung.py <S0> <scratch>
- Packt den Baum am Commit S0 mit `git archive` nach <scratch>/tb130_s0/ (nur die Pfade, die Anhang A nennt;
  die Dateimuster aus `glob_zaehlungen` werden ueber `git ls-tree` am Commit aufgeloest).
- Schneidet das Pruefskript aus Anhang A des Auftrags (am Commit S0) heraus, legt es als
  docs/belege/TB-130/pruefe_anhang_tb130.py ab und ruft es gegen den ausgepackten Baum auf
  (Nr. 1 Marken, Nr. 2 Quelle, Nr. 3 '## 52.' und '> R63 — ', Nr. 4 Fundstellen, Zaehlungen, glob_zaehlungen).
- Gibt Nr. 1 bis 4 zusaetzlich je Eintrag aus.
rc 0 = alles wie angegeben; rc 1 = Abweichung (Abbruch vor Schritt A).
"""
import fnmatch, json, os, re, subprocess, sys

S0, SP = sys.argv[1], sys.argv[2]
AUFTRAG = "docs/auftraege/MAC_TB-130_register_fable_02a.md"
BL = "docs/belege/TB-130"
PY = "trading-env/bin/python3"


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


fehler = []
auftrag = git("show", f"{S0}:{AUFTRAG}")
daten = json.loads(auftrag.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])

# Pruefskript aus Anhang A schneiden (erster ```python-Block nach "Prüfskript (liest den JSON-Block")
teil = auftrag.split("Prüfskript (liest den JSON-Block", 1)[1]
skript = teil.split("```python\n", 1)[1].split("\n```\n", 1)[0] + "\n"
open(f"{BL}/pruefe_anhang_tb130.py", "w", encoding="utf-8").write(skript)

# Baum am Commit S0 auspacken
alle = git("ls-tree", "-r", "--name-only", S0).split("\n")
glob_pfade = {p for gl, _, _, _ in daten["glob_zaehlungen"] for p in alle if fnmatch.fnmatch(p, gl) and p.count("/") == gl.count("/")}
pfade = sorted({daten["register"], daten["quelle"]["pfad"], *(d for d, _, _ in daten["fundstellen"]),
                *(d for d, _, _ in daten["zaehlungen"]), *daten["kalender"]["dateien"], *glob_pfade})
ziel = os.path.join(SP, "tb130_s0")
subprocess.run(["rm", "-rf", ziel], check=True)
os.makedirs(ziel)
arch = subprocess.run(["git", "archive", S0, *pfade], capture_output=True, check=True).stdout
subprocess.run(["tar", "-x", "-C", ziel], input=arch, check=True)
print(f"# TB-130 0d Vorpruefung am Commit {S0} ({git('rev-parse', S0).strip()})")
print(f"Baum am Commit ausgepackt: {len(pfade)} Dateien nach {ziel}")
for p in pfade:
    print("  ", p)

# Auftrag am Commit S0 als Datei fuer das Pruefskript
amd = os.path.join(SP, "tb130_auftrag_s0.md")
open(amd, "w", encoding="utf-8").write(auftrag)

print("## Nr. 1-4: Pruefskript aus Anhang A gegen den Baum am Commit")
r = subprocess.run([PY, f"{BL}/pruefe_anhang_tb130.py", amd, ziel], capture_output=True, text=True)
print(r.stdout.rstrip())
if r.stderr.strip():
    print("stderr:", r.stderr.rstrip())
print(f"Pruefskript rc {r.returncode}")
if r.returncode != 0:
    fehler.append("Pruefskript Anhang A rc != 0")

# Je Marke einzeln (Nr. 1, ausfuehrlich)
reg = git("show", f"{S0}:{daten['register']}")
L = reg.split("\n")
print("## Nr. 1 je Marke")
for m in daten["marken"]:
    n = reg.count(m["anker"])
    ok_a = L[m["ankerzeile"] - 1].startswith(m["anker"])
    ok_n = L[m["nach"] - 1].startswith(m["anfang40"])
    print(f"Nr {m['nr']:2d} R{m['R']}: Anker {n}x, Ankerzeile {m['ankerzeile']} {'ja' if ok_a else 'NEIN'}, "
          f"nach Z. {m['nach']} {'ja' if ok_n else 'NEIN'}")
    if not (n == 1 and ok_a and ok_n):
        fehler.append(f"Marke Nr {m['nr']} weicht ab")

print("## Nr. 2")
q = daten["quelle"]
qroh = subprocess.run(["git", "show", f"{S0}:{q['pfad']}"], capture_output=True, check=True).stdout
import hashlib
print(f"Quelle md5 {hashlib.md5(qroh).hexdigest()} (Soll {q['md5']}), {len(qroh)} B (Soll {q['bytes']})")
if hashlib.md5(qroh).hexdigest() != q["md5"] or len(qroh) != q["bytes"]:
    fehler.append("Quelle md5/Bytes")
z = qroh.decode("utf-8").split("\n")
starts = [i for i in range(q["von"], q["bis"] + 1) if re.match(r"^R(\d+) — ", z[i - 1])]
print(f"Blockanfaenge in Z. {q['von']}-{q['bis']}: " + ", ".join(f"Z. {i} {z[i-1].split(' ', 1)[0]}" for i in starts))

print("## Nr. 3")
n52 = reg.count("## 52.")
n63 = sum(s.startswith("> R63 — ") for s in L)
print(f"'## 52.' im Register: {n52} (Soll 0); Zeilen mit '> R63 — ': {n63} (Soll 0)")
if n52 or n63:
    fehler.append("Nr. 3")

print("## Nr. 4 je Eintrag")
for d, znr, teilk in daten["fundstellen"]:
    zl = git("show", f"{S0}:{d}").split("\n")
    ok = znr <= len(zl) and teilk in zl[znr - 1]
    print(f"{d}:{znr} enthaelt {teilk!r}: {'ja' if ok else 'NEIN'}")
    if not ok:
        fehler.append(f"Fundstelle {d}:{znr}")
for d, muster, soll in daten["zaehlungen"]:
    ist = len(re.findall(muster, git("show", f"{S0}:{d}"), re.M))
    print(f"{d} /{muster}/: {ist} (Soll {soll}) {'ja' if ist == soll else 'NEIN'}")
    if ist != soll:
        fehler.append(f"Zaehlung {d}")
for gl, muster, soll, dateien in daten["glob_zaehlungen"]:
    pf = sorted(p for p in glob_pfade if fnmatch.fnmatch(p, gl))
    print(f"{gl}: {len(pf)} Dateien (Soll {dateien})")
    if len(pf) != dateien:
        fehler.append(f"Glob {gl}")
    for p in pf:
        ist = len(re.findall(muster, git("show", f"{S0}:{p}"), re.M))
        print(f"  {p} /{muster}/: {ist} (Soll {soll}) {'ja' if ist == soll else 'NEIN'}")
        if ist != soll:
            fehler.append(f"Zaehlung {p}")

if fehler:
    print("ABBRUCH:", fehler)
    sys.exit(1)
print("rc 0: alles wie angegeben")
