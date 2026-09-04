"""
Agent 3: Marktkontext via Web-Suche
========================================
Nutzt Claudes eingebaute Web-Suche (server-seitig, ueber die Anthropic-
API), um kurz zusammenzufassen, ob es aktuell relevante Nachrichten oder
Marktereignisse fuer die beobachteten Symbole gibt - Information, die aus
reinen historischen Kursdaten nicht ablesbar ist.

WICHTIG - bewusste Design-Entscheidung:
Dieser Agent liefert AUSSCHLIESSLICH informativen Kontext fuer die
taegliche E-Mail. Er trifft KEINE Trading-Entscheidung und blockiert
KEINE Signale - so ein "News-Veto" waere ein eigenstaendiges Feature,
das erst separat backgetestet und validiert werden muesste, bevor es
echten Einfluss auf Trades haben duerfte. Aktuell ist er reine
Zusatzinformation zum Lesen, mehr nicht.

Wird bewusst nur EINMAL TAEGLICH aufgerufen (nicht bei jedem
Forward-Test-Lauf), um Kosten und API-Anfragen ueberschaubar zu halten.
"""

from claude_client import call_claude

SYSTEM_PROMPT = """Du bist ein neutraler Marktbeobachter. Du bekommst eine
Liste von Symbolen (Kryptowaehrungen oder Aktien) und sollst kurz
recherchieren, ob es aktuell (letzte 24-48 Stunden) wesentliche
Nachrichten oder Ereignisse gibt, die diese Symbole betreffen.

WICHTIG:
- Nur recherchieren, wenn du Web-Suche zur Verfuegung hast
- 3-5 Saetze, sachlich, keine Uebertreibung
- Nur wirklich relevante Ereignisse nennen (z.B. Quartalszahlen,
  regulatorische Entscheidungen, grosse Kursbewegungen mit Ursache) -
  nicht jede Kleinigkeit
- Falls nichts Nennenswertes zu finden ist, sag das kurz und direkt
- KEINE Handelsempfehlung, KEINE Prognose - nur Fakten zusammenfassen
- Antworte NUR mit dem Fliesstext, keine Ueberschriften
"""

WEB_SEARCH_TOOL = {"type": "web_search_20250305", "name": "web_search"}


def get_market_context(symbols: list, context_label: str = "") -> str:
    """
    Gibt eine kurze Marktkontext-Zusammenfassung zurueck, oder einen
    leeren String bei fehlendem API-Key oder Fehlern.

    symbols: Liste der zu recherchierenden Symbole (aus Kostengruenden
             idealerweise nur die Symbole mit aktuell offenen Positionen
             oder neuen Signalen, nicht die komplette Watchlist).
    """
    if not symbols:
        return ""

    symbols_text = ", ".join(symbols[:10])  # hartes Limit, um Kosten zu begrenzen
    user_message = f"Symbole ({context_label}): {symbols_text}\n\nGibt es aktuell relevante Nachrichten?"

    # thinking bleibt hier bewusst UNGESETZT (= adaptive, der Standard bei
    # MODEL_SONNET/claude-sonnet-5) statt wie bei den anderen drei Agenten
    # explizit deaktiviert zu werden: dieser Agent nutzt echtes Tool-Use
    # (Web-Suche), wo Thinking dem Modell hilft, Suchanfragen zu planen und
    # Ergebnisse einzuordnen. Stattdessen wird das max_tokens-Budget
    # grosszuegig genug gesetzt, um Thinking + Suchergebnis-Bloecke + die
    # finale 3-5-Satz-Antwort gemeinsam abzudecken - die alten 400 Tokens
    # waren dafuer im Zweifel zu knapp (siehe portfolio_interpreter_agent.py:
    # dort hat ein zu knappes Budget dazu gefuehrt, dass Thinking allein
    # schon das gesamte Budget verbraucht hat, BEVOR sichtbarer Text
    # entstand - das Risiko besteht hier grundsaetzlich genauso).
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=2000, tools=[WEB_SEARCH_TOOL])

    if not result["success"]:
        return ""

    if result.get("stop_reason") == "max_tokens":
        raw = result.get("raw")
        block_types = ([getattr(b, "type", "?") for b in raw.content] if raw is not None
                        else "unbekannt (kein raw-Objekt)")
        print(f"  Warnung: Antwort von Agent 3 (Marktkontext) wurde bei max_tokens "
              f"abgeschnitten ({len(result['text'])} Zeichen sichtbarer Text, "
              f"Content-Block-Typen: {block_types}) - verwerfe die unvollstaendige Antwort. "
              f"Bei wiederholtem Auftreten max_tokens in get_market_context() weiter erhoehen "
              f"(Thinking hier bewusst NICHT deaktivieren, siehe Kommentar oben).")
        return ""

    return result["text"].strip()
