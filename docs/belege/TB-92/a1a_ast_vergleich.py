"""TB-92 A1a-4: AST von auswertung.py, HEAD gegen Arbeitsbaum.
Vergleicht (1) jede Funktion/Klasse (auch verschachtelt, ast.walk) per ast.dump,
(2) die Anweisungen auf Modulebene. Druckt jede Abweichung."""
import ast, subprocess, sys
PFAD = "research/vorregistrierung/auswertung.py"
rev = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
alt = ast.parse(subprocess.run(["git", "show", f"{rev}:{PFAD}"], capture_output=True,
                               text=True, check=True).stdout)
neu = ast.parse(open(PFAD, encoding="utf-8").read())
def defs(baum):
    return {n.name: ast.dump(n) for n in ast.walk(baum)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
da, dn = defs(alt), defs(neu)
gleich = [k for k in da if dn.get(k) == da[k]]
anders = [k for k in da if k in dn and dn[k] != da[k]]
print(f"Funktionen/Klassen: HEAD {len(da)}, neu {len(dn)}, gleich {len(gleich)}, "
      f"verschieden {len(anders)}, nur HEAD {sorted(set(da)-set(dn))}, nur neu {sorted(set(dn)-set(da))}")
for k in anders:
    print(f"  VERSCHIEDEN: {k}")
def modul(baum):
    return [(ast.dump(n), n) for n in baum.body if not isinstance(n, (ast.FunctionDef, ast.ClassDef))]
ma, mn = modul(alt), modul(neu)
sa, sn = {d for d, _ in ma}, {d for d, _ in mn}
neu_nur = [n for d, n in mn if d not in sa]; alt_nur = [n for d, n in ma if d not in sn]
print(f"Modulebene (ohne def/class): HEAD {len(ma)}, neu {len(mn)}; nur neu {len(neu_nur)}, nur HEAD {len(alt_nur)}")
for n in neu_nur:
    print(f"  NUR NEU ({type(n).__name__}):", ast.unparse(n))
for n in alt_nur:
    print(f"  NUR HEAD ({type(n).__name__}):", ast.unparse(n))
# Die eine verschiedene Funktion: welche Knoten unterscheiden sich?
import difflib
for k in anders:
    fa = [n for n in ast.walk(alt) if getattr(n, "name", None) == k][0]
    fn = [n for n in ast.walk(neu) if getattr(n, "name", None) == k][0]
    ua, un = ast.unparse(fa).splitlines(), ast.unparse(fn).splitlines()
    print(f"  Unterschied in {k} (ast.unparse):")
    for z in difflib.unified_diff(ua, un, lineterm="", n=0):
        if not z.startswith(("---", "+++", "@@")):
            print("    " + z)
