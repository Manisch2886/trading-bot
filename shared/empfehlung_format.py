"""
Hervorhebung von Handlungsempfehlungen in den Telegram-Berichten
=====================================================================
Alle bot-eigenen Berichte laufen seit PR #16 ueber Telegram. Mehrere
Agenten erzeugen darin Freitext, der de facto Handlungsempfehlungen
enthaelt ("eine Ueberpruefung der Parametrisierung sollte in Betracht
gezogen werden") - bisher stand das undifferenziert im Fliesstext, also
genau dort, wo es ueberlesen wird.

Dieses Modul ist die EINZIGE Stelle, an der die Hervorhebung definiert
wird; alle 13 Versandstellen bauen ihre Bloecke ueber die Funktionen hier.
Zwei bewusst unterschiedlich behandelte Arten:

TYP A - Interpretations-Hinweis (daily_interpreter, portfolio_interpreter_
agent, quarterly_interpreter): der Agent ordnet die Lage ein. Das ist eine
BEOBACHTUNG, keine getestete Empfehlung - der Vorspann unter der
Ueberschrift sagt das woertlich, damit der Unterschied nicht an der
Formulierungslaune des Modells haengt.

TYP B - konkreter Parameter-Vorschlag (param_search_agent): hier stehen
tatsaechlich neue Zahlenwerte. Der Unvalidiert-Hinweis dazu wird NICHT vom
Agenten erzeugt, sondern hier fest verdrahtet - ein Modell koennte ihn
variieren, abschwaechen oder vergessen, ein Konstanten-String nicht.
Zusaetzlich wird PFLICHTBLOCK_TYP_B ueber notify.send_report(...,
unteilbare_bloecke=...) gegen das Zeilen-Chunking geschuetzt, damit die
Ueberschrift nicht in Nachricht 1 und der Pflichthinweis in Nachricht 2
landet.

FORMATIERUNG: Emoji + Grossbuchstaben-Header, KEIN Markdown-Fett. Grund
ist der in notify.send_report() dokumentierte Live-Bug: Telegrams
Legacy-Markdown kennt kein Backslash-Escaping, weshalb send_report()
bewusst komplett ohne parse_mode verschickt. Fettung ist damit gar nicht
verfuegbar - und wird hier auch nicht ueber Umwege versucht.
"""

# Marker-Zeile, die die Typ-A-Agenten ans ENDE ihrer Antwort haengen, falls
# sie einen Hinweis haben. Wird per PROMPT_BAUSTEIN_HINWEIS in die
# System-Prompts eingesetzt (nicht dort abgetippt), damit Prompt und
# Erkennungs-Logik nicht auseinanderlaufen koennen.
MARKER_HINWEIS = "[HINWEIS]"

PROMPT_BAUSTEIN_HINWEIS = f"""ABSCHLIESSENDER HINWEIS-ABSCHNITT (optional):
Falls sich aus deiner Einordnung etwas ergibt, das der Nutzer sich ansehen
sollte, haenge GANZ AM ENDE deiner Antwort eine Zeile an, die exakt und nur
"{MARKER_HINWEIS}" enthaelt, und darunter 1-3 Saetze dazu. Diese Saetze
muessen fuer jemanden verstaendlich sein, der sich nicht taeglich mit dem
Projekt beschaeftigt: sag konkret, WAS gemeint ist und WARUM - keine
Fachbegriffe ohne kurze Erklaerung. Formuliere als Beobachtung
("waere zu beobachten", "koennte"), nie als Anweisung.
Falls es nichts dergleichen gibt - bei ruhigem Verlauf der Normalfall -,
lass die Marker-Zeile ERSATZLOS WEG. Schreibe die Marker-Zeile niemals
ohne nachfolgenden Text und erzwinge nie einen Hinweis, nur damit der
Bericht vollstaendiger wirkt."""

# --- Typ A ----------------------------------------------------------------
HEADER_TYP_A = "🎯 EINORDNUNG & HINWEIS"

VORSPANN_TYP_A = (
    "Beobachtung des Auswertungs-Agenten - KEINE geprüfte Handlungsanweisung.\n"
    "Es wurde nichts automatisch geändert; jede Änderung bleibt manuell."
)

# --- Typ B ----------------------------------------------------------------
HEADER_TYP_B = "⚠️ PARAMETER-VORSCHLAG (UNVALIDIERT)"

# Wortlaut aus der Aufgabenstellung, bewusst unveraendert uebernommen.
UNVALIDIERT_HINWEIS = (
    "Dieser Vorschlag wurde NICHT durch Walk-Forward-Validierung geprüft.\n"
    "Keine automatische Umsetzung. Erst nach manueller "
    "In-Sample/Out-of-Sample-Prüfung überhaupt in Erwägung ziehen."
)

# Ueberschrift + Pflichthinweis als ein Stueck: pflichtblock_typ_b() gibt
# genau diesen Teil zurueck, er wird an
# notify.send_report(unteilbare_bloecke=[...]) uebergeben. Bewusst NUR
# dieser kurze, laengenbegrenzte Teil und nicht der ganze Vorschlagsblock -
# ein Block, der fuer sich allein schon laenger als eine Telegram-Nachricht
# ist, liesse sich gar nicht zusammenhalten. Ueberschrift und Pflichthinweis
# zusammen sind unter 300 Zeichen und passen immer.
_PFLICHTTEXT_TYP_B = f"{HEADER_TYP_B}\n{UNVALIDIERT_HINWEIS}"


def _trenner(breite: int) -> str:
    return "=" * breite


def teile_hinweis(text: str) -> tuple:
    """Trennt einen Agenten-Text an der Marker-Zeile in (Analyse, Hinweis).

    Erkennt die Marker-Zeile tolerant (Gross-/Kleinschreibung, umgebende
    Leerzeichen, angehaengter Doppelpunkt, Text direkt hinter dem Marker in
    derselben Zeile) - ein Modell haelt sich nie zu 100 Prozent an ein
    Format, und ein knapp verfehlter Marker soll nicht dazu fuehren, dass
    der Hinweis unhervorgehoben im Fliesstext landet.

    Steht kein Marker im Text oder folgt ihm nichts Substanzielles, ist der
    Hinweis leer - dann darf und wird KEIN Hervorhebungsblock entstehen.
    """
    if not text:
        return "", ""

    zeilen = text.split("\n")
    marker_ohne_klammern = MARKER_HINWEIS.strip("[]").upper()

    for i, zeile in enumerate(zeilen):
        kern = zeile.strip().rstrip(":").strip()
        kern_ohne_klammern = kern.strip("[]").upper()

        if kern_ohne_klammern == marker_ohne_klammern:
            rest_der_zeile = ""
        elif kern.upper().startswith(MARKER_HINWEIS.upper()):
            # Modell hat den Hinweis in dieselbe Zeile geschrieben.
            rest_der_zeile = kern[len(MARKER_HINWEIS):].lstrip(": ").strip()
        else:
            continue

        analyse = "\n".join(zeilen[:i]).strip()
        hinweis_zeilen = ([rest_der_zeile] if rest_der_zeile else []) + zeilen[i + 1:]
        hinweis = "\n".join(hinweis_zeilen).strip()
        if not hinweis:
            # Marker ohne Inhalt: so tun, als waere er nie dagewesen -
            # lieber kein Block als ein leerer Block.
            return text.strip(), ""
        return analyse, hinweis

    return text.strip(), ""


def formatiere_typ_a(text: str, analyse_ueberschrift: str, breite: int = 50,
                      alles_ist_hinweis: bool = False) -> str:
    """Baut den fertigen Berichts-Abschnitt fuer einen Typ-A-Agenten.

    text:                 Rohantwort des Agenten (leer -> leerer Rueckgabewert)
    analyse_ueberschrift: bisherige Ueberschrift des Abschnitts, z.B.
                          "KI-EINORDNUNG DES TAGES" - bleibt unveraendert,
                          damit die gewohnte Berichtsstruktur erhalten bleibt.
    alles_ist_hinweis:    True fuer quarterly_interpreter, dessen Antwort
                          KOMPLETT aus der Empfehlung besteht ("Empfehlung:
                          Parameter beibehalten" + Begruendung) - dort gibt
                          es keinen davon zu trennenden Analyse-Teil.

    Ohne erkannten Hinweis ist die Ausgabe exakt das bisherige Format -
    kein leerer Hervorhebungs-Block, keine sonstige Aenderung.
    """
    if not text or not text.strip():
        return ""

    if alles_ist_hinweis:
        analyse, hinweis = "", text.strip()
    else:
        analyse, hinweis = teile_hinweis(text)

    trenner = _trenner(breite)
    bloecke = []

    if hinweis:
        bloecke.append(f"{trenner}\n{HEADER_TYP_A}\n{trenner}\n"
                       f"{VORSPANN_TYP_A}\n\n{hinweis}")
    if analyse:
        bloecke.append(f"{trenner}\n{analyse_ueberschrift}\n{trenner}\n{analyse}")

    return "\n\n".join(bloecke)


def pflichtblock_typ_b(breite: int = 50) -> str:
    """Ueberschrift + Pflichthinweis als zusammenhaengender Block.

    Genau dieser String wird notify.send_report(unteilbare_bloecke=[...])
    uebergeben: das Zeilen-Chunking darf ihn nicht auseinanderreissen, sonst
    stuende die Ueberschrift "PARAMETER-VORSCHLAG" am Ende der einen und der
    Unvalidiert-Hinweis am Anfang der naechsten Telegram-Nachricht.
    """
    trenner = _trenner(breite)
    return f"{trenner}\n{_PFLICHTTEXT_TYP_B}\n{trenner}"


def formatiere_typ_b(details: str, breite: int = 50) -> str:
    """Baut den fertigen Abschnitt fuer einen konkreten Parameter-Vorschlag.

    details: die Vorschlags-Details (Parameterwerte, Walk-Forward-Zahlen),
             wie sie das aufrufende Skript ohnehin schon zusammenstellt.

    Der Pflichthinweis steht IMMER und unmittelbar unter der Ueberschrift,
    also VOR den Zahlen - wer nur den Anfang des Blocks liest, hat ihn
    trotzdem gesehen. Er stammt aus UNVALIDIERT_HINWEIS und kann vom
    Agenten weder umformuliert noch weggelassen werden.
    """
    block = pflichtblock_typ_b(breite)
    if details and details.strip():
        # Nur Leerzeilen am Rand entfernen, nicht die Einrueckung der ersten
        # Zeile: die Berichte ruecken Parameter-Zeilen bewusst um zwei
        # Leerzeichen ein.
        block += "\n" + details.strip("\n").rstrip()
    return block
