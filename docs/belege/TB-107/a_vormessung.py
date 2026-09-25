"""TB-107 A1-A7 - Vormessung, nur lesend, am Code-Stand f22f91e. Aufruf aus der Repo-Wurzel:
    trading-env/bin/python3 -W ignore docs/belege/TB-107/a_vormessung.py
"""
import ast, os, re, sys
sys.path.insert(0, "research/faltenplan_neun")
import faltenplan_neun as fn
import faltenschranke_messung as fsm

MUSTER = r"^(MIN_HISTORY_(?:DAYS|HOURS))\s*=\s*(\d+)"
print("== A1 _min_history: Treffer je Bot-Datei (re.findall, gleiches Muster, re.M)")
for bot in fn.BOTS:
    pfad = os.path.join(fsm.BASE_DIR, "strategies", bot, "multi_symbol_optimise.py")
    t = re.findall(MUSTER, open(pfad, encoding="utf-8").read(), re.M)
    print("   %-28s %d Treffer %s | _min_history() = %s" % (bot, len(t), [n for n, _ in t], fsm._min_history(bot)[0]))
print("== A2 Name der Schranke in strategies/elliott_wave/multi_symbol_optimise.py:", fsm._min_history("elliott_wave")[0])
print("== A3 loader_lesart: n = None nur wenn _min_history (None, None) liefert; heute bei keinem Bot (A1)")
print("== A4 faltenplan_neun.volle_jahre()/faltenlaenge() mit der echten Eingabe (basis=None -> BASE_DIR %s)" % fn.BASE_DIR)
for bot in fn.BOTS:
    z = fn.gefundene_trades_je_jahr(bot)
    jahre = sorted(z)
    innen = [j for j in jahre[1:-1]]
    print("   %-28s Jahre %d, innere Jahre %d -> Ersatz 'erstes Jahr' erreicht: %s; leere Zaehlung: %s"
          % (bot, len(jahre), len(innen), "ja" if not innen else "nein", "ja" if not z else "nein"))
print("   Aufrufer von faltenlaenge(): nur plan_fuer_bot() (faltenplan_neun.py), basis aus faltenplan(basis=...)")
src = open("research/faltenplan_neun/faltenplan_neun.py", encoding="utf-8").read()
for m in re.finditer(r"^.*\b(faltenlaenge|volle_jahre|plan_fuer_bot|faltenplan)\((.*)$", src, re.M):
    zeile = src[:m.start()].count("\n") + 1
    print("   faltenplan_neun.py:%d %s" % (zeile, m.group(0).strip()[:110]))
print("== A5 strategy_paths._im_selektionsmodus")
sp = open("shared/strategy_paths.py", encoding="utf-8").read()
for i, z in enumerate(sp.splitlines(), 1):
    if "getattr(" in z or "_im_selektionsmodus" in z:
        print("   strategy_paths.py:%d %s" % (i, z.strip()))
print("== A6 universum_trockenlauf.py: mkdtemp-Stellen")
ut = open("research/universum_trockenlauf/universum_trockenlauf.py", encoding="utf-8").read()
for i, z in enumerate(ut.splitlines(), 1):
    if "mkdtemp" in z or "rmtree" in z:
        print("   universum_trockenlauf.py:%d %s" % (i, z.strip()))
