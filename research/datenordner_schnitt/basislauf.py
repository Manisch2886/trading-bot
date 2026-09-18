#!/usr/bin/env python3
"""
Basislauf: jede Testdatei einmal, mit Zeitgrenze (TB-46)
==============================================================================
Ein Basislauf soll eine Frage beantworten: **hat diese Arbeit etwas kaputt
gemacht?** Dazu muss er drei Dinge auseinanderhalten, die sonst alle als
"rot" oder alle als "gruen" erscheinen:

  **rot**          der Test lief und meldete Fehler
  **bekannt rot**  er war vor dieser Arbeit schon rot - mit dem Vermerk, auf
                   **welchem Rechner** gemessen wurde
  **ungeprueft**   er verlangt ein Argument und gibt ohne eines nur seine
                   Nutzungszeile aus. ⚠️ Das ist Rueckgabewert 0 oder 1, aber
                   **keine Messung** - und es darf nicht als "gruen" gelten.
  **Zeitgrenze**   er terminiert nicht. Der Kindprozess wird danach
                   **beendet**, sonst rechnet er weiter.

⚠️ Warum ein Python-Runner und kein `timeout`: auf dem Mac des Betreibers gibt
es **kein GNU `timeout`**. Ein Basislauf, der dort nicht laeuft, ist der
falsche Basislauf - der Mac ist der Rechner, auf dem der Betrieb stattfindet.

⚠️ `trading-env/` wird ausgeschlossen. Ohne diesen Ausschluss findet `find`
**1312** statt 62 Testdateien - die Fremdpakete bringen ihre eigenen mit.

Jede Datei laeuft in einem **eigenen Prozess**. Das ist keine Vorsicht: neun
Bots fuehren gleichnamige `equity_simulation.py`, die sich in `sys.modules`
gegenseitig verdecken (TB-40).

    python3 research/datenordner_schnitt/basislauf.py
    python3 research/datenordner_schnitt/basislauf.py --grenze 300
    python3 research/datenordner_schnitt/basislauf.py --json ergebnisse/basislauf.json

Rueckgabewert 0, wenn kein **unerwartet** roter Test dabei war; sonst 1.
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))

AUSGENOMMEN = ("trading-env", "__pycache__", ".git", "node_modules")

# ---------------------------------------------------------------------------
# Bekannt rot - ⚠️ mit dem Rechner, auf dem gemessen wurde. Mehrere Listen
# dieses Projekts waren falsch, weil sie unbesehen von einer Umgebung in die
# andere uebernommen wurden (docs/UMGEBUNGEN.md, Regel 3).
# ---------------------------------------------------------------------------
# ⚠️ GESTRICHEN (TB-46b, 17.09.2026): `system/test_log_rotation.py` stand hier
# mit "Mac 17.09.: 1 Fehler". Der Eintrag war falsch - die Datei ist auf
# BEIDEN Rechnern gruen (117/117; Mac-Messung im TB-46-Maclauf, Cloud-Messung
# im TB-46b-Basislauf). Ein falscher Eintrag in dieser Liste ist teurer als
# gar keiner: er macht einen Test, der eines Tages wirklich rot wird,
# unsichtbar. Das ist genau die Fehlerfamilie, gegen die TB-45 und TB-46b
# gebaut sind - eine Wache, die aufgehoert hat zu beissen, ohne es zu sagen.
BEKANNT_ROT = {
    "dashboard/test_portfolio_sicht.py": "Mac 17.09.: 1 Fehler",
    "shared/test_stabile_sortierung.py": "Mac 17.09.: 3 Fehler",
    "shared/test_wellenauswahl.py": "Mac 17.09.: 1 Fehler",
    "research/exposure_messung/test_exposure_kern.py": "Mac 17.09.: 1 Fehler",
    "research/hrp_portfolio/test_hrp_core.py": "Mac 17.09.: scipy fehlt",
}

# Nicht rot, sondern UNGEPRUEFT: sie verlangen ein Bot-Argument.
UNGEPRUEFT = {
    "research/drawdown_reihenfolge/test_drawdown.py": "verlangt ein Bot-Argument",
    "research/fib_score_stufen/test_stufen.py": "verlangt ein Bot-Argument",
    "research/elliott_wave_params/test_params.py": "verlangt ein Bot-Argument",
}

# Terminiert nicht - Zeitgrenze und danach beenden.
LAEUFT_WEITER = {
    "shared/test_drawdown_beide_masse.py": "terminiert nicht (bekannt)",
}


def testdateien(wurzel=_WURZEL):
    gefunden = []
    for pfad, unter, dateien in os.walk(wurzel):
        unter[:] = [u for u in unter if u not in AUSGENOMMEN]
        if any(a in pfad for a in AUSGENOMMEN):
            continue
        for name in dateien:
            if name.startswith("test_") and name.endswith(".py"):
                gefunden.append(os.path.relpath(os.path.join(pfad, name),
                                                wurzel))
    return sorted(gefunden)


def beende_gruppe(prozess):
    """Die ganze Prozessgruppe beenden - nicht nur den Kindprozess.

    ⚠️ **TB-47, der Anlass.** `prozess.kill()` beendet genau **einen**
    Prozess: den, den `Popen` gestartet hat. Startet der Test sich selbst
    einen Unterprozess - und mehrere tun das, sie fuehren Bots oder
    Wegwerf-Module in einem eigenen Prozess aus -, dann ueberlebt dieser
    **Enkel** den `kill`. Er verliert nur seinen Elternprozess, haengt sich
    an PID 1 und rechnet weiter.

    Gemessen, nicht vermutet: in **beiden** Mac-Laeufen blieb nach der
    Zeitgrenze von `shared/test_drawdown_beide_masse.py` ein
    `--bot elliott_wave` zurueck, zuletzt **22 Minuten bei 99 % CPU**, bis
    ihn ein Mensch von Hand beendet hat. Das kostet bei jedem Basislauf eine
    Viertelstunde Rechenzeit und einen Handgriff.

    Die Abhilfe hat zwei Haelften, und beide sind noetig:

      * `start_new_session=True` beim Start - der Kindprozess wird
        **Anfuehrer einer eigenen Prozessgruppe**, und jeder Enkel landet
        in derselben Gruppe. Ohne das zeigte `os.killpg` auf die Gruppe
        des Runners selbst - er braechte sich um.
      * `os.killpg` statt `kill` - das Signal geht an **alle** Mitglieder
        der Gruppe.

    Erst `SIGTERM`, damit ein Test seine Wegwerf-Verzeichnisse noch
    aufraeumen kann, nach kurzer Frist `SIGKILL`.
    """
    try:
        gruppe = os.getpgid(prozess.pid)
    except (OSError, AttributeError):
        # Der Prozess ist schon weg, oder das Betriebssystem kennt keine
        # Prozessgruppen (Windows). Dann bleibt nur der Kindprozess.
        prozess.kill()
        return
    for signal_ in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(gruppe, signal_)
        except OSError:
            return                      # niemand mehr da - fertig
        try:
            prozess.wait(timeout=5)
            if signal_ is signal.SIGTERM:
                # Der Kindprozess ist weg. Die Enkel koennen es trotzdem
                # noch nicht sein - deshalb kommt SIGKILL auf die Gruppe
                # in jedem Fall hinterher.
                continue
            return
        except subprocess.TimeoutExpired:
            continue


def fuehre_aus(rel, wurzel, grenze):
    """Eine Testdatei, eigener Prozess, Zeitgrenze.

    ⚠️ Die **ganze Prozessgruppe** wird danach beendet, nicht nur der
    Kindprozess - siehe `beende_gruppe`. `communicate(timeout=)` allein
    laesst ihn weiterrechnen, und `kill()` allein laesst die Enkel
    weiterrechnen.
    """
    beginn = time.time()
    prozess = subprocess.Popen(
        [sys.executable, os.path.join(wurzel, rel)],
        cwd=wurzel, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, start_new_session=True)
    abgebrochen = False
    try:
        ausgabe, _ = prozess.communicate(timeout=grenze)
    except subprocess.TimeoutExpired:
        abgebrochen = True
        beende_gruppe(prozess)          # ⚠️ sonst rechnen die Enkel weiter
        try:
            ausgabe, _ = prozess.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            ausgabe = ""
    dauer = time.time() - beginn
    rueckgabe = prozess.returncode

    # Die Nutzungszeile erkennen: ein Test, der nur seinen Aufruf erklaert,
    # hat nichts gemessen. Er ist `ungeprueft`, nicht `gruen`.
    text = ausgabe or ""
    nutzungszeile = (("usage:" in text.lower() or "Nutzung:" in text
                      or "aufruf:" in text.lower())
                     and "bestanden" not in text)

    if abgebrochen:
        art = "zeitgrenze"
    elif rel in UNGEPRUEFT or (nutzungszeile and "Pruefungen" not in text):
        art = "ungeprueft"
    elif rueckgabe == 0:
        art = "gruen"
    else:
        art = "rot"

    return {"datei": rel, "rueckgabe": rueckgabe, "art": art,
            "sekunden": round(dauer, 1), "abgebrochen": abgebrochen,
            "letzte_zeilen": [z for z in text.strip().splitlines()[-4:]]}


def main(argv=None) -> int:
    z = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    z.add_argument("--wurzel", default=_WURZEL)
    z.add_argument("--grenze", type=int, default=420,
                   help="Zeitgrenze je Testdatei in Sekunden")
    z.add_argument("--json", default=None)
    a = z.parse_args(argv)

    dateien = testdateien(a.wurzel)
    if not dateien:
        # Kein stiller Erfolg: null Testdateien ist ein Fehler der Suche.
        print("NICHT MESSBAR: keine einzige Testdatei gefunden.",
              file=sys.stderr)
        return 1

    print("=" * 78)
    print("TB-46 BASISLAUF - %d Testdateien, Zeitgrenze %d s je Datei"
          % (len(dateien), a.grenze))
    print("=" * 78)

    ergebnisse = []
    for rel in dateien:
        e = fuehre_aus(rel, a.wurzel, a.grenze)
        # Einordnung gegen die Listen oben
        if rel in LAEUFT_WEITER and e["art"] == "zeitgrenze":
            e["einordnung"] = "erwartet: %s" % LAEUFT_WEITER[rel]
            e["unerwartet"] = False
        elif rel in UNGEPRUEFT:
            e["einordnung"] = "ungeprueft: %s" % UNGEPRUEFT[rel]
            e["unerwartet"] = False
        elif rel in BEKANNT_ROT:
            e["einordnung"] = "bekannt rot (%s)" % BEKANNT_ROT[rel]
            # ⚠️ Auch das Gegenteil ist eine Abweichung: ein bekannt roter
            # Test, der hier gruen ist, sagt etwas ueber den Unterschied der
            # Rechner - und das gehoert gemeldet, nicht verschwiegen.
            e["unerwartet"] = e["art"] == "gruen"
            if e["unerwartet"]:
                e["einordnung"] += " - hier aber GRUEN"
        else:
            e["einordnung"] = ""
            e["unerwartet"] = e["art"] in ("rot", "zeitgrenze")
        ergebnisse.append(e)

        zeichen = {"gruen": "OK  ", "rot": "ROT ", "ungeprueft": "----",
                   "zeitgrenze": "ZEIT"}[e["art"]]
        marke = " <-- UNERWARTET" if e["unerwartet"] else ""
        print("  [%s] %-62s %6.1fs %s%s"
              % (zeichen, rel, e["sekunden"],
                 e["einordnung"], marke))

    je_art = {}
    for e in ergebnisse:
        je_art[e["art"]] = je_art.get(e["art"], 0) + 1
    unerwartet = [e for e in ergebnisse if e["unerwartet"]]

    print("\n" + "=" * 78)
    for art in ("gruen", "rot", "ungeprueft", "zeitgrenze"):
        print("  %-12s %3d" % (art, je_art.get(art, 0)))
    print("  %-12s %3d" % ("UNERWARTET", len(unerwartet)))
    for e in unerwartet:
        print("    - %s (%s, Rueckgabewert %s)"
              % (e["datei"], e["art"], e["rueckgabe"]))
        for zeile in e["letzte_zeilen"]:
            print("        %s" % zeile[:110])

    if a.json:
        ziel = (a.json if os.path.isabs(a.json) else os.path.join(_HIER, a.json))
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump({"grenze": a.grenze, "je_art": je_art,
                       "ergebnisse": ergebnisse}, datei, indent=2,
                      ensure_ascii=False, sort_keys=True)
        print("\nJSON: %s" % ziel)

    return 1 if unerwartet else 0


if __name__ == "__main__":
    sys.exit(main())
