# ENTSCHEIDUNGEN 2026-09-26 — Auswahlkarten zu Fable 25f (Gesamtanalyse)

*Abgelegt vom steuernden Chat, 26.09.2026, 07:15. Der erste Teil ist die vorbereitete Kartenliste (02:30), danach folgen die Antworten des Betreibers wörtlich.*


*Vorbereitet 02:30 vom steuernden Chat. Grundlage: Fable 25f Teil C3, dazu die Messung `MESSUNG_2026-09-26_fable25f_voraussetzungen.md`. Vorgelegt wird in zwei Runden zu je höchstens vier Fragen. Entscheidung 8 (P1) entfällt, weil das Budget je Zelle schon in Register 16.4 (g)–(m) steht.*

## Runde 1 — jetzt wirksam (Arbeitsweise und Nacht)

| # | Frage | Optionen (erste = Empfehlung) |
|---|---|---|
| R1 | Sitzung B (TB-111) lief nicht. Wie weiter? | **B jetzt im Ordner `trading-bot-tb111` starten (Empfohlen)**: der Auftrag steht, der Hauptordner bleibt frei · TB-111 in den Hauptordner umschreiben und über den Wächter starten · TB-111 zurückstellen |
| R2 | Freigabeklassen (25f Entsch. 6) | **Handwerk ohne Sperrlistennähe pauschal frei, der Rest einzeln (Empfohlen)** (Ablagen, Stummel, Tatsachennotizen, Testdateien) · wie bisher, jede Öffnung eine Karte · alles pauschal bis zum Tag, nur Sperrliste und `main` einzeln |
| R3 | Fable-Takt (25f Entsch. 7) | **Eine gesammelte Anfrage je Tag; Fable liefert Registertext als Kopierblock (Empfohlen)** · wie bisher, jede Frage sofort · nur bei Registertext- oder Sperrlistenfragen |
| R4 | Zweck des Projekts (25f Entsch. 4, „ein Satz“) | **Hobby mit Methode: der Tag ist das Ziel, Live optional** · Forschung/Lernen: der Baukasten ist das Produkt · Einkommensziel: dann gelten W1–W4 als Schwellen · *(keine Empfehlung des Chats: das ist die Sache des Betreibers. Fable rät, (a) oder (c) ehrlich zu benennen)* |

## Runde 2 — vor dem Tag, ohne Laufberührung

| # | Frage | Optionen |
|---|---|---|
| R5 | Die vier billigen Dinge vor dem Tag (25f C2 H1 Nr. 9) | Mehrfachauswahl: **db-Sicherung ausserhalb des Macs (O6)** · **zweiter und kalter Leser im Prüfgang (V8/F3)** · **Nullbefund-Skizze, eine Seite (F4)** · **Werkzeugkosten als Jahresbudget (W2)** — Empfehlung: alle vier |
| R6 | Ziel der db-Sicherung (O6), falls R5 | **iCloud Drive / externe Platte, täglich per Cron mit Quersumme (Empfohlen)** · Hetzner-VM (liegt ausserhalb des Hauses) · anderes Medium |
| R7 | Scope-Freeze bis zum Tag (25f H1 Nr. 10) | **Ja: neue Ideen nur in `KANDIDATEN_DURCHGANG_2.md`, ohne Auftrag (Empfohlen)** · nein, fallweise |
| R8 | Bündelung (25f A3) | **Drei Bündel: (1) Reste 25d/25e = TB-109 + TB-111, fast fertig · (2) Register 41–44 · (3) 19-Auftrag mit F8 (Empfohlen)** · weiter Einzelaufträge |

## Runde 3 — nach dem Tag (nur zur Kenntnis, jetzt nicht entscheiden)

- Entsch. 1 Ausführungsstelle Krypto (Bitvavo prüfen / nur Aktien live);
- Entsch. 2 erster Live-Bot (Trend-Bot unabhängig vom Rang);
- Entsch. 3 Kapitalrahmen;
- Entsch. 5 Datenquelle Durchgang 2.

Vorschlag für die Karte: „Jetzt nicht, nach dem Tag vorlegen (Empfohlen)“.

---

## Antworten des Betreibers, Runde 1 — 26.09.2026, ca. 06:35

| # | Antwort (wörtlich) |
|---|---|
| R1 | „Jetzt im Worktree starten (Empfohlen)“ |
| R2 | „Handwerk pauschal (Empfohlen)“ — Handwerk ohne Sperrlistennähe (Ablagen, Stummel, Tatsachennotizen, Testdateien) pauschal frei; Registertext, Sperrliste, Live-Code und Reihenfolge nach 36.3 einzeln |
| R3 | „Einmal je Tag, gesammelt (Empfohlen)“ — Fable liefert Registertext als Kopierblock |
| R4 | „Hobby mit Methode“ — der Tag ist das Ziel, Live optional |

## Antworten des Betreibers, Runde 2 — 26.09.2026, ca. 06:40

| # | Antwort (wörtlich) |
|---|---|
| R5 | „Alle“ — O6 db-Sicherung, V8/F3 zweiter und kalter Leser, F4 Nullbefund-Skizze, W2 Werkzeugkosten-Budget |
| R6 | „iCloud Drive (Empfohlen)“ |
| R7 | „Nein, fallweise“ — kein Scope-Freeze; neue Ideen können vor dem Tag Aufträge werden |
| R8 | „Ja, Bündel (Empfohlen)“ |

Runde 3 (Entsch. 1, 2, 3, 5): nach dem Tag vorlegen.

## Antwort des Betreibers, TB-112 — 26.09.2026, ca. 07:00

*„Der nächste Auftrag für den Hauptordner (TB-112, parallel zu B) soll ein Bündel sein. Welche Teile gebe ich frei?“* ⇒ **„Alles“**:
- 19 auf den Laufbereich (`shared/paths.py`, nur unter dem Modus);
- db-Sicherung als Skript (lesend, iCloud, Cron-Zeile durch den Betreiber);
- `tb40_test_*` aufräumen.

## Folgen

- **Entscheidung 8 (P1) entfällt:** Das Budget je Zelle steht in Register 16.4 (g)–(m). Offen ist nur der Vollzug (16.11 Nr. 3, Leiter-Skript), der zu Stufe IV gehört.
- **Kein Scope-Freeze (R7):** Neue Ideen dürfen vor dem Tag Aufträge werden; das entscheidet der Betreiber fallweise.
- **Fable-Takt (R3):** Ab heute geht eine gesammelte Anfrage je Tag an Fable. Die erste ist `FABLE_ANFRAGE_2026-09-26a_…`.
- **V8/F3:** Der zweite und der kalte Leser kommen in Stufe VI (Registerprüfgang). **W2 und F4** schreibt der steuernde Chat; Fable prüft sie in der Tagesanfrage.
- **Nummern:** TB-112 = dieses Bündel. Die Zusammenführung `tb-111` ⇒ `main` samt Register 44 wird **TB-113**.
