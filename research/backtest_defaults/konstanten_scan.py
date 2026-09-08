"""
Schritt 3: Modulkonstanten, die NICHT ueber einen Default wirken
================================================================================
default_scan.py betrachtet Funktions-DEFAULTS. Es gibt aber einen zweiten,
leicht zu uebersehenden Weg, auf dem eine Konstante wirksam wird: sie wird
direkt IM RUMPF einer Funktion gelesen, ohne je Parameter zu sein.

    TAKE_PROFIT_FIB = 0.382                      # Modulebene
    def run_backtest(price_df, impulses, ...):
        target_price = entry_price + total_move * TAKE_PROFIT_FIB   # <- hier

Ein reiner Default-Scan meldet hier NICHTS, obwohl der Wert die Trades
bestimmt. Dieses Skript schliesst die Luecke.

Dazu kommt ein dritter Weg, der die Bewertung wieder umdreht: MONKEY
PATCHING. Beide Elliott-Bots setzen den Wert vor dem Backtest zur Laufzeit
von aussen neu -

    backtest_elliott.TAKE_PROFIT_FIB = take_profit_fib

- womit das Modul-Literal wieder folgenlos ist. Wer nur die Zahlen
vergleicht, meldet hier eine dramatische Abweichung (0.382 gegen live
0.236), die in Wirklichkeit nie zum Tragen kommt. Deshalb wird auch nach
solchen Zuweisungen gesucht und ihre Rolle (LIVE/SUCHE/STUDIE) bestimmt.

Ergebnis je Konstante mit Gegenstueck in live_params.py:
  WIRKT      wird im Live-Pfad gelesen und dort NICHT gepatcht
  GEPATCHT   wird im Live-Pfad vor der Nutzung ueberschrieben -> folgenlos
  NUR DEFAULT  wird nur als Parameter-Default genutzt (Sache von default_scan)

WICHTIG - reine Untersuchung: veraendert keine Datei ausserhalb von
research/backtest_defaults/.

Nutzung:  python3 konstanten_scan.py
"""

import ast
import os

from default_scan import (BOTS, STRATEGIES, Datei, MODULEBENE,
                           modul_konstanten, live_params_importe, LIVE_EINSTIEG)
from kandidaten import ALIASES


def _funktions_leser(datei: Datei, konstanten: set) -> dict:
    """{konstante: {funktionsname, ...}} - wer liest sie im Rumpf?"""
    leser = {}

    def besuche(knoten, umgebung):
        for kind in ast.iter_child_nodes(knoten):
            if isinstance(kind, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Die Signatur (Defaults) gehoert zur UMGEBENDEN Ebene, nicht
                # zum Rumpf - sonst zaehlte jeder Default als Rumpf-Lesezugriff.
                for teil in kind.body:
                    besuche_rumpf(teil, kind.name)
                continue
            if isinstance(kind, ast.Name) and isinstance(kind.ctx, ast.Load) \
                    and kind.id in konstanten and umgebung != MODULEBENE:
                leser.setdefault(kind.id, set()).add(umgebung)
            besuche(kind, umgebung)

    def besuche_rumpf(knoten, umgebung):
        if isinstance(knoten, ast.Name) and isinstance(knoten.ctx, ast.Load) \
                and knoten.id in konstanten:
            leser.setdefault(knoten.id, set()).add(umgebung)
        for kind in ast.iter_child_nodes(knoten):
            if isinstance(kind, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for teil in kind.body:
                    besuche_rumpf(teil, f"{umgebung}.{kind.name}")
                continue
            besuche_rumpf(kind, umgebung)

    besuche(datei.baum, MODULEBENE)
    return leser


def _patches(ordner: str, dateien: dict) -> list:
    """Zuweisungen der Form  modul.KONSTANTE = ...  im ganzen Bot-Ordner."""
    treffer = []
    for name, datei in dateien.items():
        for knoten in ast.walk(datei.baum):
            if not isinstance(knoten, ast.Assign):
                continue
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Attribute) and \
                        isinstance(ziel.value, ast.Name) and ziel.attr.isupper():
                    treffer.append({"datei": name, "modul": ziel.value.id + ".py",
                                     "konstante": ziel.attr, "zeile": knoten.lineno})
    return treffer


def main():
    print("Modulkonstanten mit Gegenstueck in live_params.py, die im "
          "Funktionsrumpf gelesen werden\n")
    kopf = (f"{'Bot':<27} {'Modul':<24} {'Konstante':<22} "
            f"{'Wert':>8} {'live':>8}  Urteil")
    print(kopf)
    print("-" * len(kopf))

    for bot in BOTS:
        ordner = os.path.join(STRATEGIES, bot)
        namen = sorted(f for f in os.listdir(ordner) if f.endswith(".py"))
        dateien = {n: Datei(ordner, n) for n in namen}
        live_werte = modul_konstanten(os.path.join(ordner, "live_params.py"))
        patches = _patches(ordner, dateien)

        for dname, datei in dateien.items():
            if dname in ("live_params.py", "forward_test.py"):
                continue
            konst = modul_konstanten(os.path.join(ordner, dname))
            # Namen, die das Modul bereits AUS live_params.py importiert,
            # sind ebenfalls Gegenstuecke - sie tauchen nur nicht als
            # Zuweisung auf. Ohne sie fiele ein gekoppelter Wert stillschweigend
            # aus der Tabelle, statt als "GEKOPPELT" bestaetigt zu werden.
            importiert = live_params_importe(os.path.join(ordner, dname))
            mit_gegenstueck = {k for k in konst
                                if ALIASES.get(k, k) in live_werte}
            mit_gegenstueck |= {k for k, ln in importiert.items()
                                 if ln in live_werte}
            if not mit_gegenstueck:
                continue

            leser = _funktions_leser(datei, mit_gegenstueck)
            for k in sorted(mit_gegenstueck):
                ln = importiert.get(k) or ALIASES.get(k, k)
                if k in importiert:
                    gelesen = (f", gelesen in {', '.join(sorted(leser[k]))}"
                                if k in leser else "")
                    print(f"{bot:<27} {dname:<24} {k:<22} "
                          f"{live_werte[ln]!r:>8} {live_werte[ln]!r:>8}  "
                          f"GEKOPPELT an live_params.{ln}{gelesen}")
                    continue
                if k not in leser:
                    urteil = "nur Parameter-Default (siehe default_scan.py)"
                else:
                    passend = [p for p in patches
                                if p["modul"] == dname and p["konstante"] == k]
                    live_patch = [p for p in passend
                                   if p["datei"] in LIVE_EINSTIEG]
                    if live_patch:
                        stellen = ", ".join(f"{p['datei']}:{p['zeile']}"
                                             for p in live_patch)
                        urteil = f"GEPATCHT im Live-Pfad ({stellen}) -> folgenlos"
                    else:
                        urteil = f"WIRKT (gelesen in {', '.join(sorted(leser[k]))})"

                gleich = "" if konst[k] == live_werte[ln] else "  <-- UNGLEICH"
                print(f"{bot:<27} {dname:<24} {k:<22} "
                      f"{konst[k]!r:>8} {live_werte[ln]!r:>8}  {urteil}{gleich}")


if __name__ == "__main__":
    main()
