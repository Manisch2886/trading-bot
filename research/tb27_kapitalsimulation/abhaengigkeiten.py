#!/usr/bin/env python3
"""TB-27 - Wer haengt an den neun `equity_simulation.py`?

TB-26 hat begruendet abgelehnt, die neun Dateien zusammenzulegen, weil mehrere
Werkzeuge an ihrer heutigen Form haengen: ein `equity_simulation.py` je Bot, je
Unterprozess importiert, mit `inspect.signature`-Abfragen darauf. Genannt waren
`shared/determinismus.py`, `shared/ergebniskurven.py`,
`shared/portfolio_overview.py`, `shared/zuteilung.py` und
`research/order_sensitivity/run_one_bot.py` - mit dem ausdruecklichen Zusatz,
die Liste sei vermutlich nicht vollstaendig.

Dieses Werkzeug sucht sie mechanisch und teilt jede Fundstelle in eine von
fuenf Klassen ein:

  IMPORT     `import equity_simulation` / `from equity_simulation import ...`
             Traegt nur, wenn `sys.path` vorher auf den Bot-Ordner zeigt -
             der Name ist bewusst nicht eindeutig, jeder Bot hat einen eigenen.
  LADEN      dieselbe Datei ueber `importlib.util.spec_from_file_location`,
             `runpy.run_path` oder `exec()` geladen, also ueber ihren PFAD.
  PROZESS    als Unterprozess gestartet (`subprocess`), meist ueber
             `sys.executable`.
  SIGNATUR   fragt die Signatur einer Funktion daraus ab
             (`inspect.signature`, `co_varnames`, `__code__`).
  PFAD       spricht die Datei als Pfad an, ohne sie auszufuehren -
             Existenzpruefung, Einlesen, AST-Vergleich.
  ERWAEHNUNG kommt nur in Kommentar, Docstring oder Text vor.

Ein und dieselbe Datei kann in mehreren Klassen stehen; ausgegeben werden alle
zutreffenden.

Aufruf:

    python3 research/tb27_kapitalsimulation/abhaengigkeiten.py
    python3 research/tb27_kapitalsimulation/abhaengigkeiten.py --ohne-erwaehnung
    python3 research/tb27_kapitalsimulation/abhaengigkeiten.py --zeilen

Grenzen des Verfahrens - im Bericht ausgewiesen
-----------------------------------------------
Gesucht wird nach dem Zeichenketten-Stamm `equity_simulation` im Quelltext.
Wer die Datei ueber einen zusammengesetzten Namen erreicht (etwa
`"equity_" + "simulation.py"`) oder ueber ein Verzeichnis-Listing aller
`.py`-Dateien eines Bots, faellt durch das Raster. Nach beidem ist zusaetzlich
von Hand gesucht worden (siehe BERICHT.md, Abschnitt 5). Nicht durchsucht
werden Crontab und launchd-Vorlagen des Nutzers - die liegen nicht im Repo.
"""

import argparse
import os
import re
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))

STAMM = "equity_simulation"

# Klassenerkennung. Jede Regel ist ein regulaerer Ausdruck auf einer Zeile,
# ausser SIGNATUR und PROZESS: die pruefen zusaetzlich die ganze Datei, weil
# der Bezug dort ueber mehrere Zeilen laeuft.
ZEILENREGELN = [
    ("IMPORT", re.compile(r"^\s*(?:import\s+(?:oos_)?equity_simulation"
                          r"|from\s+(?:oos_)?equity_simulation\s+import)")),
    ("LADEN", re.compile(r"(spec_from_file_location|run_path|exec\()")),
    ("PFAD", re.compile(r"[\"']" + STAMM + r"(?:\.py)?[\"']|" + STAMM + r"\.py")),
]

DATEIREGELN = [
    ("SIGNATUR", re.compile(r"^(?!\s*#).*(inspect\.signature|co_varnames"
                            r"|__code__|getfullargspec)", re.M)),
    ("PROZESS", re.compile(r"^(?!\s*#).*subprocess\.", re.M)),
]

# Verzeichnisse, die nichts zur Sache beitragen. `tb27_kapitalsimulation` ist
# dieses Werkzeug selbst - es faende sonst sich.
AUSGENOMMEN = {".git", "__pycache__", "data", "results", "logs",
               "tb27_kapitalsimulation"}


def py_dateien():
    for wurzel, ordner, dateien in os.walk(_WURZEL):
        ordner[:] = [o for o in ordner if o not in AUSGENOMMEN]
        for name in sorted(dateien):
            if name.endswith(".py"):
                yield os.path.join(wurzel, name)


def _kommentar_oder_text(zeile):
    """Grobe, bewusst konservative Schaetzung: steht der Fund in Prosa?

    Konservativ heisst hier: im Zweifel NICHT als blosse Erwaehnung einordnen.
    Eine falsch als Prosa eingeordnete Codezeile waere eine uebersehene
    Abhaengigkeit; eine falsch als Code eingeordnete Prosazeile kostet nur
    einen Blick.
    """
    ohne = zeile.strip()
    return ohne.startswith("#") or ohne.startswith("*") or ohne.startswith(">")


def untersuchen(pfad):
    with open(pfad, encoding="utf-8", errors="replace") as f:
        text = f.read()
    if STAMM not in text:
        return None

    zeilen = text.splitlines()
    klassen = {}
    for nr, zeile in enumerate(zeilen, 1):
        if STAMM not in zeile:
            continue
        getroffen = False
        for klasse, regel in ZEILENREGELN:
            if regel.search(zeile) and not _kommentar_oder_text(zeile):
                klassen.setdefault(klasse, []).append((nr, zeile.strip()))
                getroffen = True
        if not getroffen:
            klassen.setdefault("ERWAEHNUNG", []).append((nr, zeile.strip()))

    # Dateiweite Regeln greifen nur, wenn die Datei die Simulation ueberhaupt
    # als Code anfasst - sonst waere jedes Skript mit `subprocess` dabei.
    fasst_an = bool(set(klassen) - {"ERWAEHNUNG"})
    if fasst_an:
        for klasse, regel in DATEIREGELN:
            if regel.search(text):
                klassen[klasse] = klassen.get(klasse, [])

    return klassen


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--ohne-erwaehnung", action="store_true",
                   help="Dateien weglassen, die die Simulation nur nennen")
    p.add_argument("--zeilen", action="store_true",
                   help="die gefundenen Zeilen mit ausgeben")
    args = p.parse_args(argv)

    treffer = {}
    genannt = 0
    for pfad in py_dateien():
        klassen = untersuchen(pfad)
        if not klassen:
            continue
        genannt += 1
        rel = os.path.relpath(pfad, _WURZEL)
        if args.ohne_erwaehnung and set(klassen) == {"ERWAEHNUNG"}:
            continue
        treffer[rel] = klassen

    reihenfolge = ["IMPORT", "LADEN", "PROZESS", "SIGNATUR", "PFAD", "ERWAEHNUNG"]
    nach_klasse = {k: [] for k in reihenfolge}
    for rel, klassen in treffer.items():
        for k in klassen:
            nach_klasse[k].append(rel)

    print(f"{genannt} Python-Dateien nennen `{STAMM}` ueberhaupt.\n")
    for klasse in reihenfolge:
        dateien = sorted(nach_klasse[klasse])
        if not dateien:
            continue
        print(f"{klasse}  ({len(dateien)})")
        print("-" * 72)
        for rel in dateien:
            print(f"  {rel}")
            if args.zeilen:
                for nr, zeile in treffer[rel].get(klasse, [])[:4]:
                    print(f"       {nr}: {zeile[:100]}")
        print()

    # Die neun Dateien selbst zaehlen nicht als Abhaengigkeit von aussen.
    kode = [r for r, k in treffer.items() if set(k) != {"ERWAEHNUNG"}]
    von_aussen = [r for r in kode
                  if not re.fullmatch(r"strategies/[a-z0-9_]+/equity_simulation\.py", r)]
    nur_prosa = genannt - len(kode)
    print(f"ZUSAMMEN: von {genannt} Dateien, die den Namen nennen, fassen "
          f"{len(kode)} ihn als Code an\n"
          f"          ({len(von_aussen)} davon von aussen, der Rest sind die "
          f"neun Dateien selbst);\n"
          f"          {nur_prosa} nennen ihn nur in Kommentar oder Text.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # Der Aufruf endete in `head` o. ae. - kein Fehler.
        os._exit(0)
