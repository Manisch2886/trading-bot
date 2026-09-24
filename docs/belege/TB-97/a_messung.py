#!/usr/bin/env python3
"""TB-97 Block A3/A4 - rein lesende Messung zu F4 und den vier Jahresliteralen.

Aufruf (Repo-Wurzel):  trading-env/bin/python3 -W ignore docs/belege/TB-97/a_messung.py
Schreibt a3_f4.txt und a4_literale.txt neben sich. Aendert keine Datei im Repo;
die Laeufe gehen wie im Test in Wegwerf-Verzeichnisse.
"""
import datetime as dt
import os
import subprocess
import sys
import tempfile

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.abspath(os.path.join(HIER, "..", "..", ".."))
VR = os.path.join(WURZEL, "research", "vorregistrierung")
sys.path.insert(0, VR)

import test_vorregistrierung as t  # noqa: E402  (main() laeuft nicht beim Import)
import benchmark as bm  # noqa: E402
import registerdaten as rd  # noqa: E402

KOPF = (f"# TB-97 Block A - HEAD {subprocess.run(['git', '-C', WURZEL, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()}"
        f", {dt.datetime.now().astimezone():%Y-%m-%d %H:%M:%S %z}\n"
        f"# Werkzeug: docs/belege/TB-97/a_messung.py, Python {sys.version.split()[0]}\n")

plan = t._plan()
tab = t._tabellen()
BOT = t.BOT


def f_lauf(ohne):
    """Teil F am Ablauf, mit einer Menge Falten ohne Trade."""
    with tempfile.TemporaryDirectory() as d:
        e = t.lauf(d, trades_fn=lambda w, i, f, a: 0 if f in ohne else 40,
                   sharpe_fn=lambda w, i, f, a: 9.0 if f in ohne else 0.10)
    return e


# --------------------------------------------------------------------------- A3
z = [KOPF, f"# A3 - F4 ausgemessen. BOT = {BOT}\n\n"]
sel = t._selektionsfalten(plan[BOT])
z.append(f"Selektionsfalten ({len(sel)}): {sel}\n")
z.append(f"Bestaetigung: {[f['name'] for f in plan[BOT]['falten'] if f['rolle'] == 'bestaetigung']}\n\n")
z.append("Code (Stand HEAD, test_vorregistrierung.py Teil F):\n"
         "  ohne = \"2022\"   (ein Literal, eine Falte)\n"
         "  F4 Text:  \"der Median mit der Null liegt unter dem Median ohne sie\"\n"
         "  F4 Code:  median(werte) <= median([v for k, v in falten.items() if k != ohne])\n"
         "  Vergleichszeichen <=  -  der Text sagt \"unter\" (<)\n\n")
e = f_lauf({"2022"})
falten = e["beurteilung"]["falten_sharpe"]
mit = float(np.median(list(falten.values())))
ohne_n = float(np.median([v for k, v in falten.items() if k != "2022"]))
z.append(f"Heutiger Lauf (ohne = {{'2022'}}): falten_sharpe = {falten}\n"
         f"  Falten auf null gesetzt: {sum(1 for v in falten.values() if v == 0.0)} von {len(falten)}\n"
         f"  Median mit der Null {mit:.4f}, ohne sie {ohne_n:.4f}\n"
         f"  <= : {mit <= ohne_n}   < : {mit < ohne_n}   -> F4 heute {'bestanden' if mit <= ohne_n else 'GESCHEITERT'}, "
         f"mit < waere es {'bestanden' if mit < ohne_n else 'GESCHEITERT'}\n\n")
z.append("Ab welchem k verschiebt sich der Median? (k Nullen unter n Falten, sonst 0,10; Rechnung wie TB-95)\n")
n = len(sel)
for k in range(0, n + 1):
    werte = [0.0] * k + [0.10] * (n - k)
    m_mit = float(np.median(werte))
    m_ohne = float(np.median([0.10] * (n - k))) if n - k else float("nan")
    z.append(f"  k={k}: Median mit {m_mit:.4f}, ohne die Nullen {m_ohne:.4f}, < {m_mit < m_ohne}\n")
z.append(f"  -> kleinstes wirksames k = {n // 2 + 1} (strikte Mehrheit len(sel)//2+1) bei n = {n}\n\n")
maj = set(sel[:len(sel) // 2 + 1])
e2 = f_lauf(maj)
f2 = e2["beurteilung"]["falten_sharpe"]
m1 = float(np.median(list(f2.values())))
m2 = float(np.median([v for k, v in f2.items() if k not in maj]))
z.append(f"Am Ablauf mit der Mehrheit {sorted(maj)}: Median mit {m1:.4f}, ohne {m2:.4f}, < {m1 < m2}\n")
e3 = f_lauf(set())
f3 = e3["beurteilung"]["falten_sharpe"]
m1 = float(np.median(list(f3.values())))
z.append(f"Am Ablauf mit leerer Menge: Median mit {m1:.4f}, ohne {m1:.4f}, < False (Gegenprobe scheitert wie gefordert)\n")
open(os.path.join(HIER, "a3_f4.txt"), "w").write("".join(z))

# --------------------------------------------------------------------------- A4
z = [KOPF, f"# A4 - die vier Jahresliterale. BOT = {BOT}, Exposure 0,50 (Teil D) bzw. 0,40/0,60 (beispieldaten)\n\n"]
z.append("Fundstellen (grep -nE '\"20[12][0-9]\"' am Stand HEAD):\n")
z.append(subprocess.run(["grep", "-nE", '"20[12][0-9]"', os.path.join(VR, "test_vorregistrierung.py"),
                         os.path.join(VR, "beispieldaten.py")], capture_output=True, text=True).stdout
         .replace(WURZEL + "/", ""))
z.append("\nBenchmark-Tabelle des Laufs (aw.BENCHMARK_TABELLE) fuer BOT, je Selektionsfalte:\n")
z.append("  falte       DD_bench(0,5)  1,25x     DD_tol(0,5)  erlaubt   bindet     | DD_bench(0,6) erlaubt(0,6) -11 zulaessig | erlaubt(0,4) -3 zulaessig\n")
dd_tol = bm.nachschlagen(tab[BOT]["dd_toleranz"], 0.5)
for f in sel:
    d5 = bm.nachschlagen(tab[BOT]["falten"][f]["dd_benchmark"], 0.5)
    g5 = bm.erlaubt(d5, dd_tol)
    bindet = "Toleranz" if g5 == dd_tol and dd_tol < rd.DD_RELATIVER_FAKTOR * d5 else "relativ"
    d6 = bm.nachschlagen(tab[BOT]["falten"][f]["dd_benchmark"], 0.6)
    g6 = bm.erlaubt(d6, bm.nachschlagen(tab[BOT]["dd_toleranz"], 0.6))
    d4 = bm.nachschlagen(tab[BOT]["falten"][f]["dd_benchmark"], 0.4)
    g4 = bm.erlaubt(d4, bm.nachschlagen(tab[BOT]["dd_toleranz"], 0.4))
    z.append(f"  {f:10s} {d5:10.2f} {rd.DD_RELATIVER_FAKTOR * d5:10.2f} {dd_tol:10.2f} {g5:10.2f}   {bindet:9s} |"
             f" {d6:10.2f} {g6:10.2f}   {'ja' if -11.0 >= g6 else 'NEIN':4s}        | {g4:8.2f}   {'ja' if -3.0 >= g4 else 'NEIN'}\n")
ruhigste = max(sel, key=lambda f: bm.nachschlagen(tab[BOT]["falten"][f]["dd_benchmark"], 0.5))
schwerste = min(sel, key=lambda f: bm.nachschlagen(tab[BOT]["falten"][f]["dd_benchmark"], 0.5))
z.append(f"\n  ruhigste Selektionsfalte (flachster DD_bench): {ruhigste}; schwerste (tiefster): {schwerste}\n")
z.append(f"  zweite Selektionsfalte des Plans (Fables Beispiel): {sel[1]}\n")

z.append("\nAlle neun Bots - welche Selektionsfalten deckt das Literal (\"2020\", \"2022\") in beispieldaten.py als Namen?\n")
for bot, p in plan.items():
    if p["status"] != "endgueltig":
        z.append(f"  {bot:28s} Platzhalter\n")
        continue
    s = t._selektionsfalten(p)
    treffer = [f for f in s if f in ("2020", "2022")]
    z.append(f"  {bot:28s} Selektionsfalten {s[0]}..{s[-1]} ({len(s)}), Treffer {treffer}\n")
open(os.path.join(HIER, "a4_literale.txt"), "w").write("".join(z))
print("geschrieben: a3_f4.txt, a4_literale.txt")
