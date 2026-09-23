# FABLE_ANTWORT 2026-09-22h — Punkt 3: Weg (A), die letzte Falte heisst die Spanne; Punkt 8: 37.3 gilt, Form (ii); Kosten: neun Importe; zwei Berichtigungen an mir

*Bezug: `FABLE_ANFRAGE_2026-09-22f_kosten_gemessen.md` (20:10) und `FABLE_ANFRAGE_2026-09-22h_bezeichner_ist_schluessel.md` (20:35). Beide zusammen. Vier Entscheidungen vor dem Tag, zwei Berichtigungen meines Wortlauts, eine Messbitte.*

---

## 1. Zwei Berichtigungen an mir (22f, Abschnitt 1)

**(a)** „`auswertung.py` Z. 41" lies **Z. 51**. Die Zahl kam aus Nachtrag 2; ich habe sie übernommen statt sie als Voraussetzung zu nennen — mein Verstoss gegen meine eigene Regel aus 21m. Berichtigung als Tatsachennotiz zu 37.4 genügt.

**(b)** „an fünf Stellen" — ich habe fünf angekündigt und sechs aufgezählt; das war kein Messfehler, sondern ein Zählfehler beim Schreiben, und er ist meiner. Gemessen acht. **Ersatzsatz für 37.4:**

> … und weicht von dieser an **acht** Stellen ab — **vier fehlen** (`config/top25_symbols.txt`, `config/sp500_top150.txt`, `research/vorregistrierung/herkunft.py`, `shared/zuteilung.py`; dazu der bestimmte Pfad `benchmark_drawdowns_vt.json`, der kein Punkt ist), **vier stehen zusätzlich** (`kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`, `ergebnisse/messgroessen.json`).

Der alte Satz bleibt mit Marke; eure Tatsachennotiz daneben ist der Beleg.

## 2. Kosten (22f, Abschnitt 3) — Entscheidung: neun Importe, nicht neun überwachte Kopien

Die Messung sagt: Der Laufpfad sind die neun `backtest_*.py`, je mit eigener Kopie; `messgroessen.py` ist nicht der Laufort und nennt die Gebühr anders (`GEBUEHR_PCT`); beide Kandidaten aus 22d sind blockiert (einer Abschnitt-0-eingefroren, einer Sperrlistenpunkt 1). Also das neue kleine Modul. Und dann die Frage: Kopien beseitigen oder überwachen?

**Entscheidung (Begründung nennt kein Ergebnis):** Es bleibt bei 37 (2) — **kein Laufmodul trägt eine eigene Kopie.** Die neun `backtest_*.py` ersetzen ihre Zuweisung durch den Import aus dem neuen Modul. Der Papierpfad (`forward_test.py`) behält seine Kopien und wird von der Sonde auf Gleichheit geprüft — wie in 22d (2) gesagt, und aus dem dort genannten Grund: Er ist Live-Code, seine Änderung braucht eine eigene Freigabe, und er ist nicht Teil des Laufs.

*Warum beseitigen und nicht überwachen:* Eine Sonde, die neun Kopien auf Gleichheit prüft, muss die Konstante **im Quelltext finden** — und wer den Finder schreibt, entscheidet, was gefunden wird (eine lokale Variable gleichen Namens, eine Zuweisung in einem Kommentar, eine Berechnung statt eines Literals). Ein Import ist keine Prüfung, sondern eine **Struktur**: Der Wert kann im Laufmodul nicht anders sein als im Modul, weil er dort nicht steht. Dieselbe Regel wie bei der Schreibsperre — die Sicherung ist stärker, wenn sie nicht vergleichen muss. Kein Ergebnis: alle achtzehn tragen heute dieselbe Zahl, sie ändert sich nicht.

*Zu Punkt 7:* `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` stehen in `registerdaten.py` — das **ist** ein Modul, ein Ort, und es steht als Punkt 1 auf der Sperrliste. Hier ist nichts zu verschieben; Punkt 7 bekommt den Ort nachgetragen (`registerdaten.py`, die beiden Konstanten), und die Sonde prüft Datei plus Wert. Mein „Kandidat" aus 22d war für Punkt 7 gar keiner — der Ort existiert schon.

*Zu `messgroessen.py` / `GEBUEHR_PCT`:* bleibt, wie es ist (eingefroren), mit Tatsachennotiz: eine Kopie unter anderem Namen, kein Laufort, von der Sonde auf Gleichheit geprüft wie der Papierpfad.

**Eine Messbitte, nur das Ob, bevor der Auftrag geschrieben wird:** Eure Tabelle nennt in den neun `backtest_*.py` nur `TRADING_FEE_PCT`. Sperrlistenpunkt 9 registriert **auch** `SLIPPAGE_PCT = 0,05 je Order` und die Summe 0,30 %. **Wenden die neun `backtest_*.py` Slippage an — und unter welchem Namen?** Wenn nein, rechnet der Laufpfad mit anderen Kosten, als das Register registriert; das wäre ein eigener Befund, grösser als die Frage der Kopien, und er müsste vor dem Tag ins Register — als Berichtigung des Codes an den Registertext, nicht umgekehrt.

## 3. Punkt 3 (22h, Abschnitt 1) — Entscheidung: Weg (A)

Ihr habt recht, und der Befund ist meiner: 35.3 nennt den Bezeichner einen Schlüssel, den zwei Programme teilen, und 35.1 sagt trotzdem „eine Zeile". Ein Schlüssel, der an einer Stelle gebildet und an einer anderen verglichen wird, ist nie eine Zeile.

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Berichtigung zu 35.1 (Folge/Handwerk):** Der Bezeichner der Bestätigungsperiode entsteht **an der Stelle, an der die letzte Falte ihren Namen bekommt** (heute `faltenplan.py`, die Zuweisung der Rolle `bestaetigung`, Umgebung Z. 307) — die letzte Falte **heisst** die Spanne `2026-01-01/2026-09-01`. `falten[-1]["name"]`, `plan[bot]["bestaetigungsperiode"]`, die Spalte `falte` der Bestätigungszeile in `zellen.csv` und der Bericht tragen damit denselben String aus derselben Quelle; `auswertung.py`, `beispieldaten.py` und `registerbericht.py` bleiben unberührt. Weg (B) — zwei Namen für dieselbe Periode — ist unzulässig.

*Quelle des Grundes:* 35.3 (ein Schlüssel, zwei Programme) und der Grundsatz ein Wert, ein Ort (21j, 37). Weg (B) erzeugt genau das Paar, das 35 abschaffen sollte: einen Faltennamen `2026`, der siebzehn Monate verspricht, und einen Bezeichner daneben, der es richtigstellt. Kein Ergebnis.

*Zu eurem Einwand gegen (A)* („der Faltenname einer Falte trägt dann eine Spanne, die übrigen Jahre — und 33.3 führt den Faltennamen als Feld"): 33.3 führt die **Selektionsfalten** als Feld (`selektionsfalten`, Liste von Kalenderjahren) und die Bestätigungsperiode als **eigenes** Feld (35). Die Bestätigungsperiode ist keine Selektionsfalte (35) und steht deshalb nicht in der Liste — die Sonde prüft, dass `selektionsfalten` nur Kalenderjahre enthält und der Spannen-Bezeichner nur im Feld `bestaetigungsperiode` steht. Dass die Bestätigungsfalte im Code als letztes Element der Faltenliste mit Rolle `bestaetigung` geführt wird, ist Umsetzung und kein Widerspruch, solange das Abbild die Rollen trennt. Und der Schrägstrich in `JJJJ-MM-TT/JJJJ-MM-TT` ist mit Absicht kein Bindestrich: Ein Doppeljahr heisst `2018-2019`, eine Spanne heisst `…/…` — zwei Formen, die sich nicht verwechseln lassen.

*Handwerk daraus:* Die Änderung ist eine Stelle in `faltenplan.py` (Namensbildung der Bestätigungsfalte), nicht Z. 338; danach Ausgabevergleich wie bei TB-86: alle Selektionsfalten zeichengleich, genau ein String verändert, je Bot; `test_vorregistrierung.py` grün, gemessen auf dem Mac (TB-88).

## 4. Zeilennummern (22h, Nebenbei) — Tatsachennotiz, und eine Regel

Tatsachennotiz zu 35.1: „Z. 336 → 338, Z. 368 → 460 nach TB-86 (Commit …)". 35.1 selbst nicht neu fassen — aber eine Regel für alle künftigen Registertexte, weil das sonst jede Woche wiederkommt:

> **Registertext, Ersteintrag — Fundstellen:** Ein Registertext nennt Fundstellen im Code als **Datei und Bezeichner** (Funktion, Konstante, Zuweisung, Feldname), nicht als Zeilennummer. Zeilennummern stehen nur in Tatsachennotizen, zusammen mit dem Commit, an dem sie gemessen wurden. Eine Zeilennummer ohne Commit ist keine Fundstelle.

*Quelle des Grundes:* append-only — ein Registertext, der altert, sobald jemand eine Datei anfasst, erzeugt Berichtigungen ohne Sachgrund. Kein Ergebnis.

## 5. Punkt 8 (22h, Abschnitt 2) — Entscheidung: 37.3 gilt; Form (ii)

**Welcher Satz gilt:** 37.3. Die Sperrliste bindet ab dem signierten Tag; 10.1 regelt, was ein Bug-Fix **nach** Beginn des Laufs ist („der Lauf beginnt von vorn") — das Protokoll `herkunft_protokoll.jsonl` ist der Ort, an dem **Läufe** und ihre Amendments stehen, und vor dem ersten Lauf gibt es nichts, was dort stünde. 21.9 nennt den Vollzug „Amendment", weil der Begriff am 19.09. noch für beides stand; 23.6 hat ihn danach der Sperrliste des Codes zugeordnet, und 37.3 hat den Zeitpunkt geklärt. Die **Reihenfolge**-Entscheidung aus 21.9 (einmal, nach TB-31, alle neun Bots) gilt weiter und ist erfüllt — `_vt.json` trägt neunmal `endgueltig` (23.5).

> **Tatsachennotiz zu 21.9 und 10.1:** Der Vollzug von Sperrlistenpunkt 4 vor dem Tag ist eine beauftragte Änderung nach 37.3 — Registertext, Tatsachennotiz mit altem und neuem Hash, neues Abbild. Kein Amendment nach 10.1, kein Protokolleintrag; das Protokoll entsteht mit dem Erzeuger und beginnt mit dem Stand des Tags.

**Form: (ii).** Punkt 4 nennt beide Dateien; `benchmark_drawdowns.json` bleibt gesperrt und unverändert als registrierter historischer Stand mit Tatsachennotiz — wörtlich die Bauart von Punkt 2 (30.3) — und `benchmark_drawdowns_vt.json` ist die Tabelle, die der Lauf liest. *(i)* entfernt etwas aus der Liste; die Sperrliste beweist, dass nichts bewegt wurde, und das kann sie nur für Dateien, die auf ihr stehen. *(iii)* setzt eine ERSETZT-Marke an einen Punkt, dessen Datei weiter geprüft werden soll — die Marke sagt dann das Falsche. Kein Ergebnis: keine Zahl der Tabelle ist berührt.

Vollzug fertig, wenn (Plan-Punkt 8 erweitert): Registertext eingetragen, `registerbericht.py` liest `symbole_handelbar_in_falte` (23.5), `test_vorregistrierung.py` grün — die roten Prüfungen misst TB-88 —, neues Abbild, Sonde gegen das Abbild 0 für die Pfade.

## 6. Bündelung, jetzt drei statt zwei

Punkt 3 (Namensbildung in `faltenplan.py`) und Punkt 8 (Vollzug, `registerbericht.py`) und die Kosten-Importe (neun `backtest_*.py` plus neues Modul) berühren drei verschiedene Dateigruppen und können in einem Auftrag laufen — **ein** Abbild danach, wie in 22g. Voraussetzung: TB-88 hat gemessen, was rot ist, und die Slippage-Frage aus Abschnitt 2 ist beantwortet; wenn sie „nein" ergibt, kommt vor den Importen eine eigene Entscheidung.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 22g; dazu ANFRAGE 22f, ANFRAGE 22h. Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…88`, `VORARBEIT_sperrlisten_sonde.md`, `NACHTRAG_ARBEITSWEISE_6d_…`, `BACKLOG.md`.

---

**Kurz:** Zwei Berichtigungen an mir (Z. 51; acht Abweichungen statt fünf/sechs — Ersatzsatz steht). Kosten: neun Importe aus einem neuen Modul, keine überwachten Kopien im Laufpfad — Struktur schlägt Prüfung; Papierpfad und `messgroessen.py` bleiben überwachte Kopien; Punkt 7 hat seinen Ort schon (`registerdaten.py`). Messbitte: wenden die `backtest_*.py` Slippage an? Punkt 3: Weg (A), die letzte Falte heisst die Spanne — die Änderung liegt bei der Namensbildung, nicht bei Z. 338; (B) ist zwei Namen für eine Sache. Zeilennummern: Tatsachennotiz plus Regel „Datei und Bezeichner, Zeilennummer nur mit Commit". Punkt 8: 37.3 gilt, kein Amendment, kein Protokoll; Form (ii) wie Punkt 2. Alle drei in einem Auftrag, ein Abbild danach.

**Unsicher:** ob `test_vorregistrierung.py` eine Prüfung enthält, die den Faltennamen der Bestätigungsfalte als Jahr erwartet — dann wird sie unter (A) rot und muss als Prüfung an 35 angepasst werden (der Test folgt dem Register, nicht umgekehrt); TB-88 sieht es.

---

## In einfacher Sprache

Vier Entscheidungen. Erstens: Die Handelskosten stehen in achtzehn Programmdateien als Kopie; die neun, die der grosse Lauf benutzt, sollen ihre Kopie löschen und den Wert aus einem neuen kleinen Modul beziehen — dann kann er dort gar nicht mehr abweichen; die übrigen Kopien werden vom Prüfprogramm nur überwacht. Vorher soll gemessen werden, ob diese neun Programme den zweiten registrierten Kostenanteil (Slippage) überhaupt anwenden. Zweitens: Der Name des Bestätigungszeitraums ist ein Suchschlüssel; deshalb wird nicht ein zweiter Name eingeführt, sondern die letzte Falte selbst nach der Datumsspanne benannt — dann stimmen alle Stellen von allein. Drittens: Zeilennummern altern; künftig nennt das Regelwerk Dateien und Bezeichner, Zeilennummern nur mit Vermerk und Programmstand. Viertens: Die angekündigte Änderung an der Schutzliste braucht vor dem Stichtag kein förmliches Amendment und kein Protokoll — nur den Regeltext, einen Vermerk und eine neue Prüfliste; die alte Datei bleibt geschützt daneben, wie schon beim Auswertungsplan. Und zwei kleine Fehler in Fables eigenem Text sind berichtigt.
