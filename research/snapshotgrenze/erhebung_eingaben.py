#!/usr/bin/env python3
"""
TB-47, Teil 1 - Was gehoert in den Snapshot?
==============================================================================
Registertext 5a sagt: der Snapshot enthaelt **alle Eingaben des Laufs, die
nicht Code unter dem registrierten Commit sind**. Diese Menge ist zu
**bestimmen**, nicht zu raten. Dieses Programm bestimmt sie.

⚠️ **Es misst und aendert nichts.** Es liest Quelltext, baut den Syntaxbaum
und schreibt eine Tabelle. Es fasst `data/` nicht an, es importiert die
untersuchten Module nicht (TB-40: gleichnamige Module werden nicht
importiert - `ast.parse` braucht keinen Import).

Warum ueber den Syntaxbaum und nicht per Textsuche
------------------------------------------------------------------------------
Eine Textsuche nach `open(` findet `# open( ist hier verboten` und findet
`pd.read_csv(pfad)` nicht als Leser einer *bestimmten* Datei. Der Syntaxbaum
kennt den Unterschied zwischen einem Aufruf und einer Zeichenkette, er kennt
das Argument an seiner Stelle, und er loest eine Konstante auf, die zehn
Zeilen weiter oben zugewiesen wurde. TB-46 hat denselben Weg genommen; dies
hier ist die Fortsetzung mit einer anderen Frage.

Die Ausgangsmenge
------------------------------------------------------------------------------
Die **90 Selektionsmodule** aus TB-46
(`research/datenordner_schnitt/ergebnisse/erhebung.json`, Rolle
`Selektion/Backtest`). ⚠️ **Die Rollenzuordnung wird uebernommen** - sie ist
dort begruendet und gemessen. **Die Dateiliste wird neu erhoben**, denn TB-46
hat nach `data/` gefragt, nicht nach Nicht-Code-Eingaben.

⚠️ Erhoben wird ueber die **transitive Huelle**: ein Selektionsmodul, das
`shared/kursdaten.py` importiert, liest auch das, was jenes liest. Wer nur
die 90 Dateien ansieht, findet die Symbolliste nicht, die ein importiertes
Modul oeffnet.

Die drei Einstufungen
------------------------------------------------------------------------------
  **Eingabe**    Eine Datei im Repo oder unter `config/`, die der Lauf liest
                 und die nicht Code unter dem registrierten Commit ist.
                 **Sie gehoert in den Snapshot.**
  **Umgebung**   Eine Datei, die aus einem **Fremdpaket** kommt. Sie gehoert
                 ins Lock, nicht in den Snapshot - ihr Inhalt haengt an einer
                 Paketfassung, und die steht woanders.
  **unklar**     ⚠️ **Ein gueltiger Ausgang.** Ein Pfad, der zur Laufzeit
                 entsteht, ein Argument aus der Befehlszeile, eine Variable,
                 die dieses Programm nicht aufloesen kann. Wird berichtet,
                 nicht geraten.

Zusaetzlich, und ausserhalb der drei: **erzeugt** - eine Datei, die der Lauf
selbst schreibt und danach wieder liest. Sie ist keine Eingabe des Laufs,
sondern sein Zwischenstand.

Nutzung
------------------------------------------------------------------------------
    python3 research/snapshotgrenze/erhebung_eingaben.py
    python3 research/snapshotgrenze/erhebung_eingaben.py --json ergebnisse/eingaben.json
"""

import argparse
import ast
import json
import os
import subprocess
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))

TB46_ERHEBUNG = os.path.join(_WURZEL, "research", "datenordner_schnitt",
                             "ergebnisse", "erhebung.json")
SELEKTIONSROLLE = "Selektion/Backtest"

AUSGENOMMEN = ("trading-env", "__pycache__", ".git", "node_modules")

# Aufrufe, die eine Datei oeffnen. Der Wert ist die Nummer des Arguments,
# an dem der Pfad steht.
LESE_AUFRUFE = {
    "open": 0,
    "read_csv": 0,
    "read_json": 0,
    "read_excel": 0,
    "read_parquet": 0,
    "read_table": 0,
    "read_text": None,      # Path.read_text() - der Pfad ist das Objekt
    "read_bytes": None,
    "load": 0,              # json.load / pickle.load - Sonderfall, s.u.
    "loads": None,
    "safe_load": 0,
}

# Endungen, die als Nicht-Code gelten. `.py` ist Code und faellt heraus.
NICHT_CODE = (".csv", ".json", ".txt", ".yaml", ".yml", ".db", ".sqlite",
              ".parquet", ".xlsx", ".pkl", ".pickle", ".ini", ".cfg", ".md")

# Fremdpakete, deren Dateien Umgebung sind, nicht Eingabe.
FREMDPAKETE = ("pandas_market_calendars", "exchange_calendars", "pandas",
               "numpy", "yfinance", "binance", "dateparser", "pytz",
               "scipy", "matplotlib", "holidays")


class Fund:
    """Eine Fundstelle: hier liest ein Modul eine Nicht-Code-Datei."""

    def __init__(self, modul, zeile, leser, ausdruck, ziel=None):
        self.modul = modul
        self.zeile = zeile
        self.leser = leser
        self.ausdruck = ausdruck
        self.ziel = ziel            # aufgeloester Pfad, wenn bestimmbar

    def als_dict(self):
        return {"modul": self.modul, "zeile": self.zeile, "leser": self.leser,
                "ausdruck": self.ausdruck, "ziel": self.ziel}


# ===========================================================================
# Quelltext lesen und den Baum bauen
# ===========================================================================

def _quelle(knoten, zeilen):
    """Die Quelltextzeile(n) eines Knotens - fuer die Tabelle."""
    try:
        anfang = knoten.lineno - 1
        ende = getattr(knoten, "end_lineno", knoten.lineno)
        text = " ".join(z.strip() for z in zeilen[anfang:ende])
    except (AttributeError, IndexError):
        return "?"
    return text[:160]


def _punktname(knoten):
    """`os.path.join` aus einem Attribute-Baum - oder None."""
    teile = []
    while isinstance(knoten, ast.Attribute):
        teile.append(knoten.attr)
        knoten = knoten.value
    if isinstance(knoten, ast.Name):
        teile.append(knoten.id)
    elif not teile:
        return None
    return ".".join(reversed(teile))


def _schreibmodus(knoten, konstanten):
    """Oeffnet dieser `open`-Aufruf zum Schreiben?

    Der Modus steht als zweites Argument oder als `mode=`. Steht er nicht da,
    ist es der Lesemodus `"r"` - das ist die Voreinstellung von `open`.
    """
    modus = None
    if len(knoten.args) > 1:
        modus = _statischer_wert(knoten.args[1], konstanten)
    for schluessel in knoten.keywords:
        if schluessel.arg == "mode":
            modus = _statischer_wert(schluessel.value, konstanten)
    if modus is None:
        return False
    return any(z in modus for z in ("w", "a", "x", "+"))


def _ruf_name(knoten):
    """Der Name der gerufenen Funktion: `open`, `read_csv`, `json.load`."""
    if isinstance(knoten.func, ast.Name):
        return knoten.func.id
    if isinstance(knoten.func, ast.Attribute):
        return knoten.func.attr
    return None


# ===========================================================================
# Konstanten aufloesen
# ===========================================================================

def _modulkonstanten(baum):
    """Namen auf oberster Ebene, die auf eine Zeichenkette zeigen.

    Nur das Einfache: `LISTE = "symbole.json"` und
    `LISTE = os.path.join(BASE_DIR, "symbole.json")`. Alles andere bleibt
    ungeloest - und das ist dann **unklar**, nicht geraten.
    """
    konstanten = {}
    for knoten in baum.body:
        if not isinstance(knoten, ast.Assign) or len(knoten.targets) != 1:
            continue
        ziel = knoten.targets[0]
        if not isinstance(ziel, ast.Name):
            continue
        wert = _statischer_wert(knoten.value, konstanten)
        if wert is not None:
            konstanten[ziel.id] = wert
            continue
        # ⚠️ Nicht ganz aufloesbar heisst nicht wertlos: der Dateiname steht
        # oft als Literal im sonst dynamischen Pfadbau (siehe `_literale`).
        teile = _literale(knoten.value, konstanten)
        if teile:
            konstanten[ziel.id] = teile
    return konstanten


def _literale(knoten, konstanten, tiefe=0):
    """Alle Zeichenketten-Literale im Teilbaum eines Ausdrucks.

    ⚠️ **Das ist die Stelle, an der der erste Anlauf dieser Erhebung
    gescheitert ist.** Ein Pfad steht im Projekt fast nie als ganzes Literal
    da; er entsteht aus einem Wurzelpfad, der zur Laufzeit berechnet wird:

        CONFIG_DIR  = os.path.join(BASE_DIR, "config")
        SYMBOLS_FILE = os.path.join(CONFIG_DIR, "top25_symbols.txt")
        open(SYMBOLS_FILE)

    `BASE_DIR` ist `os.path.dirname(...)` und steht statisch **nicht** fest.
    Wer den ganzen Ausdruck aufloesen will, bekommt `None` - und uebersieht
    `top25_symbols.txt`, die **Symbolliste aller neun Bots**.

    Der Dateiname steht aber sehr wohl da. Dieses Verfahren sammelt deshalb
    die Literale ein und laesst den unaufloesbaren Wurzelteil weg; die
    Zuordnung zu einer wirklichen Datei macht `einstufen` danach ueber den
    Basisnamen.
    """
    gefunden = []
    if tiefe > 12:
        return gefunden
    if isinstance(knoten, ast.Constant) and isinstance(knoten.value, str):
        return [knoten.value]
    if isinstance(knoten, ast.Name):
        wert = konstanten.get(knoten.id)
        if isinstance(wert, str):
            return [wert]
        if isinstance(wert, list):
            return list(wert)
        return gefunden
    for kind in ast.iter_child_nodes(knoten):
        gefunden.extend(_literale(kind, konstanten, tiefe + 1))
    return gefunden


def _dateinamen(knoten, konstanten):
    """Die Literale, die wie eine Nicht-Code-Datei aussehen."""
    treffer = []
    for wert in _literale(knoten, konstanten):
        if any(wert.lower().endswith(e) for e in NICHT_CODE):
            treffer.append(wert)
    return treffer


def _statischer_wert(knoten, konstanten):
    """Den Wert eines Ausdrucks bestimmen - oder None, wenn er nicht steht."""
    if isinstance(knoten, ast.Constant) and isinstance(knoten.value, str):
        return knoten.value
    if isinstance(knoten, ast.Name):
        wert = konstanten.get(knoten.id)
        # Eine Liste ist ein **Teilergebnis** (gesammelte Literale), kein
        # aufgeloester Pfad. Sie darf hier nicht als Zeichenkette durchgehen.
        return wert if isinstance(wert, str) else None
    if isinstance(knoten, ast.JoinedStr):       # f-string
        teile = []
        for stueck in knoten.values:
            if isinstance(stueck, ast.Constant) and isinstance(stueck.value, str):
                teile.append(stueck.value)
            else:
                teile.append("{?}")
        return "".join(teile)
    if isinstance(knoten, ast.BinOp) and isinstance(knoten.op, ast.Add):
        links = _statischer_wert(knoten.left, konstanten)
        rechts = _statischer_wert(knoten.right, konstanten)
        if links is not None and rechts is not None:
            return links + rechts
        return None
    if isinstance(knoten, ast.Call):
        name = _punktname(knoten.func) or ""
        if name.endswith("os.path.join") or name == "join":
            teile = [_statischer_wert(a, konstanten) for a in knoten.args]
            if any(t is None for t in teile):
                return None
            return "/".join(t.strip("/") for t in teile if t)
    return None


# ===========================================================================
# Ein Modul untersuchen
# ===========================================================================

def untersuche(pfad, rel):
    """Alle Lesestellen fuer Nicht-Code-Dateien in einem Modul."""
    try:
        with open(pfad, "r", encoding="utf-8") as datei:
            text = datei.read()
    except OSError as fehler:
        return [], [], "nicht lesbar: %s" % fehler
    try:
        baum = ast.parse(text, filename=pfad)
    except SyntaxError as fehler:
        return [], [], "nicht parsbar: %s" % fehler

    zeilen = text.splitlines()
    konstanten = _modulkonstanten(baum)
    funde = []

    for knoten in ast.walk(baum):
        if not isinstance(knoten, ast.Call):
            continue
        name = _ruf_name(knoten)
        if name not in LESE_AUFRUFE:
            continue

        # json.load(f) / pickle.load(f) bekommen ein Dateiobjekt, keinen
        # Pfad. Die Datei steht dann am `open` weiter oben - dort wird sie
        # schon gezaehlt. Hier nur mitnehmen, wenn wirklich ein Pfad steht.
        # ⚠️ `open` ist nicht immer ein Leser. `open(pfad, "w")` **schreibt**,
        # und eine geschriebene Datei ist keine Eingabe des Laufs. Ohne diese
        # Unterscheidung stand `shared/abrufschutz.py:552` - eine
        # JSON-Ausgabe - als unklare Eingabe in der Tabelle.
        if name == "open" and _schreibmodus(knoten, konstanten):
            continue

        stelle = LESE_AUFRUFE[name]
        argument = None
        if stelle is not None and len(knoten.args) > stelle:
            argument = knoten.args[stelle]
        elif stelle is None and isinstance(knoten.func, ast.Attribute):
            argument = knoten.func.value
        if argument is None:
            continue

        quelle = _quelle(knoten, zeilen)
        namen = _dateinamen(argument, konstanten)
        if namen:
            for treffer in sorted(set(namen)):
                funde.append(Fund(rel, knoten.lineno, name, quelle, treffer))
            continue

        # Kein Literal im Ausdruck. Nur behalten, wenn die Zeile ueberhaupt
        # nach einer Nicht-Code-Datei aussieht - sonst ertrinkt die Tabelle
        # in `open(irgendwas)`. Ausgang: **unklar**, nicht geraten.
        if not any(e in quelle for e in NICHT_CODE):
            continue
        funde.append(Fund(rel, knoten.lineno, name, quelle, None))

    # Importe - fuer die transitive Huelle
    importe = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            for alias in knoten.names:
                importe.append(alias.name)
        elif isinstance(knoten, ast.ImportFrom):
            if knoten.module:
                importe.append(knoten.module)
    return funde, importe, None


# ===========================================================================
# Die transitive Huelle der 90
# ===========================================================================

def _modulpfad(name, wurzel):
    """Einen Importnamen auf eine Datei im Repo abbilden - oder None.

    None heisst: das ist kein Modul dieses Repos, also ein Fremdpaket oder
    die Standardbibliothek.
    """
    teile = name.split(".")
    for stamm in ("", "shared", "strategies", "research", "config"):
        kandidat = os.path.join(wurzel, stamm, *teile) + ".py"
        if os.path.isfile(kandidat):
            return os.path.relpath(kandidat, wurzel)
        kandidat = os.path.join(wurzel, stamm, *teile, "__init__.py")
        if os.path.isfile(kandidat):
            return os.path.relpath(kandidat, wurzel)
    return None


def _gleichnamige(name, wurzel):
    """Alle Dateien im Repo, die so heissen.

    ⚠️ Das Projekt hat gleichnamige Module in verschiedenen Strategieordnern
    (neun `equity_simulation.py`). Ein `import live_params` in
    `strategies/rsi2_crypto/` meint das dortige. Weil der Suchpfad zur
    Laufzeit vom Arbeitsverzeichnis abhaengt, werden hier **alle**
    Gleichnamigen in die Huelle genommen - lieber zu viel ansehen als eine
    Eingabe uebersehen.
    """
    treffer = []
    for ordner, unter, dateien in os.walk(wurzel):
        unter[:] = [u for u in unter if u not in AUSGENOMMEN
                    and not u.startswith(".")]
        if name + ".py" in dateien:
            treffer.append(os.path.relpath(os.path.join(ordner, name + ".py"),
                                           wurzel))
    return treffer


def huelle(start, wurzel):
    """Die 90 plus alles, was sie (transitiv) importieren."""
    offen = list(start)
    gesehen = set()
    funde = []
    fehler = {}
    importe_gesamt = {}

    while offen:
        rel = offen.pop()
        if rel in gesehen:
            continue
        gesehen.add(rel)
        pfad = os.path.join(wurzel, rel)
        if not os.path.isfile(pfad):
            continue
        f, importe, problem = untersuche(pfad, rel)
        if problem:
            fehler[rel] = problem
            continue
        funde.extend(f)
        importe_gesamt[rel] = sorted(set(importe))
        for name in importe:
            kurz = name.split(".")[0]
            ziel = _modulpfad(name, wurzel)
            if ziel:
                offen.append(ziel)
            else:
                for g in _gleichnamige(kurz, wurzel):
                    offen.append(g)
    return funde, sorted(gesehen), fehler, importe_gesamt


# ===========================================================================
# Einstufen
# ===========================================================================

def versioniert(rel, wurzel):
    """Steht die Datei unter Versionskontrolle?

    ⚠️ Eine gitignorierte Eingabedatei ist der gefaehrlichste Fall: sie
    existiert genau einmal, auf genau einem Rechner.
    """
    try:
        ergebnis = subprocess.run(
            ["git", "ls-files", "--error-unmatch", rel],
            cwd=wurzel, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return ergebnis.returncode == 0
    except OSError:
        return None


def einstufen(ziel, wurzel):
    """(Einstufung, Herkunft, Begruendung) fuer einen aufgeloesten Pfad."""
    if ziel is None:
        return "unklar", "nicht aufloesbar", (
            "Der Pfad entsteht zur Laufzeit oder aus einer Variablen, die "
            "statisch nicht feststeht.")

    if any(p in ziel for p in FREMDPAKETE):
        return "Umgebung", "Fremdpaket", (
            "Die Datei kommt aus einem Fremdpaket. Sie gehoert ins Lock, "
            "nicht in den Snapshot.")

    if "{?}" in ziel:
        return "unklar", "teilweise aufloesbar", (
            "Der Pfad enthaelt einen zur Laufzeit gefuellten Teil.")

    treffer = _finde_im_repo(ziel, wurzel)
    if not treffer:
        return "unklar", "nicht auffindbar", (
            "Der Dateiname steht im Quelltext, aber keine solche Datei liegt "
            "im Repo. Entweder wird sie zur Laufzeit erzeugt (dann ist sie "
            "Zwischenstand, keine Eingabe), oder sie liegt auf dem "
            "Betriebsrechner und hier nicht.")

    if len(treffer) > 1:
        return "unklar", "mehrdeutig (%d Fundorte)" % len(treffer), (
            "Der Basisname passt auf mehrere Dateien im Repo; welche gemeint "
            "ist, entscheidet ein Wurzelpfad, der zur Laufzeit entsteht.")

    rel = treffer[0]
    if rel.startswith("data" + os.sep):
        return "Eingabe", "Repo (Kursdaten)", (
            "Kursdatei - schon heute im Snapshot.")
    if rel.startswith("results" + os.sep) or os.sep + "results" + os.sep in rel:
        return "erzeugt", "Laufergebnis", (
            "Wird vom Lauf selbst geschrieben und danach wieder gelesen - "
            "Zwischenstand, keine Eingabe.")

    v = versioniert(rel, wurzel)
    if v:
        return "Eingabe", "Repo (versioniert): %s" % rel, (
            "Versionierte Nicht-Code-Datei im Repo.")
    return "Eingabe", "Repo (NICHT versioniert): %s" % rel, (
        "⚠️ Gitignoriert oder unverfolgt - sie existiert genau einmal.")


_REPOINDEX = {}


def _finde_im_repo(ziel, wurzel):
    """Alle Dateien im Repo, deren Pfad auf `ziel` endet.

    Gesucht wird ueber den **Basisnamen**, weil der Wurzelteil des Pfades im
    Quelltext oft nicht steht (siehe `_literale`). Mehrere Treffer sind ein
    Ergebnis, kein Fehler - sie werden als **unklar** berichtet.
    """
    if not _REPOINDEX:
        for ordner, unter, dateien in os.walk(wurzel):
            unter[:] = [u for u in unter if u not in AUSGENOMMEN
                        and not u.startswith(".")]
            for d in dateien:
                rel = os.path.relpath(os.path.join(ordner, d), wurzel)
                _REPOINDEX.setdefault(d, []).append(rel)

    basis = os.path.basename(ziel)
    kandidaten = _REPOINDEX.get(basis, [])
    if "/" in ziel or os.sep in ziel:
        genauer = [k for k in kandidaten
                   if k.replace(os.sep, "/").endswith(ziel.replace(os.sep, "/"))]
        if genauer:
            return sorted(genauer)
    return sorted(kandidaten)


# ===========================================================================
# Sammeln und berichten
# ===========================================================================

def lade_selektionsmodule(pfad=TB46_ERHEBUNG):
    """Die 90 aus TB-46. Die Rollenzuordnung wird uebernommen."""
    if not os.path.exists(pfad):
        raise SystemExit(
            "Die TB-46-Erhebung fehlt: %s. Ohne sie ist die Ausgangsmenge "
            "geraten, und das ist hier nicht zulaessig." % pfad)
    with open(pfad, "r", encoding="utf-8") as datei:
        daten = json.load(datei)
    return sorted(k for k, v in daten["module"].items()
                  if v.get("rolle") == SELEKTIONSROLLE)


def sammle(wurzel=_WURZEL):
    start = lade_selektionsmodule()
    funde, gesehen, fehler, importe = huelle(start, wurzel)

    # Je Zieldatei zusammenfassen
    je_datei = {}
    for f in funde:
        schluessel = f.ziel if f.ziel else "(unaufloesbar) %s:%d" % (f.modul,
                                                                     f.zeile)
        eintrag = je_datei.setdefault(schluessel, {
            "ziel": f.ziel, "leser": [], "einstufung": None})
        eintrag["leser"].append("%s:%d (%s)" % (f.modul, f.zeile, f.leser))

    for schluessel, eintrag in je_datei.items():
        stufe, herkunft, grund = einstufen(eintrag["ziel"], wurzel)
        eintrag["einstufung"] = stufe
        eintrag["herkunft"] = herkunft
        eintrag["begruendung"] = grund
        eintrag["leser"] = sorted(set(eintrag["leser"]))

    return {
        "selektionsmodule": len(start),
        "huelle": len(gesehen),
        "module_der_huelle": gesehen,
        "nicht_parsbar": fehler,
        "dateien": je_datei,
        "kalender": kalenderfrage(wurzel, importe),
    }


def kalenderfrage(wurzel, importe):
    """⭐ Kommt der Handelskalender aus einer Datei oder aus einem Paket?

    Das ist die Frage, die der Auftrag ausdruecklich beantwortet haben will -
    denn im zweiten Fall haengt das Ergebnis an einer **Paketfassung**, nicht
    an einer Eingabe, und dann gehoert er ins Lock statt in den Snapshot.
    """
    # 1. In der Huelle der 90 - wird der Kalender vom Selektionslauf ueberhaupt
    #    erreicht?
    in_huelle = []
    for rel, namen in importe.items():
        for n in namen:
            if "market_calendar" in n or "exchange_calendar" in n:
                in_huelle.append({"modul": rel, "import": n})

    # 2. Im ganzen Repo - unabhaengig von der Huelle, denn die Frage ist
    #    ausdruecklich gestellt und wird so oder so beantwortet.
    im_repo = []
    for ordner, unter, dateien in os.walk(wurzel):
        unter[:] = [u for u in unter if u not in AUSGENOMMEN
                    and not u.startswith(".")]
        for d in dateien:
            if not d.endswith(".py"):
                continue
            pfad = os.path.join(ordner, d)
            rel = os.path.relpath(pfad, wurzel)
            try:
                with open(pfad, "r", encoding="utf-8") as datei:
                    baum = ast.parse(datei.read(), filename=pfad)
            except (OSError, SyntaxError):
                continue
            for knoten in ast.walk(baum):
                namen = []
                if isinstance(knoten, ast.Import):
                    namen = [a.name for a in knoten.names]
                elif isinstance(knoten, ast.ImportFrom) and knoten.module:
                    namen = [knoten.module]
                for n in namen:
                    if "market_calendar" in n or "exchange_calendar" in n:
                        im_repo.append({"modul": rel, "import": n,
                                        "zeile": knoten.lineno})

    return {
        "in_selektionshuelle": sorted(in_huelle, key=lambda e: e["modul"]),
        "im_repo": sorted(im_repo, key=lambda e: (e["modul"], e["zeile"])),
        "paket_vorhanden": _paketfassung("pandas_market_calendars"),
    }


def _paketfassung(name):
    try:
        import importlib.metadata as md
        return md.version(name)
    except Exception:                                 # noqa: BLE001
        return None


def berichte(ergebnis):
    print("=" * 78)
    print("TB-47 TEIL 1 - Was gehoert in den Snapshot?")
    print("=" * 78)
    print()
    print("Ausgangsmenge   %d Selektionsmodule (Rolle aus TB-46 uebernommen)"
          % ergebnis["selektionsmodule"])
    print("Transitive Huelle %d Module (die 90 plus alles, was sie "
          "importieren)" % ergebnis["huelle"])
    if ergebnis["nicht_parsbar"]:
        print("⚠️ nicht parsbar: %d" % len(ergebnis["nicht_parsbar"]))
        for rel, grund in sorted(ergebnis["nicht_parsbar"].items()):
            print("     %-55s %s" % (rel, grund))
    print()

    dateien = ergebnis["dateien"]
    print("-" * 78)
    print("%-42s %-10s %s" % ("DATEI", "EINSTUFUNG", "HERKUNFT"))
    print("-" * 78)
    for schluessel in sorted(dateien):
        e = dateien[schluessel]
        print("%-42s %-10s %s" % (schluessel[:42], e["einstufung"],
                                  e["herkunft"]))
        for leser in e["leser"][:4]:
            print("      gelesen von  %s" % leser)
        if len(e["leser"]) > 4:
            print("      ... und %d weitere" % (len(e["leser"]) - 4))
    print("-" * 78)

    import collections
    c = collections.Counter(e["einstufung"] for e in dateien.values())
    print()
    for stufe in ("Eingabe", "Umgebung", "erzeugt", "unklar"):
        print("  %-10s %d" % (stufe, c.get(stufe, 0)))

    print()
    print("=" * 78)
    print("⭐ DER HANDELSKALENDER - Datei oder Paket?")
    print("=" * 78)
    k = ergebnis["kalender"]
    if not k["im_repo"]:
        print("  Kein Kalenderpaket im Repo gefunden - der Kalender kaeme "
              "dann aus einer Datei.")
        return

    print("  AUS EINEM PAKET. Kein Modul dieses Projekts liest einen "
          "Kalender aus")
    print("  einer Datei; er wird zur Laufzeit von "
          "`pandas_market_calendars` gebaut.")
    print()
    print("  Fundstellen im ganzen Repo:")
    for e in k["im_repo"]:
        print("     %-50s Z%-5d %s" % (e["modul"], e["zeile"], e["import"]))
    print()
    print("  Paketfassung hier: %s" % (k["paket_vorhanden"]
                                       or "nicht installiert"))
    print()
    if k["in_selektionshuelle"]:
        print("  ⚠️ Er liegt IN der Huelle der 90 - der Selektionslauf "
              "erreicht ihn.")
        for e in k["in_selektionshuelle"]:
            print("     %-55s %s" % (e["modul"], e["import"]))
    else:
        print("  ⭐ Er liegt NICHT in der Huelle der 90. Der Selektionslauf "
              "erreicht")
        print("     ihn nicht - er haengt am Live-Pfad "
              "(`shared/entscheidungskerze.py`),")
        print("     und der ist Betrieb, nicht Selektion.")
    print()
    print("  ⚠️ EINSTUFUNG: UMGEBUNG, nicht Eingabe. Er gehoert ins Lock, "
          "nicht in")
    print("     den Snapshot - und damit haengt das Ergebnis an einer "
          "PAKETFASSUNG,")
    print("     nicht an einer Eingabedatei. Ein Snapshot kann das nicht "
          "einfangen.")


def main(argv=None) -> int:
    z = argparse.ArgumentParser(
        description="TB-47 Teil 1: welche Nicht-Code-Dateien liest die "
                    "Selektionsseite? (misst, aendert nichts)")
    z.add_argument("--json", metavar="PFAD", default=None)
    a = z.parse_args(argv)

    ergebnis = sammle()
    berichte(ergebnis)

    if a.json:
        pfad = a.json if os.path.isabs(a.json) else os.path.join(_HIER, a.json)
        os.makedirs(os.path.dirname(os.path.abspath(pfad)), exist_ok=True)
        with open(pfad, "w", encoding="utf-8") as datei:
            json.dump(ergebnis, datei, indent=2, ensure_ascii=False,
                      sort_keys=True)
            datei.write("\n")
        print("\nJSON: %s" % pfad)
    return 0


if __name__ == "__main__":
    sys.exit(main())
