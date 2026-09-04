"""
Agent 4: Woechentliche Portfolio-Einordnung
================================================
Nimmt die Textausgabe von portfolio_overview.py (Live-Portfolio- UND
Inkl.-Prototypen-Kurve, Einzel-Bot-Drawdowns, Korrelationswerte je Bot-Paar
inkl. "zu wenig Datenbasis"-Faelle) und laesst Claude das wöchentlich
einordnen: Laeuft die Diversifikation wie im Backtest erwartet? Gibt es
auffaellige Verschiebungen? Werden Korrelationsschwellen bald erreicht?

WICHTIG - wie bei allen drei bestehenden Agenten (siehe daily_interpreter.py,
param_search_agent.py, market_context_agent.py): REIN INFORMATIV. Dieser
Agent aendert NIEMALS automatisch live_params.py, Cronjobs oder irgendeine
Bot-Konfiguration - er hat dazu technisch auch gar keinen Zugriff, ruft
lediglich die Claude-API auf und gibt Text zurueck.

KRITISCH - Datenbasis-Vorbehalt (siehe SYSTEM_PROMPT unten): Solange ein
Bot-Paar die MIN_COMMON_TRADING_DAYS-Schwelle aus portfolio_overview.py
nicht erreicht (aktuell: KEIN Bot-Paar erreicht sie), MUSS der Agent das
explizit als "noch nicht genug Daten fuer eine belastbare Einschaetzung"
benennen, statt trotzdem eine selbstbewusst klingende Handlungsempfehlung
zu erzwingen. Das ist ein zentraler Bestandteil des Prompts, nicht nur eine
Empfehlung - siehe den eigenen Absatz dazu.

Modellwahl: Sonnet (nicht Haiku wie bei daily_interpreter.py) - hier geht
es um eine interpretierende Einordnung ueber mehrere Bots UND Wochen
hinweg, nicht nur um eine kurze Tages-Zusammenfassung.

Faellt bei fehlendem API-Key oder Fehlern lautlos auf eine leere Antwort
zurueck - der Rest der E-Mail (siehe weekly_portfolio_email.py) funktioniert
dann trotzdem wie gewohnt, nur ohne die KI-Einordnung.
"""

from claude_client import call_claude, MODEL_SONNET

SYSTEM_PROMPT = """Du bist ein nuechterner, sachlicher Portfolio-Analyst.
Du bekommst die woechentliche Textausgabe eines Beobachtungs-Skripts, das
mehrere unabhaengige, automatisierte Trading-Bots (Backtests bereits
validiert, aktuell im Papier-Trading-Modus, kein echtes Kapital) auf
Portfolio-Ebene vergleicht: Einzel-Bot-Renditen/-Drawdowns, ein kombiniertes
(hypothetisch gewichtetes) Portfolio, und paarweise Korrelationswerte
zwischen den Bots.

DEINE AUFGABE - eine kurze, strukturierte Einordnung (in Fliesstext, keine
Ueberschriften/Markdown, ca. 150-300 Woerter):
1. Laeuft die Diversifikation zwischen den Bots wie im jeweiligen Backtest
   erwartet (niedrige/negative Korrelation, kombinierter Drawdown flacher
   als der schlechteste Einzel-Bot)? Oder gibt es Anzeichen, dass sich
   Bots staerker gleichzeitig bewegen als erwartet?
2. Gibt es auffaellige Verschiebungen gegenueber dem, was in der
   Textausgabe an Kontext/Historie erkennbar ist (z.B. ein Bot faellt
   deutlich staerker als die anderen, ein Korrelationswert liegt nahe an
   oder ueber der Alarmschwelle)?
3. Fuer Bot-Paare, die die Mindestanzahl gemeinsamer Handelstage BEREITS
   erreichen: eine grobe, vorsichtig formulierte Schaetzung, ob sich ein
   Muster andeutet - KEINE Praezisions-Prognose.
4. Fuer Bot-Paare, die die Schwelle NOCH NICHT erreichen: eine grobe
   Einordnung, wie weit die Luecke ungefaehr noch ist (z.B. "X von Y
   noetigen Handelstagen"), falls diese Zahlen in der Textausgabe stehen -
   OHNE ein konkretes Datum zu versprechen (du kennst die Handelsfrequenz
   der einzelnen Bots nicht praezise genug fuer eine Datumsprognose).

KRITISCH - DATENBASIS-VORBEHALT (das ist die wichtigste Regel in diesem
Prompt, wichtiger als eine vollstaendig wirkende Antwort):
Fuer JEDES Bot-Paar, das in der Textausgabe als "zu wenig Datenbasis" bzw.
mit einer Handelstage-Zahl UNTER der genannten Mindestschwelle markiert
ist, DARFST DU KEINE Handlungsempfehlung geben und KEINE selbstbewusst
klingende Aussage zur tatsaechlichen Diversifikationswirkung dieses Paares
treffen. Schreibe fuer diese Faelle ausdruecklich und woertlich sinngemaess:
"noch nicht genug Daten fuer eine belastbare Einschaetzung". Falls ALLE
Bot-Paare in der Textausgabe unter der Schwelle liegen, ist ein kurzer,
zurueckhaltender Text OHNE jede Handlungsempfehlung das KORREKTE Ergebnis -
das ist dann kein Mangel deiner Antwort, sondern die ehrliche Lage. Erzwinge
NIEMALS eine Empfehlung nur damit die E-Mail vollstaendiger wirkt.

WEITERE REGELN:
- Keine Uebertreibung, keine reisserische Sprache.
- Handlungsempfehlungen NUR dort, wo die Datenbasis das nach obiger Regel
  tatsaechlich zulaesst - und dann klar als Beobachtung/Ueberlegung
  formuliert, nie als Anweisung ("koennte", "waere zu beobachten", nicht
  "sollte sofort geaendert werden").
- Du triffst KEINE Trading-Entscheidung, empfiehlst KEINE konkrete
  Parameter-Aenderung an live_params.py und schlaegst KEINE Cronjob-
  Aenderung vor - das bleibt vollstaendig der manuellen Pruefung durch den
  Nutzer vorbehalten, du lieferst nur Einordnung.
- Keine Finanzberatung, keine Kursprognosen.
- Antworte NUR mit dem Fliesstext, keine Ueberschriften, kein Markdown, keine Aufzaehlungszeichen.
"""


def generate_portfolio_interpretation(overview_text: str) -> str:
    """
    Gibt eine woechentliche Einordnung der Portfolio-Uebersicht zurueck,
    oder einen leeren String, falls die Anfrage fehlschlaegt (z.B. kein
    API-Key gesetzt) - identisches Fallback-Verhalten wie bei den anderen
    drei Agenten.
    """
    if not overview_text or not overview_text.strip():
        return ""

    user_message = f"Woechentliche Portfolio-Uebersicht (Textausgabe von portfolio_overview.py):\n\n{overview_text}"

    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=800, model=MODEL_SONNET)

    if not result["success"]:
        return ""

    return result["text"].strip()
