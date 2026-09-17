#!/usr/bin/env python3
"""
TB-45, Teil 5: was kommt bei `fromisoformat` im Live-Pfad wirklich an?
==============================================================================
`shared/entscheidungskerze.py` benutzt `dt.datetime.fromisoformat` - in der
Funktion, mit der **alle neun Bots seit dem Umstellungstag (16.09.2026,
04:42:24Z) ihre Entscheidungskerze bestimmen**. Python 3.11 nimmt dort
deutlich mehr Schreibweisen an als Python 3.9, und der Betrieb laeuft auf
3.9.6.

⚠ **Diese Untersuchung MISST und BERICHTET. Sie aendert
`shared/entscheidungskerze.py` nicht.** Eine Aenderung an der
Entscheidungskerze ist eine Aenderung am Live-Pfad aller neun Bots und
braucht eine eigene Freigabe.

Drei Fragen, drei Messungen:

  A  **Was kommt heute an dieser Stelle an?** Nicht geraten, sondern
     mitgeschrieben: `dt.datetime.fromisoformat` wird im Modulnamensraum
     durch einen Mitschreiber ersetzt, und danach laeuft `lade()` fuer
     echte Symbole beider Maerkte - aus `data/` und, wo `data/` veraltet
     ist, ueber den Rueckfallweg.
  B  **Welche Formen wuerden auf 3.9 scheitern und auf 3.11 durchgehen?**
     Derselbe Katalog, beiden Fassungen vorgelegt, Zeile fuer Zeile.
  C  **Was passiert dann?** Abbruch, stiller Rueckfall oder falsche Kerze -
     am Ablauf beobachtet, indem der Mitschreiber genau die Form
     zurueckgibt, die auf 3.9 scheitert.

Nutzung:
    python3 research/fromisoformat_registerfrage/messung.py
    python3 research/fromisoformat_registerfrage/messung.py --json
    python3 research/fromisoformat_registerfrage/messung.py \\
            --zweite-fassung /pfad/zu/python3.9

`--zweite-fassung` nennt einen zweiten Interpreter (auf dem Mac:
`trading-env/bin/python3`). Fehlt er, faellt Messung B auf das aus, was der
laufende Interpreter kann, und sagt das ausdruecklich.
"""

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, os.path.join(BASE_DIR, "shared"))


# ---------------------------------------------------------------------------
# Der Katalog - jede Zeile mit dem Grund, warum sie drinsteht
# ---------------------------------------------------------------------------
KATALOG = [
    ("2026-09-16T00:00:00", "kanonisch - genau das, was der Code heute baut"),
    ("2026-09-16 00:00:00", "Leerzeichen statt T - so fuehren die Kursdateien es"),
    ("2026-09-16T00:00:00.123456", "Mikrosekunden, sechs Stellen"),
    ("2026-09-16T00:00:00.123456789", "NANOsekunden, neun Stellen"),
    ("2026-09-16T00:00:00+00:00", "Offset ausgeschrieben"),
    ("2026-09-16T00:00:00Z", "Z-Suffix - wird im Code VOR dem Aufruf ersetzt"),
    ("20260916T000000", "Grundform ohne Trennzeichen"),
    ("20260916", "nur das Datum, ohne Trennzeichen"),
    ("2026-W38-3", "Wochendatum nach ISO 8601"),
    ("2026-260", "Ordinaldatum (Tag im Jahr)"),
    ("2026-09-16T00:00:00,123", "Dezimalkomma statt Punkt"),
    ("2026-09-16T24:00:00", "24:00 als Tagesende"),
    ("2026-09-16T00:00", "Stunde und Minute, ohne Sekunden"),
    ("2026-09-16", "nur das Datum"),
]


# ===========================================================================
# A  Was kommt heute an?
# ===========================================================================
_MITSCHREIBER = r'''
import datetime as dt, json, os, sys
BASE_DIR = sys.argv[1]
sys.path.insert(0, os.path.join(BASE_DIR, "shared"))
import entscheidungskerze as ek

MITSCHRIFT = []
_echt = dt.datetime.fromisoformat

class _DatetimeErsatz:
    def __init__(self, echt):
        self._echt = echt
    def __getattr__(self, name):
        return getattr(self._echt, name)
    def fromisoformat(self, text):
        MITSCHRIFT.append({"typ": type(text).__name__, "text": str(text)})
        return _echt(text)
    def __call__(self, *a, **k):
        return self._echt(*a, **k)
    def __instancecheck__(self, obj):
        return isinstance(obj, self._echt)

class _ModulErsatz:
    def __init__(self, echt):
        self._echt = echt
        self.datetime = _DatetimeErsatz(echt.datetime)
    def __getattr__(self, name):
        return getattr(self._echt, name)

# NUR im Namensraum von entscheidungskerze - nicht global.
ek.dt = _ModulErsatz(dt)

import pandas as pd
symbole = json.loads(sys.argv[2])
fehler = []
for symbol, intervall, markt in symbole:
    pfad = os.path.join(BASE_DIR, "data", "%s_%s.csv" % (symbol, intervall))
    # Binance und yfinance sind aus der Cloud gesperrt. Der Rueckfallweg
    # soll trotzdem GANZ durchlaufen - sonst endet die Messung genau vor
    # der Stelle, um die es geht. Der Abruf liefert deshalb dieselbe Datei
    # zurueck, die `data/` fuehrt: der WEG ist echt, nur die Gegenstelle
    # nicht. Auf dem Mac laeuft derselbe Aufruf gegen den echten Endpunkt.
    def _abruf(_p=pfad):
        return pd.read_csv(_p, parse_dates=["open_time"])
    try:
        ek.lade(symbol, intervall, markt, abruf=_abruf, melden=False)
    except Exception as e:
        fehler.append({"symbol": symbol, "fehler": "%s: %s" % (type(e).__name__, e)})

print("###" + json.dumps({"mitschrift": MITSCHRIFT, "fehler": fehler}))
'''


def messung_a(symbole):
    """Jeden Wert mitschreiben, der im Live-Pfad bei `fromisoformat` ankommt."""
    lauf = subprocess.run(
        [sys.executable, "-c", _MITSCHREIBER, BASE_DIR, json.dumps(symbole)],
        capture_output=True, text=True, timeout=900, cwd=BASE_DIR)
    for zeile in reversed(lauf.stdout.splitlines()):
        if zeile.startswith("###"):
            return json.loads(zeile[3:])
    return {"mitschrift": None, "fehler": [{"symbol": "<alle>",
            "fehler": (lauf.stdout + lauf.stderr)[-600:]}]}


# ===========================================================================
# B  Welche Formen nimmt welche Fassung?
# ===========================================================================
_KATALOGLAUF = r'''
import datetime as dt, json, sys
erg = {}
for text in json.loads(sys.argv[1]):
    try:
        erg[text] = dt.datetime.fromisoformat(text).isoformat()
    except Exception as e:
        erg[text] = "!" + type(e).__name__
print(json.dumps({"fassung": "%d.%d.%d" % sys.version_info[:3], "erg": erg}))
'''


def messung_b(zweite_fassung):
    formen = [t for t, _g in KATALOG]
    ergebnisse = {}
    for pfad in [sys.executable] + ([zweite_fassung] if zweite_fassung else []):
        lauf = subprocess.run([pfad, "-c", _KATALOGLAUF, json.dumps(formen)],
                              capture_output=True, text=True, timeout=120)
        if lauf.returncode != 0:
            ergebnisse[pfad] = {"fassung": "<lief nicht>",
                                "erg": {}, "meldung": lauf.stderr[-200:]}
            continue
        ergebnisse[pfad] = json.loads(lauf.stdout.strip().splitlines()[-1])
    return ergebnisse


# ===========================================================================
# C  Was passiert, wenn die Form auf 3.9 scheitert?
# ===========================================================================
_FOLGENLAUF = r'''
import datetime as dt, json, os, sys
BASE_DIR, form = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(BASE_DIR, "shared"))
import entscheidungskerze as ek

# Die Form, die auf 3.9 scheitert, wird DORT eingespeist, wo der Code heute
# `f"{tag}T00:00:00"` baut: `letzter_handelstag` liefert den Tag. Damit
# laeuft der echte Weg, nur mit einer Schreibweise, die 3.9 nicht kennt.
ek.letzter_handelstag = lambda startzeit, kalender=None: (form, None)

erg = {"form": form}

# Zusaetzlich: auf 3.9 wuerde `fromisoformat` bei dieser Form werfen. Das
# wird hier nachgestellt, damit die FOLGE auch auf 3.11 sichtbar wird.
_echt = dt.datetime.fromisoformat
class _DatetimeErsatz:
    def __init__(self, echt):
        self._echt = echt
    def __getattr__(self, name):
        return getattr(self._echt, name)
    def fromisoformat(self, text):
        if text.startswith(form):
            raise ValueError("Invalid isoformat string: %r (nachgestelltes 3.9)" % text)
        return _echt(text)
    def __call__(self, *a, **k):
        return self._echt(*a, **k)
class _ModulErsatz:
    def __init__(self, echt):
        self._echt = echt
        self.datetime = _DatetimeErsatz(echt.datetime)
    def __getattr__(self, name):
        return getattr(self._echt, name)
ek.dt = _ModulErsatz(dt)

import pandas as pd
pfad = os.path.join(BASE_DIR, "data", "AAPL_1d.csv")
df = pd.read_csv(pfad, parse_dates=["open_time"])
try:
    gefiltert, verworfen, hinweis = ek.nur_entscheidbar(
        df, "1d", ek.AKTIEN, symbol="AAPL", melden=False)
    erg["ausgang"] = "durchgelaufen"
    erg["zeilen_vorher"] = len(df)
    erg["zeilen_nachher"] = len(gefiltert)
    erg["verworfen"] = int(verworfen)
    erg["hinweis"] = str(hinweis)[:200]
except Exception as e:
    erg["ausgang"] = "%s: %s" % (type(e).__name__, str(e)[:160])

# Und eine Ebene hoeher: was sieht der BOT? `lade()` ist die Tuer, durch die
# alle neun gehen. Faengt sie den Fehler ab, oder kommt er beim Bot an?
try:
    ek.lade("AAPL", "1d", ek.AKTIEN,
            abruf=lambda: pd.read_csv(pfad, parse_dates=["open_time"]),
            melden=False)
    erg["lade_ausgang"] = "durchgelaufen"
except Exception as e:
    erg["lade_ausgang"] = "%s: %s" % (type(e).__name__, str(e)[:120])

# Und fuer Krypto - derselbe Lauf, derselbe kaputte Tag.
try:
    ek.lade("BTCUSDT", "1h", ek.KRYPTO,
            abruf=lambda: pd.read_csv(
                os.path.join(BASE_DIR, "data", "BTCUSDT_1h.csv"),
                parse_dates=["open_time"]),
            melden=False)
    erg["lade_krypto"] = "durchgelaufen"
except Exception as e:
    erg["lade_krypto"] = "%s: %s" % (type(e).__name__, str(e)[:120])

print("###" + json.dumps(erg, default=str))
'''


def messung_c(form):
    lauf = subprocess.run(
        [sys.executable, "-c", _FOLGENLAUF, BASE_DIR, form],
        capture_output=True, text=True, timeout=600, cwd=BASE_DIR)
    for zeile in reversed(lauf.stdout.splitlines()):
        if zeile.startswith("###"):
            return json.loads(zeile[3:])
    return {"form": form, "ausgang": (lauf.stdout + lauf.stderr)[-500:]}


_BOTLAUF = r"""
import datetime as dt, json, os, runpy, sys, tempfile
BASE_DIR, form = sys.argv[1], sys.argv[2]
botdir = os.path.join(BASE_DIR, "strategies", "elliott_wave_stocks")
os.chdir(botdir)
sys.path.insert(0, os.path.join(BASE_DIR, "shared"))
sys.path.insert(0, botdir)
import pandas as pd

tmp = tempfile.mkdtemp(prefix="tb45_teil5_")
import strategy_paths
_echt_pfade = strategy_paths.get_strategy_paths
def _wegwerf(caller_file):
    p = dict(_echt_pfade(caller_file))
    p.update({"RESULTS_DIR": tmp, "LOGS_DIR": tmp,
              "DB_FILE": os.path.join(tmp, "probe.db")})
    return p
strategy_paths.get_strategy_paths = _wegwerf

import stocks_symbols_config
stocks_symbols_config.SYMBOLS = ["AAPL", "MSFT", "IBM"]

import entscheidungskerze as ek
ek.melde = lambda *a, **k: None
ek.letzter_handelstag = lambda startzeit, kalender=None: (form, None)
_echt = dt.datetime.fromisoformat
class _DatetimeErsatz:
    def __init__(self, echt):
        self._echt = echt
    def __getattr__(self, name):
        return getattr(self._echt, name)
    def fromisoformat(self, text):
        if text.startswith(form):
            raise ValueError("Invalid isoformat string: %r (nachgestelltes 3.9)" % text)
        return _echt(text)
    def __call__(self, *a, **k):
        return self._echt(*a, **k)
class _ModulErsatz:
    def __init__(self, echt):
        self._echt = echt
        self.datetime = _DatetimeErsatz(echt.datetime)
    def __getattr__(self, name):
        return getattr(self._echt, name)
ek.dt = _ModulErsatz(dt)

_alt = ek.lade
def _lade(symbol, intervall, markt, abruf=None, **k):
    pfad = os.path.join(BASE_DIR, "data", "%s_%s.csv" % (symbol, intervall))
    return _alt(symbol, intervall, markt,
                abruf=lambda: pd.read_csv(pfad, parse_dates=["open_time"]), **k)
ek.lade = _lade

import io as _io, contextlib
gemerkt = _io.StringIO()
ausgang = "durchgelaufen"
try:
    with contextlib.redirect_stdout(gemerkt):
        runpy.run_path(os.path.join(botdir, "forward_test.py"), run_name="__main__")
except SystemExit:
    pass
except Exception as e:
    ausgang = "%s: %s" % (type(e).__name__, str(e)[:120])
text = gemerkt.getvalue()
print("###" + json.dumps({
    "ausgang": ausgang,
    "fehlerzeilen": [z.strip() for z in text.splitlines() if "Fehler bei" in z],
    "geladene_zeile": [z.strip() for z in text.splitlines()
                       if "Offene Papier-Positionen" in z],
}))
"""


def messung_c_bot(form):
    """Und was sieht der BOT? Die Registerfrage haingt genau daran."""
    lauf = subprocess.run([sys.executable, "-c", _BOTLAUF, BASE_DIR, form],
                          capture_output=True, text=True, timeout=900,
                          cwd=BASE_DIR)
    for zeile in reversed(lauf.stdout.splitlines()):
        if zeile.startswith("###"):
            return json.loads(zeile[3:])
    return {"ausgang": (lauf.stdout + lauf.stderr)[-500:], "fehlerzeilen": [],
            "geladene_zeile": []}


# ===========================================================================
# D  Nebenbefund aus TB-44: os.fstat in system/test_log_rotation.py
# ===========================================================================
_FSTATLAUF = r"""
import importlib, json, os, sys
treffer = []
for modulname in ("pathlib", "io", "tempfile", "shutil", "os", "zipfile",
                  "tarfile", "gzip", "mmap", "socket", "subprocess"):
    try:
        modul = importlib.import_module(modulname)
    except Exception:
        continue
    for name, wert in list(vars(modul).items()):
        if not isinstance(wert, type):
            continue
        for kname, kwert in list(vars(wert).items()):
            if kwert is os.fstat:
                treffer.append(modulname + "." + name + "." + kname)
print(json.dumps({"fassung": "%d.%d.%d" % sys.version_info[:3],
                  "fstat_typ": type(os.fstat).__name__,
                  "klassenruempfe": sorted(treffer)}))
"""


def _fassungen(zusaetzlich=None):
    """Jeder Python-Interpreter, der auf diesem Rechner liegt."""
    import glob
    pfade = {sys.executable}
    for muster in ("/usr/bin/python3.*", "/usr/local/bin/python3.*",
                   os.path.expanduser("~/.local/share/uv/python/*/bin/python3.*")):
        for p in glob.glob(muster):
            if os.path.isfile(p) and not p.endswith("-config"):
                pfade.add(p)
    if zusaetzlich:
        pfade.add(zusaetzlich)
    return sorted(pfade)


def messung_d(zweite_fassung=None):
    """Ist der Deskriptor-Ersatz von `os.fstat` stabil?

    Der Kern des TB-44-Befundes: eine C-Funktion ist KEIN Deskriptor, eine
    Python-Funktion schon. Steht sie in einem Klassenrumpf, wird sie zur
    gebundenen Methode - und die Argumente verrutschen. Genau das war bei
    `pathlib._NormalAccessor.open` der Fall, und zwar NUR auf 3.9 und 3.10.
    "Stabil" heisst hier deshalb nicht "auf meinem Rechner harmlos", sondern
    "auf JEDER Fassung, die auf diesem Rechner liegt, harmlos" - dieselbe
    Frage, dieselbe Methode wie Teil L des Trockenlaufs.
    """
    ergebnisse = []
    for pfad in _fassungen(zweite_fassung):
        lauf = subprocess.run([pfad, "-c", _FSTATLAUF],
                              capture_output=True, text=True, timeout=120)
        if lauf.returncode != 0:
            ergebnisse.append({"pfad": pfad, "fassung": "<lief nicht>",
                               "klassenruempfe": [], "fstat_typ": "?"})
            continue
        e = json.loads(lauf.stdout.strip().splitlines()[-1])
        e["pfad"] = pfad
        ergebnisse.append(e)
    return ergebnisse


# ===========================================================================
def main():
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[1])
    p.add_argument("--json", action="store_true")
    p.add_argument("--zweite-fassung", default=None,
                   help="Pfad zu einem zweiten Interpreter (Mac: "
                        "trading-env/bin/python3)")
    args = p.parse_args()

    symbole = [("AAPL", "1d", "aktien"), ("MSFT", "1d", "aktien"),
               ("BTCUSDT", "1h", "krypto"), ("BTCUSDT", "4h", "krypto"),
               ("ETHUSDT", "1d", "krypto")]

    bericht = {
        "gemessen_am": dt.datetime.utcnow().isoformat(timespec="seconds"),
        "laufende_fassung": "%d.%d.%d" % sys.version_info[:3],
        "A_was_ankommt": messung_a(symbole),
        "B_katalog": messung_b(args.zweite_fassung),
        "C_folge": [messung_c(f) for f in ("2026-W38-3", "20260916")],
        "C_bot": messung_c_bot("2026-W38-3"),
        "D_fstat": messung_d(args.zweite_fassung),
    }

    if args.json:
        print(json.dumps(bericht, indent=1, ensure_ascii=False))
        return 0

    print("=" * 78)
    print("TB-45, Teil 5: fromisoformat im Live-Pfad - gemessen")
    print("=" * 78)
    print(f"Laufender Interpreter: Python {bericht['laufende_fassung']}")

    print("\nA) Was heute an dieser Stelle ankommt")
    a = bericht["A_was_ankommt"]
    if a["mitschrift"] is None:
        print("   Die Messung lief nicht:", a["fehler"])
    elif not a["mitschrift"]:
        print("   KEIN EINZIGER Aufruf - `fromisoformat` wurde in diesen "
              "Laeufen gar nicht erreicht.")
    else:
        gesehen = {}
        for e in a["mitschrift"]:
            gesehen[(e["typ"], e["text"])] = gesehen.get((e["typ"], e["text"]), 0) + 1
        print(f"   {len(a['mitschrift'])} Aufruf(e), "
              f"{len(gesehen)} verschiedene Werte:")
        for (typ, text), n in sorted(gesehen.items()):
            print(f"     {n:4d}x  {typ:<6}  {text!r}")
    for f in a["fehler"]:
        print(f"   Hinweis {f['symbol']}: {f['fehler'][:160]}")

    print("\nB) Der Katalog, je Fassung")
    fassungen = list(bericht["B_katalog"].items())
    kopf = "   %-32s %-52s" % ("Form", "Grund")
    print(kopf)
    for text, grund in KATALOG:
        zeile = "   %-32s %-52s" % (repr(text), grund)
        for _pfad, e in fassungen:
            wert = e["erg"].get(text, "?")
            zeile += " | %s %s" % (e["fassung"],
                                   "SCHEITERT" if str(wert).startswith("!") else "ok")
        print(zeile)
    if len(fassungen) < 2:
        print("   ⚠ Nur EINE Fassung gemessen - `--zweite-fassung` nicht "
              "angegeben. Die 3.9-Spalte holt der Mac-Testauftrag nach.")

    print("\nC) Was geschieht, wenn die Form auf 3.9 scheitert")
    for c in bericht["C_folge"]:
        print(f"   {c['form']!r}")
        print(f"      nur_entscheidbar(): {c['ausgang']}")
        if c.get("zeilen_vorher") is not None:
            print(f"      {c['zeilen_vorher']} Zeilen hinein, "
                  f"{c.get('zeilen_nachher')} heraus, "
                  f"{c.get('verworfen')} verworfen")
        print(f"      lade() Aktien:     {c.get('lade_ausgang')}")
        print(f"      lade() Krypto:     {c.get('lade_krypto')}")
    cb = bericht["C_bot"]
    print(f"   Und der Bot (elliott_wave_stocks, 3 Symbole): {cb['ausgang']}")
    print(f"      {len(cb['fehlerzeilen'])} Fehlerzeile(n), je Symbol eine")
    for z in cb["fehlerzeilen"][:2]:
        print(f"        {z[:110]}")
    for z in cb["geladene_zeile"]:
        print(f"      {z}")

    print("\nD) Nebenbefund: os.fstat im Klassenrumpf - je Fassung")
    for d in bericht["D_fstat"]:
        print(f"   Python {d['fassung']:<9} os.fstat ist ein {d['fstat_typ']:<28} "
              f"Klassenruempfe: {d['klassenruempfe'] or 'keiner'}")
    print("\n" + "=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
