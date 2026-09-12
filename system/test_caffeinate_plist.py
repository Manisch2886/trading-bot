"""
Selbsttests der caffeinate-launchd-Vorlage
==============================================================================
Geprueft wird die DATEI system/com.manisch.caffeinate.plist, nicht ein
laufender Dienst: gueltiges XML, die von launchd erwarteten Schluessel und
vor allem die Flag-Wahl. Der Test laeuft deshalb auf jedem Rechner, auch
ohne macOS.

Der wichtigste Punkt ist die NEGATIV-Pruefung: `-d` (Display dauerhaft
wach) und `-u` (Display aktiv einschalten) duerfen NICHT auftauchen - weder
einzeln noch in einem zusammengefassten Argument wie "-imsd". Sie kosten im
Dauerbetrieb Strom und Displaylebensdauer, ohne fuer die Cronjobs etwas zu
bringen. Genau so ein Flag rutscht beim spaeteren Aufraeumen leicht mit
hinein; deshalb steht es hier als Test und nicht nur als Kommentar.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:  python3 system/test_caffeinate_plist.py
"""

import os
import plistlib
import sys
import xml.etree.ElementTree as ET

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)

PLIST = os.path.join(_DIR, "com.manisch.caffeinate.plist")
README = os.path.join(_DIR, "README_CAFFEINATE.md")
TESTAUFTRAG = os.path.join(_DIR, "TESTAUFTRAG_CAFFEINATE.md")

ERWARTETE_FLAGS = ["-i", "-m", "-s"]
VERBOTENE_FLAGS = ["-d", "-u"]

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        FEHLER.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


def lade():
    """Die Vorlage als Python-Dict. Faellt der Test hier aus, sind alle
    weiteren Aussagen wertlos - deshalb bricht er dann ab."""
    with open(PLIST, "rb") as datei:
        return plistlib.load(datei)


# ---------------------------------------------------------------------------
def test_datei_und_xml():
    print("\n1) Datei und XML")
    check("Vorlage vorhanden", os.path.isfile(PLIST), PLIST)
    if not os.path.isfile(PLIST):
        return

    roh = open(PLIST, "r", encoding="utf-8").read()

    try:
        ET.parse(PLIST)
        wohlgeformt = True
        fehlertext = ""
    except ET.ParseError as fehler:                      # noqa: BLE001
        wohlgeformt = False
        fehlertext = str(fehler)
    check("Gueltiges, wohlgeformtes XML", wohlgeformt, fehlertext)

    check("XML-Deklaration in Zeile 1",
          roh.splitlines()[0].startswith("<?xml version=\"1.0\""))
    check("Apple-DOCTYPE vorhanden",
          "-//Apple//DTD PLIST 1.0//EN" in roh)
    check("plist-Version 1.0", "<plist version=\"1.0\">" in roh)

    try:
        daten = lade()
        lesbar = isinstance(daten, dict)
    except Exception as fehler:                          # noqa: BLE001
        lesbar = False
        daten = None
        print(f"       plistlib: {fehler}")
    check("plistlib liest die Datei als Dictionary", lesbar)


# ---------------------------------------------------------------------------
def test_schluessel():
    print("\n2) Erwartete launchd-Schluessel")
    daten = lade()

    for schluessel in ("Label", "ProgramArguments", "RunAtLoad", "KeepAlive",
                       "StandardOutPath", "StandardErrorPath"):
        check(f"Schluessel {schluessel} vorhanden", schluessel in daten)

    check("Label ist com.manisch.caffeinate",
          daten.get("Label") == "com.manisch.caffeinate",
          repr(daten.get("Label")))

    # Wichtig: echte Booleans (<true/>), nicht die Zeichenketten "true" -
    # launchd wertet <string>true</string> anders aus als <true/>.
    check("RunAtLoad ist der Boolean true (nicht \"true\")",
          daten.get("RunAtLoad") is True, repr(daten.get("RunAtLoad")))
    check("KeepAlive ist der Boolean true (nicht \"true\")",
          daten.get("KeepAlive") is True, repr(daten.get("KeepAlive")))

    check("Kein Program-Schluessel neben ProgramArguments",
          "Program" not in daten)


# ---------------------------------------------------------------------------
def test_flags():
    print("\n3) Aufruf und Flags")
    daten = lade()
    argumente = daten.get("ProgramArguments")

    check("ProgramArguments ist eine Liste", isinstance(argumente, list))
    if not isinstance(argumente, list) or not argumente:
        return

    check("Alle Argumente sind Zeichenketten",
          all(isinstance(a, str) for a in argumente))
    check("Erstes Argument ist /usr/bin/caffeinate",
          argumente[0] == "/usr/bin/caffeinate", repr(argumente[0]))

    flags = argumente[1:]
    check("Genau drei Flags", len(flags) == 3, repr(flags))
    check("Flags sind -i, -m und -s", sorted(flags) == sorted(ERWARTETE_FLAGS),
          repr(flags))
    check("Jedes Flag ist ein EIGENES Argument (kein \"-ims\")",
          all(len(f) == 2 and f.startswith("-") for f in flags), repr(flags))
    check("Keine doppelten Flags", len(set(flags)) == len(flags))


# ---------------------------------------------------------------------------
def test_keine_display_flags():
    """Die eigentliche Absicherung: -d und -u halten das Display wach bzw.
    schalten es ein. Beides ist hier unerwuenscht."""
    print("\n4) Display-Flags -d und -u sind NICHT enthalten")
    daten = lade()
    argumente = daten.get("ProgramArguments") or []
    flags = [a for a in argumente[1:] if isinstance(a, str)]

    for verboten in VERBOTENE_FLAGS:
        check(f"{verboten} kommt als eigenes Argument nicht vor",
              verboten not in flags)

    # Auch zusammengefasst nicht: ein spaeteres "-imsd" wuerde die Pruefung
    # oben passieren, wenn sie nur auf exakte Argumente schaut.
    gebuendelt = [f for f in flags
                  if f.startswith("-")
                  and any(b in f[1:] for b in ("d", "u"))]
    check("d/u auch nicht in einem gebuendelten Flag versteckt",
          not gebuendelt, repr(gebuendelt))

    check("Kein Argument enthaelt ein weiteres unerwartetes Flag",
          all(f in ERWARTETE_FLAGS for f in flags), repr(flags))


# ---------------------------------------------------------------------------
def test_logpfade():
    print("\n5) Log-Pfade")
    daten = lade()
    aus = daten.get("StandardOutPath", "")
    err = daten.get("StandardErrorPath", "")

    check("StandardOutPath ist absolut", aus.startswith("/"), aus)
    check("StandardErrorPath ist absolut", err.startswith("/"), err)
    check("StandardOutPath zeigt auf logs/system/caffeinate.log",
          aus.endswith("/logs/system/caffeinate.log"), aus)
    check("StandardErrorPath zeigt auf logs/system/caffeinate.err.log",
          err.endswith("/logs/system/caffeinate.err.log"), err)
    check("Beide Logs liegen im selben Ordner",
          os.path.dirname(aus) == os.path.dirname(err))

    # Konsistenz mit dem bereits eingerichteten Telegram-Dienst: beide
    # Vorlagen muessen denselben Projektpfad annehmen, sonst schreibt eine
    # von beiden ins Leere.
    #
    # Die Telegram-Vorlage lag bis TB-15 unter notifications/ und liegt
    # seitdem neben dieser hier unter system/. Frueher stand der Vergleich
    # hinter einem "if os.path.isfile(...)": verschwand die Datei oder zog
    # sie um, fiel die Pruefung stillschweigend weg und der Test blieb
    # gruen. Ihre Existenz wird deshalb jetzt selbst geprueft.
    telegram = os.path.join(_DIR, "com.manisch.telegram-tradesignal-bot.plist")
    check("Telegram-Vorlage liegt neben dieser unter system/",
          os.path.isfile(telegram), telegram)
    if os.path.isfile(telegram):
        with open(telegram, "rb") as datei:
            anderes = plistlib.load(datei)
        wurzel_telegram = anderes.get("StandardOutPath", "").split("/logs/")[0]
        wurzel_hier = aus.split("/logs/")[0]
        check("Projektpfad stimmt mit der Telegram-Vorlage ueberein",
              wurzel_hier == wurzel_telegram,
              f"{wurzel_hier} vs. {wurzel_telegram}")


# ---------------------------------------------------------------------------
def test_dokumentation():
    print("\n6) Dokumentation")
    check("README_CAFFEINATE.md vorhanden", os.path.isfile(README))
    check("TESTAUFTRAG_CAFFEINATE.md vorhanden", os.path.isfile(TESTAUFTRAG))
    if not os.path.isfile(README):
        return
    text = open(README, "r", encoding="utf-8").read()

    for befehl, zweck in (
        ("cp system/com.manisch.caffeinate.plist ~/Library/LaunchAgents/",
         "Installation"),
        ("launchctl load ~/Library/LaunchAgents/com.manisch.caffeinate.plist",
         "Laden"),
        ("launchctl unload ~/Library/LaunchAgents/com.manisch.caffeinate.plist",
         "Entfernen"),
        ("pmset -g assertions", "Pruefung"),
        ("mkdir -p ~/trading-bot/logs/system", "Log-Ordner"),
        ("pgrep -fl caffeinate", "manuelles caffeinate finden"),
    ):
        check(f"README nennt den Befehl fuer {zweck}", befehl in text)

    check("README nennt das erwartete Ergebnis PreventSystemSleep",
          "PreventSystemSleep" in text)
    check("README nennt das erwartete Ergebnis PreventUserIdleSystemSleep",
          "PreventUserIdleSystemSleep" in text)

    for flag in ERWARTETE_FLAGS + VERBOTENE_FLAGS:
        check(f"README begruendet {flag}", f"`{flag}`" in text)

    for stichwort, grenze in (
        ("ugeklappt", "zugeklapptes MacBook"),
        ("Anmeldung", "LaunchAgent erst nach Anmeldung"),
        ("LaunchDaemon", "LaunchDaemon nur als Option"),
        ("Batteriebetrieb", "-s wirkt nicht auf Batterie"),
    ):
        check(f"README dokumentiert die Grenze: {grenze}", stichwort in text)


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("Selbsttests der caffeinate-launchd-Vorlage")
    print("=" * 78)
    tests = [test_datei_und_xml, test_schluessel, test_flags,
             test_keine_display_flags, test_logpfade, test_dokumentation]
    for test in tests:
        try:
            test()
        except Exception as fehler:                      # noqa: BLE001
            import traceback
            FEHLER.append(f"{test.__name__} (Ausnahme)")
            print(f"  [FEHLER] {test.__name__} warf eine Ausnahme: {fehler}")
            traceback.print_exc()

    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print(f"{BESTANDEN} von {gesamt} Pruefungen bestanden, "
          f"{len(FEHLER)} fehlgeschlagen.")
    for name in FEHLER:
        print(f"  - {name}")
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
