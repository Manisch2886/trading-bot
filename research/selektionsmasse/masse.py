#!/usr/bin/env python3
"""
Die Messwerkzeuge hinter den zwei Selektionsmassen (TB-52, Teil 2)
==============================================================================
Hier steht, **wie** gemessen wird. Die beiden Masse selbst - mit ihren
Ausgangszahlen - stehen daneben in `test_wanduhr.py` und
`test_eigener_pfadbau.py`.

⚠️⚠️ **Gemessen wird am Syntaxbaum, NICHT mit Textsuche** (Prueffrage B5).
*In TB-46 nennen zwei `forward_test.py` den Datenordner in einer
Protokollzeile - eine Textsuche haette gemeldet, der Umbau muesse genau die
Dateien anfassen, die er nicht anfassen darf.*

⚠️ **Dieses Modul aendert nichts.** Es liest Quelltext und zaehlt.

**Woher die 90 Selektionsmodule kommen:** aus
`research/datenordner_schnitt/ergebnisse/erhebung.json`, Rolle
`Selektion/Backtest`. ⚠️ Die Liste wird **nicht** hier noch einmal gefuehrt -
eine zweite Fassung derselben Liste ist in diesem Projekt schon einmal
unbemerkt auseinandergelaufen. Fehlt die Erhebung, ist das Ergebnis
**NICHT PRUEFBAR** (Prueffrage A2), nicht gruen.
"""

import ast
import json
import os

_HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(_HIER))

ERHEBUNG = os.path.join(WURZEL, "research", "datenordner_schnitt",
                        "ergebnisse", "erhebung.json")
SELEKTIONSROLLE = "Selektion/Backtest"

# ⚠️ **Zwei** zentrale Pfadquellen, und nur EINE davon ist der Resolver:
#
#   `shared/paths.py`          - traegt seit TB-52 den Selektionsmodus
#   `shared/strategy_paths.py` - ⚠️ leitet `DATA_DIR` SELBST ab
#                                (`os.path.join(base_dir, "data")`) und
#                                beruehrt `paths.py` nie
#
# ⭐ **Das ist der Befund, den dieses Mass sichtbar macht:** ein Modul, das
# seinen Datenpfad aus `strategy_paths` zieht, geht an `paths.py` vorbei -
# und damit am Selektionsmodus. Es ist zentral versorgt und trotzdem
# ausserhalb des Resolvers.
RESOLVER_MODUL = "shared/paths.py"
ZWEITE_QUELLE = "shared/strategy_paths.py"
# ⚠️ **Alle** Namen, die aus `paths.py` oder `strategy_paths.py` stammen -
# nicht nur die Datennamen. Das Mass fragt: "baut das Modul einen Pfad
# ausserhalb des Resolvers?" `RESULTS_DIR`, `LOGS_DIR` und `DB_FILE` kommen
# aus `strategy_paths.get_strategy_paths()`, also **aus** dem Resolver.
# ⚠️ Im ersten Entwurf fehlten sie hier - das Mass zaehlte daraufhin **127**
# statt 0 Treffer, fast alle davon gewoehnliche Ergebnisdateien
# (`os.path.join(RESULTS_DIR, "equity_curve.csv")`). Eine Zahl, die man
# ungeprueft festgeschrieben haette, waere die Ausgangszahl fuer TB-53
# gewesen.
ZENTRALE_NAMEN = ("DATA_DIR", "CONFIG_DIR", "LIVE_DATA_DIR",
                  "LIVE_CONFIG_DIR", "get_strategy_paths", "BASE_DIR",
                  "RESULTS_DIR", "LOGS_DIR", "DB_FILE", "SHARED_DIR",
                  "STRATEGY_NAME")

# Bekannte Kursdatei-Endungen.
KURSENDUNGEN = (".csv", ".parquet", ".feather", ".h5", ".pkl")

# ---------------------------------------------------------------------------
# Mass 1: die Wanduhren. ⚠️ Die Liste aus dem Auftrag, plus was uns beim
# Messen sonst begegnet ist und dieselbe Wirkung hat.
# ---------------------------------------------------------------------------
WANDUHREN = (
    # aus dem Auftrag
    "datetime.now", "datetime.utcnow", "date.today", "time.time",
    "Timestamp.now", "Timestamp.today", "time.localtime", "time.gmtime",
    # ⭐ zusaetzlich gefunden - dieselbe Wirkung, nicht auf der Auftragsliste:
    "datetime.today",        # wie date.today, aber mit Uhrzeit
    "Timestamp.utcnow",      # pandas-Gegenstueck zu datetime.utcnow
    "date.fromtimestamp",    # time.time() ueber einen Umweg
    "datetime.fromtimestamp",
    "os.path.getmtime",      # Frischepruefung ueber den Dateizeitstempel
    "os.path.getctime",
    "time.time_ns",
    "time.monotonic",        # kein Kalenderdatum, aber laufzeitabhaengig
)
# `numpy.datetime64("now")` / `pd.Timestamp("now"|"today")` sind Aufrufe mit
# einem verraeterischen Argument statt eines verraeterischen Namens - sie
# werden eigens erkannt (siehe `_zeitargument`).
ZEITARGUMENTE = ("now", "today", "NOW", "TODAY")
ZEITTYPEN = ("datetime64", "Timestamp", "to_datetime")


class Fund(object):
    """Ein Treffer: Datei, Zeile, was gefunden wurde, wozu es dient."""

    def __init__(self, datei, zeile, was, verwendung, quelltext):
        self.datei = datei
        self.zeile = zeile
        self.was = was
        self.verwendung = verwendung
        self.quelltext = quelltext

    def als_dict(self):
        return {"datei": self.datei, "zeile": self.zeile, "was": self.was,
                "verwendung": self.verwendung, "quelltext": self.quelltext}

    def __repr__(self):
        return "%s:%d %s (%s)" % (self.datei, self.zeile, self.was,
                                  self.verwendung)


def selektionsmodule():
    """Die 90 - oder (None, Grund), wenn die Erhebung fehlt."""
    if not os.path.exists(ERHEBUNG):
        return None, "%s fehlt" % os.path.relpath(ERHEBUNG, WURZEL)
    try:
        with open(ERHEBUNG, encoding="utf-8") as datei:
            erhebung = json.load(datei)
    except (OSError, ValueError) as fehler:
        return None, "%s nicht lesbar: %s" % (ERHEBUNG, fehler)
    module = sorted(k for k, v in erhebung.get("module", {}).items()
                    if v.get("rolle") == SELEKTIONSROLLE)
    if not module:
        return None, "kein Modul mit der Rolle %r in der Erhebung" \
            % SELEKTIONSROLLE
    return module, None


def _punktname(knoten):
    """`a.b.c` als Zeichenkette - oder None."""
    teile = []
    while isinstance(knoten, ast.Attribute):
        teile.append(knoten.attr)
        knoten = knoten.value
    if isinstance(knoten, ast.Name):
        teile.append(knoten.id)
    elif isinstance(knoten, ast.Call):
        return None
    else:
        return None
    return ".".join(reversed(teile))


def _passt_wanduhr(name):
    """Auf das ENDE des Punktnamens pruefen.

    ⚠️ So faellt `dt.datetime.now`, `datetime.datetime.now` und
    `pd.Timestamp.now` gleichermassen auf - eine Namensliste, die auf den
    vollen Punktnamen prueft, haette an jedem Alias vorbeigesehen.
    """
    for muster in WANDUHREN:
        if name == muster or name.endswith("." + muster):
            return muster
    return None


def _zeitargument(knoten):
    """`np.datetime64("now")`, `pd.Timestamp("today")` und Verwandte."""
    if not isinstance(knoten, ast.Call) or not knoten.args:
        return None
    name = _punktname(knoten.func) or ""
    letzter = name.rsplit(".", 1)[-1]
    if letzter not in ZEITTYPEN:
        return None
    erstes = knoten.args[0]
    if isinstance(erstes, ast.Constant) and erstes.value in ZEITARGUMENTE:
        return "%s(%r)" % (letzter, erstes.value)
    return None


def _elternkarte(baum):
    karte = {}
    for eltern in ast.walk(baum):
        for kind in ast.iter_child_nodes(eltern):
            karte[kind] = eltern
    return karte


_PROTOKOLLZIELE = ("print", "write", "info", "debug", "warning", "error",
                   "critical", "log", "exception", "echo")


def _verwendung(knoten, karte):
    """Wozu der Wert benutzt wird - die Unterscheidung, die zaehlt.

    ⭐ *Eine Wanduhr in einer Protokollzeile ist harmlos; eine im Datenschnitt
    entwertet den Lauf.* **Der Test unterscheidet das nicht - der Bericht muss
    es**, also liefert diese Funktion die Einstufung mit.

    ⚠️ Im Zweifel `zu pruefen`, nie `nur Protokollzeile`. Eine Einstufung, die
    im Zweifel entwarnt, macht aus einem Befund ein Schweigen.
    """
    aktuell = knoten
    tiefe = 0
    schnitt = False
    while aktuell in karte and tiefe < 12:
        eltern = karte[aktuell]
        tiefe += 1
        if isinstance(eltern, ast.Call):
            ziel = (_punktname(eltern.func) or "").rsplit(".", 1)[-1]
            if ziel in _PROTOKOLLZIELE:
                return "nur Protokollzeile"
            if ziel in ("strftime", "isoformat", "timedelta"):
                aktuell = eltern
                continue
        # Vergleich, Schnitt oder Auswahl: der Wert steuert, WELCHE Daten
        # weiterverwendet werden.
        if isinstance(eltern, (ast.Compare, ast.Subscript, ast.Slice)):
            schnitt = True
        if isinstance(eltern, (ast.FunctionDef, ast.Module,
                               ast.AsyncFunctionDef)):
            break
        aktuell = eltern
    if schnitt:
        return "Datenschnitt / Frischepruefung"
    return "zu pruefen (von Hand ansehen)"


def lies(pfad):
    """(Baum, Quelltextzeilen) - oder (None, Grund)."""
    try:
        with open(pfad, encoding="utf-8") as datei:
            text = datei.read()
    except OSError as fehler:
        return None, "nicht lesbar: %s" % fehler
    try:
        return (ast.parse(text), text.splitlines()), None
    except SyntaxError as fehler:
        # Prueffrage A2: nicht parsbar ist nicht "kein Treffer".
        return None, "nicht parsbar: %s" % fehler


def _zeile(zeilen, nummer):
    if 0 < nummer <= len(zeilen):
        return zeilen[nummer - 1].strip()[:120]
    return ""


# ===========================================================================
# Mass 1 - keine Wanduhr im Selektionspfad
# ===========================================================================

def wanduhren(pfad, anzeige):
    baum_und_zeilen, grund = lies(pfad)
    if baum_und_zeilen is None:
        return [], grund
    baum, zeilen = baum_und_zeilen
    karte = _elternkarte(baum)
    funde = []
    for knoten in ast.walk(baum):
        was = None
        if isinstance(knoten, ast.Call):
            name = _punktname(knoten.func)
            if name:
                treffer = _passt_wanduhr(name)
                if treffer:
                    was = name + "()"
            if was is None:
                was = _zeitargument(knoten)
        elif isinstance(knoten, ast.Attribute):
            # Auch die ungerufene Referenz zaehlt: `f = datetime.now` und
            # spaeter `f()` ist dieselbe Wanduhr, nur eine Zeile weiter.
            eltern = karte.get(knoten)
            if not isinstance(eltern, ast.Call) or eltern.func is not knoten:
                name = _punktname(knoten)
                if name and _passt_wanduhr(name):
                    was = name + " (Referenz)"
        if was:
            funde.append(Fund(anzeige, knoten.lineno, was,
                              _verwendung(knoten, karte),
                              _zeile(zeilen, knoten.lineno)))
    return funde, None


# ===========================================================================
# Mass 2 - kein eigener Datenpfad
# ===========================================================================

def _zeigt_auf_daten(text):
    if not isinstance(text, str):
        return False
    schlank = text.strip()
    if schlank in ("data", "data/", "./data", "../data") \
            or schlank.startswith("data/") or schlank.endswith("/data") \
            or "/data/" in schlank:
        return True
    return any(schlank.endswith(e) for e in KURSENDUNGEN)


def _konstanten(knoten):
    """Alle Zeichenketten-Konstanten unterhalb eines Knotens."""
    for unter in ast.walk(knoten):
        if isinstance(unter, ast.Constant) and isinstance(unter.value, str):
            yield unter.value


def _geht_ueber_resolver(knoten):
    """Steht irgendwo in diesem Ausdruck ein Resolver-Name?"""
    for unter in ast.walk(knoten):
        if isinstance(unter, ast.Name) and unter.id in ZENTRALE_NAMEN:
            return True
        if isinstance(unter, ast.Attribute) and unter.attr in ZENTRALE_NAMEN:
            return True
        if isinstance(unter, ast.Subscript):
            for k in _konstanten(unter.slice):
                if k in ZENTRALE_NAMEN:
                    return True
    return False


def _ist_pfadbau(knoten):
    """Ist dieser Knoten ein Pfadbau-Konstrukt? Dann: welcher Art.

    Die drei Arten stehen so im Auftrag: `os.path.join(...)`, f-String,
    `Path(...)`. ⭐ **Dazu** die %-Formatierung - sie ist derselbe Bau mit
    aelterer Schreibweise, und dieses Projekt benutzt sie durchgehend. Eine
    Liste, die sie auslaesst, haette ein Loch genau dort, wo der meiste
    Quelltext liegt.
    """
    if isinstance(knoten, ast.Call):
        name = (_punktname(knoten.func) or "")
        letzter = name.rsplit(".", 1)[-1]
        if name.endswith("os.path.join") or letzter == "join":
            return "os.path.join(...)"
        if letzter in ("Path", "PosixPath", "WindowsPath"):
            return "Path(...)"
    elif isinstance(knoten, ast.JoinedStr):
        return "f-String"
    elif isinstance(knoten, ast.BinOp) and isinstance(knoten.op, ast.Mod):
        return "%-Formatierung"
    return None


# Funktionen, die eine Zeichenkette als Datei oeffnen. Eine **blanke**
# Konstante darin ist ebenfalls ein eigener Pfad - sie wird nur nicht
# "gebaut", sondern steht schon fertig da.
_DATEIFUNKTIONEN = ("open", "read_csv", "read_parquet", "to_csv", "glob",
                    "iglob", "read_table", "load", "savetxt")


def pfadbau(pfad, anzeige):
    """Pfadbau, der auf Daten zeigt und NICHT ueber den Resolver geht.

    ⚠️ Gezaehlt wird nur der **aeusserste** Ausdruck. Sonst faellt
    `os.path.join(DATA_DIR, f"{symbol}_1d.csv")` doppelt auf: einmal als
    Verbund (der ueber den Resolver geht und richtigerweise durchfaellt) und
    einmal als der f-String darin - der fuer sich genommen keinen Resolver
    sieht. **Der innere Teil eines Ausdrucks, dessen Wurzel ueber den
    Resolver geht, ist kein eigener Pfadbau.**
    """
    baum_und_zeilen, grund = lies(pfad)
    if baum_und_zeilen is None:
        return [], grund
    baum, zeilen = baum_und_zeilen
    karte = _elternkarte(baum)

    def hat_pfadbau_ueber_sich(knoten):
        eltern = karte.get(knoten)
        while eltern is not None:
            if _ist_pfadbau(eltern) is not None:
                return True
            eltern = karte.get(eltern)
        return False

    funde = []
    for knoten in ast.walk(baum):
        art = _ist_pfadbau(knoten)
        if art is not None:
            if hat_pfadbau_ueber_sich(knoten):
                continue            # der aeussere Ausdruck entscheidet
            if not any(_zeigt_auf_daten(k) for k in _konstanten(knoten)):
                continue
            if _geht_ueber_resolver(knoten):
                continue
        elif isinstance(knoten, ast.Call):
            # Der zweite Fall: eine blanke Konstante in einer Dateifunktion.
            letzter = (_punktname(knoten.func) or "").rsplit(".", 1)[-1]
            if letzter not in _DATEIFUNKTIONEN or not knoten.args:
                continue
            erstes = knoten.args[0]
            if not (isinstance(erstes, ast.Constant)
                    and _zeigt_auf_daten(erstes.value)):
                continue
            art = "blanke Konstante in %s()" % letzter
        elif (isinstance(knoten, ast.Subscript)
              and isinstance(knoten.slice, ast.Constant)
              and knoten.slice.value in ("DATA_DIR", "CONFIG_DIR")):
            # ⭐ Der dritte Fall, und heute der einzige, der vorkommt: der
            # Datenpfad wird aus `strategy_paths` gezogen. Zentral versorgt -
            # aber an `shared/paths.py` und damit am Selektionsmodus vorbei.
            art = "Datenpfad aus %s" % ZWEITE_QUELLE
        else:
            continue
        funde.append(Fund(anzeige, knoten.lineno, art,
                          _verwendung(knoten, karte),
                          _zeile(zeilen, knoten.lineno)))
    return funde, None


# ===========================================================================
# Die Sperrklinke
# ===========================================================================

def messen(messfunktion):
    """(funde, unlesbar, module) ueber die 90 - oder (None, grund, None)."""
    module, grund = selektionsmodule()
    if module is None:
        return None, grund, None
    funde = []
    unlesbar = []
    for anzeige in module:
        pfad = os.path.join(WURZEL, anzeige)
        if not os.path.exists(pfad):
            unlesbar.append((anzeige, "Datei fehlt"))
            continue
        teil, grund = messfunktion(pfad, anzeige)
        if grund:
            unlesbar.append((anzeige, grund))
        funde.extend(teil)
    return funde, unlesbar, module


def berichte(titel, funde, unlesbar, module, ausgangszahl, erlaeuterung,
             json_ziel=None):
    """Die Ausgabe. ⚠️ Immer mit Liste - eine Zahl ohne Liste ist kein Mass."""
    print("=" * 78)
    print(titel)
    print("=" * 78)
    if funde is None:
        print("NICHT PRUEFBAR: %s" % unlesbar)
        print("⚠️ Das ist weder gruen noch rot (Prueffrage A2).")
        return 2
    print(erlaeuterung)
    print()
    print("Selektionsmodule geprueft : %d" % len(module))
    print("Ausgangszahl (festgeschrieben) : %d" % ausgangszahl)
    print("Heutiger Stand                 : %d" % len(funde))
    print()
    if unlesbar:
        print("⚠️ NICHT gemessen (%d) - das ist kein 'kein Treffer':"
              % len(unlesbar))
        for anzeige, grund in unlesbar:
            print("   %s: %s" % (anzeige, grund))
        print()
    if funde:
        print("Treffer, je mit Datei, Zeile und Verwendung:")
        breite = max(len(f.datei) for f in funde)
        for f in sorted(funde, key=lambda x: (x.datei, x.zeile)):
            print("   %-*s :%-5d %-28s %s"
                  % (breite, f.datei, f.zeile, f.was, f.verwendung))
            print("   %s| %s" % (" " * (breite + 8), f.quelltext))
    else:
        print("Keine Treffer.")
    print()
    nach_verwendung = {}
    for f in funde:
        nach_verwendung[f.verwendung] = nach_verwendung.get(f.verwendung, 0) + 1
    if nach_verwendung:
        print("Nach Verwendung:")
        for k in sorted(nach_verwendung):
            print("   %-32s %d" % (k, nach_verwendung[k]))
        print()

    if json_ziel:
        ziel = json_ziel if os.path.isabs(json_ziel) \
            else os.path.join(_HIER, json_ziel)
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump({"ausgangszahl": ausgangszahl,
                       "stand": len(funde),
                       "module_geprueft": len(module),
                       "nicht_gemessen": [{"modul": m, "grund": g}
                                          for m, g in unlesbar],
                       "treffer": [f.als_dict() for f in funde]},
                      datei, indent=2, ensure_ascii=False, sort_keys=True)
            datei.write("\n")

    if unlesbar:
        print("ERGEBNIS: NICHT PRUEFBAR - %d Modul(e) liessen sich nicht "
              "messen." % len(unlesbar))
        return 2
    if len(funde) > ausgangszahl:
        print("ERGEBNIS: ⚠️ ROT - %d Treffer, die Ausgangszahl ist %d. "
              "Es ist einer dazugekommen."
              % (len(funde), ausgangszahl))
        return 1
    if len(funde) < ausgangszahl:
        print("ERGEBNIS: GRUEN - %d von %d. ⭐ Die Ausgangszahl ist zu hoch "
              "geworden; sie gehoert im selben Commit mitgesenkt."
              % (len(funde), ausgangszahl))
        return 0
    print("ERGEBNIS: GRUEN - %d, genau die Ausgangszahl. Nichts dazugekommen."
          % len(funde))
    return 0
