"""
Selbsttests der drei launchd-Dienst-Vorlagen
==============================================================================
Geprueft werden die DATEIEN unter system/, nicht laufende Dienste:

    com.manisch.caffeinate.plist            (haelt den Mac wach)
    com.manisch.telegram-tradesignal-bot.plist
    com.manisch.trading-dashboard.plist

Der Test laeuft auf jedem Rechner, auch ohne macOS. Die Flag-Wahl von
caffeinate bleibt in test_caffeinate_plist.py - hier stehen nur die
Zusicherungen, die fuer ALLE drei gelten, plus die beiden Python-Dienste.

DREI ERGEBNISSE STATT ZWEI - der Kern dieses Tests
--------------------------------------------------------------------------
Die Dashboard-Vorlage ist noch ein PLATZHALTER: die laufende Fassung liegt
nur unter ~/Library/LaunchAgents/ auf dem Mac des Nutzers, eine
Cloud-Sitzung kommt nicht daran, und Raten waere hier schlimmer als eine
Luecke. Ein Test, der einen Platzhalter fuer gueltig haelt, ist schlechter
als gar keiner - er behauptet eine Zusicherung, die es nicht gibt.

Deshalb hat jede Pruefung drei moegliche Ausgaenge, nicht zwei:

    [OK   ]  geprueft und in Ordnung
    [FEHL ]  geprueft und falsch
    [OFFEN]  NICHT geprueft, weil der Wert ein Platzhalter ist

Ein Platzhalter landet NIE im OK-Topf. Der Rueckgabewert unterscheidet die
drei Zustaende ebenfalls:

    0 = alles geprueft und in Ordnung
    1 = mindestens eine Pruefung ist fehlgeschlagen
    2 = keine Fehler, aber offene Platzhalter (heutiger Soll-Zustand)

Aus der 2 wird eine 0, sobald der Nutzer den einen Schritt aus
system/README_DIENSTE.md ausgefuehrt hat:

    cp ~/Library/LaunchAgents/com.manisch.trading-dashboard.plist system/

Mutationsproben
--------------------------------------------------------------------------
Abschnitt 7 verbiegt eine echte Vorlage auf der Platte und laesst dieselbe
Pruefkette darueber laufen, die oben auch die echten Dateien prueft. Zwei
Fallen, die in frueheren PRs (#73, #77, #78, #79, #81, #86) aufgetreten
sind, werden dabei ausdruecklich vermieden:

1. "Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst." Es wird deshalb KEIN Dictionary gebaut und dann ein Praedikat
   darauf losgelassen - das wuerde nur zeigen, dass das Praedikat auf
   selbstgebaute Daten reagiert. Stattdessen wird die echte Datei kopiert,
   im Text an genau einer Stelle veraendert und die ECHTE Pruefkette
   (Einlesen, plistlib, alle Checks) darauf angewandt. Beobachtet wird der
   Ablauf, nicht ein nachgestellter Zustand.

2. "Eine zweite Wache verdeckt das Fehlen der ersten." Jede Probe
   vergleicht die Menge der fehlgeschlagenen Pruefungen EXAKT mit der
   erwarteten Menge - nicht "irgendetwas ist fehlgeschlagen". Faellt die
   gepruefte Wache weg, ist die Menge kleiner als erwartet und die Probe
   schlaegt an; springt stattdessen eine andere Wache an, ist die Menge
   eine andere und die Probe schlaegt ebenfalls an. Als Grundlage dient
   die Telegram-Vorlage, weil sie als einzige der drei vollstaendig aus
   der laufenden Fassung stammt und keinen Platzhalter enthaelt.

Eine BEDINGTE Zusicherung (TB-16)
--------------------------------------------------------------------------
Zwei Pruefungen verlangten, dass die Dashboard-Vorlage DASHBOARD_HOST und
DASHBOARD_PORT in EnvironmentVariables setzt. Beide waren als
"erschlossen, nicht belegt" gekennzeichnet und sind am 12.09.2026
widerlegt worden: die laufende Fassung setzt keinen von beiden. Host und
Port duerfen aus der plist, aus der .env ODER aus der Voreinstellung in
dashboard/konfig.py kommen - der Test erklaert keinen Weg zum einzig
richtigen. Er prueft stattdessen: WENN die Vorlage einen der Werte setzt,
muss er der richtige sein. Begruendung und Bauform stehen bei
pruefe_dashboard_bindung(); dass die Pruefung dabei nicht einfach
verstummt ist, zeigen die Proben am Ende von Abschnitt 7.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:  python3 system/test_dienst_plists.py
"""

import os
import plistlib
import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)

CAFFEINATE = os.path.join(_DIR, "com.manisch.caffeinate.plist")
TELEGRAM = os.path.join(_DIR, "com.manisch.telegram-tradesignal-bot.plist")
DASHBOARD = os.path.join(_DIR, "com.manisch.trading-dashboard.plist")
README = os.path.join(_DIR, "README_DIENSTE.md")
TESTAUFTRAG = os.path.join(_DIR, "TESTAUFTRAG_DIENSTE.md")

# Ein Wert, der so beginnt, ist ausdruecklich NICHT belegt. Die Marke ist
# absichtlich kein gueltiger Pfad: launchd soll eine unbefuellte Vorlage
# nicht klaglos annehmen.
MARKE = "PLATZHALTER__"


class Vorlage:
    """Was von einer Vorlage erwartet wird. skript_rel ist der Pfad des
    Einstiegspunkts RELATIV zum Projekt-Root - genau der Teil, den ein
    spaeteres Umbenennen im Repo kaputtmachen wuerde."""

    def __init__(self, pfad, label, skript_rel=None):
        self.pfad = pfad
        self.label = label
        self.skript_rel = skript_rel

    @property
    def name(self):
        return os.path.basename(self.pfad)


VORLAGEN = [
    Vorlage(CAFFEINATE, "com.manisch.caffeinate"),
    Vorlage(TELEGRAM, "com.manisch.telegram-tradesignal-bot",
            "notifications/telegram_bot.py"),
    Vorlage(DASHBOARD, "com.manisch.trading-dashboard",
            "dashboard/server.py"),
]


# ---------------------------------------------------------------------------
class Pruefer:
    """Sammelt Ergebnisse in DREI Toepfen. Der dritte (offen) ist der
    Grund, warum es diese Klasse ueberhaupt gibt: ein Platzhalter darf
    weder als bestanden noch als Fehler gezaehlt werden."""

    def __init__(self, laut=True):
        self.laut = laut
        self.ok = []
        self.fehler = []
        self.offen = []

    def check(self, name, bedingung, detail=""):
        if bedingung:
            self.ok.append(name)
            self._sag("OK   ", name, detail)
        else:
            self.fehler.append(name)
            self._sag("FEHL ", name, detail)

    def check_wert(self, name, wert, praedikat, detail=""):
        """Wie check(), aber der zu pruefende Wert wird zuerst auf die
        Platzhalter-Marke geprueft. Ein Platzhalter wird NICHT bewertet,
        sondern als offen gemeldet - sonst wuerde der Test eine Zusicherung
        behaupten, die niemand eingeloest hat."""
        if isinstance(wert, str) and wert.startswith(MARKE):
            self.offen.append(name)
            self._sag("OFFEN", name, f"Platzhalter: {wert}")
            return
        self.check(name, praedikat(wert), detail or repr(wert))

    def _sag(self, marke, name, detail):
        if self.laut:
            print(f"  [{marke}] {name}" + (f"   {detail}" if detail else ""))


def lade(pfad):
    with open(pfad, "rb") as datei:
        return plistlib.load(datei)


def platzhalter_in(pfad):
    """Alle Platzhalter-Werte einer Vorlage, rekursiv. Bewusst ueber die
    eingelesenen Werte und nicht ueber den Rohtext: ein PLATZHALTER__ in
    einem XML-Kommentar ist Dokumentation und kein offener Wert."""
    gefunden = []

    def geh(knoten):
        if isinstance(knoten, str) and knoten.startswith(MARKE):
            gefunden.append(knoten)
        elif isinstance(knoten, dict):
            for wert in knoten.values():
                geh(wert)
        elif isinstance(knoten, list):
            for wert in knoten:
                geh(wert)

    try:
        geh(lade(pfad))
    except Exception:                                    # noqa: BLE001
        pass
    return gefunden


# ---------------------------------------------------------------------------
# Die gemeinsame Pruefkette. Genau diese Funktion laeuft sowohl ueber die
# echten Dateien (Abschnitte 1-3) als auch ueber die verbogenen Kopien in
# den Mutationsproben (Abschnitt 7) - deshalb pruefen die Proben den
# tatsaechlichen Ablauf und nicht eine nachgestellte Kulisse.
# ---------------------------------------------------------------------------
def pruefe_vorlage(vorlage, p):
    n = vorlage.name

    p.check(f"{n}: Datei vorhanden", os.path.isfile(vorlage.pfad))
    if not os.path.isfile(vorlage.pfad):
        return

    roh = open(vorlage.pfad, "r", encoding="utf-8").read()

    try:
        ET.parse(vorlage.pfad)
        wohlgeformt, fehlertext = True, ""
    except ET.ParseError as fehler:                      # noqa: BLE001
        wohlgeformt, fehlertext = False, str(fehler)
    p.check(f"{n}: Gueltiges, wohlgeformtes XML", wohlgeformt, fehlertext)

    p.check(f"{n}: XML-Deklaration in Zeile 1",
            roh.splitlines()[0].startswith('<?xml version="1.0"'))
    p.check(f"{n}: Apple-DOCTYPE vorhanden",
            "-//Apple//DTD PLIST 1.0//EN" in roh)
    p.check(f"{n}: plist-Version 1.0", '<plist version="1.0">' in roh)

    try:
        daten = lade(vorlage.pfad)
        lesbar = isinstance(daten, dict)
    except Exception as fehler:                          # noqa: BLE001
        p.check(f"{n}: plistlib liest die Datei als Dictionary", False,
                str(fehler))
        return
    p.check(f"{n}: plistlib liest die Datei als Dictionary", lesbar)
    if not lesbar:
        return

    for schluessel in ("Label", "ProgramArguments", "RunAtLoad", "KeepAlive",
                       "StandardOutPath", "StandardErrorPath"):
        p.check(f"{n}: Schluessel {schluessel} vorhanden", schluessel in daten)

    p.check(f"{n}: Label ist {vorlage.label}",
            daten.get("Label") == vorlage.label, repr(daten.get("Label")))

    # launchd wertet <string>true</string> anders aus als <true/>. Der
    # Unterschied ist im Editor kaum zu sehen und im Betrieb fatal: der
    # Dienst startet dann nicht automatisch.
    p.check(f"{n}: RunAtLoad ist der Boolean true (nicht \"true\")",
            daten.get("RunAtLoad") is True, repr(daten.get("RunAtLoad")))
    p.check(f"{n}: KeepAlive ist der Boolean true (nicht \"true\")",
            daten.get("KeepAlive") is True, repr(daten.get("KeepAlive")))
    p.check(f"{n}: Kein Program-Schluessel neben ProgramArguments",
            "Program" not in daten)

    argumente = daten.get("ProgramArguments")
    p.check(f"{n}: ProgramArguments ist eine nichtleere Liste",
            isinstance(argumente, list) and bool(argumente))
    if not isinstance(argumente, list) or not argumente:
        return
    p.check(f"{n}: Alle Argumente sind Zeichenketten",
            all(isinstance(a, str) for a in argumente))

    p.check_wert(f"{n}: Erstes Argument ist ein absoluter Pfad",
                 argumente[0], lambda w: isinstance(w, str) and w.startswith("/"))

    for schluessel in ("StandardOutPath", "StandardErrorPath"):
        p.check_wert(f"{n}: {schluessel} ist absolut", daten.get(schluessel, ""),
                     lambda w: isinstance(w, str) and w.startswith("/"))

    if vorlage.skript_rel is None:
        return

    # --- ab hier nur die beiden Python-Dienste ---------------------------
    p.check(f"{n}: Genau zwei Argumente (Interpreter + Skript)",
            len(argumente) == 2, repr(argumente))
    if len(argumente) < 2:
        return

    skript = argumente[1]
    p.check(f"{n}: Skriptpfad ist absolut",
            isinstance(skript, str) and skript.startswith("/"), repr(skript))
    p.check(f"{n}: Skriptpfad endet auf {vorlage.skript_rel}",
            isinstance(skript, str) and skript.endswith("/" + vorlage.skript_rel),
            repr(skript))

    arbeitsverzeichnis = daten.get("WorkingDirectory", "")
    p.check(f"{n}: Schluessel WorkingDirectory vorhanden", "WorkingDirectory" in daten)
    p.check_wert(f"{n}: Skriptpfad liegt unter WorkingDirectory",
                 arbeitsverzeichnis,
                 lambda w: isinstance(skript, str) and bool(w)
                 and skript.startswith(w.rstrip("/") + "/"),
                 f"{arbeitsverzeichnis!r} vs. {skript!r}")

    # Die Pruefung, die verhindert, dass eine Vorlage still veraltet.
    #
    # Entscheidend ist, dass der zu pruefende Pfad AUS DER VORLAGE stammt
    # und nicht aus der Erwartung dieses Tests. Die erste Fassung pruefte
    # os.path.isfile(BASE_DIR + vorlage.skript_rel) - also ob die Datei
    # existiert, von der der Test ohnehin ausgeht. Das war zirkulaer: die
    # Mutationsprobe "Einstiegspunkt umbenannt" veraenderte die Vorlage,
    # und die Pruefung blieb trotzdem gruen, weil sie die Vorlage gar nicht
    # ansah. Die Probe unten hat genau das aufgedeckt.
    rechte_seite = ""
    if isinstance(skript, str) and arbeitsverzeichnis and \
            skript.startswith(arbeitsverzeichnis.rstrip("/") + "/"):
        rechte_seite = skript[len(arbeitsverzeichnis.rstrip("/")) + 1:]
    p.check(f"{n}: Einstiegspunkt aus der Vorlage existiert im Repo",
            bool(rechte_seite) and os.path.isfile(os.path.join(BASE_DIR, rechte_seite)),
            f"{rechte_seite!r}")


# ---------------------------------------------------------------------------
# Bindung des Dashboards: eine BEDINGTE Zusicherung
#
# Die erste Fassung (TB-15) verlangte, dass die Vorlage DASHBOARD_HOST und
# DASHBOARD_PORT in EnvironmentVariables setzt. Das war als "erschlossen,
# nicht belegt" gekennzeichnet - und ist am 12.09.2026 widerlegt worden:
# die laufende Fassung setzt KEINEN von beiden. Der Host steht in der .env,
# der Port nirgends (es gilt STANDARD_PORT aus dashboard/konfig.py). Der
# Dienst laeuft seit Monaten korrekt auf 100.106.38.8:8787.
#
# dashboard/konfig.py._wert() nimmt Umgebung, sonst .env, sonst
# Voreinstellung - ALLE DREI Bezugswege sind zulaessig, und der Test darf
# keinen davon zum einzig richtigen erklaeren. Zusichern laesst sich
# stattdessen: WENN die Vorlage einen der Werte setzt, muss er der richtige
# sein. Ein falscher Port in der plist ueberstimmt .env und Voreinstellung
# und macht das Dashboard unerreichbar - genau davor schuetzt das hier.
#
# Warum zwei bedingte Pruefungen und kein eigener Ergebnistopf: OFFEN
# heisst in diesem Test "noch nicht befuellt, jemand muss etwas tun", und
# genau das treibt den Rueckgabewert 2. Ein nicht gesetzter Host ist aber
# keine offene Aufgabe, sondern ein fertiger, gueltiger Zustand. Als OFFEN
# gemeldet kaeme der Test auf dem Mac des Nutzers nie mehr auf 0 - der
# Rueckgabewert-Mechanismus aus TB-15 wuerde dadurch entwertet.
# ---------------------------------------------------------------------------
def _ist_tailscale_adresse(wert):
    """100.64.0.0/10 - der CGNAT-Bereich, aus dem Tailscale seine Adressen
    vergibt. Absichtlich enger als "beginnt mit 100.": 100.0.x bis 100.63.x
    und 100.128.x aufwaerts sind gewoehnliche oeffentliche Adressen und in
    einer DASHBOARD_HOST-Zeile ein Fehler, kein Tailscale-Host."""
    if not isinstance(wert, str):
        return False
    teile = wert.split(".")
    if len(teile) != 4:
        return False
    for teil in teile:
        if not teil.isdigit() or not 0 <= int(teil) <= 255:
            return False
    return int(teile[0]) == 100 and 64 <= int(teile[1]) <= 127


# Was von den beiden Werten erwartet wird, WENN die Vorlage sie setzt.
BINDUNG = (
    ("DASHBOARD_HOST", "eine Tailscale-Adresse (100.64.x - 100.127.x)",
     _ist_tailscale_adresse),
    ("DASHBOARD_PORT", "8787", lambda w: w == "8787"),
)


def pruefe_dashboard_bindung(pfad, p):
    """Die bedingte Pruefung. Laeuft in Abschnitt 3 ueber die echte Vorlage
    und in Abschnitt 7 ueber verbogene Kopien - dieselbe Funktion, damit
    die Proben den tatsaechlichen Ablauf pruefen."""
    try:
        umgebung = lade(pfad).get("EnvironmentVariables") or {}
    except Exception as fehler:                          # noqa: BLE001
        for variable, erwartung, _ in BINDUNG:
            p.check(f"Vorlage setzt {variable} gar nicht oder auf {erwartung}",
                    False, str(fehler))
        return

    for variable, erwartung, praedikat in BINDUNG:
        name = f"Vorlage setzt {variable} gar nicht oder auf {erwartung}"
        if variable not in umgebung:
            # Kein Fehler und auch nichts Offenes: der Wert kommt dann aus
            # der .env oder aus der Voreinstellung in dashboard/konfig.py.
            p.check(name, True, "nicht in der Vorlage gesetzt - kommt aus "
                                ".env oder dashboard/konfig.py")
            continue
        p.check_wert(name, umgebung[variable], praedikat)


# ---------------------------------------------------------------------------
def abschnitt(titel):
    print(f"\n{titel}")


def test_vorlagen(p):
    abschnitt("1) Die drei Vorlagen - Aufbau, Schluessel, Pfade")
    for vorlage in VORLAGEN:
        pruefe_vorlage(vorlage, p)


def test_gemeinsam(p):
    abschnitt("2) Was fuer alle drei zusammen gelten muss")

    p.check("Alle drei Vorlagen liegen unter system/",
            all(os.path.isfile(v.pfad) for v in VORLAGEN),
            repr([v.name for v in VORLAGEN if not os.path.isfile(v.pfad)]))
    if not all(os.path.isfile(v.pfad) for v in VORLAGEN):
        return

    labels = [lade(v.pfad).get("Label") for v in VORLAGEN]
    p.check("Die drei Labels sind verschieden", len(set(labels)) == 3, repr(labels))
    p.check("Jedes Label beginnt mit com.manisch.",
            all(isinstance(l, str) and l.startswith("com.manisch.") for l in labels))
    p.check("Dateiname entspricht jeweils dem Label",
            all(os.path.basename(v.pfad) == f"{lade(v.pfad).get('Label')}.plist"
                for v in VORLAGEN))

    # Alle drei muessen denselben Projekt-Root annehmen. Laufen sie
    # auseinander, schreibt mindestens einer ins Leere - und das faellt im
    # Betrieb erst auf, wenn man ein Log sucht und keines findet.
    wurzeln = set()
    for v in VORLAGEN:
        daten = lade(v.pfad)
        for wert in (daten.get("WorkingDirectory"),
                     daten.get("StandardOutPath", "").split("/logs/")[0]):
            if isinstance(wert, str) and wert.startswith("/Users/"):
                wurzeln.add(wert.rstrip("/"))
    p.check("Alle drei Vorlagen nehmen denselben Projektpfad an",
            len(wurzeln) == 1, repr(sorted(wurzeln)))


def test_dashboard_einstiegspunkt(p):
    """Die Vorlage behauptet, dashboard/server.py sei der Einstiegspunkt.
    Das wird hier am Quelltext belegt statt geglaubt."""
    abschnitt("3) Dashboard-Einstiegspunkt ist belegt, nicht behauptet")

    server = os.path.join(BASE_DIR, "dashboard", "server.py")
    app = os.path.join(BASE_DIR, "dashboard", "app.py")
    p.check("dashboard/server.py vorhanden", os.path.isfile(server))
    p.check("dashboard/app.py vorhanden", os.path.isfile(app))
    if not (os.path.isfile(server) and os.path.isfile(app)):
        return

    quelle = open(server, "r", encoding="utf-8").read()
    p.check("server.py importiert erzeuge_app aus app.py",
            re.search(r"^from\s+app\s+import\s+.*\berzeuge_app\b",
                      quelle, re.M) is not None)
    p.check("server.py startet uvicorn", "uvicorn.run(" in quelle)
    p.check("server.py ist direkt ausfuehrbar (__main__-Block)",
            '__name__ == "__main__"' in quelle)
    p.check("app.py definiert erzeuge_app",
            re.search(r"^def\s+erzeuge_app\b", open(app, encoding="utf-8").read(),
                      re.M) is not None)

    # Die Vorlage darf NICHT auf app.py zeigen - app.py baut die App, aber
    # startet keinen Server.
    argumente = lade(DASHBOARD).get("ProgramArguments") or []
    p.check("Die Vorlage zeigt nicht auf dashboard/app.py",
            not any(isinstance(a, str) and a.endswith("/dashboard/app.py")
                    for a in argumente))

    # Port und Bindung. Die Grundeinstellung im Code ist localhost - die
    # Tailscale-Adresse muss also von aussen kommen. WOHER sie kommt, ist
    # damit aber noch nicht festgelegt; siehe pruefe_dashboard_bindung().
    konfig = open(os.path.join(BASE_DIR, "dashboard", "konfig.py"),
                  encoding="utf-8").read()
    p.check("konfig.py: STANDARD_PORT ist 8787",
            re.search(r"^STANDARD_PORT\s*=\s*8787", konfig, re.M) is not None)
    p.check("konfig.py: STANDARD_HOST ist 127.0.0.1 (Bindung muss gesetzt werden)",
            re.search(r'^STANDARD_HOST\s*=\s*"127\.0\.0\.1"', konfig, re.M) is not None)

    # Der Beleg dafuer, dass die Pruefung unten bedingt sein MUSS: _wert()
    # nimmt zuerst die Umgebung (also EnvironmentVariables der plist), dann
    # die .env, dann die Voreinstellung. Alle drei Wege fuehren zum Ziel.
    # Waere diese Reihenfolge eines Tages anders, faellt genau hier auf,
    # dass die Begruendung der bedingten Pruefung nicht mehr traegt.
    p.check("konfig.py: Wert kommt aus der Umgebung, sonst .env, sonst "
            "Voreinstellung",
            re.search(r"return\s+os\.environ\.get\(name\)\s+or\s+"
                      r"env_werte\.get\(name\)\s+or\s+standard",
                      konfig) is not None)

    pruefe_dashboard_bindung(DASHBOARD, p)


def test_platzhalter(p):
    """Der Platzhalter-Zustand wird ausdruecklich festgestellt und gemeldet.
    Genau hier wuerde ein nachlaessiger Test stillschweigend gruen zeigen."""
    abschnitt("4) Platzhalter-Zustand der Vorlagen")

    for vorlage in (CAFFEINATE, TELEGRAM):
        offen = platzhalter_in(vorlage)
        p.check(f"{os.path.basename(vorlage)}: vollstaendig, kein Platzhalter",
                not offen, repr(offen))

    offen = platzhalter_in(DASHBOARD)
    if offen:
        print(f"  [OFFEN] {os.path.basename(DASHBOARD)}: noch ein Platzhalter "
              f"({len(offen)} Werte)")
        for wert in offen:
            print(f"          - {wert}")
        p.offen.append("Dashboard-Vorlage ist noch ein Platzhalter")
    else:
        p.check(f"{os.path.basename(DASHBOARD)}: aus der laufenden Fassung "
                f"befuellt", True)


def test_dokumentation(p):
    abschnitt("5) Dokumentation")
    p.check("README_DIENSTE.md vorhanden", os.path.isfile(README))
    p.check("TESTAUFTRAG_DIENSTE.md vorhanden", os.path.isfile(TESTAUFTRAG))
    if not os.path.isfile(README):
        return
    text = open(README, "r", encoding="utf-8").read()

    for label in ("com.manisch.caffeinate", "com.manisch.telegram-tradesignal-bot",
                  "com.manisch.trading-dashboard"):
        p.check(f"README beschreibt {label}", label in text)

    for befehl, zweck in (
        ("launchctl kickstart -k gui/$(id -u)/", "Neustart"),
        ("launchctl list | grep manisch", "Pruefen"),
        ("launchctl load ~/Library/LaunchAgents/", "Laden"),
        ("launchctl unload ~/Library/LaunchAgents/", "Entfernen"),
        ("cp ~/Library/LaunchAgents/com.manisch.trading-dashboard.plist system/",
         "Befuellen der Dashboard-Vorlage"),
        ("python3 system/test_dienst_plists.py", "Gegenpruefung"),
    ):
        p.check(f"README nennt den Befehl fuer {zweck}", befehl in text)

    for stichwort, thema in (
        ("100.106.38.8", "Tailscale-Adresse statt localhost"),
        ("8787", "Port"),
        ("303", "303 ohne Token ist korrektes Verhalten"),
        ("-15", "negative Zahl ist der Exit-Status des Vorgaengers"),
        ("Signal 15", "Erklaerung der -15"),
        ("Anmeldung", "LaunchAgent erst nach grafischer Anmeldung"),
        ("git pull", "Neustart nur bei Aenderungen an dashboard/"),
        # TB-16: der Befund, der die bedingte Pruefung ausgeloest hat. Er
        # ist Betriebswissen und darf nicht still aus dem README fallen.
        ("nicht versioniert",
         "die .env ist nicht versioniert - der Fernzugriff haengt an ihr"),
        ("logs/dashboard/launchd.err.log", "Logpfad des Dashboard-Dienstes"),
    ):
        p.check(f"README dokumentiert: {thema}", stichwort in text)


# ---------------------------------------------------------------------------
# 7) Mutationsproben
# ---------------------------------------------------------------------------
def _probe(quelle, vorlage_vorlage, ersetzungen, erwartete_fehler, p,
           beschreibung, erwartet_offen=None):
    """Verbiegt eine ECHTE Vorlage an genau einer Stelle und laesst die
    ECHTE Pruefkette darueber laufen. Verglichen wird die Menge der
    fehlgeschlagenen Pruefungen EXAKT - nicht "irgendetwas ist rot".

    Damit kann weder eine fehlende Wache unbemerkt bleiben (die Menge
    waere zu klein) noch eine andere Wache die gepruefte ersetzen (die
    Menge waere eine andere)."""
    with tempfile.TemporaryDirectory() as ordner:
        ziel = os.path.join(ordner, os.path.basename(quelle))
        shutil.copy(quelle, ziel)
        text = open(ziel, encoding="utf-8").read()
        for alt, neu in ersetzungen:
            if alt not in text:
                p.check(f"Probe '{beschreibung}': Ansatzpunkt gefunden", False,
                        repr(alt))
                return
            text = text.replace(alt, neu, 1)
        open(ziel, "w", encoding="utf-8").write(text)

        verbogen = Vorlage(ziel, vorlage_vorlage.label, vorlage_vorlage.skript_rel)
        still = Pruefer(laut=False)
        pruefe_vorlage(verbogen, still)

        # Die Pruefnamen tragen den Dateinamen; der ist in der Kopie
        # derselbe, also sind die Mengen direkt vergleichbar.
        ist = set(still.fehler)
        soll = set(erwartete_fehler)
        p.check(f"Probe '{beschreibung}' schlaegt genau bei den erwarteten "
                f"Pruefungen an", ist == soll,
                "" if ist == soll else f"zuviel={sorted(ist - soll)} "
                                       f"fehlt={sorted(soll - ist)}")

        if erwartet_offen is not None:
            p.check(f"Probe '{beschreibung}': erwartete offene Pruefungen",
                    set(still.offen) == set(erwartet_offen),
                    repr(sorted(still.offen)))


def _probe_bindung(quelle, eintraege, erwartete_fehler, p, beschreibung,
                   erwartet_offen=None):
    """Wie _probe(), nur fuer die bedingte Bindungs-Pruefung: eine ECHTE
    Vorlage wird kopiert, an genau einer Stelle um einen
    EnvironmentVariables-Block ergaenzt und durch die ECHTE Pruefkette
    geschickt. Verglichen werden die Mengen der fehlgeschlagenen und - wo
    angegeben - der offenen Pruefungen EXAKT."""
    with tempfile.TemporaryDirectory() as ordner:
        ziel = os.path.join(ordner, os.path.basename(quelle))
        shutil.copy(quelle, ziel)
        if eintraege:
            zeilen = "".join(f"        <key>{name}</key>\n"
                             f"        <string>{wert}</string>\n"
                             for name, wert in eintraege)
            block = ("    <key>EnvironmentVariables</key>\n"
                     "    <dict>\n" + zeilen + "    </dict>\n</dict>")
            text = open(ziel, encoding="utf-8").read()
            if "</dict>\n</plist>" not in text:
                p.check(f"Probe '{beschreibung}': Ansatzpunkt gefunden", False)
                return
            open(ziel, "w", encoding="utf-8").write(
                text.replace("</dict>\n</plist>", block + "\n</plist>", 1))

        still = Pruefer(laut=False)
        pruefe_dashboard_bindung(ziel, still)

        ist, soll = set(still.fehler), set(erwartete_fehler)
        p.check(f"Probe '{beschreibung}' schlaegt genau bei den erwarteten "
                f"Pruefungen an", ist == soll,
                "" if ist == soll else f"zuviel={sorted(ist - soll)} "
                                       f"fehlt={sorted(soll - ist)}")
        p.check(f"Probe '{beschreibung}': erwartete offene Pruefungen",
                set(still.offen) == set(erwartet_offen or []),
                repr(sorted(still.offen)))


def test_mutationsproben(p):
    abschnitt("7) Mutationsproben - schlagen die Wachen wirklich an?")

    basis = VORLAGEN[1]            # Telegram: vollstaendig, kein Platzhalter
    n = basis.name

    # Gegenprobe zuerst: die unveraenderte Datei muss sauber durchlaufen.
    # Ohne sie wuerde jede Probe unten auch dann "anschlagen", wenn die
    # Grundlage schon kaputt ist.
    still = Pruefer(laut=False)
    pruefe_vorlage(basis, still)
    p.check("Gegenprobe: die unveraenderte Telegram-Vorlage hat 0 Fehler",
            not still.fehler, repr(still.fehler))
    p.check("Gegenprobe: die unveraenderte Telegram-Vorlage hat 0 offene Werte",
            not still.offen, repr(still.offen))

    _probe(basis.pfad, basis,
           [("    <key>RunAtLoad</key>\n    <true/>",
             "    <key>RunAtLoad</key>\n    <string>true</string>")],
           [f'{n}: RunAtLoad ist der Boolean true (nicht "true")'],
           p, "RunAtLoad als Zeichenkette statt Boolean")

    _probe(basis.pfad, basis,
           [("    <key>KeepAlive</key>\n    <true/>",
             "    <key>KeepAlive</key>\n    <string>true</string>")],
           [f'{n}: KeepAlive ist der Boolean true (nicht "true")'],
           p, "KeepAlive als Zeichenkette statt Boolean")

    _probe(basis.pfad, basis,
           [("<string>com.manisch.telegram-tradesignal-bot</string>",
             "<string>com.manisch.telegram-bot</string>")],
           [f"{n}: Label ist com.manisch.telegram-tradesignal-bot"],
           p, "Label weicht vom erwarteten ab")

    # Die Anti-Veralterungs-Pruefung: der Einstiegspunkt wird umbenannt.
    _probe(basis.pfad, basis,
           [("notifications/telegram_bot.py</string>",
             "notifications/telegram_bot_alt.py</string>")],
           [f"{n}: Skriptpfad endet auf notifications/telegram_bot.py",
            f"{n}: Einstiegspunkt aus der Vorlage existiert im Repo"],
           p, "Einstiegspunkt im Repo umbenannt")

    # Diese Probe isoliert die Anti-Veralterungs-Pruefung vollstaendig:
    # der Pfad endet weiterhin auf notifications/telegram_bot.py und liegt
    # weiterhin unter dem WorkingDirectory - nur die Datei gibt es im Repo
    # nicht. Es KANN also nur die eine Wache anschlagen. Waere sie (wie in
    # der ersten Fassung) zirkulaer gegen die Erwartung statt gegen die
    # Vorlage gebaut, bliebe hier alles gruen und die Probe schluege an.
    _probe(basis.pfad, basis,
           [("<string>/Users/jaquelineloffler/trading-bot/notifications/"
             "telegram_bot.py</string>",
             "<string>/Users/jaquelineloffler/trading-bot/alt/notifications/"
             "telegram_bot.py</string>")],
           [f"{n}: Einstiegspunkt aus der Vorlage existiert im Repo"],
           p, "Vorlage zeigt auf einen Ordner, den es im Repo nicht gibt")

    _probe(basis.pfad, basis,
           [("    </array>", "        <string>--debug</string>\n    </array>")],
           [f"{n}: Genau zwei Argumente (Interpreter + Skript)"],
           p, "Drittes Argument eingeschmuggelt")

    _probe(basis.pfad, basis,
           [("<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\"\n"
             "  \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n", "")],
           [f"{n}: Apple-DOCTYPE vorhanden"],
           p, "Apple-DOCTYPE entfernt")

    _probe(basis.pfad, basis,
           [("    <key>StandardOutPath</key>\n    <string>/Users/jaquelineloffler"
             "/trading-bot/logs/notifications/launchd.out.log</string>",
             "    <key>StandardOutPath</key>\n    <string>logs/notifications/"
             "launchd.out.log</string>")],
           [f"{n}: StandardOutPath ist absolut"],
           p, "StandardOutPath relativ statt absolut")

    _probe(basis.pfad, basis,
           [("    <key>Label</key>", "    <key>Program</key>\n"
             "    <string>/bin/echo</string>\n\n    <key>Label</key>")],
           [f"{n}: Kein Program-Schluessel neben ProgramArguments"],
           p, "Program-Schluessel neben ProgramArguments")

    # Die wichtigste Probe: erkennt der Platzhalter-Melder einen
    # Platzhalter ueberhaupt? Oben wurde gezeigt, dass er bei der echten
    # Telegram-Vorlage NICHT anschlaegt; hier muss er anschlagen. Ein
    # Melder, der immer schweigt, waere sonst nicht von einem richtigen zu
    # unterscheiden.
    _probe(basis.pfad, basis,
           [("<string>/Users/jaquelineloffler/trading-bot/trading-env/bin/"
             "python3</string>",
             f"<string>{MARKE}PYTHON3_PFAD</string>")],
           [],
           p, "Platzhalter im Interpreter-Pfad",
           erwartet_offen=[f"{n}: Erstes Argument ist ein absoluter Pfad"])

    with tempfile.TemporaryDirectory() as ordner:
        ziel = os.path.join(ordner, os.path.basename(basis.pfad))
        shutil.copy(basis.pfad, ziel)
        text = open(ziel, encoding="utf-8").read().replace(
            "<string>/Users/jaquelineloffler/trading-bot/trading-env/bin/python3</string>",
            f"<string>{MARKE}PYTHON3_PFAD</string>", 1)
        open(ziel, "w", encoding="utf-8").write(text)
        p.check("Platzhalter-Melder findet den eingeschmuggelten Platzhalter",
                platzhalter_in(ziel) == [f"{MARKE}PYTHON3_PFAD"],
                repr(platzhalter_in(ziel)))

    # --- Proben zur bedingten Bindungs-Pruefung --------------------------
    #
    # Grundlage ist wieder die Telegram-Vorlage, und diesmal aus einem
    # zweiten Grund: sie ist die einzige der drei, die der Nutzer NICHT
    # ueberschreibt, wenn er die Dashboard-Vorlage aus der laufenden
    # Fassung befuellt. Proben, die an der Dashboard-Vorlage haengen,
    # wuerden nach diesem einen cp ihren Ansatzpunkt verlieren.
    #
    # Sie setzt von sich aus keine EnvironmentVariables - das ist genau der
    # Zustand der uebernommenen Dashboard-Vorlage. Die erste Probe haelt
    # diesen Zustand fest, die weiteren schmuggeln je EINEN falschen Wert
    # ein. Ohne die letzten beiden waere nicht zu unterscheiden, ob die
    # Pruefung noch etwas zusichert oder nach der Korrektur nur noch
    # schweigt.
    _probe_bindung(basis.pfad, [], [], p,
                   "keine EnvironmentVariables (Zustand der laufenden Fassung)")

    _probe_bindung(basis.pfad,
                   [("DASHBOARD_PORT", "8080")],
                   ["Vorlage setzt DASHBOARD_PORT gar nicht oder auf 8787"],
                   p, "falscher Port 8080 in der Vorlage")

    _probe_bindung(basis.pfad,
                   [("DASHBOARD_PORT", "8787")], [],
                   p, "richtiger Port 8787 in der Vorlage")

    _probe_bindung(basis.pfad,
                   [("DASHBOARD_HOST", "127.0.0.1")],
                   ["Vorlage setzt DASHBOARD_HOST gar nicht oder auf eine "
                    "Tailscale-Adresse (100.64.x - 100.127.x)"],
                   p, "Bindung auf localhost statt Tailscale")

    # 100.7.x sieht aus wie eine Tailscale-Adresse, liegt aber unterhalb
    # von 100.64 und ist damit eine gewoehnliche oeffentliche Adresse.
    _probe_bindung(basis.pfad,
                   [("DASHBOARD_HOST", "100.7.38.8")],
                   ["Vorlage setzt DASHBOARD_HOST gar nicht oder auf eine "
                    "Tailscale-Adresse (100.64.x - 100.127.x)"],
                   p, "100.x ausserhalb des Tailscale-Bereichs")

    _probe_bindung(basis.pfad,
                   [("DASHBOARD_HOST", "100.106.38.8")], [],
                   p, "richtige Tailscale-Adresse in der Vorlage")

    # Ein Platzhalter gehoert auch hier weder in den OK- noch in den
    # Fehler-Topf.
    _probe_bindung(basis.pfad,
                   [("DASHBOARD_HOST", f"{MARKE}TAILSCALE_ADRESSE")], [], p,
                   "Platzhalter als Bindungsadresse",
                   erwartet_offen=["Vorlage setzt DASHBOARD_HOST gar nicht "
                                   "oder auf eine Tailscale-Adresse "
                                   "(100.64.x - 100.127.x)"])

    # Und die Gegenrichtung: ein PLATZHALTER__ im Kommentar ist
    # Dokumentation, kein offener Wert - sonst waere die echte
    # Dashboard-Vorlage nie befuellbar, weil ihr Kommentar die Marke
    # erklaert.
    with tempfile.TemporaryDirectory() as ordner:
        ziel = os.path.join(ordner, os.path.basename(basis.pfad))
        shutil.copy(basis.pfad, ziel)
        text = open(ziel, encoding="utf-8").read().replace(
            "<plist version=\"1.0\">",
            f"<!-- Beispiel: {MARKE}IRGENDWAS -->\n<plist version=\"1.0\">", 1)
        open(ziel, "w", encoding="utf-8").write(text)
        p.check("Platzhalter-Melder ignoriert die Marke im XML-Kommentar",
                platzhalter_in(ziel) == [], repr(platzhalter_in(ziel)))


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("Selbsttests der drei launchd-Dienst-Vorlagen")
    print("=" * 78)

    p = Pruefer()
    for test in (test_vorlagen, test_gemeinsam, test_dashboard_einstiegspunkt,
                 test_platzhalter, test_dokumentation, test_mutationsproben):
        try:
            test(p)
        except Exception as fehler:                      # noqa: BLE001
            import traceback
            p.fehler.append(f"{test.__name__} (Ausnahme)")
            print(f"  [FEHL ] {test.__name__} warf eine Ausnahme: {fehler}")
            traceback.print_exc()

    gesamt = len(p.ok) + len(p.fehler) + len(p.offen)
    print("\n" + "=" * 78)
    print(f"{len(p.ok)} von {gesamt} Pruefungen bestanden, "
          f"{len(p.fehler)} fehlgeschlagen, {len(p.offen)} offen (Platzhalter).")
    for name in p.fehler:
        print(f"  [FEHL ] {name}")
    for name in p.offen:
        print(f"  [OFFEN] {name}")

    if p.fehler:
        print("\nErgebnis: FEHLER. Rueckgabewert 1.")
        return 1
    if p.offen:
        print("""
Ergebnis: KEINE FEHLER, ABER NOCH OFFEN. Rueckgabewert 2.

Die Dashboard-Vorlage ist absichtlich ein Platzhalter: ihre laufende
Fassung liegt nur unter ~/Library/LaunchAgents/ auf dem Mac und war nie im
Repo. Die offenen Werte sind NICHT geraten worden - deshalb meldet dieser
Test sie als offen, statt sie gruen durchzuwinken.

So wird aus der 2 eine 0 (auf dem Mac des Nutzers, Einzelheiten in
system/README_DIENSTE.md):

    cp ~/Library/LaunchAgents/com.manisch.trading-dashboard.plist system/
    python3 system/test_dienst_plists.py
""")
        return 2
    print("\nErgebnis: alles geprueft und in Ordnung. Rueckgabewert 0.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
