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

    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=400, tools=[WEB_SEARCH_TOOL])

    if not result["success"]:
        return ""

    return result["text"].strip()
