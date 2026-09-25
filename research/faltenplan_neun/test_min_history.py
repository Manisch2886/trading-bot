#!/usr/bin/env python3
"""
TB-107 Block B - die Loader-Schranke aus dem Programmtext: genau ein Treffer
==============================================================================
`faltenschranke_messung._min_history()` liest `MIN_HISTORY_DAYS` bzw.
`MIN_HISTORY_HOURS` aus `strategies/<bot>/multi_symbol_optimise.py`. Bis TB-107
nahm es mit `re.search` still den ERSTEN Treffer, und ohne Treffer ging
`(None, None)` weiter (in `loader_lesart()` dann `TypeError`, rc 1).
`kerzen_elliott_wave()` gab bei einer anderen Schranke als `MIN_HISTORY_HOURS`
still einen `"hinweis"` statt eines Werts zurueck. Fable 25c 4 (2): genau ein
Treffer, sonst 2, unabhaengig vom Modus.

  P   Die Probe: der Zweig wird erreicht und der Prozess endet mit 2
      (`paths.RUECKGABEWERT_STARTPRUEFUNG`), die Meldung auf stderr nennt die
      Stelle.
  M   Die Mutationsprobe: in einer Kopie von `faltenschranke_messung.py` steht
      an GENAU dieser Stelle wieder der alte Code - dann ist P rot. Jede
      Mutation beisst allein (24b B3).
  M-G Die Gegenprobe (Register 40.7): dieselbe Mutationsprobe OHNE die
      Mutation muss scheitern.

Die Bot-Dateien liegen als Kopie in einem Wegwerfbaum (`TB36_BASE_DIR`, die
Ersatzwurzel von `faltenplan_neun.py` - ohne Modus zulaessig); nur die eine
Zeile der Schranke ist dort veraendert. Jede Probe laeuft als eigener Prozess
ohne Modus-Variablen. Der Arbeitsbaum wird nicht angefasst.

Aufruf: trading-env/bin/python3 research/faltenplan_neun/test_min_history.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HIER))
_WERKZEUG = os.path.join(_HIER, "faltenschranke_messung.py")

RC_ZWEI = 2       # paths.RUECKGABEWERT_STARTPRUEFUNG - hier als Erwartung
MUSTER = r"^(MIN_HISTORY_(?:DAYS|HOURS))\s*=\s*(\d+)"

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
    """Mit Mutation muss `bedingung` gelten, ohne Mutation darf sie nicht
    gelten (Register 40.7)."""
    r = lauf(True)
    pruefe(f"{name}: {text}", bedingung(r), zusatz(r))
    g = lauf(False)
    pruefe(f"{name}-G: Gegenprobe zu {name} - ohne die Mutation scheitert sie",
           not bedingung(g), zusatz(g))


def _ersetze(text, alt, neu):
    if text.count(alt) != 1:
        raise AssertionError(f"Stelle nicht genau einmal vorhanden: {alt!r}")
    return text.replace(alt, neu, 1)


def _bot_quelle(bot):
    with open(os.path.join(_REPO, "strategies", bot, "multi_symbol_optimise.py"),
              encoding="utf-8") as f:
        return f.read()


def _schrankenzeile(quelle):
    """Die eine Zeile der Schranke in der echten Bot-Datei (ganze Zeile)."""
    m = re.search(MUSTER + r".*$", quelle, re.M)
    if not m:
        raise AssertionError("keine Schrankenzeile in der echten Bot-Datei")
    return m.group(0)


def _lauf(bot, bot_quelle, treiber, werkzeug_alt=None, werkzeug_neu=None, mutieren=False):
    """Wegwerfbaum mit `strategies/<bot>/multi_symbol_optimise.py` = `bot_quelle`
    und einer Kopie von `faltenschranke_messung.py` (hoechstens EINE Stelle
    mutiert); `treiber` laeuft als eigener Prozess. `faltenplan_neun.py` ist das
    echte; es sieht den Baum ueber `TB36_BASE_DIR`."""
    with tempfile.TemporaryDirectory() as baum:
        ordner = os.path.join(baum, "strategies", bot)
        os.makedirs(ordner)
        with open(os.path.join(ordner, "multi_symbol_optimise.py"), "w",
                  encoding="utf-8") as f:
            f.write(bot_quelle)
        # Fuer loader_lesart(): die echte Krypto-Universumsdatei und EINE
        # erfundene Kursdatei (das erste Symbol, zwei Zeilen) - sonst erreicht
        # die Mutation den alten TypeError-Pfad gar nicht (B-A3M).
        os.makedirs(os.path.join(baum, "config"))
        os.makedirs(os.path.join(baum, "data"))
        shutil.copy2(os.path.join(_REPO, "config", "top25_symbols.txt"),
                     os.path.join(baum, "config", "top25_symbols.txt"))
        with open(os.path.join(_REPO, "config", "top25_symbols.txt"), encoding="utf-8") as f:
            erstes = next(z.strip() for z in f if z.strip())
        with open(os.path.join(baum, "data", f"{erstes}_1d.csv"), "w", encoding="utf-8") as f:
            f.write("timestamp,close\n2020-01-01,1.0\n2020-01-02,1.0\n")
        werkzeug = os.path.join(baum, "werkzeug")
        os.makedirs(werkzeug)
        with open(_WERKZEUG, encoding="utf-8") as f:
            text = f.read()
        if werkzeug_alt is not None:
            # Die Gegenprobe geht denselben Weg: die Stelle muss existieren.
            geaendert = _ersetze(text, werkzeug_alt, werkzeug_neu)
            if mutieren:
                text = geaendert
        with open(os.path.join(werkzeug, "faltenschranke_messung.py"), "w",
                  encoding="utf-8") as f:
            f.write(text)
        umgebung = {k: v for k, v in os.environ.items()
                    if not k.startswith("TB_SELEKTIONS")}
        umgebung["TB36_BASE_DIR"] = baum
        r = subprocess.run(
            [sys.executable, "-W", "ignore", "-c",
             f"import sys; sys.path.insert(0, {_HIER!r}); sys.path.insert(0, {werkzeug!r})\n"
             "import faltenschranke_messung as fsm\n" + treiber],
            capture_output=True, text=True, env=umgebung)
    return {"rc": r.returncode, "out": r.stdout[-400:], "err": r.stderr[-600:]}


def _rc2(r, stelle):
    return r["rc"] == RC_ZWEI and f"faltenschranke_messung.py::{stelle}" in r["err"]


def _info(r):
    return f"rc {r['rc']}; stdout {r['out'][-160:]!r}; stderr {r['err'][-300:]!r}"


# --- die Stellen im Werkzeug: neu (TB-107) und alt (bis TB-106) ---------------
B1_NEU = ('    treffer = re.findall(r"^(MIN_HISTORY_(?:DAYS|HOURS))\\s*=\\s*(\\d+)", quelle, re.M)\n'
          '    if len(treffer) != 1:\n')
B1_ALT = ('    treffer = re.search(r"^(MIN_HISTORY_(?:DAYS|HOURS))\\s*=\\s*(\\d+)", quelle, re.M)\n'
          '    if not treffer:\n'
          '        return None, None\n'
          '    return treffer.group(1), int(treffer.group(2))\n'
          '    if len(treffer) != 1:\n')
B2_NEU = '    if name != "MIN_HISTORY_HOURS":\n        _abbruch_2("kerzen_elliott_wave",'
B2_ALT = ('    if name != "MIN_HISTORY_HOURS":\n'
          '        ergebnis["hinweis"] = "elliott_wave zaehlt heute nicht mehr Kerzen"\n'
          '        return ergebnis\n'
          '        _abbruch_2("kerzen_elliott_wave",')

T_MIN = "print(fsm._min_history({bot!r}))\n"
T_KERZEN = "print(fsm.kerzen_elliott_wave())\n"
T_LESART = "print(fsm.loader_lesart({bot!r})['schranke'])\n"


def main():
    print(__doc__.strip().split("\n")[0])
    ew = _bot_quelle("elliott_wave")
    zeile_ew = _schrankenzeile(ew)
    rsi = _bot_quelle("rsi2_crypto")
    zeile_rsi = _schrankenzeile(rsi)

    zwei = rsi.replace(zeile_rsi, zeile_rsi + "\nMIN_HISTORY_DAYS = 1", 1)
    kein = rsi.replace(zeile_rsi, "# Schranke entfernt (Probe TB-107)", 1)
    ew_tage = ew.replace(zeile_ew, "MIN_HISTORY_DAYS = 730", 1)

    # --- P: die Probe laeuft auf der unveraenderten Kopie durch --------------
    r = _lauf("rsi2_crypto", rsi, T_MIN.format(bot="rsi2_crypto"))
    pruefe("B-0: unveraenderte Bot-Kopie - genau ein Treffer, rc 0, derselbe Wert wie im Repo",
           r["rc"] == 0 and r["out"].strip() == repr(
               tuple((n, int(w)) for n, w in re.findall(MUSTER, rsi, re.M))[0]), _info(r))
    r = _lauf("elliott_wave", ew, "print(fsm._min_history('elliott_wave')[0])\n")
    pruefe("B-0e: elliott_wave traegt heute MIN_HISTORY_HOURS (A2)",
           r["rc"] == 0 and r["out"].strip() == "MIN_HISTORY_HOURS", _info(r))

    # --- B1: zwei Treffer, kein Treffer ---------------------------------------
    r = _lauf("rsi2_crypto", zwei, T_MIN.format(bot="rsi2_crypto"))
    pruefe("B-A1z: zwei Treffer => rc 2, Meldung nennt Datei und Trefferzahl",
           _rc2(r, "_min_history") and "2 Treffer" in r["err"]
           and "multi_symbol_optimise.py" in r["err"], _info(r))
    r = _lauf("rsi2_crypto", kein, T_MIN.format(bot="rsi2_crypto"))
    pruefe("B-A1k: kein Treffer => rc 2, Meldung nennt Datei und Trefferzahl",
           _rc2(r, "_min_history") and "0 Treffer" in r["err"], _info(r))
    _mit_gegenprobe(
        "B-A1zM", "Mutationsprobe 're.search zurueck' - bei zwei Treffern still der erste, B-A1z waere rot",
        lambda mut: _lauf("rsi2_crypto", zwei, T_MIN.format(bot="rsi2_crypto"),
                          B1_NEU, B1_ALT, mut),
        lambda r: r["rc"] == 0 and "MIN_HISTORY_DAYS" in r["out"], _info)
    _mit_gegenprobe(
        "B-A1kM", "Mutationsprobe 're.search zurueck' - ohne Treffer still (None, None), B-A1k waere rot",
        lambda mut: _lauf("rsi2_crypto", kein, T_MIN.format(bot="rsi2_crypto"),
                          B1_NEU, B1_ALT, mut),
        lambda r: r["rc"] == 0 and r["out"].strip() == "(None, None)", _info)

    # --- B2: elliott_wave mit einer Tage-Schranke ------------------------------
    r = _lauf("elliott_wave", ew_tage, T_KERZEN)
    pruefe("B-A2: elliott_wave mit MIN_HISTORY_DAYS => kerzen_elliott_wave endet mit 2",
           _rc2(r, "kerzen_elliott_wave") and "MIN_HISTORY_DAYS" in r["err"], _info(r))
    _mit_gegenprobe(
        "B-A2M", "Mutationsprobe 'stiller Hinweis zurueck' - B-A2 waere rot",
        lambda mut: _lauf("elliott_wave", ew_tage, T_KERZEN, B2_NEU, B2_ALT, mut),
        lambda r: r["rc"] == 0 and "hinweis" in r["out"], _info)

    # --- B3: loader_lesart erreicht den TypeError-Pfad nicht mehr --------------
    r = _lauf("rsi2_crypto", kein, T_LESART.format(bot="rsi2_crypto"))
    pruefe("B-A3: loader_lesart ohne Treffer endet in _min_history mit 2 (kein TypeError, rc 1)",
           _rc2(r, "_min_history") and "TypeError" not in r["err"], _info(r))
    _mit_gegenprobe(
        "B-A3M", "Mutationsprobe 're.search zurueck' - loader_lesart faellt wieder in den TypeError (rc 1)",
        lambda mut: _lauf("rsi2_crypto", kein, T_LESART.format(bot="rsi2_crypto"),
                          B1_NEU, B1_ALT, mut),
        lambda r: r["rc"] == 1 and "TypeError" in r["err"], _info)

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
