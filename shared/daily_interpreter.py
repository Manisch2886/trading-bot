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
from empfehlung_format import PROMPT_BAUSTEIN_HINWEIS

# Der Hinweis-Baustein wird NICHT hier abgetippt, sondern aus
# empfehlung_format importiert: dort steht auch die Erkennungs-Logik
# (teile_hinweis()), die genau diese Marker-Zeile wieder herausschneidet -
# zwei getrennte Textstellen wuerden frueher oder spaeter auseinanderlaufen.
SYSTEM_PROMPT = """Du bist ein nuechterner, sachlicher Trading-Analyst.
Du bekommst die statistische Tages-Zusammenfassung eines automatisierten
Trading-Bots (Backtests bereits validiert, laeuft aktuell im Papier-Trading-
Modus). Deine Aufgabe: 2-4 Saetze knappe, sachliche Einordnung.

WICHTIG:
- Keine Uebertreibung, keine Kauf-/Verkaufsempfehlungen ("jetzt kaufen"
  o.ae.) - der optionale Hinweis-Abschnitt unten ist ausdruecklich KEINE
  solche Empfehlung, sondern eine Beobachtung zum Bot-Verhalten
- Wenn nichts Auffaelliges passiert ist, sag das auch einfach so
  ("Ruhiger Tag, keine besonderen Auffaelligkeiten")
- Bei ungewoehnlichen Mustern (z.B. mehrere Verluste in Folge,
  ungewoehnlich hohe/niedrige Aktivitaet) das benennen, aber nicht
  dramatisieren
- Keine Finanzberatung, keine Prognosen fuer die Zukunft
- Antworte NUR mit dem Fliesstext, keine Ueberschriften, kein Markdown -
  einzige Ausnahme ist die unten beschriebene Marker-Zeile

""" + PROMPT_BAUSTEIN_HINWEIS


def generate_interpretation(strategy_name: str, summary_text: str) -> str:
    """
    Gibt einen kurzen Interpretations-Text zurueck, oder einen leeren
    String, falls die Anfrage fehlschlaegt (z.B. kein API-Key gesetzt).
    """
    user_message = f"Strategie: {strategy_name}\n\nTages-Zusammenfassung:\n{summary_text}"

    # max_tokens von 300 auf 500 angehoben: der Prompt kann jetzt zusaetzlich
    # zu den 2-4 Saetzen Einordnung noch 1-3 Saetze Hinweis-Abschnitt
    # verlangen (siehe PROMPT_BAUSTEIN_HINWEIS). 300 waeren dafuer knapp -
    # und ein mitten im Satz abgeschnittener Hinweis waere genau in dem
    # Abschnitt, der jetzt hervorgehoben wird, besonders unschoen.
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=500, model=MODEL_HAIKU)

    if not result["success"]:
        return ""

    return result["text"].strip()
