"""
Schritt 2: welche wirksamen Defaults sind Kopplungs-Kandidaten?
================================================================================
Baut auf default_scan.py auf und beantwortet die drei Fragen der Aufgabe
je wirksamem Default:

  1. Gibt es in live_params.py ueberhaupt ein Gegenstueck? (ggf. unter
     anderem Namen - siehe ALIASES)
  2. Wird der Parameter von einem Optimierungs-Skript absichtlich variiert?
     Dann darf er NICHT gekoppelt werden.
  3. Stimmt der aktuelle Wert mit dem Live-Wert ueberein - oder liegt eine
     echte Abweichung vor, die eine eigene Entscheidung braucht?

Ergebnis sind drei Listen:
  KANDIDAT       wirksam, nicht variiert, Live-Gegenstueck da, Wert gleich
                 -> auf Import umstellen, Regressionscheck muss identisch sein
  ABWEICHUNG     wie oben, aber Wert UNGLEICH -> nicht automatisch uebernehmen,
                 separat vorlegen
  KEIN GEGENSTUECK / VARIIERT   -> nur dokumentieren, Code nicht koppeln

WICHTIG - reine Untersuchung: veraendert keine Datei ausserhalb von
research/backtest_defaults/.

Nutzung:  python3 kandidaten.py [--json]
"""

import json
import os
import sys

from default_scan import BOTS, analysiere_bot, RESULTS_DIR

# Dieselbe Groesse unter unterschiedlichem Namen: Name im backtest-Modul
# -> Name in live_params.py. Ohne diese Tabelle waeren die Squeeze-Parameter
# unsichtbar, weil sie in live_params.py BB_* heissen.
ALIASES = {
    "SQUEEZE_LOOKBACK_DAYS": "BB_LOOKBACK",
    "SQUEEZE_PERCENTILE": "BB_SQUEEZE_PERCENTILE",
}

# Parameter, die keine Strategie-Einstellung sind, sondern den Datenausschnitt
# steuern (Beginn des ausgewerteten Zeitraums). Sie haben bewusst kein
# Gegenstueck in live_params.py.
KEIN_STRATEGIEPARAMETER = {"entry_cutoff"}


def live_name(konstante: str) -> str:
    return ALIASES.get(konstante, konstante)


def bewerte(zeile: dict, live_werte: dict) -> dict:
    p = zeile["parameter"]
    quelle = zeile["default_quelle"]

    # Bereits gekoppelt: der Default zeigt auf einen Namen, den das Modul
    # aus live_params.py importiert. Dann gibt es per Konstruktion keinen
    # zweiten Wert mehr, der auseinanderlaufen koennte - und modul_konstanten()
    # findet dafuer auch keine Zuweisung, was ohne diese Abfrage faelschlich
    # als "Wert None gegen Live-Wert X" gemeldet wuerde.
    if zeile.get("quelle_aus_live_params"):
        return {"urteil": "GEKOPPELT", "live_name": zeile["quelle_aus_live_params"],
                "wert": live_werte.get(zeile["quelle_aus_live_params"]),
                "live_wert": live_werte.get(zeile["quelle_aus_live_params"])}

    if p in KEIN_STRATEGIEPARAMETER:
        return {"urteil": "KEIN STRATEGIEPARAMETER",
                "grund": "steuert den Datenausschnitt, nicht die Strategie"}

    if zeile["variiert_in_suche"]:
        return {"urteil": "VARIIERT",
                "grund": "wird von einem Optimierungs-Skript absichtlich variiert",
                "stellen": zeile["ueberschrieben"].get("SUCHE")}

    # Ohne benannte Quelle (Literal direkt in der Signatur) gibt es nichts
    # zu koppeln, ausser der Name selbst faende sich in live_params.
    kandidat_name = live_name(quelle) if quelle else None
    if kandidat_name is None or kandidat_name not in live_werte:
        return {"urteil": "KEIN GEGENSTUECK",
                "grund": (f"'{quelle}' hat keinen Eintrag in live_params.py"
                           if quelle
                           else "Default ist ein Literal ohne benannte Konstante")}

    ist = zeile["quelle_wert"]
    soll = live_werte[kandidat_name]
    if ist == soll:
        return {"urteil": "KANDIDAT", "live_name": kandidat_name,
                "wert": ist, "live_wert": soll}
    return {"urteil": "ABWEICHUNG", "live_name": kandidat_name,
            "wert": ist, "live_wert": soll}


def main():
    ausgabe = []
    for bot in BOTS:
        eintrag = analysiere_bot(bot)
        live_werte = eintrag["live_werte"]
        for z in eintrag["parameter"]:
            if not z["wirksam_im_live_pfad"]:
                continue
            ausgabe.append({**z, **bewerte(z, live_werte)})

    reihenfolge = ["ABWEICHUNG", "KANDIDAT", "GEKOPPELT", "VARIIERT",
                   "KEIN GEGENSTUECK", "KEIN STRATEGIEPARAMETER"]
    for urteil in reihenfolge:
        treffer = [a for a in ausgabe if a["urteil"] == urteil]
        if not treffer:
            continue
        print(f"\n{'=' * 78}\n{urteil}  ({len(treffer)})\n{'=' * 78}")
        for a in treffer:
            kopf = (f"{a['bot']}/{a['datei']}  "
                    f"{a['funktion']}({a['parameter']})")
            print(kopf)
            if urteil == "GEKOPPELT":
                print(f"    kommt aus live_params.{a['live_name']} "
                      f"= {a['live_wert']!r}")
            elif urteil in ("KANDIDAT", "ABWEICHUNG"):
                print(f"    {a['default_quelle']} = {a['wert']!r}   "
                      f"live_params.{a['live_name']} = {a['live_wert']!r}")
            else:
                print(f"    {a.get('grund', '')}")
                if a.get("stellen"):
                    print(f"    variiert in: {', '.join(a['stellen'])}")
            print(f"    wirkt live in: {', '.join(a['wirkt_in']['LIVE'])}")

    print(f"\n{'=' * 78}")
    zaehler = {u: sum(1 for a in ausgabe if a["urteil"] == u) for u in reihenfolge}
    print("  ".join(f"{u}: {n}" for u, n in zaehler.items() if n))

    if "--json" in sys.argv:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        ziel = os.path.join(RESULTS_DIR, "kandidaten.json")
        with open(ziel, "w", encoding="utf-8") as f:
            json.dump(ausgabe, f, indent=2, ensure_ascii=False, default=str)
        print(f"geschrieben: {ziel}")


if __name__ == "__main__":
    main()
