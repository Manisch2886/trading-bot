#!/usr/bin/env python3
"""TB-64, Schritt 3 - Gegenprobe: vier Mutationen am Waechter, je in einer
Kopie unter $TMPDIR; der Selbsttest muss bei jeder rot werden.
(Uebergabeprotokoll Abschnitt 7, Punkt 12: eine gruene Pruefung ist erst
etwas wert, wenn belegt ist, dass sie auch rot werden kann.)"""
import os, re, shutil, subprocess, sys, tempfile

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SYSTEM = os.path.join(WURZEL, "system")
MUTATIONEN = [
    ("A  schliessender Balken im K-Muster",
     'RE_K = re.compile(r"^\\| \\*\\*(K\\d[a-z])\\*\\*")',
     'RE_K = re.compile(r"^\\| \\*\\*(K\\d[a-z])\\*\\* \\|")'),
    ("B  sort -u (set) in der Doppelbelegung",
     "            for nummer in liste:",
     "            for nummer in sorted(set(liste)):"),
    ("C  Kernpruefung abgeschaltet - die Nummer genuegt",
     "        if kerntext and any(kerntext in normiere(z) for z in gleiche):",
     "        if gleiche:"),
    ("D  Vergabevermerk ohne Bindung an den Nachtrag",
     "            if not any(k in zeile for k in kennzeichen):",
     "            if False:"),
]
print(f"Interpreter: {sys.executable}")
for titel, alt, neu in MUTATIONEN:
    ordner = tempfile.mkdtemp(prefix="tb64_mutation_")
    try:
        for name in ("nachtragswaechter.py", "test_nachtragswaechter.py"):
            shutil.copy(os.path.join(SYSTEM, name), ordner)
        pfad = os.path.join(ordner, "nachtragswaechter.py")
        quelle = open(pfad, encoding="utf-8").read()
        assert quelle.count(alt) == 1, (titel, quelle.count(alt))
        open(pfad, "w", encoding="utf-8").write(quelle.replace(alt, neu))
        p = subprocess.run([sys.executable, os.path.join(ordner, "test_nachtragswaechter.py")],
                           capture_output=True, text=True)
        rot = [z.strip() for z in p.stdout.splitlines() if "[FEHLER]" in z]
        bilanz = next((z for z in p.stdout.splitlines() if "bestanden" in z), "?")
        print(f"\nMutation {titel}\n  rc={p.returncode}  {bilanz}")
        for z in rot:
            print(f"  {z}")
        if p.returncode == 0:
            print("  !!! DIE MUTATION WURDE NICHT ERKANNT")
    finally:
        shutil.rmtree(ordner, ignore_errors=True)
