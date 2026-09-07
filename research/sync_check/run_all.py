"""
Fuehrt den vollstaendigen Sync-Check aus.

Nutzung:  python3 run_all.py
"""

import json
import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(_DIR, "results")


def run(args):
    print(f"\n$ python3 {' '.join(args)}")
    return subprocess.call([sys.executable] + args, cwd=_DIR)


def main():
    failures = []
    print("=" * 78, "\nSCHRITT 1 - Sync-Tabelle aller 9 Bots\n", "=" * 78, sep="")
    if run(["sync_table.py", "--json"]) != 0:
        sys.exit("Sync-Tabelle fehlgeschlagen.")

    with open(os.path.join(RESULTS, "sync_table.json")) as f:
        divergent = json.load(f)["abweichend"]

    print("\n" + "=" * 78, f"\nSCHRITT 2 - Baseline-Vergleich fuer {len(divergent)} abweichende Bots\n",
          "=" * 78, sep="")
    for bot in divergent:
        if run(["impact.py", bot]) != 0:
            failures.append(f"impact {bot}")

    print("\n" + "=" * 78, "\nSCHRITT 3 - Betroffenheit der fuenf Studien\n", "=" * 78, sep="")
    if run(["study_exposure.py", "--verify"]) != 0:
        failures.append("study_exposure")

    print("\n" + "=" * 78)
    if failures:
        print("FEHLGESCHLAGEN: " + ", ".join(failures))
        sys.exit(1)
    print("Sync-Check vollstaendig durchgelaufen.")


if __name__ == "__main__":
    main()
