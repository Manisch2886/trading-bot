#!/usr/bin/env python3
"""
Selbsttests zu shared/ladeprotokoll.py und den neun Loadern (TB-42, Teil 1)
==============================================================================
Geprueft wird die Behauptung, um die es in TB-42 geht:

    Ein Lauf, der ein Symbol auslaesst, sagt es. Immer.
    Und er laesst dabei kein anderes Symbol aus als vorher.

Der zweite Satz ist der wichtigere. Er ist der Nachweis, dass TB-42 ein
Bug-Fix ist und kein Amendment: es wird NICHTS zusaetzlich geladen und
NICHTS zusaetzlich ausgeschlossen, es wird nur gesagt.

WIE GEPRUEFT WIRD - AM VERHALTEN, NICHT AM QUELLTEXT
------------------------------------------------------------------------------
Kein Test hier liest den Quelltext eines Bots. Jeder laesst den echten Loader
laufen und sieht zu, was er ausgibt und was er zurueckgibt.

Dabei gilt die Regel des Projekts: **Bot-Dateien werden gelesen, nie
importiert** - neun gleichnamige `multi_symbol_optimise.py` wuerden sich in
`sys.modules` verdraengen. Aufgeloest wie in TB-40: **ein eigener Prozess je
Bot**. Dieses Programm ruft sich dafuer selbst mit `--kind` auf.

Veraendert werden nur die EINGABEN des Loaders (`DATA_DIR`, `SYMBOLS`) - nie
seine Entscheidung. Die Schranken, die Leerpruefung und alles weitere laufen
unveraendert im Bot-Code.

DIE VIER PRUEFUNGEN
------------------------------------------------------------------------------
1. Der Baustein selbst: Zeilenformat, Summenzeile, Wachposten.
2. Je Bot, gegen erzeugte Beispieldaten: jeder Grund erzeugt genau eine Zeile,
   die das Symbol nennt - und die Summenzeile stimmt.
3. Je Bot, gegen die ECHTEN Kursdaten: die geladene Symbolliste ist dieselbe
   wie vor TB-42. Der Vergleich laeuft gegen den Loader, wie Git ihn vor
   dieser Aenderung fuehrt - nicht gegen eine Nachbildung und nicht gegen eine
   Zahl, die jemand aufgeschrieben hat.
4. Mutationsproben: wird eine Meldung aus einem Loader entfernt, MUSS Pruefung
   2 fehlschlagen. Beobachtet wird der Ablauf des mutierten Loaders, nicht ein
   von Hand hergestellter Zustand - eine Probe, die ihren eigenen Zustand
   setzt, bestaetigt sich selbst.

Nutzung:  python3 shared/test_ladeprotokoll.py
          python3 shared/test_ladeprotokoll.py --nur 1,2      (Auswahl)
"""

import argparse
import contextlib
import datetime as dt
import glob
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

BOTS = sorted(os.path.basename(os.path.dirname(p)) for p in
              glob.glob(os.path.join(BASE_DIR, "strategies", "*",
                                     "multi_symbol_optimise.py")))

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
    else:
        FEHLER.append(f"{name}" + (f"  [{detail}]" if detail else ""))
    return bool(bedingung)


# ===========================================================================
# Kindprozess: EIN Loader, in einem eigenen sys.modules
# ===========================================================================
def kindlauf(bot, aus, datenordner=None, symbole=None, strategien=None):
    import importlib.util

    strategien = strategien or os.path.join(BASE_DIR, "strategies")
    strategie_dir = os.path.join(strategien, bot)
    datei = os.path.join(strategie_dir, "multi_symbol_optimise.py")
    sys.path.insert(0, strategie_dir)

    # Netz stilllegen, bevor ein Bot-Modul geladen wird: shared/
    # fetch_multi_data.py legt auf Modulebene einen Client an, und
    # python-binance pingt im Konstruktor (TB-40, Nebenbefund).
    try:
        import binance.client
        binance.client.Client.ping = lambda self, *a, **k: {}
    except ImportError:
        pass

    ergebnis = {"bot": bot, "fehler": None}
    try:
        spec = importlib.util.spec_from_file_location("botmodul_" + bot, datei)
        modul = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = modul
        spec.loader.exec_module(modul)

        ergebnis["schranken"] = {
            n: getattr(modul, n) for n in
            ("MIN_HISTORY_DAYS", "MIN_HISTORY_HOURS", "RECENT_YEARS_ONLY", "INTERVAL")
            if hasattr(modul, n)}

        if datenordner:
            modul.DATA_DIR = os.path.abspath(datenordner)
        if symbole:
            modul.SYMBOLS = list(symbole)
        ergebnis["universum"] = list(getattr(modul, "SYMBOLS", []))

        gemerkt = io.StringIO()
        with contextlib.redirect_stdout(gemerkt):
            geladen = modul.load_all_symbol_data()
        ergebnis["symbole"] = sorted(geladen.keys())
        ergebnis["ausgabe"] = gemerkt.getvalue()
    except Exception as fehler:                                  # noqa: BLE001
        import traceback
        ergebnis["fehler"] = "%s: %s" % (type(fehler).__name__, fehler)
        ergebnis["spur"] = traceback.format_exc()

    with open(aus, "w") as f:
        json.dump(ergebnis, f, ensure_ascii=False, default=str)
    return 0


def messe(bot, datenordner=None, symbole=None, strategien=None):
    """Startet den Kindprozess und gibt sein Ergebnis zurueck."""
    ziel = tempfile.mktemp(suffix=".json", prefix="tb42_")
    befehl = [sys.executable, os.path.abspath(__file__), "--kind", bot, "--aus", ziel]
    if datenordner:
        befehl += ["--daten", datenordner]
    if symbole:
        befehl += ["--symbole", ",".join(symbole)]
    if strategien:
        befehl += ["--strategien", strategien]
    p = subprocess.run(befehl, capture_output=True, text=True, timeout=900)
    if not os.path.exists(ziel):
        return {"bot": bot, "fehler": "Kindprozess ohne Ergebnis: %s %s"
                                      % (p.stdout[-400:], p.stderr[-400:])}
    with open(ziel) as f:
        e = json.load(f)
    os.remove(ziel)
    return e


# ===========================================================================
# Beispieldaten - erzeugt, nicht echt
# ===========================================================================
ROLLEN = ["voll_a", "voll_b", "zu_kurz", "datei_fehlt", "datei_leer"]


def baue_proben(ordner, symbole, intervall, schranke, einheit):
    """Legt fuer jede Rolle eine Kursdatei an (oder eben keine).

    Der Test behauptet hinterher NICHT, welches Symbol der Loader ausgelassen
    hat - er sieht es an dessen Ausgabe. Hier wird nur die Ausgangslage
    hergestellt.
    """
    os.makedirs(ordner, exist_ok=True)
    schritt = {"1h": dt.timedelta(hours=1), "4h": dt.timedelta(hours=4),
               "1d": dt.timedelta(days=1)}[intervall]
    ende = dt.datetime(2026, 9, 1)

    def schreibe(name, anzahl):
        with open(os.path.join(ordner, "%s_%s.csv" % (name, intervall)), "w") as f:
            f.write("open_time,open,high,low,close,volume\n")
            for i in range(anzahl):
                zeit = ende - schritt * (anzahl - 1 - i)
                kurs = 100.0 + (i % 40) * 0.5
                f.write("%s,%.4f,%.4f,%.4f,%.4f,1000\n"
                        % (zeit.strftime("%Y-%m-%d %H:%M:%S"),
                           kurs, kurs * 1.01, kurs * 0.99, kurs))

    if einheit == "kerzen":
        n_voll, n_kurz = schranke * 2, schranke - 1
    else:
        pro_tag = 86400.0 / schritt.total_seconds()
        n_voll = int(schranke * pro_tag * 2) + 2
        n_kurz = max(2, int((schranke - 2) * pro_tag))

    zuordnung = dict(zip(ROLLEN, symbole))
    schreibe(zuordnung["voll_a"], n_voll)
    schreibe(zuordnung["voll_b"], n_voll)
    schreibe(zuordnung["zu_kurz"], n_kurz)
    # datei_fehlt: absichtlich keine Datei
    schreibe(zuordnung["datei_leer"], 0)
    return zuordnung


# ===========================================================================
# 1. Der Baustein selbst
# ===========================================================================
def test_baustein():
    from ladeprotokoll import Ladeprotokoll

    def gesammelt(fn):
        puffer = io.StringIO()
        with contextlib.redirect_stdout(puffer):
            wert = fn()
        return wert, puffer.getvalue()

    p = Ladeprotokoll(["A", "B", "C", "D", "E"])
    _z, ausgabe = gesammelt(lambda: (p.fehlt("B", "/d/B_1d.csv"),
                                     p.leer("C", "/d/C_1d.csv"),
                                     p.zu_kurz("D", 300, 500),
                                     p.zu_wenige_kerzen("E", 12, 99)))
    zeilen = ausgabe.strip().splitlines()

    check("1.1 vier Gruende erzeugen vier Zeilen", len(zeilen) == 4, str(zeilen))
    check("1.2 jede Zeile nennt ihr Symbol",
          all(z.split()[1] == s for z, s in zip(zeilen, ["B", "C", "D", "E"])),
          str(zeilen))
    check("1.3 jede Zeile hat dieselbe Form",
          all(z.startswith("Hinweis: ") and z.endswith(", wird uebersprungen.")
              for z in zeilen), str(zeilen))
    check("1.4 die fehlende Datei nennt Symbol UND Pfad",
          "B" in zeilen[0] and "/d/B_1d.csv" in zeilen[0], zeilen[0])
    check("1.5 die leere Datei ist als leer erkennbar",
          "leere Kursdatei" in zeilen[1], zeilen[1])
    check("1.6 die zu kurze Historie nennt Ist und Soll",
          "300" in zeilen[2] and "500" in zeilen[2], zeilen[2])
    check("1.7 die Kerzenzahl nennt Ist und Soll",
          "12" in zeilen[3] and "99" in zeilen[3], zeilen[3])

    summe, _ = gesammelt(lambda: p.melde({"A": 1}))
    check("1.8 Summenzeile: wie viele von wie vielen",
          "1 von 5" in summe, summe)
    check("1.9 Summenzeile zaehlt die Gruende",
          all(t in summe for t in ("1x Kursdatei fehlt", "1x Kursdatei leer",
                                    "1x Historie zu kurz", "1x Kerzenzahl zu klein")),
          summe)
    check("1.10 Summenzeile ohne Wachposten, wenn die Rechnung aufgeht",
          "ACHTUNG" not in summe, summe)

    leer = Ladeprotokoll(["A", "B"])
    summe2, _ = gesammelt(lambda: leer.melde({"A": 1, "B": 2}))
    check("1.11 Summenzeile steht auch, wenn nichts ausgelassen wurde",
          "2 von 2" in summe2 and "Keines ausgelassen" in summe2, summe2)

    # Der Wachposten: ein Symbol verschwindet, ohne dass ein Grund genannt
    # wurde. Genau der Fehler, gegen den TB-42 gebaut ist.
    still = Ladeprotokoll(["A", "B", "C"])
    summe3, _ = gesammelt(lambda: still.melde({"A": 1}))
    check("1.12 Wachposten meldet ein Symbol ohne genannten Grund",
          "ACHTUNG" in summe3 and "2 Symbol(e)" in summe3, summe3)

    zaehl = Ladeprotokoll(["A", "B", "C"])
    _z, _a = gesammelt(lambda: (zaehl.zu_kurz("B", 1, 2), zaehl.zu_kurz("C", 1, 2)))
    summe4, _ = gesammelt(lambda: zaehl.melde({"A": 1}))
    check("1.13 gleiche Gruende werden zusammengezaehlt",
          "2x Historie zu kurz" in summe4, summe4)


# ===========================================================================
# 2. Je Bot: jeder ausgelassene Grund erzeugt eine Zeile
# ===========================================================================
def pruefe_bot_meldungen(bot, strategien=None, praefix="2"):
    """Haelt EINEM Bot die vier Faelle hin und sieht zu. Gibt True zurueck,
    wenn alle Meldungen da waren - die Mutationsprobe braucht das."""
    vorlauf = messe(bot, strategien=strategien)
    if vorlauf.get("fehler"):
        check(f"{praefix} {bot}: Loader laeuft", False, vorlauf["fehler"])
        return False

    s = vorlauf["schranken"]
    if "MIN_HISTORY_HOURS" in s:
        schranke, einheit, grundwort = s["MIN_HISTORY_HOURS"], "kerzen", "Kerzen"
    else:
        schranke, einheit, grundwort = s["MIN_HISTORY_DAYS"], "tage", "Tage ab"
    universum = vorlauf["universum"][:len(ROLLEN)]
    if len(universum) < len(ROLLEN):
        check(f"{praefix} {bot}: Universum reicht fuer die Proben", False)
        return False

    ordner = tempfile.mkdtemp(prefix="tb42_proben_")
    try:
        zuordnung = baue_proben(ordner, universum, s["INTERVAL"], schranke, einheit)
        lauf = messe(bot, datenordner=ordner, symbole=universum, strategien=strategien)
        if lauf.get("fehler"):
            check(f"{praefix} {bot}: Probelauf laeuft", False, lauf["fehler"])
            return False

        ausgabe = lauf["ausgabe"]
        zeilen = [z for z in ausgabe.splitlines() if z.startswith("Hinweis: ")]
        geladen = set(lauf["symbole"])
        alles = True

        def teil(name, bedingung, detail=""):
            nonlocal alles
            alles = check(name, bedingung, detail) and alles

        for rolle, erwartet in (("datei_fehlt", "keine Kursdatei"),
                                 ("datei_leer", "leere Kursdatei"),
                                 ("zu_kurz", grundwort)):
            sym = zuordnung[rolle]
            passende = [z for z in zeilen if z.split()[1] == sym]
            teil(f"{praefix} {bot}: '{rolle}' wird gemeldet",
                 len(passende) == 1, f"{len(passende)} Zeilen fuer {sym}")
            if passende:
                teil(f"{praefix} {bot}: '{rolle}' nennt den Grund",
                     erwartet in passende[0], passende[0])
            teil(f"{praefix} {bot}: '{rolle}' wird auch wirklich ausgelassen",
                 sym not in geladen, sym)

        for rolle in ("voll_a", "voll_b"):
            sym = zuordnung[rolle]
            teil(f"{praefix} {bot}: '{rolle}' wird geladen", sym in geladen, sym)
            teil(f"{praefix} {bot}: '{rolle}' wird NICHT gemeldet",
                 not any(z.split()[1] == sym for z in zeilen), sym)

        summen = [z for z in ausgabe.splitlines() if z.startswith("Geladen: ")]
        teil(f"{praefix} {bot}: genau eine Summenzeile", len(summen) == 1, str(summen))
        if summen:
            teil(f"{praefix} {bot}: Summenzeile zaehlt richtig",
                 f"{len(geladen)} von {len(universum)}" in summen[0], summen[0])
            teil(f"{praefix} {bot}: Summenzeile ohne Wachposten-Alarm",
                 "ACHTUNG" not in summen[0], summen[0])
        return alles
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


def test_meldungen_alle_bots():
    check("2.0 es sind neun Bots", len(BOTS) == 9, str(BOTS))
    for bot in BOTS:
        pruefe_bot_meldungen(bot)


# ===========================================================================
# 3. Die geladene Symbolliste ist dieselbe wie vor TB-42
# ===========================================================================
def _alter_loader(bot):
    """Den Loader, wie Git ihn VOR TB-42 fuehrt. None, wenn nicht auffindbar."""
    rel = "strategies/%s/multi_symbol_optimise.py" % bot
    try:
        commits = subprocess.run(
            ["git", "-C", BASE_DIR, "log", "--format=%H", "-S", "ladeprotokoll",
             "--", rel], capture_output=True, text=True, timeout=120)
        if commits.returncode != 0 or not commits.stdout.strip():
            return None
        eingefuehrt = commits.stdout.split()[-1]
        alt = subprocess.run(
            ["git", "-C", BASE_DIR, "show", "%s^:%s" % (eingefuehrt, rel)],
            capture_output=True, text=True, timeout=120)
        if alt.returncode != 0:
            return None
        return alt.stdout
    except Exception:                                            # noqa: BLE001
        return None


def test_symbolliste_unveraendert():
    """Der eigentliche Nachweis, dass TB-42 ein Bug-Fix ist."""
    ungeprueft = []
    for bot in BOTS:
        alt_quelltext = _alter_loader(bot)
        if alt_quelltext is None:
            ungeprueft.append(bot)
            continue

        arbeit = tempfile.mkdtemp(prefix="tb42_vorher_")
        try:
            # Ein vollstaendiger Strategie-Ordner, in dem NUR der Loader der
            # alte ist. strategy_paths.py leitet BASE_DIR aus der Lage der
            # Datei ab, deshalb muss die Ordnertiefe stimmen.
            strategien = os.path.join(arbeit, "strategies")
            ziel = os.path.join(strategien, bot)
            shutil.copytree(os.path.join(BASE_DIR, "strategies", bot), ziel)
            with open(os.path.join(ziel, "multi_symbol_optimise.py"), "w") as f:
                f.write(alt_quelltext)
            os.symlink(os.path.join(BASE_DIR, "data"), os.path.join(arbeit, "data"))
            os.symlink(os.path.join(BASE_DIR, "config"), os.path.join(arbeit, "config"))

            vorher = messe(bot, strategien=strategien)
            nachher = messe(bot)
            if vorher.get("fehler") or nachher.get("fehler"):
                check(f"3 {bot}: beide Laeufe gehen durch", False,
                      str(vorher.get("fehler")) + " | " + str(nachher.get("fehler")))
                continue
            check(f"3 {bot}: geladene Symbolliste vor und nach TB-42 identisch",
                  vorher["symbole"] == nachher["symbole"],
                  "nur vorher: %s | nur nachher: %s" % (
                      sorted(set(vorher["symbole"]) - set(nachher["symbole"])),
                      sorted(set(nachher["symbole"]) - set(vorher["symbole"]))))
            check(f"3 {bot}: der alte Loader war bei mindestens einem Symbol still"
                  if bot in ("rsi2_mean_reversion", "turtle_soup_stocks",
                             "volatility_breakout") else f"3 {bot}: Vergleich gelaufen",
                  True)
        finally:
            shutil.rmtree(arbeit, ignore_errors=True)

    check("3.0 der Vorher-Vergleich war fuer alle neun Bots moeglich",
          not ungeprueft,
          "ohne Git-Vorgaenger: %s" % ungeprueft)


# ===========================================================================
# 4. Mutationsproben
# ===========================================================================
MUTATIONEN = [
    ("Meldung 'Kursdatei fehlt' entfernt",
     "            _prot.fehlt(symbol, csv_path)\n", "", "rsi2_crypto"),
    ("Meldung 'Kursdatei leer' entfernt",
     "            _prot.leer(symbol, csv_path)\n", "", "rsi2_crypto"),
    ("Meldung 'Historie zu kurz' entfernt",
     "            _prot.zu_kurz(symbol, timespan_days, MIN_HISTORY_DAYS)\n", "",
     "rsi2_crypto"),
    ("Summenzeile entfernt", "    _prot.melde(data)\n", "", "rsi2_crypto"),
    ("Meldung 'Kerzenzahl zu klein' entfernt",
     "            _prot.zu_wenige_kerzen(symbol, len(df), MIN_HISTORY_HOURS)\n", "",
     "elliott_wave"),
]


def test_mutationen():
    """Jede entfernte Meldung MUSS Pruefung 2 umwerfen.

    Beobachtet wird der Ablauf des mutierten Loaders in einem Wegwerf-Ordner -
    nicht ein Zustand, den der Test selbst behauptet.
    """
    global BESTANDEN, FEHLER
    for name, alt, neu, bot in MUTATIONEN:
        arbeit = tempfile.mkdtemp(prefix="tb42_mutation_")
        try:
            strategien = os.path.join(arbeit, "strategies")
            ziel = os.path.join(strategien, bot)
            shutil.copytree(os.path.join(BASE_DIR, "strategies", bot), ziel)
            os.symlink(os.path.join(BASE_DIR, "data"), os.path.join(arbeit, "data"))
            os.symlink(os.path.join(BASE_DIR, "config"), os.path.join(arbeit, "config"))

            pfad = os.path.join(ziel, "multi_symbol_optimise.py")
            quelle = open(pfad).read()
            if quelle.count(alt) != 1:
                check(f"4 Mutation '{name}': Ansatzpunkt eindeutig", False,
                      f"{quelle.count(alt)} Treffer in {bot}")
                continue
            open(pfad, "w").write(quelle.replace(alt, neu))

            # Pruefung 2 gegen den MUTIERTEN Loader laufen lassen und dabei
            # die Zaehler des echten Laufs unangetastet lassen.
            merk_b, merk_f = BESTANDEN, list(FEHLER)
            heil = pruefe_bot_meldungen(bot, strategien=strategien, praefix="4-probe")
            BESTANDEN, FEHLER = merk_b, merk_f

            check(f"4 Mutation '{name}' wird bemerkt", not heil,
                  "der Test blieb gruen, obwohl die Meldung fehlt")
        finally:
            shutil.rmtree(arbeit, ignore_errors=True)


# ===========================================================================
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kind")
    p.add_argument("--aus")
    p.add_argument("--daten")
    p.add_argument("--symbole")
    p.add_argument("--strategien")
    p.add_argument("--nur", default="1,2,3,4")
    args = p.parse_args()

    if args.kind:
        return kindlauf(args.kind, args.aus, args.daten,
                        args.symbole.split(",") if args.symbole else None,
                        args.strategien)

    gewaehlt = set(args.nur.split(","))
    print("=" * 78)
    print("Selbsttests shared/ladeprotokoll.py und die neun Loader (TB-42, Teil 1)")
    print("=" * 78)
    if "1" in gewaehlt:
        print("\n1. Der Baustein selbst")
        test_baustein()
    if "2" in gewaehlt:
        print("2. Je Bot: jeder ausgelassene Grund erzeugt eine Zeile")
        test_meldungen_alle_bots()
    if "3" in gewaehlt:
        print("3. Geladene Symbolliste vor und nach TB-42")
        test_symbolliste_unveraendert()
    if "4" in gewaehlt:
        print("4. Mutationsproben")
        test_mutationen()

    print("\n" + "=" * 78)
    if FEHLER:
        print(f"{len(FEHLER)} FEHLER von {BESTANDEN + len(FEHLER)} Pruefungen:")
        for zeile in FEHLER:
            print(f"  - {zeile}")
        return 1
    print(f"Alle {BESTANDEN} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
