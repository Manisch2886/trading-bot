#!/usr/bin/env python3
"""
Selbstpruefung der Warteauftraege AN EINER ARBEITSKOPIE
==============================================================================
Dieses Skript SCHREIBT in Bot-Datenbanken - deshalb laeuft es ausschliesslich
in einer Arbeitskopie des Projekts, nie im echten Projekt.

WOFUER: Es prueft auf Modulebene (ohne HTTP, ohne Browser) genau die Faelle,
die sich sonst nur zu bestimmten Tageszeiten pruefen liessen - geschlossene
Boerse, Feiertag, offene Boerse, "der Bot war schneller", Stornieren, Krypto.
Dafuer faelscht es die UHR, nicht den Kalender: die echte Bibliothek rechnet
weiter mit echten NYSE-Regeln, nur an einem Tag, den dieses Skript kennt. Eine
Kalender-Attrappe waere immer gruen, weil sie nichts misst (Methodik-Grundsatz
12 im Uebergabeprotokoll).

Es ergaenzt die Selbsttests (dashboard/test_dashboard.py), ersetzt sie nicht:
die laufen gegen ein synthetisches Testprojekt, dieses Skript gegen eine echte
Projektkopie mit echten Bot-Dateien.

SICHERHEITSSPERRE: es laeuft nur, wenn im Projektordner die Markierungsdatei
`.probe-kopie` liegt. Im echten Projekt gibt es sie nicht - dort bricht das
Skript mit Rueckgabewert 2 ab, bevor es irgendetwas anfasst. Die Sperre ist
bewusst eine DATEI und keine Pfadpruefung: ein Pfadvergleich waere nach dem
ersten Umbenennen des Projektordners wirkungslos, und zwar unbemerkt.

Aufruf (aus der Arbeitskopie heraus):
    cd ~/trading-bot-probe && python3 dashboard/pruefe_warteauftraege_kopie.py

Rueckgabewert 0 = alles bestanden, 1 = mindestens eine Pruefung fehlgeschlagen,
2 = Sicherheitssperre hat ausgeloest (es wurde nichts angefasst).
"""

import os
import sqlite3
import sys

# Das Skript liegt in dashboard/, der Projektordner ist eine Ebene darueber.
BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists(os.path.join(BASIS, ".probe-kopie")):
    print("ABBRUCH: keine Markierungsdatei .probe-kopie in " + BASIS)
    print("Dieses Skript darf ausschliesslich in einer Arbeitskopie laufen.")
    sys.exit(2)

sys.path.insert(0, os.path.join(BASIS, "notifications"))
sys.path.insert(0, os.path.join(BASIS, "dashboard"))

import boersenkalender          # noqa: E402
import manual_close             # noqa: E402
import warteauftraege           # noqa: E402
import schliessen               # noqa: E402
import warteauftraege_ausfuehren as skript   # noqa: E402

BOT = "volatility_breakout"
DB = os.path.join(BASIS, f"paper_trading_{BOT}.db")

ZEIT_OFFEN = "2026-09-10 17:00:00+00:00"        # Donnerstag, 13:00 New York
ZEIT_ZU = "2026-09-12 17:00:00+00:00"           # Samstag
ZEIT_FEIERTAG = "2026-11-26 17:00:00+00:00"     # Thanksgiving

ERGEBNISSE = []


def pruefe(name, bedingung, detail=""):
    ERGEBNISSE.append(bool(bedingung))
    marke = "PASS" if bedingung else "FAIL"
    print(f"  [{marke}] {name}" + (f"   {detail}" if detail else ""))


class uhr:
    """Setzt die Testuhr - der ECHTE Kalender rechnet weiter, nur an einem
    Tag, den dieses Skript kennt."""

    echt = staticmethod(boersenkalender.status)

    def __init__(self, zeitpunkt):
        self.zeitpunkt = zeitpunkt

    def __enter__(self):
        boersenkalender.status = lambda jetzt=None: uhr.echt(
            jetzt if jetzt is not None else self.zeitpunkt)
        boersenkalender.zwischenspeicher_leeren()

    def __exit__(self, *_):
        boersenkalender.status = uhr.echt
        boersenkalender.zwischenspeicher_leeren()


def zeilen():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    daten = [dict(z) for z in conn.execute("SELECT * FROM trades ORDER BY id")]
    conn.close()
    return daten


def lege_position_an(symbol, entry):
    conn = sqlite3.connect(DB)
    cursor = conn.execute(
        "INSERT INTO trades (symbol, signal_time, entry_time, entry_price, "
        "stop_price, status) VALUES (?,?,?,?,?, 'open')",
        (symbol, f"probe-{symbol}-{os.urandom(3).hex()}", "2026-03-01 00:00:00",
         entry, entry * 0.95))
    conn.commit()
    trade_id = cursor.lastrowid
    conn.close()
    return trade_id


def main():
    print(f"Arbeitskopie: {BASIS}")
    pruefe("Der Schreibkern zeigt auf die KOPIE, nicht auf das echte Projekt",
           manual_close.BASE_DIR == BASIS, manual_close.BASE_DIR)
    pruefe("Die Auftragsdatei liegt ebenfalls in der Kopie",
           warteauftraege.datei().startswith(BASIS), warteauftraege.datei())
    pruefe("Der Boersenkalender ist einsatzbereit",
           boersenkalender.bibliothek_verfuegbar(),
           str(boersenkalender.BIBLIOTHEK_FEHLER))
    if not all(ERGEBNISSE):
        print("\nABBRUCH: Grundvoraussetzungen nicht erfuellt.")
        return 1

    warteauftraege.alles_loeschen()
    trade_id = lege_position_an("AAPL", 150.0)
    vorher = zeilen()
    print(f"\nTestposition angelegt: Trade {trade_id} (AAPL, Einstieg 150.0)")

    # --- 1) Boerse GESCHLOSSEN ------------------------------------------
    print("\n1) Boerse geschlossen (Samstag)")
    with uhr(ZEIT_ZU):
        lage = schliessen.lage_fuer_bot(BOT)
        pruefe("Die Lage meldet 'vormerken', nicht 'handelbar'",
               lage["warteauftrag_noetig"] is True
               and lage["handelbar_jetzt"] is False, str(lage["grund"])[:80])

        vorgang = schliessen.vorbereiten(BOT, trade_id, {"AAPL": 160.0})
        pruefe("Der Vorgang ist ein Warteauftrags-Vorgang",
               vorgang["warteauftrag"] is True)
        pruefe("Vorbereiten hat nichts geschrieben", zeilen() == vorher)

        try:
            schliessen.ausfuehren(BOT, vorgang["vorgang"], "pruefskript")
            pruefe("Ohne Bestaetigung wird abgelehnt", False,
                   "es wurde KEIN Fehler geworfen")
        except schliessen.SchliessenNichtMoeglich as fehler:
            pruefe("Ohne Bestaetigung des Warnschritts: abgelehnt",
                   "nichts geaendert" in str(fehler), str(fehler)[:80])
        pruefe("Dabei wurde weder geschrieben noch vorgemerkt",
               zeilen() == vorher and warteauftraege.alle() == [])

        vorgang = schliessen.vorbereiten(BOT, trade_id, {"AAPL": 160.0})
        ergebnis = schliessen.ausfuehren(BOT, vorgang["vorgang"], "pruefskript",
                                          warteauftrag_bestaetigt=True)
        pruefe("Mit Bestaetigung entsteht ein Warteauftrag",
               ergebnis["warteauftrag"] is True)
        pruefe("Die Datenbank ist unveraendert", zeilen() == vorher)
        pruefe("Der Auftrag steht in der Datei auf der Platte",
               len(warteauftraege.alle()) == 1
               and warteauftraege.alle()[0]["trade_id"] == trade_id)
        pruefe("Er enthaelt bewusst KEINEN Ausstiegskurs",
               "kurs" not in warteauftraege.alle()[0])

        # Ausfuehrungsskript bei geschlossener Boerse: nichts.
        lauf = skript.lauf(kurse_holen=lambda s: {"AAPL": 160.0})
        pruefe("Das Ausfuehrungsskript tut bei geschlossener Boerse nichts",
               lauf["geschlossen"] == [] and len(warteauftraege.alle()) == 1,
               lauf["meldung"][:80])
        pruefe("Und die Datenbank bleibt unveraendert", zeilen() == vorher)

    # --- 2) Feiertag -----------------------------------------------------
    print("\n2) Feiertag (Thanksgiving, Donnerstag mitten in der Handelszeit)")
    with uhr(ZEIT_FEIERTAG):
        lauf = skript.lauf(kurse_holen=lambda s: {"AAPL": 160.0})
        pruefe("Auch am Feiertag wird nichts geschlossen",
               lauf["geschlossen"] == [] and len(warteauftraege.alle()) == 1,
               lauf["meldung"][:80])
        pruefe("Datenbank unveraendert", zeilen() == vorher)

    # --- 3) Boerse OFFEN: Trockenlauf und Ernstfall ---------------------
    print("\n3) Boerse offen")
    with uhr(ZEIT_OFFEN):
        trocken = skript.lauf(trockenlauf=True,
                               kurse_holen=lambda s: {"AAPL": 165.0})
        pruefe("Der Trockenlauf meldet, was er taete",
               len(trocken["geschlossen"]) == 1)
        pruefe("... schreibt aber nichts und laesst den Auftrag stehen",
               zeilen() == vorher and len(warteauftraege.alle()) == 1)

        lauf = skript.lauf(kurse_holen=lambda s: {"AAPL": 165.0})
        pruefe("Der Ernstfall schliesst die Position",
               len(lauf["geschlossen"]) == 1, lauf["meldung"][:80])
        nachher = [z for z in zeilen() if z["id"] == trade_id][0]
        pruefe("Vermerkt als manual_close, geschlossen",
               nachher["status"] == "closed"
               and nachher["result"] == "manual_close",
               f"{nachher['status']} / {nachher['result']}")
        pruefe("Zum Kurs des AUSFUEHRUNGSZEITPUNKTS (165.0)",
               nachher["exit_price"] == 165.0, str(nachher["exit_price"]))
        pruefe("PnL nach der Formel des Bots (150 -> 165 = +9.70)",
               nachher["pnl_pct"] == 9.7, str(nachher["pnl_pct"]))
        pruefe("Der Auftrag ist abgeraeumt", warteauftraege.alle() == [])

    # --- 4) Der Bot war schneller ---------------------------------------
    print("\n4) Der Bot schliesst die Position selbst, waehrend ein Auftrag wartet")
    zweite = lege_position_an("MSFT", 300.0)
    with uhr(ZEIT_ZU):
        vorgang = schliessen.vorbereiten(BOT, zweite, {"MSFT": 310.0})
        schliessen.ausfuehren(BOT, vorgang["vorgang"], "pruefskript",
                               warteauftrag_bestaetigt=True)
    conn = sqlite3.connect(DB)
    conn.execute("UPDATE trades SET status='closed', result='sma_exit', "
                  "exit_price=305.0, pnl_pct=1.37, "
                  "exit_time='2026-09-11 20:00:00' WHERE id=?", (zweite,))
    conn.commit()
    conn.close()
    vor_lauf = zeilen()
    with uhr(ZEIT_OFFEN):
        lauf = skript.lauf(kurse_holen=lambda s: {"MSFT": 250.0})
    pruefe("Der Auftrag wird UEBERSPRUNGEN, nicht ausgefuehrt",
           len(lauf["uebersprungen"]) == 1 and lauf["geschlossen"] == [],
           lauf["meldung"][:80])
    pruefe("Ausdruecklich KEIN Fehlschlag", lauf["fehlgeschlagen"] == [])
    pruefe("Die Zeile des Bots bleibt unberuehrt (sma_exit, 305.0)",
           zeilen() == vor_lauf)
    pruefe("Der Auftrag ist abgeraeumt", warteauftraege.alle() == [])

    # --- 5) Stornieren ---------------------------------------------------
    print("\n5) Stornieren verhindert die Ausfuehrung")
    dritte = lege_position_an("NVDA", 500.0)
    vor_storno = zeilen()
    with uhr(ZEIT_ZU):
        vorgang = schliessen.vorbereiten(BOT, dritte, {"NVDA": 520.0})
        ergebnis = schliessen.ausfuehren(BOT, vorgang["vorgang"], "pruefskript",
                                          warteauftrag_bestaetigt=True)
    auftrag_id = ergebnis["auftrag"]["id"]
    schliessen.warteauftrag_stornieren(auftrag_id, "pruefskript")
    pruefe("Der Auftrag ist weg", warteauftraege.alle() == [])
    with uhr(ZEIT_OFFEN):
        lauf = skript.lauf(kurse_holen=lambda s: {"NVDA": 400.0})
    pruefe("Bei offener Boerse passiert danach nichts mehr",
           lauf["geschlossen"] == [])
    pruefe("Die Position ist noch offen und unveraendert",
           zeilen() == vor_storno)

    # --- 6) Krypto ist nicht betroffen -----------------------------------
    print("\n6) Krypto")
    with uhr(ZEIT_ZU):
        lage = schliessen.lage_fuer_bot("t3_supertrend")
        pruefe("Ein Krypto-Bot ist auch am Samstag sofort handelbar",
               lage["handelbar_jetzt"] is True
               and lage["warteauftrag_noetig"] is False)
        try:
            warteauftraege.anlegen("t3_supertrend", 1, "BTCUSDT", "pruefskript",
                                    "pruefskript")
            pruefe("Ein Krypto-Warteauftrag wird abgelehnt", False,
                   "es wurde KEIN Fehler geworfen")
        except warteauftraege.WarteauftragNichtMoeglich as fehler:
            pruefe("Ein Krypto-Warteauftrag wird abgelehnt",
                   "Krypto-Bot" in str(fehler), str(fehler)[:70])

    bestanden = sum(1 for e in ERGEBNISSE if e)
    print(f"\n{bestanden}/{len(ERGEBNISSE)} Pruefungen bestanden.")
    return 0 if bestanden == len(ERGEBNISSE) else 1


if __name__ == "__main__":
    sys.exit(main())
