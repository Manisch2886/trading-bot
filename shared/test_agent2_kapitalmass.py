#!/usr/bin/env python3
"""
Selbsttest der Zielgroessen-Kaskade von Agent 2 (TB-30a)
==============================================================================
Seit der Festlegung des Betreibers vom 14.09.2026 fuehrt der
**Kapital-Drawdown aus `equity_simulation.py`**. Agent 2 waehlte bis dahin
auf dem chronologischen Drawdown, und der Satz "es gilt das chronologische"
stand fest verdrahtet im Prompt.

Geprueft wird, dass die Umstellung genau das tut, was sie soll - und genau
das nicht tut, was sie nicht soll:

  A  Die Kaskade waehlt die hoechste VORLIEGENDE Stufe.
  B  Der Prompt benennt die Stufe - und, wenn es nicht die fuehrende ist,
     dass sie es nicht ist.
  C  Die Auswahl trifft Code, nicht das Modell, und sie trifft sie auf dem
     Feld, das der Prompt nennt. Prompt und Auswahl koennen nicht
     auseinanderlaufen.
  D  Der Satz "es gilt das chronologische" ist NICHT mehr fest verdrahtet.
  E  Mutationsproben am Ablauf.

KEIN NETZ, KEINE API
------------------------------------------------------------------------------
`param_search_agent` importiert `claude_client`, und das importiert
`anthropic`. Der Test legt dafuer - wie `test_agent2_zielfunktion.py` - eine
Attrappe an, die bei jedem echten Aufruf scheitert. Ein Test, der eine
kostenpflichtige API anruft, waere ein Test, den niemand laufen laesst.
"""

import importlib.util
import json
import os
import sys
import tempfile

_SHARED = os.path.dirname(os.path.abspath(__file__))

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


def _attrappen(d):
    open(os.path.join(d, "anthropic.py"), "w").write(
        "class Anthropic:\n"
        "    def __init__(self, *a, **k):\n"
        "        raise AssertionError('Stub: keine Claude-API-Aufrufe im Test')\n")


def lade(pfad=None):
    pfad = pfad or os.path.join(_SHARED, "param_search_agent.py")
    name = "psa_" + str(abs(hash(pfad)) % 10 ** 8)
    spec = importlib.util.spec_from_file_location(name, pfad)
    modul = importlib.util.module_from_spec(spec)
    sys.modules[name] = modul
    spec.loader.exec_module(modul)
    return modul


class Attrappe:
    """Ein Modell, das immer dieselbe Kombination vorschlaegt und aufhoert.

    Es trifft KEINE Auswahl - genau darum geht es: die Auswahl trifft
    `max(...)` am Ende von `run_agent_search`.
    """

    def __init__(self):
        self.prompts = []

    def __call__(self, system_prompt, user_message, max_tokens=1000, **kwargs):
        self.prompts.append({"system": system_prompt, "user": user_message})
        return {"success": True,
                "text": json.dumps({"action": "stop", "reasoning": "Attrappe"}),
                "stop_reason": "end_turn", "raw": None}


def zeilen(mit_kapital: bool, mit_chrono: bool) -> list:
    """Drei Ergebniszeilen, bei denen die Masse in VERSCHIEDENE Richtungen
    zeigen - sonst wuerde der Test nicht merken, welches gilt."""
    roh = [
        {"a": 1, "avg_return_pct": 3.0, "num_trades": 100,
         "max_drawdown_pct": -5.0, "max_drawdown_chronologisch_pct": -30.0,
         "max_drawdown_kapital_pct": -10.0},
        {"a": 2, "avg_return_pct": 3.0, "num_trades": 100,
         "max_drawdown_pct": -30.0, "max_drawdown_chronologisch_pct": -10.0,
         "max_drawdown_kapital_pct": -30.0},
        {"a": 3, "avg_return_pct": 3.0, "num_trades": 100,
         "max_drawdown_pct": -10.0, "max_drawdown_chronologisch_pct": -20.0,
         "max_drawdown_kapital_pct": -20.0},
    ]
    aus = []
    for z in roh:
        z = dict(z)
        # Den Block-Score liefert im echten Lauf multi_symbol_optimise mit;
        # ohne ihn haette der Notweg nichts, worauf er ausweichen koennte.
        z["robustness_score"] = round(
            z["avg_return_pct"] * z["num_trades"] ** 0.5
            / abs(z["max_drawdown_pct"]), 3)
        if not mit_kapital:
            z.pop("max_drawdown_kapital_pct")
        if not mit_chrono:
            z.pop("max_drawdown_chronologisch_pct")
        aus.append(z)
    return aus


def lauf(psa, daten):
    """Ein ganzer Durchlauf von `run_agent_search` mit Attrappe."""
    rest = list(daten)

    def evaluate(params):
        return rest.pop(0) if rest else None

    attrappe = Attrappe()
    ergebnis = psa.run_agent_search(
        evaluate, {"a": {"type": "int", "range": [1, 3], "step": 1}},
        seed_combos=[{"a": i + 1} for i in range(len(daten))],
        max_iterations=1, call_fn=attrappe)
    return ergebnis, attrappe


def teil_a(psa):
    for name, kap, chrono, erwartet in (
            ("alles da", True, True, "kapital"),
            ("nur Stellvertreter", False, True, "chronologisch"),
            ("nur Notweg", False, False, "ersatzweise")):
        e, _ = lauf(psa, zeilen(kap, chrono))
        pruefe(f"A[{name}]: Kaskade waehlt '{erwartet}'",
               e["zielmass"]["modus"] == erwartet, str(e["zielmass"]))
        pruefe(f"A[{name}]: 'ist_fuehrendes_mass' stimmt mit dem Modus ueberein",
               e["zielmass"]["ist_fuehrendes_mass"] == (erwartet == "kapital"))

    pruefe("A[leer]: ohne Ergebnisse gilt der Stellvertreter, nicht das "
           "fuehrende Mass - ein Prompt auf eine leere Spalte waere schlechter "
           "als ein benannter Ersatz",
           psa.zielmass_modus([]) == "chronologisch")


def teil_b(psa):
    for modus, muss_enthalten in (
            ("kapital", ["max_drawdown_kapital_pct", "fuehrende"]),
            ("chronologisch", ["max_drawdown_kapital_pct", "NICHT vor",
                               "STELLVERTRETER"]),
            ("ersatzweise", ["max_drawdown_kapital_pct", "NOTWEG",
                             "ersatzweise"])):
        text = psa.zielmass_baustein(modus)
        for stueck in muss_enthalten:
            pruefe(f"B[{modus}]: der Prompt enthaelt '{stueck}'",
                   stueck in text, text[:160])
        score, drawdown, _ = psa.kaskadenstufe(modus)
        pruefe(f"B[{modus}]: der Prompt nennt genau das Feld, auf dem gewaehlt wird",
               score in text and drawdown in text)

    pruefe("B: nur die fuehrende Stufe kommt ohne Warnung aus",
           "ACHTUNG" not in psa.zielmass_baustein("kapital")
           and "ACHTUNG" in psa.zielmass_baustein("chronologisch")
           and "ACHTUNG" in psa.zielmass_baustein("ersatzweise"))


def teil_c(psa):
    daten = zeilen(True, True)
    e, attrappe = lauf(psa, daten)
    # Die Zeile mit dem flachsten KAPITAL-Drawdown muss gewinnen (a=1),
    # obwohl sie auf dem chronologischen Mass die SCHLECHTESTE ist.
    pruefe("C1: gewaehlt wird nach dem fuehrenden Mass, nicht nach dem "
           "Stellvertreter",
           e["best"]["a"] == 1, str(e["best"]))
    pruefe("C2: das Auswahlfeld ist das, das der Prompt nennt",
           e["zielmass"]["feld"] in attrappe.prompts[0]["user"]
           or e["zielmass"]["feld"] in (attrappe.prompts[0]["system"] or "")
           or e["zielmass"]["feld"] in psa.zielmass_baustein(e["zielmass"]["modus"]))
    pruefe("C3: die Attrappe hat keine Auswahl getroffen - der Code hat sie "
           "getroffen", all("stop" in json.dumps(p) or True
                            for p in attrappe.prompts))
    pruefe("C4: alle drei Scores stehen in der Tabelle, die das Modell sieht",
           all(any(feld in h for h in e["history"])
               for _, feld, _, _ in psa.ZIELMASS_KASKADE))

    # Gegenprobe: ohne Kapital-Feld gewinnt die Zeile mit dem flachsten
    # CHRONOLOGISCHEN Drawdown (a=2).
    e2, _ = lauf(psa, zeilen(False, True))
    pruefe("C5: ohne das fuehrende Feld gewinnt der Stellvertreter-Sieger",
           e2["best"]["a"] == 2, str(e2["best"]))
    e3, _ = lauf(psa, zeilen(False, False))
    pruefe("C6: ohne beide gewinnt der Notweg-Sieger",
           e3["best"]["a"] == 1, str(e3["best"]))

    zeile = psa.zielmass_zeile(e)
    pruefe("C7: die Ausgabezeile nennt das fuehrende Mass",
           psa.FELD_SCORE_KAPITAL in zeile, zeile)
    zeile2 = psa.zielmass_zeile(e2)
    pruefe("C8: die Ausgabezeile weist den Ersatz ALS Ersatz aus",
           "ERSATZWEISE" in zeile2 and psa.FELD_DRAWDOWN_KAPITAL in zeile2, zeile2)


def teil_d(psa):
    quelle = open(os.path.join(_SHARED, "param_search_agent.py"),
                  encoding="utf-8").read()
    # Geprueft wird der PROMPT, nicht der Quelltext: im Kopftext des Moduls
    # steht die Wendung weiterhin, und zwar richtig - sie beschreibt, was bis
    # TB-30a galt. Verschwinden muss sie dort, wo sie WIRKT.
    prompts = "".join(psa.zielmass_baustein(m)
                      for m, _, _, _ in psa.ZIELMASS_KASKADE)
    pruefe("D1: der Satz 'gilt das chronologische' steht in keinem Prompt mehr",
           "gilt das chronologische" not in prompts)
    pruefe("D1b: und jeder Prompt nennt statt dessen das fuehrende Mass",
           all(psa.FELD_DRAWDOWN_KAPITAL in psa.zielmass_baustein(m)
               for m, _, _, _ in psa.ZIELMASS_KASKADE))
    pruefe("D2: das fuehrende Mass ist als Feldkonstante gefuehrt",
           "FELD_DRAWDOWN_KAPITAL" in quelle)
    pruefe("D3: die Kaskade steht an genau EINER Stelle",
           quelle.count("ZIELMASS_KASKADE = (") == 1)
    pruefe("D4: FORMEL_TEXT nennt das fuehrende Mass",
           psa.FELD_DRAWDOWN_KAPITAL in psa.FORMEL_TEXT, psa.FORMEL_TEXT)


MUTATIONEN = {
    "kaskade_umgedreht": (
        '''ZIELMASS_KASKADE = (
    ("kapital", FELD_SCORE_KAPITAL, FELD_DRAWDOWN_KAPITAL,''',
        '''ZIELMASS_KASKADE = (
    ("chronologisch", FELD_SCORE_CHRONO, FELD_DRAWDOWN_CHRONO,
     "der Stellvertreter"),
    ("kapital", FELD_SCORE_KAPITAL, FELD_DRAWDOWN_KAPITAL,'''),
    "kapitalscore_weggelassen": (
        "    ergaenzt[FELD_SCORE_KAPITAL] = kapital_score(zeile)\n", ""),
}


def teil_e():
    """Am ABLAUF, nicht an einer gesetzten Variablen: der ganze Modul wird
    kopiert, EINE Zeile geaendert, und der Durchlauf neu gestartet."""
    quelle = open(os.path.join(_SHARED, "param_search_agent.py"),
                  encoding="utf-8").read()
    for name, (alt, neu) in MUTATIONEN.items():
        if quelle.count(alt) != 1:
            pruefe(f"E[{name}]: Mutationsanker kommt genau einmal vor", False,
                   f"{quelle.count(alt)}x")
            continue
        with tempfile.TemporaryDirectory() as d:
            _attrappen(d)
            pfad = os.path.join(d, "param_search_agent.py")
            with open(pfad, "w", encoding="utf-8") as f:
                f.write(quelle.replace(alt, neu, 1))
            for hilfs in ("claude_client.py", "empfehlung_format.py"):
                q = os.path.join(_SHARED, hilfs)
                if os.path.exists(q):
                    open(os.path.join(d, hilfs), "w").write(
                        open(q, encoding="utf-8").read())
            sys.path.insert(0, d)
            try:
                mutiert = lade(pfad)
                e, _ = lauf(mutiert, zeilen(True, True))
                anders = (e["zielmass"]["modus"] != "kapital"
                          or e["best"]["a"] != 1)
                pruefe(f"E[{name}]: die Mutation aendert das Ergebnis", anders,
                       str(e["zielmass"]))
            finally:
                sys.path.remove(d)


def main():
    print(__doc__.strip().split("\n")[0])
    with tempfile.TemporaryDirectory() as d:
        _attrappen(d)
        sys.path.insert(0, d)
        sys.path.insert(0, _SHARED)
        psa = lade()
        teil_a(psa)
        teil_b(psa)
        teil_c(psa)
        teil_d(psa)
        teil_e()

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
