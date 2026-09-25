#!/usr/bin/env python3
"""
TB-107 Block C - die zweite Kopie der Faltenlaengen-Regel in faltenplan_neun.py
==============================================================================
`faltenplan_neun.volle_jahre()` nahm ohne inneres Kalenderjahr still das erste,
angeschnittene Jahr als Ersatz; `faltenlaenge()` gab bei leerer Zaehlung still
`(2, 0.0)` zurueck. Dieselbe Regel steht in
`research/vorregistrierung/faltenplan.py` und endet dort seit TB-106 mit 2
(TB-106 Befund 1). Jetzt auch hier - Bauart und Proben wie TB-106 `B-A1`/`B-A2`
(`research/vorregistrierung/test_ersatzwerte.py`).

⚠️ Eigener Commit: Fables Antwort auf die Anfrage 25d steht aus. Sagt Fable
"nur Tatsachennotiz", werden Block C und diese Datei gemeinsam zurueckgenommen.

  P   Die Probe: der Zweig wird erreicht, der Prozess endet mit 2, die Meldung
      auf stderr nennt die Stelle.
  M   Die Mutationsprobe: in einer Kopie steht an GENAU dieser Stelle wieder
      der alte Ersatzwert - dann ist P rot. Jede Mutation beisst allein.
  M-G Die Gegenprobe (Register 40.7): ohne die Mutation scheitert sie.

Jede Probe laeuft als eigener Prozess ohne Modus-Variablen in einem
Wegwerfbaum (`research/faltenplan_neun/faltenplan_neun.py` als Kopie, daneben
die echte `shared/paths.py`).

Aufruf: trading-env/bin/python3 research/faltenplan_neun/test_volle_jahre.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HIER))

RC_ZWEI = 2       # paths.RUECKGABEWERT_STARTPRUEFUNG - hier als Erwartung
BOT = "turtle_soup_stocks"

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print(f"  [ok]     {name}")
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")
        print(f"  [FEHLER] {name}{(' - ' + zusatz) if zusatz else ''}")


def _mit_gegenprobe(name, text, lauf, bedingung, zusatz=lambda r: ""):
    r = lauf(True)
    pruefe(f"{name}: {text}", bedingung(r), zusatz(r))
    g = lauf(False)
    pruefe(f"{name}-G: Gegenprobe zu {name} - ohne die Mutation scheitert sie",
           not bedingung(g), zusatz(g))


def _in_kopie(treiber, alt=None, neu=None, mutieren=False):
    """Wegwerfbaum, hoechstens EINE Stelle in der Kopie mutiert, `treiber`
    als eigener Prozess. Mit `mutieren=False` wird nur geprueft, dass die
    Stelle genau einmal existiert (die Gegenprobe geht denselben Weg)."""
    with tempfile.TemporaryDirectory() as baum:
        ordner = os.path.join(baum, "research", "faltenplan_neun")
        os.makedirs(ordner)
        os.makedirs(os.path.join(baum, "shared"))
        shutil.copy2(os.path.join(_REPO, "shared", "paths.py"),
                     os.path.join(baum, "shared", "paths.py"))
        with open(os.path.join(_HIER, "faltenplan_neun.py"), encoding="utf-8") as f:
            text = f.read()
        if alt is not None:
            if text.count(alt) != 1:
                raise AssertionError(f"Mutationsstelle nicht genau einmal: {alt!r}")
            if mutieren:
                text = text.replace(alt, neu, 1)
        with open(os.path.join(ordner, "faltenplan_neun.py"), "w", encoding="utf-8") as f:
            f.write(text)
        umgebung = {k: v for k, v in os.environ.items()
                    if not k.startswith("TB_SELEKTIONS") and k != "TB36_BASE_DIR"}
        r = subprocess.run([sys.executable, "-W", "ignore", "-c",
                            f"import sys; sys.path.insert(0, {ordner!r})\n"
                            "import faltenplan_neun as fn\n" + treiber],
                           capture_output=True, text=True, env=umgebung)
    return {"rc": r.returncode, "out": r.stdout[-400:], "err": r.stderr[-600:]}


def _rc2(r, stelle):
    return r["rc"] == RC_ZWEI and f"faltenplan_neun.py::{stelle}" in r["err"]


def _info(r):
    return f"rc {r['rc']}; stdout {r['out'][-120:]!r}; stderr {r['err'][-300:]!r}"


T_A1 = "print(fn.volle_jahre({2019: 3, 2020: 4}))\n"
T_A2 = ("fn.gefundene_trades_je_jahr = lambda bot, basis=None: {}\n"
        f"print(fn.faltenlaenge({BOT!r}))\n")

A1_NEU = ('    innen = {j: zaehlung[j] for j in jahre[1:-1]}\n'
          '    if not innen:\n'
          '        _abbruch_2("volle_jahre",')
A1_ALT = ('    innen = {j: zaehlung[j] for j in jahre[1:-1]} or {jahre[0]: zaehlung[jahre[0]]}\n'
          '    if not innen:\n'
          '        _abbruch_2("volle_jahre",')
A2_NEU = '    if not zaehlung:\n        _abbruch_2("faltenlaenge",'
A2_ALT = '    if not zaehlung:\n        return 2, 0.0\n        _abbruch_2("faltenlaenge",'


def main():
    print(__doc__.strip().split("\n")[0])

    r = _in_kopie(T_A1)
    pruefe("C-A1: volle_jahre ohne inneres Jahr endet mit 2", _rc2(r, "volle_jahre"), _info(r))
    r = _in_kopie("assert fn.volle_jahre({2018: 1, 2019: 3, 2020: 4}) == {2019: 3}\n"
                  "assert fn.volle_jahre({}) == {}\n")
    pruefe("C-A1b: mit innerem Jahr unveraendert, leere Zaehlung bleibt {}", r["rc"] == 0, _info(r))
    _mit_gegenprobe(
        "C-A1M", "Mutationsprobe 'erstes angeschnittenes Jahr als Ersatz zurueck' - C-A1 waere rot",
        lambda mut: _in_kopie(T_A1, A1_NEU, A1_ALT, mut),
        lambda r: r["rc"] == 0 and r["out"].strip() == "{2019: 3}", _info)

    r = _in_kopie(T_A2)
    pruefe("C-A2: faltenlaenge mit leerer Zaehlung endet mit 2", _rc2(r, "faltenlaenge"), _info(r))
    _mit_gegenprobe(
        "C-A2M", "Mutationsprobe 'Faltenlaenge 2 mit 0.0 als Ersatz zurueck' - C-A2 waere rot",
        lambda mut: _in_kopie(T_A2, A2_NEU, A2_ALT, mut),
        lambda r: r["rc"] == 0 and r["out"].strip() == "(2, 0.0)", _info)

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
