#!/usr/bin/env python3
"""TB-120 B - prueft jedes Kurzzitat „…“ in b_anforderungen.md und b_offen.md
gegen seine Quelle. Nur lesend.

Normalisierung der Quelle (und nur dieser): Zitatzeichen `>` am Zeilenanfang
weg, Zeilen mit Leerzeichen verbunden, Leerraum zusammengefasst, `**` entfernt
(die Hervorhebungen des Registers sind im Zitat weggelassen, B-Kopf). Das Zitat
selbst wird nur im Leerraum zusammengefasst. Ausserdem gezaehlt: Woerter je
Zitat (Grenze 15 fuer die Fundstellen-Spalte von b_anforderungen.md).

Aufruf von der Repo-Wurzel: python3 docs/belege/TB-120/b_zitate_pruefen.py
"""
import re
import sys

QUELLEN = {
    "register": "docs/VORREGISTRIERUNG_neuselektion.md",
    "plan": "docs/projektfuehrung/PLAN_VOR_DEM_TAG.md",
    "auswertung": "research/vorregistrierung/auswertung.py",
    "beispieldaten": "research/vorregistrierung/beispieldaten.py",
    "anfrage27c": "docs/projektfuehrung/FABLE_ANFRAGE_2026-09-27c_tagesanfrage_tb116_tb117.md",
    "positionen_holen": "research/tb24_haltedauern/positionen_holen.py",
}


def normal(text):
    zeilen = [re.sub(r"^\s*(>\s*)+", "", z) for z in text.splitlines()]
    t = " ".join(zeilen).replace("**", "")
    return re.sub(r"\s+", " ", t)


def main():
    quellen = {k: normal(open(p, encoding="utf-8").read()) for k, p in QUELLEN.items()}
    fehler = 0
    for datei, grenze in (("docs/belege/TB-120/b_anforderungen.md", 15),
                          ("docs/belege/TB-120/b_offen.md", None)):
        text = open(datei, encoding="utf-8").read()
        zitate = re.findall(r"„([^“]+)“", text)
        print(f"## {datei}: {len(zitate)} Zitate")
        for z in zitate:
            zn = re.sub(r"\s+", " ", z).strip()
            wo = [k for k, q in quellen.items() if zn in q]
            n = len(zn.split())
            zu_lang = grenze is not None and n > grenze
            if not wo:
                fehler += 1
            print(f"{'OK ' if wo else 'FEHLT'} {'LANG' if zu_lang else '    '} {n:3d} W  "
                  f"{','.join(wo) or '-':12s} {zn[:110]}")
    print(f"\nnicht gefunden: {fehler}")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
