#!/usr/bin/env python3
"""
Wer liest `data/`, wer holt live, wer schreibt hinein? (TB-34)
==============================================================================
Der Auftrag von TB-34 stellt eine Frage, die bisher niemand beantwortet hat:

    Woher holen die neun `forward_test.py` ihre Daten - live, aus `data/`,
    oder gemischt? Und welche Programme lesen `data/`, rechnen also auf dem
    Stand des letzten Abrufs von Hand?

Diese Untersuchung beantwortet sie **mechanisch** statt aus dem Gedaechtnis.
Sie liest den Quelltext, nicht die Dokumentation - eine Liste von Hand waere
am Tag nach der naechsten Aenderung falsch, ohne dass es auffiele. Genau
dieses Muster hat das Projekt bei den Ergebniskurven schon einmal
eingesammelt (`shared/ergebniskurven.py`, Protokoll 4.2).

Was als was gilt
------------------------------------------------------------------------------
* **liest data/** - irgendwo im Modul steht ein `pandas.read_csv(...)`, dessen
  Pfadausdruck `DATA_DIR` enthaelt (auch in der Form `_P["DATA_DIR"]`).
* **schreibt data/** - ein `to_csv(...)` auf einen Pfad, der aus `DATA_DIR`
  gebaut ist; auch ueber eine Zwischenvariable (`output_file = os.path.join(
  DATA_DIR, ...)`), weil genau so die Abrufskripte geschrieben sind.
* **holt live** - das Modul bindet `fetch_historical_data` ein (aus
  `fetch_binance_data` oder `fetch_stock_data`) oder importiert `yfinance`
  bzw. `binance.client` unmittelbar.
* **mittelbar** - das Modul importiert `load_all_symbol_data` aus einem
  `multi_symbol_optimise`. Diese Funktion ist der Trichter, durch den in
  diesem Projekt fast alles an die Kursdateien kommt: Equity-Simulationen,
  Walk-Forwards, Determinismuslaeufe und der Grossteil der Untersuchungen
  unter `research/`. Wer sie aufruft, rechnet auf `data/`, auch wenn im
  eigenen Quelltext kein `read_csv` steht - und genau deshalb ist die Zahl
  der **mittelbaren** Leser die Zahl, um die es geht.

Gesucht wird ueber den **Syntaxbaum**, nicht mit Textsuche: ein `read_csv` in
einem Kommentar oder einem Zeichenkettenliteral soll nicht mitzaehlen.

Die Untersuchung fasst **keinen** Bot-Code an und aendert nichts. Sie braucht
nur die Standardbibliothek.

    python3 research/kursdaten_neuaufbau/datenwege.py
    python3 research/kursdaten_neuaufbau/datenwege.py --json daten/datenwege.json

Rueckgabewert 0. Sie ist ein Bericht, kein Waechter.
"""

import argparse
import ast
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))

ORDNER = ["shared", "strategies", "research", "dashboard", "notifications",
          "broker", "system", "config"]

LIVE_MODULE = {"yfinance", "binance", "binance.client"}
TRICHTER = "load_all_symbol_data"
LIVE_FUNKTIONEN = {"fetch_historical_data"}
DATA_MARKER = "DATA_DIR"


def quelle(knoten, text):
    ausschnitt = ast.get_source_segment(text, knoten)
    return ausschnitt or ""


def untersuche(pfad):
    """Ein Modul -> was es mit Kursdaten tut."""
    with open(pfad, "r", encoding="utf-8") as datei:
        text = datei.read()
    try:
        baum = ast.parse(text)
    except SyntaxError as fehler:
        return {"fehler": f"nicht parsbar: {fehler}"}

    liest, schreibt, live, mittelbar = [], [], [], []
    # Variablen, die aus DATA_DIR gebaut wurden - die Abrufskripte legen den
    # Zielpfad erst in eine Variable und geben die dann an `to_csv`.
    aus_data_dir = set()

    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Assign):
            rechts = quelle(knoten.value, text)
            if DATA_MARKER in rechts:
                for ziel in knoten.targets:
                    if isinstance(ziel, ast.Name):
                        aus_data_dir.add(ziel.id)

        if isinstance(knoten, (ast.Import, ast.ImportFrom)):
            namen = ([a.name for a in knoten.names] if isinstance(knoten, ast.Import)
                     else [knoten.module or ""] + [a.name for a in knoten.names])
            for name in namen:
                wurzel = (name or "").split(".")[0]
                if name in LIVE_MODULE or wurzel in LIVE_MODULE:
                    live.append(f"import {name} (Zeile {knoten.lineno})")
                if name in LIVE_FUNKTIONEN:
                    live.append(f"{name} (Zeile {knoten.lineno})")
                if name == TRICHTER:
                    mittelbar.append(f"{TRICHTER} (Zeile {knoten.lineno})")

        if isinstance(knoten, ast.Call):
            name = (knoten.func.attr if isinstance(knoten.func, ast.Attribute)
                    else getattr(knoten.func, "id", ""))
            if name not in ("read_csv", "to_csv"):
                continue
            argumente = list(knoten.args)
            erstes = quelle(argumente[0], text) if argumente else ""
            trifft = (DATA_MARKER in erstes
                      or (isinstance(argumente[0], ast.Name)
                          and argumente[0].id in aus_data_dir if argumente else False))
            if not trifft:
                continue
            eintrag = f"Zeile {knoten.lineno}: {erstes[:60]}"
            (liest if name == "read_csv" else schreibt).append(eintrag)

    return {"liest": liest, "schreibt": schreibt, "live": sorted(set(live)),
            "mittelbar": sorted(set(mittelbar)), "fehler": None}


def sammle(wurzel=_WURZEL, ordner=None):
    befunde = {}
    for teil in (ordner or ORDNER):
        for pfad, _, dateien in os.walk(os.path.join(wurzel, teil)):
            if "__pycache__" in pfad:
                continue
            for name in sorted(dateien):
                if not name.endswith(".py"):
                    continue
                voll = os.path.join(pfad, name)
                ergebnis = untersuche(voll)
                if ergebnis.get("fehler"):
                    continue
                if (ergebnis["liest"] or ergebnis["schreibt"]
                        or ergebnis["live"] or ergebnis["mittelbar"]):
                    befunde[os.path.relpath(voll, wurzel)] = ergebnis
    return befunde


def datenstand(wurzel=_WURZEL):
    """Der juengste Zeitstempel je Kursdatei - der wirkliche Stand von `data/`.

    Nicht `mtime`: ein frischer Klon setzt die Dateizeiten auf den Klonzeitpunkt.
    Der letzte Zeitstempel IN der Datei ist die Aussage, um die es geht.
    """
    ordner = os.path.join(wurzel, "data")
    je_tag = {}
    for name in sorted(os.listdir(ordner)):
        if not name.endswith(".csv"):
            continue
        pfad = os.path.join(ordner, name)
        with open(pfad, "rb") as datei:
            groesse = os.path.getsize(pfad)
            datei.seek(max(0, groesse - 200))
            zeilen = datei.read().decode("utf-8", "replace").strip().splitlines()
        if not zeilen:
            continue
        tag = zeilen[-1].split(",")[0][:10]
        je_tag.setdefault(tag, []).append(name)
    return je_tag


def berichte(befunde, stand):
    leser = {k: v for k, v in befunde.items() if v["liest"]}
    schreiber = {k: v for k, v in befunde.items() if v["schreibt"]}
    live = {k: v for k, v in befunde.items() if v["live"]}
    mittelbar = {k: v for k, v in befunde.items()
                 if v["mittelbar"] and not v["liest"]}
    forward = {k: v for k, v in befunde.items()
               if os.path.basename(k) == "forward_test.py"}

    print("=" * 78)
    print("DATENWEGE - wer liest data/, wer holt live, wer schreibt hinein")
    print("=" * 78)

    print("\n1. DER STAND VON data/ (juengster Zeitstempel IN den Dateien)")
    for tag, dateien in sorted(stand.items()):
        print(f"   {tag}   {len(dateien):>3} Datei(en)")

    print(f"\n2. DIE NEUN forward_test.py ({len(forward)} gefunden)")
    for pfad in sorted(forward):
        eintrag = forward[pfad]
        weg = "LIVE" if eintrag["live"] else "?"
        if eintrag["liest"]:
            weg = "LIVE + liest data/" if eintrag["live"] else "liest data/"
        print(f"   {os.path.dirname(pfad).split(os.sep)[-1]:<28} {weg}")
    ohne_data = [p for p in forward if not forward[p]["liest"]]
    print(f"   -> {len(ohne_data)} von {len(forward)} lesen KEINE Datei aus data/.")

    print(f"\n3. WER data/ LIEST - und damit auf dem Stand von oben rechnet "
          f"({len(leser)} Module)")
    for pfad in sorted(leser):
        print(f"   {pfad}")
        for stelle in leser[pfad]["liest"][:2]:
            print(f"        {stelle}")
        if len(leser[pfad]["liest"]) > 2:
            print(f"        ... und {len(leser[pfad]['liest']) - 2} weitere Stelle(n)")

    print(f"\n3b. WER MITTELBAR AUF data/ RECHNET - ueber "
          f"{TRICHTER}() ({len(mittelbar)} weitere Module)")
    print("    Ihr eigener Quelltext enthaelt kein read_csv auf data/; sie")
    print("    holen die Kursdaten ueber den gemeinsamen Trichter.")
    nach_ordner = {}
    for pfad in sorted(mittelbar):
        nach_ordner.setdefault(pfad.split(os.sep)[0], []).append(pfad)
    for ordner, pfade in sorted(nach_ordner.items()):
        print(f"    {ordner + '/':<14} {len(pfade):>3} Modul(e)")

    print(f"\n4. WER data/ SCHREIBT ({len(schreiber)} Module)")
    for pfad in sorted(schreiber):
        print(f"   {pfad}")
        for stelle in schreiber[pfad]["schreibt"][:2]:
            print(f"        {stelle}")

    print(f"\n5. WER LIVE HOLT, OHNE data/ ANZUFASSEN "
          f"({len([p for p in live if not befunde[p]['liest'] and not befunde[p]['schreibt']])} Module)")
    for pfad in sorted(live):
        if befunde[pfad]["liest"] or befunde[pfad]["schreibt"]:
            continue
        print(f"   {pfad}: {', '.join(befunde[pfad]['live'][:2])}")

    print("\n" + "=" * 78)
    print(f"Zusammenfassung: {len(leser)} Module lesen data/ unmittelbar, "
          f"{len(mittelbar)} weitere")
    print(f"ueber {TRICHTER}() - zusammen {len(leser) + len(mittelbar)}. "
          f"{len(schreiber)} Module schreiben")
    print(f"nach data/, {len(live)} holen live.")


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Listet mechanisch auf, welche Module Kursdaten aus data/ "
                    "lesen, dorthin schreiben oder live holen.")
    zerleger.add_argument("--wurzel", default=_WURZEL)
    zerleger.add_argument("--json", default=None)
    argumente = zerleger.parse_args(argv)

    befunde = sammle(argumente.wurzel)
    stand = datenstand(argumente.wurzel)
    berichte(befunde, stand)

    if argumente.json:
        ziel = (argumente.json if os.path.isabs(argumente.json)
                else os.path.join(_HIER, argumente.json))
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump({"datenstand": stand, "module": befunde}, datei,
                      indent=2, ensure_ascii=False, sort_keys=True)
        print(f"\nJSON: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
