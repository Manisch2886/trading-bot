# REGISTER-KOPIE Abschnitt 30 (von 0–56) — Register-Z. 5458–5591 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 30. Was der gesperrte Faltenplan ist — und was der Plan nach 4a ist (Fable 21i, 21.09.2026)

⭐ **Neuer Registertext.** Er trennt zwei Dinge, die bis heute denselben Namen
trugen: die **gesperrte Datei** `ergebnisse/faltenplan.json` und den
**Faltenplan nach 4a**. Dazu zwei Präzisierungen zu den Abschnitten 28 und 29,
die aus derselben Antwort stammen (30.6, 30.7).

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21i_gesperrter_faltenplan.md`,
zeichengleich. Anlass: die Messmeldung
`FABLE_ANFRAGE_2026-09-21b_messmeldung_vorlauf_und_kapitalpfad.md`, Abschnitt (C).

### 30.1 Der Befund — die gesperrte Datei stammt aus einem anderen Verfahrensstand

**Gemessen 21.09.2026 an
`research/vorregistrierung/ergebnisse/faltenplan.json` (`0e54ac5c…`):**

| | |
|---|---|
| ⚠️ | Die Datei führt je Falte ein Feld **`training_bis_ausschliesslich`** (Beispiel `2018-12-14`) und ein Feld **`embargo_tage: 18`**. ⭐⭐ **Verfahren B hat ausdrücklich KEIN Trainingsfenster** (V5c, Fable 15.09.2026) |
| ⚠️ | Erste Selektionsfalte `turtle_soup_stocks` im gesperrten Plan: **2019** — nicht 2017 oder 2018 |
| ⚠️ | TB-72 hat einen neuen Plan **daneben** gelegt (`ergebnisse/faltenplan_tb72.json`); der gesperrte ist unberührt, aber er ist **nicht** der Plan nach 4a |

⇒ **Die Frage, die Fable stellte, war an dieser Datei nicht beantwortbar.** Nach
`A2` ist *„konnte nicht messen"* ein eigenes Ergebnis, nicht grün und nicht rot.

### 30.2 Der Registertext, zeichengleich

> **Registertext (zu 26 / Sperrliste):**
> **(1)** `faltenplan.json` (0e54ac5c…) bleibt gesperrt und unverändert. Er ist der **registrierte historische Stand** eines früheren Verfahrensstands (Trainingsfenster, Embargo); er ist **nicht** der Faltenplan nach 4a und wird vom Lauf nicht gelesen. Sperrlistenpunkt 2 erhält eine Tatsachennotiz mit diesem Satz — kein Ersatz, keine Streichung.
> **(2)** Der Faltenplan nach 4a ist **Registertext**: je Bot die Liste der Selektionsfalten (Kalenderjahre), abgeleitet aus asof, `RECENT_YEARS_ONLY`, dem Indikator-Vorlauf gegen den Horizontbeginn und dem Trockenlauf nach 3b (b). Der Registertext ist die Quelle; jede Datei, die ihn maschinenlesbar wiedergibt, ist Abbild.
> > ⚠️ **Berichtigt (34.3, TB-82, 22.09.2026):** „Trockenlauf nach 3b (b)" lies **„3b (a)"** — Fable 21m, Frage 3, zeichengleich: *„Gemeint ist der Trockenlauf aus 3b (a), der die `MIN_HISTORY_*`-Tabelle aus 3b (b) anwendet; ein zweiter Trockenlauf existiert nicht."* Der Satz oben bleibt zeichengleich stehen; 16.7: 3b (a) ist der Trockenlauf-Satz, 3b (b) die `MIN_HISTORY_*`-Tabelle.
> **(3)** Genau **eine** solche Datei wird vor dem Tag mit Hash in die Sperrliste aufgenommen (neuer Punkt), und der Lauf liest genau diese. Ihr Inhalt muss dem Registertext aus (2) entsprechen; der Abgleich (Datei gegen Registertext, je Bot, je Jahr) ist eine Prüfung vor dem Tag und wird als Tatsachennotiz mit Ergebnis eingetragen. Trägt eine Datei Felder, die 4a nicht kennt (Trainingsgrenzen, Embargo), ist sie nicht dieses Abbild.
> > ⭐ **Präzisiert (35.4, TB-83, 22.09.2026):** „und der Lauf liest genau diese" — Fable 22a, zeichengleich: *„Der Lauf verwendet den Plan, den `faltenplan.py` zur Laufzeit bildet. Die Sonde vergleicht diesen Plan **vor dem Start des Laufs** mit dem Abbild (Feldmenge und Werte); bei Abweichung bricht der Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Das Abbild ist damit der registrierte Sollzustand, gegen den der gerechnete Plan geprüft wird — nicht die Datei, die `auswertung.py` öffnet."* Gemessen (Beleg M3): `auswertung.py` rechnet den Plan über genau einen Aufruf, `fp.faltenplan(mess)`, Z. 589. Der Satz oben bleibt zeichengleich; Sonde und Wrapper sind nicht geschrieben.
> **(4)** Ob `faltenplan_tb72.json` diese Datei ist, entscheidet allein der Abgleich nach (3) — nicht ihre Herkunft.

> ⭐ **Eingaben in der Gruppe `eingefroren`: siehe 45.3, vollzogen in 45.11**
> (Fable 26a R3, TB-114, 26.09.2026). Der Registertext oben bleibt
> zeichengleich.

**Quelle des Grundes,** Fable wörtlich: *„Das Register ist append-only …
Ersetztes bleibt mit Marke stehen — das gilt für Dateien in der Sperrliste
genauso wie für Sätze. Und 4a definiert die Falten als Funktion registrierter
Konstanten plus Trockenlauf … ein Plan, der ein Trainingsfenster kennt, kann
diese Funktion nicht sein."* Kein Ergebnis; **welche Jahre herauskommen, spielt
für die Regel keine Rolle.**

⭐⭐ **Warum nicht „ersetzen und den alten von der Sperrliste nehmen",** wörtlich:

> *„Die Sperrliste beweist, dass nichts bewegt wurde. Einen Punkt zu entfernen, weil er obsolet ist, öffnet die Frage, wer ‚obsolet' entscheidet — und das ist genau die Stelle, an der später jemand einen unbequemen Punkt für obsolet erklären könnte. Ergänzen, markieren, stehen lassen."*

### 30.3 Die Tatsachennotiz zu Sperrlistenpunkt 2 — und warum sie dort steht

⭐ **Handwerksentscheidung, gemessen:** Die Sperrliste kennt die Form bereits.
**Punkt 8** trägt seit Abschnitt 15 eine eingerückte Notiz unter dem Punkt
(*„⚠️ Der Halbsatz ‚vier Jahre Vorlauf je Symbol' ist ersetzt (Abschnitt 15,
Registertext 3) …"*). **Kein neues Element** — Punkt 2 bekommt dieselbe Form.
*Fable hatte das offengelassen: „ob die Sperrliste heute schon eine Form für
‚Tatsachennotiz zu einem Punkt' kennt … Handwerk, eure Wahl."*

⚠️ **Es ist ein reiner Zusatz** — Abschnitt 10 verliert keine Zeile.

⚠️ **Folge der Einfügung, gemessen beim Eintragen (TB-78):** Die sieben
Notizzeilen unter Punkt 2 verschieben jede Zeilennummer unterhalb von Z. 818
um **+7**. Alle Zeilenangaben in den Abschnitten 26 bis 29 (etwa Z. 4296,
Z. 4307, Z. 3897) gelten für den Stand `83e3a85`; im aktuellen Stand liegen
sie sieben Zeilen tiefer. *Eine Zeilenangabe im Register trägt ab hier ihren
Commit-Stand mit.*

### 30.4 Fables Rückfrage nach der Herkunft der Faltenmenge — beantwortet: steht

Er fragt, **nur das Ob**, gegen welchen Plan die 64 Falten aus 24.6 und die
„sieben statt acht" für `t3_supertrend` aus 25 gezählt wurden — *„damit die
Zahlen dort nicht mit dem Plan nach 4a verwechselt werden"*.

| | steht dort schon? | Fundstelle |
|---|---|---|
| **24.6** | ✅ **ja, wörtlich** | Z. 3897 (Stand `83e3a85`): *„Falten aus `research/vorregistrierung/ergebnisse/faltenplan_tb72.json` (TB-72)"* |
| **25** | ✅ **ja, und stärker** | Abschnitt 25 ist der Abschnitt, der `faltenplan_tb72.json` **erzeugt** hat (25.4; *„der neue Plan, daneben; `faltenplan.json` (`0e54ac5c…`) unberührt"*) |

⇒ ⭐ **Seine Bedingung ist erfüllt** (*„Wenn sie schon dort steht, genügt
‚steht'"*). **Keine Nachtragszeile an 24.6 oder 25** — beide sind append-only
abgeschlossen.

⚠️ **Festgehalten, weil es die Verwechslung benennt:** Weder 24.6 noch 25 zählt
gegen den **gesperrten** Plan (`0e54ac5c…`); beide zählen gegen
`faltenplan_tb72.json`. ⛔ **Und keiner von beiden ist der Plan nach 4a** — der
existiert noch nicht.

### 30.5 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Den Faltenplan nach 4a ableiten und als Registertext eintragen** (30.2 (2)) | eigene Aufgabe, nächster Schritt vor dem Tag |
| ⛔ | **Eine Abbild-Datei auf die Sperrliste nehmen** (30.2 (3)) — setzt (2) voraus | dieselbe Aufgabe |
| ⛔ | **Den Abgleich `faltenplan_tb72.json` gegen den Registertext** — es gibt noch keinen Registertext, gegen den abzugleichen wäre. ⚠️ **Gemessen 21.09.2026 (TB-78, beim Eintragen):** die Datei trägt `training_bis_ausschliesslich` (77 Vorkommen) und `embargo_tage` (9 Vorkommen) — dieselben Felder wie der gesperrte Plan. *Der Nachtrag v2 hatte „trägt keine Trainingsfelder" angenommen; das ist an der Datei widerlegt und nicht übernommen.* Ob sie das Abbild ist, entscheidet nach 30.2 (4) allein der Abgleich; 30.2 (3) spricht in ihrer heutigen Form dagegen | dieselbe Aufgabe |
| ⛔ | **`faltenplan.json` anfassen** — byteweise `0e54ac5c…` | nie |

### 30.6 Präzisierung zu 28.6 — der Vorlauf-Satz ist ein Ersteintrag

⚠️ **28.6 trägt die Kategorie „Berichtigung (Registertext an Registertext)".
Sie ist präzisiert, und 28.6 bleibt zeichengleich stehen.**

**Fable, 21i Abschnitt 1 (A), wörtlich:**

> *„Eure Tatsache aus 26.2 löst meine Unsicherheit: Es gab im Register nichts zu streichen, der Satz ist zwischen zwei meiner Antworten verlorengegangen. Damit ist auch die Kategorie präziser als in 21c: kein Berichtigung *eines Registersatzes*, sondern **Ersteintrag** — der Satz kommt mit der 4a-Präzisierung erstmals in Registertext (26). Quelle des Grundes unverändert 4a/26; F17 ist erfüllt, die Kategorie ist Handwerk."*

⇒ **Gültig ist: Ersteintrag.** ⭐ **Die Einordnung folgt damit der Messung des
steuernden Chats** (*„Horizontbeginn" 0 Treffer, „4a, Präzisierung" 0 Treffer im
Register*) **und nicht der ersten Vermutung — auch nicht Fables eigener.**

⚠️ **Warum das mehr ist als ein Etikett:** Eine Berichtigung setzt einen Satz
voraus, der berichtigt wird. Gäbe es ihn, wäre er irgendwo in Kraft gewesen —
und dann müsste geprüft werden, was auf ihm ruht. **Es gab ihn nie.** *Die
Kategorie ist die Frage, ob etwas ersetzt wurde oder zum ersten Mal gilt.*

### 30.7 Ergänzung zu 29.2 — die Reihenfolge ist der Beleg, nicht die Zahl

**Fable, 21i Abschnitt 1 (B), wörtlich:**

> *„Die Zeile 4296 ist der Beleg, dass der Schaden im Register benannt war, bevor die Regel dagegen stand — das ist die richtige Reihenfolge, und sie soll so in der Tatsachennotiz zu 26 stehen."*

⭐⭐ **Damit ist Z. 4296 nicht bloss der einzige Treffer einer Suche, sondern
der Nachweis der Bauart 24.3:** *eine Regel, die vor der Messung steht, kann
durch die Messung nicht gewählt worden sein.* ⚠️ **Wäre es umgekehrt** — erst
die Wirkung gemessen, dann die Regel geschrieben —, **wäre 29.3 eine
nachträgliche Wahl**, gleich wie gut sie begründet wäre.

⚠️ **Und die Grenze, damit der Beleg nicht überdehnt wird:** Z. 4296 belegt,
dass der **Schaden** benannt war. Sie belegt **nicht**, dass jemand seine Grösse
kannte — die ist bis heute nicht gemessen (29.5) und soll es nach 27.1 vor dem
Tag auch nicht werden.

---

