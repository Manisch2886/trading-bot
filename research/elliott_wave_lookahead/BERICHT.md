# Elliott-Wave-Zigzag-Look-Ahead im Backtest — Untersuchung

> ## ✅ Nachtrag: der Backtest ist inzwischen korrigiert
>
> Diese Untersuchung hat den Look-Ahead beschrieben und beziffert. **Beide
> Kanäle sind seither im Bot-Code behoben** — siehe Abschnitt **„Nachtrag K"**
> am Ende dieses Berichts. Die Abschnitte 1–8 beschreiben also den Zustand
> VOR der Korrektur; die Mechanismus-Erklärung gilt unverändert, die
> Baseline-Zahlen sind Geschichte.
>
> Kurz: `equity_simulation.py`/`backtest_elliott.py` steigen jetzt zum
> Bestätigungskurs ein, und die Wellenauswahl ist kausal
> (`find_causal_waves`). **1301 Trades einzeln geprüft, 0
> Kausalitätsverletzungen.** `forward_test.py` und `live_params.py` blieben
> unverändert.


**Status: reine Untersuchung. KEINE Änderung an `equity_simulation.py`,
`forward_test.py`, `live_params.py`, `portfolio_overview.py` oder irgendeiner
`equity_curve.csv`. Keine Korrektur- oder Aktivierungsempfehlung.** Alle Skripte
liegen ausschliesslich unter `research/elliott_wave_lookahead/`.

---

## 0. Entscheidungsgrundlage

### Die vier Antworten in Kurzform

| Frage | Antwort |
|---|---|
| **1 Mechanismus** | Der Zigzag-Indikator selbst — nicht eine Eigenheit von `equity_simulation.py`. Ein Pivot **ist** erst dann ein Pivot, wenn der Kurs sich danach um `deviation_pct` in die Gegenrichtung bewegt hat. Der Backtest steigt trotzdem zum Zeitpunkt **und Preis** des Pivots ein. |
| **2 `forward_test.py` korrigiert?** | **Ja, bestätigt** — bei beiden Bots, und im Übergabeprotokoll (Abschnitt 3, „Wichtiger behobener Bug") dokumentiert. Der Mechanismus ist allerdings **keine Bestätigungs-Verzögerung**, sondern eine Einstiegspreis-Korrektur. |
| **3 Auswirkung** | Massiv. `elliott_wave`: **+2184,96 % → −24,44 %** (aus einer der profitabelsten Strategien wird eine verlustbringende). `elliott_wave_stocks`: **+3084,09 % → +338,26 %**, Calmar 315,02 → 15,24. |
| **4 Entscheidungen** | Die Take-Profit-Entscheidung **hält und wird sogar besser begründet**. Die Parameterwahl dagegen hält nicht: bei `elliott_wave` besteht **keine einzige** der 36 Rasterkombinationen mehr die projekteigenen Mindestfilter. |
| **5 Telegram** | **Prämisse korrigiert:** die Telegram-Berichte sind **nicht** betroffen — sie lesen ausschliesslich die Live-Datenbanken. Betroffen ist die **wöchentliche Portfolio-E-Mail**. |

### Datenbasis

| Bot | Symbole | Zeitraum | Balken | Baseline-Trades |
|---|---|---|---|---|
| `elliott_wave` | 18 Kryptos | 2021-09-07 … 2026-08-27 (4,97 J.) | 1 h | 783 |
| `elliott_wave_stocks` | 147 Aktien | 2016-10-27 … 2026-09-01 (9,85 J.) | 1 d | 519 |

### Pflicht-Gegenchecks — vor allem anderen

`verify_baseline.py`, **13/13 je Bot**:

1. **85 219 Zigzag-Pivots** (42 272 + 42 947) über alle 165 Symbole beider Bots
   sind **exakt identisch** zur unveränderten `zigzag_indicator.calculate_zigzag`.
   Die Zusatzspalte ändert nichts an der Erkennung.
2. Der Trade-Nachbau erzeugt **Trade für Trade denselben Satz** wie die
   bot-eigene `equity_simulation.collect_all_trades` — gleiche Anzahl, gleiche
   Einstiegs- und Ausstiegspreise, gleiche Ausstiegszeitpunkte, gleiche
   Ergebnis-Kategorien, Abweichung 0 bei allen 1302 Trades.
3. Die Baseline trifft die **veröffentlichten Kennzahlen** exakt:
   `elliott_wave` 783 Trades / 782 ausgeführt / +2184,96 % / −1,83 %
   (aus `research/order_sensitivity/`, PR #23) und `elliott_wave_stocks`
   519 / 288 / +3084,09 % / −9,79 % (aus
   `results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md` — genau die Zahl, mit
   der die Take-Profit-Entscheidung begründet ist).

Dazu `decisions.py`: **9/9** Zellen der veröffentlichten 2×4-Matrix exakt
reproduziert, bevor irgendeine korrigierte Zelle gerechnet wird. Und
`test_lookahead.py`: **21** Sanity-Checks auf konstruierten Kursreihen.

### Belastbarkeit

Der Befund hängt **nicht** an einer statistischen Schätzung, sondern an einer
Konstruktionseigenschaft, die sich abzählen lässt:

* Der Backtest kauft in **100 % der Trades** günstiger, als es live möglich war
  (Median 4,06 % bzw. 5,64 % unter dem Bestätigungskurs).
* In **0 von 783** bzw. **0 von 519** Trades konnte der Stop vor der Bestätigung
  überhaupt ausgelöst werden.

Beides ist kein Messergebnis mit Streubreite, sondern eine Zählung. Die
Unsicherheit steckt allein in der Frage, wie man den korrigierten Einstieg
modelliert — dafür ist die Variante `verzoegert` da (siehe Annahme K-A2), und
sie ändert nichts am Bild.

### Scope-Grenzen — was diese Untersuchung NICHT leistet

* **Die Korrektur ist unvollständig, und zwar zugunsten der Strategie.** Die
  Wellenerkennung (`find_impulse_waves` + `remove_overlapping`) läuft weiterhin
  über die **gesamte** Historie auf einmal. Eine Welle kann dort zugunsten einer
  **späteren**, besser bewerteten Welle verworfen werden — auch das ist
  Zukunftswissen. Die korrigierten Zahlen unten sind deshalb **weiterhin zu
  optimistisch**, nicht zu pessimistisch (siehe Abschnitt 6).
* Keine Aussage darüber, ob die Strategie mit anderen Parametern funktionieren
  würde. Das Raster wird nur nachgerechnet, nicht erweitert.
* Keine Bewertung der Live-Ergebnisse. Die Live-Datenbanken sind in diesem
  Repo nicht vorhanden.
* Keine Korrektur irgendeiner Datei ausserhalb dieses Verzeichnisses.

### Reproduktion

```
cd research/elliott_wave_lookahead
python3 run_all.py                          # alles, in der richtigen Reihenfolge
# oder einzeln:
python3 test_lookahead.py                   # 21 Sanity-Checks
python3 verify_baseline.py elliott_wave     # 13/13 - Gate für alles Weitere
python3 run_one_bot.py elliott_wave         # drei Varianten + Mechanismus-Diagnose
python3 grid.py elliott_wave                # Rasteroptimierung, beide Grundlagen
python3 decisions.py elliott_wave_stocks    # 2×4-Matrix, beide Grundlagen
```

`run_all.py` bricht ab, sobald ein Regressionscheck fehlschlägt.

---

## 1. Der Mechanismus, in einfachen Worten (Frage 1)

### Die Ursache liegt im Indikator, nicht im Simulationsskript

Ein Zigzag markiert Hoch- und Tiefpunkte. Aber: **man weiss erst hinterher, dass
ein Tief ein Tief war.** Der Indikator trägt einen Tiefpunkt erst dann ein, wenn
der Kurs von dort aus wieder um `deviation_pct` gestiegen ist — vorher könnte es
ja noch tiefer gehen. Im Code (`zigzag_indicator.py`) ist das die Zeile

```python
elif (highs[i] - last_pivot_price) / last_pivot_price * 100 >= deviation_pct:
    pivots.append((times[last_pivot_idx], last_pivot_price, "low"))
```

Der eingetragene Zeitstempel ist `times[last_pivot_idx]` — der des **Tiefs**.
Erkannt wurde es aber am Balken `i`, also **später**. Diese Lücke ist der ganze
Look-Ahead. Sie ist keine Nachlässigkeit, sondern liegt in der Natur des
Indikators; jeder Zigzag verhält sich so.

Der Backtest (`backtest_elliott.py::run_backtest`) benutzt dann:

```python
entry_time = pd.to_datetime(wave["end_time"])   # Zeitpunkt des Pivots
entry_price = wave["wave5"]                     # PREIS des Pivots
```

Er kauft also zu einem Zeitpunkt und Preis, die zum Kaufzeitpunkt noch niemand
kennen konnte.

### Daraus folgen zwei Vorteile — beide messbar

**Kanal 1: Der Einstieg liegt auf dem Tiefpunkt des ganzen Abwärtsschenkels.**

Solange der Zigzag im Abwärtstrend ist, verschiebt er den Pivot bei jedem neuen
Tief nach unten (`if lows[i] < last_pivot_price: last_pivot_price = lows[i]`).
Der schliesslich eingetragene Pivot ist damit **das Minimum des gesamten
Schenkels**. Zwei Konsequenzen:

* Der Backtest kauft zum **besten Kurs, den es in dieser Bewegung gab** — im
  Median **4,06 %** (Krypto) bzw. **5,64 %** (Aktien) unter dem Kurs, den der
  Live-Bot bei der Bestätigung zahlen musste. Gemessen: **in 100 % der Trades**
  günstiger, nie teurer.
* Der Stop-Loss liegt X % **unter** diesem Minimum. Zwischen Einstieg und
  Bestätigung kann er daher **mathematisch nicht ausgelöst werden**. Gemessen:
  **0 von 783** und **0 von 519** Trades.

**Kanal 2: Die Gegenbewegung ist garantiert — aber nur, wenn ein Ziel gesetzt ist.**

Bis zur Bestätigung muss der Kurs per Konstruktion **mindestens
`deviation_pct`** über den Pivot gestiegen sein. Liegt das Kursziel innerhalb
dieser Distanz, ist der Gewinn sicher, bevor das Signal überhaupt existiert.

Bei `elliott_wave` (Ziel im Median 5,42 %, garantierte Gegenbewegung 4,0 %)
trifft das auf **19,4 %** der Trades zu. Und **46,2 % aller Trades waren
bereits vollständig entschieden**, bevor ihr Signal erkennbar war.

Bei `elliott_wave_stocks` ist `USE_TAKE_PROFIT = False` — es gibt kein Ziel, das
die Konstruktion garantieren könnte. **Kanal 2 entfällt dort vollständig, Kanal 1
wirkt weiter** — und richtet, wie Abschnitt 3 zeigt, allein schon genug an.

### Wie viel Zukunft der Backtest kennt

| Bot | Median | Mittel | Maximum |
|---|---|---|---|
| `elliott_wave` (1 h) | 2 Balken | 4,2 | 198 |
| `elliott_wave_stocks` (1 d) | 1 Balken | 1,8 | 10 |

Das klingt wenig. Entscheidend ist aber nicht die Dauer, sondern **was** in
dieser Zeit garantiert ist: ein unerreichbarer Stop und eine sichere
Aufwärtsbewegung.

---

## 2. Ist `forward_test.py` wirklich korrigiert? (Frage 2)

**Ja — bestätigt, bei beiden Bots, im Code nachgelesen.**

Der Korrekturmechanismus ist allerdings **nicht** der in der Fragestellung
vermutete („Bestätigungs-Verzögerung, bevor ein Zigzag-Punkt als abgeschlossen
gilt"), sondern eine **Einstiegspreis-Korrektur**. Beide Dateien enthalten
wortgleich:

```python
# WICHTIG: Als Einstiegspreis den AKTUELLEN Marktpreis nehmen,
# nicht den historischen Preis vom Wellenende - sonst wuerde
# ein Trade zu einem laengst vergangenen Kurs eroeffnet.
latest_price_row = df[df["open_time"] > end_time]
if latest_price_row.empty:
    continue
entry_price = latest_price_row.iloc[-1]["close"]
entry_reference_time = latest_price_row.iloc[-1]["open_time"]

total_move = abs(wave["wave5"] - wave["wave0"])
target_price = entry_price + total_move * TAKE_PROFIT_FIB
stop_price = entry_price * (1 - STOP_LOSS_PCT / 100)
```

Vier Dinge stellen die Kausalität sicher:

1. **Der Einstiegspreis ist der letzte verfügbare Schlusskurs**, nicht der
   Pivot-Preis. Zum Laufzeitpunkt ist die Bestätigung bereits geschehen — der
   Preis liegt also mindestens `deviation_pct` über dem Pivot. **Beide Kanäle
   aus Abschnitt 1 sind damit geschlossen.**
2. **Ziel und Stop werden aus diesem neuen Einstiegspreis neu berechnet**, nicht
   aus dem Pivot. Der Stop liegt damit unter dem *aktuellen* Kurs und ist ganz
   normal erreichbar.
3. **Ein Frische-Fenster** (`SIGNAL_FRESHNESS_HOURS = 48` bzw.
   `SIGNAL_FRESHNESS_DAYS = 5`) verwirft Muster, deren Wellenende zu lange
   zurückliegt.
4. **Das Datenbankschema trennt `signal_time` von `entry_time`** — Wellenende
   und tatsächlicher Ausführungszeitpunkt sind getrennte Spalten.

Die frühere Notiz ist damit **korrekt**. Sie wird zusätzlich vom Übergabeprotokoll
gestützt (Abschnitt 3, „Wichtiger behobener Bug"), das denselben Sachverhalt und
dieselbe Lösung beschreibt — inklusive des Zusatz-Fixes, den Cronjob von täglich
auf **stündlich** umzustellen, damit die Erkennung zur Stundenkerzen-Auflösung
passt.

**Die Lücke besteht also nur im Backtest.** Der Live-Bot handelt sauber; die
Zahlen, mit denen er begründet wurde, stammen aus einer Simulation, die er so
nie hätte nachvollziehen können.

---

## 3. Wie stark verschiebt sich der Backtest? (Frage 3)

Alle Varianten mit den **live gesetzten** Parametern und der bot-eigenen,
unveränderten `simulate_portfolio`.

### `elliott_wave` (Krypto, 1 h, Zigzag 4 %, Stop 2 %, Take-Profit-Fib 0,236)

| Variante | Trades | ausgeführt | Rendite | Max DD | **Calmar** | Gewinnrate | Ø PnL |
|---|---|---|---|---|---|---|---|
| **baseline** (heutiger Backtest) | 783 | 782 | **+2184,96 %** | −1,83 % | **1193,97** | 82,9 % | +4,04 % |
| **korrigiert** | 780 | 780 | **−24,44 %** | **−25,58 %** | **−0,96** | 27,7 % | −0,35 % |
| verzögert (+1 Balken) | 780 | 780 | −31,76 % | −32,62 % | −0,97 | 26,3 % | −0,48 % |

**Aus einer Strategie mit +2185 % und praktisch keinem Drawdown wird eine
Strategie, die Geld verliert.** Die Ergebnis-Verteilung dreht sich um: aus
649 Take-Profits und 134 Stops werden **564 Stops und 216 Take-Profits**.

### `elliott_wave_stocks` (Aktien, 1 d, Zigzag 5 %, Stop 3 %, Take-Profit AUS, Limit 8)

| Variante | Trades | ausgeführt | Rendite | Max DD | **Calmar** | Gewinnrate | Ø PnL |
|---|---|---|---|---|---|---|---|
| **baseline** (heutiger Backtest) | 519 | 288 | **+3084,09 %** | −9,79 % | **315,02** | 43,9 % | +14,88 % |
| **korrigiert** | 497 | 392 | **+338,26 %** | **−22,19 %** | **15,24** | 21,7 % | +4,87 % |
| verzögert (+1 Balken) | 485 | 389 | +332,99 % | −23,39 % | 14,24 | 19,8 % | +3,78 % |

Hier bleibt die Strategie profitabel — aber die Rendite fällt auf **11 %** des
berichteten Werts, der Drawdown **verdoppelt sich mehr als**, und die
Calmar-Ratio fällt um **den Faktor 21**. Bemerkenswert: das passiert **ohne**
Kanal 2, allein durch den Einstiegspreis.

**Die `verzoegert`-Variante ändert am Bild nichts** — der Befund hängt nicht an
der genauen Modellierung des Ausführungszeitpunkts, sondern daran, *dass*
überhaupt erst nach der Bestätigung eingestiegen wird.

---

## 4. Halten die getroffenen Entscheidungen? (Frage 4)

### 4.1 `USE_TAKE_PROFIT = False` — **hält, und wird besser begründet**

Rendite % / Max Drawdown % / **Calmar**, Limit 8 (wie live):

| Grundlage | Periode | mit Take-Profit | ohne Take-Profit | ohne besser? |
|---|---|---|---|---|
| baseline | gesamt | 1500,53 / −1,90 / **789,75** | 3084,09 / −9,79 / **315,02** | Rendite ja, **Calmar nein** |
| **korrigiert** | gesamt | 28,69 / −11,58 / **2,48** | 338,26 / −22,19 / **15,24** | **Rendite ja, Calmar ja** |
| baseline | out-of-sample | 107,87 / −1,65 / **65,38** | 203,66 / −5,04 / **40,41** | Rendite ja, **Calmar nein** |
| **korrigiert** | out-of-sample | 14,68 / −5,87 / **2,50** | 89,30 / −11,30 / **7,90** | **Rendite ja, Calmar ja** |

Die Entscheidung war auf der Baseline eine **reine Rendite-Entscheidung** —
risikoadjustiert war sie dort sogar schlechter (das hatte bereits PR #23
festgestellt). **Ohne den Look-Ahead ist sie in beiden Massen die bessere
Wahl**, in-sample wie out-of-sample. Sie kippt also nicht; sie wird durch die
Korrektur erst konsistent begründbar.

Der Grund ist einleuchtend: der Take-Profit profitierte am stärksten von Kanal 2
(garantierte Gegenbewegung). Fällt der Look-Ahead weg, fällt sein künstlicher
Vorteil mit.

### 4.2 `MAX_CONCURRENT_POSITIONS = 8` — die Begründung dreht sich um

Calmar-Ratio je Positionslimit, „ohne Take-Profit" (Live-Konfiguration):

| Grundlage | Limit 3 | Limit 5 | **Limit 8 (live)** | unbegrenzt | bestes |
|---|---|---|---|---|---|
| baseline, gesamt | 124,01 | 173,07 | **315,02** | 412,89 | unbegrenzt |
| **korrigiert, gesamt** | **30,88** | 19,59 | **15,24** | 15,53 | **Limit 3** |
| baseline, OOS | 35,88 | 42,86 | **40,41** | 45,42 | unbegrenzt |
| **korrigiert, OOS** | **12,96** | 10,57 | **7,90** | 8,65 | **Limit 3** |

Auf der Baseline wird die Calmar-Ratio mit **mehr** gleichzeitigen Positionen
besser — 8 war dort der bewusst konservative Zwischenschritt in Richtung
„unbegrenzt", genau so ist es in `live_params.py` dokumentiert. Korrigiert dreht
sich die Richtung: **weniger** Positionen sind risikoadjustiert besser, das
Optimum liegt bei 3, und 8 ist die **drittbeste** von vier Optionen.

Die gewählte 8 kippt damit nicht in dem Sinne, dass sie schlecht wäre — aber die
Begründung („konservativer Zwischenschritt in Richtung unbegrenzt") zeigt in die
falsche Richtung. Konservativ wäre unter der korrigierten Grundlage das
**kleinere** Limit.

### 4.3 Die Parameterwahl selbst — hält bei keinem der beiden Bots

Die live gesetzten `DEVIATION_PCT` / `STOP_LOSS_PCT` / `TAKE_PROFIT_FIB` stammen
aus der Rasteroptimierung in `multi_symbol_optimise.py`. `grid.py` rechnet dieses
Raster auf beiden Grundlagen nach — Bewertungsmass, Mindestfilter und Sortierung
wörtlich übernommen.

**`elliott_wave` (36 Kombinationen):**

| Grundlage | Kombinationen, die die Mindestfilter bestehen |
|---|---|
| baseline | **36 von 36** |
| **korrigiert** | **0 von 36** |

Ohne den Look-Ahead erreicht **keine einzige** Parameterkombination die
projekteigene Mindestanforderung `MIN_AVG_RETURN_PCT = 2.0` %. **Die Strategie
wäre nach den eigenen Kriterien des Projekts nie ausgewählt worden.**

**`elliott_wave_stocks` (48 Kombinationen):**

| Grundlage | bestehen die Filter | Rang der Live-Kombination | Sieger |
|---|---|---|---|
| baseline | 48 von 48 | **4** | Zigzag 5 %, Stop 2 %, Fib 0,236 |
| **korrigiert** | 45 von 48 | **16 von 45** | **Zigzag 4 %, Stop 8 %, Fib 0,382** |

Die Live-Kombination fällt von Rang 4 auf Rang 16, und der Sieger wechselt zu
einem **deutlich weiteren Stop** (8 % statt 2–3 %) — plausibel, denn ohne den
künstlich unerreichbaren Stop wird ein enger Stop zum Nachteil.

> **Einordnung, damit die Zahl nicht überinterpretiert wird:** dieser Vergleich
> läuft für beide Grundlagen auf dem **heutigen** Symboluniversum. Die
> historische Entscheidung fiel auf einer anderen Datenbasis — die gespeicherte
> `results/multi_symbol_optimisation_results.csv` von `elliott_wave` deckt nur
> **5 Symbole** ab. Der Rangvergleich zeigt also, wie das Raster **heute** auf
> beiden Grundlagen ausfällt, nicht, was damals herausgekommen wäre.

### 4.4 Weitere betroffene Entscheidungen — benannt, nicht nachgerechnet

Alles, was auf `equity_simulation.py` oder `backtest_elliott.py` beider Bots
aufsetzt, erbt den Bias:

* **Walk-Forward-Validierung** (`multi_symbol_walk_forward.py`, `walk_forward.py`)
  — der Look-Ahead steckt in beiden Hälften, In-Sample wie Out-of-Sample. Ein
  bestandener OOS-Test schliesst ihn deshalb **nicht** aus. Das erklärt, warum
  die Take-Profit-Entscheidung damals „OOS-stabil" wirkte.
* **Der Quartals-Review** (`quarterly_review.py`) vergleicht Agenten-Vorschläge
  gegen dieselbe verzerrte Grundlage.
* **Die Wahl des Aktien-Universums** (Top 100 → Top 150) und der
  `RECENT_YEARS_ONLY`-Konvention.
* **Der Buy-and-Hold-Vergleich** von `elliott_wave_stocks`: Buy-and-Hold ist
  korrekt gerechnet, die Strategie-Seite nicht. Der dokumentierte Vorsprung
  („1458 % gegen 756 %") beruht auf dieser Asymmetrie.
* **Alle Studien der Profitabilitäts-Serie**, soweit sie Elliott-Wave-Kurven
  benutzen — PR #21 hat die beiden Bots deshalb bereits als „nicht auswertbar"
  eingestuft, PR #19/#20 führen die `elliott_wave`-Kurve als eigene Grundlage.

---

## 5. Betrifft es die angezeigte Performance? (Frage 5)

### Die Prämisse muss präzisiert werden: Telegram ist nicht betroffen

`notifications/monitor.py` sagt in seinem eigenen Modul-Kopf:

> *„liest AUSSCHLIESSLICH ihre bereits vorhandenen Live-Datenbanken
> (`paper_trading_<bot>.db`, read-only geöffnet)"*

und weiter, zur Performance-Ausgabe von `/pnl`:

> *„Die schwergewichtige Portfolio-Logik aus `shared/portfolio_overview.py`
> (hypothetische Gewichtung, Korrelationen, Equity-Kurven-Rekonstruktion) ist für
> eine kurze Chat-Ausgabe bewusst NICHT wiederverwendet."*

**Die Telegram-Befehle `/status`, `/positions` und `/pnl` zeigen also echte
Live-Trades und sind vom Look-Ahead nicht berührt.** Dasselbe gilt für die
täglichen `daily_summary_email.py` beider Bots — auch sie lesen die Live-DB.

### Betroffen ist die wöchentliche Portfolio-E-Mail

`shared/weekly_portfolio_email.py` ruft `portfolio_overview.main()` auf. Und
`portfolio_overview.load_all_curves` benutzt `results/<bot>/equity_curve.csv` als
Fallback, solange ein Bot weniger als `MIN_LIVE_CLOSED_TRADES = 10`
geschlossene Live-Trades hat.

**Für beide Elliott-Wave-Bots ist dieser Fallback der Backtest — und der
Backtest enthält den Look-Ahead.** Die dort ausgewiesene Kurve ist damit
erheblich optimistischer als das, was der Live-Bot erreichen kann:

| Bot | Kurve in der Wochen-E-Mail | korrigiert |
|---|---|---|
| `elliott_wave` | +2184,96 % bei −1,83 % Drawdown | **−24,44 % bei −25,58 %** |
| `elliott_wave_stocks` | +1500,53 % bei −1,90 % ¹ | **+28,69 % bei −11,58 %** ¹ |

¹ Die gespeicherte Datei `results/elliott_wave_stocks/equity_curve.csv` enthält
469 ausgeführte Trades — sie stammt aus dem Lauf **mit** Take-Profit, während
`live_params.py` inzwischen `USE_TAKE_PROFIT = False` führt. Die Zeile zeigt
deshalb die Take-Profit-Variante, passend zur tatsächlich gespeicherten Datei.
Das ist die im Sync-Check (PR #24) beschriebene Konfigurations-Divergenz,
unabhängig vom Look-Ahead.

**Zusätzlich, und unabhängig davon:** die `elliott_wave`-Kurve
(`results/equity_curve.csv`) stammt aus dem Initial Commit und deckt nur
**5 Symbole / 144 Trades** ab statt 18 / 782 — festgestellt im Nachtrag zu
PR #19/#20. Die in der Wochen-E-Mail gezeigte Elliott-Wave-Performance ist also
gleich **dreifach** unzuverlässig: veraltet, konfigurationsabweichend und
look-ahead-verzerrt.

**Nur Beobachtung, auftragsgemäss keine Änderung.**

---

## 6. Getroffene Annahmen (vollständig)

**K-A1 — Der korrigierte Einstieg erfolgt zum Schlusskurs des
Bestätigungsbalkens.** Das ist der **früheste ehrliche** Zeitpunkt: der erste
Balken, an dem `calculate_zigzag` den Pivot überhaupt einträgt. Live liegt der
Einstieg beim nächsten Cron-Lauf danach — bei `elliott_wave` stündlich auf
Stundenkerzen, bei `elliott_wave_stocks` täglich auf Tageskerzen, also höchstens
einen Balken später. Die Annahme ist damit **strategiefreundlich**, nicht
konservativ.

**K-A2 — Die Variante `verzoegert` deckt genau diese Latenz ab** (+1 Balken).
Sie ändert die Schlussfolgerung nicht (Krypto −24,44 % → −31,76 %, Aktien
+338,26 % → +332,99 %).

**K-A3 — Das Frische-Fenster von `forward_test.py` wird übernommen**
(48 Stunden bzw. 5 Tage). Liegt die Bestätigung weiter zurück, hätte der
Live-Bot den Trade nie eröffnet. Das entfernt 3 (Krypto) bzw. 22 (Aktien) Trades.

**K-A4 — Ziel und Stop werden aus dem neuen Einstiegspreis berechnet**, exakt
wie in `forward_test.py::find_new_signals`. Sie aus dem Pivot-Preis zu belassen
wäre eine dritte, im Projekt nirgends vorkommende Variante.

**K-A5 — Die Wellenerkennung bleibt unverändert und behält ihren eigenen
Look-Ahead.** `find_impulse_waves` und `remove_overlapping` laufen weiterhin
über die gesamte Historie; eine Welle kann dort zugunsten einer **späteren**
verworfen werden. Diese Untersuchung korrigiert nur den Einstieg. **Die
korrigierten Zahlen sind deshalb weiterhin eine Obergrenze** — die echte
kausale Performance liegt darunter, nicht darüber.

**K-A6 — Die Baseline stammt aus der bot-eigenen `collect_all_trades`, nicht
aus dem Nachbau.** Beide erzeugen denselben Trade-Satz (geprüft, Abweichung 0),
aber eine andere Zeilenreihenfolge bei gleichzeitigen Einstiegen; die
Portfolio-Simulation ist davon abhängig (PR #23). Der Unterschied beträgt bei
`elliott_wave` 0,32 pp auf +2185 % und liegt vollständig innerhalb der dort
gemessenen Reihenfolge-Streubreite.

**K-A7 — Das Rastervergleich läuft auf dem heutigen Symboluniversum**, für beide
Grundlagen gleich. Siehe die Einordnung in Abschnitt 4.3.

---

## 7. Gesamteinschätzung (ohne Handlungsempfehlung)

Der Befund aus PR #21 bestätigt sich und ist gravierender als dort vermutet. Er
betrifft nicht nur die Trailing-Stop-Untersuchung, sondern **jede Zahl, die je
aus dem Elliott-Wave-Backtest stammte** — einschliesslich der Zahlen, mit denen
die Live-Parameter beider Bots ausgewählt wurden.

Drei Punkte scheinen mir für die weitere Bewertung am wichtigsten:

1. **Der Live-Bot ist in Ordnung.** Die Korrektur ist dort seit Langem drin und
   dokumentiert. Es geht nicht um einen Fehler im laufenden Betrieb, sondern um
   die Belastbarkeit der Begründungen.
2. **`elliott_wave` (Krypto) fällt unter die eigenen Mindestanforderungen des
   Projekts** — keine der 36 Rasterkombinationen besteht sie ohne den
   Look-Ahead. Das ist die schwerwiegendste Einzelaussage dieser Untersuchung.
3. **`elliott_wave_stocks` bleibt profitabel**, aber auf einem ganz anderen
   Niveau (Calmar 315 → 15) — und der korrigierte Wert ist wegen K-A5 immer
   noch eine Obergrenze.

Was **nicht** gezeigt wurde: dass die Strategie-Idee falsch ist. Gezeigt wurde,
dass die vorliegenden Zahlen sie nicht stützen können.

### Vorschläge für Folgeaufgaben (hier ausdrücklich nicht umgesetzt)

1. **Den Backtest an `forward_test.py` angleichen** — Einstieg zum
   Bestätigungskurs. Das ist eine Änderung an `equity_simulation.py` /
   `backtest_elliott.py` und damit ausserhalb dieser Aufgabe.
2. **Den zweiten Look-Ahead schliessen** (K-A5): Wellenerkennung rollierend
   statt über die Gesamthistorie. Erst danach wäre eine belastbare Neubewertung
   der Strategie möglich.
3. **Danach** die Parameter neu bestimmen und entscheiden, ob `elliott_wave`
   (Krypto) überhaupt weiterlaufen soll.
4. **Die `equity_curve.csv`-Fallbacks in der Wochen-E-Mail einordnen** —
   entweder neu erzeugen oder als „Backtest, nicht Live" kennzeichnen.

---

## 8. Dateien

| Datei | Rolle |
|---|---|
| `zigzag_confirm.py` | Zigzag wie im Bot, zusätzlich mit Bestätigungszeitpunkt je Pivot |
| `run_one_bot.py` | drei Varianten je Bot + Mechanismus-Diagnose |
| `verify_baseline.py` | Regressionscheck: Pivots, Trades und veröffentlichte Kennzahlen (13/13 je Bot) |
| `grid.py` | Rasteroptimierung auf beiden Grundlagen |
| `decisions.py` | 2×4-Matrix Take-Profit × Positionslimit, beide Grundlagen, IS/OOS |
| `test_lookahead.py` | 21 Sanity-Checks auf konstruierten Kursreihen |
| `run_all.py` | alles in der richtigen Reihenfolge, bricht bei jedem Fehlschlag ab |
| `results/*.json`, `results/*_trades_*.csv` | vollständige Ergebnisse und Trade-Sätze |


---

# Nachtrag K: die Korrektur im Bot-Code

## K0. Entscheidungsgrundlage

### Was gemacht wurde

Beide in dieser Untersuchung beschriebenen Look-Ahead-Kanäle sind jetzt im
**echten Backtest-Code** behoben — nicht mehr nur als Research-Kopie in diesem
Verzeichnis:

| Kanal | Behoben durch | Datei |
|---|---|---|
| **1** Einstieg zum Pivot-Preis | Einstieg zum **Schlusskurs des Bestätigungsbalkens**, Ziel und Stop daraus neu berechnet, Frische-Fenster wie live | `backtest_elliott.py` |
| **2** rückblickende Wellenauswahl | **`find_causal_waves`** — bildet die Läufe von `forward_test.py` nach | `elliott_wave_counter.py` |

Dazu: `calculate_zigzag_with_confirmation` in `zigzag_indicator.py` (liefert je
Pivot den Bestätigungszeitpunkt), und die beiden Aufrufstellen
`multi_symbol_optimise.get_trades_for_symbol` und `optimise_elliott.py` wurden
auf die kausale Kette umgestellt. Beide Bots, symmetrisch.

**`forward_test.py` und `live_params.py` sind unverändert** — nachgewiesen per
`git diff` (leer). Der Live-Bot war nie betroffen; er machte es von Anfang an
richtig.

**Keine Parametersuche, keine Aktivierungsempfehlung.** Was die neuen Zahlen für
die aktuell gesetzten Parameter bedeuten, ist eine separate Entscheidung.

### Wie Kanal 2 behoben wurde — und warum so

Das Problem sitzt in `remove_overlapping`:

```python
if row["fib_score"] > kept_row["fib_score"]:
    kept[i] = row          # eine SPAETERE Welle verdraengt eine fruehere
```

Live ist das unmöglich: der Bot hätte die frühere Welle längst gehandelt, als
die spätere noch gar nicht existierte.

`find_causal_waves` erfindet **keine neue Auswahlregel**. Es bildet nach, was
`forward_test.py::find_new_signals` tatsächlich tut, Lauf für Lauf:

1. Bekannt sind nur Wellen, deren Welle-5-Pivot **bestätigt** ist.
2. Auf genau diese wird die **unveränderte** `remove_overlapping` angewendet.
3. Was übrig bleibt, frisch genug und noch nicht gehandelt ist, wird gehandelt.
   **Einmal gehandelt heisst endgültig gehandelt** — wie
   `UNIQUE(symbol, signal_time)` in der Live-Datenbank.

Ausgewertet wird nur an den Balken, an denen eine **neue** Welle bestätigt wird.
Dazwischen ändert sich die bekannte Menge nicht, `remove_overlapping` liefert
dasselbe, und das Frische-Fenster kann nur ablaufen — also nie einen
zusätzlichen Trade erzeugen. Das ist exakt äquivalent zu einer Auswertung an
jedem einzelnen Balken, nur ohne die leeren Durchläufe.

`find_impulse_waves` und `remove_overlapping` selbst bleiben **unverändert** —
`forward_test.py` benutzt sie.

### Der Kausalitäts-Nachweis — jeder Trade, nicht stichprobenartig

`verify_causality.py` prüft **alle 1301 Trades** beider Bots. Entscheidend: die
Gegenrechnung läuft auf einem **echt abgeschnittenen** Kurs-DataFrame
(`price_df.iloc[:entry_idx + 1]`), nicht auf der vollen Historie mit
nachträglichem Filter. Was dort nicht sichtbar ist, kann auch nicht
versehentlich einfliessen.

| Prüfung | `elliott_wave` (791) | `elliott_wave_stocks` (510) |
|---|---|---|
| P1 Zigzag ist präfix-stabil | 0 Verletzungen | 0 Verletzungen |
| P2 Welle war zum Einstieg bereits ausgewählt | **0** | **0** |
| P3 Einstiegskurs = Schlusskurs des Einstiegsbalkens | 0 | 0 |
| P4 Frische-Fenster eingehalten | 0 | 0 |
| P5a Ausstieg nach Einstieg | 0 | 0 |
| P5b jedes Wellenende höchstens einmal gehandelt | 0 | 0 |

**P2 ist die eigentliche Prüfung:** die gehandelte Welle muss in der Auswahl
sein, die man zum Einstiegszeitpunkt allein aus den abgeschnittenen Daten
getroffen hätte. Eine später auftauchende, besser bewertete Welle kann sie also
nicht mehr verdrängt haben.

**P1 ist die Voraussetzung dafür:** nur weil der Zigzag präfix-stabil ist
(abgeschnittene Daten liefern dieselben Pivots wie die vollen, eingeschränkt auf
die bis dahin bestätigten), bedeutet `confirm_idx <= T` überhaupt „war zu T
bekannt". Auf echten Daten an jedem einzelnen Einstiegsbalken geprüft.

### Regressionschecks

* `verify_baseline.py` **14/14 je Bot** — Zigzag-Pivots identisch zur
  unveränderten `calculate_zigzag`; die neue Bot-Fassung
  `calculate_zigzag_with_confirmation` deckungsgleich mit der Kopie hier; der
  Trade-Nachbau Trade für Trade identisch zum eingefrorenen Bot-Stand.
* `decisions.py` **10/10** veröffentlichte Matrix-Zellen exakt
  (1500,53 / −1,90 / 469 und 3084,09 / −9,79 / 288 und die
  Unbegrenzt-Zeilen) — gerechnet auf den eingefrorenen Original-Trade-Sätzen.
* `test_lookahead.py` **35** Sanity-Checks, davon 13 neu für die kausale
  Wellenerkennung.

### Was diese Korrektur NICHT leistet

* **Keine Parameter-Neubestimmung.** Die Zahlen unten gelten für die aktuell
  in `live_params.py` gesetzten Werte. Ob diese Werte auf sauberer Grundlage
  noch die richtigen sind, ist offen — Abschnitt 4.3 dieses Berichts legt nahe,
  dass sie es nicht sind.
* **Keine Entscheidung über den Weiterbetrieb** der beiden Bots.
* **Keine Neuerzeugung der `equity_curve.csv`.** Die Wochenbericht-Kennzeichnung
  läuft separat (PR #27).
* **Das rollierende Datenfenster von `forward_test.py`** (90 Tage Krypto,
  3 Jahre Aktien) wird nicht nachgebildet — der Backtest rechnet weiter auf der
  vollen Historie. Siehe Annahme K-A3.

### Reproduktion

```
cd research/elliott_wave_lookahead
python3 run_all.py                          # alles, ca. 4 Minuten
python3 verify_causality.py elliott_wave    # nur der Kausalitaets-Nachweis
python3 compare_channels.py elliott_wave    # nur der Stufenvergleich
```

---

## K1. Was die zweite Korrektur bewirkt

Rendite % / Max Drawdown % / **Calmar**:

### `elliott_wave`

| Stufe | Trades | ausgeführt | Rendite | Max DD | **Calmar** | Gewinnrate |
|---|---|---|---|---|---|---|
| baseline (kein Kanal korrigiert) | 783 | 782 | +2184,96 % | −1,83 % | **1193,97** | 82,9 % |
| nur Kanal 1 (Einstiegskurs) | 780 | 780 | −24,44 % | −25,58 % | **−0,96** | 27,7 % |
| **beide Kanäle (Bot-Stand heute)** | 791 | 791 | **−25,73 %** | **−26,84 %** | **−0,96** | 27,4 % |

### `elliott_wave_stocks`

| Stufe | Trades | ausgeführt | Rendite | Max DD | **Calmar** | Gewinnrate |
|---|---|---|---|---|---|---|
| baseline (kein Kanal korrigiert) | 519 | 288 | +3084,09 % | −9,79 % | **315,02** | 43,9 % |
| nur Kanal 1 (Einstiegskurs) | 497 | 392 | +338,26 % | −22,19 % | **15,24** | 21,7 % |
| **beide Kanäle (Bot-Stand heute)** | 510 | 395 | **+352,72 %** | **−22,44 %** | **15,72** | 21,4 % |

## K2. Die Erwartung aus Annahme K-A5 hält nur zur Hälfte — Korrektur

Abschnitt 6 dieses Berichts (Annahme K-A5) sagt, die Kanal-1-Zahlen seien eine
**Obergrenze**: mit der zweiten Korrektur sollten sie niedriger ausfallen.

| Bot | Wirkung von Kanal 2 | Erwartung |
|---|---|---|
| `elliott_wave` | Rendite **−1,29 pp**, Drawdown −1,26 pp | **bestätigt** |
| `elliott_wave_stocks` | Rendite **+14,46 pp**, Calmar +0,48 | **nicht bestätigt** |

**Diese Erwartung war zu pauschal formuliert und wird hiermit korrigiert.**

Der Grund ist strukturell: die kausale Auswahl streicht **keine** Welle mehr
rückwirkend — es kommen also *mehr* Trades zustande (+11 bzw. +13). Ob das hilft
oder schadet, ist durch die Art des Bias nicht festgelegt. Rückblickend wurde
nach dem **Fibonacci-Score** ausgewählt, und der ist ein **Formmass, kein
Gewinnmass**. Die „im Rückblick bessere" Welle war nicht systematisch die
profitablere.

Was bleibt: die Kanal-1-Zahlen waren **nicht belastbar als exakte Werte** —
das gilt weiterhin. Nur die behauptete *Richtung* der Abweichung war nicht
begründet.

Am Gesamtbild ändert das nichts: `elliott_wave` verliert Geld
(Calmar −0,96), `elliott_wave_stocks` bleibt profitabel, aber mit einer
Calmar-Ratio von 15,7 statt der berichteten 315.

## K3. Getroffene Annahmen der Korrektur

**K-K1 — Der Einstieg erfolgt zum Schlusskurs des Bestätigungsbalkens**, dem
frühesten ehrlichen Zeitpunkt. Live liegt er beim nächsten Cron-Lauf danach
(stündlich auf Stundenkerzen, täglich auf Tageskerzen), also höchstens einen
Balken später. Die Annahme ist **strategiefreundlich**; die Variante
`verzoegert` in `run_one_bot.py` zeigt die Latenz-Empfindlichkeit.

**K-K2 — `SIGNAL_FRESHNESS_BARS` spiegelt `forward_test.py`** (48 bzw. 5) und
liegt bewusst in `backtest_elliott.py`, mit Verweis auf die Quelle. Eine
Änderung dort muss hier nachgezogen werden — der Kommentar sagt das.

**K-K3 — Das rollierende Datenfenster wird nicht nachgebildet.** `forward_test.py`
lädt nur die letzten 90 Tage (Krypto) bzw. 3 Jahre (Aktien); der Backtest rechnet
auf der vollen Historie. Das betrifft die Anlaufphase des Zigzag, nicht die
Kausalität: alles, was der Backtest benutzt, liegt vor dem Einstieg. Eine
Nachbildung würde die Ergebnisse von einem willkürlichen Fensterrand abhängig
machen.

**K-K4 — `run_backtest` verlangt jetzt die Spalte `entry_idx`** und bricht sonst
mit einer erklärenden Fehlermeldung ab, statt still auf den Pivot-Einstieg
zurückzufallen. Ein stiller Rückfall wäre genau der behobene Fehler.

**K-K5 — Die Baseline in `run_one_bot.py` und `decisions.py` kommt aus
eingefrorenen Dateien** (`results/frozen_pr26/`), nicht aus dem Nachbau. Nicht
nur der Trade-Satz zählt, sondern die **Zeilenreihenfolge**: bei Limit 8
verschiebt sie die Rendite um über 100 Prozentpunkte (siehe
`research/order_sensitivity`). Für einen Regressionscheck gegen die
veröffentlichten Zellen taugt nur die Originaldatei.

## K4. Geänderte Dateien

**Bot-Code** (je zweimal, beide Bots symmetrisch):

| Datei | Änderung |
|---|---|
| `zigzag_indicator.py` | **neu:** `calculate_zigzag_with_confirmation`. `calculate_zigzag` unverändert (forward_test.py benutzt sie) |
| `elliott_wave_counter.py` | **neu:** `find_causal_waves`. `find_impulse_waves` / `remove_overlapping` unverändert |
| `backtest_elliott.py` | Einstieg zum Bestätigungskurs, `SIGNAL_FRESHNESS_BARS`, `signal_time` im Trade, Schutz gegen fehlendes `entry_idx` |
| `multi_symbol_optimise.py` | `get_trades_for_symbol` nutzt die kausale Kette |
| `optimise_elliott.py` | dieselbe Umstellung |

**Unverändert:** `forward_test.py`, `live_params.py`, `equity_simulation.py`
(erbt die Korrektur über `get_trades_for_symbol`), alle
`experiment_*.py`, `walk_forward.py`, `quarterly_review.py` — sie hängen an
`collect_all_trades` und bekommen die Korrektur automatisch.

**Research** (dieses Verzeichnis):

| Datei | Rolle |
|---|---|
| `verify_causality.py` | **neu** — prüft jeden Trade auf Kausalität |
| `compare_channels.py` | **neu** — Stufenvergleich baseline / Kanal 1 / beide |
| `results/frozen_pr26/` | **neu** — die Trade-Sätze des unkorrigierten Bot-Stands |
| `test_lookahead.py` | 35 statt 21 Checks (Abschnitt 5 neu) |
| `verify_baseline.py`, `run_one_bot.py`, `decisions.py` | Baseline aus den eingefrorenen Dateien |
