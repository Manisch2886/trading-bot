import ast, hashlib, sys
vorher, nachher = sys.argv[1], sys.argv[2]
def fns(p):
    t = ast.parse(open(p, encoding="utf-8").read())
    return t, {n.name: n for n in ast.walk(t) if isinstance(n, ast.FunctionDef)}
tv, fv = fns(vorher); tn, fn = fns(nachher)
print("Python", sys.version.split()[0])
ACHT = ["universum","lies","rsi","adx","rma","je_zeitrahmen","haltedauern","datenbereiche"]
for n in ACHT:
    a = ast.dump(fv[n]); b = ast.dump(fn[n])
    print("  %-14s %s  %s" % (n, "GLEICH " if a == b else "ANDERS ", hashlib.sha256(a.encode()).hexdigest()[:16]))
print("  nur vorher:", sorted(set(fv)-set(fn)))
print("  nur nachher:", sorted(set(fn)-set(fv)))
print("  geaendert:", sorted(k for k in set(fv)&set(fn) if ast.dump(fv[k])!=ast.dump(fn[k])))
def dumps(t, src):
    out=[]
    for node in ast.walk(t):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr=="dump" and getattr(node.func.value,"id",None)=="json":
            out.append((node.lineno, ast.get_source_segment(src, node), ast.dump(node)))
    return out
sv=open(vorher,encoding="utf-8").read(); sn=open(nachher,encoding="utf-8").read()
dv=dumps(tv,sv); dn=dumps(tn,sn)
print("  json.dump vorher :", [(l,s) for l,s,_ in dv])
print("  json.dump nachher:", [(l,s) for l,s,_ in dn])
print("  zeichengleich (Quelltext):", len(dv)==len(dn)==1 and dv[0][1]==dn[0][1])
print("  AST gleich:", len(dv)==len(dn)==1 and dv[0][2]==dn[0][2])
# Schreibziele
for lbl,t in (("vorher",tv),("nachher",tn)):
    calls=[]
    for node in ast.walk(t):
        if isinstance(node, ast.Call):
            f=node.func; name = f.attr if isinstance(f,ast.Attribute) else getattr(f,"id",None)
            if name in ("open","dump","to_csv","to_json","write_text","write_bytes","fdopen","makedirs"):
                calls.append((node.lineno,name))
    print("  Schreib-/Oeffnungsaufrufe", lbl, sorted(calls))
