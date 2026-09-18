#!/usr/bin/env python3
"""
Selbsttests zu TB-46/47/49: die Wache ueber `shared/snapshot.py`
==============================================================================
Der Snapshot ist die Grundlage des Selektionslaufs. Wenn das Werkzeug, das ihn
zieht, eine Abweichung uebersieht, faellt das **niemals** auf: ein Snapshot,
der nicht zu seinem Namen passt, sieht genauso aus wie einer, der passt.

DIE LEHRE AUS TB-45, UND WARUM SIE HIER DIE BAUFORM BESTIMMT
------------------------------------------------------------------------------
In TB-45 meldeten zwei Wachen "bestanden" - eine davon mit **28 gruenen
Pruefungen, ohne etwas gemessen zu haben**. Ein gescheiterter Aufruf und ein
leeres Ergebnis sahen gleich aus. Daraus folgt hier dreierlei:

  1. **Der Rueckgabewert wird geprueft, bevor das Ergebnis gelesen wird.**
     Jeder Prueflauf geht durch `main()` in einem eigenen Prozess; geprueft
     wird zuerst der Wert (0 / 1 / 2), dann der Text.
  2. **"Konnte nicht messen" ist ein eigener, roter Ausgang.** Ein fehlendes
     oder beschaedigtes Manifest ergibt **2**, nicht 0 und nicht 1. Eine
     Datei, deren Quersumme sich nicht bilden laesst, ergibt **2** - nicht
     "veraendert", denn ob sie sich geaendert hat, ist gerade nicht bekannt.
  3. **Eine Probe, die nur rot sein kann, beweist nichts.** Zu jeder
     Mutationsprobe gehoert die **Negativ-Probe** am unberuehrten Snapshot:
     der muss gruen sein.

WIE DIE PROBEN ZEIGEN, DASS SIE BEISSEN
------------------------------------------------------------------------------
Der Auftrag verlangt: *jede Probe muss am Stand ohne die Reparatur wirklich
durchfallen - das ist zu zeigen, nicht zu behaupten.* `shared/snapshot.py` ist
neu; einen "Stand ohne die Reparatur" gibt es nicht als Commit. Er wird
deshalb **hergestellt**: Abschnitt 3 laedt den Quelltext, **entfernt eine
einzelne Wache im Speicher**, fuehrt das Ergebnis als eigenes Modul aus und
laesst dieselbe Probe erneut laufen.

    echtes Modul   -> muss die Abweichung FINDEN
    ohne die Wache -> muss sie UEBERSEHEN

Findet die Fassung ohne Wache die Abweichung auch, dann prueft die Probe eine
andere Stelle als angenommen, und das ist ein Befund ueber den Test, nicht
ueber das Werkzeug. ⚠️ Findet sich der Ankertext einer Mutation nicht mehr im
Quelltext, ist die Probe **rot** - nicht uebersprungen: eine Wache, die
umgezogen ist, ist eine Wache, die dieser Test nicht mehr bewacht.

DER GEFAEHRLICHSTE FALL, UND WARUM ER EIGENS VORKOMMT
------------------------------------------------------------------------------
Eine **hinzugefuegte Datei, die nicht `.csv` heisst**, aendert den
Datenstand-Hash nicht (das Verfahren zaehlt nur `*.csv`). Wer nur die
Manifesteintraege durchgeht oder nur den Gesamthash vergleicht, sieht sie
nicht. Nur der Vergleich in **beide** Richtungen findet sie. Genau dieser Fall
ist die Probe 3f.

DIE AUSNAHME IST EINE REGEL - UND SIE WIRD ALS SOLCHE GEPRUEFT (TB-49)
------------------------------------------------------------------------------
Registertext 5a, Zusatz (Abschnitt 17.3) laesst `rand_erste` an der ersten
Kerze zu, wenn die Kerze das Aggregat genau der vorhandenen feineren Kerzen
ist. Abschnitt 3c prueft **die Regel**, nicht die 36 Dateien, die sie heute
trifft: er baut einen Wegwerf-Bestand mit genau diesen 36 Befunden und stellt
daneben die vier Faelle, die weiterhin abbrechen muessen.

⚠️ **Zwei davon lassen sich aus Kursdateien nicht herstellen** - ein
`rand_erste` an einer spaeteren Kerze und einer ohne Deckungspruefung. Die
heutige `zeitabdeckung.py` vergibt beides nicht. Sie werden deshalb
**gestellt** (`_stubpruefung`): `snapshot.py` darf sich nicht darauf
verlassen, dass seine Eingabe wohlgeformt ist. Wer Bedingung (b) aus dem Namen
der Befundart folgert, prueft nichts.

WAS DIESER TEST NICHT ANFASST
------------------------------------------------------------------------------
⚠️ `data/` wird **ausschliesslich gelesen** - einmal, um nachzuweisen, dass
das Werkzeug den registrierten Datenstand-Hash reproduziert. Gezogen wird
nur in Wegwerf-Verzeichnisse unter `tempfile.mkdtemp()`. Abschnitt 5 misst
den Datenstand vor und nach dem Lauf und vergleicht beide.

Keine Bot-Datei wird importiert. Kein Test-Framework, wie in allen uebrigen
Selbsttests dieses Projekts.

Nutzung:  python3 shared/test_snapshot.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import types

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

import snapshot                                             # noqa: E402

SNAPSHOT_PFAD = os.path.join(_SHARED, "snapshot.py")
DATA_DIR = os.path.join(BASE_DIR, "data")

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print("  [OK ] %s%s" % (name, "   " + detail if detail else ""))
    else:
        FEHLER.append(name)
        print("  [FEHLER] %s%s" % (name, "   " + detail if detail else ""))


# ---------------------------------------------------------------------------
# Werkzeuge der Proben
# ---------------------------------------------------------------------------

def _quelle_bauen(ordner, kursdateien=("TESTUSDT_1d.csv", "ZZZ_1h.csv"),
                  beigabe=None):
    """Ein Wegwerf-`data/` mit ein paar Zeilen je Datei.

    ⚠️ **TB-47: die Zeitstempel muessen zum Intervall passen.** Seit TB-47
    laeuft vor jedem Ziehen die Teilkerzen-Pruefung ueber die Quelle, und die
    liest `open_time` nach dem Format ihres Intervalls: `1d` **ohne**
    Uhrzeit, `1h`/`4h` **mit**. Eine Wegwerf-Quelle mit `2026-01-01 00:00:00`
    in einer `_1d.csv` ist fuer die Pruefung `unlesbar` - und dann bricht
    jedes Ziehen ab, bevor die Probe ueberhaupt zu ihrer Frage kommt.

    Die Zeitpunkte liegen ausserdem in der **Vergangenheit**, damit die
    letzte Kerze abgelaufen ist (die Wache `S - Stand`).
    """
    os.makedirs(ordner, exist_ok=True)
    for i, name in enumerate(kursdateien):
        tages = name.endswith("_1d.csv")
        with open(os.path.join(ordner, name), "w", encoding="utf-8") as f:
            f.write("open_time,open,high,low,close,volume\n")
            for tag in (1, 2):
                stempel = ("2026-01-0%d" % tag if tages
                           else "2026-01-0%d 00:00:00" % tag)
                f.write("%s,%d,%d,%d,%d,%d\n"
                        % (stempel, i + 1, i + 2, i, i + 1, 10 * (i + 1)))
    if beigabe:
        for name, inhalt in beigabe.items():
            ziel = os.path.join(ordner, name)
            os.makedirs(os.path.dirname(ziel), exist_ok=True)
            with open(ziel, "w", encoding="utf-8") as f:
                f.write(inhalt)
    return ordner


def _wurzel_bauen(ordner, eingaben=None):
    """Eine Wegwerf-Wurzel mit den Eingaben der Liste (TB-47).

    Die Eingaben liegen **nicht** in der Quelle, sondern neben ihr - genau
    wie `config/` neben `data/` liegt.
    """
    eingaben = eingaben or {"config/liste.txt": "AAA\nBBB\n"}
    for rel, inhalt in eingaben.items():
        ziel = os.path.join(ordner, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as f:
            f.write(inhalt)
    return ordner, sorted(eingaben)


def _lauf(*argumente):
    """`snapshot.py` in einem eigenen Prozess. (Rueckgabewert, Ausgabe).

    Eigener Prozess, weil der Rueckgabewert der Befehlszeile geprueft wird -
    genau der Wert, den ein Cronjob oder ein Testauftrag sieht. Ein Aufruf von
    `main()` im selben Prozess wuerde den Weg ueber `sys.exit` nicht messen.
    """
    lauf = subprocess.run([sys.executable, SNAPSHOT_PFAD] + list(argumente),
                          capture_output=True, text=True)
    return lauf.returncode, (lauf.stdout or "") + (lauf.stderr or "")


def _mutiert(name, ersetzungen):
    """`snapshot.py` mit entfernter Wache - als eigenes Modul im Speicher.

    ⚠️ Der Ankertext muss gefunden werden. Ein `replace`, das nichts trifft,
    liefert eine unveraenderte Fassung - und die Probe waere dann gruen, ohne
    etwas gezeigt zu haben. Das ist derselbe stille Ausfall, gegen den dieser
    Test geschrieben ist, nur eine Ebene hoeher.
    """
    with open(SNAPSHOT_PFAD, "r", encoding="utf-8") as f:
        text = f.read()
    for alt, neu in ersetzungen:
        if alt not in text:
            raise AssertionError(
                "Ankertext der Mutation `%s` steht nicht mehr in snapshot.py: "
                "%r" % (name, alt[:70]))
        text = text.replace(alt, neu, 1)
    modul = types.ModuleType("snapshot_ohne_" + name)
    modul.__file__ = SNAPSHOT_PFAD
    exec(compile(text, "<snapshot ohne %s>" % name, "exec"), modul.__dict__)
    return modul


def _zieht(modul, quelle, ziel, wurzel=None, eingaben=None):
    """(gelungen, Grund) - zieht mit dem uebergebenen Modul.

    ⚠️ **TB-47: `anker=False`.** Eine Wegwerf-Quelle kann den verankerten
    `datenstand_hash` `d9449faf…` nicht treffen; stuende der Anker hier
    scharf, braeche **jede** Probe an ihm ab - und zwar bevor sie zu der
    Wache kommt, die sie meint. Die Proben waeren dann alle rot und wuerden
    trotzdem nichts ueber ihre Wache aussagen. Der Anker ist Gegenstand von
    Probe 3o, nicht Rahmenbedingung der uebrigen.

    Ohne `eingaben` wird mit **leerer** Liste gezogen: die Probe prueft dann
    nur die Kursdateien, und das genuegt ihr.
    """
    try:
        bericht = modul.ziehen(quelle, ziel, wirklich=True, anker=False,
                               wurzel=wurzel or os.path.dirname(quelle),
                               eingaben=eingaben or ())
        return bool(bericht.get("gezogen")), None
    except Exception as fehler:                              # noqa: BLE001
        return False, str(fehler)


# ===========================================================================
# Abschnitt 1 - Das Hash-Verfahren ist das registrierte
# ===========================================================================

def abschnitt_1():
    print("\n1. DER HASH IST DER REGISTRIERTE - nicht ein zweiter daneben")

    # Das Soll kommt aus dem Register, nicht aus diesem Test: eine hier
    # abgetippte Zahl waere die Doppelfuehrung, die das Projekt schon
    # zweimal eingesammelt hat.
    register_pfad = os.path.join(BASE_DIR, "research", "etf_trendfolge",
                                 "register.py")
    soll_hash, soll_anzahl = None, None
    if os.path.exists(register_pfad):
        # ⚠️ Die Konstante steht ueber zwei Zeilen fortgesetzt. Sie wird
        # deshalb als Quelltext ausgewertet, nicht zeilenweise zerschnitten -
        # ein `startswith`-Filter bekaeme nur die erste Haelfte des Hashes.
        try:
            eigen = {}
            with open(register_pfad, "r", encoding="utf-8") as f:
                quelltext = f.read()
            beginn = quelltext.index("DATENSTAND_SOLL")
            ende = quelltext.index("\n\n", beginn)
            exec(compile(quelltext[beginn:ende], "<register>", "exec"), eigen)
            soll_hash = eigen.get("DATENSTAND_SOLL")
            soll_anzahl = eigen.get("DATENSTAND_DATEIEN_SOLL")
        except Exception as fehler:                          # noqa: BLE001
            check("das registrierte Soll ist auslesbar", False, str(fehler))

    check("das registrierte Soll ist auslesbar",
          bool(soll_hash) and bool(soll_anzahl),
          "%s... / %s" % (str(soll_hash)[:16], soll_anzahl))

    if not soll_hash:
        return

    if not os.path.isdir(DATA_DIR):
        # Kein stillschweigendes Ueberspringen: hier gibt es nichts zu messen,
        # und das ist ein roter Ausgang, kein gruener.
        check("data/ ist vorhanden, um den Hash nachzurechnen", False,
              "%s fehlt" % DATA_DIR)
        return

    ist_hash, ist_anzahl = snapshot.gesamthash(DATA_DIR)
    check("snapshot.gesamthash(data/) reproduziert den registrierten Hash",
          ist_hash == soll_hash and ist_anzahl == soll_anzahl,
          "%s... / %d" % (ist_hash[:16], ist_anzahl))

    # Und dass er dasselbe rechnet wie die Quelle des Verfahrens - nicht
    # zufaellig dieselbe Zahl, sondern dieselbe Funktion.
    herkunft = snapshot.lade_herkunft()
    check("er kommt aus herkunft.datenstand, nicht aus einer eigenen Rechnung",
          herkunft.datenstand(DATA_DIR)["datenstand"] == ist_hash)

    # Faellt die Quelle des Verfahrens aus, wird NICHT ersatzweise selbst
    # gerechnet.
    try:
        snapshot.lade_herkunft(os.path.join(BASE_DIR, "gibt_es_nicht.py"))
        gebissen = False
    except snapshot.Snapshotfehler:
        gebissen = True
    check("fehlt das Verfahren, bricht es ab statt selbst zu rechnen", gebissen)


# ===========================================================================
# Abschnitt 2 - Ziehen, Manifest, Gegenpruefung
# ===========================================================================

def abschnitt_2():
    print("\n2. ZIEHEN - Manifest, Zeitstempel, Gegenpruefung")
    arbeit = tempfile.mkdtemp(prefix="tb46_ziehen_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"))
        # ⚠️ TB-47: die Nicht-Kursdatei liegt jetzt in der **Wurzel**, nicht
        # in der Quelle. Eine Datei neben den Kursdateien in der Quelle ist
        # seit TB-47 ein Abbruchgrund (siehe Probe 3n) - aufgenommen wird,
        # was in der Liste steht, und die Liste zeigt auf die Wurzel.
        wurzel, liste = _wurzel_bauen(os.path.join(arbeit, "wurzel"),
                                      {"config/NOTIZ.json": '{"x": 1}\n'})
        ziel = os.path.join(arbeit, "snapshots")
        gemeinsam = ["--quelle", quelle, "--ziel", ziel, "--wurzel", wurzel,
                     "--kein-anker"]
        for e in liste:
            gemeinsam += ["--eingabe", e]

        # Trockenlauf: er darf nichts anlegen. Die Voreinstellung ist der
        # Trockenlauf - dieselbe Bauform wie kursdaten_neuaufbau.py.
        rc, ausgabe = _lauf(*gemeinsam)
        check("Trockenlauf: Rueckgabewert 0", rc == 0, "rc=%d" % rc)
        check("Trockenlauf legt nichts an", not os.path.exists(ziel))
        check("Trockenlauf sagt, dass er einer ist", "TROCKENLAUF" in ausgabe)

        # Wirklich ziehen
        rc, ausgabe = _lauf(*(gemeinsam + ["--ziehen"]))
        check("Ziehen: Rueckgabewert 0", rc == 0, "rc=%d" % rc)
        hash_, anzahl = snapshot.gesamthash(quelle)
        paare = {"TESTUSDT_1d.csv": snapshot.quersumme(
                     os.path.join(quelle, "TESTUSDT_1d.csv")),
                 "ZZZ_1h.csv": snapshot.quersumme(
                     os.path.join(quelle, "ZZZ_1h.csv")),
                 "config/NOTIZ.json": snapshot.quersumme(
                     os.path.join(wurzel, "config", "NOTIZ.json"))}
        name_ = snapshot.snapshot_hash(paare)
        snap = os.path.join(ziel, name_)
        check("der Zielordner heisst wie der snapshot_hash der Eingaben",
              os.path.isdir(snap), snap)

        # Vollstaendigkeit: auch die Datei, die nicht in den Datenstand eingeht
        vorhanden = sorted(os.listdir(snap))
        check("die Kursdateien liegen flach, das Manifest daneben",
              vorhanden == ["MANIFEST.json", "TESTUSDT_1d.csv", "ZZZ_1h.csv",
                            "config"], str(vorhanden))
        check("die Nicht-Kursdatei ist da - mit ihrer Ordnerstruktur",
              os.path.isfile(os.path.join(snap, "config", "NOTIZ.json")))

        # Zeitstempel
        gleich = all(
            int(os.path.getmtime(os.path.join(quelle, n))) ==
            int(os.path.getmtime(os.path.join(snap, n)))
            for n in ("TESTUSDT_1d.csv", "ZZZ_1h.csv"))
        gleich = gleich and (
            int(os.path.getmtime(os.path.join(wurzel, "config", "NOTIZ.json")))
            == int(os.path.getmtime(os.path.join(snap, "config",
                                                 "NOTIZ.json"))))
        check("die Zeitstempel sind erhalten (copy2)", gleich)

        with open(os.path.join(snap, "MANIFEST.json"), encoding="utf-8") as f:
            manifest = json.load(f)
        check("das Manifest nennt Gesamthash und Dateizahl",
              manifest["datenstand_hash"] == hash_
              and manifest["kursdateien"] == anzahl == 2,
              "%s... / %s" % (manifest["datenstand_hash"][:16],
                              manifest["kursdateien"]))
        check("das Manifest nennt je Datei Name, Groesse und Quersumme",
              all(set(e) >= {"sha256", "bytes"}
                  for e in manifest["dateien"].values())
              and len(manifest["dateien"]) == 3)
        check("der Zeitpunkt steht in UTC",
              manifest["zeitpunkt_utc"].endswith("+00:00"),
              manifest["zeitpunkt_utc"])
        check("das Manifest nennt das Verfahren, mit dem gerechnet wurde",
              "herkunft.py::datenstand"
              in manifest["verfahren"]["datenstand_hash"])

        # Das Manifest selbst aendert den Hash nicht - der Ordner traegt zu
        # Recht den Namen des Bestandes, den er enthaelt.
        nach_hash, nach_anzahl = snapshot.gesamthash(snap)
        check("das MANIFEST.json aendert den Datenstand-Hash nicht",
              nach_hash == hash_ and nach_anzahl == anzahl)

        # Nachpruefen am unberuehrten Snapshot: die Negativ-Probe. Ohne sie
        # koennte jede Mutationsprobe gruen sein, weil alles rot ist.
        rc, ausgabe = _lauf("--pruefen", snap)
        check("NEGATIV-PROBE: der unberuehrte Snapshot ist UNVERAENDERT (0)",
              rc == 0 and "UNVERAENDERT" in ausgabe, "rc=%d" % rc)

        # Die Quelle ist unberuehrt geblieben
        quelle_hash, _ = snapshot.gesamthash(quelle)
        check("die Quelle ist durch das Ziehen unveraendert",
              quelle_hash == hash_)
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


# ===========================================================================
# Abschnitt 3 - Die Mutationsproben
# ===========================================================================
# Je Probe: (Name, was hergestellt wird, was das echte Modul sagen muss,
# welche Wache entfernt wird, was die Fassung ohne sie sagt).
# ---------------------------------------------------------------------------

def _snapshot_bauen(arbeit, beigabe=None, modul=None, eingaben=None):
    """Quelle + Wurzel + gezogener Snapshot in einem Wegwerf-Verzeichnis.

    ⚠️ **TB-47:** `anker=False`, denn eine Wegwerf-Quelle kann den verankerten
    `datenstand_hash` `d9449faf…` naturgemaess nicht treffen. Der Anker selbst
    wird in Probe 3j eigens geprueft - dort ist er der Gegenstand, nicht das
    Hindernis.

    Der Ordner heisst seit TB-47 nach dem **snapshot_hash**, nicht mehr nach
    dem `datenstand_hash`.
    """
    modul = modul or snapshot
    quelle = _quelle_bauen(os.path.join(arbeit, "quelle"), beigabe=beigabe)
    wurzel, liste = _wurzel_bauen(os.path.join(arbeit, "wurzel"), eingaben)
    ziel = os.path.join(arbeit, "snapshots")
    bericht = modul.ziehen(
        quelle, ziel, wirklich=True, wurzel=wurzel, anker=False,
        eingaben=_liste(liste))
    return quelle, os.path.join(ziel, bericht["snapshot_hash"])


def _liste(pfade):
    """Die Eingabeliste in der Form, die `ziehen` erwartet."""
    return tuple({"pfad": p, "rolle": "Probe", "leser": "Probe"}
                 for p in pfade)


def _flaggen(arbeit, liste=("config/liste.txt",)):
    """Die Befehlszeilenflaggen, die zu `_snapshot_bauen` passen.

    ⚠️ Ohne sie zoege ein CLI-Lauf gegen die **echte** Wurzel und die echte
    Liste `EINGABEN` - er bekaeme also einen anderen `snapshot_hash` als der
    Snapshot, den die Probe eben gebaut hat, und die Probe pruefte an ihrem
    Gegenstand vorbei. Genau daran ist Probe 3c beim ersten Anlauf
    vorbeigelaufen: sie erwartete eine Namenskollision, die es gar nicht gab.
    """
    flaggen = ["--wurzel", os.path.join(arbeit, "wurzel"), "--kein-anker"]
    for p in liste:
        flaggen += ["--eingabe", p]
    return flaggen


def probe_3a_datei_veraendert():
    """Eine Datei im Snapshot wird nach dem Ziehen veraendert.

    ⚠️ Veraendert wird **bei gleicher Laenge** - ein Byte wird ersetzt, keines
    angehaengt. Das ist Absicht: ein Anhaengen wuerde auch der
    Groessenvergleich finden, und die Probe wuerde dann gruen bleiben, ohne
    etwas ueber die Quersumme zu sagen. Der erste Entwurf dieser Probe hatte
    genau diesen Fehler, und er ist hier aufgefallen.
    """
    arbeit = tempfile.mkdtemp(prefix="tb46_3a_")
    try:
        _, snap = _snapshot_bauen(arbeit)
        pfad = os.path.join(snap, "TESTUSDT_1d.csv")
        vorher = os.path.getsize(pfad)
        with open(pfad, "r+b") as f:
            f.seek(vorher - 3)
            f.write(b"7\n" if vorher >= 3 else b"7")
        check("3a die Laenge hat sich dabei NICHT geaendert",
              os.path.getsize(pfad) == vorher,
              "%d Bytes" % os.path.getsize(pfad))

        rc, ausgabe = _lauf("--pruefen", snap)
        check("3a echtes Modul: veraenderte Datei -> VERAENDERT (1)",
              rc == 1 and "veraendert" in ausgabe, "rc=%d" % rc)
        check("3a es nennt die Datei",
              "TESTUSDT_1d.csv" in ausgabe)

        # Ohne den Quersummenvergleich je Datei und ohne den Gesamthash bleibt
        # nur noch die Groesse - und die stimmt.
        ohne = _mutiert("quersummenvergleich", [
            ('        if ist != eintrag.get("sha256"):',
             '        if False:'),
            ('    if ist_hash != manifest["datenstand_hash"]:',
             '    if False:'),
            # ⚠️ TB-47 hat ein ZWEITES Netz gespannt: der `snapshot_hash`
            # faellt bei derselben Lage ebenfalls an. Um die Wache zu
            # isolieren, die diese Probe meint, muss auch er weg - sonst
            # zeigt die Probe nur, dass irgendeine Wache greift.
            ('    if ist_snapshot != manifest["snapshot_hash"]:',
             '    if False:'),
        ])
        b = ohne.pruefen(snap)
        check("3a ohne die Wache: dieselbe Lage gilt als unveraendert",
              b["ausgang"] == ohne.UNVERAENDERT, b["ausgang"])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3b_datei_entfernt():
    arbeit = tempfile.mkdtemp(prefix="tb46_3b_")
    try:
        _, snap = _snapshot_bauen(arbeit)
        os.remove(os.path.join(snap, "ZZZ_1h.csv"))

        rc, ausgabe = _lauf("--pruefen", snap)
        check("3b echtes Modul: entfernte Datei -> VERAENDERT (1)",
              rc == 1 and "entfernt" in ausgabe, "rc=%d" % rc)

        ohne = _mutiert("entfernt", [
            ('        if not os.path.exists(pfad):\n'
             '            abweichungen.append({"datei": name, "art": "entfernt"})\n'
             '            continue',
             '        if not os.path.exists(pfad):\n'
             '            continue'),
            ('    if ist_hash != manifest["datenstand_hash"]:',
             '    if False:'),
            # ⚠️ TB-47 hat ein ZWEITES Netz gespannt: der `snapshot_hash`
            # faellt bei derselben Lage ebenfalls an. Um die Wache zu
            # isolieren, die diese Probe meint, muss auch er weg - sonst
            # zeigt die Probe nur, dass irgendeine Wache greift.
            ('    if ist_snapshot != manifest["snapshot_hash"]:',
             '    if False:'),
            ('    if ist_anzahl != manifest["kursdateien"]:',
             '    if False:'),
        ])
        b = ohne.pruefen(snap)
        check("3b ohne die Wache: die fehlende Datei faellt nicht auf",
              b["ausgang"] == ohne.UNVERAENDERT, b["ausgang"])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3c_ziel_existiert():
    arbeit = tempfile.mkdtemp(prefix="tb46_3c_")
    try:
        quelle, snap = _snapshot_bauen(arbeit)
        # Der Beweis, dass nicht ueberschrieben wurde: eine Spur im Ordner.
        spur = os.path.join(snap, "SPUR.txt")
        with open(spur, "w", encoding="utf-8") as f:
            f.write("der erste Lauf war hier\n")

        ziel = os.path.dirname(snap)
        rc, ausgabe = _lauf("--quelle", quelle, "--ziel", ziel,
                            *(_flaggen(arbeit) + ["--ziehen"]))
        check("3c echtes Modul: bestehendes <hash>/ -> Abbruch (2)",
              rc == 2 and "existiert bereits" in ausgabe, "rc=%d" % rc)
        check("3c die Spur des ersten Laufs ist unberuehrt",
              os.path.exists(spur))

        ohne = _mutiert("zielpruefung", [
            ('    if os.path.exists(ziel):\n'
             '        raise Snapshotfehler(',
             '    if False:\n'
             '        raise Snapshotfehler('),
            ('    os.makedirs(ziel, exist_ok=False)',
             '    os.makedirs(ziel, exist_ok=True)'),
        ])
        gelungen, grund = _zieht(ohne, quelle, ziel,
                                 wurzel=os.path.join(arbeit, "wurzel"),
                                 eingaben=_liste(["config/liste.txt"]))
        check("3c ohne die Wache: der bestehende Snapshot wird ueberschrieben",
              gelungen, grund or "")
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3d_quelle_leer():
    arbeit = tempfile.mkdtemp(prefix="tb46_3d_")
    try:
        leer = os.path.join(arbeit, "leer")
        os.makedirs(leer)
        ziel = os.path.join(arbeit, "snapshots")

        rc, ausgabe = _lauf("--quelle", leer, "--ziel", ziel, "--kein-anker", "--ziehen")
        check("3d echtes Modul: leere Quelle -> Abbruch (2)",
              rc == 2 and "keine einzige" in ausgabe, "rc=%d" % rc)
        check("3d es entsteht kein Snapshot", not os.path.exists(ziel))

        ohne = _mutiert("leerpruefung", [
            ('    if not kursdateien:\n'
             '        raise Snapshotfehler(',
             '    if False:\n'
             '        raise Snapshotfehler('),
            # ⚠️ TB-47 haelt an derselben Stelle ein zweites Mal Wache: der
            # `snapshot_hash` weigert sich, ueber null Dateien gebildet zu
            # werden. Um zu zeigen, dass die ERSTE Wache beisst, muss auch
            # die zweite weg - sonst zeigt die Probe nur, dass irgendeine
            # von beiden greift.
            ('    if not paare:\n'
             '        raise Snapshotfehler(',
             '    if False:\n'
             '        raise Snapshotfehler('),
        ])
        gelungen, grund = _zieht(ohne, leer, os.path.join(arbeit, "s2"))
        check("3d ohne die Wache: ein leerer Snapshot entsteht und sieht "
              "gueltig aus", gelungen, grund or "")
        if gelungen:
            # Und er traegt den Hash der leeren Menge - ein Name, der
            # nichts beschreibt.
            leere = sorted(os.listdir(os.path.join(arbeit, "s2")))
            check("3d ohne die Wache: sein Name ist der Hash der leeren Menge",
                  leere and leere[0].startswith("e3b0c442"), str(leere))
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3e_quersumme_nicht_bildbar():
    """Eine Datei, deren Quersumme sich nicht bilden laesst.

    Hergestellt, ohne auf Zugriffsrechte zu setzen: als **root** greift
    `chmod 000` nicht, und der Test lief in der Cloud als root. Stattdessen
    steht an der Stelle der Datei ein **Verzeichnis** gleichen Namens -
    `os.path.exists` sagt ja, `open(...,'rb')` scheitert.
    """
    arbeit = tempfile.mkdtemp(prefix="tb46_3e_")
    try:
        _, snap = _snapshot_bauen(arbeit)
        pfad = os.path.join(snap, "ZZZ_1h.csv")
        os.remove(pfad)
        os.makedirs(pfad)

        rc, ausgabe = _lauf("--pruefen", snap)
        check("3e echtes Modul: Quersumme nicht bildbar -> NICHT PRUEFBAR (2)",
              rc == 2 and "NICHT PRUEFBAR" in ausgabe, "rc=%d" % rc)
        check("3e und NICHT als `veraendert` verbucht",
              "VERAENDERT" not in ausgabe)
        echt = snapshot.pruefen(snap)
        check("3e das echte Modul behauptet NICHTS ueber diese Datei",
              not [a for a in echt["abweichungen"]
                   if a["datei"] == "ZZZ_1h.csv"],
              str(echt["abweichungen"])[:90])

        # Die Mutation, die TB-45 beschreibt: den Fehler verschlucken und
        # etwas Leeres zurueckgeben. Dann heisst "konnte nicht messen"
        # ploetzlich "veraendert" - eine Aussage, die niemand gemessen hat.
        # ⚠️ Der Gesamthash bricht danach immer noch ab (`herkunft.datenstand`
        # kommt an dieselbe Datei nicht heran), der Ausgang bleibt also
        # `nicht pruefbar`. Verglichen wird deshalb die **Aussage ueber die
        # Datei**, nicht der Ausgang: dort steht beim echten Modul nichts und
        # bei der Fassung ohne Wache ein Urteil.
        ohne = _mutiert("quersummenfehler", [
            ('    except OSError as fehler:\n'
             '        raise Snapshotfehler(\n'
             '            "Quersumme von %s nicht bildbar: %s" % (pfad, fehler))',
             '    except OSError:\n'
             '        return ""'),
        ])
        b = ohne.pruefen(snap)
        erfunden = [a for a in b["abweichungen"]
                    if a["datei"] == "ZZZ_1h.csv" and a["art"] == "veraendert"]
        check("3e ohne die Wache: aus `nicht messbar` wird ein Urteil "
              "`veraendert`", bool(erfunden), str(b["abweichungen"])[:90])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3f_datei_hinzugefuegt():
    """Zwei Faelle - und nur einer davon wird vom Gesamthash gesehen."""
    arbeit = tempfile.mkdtemp(prefix="tb46_3f_")
    try:
        _, snap = _snapshot_bauen(arbeit)

        # Fall 1: eine hinzugefuegte .csv - der Gesamthash sieht sie auch.
        neu_csv = os.path.join(snap, "NEU_1d.csv")
        with open(neu_csv, "w", encoding="utf-8") as f:
            f.write("open_time\n2026-01-09 00:00:00\n")
        rc, ausgabe = _lauf("--pruefen", snap)
        check("3f echtes Modul: hinzugefuegte .csv -> VERAENDERT (1)",
              rc == 1 and "hinzugefuegt" in ausgabe, "rc=%d" % rc)
        os.remove(neu_csv)

        # Fall 2: eine hinzugefuegte Datei, die NICHT .csv heisst.
        # ⚠️ Der Gesamthash zaehlt nur *.csv - er aendert sich nicht. Nur der
        # Vergleich in beide Richtungen findet sie.
        neu_json = os.path.join(snap, "HEIMLICH.json")
        with open(neu_json, "w", encoding="utf-8") as f:
            f.write('{"unbemerkt": true}\n')
        vorher, _ = snapshot.gesamthash(snap)
        with open(os.path.join(snap, "MANIFEST.json"), encoding="utf-8") as f:
            soll = json.load(f)["datenstand_hash"]
        check("3f der Gesamthash sieht eine Nicht-.csv NICHT",
              vorher == soll, "%s..." % vorher[:16])

        rc, ausgabe = _lauf("--pruefen", snap)
        check("3f echtes Modul findet sie trotzdem -> VERAENDERT (1)",
              rc == 1 and "HEIMLICH.json" in ausgabe, "rc=%d" % rc)

        ohne = _mutiert("richtung2", [
            ('    for name in vorhanden:\n'
             '        if name == MANIFEST or name == MANIFEST + ".neu":\n'
             '            continue\n'
             '        if name not in erwartet:\n'
             '            abweichungen.append({"datei": name, "art": "hinzugefuegt"})',
             '    for name in []:\n'
             '        pass'),
            # ⚠️ TB-47: der `snapshot_hash` laeuft ueber ALLE Dateien des
            # Ordners und faellt bei der hinzugefuegten ebenfalls an. Fuer
            # diese Probe muss auch er weg - sie meint den Vergleich in
            # Richtung 2, nicht den Hash.
            ('    if ist_snapshot != manifest["snapshot_hash"]:',
             '    if False:'),
        ])
        b = ohne.pruefen(snap)
        check("3f ohne die Wache: die hinzugefuegte Datei faellt nicht auf",
              b["ausgang"] == ohne.UNVERAENDERT, b["ausgang"])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3g_manifest_fehlt():
    arbeit = tempfile.mkdtemp(prefix="tb46_3g_")
    try:
        _, snap = _snapshot_bauen(arbeit)
        os.remove(os.path.join(snap, "MANIFEST.json"))

        rc, ausgabe = _lauf("--pruefen", snap)
        check("3g echtes Modul: Manifest fehlt -> NICHT PRUEFBAR (2)",
              rc == 2 and "NICHT PRUEFBAR" in ausgabe, "rc=%d" % rc)
        check("3g und nicht als `unveraendert` (0) durchgewinkt", rc != 0)

        # Die Mutation ist der stille Ausfall aus TB-45 in Reinform: kein
        # Manifest, kein Eintrag, keine Abweichung - also "bestanden".
        ohne = _mutiert("manifestpflicht", [
            ('    if not os.path.exists(pfad):\n'
             '        return None, ("%s fehlt - dieser Ordner ist kein Snapshot dieses "\n'
             '                      "Werkzeugs." % pfad)',
             '    if not os.path.exists(pfad):\n'
             '        return {"dateien": {"x": {}}, "datenstand_hash": None,\n'
             '                "snapshot_hash": None, "kursdateien": None}, None'),
            ('        if not os.path.exists(pfad):\n'
             '            abweichungen.append({"datei": name, "art": "entfernt"})\n'
             '            continue',
             '        if not os.path.exists(pfad):\n'
             '            continue'),
            ('    if ist_hash != manifest["datenstand_hash"]:',
             '    if False:'),
            # ⚠️ TB-47 hat ein ZWEITES Netz gespannt: der `snapshot_hash`
            # faellt bei derselben Lage ebenfalls an. Um die Wache zu
            # isolieren, die diese Probe meint, muss auch er weg - sonst
            # zeigt die Probe nur, dass irgendeine Wache greift.
            ('    if ist_snapshot != manifest["snapshot_hash"]:',
             '    if False:'),
            ('    if ist_anzahl != manifest["kursdateien"]:',
             '    if False:'),
            ('    for name in vorhanden:\n'
             '        if name == MANIFEST or name == MANIFEST + ".neu":\n'
             '            continue\n'
             '        if name not in erwartet:\n'
             '            abweichungen.append({"datei": name, "art": "hinzugefuegt"})',
             '    for name in []:\n'
             '        pass'),
        ])
        b = ohne.pruefen(snap)
        check("3g ohne die Wache: ein Ordner ohne Manifest gilt als geprueft "
              "und unveraendert", b["ausgang"] == ohne.UNVERAENDERT,
              b["ausgang"])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3h_manifest_beschaedigt():
    arbeit = tempfile.mkdtemp(prefix="tb46_3h_")
    try:
        _, snap = _snapshot_bauen(arbeit)
        pfad = os.path.join(snap, "MANIFEST.json")

        # (1) kein gueltiges JSON
        with open(pfad, "w", encoding="utf-8") as f:
            f.write("{das ist kein json")
        rc, ausgabe = _lauf("--pruefen", snap)
        check("3h echtes Modul: Manifest kein JSON -> NICHT PRUEFBAR (2)",
              rc == 2 and "beschaedigt" in ausgabe, "rc=%d" % rc)

        # (2) gueltiges JSON, aber der Eintrag `dateien` fehlt
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump({"datenstand_hash": "x", "snapshot_hash": "y",
                       "kursdateien": 2}, f)
        rc, ausgabe = _lauf("--pruefen", snap)
        check("3h echtes Modul: Manifest ohne `dateien` -> NICHT PRUEFBAR (2)",
              rc == 2, "rc=%d" % rc)

        # (3) gueltiges JSON, `dateien` leer - der Fall, der am harmlosesten
        # aussieht und am gefaehrlichsten ist: nichts zu pruefen heisst nicht
        # geprueft.
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump({"datenstand_hash": "x", "snapshot_hash": "y",
                       "kursdateien": 2, "dateien": {}}, f)
        rc, ausgabe = _lauf("--pruefen", snap)
        check("3h echtes Modul: Manifest mit leerem `dateien` -> "
              "NICHT PRUEFBAR (2)", rc == 2, "rc=%d" % rc)

        ohne = _mutiert("manifestpruefung", [
            ('    if not isinstance(manifest["dateien"], dict) or not manifest["dateien"]:',
             '    if False:'),
            ('    if ist_hash != manifest["datenstand_hash"]:',
             '    if False:'),
            # ⚠️ TB-47 hat ein ZWEITES Netz gespannt: der `snapshot_hash`
            # faellt bei derselben Lage ebenfalls an. Um die Wache zu
            # isolieren, die diese Probe meint, muss auch er weg - sonst
            # zeigt die Probe nur, dass irgendeine Wache greift.
            ('    if ist_snapshot != manifest["snapshot_hash"]:',
             '    if False:'),
            ('    if ist_anzahl != manifest["kursdateien"]:',
             '    if False:'),
            ('    for name in vorhanden:\n'
             '        if name == MANIFEST or name == MANIFEST + ".neu":\n'
             '            continue\n'
             '        if name not in erwartet:\n'
             '            abweichungen.append({"datei": name, "art": "hinzugefuegt"})',
             '    for name in []:\n'
             '        pass'),
        ])
        b = ohne.pruefen(snap)
        check("3h ohne die Wache: ein leeres `dateien` gilt als geprueft",
              b["ausgang"] == ohne.UNVERAENDERT, b["ausgang"])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3i_kopie_weicht_ab():
    """Die Gegenpruefung beim Ziehen: eine Kopie, die nicht der Quelle gleicht.

    Hergestellt durch ein `copy2`, das absichtlich etwas anderes schreibt -
    so, wie ein Dateisystem- oder Uebertragungsfehler sich auswirken wuerde.
    """
    arbeit = tempfile.mkdtemp(prefix="tb46_3i_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"))
        ziel = os.path.join(arbeit, "snapshots")

        falsches_copy2 = (
            'def _falsches_copy2(a, b):\n'
            '    with open(a, "rb") as q, open(b, "wb") as z:\n'
            '        z.write(q.read() + b"# ein Byte zu viel\\n")\n'
            'shutil = type(shutil)("shutil_attrappe", "")\n'
        )

        # Das echte Modul, mit nur einer eingesetzten Stoerung: copy2
        # schreibt etwas anderes. Alles andere bleibt, wie es ist.
        echt = _mutiert("stoerung_copy2", [
            ('                shutil.copy2(q_pfad, z_pfad)      # copy2: Zeitstempel bleiben',
             '                with open(q_pfad, "rb") as _q, open(z_pfad, "wb") as _z:\n'
             '                    _z.write(_q.read() + b"# ein Byte zu viel\\n")'),
        ])
        gelungen, grund = _zieht(echt, quelle, ziel)
        check("3i echtes Modul: abweichende Kopie -> Abbruch",
              not gelungen and "ABWEICHUNG" in (grund or ""),
              (grund or "")[:80])
        check("3i der halb gezogene Snapshot wird wieder entfernt",
              not os.path.exists(ziel) or not os.listdir(ziel),
              str(os.listdir(ziel)) if os.path.exists(ziel) else "-")

        # Dieselbe Stoerung, aber ohne die Gegenpruefung: der Snapshot
        # entsteht, traegt den Hash der Quelle - und enthaelt andere Bytes.
        ohne = _mutiert("gegenpruefung", [
            ('                shutil.copy2(q_pfad, z_pfad)      # copy2: Zeitstempel bleiben',
             '                with open(q_pfad, "rb") as _q, open(z_pfad, "wb") as _z:\n'
             '                    _z.write(_q.read() + b"# ein Byte zu viel\\n")'),
            ('            if summe_quelle != summe_kopie:', '            if False:'),
            ('            if not _byteweise_gleich(q_pfad, z_pfad):',
             '            if False:'),
            ('        if kopie_hash != hash_ or kopie_anzahl != anzahl:',
             '        if False:'),
            # ⚠️ TB-47 stellt die Kopie ein zweites Mal gegen ihren Namen,
            # diesmal ueber ALLE Dateien statt nur ueber die `*.csv`. Fuer
            # diese Probe muss auch diese Gegenpruefung weg.
            ('        if snapshot_hash(kopie_paare) != name_:',
             '        if False:'),
        ])
        ziel2 = os.path.join(arbeit, "snapshots2")
        gelungen, grund = _zieht(ohne, quelle, ziel2)
        check("3i ohne die Gegenpruefung: der falsche Snapshot entsteht",
              gelungen, grund or "")
        if gelungen:
            name = os.listdir(ziel2)[0]
            drin, _ = snapshot.gesamthash(os.path.join(ziel2, name))
            check("3i ohne die Gegenpruefung: er traegt einen Namen, den sein "
                  "Inhalt nicht erfuellt", drin != name,
                  "Name %s..., Inhalt %s..." % (name[:16], drin[:16]))
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3j_quelle_mit_unterordner():
    """Ein Unterordner in der Quelle - der Fall, den Entwurf A herstellt."""
    arbeit = tempfile.mkdtemp(prefix="tb46_3j_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"))
        os.makedirs(os.path.join(quelle, "snapshots", "aelter"))
        with open(os.path.join(quelle, "snapshots", "aelter", "A_1d.csv"),
                  "w", encoding="utf-8") as f:
            f.write("open_time\n2025-01-01 00:00:00\n")

        rc, ausgabe = _lauf("--quelle", quelle, "--ziel",
                            os.path.join(arbeit, "s"), "--kein-anker",
                            "--ziehen")
        check("3j echtes Modul: Unterordner in der Quelle -> Abbruch (2)",
              rc == 2 and "NICHT rekursiv" in ausgabe, "rc=%d" % rc)

        # Und der Beweis der Aussage, auf der die Wache ruht: der
        # Datenstand-Hash aendert sich durch den Unterordner NICHT.
        mit, anzahl_mit = snapshot.gesamthash(quelle)
        rein = _quelle_bauen(os.path.join(arbeit, "rein"))
        ohne_unter, anzahl_ohne = snapshot.gesamthash(rein)
        check("3j ein Unterordner aendert den registrierten Hash nicht - "
              "die Berechnung ist nicht rekursiv",
              mit == ohne_unter and anzahl_mit == anzahl_ohne,
              "%s... == %s..." % (mit[:16], ohne_unter[:16]))

        ohne = _mutiert("unterordnerpruefung", [
            ('    if unterordner:\n'
             '        raise Snapshotfehler(',
             '    if False:\n'
             '        raise Snapshotfehler('),
        ])
        gelungen, grund = _zieht(ohne, quelle, os.path.join(arbeit, "s2"))
        check("3j ohne die Wache: der Snapshot entsteht ohne den Unterordner",
              gelungen, grund or "")
        if gelungen:
            name = os.listdir(os.path.join(arbeit, "s2"))[0]
            inhalt = sorted(os.listdir(os.path.join(arbeit, "s2", name)))
            check("3j ohne die Wache: `snapshots/` fehlt in der Kopie - "
                  "stillschweigend", "snapshots" not in inhalt, str(inhalt))
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3k_ziel_in_der_quelle():
    arbeit = tempfile.mkdtemp(prefix="tb46_3k_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"))
        rc, ausgabe = _lauf("--quelle", quelle, "--ziel",
                            os.path.join(quelle, "snapshots"), "--kein-anker",
                            "--ziehen")
        check("3k echtes Modul: Ziel innerhalb der Quelle -> Abbruch (2)",
              rc == 2 and "innerhalb der Quelle" in ausgabe, "rc=%d" % rc)
        check("3k in der Quelle ist nichts entstanden",
              not os.path.exists(os.path.join(quelle, "snapshots")))

        ohne = _mutiert("ortspruefung", [
            ('    if z == q or z.startswith(q + os.sep):\n'
             '        raise Snapshotfehler(',
             '    if False:\n'
             '        raise Snapshotfehler('),
        ])
        gelungen, grund = _zieht(ohne, quelle,
                                 os.path.join(quelle, "snapshots"))
        check("3k ohne die Wache: der Lauf kopiert in die eigene Quelle",
              gelungen, grund or "")
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3m_quelle_hat_schon_ein_manifest():
    """Eine Quelldatei, die schon `MANIFEST.json` heisst.

    Der unauffaelligste Fall von allen: das Manifest des Snapshots
    ueberschreibt sie, und weil das Manifest sich selbst nicht auffuehrt,
    findet `--pruefen` die verlorene Datei **nie**.
    """
    arbeit = tempfile.mkdtemp(prefix="tb46_3m_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"),
                              beigabe={"MANIFEST.json": '{"fremd": true}\n'})
        ziel = os.path.join(arbeit, "snapshots")

        rc, ausgabe = _lauf("--quelle", quelle, "--ziel", ziel, "--kein-anker", "--ziehen")
        check("3m echtes Modul: Quelle hat schon ein MANIFEST.json -> "
              "Abbruch (2)", rc == 2 and "ueberschreiben" in ausgabe,
              "rc=%d" % rc)
        check("3m es entsteht kein Snapshot", not os.path.exists(ziel))

        ohne = _mutiert("manifestkollision", [
            ('    if MANIFEST in dateien:\n'
             '        raise Snapshotfehler(',
             '    if False:\n'
             '        raise Snapshotfehler('),
            # ⚠️ TB-47: `eingabeliste` bricht bei JEDER Datei ab, die weder
            # Kursdatei noch Listeneintrag ist - also auch bei dieser. Das
            # ist eine zweite, unabhaengige Wache an derselben Stelle; fuer
            # diese Probe muss sie ebenfalls weg, sonst zeigt die Probe nur,
            # dass eine von beiden greift.
            ('        if not name.endswith(".csv"):', '        if False:'),
        ])
        gelungen, grund = _zieht(ohne, quelle, ziel)
        check("3m ohne die Wache: der Snapshot entsteht", gelungen, grund or "")
        if gelungen:
            name = os.listdir(ziel)[0]
            with open(os.path.join(ziel, name, "MANIFEST.json"),
                      encoding="utf-8") as f:
                inhalt = json.load(f)
            check("3m ohne die Wache: die Quelldatei ist weg, ueberschrieben "
                  "vom eigenen Manifest", "fremd" not in inhalt)
            # ⚠️ Und jetzt die Stelle, an der diese Probe im ersten Entwurf
            # falsch lag: es wurde behauptet, das bleibe unentdeckt. Gemessen
            # bleibt es das NICHT - das Manifest fuehrt die Quelldatei
            # `MANIFEST.json` mit ihrer alten Quersumme, und die stimmt nach
            # dem Ueberschreiben nicht mehr. `--pruefen` meldet also
            # `veraendert`, **aber es zeigt auf das Manifest**, nicht auf die
            # verlorene Datei. Der Wert der Wache liegt darin, den Grund
            # vorher zu nennen, nicht darin, der einzige Finder zu sein.
            b = ohne.pruefen(os.path.join(ziel, name))
            zeigt_auf_manifest = [a for a in b["abweichungen"]
                                  if a["datei"] == "MANIFEST.json"]
            check("3m ohne die Wache: --pruefen findet nur das Manifest "
                  "selbst, nicht die verlorene Datei",
                  b["ausgang"] == ohne.VERAENDERT and bool(zeigt_auf_manifest)
                  and not [a for a in b["abweichungen"]
                           if a["art"] == "entfernt"],
                  str(b["abweichungen"])[:100])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3l_kein_verzeichnis():
    """`--pruefen` auf etwas, das kein Snapshot ist."""
    arbeit = tempfile.mkdtemp(prefix="tb46_3l_")
    try:
        datei = os.path.join(arbeit, "keine_kopie.txt")
        with open(datei, "w", encoding="utf-8") as f:
            f.write("nichts\n")
        rc, ausgabe = _lauf("--pruefen", datei)
        check("3l echtes Modul: `--pruefen` auf eine Datei -> "
              "NICHT PRUEFBAR (2)", rc == 2 and "NICHT PRUEFBAR" in ausgabe,
              "rc=%d" % rc)
        rc, ausgabe = _lauf("--pruefen", os.path.join(arbeit, "gibt_es_nicht"))
        check("3l echtes Modul: `--pruefen` auf einen fehlenden Ordner -> "
              "NICHT PRUEFBAR (2)", rc == 2, "rc=%d" % rc)
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def abschnitt_3():
    print("\n3. MUTATIONSPROBEN - jede zeigt, dass sie beisst")
    for probe in (probe_3a_datei_veraendert, probe_3b_datei_entfernt,
                  probe_3c_ziel_existiert, probe_3d_quelle_leer,
                  probe_3e_quersumme_nicht_bildbar,
                  probe_3f_datei_hinzugefuegt, probe_3g_manifest_fehlt,
                  probe_3h_manifest_beschaedigt, probe_3i_kopie_weicht_ab,
                  probe_3j_quelle_mit_unterordner,
                  probe_3k_ziel_in_der_quelle, probe_3l_kein_verzeichnis,
                  probe_3m_quelle_hat_schon_ein_manifest):
        try:
            probe()
        except AssertionError as fehler:
            # Ein nicht gefundener Ankertext: die Wache ist umgezogen. Das ist
            # rot, nicht uebersprungen.
            FEHLER.append(probe.__name__ + " (Anker)")
            print("  [FEHLER] %s: %s" % (probe.__name__, fehler))
        except Exception as fehler:                          # noqa: BLE001
            import traceback
            FEHLER.append(probe.__name__ + " (Ausnahme)")
            print("  [FEHLER] %s warf eine Ausnahme: %s"
                  % (probe.__name__, fehler))
            traceback.print_exc()


# ===========================================================================
# Abschnitt 3b - Die Proben zu TB-47: die Grenze und die zwei Hashes
# ===========================================================================
# ⚠️ Dieselbe Bauform wie Abschnitt 3: erst das echte Modul, dann dieselbe
# Lage ohne die Wache. Neu ist die Frage, die sie stellen - nicht die Form.
# ---------------------------------------------------------------------------

def probe_3n_nichtkursdatei_veraendert():
    """⭐ Der Fall, fuer den es ZWEI Hashes gibt.

    Eine Nicht-Kursdatei im Snapshot wird veraendert. Der `datenstand_hash`
    zaehlt nur `*.csv` auf der obersten Ebene - er **bleibt gleich**, und das
    ist richtig so: die Kursdaten sind ja dieselben. Der `snapshot_hash`
    laeuft ueber alle Dateien und **aendert sich**.

    ⚠️ Waere dieser Fall nicht unterscheidbar, haette eine veraenderte
    Symbolliste denselben Snapshotnamen wie die urspruengliche - ein anderer
    Eingabesatz unter demselben Namen. Genau das verhindert der zweite Hash.
    """
    arbeit = tempfile.mkdtemp(prefix="tb47_3n_")
    try:
        _, snap = _snapshot_bauen(arbeit)
        pfad = os.path.join(snap, "config", "liste.txt")
        vorher_daten, _ = snapshot.gesamthash(snap)
        with open(pfad, "w", encoding="utf-8") as f:
            f.write("CCC\nDDD\n")
        nachher_daten, _ = snapshot.gesamthash(snap)

        check("3n der datenstand_hash bleibt gleich - er zaehlt nur *.csv",
              vorher_daten == nachher_daten, "%s..." % nachher_daten[:16])

        b = snapshot.pruefen(snap)
        check("3n echtes Modul: VERAENDERT", b["ausgang"] == snapshot.VERAENDERT,
              b["ausgang"])
        check("3n und es nennt den snapshot_hash als das, was abweicht",
              any(a["datei"] == "(snapshot_hash)" for a in b["abweichungen"]),
              str([a["datei"] for a in b["abweichungen"]]))

        rc, ausgabe = _lauf("--pruefen", snap)
        check("3n ueber die Befehlszeile: Rueckgabewert 1", rc == 1,
              "rc=%d" % rc)

        # Ohne den Quersummenvergleich je Datei UND ohne den snapshot_hash
        # bleibt nur der datenstand_hash - und der schweigt hier.
        ohne = _mutiert("zweiter_hash", [
            ('        if ist != eintrag.get("sha256"):',
             '        if False:'),
            ('    if ist_snapshot != manifest["snapshot_hash"]:',
             '    if False:'),
        ])
        b2 = ohne.pruefen(snap)
        check("3n ohne den zweiten Hash: dieselbe Lage gilt als unveraendert",
              b2["ausgang"] == ohne.UNVERAENDERT, b2["ausgang"])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3o_kursdatei_veraendert_beide():
    """Eine Kursdatei veraendert: **beide** Hashes muessen sich aendern."""
    arbeit = tempfile.mkdtemp(prefix="tb47_3o_")
    try:
        _, snap = _snapshot_bauen(arbeit)
        with open(os.path.join(snap, "MANIFEST.json"), encoding="utf-8") as f:
            manifest = json.load(f)

        pfad = os.path.join(snap, "TESTUSDT_1d.csv")
        with open(pfad, "a", encoding="utf-8") as f:
            f.write("2026-01-03,9,9,9,9,99\n")

        ist_daten, _ = snapshot.gesamthash(snap)
        check("3o der datenstand_hash aendert sich",
              ist_daten != manifest["datenstand_hash"],
              "%s... statt %s..." % (ist_daten[:16],
                                     manifest["datenstand_hash"][:16]))

        b = snapshot.pruefen(snap)
        namen = [a["datei"] for a in b["abweichungen"]]
        check("3o der snapshot_hash aendert sich ebenfalls",
              "(snapshot_hash)" in namen, str(namen))
        check("3o beide werden als Abweichung genannt",
              "(datenstand_hash)" in namen and "(snapshot_hash)" in namen,
              str(namen))
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3p_manifestfeld_ergaenzt():
    """⭐ Der Beweis, dass der snapshot_hash ueber die DATEIEN laeuft.

    Ein zusaetzliches Feld im Manifest darf den Namen des Snapshots **nicht**
    aendern. Liefe der Hash ueber das Manifest, bekaeme derselbe Eingabesatz
    nach jeder Erweiterung des Manifests einen neuen Namen - und zwei
    Snapshots mit gleichem Inhalt hiessen verschieden.
    """
    arbeit = tempfile.mkdtemp(prefix="tb47_3p_")
    try:
        _, snap = _snapshot_bauen(arbeit)
        pfad = os.path.join(snap, "MANIFEST.json")
        with open(pfad, encoding="utf-8") as f:
            manifest = json.load(f)
        vorher = manifest["snapshot_hash"]

        manifest["ein_neues_feld"] = "TB-48 haette das gern mitgefuehrt"
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False,
                      sort_keys=True)

        b = snapshot.pruefen(snap)
        check("3p der snapshot_hash bleibt derselbe",
              b["snapshot_ist"] == vorher, "%s..." % str(b["snapshot_ist"])[:16])
        check("3p der Snapshot gilt weiterhin als UNVERAENDERT",
              b["ausgang"] == snapshot.UNVERAENDERT, b["ausgang"])

        rc, _ = _lauf("--pruefen", snap)
        check("3p ueber die Befehlszeile: Rueckgabewert 0", rc == 0,
              "rc=%d" % rc)

        # Die Gegenprobe zur Aussage: liefe er ueber das Manifest, waere die
        # Lage jetzt VERAENDERT. Das wird hergestellt, nicht behauptet.
        ohne = _mutiert("hash_ueber_manifest", [
            ('        ist_snapshot = snapshot_hash(paare) if paare else None',
             '        ist_snapshot = hashlib.sha256(\n'
             '            open(os.path.join(ordner, MANIFEST), "rb").read()\n'
             '        ).hexdigest()'),
        ])
        b2 = ohne.pruefen(snap)
        check("3p ueber das Manifest gerechnet waere dieselbe Lage "
              "VERAENDERT - deshalb laeuft er ueber die Dateien",
              b2["ausgang"] == ohne.VERAENDERT, b2["ausgang"])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3q_eingabedatei_fehlt():
    """Eine Datei aus der Eingabeliste fehlt in der Quelle: Abbruch."""
    arbeit = tempfile.mkdtemp(prefix="tb47_3q_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"))
        wurzel = os.path.join(arbeit, "wurzel")
        os.makedirs(os.path.join(wurzel, "config"), exist_ok=True)
        ziel = os.path.join(arbeit, "snapshots")

        rc, ausgabe = _lauf("--quelle", quelle, "--ziel", ziel,
                            "--wurzel", wurzel, "--kein-anker",
                            "--eingabe", "config/fehlt_wirklich.txt",
                            "--ziehen")
        check("3q echtes Modul: fehlende Eingabedatei -> Abbruch (2)",
              rc == 2, "rc=%d" % rc)
        check("3q die fehlende Datei wird NAMENTLICH genannt",
              "config/fehlt_wirklich.txt" in ausgabe, ausgabe.strip()[:120])
        check("3q es entsteht kein Snapshot", not os.path.exists(ziel))

        ohne = _mutiert("eingabepflicht", [
            ('    if fehlend:\n'
             '        raise Snapshotfehler(',
             '    if False:\n'
             '        raise Snapshotfehler('),
        ])
        gelungen, grund = _zieht(
            ohne, quelle, ziel, wurzel=wurzel,
            eingaben=_liste(["config/fehlt_wirklich.txt"]))
        check("3q ohne die Wache: der Snapshot entsteht ohne die Eingabe",
              gelungen, grund or "")
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3r_quelle_hat_datei_ausserhalb_der_liste():
    """Eine Datei in der Quelle, die nicht in der Liste steht: ABBRUCH.

    ⭐ **Die Entscheidung, die der Auftrag verlangt - und ihre Begruendung.**
    Moeglich waere auch eine blosse Meldung gewesen. Dagegen spricht: der
    Name des Ordners ist der Hash ueber genau die Dateien der Liste. Eine
    Datei daneben hat nur zwei Ausgaenge, und beide sind still - sie wird
    nicht mitkopiert (dann ist der Snapshot unvollstaendig und sieht
    vollstaendig aus), oder sie wird mitkopiert (dann luegt die Liste). Das
    Modul bricht an allen vergleichbaren Stellen ab; eine Meldung waere hier
    die einzige Ausnahme.
    """
    arbeit = tempfile.mkdtemp(prefix="tb47_3r_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"),
                               beigabe={"FREMD.json": '{"x": 1}\n'})
        ziel = os.path.join(arbeit, "snapshots")

        rc, ausgabe = _lauf("--quelle", quelle, "--ziel", ziel,
                            "--kein-anker", "--ziehen")
        check("3r echtes Modul: Datei ausserhalb der Liste -> Abbruch (2)",
              rc == 2, "rc=%d" % rc)
        check("3r die Datei wird namentlich genannt", "FREMD.json" in ausgabe,
              ausgabe.strip()[:120])
        check("3r es entsteht kein Snapshot", not os.path.exists(ziel))

        ohne = _mutiert("listenpflicht", [
            ('        if not name.endswith(".csv"):', '        if False:'),
        ])
        gelungen, grund = _zieht(ohne, quelle, ziel)
        check("3r ohne die Wache: die fremde Datei wandert stillschweigend "
              "in den Snapshot", gelungen, grund or "")
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3s_teilkerzen_schlagen_an():
    """Die Teilkerzen-Pruefung findet etwas: kein Snapshot."""
    arbeit = tempfile.mkdtemp(prefix="tb47_3s_")
    try:
        quelle = os.path.join(arbeit, "quelle")
        os.makedirs(quelle)
        # Eine Tagesdatei, deren letzte Kerze noch LAEUFT - der Fall, den die
        # Wache `S - Stand` meint: ein Abruf hat mitten in der Kerze
        # geschrieben.
        morgen = __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc).date()
        with open(os.path.join(quelle, "LAUFEND_1d.csv"), "w",
                  encoding="utf-8") as f:
            f.write("open_time,open,high,low,close,volume\n")
            f.write("%s,1,2,0,1,10\n" % morgen.isoformat())
        ziel = os.path.join(arbeit, "snapshots")

        rc, ausgabe = _lauf("--quelle", quelle, "--ziel", ziel,
                            "--kein-anker", "--ziehen")
        check("3s echtes Modul: Teilkerze -> Abbruch (2)", rc == 2,
              "rc=%d" % rc)
        check("3s die Begruendung nennt die Teilkerzen-Pruefung",
              "Teilkerzen" in ausgabe, ausgabe.strip()[:120])
        check("3s es entsteht KEIN Snapshot", not os.path.exists(ziel))

        ohne = _mutiert("teilkerzenpflicht", [
            ('    if kerzen["nicht_zugelassen"]:\n'
             '        offen =',
             '    if False:\n'
             '        offen ='),
        ])
        gelungen, grund = _zieht(ohne, quelle, ziel)
        check("3s ohne die Wache: der Snapshot entsteht trotz Teilkerze",
              gelungen, grund or "")
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3t_teilkerzenpruefung_nicht_ausfuehrbar():
    """⚠️ Nicht ausfuehrbar ist **2**, nie 0.

    Die Lehre aus TB-45 auf die neue Pruefung angewandt: ein gescheiterter
    Aufruf darf nicht aussehen wie "kein Befund".
    """
    arbeit = tempfile.mkdtemp(prefix="tb47_3t_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"))
        ziel = os.path.join(arbeit, "snapshots")

        # Die Pruefung ist nicht auffindbar: ein Pfad, der ins Leere zeigt.
        ohne_datei = _mutiert("zeitabdeckung_fehlt", [
            ('ZEITABDECKUNG_PFAD = os.path.join(_SHARED_DIR, '
             '"zeitabdeckung.py")',
             'ZEITABDECKUNG_PFAD = os.path.join(_SHARED_DIR, '
             '"gibt_es_nicht_tb47.py")'),
        ])
        gelungen, grund = _zieht(ohne_datei, quelle, ziel)
        check("3t fehlende Pruefung: es wird NICHT gezogen", not gelungen)
        check("3t und die Begruendung sagt, dass sie fehlt",
              "nicht auffindbar" in (grund or ""), (grund or "")[:100])
        check("3t es entsteht kein Snapshot", not os.path.exists(ziel))

        # Und der Rueckgabewert der Befehlszeile ist die 2.
        rc = ohne_datei.main(["--quelle", quelle, "--ziel", ziel,
                              "--kein-anker", "--ziehen"])
        check("3t der Rueckgabewert ist NICHT_PRUEFBAR (2), nie 0",
              rc == ohne_datei.NICHT_PRUEFBAR, "rc=%s" % rc)

        # Die Pruefung ist da, wirft aber: auch das ist 2, nicht 0.
        wirft = _mutiert("zeitabdeckung_wirft", [
            ('        rohbefunde = modul.pruefe_ordner(quelle, stand=stand)',
             '        raise RuntimeError("die Pruefung faellt hier aus")'),
        ])
        gelungen2, grund2 = _zieht(wirft, quelle, ziel)
        check("3t eine werfende Pruefung zieht ebenfalls nicht", not gelungen2)
        check("3t und sie sagt NICHT PRUEFBAR, nicht 'in Ordnung'",
              "NICHT PRUEFBAR" in (grund2 or ""), (grund2 or "")[:100])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3u_datenstand_weicht_vom_anker_ab():
    """Der verankerte Datenstand `d9449faf…` wird erzwungen.

    ⚠️ Hier ist der Anker der **Gegenstand** der Probe, nicht die
    Rahmenbedingung - deshalb laeuft sie ohne `--kein-anker`.
    """
    arbeit = tempfile.mkdtemp(prefix="tb47_3u_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"))
        wurzel, liste = _wurzel_bauen(os.path.join(arbeit, "wurzel"))
        ziel = os.path.join(arbeit, "snapshots")

        rc, ausgabe = _lauf("--quelle", quelle, "--ziel", ziel,
                            "--wurzel", wurzel, "--eingabe", liste[0],
                            "--ziehen")
        check("3u echtes Modul: abweichender Datenstand -> Abbruch (2)",
              rc == 2, "rc=%d" % rc)
        check("3u die Meldung nennt den verankerten Wert",
              snapshot.VERANKERTER_DATENSTAND[:16] in ausgabe,
              ausgabe.strip()[:140])
        check("3u es entsteht kein Snapshot", not os.path.exists(ziel))

        # Ohne die Wache entsteht er - und traegt einen Namen, der einen
        # anderen Bestand beschreibt als den verankerten.
        ohne = _mutiert("ankerpflicht", [
            ('    if anker and (hash_ != VERANKERTER_DATENSTAND',
             '    if False and (hash_ != VERANKERTER_DATENSTAND'),
        ])
        gelungen, grund = _zieht(ohne, quelle, ziel, wurzel=wurzel,
                                 eingaben=_liste(liste))
        check("3u ohne die Wache: der Snapshot entsteht auf fremdem Bestand",
              gelungen, grund or "")
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3v_manifest_fuehrt_liste_und_teilkerzen():
    """Das Manifest fuehrt beide Hashes, die Liste und die Teilkerzen mit."""
    arbeit = tempfile.mkdtemp(prefix="tb47_3v_")
    try:
        _, snap = _snapshot_bauen(arbeit)
        with open(os.path.join(snap, "MANIFEST.json"), encoding="utf-8") as f:
            m = json.load(f)

        check("3v das Manifest fuehrt BEIDE Hashes unter eigenen Namen",
              isinstance(m.get("snapshot_hash"), str)
              and isinstance(m.get("datenstand_hash"), str)
              and m["snapshot_hash"] != m["datenstand_hash"],
              "%s... / %s..." % (str(m.get("snapshot_hash"))[:12],
                                 str(m.get("datenstand_hash"))[:12]))
        check("3v der Ordner heisst wie der snapshot_hash",
              os.path.basename(snap) == m["snapshot_hash"])
        check("3v das Manifest fuehrt die Eingabeliste mit",
              isinstance(m.get("eingabeliste"), list)
              and any(e.get("art") == "Eingabe" for e in m["eingabeliste"]),
              str(len(m.get("eingabeliste") or [])) + " Eintraege")
        check("3v jeder Eintrag der Liste nennt Pfad, Herkunft und Rolle",
              all({"im_snapshot", "herkunft", "art", "rolle"} <= set(e)
                  for e in m["eingabeliste"]))
        check("3v das Manifest haelt das Ergebnis der Teilkerzen-Pruefung fest",
              isinstance(m.get("teilkerzen"), dict)
              and m["teilkerzen"].get("frei_von_teilkerzen") is True
              and m["teilkerzen"].get("dateien_geprueft") == 2,
              str(m.get("teilkerzen", {}).get("dateien_geprueft")))
        check("3v es nennt beide Rechenwege getrennt",
              set(m.get("verfahren", {})) == {"snapshot_hash",
                                              "datenstand_hash"},
              str(list(m.get("verfahren", {}))))
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def abschnitt_3b():
    print("\n3b. TB-47 - DIE GRENZE UND DIE ZWEI HASHES")
    for probe in (probe_3n_nichtkursdatei_veraendert,
                  probe_3o_kursdatei_veraendert_beide,
                  probe_3p_manifestfeld_ergaenzt,
                  probe_3q_eingabedatei_fehlt,
                  probe_3r_quelle_hat_datei_ausserhalb_der_liste,
                  probe_3s_teilkerzen_schlagen_an,
                  probe_3t_teilkerzenpruefung_nicht_ausfuehrbar,
                  probe_3u_datenstand_weicht_vom_anker_ab,
                  probe_3v_manifest_fuehrt_liste_und_teilkerzen):
        try:
            probe()
        except AssertionError as fehler:
            FEHLER.append(probe.__name__ + " (Anker)")
            print("  [FEHLER] %s: %s" % (probe.__name__, fehler))
        except Exception as fehler:                          # noqa: BLE001
            import traceback
            FEHLER.append(probe.__name__ + " (Ausnahme)")
            print("  [FEHLER] %s warf eine Ausnahme: %s"
                  % (probe.__name__, fehler))
            traceback.print_exc()


# ===========================================================================
# Abschnitt 3c - TB-49: DIE AUSNAHME `rand_erste`
# ===========================================================================
#
# Registertext 5a, Zusatz (Vorregistrierung, Abschnitt 17.3) laesst eine
# Befundart zu - und nur unter drei Bedingungen. Dieser Abschnitt zeigt an
# einem Wegwerf-Bestand, dass genau diese drei gelten und keine vierte.
#
# ⚠️ **Die Bauform bleibt dieselbe wie in Abschnitt 3**: zu jeder Probe
# gehoert die Fassung mit **entfernter Bedingung**, und die muss die
# Abweichung UEBERSEHEN. Sonst prueft die Probe eine andere Stelle als
# angenommen.

# Wie viele Befunde `data/` traegt - dieselbe Zahl, gegen die der
# Registereintrag geschrieben ist. Die Probe baut sie nach, statt sie zu
# behaupten.
BEFUNDE_IM_BESTAND = 36


def _teilkerzen_quelle(ordner, symbole, erste_stunden=range(12, 24),
                       letzte_stunden=range(0, 24), erste_verfaelschen=False):
    """Ein Wegwerf-`data/`, das die Teilkerzen-Pruefung anschlagen laesst.

    Je Symbol zwei Dateien - eine `_1h.csv` als **Zeuge** und eine `_1d.csv`,
    deren Tageskerzen genau die Aggregate der jeweiligen Stunden sind:

        Tag 1  nur `erste_stunden` belegt  -> die erste Tageskerze deckt
                                              ihren Zeitraum nicht voll ab,
                                              ist aber das Aggregat genau
                                              dieser Stunden  -> `rand_erste`
                                              mit Urteil `abgeleitete_teilkerze`
        Tag 2  `letzte_stunden` belegt     -> voll und passend -> kein Befund

    Mit `letzte_stunden=range(0, 12)` wird daraus zusaetzlich ein
    **`rand_letzte`**; mit `erste_verfaelschen=True` stimmt die erste
    Tageskerze nicht mehr mit dem Aggregat ueberein und das Urteil wird
    `unbelegt`.

    ⚠️ Die Werte sind so gewaehlt, dass Summe und Extremwerte **exakt** in
    Gleitkomma aufgehen. Eine Probe, die an einem Rundungsrest scheitert,
    sagt nichts ueber die Wache aus.
    """
    os.makedirs(ordner, exist_ok=True)

    def kerzen(stunden, basis):
        return [{"h": h, "open": basis + h, "high": basis + h + 0.5,
                 "low": basis + h - 0.5, "close": basis + h + 0.25,
                 "volume": 10.0} for h in stunden]

    def aggregat(ks):
        return {"open": ks[0]["open"], "high": max(k["high"] for k in ks),
                "low": min(k["low"] for k in ks), "close": ks[-1]["close"],
                "volume": sum(k["volume"] for k in ks)}

    def zeile(stempel, w):
        return "%s,%r,%r,%r,%r,%r\n" % (stempel, w["open"], w["high"],
                                        w["low"], w["close"], w["volume"])

    for i, symbol in enumerate(symbole):
        tag1 = kerzen(list(erste_stunden), 100.0 + 10 * i)
        tag2 = kerzen(list(letzte_stunden), 200.0 + 10 * i)
        with open(os.path.join(ordner, "%s_1h.csv" % symbol), "w",
                  encoding="utf-8") as f:
            f.write("open_time,open,high,low,close,volume\n")
            for k in tag1:
                f.write(zeile("2026-01-01 %02d:00:00" % k["h"], k))
            for k in tag2:
                f.write(zeile("2026-01-02 %02d:00:00" % k["h"], k))
        erste, letzte = aggregat(tag1), aggregat(tag2)
        if erste_verfaelschen:
            erste = dict(erste, close=erste["close"] + 1.0)
        with open(os.path.join(ordner, "%s_1d.csv" % symbol), "w",
                  encoding="utf-8") as f:
            f.write("open_time,open,high,low,close,volume\n")
            f.write(zeile("2026-01-01", erste))
            f.write(zeile("2026-01-02", letzte))
    return ordner


def _stubpruefung(eintraege, urteil="abgeleitete_teilkerze"):
    """Eine vorgetaeuschte Teilkerzen-Pruefung mit gestellten Befunden.

    ⚠️ Zwei der vier Faelle des Auftrags lassen sich aus Kursdateien **nicht**
    herstellen: `shared/zeitabdeckung.py` vergibt `rand_erste` heute nur an
    der ersten Kerze und nur dort, wo eine Deckungspruefung vorliegt. Genau
    deshalb muessen sie gestellt werden - die Regel in `snapshot.py` darf
    sich nicht darauf verlassen, dass ihre Eingabe wohlgeformt ist. Wer die
    Bedingung aus der Herkunft des Namens folgert, prueft nichts.
    """
    return types.SimpleNamespace(
        ABGELEITETE_TEILKERZE=urteil,
        jetzt_utc=lambda: __import__("datetime").datetime(2026, 9, 18),
        pruefe_ordner=lambda ordner, stand=None: eintraege,
    )


def _zieht_mit(modul, quelle, ziel, zeitabdeckung=None):
    """Wie `_zieht`, aber mit einer uebergebenen Teilkerzen-Pruefung."""
    try:
        bericht = modul.ziehen(quelle, ziel, wirklich=True, anker=False,
                               wurzel=os.path.dirname(quelle), eingaben=(),
                               zeitabdeckung=zeitabdeckung)
        return bool(bericht.get("gezogen")), bericht
    except Exception as fehler:                              # noqa: BLE001
        return False, str(fehler)


def probe_3w_sechsunddreissig_zugelassene_befunde():
    """⭐ Der Hauptfall: 36 Befunde, alle zugelassen - und es wird gezogen.

    Bis TB-48 brach dieser Lauf ab. Das ist die Aenderung, die TB-49 macht,
    und sie wird hier an einem Bestand gemessen, der die **36** des
    Registereintrags nachbaut.
    """
    arbeit = tempfile.mkdtemp(prefix="tb49_3w_")
    try:
        symbole = ["S%02d" % i for i in range(BEFUNDE_IM_BESTAND)]
        quelle = _teilkerzen_quelle(os.path.join(arbeit, "quelle"), symbole)
        ziel = os.path.join(arbeit, "snapshots")

        kerzen = snapshot.teilkerzen(quelle)
        check("3w die Pruefung schlaegt weiter an - %d Befunde, nicht null"
              % BEFUNDE_IM_BESTAND,
              len(kerzen["befunde"]) == BEFUNDE_IM_BESTAND
              and kerzen["frei_von_teilkerzen"] is False,
              "%d Befund(e)" % len(kerzen["befunde"]))
        check("3w alle Befunde sind `rand_erste`",
              {a for b in kerzen["befunde"] for a in b["arten"]}
              == {"rand_erste"},
              str(sorted({a for b in kerzen["befunde"] for a in b["arten"]})))
        check("3w alle %d sind zugelassen, keiner offen" % BEFUNDE_IM_BESTAND,
              kerzen["zugelassen_anzahl"] == BEFUNDE_IM_BESTAND
              and not kerzen["nicht_zugelassen"],
              "%d zugelassen / %d offen" % (kerzen["zugelassen_anzahl"],
                                            len(kerzen["nicht_zugelassen"])))

        rc, ausgabe = _lauf("--quelle", quelle, "--ziel", ziel,
                            "--kein-anker", "--ziehen")
        check("3w das Werkzeug ZIEHT (rc=0)", rc == 0, "rc=%d" % rc)
        check("3w und sagt in der Ausgabe, dass es Befunde gab",
              "Teilkerzen" in ausgabe and "zugelassen" in ausgabe,
              ausgabe.strip()[-200:])

        ordner = [d for d in os.listdir(ziel)
                  if os.path.isdir(os.path.join(ziel, d))]
        check("3w genau ein Snapshot ist entstanden", len(ordner) == 1,
              str(ordner))
        with open(os.path.join(ziel, ordner[0], "MANIFEST.json"),
                  encoding="utf-8") as f:
            m = json.load(f)

        zug = m.get("zugelassene_befunde")
        check("3w das Manifest fuehrt alle %d zugelassenen Befunde auf"
              % BEFUNDE_IM_BESTAND,
              isinstance(zug, list) and len(zug) == BEFUNDE_IM_BESTAND
              and m.get("zugelassene_befunde_anzahl") == BEFUNDE_IM_BESTAND,
              "%s Eintraege" % (len(zug) if isinstance(zug, list) else zug))
        check("3w je Eintrag: Name, Art und erste Kerze",
              all({"datei", "art", "erste_kerze"} <= set(e) and e["datei"]
                  and e["art"] == "rand_erste" and e["erste_kerze"]
                  for e in zug),
              str(zug[0]) if zug else "")
        check("3w die Dateinamen im Manifest sind die 36 Tagesdateien",
              {e["datei"] for e in zug}
              == {"%s_1d.csv" % s for s in symbole},
              "%d verschiedene Namen" % len({e["datei"] for e in zug}))

        herkunft = m.get("zugelassene_befunde_herkunft") or {}
        check("3w das Manifest nennt die Herkunft der Erlaubnis: "
              "Registertext 5a",
              "5a" in str(herkunft.get("registertext")),
              str(herkunft.get("registertext")))
        check("3w und die Fundstelle: Abschnitt 17.3",
              "17.3" in str(herkunft.get("fundstelle"))
              and "VORREGISTRIERUNG" in str(herkunft.get("fundstelle")),
              str(herkunft.get("fundstelle")))
        check("3w das Ergebnis der Pruefung steht unveraendert daneben",
              m["teilkerzen"]["frei_von_teilkerzen"] is False
              and len(m["teilkerzen"]["befunde"]) == BEFUNDE_IM_BESTAND,
              "%d Befunde im Manifest"
              % len(m["teilkerzen"].get("befunde") or []))

        # ⚠️ Und die Gegenprobe zur Aenderung selbst: OHNE die Ausnahme -
        # also mit der Fassung, die TB-48 vorgefunden hat - wird NICHT
        # gezogen. Sonst zeigte diese Probe nur, dass ein Snapshot entsteht.
        alt = _mutiert("ausnahme", [
            ('def _zulassung(eintrag, befund, abgeleitet):\n'
             '    """Die drei Bedingungen der Ausnahme an EINEM Befund '
             'pruefen.',
             'def _zulassung(eintrag, befund, abgeleitet):\n'
             '    return False, "keine Ausnahme - Stand vor TB-49"\n'
             '    """Die drei Bedingungen der Ausnahme an EINEM Befund '
             'pruefen.'),
        ])
        gelungen, grund = _zieht(alt, quelle, os.path.join(arbeit, "alt"))
        check("3w ⭐ am Stand VOR der Ausnahme wird nicht gezogen",
              not gelungen, (grund or "")[:100])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3x_rand_letzte_bricht_ab():
    """⚠️ `rand_letzte` bricht ab - ohne Ausnahme, auch bei EINER Datei.

    Der gefaehrliche Rand: in die letzte Kerze kann ein Abruf mitten
    hineingeschrieben haben. Registertext 5a, Zusatz nimmt sie ausdruecklich
    aus.
    """
    arbeit = tempfile.mkdtemp(prefix="tb49_3x_")
    try:
        # 36 saubere Symbole - und EINES, dessen letzter Tag angeschnitten
        # ist. Die Probe zeigt damit zugleich, dass eine einzige Datei
        # genuegt.
        quelle = _teilkerzen_quelle(os.path.join(arbeit, "quelle"),
                                    ["S%02d" % i for i in range(3)])
        _teilkerzen_quelle(quelle, ["ANGESCHNITTEN"],
                           letzte_stunden=range(0, 12))
        ziel = os.path.join(arbeit, "snapshots")

        kerzen = snapshot.teilkerzen(quelle)
        arten = {a for b in kerzen["befunde"] for a in b["arten"]}
        check("3x der Bestand traegt einen `rand_letzte`",
              "rand_letzte" in arten, str(sorted(arten)))
        check("3x genau eine Datei ist nicht zugelassen",
              len(kerzen["nicht_zugelassen"]) == 1,
              str([e["datei"] for e in kerzen["nicht_zugelassen"]]))
        # ⚠️ Vier, nicht drei: die angeschnittene Datei traegt BEIDE Befunde -
        # ihr `rand_erste` ist zugelassen, ihr `rand_letzte` nicht. Die
        # Zulassung wird je Befund entschieden, nicht je Datei; genau deshalb
        # bricht die Datei trotzdem ab.
        check("3x vier `rand_erste` bleiben zugelassen - je Befund, nicht "
              "je Datei", kerzen["zugelassen_anzahl"] == 4,
              "%d zugelassen" % kerzen["zugelassen_anzahl"])

        rc, ausgabe = _lauf("--quelle", quelle, "--ziel", ziel,
                            "--kein-anker", "--ziehen")
        check("3x echtes Modul: Abbruch (2)", rc == 2, "rc=%d" % rc)
        check("3x die Datei wird genannt",
              "ANGESCHNITTEN_1d.csv" in ausgabe, ausgabe.strip()[:200])
        check("3x und die Begruendung nennt die Art `rand_letzte`",
              "rand_letzte" in ausgabe, ausgabe.strip()[:200])
        check("3x es entsteht KEIN Snapshot", not os.path.exists(ziel))

        # Ohne Bedingung (a) waere `rand_letzte` mit durchgegangen.
        ohne = _mutiert("bedingung_a", [
            ('    if art != ZUGELASSENE_ART:', '    if False:'),
        ])
        gelungen, grund = _zieht(ohne, quelle, ziel)
        check("3x ohne Bedingung (a): der Snapshot entsteht trotz "
              "`rand_letzte`", gelungen, grund or "")
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3y_nicht_abgeleitet_bricht_ab():
    """⚠️ Ein `rand_erste`, der NICHT das Aggregat der feineren Kerzen ist.

    Das ist der Fall, den die Ausnahme gerade nicht deckt: die Kerze
    **widerspricht** ihren Stundenkerzen. Mindestens eine der beiden Dateien
    ist am Rand angeschnitten - und welche, sagt niemand.
    """
    arbeit = tempfile.mkdtemp(prefix="tb49_3y_")
    try:
        quelle = _teilkerzen_quelle(os.path.join(arbeit, "quelle"),
                                    ["S%02d" % i for i in range(3)])
        _teilkerzen_quelle(quelle, ["VERFAELSCHT"], erste_verfaelschen=True)
        ziel = os.path.join(arbeit, "snapshots")

        kerzen = snapshot.teilkerzen(quelle)
        check("3y der Befund ist weiterhin ein `rand_erste`",
              all(b["arten"] == ["rand_erste"] for b in kerzen["befunde"]),
              str(sorted({a for b in kerzen["befunde"] for a in b["arten"]})))
        check("3y aber er ist NICHT zugelassen",
              [e["datei"] for e in kerzen["nicht_zugelassen"]]
              == ["VERFAELSCHT_1d.csv"],
              str([e["datei"] for e in kerzen["nicht_zugelassen"]]))
        check("3y und der Grund nennt das Urteil `unbelegt`",
              any("unbelegt" in g["grund"]
                  for e in kerzen["nicht_zugelassen"] for g in e["gruende"]),
              str(kerzen["nicht_zugelassen"][:1])[:160])

        rc, ausgabe = _lauf("--quelle", quelle, "--ziel", ziel,
                            "--kein-anker", "--ziehen")
        check("3y echtes Modul: Abbruch (2)", rc == 2, "rc=%d" % rc)
        check("3y die Datei wird genannt",
              "VERFAELSCHT_1d.csv" in ausgabe, ausgabe.strip()[:200])
        check("3y es entsteht KEIN Snapshot", not os.path.exists(ziel))

        ohne = _mutiert("bedingung_c", [
            ('    if urteil != abgeleitet or deckung.get("aggregat_passt") '
             'is not True:', '    if False:'),
        ])
        gelungen, grund = _zieht(ohne, quelle, ziel)
        check("3y ohne Bedingung (c): der Snapshot entsteht trotz "
              "widersprechender Kerze", gelungen, grund or "")
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3z_befund_an_spaeterer_kerze_bricht_ab():
    """⚠️ Ein `rand_erste` an einer ANDEREN als der ersten Kerze.

    ⚠️ Dieser Fall laesst sich aus Kursdateien nicht herstellen: die heutige
    Pruefung vergibt `rand_erste` nur an der ersten Kerze. Genau deshalb wird
    er **gestellt** - Bedingung (b) darf nicht aus dem Namen der Art gefolgert
    werden, sondern muss die Kerze gegen die erste Kerze der Datei halten.
    Zoege das Werkzeug hier, haette es die Bedingung nur behauptet.
    """
    arbeit = tempfile.mkdtemp(prefix="tb49_3z_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"))
        ziel = os.path.join(arbeit, "snapshots")

        gestellt = [{
            "datei": "SPAET_1d.csv", "symbol": "SPAET", "intervall": "1d",
            "erste": "2026-01-01", "letzte": "2026-01-09",
            "befunde": [{"art": "rand_erste",
                         "urteil": "abgeleitete_teilkerze",
                         "text": "Erste Kerze 2026-01-05: …"}],
            "hinweise": [],
            "deckung": {"erste": {"kerze": "2026-01-05",
                                  "urteil": "abgeleitete_teilkerze",
                                  "aggregat_passt": True}},
        }]
        gelungen, grund = _zieht_mit(snapshot, quelle, ziel,
                                     _stubpruefung(gestellt))
        check("3z echtes Modul: es wird NICHT gezogen", not gelungen,
              str(grund)[:120])
        check("3z die Datei wird genannt",
              "SPAET_1d.csv" in str(grund), str(grund)[:200])
        check("3z der Grund nennt beide Kerzen",
              "2026-01-05" in str(grund) and "2026-01-01" in str(grund),
              str(grund)[:200])
        check("3z es entsteht kein Snapshot", not os.path.exists(ziel))

        ohne = _mutiert("bedingung_b", [
            ('    if not erste or deckung.get("kerze") != erste:',
             '    if False:'),
        ])
        gelungen2, _ = _zieht_mit(ohne, quelle, ziel, _stubpruefung(gestellt))
        check("3z ohne Bedingung (b): der Snapshot entsteht trotz Befund an "
              "spaeterer Kerze", gelungen2)
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3aa_kein_zeuge():
    """⭐ Der fuenfte Fall: eine Datei OHNE feineren Zeugen.

    ⚠️ **Die Entscheidung, und ihre Begruendung.** Bedingung (c) verlangt den
    Nachweis, dass die Kerze das Aggregat genau der vorhandenen feineren
    Kerzen ist. Ohne Zeugen gibt es diesen Nachweis nicht. **Nicht belegbar
    ist nicht zugelassen** - dieselbe Regel, nach der dieses Projekt seit
    TB-45 die **2** von der **0** trennt: wer nicht messen konnte, sagt es,
    statt "in Ordnung" zu melden.

    ⭐ **Folgenlos fuer den Bestand, und das wird hier gemessen:** 175 der 223
    Dateien tragen `kein_zeuge`, und **keine einzige** von ihnen traegt einen
    Befund. `pruefe_datei` kehrt bei fehlendem Zeugen um, **bevor** die
    Deckungspruefung laeuft; die Art `rand_erste` entsteht allein aus dieser
    Pruefung. Die Regel kann dort also gar nicht greifen - sie wird erst
    scharf, wenn eine Eingabe von aussen einen Befund ohne Deckung behauptet.
    """
    arbeit = tempfile.mkdtemp(prefix="tb49_3aa_")
    try:
        # (1) Der echte Fall: eine Tagesdatei ohne Stundendatei.
        quelle = os.path.join(arbeit, "quelle")
        _teilkerzen_quelle(quelle, ["MITZEUGE"])
        os.remove(os.path.join(quelle, "MITZEUGE_1h.csv"))
        kerzen = snapshot.teilkerzen(quelle)
        check("3aa ohne Zeugen entsteht ueberhaupt kein Befund",
              kerzen["befunde"] == [] and kerzen["frei_von_teilkerzen"],
              str(kerzen["befunde"]))

        # (2) Der gestellte Fall: ein `rand_erste` OHNE Deckungspruefung.
        quelle2 = _quelle_bauen(os.path.join(arbeit, "quelle2"))
        ziel = os.path.join(arbeit, "snapshots")
        gestellt = [{
            "datei": "OHNEZEUGE_1d.csv", "symbol": "OHNEZEUGE",
            "intervall": "1d", "erste": "2026-01-01", "letzte": "2026-01-09",
            "befunde": [{"art": "rand_erste",
                         "text": "Erste Kerze 2026-01-01: …"}],
            "hinweise": [{"art": "kein_zeuge", "text": "keine feinere Datei"}],
        }]
        gelungen, grund = _zieht_mit(snapshot, quelle2, ziel,
                                     _stubpruefung(gestellt))
        check("3aa ein behaupteter `rand_erste` ohne Deckung zieht NICHT",
              not gelungen, str(grund)[:120])
        check("3aa und der Grund sagt, dass er nicht belegbar ist",
              "nicht belegbar" in str(grund), str(grund)[:220])
        check("3aa es entsteht kein Snapshot", not os.path.exists(ziel))

        # ⚠️ Die Mutation baut genau den stillen Rueckfall ein, den das Modul
        # verweigert: "keine Deckungspruefung vorhanden" wird zu "war schon in
        # Ordnung". Das ist die Bauform aus TB-45 - ein gescheiterter Nachweis
        # und ein gefuehrter Nachweis sehen dann gleich aus.
        ohne = _mutiert("keine_deckung", [
            ('    if deckung is None:\n',
             '    if deckung is None:\n'
             '        deckung = {"kerze": eintrag.get("erste"),\n'
             '                   "urteil": abgeleitet,\n'
             '                   "aggregat_passt": True}\n'
             '    if False:\n'),
        ])
        gelungen2, _ = _zieht_mit(ohne, quelle2, ziel,
                                  _stubpruefung(gestellt))
        check("3aa ohne diese Wache: der Snapshot entsteht auf einem "
              "unbelegten Befund", gelungen2)
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3ab_urteil_nicht_ermittelbar():
    """⚠️ Bedingung (c) ist nicht pruefbar: **2**, nie 0.

    Die Lehre aus TB-45 auf die Ausnahme angewandt. Bedingung (c) haengt am
    Urteil `ABGELEITETE_TEILKERZE` der Teilkerzen-Pruefung. Zieht die Pruefung
    diesen Namen ein, ist die Bedingung **nicht mehr pruefbar** - und dann
    wird nicht gezogen, statt sie stillschweigend als erfuellt zu behandeln.

    ⚠️ **Die gefaehrliche Reparatur waere, den Namen in `snapshot.py`
    abzuschreiben.** Dann prueft das Werkzeug gegen ein Urteil, das die
    Pruefung gar nicht mehr vergibt, und die Ausnahme greift entweder nie
    oder - wie hier gezeigt - **immer**. Genau diese Fassung ist die Mutation.
    """
    arbeit = tempfile.mkdtemp(prefix="tb49_3ab_")
    echter_pfad = snapshot.ZEITABDECKUNG_PFAD
    try:
        quelle = _teilkerzen_quelle(os.path.join(arbeit, "quelle"), ["AAA"])
        ziel = os.path.join(arbeit, "snapshots")

        # Eine echte Fassung von `zeitabdeckung.py`, in der das Urteil
        # umbenannt ist - der Werteinhalt bleibt, nur der Name geht weg.
        with open(echter_pfad, "r", encoding="utf-8") as f:
            text = f.read()
        if "ABGELEITETE_TEILKERZE" not in text:
            raise AssertionError(
                "zeitabdeckung.py kennt `ABGELEITETE_TEILKERZE` nicht mehr - "
                "dann prueft diese Probe etwas anderes als angenommen.")
        umbenannt = os.path.join(arbeit, "zeitabdeckung_umbenannt.py")
        with open(umbenannt, "w", encoding="utf-8") as f:
            f.write(text.replace("ABGELEITETE_TEILKERZE",
                                 "ABGELEITETE_TEILKERZE_NEU"))

        snapshot.ZEITABDECKUNG_PFAD = umbenannt
        gelungen, grund = _zieht(snapshot, quelle, ziel)
        check("3ab der eingezogene Name laesst NICHT ziehen", not gelungen,
              str(grund)[:120])
        check("3ab und die Begruendung nennt ihn beim Namen",
              "ABGELEITETE_TEILKERZE" in str(grund), str(grund)[:200])
        check("3ab es entsteht kein Snapshot", not os.path.exists(ziel))

        rc = snapshot.main(["--quelle", quelle, "--ziel", ziel,
                            "--kein-anker", "--ziehen"])
        check("3ab der Rueckgabewert ist NICHT_PRUEFBAR (2), nie 0",
              rc == snapshot.NICHT_PRUEFBAR, "rc=%s" % rc)

        # ⚠️ Die Mutation: das Urteil wird abgeschrieben statt geholt.
        abgeschrieben = _mutiert("urteil_abgeschrieben", [
            ('    if not hasattr(modul, "ABGELEITETE_TEILKERZE"):',
             '    if False:'),
            ('    abgeleitet = getattr(modul, "ABGELEITETE_TEILKERZE", None)',
             '    abgeleitet = getattr(modul, "ABGELEITETE_TEILKERZE", '
             '"abgeleitete_teilkerze")'),
        ])
        abgeschrieben.ZEITABDECKUNG_PFAD = umbenannt
        gelungen2, grund2 = _zieht(abgeschrieben, quelle,
                                   os.path.join(arbeit, "snapshots2"))
        check("3ab mit abgeschriebenem Urteil entsteht der Snapshot doch",
              gelungen2, str(grund2)[:120])

        # Und eine Pruefung, die den Namen gar nicht erst mitbringt.
        stumpf = types.SimpleNamespace(
            jetzt_utc=lambda: __import__("datetime").datetime(2026, 9, 18),
            pruefe_ordner=lambda ordner, stand=None: [])
        snapshot.ZEITABDECKUNG_PFAD = echter_pfad
        gelungen3, grund3 = _zieht_mit(snapshot, quelle,
                                       os.path.join(arbeit, "snapshots3"),
                                       stumpf)
        check("3ab auch eine uebergebene Pruefung ohne den Namen zieht nicht",
              not gelungen3, str(grund3)[:120])
    finally:
        snapshot.ZEITABDECKUNG_PFAD = echter_pfad
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3ac_negativprobe_ohne_befund():
    """Die Negativprobe: ein Bestand OHNE jeden Befund zieht unveraendert.

    ⚠️ Ohne sie zeigte dieser Abschnitt nur, dass etwas abbricht. Eine Probe,
    die nur rot sein kann, beweist nichts - dieselbe Bauform wie in
    Abschnitt 3.
    """
    arbeit = tempfile.mkdtemp(prefix="tb49_3ac_")
    try:
        quelle, snap = _snapshot_bauen(arbeit)
        with open(os.path.join(snap, "MANIFEST.json"), encoding="utf-8") as f:
            m = json.load(f)
        check("3ac ein Bestand ohne Befund zieht weiterhin",
              os.path.isdir(snap))
        check("3ac die Pruefung meldet ihn als frei von Teilkerzen",
              m["teilkerzen"]["frei_von_teilkerzen"] is True
              and m["teilkerzen"]["befunde"] == [])
        check("3ac das Manifest fuehrt null zugelassene Befunde",
              m.get("zugelassene_befunde") == []
              and m.get("zugelassene_befunde_anzahl") == 0,
              str(m.get("zugelassene_befunde_anzahl")))
        check("3ac und nennt die Herkunft der Erlaubnis trotzdem",
              "17.3" in str((m.get("zugelassene_befunde_herkunft")
                             or {}).get("fundstelle")),
              str((m.get("zugelassene_befunde_herkunft") or {})
                  .get("fundstelle")))
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def probe_3ad_keine_uebergehen_flagge():
    """⚠️ Es gibt KEINE Uebergehen-Flagge - und das wird gemessen.

    Registertext 5a, Zusatz: *"Die Pruefung selbst wird nicht
    abgeschwaecht."* Eine Option, die Befunde uebergeht, waere die Ausnahme
    in ihr Gegenteil verkehrt. Diese Probe haelt die Befehlszeile dagegen.
    """
    with open(SNAPSHOT_PFAD, "r", encoding="utf-8") as f:
        quelltext = f.read()
    verdaechtig = [w for w in ("--teilkerzen-egal", "--ohne-teilkerzen",
                               "--kein-teilkerzen", "--befunde-egal",
                               "--trotzdem", "--erzwingen", "--force")
                   if w in quelltext]
    check("3ad snapshot.py kennt keine Option, die Befunde uebergeht",
          not verdaechtig, str(verdaechtig))

    arbeit = tempfile.mkdtemp(prefix="tb49_3ad_")
    try:
        quelle = _teilkerzen_quelle(os.path.join(arbeit, "quelle"),
                                    ["VERFAELSCHT"], erste_verfaelschen=True)
        ziel = os.path.join(arbeit, "snapshots")
        for flagge in ("--trotzdem", "--erzwingen", "--force"):
            rc, _ = _lauf("--quelle", quelle, "--ziel", ziel, "--kein-anker",
                          "--ziehen", flagge)
            check("3ad `%s` gibt es nicht (rc=2)" % flagge, rc == 2,
                  "rc=%d" % rc)
        check("3ad und ohne Flagge bleibt es beim Abbruch",
              _lauf("--quelle", quelle, "--ziel", ziel, "--kein-anker",
                    "--ziehen")[0] == 2)
        check("3ad es entsteht kein Snapshot", not os.path.exists(ziel))
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


def abschnitt_3c():
    print("\n3c. TB-49 - DIE AUSNAHME `rand_erste` (Registertext 5a, 17.3)")
    for probe in (probe_3w_sechsunddreissig_zugelassene_befunde,
                  probe_3x_rand_letzte_bricht_ab,
                  probe_3y_nicht_abgeleitet_bricht_ab,
                  probe_3z_befund_an_spaeterer_kerze_bricht_ab,
                  probe_3aa_kein_zeuge,
                  probe_3ab_urteil_nicht_ermittelbar,
                  probe_3ac_negativprobe_ohne_befund,
                  probe_3ad_keine_uebergehen_flagge):
        try:
            probe()
        except AssertionError as fehler:
            FEHLER.append(probe.__name__ + " (Anker)")
            print("  [FEHLER] %s: %s" % (probe.__name__, fehler))
        except Exception as fehler:                          # noqa: BLE001
            import traceback
            FEHLER.append(probe.__name__ + " (Ausnahme)")
            print("  [FEHLER] %s warf eine Ausnahme: %s"
                  % (probe.__name__, fehler))
            traceback.print_exc()


# ===========================================================================
# Abschnitt 4 - Die Rueckgabewerte sind unterscheidbar
# ===========================================================================

def abschnitt_4():
    print("\n4. DIE DREI RUECKGABEWERTE SIND UNTERSCHEIDBAR")
    check("die drei Werte sind verschieden",
          len({snapshot.OK, snapshot.BEFUND, snapshot.NICHT_PRUEFBAR}) == 3,
          "%d / %d / %d" % (snapshot.OK, snapshot.BEFUND,
                            snapshot.NICHT_PRUEFBAR))
    check("und die drei Ausgaenge von --pruefen auch",
          len({snapshot.UNVERAENDERT, snapshot.VERAENDERT,
               snapshot.UNPRUEFBAR}) == 3)
    # `--nur-hash` ist der einzige Aufruf, der nichts anlegt und nichts
    # prueft - er muss trotzdem 0 liefern, sonst waere er nicht benutzbar.
    arbeit = tempfile.mkdtemp(prefix="tb46_4_")
    try:
        quelle = _quelle_bauen(os.path.join(arbeit, "quelle"))
        rc, ausgabe = _lauf("--quelle", quelle, "--nur-hash")
        erwartet, anzahl = snapshot.gesamthash(quelle)
        check("--nur-hash gibt den Hash aus und liefert 0",
              rc == 0 and erwartet in ausgabe, "rc=%d" % rc)
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


# ===========================================================================
# Abschnitt 5 - Die Randbedingung: `data/` ist unberuehrt
# ===========================================================================

def abschnitt_5(vorher):
    print("\n5. RANDBEDINGUNG - unter data/ ist nichts passiert")
    if vorher is None:
        check("der Datenstand war vor dem Lauf messbar", False,
              "vorher nicht gemessen")
        return
    nachher = snapshot.gesamthash(DATA_DIR)
    check("der Datenstand-Hash ist derselbe wie vor dem Lauf",
          nachher == vorher,
          "vorher %s.../%d, nachher %s.../%d"
          % (vorher[0][:16], vorher[1], nachher[0][:16], nachher[1]))

    lauf = subprocess.run(["git", "-C", BASE_DIR, "status", "--porcelain",
                           "--", "data"], capture_output=True, text=True)
    # ⚠️ Der Rueckgabewert zuerst: ein gescheitertes `git` hat eine leere
    # Ausgabe, und leer sah in TB-45 wie "nichts veraendert" aus.
    if lauf.returncode != 0:
        check("git kann den Zustand von data/ beurteilen", False,
              (lauf.stderr or "").strip()[:120])
        return
    offen = [z for z in lauf.stdout.splitlines() if z.strip()]
    check("git sieht unter data/ nichts Geaendertes oder Unversioniertes",
          not offen, str(offen)[:200])


def main():
    print("=" * 78)
    print("TB-46/47/49: das Snapshot-Werkzeug und seine Wache")
    print("=" * 78)

    vorher = None
    if os.path.isdir(DATA_DIR):
        try:
            vorher = snapshot.gesamthash(DATA_DIR)
        except snapshot.Snapshotfehler as fehler:
            print("  ⚠️ Datenstand vorher nicht messbar: %s" % fehler)

    for abschnitt in (abschnitt_1, abschnitt_2, abschnitt_3, abschnitt_3b,
                      abschnitt_3c, abschnitt_4):
        try:
            abschnitt()
        except Exception as fehler:                          # noqa: BLE001
            import traceback
            FEHLER.append("%s (Ausnahme)" % abschnitt.__name__)
            print("  [FEHLER] %s warf eine Ausnahme: %s"
                  % (abschnitt.__name__, fehler))
            traceback.print_exc()
    try:
        abschnitt_5(vorher)
    except Exception as fehler:                              # noqa: BLE001
        FEHLER.append("abschnitt_5 (Ausnahme)")
        print("  [FEHLER] abschnitt_5 warf eine Ausnahme: %s" % fehler)

    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print("%d von %d Pruefungen bestanden, %d fehlgeschlagen."
          % (BESTANDEN, gesamt, len(FEHLER)))
    for name in FEHLER:
        print("  - %s" % name)
    if gesamt == 0:
        # Die Lehre aus TB-45 auf diesen Test selbst angewandt: null
        # Pruefungen sind kein Erfolg.
        print("KEINE EINZIGE PRUEFUNG GELAUFEN - das ist ein Fehler, "
              "kein Bestehen.")
        return 1
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
