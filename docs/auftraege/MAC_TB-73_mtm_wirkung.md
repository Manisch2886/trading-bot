# TB-73 Die Wirkung des Mark-to-Market-Drawdowns messen — nachdem die Regel steht

**an: Claude Code am Mac (lokale Sitzung)**

**Sitzungstitel für Claude Code: `TB-73 MtM-Wirkung`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⚠️ **Diese Aufgabe RECHNET.** ⛔ **Sie entscheidet nichts.**

---

## 0. ⭐⭐ Lies das zuerst — es ist der Grund, warum diese Aufgabe existiert

**Register 24.3 trägt seit TB-71 diesen Satz:**

> Der Drawdown der Nebenbedingung wird auf der täglichen
> Mark-to-Market-Reihe gerechnet (1a); **die Grösse der Abweichung zur
> ereignisindizierten Kurve wird gemessen und berichtet und ist für die
> Entscheidung ohne Belang.**

⭐ **Er stand dort, bevor diese Messung begonnen hat.** Das war eine
Betreiberentscheidung vom 20.09.2026, 18:15, auf Fables Rat:

> Die Zahl beziffert, sie entscheidet nicht. Aber das ist nur dann wahr, wenn es
> **vor** der Messung aufgeschrieben ist — sonst ist die Zahl, sobald sie da ist,
> ein Argument, und zwar in beide Richtungen … **Eine Zahl, die nichts
> entscheiden darf, sollte nicht auf dem Tisch liegen, während entschieden
> wird.**

⛔⛔ **Daraus folgt für dich, wörtlich:** **Du legst am Ende keine Empfehlung
vor, keine Abwägung, kein *„angesichts dieser Zahl sollte man …"*.** Du misst,
berichtest und trägst das Ergebnis in die Notiz. **Die Entscheidung ist
gefallen, bevor du angefangen hast.**

⚠️ **Und Fables Warnung, die in den Bericht gehört:**

> Eine kleine Abweichung im Mittel sagt nichts über die Falten, in denen die
> Nebenbedingung binden soll — **2020 und 2022 sind die Falten mit den grössten
> unrealisierten Verlusten innerhalb offener Positionen.**

⇒ ⭐ **Berichte je Falte, nicht nur im Mittel.** Ein Durchschnitt über alle
Falten wäre hier die Zahl, die nichts sagt.

---

## 1. Was gemessen wird

**Der Bot-Drawdown je Falte, auf zwei Arten:**

| | Fassung | wie sie heute entsteht |
|---|---|---|
| **E** | **ereignisindiziert** — der heutige Weg | `shared/zuteilung.py` baut `equity_curve` je Ein- und Ausstieg; `shared/messkette.py::calculate_max_drawdown` rechnet über `capital_after` |
| **M** | **Mark-to-Market, täglich** — was Registertext 1a verlangt | **Gibt es nicht.** Zu bauen: der Kapitalpfad wird an **jedem** Handelstag bewertet, offene Positionen zum Schlusskurs des Tages, flache Tage mit Rendite 0 |

⭐ **Die Grundlage liegt vor:** die Trade-Listen aus `research/tb24_haltedauern/`
und die Kursdateien in `data/`. ⚠️ **Prüfe das zuerst** — nenne, was du
vorfindest, und **wenn die Listen nicht reichen, sag es und miss nicht
drumherum** (`A2`).

---

## 2. ⛔ Wo das gebaut wird — und wo nicht

| | |
|---|---|
| ⭐ | **Ein eigenes Forschungsskript**, `research/mtm_drawdown/`, nach dem Muster von `research/drawdown_reihenfolge/` |
| ⛔ | **Nicht in `research/vorregistrierung/`.** Kein Laufcode, keine der vier gesperrten Rechenfunktionen, keine Ergebnisdatei dort |
| ⛔ | **`shared/zuteilung.py` und `shared/messkette.py` werden gelesen, nicht geändert** — sie tragen den Live-Betrieb aller neun Bots |
| ⛔ | **Keine Konstantenkopie.** Kosten, Slippage, Zuteilungskaskade und Seed werden **importiert** (`T56b.6`) |
| ⚠️ | **Die Zuteilungskaskade entscheidet, welche Trades überhaupt laufen.** ⭐ **Bau M auf denselben ausgeführten Positionen, die E benutzt** — sonst misst du zwei verschiedene Bots, nicht zwei Bewertungen desselben |

---

## 3. Die Schritte

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt**, getrennt nach Urheber, wie TB-68/71/72.

### Schritt 1 — die Grundlage prüfen, bevor gebaut wird

**Für jeden der neun Bots:** Gibt es eine Trade-Liste mit Einstiegs- und
Ausstiegszeitpunkt je Position? Decken die Kursdateien die Haltedauern ab?

⛔ **Nichts schätzen.** Fehlt etwas, steht das so da, und der Bot fehlt in der
Tabelle statt mit einer erfundenen Zahl darin.

**Sichern: commit und push.**

### Schritt 2 — den MtM-Pfad bauen

**Je Bot und Falte:** aus den ausgeführten Positionen und den Tagesschlusskursen
eine **tägliche** Kapitalreihe. Offene Positionen zum Schlusskurs bewertet,
Kosten und Slippage wie im Original (importiert), Tage ohne Position tragen 0.

⭐⭐ **Zwei Proben, die beissen können** (`B1`), bevor du irgendeine Zahl
berichtest:

| | Probe | was sie zeigen muss |
|---|---|---|
| **1** | Ein Bot, dessen Positionen **alle innerhalb eines Tages** geschlossen werden | E und M müssen **gleich** sein — gibt es keinen unrealisierten Verlust, gibt es keinen Unterschied |
| **2** | Eine **einzelne Position von Hand**, deren Verlauf du ausrechnen kannst | M muss den bekannten Zwischenverlust zeigen, E nicht |

⛔ **Schlägt eine der beiden fehl, ist der Pfad falsch** — dann melde das und
rechne nichts weiter.

**Sichern: commit und push.**

### Schritt 3 — die Messung

**Je Bot, je Falte, bei 25 / 50 / 100 % Exposure:** E gegen M.

⭐ **Berichtet werden:**

| | |
|---|---|
| **je Falte** | E, M, Differenz in Prozentpunkten und als Faktor |
| ⭐ | **2020 und 2022 einzeln hervorgehoben** — Fables Warnung |
| ⭐ | **Der Median über die Selektionsfalten** je Bot, das ist die Grösse, die zur `DD_Toleranz` führt |
| ⚠️ | **Die Richtung, gegengeprüft:** M darf **nie flacher** sein als E. **Findest du einen Fall, in dem doch, ist der Pfad falsch** — melde ihn, statt ihn zu glätten |

⚠️ **Die Falten kommen aus `faltenplan_tb72.json`** (TB-72), nicht aus
`faltenplan.json` — die Datei auf der Platte ist TB-30a-Stand (`K4k`).

**Sichern: commit und push.**

### Schritt 4 — die Notiz ins Register

**Ein Nachtrag zu Abschnitt 24**, als **24.6**: die gemessene Wirkung, je Bot
und mit den beiden hervorgehobenen Falten.

⛔ **Append-only**, `numstat` Spalte zwei = 0.
⛔ **Kein Satz, der die Entscheidung erneut aufwirft.** Die Notiz berichtet;
24.3 hat entschieden.

**Sichern: commit und push.**

### Schritt 5 — eine Backlog-Zeile und die Abgabe

**Eine** Zeile in Abschnitt 4, K-Nummer selbst gemessen (Muster
`^\| \*\*(K\d[a-z])\*\*` **ohne schliessenden Balken**, **kein `sort -u`**, über
`BACKLOG.md` **und** `BACKLOG_ARCHIV.md`).

`docs/ERGEBNIS_TB-73_mtm_wirkung.md` und ein Journal-Nachtrag
⭐ **mit der Quellenzeile aus TB-67**.

**Sichern: commit und push.**

---

## 4. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐ Schritt 1: je Bot, welche Grundlage vorliegt — **und welche fehlt** |
| **3** | ⭐⭐ **Die beiden Proben aus Schritt 2**, je mit Ergebnis. ⚠️ **Ohne sie gilt keine Zahl aus Schritt 3** |
| **4** | Die Messung je Bot und Falte, 2020 und 2022 hervorgehoben |
| **5** | ⭐ **Die Richtungsprobe**: kein Fall, in dem M flacher ist als E — oder die Fälle einzeln benannt |
| **6** | SHA-256 von `benchmark_drawdowns.json` (`a163c498…`), `_vt.json` (`4549395f…`), `_tb72.json` und `faltenplan.json` (`0e54ac5c…`) — **alle unverändert** |
| **7** | Register: `numstat` Spalte zwei = **0** |
| **8** | Laufzeit je Messung genannt *(Regel aus TB-72, Journal-Nachtrag 20k)* |
| **9** | `git diff --numstat` je Datei; **nichts in `research/vorregistrierung/`, nichts in `shared/`, nichts in `strategies/`** |

---

## 5. Die harten Auflagen

| | |
|---|---|
| ⛔⛔ | **Keine Empfehlung, keine Abwägung, kein Vorschlag am Ende.** Register 24.3: *„für die Entscheidung ohne Belang"* |
| ⛔ | **Nichts in `research/vorregistrierung/`, `shared/`, `strategies/`** |
| ⛔ | **Keine Konstantenkopie** — Kosten, Slippage, Seed, Kaskade werden importiert |
| ⛔ | **Kein Mittelwert ohne die Faltenwerte daneben** |
| ⭐ | **Sichern nach jedem fertigen Teil** — sechs Commits oben benannt |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** ⭐ *Die letzten acht Aufträge lagen je an mehreren Stellen daneben, und jedes Mal hatte die ausführende Sitzung recht — zuletzt TB-72, dessen Schritt-1-Messung meinen eigenen Umbauvorschlag und Fables Prämisse zugleich widerlegt hat* |
| ⭐ | **Entscheidungen an den Betreiber gehen als anklickbare Frage mit Empfehlung** (`ARBEITSWEISE.md` 6d) — *für diese Aufgabe ist keine vorgesehen* |

---

## 6. Was diese Aufgabe NICHT tut

| | |
|---|---|
| ⛔ | **Den Laufcode schreiben** — die drei Code-Stellen aus `K4j` folgen später |
| ⛔ | **Die Sperrlisten-Änderung vollziehen** |
| ⛔ | **Die Uhr im Selektionspfad anfassen** — das ist `TB-74`, und es wartet auf Fable |
| ⛔ | **Den Tag setzen** |
| ⛔ | **G6 und H3 reparieren** |

---

## In einfacher Sprache

**Worum es geht:** Die Verlustgrenze eines Bots wird heute nur an Kauf- und
Verkaufszeitpunkten gemessen. Was eine Position zwischendurch an Buchverlust
hatte, zählt nicht. Künftig soll täglich gemessen werden — das ist bereits
entschieden und steht im Regelwerk.

**Was diese Aufgabe macht:** Sie rechnet aus, wie gross der Unterschied
tatsächlich ist. Je Bot, je Jahr.

**Was sie ausdrücklich nicht macht:** Sie zieht daraus keinen Schluss. Die
Entscheidung wurde absichtlich getroffen, **bevor** diese Zahl existierte —
damit die Zahl sie nicht beeinflussen kann. Sie wird berichtet und abgelegt,
mehr nicht.

**Eine Warnung gehört dazu:** Wenn der Durchschnitt klein ausfällt, ist das
**kein** Grund zur Entwarnung. Entscheidend sind die schweren Jahre 2020 und
2022 — dort sind die Buchverluste innerhalb offener Positionen am grössten, und
genau dort soll die Grenze greifen.
