# Journal-Nachtrag (j) — 20.09.2026, TB-72 Schritt 1: die Messung, die den Auftrag angehalten hat — 4a und 3b (a) laufen bei sechs Bots auseinander, fünfmal in die andere Richtung

**Quelle:** Mac-Sitzung **TB-72 erste Falte aus Trockenlauf**, 20.09.2026,
zweiter Anlauf ab 19:50 Ortszeit (der erste bis 19:20, Verbindungsabbruch nach
Schritt 1), Ausgang `25f568a` (= `origin/main` beim Start), Interpreter
`trading-env/bin/python3` 3.9.6. **Rein lesend am Code**: kein Bot-Code, kein
`faltenplan.py`, kein `benchmark.py`, keine Ergebnisdatei angefasst. Commits
`c63bfed` und `14c796b` (Schritt 0, nach Urheber getrennt), `0562c75` und
`72e512f` (Schritt 1 nachgemessen), dann dieser Nachtrag, eine Backlog-Zeile
`K4k` und das Ergebnisdokument `docs/ERGEBNIS_TB-72_schritt1_erste_falte.md`.
**Einzuarbeiten als nächster Block nach dem höchsten vorhandenen** (am
20.09.2026 gemessen: `BT`; `(20g)`, `(20h)`, `(20i)` liegen davor — die Nummer
vergibt die einarbeitende Sitzung).

⭐ **Quellenzeile für den Block, wörtlich zu übernehmen:**

```
*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20j.md`*
```

---

## Was der Auftrag wollte und was er bekam

TB-72 sollte zweierlei: `t3_supertrend` nach Register 21.3 (b) auf 2019
berichtigen (die *Instanz*) und `faltenplan.py` die erste Falte aus dem
Trockenlauf ableiten lassen statt sie nach 4a nachzurechnen (die *Schliessung
der Klasse*, Fables Vorschlag vom 20.09., Antwort d, Abschnitt 2). **Schritt 1
war die Messung in beide Richtungen, bevor eine Zeile Code fällt** — und sie
hat den Auftrag angehalten. Der HALT-Nachtrag des Betreibers (19:40) hat
daraus fünf Punkte für diese Sitzung gemacht: Schritt 0, Schritt 1
nachmessen, die Gegenprobe gegen TB-56 nachprüfen, ein Ergebnisdokument nur
über Schritt 1, Stopp vor Schritt 2.

**Bekommen hat er alle fünf.** Die Nachmessung ist mit dem ersten Anlauf
**byteweise gleich** (JSON `fb68537a…`, 4 min 51 s, rc 0); eine zweite,
vom Kindprozess unabhängige Methode (`faltenschranke_messung.loader_lesart`,
Nachrechnung aus den fünf registrierten `MIN_HISTORY_*`) nennt **9/9**
dieselben Jahre; die Vormessung des Chats aus `benchmark_drawdowns_vt.json`
ist aus derselben Datei nachvollzogen. Hashes der drei Sperrlisten-Dateien
vorher = nachher (`a163c498…`, `4549395f…`, `0e54ac5c…`).

| Bot | Plan = 4a | Trockenlauf ab 4a | Trockenlauf beide Richtungen | |
|---|---:|---:|---:|---|
| `t3_supertrend` | 2018 | **2019** | 2019 | später (1 Bot) |
| `rsi2_crypto` | 2019 | 2019 | **2018** (`H = 2`, BTC/ETH ab 2018-12-30) | früher |
| vier Aktien-Bots | 2017 / 2018 | 2017 / 2018 | **1967** (`H = 16`, 1962-01-02 + 1 825 Tage) | früher |
| die drei anderen Krypto-Bots | 2018 | 2018 | 2018 | gleich |

---

## Drei Befunde

### 1. ⭐⭐ Eine Regel ohne Richtung bindet in beide — und die Begründung daneben meint nur eine

Register 21.3 (b) sagt *„Ergeben 4a und 3b (a) für einen Bot verschiedene
erste Falten, bindet 3b (a)"*. Der Satz hat keine Richtung. Seine Begründung
im selben Absatz hat eine: *„Eine Falte, in der der Loader kein Symbol
handelbar macht, erzeugt keinen Trade"* — das rechtfertigt, den Beginn nach
hinten zu schieben, und sagt nichts über nach vorn. Fables Vorschlag, den Plan
aus dem Trockenlauf abzuleiten, trug dieselbe Einseitigkeit als Prämisse
(*„`MIN_HISTORY_*` macht Symbole **später** handelbar"*). Gemessen ist das bei
**einem** Bot der Fall und bei **fünf** das Gegenteil, weil 4a mit *„Universum
… liegt vor"* eine Bedingung trägt, die der Trockenlauf gar nicht prüft: er
misst den Loader gegen den Kursbestand bis zum Faltenende, und der reicht bei
den Aktien bis 1962.

⭐ **Regel:** *Bevor eine Regel „X bindet" operativ umgesetzt wird, ist zu
messen, in welche Richtungen X überhaupt vom bisherigen Wert abweichen kann —
und ob die Begründung der Regel alle diese Richtungen deckt. Deckt sie nur
eine, ist die Umsetzung eine Auslegung und keine Ableitung.* Der Auftrag hat
das mit *„Prüfe beide Richtungen — später und früher"* verlangt; ohne diesen
Satz wäre Schritt 2 gelaufen und hätte vier Bots fünfzig Jahre gegeben.

### 2. ⭐ „Alle gleich: ja" war wahr — und hätte trotzdem in die Irre geführt

Die Gegenprobe des ersten Anlaufs gegen TB-56 (`trockenlauf_ohne_schranke`)
meldet für alle neun Bots „gleich". Nachgeprüft: Das Flag vergleicht die
TB-56-Falte mit dem Trockenlauf **ab 4a**, nicht mit der Spalte „beide
Richtungen" — und das ist zutreffend, weil TB-56 den vollen Trockenlauf auf den
Plan von `faltenplan_neun` ohne Schranke setzt, der **bei 4a beginnt**. Für die
Richtung „früher" ist diese Gegenprobe konstruktionsbedingt blind. Der Satz war
also kein Fehler; ohne die Einordnung liesse er sich aber als „der Trockenlauf
bestätigt die neun Zahlen in beide Richtungen" lesen. Deshalb steht im
Ergebnisdokument die Tabelle, **was** das Flag vergleicht, und daneben die
zweite Methode als Ersatz-Gegenprobe für die andere Richtung.

⭐ **Regel:** *Eine Gegenprobe nennt, welche Grösse sie vergleicht — nicht nur,
dass sie „gleich" sagt. Prüfprinzip A1 in anderer Form: ein „gleich" über den
sichtbaren Bereich sieht genauso aus wie ein „gleich" über alles.*

### 3. Die Vormessung aus dem Chat hatte recht, wo sie sehen konnte — und der Auftrag hat ihren blinden Fleck vorher benannt

*„Nur `t3_supertrend` weicht ab"* (Vormessung 19:00 aus `_vt.json`) trifft für
die Richtung „später" Zahl für Zahl. Die Datei enthält aber nur Falten, die im
Plan stehen; eine Falte **vor** dem Plan, die der Loader handelbar macht, ist
darin unsichtbar. Der Auftrag hat das selbst gesagt (*„Diese Messung hat einen
blinden Fleck, und du musst ihn schliessen"*) und verlangt, beide Zahlen zu
nennen und auszusprechen, ob die Vormessung getroffen hat. **Antwort: für
„später" ja, als Gesamtaussage nein.** Der erste Anlauf hat das gemessen, der
zweite reproduziert.

---

## Was der Auftrag anders sah — und wo die Messung galt

| Auftrag | gemessen / getan |
|---|---|
| Abschnitt 0, Fables Prämisse: Abweichung geht nur nach hinten | bei einem Bot; bei fünf nach vorn |
| Schritt 2 (Fassung vor dem HALT): `erste` aus dem Trockenlauf | wörtlich 1967 für vier Bots — nicht ausgeführt (HALT Punkt 5) |
| HALT Punkt 3: „alle gleich: ja" nachprüfen | wahr für „später"; für „früher" blind; Ersatz-Gegenprobe `loader_lesart` 9/9 |
| Schritt 3 (steht aus): Gegenüberstellung gegen `ergebnisse/faltenplan.json`, *„genau ein Bot, genau eine Falte"* | die Datei ist TB-30a-Stand (bekannt: TB-61 Z. 251); das gilt nur gegen den Speicherstand `faltenplan.faltenplan()`, den der erste Anlauf als `faltenplan_4a_stand_vor_tb72.json` festgehalten hat |

---

## Offen

| | wer |
|---|---|
| ⛔ **Fables Antwort** (`FABLE_ANFRAGE_2026-09-20e_erste_falte.md`, drei Fragen: Lesart `max(4a, 3b (a))`; Berichtigung oder Präzisierung von 21.3 (b); Satz zu „Universum liegt vor" in 4a) | Fable / steuernder Chat |
| Schritte 2–7 von TB-72 — Schritt 2 voraussichtlich in der Form aus der Anfrage (*„4a wie bisher UND Trockenlauf als Verschiebung nach hinten, in einer Funktion"*) | Sitzung nach der Antwort |
| `research/faltenplan_neun/erste_falte_trockenlauf.py` liegt gesichert, ohne Test, ohne Erwähnung in `BERICHT.md` | Schritt 5 |
| Dieser Nachtrag ins Journal (Block nach `BW`, falls `(20g)`–`(20i)` bis dahin `BU`–`BW` geworden sind) | nächste Einarbeitung / TB-64-Wächter |
| Projektablage nachziehen (`K4e`): Backlog geändert, neues Ergebnisdokument | steuernder Chat / Betreiber |
