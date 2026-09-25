"""TB-106 A8 - Tatsachennotizen: erreicht die registrierte Eingabe einen der Ersatzwert-Zweige?
Rein lesend, am Stand VOR Block B-E. Aufruf aus der Repo-Wurzel:
    trading-env/bin/python3 -W ignore docs/belege/TB-106/a8_messung.py <beispieldaten-ordner>
Sichtschutz 27.1: keine Kennzahl, keine Trade-Zahl, keine Faltenlaenge je Bot - nur Wahrheitswerte,
Zaehlungen von Zweigtreffern, Verhaeltnisse und Hashes.
"""
import hashlib
import json
import os
import sys
from datetime import datetime

V = "research/vorregistrierung"
sys.path.insert(0, V)
import auswertung as aw  # noqa: E402
import benchmark as bm  # noqa: E402
import faltenplan as fp  # noqa: E402
import registerdaten as rd  # noqa: E402

ROH = sys.argv[1] if len(sys.argv) > 1 else None
print("# TB-106 A8, HEAD %s, %s" % (os.popen("git rev-parse --short HEAD").read().strip(),
                                    datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")))
TAB = aw.BENCHMARK_TABELLE
print("Benchmark-Tabelle des Laufs: %s sha256 %s" % (
    os.path.relpath(TAB), hashlib.sha256(open(TAB, "rb").read()).hexdigest()))
tabellen = json.load(open(TAB, encoding="utf-8"))
mess = rd._mess()
plan = fp.faltenplan(mess)

print("\n== A1/A2 faltenplan.volle_jahre / faltenlaenge_jahre (Eingabe: %s)" % os.path.relpath(fp.TB24_DATEN))
for bot in rd.BOTS:
    z = fp.gefundene_trades_je_jahr(bot)
    jahre = sorted(z)
    innen = jahre[1:-1]
    print("  %-28s Zaehlung leer: %-5s  innere Jahre vorhanden: %-5s  -> A1 erreicht: %-5s A2 erreicht: %s" % (
        bot, not z, bool(innen), bool(z) and not innen, not z))

print("\n== A3 benchmark.drawdown_bei_exposure mit leerer Reihe - Handelstage je Falte in der Tabelle")
leer = [(b, n) for b, e in tabellen.items() for n, f in e["falten"].items() if f["handelstage"] == 0]
anz = sum(len(e["falten"]) for e in tabellen.values())
print("  Falten in der Tabelle: %d (alle Rollen), davon mit 0 Handelstagen: %d %s" % (anz, len(leer), leer))
print("  Falten der Tabelle = Falten des gerechneten Plans (Name und Rolle): %s" % all(
    [(f["name"], f["rolle"]) for f in plan[b]["falten"]]
    == [(n, f["rolle"]) for n, f in tabellen[b]["falten"].items()] for b in rd.BOTS))

print("\n== A4 benchmark.je_bot: dd_toleranz ohne Selektionsfalte")
for bot in rd.BOTS:
    sel_plan = [f for f in plan[bot]["falten"] if f["rolle"] == "selektion"]
    sel_tab = [n for n, f in tabellen[bot]["falten"].items() if f["rolle"] == "selektion"]
    print("  %-28s Plan hat Selektionsfalten: %-5s  Tabelle hat Selektionsfalten: %-5s -> A4 erreicht: %s" % (
        bot, bool(sel_plan), bool(sel_tab), not sel_plan))

print("\n== A5 benchmark.nachschlagen, e <= 0 -> 0.0: Grenzwert der Interpolation unterhalb der ersten Stufe")
stufe0 = min(float(k) for k in next(iter(tabellen.values()))["dd_toleranz"])
print("  erste Stufe: %.2f; Formel unterhalb: tabelle[stufe0] * e / stufe0" % stufe0)
abw = 0.0
gross = {e: 0.0 for e in (1e-3, 1e-4, 1e-6, 1e-9)}
n = 0
for bot, e in tabellen.items():
    for t in [e["dd_toleranz"]] + [f["dd_benchmark"] for f in e["falten"].values()]:
        y0 = bm.nachschlagen(t, stufe0)
        for x in gross:
            y = bm.nachschlagen(t, x)
            if y0:
                abw = max(abw, abs(y / y0 - x / stufe0))
            gross[x] = max(gross[x], abs(y))
        assert bm.nachschlagen(t, 0.0) == 0.0
        n += 1
print("  Tabellen (dd_toleranz + dd_benchmark je Falte, alle Bots): %d" % n)
print("  max |nachschlagen(t,e)/nachschlagen(t,stufe0) - e/stufe0| ueber alle Tabellen und e: %.3g" % abw)
for x, g in gross.items():
    # Sichtschutz 27.1: nicht der Betrag, nur ob er unter der Schranke |tabelle| <= 100 liegt
    print("  e = %-6g  max |nachschlagen(t,e)| <= 100*e/stufe0 = %.3g: %s" % (
        x, 100 * x / stufe0, g <= 100 * x / stufe0))
print("  nachschlagen(t, 0.0) == 0.0 fuer alle %d Tabellen: True" % n)
print("  -> die Formel geht fuer e -> 0 stetig gegen 0; der Zweig 'e <= 0 -> 0.0' ist ihr Grenzwert, keine Ersatzzahl")

print("\n== A7c registerdaten.raster_definition()['_bedingung'] je Bot")
for bot, d in rd.raster_definition().items():
    print("  %-28s _bedingung vorhanden: %-5s Text: %r" % (bot, "_bedingung" in d, d.get("_bedingung")))

if ROH:
    print("\n== A6/A7/A7b auswertung auf den Beispieldaten (%s) - Zweigtreffer instrumentiert" % ROH)
    treffer = {"A6_zelle_fehlt": 0, "A6_nachbar_fehlt": 0, "A7_ohne_selektionsfalten": 0}
    orig_plateau = aw.plateau
    orig_beta = aw.beta_bereinigung

    def plateau(achsen, bedingung, statistik):
        vorhanden, nachbarn = aw.nachbarschaften(achsen, bedingung)
        ids = set(statistik.index)
        for idx, w in vorhanden.items():
            if aw.zelle_id(achsen, w) not in ids:
                treffer["A6_zelle_fehlt"] += 1
            for nb in nachbarn[idx]:
                if aw.zelle_id(achsen, vorhanden[nb]) not in ids:
                    treffer["A6_nachbar_fehlt"] += 1
        return orig_plateau(achsen, bedingung, statistik)

    def beta(bot, wurzel, zid, plan_, sel):
        r = orig_beta(bot, wurzel, zid, plan_, sel)
        if not r.get("bestimmt"):
            treffer["A7_ohne_selektionsfalten"] += 1
        return r

    aw.plateau, aw.beta_bereinigung = plateau, beta
    for bot in rd.BOTS:
        if not os.path.isdir(os.path.join(ROH, bot)):
            print("  %-28s keine Beispieldaten" % bot)
            continue
        vor = dict(treffer)
        e = aw.ein_bot(bot, ROH, mess, plan, tabellen)
        print("  %-28s auswertbar %-5s  Treffer A6 Zelle %d, A6 Nachbar %d, A7 %d" % (
            bot, e["auswertbar"], treffer["A6_zelle_fehlt"] - vor["A6_zelle_fehlt"],
            treffer["A6_nachbar_fehlt"] - vor["A6_nachbar_fehlt"],
            treffer["A7_ohne_selektionsfalten"] - vor["A7_ohne_selektionsfalten"]))
    print("  Summe: %s" % treffer)
print("ENDE")
