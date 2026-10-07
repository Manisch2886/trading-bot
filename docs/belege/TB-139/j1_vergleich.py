#!/usr/bin/env python3
"""TB-139 D2 - Zeichengleichheit des Absatzes J1 im Journal.

Eigener Leser (nicht der aus j1_einsetzen.py): nimmt den ersten Codeblock ohne Zaeune nach der
Zeile `#### J1 — ` des Auftrags und prueft als Bytevergleich, dass der Text in JOURNAL.md genau
einmal vorkommt, an Zeilengrenzen steht, zwischen der Kopfzeile des neuen Blocks und dem
Ankertext liegt und mit je einer Leerzeile vor `### Was gemessen ist` steht.
Mit --soll-vorkommen 0 (wenn E1 nicht lief): der Text darf im Journal nicht stehen, auch keine
seiner Zeilen einzeln.
Ausgabe nach j1_vergleich.txt.

Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 -B docs/belege/TB-139/j1_vergleich.py --kennung EI
Rueckgabe: 0 wie das Soll, 1 Abweichung, 2 nicht messbar."""
import argparse
import re
import sys
import traceback
from pathlib import Path

AUFTRAG = Path("docs/auftraege/MAC_TB-139_register_fable_07a.md")
JOURNAL = Path("docs/projektfuehrung/JOURNAL.md")
AUSGABE = Path("docs/belege/TB-139/j1_vergleich.txt")
ANKER = b"\n---\n\n## Wiederkehrende Lehren\n"
ZIEL_ZEILE = b"### Was gemessen ist"


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--kennung", required=True)
    a.add_argument("--soll-vorkommen", type=int, choices=(0, 1), default=1)
    x = a.parse_args(argv)
    teile = re.split("\n(?=#### J1 — )".encode("utf-8"), AUFTRAG.read_bytes())
    cb = re.search(rb"\n```\n(.*?)\n```\n", teile[1], re.S) if len(teile) == 2 else None
    if cb is None:
        print("NICHT MESSBAR: `#### J1 — ` mit Codeblock steht nicht genau einmal im Auftrag")
        return 2
    text = cb.group(1)
    ziel = JOURNAL.read_bytes()
    kopf = ("\n## %s — TB-139" % x.kennung).encode("utf-8")
    gesamt = ziel.count(text)
    grenzen = ziel.count(b"\n" + text + b"\n")
    einzeln = sum(1 for z in text.split(b"\n") if b"\n" + z + b"\n" in ziel)
    im_block = (ziel.count(kopf) == 1 and ziel.count(ANKER) == 1
                and ziel.find(kopf) < ziel.find(text) < ziel.find(ANKER))
    am_ort = ziel.count(b"\n\n" + text + b"\n\n" + ZIEL_ZEILE + b"\n") == 1
    if x.soll_vorkommen == 1:
        gut = gesamt == 1 and grenzen == 1 and im_block and am_ort
        wort = "GLEICH" if gut else "ABWEICHUNG"
    else:
        gut = gesamt == 0 and einzeln == 0
        wort = "NICHT EINGESETZT, wie das Soll" if gut else "ABWEICHUNG"
    zeile = ("J1 · %s · %d Bytes · %d Zeile(n) · Soll Vorkommen %d · Vorkommen %d · an Zeilengrenzen %d · "
             "Zeilen von J1 einzeln im Journal %d · im neuen Block %s %s · vor `%s` %s · %s" % (
                 JOURNAL, len(text), text.count(b"\n") + 1, x.soll_vorkommen, gesamt, grenzen, einzeln,
                 x.kennung, "ja" if im_block else "nein", ZIEL_ZEILE.decode(), "ja" if am_ort else "nein", wort))
    AUSGABE.write_text("# TB-139 D2 — Zeichengleichheit J1 (j1_vergleich.py)\n" + zeile + "\n", encoding="utf-8")
    print(zeile)
    return 0 if gut else 1


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        RC = 2
    sys.exit(RC)
