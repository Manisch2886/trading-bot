# TB-160 Ampel mit Farbzeichen und Absatz „Schlanke Arbeitsweise“ — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 15.10.2026, 17:07** (Helfer BAU160, per Skript `$HOME/sc/tb160/bau/bau.py`), gebaut ausserhalb des Repos, nur lesend am Repo; alle Befehle an einer Kopie als eigenes git-Repo simuliert. Urteil und Freigabe liegen beim steuernden Chat. Kein Gegenleser (Doku und Werkzeug, Betreiber 13.10.2026, 22:36, Punkt 2). **Gebaut am HEAD `55d503a`.**

**Sitzungstitel:** `TB-160` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `55d503a` (kommt bis zum Start ein Commit dazu, der eine der Zieldateien ändert, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-160`), nicht von Hand.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-160_ampel_farbe_schlank.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9), unten kurz `PY`; das Werkzeug `docs/belege/TB-160/tb160_wz.py` (Anhang B) kurz `WZ`. **Belege:** `docs/belege/TB-160/`. **Ergebnis:** `docs/ERGEBNIS_TB-160_ampel_farbe_schlank.md`.
**Ziel:** (a) `docs/werkzeuge/ampel.py` zeigt wieder das Farbzeichen 🟢/🟡/🔴 mit Empfehlung nach `UMZUG.md` Abschnitt 3 (Betreiber 13.10.2026, 22:36: „repariere die Ampel“). (b) Ein Absatz „Schlanke Arbeitsweise“ am Anfang von `ARBEITSWEISE.md` Abschnitt 0 mit dem Vorschlag vom 13.10.2026, 22:34, und dem Ja von 22:36 im Wortlaut; die abgelösten oder eingeschränkten Zeilen (Karte des Betreibers 15.10.2026) bleiben stehen und bekommen eine Marke, ebenso `UMZUG.md` Z. 106. (c) Eine Backlog-Zeile, ein Journalblock.
**Bauart:** Dokumentations- und Werkzeugauftrag; Vorbild gleicher Bauart: `docs/auftraege/MAC_TB-157_regelwerk_nachtrag_1013.md` (Gliederung, Journalkennung zur Laufzeit, Backlog-Zeile, Commits). Bei Widerspruch gilt dieser Auftrag. **Reihenfolge:** Schritt 0 → E (Einsetzen, Commit) → J/F (Journal, Ergebnis, Abgabe). **Jede Datei, die die Sitzung schreibt, entsteht mit dem Befehl aus dem Anhang „Dateien und ihre Befehle“.**

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei (Betreiber 26.09.2026)** — kein Handelscode, kein Programm unter `research/`, `bots/` oder `config/`; kein Programm ausserhalb des Repos (kein `osascript`, `launchctl`, `kill`).

**Die Sitzung darf ändern, und nichts sonst:**

| Zieldatei | Stücke | numstat-Soll (+ / −) |
|---|---|---|
| `docs/werkzeuge/ampel.py` | A1 (ganze Datei) | **20 / 2** |
| `docs/projektfuehrung/ARBEITSWEISE.md` | A2, M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15 | **43 / 15** |
| `docs/projektfuehrung/UMZUG.md` | M16 | **1 / 1** |
| `docs/projektfuehrung/BACKLOG.md` | B1 | **6 / 0** |
| `docs/projektfuehrung/JOURNAL.md` | Block der Sitzung (Schritt J) | Zeilen des Blocks + 3 / 0 |
| neu: `docs/belege/TB-160/…`, `docs/ERGEBNIS_TB-160_ampel_farbe_schlank.md` | Belege, Werkzeug, Ergebnis | — |

**Nicht erlaubt:** jede andere Datei; `UEBERGABE.md` und `EROEFFNUNG_STEUERNDER_CHAT.md` nach Schritt 0.

## Belegt · erschlossen · offen

- **Belegt** (am HEAD `55d503a` gemessen, Helfer BAU160, 15.10.2026, 17:07): md5 der Zieldateien wie in den Sollwerten (Anhang B); jede Alt-Zeile M1–M16 trifft genau eine Zeile; vor `**Immer**` in Abschnitt 0 und vor `## 6 — Geparkt` steht je eine Leerzeile. Letzte Journalkennung EX; vor `## Wiederkehrende Lehren` stehen `---` und eine Leerzeile.
- **Wortlaute:** Vorschlag 22:34 (vier Punkte und Einschränkung), Ja 22:36 und Anweisung 22:53 Punkt 1 per Skript aus `logs/steuernder_chat/2026-10-14_BETREIBER_chat25_wortlaut.md` (nicht im Repo verfolgt; Kopie im Stück A2). Die neue `ampel.py`: Messformel und die zwei alten Ausgabezeilen zeichengleich zur alten (Probe an 6 synthetischen Protokollen, Bericht BAU160); neu die Zeile `Umzugsampel: <Farbe> · Verlauf <n> (Grundlast <g>) · <Empfehlung>` (Form und Schwellen: `UMZUG.md` Abschnitt 3).
- **Offen — misst die Sitzung, nie raten:** Kennung des Journalblocks (am Bau-HEAD erwartet EY; eine andere ist kein Abbruch).
- **Entscheide:** welche Zeilen abgelöst oder eingeschränkt sind, hat der Betreiber am 15.10.2026 per Karte entschieden (Liste `$HOME/sc/tb160/stellen.md`); die Wegfall-Liste nach Anweisung 22:53, Punkt 3, ist `$HOME/sc/tb160/wegfall.txt` (wegfallend 0, geändert 16 (alt), eingefügt 28 (neu)) — der Betreiber sieht sie vor dem Start.

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-160/` entsteht:** `git status --porcelain > "$TMPDIR/tb160_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD beginnt mit `55d503a` und genau diese Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-160_ampel_farbe_schlank.md
```

Dann das Werkzeug aus Anhang B holen (genau dieser Befehl):

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-160_ampel_farbe_schlank.md "$TMPDIR/tb160_wz.py" <<'EOF2'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
a = z.index("```python", z.index("### Werkzeug"))
t = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
open(sys.argv[2], "w", encoding="utf-8").write(t)
print("tb160_wz.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF2
```

Soll: `tb160_wz.py 16d35fbe6d0243910bee4724eccb521b8078ac2ea0fae2e0840746da6775fb3a`; sonst **ABBRUCH**. Commit `TB-160 Schritt 0: Stand des steuernden Chats vor TB-160` mit genau den Pfaden aus 0a (je eine Zeile `git add <Pfad>`), pushen ⇒ **⟨S0⟩**.

**0b. Ausgang.** `PY "$TMPDIR/tb160_wz.py" ausgang; echo "rc $?"` — legt `docs/belege/TB-160/` an und schreibt `0b_ausgang.txt`. Soll: fünf Zeilen `… · gleich`, `rc 0`. rc 1 ⇒ **ABBRUCH** (Ausgang weicht ab; nichts einsetzen). Dann `cp "$TMPDIR/tb160_0a.txt" docs/belege/TB-160/0a_status.txt` und `cp "$TMPDIR/tb160_wz.py" docs/belege/TB-160/tb160_wz.py`, je `cmp` gleich.

## Schritt E — Einsetzen mit dem Werkzeug

**Probe.** `PY WZ probe > docs/belege/TB-160/e_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-160/e_probe.txt`. Soll: je Stück `… · ok`, je Zieldatei `Soll … · Ist … · gleich`, `Gesamt: wie Soll, nichts geschrieben (Probe)`, `rc 0`. rc ≠ 0 ⇒ **ABBRUCH**.
**Einsetzen.** `PY WZ einfuegen > docs/belege/TB-160/e_einfuegen.txt 2>&1; echo "rc $?" >> docs/belege/TB-160/e_einfuegen.txt`. Soll: wie die Probe, je Datei `geschrieben und zurueckgelesen: … · gleich`, `Gesamt: wie Soll, alle eingefuegt`, `rc 0`.
**Vergleich.** `PY WZ vergleich > docs/belege/TB-160/e_vergleich.txt 2>&1; echo "rc $?" >> docs/belege/TB-160/e_vergleich.txt`. Soll: vier Zeilen `… · GLEICH`, `Gesamt: alle wie Soll`, `rc 0`.
**Zweiter Lauf.** `PY WZ einfuegen > docs/belege/TB-160/e_zweitlauf.txt 2>&1; echo "rc $?" >> docs/belege/TB-160/e_zweitlauf.txt`. Soll: `ABGEWIESEN, nichts geschrieben: schon eingefuegt: …` mit den vier Zieldateien, `rc 2`.

Commit `TB-160 E: Ampel mit Farbzeichen, Absatz Schlanke Arbeitsweise` mit diesen Pfaden (je eine Zeile `git add`), pushen ⇒ **⟨E⟩**:

```
git add docs/werkzeuge/ampel.py
git add docs/projektfuehrung/ARBEITSWEISE.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/UMZUG.md
git add docs/belege/TB-160/0a_status.txt
git add docs/belege/TB-160/tb160_wz.py
git add docs/belege/TB-160/0b_ausgang.txt
git add docs/belege/TB-160/e_probe.txt
git add docs/belege/TB-160/e_einfuegen.txt
git add docs/belege/TB-160/e_vergleich.txt
git add docs/belege/TB-160/e_zweitlauf.txt
```

**Numstat.** `git diff --numstat ⟨S0⟩ ⟨E⟩ > docs/belege/TB-160/e_numstat.txt` (⟨S0⟩ und ⟨E⟩ als Hash). Soll: die vier Zieldateien wie in der Tabelle unter „Freigabe“, dazu nur Dateien unter `docs/belege/TB-160/`. Weicht es ab: weiter, unter „Abweichungen“ nennen.

## Schritt J und F — Journal, Ergebnis, Abgabe

**Journal.** Die Sitzung schreibt ihren Block nach `docs/belege/TB-160/j_block.md` (Gliederung Anhang C; was TB-160 tat, in eigenen Worten; die Kennung misst `PY WZ journal … --probe`). Dann `PY WZ journal docs/belege/TB-160/j_block.md --probe > docs/belege/TB-160/j_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-160/j_journal_probe.txt` und, wenn alle Prüfzeilen `ja` sagen, ohne `--probe` nach `j_journal.txt`. rc 2 ⇒ Block berichtigen (Kopfzeile mit der gemessenen Kennung), erneut.
**Ergebnis** `docs/ERGEBNIS_TB-160_ampel_farbe_schlank.md` (Schreibwerkzeug von Claude Code): Kopf (Stand, Commits) · „Kurz“ (Schritt · Soll · Ist) · „Belege“ (Datei · was) · „Abweichungen“ · „In einfacher Sprache“ (zwei Zeilen).
**Abgabe.** Commit `TB-160 Abgabe: Ergebnis, Journal <Kennung>` mit diesen Pfaden, pushen ⇒ **⟨F⟩**:

```
git add docs/projektfuehrung/JOURNAL.md
git add docs/ERGEBNIS_TB-160_ampel_farbe_schlank.md
git add docs/belege/TB-160/e_numstat.txt
git add docs/belege/TB-160/j_block.md
git add docs/belege/TB-160/j_journal_probe.txt
git add docs/belege/TB-160/j_journal.txt
```

Dann `git status --porcelain > "$TMPDIR/tb160_f.txt"`, `cp "$TMPDIR/tb160_f.txt" docs/belege/TB-160/f_porcelain.txt` (`cmp` gleich; Soll 0 B), Commit `TB-160 Abgabe-Nachweis` mit `git add docs/belege/TB-160/f_porcelain.txt`, pushen ⇒ **⟨F2⟩**. Danach meldet die Sitzung im Chat ⟨S0⟩, ⟨E⟩, ⟨F⟩, ⟨F2⟩ und die Journalkennung.

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD), der sha256 des Werkzeugs weicht ab, oder `ausgang` endet mit rc ≠ 0.
- Schritt E: `probe` oder `einfuegen` endet mit rc ≠ 0; `vergleich` endet nicht mit rc 0; der zweite Lauf endet nicht mit rc 2. Kein Stück von Hand einsetzen.
- `journal` endet mit rc 64 oder mit einer Python-Ausnahme.
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung:** melden, nicht umgehen; den Wortlaut der Frage im Chat melden.
- Eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal.

**Kein Abbruch:** eine andere Journalkennung als EY; `e_numstat.txt` weicht ab; `f_porcelain.txt` nicht leer — je weiter, unter „Abweichungen“ nennen.

**Abbruchweg — so wenig schreiben wie möglich.** Solange ⟨S0⟩ nicht gepusht ist: nichts schreiben, nichts committen, nur im Chat melden (die Abweichung wörtlich). Ab dem gepushten ⟨S0⟩: `printf '%s\n' "<Schritt> · <Abweichung wörtlich>" > docs/belege/TB-160/abbruch.txt`, dann `git add docs/belege/TB-160/abbruch.txt` und die schon geschriebenen Belege, Commit `TB-160 ABBRUCH: <Schritt>`, ein Push-Versuch; nichts zurücksetzen.

## Nicht in TB-160

- Änderungen an `UMZUG.md` ausser der Marke an Z. 106 (kürzere Übergaben, Punkt 3) — nicht in diesem Auftrag.
- Die Eröffnung (`EROEFFNUNG_STEUERNDER_CHAT.md`) — der Absatz hält nur den Entscheid fest.
- Der `jq`-Weg der Ampel (ohne Farbe) — offen.
- Ein Lauf der neuen `ampel.py` an einem echten Sitzungsprotokoll — macht der steuernde Chat.

## In einfacher Sprache

Die Umzugsampel zeigt wieder eine Farbe: Grün heisst bleiben, Gelb heisst Umzug vorschlagen, Rot heisst Umzug vor dem nächsten Auftrag vorschlagen — umgezogen wird erst nach dem Ja des Betreibers. Ausserdem steht der Entscheid vom 13.10.2026 für eine schlankere Arbeitsweise jetzt im Regelwerk; die alten Vorgaben, die er ersetzt, bleiben lesbar und sind markiert.

## Anhang — Dateien und ihre Befehle

| Datei | Befehl |
|---|---|
| `docs/belege/TB-160/0a_status.txt` | `git status --porcelain > "$TMPDIR/tb160_0a.txt"`, nach 0b `cp` (Schritt 0) |
| `docs/belege/TB-160/tb160_wz.py` | Holbefehl aus Schritt 0a nach `$TMPDIR`, nach 0b `cp` |
| `docs/belege/TB-160/0b_ausgang.txt` | `PY "$TMPDIR/tb160_wz.py" ausgang` (Schritt 0b) |
| `docs/belege/TB-160/e_probe.txt`, `e_einfuegen.txt`, `e_vergleich.txt`, `e_zweitlauf.txt` | `PY WZ … > …` (Schritt E) |
| `docs/belege/TB-160/e_numstat.txt` | `git diff --numstat ⟨S0⟩ ⟨E⟩ > …` (Schritt E) |
| `docs/belege/TB-160/j_block.md` | Schreibwerkzeug von Claude Code, Gliederung Anhang C |
| `docs/belege/TB-160/j_journal_probe.txt`, `j_journal.txt` | `PY WZ journal … > …` (Schritt J) |
| `docs/ERGEBNIS_TB-160_ampel_farbe_schlank.md` | Schreibwerkzeug von Claude Code (Schritt F) |
| `docs/belege/TB-160/f_porcelain.txt` | `git status --porcelain > "$TMPDIR/tb160_f.txt"`, dann `cp` (Schritt F) |
| `docs/belege/TB-160/abbruch.txt` | nur bei Abbruch: `printf '%s\n' "…" > …` |
| `docs/werkzeuge/ampel.py`, `docs/projektfuehrung/ARBEITSWEISE.md`, `docs/projektfuehrung/BACKLOG.md`, `docs/projektfuehrung/UMZUG.md` | `PY WZ einfuegen` (Schritt E) |
| `docs/projektfuehrung/JOURNAL.md` | `PY WZ journal …` (Schritt J) |
| `$TMPDIR/tb160_0a.txt`, `$TMPDIR/tb160_wz.py`, `$TMPDIR/tb160_f.txt` | bleiben liegen — nicht löschen (`deny`: `Bash(rm:*)`), nicht committen |

## Anhang A — Stücke (wörtlich)

#### A1 — docs/werkzeuge/ampel.py, ganze Datei

Ersetzt die Datei ganz (Quelle: `$HOME/sc/tb160/ampel.py`, 3040 B, md5 c0e9b93945dc1d075a5d49e60a1d0734).

~~~
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
~~~

#### A2 — ARBEITSWEISE Abschnitt 0, Absatz vor ⟦**Immer**⟧

Art: vor der ersten Zeile `**Immer**` nach `## 0. Vor jeder Antwort — die Ausgabe-Checkliste` (am HEAD `55d503a`: Z. 37); das Werkzeug setzt nach dem Text eine Leerzeile.

~~~
⭐⭐ **Schlanke Arbeitsweise (Betreiber 13.10.2026, 22:36, und Karte 15.10.2026; eingetragen mit TB-160).** Der Betreiber hat den Vorschlag des steuernden Chats vom 13.10.2026, 22:34, mit „Ja“ angenommen und am 15.10.2026 per Karte die offenen Stellen entschieden. Der Absatz ist keine neue Ablaufregel, sondern ersetzt die alten Vorgaben an den unten genannten Stellen; diese bleiben stehen und tragen eine Marke („abgelöst durch …“ oder „gilt nur noch für …“). Wortlaut (per Skript aus `logs/steuernder_chat/2026-10-14_BETREIBER_chat25_wortlaut.md`; vom Vorschlag die vier Punkte und die Einschränkung):

> Meine Empfehlung: alle vier Punkte. Zwei davon mit einer Einschränkung:
>
> 1. **Keine neuen Ablaufregeln.** Fehler der Chats notiere ich nur noch als eine Zeile im Journal. Eine Regel entsteht nur noch, wenn ein Fehler echten Schaden angerichtet hat, etwa an Daten, am Handel oder an Geld.
> 2. **Gegenlesen nur bei Handelscode.** Code, der Handel, Daten oder Broker berührt, prüft weiter ein unabhängiger Prüfer, denn dort geht es um Qualität. Doku, Regeln und Ablage gehen ohne Prüferrunden ins Repo.
> 3. **Kurze Übergaben.** Das spart am meisten. Heute liest jeder neue Chat zuerst rund 100 KB Regeln und Übergabe, bevor er etwas tut. Künftig sollen es 1–2 KB sein: Stand, nächster Schritt, offene Entscheide. Die Details holt der Chat sich nur bei Bedarf.
> 4. **Seltener umziehen.** Den Chat wechsle ich erst, wenn er wirklich voll ist.
>
> **Einschränkung:** Damit das auch für die nächsten Chats gilt, muss es einmal kurz im Repo stehen. Das soll keine neue Regel sein, sondern ein Absatz, der die alten Vorgaben an diesen Stellen ersetzt. Ich würde ihn mit TB-159 zusammen einspielen, dann kostet das keine eigene Runde.

Betreiber, 13.10.2026, 22:36: „Ja und repariere die Ampel sie zeigt keine farbliches signal mehr“

Dazu Anweisung des Betreibers, 13.10.2026, 22:53, Punkt 1 (Wortlaut):

> 1. Fortschritt vor Verwaltung. Token sparen heißt: weniger Nebenarbeit, nicht weniger Sorgfalt. Keine Prüfung, die noch nie etwas gefunden hat; keine Dokumentation, die niemand liest. Große Sammeldateien nicht nach jedem Schritt nachziehen, sondern einmal gebündelt beim Umzug.

Karte des Betreibers, 15.10.2026 (Karte 08:45, eingetragen 08:47; Entscheide zu den offenen Stellen, Zeilen am HEAD `55d503a`, per Skript aus der Nachricht des steuernden Chats):

> - Z. 54 und Z. 142: „wird ersetzt“ — Anweisungen und Befunde gehen sofort als eine Zeile ins Journal (Schutz gegen Verlust), UEBERGABE und Träger werden gebündelt beim Umzug nachgezogen.
> - Z. 107: „wird ersetzt“ — Fable-Anfragen ohne Gegenleser, Zitate per Skript.
> - Z. 281 und 288: „bleibt“, aber nur für Ergebnisse, die Handel oder Daten berühren.
> - Z. 325: „wird ersetzt“ — Zeilenangaben für Registertext setzt ein Skript an der Quelle, kein zweiter Helfer.
> - Z. 125: der Halbsatz „ein Chat je Auftragsrunde“ wird ersetzt; die Ampelschwellen bleiben (gelb ab 200 000 ankündigen, rot über 300 000, Umzug erst nach Ja des Betreibers); UMZUG Z. 106 entsprechend mit Marke.
> - Die 60 Zeilen mit „Fehler Nr.“ bleiben.

Marken (Zeilen am HEAD `55d503a`, vor dem Einfügen dieses Absatzes): abgelöst Z. 54, 107, 121, 125, 142, 276, 302, 325, 333, 340, 345, 346, 349; eingeschränkt Z. 281, 288; dazu `UMZUG.md` Z. 106.
~~~

#### M1 — ARBEITSWEISE Z. 54

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 54 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Sagt der Betreiber „zukünftig": in derselben Antwort in alle Träger eingetragen, ohne Rückfrage | 15 |
~~~

Neu:

~~~
| ☐ | Sagt der Betreiber „zukünftig": in derselben Antwort in alle Träger eingetragen, ohne Rückfrage (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0: Anweisungen und Befunde gehen sofort als eine Zeile ins Journal, UEBERGABE und Träger werden gebündelt beim Umzug nachgezogen — Karte des Betreibers 15.10.2026) | 15 |
~~~

#### M2 — ARBEITSWEISE Z. 107

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 107 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Eine Fable-Anfrage baut ein frischer Helfer (Vorprüfung und Entwurf), ein zweiter liest gegen. Ein frischer Chat nur nach dem Ja des Betreibers zum Umzug (Regel 05.10.2026, 23:58, geht vor); der Kopierblock kommt aus einer Datei, die ein Skript gebaut hat, und wird nur einmal in den Chat geholt — ab rund 20 KB geht die Datei selbst (Zeile „ab rund 20 KB“ oben) (Vorgabe W4, 08.10.2026; 06.10.2026: Rund 82 000 kostete die Fable-Anfrage) | 22.10; UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 5 |
~~~

Neu:

~~~
| ☐ | Eine Fable-Anfrage baut ein frischer Helfer (Vorprüfung und Entwurf), ein zweiter liest gegen. Ein frischer Chat nur nach dem Ja des Betreibers zum Umzug (Regel 05.10.2026, 23:58, geht vor); der Kopierblock kommt aus einer Datei, die ein Skript gebaut hat, und wird nur einmal in den Chat geholt — ab rund 20 KB geht die Datei selbst (Zeile „ab rund 20 KB“ oben) (Vorgabe W4, 08.10.2026; 06.10.2026: Rund 82 000 kostete die Fable-Anfrage) (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0, soweit die Zeile einen Gegenleser verlangt: Fable-Anfragen ohne Gegenleser, Zitate per Skript — Karte des Betreibers 15.10.2026) | 22.10; UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 5 |
~~~

#### M3 — ARBEITSWEISE Z. 121

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 121 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | `BACKLOG.md` und `JOURNAL.md` fortgeschrieben — als Auftrag an die Mac-Sitzung | 5, 5b |
~~~

Neu:

~~~
| ☐ | `BACKLOG.md` und `JOURNAL.md` fortgeschrieben — als Auftrag an die Mac-Sitzung (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0: Backlog, Journal und andere Sammeldateien einmal gebündelt beim Umzug — Anweisung des Betreibers 13.10.2026, 22:53, Punkt 1) | 5, 5b |
~~~

#### M4 — ARBEITSWEISE Z. 125

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 125 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Ein nötiger Umzug wird frühzeitig angekündigt — nach gemessener Ampel (Verlauf ab 200 000 am nächsten sauberen Stand oder vor dem nächsten grossen Block), mit Zahl und Uhrzeit; ein Chat je Auftragsrunde (S1; Schwelle nach der Ampel vom 01.10.2026, 21:35) | 10; UMZUG 3 |
~~~

Neu:

~~~
| ☐ | Ein nötiger Umzug wird frühzeitig angekündigt — nach gemessener Ampel (Verlauf ab 200 000 am nächsten sauberen Stand oder vor dem nächsten grossen Block), mit Zahl und Uhrzeit; ein Chat je Auftragsrunde (S1; Schwelle nach der Ampel vom 01.10.2026, 21:35) (Halbsatz „ein Chat je Auftragsrunde“ abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0, Punkt 4; die Ampelschwellen bleiben — Karte des Betreibers 15.10.2026) | 10; UMZUG 3 |
~~~

#### M5 — ARBEITSWEISE Z. 142

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 142 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Befunde aus der Antwort sofort in die Übergabe (10.10.2026, gelernt: Die Geräteanbindung fiel zweimal weg (10:53 bis 10:55; zwei Gegenleser verloren P3 bis P7 aus der Berichtsdatei)) | UEBERGABE, Umzug 10.10.2026, 11:31, Block 7 |
~~~

Neu:

~~~
| ☐ | Befunde aus der Antwort sofort in die Übergabe (10.10.2026, gelernt: Die Geräteanbindung fiel zweimal weg (10:53 bis 10:55; zwei Gegenleser verloren P3 bis P7 aus der Berichtsdatei)) (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0: Anweisungen und Befunde gehen sofort als eine Zeile ins Journal, UEBERGABE und Träger werden gebündelt beim Umzug nachgezogen — Karte des Betreibers 15.10.2026) | UEBERGABE, Umzug 10.10.2026, 11:31, Block 7 |
~~~

#### M6 — ARBEITSWEISE Z. 276

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 276 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Backlog- und Journal-Nachtrag in derselben Antwort — auch bei Fable, auch wenn kurz | 5b |
~~~

Neu:

~~~
| ☐ | Backlog- und Journal-Nachtrag in derselben Antwort — auch bei Fable, auch wenn kurz (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0: Backlog, Journal und andere Sammeldateien einmal gebündelt beim Umzug — Anweisung des Betreibers 13.10.2026, 22:53, Punkt 1) | 5b |
~~~

#### M7 — ARBEITSWEISE Z. 281

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 281 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Die Abnahme macht ein eng zugeschnittener Helfer, nur lesend, mit eigenem Ordner für Rohausgaben ausserhalb des Repos; er rechnet jede Zahl an der Rohausgabe nach (wie oben in dieser Gruppe), die Kernzahlen rechnet der steuernde Chat danach mit eigenen Befehlen nach (05.10.2026, Abnahme TB-136) | UEBERGABE, Nachtrag 05.10.2026, 22:55; Umzug 05.10.2026, 22:31 und 23:46, Block 7 |
~~~

Neu:

~~~
| ☐ | Die Abnahme macht ein eng zugeschnittener Helfer, nur lesend, mit eigenem Ordner für Rohausgaben ausserhalb des Repos; er rechnet jede Zahl an der Rohausgabe nach (wie oben in dieser Gruppe), die Kernzahlen rechnet der steuernde Chat danach mit eigenen Befehlen nach (05.10.2026, Abnahme TB-136) (gilt nur noch für Ergebnisse, die Handel oder Daten berühren — den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0, Karte des Betreibers 15.10.2026) | UEBERGABE, Nachtrag 05.10.2026, 22:55; Umzug 05.10.2026, 22:31 und 23:46, Block 7 |
~~~

#### M8 — ARBEITSWEISE Z. 288

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 288 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Abnahme in zwei gleichzeitigen Helfern mit getrenntem Zuschnitt; das Ergebnis einer fremden Sitzung zuerst sichern, dann abnehmen, dann schliessen (10.10.2026, so getragen) | UEBERGABE, Umzug 10.10.2026, 09:52, Block 7 |
~~~

Neu:

~~~
| ☐ | Abnahme in zwei gleichzeitigen Helfern mit getrenntem Zuschnitt; das Ergebnis einer fremden Sitzung zuerst sichern, dann abnehmen, dann schliessen (10.10.2026, so getragen) (gilt nur noch für Ergebnisse, die Handel oder Daten berühren — den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0, Karte des Betreibers 15.10.2026) | UEBERGABE, Umzug 10.10.2026, 09:52, Block 7 |
~~~

#### M9 — ARBEITSWEISE Z. 302

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 302 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Vor dem Übergeben liest ein frischer Helfer gegen — jede Zahl, Fundstelle und Werkzeug-Erwartung an der Quelle, bei Fable-Anfragen auch gegen 27.1; gestuft nach T2 | 22.10 |
~~~

Neu:

~~~
| ☐ | Vor dem Übergeben liest ein frischer Helfer gegen — jede Zahl, Fundstelle und Werkzeug-Erwartung an der Quelle, bei Fable-Anfragen auch gegen 27.1; gestuft nach T2 (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0, soweit nicht Code, der Handel, Daten oder Broker berührt — Betreiber 13.10.2026, 22:36, Punkt 2) | 22.10 |
~~~

#### M10 — ARBEITSWEISE Z. 325

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 325 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Zeilenangaben, die in Registertext gehen, misst ein zweiter Helfer an der Quelle (04.10.2026: „02b Z. 128“ aus einem Helferbericht übernommen, richtig ist Z. 127) | UEBERGABE, Umzug 04.10.2026, 13:17, Block 7 |
~~~

Neu:

~~~
| ☐ | Zeilenangaben, die in Registertext gehen, misst ein zweiter Helfer an der Quelle (04.10.2026: „02b Z. 128“ aus einem Helferbericht übernommen, richtig ist Z. 127) (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0: Zeilenangaben für Registertext setzt ein Skript an der Quelle, kein zweiter Helfer — Karte des Betreibers 15.10.2026) | UEBERGABE, Umzug 04.10.2026, 13:17, Block 7 |
~~~

#### M11 — ARBEITSWEISE Z. 333

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 333 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Die Bestandsaufnahme vor dem Bau (zwei Helfer, getrennter Zuschnitt); Bestand und Entwurf in einem Helfer, danach Gegenleser mit getrenntem Zeilenbereich (06. und 07.10.2026, so getragen) | UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 6; UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 8 |
~~~

Neu:

~~~
| ☐ | Die Bestandsaufnahme vor dem Bau (zwei Helfer, getrennter Zuschnitt); Bestand und Entwurf in einem Helfer, danach Gegenleser mit getrenntem Zeilenbereich (06. und 07.10.2026, so getragen) (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0, soweit nicht Code, der Handel, Daten oder Broker berührt — Betreiber 13.10.2026, 22:36, Punkt 2) | UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 6; UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 8 |
~~~

#### M12 — ARBEITSWEISE Z. 340

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 340 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Zählungen im Auftrag kommen aus dem Skript; zwei Runden Gegenlesen bleiben (06.10.2026: beim Bau von TB-133 die Zeilen einer Einfügung falsch gezählt) | UEBERGABE, Umzug 06.10.2026, 07:08, Block 7 Nr. 3 |
~~~

Neu:

~~~
| ☐ | Zählungen im Auftrag kommen aus dem Skript; zwei Runden Gegenlesen bleiben (06.10.2026: beim Bau von TB-133 die Zeilen einer Einfügung falsch gezählt) (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0, soweit nicht Code, der Handel, Daten oder Broker berührt — Betreiber 13.10.2026, 22:36, Punkt 2) | UEBERGABE, Umzug 06.10.2026, 07:08, Block 7 Nr. 3 |
~~~

#### M13 — ARBEITSWEISE Z. 345

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 345 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Kleine Berichtigungen (einzelne Zeilen, kein Sollwert) macht der steuernde Chat per Skript mit `assert` auf genau einen Treffer und lässt einen engen frischen Gegenleser nur diese Zeilen lesen (rund 12 Schritte) (09.10.2026: Nach v5 kam kein Gegenleser mehr — dem Betreiber vor der Karte gesagt) | UEBERGABE, Umzug 09.10.2026, 06:52, Block 7 |
~~~

Neu:

~~~
| ☐ | Kleine Berichtigungen (einzelne Zeilen, kein Sollwert) macht der steuernde Chat per Skript mit `assert` auf genau einen Treffer und lässt einen engen frischen Gegenleser nur diese Zeilen lesen (rund 12 Schritte) (09.10.2026: Nach v5 kam kein Gegenleser mehr — dem Betreiber vor der Karte gesagt) (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0, soweit nicht Code, der Handel, Daten oder Broker berührt — Betreiber 13.10.2026, 22:36, Punkt 2) | UEBERGABE, Umzug 09.10.2026, 06:52, Block 7 |
~~~

#### M14 — ARBEITSWEISE Z. 346

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 346 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Zusatz zur Zeile darüber: Die Zeile „kleine Berichtigungen … enger Gegenleser“ gilt auch unter Zeitdruck; sonst steht „Berichtigungen nicht gegengelesen“ in der Übergabe an den Betreiber (09.10.2026, Fehler Nr. 41: den Cloud-Auftrag mit sechs eingearbeiteten Berichtigungen ausgegeben, bevor ein enger Gegenleser die geänderten Zeilen gelesen hatte, und dem Betreiber nur „gegengelesen“ gesagt) | UEBERGABE, Nachtrag 09.10.2026, 23:51; Umzug 10.10.2026, 07:38, Block 7 Nr. 41 |
~~~

Neu:

~~~
| ☐ | Zusatz zur Zeile darüber: Die Zeile „kleine Berichtigungen … enger Gegenleser“ gilt auch unter Zeitdruck; sonst steht „Berichtigungen nicht gegengelesen“ in der Übergabe an den Betreiber (09.10.2026, Fehler Nr. 41: den Cloud-Auftrag mit sechs eingearbeiteten Berichtigungen ausgegeben, bevor ein enger Gegenleser die geänderten Zeilen gelesen hatte, und dem Betreiber nur „gegengelesen“ gesagt) (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0, soweit nicht Code, der Handel, Daten oder Broker berührt — Betreiber 13.10.2026, 22:36, Punkt 2) | UEBERGABE, Nachtrag 09.10.2026, 23:51; Umzug 10.10.2026, 07:38, Block 7 Nr. 41 |
~~~

#### M15 — ARBEITSWEISE Z. 349

Am HEAD `55d503a`: `docs/projektfuehrung/ARBEITSWEISE.md` Z. 349 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
| ☐ | Ein Bauskript prüft an der Quelle; zwei gleichzeitige Gegenleser mit getrenntem Zuschnitt (Quellen, Logik) und ein dritter für die Nachlese (06.10.2026: Bauskript mit 139 Prüfungen an der Quelle; 07.10.2026: zwei Gegenleser mit getrenntem Bereich) | UEBERGABE, Umzug 06.10.2026, 16:40, Block 7 Nr. 5; UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 8; UEBERGABE, Umzug 07.10.2026, 23:39, Block 7 Nr. 6 |
~~~

Neu:

~~~
| ☐ | Ein Bauskript prüft an der Quelle; zwei gleichzeitige Gegenleser mit getrenntem Zuschnitt (Quellen, Logik) und ein dritter für die Nachlese (06.10.2026: Bauskript mit 139 Prüfungen an der Quelle; 07.10.2026: zwei Gegenleser mit getrenntem Bereich) (abgelöst durch den Absatz „Schlanke Arbeitsweise“ am Anfang von Abschnitt 0, soweit nicht Code, der Handel, Daten oder Broker berührt — Betreiber 13.10.2026, 22:36, Punkt 2) | UEBERGABE, Umzug 06.10.2026, 16:40, Block 7 Nr. 5; UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 8; UEBERGABE, Umzug 07.10.2026, 23:39, Block 7 Nr. 6 |
~~~

#### M16 — UMZUG Z. 106

Am HEAD `55d503a`: `docs/projektfuehrung/UMZUG.md` Z. 106 · Art: ersetzen (ganze Zeile, genau ein Treffer) · Grund: Marke nach dem Absatz „Schlanke Arbeitsweise“ (Liste `stellen.md`)

Alt:

~~~
⭐ **Ein Chat je Auftragsrunde (S1, S7; Betreiberentscheid 01.10.2026, ca. 20:10):** Auftrag schreiben, gegenlesen, freigeben, starten, dann umziehen; die Abnahme macht der nächste Chat. Umzug nach gemessener Ampel und vor einer Pause von mehr als einer Stunde (S1). Seit 21:35 gelten dafür die Ampel auf den Verlauf ohne Grundlast und „vor einer Pause nur ab 🟡“ (oben); die Zahl „rund 250 000“ aus S1 folgt nach Lesart des steuernden Chats dieser Ampel. Eine Nachschau liegt unter einer Stunde, oder vorher wird umgezogen (S7).
~~~

Neu:

~~~
⭐ **Ein Chat je Auftragsrunde (S1, S7; Betreiberentscheid 01.10.2026, ca. 20:10):** Auftrag schreiben, gegenlesen, freigeben, starten, dann umziehen; die Abnahme macht der nächste Chat. Umzug nach gemessener Ampel und vor einer Pause von mehr als einer Stunde (S1). Seit 21:35 gelten dafür die Ampel auf den Verlauf ohne Grundlast und „vor einer Pause nur ab 🟡“ (oben); die Zahl „rund 250 000“ aus S1 folgt nach Lesart des steuernden Chats dieser Ampel. Eine Nachschau liegt unter einer Stunde, oder vorher wird umgezogen (S7). (Seit 15.10.2026 abgelöst, soweit „ein Chat je Auftragsrunde“: `ARBEITSWEISE.md` Abschnitt 0, Absatz „Schlanke Arbeitsweise“, Punkt 4; die Ampelschwellen bleiben — Karte des Betreibers 15.10.2026.)
~~~

#### B1 — BACKLOG Abschnitt 5, Ende, vor ⟦## 6 — Geparkt⟧

Art: vor der Zeile, die mit `## 6 — Geparkt, null Arbeit` beginnt (am HEAD `55d503a`: Z. 487); das Werkzeug setzt nach dem Text eine Leerzeile.

~~~
### Schlanke Arbeitsweise und Ampel mit Farbzeichen — eingetragen mit TB-160

- **Ampel mit Farbzeichen** (Betreiber 13.10.2026, 22:36: „repariere die Ampel sie zeigt keine farbliches signal mehr“; Anweisung 22:53, Punkt 4): `docs/werkzeuge/ampel.py` gibt wieder 🟢/🟡/🔴 und die Empfehlung nach `UMZUG.md` Abschnitt 3 aus; Messformel und die zwei bisherigen Ausgabezeilen unverändert. Eingetragen mit TB-160.
- **Schlanke Arbeitsweise** (Vorschlag des steuernden Chats 13.10.2026, 22:34; Ja des Betreibers 22:36; Anweisung 22:53, Punkt 1; Karte des Betreibers 15.10.2026): Absatz am Anfang von `ARBEITSWEISE.md` Abschnitt 0; 15 Zeilen dort und `UMZUG.md` Z. 106 tragen eine Marke („abgelöst durch …“ oder „gilt nur noch für …“). Die 60 Zeilen mit „Fehler Nr.“ bleiben (Karte 15.10.2026). Eingetragen mit TB-160.
- **Offen:** der `jq`-Weg der Ampel (Abschnitt 0, „Am Ende jeder Antwort“) gibt keine Farbe aus.
~~~

## Anhang B — Werkzeug und Sollwerte

### Werkzeug

```python
#!/usr/bin/env python3
# TB-160 Werkzeug (Python 3.9): setzt die Stuecke aus Anhang A des Auftrags ein, nur in die vier Zieldateien dort (ampel.py, ARBEITSWEISE, BACKLOG, UMZUG).
# Liest nur den Auftrag und die Zieldateien. Prueft alles, bevor es schreibt.
# Aufruf im Repo: PY WZ ausgang | probe | einfuegen | vergleich | journal <j_block> [--probe]
# rc 0 gut · 1 vergleich/ausgang abweichend · 2 abgewiesen, nichts geschrieben · 64 falscher Aufruf
import hashlib, json, os, re, sys
AUF = "docs/auftraege/MAC_TB-160_ampel_farbe_schlank.md"
BEL = "docs/belege/TB-160/"
AMP, AW, BL, JOU = ("docs/werkzeuge/ampel.py", "docs/projektfuehrung/ARBEITSWEISE.md",
                    "docs/projektfuehrung/BACKLOG.md", "docs/projektfuehrung/JOURNAL.md")
UM = "docs/projektfuehrung/UMZUG.md"
ZIEL = [AMP, AW, BL, UM]
KURZ = {"ARBEITSWEISE": AW, "UMZUG": UM}

def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def md5t(t):
    return hashlib.md5(t.encode("utf-8")).hexdigest()

def zaun(z, kopf):
    i = z.index(kopf)
    a = z.index("~~~", i)
    e = z.index("~~~", a + 1)
    return z[a + 1:e], e

def stuecke():
    z = lies(AUF).split("\n")
    s = {"A1": zaun(z, "#### A1 — docs/werkzeuge/ampel.py, ganze Datei")[0],
         "A2": zaun(z, "#### A2 — ARBEITSWEISE Abschnitt 0, Absatz vor ⟦**Immer**⟧")[0],
         "B1": zaun(z, "#### B1 — BACKLOG Abschnitt 5, Ende, vor ⟦## 6 — Geparkt⟧")[0], "M": []}
    for k in [x for x in z if x.startswith("#### M")]:
        alt, e = zaun(z, k)
        j = z.index("Neu:", z.index(k))
        a2 = z.index("~~~", j); e2 = z.index("~~~", a2 + 1)
        neu = z[a2 + 1:e2]
        assert len(alt) == 1 and len(neu) == 1, k
        s["M"].append((k.split(" ")[1], KURZ[k.split(" ")[3]], alt[0], neu[0]))
    soll = json.loads("\n".join(zaun(z, "### Sollwerte (maschinenlesbar)")[0]))
    return s, soll

def bauen(s):
    neu, fehler = {}, []
    neu[AMP] = "\n".join(s["A1"]) + "\n"
    z = lies(AW).split("\n")
    u = lies(UM).split("\n")
    k0 = z.index("## 0. Vor jeder Antwort — die Ausgabe-Checkliste")
    i = z.index("**Immer**", k0)
    if z[i - 1] != "":
        fehler.append("A2: vor **Immer** keine Leerzeile")
    for mid, p, alt, nz in s["M"]:
        d = z if p == AW else u
        n = d.count(alt)
        print("%s · %s · Alt Vorkommen %d · %s" % (mid, p, n, "ok" if n == 1 else "FEHLER"))
        if n != 1:
            fehler.append(mid)
        else:
            d[d.index(alt)] = nz
    z[i:i] = s["A2"] + [""]
    print("A2 · ARBEITSWEISE · vor Z. %d · %d Zeilen" % (i + 1, len(s["A2"]) + 1))
    neu[AW] = "\n".join(z)
    neu[UM] = "\n".join(u)
    b = lies(BL).split("\n")
    a = [k for k, x in enumerate(b) if x.startswith("## 6 — Geparkt, null Arbeit")]
    if len(a) != 1 or b[a[0] - 1] != "":
        fehler.append("B1: Anker")
    else:
        b[a[0]:a[0]] = s["B1"] + [""]
        print("B1 · BACKLOG · vor Z. %d · %d Zeilen" % (a[0] + 1, len(s["B1"]) + 1))
    neu[BL] = "\n".join(b)
    return neu, fehler

def main(a):
    if not a or a[0] not in ("ausgang", "probe", "einfuegen", "vergleich", "journal"):
        print(__doc__ or "Aufruf: ausgang | probe | einfuegen | vergleich | journal <j_block> [--probe]")
        return 64
    s, soll = stuecke()
    if a[0] == "ausgang":
        os.makedirs(BEL, exist_ok=True)
        zeilen, ok = [], True
        for p in ZIEL + [JOU]:
            t = lies(p); g = md5t(t) == soll["vor"][p]
            ok = ok and g
            zeilen.append("%s · %d Z. · md5 %s · Soll %s · %s" % (p, len(t.split("\n")) - 1, md5t(t), soll["vor"][p], "gleich" if g else "UNGLEICH"))
        with open(BEL + "0b_ausgang.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(zeilen) + "\n")
        print("\n".join(zeilen))
        return 0 if ok else 1
    if a[0] == "vergleich":
        ok = True
        for p in ZIEL:
            g = md5t(lies(p)) == soll["nach"][p]
            ok = ok and g
            print("%s · md5 %s · %s" % (p, md5t(lies(p)), "GLEICH" if g else "UNGLEICH"))
        print("Gesamt: " + ("alle wie Soll" if ok else "ABWEICHUNG"))
        return 0 if ok else 1
    if a[0] in ("probe", "einfuegen"):
        if len(a) != 1:
            return main([])
        schon = [p for p in ZIEL if md5t(lies(p)) == soll["nach"][p]]
        if schon:
            print("ABGEWIESEN, nichts geschrieben: schon eingefuegt: " + ", ".join(schon)); return 2
        vor = [p for p in ZIEL if md5t(lies(p)) != soll["vor"][p]]
        if vor:
            print("ABGEWIESEN, nichts geschrieben: Ausgang weicht ab: " + ", ".join(vor)); return 2
        neu, fehler = bauen(s)
        for p in ZIEL:
            g = md5t(neu[p]) == soll["nach"][p]
            if not g:
                fehler.append(p)
            print("%s · Soll %s · Ist %s · %s" % (p, soll["nach"][p], md5t(neu[p]), "gleich" if g else "UNGLEICH"))
        if fehler:
            print("ABGEWIESEN, nichts geschrieben: " + ", ".join(fehler)); return 2
        if a[0] == "probe":
            print("Gesamt: wie Soll, nichts geschrieben (Probe)"); return 0
        for p in ZIEL:
            with open(p, "w", encoding="utf-8") as f:
                f.write(neu[p])
            print("geschrieben und zurueckgelesen: %s · %s" % (p, "gleich" if lies(p) == neu[p] else "UNGLEICH"))
        print("Gesamt: wie Soll, alle eingefuegt"); return 0
    if len(a) not in (2, 3) or (len(a) == 3 and a[2] != "--probe"):
        return main([])
    b, z = lies(a[1]), lies(JOU).split("\n")
    bz = b.split("\n")
    L = [i for i, x in enumerate(z) if x == "## Wiederkehrende Lehren"]
    k = [re.match(r"^## ([A-Z]{2}) — TB-", x).group(1) for x in z[:L[0] if L else 0] if re.match(r"^## ([A-Z]{2}) — TB-", x)]
    letzte = k[-1] if k else "??"
    nk = (letzte[0] if letzte[1] != "Z" else chr(ord(letzte[0]) + 1)) + (chr(ord(letzte[1]) + 1) if letzte[1] != "Z" else "A")
    be = [("endet mit Zeilenende", b.endswith("\n") and not b.endswith("\n\n")),
          ("Kopfzeile ## %s — TB-160: …" % nk, bz[0].startswith("## %s — TB-160: " % nk)),
          ("keine Zeile ---", "---" not in bz),
          ("Schlusszeile *Geschrieben …", len(bz) > 1 and bz[-2].startswith("*Geschrieben ")),
          ("## Wiederkehrende Lehren genau einmal", len(L) == 1),
          ("davor --- und Leerzeile", len(L) == 1 and z[L[0] - 1] == "" and z[L[0] - 2] == "---"),
          ("Kennung noch frei", not any(x.startswith("## %s — " % nk) for x in z))]
    for t, v in be:
        print("%s: %s" % (t, "ja" if v else "NEIN"))
    print("Kennung %s (gemessen; am Bau-HEAD erwartet %s) · letzte %s" % (nk, soll["journal_kennung"], letzte))
    if not all(v for _, v in be):
        return 2
    neu = bz[:-1] + ["", "---", ""]
    print("Zeilen +%d" % len(neu))
    if len(a) == 3:
        print("Probe: nichts geschrieben"); return 0
    z[L[0]:L[0]] = neu
    t = "\n".join(z)
    with open(JOU, "w", encoding="utf-8") as f:
        f.write(t)
    print("geschrieben und zurueckgelesen: %s · md5 %s · %s" % (JOU, md5t(lies(JOU)), "gleich" if lies(JOU) == t else "UNGLEICH"))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

### Sollwerte (maschinenlesbar)

~~~
{
 "vor": {
  "docs/werkzeuge/ampel.py": "997ce08b0d944bed680285584b9936f8",
  "docs/projektfuehrung/ARBEITSWEISE.md": "881739c9856a810d53373d6f32d1f742",
  "docs/projektfuehrung/BACKLOG.md": "350a08d00c147ab9241362d8327a9ccf",
  "docs/projektfuehrung/JOURNAL.md": "ab0a91e08d3f0e28667325bfa5a585f6",
  "docs/projektfuehrung/UMZUG.md": "ed0c881aba18239fd4fe7adcb3174d6c"
 },
 "nach": {
  "docs/werkzeuge/ampel.py": "c0e9b93945dc1d075a5d49e60a1d0734",
  "docs/projektfuehrung/ARBEITSWEISE.md": "1b248e900249a13ec4e7530a24bbcb7c",
  "docs/projektfuehrung/BACKLOG.md": "05a63a1ef403016834a2460391ca3471",
  "docs/projektfuehrung/UMZUG.md": "572c0fc5029d541b9398d05e8d0a1907"
 },
 "journal_kennung": "EY",
 "numstat_E": {
  "docs/projektfuehrung/ARBEITSWEISE.md": "43 / 15",
  "docs/projektfuehrung/BACKLOG.md": "6 / 0",
  "docs/projektfuehrung/UMZUG.md": "1 / 1",
  "docs/werkzeuge/ampel.py": "20 / 2"
 }
}
~~~

## Anhang C — Journalblock (Gliederung; die Sitzung füllt `<…>` in eigenen Worten)

~~~
## <Kennung> — TB-160: Ampel mit Farbzeichen und Absatz Schlanke Arbeitsweise
*Quelle: `docs/ERGEBNIS_TB-160_ampel_farbe_schlank.md`, Commits <⟨S0⟩, ⟨E⟩, ⟨F⟩>.*

**Quelle:** <ein Satz: was eingesetzt ist, wo>

### Was gemessen ist
- <je Schritt eine Zeile mit Soll und Ist>

### Was offen bleibt
- <mindestens: der jq-Weg ohne Farbe>

*Geschrieben <Datum, Uhrzeit aus date> von der Mac-Sitzung TB-160. Quellenvermerk: siehe Kopf.*
~~~
