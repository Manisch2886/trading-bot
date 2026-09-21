"""TB-80 Schritt 0, Zusatz: das frueheste Warm-Datum je Bot unter dem heutigen
Anker (fn.fensteranker, Datenuhr) - die Groesse HINTER erste_falte_4a, auf
Tagesebene. Sie wird gemessen, damit die Mutationsprobe in Schritt 3 unterhalb
der Jahresebene vergleichen kann: ein Jahr, das sich nicht bewegt, sagt nichts
darueber, ob der Anker gewechselt hat.

    trading-env/bin/python3 docs/belege/TB-80/schritt0_warm_ab.py
"""
import os, sys
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(BASE, "research", "vorregistrierung"))
import faltenplan as vfp
fn = vfp.fn

print(f"{'Bot':28s} {'Anker':11s} {'warm ab (fruehestes)':21s} Symbol(e)  -> 4a-Jahr")
for bot, eig in fn.BOTS.items():
    anker = fn.fensteranker(eig["markt"])
    beginn = fn.symbolbeginn(bot, anker)
    warme = {s: w for s, (_, w) in beginn.items() if w is not None}
    fruehestes = min(warme.values())
    symbole = sorted(s for s, w in warme.items() if w == fruehestes)
    jahr = fn._ungebremstes_faltenjahr(beginn)
    print(f"{bot:28s} {str(anker):11s} {fruehestes.isoformat():21s} "
          f"{','.join(symbole[:4])}{'...' if len(symbole) > 4 else ''} ({len(symbole)}) -> {jahr}")
