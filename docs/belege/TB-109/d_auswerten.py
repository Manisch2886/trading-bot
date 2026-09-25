"""TB-109 E2 - Fassung von docs/belege/TB-104/d_auswerten.py mit Klasse (iv) (Fable 25e 3 (b)).
Die alte Fassung bleibt unveraendert liegen. Einziger Unterschied: Zugriffe eines Laufs auf seine
EIGENE Zwischenablage stehen unter (iv), nicht unter (i) ausserhalb.

  (iv)  Zwischenablagen - ein Verzeichnis im temporaeren Verzeichnis des Systems
                     (tempfile.gettempdir(), Symlinks aufgeloest), das ein Prozess DIESES Laufs
                     selbst angelegt hat (mkdir im Protokoll). Jeder lesende Zugriff auf das
                     Verzeichnis selbst oder darunter (Ergebnis lesen, Aufraeumen per rmtree =
                     Verzeichnis-Oeffnung) gehoert zu (iv). Schreibende Zugriffe und die Anlage
                     bleiben zusaetzlich unter (iii) stehen (dort unveraendert gegen TB-104).
                     Je Ablage: ob sie bei der Auswertung noch existiert (entfernt ja/nein).

Rest wie TB-104:

TB-104 C5/D1 - wertet die Protokolle des Hakens (docs/belege/TB-104/haken/) eines oder
mehrerer Laeufe aus. Bauart TB-103 d_lesequellen.py, geordnet nach den drei Klassen aus
Fable 25a 3 (A):

  (i)   Eingaben   - gelesene Dateien, die weder Code noch Umgebung sind; getrennt nach
                     Snapshot / ausserhalb. Jede Datei ausserhalb mit Aufrufstapel.
  (ii)  Umgebung   - Interpreter-, Paket-, Plattform-, Zufalls-, Zeitzonendateien,
                     requirements.lock; als Liste der Dateien AUSSERHALB der Python-
                     Installation (Pakete/Standardbibliothek nur gezaehlt) mit Stapel.
  (iii) Schreibziele - jede zum Schreiben geoeffnete Datei und jede Verzeichnisanlage
                     ausserhalb des Scratchpads, mit Stapel - auch ohne geschriebene Bytes.

Dazu: Quelltext, der als DATEN gelesen wird (eine .py-Datei, die im Prozess nicht als
Modul geladen ist), und die Liste der geladenen REPO-Module (Modulliste des Hakens,
Bytecode auf die Quelle zurueckgefuehrt) je Prozess und vereinigt.

Aufruf:  python3 d_auswerten.py <repo> <scratch> <lauf-ordner> [<lauf-ordner> ...]
Sichtschutz 27.1: nur Pfade, Modi, Stapel - keine Kennzahl, keine Trade-Zahl.
"""
import collections
import glob
import os
import sys
import tempfile

repo = os.path.realpath(sys.argv[1])
scratch = os.path.realpath(sys.argv[2])
laeufe = sys.argv[3:]
SNAP = os.path.join(repo, "snapshots",
                    "63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2")
ENV = os.path.join(repo, "trading-env")
TEMP = os.path.realpath(tempfile.gettempdir())


def echt(p):
    try:
        return os.path.realpath(p)
    except OSError:
        return p


def ist_python_installation(p):
    return (p.startswith(ENV + os.sep) or "/lib/python" in p or "site-packages" in p
            or "/Library/Caches/com.apple.python" in p or "/__pycache__/" in p
            or "/Library/Developer/CommandLineTools/" in p
            or "/Applications/Xcode" in p)


def umgebung(p):
    return (ist_python_installation(p) or p.startswith(("/dev/", "/etc/", "/private/etc/",
            "/usr/", "/System/", "/private/var/db/", "/var/db/", "/Library/"))
            or p == os.path.join(repo, "requirements.lock"))


def schreibend(modus):
    return any(z in modus for z in ("w", "a", "x", "+"))


def rel(p):
    for wurzel, name in ((SNAP, "<snapshot>"), (scratch, "<scratch>"), (repo, "<repo>")):
        if p == wurzel or p.startswith(wurzel + os.sep):
            return name + p[len(wurzel):]
    return p


def stapel_kurz(s):
    return " < ".join(rel(t) for t in s.split(" < ") if t)[:400]


for lauf in laeufe:
    prot = os.path.join(lauf, "prot")
    prozesse = sorted(glob.glob(os.path.join(prot, "*.tsv")))
    prozesse = [p for p in prozesse if not p.endswith(".module.tsv")]
    print("=" * 100)
    print("LAUF %s  (Prozesse: %d, rc %s)" % (rel(echt(lauf)), len(prozesse),
          open(os.path.join(lauf, "rc")).read().strip() if os.path.exists(os.path.join(lauf, "rc")) else "?"))
    eingaben = collections.OrderedDict()      # pfad -> (anzahl, stapel)
    env_datei = collections.OrderedDict()
    env_zahl = collections.Counter()
    schreib = collections.OrderedDict()
    code_als_daten = collections.OrderedDict()
    module_je_prozess = {}
    argv = {}
    # (iv): die Verzeichnisse, die ein Prozess dieses Laufs im Temp-Verzeichnis selbst anlegt
    ablagen = set()
    for datei in prozesse:
        for z in open(datei, encoding="utf-8", errors="replace"):
            teile = z.rstrip("\n").split("\t")
            if len(teile) >= 4 and teile[0] == "mkdir":
                p = echt(teile[2])
                if p.startswith(TEMP + os.sep):
                    ablagen.add(p)
    ablage_zugriffe = collections.OrderedDict()   # pfad -> [anzahl, stapel, ablage]

    def eigene_ablage(p):
        for a in ablagen:
            if p == a or p.startswith(a + os.sep):
                return a
        return None

    for datei in prozesse:
        pid = os.path.basename(datei)[:-4]
        modul_datei = os.path.join(prot, pid + ".module.tsv")
        geladen = set()
        if os.path.exists(modul_datei):
            for z in open(modul_datei, encoding="utf-8"):
                name, quelle = z.rstrip("\n").split("\t")
                if quelle != "-":
                    geladen.add(echt(quelle))
            module_je_prozess[pid] = geladen
        else:
            module_je_prozess[pid] = None
        for z in open(datei, encoding="utf-8", errors="replace"):
            z = z.rstrip("\n")
            if z.startswith("#argv"):
                argv[pid] = z.split("\t", 1)[1]
                continue
            teile = z.split("\t")
            if len(teile) < 4:
                continue
            art, modus, pfad, stapel = teile[0], teile[1], teile[2], teile[3]
            p = echt(pfad)
            if p.startswith(scratch + os.sep) or p == scratch:
                continue                      # eigene Protokolle/Ausgaben
            if art == "mkdir":
                schreib.setdefault(("mkdir", p), [0, stapel])[0] += 1
                continue
            if schreibend(modus):
                schreib.setdefault((modus, p), [0, stapel])[0] += 1
                continue
            a = eigene_ablage(p)
            if a is not None:
                ablage_zugriffe.setdefault(p, [0, stapel, a])[0] += 1
                continue
            if umgebung(p):
                if ist_python_installation(p):
                    env_zahl["Python-Installation/Pakete/Bytecode"] += 1
                else:
                    env_datei.setdefault(p, [0, stapel])[0] += 1
                continue
            if p.endswith(".py"):
                if module_je_prozess[pid] is not None and p not in module_je_prozess[pid]:
                    code_als_daten.setdefault(p, [0, stapel, pid])[0] += 1
                continue
            if p.endswith((".pyc", ".so", ".pth")):
                continue
            eingaben.setdefault(p, [0, stapel])[0] += 1
    im_snap = {p: v for p, v in eingaben.items() if p.startswith(SNAP + os.sep)}
    ausserhalb = {p: v for p, v in eingaben.items() if not p.startswith(SNAP + os.sep)}
    print("\n(i) EINGABEN: %d verschiedene Dateien, davon %d im Snapshot (%d CSV, %d config/, "
          "%d sonst), %d AUSSERHALB" % (
              len(eingaben), len(im_snap),
              sum(p.endswith(".csv") for p in im_snap),
              sum("/config/" in p[len(SNAP):] for p in im_snap),
              sum(not p.endswith(".csv") and "/config/" not in p[len(SNAP):] for p in im_snap),
              len(ausserhalb)))
    for p, (n, s) in ausserhalb.items():
        print("   %4dx  %s\n          <- %s" % (n, rel(p), stapel_kurz(s)))
    print("\n    Quelltext als DATEN gelesen (.py, im Prozess nicht als Modul geladen): %d" % len(code_als_daten))
    for p, (n, s, pid) in code_als_daten.items():
        print("   %4dx  %s\n          <- %s" % (n, rel(p), stapel_kurz(s)))
    print("\n(ii) UMGEBUNG: %d Zugriffe in der Python-Installation (nur gezaehlt); "
          "%d weitere verschiedene Dateien:" % (sum(env_zahl.values()), len(env_datei)))
    for p, (n, s) in env_datei.items():
        print("   %4dx  %s\n          <- %s" % (n, rel(p), stapel_kurz(s)))
    print("\n(iii) SCHREIBZIELE ausserhalb des Scratchpads: %d" % len(schreib))
    for (modus, p), (n, s) in schreib.items():
        print("   %4dx  %-6s %s\n          <- %s" % (n, modus, rel(p), stapel_kurz(s)))
    oeffnungen = sum(1 for p, (n, s, a) in ablage_zugriffe.items() if p == a)
    print("\n(iv) ZWISCHENABLAGEN: %d eigene Ablagen im Temp-Verzeichnis, %d verschiedene lesende Zugriffe "
          "darauf (%d Verzeichnis-Oeffnungen, %d Dateien darin)" % (
              len(ablagen), len(ablage_zugriffe), oeffnungen, len(ablage_zugriffe) - oeffnungen))
    for a in sorted(ablagen):
        print("   Ablage %s  - bei der Auswertung %s" % (
            rel(a), "noch vorhanden" if os.path.exists(a) else "entfernt"))
    for p, (n, s, a) in ablage_zugriffe.items():
        print("   %4dx  %s%s\n          <- %s" % (n, rel(p), "  (Verzeichnis)" if p == a else "",
                                                  stapel_kurz(s)))
    print("\nGELADENE REPO-MODULE (ohne trading-env), je Prozess:")
    alle = set()
    for pid, geladen in module_je_prozess.items():
        if geladen is None:
            print("   pid %s: KEINE Modulliste (Prozess ohne atexit beendet) - argv %s"
                  % (pid, argv.get(pid, "?")[:160]))
            continue
        eigene = sorted(p for p in geladen
                        if p.startswith(repo + os.sep) and not p.startswith(ENV + os.sep))
        alle |= set(eigene)
        print("   pid %s (%d Repo-Module) argv %s" % (pid, len(eigene), rel(argv.get(pid, "?"))[:160]))
    print("\n   VEREINIGUNG dieses Laufs: %d Repo-Module" % len(alle))
    for p in sorted(alle):
        print("      %s" % rel(p))
