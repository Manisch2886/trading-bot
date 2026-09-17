#!/usr/bin/env python3
"""
Der unveraenderliche Kursdaten-Snapshot (TB-46, Teil 3)
==============================================================================
Registertext 5 (Abschnitt 16.3 der Vorregistrierung) verlangt **zwei**
Kursdatenbestaende:

  * einen **Live-Bestand**, taeglich fortgeschrieben, aus dem die neun
    `forward_test.py` und die Backtester-Pruefung nach Registertext 7 lesen;
  * einen **Snapshot** `<hash>/`, einmal gezogen und danach unveraenderlich,
    aus dem **ausschliesslich der Selektionslauf** liest.

Der Grund steht in Registertext 7: solange die Bots live abrufen, existiert
von ihrer Eingabe **keine Kopie**. Ein Vergleich gegen etwas, das nicht mehr
nachsehbar ist, ist kein Vergleich. Dieses Modul zieht die Kopie.

⚠️ **Was dieses Modul NICHT tut.** Es benennt `data/` nicht um, verschiebt
nichts, stellt kein Modul auf einen neuen Pfad um und entscheidet nicht,
welcher der beiden Ordnerentwuerfe gilt. Es ist das Werkzeug; der Schnitt ist
eine eigene Aufgabe und die Entscheidung darueber trifft der Betreiber.

Der Hash wird nicht neu erfunden
------------------------------------------------------------------------------
Der registrierte Datenstand-Hash entsteht in **einer** Funktion:

    research/vorregistrierung/herkunft.py :: datenstand(daten_dir)

SHA-256 ueber die `*.csv` **direkt** im Ordner, in sortierter
Dateinamenfolge, je Datei **Name + Groesse + SHA-256 des Inhalts**. Diese
Funktion hat den registrierten Wert
`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` bei 223
Dateien erzeugt, und dieses Modul **benutzt sie**, statt sie abzuschreiben.

⚠️ Eine zweite Berechnung koennte dieselbe Zahl liefern und trotzdem eine
andere Frage beantworten - andere Reihenfolge, andere Dateiauswahl. Genau
dieses Muster hat das Projekt bei der Messkette (TB-27/TB-28) und bei den
Ergebniskurven schon eingesammelt. `research/etf_trendfolge/datenstand.py`
hat sich aus demselben Grund geweigert, den Hash selbst zu rechnen.

⚠️ **Befund am Rande, gehoert in den Bericht:** die Berechnung steht
**trotzdem zweimal** im Repo - ein zeichengleiches Duplikat liegt in
`research/registernachtrag_tb41/pruefe_register.py:319`. Heute liefern beide
dasselbe. Wer eines von beiden aendert, merkt den Unterschied nicht.

Drei Eigenschaften der Berechnung, die den Zuschnitt betreffen
------------------------------------------------------------------------------
1. **Sie ist NICHT rekursiv.** `os.listdir` + `endswith(".csv")` sieht
   Unterordner nicht. Ein `data/snapshots/` **innerhalb** von `data/` wuerde
   den registrierten Hash also **nicht** mitzaehlen.
2. **Sie zaehlt nur `*.csv`.** Das `MANIFEST.json`, das dieses Modul in den
   Snapshot legt, aendert den Hash des Snapshots deshalb nicht - der Ordner
   traegt zu Recht den Namen des Bestandes, den er enthaelt.
3. **Sie haengt am uebergebenen Ordner.** Wird `data/` zu `data/live/`, zeigt
   die Voreinstellung von `datenstand()` auf einen Ordner ohne eine einzige
   `.csv` - der Hash wird dann der der **leeren** Menge, und das sieht wie
   eine Datenaenderung aus, obwohl nur der Ordner umgezogen ist.

Die Voreinstellung ist der Trockenlauf
------------------------------------------------------------------------------
Kopiert wird nur mit `--ziehen`. 202 MB zu kopieren gehoert nicht in die
Voreinstellung - dieselbe Abwaegung wie bei `kursdaten_neuaufbau.py`
(`--schreiben`) und bei den Broker-Bruecken (`--echt`).

Was ausdruecklich zum Abbruch fuehrt
------------------------------------------------------------------------------
⚠️ Keiner dieser Faelle laeuft still weiter:

  * **Das Ziel `<hash>/` existiert schon.** Es wird **nie** ueberschrieben -
    ein zweiter Snapshot ist ein neuer Lauf (Registertext 5c).
  * **Die Quelle ist leer.** Ein Snapshot ohne Kursdatei ist kein Snapshot;
    er traegt sogar einen gueltig aussehenden Namen (den Hash der leeren
    Menge). Das ist die gefaehrlichste Form von "erfolgreich".
  * **Eine Quersumme laesst sich nicht bilden** (Datei unlesbar, verschwindet
    mitten im Lauf).
  * **Eine Kopie weicht byteweise von der Quelle ab.** Dann wird der
    angelegte Ordner wieder entfernt und die Datei genannt.
  * **Die Quelle enthaelt Unterordner.** Die Hash-Berechnung ist nicht
    rekursiv (siehe 1.): ein Snapshot eines Baums traegt einen Namen, der
    nur seine oberste Ebene beschreibt. "Vollstaendig" waere dann eine
    Behauptung, die der Name nicht deckt.
  * **Das Ziel liegt innerhalb der Quelle.** Dann kopierte der Lauf in den
    Bestand, den er beschreibt.
  * **Die Quelle enthaelt schon eine Datei `MANIFEST.json`.** Sie wuerde vom
    Manifest des Snapshots ueberschrieben - und weil das Manifest sich selbst
    nicht auffuehrt, faellt das beim Nachpruefen nicht auf.

Rueckgabewerte - "konnte nicht messen" ist ein eigener, roter Ausgang
------------------------------------------------------------------------------
    0   in Ordnung: gezogen, oder `--pruefen` findet den Stand unveraendert
    1   Befund: `--pruefen` findet den Snapshot VERAENDERT
    2   NICHT PRUEFBAR / abgebrochen

⚠️ Die 2 ist der Grund, warum es sie gibt. In TB-45 haben zwei Wachen
"bestanden" gemeldet, ohne etwas gemessen zu haben - ein gescheiterter Aufruf
und ein leeres Ergebnis sahen gleich aus. Hier nicht: wer nicht messen
konnte, sagt es mit einem eigenen Wert.

Nutzung
------------------------------------------------------------------------------
    python3 shared/snapshot.py --quelle data --ziel snapshots        # Trockenlauf
    python3 shared/snapshot.py --quelle data --ziel snapshots --ziehen
    python3 shared/snapshot.py --pruefen snapshots/<hash>
    python3 shared/snapshot.py --quelle data --nur-hash
"""

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys
from datetime import datetime, timezone

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)

MANIFEST = "MANIFEST.json"
WERKZEUG = "shared/snapshot.py"

# Wo das registrierte Hash-Verfahren steht. Ein Pfad, keine Abschrift.
HERKUNFT_PFAD = os.path.join(BASE_DIR, "research", "vorregistrierung",
                             "herkunft.py")

# Rueckgabewerte
OK = 0
BEFUND = 1
NICHT_PRUEFBAR = 2

# Die drei Ausgaenge von `--pruefen`
UNVERAENDERT = "unveraendert"
VERAENDERT = "veraendert"
UNPRUEFBAR = "nicht pruefbar"


class Snapshotfehler(Exception):
    """Ein Lauf, der nicht zu Ende gebracht werden darf.

    Jede Stelle, die still weiterlaufen koennte, wirft stattdessen diese
    Ausnahme. `main` faengt sie und gibt 2 zurueck.
    """


# ===========================================================================
# Teil 1 - Das Hash-Verfahren, geliehen statt abgeschrieben
# ===========================================================================

def lade_herkunft(pfad=None):
    """Das Modul mit dem registrierten Hash-Verfahren laden.

    Ueber den Dateipfad, nicht ueber `sys.path`: der fremde Ordner
    `research/vorregistrierung/` bringt ein eigenes `beispieldaten.py` mit,
    das bei einem Import ueber den Suchpfad hiesige Namen verdecken kann.
    Denselben Weg geht `research/etf_trendfolge/register.py`.

    ⚠️ Faellt das Laden aus, wird **nicht** auf eine eigene Berechnung
    ausgewichen. Eine Ersatzberechnung waere genau die Doppelfuehrung, gegen
    die dieses Modul geschrieben ist - und sie waere unsichtbar.
    """
    pfad = pfad or HERKUNFT_PFAD
    if not os.path.exists(pfad):
        raise Snapshotfehler(
            "Das registrierte Hash-Verfahren ist nicht auffindbar: %s fehlt. "
            "Ohne es wird KEIN Hash gebildet - eine eigene Berechnung waere "
            "eine zweite Wahrheit." % pfad)
    spez = importlib.util.spec_from_file_location("tb46_herkunft", pfad)
    if spez is None or spez.loader is None:
        raise Snapshotfehler("%s ist nicht als Modul ladbar." % pfad)
    modul = importlib.util.module_from_spec(spez)
    try:
        spez.loader.exec_module(modul)
    except Exception as fehler:                       # noqa: BLE001
        raise Snapshotfehler("%s laesst sich nicht laden: %s" % (pfad, fehler))
    if not hasattr(modul, "datenstand"):
        raise Snapshotfehler(
            "%s kennt kein `datenstand()` mehr. Das Verfahren ist umgezogen - "
            "dieses Modul darf dann nicht weiterrechnen." % pfad)
    return modul


def gesamthash(ordner, herkunft=None):
    """(hash, dateizahl) - nach dem registrierten Verfahren.

    Gerechnet wird von `herkunft.datenstand`, nicht hier.
    """
    if not os.path.isdir(ordner):
        raise Snapshotfehler("%s ist kein Verzeichnis." % ordner)
    h = herkunft or lade_herkunft()
    try:
        stand = h.datenstand(ordner)
    except OSError as fehler:
        raise Snapshotfehler(
            "Der Hash ueber %s laesst sich nicht bilden: %s" % (ordner, fehler))
    return stand["datenstand"], stand["dateien"]


def quersumme(pfad):
    """SHA-256 einer einzelnen Datei - dieselbe Rechnung wie im Gesamthash.

    ⚠️ Ein `IOError` wird **nicht** zu "keine Quersumme" verschluckt. Eine
    Datei, deren Quersumme sich nicht bilden laesst, ist kein Eintrag mit
    leerem Feld, sondern ein Abbruchgrund.
    """
    hasher = hashlib.sha256()
    try:
        with open(pfad, "rb") as datei:
            for block in iter(lambda: datei.read(1 << 20), b""):
                hasher.update(block)
    except OSError as fehler:
        raise Snapshotfehler(
            "Quersumme von %s nicht bildbar: %s" % (pfad, fehler))
    return hasher.hexdigest()


# ===========================================================================
# Teil 2 - Ziehen
# ===========================================================================

def _pruefe_quelle(quelle):
    """Die Quelle, bevor irgendetwas kopiert wird. Wirft, statt zu warnen."""
    if not os.path.isdir(quelle):
        raise Snapshotfehler("Die Quelle %s ist kein Verzeichnis." % quelle)
    try:
        eintraege = sorted(os.listdir(quelle))
    except OSError as fehler:
        raise Snapshotfehler("Die Quelle %s ist nicht lesbar: %s"
                             % (quelle, fehler))

    unterordner = [e for e in eintraege
                   if os.path.isdir(os.path.join(quelle, e))]
    if unterordner:
        raise Snapshotfehler(
            "Die Quelle %s enthaelt Unterordner (%s). Das registrierte "
            "Hash-Verfahren ist NICHT rekursiv - ein Snapshot dieses Baums "
            "traege einen Namen, der nur seine oberste Ebene beschreibt."
            % (quelle, ", ".join(unterordner)))

    dateien = [e for e in eintraege
               if os.path.isfile(os.path.join(quelle, e))]

    # ⚠️ Eine Quelldatei, die schon `MANIFEST.json` heisst, wuerde beim
    # Schreiben des Manifests **ueberschrieben** - der Snapshot waere dann
    # unvollstaendig und saehe vollstaendig aus. Beim Nachpruefen faellt es
    # nicht auf, weil das Manifest sich selbst nicht auffuehrt.
    if MANIFEST in dateien:
        raise Snapshotfehler(
            "Die Quelle %s enthaelt schon eine Datei namens %s. Das Manifest "
            "des Snapshots wuerde sie ueberschreiben, und der Snapshot waere "
            "unvollstaendig, ohne es zu sagen." % (quelle, MANIFEST))

    kursdateien = [e for e in dateien if e.endswith(".csv")]
    if not kursdateien:
        raise Snapshotfehler(
            "Die Quelle %s enthaelt keine einzige `.csv`. Ein leerer Snapshot "
            "traegt den Hash der leeren Menge und sieht dabei gueltig aus - "
            "das ist kein Erfolg." % quelle)
    return dateien, kursdateien


def _pruefe_ziel(quelle, ziel_basis, hash_):
    """Der Zielordner, bevor er angelegt wird."""
    q = os.path.realpath(quelle)
    z = os.path.realpath(ziel_basis)
    if z == q or z.startswith(q + os.sep):
        raise Snapshotfehler(
            "Das Ziel %s liegt innerhalb der Quelle %s. Der Lauf kopierte in "
            "den Bestand, den er beschreibt." % (z, q))
    ziel = os.path.join(ziel_basis, hash_)
    if os.path.exists(ziel):
        raise Snapshotfehler(
            "%s existiert bereits. Ein bestehender Snapshot wird NIE "
            "ueberschrieben - ein zweiter Snapshot ist ein neuer Lauf "
            "(Registertext 5c)." % ziel)
    return ziel


def ziehen(quelle, ziel_basis, wirklich=False, herkunft=None):
    """Eine Quelle vollstaendig nach `<ziel_basis>/<hash>/` kopieren.

    Die Reihenfolge ist nicht beliebig:

      1. Quelle pruefen (leer? Unterordner?)
      2. Hash der Quelle bilden - er ist der **Name** des Ziels
      3. Ziel pruefen (existiert? liegt es in der Quelle?)
      4. kopieren, Zeitstempel erhalten
      5. **jede Datei byteweise** gegen die Quelle
      6. Hash der Kopie bilden und gegen den der Quelle stellen
      7. Manifest schreiben

    Schritt 5 und 6 sind nicht dasselbe. Schritt 6 vergleicht den
    **registrierten** Hash, und der zaehlt nur `*.csv` - eine beschaedigt
    angekommene Datei, die keine Kursdatei ist (etwa eine `.json` neben ihnen),
    geht dort nicht ein. Schritt 5 prueft **jede** Datei, unabhaengig von ihrer
    Endung, und zwar zweimal: ueber die Quersumme und byteweise.
    """
    dateien, kursdateien = _pruefe_quelle(quelle)
    hash_, anzahl = gesamthash(quelle, herkunft)
    ziel = _pruefe_ziel(quelle, ziel_basis, hash_)

    bericht = {
        "werkzeug": WERKZEUG,
        "zeitpunkt_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "quelle": os.path.realpath(quelle),
        "ziel": os.path.realpath(ziel) if wirklich else ziel,
        "datenstand": hash_,
        "kursdateien": anzahl,
        "dateien_gesamt": len(dateien),
        "nicht_im_hash": sorted(d for d in dateien if not d.endswith(".csv")),
        "gezogen": False,
        "trockenlauf": not wirklich,
    }
    if anzahl != len(kursdateien):
        # Kann nur eintreten, wenn sich der Ordner zwischen zwei Blicken
        # aendert. Dann ist der Hash nicht der des kopierten Bestandes.
        raise Snapshotfehler(
            "Die Quelle hat sich waehrend des Laufs geaendert: %d Kursdateien "
            "gezaehlt, %d im Hash." % (len(kursdateien), anzahl))

    if not wirklich:
        bericht["hinweis"] = ("Trockenlauf - es wurde nichts kopiert. "
                              "Mit --ziehen wird wirklich gezogen.")
        return bericht

    os.makedirs(ziel, exist_ok=False)
    eintraege = {}
    try:
        for name in sorted(dateien):
            q_pfad = os.path.join(quelle, name)
            z_pfad = os.path.join(ziel, name)
            try:
                shutil.copy2(q_pfad, z_pfad)      # copy2: Zeitstempel bleiben
            except OSError as fehler:
                raise Snapshotfehler("%s laesst sich nicht kopieren: %s"
                                     % (name, fehler))
            summe_quelle = quersumme(q_pfad)
            summe_kopie = quersumme(z_pfad)
            if summe_quelle != summe_kopie:
                raise Snapshotfehler(
                    "ABWEICHUNG bei %s: die Kopie stimmt nicht mit der Quelle "
                    "ueberein (%s gegen %s)."
                    % (name, summe_quelle[:16], summe_kopie[:16]))
            if not _byteweise_gleich(q_pfad, z_pfad):
                raise Snapshotfehler(
                    "ABWEICHUNG bei %s: byteweiser Vergleich mit der Quelle "
                    "fehlgeschlagen." % name)
            eintraege[name] = {
                "sha256": summe_kopie,
                "bytes": os.path.getsize(z_pfad),
                "im_hash": name.endswith(".csv"),
            }

        kopie_hash, kopie_anzahl = gesamthash(ziel, herkunft)
        if kopie_hash != hash_ or kopie_anzahl != anzahl:
            raise Snapshotfehler(
                "Der Hash der Kopie weicht vom Hash der Quelle ab "
                "(%s... / %d gegen %s... / %d)."
                % (kopie_hash[:16], kopie_anzahl, hash_[:16], anzahl))

        bericht["dateien"] = eintraege
        bericht["bytes_gesamt"] = sum(e["bytes"] for e in eintraege.values())
        schreibe_manifest(ziel, bericht)
        bericht["gezogen"] = True
    except Exception:
        # ⚠️ Ein halb gezogener Snapshot ist schlimmer als keiner: er sieht
        # wie ein Snapshot aus und traegt einen Hash, den sein Inhalt nicht
        # erfuellt. Er wird entfernt - und zwar nur er, nie die Quelle.
        shutil.rmtree(ziel, ignore_errors=True)
        raise
    return bericht


def _byteweise_gleich(a, b, block=1 << 20):
    """Zwei Dateien Block fuer Block vergleichen.

    Zusaetzlich zur Quersumme, nicht an ihrer Stelle: die Quersumme prueft,
    ob der Inhalt derselbe ist, dieser Vergleich prueft es ein zweites Mal
    auf einem anderen Weg. Bei 202 MB kostet das wenig und ist der einzige
    Schritt, der ohne die Annahme auskommt, dass SHA-256 hier stimmt.
    """
    try:
        with open(a, "rb") as fa, open(b, "rb") as fb:
            while True:
                ba, bb = fa.read(block), fb.read(block)
                if ba != bb:
                    return False
                if not ba:
                    return True
    except OSError as fehler:
        raise Snapshotfehler("Vergleich %s / %s nicht moeglich: %s"
                             % (a, b, fehler))


def schreibe_manifest(ordner, bericht):
    """Das Manifest in den Snapshot legen - erst vorlaeufig, dann umbenannt.

    `os.replace` ist atomar: es gibt kein halb geschriebenes Manifest, das
    beim Nachpruefen als "beschaedigt" erscheint, obwohl nur der Schreibvorgang
    unterbrochen wurde.
    """
    inhalt = {
        "werkzeug": bericht["werkzeug"],
        "zeitpunkt_utc": bericht["zeitpunkt_utc"],
        "quelle": bericht["quelle"],
        "datenstand": bericht["datenstand"],
        "kursdateien": bericht["kursdateien"],
        "dateien_gesamt": bericht["dateien_gesamt"],
        "bytes_gesamt": bericht.get("bytes_gesamt"),
        "verfahren": ("research/vorregistrierung/herkunft.py::datenstand - "
                      "SHA-256 ueber die *.csv direkt im Ordner, sortiert, "
                      "je Datei Name + Groesse + SHA-256 des Inhalts"),
        "dateien": bericht["dateien"],
    }
    pfad = os.path.join(ordner, MANIFEST)
    vorlaeufig = pfad + ".neu"
    try:
        with open(vorlaeufig, "w", encoding="utf-8") as datei:
            json.dump(inhalt, datei, indent=2, ensure_ascii=False,
                      sort_keys=True)
            datei.write("\n")
        os.replace(vorlaeufig, pfad)
    except OSError as fehler:
        raise Snapshotfehler("Manifest %s nicht schreibbar: %s"
                             % (pfad, fehler))
    return pfad


# ===========================================================================
# Teil 3 - Nachpruefen
# ===========================================================================

def _lies_manifest(ordner):
    """Das Manifest lesen - oder sagen, warum es nicht geht."""
    pfad = os.path.join(ordner, MANIFEST)
    if not os.path.isdir(ordner):
        return None, "%s ist kein Verzeichnis." % ordner
    if not os.path.exists(pfad):
        return None, ("%s fehlt - dieser Ordner ist kein Snapshot dieses "
                      "Werkzeugs." % pfad)
    try:
        with open(pfad, "r", encoding="utf-8") as datei:
            manifest = json.load(datei)
    except (OSError, ValueError) as fehler:
        return None, "%s ist nicht lesbar oder beschaedigt: %s" % (pfad, fehler)
    if not isinstance(manifest, dict):
        return None, "%s enthaelt kein Manifest-Objekt." % pfad
    for schluessel in ("dateien", "datenstand", "kursdateien"):
        if schluessel not in manifest:
            return None, ("%s ist beschaedigt: der Eintrag `%s` fehlt."
                          % (pfad, schluessel))
    if not isinstance(manifest["dateien"], dict) or not manifest["dateien"]:
        return None, ("%s ist beschaedigt: `dateien` ist leer oder kein "
                      "Objekt." % pfad)
    return manifest, None


def pruefen(ordner, herkunft=None):
    """Manifest gegen Ordner. Drei Ausgaenge, nie zwei.

    ⚠️ Geprueft wird in **beide** Richtungen. Nur die Manifesteintraege
    durchzugehen wuerde eine **hinzugefuegte** Datei nie finden - und genau
    eine hinzugefuegte Datei ist es, die den Datenstand-Hash aendert, ohne
    dass eine bekannte Datei sich ruehrt. Das ist der Fall, gegen den
    `research/etf_trendfolge/datenstand.py` Wache haelt.
    """
    manifest, grund = _lies_manifest(ordner)
    if manifest is None:
        return {"ausgang": UNPRUEFBAR, "grund": grund, "ordner": ordner,
                "abweichungen": []}

    abweichungen = []
    erwartet = manifest["dateien"]

    try:
        vorhanden = sorted(e for e in os.listdir(ordner)
                           if os.path.isfile(os.path.join(ordner, e)))
    except OSError as fehler:
        return {"ausgang": UNPRUEFBAR, "ordner": ordner, "abweichungen": [],
                "grund": "%s ist nicht lesbar: %s" % (ordner, fehler)}

    # Richtung 1: was das Manifest kennt
    for name in sorted(erwartet):
        eintrag = erwartet[name]
        pfad = os.path.join(ordner, name)
        if not os.path.exists(pfad):
            abweichungen.append({"datei": name, "art": "entfernt"})
            continue
        try:
            ist = quersumme(pfad)
        except Snapshotfehler as fehler:
            # Nicht als "veraendert" verbuchen: ob sie sich geaendert hat,
            # ist gerade NICHT feststellbar.
            return {"ausgang": UNPRUEFBAR, "ordner": ordner,
                    "abweichungen": abweichungen, "grund": str(fehler)}
        if ist != eintrag.get("sha256"):
            abweichungen.append({"datei": name, "art": "veraendert",
                                 "soll": eintrag.get("sha256"), "ist": ist})
            continue
        groesse = os.path.getsize(pfad)
        if eintrag.get("bytes") is not None and groesse != eintrag["bytes"]:
            abweichungen.append({"datei": name, "art": "andere Groesse",
                                 "soll": eintrag["bytes"], "ist": groesse})

    # Richtung 2: was im Ordner liegt, aber nicht im Manifest steht
    for name in vorhanden:
        if name == MANIFEST or name == MANIFEST + ".neu":
            continue
        if name not in erwartet:
            abweichungen.append({"datei": name, "art": "hinzugefuegt"})

    # Der Gesamthash zum Schluss - er ist die Aussage, auf die es ankommt.
    try:
        ist_hash, ist_anzahl = gesamthash(ordner, herkunft)
    except Snapshotfehler as fehler:
        return {"ausgang": UNPRUEFBAR, "ordner": ordner,
                "abweichungen": abweichungen, "grund": str(fehler)}

    if ist_hash != manifest["datenstand"]:
        abweichungen.append({"datei": "(Gesamthash)", "art": "veraendert",
                             "soll": manifest["datenstand"], "ist": ist_hash})
    if ist_anzahl != manifest["kursdateien"]:
        abweichungen.append({"datei": "(Dateizahl)", "art": "veraendert",
                             "soll": manifest["kursdateien"],
                             "ist": ist_anzahl})

    return {
        "ausgang": VERAENDERT if abweichungen else UNVERAENDERT,
        "ordner": ordner,
        "grund": None,
        "datenstand_soll": manifest["datenstand"],
        "datenstand_ist": ist_hash,
        "kursdateien_soll": manifest["kursdateien"],
        "kursdateien_ist": ist_anzahl,
        "abweichungen": abweichungen,
    }


# ===========================================================================
# Teil 4 - Befehlszeile
# ===========================================================================

def _drucke_pruefung(b):
    print("Snapshot nachpruefen: %s\n" % b["ordner"])
    if b["ausgang"] == UNPRUEFBAR:
        print("  NICHT PRUEFBAR")
        print("  %s" % b["grund"])
        return
    print("  Soll   %s  (%d Kursdateien)"
          % (b["datenstand_soll"], b["kursdateien_soll"]))
    print("  Ist    %s  (%d Kursdateien)"
          % (b["datenstand_ist"], b["kursdateien_ist"]))
    if b["ausgang"] == UNVERAENDERT:
        print("\n  UNVERAENDERT")
        return
    print("\n  VERAENDERT - %d Abweichung(en):" % len(b["abweichungen"]))
    for a in b["abweichungen"]:
        zusatz = ""
        if a.get("soll") is not None:
            zusatz = "  (soll %s, ist %s)" % (str(a["soll"])[:16],
                                              str(a["ist"])[:16])
        print("    %-40s %s%s" % (a["datei"], a["art"], zusatz))


def _drucke_ziehen(b):
    print("Snapshot ziehen\n")
    print("  Quelle      %s" % b["quelle"])
    print("  Datenstand  %s" % b["datenstand"])
    print("  Kursdateien %d   (Dateien gesamt: %d)"
          % (b["kursdateien"], b["dateien_gesamt"]))
    if b["nicht_im_hash"]:
        print("  ⚠️ nicht im Hash (keine .csv): %s"
              % ", ".join(b["nicht_im_hash"]))
    print("  Ziel        %s" % b["ziel"])
    if b["gezogen"]:
        print("\n  GEZOGEN - %d Datei(en), %.1f MB, jede byteweise gegen die "
              "Quelle geprueft." % (len(b["dateien"]),
                                    b["bytes_gesamt"] / 1e6))
        print("  Manifest    %s" % os.path.join(b["ziel"], MANIFEST))
    else:
        print("\n  TROCKENLAUF - nichts kopiert. Mit --ziehen wirklich ziehen.")


def main(argv=None) -> int:
    z = argparse.ArgumentParser(
        description="Zieht einen unveraenderlichen Kursdaten-Snapshot und "
                    "prueft ihn nach (TB-46, Registertext 5).")
    z.add_argument("--quelle", default=os.path.join(BASE_DIR, "data"),
                   help="der Bestand, der kopiert wird (Standard: data/)")
    z.add_argument("--ziel", default=os.path.join(BASE_DIR, "snapshots"),
                   help="der Ordner, in dem <hash>/ entsteht")
    z.add_argument("--ziehen", action="store_true",
                   help="wirklich kopieren (ohne dies: Trockenlauf)")
    z.add_argument("--pruefen", metavar="ORDNER", default=None,
                   help="einen vorhandenen Snapshot gegen sein Manifest pruefen")
    z.add_argument("--nur-hash", action="store_true",
                   help="nur den Datenstand-Hash der Quelle ausgeben")
    z.add_argument("--json", metavar="PFAD", default=None)
    a = z.parse_args(argv)

    try:
        if a.pruefen:
            bericht = pruefen(a.pruefen)
            _drucke_pruefung(bericht)
            rueckgabe = {UNVERAENDERT: OK, VERAENDERT: BEFUND,
                         UNPRUEFBAR: NICHT_PRUEFBAR}[bericht["ausgang"]]
        elif a.nur_hash:
            hash_, anzahl = gesamthash(a.quelle)
            bericht = {"quelle": os.path.realpath(a.quelle),
                       "datenstand": hash_, "kursdateien": anzahl}
            print("%s  (%d Kursdateien)  %s" % (hash_, anzahl, a.quelle))
            rueckgabe = OK
        else:
            bericht = ziehen(a.quelle, a.ziel, wirklich=a.ziehen)
            _drucke_ziehen(bericht)
            rueckgabe = OK
    except Snapshotfehler as fehler:
        print("ABBRUCH: %s" % fehler, file=sys.stderr)
        if a.json:
            _schreibe_json(a.json, {"abgebrochen": True, "grund": str(fehler)})
        return NICHT_PRUEFBAR

    if a.json:
        _schreibe_json(a.json, bericht)
        print("\nJSON: %s" % a.json)
    return rueckgabe


def _schreibe_json(pfad, inhalt):
    ordner = os.path.dirname(os.path.abspath(pfad))
    if ordner:
        os.makedirs(ordner, exist_ok=True)
    with open(pfad, "w", encoding="utf-8") as datei:
        json.dump(inhalt, datei, indent=2, ensure_ascii=False, sort_keys=True)
        datei.write("\n")


if __name__ == "__main__":
    sys.exit(main())
