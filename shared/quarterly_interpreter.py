"""
Quartals-Empfehlungs-Agent
===============================
Nimmt den Walk-Forward-Vergleich (aktuelle vs. vorgeschlagene Parameter)
sowie die echten Forward-Test-Ergebnisse und schreibt daraus eine klare,
begruendete Empfehlung - nicht nur eine Wiederholung der Zahlen.

Zentrale Regel, die dem Modell explizit mitgegeben wird: Out-of-Sample-
Ergebnisse zaehlen deutlich mehr als In-Sample-Ergebnisse. Sieht der
Vorschlag In-Sample gut aus, faellt aber Out-of-Sample ab, ist das ein
Overfitting-Warnsignal und sollte auch so benannt werden - genau das
Muster, das in der Praxis mehrfach in diesem Projekt aufgetreten ist.
"""

from claude_client import call_claude

SYSTEM_PROMPT = """Du bist ein erfahrener, kritischer quantitativer Analyst,
der entscheiden hilft, ob eine neu vorgeschlagene Parameter-Kombination
fuer eine Trading-Strategie die aktuell laufende Kombination ersetzen sollte.

Du bekommst:
1. Die aktuellen Live-Parameter mit ihren Walk-Forward-Ergebnissen
   (In-Sample UND Out-of-Sample)
2. Die vorgeschlagenen neuen Parameter mit denselben Kennzahlen
3. Die echten, bereits aufgelaufenen Forward-Test-Ergebnisse (falls vorhanden)

WICHTIGE BEWERTUNGSREGELN:
- Out-of-Sample-Ergebnisse sind das, was zaehlt - In-Sample-Ergebnisse
  sind fast immer optimistisch verzerrt. Ein Vorschlag, der In-Sample
  gut aussieht, aber Out-of-Sample schlechter abschneidet als die
  aktuelle Kombination, ist ein klassisches Overfitting-Warnsignal -
  benenne das explizit und empfiehl in diesem Fall, NICHT zu wechseln.
- Beruecksichtige auch die Stichprobengroesse (Anzahl Trades) - eine
  kleinere Stichprobe verdient weniger Vertrauen.
- Falls echte Forward-Test-Daten vorhanden sind, gewichte diese am
  hoechsten - sie koennen nicht ueberoptimiert sein.
- Bei zu wenigen Trades (egal wo) explizit sagen, dass die Datenbasis
  noch zu duenn fuer eine verlaessliche Entscheidung ist.

STRUKTUR DEINER ANTWORT (4-6 Saetze, sachlich, kein Marketing-Ton):
1. Eine klare Kernaussage: "Empfehlung: Parameter beibehalten" ODER
   "Empfehlung: Wechsel in Erwaegung ziehen" ODER "Zu wenig Daten fuer
   eine Entscheidung"
2. Kurze Begruendung anhand der Out-of-Sample-Zahlen
3. Falls relevant: Hinweis auf ein Overfitting-Muster oder zu kleine
   Stichprobe

Antworte NUR mit dem Fliesstext, keine Ueberschriften, kein Markdown.
Das ist KEINE Finanzberatung, sondern eine statistische Einordnung -
formuliere entsprechend vorsichtig, ohne False es zu weich zu machen.
"""


def generate_recommendation(strategy_name: str, current_params: dict, current_wf: dict,
                             proposed_params: dict, proposed_wf: dict, real_stats: dict) -> str:
    """
    Gibt eine kurze, begruendete Empfehlung zurueck, oder einen leeren
    String, falls die Anfrage fehlschlaegt (z.B. kein API-Key gesetzt).
    """
    if proposed_params is None:
        return ""  # kein Vorschlag vorhanden, keine Empfehlung noetig

    user_message = f"""Strategie: {strategy_name}

AKTUELLE PARAMETER: {current_params}
Walk-Forward In-Sample: {current_wf.get('in_sample')}
Walk-Forward Out-of-Sample: {current_wf.get('out_of_sample')}

VORGESCHLAGENE PARAMETER: {proposed_params}
Walk-Forward In-Sample: {proposed_wf.get('in_sample')}
Walk-Forward Out-of-Sample: {proposed_wf.get('out_of_sample')}

ECHTE FORWARD-TEST-ERGEBNISSE (aktuelle Parameter, seit Start): {real_stats}

Gib deine Empfehlung."""

    # thinking bewusst deaktiviert: reine Textsynthese ohne Tool-Use.
    # MODEL_SONNET (claude-sonnet-5, Standardmodell von call_claude()) faehrt
    # sonst automatisch "adaptive" Extended Thinking, deren Tokens sich das
    # max_tokens-Budget mit der sichtbaren Antwort teilen - bei knappem Limit
    # kann das Modell dadurch das komplette Budget "wegdenken", bevor
    # ueberhaupt Antworttext entsteht (siehe portfolio_interpreter_agent.py,
    # wo genau dieser Fall live auftrat).
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=500,
                          thinking={"type": "disabled"})

    if not result["success"]:
        return ""

    if result.get("stop_reason") == "max_tokens":
        raw = result.get("raw")
        block_types = ([getattr(b, "type", "?") for b in raw.content] if raw is not None
                        else "unbekannt (kein raw-Objekt)")
        print(f"  Warnung: Antwort des Quartals-Empfehlungs-Agenten wurde bei max_tokens "
              f"abgeschnitten ({len(result['text'])} Zeichen sichtbarer Text, "
              f"Content-Block-Typen: {block_types}) - verwerfe die unvollstaendige Antwort "
              f"statt eine mitten im Satz abbrechende oder leere Empfehlung zurueckzugeben.")
        return ""

    return result["text"].strip()
