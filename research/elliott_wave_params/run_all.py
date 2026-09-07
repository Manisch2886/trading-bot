"""
Alles nacheinander - Parameter-Neubestimmung, beide Bots
====================================================================
Startet je Bot einen eigenen Prozess je Schritt (beide Bots haben
gleichnamige, inhaltlich verschiedene Module - siehe botenv.py) und
bricht beim ersten Fehlschlag ab.

Reihenfolge je Bot:
    test_params.py    Selbsttests des Rechenkerns
    search.py         Rastersuche auf gesamt / In-Sample / Out-of-Sample
    walkforward.py    Walk-Forward: Kandidaten und Verfahren
    stability.py      Nachbarschaft, feine Zigzag-Verschiebung, Reihenfolge
    symbols.py        Beitragsverteilung und ehrlicher Symbol-Auswahltest
    benchmark.py      Buy-and-Hold je Fenster

Laufzeit: rund 40-60 Minuten (der Krypto-Bot dominiert - 18 Symbole mit
je ~44.000 Stundenkerzen, und der feinste Zigzag erzeugt die meisten
Wellenkandidaten).

Nutzung:  python3 run_all.py [bot ...]
"""

import os
import subprocess
import sys
import time

DIR = os.path.dirname(os.path.abspath(__file__))
BOTS = ("elliott_wave", "elliott_wave_stocks")
STEPS = ("test_params.py", "search.py", "walkforward.py", "stability.py",
         "symbols.py", "benchmark.py", "summary.py")


def run(script, bot):
    print(f"\n{'=' * 74}\n{script}  {bot}\n{'=' * 74}", flush=True)
    t0 = time.time()
    res = subprocess.run([sys.executable, os.path.join(DIR, script), bot],
                          cwd=DIR, text=True)
    secs = round(time.time() - t0, 1)
    if res.returncode != 0:
        print(f"\nABBRUCH: {script} {bot} endete mit Code {res.returncode} nach {secs} s")
        sys.exit(res.returncode)
    print(f"-- {script} {bot}: {secs} s", flush=True)


if __name__ == "__main__":
    sys.path.insert(0, DIR)
    import botenv
    botenv.print_hinweis()
    bots = sys.argv[1:] or list(BOTS)
    t0 = time.time()
    for bot in bots:
        for step in STEPS:
            run(step, bot)
    print(f"\nAlle Schritte erfolgreich ({round(time.time() - t0, 1)} s).")
    botenv.print_hinweis()
