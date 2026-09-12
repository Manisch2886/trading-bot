"""
Alles nacheinander - ein Prozess je Bot und Schritt
====================================================================
Aufruf:  python3 run_all.py [<bot> ...]

Ohne Argumente laeuft alles fuer alle neun Bots, rund 2,5 Stunden. Der
weitaus groesste Teil davon geht auf `elliott_wave`: dessen Zigzag laeuft
auf Stundenkerzen (18 Symbole x rund 44 000 Balken), und bei
`deviation_pct = 2 %` dauert eine einzige Rasterkombination ueber drei
Minuten.

WARUM EIN PROZESS JE BOT: die neun Bots haben gleichnamige, inhaltlich
verschiedene Module (`backtest_elliott.py`, `multi_symbol_optimise.py`,
...). Ein Import zweier Bots im selben Prozess wuerde ueber sys.modules
still den falschen laden - und das Ergebnis waere falsch, ohne
Fehlermeldung. Deshalb wird jeder Schritt als eigener Prozess gestartet.

Dieses Skript aendert nichts am Bot-Code und an keiner Bot-Ergebnisdatei;
geschrieben wird ausschliesslich unter results/ dieses Ordners.
"""

import os
import subprocess
import sys
import time

import botenv

DIR = os.path.dirname(os.path.abspath(__file__))

# (Skript, Bot, zusaetzliche Argumente)
def schritte(bots):
    for bot in bots:
        yield ("test_drawdown.py", bot, [])
        yield ("analyse.py", bot, [])
        yield ("einzelsymbol.py", bot, [])
        yield ("historie.py", bot, [])
        yield ("kapitalkurve.py", bot, [])
        # In-Sample nur, wo der Bot sein Fenster ueber einen Trade-Filter
        # bildet - die drei aelteren schneiden die Kursreihe, dort waere
        # die Ableitung falsch (siehe adapters.py, `unterstuetzt_is`).
        if bot not in ("elliott_wave", "elliott_wave_stocks", "t3_supertrend"):
            yield ("analyse.py", bot, ["--fenster", "is"])
        # Der historische Stand von t3_supertrend, vor dem Regimefilter -
        # der Stand, aus dem seine gespeicherte Ergebnisdatei stammt.
        if bot == "t3_supertrend":
            yield ("analyse.py", bot, ["--ohne-regimefilter"])
            yield ("historie.py", bot, ["--ohne-regimefilter"])


def main():
    bots = [a for a in sys.argv[1:] if not a.startswith("-")] or list(botenv.BOTS)
    for b in bots:
        if b not in botenv.BOTS:
            raise SystemExit(f"Unbekannter Bot: {b}")

    botenv.print_hinweis()
    alle = list(schritte(bots))
    t0 = time.time()
    fehler = []
    for i, (skript, bot, extra) in enumerate(alle, 1):
        titel = f"{skript} {bot} {' '.join(extra)}".strip()
        print(f"\n{'=' * 70}\n[{i}/{len(alle)}] {titel}\n{'=' * 70}", flush=True)
        t1 = time.time()
        rc = subprocess.call([sys.executable, os.path.join(DIR, skript), bot] + extra,
                             cwd=DIR)
        print(f"-> {titel}: Rueckgabewert {rc}, {round(time.time() - t1, 1)} s", flush=True)
        if rc != 0:
            fehler.append(f"{titel} (Rueckgabewert {rc})")

    # Die Zusammenfassung zuletzt, wenn alle Ergebnisdateien stehen.
    print(f"\n{'=' * 70}\nuebersicht.py\n{'=' * 70}", flush=True)
    subprocess.call([sys.executable, os.path.join(DIR, "uebersicht.py")], cwd=DIR)

    print(f"\nGesamtdauer: {round((time.time() - t0) / 60, 1)} Minuten")
    if fehler:
        print(f"\n{len(fehler)} Schritte mit Fehler:")
        for f in fehler:
            print(f"  {f}")
    else:
        print("Alle Schritte ohne Fehler.")
    botenv.print_hinweis()
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
