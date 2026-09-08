"""
Selbsttests zur Default-Analyse und zur Kopplung
================================================================================
Zwei Arten von Pruefungen:

  A) DAS WERKZEUG. Kuenstliche Mini-Projekte in einem temporaeren Ordner,
     bei denen die richtige Antwort vorher feststeht. Sie sichern genau die
     Unterscheidungen ab, an denen eine naive Umsetzung scheitert:
     Positions-Argumente zaehlen als Ueberschreibung, Kommentare nicht,
     der Live-Pfad ist transitiv, **kwargs ist statisch nicht entscheidbar.
  B) DAS ERGEBNIS IM REPO. Dass die neun umgestellten Konstanten wirklich
     aus live_params.py kommen und dass keine Datei angefasst wurde, die
     diese Aufgabe nicht anfassen darf.

Nutzung:  python3 test_backtest_defaults.py
"""

import ast
import os
import shutil
import sys
import tempfile

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import default_scan
import konstanten_scan
from default_scan import STRATEGIES, Datei, live_params_importe, modul_konstanten
from kandidaten import ALIASES, bewerte

_bestanden = 0
_fehler = []


def check(name, ok, detail=""):
    global _bestanden
    if ok:
        _bestanden += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        _fehler.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# A) Das Werkzeug an kuenstlichen Faellen
# ---------------------------------------------------------------------------

def baue_bot(wurzel: str, name: str, dateien: dict) -> str:
    ordner = os.path.join(wurzel, name)
    os.makedirs(ordner, exist_ok=True)
    for datei, inhalt in dateien.items():
        with open(os.path.join(ordner, datei), "w", encoding="utf-8") as f:
            f.write(inhalt)
    return ordner


def analysiere(wurzel: str, name: str) -> list:
    """analysiere_bot() gegen das Testprojekt statt gegen strategies/."""
    alt = default_scan.STRATEGIES
    default_scan.STRATEGIES = wurzel
    try:
        return default_scan.analysiere_bot(name)["parameter"]
    finally:
        default_scan.STRATEGIES = alt


def finde(zeilen, funktion, parameter):
    for z in zeilen:
        if z["funktion"] == funktion and z["parameter"] == parameter:
            return z
    return None


def teste_werkzeug():
    print("\n1) Das Werkzeug an kuenstlichen Faellen")
    wurzel = tempfile.mkdtemp(prefix="defaults_test_")
    try:
        # --- Fall 1: Positions-Argument, Schluesselwort, Kommentar ---------
        baue_bot(wurzel, "fall_positional", {
            "live_params.py": "A = 1\nB = 2\nC = 3\n",
            "backtest_x.py": (
                "A = 1\nB = 2\nC = 3\n"
                "def run(df, a=A, b=B, c=C):\n"
                "    return df\n"),
            "equity_simulation.py": (
                "from backtest_x import run\n"
                "# Achtung: run(df, 9, b=9, c=9) im Kommentar zaehlt NICHT\n"
                "def los(df):\n"
                "    return run(df, 5, b=7)\n"),
        })
        z = analysiere(wurzel, "fall_positional")
        check("Positions-Argument zaehlt als Ueberschreibung",
              finde(z, "run", "a")["ueberschrieben"].get("LIVE") is not None
              and not finde(z, "run", "a")["wirksam_im_live_pfad"])
        check("Schluesselwort-Argument zaehlt als Ueberschreibung",
              not finde(z, "run", "b")["wirksam_im_live_pfad"])
        check("Nicht uebergebener Parameter wirkt ueber den Default",
              finde(z, "run", "c")["wirksam_im_live_pfad"],
              detail=str(finde(z, "run", "c")["wirkt_in"]))
        check("Ein Aufruf im KOMMENTAR aendert nichts",
              finde(z, "run", "c")["wirksam_im_live_pfad"])

        # --- Fall 2: Live-Pfad ist transitiv -------------------------------
        # Der eigentliche run()-Aufruf steht in einer Datei, die dem Namen
        # nach Grid-Search ist. Genau so liegt der Fall bei allen echten
        # Bots (multi_symbol_optimise.get_trades_for_symbol).
        baue_bot(wurzel, "fall_transitiv", {
            "live_params.py": "A = 1\n",
            "backtest_x.py": "A = 1\ndef run(df, a=A):\n    return df\n",
            "multi_symbol_optimise.py": (
                "from backtest_x import run\n"
                "def get_trades_for_symbol(df):\n"
                "    return run(df)\n"
                "def evaluate(df, a):\n"
                "    return run(df, a=a)\n"),
            "equity_simulation.py": (
                "from multi_symbol_optimise import get_trades_for_symbol\n"
                "def los(df):\n"
                "    return get_trades_for_symbol(df)\n"),
        })
        z = analysiere(wurzel, "fall_transitiv")
        eintrag = finde(z, "run", "a")
        check("Live-Pfad wird transitiv erkannt (ueber eine Suchdatei hinweg)",
              eintrag["wirksam_im_live_pfad"], detail=str(eintrag["wirkt_in"]))
        check("Die daneben stehende Suchfunktion gilt NICHT als Live-Pfad",
              eintrag["ueberschrieben"].get("LIVE") is None
              and eintrag["ueberschrieben"].get("SUCHE") is not None)

        # --- Fall 3: **kwargs ist nicht entscheidbar -----------------------
        baue_bot(wurzel, "fall_kwargs", {
            "live_params.py": "A = 1\n",
            "backtest_x.py": "A = 1\ndef run(df, a=A):\n    return df\n",
            "equity_simulation.py": (
                "from backtest_x import run\n"
                "def los(df, a=None):\n"
                "    kw = {} if a is None else {'a': a}\n"
                "    return run(df, **kw)\n"),
        })
        z = analysiere(wurzel, "fall_kwargs")
        check("**kwargs-Aufrufstelle wird als unklar gemeldet, nicht "
              "stillschweigend entschieden",
              bool(finde(z, "run", "a")["unklar_wegen_sternchen"]))

        # --- Fall 4: Alias-Aufloesung und Wertevergleich --------------------
        baue_bot(wurzel, "fall_alias", {
            "live_params.py": "BB_LOOKBACK = 126\n",
            "backtest_x.py": ("SQUEEZE_LOOKBACK_DAYS = 126\n"
                               "def run(df, squeeze_lookback_days=SQUEEZE_LOOKBACK_DAYS):\n"
                               "    return df\n"),
            "equity_simulation.py": ("from backtest_x import run\n"
                                      "def los(df):\n    return run(df)\n"),
        })
        z = analysiere(wurzel, "fall_alias")
        urteil = bewerte(finde(z, "run", "squeeze_lookback_days"),
                          {"BB_LOOKBACK": 126})
        check("Alias SQUEEZE_LOOKBACK_DAYS -> BB_LOOKBACK wird aufgeloest",
              urteil["urteil"] == "KANDIDAT", detail=urteil["urteil"])
        urteil = bewerte(finde(z, "run", "squeeze_lookback_days"),
                          {"BB_LOOKBACK": 99})
        check("Ein abweichender Wert wird als ABWEICHUNG gemeldet, nicht "
              "als Kandidat",
              urteil["urteil"] == "ABWEICHUNG", detail=urteil["urteil"])

        # --- Fall 5: Monkey Patching macht ein Modul-Literal folgenlos -----
        baue_bot(wurzel, "fall_patch", {
            "live_params.py": "TAKE_PROFIT_FIB = 0.236\n",
            "backtest_x.py": ("TAKE_PROFIT_FIB = 0.382\n"
                               "def run(df):\n"
                               "    return df * TAKE_PROFIT_FIB\n"),
            "equity_simulation.py": ("import backtest_x\n"
                                      "from live_params import TAKE_PROFIT_FIB\n"
                                      "def los(df):\n"
                                      "    backtest_x.TAKE_PROFIT_FIB = TAKE_PROFIT_FIB\n"
                                      "    return backtest_x.run(df)\n"),
        })
        ordner = os.path.join(wurzel, "fall_patch")
        dateien = {n: Datei(ordner, n)
                    for n in sorted(os.listdir(ordner)) if n.endswith(".py")}
        patches = konstanten_scan._patches(ordner, dateien)
        check("Zuweisung 'modul.KONSTANTE = ...' wird gefunden",
              any(p["modul"] == "backtest_x.py"
                  and p["konstante"] == "TAKE_PROFIT_FIB"
                  and p["datei"] == "equity_simulation.py" for p in patches),
              detail=str(patches))
        leser = konstanten_scan._funktions_leser(dateien["backtest_x.py"],
                                                  {"TAKE_PROFIT_FIB"})
        check("Ein im Rumpf gelesener Modulwert wird erkannt (das sieht ein "
              "reiner Default-Scan nicht)",
              leser.get("TAKE_PROFIT_FIB") == {"run"}, detail=str(leser))

        # --- Fall 6: Default in der Signatur ist KEIN Rumpf-Lesezugriff ----
        baue_bot(wurzel, "fall_signatur", {
            "live_params.py": "A = 1\n",
            "backtest_x.py": "A = 1\ndef run(df, a=A):\n    return df + a\n",
            "equity_simulation.py": ("from backtest_x import run\n"
                                      "def los(df):\n    return run(df)\n"),
        })
        ordner = os.path.join(wurzel, "fall_signatur")
        datei = Datei(ordner, "backtest_x.py")
        check("Ein Default in der Signatur zaehlt NICHT als Rumpf-Lesezugriff",
              "A" not in konstanten_scan._funktions_leser(datei, {"A"}))
    finally:
        shutil.rmtree(wurzel, ignore_errors=True)


# ---------------------------------------------------------------------------
# B) Das Ergebnis im Repo
# ---------------------------------------------------------------------------

# Die neun Konstanten, die diese Aenderung gekoppelt hat:
# (Bot, Modul, Name im Modul, Name in live_params.py)
GEKOPPELT = [
    ("rsi2_mean_reversion", "backtest_rsi2.py", "MAX_HOLD_DAYS", "MAX_HOLD_DAYS"),
    ("turtle_soup_crypto", "backtest_turtle_soup.py", "MAX_HOLD_DAYS", "MAX_HOLD_DAYS"),
    ("turtle_soup_stocks", "backtest_turtle_soup.py", "MAX_HOLD_DAYS", "MAX_HOLD_DAYS"),
    ("volatility_breakout", "backtest_breakout.py", "MAX_HOLD_DAYS", "MAX_HOLD_DAYS"),
    ("volatility_breakout", "backtest_breakout.py", "SQUEEZE_LOOKBACK_DAYS", "BB_LOOKBACK"),
    ("volatility_breakout", "backtest_breakout.py", "SQUEEZE_PERCENTILE", "BB_SQUEEZE_PERCENTILE"),
    ("volatility_breakout_crypto", "backtest_breakout.py", "MAX_HOLD_DAYS", "MAX_HOLD_DAYS"),
    ("volatility_breakout_crypto", "backtest_breakout.py", "SQUEEZE_LOOKBACK_DAYS", "BB_LOOKBACK"),
    ("volatility_breakout_crypto", "backtest_breakout.py", "SQUEEZE_PERCENTILE", "BB_SQUEEZE_PERCENTILE"),
]

# Bewusst NICHT gekoppelt, weil ein Optimierungs-Skript sie variiert.
NICHT_GEKOPPELT = [
    ("turtle_soup_crypto", "backtest_turtle_soup.py", "DONCHIAN_PERIOD"),
    ("turtle_soup_stocks", "backtest_turtle_soup.py", "DONCHIAN_PERIOD"),
    ("t3_supertrend", "backtest_trend.py", "T3_FAST_LENGTH"),
    ("t3_supertrend", "backtest_trend.py", "T3_SLOW_LENGTH"),
    ("t3_supertrend", "backtest_trend.py", "ADX_THRESHOLD"),
    ("t3_supertrend", "backtest_trend.py", "STOP_LOSS_PCT"),
    ("elliott_wave", "backtest_elliott.py", "STOP_LOSS_PCT"),
    ("elliott_wave", "backtest_elliott.py", "TAKE_PROFIT_FIB"),
    ("elliott_wave_stocks", "backtest_elliott.py", "STOP_LOSS_PCT"),
    ("elliott_wave_stocks", "backtest_elliott.py", "TAKE_PROFIT_FIB"),
]


def teste_repo():
    print("\n2) Das Ergebnis im Repo")

    for bot, modul, name, live in GEKOPPELT:
        pfad = os.path.join(STRATEGIES, bot, modul)
        importe = live_params_importe(pfad)
        check(f"{bot}/{modul}: {name} kommt aus live_params.{live}",
              importe.get(name) == live, detail=str(importe.get(name)))
        check(f"{bot}/{modul}: {name} steht NICHT mehr als eigene Zahl da",
              name not in modul_konstanten(pfad))

    for bot, modul, name in NICHT_GEKOPPELT:
        pfad = os.path.join(STRATEGIES, bot, modul)
        check(f"{bot}/{modul}: {name} bleibt bewusst eine eigene Konstante",
              name in modul_konstanten(pfad)
              and name not in live_params_importe(pfad))

    # Kein Importzyklus: live_params.py darf selbst nichts aus dem Bot holen.
    for bot in default_scan.BOTS:
        pfad = os.path.join(STRATEGIES, bot, "live_params.py")
        with open(pfad, encoding="utf-8") as f:
            baum = ast.parse(f.read())
        importe = [k for k in ast.walk(baum)
                    if isinstance(k, (ast.Import, ast.ImportFrom))]
        check(f"{bot}/live_params.py importiert nichts (kein Importzyklus)",
              not importe)

    # Die betroffenen backtest-Module muessen weiterhin einzeln ladbar sein.
    for bot, modul, _, _ in GEKOPPELT:
        pfad = os.path.join(STRATEGIES, bot, modul)
        with open(pfad, encoding="utf-8") as f:
            try:
                ast.parse(f.read(), filename=pfad)
                ok, detail = True, ""
            except SyntaxError as e:
                ok, detail = False, str(e)
        check(f"{bot}/{modul} ist syntaktisch gueltig", ok, detail)


def teste_keine_offenen_faelle():
    print("\n3) Keine offenen Faelle mehr")
    from kandidaten import bewerte as _bewerte
    offen = []
    for bot in default_scan.BOTS:
        eintrag = default_scan.analysiere_bot(bot)
        for z in eintrag["parameter"]:
            if not z["wirksam_im_live_pfad"]:
                continue
            urteil = _bewerte(z, eintrag["live_werte"])["urteil"]
            if urteil in ("KANDIDAT", "ABWEICHUNG"):
                offen.append(f"{bot}/{z['datei']}:{z['funktion']}"
                              f"({z['parameter']}) -> {urteil}")
    check("Kein wirksamer Default ist mehr Kandidat oder Abweichung",
          not offen, detail="; ".join(offen))


def main():
    print("Selbsttests: backtest-Defaults und Kopplung an live_params.py")
    teste_werkzeug()
    teste_repo()
    teste_keine_offenen_faelle()

    print(f"\n{_bestanden}/{_bestanden + len(_fehler)} Pruefungen bestanden.")
    for name in _fehler:
        print(f"FEHLGESCHLAGEN: {name}")
    sys.exit(1 if _fehler else 0)


if __name__ == "__main__":
    main()
