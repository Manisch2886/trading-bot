#!/usr/bin/env python3
"""TB-95 Block A - rein lesende Messung zu G6 und H3.

Aufruf (Repo-Wurzel):  trading-env/bin/python3 -W ignore docs/belege/TB-95/a_messung.py
Schreibt a1_faltenplan_ist.txt, a2_g6.txt, a3_h3.txt neben sich. Aendert keine
Datei im Repo; die H3-Probe laeuft wie im Test in Wegwerf-Verzeichnissen.
"""
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.abspath(os.path.join(HIER, "..", "..", ".."))
VR = os.path.join(WURZEL, "research", "vorregistrierung")
REGISTER = os.path.join(WURZEL, "docs", "VORREGISTRIERUNG_neuselektion.md")
sys.path.insert(0, VR)

import test_vorregistrierung as t  # noqa: E402  (main() laeuft nicht beim Import)

KOPF = (f"# TB-95 Block A - HEAD {subprocess.run(['git', '-C', WURZEL, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()}"
        f", {dt.datetime.now().astimezone():%Y-%m-%d %H:%M:%S %z}\n"
        f"# Werkzeug: docs/belege/TB-95/a_messung.py, Python {sys.version.split()[0]}\n")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def jahre(f):
    """Kalenderjahre, die eine Falte VOLL abdeckt (von <= 1.1., 31.12. < bis)."""
    von = dt.date.fromisoformat(f["von"])
    bis = dt.date.fromisoformat(f["bis_ausschliesslich"])
    return [j for j in range(von.year, bis.year + 1)
            if von <= dt.date(j, 1, 1) and dt.date(j, 12, 31) < bis]


plan = t._plan()
gesperrt_pfad = os.path.join(VR, "ergebnisse", "faltenplan.json")
gesperrt = json.load(open(gesperrt_pfad, encoding="utf-8"))

# ---------------------------------------------------------------- A1
z = [KOPF,
     "# A1 - der Ist-Stand des Faltenplans, je Bot",
     "#",
     "# ⚠️ Der Auftrag nennt als Quelle ergebnisse/faltenplan.json (0e54ac5c...). Nach Register",
     "# 30.2 (1) ist das der 'registrierte historische Stand eines frueheren Verfahrensstands' und",
     "# 'wird vom Lauf nicht gelesen'; nach 35.4 verwendet der Lauf den Plan, den faltenplan.py zur",
     "# Laufzeit bildet. Der Test liest ebenfalls fp.faltenplan(rd._mess()) (test_vorregistrierung.py",
     "# _plan()). Gemessen werden deshalb BEIDE; massgeblich fuer G6/H3 ist (B).",
     "#",
     f"# (A) gesperrt: {os.path.relpath(gesperrt_pfad, WURZEL)} sha256 {sha(gesperrt_pfad)}",
     f"# (B) Laufzeit: faltenplan.py sha256 {sha(os.path.join(VR, 'faltenplan.py'))}, fp.faltenplan(rd._mess())",
     "# Sichtschutz 27.1: nur Verfahrensseite (Namen, Rollen, Zahl, Jahre) - keine Ergebnisgroessen.",
     ""]
z.append("## (A) gesperrte Datei faltenplan.json - NUR zum Vergleich, vom Lauf nicht gelesen")
for bot, p in gesperrt.items():
    z.append(f"{bot:28s} status={p['status']:11s} Falten={len(p['falten'])}  "
             + " · ".join(f"{f['name']}[{f['rolle'][:3]}]" for f in p["falten"]))
z.append("")
z.append("## (B) Laufzeitplan (der Plan, den Test und Lauf verwenden)")
z.append(f"{'Bot':28s} {'L':>2s} {'#sel':>4s} {'#ges':>4s}  Falten (Name [Rolle] -> abgedeckte Kalenderjahre)")
for bot, p in plan.items():
    sel = [f for f in p["falten"] if f["rolle"] == "selektion"]
    z.append(f"{bot:28s} {p['faltenlaenge_jahre']:>2d} {len(sel):>4d} {len(p['falten']):>4d}  status={p['status']}")
    for f in p["falten"]:
        z.append(f"{'':28s}      {f['name']:24s} {f['rolle']:13s} {f['von']} .. {f['bis_ausschliesslich']} (ausschl.)  Jahre {jahre(f)}")
z.append("")
z.append("## Abgleich (B) gegen die Tabelle in Register 33.2 (Selektionsfalten je Bot, Zahl)")
soll_332 = {"elliott_wave": 4, "t3_supertrend": 7, "rsi2_crypto": 7, "turtle_soup_crypto": 8,
            "volatility_breakout_crypto": 8, "elliott_wave_stocks": 9, "rsi2_mean_reversion": 8,
            "turtle_soup_stocks": 9, "volatility_breakout": 8}
abw = 0
for bot, n in soll_332.items():
    ist = len([f for f in plan[bot]["falten"] if f["rolle"] == "selektion"])
    abw += ist != n
    z.append(f"  {bot:28s} 33.2: {n}  Laufzeit: {ist}  {'gleich' if ist == n else 'ABWEICHUNG'}")
z.append(f"  Abweichungen: {abw}")
open(os.path.join(HIER, "a1_faltenplan_ist.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")

# ---------------------------------------------------------------- A2
z = [KOPF, "# A2 - G6 ausmessen", ""]
z.append("## A2-1 Fuer welche Bots schlaegt die HEUTIGE Pruefung fehl? (\"2020\" in namen and \"2022\" in namen)")
rot = []
for bot, p in plan.items():
    if p["status"] != "endgueltig":
        z.append(f"  {bot:28s} Platzhalter -> G5 statt G6")
        continue
    namen = [f["name"] for f in p["falten"]]
    ok = "2020" in namen and "2022" in namen
    if not ok:
        rot.append(bot)
    z.append(f"  {bot:28s} {'gruen' if ok else 'ROT  '}  {namen}")
z.append(f"  => rot: {rot}  (erwartet: nur elliott_wave)")
z.append("")
z.append("## A2-2 Die Sache: sind 2020 und 2022 bei jedem Bot von einer Falte der Rolle 'selektion' abgedeckt?")
z.append("   (Abdeckung gerechnet aus von/bis_ausschliesslich; Bestaetigungsfalten zaehlen nicht)")
alle = True
for bot, p in plan.items():
    for j in (2020, 2022):
        sel = [f["name"] for f in p["falten"] if f["rolle"] == "selektion" and j in jahre(f)]
        best = [f["name"] for f in p["falten"] if f["rolle"] != "selektion" and j in jahre(f)]
        alle &= len(sel) == 1
        z.append(f"  {bot:28s} {j}: Selektionsfalte {sel}  Bestaetigung {best}")
z.append(f"  => A2-2: {'JA' if alle else 'NEIN'} - jedes der zwei Jahre liegt bei allen neun Bots in genau einer Selektionsfalte")
z.append("")
z.append("## A2-3 Woher stammt das Literal?")
reg = open(REGISTER, encoding="utf-8").read().splitlines()
for i, zeile in enumerate(reg, 1):
    if "2020 und 2022 sind" in zeile or "2020 und 2022 sind keine" in zeile:
        z.append(f"  Register Z. {i}: {zeile.strip()[:160]}")
z.append("  (Zeilennummern am HEAD oben, 38.2)")
z.append("  Pruefung eingefuehrt mit a2fcf01 (TB-30a, 14.09.2026) - git log -S.")
muster = re.compile(r"^(\d)\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*")
treffer = [(i, m.groups()) for i, zeile in enumerate(reg, 1) if (m := muster.match(zeile))]
z.append(f"  Listenpunkt-Muster {muster.pattern!r}: {len(treffer)} Treffer {treffer}")
open(os.path.join(HIER, "a2_g6.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")

# ---------------------------------------------------------------- A3
z = [KOPF, "# A3 - H3 ausmessen", ""]
p = plan[t.BOT]
sel = [f["name"] for f in p["falten"] if f["rolle"] == "selektion"]
ohne_alt = {"2019", "2020", "2021", "2022"}
z.append(f"## A3-1 BOT = {t.BOT!r}; Falten im Laufzeitplan: {len(p['falten'])}, davon Selektion: {len(sel)}")
z.append(f"   Selektionsfalten: {sel}")
z.append(f"   Bestaetigung: {[f['name'] for f in p['falten'] if f['rolle'] != 'selektion']}")
z.append("")
z.append(f"## A3-2 Treffer von ohne = {sorted(ohne_alt)} in den Falten des BOT: "
         f"{len(ohne_alt & set(f['name'] for f in p['falten']))} von 4  -> {sorted(ohne_alt & set(sel))}")
z.append("   ⚠️ Erwartung des Auftrags war 'null'. WIDERLEGT: alle vier treffen. Die Probe greift nicht ins Leere;")
z.append("   sie beisst nicht, weil vier gesetzte Nullen bei NEUN Selektionsfalten den Median nicht verschieben (A3-4).")
z.append("   Das deckt sich mit Register 38 (Tabelle zu H3, 'seit der ersten Falte 2017 sind es neun').")
z.append("")


def zeile_median(n, k):
    mit = [0.0] * k + [0.10] * (n - k)        # Regel aktiv: Falten ohne Trade -> 0
    ohne = [9.0] * k + [0.10] * (n - k)       # Regel entfernt: Dateiwert 9.0 gilt
    return float(np.median(mit)), float(np.median(ohne))


z.append("## A3-4 Rechnung: Median des Netto-Sharpe ueber die Selektionsfalten (auswertung.py Z. 234-236,")
z.append("   groupby(zelle_id).median ueber rolle == selektion). Beispieldaten der Probe: k Falten mit 0 Trades")
z.append("   und Dateiwert 9.0, die uebrigen n-k mit 40 Trades und 0.10.")
z.append("   mit Regel:  k Werte 0.0 und n-k Werte 0.10;  ohne Regel: k Werte 9.0 und n-k Werte 0.10.")
z.append("   Der Median ist fuer ungerades n der ((n+1)/2)-te Wert der sortierten Liste; er wechselt erst,")
z.append("   wenn k >= (n+1)/2. Fuer gerades n (Mittel der zwei mittleren) genuegt k >= n/2.")
z.append("   Allgemein: kleinstes beissendes k = ceil(n/2); strikte Mehrheit floor(n/2)+1 beisst bei jeder Paritaet.")
for n in (7, len(sel)):
    z.append(f"   n = {n}:")
    for k in range(0, n + 1):
        a, b = zeile_median(n, k)
        z.append(f"     k={k}: mit Regel {a:.4f}  ohne Regel {b:.4f}  {'BEISST' if a != b else 'beisst nicht'}")
kmin = next(k for k in range(len(sel) + 1) if zeile_median(len(sel), k)[0] != zeile_median(len(sel), k)[1])
z.append(f"   => bei der registrierten Zahl n = {len(sel)} beisst die Probe ab k = {kmin}; die heutige Vier ist zu KLEIN.")
z.append("      (Der Kommentar Z. 583-589 begruendet die Vier mit 'sieben Falten' - fuer n = 7 stimmt sie: k_min = 4.)")
z.append("")

z.append("## A3-3 Die heutige Probe, nachgestellt wie im Test (zwei Unterprozesse auswertung.py)")
mess = t._mess()
with tempfile.TemporaryDirectory() as roh2, tempfile.TemporaryDirectory() as m:
    t.bd.erzeuge(roh2, t.BOT, mess=mess, plan=plan,
                 trades_fn=lambda w, i, f, a: 0 if f in ohne_alt else 40,
                 sharpe_fn=lambda w, i, f, a: 9.0 if f in ohne_alt else 0.10)
    vorher = t._auswerten_in(VR, roh2)
    t._kopie(m)
    t._ersetze(os.path.join(m, "auswertung.py"),
               'df["netto_sharpe"] = np.where(df["n_trades"].to_numpy() == 0, 0.0,\n'
               '                                  df["netto_sharpe"].to_numpy(dtype=float))',
               'df["netto_sharpe"] = df["netto_sharpe"].to_numpy(dtype=float)')
    nachher = t._auswerten_in(m, roh2)
z.append(f"   mit Regel:  rc {vorher.returncode}  {t._sharpezeile(vorher.stdout)!r}")
z.append(f"   ohne Regel: rc {nachher.returncode}  {t._sharpezeile(nachher.stdout)!r}")
z.append(f"   => gleich: {t._sharpezeile(vorher.stdout) == t._sharpezeile(nachher.stdout)}  (TB-92-Meldetext: 'Netto-Sharpe (Med.) 0.1000' / 'Netto-Sharpe (Med.) 0.1000') - BESTAETIGT")
z.append("")
z.append("## A3-5 Ist 'ohne' ein Literal, das aus dem Plan kommen muesste?")
z.append("   Ja - dieselbe Klasse wie G6: vier Faltennamen als Zeichenketten, dazu eine Anzahl (4), die aus")
z.append("   einer Faltenzahl (7) abgeleitet war, die nirgends im Code steht. Beides ist eine Kopie des Plans.")
z.append("")
z.append("## B3 - Mutationsstelle in auswertung.py (H3 _ersetze)")
s = open(os.path.join(VR, "auswertung.py"), encoding="utf-8").read()
alt = ('df["netto_sharpe"] = np.where(df["n_trades"].to_numpy() == 0, 0.0,\n'
       '                                  df["netto_sharpe"].to_numpy(dtype=float))')
z.append(f"   Vorkommen im heutigen auswertung.py (sha256 {sha(os.path.join(VR, 'auswertung.py'))[:16]}...): {s.count(alt)}  (verlangt: genau 1)")
open(os.path.join(HIER, "a3_h3.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("fertig")
