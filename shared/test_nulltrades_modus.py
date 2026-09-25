#!/usr/bin/env python3
"""
Selbsttest zu TB-109 Block B: null Trades unter dem Modus - Rueckgabe 2
==============================================================================
Fable 25e (2): "Ein Lauf des Laufbereichs, der keine Trades findet oder
ausfuehrt, schreibt dieses Ergebnis ... und endet mit 0; er endet nie ohne
Ausgabe. Unter dem Modus endet ein `exit()` ohne geschriebenes Ergebnis mit 2,
gleich was ihm vorausgeht."

Die 10 Stellen `if trades.empty: ... exit()` in den neun
`strategies/*/equity_simulation.py` (Liste TB-107 f_gegenprobe.txt) tragen
seitdem die Modus-Abfrage, Bauart TB-105 Block C (Abfrage an der Stelle, ueber
`paths`, kein Name aus `strategy_paths`).

  N1  je Stelle: leere Trade-Liste unter dem Modus => rc 2, Meldung auf
      stderr, nicht auf stdout.
  N2  je Stelle: dieselbe leere Liste ohne Modus => rc 0, Meldung auf stdout
      wie bisher.
  N3  Mutationsprobe fuer die Bauart (an einer Stelle faellt die Abfrage weg)
      => N1 waere rot; Gegenprobe am unveraenderten Baum.

Wie die Liste leer wird: In der Kopie im Wegwerfbaum (nicht im Repo) wird nur
der ERZEUGER ersetzt, die Stelle selbst bleibt zeichengleich -
`all_data = load_all_symbol_data()` liefert ein nicht leeres Attrappen-dict,
`trades = collect_all_trades(` wird zu `trades = <leer> if True else
collect_all_trades(` (die Argumentliste bleibt syntaktisch stehen). Fuer die
zweite Stelle in volatility_breakout_crypto (nach dem BTC-Regimefilter)
liefert der Erzeuger eine nicht leere Liste, und der Filter gibt sie leer
zurueck.

Wegwerfbaum und Snapshot-Attrappe wie `shared/test_rueckfaelle_modus.py`
(Funktionen von dort importiert, nicht kopiert); jede Probe ein eigener
Prozess.

Aufruf:  python3 shared/test_nulltrades_modus.py
"""

import os
import shutil
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)
import test_rueckfaelle_modus as trm  # noqa: E402  (nur die Baumfunktionen)

LADEN = "all_data = load_all_symbol_data()"
LADEN_ATTRAPPE = 'all_data = {"ATTRAPPE": None}'
ERZEUGER = "    trades = collect_all_trades("
FILTER = "    trades = apply_btc_regime_filter(trades, all_data)"

# (Datei, Meldung, Stelle): "erzeuger" = die Liste ist schon nach
# collect_all_trades leer; "filter" = erst nach dem BTC-Regimefilter.
STELLEN = [
    ("strategies/%s/equity_simulation.py" % bot, "Keine Trades fuer diese Parameter-Kombination gefunden.", "erzeuger")
    for bot in ("elliott_wave", "elliott_wave_stocks", "rsi2_crypto", "rsi2_mean_reversion",
                "t3_supertrend", "turtle_soup_crypto", "turtle_soup_stocks", "volatility_breakout",
                "volatility_breakout_crypto")
] + [("strategies/volatility_breakout_crypto/equity_simulation.py",
      "Nach dem BTC-Regimefilter bleibt kein Trade uebrig.", "filter")]

# Die Mutation (eine Stelle, nicht zehn): die Abfrage vor der Meldung faellt weg.
MUT_ALT = ('        if paths.selektionsmodus() is not None:\n'
           '            sys.stderr.write("Keine Trades fuer diese Parameter-Kombination gefunden."')
MUT_NEU = ('        if False:\n'
           '            sys.stderr.write("Keine Trades fuer diese Parameter-Kombination gefunden."')

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


def harness(text, art):
    """Nur den Erzeuger der Kopie ersetzen. Gibt (neuer Text, griff?) zurueck."""
    griff = text.count(LADEN) == 1 and text.count(ERZEUGER) == 1
    text = text.replace(LADEN, LADEN_ATTRAPPE, 1)
    if art == "erzeuger":
        text = text.replace(ERZEUGER, "    trades = pd.DataFrame() if True else collect_all_trades(", 1)
    else:
        griff = griff and text.count(FILTER) == 1
        text = text.replace(ERZEUGER,
                            '    trades = pd.DataFrame({"attrappe": [1]}) if True else collect_all_trades(', 1)
        text = text.replace(FILTER, "    trades = trades.iloc[0:0]", 1)
    return text, griff


def baum_mit(arbeit, name, rel, art, mutation=False):
    """Wegwerfbaum (trm.baue_baum), darin die eine Datei vorbereitet, neu committet."""
    w, _ = trm.baue_baum(arbeit, name)
    pfad = os.path.join(w, rel)
    text = open(pfad, encoding="utf-8").read()
    text, griff = harness(text, art)
    if mutation:
        griff = griff and text.count(MUT_ALT) == 1
        text = text.replace(MUT_ALT, MUT_NEU, 1)
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(text)
    trm._git(w, "-c", "user.name=tb109_test", "-c", "user.email=tb109@test",
             "commit", "-q", "-a", "--amend", "-m", "Wegwerfbaum TB-109")
    return w, griff


def main():
    print(__doc__.strip().split("\n")[0])
    arbeit = tempfile.mkdtemp(prefix="tb109_nulltrades_")
    try:
        attrappe = trm.baue_attrappe(arbeit, "snap", trm.echtes_universum())
        pruefe("N0 zehn Stellen", len(STELLEN) == 10, str(len(STELLEN)))
        for i, (rel, meldung, art) in enumerate(STELLEN):
            w, griff = baum_mit(arbeit, "n%d" % i, rel, art)
            pruefe("N0 %s (%s): Erzeuger in der Kopie ersetzt" % (rel, art), griff)
            rc, out, err = trm.lauf(w, [os.path.join(w, rel)], attrappe)
            pruefe("N1 %s (%s): Modus, leere Trade-Liste => rc 2, Meldung auf stderr" % (rel, art),
                   rc == 2 and meldung in err and meldung not in out,
                   "rc %d, stdout %r, stderr %r" % (rc, out.strip()[-160:], err.strip()[-200:]))
            rc, out, err = trm.lauf(w, [os.path.join(w, rel)])
            pruefe("N2 %s (%s): ohne Modus => rc 0, Meldung auf stdout wie bisher" % (rel, art),
                   rc == 0 and meldung in out and meldung not in err,
                   "rc %d, stdout %r, stderr %r" % (rc, out.strip()[-160:], err.strip()[-200:]))
            shutil.rmtree(w, ignore_errors=True)

        rel, meldung, art = STELLEN[0]
        w, griff = baum_mit(arbeit, "n_mut", rel, art, mutation=True)
        pruefe("N3 Mutation 'Modus-Abfrage weg' griff", griff)
        rc, out, err = trm.lauf(w, [os.path.join(w, rel)], attrappe)
        pruefe("N3 Mutation => Probe N1 rot (rc 0 statt 2)", rc != 2, "rc %d" % rc)
        w, _ = baum_mit(arbeit, "n_gegen", rel, art)
        rc, out, err = trm.lauf(w, [os.path.join(w, rel)], attrappe)
        pruefe("N3 Gegenprobe: unveraenderter Baum => rc 2", rc == 2, "rc %d" % rc)
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
