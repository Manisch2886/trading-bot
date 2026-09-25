"""TB-105 A3: statische Importketten der Betriebs-Einstiegspunkte (liest nur Quelltext, fuehrt nichts aus).

crontab -l ist in dieser Sitzung abgelehnt (Werkzeugsperre). Die Einstiegspunkte stammen deshalb aus
UEBERGABEPROTOKOLL Abschnitt 2 (Bots), 4.3 (Dashboard/Warteauftraege), 4.4 (Bruecke), 4.6/4.7 (Waechter),
6.4 (Quartals-Review) und den launchd-Plists unter system/.
Aufloesung eines Namens: zuerst Ordner der importierenden Datei, dann shared/, notifications/, dashboard/,
broker/, Repo-Wurzel (die Programme setzen shared/ per sys.path.insert). runpy.run_path/subprocess-Ziele
sind nicht statisch sichtbar und werden als Zusatzkanten von Hand eingetragen (ZUSATZ)."""
import ast, glob, os, sys
W = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
os.chdir(W)
SUCH = ["shared", "notifications", "dashboard", "broker", "."]
ZIELE = sorted(glob.glob("strategies/*/equity_simulation.py") + glob.glob("strategies/*/multi_symbol_optimise.py")) + [
    "shared/symbols_config.py", "notifications/manual_close.py", "shared/strategy_paths.py",
    "research/exposure_messung/bot_lauf.py"]
EIN = (sorted(glob.glob("strategies/*/forward_test.py")) + sorted(glob.glob("strategies/*/quarterly_review.py")) +
       ["broker/spiegel.py", "broker/ibkr_spiegel.py", "dashboard/server.py", "dashboard/warteauftraege_ausfuehren.py",
        "notifications/telegram_bot.py", "notifications/waechter_melden.py", "system/log_rotation.py",
        "shared/ergebniskurven.py", "shared/determinismus.py", "research/versuchsregister/versuchsregister.py",
        "research/tb27_kapitalsimulation/vergleich.py", "system/nachtragswaechter.py"])
# Kindprozesse / runpy (aus dem Quelltext gelesen: ergebniskurven.py:185 -> kurven_lauf.py -> runpy equity_simulation;
# determinismus.py:160 -> determinismus_lauf.py -> runpy equity_simulation)
ZUSATZ = {"shared/ergebniskurven.py": ["shared/kurven_lauf.py"],
          "shared/determinismus.py": ["shared/determinismus_lauf.py"],
          "shared/kurven_lauf.py": sorted(glob.glob("strategies/*/equity_simulation.py")),
          "shared/determinismus_lauf.py": sorted(glob.glob("strategies/*/equity_simulation.py"))}

def aufloesen(name, von):
    teile = name.split(".")
    for basis in [os.path.dirname(von)] + SUCH:
        p = os.path.normpath(os.path.join(basis, *teile) + ".py")
        if os.path.isfile(p):
            return p
        p = os.path.normpath(os.path.join(basis, *teile, "__init__.py"))
        if os.path.isfile(p):
            return p
    return None

def importe(datei):
    try:
        baum = ast.parse(open(datei, encoding="utf-8").read())
    except Exception:
        return []
    namen = []
    for k in ast.walk(baum):
        if isinstance(k, ast.Import):
            namen += [a.name for a in k.names]
        elif isinstance(k, ast.ImportFrom) and k.module and not k.level:
            namen.append(k.module)
            namen += [k.module + "." + a.name for a in k.names]
    out = []
    for n in namen:
        p = aufloesen(n, datei)
        if p and p not in out:
            out.append(p)
    return out + ZUSATZ.get(datei, [])

def huelle(start):
    gesehen, stapel = set(), [start]
    while stapel:
        d = stapel.pop()
        if d in gesehen:
            continue
        gesehen.add(d)
        stapel += importe(d)
    return gesehen

H = {e: huelle(e) for e in EIN if os.path.isfile(e)}
print("# TB-105 A3 statische Importketten (a3_importketten.py); Einstiegspunkte: %d" % len(H))
print("| Datei (geaendert in TB-105) | geladen von Einstiegspunkt(en) |")
print("|---|---|")
for z in ZIELE:
    wer = [e for e in H if z in H[e]]
    print("| %s | %s |" % (z, ", ".join(wer) if wer else "keinem"))
