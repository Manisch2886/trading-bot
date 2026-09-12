"""
Haelt die abgelegten Ergebniskurven gegen die heutige Konfiguration
==============================================================================
Die Dateien `results/<bot>/equity_curve.csv` sind keine Ablage, sondern eine
Aussage: "so verlaeuft das Kapital dieses Bots". Sie sind die Grundlage der
Montags-Mail und der Dashboard-Portfolio-Sicht (Protokoll 4.3b), solange ein
Bot unter `MIN_LIVE_CLOSED_TRADES = 10` geschlossenen Live-Trades liegt - und
das tun derzeit alle neun. Sie sind ausserdem die Grundlage praktisch jeder
Untersuchung unter `research/`.

Eine solche Datei veraltet lautlos. Aendert sich ein Parameter, ein Filter
oder der Datenpfad, beschreibt sie ab diesem Moment einen Bot, den es nicht
mehr gibt - und nichts sagt es. Genau das ist dreimal passiert:

1. `research/hrp_portfolio` musste zweimal nachgerechnet werden; ein dritter
   Nachtrag drehte die Kernaussage am selben Tag zurueck, weil EINE Kurve
   (`volatility_breakout_crypto`) den live aktiven BTC-Regimefilter nicht
   enthielt. Das Vorzeichen hing dort an 0,7 %.
2. `research/volatility_scaled_sizing` brauchte einen Nachtrag aus demselben
   Grund.
3. `research/exposure_messung` (PR #84) fand es erneut - und traf dabei
   dieselbe `elliott_wave`-Kurve mit 144 Zeilen an, die der HRP-Bericht zwei
   Tage zuvor bereits als veraltet benannt hatte.

Dieses Programm ist die Wiederholungssperre.

    python3 shared/ergebniskurven.py                 # pruefen (Rueckgabewert 1 bei Befund)
    python3 shared/ergebniskurven.py --erzeugen      # Kurven neu schreiben
    python3 shared/ergebniskurven.py --bot t3_supertrend
    python3 shared/ergebniskurven.py --nur-abweichung
    python3 shared/ergebniskurven.py --json bericht.json

WORAN DIE PRUEFUNG SICH FESTMACHT - UND WARUM
------------------------------------------------------------------------------
Sie erzeugt die Kurve neu und vergleicht sie **Zeile fuer Zeile** mit der
abgelegten. Nicht die Zeilenzahl, nicht einen Parameter-Fingerabdruck, nicht
den Zeitstempel der Datei.

Der Grund steht im HRP-Fall: dort war nicht die Zahl der Trades das Problem,
sondern ein nicht angewendeter Regimefilter. Und dieser Filter ist kein Wert
in `live_params.py`, sondern **eine Aufrufstelle im `__main__`-Block** von
`volatility_breakout_crypto/equity_simulation.py` (PR #57 - dort ausdruecklich
so platziert, weil drei Experiment-Skripte dieses Bots ueber
`collect_all_trades()` ihren ungefilterten Vergleichsdatensatz holen). Der
`live_params.py`-Diff jenes PRs bestand aus **einer geaenderten
Kommentar-Zeilennummer**; ein Fingerabdruck ueber die Parameterwerte haette
die Aenderung nicht gesehen. Ein Fingerabdruck ueber den Quelltext haette
umgekehrt jede Kommentaraenderung gemeldet - und eine Pruefung, die staendig
grundlos anschlaegt, liest bald niemand mehr.

Die einzige Groesse, die weder unvollstaendig noch verrauscht sein kann, ist
die Kurve selbst. Sie ist das, worauf sich Mail, Dashboard und Berichte
berufen; wenn sie stimmt, ist die Frage beantwortet, und wenn sie nicht
stimmt, ist es egal, welcher der moeglichen Gruende es war.

Der Preis dafuer ist Rechenzeit (rund eine halbe Minute fuer alle neun Bots,
je ein Prozess). Fuer eine naechtliche Pruefung ist das unerheblich.

ZWEI ARTEN VON BEFUND - UND WARUM SIE GETRENNT WERDEN
------------------------------------------------------------------------------
Eine Kurve kann aus zwei ganz verschiedenen Gruenden nicht mehr zum heutigen
Lauf passen:

* **VERALTET** - die abgelegte Kurve ist ein exakter Anfang der heutigen:
  jede gemeinsame Zeile stimmt, die heutige ist nur laenger. Dann sind
  schlicht neue Kursdaten dazugekommen. Die abgelegte Kurve ist unvollstaendig,
  aber nicht falsch; Aussagen, die auf ihr beruhen, bleiben fuer ihren
  Zeitraum gueltig.
* **ABWEICHEND** - schon im gemeinsamen Teil laufen die Kurven auseinander,
  oder die abgelegte ist laenger als der heutige Lauf. Dann beschreibt sie
  einen anderen Bot. Das ist der Schaden, um den es hier geht: jede Zahl, die
  aus ihr abgeleitet wurde, ist neu zu pruefen.

Ohne diese Trennung waere die Pruefung wertlos. Die Kursdaten wachsen
taeglich; eine Pruefung, die deshalb jeden Tag anschlaegt, meldet nicht mehr,
sondern verdeckt. Deshalb meldet sie beides mit eigener Marke, und
`--nur-abweichung` laesst einen Cronjob auf den ernsten Fall verengen.

Voreinstellung ist trotzdem "beides meldet" - wer von Hand prueft, will auch
wissen, dass eine Kurve 200 Zeilen hinterherhinkt.

WAS DIESES PROGRAMM NIE TUT
------------------------------------------------------------------------------
* **Es blockiert nichts.** Es faehrt keinen Bot herunter, aendert keine
  `live_params.py`, fasst keine Bot-Datenbank an, sendet keine Order. Es
  meldet. Der Rueckgabewert 1 ist fuer den Cronjob da, nicht fuer den
  Live-Betrieb - kein Bot ruft dieses Programm auf.
* **Beim Pruefen schreibt es nicht nach `results/`.** Das ist strukturell
  abgesichert, nicht versprochen: `kurven_lauf.py` lenkt `RESULTS_DIR` in
  einen temporaeren Ordner um, und nur `--erzeugen` kopiert von dort in die
  Ablage.

Vorbild fuer Aufbau und Rueckgabewert: `shared/kursdaten.py` (PR #81).
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

import pandas as pd

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)
STRATEGIES_DIR = os.path.join(BASE_DIR, "strategies")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
KURVEN_LAUF = os.path.join(_SHARED_DIR, "kurven_lauf.py")

# Spalten, an denen sich die Gleichheit zweier Kurven entscheidet. `symbol`
# gehoert dazu: ein Trade mit gleichem PnL an gleicher Stelle, aber anderem
# Symbol, ist ein anderer Trade.
VERGLEICHSSPALTEN = ["time", "symbol", "pnl_pct", "allocation", "capital_after"]

# Gerundet wird auf sechs Stellen - `allocation` und `capital_after` stehen in
# der Datei bereits auf zwei gerundet, `pnl_pct` in voller Breite. Sechs
# Stellen sind genug, um jede echte Abweichung zu sehen, und robust gegen die
# letzte Bit-Stelle einer Gleitkommazahl.
RUNDUNG = 6

# Der Krypto-Elliott-Wave-Bot legt seine Kurve historisch in der Wurzel von
# results/ ab statt im Unterordner (Relikt aus der Zeit vor
# strategy_paths.py). Dieselbe Aufloesung wie in
# shared/portfolio_overview.py: der Standardpfad gewinnt, WENN es ihn gibt -
# sonst der historische. Damit prueft dieses Programm genau die Datei, die
# Montags-Mail und Dashboard auch lesen.
HISTORISCHE_PFADE = {
    "elliott_wave": os.path.join(RESULTS_DIR, "equity_curve.csv"),
}

AKTUELL = "AKTUELL"
VERALTET = "VERALTET"
ABWEICHEND = "ABWEICHEND"
FEHLT = "FEHLT"
FEHLER = "FEHLER"

# Welcher Zustand ist ein Befund? FEHLT ebenfalls: eine Kurve, die es nicht
# gibt, faellt in portfolio_overview.load_all_curves() lautlos aus der Summe
# (Protokoll 4.3b, Befund 2).
BEFUND_ZUSTAENDE = {VERALTET, ABWEICHEND, FEHLT, FEHLER}
ERNSTE_ZUSTAENDE = {ABWEICHEND, FEHLT, FEHLER}


def finde_bots() -> list:
    """Alle Strategie-Ordner mit einer equity_simulation.py. Nicht hart
    codiert - ein zehnter Bot wird automatisch mitgeprueft, sobald er der
    Projektkonvention folgt."""
    if not os.path.isdir(STRATEGIES_DIR):
        return []
    return sorted(
        name for name in os.listdir(STRATEGIES_DIR)
        if os.path.exists(os.path.join(STRATEGIES_DIR, name, "equity_simulation.py"))
    )


def ablage_pfad(bot: str) -> str:
    """Der Pfad, unter dem die Kurve dieses Bots abgelegt ist."""
    standard = os.path.join(RESULTS_DIR, bot, "equity_curve.csv")
    if not os.path.exists(standard) and bot in HISTORISCHE_PFADE:
        return HISTORISCHE_PFADE[bot]
    return standard


def erzeuge_kurve(bot: str, zielordner: str) -> dict:
    """Startet einen eigenen Prozess je Bot (neun gleichnamige
    equity_simulation.py kollidieren in sys.modules) und gibt die Meta-Angaben
    des Laufs zurueck."""
    os.makedirs(zielordner, exist_ok=True)
    lauf = subprocess.run(
        [sys.executable, KURVEN_LAUF, bot, zielordner],
        capture_output=True, text=True, cwd=BASE_DIR)
    if lauf.returncode != 0:
        raise RuntimeError(
            f"{bot}: Lauf fehlgeschlagen (Rueckgabewert {lauf.returncode}).\n"
            f"{lauf.stderr.strip() or lauf.stdout.strip()}")

    meta = {}
    for zeile in reversed(lauf.stdout.splitlines()):
        if zeile.startswith("__KURVEN_META__ "):
            meta = json.loads(zeile[len("__KURVEN_META__ "):])
            break
    if not meta:
        raise RuntimeError(f"{bot}: Lauf hat keine Meldezeile ausgegeben.")
    meta["ausgabe"] = lauf.stdout
    return meta


def lies_kurve(pfad: str) -> pd.DataFrame:
    df = pd.read_csv(pfad)
    fehlend = [s for s in VERGLEICHSSPALTEN if s not in df.columns]
    if fehlend:
        raise ValueError(f"{pfad}: Spalten fehlen: {', '.join(fehlend)}")
    return df


def _vergleichsform(df: pd.DataFrame) -> pd.DataFrame:
    """Bringt eine Kurve in die Form, in der zwei Kurven vergleichbar sind:
    Zeitstempel normiert (eine Datei kann '2021-09-14 19:00:00' schreiben, die
    andere '2021-09-14T19:00:00'), Zahlen gerundet."""
    form = df[VERGLEICHSSPALTEN].copy()
    form["time"] = pd.to_datetime(form["time"]).astype(str)
    form["symbol"] = form["symbol"].astype(str)
    for spalte in ("pnl_pct", "allocation", "capital_after"):
        form[spalte] = pd.to_numeric(form[spalte], errors="coerce").round(RUNDUNG)
    return form.reset_index(drop=True)


def kennzahlen(df: pd.DataFrame, startkapital: float) -> dict:
    """Dieselben Kennzahlen, die die Bots selbst ausgeben - der Max Drawdown
    nach der Formel aus ihrem `calculate_max_drawdown()`: die Kapitalreihe
    beginnt beim Startkapital, damit ein Verlust im ersten Trade nicht
    wegfaellt."""
    if df.empty:
        return {"zeilen": 0, "von": None, "bis": None, "endkapital": None,
                "rendite_pct": None, "max_drawdown_pct": None}
    zeiten = pd.to_datetime(df["time"])
    kapital = pd.concat([pd.Series([startkapital]),
                          pd.to_numeric(df["capital_after"])], ignore_index=True)
    laufendes_max = kapital.cummax()
    max_dd = ((kapital - laufendes_max) / laufendes_max * 100).min()
    end = float(kapital.iloc[-1])
    return {
        "zeilen": int(len(df)),
        "von": str(zeiten.min()),
        "bis": str(zeiten.max()),
        "endkapital": round(end, 2),
        "rendite_pct": round((end / startkapital - 1) * 100, 2),
        "max_drawdown_pct": round(float(max_dd), 2),
    }


def vergleiche(abgelegt: pd.DataFrame, frisch: pd.DataFrame) -> dict:
    """Der Kern: passt die abgelegte Kurve noch zum heutigen Lauf?

    Der gemeinsame Anfang entscheidet. Stimmt er ueberall und ist die heutige
    Kurve laenger, sind nur Kursdaten dazugekommen (VERALTET). Laeuft schon
    der gemeinsame Anfang auseinander - oder ist die abgelegte Kurve laenger,
    enthaelt also Trades, die der Bot heute gar nicht mehr macht -, dann
    beschreibt sie einen anderen Bot (ABWEICHEND)."""
    a = _vergleichsform(abgelegt)
    b = _vergleichsform(frisch)
    gemeinsam = min(len(a), len(b))

    erste_abweichung = None
    abweichende_zeilen = 0
    if gemeinsam:
        ungleich = (a.iloc[:gemeinsam] != b.iloc[:gemeinsam]).any(axis=1)
        abweichende_zeilen = int(ungleich.sum())
        if abweichende_zeilen:
            i = int(ungleich.idxmax())
            spalten = [s for s in VERGLEICHSSPALTEN
                       if a.iloc[i][s] != b.iloc[i][s]]
            erste_abweichung = {
                "zeile": i,
                "spalten": spalten,
                "abgelegt": {s: a.iloc[i][s] for s in spalten},
                "heute": {s: b.iloc[i][s] for s in spalten},
            }

    if abweichende_zeilen:
        zustand = ABWEICHEND
        grund = (f"schon im gemeinsamen Teil laufen die Kurven auseinander "
                 f"({abweichende_zeilen} von {gemeinsam} Zeilen, erstmals in Zeile "
                 f"{erste_abweichung['zeile']})")
    elif len(a) > len(b):
        zustand = ABWEICHEND
        grund = (f"die abgelegte Kurve ist laenger als der heutige Lauf "
                 f"({len(a)} statt {len(b)} Zeilen) - sie enthaelt Trades, die "
                 f"der Bot heute nicht mehr macht")
    elif len(a) < len(b):
        zustand = VERALTET
        grund = (f"der gemeinsame Teil stimmt, es fehlen {len(b) - len(a)} "
                 f"spaetere Zeilen (neue Kursdaten)")
    else:
        zustand = AKTUELL
        grund = "Zeile fuer Zeile identisch"

    return {
        "zustand": zustand,
        "grund": grund,
        "zeilen_abgelegt": len(a),
        "zeilen_heute": len(b),
        "gemeinsamer_teil": gemeinsam,
        "abweichende_zeilen": abweichende_zeilen,
        "erste_abweichung": erste_abweichung,
    }


def pruefe_bot(bot: str, arbeitsordner: str) -> dict:
    """Ein Bot: erzeugen, vergleichen, Kennzahlen beider Fassungen."""
    befund = {"bot": bot, "ablage": os.path.relpath(ablage_pfad(bot), BASE_DIR)}
    try:
        meta = erzeuge_kurve(bot, os.path.join(arbeitsordner, bot))
    except RuntimeError as fehler:
        befund.update({"zustand": FEHLER, "grund": str(fehler).splitlines()[0],
                       "meldung": str(fehler)})
        return befund

    startkapital = meta.get("startkapital") or 10_000.0
    frisch = lies_kurve(meta["kurve"])
    befund["heute"] = kennzahlen(frisch, startkapital)
    befund["heute_datei"] = meta["kurve"]
    befund["lauf"] = {k: meta.get(k) for k in
                      ("startkapital", "allocation_pct", "max_concurrent_positions",
                       "trades_gefunden", "trades_ausgefuehrt", "trades_uebersprungen",
                       "endkapital", "max_drawdown_pct")}

    pfad = ablage_pfad(bot)
    if not os.path.exists(pfad):
        befund.update({
            "zustand": FEHLT,
            "grund": "keine abgelegte Kurve vorhanden - der Bot faellt aus jeder "
                     "Portfolio-Summe heraus, ohne dass es auffaellt",
            "abgelegt": None,
        })
        return befund

    abgelegt = lies_kurve(pfad)
    befund["abgelegt"] = kennzahlen(abgelegt, startkapital)
    befund.update(vergleiche(abgelegt, frisch))
    befund["byteweise_identisch"] = _byteweise_gleich(pfad, meta["kurve"])
    return befund


def _byteweise_gleich(a: str, b: str) -> bool:
    with open(a, "rb") as fa, open(b, "rb") as fb:
        return fa.read() == fb.read()


def uebernehmen(befund: dict) -> bool:
    """Kopiert die frisch erzeugte Kurve an ihren Ablageplatz. Byteweise
    Kopie, damit zwei Laeufe dieselbe Datei ergeben. Gibt zurueck, ob sich
    dabei etwas geaendert hat."""
    quelle = befund.get("heute_datei")
    if not quelle:
        return False
    ziel = ablage_pfad(befund["bot"])
    if os.path.exists(ziel) and _byteweise_gleich(ziel, quelle):
        return False
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    shutil.copyfile(quelle, ziel)
    return True


# --- Ausgabe ---------------------------------------------------------------

def _zahl(wert, einheit="", stellen=2):
    if wert is None:
        return "-"
    return f"{wert:,.{stellen}f}{einheit}"


def _zeitraum(kenn):
    if not kenn or not kenn.get("von"):
        return "-"
    return f"{str(kenn['von'])[:10]} bis {str(kenn['bis'])[:10]}"


def berichte(befunde: list):
    print("=" * 78)
    print("ERGEBNISKURVEN - abgelegte Kurve gegen die heutige Konfiguration")
    print("=" * 78)

    for befund in befunde:
        marke = {AKTUELL: "OK", VERALTET: "[!] VERALTET",
                 ABWEICHEND: "[!!] ABWEICHEND", FEHLT: "[!!] FEHLT",
                 FEHLER: "[!!] FEHLER"}[befund["zustand"]]
        print(f"\n{befund['bot']}  -  {marke}")
        print(f"  Datei:  {befund['ablage']}")
        print(f"  Grund:  {befund.get('grund', '')}")

        if befund["zustand"] == FEHLER:
            for zeile in befund.get("meldung", "").splitlines()[:8]:
                print(f"          {zeile}")
            continue

        abgelegt, heute = befund.get("abgelegt"), befund.get("heute")
        kopf = f"  {'':10} {'Zeilen':>8} {'Endkapital':>14} {'Rendite':>10} {'MaxDD':>9}  Zeitraum"
        print(kopf)
        if abgelegt:
            print(f"  {'abgelegt':10} {abgelegt['zeilen']:>8} "
                  f"{_zahl(abgelegt['endkapital']):>14} "
                  f"{_zahl(abgelegt['rendite_pct'], ' %'):>10} "
                  f"{_zahl(abgelegt['max_drawdown_pct'], ' %'):>9}  {_zeitraum(abgelegt)}")
        print(f"  {'heute':10} {heute['zeilen']:>8} "
              f"{_zahl(heute['endkapital']):>14} "
              f"{_zahl(heute['rendite_pct'], ' %'):>10} "
              f"{_zahl(heute['max_drawdown_pct'], ' %'):>9}  {_zeitraum(heute)}")

        erste = befund.get("erste_abweichung")
        if erste:
            print(f"  Erste abweichende Zeile ({erste['zeile']}), Spalten "
                  f"{', '.join(erste['spalten'])}:")
            print(f"          abgelegt: {erste['abgelegt']}")
            print(f"          heute:    {erste['heute']}")

    print("\n" + "=" * 78)
    zaehler = {}
    for befund in befunde:
        zaehler[befund["zustand"]] = zaehler.get(befund["zustand"], 0) + 1
    print("Zusammenfassung: " + ", ".join(
        f"{anzahl}x {zustand}" for zustand, anzahl in sorted(zaehler.items())))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Prueft die abgelegten Ergebniskurven gegen die heutige "
                    "Konfiguration und erzeugt sie auf Wunsch neu.")
    parser.add_argument("--erzeugen", action="store_true",
                        help="die abgelegten Kurven durch die frisch erzeugten ersetzen")
    parser.add_argument("--bot", action="append", default=None,
                        help="nur diesen Bot (mehrfach angebbar)")
    parser.add_argument("--nur-abweichung", action="store_true",
                        help="Rueckgabewert 1 nur bei echter Abweichung, nicht bei "
                             "einer blossen Verlaengerung durch neue Kursdaten")
    parser.add_argument("--json", metavar="PFAD", default=None,
                        help="Befunde zusaetzlich als JSON ablegen")
    args = parser.parse_args(argv)

    bots = args.bot or finde_bots()
    unbekannt = [b for b in bots if not os.path.exists(
        os.path.join(STRATEGIES_DIR, b, "equity_simulation.py"))]
    if unbekannt:
        print(f"Unbekannter Bot: {', '.join(unbekannt)}", file=sys.stderr)
        return 2
    if not bots:
        print("Keine Bots mit equity_simulation.py gefunden.", file=sys.stderr)
        return 2

    arbeitsordner = tempfile.mkdtemp(prefix="ergebniskurven_")
    try:
        befunde = [pruefe_bot(bot, arbeitsordner) for bot in bots]
        berichte(befunde)

        if args.erzeugen:
            print("\n" + "=" * 78)
            print("UEBERNAHME (--erzeugen)")
            print("=" * 78)
            for befund in befunde:
                if befund["zustand"] == FEHLER:
                    print(f"  {befund['bot']}: uebersprungen (Lauf fehlgeschlagen)")
                    continue
                geaendert = uebernehmen(befund)
                print(f"  {befund['bot']}: "
                      f"{'geschrieben' if geaendert else 'unveraendert'} -> {befund['ablage']}")

        if args.json:
            schlank = [{k: v for k, v in b.items() if k != "heute_datei"} for b in befunde]
            with open(args.json, "w") as f:
                json.dump(schlank, f, indent=2, ensure_ascii=False, default=str)
            print(f"\nBefunde als JSON: {args.json}")
    finally:
        shutil.rmtree(arbeitsordner, ignore_errors=True)

    ausloeser = ERNSTE_ZUSTAENDE if args.nur_abweichung else BEFUND_ZUSTAENDE
    treffer = [b for b in befunde if b["zustand"] in ausloeser]
    if treffer:
        print(f"\nBEFUND: {len(treffer)} von {len(befunde)} Kurven passen nicht "
              f"zur heutigen Konfiguration "
              f"({', '.join(b['bot'] for b in treffer)}).")
        print("Neu erzeugen mit:  python3 shared/ergebniskurven.py --erzeugen")
        return 1

    print("\nAlle geprueften Kurven passen zur heutigen Konfiguration.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
