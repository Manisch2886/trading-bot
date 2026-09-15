#!/usr/bin/env python3
"""
Zeitabdeckung der Kursdateien pruefen (TB-34)
==============================================================================
`shared/kursdaten.py` prueft auf **fehlende** Werte - der APH-Fall: eine
Kerze, deren vier Kursspalten leer sind. Eine **Teilkerze** hat vier
gefuellte Kursspalten. Sie ist nicht leer, sie ist falsch, und
`kursdaten.py` findet sie deshalb nicht.

Dieses Programm stellt die andere Frage:

    Deckt die erste und die letzte Kerze einer Datei den vollen Zeitraum
    ihres Intervalls ab?

Der Anlass ist gemessen (TB-31, hier unabhaengig nachgerechnet): **alle 24**
Krypto-Tagesdateien wurden von `shared/build_daily_crypto_data.py` aus den
1h-Daten abgeleitet. Ihre erste Tageskerze deckt 6 bis 16 statt 24 Stunden
ab, ihre letzte 13 statt 24. Solange die Datei dort beginnt bzw. endet, sitzt
die Teilkerze am Rand und faellt niemandem auf. Sobald Historie davorgesetzt
wird, sitzt sie **mitten** in der Reihe - ein stillschweigender 11-Stunden-Tag
zwischen lauter 24-Stunden-Tagen.

WORAN DIE PRUEFUNG SICH FESTMACHT - UND WAS SIE NICHT KANN
------------------------------------------------------------------------------
Eine Kursdatei enthaelt nur `open_time` und OHLCV. Ob die Kerze
`2021-09-01` 24 oder 11 Stunden umfasst, steht **nicht darin**. Die Pruefung
braucht also einen Zeugen, und sie benutzt drei - jeder mit einer klar
benannten Reichweite:

**R - Raster.** Jede `open_time` muss auf dem Raster ihres Intervalls sitzen
(1d auf dem Tag, 4h auf 00/04/08/12/16/20, 1h auf der vollen Stunde). Immer
moeglich, kostet einen Durchlauf. Faellt eine Zeile aus dem Raster, bedeuten
die Kerzen dieser Datei nicht das, was ihr Intervall behauptet.

**D - Deckung durch die feinere Datei.** Fuer `X_1d.csv` ist `X_1h.csv` der
Zeuge, fuer `X_4h.csv` ebenfalls. Die Pruefung zaehlt, wieviele der
feineren Kerzen im Zeitraum der ersten bzw. letzten groben Kerze wirklich
vorliegen, und vergleicht die grobe Kerze mit dem Aggregat genau dieser
vorliegenden. Daraus werden fuenf unterscheidbare Lagen:

| vorliegend | grobe Kerze = Aggregat | Urteil | |
|---|---|---|---|
| vollstaendig | ja | `vollstaendig` | kein Befund |
| vollstaendig | nein | `widerspruch` | **Befund** |
| unvollstaendig | ja | `abgeleitete_teilkerze` | **Befund** - der Beweis |
| unvollstaendig | nein | `unbelegt` | **Befund** |
| keine | - | `keine_aussage` | Hinweis |

Die dritte Zeile ist der Kern: passt die grobe Kerze auf die letzte Stelle
zum Aggregat *genau der vorhandenen* feineren Kerzen, dann ist sie daraus
**abgeleitet** - das ist kein Verdacht, sondern ein Nachweis.

**S - Stand.** Der Zeitraum der letzten Kerze muss zum Stichzeitpunkt
(`--stand`, Voreinstellung: jetzt) **abgelaufen** sein. Eine Kerze, deren
Periode noch laeuft, ist zwingend eine Teilkerze. Das ist die Wache fuer den
laufenden Betrieb: sie schlaegt genau dann an, wenn ein Abruf mitten in einer
Kerze geschrieben hat und man kurz danach nachsieht.

**Was die Pruefung nicht kann, und das ist wichtig:** die letzte Kerze der
**feinsten** Datei eines Symbols (`X_1h.csv`) hat keinen feineren Zeugen. War
sie beim Abruf angeschnitten, steht das nirgends in den Dateien. Dafuer gibt
es genau zwei Antworten, und beide stehen ausserhalb dieses Programms: der
Stand-Zeuge, wenn kurz nach dem Abruf geprueft wird, und
`shared/kursdaten_neuaufbau.py`, das eine noch laufende Kerze gar nicht erst
schreibt. Der Bericht sagt je Datei, welche Zeugen greifen konnten - eine
Datei ohne Befund ist nicht dasselbe wie eine geprueft vollstaendige.

DIE ERSTE KERZE EINER HISTORIE - DER EINE FALL, DER AUSSEN BLEIBEN MUSS
------------------------------------------------------------------------------
Eine angeschnittene **erste** Kerze kann zwei ganz verschiedene Ursachen
haben, und die Dateien allein unterscheiden sie nicht:

* das Abruffenster hat die Historie beschnitten (`LOOKBACK`) - **Fehler**, und
  genau der Befund, um den es hier geht;
* das Symbol wurde an diesem Tag gelistet - dann hat der Tag auch nativ keine
  24 Stunden Handel, und die kurze Kerze ist **richtig**.

Offline ist das nicht entscheidbar. Deshalb meldet die Pruefung eine kurze
erste Kerze in der Voreinstellung als Befund und laesst sich mit
`--datenbeginn <datei.json>` eines Besseren belehren: eine Datei, die je
Symbol und Zeitrahmen den **gemessenen** Datenbeginn des Endpunkts nennt.
Genau diese Datei schreibt `kursdaten_neuaufbau.py` bei jedem Lauf.
Ohne sie wird gemeldet statt geraten.

MELDEN, NICHT STOPPEN
------------------------------------------------------------------------------
Dieses Modul wird von **keinem** Bot importiert, und das ist Absicht:

1. `kursdaten.entferne_unvollstaendige()` laeuft in allen neun Bots bei jedem
   Laden. Es arbeitet zeilenweise auf einem DataFrame im Speicher. Die
   Deckungspruefung braucht **andere Dateien** und einen Stichzeitpunkt -
   beides waere in einer Zeilenmaske fehl am Platz und kostete jeden Botlauf
   zusaetzliche Lesevorgaenge.
2. `kursdaten.py` **streicht und zaehlt**. Eine Teilkerze darf nicht
   stillschweigend gestrichen werden: die letzte Tageskerze zu streichen
   verschoebe das Ende jedes Backtests. Sie gehoert gemeldet und von einem
   Menschen entschieden.
3. Der Live-Betrieb darf nie an einer Datenpruefung haengenbleiben. Ein
   eigenstaendiges Werkzeug mit Rueckgabewert 1 kann ein Cronjob sichtbar
   machen, ohne dass ein Bot davon abhaengt - dasselbe Muster wie
   `shared/ergebniskurven.py` und `shared/determinismus.py`.

Das Modul benutzt **nur die Standardbibliothek** und liest die Dateien
zeilenweise; es laeuft damit auch dort, wo pandas fehlt, und haelt nie eine
ganze Kursdatei im Speicher.

    python3 shared/zeitabdeckung.py                      # prueft data/
    python3 shared/zeitabdeckung.py --ordner X
    python3 shared/zeitabdeckung.py --datei data/BTCUSDT_1d.csv
    python3 shared/zeitabdeckung.py --stand 2026-08-31T13:00:00
    python3 shared/zeitabdeckung.py --datenbeginn datenbeginn.json
    python3 shared/zeitabdeckung.py --luecken            # Luecken mitzaehlen
    python3 shared/zeitabdeckung.py --json bericht.json

Rueckgabewert 1 bei Befund, 0 sonst, 2 bei Aufruffehler.
"""

import argparse
import csv
import datetime as dt
import glob
import json
import os
import sys

# ---------------------------------------------------------------------------
# Die drei Zeitrahmen dieses Projekts
# ---------------------------------------------------------------------------
INTERVALL_SEK = {
    "1h": 3600,
    "4h": 14400,
    "1d": 86400,
}

ZEITFORMAT = {
    "1h": "%Y-%m-%d %H:%M:%S",
    "4h": "%Y-%m-%d %H:%M:%S",
    "1d": "%Y-%m-%d",
}

# Welcher Zeitrahmen kann fuer welchen als Zeuge dienen? Der feinste zuerst -
# er gibt die genaueste Aussage ueber die Abdeckung.
ZEUGEN = {
    "1d": ["1h", "4h"],
    "4h": ["1h"],
    "1h": [],
}

KURSSPALTEN = ["open", "high", "low", "close"]

# Relative Toleranz fuer das Volumen - und nur dort. Begruendung wie in
# `binance_historie.VOLUMEN_TOLERANZ`: eine Summe von 24 Gleitkommawerten
# landet in den letzten Bits anders als dieselben Handel in anderer
# Reihenfolge summiert. Die vier Kursspalten werden exakt verglichen.
VOLUMEN_TOLERANZ = 1e-9

# Urteile der Deckungspruefung
VOLLSTAENDIG = "vollstaendig"
ABGELEITETE_TEILKERZE = "abgeleitete_teilkerze"
UNBELEGT = "unbelegt"
WIDERSPRUCH = "widerspruch"
KEINE_AUSSAGE = "keine_aussage"

# Welche Urteile sind ein Befund?
DECKUNGS_BEFUNDE = {ABGELEITETE_TEILKERZE, UNBELEGT, WIDERSPRUCH}


class Unlesbar(RuntimeError):
    """Die Datei laesst sich nicht als Kursdatei lesen."""


# ---------------------------------------------------------------------------
# Dateiname -> Symbol und Zeitrahmen
# ---------------------------------------------------------------------------
def zerlege_namen(dateiname):
    """`BTCUSDT_1d.csv` -> ('BTCUSDT', '1d').

    Die Namensform ist im ganzen Projekt dieselbe (`<SYMBOL>_<intervall>.csv`),
    und der Zeitrahmen steht nirgends sonst in der Datei. Er *muss* aus dem
    Namen kommen. Zurueckgegeben wird der Suffix auch dann, wenn er keiner
    der drei gefuehrten Zeitrahmen ist - der Bericht soll `BTCUSDT_15m.csv`
    beim Namen nennen koennen statt es "unbekannt" zu heissen.
    """
    rumpf = os.path.basename(dateiname)
    if not rumpf.endswith(".csv"):
        return None, None
    rumpf = rumpf[:-4]
    if "_" not in rumpf:
        return None, None
    symbol, _, suffix = rumpf.rpartition("_")
    if not symbol:
        return None, None
    return symbol, suffix


def lies_zeitpunkt(text, intervall):
    return dt.datetime.strptime(text, ZEITFORMAT[intervall])


def schreibe_zeitpunkt(zeitpunkt, intervall):
    return zeitpunkt.strftime(ZEITFORMAT[intervall])


# ---------------------------------------------------------------------------
# Lesen - immer zeilenweise, nie die ganze Datei im Speicher
# ---------------------------------------------------------------------------
def _zerlege_zeile(zeile, intervall, nummer, pfad):
    try:
        zeitpunkt = lies_zeitpunkt(zeile["open_time"], intervall)
    except (KeyError, TypeError, ValueError) as fehler:
        raise Unlesbar(f"{os.path.basename(pfad)} Zeile {nummer}: "
                       f"open_time unlesbar ({fehler})") from fehler
    werte = {"zeitpunkt": zeitpunkt, "text": zeile["open_time"]}
    for spalte in KURSSPALTEN + ["volume"]:
        roh = zeile.get(spalte)
        try:
            werte[spalte] = float(roh) if roh not in (None, "") else None
        except ValueError:
            werte[spalte] = None
    return werte


def durchlaufe(pfad, intervall):
    """Erzeugt je Zeile ein Werte-Dict. Streaming, kein Zwischenspeicher."""
    with open(pfad, "r", encoding="utf-8", newline="") as datei:
        leser = csv.DictReader(datei)
        if not leser.fieldnames or "open_time" not in leser.fieldnames:
            raise Unlesbar(f"{os.path.basename(pfad)}: keine Spalte 'open_time'")
        for nummer, zeile in enumerate(leser, 2):
            yield _zerlege_zeile(zeile, intervall, nummer, pfad)


def lies_grundriss(pfad, intervall):
    """Ein Durchlauf, der alles liefert, was ohne Zeugen zu haben ist.

    Rueckgabe-Dict: `zeilen`, `erste`, `letzte` (volle Werte-Dicts),
    `raster_fehler` (bis zu fuenf Zeitpunkte ausserhalb des Rasters),
    `luecken` (Zahl fehlender Rasterplaetze zwischen erster und letzter
    Kerze) und `erste_luecke`.
    """
    schrittweite = dt.timedelta(seconds=INTERVALL_SEK[intervall])
    zeilen = 0
    erste = None
    letzte = None
    vorige = None
    raster_fehler = []
    luecken = 0
    erste_luecke = None

    for werte in durchlaufe(pfad, intervall):
        zeilen += 1
        if erste is None:
            erste = werte
        if not auf_raster(werte["zeitpunkt"], intervall):
            if len(raster_fehler) < 5:
                raster_fehler.append(werte["text"])
        if vorige is not None:
            abstand = werte["zeitpunkt"] - vorige
            fehlend = int(abstand / schrittweite) - 1
            # Ein Abstand <= 0 heisst: die Datei ist nicht aufsteigend sortiert
            # oder fuehrt einen Zeitpunkt doppelt. Das muss vor der
            # Vielfachen-Pruefung stehen - ein Rueckwaertssprung um genau ein
            # Intervall ginge sonst als "krumm? nein" durch.
            if abstand <= dt.timedelta(0):
                if len(raster_fehler) < 5:
                    raster_fehler.append(werte["text"])
            elif abstand % schrittweite != dt.timedelta(0):
                if len(raster_fehler) < 5:
                    raster_fehler.append(werte["text"])
            elif fehlend > 0:
                luecken += fehlend
                if erste_luecke is None:
                    erste_luecke = schreibe_zeitpunkt(vorige + schrittweite, intervall)
        vorige = werte["zeitpunkt"]
        letzte = werte

    if zeilen == 0:
        raise Unlesbar(f"{os.path.basename(pfad)}: keine Datenzeilen")

    return {"zeilen": zeilen, "erste": erste, "letzte": letzte,
            "raster_fehler": raster_fehler, "luecken": luecken,
            "erste_luecke": erste_luecke}


def auf_raster(zeitpunkt, intervall):
    """Sitzt der Zeitpunkt auf dem Raster seines Intervalls?

    Gerechnet wird gegen die Epoche - dasselbe Raster, das der Endpunkt
    benutzt (UTC-Millisekunden, teilbar durch die Intervalllaenge).
    """
    sekunden = int((zeitpunkt - dt.datetime(1970, 1, 1)).total_seconds())
    return sekunden % INTERVALL_SEK[intervall] == 0


def lies_fenster(pfad, intervall, von, bis):
    """Alle Zeilen mit `von <= open_time < bis`. Bricht ab, sobald sie durch
    sind - bei der ersten Kerze kostet das ein paar Zeilen statt der Datei."""
    treffer = []
    for werte in durchlaufe(pfad, intervall):
        if werte["zeitpunkt"] >= bis:
            break
        if werte["zeitpunkt"] >= von:
            treffer.append(werte)
    return treffer


# ---------------------------------------------------------------------------
# Der Zeuge: deckt die feinere Datei den Zeitraum der groben Kerze?
# ---------------------------------------------------------------------------
def aggregat(zeilen):
    """OHLCV der feineren Kerzen zu einer groben zusammenfassen.

    Genau die Rechnung, die `build_daily_crypto_data.resample_to_daily()`
    macht - deshalb ist die Uebereinstimmung ein Nachweis der Ableitung und
    keine Aehnlichkeit.
    """
    if not zeilen:
        return None
    hochs = [z["high"] for z in zeilen if z["high"] is not None]
    tiefs = [z["low"] for z in zeilen if z["low"] is not None]
    volumen = [z["volume"] for z in zeilen if z["volume"] is not None]
    return {
        "open": zeilen[0]["open"],
        "high": max(hochs) if hochs else None,
        "low": min(tiefs) if tiefs else None,
        "close": zeilen[-1]["close"],
        "volume": sum(volumen) if volumen else None,
    }


def gleich_bis_aufs_volumen(kerze, summe):
    """Vier Kursspalten exakt, Volumen mit Toleranz."""
    if summe is None:
        return False
    for spalte in KURSSPALTEN:
        if kerze.get(spalte) is None or summe.get(spalte) is None:
            return False
        if kerze[spalte] != summe[spalte]:
            return False
    alt, neu = kerze.get("volume"), summe.get("volume")
    if alt is None or neu is None:
        return True
    if alt == neu:
        return True
    bezug = max(abs(alt), abs(neu), 1e-30)
    return abs(alt - neu) / bezug <= VOLUMEN_TOLERANZ


def pruefe_deckung(kerze, intervall, zeugenpfad, zeugen_intervall):
    """Die Kerze `kerze` gegen die feinere Datei `zeugenpfad` halten.

    Rueckgabe: Dict mit `urteil`, `vorhanden`, `erwartet` und - wo es etwas
    zu sagen gibt - der Zahl der wirklich belegten Zeiteinheiten.
    """
    von = kerze["zeitpunkt"]
    bis = von + dt.timedelta(seconds=INTERVALL_SEK[intervall])
    erwartet = INTERVALL_SEK[intervall] // INTERVALL_SEK[zeugen_intervall]
    zeilen = lies_fenster(zeugenpfad, zeugen_intervall, von, bis)
    vorhanden = len(zeilen)

    ergebnis = {
        "zeuge": os.path.basename(zeugenpfad),
        "zeuge_intervall": zeugen_intervall,
        "erwartet": erwartet,
        "vorhanden": vorhanden,
        "stunden": round(vorhanden * INTERVALL_SEK[zeugen_intervall] / 3600.0, 2),
        "stunden_erwartet": round(INTERVALL_SEK[intervall] / 3600.0, 2),
    }

    if vorhanden == 0:
        ergebnis["urteil"] = KEINE_AUSSAGE
        return ergebnis

    passt = gleich_bis_aufs_volumen(kerze, aggregat(zeilen))
    ergebnis["aggregat_passt"] = passt
    if vorhanden == erwartet:
        ergebnis["urteil"] = VOLLSTAENDIG if passt else WIDERSPRUCH
    else:
        ergebnis["urteil"] = ABGELEITETE_TEILKERZE if passt else UNBELEGT
    return ergebnis


def finde_zeugen(ordner, symbol, intervall):
    """Der feinste vorhandene Zeuge - oder (None, None)."""
    for feiner in ZEUGEN.get(intervall, []):
        pfad = os.path.join(ordner, f"{symbol}_{feiner}.csv")
        if os.path.exists(pfad):
            return pfad, feiner
    return None, None


# ---------------------------------------------------------------------------
# Eine Datei pruefen
# ---------------------------------------------------------------------------
def pruefe_datei(pfad, stand, datenbeginn=None, luecken_zaehlen=False, ordner=None):
    """Alle drei Zeugen auf eine Datei anwenden.

    `datenbeginn`: {"SYMBOL": {"1d": "2017-08-17", ...}} - der **gemessene**
    Datenbeginn des Endpunkts. Stimmt die erste Kerze damit ueberein, ist
    ihre kurze Abdeckung der Listing-Tag und kein Befund.
    """
    ordner = ordner or os.path.dirname(os.path.abspath(pfad))
    symbol, intervall = zerlege_namen(pfad)
    befund = {
        "datei": os.path.basename(pfad), "symbol": symbol, "intervall": intervall,
        "befunde": [], "hinweise": [], "zeugen": [],
    }
    if intervall not in INTERVALL_SEK:
        befund["intervall"] = None
        befund["suffix"] = intervall
        befund["hinweise"].append({
            "art": "nicht_gefuehrt",
            "text": (f"Zeitrahmen {intervall!r} wird von diesem Projekt nicht "
                     f"gefuehrt" if intervall else
                     "kein Zeitrahmen im Dateinamen") + " - uebersprungen",
        })
        befund["uebersprungen"] = True
        return befund

    grundriss = lies_grundriss(pfad, intervall)
    befund.update({
        "zeilen": grundriss["zeilen"],
        "erste": grundriss["erste"]["text"],
        "letzte": grundriss["letzte"]["text"],
        "luecken": grundriss["luecken"],
        "erste_luecke": grundriss["erste_luecke"],
    })

    # --- R: Raster ---------------------------------------------------------
    befund["zeugen"].append("R")
    if grundriss["raster_fehler"]:
        befund["befunde"].append({
            "art": "raster",
            "text": f"{len(grundriss['raster_fehler'])} Zeitpunkt(e) sitzen nicht "
                    f"auf dem {intervall}-Raster oder haben einen krummen Abstand "
                    f"(erste: {grundriss['raster_fehler'][0]})",
        })
    if grundriss["luecken"]:
        meldung = {
            "art": "luecke",
            "text": f"{grundriss['luecken']} fehlende(r) Rasterplatz/-plaetze "
                    f"zwischen erster und letzter Kerze "
                    f"(erste ab {grundriss['erste_luecke']})",
        }
        (befund["befunde"] if luecken_zaehlen else befund["hinweise"]).append(meldung)

    # --- S: Stand ----------------------------------------------------------
    befund["zeugen"].append("S")
    ende_letzte = (grundriss["letzte"]["zeitpunkt"]
                   + dt.timedelta(seconds=INTERVALL_SEK[intervall]))
    befund["ende_letzte"] = ende_letzte.isoformat(sep=" ")
    if ende_letzte > stand:
        befund["befunde"].append({
            "art": "offen",
            "text": f"die letzte Kerze {grundriss['letzte']['text']} laeuft bis "
                    f"{ende_letzte.isoformat(sep=' ')} und ist zum Stand "
                    f"{stand.isoformat(sep=' ')} noch nicht abgeschlossen - "
                    f"sie ist zwingend eine Teilkerze",
        })

    # --- D: Deckung durch die feinere Datei --------------------------------
    zeugenpfad, zeugen_intervall = finde_zeugen(ordner, symbol, intervall)
    if zeugenpfad is None:
        befund["hinweise"].append({
            "art": "kein_zeuge",
            "text": f"keine feinere Datei fuer {symbol}_{intervall} - die "
                    f"Abdeckung der Randkerzen ist aus den Dateien nicht belegbar",
        })
        return befund

    befund["zeugen"].append("D")
    bekannt_ab = None
    if datenbeginn:
        bekannt_ab = (datenbeginn.get(symbol) or {}).get(intervall)

    for rand, kerze in (("erste", grundriss["erste"]), ("letzte", grundriss["letzte"])):
        if grundriss["zeilen"] == 1 and rand == "letzte":
            continue
        deckung = pruefe_deckung(kerze, intervall, zeugenpfad, zeugen_intervall)
        deckung["rand"] = rand
        deckung["kerze"] = kerze["text"]
        befund.setdefault("deckung", {})[rand] = deckung

        if deckung["urteil"] not in DECKUNGS_BEFUNDE:
            continue

        # Der eine Fall, der aussen bleiben muss: die erste Kerze steht am
        # gemessenen Datenbeginn des Endpunkts, also am Listing-Tag.
        if (rand == "erste" and bekannt_ab is not None
                and kerze["text"] == bekannt_ab):
            befund["hinweise"].append({
                "art": "listing_tag",
                "text": f"erste Kerze {kerze['text']} deckt nur "
                        f"{deckung['stunden']:g} von {deckung['stunden_erwartet']:g} "
                        f"Stunden ab - das ist der gemessene Datenbeginn des "
                        f"Endpunkts, also der Listing-Tag. Kein Befund.",
            })
            deckung["urteil_gemildert"] = "listing_tag"
            continue

        befund["befunde"].append({
            "art": f"rand_{rand}",
            "urteil": deckung["urteil"],
            "text": _deckungstext(rand, kerze["text"], deckung),
        })

    return befund


def _deckungstext(rand, zeitpunkt, deckung):
    kopf = (f"{rand.capitalize()} Kerze {zeitpunkt}: {deckung['zeuge']} belegt "
            f"{deckung['vorhanden']} von {deckung['erwartet']} "
            f"{deckung['zeuge_intervall']}-Kerzen "
            f"({deckung['stunden']:g} von {deckung['stunden_erwartet']:g} Stunden)")
    if deckung["urteil"] == ABGELEITETE_TEILKERZE:
        return (kopf + " - und die Kerze ist auf die letzte Stelle das Aggregat "
                       "genau dieser Teilmenge: sie ist daraus ABGELEITET.")
    if deckung["urteil"] == UNBELEGT:
        return (kopf + " - und sie stimmt nicht mit dem Aggregat dieser Teilmenge "
                       "ueberein. Mindestens eine der beiden Dateien ist am Rand "
                       "angeschnitten.")
    return (f"{rand.capitalize()} Kerze {zeitpunkt}: {deckung['zeuge']} belegt den "
            f"Zeitraum vollstaendig, aber die Kerze stimmt nicht mit dem Aggregat "
            f"ueberein - die beiden Dateien widersprechen sich.")


# ---------------------------------------------------------------------------
def jetzt_utc():
    """Jetzt in UTC, ohne Zeitzonenangabe - so wie die Kursdateien rechnen.

    Nicht `utcnow()`: das ist ab Python 3.12 als veraltet markiert, und dieses
    Projekt laeuft auf 3.9 wie auf 3.11.
    """
    return dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)


def pruefe_ordner(ordner, muster="*.csv", stand=None, datenbeginn=None,
                  luecken_zaehlen=False):
    stand = stand or jetzt_utc()
    befunde = []
    for pfad in sorted(glob.glob(os.path.join(ordner, muster))):
        try:
            befunde.append(pruefe_datei(pfad, stand, datenbeginn=datenbeginn,
                                        luecken_zaehlen=luecken_zaehlen,
                                        ordner=ordner))
        except (Unlesbar, OSError) as fehler:
            befunde.append({"datei": os.path.basename(pfad), "symbol": None,
                            "intervall": None, "befunde": [{"art": "unlesbar",
                                                            "text": str(fehler)}],
                            "hinweise": [], "zeugen": []})
    return befunde


def _text(eintrag):
    return eintrag["text"] if isinstance(eintrag, dict) else str(eintrag)


def berichte(befunde, stand):
    print("=" * 78)
    print("ZEITABDECKUNG - deckt die erste und letzte Kerze ihren Zeitraum ab?")
    print("=" * 78)
    print(f"Stand: {stand.isoformat(sep=' ')} (UTC)")

    mit_befund = [b for b in befunde if b["befunde"]]
    geprueft = [b for b in befunde if not b.get("uebersprungen")]
    ohne_zeugen = [b for b in geprueft if "D" not in b.get("zeugen", [])]

    print(f"Geprueft: {len(geprueft)} Kursdatei(en), "
          f"{len(befunde) - len(geprueft)} uebersprungen.\n")

    if mit_befund:
        print(f"{len(mit_befund)} Datei(en) mit Befund:\n")
        for befund in mit_befund:
            print(f"  {befund['datei']}  ({befund.get('zeilen', '?')} Zeilen, "
                  f"{befund.get('erste', '?')} bis {befund.get('letzte', '?')})")
            for eintrag in befund["befunde"]:
                print(f"      [!] {_text(eintrag)}")
            for eintrag in befund["hinweise"]:
                print(f"      -   {_text(eintrag)}")
            print()
    else:
        print("Kein Befund: jede gepruefte Randkerze deckt ihren Zeitraum ab, "
              "soweit die Zeugen reichen.\n")

    if ohne_zeugen:
        print(f"Ohne Deckungszeugen (keine feinere Datei vorhanden): "
              f"{len(ohne_zeugen)} Datei(en).")
        print("  Fuer sie ist nur Raster und Stand geprueft. Eine angeschnittene")
        print("  letzte Kerze waere dort aus den Dateien allein nicht zu sehen.")
        namen = ", ".join(b["datei"] for b in ohne_zeugen[:6])
        print(f"  {namen}{' ...' if len(ohne_zeugen) > 6 else ''}\n")

    mit_luecke = [b for b in geprueft if b.get("luecken")]
    if mit_luecke:
        print(f"Rasterluecken: {len(mit_luecke)} Datei(en), zusammen "
              f"{sum(b['luecken'] for b in mit_luecke)} fehlende(r) Rasterplatz/"
              f"-plaetze.")
        print("  Fuer Aktien-Tagesdateien ist das der Normalfall (Wochenenden,")
        print("  Feiertage) und keine Aussage. Bei Krypto laeuft der Handel "
              "durch -")
        print("  dort ist jede Luecke ein Ausfall des Endpunkts oder des Abrufs.")
        krypto = [b for b in mit_luecke if (b.get("symbol") or "").endswith("USDT")]
        for b in krypto[:5]:
            print(f"    {b['datei']}: {b['luecken']} ab {b['erste_luecke']}")
        if len(krypto) > 5:
            print(f"    ... und {len(krypto) - 5} weitere Krypto-Datei(en)")
        print()

    zaehler = {}
    for befund in befunde:
        for eintrag in befund["befunde"]:
            art = eintrag["art"] if isinstance(eintrag, dict) else "unbekannt"
            zaehler[art] = zaehler.get(art, 0) + 1
    print("=" * 78)
    if zaehler:
        print("Zusammenfassung: " + ", ".join(
            f"{anzahl}x {art}" for art, anzahl in sorted(zaehler.items())))
    else:
        print("Zusammenfassung: kein Befund.")


def lade_datenbeginn(pfad):
    """Die gemessenen Datenbeginne lesen.

    Zwei Formen werden angenommen: die schlanke `{"BTCUSDT": {"1d": "..."}}`
    und der Bericht von `kursdaten_neuaufbau.py`, der sie unter
    `"datenbeginn"` fuehrt.
    """
    with open(pfad, "r", encoding="utf-8") as datei:
        roh = json.load(datei)
    if isinstance(roh, dict) and "datenbeginn" in roh:
        roh = roh["datenbeginn"]
    sauber = {}
    for symbol, je_intervall in (roh or {}).items():
        if not isinstance(je_intervall, dict):
            continue
        sauber[symbol] = {}
        for intervall, wert in je_intervall.items():
            if isinstance(wert, dict):          # Form aus `messe_datenbeginn`
                wert = wert.get("beginn")
            if wert:
                sauber[symbol][intervall] = wert
    return sauber


def _stand_lesen(text):
    text = text.strip().replace("Z", "")
    for form in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d %H:%M:%S.%f",
                 "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(text, form)
        except ValueError:
            continue
    raise ValueError(f"Stand nicht lesbar: {text!r}")


def main(argv=None) -> int:
    _SHARED = os.path.dirname(os.path.abspath(__file__))
    standard = os.path.join(os.path.dirname(_SHARED), "data")

    zerleger = argparse.ArgumentParser(
        description="Prueft, ob die erste und letzte Kerze jeder Kursdatei den "
                    "vollen Zeitraum ihres Intervalls abdeckt.")
    zerleger.add_argument("--ordner", default=standard)
    zerleger.add_argument("--muster", default="*.csv")
    zerleger.add_argument("--datei", action="append", default=None,
                          help="nur diese Datei(en) pruefen (mehrfach angebbar)")
    zerleger.add_argument("--stand", default=None,
                          help="Stichzeitpunkt (UTC), Voreinstellung: jetzt")
    zerleger.add_argument("--datenbeginn", default=None,
                          help="JSON mit dem gemessenen Datenbeginn je Symbol - "
                               "eine kurze erste Kerze gilt dann als Listing-Tag")
    zerleger.add_argument("--luecken", action="store_true",
                          help="fehlende Rasterplaetze als Befund werten, nicht "
                               "nur als Hinweis")
    zerleger.add_argument("--json", metavar="PFAD", default=None)
    argumente = zerleger.parse_args(argv)

    try:
        stand = _stand_lesen(argumente.stand) if argumente.stand else jetzt_utc()
    except ValueError as fehler:
        print(str(fehler), file=sys.stderr)
        return 2

    datenbeginn = None
    if argumente.datenbeginn:
        try:
            datenbeginn = lade_datenbeginn(argumente.datenbeginn)
        except (OSError, ValueError) as fehler:
            print(f"--datenbeginn nicht lesbar: {fehler}", file=sys.stderr)
            return 2

    if argumente.datei:
        befunde = []
        for pfad in argumente.datei:
            if not os.path.exists(pfad):
                print(f"Datei nicht gefunden: {pfad}", file=sys.stderr)
                return 2
            try:
                befunde.append(pruefe_datei(pfad, stand, datenbeginn=datenbeginn,
                                            luecken_zaehlen=argumente.luecken))
            except (Unlesbar, OSError) as fehler:
                befunde.append({"datei": os.path.basename(pfad), "symbol": None,
                                "intervall": None, "hinweise": [], "zeugen": [],
                                "befunde": [{"art": "unlesbar", "text": str(fehler)}]})
    else:
        if not os.path.isdir(argumente.ordner):
            print(f"Ordner nicht gefunden: {argumente.ordner}", file=sys.stderr)
            return 2
        befunde = pruefe_ordner(argumente.ordner, argumente.muster, stand=stand,
                                datenbeginn=datenbeginn,
                                luecken_zaehlen=argumente.luecken)

    berichte(befunde, stand)

    if argumente.json:
        with open(argumente.json, "w", encoding="utf-8") as datei:
            json.dump({"stand": stand.isoformat(), "befunde": befunde},
                      datei, indent=2, ensure_ascii=False, default=str)
        print(f"Bericht als JSON: {argumente.json}")

    treffer = [b for b in befunde if b["befunde"]]
    if treffer:
        print(f"\nBEFUND: {len(treffer)} Datei(en) haben eine Randkerze, die "
              f"ihren Zeitraum nicht abdeckt.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
