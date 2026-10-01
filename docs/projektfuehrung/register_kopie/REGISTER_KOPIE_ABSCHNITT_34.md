# REGISTER-KOPIE Abschnitt 34 (von 0–50) — Register-Z. 6081–6291 — Commit db108a68ec57316250ca792a0673b5932dd0f0e8 — 2026-10-01 — Original sha256 b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1 — KOPIE, nicht das Register

## 34. Fünf Einträge des Verfahrensprüfers aus 21l/21m und eine Berichtigung eines eigenen Satzes — Faltenregeln, `horizontbeginn`, „vier" → „neun" (TB-82, 22.09.2026)

⭐ **Reines Eintragen von Registertext.** Fünf Einträge sind zeichengleich von
Fable (vier aus 21m, einer aus 21l), der sechste berichtigt einen Satz des
steuernden Chats in 33.4. **Kein Code, keine Abbild-Datei, keine Sonde, kein
Hash, keine Wache** — 34.7.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21m_faltenplan_pruefung.md`
(34.1–34.4) und `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21l_standpruefung.md`
(34.5), zeichengleich; 34.6 aus
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21g_berichtigung_und_bestaetigungsperiode.md`
Punkt 2 und 3. Auftrag `docs/auftraege/MAC_TB-82_register_34.md`; Messungen
`docs/belege/TB-82/` (M1–M5), alle **vor** dem Eintrag gemessen, HEAD `9614624`.

⭐⭐ **Neu in diesem Abschnitt — die Marke steht AM ALTEN ORT.** Jeder der sechs
Einträge ist an zwei Stellen sichtbar: hier mit vollem Text, Herkunft und Grund,
und **direkt unter dem berichtigten Satz** als eingerückter Hinweisblock mit
Verweis auf 34.x. Der alte Satz bleibt zeichengleich; die Marke fügt nur hinzu
(dieselbe Bauart wie die Tatsachennotiz unter Sperrlistenpunkt 2, Abschnitt 10
und 30.3). *Fables Grund, 21m Frage 3, wörtlich:* *„Wer 30.2 (2) liest und
abschreibt, sieht 33.2 nicht — genau der Fehler aus 21h. Eine Marke am falschen
Satz kostet eine Zeile; ein Hinweis drei Abschnitte weiter kostet irgendwann
eine Rücknahme."* Prüfbar: `git diff --numstat` auf dieses Register zeigt für
TB-82 in der zweiten Spalte `0`.

⭐ **Fables Regel aus dem Vorab von 21m, die ab hier für jeden seiner Texte gilt,
wörtlich:** *„Wo mein Registertext eine Tatsache über den Bestand voraussetzt (ein Feld, eine Datei, eine Zahl von Modulen), nenne ich sie als Voraussetzung, und ihr messt sie, bevor der Text eingetragen wird."* — deshalb tragen 34.1, 34.2, 34.5 und 34.6 je eine
Tatsachennotiz mit der Messung, die der Text voraussetzt.

### 34.1 Ergänzung zu 33.2 — Falten mit Faltenlänge L > 1

**Fable, 21m Frage 1 (1a), zeichengleich:**

> **Ergänzung zu 33.2:** Bei Faltenlänge L > 1 ist ein Kalenderjahr J erstes Jahr einer Selektionsfalte, wenn J die Bedingungen (i) und (ii) nach 25 erfüllt; die Falte umfasst J bis J + L − 1. Die erste Selektionsfalte beginnt mit dem ersten Kalenderjahr, das (i) und (ii) erfüllt; die folgenden Falten schliessen lückenlos an.

**Fables Grund, zeichengleich:**

> *Grund:* (i) prüft den Vorlauf am 1. Januar — der einzige 1. Januar, an dem eine Falte beginnt, ist der ihres ersten Jahres. (ii) muss am ersten Jahr geprüft werden, weil die Falte sonst mit Jahren beginnen könnte, in denen der Bot nichts handelt — der Kapitalpfad (29) startet am 1. Januar der ersten Falte und braucht dort Handelbarkeit.

**Tatsachennotiz (TB-82, gemessen vor dem Eintrag, `m5_faltenlisten.txt`):**
Betroffen ist nur `elliott_wave` (L = 2); die acht übrigen Bots haben L = 1,
für sie ist 34.1 die Regel aus 25 unverändert. Für `elliott_wave` ergibt der
Text, auf das erste Jahr 2018 angewandt und lückenlos fortgesetzt, genau die
vier Falten aus 33.2 (2018–2019 · 2020–2021 · 2022–2023 · 2024–2025).
⭐ **Die Faltenliste in 33.2 ändert sich durch diese Ergänzung nicht** — die
neun Tabellenzeilen sind vor und nach dem Eintrag zeichengleich (SHA-256 der
Zeilen im Beleg) und gegen 21.4 mit 0 Abweichungen.

**Marke am alten Ort:** unter 33.2, nach dem Registertext-Block.

### 34.2 Ergänzung zu 33.2 — der Rest vor dem Go-Live-Schnitt

**Fable, 21m Frage 1 (1b), zeichengleich:**

> **Ergänzung zu 33.2:** Ein Rest von weniger als L Kalenderjahren zwischen der letzten vollen Selektionsfalte und dem Go-Live-Schnitt ist keine Selektionsfalte. Sein Verhältnis zur Bestätigungsperiode regelt 21.4; 33.2 trifft dazu keine Aussage.

**Fables Grund, zeichengleich:**

> *Grund:* 4a kennt nur ganze Falten; eine Teilfalte hätte weniger Beobachtungen als die übrigen und ginge mit gleichem Gewicht in den Faltenmedian — eine Verzerrung, die 4a nirgends zulässt. Kein Ergebnis: Für den registrierten Bestand tritt der Fall nicht ein; die Faltenliste ändert sich um nichts.

⭐⭐ **Tatsachennotiz — Antwort auf Fables ausdrückliche Unsicherheit** (21m:
*„ob 21.4 den Rest vor Go-Live bereits regelt — dann ist (1b) ein Verweis statt
einer Regel"*), **gemessen von TB-82 vor dem Eintrag** (`m1_rest.txt`, HEAD
`9614624`; die Zahl des steuernden Chats vom 21.09. an `ad020b5` wurde nicht
übernommen, sondern nachgemessen): Gesucht wurde im ganzen Register nach
`Rest` (als ganzes Wort, mit Positivkontrolle der Wortgrenze), `Teilfalte` und
`angebrochene` — **null Treffer**, in zwei Lesungen (`\b` und `-w`). 21.4 führt
je Bot ausschliesslich Markt, Faltenlänge, erste Falte, Anzahl der
Selektionsfalten, „Bestätigung ab" und „4b erfüllt" (`m3_bestaetigung_ab.txt`).
⇒ **(1b) ist eine Regel, kein Verweis.** Für den registrierten Bestand tritt
der Fall nicht ein: Bei allen neun Bots enden die Selektionsfalten mit 2025;
zwischen der letzten vollen Falte und dem Go-Live-Schnitt `2026-09-01` liegt bei
allen neun derselbe Rest, `2026-01-01` bis `2026-09-01` — kürzer als L bei
jedem Bot, also nach 34.2 keine Selektionsfalte. Die Faltenliste ändert sich
um nichts (34.1, Beleg M5).

**Marke am alten Ort:** unter 33.2, zusammen mit 34.1.

### 34.3 Berichtigung zu 30.2 (2) — `3b (b)` lies `3b (a)`

**Fable, 21m Frage 3, zeichengleich:**

> **Berichtigung zu 30.2 (2):** Die Fundstelle „Trockenlauf nach 3b (b)" lies „3b (a)". Gemeint ist der Trockenlauf aus 3b (a), der die `MIN_HISTORY_*`-Tabelle aus 3b (b) anwendet; ein zweiter Trockenlauf existiert nicht.

**Fables Grund, warum ein eigener Satz und nicht nur der Zitierhinweis in 33.2,
zeichengleich:**

> *Warum nicht nur der Hinweis in 33.2:* Wer 30.2 (2) liest und abschreibt, sieht 33.2 nicht — genau der Fehler aus 21h. Eine Marke am falschen Satz kostet eine Zeile; ein Hinweis drei Abschnitte weiter kostet irgendwann eine Rücknahme. Meine Zitierregel (nur vorgelegte Fundstellen) hat hier versagt, weil ich „3b (b)" aus 20e übernommen hatte, wo es um die Handelbarkeitstage ging — dieselbe Unternummer, andere Sache.

⚠️⚠️ **Der Satz „Trockenlauf nach 3b (b)" in 30.2 (2) bleibt zeichengleich
stehen** (append-only) und trägt die Marke **direkt unter 30.2 (2)** — genau
dieser Eintrag ist der Anlass für die Regel „Marke am alten Ort" im Kopf dieses
Abschnitts. Der Zitierhinweis in 33.2 (TB-81) bleibt ebenfalls zeichengleich
stehen und bekommt einen Satz, dass die ausdrückliche Berichtigung in 34.3
steht. Gemessen (TB-81, Beleg Schritt 2, unverändert): In 16.7 ist **3b (a)**
der Trockenlauf-Satz, **3b (b)** die `MIN_HISTORY_*`-Tabelle; 21.3 (a), 21.4
und `erste_falte_quelle` zitieren 3b (a).

### 34.4 Ergänzung zu 33.3, Feld `horizontbeginn` — Zeichenkette oder Datum

**Fable, 21m Frage 4, zeichengleich:**

> **Ergänzung zu 33.3, Feld `horizontbeginn`:** Der Wert ist entweder ein Datum im Format `JJJJ-MM-TT` oder die Zeichenkette `"kein Horizont"` — genau eine der beiden Formen. JSON-`null`, ein fehlender Schlüssel oder eine leere Zeichenkette sind Fehlschläge der Sonde. Die Sonde prüft den Wert positiv gegen diese zwei Formen, nicht das Vorhandensein des Schlüssels.

**Fables Grund, zeichengleich:**

> *Grund:* Derselbe wie bei der Feldliste — eine **positive** Prüfung gegen eine abschliessende Menge ersetzt ein Urteil über Abwesenheit. `null` ist genau das Gegenteil: ein Wert, der „nichts" bedeutet und in einer Bibliothek von „fehlt" unterscheidbar ist, in der nächsten nicht (euer Befund). „Gesetzt, nicht weggelassen" hiess: Wer die Datei liest, soll *lesen*, dass der Bot keinen Horizont hat — nicht schliessen, dass ihm einer fehlt. Eine Zeichenkette tut das; `null` verlangt Kenntnis der Konvention. Folge: `faltenplan_tb80.json` (Schlüssel mit `null`) ist auch daran kein Abbild; das war es nach 33.3 schon nicht.

⭐ **Folge, die Fable selbst zieht und die hier eingetragen wird:**
`research/vorregistrierung/ergebnisse/faltenplan_tb80.json` — Schlüssel
`horizontbeginn` mit JSON-`null` bei den fünf Krypto-Bots (33.2, Lesehilfe;
TB-81 Schritt 1) — ist **auch daran** kein Abbild; *„das war es nach 33.3 schon
nicht"* (Feldmenge 18 statt der Feldliste). Damit ist die in TB-81 offen
gelassene Frage, ob `null` das „ausdrücklich gesetzt" aus 33.3 ist,
**entschieden: nein.** Die Zeile in 33.2 („kein Horizont" steht in der
gemessenen Datei als JSON-`null`) bleibt als Tatsachennotiz zur gemessenen
Datei richtig; für das Abbild gilt 34.4.

**Marke am alten Ort:** in der Feldliste 33.3, als eigene Zeile direkt unter
`horizontbeginn`.

### 34.5 Berichtigung zu 29.4 — „vier" → „neun" `multi_symbol_optimise.py`

**Fable, 21l Punkt 4 (b), zeichengleich:**

> **Berichtigung zu 29.4:** Die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte" wird in **allen neun** `multi_symbol_optimise.py` eingebaut, nicht nur in den vier Aktien-Optimierern. Der Bericht führt je Bot Horizontbeginn (oder „kein Horizont"), Beginn der ersten Selektionsfalte und frühesten Einstieg nebeneinander auf.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* Die Regel 29 (Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte) gilt je Bot für alle neun; 21c 3.2 hat den Fall für Krypto ausdrücklich benannt („rsi2_crypto: 2018 handelbar, erste Falte 2019"). „Die vier" stammt aus 21b, als die Wache noch gegen den Horizontbeginn prüfte, den nur Aktien-Bots haben. Mit dem Wechsel des Prüfdatums in 21c/29.4 hätte die Zahl mitwandern müssen; sie ist es nicht — mein Versehen, dieselbe Art wie der verlorene Vorlauf-Satz. Kein Ergebnis: Ob die Wache bei einem Krypto-Bot je anschlägt, ist für die Regel gleichgültig.

*Fables Einordnung, 21l, zeichengleich:* *„Kategorie: Berichtigung mit Ersatzwort, „vier" → „neun"; 29.4 bleibt stehen, Marke wie üblich."*

⭐ **Tatsachennotiz (TB-82, gemessen vor dem Eintrag, `m4_wachen_optimierer.txt`,
nur lesend):** In **keinem** der neun `strategies/<bot>/multi_symbol_optimise.py`
steht heute eine Wache — `assert `, `raise `, „Wache" je Datei **0**, in einer
zweiten, weiter gefassten Lesung (`assert`, `raise`, `wache` ohne Rücksicht auf
Gross-/Kleinschreibung, `Selektionsfalte`) ebenfalls **0**; neun Dateien, alle
vorhanden, SHA-256 je Datei im Beleg. ⇒ Der Einbau ist ein **Ersteinbau**, keine
Änderung — und er gehört zu **TB-30b**, nicht zu diesem Auftrag. Der Satz
„Ort der Wache unverändert: in den vier `multi_symbol_optimise.py`" in 29.4
bleibt zeichengleich stehen und trägt die Marke; unverändert gilt daraus:
**nicht** in `auswertung.py`.

**Marke am alten Ort:** unter 29.4, direkt am Absatz „in den vier
`multi_symbol_optimise.py`".

> ⭐ **34.5 BERICHTIGT durch R43 (48.11)** (Fable 29b R43, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 34.6 ⚠️ Berichtigung zu 33.4 Punkt 3 — eine Fundstelle des steuernden Chats trug ihren Satz nicht

⚠️ **Kein Fable-Eintrag, sondern die Berichtigung eines eigenen Satzes.** Was
in 33.4 Punkt 3 steht, bleibt zeichengleich: *„Sie steht **bereits** in
Register 21.4 und folgt aus Faltenlänge und Go-Live-Schnitt (`elliott_wave`
`2026-2027`, die acht übrigen `2026`)."*

> **Berichtigung zu 33.4 Punkt 3 (steuernder Chat, 21.09.2026; nachgemessen
> von TB-82 vor dem Eintrag, `m2_2026-2027.txt` und `m3_bestaetigung_ab.txt`).**
> Die Fundstelle „21.4" trägt den Satz nicht. **Gemessen:** 21.4 führt die
> Spalte **„Bestätigung ab"** mit dem Wert `2026-01-01` **für alle neun Bots**
> (9/9); die Werte `2026-2027` und `2026` als Faltenname kommen dort nicht vor
> (0 Treffer in den neun Zeilen, beide Strichformen). Gegenprobe über das ganze
> Register: `2026-2027` hat **genau einen** Treffer (Z. 5431 im Stand
> `9614624`), und das ist der berichtigte Satz selbst. **Die Werte stammen aus
> `research/vorregistrierung/faltenplan.py:336`** (`falten[-1]["name"]`, nur
> gelesen), also aus dem Code. **Registriert ist die Bestätigungsperiode
> gleichwohl** — ihr **Beginn** in 21.4 (`2026-01-01`), ihr **Ende** in 5.2
> (Go-Live-Schnitt `2026-09-01`, ausschliesslich), also als **Datumsspanne
> statt als Faltenname**. ⭐ **Fables Schluss in 21m Frage 2 (3) bleibt davon
> unberührt:** Sein erster Halbsatz — *„33.2 nennt sie nicht"* — trägt allein;
> die Bestätigungsperiode ist **kein Feld** der Feldliste.

⚠️⚠️ **Offen — hier eingetragen, nicht entschieden:**

> **Offen (an Fable, Anfrage 21g Punkt 3):** Der Begriff „Bestätigungsperiode"
> trägt zwei Formen — im Register eine **Datumsspanne** (`2026-01-01` bis
> `2026-09-01`), in `faltenplan.py` einen **Faltennamen**. Für `elliott_wave`
> klaffen sie: Der Name lautet `2026-2027`, die Periode endet am `2026-09-01`.
> ⚠️ **Welche Form gilt, ist nicht registriert.** Die Frage liegt bei Fable
> (Anfrage 21g); **dieser Abschnitt entscheidet sie nicht.**

> ⭐ **Beantwortet und ersetzt (35.1 / 35.3, TB-83, 22.09.2026):** Fable 22a hat
> entschieden — **die Datumsspanne gilt**; der Bezeichner ist die Spanne selbst,
> `JJJJ-MM-TT/JJJJ-MM-TT`, für alle neun Bots `2026-01-01/2026-09-01`; der Faltenname
> `2026-2027` ist unzulässig (35.1). Und der Schluss oben *„die Bestätigungsperiode
> ist **kein Feld** der Feldliste"* ist **ERSETZT**: `bestaetigungsperiode` ist Feld
> (35.2/35.3, Fables sechste Rücknahme — der Name ist ein Schlüssel, den
> `auswertung.py` und der Erzeuger teilen). Der Block oben bleibt zeichengleich.

**Marke am alten Ort:** in der Tabelle 33.4, als eigene Zeile direkt unter
Punkt 3.

### 34.7 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Abbild-Datei erzeugen** | eigene Aufgabe, eigene Betreiberfreigabe (33.5) |
| ⛔ | **Die Sonde schreiben** — auch nicht die positive Prüfung aus 34.4 | dieselbe Aufgabe |
| ⛔ | **Einen Hash auf die Sperrliste nehmen** | dieselbe Aufgabe |
| ⛔ | **`faltenplan.py` oder irgendeine `.py` ändern** — keine Freigabe; die vom 21.09. galt für Bedingung (i) und ist verbraucht | — |
| ⛔ | **Die Wache aus 29.4/34.5 einbauen** — sie ist Ersteinbau in allen neun Optimierern | TB-30b |
| ⛔ | **Die offene Frage aus 34.6 beantworten** | Fable (Anfrage 21g) |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (Beleg M5); die drei Sperrlisten-Hashes `0e54ac5c…`, `a163c498…`, `4549395f…` unverändert | — |

*Dieser Abschnitt ist rein additiv: Er trägt fünf Texte des Verfahrensprüfers
zeichengleich ein, berichtigt einen eigenen Satz, setzt zu jedem der sechs eine
Marke am alten Ort — und entfernt nichts.*

---

