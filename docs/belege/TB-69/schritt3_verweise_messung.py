import re, os, sys, collections
ROOT='.'
SECT=r'(5b|6bb|6b|6c|6d|7b|7c|1[0-8]|[1-9])'
# Verweis = ARBEITSWEISE + Abschnittsangabe in derselben Zeile, in dieser Form:
#   ARBEITSWEISE.md` Abschnitt N | ARBEITSWEISE.md` §N | ARBEITSWEISE.md` N | ARBEITSWEISE §N | Abschnitt N ... ARBEITSWEISE
pat=re.compile(r'ARBEITSWEISE(?:\.md)?`?\s*(?:,\s*)?(?:Abschnitte?|§|Regel)?\s*'+SECT+r'\b(?![.,]\d)|Abschnitte?\s+'+SECT+r'[^|]{0,60}ARBEITSWEISE', re.U)
# innerhalb ARBEITSWEISE.md: Selbstverweise "Abschnitt N" / "Abschnitte N, M"
selfpat=re.compile(r'Abschnitte?\s+'+SECT+r'\b(?![.,]\d)')
counts=collections.OrderedDict(); total=0; letter=0
letterpat=re.compile(r'\b(5b|6bb|6b|6c|6d|7b|7c)\b')
for dp,dn,fn in os.walk(ROOT):
    if 'trading-env' in dp or '.git' in dp: continue
    for f in fn:
        p=os.path.join(dp,f)
        try: txt=open(p,encoding='utf-8',errors='replace').read().splitlines()
        except: continue
        hits=[]
        for i,l in enumerate(txt,1):
            if p.endswith('projektfuehrung/ARBEITSWEISE.md'):
                if selfpat.search(l) or pat.search(l): hits.append((i,l))
            elif pat.search(l): hits.append((i,l))
        if hits:
            counts[p]=hits
for p,h in sorted(counts.items(), key=lambda x:-len(x[1])):
    lt=sum(1 for i,l in h if letterpat.search(l))
    total+=len(h); letter+=lt
    print(f"{len(h):3d} Zeilen ({lt} mit Buchstabenabschnitt)  {p}")
print(f"\nSUMME: {total} Zeilen in {len(counts)} Dateien, davon {letter} mit Buchstabenabschnitt")
if '-v' in sys.argv:
    print("\n== Zeilen ==")
    for p,h in counts.items():
        for i,l in h: print(f"{p}:{i}: {l[:200]}")
