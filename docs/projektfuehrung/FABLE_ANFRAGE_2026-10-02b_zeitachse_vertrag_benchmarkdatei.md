# FABLE_ANFRAGE 2026-10-02b — sechs vorgeprüfte Verfahrensfragen nach TB-130 (Zeitachse der Tagesreihe, fehlende Werte und doppelte Daten, Bestätigungsperiode, Benchmark-Datei, Marke an 7 (c), Tatsachennotiz zu 23.3) — an: Fable, neuer Chat (eröffnet 02.10.2026)

*Steuernder Chat, 02.10.2026, 18:49. Stand Repo: HEAD `0779453`. Register am `ad351d5`, sha256 `a7496780…`, 11 313 Zeilen, Abschnitte 0–52. Vorgeprüft hat ein Helfer des steuernden Chats Register und Code, nur lesend, mit Fundstellen; ein zweiter hat diese Anfrage gegengelesen, ein dritter die Änderungen danach. Nichts ist ausgeführt worden.*

⛔ **Sichtschutz 27.1:** Die Anfrage enthält keine Ergebnisgrössen des Selektionsraums. Die Zahlen sind Registerzeilen, Codefundstellen, Dateigrössen und Zählungen.

**Antwortform (ARBEITSWEISE 22.11 Nr. 3):** je Frage „einverstanden“ oder „anders, weil …“. Registertext nur als R-Block, Nummern ab **R66**. Ablage wie üblich: `projektfuehrung/FABLE_ANTWORT_2026-10-02b_<stichwort>.md`.

**Abschnitte nach F5, mit Dateigrösse (1 KB = 1 000 Bytes):** 52 (ganz; 13,8 KB); für Frage 1 und 6: 15 (15.3, 15.4; 25,9 KB), 23 (23.2–23.5; 29,2 KB), 24 (24.1, 24.2; 25,5 KB), 29 (29.3; 4,7 KB), 48 (48.4; 28,7 KB); für Frage 2 bis 4: 48 (48.1, 48.5, 48.7, 48.8, 48.14); für Frage 5: 7 (3,7 KB), 51 (51.6; 22,4 KB), 49 (49.2, 49.3; 5,1 KB), 4 (4.2; 6,0 KB). Bei Bedarf 50 (50.2), 35 (35.1), 34. **Reicht der Platz nicht, haben Frage 1 und Frage 6 Vorrang;** nenne dann, was offen bleibt.

---

## Teil 0. Kenntnis (je eine Zeile, keine Antwort nötig)

1. **TB-130:** R63–R65 stehen zeichengleich in 52.1–52.3. Gesetzt sind zwölf Marken: die fünf aus R65 (b) und sieben, die der steuernde Chat nach R65 (a) bestimmt hat (4.2, 48.16, 48.19, 51.5 zweimal, 51.6, 51.9). Widersprich, wenn eine davon nicht trägt.
2. **Voraussetzungen aus 02a** (52.4): R63 (c) trifft (`bot_lauf.py` ganz gelesen: kein Anteil je Tag, kein Mittel). R64, erste, trifft. R64, zweite, ist nicht entscheidbar, solange kein Code den Kalender der Tagesreihe festlegt; sie hängt an Frage 1.
3. **Marke an 25.2:** Sie steht nach 34.3 direkt unter dem berichtigten Satz und damit vor der älteren Marke aus R53; die Reihenfolge am Ort ist dort nicht mehr die zeitliche.
4. **Werkzeug, Handwerk:** `registerkopie.py --marken` zählt die erste Zitatzeile von R61 und von R65 als Marke; im Index sind beide nicht als Marke geführt.

---

## Teil 1. Fragen

### Frage 1 — Führt die Tagesreihe Tage vor dem ersten Handelbar-Tag, und über welche Tage läuft der Falten-Sharpe? (02a, „Unsicher“ 1; R64 (e))

- **Fundstellen:**
  - REG Z. 1430–1432 (15.3, 1a): „Flache Tage stehen mit Rendite 0 in der Reihe.“
  - REG Z. 1439–1443 (15.3, 1c): „Der Falten-Sharpe wird für jeden Parametersatz in jeder Falte aus den täglichen Netto-Renditen des Kapitalpfads gerechnet“.
  - REG Z. 1475–1476 (15.4, 2a): „Jeder Handelstag gehört zu der Falte, in die sein Datum fällt.“
  - REG Z. 5384 (29.3): „Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten Selektionsfalte mit dem registrierten Startkapital und ohne offene Position.“
  - REG Z. 3933–3939 (23.3): „Ein Tag, an dem kein Symbol handelbar ist, gehört nicht zum Benchmark — er wird nicht mit Rendite 0 geführt, sondern gar nicht.“
  - REG Z. 3908 (23.2, zweiter Grund, zu Rang 3): „Unter VH erzeugt Rang 3 Alpha aus Nichtteilnahme.“
  - REG Z. 3947–3949 (23.3, zur Entstehung): „Seine zweite Fassung band den Benchmark an den Kalender des Bot-Kapitalpfades — **den es nicht gibt**: der Pfad ist ereignisindiziert (`shared/zuteilung.py:720–735`, gemessen 20.09.2026).“
  - REG Z. 4295 (24.1, Zitat aus deiner Antwort): „Der Drawdown gehört aus derselben Tagesreihe wie der Sharpe.“
  - REG Z. 4303–4305 (24.2, Registertext): Der Kapital-Drawdown einer Falte wird „auf der täglichen Mark-to-Market-Reihe des Kapitalpfads gerechnet (1a), auf denselben Tagen wie der Benchmark (3b (c))“. REG Z. 4309–4311 (24.2, Erläuterung): Der Satz legt „die **Zeitachse** (dieselben Tage wie der Benchmark, 3b (c) in der Fassung aus 23.3)“ fest — für den Drawdown; vom Sharpe spricht 24.2 nicht.
  - REG Z. 10794 (48.4, R36): „Der Drawdown je Falte ist der Ausschnitt eines durchgehenden Kapitalpfads (29.3, 2a): gemessen innerhalb der Falte, mit dem Kapitalstand am Faltenbeginn als erstem Hochpunkt, ohne Neustart des Kapitals.“
  - REG Z. 11276 (52.2, R64 (e)): „Welche Tage die Tagesreihe über die Tage nach (a) hinaus führt, legt dieser Block nicht fest.“
  - Wortsuche in den Abschnitten 16, 21 und 33: „Tagesreihe“ kommt dort nicht vor (auch nicht klein geschrieben oder im Plural).
- **Stand:** 1a, 2a und 29.3 lesen sich als Reihe ab dem 1. Januar mit flachen Tagen. 23.3 nimmt Tage ohne handelbares Symbol aus dem Benchmark aus, 24.2 rechnet den Drawdown auf den Tagen des Benchmarks. 24.1 holt den Drawdown auf die Tagesreihe des Sharpe; die Richtung geht vom Sharpe zum Drawdown, nicht umgekehrt. Der Kapitalpfad im Code ist nach 23.3 ereignisindiziert; 52.4 (REG Z. 11297) hält fest: „Den Kalender der Tagesreihe legt noch kein Code fest“. Keine Stelle sagt, ob die Tagesreihe die Tage vor dem ersten Handelbar-Tag führt. Der Fall betrifft nur Falten, in denen der Benchmark nicht an allen Tagen definiert ist (23.4).
- **Frage (a):** Führt die Tagesreihe einer Zelle in einer solchen Falte die Tage vor dem ersten Handelbar-Tag des Bots, flach mit Rendite 0?
- **Frage (b):** Über welche Tage läuft der Falten-Sharpe nach 1c: über alle Tage der Tagesreihe in der Falte oder über die Benchmark-Tage des Bots in der Falte (R64 (a))?
- **Neigung:** (a) ja: Der Kapitalpfad ist durchgehend ab dem 1. Januar (29.3, R36), flache Tage stehen mit 0 darin (1a). (b) über die Benchmark-Tage. Das ist meine Lesart, kein Registerwortlaut: 24.1 will Drawdown und Sharpe auf derselben Tagesreihe, 24.2 setzt die Zeitachse des Drawdowns auf die Tage des Benchmarks; ich übertrage diese Zeitachse auf den Sharpe, damit beide auf denselben Tagen stehen. Dafür führe ich den zweiten Grund aus 23.2 an („Alpha aus Nichtteilnahme“, dort zu Rang 3) und verallgemeinere ihn auf den Sharpe: Tage, an denen der Bot nichts halten konnte, sollen auch dort keine Grösse bilden. Das steht so nicht im Register. Dagegen spricht: 1c nennt „aus den täglichen Netto-Renditen des Kapitalpfads“ ohne Einschränkung, und 24.2 nennt die Zeitachse nur für den Drawdown.

### Frage 2 — Wer schliesst fehlende Werte und doppelte Datumszeilen aus? (52.5 Nr. 5)

- **Fundstellen:**
  - REG Z. 11296 (52.4): „Fehlende Werte und doppelte Daten werden dort weder behandelt noch geprüft“.
  - `research/vorregistrierung/auswertung.py`: `lies_tagesreihe` (Z. 361–370) und `lies_benchmark` (Z. 378–386) prüfen Existenz und Spalten und sortieren nach `datum`. Die einzige Prüfung auf fehlende Werte steht in Z. 355 und gilt `netto_sharpe` in `zellen.csv`. `dropna`, `fillna`, `duplicat`, `is_unique`, `isfinite` kommen in der Datei nicht vor.
  - Register: In 43 und 45–52 (R12, R39, R40, R46) ist kein Satz gefunden, der fehlende Werte oder doppelte Daten in Tagesreihe oder Benchmark-Reihe ausschliesst.
- **Frage:** Wo wird das geregelt: im Datenvertrag als Registertext, als Wache im Erzeuger oder in der Abnahme nach R46?
- **Neigung:** Registertext nach der Bauart von R64 (c): In jeder Tagesreihe und jeder Benchmark-Reihe ist `datum` eindeutig und kein Feld leer; der Zellen-Erzeuger prüft das im Lauf und endet sonst mit 2; die Abnahme nach R46 prüft die Wache mit Gegenprobe. `auswertung.py` bleibt zu.

### Frage 3 — Gilt R64 für die Zeile der Bestätigungsperiode, und ab welchem Tag? (02a, „Unsicher“ 4)

- **Fundstellen:**
  - REG Z. 10801 (48.5, R37): „Die Bestätigungsperiode des Selektionslaufs ist die Spanne nach 35.1“; „Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position des Gewinners mehr offen ist; Deckel je Bot nach 16.6/41.3 C2; eine am Deckeltag noch offene solche Position zählt nicht (Attribution je Position). Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle (bestaetigung_ab_effektiv, R34); auswertung.py nimmt den Wert der Gewinnerzelle (41.3 C3).“
  - REG Z. 10773 (48.1, R33): „Selektionsfalten und Bestätigungsperiode (35.1) — genau eine Zeile“.
  - Code: `bestaetigungsperiode` (`auswertung.py` Z. 608–629, „Kein Veto“) reicht `mittlere_exposure` (Z. 626) nur in den Bericht. `zulaessigkeit` (Z. 403) und `beta_bereinigung` (Z. 502–503) filtern auf die Selektionsfalten. `bestaetigung_ab_effektiv` kommt im Code nicht vor.
- **Frage:** Gilt R64 (a) für die mittlere Exposure in der Zeile der Bestätigungsperiode, und beginnen ihre Tage am Anfang der Spanne (35.1) oder am Tag `bestaetigung_ab_effektiv` der Zelle?
- **Neigung:** R64 (a) gilt; die Tage beginnen am Tag `bestaetigung_ab_effektiv` der Zelle, weil R37 den Beginn der Bestätigungsstatistik an diesen Tag bindet und ihn für jede Zelle bestimmen lässt. Die Grösse ist Bericht, kein Urteil liest sie. Dagegen spricht: R37 nennt nur die „Bestätigungsstatistik des Gewinners“; die Periode selbst bleibt „die Spanne nach 35.1“, und 35.1 führt die Spanne als Bezeichner.

### Frage 4 — R39 nennt `<bot>.csv`, der eingefrorene Code liest `<markt>.csv` (52.5 Nr. 7)

- **Fundstellen:**
  - REG Z. 10815 (48.7, R39): „im Vertrag lies „<bot>.csv““. REG Z. 11298 (52.4, Befund des steuernden Chats): „Wann der Code den Namen je Bot liest, ist nicht festgelegt; `auswertung.py` wird nach R64 (e) nicht geöffnet (52.5)“.
  - `auswertung.py:379`: `os.path.join(wurzel, "benchmark_tagesreihen", f"{markt}.csv")`, `markt` aus `rd.BOTS[bot]["markt"]` (Z. 498). Suche nach `benchmark_tagesreihen` in allen `*.py` des Repos (ohne `ergebnisse/`): schreibend `research/vorregistrierung/beispieldaten.py:173, 233` (`f"{markt}.csv"`) und `research/vorregistrierung/test_ersatzwerte.py:293/298, 793/798` (`aktien.csv`); lesend `auswertung.py:379` (Docstring Z. 64) und `research/vorregistrierung/test_vorregistrierung.py:425, 465, 491` (`aktien.csv`); dazu eine Nennung im Text von `docs/belege/TB-115/m3_kette.py:48`. Ein Erzeuger des Laufs liegt nicht vor. Keine Registerstelle sagt, wer den Dateinamen umstellt.
- **Frage:** Wie wird das aufgelöst? R64 (e) sagt: „auswertung.py wird für nichts davon geöffnet.“
- **Neigung:** Ein Register-Code-Widerspruch nach 25c (1), aufzulösen vor dem Tag durch eine Öffnung von `auswertung.py` an dieser einen Stelle (Z. 379 und Docstring), als eigener Umsetzungsauftrag mit Einzelfreigabe, zusammen mit dem Zellen-Erzeuger. Der Satz in R64 (e) bezieht sich nach meiner Lesart auf die Wache und die Probe aus R64, nicht auf R39. Dagegen spricht: R64 (a) nennt selbst „wie benchmark_tagesreihen/<bot>.csv sie führt (R39)“, im selben Block wie der Satz in (e); und 52.4 liest R64 (e) als Sperre auch für diese Stelle; trifft das, bleibt nur ein Block, der die Öffnung erlaubt, oder die Berichtigung von R39. Jede Öffnung des eingefrorenen Codes hat ihren Preis; der Erzeuger könnte je Markt schreiben, wenn R39 berichtigt würde.

### Frage 5 — Trägt 7 (c) eine Marke zu R64 (a)? (52.5 Nr. 9)

- **Fundstellen:**
  - REG Z. 11276 (52.2, R64 (a)): „Das gilt für die mittlere Exposure je (Zelle, Falte) (4.2) und für die des Gewinners über seine Selektionsfalten (7 (c)).“
  - REG Z. 829–834 (7, Präzisierungen): „Beide Reihen werden auf gemeinsame Tage gebracht; weniger als drei gemeinsame Tage sind ein Abbruch, keine Annahme.“
  - REG Z. 11209 (51.6, R61 (b)), zweiter Satz: „Keine Marke erhält ein Ort, der nur Quelle des Grundes, Statusliste, Plan oder Code ist, der im erzeugten Block liegt oder in Abschnitt 10.“ Später im selben Block: „Ohne Marke bleiben, vom Index geführt: R27, R28, R30, R54 an 7 (c), …“.
  - REG Z. 11313 (52.5 Nr. 9, Text des steuernden Chats): „Die Präzisierungen in Abschnitt 7 tragen die Regel selbst, und R61 (b) führt 7 (c) als Ort ohne Marke“. Genauer: R61 (b) führt dort R54 an 7 (c).
  - REG Z. 11283 (52.3, R65 (a)): „Gibt ein Block einem benannten Ort ein „lies“, eine Ergänzung oder eine Bestätigung, trägt der Ort die Marke, auch wenn die Aufzählung des Blocks ihn nicht nennt; ausgenommen bleiben die Orte nach R61 (b), zweiter Satz.“
- **Gesetzt in TB-130:** eine Marke an 4.2 (PRÄZISIERT durch R64), keine an 7 (c).
- **Frage:** Trägt 7 (c) eine Marke zu R64?
- **Neigung:** nein. Abschnitt 7 trägt die Regel selbst („gemeinsame Tage“, „über dieselben Tage“); R64 (b) nennt sie als die Regel, der der Code folgt, und R64 (a) nennt 7 (c) als Geltungsbereich. 7 (c) ist damit für R64 Quelle des Grundes (R61 (b), zweiter Satz) und nach R65 (a) ausgenommen. Der Index führt den Verweis. Dagegen spricht: R64 (a) sagt, welche Tage in 7 (c) „dieselben Tage“ sind; das lässt sich als Präzisierung von 7 (c) lesen, wie die an 4.2 — dann wäre 7 (c) nicht „nur“ Quelle des Grundes.

### Frage 6 — Tatsachennotiz zu 23.3: „je Falte“ gegen den Code

- **Fundstellen:**
  - REG Z. 3959–3964 (23.3, Tatsachennotiz): „Die Umsetzung lässt den ersten Kurstag je Falte aus, weil `pct_change` dort keine Rendite liefert. Abweichung gegenüber dem Satz: höchstens ein Tag je Falte.“
  - `research/vorregistrierung/benchmark.py`: Z. 185 `r = r[r.index >= ab]` (je Symbol ab Handelbar-Tag); Z. 205 `rahmen.pct_change().mean(axis=1, skipna=True).dropna()`; Kommentar Z. 264–267: die Reihe wird „EINMAL“ gebildet „und je Falte nur noch ausgeschnitten“ (Bildung Z. 272, Ausschnitt Z. 290).
- **Stand (gelesen, nicht ausgeführt):** Die Rendite fehlt am ersten Punkt jedes Symbols. Ein Tag entfällt nur dort, wo kein Symbol eine Rendite hat: am ersten Tag des Rahmens, einmal je Bot und nicht in jeder Falte. „Höchstens ein Tag je Falte“ bleibt als Schranke richtig.
- **Frage:** Ist „je Falte“ zu berichtigen? R64 (a) nimmt die Notiz in Bezug („die Tatsachennotiz zu 23.3 (erster Kurstag) gilt mit“).
- **Neigung:** ja, in „lies“-Form mit Marke an 23.3: „lässt den ersten Kurstag des Rahmens aus, einmal je Bot“. [Voraussetzung, vor dem Eintrag zu messen: das Verhalten an Kurslücken, durch einen Test am Code, nicht durch Lesen.]

---

## Nach deiner Antwort

Ein Registerauftrag (Einzelfreigabe des Betreibers) trägt R66 und folgende ein. Frage 1 entscheidet mit, was der Zellen-Erzeuger als Kalender der Tagesreihe schreibt.
