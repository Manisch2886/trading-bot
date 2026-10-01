#!/usr/bin/env python3
"""Umzugsampel aus dem Sitzungsprotokoll messen (S2, mit Grundlast-Abzug; Messung 01.10.2026).

Aufruf: python3 ampel.py <sitzung>.jsonl
Läuft dort, wo der Chat läuft (Protokoll unter ~/.claude/projects/*/<sitzung>.jsonl).

Grösse    = input + cache_read + cache_creation des letzten Schritts (Kontext, den das Modell sieht)
Grundlast = Grösse des ersten Schritts (feste Anweisungen, Werkzeuge, erste Nachricht)
Verlauf   = Grösse - Grundlast (das, was der Chat selbst angesammelt hat)
effektiv  = input + 0,1 x cache_read + 2 x cache_creation + 5 x output (Gewichte wie Nachtrag 20:15)
Mehrere Protokollzeilen derselben API-Antwort (gleiche message.id) zählen einmal.
"""
import json, sys

rows, seen = [], set()
for line in open(sys.argv[1], encoding="utf-8"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    m = d.get("message") or {}
    if d.get("type") != "assistant" or not isinstance(m, dict) or not m.get("usage"):
        continue
    if m.get("id") in seen:
        continue
    seen.add(m.get("id"))
    u = m["usage"]
    rows.append((d.get("timestamp", ""), u.get("input_tokens", 0), u.get("cache_read_input_tokens", 0),
                 u.get("cache_creation_input_tokens", 0), u.get("output_tokens", 0)))

groesse = lambda r: r[1] + r[2] + r[3]
grund, jetzt = groesse(rows[0]), groesse(rows[-1])
eff = sum(r[1] + 0.1 * r[2] + 2 * r[3] + 5 * r[4] for r in rows)
print(f"Schritte {len(rows)} · Grösse {jetzt} · Grundlast {grund} · Verlauf {jetzt - grund} · effektiv gesamt {eff:.0f}")
print(f"Kosten nächster Schritt (nur Cache-Lesen) ~{0.1 * jetzt:.0f}")
