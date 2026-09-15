#!/usr/bin/env python3
"""
Krypto-Kursdaten vollstaendig neu aufbauen (TB-34)
==============================================================================
Der Kursdatenbestand unter `data/` wird **nativ vom Endpunkt** neu geladen -
1h, 4h **und 1d**, letztere nicht mehr aus den Stundendaten abgeleitet.

Warum ueberhaupt, und warum jetzt
------------------------------------------------------------------------------
Drei Befunde aus TB-31, die zusammen keinen anderen Schluss zulassen:

1. **Alle 72 Krypto-Kursdateien enden mit einer Teilkerze.** Der letzte Abruf
   lief am 2026-08-31 gegen 13:00 UTC, mitten am Tag. Die letzte 1h-, 4h- und
   1d-Kerze jeder Datei haelt deshalb einen abgeschnittenen Zeitraum fest.
2. **Die 24 Tagesdateien sind abgeleitet, nicht abgerufen**
   (`shared/build_daily_crypto_data.py`, ausdruecklich als Sandbox-Ersatz
   geschrieben). Ihre erste Tageskerze deckt 6 bis 16 statt 24 Stunden ab.
   `shared/zeitabdeckung.py` rechnet beides unabhaengig nach.
3. **Es gibt keinen Cronjob, der `data/` aktualisiert.** Die neun
   `forward_test.py` holen ihre Daten live beim Lauf; `data/` wird nur von
   Hand gefuellt. Jeder Backtest und jede Optimierung rechnet deshalb auf dem
   Stand des letzten Abrufs von Hand.

`shared/binance_historie.py` (TB-31) kann das nicht heilen, und das ist kein
Mangel: es **verlaengert** nach vorn und schreibt jede vorhandene Zeile
zeichengleich zurueck. Sein ganzer Wert liegt darin, niemals zu
ueberschreiben. Ein Werkzeug, das den Bestand ersetzt, hat den **entgegen-
gesetzten** Vertrag.

Warum ein eigenes Modul und keine Erweiterung
------------------------------------------------------------------------------
Beides in eine Datei zu legen hiesse, die Zusicherung "es ueberschreibt nie"
von einem Laufzeitschalter abhaengig zu machen. Genau diese Bauform hat das
Projekt bei der Binance-Bruecke schon einmal verworfen (`testnet=True` als
Flag im Aufrufpfad, Protokoll 4.4): eine Zusicherung, die an einem Argument
haengt, ist keine.

Geteilt wird trotzdem alles, was sich teilen laesst - und zwar durch
**Benutzung**, nicht durch Abschrift: `Drossel`, `Abrufer`, `kerzen_laden`,
`erste_kerze_ms`, `als_dataframe`, `zeilen_aus_dataframe`, `schreibe_datei`,
`ZEITFORMAT`, `Kursdatei` und die 418-Behandlung kommen aus
`binance_historie`. Es gibt nur **eine** Netzstelle und nur **eine**
Schreibweise im Projekt.

Die fuenf Zusicherungen
------------------------------------------------------------------------------
**1. Nur `/api/v3/klines`.** Oeffentlich, ohne Schluessel, kein `/sapi/`,
kein `/fapi/`. Das gitignorierte `shared/fetch_binance_data.py` (enthaelt
Zugangsdaten) wird nicht eingebunden.

**2. Keine angeschnittene Kerze - strukturell, nicht durch Sorgfalt.**
Uebernommen wird nur, was der Endpunkt als **abgeschlossen** meldet:
`close_time <= Stand`. Der Stand ist die Uhrzeit des Laufs, mit `--stand`
festsetzbar. Die laufende Kerze wird gar nicht erst geschrieben - der Fehler,
der diese Aufgabe ausgeloest hat, ist damit nicht vermieden, sondern
unmoeglich.

**3. Sicherung vor dem Schreiben.** Jede Datei wird kopiert, **bevor** sie
ersetzt wird, mit SHA-256 im `MANIFEST.json`. `--zurueckspielen` stellt den
alten Stand wieder her und prueft dabei jede Pruefsumme. Es wird **nichts**
automatisch geloescht: eine Sicherung, die von selbst verschwindet, ist im
entscheidenden Moment weg (dieselbe Abwaegung wie bei der Log-Rotation,
Protokoll 4.6 - nur faellt sie hier gegen das Loeschen aus, weil ein
Kursdatenstand nicht wiederherstellbar ist, wenn der Endpunkt ihn nicht mehr
liefert).

**4. Vergleich alt gegen neu, Zeile fuer Zeile.** Je Datei: Zeilenzahl,
Zeitraum und die Zahl der Zeilen, die sich im **gemeinsamen** Bereich
unterscheiden. Eine Abweichung **an den Raendern** (erste oder letzte Zeile
des Altbestands) ist die erwartete Teilkerze. Jede Abweichung **dazwischen**
ist ein Befund: sie verhindert das Schreiben dieser Datei und steht am Anfang
der Zusammenfassung. Dafuer gibt es **keinen** Schalter - eine Historie, die
sich im Innern geaendert hat, ist etwas, das ein Mensch ansehen muss.

**5. Wiederholbar.** Zwei Laeufe mit demselben `--stand` liefern
byte-identische Dateien. Ohne `--stand` ist der Stand die Uhrzeit; dann
kommen zwischen zwei Laeufen abgeschlossene Kerzen hinzu, sobald eine
Intervallgrenze dazwischen liegt - das ist kein Zufall, sondern der Zweck.
Die Gegenprobe im Testauftrag setzt deshalb `--stand`.

Die Voreinstellung ist der Trockenlauf
------------------------------------------------------------------------------
Geschrieben wird nur mit `--schreiben`. 72 Dateien zu ersetzen ist der
groesste schreibende Eingriff, den dieses Projekt auf `data/` kennt; er
gehoert nicht in die Voreinstellung.

    python3 shared/kursdaten_neuaufbau.py                      # Trockenlauf
    python3 shared/kursdaten_neuaufbau.py --schreiben
    python3 shared/kursdaten_neuaufbau.py --symbole BTCUSDT --zeitrahmen 1d
    python3 shared/kursdaten_neuaufbau.py --stand 2026-09-15T00:00:00
    python3 shared/kursdaten_neuaufbau.py --bericht neuaufbau.json
    python3 shared/kursdaten_neuaufbau.py --zurueckspielen data_sicherung/<lauf>

Rueckgabewerte: 0 alles in Ordnung, 1 Befund (Abweichung im Innern oder eine
Datei nicht geschrieben), 2 Aufruffehler, 3 Abbruch (HTTP 418).
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

import binance_historie as bh                              # noqa: E402
import kursdaten                                           # noqa: E402

# Ein Kerzenfeld des Endpunkts: [open_time, o, h, l, c, v, close_time, ...]
FELD_OEFFNUNGSZEIT = 0
FELD_SCHLUSSZEIT = 6

KURSSPALTEN = bh.KURSSPALTEN
VOLUMEN_TOLERANZ = bh.VOLUMEN_TOLERANZ

SICHERUNGSORDNER = "data_sicherung"
MANIFEST = "MANIFEST.json"


class Neuaufbaufehler(RuntimeError):
    """Der Lauf kann fuer diese Datei nicht sinnvoll fortgesetzt werden."""


# ---------------------------------------------------------------------------
# Stand und Zeit
# ---------------------------------------------------------------------------
def stand_lesen(text):
    """`--stand` in einen UTC-Zeitpunkt uebersetzen."""
    text = text.strip().replace("Z", "")
    for form in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d %H:%M:%S.%f",
                 "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(text, form)
        except ValueError:
            continue
    raise ValueError(f"Stand nicht lesbar: {text!r}")


def als_ms(zeitpunkt):
    return int((zeitpunkt - dt.datetime(1970, 1, 1)).total_seconds() * 1000)


def abgeschlossene_kerzen(kerzen, intervall, stand_ms):
    """Nur die Kerzen, deren Zeitraum zum Stand **vorbei** ist.

    Der Endpunkt liefert die laufende Kerze mit - mit den Werten, die sie
    gerade hat. Genau daraus ist der gesamte Altbestand entstanden. Massgeblich
    ist `close_time` (Feld 6); fehlt es, wird es aus der Intervalllaenge
    gerechnet, damit eine unvollstaendige Antwort nicht zum Durchrutschen
    fuehrt.
    """
    laenge = bh.INTERVALL_MS[intervall]
    behalten = []
    verworfen = 0
    for kerze in kerzen:
        oeffnung = int(kerze[FELD_OEFFNUNGSZEIT])
        if len(kerze) > FELD_SCHLUSSZEIT:
            try:
                schluss = int(kerze[FELD_SCHLUSSZEIT])
            except (TypeError, ValueError):
                schluss = oeffnung + laenge - 1
        else:
            schluss = oeffnung + laenge - 1
        # Eine offensichtlich unbrauchbare Schlusszeit (z.B. 0) darf nicht
        # dazu fuehren, dass eine laufende Kerze als abgeschlossen gilt.
        if schluss < oeffnung:
            schluss = oeffnung + laenge - 1
        if schluss <= stand_ms:
            behalten.append(kerze)
        else:
            verworfen += 1
    return behalten, verworfen


# ---------------------------------------------------------------------------
# Vergleich alt gegen neu
# ---------------------------------------------------------------------------
def werte_aus_zeilen(zeilen_text, intervall):
    """CSV-Zeilen (ohne Kopf) -> {Zeitstempel: Werte-Dict}."""
    def zahl(text):
        # Ein leeres Feld ist genau die Form, in der eine Kerze ohne Kurse in
        # einer CSV steht (`pandas.to_csv` schreibt sie so, nicht als `nan`).
        # Sie darf den Vergleich nicht abbrechen lassen - sie ist das, wovor
        # `kursdaten.entferne_unvollstaendige()` schuetzt, und wenn die Wache
        # einmal ausfaellt, soll der Vergleich das sehen statt abzustuerzen.
        try:
            return float(text)
        except (TypeError, ValueError):
            return None

    nach_zeitpunkt = {}
    for zeile in zeilen_text:
        teile = zeile.split(",")
        if len(teile) != len(bh.SPALTEN):
            continue
        nach_zeitpunkt[teile[0]] = {
            "open": zahl(teile[1]), "high": zahl(teile[2]),
            "low": zahl(teile[3]), "close": zahl(teile[4]),
            "volume": zahl(teile[5]),
        }
    return nach_zeitpunkt


def vergleiche(alt, neu, rand_zeitpunkte):
    """Alt gegen neu im **gemeinsamen** Zeitraum, Zeile fuer Zeile.

    `alt`, `neu`: {Zeitstempel -> Werte}. `rand_zeitpunkte`: die Zeitstempel,
    an denen eine Abweichung die erwartete Teilkerze ist (erste und letzte
    Zeile des Altbestands).

    Rueckgabe: Liste von Abweichungen, jede mit `art`, `zeitpunkt`, `rand`
    (True/False) und - wo es passt - `spalte`, `alt`, `neu`.

      * `nur_alt`   - der Endpunkt kennt diesen Zeitpunkt nicht
      * `nur_neu`   - der Altbestand hat hier eine Luecke, die gefuellt wird
      * `kurs`      - mindestens eine der vier Kursspalten weicht ab
      * `volumen`   - das Volumen weicht ueber die Toleranz hinaus ab
      * `volumen_rundung` - innerhalb der Toleranz; gezaehlt, kein Befund
    """
    if not alt or not neu:
        return []
    von = max(min(alt), min(neu))
    bis = min(max(alt), max(neu))
    abweichungen = []

    for zeitpunkt in sorted(set(alt) | set(neu)):
        if zeitpunkt < von or zeitpunkt > bis:
            continue
        am_rand = zeitpunkt in rand_zeitpunkte
        a, n = alt.get(zeitpunkt), neu.get(zeitpunkt)
        if a is None:
            abweichungen.append({"art": "nur_neu", "zeitpunkt": zeitpunkt,
                                 "rand": am_rand, "spalte": None,
                                 "alt": None, "neu": None})
            continue
        if n is None:
            abweichungen.append({"art": "nur_alt", "zeitpunkt": zeitpunkt,
                                 "rand": am_rand, "spalte": None,
                                 "alt": None, "neu": None})
            continue
        for spalte in KURSSPALTEN:
            if a[spalte] != n[spalte]:
                abweichungen.append({"art": "kurs", "zeitpunkt": zeitpunkt,
                                     "rand": am_rand, "spalte": spalte,
                                     "alt": a[spalte], "neu": n[spalte]})
        if a["volume"] is None or n["volume"] is None:
            if a["volume"] is not n["volume"]:
                abweichungen.append({"art": "volumen", "zeitpunkt": zeitpunkt,
                                     "rand": am_rand, "spalte": "volume",
                                     "alt": a["volume"], "neu": n["volume"]})
        elif a["volume"] != n["volume"]:
            bezug = max(abs(a["volume"]), abs(n["volume"]), 1e-30)
            relativ = abs(a["volume"] - n["volume"]) / bezug
            art = "volumen_rundung" if relativ <= VOLUMEN_TOLERANZ else "volumen"
            abweichungen.append({"art": art, "zeitpunkt": zeitpunkt,
                                 "rand": am_rand, "spalte": "volume",
                                 "alt": a["volume"], "neu": n["volume"],
                                 "relativ": relativ})
    return abweichungen


# Welche Arten zaehlen als echte Abweichung (statt als Rundung oder als
# gefuellte Luecke)?
ECHTE_ARTEN = {"nur_alt", "kurs", "volumen"}


def abweichende_zeilen(abweichungen, nur_innen=False):
    """Die **Zeilen** (nicht Spalten), die sich unterscheiden.

    Mehrere abweichende Spalten derselben Zeile sind eine Zeile. Genau diese
    Zahl verlangt der Auftrag je Datei.
    """
    zeitpunkte = set()
    for a in abweichungen:
        if a["art"] not in ECHTE_ARTEN:
            continue
        if nur_innen and a["rand"]:
            continue
        zeitpunkte.add(a["zeitpunkt"])
    return sorted(zeitpunkte)


# ---------------------------------------------------------------------------
# Sicherung
# ---------------------------------------------------------------------------
def pruefsumme(pfad):
    hasher = hashlib.sha256()
    with open(pfad, "rb") as datei:
        for block in iter(lambda: datei.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


class Sicherung:
    """Kopiert jede Datei, **bevor** sie ersetzt wird, und haelt das fest.

    Das Manifest wird nach jeder Datei fortgeschrieben, nicht erst am Ende:
    ein Lauf, der in der Mitte abbricht, muss eine gueltige Sicherung der
    bereits ersetzten Dateien hinterlassen - sonst waere die Sicherung genau
    dann wertlos, wenn sie gebraucht wird.
    """

    def __init__(self, ordner, stand, quelle):
        # Ein belegter Sicherungsordner wird NICHT weiterbenutzt. Ein zweiter
        # Lauf in denselben Ordner wuerde die Sicherung des ersten durch den
        # bereits neu geschriebenen Stand ersetzen - die Sicherung waere dann
        # genau in dem Moment wertlos, in dem sie gebraucht wird.
        if os.path.exists(os.path.join(ordner, MANIFEST)):
            raise Neuaufbaufehler(
                f"{ordner}: enthaelt bereits ein {MANIFEST}. Ein belegter "
                f"Sicherungsordner wird nicht ueberschrieben - bitte einen "
                f"anderen angeben.")
        self.ordner = ordner
        self.stand = stand
        self.quelle = quelle
        self.eintraege = {}
        self.angelegt = False

    def _anlegen(self):
        if not self.angelegt:
            os.makedirs(self.ordner, exist_ok=True)
            self.angelegt = True

    def sichere(self, pfad):
        """Eine Datei sichern. Rueckgabe: der Pfad der Kopie."""
        self._anlegen()
        name = os.path.basename(pfad)
        ziel = os.path.join(self.ordner, name)
        shutil.copy2(pfad, ziel)
        eigen = pruefsumme(ziel)
        if eigen != pruefsumme(pfad):
            raise Neuaufbaufehler(
                f"{name}: die Sicherung stimmt nicht mit dem Original ueberein")
        self.eintraege[name] = {
            "sha256": eigen,
            "bytes": os.path.getsize(ziel),
        }
        self.schreibe_manifest()
        return ziel

    def schreibe_manifest(self):
        self._anlegen()
        inhalt = {
            "erzeugt": dt.datetime.now().isoformat(timespec="seconds"),
            "stand": self.stand.isoformat(sep=" "),
            "quelle": self.quelle,
            "werkzeug": "shared/kursdaten_neuaufbau.py",
            "dateien": self.eintraege,
        }
        pfad = os.path.join(self.ordner, MANIFEST)
        vorlaeufig = pfad + ".neu"
        with open(vorlaeufig, "w", encoding="utf-8") as datei:
            json.dump(inhalt, datei, indent=2, ensure_ascii=False, sort_keys=True)
        os.replace(vorlaeufig, pfad)

    @property
    def groesse(self):
        return sum(e["bytes"] for e in self.eintraege.values())


def zurueckspielen(sicherungsordner, zielordner):
    """Einen gesicherten Stand wiederherstellen - mit Pruefsummen.

    Geprueft wird **zweimal**: die Kopie im Sicherungsordner gegen das
    Manifest (hat jemand daran gedreht?) und die zurueckgespielte Datei gegen
    dasselbe Manifest (ist sie heil angekommen?). Ohne die zweite Pruefung
    waere "zurueckgespielt" nur eine Behauptung.
    """
    pfad = os.path.join(sicherungsordner, MANIFEST)
    if not os.path.exists(pfad):
        raise Neuaufbaufehler(f"{sicherungsordner}: kein {MANIFEST} - das ist "
                              f"keine Sicherung dieses Werkzeugs")
    with open(pfad, "r", encoding="utf-8") as datei:
        manifest = json.load(datei)

    ergebnisse = []
    for name, eintrag in sorted(manifest.get("dateien", {}).items()):
        quelle = os.path.join(sicherungsordner, name)
        ziel = os.path.join(zielordner, name)
        zeile = {"datei": name, "zurueckgespielt": False, "grund": None}
        if not os.path.exists(quelle):
            zeile["grund"] = "fehlt im Sicherungsordner"
            ergebnisse.append(zeile)
            continue
        if pruefsumme(quelle) != eintrag["sha256"]:
            zeile["grund"] = "Pruefsumme der Sicherung stimmt nicht mit dem Manifest"
            ergebnisse.append(zeile)
            continue
        vorlaeufig = ziel + ".zurueck"
        shutil.copy2(quelle, vorlaeufig)
        os.replace(vorlaeufig, ziel)
        if pruefsumme(ziel) != eintrag["sha256"]:
            zeile["grund"] = "zurueckgespielte Datei stimmt nicht mit dem Manifest"
        else:
            zeile["zurueckgespielt"] = True
        ergebnisse.append(zeile)
    return manifest, ergebnisse


# ---------------------------------------------------------------------------
# Eine Datei neu aufbauen
# ---------------------------------------------------------------------------
def baue_datei_neu(abrufer, pfad, symbol, intervall, stand, schreiben=False,
                   sicherung=None, zaehler=None):
    """Laedt eine Kursdatei nativ neu und ersetzt sie - wenn nichts dagegen steht.

    Der Ablauf, in der Reihenfolge, in der er auch scheitern koennen muss:

    1. den Altbestand lesen (Text **und** Werte),
    2. den tatsaechlichen Datenbeginn des Endpunkts **messen**,
    3. vom Datenbeginn bis zum Stand laden,
    4. alles verwerfen, dessen Zeitraum zum Stand noch laeuft,
    5. Kerzen ohne Kurse streichen und zaehlen (`kursdaten.py`),
    6. alt gegen neu vergleichen - Zeile fuer Zeile,
    7. **erst danach** sichern und schreiben, und nur, wenn keine Abweichung
       im Innern steht.
    """
    datei = bh.Kursdatei(pfad, intervall)
    ergebnis = {
        "symbol": symbol, "intervall": intervall, "pfad": pfad,
        "alt_zeilen": len(datei.werte),
        "alt_von": datei.erster_zeitpunkt, "alt_bis": datei.letzter_zeitpunkt,
        "neu_zeilen": 0, "neu_von": None, "neu_bis": None,
        "datenbeginn": None, "laufende_kerzen": 0, "gestrichene_kerzen": 0,
        "abweichende_zeilen": 0, "abweichende_zeilen_innen": 0,
        "abweichungen_innen": [], "abweichungen_rand": [],
        "volumen_rundung": 0, "gefuellte_luecken": 0,
        "geschrieben": False, "gesichert": None, "grund": None,
    }

    beginn_ms = bh.erste_kerze_ms(abrufer, symbol, intervall)
    if beginn_ms is None:
        ergebnis["grund"] = "Endpunkt liefert fuer dieses Symbol keine Kerzen"
        return ergebnis

    stand_ms = als_ms(stand)
    kerzen = bh.kerzen_laden(abrufer, symbol, intervall, beginn_ms, stand_ms)
    kerzen, laufend = abgeschlossene_kerzen(kerzen, intervall, stand_ms)
    ergebnis["laufende_kerzen"] = laufend
    if not kerzen:
        ergebnis["grund"] = "Endpunkt liefert bis zum Stand keine abgeschlossene Kerze"
        return ergebnis

    df = bh.als_dataframe(kerzen, intervall)
    df, gestrichen = kursdaten.entferne_unvollstaendige(
        df, symbol=f"{symbol}_{intervall}", melden=False)
    ergebnis["gestrichene_kerzen"] = gestrichen
    if zaehler is not None:
        zaehler.erfasse(f"{symbol}_{intervall}", gestrichen)
    if len(df) == 0:
        ergebnis["grund"] = "Endpunkt liefert keine verwertbaren Kerzen"
        return ergebnis

    neue_zeilen = bh.zeilen_aus_dataframe(df, intervall)
    ergebnis["neu_zeilen"] = len(neue_zeilen)
    ergebnis["neu_von"] = neue_zeilen[0].split(",")[0]
    ergebnis["neu_bis"] = neue_zeilen[-1].split(",")[0]
    ergebnis["datenbeginn"] = bh.zeitstempel_text(
        df["open_time"].iloc[0], intervall)

    alt_werte = {w["zeitpunkt"]: w for w in datei.werte}
    neu_werte = werte_aus_zeilen(neue_zeilen, intervall)
    raender = {datei.erster_zeitpunkt, datei.letzter_zeitpunkt}
    abweichungen = vergleiche(alt_werte, neu_werte, raender)

    # Getrennt ablegen, und die inneren zuerst: eine einzige Abweichung im
    # Innern ist der wichtigste Satz des Laufs, und sie darf nicht hinter
    # hundert Rundungszeilen abgeschnitten werden.
    ergebnis["abweichungen_innen"] = [
        a for a in abweichungen if a["art"] in ECHTE_ARTEN and not a["rand"]][:20]
    ergebnis["abweichungen_rand"] = [
        a for a in abweichungen if a["art"] in ECHTE_ARTEN and a["rand"]][:10]
    ergebnis["abweichungen_gesamt"] = len(abweichungen)
    ergebnis["volumen_rundung"] = sum(
        1 for a in abweichungen if a["art"] == "volumen_rundung")
    ergebnis["gefuellte_luecken"] = sum(
        1 for a in abweichungen if a["art"] == "nur_neu")

    alle_zeilen = abweichende_zeilen(abweichungen)
    innen = abweichende_zeilen(abweichungen, nur_innen=True)
    ergebnis["abweichende_zeilen"] = len(alle_zeilen)
    ergebnis["abweichende_zeilen_innen"] = len(innen)
    ergebnis["erste_abweichung_innen"] = innen[0] if innen else None
    ergebnis["rand_abweichungen"] = sorted(set(alle_zeilen) - set(innen))

    if innen:
        ergebnis["grund"] = (
            f"{len(innen)} Zeile(n) weichen AUSSERHALB der Raender ab "
            f"(erste: {innen[0]}) - nicht geschrieben")
        return ergebnis

    if not schreiben:
        ergebnis["grund"] = "Trockenlauf - nicht geschrieben"
        return ergebnis

    if sicherung is not None:
        ergebnis["gesichert"] = sicherung.sichere(pfad)
    bh.schreibe_datei(pfad, datei.kopfzeile, neue_zeilen, datei.endet_mit_umbruch)
    ergebnis["geschrieben"] = True
    return ergebnis


# ---------------------------------------------------------------------------
# Bericht
# ---------------------------------------------------------------------------
def _zeile(ergebnis):
    zustand = ("geschrieben" if ergebnis["geschrieben"]
               else (ergebnis["grund"] or "-"))
    return (f"  {ergebnis['symbol']:<12} {ergebnis['intervall']:<3} "
            f"{ergebnis['alt_zeilen']:>6} -> {ergebnis['neu_zeilen']:>6} Zeilen   "
            f"ab {str(ergebnis['neu_von'])[:10]:<11} "
            f"{ergebnis['abweichende_zeilen_innen']:>3} innen / "
            f"{ergebnis['abweichende_zeilen']:>3} gesamt   {zustand}")


def berichte(ergebnisse, drossel, stand, sicherung, geschrieben_erlaubt):
    mit_befund = [e for e in ergebnisse if e["abweichende_zeilen_innen"]]

    print()
    print("=" * 78)
    if mit_befund:
        # Der Auftrag verlangt das hier und nirgends weiter unten: eine
        # Abweichung, die nicht an einer Teilkerze sitzt, ist der wichtigste
        # Satz des ganzen Laufs.
        print(f"BEFUND: {len(mit_befund)} Datei(en) weichen im gemeinsamen Bereich "
              f"AUSSERHALB der Raender ab.")
        print("=" * 78)
        for e in mit_befund:
            print(f"  {e['symbol']}_{e['intervall']}: "
                  f"{e['abweichende_zeilen_innen']} Zeile(n), erste bei "
                  f"{e['erste_abweichung_innen']}")
            for a in e["abweichungen_innen"][:3]:
                print(f"      {a['zeitpunkt']}  {a['art']}"
                      f"{'/' + a['spalte'] if a['spalte'] else ''}: "
                      f"alt {a['alt']}  neu {a['neu']}")
        print("  Diese Dateien wurden NICHT geschrieben. Eine Historie, die sich")
        print("  im Innern geaendert hat, gehoert angesehen, nicht uebernommen.")
        print("=" * 78)
    else:
        print("Kein Befund: alle Abweichungen im gemeinsamen Bereich sitzen an "
              "den Raendern")
        print("(erste bzw. letzte Zeile des Altbestands) - genau dort, wo die "
              "Teilkerzen stehen.")
        print("=" * 78)

    geschrieben = [e for e in ergebnisse if e["geschrieben"]]
    rand = sum(len(e.get("rand_abweichungen", [])) for e in ergebnisse)
    rundung = sum(e["volumen_rundung"] for e in ergebnisse)
    luecken = sum(e["gefuellte_luecken"] for e in ergebnisse)
    laufend = sum(e["laufende_kerzen"] for e in ergebnisse)
    alt = sum(e["alt_zeilen"] for e in ergebnisse)
    neu = sum(e["neu_zeilen"] for e in ergebnisse)

    print(f"\n{len(ergebnisse)} Datei(en) geladen, {len(geschrieben)} geschrieben.")
    print(f"Zeilen gesamt: {alt} -> {neu} ({neu - alt:+d}).")
    print(f"Randabweichungen (erwartete Teilkerzen): {rand} Zeile(n).")
    if luecken:
        print(f"Luecken im Altbestand, die der Neuaufbau fuellt: {luecken} Zeile(n).")
    if rundung:
        print(f"Volumen-Abweichungen innerhalb der Toleranz "
              f"({VOLUMEN_TOLERANZ:g} relativ): {rundung} Zeile(n) - "
              f"Gleitkomma-Summe, kein Befund.")
    print(f"Laufende Kerzen verworfen (close_time > Stand {stand.isoformat(sep=' ')}): "
          f"{laufend}.")
    if sicherung is not None and sicherung.eintraege:
        print(f"\nSicherung: {len(sicherung.eintraege)} Datei(en), "
              f"{sicherung.groesse / (1024 * 1024):.1f} MB in")
        print(f"  {sicherung.ordner}")
        print("  Sie wird NICHT automatisch geloescht. Zurueckspielen mit:")
        print(f"    python3 shared/kursdaten_neuaufbau.py --zurueckspielen "
              f"{sicherung.ordner}")
    elif not geschrieben_erlaubt:
        print("\nTrockenlauf - es wurde nichts gesichert und nichts geschrieben. "
              "Schreiben mit --schreiben.")
    print(f"{drossel.anfragen} Anfragen, {drossel.wartezeit_gesamt:.1f}s gewartet, "
          f"{drossel.pausen_wegen_gewicht} Pause(n) wegen Gewicht.")


def datenbeginn_tabelle(ergebnisse):
    """{Symbol: {Intervall: erster Zeitstempel}} - fuer `zeitabdeckung.py`."""
    tabelle = {}
    for e in ergebnisse:
        if e.get("datenbeginn"):
            tabelle.setdefault(e["symbol"], {})[e["intervall"]] = e["datenbeginn"]
    return tabelle


# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    from paths import DATA_DIR, BASE_DIR                   # noqa: PLC0415
    from symbols_config import SYMBOLS                     # noqa: PLC0415

    zerleger = argparse.ArgumentParser(
        description="Laedt den Krypto-Kursdatenbestand ueber /api/v3/klines "
                    "vollstaendig neu - Tageskerzen nativ, nicht abgeleitet.")
    zerleger.add_argument("--schreiben", action="store_true",
                          help="die Dateien wirklich ersetzen (Voreinstellung: "
                               "Trockenlauf)")
    zerleger.add_argument("--symbole", default=None,
                          help="kommagetrennt; Voreinstellung: symbols_config")
    zerleger.add_argument("--zeitrahmen", default="1h,4h,1d")
    zerleger.add_argument("--ordner", default=DATA_DIR)
    zerleger.add_argument("--stand", default=None,
                          help="Stichzeitpunkt (UTC). Kerzen, die dann noch "
                               "laufen, werden verworfen. Voreinstellung: jetzt")
    zerleger.add_argument("--sicherung", default=None,
                          help=f"Ordner fuer die Sicherung; Voreinstellung: "
                               f"{SICHERUNGSORDNER}/<Zeitstempel> neben data/")
    zerleger.add_argument("--zurueckspielen", metavar="ORDNER", default=None,
                          help="einen gesicherten Stand wiederherstellen")
    zerleger.add_argument("--pause", type=float, default=0.25,
                          help="Mindestpause zwischen zwei Anfragen in Sekunden")
    zerleger.add_argument("--bericht", default=None,
                          help="Pfad fuer den JSON-Bericht des Laufs")
    argumente = zerleger.parse_args(argv)

    # --- Zurueckspielen ist ein eigener Betriebsfall, ohne Netz ------------
    if argumente.zurueckspielen:
        try:
            manifest, zeilen = zurueckspielen(argumente.zurueckspielen,
                                              argumente.ordner)
        except (Neuaufbaufehler, OSError, ValueError) as fehler:
            print(f"Zurueckspielen nicht moeglich: {fehler}", file=sys.stderr)
            return 2
        gut = [z for z in zeilen if z["zurueckgespielt"]]
        print(f"Sicherung vom {manifest.get('erzeugt', '?')} "
              f"(Stand {manifest.get('stand', '?')})")
        print(f"{len(gut)} von {len(zeilen)} Datei(en) zurueckgespielt nach "
              f"{argumente.ordner}")
        for z in zeilen:
            if not z["zurueckgespielt"]:
                print(f"  FEHLT {z['datei']}: {z['grund']}")
        return 0 if len(gut) == len(zeilen) and zeilen else 1

    try:
        stand = (stand_lesen(argumente.stand) if argumente.stand
                 else dt.datetime.now(dt.timezone.utc).replace(
                     tzinfo=None, microsecond=0))
    except ValueError as fehler:
        print(str(fehler), file=sys.stderr)
        return 2

    symbole = ([s.strip() for s in argumente.symbole.split(",") if s.strip()]
               if argumente.symbole else list(SYMBOLS))
    zeitrahmen = [z.strip() for z in argumente.zeitrahmen.split(",") if z.strip()]
    unbekannt = [z for z in zeitrahmen if z not in bh.INTERVALL_MS]
    if unbekannt:
        print(f"Unbekannte(r) Zeitrahmen: {', '.join(unbekannt)}", file=sys.stderr)
        return 2

    sicherungsordner = argumente.sicherung or os.path.join(
        BASE_DIR, SICHERUNGSORDNER,
        dt.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
    try:
        sicherung = (Sicherung(sicherungsordner, stand, argumente.ordner)
                     if argumente.schreiben else None)
    except Neuaufbaufehler as fehler:
        print(str(fehler), file=sys.stderr)
        return 2

    drossel = bh.Drossel(mindestpause=argumente.pause)
    abrufer = bh.Abrufer(drossel=drossel)

    print(f"Endpunkt: {bh.BASIS_URL}{bh.ENDPUNKT} (oeffentlich, ohne Schluessel)")
    print(f"Stand:    {stand.isoformat(sep=' ')} UTC - Kerzen, die dann noch "
          f"laufen, werden verworfen")
    print(f"Modus:    {'SCHREIBEN' if argumente.schreiben else 'Trockenlauf'}")
    print(f"{len(symbole)} Symbol(e), Zeitrahmen: {', '.join(zeitrahmen)}\n")

    zaehler = kursdaten.Zaehler()
    ergebnisse = []
    for symbol in symbole:
        for intervall in zeitrahmen:
            pfad = os.path.join(argumente.ordner, f"{symbol}_{intervall}.csv")
            if not os.path.exists(pfad):
                print(f"  {symbol:<12} {intervall:<3} keine Datei im Repo - "
                      f"uebersprungen")
                continue
            try:
                ergebnis = baue_datei_neu(
                    abrufer, pfad, symbol, intervall, stand,
                    schreiben=argumente.schreiben, sicherung=sicherung,
                    zaehler=zaehler)
            except bh.Gesperrt as fehler:
                print(f"\nABBRUCH: {fehler}")
                return 3
            except (bh.BinanceFehler, Neuaufbaufehler) as fehler:
                print(f"  {symbol:<12} {intervall:<3} FEHLER: {fehler}")
                continue
            ergebnisse.append(ergebnis)
            print(_zeile(ergebnis))

    print()
    if zaehler.melde() is None:
        print("Datenqualitaet: keine unvollstaendigen Kerzen in den geladenen Daten.")
    berichte(ergebnisse, drossel, stand, sicherung, argumente.schreiben)

    if argumente.bericht:
        with open(argumente.bericht, "w", encoding="utf-8") as datei:
            json.dump({"stand": stand.isoformat(sep=" "),
                       "geschrieben": argumente.schreiben,
                       "sicherung": sicherungsordner if sicherung else None,
                       "datenbeginn": datenbeginn_tabelle(ergebnisse),
                       "ergebnisse": ergebnisse},
                      datei, indent=2, ensure_ascii=False, sort_keys=True,
                      default=str)
        print(f"\nBericht: {argumente.bericht}")
        print("  Er enthaelt den gemessenen Datenbeginn je Symbol. "
              "Damit kennt")
        print("  `shared/zeitabdeckung.py --datenbeginn <bericht>` den "
              "Listing-Tag.")

    if not ergebnisse:
        print("\nKeine Datei geladen.", file=sys.stderr)
        return 2
    if any(e["abweichende_zeilen_innen"] for e in ergebnisse):
        return 1
    if argumente.schreiben and any(not e["geschrieben"] for e in ergebnisse):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
