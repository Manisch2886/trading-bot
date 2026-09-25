"""TB-109 A3/B3 - die Trade-Listen der neun `__main__`-Bloecke von equity_simulation.py im Speicher.

Bauart TB-105 b3_trades.py, aber fuer alle neun Bots und ueber den `__main__`-Block selbst: das Modul wird
importiert (Stubs wie shared/kurven_lauf.py, Arbeitsordner wie dort der Strategieordner), danach werden die
Anweisungen des `__main__`-Blocks EINZELN im Modul-Namensraum ausgefuehrt - bis VOR die erste Anweisung, die
`simulate_portfolio(` aufruft (dort beginnt die Rechnung, die schreibt). Vor jeder Anweisung
`if trades.empty: ...` wird festgehalten, ob die Liste leer ist; endet eine Anweisung mit SystemExit, steht
die Zeile im Ergebnis.

Sichtschutz 27.1: keine Trade-Zahl, keine Kennzahl - je Stelle nur "leer ja/nein" und der sha256 der Liste.
Schreibt nichts ausser auf stdout.

Aufruf aus der Repo-Wurzel, OHNE Modus, je Bot ein Prozess:
  trading-env/bin/python3 -W ignore docs/belege/TB-109/a3_b3_trades.py <bot>
"""
import ast, contextlib, hashlib, io, json, os, sys

bot = sys.argv[1]
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sdir = os.path.join(_REPO, "strategies", bot)
skript = os.path.join(sdir, "equity_simulation.py")
sys.path.insert(0, sdir)
sys.path.insert(0, os.path.join(_REPO, "shared"))
import kurven_lauf  # noqa: E402  (nur fuer die Stubs; der Import schreibt nichts)
kurven_lauf._stubs_setzen()
os.chdir(sdir)


def h(df):
    text = df.to_json(orient="records", date_format="iso", double_precision=15)
    return hashlib.sha256(json.dumps(json.loads(text), sort_keys=True, default=str).encode("utf-8")).hexdigest()


with contextlib.redirect_stdout(io.StringIO()):
    import equity_simulation as es
ns = es.__dict__

baum = ast.parse(open(skript, encoding="utf-8").read())
haupt = [k for k in baum.body if isinstance(k, ast.If) and "__main__" in ast.dump(k.test)]
assert len(haupt) == 1, "kein eindeutiger __main__-Block"


def ruft_simulate(knoten):
    return any(isinstance(n, ast.Call) and getattr(n.func, "id", None) == "simulate_portfolio"
               for n in ast.walk(knoten))


def ist_leer_pruefung(knoten):
    return isinstance(knoten, ast.If) and ast.unparse(knoten.test) == "trades.empty"


print("# %s (%s)" % (bot, os.path.relpath(skript, _REPO)))
for anw in haupt[0].body:
    if ruft_simulate(anw):
        print("  Z.%-4d simulate_portfolio erreicht - Ende der Messung (keine der Stellen hat beendet)" % anw.lineno)
        break
    if ist_leer_pruefung(anw):
        t = ns["trades"]
        print("  Z.%-4d if trades.empty: leer %s, sha256 %s" % (anw.lineno, "ja" if t.empty else "nein", h(t)))
    code = compile(ast.Module(body=[anw], type_ignores=[]), skript, "exec")
    puffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(puffer):
            exec(code, ns)
    except SystemExit as e:
        print("  Z.%-4d SystemExit(%r) - der Lauf endet HIER" % (anw.lineno, e.code))
        break
