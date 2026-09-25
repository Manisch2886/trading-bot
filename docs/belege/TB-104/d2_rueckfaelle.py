"""TB-104 D2 - das Rueckfall-Inventar aus TB-103 (docs/belege/TB-103/a4_rueckfaelle.txt)
gegen den gemessenen Laufbereich (D1) legen: je Fundstelle "im Laufbereich ja/nein" und
welcher Lauf-Typ die Datei laedt. NICHTS wird geaendert.

Eingaben:  <inventar>  docs/belege/TB-103/a4_rueckfaelle.txt
           <liste>...  je Lauf-Typ eine Datei "<lauftyp>\\t<repo-relativer Pfad>" (d1_laufbereich_*.txt,
                       Abschnitt LISTE), erzeugt von d1_listen.py
Fundstellen mit Stern (strategies/*/...) oder Aufzaehlung ({a,b}) werden gegen die Liste
aufgeloest; die Zeile gilt als "ja", wenn mindestens eine ihrer Dateien geladen wird, und
nennt dann genau diese Dateien. Zeilennummern werden nicht geprueft (Stand d05e3ff).

Aufruf:  python3 d2_rueckfaelle.py <inventar> <liste> [<liste> ...]
"""
import fnmatch
import re
import sys

inventar, listen = sys.argv[1], sys.argv[2:]
geladen = {}                                   # pfad -> {lauftyp}
for datei in listen:
    for z in open(datei, encoding="utf-8"):
        if "\t" not in z or z.startswith("#"):
            continue
        typ, pfad = z.rstrip("\n").split("\t", 1)
        geladen.setdefault(pfad, set()).add(typ)


def aufloesen(ausdruck):
    """'strategies/{a,b}/x.py' -> ['strategies/a/x.py', 'strategies/b/x.py']."""
    m = re.search(r"\{([^}]*)\}", ausdruck)
    if not m:
        return [ausdruck]
    aus = []
    for teil in m.group(1).split(","):
        aus += aufloesen(ausdruck[:m.start()] + teil.strip() + ausdruck[m.end():])
    return aus


def dateien_der_zeile(kopf):
    """Die Dateimuster einer Inventarzeile (erste Spalte), ohne Zeilenangaben."""
    kopf = re.sub(r"\(.*?\)", "", kopf)
    muster = []
    for roh in re.split(r"[;]| \+ ", kopf):
        for stueck in re.split(r",\s*(?=[a-z_]+[/.])", roh.strip()):
            stueck = stueck.strip()
            m = re.match(r"([A-Za-z0-9_./*{},-]+\.py)", stueck)
            if m:
                muster += aufloesen(m.group(1))
    return muster


print("# TB-104 D2 - Rueckfall-Inventar TB-103 (a4_rueckfaelle.txt) gegen den Laufbereich (D1)")
print("# Laufbereich = Vereinigung der geladenen Repo-Module aus: %s" % ", ".join(listen))
print("# Spalten: Nr | Fundstelle (Inventar, gekuerzt) | im Laufbereich | geladen von (Lauf-Typ: Datei)")
print()
nr = 0
ja = nein = 0
for z in open(inventar, encoding="utf-8"):
    if " | " not in z or z.startswith(("Datei:Zeile", "#", "-")):
        continue
    kopf = z.split(" | ")[0].strip()
    muster = dateien_der_zeile(kopf)
    if not muster:
        continue
    nr += 1
    treffer = {}
    for mu in muster:
        for pfad, typen in geladen.items():
            if fnmatch.fnmatch(pfad, mu):
                treffer[pfad] = typen
    im = "JA" if treffer else "nein"
    ja += bool(treffer)
    nein += not treffer
    wer = "; ".join("%s: %s" % ("/".join(sorted(t)), p) for p, t in sorted(treffer.items()))
    print("%2d | %s | %s | %s" % (nr, kopf[:110], im, wer or "-"))
print()
print("Summe: %d Fundstellen-Zeilen, %d im Laufbereich, %d nicht" % (nr, ja, nein))
