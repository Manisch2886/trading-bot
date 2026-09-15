#!/usr/bin/env python3
"""
Selbsttests zu shared/fetch_binance_data.py (TB-37)
==============================================================================
Geprueft wird das **Verhalten**, nicht das Vorhandensein von Codestuecken.
Eine Pruefung wie "im Quelltext kommt `os.environ` vor" waere wertlos: sie
bliebe gruen, wenn daneben ein Schluessel im Klartext staende.

Die Datei, die hier geprueft wird, ist der Ersatz fuer diejenige, die bis
TB-37 gitignoriert war und genau einmal existierte. Neun Module haengen an
ihr, fuenf davon im Live-Betrieb. Sie darf deshalb weder in der Signatur noch
in der Rueckgabeform von der alten abweichen - und das prueft Abschnitt 1
**mechanisch an den Aufrufern**, nicht an einer Liste von Hand.

Die zwei wiederkehrenden Fallen dieses Projekts sind ausdruecklich adressiert:

* **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
  selbst.** Deshalb Abschnitt 9: jede Absicherung wird an einer Kopie des
  Moduls einzeln **ausgeschaltet**, und danach muss genau die Pruefung, die
  sie bewacht, auch wirklich FEHLSCHLAGEN. Eine Pruefung, die ohne ihre
  Absicherung gruen bleibt, prueft nichts.
* **Eine zweite Wache verdeckt das Fehlen der ersten.** Abschnitt 9 prueft
  deshalb nicht nur, dass die zugehoerige Pruefung faellt, sondern auch, dass
  die **uebrigen** stehen bleiben. Faellt bei einer Mutation alles, sagt das
  nichts ueber die einzelne Absicherung.

Ohne Netz und ohne `binance`. Binance ist aus der Cloud gesperrt (HTTP 403),
und `python-binance` ist dort nicht installiert. Beides wird hier nicht
gebraucht: der Netzzugriff wird an genau **einer** Stelle ersetzt - dort, wo
python-binance sein Ergebnis abliefert. Alles davor und danach (Umgebung
lesen, Schluessel entscheiden, umwandeln, leeres Ergebnis erkennen, melden)
laeuft echt.

⚠️ In dieser Datei steht kein Schluessel und nichts, was wie einer aussieht.
Abschnitt 8 prueft genau das - fuer diese Datei wie fuer alle uebrigen, die
TB-37 dem Repo hinzufuegt.

Nutzung:  python3 shared/test_fetch_binance_data.py
"""

import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

import pandas as pd                                            # noqa: E402

import fetch_binance_data as fbd                               # noqa: E402

BESTANDEN = 0
FEHLER = []

MODULPFAD = os.path.join(_SHARED, "fetch_binance_data.py")


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print(f"  [OK]     {name}")
    else:
        FEHLER.append(name)
        print(f"  [FEHLER] {name}" + (f"  ({detail})" if detail else ""))
    return bool(bedingung)


# ---------------------------------------------------------------------------
# Attrappen - die EINE Stelle, an der hier etwas ersetzt wird
# ---------------------------------------------------------------------------
class AttrappeClient:
    """Was python-binance an dieser Stelle liefern wuerde, mehr nicht.

    Sie merkt sich, WOMIT sie aufgerufen wurde. Dadurch prueft Abschnitt 1
    nicht nur, dass ein Aufruf durchgeht, sondern dass Symbol, Intervall und
    Lookback unveraendert bis hierher kommen - das Durchreichen ist der
    eigentliche Vertrag mit python-binance.
    """

    def __init__(self, kerzen):
        self.kerzen = kerzen
        self.aufrufe = []

    def get_historical_klines(self, symbol, interval, start_str=None,
                              *rest, **benannt):
        self.aufrufe.append((symbol, interval, start_str))
        return self.kerzen


class AttrappeClientKlasse:
    """Steht anstelle von `binance.client.Client`.

    Sie haelt fest, MIT WIE VIELEN Argumenten sie gebaut wurde. Genau daran
    zeigt sich, ob `erzeuge_client` einen vorhandenen Schluessel benutzt und
    einen fehlenden weglaesst - ohne dass ein Schluesselwert irgendwo
    ausgegeben werden muesste.
    """

    letzte_argumente = None
    KLINE_INTERVAL_1DAY = "1d"

    def __init__(self, *argumente, **benannt):
        AttrappeClientKlasse.letzte_argumente = (argumente, benannt)
        self.kerzen = []

    def get_historical_klines(self, *argumente, **benannt):
        return self.kerzen


def mit_binance_attrappe():
    """Ein `binance`-Paket vortaeuschen, solange der Block laeuft."""
    import types                                              # noqa: PLC0415

    paket = types.ModuleType("binance")
    client_modul = types.ModuleType("binance.client")
    client_modul.Client = AttrappeClientKlasse
    paket.client = client_modul
    return {"binance": paket, "binance.client": client_modul}


class _Eingesetzt:
    """sys.modules-Eintraege setzen und hinterher sauber zuruecknehmen."""

    def __init__(self, module):
        self.module = module
        self.vorher = {}

    def __enter__(self):
        for name, modul in self.module.items():
            self.vorher[name] = sys.modules.get(name)
            sys.modules[name] = modul
        return self

    def __exit__(self, *_):
        for name, alt in self.vorher.items():
            if alt is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = alt
        return False


def lade_kopie(quelltext, name):
    """Ein Modul aus Quelltext laden, ohne `fetch_binance_data` zu beruehren.

    Fuer die Mutationsproben: die Kopie bekommt einen eigenen Namen und eine
    eigene Datei, damit das echte Modul im Prozess unberuehrt bleibt.
    """
    ordner = tempfile.mkdtemp(prefix="tb37_")
    pfad = os.path.join(ordner, f"{name}.py")
    with open(pfad, "w", encoding="utf-8") as datei:
        datei.write(quelltext)
    spezifikation = importlib.util.spec_from_file_location(name, pfad)
    modul = importlib.util.module_from_spec(spezifikation)
    spezifikation.loader.exec_module(modul)
    modul._TESTORDNER = ordner
    return modul


def kerzen_aus_zeile(zeile, intervall):
    """Eine Zeile einer echten Kursdatei -> die Rohform des Endpunkts.

    Der Weg zurueck: aus `2017-08-17 04:00:00,4261.48,...` wird, was Binance
    geliefert haben muss. Damit prueft Abschnitt 5 den Rueckweg gegen eine
    Zeile, die WIRKLICH in `data/` steht - nicht gegen eine, die dieser Test
    sich selbst ausgedacht hat.
    """
    teile = zeile.strip().split(",")
    zeitpunkt = pd.Timestamp(teile[0], tz="UTC")
    millisekunden = int(zeitpunkt.timestamp() * 1000)
    # Binance liefert Zeichenketten mit acht Nachkommastellen.
    zahlen = [f"{float(wert):.8f}" for wert in teile[1:6]]
    return [millisekunden] + zahlen + ["0"] * 6


def erste_datenzeile(dateiname):
    pfad = os.path.join(BASE_DIR, "data", dateiname)
    with open(pfad, encoding="utf-8") as datei:
        kopf = datei.readline().rstrip("\n")
        erste = datei.readline().rstrip("\n")
    return kopf, erste


BEISPIELKERZEN = [
    [1502942400000, "4261.48000000", "4313.62000000", "4261.32000000",
     "4308.83000000", "47.18100900"] + ["0"] * 6,
    [1502946000000, "4308.83000000", "4328.69000000", "4291.37000000",
     "4315.32000000", "23.23491600"] + ["0"] * 6,
]


# ===========================================================================
# 1. Die Signatur - mechanisch gegen die neun Aufrufer, nicht gegen eine Liste
# ===========================================================================
def test_signatur_gegen_aufrufer():
    print("\n1. Die Signatur haelt, was die neun Aufrufer verlangen")

    sys.path.insert(0, os.path.join(BASE_DIR, "research", "zugangsdaten"))
    import geruest                                            # noqa: PLC0415

    befunde = geruest.sammle(BASE_DIR)
    sig = geruest.signatur(befunde)

    check("genau neun Module binden fetch_binance_data ein",
          len(befunde) == 9, f"{len(befunde)}: {sorted(befunde)}")
    check("jedes davon ruft fetch_historical_data mindestens einmal auf",
          all(e["aufrufe"] for e in befunde.values()),
          str([p for p, e in sorted(befunde.items()) if not e["aufrufe"]]))
    check("kein Aufrufer benutzt benannte Argumente oder * / **",
          not sig["benannt"] and not sig["stern"],
          f"benannt={sig['benannt']} stern={sig['stern']}")

    # Der Kern: die Funktion wird GENAU SO aufgerufen, wie die neun es tun -
    # drei Argumente der Reihe nach. Kein Nachbau, dieselbe Form.
    import inspect                                            # noqa: PLC0415

    unterschrift = inspect.signature(fbd.fetch_historical_data)
    pflicht = [p for p in unterschrift.parameters.values()
               if p.default is inspect.Parameter.empty
               and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
    check(f"fetch_historical_data verlangt genau {sig['mindestens']} "
          f"Argumente ohne Vorgabe",
          len(pflicht) == sig["mindestens"],
          f"{[p.name for p in pflicht]}")

    # Und jede im Repo wirklich vorkommende Kombination aus Intervall und
    # Lookback wird einmal durchgereicht.
    kombinationen = sorted({
        (a["stellung"][1].get("wert"), a["stellung"][2].get("wert"))
        for e in befunde.values() for a in e["aufrufe"]
        if len(a["stellung"]) >= 3})
    durchgereicht = True
    for intervall, lookback in kombinationen:
        attrappe = AttrappeClient(BEISPIELKERZEN)
        fbd.fetch_historical_data("BTCUSDT", intervall, lookback,
                                  client=attrappe)
        if attrappe.aufrufe != [("BTCUSDT", intervall, lookback)]:
            durchgereicht = False
    check(f"alle {len(kombinationen)} im Repo vorkommenden "
          f"(Intervall, Lookback)-Paare kommen unveraendert an",
          durchgereicht, str(kombinationen))


# ===========================================================================
# 2. Der oeffentliche Pfad laeuft OHNE Schluessel
# ===========================================================================
def test_oeffentlicher_pfad_ohne_schluessel():
    print("\n2. Ohne Schluessel: der Abruf laeuft, und er laeuft vollstaendig")

    umgebung = {}
    check("ohne Umgebung fehlen beide Namen",
          fbd.fehlende_namen(umgebung, pfad=os.devnull)
          == [fbd.SCHLUESSEL_NAME, fbd.GEHEIMNIS_NAME])

    attrappe = AttrappeClient(BEISPIELKERZEN)
    df = fbd.fetch_historical_data("BTCUSDT", "1h", "90 day ago UTC",
                                   client=attrappe)
    check("der Abruf liefert Zeilen statt einer leeren Tabelle",
          len(df) == len(BEISPIELKERZEN), f"{len(df)} Zeilen")
    check("keine Zeile geht verloren",
          list(df["close"]) == [4308.83, 4315.32], str(list(df["close"])))

    # Und der Client wird ohne Schluessel gebaut, nicht mit leeren.
    with _Eingesetzt(mit_binance_attrappe()):
        AttrappeClientKlasse.letzte_argumente = None
        fbd.erzeuge_client(umgebung={}, pfad=os.devnull,
                           ausgabe=io.StringIO())
        argumente, benannt = AttrappeClientKlasse.letzte_argumente
        check("ohne Schluessel wird Client() ohne Argumente gebaut",
              argumente == () and not benannt,
              f"{argumente!r} {benannt!r}")

        AttrappeClientKlasse.letzte_argumente = None
        fbd.erzeuge_client(umgebung={fbd.SCHLUESSEL_NAME: "A" * 8,
                                     fbd.GEHEIMNIS_NAME: "B" * 8},
                           pfad=os.devnull, ausgabe=io.StringIO())
        argumente, benannt = AttrappeClientKlasse.letzte_argumente
        check("mit Schluessel wird Client(schluessel, geheimnis) gebaut",
              len(argumente) == 2, f"{len(argumente)} Argument(e)")


# ===========================================================================
# 3. Fehlende Schluessel: laut, aber nie blockierend
# ===========================================================================
def test_fehlende_schluessel():
    print("\n3. Fehlende Schluessel melden sich - genau einmal")

    fbd.warnung_zuruecksetzen()
    ausgabe = io.StringIO()
    erste = fbd._melde_fehlende_schluessel([fbd.SCHLUESSEL_NAME], ausgabe)
    zweite = fbd._melde_fehlende_schluessel([fbd.SCHLUESSEL_NAME], ausgabe)
    text = ausgabe.getvalue()
    check("die Meldung kommt beim ersten Mal", erste and text.strip() != "")
    check("und beim zweiten Mal nicht mehr", not zweite)
    check("sie steht genau einmal da",
          text.count(fbd.SCHLUESSEL_NAME) == 1, repr(text[:120]))
    check("sie nennt den Namen und den Ort der .env",
          fbd.SCHLUESSEL_NAME in text and ".env" in text)
    fbd.warnung_zuruecksetzen()

    # Blockieren darf sie nie - der Abruf laeuft danach weiter.
    attrappe = AttrappeClient(BEISPIELKERZEN)
    df = fbd.fetch_historical_data("BTCUSDT", "1d", "400 day ago UTC",
                                   client=attrappe)
    check("nach der Meldung laeuft der Abruf weiter", len(df) == 2)

    # Wer wirklich einen Schluessel braucht, bekommt eine Ausnahme.
    try:
        fbd.verlange_zugangsdaten(umgebung={}, pfad=os.devnull)
        check("verlange_zugangsdaten wirft ohne Schluessel", False,
              "nichts geworfen")
    except fbd.ZugangsdatenFehlen as fehler:
        check("verlange_zugangsdaten wirft ohne Schluessel", True)
        check("die Ausnahme nennt beide fehlenden Namen",
              fbd.SCHLUESSEL_NAME in str(fehler)
              and fbd.GEHEIMNIS_NAME in str(fehler))

    schluessel, geheimnis = fbd.verlange_zugangsdaten(
        umgebung={fbd.SCHLUESSEL_NAME: "A" * 8, fbd.GEHEIMNIS_NAME: "B" * 8},
        pfad=os.devnull)
    check("mit Schluessel gibt verlange_zugangsdaten beide zurueck",
          schluessel == "A" * 8 and geheimnis == "B" * 8)

    # Ein leerer Eintrag ist ein vergessener Eintrag, kein Schluessel.
    check("ein leerer Wert zaehlt als fehlend",
          fbd.fehlende_namen({fbd.SCHLUESSEL_NAME: "   ",
                              fbd.GEHEIMNIS_NAME: ""}, pfad=os.devnull)
          == [fbd.SCHLUESSEL_NAME, fbd.GEHEIMNIS_NAME])


# ===========================================================================
# 4. Ein leeres Ergebnis wird geworfen, nicht geliefert
# ===========================================================================
def test_leeres_ergebnis():
    print("\n4. Leere Antwort: laut scheitern statt still leer liefern")

    attrappe = AttrappeClient([])
    try:
        ergebnis = fbd.fetch_historical_data("NICHTSUSDT", "1d",
                                             "400 day ago UTC",
                                             client=attrappe)
        check("eine leere Antwort wirft AbrufLeer", False,
              f"lieferte {type(ergebnis).__name__} mit {len(ergebnis)} Zeilen")
    except fbd.AbrufLeer as fehler:
        check("eine leere Antwort wirft AbrufLeer", True)
        check("die Ausnahme nennt Symbol und Intervall",
              "NICHTSUSDT" in str(fehler) and "1d" in str(fehler))

    # Und der Aufrufer wird davon nicht umgebracht: alle neun fangen
    # `Exception` je Symbol ab. Das ist hier nachgestellt, damit der Satz
    # "blockiert den Live-Betrieb nicht" nicht nur behauptet ist.
    geschafft, gescheitert = [], []
    for symbol, kerzen in (("BTCUSDT", BEISPIELKERZEN), ("NICHTSUSDT", []),
                           ("ETHUSDT", BEISPIELKERZEN)):
        try:
            fbd.fetch_historical_data(symbol, "1d", "400 day ago UTC",
                                      client=AttrappeClient(kerzen))
            geschafft.append(symbol)
        except Exception:                                     # noqa: BLE001
            gescheitert.append(symbol)
    check("ein leeres Symbol stoppt die Schleife der Aufrufer nicht",
          geschafft == ["BTCUSDT", "ETHUSDT"] and gescheitert == ["NICHTSUSDT"],
          f"{geschafft} / {gescheitert}")


# ===========================================================================
# 5. Die Rueckgabeform - und was to_csv daraus macht
# ===========================================================================
def test_rueckgabeform():
    print("\n5. Rueckgabeform: dieselbe Schreibweise wie die Dateien in data/")

    df = fbd.als_dataframe(BEISPIELKERZEN)
    check("genau die sechs Spalten, in dieser Reihenfolge",
          list(df.columns) == fbd.SPALTEN, str(list(df.columns)))
    check("close_time ist NICHT dabei", "close_time" not in df.columns)
    check("open_time ist ein zeitzonenfreier Zeitstempel",
          str(df["open_time"].dtype).startswith("datetime64")
          and getattr(df["open_time"].dtype, "tz", None) is None,
          str(df["open_time"].dtype))
    check("die fuenf Kursspalten sind float",
          all(str(df[s].dtype).startswith("float")
              for s in ("open", "high", "low", "close", "volume")),
          str({s: str(df[s].dtype) for s in fbd.SPALTEN}))
    check("die Zeilen stehen aufsteigend nach open_time",
          list(df["open_time"]) == sorted(df["open_time"]))

    # Der eigentliche Punkt: was `to_csv` schreibt, muss zeichengleich mit
    # dem sein, was in data/ steht. Sonst aendert sich der Datenstand-Hash,
    # ohne dass ein Kurs anders waere.
    for dateiname, intervall in (("BTCUSDT_1h.csv", "1h"),
                                 ("BTCUSDT_4h.csv", "4h"),
                                 ("BTCUSDT_1d.csv", "1d")):
        kopf, echte_zeile = erste_datenzeile(dateiname)
        kerze = kerzen_aus_zeile(echte_zeile, intervall)
        puffer = io.StringIO()
        fbd.als_dataframe([kerze]).to_csv(puffer, index=False)
        geschrieben = puffer.getvalue().splitlines()
        check(f"{dateiname}: Kopfzeile zeichengleich",
              geschrieben[0] == kopf, f"{geschrieben[0]!r} != {kopf!r}")
        check(f"{dateiname}: Datenzeile zeichengleich",
              geschrieben[1] == echte_zeile,
              f"{geschrieben[1]!r} != {echte_zeile!r}")


# ===========================================================================
# 6. Die laufende Kerze bleibt drin - und abrufschutz schneidet sie ab
# ===========================================================================
def test_laufende_kerze_bleibt():
    print("\n6. Die laufende Kerze wird NICHT hier gefiltert")

    import abrufschutz                                        # noqa: PLC0415

    # Zwei Tageskerzen: eine abgeschlossene und eine, die gerade laeuft.
    gestern = pd.Timestamp("2026-09-14")
    heute = pd.Timestamp("2026-09-15")
    kerzen = [
        [int(gestern.timestamp() * 1000), "1", "2", "0.5", "1.5", "10"]
        + ["0"] * 6,
        [int(heute.timestamp() * 1000), "1.5", "2.5", "1", "2", "5"]
        + ["0"] * 6,
    ]
    df = fbd.fetch_historical_data("BTCUSDT", "1d", "400 day ago UTC",
                                   client=AttrappeClient(kerzen))
    check("beide Kerzen kommen an - auch die laufende", len(df) == 2,
          f"{len(df)}")

    stand = heute + pd.Timedelta(hours=6)          # mitten im heutigen Tag
    gefiltert, laufend = abrufschutz.nur_abgeschlossene(
        df, "1d", stand=stand.to_pydatetime(), symbol="BTCUSDT")
    check("abrufschutz erkennt die laufende Kerze und schneidet sie ab",
          len(gefiltert) == 1 and laufend == 1, f"{len(gefiltert)}/{laufend}")
    check("die abgeschlossene Kerze bleibt stehen",
          list(gefiltert["open_time"]) == [gestern])
    print("       -> Wuerde hier gefiltert, waere abrufschutz wirkungslos "
          "und die\n          fuenf forward_test.py laesen mit df.iloc[-1] "
          "eine andere Kerze.")


# ===========================================================================
# 7. Die .env: lesen, aber nie ueberschreiben
# ===========================================================================
def test_env_lesen():
    print("\n7. Die .env wird gelesen - und ueberstimmt die Umgebung nicht")

    with tempfile.TemporaryDirectory() as ordner:
        pfad = os.path.join(ordner, ".env")
        with open(pfad, "w", encoding="utf-8") as datei:
            datei.write("# ein Kommentar\n"
                        "\n"
                        f"{fbd.SCHLUESSEL_NAME}=aus-der-datei\n"
                        f'export {fbd.GEHEIMNIS_NAME}="in-anfuehrungszeichen"\n'
                        "OHNE_GLEICHHEITSZEICHEN\n"
                        "LEER=\n")
        werte = fbd.lies_env(pfad)
        check("Kommentar- und Leerzeilen werden uebergangen",
              "# ein Kommentar" not in werte)
        check("eine Zeile ohne = wird uebergangen",
              "OHNE_GLEICHHEITSZEICHEN" not in werte, str(sorted(werte)))
        check("ein fuehrendes `export` stoert nicht",
              werte.get(fbd.GEHEIMNIS_NAME) == "in-anfuehrungszeichen",
              repr(werte.get(fbd.GEHEIMNIS_NAME)))
        check("Anfuehrungszeichen werden entfernt",
              not werte.get(fbd.GEHEIMNIS_NAME, "").startswith('"'))
        check("ein leerer Wert wird als leer gelesen", werte.get("LEER") == "")

        # Was schon in der Umgebung steht, gewinnt - und die Umgebung wird
        # dabei NICHT veraendert.
        umgebung = {fbd.SCHLUESSEL_NAME: "aus-der-umgebung"}
        schluessel, geheimnis = fbd.zugangsdaten(umgebung, pfad)
        check("die Umgebung gewinnt gegen die .env",
              schluessel == "aus-der-umgebung", str(schluessel))
        check("was nur in der .env steht, wird von dort genommen",
              geheimnis == "in-anfuehrungszeichen", str(geheimnis))
        check("die Umgebung wird dabei nicht veraendert",
              umgebung == {fbd.SCHLUESSEL_NAME: "aus-der-umgebung"},
              str(sorted(umgebung)))

        # Und os.environ schon gar nicht: die .env dieses Projekts traegt
        # auch Telegram- und Testnet-Angaben.
        vorher = dict(os.environ)
        fbd.zugangsdaten(pfad=pfad)
        check("os.environ bleibt unberuehrt", dict(os.environ) == vorher,
              str(sorted(set(os.environ) - set(vorher))))

    check("eine fehlende .env ist kein Fehler",
          fbd.lies_env(os.path.join(ordner, "gibtsnicht")) == {})


# ===========================================================================
# 8. Kein Wert, der wie ein Schluessel aussieht - nirgends
# ===========================================================================
# Die Dateien, die TB-37 dem Repo hinzufuegt oder aendert. Sie werden hier
# namentlich geprueft, damit die Pruefung nicht an einem `git`-Aufruf haengt,
# der in einem Abbild ohne Historie ins Leere liefe.
TB37_DATEIEN = [
    "shared/fetch_binance_data.py",
    "shared/test_fetch_binance_data.py",
    ".env.beispiel",
    ".gitignore",
    "research/zugangsdaten/geruest.py",
    "research/zugangsdaten/gitignoriert.py",
    "research/zugangsdaten/BERICHT.md",
    "docs/TESTAUFTRAG_TB-37_zugangsdaten.md",
    "docs/ERGEBNIS_TB-37_zugangsdaten.md",
]

# Ein Binance-Schluessel ist 64 Zeichen aus Buchstaben und Ziffern, gemischt
# gross und klein. Ein Datenstand-Hash ist ebenfalls lang, aber reines
# Kleinhex - deshalb die Bedingung "mindestens ein Grossbuchstabe": sonst
# schluege diese Pruefung bei jedem erwaehnten Hash an (etwa dem der
# Vorregistrierung) und waere binnen einer Woche abgeschaltet.
_LANGES_WORT = re.compile(r"[A-Za-z0-9]{32,}")

# Was nach `BINANCE_API_KEY=` stehen darf: nichts. Alles andere waere ein
# Wert. Ein Satzzeichen ist aber kein Wert - `BINANCE_API_KEY=` am Ende
# eines Fliesstextes endet oft auf einem Anfuehrungszeichen oder Punkt.
# Deshalb: mindestens acht Zeichen aus dem Alphabet, aus dem Schluessel
# bestehen.
_WERT_HINTER_NAMEN = re.compile(r"[A-Za-z0-9_+/=-]{8,}")


def _verdaechtige_woerter(text):
    treffer = []
    for wort in _LANGES_WORT.findall(text):
        if not any(z.isupper() for z in wort):
            continue                       # reines Kleinhex: ein Hash
        if not any(z.isdigit() for z in wort):
            continue                       # ein langer Bezeichner
        treffer.append(wort)
    return treffer


def erfundener_schluessel(salz):
    """Etwas, das die Form eines Schluessels hat - ohne im Quelltext zu stehen.

    Abschnitt 8 muss zweierlei zeigen: dass in keiner TB-37-Datei ein
    schluesselfoermiges Wort steht, UND dass die Pruefung eines erkennen
    wuerde. Beides zugleich geht nur, wenn die Probe zur Laufzeit entsteht.
    Ein hineingeschriebener Platzhalter waere genau das, was hier verboten
    ist - und er wuerde die Pruefung, die er belegen soll, selbst
    ausloesen.
    """
    import hashlib                                            # noqa: PLC0415

    roh = hashlib.sha256(salz.encode("utf-8")).hexdigest()
    # Hex ist Kleinschrift; jedes dritte Zeichen gross gibt die gemischte
    # Form, an der `_verdaechtige_woerter` einen Schluessel erkennt.
    return "".join(z.upper() if i % 3 == 0 else z
                   for i, z in enumerate(roh))


def repo_dateien():
    """Die vom Repo verfolgten Textdateien.

    Ueber `git ls-files`, und das ist wichtig: so kommt die **echte** `.env`
    des Betreibers hier nie vor. Sie ist gitignoriert, dieser Test liest sie
    also nicht - und kann folglich auch nichts aus ihr ausgeben. Ohne git
    (etwa in einem Abbild ohne Historie) bleibt die Liste der TB-37-Dateien.
    """
    gefunden = set(TB37_DATEIEN)
    try:
        # `--cached --others --exclude-standard`: verfolgte UND neue, aber
        # keine ignorierten. Ein blosses `git ls-files` liesse die Dateien
        # aus, die gerade erst hinzugekommen sind - also ausgerechnet die,
        # die noch niemand angesehen hat.
        lauf = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=BASE_DIR, capture_output=True, text=True, timeout=60)
        if lauf.returncode == 0 and lauf.stdout.strip():
            endungen = (".py", ".md", ".txt", ".json", ".sh", ".yml",
                        ".yaml", ".cfg", ".beispiel", ".gitignore")
            gefunden.update(z for z in lauf.stdout.splitlines()
                            if z.endswith(endungen)
                            or os.path.basename(z) == ".gitignore")
    except (OSError, subprocess.SubprocessError):
        pass
    return sorted(gefunden)


def test_keine_schluessel_im_repo():
    print("\n8. In keiner TB-37-Datei steht ein Wert hinter einem Namen")

    # a) Der Name darf vorkommen. Ein Wert dahinter nie - und das gilt fuer
    #    JEDE vom Repo verfolgte Datei, nicht nur fuer die neun von TB-37.
    muster = re.compile(
        rf"({re.escape(fbd.SCHLUESSEL_NAME)}|{re.escape(fbd.GEHEIMNIS_NAME)})"
        rf"\s*[=:]\s*(\S+)")
    verfolgt = repo_dateien()
    check("die Dateiliste des Repos ist nicht leer", len(verfolgt) > 50,
          f"{len(verfolgt)} Dateien")
    befunde = []
    for rel in verfolgt:
        pfad = os.path.join(BASE_DIR, rel)
        if not os.path.exists(pfad):
            continue
        try:
            with open(pfad, encoding="utf-8") as datei:
                zeilen = list(enumerate(datei, 1))
        except (OSError, UnicodeDecodeError):
            continue
        for nummer, zeile in zeilen:
            for name, wert in muster.findall(zeile):
                sauber = wert.strip("\"',.;:`)")
                # `NAME = "BINANCE_API_KEY"` ist die Definition des Namens
                # selbst, kein Wert dahinter.
                if sauber in (fbd.SCHLUESSEL_NAME, fbd.GEHEIMNIS_NAME):
                    continue
                if not _WERT_HINTER_NAMEN.fullmatch(sauber):
                    continue        # Satzzeichen, Backtick, Fliesstext
                befunde.append(f"{rel}:{nummer} {name}")
    check(f"in keiner der {len(verfolgt)} verfolgten Dateien steht ein Wert "
          f"hinter dem Namen", not befunde, "; ".join(befunde))

    # b) Und ganz unabhaengig davon: kein langes Wort, das wie ein Schluessel
    #    aussieht - in den Dateien, die TB-37 hinzufuegt.
    lang = []
    for rel in TB37_DATEIEN:
        pfad = os.path.join(BASE_DIR, rel)
        if not os.path.exists(pfad):
            continue
        with open(pfad, encoding="utf-8") as datei:
            for nummer, zeile in enumerate(datei, 1):
                for wort in _verdaechtige_woerter(zeile):
                    lang.append(f"{rel}:{nummer} {wort[:4]}...")
    check("keine TB-37-Datei enthaelt ein schluesselfoermiges Wort",
          not lang, "; ".join(lang))

    # c) Die Pruefung selbst muss anschlagen koennen - sonst ist sie Zierde.
    #    Die Probe entsteht zur Laufzeit und steht deshalb in keiner Datei.
    probe = erfundener_schluessel("tb37-probe")
    zeile = f"{fbd.SCHLUESSEL_NAME}={probe}"
    check("die Pruefung erkennt einen erfundenen Schluessel",
          bool(_verdaechtige_woerter(zeile)) and bool(muster.findall(zeile)),
          f"{len(probe)} Zeichen")
    check("und sie schlaegt bei einem blossen Namen ohne Wert NICHT an",
          not _verdaechtige_woerter(f"{fbd.SCHLUESSEL_NAME}=")
          and not _verdaechtige_woerter(
              f"`{fbd.SCHLUESSEL_NAME}=` in der .env ist leer"))

    # d) `.env.beispiel` ist im Repo, `.env` ist es nicht.
    check(".env.beispiel liegt im Repo",
          os.path.exists(os.path.join(BASE_DIR, ".env.beispiel")))
    with open(os.path.join(BASE_DIR, ".gitignore"), encoding="utf-8") as datei:
        ignoriert = datei.read()
    check(".gitignore schliesst .env weiterhin aus", "\n.env\n" in ignoriert)
    check(".gitignore schliesst fetch_binance_data NICHT mehr aus",
          not any(z.strip() == "shared/fetch_binance_data.py"
                  for z in ignoriert.splitlines()))

    # e) Der Selbstbericht des Moduls gibt keinen Wert aus.
    umgebung = dict(os.environ)
    umgebung[fbd.SCHLUESSEL_NAME] = erfundener_schluessel("schluessel")
    umgebung[fbd.GEHEIMNIS_NAME] = erfundener_schluessel("geheimnis")
    lauf = subprocess.run([sys.executable, MODULPFAD], capture_output=True,
                          text=True, env=umgebung, cwd=BASE_DIR, timeout=60)
    ausgabe = lauf.stdout + lauf.stderr
    check("der Selbstbericht laeuft durch", lauf.returncode == 0,
          ausgabe[-200:])
    check("der Selbstbericht gibt KEINEN Wert aus",
          umgebung[fbd.SCHLUESSEL_NAME] not in ausgabe
          and umgebung[fbd.GEHEIMNIS_NAME] not in ausgabe)
    check("er sagt trotzdem, dass die Namen gesetzt sind",
          "gesetzt" in ausgabe, ausgabe[:200])

    # f) Auch eine Ausnahme verraet nichts.
    halb = erfundener_schluessel("nur-der-schluessel")
    try:
        fbd.verlange_zugangsdaten(umgebung={fbd.SCHLUESSEL_NAME: halb},
                                  pfad=os.devnull)
        check("die Ausnahme verraet den halben Schluessel nicht", False,
              "nichts geworfen")
    except fbd.ZugangsdatenFehlen as fehler:
        check("die Ausnahme verraet den vorhandenen Schluessel nicht",
              halb not in str(fehler) and halb[:12] not in str(fehler),
              str(fehler)[:120])


# ===========================================================================
# 8b. Die Namen sind nicht erfunden - broker/zugang.py nennt sie schon
# ===========================================================================
def test_namen_stimmen_mit_broker():
    print("\n8b. Die Schluesselnamen stimmen mit broker/zugang.py ueberein")

    # `broker/zugang.py` fuehrt seit jeher eine Liste der Variablen, die zum
    # KURSDATENABRUF gehoeren, und bricht ab, wenn ein Testnet-Schluessel mit
    # einer davon uebereinstimmt. Die Namen dieses Moduls muessen dieselben
    # sein - sonst greift jene Verwechslungssperre ins Leere.
    #
    # Gelesen wird ueber den Syntaxbaum, NICHT ueber einen Import: alles
    # unter broker/ bleibt bei TB-37 unberuehrt, und ein Import zoege
    # dessen Modulebene in diesen Test.
    import ast                                                # noqa: PLC0415

    pfad = os.path.join(BASE_DIR, "broker", "zugang.py")
    with open(pfad, encoding="utf-8") as datei:
        baum = ast.parse(datei.read())
    gefunden = None
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign) and any(
                isinstance(z, ast.Name) and z.id == "DATENABRUF_VARIABLEN"
                for z in knoten.targets):
            gefunden = tuple(e.value for e in knoten.value.elts)
    check("broker/zugang.py fuehrt DATENABRUF_VARIABLEN", gefunden is not None)
    check("die beiden Namen stimmen ueberein",
          gefunden == (fbd.SCHLUESSEL_NAME, fbd.GEHEIMNIS_NAME),
          f"broker: {gefunden}, hier: "
          f"{(fbd.SCHLUESSEL_NAME, fbd.GEHEIMNIS_NAME)}")
    print("       -> Die Namen sind damit nicht geraten, sondern die im Repo\n"
          "          bereits dokumentierten. broker/zugang.py:101.")

    # Und: das `.env`-Format ist dasselbe. broker/zugang.py und
    # notifications/telegram_config.py lesen `NAME=WERT`, `#` als Kommentar,
    # Anfuehrungszeichen weg. Hier wird nachgesehen, ob beide Leser bei
    # derselben Datei dasselbe herausbekommen - nicht, ob der Quelltext
    # gleich aussieht.
    with tempfile.TemporaryDirectory() as ordner:
        env = os.path.join(ordner, ".env")
        with open(env, "w", encoding="utf-8") as datei:
            datei.write("# Kommentar\n"
                        "EINFACH=abc\n"
                        'MIT_ANFUEHRUNG="def"\n'
                        "MIT_HOCHKOMMA='ghi'\n"
                        "LEER=\n"
                        "OHNE_GLEICH\n")
        meins = fbd.lies_env(env)

        # broker/zugang.py._parse_env_file, ohne broker/ zu importieren:
        # derselbe Quelltext, in einem eigenen Modul ausgefuehrt.
        with open(pfad, encoding="utf-8") as datei:
            quelle = datei.read()
        anfang = quelle.index("def _parse_env_file")
        ende = quelle.index("def _aus_umgebung")
        fremd_modul = lade_kopie("import os\n\n" + quelle[anfang:ende],
                                 "tb37_broker_parser")
        try:
            fremd = fremd_modul._parse_env_file(env)
        finally:
            shutil.rmtree(fremd_modul._TESTORDNER, ignore_errors=True)
            sys.modules.pop("tb37_broker_parser", None)

        check("beide .env-Leser kommen zum selben Ergebnis",
              meins == fremd, f"hier {meins}, broker {fremd}")


# ===========================================================================
# 9. Mutationsproben: jede Absicherung einzeln abschalten
# ===========================================================================
# Je Mutation: die Marke, die ersetzt wird, und die Pruefung, die danach
# fallen MUSS. Die uebrigen muessen stehen bleiben - sonst sagt die Probe
# nichts ueber die einzelne Absicherung, sondern nur, dass das Modul kaputt
# ist.
MUTATIONEN = [
    ("leere Antwort wird geworfen",
     "    if not kerzen:\n        raise AbrufLeer(",
     "    if False:\n        raise AbrufLeer(",
     "leer"),
    ("Meldung kommt nur einmal",
     "    if _GEWARNT or not fehlt:\n        return False",
     "    if not fehlt:\n        return False",
     "einmal"),
    ("Kurse werden zu float",
     '        "close": [float(k[4]) for k in kerzen],',
     '        "close": [k[4] for k in kerzen],',
     "schreibweise"),
    ("verlange_zugangsdaten wirft",
     "        raise ZugangsdatenFehlen(",
     "        return None, None\n        raise ZugangsdatenFehlen(",
     "verlangt"),
    (".env ueberstimmt die Umgebung nicht",
     "    return ziel.get(name) or aus_datei.get(name)",
     "    return aus_datei.get(name) or ziel.get(name)",
     "umgebung"),
]


def _proben(modul):
    """Die fuenf Pruefungen, die je eine Absicherung bewachen.

    Jede gibt True zurueck, wenn die Absicherung greift. Sie laufen gegen
    ein uebergebenes Modul - das echte oder eine mutierte Kopie -, damit
    beide Male derselbe Ablauf beobachtet wird und nicht zwei verschiedene.
    """
    ergebnis = {}

    try:
        modul.fetch_historical_data("X", "1d", "400 day ago UTC",
                                    client=AttrappeClient([]))
        ergebnis["leer"] = False
    except modul.AbrufLeer:
        ergebnis["leer"] = True
    except Exception:                                         # noqa: BLE001
        ergebnis["leer"] = False

    modul.warnung_zuruecksetzen()
    puffer = io.StringIO()
    modul._melde_fehlende_schluessel([modul.SCHLUESSEL_NAME], puffer)
    modul._melde_fehlende_schluessel([modul.SCHLUESSEL_NAME], puffer)
    ergebnis["einmal"] = puffer.getvalue().count(modul.SCHLUESSEL_NAME) == 1
    modul.warnung_zuruecksetzen()

    kopf, zeile = erste_datenzeile("BTCUSDT_1h.csv")
    puffer = io.StringIO()
    modul.als_dataframe([kerzen_aus_zeile(zeile, "1h")]).to_csv(puffer,
                                                                index=False)
    ergebnis["schreibweise"] = puffer.getvalue().splitlines()[1] == zeile

    try:
        modul.verlange_zugangsdaten(umgebung={}, pfad=os.devnull)
        ergebnis["verlangt"] = False
    except modul.ZugangsdatenFehlen:
        ergebnis["verlangt"] = True
    except Exception:                                         # noqa: BLE001
        ergebnis["verlangt"] = False

    with tempfile.TemporaryDirectory() as ordner:
        pfad = os.path.join(ordner, ".env")
        with open(pfad, "w", encoding="utf-8") as datei:
            datei.write(f"{modul.SCHLUESSEL_NAME}=aus-der-datei\n"
                        f"{modul.GEHEIMNIS_NAME}=aus-der-datei\n")
        umgebung = {modul.SCHLUESSEL_NAME: "aus-der-umgebung",
                    modul.GEHEIMNIS_NAME: "aus-der-umgebung"}
        schluessel, _ = modul.zugangsdaten(umgebung, pfad)
        ergebnis["umgebung"] = schluessel == "aus-der-umgebung"
    return ergebnis


def test_mutationsproben():
    print("\n9. Mutationsproben: Absicherung aus -> die zugehoerige Pruefung "
          "muss fallen")

    with open(MODULPFAD, encoding="utf-8") as datei:
        quelltext = datei.read()

    vorher = _proben(fbd)
    check("am unveraenderten Modul greifen alle fuenf Absicherungen",
          all(vorher.values()), str(vorher))

    for nummer, (titel, marke, ersatz, schluessel) in enumerate(MUTATIONEN, 1):
        if quelltext.count(marke) != 1:
            check(f"M{nummer} {titel}: Mutationsstelle eindeutig", False,
                  f"{quelltext.count(marke)} Treffer")
            continue
        check(f"M{nummer} {titel}: Mutationsstelle eindeutig", True)

        kopie = lade_kopie(quelltext.replace(marke, ersatz),
                           f"fbd_mutiert_{nummer}")
        try:
            nachher = _proben(kopie)
        finally:
            shutil.rmtree(kopie._TESTORDNER, ignore_errors=True)
            sys.modules.pop(f"fbd_mutiert_{nummer}", None)

        check(f"M{nummer} {titel}: die zugehoerige Pruefung faellt",
              nachher[schluessel] is False,
              f"{schluessel} blieb {nachher[schluessel]}")
        # Die zweite Falle: wenn hier ALLES faellt, sagt die Probe nichts
        # ueber die einzelne Absicherung.
        andere = {k: v for k, v in nachher.items() if k != schluessel}
        check(f"M{nummer} {titel}: die uebrigen vier bleiben stehen",
              all(andere.values()), str(andere))

    fbd.warnung_zuruecksetzen()
    print("       -> Jede der fuenf Pruefungen haengt also an genau ihrer "
          "Absicherung\n          und wird von keiner anderen mitgetragen.")


# ===========================================================================
def main():
    print("=" * 78)
    print("SELBSTTESTS shared/fetch_binance_data.py (TB-37)")
    print("=" * 78)

    tests = [
        ("test_signatur_gegen_aufrufer", test_signatur_gegen_aufrufer),
        ("test_oeffentlicher_pfad_ohne_schluessel",
         test_oeffentlicher_pfad_ohne_schluessel),
        ("test_fehlende_schluessel", test_fehlende_schluessel),
        ("test_leeres_ergebnis", test_leeres_ergebnis),
        ("test_rueckgabeform", test_rueckgabeform),
        ("test_laufende_kerze_bleibt", test_laufende_kerze_bleibt),
        ("test_env_lesen", test_env_lesen),
        ("test_keine_schluessel_im_repo", test_keine_schluessel_im_repo),
        ("test_namen_stimmen_mit_broker", test_namen_stimmen_mit_broker),
        ("test_mutationsproben", test_mutationsproben),
    ]

    for name, test in tests:
        try:
            test()
        except Exception as fehler:                            # noqa: BLE001
            import traceback
            FEHLER.append(f"{name} (Ausnahme)")
            print(f"  [FEHLER] {name} warf eine Ausnahme: {fehler}")
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
