"""
Selbsttests der Log-Rotation
==============================================================================
Geprueft wird das VERHALTEN von system/log_rotation.py gegen echte Dateien in
einem Wegwerf-Ordner unter /tmp - nie gegen das echte logs/ des Projekts.

Der Kern dieser Aufgabe ist der offene Schreibzugriff (Abschnitt 4): ein
ECHTER zweiter Prozess haelt die Logdatei waehrend der Rotation offen und
schreibt durchgehend weiter. Danach muessen seine neuen Zeilen in der NEUEN
Datei stehen und jede einzelne Zeile noch auffindbar sein. Das ist die
eigentliche Zusicherung - sie wird am Verhalten gemessen und nicht behauptet.

Derselbe Abschnitt beziffert das Restfenster zwischen Sichern und Leeren: er
laesst waehrend fortlaufenden Schreibens mehrfach rotieren und zaehlt am Ende
die fehlenden Zeilennummern.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:  python3 system/test_log_rotation.py
"""

import ast
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import time

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)
sys.path.insert(0, _DIR)

import log_rotation as lr                                    # noqa: E402

README = os.path.join(_DIR, "README_LOG_ROTATION.md")

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


# ---------------------------------------------------------------------------
class Wegwerflogs:
    """Ein Log-Ordner unter /tmp. Die Tests fassen das echte logs/ nie an."""

    def __enter__(self):
        self.wurzel = tempfile.mkdtemp(prefix="logrot_")
        return self

    def __exit__(self, *_):
        shutil.rmtree(self.wurzel, ignore_errors=True)

    def schreibe(self, rel, inhalt):
        pfad = os.path.join(self.wurzel, rel)
        os.makedirs(os.path.dirname(pfad), exist_ok=True)
        with open(pfad, "wb") as datei:
            datei.write(inhalt if isinstance(inhalt, bytes)
                        else inhalt.encode("utf-8"))
        return pfad

    def pfad(self, rel):
        return os.path.join(self.wurzel, rel)


def fuellung(bytes_anzahl, marke=b"x"):
    return marke * bytes_anzahl


# ---------------------------------------------------------------------------
def test_auswahl():
    print("\n1) Welche Dateien ueberhaupt in Frage kommen")
    with Wegwerflogs() as w:
        w.schreibe("t3_supertrend/cron.log", "a\n")
        w.schreibe("broker/cron.log", "b\n")
        w.schreibe("notifications/schliess_benachrichtigung.log", "c\n")
        gefunden = lr.gefundene_logs(w.wurzel)
        check("findet Logs in allen Unterordnern", len(gefunden) == 3, gefunden)
        check("Pfade sind relativ zu logs/",
              all(not p.startswith("/") for p in gefunden), gefunden)

        # Alles, was kein .log ist, bleibt aussen vor - ausdruecklich auch
        # Datenbanken und .env, die der Auftrag nennt.
        w.schreibe("t3_supertrend/trades.db", "DBDBDB")
        w.schreibe("t3_supertrend/state.json", "{}")
        w.schreibe("notifications/.env", "TOKEN=geheim")
        w.schreibe("broker/testnet_spiegel.log.1", "fremdes Archiv")
        gefunden = lr.gefundene_logs(w.wurzel)
        check("Datenbank wird nicht gefunden",
              not any("trades.db" in p for p in gefunden), gefunden)
        check("JSON-Zustand wird nicht gefunden",
              not any(".json" in p for p in gefunden), gefunden)
        check(".env wird nicht gefunden",
              not any(".env" in p for p in gefunden), gefunden)
        check("Fremdarchiv *.log.1 wird nicht gefunden",
              not any(p.endswith(".log.1") for p in gefunden), gefunden)

        # Eigene Archive enden nicht auf .log und werden deshalb nie selbst
        # zum Rotationskandidaten.
        w.schreibe("broker/cron.log.2026-09-12T07-40-00", "eigenes Archiv")
        gefunden = lr.gefundene_logs(w.wurzel)
        check("eigenes Archiv wird nicht erneut gefunden",
              gefunden.count(os.path.join("broker", "cron.log")) == 1
              and not any(p.startswith(os.path.join("broker", "cron.log."))
                          for p in gefunden), gefunden)

        leer = lr.gefundene_logs(os.path.join(w.wurzel, "gibt_es_nicht"))
        check("fehlender Log-Ordner ergibt leere Liste, keinen Absturz",
              leer == [], leer)


def test_symlink_und_grenze():
    print("\n2) Nichts ausserhalb von logs/")
    with Wegwerflogs() as w:
        aussen = tempfile.mkdtemp(prefix="logrot_aussen_")
        try:
            ziel = os.path.join(aussen, "wichtig.log")
            with open(ziel, "wb") as datei:
                datei.write(fuellung(5000))
            os.makedirs(w.pfad("dienst"), exist_ok=True)
            link = w.pfad("dienst/zeigt_nach_aussen.log")
            os.symlink(ziel, link)

            eintraege = {e["rel"]: e for e in lr.plan(w.wurzel, schwelle=100)}
            rel = os.path.join("dienst", "zeigt_nach_aussen.log")
            check("Symlink wird nicht rotiert",
                  rel in eintraege and not eintraege[rel]["rotieren"],
                  eintraege.get(rel, {}).get("grund"))

            lr.rotiere(w.wurzel, schwelle=100)
            check("Ziel des Symlinks unveraendert",
                  os.path.getsize(ziel) == 5000, os.path.getsize(ziel))
            check("kein Archiv ausserhalb von logs/ angelegt",
                  os.listdir(aussen) == ["wichtig.log"], os.listdir(aussen))
        finally:
            shutil.rmtree(aussen, ignore_errors=True)

    # Ein Symlink INNERHALB von logs/. Wichtig als eigener Fall: beim Link nach
    # aussen greift schon die Pfadgrenze, der Symlink-Schutz selbst wird dabei
    # also nie geprueft. Ueber den Link zu rotieren wuerde die echte Datei
    # leeren und das Archiv unter dem Namen des Links ablegen.
    with Wegwerflogs() as w:
        echt = w.schreibe("dienst/echt.log", fuellung(5000, b"e"))
        link = w.pfad("dienst/link.log")
        os.symlink(echt, link)
        eintraege = {e["rel"]: e for e in lr.plan(w.wurzel, schwelle=100)}
        rel_link = os.path.join("dienst", "link.log")
        check("Symlink innerhalb von logs/ wird nicht rotiert",
              not eintraege[rel_link]["rotieren"],
              eintraege[rel_link]["grund"])
        check("der Grund nennt den Symlink",
              "Symlink" in eintraege[rel_link]["grund"],
              eintraege[rel_link]["grund"])
        lr.rotiere(w.wurzel, schwelle=100)
        check("es gibt kein Archiv unter dem Namen des Links",
              lr.alte_staende(link) == [], lr.alte_staende(link))
        check("die echte Datei wurde genau einmal rotiert",
              len(lr.alte_staende(echt)) == 1, lr.alte_staende(echt))
        try:
            pass
        finally:
            shutil.rmtree(aussen, ignore_errors=True)


def test_schwelle():
    print("\n3) Rotation nur ueber der Schwelle")
    with Wegwerflogs() as w:
        w.schreibe("a/klein.log", fuellung(999))
        w.schreibe("a/genau.log", fuellung(1000))
        w.schreibe("a/gross.log", fuellung(1001))
        eintraege = {e["rel"]: e for e in lr.plan(w.wurzel, schwelle=1000)}

        check("unter der Schwelle: keine Rotation",
              not eintraege[os.path.join("a", "klein.log")]["rotieren"])
        check("genau auf der Schwelle: Rotation",
              eintraege[os.path.join("a", "genau.log")]["rotieren"])
        check("ueber der Schwelle: Rotation",
              eintraege[os.path.join("a", "gross.log")]["rotieren"])

        ergebnisse = {e["rel"]: e for e in lr.rotiere(w.wurzel, schwelle=1000)}
        check("kleine Datei bleibt unangetastet",
              os.path.getsize(w.pfad("a/klein.log")) == 999)
        check("kleine Datei hat kein Archiv",
              lr.alte_staende(w.pfad("a/klein.log")) == [])
        check("grosse Datei ist geleert",
              os.path.getsize(w.pfad("a/gross.log")) == 0)
        check("grosse Datei hat genau ein Archiv",
              len(lr.alte_staende(w.pfad("a/gross.log"))) == 1)
        check("Ergebnis meldet 'uebersprungen' fuer die kleine Datei",
              ergebnisse[os.path.join("a", "klein.log")]["ergebnis"]
              == "uebersprungen")
        check("Ergebnis meldet 'rotiert' fuer die grosse Datei",
              ergebnisse[os.path.join("a", "gross.log")]["ergebnis"]
              == "rotiert")


def test_inhalt_und_inode():
    print("\n4) Inhalt vollstaendig, Datei behaelt ihren Inode")
    with Wegwerflogs() as w:
        inhalt = ("".join(f"zeile {i}\n" for i in range(5000))).encode()
        pfad = w.schreibe("dienst/lang.log", inhalt)
        inode_vorher = os.stat(pfad).st_ino

        ergebnis = lr.rotiere_eine(lr.plan(w.wurzel, schwelle=100)[0])
        check("Rotation gemeldet als erfolgreich",
              ergebnis["ergebnis"] == "rotiert", ergebnis["grund"])

        archive = lr.alte_staende(pfad)
        check("genau ein Archiv angelegt", len(archive) == 1, archive)
        with open(archive[0], "rb") as datei:
            gesichert = datei.read()
        check("Archiv ist byteweise identisch mit dem alten Inhalt",
              gesichert == inhalt,
              f"{len(gesichert)} statt {len(inhalt)} Bytes")
        check("gemeldete Byte-Zahl stimmt",
              ergebnis["gesichert"] == len(inhalt), ergebnis["gesichert"])
        check("Originaldatei ist leer", os.path.getsize(pfad) == 0)
        check("Originaldatei existiert weiter", os.path.isfile(pfad))
        check("Inode unveraendert - das ist der Grund, warum offene Handles "
              "weiter funktionieren",
              os.stat(pfad).st_ino == inode_vorher)
        check("Archivname endet nicht auf .log",
              not archive[0].endswith(".log"), archive[0])
        check("Archivname traegt eine Zeitmarke",
              lr.STAND_MUSTER.search(archive[0]) is not None, archive[0])


# ---------------------------------------------------------------------------
SCHREIBER = r"""
import os, sys, time
pfad, stopp = sys.argv[1], sys.argv[2]
n = 0
with open(pfad, "a", buffering=1) as datei:
    while not os.path.exists(stopp):
        n += 1
        datei.write("ZEILE %08d\n" % n)
        time.sleep(0.0002)
sys.stdout.write(str(n))
"""


SCHREIBER_TAKT = r"""
import os, sys, time
pfad, stopp, pause = sys.argv[1], sys.argv[2], float(sys.argv[3])
n = 0
with open(pfad, "a", buffering=1) as datei:
    while not os.path.exists(stopp):
        n += 1
        datei.write("ZEILE %08d\n" % n)
        time.sleep(pause)
sys.stdout.write(str(n))
"""


def _warte_auf_groesse(pfad, mindestens, sekunden=10.0):
    ende = time.time() + sekunden
    while time.time() < ende:
        if os.path.exists(pfad) and os.path.getsize(pfad) >= mindestens:
            return True
        time.sleep(0.01)
    return False


def _zeilennummern(text):
    nummern = set()
    for zeile in text.splitlines():
        if zeile.startswith("ZEILE ") and len(zeile) == 14:
            try:
                nummern.add(int(zeile[6:]))
            except ValueError:
                pass
    return nummern


def test_offener_schreibzugriff():
    print("\n5) Der Kernfall: ein anderer Prozess haelt die Datei offen")
    with Wegwerflogs() as w:
        os.makedirs(w.pfad("dienst"), exist_ok=True)
        pfad = w.pfad("dienst/dauerlaeufer.log")
        stopp = os.path.join(w.wurzel, "STOPP")

        prozess = subprocess.Popen(
            [sys.executable, "-c", SCHREIBER, pfad, stopp],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            bereit = _warte_auf_groesse(pfad, 3000)
            check("Schreiberprozess laeuft und fuellt die Datei", bereit,
                  f"{os.path.getsize(pfad) if os.path.exists(pfad) else 0} Bytes")
            inode_vorher = os.stat(pfad).st_ino

            ergebnis = lr.rotiere_eine(
                {"rel": "dienst/dauerlaeufer.log", "pfad": pfad,
                 "staende": 5, "groesse": os.path.getsize(pfad)})
            check("Rotation bei offenem Schreibzugriff erfolgreich",
                  ergebnis["ergebnis"] == "rotiert", ergebnis.get("grund"))

            groesse_direkt_danach = os.path.getsize(pfad)
            check("Datei ist unmittelbar nach der Rotation (fast) leer",
                  groesse_direkt_danach < 3000, groesse_direkt_danach)
            check("Inode unveraendert", os.stat(pfad).st_ino == inode_vorher)

            # DIE Zusicherung: der Prozess schreibt jetzt weiter - und zwar in
            # die neue, geleerte Datei, nicht ins Archiv.
            archiv_groesse_nach_rotation = os.path.getsize(ergebnis["archiv"])
            gewachsen = _warte_auf_groesse(pfad, groesse_direkt_danach + 2000)
            check("die NEUE Datei waechst weiter", gewachsen,
                  os.path.getsize(pfad))
            check("das Archiv waechst NICHT mehr",
                  os.path.getsize(ergebnis["archiv"])
                  == archiv_groesse_nach_rotation,
                  os.path.getsize(ergebnis["archiv"]))
            check("keine Nullbytes am Dateianfang (Anhaengemodus bestaetigt)",
                  open(pfad, "rb").read(64).count(b"\0") == 0)

            with open(stopp, "w") as datei:
                datei.write("halt")
            aus, err = prozess.communicate(timeout=30)
            check("Schreiber beendet sich ohne Fehler", not err.strip(), err[:200])
        finally:
            if not os.path.exists(stopp):
                with open(stopp, "w") as datei:
                    datei.write("halt")
            try:
                prozess.communicate(timeout=10)
            except Exception:                                # noqa: BLE001
                prozess.kill()


def _verlustmessung(pause, rotationen, wurzel):
    """Schreibt durchgehend mit `pause` Sekunden Abstand, rotiert `rotationen`
    mal und gibt (geschrieben, fehlend, unvollstaendige_enden) zurueck."""
    os.makedirs(os.path.join(wurzel, "m"), exist_ok=True)
    pfad = os.path.join(wurzel, "m", "dauer.log")
    stopp = os.path.join(wurzel, "STOPP_MESSUNG")
    prozess = subprocess.Popen(
        [sys.executable, "-c", SCHREIBER_TAKT, pfad, stopp, str(pause)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        for _ in range(rotationen):
            if not _warte_auf_groesse(pfad, 1500, sekunden=20.0):
                break
            lr.rotiere_eine({"rel": "m/dauer.log", "pfad": pfad,
                             "staende": 99, "groesse": os.path.getsize(pfad)})
            time.sleep(0.02)
        with open(stopp, "w") as datei:
            datei.write("halt")
        aus, _ = prozess.communicate(timeout=30)
        geschrieben = int(aus.strip())
    finally:
        if not os.path.exists(stopp):
            with open(stopp, "w") as datei:
                datei.write("halt")
        try:
            prozess.communicate(timeout=10)
        except Exception:                                    # noqa: BLE001
            prozess.kill()

    gefunden = set()
    unvollstaendig = 0
    for teil in sorted(lr.alte_staende(pfad)) + [pfad]:
        with open(teil, "rb") as datei:
            roh = datei.read()
        if roh and not roh.endswith(b"\n"):
            unvollstaendig += 1
        gefunden |= _zeilennummern(roh.decode("utf-8", "replace"))
    erwartet = set(range(1, geschrieben + 1))
    return geschrieben, sorted(erwartet - gefunden), unvollstaendig, gefunden


def test_verlustfenster():
    print("\n6) Das Restfenster zwischen Sichern und Leeren, beziffert")

    # a) Realistische Rate. Der schreibfreudigste Dienst des Projekts ist das
    #    uvicorn-Fehlerlog mit einer Handvoll Zeilen je Anfrage; 200 Zeilen je
    #    Sekunde liegen weit darueber. Hier darf NICHTS verloren gehen.
    with Wegwerflogs() as w:
        geschrieben, fehlend, unvollstaendig, gefunden = _verlustmessung(
            0.005, 5, w.wurzel)
        check(f"200 Zeilen/s, 5 Rotationen: alle {geschrieben} Zeilen da",
              not fehlend, f"{len(fehlend)} fehlen: {fehlend[:10]}")
        check("keine Zeile wurde zerrissen", unvollstaendig == 0, unvollstaendig)
        check("keine Zeile doppelt",
              not (gefunden - set(range(1, geschrieben + 1))))

    # c) Der scharfe Nachweis der REIHENFOLGE, ohne Timing-Glueck: fsync wird
    #    kuenstlich langsam gemacht. Liegt irgendein fsync zwischen dem letzten
    #    Lesevorgang und dem Leeren, kostet das bei 200 Zeilen/s sofort ein
    #    Dutzend Zeilen. Liegt keines dort, kostet es null - beliebig langsam.
    #
    #    Zugesichert wird nur das: ein langsames fsync darf keine Zeile kosten.
    #    Ob die Rotation dabei durchlaeuft, ist offen - bei absichtlich zaehem
    #    fsync kann die Nachlese abbrechen, und ein Abbruch leert nichts.
    with Wegwerflogs() as w:
        echter_ordner = lr._fsync_ordner
        aufrufe = []

        def zaeher_ordner(ziel):
            aufrufe.append(ziel)
            time.sleep(0.1)
            return echter_ordner(ziel)

        lr._fsync_ordner = zaeher_ordner
        try:
            geschrieben, fehlend, unvollstaendig, _ = _verlustmessung(
                0.005, 2, w.wurzel)
        finally:
            lr._fsync_ordner = echter_ordner
        check("ein 100 ms langes fsync kostet keine einzige Zeile - es liegt "
              "nie zwischen dem letzten Lesen und dem Leeren",
              not fehlend,
              f"{len(fehlend)} von {geschrieben} fehlen: {fehlend[:10]}")
        check("auch dabei wird keine Zeile zerrissen",
              unvollstaendig == 0, unvollstaendig)
        check("je Rotation genau EIN fsync auf den Verzeichniseintrag",
              len(aufrufe) == 2, f"{len(aufrufe)} Aufrufe bei 2 Rotationen")

    # Derselbe Zaehler ohne Nebenwirkung, damit die Aussage auch ohne
    # laufenden Schreiber festgenagelt ist: nicht null (der Name des Archivs
    # muss dauerhaft werden) und nicht zwei (der zweite laege im heiklen Teil).
    with Wegwerflogs() as w:
        pfad = w.schreibe("dienst/zaehl.log", fuellung(3000, b"z"))
        echter_ordner = lr._fsync_ordner
        aufrufe = []
        lr._fsync_ordner = lambda ziel: aufrufe.append(ziel) or echter_ordner(ziel)
        try:
            ergebnis = lr.rotiere_eine({"rel": "dienst/zaehl.log",
                                        "pfad": pfad, "staende": 5,
                                        "groesse": 3000})
        finally:
            lr._fsync_ordner = echter_ordner
        check("Rotation erfolgreich", ergebnis["ergebnis"] == "rotiert",
              ergebnis.get("grund"))
        check("genau ein fsync auf den Verzeichniseintrag, nicht null und "
              "nicht zwei", len(aufrufe) == 1, aufrufe)

    # b) Extreme Rate, 25-fach, 10 Rotationen. Hier IST das Fenster messbar,
    #    die Zusicherung ist deshalb eine Obergrenze statt "nichts".
    #
    #    Die Grenze 3 ist gemessen, nicht geraten: ueber je sechs Durchgaenge
    #    verlor die richtige Reihenfolge hoechstens EINE Zeile je 10 Rotationen,
    #    ein hinter den letzten Lesevorgang verschobener fsync dagegen SECHS bis
    #    ZEHN. 3 liegt mit Abstand zwischen beidem - der Test erkennt die
    #    Verschiebung also, ohne bei richtiger Reihenfolge zu wackeln.
    with Wegwerflogs() as w:
        geschrieben, fehlend, unvollstaendig, _ = _verlustmessung(
            0.0002, 10, w.wurzel)
        anteil = 100.0 * len(fehlend) / max(geschrieben, 1)
        check(f"5.000 Zeilen/s, 10 Rotationen: hoechstens 3 Zeilen "
              f"({len(fehlend)} von {geschrieben} = {anteil:.3f} %)",
              len(fehlend) <= 3, fehlend[:10])
        check("die Verluste sind einzelne Zeilen, kein Block",
              all(b - a > 1 for a, b in zip(fehlend, fehlend[1:])), fehlend)
        check("auch hier wird keine Zeile zerrissen",
              unvollstaendig == 0, unvollstaendig)


def test_staende():
    print("\n7) Alte Staende: behalten und loeschen")
    with Wegwerflogs() as w:
        pfad = w.schreibe("dienst/viel.log", fuellung(2000))
        marken = [f"2026-09-0{i}T00-00-00" for i in range(1, 8)]
        for marke in marken:
            with open(f"{pfad}.{marke}", "wb") as datei:
                datei.write(marke.encode())
        fremd = f"{pfad}.1"
        with open(fremd, "wb") as datei:
            datei.write(b"Archiv eines RotatingFileHandler")

        check("alte Staende werden gefunden",
              len(lr.alte_staende(pfad)) == 7, lr.alte_staende(pfad))
        check("Fremdarchiv .log.1 gilt nicht als eigener Stand",
              fremd not in lr.alte_staende(pfad))

        ergebnis = lr.rotiere_eine({"rel": "dienst/viel.log", "pfad": pfad,
                                    "staende": 5, "groesse": 2000})
        check("Rotation erfolgreich", ergebnis["ergebnis"] == "rotiert",
              ergebnis.get("grund"))
        uebrig = lr.alte_staende(pfad)
        check("es bleiben genau 5 Staende", len(uebrig) == 5, uebrig)
        check("geloescht wurden die 3 aeltesten",
              len(ergebnis["geloescht"]) == 3, ergebnis["geloescht"])
        check("der aelteste Stand ist weg",
              not os.path.exists(f"{pfad}.2026-09-01T00-00-00"))
        check("die NEUESTEN Staende sind erhalten (nicht die aeltesten)",
              all(os.path.basename(p) > os.path.basename(f"{pfad}.2026-09-02T00-00-00")
                  or p.endswith("2026-09-03T00-00-00") for p in uebrig),
              [os.path.basename(p) for p in uebrig])
        check("das neue Archiv ist der neueste Stand",
              uebrig[-1] == ergebnis["archiv"], uebrig[-1])
        check("Fremdarchiv .log.1 wurde NICHT geloescht",
              os.path.exists(fremd))

        # Mehr Staende fuer die Bruecken-Protokolle.
        staende, _ = lr.einstellung(os.path.join("broker", "testnet_spiegel.log"))
        check("testnet_spiegel.log behaelt mehr Staende",
              staende == lr.MEHR_STAENDE, staende)
        staende, _ = lr.einstellung(os.path.join("broker", "ibkr_paper_spiegel.log"))
        check("ibkr_paper_spiegel.log behaelt mehr Staende",
              staende == lr.MEHR_STAENDE, staende)
        check("mehr Staende sind deutlich mehr als der Standard",
              lr.MEHR_STAENDE >= 4 * lr.STANDARD_STAENDE,
              f"{lr.MEHR_STAENDE} vs {lr.STANDARD_STAENDE}")
        staende, _ = lr.einstellung(os.path.join("t3_supertrend", "cron.log"))
        check("normales Log behaelt den Standard",
              staende == lr.STANDARD_STAENDE, staende)


def test_fehlschlag():
    print("\n8) Fehlschlag stoppt nichts und loescht nichts Ungesichertes")
    with Wegwerflogs() as w:
        kaputt = w.schreibe("a/kaputt.log", fuellung(2000, b"k"))
        gut = w.schreibe("b/gut.log", fuellung(2000, b"g"))
        alt = f"{kaputt}.2026-09-01T00-00-00"
        with open(alt, "wb") as datei:
            datei.write(b"alter Stand")

        # Der Zielpfad zeigt in einen Ordner, den es nicht gibt: das Archiv
        # kann nicht angelegt werden.
        original = lr.archivname

        def kaputter_name(pfad, jetzt=None):
            if pfad.endswith("kaputt.log"):
                return os.path.join(pfad + ".gibt_es_nicht", "archiv")
            return original(pfad, jetzt)

        lr.archivname = kaputter_name
        try:
            ergebnisse = {e["rel"]: e for e in lr.rotiere(w.wurzel, schwelle=100)}
        finally:
            lr.archivname = original

        rel_kaputt = os.path.join("a", "kaputt.log")
        rel_gut = os.path.join("b", "gut.log")
        check("Fehlschlag wird als solcher gemeldet",
              ergebnisse[rel_kaputt]["ergebnis"] == "fehlgeschlagen",
              ergebnisse[rel_kaputt]["ergebnis"])
        check("die fehlgeschlagene Datei wurde NICHT geleert",
              os.path.getsize(kaputt) == 2000, os.path.getsize(kaputt))
        check("ihr Inhalt ist unveraendert",
              open(kaputt, "rb").read() == fuellung(2000, b"k"))
        check("ihr alter Stand wurde NICHT geloescht", os.path.exists(alt))
        check("kein halbes Archiv liegt herum",
              lr.alte_staende(kaputt) == [alt], lr.alte_staende(kaputt))
        check("die ANDERE Datei wurde trotzdem rotiert",
              ergebnisse[rel_gut]["ergebnis"] == "rotiert",
              ergebnisse[rel_gut].get("grund"))
        check("die andere Datei ist geleert", os.path.getsize(gut) == 0)

        rueck = lr.main(["--wurzel", w.wurzel, "--schwelle", "100"])
        check("ein Lauf ohne faellige Datei meldet Erfolg", rueck == 0, rueck)

        lr.archivname = kaputter_name
        try:
            with open(kaputt, "wb") as datei:
                datei.write(fuellung(2000, b"k"))
            rueck = lr.main(["--wurzel", w.wurzel, "--schwelle", "100"])
        finally:
            lr.archivname = original
        check("ein Lauf MIT Fehlschlag meldet Rueckgabewert 1", rueck == 1, rueck)


def test_wachstum_bricht_ab():
    print("\n9) Waechst die Datei schneller als wir kopieren, wird nicht geleert")
    with Wegwerflogs() as w:
        pfad = w.schreibe("dienst/schnell.log", fuellung(2000, b"s"))
        vorher = lr.MAX_NACHLESE_RUNDEN
        lr.MAX_NACHLESE_RUNDEN = 0
        try:
            ergebnis = lr.rotiere_eine({"rel": "dienst/schnell.log",
                                        "pfad": pfad, "staende": 5,
                                        "groesse": 2000})
        finally:
            lr.MAX_NACHLESE_RUNDEN = vorher
        check("Abbruch wird als Fehlschlag gemeldet",
              ergebnis["ergebnis"] == "fehlgeschlagen", ergebnis["ergebnis"])
        check("Abbruchgrund benennt das Wachstum",
              "waechst schneller" in ergebnis["grund"], ergebnis["grund"])
        check("die Datei wurde NICHT geleert",
              os.path.getsize(pfad) == 2000, os.path.getsize(pfad))

    print("\n10) Unvollstaendiges Archiv wird nie zum Leeren freigegeben")
    with Wegwerflogs() as w:
        pfad = w.schreibe("dienst/pruef.log", fuellung(2000, b"p"))

        class KleinerStat:
            st_size = 7

        echtes_fstat = os.fstat
        os.fstat = lambda fd: KleinerStat()
        try:
            ergebnis = lr.rotiere_eine({"rel": "dienst/pruef.log",
                                        "pfad": pfad, "staende": 5,
                                        "groesse": 2000})
        finally:
            os.fstat = echtes_fstat
        check("Groessenabweichung wird als Fehlschlag gemeldet",
              ergebnis["ergebnis"] == "fehlgeschlagen", ergebnis["ergebnis"])
        check("Grund benennt die Abweichung",
              "wird NICHT geleert" in ergebnis["grund"], ergebnis["grund"])
        check("die Datei wurde NICHT geleert",
              os.path.getsize(pfad) == 2000, os.path.getsize(pfad))


def test_kein_ueberschreiben():
    print("\n11) Ein vorhandenes Archiv wird nie ueberschrieben")
    with Wegwerflogs() as w:
        pfad = w.schreibe("dienst/kollision.log", fuellung(2000, b"n"))
        belegt = f"{pfad}.2026-09-01T00-00-00"
        with open(belegt, "wb") as datei:
            datei.write(b"darf nicht verloren gehen")

        original = lr.archivname
        lr.archivname = lambda p, jetzt=None: belegt
        try:
            ergebnis = lr.rotiere_eine({"rel": "dienst/kollision.log",
                                        "pfad": pfad, "staende": 5,
                                        "groesse": 2000})
        finally:
            lr.archivname = original
        check("Rotation auf einen belegten Namen schlaegt fehl",
              ergebnis["ergebnis"] == "fehlgeschlagen", ergebnis["ergebnis"])
        check("der belegte Stand ist unveraendert",
              open(belegt, "rb").read() == b"darf nicht verloren gehen")
        check("die Logdatei wurde nicht geleert",
              os.path.getsize(pfad) == 2000)

        # Zwei Rotationen in derselben Sekunde bekommen verschiedene Namen.
        pfad2 = w.schreibe("dienst/zweimal.log", fuellung(2000, b"z"))
        fest = __import__("datetime").datetime(2026, 9, 12, 7, 40, 0)
        eins = lr.archivname(pfad2, fest)
        with open(eins, "wb") as datei:
            datei.write(b"erster")
        zwei = lr.archivname(pfad2, fest)
        check("gleiche Sekunde ergibt unterschiedliche Archivnamen",
              eins != zwei, f"{os.path.basename(eins)} / {os.path.basename(zwei)}")
        check("der zweite Name bleibt ein erkennbarer Stand",
              lr.STAND_MUSTER.search(zwei) is not None, zwei)


def _handler_argumente(quelle):
    """maxBytes und backupCount des RotatingFileHandler aus einer Quelldatei -
    per AST, damit die Werte in log_rotation.py nicht von den echten
    Einstellungen abdriften koennen."""
    with open(os.path.join(BASE_DIR, quelle), "r", encoding="utf-8") as datei:
        baum = ast.parse(datei.read())
    for knoten in ast.walk(baum):
        if (isinstance(knoten, ast.Call)
                and getattr(knoten.func, "id", "") == "RotatingFileHandler"):
            werte = {}
            for schlagwort in knoten.keywords:
                if isinstance(schlagwort.value, ast.Constant):
                    werte[schlagwort.arg] = schlagwort.value.value
            if "maxBytes" in werte:
                return werte.get("maxBytes"), werte.get("backupCount")
    return None, None


def test_selbstrotierende():
    print("\n12) Dateien, die sich selbst rotieren, bleiben unberuehrt")
    with Wegwerflogs() as w:
        for rel in lr.SELBSTROTIEREND:
            w.schreibe(rel, fuellung(5_000_000, b"r"))
        eintraege = {e["rel"]: e for e in lr.plan(w.wurzel, schwelle=1000)}
        for rel in lr.SELBSTROTIEREND:
            check(f"{rel} wird nicht rotiert",
                  not eintraege[rel]["rotieren"], eintraege[rel]["grund"])
            check(f"{rel} nennt den Grund",
                  "rotiert selbst" in eintraege[rel]["grund"],
                  eintraege[rel]["grund"])
        lr.rotiere(w.wurzel, schwelle=1000)
        for rel in lr.SELBSTROTIEREND:
            check(f"{rel} ist nach dem Lauf unveraendert gross",
                  os.path.getsize(w.pfad(rel)) == 5_000_000)
            check(f"{rel} hat kein Archiv von uns",
                  lr.alte_staende(w.pfad(rel)) == [])

    for rel, (quelle, max_bytes, staende) in lr.SELBSTROTIEREND.items():
        echte_bytes, echte_staende = _handler_argumente(quelle)
        check(f"maxBytes in {quelle} stimmt mit der Angabe hier ueberein",
              echte_bytes == max_bytes, f"{echte_bytes} vs {max_bytes}")
        check(f"backupCount in {quelle} stimmt mit der Angabe hier ueberein",
              echte_staende == staende, f"{echte_staende} vs {staende}")


def test_grenzen_des_skripts():
    print("\n13) Was das Skript nicht anfasst")
    with open(os.path.join(_DIR, "log_rotation.py"), "r",
              encoding="utf-8") as datei:
        quelle = datei.read()
    baum = ast.parse(quelle)
    importe = set()
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            importe |= {a.name.split(".")[0] for a in knoten.names}
        elif isinstance(knoten, ast.ImportFrom) and knoten.module:
            importe.add(knoten.module.split(".")[0])
    for verboten in ("forward_test", "live_params", "equity_simulation",
                     "spiegel", "ibkr_spiegel", "bot_db"):
        check(f"importiert kein {verboten}", verboten not in importe, importe)
    check("nur Standardbibliothek",
          importe <= {"argparse", "glob", "logging", "os", "re", "sys",
                      "datetime"}, importe)
    check("kein Aufruf von os.rename/shutil.move (das waere der Fehler, "
          "den diese Aufgabe vermeidet)",
          "os.rename" not in quelle and "shutil.move" not in quelle)
    check("kein --echt und kein Order-Begriff", "--echt" not in quelle)
    check("truncate wird benutzt", "truncate(0)" in quelle)


def test_dokumentation():
    print("\n14) Dokumentation")
    check("README vorhanden", os.path.isfile(README), README)
    if not os.path.isfile(README):
        return
    with open(README, "r", encoding="utf-8") as datei:
        text = datei.read()
    check("README erklaert kopieren-und-leeren statt umbenennen",
          "truncate" in text and ("Inode" in text or "inode" in text))
    check("README nennt die Schwelle",
          str(lr.STANDARD_SCHWELLE) in text or "1 MB" in text)
    check("README nennt die Zahl der Staende",
          str(lr.STANDARD_STAENDE) in text)
    check("README nennt die Sonderbehandlung der Bruecken-Protokolle",
          "testnet_spiegel" in text and str(lr.MEHR_STAENDE) in text)
    check("README nennt die selbstrotierenden Dateien",
          "telegram_bot.log" in text and "manuelle_eingriffe.log" in text)
    check("README enthaelt eine Cron-Zeile fuer das Skript",
          "system/log_rotation.py" in text and "* * *" in text)
    check("README sagt, dass die Cron-Zeile NICHT eingetragen ist",
          "nicht eingetragen" in text.lower())
    check("README benennt das Restfenster zwischen Sichern und Leeren",
          "Restfenster" in text or "Fenster" in text)
    check("README erwaehnt newsyslog und warum nicht",
          "newsyslog" in text)


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("Selbsttests der Log-Rotation")
    print("=" * 78)
    tests = [test_auswahl, test_symlink_und_grenze, test_schwelle,
             test_inhalt_und_inode, test_offener_schreibzugriff,
             test_verlustfenster, test_staende, test_fehlschlag, test_wachstum_bricht_ab,
             test_kein_ueberschreiben, test_selbstrotierende,
             test_grenzen_des_skripts, test_dokumentation]
    for test in tests:
        try:
            test()
        except Exception as fehler:                          # noqa: BLE001
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
