"""
Agent 1: Taegliche Interpretation
======================================
Nimmt die statistische Tages-Zusammenfassung (wie sie bisher in die
E-Mail ging) und laesst Claude eine kurze, verstaendliche Einordnung
schreiben - z.B. "Die heutige Trefferquote liegt im Rahmen des
historischen Durchschnitts" oder "Auffaellig: zwei Trades in Folge
wurden per Stop-Loss beendet, das kommt bei dieser Strategie selten vor".

Faellt bei fehlendem API-Key oder Fehlern lautlos auf eine leere
Antwort zurueck - der Rest der E-Mail funktioniert dann trotzdem wie
gewohnt (nur ohne die Zusatz-Einordnung).
"""

from claude_client import call_claude, MODEL_HAIKU

SYSTEM_PROMPT = """Du bist ein nuechterner, sachlicher Trading-Analyst.
Du bekommst die statistische Tages-Zusammenfassung eines automatisierten
Trading-Bots (Backtests bereits validiert, laeuft aktuell im Papier-Trading-
Modus). Deine Aufgabe: 2-4 Saetze knappe, sachliche Einordnung.

WICHTIG:
- Keine Uebertreibung, keine Empfehlungen ("jetzt kaufen" o.ae.)
- Wenn nichts Auffaelliges passiert ist, sag das auch einfach so
  ("Ruhiger Tag, keine besonderen Auffaelligkeiten")
- Bei ungewoehnlichen Mustern (z.B. mehrere Verluste in Folge,
  ungewoehnlich hohe/niedrige Aktivitaet) das benennen, aber nicht
  dramatisieren
- Keine Finanzberatung, keine Prognosen fuer die Zukunft
- Antworte NUR mit dem Fliesstext, keine Ueberschriften, kein Markdown
"""


def generate_interpretation(strategy_name: str, summary_text: str) -> str:
    """
    Gibt einen kurzen Interpretations-Text zurueck, oder einen leeren
    String, falls die Anfrage fehlschlaegt (z.B. kein API-Key gesetzt).
    """
    user_message = f"Strategie: {strategy_name}\n\nTages-Zusammenfassung:\n{summary_text}"

    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=300, model=MODEL_HAIKU)

    if not result["success"]:
        return ""

    return result["text"].strip()
