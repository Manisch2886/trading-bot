"""TB-98 B3: AST von positionen_holen.py und alle_bots.py, e87b06f gegen
Arbeitsbaum (Bauart TB-92 a1a_ast_vergleich.py). Vergleicht (1) jede
Funktion/Klasse per ast.dump, (2) die Anweisungen auf Modulebene, und druckt
jede Abweichung als ast.unparse-Differenz. Docstrings zaehlen mit.

Aufruf (Repo-Wurzel, Python >= 3.9):  python3 b_ast_vergleich.py [rev]
"""
import ast
import difflib
import subprocess
import sys

rev = sys.argv[1] if len(sys.argv) > 1 else "e87b06f"
for PFAD in ("research/tb24_haltedauern/positionen_holen.py",
             "research/tb24_haltedauern/alle_bots.py"):
    alt = ast.parse(subprocess.run(["git", "show", f"{rev}:{PFAD}"], capture_output=True,
                                   text=True, check=True).stdout)
    neu = ast.parse(open(PFAD, encoding="utf-8").read())

    def defs(baum):
        return {n.name: n for n in ast.walk(baum)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}

    da, dn = defs(alt), defs(neu)
    gleich = sorted(k for k in da if k in dn and ast.dump(dn[k]) == ast.dump(da[k]))
    anders = sorted(k for k in da if k in dn and ast.dump(dn[k]) != ast.dump(da[k]))
    print(f"=== {PFAD}  ({rev} gegen Arbeitsbaum)")
    print(f"Funktionen/Klassen: {rev} {len(da)}, neu {len(dn)}, gleich {len(gleich)}, "
          f"verschieden {len(anders)}")
    print(f"  gleich:        {gleich}")
    print(f"  verschieden:   {anders}")
    print(f"  nur {rev}:   {sorted(set(da) - set(dn))}")
    print(f"  nur neu:       {sorted(set(dn) - set(da))}")
    for k in anders:
        ua, un = ast.unparse(da[k]).splitlines(), ast.unparse(dn[k]).splitlines()
        print(f"  Unterschied in {k} (ast.unparse):")
        for z in difflib.unified_diff(ua, un, lineterm="", n=0):
            if not z.startswith(("---", "+++")):
                print("    " + z)

    def modul(baum):
        return [n for n in baum.body
                if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]

    ma = [ast.unparse(n) for n in modul(alt)]
    mn = [ast.unparse(n) for n in modul(neu)]
    print(f"Modulebene (ohne def/class): {rev} {len(ma)}, neu {len(mn)} Anweisungen")
    for z in difflib.unified_diff(ma, mn, lineterm="", n=0):
        if not z.startswith(("---", "+++")):
            for zz in z.splitlines():
                print("    " + (zz if len(zz) < 160 else zz[:157] + "..."))
    print()
