#!/usr/bin/env python3
"""TB-140 D2 - setzt den Absatz J1 aus dem Auftrag in den Journalblock der Sitzung.

Liest J1 aus dem ersten Codezaun nach der Zeile `#### J1 — ` des Auftrags (nicht aus dem
Gedaechtnis) und setzt ihn im neuen Block vor die Zeile `### Was gemessen ist`, mit genau einer
Leerzeile davor und danach. Geschrieben wird nur docs/projektfuehrung/JOURNAL.md und die
Ausgabedatei. Trifft eine Bedingung nicht zu (assert), wird nichts geschrieben.

Aufruf aus der Repo-Wurzel, nachdem der Block der Sitzung im Journal steht:
  trading-env/bin/python3 -B docs/belege/TB-140/j1_einsetzen.py --kennung EH --probe   (nur lesen)
  trading-env/bin/python3 -B docs/belege/TB-140/j1_einsetzen.py --kennung EH
Rueckgabe: 0 eingesetzt (mit --probe: einsetzbar), 2 nicht eingesetzt."""
import argparse
import sys
import traceback
from pathlib import Path

AUFTRAG = Path("docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md")
JOURNAL = Path("docs/projektfuehrung/JOURNAL.md")
AUSGABE = Path("docs/belege/TB-140/j1_einsetzen.txt")
ANKER = "\n---\n\n## Wiederkehrende Lehren\n"
ZIEL_ZEILE = "### Was gemessen ist"
ERSTE_ZEILE = "**Nachtrag des steuernden Chats zum Stand vor TB-140"


def j1_lesen(text):
    zeilen = text.split("\n")
    kopf = [i for i, z in enumerate(zeilen) if z.startswith("#### J1 — ")]
    assert len(kopf) == 1, "Zeile `#### J1 — ` steht nicht genau einmal im Auftrag: %d" % len(kopf)
    j = kopf[0] + 1
    while zeilen[j] != "```":
        assert not zeilen[j].startswith("#"), "zwischen `#### J1 — ` und dem Codezaun steht eine Ueberschrift"
        j += 1
    k = j + 1
    while zeilen[k] != "```":
        k += 1
    block = zeilen[j + 1:k]
    assert block and block[0].startswith(ERSTE_ZEILE), "die erste Zeile von J1 lautet anders als erwartet"
    assert all(z != "" for z in block), "J1 traegt eine Leerzeile"
    return block


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--kennung", required=True, help="Kennung des neuen Journalblocks, zum Beispiel EH")
    a.add_argument("--probe", action="store_true", help="nur lesen, nichts schreiben")
    x = a.parse_args(argv)
    j1 = j1_lesen(AUFTRAG.read_text(encoding="utf-8"))
    inhalt = JOURNAL.read_text(encoding="utf-8")
    assert inhalt.count(ANKER) == 1, "Ankertext steht nicht genau einmal im Journal: %d" % inhalt.count(ANKER)
    assert inhalt.count(j1[0]) == 0, "die erste Zeile von J1 steht schon im Journal"
    kopfzeile = "\n## %s — TB-140" % x.kennung
    assert inhalt.count(kopfzeile) == 1, "Kopfzeile `## %s — TB-140` steht nicht genau einmal: %d" % (
        x.kennung, inhalt.count(kopfzeile))
    anfang, ende = inhalt.index(kopfzeile) + 1, inhalt.index(ANKER)
    assert anfang < ende, "der neue Block steht nicht vor dem Ankertext"
    block = inhalt[anfang:ende].split("\n")
    assert not [z for z in block[1:] if z.startswith("## ")], "zwischen Kopfzeile und Ankertext steht ein weiterer Block"
    quelle = [i for i, z in enumerate(block) if z.startswith("**Quelle:**")]
    ziel = [i for i, z in enumerate(block) if z == ZIEL_ZEILE]
    assert len(quelle) == 1, "Absatz `**Quelle:**` steht nicht genau einmal im neuen Block: %d" % len(quelle)
    assert len(ziel) == 1, "Zeile `%s` steht nicht genau einmal im neuen Block: %d" % (ZIEL_ZEILE, len(ziel))
    assert quelle[0] < ziel[0], "`**Quelle:**` steht nicht vor `%s`" % ZIEL_ZEILE
    g = ziel[0]
    vor = [] if block[g - 1] == "" else [""]
    neu = inhalt[:anfang] + "\n".join(block[:g] + vor + j1 + [""] + block[g:]) + inhalt[ende:]
    text = "\n".join(j1)
    assert neu.count(text) == 1 and neu.count("\n\n" + text + "\n\n" + ZIEL_ZEILE + "\n") == 1, "J1 stuende nicht genau einmal am Ort"
    zeile = "J1 · %s · Block %s · Ankertext 1 · `**Quelle:**` 1 · `%s` 1 · Textzeilen %d · %s" % (
        JOURNAL, x.kennung, ZIEL_ZEILE, len(j1), "einsetzbar (Probe, nichts geschrieben)" if x.probe else "eingesetzt")
    print(zeile)
    if not x.probe:
        JOURNAL.write_text(neu, encoding="utf-8")
        AUSGABE.write_text("# TB-140 D2 — Absatz J1 (erzeugt von j1_einsetzen.py)\n" + zeile + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        RC = main()
    except AssertionError as e:
        print("NICHT EINGESETZT: %s" % e)
        RC = 2
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT EINGESETZT: ungefangene Ausnahme (Traceback oben)")
        RC = 2
    sys.exit(RC)
