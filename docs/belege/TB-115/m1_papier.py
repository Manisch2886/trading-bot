#!/usr/bin/env python3
"""TB-115 M1, Papierpfad - rein lesend, nur Quelltext (ast), kein Import der Bots.

Je `strategies/<bot>/forward_test.py`:
  (1) Aufrufe `entscheidungskerze.lade(...)` und `.melde()`;
  (2) jeder Aufruf von `fetch_historical_data` AUSSERHALB eines Lambdas
      (= Abruf an der Schicht vorbei);
  (3) jede andere Datenquelle: `read_csv`, `yf.*`, `Client(`, `requests.*`;
  (4) jeder Zugriff auf "die letzte Zeile" nach den Suchmustern unten, mit
      umschliessender Funktion - zur Einordnung von Hand (Entscheidung /
      Anzeige / Protokoll), die Einordnung steht in m1_papier_einordnung.md.

Suchmuster fuer (4), wie im Auftrag verlangt:
  M-a  `<x>.iloc[<negativer Index>]`       (iloc[-1], iloc[-2])
  M-b  `<x>.tail(<n>)`
  M-c  `<x>[<negativer Beginn>:]`          (df[-1:])
  M-d  `<x>.iat[-1]` / `<x>.values[-1]` / `<x>[-1]`
  M-e  `<x>.max()` auf einer Zeitspalte    (Datenende als Anker)
Zusaetzlich Wanduhr-Zugriffe (M-f: `utcnow`, `now`, `time.time`), weil eine
zweite Uhr neben `laufbeginn()` eine zweite Kerzenwahl bedeuten KOENNTE.

Aufruf aus der Repo-Wurzel: python3 docs/belege/TB-115/m1_papier.py
"""
import ast
import glob
import os
import sys


def _funktion(stapel):
    for knoten in reversed(stapel):
        if isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return knoten.name
    return "<modul>"


def _neg(knoten):
    if isinstance(knoten, ast.UnaryOp) and isinstance(knoten.op, ast.USub) \
            and isinstance(knoten.operand, ast.Constant):
        return True
    return isinstance(knoten, ast.Constant) and isinstance(knoten.value, int) \
        and knoten.value < 0


class Sucher(ast.NodeVisitor):
    def __init__(self, zeilen):
        self.zeilen = zeilen
        self.stapel = []
        self.lambdas = 0
        self.funde = []

    def generic_visit(self, knoten):
        self.stapel.append(knoten)
        if isinstance(knoten, ast.Lambda):
            self.lambdas += 1
        self._pruefe(knoten)
        super().generic_visit(knoten)
        if isinstance(knoten, ast.Lambda):
            self.lambdas -= 1
        self.stapel.pop()

    def _fund(self, art, knoten):
        text = self.zeilen[knoten.lineno - 1].strip()
        self.funde.append((knoten.lineno, art, _funktion(self.stapel), text))

    def _pruefe(self, k):
        if isinstance(k, ast.Call):
            f = k.func
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                if f.value.id == "entscheidungskerze" and f.attr in ("lade", "melde"):
                    self._fund(f"(1) entscheidungskerze.{f.attr}", k)
                if f.value.id in ("yf", "requests"):
                    self._fund(f"(3) {f.value.id}.{f.attr}", k)
            if isinstance(f, ast.Attribute) and f.attr == "read_csv":
                self._fund("(3) read_csv", k)
            if isinstance(f, ast.Name) and f.id == "Client":
                self._fund("(3) Client()", k)
            if isinstance(f, ast.Name) and f.id == "fetch_historical_data":
                self._fund("(2) fetch_historical_data " +
                           ("im Lambda (abruf=)" if self.lambdas else
                            "AUSSERHALB eines Lambdas"), k)
            if isinstance(f, ast.Attribute) and f.attr == "tail":
                self._fund("(4) M-b .tail()", k)
            if isinstance(f, ast.Attribute) and f.attr == "max" and not k.args:
                if isinstance(f.value, ast.Subscript):
                    self._fund("(4) M-e .max()", k)
            if isinstance(f, ast.Attribute) and f.attr in ("utcnow", "now", "time"):
                self._fund(f"(M-f) Wanduhr .{f.attr}()", k)
        if isinstance(k, ast.Subscript):
            s = k.slice
            if isinstance(s, ast.Index):            # Python 3.8
                s = s.value
            wert = k.value
            if isinstance(wert, ast.Attribute) and wert.attr == "iloc" and _neg(s):
                self._fund("(4) M-a .iloc[negativ]", k)
            elif isinstance(wert, ast.Attribute) and wert.attr in ("iat", "values") \
                    and _neg(s):
                self._fund(f"(4) M-d .{wert.attr}[negativ]", k)
            elif isinstance(s, ast.Slice) and s.lower is not None and _neg(s.lower):
                self._fund("(4) M-c [negativ:]", k)
            elif _neg(s) and not (isinstance(wert, ast.Attribute)
                                  and wert.attr in ("iloc", "iat", "values")):
                self._fund("(4) M-d [negativ]", k)


def main():
    pfade = sorted(glob.glob(os.path.join("strategies", "*", "forward_test.py")))
    print(f"# TB-115 M1 Papierpfad - {len(pfade)} forward_test.py, ast-Suche")
    for pfad in pfade:
        with open(pfad, encoding="utf-8") as d:
            quelle = d.read()
        s = Sucher(quelle.splitlines())
        s.visit(ast.parse(quelle))
        bot = pfad.split(os.sep)[1]
        n = {"lade": 0, "melde": 0, "vorbei": 0, "quelle": 0, "letzte": 0}
        for _z, art, _f, _t in s.funde:
            n["lade"] += art.endswith(".lade")
            n["melde"] += art.endswith(".melde")
            n["vorbei"] += "AUSSERHALB" in art
            n["quelle"] += art.startswith("(3)")
            n["letzte"] += art.startswith("(4)")
        print(f"\n## {bot}  (lade {n['lade']}, melde {n['melde']}, Abruf an der "
              f"Schicht vorbei {n['vorbei']}, andere Datenquelle {n['quelle']}, "
              f"Letzte-Zeile-Zugriffe {n['letzte']})")
        for zeile, art, funktion, text in sorted(s.funde):
            print(f"  Z.{zeile:>4}  {art:<42} {funktion:<20} {text[:95]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
