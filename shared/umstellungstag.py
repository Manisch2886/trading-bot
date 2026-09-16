#!/usr/bin/env python3
"""
Der Umstellungstag je Bot - Beginn des einzigen verwertbaren Vergleichsfensters
==============================================================================
Ab TB-38 entscheiden alle neun Bots auf der **Entscheidungskerze** (die letzte
Kerze, deren Zeitraum vor der Startzeit des Laufs endete) statt auf der
laufenden. Erst ab diesem Tag entsteht ein Papierpfad, der nach denselben
Regeln laeuft wie der Backtest.

    Papierpfade VOR diesem Tag gelten fuer den Vergleich Backtest gegen Live
    als nicht vergleichbar. Der Backtest-gegen-Live-Vergleich beginnt fuer
    diese Bots NEU.

Das ist keine Formalie. Der Live-Record ist die einzige Out-of-Sample-Evidenz
des Projekts, und bis zum Stichtag der Neuselektion am **13.12.2026** ist das
verbleibende Fenster kurz. Wer spaeter auswertet, muss auf eine Zahl zeigen
koennen statt auf eine Erinnerung - und er muss es **maschinell** koennen,
sonst wird die Zaesur beim ersten automatisierten Vergleich uebersehen.

------------------------------------------------------------------------------
Wo die Datei liegt, und warum dort
------------------------------------------------------------------------------
`docs/umstellungstag_entscheidungskerze.json`.

* **Nicht in `shared/` oder `strategies/`.** Kein Bot liest diesen Wert, und
  keine Handelszahl haengt daran. Eine Datei neben dem Bot-Code lockt den
  naechsten Leser dazu, sie im Live-Pfad zu benutzen - und damit waere eine
  Aufzeichnung ueber den Betrieb zu einem Eingang des Betriebs geworden.
* **Nicht in `data/`.** Das sind Kursdateien, und ihr SHA-256 ist der
  Datenstand-Hash der Vorregistrierung. Was dort hineinwaechst, aendert eine
  Pruefsumme, die etwas ganz anderes bezeugen soll.
* **Nicht in `results/`.** Dort steht Rechenergebnis, das der naechste Lauf
  ueberschreibt. Dieser Vermerk muss jeden Lauf ueberleben.
* **In `docs/`**, weil dort der Aufschrieb des Projekts liegt - und weil die
  Prosa-Fassung derselben Zaesur einen Ordner weiter in
  `docs/DATENLUECKEN.md` steht. Wer die JSON findet, findet die Begruendung
  im selben Verzeichnislisting.

------------------------------------------------------------------------------
Warum ein Eintrag nicht ueberschrieben wird
------------------------------------------------------------------------------
Der Umstellungstag ist eine **Tatsache**, kein Zustand. Ein zweiter Aufruf
darf ihn nicht stillschweigend vorruecken: das waere der Anfang des
Vergleichsfensters, verschoben ohne dass es jemandem auffiele - und der
Vergleich haette danach ein Fenster, das kuerzer ist als das, was tatsaechlich
gemessen wurde. Wer wirklich korrigieren will, sagt es ausdruecklich
(`--erneut`), und der alte Wert bleibt als `frueher` erhalten.

------------------------------------------------------------------------------
Gebrauch
------------------------------------------------------------------------------
    python3 shared/umstellungstag.py --festhalten --alle
    python3 shared/umstellungstag.py --festhalten t3_supertrend elliott_wave
    python3 shared/umstellungstag.py --zeigen
    python3 shared/umstellungstag.py --pruefen        # 1, wenn ein Bot fehlt

Rueckgabewerte: 0 ohne Befund, 1 mit Befund, 2 bei Bedienfehler.
"""

import argparse
import datetime as dt
import json
import os
import socket
import subprocess
import sys

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

from entscheidungskerze import _BOTS                        # noqa: E402

DATEI = os.path.join(BASE_DIR, "docs",
                     "umstellungstag_entscheidungskerze.json")

VERSION = 1
ZEITFORMAT = "%Y-%m-%dT%H:%M:%SZ"

# Die neun Bots, ihr Intervall und ihr Markt - aus EINER Quelle, damit die
# Liste hier nicht von der abweichen kann, mit der die Schicht arbeitet.
BOTS = {name: {"intervall": intervall, "markt": markt}
        for name, intervall, markt in _BOTS}

VORHER = "df.iloc[-1] - die zum Laufzeitpunkt LAUFENDE Kerze (Teilkerze)"
NACHHER = ("die letzte Kerze, deren Zeitraum vor der Startzeit des Laufs "
           "endete (Entscheidungskerze, TB-38)")

BESCHREIBUNG = (
    "Je Bot der Zeitpunkt, ab dem er auf der Entscheidungskerze entscheidet "
    "statt auf der laufenden (TB-38). Papierpfade VOR diesem Zeitpunkt sind "
    "fuer den Vergleich Backtest gegen Live nicht vergleichbar - der "
    "Vergleich beginnt fuer diesen Bot dort neu. Gelesen wird diese Datei "
    "vom Vergleich, NICHT von den Bots. Prosa-Fassung: docs/DATENLUECKEN.md, "
    "Abschnitt 'Zaesur 2026 - die Entscheidungskerze'.")


def jetzt_utc():
    return dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)


def _commit():
    """Der Commit, auf dem die Umstellung stattfand - oder None.

    Er beantwortet die Frage, die beim spaeteren Auswerten wirklich gestellt
    wird: "welcher Code lief ab diesem Tag?". Ein Datum allein beantwortet
    sie nicht.
    """
    try:
        roh = subprocess.run(["git", "-C", BASE_DIR, "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=10)
    except Exception:                                       # noqa: BLE001
        return None
    if roh.returncode != 0:
        return None
    return (roh.stdout or "").strip() or None


def lesen(pfad=None):
    """Der abgelegte Stand - oder ein leeres Geruest.

    Eine unlesbare Datei wird NICHT stillschweigend durch ein leeres Geruest
    ersetzt: hier stehen Tatsachen, die sich nicht wiederherstellen lassen.
    """
    ziel = pfad or DATEI
    try:
        with open(ziel, encoding="utf-8") as datei:
            daten = json.load(datei)
    except FileNotFoundError:
        return {"version": VERSION, "beschreibung": BESCHREIBUNG, "bots": {}}
    if not isinstance(daten, dict) or not isinstance(daten.get("bots"), dict):
        raise ValueError(
            f"{ziel} ist vorhanden, sieht aber nicht aus wie ein "
            f"Umstellungsvermerk (erwartet ein Objekt mit 'bots'). Es wird "
            f"NICHTS ueberschrieben - hier stehen Zeitpunkte, die sich nicht "
            f"rekonstruieren lassen.")
    return daten


def schreiben(daten, pfad=None):
    """Erst in eine Nebendatei, dann umbenennen - wie warteauftraege.json."""
    ziel = pfad or DATEI
    ordner = os.path.dirname(ziel)
    if ordner:
        os.makedirs(ordner, exist_ok=True)
    neu = ziel + ".neu"
    with open(neu, "w", encoding="utf-8") as datei:
        json.dump(daten, datei, indent=2, ensure_ascii=False, sort_keys=True)
        datei.write("\n")
    os.replace(neu, ziel)
    return ziel


def festhalten(bots, pfad=None, jetzt=None, erneut=False, rechner=None):
    """(neu festgehalten, uebersprungen) - je eine Liste von Botnamen."""
    unbekannt = [b for b in bots if b not in BOTS]
    if unbekannt:
        raise ValueError(
            f"Unbekannte(r) Bot: {', '.join(sorted(unbekannt))}. Bekannt sind "
            f"die neun aus shared/entscheidungskerze.py: "
            f"{', '.join(sorted(BOTS))}.")

    daten = lesen(pfad)
    daten.setdefault("version", VERSION)
    daten["beschreibung"] = BESCHREIBUNG
    zeitpunkt = (jetzt or jetzt_utc()).strftime(ZEITFORMAT)
    commit = _commit()
    wo = rechner if rechner is not None else socket.gethostname()

    neu, uebersprungen = [], []
    for name in bots:
        vorhanden = daten["bots"].get(name)
        if vorhanden and not erneut:
            uebersprungen.append(name)
            continue
        eintrag = {
            "umgestellt_am": zeitpunkt,
            "intervall": BOTS[name]["intervall"],
            "markt": BOTS[name]["markt"],
            "vorher": VORHER,
            "nachher": NACHHER,
            "commit": commit,
            "rechner": wo,
        }
        if vorhanden:
            # Der alte Wert geht nicht verloren - eine Korrektur, die den
            # vorigen Beginn des Vergleichsfensters spurlos loescht, waere
            # genau das, was diese Datei verhindern soll.
            eintrag["frueher"] = [x for x in
                                  (vorhanden.get("frueher") or []) ] + [
                {k: v for k, v in vorhanden.items() if k != "frueher"}]
        daten["bots"][name] = eintrag
        neu.append(name)

    if neu:
        schreiben(daten, pfad)
    return neu, uebersprungen


def fehlende(pfad=None):
    """Welche der neun Bots haben noch keinen Umstellungstag?"""
    daten = lesen(pfad)
    return sorted(b for b in BOTS if b not in daten["bots"])


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Haelt je Bot fest, ab wann er auf der Entscheidungskerze "
                    "entscheidet (TB-38).")
    zerleger.add_argument("bots", nargs="*", metavar="BOT")
    zerleger.add_argument("--festhalten", action="store_true")
    zerleger.add_argument("--alle", action="store_true",
                          help="alle neun Bots")
    zerleger.add_argument("--erneut", action="store_true",
                          help="einen vorhandenen Eintrag ausdruecklich "
                               "ueberschreiben (der alte bleibt als "
                               "'frueher' erhalten)")
    zerleger.add_argument("--zeigen", action="store_true")
    zerleger.add_argument("--pruefen", action="store_true",
                          help="Rueckgabewert 1, wenn ein Bot fehlt")
    zerleger.add_argument("--datei", default=None)
    argumente = zerleger.parse_args(argv)

    if sum(map(bool, (argumente.festhalten, argumente.zeigen,
                      argumente.pruefen))) != 1:
        print("Genau eines von --festhalten / --zeigen / --pruefen angeben.",
              file=sys.stderr)
        return 2

    pfad = argumente.datei or DATEI

    if argumente.festhalten:
        ziel = sorted(BOTS) if argumente.alle else list(argumente.bots)
        if not ziel:
            print("Welche Bots? Namen angeben oder --alle.", file=sys.stderr)
            return 2
        try:
            neu, uebersprungen = festhalten(ziel, pfad, erneut=argumente.erneut)
        except ValueError as fehler:
            print(str(fehler), file=sys.stderr)
            return 2
        for name in neu:
            print(f"festgehalten: {name}")
        for name in uebersprungen:
            vorher = lesen(pfad)["bots"][name]["umgestellt_am"]
            print(f"unveraendert: {name} (steht seit {vorher} - der "
                  f"Umstellungstag ist eine Tatsache, kein Zustand; "
                  f"--erneut ueberschreibt ausdruecklich)")
        print(f"\nDatei: {pfad}")
        return 0

    if argumente.zeigen:
        daten = lesen(pfad)
        if not daten["bots"]:
            print(f"Noch kein Umstellungstag festgehalten ({pfad}).")
            return 0
        print(f"{'Bot':28} {'umgestellt am':22} {'Intervall':10} Markt")
        for name in sorted(daten["bots"]):
            e = daten["bots"][name]
            print(f"{name:28} {e['umgestellt_am']:22} "
                  f"{e.get('intervall', '?'):10} {e.get('markt', '?')}")
        offen = fehlende(pfad)
        if offen:
            print(f"\nNoch offen: {', '.join(offen)}")
        return 0

    offen = fehlende(pfad)
    print(f"Geprueft: {len(BOTS)} Bots gegen {pfad}")
    if not offen:
        print("Kein Befund: fuer jeden Bot steht ein Umstellungstag.")
        return 0
    print(f"\n{len(offen)} Bot(s) ohne Umstellungstag: {', '.join(offen)}")
    print("Fuer diese Bots laesst sich nicht sagen, ab wann ihr Papierpfad "
          "mit dem Backtest vergleichbar ist.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
