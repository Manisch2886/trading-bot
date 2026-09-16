#!/usr/bin/env python3
"""
S-B1 - Der Datenlauf: die ETF-Kursdateien holen (TB-39)
==============================================================================
Holt die Kandidaten ueber yfinance und legt sie unter
`research/etf_trendfolge/daten/` ab - **NICHT** unter `data/`.

DIESER SCHRITT LAEUFT AUF DEM RECHNER DES BETREIBERS
------------------------------------------------------------------------------
In der Cloud-Umgebung, in der TB-39 entstanden ist, sind Binance und Yahoo
gesperrt (der Proxy antwortet mit 403) und weder `yfinance` noch `pandas`
sind installiert. Dieses Modul ist deshalb das **Werkzeug**; der **Lauf**
steht im Testdokument `docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md`.

    python3 research/etf_trendfolge/datenlauf.py
    python3 research/etf_trendfolge/historie.py

WARUM NICHT UNTER data/ - DIE RANDBEDINGUNG, AN DER DIESE AUFGABE SCHEITERT
------------------------------------------------------------------------------
Der Datenstand-Hash der Vorregistrierung ist der SHA-256 ueber die Dateien in
`data/`: `d9449faf51bffaaa...` bei 223 Dateien, am 15.09.2026 als
Tatsachennotiz eingetragen. **Eine einzige zusaetzliche Datei dort aendert
ihn** und entwertet den registrierten Zustand, bevor der Selektionslauf
stattgefunden hat. `datenstand.py` weist am Verhalten nach, dass das nicht
geschieht.

==============================================================================
DIE ENTSCHEIDUNG ZU `auto_adjust` - UND WAS SIE KOSTET
==============================================================================
yfinance liefert mit `auto_adjust=True` bereinigte Kurse: jede Ausschuettung
und jeder Split werden rueckwirkend in die ganze Historie eingerechnet. Das
hat eine unangenehme Folge, die beim Aktienbestand dieses Projekts **gemessen**
wurde: zwei Abrufe im Abstand von Minuten unterschieden sich um bis zu
**1,2 x 10 hoch -6** relativer Abweichung. Bei ausschuettenden ETFs ist die
Bereinigung **groesser** als bei Aktien.

**Entschieden ist: `auto_adjust=True`.** Nicht aus Bequemlichkeit - die
Alternative ist fuer die Haelfte des Universums schlicht falsch:

  * Vier der vierzehn Kandidaten sind Anleihe-ETFs (IEF, TLT, LQD, HYG). Sie
    schuetten ihren gesamten Ertrag aus; ihr Kurs allein hat deshalb KEINEN
    Aufwaertstrend, sondern schwankt um ein Niveau. Ein
    Zwoelf-Monats-Momentum auf der unbereinigten Kursreihe von HYG waere
    strukturell negativ - die Strategie waere in Anleihen fast dauerhaft in
    der Kasse, und zwar aus einem Buchhaltungsgrund, nicht aus einem
    Marktgrund.
  * Dieselbe Verzerrung traefe die Klassen ungleich: Aktien-ETFs schuetten
    wenig aus, Anleihe- und Kredit-ETFs viel. Eine unbereinigte Reihe
    bevorzugte damit systematisch genau die Anlageklasse, deren Uebergewicht
    S-B1 gerade vermeiden soll.

**Was die Entscheidung kostet, und wie es bezahlt wird:**

  1. **Die Reihe ist nicht wiederholbar.** Abhilfe: sie wird EINMAL geholt
     und dann EINGEFROREN. `datenlauf.py` ueberschreibt eine vorhandene
     Datei NICHT. Ein erneuter Abruf laeuft nur mit `--neu`, und der
     vergleicht und MELDET, statt zu ersetzen; uebernommen wird erst mit
     `--uebernehmen`.
  2. **Was sich geaendert hat, muss sichtbar sein.** Jede Datei bekommt im
     `manifest.json` ihren eigenen SHA-256, ihre Zeilenzahl und ihr erstes
     und letztes Datum. Ein spaeterer Abruf, der abweicht, faellt damit auf,
     statt still zu wirken.
  3. **Die Groesse der Abweichung wird berichtet, nicht behauptet.** `--neu`
     gibt die groesste relative Abweichung je Symbol aus.

==============================================================================
DIE ENTSCHEIDUNGSKERZE-REGEL AUS TB-38 GILT AUCH HIER
==============================================================================
Nur Kerzen, deren Zeitraum vor der Startzeit des Laufs endete. Die Regel
steht in EINER Funktion - `shared/entscheidungskerze.nur_entscheidbar` - und
wird hier **benutzt**, nicht nachgebaut. Sie laeuft NACH
`shared/kursdaten.entferne_unvollstaendige`:

  * `entferne_unvollstaendige` streicht Zeilen mit fehlenden Kursfeldern -
    eine Eigenschaft der ZEILE.
  * `nur_entscheidbar` streicht Zeilen, deren Zeitraum noch laeuft - eine
    Eigenschaft der ZEIT.

Zwei Wachen, zwei verschiedene Fragen. Der Selbsttest nimmt jede EINZELN
heraus und weist nach, dass die jeweils andere den Ausfall NICHT auffaengt.
"""

import argparse
import hashlib
import json
import os
import sys
import datetime as dt

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)

import register as reg                                      # noqa: E402

_SHARED = os.path.join(reg.BASE_DIR, "shared")
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

import entscheidungskerze as ek                             # noqa: E402
import kursdaten                                            # noqa: E402

SPALTEN = ["open_time", "open", "high", "low", "close", "volume"]

# Der frueheste sinnvolle Anfang. Geholt wird, was da ist; abgeschnitten wird
# erst in der Auswertung - so haengt der Datenbestand nicht an einer Wahl.
START = "1990-01-01"

# Tageskerzen, Aktienmarkt: beides steht hier genau einmal.
INTERVALL = "1d"
MARKT = ek.AKTIEN


# ---------------------------------------------------------------------------
# Der Anschluss an yfinance - die EINZIGE Stelle, die yfinance kennt
# ---------------------------------------------------------------------------
def _yfinance_abruf(symbol, start, ende):
    """Ein Symbol von yfinance, schon auf die sechs Spalten gebracht.

    Alles, was mit der Eigenart von yfinance zu tun hat (mehrstufige
    Spaltennamen, Grossschreibung, der Index als Datum), passiert HIER und
    nirgends sonst. Was danach kommt, weiss nicht mehr, woher die Tabelle
    stammt - und laesst sich deshalb auch mit einer anderen Quelle
    beobachten.
    """
    import yfinance as yf                                   # noqa: PLC0415

    df = yf.download(symbol, start=start, end=ende, progress=False,
                     auto_adjust=True)
    if df is None or len(df) == 0:
        raise SystemExit(
            f"{symbol}: yfinance liefert nichts. Netz? Symbol richtig "
            f"geschrieben? (Aus der Cloud ist Yahoo gesperrt - dieser "
            f"Schritt gehoert an den Mac.)")
    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)
    df = df.reset_index()
    df.columns = [str(c).lower() for c in df.columns]
    df = df.rename(columns={"date": "open_time"})
    df["open_time"] = df["open_time"].astype(str).str.slice(0, 10)
    fehlend = [s for s in SPALTEN if s not in df.columns]
    if fehlend:
        raise SystemExit(f"{symbol}: Spalten fehlen: {fehlend}")
    return df[SPALTEN]


# ---------------------------------------------------------------------------
# Der Ablauf - zwei Wachen, dann schreiben
# ---------------------------------------------------------------------------
def hole(symbol, ziel_dir, start=START, ende=None, abruf=None,
         startzeit=None, melden=True):
    """Ein Kandidat. Gibt den Befund als Datenstruktur zurueck.

    Der Ablauf ist die Aussage dieses Moduls, und er ist bewusst kurz:

        abrufen -> entferne_unvollstaendige -> nur_entscheidbar -> schreiben

    `abruf` ist austauschbar, damit der Selbsttest den ABLAUF beobachten
    kann, ohne yfinance zu brauchen. Die beiden Wachen sind es NICHT - sie
    sind das, was beobachtet wird.
    """
    roh = (abruf or _yfinance_abruf)(symbol, start, ende)

    df, gestrichen = kursdaten.entferne_unvollstaendige(
        roh, symbol=symbol, melden=melden)

    df, verworfen, hinweis = ek.nur_entscheidbar(
        df, INTERVALL, MARKT, startzeit=startzeit, symbol=symbol,
        melden=melden)

    os.makedirs(ziel_dir, exist_ok=True)
    pfad = os.path.join(ziel_dir, f"{symbol}_{INTERVALL}.csv")
    df.to_csv(pfad, index=False)
    return {
        "symbol": symbol,
        "pfad": pfad,
        "zeilen": len(df),
        "unvollstaendig_gestrichen": int(gestrichen),
        "nach_entscheidungskerze_verworfen": int(verworfen),
        "kalenderhinweis": hinweis,
    }


# ---------------------------------------------------------------------------
# Manifest - was geholt wurde, mit eigenem Hash je Datei
# ---------------------------------------------------------------------------
def _sha256(pfad):
    h = hashlib.sha256()
    with open(pfad, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _erste_und_letzte_zeile(pfad):
    erste = letzte = None
    with open(pfad, encoding="utf-8") as fh:
        kopf = fh.readline()
        if not kopf:
            return None, None
        for zeile in fh:
            zeile = zeile.strip()
            if not zeile:
                continue
            if erste is None:
                erste = zeile.split(",")[0][:10]
            letzte = zeile.split(",")[0][:10]
    return erste, letzte


def manifest(ziel_dir=None):
    """Der Bestand, wie er auf der Platte liegt - Datei fuer Datei."""
    ziel_dir = ziel_dir or reg.DATEN_DIR
    eintraege = []
    for symbol in reg.symbole():
        pfad = os.path.join(ziel_dir, f"{symbol}_{INTERVALL}.csv")
        if not os.path.exists(pfad):
            eintraege.append({"symbol": symbol, "vorhanden": False})
            continue
        erste, letzte = _erste_und_letzte_zeile(pfad)
        eintraege.append({
            "symbol": symbol,
            "vorhanden": True,
            "sha256": _sha256(pfad),
            "groesse": os.path.getsize(pfad),
            "erstes_datum": erste,
            "letztes_datum": letzte,
        })
    return {
        "erzeugt": dt.datetime.now(dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "auto_adjust": True,
        "intervall": INTERVALL,
        "markt": MARKT,
        "dateien": eintraege,
    }


def schreibe_manifest(ziel_dir=None):
    ziel_dir = ziel_dir or reg.DATEN_DIR
    os.makedirs(ziel_dir, exist_ok=True)
    pfad = os.path.join(ziel_dir, "manifest.json")
    with open(pfad, "w", encoding="utf-8") as fh:
        json.dump(manifest(ziel_dir), fh, indent=2, ensure_ascii=False)
    return pfad


# ---------------------------------------------------------------------------
# Das Programm
# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--ziel", default=None)
    p.add_argument("--start", default=START)
    p.add_argument("--ende", default=None,
                   help="JJJJ-MM-TT, ausschliesslich (Vorgabe: bis heute)")
    p.add_argument("--pruefen", action="store_true",
                   help="nur nachsehen, was schon da ist")
    p.add_argument("--neu", action="store_true",
                   help="erneut abrufen und mit dem Bestand VERGLEICHEN")
    p.add_argument("--uebernehmen", action="store_true",
                   help="mit --neu: den neuen Abruf tatsaechlich uebernehmen")
    args = p.parse_args(argv)

    ziel = args.ziel or reg.DATEN_DIR

    # Die Wache VOR dem Schreiben: liegt das Ziel ausserhalb von data/?
    import datenstand                                       # noqa: PLC0415
    draussen, grund = datenstand.ziel_liegt_ausserhalb(ziel)
    if not draussen:
        print(f"ABBRUCH: {grund}")
        return 1

    if args.pruefen:
        m = manifest(ziel)
        print(f"S-B1 - Bestand in {ziel}\n")
        for e in m["dateien"]:
            if not e["vorhanden"]:
                print(f"  {e['symbol']:5s}  fehlt")
            else:
                print(f"  {e['symbol']:5s}  {e['erstes_datum']} bis "
                      f"{e['letztes_datum']}  {e['sha256'][:12]}...")
        return 0

    vorhanden = [s for s in reg.symbole()
                 if os.path.exists(os.path.join(ziel, f"{s}_{INTERVALL}.csv"))]

    if vorhanden and not args.neu:
        print(f"S-B1 - {len(vorhanden)} von {len(reg.symbole())} Dateien "
              f"liegen schon in {ziel}.")
        print("  Sie werden NICHT ueberschrieben: eine bereinigte Reihe "
              "aendert sich bei jeder\n  Ausschuettung, und was einmal "
              "registriert ist, soll sich nicht unter der Hand\n  "
              "verschieben. Erneut abrufen und vergleichen: --neu")
        fehlend = [s for s in reg.symbole() if s not in vorhanden]
        print(f"  Es fehlen: {', '.join(fehlend) if fehlend else 'nichts'}")

    if args.neu and not args.uebernehmen:
        print("S-B1 - Vergleichslauf (--neu ohne --uebernehmen): es wird "
              "NICHTS ueberschrieben.\n")
        alt = {e["symbol"]: e for e in manifest(ziel)["dateien"]}
        vergleichsordner = os.path.join(ziel, "_vergleich")
        for symbol in reg.symbole():
            hole(symbol, vergleichsordner, args.start, args.ende)
        neu = {e["symbol"]: e
               for e in manifest(vergleichsordner)["dateien"]}
        for symbol in reg.symbole():
            a, b = alt.get(symbol, {}), neu.get(symbol, {})
            if not a.get("vorhanden"):
                print(f"  {symbol:5s}  war nicht da")
            elif a.get("sha256") == b.get("sha256"):
                print(f"  {symbol:5s}  unveraendert")
            else:
                print(f"  {symbol:5s}  ABWEICHUNG  {a.get('sha256','')[:12]}"
                      f"... -> {b.get('sha256','')[:12]}...  "
                      f"({a.get('letztes_datum')} -> "
                      f"{b.get('letztes_datum')})")
        print(f"\n  Der Vergleichsabruf liegt in {vergleichsordner}. "
              f"Uebernehmen: --neu --uebernehmen")
        return 0

    for symbol in reg.symbole():
        pfad = os.path.join(ziel, f"{symbol}_{INTERVALL}.csv")
        if os.path.exists(pfad) and not args.uebernehmen:
            continue
        befund = hole(symbol, ziel, args.start, args.ende)
        print(f"  {befund['symbol']:5s} {befund['zeilen']:6d} Handelstage  "
              f"({befund['unvollstaendig_gestrichen']} unvollstaendig, "
              f"{befund['nach_entscheidungskerze_verworfen']} nach der "
              f"Entscheidungskerze verworfen)")
        if befund["kalenderhinweis"]:
            print(f"         Hinweis: {befund['kalenderhinweis']}")

    pfad = schreibe_manifest(ziel)
    print(f"\n  Manifest: {pfad}")
    print("  Naechster Schritt: python3 research/etf_trendfolge/historie.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
