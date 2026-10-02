#!/usr/bin/env python3
"""TB-129 0d - Vorpruefung vor jedem Registereintrag, alles am Commit S0.

Aufruf aus der Repo-Wurzel:  trading-env/bin/python3 docs/belege/TB-129/0d_vorpruefung.py <S0> <scratch>
- Packt den Baum am Commit S0 mit `git archive` nach <scratch>/tb129_s0/ (nur die Pfade, die Anhang A nennt).
- Schneidet das Pruefskript aus Anhang A des Auftrags (am Commit S0) heraus, legt es als
  docs/belege/TB-129/pruefe_anhang_tb129.py ab und ruft es gegen den ausgepackten Baum auf
  (Nr. 1 Marken, Nr. 2 Quelle, Nr. 3 '## 51.' und '> R56 — ', Nr. 4 Fundstellen, Zaehlungen, Kalender).
- Nr. 4, Git-Tatsachen: je Datei die Commits aus `git log --format=%h S0 -- <datei>`; Ueberschrift
  'Fassung 2' am eaea530, 'Fassung 3' erst am 7238842; Commit-Datum `git log -1 --format=%cs` je Commit.
rc 0 = alles wie angegeben; rc 1 = Abweichung (Abbruch vor Schritt A).
"""
import json, os, subprocess, sys

S0, SP = sys.argv[1], sys.argv[2]
AUFTRAG = "docs/auftraege/MAC_TB-129_register_fable_01a.md"
BL = "docs/belege/TB-129"
PY = "trading-env/bin/python3"


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


fehler = []
auftrag = git("show", f"{S0}:{AUFTRAG}")
daten = json.loads(auftrag.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])

# Pruefskript aus Anhang A schneiden (erster ```python-Block nach "Prüfskript (liest den JSON-Block")
teil = auftrag.split("Prüfskript (liest den JSON-Block", 1)[1]
skript = teil.split("```python\n", 1)[1].split("\n```\n", 1)[0] + "\n"
open(f"{BL}/pruefe_anhang_tb129.py", "w", encoding="utf-8").write(skript)

# Baum am Commit S0 auspacken
pfade = sorted({daten["register"], daten["quelle"]["pfad"], *(d for d, _, _ in daten["fundstellen"]),
                *(d for d, _, _ in daten["zaehlungen"]), *daten["kalender"]["dateien"]})
ziel = os.path.join(SP, "tb129_s0")
subprocess.run(["rm", "-rf", ziel], check=True)
os.makedirs(ziel)
arch = subprocess.run(["git", "archive", S0, *pfade], capture_output=True, check=True).stdout
subprocess.run(["tar", "-x", "-C", ziel], input=arch, check=True)
print(f"# TB-129 0d Vorpruefung am Commit {S0} ({git('rev-parse', S0).strip()})")
print(f"Baum am Commit ausgepackt: {len(pfade)} Dateien nach {ziel}")
for p in pfade:
    print("  ", p)

# Auftrag am Commit S0 als Datei fuer das Pruefskript
amd = os.path.join(SP, "tb129_auftrag_s0.md")
open(amd, "w", encoding="utf-8").write(auftrag)

print("## Nr. 1-4: Pruefskript aus Anhang A gegen den Baum am Commit")
r = subprocess.run([PY, f"{BL}/pruefe_anhang_tb129.py", amd, ziel], capture_output=True, text=True)
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
print("## Nr. 3")
print(f"'## 51.' im Register: {reg.count('## 51.')} (Soll 0); Zeilen mit '> R56 — ': "
      f"{sum(s.startswith('> R56 — ') for s in L)} (Soll 0)")

print("## Nr. 4, Git-Tatsachen")
for g in daten["git_tatsachen"]:
    ist = git("log", "--format=%h", S0, "--", g["datei"]).split()
    ok = ist == g["commits"]
    print(f"{g['datei']}: Commits {ist} (Soll {g['commits']}) {'ja' if ok else 'NEIN'}")
    if not ok:
        fehler.append(f"Commits {g['datei']}")
    for c, kern in g.get("ueberschrift_am", {}).items():
        txt = git("show", f"{c}:{g['datei']}")
        treffer = [s for s in txt.split("\n") if s.startswith("#") and kern in s]
        print(f"  am {c}: Ueberschrift mit {kern!r}: {len(treffer)}x {treffer[:1]}")
        if len(treffer) < 1:
            fehler.append(f"Ueberschrift {kern!r} fehlt am {c}")
    # 'Fassung 3' erst am 7238842: am eaea530 keine solche Ueberschrift
    if "ueberschrift_am" in g:
        alt = git("show", f"eaea530:{g['datei']}")
        n3 = sum(1 for s in alt.split("\n") if s.startswith("#") and "— Fassung 3 (" in s)
        print(f"  am eaea530: Ueberschrift mit '— Fassung 3 (': {n3}x (Soll 0)")
        if n3 != 0:
            fehler.append("Fassung 3 schon am eaea530")
for c, soll in daten["commit_datum"].items():
    ist = git("log", "-1", "--format=%cs", c).strip()
    print(f"Commit-Datum {c}: {ist} (Soll {soll}) {'ja' if ist == soll else 'NEIN'}")
    if ist != soll:
        fehler.append(f"Commit-Datum {c}")

if fehler:
    print("ABBRUCH:", fehler)
    sys.exit(1)
print("rc 0: alles wie angegeben")
