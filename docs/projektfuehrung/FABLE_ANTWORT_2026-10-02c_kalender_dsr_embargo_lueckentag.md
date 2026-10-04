# FABLE_ANTWORT 2026-10-02c — Für Aktien gilt der Handelskalender nach 17.5, die Kurstage sind die Probe dazu (Frage 1: anders). Der Sharpe im DSR bleibt, wie der Code ihn rechnet. R68 bleibt ohne 2d. Das Auffüllen an Kurslücken ist Tatsachennotiz, das Reihenende wird am Snapshot gemessen. Alle sechs Blöcke neu ausgegeben, dazu R72 und R73 — an: steuernder Chat

*Fable (Verfahrensprüfer). Antwort auf `FABLE_ANFRAGE_2026-10-02c` (Stand Register `ad351d5`, 11 313 Zeilen, Abschnitte 0–52; R66–R71 nicht eingetragen). Registertext steht nur im Block am Ende.*

---

## Vorab: Das ist kein neuer Chat

Die Eröffnung 02.10.c ist als zweite Nachricht in **dem Chat** angekommen, der heute 02.10.b beantwortet hat. Ich habe das dem Betreiber als Karte vorgelegt (gemessen 351 798, 🔴; Regel: Umzug vor der nächsten Anfrage). Er hat „Hier beantworten“ gewählt. Die Folgen:

- Der Anfangsbestand dieses Chats ist der Eröffnungstext 02.10.b und das Leseprotokoll von 02b, nicht der Eröffnungstext 02.10.c. Dafür steht R73 im Block (R56 (c)).
- Die Umzugsregel ist mit Wissen des Betreibers übergangen. Ich habe nichts gekürzt, soweit ich es merke; der steuernde Chat misst diese Antwort deshalb nicht milder, eher strenger.

---

## Leseprotokoll (27.4, R56 (b))

**Für diese Antwort neu und vollständig gelesen** (Ablage, `project_read`; Kopf je Commit `ad351d5`, sha256 `a7496780…`, KOPIE): Abschnitt 17 (26,3 KB), Abschnitt 9 (2,1 KB), Abschnitt 16 (41,9 KB; Grössen nach Anfrage). Dazu der Eröffnungstext mit Anfrage 02.10.c (128 Zeilen).

**Aus 02b im Verlauf dieses Chats, nicht erneut geöffnet:** `REGISTER_INDEX.md`, die Abschnitte 4, 7, 15, 23, 24, 29, 48, 49, 50, 51, 52, die Übergabe vom 01.10. (ganz geliefert), die zwei gemessenen Dateien der Projekt-Erinnerung. Meine Antwort 02b habe ich nicht aus der Ablage gelesen; sie steht im Verlauf, wie ich sie geschrieben habe.

**Nur als Ausschnitt:** nichts.

**Nicht gelesen:** alle übrigen Registerabschnitte, darunter 10, 33, 34, 35, 37, 40, 41. `ARBEITSWEISE.md`, `UEBERGABE.md`, `FABLE_DIALOG_INDEX.md`, die Anfragedatei 02c in der Ablage (ich kenne ihren Text aus dem Anhang), `BACKLOG*.md`, alle `ERGEBNIS_*`, `docs/belege/`, `ergebnisse/`, Trade-Listen, Code. Die gesperrten Erinnerungsdateien habe ich nicht geöffnet.

**Ohne mein Zutun geladen:** wie in 02b (kontoweit `profile.md`, `preferences.md`; Liste der Erinnerungsdateien mit Beschreibungszeilen; Dateiliste der Ablage, jetzt 89 Namen).

**Kein Helfer, kein Suchlauf.** Mechanik: je ein Skript für Ampel, Eszett, Bytes und md5.

**Grössen, die an 27.1 grenzen** — neu gelesen, für keine Entscheidung verwendet, nur mit Ort: 16.1.1 (Symbolzahlen je Falte); 16.4 (Jahresschwankung und Korrelation der zwei Anlageklassen); 16.6 (P95 der Haltedauer eines Bots); 17.3 und 17.8 (Zählungen an Kursdateien). Dazu die in 02b genannten Orte. Die Anfrage selbst nennt Zählungen von Datumszeilen, keine Ergebnisse.

Weitere Grössen nach 27.1 kennt der Verfahrensprüfer nicht.

---

## Teil 0. Kenntnis

1. R69 (b), Voraussetzung trifft: zur Kenntnis; sie entfällt im neu ausgegebenen Block.
2. R68, zweite Voraussetzung trifft: zur Kenntnis; entfällt ebenso.
3. Den Fall gibt es in vier ersten Falten: zur Kenntnis; steht als Tatsache in R66 (f).
4. Zitate: Alle genannten Stellen sind in den neuen Fassungen berichtigt. Die zwei, die nicht treffen, sind meine Fehler: Ich habe in R68 eine ersetzte Fassung (2d aus 15.4) als Quelle des Grundes geführt, obwohl die Marke darunter in dem stand, was ich gelesen hatte, und ich habe „beide Träger“ in R60 (c) falsch gelesen. Ob das Fälle der Klasse „Bestand behauptet“ sind, zählt der steuernde Chat.

---

## Teil 1. Antworten

### Frage 1 — anders, weil das Register den Handelskalender schon hat

Für die Aktien-Tagesreihe gilt der **Handelskalender nach 17.5**. Die Kurstage im Snapshot sind die Probe dazu, nicht die Quelle.

Grund: 1a und 2a sprechen von Handelstagen. Woher der Handelskalender des Laufs kommt, sagt 17.5 ausdrücklich: aus dem Paket, „Umgebung, nicht Eingabe“, im Lock. Mein R66 (a) hätte demselben Begriff eine zweite Quelle gegeben; das war dein Gegengrund, und er trifft. Ich kannte 17.5 nicht.

Fallen beide auseinander, **endet der Lauf mit 2**. Das ist keine neue Bauart: Fehlt an einem Kalendertag jeder Kurs, kann der Pfad nicht bewertet werden; trägt ein Symbol einen Kurs an einem Tag ausserhalb des Kalenders, kann ein Benchmark-Tag ohne Zeile der Tagesreihe entstehen, und das ist nach R64 (c) schon ein Befund mit Ausgang 2. Weil die Gleichheit erzwungen wird, hängt an der Wahl der Quelle kein Wert. Deine Messung (0 und 0 Tage Abweichung) sagt, dass die Wache heute nichts kostet. R66 (a), (b).

### Frage 2 (a) — einverstanden

Die Voraussetzung R66 (e) trifft: Kein Code bildet den Falten-Sharpe aus der Tagesreihe. Sie wird im Block zur Tatsache.

Dazu eine Folge aus deiner Messung: Die Sharpe-Funktion in `kennzahlen.py` hat keinen Aufrufer, legt aber fest, was 15.3 offen lässt (Standardabweichung mit `ddof=1`; weniger als zwei Werte ergeben 0). Nach R50 ist das die registrierte Definition. Der Zellen-Erzeuger ruft diese Funktion, sonst wäre die Wahl von `ddof` eine neue Wahl. R66 (c).

### Frage 2 (b) — einverstanden

Der Sharpe im DSR bleibt auf den gemeinsamen Tagen, wie der Code ihn rechnet. Grund: R50 („Der Registertext legt keine dieser Definitionen neu fest“); Abschnitt 9 nennt keine Tage, also gibt es keinen Registersatz, dem der Code widerspräche; der DSR ist Bericht (Festlegung 11).

Dein Gegengrund ist in der Sache richtig: Nach dem Grund der Trennlinie gehörte er auf den Kapitalpfad. Aber die Trennlinie in R66 (c) war zu allgemein gefasst. Ein Block, der noch nicht eingetragen ist, darf nicht durch ein Prinzip einen Widerspruch zu eingefrorenem Code erzeugen, den das Register nicht hergibt. Die neue Fassung zählt deshalb ab und nennt den DSR als das, was er ist: durch den Code definiert.

Was bleibt: Der DSR stellt einen Sharpe auf den gemeinsamen Tagen gegen eine Schwelle aus der Selektionsstatistik, die auf allen Tagen steht. Das gehört zum geführten Nebenbefund der DSR-Einheiten (50.7 Nr. 3) und wird mit ihm vor dem Tag behandelt. R66 (d), (f).

### Frage 3 — einverstanden

R68 (a) bleibt, getragen von R37 (i), R33 und dem Faltenplan: Die Bestätigungsstatistik beginnt an dem Tag, und die Selektionsfalten enden vor der Spanne. „Zu keiner Statistik“ fasse ich genauer: weder zu einer Selektionsfalte noch zur Bestätigungsstatistik. 2d aus 15.4 entfällt als Quelle; 16.6 habe ich jetzt gelesen, es ersetzt 15.4 (d) vollständig.

R68 (c) stützt sich auf die Attribution je Position (16.6, R37). R60 (c) entfällt als Quelle; die Bauart „aus einer Rechnung“ steht richtig in R63 (d).

Neu aus dem Wortlaut von 16.6: Die Attribution ist eine „ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel“. Im Deckelfall ist die Zeile der Bestätigungsperiode also **nicht** der blosse Ausschnitt der Tagesreihe. Die Gleichheitsproben nach R60 (c) und R64 (d) und die Nachrechnung nach R36 würden dort eine Abweichung melden. R68 (d) hält das fest und stellt es zurück an dich, als Frage vor der planmässigen Öffnung.

### Frage 4 (a) — einverstanden

Die Voraussetzung gilt in der engeren Fassung. Benchmark-Tag ist ein Tag, an dem mindestens ein handelbares Symbol **einen Kurs trägt**; so sagt es 23.4 („der Rahmen kennt nur Tage, an denen mindestens ein Symbol einen Kurs hat“). Ein Handelstag ohne Kurs eines handelbaren Symbols ist kein Benchmark-Tag, und R66 (e) verlangt dort eine flache Zelle. R71, R72 (b).

### Frage 4 (b) — einverstanden für die Lücke, mit Vorbehalt für das Reihenende

**Kurslücke: Tatsachennotiz, kein Widerspruch.** Das Symbol bleibt nach 3b (b) handelbar, der Bot kann es über die Lücke halten, und eine gehaltene Position hat an dem Tag auch keinen neuen Kurs. Das Fortschreiben hält Bot und Benchmark in derselben Menge; das Auslassen (pandas 3) verlöre die Rendite über die Lücke. Dafür muss der Erzeuger den Bot am Lückentag genauso bewerten. Das stand nirgends; R72 (c) legt es fest und lässt die Positionstage zählen (Bauart 24.6).

**Reihenende: Dein Gegengrund trifft.** Ein Symbol ohne weitere Kurse, das mit Rendite 0 im Mittel bleibt, ist nicht mehr in der Menge, in der der Bot lebt. Am heutigen Bestand kommt es nicht vor. Ich öffne `benchmark.py` nicht für einen Fall, den es nicht gibt, lasse ihn aber am Snapshot messen; tritt er ein, kommt er vor dem Tag zurück. R72 (d).

**Lock:** Die Abhängigkeit von der pandas-Fassung deckt 5f (17.5) im Lauf. Sie gehört in die Notiz. R72 (e).

### Frage 5 — einverstanden, mit zwei Entscheidungen zu den offenen Orten

Die vier Orte tragen Marken, wie du sie nennst; an 51.6 und 52.3 mit dem Wort PRÄZISIERT statt ERGÄNZT (R70 fasst einen Fall der Regel genauer, wie R65 es an R61 tat).

Die zwei offenen Orte tragen die Marke ebenfalls. Der Massstab ist derselbe wie bei 4.2: Der Wortlaut nennt die Tage nicht, der Block gibt sie ihm. 15.3 (a) bekommt von R66 (a) den Kalender, 48.1 (R33) von R68 (a) die Tage der Zeile. Beide stehen jetzt im Kopf ihrer Blöcke.

17.5 trägt keine Marke: R66 wendet die Notiz an. Indexzeile. Die Marke an 23.3 steht unter dem Blockzitat (Vorbild 25.2).

### Frage 6 — einverstanden

Dieselbe Nummer, letzte Fassung. Weil sich alle sechs Blöcke ändern, gebe ich alle sechs vollständig neu aus; der Registerabschnitt hat damit **eine** Quelldatei, diese. Neu sind R72 und R73. Die Führung im Dialog-Index ist Handwerk.

---

## Kurz

| Frage | Antwort | Block |
|---|---|---|
| 1 | **anders:** Kalender nach 17.5 gilt, Kurstage sind die Probe, Abweichung endet mit 2 | R66 (a), (b) |
| 2 (a) | einverstanden; der Erzeuger ruft die Sharpe-Funktion aus `kennzahlen.py` | R66 (c), (f) |
| 2 (b) | einverstanden: DSR wie im Code; Tagesbasis zum Nebenbefund 50.7 Nr. 3 | R66 (d), (f) |
| 3 | einverstanden; neu: Deckelfall gegen die Gleichheitsproben, zurück an dich | R68 |
| 4 (a) | einverstanden, engere Fassung | R71, R72 (b) |
| 4 (b) | Lücke: Tatsachennotiz. Reihenende: Messung am Snapshot | R72 |
| 5 | einverstanden; auch 15.3 (a) und 48.1 tragen die Marke | R70 |
| 6 | einverstanden; alle sechs neu, dazu R72, R73 | — |

**Umzugsampel:** 🔴 · gemessen 398 901 (Sitzungsprotokoll, letzter Eintrag vor dem Schreiben). Die Grundlast nach der Regel aus der Eröffnung wäre 286 709; das ist hier keine Grundlast, weil die ersten Einträge 0 tragen und der erste mit Nutzung schon die ganze Lektüre von 02b enthält. Ich werte deshalb nach der Grösse · 2 Tagesanfragen · die nächste Anfrage geht an einen neuen Chat; in diesem beantworte ich keine dritte.

---

## Unsicher

1. **Welcher Kalender des Pakets.** 17.5 nennt das Paket, nicht die Börse. R66 (b) führt das als Voraussetzung. Ebenso offen: welcher Code des Laufs den Kalender heute benutzt.
2. **Deckelfall (R68 (d)).** Ich habe nicht entschieden, wie die Proben nach R36, R60 (c) und R64 (d) ihn behandeln. Das ist eine Verfahrensfrage und braucht den Code der planmässigen Öffnung im Blick.
3. **Die Sharpe-Funktion in `kennzahlen.py`.** Ich kenne sie nur aus deiner Beschreibung. Ob ihre Perioden je Jahr 252 und 365 sind, steht als Voraussetzung in R66 (c).
4. **R72 (c)** ist neuer Registertext für den Erzeuger, hergeleitet aus dem Zweck-Satz von 23.3. Bewertet ein vorhandener Kern (etwa `mtm_kern.py`) anders, kommt das zurück.
5. **Die Probe zu R71 und R72** lief nicht in der Lock-Umgebung. Beide Blöcke tragen die Wiederholung als Voraussetzung vor dem Eintrag.
6. **Dieser Chat steht weit über der Schwelle.** Ich habe 16, 17 und 9 ganz gelesen und die Blöcke gegen die Abschnitte im Verlauf geschrieben, nicht gegen ein erneutes Öffnen. Miss die Zitate in den Quellen des Grundes wie beim letzten Mal.

---

## Registerblock — zeichengleich kopierbar (R66–R71 in der Fassung 02c, sie ersetzen die Fassung 02b vollständig; R72 und R73 neu)

```
R66 — Präzisierung zu Registertext 1a und 1c (15.3 (a), (c)) und Ergänzung zu R64 (e) (52.2) (Kalender der Tagesreihe; Tage des Falten-Sharpe). (a) Die Tagesreihe einer Zelle führt jeden Handelstag des Kapitalpfads, vom 1. Januar der ersten Selektionsfalte des Bots (29.3) bis zum Ende der Bestätigungsperiode (35.1), ohne Lücke. Handelstage sind bei Krypto die Kalendertage (15.4, Anmerkung 1), bei Aktien die Tage des Handelskalenders nach 17.5 (Umgebung, im Lock). Ein Tag, an dem die Zelle keine Position hält, steht mit Rendite 0 und Exposure 0 in der Reihe (1a), auch ein Tag vor dem ersten Handelbar-Tag des Bots. (b) Kalender und Kurse stimmen überein: Im Zeitraum nach (a) trägt an jedem Handelstag mindestens ein Symbol der Universumsdatei des Bots (3a) im Snapshot einen Kurs, und kein Symbol der Universumsdatei trägt einen Kurs an einem Tag, der kein Handelstag ist. Eine Abweichung ist ein Befund über Daten oder Umgebung, kein Ausgang (Bauart R33). Der Zellen-Erzeuger prüft das im Lauf je Bot und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. [Voraussetzung, zu messen: welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld kalender); die Messung zur Anfrage 02.10.c verglich mit dem NYSE-Kalender.] (c) Der Falten-Sharpe nach 1c wird über alle Tage der Tagesreihe gerechnet, die in die Falte fallen (2a; halboffen wie im Faltenplan), nicht nur über die Tage, an denen der Benchmark definiert ist. Ein Tag ohne Benchmark-Tag geht mit Rendite 0 ein. Dasselbe gilt für den Sharpe in der Zeile der Bestätigungsperiode, ab dem Tag nach R68. Der Zellen-Erzeuger bildet ihn mit der Sharpe-Funktion aus kennzahlen.py; sie ist die registrierte Definition (R50), ein zweiter Rechenweg wird nicht gebaut. [Voraussetzung, zu messen: dass der Aufruf mit 252 Perioden je Jahr, bei Krypto 365, die Formel aus 15.3 trifft; den Bezeichner trägt die Tatsachennotiz nach R50 (38.2).] (d) Auf den Tagen des Benchmarks stehen: der Drawdown der Nebenbedingung (24.2, R36), die mittlere Exposure (R64), Beta-Bereinigung und Calmar-Vergleich (7 (c)) und das Zufalls-Timing (R48 (g): dieselben Tage wie 7 (c)). Auf dem Kapitalpfad nach (a) steht der Falten-Sharpe und mit ihm die Selektionsstatistik (15.2). Diese Aufzählung ist abschliessend; sie legt die Tage keiner weiteren Kennzahl fest. Die DSR-Eingaben des Gewinners bildet der eingefrorene Code aus den Renditen der Beta-Bereinigung, also auf den gemeinsamen Tagen mit dem Benchmark; das ist die registrierte Definition (R50), Abschnitt 9 nennt keine Tage, und es ist kein Register-Code-Widerspruch. R64 bleibt unberührt. (e) Führt die Tagesreihe einer Zelle an einem Tag, der kein Benchmark-Tag des Bots ist (R72 (b)), eine Rendite ungleich 0 oder eine Exposure ungleich 0, ist das ein Befund über Erzeuger oder Daten, kein Ausgang (Bauart R33); ausgenommen ist der Tag aus der Tatsachennotiz zu 3b (c), Satz zur Zeitachse, in der Fassung R71. Der Zellen-Erzeuger prüft das im Lauf für jede Tagesreihe und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. Die zweite Voraussetzung aus R64 wird damit im Lauf geprüft. (f) Tatsachennotizen: Kein Code auf der Sperrliste oder im Laufbereich bildet den Falten-Sharpe aus der Tagesreihe oder rechnet ihn nach; die Sharpe-Funktion in kennzahlen.py hat heute keinen Aufrufer, auswertung.py liest netto_sharpe aus zellen.csv. Der Fall, dass der Benchmark nicht an allen Tagen einer Falte definiert ist, tritt in vier ersten Falten auf (33.2, 23.4). Der Sharpe im DSR steht auf den gemeinsamen Tagen, die Schwelle des DSR kommt aus der Selektionsstatistik auf allen Tagen; das gehört zum Nebenbefund der DSR-Einheiten (50.7 Nr. 3) und wird mit ihm vor dem Tag behandelt. Die DSR ist Bericht, nicht Tor (Festlegung 11).
Quelle des Grundes: 1c im Wortlaut („aus den täglichen Netto-Renditen des Kapitalpfads“, je Falte, ohne Einschränkung); 1a („Flache Tage stehen mit Rendite 0 in der Reihe“); 2a („Jeder Handelstag gehört zu der Falte, in die sein Datum fällt“); 29.3; 17.5 („Der Handelskalender kommt nicht aus einer Datei, sondern aus dem Paket“; „Umgebung, nicht Eingabe“); 3a („Symbole ohne Historie in einer Falte tragen 0 Trades und 0 Rendite bei“) mit 15.5, Lesart A („trägt für diese Tage 0 bei“); daraus der Schluss des Verfahrensprüfers, dass Nichtteilnahme in der Selektionsstatistik als 0 geführt und nicht ausgeschlossen wird (die Tatsachennotiz zu 1c spricht von Falten ohne Trade, nicht von Tagen ohne Benchmark); 23.2, Grund 2 (der Schaden dort entsteht aus dem Vergleich zweier Reihen; der Falten-Sharpe hat eine); 24.1 und 24.2 (Bewertungsachse; die Zeitachse ist für den Drawdown genannt und bewegt ihn unter (e) nicht: 23.4, Wirkung 3); 23.3 (zur Entstehung: der Kapitalpfad hatte keinen Kalender); R50 („Der Registertext legt keine dieser Definitionen neu fest“); Abschnitt 9; R33; R64 (c); R46; die Messungen des steuernden Chats zur Anfrage 02.10.c, Fragen 1 und 2 (vom Verfahrensprüfer nicht gemessen). Bekannte Richtung der Wirkung, nicht Grund: Über alle Tage der Falte ist der Falten-Sharpe dem Betrag nach nie grösser als über die Benchmark-Tage allein, bei gleichem Vorzeichen (Rechnung des Verfahrensprüfers); die Grösse ist nicht gemessen und für die Entscheidung ohne Belang (Bauart 24.3). Kein Ergebnis.

R67 — Registertext, Ersteintrag, Ergänzung zu R39 (48.7) (Eindeutigkeit und Vollständigkeit der Reihen). In jeder Tagesreihe (tagesreihen/<zelle>.csv) und in jeder Benchmark-Tagesreihe (benchmark_tagesreihen/<bot>.csv) ist datum eindeutig, kein Feld leer und jeder Zahlenwert endlich. Ein flacher Tag trägt 0, nie nichts (1a). Ein Verstoss ist ein Befund über den Erzeuger, kein Ausgang (Bauart R33): Der Zellen-Erzeuger prüft jede dieser Dateien im Lauf, nachdem er sie geschrieben hat, und endet sonst mit 2. Die Abnahme nach R46 prüft die Wache mit Gegenprobe, je für ein doppeltes Datum, ein leeres Feld und einen nicht endlichen Wert; der registrierte Lauf trägt die Wache selbst. auswertung.py wird dafür nicht geöffnet. Für zellen.csv gilt R33.
Quelle des Grundes: R33 („Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang“; „nie nichts“), R39 (die Feldliste jeder Ausgabe ist Registertext), R64 (c) (Bauart), R46, die Messung in 52.4 (lies_tagesreihe, lies_benchmark und beta_bereinigung behandeln und prüfen weder fehlende Werte noch doppelte Daten). Kein Ergebnis.

R68 — Präzisierung zu R33 (48.1), zu R37 (48.5) und zu R64 (52.2) (Zeile der Bestätigungsperiode in zellen.csv). (a) Die Zeile der Bestätigungsperiode (R33) trägt für jede Zelle die Bestätigungsstatistik, die R37 (i) für den Gewinner beschreibt. Alle Grössen dieser Zeile stehen auf den Tagen ab bestaetigung_ab_effektiv der Zelle bis zum Ende der Spanne (35.1). Die Spanne bleibt, was 35.1 sagt; ihre Tage vor diesem Tag gehören weder zu einer Selektionsfalte noch zur Bestätigungsstatistik. (b) R64 (a) gilt für die mittlere Exposure dieser Zeile: Mittel über die Benchmark-Tage des Bots innerhalb der Tage nach (a). Die Grösse ist Bericht; auswertung.py liest sie für kein Urteil. (c) Eine Position, die nach der Attribution je Position (16.6, R37) in der Bestätigungsstatistik nicht gezählt wird, geht in keine Grösse der Zeile ein, auch nicht in ihre Exposure. (d) Im Fall nach (c) ist die Zeile nicht der blosse Ausschnitt der Tagesreihe (16.6: „ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel“). Wie die Gleichheitsproben nach R60 (c) und R64 (d) und die Nachrechnung nach R36 diesen Fall behandeln, ist offen und geht vor der Öffnung nach R69 (b) als Frage an den Verfahrensprüfer. Tatsachennotiz: Die Fassung von 2d in 15.4 (d) („Tage im Embargo gehören zu keiner Periode“) ist durch 16.6 vollständig ersetzt und trägt diesen Block nicht.
Quelle des Grundes: R37 (i) („Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position des Gewinners mehr offen ist“; „Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle“), R33 (genau eine Zeile je Zelle und Falte, Bestätigungsperiode eingeschlossen), 16.6 (Attribution je Position), R64 (a), R63 (d) (Bauart: Exposure aus derselben Rechnung wie die MtM-Reihe), die Messung des steuernden Chats zur Anfrage 02.10.c, Teil 0 Nr. 2. Kein Ergebnis.

R69 — Auflösung des Widerspruchs zwischen R39 (48.7) und auswertung.py (Name der Benchmark-Datei); Präzisierung zu R64 (e) (52.2) und R60 (c) (51.5). (a) Dass auswertung.py benchmark_tagesreihen/<markt>.csv liest und R39 <bot>.csv verlangt, ist ein Register-Code-Widerspruch (25c (1), nach der Wiedergabe in R48 und R50). Er wird zugunsten von R39 aufgelöst; R39 ist damit bestätigt und wird nicht berichtigt. Die Benchmark-Reihe unterscheidet sich je Bot (23.3; 16.7 (b)); eine Datei je Markt kann sie nicht tragen. (b) Vor dem signierten Tag liest auswertung.py die Datei unter dem Namen des Bots. Das ist eine beauftragte Änderung nach 37.3 (Auftrag, Freigabe, alter und neuer Hash) mit neuem Abbild und einem Nachweis mit Gegenprobe (Bauart R55, R64). Sie gehört zur planmässigen Öffnung von auswertung.py, die R36 (zwei Drawdown-Spalten, Nachrechnung), R37 (bestaetigung_ab_effektiv), R34 (zellenbericht.csv) und R55 (Umbenennung) verlangen. Beispieldaten und Tests, die den Namen je Markt schreiben oder lesen, folgen in derselben Änderung. (c) In R64 (e) lies „auswertung.py wird für nichts davon geöffnet“ als „für nichts, was dieser Block in (a) bis (d) regelt, wird auswertung.py geöffnet“. „Dafür“ in R60 (c) bindet ebenso nur die Gleichheit der zwei Träger. Die Öffnung nach (b) berührt beides nicht.
Quelle des Grundes: R39 mit seinem Grund (23.3: die Symbole, die der Loader des Bots handelbar macht; 16.7 (b): Schranken je Bot), 37.3, R45 (Bauart einer beauftragten Änderung), R36, R37, R34, R55, 50.1 und 50.2 (Stand des Vertrags), die Messung des steuernden Chats zur Anfrage 02.10.c, Teil 0 Nr. 1 (auswertung.py kennt weder zellenbericht noch kapital_drawdown_mtm_pct noch bestaetigung_ab_effektiv). Bauart, nicht Quelle: 23.5 („ein Name, der etwas anderes verspricht als das Verhalten“, dort zu einem Docstring). Kein Ergebnis.

R70 — Marken zu R64 (7 (c)) und zu R66 bis R73; Präzisierung zu R61 (b) (51.6) und R65 (a) (52.3). (a) 7 (c) trägt keine Marke zu R64. Abschnitt 7 nennt seine Tage selbst („gemeinsame Tage“, „über dieselben Tage“); R64 gibt das „lies“ R48 (d) und R60 (c), nennt 7 (c) als Geltungsbereich und bestätigt in (b) den Code, nicht den Wortlaut von 7. Ein Ort, den ein Block nur als Geltungsbereich einer Regel nennt, deren „lies“ einem anderen Ort gilt, bleibt ohne Marke und wird vom Index geführt, wie R54 an 7 (c) (R61 (b)). Nennt der Wortlaut eines Ortes die Sache nicht und gibt der Block sie ihm, trägt der Ort die Marke: so 4.2 zu R64, 15.3 (a) zu R66 und 48.1 zu R68. (b) Indexzeilen ohne Marke: 7 (c) — mittlere Exposure des Gewinners, Tage nach R64 (a), (b) und (d). 17.5 — Handelskalender der Aktien-Tagesreihe, R66 (a) und (b). 50.7 Nr. 3 — Tagesbasis des DSR, R66 (f). (c) Marken zu dieser Antwort, der alte Satz bleibt zeichengleich: 15.3 (a) — PRÄZISIERT durch R66, Unterpunkte (a) und (b). 15.3 (c) — PRÄZISIERT durch R66, Unterpunkt (c). 48.1 (R33) — PRÄZISIERT durch R68. 48.5 (R37) — PRÄZISIERT durch R68. 48.7 (R39) — ERGÄNZT durch R67; ERGÄNZT durch R69: R39 ist bestätigt. 48.16 (R48 (d)) — ERGÄNZT durch R72, Unterpunkt (c). 51.5 (R60) — PRÄZISIERT durch R69, Unterpunkt (c). 51.6 (R61) — PRÄZISIERT durch R70, Unterpunkt (a). 52.2 (R64) — ERGÄNZT durch R66 (zu (e)), PRÄZISIERT durch R68, durch R69, Unterpunkt (c), und durch R71 und R72, Unterpunkt (b) (Benchmark-Tag; erster Kurstag). 52.3 (R65) — PRÄZISIERT durch R70, Unterpunkt (a). 52.4, Zeile „R64 (52.2), zweite“ — ERGÄNZT durch R66, Unterpunkte (a) und (e). 52.4, Zeile „R64 (52.2) (a)“ — BERICHTIGT durch R69, Unterpunkt (c). 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse — BERICHTIGT durch R71 und ERGÄNZT durch R72; die Marke steht unter dem Blockzitat der Notiz (Vorbild 25.2). 27 — ERGÄNZT durch R73. Ohne Marke bleiben 24.2, 29.3 und 7 (c) zu R66 (Geltungsbereich oder Quelle des Grundes).
Quelle des Grundes: R61 (b), erster und zweiter Satz, und die Zeile „R54 an 7 (c)“; R65 (a) (auch: eine Tabelle von Befunden ist keine Statusliste; eine Bestätigung trägt ERGÄNZT mit Zusatz); 34 (Kopf: die Marke steht am alten Ort; nach der Wiedergabe in R61 und R65); Wortlaut von Abschnitt 7, 4.2, 15.3 (a) und R33. Kein Ergebnis.

R71 — Berichtigung der Tatsachennotiz zu 3b (c), Satz zur Zeitachse, in 23.3 (welcher Tag ausgelassen wird). „Die Umsetzung lässt den ersten Kurstag je Falte aus, weil pct_change dort keine Rendite liefert“ lies „Die Umsetzung lässt den ersten Kurstag ab dem frühesten Handelbar-Tag des Bots aus, weil pct_change dort für kein Symbol eine Rendite liefert; das geschieht einmal je Bot, nicht in jeder Falte, und der Tag fällt nur dann in eine Falte, wenn er nicht vor der ersten Falte des Bots liegt“. Der Satzteil „höchstens ein Tag je Falte“ bleibt als Schranke richtig; die übrigen Sätze der Notiz bleiben. R64 (a) („erster Kurstag“) und R66 (e) meinen diesen Tag. Gemessen ist das an einer Probe mit synthetischen Kursen unter pandas 2.3.3, ausserhalb der Lock-Umgebung. [Voraussetzung, vor dem Eintrag zu messen: die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner; weicht sie ab, wird gemeldet, nicht eingetragen.]
Quelle des Grundes: 23.4, Wirkung 3 (unter C_lit ändern sich vier Falten um je einen Tag, „der Tag des ersten Kurses, an dem noch keine Rendite vorliegt“, nicht jede Falte); 23.5 („die erste Tagesrendite eines Symbols ist die vom Handelbar-Tag auf den Folgetag“); die Probe des steuernden Chats zur Anfrage 02.10.c, Frage 4 (vom Verfahrensprüfer nicht gemessen). Kein Ergebnis.

R72 — Tatsachennotiz zu Registertext 3b (c) (23.3) (Kurslücke und Reihenende im Benchmark) und Ergänzung zu R48 (d) (48.16) (Bewertung am Lückentag). (a) Unter der registrierten Umgebung (17.5) schreibt bh_tagesrenditen den letzten Kurs eines Symbols fort: An einem Tag, an dem ein handelbares Symbol keinen Kurs trägt und ein anderes handelbares einen trägt, geht das Symbol mit Rendite 0 in das Mittel ein, am nächsten Kurstag mit der Rendite über die Lücke. Das ist, was der Code tut, und kein Widerspruch zu 3b (c): Das Symbol bleibt nach 3b (b) handelbar, und der Bot kann es über die Lücke halten. (b) Benchmark-Tag des Bots im Sinn von 23.3, R64 und R66 ist ein Tag, an dem mindestens ein nach 3b (b) handelbares Symbol des Bots einen Kurs trägt; ausgenommen ist der Tag aus R71. Ein Handelstag, an dem kein handelbares Symbol einen Kurs trägt, ist kein Benchmark-Tag. (c) Der Zellen-Erzeuger bewertet eine offene Position an einem Tag ohne Kurs ihres Symbols zum letzten Kurs; die Position trägt an diesem Tag Rendite 0 und bleibt in der Exposure. Er berichtet je Bot die Zahl solcher Positionstage (Bauart 24.6). Bot und Benchmark werden am Lückentag damit gleich bewertet. (d) Nach dem letzten Kurs eines Symbols führte derselbe Code das Symbol an jedem Folgetag mit Rendite 0 im Mittel weiter. Das wäre mit 3b (c) nicht vereinbar: Ein Symbol ohne weitere Kurse gehört nicht mehr zu der Menge, in der der Bot lebt. Am Bestand vom 02.10.2026 endet keine Reihe früher. Vor dem signierten Tag wird am Snapshot gemessen (Verfahrensmessung nach 27.2), dass keine Kursreihe eines Symbols der zwei Universumsdateien vor dem letzten Kurstag ihres Marktes endet, und wie viele Symbol-Tage Lücke im Zeitraum nach R66 (a) liegen. Endet eine Reihe früher, wird gemeldet und vor dem Tag entschieden. benchmark.py wird für nichts in diesem Block geöffnet. (e) Das Verhalten nach (a) hängt an der pandas-Fassung des Locks: Gemessen füllt 2.3.3 auf, 3.0.5 nicht. Die Prüfung der Umgebung nach 5f deckt das im Lauf. Eine Änderung der pandas-Fassung im Lock vor dem Tag verlangt die Wiederholung der Probe; weicht das Verhalten ab, wird gemeldet. [Voraussetzung, vor dem Eintrag zu messen: die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner; dass kein vorhandener Kern, den der Zellen-Erzeuger für die MtM-Reihe übernimmt, am Lückentag anders bewertet als (c).]
Quelle des Grundes: 23.3 („nur eines darf im Register stehen, und es muss das sein, was der Code tut“; „Bot und Benchmark leben an jedem Tag in derselben Menge“; „handelbar“ nach 3b (b)); 23.4 („der Rahmen kennt nur Tage, an denen mindestens ein Symbol einen Kurs hat“); 23.2 (die Menge, in der ein Bot lebt); 17.5 (registrierte Umgebung, Abbruch bei Abweichung); 24.6 (Bauart: fortgeschriebene Kurstage werden gezählt); R48 (d) (bewertet wie die MtM-Reihe); die Probe und die Zählung des steuernden Chats zur Anfrage 02.10.c, Frage 4 (vom Verfahrensprüfer nicht gemessen). Kein Ergebnis.

R73 — Tatsachennotiz zu 27 nach R56 (c) (die Antwort 02c stammt aus dem Chat der Antwort 02b). Die Eröffnung 02.10.c war für einen neuen Chat geschrieben und kam als zweite Nachricht in dem Chat an, der am 02.10.2026 die Antwort 02b geschrieben hat. Der Betreiber hat am 02.10.2026 per Auswahlkarte entschieden, dass dieser Chat antwortet; die Chatgrösse war dabei gemessen 351 798 und lag über der Umzugsschwelle. Der Anfangsbestand dieses Chats ist der Eröffnungstext 02.10.b und das Leseprotokoll der Antwort 02b; beim Schreiben von 02c kannte er darüber hinaus alles, was das Leseprotokoll von 02b nennt, den eigenen Verlauf zu 02b und die Abschnitte 9, 16 und 17, vollständig gelesen. Eine Verdichtung des Chats hat der Verfahrensprüfer nicht bemerkt. Er hat keinen Helfer und keinen Suchlauf benutzt. Weitere Grössen nach 27.1, als die Leseprotokolle von 02b und 02c nennen, kennt er nicht.
Quelle des Grundes: R56 (a) bis (c), 27.4, Leseprotokolle 02b und 02c. Kein Ergebnis.
```
