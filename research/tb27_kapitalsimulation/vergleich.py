#!/usr/bin/env python3
"""TB-27 - Vergleich der neun `equity_simulation.py`, Funktion fuer Funktion.

Warum nicht `diff`
------------------
Ein Textvergleich ueber ganze Dateien geht bei diesen neun Dateien sofort
unter: ihre `collect_all_trades()` haben verschiedene Signaturen, ihre
Kopfkommentare sind je Bot verschieden lang, und die Reihenfolge der Importe
weicht ab. `diff` meldet dann alles und damit nichts.

Dieses Werkzeug vergleicht deshalb **je Funktion** und auf **drei Stufen**:

  1. `zeichengleich`   - dieselben Zeichen, Kommentare und Umbrueche inbegriffen
  2. `ohne Kommentar`  - gleich, nachdem Kommentare, Zeilenumbrueche und
                         Einrueckung entfernt sind. Docstrings zaehlen auf
                         dieser Stufe noch mit; sie fallen erst auf Stufe 3
                         weg. So laesst sich unterscheiden, ob nur ein
                         Kommentar oder auch die Beschreibung abweicht.
  3. `sachlich gleich` - gleicher abstrakter Syntaxbaum ohne Docstrings
                         (AST). Das ist die aussagekraeftigste Stufe: nur was
                         hier abweicht, kann das Ergebnis veraendern.
  4. `ohne Ausgabe`    - wie 3, zusaetzlich sind die Argumente jedes
                         `print(...)` durch einen Platzhalter ersetzt. Diese
                         Stufe beantwortet die Frage, ob zwei Faelle
                         verschieden RECHNEN oder bloss verschieden REDEN.
                         Sie steht bewusst neben Stufe 3, nicht an ihrer
                         Stelle: was auf dem Bildschirm steht, ist bei diesen
                         Dateien selbst schon einmal falsch gewesen (der
                         Klammerzusatz zu den uebersprungenen Trades, PR #48).

Vorbild ist TB-17, das per AST belegt hat, dass an einer Stelle nur ein
Docstring geaendert wurde.

Was das Werkzeug NICHT kann
---------------------------
Es liest Quelltext, es fuehrt nichts aus. Zwei sachlich gleiche Funktionen
koennen sich trotzdem verschieden verhalten, wenn die von ihnen gerufenen
Namen in den Bots Verschiedenes bedeuten - `get_trades_for_symbol()` etwa ist
in jedem Bot eine andere Funktion. Der AST-Vergleich beweist also
Gleichheit des Codes, nicht Gleichheit des Verhaltens. Umgekehrt gilt der
Befund streng: was hier als verschieden gemeldet wird, IST verschieden.

Aufrufe
-------
    python3 research/tb27_kapitalsimulation/vergleich.py
        Uebersicht: welche Funktion kommt wo vor, und welche Bots teilen sich
        denselben Rumpf.

    python3 research/tb27_kapitalsimulation/vergleich.py --pruefen
        Waechter-Betrieb. Vergleicht die heutige Gruppierung mit der in
        ERWARTUNG festgehaltenen (Stand TB-27, 13.09.2026) und meldet jede
        Abweichung. Rueckgabewert 1, sobald eine Funktion, die heute in allen
        neun Bots gleich ist, in einem Bot auseinanderlaeuft - oder eine
        bekannte Abweichung verschwindet, ohne dass ERWARTUNG nachgezogen
        wurde. Fuer den Cronjob oder einen Pruefdurchlauf vor dem Merge.

    python3 research/tb27_kapitalsimulation/vergleich.py --zeige FUNKTION
        Den Quelltext dieser Funktion aus allen Bots nebeneinander, gruppiert
        nach sachlicher Gleichheit.

    python3 research/tb27_kapitalsimulation/vergleich.py --datei DATEI
        Dasselbe fuer eine andere Datei, die es je Bot gibt - etwa
        `multi_symbol_optimise.py`, wo die Zielfunktion der Parametersuche
        steht. `--pruefen` gibt es nur fuer `equity_simulation.py`; nur dafuer
        ist unten eine Erwartung festgehalten.

Das Werkzeug importiert keinen Bot-Code (kein pandas noetig) und schreibt
nichts. Es liest ausschliesslich `strategies/*/equity_simulation.py`.
"""

import argparse
import ast
import hashlib
import io
import os
import sys
import tokenize
from typing import NamedTuple

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))

# Normalerweise die neun echten Bots. `TB27_STRATEGIEN` zeigt auf einen
# anderen Ordner - das braucht der Selbsttest, um dem Waechter eine
# absichtlich verfaelschte Kopie vorzulegen und nachzuweisen, dass er
# darauf ROT meldet. Eine gruene Pruefung, die nie rot werden kann, ist
# keine Pruefung (Methodik-Prinzip 12).
_STRATEGIEN = os.environ.get("TB27_STRATEGIEN") or os.path.join(_WURZEL, "strategies")

DATEINAME = "equity_simulation.py"

# Der `if __name__ == "__main__"`-Block wird wie eine Funktion behandelt und
# unter diesem Namen gefuehrt - er ist bei diesen Dateien der Ort, an dem aus
# der Trade-Liste eine Zahl wird, und gehoert deshalb in den Vergleich.
HAUPTBLOCK = "__main__"


# ---------------------------------------------------------------------------
# Erwartungswerte, Stand TB-27 (13.09.2026)
# ---------------------------------------------------------------------------
# Je Funktionsname: die Gruppen sachlich gleicher Faelle, jede Gruppe als
# sortiertes Tupel von Bot-Namen. Eine Funktion, die nur in einem Teil der
# Bots vorkommt, taucht auch nur mit diesen auf.
#
# Diese Tabelle ist eine BESTANDSAUFNAHME, keine Zielvorgabe: sie schreibt
# fest, wie es am 13.09.2026 war, damit eine spaetere, unbeabsichtigte
# Abweichung auffaellt. Wer eine Abweichung bewusst herbeifuehrt, zieht die
# Tabelle mit nach und begruendet es im zugehoerigen Pull Request.
#
# NACHGEZOGEN IN TB-28 (13.09.2026): `calculate_max_drawdown` stand hier als
# EINE Gruppe ueber alle neun Bots - zeichengleich, und genau deshalb ein
# Kandidat fuer die Zusammenlegung. Die Funktion ist seit TB-28 nicht mehr
# Teil dieser neun Dateien: sie steht einmal in `shared/messkette.py` und
# wird dort importiert. Der Eintrag entfaellt deshalb - nicht, weil eine
# Divergenz hingenommen wird, sondern weil es die Fassungen nicht mehr gibt,
# zwischen denen eine entstehen koennte.
#
# Der Waechter hat diese Aenderung gemeldet, wie er soll ("FUNKTION FEHLT:
# calculate_max_drawdown"). Die Renditeformel steht nicht in dieser Tabelle,
# weil sie keine Funktion ist, sondern eine Zeile im `__main__`-Block; ihre
# Gruppierung dort bleibt unveraendert (acht Gruppen, wie in TB-27).
ERWARTUNG = {
    "simulate_portfolio": [
        # Acht Bots teilen sich denselben Rumpf.
        ("elliott_wave_stocks", "rsi2_crypto", "rsi2_mean_reversion",
         "t3_supertrend", "turtle_soup_crypto", "turtle_soup_stocks",
         "volatility_breakout", "volatility_breakout_crypto"),
        # `elliott_wave` kennt bewusst kein Positionslimit-Argument und
        # reicht deshalb `None` durch (TB-26). Mehrere Werkzeuge erkennen
        # genau daran, welcher Bot kein Limit hat.
        ("elliott_wave",),
    ],
    "collect_all_trades": [
        ("elliott_wave",), ("elliott_wave_stocks",), ("rsi2_crypto",),
        ("rsi2_mean_reversion",), ("t3_supertrend",),
        ("turtle_soup_crypto",), ("turtle_soup_stocks",),
        ("volatility_breakout",), ("volatility_breakout_crypto",),
    ],
    "apply_btc_regime_filter": [
        ("volatility_breakout_crypto",),
    ],
    HAUPTBLOCK: [
        # Die beiden Turtle-Soup-Bots rufen `collect_all_trades` mit
        # denselben Namen auf und sind deshalb zeichengleich. Alle uebrigen
        # unterscheiden sich - nach Abzug der Bildschirmausgabe aber nur an
        # drei Stellen, und alle drei sind bot-eigen noetig (siehe
        # BERICHT.md, Abschnitt 2.4): die Argumentliste von
        # `collect_all_trades`, das fehlende Positionslimit bei
        # `elliott_wave` und der Regimefilter-Schritt bei
        # `volatility_breakout_crypto` (PR #57).
        ("turtle_soup_crypto", "turtle_soup_stocks"),
        ("elliott_wave",), ("elliott_wave_stocks",), ("rsi2_crypto",),
        ("rsi2_mean_reversion",), ("t3_supertrend",),
        ("volatility_breakout",), ("volatility_breakout_crypto",),
    ],
}

# Modulweite Zuweisungen, die verglichen werden. Alles andere auf Modulebene
# (Pfadaufbau, Importe) ist bei allen neun gleich oder bot-spezifisch noetig
# und steht im Bericht, nicht hier.
KONSTANTEN = ("STARTING_CAPITAL", "ALLOCATION_PCT", "SIGNALSPALTE", "RESULTS_DIR")


# ---------------------------------------------------------------------------
# Einlesen und Normalisieren
# ---------------------------------------------------------------------------

def bots(dateiname=DATEINAME):
    """Die Bot-Ordner, die eine Datei dieses Namens haben (neun beim Standard)."""
    gefunden = []
    for name in sorted(os.listdir(_STRATEGIEN)):
        if os.path.isfile(os.path.join(_STRATEGIEN, name, dateiname)):
            gefunden.append(name)
    return gefunden


def _quelle(bot, dateiname=DATEINAME):
    with open(os.path.join(_STRATEGIEN, bot, dateiname), encoding="utf-8") as f:
        return f.read()


def _ohne_docstring(knoten):
    """Kopie des Knotens ohne fuehrenden Docstring.

    Der Docstring steht im AST als gewoehnlicher Ausdruck und wuerde einen
    reinen Kommentarunterschied als sachlichen melden. Genau das soll die
    Stufe `sachlich gleich` nicht tun.
    """
    kopie = ast.parse(ast.unparse(knoten))
    for teil in ast.walk(kopie):
        koerper = getattr(teil, "body", None)
        if not isinstance(koerper, list) or not koerper:
            continue
        erster = koerper[0]
        if (isinstance(erster, ast.Expr) and isinstance(erster.value, ast.Constant)
                and isinstance(erster.value.value, str)):
            koerper.pop(0)
            if not koerper:
                koerper.append(ast.Pass())
    return kopie


class _AusgabeLeeren(ast.NodeTransformer):
    """Ersetzt die Argumente jedes `print(...)` durch einen Platzhalter."""

    def visit_Call(self, knoten):  # noqa: N802 - von ast vorgegeben
        self.generic_visit(knoten)
        if isinstance(knoten.func, ast.Name) and knoten.func.id == "print":
            knoten.args = [ast.Constant(value="<ausgabe>")]
            knoten.keywords = []
        return knoten


def _ast_kennung(knoten, ohne_ausgabe=False):
    baum = _ohne_docstring(knoten)
    if ohne_ausgabe:
        baum = ast.fix_missing_locations(_AusgabeLeeren().visit(baum))
    return hashlib.sha256(
        ast.dump(baum, include_attributes=False).encode()
    ).hexdigest()[:16]


def _tokenkennung(text):
    """Kennung des Tokenstroms ohne Kommentare, Docstrings und Leerraum."""
    stuecke = []
    letzter_war_string_allein = False
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE,
                            tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER):
                continue
            stuecke.append(f"{tok.type}:{tok.string}")
    except (tokenize.TokenError, IndentationError):
        # Ein Funktionsrumpf allein ist nicht immer fuer sich tokenisierbar;
        # dann faellt diese Stufe aus und nur AST und Text zaehlen.
        return None
    del letzter_war_string_allein
    return hashlib.sha256("|".join(stuecke).encode()).hexdigest()[:16]


class Stueck(NamedTuple):
    """Ein vergleichbares Stueck Quelltext auf den vier Stufen."""

    text: str                  # Stufe 1
    token: str                 # Stufe 2 (None, wenn nicht tokenisierbar)
    baum: str                  # Stufe 3
    baum_ohne_ausgabe: str     # Stufe 4


class Datei:
    """Eine `equity_simulation.py`, zerlegt in vergleichbare Stuecke."""

    def __init__(self, bot, dateiname=DATEINAME):
        self.bot = bot
        self.dateiname = dateiname
        self.text = _quelle(bot, dateiname)
        self.baum = ast.parse(self.text)
        self.stuecke = {}      # Name -> (ast-Kennung, token-Kennung, Quelltext)
        self.konstanten = {}   # Name -> Quelltext der Zuweisung
        self.importe = []      # (modul, [namen])
        self._zerlegen()

    def _merken(self, name, knoten):
        quelle = ast.get_source_segment(self.text, knoten) or ""
        self.stuecke[name] = Stueck(
            text=quelle,
            token=_tokenkennung(ast.unparse(knoten)),
            baum=_ast_kennung(knoten),
            baum_ohne_ausgabe=_ast_kennung(knoten, ohne_ausgabe=True),
        )

    def _zerlegen(self):
        for knoten in self.baum.body:
            if isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._merken(knoten.name, knoten)
            elif isinstance(knoten, ast.ClassDef):
                self._merken("class " + knoten.name, knoten)
            elif isinstance(knoten, ast.If) and _ist_hauptblock(knoten):
                self._merken(HAUPTBLOCK, knoten)
            elif isinstance(knoten, ast.Assign):
                for ziel in knoten.targets:
                    if isinstance(ziel, ast.Name):
                        self.konstanten[ziel.id] = ast.unparse(knoten)
            elif isinstance(knoten, (ast.Import, ast.ImportFrom)):
                modul = getattr(knoten, "module", None) or ""
                self.importe.append((modul, [a.name for a in knoten.names]))

    def signatur(self, name):
        for knoten in self.baum.body:
            if isinstance(knoten, ast.FunctionDef) and knoten.name == name:
                return f"{name}({ast.unparse(knoten.args)})"
        return None


def _ist_hauptblock(knoten):
    pruef = knoten.test
    return (isinstance(pruef, ast.Compare)
            and isinstance(pruef.left, ast.Name) and pruef.left.id == "__name__")


# ---------------------------------------------------------------------------
# Vergleich
# ---------------------------------------------------------------------------

def gruppen(dateien, name, stufe="baum"):
    """Bots, gruppiert nach Gleichheit dieser Funktion auf der genannten Stufe.

    `stufe` ist `baum` (sachlich, die Voreinstellung) oder `baum_ohne_ausgabe`.

    Rueckgabe: Liste von (Bot-Tupel, Guete). `Guete` ist die staerkste
    Gleichheit, die innerhalb der Gruppe noch gilt: `zeichengleich`,
    `ohne Kommentar` oder der Name der Gruppierungsstufe. Eine Gruppe mit nur
    einem Bot bekommt `einzeln` - dort ist Gleichheit trivial und die Angabe
    waere irrefuehrend.
    """
    nach_kennung = {}
    for datei in dateien:
        if name not in datei.stuecke:
            continue
        stueck = datei.stuecke[name]
        nach_kennung.setdefault(getattr(stueck, stufe), []).append((datei.bot, stueck))

    ergebnis = []
    for eintraege in nach_kennung.values():
        namen = tuple(sorted(e[0] for e in eintraege))
        stuecke = [e[1] for e in eintraege]
        if len(namen) == 1:
            guete = "einzeln"
        elif len({s.text for s in stuecke}) == 1:
            guete = "zeichengleich"
        elif len({s.token for s in stuecke}) == 1 and None not in {s.token for s in stuecke}:
            guete = "ohne Kommentar"
        elif stufe == "baum":
            guete = "sachlich gleich"
        else:
            guete = "gleich bis auf die Ausgabe"
        ergebnis.append((namen, guete))
    return sorted(ergebnis, key=lambda g: (-len(g[0]), g[0]))


def alle_namen(dateien):
    namen = set()
    for datei in dateien:
        namen |= set(datei.stuecke)
    # bekannte Reihenfolge zuerst, alles Weitere danach alphabetisch
    reihenfolge = ["collect_all_trades", "apply_btc_regime_filter",
                   "simulate_portfolio", "calculate_max_drawdown", HAUPTBLOCK]
    return [n for n in reihenfolge if n in namen] + sorted(namen - set(reihenfolge))


# ---------------------------------------------------------------------------
# Ausgabe
# ---------------------------------------------------------------------------

def uebersicht(dateien):
    liste = [d.bot for d in dateien]
    print(f"{len(liste)}x {dateien[0].dateiname}: " + ", ".join(liste))
    print()
    print("VORKOMMEN")
    print("-" * 72)
    for name in alle_namen(dateien):
        da = [d.bot for d in dateien if name in d.stuecke]
        marke = "alle neun" if len(da) == len(dateien) else ", ".join(da)
        print(f"  {name:<26} {len(da)}/{len(dateien)}  {marke if len(da) < len(dateien) else ''}")
    print()
    print("GRUPPEN SACHLICHER GLEICHHEIT (Stufe 3: AST ohne Docstrings)")
    print("-" * 72)
    for name in alle_namen(dateien):
        g = gruppen(dateien, name)
        print(f"\n  {name}   ({len(g)} Gruppe{'n' if len(g) != 1 else ''})")
        for namen, guete in g:
            if len(namen) == len(dateien):
                print(f"     alle {len(dateien)}, {guete}")
            else:
                print(f"     [{guete}] " + ", ".join(namen))
        ohne = gruppen(dateien, name, stufe="baum_ohne_ausgabe")
        if len(ohne) < len(g):
            print(f"     -> ohne die Bildschirmausgabe waeren es {len(ohne)} "
                  f"Gruppe{'n' if len(ohne) != 1 else ''}:")
            for namen, _ in ohne:
                print("        " + ", ".join(namen))
    print()
    print("SIGNATUREN")
    print("-" * 72)
    for name in alle_namen(dateien):
        if name == HAUPTBLOCK:
            continue
        print(f"\n  {name}")
        for datei in dateien:
            sig = datei.signatur(name)
            if sig:
                print(f"     {datei.bot:<28} {sig}")
    print()
    print("MODULWEITE KONSTANTEN")
    print("-" * 72)
    for k in KONSTANTEN:
        print(f"\n  {k}")
        for datei in dateien:
            if k in datei.konstanten:
                print(f"     {datei.bot:<28} {datei.konstanten[k]}")
            else:
                print(f"     {datei.bot:<28} -")


def pruefen(dateien):
    """Waechter: heutige Gruppierung gegen ERWARTUNG."""
    abweichungen = []
    namen_heute = set(alle_namen(dateien))
    namen_erwartet = set(ERWARTUNG)

    for neu in sorted(namen_heute - namen_erwartet):
        abweichungen.append(
            f"NEUE FUNKTION  {neu}: kommt in "
            f"{', '.join(d.bot for d in dateien if neu in d.stuecke)} vor und "
            f"steht nicht in ERWARTUNG.")
    for weg in sorted(namen_erwartet - namen_heute):
        abweichungen.append(f"FUNKTION FEHLT  {weg}: steht in ERWARTUNG, kommt nicht mehr vor.")

    for name in sorted(namen_heute & namen_erwartet):
        ist = [g[0] for g in gruppen(dateien, name)]
        soll = [tuple(sorted(g)) for g in ERWARTUNG[name]]
        if sorted(ist) != sorted(soll):
            abweichungen.append(
                f"GRUPPEN ANDERS  {name}\n"
                f"      erwartet: {sorted(soll)}\n"
                f"      gefunden: {sorted(ist)}")

    if abweichungen:
        print("ABWEICHUNG gegenueber dem Stand TB-27 (13.09.2026):\n")
        for a in abweichungen:
            print("  " + a)
        print("\nEntweder ist eine stille Divergenz entstanden - dann gehoert sie "
              "behoben -,\noder die Aenderung war gewollt; dann ist ERWARTUNG in "
              "diesem Werkzeug\nnachzuziehen und im Pull Request zu begruenden.")
        return 1

    print(f"UNVERAENDERT gegenueber dem Stand TB-27 (13.09.2026). "
          f"{len(namen_heute)} Funktionen ueber {len(dateien)} Bots geprueft.")
    return 0


def zeigen(dateien, name):
    g = gruppen(dateien, name)
    if not g:
        print(f"{name} kommt in keiner der Dateien vor.")
        return 1
    for namen, guete in g:
        print("=" * 72)
        print(f"{', '.join(namen)}   [{guete}]")
        print("=" * 72)
        erster = next(d for d in dateien if d.bot == namen[0])
        print(erster.stuecke[name].text)
        print()
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--pruefen", action="store_true",
                   help="Waechter-Betrieb, Rueckgabewert 1 bei Abweichung")
    p.add_argument("--zeige", metavar="FUNKTION",
                   help="Quelltext dieser Funktion je Gruppe ausgeben")
    p.add_argument("--datei", metavar="DATEI", default=DATEINAME,
                   help="andere je Bot vorhandene Datei vergleichen "
                        f"(Vorgabe: {DATEINAME})")
    args = p.parse_args(argv)

    if args.pruefen and args.datei != DATEINAME:
        p.error("--pruefen gibt es nur fuer " + DATEINAME
                + " - nur dafuer ist eine Erwartung festgehalten.")

    dateien = [Datei(b, args.datei) for b in bots(args.datei)]
    if not dateien:
        print(f"Keine strategies/*/{args.datei} gefunden.")
        return 1
    if args.zeige:
        return zeigen(dateien, args.zeige)
    if args.pruefen:
        return pruefen(dateien)
    uebersicht(dateien)
    return 0


if __name__ == "__main__":
    sys.exit(main())
