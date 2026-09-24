#!/usr/bin/env python3
"""TB-97 Block A2 - beisst jede Mutationsprobe? Gemessen, nicht geraten.

Aufruf (Repo-Wurzel):
    trading-env/bin/python3 -W ignore docs/belege/TB-97/a2_beissen.py <ausgabe.txt>

Fuer jede Mutation k in Teil H laeuft `teil_h()` des Tests einmal, wobei GENAU
diese eine Mutation weggelassen wird: `_ersetze` prueft weiter, dass die Stelle
existiert (sonst AssertionError wie im Test), schreibt aber nicht. Die uebrigen
Mutationen bleiben - H6 braucht die Mutation von H5 als Voraussetzung.
Erwartung nach 40.7: die zugehoerige Probe SCHEITERT ("beisst"). Besteht sie
trotzdem, beisst sie nicht.

Dazu H3 mit leerer Menge (TB-95-Gegenprobe) und F4 (keine Code-Mutation; die
"Mutation" ist die Falte ohne Trade - weggelassen = leere Menge).
Aendert keine Datei im Repo; alles in Wegwerf-Verzeichnissen.
"""
import datetime as dt
import os
import subprocess
import sys
import tempfile
import time

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.abspath(os.path.join(HIER, "..", "..", ".."))
VR = os.path.join(WURZEL, "research", "vorregistrierung")
sys.path.insert(0, VR)

import test_vorregistrierung as t  # noqa: E402

AUS = sys.argv[1]
_orig_ersetze = t._ersetze
# Die Mutationen in Teil H in Aufrufreihenfolge (Datei, Anfang des alten Textes)
MUTATIONEN = [
    ("H1", "registerdaten.py", "SPITZEN_SCHWELLE = 0.50"),
    ("H2", "auswertung.py", "float(np.mean([s] + nachbar_werte))"),
    ("H3", "auswertung.py", 'df["netto_sharpe"] = np.where('),
    ("H4", "registerdaten.py", "DD_RELATIVER_FAKTOR = 1.25"),
    ("H5", "registerdaten.py", '"Ein Stop enger als ein halbes Tages-Sigma'),
    ("H6", "pruefe_grenzsaetze.py", 'treffer = zahlen_im_satz(g.get("satz")) & alle_live'),
    ("H7", "registerdaten.py", '        "stufen": 4,\n        "unten": _grenze('),
]


def schreib(z):
    with open(AUS, "a", encoding="utf-8") as f:
        f.write(z)


def lauf_ohne(ziel):
    """teil_h mit weggelassener Mutation `ziel`; liefert (Liste gescheitert, getroffen?)."""
    getroffen = []

    def ersetze(pfad, alt, neu):
        for name, datei, anfang in MUTATIONEN:
            if name == ziel and os.path.basename(pfad) == datei and alt.startswith(anfang):
                with open(pfad, encoding="utf-8") as f:
                    if alt not in f.read():
                        raise AssertionError(f"Mutationsstelle nicht gefunden: {alt!r}")
                getroffen.append(name)
                return                                   # weggelassen
        return _orig_ersetze(pfad, alt, neu)

    t._ersetze = ersetze
    t.bestanden, t.gescheitert[:] = 0, []
    try:
        t.teil_h()
    finally:
        t._ersetze = _orig_ersetze
    return list(t.gescheitert), t.bestanden, getroffen


open(AUS, "w").close()
kopf = subprocess.run(["git", "-C", WURZEL, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
schreib(f"# TB-97 A2 - beisst jede Mutationsprobe heute? HEAD {kopf}, "
        f"{dt.datetime.now().astimezone():%Y-%m-%d %H:%M:%S %z}\n"
        f"# Werkzeug: docs/belege/TB-97/a2_beissen.py, Python {sys.version.split()[0]}; "
        f"test_vorregistrierung.py unveraendert (Mutation per Ersatz von _ersetze weggelassen)\n\n")

t0 = time.time()
t.bestanden, t.gescheitert[:] = 0, []
t.teil_h()
schreib(f"Grundlauf teil_h (alle Mutationen): {t.bestanden} bestanden, gescheitert {t.gescheitert}  [{time.time() - t0:.0f} s]\n\n")

for name, datei, _ in MUTATIONEN:
    s = time.time()
    gesch, best, getroffen = lauf_ohne(name)
    eigen = [g for g in gesch if g.startswith(name + ":")]
    urteil = "BEISST" if eigen else "BEISST NICHT"
    if not getroffen:
        urteil = "NICHT MESSBAR (Mutation nicht getroffen)"
    schreib(f"{name} ohne ihre Mutation ({datei}): {urteil}\n"
            f"   gescheitert: {gesch}\n   bestanden {best}, Mutation weggelassen: {getroffen}  [{time.time() - s:.0f} s]\n\n")

# H6 zusaetzlich: auch die Voraussetzung (Mutation von H5) weggelassen
s = time.time()
getroffen = []


def ersetze_h56(pfad, alt, neu):
    for name, datei, anfang in MUTATIONEN:
        if name in ("H5", "H6") and os.path.basename(pfad) == datei and alt.startswith(anfang):
            getroffen.append(name)
            return
    return _orig_ersetze(pfad, alt, neu)


t._ersetze = ersetze_h56
t.bestanden, t.gescheitert[:] = 0, []
t.teil_h()
t._ersetze = _orig_ersetze
schreib(f"Zusatz: H5 UND H6 ohne Mutation: gescheitert {t.gescheitert}\n"
        f"   -> H6 {'besteht' if not any(g.startswith('H6:') for g in t.gescheitert) else 'scheitert'} ohne jede Mutation "
        f"(prueft rc 0; ohne den Live-Wert aus H5 ist rc 0 trivial) - H6 traegt nur zusammen mit H5  [{time.time() - s:.0f} s]\n\n")

# H3 mit leerer Menge (TB-95-Gegenprobe) - ueber den Weg des Tests
s = time.time()
mess, plan = t._mess(), t._plan()
vorher, nachher = t._h3_lauf(mess, plan, set())
ok = (vorher.returncode == 0 and nachher.returncode == 0
      and t._sharpezeile(vorher.stdout) != t._sharpezeile(nachher.stdout))
schreib(f"H3 mit leerer Menge (ohne = {{}}): Bedingung {ok} -> {'BEISST' if not ok else 'BEISST NICHT'}\n"
        f"   {t._sharpezeile(vorher.stdout)!r} / {t._sharpezeile(nachher.stdout)!r}  [{time.time() - s:.0f} s]\n\n")

# F4 heute - "Mutation" weggelassen = keine Falte ohne Trade
s = time.time()
with tempfile.TemporaryDirectory() as d:
    e = t.lauf(d, trades_fn=lambda w, i, f, a: 40, sharpe_fn=lambda w, i, f, a: 0.10)
falten = e["beurteilung"]["falten_sharpe"]
werte = list(falten.values())
cond = float(np.median(werte)) <= float(np.median([v for k, v in falten.items() if k != "2022"]))
schreib(f"F4 (keine Code-Mutation) ohne Falte ohne Trade: Bedingung (<=) {cond} -> "
        f"{'BEISST NICHT' if cond else 'BEISST'}  [{time.time() - s:.0f} s]\n")
schreib(f"\nGesamtzeit {time.time() - t0:.0f} s\n")
