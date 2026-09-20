# Journal-Nachtrag (f) — 20.09.2026, TB-66: der Benchmark wird tagesgenau — Fables Festlegung VT im Register, im Code und im Lauf

**Quelle:** Mac-Sitzung **TB-66 Benchmark tagesgenau**, 20.09.2026, 14:19 bis
etwa 15:10 UTC, `trading-env/bin/python3` 3.9.6, Ausgang `1e6fcc7`, Commits
`19a1996` (Code auf VT, Lauf daneben), `ec7eff4` (Messung W gegen C), `a901e03`
(Register Abschnitt 23, Backlog-Begriff) und der Abgabe-Commit. Ergebnisdokument
`docs/ERGEBNIS_TB-66_benchmark_tagesgenau.md`, Belege `docs/belege/TB-66/`.
**Ändert einen Registertext** (3b (c), freigegeben durch den Auftrag) und
`benchmark.py`; die gesperrte Tabelle `a163c498…` und die TB-61-Tabelle
`e06812d2…` sind byteweise unverändert.

---

## Was der Auftrag wollte und was er bekam

Fables Festlegung vom Nachmittag umsetzen: Registertext 3b (c) neu (tagesgenau
nach dem Loader des Bots), `benchmark.py` ohne Vierjahresfilter, Lauf daneben,
Dreispalten-Vergleich, eine Formulierungsfrage messen statt entscheiden, und
nebenbei den Begriff „Amendment" dort berichtigen, wo er das Register meint.

**Bekommen hat er alles davon — und an drei Stellen etwas anderes als
erwartet:** Die vier Aktien-Bots sind gegenüber TB-61 **nicht** unverändert
(der Auftrag hatte die VH-Zeichengleichheit aus TB-65 auf VT übertragen); die
Begriffsstellen 21.9 und `T56b.3`, die der Auftrag zum Berichtigen nennt,
sprechen genau von der Tabelle, für die er den Begriff zugleich richtig nennt
(aufgelöst über vor/nach dem Tag); und Fassung C („`.fillna(0)`") setzt Fables
Satz nur teilweise um. Alles drei steht als Widerspruch im Ergebnisdokument.

---

## Vier Befunde, und was aus jedem folgt

### 1. Der Registertext, der etwas anderes sagt als der Code — diesmal vor dem Eintrag gefunden

Fable selbst hatte die Unsicherheit benannt („nur eines darf im Register stehen,
und es muss das sein, was der Code tut"). Nachgesehen: *„gleichgewichtet, täglich
rebalanciert"* trifft `bh_tagesrenditen` — *„Tage ohne handelbares Symbol tragen
Rendite 0"* trifft es nicht (`.dropna()`). Gemessen über 78 Falten × 100 Stufen:
für den Drawdown **null** Unterschied, für `handelstage` einer in vier bzw. fünf
Krypto-Falten. Im Register steht an der Stelle ein **sichtbarer Platzhalter**,
keine der beiden Fassungen.

⇒ ⭐⭐ **Ein Platzhalter im Register ist ehrlicher als ein Satz, der den Code
nicht trifft.** Abschnitt 21 hat berichtigt, was 15.6 über den Code behauptete;
hier wäre dieselbe Fehlerklasse mit Fables eigenem Wortlaut entstanden. *Vor dem
Eintrag nachsehen* heisst: messen, ob es einen Zahlenunterschied macht, und
wenn ja, die Entscheidung dem Betreiber lassen — auch wenn der Satz vom
Methodenberater kommt.

### 2. „Nichts ändert sich" galt für die Lesart, die nicht gewählt wurde

TB-65 hatte gemessen: V0 und VH sind bei den Aktien-Bots in 40 von 40 Falten
zeichengleich. Der Auftrag machte daraus eine Gegenprobe für VT. Unter VT
ändern sich 2019, 2025 und 2026 bei allen vier Aktien-Bots — weil `ANET`,
`PLTR`/`DASH`/`ABNB` und `APP` mitten im Jahr handelbar werden und TB-61 sie für
das ganze Jahr zählte, auch während der Peak-Trough-Episode davor. Zwei Bots
bekommen dadurch eine um 0,12 Punkte **strengere** Toleranz als in TB-61.

⇒ ⭐ **Eine Gegenprobe erbt die Lesart, unter der sie gemessen wurde.** Wer sie
in einen Auftrag übernimmt, nennt die Lesart mit — sonst wird ein richtiges
Ergebnis als „Lauf nicht fertig" gelesen. Hier hat *„Widersprich diesem Auftrag,
wo er falsch ist"* die Sitzung davor bewahrt, einen korrekten Lauf zu verwerfen;
der Mechanismus (Eintritt vor oder nach der Drawdown-Episode) ist je Falte
vorgerechnet, nicht behauptet.

### 3. Die Loader-Menge kommt aus einem Werkzeug, nicht aus einer dritten Konstantenkopie

`benchmark.py` liest das Handelbar-Datum je Symbol über
`faltenschranke_messung.loader_lesart` — das TB-56-Werkzeug, das `MIN_HISTORY_*`
aus der Bot-Datei liest und dessen Mengen TB-65 in 78 von 78 Falten gegen den
Trockenlauf bestätigt hat. Vorab gemessen, dass seine Zählung die des Loaders
ist (keine unvollständigen 1h-Kerzen, keine unvollständige erste Zeile in 1d/4h).
Gegen die VT-Spalte von TB-65: 78 / 78 Falten gleich.

⇒ ⭐ **Wo eine Regel schon einmal als Werkzeug steht und gegen den Laufcode
geprüft ist, wird sie importiert, nicht nachgebaut.** Die Alternative — eine
Tabelle 500 / 730 / 1 825 / 17 520 in `benchmark.py` — wäre die vierte Kopie einer
Zahl gewesen, die in diesem Projekt schon dreimal auseinandergelaufen ist
(`FRUEHESTE_FALTE`, `MINDESTTRAINING_JAHRE`, `K4f`).

### 4. Die vier gesperrten Funktionen sind unberührt, obwohl die Menge jetzt täglich wechselt

Die Mengenwahl steckt in den **Eingabereihen** (jede Reihe beginnt an ihrem
Handelbar-Tag), nicht in der Rechenfunktion: `pct_change` liefert am ersten
Punkt NaN, `mean(skipna=True)` mittelt über die Symbole, die an dem Tag eine
Rendite haben. `bh_tagesrenditen`, `drawdown_bei_exposure`, `nachschlagen`,
`erlaubt` und die Medianbildung haben keinen Diff-Hunk im Körper.

⇒ **Eine Änderung der Menge ist eine Änderung der Eingabe.** Wer sie in der
Rechenfunktion unterbringen wollte, hätte Sperrliste 6 anfassen müssen — genau
das, was Fassung C täte und was deshalb zur Betreiberentscheidung gehört.

---

## Zwei Dinge zur Form

**Der Registereintrag ist eine Berichtigung nach der Form von Abschnitt 21:**
Marke am alten Satz, neuer Abschnitt am Ende, `numstat 313 0`. Die
Begriffsberichtigung „Amendment" ist im Register **nicht** als Umschreiben
ausgeführt, sondern als Tabelle „Satz, wie er dasteht / Satz, wie er zu lesen
ist" (23.6) — das Register bleibt append-only, und trotzdem ist jede Stelle
einzeln benannt. Im Backlog, das kein append-only-Dokument ist, ist der Wortlaut
geändert (Regel 9).

**Der Test wurde zweimal ausgeführt:** im Repo (bricht am `KeyError: '2017'`
der gesperrten Tabelle, erwartet) und in einer Wegwerf-Kopie mit der VT-Tabelle
an der Stelle der gesperrten — damit vor dem Vollzug bekannt ist, was der Test
mit der neuen Tabelle tut. Ergebnis im Ergebnisdokument, Nachweis 8.

---

## Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐⭐ | **Ein Registertext wird gegen den Code gemessen, bevor er eingetragen wird — auch wenn er vom Methodenberater kommt.** Trifft ein Satz den Code nicht, steht ein sichtbarer Platzhalter, und die Messung, ob es einen Zahlenunterschied macht, geht mit der Frage zum Betreiber |
| ⭐⭐ | **Eine Gegenprobe nennt die Lesart, unter der sie gilt.** „Bei den Aktien-Bots ändert sich nichts" war eine VH-Aussage; unter VT ist sie falsch, und der Lauf trotzdem richtig |
| ⭐ | **Eine Menge, die täglich wechselt, gehört in die Eingabe, nicht in die gesperrte Rechenfunktion** — dann bleibt die Sperrliste unberührt und die Änderung ist eine Berichtigung des Auswerters, kein Eingriff in die Rechnung |
| ⭐ | **Ein geprüftes Werkzeug wird importiert, nicht nachgebaut** — die vierte Kopie einer Schranke ist die, die beim nächsten Mal auseinanderläuft |
| | „Amendment" heisst nach 10.1 *der Lauf beginnt von vorn*; vor dem Tag gibt es keinen Lauf, also ist es eine Berichtigung (Register) und ein Bug-Fix (Auswerter). Der Begriff bleibt für die Sperrliste **nach** dem Tag |

*Nachgetragen 20.09.2026 aus der Mac-Sitzung TB-66. Quellenvermerk: siehe Kopf.*
