#!/usr/bin/env python3
"""
Selbsttest der gemeinsamen Messkette (TB-28)
==============================================================================
`shared/messkette.py` zieht zwei Rechnungen an eine Stelle, die bis TB-28
neunmal zeichengleich in den `strategies/*/equity_simulation.py` standen: das
Drawdown-Mass und die Renditeformel. Dieser Test haelt zwei Zusicherungen
nach - beide **am Verhalten**, nicht am Quelltext:

  A. **Die Rechnung hat sich nicht geaendert.** Die gemeinsame Fassung liefert
     auf denselben Eingaben dieselben Zahlen wie die bis TB-28 gueltige,
     hier woertlich hinterlegte Formel.
  B. **Es ist wirklich EINE Stelle.** Wird `shared/messkette.py` verfaelscht,
     rechnet JEDER der neun Bots verfaelscht mit. Ein Bot, der still eine
     eigene Kopie behalten haette, faellt hier durch.

Dazu kommen die drei Abhaengigkeiten, die TB-27 als tragend benannt hat und
die diese Aenderung nicht brechen darf: die Signaturabfrage auf
`simulate_portfolio` (zwoelf Stellen im Repo), der schreibende Weg ueber
`notifications/manual_close.py::allokation()` und die Bot-Liste ueber die
Dateiexistenz.

ZU DEN MUTATIONSPROBEN - WARUM SIE SO GEBAUT SIND
------------------------------------------------------------------------------
Zwei Fallen sind in diesem Projekt wiederholt aufgetreten (#73, #77, #78, #79,
#81, #86, TB-15, TB-20, TB-22, TB-26), und der Waechter aus TB-27 ist ihnen in
genau dieser Aenderung selbst zum Opfer gefallen:

1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst.** `research/tb27_kapitalsimulation/test_vergleich.py` verfaelschte
   bis TB-28 die Zeile `capital_series.cummax()` in einer Kopie der neun
   Dateien. Genau diese Zeile ist durch TB-28 aus den neun Dateien
   verschwunden - die Verfaelschung haette ab sofort ins Leere gegriffen und
   der Test waere trotzdem gruen geblieben. Aufgefallen ist es nur, weil jene
   Probe **den Ablauf beobachtet**: `pruefe("die Verfaelschung greift
   ueberhaupt", verfaelscht != text)`.

   Deshalb hier dasselbe Muster, zweistufig: jede Mutationsprobe belegt
   erst, dass sie **ohne** Mutation den echten Wert sieht, und dann, dass sie
   **mit** Mutation den verfaelschten sieht. Bliebe eine der beiden Richtungen
   ungeprueft, koennte die Probe stumm sein, ohne dass man es merkt.

2. **Eine zweite Wache verdeckt das Fehlen der ersten.** Deshalb laeuft jede
   Bot-Probe in einem **eigenen Unterprozess** mit **einer** Frage, und die
   Zusicherung "es ist eine Stelle" wird NICHT ueber den Quelltext gestuetzt
   (kein `grep` auf `from messkette import`, kein AST-Vergleich). Ein
   Quelltext-Beleg wuerde hier gruen bleiben, auch wenn der Import wirkungslos
   waere - etwa weil eine spaetere Zeile die Funktion wieder ueberschreibt.
   Geprueft wird ausschliesslich, welche Zahl herauskommt.

Der Test schreibt nichts ins Repo. Er braucht `pandas`; die Bot-Proben
brauchen zusaetzlich die Kursdaten unter `data/` und die
Modul-Ersatzstuecke aus `shared/kurven_lauf.py`.

    python3 shared/test_messkette.py            # alle Proben
    python3 shared/test_messkette.py --schnell  # ohne die drei __main__-Laeufe

Rueckgabewert 0, wenn alle Pruefungen bestehen, sonst 1.
"""

import json
import os
import subprocess
import sys
import tempfile

import pandas as pd

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)
STRATEGIES_DIR = os.path.join(BASE_DIR, "strategies")
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

import messkette

bestanden = 0
gescheitert = []


def pruefe(was, bedingung, hinweis=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print(f"  OK    {was}")
    else:
        gescheitert.append(was)
        print(f"  FEHLT {was}" + (f"   [{hinweis}]" if hinweis else ""))


def bots():
    """Dieselbe Bot-Liste wie `shared/ergebniskurven.py`: alle Ordner unter
    strategies/ mit einer equity_simulation.py. Nicht hart codiert."""
    return sorted(n for n in os.listdir(STRATEGIES_DIR)
                  if os.path.isfile(os.path.join(STRATEGIES_DIR, n, "equity_simulation.py")))


# ---------------------------------------------------------------------------
# A. Die Rechnung hat sich nicht geaendert
# ---------------------------------------------------------------------------
# Die Fassung, die bis TB-28 neunmal ZEICHENGLEICH in den
# strategies/*/equity_simulation.py stand (TB-27, Abschnitt 2.3). Sie steht
# hier woertlich, damit die Gleichheit gegen den HISTORISCHEN Stand geprueft
# wird und nicht gegen sich selbst.
def _fassung_bis_tb27(equity_df, starting_capital):
    if equity_df.empty:
        return 0.0
    capital_series = pd.concat([pd.Series([starting_capital]), equity_df["capital_after"]],
                               ignore_index=True)
    running_max = capital_series.cummax()
    drawdown_pct = (capital_series - running_max) / running_max * 100
    return round(drawdown_pct.min(), 2)


def _rendite_bis_tb27(endkapital, startkapital):
    return (endkapital / startkapital - 1) * 100


KURVEN = {
    "leer": [],
    "nur Gewinne": [10500.0, 11000.0, 13000.0],
    "nur Verluste": [9500.0, 9000.0, 4000.0],
    "Verlust im ersten Trade": [9000.0, 12000.0],
    "Rueckgang nach Hoechststand": [12000.0, 9600.0, 15000.0],
    "unveraendert": [10000.0, 10000.0],
    "ein einziger Trade": [8888.88],
    "tiefster Punkt am Ende": [11000.0, 12000.0, 5000.0],
}


def teil_a():
    print("\nA. Liefert die gemeinsame Fassung dieselben Zahlen wie bis TB-27?")
    print("-" * 78)
    for name, werte in KURVEN.items():
        df = pd.DataFrame({"capital_after": werte}, dtype="float64")
        alt = _fassung_bis_tb27(df, 10_000.0)
        neu = messkette.calculate_max_drawdown(df, 10_000.0)
        pruefe(f"Drawdown gleich der Fassung bis TB-27: {name}",
               alt == neu, f"alt={alt!r} neu={neu!r}")

    # Der Anfangswert ist die Stelle, an der diese Formel schon einmal falsch
    # sein KOENNTE: ohne ihn faellt ein Verlust im ersten Trade heraus.
    df = pd.DataFrame({"capital_after": [9000.0, 12000.0]}, dtype="float64")
    pruefe("ein Verlust im ERSTEN Trade zaehlt mit (-10.0, nicht 0.0)",
           messkette.calculate_max_drawdown(df, 10_000.0) == -10.0,
           str(messkette.calculate_max_drawdown(df, 10_000.0)))

    for endkapital in (16_777.45, 10_000.0, 4_000.0, 51_907.0):
        pruefe(f"Rendite gleich der Fassung bis TB-27: Endkapital {endkapital:,.2f}",
               messkette.rendite_pct(endkapital, 10_000.0)
               == _rendite_bis_tb27(endkapital, 10_000.0))

    # Ungerundet ist eine Zusicherung, kein Zufall: rundete diese Funktion,
    # muesste einer ihrer drei Verbraucher sein heutiges Verhalten aufgeben.
    pruefe("rendite_pct rundet NICHT (67.7745 bleibt 67.7745)",
           messkette.rendite_pct(16_777.45, 10_000.0) == 67.7745,
           str(messkette.rendite_pct(16_777.45, 10_000.0)))
    pruefe("calculate_max_drawdown rundet dagegen auf zwei Stellen",
           messkette.calculate_max_drawdown(
               pd.DataFrame({"capital_after": [9876.5432]}, dtype="float64"),
               10_000.0) == -1.23)
    pruefe("die leere Kurve gibt 0.0 (kein Rueckgang), nicht None",
           messkette.calculate_max_drawdown(pd.DataFrame(), 10_000.0) == 0.0)


# ---------------------------------------------------------------------------
# B. Die beiden Nachrechner in shared/
# ---------------------------------------------------------------------------
def teil_b():
    print("\nB. Rechnen die beiden Werkzeuge in shared/ dasselbe wie die Bots?")
    print("-" * 78)
    import ergebniskurven

    for name, werte in KURVEN.items():
        if not werte:
            continue
        df = pd.DataFrame({"time": pd.date_range("2024-01-01", periods=len(werte)),
                           "capital_after": werte})
        k = ergebniskurven.kennzahlen(df, 10_000.0)
        bot_dd = messkette.calculate_max_drawdown(df, 10_000.0)
        pruefe(f"kennzahlen() und der Bot melden denselben Drawdown: {name}",
               k["max_drawdown_pct"] == bot_dd, f"{k['max_drawdown_pct']!r} vs {bot_dd!r}")
        pruefe(f"kennzahlen() und der Bot melden dieselbe Rendite: {name}",
               k["rendite_pct"] == round(messkette.rendite_pct(werte[-1], 10_000.0), 2))

    # Der EINE Unterschied, den TB-28 gefunden und BEWUSST stehen gelassen
    # hat: derselbe Wert, ein anderer Typ (TB-27, U10). Er wird hier
    # festgehalten, nicht wegdefiniert - wer ihn spaeter angleicht, soll das
    # als Entscheidung tun und nicht aus Versehen.
    df = pd.DataFrame({"time": pd.date_range("2024-01-01", periods=2),
                       "capital_after": [9000.0, 12000.0]})
    k = ergebniskurven.kennzahlen(df, 10_000.0)
    pruefe("kennzahlen() liefert `float`, der Bot `numpy.float64` - gleicher "
           "Wert, anderer Typ (offener Punkt aus TB-28)",
           type(k["max_drawdown_pct"]) is float
           and type(messkette.calculate_max_drawdown(df, 10_000.0)) is not float
           and k["max_drawdown_pct"] == messkette.calculate_max_drawdown(df, 10_000.0))

    # Die leere Kurve ist der zweite bewusst belassene Unterschied.
    leer = ergebniskurven.kennzahlen(pd.DataFrame(), 10_000.0)
    pruefe("kennzahlen() meldet fuer die leere Kurve None, der Bot 0.0",
           leer["max_drawdown_pct"] is None
           and messkette.calculate_max_drawdown(pd.DataFrame(), 10_000.0) == 0.0)


# ---------------------------------------------------------------------------
# C. Es ist wirklich EINE Stelle - die Mutationsprobe je Bot
# ---------------------------------------------------------------------------
# Der Ersatz wird VOR dem Import des Bots als `sys.modules["messkette"]`
# hinterlegt. Das ist derselbe Weg, auf dem `shared/kurven_lauf.py` seit je
# `strategy_paths` umlenkt - und der einzige, der zuverlaessig greift: der Bot
# schiebt `shared/` beim Import selbst an den Anfang von `sys.path`, ein
# vorgelagerter Ordner wuerde also uebergangen.
_BOT_PROBE = r'''
import json, os, sys, types

BASE = %(base)r
BOT = sys.argv[1]
MUTATION = float(sys.argv[2])          # 0.0 = unveraendert

sd = os.path.join(BASE, "strategies", BOT)
sh = os.path.join(BASE, "shared")
sys.path.insert(0, sd)
sys.path.insert(0, sh)

import kurven_lauf                      # bringt die Modul-Ersatzstuecke mit
kurven_lauf._stubs_setzen()

import messkette as echt
if MUTATION:
    ersatz = types.ModuleType("messkette")
    ersatz.max_drawdown_ungerundet = echt.max_drawdown_ungerundet
    ersatz.calculate_max_drawdown = (
        lambda df, start: echt.calculate_max_drawdown(df, start) + MUTATION)
    ersatz.rendite_pct = (
        lambda ende, start: echt.rendite_pct(ende, start) + MUTATION)
    sys.modules["messkette"] = ersatz

os.chdir(sd)
import importlib, inspect
import pandas as pd
es = importlib.import_module("equity_simulation")

df = pd.DataFrame({"capital_after": [9000.0, 12000.0]}, dtype="float64")
print("__PROBE__ " + json.dumps({
    "bot": BOT,
    "drawdown": float(es.calculate_max_drawdown(df, 10_000.0)),
    "rendite": float(es.rendite_pct(12_000.0, 10_000.0)),
    "signatur": list(inspect.signature(es.simulate_portfolio).parameters),
    "co_varnames": list(es.simulate_portfolio.__code__.co_varnames),
    "allocation_pct": es.ALLOCATION_PCT,
}))
'''


def _probe(skript, bot, mutation):
    lauf = subprocess.run([sys.executable, skript, bot, str(mutation)],
                          capture_output=True, text=True, cwd=BASE_DIR)
    for zeile in lauf.stdout.splitlines():
        if zeile.startswith("__PROBE__ "):
            return json.loads(zeile[len("__PROBE__ "):])
    raise RuntimeError(f"{bot} (Mutation {mutation}): keine Antwort.\n"
                       f"{lauf.stderr.strip()[-600:] or lauf.stdout.strip()[-600:]}")


def teil_c(skript):
    print("\nC. Verfaelscht man shared/messkette.py, rechnen ALLE NEUN falsch")
    print("-" * 78)
    # Ein Wert, der in keiner echten Rechnung vorkommen kann und den auch eine
    # Rundung nicht erzeugt - eine Mutation, die zufaellig den richtigen Wert
    # traefe, waere eine stumme Probe.
    MUT = 7.77
    # 12.000 auf 10.000 sind 20 % - aber `(12000/10000 - 1) * 100` ergibt in
    # Gleitkomma 19.999999999999996. Deshalb wird hier gerundet verglichen;
    # ungerundet zu vergleichen waere eine Probe, die aus dem falschen Grund
    # rot wird.
    ECHT_DD, ECHT_RENDITE = -10.0, 20.0

    for bot in bots():
        ohne = _probe(skript, bot, 0.0)
        mit = _probe(skript, bot, MUT)

        # Richtung 1 - die Probe sieht ohne Mutation den echten Wert. Ohne
        # diese Haelfte koennte sie stumm sein, ohne dass es auffaellt.
        pruefe(f"{bot}: ohne Mutation der echte Drawdown ({ECHT_DD})",
               ohne["drawdown"] == ECHT_DD, repr(ohne["drawdown"]))
        # Richtung 2 - mit Mutation traegt der Wert die Marke. Haette dieser
        # Bot noch eine eigene Kopie, bliebe er hier beim echten Wert.
        pruefe(f"{bot}: mit Mutation traegt der Drawdown die Marke "
               f"({ECHT_DD} + {MUT})",
               round(mit["drawdown"] - ohne["drawdown"], 6) == MUT,
               f"{ohne['drawdown']!r} -> {mit['drawdown']!r}")
        pruefe(f"{bot}: mit Mutation traegt auch die Rendite die Marke",
               round(mit["rendite"] - ohne["rendite"], 6) == MUT
               and round(ohne["rendite"], 6) == ECHT_RENDITE,
               f"{ohne['rendite']!r} -> {mit['rendite']!r}")


# ---------------------------------------------------------------------------
# D. Was diese Aenderung nicht brechen darf
# ---------------------------------------------------------------------------
def teil_d(skript):
    print("\nD. Die tragenden Abhaengigkeiten aus TB-27")
    print("-" * 78)

    print("\n  D1. Die Signaturabfrage - zwoelf Stellen erkennen daran, welcher")
    print("      Bot KEIN Positionslimit hat (TB-27, Abschnitt 5.1)")
    ohne_limit, mit_limit = [], []
    for bot in bots():
        antwort = _probe(skript, bot, 0.0)
        # Beide Formen werden im Repo benutzt: `inspect.signature(...)`
        # (drei Stellen) und `co_varnames` (neun). Sie muessen dasselbe sagen.
        per_signatur = "max_concurrent_positions" in antwort["signatur"]
        per_varnames = "max_concurrent_positions" in antwort["co_varnames"]
        pruefe(f"{bot}: inspect.signature und co_varnames stimmen ueberein",
               per_signatur == per_varnames)
        (mit_limit if per_signatur else ohne_limit).append(bot)

    pruefe("GENAU EIN Bot hat kein Positionslimit, und es ist elliott_wave",
           ohne_limit == ["elliott_wave"], str(ohne_limit))
    pruefe("die uebrigen ACHT haben eines", len(mit_limit) == 8, str(mit_limit))

    print("\n  D2. Der SCHREIBENDE Weg: notifications/manual_close.py liest")
    print("      ALLOCATION_PCT fuer alle neun (Schliess-Dialog des Dashboards)")
    sys.path.insert(0, os.path.join(BASE_DIR, "notifications"))
    import manual_close
    # Fuer diese drei ist equity_simulation.py die EINZIGE Quelle: ihre
    # live_params.py fuehrt den Wert nicht. Ginge das Literal dort verloren,
    # zeigte der Bestaetigungsdialog keine Positionsgroesse mehr.
    NUR_AUS_EQUITY_SIM = {"elliott_wave", "elliott_wave_stocks", "t3_supertrend"}
    for bot in bots():
        a = manual_close.allokation(bot)
        pruefe(f"{bot}: allokation() liefert einen Anteil",
               a["anteil"] is not None and 0 < a["anteil"] <= 1,
               str(a))
        if bot in NUR_AUS_EQUITY_SIM:
            pruefe(f"{bot}: die Quelle ist weiterhin equity_simulation.py",
                   a["quelle"] == "equity_simulation.py", str(a))

    print("\n  D3. Die Bot-Liste ueber die Dateiexistenz (drei Werkzeuge)")
    pruefe("es sind weiterhin neun equity_simulation.py an ihren Pfaden",
           len(bots()) == 9, str(bots()))
    pruefe("keine davon ist nach shared/ gewandert",
           not os.path.exists(os.path.join(_SHARED_DIR, "equity_simulation.py")))


# ---------------------------------------------------------------------------
# E. Der __main__-Block benutzt die gemeinsame Fassung wirklich
# ---------------------------------------------------------------------------
# Teil C prueft das Modul; hier laeuft der `__main__`-Block selbst. Das ist
# der Weg, den `shared/kurven_lauf.py` und `shared/determinismus_lauf.py`
# nehmen, und der einzige Ort, an dem die Renditeformel tatsaechlich
# ausgewertet wird. Drei Bots genuegen und halten die Laufzeit unten:
# der schnellste Krypto-Bot, der mit dem Regimefilter, und der ohne
# Positionslimit.
_MAIN_PROBE = r'''
import contextlib, io, os, re, runpy, sys, tempfile, types

BASE = %(base)r
BOT = sys.argv[1]
MUTATION = float(sys.argv[2])

sd = os.path.join(BASE, "strategies", BOT)
sh = os.path.join(BASE, "shared")
sys.path.insert(0, sd)
sys.path.insert(0, sh)

import kurven_lauf
kurven_lauf._stubs_setzen()
ziel = tempfile.mkdtemp(prefix="tb28_")
kurven_lauf._results_dir_umlenken(ziel)

import messkette as echt
if MUTATION:
    ersatz = types.ModuleType("messkette")
    ersatz.max_drawdown_ungerundet = echt.max_drawdown_ungerundet
    ersatz.calculate_max_drawdown = (
        lambda df, start: echt.calculate_max_drawdown(df, start) + MUTATION)
    ersatz.rendite_pct = (
        lambda ende, start: echt.rendite_pct(ende, start) + MUTATION)
    sys.modules["messkette"] = ersatz

os.chdir(sd)
puffer = io.StringIO()
with contextlib.redirect_stdout(puffer):
    runpy.run_path(os.path.join(sd, "equity_simulation.py"), run_name="__main__")
ausgabe = puffer.getvalue()

rendite = re.search(r"Gesamtrendite:\s+(-?[\d.]+)%%", ausgabe)
drawdown = re.search(r"Max Drawdown \(Kapital\):\s+(-?[\d.]+)%%", ausgabe)
print("__MAIN__ %%s %%s" %% (rendite.group(1) if rendite else "?",
                           drawdown.group(1) if drawdown else "?"))
'''


def _main_probe(skript, bot, mutation):
    lauf = subprocess.run([sys.executable, skript, bot, str(mutation)],
                          capture_output=True, text=True, cwd=BASE_DIR)
    for zeile in lauf.stdout.splitlines():
        if zeile.startswith("__MAIN__ "):
            r, d = zeile.split()[1:3]
            return float(r), float(d)
    raise RuntimeError(f"{bot} (Mutation {mutation}): kein __main__-Ergebnis.\n"
                       f"{lauf.stderr.strip()[-600:] or lauf.stdout.strip()[-600:]}")


def teil_e(skript):
    print("\nE. Auch der __main__-Block rechnet mit der gemeinsamen Fassung")
    print("-" * 78)
    MUT = 7.77
    for bot in ("rsi2_crypto", "volatility_breakout_crypto", "elliott_wave"):
        r0, d0 = _main_probe(skript, bot, 0.0)
        r1, d1 = _main_probe(skript, bot, MUT)
        pruefe(f"{bot}: ohne Mutation meldet der Lauf ueberhaupt Zahlen",
               r0 == r0 and d0 == d0 and d0 < 0, f"{r0} / {d0}")
        pruefe(f"{bot}: die gedruckte Gesamtrendite traegt die Marke",
               round(r1 - r0, 2) == MUT, f"{r0} -> {r1}")
        pruefe(f"{bot}: der gedruckte Max Drawdown traegt die Marke",
               round(d1 - d0, 2) == MUT, f"{d0} -> {d1}")


def main():
    schnell = "--schnell" in sys.argv
    print(__doc__.strip().split("\n")[0])
    if schnell:
        print("(--schnell: die drei __main__-Laeufe aus Teil E entfallen)")

    with tempfile.TemporaryDirectory() as ordner:
        bot_skript = os.path.join(ordner, "bot_probe.py")
        with open(bot_skript, "w", encoding="utf-8") as f:
            f.write(_BOT_PROBE % {"base": BASE_DIR})
        main_skript = os.path.join(ordner, "main_probe.py")
        with open(main_skript, "w", encoding="utf-8") as f:
            f.write(_MAIN_PROBE % {"base": BASE_DIR})

        teil_a()
        teil_b()
        teil_c(bot_skript)
        teil_d(bot_skript)
        if not schnell:
            teil_e(main_skript)

    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
