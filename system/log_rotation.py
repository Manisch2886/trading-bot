"""
Log-Rotation fuer die Dateien unter logs/
==============================================================================
Mehrere Logdateien des Projekts wachsen unbegrenzt. Das Problem ist nicht der
Platz, sondern die LESBARKEIT: in einer Datei, die zu neun Zehnteln aus
wiederholten Routinemeldungen besteht, geht eine echte Fehlermeldung unter.

Dieses Skript laeuft per Cron (Zeile in system/README_LOG_ROTATION.md, NICHT
eingetragen) oder von Hand. Es kennt keinen Zustand: es entscheidet allein
anhand der aktuellen Dateigroesse und ist damit beliebig oft wiederholbar.

Der eine Punkt, an dem eine Log-Rotation ueblicherweise scheitert
------------------------------------------------------------------------------
Dashboard, Telegram-Bot und caffeinate halten ihre Logdatei DAUERHAFT offen.
Ein `mv datei datei.alt` wuerde das offene Dateihandle mitnehmen: der Dienst
schreibt weiter in `datei.alt`, die neue `datei` bleibt fuer immer leer, und
niemand merkt es, bis man beim naechsten Fehler in die falsche Datei schaut.

Deshalb wird hier NICHT umbenannt, sondern KOPIERT und die Originaldatei
anschliessend GELEERT (`truncate`). Die Datei behaelt dabei ihren Inode -
jedes offene Handle zeigt weiter auf dieselbe, nun leere Datei.

Voraussetzung dafuer ist, dass die Schreiber im Anhaengemodus (O_APPEND)
schreiben, denn nur dann wird der Schreib-Offset bei jedem Schreibvorgang neu
auf das Dateiende gesetzt. Das ist bei allen Schreibern dieses Projekts der
Fall und keine Annahme, sondern die Funktionsweise der jeweiligen Stelle:

  * Cronjobs schreiben mit `>>` (Shell, O_APPEND).
  * launchd oeffnet StandardOutPath/StandardErrorPath anhaengend.
  * Pythons logging.FileHandler benutzt standardmaessig mode="a".

Wuerde ein Schreiber die Datei ohne O_APPEND offen halten, entstuende nach dem
Leeren ein Loch aus Nullbytes bis zu seinem alten Offset - Inhalt geht dabei
nicht verloren, die Datei sieht aber am Anfang unschoen aus. Der Selbsttest
prueft den Anhaengefall am Verhalten, mit einem echten zweiten Prozess.

Datenverlust zwischen Sichern und Leeren
------------------------------------------------------------------------------
Naiv gilt: was zwischen dem letzten Lesen und dem `truncate` geschrieben wird,
ist weg. Dieses Fenster wird hier so klein gemacht, wie es ohne Sperre geht:

  1. Alles lesen und ins Archiv schreiben.
  2. Archiv dauerhaft sichern (flush + fsync, dazu fsync auf den Ordner).
  3. NOCHMAL lesen. Kam etwas nach, zurueck zu Schritt 1.
  4. Erst wenn ein Lesevorgang leer zurueckkommt, wird geleert.

Zwischen dem leeren Lesevorgang aus Schritt 3 und dem `truncate` liegt damit
kein Datei-Zugriff mehr, nur zwei unmittelbar aufeinander folgende Systemaufrufe
auf demselben Dateideskriptor. Restfenster: einige Mikrosekunden. Es ist nicht
null und wird deshalb hier benannt statt verschwiegen; der Selbsttest beziffert
es, indem er waehrend fortlaufender Rotation durchgehend schreibt und danach
jede einzelne Zeile wiederfindet.

Geleert wird ausserdem nur, wenn das Archiv nachweislich vollstaendig ist
(Groesse des Archivs == Zahl der kopierten Bytes). Alte Staende werden erst
NACH dieser Pruefung geloescht.

Nutzung:
    python3 system/log_rotation.py                 # rotiert, was zu gross ist
    python3 system/log_rotation.py --trockenlauf   # zeigt nur, was passieren wuerde
    python3 system/log_rotation.py --status        # Uebersicht inkl. alter Staende
"""

import argparse
import glob
import logging
import os
import re
import sys
from datetime import datetime

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)
LOG_WURZEL = os.path.join(BASE_DIR, "logs")

logger = logging.getLogger("log_rotation")

# ---------------------------------------------------------------------------
# Schwelle und Zahl der Staende
#
# 1 MB: die groesste Logdatei des Projekts lag am 12.09.2026 bei rund 262 KB
# (forward_test.log) und ist ueber Monate gewachsen. 1 MB laesst also reichlich
# Luft und die Rotation bleibt ein seltenes Ereignis - wichtig, weil jede
# Rotation eine Schnittstelle im Protokoll ist, an der man beim Suchen eine
# Datei weiterblaettern muss. Nach oben begrenzt die Lesbarkeit: 1 MB Text sind
# gut 10.000 Zeilen. `grep` und `tail` stoert das nicht, ein Mensch scrollt da
# nicht mehr durch, und genau um diesen Menschen geht es bei dieser Aufgabe.
#
# 5 Staende: 1 MB x (1 + 5) = 6 MB Obergrenze je Datei. Bei den heutigen
# Wachstumsraten deckt das den Zeitraum ab, in dem man nach einem Vorfall
# ueberhaupt noch nachsieht. Mehr Staende kosten nichts an Platz, machen aber
# das Durchsuchen umstaendlicher.
# ---------------------------------------------------------------------------
STANDARD_SCHWELLE = 1_000_000
STANDARD_STAENDE = 5

# Die beiden Brueckenprotokolle sind KEINE Wegwerf-Logs: dort stehen Order-IDs,
# Ausfuehrungspreise, Teilausfuehrungen, Gebuehren und - anders als in der
# Datenbank - auch der VERLAUF fehlgeschlagener Versuche samt Traceback.
#
# Ausgenommen werden sie trotzdem nicht, denn "ausgenommen" heisst hier
# "waechst weiter unbegrenzt", und das ist der Zustand, der behoben werden
# soll. Der Ausweg ist die zweite vom Auftrag angebotene Variante: deutlich
# mehr Staende. 20 x 1 MB = 20 MB Verlauf je Bruecke.
#
# Tragfaehig ist das, weil das Endergebnis jeder Order zusaetzlich in der
# Broker-Datenbank steht (Tabelle `spiegelungen`: order_id,
# ausfuehrungspreis, gebuehr, antwort - je Trade und Seite; Fehlversuche in
# `versuche`). Das Protokoll ist die ausfuehrliche Fassung, nicht die
# einzige.
MEHR_STAENDE = 20

SONDERFAELLE = {
    os.path.join("broker", "testnet_spiegel.log"): MEHR_STAENDE,
    os.path.join("broker", "ibkr_paper_spiegel.log"): MEHR_STAENDE,
}

# Dateien, die sich SELBST rotieren. Ein zweiter Rotator wuerde hier nichts
# verbessern und zwei konkurrierende Namensschemata fuer dieselbe Datei
# einfuehren (`.log.1` vom Handler neben `.log.<Zeitmarke>` von hier).
# Beide sind durch maxBytes x backupCount bereits nach oben begrenzt - also
# genau das, was diese Aufgabe erreichen will.
#
# Die Zahlen stehen hier nur zur Anzeige; der Selbsttest vergleicht sie per AST
# mit den echten Handler-Argumenten, damit sie nicht auseinanderlaufen.
SELBSTROTIEREND = {
    os.path.join("notifications", "telegram_bot.log"):
        ("notifications/telegram_bot.py", 2_000_000, 3),
    os.path.join("notifications", "manuelle_eingriffe.log"):
        ("notifications/manual_close.py", 1_000_000, 5),
}

# Ein Archiv heisst <name>.log.<Zeitmarke> und endet damit NICHT auf ".log" -
# es wird also nie selbst zum Rotationskandidaten. Das Muster ist streng, damit
# beim Aufraeumen ausschliesslich eigene Archive geloescht werden und
# beispielsweise die `.log.1` eines RotatingFileHandler unangetastet bleibt.
ZEITMARKE = "%Y-%m-%dT%H-%M-%S"
STAND_MUSTER = re.compile(r"\.log\.\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}(-\d+)?$")

# Wenn eine Datei schneller waechst, als wir sie kopieren koennen, wird nach so
# vielen Nachlese-Runden abgebrochen - ohne zu leeren. Lieber keine Rotation
# als eine, die im Kreis laeuft.
MAX_NACHLESE_RUNDEN = 20

BLOCK = 1 << 20


# ---------------------------------------------------------------------------
def _innerhalb(pfad: str, wurzel: str) -> bool:
    """Liegt `pfad` wirklich unter `wurzel`? Geprueft an den aufgeloesten
    Pfaden, damit ein Symlink nicht aus logs/ herausfuehrt."""
    echt_wurzel = os.path.realpath(wurzel)
    return os.path.realpath(pfad).startswith(echt_wurzel + os.sep)


def gefundene_logs(log_wurzel: str = LOG_WURZEL):
    """Alle `*.log` unterhalb von logs/, als Pfade relativ zu logs/.

    Bewusst gesucht statt aufgelistet: eine Liste waere eine Stelle, an der ein
    neuer Bot oder ein neuer Dienst vergessen wird. Alles ausser `*.log` bleibt
    dadurch automatisch aussen vor - Datenbanken, JSON-Zustaende, `.env`.
    """
    if not os.path.isdir(log_wurzel):
        return []
    gefunden = []
    muster = os.path.join(log_wurzel, "**", "*.log")
    for pfad in glob.glob(muster, recursive=True):
        if not os.path.isfile(pfad):
            continue
        gefunden.append(os.path.relpath(pfad, log_wurzel))
    return sorted(gefunden)


def einstellung(rel: str):
    """(staende, ausgenommen_grund) fuer eine Logdatei."""
    if rel in SELBSTROTIEREND:
        quelle, max_bytes, staende = SELBSTROTIEREND[rel]
        return staende, (f"rotiert selbst: RotatingFileHandler in {quelle}, "
                         f"{max_bytes // 1000} KB x {staende} Staende")
    return SONDERFAELLE.get(rel, STANDARD_STAENDE), None


def plan(log_wurzel: str = LOG_WURZEL, schwelle: int = STANDARD_SCHWELLE):
    """Was zu tun waere - ohne irgendetwas zu tun. Grundlage von
    --trockenlauf, --status und des echten Laufs, damit alle drei dieselbe
    Entscheidung treffen."""
    eintraege = []
    for rel in gefundene_logs(log_wurzel):
        pfad = os.path.join(log_wurzel, rel)
        staende, ausgenommen = einstellung(rel)
        eintrag = {
            "rel": rel,
            "pfad": pfad,
            "groesse": os.path.getsize(pfad),
            "schwelle": schwelle,
            "staende": staende,
            "ausgenommen": ausgenommen,
            "rotieren": False,
            "grund": "",
        }
        if ausgenommen:
            eintrag["grund"] = ausgenommen
        elif os.path.islink(pfad):
            eintrag["grund"] = "Symlink - wird nicht angefasst"
        elif not _innerhalb(pfad, log_wurzel):
            eintrag["grund"] = "zeigt aus logs/ heraus - wird nicht angefasst"
        elif eintrag["groesse"] < schwelle:
            eintrag["grund"] = (f"unter der Schwelle "
                                f"({eintrag['groesse']} < {schwelle} Bytes)")
        else:
            eintrag["rotieren"] = True
            eintrag["grund"] = (f"ueber der Schwelle "
                               f"({eintrag['groesse']} >= {schwelle} Bytes)")
        eintraege.append(eintrag)
    return eintraege


# ---------------------------------------------------------------------------
def _fsync_ordner(pfad: str) -> None:
    """Sorgt dafuer, dass der NAME des neuen Archivs die Platte erreicht, nicht
    nur sein Inhalt. Ohne das kann ein Stromausfall unmittelbar nach dem Leeren
    ein Archiv hinterlassen, das es im Verzeichnis nicht gibt."""
    ordner = os.path.dirname(os.path.abspath(pfad)) or "."
    fd = os.open(ordner, os.O_RDONLY)
    try:
        os.fsync(fd)
    except OSError:
        # Manche Dateisysteme verweigern fsync auf Ordner. Kein Grund, die
        # Rotation abzubrechen - der Inhalt des Archivs ist bereits gesichert.
        logger.debug("fsync auf Ordner %s nicht moeglich", ordner)
    finally:
        os.close(fd)


def archivname(pfad: str, jetzt=None) -> str:
    """<pfad>.<Zeitmarke>, bei Kollision mit angehaengtem Zaehler.

    Zeitmarke statt durchnummerierter Staende (.1, .2, .3): kein Umbenennen
    einer ganzen Kette bei jeder Rotation - jedes Umbenennen waere eine
    weitere Stelle, an der ein Lauf auf halber Strecke abbrechen und einen
    Stand ueberschreiben kann. Ausserdem sortiert die Zeitmarke lexikalisch
    wie chronologisch, und man sieht am Namen, wann geschnitten wurde.
    """
    marke = (jetzt or datetime.now()).strftime(ZEITMARKE)
    kandidat = f"{pfad}.{marke}"
    zaehler = 1
    while os.path.exists(kandidat):
        kandidat = f"{pfad}.{marke}-{zaehler}"
        zaehler += 1
    return kandidat


def alte_staende(pfad: str):
    """Vorhandene eigene Archive einer Logdatei, aeltester zuerst."""
    treffer = [p for p in glob.glob(glob.escape(pfad) + ".*")
               if STAND_MUSTER.search(p) and os.path.isfile(p)]
    return sorted(treffer)


def sichere_und_leere(pfad: str, ziel: str) -> int:
    """Kopiert den Inhalt von `pfad` nach `ziel` und leert `pfad` anschliessend,
    ohne ihn umzubenennen oder neu anzulegen. Gibt die Zahl der gesicherten
    Bytes zurueck. Wirft eine Ausnahme, wenn das Archiv nicht vollstaendig ist -
    dann wurde NICHT geleert.

    Die Schleife hat genau eine Aufgabe: dafuer zu sorgen, dass der letzte
    Dateizugriff vor dem `truncate` ein LEERER Lesevorgang ist und zwischen
    beiden nichts mehr liegt als zwei Abfragen. Jeder Aufruf, der dort
    dazwischengeraet, kostet Zeilen - ein `fsync` an dieser Stelle kostete
    messbar knapp eine Zeile je Rotation bei 5.000 Zeilen/s.

    Deshalb stehen fsync des Inhalts, fsync des Verzeichnisses und die
    Groessenpruefung alle VOR dem letzten Lesevorgang. Erlaubt ist das, weil
    ein leerer Lesevorgang beweist, dass seit der Pruefung nichts dazukam.
    """
    gesichert = 0
    ungesichert = 0
    runden = 0
    with open(pfad, "r+b") as quelle:
        with open(ziel, "xb") as archiv:
            # Der NAME des Archivs, einmalig: spaeteres Anhaengen aendert den
            # Verzeichniseintrag nicht mehr. Damit ist dieser teure Aufruf aus
            # dem heiklen Teil heraus.
            _fsync_ordner(ziel)

            while True:
                block = quelle.read(BLOCK)
                if block:
                    archiv.write(block)
                    gesichert += len(block)
                    ungesichert += len(block)
                    continue

                if ungesichert:
                    # Gelesen, aber noch nicht dauerhaft. Sichern und NOCHMAL
                    # lesen - nicht leeren.
                    archiv.flush()
                    os.fsync(archiv.fileno())
                    echte_groesse = os.fstat(archiv.fileno()).st_size
                    if echte_groesse != gesichert:
                        raise RuntimeError(
                            f"Archiv {ziel} ist {echte_groesse} Bytes gross, "
                            f"kopiert wurden {gesichert} - es wird NICHT "
                            f"geleert.")
                    ungesichert = 0
                    runden += 1
                    if runden > MAX_NACHLESE_RUNDEN:
                        raise RuntimeError(
                            f"{pfad} waechst schneller als die Rotation "
                            f"kopieren kann ({runden} Nachlese-Runden, "
                            f"{gesichert} Bytes). Es wurde NICHTS geleert.")
                    continue

                # Nichts nachgekommen, nichts ungesichert: jetzt und nur jetzt.
                quelle.truncate(0)
                break

        quelle.flush()
        os.fsync(quelle.fileno())
    return gesichert


def raeume_staende_auf(pfad: str, staende: int):
    """Loescht die aeltesten eigenen Archive, bis nur noch `staende` da sind.
    Gibt die geloeschten Pfade zurueck. Wird erst aufgerufen, wenn das neue
    Archiv vollstaendig gesichert ist."""
    vorhanden = alte_staende(pfad)
    ueberzaehlig = vorhanden[:-staende] if staende > 0 else list(vorhanden)
    geloescht = []
    for alt in ueberzaehlig:
        try:
            os.remove(alt)
            geloescht.append(alt)
        except OSError as fehler:
            logger.warning("Alter Stand %s liess sich nicht loeschen: %s",
                           alt, fehler)
    return geloescht


def rotiere_eine(eintrag: dict) -> dict:
    """Rotiert genau eine Datei. Faengt jeden Fehler ab: ein kaputtes Log darf
    die Rotation der anderen nicht verhindern und erst recht keinen Dienst
    stoppen."""
    ergebnis = dict(eintrag, ergebnis="fehlgeschlagen", gesichert=0,
                    archiv=None, geloescht=[])
    try:
        ziel = archivname(eintrag["pfad"])
        gesichert = sichere_und_leere(eintrag["pfad"], ziel)
        ergebnis["archiv"] = ziel
        ergebnis["gesichert"] = gesichert
        ergebnis["geloescht"] = raeume_staende_auf(eintrag["pfad"],
                                                   eintrag["staende"])
        ergebnis["ergebnis"] = "rotiert"
        logger.info("%s rotiert: %d Bytes gesichert nach %s%s",
                    eintrag["rel"], gesichert, os.path.basename(ziel),
                    (f", {len(ergebnis['geloescht'])} alte Stand(e) geloescht"
                     if ergebnis["geloescht"] else ""))
    except Exception as fehler:                                # noqa: BLE001
        ergebnis["grund"] = str(fehler)
        logger.error("%s NICHT rotiert: %s", eintrag["rel"], fehler)
    return ergebnis


def rotiere(log_wurzel: str = LOG_WURZEL, schwelle: int = STANDARD_SCHWELLE):
    """Ein vollstaendiger Lauf. Gibt die Ergebnisse je Datei zurueck."""
    ergebnisse = []
    for eintrag in plan(log_wurzel, schwelle):
        if not eintrag["rotieren"]:
            ergebnisse.append(dict(eintrag, ergebnis="uebersprungen",
                                   gesichert=0, archiv=None, geloescht=[]))
            continue
        ergebnisse.append(rotiere_eine(eintrag))
    return ergebnisse


# ---------------------------------------------------------------------------
def _kb(bytes_: int) -> str:
    return f"{bytes_ / 1000:.1f} KB"


def zeige_plan(eintraege, ueberschrift: str, mit_staenden: bool = False):
    print(ueberschrift)
    print("-" * 78)
    if not eintraege:
        print("  Keine Logdateien gefunden.")
        return
    for eintrag in eintraege:
        marke = "ROTIEREN" if eintrag["rotieren"] else "        "
        print(f"  {marke}  {eintrag['rel']:<46} {_kb(eintrag['groesse']):>10}")
        print(f"            {eintrag['grund']}")
        if mit_staenden:
            vorhanden = alte_staende(eintrag["pfad"])
            if vorhanden:
                print(f"            {len(vorhanden)} alte Stand(e), es werden "
                      f"{eintrag['staende']} behalten:")
                for alt in vorhanden:
                    print(f"              {os.path.basename(alt)}  "
                          f"{_kb(os.path.getsize(alt))}")


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Rotiert die Logdateien unter logs/ nach Groesse, ohne "
                    "laufende Dienste zu stoeren.")
    zerleger.add_argument("--schwelle", type=int, default=STANDARD_SCHWELLE,
                          metavar="BYTES",
                          help=f"Groesse, ab der rotiert wird "
                               f"(Standard {STANDARD_SCHWELLE})")
    zerleger.add_argument("--wurzel", default=LOG_WURZEL, metavar="ORDNER",
                          help="Log-Ordner (Standard: logs/ des Projekts)")
    gruppe = zerleger.add_mutually_exclusive_group()
    gruppe.add_argument("--trockenlauf", action="store_true",
                        help="zeigt nur, was rotiert wuerde")
    gruppe.add_argument("--status", action="store_true",
                        help="Uebersicht inklusive vorhandener alter Staende")
    argumente = zerleger.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    if argumente.status or argumente.trockenlauf:
        eintraege = plan(argumente.wurzel, argumente.schwelle)
        if argumente.status:
            zeige_plan(eintraege, "Status der Logdateien unter "
                       f"{argumente.wurzel}", mit_staenden=True)
        else:
            zeige_plan(eintraege, "TROCKENLAUF - es wird nichts veraendert.")
            faellig = sum(1 for e in eintraege if e["rotieren"])
            print("-" * 78)
            print(f"  {faellig} von {len(eintraege)} Dateien waere faellig.")
        return 0

    ergebnisse = rotiere(argumente.wurzel, argumente.schwelle)
    rotiert = [e for e in ergebnisse if e["ergebnis"] == "rotiert"]
    fehler = [e for e in ergebnisse if e["ergebnis"] == "fehlgeschlagen"]
    gesichert = sum(e["gesichert"] for e in rotiert)
    geloescht = sum(len(e["geloescht"]) for e in rotiert)

    print(f"Log-Rotation: {len(rotiert)} von {len(ergebnisse)} Dateien "
          f"rotiert, {_kb(gesichert)} gesichert, {geloescht} alte "
          f"Stand(e) geloescht, {len(fehler)} fehlgeschlagen.")
    for eintrag in fehler:
        print(f"  FEHLGESCHLAGEN {eintrag['rel']}: {eintrag['grund']}")

    # Rueckgabewert 1 nur bei echtem Fehlschlag. Ein Lauf ohne faellige Datei
    # ist der Normalfall und keine Meldung wert - sonst kaeme die Cron-Mail
    # taeglich und man liest sie nicht mehr.
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
