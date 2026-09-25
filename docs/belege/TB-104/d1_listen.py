"""TB-104 D1 - die Menge der geladenen REPO-Module je Lauf-Typ (Laufbereich, Fable 25a
Abschnitt 4), aus den Protokollen des Hakens docs/belege/TB-104/haken/sitecustomize.py.

Zwei Quellen je Prozess, beide ausgewiesen:
  (a) die Modulliste beim Prozessende (sys.modules, __file__; Bytecode ueber
      importlib.util.source_from_cache auf die Quelle zurueckgefuehrt)
  (b) die Oeffnungen von .py-Dateien und von Bytecode (.pyc, auch unter dem
      Apple-Cache ~/Library/Caches/com.apple.python/<pfad>/__pycache__/), auf die
      Quelle zurueckgefuehrt - fuer Prozesse, die ohne atexit enden (os._exit),
      und als Gegenprobe zu (a).
  (c) der Einstiegspunkt aus der Zeile "#argv" (ausgefuehrt; `__main__` traegt beim
      Prozessende kein `__file__` mehr).
Je Prozess zaehlt (a) - oder, wo die Modulliste fehlt, (b) -, dazu (c). Ein .py, das in
einem Prozess MIT Modulliste geoeffnet, dort aber nicht geladen wurde, ist als DATEN
gelesen (z. B. MIN_HISTORY_* aus multi_symbol_optimise.py); es wird getrennt ausgewiesen
und zaehlt nur, wenn ein anderer Prozess es laedt.

Aufruf:  python3 d1_listen.py <repo> <lauftyp> <lauf-ordner> [<lauf-ordner> ...]
Ausgabe: Kopf, Zaehlungen, dann Abschnitt LISTE mit Zeilen "<lauftyp>\\t<repo-relativer Pfad>".
"""
import glob
import os
import re
import sys

repo = os.path.realpath(sys.argv[1])
typ = sys.argv[2]
laeufe = sys.argv[3:]
ENV = os.path.join(repo, "trading-env")
CACHE = os.path.expanduser("~/Library/Caches/com.apple.python")


def quelle_aus_bytecode(p):
    if p.startswith(CACHE + os.sep):
        p = p[len(CACHE):]
    p = p.replace(os.sep + "__pycache__" + os.sep, os.sep)
    return re.sub(r"\.cpython-\d+(\.opt-\d)?\.pyc$", ".py", p)


def im_repo(p):
    return p.startswith(repo + os.sep) and not p.startswith(ENV + os.sep)


liste_a, liste_b, als_daten, laufbereich, einstieg = set(), set(), set(), set(), set()
prozesse = ohne_liste = 0
for lauf in laeufe:
    for datei in sorted(glob.glob(os.path.join(lauf, "prot", "*.tsv"))):
        if datei.endswith(".module.tsv"):
            continue
        prozesse += 1
        pid = os.path.basename(datei)[:-4]
        a = set()
        modul = os.path.join(lauf, "prot", pid + ".module.tsv")
        if os.path.exists(modul):
            for z in open(modul, encoding="utf-8"):
                q = z.rstrip("\n").split("\t")[1]
                if q != "-":
                    q = os.path.realpath(q)
                    if im_repo(q):
                        a.add(q)
        else:
            ohne_liste += 1
        b = set()
        for z in open(datei, encoding="utf-8", errors="replace"):
            if z.startswith("#argv\t"):
                erstes = z.rstrip("\n").split("\t", 1)[1].split(" ")[0]
                if erstes.endswith(".py"):
                    e = os.path.realpath(os.path.join(repo, erstes))
                    if im_repo(e):
                        einstieg.add(e)
                continue
            teile = z.rstrip("\n").split("\t")
            if len(teile) < 4 or teile[0] != "open":
                continue
            p = teile[2]
            if p.endswith(".pyc"):
                p = quelle_aus_bytecode(p)
            elif not p.endswith(".py"):
                continue
            p = os.path.realpath(p)
            if im_repo(p):
                b.add(p)
        if os.path.exists(modul):
            als_daten |= b - a
            laufbereich |= a
        else:
            laufbereich |= b
        liste_a |= a
        liste_b |= b
laufbereich |= einstieg
als_daten -= laufbereich


def rel(p):
    return os.path.relpath(p, repo)


print("# TB-104 D1 Laufbereich '%s' - Laeufe: %s" % (typ, ", ".join(laeufe)))
print("# Prozesse %d, davon ohne Modulliste %d (Prozess konnte sie beim Ende nicht schreiben: os._exit oder eigener Schreibschutz wie loaderlauf.py)" % (prozesse, ohne_liste))
print("# (a) Modulliste: %d Repo-Module; (b) aus Oeffnungen: %d; (b) ohne (a) = als Daten gelesen: %d"
      % (len(liste_a), len(liste_b), len(als_daten)))
print("# (a) ohne (b) (geladen, aber keine Oeffnung protokolliert - z. B. vor dem Haken): %d"
      % len(liste_a - liste_b))
for p in sorted(liste_a - liste_b):
    print("#    %s" % rel(p))
print("# (c) Einstiegspunkte (ausgefuehrt): %d" % len(einstieg))
for p in sorted(einstieg):
    print("#    %s" % rel(p))
print("# Quelltext als DATEN gelesen und in keinem Prozess geladen (nicht im Laufbereich):")
for p in sorted(als_daten):
    print("#    %s" % rel(p))
print("# Laufbereich (Vereinigung): %d Repo-Module" % len(laufbereich))
print("LISTE")
for p in sorted(laufbereich):
    print("%s\t%s" % (typ, rel(p)))
