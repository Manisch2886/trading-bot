# Reihenfolge-Empfindlichkeit bei gleichzeitigen Signalen — alle 9 Bots

**Status: reine Untersuchung. KEINE Änderung an bestehenden Backtest- oder
Live-Dateien.** Alle Skripte liegen ausschliesslich unter
`research/order_sensitivity/`. Verifiziert per `git status`. Es wird auch
**keine „korrekte" Tie-Breaking-Regel eingeführt** — das wäre eine eigene
Aufgabe.

---

## 0. Entscheidungsgrundlage

### Datenbasis

Alle 9 Bots, jeweils mit dem **unveränderten Original-Trade-Satz** aus ihrem
eigenen `equity_simulation.py`. 500 Permutationen je Bot, fester Seed.

| | |
|---|---|
| Bots | 9 von 9 |
| Trades gesamt | 26.649 über alle Bots |
| Permutationen | 500 je Bot und je verglichener Konfiguration |
| Konfigurationsquelle | die Modul-Konstanten des jeweiligen `equity_simulation.py` |
| geprüfte Entscheidungen | 6 dokumentierte, bereits umgesetzte |

### Pflicht-Gegencheck: rechnet diese Untersuchung dasselbe wie die Bots?

Die Permutationen laufen aus Laufzeitgründen über eine NumPy-Umsetzung der in
allen 9 Bots gleichlautenden `simulate_portfolio()`. Für **jeden Bot** werden
25 Permutationen zusätzlich mit der **bot-eigenen, unveränderten Funktion**
nachgerechnet und verglichen (Rendite, Max Drawdown, Anzahl ausgeführter
Trades).

**Ergebnis: 0 Abweichungen über alle 9 Bots und alle 225 nachgerechneten
Permutationen.** Zusätzlich prüft `test_order_core.py` die Umsetzung gegen
eine wortgetreue Kopie der Bot-Funktion über fünf Kapitalkonfigurationen.

Zwei weitere Bestätigungen, dass die richtigen Zahlen reproduziert werden:

- `elliott_wave_stocks`: die Punktschätzer **+1500,53 % / −1,90 %** (mit
  Take-Profit) und **+3084,09 % / −9,79 %** (ohne) stimmen exakt mit den in
  `results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md` dokumentierten Werten
  überein — also mit genau den Zahlen, auf denen die Entscheidung beruht.
- `t3_supertrend`: **129,64 % / −22,20 %** entspricht exakt dem im
  Übergabeprotokoll (Abschnitt 3.2) berichteten Wert.

### Belastbarkeit

Der Effekt ist **kein Schätzproblem, sondern eine deterministische
Willkür**: bei gegebener Reihenfolge ist das Ergebnis eindeutig. Gemessen
wird, wie stark es sich ändert, wenn man ausschliesslich diese eine,
inhaltlich beliebige Grösse variiert — Kursdaten, Signale, Parameter und
Simulationslogik bleiben identisch. Es gibt hier keine Stichprobenunsicherheit
zu quantifizieren; die berichtete Spanne ist die vollständige Bandbreite
gleichermassen legitimer Ergebnisse.

### Scope-Grenzen

Nur die **Portfolio-Simulation** wird untersucht. Nicht untersucht: ob die
Signalerkennung selbst reihenfolgeabhängig ist (sie ist es nicht — sie läuft
je Symbol unabhängig), und ob eine bestimmte Tie-Breaking-Regel besser wäre.
Für die Live-Bots wird die Verarbeitungsreihenfolge nur **beschrieben**
(Abschnitt 6), nicht bewertet.

### Reproduktion

```
cd research/order_sensitivity
python3 test_order_core.py           # 32 Sanity-Checks
python3 run_all.py                   # alle 9 Bots (~2 min)
python3 decisions.py <bot>           # Entscheidungs-Robustheit je Bot
python3 live_order_observation.py    # Live-Verarbeitungsreihenfolge
python3 aggregate_report.py          # Uebersichtstabellen
```

---

## 1. Kurzfassung

**Ja, die ursprünglichen Backtests sind betroffen — und zwar deutlich stärker
als die Research-Studien vermuten liessen.** Bei **3 von 9 Bots** verschiebt
allein die willkürliche Verarbeitungsreihenfolge die Calmar-Ratio um mehr als
das Vierfache; bei `rsi2_mean_reversion` um das **Zwölffache** (0,21 bis 2,54).

Drei Befunde, die über die ursprüngliche Vermutung hinausgehen:

1. **Der Engpass ist fast nie das Kapital, sondern das Positionslimit.** Über
   alle 9 Bots hinweg sind praktisch **100 % der Ablehnungen** durch
   `MAX_CONCURRENT_POSITIONS` verursacht, nicht durch fehlendes Kapital. Bei
   10 % Allokation binden 8 Positionen erst 80 % des Kapitals — die
   Kapitalprüfung greift schlicht nie zuerst. Die Reihenfolge entscheidet
   also darüber, wer einen der 8 Plätze bekommt.
2. **Die Ablehnungsquoten sind teils extrem**: `turtle_soup_stocks` verwirft
   **84,4 %** aller gefundenen Signale, `volatility_breakout` 72,6 %,
   `rsi2_mean_reversion` 51,0 %. Bei diesen drei ist auch der Anteil
   *umstrittener* Trades (Ausführungs-Status über die Permutationen nicht
   konstant) mit rund **50 %** am höchsten.
3. **Bei `turtle_soup_crypto` liegt der ursprünglich berichtete Wert im
   96,6. Perzentil** der Permutations-Verteilung — die tatsächlich verwendete
   Reihenfolge war dort eine ungewöhnlich günstige Ziehung (Calmar 5,48 bei
   einer Spanne von 2,41 bis 6,51, Median 4,07).

**Zu den bereits getroffenen Entscheidungen (Abschnitt 5): keine der sechs
geprüften kippt.** Fünf bleiben über die Permutationen hinweg klar bestätigt.
Die sechste — die Take-Profit-Deaktivierung beim Aktien-Elliott-Wave-Bot —
kippt ebenfalls nicht, aber die Prüfung legt etwas anderes offen: sie war
nie eine Calmar-Entscheidung, sondern eine reine Rendite-Entscheidung, und
das in **jeder** Permutation.

**Live-Perspektive (nur Beobachtung):** 8 der 9 Bots setzen das
Positionslimit auch in `forward_test.py` durch und iterieren dabei über eine
nach Marktkapitalisierung bzw. 24-Stunden-Volumen **absteigend sortierte**
Symbolliste. Die Reihenfolge ist dort also nicht zufällig, sondern
systematisch — die grössten Werte erhalten strukturell zuerst einen Platz.

---

## 2. Der Mechanismus

Alle 9 Bots nutzen dieselbe ereignisbasierte Schleife:

```python
events.sort(key=lambda e: (e[0], e[1] != "exit"))
```

Bei **gleichem Zeitstempel** ist diese Sortierung stabil. Die Reihenfolge
entspricht damit der Zeilenreihenfolge des Trade-DataFrames — und die wiederum
der Reihenfolge, in der `collect_all_trades()` die Symbole durchlaufen hat,
also der Reihenfolge der Symbolliste in der Konfigurationsdatei.

Solange Kapital **und** Positionslimit für alle gleichzeitigen Signale
reichen, ist das folgenlos. Reichen sie nicht, entscheidet diese Reihenfolge,
**welche** Signale zu Trades werden. Sie wurde nie bewusst gewählt.

`test_order_core.py` belegt beide Randfälle: ohne Engpass ist die Permutation
exakt wirkungslos (identisches Ergebnis in allen Läufen), mit Engpass streut
das Ergebnis.

---

## 3. Methodik

**Permutation:** Zeilen zufällig mischen, danach **stabil** nach `entry_time`
sortieren. Die chronologische Abfolge bleibt exakt erhalten; verschoben wird
ausschliesslich die Rangfolge innerhalb identischer Zeitstempel. Die
Simulation sieht dieselben Trades zu denselben Zeitpunkten.

`kind="stable"` ist zwingend — pandas' Standard (quicksort) ist nicht stabil
und würde die gemischte Reihenfolge teilweise wieder überschreiben.

**Drei Kennzahlen je Bot:**

- **Anteil geteilter Zeitstempel** — notwendige, aber nicht hinreichende
  Bedingung dafür, dass die Reihenfolge überhaupt wirken kann.
- **Ablehnungsquote**, getrennt nach Positionslimit und Kapital. Das Original
  zählt beides zusammen; die Trennung ist neu und liefert den zentralen
  Befund dieser Untersuchung.
- **Anteil umstrittener Trades** — Trades, deren Ausführungs-Status über die
  500 Permutationen **nicht konstant** ist. Das ist die eigentlich
  aussagekräftige Grösse: ein Bot kann eine hohe Ablehnungsquote haben und
  trotzdem unempfindlich sein, wenn immer dieselben Trades abgelehnt werden.

---

## 4. Getroffene Annahmen

1. **Konfiguration aus `equity_simulation.py`, nicht aus `live_params.py`.**
   Die Frage lautet, ob die *ursprünglichen* Backtests betroffen sind, und
   der ursprüngliche Backtest ist das, was `python3 equity_simulation.py`
   ausgibt. **Nebenbefund:** bei vier Bots weichen die beiden inzwischen
   voneinander ab — siehe Abschnitt 7.
2. **500 Permutationen**, identisch zu `research/trailing_stops/` und
   `research/vbc_deepdive/`, damit die Zahlen vergleichbar bleiben. Seed
   20260907, fest.
3. **Einstufung der Betroffenheit** (`aggregate_report.py::classify`):
   < 2 % umstrittene Trades = „praktisch nicht betroffen"; sonst nach dem
   Verhältnis max/min der Calmar-Spanne (≥ 3× = „stark", ≥ 1,5× =
   „spürbar"). Selbst gewählte, dokumentierte Heuristik, kein Standardmass.
4. **Gepaarter Vergleich bei den Entscheidungen**, wo beide Varianten
   denselben Trade-Satz haben (Kapitalparameter). Wo sich die Trade-Sätze
   unterscheiden (Take-Profit an/aus), ist die Paarung nur nominell — bei
   der betroffenen Entscheidung vermerkt.
5. **`elliott_wave` hat keinen Positionslimit-Parameter.** Dessen
   `simulate_portfolio()` kennt schlicht kein `max_concurrent_positions`.
   Das ist kein Versehen dieser Untersuchung, sondern der Stand jenes Bots —
   und der Grund, warum er als einziger praktisch nicht betroffen ist.

---

## 5. Frage 1 + 2 + 3: Ausmass und Auswirkung

### Ausmass

| Bot | Trades | geteilte Zeitstempel | grösste Gruppe | Limit | abgelehnt | davon kapitalbedingt | **umstritten** |
|---|---|---|---|---|---|---|---|
| `elliott_wave` | 783 | 46,1 % | 9 | keins | 1 (0,1 %) | 1,0 | **9 (1,1 %)** |
| `elliott_wave_stocks` | 519 | 63,6 % | 19 | 8 | 50 (9,6 %) | 0,0 | **113 (21,8 %)** |
| `t3_supertrend` | 980 | 43,8 % | 9 | 5 | 324 (33,1 %) | 0,0 | **143 (14,6 %)** |
| `rsi2_crypto` | 439 | 65,8 % | 9 | 8 | 47 (10,7 %) | 0,0 | **65 (14,8 %)** |
| `rsi2_mean_reversion` | 5391 | 90,7 % | 46 | 8 | 2750 (51,0 %) | 0,0 | **2703 (50,1 %)** |
| `turtle_soup_crypto` | 1599 | 84,4 % | 20 | 8 | 185 (11,6 %) | 0,0 | **508 (31,8 %)** |
| `turtle_soup_stocks` | 12069 | 96,5 % | 68 | 8 | 10182 (84,4 %) | 0,0 | **6035 (50,0 %)** |
| `volatility_breakout` | 4510 | 87,7 % | 24 | 8 | 3274 (72,6 %) | 0,0 | **2312 (51,3 %)** |
| `volatility_breakout_crypto` | 359 | 59,6 % | 9 | 8 | 49 (13,6 %) | 0,0 | **62 (17,3 %)** |

**Die Spalte „davon kapitalbedingt" ist der wichtigste Einzelbefund dieser
Tabelle.** Sie ist bei acht von neun Bots exakt null: der Engpass ist immer
das Positionslimit, nie das Kapital. Nur `elliott_wave`, der einzige Bot ohne
Limit, hat überhaupt eine kapitalbedingte Ablehnung — und zwar genau eine.

Das ist rechnerisch zwingend: bei 10 % Allokation binden 8 offene Positionen
80 % des Kapitals. Das Limit greift, bevor das Kapital knapp wird. Die im
Projekt gelegentlich verwendete Formulierung „nicht genug freies Kapital"
beschreibt also nicht, was tatsächlich passiert.

### Auswirkung

| Bot | ursprünglich berichtet | min | Median | max | Faktor | Perzentil | Einstufung |
|---|---|---|---|---|---|---|---|
| `elliott_wave` | 1193,97 | 1189,21 | 1193,79 | 1197,19 | 1,0× | 56,4 | praktisch nicht betroffen |
| `t3_supertrend` | 5,84 | 4,72 | 5,71 | 6,40 | 1,4× | 66,0 | leicht betroffen |
| `volatility_breakout_crypto` | 4,25 | 2,98 | 3,52 | 4,90 | 1,6× | 61,4 | spürbar betroffen |
| `rsi2_crypto` | 2,13 | 1,50 | 2,11 | 2,77 | 1,8× | 52,6 | spürbar betroffen |
| `elliott_wave_stocks` | 789,75 | 475,78 | 704,35 | 919,67 | 1,9× | 74,6 | spürbar betroffen |
| `turtle_soup_crypto` | 5,48 | 2,41 | 4,07 | 6,51 | 2,7× | **96,6** | spürbar betroffen |
| `volatility_breakout` | 6,34 | 2,86 | 7,11 | 12,43 | 4,3× | 31,4 | **stark betroffen** |
| `turtle_soup_stocks` | 4,09 | 1,38 | 3,91 | 8,16 | 5,9× | 57,8 | **stark betroffen** |
| `rsi2_mean_reversion` | 1,37 | 0,21 | 1,21 | 2,54 | **12,1×** | 65,0 | **stark betroffen** |

**Lage des ursprünglichen Werts:** bei sieben Bots liegt er im mittleren
Bereich (31. bis 75. Perzentil) — die tatsächlich verwendete Reihenfolge war
dort also typisch. Zwei Ausnahmen:

- **`turtle_soup_crypto`, 96,6. Perzentil:** der berichtete Wert 5,48 liegt
  fast am oberen Rand einer Spanne von 2,41 bis 6,51 (Median 4,07). Nur rund
  3 % der gleichermassen legitimen Reihenfolgen hätten ein besseres Ergebnis
  geliefert. Die Zahl stellt den Bot damit systematisch zu gut dar.
- **`volatility_breakout`, 31,4. Perzentil:** hier umgekehrt — der berichtete
  Wert 6,34 liegt unter dem Median 7,11. Die verwendete Reihenfolge war eine
  eher ungünstige Ziehung.

### Max Drawdown

| Bot | min | Median | max |
|---|---|---|---|
| `elliott_wave` | −1,83 | −1,83 | −1,83 |
| `volatility_breakout_crypto` | −16,77 | −16,77 | −16,77 |
| `t3_supertrend` | −22,85 | −22,32 | −22,14 |
| `elliott_wave_stocks` | −2,96 | −2,22 | −1,90 |
| `rsi2_crypto` | −14,85 | −13,45 | −12,25 |
| `volatility_breakout` | −27,06 | −22,02 | −18,75 |
| `rsi2_mean_reversion` | −27,72 | −22,30 | −16,92 |
| `turtle_soup_stocks` | −37,61 | −31,97 | −27,35 |
| `turtle_soup_crypto` | −43,05 | −36,55 | −30,83 |

**Wichtige Korrektur zu den beiden Vorgänger-Untersuchungen:** dort wurde
festgehalten, der Max Drawdown sei gegenüber der Reihenfolge „weitgehend
invariant". Über alle 9 Bots gilt das **nicht**. Es gilt für die gering
ausgelasteten Bots (`elliott_wave`, `volatility_breakout_crypto`: exakt
konstant; `t3_supertrend`: 0,7 Prozentpunkte Spanne) — genau jene, die dort
betrachtet wurden. Bei den stark ausgelasteten Bots schwankt der Drawdown
erheblich: `turtle_soup_crypto` zwischen −30,83 % und −43,05 %,
`rsi2_mean_reversion` zwischen −16,92 % und −27,72 %. Die dort formulierte
Verallgemeinerung war zu weit gefasst.

---

## 6. Frage 4: Halten die bereits getroffenen Entscheidungen stand?

Für jede Entscheidung wurden **beide** verglichenen Konfigurationen über 500
Permutationen gerechnet und ausgezählt, in wie vielen die tatsächlich
gewählte Variante besser abschneidet.

| Entscheidung | Bot | gewählt besser in … der Permutationen | Urteil |
|---|---|---|---|
| Kapitalmanagement unverändert (10 % / Limit 8) | `turtle_soup_crypto` | Calmar **100 %**, Rendite **100 %** | **robust** |
| `MAX_CONCURRENT_POSITIONS = 5` statt 8 | `t3_supertrend` | Calmar **96,8 %**, Drawdown **100 %** | **robust** |
| 5 % Allokation / Limit 20 statt 10 % / 8 | `rsi2_mean_reversion` | Calmar **93,6 %**, Rendite 91,8 % | **robust** |
| `MAX_CONCURRENT_POSITIONS = 15` statt 8 | `volatility_breakout` | Rendite **96,6 %**, Calmar 85,6 % | **robust** |
| 2 % Allokation / unbegrenzt statt 10 % / 8 | `turtle_soup_stocks` | Calmar 77,8 %, Drawdown 89,8 % | **überwiegend robust** |
| `USE_TAKE_PROFIT = False` | `elliott_wave_stocks` | Rendite **100 %**, Calmar **0 %** | **robust, aber siehe unten** |

**Keine der sechs Entscheidungen kippt durch die Reihenfolge-Willkür.** Das
ist das beruhigende Hauptergebnis dieses Abschnitts — auch und gerade bei den
drei stark betroffenen Bots: die Streuung ist zwar gross, trifft aber beide
verglichenen Varianten gleichermassen, und der gepaarte Vergleich (dieselbe
Permutation auf beide angewendet) kürzt sie weitgehend heraus.

**Zur Take-Profit-Entscheidung bei `elliott_wave_stocks`** ist eine
Präzisierung nötig, die nichts mit der Reihenfolge zu tun hat, aber bei
dieser Prüfung auffiel: „ohne Take-Profit" liefert in **100 %** der
Permutationen die höhere Rendite (+3084 % gegen +1500 %) und in **100 %** der
Permutationen die **schlechtere** Calmar-Ratio (315 gegen 790, weil der
Drawdown von −1,90 % auf −9,79 % steigt). Beide Aussagen sind über alle
Permutationen stabil — die Entscheidung ist also robust, war aber eine reine
Rendite-Entscheidung. Unter der in allen späteren Untersuchungen verwendeten
Calmar-Konvention wäre sie anders ausgefallen. Das ist eine
Konsistenz-Beobachtung, keine Fehlerfeststellung: die Entscheidung wurde
seinerzeit ausdrücklich mit „Gewinne laufen lassen" begründet, und der höhere
Drawdown ist in `live_params.py` dokumentiert.

**Zusatzbefund `t3_supertrend`:** Limit 5 gewinnt auf Calmar (96,8 %) und
Drawdown (100 %), verliert aber bei der reinen Rendite gegen Limit 8 (nur
7,2 %). Auch das ist über alle Permutationen stabil — die damalige Wahl von 5
war eine bewusste Risiko-Entscheidung, keine Rendite-Maximierung, und
bestätigt sich als solche.

---

## 7. Frage 5: Verarbeitungsreihenfolge im Live-Code (nur Beobachtung)

| Bot | iteriert über die Symbolliste | setzt Positionslimit durch | Symbolliste |
|---|---|---|---|
| `elliott_wave` | ja | **nein** | `config/top25_symbols.txt` |
| die übrigen 8 | ja | **ja** | `top25_symbols.txt` bzw. `sp500_top150.txt` |

Alle Bots iterieren mit `for symbol in SYMBOLS` über die Liste aus ihrer
Konfigurationsdatei. Keiner sortiert sie selbst um.

**Die Listen sind nicht neutral geordnet:**

- `config/sp500_top150.txt` — erzeugt von `get_top_stocks.py`, **absteigend
  nach Marktkapitalisierung**. Anfang: NVDA, AAPL, GOOGL, GOOG, MSFT, AMZN,
  AVGO, META.
- `config/top25_symbols.txt` — erzeugt von `get_top_symbols.py`, **absteigend
  nach 24-Stunden-Handelsvolumen**. Anfang: BTCUSDT, ETHUSDT, SOLUSDT,
  ZECUSDT, XRPUSDT.

**Beobachtung:** die Verarbeitungsreihenfolge im Live-Betrieb ist damit fest
und reproduzierbar — kein Zufall. Sie ist aber nicht willkürlich im Sinne von
„beliebig", sondern **systematisch**: wenn das Positionslimit erreicht ist,
erhalten strukturell immer die Symbole mit der grössten Marktkapitalisierung
bzw. dem höchsten Volumen den freien Platz. Ob das erwünscht ist, ist nicht
Gegenstand dieser Untersuchung. Auftragsgemäss nur beschrieben.

---

## 8. Was das für die bisherigen Untersuchungen bedeutet

- **Die vier Backlog-Untersuchungen und die Vertiefungsstudie** haben diesen
  Effekt für `t3_supertrend`, `volatility_breakout` und
  `volatility_breakout_crypto` bereits gemessen; die Zahlen dort stimmen mit
  den hier ermittelten überein, soweit dieselbe Konfiguration verwendet wurde.
- **Neu und über jene Studien hinausgehend:** `rsi2_mean_reversion`,
  `turtle_soup_stocks` und `turtle_soup_crypto` sind ebenso stark oder stärker
  betroffen und waren dort gar nicht untersucht.
- **Zu korrigieren:** die dort formulierte Verallgemeinerung, der Drawdown sei
  gegenüber der Reihenfolge weitgehend stabil, gilt nur für die gering
  ausgelasteten Bots (Abschnitt 5).
- **Nebenbefund (nicht Teil der Fragestellung):** bei vier Bots weichen die
  Konstanten in `equity_simulation.py` inzwischen von `live_params.py` ab —
  `volatility_breakout` (Limit 8 gegen live 15), `rsi2_mean_reversion` (10 % /
  8 gegen live 5 % / 20), `turtle_soup_stocks` (10 % / 8 gegen live 2 % /
  unbegrenzt), `elliott_wave_stocks` (`USE_TAKE_PROFIT = True` gegen live
  `False`). Wer `equity_simulation.py` direkt ausführt, erhält also nicht die
  Live-Konfiguration. Reine Beobachtung.

---

## 9. Gesamteinschätzung (unaufgeregt, ohne Handlungsempfehlung)

Die Ausgangsfrage war, ob eine in den Research-Studien entdeckte Willkür auch
die ursprünglichen, als validiert geltenden Backtests betrifft. Die Antwort
ist ja, und bei drei Bots (`rsi2_mean_reversion`, `turtle_soup_stocks`,
`volatility_breakout`) in einer Grössenordnung, die einzelne berichtete
Kennzahlen weitgehend entwertet — eine Calmar-Ratio, die je nach beliebiger
Reihenfolge zwischen 0,21 und 2,54 liegen kann, trägt als Einzelzahl keine
Aussage.

Gleichzeitig gilt: **keine der sechs geprüften, bereits umgesetzten
Entscheidungen kippt dadurch.** Der Grund ist strukturell und nicht Zufall:
Entscheidungen sind Vergleiche zwischen zwei Konfigurationen, und die
Reihenfolge-Willkür trifft beide Seiten gleichermassen. Sie verzerrt die
*absoluten* Kennzahlen erheblich, aber nur selten deren *Rangfolge*.

Zwei Punkte, die über den Auftrag hinaus auffielen und ohne Bewertung
festgehalten seien:

- Der Engpass ist durchgängig das **Positionslimit**, nicht das Kapital.
  Wer die Reihenfolge-Empfindlichkeit reduzieren wollte, hätte dort den
  Hebel — nicht bei der Allokation.
- Der berichtete Wert von `turtle_soup_crypto` liegt im 96,6. Perzentil
  seiner Verteilung. Das ist der einzige Bot, bei dem eine bereits
  dokumentierte Kennzahl den Bot spürbar zu gut darstellt.

Ob und was daraus folgt — insbesondere ob eine bewusste Tie-Breaking-Regel
eingeführt werden sollte — ist ausdrücklich nicht Teil dieser Untersuchung.

---

## 10. Explizit ausserhalb des Scopes

Jede Code-Änderung an bestehenden Backtest- oder Live-Dateien; die Einführung
einer „korrekten" Tie-Breaking-Regel; jede Bewertung der Live-Sortierung nach
Marktkapitalisierung/Volumen; jede Aktivierungsempfehlung; die
BTC-Regimefilter-Untersuchung (auftragsgemäss zurückgestellt).

## 11. Dateien

| Datei | Inhalt |
|---|---|
| `order_core.py` | Permutation, NumPy-Simulation, Ablehnungsgründe, Streuungs- und Perzentil-Kennzahlen |
| `run_one_bot.py` | Analyse je Bot, ruft die bot-eigenen Original-Funktionen auf; Äquivalenz-Nachweis |
| `run_all.py` | alle 9 Bots, je eigener Prozess |
| `decisions.py` | Robustheit der 6 dokumentierten Entscheidungen |
| `live_order_observation.py` | Verarbeitungsreihenfolge im Live-Code (Beobachtung) |
| `test_order_core.py` | 32 Sanity-Checks inkl. Abgleich gegen eine wortgetreue Kopie der Bot-Funktion |
| `aggregate_report.py` | Übersichtstabellen, `results/summary_table.json` |
| `results/` | je Bot eine JSON, dazu Entscheidungen, Live-Beobachtung und Gesamttabelle |
