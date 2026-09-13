"""
Ist der Backtest reproduzierbar, wenn die Symbolliste anders sortiert ist?
==============================================================================
    python3 shared/determinismus.py                    # alle Bots (Rueckgabewert 1 bei Befund)
    python3 shared/determinismus.py --schnell          # unter zwei Minuten, fuer den Cronjob
    python3 shared/determinismus.py --voll             # ohne Zwischenspeicher, alles neu gerechnet
    python3 shared/determinismus.py --bot t3_supertrend --perms 50
    python3 shared/determinismus.py --json bericht.json --ausgabe ordner/

DIE FRAGE
------------------------------------------------------------------------------
Ein Backtest, der mit 20 zufaelligen Permutationen der Symboldatei laeuft,
muss bitidentische Ergebnisse liefern. Ist er das nicht, gibt es versteckten
Zustand - eine Groesse, die das Ergebnis mitbestimmt, ohne in Kursdaten,
Parametern oder Strategielogik zu stehen.

Warum das keine akademische Frage ist, steht gemessen im Repo:
`research/drawdown_reihenfolge/` - ueber 200 Permutationen haelt der Sieger
einer Parametersuche nur in 30,5 % / 34,5 % / 40,0 % der Faelle. Waere
`config/sp500_top150.txt` alphabetisch statt nach Marktkapitalisierung
sortiert, stuenden bei drei Bots andere Live-Parameter.

WAS VERGLICHEN WIRD - UND WARUM NICHT NUR DIE KENNZAHLEN
------------------------------------------------------------------------------
Drei Ebenen, absichtlich getrennt (Einzelheiten in
`shared/determinismus_lauf.py`):

1. **Signalmenge** - alle erzeugten Trades, bevor das Kapital darueber
   entscheidet, als Multimenge. Weicht sie ab, hat die Signalerzeugung selbst
   symboluebergreifenden Zustand. Schwerster denkbarer Befund.
2. **Ausgefuehrte Trades** - welche Trades tatsaechlich Kapital bekommen
   haben, als Multimenge. **Leitkriterium.** Hier schlaegt die Zuteilung bei
   bindendem Positionslimit durch.
3. **Kapitalpfad** - die Zeilen der Kapitalkurve in ihrer Reihenfolge, mit
   Allokation und Kapitalstand. Strengste Ebene.

Die Kennzahlen (Rendite, Drawdown, Trade-Zahl) werden ausgewiesen, sind aber
**kein** Kriterium. Ein Vergleich der Kennzahlen allein wuerde genau die
Unterschiede verdecken, die sich herausmitteln: zwei Permutationen koennen
voellig verschiedene Trades handeln und trotzdem auf dieselbe Rendite kommen.

Reihenfolgeunabhaengig verglichen wird auf Ebene 1 und 2 bewusst. Die
Zeilenreihenfolge des zusammengehaengten Trade-DataFrames ist ein Nebenprodukt
der Symbolbloecke und beschreibt keinen Verlauf, den jemand haette erleben
koennen - dieselbe Begruendung steht seit `research/drawdown_reihenfolge/`
bereits in `multi_symbol_optimise.py`. Wuerde man sie als Kriterium nehmen,
waeren alle neun Bots aus einem Grund ohne inhaltlichen Gehalt rot, und eine
Pruefung, die immer anschlaegt, liest bald niemand mehr.

DREI URTEILE
------------------------------------------------------------------------------
* **DETERMINISTISCH** - alle drei Ebenen identisch ueber alle Permutationen.
* **NUR REIHENFOLGE** - dieselben Trades werden ausgefuehrt, nur in anderer
  Abrechnungsreihenfolge bei gleichem Zeitstempel. Das aendert die
  Zwischenstaende der Kurve (und damit den Drawdown), nicht aber, wer
  gehandelt wurde. Ein Befund, aber ein schwaecherer.
* **NICHT DETERMINISTISCH** - die Auswahl selbst haengt an der
  Symbolreihenfolge.

WAS DIESES PROGRAMM NIE TUT
------------------------------------------------------------------------------
* **Es behebt nichts.** Es misst und meldet. Die Zuteilungsregel nach
  Signalstaerke und die stabile Sortierung an den offenen Stellen sind eigene
  Aufgaben.
* **Es aendert keine Symboldatei**, auch nicht voruebergehend. Permutiert wird
  im Speicher, an der Stelle, an der die Liste in den Bot eintritt.
* **Es schreibt nicht nach `results/`.** Strukturell abgesichert wie in
  `kurven_lauf.py`: `RESULTS_DIR` zeigt waehrend der Laeufe in einen
  temporaeren Ordner. `shared/ergebniskurven.py` meldet nach einem Lauf
  weiterhin 9x AKTUELL.
* **Es fasst keinen Bot-Code an** und importiert keinen Bot in den eigenen
  Prozess (neun gleichnamige `equity_simulation.py` kollidieren in
  `sys.modules`) - ein Subprozess je Bot, wie in
  `shared/portfolio_overview.py` und `shared/ergebniskurven.py`.

Vorbild fuer Aufbau und Rueckgabewert: `shared/kursdaten.py` (PR #81) und
`shared/ergebniskurven.py` (PR #86).
"""

import argparse
import json
import os
import subprocess
import sys
import time

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)
STRATEGIES_DIR = os.path.join(BASE_DIR, "strategies")
LAUF_SKRIPT = os.path.join(_SHARED_DIR, "determinismus_lauf.py")

META_PREFIX = "__DETERMINISMUS__ "

# Voreinstellung 20: die Zahl aus der externen Analyse, die diese Aufgabe
# ausgeloest hat. Sie ist nicht statistisch begruendet und muss es auch nicht
# sein - gesucht wird kein Erwartungswert, sondern ein GEGENBEISPIEL. Schon
# zwei Permutationen mit verschiedenem Ergebnis beweisen versteckten Zustand;
# 20 sind da, um die Streuung mit einer brauchbaren Spanne zu beziffern und um
# einen seltenen Effekt nicht zu uebersehen. Wer eine engere Spanne braucht,
# erhoeht die Zahl - die Aussage "deterministisch/nicht" aendert sich davon
# praktisch nie, wohl aber die berichtete Bandbreite.
PERMUTATIONEN = 20

# Fester Startwert: derselbe Aufruf liefert dieselbe Permutationsfolge.
SEED = 20260913

# So viele Wiederholungen werden trotz Zwischenspeicher voll nachgerechnet und
# Symbol fuer Symbol mit dem gespeicherten Ergebnis verglichen. Zwei reichen,
# um die Voraussetzung des Speichers (je Symbol unabhaengig) an echten Daten
# zu belegen, ohne die Laufzeit zu verdreifachen. `--voll` schaltet den
# Speicher ganz ab.
PRUEF_LAEUFE = 2

# --schnell: fuer die regelmaessige Pruefung. Fuenf Permutationen und ein
# Nachrechnungslauf; das findet jeden Befund, den 20 auch finden (siehe
# research/determinismus/BERICHT.md, Abschnitt 5), beziffert die Streuung nur
# groeber.
SCHNELL_PERMUTATIONEN = 5
SCHNELL_PRUEF_LAEUFE = 1

DETERMINISTISCH = "DETERMINISTISCH"
NUR_REIHENFOLGE = "NUR REIHENFOLGE"
NICHT = "NICHT DETERMINISTISCH"
UNKLAR = "UNKLAR"

# Welches Urteil ist ein Befund? UNKLAR ebenfalls - ein Lauf, der nicht
# durchlief, ist keine Entwarnung. Genau dieser Fehler ("abgestuerzte Laeufe
# als identisch gewertet, beide Ausgaben leer") steht als Prinzip 7.12 im
# Uebergabeprotokoll.
BEFUND_URTEILE = {NICHT, NUR_REIHENFOLGE, UNKLAR}
ERNSTE_URTEILE = {NICHT, UNKLAR}


def finde_bots(strategien: str = None) -> list:
    """Alle Strategie-Ordner mit einer equity_simulation.py. Nicht hart
    codiert - ein zehnter Bot wird automatisch mitgeprueft."""
    ordner = strategien or STRATEGIES_DIR
    if not os.path.isdir(ordner):
        return []
    return sorted(
        name for name in os.listdir(ordner)
        if os.path.exists(os.path.join(ordner, name, "equity_simulation.py"))
    )


def pruefe_bot(bot: str, perms: int, seed: int, pruef_laeufe: int,
               voll: bool, basis: str = None) -> dict:
    """Ein Subprozess je Bot. Der Rueckgabewert des Kindes wird bewusst NICHT
    als Urteil benutzt - das Urteil steht in der Meldezeile. Ein Kind ohne
    Meldezeile ist ein Fehlschlag und wird als solcher gefuehrt, nicht als
    stille Entwarnung."""
    befehl = [sys.executable, LAUF_SKRIPT, bot, "--perms", str(perms),
              "--seed", str(seed), "--pruef-laeufe", str(pruef_laeufe)]
    if voll:
        befehl.append("--voll")
    if basis:
        befehl += ["--basis", basis]

    begonnen = time.time()
    kind = subprocess.run(befehl, capture_output=True, text=True, cwd=BASE_DIR)
    dauer = time.time() - begonnen

    for zeile in reversed(kind.stdout.splitlines()):
        if zeile.startswith(META_PREFIX):
            bericht = json.loads(zeile[len(META_PREFIX):])
            bericht["wanduhr_s"] = round(dauer, 1)
            return bericht

    return {
        "bot": bot,
        "urteil": UNKLAR,
        "wanduhr_s": round(dauer, 1),
        "fehler": [f"Lauf fehlgeschlagen (Rueckgabewert {kind.returncode}).",
                   (kind.stderr.strip() or kind.stdout.strip())[-1200:]],
    }


def _zahl(wert, nachkomma=2, leer="-"):
    if wert is None:
        return leer
    return f"{wert:.{nachkomma}f}"


def berichte(befunde: list):
    print("=" * 100)
    print("DETERMINISMUS DER BACKTESTS UNTER PERMUTIERTER SYMBOLREIHENFOLGE")
    print("=" * 100)
    print(f"{'Bot':<28} {'Urteil':<22} {'umstr.':>7} {'Rendite-Spanne':>22} "
          f"{'Drawdown-Spanne':>20}")
    print("-" * 100)

    for b in befunde:
        urteil = b.get("urteil", UNKLAR)
        umstritten = b.get("umstrittene_trades") or {}
        streuung = b.get("streuung") or {}
        rendite = streuung.get("rendite_pct") or {}
        drawdown = streuung.get("max_drawdown_pct") or {}

        anteil = (f"{umstritten['anteil_pct']:.1f}%"
                  if umstritten.get("anteil_pct") is not None else "-")
        r = (f"{_zahl(rendite.get('min'))} .. {_zahl(rendite.get('max'))}"
             if rendite.get("min") is not None else "-")
        d = (f"{_zahl(drawdown.get('min'))} .. {_zahl(drawdown.get('max'))}"
             if drawdown.get("min") is not None else "-")
        print(f"{b['bot']:<28} {urteil:<22} {anteil:>7} {r:>22} {d:>20}")

    print("-" * 100)
    print()
    print(f"{'Bot':<28} {'Limit':>7} {'max. gleichzeitig':>18} {'Limit erreicht':>16} "
          f"{'Trades':>8} {'abgelehnt':>18}")
    print("-" * 100)
    for b in befunde:
        pl = b.get("positionslimit") or {}
        streuung = (b.get("streuung") or {}).get("trades_uebersprungen") or {}
        umstritten = b.get("umstrittene_trades") or {}
        limit = pl.get("limit")
        erreicht = (f"{pl['limit_erreicht_in_laeufen']}/{pl['laeufe']} Laeufen"
                    if pl.get("laeufe") else "-")
        offen = (f"{pl['gleichzeitig_offen_min']}..{pl['gleichzeitig_offen_max']}"
                 if pl.get("gleichzeitig_offen_max") is not None else "-")
        abgelehnt = (f"{_zahl(streuung.get('min'), 0)}..{_zahl(streuung.get('max'), 0)}"
                     if streuung.get("min") is not None else "-")
        print(f"{b['bot']:<28} {str(limit if limit is not None else 'keins'):>7} "
              f"{offen:>18} {erreicht:>16} "
              f"{str(umstritten.get('trades_gesamt', '-')):>8} {abgelehnt:>18}")
    print("-" * 100)

    for b in befunde:
        if b.get("ursache"):
            print(f"  {b['bot']}: {b['ursache']}")
        for fehler in b.get("fehler") or []:
            print(f"  {b['bot']}: FEHLER - {fehler}")
        speicher = b.get("zwischenspeicher") or {}
        if speicher.get("abweichungen"):
            print(f"  {b['bot']}: Signalerzeugung weicht bei "
                  f"{len(speicher['abweichungen'])} Symbolrechnung(en) ab - siehe JSON")
        if speicher.get("kursdaten_abweichungen"):
            print(f"  {b['bot']}: Kursdaten weichen bei "
                  f"{len(speicher['kursdaten_abweichungen'])} Symbol(en) zwischen "
                  f"zwei Ladevorgaengen ab - siehe JSON")

    print()
    print("Erlaeuterung der Spalten:")
    print("  umstr.   Anteil der Trades, die nur in EINEM TEIL der Permutationen")
    print("           ausgefuehrt werden (weder immer noch nie). Ein Bot kann viele")
    print("           Trades ablehnen und trotzdem unempfindlich sein - naemlich")
    print("           dann, wenn es immer dieselben sind.")
    print("  Spannen  ueber alle Permutationen, in Prozent.")
    print()
    print("Diese Pruefung behebt nichts. Sie misst und meldet.")


def zusammenfassung(befunde: list) -> dict:
    return {
        "bots_geprueft": len(befunde),
        "deterministisch": [b["bot"] for b in befunde if b.get("urteil") == DETERMINISTISCH],
        "nur_reihenfolge": [b["bot"] for b in befunde if b.get("urteil") == NUR_REIHENFOLGE],
        "nicht_deterministisch": [b["bot"] for b in befunde if b.get("urteil") == NICHT],
        "unklar": [b["bot"] for b in befunde if b.get("urteil") == UNKLAR],
    }


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Prueft, ob die Backtests bei permutierter Symbolreihenfolge "
                    "dasselbe Ergebnis liefern.")
    zerleger.add_argument("--bot", action="append", default=None,
                          help="nur diesen Bot (mehrfach angebbar)")
    zerleger.add_argument("--perms", type=int, default=None,
                          help=f"Anzahl Permutationen (Voreinstellung {PERMUTATIONEN}, "
                               f"Lauf 0 ist immer die Originalreihenfolge)")
    zerleger.add_argument("--seed", type=int, default=SEED)
    zerleger.add_argument("--pruef-laeufe", type=int, default=None,
                          help="so viele Wiederholungen trotz Zwischenspeicher "
                               "voll nachrechnen")
    zerleger.add_argument("--voll", action="store_true",
                          help="Zwischenspeicher abschalten - jede Permutation "
                               "rechnet komplett neu")
    zerleger.add_argument("--schnell", action="store_true",
                          help=f"{SCHNELL_PERMUTATIONEN} Permutationen statt "
                               f"{PERMUTATIONEN} - fuer die regelmaessige Pruefung")
    zerleger.add_argument("--nur-auswahl", action="store_true",
                          help="Rueckgabewert 1 nur, wenn die AUSWAHL der Trades "
                               "schwankt - ein reiner Reihenfolgeunterschied im "
                               "Kapitalpfad zaehlt dann nicht als Befund")
    zerleger.add_argument("--json", metavar="PFAD", default=None,
                          help="Gesamtbericht als JSON ablegen")
    zerleger.add_argument("--ausgabe", metavar="ORDNER", default=None,
                          help="je Bot eine JSON-Datei ablegen")
    zerleger.add_argument("--basis", metavar="ORDNER", default=None,
                          help="andere Projektwurzel (fuer die Selbsttests)")
    args = zerleger.parse_args(argv)

    strategien = (os.path.join(args.basis, "strategies") if args.basis
                  else STRATEGIES_DIR)

    perms = args.perms if args.perms is not None else (
        SCHNELL_PERMUTATIONEN if args.schnell else PERMUTATIONEN)
    pruef_laeufe = args.pruef_laeufe if args.pruef_laeufe is not None else (
        SCHNELL_PRUEF_LAEUFE if args.schnell else PRUEF_LAEUFE)

    if perms < 2:
        print("--perms muss mindestens 2 sein (Original plus eine Permutation).",
              file=sys.stderr)
        return 2

    bots = args.bot or finde_bots(strategien)
    unbekannt = [b for b in bots if not os.path.exists(
        os.path.join(strategien, b, "equity_simulation.py"))]
    if unbekannt:
        print(f"Unbekannter Bot: {', '.join(unbekannt)}", file=sys.stderr)
        return 2
    if not bots:
        print("Keine Bots mit equity_simulation.py gefunden.", file=sys.stderr)
        return 2

    print(f"{len(bots)} Bot(s), {perms} Permutationen je Bot, Startwert {args.seed}"
          f"{', ohne Zwischenspeicher' if args.voll else ''}"
          f"{', Schnellmodus' if args.schnell else ''}.\n")

    begonnen = time.time()
    befunde = []
    for bot in bots:
        befund = pruefe_bot(bot, perms, args.seed, pruef_laeufe, args.voll,
                            args.basis)
        befunde.append(befund)
        print(f"  {bot:<28} {befund.get('urteil', UNKLAR):<22} "
              f"{befund.get('wanduhr_s', 0):>6.1f}s")
    dauer = time.time() - begonnen
    print()

    berichte(befunde)
    print(f"\nGesamtlaufzeit: {dauer:.1f}s")

    if args.ausgabe:
        os.makedirs(args.ausgabe, exist_ok=True)
        for b in befunde:
            with open(os.path.join(args.ausgabe, f"{b['bot']}.json"), "w") as f:
                json.dump(b, f, indent=2, default=str)
        print(f"Je Bot abgelegt unter: {args.ausgabe}")

    gesamt = {
        "erzeugt_am": time.strftime("%Y-%m-%d %H:%M:%S"),
        "permutationen": perms,
        "seed": args.seed,
        "voll_modus": args.voll,
        "laufzeit_s": round(dauer, 1),
        "zusammenfassung": zusammenfassung(befunde),
        "befunde": befunde,
    }
    if args.json:
        with open(args.json, "w") as f:
            json.dump(gesamt, f, indent=2, default=str)
        print(f"Gesamtbericht: {args.json}")

    ausloeser = ERNSTE_URTEILE if args.nur_auswahl else BEFUND_URTEILE
    return 1 if any(b.get("urteil", UNKLAR) in ausloeser for b in befunde) else 0


if __name__ == "__main__":
    sys.exit(main())
