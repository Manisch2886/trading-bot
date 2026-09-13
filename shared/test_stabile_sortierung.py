"""
Selbsttests: stabile Sortierung der beiden Tages-Kapitalkurven (TB-19)
==============================================================================
Geprueft wird das VERHALTEN von

    shared/portfolio_overview.py
        -> _daily_capital_curve_from_equity_df()   (speist die Montags-Mail
                                                     und die Dashboard-
                                                     Portfolio-Sicht)
    strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py
        -> build_daily_capital_curve()             (Vier-Bot-Korrelation)

nicht das Vorhandensein von `kind="stable"` im Quelltext. Eine Textsuche
waere hier besonders wertlos: sie prueft genau das, was der Diff ohnehin
zeigt, und sagt nichts darueber, ob die Zusicherung traegt.


DIE EIGENTLICHE ZUSICHERUNG
------------------------------------------------------------------------------
Beide Funktionen bauen aus einer `equity_curve.csv` eine taegliche
Kapitalkurve: sortieren nach `time`, dann `groupby("date")[...].last()`.

Die Datei steht in EREIGNISREIHENFOLGE - so schreibt sie
`equity_simulation.py`. Mehrere Ausstiege am selben Tag tragen denselben
Zeitstempel (Tagesbots: Datum ohne Uhrzeit). Der Kapitalstand des Tages ist
deshalb der Wert der Zeile, die unter diesen Gleichstaenden ZULETZT in der
Datei steht - alle frueheren sind Zwischenstaende mitten im Tag.

Zugesichert wird also:

    Der Tageswert ist der `capital_after` der in der EINGABEREIHENFOLGE
    letzten Zeile dieses Tages - unabhaengig davon, wie viele Zeilen
    anderer Tage daneben stehen.

Der Zusatz nach dem Gedankenstrich ist der Kern. `sort_values` ohne
`kind="stable"` sortiert mit Quicksort; dessen Vertauschung von
Gleichstaenden haengt an Laenge und Lage des gesamten Feldes. Fremdzeilen
anderer Tage koennen den Wert eines Tages inhaltlich nicht beruehren - unter
einer instabilen Sortierung tun sie es trotzdem.

Das ist kein theoretischer Fall: auf dem Datenstand vom 13.09.2026 weichen
bei ALLEN NEUN abgelegten Kurven Tageswerte ab, von 1 Tag (`elliott_wave`)
bis 698 von 2022 Tagen (`turtle_soup_stocks`).


DIE BEIDEN WIEDERKEHRENDEN FALLEN
------------------------------------------------------------------------------
**Falle 1 - die selbstbestaetigende Probe.** Nirgends stellt der Test den
Zustand her, den er anschliessend wiedererkennt. Der Erwartungswert wird
nicht aus einem Lauf der geprueften Funktion gewonnen, sondern aus der
Konstruktion der Eingabe hergeleitet (die zuletzt eingefuegte Zeile des
Tages). Und dass die Probe ueberhaupt unterscheidet, wird nicht
vorausgesetzt, sondern am ABLAUF nachgewiesen: derselbe Fall laeuft
zusaetzlich gegen eine MUTIERTE Kopie der echten Datei, in der genau eine
Wache entfernt ist. Schlaegt die Mutante nicht fehl, ist der Test selbst
durchgefallen - nicht bestanden.

**Falle 2 - die zweite Wache verdeckt das Fehlen der ersten.** Zwei Wachen
stecken in derselben Zeile: dass ueberhaupt sortiert wird, und dass STABIL
sortiert wird. Die Pruefungen sind so gewaehlt, dass je nur eine greifen
kann:

  * Abschnitt 1 (Gleichstaende, ALLE Zeilen des Tages auf demselben
    Zeitstempel) haengt ausschliesslich an der Stabilitaet. Wuerde die
    Sortierung ersatzlos entfallen, bestuende dieser Abschnitt weiterhin -
    ohne Gleichstand-Vertauschung liefert `groupby().last()` von sich aus
    die zuletzt eingefuegte Zeile. Abschnitt 1 sagt also nichts darueber,
    ob sortiert wird.
  * Abschnitt 2 (KEINE Gleichstaende, die Zeilen eines Tages stehen
    verkehrt herum in der Datei) haengt ausschliesslich daran, DASS
    sortiert wird. Ohne Gleichstaende ist jede korrekte Sortierung - stabil
    oder nicht - gleichwertig; der Abschnitt sagt nichts ueber Stabilitaet.

Abschnitt 5 weist diese Trennung nicht als Absicht aus, sondern misst sie:
je Mutante wird festgehalten, welche Abschnitte anschlagen, und genau die
erwarteten muessen es sein - nicht mehr und nicht weniger.


WAS DIESER TEST NICHT VERAENDERT
------------------------------------------------------------------------------
Die geprueften Dateien werden als BIBLIOTHEK eingebunden, ihr
`__main__`-Block laeuft nie. Mutationen entstehen ausschliesslich in Kopien
unter einem temporaeren Ordner. Abschnitt 7 weist per `git status` nach,
dass im Repo nichts entstanden oder veraendert ist.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:
    python3 shared/test_stabile_sortierung.py
    python3 shared/test_stabile_sortierung.py --schnell   # ohne Abschnitt 4/6
"""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

import pandas as pd

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)

# Die beiden geprueften Stellen. `sortierzeile` ist NICHT die Zusicherung -
# sie ist der Angriffspunkt der Mutationen in Abschnitt 5.
ZIELE = {
    "portfolio_overview": {
        "pfad": os.path.join(BASE_DIR, "shared", "portfolio_overview.py"),
        "funktion": "_daily_capital_curve_from_equity_df",
        "nimmt": "dataframe",
        "sortierzeile": 'df = equity_df.sort_values("time", kind="stable").copy()',
        "ohne_stable": 'df = equity_df.sort_values("time").copy()',
        "ohne_sortierung": 'df = equity_df.copy()',
    },
    "portfolio_correlation_analysis": {
        "pfad": os.path.join(BASE_DIR, "strategies", "rsi2_mean_reversion",
                             "portfolio_correlation_analysis.py"),
        "funktion": "build_daily_capital_curve",
        "nimmt": "csv",
        "sortierzeile": 'df = df.sort_values("time", kind="stable")',
        "ohne_stable": 'df = df.sort_values("time")',
        "ohne_sortierung": 'df = df.copy()',
    },
}


class Protokoll:
    """Sammelt Pruefungen, statt beim ersten Fehler abzubrechen - ein
    einzelner Fehlschlag soll nicht verbergen, was die uebrigen Abschnitte
    gesagt haetten."""

    def __init__(self):
        self.ok = 0
        self.fehler = []
        self.abschnitte = set()   # Abschnitte MIT Fehler (fuer Abschnitt 5)

    def pruefe(self, abschnitt: str, text: str, bedingung: bool, zusatz: str = ""):
        if bedingung:
            self.ok += 1
            print(f"  OK    {text}")
        else:
            self.fehler.append(f"{abschnitt}: {text}{(' - ' + zusatz) if zusatz else ''}")
            self.abschnitte.add(abschnitt)
            print(f"  FEHLT {text}" + (f"  [{zusatz}]" if zusatz else ""))


# ===========================================================================
# Module laden - Original wie Mutante ueber denselben Weg
# ===========================================================================
def lade(pfad: str, name: str):
    spec = importlib.util.spec_from_file_location(name, pfad)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def mutiere(ziel: dict, alt: str, neu: str, wurzel: str, name: str):
    """Kopiert die echte Datei in den temporaeren Ordner und ersetzt dort -
    und nur dort - genau eine Zeile. Gibt None zurueck, wenn die Zeile nicht
    genau einmal vorkommt: dann hat der Test die Datei nicht mehr
    verstanden, und das ist ein Befund, kein stilles Ueberspringen."""
    kopie = os.path.join(wurzel, name + ".py")
    shutil.copyfile(ziel["pfad"], kopie)
    text = open(kopie, encoding="utf-8").read()
    if text.count(alt) != 1:
        return None
    open(kopie, "w", encoding="utf-8").write(text.replace(alt, neu))
    return lade(kopie, name)


def tageskurve(modul, ziel: dict, zeilen: list, wurzel: str) -> pd.Series:
    """Ruft die ECHTE Funktion des Moduls auf. Die beiden Stellen nehmen
    Unterschiedliches entgegen (DataFrame bzw. Dateipfad); der Unterschied
    wird hier aufgeloest, damit beide denselben Pruefsatz durchlaufen."""
    df = pd.DataFrame(zeilen, columns=["time", "capital_after"])
    df["time"] = pd.to_datetime(df["time"])
    funktion = getattr(modul, ziel["funktion"])
    if ziel["nimmt"] == "dataframe":
        return funktion(df)
    pfad = os.path.join(wurzel, "eingabe.csv")
    df.to_csv(pfad, index=False)
    return funktion(pfad)


# ===========================================================================
# Die Faelle. Jeder Fall liefert (Zeilen, geprueftes Datum, erwarteter Wert).
# Der erwartete Wert folgt aus der KONSTRUKTION, nicht aus einem Lauf.
# ===========================================================================
TAG = "2020-06-15"


def fall_gleichstand(anzahl_gleich: int, fremdtage: int):
    """Abschnitt 1: alle Zeilen des geprueften Tages auf DEMSELBEN
    Zeitstempel, dahinter `fremdtage` Zeilen anderer Tage.

    Die Fremdzeilen koennen den Kapitalstand des 15.06. inhaltlich nicht
    beruehren - sie liegen an anderen Tagen. Sie veraendern aber Laenge und
    Lage des zu sortierenden Feldes, und genau daran haengt die
    Vertauschung der Gleichstaende unter Quicksort."""
    zeilen = [(TAG, 1000.0 + i) for i in range(anzahl_gleich)]
    for k in range(fremdtage):
        zeilen.append((f"2020-06-{16 + k:02d}", 5000.0 + k))
    erwartet = 1000.0 + anzahl_gleich - 1      # die zuletzt eingefuegte Zeile
    return zeilen, TAG, erwartet


def fall_verkehrt_ohne_gleichstand(fremdtage: int):
    """Abschnitt 2: KEINE Gleichstaende - die drei Zeilen des geprueften
    Tages tragen verschiedene Uhrzeiten und stehen ABSTEIGEND in der Datei.

    Der Kapitalstand des Tages ist der spaeteste, also der 12:00-Wert. In
    der Eingabereihenfolge steht der aber VORNE; zuletzt steht 06:00. Ohne
    eine tatsaechlich ausgefuehrte Sortierung greift `groupby().last()`
    deshalb 600.0 ab. Stabil oder nicht ist hier gleichgueltig - es gibt
    keine Gleichstaende, die eine Sortierung vertauschen koennte."""
    zeilen = [
        (f"{TAG} 12:00:00", 1200.0),
        (f"{TAG} 09:00:00", 900.0),
        (f"{TAG} 06:00:00", 600.0),
    ]
    for k in range(fremdtage):
        zeilen.append((f"2020-06-{16 + k:02d} 09:00:00", 5000.0 + k))
    return zeilen, TAG, 1200.0


def fall_ohne_dubletten(fremdtage: int):
    """Abschnitt 3 (Gegenprobe): ein Zeitstempel je Tag, chronologisch."""
    zeilen = [(f"2020-06-{15 + k:02d}", 1000.0 + k) for k in range(3 + fremdtage)]
    return zeilen, TAG, 1000.0


# Wie viele Fremdzeilen danebenstehen, ist inhaltlich gleichgueltig - der
# Wert des geprueften Tages muss bei JEDER dieser Laengen derselbe sein.
# Die Spanne ist bewusst breit: numpy wechselt unterhalb einer Feldlaenge
# von 16 auf Insertion Sort (die zufaellig stabil ist), darueber auf
# Introsort. Eine schmale Spanne koennte an dieser Schwelle vorbeilaufen.
FREMDTAGE = (0, 1, 2, 3, 5, 8, 12)
GLEICHSTAENDE = (5, 17, 40)


# ===========================================================================
# Abschnitt 1 - der Kernfall: Gleichstaende
# ===========================================================================
def abschnitt1(modul, ziel, wurzel, p, praefix=""):
    treffer = 0
    for anzahl in GLEICHSTAENDE:
        werte = {}
        for fremd in FREMDTAGE:
            zeilen, tag, erwartet = fall_gleichstand(anzahl, fremd)
            kurve = tageskurve(modul, ziel, zeilen, wurzel)
            werte[fremd] = float(kurve.loc[pd.Timestamp(tag)])
        einheitlich = len(set(werte.values())) == 1
        richtig = all(v == erwartet for v in werte.values())
        p.pruefe("Abschnitt 1",
                 f"{praefix}{anzahl} Gleichstaende: Tageswert ist der zuletzt "
                 f"eingefuegte ({erwartet:.1f}) und haengt nicht an Fremdzeilen",
                 einheitlich and richtig,
                 "" if (einheitlich and richtig) else f"erhalten {werte}")
        treffer += 1
    return treffer


# ===========================================================================
# Abschnitt 2 - es wird ueberhaupt sortiert (ohne Gleichstaende)
# ===========================================================================
def abschnitt2(modul, ziel, wurzel, p, praefix=""):
    for fremd in FREMDTAGE:
        zeilen, tag, erwartet = fall_verkehrt_ohne_gleichstand(fremd)
        kurve = tageskurve(modul, ziel, zeilen, wurzel)
        wert = float(kurve.loc[pd.Timestamp(tag)])
        p.pruefe("Abschnitt 2",
                 f"{praefix}absteigend abgelegter Tag ({fremd} Fremdzeilen): "
                 f"Tageswert ist der spaeteste ({erwartet:.1f})",
                 wert == erwartet, "" if wert == erwartet else f"erhalten {wert}")


# ===========================================================================
# Abschnitt 3 - Gegenprobe: ohne doppelte Zeitstempel aendert sich nichts
# ===========================================================================
def abschnitt3(modul, mutant_ohne_stable, ziel, wurzel, p):
    """Die Gegenprobe vergleicht nicht gegen eine hingeschriebene Zahl,
    sondern gegen den LAUF der unveraenderten Fassung: dieselbe Eingabe,
    einmal durch die heutige Datei, einmal durch die Fassung ohne
    `kind="stable"`. Ohne Gleichstaende muessen beide Zeile fuer Zeile
    dasselbe liefern - die Umstellung darf dort nichts bewegen."""
    for fremd in FREMDTAGE:
        zeilen, _, _ = fall_ohne_dubletten(fremd)
        a = tageskurve(modul, ziel, zeilen, wurzel)
        b = tageskurve(mutant_ohne_stable, ziel, zeilen, wurzel)
        p.pruefe("Abschnitt 3",
                 f"ohne doppelte Zeitstempel ({len(zeilen)} Zeilen): stabil und "
                 f"unstabil liefern dieselbe Kurve",
                 a.equals(b), "" if a.equals(b) else "Kurven unterscheiden sich")


# ===========================================================================
# Abschnitt 4 - echte Daten und Wiederholbarkeit
# ===========================================================================
SKRIPTE = (
    ("shared/portfolio_overview.py", "Max Drawdown kombiniert"),
    ("strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py",
     "Max Drawdown kombiniert"),
)


# `shared/portfolio_overview.py` schreibt beim Lauf seine eigenen
# Ergebnisdateien nach results/portfolio_overview/ - das ist seine Aufgabe,
# nicht ein Fehler des Tests. Damit Abschnitt 7 trotzdem streng bleiben kann
# (leere Differenz statt einer Ausnahmeliste, hinter der sich echte
# Aenderungen verstecken koennten), sichert der Test diesen Ordner vor den
# Laeufen byteweise und stellt ihn danach wieder her.
AUSGABEORDNER = os.path.join(BASE_DIR, "results", "portfolio_overview")


def _sichern() -> dict:
    if not os.path.isdir(AUSGABEORDNER):
        return {}
    return {n: open(os.path.join(AUSGABEORDNER, n), "rb").read()
            for n in os.listdir(AUSGABEORDNER)
            if os.path.isfile(os.path.join(AUSGABEORDNER, n))}


def _zuruecksichern(stand: dict):
    if not os.path.isdir(AUSGABEORDNER):
        return
    for n in os.listdir(AUSGABEORDNER):
        pfad = os.path.join(AUSGABEORDNER, n)
        if not os.path.isfile(pfad):
            continue
        if n in stand:
            open(pfad, "wb").write(stand[n])
        else:
            os.remove(pfad)          # waehrend des Laufs neu entstanden


def abschnitt4(p):
    """Derselbe Lauf zweimal muss byteweise dasselbe liefern. Geprueft wird
    die vollstaendige Ausgabe, nicht eine herausgegriffene Zahl."""
    stand = _sichern()
    try:
        for rel, marke in SKRIPTE:
            laeufe = []
            for _ in range(2):
                lauf = subprocess.run([sys.executable, os.path.join(BASE_DIR, rel)],
                                      cwd=BASE_DIR, capture_output=True, text=True)
                laeufe.append(lauf.stdout)
            gleich = laeufe[0] == laeufe[1] and laeufe[0] != ""
            p.pruefe("Abschnitt 4", f"{rel}: zwei Laeufe, byteweise dieselbe Ausgabe",
                     gleich, "" if gleich else "Ausgaben unterscheiden sich oder sind leer")
            p.pruefe("Abschnitt 4", f"{rel}: Ausgabe enthaelt '{marke}'",
                     marke in laeufe[0])
    finally:
        _zuruecksichern(stand)


def abschnitt4b(p):
    """Die abgelegten Kurven aller neun Bots sind ECHTE Daten mit echten
    Gleichstaenden. Hier wird nicht gerechnet, sondern nur festgehalten,
    dass die Probe aus Abschnitt 1 kein Laborfall ist: in jeder dieser
    Dateien gibt es Tage, an denen die Reihenfolge den Wert entscheidet."""
    kurven = []
    for ordner, _, dateien in os.walk(os.path.join(BASE_DIR, "results")):
        if "equity_curve.csv" in dateien:
            kurven.append(os.path.join(ordner, "equity_curve.csv"))
    p.pruefe("Abschnitt 4", f"abgelegte Kapitalkurven gefunden ({len(kurven)})",
             len(kurven) >= 9, f"gefunden: {len(kurven)}")
    betroffen = 0
    for pfad in kurven:
        df = pd.read_csv(pfad, parse_dates=["time"])
        if df["time"].duplicated().any():
            betroffen += 1
    p.pruefe("Abschnitt 4",
             "jede abgelegte Kurve enthaelt doppelte Zeitstempel "
             "(der geprueften Fall kommt in echten Daten vor)",
             betroffen == len(kurven), f"{betroffen} von {len(kurven)}")


# ===========================================================================
# Abschnitt 5 - Mutationsproben
# ===========================================================================
# Je Mutante steht dahinter, WELCHE Abschnitte anschlagen muessen. Die
# Erwartung ist exakt: mehr waere eine Wache, die zu viel abdeckt (Falle 2),
# weniger eine Pruefung, die nichts sichert.
MUTATIONEN = (
    ("ohne stabile Sortierung", "ohne_stable", {"Abschnitt 1"}),
    ("Sortierung ersatzlos entfernt", "ohne_sortierung", {"Abschnitt 2"}),
)


def abschnitt5(ziel, name, wurzel, p):
    for titel, schluessel, erwartete_abschnitte in MUTATIONEN:
        unterwurzel = os.path.join(wurzel, "mutante_" + schluessel)
        os.makedirs(unterwurzel, exist_ok=True)
        mutant = mutiere(ziel, ziel["sortierzeile"], ziel[schluessel],
                         unterwurzel, f"{name}_{schluessel}")
        if mutant is None:
            p.pruefe("Abschnitt 5", f"Mutante '{titel}' liess sich erzeugen", False,
                     "Sortierzeile nicht genau einmal gefunden")
            continue

        # Die Abschnitte laufen gegen die Mutante in ein EIGENES Protokoll.
        mp = Protokoll()
        print(f"    (Mutante '{titel}' - die folgenden FEHLT-Zeilen sind das Ziel)")
        abschnitt1(mutant, ziel, unterwurzel, mp, praefix="[Mutante] ")
        abschnitt2(mutant, ziel, unterwurzel, mp, praefix="[Mutante] ")

        p.pruefe("Abschnitt 5",
                 f"Mutante '{titel}': genau {sorted(erwartete_abschnitte)} schlaegt an",
                 mp.abschnitte == erwartete_abschnitte,
                 f"angeschlagen: {sorted(mp.abschnitte) or 'nichts'}")


# ===========================================================================
# Abschnitt 6 - die abgelegten Kurven bleiben unberuehrt
# ===========================================================================
def abschnitt6(p):
    lauf = subprocess.run([sys.executable, os.path.join(BASE_DIR, "shared", "ergebniskurven.py")],
                          cwd=BASE_DIR, capture_output=True, text=True)
    treffer = "Zusammenfassung: 9x AKTUELL" in lauf.stdout
    letzte = lauf.stdout.strip().splitlines()[-1:] or [lauf.stderr[-200:]]
    p.pruefe("Abschnitt 6", "shared/ergebniskurven.py meldet '9x AKTUELL'",
             treffer and lauf.returncode == 0,
             "" if treffer else str(letzte[0]))


# ===========================================================================
# Abschnitt 7 - der Test selbst veraendert nichts
# ===========================================================================
BEOBACHTET = ("strategies/", "results/", "data/", "shared/", "logs/", "paper_trading_")


def git_zustand() -> str:
    lauf = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR,
                          capture_output=True, text=True)
    return "\n".join(sorted(z for z in lauf.stdout.splitlines()
                            if z[3:].strip('"').startswith(BEOBACHTET)))


# ===========================================================================
def main() -> int:
    schnell = "--schnell" in sys.argv
    vorher = git_zustand()
    p = Protokoll()

    with tempfile.TemporaryDirectory(prefix="tb19_") as wurzel:
        for name, ziel in ZIELE.items():
            print(f"\n--- {os.path.relpath(ziel['pfad'], BASE_DIR)} ---")
            unterwurzel = os.path.join(wurzel, name)
            os.makedirs(unterwurzel, exist_ok=True)
            modul = lade(ziel["pfad"], "geprueft_" + name)

            abschnitt1(modul, ziel, unterwurzel, p)
            abschnitt2(modul, ziel, unterwurzel, p)

            gegenprobe_wurzel = os.path.join(unterwurzel, "gegenprobe")
            os.makedirs(gegenprobe_wurzel, exist_ok=True)
            ohne_stable = mutiere(ziel, ziel["sortierzeile"], ziel["ohne_stable"],
                                  gegenprobe_wurzel, name + "_gegenprobe")
            if ohne_stable is None:
                p.pruefe("Abschnitt 3", "Vergleichsfassung ohne kind=stable erzeugt",
                         False, "Sortierzeile nicht genau einmal gefunden")
            else:
                abschnitt3(modul, ohne_stable, ziel, gegenprobe_wurzel, p)

            abschnitt5(ziel, name, os.path.join(wurzel, "mut_" + name), p)

        print("\n--- echte Daten ---")
        abschnitt4b(p)
        if not schnell:
            abschnitt4(p)
            print("\n--- abgelegte Ergebniskurven ---")
            abschnitt6(p)
        else:
            print("  (Abschnitt 4 und 6 uebersprungen: --schnell)")

    print("\n--- der Test selbst ---")
    nachher = git_zustand()
    p.pruefe("Abschnitt 7", "git status unveraendert (der Test schreibt nicht ins Repo)",
             vorher == nachher, f"vorher:\n{vorher}\nnachher:\n{nachher}")

    print("\n" + "=" * 78)
    print(f"Ergebnis: {p.ok} bestanden, {len(p.fehler)} fehlgeschlagen")
    for f in p.fehler:
        print(f"  - {f}")
    print("=" * 78)
    return 1 if p.fehler else 0


if __name__ == "__main__":
    sys.exit(main())
