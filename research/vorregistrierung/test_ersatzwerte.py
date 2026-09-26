#!/usr/bin/env python3
"""
TB-106 - Rueckfall (d): stille Ersatzwerte in faltenplan.py, benchmark.py,
auswertung.py und der Datenpfad in herkunft.py
==============================================================================
Geprueft wird je Stelle aus dem Auftrag TB-106 (Block A, Fable 24b A2, 25a
Rang 3, 25c 1 und 2 (a), 4 (4)(b)):

  P   Die Probe: der Zweig wird erreicht und der Prozess endet mit 2
      (`paths.RUECKGABEWERT_STARTPRUEFUNG`), die Meldung auf stderr nennt die
      Stelle.
  M   Die Mutationsprobe: in einer Kopie des Ordners steht an GENAU dieser
      Stelle wieder der alte Ersatzwert - dann ist P rot. Jede Mutation
      beisst allein (24b B3): die anderen Stellen bleiben unveraendert.
  M-G Die Gegenprobe (Register 40.7): dieselbe Mutationsprobe OHNE die
      Mutation muss scheitern.

Gerechnet wird immer in einem EIGENEN Prozess auf einer Kopie des Ordners -
nie im laufenden Prozess an einer umgebogenen Variablen (Kopf von
test_vorregistrierung.py, Falle 1).

Die Proben zu `herkunft.py` (E) laufen in einem Wegwerfbaum (Git-Repo mit
einem Commit, echte `paths.py`, Snapshot-Attrappe): `PROTOKOLL` haengt an
`_HIER`, und das echte `ergebnisse/herkunft_protokoll.jsonl` darf keine Probe
beschreiben. Am Ende prueft die Datei, dass es unberuehrt ist.

TB-111 (Fable 25d (2)/(3)) - Teil F, ebenfalls im Wegwerfbaum:
  F-a  die Pruefansicht (`herkunft.py`, `--json`) laeuft unter dem Modus mit
       rc 0 und hasht den Snapshot (`paths.DATA_DIR`), am echten Snapshot
       `d9449faf...`/223;
  F-b  Modus + `TB30A_BASE_DIR` endet mit 2 - Pruefansicht, `commit()`,
       `register()`, `block()` -, die Meldung nennt die Variable, und ein
       Lesehaken sieht keinen Zugriff unter der Ersatzwurzel;
  F-c  ohne Modus wirkt `TB30A_BASE_DIR` wie vorher;
  F-aM, F-bM, F-bM2  Mutationsproben mit Gegenprobe.

TB-111 (Fable 25d (4), Ergaenzung zu 36.5) - Teil G: `auswertung.Abbruch`
endet mit 2 statt 1, die Meldung steht weiter auf stderr - an leeren
Rohergebnissen (Aufruf wie im Betrieb) und an drei der zwoelf Stellen
(fehlende Spalte, Zelle ausserhalb des Rasters, zu wenige gemeinsame Tage);
G-M ist die Mutationsprobe "Code 1 zurueck" mit Gegenprobe.

TB-114 (Fable 26a R3/R5 (c), Register 45) - Teil H:
  H-a  B1: fuer jeden Eintrag von `EINGEFROREN` liefern
       `herkunft._eingefroren_pfad` und `sperrlistensonde._aufloesen`
       denselben absoluten Pfad (eine Pfadregel; die Sonde wird von
       herkunft.py nicht importiert) - im laufenden Prozess (H-a) und im
       Wegwerfbaum (H-a2);
  H-aM Mutationsprobe "alte Regel (jeder Eintrag relativ zu _HIER)" mit
       Gegenprobe - die neun Eintraege mit '/' ausserhalb 'ergebnisse/'
       laegen dann woanders;
  H-b  B3: `register()` im Repo - `fehlend` leer, die neun TB-24-Listen
       unter den Teilen;
  H-c  B4: unter dem Modus endet `datenstand()` ohne Pfad mit 2;
  H-cM Mutationsprobe "Voreinstellung BASE_DIR/data unter dem Modus zurueck"
       mit Gegenprobe;
  H-d  ohne Modus liefert `datenstand()` ohne Pfad wie vorher BASE_DIR/data.
Nachgezogen (Grundsatz 40): E-bM - seit B4 endet die Mutation "Voreinstellung
in block() zurueck" nicht mehr mit 0, sondern an der zweiten Wache in
`datenstand()` mit 2; die Mutation beisst weiter, weil E-b die Stelle `block`
verlangt.

Aufruf: trading-env/bin/python3 research/vorregistrierung/test_ersatzwerte.py
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, _HIER)

import herkunft  # noqa: E402

RC_ZWEI = 2       # paths.RUECKGABEWERT_STARTPRUEFUNG - hier als Erwartung
BOT = "turtle_soup_stocks"
ECHTES_PROTOKOLL = os.path.join(_HIER, "ergebnisse", "herkunft_protokoll.jsonl")

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


def _mit_gegenprobe(name, text, lauf, bedingung, zusatz=lambda r: ""):
    """Wie in test_vorregistrierung.py: mit Mutation muss `bedingung` gelten,
    ohne Mutation darf sie nicht gelten (Register 40.7)."""
    r = lauf(True)
    pruefe(f"{name}: {text}", bedingung(r), zusatz(r))
    g = lauf(False)
    pruefe(f"{name}-G: Gegenprobe zu {name} - ohne die Mutation scheitert sie",
           not bedingung(g), zusatz(g))


def _umgebung():
    """Die Repo-Wurzel wandert mit (siehe registerdaten.BASE_DIR); kein Modus."""
    u = {k: v for k, v in os.environ.items() if not k.startswith("TB_SELEKTIONS")}
    u["TB30A_BASE_DIR"] = _REPO
    return u


def _ersetze(pfad, alt, neu, mutieren=True):
    """Die Mutation; mit `mutieren=False` nur die Pruefung, dass die Stelle
    existiert (die Gegenprobe geht denselben Weg ohne die Aenderung)."""
    with open(pfad, encoding="utf-8") as f:
        s = f.read()
    if s.count(alt) != 1:
        raise AssertionError(f"Mutationsstelle nicht genau einmal in {pfad}: {alt!r}")
    if mutieren:
        with open(pfad, "w", encoding="utf-8") as f:
            f.write(s.replace(alt, neu, 1))


def _in_kopie(treiber, datei=None, alt=None, neu=None, mutieren=False):
    """Ordner kopieren, hoechstens EINE Stelle mutieren, `treiber` (Python-
    Text) dort als eigenen Prozess laufen lassen. Rueckgabe rc/stdout/stderr."""
    with tempfile.TemporaryDirectory() as m:
        shutil.copytree(_HIER, m, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "ergebnisse"))
        # ergebnisse/ wird nicht kopiert (keine Probe hier liest daraus, und
        # eine Kopie des Protokolls darf es nicht geben); auswertung.py nennt
        # die Tabelle nur als Pfad.
        if datei:
            _ersetze(os.path.join(m, datei), alt, neu, mutieren)
        r = subprocess.run([sys.executable, "-W", "ignore", "-c",
                            f"import sys; sys.path.insert(0, {m!r})\n" + treiber],
                           capture_output=True, text=True, env=_umgebung())
    return {"rc": r.returncode, "out": r.stdout[-400:], "err": r.stderr[-600:]}


def _rc2(r, stelle):
    return r["rc"] == RC_ZWEI and stelle in r["err"]


def _info(r):
    return f"rc {r['rc']}; stderr {r['err'][-300:]!r}"


# ===========================================================================
# B  faltenplan.py
# ===========================================================================
T_A1 = "import faltenplan as fp\nprint(fp.volle_jahre({2019: 3, 2020: 4}))\n"
T_A2 = ("import faltenplan as fp\nfp.gefundene_trades_je_jahr = lambda bot: {}\n"
        f"print(fp.faltenlaenge_jahre({BOT!r}))\n")

A1_NEU = ('    innen = {j: zaehlung[j] for j in jahre[1:-1]}\n'
          '    if not innen:\n'
          '        _abbruch_2("volle_jahre",')
A1_ALT = ('    innen = {j: zaehlung[j] for j in jahre[1:-1]} or {jahre[0]: zaehlung[jahre[0]]}\n'
          '    if not innen:\n'
          '        _abbruch_2("volle_jahre",')
A2_NEU = '    if not zaehlung:\n        _abbruch_2("faltenlaenge_jahre",'
A2_ALT = ('    if not zaehlung:\n        return 2, 0.0, "keine vollen Kalenderjahre gemessen"\n'
          '        _abbruch_2("faltenlaenge_jahre",')


def teil_b():
    r = _in_kopie(T_A1)
    pruefe("B-A1: volle_jahre ohne inneres Jahr endet mit 2", _rc2(r, "volle_jahre"), _info(r))
    r = _in_kopie("import faltenplan as fp\nassert fp.volle_jahre({2018: 1, 2019: 3, 2020: 4}) == {2019: 3}\n"
                  "assert fp.volle_jahre({}) == {}\n")
    pruefe("B-A1b: mit innerem Jahr unveraendert, leere Zaehlung bleibt {}", r["rc"] == 0, _info(r))
    _mit_gegenprobe(
        "B-A1M", "Mutationsprobe 'erstes angeschnittenes Jahr als Ersatz zurueck' - B-A1 waere rot",
        lambda mut: _in_kopie(T_A1, "faltenplan.py", A1_NEU, A1_ALT, mut),
        lambda r: r["rc"] == 0, _info)

    r = _in_kopie(T_A2)
    pruefe("B-A2: faltenlaenge_jahre mit leerer Zaehlung endet mit 2",
           _rc2(r, "faltenlaenge_jahre"), _info(r))
    _mit_gegenprobe(
        "B-A2M", "Mutationsprobe 'Faltenlaenge 2 als Ersatz zurueck' - B-A2 waere rot",
        lambda mut: _in_kopie(T_A2, "faltenplan.py", A2_NEU, A2_ALT, mut),
        lambda r: r["rc"] == 0, _info)


# ===========================================================================
# C  benchmark.py
# ===========================================================================
T_A3 = ("import benchmark as bm, pandas as pd\n"
        "print(bm.drawdown_bei_exposure(pd.Series([], dtype=float), 0.5))\n")
T_A4 = ("import benchmark as bm, registerdaten as rd\n"
        f"bm.fp.faltenplan = lambda mess: {{{BOT!r}: {{'status': 'endgueltig', 'falten': []}}}}\n"
        "bm.tagesschluss = lambda markt: {}\n"
        "bm.fsm.loader_lesart = lambda bot: {'handelbar_ab': {}, 'schranke': 'S', 'wert': 0}\n"
        f"rd.BOTS = {{{BOT!r}: rd.BOTS[{BOT!r}]}}\n"
        f"print(bm.je_bot({{}})[{BOT!r}]['dd_toleranz']['0.50'])\n")

A3_NEU = '    if renditen.empty:\n        _abbruch_2("drawdown_bei_exposure",'
A3_ALT = '    if renditen.empty:\n        return 0.0\n        _abbruch_2("drawdown_bei_exposure",'
A4_NEU = '        if not sel:\n            _abbruch_2("je_bot",'
A4_ALT = '        if not sel:\n            pass\n        if False:\n            _abbruch_2("je_bot",'
A4_MEDIAN_NEU = 'round(float(np.median(werte)), 2)\n'
A4_MEDIAN_ALT = 'round(float(np.median(werte)), 2) if werte else 0.0\n'


def _a4_lauf(mut):
    """Beide Zeilen der alten Stelle zurueck: die Wache weg UND `if werte
    else 0.0` wieder da - sonst scheitert die Mutation an np.median([]) (NaN
    mit Warnung) statt am Ersatzwert."""
    with tempfile.TemporaryDirectory() as m:
        shutil.copytree(_HIER, m, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "ergebnisse"))
        pfad = os.path.join(m, "benchmark.py")
        _ersetze(pfad, A4_NEU, A4_ALT, mut)
        _ersetze(pfad, A4_MEDIAN_NEU, A4_MEDIAN_ALT, mut)
        r = subprocess.run([sys.executable, "-W", "ignore", "-c",
                            f"import sys; sys.path.insert(0, {m!r})\n" + T_A4],
                           capture_output=True, text=True, env=_umgebung())
    return {"rc": r.returncode, "out": r.stdout[-400:], "err": r.stderr[-600:]}


def teil_c():
    r = _in_kopie(T_A3)
    pruefe("C-A3: drawdown_bei_exposure mit leerer Reihe endet mit 2",
           _rc2(r, "drawdown_bei_exposure"), _info(r))
    _mit_gegenprobe(
        "C-A3M", "Mutationsprobe '0.0 fuer die leere Reihe zurueck' - C-A3 waere rot",
        lambda mut: _in_kopie(T_A3, "benchmark.py", A3_NEU, A3_ALT, mut),
        lambda r: r["rc"] == 0 and r["out"].strip().endswith("0.0"), _info)

    r = _in_kopie(T_A4)
    pruefe("C-A4: je_bot ohne Selektionsfalte endet mit 2", _rc2(r, "je_bot"), _info(r))
    _mit_gegenprobe(
        "C-A4M", "Mutationsprobe 'dd_toleranz 0.0 ohne Selektionsfalte zurueck' - C-A4 waere rot",
        _a4_lauf, lambda r: r["rc"] == 0 and r["out"].strip().endswith("0.0"), _info)

    r = _in_kopie("import benchmark as bm\nt = {'0.01': -2.0, '0.02': -4.0}\n"
                  "assert bm.nachschlagen(t, 0.0) == 0.0 and bm.nachschlagen(t, -1) == 0.0\n"
                  "assert abs(bm.nachschlagen(t, 0.005) + 1.0) < 1e-12\n")
    pruefe("C-A5: nachschlagen(e <= 0) bleibt 0.0 - Rechenregel, nicht geaendert (C2)",
           r["rc"] == 0, _info(r))


# ===========================================================================
# D  auswertung.py
# ===========================================================================
T_A6_ZELLE = ("import auswertung as aw, pandas as pd\n"
              "aw.plateau({'a': [1, 2, 3]}, None, pd.Series({'a=2': 0.2, 'a=3': 0.3}))\n")
T_A6_NACHBAR = ("import auswertung as aw, pandas as pd\n"
                "aw.plateau({'a': [1, 2, 3]}, None, pd.Series({'a=1': 0.1, 'a=2': 0.2}))\n")
A6_NEU = ('    if zid not in statistik.index:\n'
          '        _abbruch_2("plateau",')
A6_ALT = ('    if zid not in statistik.index:\n'
          '        return 0.0\n'
          '        _abbruch_2("plateau",')

T_A7 = f"""
import os, tempfile, pandas as pd, auswertung as aw
w = tempfile.mkdtemp()
os.makedirs(os.path.join(w, {BOT!r}, "tagesreihen"))
os.makedirs(os.path.join(w, "benchmark_tagesreihen"))
tage = pd.date_range("2020-01-01", periods=10, freq="B")
pd.DataFrame({{"datum": tage, "netto_rendite": 0.001, "exposure": 0.5}}).to_csv(
    os.path.join(w, {BOT!r}, "tagesreihen", "z.csv"), index=False)
pd.DataFrame({{"datum": tage, "netto_rendite": 0.001}}).to_csv(
    os.path.join(w, "benchmark_tagesreihen", "aktien.csv"), index=False)
plan = {{{BOT!r}: {{"falten": [{{"name": "2020", "von": "2020-01-01",
    "bis_ausschliesslich": "2021-01-01", "rolle": "bestaetigung"}}]}}}}
print(aw.beta_bereinigung({BOT!r}, w, "z", plan, []))
"""
A7_NEU = '    if not fenster:\n        _abbruch_2("beta_bereinigung",'
A7_ALT = ('    if not fenster:\n'
          '        return {"bestimmt": False, "grund": "keine Selektionsfalten (Platzhalter)"}\n'
          '        _abbruch_2("beta_bereinigung",')

T_A7B = ("import auswertung as aw\n"
         "k = aw.abbruchkriterien('x', {'statistik': 1.0, 'spitze': False}, None, {'z'}, None,\n"
         "                        {'bestimmt': False, 'grund': 'Platzhalter'}, None)\n"
         "print('c =', k['c_beta_bereinigung'])\n")
A7B_NEU = ('    c = (bereinigung["alpha_pct_pa"] <= 0.0\n'
           '         and bereinigung["strategie_calmar"]\n'
           '         < bereinigung["konstante_exposure"]["calmar"])\n')
A7B_ALT = ('    if bereinigung.get("bestimmt"):\n'
           '        c = (bereinigung["alpha_pct_pa"] <= 0.0\n'
           '             and bereinigung["strategie_calmar"]\n'
           '             < bereinigung["konstante_exposure"]["calmar"])\n'
           '    else:\n'
           '        c = False\n')
T_A7B_EIN_BOT = ("import auswertung as aw\n"
                 "print('get', open(aw.__file__, encoding='utf-8').read().count('bereinigung.get('))\n")
A7B_EB_NEU = 'dsr_drei_werte(bereinigung["renditen"], buch)'
A7B_EB_ALT = 'dsr_drei_werte(bereinigung.get("renditen", []), buch)'

T_A7C = ("import auswertung as aw\n"
         "aw.rd.raster_definition = lambda: {'x': {'_bedingung': 'a < b'}}\n"
         "print(aw.bedingung_fuer('x'))\n")
A7C_NEU = '    _abbruch_2("bedingung_fuer",'
A7C_ALT = '    return None\n    _abbruch_2("bedingung_fuer",'


def teil_d():
    r = _in_kopie(T_A6_ZELLE)
    pruefe("D-A6: plateau ohne Statistik fuer eine existierende Zelle endet mit 2",
           _rc2(r, "plateau") and "Zelle" in r["err"], _info(r))
    r = _in_kopie(T_A6_NACHBAR)
    pruefe("D-A6n: plateau ohne Statistik fuer einen Nachbarn endet mit 2",
           _rc2(r, "plateau") and "Nachbar" in r["err"], _info(r))
    _mit_gegenprobe(
        "D-A6M", "Mutationsprobe 'statistik.get(..., 0.0) zurueck' - D-A6 waere rot",
        lambda mut: _in_kopie(T_A6_ZELLE, "auswertung.py", A6_NEU, A6_ALT, mut),
        lambda r: r["rc"] == 0, _info)

    r = _in_kopie(T_A7)
    pruefe("D-A7: beta_bereinigung ohne Selektionsfalten endet mit 2",
           _rc2(r, "beta_bereinigung"), _info(r))
    _mit_gegenprobe(
        "D-A7M", "Mutationsprobe \"'bestimmt: False' zurueck\" - D-A7 waere rot",
        lambda mut: _in_kopie(T_A7, "auswertung.py", A7_NEU, A7_ALT, mut),
        lambda r: r["rc"] == 0 and "'bestimmt': False" in r["out"], _info)

    # A7b: nach D2 ist der Zweig unerreichbar; geprueft wird, dass eine
    # unvollstaendige Bereinigung nicht mehr still c = False ergibt.
    r = _in_kopie(T_A7B)
    pruefe("D-A7b: abbruchkriterien mit unvollstaendiger Bereinigung liefert kein stilles c = False",
           r["rc"] != 0 and "KeyError" in r["err"], _info(r))
    _mit_gegenprobe(
        "D-A7bM", "Mutationsprobe \"'else: c = False' zurueck\" - D-A7b waere rot",
        lambda mut: _in_kopie(T_A7B, "auswertung.py", A7B_NEU, A7B_ALT, mut),
        lambda r: r["rc"] == 0 and "c = False" in r["out"], _info)
    r = _in_kopie(T_A7B_EIN_BOT)
    pruefe("D-A7b2: ein_bot liest die Bereinigung ohne .get(...)",
           r["rc"] == 0 and r["out"].strip().endswith("get 0"), _info(r))
    _mit_gegenprobe(
        "D-A7b2M", "Mutationsprobe \"'.get(\"renditen\", [])' zurueck\" - D-A7b2 waere rot",
        lambda mut: _in_kopie(T_A7B_EIN_BOT, "auswertung.py", A7B_EB_NEU, A7B_EB_ALT, mut),
        lambda r: r["rc"] == 0 and r["out"].strip().endswith("get 1"), _info)

    r = _in_kopie(T_A7C)
    pruefe("D-A7c: unbekannter _bedingung-Text endet mit 2", _rc2(r, "bedingung_fuer"), _info(r))
    r = _in_kopie("import auswertung as aw\n"
                  "aw.rd.raster_definition = lambda: {'o': {}, 'l': {'_bedingung': ''}}\n"
                  "assert aw.bedingung_fuer('o') is None and aw.bedingung_fuer('l') is None\n"
                  "aw.rd.raster_definition = lambda: {'t': {'_bedingung': 't3_fast_length < t3_slow_length'}}\n"
                  "b = aw.bedingung_fuer('t')\n"
                  "assert b({'t3_fast_length': 1, 't3_slow_length': 2}) and not b({'t3_fast_length': 2, 't3_slow_length': 2})\n")
    pruefe("D-A7c2: ohne Text keine Rasterbedingung, der bekannte Text unveraendert", r["rc"] == 0, _info(r))
    _mit_gegenprobe(
        "D-A7cM", "Mutationsprobe 'stilles None zurueck' - D-A7c waere rot",
        lambda mut: _in_kopie(T_A7C, "auswertung.py", A7C_NEU, A7C_ALT, mut),
        lambda r: r["rc"] == 0 and r["out"].strip().endswith("None"), _info)


# ===========================================================================
# E  herkunft.py - Datenpfad und Protokollordner, im Wegwerfbaum
# ===========================================================================
_E_SNAP_HASH = "attrappe_tb106_herkunft_00000000000000"
E1_NEU = '    if daten_dir is None and _paths().selektionsmodus() is not None:\n'
E1_ALT = '    if False:\n'
E3_NEU = ('    if not os.path.isdir(os.path.dirname(PROTOKOLL)):\n'
          '        _abbruch_2("anhaengen",')
E3_ALT = ('    os.makedirs(os.path.dirname(PROTOKOLL), exist_ok=True)\n'
          '    if not os.path.isdir(os.path.dirname(PROTOKOLL)):\n'
          '        _abbruch_2("anhaengen",')
_E_TREIBER = ("import sys, os, json\n"
              "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
              "import herkunft\n"
              "print(json.dumps(herkunft.block('probe'), sort_keys=True))\n")


def _git(baum, *a):
    subprocess.run(["git", "-C", baum] + list(a), check=True, capture_output=True, text=True)


def _csv(pfad, text):
    with open(pfad, "w", encoding="utf-8") as f:
        f.write("open_time,close\n2020-01-01,%s\n" % text)


def _e_baum(t, mutation=None, mit_ergebnisse=True, git=True):
    """Ein Baum mit echter paths.py und (mutierter) herkunft.py; data/ und
    die Snapshot-Attrappe tragen VERSCHIEDENE Kursdateien, damit sich zeigt,
    welcher Ordner gehasht wurde."""
    baum, snap = os.path.join(t, "baum"), os.path.join(t, "snap")
    v = os.path.join(baum, "research", "vorregistrierung")
    for o in (os.path.join(baum, "shared"), os.path.join(baum, "data"), v,
              os.path.join(snap, "config")):
        os.makedirs(o)
    shutil.copy2(os.path.join(_REPO, "shared", "paths.py"), os.path.join(baum, "shared"))
    shutil.copy2(os.path.join(_REPO, "requirements.lock"), baum)
    shutil.copy2(os.path.join(_HIER, "herkunft.py"), v)
    if mutation:
        _ersetze(os.path.join(v, "herkunft.py"), *mutation)
    with open(os.path.join(v, "probe_block.py"), "w", encoding="utf-8") as f:
        f.write(_E_TREIBER)
    if mit_ergebnisse:
        os.makedirs(os.path.join(v, "ergebnisse"))
        with open(os.path.join(v, "ergebnisse", "LIESMICH.txt"), "w") as f:
            f.write("versioniert, damit der Ordner im Klon existiert\n")
    _csv(os.path.join(baum, "data", "AAA_1d.csv"), "1.0")
    _csv(os.path.join(snap, "AAA_1d.csv"), "2.0")
    _csv(os.path.join(snap, "BBB_1d.csv"), "3.0")
    for name, text in (("top25_symbols.txt", "AAAUSDT\n"), ("sp500_top150.txt", "AAA\n")):
        with open(os.path.join(snap, "config", name), "w") as f:
            f.write(text)
    with open(os.path.join(snap, "MANIFEST.json"), "w") as f:
        json.dump({"snapshot_hash": _E_SNAP_HASH,
                   "dateien": {"AAA_1d.csv": {}, "BBB_1d.csv": {},
                               "config/top25_symbols.txt": {},
                               "config/sp500_top150.txt": {}}}, f)
    head = None
    if git:
        # Wie im Repo: Bytecode-Caches sind ignoriert (Fable 25c 4 (4)(a)) -
        # sonst machte der Import von paths.py den Baum selbst schmutzig.
        with open(os.path.join(baum, ".gitignore"), "w") as f:
            f.write("__pycache__/\n")
        _git(baum, "init", "-q")
        _git(baum, "add", "-A")
        _git(baum, "-c", "user.name=tb106", "-c", "user.email=tb106@test",
             "commit", "-q", "-m", "Wegwerfbaum")
        head = subprocess.run(["git", "-C", baum, "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    return baum, snap, v, head


def _e_lauf(t, baum, snap, head, argv, modus=True):
    u = {k: v for k, v in os.environ.items()
         if k not in ("TB30A_BASE_DIR", "PYTHONPATH") and not k.startswith("TB_SELEKTIONS")}
    if modus:
        u.update({"TB_SELEKTIONSWURZEL": snap, "TB_SELEKTIONSHASH": _E_SNAP_HASH,
                  "TB_SELEKTIONSCOMMIT": head})
    r = subprocess.run([sys.executable, "-W", "ignore"] + argv,
                       capture_output=True, text=True, env=u)
    return {"rc": r.returncode, "out": r.stdout, "err": r.stderr[-600:]}


def _e2_lauf(mut):
    """Modus, block() ohne daten_dir."""
    with tempfile.TemporaryDirectory() as t:
        baum, snap, v, head = _e_baum(t, (E1_NEU, E1_ALT, mut))
        return _e_lauf(t, baum, snap, head, [os.path.join(v, "probe_block.py")])


def _e3_lauf(mut):
    """Ohne Modus, ergebnisse/ fehlt: anhaengen() endet mit 2, kein Ordner."""
    with tempfile.TemporaryDirectory() as t:
        baum, snap, v, head = _e_baum(t, (E3_NEU, E3_ALT, mut), mit_ergebnisse=False, git=False)
        r = _e_lauf(t, baum, snap, head, [os.path.join(v, "herkunft.py"), "--anhaengen", "probe"],
                    modus=False)
        r["ordner_angelegt"] = os.path.exists(os.path.join(v, "ergebnisse"))
        return r


def teil_e():
    vorher = _sha(ECHTES_PROTOKOLL)

    # E1/E2: Modus, CLI --anhaengen uebergibt paths.DATA_DIR = Snapshot.
    with tempfile.TemporaryDirectory() as t:
        baum, snap, v, head = _e_baum(t)
        r = _e_lauf(t, baum, snap, head, [os.path.join(v, "herkunft.py"), "--anhaengen", "probe"])
        prot = os.path.join(v, "ergebnisse", "herkunft_protokoll.jsonl")
        zeile = {}
        if r["rc"] == 0 and os.path.exists(prot):
            with open(prot, encoding="utf-8") as f:
                zeile = json.loads(f.read().splitlines()[-1])
        soll = herkunft.datenstand(snap)
        falsch = herkunft.datenstand(os.path.join(baum, "data"))
        pruefe("E-a: Modus, --anhaengen hasht den Snapshot (paths.DATA_DIR), nicht data/",
               r["rc"] == 0 and zeile.get("datenstand") == soll["datenstand"]
               and zeile.get("datendateien") == soll["dateien"] == 2
               and soll["datenstand"] != falsch["datenstand"],
               f"{_info(r)}; Zeile {zeile.get('datenstand')}, Snapshot {soll}, data/ {falsch}")

    r = _e2_lauf(False)
    pruefe("E-b: Modus, block() ohne daten_dir endet mit 2", _rc2(r, "block"), _info(r))
    # TB-114 (Grundsatz 40): bis TB-113 lief die Mutation mit rc 0 durch; seit
    # B4 haelt sie `datenstand()` mit 2 auf. Die Mutation beisst weiter: E-b
    # verlangt 2 an der Stelle `block`, die Mutation endet an `datenstand`.
    _mit_gegenprobe(
        "E-bM", "Mutationsprobe 'Voreinstellung BASE_DIR/data unter dem Modus zurueck' - E-b waere rot",
        _e2_lauf, lambda r: not _rc2(r, "block") and _rc2(r, "datenstand"), _info)

    r = _e3_lauf(False)
    pruefe("E-c: ohne Modus, Protokollordner fehlt -> 2, kein Ordner angelegt",
           _rc2(r, "anhaengen") and not r["ordner_angelegt"], _info(r))
    _mit_gegenprobe(
        "E-cM", "Mutationsprobe 'makedirs zurueck' - E-c waere rot",
        _e3_lauf, lambda r: r["rc"] == 0 and r["ordner_angelegt"],
        lambda r: _info(r) + f"; Ordner angelegt {r['ordner_angelegt']}")

    # E-d: ohne Modus liefert block() dieselben Felder wie vorher und hasht
    # BASE_DIR/data (die Voreinstellung bleibt).
    with tempfile.TemporaryDirectory() as t:
        baum, snap, v, head = _e_baum(t)
        r = _e_lauf(t, baum, snap, head, [os.path.join(v, "probe_block.py")], modus=False)
        b = json.loads(r["out"].strip().splitlines()[-1]) if r["rc"] == 0 else {}
        felder = {"zeitpunkt_utc", "anlass", "commit", "arbeitsbaum_sauber",
                  "geaenderte_dateien", "datenstand", "datendateien", "register",
                  "register_fehlend"}
        pruefe("E-d: ohne Modus block() wie vorher - dieselben Felder, Datenstand von BASE_DIR/data",
               set(b) == felder and b.get("datenstand")
               == herkunft.datenstand(os.path.join(baum, "data"))["datenstand"],
               f"{_info(r)}; Felder {sorted(b)}")

    pruefe("E-e: das echte herkunft_protokoll.jsonl ist unberuehrt",
           _sha(ECHTES_PROTOKOLL) == vorher, f"vorher {vorher}, nachher {_sha(ECHTES_PROTOKOLL)}")


# ===========================================================================
# F  herkunft.py - Pruefansicht und TB30A_BASE_DIR unter dem Modus (TB-111)
# ===========================================================================
_F_SNAP_HASH = "63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
_F_SNAP = os.path.join(_REPO, "snapshots", _F_SNAP_HASH)
_F_DATENSTAND = "d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84"
FA_NEU = ('    b = block("pruefung", resolver.DATA_DIR\n'
          '              if resolver.selektionsmodus() is not None else None)\n')
FA_ALT = '    b = block("pruefung")\n'
FB_NEU = ('    if not (os.environ.get("TB30A_BASE_DIR") or BASE_DIR != _WURZEL):\n'
          '        return\n')
FB_ALT = '    return\n'
FB2_NEU = '    ordner = os.path.join(_WURZEL, "shared")\n'
FB2_ALT = '    ordner = os.path.join(BASE_DIR, "shared")\n'
_F_TREIBER = ("import sys, os, json\n"
              "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
              "import herkunft\n"
              "was = sys.argv[1]\n"
              "e = (herkunft.commit() if was == 'commit' else herkunft.register()\n"
              "     if was == 'register' else herkunft.block('probe', sys.argv[2]))\n"
              "print(json.dumps(e, sort_keys=True))\n")
# Der Lesehaken: jeder Zugriff unter der Ersatzwurzel (open, listdir, scandir,
# stat - darueber auch exists/isdir -, git und jeder andere Unterprozess)
# landet im Protokoll. Ueber PYTHONPATH als sitecustomize geladen.
_F_HAKEN = """
import builtins, io, os, subprocess
_E = os.path.realpath(os.environ["TB111_ERSATZ"])
_P = os.environ["TB111_PROT"]
_open = builtins.open
def _merke(art, pfad):
    try:
        r = os.path.realpath(os.fspath(pfad))
    except Exception:
        return
    if r == _E or r.startswith(_E + os.sep):
        with _open(_P, "a") as f:
            f.write(art + " " + r + chr(10))
def _huelle(art, echt):
    def h(pfad=".", *a, **k):
        if not isinstance(pfad, int):
            _merke(art, pfad)
        return echt(pfad, *a, **k)
    return h
builtins.open = io.open = _huelle("open", _open)
os.listdir = _huelle("listdir", os.listdir)
os.scandir = _huelle("scandir", os.scandir)
os.stat = _huelle("stat", os.stat)
_popen = subprocess.Popen.__init__
def _popen_haken(self, args, *a, **k):
    for x in ([args] if isinstance(args, (str, bytes)) else list(args)) + [k.get("cwd") or ""]:
        if isinstance(x, (str, bytes, os.PathLike)) and x:
            _merke("subprocess", x)
    return _popen(self, args, *a, **k)
subprocess.Popen.__init__ = _popen_haken
"""


def _f_ersatz(t):
    """Die Ersatzwurzel: ein Baum, den `TB30A_BASE_DIR` benennt - mit data/,
    Registerdatei und eigenem Git, damit jeder Zugriff etwas faende."""
    e = os.path.join(t, "ersatz")
    for o in (os.path.join(e, "data"), os.path.join(e, "docs")):
        os.makedirs(o)
    _csv(os.path.join(e, "data", "ZZZ_1d.csv"), "9.0")
    with open(os.path.join(e, "docs", "VORREGISTRIERUNG_neuselektion.md"), "w") as f:
        f.write("Ersatzregister\n")
    _git(e, "init", "-q")
    _git(e, "add", "-A")
    _git(e, "-c", "user.name=tb111", "-c", "user.email=tb111@test",
         "commit", "-q", "-m", "Ersatzwurzel")
    return e


def _f_lauf(t, baum, head, argv, snap=_F_SNAP, snap_hash=_F_SNAP_HASH,
            modus=True, ersatz=None):
    """Ein Lauf im Wegwerfbaum; mit `ersatz` steht TB30A_BASE_DIR und der
    Lesehaken zeichnet jeden Zugriff darunter auf."""
    u = {k: v for k, v in os.environ.items()
         if k not in ("TB30A_BASE_DIR", "PYTHONPATH") and not k.startswith("TB_SELEKTIONS")}
    if modus:
        u.update({"TB_SELEKTIONSWURZEL": snap, "TB_SELEKTIONSHASH": snap_hash,
                  "TB_SELEKTIONSCOMMIT": head})
    prot = os.path.join(t, "lesehaken.txt")
    if ersatz:
        haken = os.path.join(t, "haken")
        os.makedirs(haken, exist_ok=True)
        with open(os.path.join(haken, "sitecustomize.py"), "w") as f:
            f.write(_F_HAKEN)
        u.update({"TB30A_BASE_DIR": ersatz, "PYTHONPATH": haken,
                  "TB111_ERSATZ": ersatz, "TB111_PROT": prot})
    r = subprocess.run([sys.executable, "-W", "ignore"] + argv,
                       capture_output=True, text=True, env=u)
    zugriffe = []
    if os.path.exists(prot):
        with open(prot) as f:
            zugriffe = [z for z in f.read().splitlines() if z]
    return {"rc": r.returncode, "out": r.stdout, "err": r.stderr[-600:],
            "zugriffe": zugriffe}


def _f_treiber(v):
    with open(os.path.join(v, "probe_f.py"), "w", encoding="utf-8") as f:
        f.write(_F_TREIBER)
    return os.path.join(v, "probe_f.py")


def _f_info(r):
    return _info(r) + f"; Zugriffe unter der Ersatzwurzel {len(r['zugriffe'])}: {r['zugriffe'][:3]}"


def _fa_lauf(mut, snap=_F_SNAP, snap_hash=_F_SNAP_HASH):
    """Modus, Pruefansicht --json im Wegwerfbaum."""
    with tempfile.TemporaryDirectory() as t:
        baum, _, v, head = _e_baum(t, (FA_NEU, FA_ALT, mut))
        r = _f_lauf(t, baum, head, [os.path.join(v, "herkunft.py"), "--json"],
                    snap=snap, snap_hash=snap_hash)
        r["json"] = json.loads(r["out"]) if r["rc"] == 0 else {}
        r["data_stand"] = herkunft.datenstand(os.path.join(baum, "data"))["datenstand"]
        return r


def _fb_lauf(mut, mutation=None, argv=("pruefansicht",)):
    """Modus + TB30A_BASE_DIR mit Lesehaken; `mutation` = (neu, alt)."""
    with tempfile.TemporaryDirectory() as t:
        ersatz = _f_ersatz(t)
        baum, _, v, head = _e_baum(t, (mutation + (mut,)) if mutation else None)
        ziel = ([os.path.join(v, "herkunft.py")] if argv[0] == "pruefansicht"
                else [_f_treiber(v)] + list(argv))
        return _f_lauf(t, baum, head, ziel, ersatz=ersatz)


def _f_rc2_ohne_zugriff(r, stelle):
    return (_rc2(r, stelle) and "TB30A_BASE_DIR" in r["err"]
            and r["zugriffe"] == [])


def teil_f():
    vorher = _sha(ECHTES_PROTOKOLL)

    # F-a: Pruefansicht im Modus, am echten Snapshot und an der Attrappe
    # (die Attrappe zeigt, dass der Snapshot gehasht wird, nicht data/).
    r = _fa_lauf(False)
    h = r["json"].get("herkunft", {})
    pruefe("F-a: Modus, Pruefansicht --json rc 0, Datenstand des Snapshots d9449faf.../223",
           r["rc"] == 0 and h.get("datenstand") == _F_DATENSTAND
           and h.get("datendateien") == 223, _info(r) + f"; herkunft {h}")
    with tempfile.TemporaryDirectory() as t:
        baum, snap, v, head = _e_baum(t)
        r2 = _f_lauf(t, baum, head, [os.path.join(v, "herkunft.py"), "--json"],
                     snap=snap, snap_hash=_E_SNAP_HASH)
        h2 = json.loads(r2["out"]).get("herkunft", {}) if r2["rc"] == 0 else {}
        pruefe("F-a2: Modus, Pruefansicht an der Attrappe hasht den Snapshot, nicht data/",
               r2["rc"] == 0 and h2.get("datenstand") == herkunft.datenstand(snap)["datenstand"]
               != herkunft.datenstand(os.path.join(baum, "data"))["datenstand"],
               _info(r2) + f"; herkunft {h2}")
        r3 = _f_lauf(t, baum, head, [os.path.join(v, "herkunft.py")],
                     snap=snap, snap_hash=_E_SNAP_HASH)
        pruefe("F-a3: Modus, Pruefansicht ohne --json rc 0", r3["rc"] == 0, _info(r3))
    _mit_gegenprobe(
        "F-aM", "Mutationsprobe 'Pruefansicht ohne Pfad' - F-a waere rot (rc 2 an block)",
        _fa_lauf, lambda r: _rc2(r, "block"), _info)

    # F-b: Modus + TB30A_BASE_DIR - jeder Einstieg endet mit 2, nichts gelesen.
    for name, argv, stelle in (("F-b", ("pruefansicht",), "block"),
                               ("F-b2", ("commit",), "commit"),
                               ("F-b3", ("register",), "register"),
                               ("F-b4", ("block", _F_SNAP), "block")):
        r = _fb_lauf(False, argv=argv)
        pruefe(f"{name}: Modus + TB30A_BASE_DIR, {argv[0]} endet mit 2, Meldung nennt die "
               f"Variable, kein Zugriff unter der Ersatzwurzel",
               _f_rc2_ohne_zugriff(r, stelle), _f_info(r))
    _mit_gegenprobe(
        "F-bM", "Mutationsprobe 'Pruefung von TB30A_BASE_DIR weg' - F-b waere rot",
        lambda mut: _fb_lauf(mut, (FB_NEU, FB_ALT)),
        lambda r: not _f_rc2_ohne_zugriff(r, "block"), _f_info)
    _mit_gegenprobe(
        "F-bM2", "Mutationsprobe 'paths wieder aus BASE_DIR' - F-b waere rot",
        lambda mut: _fb_lauf(mut, (FB2_NEU, FB2_ALT)),
        lambda r: not _f_rc2_ohne_zugriff(r, "block"), _f_info)

    # F-c: ohne Modus ist TB30A_BASE_DIR die Ersatzwurzel wie vorher: block()
    # hasht ersatz/data, register() liest die Registerdatei dort, commit() ist
    # der Commit der Ersatzwurzel.
    with tempfile.TemporaryDirectory() as t:
        ersatz = _f_ersatz(t)
        baum, _, v, head = _e_baum(t)
        r = _f_lauf(t, baum, head, [_f_treiber(v), "block", os.path.join(ersatz, "data")],
                    modus=False, ersatz=ersatz)
        b = json.loads(r["out"].strip().splitlines()[-1]) if r["rc"] == 0 else {}
        e_head = subprocess.run(["git", "-C", ersatz, "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
        rr = _f_lauf(t, baum, head, [_f_treiber(v), "register"], modus=False, ersatz=ersatz)
        reg = json.loads(rr["out"].strip().splitlines()[-1]) if rr["rc"] == 0 else {}
        pruefe("F-c: ohne Modus wirkt TB30A_BASE_DIR wie vorher (Commit, Datenstand, "
               "Registerdatei der Ersatzwurzel)",
               r["rc"] == 0 and b.get("commit") == e_head
               and b.get("datenstand") == herkunft.datenstand(os.path.join(ersatz, "data"))["datenstand"]
               and rr["rc"] == 0 and any(x["datei"].endswith("VORREGISTRIERUNG_neuselektion.md")
                                         and x["sha256"] == _sha(os.path.join(
                                             ersatz, "docs", "VORREGISTRIERUNG_neuselektion.md"))
                                         for x in reg.get("teile", [])),
               _info(r) + f"; commit {b.get('commit')} / {e_head}; register {_info(rr)}")

    pruefe("F-e: das echte herkunft_protokoll.jsonl ist unberuehrt",
           _sha(ECHTES_PROTOKOLL) == vorher, f"vorher {vorher}, nachher {_sha(ECHTES_PROTOKOLL)}")


# ===========================================================================
# G  auswertung.py - Abbruch endet mit 2 (TB-111)
# ===========================================================================
T_G_SPALTE = f"""
import os, tempfile, auswertung as aw
w = tempfile.mkdtemp()
os.makedirs(os.path.join(w, {BOT!r}))
with open(os.path.join(w, {BOT!r}, "zellen.csv"), "w") as f:
    f.write(",".join(aw.PFLICHTSPALTEN[:-1]) + chr(10))
aw.lies_zellen({BOT!r}, w, None, None)
"""
T_G_ZELLE = f"""
import os, tempfile, auswertung as aw
w = tempfile.mkdtemp()
os.makedirs(os.path.join(w, {BOT!r}))
with open(os.path.join(w, {BOT!r}, "zellen.csv"), "w") as f:
    f.write(",".join(aw.PFLICHTSPALTEN) + chr(10) + "ausserhalb=1,2020,selektion,1,0.1,1.0,-5.0,0.5" + chr(10))
aw.gitterachsen = lambda bot, mess: {{"a": [1, 2]}}
aw.bedingung_fuer = lambda bot: None
aw.lies_zellen({BOT!r}, w, None, None)
"""
T_G_TAGE = f"""
import os, tempfile, pandas as pd, auswertung as aw
w = tempfile.mkdtemp()
os.makedirs(os.path.join(w, {BOT!r}, "tagesreihen"))
os.makedirs(os.path.join(w, "benchmark_tagesreihen"))
tage = pd.date_range("2020-01-01", periods=10, freq="B")
pd.DataFrame({{"datum": tage, "netto_rendite": 0.001, "exposure": 0.5}}).to_csv(
    os.path.join(w, {BOT!r}, "tagesreihen", "z.csv"), index=False)
pd.DataFrame({{"datum": tage[:2], "netto_rendite": 0.001}}).to_csv(
    os.path.join(w, "benchmark_tagesreihen", "aktien.csv"), index=False)
plan = {{{BOT!r}: {{"falten": [{{"name": "2020", "von": "2020-01-01",
    "bis_ausschliesslich": "2021-01-01", "rolle": "selektion"}}]}}}}
print(aw.beta_bereinigung({BOT!r}, w, "z", plan, ["2020"]))
"""
G_NEU = '        super().__init__(paths.RUECKGABEWERT_STARTPRUEFUNG)\n'
G_ALT = '        super().__init__(1)\n'


def _abbruch2(r, text):
    return r["rc"] == RC_ZWEI and text in r["err"]


def teil_g():
    with tempfile.TemporaryDirectory() as leer:
        r = subprocess.run([sys.executable, "-W", "ignore", os.path.join(_HIER, "auswertung.py"),
                            "--rohergebnisse", leer], capture_output=True, text=True,
                           env=_umgebung())
        r = {"rc": r.returncode, "out": r.stdout[-400:], "err": r.stderr[-600:]}
    pruefe("G-a: auswertung.py --rohergebnisse <leer> endet mit 2 (vorher 1), Meldung auf stderr",
           _abbruch2(r, "fehlt - der Lauf ist unvollstaendig"), _info(r))
    for name, treiber, text in (("G-b", T_G_SPALTE, "Spalten fehlen in zellen.csv"),
                                ("G-c", T_G_ZELLE, "liegen nicht im Raster"),
                                ("G-d", T_G_TAGE, "weniger als drei gemeinsame Tage")):
        r = _in_kopie(treiber)
        pruefe(f"{name}: Abbruch '{text}' endet mit 2, Meldung auf stderr",
               _abbruch2(r, text), _info(r))
    _mit_gegenprobe(
        "G-M", "Mutationsprobe 'Code 1 zurueck' - G-b waere rot",
        lambda mut: _in_kopie(T_G_SPALTE, "auswertung.py", G_NEU, G_ALT, mut),
        lambda r: r["rc"] == 1 and "Spalten fehlen in zellen.csv" in r["err"], _info)


# ===============================================================================
# H  herkunft.py - eine Pfadregel mit der Sonde, die neun TB-24-Listen,
#    datenstand(None) unter dem Modus (TB-114)
# ===============================================================================
H1_NEU = '    return os.path.normpath(os.path.join(_WURZEL, rel))\n'
H1_ALT = '    return os.path.normpath(os.path.join(_HIER, rel))\n'
B4_NEU = '    if not daten_dir and _paths().selektionsmodus() is not None:\n'
B4_ALT = '    if False:\n'
TB24_LISTEN = ["research/tb24_haltedauern/daten/%s_alle_trades.csv" % b
               for b in sorted(os.listdir(os.path.join(_REPO, "strategies")))
               if os.path.isdir(os.path.join(_REPO, "strategies", b))]
# Treiber der Gegenprobe: laedt herkunft.py aus seinem Baum und die Sonde aus
# der echten shared/ - vergleicht je Eintrag die absoluten Pfade.
_H_TREIBER = ("import sys, os, json\n"
              "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
              "sys.path.insert(0, sys.argv[1])\n"
              "import herkunft, sperrlistensonde as s\n"
              "w = herkunft._WURZEL\n"
              "a = [rel for rel in herkunft.EINGEFROREN if herkunft._eingefroren_pfad(rel)\n"
              "     != os.path.normpath(os.path.join(w, s._aufloesen(rel)))]\n"
              "print(json.dumps({'eintraege': len(herkunft.EINGEFROREN), 'abweichend': a}))\n")
_H_DATENSTAND = ("import sys, os, json\n"
                 "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
                 "import herkunft\n"
                 "print(json.dumps(herkunft.datenstand(), sort_keys=True))\n")


def gegenprobe_pfadregel(herkunft_modul, sonde_modul):
    """B1 im laufenden Prozess: die Eintraege, deren Orte sich unterscheiden."""
    w = herkunft_modul._WURZEL
    return [rel for rel in herkunft_modul.EINGEFROREN
            if herkunft_modul._eingefroren_pfad(rel)
            != os.path.normpath(os.path.join(w, sonde_modul._aufloesen(rel)))]


def _ha_lauf(mut):
    """Gegenprobe in einem Wegwerfbaum <t>/research/vorregistrierung/, damit
    `_WURZEL` dort liegt; mit Mutation steht die alte Regel (_HIER) wieder da."""
    with tempfile.TemporaryDirectory() as t:
        v = os.path.join(t, "research", "vorregistrierung")
        os.makedirs(v)
        shutil.copy2(os.path.join(_HIER, "herkunft.py"), v)
        _ersetze(os.path.join(v, "herkunft.py"), H1_NEU, H1_ALT, mut)
        with open(os.path.join(v, "probe_pfadregel.py"), "w", encoding="utf-8") as f:
            f.write(_H_TREIBER)
        r = subprocess.run([sys.executable, "-W", "ignore", os.path.join(v, "probe_pfadregel.py"),
                            os.path.join(_REPO, "shared")], capture_output=True, text=True,
                           env={k: x for k, x in os.environ.items()
                                if k not in ("TB30A_BASE_DIR", "PYTHONPATH")
                                and not k.startswith("TB_SELEKTIONS")})
    e = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 else {}
    return {"rc": r.returncode, "out": r.stdout[-400:], "err": r.stderr[-600:],
            "eintraege": e.get("eintraege"), "abweichend": e.get("abweichend")}


def _h_datenstand_lauf(mut, modus=True):
    """datenstand() ohne Pfad im Wegwerfbaum aus Teil E; die Probe ist mit
    committet, damit der Baum sauber ist."""
    with tempfile.TemporaryDirectory() as t:
        baum, snap, v, head = _e_baum(t, (B4_NEU, B4_ALT, mut))
        with open(os.path.join(v, "probe_datenstand.py"), "w", encoding="utf-8") as f:
            f.write(_H_DATENSTAND)
        _git(baum, "add", "-A")
        _git(baum, "-c", "user.name=tb114", "-c", "user.email=tb114@test",
             "commit", "-q", "-m", "Probe")
        head = subprocess.run(["git", "-C", baum, "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        r = _e_lauf(t, baum, snap, head, [os.path.join(v, "probe_datenstand.py")], modus=modus)
        r["soll_data"] = herkunft.datenstand(os.path.join(baum, "data"))["datenstand"]
        r["ist"] = (json.loads(r["out"].strip().splitlines()[-1])["datenstand"]
                    if r["rc"] == 0 else None)
        return r


def teil_h():
    sys.path.insert(0, os.path.join(_REPO, "shared"))
    import sperrlistensonde  # noqa: E402

    a = gegenprobe_pfadregel(herkunft, sperrlistensonde)
    pruefe("H-a: B1 - je Eintrag von EINGEFROREN derselbe absolute Pfad in herkunft.py und "
           "in der Sonde (%d Eintraege)" % len(herkunft.EINGEFROREN),
           not a and len(herkunft.EINGEFROREN) == 19, f"abweichend {a}")
    r = _ha_lauf(False)
    pruefe("H-a2: dieselbe Gegenprobe im Wegwerfbaum, rc 0, 0 abweichend",
           r["rc"] == 0 and r["abweichend"] == [] and r["eintraege"] == 19, _info(r))
    _mit_gegenprobe(
        "H-aM", "Mutationsprobe 'alte Regel: jeder Eintrag relativ zu _HIER' - Gegenprobe rot",
        _ha_lauf,
        lambda r: r["rc"] == 0 and sorted(r["abweichend"] or []) == sorted(TB24_LISTEN),
        lambda r: _info(r) + f"; abweichend {r['abweichend']}")

    reg = herkunft.register()
    teile = [t["datei"] for t in reg["teile"]]
    pruefe("H-b: B3 - register() im Repo: fehlend leer, 20 Teile, die neun TB-24-Listen "
           "in der Reihenfolge von strategies/",
           reg["fehlend"] == [] and len(teile) == 20 and len(TB24_LISTEN) == 9
           and teile[-9:] == TB24_LISTEN, f"fehlend {reg['fehlend']}; Teile {teile}")

    r = _h_datenstand_lauf(False)
    pruefe("H-c: B4 - Modus, datenstand() ohne Pfad endet mit 2, Meldung nennt datenstand, "
           "keine Ausgabe",
           _rc2(r, "datenstand") and r["out"] == "", _info(r))
    _mit_gegenprobe(
        "H-cM", "Mutationsprobe 'Voreinstellung BASE_DIR/data unter dem Modus zurueck' - H-c waere rot",
        _h_datenstand_lauf, lambda r: r["rc"] == 0 and r["ist"] == r["soll_data"], _info)
    r = _h_datenstand_lauf(False, modus=False)
    pruefe("H-d: ohne Modus datenstand() ohne Pfad wie vorher - rc 0, hasht BASE_DIR/data",
           r["rc"] == 0 and r["ist"] == r["soll_data"], _info(r))


def _sha(pfad):
    if not os.path.exists(pfad):
        return "(fehlt)"
    with open(pfad, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    print(__doc__.strip().split("\n")[0])
    for name, teil in (("B", teil_b), ("C", teil_c), ("D", teil_d), ("E", teil_e),
                       ("F", teil_f), ("G", teil_g), ("H", teil_h)):
        print(f"  Teil {name} ...", flush=True)
        teil()
    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
