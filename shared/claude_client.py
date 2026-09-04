"""
Zentraler Claude-API-Client
================================
Gemeinsame Basis fuer alle drei Agenten (Tages-Interpretation,
Parameter-Suche, Marktkontext). Nutzt die offizielle Anthropic
Python-SDK.

WICHTIG - BEVOR DU DAS NUTZT:
1. API-Key erstellen: https://console.anthropic.com
2. Als Umgebungsvariable setzen (NICHT im Code eintragen!):
   im Terminal: export ANTHROPIC_API_KEY="dein-key-hier"
   Fuer Cronjobs (die keine interaktive Shell haben) muss der Key in
   der jeweiligen Cronjob-Zeile gesetzt werden, siehe Anleitung.
3. Jede Anfrage kostet Geld (abhaengig vom genutzten Modell und der
   Textmenge) - das ist unabhaengig von deinem normalen Claude.ai-Zugang.

Alle Agenten-Funktionen sind bewusst so gebaut, dass ein Fehler oder
fehlender API-Key NICHT den Rest des Bots zum Absturz bringt - sie
geben dann einfach eine leere/neutrale Antwort zurueck und der Bot
laeuft normal weiter (nur ohne die KI-Zusatzfunktion).
"""

import os
import json
import anthropic

# Sonnet fuer Aufgaben, die mehr Kontext-Verstaendnis brauchen (Marktkontext,
# Parameter-Suche). Haiku ist deutlich guenstiger und reicht fuer einfache
# Zusammenfassungen (taegliche Einordnung) locker aus.
MODEL_SONNET = "claude-sonnet-5"
MODEL_HAIKU = "claude-haiku-4-5-20251001"


def get_client():
    """
    Gibt einen Anthropic-Client zurueck, oder None falls kein API-Key
    gefunden wird. Sucht in dieser Reihenfolge:
    1. Umgebungsvariable ANTHROPIC_API_KEY (falls gesetzt)
    2. ANTHROPIC_API_KEY in config/email_config.py (einfachste Variante -
       gleiche Datei, die du schon fuer die E-Mail-Zugangsdaten nutzt)

    Findet den config/-Ordner selbststaendig (relativ zu diesem Skript,
    das in shared/ liegt) - unabhaengig davon, welches Skript diese
    Funktion aufruft und ob es CONFIG_DIR selbst schon kennt.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        try:
            import sys
            _shared_dir = os.path.dirname(os.path.abspath(__file__))
            _config_dir = os.path.join(os.path.dirname(_shared_dir), "config")
            if _config_dir not in sys.path:
                sys.path.insert(0, _config_dir)

            import email_config as cfg
            api_key = getattr(cfg, "ANTHROPIC_API_KEY", None)
        except ImportError:
            pass
            import email_config as cfg
            api_key = getattr(cfg, "ANTHROPIC_API_KEY", None)
        except ImportError:
            pass

    if not api_key or api_key == "dein-anthropic-api-key-hier":
        return None

    return anthropic.Anthropic(api_key=api_key)


def call_claude(system_prompt: str, user_message: str, max_tokens: int = 1000,
                 tools: list = None, model: str = MODEL_SONNET) -> dict:
    """
    Zentraler Aufruf-Wrapper. Gibt bei Erfolg {'success': True, 'text': ..., 'raw': ...}
    zurueck, bei Fehler oder fehlendem Key {'success': False, 'error': ...}.
    Wirft absichtlich KEINE Exception nach aussen - Aufrufer koennen sich
    darauf verlassen, dass der Bot dadurch nie abstuerzt.

    model: MODEL_SONNET (Standard) oder MODEL_HAIKU (guenstiger, fuer
           einfache Zusammenfassungsaufgaben ausreichend).
    """
    client = get_client()
    if client is None:
        return {"success": False, "error": "Kein ANTHROPIC_API_KEY gesetzt."}

    try:
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
        }
        if tools:
            kwargs["tools"] = tools

        response = client.messages.create(**kwargs)

        text_parts = [block.text for block in response.content if getattr(block, "type", None) == "text"]
        return {"success": True, "text": "\n".join(text_parts), "stop_reason": response.stop_reason, "raw": response}

    except Exception as e:
        return {"success": False, "error": str(e)}


def extract_json(text: str):
    """
    Versucht, aus einer Textantwort ein JSON-Objekt zu extrahieren -
    Claude haelt sich meist an die Anweisung 'nur JSON', packt es aber
    manchmal trotzdem in ```json ... ``` Codebloecke. Diese Funktion
    raeumt das robust auf.
    """
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    try:
        return json.loads(cleaned.strip())
    except (json.JSONDecodeError, IndexError):
        return None
