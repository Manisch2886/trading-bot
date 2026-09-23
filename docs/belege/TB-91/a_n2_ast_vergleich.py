"""TB-91 A-N2: AST-Vergleich aller Funktionen von benchmark.py, vorher gegen nachher.

Aufruf: python3 docs/belege/TB-91/a_n2_ast_vergleich.py <vorher.py> <nachher.py>
Vorher = git show d23bdd1:research/vorregistrierung/benchmark.py
Verglichen wird ast.dump des Funktionskoerpers (ohne Docstring-Sonderbehandlung:
der Docstring gehoert zum Koerper und zaehlt mit).
"""
import ast
import hashlib
import sys

GESPERRT = ("bh_tagesrenditen", "drawdown_bei_exposure", "nachschlagen", "erlaubt")


def funktionen(pfad):
    baum = ast.parse(open(pfad, encoding="utf-8").read())
    return {n.name: ast.dump(n) for n in baum.body if isinstance(n, ast.FunctionDef)}


vorher, nachher = funktionen(sys.argv[1]), funktionen(sys.argv[2])
print("Gesperrte Rechenfunktionen (23.5):")
alle_gleich = True
for name in GESPERRT:
    a, b = vorher.get(name), nachher.get(name)
    if a is None or b is None:
        urteil = "FEHLT"
        alle_gleich = False
    elif a == b:
        urteil = "GLEICH"
    else:
        urteil = "GEAENDERT"
        alle_gleich = False
    h = hashlib.sha256((b or "").encode()).hexdigest()[:16]
    print(f"  {name:24s} {urteil:10s} {h}")
print("\nUebrige Funktionen:")
for name in sorted(set(vorher) | set(nachher)):
    if name in GESPERRT:
        continue
    if name not in vorher:
        u = "NEU"
    elif name not in nachher:
        u = "ENTFERNT"
    else:
        u = "gleich" if vorher[name] == nachher[name] else "GEAENDERT"
    print(f"  {name:24s} {u}")
print(f"\nmedian in vorher: {'median' in vorher}, in nachher: {'median' in nachher}")
print(f"\nERGEBNIS: vier gesperrte Funktionen {'alle GLEICH' if alle_gleich else 'NICHT alle gleich'}")
sys.exit(0 if alle_gleich else 1)
