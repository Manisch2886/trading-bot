#!/usr/bin/env python3
"""
Wer haengt an `shared/fetch_binance_data.py`? (TB-35)
==============================================================================
Diese Datei ist **gitignoriert**. Sie enthaelt Zugangsdaten und existiert nur
auf dem Rechner des Betreibers. Weder TB-34 noch TB-35 konnten sie lesen; was
sie tut, ist ausschliesslich aus ihrem Ergebnis erschlossen.

Das ist unangenehm, weil sie der **einzige** Weg ist, auf dem Krypto-Kursdaten
in dieses Projekt kommen - fuer die Abrufskripte ebenso wie fuer die Bots im
Live-Betrieb. Wer von ihr abhaengt, soll deshalb nicht aus dem Gedaechtnis
aufgezaehlt werden, sondern mechanisch: eine Liste von Hand waere am Tag nach
der naechsten Aenderung falsch, ohne dass es auffiele. Dasselbe Vorgehen wie
in `research/kursdaten_neuaufbau/datenwege.py`.

Gesucht wird ueber den **Syntaxbaum**, nicht mit Textsuche: ein Name in einem
Kommentar oder einer Zeichenkette soll nicht mitzaehlen.

Was die Untersuchung feststellt
------------------------------------------------------------------------------
1. **Wer sie einbindet** - und in welcher Zeile.
2. **Was der Aufrufer mit dem Ergebnis macht** - schreibt er es nach `data/`,
   oder haengt eine Handelsentscheidung daran (`df.iloc[-1]`)? Das ist der
   Unterschied zwischen "eine CSV ist falsch" und "ein Bot handelt falsch".
3. **Welche Spalten er voraussetzt** - der stillschweigende Vertrag mit einer
   Datei, die niemand nachlesen kann.

Die Untersuchung aendert nichts und fasst keinen Bot-Code an. Sie braucht nur
die Standardbibliothek. Rueckgabewert 0 - sie ist ein Bericht, kein Waechter.

    python3 research/abrufskripte/abrufwege.py
    python3 research/abrufskripte/abrufwege.py --json daten/abrufwege.json
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

MODUL = "fetch_binance_data"
FUNKTION = "fetch_historical_data"
KURSSPALTEN = ["open_time", "open", "high", "low", "close", "volume",
               "close_time"]
DATA_MARKER = "DATA_DIR"

# Die Zusicherungen, die an dieser Datei haengen. Sie stehen hier als Text,
# weil sie sich NICHT aus dem Quelltext der Aufrufer ablesen lassen - genau
# das ist der Punkt: sie sind vorausgesetzt, nicht gepruft.
ZUSICHERUNGEN = [
    ("Spalten", "Das Ergebnis hat open_time/open/high/low/close/volume - "
                "und KEINE close_time. Nachgerechnet an den Kursdateien "
                "selbst, nicht an der Quelle."),
    ("Reihenfolge", "Die Zeilen stehen aufsteigend nach open_time. Jeder "
                    "Aufrufer, der df.iloc[-1] als 'die juengste Kerze' liest, "
                    "setzt das voraus."),
    ("Raster", "Die open_time-Werte liegen auf dem Raster des angefragten "
               "Intervalls, ohne Doppelungen. shared/zeitabdeckung.py prueft "
               "das an den fertigen Dateien nach - nicht an der Antwort."),
    ("Schreibweise", "Zeitstempel als 'YYYY-MM-DD HH:MM:SS' bzw. 'YYYY-MM-DD' "
                     "bei Tageskerzen. Aendert sie sich, aendert sich der "
                     "Datenstand-Hash, ohne dass ein Kurs anders waere."),
    ("Vollstaendigkeit", "Das LOOKBACK-Argument wird als 'ab diesem Zeitpunkt' "
                         "gelesen und liefert alles Vorhandene, auch ueber die "
                         "1000-Kerzen-Grenze des Endpunkts hinaus."),
    ("Laufende Kerze", "Sie IST im Ergebnis enthalten. Das ist der Befund, der "
                       "TB-35 ausgeloest hat - erschlossen aus den Dateien, "
                       "nicht aus der Quelle."),
]


def quelle(knoten, text):
    return ast.get_source_segment(text, knoten) or ""


def untersuche(pfad):
    with open(pfad, "r", encoding="utf-8") as datei:
        text = datei.read()
    try:
        baum = ast.parse(text)
    except SyntaxError:
        return None

    bindet_ein = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.ImportFrom) and (knoten.module or "").endswith(MODUL):
            namen = ", ".join(a.name for a in knoten.names)
            bindet_ein.append(f"Zeile {knoten.lineno}: from {knoten.module} "
                              f"import {namen}")
        elif isinstance(knoten, ast.Import):
            for eintrag in knoten.names:
                if eintrag.name.endswith(MODUL):
                    bindet_ein.append(f"Zeile {knoten.lineno}: import "
                                      f"{eintrag.name}")
    if not bindet_ein:
        return None

    aus_data_dir = set()
    schreibt, aufrufe, letzte_kerze = [], [], []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Assign):
            if DATA_MARKER in quelle(knoten.value, text):
                for ziel in knoten.targets:
                    if isinstance(ziel, ast.Name):
                        aus_data_dir.add(ziel.id)

        if isinstance(knoten, ast.Call):
            name = (knoten.func.attr if isinstance(knoten.func, ast.Attribute)
                    else getattr(knoten.func, "id", ""))
            if name == FUNKTION:
                aufrufe.append(f"Zeile {knoten.lineno}")
            if name == "to_csv" and knoten.args:
                erstes = quelle(knoten.args[0], text)
                if (DATA_MARKER in erstes
                        or (isinstance(knoten.args[0], ast.Name)
                            and knoten.args[0].id in aus_data_dir)):
                    schreibt.append(f"Zeile {knoten.lineno}")

        # df.iloc[-1] - daran haengt in den forward_test.py die
        # Handelsentscheidung.
        if isinstance(knoten, ast.Subscript):
            if (isinstance(knoten.value, ast.Attribute)
                    and knoten.value.attr == "iloc"):
                stelle = quelle(knoten.slice, text).strip()
                if stelle in ("-1", "- 1"):
                    letzte_kerze.append(f"Zeile {knoten.lineno}: "
                                        f"{quelle(knoten, text)[:40]}")

    spalten = set()
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Constant) and isinstance(knoten.value, str):
            if knoten.value in KURSSPALTEN:
                spalten.add(knoten.value)

    return {"bindet_ein": bindet_ein, "aufrufe": sorted(set(aufrufe)),
            "schreibt_data": sorted(set(schreibt)),
            "letzte_kerze": sorted(set(letzte_kerze))[:3],
            "spalten": sorted(spalten)}


def sammle(wurzel=_WURZEL):
    befunde = {}
    for teil in ORDNER:
        ordner = os.path.join(wurzel, teil)
        if not os.path.isdir(ordner):
            continue
        for pfad, _, dateien in os.walk(ordner):
            if "__pycache__" in pfad:
                continue
            for name in sorted(dateien):
                if not name.endswith(".py"):
                    continue
                voll = os.path.join(pfad, name)
                ergebnis = untersuche(voll)
                if ergebnis:
                    befunde[os.path.relpath(voll, wurzel)] = ergebnis
    return befunde


def berichte(befunde):
    schreiber = {p: e for p, e in befunde.items() if e["schreibt_data"]}
    handelnde = {p: e for p, e in befunde.items() if e["letzte_kerze"]}
    stubs = {p for p in befunde if os.sep + "stubs" + os.sep in p}

    print("=" * 78)
    print(f"WER HAENGT AN shared/{MODUL}.py - der Datei, die nicht im Repo liegt")
    print("=" * 78)
    print(f"\n{len(befunde)} Modul(e) binden sie ein.\n")

    print("1. WER SIE EINBINDET")
    for pfad in sorted(befunde):
        hinweis = "   (Attrappe)" if pfad in stubs else ""
        print(f"   {pfad}{hinweis}")
        for zeile in befunde[pfad]["bindet_ein"]:
            print(f"        {zeile}")

    print(f"\n2. WAS MIT DEM ERGEBNIS GESCHIEHT")
    print(f"   a) nach data/ geschrieben ({len(schreiber)} Modul(e)) - hier "
          f"landet ein Fehler")
    print(f"      dauerhaft in einer Datei:")
    for pfad in sorted(schreiber):
        print(f"        {pfad}   ({', '.join(schreiber[pfad]['schreibt_data'])})")
    print(f"\n   b) als juengste Kerze in eine Entscheidung ({len(handelnde)} "
          f"Modul(e)) - hier")
    print(f"      haengt das Handeln eines Bots daran:")
    for pfad in sorted(handelnde):
        print(f"        {pfad}")
        for stelle in handelnde[pfad]["letzte_kerze"]:
            print(f"             {stelle}")

    print("\n3. WELCHE SPALTEN VORAUSGESETZT WERDEN")
    alle = sorted({s for e in befunde.values() for s in e["spalten"]})
    print(f"   Im Quelltext der Aufrufer kommen vor: "
          f"{', '.join(alle) if alle else '(keine namentlich)'}")
    fehlend = [s for s in ("close_time",) if s not in alle]
    if fehlend:
        print(f"   NICHT benutzt: {', '.join(fehlend)} - der Wert, an dem der "
              f"Endpunkt selbst")
        print(f"   sagt, ob eine Kerze fertig ist. Er kommt in der Antwort "
              f"dieser Datei nicht an;")
        print(f"   shared/abrufschutz.py rechnet den Schluss deshalb aus "
              f"open_time und Intervall.")

    print("\n4. ZUSICHERUNGEN, DIE AN DIESER DATEI HAENGEN")
    print("   Keine davon ist im Repo nachpruefbar - die Quelle liegt "
          "ausserhalb.")
    for titel, text in ZUSICHERUNGEN:
        print(f"\n   {titel}:")
        for zeile in _umbruch(text, 68):
            print(f"      {zeile}")

    print("\n" + "=" * 78)
    print(f"Zusammenfassung: {len(befunde)} Module haengen an einer Datei, die "
          f"genau einmal")
    print(f"existiert - auf einem Rechner, ungesichert und unversioniert. "
          f"{len(schreiber)} davon")
    print(f"schreiben ihr Ergebnis nach data/, {len(handelnde)} lassen eine "
          f"Handelsentscheidung")
    print("davon abhaengen.")


def _umbruch(text, breite):
    worte = text.split()
    zeilen, laufend = [], ""
    for wort in worte:
        if len(laufend) + len(wort) + 1 > breite:
            zeilen.append(laufend)
            laufend = wort
        else:
            laufend = f"{laufend} {wort}".strip()
    if laufend:
        zeilen.append(laufend)
    return zeilen


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description=f"Listet mechanisch auf, welche Module an "
                    f"shared/{MODUL}.py haengen.")
    zerleger.add_argument("--wurzel", default=_WURZEL)
    zerleger.add_argument("--json", default=None)
    argumente = zerleger.parse_args(argv)

    befunde = sammle(argumente.wurzel)
    berichte(befunde)

    if argumente.json:
        ziel = (argumente.json if os.path.isabs(argumente.json)
                else os.path.join(_HIER, argumente.json))
        if os.path.dirname(ziel):
            os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump({"module": befunde,
                       "zusicherungen": dict(ZUSICHERUNGEN)},
                      datei, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"\nJSON: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
