#!/usr/bin/env python3
"""
Wie erreichen die Module `data/`? (TB-46, Teil 1)
==============================================================================
TB-34 hat gezaehlt, **wer** `data/` liest: 101 Module. Diese Erhebung stellt
die andere Frage, die vor jedem Umbau zu beantworten ist:

    Sprechen die Module den Ordner **einzeln** an, oder gehen sie durch
    **eine gemeinsame Stelle**?

Denn davon haengt alles ab. Geht der Zugriff durch eine gemeinsame Stelle,
kostet ein Schnitt die Aenderung dieser einen Stelle. Baut jedes Modul den
Pfad selbst, kostet er hundert Aenderungen - und jede einzelne kann
vergessen werden, ohne dass es auffaellt.

Was gemessen wird, und was ausdruecklich nicht
------------------------------------------------------------------------------
Gesucht wird ueber den **Syntaxbaum**, nicht mit Textsuche: `data/` in einem
Kommentar oder in einer Meldung ist kein Zugriff. Genau daran haette eine
Textsuche sich verzaehlt - die neun `forward_test.py` nennen `data/` in
Kommentaren und in einer Protokollzeile und fassen den Ordner selbst nie an.

Fuenf Merkmale je Fundstelle (die Spalten des Auftrags):

  **Schreibweise**   wie der Pfad entsteht - Literal, Konstante, Parameter,
                     Umgebungsvariable. Sie entscheidet, ob eine Aenderung an
                     einer Stelle durchschlaegt.
  **Weg**            `zentral` (der Pfad kommt aus einem `shared/`-Modul),
                     `selbst` (das Modul baut ihn aus einem Literal),
                     `mittelbar` (ueber den Trichter `load_all_symbol_data`),
                     `nachgebaut` (ein eigenes `data` unter einem Temp-Ordner -
                     das ist KEIN Zugriff auf den echten Bestand).
  **Leser/Schreiber** Schreiber sind die Abrufskripte. Sie gehoeren zwingend
                     auf den Live-Bestand, nie auf den Snapshot.
  **Rolle**          Betrieb - Selektion/Backtest - Untersuchung -
                     Pruefwerkzeug. Nur die Selektionsseite soll auf den
                     Snapshot zeigen.
  **Dateimuster**    ⚠️ Es ist `AAPL_1d.csv`, nicht `AAPL.csv`.

Die Wurzelfrage: echter Bestand oder nachgebauter?
------------------------------------------------------------------------------
Ein Selbsttest, der sich unter `tempfile.mkdtemp()` ein `data` anlegt, liest
nicht den Bestand des Projekts. Wer das zusammenzaehlt, bekommt eine Zahl,
die den Umbau teurer aussehen laesst, als er ist. Die Erhebung trennt
deshalb nach der **Wurzel** des Pfadausdrucks: eine Wurzel, die auf das
Projektverzeichnis zeigt (`BASE_DIR`, `dirname(...)`, `_WURZEL`), gilt als
echt; eine, die auf einen Temp- oder Parameterordner zeigt (`tmp`, `wurzel`,
`arbeit`, `ziel`), als nachgebaut.

⚠️ Diese Unterscheidung ist eine **Heuristik am Namen** und als solche
angegeben. Sie ist nachpruefbar: jede Fundstelle steht mit Datei, Zeile und
Quelltextausschnitt im JSON.

Die Erhebung aendert nichts. Sie fasst `data/` nicht an, importiert keine
Bot-Datei und braucht nur die Standardbibliothek.

    python3 research/datenordner_schnitt/erhebung.py
    python3 research/datenordner_schnitt/erhebung.py --json ergebnisse/erhebung.json

Rueckgabewert 0, wenn gemessen wurde; **1, wenn nicht gemessen werden
konnte** (kein Modul gefunden, Wurzel unlesbar). Ein leeres Ergebnis ist
hier kein Erfolg - das ist die Lehre aus TB-45.
"""

import argparse
import ast
import json
import os
import re
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))

# Die Ordner, die zum Projekt gehoeren. `trading-env/` ist ausgenommen - sonst
# zaehlt die Erhebung 1312 Dateien der Fremdpakete mit.
ORDNER = ["shared", "strategies", "research", "dashboard", "notifications",
          "broker", "system", "config", "docs"]
AUSGENOMMEN = ("trading-env", "__pycache__", ".git", "node_modules",
               "datenordner_schnitt")   # das Messwerkzeug selbst

# ⚠️ In TB-46 neu hinzugekommen. Sie erreichen `data/` wirklich und werden
# deshalb NICHT stillschweigend uebergangen - aber sie gehoeren nicht zu dem
# Bestand, den der spaetere Umbau vorfindet. Die Erhebung nennt beide Zahlen.
NEU_IN_TB46 = ("shared/snapshot.py", "shared/test_snapshot.py")

# ---------------------------------------------------------------------------
# Die gemeinsamen Stellen: wo im Projekt der Pfad auf `data/` einmal steht
# und von anderen uebernommen wird. Ermittelt in dieser Erhebung, nicht
# geraten - jeder Eintrag ist eine Stelle, die den Pfad selbst baut UND ihn
# nach draussen gibt.
# ---------------------------------------------------------------------------
ZENTRALE_STELLEN = {
    "shared/paths.py": ["DATA_DIR"],
    "shared/strategy_paths.py": ["DATA_DIR"],
    "shared/entscheidungskerze.py": ["STANDARD_DATENORDNER"],
    "shared/kursdaten.py": ["standard"],
    "shared/abrufschutz.py": ["standard"],
    "shared/zeitabdeckung.py": ["standard"],
    "research/vorregistrierung/herkunft.py": ["daten_dir"],
}

# Namen, deren Vorkommen im Pfadausdruck bedeutet: der Pfad kommt aus einer
# gemeinsamen Stelle, nicht aus einem Literal dieses Moduls.
ZENTRALE_NAMEN = {"DATA_DIR", "STANDARD_DATENORDNER"}

# Funktionen, die ihrerseits `data/` lesen. Wer sie aufruft, rechnet auf dem
# Bestand, auch ohne eigenes `read_csv`.
ZENTRALE_AUFRUFE = {
    "load_all_symbol_data": "Trichter der Backtest-/Optimiererseite",
    "lade": "shared/entscheidungskerze.lade - der Weg der neun Bots",
    "datenstand": "herkunft.datenstand - der Datenstand-Hash",
    "pruefe_ordner": "shared/kursdaten.pruefe_ordner",
}

# Module, die die zentralen Aufrufe bereitstellen - bei ihnen ist der Aufruf
# die Definition, nicht die Benutzung.
DEFINIEREN_AUFRUFE = {
    "shared/entscheidungskerze.py", "shared/kursdaten.py",
    "research/vorregistrierung/herkunft.py",
}

# Wurzelnamen, die auf einen nachgebauten Ordner zeigen (Selbsttests).
NACHGEBAUT_MARKER = ("tmp", "temp", "wurzel", "arbeit", "ziel", "mkdtemp",
                     "verzeichnis", "sandkasten", "spiel", "attrappe")
# Wurzelnamen, die auf das Projektverzeichnis zeigen.
ECHT_MARKER = ("BASE_DIR", "_WURZEL", "WURZEL", "_HIER", "BASIS", "PROJEKT",
               "base_dir", "_SHARED", "SHARED_DIR", "_BASE")

SCHREIB_AUFRUFE = {"to_csv", "write", "writelines", "writerow", "writerows"}
SCHREIB_FUNKTIONEN = {"remove", "unlink", "rename", "replace", "rmtree",
                      "copy", "copy2", "copyfile", "move", "makedirs", "mkdir"}
LESE_AUFRUFE = {"read_csv", "listdir", "glob", "scandir", "walk", "read_json"}


# ===========================================================================
# Teil 1 - Die Fundstellen eines Moduls
# ===========================================================================

def _zeilen(text):
    """Die Zeilen einer Datei als UTF-8-Bytes.

    Bytes, nicht Zeichen: `col_offset` des Syntaxbaums zaehlt UTF-8-Bytes.
    Bei einer Datei mit Umlauten oder Warnzeichen schneidet eine
    Zeichenzaehlung an der falschen Stelle - und faellt nicht auf, weil das
    Ergebnis immer noch wie Quelltext aussieht.
    """
    return [z.encode("utf-8") for z in text.splitlines()]


def _quelle(knoten, zeilen):
    """Der Quelltextausschnitt eines Knotens.

    Nicht `ast.get_source_segment`: das zerlegt bei JEDEM Aufruf die ganze
    Datei in Zeilen. Ueber 429 Module mit zehntausenden Knoten wird die
    Erhebung dadurch minutenlang - gemessen, nicht vermutet.
    """
    von = getattr(knoten, "lineno", None)
    bis = getattr(knoten, "end_lineno", None)
    if von is None or bis is None or von < 1 or bis > len(zeilen):
        return ""
    if von == bis:
        stueck = zeilen[von - 1][knoten.col_offset:knoten.end_col_offset]
    else:
        teile = [zeilen[von - 1][knoten.col_offset:]]
        teile += zeilen[von:bis - 1]
        teile.append(zeilen[bis - 1][:knoten.end_col_offset])
        stueck = b"\n".join(teile)
    return stueck.decode("utf-8", "replace")


_BEZEICHNER = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
# Ausdruecke, die einen Pfad zusammensetzen. Nur solche geben einen
# Kursdatenpfad weiter - ein `read_csv` gibt einen DataFrame weiter.
_PFADBAU = ("os.path.join", "os.path.abspath", "os.path.realpath",
            "os.path.dirname", "Path(", "os.fspath", "%s", ".format(",
            "os.sep", "glob(", "iglob(")


def _bezeichner(ausdruck):
    """Die Bezeichner in einem Quelltextausschnitt."""
    return set(_BEZEICHNER.findall(ausdruck))


def _baut_pfad(ausdruck):
    """Setzt dieser Ausdruck einen Pfad zusammen?"""
    if any(m in ausdruck for m in _PFADBAU):
        return True
    # f"{DATA_DIR}/..." - Zeichenkette mit eingesetztem Namen
    return ausdruck.startswith("f\"") or ausdruck.startswith("f'")


def _ist_data_literal(wert):
    """Zeigt dieses Zeichenkettenliteral auf den Kursdatenordner?"""
    if not isinstance(wert, str):
        return None
    w = wert.replace("\\", "/")
    if w in ("data", "data/", "./data", "./data/"):
        return "literal_name"
    if w.startswith("data/") or w.startswith("./data/"):
        return "literal_pfad"
    if w.endswith("/data") or "/data/" in w:
        return "literal_pfad"
    return None


def _wurzel_art(ausdruck):
    """echt | nachgebaut | unklar - nach den Namen im Pfadausdruck.

    Heuristik am Namen, ausdruecklich als solche. Nachgebaut gewinnt: ein
    `os.path.join(tmp, "data")` ist auch dann nachgebaut, wenn `BASE_DIR`
    weiter oben in derselben Zeile steht.
    """
    if any(m in ausdruck for m in NACHGEBAUT_MARKER):
        return "nachgebaut"
    if any(m in ausdruck for m in ECHT_MARKER):
        return "echt"
    return "unklar"


def _schreibweise(knoten, eltern_quelle, art, in_fstring=False):
    """Wie entsteht der Pfad an dieser Stelle - und entsteht ueberhaupt einer?

    ⚠️ Der wichtigste Unterschied dieser Erhebung. Ein Modul kann `data/`
    **nennen**, ohne einen Pfad dorthin zu bauen:

        _prot.ohne_kursrahmen(symbol, "data/ und Live-Abruf")   # eine Meldung
        BEOBACHTET = ("strategies/", "data/", ...)              # ein git-Filter
        shutil.ignore_patterns("data", ".git", ...)             # ein Ausschluss

    Diese Stellen lesen und schreiben nichts. Wer sie mitzaehlt, bekommt eine
    zu hohe Zahl - und zwar an der empfindlichsten Stelle: **zwei der neun
    `forward_test.py` nennen `data/` in einer Meldung.** Eine Erhebung, die
    das als Zugriff zaehlt, wuerde melden, der Umbau muesse die Bot-Dateien
    anfassen, die er nicht anfassen darf.
    """
    if "environ" in eltern_quelle or "getenv" in eltern_quelle:
        return "Umgebungsvariable"
    if "os.path.join" in eltern_quelle:
        return "os.path.join + Literal"
    if "Path(" in eltern_quelle:
        return "pathlib + Literal"
    if in_fstring and art == "literal_pfad":
        # `f"{R}/data/{s}_1d.csv"` - ein gebauter Pfad, auch ohne os.path.
        return "f-Zeichenkette mit Pfad"
    if art == "literal_pfad" and knoten.value.endswith(".csv"):
        return "Literal mit vollem Pfad"
    return "Nennung ohne Pfadbau"


def untersuche(pfad, rel):
    """Ein Modul -> seine Fundstellen zum Kursdatenordner."""
    with open(pfad, "r", encoding="utf-8") as datei:
        text = datei.read()
    zeilen = _zeilen(text)
    try:
        baum = ast.parse(text)
    except SyntaxError as fehler:
        return {"fehler": f"nicht parsbar: {fehler}"}

    fundstellen = []
    muster = set()
    # Namen, die in diesem Modul einen Kursdatenpfad tragen.
    daten_namen = set()

    # --- Durchgang 1: Literale, die den Ordner nennen -------------------
    # Das Elternknoten-Verhaeltnis wird vorher eingetragen, damit die
    # Schreibweise am umgebenden Ausdruck erkennbar ist.
    eltern = {}
    for knoten in ast.walk(baum):
        for kind in ast.iter_child_nodes(knoten):
            eltern[kind] = knoten

    for knoten in ast.walk(baum):
        if not (isinstance(knoten, ast.Constant) and isinstance(knoten.value, str)):
            continue
        art = _ist_data_literal(knoten.value)
        if not art:
            continue
        # Der umgebende Ausdruck: bis zu drei Ebenen hoch, damit
        # `os.path.join(BASE_DIR, "data")` vollstaendig sichtbar wird.
        oben, hoch, in_fstring = knoten, 0, False
        while hoch < 3 and eltern.get(oben) is not None:
            oben = eltern[oben]
            hoch += 1
            if isinstance(oben, ast.JoinedStr):
                in_fstring = True
            if isinstance(oben, (ast.Assign, ast.Call, ast.arg, ast.Return)):
                break
        q = _quelle(oben, zeilen)
        sw = _schreibweise(knoten, q, art, in_fstring)
        fundstellen.append({
            "zeile": knoten.lineno,
            "weg": "selbst",
            "schreibweise": sw,
            "pfadbau": sw != "Nennung ohne Pfadbau",
            "wurzel": _wurzel_art(q),
            "quelle": q.replace("\n", " ")[:160],
        })
        # Nur ein gebauter Pfad wird weitergegeben. Ein git-Filter `"data/"`
        # traegt keinen Pfad, und die Variable daneben auch nicht.
        if isinstance(oben, ast.Assign) and sw != "Nennung ohne Pfadbau":
            for ziel in oben.targets:
                if isinstance(ziel, ast.Name):
                    daten_namen.add(ziel.id)

    # --- Durchgang 2: uebernommene Namen aus gemeinsamen Stellen ---------
    for knoten in ast.walk(baum):
        # `from paths import DATA_DIR`, `P["DATA_DIR"]`, `paths.DATA_DIR`
        treffer = None
        if isinstance(knoten, ast.ImportFrom):
            for a in knoten.names:
                if a.name in ZENTRALE_NAMEN:
                    treffer = a.name
        elif isinstance(knoten, ast.Attribute) and knoten.attr in ZENTRALE_NAMEN:
            treffer = knoten.attr
        elif isinstance(knoten, ast.Subscript):
            q = _quelle(knoten, zeilen)
            for name in ZENTRALE_NAMEN:
                if f'"{name}"' in q or f"'{name}'" in q:
                    treffer = name
        if not treffer:
            continue
        if rel in ZENTRALE_STELLEN:
            continue                      # hier wird sie definiert, nicht geholt
        fundstellen.append({
            "zeile": knoten.lineno,
            "weg": "zentral",
            "schreibweise": f"Konstante {treffer} aus shared/",
            "pfadbau": True,
            "wurzel": "echt",
            "quelle": _quelle(knoten, zeilen).replace("\n", " ")[:160],
        })
        daten_namen.add(treffer)

    # Zuweisungen, die einen Kursdatenpfad weitergeben. Zwei Bedingungen,
    # beide notwendig:
    #   1. die rechte Seite baut einen PFAD (`os.path.join`, `pathlib`, ...)
    #   2. sie benutzt dabei einen Namen, der schon einen Pfad traegt
    # ⚠️ Ohne Bedingung 1 wandert `df = pd.read_csv(os.path.join(DATA_DIR,
    # ...))` in die Liste, und danach gilt jedes `to_csv` als Schreiben nach
    # `data/`. Genau so entstanden im ersten Lauf 19 Schreiber statt 9.
    # Verglichen wird ueber BEZEICHNER, nicht ueber Teilzeichenketten:
    # `"P" in "output_path"` ist wahr und bedeutet nichts.
    for _runde in range(3):                 # Ketten ueber mehrere Zuweisungen
        vorher = len(daten_namen)
        for knoten in ast.walk(baum):
            if not isinstance(knoten, ast.Assign):
                continue
            rechts = _quelle(knoten.value, zeilen)
            if not _baut_pfad(rechts):
                continue
            bezeichner = _bezeichner(rechts)
            if not (bezeichner & (ZENTRALE_NAMEN | daten_namen)):
                continue
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Name):
                    daten_namen.add(ziel.id)
        if len(daten_namen) == vorher:
            break

    # --- Durchgang 3: mittelbare Wege ueber zentrale Aufrufe -------------
    for knoten in ast.walk(baum):
        if isinstance(knoten, (ast.Import, ast.ImportFrom)):
            namen = ([a.name for a in knoten.names]
                     if isinstance(knoten, ast.Import)
                     else [a.name for a in knoten.names])
            for name in namen:
                if name in ZENTRALE_AUFRUFE and rel not in DEFINIEREN_AUFRUFE:
                    fundstellen.append({
                        "zeile": knoten.lineno,
                        "weg": "mittelbar",
                        "schreibweise": f"import {name}()",
                        "pfadbau": True,
                        "wurzel": "echt",
                        "quelle": ZENTRALE_AUFRUFE[name],
                    })
        if isinstance(knoten, ast.Call):
            name = (knoten.func.attr if isinstance(knoten.func, ast.Attribute)
                    else getattr(knoten.func, "id", ""))
            if name in ZENTRALE_AUFRUFE and rel not in DEFINIEREN_AUFRUFE:
                q = _quelle(knoten, zeilen).replace("\n", " ")
                # `lade` ist ein haeufiges Wort; nur der Aufruf ueber das
                # Modul oder mit Marktargument zaehlt.
                if name == "lade" and "entscheidungskerze" not in q:
                    continue
                fundstellen.append({
                    "zeile": knoten.lineno,
                    "weg": "mittelbar",
                    "schreibweise": f"Aufruf {name}()",
                    "pfadbau": True,
                    "wurzel": "echt",
                    "quelle": q[:160],
                })

    # --- Durchgang 4: Leser oder Schreiber, und die Dateimuster ---------
    liest, schreibt = [], []
    for knoten in ast.walk(baum):
        if not isinstance(knoten, ast.Call):
            continue
        name = (knoten.func.attr if isinstance(knoten.func, ast.Attribute)
                else getattr(knoten.func, "id", ""))
        argumente = [_quelle(a, zeilen) for a in knoten.args]
        alle = " ".join(argumente)
        betrifft = (bool(_bezeichner(alle) & (daten_namen | ZENTRALE_NAMEN))
                    or any(_ist_data_literal(a.strip("\"'")) for a in argumente))
        if not betrifft:
            continue
        if name in LESE_AUFRUFE or (name == "open" and "w" not in alle
                                    and "a" not in alle):
            liest.append(f"Zeile {knoten.lineno}: {name}({alle[:60]})")
        if name in SCHREIB_AUFRUFE or name in SCHREIB_FUNKTIONEN:
            schreibt.append(f"Zeile {knoten.lineno}: {name}({alle[:60]})")
        if name == "open" and ("\"w" in alle or "'w" in alle
                               or "\"a" in alle or "'a" in alle):
            schreibt.append(f"Zeile {knoten.lineno}: open(..., schreibend)")

    # Dateimuster: jedes Literal, das nach einer Kursdatei aussieht.
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Constant) and isinstance(knoten.value, str):
            w = knoten.value
            if w.endswith(".csv") and len(w) < 60:
                muster.add(w)
        if isinstance(knoten, ast.JoinedStr):
            q = _quelle(knoten, zeilen)
            if ".csv" in q and len(q) < 80:
                muster.add(q.strip())

    if not fundstellen:
        return None
    return {
        "fundstellen": fundstellen,
        "liest": liest,
        "schreibt": schreibt,
        "dateimuster": sorted(muster),
        "fehler": None,
    }


# ===========================================================================
# Teil 2 - Rolle je Modul
# ===========================================================================

def rolle(rel):
    """Betrieb | Selektion/Backtest | Untersuchung | Pruefwerkzeug"""
    name = os.path.basename(rel)
    erster = rel.split(os.sep)[0]
    if name.startswith("test_") or name.endswith("_test.py"):
        if name == "forward_test.py":
            return "Betrieb"
        return "Pruefwerkzeug"
    if erster == "research":
        return "Untersuchung"
    if erster == "strategies":
        if name in ("forward_test.py",) or name.startswith("fetch_") \
                or name.startswith("get_top"):
            return "Betrieb"
        return "Selektion/Backtest"
    if erster in ("dashboard", "notifications", "broker", "system", "config"):
        return "Betrieb"
    if erster == "shared":
        if name.startswith("fetch_") or name in (
                "entscheidungskerze.py", "abrufschutz.py", "paths.py",
                "strategy_paths.py", "kursdaten.py", "get_top_symbols.py",
                "zeitabdeckung.py", "kursdaten_neuaufbau.py",
                "binance_historie.py", "boersenkalender.py"):
            return "Betrieb"
        return "Pruefwerkzeug"
    return "unklar"


# ===========================================================================
# Teil 3 - Sammeln und berichten
# ===========================================================================

def sammle(wurzel=_WURZEL, ordner=None):
    befunde = {}
    nicht_parsbar = []
    for teil in (ordner or ORDNER):
        oben = os.path.join(wurzel, teil)
        if not os.path.isdir(oben):
            continue
        for pfad, unter, dateien in os.walk(oben):
            unter[:] = [u for u in unter if u not in AUSGENOMMEN]
            if any(a in pfad for a in AUSGENOMMEN):
                continue
            for name in sorted(dateien):
                if not name.endswith(".py"):
                    continue
                voll = os.path.join(pfad, name)
                rel = os.path.relpath(voll, wurzel)
                ergebnis = untersuche(voll, rel)
                if ergebnis is None:
                    continue
                if ergebnis.get("fehler"):
                    nicht_parsbar.append(rel)
                    continue
                ergebnis["rolle"] = rolle(rel)
                ergebnis["wege"] = sorted({f["weg"] for f in ergebnis["fundstellen"]})
                ergebnis["wurzeln"] = sorted({f["wurzel"]
                                              for f in ergebnis["fundstellen"]})
                ergebnis["schreibweisen"] = sorted(
                    {f["schreibweise"] for f in ergebnis["fundstellen"]})
                # Ein Modul zaehlt als Zugriff auf den ECHTEN Bestand, wenn
                # mindestens eine Fundstelle nicht nachgebaut ist.
                ergebnis["echter_bestand"] = any(
                    f["wurzel"] != "nachgebaut" for f in ergebnis["fundstellen"])
                befunde[rel] = ergebnis
    return befunde, nicht_parsbar


def summen(befunde):
    echte = {k: v for k, v in befunde.items() if v["echter_bestand"]}
    nur_nachgebaut = {k: v for k, v in befunde.items() if not v["echter_bestand"]}
    neu = sorted(k for k in echte if k in NEU_IN_TB46)

    je_schreibweise, je_rolle, je_weg = {}, {}, {}
    for rel, v in echte.items():
        for s in v["schreibweisen"]:
            je_schreibweise.setdefault(s, []).append(rel)
        je_rolle.setdefault(v["rolle"], []).append(rel)
        for w in v["wege"]:
            je_weg.setdefault(w, []).append(rel)

    # Die Frage des Auftrags: selbst gebaut oder zentral bezogen?
    # Gezaehlt wird am PFADBAU, nicht an der Nennung: ein Modul, das `data/`
    # nur in einem git-Filter oder einer Meldung nennt, baut keinen Pfad und
    # muss bei einem Schnitt auch nicht angefasst werden.
    def baut_selbst(v):
        return any(f["weg"] == "selbst" and f.get("pfadbau")
                   and f["wurzel"] != "nachgebaut" for f in v["fundstellen"])

    def nur_nennung(v):
        return (not baut_selbst(v)
                and any(f["weg"] == "selbst" and not f.get("pfadbau")
                        for f in v["fundstellen"]))

    selbst = sorted(k for k, v in echte.items() if baut_selbst(v))
    selbst_ohne_neu = [k for k in selbst if k not in NEU_IN_TB46]
    nur_zentral = sorted(k for k, v in echte.items()
                         if not baut_selbst(v) and not nur_nennung(v))
    nennung = sorted(k for k, v in echte.items() if nur_nennung(v))
    schreiber = sorted(k for k, v in echte.items() if v["schreibt"])

    # --- Was jeder Entwurf kostet, in Modulen -----------------------------
    # Entwurf A benennt `data/` in `data/live/` um. Jede Stelle, die den Pfad
    # SELBST baut, zeigt danach auf einen leeren Ordner. Module, die ihn aus
    # einer gemeinsamen Stelle beziehen, sind nicht betroffen.
    # Entwurf B laesst `data/` stehen. Die Live-Seite kostet dann NICHTS; zu
    # verdrahten ist nur die Selektionsseite - und die kostet in beiden
    # Entwuerfen dasselbe.
    selektionsseite = sorted(k for k, v in echte.items()
                             if v["rolle"] == "Selektion/Backtest")
    bot_dateien = sorted(k for k in echte
                         if os.path.basename(k) in ("forward_test.py",
                                                    "live_params.py",
                                                    "equity_simulation.py"))
    bot_mit_pfadbau = sorted(k for k in bot_dateien if baut_selbst(echte[k]))
    entwuerfe = {
        "A_umbenennen": {
            "module_mit_eigenem_pfadbau": len(selbst),
            "davon_zentrale_stellen": sorted(k for k in selbst
                                             if k in ZENTRALE_STELLEN),
            "nennungen_die_irrefuehrend_werden": len(nennung),
        },
        "B_geschwisterordner": {
            "module_mit_eigenem_pfadbau": 0,
            "nennungen_die_irrefuehrend_werden": 0,
        },
        "beide": {
            "selektionsseite_zu_verdrahten": len(selektionsseite),
            "schreiber_muessen_live_bleiben": len(schreiber),
        },
        "bot_dateien_mit_fundstelle": bot_dateien,
        "bot_dateien_mit_eigenem_pfadbau": bot_mit_pfadbau,
    }

    return {
        "module_echter_bestand": len(echte),
        "module_echter_bestand_ohne_tb46": len(echte) - len(neu),
        "neu_in_tb46": neu,
        "module_nur_nachgebaut": len(nur_nachgebaut),
        "je_schreibweise": {k: len(v) for k, v in sorted(je_schreibweise.items())},
        "je_rolle": {k: len(v) for k, v in sorted(je_rolle.items())},
        "je_weg": {k: len(v) for k, v in sorted(je_weg.items())},
        "bauen_selbst": selbst,
        "bauen_selbst_ohne_tb46": selbst_ohne_neu,
        "beziehen_zentral": nur_zentral,
        "nur_nennung": nennung,
        "schreiber": schreiber,
        "entwuerfe": entwuerfe,
        "selektionsseite": selektionsseite,
        "listen": {"je_schreibweise": je_schreibweise, "je_rolle": je_rolle,
                   "je_weg": je_weg,
                   "nur_nachgebaut": sorted(nur_nachgebaut)},
    }


def berichte(befunde, s, nicht_parsbar):
    print("=" * 78)
    print("TB-46 TEIL 1 - WIE erreichen die Module den Kursdatenordner?")
    print("=" * 78)

    print(f"\nGemessen: {len(befunde)} Module mit mindestens einer Fundstelle.")
    print(f"  davon auf dem ECHTEN Bestand   {s['module_echter_bestand']:>3}")
    print(f"  ⚠️ davon neu in TB-46           {len(s['neu_in_tb46']):>3}"
          f"   {list(s['neu_in_tb46'])}")
    print(f"  = Bestand VOR TB-46            "
          f"{s['module_echter_bestand_ohne_tb46']:>3}"
          "   (die Zahl, die der Umbau vorfindet)")
    print(f"  davon nur nachgebautes data/   {s['module_nur_nachgebaut']:>3}"
          "   (Selbsttests unter Temp-Ordnern)")
    if nicht_parsbar:
        print(f"  ⚠️ nicht parsbar: {len(nicht_parsbar)} - {nicht_parsbar}")

    print("\n1. DIE FRAGE DES AUFTRAGS: selbst gebaut oder zentral bezogen?")
    print(f"   bauen den Pfad selbst (Literal im Modul)   "
          f"{len(s['bauen_selbst']):>3} Module"
          f"   davon vor TB-46: {len(s['bauen_selbst_ohne_tb46'])}")
    print(f"   beziehen ihn ausschliesslich mittelbar     "
          f"{len(s['beziehen_zentral']):>3} Module")
    print(f"   nennen data/ nur, ohne Pfad zu bauen       "
          f"{len(s['nur_nennung']):>3} Module   (git-Filter, Meldungen)")

    print("\n2. SUMMEN JE SCHREIBWEISE (Module, Mehrfachnennung moeglich)")
    for k, v in s["je_schreibweise"].items():
        print(f"   {k:<34} {v:>3}")

    print("\n3. SUMMEN JE ROLLE")
    for k, v in s["je_rolle"].items():
        print(f"   {k:<34} {v:>3}")

    print("\n4. SUMMEN JE WEG")
    for k, v in s["je_weg"].items():
        print(f"   {k:<34} {v:>3}")

    print(f"\n5. SCHREIBER ({len(s['schreiber'])}) - sie gehoeren auf den "
          f"Live-Bestand, nie auf den Snapshot")
    for rel in s["schreiber"]:
        print(f"   {rel}")

    print("\n6. DIE MODULE, DIE DEN PFAD SELBST BAUEN - Datei, Zeile, "
          "Schreibweise")
    for rel in s["bauen_selbst"]:
        v = befunde[rel]
        eigen = [f for f in v["fundstellen"] if f["weg"] == "selbst"
                 and f["wurzel"] != "nachgebaut"]
        if not eigen:
            continue
        print(f"   {rel}  [{v['rolle']}]")
        for f in eigen[:4]:
            print(f"        Zeile {f['zeile']:>5}  {f['schreibweise']:<26} "
                  f"{f['quelle'][:60]}")
        if len(eigen) > 4:
            print(f"        ... und {len(eigen) - 4} weitere Stelle(n)")

    print("\n7. DIE DATEIMUSTER - es ist `AAPL_1d.csv`, nicht `AAPL.csv`")
    alle = {}
    for v in befunde.values():
        for m in v["dateimuster"]:
            alle[m] = alle.get(m, 0) + 1
    for m, n in sorted(alle.items(), key=lambda p: -p[1])[:14]:
        print(f"   {n:>3}x  {m}")

    e = s["entwuerfe"]
    print("\n8. WAS JEDER ENTWURF KOSTET - in Modulen, aus den Fundstellen")
    print(f"   Entwurf A (data/ -> data/live/):")
    print(f"      Module mit eigenem Pfadbau, die umgestellt werden muessen  "
          f"{len(s['bauen_selbst_ohne_tb46']):>3}   (ohne die zwei aus TB-46)")
    print(f"      davon gemeinsame Stellen in shared/ bzw. research/         "
          f"{len(e['A_umbenennen']['davon_zentrale_stellen']):>3}  "
          f"{e['A_umbenennen']['davon_zentrale_stellen']}")
    print(f"      Nennungen, die danach irrefuehrend dastehen                "
          f"{e['A_umbenennen']['nennungen_die_irrefuehrend_werden']:>3}")
    print(f"   Entwurf B (data/ bleibt, snapshots/ daneben):")
    print(f"      Module mit eigenem Pfadbau, die umgestellt werden muessen  "
          f"{e['B_geschwisterordner']['module_mit_eigenem_pfadbau']:>3}")
    print(f"   Beide Entwuerfe gleich:")
    print(f"      Selektionsseite, die auf den Snapshot zu zeigen hat        "
          f"{e['beide']['selektionsseite_zu_verdrahten']:>3}")
    print(f"      Schreiber, die auf dem Live-Bestand bleiben muessen        "
          f"{e['beide']['schreiber_muessen_live_bleiben']:>3}")
    print("\n9. DIE UNANTASTBAREN BOT-DATEIEN (Regel 1 des Auftrags)")
    print(f"   forward_test.py / live_params.py / equity_simulation.py mit")
    print(f"   irgendeiner Fundstelle:      {len(e['bot_dateien_mit_fundstelle'])}")
    for k in e["bot_dateien_mit_fundstelle"]:
        print(f"      {k}")
    print(f"   davon mit eigenem PFADBAU:   "
          f"{len(e['bot_dateien_mit_eigenem_pfadbau'])}"
          f"   {e['bot_dateien_mit_eigenem_pfadbau'] or '- keine'}")

    print("\n" + "=" * 78)


def main(argv=None) -> int:
    z = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    z.add_argument("--wurzel", default=_WURZEL)
    z.add_argument("--json", default=None)
    a = z.parse_args(argv)

    if not os.path.isdir(a.wurzel):
        print(f"NICHT MESSBAR: {a.wurzel} ist kein Verzeichnis.",
              file=sys.stderr)
        return 1

    befunde, nicht_parsbar = sammle(a.wurzel)
    if not befunde:
        # Die Lehre aus TB-45: ein leeres Ergebnis ist kein gruener Ausgang.
        print("NICHT MESSBAR: kein einziges Modul mit Fundstelle gefunden. "
              "Das ist ein Fehler der Erhebung, kein Befund ueber das Repo.",
              file=sys.stderr)
        return 1

    s = summen(befunde)
    berichte(befunde, s, nicht_parsbar)

    if a.json:
        ziel = (a.json if os.path.isabs(a.json) else os.path.join(_HIER, a.json))
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump({"summen": s, "module": befunde,
                       "nicht_parsbar": nicht_parsbar},
                      datei, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"JSON: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
