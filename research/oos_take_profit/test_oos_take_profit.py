"""
Selbsttests zur Take-Profit-Uebergabe in der OOS-Validierung
================================================================================
Vier Gruppen:

  A) DIE UEBERGABE SELBST - per AST, nicht per Textsuche. Eine Suche nach
     "use_take_profit" faende auch den Docstring, den Kommentar oder eine
     gleichnamige Variable in einer anderen Funktion. Geprueft wird
     stattdessen der Aufrufknoten von collect_all_trades() und ob das
     Schluesselwort dort wirklich gesetzt ist - und ob sein Wert aus
     `best` stammt statt aus einer festen Zahl.

  B) DIE None/NaN-FALLE. Der Optimierer legt take_profit_fib als None ab,
     wenn die Kombination ohne festes Ziel laeuft (multi_symbol_optimise.py
     :153). Was daraus in der Ergebnis-DataFrame wird, haengt davon ab, ob
     UEBERHAUPT eine Kombination mit festem Ziel die Mindestfilter besteht:

       - besteht mindestens eine, ist die Spalte float64 -> NaN
       - besteht keine, ist die Spalte object     -> echtes None

     Beim Aktien-Bot trat der zweite Fall ein, und genau daran ist die
     fehlerhafte Fassung mit einem TypeError gestorben. Eine Loesung, die
     nur an NaN denkt, greift also zu kurz. Der Test baut beide Faelle nach.

  C) DASS DER SCHALTER UEBERHAUPT ETWAS TUT. simulate_trade() wird mit
     einer konstruierten Kursreihe zweimal aufgerufen. Waere das Flag
     wirkungslos, waere der ganze Fix sinnlos - und der Vorher/Nachher-
     Vergleich im Bericht wertlos.

  D) ABGRENZUNG. Der Krypto-Elliott-Bot kennt diese Dimension nicht; das
     wird belegt statt behauptet.

Nutzung:  python3 test_oos_take_profit.py
"""

import ast
import os
import sys

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
AKTIEN = os.path.join(_REPO_ROOT, "strategies", "elliott_wave_stocks")
KRYPTO = os.path.join(_REPO_ROOT, "strategies", "elliott_wave")

_bestanden = 0
_fehler = []


def check(name, ok, detail=""):
    global _bestanden
    if ok:
        _bestanden += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        _fehler.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


def _baum(pfad):
    with open(pfad, encoding="utf-8") as f:
        return ast.parse(f.read(), filename=pfad)


def aufruf_argumente(pfad: str, funktionsname: str) -> list:
    """Je Aufruf von `funktionsname`: {schluesselwort: Quelltext des Werts}.

    Bewusst ueber den Syntaxbaum: eine Textsuche wuerde auch Docstrings,
    Kommentare und gleichnamige Parameter fremder Funktionen treffen -
    genau die Verwechslung, die in dieser Session schon zweimal einen
    Befund verdeckt bzw. einen Fehlalarm ausgeloest hat.
    """
    treffer = []
    for knoten in ast.walk(_baum(pfad)):
        if not isinstance(knoten, ast.Call):
            continue
        ziel = knoten.func
        name = (ziel.id if isinstance(ziel, ast.Name)
                else ziel.attr if isinstance(ziel, ast.Attribute) else None)
        if name != funktionsname:
            continue
        treffer.append({kw.arg: ast.unparse(kw.value)
                         for kw in knoten.keywords if kw.arg})
    return treffer


# ---------------------------------------------------------------------------
# A) Die Uebergabe
# ---------------------------------------------------------------------------

def teste_uebergabe():
    print("\nA) Uebergabe von use_take_profit")

    oos = os.path.join(AKTIEN, "oos_equity_simulation.py")
    aufrufe = aufruf_argumente(oos, "collect_all_trades")
    check("oos_equity_simulation.py ruft collect_all_trades genau einmal auf",
          len(aufrufe) == 1, f"{len(aufrufe)} Aufrufe")
    if not aufrufe:
        return
    args = aufrufe[0]

    check("Der Aufruf setzt use_take_profit",
          "use_take_profit" in args, str(sorted(args)))
    check("Der Wert stammt aus dem In-Sample-Gewinner, nicht aus einer "
          "festen Zahl",
          "best[" in args.get("use_take_profit", ""),
          args.get("use_take_profit"))
    check("Die uebrigen drei Parameter kommen weiterhin aus dem Gewinner",
          all("best[" in args.get(p, "") for p in
              ("deviation_pct", "stop_loss_pct", "take_profit_fib")),
          str({p: args.get(p) for p in
                ("deviation_pct", "stop_loss_pct", "take_profit_fib")}))
    check("take_profit_fib faengt den Fall 'kein festes Ziel' ab "
          "(sonst NaN, siehe Gruppe B)",
          "if" in args.get("take_profit_fib", ""),
          args.get("take_profit_fib"))

    # Das Gegenbeispiel, an dem der Fix sich orientiert: hier war es schon
    # richtig. Faellt das zurueck, ist auch der Fix hier fragwuerdig.
    wf = os.path.join(AKTIEN, "multi_symbol_walk_forward.py")
    wf_aufrufe = aufruf_argumente(wf, "evaluate_combination_multi")
    check("multi_symbol_walk_forward.py reicht use_take_profit weiterhin durch",
          any("use_take_profit" in a for a in wf_aufrufe),
          str([sorted(a) for a in wf_aufrufe]))


# ---------------------------------------------------------------------------
# B) Die NaN-Falle
# ---------------------------------------------------------------------------

def teste_none_falle():
    print("\nB) take_profit_fib, wenn der Gewinner ohne festes Ziel laeuft")

    # Genau die Struktur, die run_multi_optimisation() liefert: Zeilen mit
    # use_take_profit=False tragen take_profit_fib=None.
    gemischt = pd.DataFrame([
        {"take_profit_fib": None, "use_take_profit": False},
        {"take_profit_fib": 0.236, "use_take_profit": True},
    ])
    nur_ohne_ziel = pd.DataFrame([
        {"take_profit_fib": None, "use_take_profit": False},
        {"take_profit_fib": None, "use_take_profit": False},
    ])

    check("Bestehen auch Kombinationen MIT Ziel die Filter, wird die Spalte "
          "float64 - aus None wird NaN",
          str(gemischt["take_profit_fib"].dtype) == "float64"
          and pd.isna(gemischt.iloc[0]["take_profit_fib"]),
          str(gemischt["take_profit_fib"].dtype))

    check("Besteht KEINE Kombination mit Ziel, bleibt die Spalte object - "
          "und damit ein echtes None",
          str(nur_ohne_ziel["take_profit_fib"].dtype) == "object"
          and nur_ohne_ziel.iloc[0]["take_profit_fib"] is None,
          str(nur_ohne_ziel["take_profit_fib"].dtype))

    # Der zweite Fall ist der, an dem die fehlerhafte Fassung stirbt:
    # None laesst sich nicht multiplizieren, NaN schon (stillschweigend).
    fehler = None
    try:
        100.0 * nur_ohne_ziel.iloc[0]["take_profit_fib"]
    except TypeError as e:
        fehler = str(e)
    check("None * float wirft TypeError - genau der Abbruch der bisherigen "
          "Fassung",
          fehler is not None and "NoneType" in fehler, str(fehler))
    check("NaN * float wuerde dagegen stillschweigend NaN ergeben - der "
          "Fehler waere dann unsichtbar geblieben",
          pd.isna(100.0 * gemischt.iloc[0]["take_profit_fib"]))

    # Der Ausdruck, den der Fix verwendet (identisch zu
    # multi_symbol_walk_forward.py:77). Er muss BEIDE Faelle abfangen.
    for name, tabelle in (("object/None", nur_ohne_ziel),
                           ("float64/NaN", gemischt)):
        zeile = tabelle.iloc[0]
        wert = (zeile["take_profit_fib"]
                if zeile["use_take_profit"] else 0.236)
        check(f"Die gewaehlte Loesung uebergibt auch bei {name} eine echte Zahl",
              isinstance(wert, float) and not pd.isna(wert), repr(wert))

    mit_ziel = gemischt.iloc[1]
    wert = (mit_ziel["take_profit_fib"]
            if mit_ziel["use_take_profit"] else 0.236)
    check("Im Fall MIT Ziel bleibt der optimierte Wert unveraendert",
          wert == 0.236, repr(wert))


# ---------------------------------------------------------------------------
# C) Wirkt der Schalter ueberhaupt?
# ---------------------------------------------------------------------------

def teste_wirkung():
    print("\nC) Wirkung des Schalters auf einen einzelnen Trade")

    sys.path.insert(0, AKTIEN)
    sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))
    sys.path.insert(0, _DIR)      # yfinance-Attrappe, siehe stubs/
    sys.path.append(os.path.join(_DIR, "stubs"))
    import backtest_elliott

    # Long-Trade: der Kurs erreicht erst das Ziel (110) und steigt danach
    # weiter auf 150. Mit festem Ziel wird bei 110 verkauft, ohne Ziel
    # laeuft die Position bis zum Zeitausstieg.
    kurse = pd.DataFrame({
        "open_time": pd.date_range("2025-01-01", periods=5, freq="D"),
        "high": [101.0, 111.0, 130.0, 150.0, 150.0],
        "low":  [99.0, 105.0, 120.0, 140.0, 145.0],
        "close": [100.0, 110.0, 128.0, 148.0, 148.0],
    })
    einstieg = kurse["open_time"].iloc[0]

    mit = backtest_elliott.simulate_trade(
        kurse, einstieg, 100.0, "long", target_price=110.0, stop_price=90.0,
        max_hold_hours=10, use_take_profit=True)
    ohne = backtest_elliott.simulate_trade(
        kurse, einstieg, 100.0, "long", target_price=float("inf"),
        stop_price=90.0, max_hold_hours=10, use_take_profit=False)

    check("MIT Take-Profit wird am Ziel ausgestiegen",
          mit["result"] == "take_profit" and mit["exit_price"] == 110.0,
          str(mit))
    check("OHNE Take-Profit laeuft die Position weiter",
          ohne["result"] == "time_exit" and ohne["exit_price"] > 110.0,
          str(ohne))
    check("Der Schalter aendert das Ergebnis also wirklich - ohne das "
          "waere der ganze Fix wirkungslos",
          mit["exit_price"] != ohne["exit_price"],
          f"{mit['exit_price']} vs. {ohne['exit_price']}")

    # Der Stop hat weiterhin Vorrang - der Schalter darf ihn nicht aushebeln.
    fallende = kurse.copy()
    fallende["low"] = [99.0, 85.0, 80.0, 75.0, 70.0]
    gestoppt = backtest_elliott.simulate_trade(
        fallende, einstieg, 100.0, "long", target_price=float("inf"),
        stop_price=90.0, max_hold_hours=10, use_take_profit=False)
    check("Der Stop-Loss greift auch ohne festes Ziel",
          gestoppt["result"] == "stop_loss", str(gestoppt))


# ---------------------------------------------------------------------------
# D) Abgrenzung zum Krypto-Bot
# ---------------------------------------------------------------------------

def teste_krypto_nicht_betroffen():
    print("\nD) Der Krypto-Elliott-Bot ist nicht betroffen")

    signatur = None
    for knoten in _baum(os.path.join(KRYPTO, "backtest_elliott.py")).body:
        if isinstance(knoten, ast.FunctionDef) and knoten.name == "run_backtest":
            signatur = [a.arg for a in knoten.args.args]
    check("Krypto: run_backtest kennt keinen use_take_profit-Parameter",
          signatur is not None and "use_take_profit" not in signatur,
          str(signatur))

    treffer = []
    for name in sorted(os.listdir(KRYPTO)):
        if not name.endswith(".py"):
            continue
        with open(os.path.join(KRYPTO, name), encoding="utf-8") as f:
            if "use_take_profit" in f.read() or "USE_TAKE_PROFIT" in f.read():
                treffer.append(name)
    check("Krypto: die Dimension kommt im ganzen Bot nicht vor - es gibt "
          "dort nichts durchzureichen",
          not treffer, str(treffer))

    # Und zur Gegenkontrolle: beim Aktien-Bot kommt sie sehr wohl vor.
    aktien_treffer = []
    for name in sorted(os.listdir(AKTIEN)):
        if not name.endswith(".py"):
            continue
        with open(os.path.join(AKTIEN, name), encoding="utf-8") as f:
            if "use_take_profit" in f.read():
                aktien_treffer.append(name)
    check("Aktien: die Dimension gibt es dort tatsaechlich (Gegenkontrolle, "
          "damit die Pruefung oben nicht nur trivial gruen ist)",
          len(aktien_treffer) >= 5, str(aktien_treffer))


# ---------------------------------------------------------------------------
# E) Die allgemeine Regel statt nur dieses einen Falls
# ---------------------------------------------------------------------------

def optimierer_dimensionen(ordner: str) -> set:
    """Welche Strategie-Parameter legt multi_symbol_optimise.py in sein
    Ergebnis-dict? Genau die kann der Gewinner tragen - und genau die muss
    die OOS-Simulation weiterreichen, sonst validiert sie etwas anderes."""
    bekannt = {"deviation_pct", "stop_loss_pct", "take_profit_fib",
               "use_take_profit", "donchian_period", "stop_mode"}
    schluessel = set()
    for knoten in ast.walk(_baum(os.path.join(ordner, "multi_symbol_optimise.py"))):
        if isinstance(knoten, ast.Dict):
            for s in knoten.keys:
                if isinstance(s, ast.Constant) and isinstance(s.value, str):
                    schluessel.add(s.value)
    return schluessel & bekannt


def teste_alle_dimensionen_durchgereicht():
    """Der eigentliche Schutz gegen eine Wiederholung.

    Der Fix an einer Zeile behebt den heutigen Fall. Wird morgen eine neue
    Dimension ins Suchraster aufgenommen und beim OOS-Aufruf vergessen,
    entsteht derselbe Fehler erneut - lautlos. Diese Pruefung vergleicht
    deshalb, was der Optimierer LIEFERN kann, mit dem, was die
    OOS-Simulation ABHOLT."""
    print("\nE) Jede gesuchte Dimension wird auch weitergereicht")

    for bot, ordner in (("elliott_wave", KRYPTO), ("elliott_wave_stocks", AKTIEN)):
        oos = os.path.join(ordner, "oos_equity_simulation.py")
        if not os.path.exists(oos):
            continue
        gesucht = optimierer_dimensionen(ordner)
        aufrufe = aufruf_argumente(oos, "collect_all_trades")
        durchgereicht = set(aufrufe[0]) if aufrufe else set()
        fehlend = gesucht - durchgereicht
        check(f"{bot}: OOS reicht alle {len(gesucht)} gesuchten Dimensionen durch",
              not fehlend,
              f"fehlt: {sorted(fehlend)}" if fehlend
              else f"{sorted(gesucht)}")


def main():
    print("Selbsttests: Take-Profit-Uebergabe in der OOS-Validierung")
    teste_uebergabe()
    teste_none_falle()
    teste_wirkung()
    teste_krypto_nicht_betroffen()
    teste_alle_dimensionen_durchgereicht()

    print(f"\n{_bestanden}/{_bestanden + len(_fehler)} Pruefungen bestanden.")
    for name in _fehler:
        print(f"FEHLGESCHLAGEN: {name}")
    sys.exit(1 if _fehler else 0)


if __name__ == "__main__":
    main()
