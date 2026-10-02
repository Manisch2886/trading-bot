# TB-131 Regelwerk-Nachtrag 02.10.2026 (Auftragstext am Antwortende, Fehler Nr. 17–19, T7, R65 (a)) und `ampel.py` (null-Felder, leere Schritte)

**Sitzungstitel:** `TB-131` · **Modell:** Opus 5.5 (Standard) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 02.10.2026 vom steuernden Chat
**Vorgänger:** TB-130 (`e8cfff8`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-131_regelwerk_nachtrag_ampel.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei** (Betreiberentscheid 26.09.2026; so auch TB-127 und TB-128). Die Regel in E1 hat der Betreiber am 02.10.2026, 10:45, wörtlich verlangt: „du sollst mir immer den text für die aufgabe der claude code tasks zum ende ausgeben damit ich diesen final starten kann. merke dir das endlich für die Zukunft.“

Geändert werden nur: `docs/projektfuehrung/ARBEITSWEISE.md`, `docs/projektfuehrung/BACKLOG.md`, `docs/werkzeuge/ampel.py`, dazu Belege, Ergebnis und Journal.

⛔ **Nicht erlaubt, mit Grund:**
- Den vorgegebenen Text umformulieren, kürzen, glätten oder zusammenlegen. *Grund:* Die Wortlaute hat der steuernde Chat aus den Quellen festgelegt und gegenlesen lassen; die Sitzung trägt sie ein (5b).
- Register, `docs/VORREGISTRIERUNG_*`, `research/`, `shared/`, `strategies/`, jede Sperrlisten-Datei, `UMZUG.md`, jedes andere Werkzeug unter `docs/werkzeuge/`. *Grund:* nicht Gegenstand.
- `UEBERGABE.md`, `UEBERGABE_ARCHIV.md` und die `FABLE_*`-Dateien ändern. *Grund:* Das sind die Quellen.

Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt (auch `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`); das ist kein Ändern im Sinn der Verbote und des Abbruchkriteriums.

**Sichtschutz:** entfällt, es werden keine Ergebnisse gelesen.

## Verfahren je Einfügung (E1–E5)

*Vorgezählt vom steuernden Chat am 02.10.2026, 17:03, über die Geräteanbindung (Python `str.count`) am `e8cfff8`: jeder Anker genau 1; die ersten Zeilen der neuen Texte kommen in den Zieldateien noch nicht vor. `ARBEITSWEISE.md` hat 2 389 Zeilen, `BACKLOG.md` 281. Die Sitzung zählt selbst nach; ihre Zahl gilt.*

Wie TB-128 (Vorlagen `docs/belege/TB-128/einfuegen.py` und `c3_vergleich.py`):
1. **Vorher:** Anker in der genannten Zieldatei zählen. **Soll: genau 1.** Weicht die Zahl ab: diese Einfügung nicht ausführen, vermerken, weitermachen (kein Abbruch).
2. **Ausführen** wie unter „Art“: „nach der Zeile“/„vor der Zeile“ bezieht sich auf die ganze Zeile mit dem Anker. Der Text ist der Inhalt des Codeblocks unter der Einfügung, ohne Zäune. Tabellenzeilen (E1–E4) ohne Leerzeilen; der Block E5 mit genau einer Leerzeile davor und danach, eine vorhandene wird nicht verdoppelt.
3. **Nachher:** Die erste Zeile des eingefügten Texts zählen. **Soll: genau 1.**
4. **Werkzeug:** per Skript `docs/belege/TB-131/einfuegen.py`, das Zieldatei, Anker, Art und Text aus **diesem Auftrag** liest, nicht aus dem Gedächtnis.

Ergebnis je Einfügung in `docs/belege/TB-131/einfuegungen.txt`: `E<n> · Datei · Anker vorher · ausgeführt ja/nein · Text nachher`.

## Schritt 0 — Sicherung, Ausgang

0a. **Zuerst, bevor `docs/belege/TB-131/` entsteht:** `git status --porcelain > "$TMPDIR/tb131_0a.txt"`. Soll: genau die Einträge unten; die Reihenfolge zählt nicht. Weicht etwas ab ⇒ Abbruch. Danach die Datei nach `docs/belege/TB-131/0a_status.txt` kopieren.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-131_regelwerk_nachtrag_ampel.md
```

Commit `TB-131 Schritt 0: Stand des steuernden Chats 02.10.2026, Abend`, pushen. Der Commit heisst im Folgenden **⟨S0⟩**.

0b. sha256, md5 und Zeilenzahl der drei Zieldateien ⇒ `docs/belege/TB-131/0b_ausgang.txt`. Soll für `docs/werkzeuge/ampel.py`: md5 `0c42ee78b6fa162e795f0cab026cde9e`, 35 Zeilen; weicht das ab ⇒ Schritt B nicht ausführen, vermerken (kein Abbruch). Die Belege aus 0a und 0b gehen mit dem Commit aus Schritt A.

## Schritt A — Die Einfügungen

#### E1 — Abschnitt 0, „Am Ende jeder Antwort“: der Text für die Aufgabe der Claude-Code-Sitzung (Betreiber 02.10.2026, 10:45)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Letzte Zeile: Umzugsampel, gemessen mit` · Art: **nach der Zeile**

```
| ☐ | Der Text für die Aufgabe der Claude-Code-Sitzung steht am Ende jeder Antwort als Kopierblock mit Empfänger darüber, unmittelbar vor der Umzugsampel (deren Zeile bleibt die letzte) — auch wenn der Sitzungswächter den Satz schon eingesetzt hat. Wortlaut aus `logs/sitzungswaechter/letzter_satz.txt` bzw. `AKTUELLER_AUFTRAG.md`, nicht aus dem Gedächtnis; ist kein Auftrag startklar, steht das dort (Betreiber 02.10.2026, 10:45: „merke dir das endlich für die Zukunft“; Fehler Nr. 19) | 6b, Start |
```

#### E2 — Abschnitt 0, „Wenn ich ein fremdes Ergebnis bewerte“: Fehler Nr. 17 und die Teilmessung

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Vor dem Urteil „Widerspruch“ prüfen, ob die Registerstelle` · Art: **nach der Zeile**

```
| ☐ | Nummern am Block zählen, nicht an der Kurzfassung (Fehler Nr. 17: Der Registerblock von Fable 01a reichte bis R62, „Kurz“ nannte R62 nicht) | UEBERGABE, Nachtrag 02.10.2026, 07:46 |
| ☐ | Ein „kein Widerspruch“ nennt, was gemessen ist und was nicht; eine Teilmessung heisst Teilmessung (02.10.2026: „Unsicher“ 2 zu Fable 01a, vom Gegenleser berichtigt) | UEBERGABE, Nachtrag 02.10.2026, 10:04 |
```

#### E3 — Abschnitt 0, „Wenn Dateien abgelegt oder aus der Ablage gelesen werden“: Fehler Nr. 18 und T7

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Grosse Dokumente nicht im Chat zusammensetzen:` · Art: **nach der Zeile**

```
| ☐ | Vor jedem Lesen in den Chat die Bytes messen und mit ÷ 1,6 gegen die Ampel rechnen; von Vorlagen nur die Gliederung und die eine gebrauchte Stelle; Wortlaute, die ein Skript einsetzt, liest das Skript (Fehler Nr. 18, 02.10.2026: Verlauf 173 970 nach 7 Minuten, 272 304 nach 33 Minuten) | UEBERGABE, Nachtrag 02.10.2026, 10:04 |
| ☐ | „Frischer Stage-Pfad“ heisst ein neuer Pfadname: Ein zweites `device_commit_files` aus demselben Pfad meldete „written“ und liess die alte Fassung liegen. Die md5-Wache steht vor Zeiger, Nachtrag und Auslöser (T7, erneut am 02.10.2026 bei TB-130) | 23 |
```

#### E4 — Abschnitt 0, „Wenn ich einen Auftrag schreibe“: R65 (a), Sperre des Arbeitsbaums, Folgeauftrag

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Marken nennen Bezeichner, nicht Zeilen (R49 (e))` · Art: **nach der Zeile**

```
| ☐ | Registerauftrag: Die Aufzählung eines Blocks schliesst die Regel aus 34 nicht ab. Der steuernde Chat bestimmt die Marken an allen Orten, denen ein Block ein „lies“, eine Ergänzung oder eine Bestätigung gibt, und weist sie im Auftrag als seine aus (R65 (a)) | Register 52.3 |
| ☐ | Vor Schritt 0 einer Mac-Sitzung legt der steuernde Chat keine weitere Datei in den Arbeitsbaum (0a zählt die Einträge); nach Schritt 0 fasst er dort nichts an, bis die Sitzung abgegeben hat (02.10.2026) | UEBERGABE, Nachtrag 02.10.2026, 10:19 |
| ☐ | Folgeauftrag gleicher Bauart: auf den Vorgänger verweisen und nur Unterschiede und Sollwerte nennen, nicht abschreiben; das Prüfskript läuft vor der Freigabe am echten Repo, nicht nur an einer Kopie (TB-130) | 2, 12 |
```

#### E5 — BACKLOG, Abschnitt 5: aus der Abnahme TB-130

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile**

```
### Aus der Abnahme TB-130 (02.10.2026)

- **Für die nächste Fable-Anfrage** (neuer Fable-Chat): 52.5 Nr. 2 (Zeitachse des Falten-Sharpe; erst Vorprüfung in 16, 21, 29, 33), Nr. 5, 6, 7 und 9; dazu drei Reibungen aus ERGEBNIS_TB-129 und ERGEBNIS_TB-130: `registerkopie.py --marken` zählt die erste Zitatzeile von R61 (TB-129) und von R65 (TB-130) als Marke; an 25.2 steht die Marke aus R65 vor der älteren aus R53; es gibt kein eigenes Markenwort für Bestätigungen.
- **T7, erneut:** Ein `device_commit_files` aus einem schon benutzten Stage-Pfad meldete „written“ und liess die alte Fassung liegen (TB-130, 02.10.2026). Die Regel dazu trägt TB-131 in ARBEITSWEISE 0 ein.
- **Mit TB-131 (Ausgang im Ergebnis TB-131):** die Regeln aus Fehler Nr. 17, 18 und 19 und aus R65 (a) in ARBEITSWEISE 0; `docs/werkzeuge/ampel.py` liest `null` als 0 und zählt Schritte mit Grösse 0 nicht.
```

Commit `TB-131 A: Regelwerk-Nachtrag`, pushen.

## Schritt B — `docs/werkzeuge/ampel.py`

**Befund (02.10.2026, 08:40, Protokoll des steuernden Chats in der Cloud):** Vor dem ersten eigenen Schritt stehen drei Schritte eines anderen Modells mit `input_tokens` 0 und `null` in `cache_read_input_tokens` und `cache_creation_input_tokens`. Das Skript bricht mit `TypeError` ab; ohne die `null`-Felder nähme es einen Schritt mit Grösse 0 als Grundlast.

B1. Die Datei wird durch genau diesen Inhalt ersetzt (zeichengleich, mit einem Zeilenumbruch am Ende). Geändert sind nur der Schluss des Docstrings und die Bildung von `rows`; Rechenweg und Ausgabe bleiben.

```python
#!/usr/bin/env python3
"""Umzugsampel aus dem Sitzungsprotokoll messen (S2, mit Grundlast-Abzug; Messung 01.10.2026).

Aufruf: python3 ampel.py <sitzung>.jsonl
Läuft dort, wo der Chat läuft (Protokoll unter ~/.claude/projects/*/<sitzung>.jsonl).

Grösse    = input + cache_read + cache_creation des letzten Schritts (Kontext, den das Modell sieht)
Grundlast = Grösse des ersten Schritts (feste Anweisungen, Werkzeuge, erste Nachricht)
Verlauf   = Grösse - Grundlast (das, was der Chat selbst angesammelt hat)
effektiv  = input + 0,1 x cache_read + 2 x cache_creation + 5 x output (Gewichte wie Nachtrag 20:15)
Mehrere Protokollzeilen derselben API-Antwort (gleiche message.id) zählen einmal.
Felder mit null zählen als 0; Schritte mit Grösse 0 (Hilfsschritte ohne Nutzung, etwa eines anderen
Modells vor dem ersten eigenen Schritt) zählen nicht (TB-131, Befund 02.10.2026).
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
eff = sum(r[1] + 0.1 * r[2] + 2 * r[3] + 5 * r[4] for r in rows)
print(f"Schritte {len(rows)} · Grösse {jetzt} · Grundlast {grund} · Verlauf {jetzt - grund} · effektiv gesamt {eff:.0f}")
print(f"Kosten nächster Schritt (nur Cache-Lesen) ~{0.1 * jetzt:.0f}")
```

Soll nachher: md5 `997ce08b0d944bed680285584b9936f8`, 40 Zeilen.

B2. Probe mit Gegenprobe, Skript `docs/belege/TB-131/b2_probe_ampel.py`, Ausgabe `b2_probe_ampel.txt`. Die alte Fassung kommt aus `git show ⟨S0⟩:docs/werkzeuge/ampel.py` nach `$TMPDIR`. Zwei erfundene Protokolle in `$TMPDIR` (keine echten Sitzungsdaten):
- **P1, normal:** drei Zeilen `type` = `assistant` mit verschiedenen `message.id` und `usage` (`input_tokens` 2; `cache_read_input_tokens` 100000, 110000, 120000; `cache_creation_input_tokens` 20000, 1000, 500; `output_tokens` 100, 50, 20).
- **P2, mit leeren Schritten:** davor zwei Zeilen `type` = `assistant` mit eigenen `message.id` und `usage` = `{"input_tokens": 0, "cache_read_input_tokens": null, "cache_creation_input_tokens": null, "output_tokens": 0}`, dann dieselben drei Zeilen wie P1.

Soll: alt(P1) rc 0 · neu(P1) rc 0 und Ausgabe bytegleich mit alt(P1) · alt(P2) rc ≠ 0 (Gegenprobe: der Befund) · neu(P2) rc 0 und Ausgabe bytegleich mit neu(P1). Wie die Fehlermeldung von alt(P2) genau aussieht, ist vom Interpreter abhängig; im Ergebnis beschreiben. Ist ein Soll rot ⇒ `git checkout -- docs/werkzeuge/ampel.py`, Schritt B als nicht ausgeführt vermerken (kein Abbruch).

Commit `TB-131 B: ampel.py liest null als 0, zählt leere Schritte nicht`, pushen.

## Schritt C — Nachweis

C1. `einfuegungen.txt`. Soll: E1–E5 je Anker vorher 1, ausgeführt, Text nachher 1.

C2. `git diff --numstat ⟨S0⟩ HEAD` je Datei ⇒ `docs/belege/TB-131/c2_numstat.txt`. Soll: `ARBEITSWEISE.md` `8	0`; `BACKLOG.md` `6	0`. `docs/werkzeuge/ampel.py` `7	2`; entfernte Zeilen gibt es nur dort.

C3. Zeichengleichheit: `docs/belege/TB-131/c3_vergleich.py` liest je Einfügung den Text aus diesem Auftrag und prüft, dass er in der Zieldatei genau einmal als zusammenhängender Block vorkommt (Bytevergleich); dazu der md5 von `ampel.py` gegen das Soll aus B1 ⇒ `c3_vergleich.txt`.

Commit `TB-131 C: Nachweis`, pushen.

## Schritt D — Abgabe

D1. `docs/ERGEBNIS_TB-131_regelwerk_nachtrag_ampel.md`: Kopf, Kurz-Tabelle (0a, 0b, E1–E5, B1, B2, C1, C2, C3), „Nicht getan“ und „In einfacher Sprache“. Unter „Nicht getan“: die Ablage von `ARBEITSWEISE.md` und `BACKLOG.md` (macht der steuernde Chat, `BACKLOG.md` erst nach der 27.4-Prüfung); K2h/K2f, die drei Trägerstellen, Fables 29a Abschnitt 1, die Sonnet-Probe, `registerkopie_abschnitte.py` entfernen (Betreiberentscheid fehlt) — unverändert offen aus ERGEBNIS_TB-128.

D2. Journalblock nach dem letzten Buchstabenblock von `JOURNAL.md`, vor `## Wiederkehrende Lehren`; Kennung messen (erwartet **EC**), mit Quellenzeile.

D3. Abgabe-Commit `TB-131 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Danach `git status --porcelain` in den Scratch und als `docs/belege/TB-131/d3_porcelain.txt`, kleiner letzter Commit, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab.
- Eine Datei ausserhalb der Zieldateien, Belege, Ergebnis und Journal müsste geändert werden.
- `git push` scheitert zweimal.

Bei Abbruch: committen, was an Belegen da ist, Grund in `docs/belege/TB-131/abbruch.txt`, pushen, melden.

## In einfacher Sprache

Heute sind neue Arbeitsregeln entstanden: Der Starttext für eine Programmiersitzung steht künftig am Ende jeder Antwort, und aus drei Fehlern des Tages sind Prüfregeln geworden. Diese Sitzung trägt sie wörtlich an den festen Stellen ein. Ausserdem repariert sie das kleine Messprogramm für die Umzugsampel, das an leeren Einträgen im Protokoll abbrach, und prüft die Reparatur an zwei erfundenen Beispielen.
