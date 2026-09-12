"""
Ist ein EINZELNES Symbol schon chronologisch?
====================================================================
Aufruf:  python3 einzelsymbol.py <bot>

Die Frage gehoert zu Frage 1 des Auftrags: das Projekt hat neben
`multi_symbol_optimise.py` auch Einzelsymbol-Optimierer
(`optimise_elliott.py`, `optimise_trend.py`), die denselben Score mit
demselben `cumsum`-Drawdown rechnen. Betrifft der Befund die auch?

Gemessen wird das Naheliegende: ob die Trade-Liste EINES Symbols, so
wie die Bot-Funktion sie liefert, bereits nach `entry_time` steigt.
Wenn ja, ist die Reihenfolge dort keine Willkuer, sondern die Zeit -
und die Einzelsymbol-Optimierer sind vom Befund nicht betroffen.

Geprueft wird auf der Live-Kombination des Bots bzw., wenn die nicht im
Raster liegt, auf der ersten Rasterkombination.
"""

import sys

import botenv
from test_drawdown import LIVE


def main():
    botenv.print_hinweis()
    bot = botenv.bot_from_argv()

    import multi_symbol_optimise as mo
    import adapters

    ad = adapters.build(bot, mo)
    data = mo.load_all_symbol_data()
    combos = ad.combinations()
    combo = LIVE[bot] if LIVE.get(bot) in combos else combos[0]

    trades, n_sym = ad.collect(data, combo)
    print(f"\n=== {bot}: {ad.label(combo)} ===")

    gesamt, monoton, verletzungen = 0, 0, []
    for blk, g in trades.groupby("_block_idx", sort=True):
        gesamt += 1
        symbol = g["symbol"].iloc[0]
        if g["entry_time"].is_monotonic_increasing:
            monoton += 1
        else:
            verletzungen.append(symbol)

    print(f"Symbole: {gesamt}")
    print(f"davon entry_time bereits monoton steigend: {monoton}")
    if verletzungen:
        print(f"NICHT monoton: {', '.join(verletzungen[:15])}")
    print()
    if monoton == gesamt:
        print("-> Innerhalb eines Symbols ist die Zeilenreihenfolge die ZEIT.")
        print("   Der Reihenfolge-Befund betrifft deshalb nur die Multi-Symbol-")
        print("   Auswertung, nicht die Einzelsymbol-Optimierer.")
    else:
        print("-> Schon innerhalb eines Symbols steht die Reihenfolge nicht")
        print("   chronologisch. Dann waeren auch die Einzelsymbol-Optimierer")
        print("   betroffen.")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()
