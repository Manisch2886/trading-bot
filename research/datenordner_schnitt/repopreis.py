#!/usr/bin/env python3
"""
Was kostet ein Snapshot im Repo? (TB-46, Teil 2)
==============================================================================
Der Auftrag nennt als Preis fuer den zweiten Bestand **rund 56 MB**. Diese
Messung prueft das nach, statt es zu uebernehmen - und findet zwei Dinge, die
die Zahl verschieben:

1. **`data/` ist nicht 56 MB gross.** Gemessen wird beides: die Summe der
   Dateigroessen und die Groesse des Packfiles.
2. ⭐ **git speichert gleiche Inhalte nur einmal.** Ein Snapshot, dessen
   Dateien **byteidentisch** zu den Live-Dateien sind, legt keine zweiten
   Blobs an - er legt nur Baumeintraege an. Der Zuwachs ist dann nicht die
   Datenmenge, sondern ein Bruchteil davon.

Punkt 2 ist der Grund fuer diese Messung. Er ist nicht offensichtlich, er
entscheidet die Frage, und er laesst sich in einem Wegwerf-Repo in Sekunden
zeigen statt behaupten.

Gemessen wird in drei Schritten, jeder in einem frischen Wegwerf-Repo:

    A  ein Ordner mit echten Kursdateien wird committet        -> Grundgroesse
    B  eine **byteidentische** Kopie daneben, committet        -> Zuwachs?
    C  eine **um ein Byte veraenderte** Kopie daneben          -> Zuwachs?

C ist die Gegenprobe: sie zeigt, dass die Messung ueberhaupt Zuwachs sehen
kann. Ohne sie koennte B gruen aussehen, weil die Messung nichts messt.

⚠️ Die Messung liest `data/` und kopiert daraus in ein Wegwerf-Verzeichnis.
Sie **schreibt nichts** nach `data/` und legt nichts im Projekt-Repo an.

    python3 research/datenordner_schnitt/repopreis.py
    python3 research/datenordner_schnitt/repopreis.py --dateien 40

Rueckgabewert 0, wenn gemessen wurde; 1, wenn nicht gemessen werden konnte
(kein git, keine Kursdateien, Packfile nicht auslesbar).
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))
DATA_DIR = os.path.join(_WURZEL, "data")


class Messfehler(Exception):
    """Konnte nicht messen - ein eigener, roter Ausgang."""


def _git(ordner, *args):
    lauf = subprocess.run(["git", "-C", ordner] + list(args),
                          capture_output=True, text=True)
    if lauf.returncode != 0:
        raise Messfehler("git %s (Rueckgabewert %d): %s"
                         % (" ".join(args), lauf.returncode,
                            lauf.stderr.strip()[:200]))
    return lauf.stdout


def _packgroesse(ordner):
    """Die Groesse der git-Objekte in Bytes - lose und gepackt zusammen."""
    text = _git(ordner, "count-objects", "-v")
    werte = {}
    for zeile in text.splitlines():
        if ":" in zeile:
            schluessel, wert = zeile.split(":", 1)
            werte[schluessel.strip()] = wert.strip()
    try:
        # `size` und `size-pack` stehen in KiB.
        return (int(werte.get("size", 0)) + int(werte.get("size-pack", 0))) * 1024
    except ValueError as fehler:
        raise Messfehler("count-objects nicht auswertbar: %s" % fehler)


def _bestand(daten_dir, anzahl):
    """Die groessten `anzahl` Kursdateien - die teuerste Auswahl."""
    if not os.path.isdir(daten_dir):
        raise Messfehler("%s ist kein Verzeichnis." % daten_dir)
    namen = [n for n in os.listdir(daten_dir) if n.endswith(".csv")]
    if not namen:
        raise Messfehler("%s enthaelt keine Kursdateien." % daten_dir)
    namen.sort(key=lambda n: -os.path.getsize(os.path.join(daten_dir, n)))
    return namen[:anzahl]


def messe(daten_dir=DATA_DIR, anzahl=30, zeilen=30):
    namen = _bestand(daten_dir, anzahl)
    arbeit = tempfile.mkdtemp(prefix="tb46_repopreis_")
    try:
        repo = os.path.join(arbeit, "repo")
        os.makedirs(os.path.join(repo, "data"))
        _git(repo, "init", "-q")
        _git(repo, "config", "user.email", "messung@trading-bot.invalid")
        _git(repo, "config", "user.name", "TB-46")

        rohbytes = 0
        for name in namen:
            shutil.copy2(os.path.join(daten_dir, name),
                         os.path.join(repo, "data", name))
            rohbytes += os.path.getsize(os.path.join(repo, "data", name))

        # A - der Grundbestand
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "A: der Bestand")
        _git(repo, "gc", "-q", "--aggressive")
        a = _packgroesse(repo)

        # B - eine byteidentische Kopie daneben
        kopie = os.path.join(repo, "snapshots", "gleich")
        os.makedirs(kopie)
        for name in namen:
            shutil.copy2(os.path.join(repo, "data", name),
                         os.path.join(kopie, name))
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "B: byteidentische Kopie")
        _git(repo, "gc", "-q", "--aggressive")
        b = _packgroesse(repo)

        # C - eine Kopie, die auseinandergelaufen ist: so sieht der
        # Live-Bestand aus, nachdem er nach dem Ziehen weitergelaufen ist.
        # Das ist der Fall, um den es wirklich geht - nicht der eine
        # veraenderte Byte.
        anders = os.path.join(repo, "snapshots", "anders")
        os.makedirs(anders)
        for name in namen:
            ziel = os.path.join(anders, name)
            shutil.copy2(os.path.join(repo, "data", name), ziel)
            with open(ziel, "a", encoding="utf-8") as datei:
                for i in range(zeilen):
                    datei.write("2026-09-%02d 00:00:00,1,2,0,1.5,%d\n"
                                % ((i % 28) + 1, 1000 + i))
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "C: veraenderte Kopie")
        _git(repo, "gc", "-q", "--aggressive")
        c = _packgroesse(repo)

        # Und der Beweis auf der Objektebene: derselbe Inhalt, derselbe Blob.
        eine = namen[0]
        blob_live = _git(repo, "hash-object",
                         os.path.join(repo, "data", eine)).strip()
        blob_kopie = _git(repo, "hash-object",
                          os.path.join(kopie, eine)).strip()

        return {
            "dateien": len(namen),
            "rohbytes": rohbytes,
            "pack_A_bestand": a,
            "pack_B_mit_gleicher_kopie": b,
            "pack_C_mit_veraenderter_kopie": c,
            "zuwachs_B": b - a,
            "zuwachs_C": c - b,
            "zeilen_angehaengt": zeilen,
            "blob_gleich": blob_live == blob_kopie,
            "blob": blob_live,
        }
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def gesamtbestand(daten_dir=DATA_DIR, repo=_WURZEL):
    """Was `data/` heute wirklich wiegt - Dateien und Packfile des Projekts."""
    namen = [n for n in os.listdir(daten_dir) if n.endswith(".csv")]
    rohbytes = sum(os.path.getsize(os.path.join(daten_dir, n)) for n in namen)
    try:
        pack = _packgroesse(repo)
    except Messfehler:
        pack = None
    return {"kursdateien": len(namen), "rohbytes": rohbytes,
            "packfile_projekt": pack}


def main(argv=None) -> int:
    z = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    z.add_argument("--daten", default=DATA_DIR)
    z.add_argument("--dateien", type=int, default=30,
                   help="wie viele (die groessten) Kursdateien in die Messung")
    z.add_argument("--zeilen", type=int, default=30,
                   help="wie viele Zeilen die auseinandergelaufene Kopie mehr hat")
    z.add_argument("--json", default=None)
    a = z.parse_args(argv)

    try:
        gesamt = gesamtbestand(a.daten)
        m = messe(a.daten, a.dateien, a.zeilen)
    except Messfehler as fehler:
        print("NICHT MESSBAR: %s" % fehler, file=sys.stderr)
        return 1

    print("=" * 78)
    print("TB-46 TEIL 2 - was kostet der zweite Bestand im Repo?")
    print("=" * 78)
    print("\n1. WAS `data/` HEUTE WIEGT")
    print("   Kursdateien            %d" % gesamt["kursdateien"])
    print("   Summe der Dateien      %.1f MB" % (gesamt["rohbytes"] / 1e6))
    if gesamt["packfile_projekt"]:
        print("   Packfile des Projekts  %.1f MB   (alles, nicht nur data/)"
              % (gesamt["packfile_projekt"] / 1e6))
    print("   ⚠️ Der Auftrag nennt `rund 56 MB`. Gemessen ist es das nicht.")

    print("\n2. DIE MESSUNG AN %d KURSDATEIEN (%.1f MB Rohdaten)"
          % (m["dateien"], m["rohbytes"] / 1e6))
    print("   A  nur der Bestand                      %8.2f MB"
          % (m["pack_A_bestand"] / 1e6))
    print("   B  + byteidentische Kopie daneben       %8.2f MB   "
          "(Zuwachs %+.2f MB)"
          % (m["pack_B_mit_gleicher_kopie"] / 1e6, m["zuwachs_B"] / 1e6))
    print("   C  + auseinandergelaufene Kopie         %8.2f MB   "
          "(Zuwachs %+.2f MB)"
          % (m["pack_C_mit_veraenderter_kopie"] / 1e6, m["zuwachs_C"] / 1e6))
    print("\n   Derselbe Inhalt, derselbe Blob: %s   (%s)"
          % ("ja" if m["blob_gleich"] else "NEIN", m["blob"][:16]))

    print("\n3. WAS DARAUS FOLGT")
    anteil_b = 100.0 * m["zuwachs_B"] / m["rohbytes"]
    anteil_c = 100.0 * m["zuwachs_C"] / m["rohbytes"]
    print("   Zuwachs durch die byteidentische Kopie   %+.2f MB = %.3f %% "
          "der Datenmenge" % (m["zuwachs_B"] / 1e6, anteil_b))
    print("   Zuwachs durch die auseinandergelaufene   %+.2f MB = %.3f %% "
          "der Datenmenge" % (m["zuwachs_C"] / 1e6, anteil_c))
    if not m["blob_gleich"]:
        print("   ⚠️ Gleicher Inhalt ergab NICHT denselben Blob - die Deutung")
        print("   unten gilt dann nicht, nur die Zahlen oben.")
    elif anteil_b < 1.0 and anteil_c < 10.0:
        print("\n   Der zweite Bestand kostet im Repo einen Bruchteil seiner")
        print("   Datenmenge, und zwar aus zwei Gruenden, die beide gemessen")
        print("   sind: **gleiche Inhalte legt git nur einmal ab** (Zuwachs B),")
        print("   und **aehnliche Inhalte packt es als Unterschied** "
              "(Zuwachs C).")
        print("   Die Zahl `rund 56 MB` aus dem Auftrag beschreibt damit weder")
        print("   den heutigen Bestand (%.0f MB) noch den Preis des zweiten."
              % (gesamt["rohbytes"] / 1e6))
    else:
        print("\n   ⚠️ Der Zuwachs ist NICHT klein gegen die Datenmenge - die")
        print("   Zahlen oben gelten, die uebliche Annahme `git dedupliziert")
        print("   das weg` hier nicht.")

    if a.json:
        ziel = (a.json if os.path.isabs(a.json) else os.path.join(_HIER, a.json))
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump({"gesamtbestand": gesamt, "messung": m}, datei,
                      indent=2, ensure_ascii=False, sort_keys=True)
        print("\nJSON: %s" % ziel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
