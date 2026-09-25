"""TB-105 A5: wo werden RESULTS_DIR / LOGS_DIR (aus get_strategy_paths) benutzt, und in welchem Kontext?
Liest Quelltext (AST), fuehrt nichts aus. Kontext: 'main' = im Block if __name__ == "__main__",
'modul' = Modulebene ausserhalb davon, sonst der Funktionsname. Schreibend = die Zeile enthaelt
to_csv/open(/savefig/to_json/write/FileHandler/basicConfig, sonst 'Pfad'."""
import ast, glob, os, re, sys
W = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
os.chdir(W)
SCHREIB = re.compile(r"to_csv|open\(|savefig|to_json|\.write|FileHandler|basicConfig|to_parquet|json\.dump")
dateien = sorted(set(glob.glob("strategies/*/*.py") + glob.glob("shared/*.py") + glob.glob("research/**/*.py", recursive=True)
                     + glob.glob("dashboard/*.py") + glob.glob("notifications/*.py") + glob.glob("broker/*.py")))
zeilen = []
for d in dateien:
    if "/test_" in d or d.startswith("trading-env"):
        continue
    try:
        text = open(d, encoding="utf-8").read(); baum = ast.parse(text)
    except Exception:
        continue
    if "RESULTS_DIR" not in text and "LOGS_DIR" not in text:
        continue
    q = text.splitlines()
    kontext = {}
    for k in baum.body:
        if isinstance(k, ast.If) and "__main__" in ast.dump(k.test):
            for n in ast.walk(k):
                if hasattr(n, "lineno"): kontext.setdefault(n.lineno, "main")
    for k in ast.walk(baum):
        if isinstance(k, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for n in ast.walk(k):
                if hasattr(n, "lineno"): kontext[n.lineno] = kontext.get(n.lineno) if kontext.get(n.lineno) not in (None, "main") else k.name
    for n in ast.walk(baum):
        if isinstance(n, ast.Name) and n.id in ("RESULTS_DIR", "LOGS_DIR") and isinstance(n.ctx, ast.Load):
            z = q[n.lineno - 1]
            zeilen.append((d, n.lineno, n.id, kontext.get(n.lineno, "modul"), "SCHREIBT" if SCHREIB.search(z) else "Pfad"))
from collections import Counter
print("# TB-105 A5 Lesestellen von RESULTS_DIR/LOGS_DIR (a5_schreiber.py), %d Stellen in %d Dateien" % (len(zeilen), len({z[0] for z in zeilen})))
c = Counter((z[3] == "main", z[4]) for z in zeilen)
print("# Zusammenfassung (im __main__-Block?, Art):", dict(c))
print("# Stellen AUSSERHALB von __main__ (in Funktionen oder auf Modulebene):")
for z in zeilen:
    if z[3] != "main":
        print("%s:%d %s [%s] %s" % z)
