#!/usr/bin/env python3
"""
Die vier Ausschlussmengen sind gleich (TB-117, Fable 27a R13 (a), Register 46.4)
==============================================================================
`XAUTUSDT_1h.csv` im Datenstand `d9449faf...` endet auf einer Teilkerze; kein
Lauf liest sie, weil vier Mengen das Symbol streichen. "Solange" jede der vier
es tut - dafuer ist diese Probe die Wache (Handwerk, keine Sperrlistennaehe):

  shared/symbols_config.py                    EXCLUDE_SYMBOLS      (Modulkonstante)
  research/vorregistrierung/messgroessen.py   AUSGESCHLOSSEN       (Modulkonstante)
  research/faltenplan_neun/faltenplan_neun.py KRYPTO_AUSSCHLUSS    (Modulkonstante)
  research/vorregistrierung/benchmark.py      symbole()            (Mengenliteral im
                                                                     Rumpf, `x not in {...}`)

Gelesen wird mit `ast`, NICHT importiert - die Dateien werden nur gelesen, keine
wird geaendert, keine ausgefuehrt (zwei davon stehen auf der Sperrliste). Jede
Menge muss genau einmal gefunden werden; alle vier muessen gleich sein und
`XAUTUSDT` enthalten. Die Zusammenlegung auf einen Ort ist NICHT Teil dieser
Probe (R13 (a): mit der jeweils naechsten planmaessigen Oeffnung).

Mutationsprobe mit Gegenprobe: in einer Kopie der vier Dateien bekommt eine
Menge ein Symbol mehr bzw. verliert `XAUTUSDT` -> die Probe wird rot; ohne die
Mutation (Gegenprobe) ist sie gruen.

Aufruf: trading-env/bin/python3 shared/test_ausschlussmengen.py
"""

import ast
import os
import shutil
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_HIER)

QUELLEN = (
    ("shared/symbols_config.py", "EXCLUDE_SYMBOLS", None),
    ("research/vorregistrierung/messgroessen.py", "AUSGESCHLOSSEN", None),
    ("research/faltenplan_neun/faltenplan_neun.py", "KRYPTO_AUSSCHLUSS", None),
    ("research/vorregistrierung/benchmark.py", None, "symbole"),
)

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print("  [ OK ] %s" % name)
    else:
        gescheitert.append("%s%s" % (name, (" - " + str(zusatz)[:300]) if zusatz else ""))
        print("  [FEHL] %s%s" % (name, (" - " + str(zusatz)[:300]) if zusatz else ""))


def _menge(pfad, konstante, funktion):
    """Die Menge aus einer Datei; Liste der Funde (genau einer erwartet)."""
    with open(pfad, encoding="utf-8") as f:
        baum = ast.parse(f.read())
    funde = []
    if konstante:
        for k in baum.body:
            if (isinstance(k, ast.Assign) and len(k.targets) == 1
                    and getattr(k.targets[0], "id", None) == konstante):
                funde.append(ast.literal_eval(k.value))
    else:
        for k in baum.body:
            if isinstance(k, ast.FunctionDef) and k.name == funktion:
                for n in ast.walk(k):
                    if (isinstance(n, ast.Compare) and len(n.ops) == 1
                            and isinstance(n.ops[0], ast.NotIn)
                            and isinstance(n.comparators[0], ast.Set)):
                        funde.append(ast.literal_eval(n.comparators[0]))
    return funde


def lies_mengen(wurzel):
    """{quelle: menge oder None}; None, wenn nicht genau ein Fund."""
    ergebnis = {}
    for rel, konstante, funktion in QUELLEN:
        funde = _menge(os.path.join(wurzel, rel), konstante, funktion)
        name = "%s::%s" % (rel, konstante or funktion + "()")
        ergebnis[name] = set(funde[0]) if len(funde) == 1 and isinstance(funde[0], set) else None
    return ergebnis


def gleich(mengen):
    werte = list(mengen.values())
    return (all(m is not None for m in werte) and all(m == werte[0] for m in werte)
            and "XAUTUSDT" in werte[0])


def _kopie(mutation=None):
    """Die vier Dateien in einen Wegwerf-Ordner; `mutation` = (rel, alt, neu)."""
    t = tempfile.mkdtemp(prefix="tb117_ausschluss_")
    for rel, _, _ in QUELLEN:
        ziel = os.path.join(t, rel)
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        shutil.copy2(os.path.join(BASE_DIR, rel), ziel)
    if mutation:
        rel, alt, neu = mutation
        p = os.path.join(t, rel)
        with open(p, encoding="utf-8") as f:
            text = f.read()
        if text.count(alt) != 1:
            raise AssertionError("Mutationsstelle nicht genau einmal in %s: %r" % (rel, alt))
        with open(p, "w", encoding="utf-8") as f:
            f.write(text.replace(alt, neu, 1))
    return t


def main():
    print(__doc__.strip().split("\n")[0])
    m = lies_mengen(BASE_DIR)
    for name, menge in m.items():
        print("    %-70s %s" % (name, sorted(menge) if menge is not None else "NICHT GENAU EINMAL"))
    pruefe("A1: jede der vier Mengen genau einmal gefunden",
           all(v is not None for v in m.values()), m)
    pruefe("A2: die vier Mengen sind gleich und enthalten XAUTUSDT", gleich(m), m)

    mutationen = (
        ("M1", "eine Menge ein Symbol mehr (messgroessen.py)",
         ("research/vorregistrierung/messgroessen.py",
          'AUSGESCHLOSSEN = {"XAUTUSDT", "PAXGUSDT"}',
          'AUSGESCHLOSSEN = {"XAUTUSDT", "PAXGUSDT", "BTCUSDT"}')),
        ("M2", "XAUTUSDT fehlt im Literal von benchmark.symbole()",
         ("research/vorregistrierung/benchmark.py",
          'not in {"XAUTUSDT", "PAXGUSDT"}]', 'not in {"PAXGUSDT"}]')),
        ("M3", "die Konstante in symbols_config.py umbenannt (nicht gefunden)",
         ("shared/symbols_config.py", "EXCLUDE_SYMBOLS = {", "EXCLUDE_SYMBOLE = {")),
    )
    for name, text, mut in mutationen:
        for mutieren in (True, False):
            t = _kopie(mut if mutieren else None)
            try:
                g = gleich(lies_mengen(t))
            finally:
                shutil.rmtree(t, ignore_errors=True)
            if mutieren:
                pruefe("%s: Mutationsprobe '%s' -> Probe rot" % (name, text), not g)
            else:
                pruefe("%s-G: Gegenprobe - dieselbe Kopie ohne Mutation -> gruen" % name, g)

    pruefe("A3: die echten Dateien sind unveraendert gelesen (erneut gleich)",
           lies_mengen(BASE_DIR) == m)
    print("\n" + "=" * 78)
    if gescheitert:
        print("%d bestanden, %d GESCHEITERT:" % (bestanden, len(gescheitert)))
        for g in gescheitert:
            print("  - %s" % g)
        return 1
    print("%d/%d Pruefungen bestanden." % (bestanden, bestanden))
    return 0


if __name__ == "__main__":
    sys.exit(main())
