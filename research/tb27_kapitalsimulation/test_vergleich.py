#!/usr/bin/env python3
"""Selbsttest fuer `vergleich.py` - der Waechter muss auch ROT werden koennen.

Warum es diesen Test gibt
-------------------------
`vergleich.py --pruefen` soll kuenftig melden, wenn eine der neun
`equity_simulation.py` still auseinanderlaeuft. Eine Pruefung, die immer gruen
ist, leistet das nicht - und man sieht ihr das nicht an (Methodik-Prinzip 12
des Uebergabeprotokolls: eine gruene Pruefung muss auch rot werden koennen).

Dieser Test legt dem Waechter deshalb absichtlich verfaelschte Kopien der neun
Dateien vor und verlangt, dass er sie erkennt - und dass er bei reinen
Kommentar- und Docstring-Aenderungen gruen bleibt, denn sonst waere er im
Alltag wertlos.

Der Test fasst nichts an: die Kopien liegen in einem temporaeren Ordner, den
er selbst wieder loescht, und `vergleich.py` schreibt ohnehin nichts. Er
braucht kein pandas, keine Kursdaten und keine Netzverbindung.

Aufruf:

    python3 research/tb27_kapitalsimulation/test_vergleich.py

Rueckgabewert 0, wenn alle Pruefungen bestehen, sonst 1.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))
_ECHTE_STRATEGIEN = os.path.join(_WURZEL, "strategies")
_WERKZEUG = os.path.join(_HIER, "vergleich.py")

DATEI = "equity_simulation.py"

bestanden = 0
gescheitert = []


def pruefe(was, bedingung, hinweis=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print(f"  OK    {was}")
    else:
        gescheitert.append(was)
        print(f"  FEHLT {was}" + (f"   [{hinweis}]" if hinweis else ""))


def laufen(strategien, *argumente):
    """`vergleich.py` gegen den angegebenen Strategie-Ordner laufen lassen."""
    umgebung = dict(os.environ, TB27_STRATEGIEN=strategien)
    fertig = subprocess.run([sys.executable, _WERKZEUG, *argumente],
                            capture_output=True, text=True, env=umgebung)
    return fertig.returncode, fertig.stdout + fertig.stderr


def kopie(ziel):
    """Eine Kopie der neun echten Dateien - nur die, mehr braucht es nicht."""
    for bot in sorted(os.listdir(_ECHTE_STRATEGIEN)):
        quelle = os.path.join(_ECHTE_STRATEGIEN, bot, DATEI)
        if not os.path.isfile(quelle):
            continue
        os.makedirs(os.path.join(ziel, bot), exist_ok=True)
        shutil.copy2(quelle, os.path.join(ziel, bot, DATEI))
    return sorted(os.listdir(ziel))


def lies(ordner, bot):
    with open(os.path.join(ordner, bot, DATEI), encoding="utf-8") as f:
        return f.read()


def schreib(ordner, bot, text):
    with open(os.path.join(ordner, bot, DATEI), "w", encoding="utf-8") as f:
        f.write(text)


def main():
    print(__doc__.strip().split("\n")[0])
    print()

    # ---------------------------------------------------------------
    print("1. Der echte Bestand")
    print("-" * 70)
    kode, ausgabe = laufen(_ECHTE_STRATEGIEN, "--pruefen")
    pruefe("die neun echten Dateien entsprechen der festgehaltenen Erwartung",
           kode == 0, ausgabe.strip()[:300])
    pruefe("die Meldung nennt den Stand", "TB-27" in ausgabe, ausgabe[:120])

    kode, uebersicht = laufen(_ECHTE_STRATEGIEN)
    pruefe("die Uebersicht laeuft durch", kode == 0)
    pruefe("sie findet neun Dateien", uebersicht.startswith("9x "), uebersicht[:60])
    pruefe("calculate_max_drawdown steht als EINE Gruppe da",
           re.search(r"calculate_max_drawdown\s+\(1 Gruppe\)", uebersicht) is not None)
    pruefe("simulate_portfolio steht als ZWEI Gruppen da",
           re.search(r"simulate_portfolio\s+\(2 Gruppen\)", uebersicht) is not None)

    with tempfile.TemporaryDirectory() as basis:
        # -----------------------------------------------------------
        print("\n2. Eine unveraenderte Kopie bleibt gruen")
        print("-" * 70)
        rein = os.path.join(basis, "rein")
        os.makedirs(rein)
        bots = kopie(rein)
        pruefe("die Kopie enthaelt neun Bots", len(bots) == 9, str(len(bots)))
        kode, ausgabe = laufen(rein, "--pruefen")
        pruefe("die unveraenderte Kopie ist gruen", kode == 0, ausgabe.strip()[:200])

        # -----------------------------------------------------------
        print("\n3. Eine stille Divergenz wird ROT")
        print("-" * 70)
        # Der Fall, um den es geht: das Drawdown-Mass laeuft in EINEM Bot
        # auseinander - dieselbe Sache, anders gerechnet. Genau das, was die
        # Kurven-Erneuerung (PR #86) an den abgelegten Kurven gefunden hat.
        divergent = os.path.join(basis, "divergent")
        os.makedirs(divergent)
        kopie(divergent)
        text = lies(divergent, "turtle_soup_crypto")
        verfaelscht = text.replace(
            "    running_max = capital_series.cummax()\n",
            "    running_max = capital_series.expanding().max()\n", 1)
        pruefe("die Verfaelschung greift ueberhaupt", verfaelscht != text)
        schreib(divergent, "turtle_soup_crypto", verfaelscht)
        kode, ausgabe = laufen(divergent, "--pruefen")
        pruefe("der Waechter meldet ROT", kode == 1, ausgabe.strip()[:200])
        pruefe("er nennt die betroffene Funktion",
               "calculate_max_drawdown" in ausgabe, ausgabe[:200])
        pruefe("er nennt den betroffenen Bot",
               "turtle_soup_crypto" in ausgabe, ausgabe[:300])

        # -----------------------------------------------------------
        print("\n4. Kommentar und Docstring allein sind KEINE Divergenz")
        print("-" * 70)
        # Waere das anders, meldete der Waechter bei jeder Doku-Pflege rot
        # und wuerde binnen weniger Wochen ignoriert.
        harmlos = os.path.join(basis, "harmlos")
        os.makedirs(harmlos)
        kopie(harmlos)
        text = lies(harmlos, "rsi2_crypto")
        mit_kommentar = text.replace(
            "    if equity_df.empty:\n        return 0.0\n",
            "    # Ein neuer, erklaerender Kommentar IM Rumpf des Masses.\n"
            "    if equity_df.empty:\n        return 0.0\n", 1)
        pruefe("die Kommentar-Aenderung greift ueberhaupt", mit_kommentar != text)
        schreib(harmlos, "rsi2_crypto", mit_kommentar)
        kode, ausgabe = laufen(harmlos, "--pruefen")
        pruefe("ein neuer Kommentar laesst den Waechter gruen",
               kode == 0, ausgabe.strip()[:300])
        kode, uebersicht = laufen(harmlos)
        pruefe("die Uebersicht stuft die Gruppe von `zeichengleich` auf "
               "`ohne Kommentar` zurueck (Stufe 2)",
               "ohne Kommentar" in uebersicht, "keine Stufe zurueckgesetzt")

        # Ein geaenderter Docstring faellt erst auf Stufe 3 weg - deshalb
        # muss die Gruppe hier bis `sachlich gleich` durchfallen und der
        # Waechter trotzdem gruen bleiben.
        text = lies(harmlos, "turtle_soup_crypto")
        anders_beschrieben = text.replace(
            '    """Kapitalsimulation mit Zuteilungskaskade.',
            '    """Kapitalsimulation mit Zuteilungskaskade (neu formuliert).', 1)
        pruefe("die Docstring-Aenderung greift ueberhaupt", anders_beschrieben != text)
        schreib(harmlos, "turtle_soup_crypto", anders_beschrieben)
        kode, ausgabe = laufen(harmlos, "--pruefen")
        pruefe("ein geaenderter Docstring laesst den Waechter gruen",
               kode == 0, ausgabe.strip()[:300])
        kode, uebersicht = laufen(harmlos)
        pruefe("die Uebersicht faellt dafuer bis `sachlich gleich` durch (Stufe 3)",
               "sachlich gleich" in uebersicht, "Stufe 3 nicht erreicht")

        # -----------------------------------------------------------
        print("\n5. Eine neue oder verschwundene Funktion faellt auf")
        print("-" * 70)
        neu = os.path.join(basis, "neu")
        os.makedirs(neu)
        kopie(neu)
        schreib(neu, "t3_supertrend",
                lies(neu, "t3_supertrend") + "\n\ndef neue_kennzahl(x):\n    return x\n")
        kode, ausgabe = laufen(neu, "--pruefen")
        pruefe("eine neu hinzugekommene Funktion wird gemeldet",
               kode == 1 and "neue_kennzahl" in ausgabe, ausgabe[:200])

        weg = os.path.join(basis, "weg")
        os.makedirs(weg)
        kopie(weg)
        text = lies(weg, "volatility_breakout_crypto")
        anfang = text.index("def apply_btc_regime_filter")
        ende = text.index("# ---", anfang)
        schreib(weg, "volatility_breakout_crypto", text[:anfang] + text[ende:])
        kode, ausgabe = laufen(weg, "--pruefen")
        pruefe("eine verschwundene Funktion wird gemeldet",
               kode == 1 and "apply_btc_regime_filter" in ausgabe, ausgabe[:200])

        # -----------------------------------------------------------
        print("\n6. Rechnen und Reden werden auseinandergehalten")
        print("-" * 70)
        # Stufe 4: wird nur der Ausgabetext geaendert, muss die Uebersicht
        # sagen koennen, dass die Rechnung dieselbe geblieben ist.
        reden = os.path.join(basis, "reden")
        os.makedirs(reden)
        kopie(reden)
        text = lies(reden, "turtle_soup_stocks")
        anders = text.replace('print("=" * 55)', 'print("=" * 60)')
        pruefe("die Ausgabe-Aenderung greift ueberhaupt", anders != text)
        schreib(reden, "turtle_soup_stocks", anders)
        kode, uebersicht = laufen(reden)
        pruefe("die Uebersicht weist aus, dass es ohne die Ausgabe weniger "
               "Gruppen waeren",
               "ohne die Bildschirmausgabe" in uebersicht,
               "kein Hinweis auf Stufe 4")
        kode, ausgabe = laufen(reden, "--pruefen")
        pruefe("eine reine Ausgabe-Aenderung meldet der Waechter trotzdem - "
               "was auf dem Bildschirm steht, war hier schon einmal falsch",
               kode == 1, ausgabe.strip()[:200])

    # ---------------------------------------------------------------
    print("\n" + "=" * 70)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
