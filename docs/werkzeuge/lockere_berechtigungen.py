#!/usr/bin/env python3
"""Lockert `.claude/settings.local.json`: erlaubt ist alles, gesperrt ist die
Sperrliste. Betreiberentscheidung 22.09.2026, 21:49.

Wirkt auf den JEWEILS AKTUELLEN Stand der Datei - Claude-Code-Sitzungen
ergaenzen die allow-Liste waehrend ihrer Laeufe selbst. Deshalb ein Skript
und keine vorbereitete Datei zum Kopieren.

Aufruf (aus der Repo-Wurzel):   python3 docs/werkzeuge/lockere_berechtigungen.py

Sichert vorher nach `.claude/settings.local.json.<zeitstempel>_vor_lockerung.bak`
und ueberschreibt nie eine bestehende Sicherung.
"""
import io
import json
import os
import sys
import time

ZIEL = os.path.join(".claude", "settings.local.json")

SAMMEL = ["Bash(*)", "Read(*)", "Edit(*)", "Write(*)",
          "Glob(*)", "Grep(*)", "WebFetch(*)", "TodoWrite(*)"]

# Die vier Sperrlisten-Programmdateien aus Registerabschnitt 10
# (Punkte 1, 2, 3/5, 4/6). "Alles ausser der Sperrliste" heisst woertlich,
# dass diese geschuetzt bleiben - eine Sitzung fragt hier weiter nach.
SPERRLISTE_PY = [
    "research/vorregistrierung/registerdaten.py",
    "research/vorregistrierung/faltenplan.py",
    "research/vorregistrierung/auswertung.py",
    "research/vorregistrierung/benchmark.py",
]

WEITERE_SPERREN = [
    # Historie umschreiben
    "Bash(git commit --amend:*)", "Bash(git rebase:*)",
    "Bash(git filter-branch:*)", "Bash(git push --mirror:*)",
    "Bash(git update-ref:*)",
    # Umgebung aendern
    "Bash(pip install:*)", "Bash(pip3 install:*)", "Bash(brew:*)",
    # Rohschreiben
    "Bash(dd:*)", "Bash(truncate:*)", "Bash(shred:*)",
    "Bash(mkfifo:*)", "Bash(chown:*)",
]


def main():
    if not os.path.isfile(ZIEL):
        print("FEHLER: %s nicht gefunden. Aus der Repo-Wurzel aufrufen." % ZIEL)
        return 1

    with io.open(ZIEL, encoding="utf-8") as f:
        d = json.load(f)

    sicherung = "%s.%s_vor_lockerung.bak" % (ZIEL, time.strftime("%Y-%m-%d_%H%M%S"))
    if os.path.exists(sicherung):
        print("FEHLER: Sicherung existiert bereits, Abbruch: %s" % sicherung)
        return 1
    with io.open(ZIEL, encoding="utf-8") as q, io.open(sicherung, "w", encoding="utf-8") as z:
        z.write(q.read())

    p = d.setdefault("permissions", {})
    allow = list(p.get("allow", []))
    deny = list(p.get("deny", []))
    vorher = (len(allow), len(deny))

    allow = [m for m in SAMMEL if m not in allow] + allow

    neu = []
    for pfad in SPERRLISTE_PY:
        neu.append("Write(%s)" % pfad)
        neu.append("Edit(%s)" % pfad)
    neu += WEITERE_SPERREN
    deny += [m for m in neu if m not in deny]

    d["permissions"] = {"allow": allow, "deny": deny}
    with io.open(ZIEL, "w", encoding="utf-8") as f:
        f.write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")

    print("Sicherung: %s" % sicherung)
    print("allow: %d -> %d" % (vorher[0], len(allow)))
    print("deny:  %d -> %d" % (vorher[1], len(deny)))
    print("Bash(*) erlaubt:          %s" % ("Bash(*)" in allow))
    print("faltenplan.py gesperrt:   %s"
          % ("Write(research/vorregistrierung/faltenplan.py)" in deny))
    print("FERTIG")
    return 0


if __name__ == "__main__":
    sys.exit(main())
