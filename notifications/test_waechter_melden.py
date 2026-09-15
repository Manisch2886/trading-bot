"""
Selbsttests des Waechter-Wrappers
==============================================================================
Geprueft wird das VERHALTEN von notifications/waechter_melden.py: ein echter
Unterprozess wird gestartet, seine Ausgabe und sein Rueckgabewert kommen aus
einem echten Programm, und der Zustand entsteht dadurch, dass der Wrapper
mehrfach laeuft.

KEIN einziger echter Telegram-Aufruf. Der Sendeweg ist ein Parameter; die
Attrappe zaehlt die Nachrichten, haelt ihren Text fest und laesst sich gezielt
kaputtmachen - dieselbe Bauart wie in
notifications/test_schliess_benachrichtigung.py.

------------------------------------------------------------------------------
ZWEI FALLEN, DIE IN DIESEM REPO WIEDERHOLT AUFGETRETEN SIND
------------------------------------------------------------------------------
FALLE 1 - die Probe, die ihren eigenen Zustand herstellt. Ein Test, der die
Zustandsdatei von Hand schreibt und danach prueft, dass gedaempft wird,
bestaetigt nur seine eigene Datei. Er wuerde auch dann bestehen, wenn der
Wrapper ueberhaupt nichts vermerkt. Deshalb schreibt KEIN Test hier eine
Zustandsdatei; jeder Zustand entsteht durch einen vorherigen Lauf des
Wrappers, und geprueft wird der ABLAUF ueber mehrere Laeufe hinweg
(`test_daempfung`, `test_versand_fehlgeschlagen`, `test_wieder_in_ordnung`).
Abschnitt "Mutationsproben" belegt zusaetzlich, dass diese Tests ueberhaupt
anschlagen koennen.

FALLE 2 - eine zweite Wache verdeckt das Fehlen der ersten. Die wichtigste
Zusicherung dieses Wrappers ist "Rueckgabewert 0 -> keine Meldung". Wuerde man
sie an einem Waechter pruefen, der vorher schon einen Befund vermerkt hatte,
koennte das Schweigen auch von der Daempfung kommen - und ein Wrapper, der die
Null-Regel gar nicht kennt, bestuende den Test. `test_null_schweigt` beginnt
deshalb mit einer LEEREN Zustandsdatei: dann gibt es nichts zu daempfen, und
nur die gepruefte Regel kann noch schweigen. Umgekehrt arbeitet
`test_daempfung` ausschliesslich mit Rueckgabewert 1, wo die Null-Regel nicht
greifen kann. Jeder Test misst genau eine Regel.

Aufruf:  python3 notifications/test_waechter_melden.py
"""

import ast
import contextlib
import datetime
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)

import waechter_melden as wm                                 # noqa: E402

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
# Werkzeuge der Tests
# ---------------------------------------------------------------------------
class Sender:
    """Attrappe des Sendewegs. Zaehlt, haelt fest, laesst sich kaputtmachen.

    `scheitert`:  liefert False (so verhaelt sich send_alert bei Netzfehler).
    `wirft`:      wirft eine Ausnahme (so verhielte sich ein kaputter
                  Sendeweg, den send_alert NICHT abgefangen hat).
    """

    def __init__(self, scheitert=False, wirft=False):
        self.texte = []
        self.scheitert = scheitert
        self.wirft = wirft

    def __call__(self, text):
        self.texte.append(text)
        if self.wirft:
            raise ConnectionError("api.telegram.org nicht erreichbar")
        return not self.scheitert

    @property
    def anzahl(self):
        return len(self.texte)

    @property
    def letzte(self):
        return self.texte[-1] if self.texte else ""


class Wegwerf:
    """Ein Ordner unter /tmp mit einer Waechter-Attrappe darin.

    Die Attrappe ist ein echtes Programm: sie druckt, was ihr per
    Umgebungsvariable vorgegeben wird, und endet mit dem vorgegebenen
    Rueckgabewert. Damit laeuft der Wrapper gegen einen echten Unterprozess
    und nicht gegen eine nachgebaute Vorstellung davon.
    """

    SKRIPT = (
        "import os, sys\n"
        "sys.stdout.write(os.environ.get('PROBE_AUS', ''))\n"
        "sys.stderr.write(os.environ.get('PROBE_FEHLER', ''))\n"
        "if os.environ.get('PROBE_WIRFT'):\n"
        "    raise RuntimeError(os.environ['PROBE_WIRFT'])\n"
        "sys.exit(int(os.environ.get('PROBE_RC', '0')))\n"
    )

    def __enter__(self):
        self.wurzel = tempfile.mkdtemp(prefix="waechter_")
        self.skript = os.path.join(self.wurzel, "probe.py")
        with open(self.skript, "w") as datei:
            datei.write(self.SKRIPT)
        self.zustand = os.path.join(self.wurzel, "zustand.json")
        return self

    def __exit__(self, *_):
        for schluessel in ("PROBE_AUS", "PROBE_FEHLER", "PROBE_RC", "PROBE_WIRFT"):
            os.environ.pop(schluessel, None)
        shutil.rmtree(self.wurzel, ignore_errors=True)

    @property
    def waechter(self):
        return wm.Waechter(schluessel="probe", klartext="Probe-Waechter",
                           befehl=(self.skript,), log="logs/system/probe.log",
                           marken=("BEFUND",), zweck="tut so")

    def stelle(self, rc=0, aus="", fehler="", wirft=""):
        os.environ["PROBE_RC"] = str(rc)
        os.environ["PROBE_AUS"] = aus
        os.environ["PROBE_FEHLER"] = fehler
        os.environ["PROBE_WIRFT"] = wirft

    def vermerke(self):
        """Der vermerkte Zustand - GELESEN, nie geschrieben."""
        if not os.path.exists(self.zustand):
            return {}
        with open(self.zustand) as datei:
            return json.load(datei)["waechter"]


T0 = datetime.datetime(2026, 9, 14, 3, 50, 0)


def tag(n):
    return T0 + datetime.timedelta(days=n)


def fuehre_aus(ort, senden, jetzt=None, **rest):
    """Ein vollstaendiger Lauf. Gibt (Rueckgabewert, stdout, stderr) zurueck.

    stdout/stderr werden abgefangen, damit die Testausgabe lesbar bleibt -
    der Wrapper schreibt dabei genau dorthin, wo im Cronjob die Logdatei
    haengt.
    """
    aus, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(aus), contextlib.redirect_stderr(err):
        rc = wm.lauf(ort.waechter, senden=senden, zustand_pfad=ort.zustand,
                     jetzt=jetzt or T0, **rest)
    return rc, aus.getvalue(), err.getvalue()


BEFUNDTEXT = "BEFUND: 3 von 9 Kurven passen nicht zur heutigen Konfiguration.\n"


# ===========================================================================
# 1. Rueckgabewert 1 -> Meldung
# ===========================================================================
def test_befund_meldet():
    print("\n--- 1. Rueckgabewert 1 heisst Befund und wird gemeldet ---")
    with Wegwerf() as ort:
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        s = Sender()
        rc, aus, _ = fuehre_aus(ort, s)

        check("Genau EINE Nachricht", s.anzahl == 1, f"{s.anzahl}")
        check("Der Rueckgabewert des Waechters kommt unveraendert heraus",
              rc == 1, f"rc={rc}")
        check("Die Ausgabe des Waechters steht im Log",
              BEFUNDTEXT.strip() in aus)
        check("Die Nachricht nennt den Waechter im Klartext, nicht die Datei",
              "Probe-Waechter" in s.letzte and "probe.py" not in s.letzte)
        check("Die Nachricht nennt, was gefunden wurde",
              "3 von 9 Kurven" in s.letzte)
        check("Die Nachricht nennt den Befehl zum Nachsehen",
              "tail -n 60 ~/trading-bot/logs/system/probe.log" in s.letzte)
        check("Sie ist kurz genug fuers Telefon (hoechstens 6 Zeilen)",
              len(s.letzte.splitlines()) <= 6,
              f"{len(s.letzte.splitlines())} Zeilen")
        check("Der Befund ist vermerkt worden",
              ort.vermerke().get("probe", {}).get("klasse") == wm.BEFUND)


# ===========================================================================
# 2. Rueckgabewert 0 -> keine Meldung (die wichtigere Haelfte)
# ===========================================================================
def test_null_schweigt():
    print("\n--- 2. Rueckgabewert 0 heisst in Ordnung und wird verschwiegen ---")
    # FALLE 2: leerer Zustand. Es gibt nichts zu daempfen - schweigt der
    # Wrapper hier, kann das NUR an der Null-Regel liegen.
    with Wegwerf() as ort:
        check("Vorbedingung: es ist nichts vermerkt, was daempfen koennte",
              ort.vermerke() == {})
        ort.stelle(rc=0, aus="Alle geprueften Kurven passen.\n")
        s = Sender()
        rc, aus, _ = fuehre_aus(ort, s)

        check("KEINE Nachricht", s.anzahl == 0, f"{s.anzahl}")
        check("Der Rueckgabewert bleibt 0", rc == 0, f"rc={rc}")
        check("Die Ausgabe steht trotzdem im Log",
              "Alle geprueften Kurven passen." in aus)
        check("Es wird auch nichts vermerkt - der Zustand bleibt leer",
              ort.vermerke() == {})

    # Zehn Laeufe hintereinander: auch der zehnte schweigt. Ein Wrapper, der
    # nur den ERSTEN Lauf besonders behandelt, faellt hier auf.
    with Wegwerf() as ort:
        ort.stelle(rc=0, aus="Alles in Ordnung.\n")
        s = Sender()
        for i in range(10):
            fuehre_aus(ort, s, jetzt=tag(i))
        check("Auch nach zehn Laeufen in Folge: keine einzige Nachricht",
              s.anzahl == 0, f"{s.anzahl}")


def test_wieder_in_ordnung():
    print("\n--- 2b. Aus Befund wird wieder 0: kein Wort, und der Vermerk faellt ---")
    with Wegwerf() as ort:
        s = Sender()
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        fuehre_aus(ort, s, jetzt=tag(0))
        check("Vorbedingung: der Befund ist gemeldet und vermerkt",
              s.anzahl == 1 and "probe" in ort.vermerke())

        ort.stelle(rc=0, aus="Alles in Ordnung.\n")
        fuehre_aus(ort, s, jetzt=tag(1))
        check("Die Aufloesung wird NICHT gemeldet", s.anzahl == 1, f"{s.anzahl}")
        check("Der Vermerk ist geraeumt", ort.vermerke() == {})

        # Und der naechste Befund gilt deshalb wieder als neu - nicht als
        # Fortsetzung eines alten.
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        fuehre_aus(ort, s, jetzt=tag(2))
        check("Ein spaeter wiederkehrender Befund wird wieder gemeldet",
              s.anzahl == 2, f"{s.anzahl}")
        check("und zwar als 'neu', nicht als Erinnerung",
              s.letzte.splitlines()[0].endswith("- neu"),
              s.letzte.splitlines()[0])


# ===========================================================================
# 3. Absturz -> unterscheidbare Meldung
# ===========================================================================
def test_absturz():
    print("\n--- 3. Ein Absturz ist etwas anderes als ein Befund ---")
    with Wegwerf() as ort:
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        s_befund = Sender()
        fuehre_aus(ort, s_befund)
        befundnachricht = s_befund.letzte

    faelle = [
        ("Rueckgabewert 2", dict(rc=2, fehler="--perms muss mindestens 2 sein.\n"), 2),
        ("Rueckgabewert 127", dict(rc=127, fehler="command not found\n"), 127),
        ("unbehandelte Ausnahme", dict(wirft="Kursdatei fehlt"), 1),
    ]
    for titel, stellung, erwartet_rc in faelle:
        with Wegwerf() as ort:
            ort.stelle(**stellung)
            s = Sender()
            rc, _, _ = fuehre_aus(ort, s)

            check(f"{titel}: es wird gemeldet", s.anzahl == 1, f"{s.anzahl}")
            check(f"{titel}: der Rueckgabewert bleibt der des Waechters",
                  rc == erwartet_rc, f"rc={rc}")
            check(f"{titel}: die Nachricht ist als Absturz gekennzeichnet",
                  s.letzte.startswith("[ABGESTUERZT]"),
                  s.letzte.splitlines()[0])
            check(f"{titel}: sie sagt ausdruecklich, dass KEIN Befund vorliegt",
                  "KEIN Befund" in s.letzte)
            check(f"{titel}: sie ist nicht dieselbe wie bei einem Befund",
                  s.letzte != befundnachricht)
            check(f"{titel}: als Absturz vermerkt, nicht als Befund",
                  ort.vermerke()["probe"]["klasse"] == wm.ABGESTUERZT)

    # Der Sonderfall: eine Ausnahme beendet Python mit Rueckgabewert 1 -
    # demselben Wert wie ein Befund. Ohne die Traceback-Probe waere der
    # Absturz von einem Befund nicht zu unterscheiden.
    with Wegwerf() as ort:
        ort.stelle(wirft="Kursdatei fehlt")
        s = Sender()
        rc, _, _ = fuehre_aus(ort, s)
        check("Der Sonderfall ist wirklich Rueckgabewert 1 - genau der eines "
              "Befundes", rc == 1, f"rc={rc}")
        check("und wird trotzdem als Absturz eingeordnet",
              ort.vermerke()["probe"]["klasse"] == wm.ABGESTUERZT)
        check("Die Traceback selbst steht nicht in der Nachricht, nur die "
              "Ausnahme", "RuntimeError: Kursdatei fehlt" in s.letzte
              and wm.TRACEBACK_MARKE not in s.letzte)

    # Ein nicht startbares Programm.
    with Wegwerf() as ort:
        kaputt = wm.Waechter("probe", "Probe-Waechter",
                             (os.path.join(ort.wurzel, "gibtesnicht.py"),),
                             "logs/system/probe.log", ("BEFUND",), "-")
        s = Sender()
        aus, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(aus), contextlib.redirect_stderr(err):
            rc = wm.lauf(kaputt, senden=s, zustand_pfad=ort.zustand, jetzt=T0)
        check("Ein nicht auffindbares Werkzeug wird als Absturz gemeldet",
              s.anzahl == 1 and s.letzte.startswith("[ABGESTUERZT]"),
              s.letzte.splitlines()[0] if s.texte else "keine Nachricht")
        check("und bekommt einen Rueckgabewert ungleich 0 und 1",
              rc not in (0, 1), f"rc={rc}")

    # Der Uebergang Befund -> Absturz ist immer eine Meldung wert, auch am
    # selben Tag: die Daempfung darf ihn nicht verschlucken.
    with Wegwerf() as ort:
        s = Sender()
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        fuehre_aus(ort, s, jetzt=tag(0))
        ort.stelle(rc=2, fehler="kaputt\n")
        fuehre_aus(ort, s, jetzt=tag(0))
        check("Wechselt ein Waechter von Befund auf Absturz, wird gemeldet",
              s.anzahl == 2, f"{s.anzahl}")
        check("und zwar als Absturz", s.letzte.startswith("[ABGESTUERZT]"))


# ===========================================================================
# 4. Telegram nicht erreichbar -> der Waechter laeuft trotzdem durch
# ===========================================================================
def test_sendeweg_kaputt():
    print("\n--- 4. Ein kaputter Sendeweg erreicht den Waechter nicht ---")
    for titel, sender in (("Versand meldet Fehlschlag", Sender(scheitert=True)),
                          ("Versand wirft eine Ausnahme", Sender(wirft=True))):
        with Wegwerf() as ort:
            ort.stelle(rc=1, aus=BEFUNDTEXT)
            rc, aus, err = fuehre_aus(ort, sender)
            check(f"{titel}: der Waechter liefert seinen eigenen "
                  f"Rueckgabewert", rc == 1, f"rc={rc}")
            check(f"{titel}: seine Ausgabe steht vollstaendig im Log",
                  BEFUNDTEXT.strip() in aus)
            check(f"{titel}: der Befund gilt als NICHT zugestellt",
                  ort.vermerke()["probe"]["zuletzt_gemeldet_am"] is None,
                  str(ort.vermerke().get("probe", {}).get("zuletzt_gemeldet_am")))

    # Eine werfende Sendefunktion wird ALS SENDEFEHLER behandelt, nicht als
    # Zusammenbruch des Meldeteils. Der Unterschied steht im Log und hat
    # Folgen: nur der Sendefehler fuehrt zu einem sauberen Vermerk, aus dem
    # beim naechsten Lauf eine NACHHOLUNG wird.
    with Wegwerf() as ort:
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        rc, aus, err = fuehre_aus(ort, Sender(wirft=True))
        check("Eine werfende Sendefunktion wird als Sendefehler protokolliert",
              "Der Versand ist gescheitert" in err, err.strip()[:90])
        check("und NICHT als Zusammenbruch des Meldeteils",
              "Der Meldeteil ist gescheitert" not in err, err.strip()[:90])
        check("Der Vermerk ist trotzdem sauber angelegt worden",
              ort.vermerke().get("probe", {}).get("laeufe") == 1,
              str(ort.vermerke()))
        heil = Sender()
        fuehre_aus(ort, heil, jetzt=tag(1))
        check("Daraus wird am naechsten Tag eine NACHHOLUNG",
              heil.anzahl == 1 and "Nachholung" in heil.letzte.splitlines()[0],
              heil.letzte.splitlines()[0] if heil.texte else "keine Nachricht")

    # Auch bei Rueckgabewert 0 und bei einem Absturz bleibt der Lauf heil.
    with Wegwerf() as ort:
        ort.stelle(rc=0, aus="alles gut\n")
        rc, aus, _ = fuehre_aus(ort, Sender(wirft=True))
        check("Auch ein Lauf ohne Befund bleibt unberuehrt", rc == 0 and "alles gut" in aus)

    # Und eine unlesbare Zustandsdatei bringt den Waechter ebenfalls nicht um.
    with Wegwerf() as ort:
        with open(ort.zustand, "w") as datei:
            datei.write("{kein gueltiges JSON")
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        s = Sender()
        rc, aus, err = fuehre_aus(ort, s)
        check("Eine unlesbare Zustandsdatei: der Waechter laeuft durch",
              rc == 1 and BEFUNDTEXT.strip() in aus)
        check("und der Befund wird gemeldet statt verschluckt", s.anzahl == 1)

    # Ein Meldeteil, der grundsaetzlich kaputt ist, darf ebenfalls nichts
    # kosten. Der Zustandspfad zeigt in einen Ordner, der eine DATEI ist.
    with Wegwerf() as ort:
        sackgasse = os.path.join(ort.skript, "unmoeglich", "zustand.json")
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        s = Sender()
        aus, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(aus), contextlib.redirect_stderr(err):
            rc = wm.lauf(ort.waechter, senden=s, zustand_pfad=sackgasse, jetzt=T0)
        check("Ein nicht schreibbarer Zustand: der Waechter laeuft durch",
              rc == 1 and BEFUNDTEXT.strip() in aus.getvalue(), f"rc={rc}")
        check("Die Nachricht ging trotzdem raus - gesendet wird VOR dem "
              "Vermerken", s.anzahl == 1, f"{s.anzahl}")
        check("Der Fehler steht im Log des Waechters",
              "[waechter_melden]" in err.getvalue(), err.getvalue().strip()[:70])


def test_reihenfolge_ausgabe_vor_meldung():
    print("\n--- 4b. Die Ausgabe ist im Log, bevor der Meldeteil beginnt ---")
    # Am ABLAUF geprueft: der Sender haelt fest, was zum Zeitpunkt des
    # Versands schon geschrieben war. Ein Wrapper, der erst meldet und dann
    # das Log schreibt, faellt hier auf - und genau der waere der, bei dem
    # ein Absturz im Meldeteil das Log kostet.
    with Wegwerf() as ort:
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        gesehen = {}

        aus = io.StringIO()

        def senden(text):
            gesehen["log"] = aus.getvalue()
            return True

        with contextlib.redirect_stdout(aus), contextlib.redirect_stderr(io.StringIO()):
            wm.lauf(ort.waechter, senden=senden, zustand_pfad=ort.zustand, jetzt=T0)
        check("Zum Zeitpunkt des Versands stand die Waechter-Ausgabe schon "
              "im Log", BEFUNDTEXT.strip() in gesehen.get("log", ""),
              repr(gesehen.get("log", ""))[:70])


# ===========================================================================
# 5. Die Wiederholungsdaempfung
# ===========================================================================
def test_daempfung():
    print("\n--- 5. Die Daempfung greift - und laesst Aenderungen durch ---")
    # FALLE 1: der Zustand entsteht ausschliesslich durch echte Laeufe.
    # FALLE 2: durchgehend Rueckgabewert 1 - die Null-Regel kann hier
    # nichts verschweigen, nur die Daempfung.
    with Wegwerf() as ort:
        s = Sender()
        ort.stelle(rc=1, aus=BEFUNDTEXT)

        fuehre_aus(ort, s, jetzt=tag(0))
        check("Tag 0, erster Befund: gemeldet", s.anzahl == 1, f"{s.anzahl}")
        check("und als 'neu' gekennzeichnet",
              s.letzte.splitlines()[0].endswith("- neu"))

        for i in range(1, 7):
            fuehre_aus(ort, s, jetzt=tag(i))
        check("Tag 1 bis 6, unveraendert: kein weiteres Wort",
              s.anzahl == 1, f"{s.anzahl}")

        fuehre_aus(ort, s, jetzt=tag(7))
        check("Tag 7: die woechentliche Erinnerung kommt", s.anzahl == 2,
              f"{s.anzahl}")
        check("Sie ist als Erinnerung gekennzeichnet",
              "Erinnerung" in s.letzte.splitlines()[0], s.letzte.splitlines()[0])
        check("Sie nennt die Standzeit",
              "seit 7 Tagen" in s.letzte, s.letzte.splitlines()[0])
        check("Sie nennt die Zahl der Laeufe",
              "8 Laeufe" in s.letzte, s.letzte.splitlines()[0])

        for i in range(8, 14):
            fuehre_aus(ort, s, jetzt=tag(i))
        check("Tag 8 bis 13: wieder still", s.anzahl == 2, f"{s.anzahl}")

        fuehre_aus(ort, s, jetzt=tag(14))
        check("Tag 14: die zweite Erinnerung", s.anzahl == 3, f"{s.anzahl}")

    # Der GEAENDERTE Befund geht sofort durch - auch am Tag danach.
    with Wegwerf() as ort:
        s = Sender()
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        fuehre_aus(ort, s, jetzt=tag(0))
        ort.stelle(rc=1, aus="BEFUND: 9 von 9 Kurven passen nicht zur "
                             "heutigen Konfiguration.\n")
        fuehre_aus(ort, s, jetzt=tag(1))
        check("Ein geaenderter Befund wird am naechsten Tag gemeldet",
              s.anzahl == 2, f"{s.anzahl}")
        check("und als geaendert gekennzeichnet",
              "geaendert" in s.letzte.splitlines()[0], s.letzte.splitlines()[0])
        check("Die neue Zahl steht drin", "9 von 9" in s.letzte)

        # Danach wird wieder gedaempft - und von vorn gezaehlt.
        fuehre_aus(ort, s, jetzt=tag(2))
        check("Der geaenderte Befund wird ab dem naechsten Tag gedaempft",
              s.anzahl == 2, f"{s.anzahl}")
        fuehre_aus(ort, s, jetzt=tag(7))
        check("Die Erinnerungsfrist laeuft ab der AENDERUNG, nicht ab dem "
              "ersten Befund: Tag 7 ist noch still", s.anzahl == 2, f"{s.anzahl}")
        fuehre_aus(ort, s, jetzt=tag(8))
        check("Tag 8 - sieben Tage nach der Aenderung - erinnert",
              s.anzahl == 3, f"{s.anzahl}")


def test_daempfung_ignoriert_laufzeiten():
    print("\n--- 5b. Wechselnde Laufzeiten heben die Daempfung nicht auf ---")
    # Alle vier Waechter drucken Laufzeiten und Zeitstempel. Ein
    # Fingerabdruck ueber die GANZE Ausgabe waere taeglich ein anderer, und
    # die Daempfung greife nie - der Fehler waere im Betrieb erst nach einer
    # Woche taeglicher Nachrichten aufgefallen.
    with Wegwerf() as ort:
        s = Sender()
        for i in range(6):
            ort.stelle(rc=1, aus=f"Start {tag(i)}\n{BEFUNDTEXT}"
                                 f"Gesamtlaufzeit: {41.2 + i:.1f}s\n")
            fuehre_aus(ort, s, jetzt=tag(i))
        check("Sechs Laeufe mit sechs verschiedenen Laufzeiten: EINE Nachricht",
              s.anzahl == 1, f"{s.anzahl}")


def test_versand_fehlgeschlagen():
    print("\n--- 5c. Was nicht ankam, gilt nicht als gemeldet ---")
    # Sonst verschluckt ein einzelner Netzausfall genau die Nachricht, fuer
    # die es diesen Wrapper gibt.
    with Wegwerf() as ort:
        kaputt, heil = Sender(scheitert=True), Sender()
        ort.stelle(rc=1, aus=BEFUNDTEXT)

        fuehre_aus(ort, kaputt, jetzt=tag(0))
        check("Tag 0: der Versand wurde versucht", kaputt.anzahl == 1)
        check("und ausdruecklich als nicht zugestellt vermerkt",
              ort.vermerke()["probe"]["zuletzt_gemeldet_am"] is None,
              str(ort.vermerke()["probe"]["zuletzt_gemeldet_am"]))

        fuehre_aus(ort, heil, jetzt=tag(1))
        check("Tag 1: derselbe, unveraenderte Befund wird NACHGEHOLT",
              heil.anzahl == 1, f"{heil.anzahl}")
        check("Die Nachricht sagt, dass sie nachgeholt wird",
              "Nachholung" in heil.letzte.splitlines()[0],
              heil.letzte.splitlines()[0])

        fuehre_aus(ort, heil, jetzt=tag(2))
        check("Tag 2: jetzt wird wieder gedaempft", heil.anzahl == 1,
              f"{heil.anzahl}")


# ===========================================================================
# 6. Die Nachricht
# ===========================================================================
def test_nachricht():
    print("\n--- 6. Was in der Meldung steht ---")
    with Wegwerf() as ort:
        ort.stelle(rc=1, aus="Zusammenfassung: 3x ABWEICHEND, 6x OK\n"
                             + BEFUNDTEXT
                             + "Neu erzeugen mit: python3 shared/ergebniskurven.py\n")
        w = ort.waechter._replace(marken=("Zusammenfassung:", "BEFUND"))
        s = Sender()
        aus, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(aus), contextlib.redirect_stderr(err):
            wm.lauf(w, senden=s, zustand_pfad=ort.zustand, jetzt=T0)
        # Ohne die Kopfzeile, die ihrerseits "[BEFUND]" enthaelt.
        uebernommen = [z for z in s.letzte.splitlines()[1:]
                       if "Zusammenfassung" in z or "BEFUND" in z]
        check("Genau zwei Zeilen aus der Ausgabe gehen mit",
              len(uebernommen) == 2, str(uebernommen))
        check("Die dritte Zeile bleibt im Log",
              "Neu erzeugen mit" not in s.letzte)
        check("Die ganze Nachricht passt auf ein Telefon (unter 500 Zeichen)",
              len(s.letzte) < 500, f"{len(s.letzte)} Zeichen")

    # Greift keine Marke, faellt die Nachricht auf die letzten Zeilen zurueck
    # UND sagt das. Eine stille Verschlechterung waere hier das Schlimmste:
    # die Nachricht saehe vollstaendig aus und waere es nicht.
    with Wegwerf() as ort:
        ort.stelle(rc=1, aus="Das Werkzeug hat seine Ausgabe umformuliert.\n"
                             "Letzte Zeile.\n")
        s = Sender()
        fuehre_aus(ort, s)
        check("Ohne Markentreffer wird das in der Nachricht gesagt",
              "keine bekannte Befundzeile erkannt" in s.letzte, s.letzte)
        check("und die letzten Ausgabezeilen gehen mit",
              "Letzte Zeile." in s.letzte)

    # Sehr lange Zeilen werden gekuerzt.
    with Wegwerf() as ort:
        ort.stelle(rc=1, aus="BEFUND: " + "x" * 5000 + "\n")
        s = Sender()
        fuehre_aus(ort, s)
        check("Eine ueberlange Zeile wird gekuerzt",
              len(s.letzte) < 500, f"{len(s.letzte)} Zeichen")
        check("und die Kuerzung ist sichtbar", "..." in s.letzte)

    # Ein Waechter, der gar nichts ausgibt, erzeugt trotzdem eine brauchbare
    # Nachricht - keine leere.
    with Wegwerf() as ort:
        ort.stelle(rc=1)
        s = Sender()
        fuehre_aus(ort, s)
        check("Ein stummer Waechter erzeugt trotzdem eine Nachricht",
              s.anzahl == 1 and "nichts ausgegeben" in s.letzte, s.letzte)


def test_doppelte_zeilen():
    print("\n--- 6b. Dieselbe Sache zweimal ist keine zweite Information ---")
    # determinismus.py nennt jeden Bot zweimal (Fortschrittszeile und
    # Tabelle). Ohne Entdopplung kosteten die beiden Zeilen ueber denselben
    # Bot den Platz der Zeile ueber den ZWEITEN betroffenen Bot.
    with Wegwerf() as ort:
        ort.stelle(rc=1, aus="  elliott_wave    NICHT DETERMINISTISCH   41.2s\n"
                             "  rsi2_crypto     NICHT DETERMINISTISCH   12.1s\n"
                             "elliott_wave     NICHT DETERMINISTISCH    3.1%\n"
                             "rsi2_crypto      NICHT DETERMINISTISCH    0.4%\n")
        w = ort.waechter._replace(marken=("NICHT DETERMINISTISCH",))
        s = Sender()
        aus, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(aus), contextlib.redirect_stderr(err):
            wm.lauf(w, senden=s, zustand_pfad=ort.zustand, jetzt=T0)
        check("Beide betroffenen Bots stehen in der Nachricht",
              "elliott_wave" in s.letzte and "rsi2_crypto" in s.letzte, s.letzte)


# ===========================================================================
# 7. Der Trockenlauf sendet nichts und vermerkt nichts
# ===========================================================================
def test_trockenlauf():
    print("\n--- 7. Der Trockenlauf ---")
    with Wegwerf() as ort:
        ort.stelle(rc=1, aus=BEFUNDTEXT)
        s = Sender()
        rc, aus, _ = fuehre_aus(ort, s, trockenlauf=True)
        check("Es wird nichts verschickt", s.anzahl == 0, f"{s.anzahl}")
        check("Es wird nichts vermerkt", ort.vermerke() == {})
        check("Der Rueckgabewert stimmt trotzdem", rc == 1)
        check("Die Nachricht wird gezeigt", "[BEFUND] Probe-Waechter" in aus)
        check("Und die Entscheidung wird benannt", "Entscheidung: MELDEN" in aus)

        rc, aus, _ = fuehre_aus(ort, s, trockenlauf=True)
        check("Ein zweiter Trockenlauf zeigt dasselbe - er hat nichts "
              "vermerkt", "Entscheidung: MELDEN" in aus)

        # Der Trockenlauf muss dieselbe Entscheidung zeigen wie der scharfe
        # Lauf - sonst prueft man mit ihm etwas anderes, als spaeter laeuft.
        ort.stelle(rc=0, aus="Alles in Ordnung.\n")
        rc, aus, _ = fuehre_aus(ort, s, trockenlauf=True)
        check("Bei Rueckgabewert 0 zeigt der Trockenlauf SCHWEIGEN",
              "Entscheidung: SCHWEIGEN" in aus, aus.strip()[-80:])
        check("und zeigt keine Nachricht", "[BEFUND]" not in aus)
        check("Auch im Trockenlauf wird nichts verschickt", s.anzahl == 0)


# ===========================================================================
# 8. Das Zeitlimit
# ===========================================================================
def test_zeitlimit():
    print("\n--- 8. Ein haengender Waechter (nur mit --zeitlimit) ---")
    with Wegwerf() as ort:
        with open(ort.skript, "w") as datei:
            datei.write("import time\ntime.sleep(30)\n")
        s = Sender()
        rc, _, _ = fuehre_aus(ort, s, zeitlimit=1.0)
        check("Er wird abgebrochen und als Absturz gemeldet",
              s.anzahl == 1 and s.letzte.startswith("[ABGESTUERZT]"),
              s.letzte.splitlines()[0] if s.texte else "keine Nachricht")
        check("Der Rueckgabewert ist 124, wie bei timeout(1)",
              rc == wm.RC_ZEITLIMIT, f"rc={rc}")
        check("Die Nachricht nennt das Zeitlimit als Grund",
              "Zeitlimit" in s.letzte)


# ===========================================================================
# 9. Die Entscheidungstabelle selbst
# ===========================================================================
def test_entscheidung():
    print("\n--- 9. Die vier Regeln, einzeln ---")
    vermerk = {"fingerabdruck": "aaa", "erstmals_am": "2026-09-01T03:50:00Z",
               "zuletzt_gemeldet_am": "2026-09-01T03:50:00Z", "laeufe": 1}
    j = datetime.datetime(2026, 9, 5, 3, 50)
    faelle = [
        ("0 schweigt immer", (wm.IN_ORDNUNG, "aaa", vermerk, j), (False, wm.STILL)),
        ("ohne Vermerk: neu", (wm.BEFUND, "aaa", None, j), (True, wm.NEU)),
        ("anderer Fingerabdruck: geaendert",
         (wm.BEFUND, "bbb", vermerk, j), (True, wm.GEAENDERT)),
        ("gleich und frisch gemeldet: still",
         (wm.BEFUND, "aaa", vermerk, j), (False, wm.GEDAEMPFT)),
        ("gleich und sieben Tage her: Erinnerung",
         (wm.BEFUND, "aaa", vermerk, datetime.datetime(2026, 9, 8, 3, 50)),
         (True, wm.ERINNERUNG)),
        ("nie zugestellt: Nachholung",
         (wm.BEFUND, "aaa", dict(vermerk, zuletzt_gemeldet_am=None), j),
         (True, wm.NACHHOLUNG)),
    ]
    for titel, args, erwartet in faelle:
        check(titel, wm.entscheidung(*args) == erwartet,
              f"{wm.entscheidung(*args)} statt {erwartet}")

    # Die Grenze ist "groesser oder gleich sieben Tage", nicht "acht".
    knapp = datetime.datetime(2026, 9, 8, 3, 49, 59)
    check("Sechs Tage, 23:59:59: noch still",
          wm.entscheidung(wm.BEFUND, "aaa", vermerk, knapp)[0] is False)
    check("Genau sieben Tage: Erinnerung",
          wm.entscheidung(wm.BEFUND, "aaa", vermerk,
                          datetime.datetime(2026, 9, 8, 3, 50))[0] is True)


# ===========================================================================
# 10. Die Waechter selbst bleiben unberuehrt
# ===========================================================================
def test_nichts_angefasst():
    print("\n--- 10. Der Wrapper fasst nichts an ---")
    quelle = open(os.path.join(_DIR, "waechter_melden.py")).read()
    check("Kein Waechter wird importiert - sie werden aufgerufen",
          "import ergebniskurven" not in quelle
          and "import determinismus" not in quelle
          and "import log_rotation" not in quelle
          and "import versuchsregister" not in quelle)
    check("Es gibt keinen zweiten Sendeweg - send_alert wird benutzt",
          "from notify import send_alert" in quelle
          and "api.telegram.org" not in quelle)
    # Schaerfer als eine Textsuche: welche Module importiert der Wrapper
    # ueberhaupt? Eine Textsuche wuerde schon an der Beschreibung eines
    # Waechters scheitern ("prueft die neun equity_simulation.py").
    erlaubt = {"argparse", "collections", "datetime", "hashlib", "json", "os",
               "subprocess", "sys", "notify"}
    importiert = set()
    for knoten in ast.walk(ast.parse(quelle)):
        if isinstance(knoten, ast.Import):
            importiert.update(n.name.split(".")[0] for n in knoten.names)
        elif isinstance(knoten, ast.ImportFrom) and knoten.module:
            importiert.add(knoten.module.split(".")[0])
    check("Der Wrapper importiert nur Standardbibliothek und notify",
          importiert <= erlaubt, f"zusaetzlich: {sorted(importiert - erlaubt)}")
    check("Kein live_params und kein forward_test - auch nicht im Text",
          "live_params" not in quelle and "forward_test" not in quelle)
    check("equity_simulation kommt nur in einer Beschreibung vor, nie als "
          "Import oder Pfad",
          "equity_simulation" not in importiert
          and quelle.count("equity_simulation") == 1)
    check("notify.py ist unveraendert geblieben",
          "def send_alert(text: str, parse_mode: str = \"Markdown\") -> bool:"
          in open(os.path.join(_DIR, "notify.py")).read())

    # Der Sendeweg wird unformatiert benutzt. Werkzeugausgabe enthaelt "_"
    # und "*"; Telegrams Legacy-Markdown kennt kein Escaping (Root-Cause-
    # Notiz in notify.py::send_report).
    check("Gesendet wird ohne parse_mode", "parse_mode=None" in quelle)

    # Jeder eingetragene Waechter zeigt auf eine Datei, die es gibt.
    for schluessel, w in wm.WAECHTER.items():
        pfad = os.path.join(BASE_DIR, w.befehl[0])
        check(f"{schluessel}: {w.befehl[0]} gibt es", os.path.exists(pfad))
        check(f"{schluessel}: hat einen Klartext-Namen ohne Dateiendung",
              w.klartext and ".py" not in w.klartext, w.klartext)
        check(f"{schluessel}: sein Log liegt unter logs/system/",
              w.log.startswith("logs/system/"), w.log)


def test_readme():
    print("\n--- 10b. Die Anleitung nennt jeden Waechter mit seiner Cron-Zeile ---")
    pfad = os.path.join(_DIR, "README_WAECHTER_MELDEN.md")
    check("README_WAECHTER_MELDEN.md ist da", os.path.exists(pfad))
    if not os.path.exists(pfad):
        return
    text = open(pfad).read()
    for schluessel in wm.WAECHTER:
        check(f"Die Cron-Zeile fuer '{schluessel}' steht im README",
              f"waechter_melden.py {schluessel}" in text)
    check("Das README sagt, dass die Crontab nicht geaendert wurde",
          "nicht eingetragen" in text)


# ===========================================================================
# 11. Mutationsproben - schlagen diese Tests ueberhaupt an?
# ===========================================================================
# Je Mutante steht dahinter, WELCHE Abschnitte fehlschlagen muessen - nicht
# mehr und nicht weniger. "Nicht mehr" ist der schaerfere Teil: er belegt,
# dass die Abschnitte unabhaengig voneinander messen und nicht einer fuer
# alle anderen mitbuergt (Falle 2).
MUTANTEN = [
    {
        "name": "null_meldet_auch",
        "titel": "die Null-Regel faellt weg (jeder Lauf meldet)",
        "alt": "    if klasse == IN_ORDNUNG:\n"
               "        return False, STILL\n",
        "neu": "    if klasse == IN_ORDNUNG and False:\n"
               "        return False, STILL\n",
        # Abschnitt 5 steht bewusst NICHT hier: die Daempfung arbeitet
        # ausschliesslich mit Rueckgabewert 1 und kann diesen Fehler gar
        # nicht sehen. Ein Test, der ihn ihr zuschriebe, behauptete eine
        # Wache, die es nicht gibt.
        "erwartet": {"2. Rueckgabewert 0", "2b. Aus Befund",
                     "7. Der Trockenlauf", "9. Die vier Regeln"},
    },
    {
        "name": "keine_daempfung",
        "titel": "die Daempfung faellt weg (taeglich dieselbe Meldung)",
        "alt": "    if (jetzt - zuletzt) >= datetime.timedelta(days=erinnerung_tage):\n"
               "        return True, ERINNERUNG\n"
               "    return False, GEDAEMPFT\n",
        "neu": "    if (jetzt - zuletzt) >= datetime.timedelta(days=erinnerung_tage):\n"
               "        return True, ERINNERUNG\n"
               "    return True, GEDAEMPFT\n",
        "erwartet": {"5. Die Daempfung", "5b. Wechselnde", "5c. Was nicht ankam",
                     "9. Die vier Regeln"},
    },
    {
        "name": "keine_erinnerung",
        "titel": "die woechentliche Erinnerung faellt weg (Befund verstummt)",
        "alt": "    if (jetzt - zuletzt) >= datetime.timedelta(days=erinnerung_tage):\n"
               "        return True, ERINNERUNG\n",
        "neu": "    if False:\n"
               "        return True, ERINNERUNG\n",
        "erwartet": {"5. Die Daempfung", "9. Die vier Regeln"},
    },
    {
        "name": "fehlversand_gilt_als_gemeldet",
        "titel": "ein fehlgeschlagener Versand gilt als zugestellt",
        "alt": "    if gesendet:\n        gemeldet_am = _zeit_schreiben(jetzt)\n",
        "neu": "    if True:\n        gemeldet_am = _zeit_schreiben(jetzt)\n",
        # Abschnitt 5 schlaegt mit an, und das ist die schaerfere Folge:
        # wird jeder Lauf als "gemeldet" vermerkt, rueckt die Frist der
        # woechentlichen Erinnerung taeglich vor und sie kommt NIE.
        "erwartet": {"4. Ein kaputter", "5. Die Daempfung",
                     "5c. Was nicht ankam"},
    },
    {
        "name": "absturz_wie_befund",
        "titel": "ein Absturz wird wie ein Befund gemeldet",
        "alt": '    kopf = ("[ABGESTUERZT]" if ergebnis.klasse == ABGESTUERZT else "[BEFUND]")\n',
        "neu": '    kopf = "[BEFUND]"\n',
        "erwartet": {"3. Ein Absturz", "8. Ein haengender"},
    },
    {
        "name": "traceback_ist_befund",
        "titel": "eine Traceback mit Rueckgabewert 1 gilt als Befund",
        "alt": "        return ABGESTUERZT if TRACEBACK_MARKE in (stderr or \"\") else BEFUND\n",
        "neu": "        return BEFUND\n",
        "erwartet": {"3. Ein Absturz"},
    },
    {
        "name": "meldung_vor_ausgabe",
        "titel": "erst melden, dann das Log schreiben",
        "alt": "    durchreichen(ergebnis)\n"
               "    try:\n"
               "        _melden(waechter, ergebnis, senden, zustand_pfad, jetzt,\n"
               "                erinnerung_tage, trockenlauf)\n",
        "neu": "    try:\n"
               "        _melden(waechter, ergebnis, senden, zustand_pfad, jetzt,\n"
               "                erinnerung_tage, trockenlauf)\n"
               "        durchreichen(ergebnis)\n",
        # Die Ausgabe kommt weiterhin - nur spaeter. Abschnitt 4 schlaegt mit
        # an, und zwar genau an der Stelle, um die es geht: dort scheitert
        # der Meldeteil, und mit ihm faellt jetzt das Log aus.
        "erwartet": {"4. Ein kaputter", "4b. Die Ausgabe"},
    },
    {
        "name": "sendefehler_reisst_mit",
        "titel": "ein Sendefehler wird weitergereicht",
        "alt": "    try:\n"
               "        return bool(senden(text))\n"
               "    except Exception as fehler:                              "
               "# noqa: BLE001\n"
               "        _hinweis(f\"Der Versand ist gescheitert "
               "({type(fehler).__name__}: \"\n"
               "                 f\"{fehler}). Die Meldung gilt als NICHT "
               "zugestellt und wird \"\n"
               "                 f\"beim naechsten Lauf erneut versucht.\")\n"
               "        return False\n",
        "neu": "    return bool(senden(text))\n",
        # Der aeussere Schutz in lauf() faengt die Ausnahme weiterhin ab -
        # der Waechter stirbt also auch ohne diese Stelle nicht. Was verloren
        # geht, ist die UNTERSCHEIDUNG: ein Netzfehler saehe im Log aus wie
        # ein zusammengebrochener Meldeteil, und der Befund bekaeme keinen
        # Vermerk, aus dem am naechsten Tag eine Nachholung wuerde.
        "erwartet": {"4. Ein kaputter"},
    },
    {
        "name": "fingerabdruck_ueber_alles",
        "titel": "der Fingerabdruck laeuft ueber die ganze Ausgabe",
        "alt": '    roh = "|".join([ergebnis.klasse, str(ergebnis.rueckgabewert)] + list(zeilen))\n',
        "neu": '    roh = "|".join([ergebnis.klasse, str(ergebnis.rueckgabewert),\n'
               '                    ergebnis.stdout, ergebnis.stderr])\n',
        "erwartet": {"5b. Wechselnde"},
    },
]


def test_mutationsproben():
    print("\n--- 11. Mutationsproben ---")
    quelle = open(os.path.join(_DIR, "waechter_melden.py")).read()
    for mutant in MUTANTEN:
        if quelle.count(mutant["alt"]) != 1:
            check(f"Mutante '{mutant['name']}': die Stelle ist eindeutig",
                  False, f"{quelle.count(mutant['alt'])}x gefunden")
            continue
        angeschlagen = _lauf_gegen_mutante(
            quelle.replace(mutant["alt"], mutant["neu"]), mutant["name"])
        fehlend = {e for e in mutant["erwartet"]
                   if not any(a.startswith(e) for a in angeschlagen)}
        ueberzaehlig = {a for a in angeschlagen
                        if not any(a.startswith(e) for e in mutant["erwartet"])}
        check(f"Mutante '{mutant['titel']}': genau die erwarteten Abschnitte "
              f"schlagen an",
              not fehlend and not ueberzaehlig,
              (f"fehlt: {sorted(fehlend) or '-'}; "
               f"zuviel: {sorted(ueberzaehlig) or '-'}"))


def _lauf_gegen_mutante(quelle, name):
    """Diese Testdatei gegen eine mutierte Fassung des Wrappers laufen lassen.

    In einem eigenen Prozess mit eigenem Modulordner - das echte
    notifications/ bleibt unberuehrt.
    """
    ordner = tempfile.mkdtemp(prefix=f"mutante_{name}_")
    try:
        with open(os.path.join(ordner, "waechter_melden.py"), "w") as datei:
            datei.write(quelle)
        shutil.copy(os.path.join(_DIR, "notify.py"), ordner)
        shutil.copy(os.path.join(_DIR, "telegram_config.py"), ordner)
        shutil.copy(os.path.join(_DIR, "README_WAECHTER_MELDEN.md"), ordner)
        shutil.copy(os.path.abspath(__file__),
                    os.path.join(ordner, "test_waechter_melden.py"))
        umgebung = dict(os.environ, WAECHTER_MUTANTE="1")
        lauf = subprocess.run(
            [sys.executable, os.path.join(ordner, "test_waechter_melden.py")],
            capture_output=True, text=True, env=umgebung, timeout=600)
        if "--- " not in lauf.stdout:
            # Die Mutante ist nicht gelaufen (z.B. Syntaxfehler). Das als
            # "nichts schlaegt an" durchgehen zu lassen waere genau die
            # Selbstbestaetigung, gegen die diese Proben gebaut sind.
            raise RuntimeError(
                f"Mutante '{name}' ist nicht gelaufen: "
                f"{(lauf.stderr or lauf.stdout).strip()[-300:]}")
        return _abschnitte_mit_fehler(lauf.stdout)
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


def _abschnitte_mit_fehler(ausgabe):
    """Welche der nummerierten Abschnitte haben mindestens einen Fehler?"""
    abschnitt, getroffen = "", set()
    for zeile in ausgabe.splitlines():
        if zeile.startswith("--- "):
            abschnitt = zeile[4:].split(" ---")[0].strip()
        elif zeile.strip().startswith("[FEHLER]") and abschnitt:
            getroffen.add(abschnitt)
    return getroffen


# ===========================================================================
def main():
    print("=" * 78)
    print("Selbsttests des Waechter-Wrappers")
    print("=" * 78)
    tests = [test_befund_meldet, test_null_schweigt, test_wieder_in_ordnung,
             test_absturz, test_sendeweg_kaputt,
             test_reihenfolge_ausgabe_vor_meldung, test_daempfung,
             test_daempfung_ignoriert_laufzeiten, test_versand_fehlgeschlagen,
             test_nachricht, test_doppelte_zeilen, test_trockenlauf,
             test_zeitlimit, test_entscheidung, test_nichts_angefasst,
             test_readme]
    if os.environ.get("WAECHTER_MUTANTE"):
        # Die Mutante laeuft in einem Wegwerf-Ordner: die beiden Abschnitte,
        # die die QUELLE und die Registereintraege pruefen, koennen dort
        # nichts messen (die Waechter-Dateien liegen woanders). Gemessen
        # wird in der Mutante ausschliesslich das Verhalten - und die
        # Mutationsproben starten sich nicht selbst noch einmal.
        tests = [t for t in tests
                 if t not in (test_nichts_angefasst, test_readme)]
    else:
        tests.append(test_mutationsproben)

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
