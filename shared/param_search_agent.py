"""
Agent 2: Intelligente Parameter-Suche
==========================================
Ersetzt das erschoepfende Grid-Search (jede Kombination durchprobieren)
durch einen iterativen Ansatz: Claude bekommt die bisherigen Testergebnisse
gezeigt und schlaegt gezielt die naechste, vielversprechendste Kombination
vor - aehnlich wie ein erfahrener Quant, der nicht stur jede Zahl testet,
sondern aus Zwischenergebnissen lernt.

Vorteil ggue. Grid-Search: bei grossen Parameterraeumen (z.B. 5+ Parameter)
waechst die Anzahl Kombinationen exponentiell - der Agent kann oft mit
deutlich weniger Testlaeufen zu einem guten Ergebnis kommen.

Nachteil: nicht erschoepfend - der Agent koennte eine gute Kombination
uebersehen, die Grid-Search gefunden haette. Fuer eine finale,
vertrauenswuerdige Validierung bleibt Grid-Search + Walk-Forward der
Goldstandard - dieser Agent eignet sich gut, um VOR einem vollen
Grid-Search schnell einen vielversprechenden Bereich einzugrenzen.
"""

import json
import pandas as pd

from claude_client import call_claude, extract_json

SYSTEM_PROMPT = """Du bist ein erfahrener quantitativer Trading-Analyst, der
eine Trading-Strategie durch iteratives Testen von Parameter-Kombinationen
optimiert.

Du bekommst:
1. Eine Beschreibung der Parameter (Name, Typ, erlaubter Bereich)
2. Eine Tabelle bereits getesteter Kombinationen mit ihren Ergebnissen

Deine Aufgabe: schlage die NAECHSTE Kombination vor, die am ehesten zu
einer robusten Verbesserung fuehrt. Beruecksichtige dabei:
- Nicht nur die hoechste Rendite - auch Trade-Anzahl (mehr = verlaesslicher)
  und Max Drawdown (kleiner = robuster)
- Wenn ein Parameter-Bereich durchgehend schlecht abschneidet, meide ihn
- Wenn sich ein Muster abzeichnet (z.B. "kleinere Stop-Loss-Werte werden
  konsistent besser"), verfeinere in diese Richtung
- Vermeide, eine bereits getestete Kombination zu wiederholen

Antworte NUR mit einem JSON-Objekt, kein zusaetzlicher Text:
{
  "action": "test" oder "stop",
  "params": {<parametername>: <wert>, ...},
  "reasoning": "kurze Begruendung, maximal 15 Woerter"
}

WICHTIG: Halte "reasoning" WIRKLICH kurz (max. 15 Woerter) - eine zu
lange Begruendung kann dazu fuehren, dass die Antwort abgeschnitten
wird und nicht mehr als gueltiges JSON gelesen werden kann.

"stop" nur waehlen, wenn du nach mehreren Iterationen ueberzeugt bist,
dass keine weitere Verbesserung mehr zu erwarten ist.
"""


def format_param_spec(param_spec: dict) -> str:
    lines = []
    for name, spec in param_spec.items():
        if "options" in spec:
            lines.append(f"- {name} ({spec['type']}): eine der Optionen {spec['options']}")
        else:
            lines.append(f"- {name} ({spec['type']}): Bereich {spec['range']}, "
                          f"Schrittweite {spec.get('step', 'beliebig')}")
    return "\n".join(lines)


def format_history(history: list) -> str:
    if not history:
        return "(noch keine Ergebnisse - das ist der erste Test)"
    df = pd.DataFrame(history)
    return df.to_string(index=False)


def run_agent_search(evaluate_fn, param_spec: dict, seed_combos: list = None,
                      max_iterations: int = 15) -> dict:
    """
    evaluate_fn: Funktion, die ein dict von Parametern annimmt und ein
                 Ergebnis-dict zurueckgibt (oder None, falls die
                 Kombination die Mindestkriterien nicht erfuellt).
    param_spec:  Beschreibung des Parameterraums (siehe format_param_spec).
    seed_combos: optionale Start-Kombinationen, die zuerst getestet werden,
                 bevor der Agent uebernimmt (z.B. sinnvolle Standardwerte).

    Rueckgabe: {"history": [...alle Ergebnisse...], "best": {...bestes Ergebnis...}}
    """
    history = []

    # Start-Kombinationen testen (falls angegeben)
    if seed_combos:
        print(f"Teste {len(seed_combos)} Start-Kombinationen...")
        for combo in seed_combos:
            result = evaluate_fn(combo)
            if result is not None:
                history.append(result)
                print(f"  {combo} -> {result.get('robustness_score', 'n/a')}")

    param_spec_text = format_param_spec(param_spec)

    for iteration in range(1, max_iterations + 1):
        print(f"\n--- Agent-Iteration {iteration}/{max_iterations} ---")

        user_message = (
            f"PARAMETER-RAUM:\n{param_spec_text}\n\n"
            f"BISHERIGE ERGEBNISSE:\n{format_history(history)}\n\n"
            f"Schlage die naechste Kombination vor."
        )

        # thinking bewusst deaktiviert: reine JSON-Textsynthese ohne Tool-Use.
        # MODEL_SONNET (claude-sonnet-5, Standardmodell von call_claude())
        # faehrt sonst automatisch "adaptive" Extended Thinking, deren
        # Tokens sich das max_tokens-Budget mit der sichtbaren Antwort
        # teilen - bei knappem Limit kann das Modell dadurch das komplette
        # Budget "wegdenken", bevor ueberhaupt JSON-Text entsteht (siehe
        # portfolio_interpreter_agent.py, wo genau dieser Fall live auftrat).
        response = call_claude(SYSTEM_PROMPT, user_message, max_tokens=1000,
                                thinking={"type": "disabled"})

        if not response["success"]:
            print(f"  Agent-Aufruf fehlgeschlagen: {response['error']}")
            print("  Breche Agent-Suche ab, nutze bisher gefundene Ergebnisse.")
            break

        if response.get("stop_reason") == "max_tokens":
            raw = response.get("raw")
            block_types = ([getattr(b, "type", "?") for b in raw.content] if raw is not None
                            else "unbekannt (kein raw-Objekt)")
            print(f"  Warnung: Antwort bei max_tokens abgeschnitten ({len(response['text'])} "
                  f"Zeichen sichtbarer Text, Content-Block-Typen: {block_types}) - kann kein "
                  f"gueltiges JSON sein, ueberspringe diese Iteration.")
            continue

        decision = extract_json(response["text"])
        if decision is None:
            print(f"  Konnte Antwort nicht als JSON lesen.")
            print(f"  Textlaenge: {len(response['text'])} Zeichen, "
                  f"stop_reason: {response.get('stop_reason', 'unbekannt')}")
            if response["text"]:
                print(f"  Roher Text: {response['text'][:300]}")
            continue

        if decision.get("action") == "stop":
            print(f"  Agent stoppt: {decision.get('reasoning', '(keine Begruendung)')}")
            break

        params = decision.get("params", {})
        reasoning = decision.get("reasoning", "")
        print(f"  Teste: {params}")
        print(f"  Begruendung: {reasoning}")

        result = evaluate_fn(params)
        if result is None:
            print("  -> Kombination erfuellt Mindestkriterien nicht (z.B. zu wenige Trades)")
            history.append({**params, "robustness_score": None, "note": "unterhalb Mindestkriterien"})
        else:
            history.append(result)
            print(f"  -> Score: {result.get('robustness_score', 'n/a')}")

    valid_results = [h for h in history if h.get("robustness_score") is not None]
    best = max(valid_results, key=lambda r: r["robustness_score"]) if valid_results else None

    return {"history": history, "best": best}
