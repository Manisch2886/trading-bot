# F3 — Streichliste für die Projekt-Erinnerung (an den Betreiber), 01.10.2026

*Steuernder Chat, ca. 22:00. Gegenstand: die Erinnerungsdateien des Projekts „Trading Bots“. Geprüft sind die zwei Regeldateien `preferences.md` (34 218 B, 50 Zeilen) und `ways-of-working.md` (10 547 B), zusammen 45 von 68 KB. Nicht geprüft: `overview.md`, `methodology-and-learnings.md`, `dashboard-roadmap.md` (Projektfakten, keine Arbeitsregeln). Grundsatz F3: Überholte Vorgeschichte fällt, jede geltende Regel steht einmal. Wo eine Regel im Repo steht (ARBEITSWEISE, UEBERGABE), bleibt in der Erinnerung eine Zeile mit Verweis.*

## preferences.md

| # | Zeile (Datum) | Vorschlag | Grund |
|---|---|---|---|
| 1 | `/remote-control` als eigener Block (19.09.) | streichen | Sitzungswächter startet die Sitzungen (23.09.) |
| 2 | Termius unterwegs per SSH (19.09.) | streichen | überholt seit 23.09. (App-Start, Wächter) |
| 3 | `screen`-Startfolge (20.09.) | streichen | überholt seit 23.09. |
| 4 | Schlüsselbund nach jedem Termius-Neuverbinden (20.09.) | streichen | überholt seit 23.09. |
| 5 | Schlüsselbund vor jeder Mac-Sitzung (20.09.) | streichen | überholt seit 23.09. |
| 6 | Ablegen/Schliessen mit `Strg`+`A`/`D` (20.09.) | streichen | ersetzt durch `schliesse_<HEAD>` (Wächter) |
| 7 | volle Startfolge `screen`/`unlock` (22.09.) | streichen | überholt seit 23.09. |
| 8 | Termius nur zum Starten / App-Start / TB-91-Probe (23.09., lange Zeile) | auf eine Zeile: „Mac-Sitzungen startet und schliesst der steuernde Chat über den Sitzungswächter (`starte_TB-<n>`, `schliesse_<HEAD>` ab 600 s), Aufwand hoch, nie Cloud; ARBEITSWEISE 19, 22.1–22.8“ | Vorgeschichte fällt, Regel bleibt |
| 9 | Mac-Sitzungen nackt starten, Zwei-Minuten-Messung (19.09.) | auf den Kern: Einfügesatz aus dem Zeiger `AKTUELLER_AUFTRAG.md`, Schritt 0, TB-Nummer vorn | Startweg überholt |
| 10 | Aufwand „hoch“ (24.09.) + Wächter-Beschreibung (23.09.) + „mit Aufwand hoch starten“ (26.09.) + „Session anlegen, bevor Text kommt“ (26.09.) | in Zeile 8 zusammenführen | vierfach |
| 11 | Multiple-Choice-Regel mit „ZUM DRITTEN MAL ANGEMAHNT“ (19./20./23.09.) | auf die Fassung M1–M3 (30.09.) | M3 hat sie eingeschränkt; die Rügegeschichte fällt |
| 12 | „nie blosse Ankündigung“ + „immer direkt weitermachen“ (beide 19.09.) | eine Zeile | doppelt |
| 13 | Fable-Kopierblock (19.09.) + Rüge 24.09. | eine Zeile mit der Prüffrage | doppelt, Rüge erzählt |
| 14 | Fable-Takt „eine Anfrage je Tag“ (26.09.) | streichen | ersetzt durch 22.11 „Takt nach Bedarf“ (29.09.) |
| 15 | Helfer-Regel 29.09. 08:50 | streichen | durch 09:20 ersetzt (steht dort selbst) |
| 16 | Umzug nach Tokenzählung ÷ 3,3 (29.09.) + Ampel (b) 09:20 + S2 (01.10.) | eine Zeile mit der geltenden Regel: Verlauf = Grösse − Grundlast, 🟢 < 200 000, 🟡 200–300 000, 🔴 darüber (21:35); Schätzung ÷ 1,6 (F2) | dreimal, zwei überholt |
| 17 | Regeln 24.–29.09. (sieben Punkte) und 29.09. 20:48 (vier Punkte) | eine Zeile „stehen in ARBEITSWEISE 0“ | seit TB-125 im Regelwerk |
| 18 | Sonnet (zwei Zeilen, 29.09.) | eine Zeile | doppelt |
| 19 | M1–M3, T1–T7, S1–S7, F1–F6 | je eine kurze Zeile mit Verweis auf UEBERGABE | Wortlaut steht dort |
| 20 | Editor-Ausweg (21.09.), eine Zeile je Befehl (22.09.), iPhone-Alternative (24.09.) | je eine Kurzzeile | gelten, aber zu lang erzählt |
| — | bleiben unverändert | Aufgabenblock am Ende · Schritt für Schritt · wenig Eigenaufwand · Fable bei Bedarf · Aufgaben [ortsunabhängig]/[Mac-pflichtig] · ZIP-Ablösung · Umzug frühzeitig, nichts verlieren · Handwerk/Verfahren-Aufteilung · selbst messen · Fable-Antwort in den Arbeitschat · „zukünftig“ nachtragen · Doku aktuell statt wachsend · einleitender Satz · Fable legt selbst ab · Empfehlung zu Fable-Karten · was mitgeht · Sichtschutz · Vormessung/Nachmessung · Einfügesatz am Schluss · Nachschau selbst planen · Freigabeklassen · Berechtigungen (gekürzt) · Fable-Sammlung · Eröffnungstext als erste Nachricht · Bote pausiert | gelten |

Erwartete Grösse: rund 12–14 KB statt 34 KB.

## ways-of-working.md (Altbestand vom 15.09., „backfill“)

| # | Teil | Vorschlag | Grund |
|---|---|---|---|
| W1 | Cloud-Aufgaben mit ZIP-Rückgabe, `git status --short` vor `pull` | streichen | Arbeit läuft über Mac-Sitzungen; `git status` über die Brücke verboten |
| W2 | ZIP-Bündelung, ZIP-Namen, ZIP-Pflicht der Mac-Sitzung | streichen | durch die ZIP-Ablösung vom 19.09. überholt |
| W3 | Start-Einzeiler **mit** Auftragstext im Startbefehl | streichen | widerspricht der geltenden Regel (Text nie im Startbefehl) |
| W4 | Fable-Anfragen als Download-Datei | streichen | widerspricht der Kopierblock-Regel |
| W5 | Übergabepaket als ZIP, `START_HIER.md`, `BACKLOG_trading_bot.md`-Blöcke A–I | streichen | Umzug läuft nach UMZUG.md; die Backlog-Struktur ist überholt |
| W6 | `/exit`-Erinnerung, lokale Sitzungen in Termius | streichen | überholt (Wächter) |
| W7 | „In einfacher Sprache“ nur bei Rückmeldungen von aussen | streichen | steht in preferences.md (einleitender Satz) und ARBEITSWEISE 4 |
| W8 | Abschnitt „Fable als Verfahrensprüfer“ | streichen | doppelt zu preferences.md und Register 27 |
| — | bleiben | Delegationsmodell (gekürzt, ohne Termius) · Datenquellen · Broker · E-Mail · Modelle · Sicherheitsnotiz Schlüssel · nano · Empfänger-Präfix im Dateinamen · Warnung vor Verlust · Pfade mitgeben | gelten |

Erwartete Grösse: rund 3–4 KB statt 10,5 KB.

## Was nicht passiert

Es wird nichts umformuliert, was gilt, ausser dass Zeilen zusammengelegt werden. Im Repo ändert sich nichts. Die kontoweiten Präferenzen ausserhalb des Projekts bleiben unberührt.
