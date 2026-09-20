# Journal-Nachtrag (i) — 20.09.2026, TB-71: das Register ist geschlossen — der Platzhalter fällt, und Festlegung 1 bekommt ihre Regel, bevor die Zahl existiert

**Quelle:** Mac-Sitzung **TB-71 Register schliessen**, 20.09.2026, ab etwa
18:45 Ortszeit, Ausgang `97cbcef` (= `origin/main` beim Start), reine
Registerarbeit (kein Interpreter, keine Kursdaten, nichts ausserhalb `docs/`,
nichts unter `research/`). Commits `d908b73` (Schritt 0, zwei Betreiber-Dateien),
`cc096e1` (Schritt (a), Platzhalter), `9eab386` (Schritt (b), Abschnitt 24),
`295b17f` (Schritt (c), `K4j`), dann dieser Nachtrag und die Abgabe.
Ergebnisdokument `docs/ERGEBNIS_TB-71_register_schliessen.md`. **Einzuarbeiten
als nächster Block nach dem höchsten vorhandenen** (am 20.09.2026 gemessen:
`BT`; `(20g)` und `(20h)` liegen davor und werden `BU` und `BV`, dieser
Nachtrag also voraussichtlich `BW` — die Nummer vergibt die einarbeitende
Sitzung).

⭐ **Quellenzeile für den Block, wörtlich zu übernehmen:**

```
*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20i.md`*
```

---

## Was der Auftrag wollte und was er bekam

Drei Einträge ins Register, alle am 20.09.2026 in vier Fable-Runden und zwei
Betreiberentscheidungen festgelegt, keiner erfunden: **(a)** der sichtbare
Platzhalter in 23.3 (Satz zu Tagen ohne handelbares Symbol, W oder C) fällt —
an seine Stelle tritt der Satz zur Zeitachse, verankert an 3b (b); **(b)** ein
neuer Abschnitt 24, der den Widerspruch zwischen Festlegung 1 (*„Kapital-Drawdown
aus `equity_simulation.py`"*) und Registertext 1a (tägliche
Mark-to-Market-Renditen) auflöst — zugunsten der täglichen Reihe — **und die
Entscheidungsregel einträgt, bevor die Wirkung gemessen ist**; **(c)** die drei
Code-Stellen, die dem folgen müssen, als eine Backlog-Zeile.

**Bekommen hat er alle drei:** 23.3 ohne Platzhalter (`grep -c` = 0), mit
Tatsachennotiz zum ersten Kurstag und `handelstage` als W-Spalte, die
W/C-Tabelle mit Marke ERSETZT; Abschnitt 24 mit Befund, Fundstellen (sieben,
gelesen, nicht ausgeführt), Registertext-4-Präzisierung, Entscheidungsregel,
Fables Begründung und Warnung, Vorgeschichte aus `research/drawdown_reihenfolge/`;
`K4j` in Abschnitt 4. Register `numstat` über die Sitzung **263/3** — die drei
entfernten Zeilen sind die drei physischen Zeilen des Platzhalters. Beide
Benchmark-Tabellen byteweise unverändert (`a163c498…`, `4549395f…`).

---

## Drei Befunde

### 1. ⭐ Eine Regel, die eine Zahl für belanglos erklärt, muss vor der Zahl stehen — sonst ist die Zahl ein Argument

Fable hat die Reihenfolge zur Bedingung gemacht, der Betreiber hat ihr um 18:15
zugestimmt, und dieser Auftrag *ist* die Regel: Register 24.3 sagt, dass die
Grösse der Abweichung zwischen ereignisindiziertem und Mark-to-Market-Drawdown
gemessen und berichtet wird **und für die Entscheidung ohne Belang ist**. Die
Messung (TB-73) läuft danach. *„Eine Zahl, die nichts entscheiden darf, sollte
nicht auf dem Tisch liegen, während entschieden wird."* — Das ist F17 auf die
Zeitachse angewendet: nicht die Richtung der Wirkung ist das Problem (sie ist
bekannt: gegen alle neun Bots), sondern dass eine Zahl in eine Frage einginge,
die keine Zahlenfrage ist.

⭐ **Regel:** *Wird eine Zahl vor der Entscheidung gemessen, ist sie ein
Argument in beide Richtungen — „ändert wenig, also nicht die Mühe" und „ändert
viel, also zu riskant". Wer die Zahl nicht entscheiden lassen will, schreibt
das auf, bevor sie existiert.*

### 2. Die Vorgeschichte gehört in die Präzisierung — sonst liest sie sich als Widerruf

Festlegung 1 kam aus `research/drawdown_reihenfolge/` (12.09.2026): drei
Drawdown-Begriffe verglichen (Blockreihenfolge, chronologisch, Kapitalkurve),
Kapitalkurve als *„der erlebbare Verlauf"* gewählt. **Mark-to-Market war
unter den dreien nicht dabei** — und ist die Definition, die das Kriterium
„erlebbar" am besten erfüllt (Fable: *„das Konto zeigt offene Positionen zum
Marktpreis, nicht zum Einstandskurs"*). Abschnitt 24.4 sagt deshalb beides:
Das Kriterium war richtig, der Vergleich unvollständig. Festlegung 1 wird
präzisiert, nicht gestrichen; Z. 47 bleibt stehen und trägt eine Marke.

### 3. Der Platzhalter war drei Zeilen, nicht eine — und sein Satz stammt aus der dritten Fassung

Der Auftrag verlangte, *„die eine ersetzte Zeile"* nachzuweisen; im Register
lief der Platzhalter über drei physische Zeilen eines umbrochenen Absatzes.
`numstat` zeigt deshalb 45/3 für Schritt (a), und alle drei entfernten Zeilen
tragen Platzhaltertext — sonst ist nichts verschwunden. Der eingetragene Satz
ist nicht Fables erste Fassung („tragen Rendite 0", von ihm zurückgezogen:
Mechanismus statt Prinzip) und nicht seine zweite (Kalender des Kapitalpfades —
den es nicht gibt, der Pfad ist ereignisindiziert, `shared/zuteilung.py:720–735`),
sondern die dritte aus `FABLE_ANFRAGE_2026-09-20c`, von ihm übernommen. 23.3
hält die Herkunft aller drei fest.

---

## Was der Auftrag anders sah — und wo die Messung galt

| Auftrag | gemessen |
|---|---|
| Nachweis 3: `ergebnisse/benchmark_drawdowns.json` | die Dateien liegen unter `research/vorregistrierung/ergebnisse/`; dort gehasht, beide Hashes wie verlangt |
| Nachweis 2: *„die eine ersetzte Zeile"* | drei physische Zeilen (Befund 3); je alter und neuer Wortlaut im Ergebnisdokument |
| Nachweis 4: *„Kein Python ausgeführt ausser Nachweis 5"* | Nachweis 5 ist ein `grep`, kein Python — **gar kein Python** ausgeführt |
| Vorgeschichte *„am 12./13.09."* | alle drei Commits von `research/drawdown_reihenfolge/` tragen das Datum **12.09.2026** |
| Schritt (a) nennt nur 23.3 | 23.7 (Zeilen „Formulierungsfrage nicht entschieden", „Platzhalter bleibt") und Abschnitt 1 (Z. 47) wären ohne Marke irreführend geblieben — je eine **angehängte** Nachtragszeile bzw. Marke, nichts entfernt |
| Nachweis 6: *„nur eine Zeile"* im Backlog | eingehalten (1/0); dadurch bleibt der Halbsatz *„vor dem Vollzug steht die Entscheidung W/C aus Register 23.3"* in Abschnitt 2 (Z. 308) **überholt stehen** — in `K4j` benannt, nicht geändert |

---

## Offen

| | wer |
|---|---|
| **TB-72** — `t3_supertrend` beginnt 2019, `faltenplan.py` leitet die erste Falte aus dem Trockenlauf ab (rechnet) | nächster Auftrag |
| **TB-73** — die MtM-Wirkung messen, je Bot, Forschungsskript; Ergebnis in die Notiz zu 24.4, nie in eine Entscheidung | nach TB-72 |
| Vollzug der Sperrlisten-Änderung (21.9) — braucht nur noch die Betreiberfreigabe; dabei `registerbericht.py:178` nachziehen (23.5) | Betreiber |
| `BACKLOG.md` Abschnitt 2, Z. 308: Halbsatz zu W/C überholt (Regel 9: Wortlaut ändern) | nächste Backlog-Pflege |
| `K4j` — die drei Code-Stellen, sobald der Laufcode geschrieben wird (TB-30b) | TB-30b |
| Dieser Nachtrag ins Journal (Block nach `BV`) | nächste Einarbeitung / TB-64-Wächter |
| Projektablage nachziehen (`K4e`): Register und Backlog sind geändert | steuernder Chat / Betreiber |
