"""TB-112 A6 - Lese-Audit "Code ungebunden nach E2": jeder LESENDE Zugriff eines Laufs auf eine Datei unter der
Codewurzel (Repo), die NICHT von paths.ARBEITSBAUM_PFADE gedeckt ist. Protokolle des Hakens
docs/belege/TB-104/haken/sitecustomize.py (Zeilen "open<TAB>modus<TAB>pfad<TAB>stapel"), Bauart
docs/belege/TB-109/d_auswerten.py (dieselbe Einteilung lesend/schreibend, Bytecode auf die Quelle zurueckgefuehrt
wie docs/belege/TB-104/d1_listen.py).

Nicht gezaehlt (ausgewiesen): der Snapshot (Daten), trading-env (Umgebung), requirements.lock (Umgebung, ohnehin
gedeckt), paths.REGISTRIERTE_PROTOKOLLE (F8), das Scratchpad, die Messumschlaege unter docs/belege/ (zaehlen
laut Auftrag nicht zum Laufbereich), Zugriffe ausserhalb des Repos.

Gezaehlt, getrennt:
  CODE     .py (auch ueber Bytecode) unter dem Repo, nicht gedeckt  -> erwartet 0, jede Fundstelle ist ein Befund
  SONSTIGE andere Dateien unter dem Repo, nicht gedeckt (z. B. Ergebnis-JSON/CSV als Eingabe) -> nur ausgewiesen,
           E2 bindet Code, nicht Eingaben

Aufruf:  python3 a6_code_audit.py <repo> <scratch> <lauf-ordner> [<lauf-ordner> ...]
Sichtschutz 27.1: nur Pfade und Zahlen.
"""
import collections
import glob
import os
import re
import sys

repo = os.path.realpath(sys.argv[1])
scratch = os.path.realpath(sys.argv[2])
laeufe = sys.argv[3:]
sys.path.insert(0, os.path.join(repo, "shared"))
for _n in ("TB_SELEKTIONSWURZEL", "TB_SELEKTIONSHASH", "TB_SELEKTIONSCOMMIT"):
    os.environ.pop(_n, None)
import paths                                                     # noqa: E402  (ohne Modus)

SNAP = os.path.join(repo, "snapshots")
ENV = os.path.join(repo, "trading-env")
CACHE = os.path.expanduser("~/Library/Caches/com.apple.python")
TUPEL = paths.ARBEITSBAUM_PFADE
PROTOKOLLE = paths.REGISTRIERTE_PROTOKOLLE


def echt(p):
    try:
        return os.path.realpath(p)
    except OSError:
        return p


def quelle_aus_bytecode(p):
    if p.startswith(CACHE + os.sep):
        p = p[len(CACHE):]
    p = p.replace(os.sep + "__pycache__" + os.sep, os.sep)
    return re.sub(r"\.cpython-\d+(\.opt-\d)?\.pyc$", ".py", p)


def gedeckt(rel):
    return any(rel == e or rel.startswith(e.rstrip("/") + "/") for e in TUPEL)


def schreibend(modus):
    return any(z in modus for z in ("w", "a", "x", "+"))


gesamt = collections.Counter()
code = collections.OrderedDict()
sonstige = collections.OrderedDict()
ausgenommen = collections.Counter()
for lauf in laeufe:
    for datei in sorted(glob.glob(os.path.join(lauf, "prot", "*.tsv"))):
        if datei.endswith(".module.tsv"):
            continue
        for z in open(datei, encoding="utf-8", errors="replace"):
            teile = z.rstrip("\n").split("\t")
            if len(teile) < 4 or teile[0] != "open" or schreibend(teile[1]):
                continue
            p = echt(teile[2])
            if p.endswith(".pyc"):
                p = quelle_aus_bytecode(p)
            gesamt["lesend"] += 1
            # Erst das Repo, dann das Scratchpad: der frische Klon LIEGT im Scratchpad.
            if not (p.startswith(repo + os.sep)):
                ausgenommen["Scratchpad (Protokolle, Ziele)" if p.startswith(scratch + os.sep)
                            else "ausserhalb des Repos"] += 1
                continue
            rel = p[len(repo) + 1:]
            if p.startswith(SNAP + os.sep):
                ausgenommen["Snapshot (Daten)"] += 1
            elif p.startswith(ENV + os.sep):
                ausgenommen["trading-env (Umgebung)"] += 1
            elif rel in PROTOKOLLE:
                ausgenommen["registriertes Protokoll (F8)"] += 1
            elif rel.startswith("docs/belege/"):
                ausgenommen["Messumschlag docs/belege/"] += 1
            elif gedeckt(rel):
                ausgenommen["gedeckt von ARBEITSBAUM_PFADE"] += 1
            elif rel.endswith(".py"):
                code.setdefault(rel, [0, set()])[0] += 1
                code[rel][1].add(os.path.basename(lauf))
            else:
                sonstige.setdefault(rel, [0, set()])[0] += 1
                sonstige[rel][1].add(os.path.basename(lauf))

print("# TB-112 A6 Lese-Audit 'Code ungebunden nach E2' - Laeufe: %s"
      % ", ".join(os.path.basename(l) for l in laeufe))
print("# ARBEITSBAUM_PFADE: %d Eintraege; REGISTRIERTE_PROTOKOLLE: %s" % (len(TUPEL), list(PROTOKOLLE)))
print("lesende Zugriffe gesamt: %d" % gesamt["lesend"])
for k, v in sorted(ausgenommen.items()):
    print("   nicht gezaehlt  %-34s %6d" % (k, v))
print("\nCODE unter der Codewurzel ausserhalb von ARBEITSBAUM_PFADE: %d verschiedene Dateien, %d Zugriffe"
      % (len(code), sum(v[0] for v in code.values())))
for rel, (n, l) in code.items():
    print("   BEFUND %4dx  %s   (Laeufe: %s)" % (n, rel, ", ".join(sorted(l))))
print("\nSONSTIGE Dateien unter dem Repo ausserhalb von ARBEITSBAUM_PFADE (Eingaben, nicht Code - nur ausgewiesen): "
      "%d verschiedene, %d Zugriffe" % (len(sonstige), sum(v[0] for v in sonstige.values())))
for rel, (n, l) in sonstige.items():
    print("          %4dx  %s   (Laeufe: %s)" % (n, rel, ", ".join(sorted(l))))
print("\nERGEBNIS CODE %d" % len(code))
