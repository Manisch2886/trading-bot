# TB-132 P3 - Mini-Probe Lueckentag, synthetische Daten, ausserhalb des Repos.
# Laedt die echten Kerne nur lesend (PYTHONDONTWRITEBYTECODE=1).
import ast, importlib.util, os, sys
import numpy as np, pandas as pd

REPO = sys.argv[1]
def lade(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

mk = lade("mtm_kern", "research/mtm_drawdown/mtm_kern.py")
ek = lade("exposure_kern", "research/exposure_messung/exposure_kern.py")
print("pandas", pd.__version__, "numpy", np.__version__, "python", sys.version.split()[0])

tage8 = pd.bdate_range("2024-03-04", periods=8)          # D1..D8 (Mo..Mi)
D = {i + 1: t for i, t in enumerate(tage8)}
ok_alle = True
def pruefe(name, bed, zusatz=""):
    global ok_alle
    ok_alle &= bool(bed)
    print(("OK   " if bed else "ABW  ") + name + (" - " + zusatz if zusatz else ""))

def ereignis(entry, exit_, sym, ep, alloc, pnl, start):
    return pd.DataFrame([{"entry_time": entry, "exit_time": exit_, "symbol": sym,
                          "entry_price": ep, "allocation": alloc, "pnl_pct": pnl,
                          "capital_after": start + alloc * pnl / 100.0}])

START, ALLOC, KOSTEN = 10_000.0, 1_000.0, 0.1
x_alle = pd.Series([100, 102, 104, 0, 0, 110, 111, 112], index=tage8, dtype=float)
y_alle = pd.Series([50, 51, 52, 53, 54, 55, 56, 57], index=tage8, dtype=float)

# --- Fall A: Zeile fehlt bei X an D4, D5; Y hat Kurs --------------------------
for etikett, x in (("Zeile fehlt", x_alle.drop([D[4], D[5]])),
                   ("close leer (NaN in der Reihe)", x_alle.where(~x_alle.index.isin([D[4], D[5]])))):
    kurse_dict = {"X": x, "Y": y_alle}
    raster = mk.tagesraster(kurse_dict)
    kurse, fort = mk.kurse_auf_raster(kurse_dict, raster)
    er = ereignis(D[2], D[7], "X", 102.0, ALLOC, 5.0, START)
    pfad = mk.mtm_pfad(er, kurse, fort, START, KOSTEN)
    print("\nFall A (%s): Raster %d Tage" % (etikett, len(raster)))
    pruefe("A1 Lueckentage D4, D5 stehen im Raster", D[4] in raster and D[5] in raster)
    pruefe("A2 Kurs X an D4, D5 = letzter Kurs (D3)",
           kurse.at[D[4], "X"] == 104.0 and kurse.at[D[5], "X"] == 104.0)
    pruefe("A3 mtm an D4 und D5 = mtm an D3 (Rendite 0 am Lueckentag)",
           pfad.at[D[4], "mtm"] == pfad.at[D[3], "mtm"] and pfad.at[D[5], "mtm"] == pfad.at[D[3], "mtm"],
           "Differenzen %r" % [float(pfad.at[D[k], "mtm"] - pfad.at[D[3], "mtm"]) for k in (4, 5)])
    pruefe("A4 Position bleibt offen: n_offen = 1, gebunden = Allokation an D4, D5",
           all(pfad.at[D[k], "n_offen"] == 1 and pfad.at[D[k], "gebunden"] == ALLOC for k in (4, 5)))
    pruefe("A5 Spalte fortgeschrieben zaehlt die Positionstage: 1 an D4, D5, sonst 0; Summe 2",
           pfad.at[D[4], "fortgeschrieben"] == 1 and pfad.at[D[5], "fortgeschrieben"] == 1
           and int(pfad["fortgeschrieben"].sum()) == 2)
    soll = START + ALLOC * (110.0 / 102.0 - 1 - KOSTEN / 100.0)
    pruefe("A6 naechster Kurstag D6 traegt die Bewegung ueber die Luecke",
           abs(pfad.at[D[6], "mtm"] - soll) < 1e-9)

# --- Fall B: kein Symbol mit Kurs an D4 --------------------------------------
kurse_dict = {"X": x_alle.drop([D[4]]).replace(0, 107.0), "Y": y_alle.drop([D[4]])}
raster = mk.tagesraster(kurse_dict)
print("\nFall B (kein Symbol hat an D4 einen Kurs)")
pruefe("B1 eigenes Raster des Kerns (tagesraster) fuehrt D4 NICHT", D[4] not in raster,
       "Raster %d Tage" % len(raster))
kurse, fort = mk.kurse_auf_raster(kurse_dict, tage8)       # Kalender-Raster von aussen
er = ereignis(D[2], D[7], "X", 102.0, ALLOC, 5.0, START)
pfad = mk.mtm_pfad(er, kurse, fort, START, KOSTEN)
pruefe("B2 mit von aussen gegebenem Kalender-Raster: D4 steht, Kurs fortgeschrieben, mtm wie D3, n_offen 1",
       kurse.at[D[4], "X"] == 104.0 and pfad.at[D[4], "mtm"] == pfad.at[D[3], "mtm"]
       and pfad.at[D[4], "n_offen"] == 1 and pfad.at[D[4], "fortgeschrieben"] == 1)

# --- Fall C: Position vor dem ersten Kurs des Symbols -------------------------
kurse_dict = {"X": x_alle.replace(0, 107.0).iloc[3:], "Y": y_alle}
kurse, fort = mk.kurse_auf_raster(kurse_dict, mk.tagesraster(kurse_dict))
try:
    mk.mtm_pfad(ereignis(D[2], D[7], "X", 102.0, ALLOC, 5.0, START), kurse, fort, START, KOSTEN)
    pruefe("C1 Position vor erstem Kurs -> ValueError", False)
except ValueError as f:
    print("\nFall C"); pruefe("C1 Position vor erstem Kurs -> ValueError (kein Fortschreiben rueckwaerts)", True, str(f)[:70])

# --- Fall D: Reihenende - X ohne Kurs ab D6, Position bis D8 ------------------
kurse_dict = {"X": x_alle.replace(0, 107.0).iloc[:5], "Y": y_alle}
kurse, fort = mk.kurse_auf_raster(kurse_dict, mk.tagesraster(kurse_dict))
pfad = mk.mtm_pfad(ereignis(D[2], D[8] + pd.Timedelta(days=1), "X", 102.0, ALLOC, 5.0, START), kurse, fort, START, KOSTEN)
print("\nFall D (Reihenende von X nach D5, Position offen bis D8)")
pruefe("D1 nach dem letzten Kurs: weiter zum letzten Kurs bewertet, offen, gezaehlt (D6..D8)",
       all(pfad.at[D[k], "mtm"] == pfad.at[D[5], "mtm"] and pfad.at[D[k], "n_offen"] == 1
           and pfad.at[D[k], "fortgeschrieben"] == 1 for k in (6, 7, 8)))

# --- Fall E: zweite Stelle - research/exposure_messung/auswertung.py::mtm_reihen
quelle = open(os.path.join(REPO, "research/exposure_messung/auswertung.py"), encoding="utf-8").read()
knoten = [k for k in ast.parse(quelle).body if isinstance(k, ast.FunctionDef) and k.name == "mtm_reihen"][0]
raum = {"np": np, "pd": pd}
exec(compile(ast.Module(body=[knoten], type_ignores=[]), "mtm_reihen", "exec"), raum)
pos = pd.DataFrame([{"entry_time": D[2], "exit_time": D[7], "symbol": "X", "allocation": ALLOC,
                     "pnl_pct": 5.0, "capital_after": START + 50.0}])
reihen = ek.taegliche_reihen(pos, START)
wert, naht = raum["mtm_reihen"]("bot", pos, {"X": x_alle.drop([D[4], D[5]]), "Y": y_alle}, reihen)
print("\nFall E (exposure_messung/auswertung.py::mtm_reihen, Kalendertage %d)" % len(reihen))
pruefe("E1 Lueckentage D4, D5 (und Wochenende): Wert wie am letzten Kurstag",
       wert.at[D[4]] == wert.at[D[3]] and wert.at[D[5]] == wert.at[D[3]]
       and wert.at[D[5] + pd.Timedelta(days=1)] == wert.at[D[3]])
pruefe("E2 Position bleibt in gebunden/n_offen an D4, D5",
       all(reihen.at[D[k], "gebunden"] == ALLOC and reihen.at[D[k], "n_offen"] == 1 for k in (4, 5)))
wert2, _ = raum["mtm_reihen"]("bot", pos, {"Y": y_alle}, reihen)
print("E3 (nur Verhalten) Symbol ganz ohne Kursreihe: Wert der Position geht mit %r ein; "
      "frei = kapital_ende - gebunden" % float(wert2.at[D[4]] - (reihen.at[D[4], "kapital_ende"] - ALLOC)))

print("\nErgebnis:", "alle Pruefungen OK" if ok_alle else "ABWEICHUNG")
sys.exit(0 if ok_alle else 1)
