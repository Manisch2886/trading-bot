"""
Selbsttests: der Agenten-Schalter config/agenten_aus.txt (TB-159)
====================================================================
Prueft claude_client.agent_abgeschaltet() (an, aus, Datei fehlt,
Kommentar, unbekannter Name, nicht lesbar) und dass die Agenten 1, 3 und 4
bei "aus" die API NICHT aufrufen und dasselbe zurueckgeben wie bei einem
fehlgeschlagenen Aufruf (leerer Text).

Kein Test ruft die API auf: anthropic wird als Platzhalter-Modul in einem
temporaeren Verzeichnis angelegt (wirft beim Erzeugen eines Clients), und
call_claude wird in jedem Agent-Modul durch eine Zaehlfunktion ersetzt.
Die Schalterdateien der Faelle liegen im temporaeren Verzeichnis; die
verfolgte config/agenten_aus.txt wird nur gelesen.

Nutzung:  python3 shared/test_agenten_aus.py
"""

import contextlib
import inspect
import io
import os
import sys
import tempfile

DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(DIR)

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append(bool(ok))
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        raise SystemExit(f"\nFEHLGESCHLAGEN: {name}\n{detail}")


STUB_DIR = tempfile.mkdtemp(prefix="tb159_stubs_")
with open(os.path.join(STUB_DIR, "anthropic.py"), "w") as f:
    f.write("class Anthropic:\n"
            "    def __init__(self, *a, **k):\n"
            "        raise RuntimeError('Test darf die API nicht aufrufen')\n")
sys.path.insert(0, STUB_DIR)
sys.path.insert(0, DIR)

import claude_client                      # noqa: E402
import daily_interpreter                  # noqa: E402
import market_context_agent               # noqa: E402
import portfolio_interpreter_agent        # noqa: E402

ARBEIT = tempfile.mkdtemp(prefix="tb159_schalter_")
FEHLT = os.path.join(ARBEIT, "gibt_es_nicht.txt")


def schalterdatei(inhalt):
    pfad = os.path.join(ARBEIT, "agenten_aus.txt")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(inhalt)
    return pfad


def abfrage(name, pfad):
    puffer = io.StringIO()
    with contextlib.redirect_stdout(puffer):
        ergebnis = claude_client.agent_abgeschaltet(name, pfad)
    return ergebnis, puffer.getvalue()


def teste_funktion():
    print("\n1) agent_abgeschaltet()")
    p = schalterdatei("# Kopf\nagent1\nagent3\nagent4\n")
    for name, n in (("agent1", "1"), ("agent3", "3"), ("agent4", "4")):
        aus, log = abfrage(name, p)
        check(f"aus: {name} steht in der Datei", aus is True)
        check(f"aus: {name} schreibt die Logzeile",
              log.strip() == f"Agent {n} abgeschaltet (config/agenten_aus.txt)", repr(log))
    aus, log = abfrage("agent1", schalterdatei("agent3\n"))
    check("an: agent1 fehlt in der Datei, keine Logzeile", aus is False and log == "", repr(log))
    check("Datei fehlt: alle drei an, keine Logzeile",
          all(abfrage(a, FEHLT) == (False, "") for a in ("agent1", "agent3", "agent4")))
    p = schalterdatei("# agent1\n  # agent3 ist aus\nagent4   # Wochen-Mail\n\n")
    check("Kommentar: auskommentierte Zeilen schalten nicht ab",
          abfrage("agent1", p)[0] is False and abfrage("agent3", p)[0] is False)
    check("Kommentar hinter dem Namen wird abgeschnitten", abfrage("agent4", p)[0] is True)
    p = schalterdatei("agent9\nagent 1\nAgent1\nagent13\n")
    check("unbekannte Namen schalten keinen der drei ab",
          all(abfrage(a, p)[0] is False for a in ("agent1", "agent3", "agent4")))
    aus, log = abfrage("agent1", ARBEIT)   # ein Verzeichnis statt einer Datei: nicht lesbar
    check("nicht lesbare Schalterdatei: Agent bleibt aus, mit Warnung",
          aus is True and "nicht lesbar" in log, repr(log))


def teste_agenten():
    print("\n2) Die drei Agenten: aus = kein API-Aufruf, an = genau ein Aufruf")
    aufrufe = []

    def zaehler(*a, **k):
        aufrufe.append(a)
        return {"success": True, "text": "TESTTEXT", "stop_reason": "end_turn", "raw": None}

    faelle = (("agent1", daily_interpreter,
               lambda: daily_interpreter.generate_interpretation("bot", "Zusammenfassung")),
              ("agent3", market_context_agent,
               lambda: market_context_agent.get_market_context(["BTCUSDT"], "bot")),
              ("agent4", portfolio_interpreter_agent,
               lambda: portfolio_interpreter_agent.generate_portfolio_interpretation("Uebersicht")))
    alt = claude_client.AGENTEN_AUS_DATEI
    try:
        for name, modul, aufruf in faelle:
            original = modul.call_claude
            modul.call_claude = zaehler
            try:
                claude_client.AGENTEN_AUS_DATEI = schalterdatei(name + "\n")
                del aufrufe[:]
                puffer = io.StringIO()
                with contextlib.redirect_stdout(puffer):
                    ergebnis = aufruf()
                check(f"{name} aus: leerer Text, kein Aufruf von call_claude",
                      ergebnis == "" and aufrufe == [], f"{ergebnis!r}, {len(aufrufe)} Aufrufe")
                check(f"{name} aus: Logzeile", "abgeschaltet (config/agenten_aus.txt)" in puffer.getvalue())
                claude_client.AGENTEN_AUS_DATEI = FEHLT
                ergebnis = aufruf()
                check(f"{name} an (Datei fehlt): genau ein Aufruf, Text kommt durch",
                      ergebnis == "TESTTEXT" and len(aufrufe) == 1, f"{ergebnis!r}, {len(aufrufe)} Aufrufe")
            finally:
                modul.call_claude = original
    finally:
        claude_client.AGENTEN_AUS_DATEI = alt


def teste_quelle():
    print("\n3) Die Pruefung liest nur die Schalterdatei")
    quelle = inspect.getsource(claude_client.agent_abgeschaltet)
    for wort in ("environ", "getenv", "email_config", "API_KEY", "get_client", "call_claude"):
        check(f"agent_abgeschaltet() enthaelt kein '{wort}'", wort not in quelle)
    check("Pfad ist config/agenten_aus.txt im Repo",
          claude_client.AGENTEN_AUS_DATEI == os.path.join(REPO_ROOT, "config", "agenten_aus.txt"))


def teste_verfolgte_datei():
    print("\n4) Die verfolgte Schalterdatei (Inhalt darf sich aendern)")
    pfad = claude_client.AGENTEN_AUS_DATEI
    if not os.path.isfile(pfad):
        check("Datei fehlt - zulaessig, alle drei Agenten laufen", True)
        return
    with open(pfad, encoding="utf-8") as f:
        inhalt = f.read()
    namen = [z.split("#", 1)[0].strip() for z in inhalt.splitlines()]
    namen = [n for n in namen if n]
    check("jeder Name ist agent1, agent3 oder agent4",
          all(n in ("agent1", "agent3", "agent4") for n in namen), repr(namen))
    check("Kopfkommentar sagt, wie man wieder einschaltet",
          "wieder ein" in inhalt and "löschen" in inhalt)
    print(f"  Stand der Datei: aus = {', '.join(namen) or 'keiner'}")


if __name__ == "__main__":
    print("Selbsttests Agenten-Schalter (TB-159)")
    teste_funktion()
    teste_agenten()
    teste_quelle()
    teste_verfolgte_datei()
    print(f"\nAlle {len(CHECKS)} Pruefungen bestanden.")
