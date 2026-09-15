"""
Waechter melden - ein Wrapper, der aus einem Rueckgabewert eine Nachricht macht
==============================================================================
Am 14.09.2026 wurden fuenf Werkzeuge in die Crontab eingetragen. Vier davon
sind Waechter: sie pruefen etwas und geben bei Befund Rueckgabewert 1. Das
fuenfte (die Log-Rotation) meldet auf demselben Weg einen echten Fehlschlag.

Alle fuenf schreiben ihre Ausgabe in eine Logdatei unter `logs/system/`.

UND DORTHIN SIEHT NIEMAND. Ein Waechter, dessen Befund in einer Datei landet,
die nie jemand oeffnet, ist ein Waechter, den es nicht gibt. Genau deshalb
gibt es diese Datei: sie fuehrt das Werkzeug aus, laesst dessen Ausgabe
unveraendert ins Log durch und schickt bei Befund EINE kurze Telegram-
Nachricht.

------------------------------------------------------------------------------
DIE ENTWURFSENTSCHEIDUNG: WANN WIRD GEMELDET, WANN GESCHWIEGEN
------------------------------------------------------------------------------
Drei Ausgaenge, nicht zwei. Das ist der Kern.

  RUECKGABEWERT 0  -> IN ORDNUNG   -> es wird GESCHWIEGEN.
      Ausnahmslos, auch beim allerersten Lauf. Ein taegliches "alles gut" ist
      nach einer Woche ungelesen, und ein Kanal, in dem 364 belanglose
      Nachrichten stehen, verbirgt die eine, auf die es ankommt. Der Kanal
      traegt nur, was Handeln verlangt.

  RUECKGABEWERT 1  -> BEFUND       -> es wird gemeldet (mit Daempfung, s.u.).
      Das Werkzeug hat gearbeitet und etwas gefunden.

  ALLES ANDERE     -> ABGESTUERZT  -> es wird gemeldet, UNTERSCHEIDBAR.
      Rueckgabewert 2, 127, ein Signal (negativer Wert), ein nicht
      startbares Programm, ein ueberschrittenes Zeitlimit - und der
      Sonderfall Rueckgabewert 1 MIT einer Traceback in der Fehlerausgabe
      (Begruendung bei TRACEBACK_MARKE). Das ist der
      gefaehrlichste der drei Faelle und deshalb der, der eine eigene
      Kennzeichnung bekommt: ein abgestuerzter Waechter meldet nie wieder
      etwas, und Schweigen sieht von aussen genau aus wie "alles in
      Ordnung". Ein Befund und ein Absturz duerfen deshalb nie dieselbe
      Nachricht erzeugen - beim Befund weiss man etwas, beim Absturz weiss
      man NICHTS.

------------------------------------------------------------------------------
DIE WIEDERHOLUNGSDAEMPFUNG - UND WARUM GENAU DIESE
------------------------------------------------------------------------------
Ein Waechter, der dieselbe Abweichung dreissig Tage lang taeglich meldet,
wird stummgeschaltet - und damit ist auch die einunddreissigste, neue
Meldung weg. Die Daempfung ist also kein Komfort, sie schuetzt den Kanal.

Vier Regeln, in dieser Reihenfolge geprueft:

  1. NEU            - zu diesem Waechter steht nichts vermerkt  -> MELDEN.
  2. GEAENDERT      - der Befund liest sich anders als zuletzt  -> MELDEN.
  3. NACHHOLUNG     - die letzte Meldung ging nicht raus        -> MELDEN.
  4. ERINNERUNG     - unveraendert, aber die letzte erfolgreiche
                      Meldung ist >= ERINNERUNG_TAGE her        -> MELDEN.
  sonst                                                         -> SCHWEIGEN.

Begruendung der vier, einzeln:

  Zu 1: Der erste Befund ist die eigentliche Nachricht. Wuerde er gedaempft,
        haette die Daempfung den Zweck des ganzen Wrappers aufgehoben.

  Zu 2: Der INHALT des Befundes ist die Information, nicht sein Vorhandensein.
        "3 von 9 Kurven passen nicht" und "9 von 9 Kurven passen nicht" sind
        zwei verschiedene Nachrichten; eine Daempfung, die nur auf "es gibt
        einen Befund" schaut, verschluckt die Eskalation. Verglichen wird
        deshalb GENAU DAS, WAS GESENDET WUERDE (siehe `fingerabdruck`) - eine
        Regel, die man in einem Satz erklaeren kann und die nicht davon
        abhaengt, wie ein einzelnes Werkzeug seine Laufzeit formatiert.

  Zu 3: Schlaegt der Versand fehl (Netz weg, Token falsch), darf der Befund
        NICHT als gemeldet gelten - sonst verschluckt ein Netzausfall genau
        die Nachricht, fuer die es diesen Wrapper gibt. Vermerkt wird erst,
        wenn die Wirkung eingetreten ist. Das ist dieselbe Lehre, die
        `notifications/schliess_benachrichtigung.py` aus dem Fehler von
        `monitor.py` gezogen hat (dort ausfuehrlich dokumentiert).

  Zu 4: Die Erinnerung ist der Preis der Daempfung. Ohne sie waere ein
        bestehender Befund ab Tag zwei nicht mehr von "alles in Ordnung" zu
        unterscheiden - und damit waere genau der Zustand wiederhergestellt,
        gegen den dieser Wrapper geschrieben ist.

  ERINNERUNG_TAGE = 7. Nicht 1 (das ist die taegliche Meldung, also keine
  Daempfung), nicht 30 (dann kann ein Befund einen ganzen Monat lang
  unerwaehnt bleiben). Sieben Tage ist der groesste Abstand, bei dem ein
  bestehender Befund in jeder Woche mindestens einmal vorkommt, und zugleich
  klein genug, dass er nie mehr als rund vier Nachrichten je Waechter und
  Monat erzeugt. Die Erinnerung traegt Standzeit und Anzahl der Laeufe mit
  ("besteht seit 8 Tagen, 8 Laeufe") - damit ist der Verlauf in der
  Nachricht selbst sichtbar und nicht nur die Momentaufnahme.

  Ein Absturz wird nach denselben vier Regeln gedaempft. Der Ausgang ist
  Teil des Fingerabdrucks: der Uebergang Befund -> Absturz (und zurueck)
  faellt deshalb immer unter Regel 2 und wird gemeldet.

WAS BEWUSST NICHT GEMELDET WIRD: die Aufloesung. Faellt ein Waechter von
Befund zurueck auf 0, wird der Vermerk stillschweigend geloescht. Das folgt
aus der Regel "0 heisst schweigen" und kostet eine Bestaetigung, dass etwas
behoben ist. Vermerkt als offener Punkt in der Uebergabe - der Kanal bleibt
dafuer frei von allem, was kein Handeln verlangt.

------------------------------------------------------------------------------
DIE HARTE BEDINGUNG: DER WRAPPER BRINGT DEN WAECHTER NIE ZUM SCHEITERN
------------------------------------------------------------------------------
Der Rueckgabewert dieses Programms ist IMMER der des Waechters, und dessen
Ausgabe geht unveraendert nach stdout/stderr - bevor auch nur der Versuch
einer Meldung unternommen wird. Erst danach folgt der Meldeteil, und der
steht vollstaendig in einem `try`. Ob Telegram erreichbar ist, ob der Token
stimmt, ob die Zustandsdatei lesbar ist: nichts davon erreicht den
Rueckgabewert und nichts davon verhindert, dass das Log geschrieben wird.
Ein Sendefehler wird protokolliert, nicht weitergereicht.

Die einzige Ausnahme ist ein ausdruecklich gesetztes `--zeitlimit`: dann
wird ein haengender Waechter abgebrochen und als Absturz gemeldet (mit
Rueckgabewert 124, wie bei `timeout(1)`). Ohne die Option - und so lauten
die vorgeschlagenen Crontab-Zeilen - gibt es kein Zeitlimit und damit kein
Verhalten, das der Waechter heute nicht schon haette.

------------------------------------------------------------------------------
WAS DIESER WRAPPER NICHT TUT
------------------------------------------------------------------------------
Er fasst keinen der Waechter an, er importiert keinen von ihnen, er liest
keine Bot-Datenbank und er baut keinen zweiten Sendeweg: verschickt wird
ueber `notifications/notify.py::send_alert()` - dieselbe Funktion wie
ueberall sonst, unveraendert.

Nutzung:

    python3 notifications/waechter_melden.py ergebniskurven
    python3 notifications/waechter_melden.py --status
    python3 notifications/waechter_melden.py determinismus --trockenlauf

Selbsttests:  python3 notifications/test_waechter_melden.py
Anleitung:    notifications/README_WAECHTER_MELDEN.md
"""

import argparse
import collections
import datetime
import hashlib
import json
import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)

# ---------------------------------------------------------------------------
# Die drei Ausgaenge
# ---------------------------------------------------------------------------
IN_ORDNUNG = "in_ordnung"
BEFUND = "befund"
ABGESTUERZT = "abgestuerzt"

# Die Anlaesse einer Meldung (siehe Kopf, "Wiederholungsdaempfung").
NEU = "neu"
GEAENDERT = "geaendert"
NACHHOLUNG = "nachholung"
ERINNERUNG = "erinnerung"
GEDAEMPFT = "gedaempft"
STILL = "still"                      # Rueckgabewert 0 - der Normalfall

STANDARD_ERINNERUNG_TAGE = 7

# Rueckgabewert bei ueberschrittenem `--zeitlimit`; dieselbe Zahl wie bei
# timeout(1), damit sie in einem Log wiedererkennbar ist.
RC_ZEITLIMIT = 124

# Hoechstens so viele Zeilen aus der Ausgabe in die Nachricht, und je Zeile
# hoechstens so viele Zeichen. Eine Telegram-Nachricht, die man scrollen
# muss, wird nicht gelesen; die volle Ausgabe steht im Log.
KERNZEILEN = 2
ZEILENLAENGE = 180

ZUSTAND_DATEI = os.path.join(_DIR, "waechter_zustand.json")
ZUSTAND_VERSION = 1

ZEITFORMAT = "%Y-%m-%dT%H:%M:%SZ"


def jetzt_utc():
    """UTC ohne Zeitzoneninfo - wie die Zeitstempel in allen drei
    Nachverfolgungen dieses Projekts. Nicht utcnow(), das ist ab
    Python 3.12 verworfen; der Rechner des Nutzers laeuft auf 3.9."""
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


# ---------------------------------------------------------------------------
# Die Werkzeuge, die dieser Wrapper kennt
# ---------------------------------------------------------------------------
# `marken`: Zeichenketten, an denen die Befundzeile in der Ausgabe erkannt
# wird. Sie stehen HIER und nicht im jeweiligen Werkzeug - die Waechter
# werden aufgerufen, nicht geaendert. Greift keine Marke (weil ein Werkzeug
# seine Ausgabe umformuliert hat), fallen die letzten Ausgabezeilen ein und
# die Nachricht sagt das ausdruecklich; die Verschlechterung ist sichtbar
# und nicht still.
Waechter = collections.namedtuple(
    "Waechter", "schluessel klartext befehl log marken zweck")

WAECHTER = collections.OrderedDict((w.schluessel, w) for w in [
    Waechter(
        schluessel="log_rotation",
        klartext="Log-Rotation",
        befehl=("system/log_rotation.py",),
        log="logs/system/log_rotation.log",
        marken=("Log-Rotation:", "FEHLGESCHLAGEN"),
        zweck="schneidet die Logdateien unter logs/ mit",
    ),
    Waechter(
        schluessel="ergebniskurven",
        klartext="Ergebniskurven",
        befehl=("shared/ergebniskurven.py", "--nur-abweichung"),
        log="logs/system/ergebniskurven.log",
        marken=("BEFUND", "Zusammenfassung:"),
        zweck="vergleicht die abgelegten Kurven mit der heutigen Konfiguration",
    ),
    Waechter(
        schluessel="determinismus",
        klartext="Determinismus der Backtests",
        befehl=("shared/determinismus.py", "--schnell"),
        log="logs/system/determinismus.log",
        marken=("NICHT DETERMINISTISCH", "NUR REIHENFOLGE", "UNKLAR",
                "FEHLER -"),
        zweck="prueft, ob eine andere Symbolreihenfolge dasselbe Ergebnis liefert",
    ),
    Waechter(
        schluessel="versuchsregister",
        klartext="Versuchsregister",
        befehl=("research/versuchsregister/versuchsregister.py", "--pruefen"),
        log="logs/system/versuchsregister.log",
        marken=("ABWEICHUNG", "RASTER", "ZEILEN GEAENDERT",
                "ERGEBNISDATEI"),
        zweck="haelt die Zahl der gefahrenen Versuche gegen den festgehaltenen Stand",
    ),
    Waechter(
        schluessel="kapitalsimulation",
        klartext="Kapitalsimulation der neun Bots",
        befehl=("research/tb27_kapitalsimulation/vergleich.py", "--pruefen"),
        log="logs/system/kapitalsimulation.log",
        marken=("ABWEICHUNG", "NEUE FUNKTION", "FUNKTION FEHLT", "GRUPPEN ANDERS"),
        zweck="prueft die neun equity_simulation.py auf stille Divergenz",
    ),
])


# ---------------------------------------------------------------------------
# Den Waechter ausfuehren
# ---------------------------------------------------------------------------
Ergebnis = collections.namedtuple(
    "Ergebnis", "rueckgabewert klasse stdout stderr grund")


# Ein unbehandelter Python-Fehler beendet den Prozess mit Rueckgabewert 1 -
# demselben Wert, mit dem ein Waechter einen BEFUND meldet. Ohne weiteres
# Merkmal waere ein abgestuerzter Waechter also nicht von einem arbeitenden
# zu unterscheiden, und das ist genau der Fall, den dieser Wrapper
# unterscheidbar melden soll.
#
# Das Merkmal ist die Fehlerausgabe: alle fuenf Werkzeuge fangen die
# Traceback eines von IHNEN gestarteten Unterprozesses ab und drucken sie in
# ihre NORMALE Ausgabe (determinismus.py:174, ergebniskurven.py:191). Steht
# eine Traceback in der FEHLERausgabe, ist also das Werkzeug selbst
# gestorben. Die Probe ist bewusst eng - und ihr Irrtum faellt in die
# harmlose Richtung: falsch eingeordnet wird eine Meldung, verschluckt wird
# keine.
TRACEBACK_MARKE = "Traceback (most recent call last):"


def _klasse_fuer(rueckgabewert, stderr=""):
    if rueckgabewert == 0:
        return IN_ORDNUNG
    if rueckgabewert == 1:
        return ABGESTUERZT if TRACEBACK_MARKE in (stderr or "") else BEFUND
    return ABGESTUERZT


def ausfuehren(waechter, zeitlimit=None, basis=None):
    """Startet den Waechter und faengt JEDEN Startfehler ab.

    Wirft nie. Was hier schiefgeht, wird zu einem Ergebnis der Klasse
    ABGESTUERZT - denn genau das ist es: das Werkzeug hat nicht gearbeitet.
    """
    basis = basis or BASE_DIR
    argv = [sys.executable] + [str(teil) for teil in waechter.befehl]
    try:
        lauf = subprocess.run(argv, cwd=basis, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=zeitlimit)
    except subprocess.TimeoutExpired as fehler:
        return Ergebnis(RC_ZEITLIMIT, ABGESTUERZT,
                        _text(fehler.stdout), _text(fehler.stderr),
                        f"Zeitlimit von {zeitlimit:.0f}s ueberschritten - "
                        f"der Lauf wurde abgebrochen.")
    except Exception as fehler:                              # noqa: BLE001
        return Ergebnis(127, ABGESTUERZT, "",
                        f"{type(fehler).__name__}: {fehler}",
                        "Das Werkzeug liess sich nicht starten.")

    rc = lauf.returncode
    stdout, stderr = _text(lauf.stdout), _text(lauf.stderr)
    klasse = _klasse_fuer(rc, stderr)
    grund = ""
    if klasse == ABGESTUERZT:
        if rc < 0:
            grund = f"Vom Signal {-rc} beendet (Rueckgabewert {rc})."
        elif rc == 1:
            grund = ("Rueckgabewert 1, aber mit einer Traceback in der "
                     "Fehlerausgabe.")
        else:
            grund = f"Rueckgabewert {rc} - weder 0 (in Ordnung) noch 1 (Befund)."
    return Ergebnis(rc, klasse, stdout, stderr, grund)


def _text(roh):
    if roh is None:
        return ""
    if isinstance(roh, bytes):
        return roh.decode("utf-8", errors="replace")
    return roh


def durchreichen(ergebnis):
    """Die Ausgabe des Waechters unveraendert weitergeben.

    Steht im Ablauf VOR dem Meldeteil: das Log ist geschrieben, bevor
    irgendetwas passieren kann, das mit Telegram zu tun hat.
    """
    if ergebnis.stdout:
        sys.stdout.write(ergebnis.stdout)
    if ergebnis.stderr:
        sys.stderr.write(ergebnis.stderr)
    sys.stdout.flush()
    sys.stderr.flush()


# ---------------------------------------------------------------------------
# Aus der Ausgabe die ein bis zwei Zeilen holen, die in die Nachricht gehoeren
# ---------------------------------------------------------------------------
def kernzeilen(ergebnis, waechter, hoechstens=KERNZEILEN):
    """(Zeilen, marke_getroffen).

    Bei einem BEFUND werden die Marken des Waechters gesucht - sie stehen in
    der Regel weit oben, waehrend darunter noch Erklaerungstext folgt.
    Bei einem ABSTURZ zaehlen die LETZTEN Zeilen von stderr: die letzte
    Zeile eines Tracebacks ist die Ausnahme, und die ist die Nachricht.
    """
    if ergebnis.klasse == ABGESTUERZT:
        zeilen = _zeilen(ergebnis.stderr) or _zeilen(ergebnis.stdout)
        return [_kuerzen(z) for z in zeilen[-hoechstens:]], False

    zeilen = _zeilen(ergebnis.stdout) or _zeilen(ergebnis.stderr)
    treffer = _ohne_wiederholung(
        [z for z in zeilen if any(m in z for m in waechter.marken)])
    if treffer:
        return [_kuerzen(z) for z in treffer[:hoechstens]], True
    return [_kuerzen(z) for z in zeilen[-hoechstens:]], False


def _ohne_wiederholung(zeilen):
    """Je Erstwort hoechstens eine Zeile.

    `determinismus.py` nennt jeden Bot zweimal - einmal in der Fortschritts-
    zeile, einmal in der Tabelle darunter. Zwei Zeilen ueber denselben Bot
    sind keine zweite Information, und in einer Nachricht mit Platz fuer zwei
    Zeilen kosten sie die eine, die noch gefehlt haette.
    """
    gesehen, behalten = set(), []
    for zeile in zeilen:
        erstes = zeile.split()[0] if zeile.split() else zeile
        if erstes in gesehen:
            continue
        gesehen.add(erstes)
        behalten.append(zeile)
    return behalten


def _zeilen(text):
    return [z.strip() for z in (text or "").splitlines() if z.strip()]


def _kuerzen(zeile):
    return zeile if len(zeile) <= ZEILENLAENGE else zeile[:ZEILENLAENGE - 3] + "..."


def fingerabdruck(ergebnis, zeilen):
    """Der Daempfungsschluessel: genau das, was gesendet wuerde.

    Bewusst NICHT die ganze Ausgabe - darin stehen Laufzeiten ("41.2s") und
    Zeitstempel, die sich bei jedem Lauf aendern. Ein Fingerabdruck darueber
    waere jeden Tag ein anderer, und die Daempfung griffe nie.
    """
    roh = "|".join([ergebnis.klasse, str(ergebnis.rueckgabewert)] + list(zeilen))
    return hashlib.sha256(roh.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Der Zustand: was wurde wann zuletzt gemeldet
# ---------------------------------------------------------------------------
def zustand_lesen(pfad):
    """Fehlt oder bricht die Datei, wird mit leerem Zustand weitergemacht.

    Das faellt in die sichere Richtung: ein verlorener Zustand fuehrt zu
    einer Meldung ZU VIEL (der bestehende Befund gilt wieder als neu), nie
    zu einer verschluckten.
    """
    try:
        with open(pfad) as datei:
            daten = json.load(datei)
        if isinstance(daten, dict) and isinstance(daten.get("waechter"), dict):
            return daten["waechter"]
    except FileNotFoundError:
        pass
    except Exception as fehler:                              # noqa: BLE001
        _hinweis(f"Zustandsdatei {pfad} nicht lesbar ({fehler}) - es wird mit "
                 f"leerem Zustand weitergemacht. Ein bestehender Befund wird "
                 f"deshalb einmal erneut gemeldet.")
    return {}


def zustand_schreiben(pfad, vermerke):
    """Erst in eine Nebendatei, dann umbenennen - wie warteauftraege.json."""
    ordner = os.path.dirname(pfad)
    if ordner:
        os.makedirs(ordner, exist_ok=True)
    neu = pfad + ".neu"
    with open(neu, "w") as datei:
        json.dump({"version": ZUSTAND_VERSION, "waechter": vermerke},
                  datei, indent=2, sort_keys=True)
    os.replace(neu, pfad)


# ---------------------------------------------------------------------------
# Die Entscheidung. Eine reine Funktion - sie liest nichts und sendet nichts.
# ---------------------------------------------------------------------------
def entscheidung(klasse, abdruck, vermerk, jetzt,
                 erinnerung_tage=STANDARD_ERINNERUNG_TAGE):
    """(melden: bool, anlass: str) - die vier Regeln aus dem Kopf."""
    if klasse == IN_ORDNUNG:
        return False, STILL
    if not vermerk:
        return True, NEU
    if vermerk.get("fingerabdruck") != abdruck:
        return True, GEAENDERT
    zuletzt = _zeit_lesen(vermerk.get("zuletzt_gemeldet_am"))
    if zuletzt is None:
        return True, NACHHOLUNG
    if (jetzt - zuletzt) >= datetime.timedelta(days=erinnerung_tage):
        return True, ERINNERUNG
    return False, GEDAEMPFT


def _zeit_lesen(text):
    try:
        return datetime.datetime.strptime(text, ZEITFORMAT)
    except (TypeError, ValueError):
        return None


def _zeit_schreiben(zeit):
    return zeit.strftime(ZEITFORMAT)


# ---------------------------------------------------------------------------
# Die Nachricht
# ---------------------------------------------------------------------------
def nachricht(waechter, ergebnis, zeilen, marke_getroffen, anlass, vermerk,
              jetzt):
    """Kurz genug fuers Telefon, vollstaendig genug zum Handeln.

    Drei Teile: WER, WAS, und der Befehl zum NACHSEHEN. Die volle Ausgabe
    bleibt im Log; hierher kommt sie ausdruecklich nicht.
    """
    kopf = ("[ABGESTUERZT]" if ergebnis.klasse == ABGESTUERZT else "[BEFUND]")
    teile = [f"{kopf} {waechter.klartext} - {_anlass_text(anlass, vermerk, jetzt)}"]

    if ergebnis.klasse == ABGESTUERZT:
        teile.append(ergebnis.grund + " Das Werkzeug selbst ist gescheitert, "
                                      "es liegt KEIN Befund vor.")
    if zeilen:
        if not marke_getroffen and ergebnis.klasse == BEFUND:
            teile.append("(keine bekannte Befundzeile erkannt - "
                         "letzte Ausgabezeilen:)")
        teile.extend(zeilen)
    else:
        teile.append("Das Werkzeug hat nichts ausgegeben.")

    teile.append(f"Nachsehen: tail -n 60 ~/trading-bot/{waechter.log}")
    return "\n".join(teile)


def _anlass_text(anlass, vermerk, jetzt):
    if anlass == NEU:
        return "neu"
    if anlass == GEAENDERT:
        return "geaendert gegenueber der letzten Meldung"
    if anlass == NACHHOLUNG:
        return "Nachholung, die letzte Meldung ging nicht raus"
    seit = _zeit_lesen((vermerk or {}).get("erstmals_am"))
    tage = (jetzt - seit).days if seit else 0
    laeufe = (vermerk or {}).get("laeufe", 0) + 1
    return (f"unveraendert seit {tage} Tag{'en' if tage != 1 else ''}, "
            f"{laeufe} Laeufe - Erinnerung")


# ---------------------------------------------------------------------------
# Der Sendeweg. EIN Parameter, damit die Selbsttests keinen echten Aufruf
# brauchen - und damit hier keine zweite Telegram-Anbindung entsteht.
# ---------------------------------------------------------------------------
def _standard_senden(text):
    # Erst hier importiert, damit beim Modulimport keine Zugangsdaten
    # gelesen werden (dieselbe Begruendung wie in
    # schliess_benachrichtigung.py::_standard_senden).
    from notify import send_alert
    # parse_mode=None: der Text enthaelt fremde Werkzeugausgabe mit "_",
    # "*" und Pfaden. Telegrams Legacy-Markdown kennt kein Escaping - siehe
    # die Root-Cause-Notiz in notify.py::send_report. Unformatiert ist hier
    # die einzige Fassung, die bei JEDER Ausgabe richtig ankommt.
    return send_alert(text, parse_mode=None)


def _hinweis(text):
    """Geht ins Log des Waechters, nicht nach Telegram."""
    sys.stderr.write(f"[waechter_melden] {text}\n")
    sys.stderr.flush()


# ---------------------------------------------------------------------------
# Ein vollstaendiger Lauf
# ---------------------------------------------------------------------------
def lauf(waechter, senden=None, zustand_pfad=None, jetzt=None,
         erinnerung_tage=STANDARD_ERINNERUNG_TAGE, zeitlimit=None,
         trockenlauf=False, basis=None):
    """Fuehrt den Waechter aus, reicht seine Ausgabe durch, meldet bei Befund.

    Gibt IMMER den Rueckgabewert des Waechters zurueck. Alles ab
    `durchreichen()` steht in einem `try` - der Meldeteil kann den Waechter
    nicht zum Scheitern bringen.
    """
    ergebnis = ausfuehren(waechter, zeitlimit=zeitlimit, basis=basis)
    durchreichen(ergebnis)
    try:
        _melden(waechter, ergebnis, senden, zustand_pfad, jetzt,
                erinnerung_tage, trockenlauf)
    except Exception as fehler:                              # noqa: BLE001
        _hinweis(f"Der Meldeteil ist gescheitert ({type(fehler).__name__}: "
                 f"{fehler}). Der Waechter selbst ist davon unberuehrt, sein "
                 f"Rueckgabewert bleibt {ergebnis.rueckgabewert}.")
    return ergebnis.rueckgabewert


def _melden(waechter, ergebnis, senden, zustand_pfad, jetzt, erinnerung_tage,
            trockenlauf):
    """Der Meldeteil. Gibt den Anlass zurueck - die Selbsttests lesen ihn."""
    jetzt = jetzt or jetzt_utc()
    pfad = zustand_pfad or ZUSTAND_DATEI
    vermerke = zustand_lesen(pfad)
    vorher = vermerke.get(waechter.schluessel)

    zeilen, marke = kernzeilen(ergebnis, waechter)
    abdruck = fingerabdruck(ergebnis, zeilen)
    melden, anlass = entscheidung(ergebnis.klasse, abdruck, vorher, jetzt,
                                  erinnerung_tage)

    # Ob gesendet wird, entscheidet AUSSCHLIESSLICH `entscheidung()`. Eine
    # zweite Abfrage auf IN_ORDNUNG an dieser Stelle waere bequem und
    # gefaehrlich: sie wuerde das Fehlen der ersten verdecken, und die
    # wichtigste Regel dieses Wrappers haette dann keine wirksame Wache mehr.
    text = (nachricht(waechter, ergebnis, zeilen, marke, anlass, vorher, jetzt)
            if melden else "")

    if trockenlauf:
        sys.stdout.write(
            "\n--- Trockenlauf, es wird nichts verschickt und nichts "
            "vermerkt ---\n"
            f"Ausgang: {ergebnis.klasse} (Rueckgabewert "
            f"{ergebnis.rueckgabewert})\n"
            f"Entscheidung: {'MELDEN' if melden else 'SCHWEIGEN'} ({anlass})\n")
        if melden:
            sys.stdout.write(text + "\n")
        sys.stdout.flush()
        return anlass

    gesendet = _versuche_senden(senden or _standard_senden, text) if melden \
        else False

    if ergebnis.klasse == IN_ORDNUNG:
        # Es steht nichts mehr offen - der Vermerk wird geraeumt, damit ein
        # spaeter wiederkehrender Befund wieder als "neu" gilt. Das ist eine
        # Aussage ueber den ZUSTAND, nicht ueber das Senden.
        if vorher:
            vermerke.pop(waechter.schluessel, None)
            zustand_schreiben(pfad, vermerke)
        return anlass

    # Ein unveraenderter Befund schreibt den bisherigen Vermerk fort; ein
    # geaenderter faengt von vorn an (neue Standzeit, neue Laufzahl).
    fortsetzung = bool(vorher) and vorher.get("fingerabdruck") == abdruck

    if gesendet:
        gemeldet_am = _zeit_schreiben(jetzt)
    elif fortsetzung:
        # Erst vermerken, wenn die Wirkung eingetreten ist: ein
        # fehlgeschlagener Versand darf den Zeitpunkt NICHT vorruecken.
        gemeldet_am = vorher.get("zuletzt_gemeldet_am")
    else:
        # Neu oder geaendert und nicht zugestellt: ausdruecklich offen -
        # daraus wird beim naechsten Lauf Regel 3 (NACHHOLUNG).
        gemeldet_am = None

    vermerke[waechter.schluessel] = {
        "klasse": ergebnis.klasse,
        "fingerabdruck": abdruck,
        "zeilen": zeilen,
        "erstmals_am": (vorher.get("erstmals_am") if fortsetzung
                        else _zeit_schreiben(jetzt)) or _zeit_schreiben(jetzt),
        "zuletzt_gesehen_am": _zeit_schreiben(jetzt),
        "zuletzt_gemeldet_am": gemeldet_am,
        "laeufe": (vorher.get("laeufe", 0) + 1) if fortsetzung else 1,
    }
    zustand_schreiben(pfad, vermerke)
    return anlass


def _versuche_senden(senden, text):
    """Ein Sendefehler wird protokolliert, nicht weitergereicht."""
    try:
        return bool(senden(text))
    except Exception as fehler:                              # noqa: BLE001
        _hinweis(f"Der Versand ist gescheitert ({type(fehler).__name__}: "
                 f"{fehler}). Die Meldung gilt als NICHT zugestellt und wird "
                 f"beim naechsten Lauf erneut versucht.")
        return False


# ---------------------------------------------------------------------------
# Uebersicht
# ---------------------------------------------------------------------------
def status(pfad=None, schreiber=None):
    schreiber = schreiber or sys.stdout
    pfad = pfad or ZUSTAND_DATEI
    vermerke = zustand_lesen(pfad)
    schreiber.write("Bekannte Waechter und ihr Stand\n")
    schreiber.write("=" * 78 + "\n")
    for schluessel, w in WAECHTER.items():
        v = vermerke.get(schluessel)
        if not v:
            stand = "still (kein offener Befund vermerkt)"
        else:
            stand = (f"{v.get('klasse')} seit {v.get('erstmals_am')}, "
                     f"{v.get('laeufe')} Laeufe, zuletzt gemeldet "
                     f"{v.get('zuletzt_gemeldet_am') or 'NIE - steht aus'}")
        schreiber.write(f"  {schluessel:<18} {w.klartext}\n")
        schreiber.write(f"  {'':<18} {w.zweck}\n")
        schreiber.write(f"  {'':<18} {stand}\n")
    schreiber.write(f"\nZustandsdatei: {pfad}\n")
    return 0


# ---------------------------------------------------------------------------
def main(argv=None):
    zerleger = argparse.ArgumentParser(
        description="Fuehrt einen Waechter aus und meldet bei Befund per "
                    "Telegram. Rueckgabewert ist immer der des Waechters.")
    zerleger.add_argument("waechter", nargs="?", choices=list(WAECHTER),
                          help="welcher Waechter (siehe --status)")
    zerleger.add_argument("--status", action="store_true",
                          help="Uebersicht ueber alle Waechter und ihren Stand")
    zerleger.add_argument("--trockenlauf", action="store_true",
                          help="ausfuehren und die Nachricht zeigen, aber nicht "
                               "senden und nichts vermerken")
    zerleger.add_argument("--zeitlimit", type=float, default=None,
                          metavar="SEKUNDEN",
                          help="haengenden Waechter abbrechen und als Absturz "
                               "melden (ohne Angabe: kein Zeitlimit)")
    zerleger.add_argument("--erinnerung-tage", type=int,
                          default=STANDARD_ERINNERUNG_TAGE, metavar="N",
                          help=f"Abstand der Erinnerung bei unveraendertem "
                               f"Befund (Vorgabe {STANDARD_ERINNERUNG_TAGE})")
    zerleger.add_argument("--zustand", default=None, metavar="PFAD",
                          help=f"andere Zustandsdatei (Vorgabe {ZUSTAND_DATEI})")
    args = zerleger.parse_args(argv)

    if args.status:
        return status(args.zustand)
    if not args.waechter:
        zerleger.error("Entweder ein Waechter oder --status.")

    return lauf(WAECHTER[args.waechter], zustand_pfad=args.zustand,
                erinnerung_tage=args.erinnerung_tage, zeitlimit=args.zeitlimit,
                trockenlauf=args.trockenlauf)


if __name__ == "__main__":
    sys.exit(main())
