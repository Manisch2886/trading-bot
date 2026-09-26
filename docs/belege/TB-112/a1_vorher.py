#!/usr/bin/env python3
"""TB-112 A1 - Vorher-Probe: haelt die Startpruefung heute (Eingangs-Commit) an,
wenn eine Datei des Laufbereichs AUSSERHALB shared/strategies uncommittet
veraendert ist?

Aufruf (aus der Repo-Wurzel, mit trading-env):
    trading-env/bin/python3 docs/belege/TB-112/a1_vorher.py <scratch-ordner>

Ablauf: frischer Klon (git clone) nach <scratch>/a1_klon, darin ein
Einstiegspunkt `tb112_probe_einstieg.py` in der Klonwurzel (unversioniert,
liegt in keinem geprueften Pfad), der nur `import paths` macht. Je Probe:
eine Kommentarzeile an die Datei anhaengen, Prozess unter dem Modus starten
(TB_SELEKTIONSWURZEL = <klon>/snapshots/<hash>, HASH, COMMIT = HEAD des
Klons), rc und die STARTPRUEFUNG-Zeile festhalten, Datei mit
`git checkout --` zurueck. Dazu eine Kontrollprobe unter shared/ (muss rc 2
geben, sonst beisst der Aufbau nicht) und eine Leerprobe ohne Aenderung
(muss rc 0 geben). Der Klon wird am Ende entfernt.
"""
import os
import shutil
import subprocess
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
PY = os.path.join(WURZEL, "trading-env", "bin", "python3")
SNAP = "63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
EINSTIEG = "tb112_probe_einstieg.py"
PROBEN = [
    ("leer (keine Aenderung)", None),
    ("Kontrolle shared/", "shared/zuteilung.py"),
    ("E2 1", "research/vorregistrierung/benchmark.py"),
    ("E2 2", "research/faltenplan_neun/faltenplan_neun.py"),
    ("E2 3", "notifications/manual_close.py"),
]


def git(klon, *a):
    return subprocess.run(["git", "-C", klon] + list(a), capture_output=True,
                          text=True, check=True).stdout.strip()


def main():
    sp = sys.argv[1]
    klon = os.path.join(sp, "a1_klon")
    if os.path.exists(klon):
        sys.exit("ABBRUCH: %s existiert" % klon)
    subprocess.run(["git", "clone", "-q", WURZEL, klon], check=True)
    try:
        head = git(klon, "rev-parse", "HEAD")
        with open(os.path.join(klon, EINSTIEG), "w") as d:
            d.write("import os, sys\nsys.path.insert(0, os.path.join("
                    "os.path.dirname(os.path.abspath(__file__)), 'shared'))\n"
                    "import paths\nprint('durchgelaufen')\n")
        umg = dict(os.environ)
        umg.update(TB_SELEKTIONSWURZEL=os.path.join(klon, "snapshots", SNAP),
                   TB_SELEKTIONSHASH=SNAP, TB_SELEKTIONSCOMMIT=head)
        print("# TB-112 A1 Vorher-Probe, Klon am Commit %s (Eingangs-Commit)" % head)
        print("# Einstieg <klon>/%s (unversioniert), Modus: Snapshot %s..." % (EINSTIEG, SNAP[:8]))
        print("# git status --porcelain im Klon vor den Proben: [%s]"
              % git(klon, "status", "--porcelain"))
        for name, pfad in PROBEN:
            if pfad:
                with open(os.path.join(klon, pfad), "a") as d:
                    d.write("\n# TB-112 A1: uncommittete Probeaenderung\n")
            lauf = subprocess.run([PY, "-W", "ignore", EINSTIEG], cwd=klon,
                                  env=umg, capture_output=True, text=True)
            zeile = [z for z in lauf.stderr.splitlines()
                     if "STARTPRUEFUNG VERLETZT" in z]
            print("%-24s %-48s rc %d  %s" % (
                name, pfad or "-", lauf.returncode,
                (zeile[0][:200] if zeile else
                 ("stdout: " + lauf.stdout.strip()))))
            if pfad:
                git(klon, "checkout", "--", pfad)
        print("# git status --porcelain im Klon nach den Proben: [%s]"
              % git(klon, "status", "--porcelain"))
    finally:
        shutil.rmtree(klon)
    print("# Klon entfernt: %s" % (not os.path.exists(klon)))


if __name__ == "__main__":
    main()
