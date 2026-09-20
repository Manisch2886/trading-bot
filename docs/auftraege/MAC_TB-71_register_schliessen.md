# TB-71 Das Register schliessen — der Platzhalter fällt, und Festlegung 1 bekommt ihre Regel

**an: Claude Code am Mac (lokale Sitzung)**

**Sitzungstitel für Claude Code: `TB-71 Register schliessen`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⭐ **Rechnet nicht.** ⛔ **Kein Python wird ausgeführt, keine Tabelle neu
gerechnet, keine Datei in `ergebnisse/` angefasst.** Reine Registerarbeit.

⚠️ **Alle Inhalte sind entschieden.** Dieser Auftrag trägt ein, was am
20.09.2026 in vier Runden mit Fable und in zwei Betreiberentscheidungen
festgelegt wurde. **Du erfindest keinen Wortlaut** — die Sätze stehen unten
wörtlich.

---

## 0. Warum es diese Aufgabe gibt

**TB-66 hat Registerabschnitt 23 angelegt und an einer Stelle bewusst einen
sichtbaren Platzhalter stehen lassen.** Er steht immer noch da. Danach hat
Fable in zwei weiteren Runden geantwortet, und dabei ist ein zweiter,
grösserer Punkt entstanden.

| | Stand | Fundstelle |
|---|---|---|
| **(a)** | Register **23.3** trägt `⚠️ **[PLATZHALTER — der Satz zu Tagen, an denen kein Symbol handelbar ist; Fassung W oder C, siehe unten; Betreiberentscheidung offen]**` | `docs/VORREGISTRIERUNG_neuselektion.md`, Abschnitt 23.3 |
| **(b)** | **Festlegung 1** der zwölf vom 14.09.2026 (*„Führendes Mass: Kapital-Drawdown aus `equity_simulation.py`"*, Register Z. 47) steht im Widerspruch zu **Registertext 1a** (tägliche Netto-Mark-to-Market-Renditen). Der Widerspruch ist benannt, aufgelöst ist er nicht | Register Z. 47 gegen Z. 1102–1104 |
| **(c)** | Die drei Code-Stellen, die der Lösung von (b) folgen müssen, sind nirgends geführt | — |

⭐ **Die vier Fable-Antworten liegen wörtlich im Repo:**
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-20{,b,c,d}*.md`. ⚠️ **Lies sie,
bevor du schreibst** — dieser Auftrag fasst zusammen, sie sind die Quelle.

---

## 1. ⛔ Was diese Aufgabe NICHT tut

| | |
|---|---|
| ⛔ | **`benchmark.py` anfassen.** Der Code ist seit TB-66 auf VT und bleibt, wie er ist — auch `bh_tagesrenditen` mit seinem `.dropna()` |
| ⛔ | **`auswertung.py` anfassen.** ⚠️ **Die Datei ist eingefroren** (Register 15.8 Nr. 3: *„die Datei ist eingefroren und wurde nicht angefasst. Ihre Umstellung ist TB-30b"*). Auch ihr Docstring nicht |
| ⛔ | **`beispieldaten.py` oder `registerdaten.py` anfassen** |
| ⛔ | **Irgendetwas rechnen.** Keine Tabelle, kein Lauf, kein Testdurchlauf ausser dem in Nachweis 5 |
| ⛔ | **`t3_supertrend` auf 2019 umstellen** — das ist **TB-72**, es rechnet |
| ⛔ | **Die MtM-Wirkung messen** — das ist **TB-73**, und es darf erst nach diesem Auftrag laufen |

⭐ **Der Grund für die letzte Zeile ist die Sache selbst:** Fable hat die
Reihenfolge zur Bedingung gemacht, und der Betreiber hat ihr zugestimmt. *Die
Regel muss geschrieben sein, bevor die Zahl existiert.* **Dieser Auftrag ist
die Regel.**

---

## 2. Schritt (a) — der Platzhalter in 23.3 fällt

**Ersetze den Platzhalter durch genau diesen Satz:**

> Der Benchmark einer Falte ist an genau den Tagen definiert, an denen
> mindestens ein Symbol des Bots nach 3b (b) handelbar ist. Ein Tag, an dem kein
> Symbol handelbar ist, gehört nicht zum Benchmark — er wird nicht mit Rendite 0
> geführt, sondern gar nicht.

⭐ **Herkunft, die dazugehört:** Der Satz ist **nicht** Fables erste Fassung.
Seine lautete *„Tage, an denen kein Symbol handelbar ist, tragen Rendite 0"*
und wurde von ihm selbst zurückgezogen, weil sie einen Mechanismus vorschrieb
statt ein Prinzip. Seine zweite Fassung band den Benchmark an den Kalender des
Bot-Kapitalpfades — **den es nicht gibt**, der Pfad ist ereignisindiziert
(`shared/zuteilung.py:720–735`). ⭐ **Die dritte Fassung, die jetzt eingetragen
wird, stammt aus diesem Chat und wurde von Fable übernommen:** *„Meine Fassung
hat einen Kalender vorausgesetzt, den der Kapitalpfad nicht hat; eure setzt
nichts voraus."*

**Darunter, als Tatsachennotiz:**

> Die Umsetzung lässt den ersten Kurstag je Falte aus, weil `pct_change` dort
> keine Rendite liefert. Abweichung gegenüber dem Satz: höchstens ein Tag je
> Falte. Wirkung auf jede registrierte Zahl: null — 0 abweichende Stufen in
> Drawdown und `DD_Toleranz` über 78 × 100 (TB-66, Nachweis 4). Wird
> `bh_tagesrenditen` je aus anderem Grund angefasst, ist `fillna(0)` auf diesem
> Tag eine Berichtigung des Codes an den Satz.

**Und:** `handelstage` bleibt unverändert die **W-Spalte** — die Länge des
gemeinsamen Kalenders.

⚠️ **Die Tabelle mit den Fassungen W und C bleibt stehen**, als ERSETZT
gekennzeichnet. ⭐ **Sie hält fest, wogegen entschieden wurde** — und sie
enthält die Messung, die C_voll ausgeschlossen hat (`t3_supertrend` 2018 hätte
365 Handelstage statt 0).

**Sichern: commit und push.**

---

## 3. Schritt (b) — Festlegung 1 bekommt ihre Regel, VOR jeder Messung

⚠️⚠️ **Das ist der Kern dieses Auftrags.** Ein neuer Registerabschnitt —
**24** —, der drei Dinge trägt:

### 24.1 Der Befund

**Wörtlich aus Fables dritter Antwort:**

> Der Drawdown der Nebenbedingung wird auf einem Objekt gerechnet, das das
> Register ausschliesst. `calculate_max_drawdown` läuft über `capital_after` je
> Ereignis — eine Kurve, die sich nur an Ein- und Ausstiegen bewegt. … **Sie
> sieht keinen unrealisierten Verlust.** Eine Position, die zwischen Einstieg und
> Ausstieg 20 % unter Wasser war und mit −3 % geschlossen wurde, trägt −3 % zum
> Drawdown bei. Der Benchmark daneben ist tagesgenau bewertet. … „Bot und
> Benchmark leben in derselben Menge" gilt dann auf der Symbol- und Zeitachse,
> aber nicht auf der Bewertungsachse.

**Mit den Fundstellen, gemessen am 20.09.2026:**

| | |
|---|---|
| `shared/zuteilung.py:720–735` | `equity_curve.append({"time": …, "capital_after": …})` je Ereignis. Kein Tageskalender |
| `shared/messkette.py:139–153` | `calculate_max_drawdown` rechnet über `equity_df["capital_after"]` |
| `research/vorregistrierung/beispieldaten.py:24–26` | *„der Kapital-Drawdown einer Falte steht in `zellen.csv`, weil er im echten Lauf aus `equity_simulation.py` kommt, und **nicht aus der Tagesreihe** nachgerechnet wird. Das ist auch im echten Lauf so."* |
| `research/vorregistrierung/auswertung.py:246–247` | die Nebenbedingung vergleicht genau dieses `kapital_drawdown_pct` gegen die Benchmark-Grenze |

### 24.2 Der Registertext — Präzisierung zu Registertext 4

**Fables Wortlaut, unverändert:**

> **Registertext 4, Präzisierung.** Der Kapital-Drawdown einer Falte für die
> Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe des Kapitalpfads
> gerechnet (1a), auf denselben Tagen wie der Benchmark (3b (c)). Der
> ereignisindizierte Drawdown aus `equity_simulation.py` wird berichtet, nicht
> bewertet.

### 24.3 ⭐⭐ Die Entscheidungsregel — der eigentliche Zweck dieses Abschnitts

**Wörtlich, und sie steht da, BEVOR jemand einen MtM-Pfad rechnet:**

> Der Drawdown der Nebenbedingung wird auf der täglichen
> Mark-to-Market-Reihe gerechnet (1a); die Grösse der Abweichung zur
> ereignisindizierten Kurve wird gemessen und berichtet und ist für die
> Entscheidung ohne Belang.

**Dazu die Begründung, warum die Reihenfolge zählt** — Fable wörtlich:

> Eure Lesart ist richtig: Der Grund kommt aus 1a und L1 und steht fest, bevor
> die Zahl existiert. Die Zahl beziffert, sie entscheidet nicht. Aber das ist nur
> dann wahr, wenn es **vor** der Messung aufgeschrieben ist — sonst ist die Zahl,
> sobald sie da ist, ein Argument, und zwar in beide Richtungen: „ändert wenig,
> also nicht die Mühe" oder „ändert viel, also zu riskant vor dem Tag". … **Eine
> Zahl, die nichts entscheiden darf, sollte nicht auf dem Tisch liegen, während
> entschieden wird.**

⚠️ **Und die Warnung, die mit in den Abschnitt gehört:**

> Eine kleine Abweichung im Mittel sagt nichts über die Falten, in denen die
> Nebenbedingung binden soll — 2020 und 2022 sind die Falten mit den grössten
> unrealisierten Verlusten innerhalb offener Positionen.

### 24.4 Was mit Festlegung 1 geschieht

⭐ **Sie wird nicht gestrichen, sie wird präzisiert.** Register Z. 47 bleibt
stehen; 24.4 stellt daneben:

| | |
|---|---|
| **Führendes Mass bleibt der Kapital-Drawdown** | unverändert |
| ⭐ **Präzisiert ist, worauf er gerechnet wird** | auf der täglichen MtM-Reihe (1a), nicht auf der Ereigniskurve |
| **Der ereignisweise Drawdown** | bleibt **Berichtswert** |
| **Betreiberentscheidung** | 20.09.2026, 18:15, per anklickbarer Frage: erst die Regel, dann die Messung |

⭐ **Die Vorgeschichte gehört ausdrücklich hinein**, sonst liest es sich wie ein
Widerruf: `research/drawdown_reihenfolge/` hat am 12./13.09. **drei**
Drawdown-Begriffe verglichen (Blockreihenfolge, chronologisch, Kapitalkurve) und
die Kapitalkurve als *„den erlebbaren Verlauf"* gewählt — daher Festlegung 1.
**Mark-to-Market war unter den dreien nicht dabei.** Fables Satz dazu, wörtlich:

> Das Kriterium war richtig; nur war die vierte Definition nicht im Vergleich —
> und sie ist die, die das Kriterium am besten erfüllt. **Erlebbar ist, was das
> Konto an jedem Tag zeigt, und das Konto zeigt offene Positionen zum
> Marktpreis, nicht zum Einstandskurs.** Die Ereigniskurve ist der *realisierte*
> Verlauf; der erlebbare ist der bewertete.

**Sichern: commit und push.**

---

## 4. Schritt (c) — die Code-Folgen werden geführt, nicht ausgeführt

⚠️ **Drei Stellen müssen 24.2 folgen, sobald der Laufcode geschrieben wird.
Keine davon wird in diesem Auftrag angefasst.** Trag sie als **eine**
Backlog-Zeile in Abschnitt 4 ein, mit gemessener K-Nummer:

| | Stelle | was folgen muss |
|---|---|---|
| **1** | `auswertung.py`, Datenvertrag Z. 40–58 | `kapital_drawdown_pct` kommt aus derselben Tagesreihe wie der Sharpe. ⚠️ **Datei eingefroren — gehört zu TB-30b** |
| **2** | `beispieldaten.py` Z. 24–26 und Z. 125 | rechnet den Drawdown heute ausdrücklich **nicht** aus der Tagesreihe und sagt im Kopf, das sei auch im echten Lauf so |
| **3** | `registerdaten.py:70`, `FESTLEGUNGEN[1]` | Text präzisieren, sobald 1 und 2 stehen |

⭐ **Der Laufcode selbst existiert nicht** — gemessen am 20.09.: kein Code im
Repo schreibt `zellen.csv` oder `tagesreihen/<zelle_id>.csv` ausser
`beispieldaten.py` (erfundene Werte). **Deshalb ist es eine Spezifikation, kein
Umbau, und deshalb kostet „Lauf wiederholen" nichts.**

⚠️ **K-Nummer selbst messen:** Muster `^\| \*\*(K\d[a-z])\*\*` **ohne
schliessenden Balken**, **kein `sort -u`**, über `BACKLOG.md` **und**
`BACKLOG_ARCHIV.md`. ⛔ **Nur eine Zeile.**

**Sichern: commit und push.**

---

## 5. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐ **`git diff --numstat` des Registers: Spalte zwei = 0.** Der Platzhalter ist die **einzige** Ausnahme — weise die eine ersetzte Zeile einzeln nach, mit altem und neuem Wortlaut |
| **3** | ⭐ **SHA-256 von `ergebnisse/benchmark_drawdowns.json` vorher und nachher** — muss `a163c498…36d1ee` bleiben. Ebenso `benchmark_drawdowns_vt.json` = `4549395f…8745d` |
| **4** | Kein Python ausgeführt ausser Nachweis 5; `git diff --numstat` zeigt **nichts** unter `research/` |
| **5** | ⭐ **Eine Suche, kein Lauf:** belege mit `grep -c`, dass der Platzhaltertext `[PLATZHALTER` im Register **null** Treffer mehr hat |
| **6** | Backlog: `numstat 1 0`, K-Nummer nirgends doppelt |
| **7** | Nichts ausserhalb `docs/` geändert |

---

## 6. Die harten Auflagen

| | |
|---|---|
| ⛔ | **Kein Wortlaut wird erfunden.** Die Sätze in Abschnitt 2 und 3 werden **zeichengleich** übernommen |
| ⛔ | **Nichts wird im Register entfernt** — ausser dem Platzhalter, der dafür gemacht wurde |
| ⛔ | **`auswertung.py` bleibt eingefroren**, auch der Docstring |
| ⭐ | **Sichern nach jedem fertigen Teil** — drei Commits oben benannt |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** ⭐ *Die letzten sechs Aufträge lagen je an mehreren Stellen daneben, und jedes Mal hatte die ausführende Sitzung recht — zuletzt TB-68, das nachgewiesen hat, dass die beiden Eröffnungstexte nicht auseinandergelaufen, sondern „als Widerspruch geboren" sind* |
| ⭐ | **Entscheidungen an den Betreiber gehen als anklickbare Frage mit Empfehlung** (`ARBEITSWEISE.md` 6d, Form-Unterabschnitt vom 20.09.) — nicht als Absatz im Ergebnisdokument |

---

## 7. Die Abgabe

`docs/ERGEBNIS_TB-71_register_schliessen.md` und ein Journal-Nachtrag
⭐ **mit der Quellenzeile aus TB-67**.

**Sichern: commit und push.**

---

## In einfacher Sprache

**Was schiefsteht:** Im Regelwerk steht an einer Stelle ausdrücklich ein
Platzhalter — eine Lücke, die absichtlich offen gelassen wurde, bis
entschieden ist. Sie ist jetzt entschieden. Und an einer zweiten Stelle
widersprechen sich zwei Regeln: Die eine sagt, der Verlust eines Bots wird
täglich zum Marktpreis gemessen, die andere nennt ein Programm, das nur bei
Käufen und Verkäufen misst.

**Was diese Aufgabe macht:** Sie trägt den entschiedenen Satz ein und löst den
Widerspruch auf — zugunsten der täglichen Messung, weil nur die zeigt, was das
Konto an einem Tag wirklich wert ist.

**Und sie schreibt eine Regel, bevor gemessen wird:** dass die Grösse des
Unterschieds für diese Entscheidung keine Rolle spielt. Das klingt umständlich,
ist aber der Kern des ganzen Verfahrens — eine Zahl, die nichts entscheiden
darf, soll nicht auf dem Tisch liegen, während entschieden wird. **Gemessen
wird danach, in einer eigenen Aufgabe.**
