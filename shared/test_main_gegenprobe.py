#!/usr/bin/env python3
"""
TB-107 Block F / TB-109 Block E1 - Gegenprobe ueber alle `__main__`-Stellen des Laufbereichs
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

TB-109 Block E1 (Fable 25e (2), "null Trades ist ein Wert"): Gezaehlt wird
seitdem JEDES `exit()`/`sys.exit()`/`quit()` im `__main__`-Block, dem kein
geschriebenes Ergebnis vorausgeht - nicht nur das nach fehlender Eingabe.
Die Abgrenzung "nach einer Rechnung" (bis TB-108: `trades.empty` nur
ausgewiesen) ist nicht das Kriterium; das Kriterium ist 36.5: kein Aufruf
endet mit 0, ohne dass gemessen und geschrieben wurde. Eine Stelle ist:
  * ein Ausstieg in einem `if` des `__main__`-Blocks (vorzeitiges Ende), und
  * im Rumpf dieses `if` steht VOR dem Ausstieg kein Schreibaufruf eines
    Ergebnisses (`json.dump`, `.to_csv`/`.to_json`/`.to_parquet`,
    `.write_text`, `open(..., "w"/"a"/"x")`). Steht einer davor, wird die
    Stelle ausgewiesen ("nach geschriebenem Ergebnis"), nicht gezaehlt.
Die Art (Daten / Trades / sonst) wird nur noch ausgewiesen. Ausgewiesen, nicht
gezaehlt: der Ausstieg als letzte Anweisung des `__main__`-Blocks
(`sys.exit(main())` u. ae.) - er traegt die Rueckgabe des Laufs nach aussen,
nachdem der Block gearbeitet hat; was `main()` in sich tut, prueft diese
Probe nicht.
Erwartet am Stand TB-109: 24 Stellen (die 14 aus TB-105 C und die 10 aus
TB-109 B), alle mit Abfrage.

  F2   am echten Stand: jede Stelle traegt die Abfrage, und es sind 24.
  F3a  Mutation: eine Kopie einer der 14 Dateien, an der Datenstelle OHNE
       Abfrage, der Liste hinzugefuegt => rot. Gegenprobe: dieselbe Kopie ohne
       Mutation => gruen.
  F3b  Mutation: eine erfundene Datei mit "Keine Daten gefunden" + `exit()`
       ohne Abfrage => rot. Gegenprobe: mit Abfrage => gruen.
  F3c  (TB-109) Mutation: eine Kopie derselben Datei, an der Stelle "Keine
       Trades" OHNE Abfrage - die 25. Stelle => rot. Gegenprobe: ohne
       Mutation => gruen.
  F3d  (TB-109) Mutation: eine erfundene Datei mit einem `exit()` ohne
       Daten- oder Trades-Bezug (`if len(sys.argv) > 2: exit()`) ohne
       Abfrage => rot. Gegenprobe: mit Abfrage => gruen.
  F3e  (TB-109) Gegenprobe zur Ausnahme: dieselbe erfundene Datei, im Rumpf
       VOR dem `exit()` ein `json.dump(...)` in eine zum Schreiben geoeffnete
       Datei, ohne Abfrage => nicht gezaehlt, kein Befund; und ein
       `sys.exit(main())` als letzte Anweisung => nicht gezaehlt.

Aufruf: trading-env/bin/python3 shared/test_main_gegenprobe.py [<listendatei>]
"""

import ast
import os
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HIER)
LISTE = os.path.join(_REPO, "docs", "belege", "TB-107", "f1_laufbereich_vereinigung.txt")
# Die Datei, aus der F3a/F3c eine Kopie ohne Abfrage machen (eine der 14 aus
# TB-105, zugleich eine der 10 aus TB-109). Die Abfrage steht dort zweimal;
# die Mutation nennt deshalb die Meldung der Stelle mit.
MUTATIONSDATEI = os.path.join("strategies", "elliott_wave", "equity_simulation.py")
ABFRAGE = "paths.selektionsmodus() is not None"
ABFRAGE_DATEN = ABFRAGE + ':\n            sys.stderr.write("Keine Daten'
ABFRAGE_TRADES = ABFRAGE + ':\n            sys.stderr.write("Keine Trades'
ZAHL_TB105 = 14
ZAHL_TB109 = 10
ZAHL = ZAHL_TB105 + ZAHL_TB109

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


def _schreibt_ergebnis(knoten):
    """Ein Schreibaufruf eines Ergebnisses (TB-109): json.dump, .to_csv,
    .to_json, .to_parquet, .write_text, open(..., "w"/"a"/"x")."""
    if not isinstance(knoten, ast.Call):
        return False
    f = knoten.func
    if isinstance(f, ast.Attribute):
        if f.attr in ("to_csv", "to_json", "to_parquet", "write_text"):
            return True
        if f.attr == "dump" and isinstance(f.value, ast.Name) and f.value.id == "json":
            return True
    if isinstance(f, ast.Name) and f.id == "open":
        modus = knoten.args[1] if len(knoten.args) > 1 else next(
            (k.value for k in knoten.keywords if k.arg == "mode"), None)
        return (isinstance(modus, ast.Constant) and isinstance(modus.value, str)
                and any(z in modus.value for z in "wax"))
    return False


def stellen(pfad):
    """Alle Ausstiegsstellen im `__main__`-Block: je Stelle (Zeile, Art, mit
    Abfrage?). Art ist "daten", "trades" oder "sonst" (gezaehlt, TB-109),
    "nach_ergebnis" oder "ende" (nur ausgewiesen)."""
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
        # Der Ausstieg als Anweisung auf oberster Ebene des Blocks: Ende.
        for st in block.body:
            if isinstance(st, ast.Expr) and _ist_ausstieg(st.value):
                raus.append((st.lineno, "ende", False))
        gesehen = set()
        for k in ast.walk(block):
            if not isinstance(k, ast.If) or k is block:
                continue
            ausstiege = [m for b in k.body for m in ast.walk(b) if _ist_ausstieg(m)]
            # verschachtelte if: die Stelle gehoert dem innersten if
            ausstiege = [m for m in ausstiege if id(m) not in gesehen
                         and not any(isinstance(i, ast.If) and i is not k
                                     and any(m is x for b2 in i.body for x in ast.walk(b2))
                                     for b in k.body for i in ast.walk(b))]
            if not ausstiege:
                continue
            gesehen |= {id(m) for m in ausstiege}
            erster = min(m.lineno for m in ausstiege)
            leer = _geprueft_auf_leer(k.test)
            texte = " ".join(m.value for b in k.body for m in ast.walk(b)
                             if isinstance(m, ast.Constant) and isinstance(m.value, str))
            if any(_schreibt_ergebnis(m) and m.lineno < erster
                   for b in k.body for m in ast.walk(b)):
                art = "nach_ergebnis"
            elif (leer is not None and leer in geladen) or "keine daten" in texte.lower():
                art = "daten"
            elif leer is not None:
                art = "trades"
            else:
                art = "sonst"
            abfrage = any(_ist_abfrage(m) and m.lineno < erster
                          for b in k.body for m in ast.walk(b))
            raus.append((k.lineno, art, abfrage))
    return raus


def gegenprobe(module, wurzel=_REPO):
    """(Stellen mit Abfrage, Befunde ohne Abfrage, ausgewiesene nicht
    gezaehlte Ausstiege, fehlende Dateien). Eintraege "<pfad>:<zeile> (<art>)"."""
    mit, ohne, ausgewiesen, fehlt = [], [], [], []
    for m in module:
        pfad = m if os.path.isabs(m) else os.path.join(wurzel, m)
        if not os.path.exists(pfad):
            fehlt.append(m)
            continue
        if not pfad.endswith(".py"):
            continue
        for zeile, art, abfrage in stellen(pfad):
            eintrag = f"{m}:{zeile} ({art})"
            if art in ("ende", "nach_ergebnis"):
                ausgewiesen.append(eintrag)
            elif abfrage:
                mit.append(eintrag)
            else:
                ohne.append(eintrag)
    return mit, ohne, ausgewiesen, fehlt


ERFUNDEN = '''import sys


def load_all_symbol_data():
    return {}


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
%s        print("Keine Daten gefunden.")
        exit()
'''
# TB-109 F3d/F3e: ein Ausstieg ohne Daten- oder Trades-Bezug.
ERFUNDEN_SONST = '''import json
import sys


def main():
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 2:
%s        print("zu viele Argumente")
        exit()
    sys.exit(main())
'''
ERFUNDEN_SCHREIBT = ('        with open("ergebnis.json", "w") as f:\n'
                     '            json.dump({"trades": []}, f)\n')
ERFUNDEN_ABFRAGE = ('        import paths\n'
                    '        if paths.selektionsmodus() is not None:\n'
                    '            raise SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)\n')


def main(argv):
    liste = argv[1] if len(argv) > 1 else LISTE
    print(__doc__.strip().split("\n")[0])
    print(f"  Liste: {os.path.relpath(liste, _REPO)}")
    module = lies_liste(liste)
    pruefe("F0: Liste gelesen, nicht leer", len(module) > 0, f"{len(module)} Module")

    mit, ohne, ausgewiesen, fehlt = gegenprobe(module)
    pruefe("F0b: jede Datei der Liste existiert", not fehlt, f"fehlend {fehlt}")
    pruefe("F2: jeder Ausstieg ohne geschriebenes Ergebnis im __main__-Block traegt paths.selektionsmodus()",
           not ohne, f"{len(mit)} mit Abfrage, {len(ohne)} ohne: {ohne}")
    pruefe(f"F2b: es sind {ZAHL} Stellen (TB-105: {ZAHL_TB105}, TB-109: {ZAHL_TB109})",
           len(mit) + len(ohne) == ZAHL, f"{len(mit) + len(ohne)} gezaehlt")
    print(f"       Stellen mit Abfrage ({len(mit)}):")
    for e in mit:
        print(f"         {e}")
    print(f"       ausgewiesen, nicht gezaehlt - Ende des Blocks bzw. nach geschriebenem Ergebnis ({len(ausgewiesen)}):")
    for e in ausgewiesen:
        print(f"         {e}")

    with tempfile.TemporaryDirectory() as t:
        # --- F3a: Kopie einer der 14 Dateien, Abfrage entfernt --------------
        with open(os.path.join(_REPO, MUTATIONSDATEI), encoding="utf-8") as f:
            text = f.read()
        for marke, stelle in (("F3a", ABFRAGE_DATEN), ("F3c", ABFRAGE_TRADES)):
            if text.count(stelle) != 1:
                pruefe(f"{marke} NICHT PRUEFBAR", False, f"{stelle!r} nicht genau einmal in {MUTATIONSDATEI}")
                continue
            ersatz = stelle.replace(ABFRAGE, "False", 1)
            for mutieren in (True, False):
                kopie = os.path.join(t, marke + ("mut" if mutieren else "gegen"), "equity_simulation.py")
                os.makedirs(os.path.dirname(kopie))
                with open(kopie, "w", encoding="utf-8") as f:
                    f.write(text.replace(stelle, ersatz, 1) if mutieren else text)
                m2, o, _, _ = gegenprobe(module + [kopie])
                was = "Datenstelle" if marke == "F3a" else "Stelle 'Keine Trades' (die 25.)"
                if mutieren:
                    pruefe(f"{marke}: Kopie von {MUTATIONSDATEI}, {was} ohne Abfrage, in der Liste => rot",
                           sum(e.startswith(kopie) for e in o) == 1, f"Befunde {len(o)}")
                else:
                    pruefe(f"{marke}-G: Gegenprobe - dieselbe Kopie MIT Abfrage => gezaehlt, kein Befund an ihr",
                           sum(e.startswith(kopie) for e in m2) == 2
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

        # --- F3d/F3e (TB-109): Ausstieg ohne Daten-/Trades-Bezug ------------
        for fall, einsatz in (("F3d", ""), ("F3d-G", ERFUNDEN_ABFRAGE), ("F3e", ERFUNDEN_SCHREIBT)):
            erfunden = os.path.join(t, fall, "sonst.py")
            os.makedirs(os.path.dirname(erfunden))
            with open(erfunden, "w", encoding="utf-8") as f:
                f.write(ERFUNDEN_SONST % einsatz)
            m2, o, a2, _ = gegenprobe(module + [erfunden])
            eigen_o = [e for e in o if e.startswith(erfunden)]
            eigen_m = [e for e in m2 if e.startswith(erfunden)]
            eigen_a = [e for e in a2 if e.startswith(erfunden)]
            if fall == "F3d":
                pruefe("F3d: erfundene Datei, exit() ohne Daten-/Trades-Bezug, ohne Abfrage => rot",
                       len(eigen_o) == 1 and eigen_o[0].endswith("(sonst)"), f"Befunde {eigen_o}")
            elif fall == "F3d-G":
                pruefe("F3d-G: Gegenprobe - dieselbe Datei mit Abfrage => gezaehlt, kein Befund",
                       len(eigen_m) == 1 and not eigen_o, f"mit {eigen_m}, Befunde {eigen_o}")
            else:
                pruefe("F3e: json.dump vor dem exit(), ohne Abfrage => nicht gezaehlt (nach_ergebnis); "
                       "sys.exit(main()) am Blockende => nicht gezaehlt (ende)",
                       not eigen_o and not eigen_m
                       and sorted(e.rsplit(" ", 1)[1] for e in eigen_a) == ["(ende)", "(nach_ergebnis)"],
                       f"ausgewiesen {eigen_a}, Befunde {eigen_o}")

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
