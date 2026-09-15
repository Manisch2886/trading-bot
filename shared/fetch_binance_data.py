"""
Krypto-Kursdaten von Binance holen - Code versioniert, Schluessel draussen
==============================================================================
Diese Datei war bis TB-37 **gitignoriert**. Sie enthielt die Zugangsdaten im
Klartext und existierte deshalb genau einmal: auf dem MacBook des Betreibers.
In keinem Commit, in keinem Zweig, auf keinem Server. **Neun** Module haengen
an ihr, **fuenf** davon im taeglichen Live-Betrieb - waere sie verlorengegangen,
haetten fuenf Bots gestanden, und niemand haette sie rekonstruieren koennen.

Der Schnitt von TB-37 trennt beides:

* **Der Code steht ab jetzt im Repo** - diese Datei.
* **Die Schluessel bleiben draussen** - sie kommen ausschliesslich aus der
  Umgebung (`os.environ`), ersatzweise aus einer unversionierten `.env` im
  Wurzelverzeichnis. `.env.beispiel` nennt die Namen, niemals die Werte.

In dieser Datei steht kein Schluessel, und sie gibt auch keinen aus. Weder in
einer Meldung noch in einer Ausnahme noch in einem Protokoll: was hier
berichtet wird, ist immer nur **ob** ein Name gesetzt ist, nie **was**
dahintersteht.

Warum Ersetzung und nicht eine zweite Datei
------------------------------------------------------------------------------
Die neun Aufrufer binden sie als `from fetch_binance_data import
fetch_historical_data` ein, aufgeloest ueber `shared/` in `sys.path`. Ein
zweites Modul neben dem alten haette also **jeden** dieser neun Aufrufer
geaendert - darunter fuenf `forward_test.py`, die den Live-Betrieb ausmachen.
Es haette ausserdem zwei Wege zu denselben Daten hinterlassen, und genau davon
hat dieses Projekt schon zu viele (siehe Uebergabeprotokoll Abschnitt 7:
jede Zahl genau einmal). Deshalb: **gleicher Pfad, gleicher Modulname,
gleiche Signatur** - und kein Aufrufer wird angefasst.

Fehlende Schluessel blockieren nichts - und schweigen auch nicht
------------------------------------------------------------------------------
Der Kursabruf laeuft ueber `/api/v3/klines`, einen **oeffentlichen** Endpunkt.
Er verlangt **keinen** Schluessel; zwei Nachbarmodule dieses Repos bauen ihren
Client schon immer ohne (`shared/get_top_symbols.py:15`,
`shared/fetch_multi_data.py:46`). Fuer den Datenpfad loest sich die Frage
damit auf, statt zu einer Abwaegung zu werden:

1. **Fehlt ein Schluessel, laeuft der Abruf trotzdem** - unangemeldet, mit
   vollem Ergebnis. Der Live-Betrieb wird nie blockiert.
2. **Er tut es nicht stillschweigend.** Einmal je Prozess geht eine Meldung
   nach `stderr`, die sagt, welcher Name fehlt und wo er hingehoert.
3. **Eine leere Antwort wird nie als Ergebnis zurueckgegeben**, sondern als
   `AbrufLeer` geworfen. Ein still geliefertes leeres Ergebnis waere der
   schlimmste Fall: es sieht in jedem Bot genauso aus wie "kein Signal" und
   faellt niemandem auf.
4. **Wer wirklich einen Schluessel braucht** (Kontostand, Orders - nichts
   davon passiert hier), bekommt von `verlange_zugangsdaten()` sofort ein
   `ZugangsdatenFehlen`. Laut, nicht leer.

Die Namen sind nicht erfunden - und der Schnitt schaerft eine zweite Wache
------------------------------------------------------------------------------
`broker/zugang.py:101` fuehrt seit jeher

    DATENABRUF_VARIABLEN = ("BINANCE_API_KEY", "BINANCE_API_SECRET")

und beschreibt sie als "die bestehenden Schluessel fuer den Kursdatenabruf
(shared/fetch_binance_data.py) - sie gehoeren zu einem ECHTEN Binance-Konto".
Die Namen hier sind also die im Repo bereits dokumentierten, nicht geraten;
`shared/test_fetch_binance_data.py` rechnet das gegen `broker/zugang.py` nach.

Daran haengt eine Nebenwirkung, die fuer sich genommen den Schnitt schon
lohnt: `broker/zugang.py.get_zugang()` bricht ab, wenn ein **Testnet**-
Schluessel mit einem dieser beiden uebereinstimmt - eine Verwechslungssperre
gegen den schlimmsten denkbaren Fehlgriff. Sie konnte bisher **nicht
greifen**: die echten Schluessel standen in einer Python-Datei, nicht in der
Umgebung, und `_aus_umgebung("BINANCE_API_KEY", ...)` fand nichts. Stehen sie
in der `.env`, findet die Sperre sie - und tut zum ersten Mal, wofuer sie
geschrieben wurde. `broker/` wird dafuer nicht angefasst.

Offener Punkt: dies ist der **dritte** Leser desselben `.env`-Formats, neben
`broker/zugang.py._parse_env_file` und `notifications/telegram_config.py`.
Zusammenzulegen waere richtig, wuerde aber `broker/` und `notifications/`
anfassen und gehoert deshalb nicht in TB-37. Der Selbsttest prueft immerhin
nach, dass dieser und der Leser in `broker/zugang.py` bei derselben Datei
zum selben Ergebnis kommen.

Was diese Datei ausdruecklich NICHT tut
------------------------------------------------------------------------------
* **Sie filtert die laufende Kerze nicht heraus.** Der Endpunkt liefert den
  gerade angefangenen Zeitraum mit, und das bleibt so: die fuenf
  `forward_test.py` lesen mit `df.iloc[-1]` genau diese Kerze, und die vier
  `fetch_*.py` schneiden sie ueber `abrufschutz.nur_abgeschlossene` selbst ab,
  **bevor** sie schreiben (TB-35). Wuerde hier gefiltert, waere `abrufschutz`
  wirkungslos und die Bots handelten auf einer anderen Kerze als bisher.
* **Sie sendet keine Orders.** Nur Marktdaten, nur lesend. Order-Code steht in
  diesem Projekt ausschliesslich unter `broker/`.
* **Sie fasst `data/` nicht an.** Das Schreiben machen die Aufrufer.

Rueckgabeform - der Vertrag mit neun Modulen
------------------------------------------------------------------------------
Ein `DataFrame` mit **genau** diesen sechs Spalten in dieser Reihenfolge:

    open_time, open, high, low, close, volume

`open_time` ist ein zeitzonenfreier UTC-Zeitstempel, die uebrigen fuenf sind
`float`. Das ist nicht beliebig: `to_csv` schreibt eine solche Spalte als
`2017-08-17 04:00:00` und, wenn alle Werte auf Mitternacht liegen, als
`2017-08-17` - also genau so, wie die Dateien unter `data/` aussehen. Eine
andere Schreibweise aendert den Datenstand-Hash der Vorregistrierung, ohne
dass ein einziger Kurs anders waere.

`close_time` kommt bewusst **nicht** mit: es steht in keiner Kursdatei dieses
Repos, und `shared/abrufschutz.py` rechnet den Kerzenschluss deshalb aus
`open_time` und Intervall aus.

Nutzung
------------------------------------------------------------------------------
    from fetch_binance_data import fetch_historical_data
    df = fetch_historical_data("BTCUSDT", "1d", "400 day ago UTC")

Einrichtung der Schluessel: `.env.beispiel` nach `.env` kopieren und die Werte
eintragen. `.env` ist gitignoriert und bleibt es.
"""

import os
import sys

# Die sechs Spalten der Kursdateien dieses Repos - in dieser Reihenfolge.
SPALTEN = ["open_time", "open", "high", "low", "close", "volume"]

# Die Namen, unter denen die Zugangsdaten in der Umgebung stehen. Hier steht
# der NAME, nirgends der Wert. `.env.beispiel` nennt dieselben zwei Namen.
SCHLUESSEL_NAME = "BINANCE_API_KEY"
GEHEIMNIS_NAME = "BINANCE_API_SECRET"

# Der Ort der unversionierten `.env` - Wurzelverzeichnis des Repos, also eine
# Ebene ueber `shared/`.
_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(_SHARED_DIR)
ENV_DATEI = os.path.join(_WURZEL, ".env")

# Wurde in diesem Prozess schon gemeldet, dass Schluessel fehlen? Einmal ist
# ein Hinweis, je Symbol waere Laerm - und Laerm wird ueberlesen.
_GEWARNT = False


class ZugangsdatenFehlen(RuntimeError):
    """Ein Schluessel wird gebraucht, steht aber nicht in der Umgebung.

    Wird vom Kursabruf NICHT geworfen - der braucht keinen. Sie ist fuer
    alles gedacht, was ohne Anmeldung wirklich nicht geht.
    """


class AbrufLeer(RuntimeError):
    """Der Endpunkt hat fuer diese Anfrage keine einzige Kerze geliefert.

    Bewusst eine Ausnahme und kein leeres Ergebnis: ein leeres Ergebnis sieht
    in jedem der neun Aufrufer genauso aus wie "kein Signal" und faellt
    niemandem auf. Alle neun fangen `Exception` je Symbol ab und machen mit
    dem naechsten weiter - der Lauf bricht also nicht ab, aber die Zeile
    steht im Protokoll.
    """


# ---------------------------------------------------------------------------
# Schluessel aus der Umgebung - niemals aus dieser Datei
# ---------------------------------------------------------------------------
def lies_env(pfad=None):
    """Die unversionierte `.env` lesen: `NAME=WERT` je Zeile.

    Absichtlich von Hand und ohne zusaetzliche Abhaengigkeit - es sind
    zwanzig Zeilen, und `requirements.txt` um ein Paket zu erweitern, damit
    zwei Namen gelesen werden koennen, waere ein schlechter Tausch.

    Leerzeilen und `#`-Zeilen werden uebergangen, ein fuehrendes `export`
    ebenso, Anfuehrungszeichen um den Wert werden entfernt. Fehlt die Datei,
    ist das **kein** Fehler: dann stehen die Namen vielleicht direkt in der
    Umgebung, und im Zweifel laeuft der Abruf auch ganz ohne.

    Rueckgabe: ein `dict`. Die Werte werden hier gelesen, aber nirgends
    ausgegeben.
    """
    ziel = pfad if pfad is not None else ENV_DATEI
    werte = {}
    try:
        with open(ziel, "r", encoding="utf-8") as datei:
            zeilen = datei.readlines()
    except (OSError, UnicodeDecodeError):
        return werte

    for zeile in zeilen:
        gestutzt = zeile.strip()
        if not gestutzt or gestutzt.startswith("#") or "=" not in gestutzt:
            continue
        if gestutzt.startswith("export "):
            gestutzt = gestutzt[len("export "):].lstrip()
        name, _, wert = gestutzt.partition("=")
        name = name.strip()
        if not name:
            continue
        wert = wert.strip()
        if len(wert) >= 2 and wert[0] == wert[-1] and wert[0] in ("'", '"'):
            wert = wert[1:-1]
        werte[name] = wert
    return werte


def aus_umgebung(name, aus_datei, umgebung=None):
    """Erst die Umgebung, dann die `.env`.

    Zeichengleich mit `broker/zugang.py._aus_umgebung` - dieselbe Reihenfolge
    im ganzen Projekt. Was in der Umgebung steht, gewinnt: wer einen
    Schluessel fuer einen einzelnen Lauf vorne an die Befehlszeile setzt, soll
    nicht von einer Datei ueberstimmt werden, die er gerade nicht im Blick
    hat.

    Es wird ausdruecklich **nichts in `os.environ` geschrieben**. Die `.env`
    dieses Projekts traegt auch Telegram- und Testnet-Angaben; sie alle
    nebenbei in die Umgebung zu heben, waere eine Nebenwirkung, die niemand
    bestellt hat - und sie erbte jeder Unterprozess mit.
    """
    ziel = os.environ if umgebung is None else umgebung
    return ziel.get(name) or aus_datei.get(name)


def zugangsdaten(umgebung=None, pfad=None):
    """Schluessel und Geheimnis - oder `(None, None)`, wenn sie fehlen.

    Ein leerer Wert zaehlt als nicht gesetzt: `BINANCE_API_KEY=` in der `.env`
    ist ein vergessener Eintrag, kein Schluessel.
    """
    aus_datei = lies_env(pfad)
    schluessel = (aus_umgebung(SCHLUESSEL_NAME, aus_datei, umgebung)
                  or "").strip() or None
    geheimnis = (aus_umgebung(GEHEIMNIS_NAME, aus_datei, umgebung)
                 or "").strip() or None
    return schluessel, geheimnis


def fehlende_namen(umgebung=None, pfad=None):
    """Welche der beiden Namen fehlen? Gibt Namen zurueck, nie Werte."""
    schluessel, geheimnis = zugangsdaten(umgebung, pfad)
    fehlt = []
    if not schluessel:
        fehlt.append(SCHLUESSEL_NAME)
    if not geheimnis:
        fehlt.append(GEHEIMNIS_NAME)
    return fehlt


def verlange_zugangsdaten(umgebung=None, pfad=None):
    """Schluessel und Geheimnis - oder eine Ausnahme.

    Fuer alles, was ohne Anmeldung wirklich nicht geht. Der Kursabruf gehoert
    NICHT dazu und ruft das hier nicht auf.
    """
    schluessel, geheimnis = zugangsdaten(umgebung, pfad)
    if not schluessel or not geheimnis:
        fehlt = ", ".join(fehlende_namen(umgebung, pfad))
        raise ZugangsdatenFehlen(
            f"Diese Aufgabe braucht Binance-Zugangsdaten, aber {fehlt} steht "
            f"nicht in der Umgebung. Sie gehoeren in {ENV_DATEI} - die Namen "
            f"stehen in .env.beispiel. Die Datei ist gitignoriert und bleibt "
            f"es; hier steht bewusst kein Wert.")
    return schluessel, geheimnis


def warnung_zuruecksetzen():
    """Die Einmal-Meldung wieder scharfstellen. Nur fuer Selbsttests."""
    global _GEWARNT
    _GEWARNT = False


def _melde_fehlende_schluessel(fehlt, ausgabe=None):
    """Einmal je Prozess sagen, dass unangemeldet abgerufen wird.

    Einmal, nicht je Symbol: bei 25 Symbolen mal fuenf Bots waere die Meldung
    Laerm, und Laerm wird ueberlesen. Nach `stderr`, damit sie nicht in einer
    Ausgabe untergeht, die jemand weiterverarbeitet.
    """
    global _GEWARNT
    if _GEWARNT or not fehlt:
        return False
    _GEWARNT = True
    ziel = ausgabe if ausgabe is not None else sys.stderr
    print(f"[fetch_binance_data] HINWEIS: {', '.join(fehlt)} fehlt in der "
          f"Umgebung. Der Kursabruf laeuft unangemeldet ueber den "
          f"oeffentlichen Endpunkt weiter - er braucht keinen Schluessel. "
          f"Wer einen setzen will: {ENV_DATEI} anlegen, Namen siehe "
          f".env.beispiel.", file=ziel)
    return True


# ---------------------------------------------------------------------------
# Der Abruf
# ---------------------------------------------------------------------------
def erzeuge_client(umgebung=None, pfad=None, ausgabe=None):
    """Einen python-binance-Client bauen - mit Schluessel, wenn vorhanden.

    `binance` wird **hier** eingebunden, nicht oben in der Datei. Dadurch
    laesst sich dieses Modul auch dort importieren, wo das Paket fehlt (etwa
    in der Cloud), und die Selbsttests koennen den Abruf pruefen, ohne es zu
    brauchen.
    """
    schluessel, geheimnis = zugangsdaten(umgebung, pfad)
    if not schluessel or not geheimnis:
        _melde_fehlende_schluessel(fehlende_namen(umgebung, pfad), ausgabe)

    from binance.client import Client                       # noqa: PLC0415

    if schluessel and geheimnis:
        return Client(schluessel, geheimnis)
    # Ohne Anmeldung. Genau das tun `get_top_symbols.py` und
    # `fetch_multi_data.py` seit jeher, und der Kursendpunkt ist damit
    # zufrieden.
    return Client()


def als_dataframe(kerzen):
    """Rohkerzen des Endpunkts -> die sechs Spalten der Repo-Dateien.

    Binance liefert zwoelf Felder je Kerze als Zeichenketten; gebraucht
    werden die ersten sechs. `open_time` kommt als UTC-Millisekunden und wird
    zu einem zeitzonenfreien Zeitstempel - dieselbe Lesart wie in
    `shared/binance_historie.py` und `shared/abrufschutz.py`.

    Die vier Kurse und das Volumen werden zu `float`. Das ist nicht Kosmetik:
    als Zeichenkette schriebe `to_csv` Binances `4427.30000000` in die Datei,
    wo `4427.3` steht - jede Zeile zeichenverschieden, der Datenstand-Hash
    neu, und kein Kurs anders.
    """
    import pandas as pd                                     # noqa: PLC0415

    if not kerzen:
        return pd.DataFrame(columns=SPALTEN)

    df = pd.DataFrame({
        "open_time": [int(k[0]) for k in kerzen],
        "open": [float(k[1]) for k in kerzen],
        "high": [float(k[2]) for k in kerzen],
        "low": [float(k[3]) for k in kerzen],
        "close": [float(k[4]) for k in kerzen],
        "volume": [float(k[5]) for k in kerzen],
    })
    df["open_time"] = (pd.to_datetime(df["open_time"], unit="ms", utc=True)
                         .dt.tz_localize(None))
    return df[SPALTEN]


def fetch_historical_data(symbol, interval, lookback, client=None):
    """Historische Kerzen fuer ein Symbol.

    Die Signatur ist der Vertrag mit neun Modulen: alle neun rufen mit genau
    drei Argumenten der Reihe nach auf (`research/zugangsdaten/geruest.py`
    zaehlt sie mechanisch nach). `client` steht dahinter, hat eine Vorgabe und
    aendert daran nichts - er ist die eine Stelle, an der ein Selbsttest den
    Netzzugriff ersetzen kann, ohne den Ablauf drumherum nachzubauen.

    `lookback` ist die Schreibweise von python-binance: `"400 day ago UTC"`
    ebenso wie `"1 Jan, 2017"`. Sie wird unveraendert durchgereicht - hier
    wird nicht nachgebaut, was das Paket kann.

    Die **laufende** Kerze ist im Ergebnis enthalten. Das ist Absicht, siehe
    Kopf dieser Datei.

    Wirft `AbrufLeer`, wenn der Endpunkt nichts liefert - nie ein stilles
    leeres Ergebnis.
    """
    verbindung = client if client is not None else erzeuge_client()
    kerzen = verbindung.get_historical_klines(symbol, interval, lookback)
    if not kerzen:
        raise AbrufLeer(
            f"{symbol} {interval} ab {lookback!r}: der Endpunkt hat keine "
            f"einzige Kerze geliefert. Kein leeres Ergebnis zurueckgeben - "
            f"das sieht im Bot genauso aus wie 'kein Signal'.")
    return als_dataframe(kerzen)


if __name__ == "__main__":
    # Ein Selbstbericht, der NIE einen Wert ausgibt - nur, ob ein Name
    # gesetzt ist. Zum Nachsehen am Mac, ohne dass ein Schluessel im
    # Terminal landet.
    fehlt = fehlende_namen()
    print(f".env erwartet unter: {ENV_DATEI}")
    print(f".env vorhanden:      {os.path.exists(ENV_DATEI)}")
    for name in (SCHLUESSEL_NAME, GEHEIMNIS_NAME):
        print(f"{name:22s} {'gesetzt' if name not in fehlt else 'FEHLT'}")
    print("\nDer Kursabruf braucht keinen Schluessel - er laeuft auch, wenn "
          "hier FEHLT steht.")
    sys.exit(0)
