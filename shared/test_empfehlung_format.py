"""
Selbsttests der Empfehlungs-Hervorhebung
====================================================================
Prueft, dass Handlungsempfehlungen der Agenten in den Telegram-Berichten
tatsaechlich erkannt, hervorgehoben und - bei Typ B - untrennbar mit dem
Unvalidiert-Pflichthinweis versehen werden. Und, genauso wichtig, dass
ohne Empfehlung KEIN leerer oder falscher Hervorhebungs-Block entsteht.

Die End-to-End-Faelle importieren die echten Versand-Skripte
(quarterly_review.py, weekly_portfolio_email.py) - keine nachgebauten
Kopien ihrer Logik. Die dafuer noetigen Zugangsdaten-/Netzwerk-Module
(email_config, telegram_config, anthropic, binance, fetch_binance_data)
werden als Stubs in einem temporaeren Verzeichnis erzeugt: Es wird
NICHTS verschickt, nichts geladen und keine echte Konfiguration gelesen.
Der Telegram-Versand wird ueber ein ersetztes send_alert() abgefangen,
das die Nachrichten nur einsammelt.

Nutzung:  python3 shared/test_empfehlung_format.py
"""

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


def stubs_anlegen() -> str:
    """Legt die Platzhalter-Module an, ohne die die Versand-Skripte nicht
    importierbar waeren. Alle Funktionen, die etwas verschicken oder laden
    wuerden, werfen AssertionError - faellt der Test also versehentlich in
    einen echten Aufruf, bricht er ab, statt still etwas zu tun."""
    d = tempfile.mkdtemp(prefix="empfehlung_stubs_")

    open(os.path.join(d, "email_config.py"), "w").write(
        "# Stub - keine echten Zugangsdaten\n"
        "EMAIL_ADDRESS = 'stub@example.invalid'\n"
        "RECIPIENT_EMAIL = 'stub@example.invalid'\n"
        "EMAIL_PASSWORD = ''\n"
        "SMTP_SERVER = 'localhost'\n"
        "SMTP_PORT = 465\n"
        "USE_SSL = True\n")

    open(os.path.join(d, "telegram_config.py"), "w").write(
        "def get_credentials():\n"
        "    raise AssertionError('Stub: es darf nichts an Telegram gehen')\n")

    open(os.path.join(d, "anthropic.py"), "w").write(
        "class Anthropic:\n"
        "    def __init__(self, *a, **k):\n"
        "        raise AssertionError('Stub: keine Claude-API-Aufrufe im Test')\n")

    os.makedirs(os.path.join(d, "binance"), exist_ok=True)
    open(os.path.join(d, "binance", "__init__.py"), "w").write("from .client import Client\n")
    open(os.path.join(d, "binance", "client.py"), "w").write(
        # Metaclass-__getattr__, weil die Bots Klassen-Konstanten wie
        # Client.KLINE_INTERVAL_1HOUR beim Import lesen.
        "class _Meta(type):\n"
        "    def __getattr__(cls, name):\n"
        "        return name\n"
        "class Client(metaclass=_Meta):\n"
        "    def __init__(self, *a, **k):\n"
        "        pass\n"
        "    def __getattr__(self, name):\n"
        "        raise AssertionError('Stub: keine Netzwerkzugriffe im Test')\n")

    open(os.path.join(d, "fetch_binance_data.py"), "w").write(
        "API_KEY = ''\nAPI_SECRET = ''\n"
        "def fetch_historical_data(*a, **k):\n"
        "    raise AssertionError('Stub: es duerfen keine Kursdaten geladen werden')\n")

    return d


STUB_DIR = stubs_anlegen()
sys.path.insert(0, STUB_DIR)
sys.path.insert(0, DIR)
sys.path.insert(0, os.path.join(REPO_ROOT, "notifications"))

import empfehlung_format as ef            # noqa: E402
import notify                             # noqa: E402


# --- Beispieltexte, wie sie die Agenten liefern koennten -------------------

DAILY_MIT_HINWEIS = """Ruhiger Tag mit zwei geschlossenen Trades, beide im
erwarteten Bereich. Die Trefferquote liegt weiter im historischen Rahmen.

[HINWEIS]
Drei der letzten vier Trades wurden per Stop-Loss beendet, also automatisch
mit Verlust geschlossen, weil der Kurs unter die vorher festgelegte Grenze
gefallen ist. Das kommt bei dieser Strategie selten vor und waere in den
naechsten Tagen zu beobachten.""".strip()

DAILY_OHNE_HINWEIS = ("Ruhiger Tag, keine besonderen Auffaelligkeiten. Es wurde "
                       "kein Trade eroeffnet oder geschlossen.")

PORTFOLIO_MIT_HINWEIS = """WAS DAS FUER DICH BEDEUTET

Diese Woche ist nichts zu tun, alles laeuft wie erwartet.

Die Bots laufen noch zu kurz, um belastbare Aussagen zur Diversifikation zu
treffen.

[HINWEIS]
Der Korrelationswert zwischen zwei Bots naehert sich der Alarmschwelle, das
heisst, sie bewegen sich zunehmend gleichzeitig. Falls das anhaelt, waere zu
ueberlegen, ob beide zusammen noch den erhofften Ausgleich bringen."""

QUARTALS_EMPFEHLUNG = ("Empfehlung: Parameter beibehalten. Der Vorschlag sieht "
                        "In-Sample besser aus, faellt aber Out-of-Sample - also auf "
                        "Daten, die bei der Optimierung nicht verwendet wurden - "
                        "deutlich ab. Das ist ein klassisches Overfitting-Muster.")


def teste_erkennung():
    print("\n1) Erkennung des Hinweis-Abschnitts")

    analyse, hinweis = ef.teile_hinweis(DAILY_MIT_HINWEIS)
    check("Marker-Zeile trennt Analyse und Hinweis",
          "Stop-Loss" in hinweis and "Ruhiger Tag" in analyse)
    check("Marker-Zeile selbst steht in keinem der beiden Teile",
          ef.MARKER_HINWEIS not in analyse and ef.MARKER_HINWEIS not in hinweis)

    analyse, hinweis = ef.teile_hinweis("Analyse-Satz.\n[hinweis]: Etwas zu beobachten.")
    check("Marker wird auch klein geschrieben, mit Doppelpunkt und Text in derselben "
          "Zeile erkannt", hinweis == "Etwas zu beobachten." and analyse == "Analyse-Satz.",
          f"hinweis={hinweis!r}")

    analyse, hinweis = ef.teile_hinweis(DAILY_OHNE_HINWEIS)
    check("Ohne Marker bleibt der Hinweis leer", hinweis == "" and analyse == DAILY_OHNE_HINWEIS)

    analyse, hinweis = ef.teile_hinweis("Analyse-Satz.\n\n[HINWEIS]\n   \n")
    check("Marker ohne Inhalt zaehlt nicht als Hinweis", hinweis == "",
          "sonst entstuende ein leerer Hervorhebungs-Block")

    check("teile_hinweis vertraegt leeren Text", ef.teile_hinweis("") == ("", ""))


def teste_typ_a():
    print("\n2) Typ A - Interpretations-Hinweis")

    block = ef.formatiere_typ_a(DAILY_MIT_HINWEIS, "KI-EINORDNUNG DES TAGES")
    check("Hervorhebungs-Ueberschrift vorhanden", ef.HEADER_TYP_A in block)
    check("Fester Vorspann 'keine geprüfte Handlungsanweisung' vorhanden",
          "keine geprüfte Handlungsanweisung" in block.replace("KEINE", "keine"))
    check("Hinweis steht VOR dem uebrigen Analyse-Text",
          block.index(ef.HEADER_TYP_A) < block.index("KI-EINORDNUNG DES TAGES"))
    check("Analyse-Text bleibt vollstaendig erhalten", "Trefferquote" in block)
    check("Hinweis-Text bleibt vollstaendig erhalten", "Stop-Loss" in block)

    ohne = ef.formatiere_typ_a(DAILY_OHNE_HINWEIS, "KI-EINORDNUNG DES TAGES")
    erwartet = f"{'=' * 50}\nKI-EINORDNUNG DES TAGES\n{'=' * 50}\n{DAILY_OHNE_HINWEIS}"
    check("Ohne Hinweis exakt das bisherige Format (kein leerer Block)",
          ohne == erwartet, f"\n--- erhalten ---\n{ohne}\n--- erwartet ---\n{erwartet}")
    check("Ohne Hinweis taucht die Hervorhebungs-Ueberschrift nirgends auf",
          ef.HEADER_TYP_A not in ohne)

    check("Leere Agenten-Antwort erzeugt gar keinen Abschnitt",
          ef.formatiere_typ_a("", "KI-EINORDNUNG DES TAGES") == "")

    nur_hinweis = ef.formatiere_typ_a(QUARTALS_EMPFEHLUNG, "KI-EMPFEHLUNG", breite=60,
                                       alles_ist_hinweis=True)
    check("alles_ist_hinweis=True hebt den kompletten Text hervor",
          ef.HEADER_TYP_A in nur_hinweis and "Overfitting" in nur_hinweis)
    check("alles_ist_hinweis=True erzeugt keinen zweiten, leeren Abschnitt",
          "KI-EMPFEHLUNG" not in nur_hinweis)

    check("Keine Markdown-Fettung in der Hervorhebung (Legacy-Markdown-Fix)",
          "*" not in block and "*" not in nur_hinweis)


def teste_typ_b():
    print("\n3) Typ B - konkreter Parameter-Vorschlag")

    details = "  {'deviation_pct': 3.0, 'stop_loss_pct': 2.5}\n\nWalk-Forward: 41 Trades"
    block = ef.formatiere_typ_b(details, breite=60)

    check("Ueberschrift kennzeichnet den Vorschlag als unvalidiert",
          ef.HEADER_TYP_B in block and "UNVALIDIERT" in ef.HEADER_TYP_B)

    pflichtsaetze = [
        "Dieser Vorschlag wurde NICHT durch Walk-Forward-Validierung geprüft.",
        "Keine automatische Umsetzung.",
        "Erst nach manueller In-Sample/Out-of-Sample-Prüfung überhaupt in Erwägung ziehen.",
    ]
    einzeilig = " ".join(block.split())
    for satz in pflichtsaetze:
        check(f"Pflichthinweis woertlich enthalten: {satz[:45]}...",
              " ".join(satz.split()) in einzeilig)

    check("Pflichthinweis steht VOR den Zahlen",
          block.index("Walk-Forward-Validierung") < block.index("deviation_pct"))
    check("Vorschlags-Details bleiben vollstaendig erhalten", "41 Trades" in block)
    check("pflichtblock_typ_b() ist Praefix des fertigen Blocks",
          block.startswith(ef.pflichtblock_typ_b(60)))
    check("Pflichtblock ist kurz genug, um immer in eine Nachricht zu passen",
          len(ef.pflichtblock_typ_b(60)) < notify.MAX_MESSAGE_LENGTH,
          f"{len(ef.pflichtblock_typ_b(60))} Zeichen")


def teste_chunking():
    print("\n4) Chunking - der Pflichthinweis darf nicht zerrissen werden")

    pflicht = ef.pflichtblock_typ_b(60)
    max_len = 400
    kopfzeile = ef.HEADER_TYP_B
    warnzeile = "Dieser Vorschlag wurde NICHT durch Walk-Forward-Validierung geprüft."

    def zerrissen(chunks):
        """True, wenn Ueberschrift und Pflichthinweis in verschiedenen
        Nachrichten stehen."""
        return any((kopfzeile in c) != (warnzeile in c) for c in chunks)

    # Der Fuelltext wird so lange verlaengert, bis die Chunk-Grenze OHNE
    # Schutz tatsaechlich mitten in den Pflichtblock faellt - sonst wuerde
    # der Test gruen sein, ohne den kritischen Fall ueberhaupt zu treffen.
    text = None
    for anzahl in range(1, 80):
        fueller = "\n".join(f"Zeile {i} mit etwas Fuelltext fuer die Laenge."
                             for i in range(anzahl))
        kandidat = fueller + "\n" + pflicht + "\n  {'deviation_pct': 3.0}\n" + fueller
        if zerrissen(notify._split_into_chunks(kandidat, max_length=max_len)):
            text = kandidat
            break

    check("Testaufbau trifft: ohne Schutz wuerde der Block auseinandergerissen",
          text is not None)
    ohne_schutz = notify._split_into_chunks(text, max_length=max_len)

    mit_schutz = notify._split_into_chunks(text, max_length=max_len,
                                            unteilbare_bloecke=[pflicht])
    check("Mit Schutz stehen Ueberschrift und Pflichthinweis in derselben Nachricht",
          not zerrissen(mit_schutz), f"{len(mit_schutz)} Chunks")
    check("Der Text geht beim Schutz nicht verloren",
          "\n".join(mit_schutz) == text)

    # Rueckwaertskompatibilitaet: ohne das neue Argument exakt das alte Verhalten.
    def altes_verfahren(t, max_length):
        chunks, current = [], []
        for line in t.split("\n"):
            candidate = "\n".join(current + [line])
            if current and len(candidate) > max_length:
                chunks.append("\n".join(current))
                current = [line]
            else:
                current.append(line)
        if current:
            chunks.append("\n".join(current))
        return chunks

    check("Ohne unteilbare_bloecke identisch zum bisherigen Chunking",
          notify._split_into_chunks(text, max_length=max_len) == altes_verfahren(text, max_len))


def teste_prompts():
    print("\n5) Prompts der Typ-A-Agenten")

    import daily_interpreter
    import portfolio_interpreter_agent
    import quarterly_interpreter

    for name, modul in (("daily_interpreter", daily_interpreter),
                        ("portfolio_interpreter_agent", portfolio_interpreter_agent)):
        check(f"{name}: Marker-Zeile steht im System-Prompt",
              ef.MARKER_HINWEIS in modul.SYSTEM_PROMPT)
        check(f"{name}: Prompt verlangt das Weglassen ohne Hinweis",
              "ERSATZLOS WEG" in modul.SYSTEM_PROMPT)

    check("quarterly_interpreter nutzt bewusst KEINEN Marker (ganze Antwort ist "
          "die Empfehlung)", ef.MARKER_HINWEIS not in quarterly_interpreter.SYSTEM_PROMPT)
    check("quarterly_interpreter verlangt verstaendliche Sprache",
          "Erklaere jeden Fachbegriff" in quarterly_interpreter.SYSTEM_PROMPT)


def teste_tagesberichte_einheitlich():
    print("\n6) Alle neun Tagesberichte nutzen dieselbe Hervorhebung")

    import glob
    dateien = sorted(glob.glob(os.path.join(REPO_ROOT, "strategies", "*", "daily_summary_email.py")))
    check("Neun Tagesbericht-Skripte gefunden", len(dateien) == 9, f"{len(dateien)} gefunden")
    for pfad in dateien:
        quelle = open(pfad).read()
        bot = os.path.basename(os.path.dirname(pfad))
        check(f"{bot}: ruft formatiere_typ_a auf",
              'formatiere_typ_a(interpretation, "KI-EINORDNUNG DES TAGES")' in quelle)
        check(f"{bot}: alte, unformatierte Einbettung entfernt",
              "KI-EINORDNUNG DES TAGES\\n{'=' * 50}\\n{interpretation}" not in quelle)


def teste_ende_zu_ende():
    print("\n7) End-to-End mit den echten Versand-Skripten")

    sys.path.insert(0, os.path.join(REPO_ROOT, "strategies", "elliott_wave"))
    import quarterly_review as qr
    import weekly_portfolio_email as wpe

    wf = {"in_sample": {"num_trades": 60, "win_rate": 41.0, "avg_return_pct": 1.2,
                        "robustness_score": 0.9},
          "out_of_sample": {"num_trades": 31, "win_rate": 38.7, "avg_return_pct": 0.8,
                             "robustness_score": 0.4}}
    real = {"num_trades": 0}

    # a) Quartals-Review MIT Vorschlag und MIT Empfehlung
    bericht = qr.build_report(wf, {"deviation_pct": 3.0, "stop_loss_pct": 2.5,
                                    "take_profit_fib": 0.382}, wf, real, QUARTALS_EMPFEHLUNG)
    check("Quartals-Review: Typ-B-Ueberschrift im Bericht", ef.HEADER_TYP_B in bericht)
    check("Quartals-Review: Pflichthinweis im Bericht",
          "Dieser Vorschlag wurde NICHT durch Walk-Forward-Validierung geprüft." in bericht)
    check("Quartals-Review: Typ-A-Ueberschrift im Bericht", ef.HEADER_TYP_A in bericht)
    check("Quartals-Review: Bestehender Schlusshinweis unveraendert",
          "WICHTIG: Es wurde NICHTS automatisch geaendert." in bericht)

    # b) Versandweg: der Pflichtblock landet in einer einzigen Nachricht
    verschickt = []
    original_send_alert = notify.send_alert
    notify.send_alert = lambda text, parse_mode="Markdown": (verschickt.append(text) or True)
    try:
        ok = notify.send_report("Quartals-Review [elliott_wave] - Parameter-Vorschlag",
                                 bericht, unteilbare_bloecke=[ef.pflichtblock_typ_b(60)])
    finally:
        notify.send_alert = original_send_alert
    check("Versand meldet Erfolg (mit abgefangenem send_alert)", ok)
    treffer = [c for c in verschickt if ef.HEADER_TYP_B in c]
    check("Ueberschrift des Vorschlags in genau einer Nachricht", len(treffer) == 1,
          f"{len(verschickt)} Nachricht(en)")
    check("Pflichthinweis steht in derselben Nachricht wie die Ueberschrift",
          "Walk-Forward-Validierung geprüft" in treffer[0])

    # c) Quartals-Review OHNE Vorschlag und OHNE Empfehlung
    leer = qr.build_report(wf, None, None, real, "")
    check("Ohne Vorschlag kein Typ-B-Block", ef.HEADER_TYP_B not in leer)
    check("Ohne Empfehlung kein Typ-A-Block", ef.HEADER_TYP_A not in leer)
    check("Ohne Vorschlag bleibt der bisherige Hinweis stehen",
          "AGENT-VORSCHLAG: nicht verfuegbar" in leer)

    # d) Wochenbericht mit und ohne Hinweis
    uebersicht = "PORTFOLIO-UEBERSICHT\nBot A: +2.1%\nBot B: -0.4%"
    mit = wpe.build_email_body(uebersicht, PORTFOLIO_MIT_HINWEIS)
    check("Wochenbericht: Hervorhebungs-Block vorhanden", ef.HEADER_TYP_A in mit)
    check("Wochenbericht: Hinweis steht vor der Einordnung",
          mit.index(ef.HEADER_TYP_A) < mit.index("KI-EINORDNUNG DER WOCHE"))
    check("Wochenbericht: Teil A des Agenten bleibt erhalten",
          "WAS DAS FUER DICH BEDEUTET" in mit)
    check("Wochenbericht: Rohdaten bleiben vollstaendig", "Bot B: -0.4%" in mit)

    ohne_hinweis = PORTFOLIO_MIT_HINWEIS.split("[HINWEIS]")[0].strip()
    ohne = wpe.build_email_body(uebersicht, ohne_hinweis)
    check("Wochenbericht ohne Hinweis: kein Hervorhebungs-Block",
          ef.HEADER_TYP_A not in ohne)
    check("Wochenbericht ohne Hinweis: Einordnung trotzdem enthalten",
          "KI-EINORDNUNG DER WOCHE" in ohne and "nichts zu tun" in ohne)

    return bericht, mit


def main():
    print("Selbsttests der Empfehlungs-Hervorhebung")
    teste_erkennung()
    teste_typ_a()
    teste_typ_b()
    teste_chunking()
    teste_prompts()
    teste_tagesberichte_einheitlich()
    teste_ende_zu_ende()
    print(f"\n{len(CHECKS)}/{len(CHECKS)} Pruefungen bestanden.")


if __name__ == "__main__":
    main()
