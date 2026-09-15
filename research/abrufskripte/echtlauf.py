#!/usr/bin/env python3
"""
Ein echter Abruf gegen den echten Endpunkt - ohne `data/` anzufassen (TB-35)
==============================================================================
Die Selbsttests in `shared/test_abrufschutz.py` laufen gegen Attrappen: der
Binance-Endpunkt und yfinance sind aus der Cloud gesperrt. Irgendwann muss
aber jemand nachsehen, ob die Absicherung auch gegen die **echte** Antwort
greift - und vor allem, ob `shared/fetch_binance_data.py` wirklich das
liefert, was `abrufschutz` von ihr annimmt. Diese Datei ist gitignoriert;
niemand ausser dem Betreiber kann sie lesen.

Das Problem dabei ist offensichtlich: ein echter Lauf eines Abrufskripts
**ueberschreibt Kursdateien**. Genau davor warnt TB-35. Ein Testlauf, der
dabei den Bestand vom 15.09.2026 anfasst, waere die Katastrophe, die er
verhindern soll.

Wie das hier geloest ist
------------------------------------------------------------------------------
Es wird ein **Miniatur-Abbild** des Projekts unter einem Wegwerf-Ordner
angelegt (`mktemp -d`, Rechte 0700). Die Abrufskripte rechnen ihren
`shared/`-Ordner aus der eigenen Lage aus - liegt eine Kopie des Skripts im
Abbild, findet sie dort ein `DATA_DIR`, das in den Wegwerf-Ordner zeigt.

    Kein Schreibzugriff auf `data/`. Nicht einer. Der echte Bestand wird
    ausschliesslich GELESEN, um das Ergebnis mit ihm zu vergleichen.

`shared/fetch_binance_data.py` wird dabei **nicht kopiert**. Das Abbild legt
dort nur eine Weiterleitung hin, die die echte Datei an ihrem Ort laedt - ihr
Inhalt wird nirgends dupliziert, nirgends ausgegeben und nirgends abgelegt.

Was der Lauf beantwortet
------------------------------------------------------------------------------
1. Laeuft das Abrufskript gegen den echten Endpunkt durch?
2. **Ist die letzte Zeile der erzeugten Datei eine abgeschlossene Kerze?**
   Das ist die eigentliche Frage von TB-35.
3. Stimmt das Erzeugte mit dem vorhandenen Bestand ueberein, soweit beide
   sich ueberschneiden - und kommt nur hinten etwas dazu?
4. Wuerde dieser Lauf eine Datei verkuerzen? (dieselbe Wache wie im Skript)

Rueckgabewert 0, wenn alles zusammenpasst; 1 bei Befund; 2 bei Bedienfehler.

    python3 research/abrufskripte/echtlauf.py \\
        --skript strategies/t3_supertrend/fetch_4h_data.py \\
        --symbole BTCUSDT,ETHUSDT

    python3 research/abrufskripte/echtlauf.py --alle-krypto --symbole BTCUSDT
    python3 research/abrufskripte/echtlauf.py \\
        --skript strategies/volatility_breakout/fetch_stock_data.py \\
        --symbole AAPL,MSFT --behalten
"""

import argparse
import datetime as dt
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))
_SHARED = os.path.join(_WURZEL, "shared")
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

import abrufschutz                                             # noqa: E402

KRYPTO = ["shared/fetch_multi_data.py",
          "strategies/t3_supertrend/fetch_4h_data.py",
          "strategies/rsi2_crypto/fetch_1d_data.py",
          "strategies/volatility_breakout_crypto/fetch_1d_data.py"]
AKTIEN = ["strategies/elliott_wave_stocks/fetch_stock_data.py",
          "strategies/rsi2_mean_reversion/fetch_stock_data.py",
          "strategies/turtle_soup_stocks/fetch_stock_data.py",
          "strategies/volatility_breakout/fetch_stock_data.py"]

# Keine Kopie, sondern eine Weiterleitung: die echte, gitignorierte Datei wird
# an ihrem Ort geladen. Ihr Inhalt verlaesst den Ordner nie.
WEITERLEITUNG = '''
"""Weiterleitung auf die echte, gitignorierte shared/fetch_binance_data.py.

Sie wird an ihrem Ort geladen - nicht kopiert, nicht ausgegeben, nirgends
abgelegt. Erzeugt von research/abrufskripte/echtlauf.py.
"""
import importlib.util
import os

_ECHT = os.path.join(os.environ["ECHTES_SHARED"], "fetch_binance_data.py")
if not os.path.exists(_ECHT):
    raise ImportError(
        f"{_ECHT} gibt es nicht. Die Datei ist gitignoriert und existiert nur "
        f"auf dem Rechner des Betreibers - in der Cloud kann dieser Lauf nicht "
        f"stattfinden.")

_spec = importlib.util.spec_from_file_location("_echte_fetch_binance_data", _ECHT)
_modul = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_modul)

fetch_historical_data = _modul.fetch_historical_data
'''

PATHS = 'import os\nDATA_DIR = os.environ["TEST_DATA_DIR"]\n'
STRATEGY_PATHS = '''
import os


def get_strategy_paths(datei=None):
    ordner = os.environ["TEST_DATA_DIR"]
    return {"DATA_DIR": ordner, "BASE_DIR": os.path.dirname(ordner),
            "RESULTS_DIR": ordner, "CONFIG_DIR": ordner,
            "LOGS_DIR": ordner, "STRATEGY_NAME": "probe",
            "DB_FILE": os.path.join(ordner, "probe.db")}
'''


def baue_abbild(wurzel, skripte, symbole):
    shared = os.path.join(wurzel, "shared")
    daten = os.path.join(wurzel, "data")
    os.makedirs(shared, exist_ok=True)
    os.makedirs(daten, exist_ok=True)

    for name in ("abrufschutz.py", "kursdaten.py", "binance_historie.py"):
        shutil.copy2(os.path.join(_SHARED, name), os.path.join(shared, name))

    def schreibe(pfad, inhalt):
        with open(pfad, "w", encoding="utf-8") as datei:
            datei.write(inhalt)

    schreibe(os.path.join(shared, "paths.py"), PATHS)
    schreibe(os.path.join(shared, "strategy_paths.py"), STRATEGY_PATHS)
    liste = "SYMBOLS = " + repr(list(symbole)) + "\n"
    schreibe(os.path.join(shared, "symbols_config.py"), liste)
    schreibe(os.path.join(shared, "stocks_symbols_config.py"), liste)
    schreibe(os.path.join(shared, "fetch_binance_data.py"), WEITERLEITUNG)

    for rel in skripte:
        ziel = os.path.join(wurzel, rel)
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        shutil.copy2(os.path.join(_WURZEL, rel), ziel)

    return daten


def starte(wurzel, rel, daten):
    umgebung = os.environ.copy()
    umgebung["TEST_DATA_DIR"] = daten
    umgebung["ECHTES_SHARED"] = _SHARED
    skript = os.path.join(wurzel, rel)
    lauf = subprocess.run([sys.executable, os.path.basename(skript)],
                          cwd=os.path.dirname(skript), env=umgebung,
                          capture_output=True, text=True, timeout=3600)
    return lauf.returncode, lauf.stdout + lauf.stderr


def _intervall_aus_name(name):
    for teil in ("_1h.csv", "_4h.csv", "_1d.csv"):
        if name.endswith(teil):
            return teil[1:3]
    return None


def _zeilen(pfad):
    with open(pfad, encoding="utf-8") as datei:
        return [z.rstrip("\n") for z in datei if z.strip()]


def pruefe_datei(neu_pfad, alt_pfad):
    """Was der echte Lauf erzeugt hat - und wie es zum Bestand passt."""
    import pandas as pd                                        # noqa: PLC0415

    name = os.path.basename(neu_pfad)
    intervall = _intervall_aus_name(name)
    ergebnis = {"datei": name, "befunde": []}

    neu = _zeilen(neu_pfad)
    ergebnis["zeilen"] = len(neu) - 1
    ergebnis["erste"] = neu[1].split(",")[0] if len(neu) > 1 else None
    ergebnis["letzte"] = neu[-1].split(",")[0] if len(neu) > 1 else None

    # DIE Frage von TB-35: ist die letzte Zeile ein abgeschlossener Zeitraum?
    if intervall and len(neu) > 1:
        probe = pd.DataFrame({"open_time": [ergebnis["letzte"]]})
        maske = abrufschutz.abgeschlossen_maske(probe, intervall)
        ergebnis["letzte_abgeschlossen"] = bool(maske.iloc[0])
        if not ergebnis["letzte_abgeschlossen"]:
            ergebnis["befunde"].append(
                f"die letzte Kerze ({ergebnis['letzte']}) ist zum jetzigen "
                f"Zeitpunkt NICHT abgeschlossen")
    else:
        ergebnis["letzte_abgeschlossen"] = None

    if not os.path.exists(alt_pfad):
        ergebnis["bestand"] = None
        return ergebnis

    alt = _zeilen(alt_pfad)
    ergebnis["bestand"] = {"zeilen": len(alt) - 1,
                           "erste": alt[1].split(",")[0] if len(alt) > 1 else None,
                           "letzte": alt[-1].split(",")[0] if len(alt) > 1 else None}

    if neu[0] != alt[0]:
        ergebnis["befunde"].append(
            f"die Kopfzeile weicht ab: {neu[0]!r} statt {alt[0]!r}")

    # Zeichengleich, soweit beide reichen? Ein Abruf, der vorhandene Zeilen
    # anders schreibt als sie dastehen, aendert den Datenstand-Hash - auch
    # wenn kein Kurs anders ist.
    gemeinsam = min(len(neu), len(alt))
    abweichend = [i for i in range(1, gemeinsam) if neu[i] != alt[i]]
    ergebnis["gemeinsame_zeilen"] = gemeinsam - 1
    ergebnis["abweichende_zeilen"] = len(abweichend)
    if abweichend:
        ergebnis["erste_abweichung"] = {
            "zeile": abweichend[0],
            "neu": neu[abweichend[0]][:70],
            "bestand": alt[abweichend[0]][:70]}
        # Die LETZTE Zeile des Bestands darf abweichen: sie kann noch die
        # Teilkerze aus der Zeit vor TB-35 sein.
        nur_am_rand = abweichend == [len(alt) - 1] and len(alt) <= len(neu)
        if nur_am_rand:
            ergebnis["befunde"].append(
                "nur die LETZTE Zeile des Bestands weicht ab - das ist die "
                "erwartete alte Teilkerze, kein Fehler")
        else:
            ergebnis["befunde"].append(
                f"{len(abweichend)} vorhandene Zeile(n) werden anders "
                f"geschrieben als sie dastehen (erste: Zeile {abweichend[0]})")

    vorher = abrufschutz.zustand(alt_pfad)
    nachher = abrufschutz.zustand(neu_pfad)
    for befund in abrufschutz.vergleiche({name: vorher}, {name: nachher}):
        ergebnis["befunde"].append(f"WACHE [{befund['art']}] {befund['text']}")

    return ergebnis


def berichte(skript, rc, ausgabe, dateien):
    print("\n" + "=" * 78)
    print(f"ECHTLAUF: {skript}")
    print("=" * 78)
    print(f"Rueckgabewert: {rc}")
    print("--- Ausgabe des Abrufskripts " + "-" * 49)
    for zeile in ausgabe.strip().splitlines()[-25:]:
        print("   " + zeile)
    print("-" * 78)

    if not dateien:
        print("Es wurde keine Datei erzeugt.")
        return 1

    schlecht = 0
    for eintrag in dateien:
        marke = "OK " if not eintrag["befunde"] else "!! "
        print(f"\n[{marke}] {eintrag['datei']}")
        print(f"        erzeugt : {eintrag['zeilen']} Zeilen, "
              f"{eintrag['erste']} .. {eintrag['letzte']}")
        if eintrag["bestand"]:
            b = eintrag["bestand"]
            print(f"        Bestand : {b['zeilen']} Zeilen, "
                  f"{b['erste']} .. {b['letzte']}")
            print(f"        gemeinsam {eintrag['gemeinsame_zeilen']} Zeile(n), "
                  f"davon {eintrag['abweichende_zeilen']} abweichend")
        else:
            print("        Bestand : (keine Entsprechung in data/)")
        print(f"        letzte Kerze abgeschlossen: "
              f"{eintrag['letzte_abgeschlossen']}")
        for befund in eintrag["befunde"]:
            print(f"        -> {befund}")
        if any(not b.startswith("nur die LETZTE") for b in eintrag["befunde"]):
            schlecht += 1

    print("\n" + "=" * 78)
    if schlecht:
        print(f"{schlecht} Datei(en) mit Befund. data/ wurde NICHT angefasst - "
              f"alles oben steht im Wegwerf-Ordner.")
        return 1
    print("Kein Befund: jede erzeugte Datei endet auf einer abgeschlossenen "
          "Kerze,\nund der vorhandene Bestand wird zeichengleich "
          "wiedergegeben.")
    return 0


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Laesst ein Abrufskript GEGEN DEN ECHTEN ENDPUNKT laufen, "
                    "aber in einen Wegwerf-Ordner statt nach data/.")
    zerleger.add_argument("--skript", action="append", default=None,
                          help="Pfad relativ zur Repo-Wurzel (mehrfach angebbar)")
    zerleger.add_argument("--alle-krypto", action="store_true")
    zerleger.add_argument("--alle-aktien", action="store_true")
    zerleger.add_argument("--symbole", default="BTCUSDT",
                          help="Kommaliste, Voreinstellung BTCUSDT")
    zerleger.add_argument("--behalten", action="store_true",
                          help="Wegwerf-Ordner nicht loeschen")
    argumente = zerleger.parse_args(argv)

    skripte = list(argumente.skript or [])
    if argumente.alle_krypto:
        skripte += KRYPTO
    if argumente.alle_aktien:
        skripte += AKTIEN
    skripte = sorted(set(skripte))
    if not skripte:
        print("Kein Skript angegeben (--skript / --alle-krypto / --alle-aktien).",
              file=sys.stderr)
        return 2
    for rel in skripte:
        if not os.path.exists(os.path.join(_WURZEL, rel)):
            print(f"Kein solches Skript: {rel}", file=sys.stderr)
            return 2

    symbole = [s.strip() for s in argumente.symbole.split(",") if s.strip()]
    if not symbole:
        print("Keine Symbole angegeben.", file=sys.stderr)
        return 2

    # Lieber hier klar scheitern als spaeter mit einem Traceback im Protokoll
    # des Abrufskripts. In der Cloud fehlen beide Bibliotheken, und
    # shared/fetch_binance_data.py gibt es dort ueberhaupt nicht.
    fehlt = []
    if any(rel in KRYPTO for rel in skripte):
        try:
            import binance                                     # noqa: F401,PLC0415
        except ImportError:
            fehlt.append("das Paket `binance` (pip3 install python-binance)")
        if not os.path.exists(os.path.join(_SHARED, "fetch_binance_data.py")):
            fehlt.append("shared/fetch_binance_data.py - die gitignorierte "
                         "Datei; dieser Lauf geht nur auf dem Rechner des "
                         "Betreibers")
    if any(rel in AKTIEN for rel in skripte):
        try:
            import yfinance                                    # noqa: F401,PLC0415
        except ImportError:
            fehlt.append("das Paket `yfinance` (pip3 install yfinance)")
    if fehlt:
        print("Dieser Lauf braucht den echten Endpunkt. Es fehlt:",
              file=sys.stderr)
        for eintrag in fehlt:
            print(f"  - {eintrag}", file=sys.stderr)
        print("\nIn der Cloud ist das erwartet: Binance und yfinance sind "
              "dort gesperrt (403).\nDieser Schritt gehoert auf den Mac.",
              file=sys.stderr)
        return 2

    wurzel = tempfile.mkdtemp(prefix="tb35_echtlauf_")
    os.chmod(wurzel, 0o700)
    print(f"Wegwerf-Ordner: {wurzel}")
    print(f"Symbole: {', '.join(symbole)}")
    print("data/ wird in diesem Lauf ausschliesslich GELESEN.\n")

    schlimmstes = 0
    try:
        daten = baue_abbild(wurzel, skripte, symbole)
        for rel in skripte:
            for name in os.listdir(daten):
                os.remove(os.path.join(daten, name))
            begonnen = dt.datetime.now()
            rc, ausgabe = starte(wurzel, rel, daten)
            dauer = (dt.datetime.now() - begonnen).total_seconds()
            dateien = []
            for name in sorted(os.listdir(daten)):
                if not name.endswith(".csv"):
                    continue
                dateien.append(pruefe_datei(
                    os.path.join(daten, name),
                    os.path.join(_WURZEL, "data", name)))
            schlimmstes = max(schlimmstes, berichte(rel, rc, ausgabe, dateien))
            print(f"(Dauer: {dauer:.1f} s)")
    finally:
        if argumente.behalten:
            print(f"\nWegwerf-Ordner bleibt stehen: {wurzel}")
            print("Zum Aufraeumen:  rm -rf " + wurzel)
        else:
            shutil.rmtree(wurzel, ignore_errors=True)
            print(f"\nWegwerf-Ordner geloescht: {wurzel}")

    return schlimmstes


if __name__ == "__main__":
    sys.exit(main())
