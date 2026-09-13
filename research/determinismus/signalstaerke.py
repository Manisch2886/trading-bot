"""
Wie fein ist die Signalstaerke, wenn sie zuteilen soll?
==============================================================================
    python3 research/determinismus/signalstaerke.py                  # alle Bots
    python3 research/determinismus/signalstaerke.py elliott_wave_stocks

Diese Untersuchung **misst und meldet**. Sie fasst keinen Bot-Code an und
schreibt nichts ins Repo (`RESULTS_DIR` zeigt waehrend des Laufs in einen
temporaeren Ordner, wie in `shared/kurven_lauf.py`).

DIE FRAGE
------------------------------------------------------------------------------
`shared/determinismus.py` zeigt: bei acht von neun Bots entscheidet die
Symbolreihenfolge, welches von mehreren gleichzeitigen Signalen den freien
Platz bekommt. Der naheliegende Vorschlag ist eine **Zuteilung nach
Signalstaerke** statt nach Dateireihenfolge.

Ob das trägt, haengt an einer Zahl: **wie viele verschiedene Werte kann die
Signalstaerke ueberhaupt annehmen?** Eine Rangregel, die die meisten
Gleichstaende nicht aufloest, verschiebt das Problem nur.

Bei `elliott_wave_stocks` ist die Signalstaerke der `fib_score`. Er ist eine
Summe aus drei festen Teilpunkten (0,34 / 0,33 / 0,33) auf zwei Stellen
gerundet und kann oberhalb von `min_fib_score = 0.3` nur **fuenf** Werte
annehmen: 0,33 / 0,34 / 0,66 / 0,67 / 1,0 (so steht es seit TB-20 im
Kommentar von `elliott_wave_counter.py`).

WAS GEMESSEN WIRD
------------------------------------------------------------------------------
Aus dem unveraenderten Trade-Satz des Bots:

* wie viele Trades mit mindestens einem anderen denselben Einstiegszeitpunkt
  teilen (nur die konkurrieren ueberhaupt um einen Platz),
* wie gross die groesste solche Gruppe ist,
* und - falls der Bot eine Staerkespalte liefert - wie viele Trades **nach**
  einer Rangregel auf dieser Spalte immer noch gleichauf laegen.

Die letzte Zahl ist die Antwort: sie ist der Rest, den eine Zuteilung nach
Signalstaerke NICHT entscheidet.

ABGRENZUNG
------------------------------------------------------------------------------
Gemessen wird die **Aufloesung** der Staerkespalte, nicht ihre Guete. Ob ein
hoeherer `fib_score` tatsaechlich den besseren Trade anzeigt, ist eine andere
Frage und hier nicht untersucht. TB-20 hat die Rangfolge zwischen mehreren
Wellenmustern **eines** Symbols bereits benannt (`fib_score`, dann `end_time`,
dann `start_time`); hier geht es um die Zuteilung zwischen **verschiedenen
Symbolen** zum selben Zeitpunkt - dort hilft `end_time` nicht weiter, weil
alle Bewerber denselben Balken teilen.
"""

import contextlib
import io
import json
import os
import runpy
import sys
import tempfile

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_DIR))
SHARED_DIR = os.path.join(BASE_DIR, "shared")
sys.path.insert(0, SHARED_DIR)

import determinismus_lauf as dl                                # noqa: E402

# Spalten, die als "Signalstaerke" in Frage kommen - je Bot die eine, die der
# Bot selbst mitfuehrt. Fehlt sie, wird das gemeldet statt eine erfunden.
STAERKESPALTE = {
    "elliott_wave": "fib_score",
    "elliott_wave_stocks": "fib_score",
}


def messe(bot: str) -> dict:
    import pandas as pd

    strategie_dir = os.path.join(BASE_DIR, "strategies", bot)
    skript = os.path.join(strategie_dir, "equity_simulation.py")
    ziel = tempfile.mkdtemp(prefix=f"signalstaerke_{bot}_")

    sys.path.insert(0, strategie_dir)
    dl._stubs_setzen()
    dl._results_dir_umlenken(ziel)
    os.chdir(strategie_dir)

    with contextlib.redirect_stdout(io.StringIO()):
        globalen = runpy.run_path(skript, run_name="__main__")

    trades = globalen["trades"]
    gruppen = trades.groupby(pd.to_datetime(trades["entry_time"]), sort=False)

    groessen = gruppen.size()
    gleichzeitig = int(groessen[groessen > 1].sum())
    gesamt = int(len(trades))

    ergebnis = {
        "bot": bot,
        "trades": gesamt,
        "zeitpunkte": int(len(groessen)),
        "trades_mit_gleichem_einstieg": gleichzeitig,
        "anteil_pct": round(gleichzeitig / gesamt * 100, 1) if gesamt else 0.0,
        "groesste_gruppe": int(groessen.max()) if len(groessen) else 0,
        "positionslimit": globalen.get("MAX_CONCURRENT_POSITIONS"),
        "staerkespalte": STAERKESPALTE.get(bot),
    }

    spalte = STAERKESPALTE.get(bot)
    if spalte is None or spalte not in trades.columns:
        ergebnis["hinweis"] = ("kein Mass fuer Signalstaerke im Trade-Satz - eine "
                               "Zuteilung nach Staerke muesste hier erst eines "
                               "einfuehren")
        return ergebnis

    werte = trades[spalte].round(6)
    ergebnis["verschiedene_werte"] = int(werte.nunique())
    ergebnis["werte"] = sorted(float(w) for w in werte.unique())[:12]

    # Der Rest, den die Staerkespalte NICHT entscheidet: innerhalb jeder
    # Gruppe gleichzeitiger Einstiege bleibt je Staerkewert alles ausser einem
    # Trade gleichauf.
    rest = 0
    for _, gruppe in gruppen:
        if len(gruppe) < 2:
            continue
        for _, teil in gruppe.groupby(gruppe[spalte].round(6)):
            if len(teil) > 1:
                rest += len(teil) - 1
    ergebnis["nach_rangregel_noch_gleichauf"] = rest
    ergebnis["nach_rangregel_noch_gleichauf_pct"] = (
        round(rest / gesamt * 100, 1) if gesamt else 0.0)
    ergebnis["von_den_gleichzeitigen_pct"] = (
        round(rest / gleichzeitig * 100, 1) if gleichzeitig else 0.0)
    return ergebnis


def main(argv=None) -> int:
    import subprocess

    bots = list(argv or sys.argv[1:])
    ziel = None
    if "--json" in bots:
        i = bots.index("--json")
        ziel = bots[i + 1]
        del bots[i:i + 2]
    if not bots:
        bots = sorted(n for n in os.listdir(os.path.join(BASE_DIR, "strategies"))
                      if os.path.exists(os.path.join(BASE_DIR, "strategies", n,
                                                      "equity_simulation.py")))

    if len(bots) > 1:
        # Ein Prozess je Bot - neun gleichnamige equity_simulation.py
        # kollidieren in sys.modules.
        befunde = []
        for bot in bots:
            kind = subprocess.run([sys.executable, os.path.abspath(__file__), bot],
                                  capture_output=True, text=True, cwd=BASE_DIR)
            for zeile in reversed(kind.stdout.splitlines()):
                if zeile.startswith("__SIGNALSTAERKE__ "):
                    befunde.append(json.loads(zeile[len("__SIGNALSTAERKE__ "):]))
                    break
            else:
                befunde.append({"bot": bot, "fehler": (kind.stderr or "")[-300:]})
        berichte(befunde)
        if ziel:
            with open(ziel, "w") as f:
                json.dump(befunde, f, indent=2, default=str)
            print(f"Abgelegt: {ziel}")
        return 0

    ergebnis = messe(bots[0])
    print("__SIGNALSTAERKE__ " + json.dumps(ergebnis, default=str))
    berichte([ergebnis])
    if ziel:
        with open(ziel, "w") as f:
            json.dump([ergebnis], f, indent=2, default=str)
    return 0


def berichte(befunde: list):
    print()
    print("=" * 96)
    print("AUFLOESUNG DER SIGNALSTAERKE BEI GLEICHZEITIGEN EINSTIEGEN")
    print("=" * 96)
    print(f"{'Bot':<28} {'Trades':>7} {'gleichzeitig':>13} {'groesste':>9} "
          f"{'Staerke':>10} {'Stufen':>7} {'bleibt gleichauf':>18}")
    print("-" * 96)
    for b in befunde:
        if b.get("fehler"):
            print(f"{b['bot']:<28} FEHLER: {b['fehler'][:60]}")
            continue
        rest = b.get("nach_rangregel_noch_gleichauf")
        rest_text = ("-" if rest is None else
                     f"{rest} ({b.get('von_den_gleichzeitigen_pct', 0)}%)")
        gleichzeitig = f"{b['trades_mit_gleichem_einstieg']} ({b['anteil_pct']}%)"
        print(f"{b['bot']:<28} {b['trades']:>7} {gleichzeitig:>13} "
              f"{b['groesste_gruppe']:>9} {str(b.get('staerkespalte') or '-'):>10} "
              f"{str(b.get('verschiedene_werte') or '-'):>7} {rest_text:>18}")
    print("-" * 96)
    print("gleichzeitig       Trades, die ihren Einstiegszeitpunkt mit mindestens einem")
    print("                   anderen teilen - nur sie konkurrieren um einen freien Platz.")
    print("Stufen             verschiedene Werte, die die Staerkespalte annimmt.")
    print("bleibt gleichauf   Trades, die eine Rangregel auf der Staerkespalte NICHT")
    print("                   entscheidet - der Rest, fuer den weiterhin etwas anderes")
    print("                   entscheiden muesste.")
    print()
    print("Diese Untersuchung misst und meldet. Sie loest nichts.")


if __name__ == "__main__":
    sys.exit(main())
