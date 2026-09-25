#!/usr/bin/env python3
"""
Selbsttest zu TB-105 Block B: die Regimewache an den drei Einbaustellen
==============================================================================
Register 11.1: an den drei Stellen aus `regimewache.EINBAUSTELLEN` bricht ein
Lauf ab, wenn BTCUSDT fehlt - er rechnet nicht still ohne den Filter weiter.
`shared/test_regimewache.py` prueft die Wache selbst und (Teil C/D) den
Quelltext; hier wird das VERHALTEN der eingebauten Stellen geprueft, am
echten Bot-Code und an echten Kursdaten aus `data/`.

Teil A  Je Einbaustelle: BTCUSDT fehlt => Abbruch mit `RegimefilterFehlt`.
Teil B  Je Einbaustelle: BTCUSDT da    => kein Abbruch (Gegenprobe zu A).
Teil C  Mutationsproben: der Einbau wird in einer Kopie des Bot-Ordners
        zurueckgenommen - je Mutation genau EINE Stelle (24b B3). Die Probe
        aus Teil A muss dann rot werden. Gegenprobe: dieselbe Kopie ohne
        Mutation ist gruen (die Kopie selbst verfaelscht nichts).

Jede Probe laeuft in einem EIGENEN Prozess: die neun Bots fuehren
gleichnamige Module (TB-40), und ein zweiter Import im selben Prozess
lieferte das erste Modul zurueck.

Aufruf:  python3 shared/test_regimewache_einbau.py      (ohne Modus)
"""

import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_HIER)
sys.path.insert(0, _HIER)

import regimewache as rw  # noqa: E402

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


# Die Probe, die im Kindprozess laeuft. Argumente: Wurzel, Bot, Stelle,
# "mit" oder "ohne" BTCUSDT. Rueckgabe: 3 = Abbruch durch die Wache,
# 0 = weitergerechnet, 4 = anderer SystemExit, 1 = anderer Fehler.
PROBE = r'''
import contextlib, io, os, sys
wurzel, bot, stelle, btc = sys.argv[1:5]
sys.path.insert(0, os.path.join(wurzel, "strategies", bot))
sys.path.insert(0, os.path.join(wurzel, "shared"))
with contextlib.redirect_stdout(io.StringIO()):
    import equity_simulation as es
    import multi_symbol_optimise as mso
    alle = mso.load_all_symbol_data()
# Zwei Symbole reichen, damit es Trades gibt und die Stelle erreicht wird.
teil = {s: alle[s] for s in ("ETHUSDT", "SOLUSDT") if s in alle}
if btc == "mit":
    teil["BTCUSDT"] = alle["BTCUSDT"]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        if bot == "t3_supertrend" and stelle == "equity_simulation.py":
            es.collect_all_trades(teil, es.T3_FAST, es.T3_SLOW,
                                  es.ADX_THRESHOLD, es.STOP_LOSS_PCT)
        elif bot == "t3_supertrend" and stelle == "multi_symbol_optimise.py":
            mso.evaluate_combination_multi(teil, es.T3_FAST, es.T3_SLOW,
                                           es.ADX_THRESHOLD, es.STOP_LOSS_PCT)
        elif bot == "volatility_breakout_crypto":
            trades = es.collect_all_trades(teil, es.STOP_LOSS_PCT)
            if trades.empty:
                print("KEINE TRADES", file=sys.stderr)
                sys.exit(1)
            es.apply_btc_regime_filter(trades, teil)
        else:
            raise ValueError(stelle)
except SystemExit as e:
    if type(e).__name__ == "RegimefilterFehlt":
        print("ABBRUCH " + str(e)[:120])
        sys.exit(3)
    print("ANDERER SystemExit " + str(e.code)[:120])
    sys.exit(4)
print("WEITER")
sys.exit(0)
'''

# Je Einbaustelle: Bot, Datei. Aus EINBAUSTELLEN abgeleitet, nicht zweimal
# gefuehrt - kommt eine Stelle hinzu, faellt Teil A1 auf.
STELLEN = [(rel.split(os.sep)[1], rel.split(os.sep)[2])
           for rel in sorted(rw.EINBAUSTELLEN)]

# Mutationen: (Bot, Datei, Name, eingebauter Text, Text ohne Einbau).
# Die t3-Texte sind die Fassung vor TB-105 (`if "BTCUSDT" in all_data:` ohne
# else); bei volatility_breakout_crypto zwei Mutationen: die alte eigene
# Abfrage (bricht ab, aber nicht ueber die Wache) und das stille Ueberspringen.
MUTATIONEN = [
    ("t3_supertrend", "equity_simulation.py", "M1 t3 equity_simulation: Einbau zurueckgenommen",
     '''    btc = btc_daten(all_data, bot="t3_supertrend",
                    holen="python3 fetch_4h_data.py")
    btc_regime = compute_btc_regime(btc)
    combined = filter_trades_by_regime(combined, btc_regime)
''',
     '''    if "BTCUSDT" in all_data:
        btc_regime = compute_btc_regime(all_data["BTCUSDT"])
        combined = filter_trades_by_regime(combined, btc_regime)
'''),
    ("t3_supertrend", "multi_symbol_optimise.py", "M2 t3 multi_symbol_optimise: Einbau zurueckgenommen",
     '''    btc = btc_daten(all_data, bot="t3_supertrend",
                    holen="python3 fetch_4h_data.py")
    btc_regime = compute_btc_regime(btc)
    combined = filter_trades_by_regime(combined, btc_regime)
    contributing_symbols = combined["symbol"].nunique() if not combined.empty else 0
''',
     '''    if "BTCUSDT" in all_data:
        btc_regime = compute_btc_regime(all_data["BTCUSDT"])
        combined = filter_trades_by_regime(combined, btc_regime)
        contributing_symbols = combined["symbol"].nunique() if not combined.empty else 0
'''),
    ("volatility_breakout_crypto", "equity_simulation.py",
     "M3 vbc equity_simulation: alte eigene Abfrage statt der Wache",
     '''    btc = btc_daten(all_data, bot="volatility_breakout_crypto",
                    holen="python3 fetch_1d_data.py",
                    aktiv=BTC_REGIME_FILTER_ENABLED)
    if btc is None:
        return trades
''',
     '''    if not BTC_REGIME_FILTER_ENABLED:
        return trades

    btc = all_data.get("BTCUSDT")
    if btc is None:
        raise SystemExit(
            "BTC_REGIME_FILTER_ENABLED ist aktiv, aber BTCUSDT fehlt in den "
            "Kursdaten - der Regimefilter ist nicht anwendbar. Erst "
            "'python3 fetch_1d_data.py' ausfuehren; ein Lauf ohne Filter "
            "wuerde eine andere Strategie beschreiben als die laufende.")
'''),
    ("volatility_breakout_crypto", "equity_simulation.py",
     "M4 vbc equity_simulation: stilles Ueberspringen",
     '''    btc = btc_daten(all_data, bot="volatility_breakout_crypto",
                    holen="python3 fetch_1d_data.py",
                    aktiv=BTC_REGIME_FILTER_ENABLED)
    if btc is None:
        return trades
''',
     '''    btc = all_data.get("BTCUSDT")
    if btc is None:
        return trades
'''),
]


def probe(wurzel, bot, datei, btc, probedatei):
    lauf = subprocess.run(
        [sys.executable, "-W", "ignore", probedatei, wurzel, bot, datei, btc],
        capture_output=True, text=True, cwd=wurzel)
    return lauf.returncode, (lauf.stdout + lauf.stderr).strip()[-300:]


def kopie(ziel, bot):
    """Wegwerfbaum: <ziel>/strategies/<bot>/*.py kopiert; shared/, data/ und
    config/ als Symlink auf die echten. (`paths.py` bestimmt seine Wurzel aus
    dem nicht aufgeloesten Pfad - ohne data/ und config/ im Wegwerfbaum
    faende der Bot dort keine Kursdaten.)"""
    ordner = os.path.join(ziel, "strategies", bot)
    os.makedirs(ordner)
    quelle = os.path.join(BASE_DIR, "strategies", bot)
    for name in os.listdir(quelle):
        if name.endswith(".py"):
            shutil.copy2(os.path.join(quelle, name), ordner)
    for name in ("shared", "data", "config"):
        if not os.path.exists(os.path.join(ziel, name)):
            os.symlink(os.path.join(BASE_DIR, name), os.path.join(ziel, name))
    return ordner


def main():
    print(__doc__.strip().split("\n")[0])
    arbeit = tempfile.mkdtemp(prefix="tb105_regimewache_")
    try:
        probedatei = os.path.join(arbeit, "probe.py")
        with open(probedatei, "w", encoding="utf-8") as f:
            f.write(PROBE)

        pruefe("A0: EINBAUSTELLEN nennt drei Stellen", len(STELLEN) == 3, str(STELLEN))
        pruefe("A0b: pruefe_einbau() meldet 3 von 3",
               rw.pruefe_einbau(BASE_DIR)["vollstaendig"], str(rw.pruefe_einbau(BASE_DIR)))

        # Teil A und B am echten Repo
        for bot, datei in STELLEN:
            rc, text = probe(BASE_DIR, bot, datei, "ohne", probedatei)
            pruefe(f"A {bot}/{datei}: BTCUSDT fehlt => Abbruch durch die Wache",
                   rc == 3, f"rc {rc}: {text}")
            rc, text = probe(BASE_DIR, bot, datei, "mit", probedatei)
            pruefe(f"B {bot}/{datei}: BTCUSDT da => kein Abbruch",
                   rc == 0, f"rc {rc}: {text}")

        # Teil C: Gegenprobe an der unveraenderten Kopie, dann je Mutation
        # eine frische Kopie mit genau einer Aenderung.
        for bot in sorted({b for b, _ in STELLEN}):
            wurzel = os.path.join(arbeit, "gegen_" + bot)
            kopie(wurzel, bot)
            for b, datei in STELLEN:
                if b != bot:
                    continue
                rc, text = probe(wurzel, bot, datei, "ohne", probedatei)
                pruefe(f"C-Gegenprobe {bot}/{datei}: unveraenderte Kopie bricht ab",
                       rc == 3, f"rc {rc}: {text}")
        for nr, (bot, datei, name, eingebaut, ohne) in enumerate(MUTATIONEN):
            wurzel = os.path.join(arbeit, "mut%d" % nr)
            ordner = kopie(wurzel, bot)
            pfad = os.path.join(ordner, datei)
            with open(pfad, encoding="utf-8") as f:
                text = f.read()
            pruefe(f"{name}: Mutationsstelle genau einmal gefunden",
                   text.count(eingebaut) == 1, "Anzahl %d" % text.count(eingebaut))
            with open(pfad, "w", encoding="utf-8") as f:
                f.write(text.replace(eingebaut, ohne))
            rc, ausgabe = probe(wurzel, bot, datei, "ohne", probedatei)
            pruefe(f"{name}: Probe A wird rot (kein Abbruch durch die Wache)",
                   rc != 3, f"rc {rc}: {ausgabe}")
            # Die uebrigen Stellen derselben Kopie bleiben gruen - die
            # Mutation beisst allein.
            for b, d in STELLEN:
                if b == bot and d != datei:
                    rc2, ausgabe2 = probe(wurzel, bot, d, "ohne", probedatei)
                    pruefe(f"{name}: {d} in derselben Kopie weiter gruen",
                           rc2 == 3, f"rc {rc2}: {ausgabe2}")
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)

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
