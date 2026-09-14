#!/usr/bin/env python3
"""
Selbsttest der Regimewache (TB-30a, Befund AB2/U5)
==============================================================================
Geprueft wird das VERHALTEN der Wache und - wichtiger - dass sie den Befund
ueberhaupt noch beschreibt. Ein Test, der nur die Wache selbst prueft, wuerde
gruen bleiben, wenn der eigentliche Fehler in `t3_supertrend` still
verschwaende oder sich verschoebe.

Teil A  Die Wache bricht ab, statt zu ueberspringen.
Teil B  Ein ABGESCHALTETER Filter ist etwas anderes als ein FEHLENDER.
Teil C  Der Befund ist noch da: `t3_supertrend` ueberspringt den Filter
        heute stillschweigend, `volatility_breakout_crypto` bricht ab. Faellt
        diese Pruefung, ist der Einbau erfolgt (TB-30b) - dann gehoert sie
        umgestellt, nicht geloescht.
Teil D  Der Einbaupruefer meldet den Stand ehrlich.
"""

import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_HIER)
sys.path.insert(0, _HIER)

import regimewache as rw

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


class _LeererRahmen:
    empty = True


def teil_a():
    try:
        rw.btc_daten({}, "t3_supertrend", "python3 fetch_4h_data.py")
        ok, text = False, ""
    except SystemExit as e:
        ok, text = True, str(e)
    pruefe("A1: fehlendes BTCUSDT bricht ab", ok)
    pruefe("A2: die Meldung nennt den Bot", "t3_supertrend" in text, text[:60])
    pruefe("A3: die Meldung nennt den Weg zu den Daten",
           "fetch_4h_data.py" in text, text[:60])
    pruefe("A4: die Meldung sagt, WARUM nicht weitergerechnet wird",
           "andere Strategie" in text, text[:80])

    try:
        rw.btc_daten({"BTCUSDT": _LeererRahmen()}, "t3_supertrend", "x")
        ok = False
    except SystemExit:
        ok = True
    pruefe("A5: ein leerer BTC-Rahmen bricht ebenfalls ab", ok)

    class _Voll:
        empty = False
    daten = {"BTCUSDT": _Voll()}
    pruefe("A6: vorhandene Daten kommen unveraendert zurueck",
           rw.btc_daten(daten, "t3_supertrend", "x") is daten["BTCUSDT"])


def teil_b():
    pruefe("B1: abgeschalteter Filter liefert None statt Abbruch",
           rw.btc_daten({}, "x", "y", aktiv=False) is None)
    pruefe("B2: abgeschaltet UND vorhanden liefert ebenfalls None",
           rw.btc_daten({"BTCUSDT": object()}, "x", "y", aktiv=False) is None)
    pruefe("B3: die Fehlerklasse endet mit Rueckgabewert != 0",
           issubclass(rw.RegimefilterFehlt, SystemExit))


def _quelltext(rel):
    with open(os.path.join(BASE_DIR, rel), encoding="utf-8") as f:
        return f.read()


def teil_c():
    """Der Befund selbst - am Quelltext der Bots, nicht an der Wache.

    Diese Pruefungen sind bewusst so geschrieben, dass sie ROT werden, sobald
    TB-30b die Wache eingebaut hat. Das ist kein Fehlalarm, sondern die
    Uebergabe: dann ist der Befund erledigt und die Zusicherung lautet
    umgekehrt.
    """
    t3_sim = _quelltext("strategies/t3_supertrend/equity_simulation.py")
    t3_opt = _quelltext("strategies/t3_supertrend/multi_symbol_optimise.py")
    vbc = _quelltext("strategies/volatility_breakout_crypto/equity_simulation.py")

    eingebaut = rw.pruefe_einbau(BASE_DIR)["vollstaendig"]
    if eingebaut:
        pruefe("C1: TB-30b hat die Wache eingebaut - der Befund ist erledigt",
               all("btc_daten(" in t for t in (t3_sim, t3_opt, vbc)))
        return

    pruefe("C1: t3_supertrend/equity_simulation.py prueft weiterhin nur "
           "'if \"BTCUSDT\" in all_data' ohne Gegenzweig",
           'if "BTCUSDT" in all_data:' in t3_sim and "btc_daten(" not in t3_sim)
    pruefe("C2: t3_supertrend/multi_symbol_optimise.py ebenso",
           'if "BTCUSDT" in all_data:' in t3_opt and "btc_daten(" not in t3_opt)
    pruefe("C3: volatility_breakout_crypto bricht heute schon ab - die "
           "Entscheidung 'abbrechen' ist also keine Neuerfindung",
           "raise SystemExit(" in vbc and "BTCUSDT" in vbc)
    pruefe("C4: der Regimefilter des T3-Bots ist eingeschaltet - der "
           "Unterschied ist also nicht hypothetisch",
           "compute_btc_regime" in t3_sim)


def teil_d():
    stand = rw.pruefe_einbau(BASE_DIR)
    pruefe("D1: der Einbaupruefer nennt alle drei Stellen",
           len(stand["offen"]) + len(stand["eingebaut"]) == len(rw.EINBAUSTELLEN),
           str(stand))
    pruefe("D2: 'vollstaendig' ist genau dann wahr, wenn nichts offen ist",
           stand["vollstaendig"] == (not stand["offen"]))
    pruefe("D3: der Pruefer laeuft auch auf einem Verzeichnis ohne die Dateien",
           rw.pruefe_einbau("/nicht/vorhanden")["vollstaendig"] is False)


def main():
    print(__doc__.strip().split("\n")[0])
    for t in (teil_a, teil_b, teil_c, teil_d):
        t()
    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    stand = rw.pruefe_einbau(BASE_DIR)
    print(f"\nEinbaustand: {len(stand['eingebaut'])} von "
          f"{len(rw.EINBAUSTELLEN)} Stellen - offen: {stand['offen'] or 'keine'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
