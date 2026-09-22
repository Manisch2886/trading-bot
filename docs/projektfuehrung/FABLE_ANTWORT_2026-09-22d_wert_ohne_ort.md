# FABLE_ANTWORT 2026-09-22d — Ein Wert ohne Ort ist eine Festlegung, keine Sperre; Tatsachennotiz zu den zwei Listen; die Sonde prüft auch „bestimmte" Pfade

*Bezug: `FABLE_ANFRAGE_2026-09-22c_herkunft_gemessen.md` (08:10) und `FABLE_ANFRAGE_2026-09-22d_klassifikation_berichtigt.md` (09:35). Beide zusammen beantwortet, weil 22d die Grundlage von 22c berichtigt. Zwei Entscheidungen vor dem Tag, eine Tatsachennotiz, eine Kenntnisnahme.*

---

## 1. Kenntnisnahme: die berichtigte Klassifikation

Zwei statt vier rein dateibezogene Punkte, zehn statt neun Pfade, erwarteter Nullpunkt-Lauf zwölf mal `2` — angenommen. Das ist kein schlechtes Ergebnis der Sonde, sondern ihr erstes richtiges: Sie zeigt, wie viel von Abschnitt 10 heute Text ist und wie wenig davon Messung. Meine Sondenentscheidung ruht nicht auf den Zahlen; meine Erwartung tat es, und sie ist berichtigt.

**Eine Präzisierung zur Sonde, damit die `2` nicht mehr verdeckt als sie zeigt:** Ein Punkt wie 14 („`auswertung.py` … Docstring") hat einen messbaren Teil (der Datei-Hash) und einen unmessbaren (der Docstring-Anteil). Eine Sonde, die den ganzen Punkt mit `2` meldet, macht den messbaren Teil unsichtbar.

> **Präzisierung zu 36.5 (Sonden-Ausgänge), Vorschlag:** Die Sperrlisten-Sonde meldet **je Punkt je Bestandteil**: für jeden genannten Pfad 0 oder 1 (Hash gegen Abbild), für jeden nicht messbaren Bestandteil 2 unter Nennung des Wortlauts. Der Gesamtwert eines Punktes ist 1, wenn ein Bestandteil 1 ist; sonst 2, wenn ein Bestandteil 2 ist; sonst 0. Der Gesamtwert des Laufs entsprechend. Am Tag gilt: Kein Pfad-Bestandteil darf 1 sein, und jeder Bestandteil mit 2 hat eine Tatsachennotiz, die sagt, wie er stattdessen geprüft wurde (Lesen, Beleg im Auftrag) — oder der Punkt wird bis zum Tag so nachgetragen, dass er messbar ist.

*Quelle des Grundes:* A2 (nicht prüfbar ist ein eigenes Ergebnis — aber je Sache, nicht je Punkt) und 22c. Kein Ergebnis.

**Zum Vorschlag aus 22c Abschnitt 4** (Sonde meldet `2` für jeden Punkt, dem der Registertext nichts Messbares gibt; „die Sonde erfindet keinen Pfad"): richtig, angenommen, und mit der Präzisierung oben verfeinert. Die TB-85-Sitzung hat sich genau richtig verhalten.

## 2. Frage aus 22c: prüft die Sonde auch „für die Sperrliste bestimmte" Pfade? — Ja, und bis zum Tag gibt es keine mehr

> **Ergänzung zu 36.6 (Abbild der Sperrliste):** Das Abbild führt zwei Gruppen: die **Punkte** des Abschnitts 10 und die **bestimmten** Pfade — Dateien, die das Register für die Sperrliste vorsieht, deren Vollzug aber aussteht (heute: `ergebnisse/benchmark_drawdowns_vt.json`, 21.9/23.7). Die Sonde prüft beide Gruppen gleich (Hash gegen Abbild) und weist die Gruppe im Bericht aus. **Am Tag ist die zweite Gruppe leer:** Jeder bestimmte Pfad hat bis dahin seinen Punkt in Abschnitt 10, oder das Register sagt, warum nicht.

*Quelle des Grundes:* Schreibregel 22b (1) („oder für sie bestimmt ist") — was die Schreibregel schützt, muss die Sonde sehen; sonst ist der Schutz eine Regel ohne Wache (A8). Und die Sperrliste ist am Tag vollständig oder sie ist keine. Kein Ergebnis.

## 3. Tatsachennotiz zu Abschnitt 10 — die zwei Listen in `herkunft.py` (meine, wie zugesagt)

> **Tatsachennotiz zu Abschnitt 10 (22.09.2026):** `research/vorregistrierung/herkunft.py` trägt zwei Listen. **`EINGEFROREN`** (Z. 57, zehn Einträge) ist die Eingabe von `register()` (Z. 114): ein Gesamthash über die Registerdatei plus diese zehn Dateien, laut Docstring „über die eingefrorenen Festlegungen" — sie bildet die Menge aus **Abschnitt 0** ab, nicht die Sperrliste aus Abschnitt 10, und weicht von dieser an fünf Stellen ab (fehlend: `benchmark_drawdowns_vt.json`, `config/top25_symbols.txt`, `config/sp500_top150.txt`; zusätzlich: `kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`). **`SPERRLISTE_DATEIEN`** (Z. 66) wird von keiner Stelle gelesen — toter Code. Keine der beiden Listen ist das Abbild der Sperrliste (36.6). `herkunft.py` wird in `research/vorregistrierung/` von keinem Modul importiert; `herkunft.json` und `herkunft_protokoll.jsonl` existieren nicht; die einzigen Aufrufer von `block()` gehören zu `research/turn_of_month/`. Sperrlistenpunkte 11 und 12 verweisen damit auf Funktionen, die im Laufbereich heute niemand aufruft; der Datenvertrag (`auswertung.py` Z. 41) verlangt `herkunft.json` als Pflichteingabe. Der Erzeuger (Nachtrag 2) ist die Stelle, an der `register()` und `datenstand()` erstmals aufgerufen werden.

**Folge für `herkunft.py`, Entscheidung:** **Nicht öffnen.** Der Erzeuger ruft `register()` auf und schreibt in `herkunft.json` **auch das Feld `teile`** (das `register()` liefert und `block()` weglässt) — dann ist lesbar, welche Dateien in den Gesamthash eingingen, ohne dass `block()` oder `herkunft.py` geändert wird. `herkunft.json` bezeugt damit die Abschnitt-0-Menge (zehn Dateien plus Register); die Sperrlisten-Sonde bezeugt Abschnitt 10; die Tatsachennotiz oben sagt, welches Dokument was bezeugt. Zwei Nachweise mit verschiedenem Gegenstand sind kein Widerspruch — zwei Nachweise mit demselben Gegenstand und verschiedenem Inhalt wären einer. *Quelle des Grundes:* 21b (3), Einfrieren vor Umbau; der Erzeuger ist neuer Code, dort darf alles stehen. Kein Ergebnis.

## 4. Die Entscheidung aus 22d: Werte ohne Ort (Punkte 7 und 9)

**Der Befund in einem Satz:** Ein Sperrlistenpunkt, der einen Wert nennt und keinen Ort, sperrt nichts — er legt fest. Festlegen ist Aufgabe der Festlegungen und des Registertexts; die Sperrliste soll sagen, **was unverändert bleibt**, und das ist immer eine Datei (oder ein Ort in einer). „Ändert jemand `TRADING_FEE_PCT` in einer der neun `forward_test.py`, merkt es kein Sperrlistenpunkt" ist genau der Zustand, den der Tag ausschliessen soll.

**Zu den drei Wegen:** *(iii) so lassen und Notiz* — nein: eine Tatsachennotiz macht eine Lücke sichtbar, sie schliesst sie nicht; der Tag friert dann eine Sperrliste ein, von der man weiss, dass sie zwei Werte nicht schützt. *(i) Ort je Punkt nachtragen* allein — nicht ausreichend, denn der Ort, den man heute misst (neun `forward_test.py`), ist nicht notwendig der Ort, aus dem der **Lauf** den Wert liest: `forward_test.py` ist der Papierpfad; die Optimierer und der noch zu schreibende Erzeuger sind der Laufpfad. Neun Kopien eines Werts als Sperrlistenorte einzutragen registriert die Kopien, nicht die Quelle. *(ii) Werte in eine Datei ziehen und sperren* — das ist der Kern, aber „ziehen" darf keine Kopie mehr erzeugen.

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Registertext, Ersteintrag — Ort registrierter Werte:**
> **(1)** Jeder Sperrlistenpunkt, der einen Zahlenwert registriert (heute 7 und 9), nennt **genau ein** Modul und dort **genau eine** Konstante, aus der der Lauf diesen Wert liest. Dieses Modul steht mit Hash auf der Sperrliste; die Sonde prüft für den Punkt Datei-Hash **und** Wert der Konstante (Bauart „Datei plus Konstante", wie Punkte 3, 4, 10).
> **(2)** Der Laufpfad (Optimierer, Equity-Simulation, Erzeuger) liest registrierte Werte ausschliesslich aus diesem Modul — kein Laufmodul trägt eine eigene Kopie. Für den Papierpfad (`forward_test.py`) gilt das nicht als Sperre, aber als Konsistenzprüfung: Die Sonde meldet als Befund, wenn eine Kopie dort vom registrierten Wert abweicht.
> **(3)** Für Punkt 9: `TRADING_FEE_PCT` und `SLIPPAGE_PCT` in einem Modul; für Punkt 7: `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` in einem Modul. Welche Module (Kandidaten nach heutiger Messung: `messgroessen.py` für 9, `registerdaten.py` für 7) und ob eines der beiden Module bereits Abschnitt-0-eingefroren ist und deshalb ein neues kleines Modul die Werte tragen muss — **Handwerk mit Freigabe**, aber die Tatsachennotiz zu 7 und 9 nennt am Ende Modul, Zeile und Wert.
> **(4)** Tatsachennotiz zu 7 und 9, jetzt: die heute gemessenen Orte (neun `forward_test.py`; `messgroessen.py:59`; `registerdaten.py:99`, `:115`) mit dem Vermerk, dass der Registertext keinen davon nennt und der Zustand bis zur Umsetzung von (1)–(3) ungeschützt war.

*Quelle des Grundes:* Zweck der Sperrliste (Übergabe Abschnitt 5) und A8; der Grundsatz ein Wert, ein Ort aus 21j. **Kein Ergebnis — und das ist hier wichtig zu sagen:** Die Werte selbst (0,1 / 0,05 / die beiden aus Punkt 7) ändern sich nicht um ein Zeichen; es ändert sich nur, wo sie stehen und dass jemand es merkt, wenn sie sich ändern.

*Warum die Optimierer die Kosten heute vielleicht gar nicht aus `forward_test.py` lesen:* Das habe ich nicht gemessen und ihr nicht gefragt. **Nur das Ob, vor der Umsetzung:** Woher beziehen die neun `multi_symbol_optimise.py` und `equity_simulation.py` heute Kosten und Slippage — aus einer eigenen Konstante, aus `forward_test.py`, aus `messgroessen.py`, oder gar nicht? Wenn die Antwort „aus einer eigenen Konstante je Bot" lautet, gibt es neun weitere Kopien, und (2) ist grösser als eine Zeile.

## 5. Was daraus auf die Liste kommt

An TB-84/85 anschliessend, in dieser Reihenfolge: Präzisierung 36.5 (je Bestandteil) → Ergänzung 36.6 (Gruppe „bestimmt") → Tatsachennotiz zu 10 (Abschnitt 3 oben) → Registertext „Ort registrierter Werte" mit Tatsachennotiz (4) → Messung „woher lesen die Optimierer Kosten" → dann Handwerk (3) mit Freigabe. Der Vollzug von `_vt.json` als eigener Punkt gehört ebenfalls vor den Tag.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 22c; dazu ANFRAGE 22c, ANFRAGE 22d. Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…86`, `VORARBEIT_sperrlisten_sonde.md`, `BACKLOG.md`; `REGISTER_KOPIE_2026-09-21.md` nur bis Abschnitt 27.

---

**Kurz:** Klassifikation berichtigt — angenommen; zwölf mal `2` ist der ehrliche Zustand von Abschnitt 10. Sonde meldet künftig je Punkt je Bestandteil, damit der Datei-Hash nicht hinter einem unmessbaren Docstring verschwindet; am Tag kein Pfad mit 1 und jede 2 mit Notiz. Sonde prüft auch „bestimmte" Pfade, und am Tag gibt es keine mehr. Tatsachennotiz zu den zwei Listen steht (Abschnitt 3); `herkunft.py` wird nicht geöffnet — der Erzeuger schreibt `teile` selbst. Werte ohne Ort: keiner der drei Wege, sondern die Regel „ein Modul, eine Konstante, auf der Sperrliste, Sonde prüft Datei und Wert; der Laufpfad liest nur dort; Kopien im Papierpfad werden auf Gleichheit geprüft". Werte bleiben zeichengleich. Eine Messung vorher: woher lesen die Optimierer heute Kosten und Slippage.

**Unsicher:** ob `messgroessen.py` und `registerdaten.py` als Abschnitt-0-eingefrorene Dateien für (3) noch geändert werden dürfen — wenn nicht, trägt ein neues kleines Modul die vier Werte, und die eingefrorenen Dateien bleiben stehen. Das seht ihr im Register (Abschnitt 0 und 15.8), ich nicht.

---

## In einfacher Sprache

Zwei Anfragen, eine Antwort. Erstens: Die Aufstellung von heute Morgen war an drei Stellen zu optimistisch, und das neue Prüfprogramm wird beim ersten Lauf bei zwölf von vierzehn Schutzpunkten „nicht prüfbar" melden. Das ist richtig so — es zeigt, wie viel von der Schutzliste heute nur Text ist. Fable verfeinert die Prüfung: Sie soll je Punkt sagen, welcher Teil prüfbar war und welcher nicht, statt den ganzen Punkt abzuhaken oder zu verwerfen.

Zweitens der ernste Fund: Zwei Schutzpunkte nennen Zahlen (etwa die Handelskosten), aber nicht, wo sie im Programm stehen. Tatsächlich stehen sie an zehn Stellen, und keine ist geschützt. Fable entscheidet: Jeder registrierte Wert bekommt genau einen Ort, dieser Ort kommt auf die Schutzliste, das Prüfprogramm kontrolliert Datei und Wert, und der grosse Lauf liest den Wert nur von dort. Die Zahlen selbst ändern sich nicht. Vorher soll gemessen werden, woher die Optimierer die Kosten heute überhaupt beziehen. Und die zwei alten Listen im Herkunftsprogramm bekommen ihren Vermerk: Die eine gehört zu einem anderen Zweck, die andere wird von niemandem gelesen; das Herkunftsprogramm selbst muss nicht angefasst werden.
