# TB-89 — Registerabschnitt 38: Fables vier Entscheidungen aus 22h, plus die Messungen aus TB-88

**Sitzungstitel:** `TB-89`
**Auftraggeber:** der steuernde Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD beim Schreiben:** `c140ca9`
**Vorgänger:** TB-88 (`ec54618`), TB-87 (`afe6192`), TB-86 (`ee4e65c`)

⛔⛔ **NUR REGISTERTEXT.** Keine `.py` ändern, kein neues Modul anlegen, keinen
Import setzen, kein Abbild erzeugen, die Sonde nicht anpassen, keinen Vollzug
ausführen, keinen Wert verschieben. **Drei Hashes vorher UND nachher.**

⭐ *Warum getrennt vom Code:* TB-84 trug die Schreibregel ein, TB-86 setzte sie
um. Ein Auftrag, der Code nach einer Regel ändert, die im Register noch nicht
steht, kehrt die Beweisrichtung um. **Der Code folgt als TB-90; die Freigabe
dafür liegt bereits vor (Betreiber, 22.09.2026).**

---

## 0. Der Anlass, in einem Satz

Fable hat in `docs/projektfuehrung/FABLE_ANTWORT_2026-09-22h_schluessel_und_vollzug.md`
**vier Entscheidungen** getroffen und **zwei eigene Sätze berichtigt**; TB-88 hat
dazu gemessen. Beides gehört ins Register, bevor eine Zeile Code entsteht.

---

## 1. Schritt 0 — der Arbeitsbaum

Im Arbeitsbaum liegt **eine geänderte Datei**, die nicht von dir stammt:
`docs/projektfuehrung/ARBEITSWEISE.md` (`numstat 10 0`, Abschnitt 7: Befehle für
den Betreiber sind **eine Zeile**). ⭐ **Committen, nicht entfernen.** Ebenso die
neu abgelegte Antwortdatei `FABLE_ANTWORT_2026-09-22h_…` und dieser Auftrag.
Danach `git status --porcelain` leer.

---

## 2. Die Quelle — und die Regel dazu

**Alle Blockzitate stehen zeichengleich in**
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22h_schluessel_und_vollzug.md`.

⚠️⚠️ **Zeichengleich heisst zeichengleich.** Nicht glätten, nicht kürzen, keine
Schreibweise angleichen, keine Zeilennummer ergänzen. Was gemessen wurde, steht
**daneben** als Tatsachennotiz, nie im Zitat.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text, Herkunft
und Grund **und** als Marke direkt beim alten Satz. Die alten Sätze bleiben
zeichengleich; `git diff --numstat` auf das Register zeigt in der zweiten Spalte
**`0`**.

---

## 3. Die Einträge — Abschnitt 38

| | Eintrag | Quelle in 22h | Marke am alten Ort |
|---|---|---|---|
| **38.1** | ⭐⭐ **Berichtigung zu 35.1 (Folge/Handwerk) — Weg (A):** die letzte Falte **heisst** die Spanne. Blockzitat, dazu Fables „Quelle des Grundes" und sein Absatz *„Zu eurem Einwand gegen (A)"* (33.3 führt die Selektionsfalten, die Bestätigungsperiode ist eigenes Feld; Schrägstrich statt Bindestrich mit Absicht) | Abschnitt 3 | **bei 35.1**, unter der bestehenden Marke |
| **38.2** | ⭐ **Registertext-Regel — Fundstellen:** Datei und Bezeichner, nicht Zeilennummer; Zeilennummern nur in Tatsachennotizen **mit Commit**. Blockzitat plus Quelle des Grundes | Abschnitt 4 | **bei 35.1** (die Tatsachennotiz zu den Zeilennummern, siehe 38.7 a) **und** im Kopf von Abschnitt 0 oder bei den Prüfprinzipien — ⭐ **du entscheidest, wo eine Regel für alle künftigen Registertexte hingehört; begründe die Wahl im Ergebnisdokument** |
| **38.3** | ⭐⭐ **Tatsachennotiz zu 21.9 und 10.1:** Der Vollzug von Sperrlistenpunkt 4 vor dem Tag ist eine beauftragte Änderung nach **37.3** — kein Amendment, kein Protokolleintrag; das Protokoll entsteht mit dem Erzeuger. Blockzitat plus Fables Begründung, warum 10.1 hier nicht greift | Abschnitt 5 | **bei 21.9** und **bei 10.1** |
| **38.4** | ⭐ **Sperrlistenpunkt 4 — Form (ii):** Punkt 4 nennt künftig **beide** Dateien; die alte bleibt gesperrt als registrierter historischer Stand, wie Punkt 2 (30.3). ⛔ **Die Form wird festgelegt, der Vollzug NICHT ausgeführt** — er ist Plan-Punkt 8 und hängt an zwei offenen Fragen (Anfrage 22i). Fables Ablehnung von (i) und (iii) zeichengleich mit aufnehmen | Abschnitt 5 | **bei Abschnitt 10, Punkt 4** — ⚠️ ausdrücklich *„Form steht fest, Vollzug steht aus"* |
| **38.5** | ⭐⭐ **Kosten — kein Laufmodul trägt eine eigene Kopie:** neun Importe aus einem neuen Modul, nicht neun überwachte Kopien. Blockzitat der Entscheidung **und** der Begründung *„Warum beseitigen und nicht überwachen"* (ein Import ist keine Prüfung, sondern eine Struktur). Dazu: Papierpfad und `messgroessen.py`/`GEBUEHR_PCT` bleiben **überwachte** Kopien; **Punkt 7 hat seinen Ort schon** (`registerdaten.py`, die beiden Konstanten) — Fables eigene Rücknahme seines 22d-Kandidaten | Abschnitt 2 | **bei Abschnitt 10, Punkt 9** und **bei Punkt 7** (beide tragen seit 37.5 eine Marke — die neue kommt **darunter**, die alte bleibt zeichengleich) · **bei 37.5** |
| **38.6** | ⚠️ **Fables zwei Berichtigungen an sich selbst:** (a) `auswertung.py` **Z. 51** statt Z. 41; (b) der **Ersatzsatz für 37.4** („an **acht** Stellen … vier fehlen … vier stehen zusätzlich"), zeichengleich. ⭐ **Der alte Satz in 37.4 bleibt stehen** und bekommt die ERSETZT-Marke | Abschnitt 1 | **bei 37.4** |
| **38.7** | ⭐ **Tatsachennotizen aus TB-88** (`docs/belege/TB-88/ERGEBNIS_TB-88.md`, Messstand `8851f67`) — siehe unten | TB-88 | bei 35.1 (a), bei Punkt 9 (b), bei 21.9/23.7 (c, d) |
| **38.8** | Schlussteil: **was 38 ausdrücklich NICHT tut** | — | — |

### Die Tatsachennotizen aus TB-88 (38.7)

| | Inhalt | wohin |
|---|---|---|
| **(a)** | Die Fundstellen aus 35.1 stehen heute auf **Z. 338** (Erzeugung) und **Z. 460** (Konsolenausgabe); verschoben durch **`4daa254`** (TB-86 Schritt 2/3). ⭐ *Damit ist 38.2 zugleich belegt* | bei 35.1 |
| **(b)** | ⭐⭐ **Slippage, Fables Messbitte:** **9 von 9** `backtest_*.py` tragen `SLIPPAGE_PCT = 0.05` und rechnen `2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)` = **0,30 %** — genau die Summe aus Punkt 9. ⚠️ Formabweichung ohne Wertunterschied bei `t3_supertrend` (`pnl_pct -= …`) | bei Punkt 9 |
| **(c)** | ⚠️⚠️ **Weg (B) hätte einen Sperrlistenpunkt berührt:** `auswertung.py` (Funktion `lies_zellen`) vergleicht die **Menge** der `falte`-Werte gegen die Faltennamen des Plans; unter (B) bricht es dort ab. *Damit steht Fables Entscheidung nicht nur auf einem Grund, sondern auf einer Messung* | bei 38.1 **und** als Marke bei 35.1 |
| **(d)** | ⚠️⚠️ **„rot" heisst heute: der Test stürzt ab** — `KeyError` in `auswertung.py` (Funktion `zulaessigkeit`), **0 bestanden, 0 gescheitert**. Die Simulation des Vollzugs ergibt **163 bestanden, 2 gescheitert** (`G6`, `H3`); beide hängen am **Faltenplan**, nicht an der Benchmark-Tabelle. ⚠️ **Damit ist Fables Fertigkriterium „`test_vorregistrierung.py` grün" (22h Abschnitt 5) heute nicht erreichbar** — die Frage liegt bei ihm (Anfrage 22i, Abschnitt 3) und ist **offen eingetragen**, nicht entschieden | bei 21.9 (wo der rote Test geführt wird) und bei 23.7 |

⭐ **(d) wird als offene Frage eingetragen, nicht als Entscheidung.** *Ein
Registerabschnitt darf eine offene Frage tragen — 21.6 hat es vorgemacht. Was er
nicht darf, ist sie stillschweigend beantworten.*

---

## 4. ⛔ Was NICHT geändert wird

| | |
|---|---|
| ⛔ | **Keine `.py`.** Weder `faltenplan.py` noch die neun `backtest_*.py`, und **kein neues Modul** |
| ⛔ | **Kein Vollzug** von Punkt 4 — nur die Form |
| ⛔ | **Kein neues Abbild**, keine Sonde angepasst, `python3 faltenplan.py` nicht aufgerufen |
| ⛔ | **Kein alter Registersatz umgeschrieben.** ERSETZT-Marken, nichts entfernt |
| ⛔ | **Kein `registerbericht.py`**, kein `test_vorregistrierung.py` |

---

## 5. ⛔ Abbruchkriterien

| | |
|---|---|
| ⛔ | `git diff --numstat` auf das Register zeigt in der zweiten Spalte **nicht** `0` |
| ⛔ | Einer der drei Hashes ändert sich (`benchmark_drawdowns.json`, `faltenplan.json`, `benchmark_drawdowns_vt.json`) |
| ⛔ | Eine Datei ausserhalb von `docs/` ist am Ende geändert |
| ⛔ | Ein Blockzitat weicht von der Quelldatei ab |

⭐ **Abbruchkriterium heisst ABBRUCH und Meldung — nie Rückfrage.**

---

## 6. Ins Ergebnisdokument

`docs/ERGEBNIS_TB-89_register_38.md`, Belege in `docs/belege/TB-89/`.

1. `numstat` auf das Register, **beide Spalten**
2. Die drei Hashes, **vorher und nachher**
3. **Die Marken einzeln aufgezählt** — wo jede steht und zu welchem Eintrag
4. Ein **Zeichenvergleich** je Blockzitat gegen die Quelldatei (`diff`), Ergebnis je Zitat
5. Wo du 38.2 (die Fundstellen-Regel) hingestellt hast — **und warum**
6. ⚠️ **Jede Abweichung** von diesem Auftrag ausdrücklich

**Danach Commit und Push**, Journalblock nach der üblichen Form.

---

## In einfacher Sprache

Der Verfahrensprüfer hat vier Dinge entschieden und zwei eigene Sätze berichtigt.
**Dieser Auftrag schreibt das ins Regelwerk — mehr nicht.** Kein Programm wird
angefasst.

Die vier Entscheidungen: Der Bestätigungszeitraum bekommt seinen Namen dort, wo
die letzte Zeitscheibe benannt wird, statt daneben. Regeltexte nennen künftig
Dateien und Namen statt Zeilennummern, weil Zeilennummern altern. Die angekündigte
Änderung an der Schutzliste braucht vor dem Stichtag kein förmliches Verfahren.
Und die Handelskosten sollen künftig an genau einer Stelle stehen, aus der die
neun Laufprogramme sie holen — statt neunmal kopiert und überwacht.

Dazu kommen die Messungen von gestern Abend als Vermerke: dass alle neun
Programme den zweiten Kostenanteil anwenden und die Summe stimmt; dass der andere
Weg beim Bestätigungszeitraum eine geschützte Datei berührt hätte; und ⚠️ **dass
ein Testprogramm, das laut Regelwerk „grün" werden soll, heute schon vor der
ersten Prüfung abstürzt und auch nach der geplanten Änderung zwei Prüfungen rot
behalten wird.** Das steht als **offene Frage** im Regelwerk — nicht als Antwort.
