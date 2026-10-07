# REGISTER-KOPIE Abschnitt 47 (von 0–55) — Register-Z. 10683–10802 — Commit ad1fc0d3e5397cec6eb75c5e62de3b1bb7868c24 — 2026-10-07 — Original sha256 ab97ae1e31da161bc1aebed6b00bb2ec6eec07f760c45c645b9801e6e916b9cd — KOPIE, nicht das Register

## 47. Fable 27c — Registerblock R18–R32 (TB-126)

Reines Eintragen von Registertext, Bauart wie 46 (46.0). Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md`, md5 `ff96392ed654fdcae2e991e51e424dc5`, 48 420 B, am Commit `0f56aeb`, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert“, Z. 161–209. Die Datei hat der steuernde Chat am 29.09.2026 aus Fables Ablage übertragen, zweifach unabhängig, `cmp` rc 0; Bytegleichheit mit der Ablage war mit dem Werkzeug nicht messbar. Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette. Die Nummern hat der steuernde Chat vergeben (Auftrag TB-126, Einzelfreigabe des Betreibers), nicht Fable. Die Regel aus 34 gilt weiter: Marke am alten Ort, der alte Satz bleibt zeichengleich. ⛔ In Abschnitt 10 steht keine Marke; was dorthin gehört, steht in der Kette und als Indexzeile in `REGISTER_INDEX.md`. Die Voraussetzungen, die Fable „zu messen“ nennt, stehen mit Befund in 50.1.

### 47.1 R18 — Präzisierung zu 16.4 (m), (h) und (l) (Zellenanteil und Klassenschlüssel; L1)

> **R18 — Präzisierung zu 16.4 (m), (h) und (l) (Zellenanteil und Klassenschlüssel; L1).** Das Buch wird zuerst nach dem Klassenschlüssel (l) auf die Anlagen geteilt. Der Zellenanteil in (m) ist der Anteil der Zelle am Budget ihrer Anlage: zu gleichen Teilen unter den Zellen dieser Anlage nach (g). „Aktive Zellen teilen das Buch zu gleichen Teilen" in (h) ist innerhalb der Anlage zu lesen. Eine Zusammensetzung von (h) und (m), die Buch unverteilt lässt, ist keine Lesart: 7.1 sagt „nicht in Kasse", und 16.4 kennt keinen Anteil, der weder in Bots noch in einer Benchmark-Position liegt.
> *Quelle des Grundes:* (l) „skaliert die Zellen einer Anlage gemeinsam" (eine Gruppe gemeinsam skalieren legt ihre Summe fest); (j) nennt die Benchmark-Position „ihrer Anlage" als Behälter der Zelle; 7.1. Kein Ergebnis.

**Kette:** Marken: 16.4 (m); 16.4 (h); 16.4 (l).

### 47.2 R19 — Präzisierung zu 16.4 (h), (j) und (k) (Zahl der Zellen; L2; T116-4)

> **R19 — Präzisierung zu 16.4 (h), (j) und (k) (Zahl der Zellen; L2; T116-4).** Die Zahl der Zellen in (h) ist die Zahl der Zeilen in (g), nicht die Zahl der gerade aktiven Zellen. Eine Zelle, in der kein Bot auf Grundbudget oder Bestätigt steht, behält ihren Anteil und hält ihn nach (j) als statische Benchmark-Position ihrer Anlage; die übrigen Zellen wachsen nicht. Eine neue Zelle im Sinn von (k) entsteht nur durch eine neue Zeile in (g) — einen nach 16.8 zugelassenen Bot, dessen Quelle × Anlage in (g) noch nicht steht. Erhält ein Bot einer bestehenden Zelle über einen neuen registrierten Lauf wieder Grundbudget (6 (d), 7.1), geht der Anteil seiner Zelle aus der Benchmark-Position an ihn zurück; die Zahl der Zellen ändert sich nicht. Ein neu zugelassener Bot in einer bestehenden Zelle tritt in deren Teilung nach (i) ein; auch das ändert sie nicht. Die Zahl der Zellen hat keine Vorgeschichte.
> *Quelle des Grundes:* (j) „nicht an andere Zellen"; das Prinzip „Die Leiter bewegt Bots. Sie bewegt keine Zellen."; (g) „die Zuordnung … ändert sich nur mit dem Bot"; (k) „folgt aus Zulassung, nicht aus Ergebnis". Kein Ergebnis.

**Kette:** Marken: 16.4 (h); 16.4 (j); 16.4 (k).

### 47.3 R20 — Ergänzung zu 16.4 (l) und (j) (Anlage ohne aktive Zelle; L3)

> **R20 — Ergänzung zu 16.4 (l) und (j) (Anlage ohne aktive Zelle; L3).** Der Klassenschlüssel (l) gilt auch dann, wenn eine Anlage keine aktive Zelle hat. Ihr Anteil nach (l) hält die statische Benchmark-Position dieser Anlage; er geht nicht an die andere Anlage.
> *Quelle des Grundes:* (l) ist ein Betreiberentscheid über den Risikobeitrag (Begründung 80/20 in 16.4), gültig bis Netting, und nicht danach gesetzt, welche Anlage läuft; (j) „nicht an andere Zellen"; 7.1 „nicht zu den Überlebenden". Kein Ergebnis.

**Kette:** Marken: 16.4 (l); 16.4 (j).

### 47.4 R21 — Präzisierung zu 16.4 (b), (i) und (j) und Ergänzung zu 7.1 (Schatten nach der Herkunft der Stufe; L4…

> **R21 — Präzisierung zu 16.4 (b), (i) und (j) und Ergänzung zu 7.1 (Schatten nach der Herkunft der Stufe; L4; Prüfung vor dem Tag).** Der Faktor 0 in (i) ist der Multiplikator jedes Bots auf Schatten. Wohin sein Budgetanteil geht, hängt an der Herkunft der Stufe: (1) Schatten durch Abstieg nach (d) — Quartalsprüfung, Out-of-Sample — zählt in der Teilung der Zelle mit Faktor 0; die übrigen Bots der Zelle teilen das Zellenbudget nach (i) ((j)). (2) Schatten aus jedem anderen Grund — nach (b) im Selektionslauf, nach 15.6 (c) unterbestimmt, nach 16.5/17.7 „Backtester nicht bestätigt", nach (e) Notbremse — behält den Anteil, den (i) ihm auf Grundbudget gäbe (Faktor 1 in der Summe der Faktoren der Zelle); dieser Anteil wird als statische Benchmark-Position seiner Anlage gehalten ((b), 7.1). Steigt ein Bot derselben Zelle auf Bestätigt, gilt (i) über alle Faktoren der Zelle einschliesslich dieses Anteils. Die Benchmark-Position einer ganz inaktiven Zelle nach (j) ist die Summe der Grundbudget-Anteile ihrer Bots. Die Eingabe des Leiter-Skripts ist je Bot die Stufe und, bei Schatten, ob die Stufe aus (d) stammt; die Herkunft steht im Journal ((b): Ergebnis des eingefrorenen Skripts; (d): Quartalsprüfung; (e): protokolliert nach 22.4). Die Prüfung vor dem Tag in 16.4 zählt jede mögliche Eingabe auf — vier Zustände je Bot, 4⁹ = 262 144 —, nicht nur die 3⁹ Stufentabellen; sie verlangt für jede Eingabe einen eindeutigen Multiplikatorvektor und eindeutige Benchmark-Anteile je Anlage, ohne Eingabe des Betreibers.
> *Quelle des Grundes:* 7.1 „nicht zu den Überlebenden" (Betreiber-Festlegung, Sperrlistenpunkt 5) und (b) für den Ausfall im Lauf; (j) „die übrigen teilen es nach (i)" für den Abstieg; das Prinzip: Out-of-Sample-Evidenz über einen Bot bewegt Kapital zwischen Bots, ein In-Sample-Ausfall nicht (22.4). Beide Sätze stehen; keiner wird gestrichen. Kein Ergebnis.

**Kette:** Marken: 7.1; 16.4 (b); 16.4 (i); 16.4 (j).

### 47.5 R22 — Präzisierung zu 16.4 (a) und (i) (Faktor „Bestätigt" vor Netting; L5)

> **R22 — Präzisierung zu 16.4 (a) und (i) (Faktor „Bestätigt" vor Netting; L5).** Der Faktor 2 in (i) gilt ab der ersten Quartalsprüfung, die einen Bot nach (c) auf Bestätigt setzt. „Rang-5-Gewichtung, sobald Netting existiert" in (a) betrifft die Gewichtung im Netting, nicht den Stufenfaktor.
> *Quelle des Grundes:* Das Register bedingt in (l) ausdrücklich auf Netting und in (i) nicht; ein Faktor 1 bis Netting machte (c) wirkungslos. Kein Ergebnis.

**Kette:** Marken: 16.4 (a); 16.4 (i).

### 47.6 R23 — Präzisierung zu 16.4 (b), 7.1 und 15.6 (c) (Budgetanteil und Höhe der Benchmark-Position; L0.1; T116-3)

> **R23 — Präzisierung zu 16.4 (b), 7.1 und 15.6 (c) (Budgetanteil und Höhe der Benchmark-Position; L0.1; T116-3).** Der Budgetanteil eines Bots auf Schatten ist ein Budget (R21). Die statische Benchmark-Position darin ist in Höhe seines mittleren Exposures: der mittleren Exposure des Plateau-Gewinners über die Selektionsfalten, wie Abschnitt 7 (c) und der Bericht nach Abschnitt 8 sie führen. Der übrige Teil des Budgets ist nicht Kasse im Sinn von 7.1, sondern der nicht investierte Teil des Budgets, wie ihn der Bot selbst mit derselben mittleren Exposure hielte; 7.1 verbietet, das Budget aus dem Buch zu ziehen oder den Überlebenden zu geben. Das Leiter-Skript gibt Budgets aus (Multiplikatoren je Bot, Benchmark-Anteile je Anlage); die Höhe der Position ist nachgelagert und kein Parameter der Prüfung vor dem Tag.
> *Quelle des Grundes:* 4.2 (Benchmark als statische Position in Höhe der mittleren Exposure), 7 (c) (mittlere Exposure des Gewinners), 7.1. Kein Ergebnis.

**Kette:** Marken: 7.1; 15.6 (c); 16.4 (b).

### 47.7 R24 — Tatsachennotiz zu 16.4 (h) und (g) (Folge der Gleichteilung bei ungleicher Besetzung; T116-5)

> **R24 — Tatsachennotiz zu 16.4 (h) und (g) (Folge der Gleichteilung bei ungleicher Besetzung; T116-5).** Unter R18–R20 trägt in der Stufentabelle „alle Grundbudget" ein Bot, der allein in seiner Zelle steht, zwei Fünftel des Buchs (TB-116: `volatility_breakout` 3,6-fach seiner heutigen Grösse; die drei Umkehr-Aktien-Bots je 1,2; die Krypto-Bots 0,45 und 0,3 — Budgetanteile aus aufgezählten Tabellen). Das ist eine Folge des Registertexts, keine Lesart und kein Fehler: (h) macht die Zelle zur Einheit der Teilung, (g) nennt die Besetzung. Eine Teilung nach Zahl der Bots je Zelle liesse Bots Zellen bewegen. Ein Deckel je Bot gehört nach 4.3 in das Netting (Rang 5), das nicht existiert; ein Deckel vor Netting wäre ein neuer, als willkürlich gekennzeichneter Registertext des Betreibers (Rest in die Benchmark-Position der Anlage), dessen Quelle des Grundes der Risikoappetit ist, nie die Zahl. Entscheidungsvorlage: (a) so lassen — Empfehlung des Verfahrensprüfers; (b) Deckel je Bot vor Netting — Betreiber.
> *Quelle des Grundes:* (h) „die einzige Aufteilung, die kein Ergebnis verwendet", das Prinzip, 4.3. Kein Ergebnis.

**Kette:** Marken: 16.4 (h); 16.4 (g). Entscheid: 50.6.

### 47.8 R25 — Bestätigung von 46.9 als Ergänzung zu 12 und R14 (Herkunftsprüfung ohne Modus; T117-1)

> **R25 — Bestätigung von 46.9 als Ergänzung zu 12 und R14 (Herkunftsprüfung ohne Modus; T117-1).** Die Herkunftsprüfung nach R14 ist Teil des Datenvertrags von `auswertung.py` unter dem Selektionsmodus: jede der fünf Bedingungen endet mit 2. Ohne Modus ist `herkunft.json` keine Pflichteingabe; sie wird gelesen, wenn vorhanden, für die ausgewerteten Bots, im Kopf des Berichts angezeigt, und ihr Fehlen oder Abweichen ist kein Abbruch. Grund: Ein Lauf dieses Registers ist ein Lauf unter dem Modus (5e/19, 42.2 E5); ohne Modus läuft `auswertung.py` gegen Beispieldaten mit erfundenen Werten (12), und eine Herkunft, die zu bezeugen wäre, gibt es dort nicht. Die übrigen Vertragsbrüche (43-1, 42.3 F1) bleiben unabhängig vom Modus 2: Ohne sie kann nicht gerechnet werden; ohne `herkunft.json` kann nicht bezeugt werden. Der Docstring, der `herkunft.json` als Teil des Vertrags nennt, trägt den Zusatz „unter dem Modus" [Voraussetzung, zu messen: ob seit TB-117 Block D vorhanden]; wenn nicht, Nachtrag mit der nächsten planmässigen Öffnung von `auswertung.py`, keine eigene.
> *Quelle des Grundes:* 12, 5e/19, 42.2 E5, R10 (dieselbe Bauart), 25c (1). Kein Ergebnis.

**Kette:** Marken: Abschnitt 12; 46.5, Block R14; 46.9. Voraussetzung gemessen: 50.1.

### 47.9 R26 — Ergänzung zu 12, R14 und 35.4 (alle neun unter dem Modus; --bot; T117-2)

> **R26 — Ergänzung zu 12, R14 und 35.4 (alle neun unter dem Modus; `--bot`; T117-2).** Unter dem Modus prüft `auswertung.py` die `herkunft.json` aller neun Bots, auch wenn nur ein Bot ausgewertet wird; ohne Modus nur die der ausgewerteten. Ein Lauf mit `--bot` unter dem Modus wertet nicht alle neun aus und ist kein Bericht dieses Registers (12: keine Option, die einen Bot ausnimmt; 14: Selektion → Bestätigungsperiode → Bericht für alle neun). Der Bericht des Tages ist der Lauf ohne `--bot`. Der Laufwrapper (35.4) startet `auswertung.py` unter dem Modus nur ohne `--bot`; `auswertung.py` selbst wird dafür nicht geöffnet. [Voraussetzung, zu messen: dass `--bot` unter dem Modus heute bis zum Bericht durchläuft; TB-117 J-7 hat den Modus im Prozess nachgestellt.]
> *Quelle des Grundes:* 12, 14, R14 „für jeden Bot", 21b (3) (Prüfungen wandern dorthin, wo geändert werden darf). Kein Ergebnis.

> ⭐ **47.9 R26 BERICHTIGT durch R61 (51.6)** (Fable 01a R61, Unterpunkt (c), nachgetragen nach Fable 02a R65 (b), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: Abschnitt 12; 35.4; 46.5, Block R14. Voraussetzung gemessen: 50.1.

### 47.10 R27 — Tatsachennotiz zu R14 Bedingung 5 und Ergänzung zu den Tag-Vorbedingungen (voller Commit-Hash; T117-3)

> **R27 — Tatsachennotiz zu R14 Bedingung 5 und Ergänzung zu den Tag-Vorbedingungen (voller Commit-Hash; T117-3).** Bedingung 5 (die neun `herkunft.json` untereinander gleich) bleibt; neben 2–4 ist sie redundant, ausser beim Commit, der nach 19 als Präfix eines 7–40-stelligen `TB_SELEKTIONSCOMMIT` verglichen wird. Tag-Vorbedingung: Am Tag ist `TB_SELEKTIONSCOMMIT` der volle Hash des Tag-Commits (40 Zeichen); der Tag referenziert seinen Hash (17.2), und ein Präfix ist nicht sein Hash. Bedingung 5 wird nicht gestrichen: Redundanz in einer Wache ist kein Grund aus der Struktur.
> *Quelle des Grundes:* 17.2, 19, Prüfprinzip C4. Kein Ergebnis.

**Kette:** Marken: 46.5, Block R14 (Bedingung 5 steht in dessen erster Zeile).

### 47.11 R28 — Tatsachennotiz zu Register 18 und Plan-Punkt 6 (drei Orte des Datenstands; T117-4)

> **R28 — Tatsachennotiz zu Register 18 und Plan-Punkt 6 (drei Orte des Datenstands; T117-4).** Der registrierte Datenstand `d9449faf…` steht in Register 18 (Quelle) und als Codekopie in `shared/snapshot.py::VERANKERTER_DATENSTAND` und `research/vorregistrierung/auswertung.py::REGISTRIERTER_DATENSTAND`. Das ist der Zustand aus 32.5 (c) — Literal mit Probe gegen den Registertext — und als benannter Zwischenstand zulässig, wenn jede Kopie ihre Probe hat; für `auswertung.py` ist es J-r (TB-117) [Voraussetzung, zu messen: ob `snapshot.py` eine Probe gegen Register 18 hat; wenn nein, Handwerk ohne Sperrlistennähe]. Zusammenlegung innerhalb des Laufbereichs mit 40.8 (h): die Konstante wandert nach `registerdaten.py`, `auswertung.py` liest sie von dort. `snapshot.py` bleibt ausserhalb des Laufbereichs und behält seine gebundene Kopie; ein Import zöge es hinein.
> *Quelle des Grundes:* 21j/37.5 (ein Wert, ein Ort), 32.5, 42.2 E5. Kein Ergebnis.

**Kette:** Marken: Abschnitt 18. Voraussetzung gemessen: 50.1.

### 47.12 R29 — Ergänzung zu 42.2 E5, R4 und R5 (a); Tatsachennotiz zu 44-6 (herkunft.py im Laufbereich; T117-5)

> **R29 — Ergänzung zu 42.2 E5, R4 und R5 (a); Tatsachennotiz zu 44-6 (`herkunft.py` im Laufbereich; T117-5).** Der Lauf-Typ „`auswertung.py` samt Laufwrapper" (E5) ist ein Lauf, kein Import. Der echte Modus-Lauf von `auswertung.py` lädt seit TB-117 Block D `research/vorregistrierung/herkunft.py`; `herkunft.py` gehört damit zum Laufbereich, vor dem Zellen-Erzeuger. Die Laufbereichsmessung misst den Lauf-Typ „auswertung" als echten Modus-Lauf (Beispieldaten mit `herkunft.json`, wie TB-117 E); eine Messung über `import auswertung` ist für diesen Lauf-Typ keine Messung nach E5. `ARBEITSBAUM_PFADE` wird nach R4 vor dem Tag nachgezogen — mit der Öffnung von `paths.py`, die der Zellen-Erzeuger braucht, spätestens vor der ersten Laufbereichsmessung, die als Tag-Messung gilt; `test_arbeitsbaum_laufbereich.py` zieht mit (Grundsatz 40). Bis dahin ist `herkunft.py` am committeten Stand über Sperrlistenpunkte 11/12 und das Abbild gebunden und am Tag über die Sonde im Laufwrapper (36.2 (b)); eine uncommittete Änderung hielte die Startprüfung nicht an, die Sonde wohl. R5 (a) gilt mit diesem Grund fort.
> *Quelle des Grundes:* 42.2 E5 (Vereinigung aller Lauf-Typen, gemessen als Lauf), R4 (Liste vor dem Tag nachgezogen, nie durch ihn), 25f A3 (keine Öffnung doppelt), Messung TB-117 E. Kein Ergebnis.

**Kette:** Marken: 42.2, Eintrag E5 (e); 44.1, Eintrag 44-6; 45.4, Block R4; 45.5, Block R5, Punkt (a).

### 47.13 R30 — Ergänzung zu 14 und zu den Tag-Vorbedingungen (Erzeuger und Auswertung am Tag-Commit; T117-6)

> **R30 — Ergänzung zu 14 und zu den Tag-Vorbedingungen (Erzeuger und Auswertung am Tag-Commit; T117-6).** Der Zellen-Erzeuger und `auswertung.py` laufen am Tag-Commit (`TB_SELEKTIONSCOMMIT` = HEAD, 19). Zwischen dem Schreiben der `herkunft.json` und der Auswertung ändert sich weder das Register noch eine Datei aus `EINGEFROREN`; sonst endet die Auswertung nach R14 mit 2, und das ist ein Befund, kein Fehler der Wache. Registereinträge zum Lauf kommen nach dem Bericht. Ein späterer Lauf von `auswertung.py` auf demselben Selektionsraum läuft am Tag-Commit, sonst 2; nach R6 ist er nur als registrierte Messbitte zulässig oder ein Versuch.
> *Quelle des Grundes:* 14 (Reihenfolge), 19 (Tag-Commit = HEAD), R14 (Register-Hash zur Laufzeit), 17.2, R6. Kein Ergebnis.

> ⭐ **47.13 R30 BERICHTIGT durch R61 (51.6)** (Fable 01a R61, Unterpunkt (c), nachgetragen nach Fable 02a R65 (b), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: keine. Abschnitt 10: Indexzeile, keine Marke.

### 47.14 R31 — Tatsachennotizen 27c

> **R31 — Tatsachennotizen 27c.**
> (a) R8 (a) ist in TB-117 Block D berichtigt statt gestrichen; der neue Satz nennt den Ausgang 2 und die Quelle 44.1. Angenommen; „Streichung" in R8 (a) und R14 war Handwerk am Wortlaut.
> (b) `shared/test_sperrlistensonde.py` (8a, H7f) wurde in TB-117 Block C nach Grundsatz 40 nachgezogen, obwohl nur für Block B freigegeben; die alten Fassungen brechen genau dort. Angenommen. Regel: Eine Freigabe je Sperrlistendatei nennt deren Tests ausdrücklich mit.
> (c) Der TB-117-Auftrag nannte einen 0b-Wert für `auswertung.py`, den TB-116 nicht gemessen hatte; die Sitzung hat gegen das Abbild `5e5ad109…` gemessen. Regel des steuernden Chats (Zahlen aus früheren Ergebnissen nur mit Fundstelle) steht.
> (d) Zu 27.3: Die Registerkopie liegt in der Ablage seit TB-118 in vier Teilen mit festen Namen (`REGISTER_KOPIE_teil1–4.md`, Abschnitte 0–23 / 24–37 / 38–43 / 44–46, Commit `1e11457`, sha256 `18e39ee2…`, KOPIE) und `REGISTER_INDEX.md`; der Verfahrensprüfer hat am 29.09.2026 alle vier vollständig gelesen (je ein Suchtreffer, Abschnitt 0 dieser Antwort).
> (e) `FABLE_ANTWORT_2026-09-26a_…` liegt nicht in der Ablage (Übergabe 29.09. sagt das Gegenteil); ihr Registertext steht zeichengleich in 45.
> *Quelle des Grundes:* ERGEBNIS_TB-117, Übergabe 29.09., `project_info` 29.09.2026. Kein Ergebnis.

**Kette:** Marken: 27.3 (im Zitatblock 27.1 bis 27.5).

### 47.15 R32 — Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim dritten Umzug (29.09.2026)

> **R32 — Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim dritten Umzug (29.09.2026).** Der Chat des Verfahrensprüfers wurde am 29.09.2026 neu begonnen; er kennt aus dem Vorgängerchat nichts. Sein Wissensstand ist: der Wortlaut von `FABLE_UEBERGABE_2026-09-29_neuer_chat.md`; `REGISTER_INDEX.md` und `REGISTER_KOPIE_teil1–4.md` (Register 0–46, Commit `1e11457`, sha256 `18e39ee2…`, vollständig gelesen); aus der Ablage gelesen: `FABLE_ANFRAGE_2026-09-27c_…`, `ERGEBNIS_TB-116_leiter_lesarten.md`, `ERGEBNIS_TB-117_wachen_vor_dem_tag.md`, `FABLE_ANTWORT_2026-09-27a_…`, `FABLE_ANTWORT_2026-09-27b_…`, `UEBERGABE.md` (Stand 29.09.2026, 07:15), die Dateiliste der Ablage (43 Dokumente); als Suchausschnitt gesehen, nicht geöffnet: `BACKLOG_ENTSCHEIDUNGEN.md` (Einträge F2, Q1, E2) und `FABLE_UEBERGABE_2026-09-24_neuer_chat.md` (Abschnitt 2). Darin enthaltene Grössen, die an 27.1 grenzen: die Verfahrensgrössen des Registers (23.4, 24.6, 25.4, 32.2), gemessen nach vorher geschriebener Regel (27.2); die Budgetanteile und Multiplikatoren aus TB-116 (aufgezählte Stufentabellen, keine Kennzahl eines Parametersatzes). `BACKLOG.md`, `BACKLOG_ENTSCHEIDUNGEN.md`, `FABLE_ANTWORT_2026-09-25f_…`, `docs/belege/`, `ergebnisse/` und Trade-Listen: nicht gelesen. Weitere Grössen nach 27.1 kennt der Verfahrensprüfer nicht.
> *Quelle des Grundes:* 27, Tatsachennotiz zum Anfangsbestand (Bauart 21.09.); Übergabe 29.09. Kein Ergebnis.

**Kette:** Marken: Abschnitt 27.

