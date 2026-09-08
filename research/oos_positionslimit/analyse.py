"""
Wie viele Trades betrifft das Positionslimit wirklich?
================================================================================
`simulate_portfolio()` liefert nur EINE Zahl uebersprungener Trades und sagt
nicht, woran ein Trade gescheitert ist:

    if max_concurrent_positions is not None and len(open_positions) >= max_concurrent_positions:
        skipped_trades.append(idx); continue          # <- Positionslimit
    ...
    if allocation > free_capital:
        skipped_trades.append(idx); continue          # <- freies Kapital

Genau diese Unterscheidung ist aber die Frage der Aufgabe. Deshalb wird die
Ereignisschleife hier nachgebildet - und zwar nachweislich TREU:

    Das Nachbild muss fuer BEIDE Konfigurationen (ohne Limit / mit Limit 8)
    exakt dieselben Zahlen liefern wie die echte Funktion. Stimmt auch nur
    eine nicht ueberein, bricht das Skript ab, statt eine schoen aussehende,
    aber unbelegte Aufschluesselung zu drucken.

Damit ist die Aufschluesselung so vertrauenswuerdig wie die Uebereinstimmung,
die sie vorher beweist.

VERWANDT, aber nicht dasselbe: der Bot hat mit
experiment_concurrency_stats.simulate_portfolio_instrumented() bereits eine
instrumentierte Kopie derselben Schleife. Sie protokolliert die Anzahl
gleichzeitig offener Positionen und die Kapitalauslastung - aber NICHT, aus
welchem der beiden Gruende ein Trade uebersprungen wurde. Genau das ergaenzt
dieses Skript; die Zaehlung der gleichzeitig offenen Positionen laeuft hier
nur als Nebenprodukt mit.

Nutzung:  python3 analyse.py
"""

import json
import os
import sys

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, os.path.join(_REPO_ROOT, "strategies", "elliott_wave_stocks"))
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))
sys.path.append(os.path.join(_DIR, "stubs"))

RESULTS_DIR = os.path.join(_DIR, "results")


def nachbild(trades: pd.DataFrame, startkapital: float, allokation: float,
              max_positionen=None) -> dict:
    """Zeile fuer Zeile dieselbe Logik wie equity_simulation.simulate_portfolio,
    nur mit getrennt gezaehlten Uebersprung-Gruenden."""
    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx))
        events.append((trade["exit_time"], "exit", idx))
    events.sort(key=lambda e: (e[0], e[1] != "exit"))

    kapital = startkapital
    offen = {}
    wegen_limit, wegen_kapital, ausgefuehrt = [], [], []
    hoechststand = 0

    for zeit, art, idx in events:
        trade = trades.loc[idx]
        if art == "entry":
            if max_positionen is not None and len(offen) >= max_positionen:
                wegen_limit.append(idx)
                continue
            gebunden = sum(offen.values())
            frei = kapital - gebunden
            betrag = kapital * allokation
            if betrag > frei:
                wegen_kapital.append(idx)
                continue
            offen[idx] = betrag
            ausgefuehrt.append(idx)
            hoechststand = max(hoechststand, len(offen))
        else:
            if idx not in offen:
                continue
            betrag = offen.pop(idx)
            kapital += betrag * (trade["pnl_pct"] / 100)

    return {
        "endkapital": round(kapital, 2),
        "ausgefuehrt": len(ausgefuehrt),
        "uebersprungen": len(wegen_limit) + len(wegen_kapital),
        "wegen_limit": len(wegen_limit),
        "wegen_kapital": len(wegen_kapital),
        "hoechststand_gleichzeitig": hoechststand,
    }


def pruefe_treue(trades, startkapital, allokation, echte_zahlen: dict,
                  max_positionen, bezeichnung: str) -> bool:
    """Das Nachbild gegen die echten Zahlen halten."""
    n = nachbild(trades, startkapital, allokation, max_positionen)
    stimmt = (n["ausgefuehrt"] == echte_zahlen["ausgefuehrt"]
              and n["uebersprungen"] == echte_zahlen["uebersprungen"]
              and abs(n["endkapital"] - echte_zahlen["endkapital"]) < 0.01)
    zeichen = "OK " if stimmt else "ABWEICHUNG"
    print(f"  [{zeichen}] {bezeichnung}: "
          f"ausgefuehrt {n['ausgefuehrt']}/{echte_zahlen['ausgefuehrt']}, "
          f"uebersprungen {n['uebersprungen']}/{echte_zahlen['uebersprungen']}, "
          f"Endkapital {n['endkapital']}/{echte_zahlen['endkapital']}")
    return stimmt


def lade(phase: str):
    with open(os.path.join(RESULTS_DIR, f"oos_{phase}.json"), encoding="utf-8") as f:
        daten = json.load(f)
    trades = pd.read_csv(os.path.join(RESULTS_DIR, f"trades_{phase}.csv"),
                          parse_dates=["entry_time", "exit_time"])
    return daten, trades


def main():
    vorher, trades_v = lade("vorher")
    nachher, trades_n = lade("nachher")

    print("Treue-Pruefung des Nachbilds (muss die echten Zahlen exakt treffen)")
    kv, kn = vorher["kennzahlen"], nachher["kennzahlen"]
    startkapital = vorher["mitschnitt"]["startkapital"]
    allokation = vorher["mitschnitt"]["allokation"]

    ok1 = pruefe_treue(trades_v, startkapital, allokation, kv, None,
                        "ohne Limit (Zustand vorher)")
    ok2 = pruefe_treue(trades_n, startkapital, allokation, kn,
                        nachher["mitschnitt"]["limit_uebergeben"],
                        f"mit Limit {nachher['mitschnitt']['limit_uebergeben']} (Zustand nachher)")
    if not (ok1 and ok2):
        print("\nDas Nachbild trifft die echten Zahlen NICHT - die "
              "Aufschluesselung waere nicht belastbar. Abbruch.")
        sys.exit(1)

    print("\nDieselben Trades vorher und nachher?")
    gleich = vorher["trades_hash"] == nachher["trades_hash"]
    print(f"  [{'OK ' if gleich else 'ABWEICHUNG'}] Trades-Hash "
          f"{vorher['trades_hash'][:16]} vs. {nachher['trades_hash'][:16]}")
    if not gleich:
        print("  Die Aenderung hat die Trade-Erzeugung beeinflusst - das darf "
              "sie nicht.")
        sys.exit(1)

    ohne = nachbild(trades_v, startkapital, allokation, None)
    mit = nachbild(trades_n, startkapital, allokation,
                    nachher["mitschnitt"]["limit_uebergeben"])

    print("\nAufschluesselung der uebersprungenen Trades")
    kopf = f"{'':<28} {'ohne Limit':>12} {'mit Limit 8':>12}"
    print(kopf); print("-" * len(kopf))
    for feld, name in (("ausgefuehrt", "ausgefuehrt"),
                        ("uebersprungen", "uebersprungen gesamt"),
                        ("wegen_limit", "davon wegen Limit"),
                        ("wegen_kapital", "davon wegen Kapital"),
                        ("hoechststand_gleichzeitig", "max. gleichzeitig offen")):
        print(f"{name:<28} {ohne[feld]:>12} {mit[feld]:>12}")

    gesamt = len(trades_v)
    print(f"\nvon insgesamt {gesamt} Trades")
    print(f"  ohne Limit betroffen: {ohne['uebersprungen']} "
          f"({ohne['uebersprungen'] / gesamt * 100:.1f}%) - alle wegen Kapital")
    print(f"  mit Limit betroffen : {mit['uebersprungen']} "
          f"({mit['uebersprungen'] / gesamt * 100:.1f}%), davon "
          f"{mit['wegen_limit']} wegen des Limits")

    ergebnis = {"ohne_limit": ohne, "mit_limit": mit, "trades_gesamt": gesamt,
                "kennzahlen_vorher": kv, "kennzahlen_nachher": kn}
    ziel = os.path.join(RESULTS_DIR, "analyse.json")
    with open(ziel, "w", encoding="utf-8") as f:
        json.dump(ergebnis, f, indent=2, ensure_ascii=False)
    print(f"\ngeschrieben: {ziel}")


if __name__ == "__main__":
    main()
