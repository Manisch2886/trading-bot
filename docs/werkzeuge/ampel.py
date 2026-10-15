#!/usr/bin/env python3
"""Umzugsampel aus dem Sitzungsprotokoll messen (S2, mit Grundlast-Abzug; Messung 01.10.2026),
mit Farbzeichen und Empfehlung nach UMZUG.md Abschnitt 3 (Betreiber 01.10.2026, ca. 21:35; 05.10.2026, 23:58).

Aufruf: python3 ampel.py <sitzung>.jsonl
Läuft dort, wo der Chat läuft (Protokoll unter ~/.claude/projects/*/<sitzung>.jsonl).

Grösse    = input + cache_read + cache_creation des letzten Schritts (Kontext, den das Modell sieht)
Grundlast = Grösse des ersten Schritts (feste Anweisungen, Werkzeuge, erste Nachricht)
Verlauf   = Grösse - Grundlast (das, was der Chat selbst angesammelt hat)
effektiv  = input + 0,1 x cache_read + 2 x cache_creation + 5 x output (Gewichte wie Nachtrag 20:15)
Mehrere Protokollzeilen derselben API-Antwort (gleiche message.id) zählen einmal.
Felder mit null zählen als 0; Schritte mit Grösse 0 (Hilfsschritte ohne Nutzung, etwa eines anderen
Modells vor dem ersten eigenen Schritt) zählen nicht (TB-131, Befund 02.10.2026).
Farben auf den Verlauf (UMZUG 3): 🟢 unter 200 000 · 🟡 200 000–300 000 · 🔴 darüber.
Die Empfehlung nennt den Zeitpunkt für den Vorschlag; umgezogen wird erst nach dem Ja des Betreibers
(UMZUG 3, 05.10.2026, 23:58). Komprimierung oder Verlust von Gelesenem (🔴 nach UMZUG 3) misst das
Werkzeug nicht; das meldet der Chat selbst.
Die letzte Zeile ist die Ampelzeile in der Form nach UMZUG 3:
Umzugsampel: <Farbe> · Verlauf <n> (Grundlast <g>) · <Empfehlung>
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
    r = (d.get("timestamp", ""), u.get("input_tokens") or 0, u.get("cache_read_input_tokens") or 0,
         u.get("cache_creation_input_tokens") or 0, u.get("output_tokens") or 0)
    if r[1] + r[2] + r[3] == 0:
        continue
    rows.append(r)

groesse = lambda r: r[1] + r[2] + r[3]
grund, jetzt = groesse(rows[0]), groesse(rows[-1])
verlauf = jetzt - grund
eff = sum(r[1] + 0.1 * r[2] + 2 * r[3] + 5 * r[4] for r in rows)
print(f"Schritte {len(rows)} · Grösse {jetzt} · Grundlast {grund} · Verlauf {verlauf} · effektiv gesamt {eff:.0f}")
print(f"Kosten nächster Schritt (nur Cache-Lesen) ~{0.1 * jetzt:.0f}")

if verlauf < 200_000:
    farbe, empf = "🟢", "bleiben"
elif verlauf <= 300_000:
    farbe, empf = "🟡", ("Umzug vorschlagen: am nächsten sauberen Stand, vor dem nächsten grossen Block "
                        "oder vor einer Pause über einer Stunde, mit Uhrzeit; umgezogen wird erst nach dem Ja")
else:
    farbe, empf = "🔴", "Umzug vorschlagen: vor dem nächsten Auftrag; umgezogen wird erst nach dem Ja"
fmt = lambda n: f"{n:,}".replace(",", " ")
print(f"Umzugsampel: {farbe} · Verlauf {fmt(verlauf)} (Grundlast {fmt(grund)}) · {empf}")
