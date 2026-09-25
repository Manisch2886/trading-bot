"""TB-109 B1 - baut an den 10 Stellen `if trades.empty: print(...); exit()` der neun
strategies/*/equity_simulation.py die Modus-Abfrage ein (Bauart TB-105 Block C, 14 Stellen).

Gesucht wird der Text (nicht die Zeilennummer):

    if trades.empty:
        print("<Meldung>")
        exit()

und ersetzt durch denselben Text mit der Abfrage VOR dem bestehenden print/exit. Ohne Modus
bleibt der Ablauf zeichengleich (print, exit()). Erwartet werden genau 10 Stellen in 9 Dateien;
jede andere Zahl bricht ab, bevor eine Datei geschrieben wird.

Aufruf aus der Repo-Wurzel:  python3 docs/belege/TB-109/b1_einbau.py [--probe]
  --probe  zaehlt nur, schreibt nichts.
"""
import glob
import re
import sys

MUSTER = re.compile(r'(?m)^    if trades\.empty:\n        print\("([^"\n]*)"\)\n        exit\(\)\n')

EINBAU = '''    if trades.empty:
        # TB-109 Block B (Fable 25e (2)): null Trades ist ein Wert (5.1 Nr. 8,
        # 1c) - unter dem Selektionsmodus endet ein exit() ohne geschriebenes
        # Ergebnis mit Rueckgabewert 2, nicht mit 0. Ohne Modus wie bisher.
        import paths
        if paths.selektionsmodus() is not None:
            sys.stderr.write("{m}" + "\\n")
            raise SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)
        print("{m}")
        exit()
'''

dateien = sorted(glob.glob("strategies/*/equity_simulation.py"))
treffer = {d: MUSTER.findall(open(d, encoding="utf-8").read()) for d in dateien}
zahl = sum(len(v) for v in treffer.values())
for d, v in treffer.items():
    print("%-50s %d  %s" % (d, len(v), v))
print("Stellen: %d in %d Dateien" % (zahl, sum(1 for v in treffer.values() if v)))
if zahl != 10 or sum(1 for v in treffer.values() if v) != 9:
    raise SystemExit("ABBRUCH: erwartet 10 Stellen in 9 Dateien")
if "--probe" in sys.argv:
    raise SystemExit(0)
for d in dateien:
    text = open(d, encoding="utf-8").read()
    if "import sys" not in text:
        raise SystemExit("ABBRUCH: %s importiert sys nicht" % d)
    neu = MUSTER.sub(lambda m: EINBAU.format(m=m.group(1)), text)
    with open(d, "w", encoding="utf-8") as f:
        f.write(neu)
print("eingebaut")
