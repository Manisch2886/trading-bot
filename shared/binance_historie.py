"""
Krypto-Historie von Binance zurueckladen (TB-31)
==============================================================================
Die Kursdateien dieses Repos beginnen fuer Krypto am **2021-09-01** - nicht
weil Binance nicht weiter zurueckreicht, sondern weil `fetch_multi_data.py`
und `strategies/t3_supertrend/fetch_4h_data.py` mit
`LOOKBACK = "1825 day ago UTC"` (fuenf Jahre ab Abruftag) arbeiten. Der
oeffentliche Spot-Endpunkt `/api/v3/klines` liefert 1d-, 4h- und 1h-Kerzen
**ab dem jeweiligen Listing-Datum**, fuer BTC und ETH also ab 2017.

Warum das gebraucht wird
------------------------------------------------------------------------------
`docs/VORREGISTRIERUNG_neuselektion.md` Abschnitt 5.3: der Krypto-Faltenplan
der anstehenden Neuselektion verlangt **vier Jahre Mindesttraining vor der
ersten Testfalte**. Mit Datenbeginn 2021-09-01 liegt die erste zulaessige
Falte hinter dem Go-Live-Schnitt - es bleibt **keine** Selektionsfalte. Ohne
mehr Historie hat die Krypto-Haelfte der Neuselektion keinen Walk-Forward.

Was dieses Modul tut - und was ausdruecklich nicht
------------------------------------------------------------------------------
* Es benutzt **nur** `https://api.binance.com/api/v3/klines`, den
  oeffentlichen Spot-Endpunkt fuer Marktdaten. Kein `/sapi/`, kein `/fapi/`,
  **kein API-Schluessel** - und damit auch nicht das (absichtlich
  gitignorierte) `shared/fetch_binance_data.py`, das Zugangsdaten enthaelt.
* Es **verlaengert** vorhandene Dateien nach vorn und schreibt die
  bestehenden Zeilen **unveraendert im Original-Text** zurueck. Es
  ueberschreibt sie nicht und formatiert sie nicht neu.
* Bevor es etwas schreibt, laedt es den **gesamten** ueberlappenden Bereich
  mit herunter und vergleicht ihn **Zeile fuer Zeile** gegen die vorhandene
  Datei. Weicht eine Zeile ab, wird die Datei **nicht** geschrieben und die
  Abweichung gemeldet. Eine stillschweigend "gegluettete" Historie waere
  schlimmer als gar keine.
* Es fasst **keinen** Bot-Code und **keine** Parametrisierung an.

Der bekannte Sonderfall: die abgeleiteten Tageskerzen
------------------------------------------------------------------------------
Die `*_1d.csv` der Krypto-Symbole sind **nicht** nativ abgerufen, sondern von
`shared/build_daily_crypto_data.py` aus den 1h-Daten abgeleitet. Weil die
1h-Reihe am 2021-09-01 erst um 13:00 UTC einsetzt, ist die **erste**
Tageskerze jeder dieser Dateien eine **Teilkerze ueber 11 statt 24 Stunden**.
Gegen die native Tageskerze von Binance weicht sie deshalb ab - das ist kein
Fehler dieses Moduls, sondern ein Befund ueber den Altbestand.

Solange die Datei dort beginnt, sitzt diese Teilkerze am Rand. Sobald
Historie davorgesetzt wird, sitzt sie **mitten** in der Reihe: ein
stillschweigender 11-Stunden-Tag zwischen lauter 24-Stunden-Tagen. Deshalb:

* **Voreinstellung:** Die Datei wird **nicht** geschrieben, die Abweichung
  wird gemeldet.
* `--teilkerze-ersetzen` ersetzt **genau diese eine fuehrende Teilkerze**
  durch die native Tageskerze - ein ausdruecklicher, gezaehlter und
  berichteter Schritt, keine Nebenwirkung.

Ratenbegrenzung
------------------------------------------------------------------------------
Binance begrenzt nach **Anfragegewicht je IP und Minute** (Standard 6000);
`/api/v3/klines` wiegt 2. Drei Vorkehrungen, alle in `Drossel`:

1. Eine **Mindestpause** zwischen zwei Anfragen (Voreinstellung 0,25 s, rund
   240 Anfragen/min = 480 Gewicht/min, also unter einem Zehntel des Budgets).
2. Das Antwort-Kopffeld **`x-mbx-used-weight-1m`** wird gelesen; ab 70 % des
   Budgets wird bis zum Beginn der naechsten Minute gewartet.
3. **HTTP 429** wird mit `Retry-After` abgewartet und die Anfrage wiederholt;
   **HTTP 418** (IP gesperrt) bricht den Lauf sofort ab - weiterprobieren
   verlaengert nur die Sperre.

Nutzung
------------------------------------------------------------------------------
    python3 shared/binance_historie.py --messen          # nur feststellen
    python3 shared/binance_historie.py --trockenlauf     # laden, nicht schreiben
    python3 shared/binance_historie.py                   # laden und verlaengern
    python3 shared/binance_historie.py --teilkerze-ersetzen
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

import kursdaten                                          # noqa: E402

BASIS_URL = "https://api.binance.com"
ENDPUNKT = "/api/v3/klines"

# Nur diese drei Zeitrahmen braucht das Projekt: 1h (elliott_wave),
# 4h (t3_supertrend), 1d (die drei uebrigen Krypto-Bots).
INTERVALL_MS = {
    "1h": 3_600_000,
    "4h": 14_400_000,
    "1d": 86_400_000,
}

SPALTEN = ["open_time", "open", "high", "low", "close", "volume"]

# Die Zeitstempel, in denen die Dateien dieses Repos geschrieben sind.
ZEITFORMAT = {
    "1h": "%Y-%m-%d %H:%M:%S",
    "4h": "%Y-%m-%d %H:%M:%S",
    "1d": "%Y-%m-%d",
}

HOECHSTZAHL_JE_ANFRAGE = 1000       # Obergrenze des Endpunkts
GEWICHT_JE_ANFRAGE = 2              # /api/v3/klines
GEWICHTSBUDGET_JE_MINUTE = 6000     # Binance-Standard je IP
GEWICHTSSCHWELLE = 0.70             # ab hier bis zur naechsten Minute warten


class BinanceFehler(RuntimeError):
    """Der Endpunkt hat nicht geliefert, was erwartet wurde."""


class Gesperrt(BinanceFehler):
    """HTTP 418 - die IP ist gesperrt. Nicht weiterprobieren."""


# ---------------------------------------------------------------------------
# Ratenbegrenzung
# ---------------------------------------------------------------------------
class Drossel:
    """Haelt die Ratenbegrenzung des Endpunkts ein.

    Die Uhr ist als Parameter hereingereicht (`uhr`, `schlafen`), damit der
    Test den Ablauf beobachten kann, ohne wirklich zu warten.
    """

    def __init__(self, mindestpause=0.25, uhr=time.monotonic, schlafen=time.sleep,
                 budget=GEWICHTSBUDGET_JE_MINUTE, schwelle=GEWICHTSSCHWELLE):
        self.mindestpause = mindestpause
        self._uhr = uhr
        self._schlafen = schlafen
        self.budget = budget
        self.schwelle = schwelle
        self.letzte_anfrage = None
        self.zuletzt_gemeldetes_gewicht = 0
        self.anfragen = 0
        self.wartezeit_gesamt = 0.0
        self.pausen_wegen_gewicht = 0

    def vor_anfrage(self):
        """Mindestpause einhalten."""
        if self.letzte_anfrage is not None:
            rest = self.mindestpause - (self._uhr() - self.letzte_anfrage)
            if rest > 0:
                self._warte(rest)
        self.letzte_anfrage = self._uhr()
        self.anfragen += 1

    def nach_antwort(self, kopffelder):
        """Das gemeldete Gewicht auswerten und noetigenfalls aussetzen."""
        roh = None
        for name in ("x-mbx-used-weight-1m", "X-MBX-USED-WEIGHT-1M"):
            if kopffelder and name in kopffelder:
                roh = kopffelder[name]
                break
        if roh is None:
            # Kein Kopffeld: die Mindestpause bleibt die einzige Wache. Das
            # gemeldete Gewicht wird dann konservativ selbst mitgezaehlt.
            self.zuletzt_gemeldetes_gewicht += GEWICHT_JE_ANFRAGE
        else:
            try:
                self.zuletzt_gemeldetes_gewicht = int(roh)
            except (TypeError, ValueError):
                self.zuletzt_gemeldetes_gewicht += GEWICHT_JE_ANFRAGE

        if self.zuletzt_gemeldetes_gewicht >= self.budget * self.schwelle:
            self.pausen_wegen_gewicht += 1
            self._warte(self._rest_der_minute())
            self.zuletzt_gemeldetes_gewicht = 0

    def _rest_der_minute(self):
        """Bis zum Beginn der naechsten vollen Minute (Wanduhr)."""
        return 60.0 - (time.time() % 60.0)

    def _warte(self, sekunden):
        if sekunden <= 0:
            return
        self.wartezeit_gesamt += sekunden
        self._schlafen(sekunden)

    def nach_429(self, retry_after):
        """Binance hat gebremst - so lange warten, wie es verlangt."""
        try:
            sekunden = float(retry_after)
        except (TypeError, ValueError):
            sekunden = 60.0
        self._warte(max(sekunden, 1.0))
        self.zuletzt_gemeldetes_gewicht = 0


# ---------------------------------------------------------------------------
# Der Abrufer: die einzige Stelle, die wirklich ins Netz geht
# ---------------------------------------------------------------------------
class Abrufer:
    """Holt Rohkerzen von `/api/v3/klines`.

    Die einzige Netzstelle des Moduls. Der Test setzt an dieselbe Stelle
    einen Ersatz und beobachtet dadurch den echten Ablauf statt einen
    von Hand hergestellten Zustand.
    """

    def __init__(self, drossel=None, basis_url=BASIS_URL, versuche=4, oeffner=None):
        self.drossel = drossel if drossel is not None else Drossel()
        self.basis_url = basis_url
        self.versuche = versuche
        self._oeffner = oeffner or urllib.request.urlopen

    def __call__(self, symbol, intervall, start_ms=None, end_ms=None, limit=None):
        parameter = {"symbol": symbol, "interval": intervall}
        if start_ms is not None:
            parameter["startTime"] = int(start_ms)
        if end_ms is not None:
            parameter["endTime"] = int(end_ms)
        parameter["limit"] = int(limit or HOECHSTZAHL_JE_ANFRAGE)
        url = f"{self.basis_url}{ENDPUNKT}?{urllib.parse.urlencode(parameter)}"

        for versuch in range(1, self.versuche + 1):
            self.drossel.vor_anfrage()
            try:
                with self._oeffner(url, timeout=30) as antwort:
                    rohtext = antwort.read()
                    kopffelder = dict(antwort.headers.items())
            except urllib.error.HTTPError as fehler:
                if fehler.code == 418:
                    raise Gesperrt(
                        "Binance hat die IP gesperrt (HTTP 418). Der Lauf "
                        "bricht ab; Weiterprobieren verlaengert die Sperre.")
                if fehler.code == 429:
                    self.drossel.nach_429(fehler.headers.get("Retry-After"))
                    continue
                if versuch == self.versuche:
                    raise BinanceFehler(
                        f"{symbol} {intervall}: HTTP {fehler.code}") from fehler
                self.drossel._warte(2 ** versuch)
                continue
            except urllib.error.URLError as fehler:
                if versuch == self.versuche:
                    raise BinanceFehler(
                        f"{symbol} {intervall}: {fehler.reason}") from fehler
                self.drossel._warte(2 ** versuch)
                continue

            self.drossel.nach_antwort(kopffelder)
            try:
                return json.loads(rohtext)
            except ValueError as fehler:
                raise BinanceFehler(
                    f"{symbol} {intervall}: Antwort ist kein JSON") from fehler

        raise BinanceFehler(f"{symbol} {intervall}: {self.versuche} Versuche erfolglos")


# ---------------------------------------------------------------------------
# Historie feststellen und laden
# ---------------------------------------------------------------------------
def erste_kerze_ms(abrufer, symbol, intervall):
    """Der tatsaechliche Datenbeginn des Symbols in diesem Zeitrahmen.

    `startTime=0` heisst fuer den Endpunkt "ab dem Anfang, den es gibt"; mit
    `limit=1` kommt genau die erste Kerze zurueck. Das ist der Grund, warum
    das Startdatum **gemessen** und nicht geschaetzt werden muss: ein 2025
    gelistetes Paar hat keine Historie ab 2017, egal was der Endpunkt
    grundsaetzlich anbietet.

    Rueckgabe: `open_time` der ersten Kerze in Millisekunden, oder `None`,
    wenn der Endpunkt fuer das Symbol nichts liefert.
    """
    kerzen = abrufer(symbol, intervall, start_ms=0, limit=1)
    if not kerzen:
        return None
    return int(kerzen[0][0])


def kerzen_laden(abrufer, symbol, intervall, start_ms, end_ms):
    """Alle Kerzen von `start_ms` bis **einschliesslich** `end_ms`.

    Blaettert in Schritten von hoechstens 1000 Kerzen. Der naechste Block
    beginnt eine Millisekunde nach der zuletzt erhaltenen `open_time`, damit
    keine Kerze doppelt kommt und keine ausgelassen wird.
    """
    schrittweite = INTERVALL_MS[intervall]
    gesammelt = []
    zeiger = int(start_ms)
    gesehen = set()
    while zeiger <= end_ms:
        block = abrufer(symbol, intervall, start_ms=zeiger, end_ms=end_ms,
                        limit=HOECHSTZAHL_JE_ANFRAGE)
        if not block:
            break
        for kerze in block:
            oeffnung = int(kerze[0])
            if oeffnung in gesehen or oeffnung > end_ms:
                continue
            gesehen.add(oeffnung)
            gesammelt.append(kerze)
        letzte = int(block[-1][0])
        if letzte < zeiger:
            # Der Endpunkt geht nicht vorwaerts - Abbruch statt Endlosschleife.
            break
        zeiger = letzte + schrittweite
    gesammelt.sort(key=lambda k: int(k[0]))
    return gesammelt


def als_dataframe(kerzen, intervall):
    """Rohkerzen -> DataFrame mit genau den sechs Spalten der Repo-Dateien.

    Binance liefert zwoelf Felder je Kerze; gebraucht werden die ersten
    sechs. Die Zeitstempel sind UTC-Millisekunden.
    """
    import pandas as pd                                    # noqa: PLC0415

    if not kerzen:
        return pd.DataFrame(columns=SPALTEN)
    zeilen = {
        "open_time": [int(k[0]) for k in kerzen],
        "open": [float(k[1]) for k in kerzen],
        "high": [float(k[2]) for k in kerzen],
        "low": [float(k[3]) for k in kerzen],
        "close": [float(k[4]) for k in kerzen],
        "volume": [float(k[5]) for k in kerzen],
    }
    df = pd.DataFrame(zeilen)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).dt.tz_localize(None)
    return df[SPALTEN]


def zeitstempel_text(wert, intervall):
    """Zeitstempel so schreiben, wie die vorhandenen Dateien es tun."""
    return wert.strftime(ZEITFORMAT[intervall])


# ---------------------------------------------------------------------------
# Vorhandene Dateien lesen - Text und Werte getrennt
# ---------------------------------------------------------------------------
class Kursdatei:
    """Eine vorhandene Kursdatei, in Rohtext **und** Werten.

    Beides wird gebraucht und darf nicht durcheinandergehen:

    * der **Rohtext** wird beim Verlaengern unveraendert zurueckgeschrieben -
      keine Zeile wird neu formatiert, sonst waere das Ergebnis ein
      Ueberschreiben mit anderer Schreibweise statt einer Verlaengerung;
    * die **Werte** dienen dem Zeile-fuer-Zeile-Vergleich gegen die frisch
      geladenen Kerzen.
    """

    def __init__(self, pfad, intervall):
        self.pfad = pfad
        self.intervall = intervall
        with open(pfad, "r", encoding="utf-8", newline="") as datei:
            inhalt = datei.read()
        self.endet_mit_umbruch = inhalt.endswith("\n")
        zeilen = inhalt.splitlines()
        if not zeilen:
            raise BinanceFehler(f"{pfad}: leer")
        self.kopfzeile = zeilen[0]
        self.zeilen = zeilen[1:]
        self.werte = [self._zerlege(z, nummer) for nummer, z in enumerate(self.zeilen, 2)]
        self.nach_zeitpunkt = {w["zeitpunkt"]: w for w in self.werte}

    def _zerlege(self, zeile, nummer):
        teile = zeile.split(",")
        if len(teile) != len(SPALTEN):
            raise BinanceFehler(
                f"{self.pfad} Zeile {nummer}: {len(teile)} Felder statt {len(SPALTEN)}")
        try:
            return {
                "zeitpunkt": teile[0],
                "open": float(teile[1]),
                "high": float(teile[2]),
                "low": float(teile[3]),
                "close": float(teile[4]),
                "volume": float(teile[5]),
                "zeile": zeile,
                "nummer": nummer,
            }
        except ValueError as fehler:
            raise BinanceFehler(f"{self.pfad} Zeile {nummer}: {fehler}") from fehler

    @property
    def erster_zeitpunkt(self):
        return self.werte[0]["zeitpunkt"] if self.werte else None

    @property
    def letzter_zeitpunkt(self):
        return self.werte[-1]["zeitpunkt"] if self.werte else None


# Relative Toleranz fuer das Volumen. Sie gilt **nur** dort und hat einen
# gemessenen Grund: die `*_1d.csv` der Krypto-Symbole sind von
# `build_daily_crypto_data.py` abgeleitet und fuehren das Volumen als
# Gleitkomma-Summe von 24 Stundenwerten (sichtbar an Werten wie
# `7565.2410899999995`). Die native Tageskerze summiert dieselben Handel in
# anderer Reihenfolge und landet in den letzten Bits anders. Die vier
# Kursspalten werden **exakt** verglichen - dort gibt es nichts zu tolerieren.
VOLUMEN_TOLERANZ = 1e-9

KURSSPALTEN = ["open", "high", "low", "close"]


def vergleiche_ueberlappung(datei, geladen_nach_zeitpunkt):
    """Vergleicht den ueberlappenden Bereich Zeile fuer Zeile.

    `geladen_nach_zeitpunkt`: {Zeitstempel-Text -> Werte-Dict} der frisch
    geladenen Kerzen.

    Rueckgabe: Liste von Befunden. Jeder Befund hat eine `art`:

    * `fehlt`            - die vorhandene Zeile kommt beim Endpunkt nicht vor
    * `kurs`             - mindestens eine der vier Kursspalten weicht ab
    * `volumen`          - das Volumen weicht ueber die Toleranz hinaus ab
    * `volumen_rundung`   - das Volumen weicht innerhalb der Toleranz ab

    Die ersten drei sind **hart** (es wird nicht geschrieben), der vierte
    wird berichtet und gezaehlt.
    """
    befunde = []
    for wert in datei.werte:
        geladen = geladen_nach_zeitpunkt.get(wert["zeitpunkt"])
        if geladen is None:
            befunde.append({"art": "fehlt", "zeitpunkt": wert["zeitpunkt"],
                            "nummer": wert["nummer"], "spalte": None,
                            "alt": None, "neu": None})
            continue
        for spalte in KURSSPALTEN:
            if wert[spalte] != geladen[spalte]:
                befunde.append({"art": "kurs", "zeitpunkt": wert["zeitpunkt"],
                                "nummer": wert["nummer"], "spalte": spalte,
                                "alt": wert[spalte], "neu": geladen[spalte]})
        alt_v, neu_v = wert["volume"], geladen["volume"]
        if alt_v != neu_v:
            bezug = max(abs(alt_v), abs(neu_v), 1e-30)
            abweichung = abs(alt_v - neu_v) / bezug
            art = "volumen_rundung" if abweichung <= VOLUMEN_TOLERANZ else "volumen"
            befunde.append({"art": art, "zeitpunkt": wert["zeitpunkt"],
                            "nummer": wert["nummer"], "spalte": "volume",
                            "alt": alt_v, "neu": neu_v, "relativ": abweichung})
    return befunde


HARTE_ARTEN = {"fehlt", "kurs", "volumen"}


def harte_befunde(befunde):
    return [b for b in befunde if b["art"] in HARTE_ARTEN]


def nur_fuehrende_teilkerze(datei, befunde):
    """True, wenn **alle** harten Befunde die erste Zeile der Datei betreffen.

    Genau die Lage, die `build_daily_crypto_data.py` hinterlassen hat. Die
    Bedingung ist absichtlich eng: sobald irgendeine spaetere Zeile abweicht,
    ist es nicht mehr dieser Sonderfall, sondern ein echter Befund.
    """
    hart = harte_befunde(befunde)
    if not hart:
        return False
    erste = datei.erster_zeitpunkt
    return all(b["zeitpunkt"] == erste for b in hart)


# ---------------------------------------------------------------------------
# Eine Datei verlaengern
# ---------------------------------------------------------------------------
def _ms_aus_text(text, intervall):
    import pandas as pd                                    # noqa: PLC0415
    return int(pd.Timestamp(text).value // 1_000_000)


def _zeilen_aus_dataframe(df, intervall):
    """DataFrame -> CSV-Zeilen in der Schreibweise der vorhandenen Dateien.

    Geschrieben wird mit demselben Werkzeug (`pandas.to_csv`), mit dem die
    Altbestaende entstanden sind - so sieht die vorangestellte Historie aus
    wie der Rest der Datei und nicht wie ein Fremdkoerper.
    """
    if len(df) == 0:
        return []
    ausgabe = df.copy()
    ausgabe["open_time"] = ausgabe["open_time"].dt.strftime(ZEITFORMAT[intervall])
    text = ausgabe.to_csv(index=False, header=False, lineterminator="\n")
    return text.splitlines()


# Oeffentliche Namen fuer die beiden Schreibbausteine. `kursdaten_neuaufbau.py`
# (TB-34) baut den Bestand vollstaendig neu auf und muss dabei **dieselbe**
# Schreibweise treffen wie die vorhandenen Dateien - eine zweite Formatierung
# waere genau die Art doppelt gefuehrter Wahrheit, die dieses Projekt schon
# mehrfach eingesammelt hat. Die Funktionen selbst bleiben unveraendert.
zeilen_aus_dataframe = _zeilen_aus_dataframe


def verlaengere_datei(abrufer, pfad, symbol, intervall, schreiben=True,
                      teilkerze_ersetzen=False, zaehler=None):
    """Laedt die Historie eines Symbols zurueck und verlaengert die Datei.

    Der Ablauf in der Reihenfolge, in der er auch scheitern koennen muss:

    1. tatsaechlichen Datenbeginn **messen** (`erste_kerze_ms`),
    2. den Bereich vom Datenbeginn bis zur letzten vorhandenen Kerze laden -
       also **einschliesslich** des ganzen ueberlappenden Teils,
    3. unvollstaendige Kerzen ueber `shared/kursdaten.py` streichen und
       zaehlen,
    4. die Ueberlappung Zeile fuer Zeile vergleichen,
    5. erst danach schreiben, und nur den Teil **vor** der ersten
       vorhandenen Zeile.

    Rueckgabe: ein Ergebnis-Dict. `geschrieben` sagt, ob die Datei
    tatsaechlich angefasst wurde.
    """
    datei = Kursdatei(pfad, intervall)
    ergebnis = {
        "symbol": symbol, "intervall": intervall, "pfad": pfad,
        "datei_beginn": datei.erster_zeitpunkt,
        "datei_ende": datei.letzter_zeitpunkt,
        "zeilen_vorher": len(datei.werte),
        "endpunkt_beginn": None, "neue_zeilen": 0, "zeilen_nachher": len(datei.werte),
        "gestrichene_kerzen": 0, "befunde": [], "luecken": [],
        "geschrieben": False, "grund": None,
    }

    beginn_ms = erste_kerze_ms(abrufer, symbol, intervall)
    if beginn_ms is None:
        ergebnis["grund"] = "Endpunkt liefert fuer dieses Symbol keine Kerzen"
        return ergebnis

    ende_ms = _ms_aus_text(datei.letzter_zeitpunkt, intervall)
    kerzen = kerzen_laden(abrufer, symbol, intervall, beginn_ms, ende_ms)
    df = als_dataframe(kerzen, intervall)
    df, gestrichen = kursdaten.entferne_unvollstaendige(
        df, symbol=f"{symbol}_{intervall}", melden=False)
    ergebnis["gestrichene_kerzen"] = gestrichen
    if zaehler is not None:
        zaehler.erfasse(f"{symbol}_{intervall}", gestrichen)
    if len(df) == 0:
        ergebnis["grund"] = "Endpunkt liefert keine verwertbaren Kerzen"
        return ergebnis

    ergebnis["endpunkt_beginn"] = zeitstempel_text(df["open_time"].iloc[0], intervall)

    zeitstempel = df["open_time"].dt.strftime(ZEITFORMAT[intervall]).tolist()
    geladen = {
        ts: {"open": o, "high": h, "low": l, "close": c, "volume": v}
        for ts, o, h, l, c, v in zip(
            zeitstempel, df["open"], df["high"], df["low"], df["close"], df["volume"])
    }

    befunde = vergleiche_ueberlappung(datei, geladen)
    ergebnis["befunde"] = befunde

    # Zeitpunkte, die der Endpunkt im ueberlappenden Bereich kennt, die
    # Datei aber nicht: eine Luecke im Altbestand. Wird berichtet, aber
    # nicht gefuellt - dieses Modul verlaengert nach vorn, es flickt nicht.
    in_datei = set(datei.nach_zeitpunkt)
    ergebnis["luecken"] = [
        ts for ts in zeitstempel
        if ts >= datei.erster_zeitpunkt and ts not in in_datei
    ]

    hart = harte_befunde(befunde)
    fuehrende_teilkerze = nur_fuehrende_teilkerze(datei, befunde)

    if hart and not (fuehrende_teilkerze and teilkerze_ersetzen):
        if fuehrende_teilkerze:
            ergebnis["grund"] = (
                "fuehrende Teilkerze weicht ab - mit --teilkerze-ersetzen "
                "wird genau diese eine Zeile durch die native Kerze ersetzt")
        else:
            ergebnis["grund"] = (
                f"{len(hart)} harte Abweichung(en) im ueberlappenden Bereich - "
                "nicht geschrieben")
        return ergebnis

    neue = df[df["open_time"] < _zeitpunkt(datei.erster_zeitpunkt)]
    neue_zeilen = _zeilen_aus_dataframe(neue, intervall)
    ergebnis["neue_zeilen"] = len(neue_zeilen)

    rumpf = list(datei.zeilen)
    ersetzt = 0
    if fuehrende_teilkerze and teilkerze_ersetzen:
        ersatz = df[df["open_time"] == _zeitpunkt(datei.erster_zeitpunkt)]
        ersatz_zeilen = _zeilen_aus_dataframe(ersatz, intervall)
        if ersatz_zeilen:
            rumpf[0] = ersatz_zeilen[0]
            ersetzt = 1
    ergebnis["ersetzte_zeilen"] = ersetzt

    if not neue_zeilen and not ersetzt:
        ergebnis["grund"] = "Datei beginnt bereits am Datenbeginn des Endpunkts"
        ergebnis["zeilen_nachher"] = len(rumpf)
        return ergebnis

    ergebnis["zeilen_nachher"] = len(neue_zeilen) + len(rumpf)
    if schreiben:
        _schreibe(pfad, datei.kopfzeile, neue_zeilen + rumpf, datei.endet_mit_umbruch)
        ergebnis["geschrieben"] = True
    else:
        ergebnis["grund"] = "Trockenlauf - nicht geschrieben"
    return ergebnis


def _zeitpunkt(text):
    import pandas as pd                                    # noqa: PLC0415
    return pd.Timestamp(text)


def _schreibe(pfad, kopfzeile, zeilen, endet_mit_umbruch):
    """Erst vollstaendig daneben schreiben, dann umbenennen.

    Ein abgebrochener Lauf darf keine halbe Kursdatei hinterlassen - die
    faellt beim naechsten Backtest nicht auf, sie liefert nur andere Zahlen.
    """
    vorlaeufig = pfad + ".neu"
    text = "\n".join([kopfzeile] + zeilen)
    if endet_mit_umbruch:
        text += "\n"
    with open(vorlaeufig, "w", encoding="utf-8", newline="") as datei:
        datei.write(text)
    os.replace(vorlaeufig, pfad)


schreibe_datei = _schreibe


# ---------------------------------------------------------------------------
# Messen: ab wann reicht der Endpunkt je Symbol zurueck?
# ---------------------------------------------------------------------------
def messe_datenbeginn(abrufer, symbole, zeitrahmen):
    """Je Symbol und Zeitrahmen das **tatsaechliche** Startdatum.

    Das ist der wichtigste Teil der Aufgabe und der Grund, warum hier nichts
    geschaetzt wird: ein Universum, in dem einige Paare ab 2017 und andere
    erst ab 2025 vorliegen, erzeugt im Backtest eine survivorship-nahe
    Verzerrung - die frueh gelisteten sind die, die den Zyklus 2018
    ueberlebt haben. Messen und ausweisen, nicht gluetten.
    """
    import pandas as pd                                    # noqa: PLC0415

    messung = {}
    for symbol in symbole:
        je_zeitrahmen = {}
        for intervall in zeitrahmen:
            try:
                ms = erste_kerze_ms(abrufer, symbol, intervall)
            except BinanceFehler as fehler:
                je_zeitrahmen[intervall] = {"beginn": None, "fehler": str(fehler)}
                continue
            if ms is None:
                je_zeitrahmen[intervall] = {"beginn": None, "fehler": "keine Kerzen"}
                continue
            zeitpunkt = pd.Timestamp(ms, unit="ms")
            je_zeitrahmen[intervall] = {
                "beginn": zeitstempel_text(zeitpunkt, intervall),
                "beginn_tag": zeitpunkt.strftime("%Y-%m-%d"),
                "fehler": None,
            }
        messung[symbol] = je_zeitrahmen
    return messung


def vorhandener_beginn(datenordner, symbol, intervall):
    """Ab wann die Datei im Repo heute reicht - oder None, wenn es sie nicht gibt."""
    pfad = os.path.join(datenordner, f"{symbol}_{intervall}.csv")
    if not os.path.exists(pfad):
        return None
    with open(pfad, "r", encoding="utf-8") as datei:
        datei.readline()
        erste = datei.readline().strip()
    return erste.split(",")[0] if erste else None


# ---------------------------------------------------------------------------
def _tabelle_messung(messung, datenordner, zeitrahmen):
    zeilen = []
    kopf = f"{'Symbol':<12} " + " ".join(
        f"{'Endpunkt ' + z:<22}" for z in zeitrahmen) + f"{'Datei heute (1h)':<20}"
    zeilen.append(kopf)
    zeilen.append("-" * len(kopf))
    for symbol in sorted(messung):
        teile = [f"{symbol:<12} "]
        for intervall in zeitrahmen:
            eintrag = messung[symbol].get(intervall, {})
            teile.append(f"{(eintrag.get('beginn') or eintrag.get('fehler') or '-'):<22}")
        heute = vorhandener_beginn(datenordner, symbol, "1h") or "-"
        teile.append(f"{heute:<20}")
        zeilen.append(" ".join(teile))
    return "\n".join(zeilen)


def main(argv=None) -> int:
    from paths import DATA_DIR                             # noqa: PLC0415
    from symbols_config import SYMBOLS                     # noqa: PLC0415

    zerleger = argparse.ArgumentParser(
        description="Laedt die Krypto-Historie ueber /api/v3/klines zurueck "
                    "und verlaengert die vorhandenen Kursdateien nach vorn.")
    zerleger.add_argument("--messen", action="store_true",
                          help="nur feststellen, ab wann der Endpunkt je Symbol reicht")
    zerleger.add_argument("--trockenlauf", action="store_true",
                          help="laden und vergleichen, aber nichts schreiben")
    zerleger.add_argument("--teilkerze-ersetzen", action="store_true",
                          help="die fuehrende Teilkerze abgeleiteter *_1d.csv durch "
                               "die native Tageskerze ersetzen")
    zerleger.add_argument("--symbole", default=None,
                          help="kommagetrennt; Voreinstellung: die Liste aus symbols_config")
    zerleger.add_argument("--zeitrahmen", default="1h,4h,1d")
    zerleger.add_argument("--ordner", default=DATA_DIR)
    zerleger.add_argument("--pause", type=float, default=0.25,
                          help="Mindestpause zwischen zwei Anfragen in Sekunden")
    zerleger.add_argument("--bericht", default=None,
                          help="Pfad fuer den JSON-Bericht des Laufs")
    argumente = zerleger.parse_args(argv)

    symbole = ([s.strip() for s in argumente.symbole.split(",") if s.strip()]
               if argumente.symbole else list(SYMBOLS))
    zeitrahmen = [z.strip() for z in argumente.zeitrahmen.split(",") if z.strip()]
    unbekannt = [z for z in zeitrahmen if z not in INTERVALL_MS]
    if unbekannt:
        print(f"Unbekannte(r) Zeitrahmen: {', '.join(unbekannt)}")
        return 2

    drossel = Drossel(mindestpause=argumente.pause)
    abrufer = Abrufer(drossel=drossel)

    print(f"Endpunkt: {BASIS_URL}{ENDPUNKT} (oeffentlich, ohne Schluessel)")
    print(f"Ratenbegrenzung: Mindestpause {argumente.pause:.2f}s, "
          f"Gewichtsbudget {GEWICHTSBUDGET_JE_MINUTE}/min, "
          f"Pause ab {int(GEWICHTSSCHWELLE * 100)} % des Budgets")
    print(f"{len(symbole)} Symbol(e), Zeitrahmen: {', '.join(zeitrahmen)}\n")

    if argumente.messen:
        messung = messe_datenbeginn(abrufer, symbole, zeitrahmen)
        print(_tabelle_messung(messung, argumente.ordner, zeitrahmen))
        print(f"\n{drossel.anfragen} Anfragen, {drossel.wartezeit_gesamt:.1f}s gewartet, "
              f"{drossel.pausen_wegen_gewicht} Pause(n) wegen Gewicht.")
        if argumente.bericht:
            with open(argumente.bericht, "w", encoding="utf-8") as datei:
                json.dump({"messung": messung}, datei, indent=2, sort_keys=True)
            print(f"Bericht: {argumente.bericht}")
        return 0

    zaehler = kursdaten.Zaehler()
    ergebnisse = []
    for symbol in symbole:
        for intervall in zeitrahmen:
            pfad = os.path.join(argumente.ordner, f"{symbol}_{intervall}.csv")
            if not os.path.exists(pfad):
                print(f"  {symbol:<12} {intervall:<3} keine Datei im Repo - uebersprungen")
                continue
            try:
                ergebnis = verlaengere_datei(
                    abrufer, pfad, symbol, intervall,
                    schreiben=not argumente.trockenlauf,
                    teilkerze_ersetzen=argumente.teilkerze_ersetzen,
                    zaehler=zaehler)
            except Gesperrt as fehler:
                print(f"\nABBRUCH: {fehler}")
                return 3
            except BinanceFehler as fehler:
                print(f"  {symbol:<12} {intervall:<3} FEHLER: {fehler}")
                continue
            ergebnisse.append(ergebnis)
            print(_zeile(ergebnis))

    print()
    bericht = zaehler.melde()
    if bericht is None:
        print("Datenqualitaet: keine unvollstaendigen Kerzen in den geladenen Daten.")
    _zusammenfassung(ergebnisse, drossel)

    if argumente.bericht:
        with open(argumente.bericht, "w", encoding="utf-8") as datei:
            json.dump({"ergebnisse": ergebnisse}, datei, indent=2,
                      sort_keys=True, default=str)
        print(f"Bericht: {argumente.bericht}")

    return 1 if any(harte_befunde(e["befunde"]) for e in ergebnisse) else 0


def _zeile(ergebnis):
    hart = len(harte_befunde(ergebnis["befunde"]))
    zustand = "geschrieben" if ergebnis["geschrieben"] else (ergebnis["grund"] or "-")
    return (f"  {ergebnis['symbol']:<12} {ergebnis['intervall']:<3} "
            f"Endpunkt ab {str(ergebnis['endpunkt_beginn']):<20} "
            f"+{ergebnis['neue_zeilen']:>6} Zeile(n)  "
            f"{hart} harte Abweichung(en)  {zustand}")


def _zusammenfassung(ergebnisse, drossel):
    geschrieben = [e for e in ergebnisse if e["geschrieben"]]
    mit_befund = [e for e in ergebnisse if harte_befunde(e["befunde"])]
    mit_luecke = [e for e in ergebnisse if e["luecken"]]
    rundung = sum(1 for e in ergebnisse
                  for b in e["befunde"] if b["art"] == "volumen_rundung")
    print(f"{len(ergebnisse)} Datei(en) geprueft, {len(geschrieben)} verlaengert, "
          f"{sum(e['neue_zeilen'] for e in ergebnisse)} Zeile(n) vorangestellt.")
    if mit_befund:
        print(f"{len(mit_befund)} Datei(en) mit harter Abweichung im ueberlappenden "
              f"Bereich - NICHT geschrieben:")
        for e in mit_befund:
            erste = harte_befunde(e["befunde"])[0]
            print(f"  {e['symbol']}_{e['intervall']}: {len(harte_befunde(e['befunde']))} "
                  f"Abweichung(en), erste bei {erste['zeitpunkt']} "
                  f"({erste['art']}, Spalte {erste['spalte']})")
    else:
        print("Der ueberlappende Bereich ist in jeder Datei identisch.")
    if rundung:
        print(f"{rundung} Zeile(n) mit Volumen-Abweichung innerhalb der Toleranz "
              f"({VOLUMEN_TOLERANZ:g} relativ) - Gleitkomma-Summe, kein Befund.")
    if mit_luecke:
        print(f"{len(mit_luecke)} Datei(en) haben im vorhandenen Bereich Luecken, "
              f"die der Endpunkt kennt (nicht gefuellt - dieses Modul verlaengert "
              f"nur nach vorn):")
        for e in mit_luecke:
            print(f"  {e['symbol']}_{e['intervall']}: {len(e['luecken'])} Zeitpunkt(e), "
                  f"erster {e['luecken'][0]}")
    print(f"{drossel.anfragen} Anfragen, {drossel.wartezeit_gesamt:.1f}s gewartet, "
          f"{drossel.pausen_wegen_gewicht} Pause(n) wegen Gewicht.")


if __name__ == "__main__":
    sys.exit(main())
