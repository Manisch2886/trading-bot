#!/usr/bin/env python3
"""TB-115 M2 (c) - nutzt ein Aktien-Bot absolute Preisniveaus? Rein lesend,
nur Quelltext (ast). Gelesen werden die Entscheidungsmodule der vier
Aktien-Bots, Papier- und Selektionspfad (Laufbereich TB-112):
  forward_test, backtest_*, indicators, zigzag_indicator, elliott_wave_counter,
  equity_simulation, multi_symbol_optimise, live_params.

Suchmuster (jede Fundstelle wird im Ergebnis eingeordnet):
  P1  Vergleich eines Preis-/Volumenausdrucks mit einem Zahl-Literal != 0
      (feste Schwelle in Waehrung, Mindestpreis, runde Zahl)
  P2  Preisausdruck +/- Zahl-Literal (Stopp/Ziel als absoluter Abstand)
  P3  int()/round()/floor()/ceil()/// auf einem Preisausdruck
      (Stueckzahl oder Rundung aus dem Preis ohne Normierung)
  P4  Preisausdruck * / Zahl-Literal ausserhalb von (1 - x/100)-Form
      (zur Kontrolle: relative Stopps erscheinen hier als (1 - PCT / 100))
  P5  Papierpfad: ein in der Datenbank ABGELEGTES Niveau (trade["..._price"])
      wird gegen eine spaeter gelesene Kerze verglichen
Preisausdruck = ein Name/Schluessel, der open/high/low/close/price/preis/
volume/kurs/stop/target/entry/exit enthaelt.

Aufruf aus der Repo-Wurzel: python3 docs/belege/TB-115/m2c_preisniveaus.py
"""
import ast
import glob
import os
import sys

BOTS = ["elliott_wave_stocks", "rsi2_mean_reversion", "turtle_soup_stocks",
        "volatility_breakout"]
MODULE = ["forward_test.py", "backtest_*.py", "indicators.py",
          "zigzag_indicator.py", "elliott_wave_counter.py",
          "equity_simulation.py", "multi_symbol_optimise.py", "live_params.py"]
WOERTER = ("open", "high", "low", "close", "price", "preis", "volume", "kurs",
           "stop", "target", "entry", "exit")


def _texte(k):
    for u in ast.walk(k):
        if isinstance(u, ast.Name):
            yield u.id.lower()
        elif isinstance(u, ast.Attribute):
            yield u.attr.lower()
        elif isinstance(u, ast.Constant) and isinstance(u.value, str):
            yield u.value.lower()


def preisig(k):
    return any(w in t for t in _texte(k) for w in WOERTER)


def zahl(k):
    if isinstance(k, ast.UnaryOp) and isinstance(k.operand, ast.Constant):
        k = k.operand
    return isinstance(k, ast.Constant) and isinstance(k.value, (int, float)) \
        and not isinstance(k.value, bool) and k.value != 0


def db_niveau(k):
    """trade["stop_price"] / trade["target_price"] / trade["entry_price"]"""
    return (isinstance(k, ast.Subscript) and isinstance(k.value, ast.Name)
            and k.value.id == "trade")


def main():
    print("# TB-115 M2 (c) - absolute Preisniveaus in den vier Aktien-Bots")
    gesamt = 0
    for bot in BOTS:
        dateien = sorted({p for m in MODULE
                          for p in glob.glob(os.path.join("strategies", bot, m))})
        print(f"\n## {bot}: {len(dateien)} Module")
        for pfad in dateien:
            quelle = open(pfad, encoding="utf-8").read()
            zeilen = quelle.splitlines()
            baum = ast.parse(quelle)
            haupt = set()
            for k in baum.body:          # Demo-Code unter __main__ markieren
                if isinstance(k, ast.If) and "__main__" in ast.dump(k.test):
                    haupt |= set(range(k.lineno, k.end_lineno + 1))
            funde = []
            for k in ast.walk(baum):
                if isinstance(k, ast.Compare):
                    teile = [k.left] + list(k.comparators)
                    if any(zahl(t) for t in teile) and any(
                            preisig(t) for t in teile if not zahl(t)):
                        funde.append((k.lineno, "P1"))
                    if any(db_niveau(t) for t in teile) and \
                            os.path.basename(pfad) == "forward_test.py":
                        funde.append((k.lineno, "P5"))
                elif isinstance(k, ast.BinOp):
                    l, r = k.left, k.right
                    if isinstance(k.op, (ast.Add, ast.Sub)) and (
                            (zahl(r) and preisig(l)) or (zahl(l) and preisig(r))):
                        funde.append((k.lineno, "P2"))
                    if isinstance(k.op, ast.FloorDiv) and (preisig(l) or preisig(r)):
                        funde.append((k.lineno, "P3"))
                    if isinstance(k.op, (ast.Mult, ast.Div)) and (
                            (zahl(r) and preisig(l)) or (zahl(l) and preisig(r))):
                        funde.append((k.lineno, "P4"))
                elif isinstance(k, ast.Call) and isinstance(k.func, (ast.Name, ast.Attribute)):
                    name = k.func.id if isinstance(k.func, ast.Name) else k.func.attr
                    if name in ("int", "round", "floor", "ceil") and k.args \
                            and preisig(k.args[0]):
                        funde.append((k.lineno, "P3"))
            funde = sorted(set(funde))
            if not funde:
                continue
            print(f"  {pfad}")
            for zeile, art in funde:
                ort = "  [__main__]" if zeile in haupt else ""
                print(f"    Z.{zeile:>4} {art}{ort}  {zeilen[zeile - 1].strip()[:110]}")
                gesamt += 1
    print(f"\nFundstellen gesamt: {gesamt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
