#!/usr/bin/env python3
"""
Das Geruest von `shared/fetch_binance_data.py` aus den Aufrufern (TB-37)
==============================================================================
`research/abrufskripte/abrufwege.py` (TB-35) hat gezaehlt, **wer** an der
gitignorierten Datei haengt. Diese Untersuchung fragt das Naechste: **Was
genau** muss der versionierte Teil koennen, damit **kein einziger Aufrufer
angefasst werden muss**?

Der Unterschied ist die Aufrufstelle. TB-35 notierte "Zeile 208: ein Aufruf".
Fuer einen Ersatz genuegt das nicht - gebraucht wird, **womit** aufgerufen
wird: drei Argumente oder zwei? Benannt oder der Reihe nach? Welcher Wert
steht hinter `INTERVAL`, welcher hinter `LOOKBACK`?

Deshalb loest diese Untersuchung die Namen auf: Wo ein Aufruf `INTERVAL`
uebergibt und das Modul weiter oben `INTERVAL = Client.KLINE_INTERVAL_1DAY`
zuweist, steht hier `'1d'` - der Wert, der wirklich ankommt. Die
`KLINE_INTERVAL_*` von `python-binance` sind schlichte Zeichenketten; die
Zuordnung steht unten in `KLINE_INTERVALLE` und wird, wenn `binance`
installiert ist, gegen das Paket selbst nachgeprueft statt geglaubt.

Gesucht wird ueber den **Syntaxbaum**, nicht mit Textsuche: ein Name in einem
Kommentar oder einer Zeichenkette soll nicht mitzaehlen. Gleiches Vorgehen
wie in `research/kursdaten_neuaufbau/datenwege.py` und
`research/abrufskripte/abrufwege.py`.

Was die Untersuchung feststellt
------------------------------------------------------------------------------
1. **Wer sie einbindet** - Modul, Zeile, importierter Name.
2. **Womit aufgerufen wird** - je Aufrufstelle die Argumente, so weit im
   Modul aufloesbar, sonst als Ausdruck im Quelltext.
3. **Welche Signatur daraus folgt** - die kleinste, die alle Aufrufe bedient.
4. **Was am Ergebnis benutzt wird** - Spalten, `.iloc[-1]`, `to_csv`.
5. **Was NICHT erschliessbar ist** - ausdruecklich als `unbekannt` benannt,
   nicht vermutet. Die Quelle liegt ausserhalb des Repos.

Die Untersuchung aendert nichts, fasst keinen Bot-Code an und **importiert
keine Bot-Datei** (neun gleichnamige `forward_test.py` kollidieren in
`sys.modules`) - sie liest Text und zerlegt ihn. Sie braucht nur die
Standardbibliothek; `pandas` und `binance` sind nicht noetig.
Rueckgabewert 0 - sie ist ein Bericht, kein Waechter.

    python3 research/zugangsdaten/geruest.py
    python3 research/zugangsdaten/geruest.py --json daten/geruest.json
"""

import argparse
import ast
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))

ORDNER = ["shared", "strategies", "research", "dashboard", "notifications",
          "broker", "system", "config"]

MODUL = "fetch_binance_data"
FUNKTION = "fetch_historical_data"

# Die `KLINE_INTERVAL_*` von python-binance sind Zeichenketten-Konstanten.
# Nur die drei, die dieses Projekt benutzt - taucht eine vierte auf, bleibt
# sie als Ausdruck stehen und faellt dadurch auf, statt still falsch zu sein.
KLINE_INTERVALLE = {
    "KLINE_INTERVAL_1HOUR": "1h",
    "KLINE_INTERVAL_4HOUR": "4h",
    "KLINE_INTERVAL_1DAY": "1d",
}

# Spaltennamen, die in den Kursdateien dieses Repos stehen, plus der eine,
# der dort NICHT steht (`close_time`) - sein Fehlen ist der Befund.
KURSSPALTEN = ["open_time", "open", "high", "low", "close", "volume",
               "close_time"]

# Was sich aus den Aufrufern **nicht** ablesen laesst. Genau diese Liste ist
# der Grund, warum der Schnitt am Mac stattfinden muss und nicht hier.
UNBEKANNT = [
    ("Ratenbegrenzung", "Ob und wie die alte Datei drosselt. Die Aufrufer "
                        "pausieren teils selbst (fetch_multi_data.py: "
                        "PAUSE_BETWEEN_REQUESTS_SEC = 0.5) - daraus folgt "
                        "weder, dass die Datei drosselt, noch dass sie es "
                        "nicht tut."),
    ("Wiederholversuche", "Ob sie bei HTTP 429/418 oder Netzfehlern "
                          "wiederholt. Kein Aufrufer verlaesst sich sichtbar "
                          "darauf; alle neun fangen breit ab."),
    ("Zeitzone", "Ob sie UTC-naiv oder zonenbehaftet zurueckgibt. Die "
                 "Kursdateien sind UTC-naiv geschrieben; ob die Umrechnung "
                 "in der Datei oder erst in to_csv passiert, steht nicht in "
                 "den Aufrufern."),
    ("Schluesselnutzung", "Ob die enthaltenen Zugangsdaten fuer den "
                          "Kursabruf ueberhaupt gebraucht werden. Der "
                          "oeffentliche Endpunkt verlangt keinen Schluessel, "
                          "und zwei Nachbarmodule im Repo bauen ihren Client "
                          "ohne (get_top_symbols.py:15, "
                          "fetch_multi_data.py:46) - bewiesen ist damit "
                          "nichts ueber die gitignorierte Datei."),
    ("Fehlerverhalten", "Was sie bei einem unbekannten Symbol tut: werfen "
                        "oder eine leere Tabelle. Alle neun Aufrufer fangen "
                        "`Exception` ab und machen mit dem naechsten Symbol "
                        "weiter - beide Verhalten sehen von aussen gleich "
                        "aus."),
]


def _quelle(knoten, text):
    return (ast.get_source_segment(text, knoten) or "").strip()


def _modulkonstanten(baum, text):
    """Zuweisungen auf Modulebene: Name -> aufgeloester Wert oder Ausdruck.

    Nur die oberste Ebene. Eine Zuweisung in einer Funktion koennte je Aufruf
    anders lauten; sie hier mitzunehmen hiesse, einen von mehreren moeglichen
    Werten als DEN Wert auszugeben.
    """
    werte = {}
    for knoten in baum.body:
        if not isinstance(knoten, ast.Assign):
            continue
        for ziel in knoten.targets:
            if not isinstance(ziel, ast.Name):
                continue
            werte[ziel.id] = _wert(knoten.value, text)
    return werte


def _wert(knoten, text):
    """Ein Ausdruck als Wert, wenn er sich ohne Ausfuehren bestimmen laesst."""
    if isinstance(knoten, ast.Constant):
        return {"art": "literal", "wert": knoten.value}
    if (isinstance(knoten, ast.Attribute)
            and knoten.attr in KLINE_INTERVALLE):
        return {"art": "kline-konstante",
                "wert": KLINE_INTERVALLE[knoten.attr],
                "ausdruck": _quelle(knoten, text)}
    return {"art": "ausdruck", "wert": None, "ausdruck": _quelle(knoten, text)}


def _argument(knoten, text, konstanten):
    """Ein Aufrufargument: sein Quelltext und, wenn moeglich, sein Wert."""
    if isinstance(knoten, ast.Name) and knoten.id in konstanten:
        aufgeloest = dict(konstanten[knoten.id])
        aufgeloest["name"] = knoten.id
        aufgeloest["ausdruck"] = knoten.id
        return aufgeloest
    return _wert(knoten, text)


def untersuche(pfad, text=None):
    if text is None:
        with open(pfad, "r", encoding="utf-8") as datei:
            text = datei.read()
    try:
        baum = ast.parse(text)
    except SyntaxError:
        return None

    # 1. Bindet das Modul die gitignorierte Datei ueberhaupt ein?
    bindet_ein = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.ImportFrom) and (knoten.module or "").endswith(MODUL):
            for eintrag in knoten.names:
                bindet_ein.append({"zeile": knoten.lineno,
                                   "form": f"from {knoten.module} import "
                                           f"{eintrag.name}",
                                   "name": eintrag.asname or eintrag.name})
        elif isinstance(knoten, ast.Import):
            for eintrag in knoten.names:
                if eintrag.name.endswith(MODUL):
                    bindet_ein.append({"zeile": knoten.lineno,
                                       "form": f"import {eintrag.name}",
                                       "name": eintrag.asname or eintrag.name})
    if not bindet_ein:
        return None

    konstanten = _modulkonstanten(baum, text)
    gebunden = {e["name"] for e in bindet_ein}

    # 2. Die Aufrufstellen - mit Argumenten, nicht nur mit Zeilennummer.
    aufrufe = []
    for knoten in ast.walk(baum):
        if not isinstance(knoten, ast.Call):
            continue
        name = (knoten.func.attr if isinstance(knoten.func, ast.Attribute)
                else getattr(knoten.func, "id", ""))
        if name != FUNKTION and name not in gebunden:
            continue
        if name != FUNKTION:
            continue
        aufrufe.append({
            "zeile": knoten.lineno,
            "quelle": _quelle(knoten, text),
            "stellung": [_argument(a, text, konstanten) for a in knoten.args],
            "benannt": {schluessel.arg: _argument(schluessel.value, text,
                                                  konstanten)
                        for schluessel in knoten.keywords
                        if schluessel.arg},
            "stern": any(schluessel.arg is None for schluessel in knoten.keywords)
                     or any(isinstance(a, ast.Starred) for a in knoten.args),
        })

    # 3. Was mit dem Ergebnis geschieht.
    spalten = sorted({k.value for k in ast.walk(baum)
                      if isinstance(k, ast.Constant)
                      and isinstance(k.value, str)
                      and k.value in KURSSPALTEN})
    schreibt_csv = sorted({k.lineno for k in ast.walk(baum)
                           if isinstance(k, ast.Call)
                           and isinstance(k.func, ast.Attribute)
                           and k.func.attr == "to_csv"})
    letzte_kerze = sorted({k.lineno for k in ast.walk(baum)
                           if isinstance(k, ast.Subscript)
                           and isinstance(k.value, ast.Attribute)
                           and k.value.attr == "iloc"
                           and _quelle(k.slice, text) in ("-1", "- 1")})

    return {"bindet_ein": sorted(bindet_ein, key=lambda e: e["zeile"]),
            "aufrufe": sorted(aufrufe, key=lambda a: a["zeile"]),
            "spalten": spalten,
            "schreibt_csv": schreibt_csv,
            "letzte_kerze": letzte_kerze}


def ist_selbsttest(rel):
    """Ein `test_*.py` ist ein Selbsttest, kein Aufrufer im Betrieb.

    Der Unterschied ist nicht kosmetisch: die Zahl **neun** meint die
    Module, an denen der Betrieb haengt. Ein Selbsttest, der dieselbe Datei
    einbindet, um sie zu pruefen, gehoert nicht dazu - wuerde er
    mitgezaehlt, stiege die Zahl bei jedem neuen Test, ohne dass ein Bot
    mehr an ihr haengt. Verschwiegen wird er trotzdem nicht: er steht im
    Bericht unter "Selbsttests".
    """
    return os.path.basename(rel).startswith("test_")


def sammle(wurzel=_WURZEL, nur_betrieb=True):
    """Alle Module, die `fetch_binance_data` einbinden.

    `nur_betrieb=True` laesst die Selbsttests weg - das ist die Sicht, aus
    der die Zahl neun stammt. `sammle(..., nur_betrieb=False)` liefert
    beides.
    """
    befunde = {}
    for teil in ORDNER:
        ordner = os.path.join(wurzel, teil)
        if not os.path.isdir(ordner):
            continue
        for pfad, _, dateien in os.walk(ordner):
            if "__pycache__" in pfad:
                continue
            for name in sorted(dateien):
                if not name.endswith(".py"):
                    continue
                voll = os.path.join(pfad, name)
                rel = os.path.relpath(voll, wurzel)
                if nur_betrieb and ist_selbsttest(rel):
                    continue
                ergebnis = untersuche(voll)
                if ergebnis:
                    befunde[rel] = ergebnis
    return befunde


def signatur(befunde):
    """Die kleinste Signatur, die alle gefundenen Aufrufe bedient."""
    alle = [a for e in befunde.values() for a in e["aufrufe"]]
    if not alle:
        return {"stellung": 0, "benannt": [], "stern": False, "aufrufe": 0}
    return {
        "stellung": max(len(a["stellung"]) for a in alle),
        "mindestens": min(len(a["stellung"]) for a in alle),
        "benannt": sorted({s for a in alle for s in a["benannt"]}),
        "stern": any(a["stern"] for a in alle),
        "aufrufe": len(alle),
    }


def werte_je_stelle(befunde):
    """Welche Werte kommen an welcher Argumentstelle wirklich an?"""
    stellen = {}
    for pfad, eintrag in sorted(befunde.items()):
        for aufruf in eintrag["aufrufe"]:
            for nummer, argument in enumerate(aufruf["stellung"]):
                eintraege = stellen.setdefault(nummer, [])
                eintraege.append({
                    "modul": pfad, "zeile": aufruf["zeile"],
                    "ausdruck": argument.get("ausdruck")
                                or repr(argument.get("wert")),
                    "wert": argument.get("wert"),
                    "art": argument["art"],
                })
    return stellen


def _pruefe_kline_konstanten():
    """Die Zuordnung KLINE_INTERVAL_* -> '1h'/'4h'/'1d' nachrechnen.

    Steht `binance` zur Verfuegung, wird gegen das Paket geprueft statt der
    Tabelle oben zu glauben. Fehlt es (Cloud), sagt der Bericht das - eine
    ungeprueft uebernommene Zuordnung soll nicht wie eine gepruefte aussehen.
    """
    try:
        from binance.client import Client                   # noqa: PLC0415
    except Exception:                                       # noqa: BLE001
        return None
    abweichungen = []
    for name, erwartet in sorted(KLINE_INTERVALLE.items()):
        tatsaechlich = getattr(Client, name, None)
        if tatsaechlich != erwartet:
            abweichungen.append(f"{name}: Tabelle {erwartet!r}, Paket "
                                f"{tatsaechlich!r}")
    return abweichungen


def berichte(befunde, schreiber=print):
    aus = schreiber
    sig = signatur(befunde)
    stellen = werte_je_stelle(befunde)

    aus("=" * 78)
    aus(f"DAS GERUEST VON shared/{MODUL}.py - erschlossen aus den Aufrufern")
    aus("=" * 78)
    aus(f"\n{len(befunde)} Modul(e) binden sie ein, mit {sig['aufrufe']} "
        f"Aufrufstelle(n).\n")

    aus("1. WER SIE EINBINDET UND WOMIT AUFRUFT")
    for pfad in sorted(befunde):
        eintrag = befunde[pfad]
        aus(f"\n   {pfad}")
        for bindung in eintrag["bindet_ein"]:
            aus(f"        Zeile {bindung['zeile']}: {bindung['form']}")
        for aufruf in eintrag["aufrufe"]:
            aus(f"        Zeile {aufruf['zeile']}: {aufruf['quelle']}")
            for nummer, argument in enumerate(aufruf["stellung"], 1):
                if argument["art"] == "ausdruck":
                    aus(f"             {nummer}. {argument['ausdruck']}  "
                        f"-> nicht aufloesbar (je Aufruf verschieden)")
                else:
                    aus(f"             {nummer}. "
                        f"{argument.get('ausdruck', '')} = "
                        f"{argument['wert']!r}")
            for schluessel, argument in sorted(aufruf["benannt"].items()):
                aus(f"             {schluessel}= {argument['wert']!r}")

    aus("\n2. DIE SIGNATUR, DIE DARAUS FOLGT")
    aus(f"   Alle {sig['aufrufe']} Aufrufe uebergeben "
        f"{sig['mindestens']} Argumente der Reihe nach, keines benannt, "
        f"keines mit * oder **.")
    aus(f"   Der versionierte Teil muss also mindestens erfuellen:")
    aus(f"        def {FUNKTION}(symbol, interval, lookback)")
    aus("   Mehr Stellen duerfen dahinter stehen, solange sie Vorgaben haben.")
    aus("   Weniger nicht: dann muesste ein Aufrufer geaendert werden - und")
    aus("   die neun forward_test.py/fetch_*.py sind der Live-Betrieb.")

    aus("\n3. WAS AN JEDER STELLE WIRKLICH ANKOMMT")
    ueberschriften = {0: "symbol", 1: "interval", 2: "lookback"}
    for nummer in sorted(stellen):
        aus(f"\n   Stelle {nummer + 1} ({ueberschriften.get(nummer, '?')}):")
        gesehen = {}
        for eintrag in stellen[nummer]:
            schluessel = (repr(eintrag["wert"]) if eintrag["art"] != "ausdruck"
                          else f"<{eintrag['ausdruck']}>")
            gesehen.setdefault(schluessel, []).append(
                f"{eintrag['modul']}:{eintrag['zeile']}")
        for schluessel in sorted(gesehen):
            aus(f"      {schluessel}")
            for ort in gesehen[schluessel]:
                aus(f"           {ort}")

    aus("\n4. WAS AM ERGEBNIS BENUTZT WIRD")
    alle_spalten = sorted({s for e in befunde.values() for s in e["spalten"]})
    aus(f"   Namentlich im Quelltext der Aufrufer: "
        f"{', '.join(alle_spalten) if alle_spalten else '(keine)'}")
    fehlend = [s for s in KURSSPALTEN if s not in alle_spalten]
    aus(f"   Nicht benutzt: {', '.join(fehlend) if fehlend else '(keine)'}")
    schreibende = sorted(p for p in befunde if befunde[p]["schreibt_csv"])
    handelnde = sorted(p for p in befunde if befunde[p]["letzte_kerze"])
    aus(f"\n   nach CSV geschrieben ({len(schreibende)}):")
    for pfad in schreibende:
        aus(f"      {pfad}  (Zeile "
            f"{', '.join(str(z) for z in befunde[pfad]['schreibt_csv'])})")
    aus(f"   als juengste Kerze in eine Entscheidung ({len(handelnde)}):")
    for pfad in handelnde:
        aus(f"      {pfad}  (Zeile "
            f"{', '.join(str(z) for z in befunde[pfad]['letzte_kerze'])})")

    abweichungen = _pruefe_kline_konstanten()
    aus("\n5. DIE KLINE-ZUORDNUNG")
    if abweichungen is None:
        aus("   `binance` ist hier nicht installiert - die Zuordnung "
            "KLINE_INTERVAL_* -> '1h'/'4h'/'1d' steht als Tabelle in dieser")
        aus("   Datei und ist NICHT gegen das Paket nachgeprueft. Auf einem "
            "Rechner mit python-binance prueft dieser Bericht sie mit.")
    elif abweichungen:
        aus("   ABWEICHEND gegen das installierte python-binance:")
        for zeile in abweichungen:
            aus(f"      {zeile}")
    else:
        aus("   Gegen das installierte python-binance geprueft: "
            "stimmt ueberein.")

    aus("\n6. WAS SICH AUS DEN AUFRUFERN NICHT ERSCHLIESSEN LAESST")
    aus("   Diese Punkte sind UNBEKANNT. Sie stehen hier, damit sie nicht")
    aus("   stillschweigend als geklaert gelten - nicht als Vermutung.")
    for titel, text in UNBEKANNT:
        aus(f"\n   {titel}: unbekannt")
        for zeile in _umbruch(text, 66):
            aus(f"      {zeile}")

    aus("\n" + "=" * 78)
    aus(f"Zusammenfassung: {len(befunde)} Module, {sig['aufrufe']} "
        f"Aufrufstellen, eine Signatur mit {sig['mindestens']} Argumenten.")
    aus(f"{len(UNBEKANNT)} Punkte bleiben unbekannt - sie entscheiden sich am "
        f"Mac, nicht hier.")


def _umbruch(text, breite):
    zeilen, laufend = [], ""
    for wort in text.split():
        if len(laufend) + len(wort) + 1 > breite:
            zeilen.append(laufend)
            laufend = wort
        else:
            laufend = f"{laufend} {wort}".strip()
    if laufend:
        zeilen.append(laufend)
    return zeilen


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description=f"Erschliesst aus den Aufrufern, was shared/{MODUL}.py "
                    f"koennen muss.")
    zerleger.add_argument("--wurzel", default=_WURZEL)
    zerleger.add_argument("--json", default=None)
    argumente = zerleger.parse_args(argv)

    befunde = sammle(argumente.wurzel)
    berichte(befunde)

    alle = sammle(argumente.wurzel, nur_betrieb=False)
    selbsttests = sorted(p for p in alle if ist_selbsttest(p))
    print("\n   Nachtrag - Selbsttests, die sie ebenfalls einbinden "
          f"({len(selbsttests)}):")
    for pfad in selbsttests:
        print(f"      {pfad}")
    print("   Sie zaehlen oben nicht mit: an ihnen haengt kein Bot.")

    if argumente.json:
        ziel = (argumente.json if os.path.isabs(argumente.json)
                else os.path.join(_HIER, argumente.json))
        if os.path.dirname(ziel):
            os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump({"module": befunde, "signatur": signatur(befunde),
                       "unbekannt": dict(UNBEKANNT)},
                      datei, indent=2, ensure_ascii=False, sort_keys=True,
                      default=str)
        print(f"\nJSON: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
