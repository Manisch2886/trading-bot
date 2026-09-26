# FABLE_ANTWORT 2026-09-26a — TB-109 bis TB-113 angenommen; Entscheidung 8 entfällt (16.4 (g)–(m) steht — meine Berichtigung); `None` bestätigt (neunter Fall); dreizehn Antworten; ein Registertext vor dem Tag aus der Nullbefund-Skizze; Registerblock am Ende

*Bezug: `FABLE_ANFRAGE_2026-09-26a_tagesanfrage_tb109_bis_113.md`. Erste gesammelte Tagesanfrage. Registertext steht als eigener Block am Ende, nummeriert R1–R8, zeichengleich kopierbar.*

**Leseprotokoll dieses Chats, Stand jetzt:** wie 25f; dazu ANFRAGE 26a (Anhang) und ein Suchtreffer in `REGISTER_KOPIE_2026-09-24_teil1_0_bis_23.md`, Abschnitt 16.4 (h)–(m) samt „Prüfung vor dem Tag" und dem Hinweis auf 16.11 Zeile 3. Die ERGEBNIS-Dateien TB-109–113 liegen im Repo, nicht in der Ablage; ich kenne sie aus eurer Kurzfassung. `AF-F0_BESTANDSAUFNAHME_2026-09-26.md` nicht geöffnet (zur Kenntnis, nach dem Tag). Ergebnisgrössen nach 27.1: keine. Die Aussage „an allen 10 Stellen ist die Liste nicht leer" nehme ich als Regelbetriebsmessung, wie ihr sie einordnet.

---

## 1. Kenntnisnahme — fünf Aufträge

**TB-109:** zehn Stellen ⇒ 2 im Modus, ohne Modus zeichengleich, 34 neue Proben; Gegenprobe zählt 24 = 14 + 10, weist 16 reguläre Blockenden aus, zwei Mutationen beissen; Ablagen im `finally`; `$TMPDIR` vorher = nachher. **Angenommen.** Der A3-Befund (kein Cron-Lauf erreicht eine der zehn Stellen) ändert nichts an der Regel — dieselbe Lage wie bei (c) in 25e.

**TB-110:** Register 43 mit 15 Einträgen, 31 Zitate `diff` rc 0, sechs Marken, keine in 10, Tatsachennotiz zu Punkt 4 in 43.1 statt in 10 — richtig, Abschnitt 10 ist die Sperrliste, nicht ihr Kommentar. **Angenommen.**

**TB-111:** Prüfansicht mit `paths.DATA_DIR`, `TB30A_BASE_DIR` unter dem Modus ⇒ 2 an allen drei Eingängen, Lesehaken 0 Zugriffe unter der Ersatzwurzel; `Abbruch` ⇒ 2 an zwölf Stellen zeichengleich, vier Brüche mit `cmp`-gleicher Ausgabe. **Angenommen — mit dem Befund A2b als dem wichtigsten Teil:** `_paths()` lud `paths.py` aus der Ersatzwurzel, und die Prüfansicht endete deshalb mit **1** statt 2. Das ist die Klasse aus 25c (1): Ein Werkzeug, das unter dem Modus einen falschen Rückgabewert liefert, nicht weil es lügt, sondern weil es seinen Nachbarn am falschen Ort sucht. Dass die zweite Änderung nötig war, um B2 zu erfüllen, ist kein Überschreiten der Freigabe — B2 war die Freigabe; ohne die Änderung wäre sie nicht erfüllbar gewesen. Tatsachennotiz genügt, sie steht in 44.

**TB-112:** 19 über den Laufbereich, 15 Einträge als Einzeldateien (nicht Ordner — der Grund mit `ergebnisse/` ist gemessen, gut), `REGISTRIERTE_PROTOKOLLE` als `:(exclude)`, 26 Proben, jede der zwölf Dateien einzeln ⇒ 2, Lese-Audit 0 `.py` ausserhalb der Liste. **Angenommen.** Der A1-Befund (uncommittete Änderung in `benchmark.py` lief unter dem Modus durch) war der Grund für E2, und er ist jetzt gemessen, nicht mehr vermutet. db-Sicherung läuft (O6 erledigt).

**TB-113:** Merge ohne gemeinsam geänderte Datei, alles nachgemessen auf dem zusammengeführten Stand, Register 44 nur Tatsachennotizen. **Angenommen.** 22.1 (`--effort high`) und 22.9 (Sitzung vor dem Einfügesatz) zur Kenntnis.

**Bündel 1 aus 25f ist vollständig; der 19-Auftrag ist vollzogen.** Von der Liste in 25f A2 bleiben: Erzeuger (3), TB-30b Posten 3/4/5 (4), Stufe IV (5), Block-4-Reste (6), Stufe VI (7).

---

## 2. Die zwei Messungen zu 25f — und meine Berichtigung

**(a) Budget je Zelle steht im Register: 16.4 (g)–(m).** Ich habe es nachgesehen (Suchtreffer, Teil 1 der Kopie): (h) Gleichteilung aktiver Zellen, (i) Stufenfaktor 0/1/2, (j) kein Übertrag, (k) Umverteilung nur durch Zulassung, (l) 80/20, (m) Leiter-Skript mit `m_b`. Dazu „Prüfung vor dem Tag": 3⁹ = 19 683 Stufentabellen, und der Hinweis, dass das Skript noch nicht existiert (16.11, Zeile 3).

**Berichtigung meines Satzes in 25f A2** (*„Ich habe im Register 0–40 keinen Abschnitt gefunden, der das ausdrücklich vollzieht"*): Der Abschnitt steht, und ich hatte Teil 1 gelesen. Die Voraussetzung war als solche markiert — das rettet den Satz nicht: „nicht gefunden" hiess hier „nicht erinnert", und ich habe aus dem Gedächtnis gesucht statt im Text. Das ist C1 (*„Fundstellen nur nennen, wenn sie vorliegen. Sonst steht ausdrücklich ‚aus dem Gedächtnis' dabei"*), auf mich angewandt. **Regel für mich:** Bevor ich sage, etwas stehe nicht im Register, suche ich im Text (Suchtreffer), nicht in der Erinnerung — und schreibe „nicht gefunden bei Suche nach …" mit dem Suchwort. **Entscheidung 8 entfällt.** P1 ist damit kein Amendment, sondern Stufe IV (Leiter-Skript), wo es in 25f A2 Nr. 5 ohnehin stand.

**(b) N = 653.** Das Versuchsregister (TB-29) zählt dedupliziert, einschliesslich Forschungsraster, und benennt in 3.4 und 5.1–5.4, was nicht gezählt und nicht rekonstruierbar ist — darunter 5.4 „verworfene Varianten ohne Bericht". Die Beschriftung, die A4.4 (b) verlangt, existiert also, und Register 9 verweist auf das Versuchsregister. **Einverstanden: vor dem Tag nichts; nach dem Tag in Register 9 ein Verweis auf Abschnitt 5 des Versuchsregisters** (R8 d). Eine Folge für die Lesart, die ich festhalte: Wegen 5.4 ist N = 653 eine **Untergrenze**; der berichtete Wert 2 × N_nominal (Register 8) ist deshalb nicht Sensitivität, sondern die ehrlichere der drei DSR-Zeilen. Das ist eine Lesehilfe für den Bericht, kein Registertext.

Die drei ungemessenen (D3 Adjustierung, TB-85-Kette, geschlossene Kerze) bleiben Messbitten; D3 und die Kerze sind Verfahrensmessungen nach 27.2 und dürfen vor dem Tag gemacht werden — die Kerze **sollte** es, weil sie eine Tag-Vorbedingung berührt (Registertext zur Entscheidungskerze steht auf der Sperrliste; ob alle neun ihn einhalten, ist eine Sauberkeitsfrage wie 19).

---

## 3. Die dreizehn Antworten

**(1) Stummel: `None` bestätigt. Und ja, der durchlaufene Zweig wird geprüft — als Beifang.** Der Stummel soll das Werkzeug so laufen lassen, wie TB-52 lief; eure Messung zeigt, dass nur `None` das tut (9 von 9 Ordner), während `False` den Modus-Zweig nimmt und das Werkzeug trotzdem 0 Unterschiede meldet — ein Werkzeug, das grün ist und den falschen Zweig misst, ist A5. Mein `lambda: False` in 25e 3 war ein Beispiel, das ich nicht gemessen habe — **neunter Fall** meiner Klasse (zweite Selbstregel: *„Auch Beispiele und Belegverweise sind Voraussetzungen, wenn ich sie nicht gemessen habe"*). 43.3 wird von „vorläufig" auf „bestätigt" gesetzt (R1). Die Zweigprüfung (angelegte Ordner im Wegwerfbaum zählen) ist genau die Wache, die den Fehler sichtbar gemacht hätte; Beifang des nächsten Bündels, kein Auftrag.

**(2) Reichweite von (iv): die gebaute Lesart ist die gemeinte.** 25b hat Klasse (iv) mit drei Bedingungen definiert — angelegt mit `mkdtemp`, **vom Lauf selbst gelesen**, entfernt oder im Beleg. Das Selbstlesen des Ergebnis-JSON ist Bestandteil der Klasse, nicht Ausnahme davon; 25e 3 (b) hat nur den Teil benannt, der im Audit falsch stand (die Verzeichnis-Öffnungen), nicht die Klasse verkleinert. Dass (i) ausserhalb damit von 31 auf 11 fällt, ist die richtige Zahl, und nach (4d) fällt sie weiter: die neun TB-24-Listen und `messgroessen.json` sind registrierte Eingaben (dann (i) *innerhalb*), die Tempfile-Probe ist Umgebung — **(ii)**, Tatsachennotiz, wie ihr neigt (R2). Damit ist „0 Zugriffe ausserhalb" (25a D2) erstmals erreichbar, nicht nur gefordert.

**(3) Grenze der Gegenprobe: das Zweite — Abnahmebedingung des Erzeugers, mit einer Zählung.** Die Gegenprobe prüft die Klasse „vorzeitiger Ausgang im `__main__`"; `main()`-Funktionen mit `return 0` ohne Ausgabe sind eine andere Klasse, und ihr Ort ist der Erzeuger, weil er der einzige Lauf-Typ ist, der Zellen schreibt. Der Satz aus 25e (2) wird Abnahmebedingung, und er bekommt eine prüfbare Form: **Zeilenzahl in `zellen.csv` = Zahl der Zellen des Rasters, für jede Zelle genau eine Zeile, Zellen ohne Trades mit der Nullzeile** (R5 b). Eine fehlende Zeile ist dann ein Befund, kein stiller Ausgang.

**(4) Bestätigungen:** Entscheidung 8 entfällt (Abschnitt 2 (a)); Verweis N = 653 nach dem Tag (Abschnitt 2 (b)). Beides bestätigt.

**(4a) `datenstand(None)` im Modus ⇒ 2 — ja, Beifang der nächsten Öffnung.** Eine Funktion, die unter dem Modus ohne Pfad auf `BASE_DIR/data` fällt, ist A10-Klasse (24b), auch wenn heute jeder Aufrufer einen Pfad übergibt: Der Laufbereich wird am Tag gemessen, und ein künftiger Aufrufer ohne Pfad wäre ein stiller Rückfall. Kein eigener Auftrag (R5 c).

**(4b) Docstring `_abbruch_2` „endet mit 1" — Tatsachennotiz jetzt, Streichung mit der nächsten Öffnung.** Einverstanden. Dass der Satz stehen blieb, weil die Freigabe „sonst nichts" lautete, ist richtig gehandelt — eine Freigabe ist keine Einladung. Ein falscher Docstring in einer Sperrlistendatei ist ein Befund über die Datei, kein Befund über den Lauf (R8 a).

**(4c) `str(e)` ist `"2"`, Meldung in `e.meldung` — Tatsachennotiz genügt, mit einer Bedingung.** „Heute liest niemand `str(e)`" ist eine Messung über den Laufbereich; sie gehört in die Notiz mit dem Suchmuster, damit sie am Tag wiederholbar ist (R8 b). Eine bessere Form (`__str__` liefert die Meldung, der Code steht in einem Attribut) ist Handwerk für die nächste Öffnung, nicht für jetzt.

**(4d) Die neun TB-24-Listen: ins Abbild, Gruppe `eingefroren`.** Eure Neigung trifft, und der Grund ist die Klassentrennung aus 25b: E2 bindet **Code** an die Startprüfung, das Abbild bindet **Eingaben** an ihren Hash. Die Listen sind Herleitungsgrössen des Faltenplans (24c B1, TB-95) — Eingaben mit Hash, nicht Code-Pfade. Dass das Faltenplan-Abbild (33.3) eine Änderung *indirekt* fände, weil sich der Plan änderte, reicht nicht: Der Plan ist Ergebnis der Herleitung, die Listen sind ihre Eingabe, und der Nachweis (24c) will beides — die Eingabe bytegleich und gelesen (R3).

**(4e) Liste als Literal mit Gegenprobe; Abweichung der Tag-Messung ist Befund.** Einverstanden. Eine Liste, die der Tag-Commit aus der Messung erzeugt, wäre eine Wache, die sich aus dem prüft, was sie prüfen soll — B3-Klasse (bewegliche Referenz). Die Gegenprobe liest die Messdatei; am Tag wird neu gemessen; Ungleichheit heisst: Laufbereich hat sich geändert, Liste nachziehen **vor** dem Tag, nicht durch ihn (R4).

**(4f) Schlüssel-Muster: Tatsachennotiz, keine deutschen Wörter.** Einverstanden — Betrieb, nicht Lauf. Die Notiz nennt das Muster und die Tabelle `zustand(schluessel, wert)` mit ihrem gemessenen Inhalt (R8 c).

**(5) Wechselwirkung `herkunft.py` — einverstanden: keine Änderung jetzt, Abnahmebedingung des Erzeugers.** Bis dahin ist `herkunft.py` über die Sperrliste (Punkte 11/12) und das Abbild gebunden — am **committeten** Stand. Die Lücke ist genau eine: eine uncommittete Änderung im Arbeitsbaum, die kein Lauf-Typ lädt. Sie schliesst sich, sobald der Erzeuger `register()`/`commit()` ruft und die Tag-Messung das Modul findet. Die Abnahmebedingung lautet deshalb wörtlich: *„Die Laufbereichsmessung nach dem Einbau des Erzeugers enthält `herkunft.py`; `ARBEITSBAUM_PFADE` ist danach nachgezogen"* (R5 a).

**(6) Nullbefund-Skizze und Budget — die Skizze reicht, mit einer Ausnahme: ein Satz gehört vor den Tag ins Register.** Teil 1 der Skizze beschreibt richtig, was das Register schon sagt (Festlegung 12, 7.1, 16.4 (b), (j), (l)); nichts davon braucht einen neuen Eintrag. **Abschnitt 2 Nr. 3 („keine Rettungsanalysen") ist anders:** Das Register verbietet in 7.1, eine Schwelle zu ändern, und verlangt für die Rückkehr eine veränderte Hypothese. Es sagt aber nicht, was mit dem **Selektionsraum** nach dem Tag geschehen darf. Die Literatur nennt den Fall: Story-telling und Data Snooping nach dem Ergebnis sind zwei der sieben Backtest-Sünden (25f A4.1, AFML), und jede nachträgliche Rechnung auf den Zellen ist ein weiterer Versuch. Nach meinem Massstab aus 22e (*Registertext, der nach dem Tag noch geändert werden müsste, wäre ein Amendment → vor dem Tag*) gehört die Regel **vor** den Tag, weil sie am Tag danach schon gelten muss. Sie ist klein (R6), und sie macht die Messbitten aus 25f zu einer **registrierten Liste** (R7) — was nicht auf der Liste steht, ist ein Versuch und zählt in N des nächsten Durchgangs. Quelle des Grundes: Literatur und 7.1, kein Ergebnis. Der Rest der Skizze bleibt Skizze; ihr Abschnitt 3 (Anschluss) ist Planung und richtig so.

**Budget (W2):** Tabelle in Ordnung. Zwei Anmerkungen ohne Änderungsbedarf: „Server nur falls vorhanden" — der Betreiber weiss, ob einer läuft; und die Summe ist meine Grössenordnung, nicht eine Rechnung — die Spalte „tatsächlich" ist der Ort, an dem sie eine wird.

---

## 4. Zur Kenntnis: Betreiberentscheidungen und AF-F0

Zweck „Hobby mit Methode", Freigabeklassen, Fable-Takt, Bündel — übernommen; diese Antwort ist die erste im neuen Takt. **Scope-Freeze „fallweise"** ist die Entscheidung des Betreibers; meine Auflage dazu bleibt die aus 25f: Jede neue Idee, die vor dem Tag Auftrag wird, sagt, ob sie den Registertext oder den Tag-Commit berührt — berührt sie eines von beiden, ist sie ein Amendment mit Quelle des Grundes, sonst Handwerk. AF-F0 nach dem Tag; zu Frage 2 dort nur dies: Ja, ein Zyklus mit N = 1 zählt ins N des nächsten Durchgangs — das ist V2, und es steht in R6 als Folge.

---

**Kurz:** Fünf Aufträge angenommen; Bündel 1 vollständig, 19 vollzogen, O6 erledigt. 16.4 (g)–(m) trägt das Zellenbudget — mein Satz in 25f war aus dem Gedächtnis, Entscheidung 8 entfällt. `None` bestätigt, neunter Fall meiner Klasse. Alle sechs Neigungen der Sitzungen treffen; (3) und (5) werden Abnahmebedingungen des Erzeugers mit prüfbarer Form. Aus der Nullbefund-Skizze gehört ein Satz vor den Tag ins Register: Nach dem Tag nur registrierte Messbitten auf dem Selektionsraum, alles andere ist ein Versuch und zählt.

**Unsicher:**
- Ob die Gruppe `eingefroren` des Abbilds heute Dateien ausserhalb `research/vorregistrierung/` aufnehmen kann (die TB-24-Listen liegen unter `research/tb24_haltedauern/daten/`) — Handwerk, nicht gemessen.
- Die Tempfile-Probe: ob `tempfile` sie bei jedem Aufruf macht oder nur beim ersten — betrifft nur die Zahl in der Notiz.
- Ob R6 eine Ergänzung zu 27 oder zu 7.1 ist — ich schlage 27 vor (es geht um Lesen nach dem Tag); Handwerk der Einordnung.

---

## In einfacher Sprache

Fünf Aufträge sind fertig und angenommen; das erste Bündel aus meiner grossen Analyse ist damit abgearbeitet, die Startprüfung deckt jetzt alle 81 Programme des Laufs, und die Datenbanken werden täglich gesichert. Ich hatte in der Analyse geschrieben, das Kapital sei vielleicht noch nicht je Strategiegruppe verteilt — es steht doch im Regelwerk, in Abschnitt 16.4, und ich hatte ihn gelesen. Ich habe aus dem Gedächtnis gesucht statt im Text; das ist mein Fehler, und die Regel dagegen steht oben. Ein kleiner Platzhalter in einem alten Prüfwerkzeug war von mir falsch vorgeschlagen; die Sitzung hat es gemessen, ich bestätige die Berichtigung. Alle dreizehn Fragen sind beantwortet, meist so, wie die Sitzungen es selbst schon vermuteten. Neu ist ein Satz fürs Regelwerk: Nach dem grossen Lauf dürfen auf den Ergebnissen nur die Auswertungen gerechnet werden, die vorher angemeldet wurden — alles andere zählt als neuer Versuch. Das schützt davor, im Ergebnis so lange zu suchen, bis etwas gut aussieht.

---

## Registerblock — zeichengleich kopierbar, nummeriert

```markdown
**R1 — Marke an 43.3 (Bestätigung).** Die Berichtigung „`selektionsmodus = lambda: None` statt `lambda: False`" ist von Fable bestätigt (26a 3 (1)). Grund: Der Stummel soll das Werkzeug so laufen lassen wie am Stand TB-52; gemessen tut das nur `None` (`strategy_paths` legt 9 von 9 Ordner an), `False` nimmt den Modus-Zweig und meldet trotzdem 0 Unterschiede. Fables Beispiel `lambda: False` in 25e 3 war ungemessen — neunter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt". Handwerk als Beifang: Das Werkzeug zählt künftig die angelegten Ordner im Wegwerfbaum und meldet den durchlaufenen Zweig.
*Quelle des Grundes:* Messung TB-109/TB-113, Prüfprinzip A5. Kein Ergebnis.

**R2 — Ergänzung zu 42 (Klasse (iv), Reichweite).** Klasse (iv) umfasst jeden lesenden Zugriff eines Laufs auf seine eigene Zwischenablage: die Verzeichnis-Öffnung beim Aufräumen und das Lesen des darin abgelegten Ergebnisses. Die Probe, die `tempfile` beim Anlegen einer Ablage selbst macht (kein `mkdir` im Protokoll, sofort entfernt), ist Umgebung — Klasse (ii) — und wird als Tatsachennotiz geführt.
*Quelle des Grundes:* 25b (Definition von (iv): angelegt mit `mkdtemp`, vom Lauf selbst gelesen, entfernt oder im Beleg), 25e 3 (b). Kein Ergebnis.

**R3 — Ergänzung zu 30.2 (3) / 33.3 (Abbild der Sperrliste, Gruppe `eingefroren`).** Versionierte Dateien, die ein Lauf des Laufbereichs als Daten liest und die kein Code sind, gehören mit ihrem Hash in die Gruppe `eingefroren` des Abbilds — namentlich die neun Listen `research/tb24_haltedauern/daten/<bot>_alle_trades.csv`, aus denen der Faltenplan seine Faltenlängen herleitet (TB-95). Die Startprüfung nach 19/E2 bindet Code; das Abbild bindet Eingaben. Dass eine Änderung der Listen den Plan und damit dessen Abbild änderte, ersetzt die Bindung der Eingabe nicht: Der Nachweis verlangt die Eingabe bytegleich und gelesen (24c).
*Quelle des Grundes:* 25b (Klasse „Code" gegen Eingaben), 24c (zwei Teile des Nachweises), 24c B1. Kein Ergebnis.

**R4 — Ergänzung zu 19 / 42.2 E2 (Pflege von `ARBEITSBAUM_PFADE`).** Die Liste der Pfade der Sauberkeitsprüfung steht als Literal im Resolver; eine Gegenprobe liest die Laufbereichsmessung aus der Messdatei und vergleicht. Am Tag-Commit wird der Laufbereich neu gemessen; weicht die Messung von der Liste ab, ist das ein Befund: Die Liste wird vor dem Tag nachgezogen, nie durch ihn. Die Liste wird nicht aus der Messung erzeugt.
*Quelle des Grundes:* Prüfprinzip B3 (ein Gegenbeweis gegen eine bewegliche Referenz prüft nichts), 25b E5 (Messung am Tag-Commit). Kein Ergebnis.

**R5 — Abnahmebedingungen des Erzeugers (Ergänzung zu 24b A12 / Plan-Punkt 10).**
(a) Die Laufbereichsmessung nach dem Einbau des Erzeugers enthält `research/vorregistrierung/herkunft.py`; `ARBEITSBAUM_PFADE` ist danach nachgezogen (R4). Bis dahin ist `herkunft.py` am committeten Stand über die Sperrliste (Punkte 11/12) und das Abbild gebunden; die Lücke im Arbeitsbaum ist als Tatsachennotiz in 44 benannt.
(b) `zellen.csv` enthält für jede Zelle des Rasters genau eine Zeile; die Zeilenzahl ist gleich der Zahl der Zellen; eine Zelle ohne Trades trägt die Nullzeile (Sharpe 0 nach Registertext 1c, leere Trade-Liste), nie nichts. Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang.
(c) `herkunft.datenstand()` endet unter dem Modus ohne übergebenen Pfad mit 2; Beifang der nächsten Öffnung von `herkunft.py`, kein eigener Auftrag.
*Quelle des Grundes:* 24b A10 (kein Fallback unter dem Modus), 25e (2) (null Trades ist ein Wert), 36.5, 26a 5. Kein Ergebnis.

**R6 — Ergänzung zu 27 (Messungen auf dem Selektionsraum nach dem Tag).** Nach dem signierten Tag werden auf dem Selektionsraum dieses Durchgangs nur die Messungen gerechnet, die vor dem Tag als Messbitte registriert sind (R7). Jede weitere Messung auf denselben Zellen ist ein Versuch: Sie wird im Versuchsregister geführt und zählt in N des nächsten Durchgangs. Keine Messung nach dem Tag — registriert oder nicht — ändert Bleibt oder Geht; das sagt 7.1. Registrierte Messbitten sind Bericht, nicht Tor.
*Quelle des Grundes:* 7.1, Festlegung 11, Literatur (Story-telling und Data Snooping nach dem Ergebnis, López de Prado; „every backtest must be reported with all trials"). Kein Ergebnis.

**R7 — Liste der registrierten Messbitten für nach dem Tag (Anhang zu R6), Stand 26a.**
1. PBO je Bot über alle Zellen (CSCV, S = 16) — 25f V3.
2. MinTRL und Lo-Standardfehler je Gewinnerzelle — 25f V7.
3. Netto-Sharpe der Gewinnerzellen unter 0,5 %, 1,0 % und 1,6 % Roundtrip — 25f K2.
4. Implizite Kelly-Fraktion je Bot gegen die feste Positionsgrösse — 25f P5.
5. Krypto-Umkehr-Bots nach Liquiditätsdrittel des Universums — 25f S8.
6. Block-Bootstrap-Band je Gewinnerzelle für den Vergleich mit der Bestätigungsperiode — 25f O2.
Verfahrensmessungen nach 27.2 (vor dem Tag zulässig, nicht Teil dieser Liste): Adjustierungsstand und Herkunft der 150 Aktienreihen im Snapshot; Nutzung von Preisniveaus je Bot; ob alle neun Bots die geschlossene Kerze lesen; ob TB-85 die Kette Erzeuger → Auswertung deckt. Ergänzungen dieser Liste vor dem Tag sind zulässig und werden datiert; nach dem Tag ist die Liste geschlossen.
*Quelle des Grundes:* R6. Kein Ergebnis.

**R8 — Tatsachennotizen 26a.**
(a) `auswertung._abbruch_2`: Der Docstring sagt „`Abbruch` … endet mit 1"; falsch seit TB-111, stehen geblieben wegen der Freigabe „sonst nichts"; Streichung mit der nächsten planmässigen Öffnung.
(b) `str(e)` eines gefangenen `Abbruch` ist `"2"`, die Meldung steht in `e.meldung`; im Laufbereich (81 Module, Stand TB-113) liest kein Aufrufer `str(e)` — Suchmuster in der Notiz nennen, Messung am Tag-Commit wiederholen.
(c) db-Sicherung (25f O6): Schlüssel-Muster `key|secret|token|api|passw`, 0 Treffer über 12 Datenbanken; die Tabelle `zustand(schluessel, wert)` in `benachrichtigungen_schliessung.db` enthält laut Code nur `erstlauf_am`; deutsche Wörter nicht aufgenommen — Betrieb, nicht Lauf.
(d) N = 653 (Register 9): Was das Versuchsregister nicht zählt und nicht rekonstruieren kann, steht dort in 3.4 und 5.1–5.4; ein Verweis aus Register 9 auf Abschnitt 5 des Versuchsregisters wird nach dem Tag eingetragen. Folge für die Lesart: N_nominal ist eine Untergrenze.
(e) Berichtigung zu 25f A2 und C3 Entscheidung 8: Das Zellenbudget steht in 16.4 (g)–(m); offen ist nur der Vollzug im Code (16.11, Zeile 3; Stufe IV). Fables Satz „keinen Abschnitt gefunden" war aus dem Gedächtnis; Fables Regel: Vor „steht nicht im Register" wird im Text gesucht, nicht erinnert, und das Suchwort genannt.
*Quelle des Grundes:* Messungen TB-111, TB-112, TB-113, 26a 3 (a)/(b). Kein Ergebnis.
```
