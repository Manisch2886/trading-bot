#!/usr/bin/env python3
"""TB-115 M3 - deckt die Sperrlisten-Sonde (TB-85) die Kette
Snapshot -> Erzeuger -> zellen.csv -> auswertung.py -> Bericht?

Rein lesend. Je Glied die Datei(en) und ihre Bindung:
  S   Sperrliste: Pfad eines Punkts in Abschnitt 10 (gelesen aus dem Abbild
      5e5ad109 - (ii) der Sonde haelt das Abbild gegen den Registertext)
  A   Abbild, Gruppe `eingefroren` (die Sonde prueft sie AUS DEM ABBILD)
  E   `herkunft.py::EINGEFROREN` heute (ast, ohne herkunft.py auszufuehren -
      derselbe Leser wie der Abbild-Erzeuger: sperrlistensonde.lies_eingefroren)
  W   `shared/paths.py::ARBEITSBAUM_PFADE` (Sauberkeit unter dem Modus; ast)
  G   im Git versioniert (git ls-files)
Dazu zwei Startpruefungs-Tatsachen, gemessen statt behauptet:
  T1  `paths._modus_aus_umgebung` vergleicht TB_SELEKTIONSHASH mit dem
      `snapshot_hash` AUS DEM MANIFEST - rechnet es die Dateien nach? (ast:
      ruft die Funktion etwas auf, das Dateiinhalte hasht?)
  T2  liest `auswertung.py` die Datei `herkunft.json`, die sein Vertrag nennt?
Und der Snapshot selbst: `shared/snapshot.py --pruefen` (liest, schreibt nichts).

Aufruf aus der Repo-Wurzel: python3 docs/belege/TB-115/m3_kette.py
"""
import ast
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, "shared")
import sperrlistensonde as sonde                              # noqa: E402

SNAP = "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
ABBILD = "research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb114.json"
V = "research/vorregistrierung"

GLIEDER = [
    ("1 Snapshot", [f"{SNAP}/MANIFEST.json", f"{SNAP}/AAPL_1d.csv",
                    f"{SNAP}/BTCUSDT_4h.csv", f"{SNAP}/config/top25_symbols.txt",
                    f"{SNAP}/config/sp500_top150.txt",
                    "config/top25_symbols.txt", "config/sp500_top150.txt",
                    "shared/snapshot.py", f"{V}/herkunft.py"]),
    ("2 Erzeuger (nicht gebaut)", [
        "strategies/volatility_breakout/equity_simulation.py",
        "strategies/volatility_breakout/multi_symbol_optimise.py",
        "strategies/volatility_breakout/backtest_breakout.py",
        "shared/paths.py", "shared/zuteilung.py", f"{V}/faltenplan.py",
        f"{V}/ergebnisse/faltenplan.json", f"{V}/registerdaten.py"]),
    ("3 zellen.csv (+ tagesreihen, herkunft.json, benchmark_tagesreihen)", [
        "<rohergebnisse>/<bot>/zellen.csv", "<rohergebnisse>/<bot>/herkunft.json",
        f"{V}/beispieldaten.py"]),
    ("4 auswertung.py (+ Importe und gelesene Tabellen)", [
        f"{V}/auswertung.py", f"{V}/kennzahlen.py", f"{V}/benchmark.py",
        f"{V}/faltenplan.py", f"{V}/registerdaten.py", f"{V}/messgroessen.py",
        f"{V}/ergebnisse/messgroessen.json",
        f"{V}/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json",
        "shared/paths.py"]),
    ("5 Bericht", ["<stdout von auswertung.py>", "<--json PFAD>",
                   f"{V}/registerbericht.py"]),
]


def arbeitsbaum_pfade():
    baum = ast.parse(open("shared/paths.py", encoding="utf-8").read())
    for k in baum.body:
        if isinstance(k, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "ARBEITSBAUM_PFADE"
                for t in k.targets):
            werte = []
            for e in k.value.elts:
                werte.append("requirements.lock" if isinstance(e, ast.Name)
                             else e.value)
            return werte
    raise SystemExit("ARBEITSBAUM_PFADE nicht gefunden")


def in_w(pfad, w):
    return any(pfad == x or pfad.startswith(x.rstrip("/") + "/") for x in w)


def versioniert(pfad):
    return subprocess.run(["git", "ls-files", "--error-unmatch", pfad],
                          capture_output=True).returncode == 0


def sha(pfad):
    with open(pfad, "rb") as d:
        return hashlib.sha256(d.read()).hexdigest()


def main():
    abbild = json.load(open(ABBILD, encoding="utf-8"))
    s_pfade = {}
    for p in abbild["punkte"]:
        for rel in p["pfade"]:
            s_pfade.setdefault(rel, []).append(p["punkt"])
    a_pfade = {e["pfad"] for e in abbild["eingefroren"]}
    e_pfade = set(sonde.lies_eingefroren("."))
    w = arbeitsbaum_pfade()
    print("# TB-115 M3 - Kette Erzeuger -> Auswertung gegen die Bindungen")
    print(f"Abbild {ABBILD} sha256 {sha(ABBILD)[:12]}...: {len(abbild['punkte'])} "
          f"Punkte, {len(s_pfade)} verschiedene Pfade; eingefroren "
          f"{len(a_pfade)}; bestimmt {len(abbild['bestimmt'])}")
    print(f"herkunft.EINGEFROREN heute: {len(e_pfade)}; gleich Abbild: "
          f"{e_pfade == a_pfade}; ARBEITSBAUM_PFADE: {len(w)} Eintraege")
    print("\nSpalten: S=Sperrliste-Punkt(e)  A=Abbild eingefroren  "
          "E=EINGEFROREN heute  W=ARBEITSBAUM_PFADE  G=versioniert")
    for glied, dateien in GLIEDER:
        print(f"\n## {glied}")
        for d in dateien:
            if d.startswith("<"):
                print(f"  {'-':<6} {'-':<2} {'-':<2} {'-':<2} {'-':<2}  {d}  "
                      f"(kein fester Pfad)")
                continue
            s = ",".join(str(x) for x in s_pfade.get(d, [])) or "-"
            print(f"  {s:<6} {'A' if d in a_pfade else '-':<2} "
                  f"{'E' if d in e_pfade else '-':<2} "
                  f"{'W' if in_w(d, w) else '-':<2} "
                  f"{'G' if versioniert(d) else '-':<2}  {d}")

    print("\n## Snapshot-config gegen Repo-config (Sperrlistenpunkt 8 nennt die "
          "Repo-Dateien; unter dem Modus liest der Lauf die Snapshot-Kopien)")
    for n in ("top25_symbols.txt", "sp500_top150.txt"):
        a, b = sha(f"config/{n}"), sha(f"{SNAP}/config/{n}")
        print(f"  {n}: Repo {a[:12]}  Snapshot {b[:12]}  gleich {a == b}")

    print("\n## T1 - rechnet die Startpruefung den Snapshot nach?")
    baum = ast.parse(open("shared/paths.py", encoding="utf-8").read())
    fn = {k.name: k for k in baum.body if isinstance(k, ast.FunctionDef)}
    for name in ("_modus_aus_umgebung", "_lies_snapshot_hash", "_lies_manifest"):
        aufrufe = sorted({(c.func.attr if isinstance(c.func, ast.Attribute)
                           else getattr(c.func, "id", "?"))
                          for c in ast.walk(fn[name]) if isinstance(c, ast.Call)})
        print(f"  paths.{name} ruft: {aufrufe}")
    print("  (kein sha256/hashlib/snapshot_hash/quersumme darunter = der Hash wird "
          "aus dem Manifest GELESEN, nicht aus den Dateien gerechnet)")

    print("\n## T2 - liest auswertung.py herkunft.json?")
    quelle = open(f"{V}/auswertung.py", encoding="utf-8").read()
    zeilen = [i + 1 for i, z in enumerate(quelle.splitlines()) if "herkunft" in z]
    code = ast.parse(quelle)
    doc_knoten = code.body[0].value          # der Modul-Docstring
    im_code = [n.lineno for n in ast.walk(code) if isinstance(n, ast.Constant)
               and isinstance(n.value, str) and "herkunft" in n.value
               and n is not doc_knoten]
    namen = [n.lineno for n in ast.walk(code)
             if isinstance(n, (ast.Name, ast.Attribute))
             and "herkunft" in (getattr(n, "id", "") + getattr(n, "attr", ""))]
    print(f"  Zeilen mit 'herkunft': {zeilen}; im Modul-Docstring "
          f"(Z. {doc_knoten.lineno}-{doc_knoten.end_lineno}): "
          f"{all(doc_knoten.lineno <= z <= doc_knoten.end_lineno for z in zeilen)}; "
          f"String-Konstanten ausserhalb des Docstrings: {im_code}; "
          f"Namen/Attribute 'herkunft': {namen}")

    print("\n## Snapshot selbst: shared/snapshot.py --pruefen (liest nur)")
    lauf = subprocess.run([sys.executable, "-W", "ignore", "shared/snapshot.py",
                           "--pruefen", SNAP], capture_output=True, text=True)
    for z in (lauf.stdout + lauf.stderr).strip().splitlines()[-6:]:
        print(f"  | {z}")
    print(f"  rc {lauf.returncode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
