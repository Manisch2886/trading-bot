"""
Verhaelt sich forward_test.py nach der Umstellung wirklich identisch?
================================================================================
Das ist der wichtigste Nachweis dieser Aenderung: zum ersten Mal wird das
tatsaechlich per Cron laufende Live-Skript angefasst. Eine Behauptung
("es werden ja nur Zahlen verschoben") genuegt hier nicht.

METHODE - beide Fassungen NEBENEINANDER, nicht nacheinander:

  Die ALTE Fassung wird aus git geholt (`git show <ref>:<pfad>`), die NEUE
  aus dem Arbeitsverzeichnis. Beide werden als eigenstaendige Module in
  getrennte Namensraeume geladen und mit IDENTISCHEN Eingaben aufgerufen:
  dieselbe Kursdatenreihe, dieselbe frisch angelegte Datenbank, derselbe
  Bestand offener Positionen.

  Verglichen wird danach BEIDES:
    - der komplette Datenbankinhalt (alle Spalten aller Trades)
    - die vollstaendige Bildschirmausgabe, Zeichen fuer Zeichen

  Ein Nacheinander-Lauf mit zwischenzeitlichem git-Checkout wuerde
  dasselbe behaupten, aber nicht ausschliessen, dass zwischen den Laeufen
  etwas anderes verrutscht ist. Hier laufen beide im selben Prozess, mit
  denselben Objekten als Eingabe.

WAS DER TEST WIRKLICH ZEIGEN KANN - und was nicht:

  Er prueft die Funktionen, die die Handelsentscheidungen treffen
  (check_open_trades und find_new_signals) auf ECHTEN Kursdaten aus data/.
  Er prueft NICHT den Netzwerkabruf und nicht die Cron-Einbettung; beides
  wird von der Aenderung auch nicht beruehrt. Damit das nicht stillschweigend
  bleibt: die Attrappen werfen, sobald jemand doch einen Abruf versucht.

ZUSAETZLICHE, UNABHAENGIGE PRUEFUNG (mehrere Wege, nicht einer):
  1. NAMENSRAUM: alle Modulkonstanten beider Fassungen vergleichen. Sie
     muessen exakt uebereinstimmen - dann kann kein Wert verrutscht sein.
  2. SYNTAXBAUM: der Unterschied zwischen alt und neu darf ausschliesslich
     aus Import- und Zuweisungsknoten der betroffenen Namen bestehen.
  3. VERHALTEN: siehe oben.

Nutzung:  python3 vergleich.py <bot> [--ref HEAD]
          z.B.  python3 vergleich.py rsi2_crypto
"""

import argparse
import ast
import difflib
import importlib.util
import io
import contextlib
import os
import sqlite3
import subprocess
import sys
import tempfile

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
STRATEGIES = os.path.join(_REPO_ROOT, "strategies")
SHARED = os.path.join(_REPO_ROOT, "shared")
STUBS = os.path.join(_DIR, "stubs")
DATA = os.path.join(_REPO_ROOT, "data")

# Die beiden Bots sind unterschiedlich gebaut - dieselbe Pruefidee, aber
# andere Funktionsnamen, Zeitrahmen und Signaturen. Statt das im Code zu
# verzweigen, steht der Unterschied hier als Profil.
PROFILE = {
    "rsi2_crypto": {
        "suffix": "1d",
        # compute_indicators() liegt im forward_test-Modul selbst
        "indikatoren": lambda m, df: m.compute_indicators(df),
        # find_new_signals(conn, daten)
        "signale": lambda m, conn, daten: m.find_new_signals(conn, daten),
        # In welchem Pfad wirkt der umgestellte Wert?
        "exit_spalte": "sma_exit",
        "exit_ueber": "close",       # Exit, wenn close > sma_exit
        "erwarteter_exit": "time_exit",
        # rsi2_crypto faengt einen fehlenden Stop ab (has_stop), live gilt
        # dort STOP_LOSS_PCT = None - "kein Stop" ist die validierte Wahl.
        "stop_faktor": None,
    },
    "t3_supertrend": {
        "suffix": "4h",
        # compute_indicators() kommt aus indicators.py und braucht genau die
        # fuenf umgestellten Werte - damit trifft der Vergleich den Pfad, um
        # den es geht, unmittelbar.
        "indikatoren": lambda m, df: m.compute_indicators(
            df, m.T3_FAST_LENGTH, m.T3_SLOW_LENGTH, m.T3_FACTOR,
            m.DI_LENGTH, m.ADX_LENGTH, m.ATR_LENGTH, m.ATR_MULT),
        # find_new_signals(conn, daten, btc_regime_bullish) - der Regimewert
        # wird fest auf True gesetzt, damit beide Fassungen denselben Zweig
        # nehmen und der Vergleich nicht am Zufall haengt.
        "signale": lambda m, conn, daten: m.find_new_signals(conn, daten, True),
        "exit_spalte": None,
        "erwarteter_exit": None,
        # t3_supertrend rechnet in check_open_trades ungeschuetzt
        # row["low"] <= trade["stop_price"] - ein fehlender Stop wirft dort
        # sofort. Live setzt forward_test.py ihn aus STOP_LOSS_PCT (4%);
        # der Vergleich bildet das mit demselben Abstand nach.
        "stop_faktor": 0.96,
    },
}

_bestanden = 0
_fehler = []


def check(name, ok, detail=""):
    global _bestanden
    if ok:
        _bestanden += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        _fehler.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# Beide Fassungen laden
# ---------------------------------------------------------------------------

def alte_fassung(bot: str, ref: str) -> str:
    pfad = f"strategies/{bot}/forward_test.py"
    fertig = subprocess.run(["git", "-C", _REPO_ROOT, "show", f"{ref}:{pfad}"],
                             capture_output=True, text=True)
    if fertig.returncode != 0:
        raise SystemExit(f"Kann {ref}:{pfad} nicht lesen:\n{fertig.stderr}")
    return fertig.stdout


def lade_modul(quelltext: str, bot: str, modulname: str, temp_dir: str):
    """Laedt einen forward_test-Quelltext als eigenstaendiges Modul.

    Die Datei wird IM Bot-Ordner abgelegt, damit die relativen Pfad- und
    Importannahmen des Skripts (get_strategy_paths(__file__), Nachbarmodule)
    genauso greifen wie im Echtbetrieb. Nur DB_FILE wird umgeleitet - das
    Skript soll die echte Live-Datenbank nicht anfassen.
    """
    bot_dir = os.path.join(STRATEGIES, bot)
    hilfsdatei = os.path.join(bot_dir, f"_vergleich_{modulname}.py")
    with open(hilfsdatei, "w", encoding="utf-8") as f:
        f.write(quelltext)

    for pfad in (bot_dir, SHARED, STUBS):
        if pfad not in sys.path:
            sys.path.insert(0, pfad)

    import strategy_paths
    echt = strategy_paths.get_strategy_paths

    def umgeleitet(caller_file):
        p = dict(echt(caller_file))
        p["DB_FILE"] = os.path.join(temp_dir, f"{modulname}.db")
        p["RESULTS_DIR"] = os.path.join(temp_dir, "results")
        p["LOGS_DIR"] = os.path.join(temp_dir, "logs")
        os.makedirs(p["RESULTS_DIR"], exist_ok=True)
        os.makedirs(p["LOGS_DIR"], exist_ok=True)
        return p

    strategy_paths.get_strategy_paths = umgeleitet
    try:
        spec = importlib.util.spec_from_file_location(modulname, hilfsdatei)
        modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modul)
        return modul
    finally:
        strategy_paths.get_strategy_paths = echt
        os.remove(hilfsdatei)


# ---------------------------------------------------------------------------
# Eingabedaten
# ---------------------------------------------------------------------------

def echte_kursdaten(modul, anzahl_symbole: int, profil: dict) -> dict:
    """Echte Kerzen aus data/, durch die Indikator-Kette des Moduls.

    Bewusst echte Daten statt konstruierter: eine Kunstreihe koennte
    zufaellig genau die Verzweigung meiden, um die es geht.
    """
    daten = {}
    for symbol in modul.SYMBOLS[:anzahl_symbole]:
        pfad = os.path.join(DATA, f"{symbol}_{profil['suffix']}.csv")
        if not os.path.exists(pfad):
            continue
        df = pd.read_csv(pfad, parse_dates=["open_time"])
        daten[symbol] = profil["indikatoren"](modul, df)
    return daten


def zeit_exit_einstiege(df: pd.DataFrame, max_hold_days: int) -> list:
    """Einstiegspunkte, an denen der ZEIT-Exit greift - nicht der SMA-Exit.

    Der Grund fuer diese Suche ist ein Fehler in der ersten Fassung dieses
    Werkzeugs: dort wurde einfach ein Einstieg 200 Kerzen vor dem Ende
    gesetzt und anschliessend geprueft, dass Positionen geschlossen wurden.
    Sie wurden geschlossen - aber ueber den SMA-Exit. Der Zeit-Exit, also
    der einzige Pfad, in dem MAX_HOLD_DAYS ueberhaupt vorkommt, wurde nie
    durchlaufen. Die Empfindlichkeitsprobe (--stoere MAX_HOLD_DAYS=9)
    entlarvte das: der Verhaltensvergleich meldete "identisch", obwohl der
    Wert veraendert war.

    Auf echten Tagesdaten fuehren nur rund 1 % der Einstiegspunkte zum
    Zeit-Exit (bei BTCUSDT 15 von ~1600) - blindes Setzen trifft ihn also
    so gut wie nie. Deshalb wird gezielt gesucht.
    """
    treffer = []
    for start in range(len(df) - max_hold_days - 2):
        future = df.iloc[start + 1:].reset_index(drop=True)
        for offset in range(len(future)):
            row = future.iloc[offset]
            if not pd.isna(row["sma_exit"]) and row["close"] > row["sma_exit"]:
                break
            if offset + 1 >= max_hold_days:
                treffer.append(start)
                break
    return treffer


def frische_db(modul, indicator_data: dict, temp_dir: str, name: str,
                einstiege: dict, stop_faktor=None):
    """Neue Datenbank mit identischem Ausgangsbestand fuer beide Fassungen.

    `einstiege` wird EINMAL bestimmt und beiden Fassungen unveraendert
    uebergeben - beide bekommen also garantiert denselben Ausgangsbestand.
    """
    pfad = os.path.join(temp_dir, f"{name}.db")
    if os.path.exists(pfad):
        os.remove(pfad)
    modul.DB_FILE = pfad
    conn = modul.init_db()

    # Das Schema unterscheidet sich je Bot (rsi2_crypto fuehrt zusaetzlich
    # rsi_at_entry, t3_supertrend nicht). Statt Spalten anzunehmen, wird das
    # tatsaechliche Schema gelesen - eine Annahme waere hier ein
    # Testaufbau-Fehler, der wie ein Befund aussaehe.
    vorhanden = {z[1] for z in conn.execute("PRAGMA table_info(trades)")}
    spalten = ["symbol", "signal_time", "entry_time", "entry_price",
               "stop_price", "status"]
    spalten = [s for s in spalten if s in vorhanden]

    for symbol, indizes in einstiege.items():
        df = indicator_data[symbol]
        for i in indizes:
            zeile = df.iloc[i]
            werte = {"symbol": symbol, "signal_time": str(zeile["open_time"]),
                      "entry_time": str(zeile["open_time"]),
                      "entry_price": float(zeile["close"]),
                      "stop_price": (float(zeile["close"]) * stop_faktor
                                      if stop_faktor else None),
                      "status": "open"}
            conn.execute(
                f"INSERT INTO trades ({', '.join(spalten)}) "
                f"VALUES ({', '.join('?' * len(spalten))})",
                [werte[s] for s in spalten])
    conn.commit()
    return conn


def db_inhalt(conn) -> str:
    df = pd.read_sql("SELECT * FROM trades ORDER BY id", conn)
    return df.to_csv(index=False)


# ---------------------------------------------------------------------------
# Die drei Pruefungen
# ---------------------------------------------------------------------------

def teste_namensraum(alt, neu, namen):
    print("\n1) Namensraum: kommen dieselben Werte an?")
    for name in namen:
        a = getattr(alt, name, "<fehlt>")
        b = getattr(neu, name, "<fehlt>")
        check(f"{name}: alt {a!r} == neu {b!r}", a == b and a != "<fehlt>")

    # Und ALLE uebrigen Modulkonstanten gleich mit - nicht nur die erwarteten.
    def konstanten(m):
        # DB_FILE wird von diesem Werkzeug selbst je Fassung umgeleitet,
        # damit die echte Live-Datenbank unberuehrt bleibt - der Unterschied
        # ist gewollt und darf hier nicht als Befund erscheinen.
        return {k: v for k, v in vars(m).items()
                 if k.isupper() and k != "DB_FILE"
                 and isinstance(v, (int, float, str, bool, type(None)))}
    ka, kb = konstanten(alt), konstanten(neu)
    unterschiede = {k for k in set(ka) | set(kb) if ka.get(k) != kb.get(k)}
    check("Auch alle uebrigen Modulkonstanten sind identisch",
          not unterschiede,
          f"{len(ka)} Konstanten geprueft" if not unterschiede
          else str({k: (ka.get(k), kb.get(k)) for k in unterschiede}))


def teste_syntaxbaum(alt_quelle: str, neu_quelle: str, namen):
    """Der Unterschied darf nur die Herkunft der Namen betreffen."""
    print("\n2) Syntaxbaum: ist wirklich nur die Herkunft der Namen anders?")

    def ohne_namen(quelle):
        """Alle Anweisungen der Modulebene, ohne die Zuweisungen und
        Importe der betroffenen Namen - der Rest muss identisch sein."""
        baum = ast.parse(quelle)
        rest = []
        for knoten in baum.body:
            if isinstance(knoten, ast.Assign) and all(
                    isinstance(z, ast.Name) and z.id in namen for z in knoten.targets):
                continue
            if isinstance(knoten, ast.ImportFrom) and knoten.module == "live_params":
                continue
            rest.append(ast.dump(knoten))
        return rest

    a, b = ohne_namen(alt_quelle), ohne_namen(neu_quelle)
    gleich = a == b
    detail = ""
    if not gleich:
        diff = list(difflib.unified_diff(a, b, "alt", "neu", lineterm=""))[:12]
        detail = " | ".join(z[:90] for z in diff)
    check("Ausser den betroffenen Zuweisungen/Importen ist der Modulrumpf "
          "unveraendert", gleich, detail)

    # Gegenkontrolle: die Aenderung darf nicht LEER sein, sonst prueft der
    # Test nichts.
    check("Es gibt ueberhaupt einen Unterschied zwischen alt und neu "
          "(sonst waere der Vergleich sinnlos)",
          alt_quelle != neu_quelle)


def teste_verhalten(alt, neu, temp_dir: str, anzahl_symbole: int, profil: dict):
    print("\n3) Verhalten: identische Eingaben, identische Ausgaben?")

    daten_alt = echte_kursdaten(alt, anzahl_symbole, profil)
    daten_neu = echte_kursdaten(neu, anzahl_symbole, profil)
    check(f"Beide Fassungen sehen dieselben {len(daten_alt)} Symbole",
          sorted(daten_alt) == sorted(daten_neu), str(sorted(daten_alt)))
    if not daten_alt:
        check("Es gibt ueberhaupt Kursdaten zum Rechnen", False,
              "keine CSV-Dateien gefunden")
        return

    # Die Indikatoren selbst muessen schon identisch sein.
    for symbol in sorted(daten_alt):
        gleich = daten_alt[symbol].to_csv(index=False) == daten_neu[symbol].to_csv(index=False)
        if not gleich:
            check(f"Indikatoren fuer {symbol} identisch", False)
            return
    check(f"Indikatoren aller {len(daten_alt)} Symbole identisch berechnet", True)

    # Einstiegspunkte EINMAL bestimmen, beiden Fassungen identisch geben.
    # Je Symbol hoechstens eine Position - die Datenbank verbietet mehrere
    # offene Trades im selben Symbol nicht, aber check_open_trades laeuft
    # ohnehin ueber alle.
    einstiege = {}
    if profil["erwarteter_exit"] == "time_exit":
        # rsi2_crypto: der umgestellte Wert wirkt NUR im Zeit-Exit-Pfad,
        # der auf echten Daten selten greift - deshalb gezielt suchen.
        for symbol, df in daten_alt.items():
            treffer = zeit_exit_einstiege(df, alt.MAX_HOLD_DAYS)
            if treffer:
                einstiege[symbol] = treffer[:2]
        check("Es wurden Einstiege gefunden, bei denen der ZEIT-Exit greift",
              bool(einstiege),
              f"{sum(len(v) for v in einstiege.values())} Positionen in "
              f"{len(einstiege)} Symbolen")
    else:
        # t3_supertrend: die umgestellten Werte gehen in die
        # INDIKATOR-Berechnung ein. Ihre Wirkung ist damit schon oben
        # geprueft (identische Indikatoren ueber alle Symbole und Spalten) -
        # das ist die schaerfere Aussage als ein einzelner Exit-Pfad. Fuer
        # den DB-Vergleich genuegen hier breit gestreute Einstiege.
        for symbol, df in daten_alt.items():
            if len(df) > 400:
                einstiege[symbol] = [len(df) - 300, len(df) - 150]
        check("Es wurden Einstiege fuer den Datenbankvergleich gesetzt",
              bool(einstiege),
              f"{sum(len(v) for v in einstiege.values())} Positionen in "
              f"{len(einstiege)} Symbolen")

    ergebnisse = {}
    for name, modul, daten in (("alt", alt, daten_alt), ("neu", neu, daten_neu)):
        conn = frische_db(modul, daten, temp_dir, name, einstiege,
                           profil["stop_faktor"])
        puffer = io.StringIO()
        with contextlib.redirect_stdout(puffer):
            modul.check_open_trades(conn, daten)
            profil["signale"](modul, conn, daten)
        ergebnisse[name] = {"db": db_inhalt(conn), "ausgabe": puffer.getvalue()}
        conn.close()

    gleich_db = ergebnisse["alt"]["db"] == ergebnisse["neu"]["db"]
    check("Datenbankinhalt nach check_open_trades + find_new_signals identisch",
          gleich_db)
    if not gleich_db:
        for zeile in list(difflib.unified_diff(
                ergebnisse["alt"]["db"].splitlines(),
                ergebnisse["neu"]["db"].splitlines(), "alt", "neu", lineterm=""))[:20]:
            print("        " + zeile)

    gleich_text = ergebnisse["alt"]["ausgabe"] == ergebnisse["neu"]["ausgabe"]
    check("Bildschirmausgabe zeichengenau identisch", gleich_text)
    if not gleich_text:
        for zeile in list(difflib.unified_diff(
                ergebnisse["alt"]["ausgabe"].splitlines(),
                ergebnisse["neu"]["ausgabe"].splitlines(), "alt", "neu", lineterm=""))[:20]:
            print("        " + zeile)

    # Gegenkontrolle: der Vergleich muss ueberhaupt etwas gesehen haben -
    # und zwar auf dem Pfad, um den es geht. "Geschlossen" allein genuegt
    # NICHT: eine Position kann ueber Stop-Loss oder SMA-Exit schliessen,
    # ohne dass MAX_HOLD_DAYS je gelesen wird (genau daran ist die erste
    # Fassung dieses Werkzeugs gescheitert).
    zeilen = len(ergebnisse["alt"]["db"].strip().splitlines()) - 1
    check("Der Vergleich hat tatsaechlich Trades verarbeitet",
          zeilen > 0, f"{zeilen} Trades in der Datenbank")
    if profil["erwarteter_exit"]:
        treffer = ergebnisse["alt"]["db"].count(profil["erwarteter_exit"])
        check(f"Darunter {profil['erwarteter_exit']}-Faelle - der Pfad, in dem "
              f"der umgestellte Wert ueberhaupt vorkommt, wurde also wirklich "
              f"durchlaufen", treffer > 0, f"{treffer} Faelle")
    else:
        geschlossen = ergebnisse["alt"]["db"].count("closed")
        check("Darunter geschlossene Positionen - check_open_trades hat also "
              "wirklich gearbeitet", geschlossen > 0, f"{geschlossen} geschlossen")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("bot")
    p.add_argument("--ref", default="HEAD",
                    help="git-Referenz der ALTEN Fassung (Standard: HEAD)")
    p.add_argument("--namen", default="",
                    help="Komma-Liste der umgestellten Konstanten")
    p.add_argument("--symbole", type=int, default=8)
    p.add_argument("--stoere", default="",
                    help="EMPFINDLICHKEITSPROBE: 'NAME=WERT' veraendert den "
                         "Wert in der NEUEN Fassung absichtlich. Der Vergleich "
                         "MUSS dann Unterschiede melden - tut er es nicht, "
                         "beweist ein 'identisch' im Normallauf gar nichts.")
    args = p.parse_args()

    namen = [n.strip() for n in args.namen.split(",") if n.strip()]
    print(f"Vergleich forward_test.py: {args.ref} (alt) gegen "
          f"Arbeitsverzeichnis (neu) - Bot {args.bot}")
    print(f"Umgestellte Namen: {', '.join(namen) or '(keine angegeben)'}")

    alt_quelle = alte_fassung(args.bot, args.ref)
    with open(os.path.join(STRATEGIES, args.bot, "forward_test.py"),
              encoding="utf-8") as f:
        neu_quelle = f.read()

    if args.stoere:
        name, _, wert = args.stoere.partition("=")
        neu_quelle += f"\n{name.strip()} = {wert.strip()}  # EMPFINDLICHKEITSPROBE\n"
        print(f"EMPFINDLICHKEITSPROBE aktiv: {name.strip()} in der neuen "
              f"Fassung auf {wert.strip()} gesetzt.\n"
              f"Der Vergleich MUSS jetzt Unterschiede melden.")

    with tempfile.TemporaryDirectory(prefix="ftsync_") as temp_dir:
        alt = lade_modul(alt_quelle, args.bot, "ft_alt", temp_dir)
        neu = lade_modul(neu_quelle, args.bot, "ft_neu", temp_dir)

        teste_namensraum(alt, neu, namen)
        teste_syntaxbaum(alt_quelle, neu_quelle, set(namen))
        teste_verhalten(alt, neu, temp_dir, args.symbole, PROFILE[args.bot])

    print(f"\n{_bestanden}/{_bestanden + len(_fehler)} Pruefungen bestanden.")
    for name in _fehler:
        print(f"FEHLGESCHLAGEN: {name}")
    sys.exit(1 if _fehler else 0)


if __name__ == "__main__":
    main()
