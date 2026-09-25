#!/usr/bin/env python3
"""
TB-107 Block F - Gegenprobe ueber alle `__main__`-Stellen des Laufbereichs
==============================================================================
Fable 25c 4 (3)(a): Jede Stelle im `__main__`-Block eines Moduls im
Laufbereich, die bei fehlenden Daten mit `exit()`/`sys.exit()` endet, traegt
die Abfrage `paths.selektionsmodus()`. Unter dem Modus ist fehlende Eingabe
ein Abbruch mit 2, kein stilles Ende mit 0 (TB-105 Block C, 14 Stellen).

⚠️ Die Liste der Module liest dieser Test AUS DER DATEI der Laufbereichsmessung
(`docs/belege/TB-107/f1_laufbereich_vereinigung.txt`, gemessen am Endstand von
TB-107 mit dem Werkzeug aus TB-104 D1), nicht aus einem Literal. Tatsache:
Diese Liste wird am Tag-Commit durch die Tag-Messung ersetzt (Fable 25b (5));
bis dahin gilt die Messung von TB-107. Eintraege unter `docs/` sind
Messumschlaege und zaehlen nicht zum Laufbereich (Kopf der Messdatei).

Gesucht wird per AST, nicht per Zeilennummer:
  * ein `if` im `__main__`-Block, in dessen Rumpf `exit()`, `quit()` oder
    `sys.exit()` steht, und
  * das bei fehlenden DATEN endet: die Bedingung prueft ein Ergebnis auf leer
    (`not x`, `x.empty`, `len(x) == 0`), das im `__main__`-Block aus einem
    Ladeaufruf stammt (`load*`/`lade*`), ODER der Rumpf nennt "Keine Daten".
Eine solche Stelle ist in Ordnung, wenn ihr Rumpf VOR dem ersten Ausstieg
`paths.selektionsmodus()` aufruft.

Ausgewiesen, aber nicht gezaehlt: Stellen, die bei fehlenden TRADES enden
(`trades.empty` nach einer Rechnung, kein Ladeaufruf) - das ist ein
Rechenergebnis, keine fehlende Eingabe.

  F2   am echten Stand: jede Datenstelle traegt die Abfrage.
  F3a  Mutation: eine Kopie einer der 14 Dateien OHNE Abfrage, der Liste
       hinzugefuegt => rot. Gegenprobe: dieselbe Kopie ohne Mutation => gruen.
  F3b  Mutation: eine erfundene fuenfzehnte Datei mit "Keine Daten gefunden"
       + `exit()` ohne Abfrage => rot. Gegenprobe: mit Abfrage => gruen.

Aufruf: trading-env/bin/python3 shared/test_main_gegenprobe.py [<listendatei>]
"""

import ast
import os
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HIER)
LISTE = os.path.join(_REPO, "docs", "belege", "TB-107", "f1_laufbereich_vereinigung.txt")
# Die Datei, aus der F3a eine Kopie ohne Abfrage macht (eine der 14 aus TB-105).
MUTATIONSDATEI = os.path.join("strategies", "elliott_wave", "equity_simulation.py")
ABFRAGE = "paths.selektionsmodus() is not None"
ZAHL_TB105 = 14

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print(f"  [ok]     {name}{(' - ' + zusatz) if zusatz else ''}")
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")
        print(f"  [FEHLER] {name}{(' - ' + zusatz) if zusatz else ''}")


def lies_liste(pfad):
    """Repo-relative Pfade aus der Laufbereichsmessung (Spalte 1), ohne
    Kommentarzeilen und ohne Messumschlaege unter docs/."""
    module = []
    with open(pfad, encoding="utf-8") as f:
        for zeile in f:
            if not zeile.strip() or zeile.startswith("#"):
                continue
            p = zeile.rstrip("\n").split("\t")[0]
            if p.startswith("docs/"):
                continue
            module.append(p)
    return module


def _ist_ausstieg(knoten):
    if not isinstance(knoten, ast.Call):
        return False
    f = knoten.func
    if isinstance(f, ast.Name) and f.id in ("exit", "quit"):
        return True
    return (isinstance(f, ast.Attribute) and f.attr == "exit"
            and isinstance(f.value, ast.Name) and f.value.id == "sys")


def _ist_abfrage(knoten):
    return (isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute)
            and knoten.func.attr == "selektionsmodus"
            and isinstance(knoten.func.value, ast.Name) and knoten.func.value.id == "paths")


def _ist_main(knoten):
    t = knoten.test
    return (isinstance(knoten, ast.If) and isinstance(t, ast.Compare)
            and isinstance(t.left, ast.Name) and t.left.id == "__name__"
            and any(isinstance(c, ast.Constant) and c.value == "__main__"
                    for c in t.comparators))


def _geprueft_auf_leer(test):
    """Der Name, der in der Bedingung auf leer geprueft wird, oder None."""
    if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not) \
            and isinstance(test.operand, ast.Name):
        return test.operand.id
    if isinstance(test, ast.Attribute) and test.attr == "empty" \
            and isinstance(test.value, ast.Name):
        return test.value.id
    if (isinstance(test, ast.Compare) and isinstance(test.left, ast.Call)
            and isinstance(test.left.func, ast.Name) and test.left.func.id == "len"
            and test.left.args and isinstance(test.left.args[0], ast.Name)
            and len(test.comparators) == 1
            and isinstance(test.comparators[0], ast.Constant)
            and test.comparators[0].value == 0):
        return test.left.args[0].id
    return None


def _aufrufname(wert):
    if isinstance(wert, ast.Call):
        f = wert.func
        if isinstance(f, ast.Name):
            return f.id
        if isinstance(f, ast.Attribute):
            return f.attr
    return None


def stellen(pfad):
    """Alle Ausstiegsstellen im `__main__`-Block: je Stelle (Zeile, Art, mit
    Abfrage?). Art ist "daten" (gezaehlt) oder "trades" (nur ausgewiesen)."""
    with open(pfad, encoding="utf-8") as f:
        baum = ast.parse(f.read(), filename=pfad)
    raus = []
    for block in (k for k in baum.body if isinstance(k, ast.If) and _ist_main(k)):
        geladen = set()
        for k in ast.walk(block):
            if isinstance(k, ast.Assign):
                name = _aufrufname(k.value)
                if name and name.lower().startswith(("load", "lade")):
                    geladen |= {z.id for z in k.targets if isinstance(z, ast.Name)}
        for k in ast.walk(block):
            if not isinstance(k, ast.If) or k is block:
                continue
            ausstiege = [m for b in k.body for m in ast.walk(b) if _ist_ausstieg(m)]
            if not ausstiege:
                continue
            leer = _geprueft_auf_leer(k.test)
            texte = " ".join(m.value for b in k.body for m in ast.walk(b)
                             if isinstance(m, ast.Constant) and isinstance(m.value, str))
            if (leer is not None and leer in geladen) or "keine daten" in texte.lower():
                art = "daten"
            elif leer is not None:
                art = "trades"
            else:
                continue
            erster = min(m.lineno for m in ausstiege)
            abfrage = any(_ist_abfrage(m) and m.lineno < erster
                          for b in k.body for m in ast.walk(b))
            raus.append((k.lineno, art, abfrage))
    return raus


def gegenprobe(module, wurzel=_REPO):
    """(Datenstellen mit Abfrage, Befunde ohne Abfrage, Trades-Stellen, fehlende Dateien)."""
    mit, ohne, trades, fehlt = [], [], [], []
    for m in module:
        pfad = m if os.path.isabs(m) else os.path.join(wurzel, m)
        if not os.path.exists(pfad):
            fehlt.append(m)
            continue
        if not pfad.endswith(".py"):
            continue
        for zeile, art, abfrage in stellen(pfad):
            eintrag = f"{m}:{zeile}"
            if art == "trades":
                trades.append(eintrag)
            elif abfrage:
                mit.append(eintrag)
            else:
                ohne.append(eintrag)
    return mit, ohne, trades, fehlt


ERFUNDEN = '''import sys


def load_all_symbol_data():
    return {}


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
%s        print("Keine Daten gefunden.")
        exit()
'''
ERFUNDEN_ABFRAGE = ('        import paths\n'
                    '        if paths.selektionsmodus() is not None:\n'
                    '            raise SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)\n')


def main(argv):
    liste = argv[1] if len(argv) > 1 else LISTE
    print(__doc__.strip().split("\n")[0])
    print(f"  Liste: {os.path.relpath(liste, _REPO)}")
    module = lies_liste(liste)
    pruefe("F0: Liste gelesen, nicht leer", len(module) > 0, f"{len(module)} Module")

    mit, ohne, trades, fehlt = gegenprobe(module)
    pruefe("F0b: jede Datei der Liste existiert", not fehlt, f"fehlend {fehlt}")
    pruefe("F2: jede Datenstelle im __main__-Block traegt paths.selektionsmodus()",
           not ohne, f"{len(mit)} mit Abfrage, {len(ohne)} ohne: {ohne}")
    print(f"       Datenstellen mit Abfrage ({len(mit)}; TB-105: {ZAHL_TB105}):")
    for e in mit:
        print(f"         {e}")
    print(f"       ausgewiesen, nicht gezaehlt - Ende bei fehlenden Trades ({len(trades)}):")
    for e in trades:
        print(f"         {e}")

    with tempfile.TemporaryDirectory() as t:
        # --- F3a: Kopie einer der 14 Dateien, Abfrage entfernt --------------
        with open(os.path.join(_REPO, MUTATIONSDATEI), encoding="utf-8") as f:
            text = f.read()
        if text.count(ABFRAGE) != 1:
            pruefe("F3a NICHT PRUEFBAR", False, f"{ABFRAGE!r} nicht genau einmal in {MUTATIONSDATEI}")
        else:
            for mutieren in (True, False):
                kopie = os.path.join(t, "mut" if mutieren else "gegen", "equity_simulation.py")
                os.makedirs(os.path.dirname(kopie))
                with open(kopie, "w", encoding="utf-8") as f:
                    f.write(text.replace(ABFRAGE, "False", 1) if mutieren else text)
                m2, o, _, _ = gegenprobe(module + [kopie])
                if mutieren:
                    pruefe("F3a: Kopie von %s ohne Abfrage in der Liste => rot" % MUTATIONSDATEI,
                           any(e.startswith(kopie) for e in o), f"Befunde {len(o)}")
                else:
                    pruefe("F3a-G: Gegenprobe - dieselbe Kopie MIT Abfrage => gezaehlt, kein Befund an ihr",
                           any(e.startswith(kopie) for e in m2)
                           and not any(e.startswith(kopie) for e in o), f"Befunde {len(o)}")

        # --- F3b: erfundene fuenfzehnte Datei -------------------------------
        for mit_abfrage in (False, True):
            erfunden = os.path.join(t, "abfrage" if mit_abfrage else "ohne", "erfunden.py")
            os.makedirs(os.path.dirname(erfunden))
            with open(erfunden, "w", encoding="utf-8") as f:
                f.write(ERFUNDEN % (ERFUNDEN_ABFRAGE if mit_abfrage else ""))
            m2, o, _, _ = gegenprobe(module + [erfunden])
            if not mit_abfrage:
                pruefe("F3b: erfundene Datei 'Keine Daten gefunden' + exit() ohne Abfrage => rot",
                       any(e.startswith(erfunden) for e in o), f"Befunde {len(o)}")
            else:
                pruefe("F3b-G: Gegenprobe - dieselbe Datei mit Abfrage => gezaehlt, kein Befund",
                       any(e.startswith(erfunden) for e in m2)
                       and not any(e.startswith(erfunden) for e in o), f"Befunde {len(o)}")

    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
