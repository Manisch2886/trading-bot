"""
TB-29 - Rastergroessen mechanisch aus dem Quelltext zaehlen
============================================================
Zaehlt, wie viele Parameter-Kombinationen ein Optimierungsskript je Lauf
auswertet. Rein statisch ueber den AST: es wird nichts importiert, nichts
ausgefuehrt und keine Kursdatei geoeffnet. Ohne pandas, ohne Netz.

Warum nicht einfach `len(itertools.product(...))` ablesen? Weil die neun
`multi_symbol_optimise.py` ihre Kombinationen in vier verschiedenen Formen
bilden - `itertools.product`, verschachtelte `for`-Schleifen, eine
List-Comprehension und eine Schleife, die zusaetzlich je Zwischenstufe
anhaengt (`elliott_wave_stocks`: das abgeschaltete Kursziel). Ein Zaehler,
der nur eine Form kennt, meldet fuer die anderen acht stillschweigend
nichts - und "nichts gefunden" saehe in einer Summe genauso aus wie "null
Versuche".

Das Zaehlmass
-------------
Gezaehlt werden **Auswertungsstellen**: jeder Aufruf einer Funktion, deren
Name mit `evaluate_combination` beginnt, gewichtet mit dem Produkt der
Schleifen, in denen er steht. Dazu Aufrufe anderer Funktionen desselben
oder eines importierten Nachbarmoduls, fuer die dasselbe Mass bereits
bestimmt ist (so erbt `multi_symbol_walk_forward.py` das Raster aus
`multi_symbol_optimise.py`).

Eine `yield`-Anweisung zaehlt ausdruecklich **nicht** mit. Ein Generator,
der Kombinationen liefert (`research/elliott_wave_params/search.py::combos`),
erzeugt Tupel; gerechnet wird erst, wo sie verbraucht werden. Wer `yield`
mitzaehlt, addiert jede Fundstelle von `combos()` erneut - und bekommt eine
Zahl, die nur zufaellig richtig aussieht.

Nicht gezaehlt wird das Anlegen einer Kombinationsliste. `combinations =
list(itertools.product(...))` erzeugt Tupel, wertet aber nichts aus; erst
die Schleife darueber tut das. Die Liste geht nur als **Schleifenlaenge**
in die Rechnung ein. Sonst haette `elliott_wave` 36 + 36 = 72 statt 36.

Was der Zaehler NICHT kann - und dann auch sagt
-----------------------------------------------
Eine Schleife ueber etwas, dessen Laenge statisch nicht feststeht (eine
Datei, ein Symbolverzeichnis, ein Funktionsergebnis), macht die Datei
`unklar`. Der Zaehler gibt dann keine Zahl aus, sondern den Grund. Eine
geratene Zahl waere hier schlimmer als eine Luecke, weil sie sich in der
Gesamtsumme nicht mehr von einer belegten unterscheiden liesse.
"""

import ast
import os


# Ein Aufruf an eine Funktion mit diesem Namensanfang ist eine
# Auswertungsstelle: hier wird genau eine Parameter-Kombination gerechnet.
AUSWERTUNG_PRAEFIX = "evaluate_combination"


class Unklar(Exception):
    """Die Groesse laesst sich aus dem Quelltext nicht bestimmen."""


class Modul:
    """Ein eingelesenes Python-Modul samt seiner Nachbarn im selben Ordner."""

    def __init__(self, pfad, cache=None):
        self.pfad = os.path.abspath(pfad)
        self.ordner = os.path.dirname(self.pfad)
        self.name = os.path.basename(self.pfad)
        self._cache = cache if cache is not None else {}
        self._cache[self.pfad] = self
        with open(self.pfad, encoding="utf-8") as fh:
            self.baum = ast.parse(fh.read(), filename=self.pfad)
        self._konstanten = None
        self._funktionen = None
        self._groessen = {}

    # ---------------------------------------------------------------- Nachbarn
    def nachbar(self, modulname):
        """Modul gleichen Ordners nachladen (`from multi_symbol_optimise import ...`)."""
        pfad = os.path.join(self.ordner, modulname + ".py")
        if not os.path.exists(pfad):
            return None
        if os.path.abspath(pfad) in self._cache:
            return self._cache[os.path.abspath(pfad)]
        return Modul(pfad, self._cache)

    # ------------------------------------------------------------- Konstanten
    @property
    def konstanten(self):
        """Name -> Laenge, fuer alle auf Modulebene gebundenen Folgen."""
        if self._konstanten is None:
            self._konstanten = {}
            for knoten in self.baum.body:
                self._binde_konstante(knoten, self._konstanten)
        return self._konstanten

    def _binde_konstante(self, knoten, umgebung):
        if isinstance(knoten, ast.Assign):
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Name):
                    laenge = self._laenge(knoten.value, umgebung)
                    if laenge is not None:
                        umgebung[ziel.id] = laenge
        elif isinstance(knoten, ast.AugAssign) and isinstance(knoten.op, ast.Add):
            if isinstance(knoten.target, ast.Name) and knoten.target.id in umgebung:
                zusatz = self._laenge(knoten.value, umgebung)
                if zusatz is None:
                    umgebung.pop(knoten.target.id, None)
                else:
                    umgebung[knoten.target.id] += zusatz
        elif isinstance(knoten, (ast.Import, ast.ImportFrom)):
            self._binde_import(knoten, umgebung)

    def _binde_import(self, knoten, umgebung):
        """`from <nachbarmodul> import A, B` - Konstanten von dort uebernehmen."""
        if not isinstance(knoten, ast.ImportFrom) or knoten.module is None:
            return
        nachbar = self.nachbar(knoten.module)
        if nachbar is None:
            return
        for alias in knoten.names:
            if alias.name in nachbar.konstanten:
                umgebung[alias.asname or alias.name] = nachbar.konstanten[alias.name]

    def _laenge(self, knoten, umgebung):
        """Laenge eines Ausdrucks, soweit statisch bestimmbar - sonst None."""
        if isinstance(knoten, (ast.List, ast.Tuple, ast.Set)):
            return len(knoten.elts)
        if isinstance(knoten, ast.Name):
            return umgebung.get(knoten.id)
        if isinstance(knoten, ast.BinOp) and isinstance(knoten.op, ast.Add):
            links = self._laenge(knoten.left, umgebung)
            rechts = self._laenge(knoten.right, umgebung)
            return None if links is None or rechts is None else links + rechts
        if isinstance(knoten, ast.IfExp):
            # `A if bedingung else B` - nur zaehlbar, wenn beide Zweige
            # gleich lang sind. Sonst haengt die Zahl an einer Bedingung,
            # die hier niemand auswertet.
            links = self._laenge(knoten.body, umgebung)
            rechts = self._laenge(knoten.orelse, umgebung)
            return links if links is not None and links == rechts else None
        if isinstance(knoten, ast.Subscript):
            # `{...}[BOT]` - nur zaehlbar, wenn alle Zweige gleich lang sind.
            if isinstance(knoten.value, ast.Dict):
                laengen = [self._laenge(v, umgebung) for v in knoten.value.values]
                if laengen and all(l is not None and l == laengen[0] for l in laengen):
                    return laengen[0]
            return None
        if isinstance(knoten, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
            produkt = 1
            for gen in knoten.generators:
                if gen.ifs:
                    return None
                teil = self._laenge(gen.iter, umgebung)
                if teil is None:
                    return None
                produkt *= teil
            return produkt
        if isinstance(knoten, ast.Call):
            ziel = _aufrufname(knoten.func)
            if ziel in ("list", "tuple", "set", "sorted") and len(knoten.args) == 1:
                return self._laenge(knoten.args[0], umgebung)
            if ziel in ("itertools.product", "product"):
                if knoten.keywords:
                    return None
                produkt = 1
                for arg in knoten.args:
                    teil = self._laenge(arg, umgebung)
                    if teil is None:
                        return None
                    produkt *= teil
                return produkt
            if ziel == "range":
                werte = [a.value for a in knoten.args
                         if isinstance(a, ast.Constant) and isinstance(a.value, int)]
                if len(werte) == len(knoten.args) == 1:
                    return werte[0]
                if len(werte) == len(knoten.args) == 2:
                    return max(0, werte[1] - werte[0])
        return None

    # ------------------------------------------------------------- Funktionen
    @property
    def funktionen(self):
        if self._funktionen is None:
            self._funktionen = {k.name: k for k in self.baum.body
                                if isinstance(k, ast.FunctionDef)}
        return self._funktionen

    def funktionsgroesse(self, name):
        """Auswertungsstellen einer Funktion dieses Moduls (0, wenn keine)."""
        if name in self._groessen:
            wert = self._groessen[name]
            if wert is _LAUFEND:
                raise Unklar(f"{self.name}: {name} ruft sich selbst auf")
            return wert
        knoten = self.funktionen.get(name)
        if knoten is None:
            return 0
        self._groessen[name] = _LAUFEND
        umgebung = dict(self.konstanten)
        wert = self._zaehle_block(knoten.body, umgebung, 1)
        self._groessen[name] = wert
        return wert

    def modulgroesse(self):
        """Auswertungsstellen eines vollstaendigen Laufs (der __main__-Block)."""
        umgebung = dict(self.konstanten)
        rumpf = []
        for knoten in self.baum.body:
            if _ist_main_block(knoten):
                rumpf = knoten.body
        if not rumpf:
            raise Unklar(f"{self.name}: kein `if __name__ == \"__main__\"`-Block")
        return self._zaehle_block(rumpf, umgebung, 1)

    # ------------------------------------------------------------ Kernzaehler
    def _zaehle_block(self, koerper, umgebung, faktor):
        summe = 0
        for knoten in koerper:
            summe += self._zaehle_knoten(knoten, umgebung, faktor)
        return summe

    def _zaehle_knoten(self, knoten, umgebung, faktor):
        if isinstance(knoten, ast.For):
            laenge = self._laenge(knoten.iter, umgebung)
            if laenge is None:
                # Schleifen ueber Symbole, Dateien oder Kursreihen sind fuer
                # das Raster belanglos - aber nur, wenn in ihnen auch keine
                # Auswertungsstelle steht. Steht dort eine, ist die Zahl
                # unbestimmbar und das gehoert gemeldet.
                if self._enthaelt_auswertung(knoten):
                    raise Unklar(
                        f"{self.name}: Schleife in Zeile {knoten.lineno} laeuft "
                        f"ueber etwas statisch Unbekanntes und enthaelt eine "
                        f"Auswertungsstelle")
                return 0
            return (self._zaehle_block(knoten.body, umgebung, faktor * laenge)
                    + self._zaehle_block(knoten.orelse, umgebung, faktor))
        if isinstance(knoten, (ast.While,)):
            if self._enthaelt_auswertung(knoten):
                raise Unklar(f"{self.name}: while-Schleife in Zeile {knoten.lineno} "
                             f"enthaelt eine Auswertungsstelle")
            return 0
        if isinstance(knoten, ast.If):
            # Beide Zweige zaehlen: welcher genommen wird, entscheidet sich
            # erst zur Laufzeit. In den geprueften Dateien steht in keinem
            # `if`-Zweig eine Auswertungsstelle; faende sich eine, waere die
            # gemeldete Zahl eine Obergrenze und das steht im Bericht.
            return (self._zaehle_block(knoten.body, umgebung, faktor)
                    + self._zaehle_block(knoten.orelse, umgebung, faktor))
        if isinstance(knoten, (ast.Try,)):
            summe = self._zaehle_block(knoten.body, umgebung, faktor)
            for behandler in knoten.handlers:
                summe += self._zaehle_block(behandler.body, umgebung, faktor)
            summe += self._zaehle_block(knoten.orelse, umgebung, faktor)
            summe += self._zaehle_block(knoten.finalbody, umgebung, faktor)
            return summe
        if isinstance(knoten, (ast.With,)):
            return self._zaehle_block(knoten.body, umgebung, faktor)
        if isinstance(knoten, (ast.Assign, ast.AugAssign, ast.ImportFrom, ast.Import)):
            self._binde_konstante(knoten, umgebung)
            return self._zaehle_ausdruecke(knoten, umgebung, faktor)
        if isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return 0     # Definitionen laufen nicht von selbst
        return self._zaehle_ausdruecke(knoten, umgebung, faktor)

    def _zaehle_ausdruecke(self, knoten, umgebung, faktor):
        """Auswertungsstellen in einer Anweisung ohne eigene Schleifenstruktur.

        Comprehensions sind hier der heikle Fall: `[f(x) for x in RANGE]`
        ist eine Schleife, steht aber im AST nicht als `For`. Ein Zaehler,
        der nur `ast.walk` benutzt, gewichtet den Aufruf darin mit 1 statt
        mit `len(RANGE)`.
        """
        return self._zaehle_ausdruck(knoten, umgebung, faktor)

    def _zaehle_ausdruck(self, knoten, umgebung, faktor):
        if isinstance(knoten, (ast.ListComp, ast.SetComp,
                               ast.GeneratorExp, ast.DictComp)):
            return self._zaehle_comprehension(knoten, umgebung, faktor)

        summe = 0
        if isinstance(knoten, ast.Call):
            self._wachse(knoten, umgebung, faktor)
            summe += faktor * self._aufrufgewicht(knoten)
        for kind in ast.iter_child_nodes(knoten):
            summe += self._zaehle_ausdruck(kind, umgebung, faktor)
        return summe

    def _zaehle_comprehension(self, knoten, umgebung, faktor):
        summe = 0
        innen = faktor
        for gen in knoten.generators:
            summe += self._zaehle_ausdruck(gen.iter, umgebung, innen)
            laenge = self._laenge(gen.iter, umgebung) if not gen.ifs else None
            if laenge is None:
                if self._enthaelt_auswertung(knoten):
                    raise Unklar(
                        f"{self.name}: Comprehension in Zeile {knoten.lineno} "
                        f"laeuft ueber etwas statisch Unbekanntes (oder ist "
                        f"gefiltert) und enthaelt eine Auswertungsstelle")
                return summe
            innen *= laenge
        teile = ([knoten.key, knoten.value] if isinstance(knoten, ast.DictComp)
                 else [knoten.elt])
        for teil in teile:
            summe += self._zaehle_ausdruck(teil, umgebung, innen)
        return summe

    def _wachse(self, aufruf, umgebung, faktor):
        """`combinations.append(...)` in einer Schleife verlaengert die Liste.

        `elliott_wave_stocks` baut sein Raster so: die innere Schleife haengt
        je Kursziel eine Zeile an, danach haengt die mittlere Schleife noch
        eine ohne Kursziel an. Wer nur die Zuweisung `combinations = []`
        ansieht, findet dort die Laenge 0 - und meldete fuer diesen Bot
        stillschweigend null Kombinationen.
        """
        if not isinstance(aufruf.func, ast.Attribute):
            return
        ziel = aufruf.func.value
        if not isinstance(ziel, ast.Name) or ziel.id not in umgebung:
            return
        if aufruf.func.attr == "append":
            umgebung[ziel.id] += faktor
        elif aufruf.func.attr == "extend" and len(aufruf.args) == 1:
            zusatz = self._laenge(aufruf.args[0], umgebung)
            if zusatz is None:
                umgebung.pop(ziel.id)      # Laenge nicht mehr bestimmbar
            else:
                umgebung[ziel.id] += faktor * zusatz

    def _aufrufgewicht(self, aufruf):
        name = _aufrufname(aufruf.func)
        if name is None:
            return 0
        kurz = name.rsplit(".", 1)[-1]
        if kurz.startswith(AUSWERTUNG_PRAEFIX):
            return 1
        if kurz in self.funktionen:
            return self.funktionsgroesse(kurz)
        herkunft = self._herkunft(kurz)
        if herkunft is not None:
            modul, urname = herkunft
            return modul.funktionsgroesse(urname)
        return 0

    def _herkunft(self, name):
        """Fundstelle eines aus einem Nachbarmodul importierten Funktionsnamens."""
        for knoten in ast.walk(self.baum):
            if not isinstance(knoten, ast.ImportFrom) or knoten.module is None:
                continue
            for alias in knoten.names:
                if (alias.asname or alias.name) != name:
                    continue
                nachbar = self.nachbar(knoten.module)
                if nachbar is not None and alias.name in nachbar.funktionen:
                    return nachbar, alias.name
        return None

    def _enthaelt_auswertung(self, knoten):
        for kind in ast.walk(knoten):
            if isinstance(kind, ast.Call):
                name = _aufrufname(kind.func)
                if name and name.rsplit(".", 1)[-1].startswith(AUSWERTUNG_PRAEFIX):
                    return True
        return False


_LAUFEND = object()


def _aufrufname(knoten):
    if isinstance(knoten, ast.Name):
        return knoten.id
    if isinstance(knoten, ast.Attribute):
        basis = _aufrufname(knoten.value)
        return f"{basis}.{knoten.attr}" if basis else knoten.attr
    return None


def _ist_main_block(knoten):
    if not isinstance(knoten, ast.If):
        return False
    pruef = knoten.test
    return (isinstance(pruef, ast.Compare)
            and isinstance(pruef.left, ast.Name)
            and pruef.left.id == "__name__")


# ----------------------------------------------------------------- Schnittstelle

def raster(pfad, funktion=None):
    """Kombinationen je Lauf. `funktion=None` -> der __main__-Block.

    Rueckgabe: (zahl, None) oder (None, grund).
    """
    try:
        modul = Modul(pfad)
        wert = modul.funktionsgroesse(funktion) if funktion else modul.modulgroesse()
        if wert == 0:
            # Null ist fuer ein Optimierungsskript keine Antwort, sondern ein
            # Hinweis, dass der Zaehler die Stelle nicht gefunden hat. Genau
            # so gehoert es gemeldet - eine 0 in einer Summe faellt nicht auf.
            return None, (f"{os.path.basename(pfad)}: keine Auswertungsstelle "
                          f"gefunden (Aufruf mit Namensanfang "
                          f"'{AUSWERTUNG_PRAEFIX}')")
        return wert, None
    except Unklar as fehler:
        return None, str(fehler)
    except (SyntaxError, OSError) as fehler:
        return None, f"{os.path.basename(pfad)}: {fehler}"


def raster_aus_text(quelltext, name="<text>"):
    """Wie `raster`, aber auf einem Quelltext im Speicher (fuer die Historie)."""
    import tempfile
    with tempfile.TemporaryDirectory() as ordner:
        pfad = os.path.join(ordner, name)
        with open(pfad, "w", encoding="utf-8") as fh:
            fh.write(quelltext)
        return raster(pfad)
