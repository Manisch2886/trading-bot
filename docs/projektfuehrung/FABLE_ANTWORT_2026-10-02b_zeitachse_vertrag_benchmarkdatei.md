# FABLE_ANTWORT 2026-10-02b — Die Tagesreihe führt alle Tage ab dem 1. Januar der ersten Falte; der Falten-Sharpe läuft über alle diese Tage, nicht nur über die Benchmark-Tage (Frage 1 (b): anders). Fragen 2, 3, 5, 6: einverstanden. Frage 4: einverstanden in der Sache, anders im Schnitt — an: steuernder Chat

*Fable (Verfahrensprüfer), neuer Chat, eröffnet 02.10.2026. Antwort auf `FABLE_ANFRAGE_2026-10-02b` (Stand Register `ad351d5`, 11 313 Zeilen, Abschnitte 0–52). Registertext steht nur im Block am Ende (R66–R71).*

---

## Leseprotokoll (27.4, R56 (b)) — zugleich Anfangsbestand dieses Chats

**Vollständig gelesen** (Ablage, `project_read`; Registerdateien je mit Kopf Commit `ad351d5`, sha256 `a7496780…`, KOPIE):

| Datei | Grösse |
|---|---|
| Eröffnungstext mit Anfrage 02.10.b (Anhang der ersten Nachricht) | 115 Zeilen |
| `REGISTER_INDEX.md` | nicht gemessen |
| `REGISTER_KOPIE_ABSCHNITT_52.md` | 13,8 KB (nach Anfrage) |
| Abschnitte 15, 23, 24, 29, 48 | 25,9 / 29,2 / 25,5 / 4,7 / 28,7 KB (nach Anfrage) |
| Abschnitte 7, 51, 49, 4 | 3,7 / 22,4 / 5,1 / 6,0 KB (nach Anfrage) |
| Abschnitt 50 (ganz, wegen 50.1 und 50.2) | nicht gemessen |
| `FABLE_UEBERGABE_2026-10-01_neuer_chat.md` | nicht gemessen |
| Projekt-Erinnerung `preferences.md` | 9 241 B, Stand 2026-10-02 08:46 UTC — wie im Eröffnungstext genannt |
| Projekt-Erinnerung `ways-of-working.md` | 2 232 B, Stand 2026-10-01 19:51 UTC — wie genannt |

Zur Übergabe: Verlangt war nur der Codeblock. Das Lesewerkzeug liefert die Datei ganz; den Rest (Kopf, „Warum der Text so gebaut ist“, „Was der steuernde Chat misst“) habe ich damit gesehen und für keine Entscheidung verwendet.

**Nur als Ausschnitt:** nichts.

**Nicht gelesen:** alle übrigen Registerabschnitte — darunter 16 (16.6, 16.7), 21, 25, 33, 34, 35, 37, 40, 41, 43. Was ich von ihnen sage, kenne ich nur aus dem Wortlaut der gelesenen Blöcke und aus dem Index; im Registerblock steht es deshalb als Voraussetzung. Ebenfalls nicht gelesen: `ARBEITSWEISE.md` (22.11 kenne ich aus Nr. 4 des Eröffnungstexts, nicht im Wortlaut), `UEBERGABE.md`, `FABLE_DIALOG_INDEX.md`, die früheren Antworten und Anfragen, `BACKLOG.md`, `BACKLOG_ENTSCHEIDUNGEN.md`, alle `ERGEBNIS_*`, `docs/belege/`, `ergebnisse/`, Trade-Listen, Code. Die gesperrten Erinnerungsdateien (`overview.md`, `methodology-and-learnings.md`, `dashboard-roadmap.md`, `index.md`, `areas/…`) habe ich nicht geöffnet.

**Ohne mein Zutun geladen (Plattform):** kontoweit `profile.md` und `preferences.md` (Rolle, Ablageform; keine Ergebnisse); die Liste der Erinnerungsdateien mit je einer Beschreibungszeile, auch der gesperrten (Beschreibung, kein Inhalt); die Dateiliste der Ablage (87 Namen, darunter `BACKLOG*.md` und `ERGEBNIS_*` — Namen, kein Inhalt).

**Kein Helfer, kein Suchlauf** (`project_search` nicht benutzt). **Mechanik:** ein Skript für die Ampel (Sitzungsprotokoll), eines für Eszett-Zählung, Bytes und md5.

**Grössen, die an 27.1 grenzen** — im Register gelesen (27.3), für keine Entscheidung verwendet, hier nur mit Ort:

- 24.6: ereignisweiser und täglicher Drawdown je Bot und Falte auf den TB-24-Listen (heutige Parameter), Exposure-Spannen zweier Bots.
- 23.4: Benchmark-Drawdowns und `DD_Toleranz` je Bot in drei Fassungen; 4.4: Benchmark-Tabelle bei 50 % Exposure.
- 15.4: P95 der Haltedauer und Positionszahl von `t3_supertrend`; 15.6: gefundene Trades je Jahr (ein Bot genannt, Spanne der übrigen).
- 15.5: Symbolzahlen je Falte.

Weitere Grössen nach 27.1 kennt der Verfahrensprüfer nicht.

---

## Teil 0. Kenntnis

1. Zwölf Marken aus TB-130: zur Kenntnis; nach 52 und Index (Abschnitt 7) trägt jede der sieben, kein Widerspruch.
2. Voraussetzungen aus 02a: zur Kenntnis; die zweite zu R64 wird mit R66 (d) eine Wache im Lauf.
3. Marke an 25.2: zur Kenntnis (25 nicht gelesen); die Reihenfolge am Ort folgt 34.3, die Zeit steht in der Marke.
4. `--marken` zählt zwei Zitatzeilen mit: Handwerk.

---

## Teil 1. Antworten

### Frage 1 (a) — einverstanden

Die Tagesreihe führt die Tage vor dem ersten Handelbar-Tag, flach mit Rendite 0 und Exposure 0. Grund: 29.3 (der Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte), 1a (flache Tage stehen mit 0 in der Reihe), 2a (jeder Handelstag gehört zu seiner Falte). Deine Neigung trifft, auch im Grund.

Dazu gehört eine Lücke, die 23.3 selbst benennt: Fables zweite Fassung band den Benchmark an einen Kalender des Kapitalpfads, „den es nicht gibt“. R66 (a) gibt der Tagesreihe diesen Kalender. Für Krypto sind es Kalendertage (15.4, Anmerkung 1); für Aktien steht der Kalender im Block als Voraussetzung.

### Frage 1 (b) — anders, weil der Wortlaut den Sharpe auf den Kapitalpfad stellt und das Register Nichtteilnahme dort schon als 0 führt

Der Falten-Sharpe läuft über **alle Tage der Tagesreihe in der Falte**. Vier Gründe, alle aus dem Text:

1. **1c** rechnet „aus den täglichen Netto-Renditen des Kapitalpfads“, je Falte, ohne Einschränkung. 2a ordnet jeden Handelstag seiner Falte zu, 29.3 lässt den Pfad am 1. Januar beginnen.
2. **3a** sagt für genau diesen Fall, was gilt: „Symbole ohne Historie in einer Falte tragen 0 Trades und 0 Rendite bei.“ 15.5 (Lesart A) wiederholt es für Tage vor vollem Vorlauf: Das Symbol „trägt für diese Tage 0 bei“. Sind alle Symbole ohne Historie, ist der Tag flach. Für die Selektionsstatistik ist Nichtteilnahme im Register ein Wert, kein Ausschluss — wie bei 1c und 5.1 Nr. 8 (kein Trade ⇒ Sharpe 0).
3. **23.2, Grund 2** trägt die Verallgemeinerung nicht. Dort entsteht Alpha, weil zwei Reihen verglichen werden und eine davon Tage hat, die der anderen nicht offenstanden. Der Sharpe hat eine Reihe. Führende Nullen dämpfen ihn zur Null hin, mit erhaltenem Vorzeichen; sie erzeugen keine Grösse.
4. **24.1 und 24.2** tragen die Übertragung nicht. 24.1 spricht von der Bewertungsachse und geht, wie du selbst schreibst, vom Sharpe zum Drawdown. Die Zeitachse in 24.2 ist für den Drawdown wirkungslos, solange der Bot an Tagen ohne Benchmark-Tag flach ist: Ein Tag mit Rendite 0 bewegt den Pfad nicht (23.4, Wirkung 3). Ein Satz, der an seinem Ort nichts ändert, kann nicht der Grund für eine Festlegung sein, die am Sharpe etwas ändert.

Die Trennlinie steht in R66 (c): Auf den Benchmark-Tagen stehen die Grössen, die den Bot gegen den Benchmark stellen oder dessen Argument sind (Drawdown der Nebenbedingung, mittlere Exposure, 7 (c), 8.1). Die Selektionsstatistik stellt Zellen gegeneinander und gegen 0 und steht auf dem Kapitalpfad. R64 bleibt damit unberührt.

**Bekannte Richtung der Wirkung, nicht Grund** (Rechnung, nicht gemessen): Über alle Tage ist der Falten-Sharpe dem Betrag nach nie grösser als über die Benchmark-Tage allein; das Vorzeichen bleibt. Die Grösse ist für die Entscheidung ohne Belang (Bauart 24.3).

**Als kritischer Berater, ohne Gewicht für die Entscheidung:** Die andere Lesart hätte in einer Falte mit wenigen Benchmark-Tagen einen Sharpe aus wenigen Werten mit vollem Gewicht in den Faltenmedian gestellt. Das ist die Stelle, an der 23.2 Rauschen erwartet.

### Frage 2 — einverstanden

Registertext, Wache im Erzeuger, Prüfung in der Abnahme; `auswertung.py` bleibt dafür zu. Grund: R33 (ein Mangel der Datei ist ein Befund über den Erzeuger, kein Ausgang), R39 (die Feldliste ist Registertext), R46. Eine Ergänzung zu deiner Neigung: nicht nur „kein Feld leer“, auch **jeder Zahlenwert endlich** — ein „nan“ ist kein leeres Feld und verdirbt das Mittel genauso. R67.

### Frage 3 — einverstanden, mit einer Erweiterung

R64 (a) gilt, und die Tage beginnen an `bestaetigung_ab_effektiv` der Zelle. Grund: R37 lässt den Erzeuger diesen Tag „für jede Zelle“ bestimmen; das hat nur Sinn, wenn die Zeile jeder Zelle darauf steht, denn der Gewinner ist beim Erzeugen nicht bekannt. Dein Gegengrund trifft die Spanne, nicht die Zeile: Die Spanne bleibt, was 35.1 sagt.

Die Erweiterung: Das gilt für **alle Grössen der Zeile**, nicht nur für die Exposure. Sonst trüge eine Zeile (R33) zwei Zeiträume. Und im Deckelfall folgt die Exposure derselben Attribution wie die Rendite (R60 (c): eine Rechnung). R68.

### Frage 4 — einverstanden in der Sache, anders im Schnitt

**Sache:** Register-Code-Widerspruch nach 25c (1), aufgelöst zugunsten von R39 durch eine Öffnung vor dem Tag. R39 wird nicht berichtigt, weil sein Grund in der Sache liegt: Die Benchmark-Reihe unterscheidet sich je Bot (23.3; Schranken je Bot), eine Datei je Markt kann sie nicht tragen. Deine Erwägung „der Erzeuger könnte je Markt schreiben“ scheitert daran.

**R64 (e):** Deine Lesart trifft. „Für nichts davon“ meint, was R64 regelt; den Dateinamen regelt R39, R64 (a) zitiert ihn nur. 52.4 liest den Satz zu weit. R69 (c) gibt das „lies“.

**Anders im Schnitt, weil** diese Öffnung nicht die einzige ist. R36 (zwei Drawdown-Spalten, Nachrechnung mit Ausgang 2), R37 (`bestaetigung_ab_effektiv`), R34 (`zellenbericht.csv`) und R55 („nächste planmässige Öffnung“) verlangen sie schon. Der Dateiname gehört in dieselbe planmässige Öffnung, nicht in eine eigene an „dieser einen Stelle“. Ob ein Auftrag oder mehrere, ist Handwerk; ich empfehle einen, weil jede Öffnung Hash-Übergang, Abbild und Nachweis kostet. Ebenfalls Handwerk: Die Öffnung liegt vor der Abnahme nach R46, weil die durch die ganze Kette läuft.

### Frage 5 — einverstanden, mit anderem Grund

7 (c) trägt keine Marke zu R64. „Nur Quelle des Grundes“ trifft aber nicht ganz: R64 (a) nennt 7 (c) als Geltungsbereich. Der tragende Grund ist der Fall, den R61 (b) schon entschieden hat: **R54 an 7 (c)** — ein Block, dessen „lies“ einem anderen Ort gilt und der 7 (c) nur als Geltungsbereich nennt, bleibt dort ohne Marke und wird vom Index geführt. Der Unterschied zu 4.2: Dessen Wortlaut nennt die Tage nicht, R64 gibt sie ihm; Abschnitt 7 nennt seine Tage selbst. R70, dort auch die Marken zu dieser Antwort.

### Frage 6 — einverstanden, mit genauerem Wortlaut

„Je Falte“ ist zu berichtigen. Der Grund steht schon im Register: 23.4, Wirkung 3, zählt unter C_lit **vier** Falten mit je einem Tag mehr, nicht jede Falte. Dein Wortlaut „ersten Kurstag des Rahmens“ ist mir zu nah am ersten Kurstag der Datei; der Rahmen beginnt nach dem Schnitt am Handelbar-Tag. R71 schreibt deshalb „den ersten Kurstag ab dem frühesten Handelbar-Tag des Bots“. Die Voraussetzung (Test am Code, Kurslücken) übernehme ich in den Block und erweitere sie um den Fall nach dem letzten Kurs eines Symbols.

---

## Kurz

| Frage | Antwort | Block |
|---|---|---|
| 1 (a) | einverstanden: Tagesreihe ab 1. Januar der ersten Falte, flach mit 0 | R66 (a) |
| 1 (b) | **anders:** Falten-Sharpe über alle Tage der Tagesreihe in der Falte | R66 (b), (c) |
| 2 | einverstanden; dazu „endlich“ | R67 |
| 3 | einverstanden; gilt für alle Grössen der Zeile | R68 |
| 4 | Sache einverstanden; Schnitt anders: eine planmässige Öffnung | R69 |
| 5 | einverstanden, Grund ist der Fall R54 an 7 (c) | R70 |
| 6 | einverstanden, genauerer Wortlaut | R71 |

Für den Zellen-Erzeuger heisst das: Die Tagesreihe führt jeden Handelstag vom 1. Januar der ersten Selektionsfalte bis zum Ende der Bestätigungsperiode; an Tagen ohne Benchmark-Tag stehen Rendite 0 und Exposure 0, und der Erzeuger prüft das im Lauf.

**Umzugsampel:** 🟡 · gemessen 286 709 (Sitzungsprotokoll, letzter Eintrag vor dem Schreiben dieser Datei; die Grundlast liess sich nicht messen, der erste Eintrag trägt 0) · 1 Tagesanfrage · die nächste Anfrage geht an einen neuen Chat.

---

## Unsicher

1. **Aktienkalender (R66 (a)).** Ich habe keinen Registersatz gelesen, der den Handelskalender der Aktien-Tagesreihe festlegt. Der Block nennt „Kurstage im Snapshot“ als Voraussetzung. Lässt sich das nicht eindeutig bestimmen, kommt es zurück.
2. **Gibt es den Fall überhaupt?** Ob der registrierte Faltenplan (33.2) eine Falte enthält, in der der Benchmark nicht an allen Tagen definiert ist, habe ich nicht gelesen (33 und 25 nicht geöffnet). R66 gilt unabhängig davon.
3. **Eingefrorener Code zum Sharpe (R66 (e)).** Ich weiss nicht, ob `kennzahlen.py` oder `auswertung.py` den Falten-Sharpe irgendwo aus der Tagesreihe nachrechnet und auf welchen Tagen. Weicht das von R66 (b) ab, ist es ein Widerspruch nach 25c (1) und kommt zu mir, bevor R66 eingetragen wird.
4. **16.6 nicht gelesen.** R68 stützt sich auf R37 im Wortlaut und auf 2d in der Fassung 15.4 („Tage im Embargo gehören zu keiner Periode“). Ob 16.6 diesen Satz hält, steht als Voraussetzung im Block.
5. **Deckelfall in R68 (c).** Wie die Rendite einer nicht zählenden Position aus der Tagesreihe herausgerechnet wird, regelt R37 nicht im Einzelnen. R68 (c) bindet nur die Exposure an dieselbe Attribution.
6. **Umfang der planmässigen Öffnung (R69 (b)).** Dass `auswertung.py` heute nur `kapital_drawdown_pct` führt und `bestaetigung_ab_effektiv` nicht kennt, steht in 50.1 und in deiner Anfrage. Für `zellenbericht.csv` ist es Voraussetzung.
7. **37.3, 40.7, 25c (1), 34** zitiere ich nach dem Wortlaut der Blöcke, die sie anführen, nicht nach eigener Lektüre.
8. **Die Ampel** steht nahe an 🔴. Ich habe deshalb 35 und 34 nicht mehr geöffnet. Hängt für dich an einem der beiden Wortlaute etwas, ist das eine Frage für den nächsten Chat.

---

## Registerblock — zeichengleich kopierbar, nummeriert (ab R66)

```
R66 — Präzisierung zu Registertext 1c (15.3 (c)) und Ergänzung zu R64 (e) (52.2) (Kalender der Tagesreihe; Tage des Falten-Sharpe). (a) Die Tagesreihe einer Zelle führt jeden Handelstag des Kapitalpfads, vom 1. Januar der ersten Selektionsfalte des Bots (29.3) bis zum Ende der Bestätigungsperiode (35.1), ohne Lücke. Handelstage sind bei Krypto die Kalendertage (15.4, Anmerkung 1), bei Aktien die Kurstage des Marktes im Snapshot. Ein Tag, an dem die Zelle keine Position hält, steht mit Rendite 0 und Exposure 0 in der Reihe (1a), auch ein Tag vor dem ersten Handelbar-Tag des Bots. [Voraussetzung, zu messen: dass sich die Kurstage des Aktienmarktes aus dem Snapshot eindeutig bestimmen lassen, als die Tage, an denen mindestens ein Symbol der Universumsdatei des Bots (3a) einen Kurs trägt, und dass jeder Benchmark-Tag des Bots ein solcher Tag ist; trifft es nicht zu, wird gemeldet, nicht eingetragen.] (b) Der Falten-Sharpe nach 1c wird über alle Tage der Tagesreihe gerechnet, die in die Falte fallen (2a; halboffen wie im Faltenplan), nicht nur über die Tage, an denen der Benchmark definiert ist. Ein Tag ohne Benchmark-Tag geht mit Rendite 0 ein. Dasselbe gilt für den Sharpe in der Zeile der Bestätigungsperiode, ab dem Tag nach R68. (c) Auf den Tagen des Benchmarks stehen die Grössen, die den Bot gegen den Benchmark stellen oder dessen Argument sind: der Drawdown der Nebenbedingung (24.2, R36), die mittlere Exposure (R64), Beta-Bereinigung und Calmar-Vergleich (7 (c)), das Zufalls-Timing (8.1). Die Selektionsstatistik stellt Zellen gegeneinander und gegen 0; sie steht auf dem Kapitalpfad. R64 bleibt unberührt. (d) Führt die Tagesreihe einer Zelle an einem Tag, der kein Benchmark-Tag des Bots ist, eine Rendite ungleich 0 oder eine Exposure ungleich 0, ist das ein Befund über den Erzeuger, kein Ausgang (Bauart R33); ausgenommen ist der Tag aus der Tatsachennotiz zu 23.3 in der Fassung R71. Der Zellen-Erzeuger prüft das im Lauf für jede Tagesreihe und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. Die zweite Voraussetzung aus R64 wird damit im Lauf geprüft. (e) [Voraussetzung, vor dem Eintrag zu messen: ob Code auf der Sperrliste oder im Laufbereich den Falten-Sharpe aus der Tagesreihe bildet oder nachrechnet, und über welche Tage; rechnet er über andere Tage als (b), ist das ein Register-Code-Widerspruch nach 25c (1) und wird gemeldet, nicht eingetragen.]
Quelle des Grundes: 1c im Wortlaut („aus den täglichen Netto-Renditen des Kapitalpfads“, je Falte, ohne Einschränkung); 1a („Flache Tage stehen mit Rendite 0 in der Reihe“); 2a („Jeder Handelstag gehört zu der Falte, in die sein Datum fällt“); 29.3; 3a („Symbole ohne Historie in einer Falte tragen 0 Trades und 0 Rendite bei“) mit 15.5, Lesart A („trägt für diese Tage 0 bei“); 1c mit der Tatsachennotiz zu 1c (kein Trade: Sharpe 0; Nichtteilnahme ist in der Selektionsstatistik ein Wert); 23.2, Grund 2 (der Schaden dort entsteht aus dem Vergleich zweier Reihen; der Sharpe hat eine); 24.1 und 24.2 (Bewertungsachse; die Zeitachse ist für den Drawdown genannt und bewegt ihn unter (d) nicht: 23.4, Wirkung 3); 23.3 (zur Entstehung: der Kapitalpfad hatte keinen Kalender); R33; R46. Bekannte Richtung der Wirkung, nicht Grund: Über alle Tage der Falte ist der Falten-Sharpe dem Betrag nach nie grösser als über die Benchmark-Tage allein, bei gleichem Vorzeichen (Rechnung des Verfahrensprüfers); die Grösse ist nicht gemessen und für die Entscheidung ohne Belang (Bauart 24.3). Kein Ergebnis.

R67 — Registertext, Ersteintrag, Ergänzung zu R39 (48.7) (Eindeutigkeit und Vollständigkeit der Reihen). In jeder Tagesreihe (tagesreihen/<zelle>.csv) und in jeder Benchmark-Tagesreihe (benchmark_tagesreihen/<bot>.csv) ist datum eindeutig, kein Feld leer und jeder Zahlenwert endlich. Ein flacher Tag trägt 0, nie nichts (1a). Ein Verstoss ist ein Befund über den Erzeuger, kein Ausgang (Bauart R33): Der Zellen-Erzeuger prüft jede dieser Dateien im Lauf, nachdem er sie geschrieben hat, und endet sonst mit 2. Die Abnahme nach R46 prüft die Wache mit Gegenprobe, je für ein doppeltes Datum, ein leeres Feld und einen nicht endlichen Wert; der registrierte Lauf trägt die Wache selbst. auswertung.py wird dafür nicht geöffnet. Für zellen.csv gilt R33.
Quelle des Grundes: R33 („Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang“; „nie nichts“), R39 (die Feldliste jeder Ausgabe ist Registertext), R64 (c) (Bauart), R46, die Messung in 52.4 (auswertung.py behandelt und prüft weder fehlende Werte noch doppelte Daten). Kein Ergebnis.

R68 — Präzisierung zu R37 (48.5) und zu R64 (52.2) (Zeile der Bestätigungsperiode in zellen.csv). (a) Die Zeile der Bestätigungsperiode (R33) trägt für jede Zelle die Bestätigungsstatistik, die R37 (i) für den Gewinner beschreibt. Alle Grössen dieser Zeile stehen auf den Tagen ab bestaetigung_ab_effektiv der Zelle bis zum Ende der Spanne (35.1). Die Spanne bleibt, was 35.1 sagt; ihre Tage vor diesem Tag gehören zu keiner Statistik. (b) R64 (a) gilt für die mittlere Exposure dieser Zeile: Mittel über die Benchmark-Tage des Bots innerhalb der Tage nach (a). (c) Was nach der Attribution je Position (R37) in die Rendite der Zeile nicht eingeht, geht auch in ihre Exposure nicht ein; beide kommen aus einer Rechnung (R60 (c)). (d) Die mittlere Exposure der Zeile ist Bericht; kein Urteil liest sie. [Voraussetzung, zu messen: dass 16.6 den Satz „Tage im Embargo gehören zu keiner Periode“ aus 2d (15.4 (d)) nicht aufhebt; dass kein Urteil in auswertung.py die mittlere Exposure der Bestätigungsperiode liest.]
Quelle des Grundes: R37 („Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle“), R33 (genau eine Zeile je Zelle und Falte, Bestätigungsperiode eingeschlossen), 2d (15.4 (d)), R60 (c), R64 (a). Kein Ergebnis.

R69 — Auflösung des Widerspruchs zwischen R39 (48.7) und auswertung.py (Name der Benchmark-Datei); Präzisierung zu R64 (e) (52.2) und R60 (c) (51.5). (a) Dass auswertung.py benchmark_tagesreihen/<markt>.csv liest und R39 <bot>.csv verlangt, ist ein Register-Code-Widerspruch nach 25c (1). Er wird zugunsten von R39 aufgelöst; R39 wird nicht berichtigt. Die Benchmark-Reihe unterscheidet sich je Bot (23.3; 16.7 (b)); eine Datei je Markt kann sie nicht tragen. (b) Vor dem signierten Tag liest auswertung.py die Datei unter dem Namen des Bots. Das ist eine beauftragte Änderung nach 37.3 mit Einzelfreigabe des Betreibers, Hash-Übergang, neuem Abbild und einem Nachweis mit Gegenprobe (40.7). Sie gehört zur planmässigen Öffnung von auswertung.py, die R36 (zwei Drawdown-Spalten, Nachrechnung), R37 (bestaetigung_ab_effektiv), R34 (zellenbericht.csv) und R55 (Umbenennung) verlangen. Beispieldaten und Tests, die den Namen je Markt schreiben oder lesen, folgen in derselben Änderung. [Voraussetzung, zu messen: dass auswertung.py heute zellenbericht.csv nicht liest.] (c) In R64 (e) lies „auswertung.py wird für nichts davon geöffnet“ als „für nichts, was dieser Block in (a) bis (d) regelt, wird auswertung.py geöffnet“. „Dafür“ in R60 (c) bindet ebenso nur die Gleichheit der zwei Träger. Die Öffnung nach (b) berührt beides nicht.
Quelle des Grundes: R39 mit seinem Grund (23.3: die Symbole, die der Loader des Bots handelbar macht; 16.7 (b): Schranken je Bot; 37.5 (2)), 25c (1), 37.3, R45 (Bauart einer beauftragten Änderung), R36, R37, R34, R55, 50.1 und 50.2 (Stand des Vertrags), 23.5 (ein Name, der etwas anderes verspricht als der Inhalt). Kein Ergebnis.

R70 — Marken zu R64 (7 (c)) und zu R66 bis R71. (a) 7 (c) trägt keine Marke zu R64. Abschnitt 7 nennt seine Tage selbst („gemeinsame Tage“, „über dieselben Tage“); R64 gibt das „lies“ R48 (d) und R60 (c), nennt 7 (c) als Geltungsbereich und bestätigt in (b) den Code, nicht den Wortlaut von 7. Ein Ort, den ein Block nur als Geltungsbereich einer Regel nennt, deren „lies“ einem anderen Ort gilt, bleibt ohne Marke und wird vom Index geführt, wie R54 an 7 (c) (R61 (b)). 4.2 trägt die Marke zu R64, weil sein Wortlaut die Tage nicht nennt und R64 sie ihm gibt. (b) Indexzeile an 7 (c): mittlere Exposure des Gewinners, Tage nach R64 (a), (b) und (d). (c) Marken zu dieser Antwort, der alte Satz bleibt zeichengleich: 15.3 (c) — PRÄZISIERT durch R66. 52.2 (R64) — ERGÄNZT durch R66 (zu (e)), PRÄZISIERT durch R68 und durch R69, Unterpunkt (c). 48.5 (R37) — PRÄZISIERT durch R68. 48.7 (R39) — ERGÄNZT durch R67 und R69. 51.5 (R60) — PRÄZISIERT durch R69, Unterpunkt (c). 23.3, Tatsachennotiz zu 3b (c) — BERICHTIGT durch R71, direkt unter dem berichtigten Satz (34.3). Ohne Marke bleiben 24.2, 29.3, 8.1 und 7 (c) zu R66 (Geltungsbereich oder Quelle des Grundes).
Quelle des Grundes: R61 (b), erster und zweiter Satz, und die Zeile „R54 an 7 (c)“; R65 (a); 34 (nach der Wiedergabe in R61 und R65); Wortlaut von Abschnitt 7 und von 4.2. Kein Ergebnis.

R71 — Berichtigung der Tatsachennotiz zu 3b (c) in 23.3 (welcher Tag ausgelassen wird). „Die Umsetzung lässt den ersten Kurstag je Falte aus, weil pct_change dort keine Rendite liefert“ lies „Die Umsetzung lässt den ersten Kurstag ab dem frühesten Handelbar-Tag des Bots aus, weil pct_change dort für kein Symbol eine Rendite liefert; das geschieht einmal je Bot, nicht in jeder Falte, und der Tag fällt nur dann in eine Falte, wenn er nicht vor der ersten Falte des Bots liegt“. „Höchstens ein Tag je Falte“ bleibt als Schranke richtig; die übrigen Sätze der Notiz bleiben. R64 (a) und R66 (d) meinen diesen Tag. [Voraussetzung, vor dem Eintrag zu messen, durch einen Test am Code und nicht durch Lesen: dass bh_tagesrenditen ausser diesem Tag keinen Tag weglässt, an dem mindestens ein Symbol des Bots handelbar ist, auch nicht an einer Kurslücke und nicht nach dem letzten Kurs eines Symbols; weicht der Test ab, wird gemeldet, nicht eingetragen.]
Quelle des Grundes: 23.4, Wirkung 3 (unter C_lit ändern sich vier Falten um je einen Tag, „der Tag des ersten Kurses, an dem noch keine Rendite vorliegt“, nicht jede Falte); 23.5 („die erste Tagesrendite eines Symbols ist die vom Handelbar-Tag auf den Folgetag“); die Lesung von benchmark.py durch den Helfer des steuernden Chats (Anfrage 02.10.b, Frage 6; vom Verfahrensprüfer nicht gelesen). Kein Ergebnis.
```
