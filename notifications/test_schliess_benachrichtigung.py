"""
Selbsttests der Schliess-Benachrichtigung
==============================================================================
KEIN einziger echter Netzaufruf. Der Sendeweg ist ein Parameter; die Attrappe
zaehlt die Nachrichten, haelt ihren Text fest und laesst sich gezielt
kaputtmachen - nur so lassen sich die Faelle pruefen, auf die es hier ankommt
(fehlgeschlagener Versand, Abbruch zwischen Senden und Vermerken).

Die Test-Datenbank entsteht aus dem ECHTEN `CREATE TABLE` eines Bots. Ein Test
gegen ein selbst erfundenes Schema waere wertlos - dieselbe Begruendung wie in
notifications/test_manual_close.py, Abschnitt 1, und in broker/test_broker.py.

Aufruf:  python3 notifications/test_schliess_benachrichtigung.py
"""

import ast
import hashlib
import os
import shutil
import sqlite3
import sys
import tempfile

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)
for _p in (_DIR, os.path.join(BASE_DIR, "broker")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import monitor                              # noqa: E402
import schliess_benachrichtigung as sb       # noqa: E402

BESTANDEN = []
FEHLER = []


def check(name, bedingung, detail=""):
    BESTANDEN.append(bool(bedingung))
    print(f"  [{'OK ' if bedingung else 'FEHLER'}] {name}"
          + (f"   {detail}" if detail else ""))
    if not bedingung:
        FEHLER.append(name)


# ---------------------------------------------------------------------------
# Attrappe des Sendewegs
# ---------------------------------------------------------------------------
class Sender:
    """Zaehlt, haelt fest und laesst sich kaputtmachen.

    `scheitert_ab`: ab dem n-ten Aufruf (1-basiert) wird False geliefert.
    `scheitert_immer`: jeder Aufruf scheitert.
    """

    def __init__(self, scheitert_ab=None, scheitert_immer=False):
        self.texte = []
        self.scheitert_ab = scheitert_ab
        self.scheitert_immer = scheitert_immer

    def __call__(self, text):
        self.texte.append(text)
        if self.scheitert_immer:
            return False
        if self.scheitert_ab and len(self.texte) >= self.scheitert_ab:
            return False
        return True

    @property
    def anzahl(self):
        return len(self.texte)

    def enthaelt(self, teil):
        return any(teil in t for t in self.texte)


# ---------------------------------------------------------------------------
# Ein Wegwerf-Projekt mit dem ECHTEN Bot-Schema
# ---------------------------------------------------------------------------
def echtes_create_table(bot="t3_supertrend") -> str:
    pfad = os.path.join(BASE_DIR, "strategies", bot, "forward_test.py")
    baum = ast.parse(open(pfad, encoding="utf-8").read(), filename=pfad)
    for knoten in ast.walk(baum):
        if (isinstance(knoten, ast.Constant) and isinstance(knoten.value, str)
                and "CREATE TABLE" in knoten.value and "trades" in knoten.value):
            return knoten.value
    raise AssertionError(f"CREATE TABLE im echten {bot}/forward_test.py nicht gefunden")


# Das ECHTE Schema hat UNIQUE(symbol, signal_time) - zwei Testtrades
# desselben Symbols mit derselben Signalzeit gaebe es dort nicht. Die
# Signalzeit traegt deshalb die Trade-Nummer als Minutenversatz; bei 300
# Testtrades sind das fuenf Stunden, also eine plausible Spanne.
def _zeit(tid):
    stunde, minute = divmod(tid, 60)
    return f"2026-09-01 {stunde % 24:02d}:{minute:02d}:00"


def offener_trade(tid, symbol="BTCUSDT", entry=50000.0):
    return (tid, symbol, _zeit(tid), _zeit(tid), entry, entry * 0.95,
            None, None, None, None, "open")


def geschlossener_trade(tid, symbol="BTCUSDT", entry=50000.0, exit_=51000.0,
                         grund="trend_flip", pnl=1.7,
                         entry_zeit=None, exit_zeit=None):
    return (tid, symbol, entry_zeit or _zeit(tid), entry_zeit or _zeit(tid),
            entry, entry * 0.95, exit_zeit or "2026-09-03 12:00:00", exit_,
            grund, pnl, "closed")


class Projekt:
    """Biegt das Modul auf ein Wegwerf-Verzeichnis um und stellt alles wieder
    zurueck - kein Test darf die echte Umgebung hinterlassen."""

    def __init__(self, trades, bot="t3_supertrend"):
        self.trades = trades
        self.bot = bot

    def __enter__(self):
        self.wurzel = tempfile.mkdtemp(prefix="schliessmeldung_")
        self.db = os.path.join(self.wurzel, f"paper_trading_{self.bot}.db")
        conn = sqlite3.connect(self.db)
        conn.execute(echtes_create_table(self.bot))
        conn.executemany(
            "INSERT INTO trades (id, symbol, signal_time, entry_time, "
            "entry_price, stop_price, exit_time, exit_price, result, pnl_pct, "
            "status) VALUES (?,?,?,?,?,?,?,?,?,?,?)", self.trades)
        conn.commit()
        conn.close()

        self.alt_base = sb.BASE_DIR
        sb.BASE_DIR = self.wurzel
        self.conn = sb.oeffne_db(os.path.join(self.wurzel, "meldungen.db"))
        return self

    def __exit__(self, *a):
        self.conn.close()
        sb.BASE_DIR = self.alt_base
        shutil.rmtree(self.wurzel, ignore_errors=True)
        return False

    def lauf(self, sender, **kw):
        return sb.lauf(senden=sender, conn=self.conn, base_dir=self.wurzel,
                        pause=0, **kw)

    def vermerke(self):
        return [dict(z) for z in self.conn.execute(
            "SELECT bot, trade_id, zustand FROM gemeldet ORDER BY trade_id")]

    def pruefsumme(self):
        return hashlib.sha256(open(self.db, "rb").read()).hexdigest()


def pruefsumme(pfad):
    return hashlib.sha256(open(pfad, "rb").read()).hexdigest()


# ---------------------------------------------------------------------------
# 1. Der Grundfall: erkennen, melden, vermerken
# ---------------------------------------------------------------------------
def test_grundfall():
    print("\n1. Erkennen, melden, vermerken")

    with Projekt([geschlossener_trade(1), offener_trade(2, "ETHUSDT", 2000.0)]) as p:
        # Erst den Erstlauf hinter uns bringen, sonst greift dessen Modus.
        p.lauf(Sender())
        # Jetzt schliesst der Bot den zweiten Trade.
        conn = sqlite3.connect(p.db)
        conn.execute("UPDATE trades SET status='closed', exit_time="
                      "'2026-09-04 08:00:00', exit_price=1900.0, "
                      "result='stop_loss', pnl_pct=-5.3 WHERE id=2")
        conn.commit()
        conn.close()

        sender = Sender()
        z = p.lauf(sender)
        check("Ein neu geschlossener Trade wird gemeldet",
              z["gesendet"] == 1 and sender.anzahl == 1, str(z))
        text = sender.texte[0]
        check("Die Nachricht nennt den verstaendlichen Bot-Namen, nicht den Ordner",
              "T3/ADX/SuperTrend (Krypto)" in text and "t3_supertrend" not in text,
              text.splitlines()[0])
        check("Sie nennt das Symbol", "ETHUSDT" in text)
        check("Das Ergebnis steht MIT Vorzeichen da",
              "-5.30 %" in text, [z for z in text.splitlines() if "%" in z][:1])
        check("Ein- UND Ausstiegskurs stehen da",
              "2000" in text and "1900" in text,
              [z for z in text.splitlines() if "Einstieg" in z])
        check("Die Haltedauer steht da",
              "Gehalten:" in text and "3 Tage" in text,
              [z for z in text.splitlines() if "Gehalten" in z])
        check("Der Ausstiegsgrund steht in VERSTAENDLICHER Form, nicht als Feldwert",
              "Stop-Loss ausgelöst" in text and "stop_loss" not in text,
              [z for z in text.splitlines() if "Grund" in z])
        check("Kein Euro- und kein Dollarbetrag in der Nachricht",
              "€" not in text and "$" not in text and "EUR" not in text
              and "USD" not in text.replace("ETHUSDT", ""))
        check("Der Vermerk steht als 'gesendet' in der eigenen Nachverfolgung",
              [v for v in p.vermerke()
               if v["trade_id"] == 2 and v["zustand"] == sb.ZUSTAND_GESENDET],
              str(p.vermerke()))

    # Ein Gewinn-Trade: anderes Vorzeichen, anderes Sinnbild.
    with Projekt([geschlossener_trade(1)]) as p:
        p.lauf(Sender())
        conn = sqlite3.connect(p.db)
        conn.execute("INSERT INTO trades (id, symbol, signal_time, entry_time, "
                      "entry_price, stop_price, exit_time, exit_price, result, "
                      "pnl_pct, status) VALUES (9,'BTCUSDT','2026-09-05 00:00:00',"
                      "'2026-09-05 00:00:00',50000.0,47500.0,'2026-09-05 06:00:00',"
                      "52000.0,'take_profit',4.0,'closed')")
        conn.commit(); conn.close()
        sender = Sender()
        p.lauf(sender)
        check("Ein Gewinn traegt ein Plus und ein gruenes Sinnbild",
              "+4.00 %" in sender.texte[0] and "\U0001F7E2" in sender.texte[0],
              sender.texte[0].splitlines()[1])
        check("Und den passenden Grund",
              "Kursziel erreicht" in sender.texte[0])


# ---------------------------------------------------------------------------
# 2. Doppelversand ist ausgeschlossen
# ---------------------------------------------------------------------------
def test_kein_doppelversand():
    print("\n2. Doppelversand ausgeschlossen - strukturell")

    with Projekt([geschlossener_trade(1)]) as p:
        p.lauf(Sender())                      # Erstlauf
        conn = sqlite3.connect(p.db)
        conn.execute("INSERT INTO trades (id, symbol, signal_time, entry_time, "
                      "entry_price, stop_price, exit_time, exit_price, result, "
                      "pnl_pct, status) VALUES (2,'ETHUSDT','2026-09-02 00:00:00',"
                      "'2026-09-02 00:00:00',2000.0,1900.0,'2026-09-03 00:00:00',"
                      "2100.0,'time_exit',5.0,'closed')")
        conn.commit(); conn.close()

        erster = Sender()
        p.lauf(erster)
        zweiter = Sender()
        z = p.lauf(zweiter)
        check("Der erste Lauf meldet, der zweite schickt NICHTS",
              erster.anzahl == 1 and zweiter.anzahl == 0 and z["gesendet"] == 0,
              f"{erster.anzahl} / {zweiter.anzahl}")

        # Die Sperre ist strukturell, nicht eine if-Abfrage: ein direkter
        # zweiter INSERT muss von SQLite abgelehnt werden.
        try:
            p.conn.execute(
                "INSERT INTO gemeldet (bot, trade_id, symbol, pnl_pct, zustand, "
                "zeitpunkt) VALUES (?,?,?,?,?,?)",
                ("t3_supertrend", 2, "ETHUSDT", 5.0, sb.ZUSTAND_GESENDET, "x"))
            check("UNIQUE(bot, trade_id) verhindert einen zweiten Vermerk", False)
        except sqlite3.IntegrityError as fehler:
            check("UNIQUE(bot, trade_id) verhindert einen zweiten Vermerk",
                  "UNIQUE" in str(fehler).upper(), str(fehler)[:60])

        # Und anspruch_nehmen() verlaesst sich darauf statt auf eine Liste.
        check("anspruch_nehmen() lehnt einen bereits vermerkten Trade ab",
              sb.anspruch_nehmen(p.conn, "t3_supertrend", {"id": 2}) is False)

    # DIE REIHENFOLGE, an der alles haengt: der Anspruch wird VOR dem Senden
    # genommen. Nur dann kann ein Abbruch zwischen Senden und Bestaetigen den
    # Trade nicht doppelt melden - und nur dann bekommen zwei gleichzeitig
    # laufende Laeufe nicht beide denselben Trade.
    #
    # Geprueft wird das nicht am Zustand HINTERHER (der laesst sich auch von
    # Hand herstellen, und genau daran ging die Gegenprobe M2 zuerst vorbei),
    # sondern WAEHREND des Sendens: die Attrappe sieht in die Nachverfolgung,
    # solange sie aufgerufen ist.
    with Projekt([geschlossener_trade(1)]) as p:
        p.conn.execute("INSERT INTO zustand (schluessel, wert) VALUES (?,?)",
                        (sb.MARKE_ERSTLAUF, "2026-09-01 00:00:00"))
        p.conn.commit()
        gesehen = []

        def sender_der_nachsieht(text):
            gesehen.append([dict(z) for z in p.conn.execute(
                "SELECT trade_id, zustand FROM gemeldet")])
            return True

        p.lauf(sender_der_nachsieht)
        check("Waehrend des Sendens liegt der Anspruch schon vor - er wird "
              "VORHER genommen, nicht erst danach",
              gesehen == [[{"trade_id": 1, "zustand": sb.ZUSTAND_WIRD_GESENDET}]],
              str(gesehen))

    # "Nachricht gesendet, Vermerk schlug fehl" - der Anspruch wird VOR dem
    # Senden genommen, deshalb kann dieser Fall den Trade nicht doppelt melden.
    with Projekt([geschlossener_trade(1), geschlossener_trade(2, "ETHUSDT", 2000.0)]) as p:
        p.conn.execute("INSERT INTO zustand (schluessel, wert) VALUES (?,?)",
                        (sb.MARKE_ERSTLAUF, "2026-09-01 00:00:00"))
        p.conn.commit()
        sender = Sender()
        p.lauf(sender)
        check("Zwei offene Meldungen, zwei Nachrichten", sender.anzahl == 2)
        # Ein abgebrochener Lauf: der Zustand bleibt auf 'wird_gesendet'.
        p.conn.execute("UPDATE gemeldet SET zustand=? WHERE trade_id=1",
                        (sb.ZUSTAND_WIRD_GESENDET,))
        p.conn.commit()
        nachher = Sender()
        p.lauf(nachher)
        check("Ein abgebrochener Lauf schickt beim naechsten Mal NICHT erneut",
              nachher.anzahl == 0, f"{nachher.anzahl} Nachricht(en)")
        check("Der unklare Zustand bleibt als solcher sichtbar, statt zu "
              "behaupten, es sei gesendet",
              [v for v in p.vermerke()
               if v["trade_id"] == 1 and v["zustand"] == sb.ZUSTAND_WIRD_GESENDET])


# ---------------------------------------------------------------------------
# 3. Fehlgeschlagener Versand fuehrt NICHT zum Vermerk
# ---------------------------------------------------------------------------
def test_versand_fehlgeschlagen():
    print("\n3. Fehlgeschlagener Versand - kein Vermerk, naechster Lauf erneut")

    with Projekt([geschlossener_trade(1), geschlossener_trade(2, "ETHUSDT", 2000.0)]) as p:
        p.conn.execute("INSERT INTO zustand (schluessel, wert) VALUES (?,?)",
                        (sb.MARKE_ERSTLAUF, "2026-09-01 00:00:00"))
        p.conn.commit()

        kaputt = Sender(scheitert_immer=True)
        z = p.lauf(kaputt)
        check("Der Versand wird versucht", kaputt.anzahl == 1)
        check("Nichts gilt als gesendet",
              z["gesendet"] == 0 and z["fehlgeschlagen"] == 1, str(z))
        check("Und es steht KEIN Vermerk in der Nachverfolgung",
              p.vermerke() == [], str(p.vermerke()))
        check("Der Lauf bricht nach dem ersten Fehlschlag ab und sagt, wie "
              "viele offen bleiben",
              z["nicht_versucht"] == 1, str(z))

        # Jetzt geht es wieder: beide Trades kommen, keiner ist verloren.
        heil = Sender()
        z2 = p.lauf(heil)
        check("Beim naechsten Lauf werden BEIDE nachgeholt",
              heil.anzahl == 2 and z2["gesendet"] == 2, str(z2))
        check("Danach stehen beide als gesendet da",
              all(v["zustand"] == sb.ZUSTAND_GESENDET for v in p.vermerke())
              and len(p.vermerke()) == 2, str(p.vermerke()))

    # Scheitert der ZWEITE Versand, bleibt der erste gemeldet und vermerkt.
    with Projekt([geschlossener_trade(1), geschlossener_trade(2, "ETHUSDT", 2000.0),
                   geschlossener_trade(3, "BNBUSDT", 600.0)]) as p:
        p.conn.execute("INSERT INTO zustand (schluessel, wert) VALUES (?,?)",
                        (sb.MARKE_ERSTLAUF, "2026-09-01 00:00:00"))
        p.conn.commit()
        sender = Sender(scheitert_ab=2)
        z = p.lauf(sender)
        check("Der erste geht raus, der zweite scheitert",
              z["gesendet"] == 1 and z["fehlgeschlagen"] == 1, str(z))
        vermerkt = {v["trade_id"]: v["zustand"] for v in p.vermerke()}
        check("Nur der erfolgreiche ist vermerkt",
              vermerkt == {1: sb.ZUSTAND_GESENDET}, str(vermerkt))
        # `nicht_versucht` zaehlt die, die gar nicht mehr versucht wurden -
        # hier Trade 3. Trade 2 IST versucht worden und gescheitert; sein
        # Anspruch ist freigegeben. Beim naechsten Lauf kommen also BEIDE.
        check("Der nicht mehr versuchte wird gezaehlt",
              z["nicht_versucht"] == 1, str(z)[:80])
        heil = Sender()
        z2 = p.lauf(heil)
        check("Und beim naechsten Lauf kommen BEIDE - der gescheiterte und der "
              "nicht versuchte",
              heil.anzahl == 2 and z2["gesendet"] == 2
              and {v["trade_id"] for v in p.vermerke()} == {1, 2, 3},
              str(z2)[:80])


# ---------------------------------------------------------------------------
# 4. Der Erstlauf
# ---------------------------------------------------------------------------
def test_erstlauf():
    print("\n4. Erstlauf: Bestand ueberspringen, EINE Bestaetigung")

    bestand = [geschlossener_trade(i, pnl=float(i)) for i in range(1, 301)]
    with Projekt(bestand) as p:
        sender = Sender()
        z = p.lauf(sender)
        check("300 bestehende Trades erzeugen KEINE 300 Nachrichten",
              sender.anzahl == 1, f"{sender.anzahl} Nachricht(en)")
        check("Sondern genau eine Bestaetigung, die die Zahl nennt",
              "300" in sender.texte[0] and "aktiv" in sender.texte[0],
              sender.texte[0].splitlines()[0])
        check("Der Bestand ist als uebersprungen vermerkt, nicht als gesendet",
              all(v["zustand"] == sb.ZUSTAND_ERSTLAUF for v in p.vermerke())
              and len(p.vermerke()) == 300)
        check("Das Ergebnis weist den Erstlauf aus",
              z["erstlauf"] is True and z["uebersprungen"] == 300, str(z)[:90])

        # Ab jetzt wird gemeldet.
        conn = sqlite3.connect(p.db)
        conn.execute("INSERT INTO trades (id, symbol, signal_time, entry_time, "
                      "entry_price, stop_price, exit_time, exit_price, result, "
                      "pnl_pct, status) VALUES (999,'AAPL','2026-09-10',"
                      "'2026-09-10',200.0,184.0,'2026-09-11',210.0,'time_exit',"
                      "5.0,'closed')")
        conn.commit(); conn.close()
        danach = Sender()
        z2 = p.lauf(danach)
        check("Der naechste neue Trade wird gemeldet",
              danach.anzahl == 1 and z2["gesendet"] == 1 and not z2["erstlauf"],
              str(z2)[:90])
        check("Und er ist es, nicht einer aus dem Bestand",
              "AAPL" in danach.texte[0])

    # Der Modus darf nicht ein zweites Mal greifen.
    with Projekt([geschlossener_trade(1)]) as p:
        p.lauf(Sender())
        lage = sb.erstlauf_lage(p.conn)
        check("Nach dem Erstlauf greift der Modus nicht mehr",
              lage["erstlauf"] is False and "bereits erfolgt" in lage["grund"],
              str(lage))
        # Selbst wenn jemand die Vermerke loescht, aber die Marke stehen bleibt.
        p.conn.execute("DELETE FROM gemeldet")
        p.conn.commit()
        lage = sb.erstlauf_lage(p.conn)
        check("Auch bei geloeschten Vermerken bleibt die Marke die Sperre",
              lage["erstlauf"] is False, str(lage))
        sender = Sender()
        z = p.lauf(sender)
        check("Der Bestand wird dann NORMAL gemeldet, nicht verschluckt",
              z["gesendet"] == 1 and sender.anzahl == 1
              and "Trade geschlossen" in sender.texte[0], str(z)[:90])

    # Und der Widerspruch: Marke fehlt, Vermerke da.
    with Projekt([geschlossener_trade(1), geschlossener_trade(2, "ETHUSDT", 2000.0)]) as p:
        p.conn.execute("INSERT INTO gemeldet (bot, trade_id, symbol, pnl_pct, "
                        "zustand, zeitpunkt) VALUES (?,?,?,?,?,?)",
                        ("t3_supertrend", 1, "BTCUSDT", 1.7,
                         sb.ZUSTAND_GESENDET, "2026-09-01 00:00:00"))
        p.conn.commit()
        lage = sb.erstlauf_lage(p.conn)
        check("Marke fehlt, aber Vermerke sind da -> Erstlauf wird ABGELEHNT",
              lage["erstlauf"] is False and lage["widerspruch"] is True,
              str(lage["grund"])[:80])
        sender = Sender()
        z = p.lauf(sender)
        check("Der Lauf meldet dann normal weiter, statt den Bestand zu "
              "verschlucken",
              z["gesendet"] == 1 and z["widerspruch"] is True, str(z)[:90])
        check("Und der uebrige Trade ist der gemeldete",
              "ETHUSDT" in sender.texte[0])


# ---------------------------------------------------------------------------
# 5. Beide Modi
# ---------------------------------------------------------------------------
def test_beide_modi():
    print("\n5. Beide Modi: einzeln und gebuendelt")

    trades = [geschlossener_trade(1, "BTCUSDT", 50000.0, 51000.0, "trend_flip", 1.7),
              geschlossener_trade(2, "ETHUSDT", 2000.0, 1900.0, "stop_loss", -5.3),
              geschlossener_trade(3, "BNBUSDT", 600.0, 620.0, "time_exit", 3.0)]

    with Projekt(trades) as p:
        p.conn.execute("INSERT INTO zustand (schluessel, wert) VALUES (?,?)",
                        (sb.MARKE_ERSTLAUF, "2026-09-01 00:00:00"))
        p.conn.commit()
        sender = Sender()
        z = p.lauf(sender, modus=sb.MODUS_EINZELN)
        check("EINZELN: drei Trades, drei Nachrichten",
              sender.anzahl == 3 and z["gesendet"] == 3, str(z)[:90])
        check("Jede nennt genau ein Symbol",
              all(sum(s in t for s in ("BTCUSDT", "ETHUSDT", "BNBUSDT")) == 1
                  for t in sender.texte))

    with Projekt(trades) as p:
        p.conn.execute("INSERT INTO zustand (schluessel, wert) VALUES (?,?)",
                        (sb.MARKE_ERSTLAUF, "2026-09-01 00:00:00"))
        p.conn.commit()
        sender = Sender()
        z = p.lauf(sender, modus=sb.MODUS_GEBUENDELT)
        check("GEBUENDELT: drei Trades, EINE Nachricht",
              sender.anzahl == 1 and z["gesendet"] == 3, str(z)[:90])
        text = sender.texte[0]
        check("Sie nennt alle drei Symbole",
              all(s in text for s in ("BTCUSDT", "ETHUSDT", "BNBUSDT")), text[:80])
        check("Mit Vorzeichen je Zeile",
              "+1.70 %" in text and "-5.30 %" in text and "+3.00 %" in text)
        check("Und mit dem verstaendlichen Grund je Zeile",
              "Stop-Loss ausgelöst" in text and "stop_loss" not in text)
        check("Alle drei sind vermerkt",
              len(p.vermerke()) == 3
              and all(v["zustand"] == sb.ZUSTAND_GESENDET for v in p.vermerke()))

    # Gebuendelt und der Versand scheitert: KEIN Vermerk, alle kommen erneut.
    with Projekt(trades) as p:
        p.conn.execute("INSERT INTO zustand (schluessel, wert) VALUES (?,?)",
                        (sb.MARKE_ERSTLAUF, "2026-09-01 00:00:00"))
        p.conn.commit()
        z = p.lauf(Sender(scheitert_immer=True), modus=sb.MODUS_GEBUENDELT)
        check("GEBUENDELT mit Fehlschlag: nichts vermerkt, alle bleiben offen",
              p.vermerke() == [] and z["nicht_versucht"] == 3, str(z)[:90])
        heil = Sender()
        z2 = p.lauf(heil, modus=sb.MODUS_GEBUENDELT)
        check("Und beim naechsten Lauf gehen sie zusammen raus",
              heil.anzahl == 1 and z2["gesendet"] == 3)

    check("Der Standardmodus ist 'einzeln' - so hat der Nutzer entschieden",
          sb.BENACHRICHTIGUNG_MODUS == sb.MODUS_EINZELN)
    try:
        sb.lauf(senden=Sender(), conn=None, modus="unsinn")
        check("Ein unbekannter Modus wird abgelehnt", False)
    except sb.BenachrichtigungFehler as fehler:
        check("Ein unbekannter Modus wird abgelehnt",
              "unsinn" in str(fehler) and "nichts gesendet" in str(fehler).lower(),
              str(fehler)[:70])


# ---------------------------------------------------------------------------
# 6. Obergrenze je Lauf
# ---------------------------------------------------------------------------
def test_obergrenze():
    print("\n6. Obergrenze je Lauf - der Rest als EINE Sammelnachricht")

    trades = [geschlossener_trade(i, f"SYM{i}USDT", 100.0 + i, 101.0 + i,
                                   "time_exit", float(i) / 10)
              for i in range(1, 31)]
    with Projekt(trades) as p:
        p.conn.execute("INSERT INTO zustand (schluessel, wert) VALUES (?,?)",
                        (sb.MARKE_ERSTLAUF, "2026-09-01 00:00:00"))
        p.conn.commit()
        sender = Sender()
        z = p.lauf(sender, grenze=25)
        check("30 Schliessungen, Grenze 25 -> 25 einzeln plus EINE Sammelnachricht",
              sender.anzahl == 26 and z["sammelnachricht"] is True, str(z)[:90])
        check("Alle 30 gelten als gesendet - keiner faellt unter den Tisch",
              z["gesendet"] == 30, str(z)[:90])
        check("Und alle 30 sind vermerkt",
              len(p.vermerke()) == 30
              and all(v["zustand"] == sb.ZUSTAND_GESENDET for v in p.vermerke()))
        sammel = sender.texte[-1]
        check("Die Sammelnachricht sagt, WARUM sie zusammengefasst ist",
              "zusammengefasst" in sammel and "25" in sammel,
              sammel.splitlines()[0][:80])
        check("Und sie enthaelt die uebrigen fuenf Symbole",
              all(f"SYM{i}USDT" in sammel for i in range(26, 31)),
              sammel.splitlines()[1][:60])
        check("Die ersten 25 stehen NICHT in der Sammelnachricht",
              "SYM1USDT" not in sammel)

        zweiter = Sender()
        check("Ein zweiter Lauf schickt nichts mehr",
              p.lauf(zweiter)["gesendet"] == 0 and zweiter.anzahl == 0)

    # Scheitert die Sammelnachricht, bleibt der Rest offen - die einzeln
    # gesendeten bleiben aber vermerkt.
    with Projekt(trades) as p:
        p.conn.execute("INSERT INTO zustand (schluessel, wert) VALUES (?,?)",
                        (sb.MARKE_ERSTLAUF, "2026-09-01 00:00:00"))
        p.conn.commit()
        sender = Sender(scheitert_ab=26)
        z = p.lauf(sender, grenze=25)
        check("Scheitert die Sammelnachricht, bleiben genau die uebrigen offen",
              z["gesendet"] == 25 and z["nicht_versucht"] == 5, str(z)[:90])
        check("Und nur die 25 einzeln gesendeten sind vermerkt",
              len(p.vermerke()) == 25, str(len(p.vermerke())))


# ---------------------------------------------------------------------------
# 7. Die Bot-Datenbank bleibt unberuehrt - geprueft, nicht behauptet
# ---------------------------------------------------------------------------
def test_nur_lesend():
    print("\n7. Bot-Datenbank: byteweise unveraendert, Schreiben verweigert")

    trades = [geschlossener_trade(1), geschlossener_trade(2, "ETHUSDT", 2000.0),
              offener_trade(3, "BNBUSDT", 600.0)]
    with Projekt(trades) as p:
        vorher = p.pruefsumme()
        p.lauf(Sender())                       # Erstlauf
        p.lauf(Sender())                       # normaler Lauf
        p.lauf(Sender(scheitert_immer=True))   # Fehlschlag
        sb.offene_meldungen(p.conn, p.wurzel)
        check("Nach Erstlauf, Lauf und Fehlschlag: Datenbank byteweise gleich",
              p.pruefsumme() == vorher)

        # mode=ro ist kein Vorsatz, sondern eine Sperre - hier belegt.
        conn = sqlite3.connect(f"file:{p.db}?mode=ro", uri=True)
        try:
            conn.execute("UPDATE trades SET status='open' WHERE id=1")
            conn.commit()
            check("SQLite verweigert den Schreibversuch im Modus mode=ro", False)
        except sqlite3.OperationalError as fehler:
            check("SQLite verweigert den Schreibversuch im Modus mode=ro",
                  "readonly" in str(fehler).lower(), str(fehler)[:55])
        finally:
            conn.close()

        namen = sorted(z[0] for z in sqlite3.connect(p.db).execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%'"))
        check("Im Schema des Bots ist keine neue Tabelle entstanden",
              namen == ["trades"], str(namen))

    # Struktureller Nachweis: das Modul liest die Bot-DB nur ueber bot_db.
    quelle = open(os.path.join(_DIR, "schliess_benachrichtigung.py"),
                   encoding="utf-8").read()
    baum = ast.parse(quelle)
    verbotene = [k for k in ast.walk(baum)
                 if isinstance(k, (ast.Import, ast.ImportFrom))
                 and any(n.name.split(".")[0] in ("forward_test", "live_params",
                                                   "equity_simulation")
                          for n in k.names)]
    check("Es wird kein forward_test/live_params/equity_simulation importiert",
          not verbotene, str(verbotene))
    check("Die Bot-Datenbank wird ausschliesslich ueber broker/bot_db.py gelesen",
          "bot_db.lies_trades(" in quelle
          and "paper_trading_" not in quelle.replace(
              "benachrichtigungen_schliessung", ""),
          "eigener DB-Pfad nachgebaut?")


# ---------------------------------------------------------------------------
# 8. Formulierungen: Gruende, Haltedauer, Sonderzeichen
# ---------------------------------------------------------------------------
def test_formulierungen():
    print("\n8. Ausstiegsgruende, Haltedauer, Sonderzeichen")

    # Jeder Wert, den irgendein Bot schreibt, hat eine Uebersetzung. Die Liste
    # stammt aus den echten forward_test.py-Dateien.
    aus_den_bots = ["stop_loss", "take_profit", "time_exit", "sma_exit",
                    "trend_flip", "t3_crossunder", "manual_close"]
    for wert in aus_den_bots:
        text = sb.grundtext(wert)
        check(f"'{wert}' hat eine verstaendliche Formulierung",
              wert not in text and len(text) > 8, text)
    check("Ein UNBEKANNTER Wert wird woertlich durchgereicht und gekennzeichnet",
          "xyz_exit" in sb.grundtext("xyz_exit")
          and "unbekannt" in sb.grundtext("xyz_exit"), sb.grundtext("xyz_exit"))
    check("Ein fehlender Wert wird benannt, nicht geraten",
          "nicht vermerkt" in sb.grundtext(None), sb.grundtext(None))

    check("Haltedauer ueber Tage und Stunden",
          sb.haltedauer_text("2026-09-01 04:00:00", "2026-09-03 09:00:00")
          == "2 Tage 5 Std.",
          sb.haltedauer_text("2026-09-01 04:00:00", "2026-09-03 09:00:00"))
    check("Einzahl bei einem Tag",
          sb.haltedauer_text("2026-09-01", "2026-09-02") == "1 Tag",
          sb.haltedauer_text("2026-09-01", "2026-09-02"))
    check("Reine Datumsform (Tages-Bots) wird gelesen",
          sb.haltedauer_text("2026-09-01", "2026-09-05") == "4 Tage")
    check("Minuten nur, wenn es nicht um Tage geht",
          sb.haltedauer_text("2026-09-01 04:00:00", "2026-09-01 05:30:00")
          == "1 Std. 30 Min.",
          sb.haltedauer_text("2026-09-01 04:00:00", "2026-09-01 05:30:00"))
    for kaputt in ((None, None), ("2026-09-01", None), ("unsinn", "auch"),
                    ("2026-09-05", "2026-09-01")):
        check(f"Unbrauchbare Zeiten ergeben 'unbekannt' statt einer Zahl {kaputt}",
              sb.haltedauer_text(*kaputt) == "unbekannt",
              sb.haltedauer_text(*kaputt))

    # Legacy-Markdown kennt kein Escaping (siehe notify.send_report) - die drei
    # wirksamen Zeichen muessen aus eingesetzten Werten VERSCHWINDEN, sonst
    # zerreisst ein Symbolname die Formatierung der ganzen Nachricht.
    def nachricht_mit(symbol):
        return sb.nachricht_fuer("t3_supertrend", {
            "id": 1, "symbol": symbol, "entry_price": 1.0, "exit_price": 2.0,
            "result": "stop_loss", "pnl_pct": 1.0,
            "entry_time": "2026-09-01", "exit_time": "2026-09-02"})

    kaputt = nachricht_mit("BTC*USD_T`")
    sauber = nachricht_mit("BTCUSDT")
    check("Sternchen, Unterstrich und Backtick werden aus Werten entfernt",
          "BTCUSDT" in kaputt and "_" not in kaputt and "`" not in kaputt,
          repr(kaputt.splitlines()[1]))
    # Die eigentliche Zusicherung: die Formatierung der Nachricht ist danach
    # GENAUSO ausbalanciert wie bei einem harmlosen Symbol. Ein ungepaartes
    # Sternchen wuerde in Telegrams Legacy-Markdown die ganze Nachricht
    # zerreissen, und escapen laesst es sich dort nicht (siehe
    # notify.send_report).
    check("Die Markdown-Paarung bleibt dieselbe wie bei einem harmlosen Symbol",
          kaputt.count("*") == sauber.count("*") == 6
          and kaputt.count("*") % 2 == 0,
          f"{kaputt.count('*')} vs. {sauber.count('*')}")

    check("Eine fehlende PnL-Zahl wird benannt, nicht als 0 dargestellt",
          "nicht vermerkt" in sb.nachricht_fuer("t3_supertrend", {
              "id": 1, "symbol": "X", "entry_price": 1, "exit_price": 2,
              "result": "time_exit", "pnl_pct": None,
              "entry_time": "2026-09-01", "exit_time": "2026-09-02"}))


# ---------------------------------------------------------------------------
# 9. Randfaelle
# ---------------------------------------------------------------------------
def test_randfaelle():
    print("\n9. Randfaelle")

    with Projekt([offener_trade(1)]) as p:
        sender = Sender()
        z = p.lauf(sender)
        check("Ohne geschlossene Trades meldet der Erstlauf 0 uebersprungene",
              z["erstlauf"] and z["uebersprungen"] == 0 and sender.anzahl == 1,
              str(z)[:80])
        leer = Sender()
        check("Und danach passiert bei nichts zu melden nichts",
              p.lauf(leer)["gesendet"] == 0 and leer.anzahl == 0)

    # Eine fehlende Bot-Datenbank ist kein Fehler.
    with Projekt([geschlossener_trade(1)]) as p:
        check("Ein Bot ohne Datenbank wird uebersprungen, nicht zum Fehler",
              sb.geschlossene_trades("elliott_wave", p.wurzel) == [])
        check("Der vorhandene Bot wird trotzdem gelesen",
              len(sb.geschlossene_trades("t3_supertrend", p.wurzel)) == 1)

    check("Die Bot-Liste kommt aus monitor.ASSET_CLASS - der EINEN Quelle",
          sb.bot_liste() == sorted(monitor.ASSET_CLASS)
          and len(sb.bot_liste()) == 9, str(len(sb.bot_liste())))

    # Die eigene Nachverfolgung liegt NICHT in der Bot-Datenbank.
    check("Die eigene Datenbank hat einen eigenen Namen",
          "benachrichtigungen" in os.path.basename(sb.db_pfad())
          and "paper_trading" not in sb.db_pfad(), sb.db_pfad())


# ---------------------------------------------------------------------------
# 10. Die alte Meldung ist wirklich weg
# ---------------------------------------------------------------------------
def test_alte_meldung_weg():
    print("\n10. Die alte, duenne Schliess-Meldung in monitor.py ist weg")

    quelle = open(os.path.join(_DIR, "monitor.py"), encoding="utf-8").read()
    ohne_kommentare = "\n".join(
        z for z in quelle.splitlines() if not z.strip().startswith("#"))
    check("monitor.py erzeugt keine Schliess-Meldung mehr",
          "STOP-LOSS ausgeloest" not in ohne_kommentare
          and "newly_closed_ids" not in ohne_kommentare)
    check("Die Eroeffnungs-Meldung ist unberuehrt",
          "Neuer Trade eroeffnet" in ohne_kommentare)
    check("Die Cronjob-Warnung ist unberuehrt",
          "Cronjob-Fehler/Script-Abbruch" in ohne_kommentare)
    check("Die Staleness-Warnung ist unberuehrt",
          "kein Cronjob-Lauf" in ohne_kommentare)
    check("Der Zustand wird weiter gefuehrt - er traegt die Erkennung NEUER "
          "Trades und die Staleness",
          "known_open_ids" in ohne_kommentare and "max_id" in ohne_kommentare)
    check("Und an der Stelle steht, wohin die Meldung umgezogen ist",
          "schliess_benachrichtigung" in quelle)

    # Der Beweis am Verhalten: ein geschlossener Trade erzeugt kein Ereignis
    # mehr, ein neu eroeffneter schon.
    wurzel = tempfile.mkdtemp(prefix="monitorprobe_")
    try:
        os.makedirs(os.path.join(wurzel, "strategies", "t3_supertrend"))
        os.makedirs(os.path.join(wurzel, "logs", "t3_supertrend"))
        db = os.path.join(wurzel, "paper_trading_t3_supertrend.db")
        conn = sqlite3.connect(db)
        conn.execute(echtes_create_table())
        conn.execute("INSERT INTO trades (id, symbol, signal_time, entry_time, "
                      "entry_price, stop_price, status) VALUES (1,'BTCUSDT',"
                      "'2026-09-01 00:00:00','2026-09-01 00:00:00',50000.0,"
                      "47500.0,'open')")
        conn.commit(); conn.close()

        alt = (monitor.BASE_DIR, monitor.STRATEGIES_DIR, monitor.LOGS_DIR,
               monitor.STATE_FILE)
        monitor.BASE_DIR = wurzel
        monitor.STRATEGIES_DIR = os.path.join(wurzel, "strategies")
        monitor.LOGS_DIR = os.path.join(wurzel, "logs")
        monitor.STATE_FILE = os.path.join(wurzel, "state.json")
        try:
            _, zustand = monitor.check_for_events()
            monitor._save_state(zustand)
            conn = sqlite3.connect(db)
            conn.execute("UPDATE trades SET status='closed', exit_time="
                          "'2026-09-02 04:00:00', exit_price=47500.0, "
                          "result='stop_loss', pnl_pct=-5.3 WHERE id=1")
            conn.commit(); conn.close()
            ereignisse, zustand = monitor.check_for_events()
            check("Eine Schliessung erzeugt in monitor.py KEIN Ereignis mehr",
                  ereignisse == [], str(ereignisse)[:90])
            monitor._save_state(zustand)

            conn = sqlite3.connect(db)
            conn.execute("INSERT INTO trades (id, symbol, signal_time, "
                          "entry_time, entry_price, stop_price, status) VALUES "
                          "(2,'ETHUSDT','2026-09-03 00:00:00',"
                          "'2026-09-03 00:00:00',2000.0,1900.0,'open')")
            conn.commit(); conn.close()
            ereignisse, _ = monitor.check_for_events()
            check("Eine EROEFFNUNG erzeugt weiterhin ein Ereignis",
                  len(ereignisse) == 1 and "eroeffnet" in ereignisse[0],
                  str(ereignisse)[:90])
        finally:
            (monitor.BASE_DIR, monitor.STRATEGIES_DIR, monitor.LOGS_DIR,
             monitor.STATE_FILE) = alt
    finally:
        shutil.rmtree(wurzel, ignore_errors=True)


# ---------------------------------------------------------------------------
def main():
    print("Selbsttests der Schliess-Benachrichtigung")
    for pruefung in (test_grundfall, test_kein_doppelversand,
                      test_versand_fehlgeschlagen, test_erstlauf,
                      test_beide_modi, test_obergrenze, test_nur_lesend,
                      test_formulierungen, test_randfaelle,
                      test_alte_meldung_weg):
        pruefung()

    print("\n" + "=" * 78)
    print(f"{sum(BESTANDEN)} von {len(BESTANDEN)} Pruefungen bestanden, "
          f"{len(FEHLER)} fehlgeschlagen.")
    if FEHLER:
        for f in FEHLER:
            print(f"  - {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
