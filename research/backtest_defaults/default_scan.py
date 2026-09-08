"""
Bestandsaufnahme: welche Funktions-Defaults wirken wirklich?
================================================================================
Fuer alle 9 Bots: jeder Parameter mit Default-Wert wird gegen JEDE
Aufrufstelle im Bot-Ordner gehalten. Die Leitfrage ist nicht "stimmt der
Wert?", sondern:

    Wird dieser Default im LIVE-Pfad explizit ueberschrieben (dann ist er
    ein folgenloses Duplikat) - oder wirkt er dort tatsaechlich?

Ein Default, den jeder Aufrufer ohnehin ueberschreibt, ist harmlos. Ein
Default, den niemand ueberschreibt, ist der tatsaechlich wirksame Wert
der Strategie und gehoert damit an live_params.py gekoppelt - es sei
denn, ein Optimierungs-Skript variiert ihn absichtlich.

WAS "LIVE-PFAD" HIER HEISST - und warum das nicht am Dateinamen haengt:

Die naheliegende Regel "equity_simulation.py ist live, multi_symbol_optimise.py
ist Grid-Search" ist FALSCH. equity_simulation.py importiert aus
multi_symbol_optimise.py die Funktion get_trades_for_symbol(), und genau
darin steht der eigentliche run_backtest()-Aufruf, der die live gemeldeten
Zahlen erzeugt. Eine Einteilung nach Datei wuerde diesen Aufruf als
"Grid-Search" abtun und damit ausgerechnet die wichtigsten Faelle
(MAX_HOLD_DAYS und die Squeeze-Parameter) uebersehen.

Deshalb wird ein AUFRUFGRAPH ueber den ganzen Bot-Ordner gebaut und von
den Live-Einstiegspunkten (equity_simulation.py, forward_test.py) aus
transitiv markiert. Eine Aufrufstelle gilt als LIVE,
wenn die Funktion, IN DER sie steht, von dort aus erreichbar ist. So ist
multi_symbol_optimise.get_trades_for_symbol LIVE, das daneben stehende
evaluate_combination_multi() aber nicht.

Die uebrigen Aufrufstellen:
  SUCHE   optimise_*.py, multi_symbol_optimise.py, *walk_forward*.py,
          agent_optimise.py, oos_equity_simulation.py - variieren
          Parameter ABSICHTLICH. Eine
          Uebergabe hier macht den Default fuer den Live-Pfad nicht
          folgenlos, zeigt aber, dass der Parameter Variationsfreiheit
          braucht und deshalb NICHT gekoppelt werden darf.
  STUDIE  experiment_*.py, stress_*.py, analysis_*.py usw. - einmalige
          Untersuchungen. Wie SUCHE: sagt nichts ueber den Live-Pfad aus.

WARUM AST UND NICHT TEXTSUCHE: eine Textsuche nach "stop_loss_pct=" findet
auch Kommentare, Docstrings und gleichnamige Parameter fremder Funktionen.
Genau diese Verwechslung hat in research/sync_check/ schon einmal einen
echten Befund verdeckt. Hier wird der Syntaxbaum ausgewertet - inklusive
POSITIONS-Argumente, die genauso ueberschreiben wie Schluesselwoerter und
die eine Suche nach "name=" komplett verpassen wuerde.

WICHTIG - reine Untersuchung: veraendert keine Datei ausserhalb von
research/backtest_defaults/.

Nutzung:  python3 default_scan.py [--json] [--nur-wirksam]
"""

import ast
import json
import os
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
STRATEGIES = os.path.join(_REPO_ROOT, "strategies")
RESULTS_DIR = os.path.join(_DIR, "results")

BOTS = ["elliott_wave", "elliott_wave_stocks", "t3_supertrend",
        "rsi2_crypto", "rsi2_mean_reversion",
        "turtle_soup_crypto", "turtle_soup_stocks",
        "volatility_breakout", "volatility_breakout_crypto"]

# Einstiegspunkte des Live-Pfads. Alles, was von hier aus erreichbar ist,
# erzeugt die live gemeldeten Zahlen.
#
# oos_equity_simulation.py gehoert bewusst NICHT dazu, obwohl der Name das
# nahelegt: dieses Skript optimiert erst auf dem In-Sample-Zeitraum und
# rechnet die Kapitalsimulation dann mit den DORT gefundenen Parametern -
# nicht mit den Live-Werten. Das ist der Sinn einer Out-of-Sample-Pruefung.
# Wuerde man es als Live-Pfad zaehlen, meldete der Scan jede bewusste
# Abweichung dieses Skripts als Sync-Luecke.
LIVE_EINSTIEG = ("equity_simulation.py", "forward_test.py")

# Dateien, deren Zweck das absichtliche Variieren von Parametern ist.
SUCHE_DATEIEN = ("optimise_", "multi_symbol_optimise", "walk_forward",
                 "agent_optimise", "oos_equity_simulation")

MODULEBENE = "<modulebene>"


# ---------------------------------------------------------------------------
# AST-Hilfen
# ---------------------------------------------------------------------------

def _baum(pfad: str) -> ast.Module:
    with open(pfad, encoding="utf-8") as f:
        return ast.parse(f.read(), filename=pfad)


def _wert(knoten):
    """Literalwert eines Default-Ausdrucks, sonst der Bezeichnername."""
    try:
        return ast.literal_eval(knoten)
    except (ValueError, SyntaxError):
        if isinstance(knoten, ast.Name):
            return f"<{knoten.id}>"
        if isinstance(knoten, ast.Attribute):
            return f"<...{knoten.attr}>"
        return "<Ausdruck>"


def modul_konstanten(pfad: str) -> dict:
    """Modulweite Zuweisungen GROSSGESCHRIEBENER Namen mit Literalwert."""
    werte = {}
    for knoten in _baum(pfad).body:
        if not isinstance(knoten, ast.Assign):
            continue
        try:
            wert = ast.literal_eval(knoten.value)
        except (ValueError, SyntaxError):
            continue
        for ziel in knoten.targets:
            if isinstance(ziel, ast.Name) and ziel.id.isupper():
                werte[ziel.id] = wert
    return werte


def live_params_importe(pfad: str) -> dict:
    """{name_im_modul: name_in_live_params} fuer from live_params import ..."""
    namen = {}
    for knoten in ast.walk(_baum(pfad)):
        if isinstance(knoten, ast.ImportFrom) and knoten.module == "live_params":
            for alias in knoten.names:
                namen[alias.asname or alias.name] = alias.name
    return namen


class Datei:
    """Eine Python-Datei eines Bots, aufbereitet fuer den Aufrufgraphen."""

    def __init__(self, ordner: str, name: str):
        self.name = name
        self.baum = _baum(os.path.join(ordner, name))

        # from X import f [as g]  ->  {g: (X.py, f)}
        self.import_von = {}
        # import X [as g]         ->  {g: X.py}
        self.import_modul = {}
        for knoten in ast.walk(self.baum):
            if isinstance(knoten, ast.ImportFrom) and knoten.module:
                for alias in knoten.names:
                    self.import_von[alias.asname or alias.name] = \
                        (knoten.module + ".py", alias.name)
            elif isinstance(knoten, ast.Import):
                for alias in knoten.names:
                    self.import_modul[alias.asname or alias.name] = \
                        alias.name + ".py"

        self.funktionen = {k.name: k for k in self.baum.body
                            if isinstance(k, (ast.FunctionDef, ast.AsyncFunctionDef))}

    def aufloesen(self, knoten: ast.Call):
        """Aufrufziel als (datei, funktionsname) - oder None."""
        ziel = knoten.func
        if isinstance(ziel, ast.Name):
            if ziel.id in self.funktionen:
                return (self.name, ziel.id)
            if ziel.id in self.import_von:
                return self.import_von[ziel.id]
            return None
        if isinstance(ziel, ast.Attribute) and isinstance(ziel.value, ast.Name):
            modul = self.import_modul.get(ziel.value.id)
            if modul:
                return (modul, ziel.attr)
        return None

    def defaults(self) -> dict:
        """{funktionsname: {"params": [(name, wert, quelle)], "reihenfolge": [...]}}"""
        ergebnis = {}
        for name, knoten in self.funktionen.items():
            args = knoten.args
            alle = args.posonlyargs + args.args
            versatz = len(alle) - len(args.defaults)
            params = []
            for i, default in enumerate(args.defaults):
                quelle = default.id if isinstance(default, ast.Name) else None
                params.append((alle[versatz + i].arg, _wert(default), quelle))
            for arg, default in zip(args.kwonlyargs, args.kw_defaults):
                if default is None:
                    continue
                quelle = default.id if isinstance(default, ast.Name) else None
                params.append((arg.arg, _wert(default), quelle))
            if params:
                ergebnis[name] = {"params": params,
                                   "reihenfolge": [a.arg for a in alle]}
        return ergebnis

    def aufrufstellen(self) -> list:
        """Alle Aufrufe, jeweils mit der Funktion, IN DER sie stehen."""
        treffer = []

        def besuche(knoten, umgebung):
            for kind in ast.iter_child_nodes(knoten):
                if isinstance(kind, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    besuche(kind, kind.name if umgebung == MODULEBENE
                            else f"{umgebung}.{kind.name}")
                    continue
                if isinstance(kind, ast.Call):
                    zielk = self.aufloesen(kind)
                    if zielk:
                        keywords = {kw.arg for kw in kind.keywords if kw.arg}
                        stern = any(kw.arg is None for kw in kind.keywords) or \
                                any(isinstance(a, ast.Starred) for a in kind.args)
                        positional = sum(1 for a in kind.args
                                          if not isinstance(a, ast.Starred))
                        treffer.append({
                            "von": (self.name, umgebung),
                            "nach": zielk,
                            "keywords": keywords,
                            "positional": positional,
                            "stern": stern,
                            "zeile": kind.lineno,
                        })
                besuche(kind, umgebung)

        besuche(self.baum, MODULEBENE)
        return treffer


# ---------------------------------------------------------------------------
# Auswertung je Bot
# ---------------------------------------------------------------------------

def ist_suchdatei(name: str) -> bool:
    return any(name.startswith(p) or name[:-3] == p for p in SUCHE_DATEIEN)


def analysiere_bot(bot: str) -> dict:
    ordner = os.path.join(STRATEGIES, bot)
    namen = sorted(f for f in os.listdir(ordner) if f.endswith(".py"))
    dateien = {n: Datei(ordner, n) for n in namen}

    kanten = [k for d in dateien.values() for k in d.aufrufstellen()]

    # --- Live-Erreichbarkeit transitiv bestimmen --------------------------
    # Wurzeln: alles, was in einer Live-Einstiegsdatei steht. Diese Skripte
    # laufen als Ganzes; welche ihrer eigenen Hilfsfunktionen genutzt wird,
    # muss hier nicht unterschieden werden.
    erreichbar = set()
    rand = []
    for name, datei in dateien.items():
        if name in LIVE_EINSTIEG:
            rand.append((name, MODULEBENE))
            rand.extend((name, f) for f in datei.funktionen)
    erreichbar.update(rand)

    nachfolger = {}
    for kante in kanten:
        nachfolger.setdefault(kante["von"], set()).add(kante["nach"])

    while rand:
        knoten = rand.pop()
        for ziel in nachfolger.get(knoten, ()):
            # Ein Ziel ist als Funktion erreichbar; von dort geht es weiter.
            if ziel not in erreichbar:
                erreichbar.add(ziel)
                rand.append(ziel)
            # Verschachtelte Funktionen unter dem Ziel ebenfalls aufnehmen
            for kante in kanten:
                if kante["von"][0] == ziel[0] and \
                        kante["von"][1].startswith(ziel[1] + ".") and \
                        kante["von"] not in erreichbar:
                    erreichbar.add(kante["von"])
                    rand.append(kante["von"])

    def rolle(von):
        if von in erreichbar:
            return "LIVE"
        if ist_suchdatei(von[0]):
            return "SUCHE"
        return "STUDIE"

    # --- Defaults gegen die Aufrufstellen halten --------------------------
    live_werte = modul_konstanten(os.path.join(ordner, "live_params.py"))

    zeilen = []
    for dname, datei in dateien.items():
        if dname in ("live_params.py", "forward_test.py"):
            continue      # nicht Gegenstand dieser Aufgabe
        aus_live = live_params_importe(os.path.join(ordner, dname))
        eigene_konstanten = modul_konstanten(os.path.join(ordner, dname))

        for fname, info in datei.defaults().items():
            reihenfolge = info["reihenfolge"]
            relevante = [k for k in kanten if k["nach"] == (dname, fname)]

            for pname, wert, quelle in info["params"]:
                index = reihenfolge.index(pname) if pname in reihenfolge else None

                ueberschrieben = {"LIVE": [], "SUCHE": [], "STUDIE": []}
                wirkt_in = {"LIVE": [], "SUCHE": [], "STUDIE": []}
                unklar = []
                for k in relevante:
                    stelle = f"{k['von'][0]}:{k['zeile']}"
                    r = rolle(k["von"])
                    getroffen = pname in k["keywords"] or \
                        (index is not None and k["positional"] > index)
                    if k["stern"]:
                        unklar.append(stelle)
                    (ueberschrieben if getroffen else wirkt_in)[r].append(stelle)

                zeilen.append({
                    "bot": bot,
                    "datei": dname,
                    "funktion": fname,
                    "parameter": pname,
                    "default": wert,
                    "default_quelle": quelle,
                    "quelle_aus_live_params": aus_live.get(quelle),
                    "quelle_wert": eigene_konstanten.get(quelle),
                    "aufrufe_gesamt": len(relevante),
                    "ueberschrieben": {k: v for k, v in ueberschrieben.items() if v},
                    "wirkt_in": {k: v for k, v in wirkt_in.items() if v},
                    "unklar_wegen_sternchen": unklar,
                    "wirksam_im_live_pfad": bool(wirkt_in["LIVE"]),
                    "variiert_in_suche": bool(ueberschrieben["SUCHE"]),
                    "variiert_in_studie": bool(ueberschrieben["STUDIE"]),
                })

    return {
        "bot": bot,
        "parameter": zeilen,
        "live_werte": live_werte,
        "live_erreichbar": sorted(f"{d}:{f}" for d, f in erreichbar),
    }


# ---------------------------------------------------------------------------

def main():
    alle = [analysiere_bot(bot) for bot in BOTS]

    if "--json" in sys.argv:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        ziel = os.path.join(RESULTS_DIR, "default_scan.json")
        with open(ziel, "w", encoding="utf-8") as f:
            json.dump(alle, f, indent=2, ensure_ascii=False, default=str)
        print(f"geschrieben: {ziel}\n")

    nur_wirksam = "--nur-wirksam" in sys.argv

    kopf = (f"{'Bot':<27} {'Datei':<26} {'Funktion':<22} {'Parameter':<24} "
            f"{'Default':>26}  Status")
    print(kopf)
    print("-" * len(kopf))
    for eintrag in alle:
        for z in eintrag["parameter"]:
            if nur_wirksam and not z["wirksam_im_live_pfad"]:
                continue
            if z["aufrufe_gesamt"] == 0:
                status = "nie aufgerufen"
            elif z["wirksam_im_live_pfad"]:
                status = "WIRKT LIVE"
                if z["variiert_in_suche"]:
                    status += " (+ Suche variiert)"
            elif z["ueberschrieben"].get("LIVE"):
                status = "live ueberschrieben"
            else:
                status = "nur Suche/Studie"
            print(f"{z['bot']:<27} {z['datei']:<26} {z['funktion']:<22} "
                  f"{z['parameter']:<24} {str(z['default']):>26}  {status}")

    wirksam = [z for e in alle for z in e["parameter"] if z["wirksam_im_live_pfad"]]
    print(f"\n{len(wirksam)} Parameter wirken im Live-Pfad ueber ihren Default.")
    unklar = [z for e in alle for z in e["parameter"] if z["unklar_wegen_sternchen"]]
    if unklar:
        print(f"WARNUNG: {len(unklar)} Parameter mit *args/**kwargs-Aufrufstellen - "
              f"dort ist die Zuordnung statisch nicht entscheidbar:")
        for z in unklar:
            print(f"  {z['bot']}/{z['datei']}:{z['funktion']}({z['parameter']}) "
                  f"-> {z['unklar_wegen_sternchen']}")


if __name__ == "__main__":
    main()
