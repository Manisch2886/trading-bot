#!/usr/bin/env python3
"""
Die Entscheidungskerze: EINE Regel, EINE Tuer, fuer Backtest und Papierpfad
==============================================================================
Der Anlass ist Nebenbefund N1 aus TB-35:

    Die fuenf Krypto-`forward_test.py` entscheiden auf der LAUFENDEN Kerze.
    `strategies/t3_supertrend/forward_test.py`, Zeile 132/133:
    `row = df.iloc[-1]`. Der Cronjob laeuft kurz nach der Vier-Stunden-
    Grenze - `row` ist damit eine wenige Minuten alte Teilkerze einer
    Vier-Stunden-Strategie, deren Hoch, Tief und Schluss noch fast auf der
    Eroeffnung liegen.

Der Backtest rechnet auf **abgeschlossenen** Kerzen. Backtest und Papierpfad
rechnen also nicht dasselbe. Das ist nicht bloss unsauber:

* Es bricht die ausdrueckliche Vorbedingung fuer den Echtgeld-Betrieb (D5):
  "Backtest-Pfad stimmt mit Papierpfad ueberein."
* Der Live-Record ist die **einzige** Out-of-Sample-Evidenz des Projekts.
  Ein Holdout, der nach anderen Regeln entsteht als das Validierte, ist als
  Bestaetigung wenig wert.

Die Richtung ist entschieden: **der Live-Betrieb folgt dem Backtest**, nicht
umgekehrt. Den Backtest eine Teilkerze nachbilden zu lassen hiesse, einen
Zustand festzuschreiben, den niemand entworfen hat - es hiesse, einen Bug zu
modellieren.

------------------------------------------------------------------------------
Die Regel, in einem Satz
------------------------------------------------------------------------------

    Entscheidungskerze ist die letzte Kerze, deren `close_time` VOR der
    Startzeit des Laufs liegt.

Und weil an dieser Stelle alles haengt, ausgeschrieben:

    `schluss < startzeit`, wobei `schluss` der LETZTE AUGENBLICK IST, DER
    NOCH ZUR KERZE GEHOERT.

Welche Lesart `close_time` hat, entscheidet darueber, ob die Regel sinnvoll
oder absurd ist - das ist kein Detail, sondern der Kern:

* **Binance-Lesart** (Feld 6 der Rohkerze): `close_time = open + Laenge - 1
  Millisekunde`. Die 08:00-Kerze eines Vier-Stunden-Charts endet um
  11:59:59.999.
* **"Natuerliche" Lesart**: die 08:00-Kerze endet um 12:00:00.

Mit der zweiten Lesart und einem strikten `<` duerfte ein Lauf, der um
12:00:00 startet, die soeben fertig gewordene 08:00-Kerze **nicht** nehmen -
er muesste auf die 04:00-Kerze zurueckgreifen und waere acht Stunden alt.
Das waere offensichtlich falsch und wuerde die Gleichheit mit dem Backtest
gerade zerstoeren.

Deshalb gilt hier die Binance-Lesart, und zwar nicht aus Bequemlichkeit,
sondern weil sie die Lesart der Datenquelle dieses Projekts IST. Damit
bedeutet die Regel ausgerechnet das Richtige:

    Lauf startet 12:00:00  ->  08:00-Kerze: schluss 11:59:59.999 < 12:00:00
                               genommen. Die 12:00-Kerze laeuft noch.

Die Grenze, an der solche Regeln kippen, ist damit ebenfalls festgelegt:
eine Kerze, deren `close_time` **genau** auf der Startzeit liegt (ein Lauf um
11:59:59.999), wird **nicht** genommen. Das ist ein striktes `<`.

------------------------------------------------------------------------------
Warum ein eigenes Modul - und warum es trotzdem KEINE zweite Regel ist
------------------------------------------------------------------------------
Dieses Projekt hat schon zu viele Wege zu denselben Daten. Diese Schicht soll
einen daraus machen, nicht einen weiteren hinzufuegen. Deshalb:

* **Die Regel selbst steht weiter genau einmal**, naemlich in
  `shared/abrufschutz.abgeschlossen_maske` (TB-35), zeichengleich mit
  `shared/kursdaten_neuaufbau.abgeschlossene_kerzen` (TB-34). Fuer Krypto
  ruft dieses Modul sie auf und rechnet sie **nicht nach**. Ein zweites
  `open + laenge - 1` waere genau die Doppelfuehrung, an der dieses Projekt
  schon einmal Zahlen verloren hat.
* **Was hier neu ist, ist nicht die Regel, sondern die Tuer**: woher die
  Daten kommen (`data/` mit Rueckfall), welche Startzeit gilt, und dass eine
  Abweichung gemeldet wird statt still zu bleiben.

Warum das nicht IN `abrufschutz.py` steht, obwohl die Regel dort wohnt: die
beiden Module bewachen entgegengesetzte Fehlerrichtungen. `abrufschutz`
schuetzt den **Schreibpfad** der acht `fetch_*.py` - dort kostet zu langes
Warten nichts, und der teure Fehler ist eine Teilkerze in der CSV. Hier geht
es um den **Lesepfad** der neun Bots - dort kostet zu langes Warten einen
ganzen Handelstag. Ein Modul mit zwei entgegengesetzten Risikoprofilen waere
schwerer zu lesen als zwei Module mit je einem, und die Abwaegung unten bei
den Aktien laesst sich nur mit diesem Unterschied begruenden.

Warum nicht in `shared/kursdaten.py`: das beantwortet eine andere Frage -
"fehlen dieser Kerze die Kurse?" (NaN in open/high/low/close), nicht "ist
ihr Zeitraum vorbei?". Beide Fragen werden hier gestellt, nacheinander, und
zwar ueber die vorhandenen Funktionen.

------------------------------------------------------------------------------
Aktien: dieselbe Regel, aber NICHT dieselbe Schranke
------------------------------------------------------------------------------
`abrufschutz` rechnet den Schluss einer Tageskerze mit `open + 24h - 1`, also
`D 23:59:59`. Fuer den Schreibpfad ist das richtig und ausdruecklich
begruendet (siehe Kopf von `abrufschutz.py`): die Frage "ist dieser Zeitraum
SICHER vorbei?" hat nur eine teure Fehlerrichtung, also genuegt eine sichere
Schranke, und `D+1 00:00 UTC` liegt garantiert nach jedem NYSE-Schluss.

Fuer den **Entscheidungspfad** stimmt dieselbe Schranke nicht mehr, und das
ist messbar:

* Die vier Aktien-Bots laufen werktags um **22:15 Uhr** Ortszeit
  (`crontab -l`, belegt am 11.09.2026, `docs/DATENLUECKEN.md`). Das sind
  20:15 UTC im Sommer bzw. 21:15 UTC im Winter.
* Die NYSE schliesst um 20:00 UTC (Sommer) bzw. 21:00 UTC (Winter).
* Die Bots laufen also **15 Minuten nach Handelsschluss** und entscheiden
  heute auf der soeben fertig gewordenen Tageskerze von Tag D.
* Mit der Schranke `D 23:59:59` waere die D-Kerze um 20:15 UTC noch nicht
  "abgeschlossen". Die Bots wuerden auf die Kerze von **D-1** zurueckfallen:
  jedes Signal einen vollen Handelstag zu spaet.

Hier ist die Frage also **zweiseitig teuer** - genau der Fall, von dem der
Kopf von `abrufschutz.py` sagt, dass eine Faustregel ihn nicht traegt und
`notifications/boersenkalender.py` zustaendig ist. Also wird gefragt, was der
Kalender sagt: der Schluss einer Tageskerze von Tag D ist der **echte
Sitzungsschluss** dieses Tages, inklusive Feiertagen, verkuerzten Handelstagen
und US-Zeitumstellung.

Praktisch braucht das genau **eine** Kalenderabfrage je Lauf, nicht eine je
Zeile: `boersenkalender.status(startzeit)["letzter_handelstag"]` ist bereits
"die letzte Sitzung, deren `market_close <= startzeit` liegt". Eine Tageskerze
ist genau dann entscheidbar, wenn ihr Datum nicht nach diesem Tag liegt -
Sitzungen sind der Reihe nach geordnet, ein Datumsvergleich genuegt.

**Wenn der Kalender nicht antworten kann** (die Bibliothek fehlt, der Kalender
wirft), wird nicht geraten. Der Kopf von `boersenkalender.py` verbietet genau
das ausdruecklich: "Was hier NICHT gemacht wird: eine Faustregel als
Rueckfallebene. Eine Naeherung, die nur dann greift, wenn die genaue Antwort
fehlt, waere die gefaehrlichste Variante von allen - sie wuerde genau in dem
Moment zuschlagen, in dem niemand mehr hinsieht." Stattdessen gilt hier die
sichere Schranke aus `abrufschutz` (`D 23:59:59`) UND der Lauf **meldet**,
dass er sie benutzt hat. Der Preis ist ein um einen Tag verspaetetes Signal;
der Gewinn ist, dass nie auf einer Teilkerze entschieden wird und dass die
Abweichung sichtbar ist statt still.

------------------------------------------------------------------------------
Die Startzeit: EIN Wert fuer den ganzen Lauf
------------------------------------------------------------------------------
Ein Wert, der sich waehrend des Laufs aendert, erzeugt innerhalb desselben
Laufs **verschiedene** Entscheidungskerzen. Bei 25 Symbolen ueber eine
Stundengrenze hinweg bekaemen die ersten Symbole Kerze N und die restlichen
Kerze N+1 - und weil alle neun Bots ihr Positionslimit laufend
hochzaehlen (`open_count += 1`), haengt das Ergebnis dann auch noch von der
Reihenfolge der Symbole ab.

Deshalb: `laufbeginn()` merkt sich den Zeitpunkt beim **ersten** Gebrauch im
Prozess und gibt danach immer denselben zurueck. Jede Funktion hier nimmt
`startzeit` zusaetzlich als Argument - das ist der Weg fuer Selbsttests und
fuer ein nachgestelltes Wiederholen eines Laufs.

**Bewusst KEINE Umgebungsvariable.** Ein `export`, das jemand einmal in sein
Shell-Profil schreibt und vergisst, wuerde alle neun Bots dauerhaft auf einer
alten Kerze einfrieren - lautlos, denn ein eingefrorener Lauf sieht in den
Zahlen genauso aus wie "kein Signal". Eine Bequemlichkeit, deren Fehlerfall
unsichtbar ist, ist den Gewinn nicht wert.

------------------------------------------------------------------------------
Die Quelle: `data/` mit Rueckfall - Entscheidung des Betreibers, 15.09.2026
------------------------------------------------------------------------------
    Die Forward-Tests lesen `data/` statt live abzurufen. Ist der Stand nicht
    frisch - die letzte abgeschlossene Kerze fehlt -, faellt der Bot auf den
    Live-Abruf zurueck und meldet das.

Die Abwaegung dahinter, damit sie nicht wieder aufgemacht wird:

| Variante   | Warum verworfen                                              |
|------------|--------------------------------------------------------------|
| nur melden | Der Cron faellt aus, die Bots handeln auf altem Stand, eine  |
|            | Mail meldet es - **dieselbe Luecke, die TB-34 aufgedeckt     |
|            | hat**, nur mit Benachrichtigung.                             |
| blockieren | verstoesst gegen "Der Live-Betrieb darf nie blockiert        |
|            | werden"; ein ausgefallener Abruf legt neun Bots still.       |
| Rueckfall  | Betrieb bleibt, Abweichung wird **sichtbar** statt still.    |

**Der Rueckfall-Abruf unterliegt derselben Regel.** Haette der Ausnahmefall
ein anderes Verhalten als der Normalfall, waere ausgerechnet der Fall
ungeprueft, den niemand ansieht. Deshalb laeuft der gefilterte Weg fuer beide
Quellen durch dieselben zwei Zeilen.

------------------------------------------------------------------------------
Die Meldung: dieselbe Leitung wie TB-32, dieselbe Daempfung
------------------------------------------------------------------------------
Eine Meldung, die in einer Protokollzeile landet, ist keine Meldung -
`logs/` sieht niemand an. TB-32 hat fuer genau diese Einsicht eine Leitung
gebaut, und zwar **ohne** eine zweite Telegram-Anbindung: das bestehende
`notify.send_alert()`. Diese Schicht benutzt dieselbe.

Sie benutzt auch dieselbe **Daempfung** - und zwar die Funktionen aus
`notifications/waechter_melden.py`, nicht eine zweite Fassung derselben vier
Regeln (neu / geaendert / Nachholung / Erinnerung nach 7 Tagen). Ohne
Daempfung waere die Meldung bei dauerhaft veraltetem `data/` eine Nachricht
je Bot und Lauf, also mehrere am Tag, dauerhaft - und damit nach einer Woche
dasselbe wie keine Meldung.

Drei harte Bedingungen, alle aus TB-32 uebernommen:

1. **Der Meldeteil bringt den Bot nie zum Scheitern.** Er steht vollstaendig
   in einem `try`; ein Sendefehler wird protokolliert, nicht weitergereicht.
2. **Ein fehlgeschlagener Versand gilt als NICHT zugestellt** und wird beim
   naechsten Lauf nachgeholt.
3. **Genau einmal je Lauf.** Gesammelt wird ueber alle Symbole, gesendet wird
   eine Nachricht mit der Gesamtzahl - nicht 25.

Fehlt `notifications/` (oder `waechter_melden`), wird **ungedaempft**
gemeldet statt gar nicht: eine Nachricht zu viel, nie eine verschluckte -
dieselbe sichere Richtung wie bei einer verlorenen Zustandsdatei in TB-32.

------------------------------------------------------------------------------
Gebrauch in einem `forward_test.py`
------------------------------------------------------------------------------
    from entscheidungskerze import lade, melde, KRYPTO

    df = lade(symbol, INTERVAL, KRYPTO,
              abruf=lambda: fetch_historical_data(symbol, INTERVAL, LOOKBACK))
    ...
    melde()          # einmal am Ende des Laufs

`df` endet damit auf der Entscheidungskerze. `df.iloc[-1]` bleibt stehen und
bedeutet ab jetzt das, was es immer bedeuten sollte.

Als Werkzeug:
    python3 shared/entscheidungskerze.py            # prueft data/ auf Frische
    python3 shared/entscheidungskerze.py --stand "2026-09-15 12:00:00"
"""

import argparse
import datetime as dt
import json
import os
import sys

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

import abrufschutz                                          # noqa: E402
from kursdaten import entferne_unvollstaendige              # noqa: E402

# Die Laengen der Kerzenzeitraeume. EINE Tabelle im ganzen Projekt - sie
# kommt ueber `abrufschutz` aus `binance_historie`.
INTERVALL_MS = abrufschutz.INTERVALL_MS

ZEITSPALTE = abrufschutz.ZEITSPALTE

# Die beiden Maerkte. Sie unterscheiden sich in genau einem Punkt: wann der
# Zeitraum einer Kerze zu Ende ist (siehe Modulkopf).
KRYPTO = "krypto"
AKTIEN = "aktien"
MAERKTE = (KRYPTO, AKTIEN)

STANDARD_DATENORDNER = os.path.join(BASE_DIR, "data")

# Woher der Rueckfall kam - die drei Gruende, getrennt gefuehrt, weil sie
# verschiedene Abhilfen haben.
FEHLT = "datei_fehlt"              # data/<symbol>_<intervall>.csv gibt es nicht
VERALTET = "veraltet"              # die letzte abgeschlossene Kerze fehlt
UNKLAR = "frische_unklar"          # der Boersenkalender konnte nicht antworten

# Der Zustand der Meldedaempfung. Neben `notifications/waechter_zustand.json`,
# nicht darin: ein gemeinsamer Schluesselraum waere eine Verwechslung, die
# beim Aufraeumen einer der beiden Seiten die andere still mitnimmt.
ZUSTAND_DATEI = os.path.join(BASE_DIR, "notifications",
                             "rueckfall_zustand.json")


# ===========================================================================
# Teil 1 - Die Startzeit des Laufs
# ===========================================================================
_LAUFBEGINN = None


def laufbeginn(startzeit=None):
    """Die Startzeit dieses Laufs - EIN Wert, so lange der Prozess lebt.

    Wird `startzeit` uebergeben, gilt sie fuer diesen einen Aufruf und
    aendert den gemerkten Wert NICHT. So kann ein Selbsttest eine Zeit
    vorgeben, ohne den Zustand des Prozesses umzuschreiben.
    """
    global _LAUFBEGINN
    if startzeit is not None:
        return _als_zeitpunkt(startzeit)
    if _LAUFBEGINN is None:
        _LAUFBEGINN = abrufschutz.jetzt_utc()
    return _LAUFBEGINN


def setze_laufbeginn(zeitpunkt):
    """Den Laufbeginn ausdruecklich festlegen. Fuer Selbsttests und fuer das
    nachgestellte Wiederholen eines Laufs - nicht fuer den Cronjob."""
    global _LAUFBEGINN
    _LAUFBEGINN = _als_zeitpunkt(zeitpunkt) if zeitpunkt is not None else None
    return _LAUFBEGINN


def laufbeginn_zuruecksetzen():
    """Nur fuer Selbsttests: der naechste Gebrauch merkt sich neu."""
    global _LAUFBEGINN
    _LAUFBEGINN = None


def _als_zeitpunkt(wert):
    """Beliebige Schreibweise -> naiver UTC-Zeitpunkt.

    Naiv und in UTC, weil die Kursdateien dieses Repos ihre Zeitstempel so
    fuehren und `abrufschutz.jetzt_utc()` sie so liest. Eine ortszeitbehaftete
    Auslegung waere im Sommer zwei Stunden daneben - genug, um eine laufende
    Kerze fuer abgeschlossen zu halten.
    """
    if isinstance(wert, dt.datetime):
        if wert.tzinfo is not None:
            return wert.astimezone(dt.timezone.utc).replace(tzinfo=None)
        return wert
    if isinstance(wert, str):
        text = wert.strip().replace(" ", "T")
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return _als_zeitpunkt(dt.datetime.fromisoformat(text))
    raise TypeError(f"Startzeit nicht lesbar: {wert!r}")


# ===========================================================================
# Teil 2 - Die Regel
# ===========================================================================
def _stand_fuer_abrufschutz(startzeit):
    """`schluss < startzeit`  <=>  `schluss <= startzeit - 1 ms`.

    `abrufschutz.abgeschlossen_maske` vergleicht mit `<=`, diese Schicht
    verlangt ein striktes `<` (siehe Modulkopf: eine Kerze, deren
    `close_time` GENAU auf der Startzeit liegt, wird nicht genommen). Der
    Unterschied ist genau eine Millisekunde, und er wird hier - an EINER
    Stelle - in die Startzeit hineingerechnet, statt die Regel drueben zu
    aendern. `abrufschutz` bleibt damit unberuehrt und der Schreibpfad
    unveraendert.
    """
    return startzeit - dt.timedelta(milliseconds=1)


def letzter_handelstag(startzeit, kalender=None):
    """(Datum der letzten geschlossenen NYSE-Sitzung, Grund) - oder (None, …).

    Genau EINE Kalenderabfrage je Lauf. `boersenkalender.status()` liefert
    `letzter_handelstag` bereits als "die letzte Sitzung, deren
    `market_close <= jetzt` liegt" - also genau die gesuchte Groesse,
    einschliesslich Feiertagen, verkuerzten Handelstagen und der
    US-Zeitumstellung.

    Wirft nie. Kann der Kalender nicht antworten, kommt `(None, Grund)`
    zurueck; der Aufrufer faellt dann auf die sichere Schranke aus
    `abrufschutz` zurueck und MELDET das (siehe Modulkopf).
    """
    if kalender is None:
        kalender = _boersenkalender()
    if kalender is None:
        return None, ("Der Boersenkalender liess sich nicht einbinden "
                      "(notifications/boersenkalender.py bzw. "
                      "pandas_market_calendars fehlt).")
    try:
        zustand = kalender.status(startzeit)
    except Exception as fehler:                             # noqa: BLE001
        return None, f"Der Boersenkalender warf {type(fehler).__name__}: {fehler}"
    tag = zustand.get("letzter_handelstag")
    if not tag:
        return None, (zustand.get("grund")
                      or "Der Boersenkalender nennt keinen letzten Handelstag.")
    return tag, None


def _boersenkalender():
    """`notifications/boersenkalender` - oder None, wenn er nicht da ist.

    Spaet und in einem `try`: dieses Modul laeuft im Live-Pfad von neun Bots,
    und ein Importfehler in einer Beobachtungsebene darf keinen Bot anhalten.
    """
    ordner = os.path.join(BASE_DIR, "notifications")
    if ordner not in sys.path:
        sys.path.insert(0, ordner)
    try:
        import boersenkalender                              # noqa: PLC0415
        return boersenkalender
    except Exception:                                       # noqa: BLE001
        return None


def entscheidbar_maske(df, intervall, markt, startzeit=None, kalender=None):
    """(Maske, Hinweis) - True je Zeile, deren Zeitraum vor `startzeit` endete.

    Krypto: die Regel kommt unveraendert aus `abrufschutz` (verschobene
    Startzeit, siehe `_stand_fuer_abrufschutz`).

    Aktien: der Schluss ist der echte Sitzungsschluss. Verglichen wird das
    Datum gegen den letzten geschlossenen Handelstag - eine Kalenderabfrage,
    nicht eine je Zeile.

    `Hinweis` ist None im Normalfall und ein Klartext-Grund, wenn fuer Aktien
    auf die sichere Schranke aus `abrufschutz` zurueckgefallen werden musste.
    """
    import pandas as pd                                     # noqa: PLC0415

    if markt not in MAERKTE:
        raise ValueError(f"Unbekannter Markt {markt!r}. Bekannt: "
                         f"{', '.join(MAERKTE)}.")
    if df is None or len(df) == 0:
        return None, None

    startzeit = laufbeginn(startzeit)

    if markt == KRYPTO:
        maske = abrufschutz.abgeschlossen_maske(
            df, intervall, stand=_stand_fuer_abrufschutz(startzeit))
        return maske, None

    # --- Aktien -----------------------------------------------------------
    if intervall != "1d":
        raise ValueError(
            f"Fuer Aktien ist nur das Tagesintervall vorgesehen, nicht "
            f"{intervall!r}. Alle vier Aktien-Bots handeln Tageskerzen; ein "
            f"anderes Intervall haette hier keinen Sitzungsschluss, an dem "
            f"sich der Kerzenschluss festmachen liesse.")

    tag, grund = letzter_handelstag(startzeit, kalender)
    if tag is None:
        # Keine Naeherung, sondern die sichere Schranke des Schreibpfads -
        # plus eine Meldung. Siehe Modulkopf.
        maske = abrufschutz.abgeschlossen_maske(
            df, intervall, stand=_stand_fuer_abrufschutz(startzeit))
        return maske, grund

    grenze_ms = abrufschutz.als_ms(_als_zeitpunkt(f"{tag}T00:00:00"))
    oeffnung = abrufschutz.oeffnungszeiten_ms(df[ZEITSPALTE])
    maske = oeffnung <= grenze_ms
    if not isinstance(maske, pd.Series):
        maske = pd.Series(maske, index=df.index)
    # Ein unlesbarer Zeitstempel gilt NICHT als entscheidbar - nichts zu
    # wissen ist kein Grund, etwas durchzulassen (wie in `abrufschutz`).
    return maske.fillna(False).astype(bool), None


def nur_entscheidbar(df, intervall, markt, startzeit=None, symbol=None,
                     melden=True, kalender=None):
    """(df bis einschliesslich Entscheidungskerze, verworfene Zeilen, Hinweis).

    Streicht und ZAEHLT - derselbe Grundsatz wie in `shared/kursdaten.py` und
    `shared/abrufschutz.py`: ein stillschweigend gestrichener Datenpunkt ist
    dasselbe Problem in Gruen.

    Die Rueckgabe ist eine ZEILENAUSWAHL der uebergebenen Tabelle; keine
    Spalte wird umgeschrieben, keine Zahl neu formatiert.
    """
    if df is None or len(df) == 0:
        return df, 0, None

    maske, hinweis = entscheidbar_maske(df, intervall, markt, startzeit,
                                        kalender)
    if maske is None:
        return df, 0, hinweis

    verworfen = int((~maske).sum())
    if verworfen == 0:
        return df, 0, hinweis

    # Nach Position auswaehlen, nicht ueber den Index: ein DataFrame mit
    # doppelten Indexwerten wuerde bei einer index-behafteten Maske nicht das
    # tun, wonach es aussieht.
    behalten = df[maske.to_numpy()]
    if melden:
        name = f"{symbol}: " if symbol else ""
        print(f"    Hinweis: {name}{verworfen} Kerze(n) nach der "
              f"Entscheidungskerze verworfen (von {len(df)}, Intervall "
              f"{intervall}, {markt}). Entschieden wird auf der letzten "
              f"Kerze, deren Zeitraum vor {laufbeginn(startzeit)} endete.")
    return behalten, verworfen, hinweis


def entscheidungskerze(df, intervall, markt, startzeit=None, kalender=None):
    """Die eine Zeile, auf der entschieden wird - oder None.

    Gedacht zum Nachsehen und fuer Selbsttests. Die Bots arbeiten mit
    `lade()` bzw. `nur_entscheidbar()` und behalten ihre Vorgeschichte, weil
    ihre Indikatoren sie brauchen.
    """
    gefiltert, _verworfen, _hinweis = nur_entscheidbar(
        df, intervall, markt, startzeit, melden=False, kalender=kalender)
    if gefiltert is None or len(gefiltert) == 0:
        return None
    return gefiltert.iloc[-1]


# ===========================================================================
# Teil 3 - Ist `data/` frisch genug?
# ===========================================================================
def erwartete_letzte_oeffnung(intervall, markt, startzeit=None, kalender=None):
    """(`open_time` der erwarteten Entscheidungskerze in ms, Grund) - oder
    (None, Grund), wenn sich das nicht sagen laesst.

    Krypto: reine Rechnung auf dem Zeitraster. Gesucht ist das groesste
    `o = k * L` mit `o + L <= startzeit`, also `o = (S // L - 1) * L`.
    Binance-Kerzen liegen auf diesem Raster (1h/4h/1d, UTC), und die aus
    ihnen abgeleiteten Tageskerzen (`shared/build_daily_crypto_data.py`)
    ebenfalls.

    Aktien: der letzte geschlossene Handelstag laut Kalender.
    """
    if intervall not in INTERVALL_MS:
        raise ValueError(f"Unbekanntes Intervall {intervall!r}. Bekannt: "
                         f"{', '.join(sorted(INTERVALL_MS))}.")
    startzeit = laufbeginn(startzeit)

    if markt == KRYPTO:
        laenge = INTERVALL_MS[intervall]
        stand_ms = abrufschutz.als_ms(startzeit)
        return (stand_ms // laenge - 1) * laenge, None

    if markt != AKTIEN:
        raise ValueError(f"Unbekannter Markt {markt!r}.")

    tag, grund = letzter_handelstag(startzeit, kalender)
    if tag is None:
        return None, grund
    return abrufschutz.als_ms(_als_zeitpunkt(f"{tag}T00:00:00")), None


def ist_frisch(df, intervall, markt, startzeit=None, kalender=None):
    """(True | False | None, Grund) - traegt `data/` die erwartete Kerze?

    `None` heisst "nicht feststellbar" und wird vom Aufrufer wie "nicht
    frisch" behandelt, aber mit eigenem Grund gemeldet: eine unbeantwortbare
    Frage ist etwas anderes als eine mit "nein" beantwortete, und sie
    verlangt eine andere Abhilfe.
    """
    if df is None or len(df) == 0:
        return False, "Die Kursdatei enthaelt keine Zeile."

    erwartet, grund = erwartete_letzte_oeffnung(intervall, markt, startzeit,
                                                kalender)
    if erwartet is None:
        return None, grund

    oeffnung = abrufschutz.oeffnungszeiten_ms(df[ZEITSPALTE])
    vorhanden = oeffnung.max()
    if vorhanden != vorhanden:                              # NaN
        return None, (f"Die Spalte {ZEITSPALTE!r} enthaelt keinen lesbaren "
                      f"Zeitstempel.")
    if vorhanden >= erwartet:
        return True, None
    fehlend = _lesbar(erwartet, intervall)
    hat = _lesbar(vorhanden, intervall)
    return False, (f"letzte Kerze in data/ ist {hat}, erwartet war "
                   f"{fehlend}")


def _lesbar(millisekunden, intervall):
    """Millisekunden -> die Schreibweise, in der die Kursdateien sie fuehren."""
    try:
        zeit = dt.datetime(1970, 1, 1) + dt.timedelta(
            milliseconds=float(millisekunden))
    except (TypeError, ValueError, OverflowError):
        return str(millisekunden)
    return zeit.strftime("%Y-%m-%d" if intervall == "1d"
                         else "%Y-%m-%d %H:%M:%S")


# ===========================================================================
# Teil 4 - Die Tuer: data/ mit Rueckfall
# ===========================================================================
class Sammler:
    """Sammelt die Rueckfaelle EINES Laufs, damit am Ende EINE Meldung steht.

    Nicht 25 Nachrichten fuer 25 Symbole: eine Nachricht, die die Symbole
    nennt. Derselbe Gedanke wie `kursdaten.Zaehler` - nur dass es hier nicht
    beim Protokoll bleibt.
    """

    def __init__(self):
        self.je_symbol = {}     # symbol -> (art, grund)
        self.kalenderhinweise = set()

    def erfasse(self, symbol, art, grund):
        self.je_symbol[symbol] = (art, grund)

    def erfasse_kalenderhinweis(self, hinweis):
        if hinweis:
            self.kalenderhinweise.add(hinweis)

    @property
    def leer(self):
        return not self.je_symbol and not self.kalenderhinweise

    def kernzeilen(self):
        """Die Zeilen, die die Daempfung vergleicht - OHNE Zeitstempel.

        Genau wie in TB-32: verglichen wird, was gesendet wuerde. Stuende
        hier eine Uhrzeit oder eine Symbolzahl, die sich taeglich aendert,
        waere der Fingerabdruck jeden Tag ein anderer und die Daempfung
        griffe nie.
        """
        zeilen = []
        for art in (FEHLT, VERALTET, UNKLAR):
            betroffen = sorted(s for s, (a, _g) in self.je_symbol.items()
                               if a == art)
            if betroffen:
                zeilen.append(f"{_ART_TEXT[art]}: {', '.join(betroffen)}")
        for hinweis in sorted(self.kalenderhinweise):
            zeilen.append(f"Boersenkalender: {hinweis}")
        return zeilen


_ART_TEXT = {
    FEHLT: "Kursdatei fehlt in data/",
    VERALTET: "data/ veraltet",
    UNKLAR: "Frische nicht feststellbar",
}

# Der Sammler dieses Prozesses. Ein Modulwert, damit der Eingriff je
# `forward_test.py` bei drei Zeilen bleibt - der Bot soll kein Objekt
# durchreichen muessen, das ihn sonst nichts angeht.
SAMMLER = Sammler()


def sammler_zuruecksetzen():
    """Nur fuer Selbsttests."""
    global SAMMLER
    SAMMLER = Sammler()
    return SAMMLER


def lade(symbol, intervall, markt, abruf, datenordner=None, startzeit=None,
         sammler=None, melden=True, kalender=None):
    """Die Kursdaten, auf denen dieser Lauf entscheidet.

    Reihenfolge - und jede Stufe hat ihren Grund:

    1. `data/<symbol>_<intervall>.csv` lesen.
    2. Kerzen ohne Kurse streichen (`kursdaten.entferne_unvollstaendige`) -
       sonst wird aus einem Zeitausstieg ein `NaN`, und das vergiftet jede
       danach berechnete Kapitalzeile, ohne Fehlermeldung.
    3. Frische pruefen. Fehlt die erwartete Entscheidungskerze, wird `abruf()`
       gerufen - der bisherige Live-Abruf des Bots, unveraendert.
    4. **Auf beide Quellen dieselbe Regel anwenden.** Der Ausnahmefall darf
       sich nicht anders verhalten als der Normalfall.

    `abruf` ist eine Funktion ohne Argumente. Die neun Bots rufen ihren
    Endpunkt verschieden (Binance mit `lookback`, yfinance mit `period`);
    diese Schicht muss das nicht wissen und soll es nicht wissen.
    """
    sammler = SAMMLER if sammler is None else sammler
    ordner = datenordner or STANDARD_DATENORDNER
    pfad = os.path.join(ordner, f"{symbol}_{intervall}.csv")

    df, art, grund = _aus_datei(pfad, symbol, intervall, markt, startzeit,
                                melden, kalender)

    if art is not None:
        sammler.erfasse(symbol, art, grund)
        if melden:
            print(f"    Rueckfall auf den Live-Abruf fuer {symbol}: "
                  f"{_ART_TEXT[art]} ({grund}).")
        df = abruf()
        df, _gestrichen = entferne_unvollstaendige(df, symbol=symbol,
                                                   melden=melden)

    gefiltert, _verworfen, hinweis = nur_entscheidbar(
        df, intervall, markt, startzeit, symbol=symbol, melden=melden,
        kalender=kalender)
    sammler.erfasse_kalenderhinweis(hinweis)
    return gefiltert


def _aus_datei(pfad, symbol, intervall, markt, startzeit, melden, kalender):
    """(df, Rueckfallart oder None, Grund). Liest, streicht, prueft Frische."""
    import pandas as pd                                     # noqa: PLC0415

    if not os.path.exists(pfad):
        return None, FEHLT, f"{os.path.basename(pfad)} gibt es nicht"

    try:
        df = pd.read_csv(pfad, parse_dates=[ZEITSPALTE])
    except Exception as fehler:                             # noqa: BLE001
        return None, FEHLT, (f"{os.path.basename(pfad)} nicht lesbar "
                             f"({type(fehler).__name__}: {fehler})")

    df, _gestrichen = entferne_unvollstaendige(df, symbol=symbol,
                                               melden=melden)

    frisch, grund = ist_frisch(df, intervall, markt, startzeit, kalender)
    if frisch is True:
        return df, None, None
    if frisch is None:
        return None, UNKLAR, grund
    return None, VERALTET, grund


# ===========================================================================
# Teil 5 - Die Meldung
# ===========================================================================
def _waechter_melden():
    """`notifications/waechter_melden` - oder None.

    Von dort kommen die vier Daempfungsregeln und das Lesen/Schreiben des
    Zustands. Sie sollen genau einmal existieren; eine zweite Fassung waere
    die Doppelfuehrung, die dieses Projekt schon Zahlen gekostet hat.
    """
    ordner = os.path.join(BASE_DIR, "notifications")
    if ordner not in sys.path:
        sys.path.insert(0, ordner)
    try:
        import waechter_melden                              # noqa: PLC0415
        return waechter_melden
    except Exception:                                       # noqa: BLE001
        return None


def _standard_senden(text):
    """Die EINE Telegram-Leitung des Projekts - keine zweite Anbindung.

    `parse_mode=None`: der Text enthaelt Dateinamen mit `_` und Symbolnamen.
    Telegrams Legacy-Markdown kennt kein Escaping; unformatiert ist die
    einzige Fassung, die bei jedem Inhalt richtig ankommt (dieselbe
    Begruendung wie in `waechter_melden._standard_senden`).
    """
    ordner = os.path.join(BASE_DIR, "notifications")
    if ordner not in sys.path:
        sys.path.insert(0, ordner)
    from notify import send_alert                           # noqa: PLC0415
    return send_alert(text, parse_mode=None)


def nachricht(bot, sammler, anlass=None):
    """Kurz genug fuers Telefon, vollstaendig genug zum Handeln."""
    zeilen = sammler.kernzeilen()
    anzahl = len(sammler.je_symbol)
    kopf = (f"[ABRUFSCHICHT] {bot}: {anzahl} Symbol(e) auf den Live-Abruf "
            f"zurueckgefallen." if anzahl else
            f"[ABRUFSCHICHT] {bot}: Hinweis zur Entscheidungskerze.")
    teile = [kopf, ""]
    teile.extend(zeilen)
    teile.append("")
    teile.append("Der Lauf ist NICHT ausgefallen - er hat live abgerufen und "
                 "dieselbe Entscheidungskerze benutzt wie aus data/. Gemeldet "
                 "wird, dass data/ nicht den Stand hatte, den der Lauf "
                 "brauchte.")
    teile.append("Abhilfe: den zustaendigen fetch_*.py laufen lassen (bzw. "
                 "als Cronjob eintragen) und mit "
                 "'python3 shared/entscheidungskerze.py' nachsehen.")
    if anlass:
        teile.append(f"({anlass})")
    return "\n".join(teile)


def melde(bot=None, sammler=None, senden=None, zustand_pfad=None, jetzt=None,
          hinweis=None):
    """Einmal je Lauf: melden, was an Rueckfaellen angefallen ist.

    Gibt den Anlass zurueck (`neu` / `geaendert` / `nachholung` /
    `erinnerung` / `gedaempft` / `still`) - die Selbsttests lesen ihn.

    **Diese Funktion bringt den Bot nie zum Scheitern.** Alles steht in einem
    `try`; ein Sendefehler wird nach `stderr` protokolliert und nicht
    weitergereicht.
    """
    sammler = SAMMLER if sammler is None else sammler
    bot = bot or _botname()
    try:
        return _melde(bot, sammler, senden, zustand_pfad, jetzt, hinweis)
    except Exception as fehler:                             # noqa: BLE001
        sys.stderr.write(
            f"[entscheidungskerze] Der Meldeteil ist gescheitert "
            f"({type(fehler).__name__}: {fehler}). Der Lauf selbst ist davon "
            f"unberuehrt; die Rueckfaelle stehen oben im Protokoll.\n")
        sys.stderr.flush()
        return None


def _botname():
    """Der Name des laufenden Bots - aus dem Ordner des Hauptskripts.

    `strategies/t3_supertrend/forward_test.py` -> `t3_supertrend`. Damit
    braucht der Eingriff im Bot kein zusaetzliches Argument, und der Name
    kann nicht von dem abweichen, unter dem der Bot sonst gefuehrt wird
    (`strategy_paths` leitet ihn genauso ab).
    """
    haupt = getattr(sys.modules.get("__main__"), "__file__", None)
    if not haupt:
        return "unbekannt"
    return os.path.basename(os.path.dirname(os.path.abspath(haupt)))


def _melde(bot, sammler, senden, zustand_pfad, jetzt, hinweis):
    wm = _waechter_melden()
    hinweis = hinweis if hinweis is not None else _hinweis
    pfad = zustand_pfad or ZUSTAND_DATEI

    if wm is None:
        # Ohne die Daempfung wird UNGEDAEMPFT gemeldet, nicht gar nicht:
        # eine Nachricht zu viel, nie eine verschluckte.
        if sammler.leer:
            return "still"
        hinweis("notifications/waechter_melden.py liess sich nicht einbinden - "
                "es wird ohne Wiederholungsdaempfung gemeldet.")
        _versuche_senden(senden or _standard_senden, nachricht(bot, sammler),
                         hinweis)
        return "ungedaempft"

    jetzt = jetzt or wm.jetzt_utc()
    vermerke = wm.zustand_lesen(pfad)
    vorher = vermerke.get(bot)

    zeilen = sammler.kernzeilen()
    klasse = wm.IN_ORDNUNG if sammler.leer else wm.BEFUND
    abdruck = _fingerabdruck(klasse, zeilen)

    # Ob gesendet wird, entscheidet AUSSCHLIESSLICH `wm.entscheidung()`.
    # Eine zweite Abfrage auf "ist der Sammler leer?" an dieser Stelle waere
    # bequem und gefaehrlich: sie wuerde das Fehlen der ersten verdecken.
    melden, anlass = wm.entscheidung(klasse, abdruck, vorher, jetzt)

    gesendet = False
    if melden:
        gesendet = _versuche_senden(senden or _standard_senden,
                                    nachricht(bot, sammler, anlass), hinweis)

    if klasse == wm.IN_ORDNUNG:
        # Es steht nichts mehr offen - der Vermerk wird geraeumt, damit ein
        # spaeter wiederkehrender Rueckfall wieder als "neu" gilt.
        if vorher:
            vermerke.pop(bot, None)
            wm.zustand_schreiben(pfad, vermerke)
        return anlass

    fortsetzung = bool(vorher) and vorher.get("fingerabdruck") == abdruck
    if gesendet:
        gemeldet_am = wm._zeit_schreiben(jetzt)
    elif fortsetzung:
        # Ein fehlgeschlagener Versand darf den Zeitpunkt NICHT vorruecken.
        gemeldet_am = vorher.get("zuletzt_gemeldet_am")
    else:
        # Neu oder geaendert und nicht zugestellt: ausdruecklich offen -
        # daraus wird beim naechsten Lauf die Nachholung.
        gemeldet_am = None

    vermerke[bot] = {
        "klasse": klasse,
        "fingerabdruck": abdruck,
        "zeilen": zeilen,
        "erstmals_am": (vorher.get("erstmals_am") if fortsetzung
                        else wm._zeit_schreiben(jetzt)) or wm._zeit_schreiben(jetzt),
        "zuletzt_gesehen_am": wm._zeit_schreiben(jetzt),
        "zuletzt_gemeldet_am": gemeldet_am,
        "laeufe": (vorher.get("laeufe", 0) + 1) if fortsetzung else 1,
    }
    wm.zustand_schreiben(pfad, vermerke)
    return anlass


def _fingerabdruck(klasse, zeilen):
    """Der Daempfungsschluessel: genau das, was gesendet wuerde.

    Bewusst ohne Zeitstempel und ohne Laufzeiten - ein Fingerabdruck darueber
    waere jeden Tag ein anderer, und die Daempfung griffe nie (TB-32).
    """
    import hashlib                                          # noqa: PLC0415
    roh = "|".join([klasse] + list(zeilen))
    return hashlib.sha256(roh.encode("utf-8")).hexdigest()[:16]


def _versuche_senden(senden, text, hinweis):
    """Ein Sendefehler wird protokolliert, nicht weitergereicht."""
    try:
        return bool(senden(text))
    except Exception as fehler:                             # noqa: BLE001
        hinweis(f"Der Versand ist gescheitert ({type(fehler).__name__}: "
                f"{fehler}). Die Meldung gilt als NICHT zugestellt und wird "
                f"beim naechsten Lauf erneut versucht.")
        return False


def _hinweis(text):
    """Geht ins Log des Bots, nicht nach Telegram."""
    sys.stderr.write(f"[entscheidungskerze] {text}\n")
    sys.stderr.flush()


# ===========================================================================
# Kommandozeile - nachsehen, ohne einen Bot zu starten
# ===========================================================================
_BOTS = [
    # (Bot, Intervall, Markt) - dieselbe Zuordnung wie in den neun
    # forward_test.py. Sie steht hier NUR fuer das Werkzeug; kein Bot liest
    # sie, und keine Handelszahl haengt daran.
    ("elliott_wave", "1h", KRYPTO),
    ("t3_supertrend", "4h", KRYPTO),
    ("rsi2_crypto", "1d", KRYPTO),
    ("turtle_soup_crypto", "1d", KRYPTO),
    ("volatility_breakout_crypto", "1d", KRYPTO),
    ("elliott_wave_stocks", "1d", AKTIEN),
    ("rsi2_mean_reversion", "1d", AKTIEN),
    ("turtle_soup_stocks", "1d", AKTIEN),
    ("volatility_breakout", "1d", AKTIEN),
]


# Krypto oder Aktie? Der Dateiname ist alles, was der Ordner hergibt.
# Alle 25 Krypto-Symbole dieses Projekts sind USDT-Paare
# (`shared/symbols_config.py`), alle Aktien sind S&P-500-Kuerzel. Diese
# Unterscheidung gilt AUSSCHLIESSLICH fuer dieses Werkzeug - kein Bot
# benutzt sie, jeder von ihnen sagt seinen Markt selbst (`lade(..., markt)`).
KRYPTO_ENDUNG = "USDT"


def markt_aus_symbol(symbol):
    return KRYPTO if symbol.upper().endswith(KRYPTO_ENDUNG) else AKTIEN


def _pruefe_ordner(ordner, startzeit):
    """Je Kursdatei: traegt sie die erwartete Entscheidungskerze? Rein lesend."""
    import glob                                             # noqa: PLC0415
    import pandas as pd                                     # noqa: PLC0415

    befunde = []
    for intervall in sorted(INTERVALL_MS):
        for pfad in sorted(glob.glob(os.path.join(ordner,
                                                  f"*_{intervall}.csv"))):
            name = os.path.basename(pfad)
            symbol = name[: -len(f"_{intervall}.csv")]
            markt = markt_aus_symbol(symbol)
            try:
                df = pd.read_csv(pfad, parse_dates=[ZEITSPALTE])
            except Exception as fehler:                     # noqa: BLE001
                befunde.append({"datei": name, "markt": markt, "frisch": None,
                                "grund": str(fehler)})
                continue
            df, _g = entferne_unvollstaendige(df, symbol=symbol, melden=False)
            frisch, grund = ist_frisch(df, intervall, markt, startzeit)
            if frisch is not True:
                befunde.append({"datei": name, "markt": markt,
                                "frisch": frisch, "grund": grund})
    return befunde

def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Traegt data/ die Kerze, auf der ein Lauf jetzt "
                    "entscheiden wuerde? Rein lesend.")
    zerleger.add_argument("--ordner", default=STANDARD_DATENORDNER)
    zerleger.add_argument("--stand", default=None,
                          help="Startzeit des gedachten Laufs (UTC), "
                               "Standard: jetzt")
    zerleger.add_argument("--json", metavar="PFAD", default=None)
    argumente = zerleger.parse_args(argv)

    startzeit = laufbeginn(argumente.stand)
    print(f"Startzeit des gedachten Laufs (UTC): {startzeit}")
    print(f"Ordner: {argumente.ordner}\n")

    print("Erwartete Entscheidungskerze je Bot:")
    unklar = False
    for bot, intervall, markt in _BOTS:
        erwartet, grund = erwartete_letzte_oeffnung(intervall, markt, startzeit)
        if erwartet is None:
            unklar = True
            print(f"  {bot:28} {intervall:3} {markt:7} nicht feststellbar - "
                  f"{grund}")
        else:
            print(f"  {bot:28} {intervall:3} {markt:7} "
                  f"{_lesbar(erwartet, intervall)}")

    import glob as _glob                                    # noqa: PLC0415
    gesamt = len(_glob.glob(os.path.join(argumente.ordner, "*.csv")))
    befunde = _pruefe_ordner(argumente.ordner, startzeit)

    print(f"\n{len(befunde)} von {gesamt} Kursdatei(en) ohne die erwartete "
          f"Kerze:")
    for markt in MAERKTE:
        betroffen = [b for b in befunde if b["markt"] == markt]
        if betroffen:
            print(f"  {markt}: {len(betroffen)}")
    for eintrag in sorted(befunde, key=lambda b: b["datei"])[:20]:
        print(f"  {eintrag['datei']:24} {eintrag['grund']}")
    if len(befunde) > 20:
        print(f"  ... und {len(befunde) - 20} weitere (vollstaendig mit "
              f"--json)")

    if argumente.json:
        with open(argumente.json, "w", encoding="utf-8") as datei:
            json.dump({"startzeit": str(startzeit), "befunde": befunde},
                      datei, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"\nJSON: {argumente.json}")

    if not befunde and not unklar:
        print("\nKein Befund: jeder Bot faende in data/ die Kerze, auf der er "
              "jetzt entscheiden wuerde.")
        return 0
    print("\nFuer diese Dateien faellt der zustaendige Bot auf den Live-Abruf "
          "zurueck und meldet das. Der Betrieb laeuft weiter.")
    # Rueckgabewert 1: ein Befund ist kein Fehler des Programms, aber etwas,
    # das ein Cronjob-Aufruf sichtbar machen soll (wie shared/kursdaten.py).
    return 1


if __name__ == "__main__":
    sys.exit(main())
