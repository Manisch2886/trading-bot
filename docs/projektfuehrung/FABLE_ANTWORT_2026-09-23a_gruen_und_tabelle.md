# FABLE_ANTWORT 2026-09-23a — „Grün" bleibt Tag-Vorbedingung, nicht Fertigkriterium von Punkt 8; die Tabelle, die der Lauf liest, ist die, deren Falten das Register sind

*Bezug: `FABLE_ANFRAGE_2026-09-22i_slippage_ja_und_gruen_nein.md` (22.09., 22:40). Kenntnisnahme zu 1, 2, 5; zwei Entscheidungen (3, 4); ein neuer Planpunkt und eine Wache.*

---

## 1. Kenntnisnahme (Abschnitte 1, 2, 5)

**Slippage:** 9/9, `2 × (0,1 + 0,05)` = 0,30 %, Ein- und Ausstieg — der Laufpfad rechnet, was Punkt 9 registriert. Die Formabweichung bei `t3_supertrend` ist Wert- und stellengleich; für die Importe verschwinden beide Schreibweisen der Zuweisung. Voraussetzung aus 22h Abschnitt 6 erfüllt; die Kosten kommen in denselben Auftrag.

**Weg (A):** Euer Grund ist stärker als meiner, und er ist gemessen: (B) und (B′) brechen an `auswertung.py` ab, weil Z. 177–182 die **Menge** der Faltennamen gegen den Plan prüft — (B) hätte Sperrlistenpunkt 5 geöffnet. Damit steht (A) auf drei Beinen: ein Wert, ein Ort (22h); kein Eingriff in gesperrten Code (eure Messung); A3 bleibt wahr (eure Messung). Angenommen.

**Berichtigungen:** Z. 435 statt 437; Commit `4daa254` für die Tatsachennotiz zu 35.1 — angenommen, und genau so gehört es in die Notiz.

## 2. Fertigkriterium Punkt 8 (Abschnitt 3) — Entscheidung: (1), mit einer Schärfung

Mein Satz „fertig, wenn `test_vorregistrierung.py` grün" hat zwei Dinge vermischt: eine **Tag-Vorbedingung** (21.9: der Test blockiert den Tag, solange er rot ist) und ein **Fertigkriterium für einen Punkt**. Das Fertigkriterium eines Punktes muss an dem hängen, was der Punkt ändert — sonst wird ein Punkt nie fertig, weil er für fremde Fehler haftet.

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Punkt 8 ist fertig, wenn:** Registertext eingetragen (Form (ii)), Tatsachennotiz mit altem und neuem Hash, `registerbericht.py` liest `symbole_handelbar_in_falte` (23.5), **der Absturz (`KeyError` an der Faltenzuordnung) ist weg** und `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**, neues Abbild, Sonde 0 für die Pfade. Der Ausgang der einzelnen Prüfungen ist nicht Fertigkriterium von Punkt 8.
>
> **Neuer Planpunkt vor dem Tag — „Testannahmen folgen dem Register":** `test_vorregistrierung.py` ist der Nachweis von Abschnitt 12 („150 Prüfungen, acht Mutationsproben"). Jede Prüfung, deren Annahme dem Register hinterherhinkt, wird an das Register angepasst — nie umgekehrt, und nie gelöscht. Für G6: Faltennamen kommen aus dem Faltenplan (Abbild 33.3), nicht als Literale `"2020"`, `"2022"`. Für H3: Eine Mutationsprobe, die nicht mehr beisst, wird so gestellt, dass sie **mit der registrierten Faltenzahl** beisst (und die Mutationsprobe selbst bleibt Pflicht — eine Probe, die immer besteht, ist keine). **Tag-Vorbedingung nach 21.9 und A4: null rote Prüfungen, null „bekannt rot".** (3) ist damit ausgeschlossen, wie ihr sagt.

*Quelle des Grundes:* 12 (der Test ist der Vollständigkeitsnachweis des Auswerters), 21.9 (rot blockiert den Tag), A4. Kein Ergebnis: Testannahmen über Faltennamen und Faltenzahl sind Verfahrensseite.

*Warum nicht (2):* G6 und H3 berühren keine Tabelle, sondern den Faltenplan, und ihr Grund (TB-56/61/72) ist drei Aufträge alt. Wer sie in Punkt 8 packt, gibt einem Vollzug, der eine Datei betrifft, Verantwortung für einen Test, der eine andere Sache prüft — und die Reihenfolge (8 blockiert den Tag, nicht nach hinten) verliert ihren Sinn, wenn 8 wächst.

**Eine Regel dazu, weil G6 die zweite Instanz derselben Fehlerklasse ist** (die erste war die Bestätigungsfalte): Prüfungen und Werkzeuge, die Falten kennen müssen, beziehen sie aus dem Abbild des Faltenplans (33.3) oder aus `faltenplan.py` — **nie als Literale**. Das ist Handwerk in der Umsetzung, aber Verfahren im Grundsatz: Ein Literal ist eine Kopie des Registers im Code, und Kopien altern.

## 3. Die Tabelle für `t3_supertrend` (Abschnitt 4) — Entscheidung: die Tabelle folgt dem registrierten Faltenplan, für alle neun

Die Frage ist grösser als ein Bot. Sperrlistenpunkt 4 registriert `DD_Toleranz` je Bot, und `DD_Toleranz` wird über die Selektionsfalten des Bots gerechnet. Eine Tabelle, die für einen Bot eine Falte enthält, die der registrierte Plan (33.2) nicht kennt, ist für diesen Bot **auf einem anderen Plan gerechnet** — und ihr `DD_Toleranz`-Wert stammt aus einer anderen Faltenmenge. Ob er sich „nur wenig" oder „viel" von der anderen Fassung unterscheidet, ist nach 24.3 ohne Belang und nach 27.1 nicht meine Sache.

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Registertext zu Sperrlistenpunkt 4 / 23 / 33:** Die Benchmark-Tabelle, die der Lauf liest, ist auf dem registrierten Faltenplan (33.2) gerechnet: Für jeden Bot ist die Faltenmenge der Tabelle gleich der Menge seiner Selektionsfalten nach 33.2 (plus Bestätigungsperiode, sofern die Tabelle sie führt) — nicht mehr, nicht weniger —, und ihre Benchmark-Definition ist die aus 23 (tagesgenau). Eine Tabelle, die diese Bedingung für auch nur einen Bot nicht erfüllt, wird nicht vollzogen; sie bleibt liegen und erhält eine Tatsachennotiz, auf welchem Planstand sie gerechnet wurde.
>
> **Wache (in den Vollzug und in den Laufwrapper):** Faltenmenge der vollzogenen Tabelle je Bot gegen das Abbild des Faltenplans — Abweichung ist 1, fehlende Datei 2. Der `KeyError '2017'` von heute ist genau dieser Befund, nur als Absturz statt als Wache.
>
> **Folge für den Vollzug:** Es wird **eine** Tabelle für alle neun Bots vollzogen, keine Mischung. Welche Datei das ist, entscheidet die Bedingung, nicht der Name: Ist `benchmark_drawdowns_tb72.json` für alle neun Bots auf 33.2 gerechnet und tagesgenau nach 23, dann ist sie die Tabelle, und `_vt.json` erhält eine Tatsachennotiz als Zwischenstand (23, vor 25); die Gruppe „bestimmt" in 37.2 wechselt entsprechend. Erfüllt keine vorhandene Tabelle die Bedingung für alle neun, wird die Tabelle **einmal neu gerechnet** — mit `benchmark.py` (Punkt 4/6), auf dem Abbild des Faltenplans, mit Beleg und Hash, vor dem Tag.

*Quelle des Grundes:* 23.7 („der Widerspruch zwischen berichtigtem Faltenplan und gesperrter Benchmark-Tabelle … wird mit demselben Amendment geschlossen") — geschlossen heisst: die Tabelle folgt dem Plan, nicht der Plan der Tabelle. Und 24.3 als Bauart: Die Regel steht hier, **bevor** ich weiss, welche Datei sie erfüllt; die Werte kenne ich nicht und brauche sie nicht. Kein Ergebnis.

*Warum nicht `_vt.json` für acht und TB-72 für einen:* Zwei Tabellen mit zwei Erzeugungszeitpunkten in einem Sperrlistenpunkt sind zwei Träger; und eine Tabelle, die für einen Bot eine tote Falte trägt, ist als Ganzes von einem Planstand, den es nicht mehr gibt — die acht „passenden" Bots passen nur, weil sich ihre Falten seit TB-66 zufällig nicht bewegt haben.

**Messbitten, nur das Ob, vor dem Vollzug:** (1) Erfüllt `benchmark_drawdowns_tb72.json` die Bedingung für alle neun Bots — Faltenmenge je Bot gleich 33.2, Benchmark tagesgenau nach 23, `status: endgueltig` neunmal? (2) Trägt eine der Tabellen die Bestätigungsperiode als Zeile, und unter welchem Namen (nach 35 künftig die Spanne)? (3) Steht `benchmark_drawdowns_tb72.json` heute in irgendeiner Sperrlisten-Gruppe oder liegt es nur daneben?

## 4. Was sich am Plan ändert

- **Punkt 8:** Fertigkriterium wie in Abschnitt 2; Tabelle nach Abschnitt 3 — erst die Messbitten, dann Vollzug. Bleibt vor dem Erzeuger, bleibt Tagblocker.
- **Neu, Stufe II/III: „Testannahmen folgen dem Register"** (G6, H3 und jede weitere Prüfung, die beim Durchlauf nach Punkt 8 rot ist). Vor dem Tag; unabhängig von 8.
- **Neu, in 7 und 10: Wache „Faltenmenge der Tabelle = Abbild".**

**Leseprotokoll dieses Chats, Stand jetzt:** wie 22h; dazu ANFRAGE 22i. Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…89`, `VORARBEIT_sperrlisten_sonde.md`, `NACHTRAG_ARBEITSWEISE_6d_…`, `BACKLOG.md`.

---

**Kurz:** Slippage 9/9 und 0,30 % — kein Befund, Kosten in denselben Auftrag. Weg (A) mit gemessenem, stärkerem Grund bestätigt. Punkt 8: fertig, wenn Registertext, Notiz, `registerbericht.py`, **Absturz weg und Test läuft durch** — der Ausgang einzelner Prüfungen ist Tag-Vorbedingung (21.9, A4), nicht Fertigkriterium des Punktes; G6/H3 werden ein eigener Punkt „Testannahmen folgen dem Register", Faltennamen aus dem Abbild statt als Literale, Mutationsproben müssen wieder beissen. Tabelle für `t3_supertrend`: keine Mischung — die Tabelle, die der Lauf liest, ist für **alle neun** auf 33.2 gerechnet und tagesgenau nach 23; erfüllt das TB-72, ist TB-72 die Tabelle und `_vt.json` ein Zwischenstand mit Notiz; erfüllt es keine, wird einmal neu gerechnet. Dazu eine Wache: Faltenmenge der Tabelle gegen das Abbild.

**Unsicher:** ob `benchmark_drawdowns_tb72.json` tagesgenau nach 23 gerechnet ist (TB-72 lag nach TB-66, aber ich habe es nicht gemessen) — Messbitte (1).

---

## In einfacher Sprache

Drei gute Nachrichten und zwei Entscheidungen. Gut: Alle neun Laufprogramme rechnen die registrierten Kosten vollständig; der Weg für den Namen des Bestätigungszeitraums ist nicht nur begründet, sondern gemessen der einzige, der ohne Eingriff in geschützten Code funktioniert; und die Zeilennummern-Regel wird angewandt. Erste Entscheidung: Fable hatte „Test grün" als Fertigkriterium gesetzt — das war zu grob. Der Vollzug ist fertig, wenn der Absturz weg ist und der Test durchläuft; zwei veraltete Testannahmen, die dem Faltenplan hinterherhinken, werden ein eigener Arbeitspunkt, denn vor dem Stichtag muss der Test trotzdem ganz grün sein — „bekannt rot" gibt es nicht. Zweite Entscheidung: Die Vergleichstabelle, die der Lauf liest, muss für alle neun Bots auf dem eingetragenen Faltenplan gerechnet sein — keine Mischung aus zwei Fassungen. Welche Datei das ist, entscheidet diese Bedingung, nicht der Name; im Zweifel wird einmal neu gerechnet. Und der Absturz von heute wird zur Wache: Die Falten der Tabelle werden künftig gegen den Plan geprüft, statt zufällig aufzufallen.
