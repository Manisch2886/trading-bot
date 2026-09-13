# TB-24 — Haltedauern und Zeithorizonte: Übergabe

**Datum: 2026-09-13.** Branch `claude/new-session-hcetas`, Base `main`
(Stand `0f39e3b`, nach PR #92/#93). Vollständiger Bericht:
`research/tb24_haltedauern/BERICHT.md`. Kurzfassung zum Kopieren:
`docs/ERGEBNIS_TB24_haltedauern.md`.

**Untersuchung, keine Änderung.** `git diff origin/main HEAD --name-only`
listet ausschliesslich Dateien unter `research/tb24_haltedauern/` und `docs/`.
Kein Produktivcode, keine `live_params.py`, kein `forward_test.py`, kein
`equity_simulation.py`, kein `multi_symbol_optimise.py`, nichts unter
`broker/`, keine Crontab, keine launchd-Vorlage. **Keine Empfehlung ist
umgesetzt.**

---

## 1. Die Antwort auf die Vermutung

> **Bespielen sechs der neun dasselbe Fenster — ja oder nein, und mit welchen
> Zahlen?**

**Ja. Genau sechs, und in einem engeren Band als vermutet.**

Die Vermutung lautete: *„Sechs der neun haben Median-Haltedauern zwischen drei
und zehn Tagen und bespielen ein Fenster."* Gemessen über **17.795 ausgeführte
Positionen** aus den Original-Bot-Funktionen, Haltedauer in Kalendertagen:

| Bot | Median | | Bot | Median |
|---|---:|---|---|---:|
| `elliott_wave` | **3,90** | | `t3_supertrend` | 2,67 |
| `rsi2_crypto` | **4,00** | | `turtle_soup_stocks` | 14,00 |
| `turtle_soup_crypto` | **4,00** | | `volatility_breakout` | 21,00 |
| `rsi2_mean_reversion` | **5,00** | | | |
| `volatility_breakout_crypto` | **6,00** | | | |
| `elliott_wave_stocks` | **7,00** | | | |

Die sechs fett gesetzten liegen zwischen **3,90 und 7,00 Kalendertagen** — die
Vermutung nannte 3 bis 10, gemessen ist ein Band von 3,1 Tagen Breite.

**Zwei Zahlen, die den Befund verschärfen:**

* `t3_supertrend` liegt mit **2,67 Tagen** knapp unter der Grenze. Zieht man
  die Klassengrenze bei 2 statt bei 3 Tagen, sind es **sieben von neun** in
  einem Fenster, und zwischen dem kürzesten und dem siebten Median liegen
  **4,3 Tage**.
* **Die Mediane aller neun liegen zwischen 2,67 und 21,0 Tagen.** Über 30 Tage
  ist das Portfolio **leer**. Es ist derselbe Befund wie bei der
  Korrelationsmessung: eine Streuung, die niemand gemessen hatte, und die es
  nicht gibt.

Der Befund ist **nicht** eine Folge des Kapitalmanagements: rechnet man
denselben Median über **alle** gefundenen Trades statt nur über die
ausgeführten (also einschliesslich der 8.066, die `MAX_CONCURRENT_POSITIONS`
oder fehlendes freies Kapital übersprungen haben), ändert er sich bei acht von
neun Bots um **0,00 Tage** und bei `t3_supertrend` um 0,25. Auch bei
`volatility_breakout`, wo zwei Drittel aller Signale übersprungen werden.

---

## 2. Der Befund, der über die Frage hinausgeht

Die Aufgabenstellung fragte, ob der Horizont eine zweite
Diversifikationsdimension ist, und gab die Einordnung mit: *„Horizont-Streuung
ohne Quellen-Streuung schützt nicht."* **Das ist hier nicht Vorsicht, sondern
Messung. Der Horizont trennt nichts; die Ertragsquelle trennt alles.**

Gemessen wurde, wie oft zwei Bots im selben Titel innerhalb von drei Tagen eine
Position eröffnen — **und wie oft das bei zufälliger Lage passieren würde**
(Einstiegstage des zweiten Bots je Symbol zufällig neu gelegt, 200 Ziehungen,
feste Saat; zusätzlich in geschlossener Form nachgerechnet, beide Werte
stimmen in allen 32 Paaren auf 0,1 Prozentpunkte überein). Der Quotient
`Überschuss` ist die Zahl: 1,0 heisst „nicht mehr als Zufall".

| | Paare | Median-Überschuss | Spanne |
|---|---:|---:|---|
| **gleiche Ertragsquelle** | 6 | **1,94 ×** | 1,68 – 3,27 |
| verschiedene Ertragsquelle | 26 | 0,32 × | 0,00 – 2,19 |
| **gleiche Horizont-Klasse** | 16 | **0,32 ×** | 0,00 – 2,19 |
| verschiedene Horizont-Klasse | 16 | 1,10 × | 0,00 – 3,27 |

Aufgeschlüsselt nach Quellen-Paar:

| Quellen-Paar | Paare | Median-Überschuss | Spanne |
|---|---:|---:|---|
| Umkehr + Umkehr | 4 | **2,58 ×** | 1,89 – 3,27 |
| Trend + Trend | 2 | **1,71 ×** | 1,68 – 1,74 |
| Muster + Umkehr | 8 | 1,43 × | 0,00 – 2,19 |
| **Trend + Umkehr** | 12 | **0,32 ×** | 0,15 – 0,93 |
| **Muster + Trend** | 6 | **0,18 ×** | 0,00 – 1,78 |

**Alle sechs Paare gleicher Quelle liegen über 1,68 ×. Alle zwölf
Trend-Umkehr-Paare liegen unter 0,95 ×.** Das stärkste Paar ist
`rsi2_mean_reversion` / `turtle_soup_stocks` mit **3,27 ×** und **1.523
gemeinsamen Einstiegsereignissen**; das schwächste ist
`volatility_breakout` / `rsi2_mean_reversion` mit **0,15 ×** — und diese beiden
liegen in **verschiedenen** Horizont-Klassen (21 gegen 5 Tage). Ein
Bollinger-Ausbruch und ein RSI-2-Signal entstehen in verschiedenen
Marktzuständen; **das** ist die echte Streuung im Portfolio, und sie kommt
nicht vom Horizont.

**Für die Entscheidungslage heisst das:** das gedrängte Fenster ist ein realer
Befund, aber es ist **nicht** die Stelle, an der das Portfolio Risiko
konzentriert. Es ist quellenseitig sogar gemischt (drei Umkehr-, zwei Muster-,
ein Trend-Bot). Wer nach dem Ergebnis dieser Untersuchung etwas ergänzen will,
ergänzt sinnvoller eine **Quelle** als einen **Horizont** — das ist die
Einordnung aus der Aufgabenstellung („zweite Dimension, nicht erste"), jetzt
mit Zahlen.

---

## 3. Warum das Fenster so besetzt ist: es ist eingestellt, nicht gewachsen

Acht der neun Bots haben eine **zweigipflige** Haltedauer-Verteilung, und die
Trennlinie ist die Ausstiegsart (geprüft ohne Verteilungsannahme: überschneiden
sich die Quartilsbereiche der beiden häufigsten Arten? Bei acht von neun:
nein). Der spätere Gipfel liegt bei jedem Bot mit Zeitbremse **exakt auf dieser
Bremse**:

| Bot | Zeitbremse | ergibt | gemessener Median der Zeitausstiege | Anteil Zeitausstiege |
|---|---|---:|---:|---:|
| `elliott_wave` | 240 Stundenbalken | 10 T | **10,00** | 33,8 % |
| `rsi2_crypto` | `MAX_HOLD_DAYS = 10` | 10 T | **10,00** | 2,0 % |
| `turtle_soup_crypto` | `= 10` | 10 T | **10,00** | 31,0 % |
| `volatility_breakout_crypto` | `= 15` | 15 T | **15,00** | 29,0 % |
| `rsi2_mean_reversion` | `= 10` Handelstage | ~14 T | **14,00** | 3,2 % |
| `turtle_soup_stocks` | `= 10` Handelstage | ~14 T | **14,00** | **100,0 %** |
| `volatility_breakout` | `= 15` Handelstage | ~21 T | **22,00** | 80,2 % |
| `elliott_wave_stocks` | 90 Tagesbalken | ~130 T | **131,00** | 20,8 % |
| `t3_supertrend` | keine | — | — | 0 % |

Der **Median eines Bots** ist damit im Wesentlichen die Antwort auf eine
einzige Frage: *wie oft feuert der Stop, bevor die Uhr abläuft?*
`turtle_soup_stocks` hat als einziger Bot gar keinen Stop
(`STOP_MODE = None`, so validiert), also endet **jeder** seiner 8.915 Trades im
Zeitausstieg — sein „Horizont" ist genau eine Zahl aus `live_params.py` und
sonst nichts. `elliott_wave` dagegen wird in 53,8 % der Fälle vom Stop
gestoppt, Median 0,88 Tage, und landet insgesamt bei 3,90.

**Sieben von neun Bots haben eine Zeitbremse von 10 bis 15 Tagen bzw.
Handelstagen.** Jede ist einzeln validiert, keine wurde je gegen die anderen
sechs gesetzt.

---

## 4. Der auffälligste Einzelfall

`elliott_wave_stocks` und `rsi2_mean_reversion` steigen in **0 von 395** Fällen
innerhalb von drei Tagen gemeinsam ein, obwohl sie **127 Titel teilen** und der
Zufall etwa 20 Treffer erwarten liesse. Das ist kein Messfehler, sondern ein
**systematischer Versatz**: der nächstgelegene RSI-2-Einstieg liegt im Median
**14 Tage vor** dem Elliott-Einstieg, und die Klassen von −3 bis +3 Tagen sind
**leer** (von 395 Fällen: 213 unter −30 Tagen, 21 / 36 / 15 in den Klassen bis
−3, dann **0 / 0**, dann 1 / 3 / 7 und 99 über +30).

Die beiden handeln denselben Kursrückgang — nur nacheinander. **Ein
Drei-Tage-Fenster allein hätte das Paar als unabhängig eingeordnet.** Das ist
die „Scheinstreuung, die eine reine Positionsüberlappung nicht zeigt" aus der
Aufgabenstellung, in ihrer zweiten Gestalt: nicht gleichzeitig mit leichtem
Versatz, sondern sequenziell mit festem Versatz. Deshalb wurde die
Versatz-**Verteilung** zusätzlich gemessen und nicht nur der Anteil im Fenster.

Eine naheliegende Erklärung liefern die Einstiegsregeln: RSI-2 kauft das Tief
selbst, während ein Zigzag-Pivot erst dann ein Pivot ist, wenn der Kurs sich um
`DEVIATION_PCT = 5 %` zurückbewegt hat. Diese Erklärung ist **plausibel, aber
nicht gemessen** — gemessen ist der Versatz, nicht seine Ursache.

---

## 5. Die Überlappungsmatrix, kurz

Vollständig (72 geordnete Paare) in
`research/tb24_haltedauern/ergebnisse/ueberlappungsmatrix.csv`, Matrizen im
Bericht Abschnitt 2.5. Beide Zahlen sind aus Sicht von A gerechnet, im
**gemeinsamen Fenster** beider Bots (die Historien starten zwischen 2016 und
2022) und **nicht symmetrisch**.

**Tages-Überlappung:** Median über alle 72 Paare **89,5 %**; die Spalte
`turtle_soup_stocks` steht durchgehend auf 100 %, weil dieser Bot an **allen
3.653 Tagen** eine Position hält. Diese Zahl misst vor allem, wie oft ein Bot
im Markt ist — sie gehört als Nenner in den Bericht, nicht als Befund. (Im
gemeinsamen Fenster aller neun Bots, 2022-03-17 bis 2026-08-20, sind im Median
**6 von 9** Bots gleichzeitig im Markt, nie weniger als 3.)

**Titel-Überlappung** — die aussagekräftigere Zahl. Stärkste Paare:

| A → B | Anteil der (Titel, Tag)-Paare von A |
|---|---:|
| `rsi2_mean_reversion` → `turtle_soup_stocks` | **48,6 %** |
| `rsi2_crypto` → `turtle_soup_crypto` | 39,3 % |
| `elliott_wave` → `turtle_soup_crypto` | 25,5 % |
| `elliott_wave_stocks` → `turtle_soup_stocks` | 24,9 % |
| `volatility_breakout_crypto` → `t3_supertrend` | 21,7 % |

Median innerhalb der Anlageklasse 3,7 %, Mittel 10,1 %. Nach Quelle sortiert:
gleiche Quelle **17,3 %**, verschiedene Quelle **3,2 %**. Nach
Horizont-Klasse sortiert kommt das Gegenteil heraus (gleicher Horizont 3,4 %,
verschiedener 6,7 %).

Das schliesst an die bekannte Exposure-Messung an: dort war das stärkste Paar
`rsi2_mean_reversion` / `turtle_soup_stocks` mit bis zu 19 gleichen Titeln an
79,4 % der Tage. **Nach Zeitdimension aufgelöst** ist es dasselbe Paar, jetzt
mit der Zusatzangabe, dass es auch **gemeinsam einsteigt** (3,27 × Zufall) und
dass die Ursache die geteilte Ertragsquelle ist, nicht der geteilte Horizont
(die Mediane sind 5 gegen 14 Tage, also verschiedene Klassen).

---

## 6. Die Datenquelle — Entscheidung und Begründung

Die Aufgabenstellung liess die Wahl offen und vermutete „wahrscheinlich beides".
**Gemessen wurde die Backtest-Seite; die Live-Seite ist nicht gemessen, sondern
vorbereitet.** Die Begründung in zwei Teilen:

1. **Was zur Verfügung steht.** Die neun `paper_trading_<bot>.db` sind laut
   `.gitignore` nicht im Repo und liegen nur auf dem Rechner des Nutzers; in
   einer Cloud-Sitzung sind sie **nicht vorhanden**. Nachgesehen wurde, nicht
   angenommen: `live_haltedauern.py` meldet „keine Datenbank gefunden" für 9
   von 9 Bots.
2. **Was sie tragen würden.** Selbst auf dem Rechner des Nutzers trägt die
   Live-Seite diese Frage nicht: laut Protokoll 4.3b erreicht **kein** Bot
   `MIN_LIVE_CLOSED_TRADES = 10`. Ein Median je Bot wäre eine Zahl aus zwei bis
   vier Werten, und eine Überlappungsmatrix hätte pro Paar meist null
   gemeinsame Positionstage.

**`research/tb24_haltedauern/live_haltedauern.py` ist deshalb auf dem Rechner
des Nutzers ohne Vorbereitung lauffähig.** Es liest jede Datenbank über
`file:…?mode=ro` (dieselbe Betriebsart wie `notifications/monitor.py` und
`broker/bot_db.py`), unterscheidet „nicht nachgesehen" von „nachgesehen, nichts
da", weist manuelle Ausstiege (`result = 'manual_close'`) **getrennt** aus —
ihre Haltedauer ist eine Entscheidung des Nutzers, keine Eigenschaft der
Strategie — und schreibt den Vorbehalt zur Trade-Anzahl in seine eigene
Ausgabe.

Dass eine Meldung „keine Datenbank gefunden" nichts über die Richtigkeit des
Lesewegs beweist, ist Prinzip 12. Abschnitt 14 der Selbsttests baut deshalb
eine Datenbank mit dem echten Schema, füllt sie mit von Hand nachrechenbaren
Trades und prüft: Median 6,5 Tage aus 3 und 10 Tagen, der offene Trade wird
nicht gelesen, der manuelle nicht gemittelt, und `mode=ro` weist einen
Schreibversuch ab.

---

## 7. Wie die Zahlen entstanden sind

* **Die Bot-Funktionen werden aufgerufen, nicht nachgebaut.**
  `positionen_holen.py` lädt je Bot dessen `equity_simulation.py` in einem
  **eigenen Prozess** (neun gleichnamige Module kollidieren in `sys.modules`)
  und ruft `load_all_symbol_data` und `collect_all_trades` mit genau den
  Argumenten auf, die der `__main__`-Block des jeweiligen Bots verwendet.
  Vorbild: `shared/portfolio_overview.py`.
* **Die bot-spezifische Argumentzuordnung steht nicht zweimal da.** Sie kommt
  per Import aus `research/exposure_messung/bot_lauf.py` — inklusive des
  BTC-Regimefilters, den `volatility_breakout_crypto` bewusst erst danach
  anwendet (im Lauf gemeldet: 126 von 359 Trades entfernt). Eine zweite Kopie
  wäre genau die Doppelführung aus Prinzip 11. Mitimportiert werden auch die
  Stubs für `binance`, `yfinance` und `fetch_binance_data`.
* **Neu gegenüber der Exposure-Messung** sind drei Spalten: die Ausstiegsart
  `result` aus den Trade-Tabellen der Backtests (sie überlebt
  `collect_all_trades`, weil das die Spalten unverändert durchreicht), die
  **aus der Kursreihe gezählte** Kerzenzahl, und die Ein-/Ausstiegskurse.
* **Die Zuordnung „welcher Trade wurde ausgeführt" ist exakt.** Übernommen aus
  `bot_lauf.py`: `simulate_portfolio()` gibt seine offenen Positionen nicht
  heraus, wird deshalb zweimal mit demselben Trade-Satz aufgerufen — einmal
  unverändert, einmal mit Zeilenkennung in der `symbol`-Spalte (`AAPL#417`),
  die dort reine Beschriftung ist. Dass das die Simulation nicht verändert,
  wird geprüft.
* **Kalendertage, nicht Handelstage**, und die Kerzenzahl daneben: die neun
  Bots laufen auf drei Zeitrahmen (1h, 4h, 1d). Bei `turtle_soup_stocks` sind
  11 Kerzen 14 Kalendertage (Wochenenden), bei `elliott_wave` sind 94,5 Kerzen
  3,9 Tage. Nur die Kalenderangabe ist vergleichbar; nur die Kerzenzahl sagt,
  wie viele Entscheidungen der Bot getroffen hat.
* **Eine Position gilt vom Einstiegs- bis zum Ausstiegstag als offen**, beide
  eingeschlossen — dieselbe Festlegung wie in
  `research/exposure_messung/exposure_kern.py`.
* **`shared/kursdaten.py`** hat wie vorgesehen gegriffen: 1 unvollständige
  Kerze gestrichen und gemeldet (`APH`, der bekannte Fall aus Protokoll 3.3).

### Pflicht-Gegencheck

Für **alle neun** Bots stimmt der hier erzeugte Positionssatz Zeile für Zeile
mit `research/exposure_messung/daten/<bot>_positionen.csv` überein (Symbol,
Ein- und Ausstiegszeit, PnL, Allokation) — gemeldet als
`"abgleich_exposure_messung": {"identisch": true}` in jeder der neun
`daten/<bot>_meta.json`. Die ausgeführten Trade-Zahlen (130 / 656 / 392 /
1.414 / 207 / 395 / 4.232 / 8.915 / 1.454) sind genau die, die
`research/exposure_messung/BERICHT.md` veröffentlicht hat. Das ist zugleich der
Beleg, dass die neuere pandas-Fassung dieser Umgebung nichts verschoben hat.

### Selbsttests: 51 von 51

`python3 research/tb24_haltedauern/test_haltedauer_kern.py`

| Abschnitt | Inhalt | Prüfungen |
|---|---|---:|
| 1–11 | Gegenproben auf dem echten Rechenkern | 35 |
| 14 | Live-Weg gegen eine **gebaute** Datenbank | 5 |
| 12 | **Mutationsproben** | 10 |
| 13 | Wache: keine Änderung ausserhalb `research/tb24_haltedauern/` und `docs/` | 1 |
| | **gesamt** | **51** |

Zu den Gegenproben: zur getrennten Verteilung die überlappende; zum Treffer bei
genau 3 Tagen Abstand der Nicht-Treffer bei 4; zur Überlappung im selben Titel
dieselben Tage in einem **anderen** Titel (100 % Tage, 0 % Titel); zur Richtung
der Überlappung die Gegenrichtung (40 % gegen 100 % beim gleichen Paar); zum
positiven Versatz der negative. Kein Erwartungswert ist aus einem Lauf des
Kerns übernommen und wiedererkannt.

Zu den Mutationsproben: der **Quelltext** des Rechenkerns wird an genau einer
Stelle textlich verfälscht, das veränderte Modul frisch geladen und dieselbe
Prüfreihe darauf angewandt — sie muss dann fehlschlagen. Jede Ersetzung wird
vorher darauf geprüft, dass sie **genau einmal** zutrifft; eine Mutation, die
nichts verändert, würde sonst als bestandene Probe durchgehen. Verfälscht
wurden: Haltedauer in Stunden statt Tagen · Ausstiegstag nicht mehr als
Positionstag gezählt · Nähe-Fenster um einen Tag zu eng · Vorzeichen des
Versatzes gedreht · Histogramm-Klassen rechts statt links geschlossen ·
Zweigipfligkeit immer bejaht · Grenze der Horizont-Klasse verschoben ·
Überlappung auf B statt A bezogen · Titel-Überlappung mit Tagen statt Titeln ·
getrennte Zeiträume als überlappend. **Alle zehn wurden erkannt**, von 1 bis 5
Prüfungen je Mutation.

---

## 8. Belastbarkeit und Grenzen

### Der Vorbehalt zur Grundlage

**Die Backtest-Trades entstehen aus Parametern, die nach einem Mass gewählt
wurden, das sich als unbrauchbar erwiesen hat.** Für Haltedauern macht das
wenig aus — und der Grund ist nicht Zuversicht, sondern Abschnitt 3: die
Haltedauern hängen an den Ausstiegsregeln, und die oberen Gipfel liegen auf den
Zeitbremsen. Eine andere Parameterwahl würde die **Stop-Quote** verschieben und
den Median zwischen den beiden Gipfeln wandern lassen, die Gipfel selbst aber
nicht.

Konkret ist die Vermutung damit gegen die Parameterwahl **nicht beliebig
robust**: wäre `turtle_soup_stocks` mit einem Stop konfiguriert (getestet,
verworfen), fiele sein Median von 14 in Richtung des gedrängten Fensters — die
Vermutung träfe dann *stärker* zu, nicht schwächer.

Gerechnet wurde mit den heutigen `live_params.py` über die heutigen
Bot-Funktionen, also auf **kausal sauberer** Grundlage (Look-Ahead-Korrektur,
Protokoll 3.1). Die Zahlen sind nicht mit denen aus
`results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md` vergleichbar.

**`docs/DATENLUECKEN.md` betrifft diese Untersuchung nicht:** das Register hält
Lücken der **Forward-Test**-Daten fest; hier wird der Backtest über die CSVs in
`data/` ausgewertet. Für die Live-Seite würde es gelten — wer
`live_haltedauern.py` auf dem Rechner des Nutzers laufen lässt, muss dort
zuerst hineinsehen.

### Was diese Untersuchung nicht beantwortet

* **Ob die Strategien gut sind.** Gemessen wird, *wann* ein Ergebnis anfällt,
  nicht *ob* es gut ist. Kein Satz ist ein Renditeurteil.
* **Wie hoch die Ergebniskorrelation ist.** Dafür ist
  `research/exposure_messung/` zuständig. Hier wird die **Lage** von Positionen
  und Einstiegen gemessen, nicht ihr Ertrag.
* **Ob die Ertragsquellen-Einteilung stimmt.** Sie ist eine **Lesart**, offen
  hingeschrieben in `auswertung.py` (`ERTRAGSQUELLE`), nicht gemessen. Die
  externe Analyse zählt „vier Trendfolge, vier Mean-Reversion"; diese
  Untersuchung zählt **drei Trend, vier Umkehr und zwei Muster** — die beiden
  Elliott-Bots handeln der Sache nach gegen den vorherigen Trend, aber weder
  einen Mittelwert-Rücklauf noch eine Ausbruchsfortsetzung. Die Abweichung ist
  benannt, nicht aufgelöst. **Die Befunde aus Abschnitt 2 hängen daran:**
  stellte man die Elliott-Bots zu „Umkehr", wanderten die acht „Muster +
  Umkehr"-Paare in die Gruppe „gleiche Quelle" und senkten deren Median von
  1,94 auf etwa 1,5. Die Richtung bliebe, die Höhe nicht.
* **Wie belastbar der Quellen-Befund ist.** Die Gruppe „gleiche Quelle" besteht
  aus **drei** ungeordneten Paaren (`rsi2_mean_reversion`/`turtle_soup_stocks`,
  `rsi2_crypto`/`turtle_soup_crypto`,
  `t3_supertrend`/`volatility_breakout_crypto`). Alle drei zeigen in dieselbe
  Richtung und der Abstand zur Gegengruppe ist gross, aber drei Paare sind drei
  Paare. Mehr Bots gleicher Quelle in derselben Anlageklasse gibt es nicht.
* **Die Live-Seite** (Abschnitt 6) und **warum ein Versatz auftritt**
  (Abschnitt 4).

---

## 9. Nebenbefund: die Zeitbremse von `elliott_wave_stocks`, beziffert

Beim Aufstellen der Zeitbremsen-Tabelle aufgefallen. **Kein Fehler, nicht
angefasst, nur beziffert.**

`elliott_wave_stocks/backtest_elliott.py:70` bremst nach `MAX_HOLD_HOURS = 90`
**Tagesbalken**; `elliott_wave_stocks/forward_test.py:51` nach
`MAX_HOLD_DAYS = 130` **Kalendertagen**, mit dem Kommentar „entspricht ~90
Handelstagen". Die Näherung ist als Näherung gekennzeichnet — jetzt ist sie
gemessen: die 82 Zeitausstiege des Backtests liegen bei **128 bis 134**
Kalendertagen (Median 131, Q1 129, Q3 132). Eine Live-Bremse bei 130 Tagen
schneidet also je Trade bis zu **4 Tage früher** oder **2 Tage später** als die
Backtest-Regel. Bei vier Monaten Haltedauer ist das wenig, und der Sync-Check
kann es nicht sehen: die beiden Grössen sind verschieden (Balken gegen
Kalendertage) und lassen sich nicht koppeln.

**Die sechs Bots mit `MAX_HOLD_DAYS` in `live_params.py` sind nicht
betroffen** — geprüft für alle sechs: ihre `forward_test.py` zählt Balken über
die Kursreihe (`if offset + 1 >= MAX_HOLD_DAYS`), genau wie ihr Backtest.
`elliott_wave` (Krypto) ebenfalls nicht: 240 Stundenbalken sind bei
durchlaufenden Krypto-Kerzen exakt 240 Stunden, und `forward_test.py` rechnet
mit `timedelta(hours=240)`.

---

## 10. Reproduktion

```bash
python3 research/tb24_haltedauern/alle_bots.py            # ~4 min, neun Prozesse
python3 research/tb24_haltedauern/auswertung.py           # ~1 min
python3 research/tb24_haltedauern/test_haltedauer_kern.py # 51 Pruefungen
python3 research/tb24_haltedauern/live_haltedauern.py     # nur auf dem Mac sinnvoll
git diff origin/main HEAD --name-only                     # nur research/tb24_haltedauern/ und docs/
```

**Zur Umgebung.** In der Cloud fehlen `pandas`, `numpy`, `scipy`, `yfinance`,
`binance` und `fastapi` im System-Python. Das ist **vorbestehend**, mit einem
Basislauf auf unverändertem `main` nachgewiesen:

```
$ python3 -c "import pandas"
ModuleNotFoundError: No module named 'pandas'
$ python3 research/exposure_messung/bot_lauf.py elliott_wave   # unveraenderte main-Datei
ModuleNotFoundError: No module named 'pandas'
```

Gerechnet wurde in einer venv mit `pandas` und `numpy` — nur diese beiden
werden gebraucht. **`scipy` bewusst nicht:** die Zweigipfligkeit ist ohne
Verteilungsannahme gemessen (Überschneidung der Quartilsbereiche), damit die
Untersuchung keine Abhängigkeit einführt, die auf dem Rechner des Nutzers
fehlen könnte. `yfinance` und `binance` werden nicht gebraucht: die Bot-Module
laufen mit den Stubs aus `bot_lauf.py` und lesen ausschliesslich die
vorhandenen CSVs unter `data/`. Auf dem Rechner des Nutzers (`trading-env`,
Python 3.9.6) läuft alles ohne diesen Zwischenschritt.

---

## 11. Dateien dieses Vorgangs

| Datei | Zweck |
|---|---|
| `research/tb24_haltedauern/BERICHT.md` | vollständiger Bericht |
| `research/tb24_haltedauern/positionen_holen.py` | Positionen aus dem echten Bot-Code, mit Ausstiegsart und gezählter Kerzenzahl |
| `research/tb24_haltedauern/alle_bots.py` | alle neun Bots, je ein Prozess |
| `research/tb24_haltedauern/haltedauer_kern.py` | Rechenkern |
| `research/tb24_haltedauern/auswertung.py` | schreibt alle Tabellen nach `ergebnisse/` |
| `research/tb24_haltedauern/live_haltedauern.py` | Live-Seite, schreibgeschützt |
| `research/tb24_haltedauern/test_haltedauer_kern.py` | 51 Prüfungen |
| `research/tb24_haltedauern/daten/` | 9 × Positionen, 9 × alle Trades, 9 × Meta |
| `research/tb24_haltedauern/ergebnisse/` | 9 Ergebnistabellen + `zusammenfassung.json` |
| `docs/ERGEBNIS_TB24_haltedauern.md` | Kurzfassung zum Kopieren |
| `docs/UEBERGABE_TB24_haltedauern.md` | dieses Dokument |

**Kein Testauftrag-Dokument.** Ein autonom ausführbares Testdokument ist laut
Aufgabenstellung nur nötig, wenn bleibender ausführbarer Code entsteht. Der
Code hier bleibt als **Untersuchungswerkzeug** unter `research/` und fasst
keinen Bot an; seine Prüfung ist `test_haltedauer_kern.py`, das
Gegenproben **und** Mutationsproben enthält und mit einem Aufruf läuft.

---

## 12. Folgeaufgaben — benannt, nicht ausgeführt

Was aus dem Ergebnis folgt, entscheidet der Nutzer. Fünf Anschlussfragen, die
sich aus den Zahlen ergeben:

1. **Eine Horizont-Dimension bewusst wählen statt einstellen.** Die Zeitbremsen
   der sieben Tages-Bots liegen alle bei 10 bis 15 Tagen bzw. Handelstagen.
   Jede ist einzeln validiert; keine wurde je gegen die anderen sechs gesetzt.
   Die Frage „welcher Horizont fehlt dem Portfolio" ist nie gestellt worden —
   sie wäre eine Optimierung auf **Portfolio-Ebene**, und das Projekt hat
   bisher ausschliesslich je Bot optimiert.
2. **Den Quellen-Befund als Aufnahmekriterium prüfen.** Der Nähe-Überschuss
   gegen Zufall ist für jeden Kandidaten **vor** seiner Aufnahme berechenbar —
   er braucht keine Live-Historie, nur Backtest-Trades. Ob das ein sinnvolles
   Kriterium ist, ist offen.
3. **Bei K1 zuerst die Haltedauer klären, dann den Takt.** Der
   Strategie-Katalog mit B1 und K1 liegt **nicht im Repo** (geprüft: unter „K1"
   findet sich nur eine gleichnamige Kausalitätsbedingung in
   `docs/KONZEPT_sentiment_sammelschicht.md`). **B1 / ETF-Trend, monatlich**
   läge ausserhalb aller neun Mediane und wäre eine echte
   Horizontergänzung. **K1, „Wochenfrist"** ist zweideutig: heisst es
   *Haltedauer* eine Woche, landet K1 mitten im gedrängten Fenster und ist
   **keine** Horizontergänzung; heisst es *wöchentlicher Entscheidungstakt* mit
   mehrwöchiger Haltedauer, liegt es bei
   `turtle_soup_stocks`/`volatility_breakout`.
4. **Das Kriterium aus Protokoll 9.4 kann sich auf diese Zahlen stützen.** Für
   `elliott_wave_stocks` ist der Prüftermin Oktober 2026 / Januar 2027 auf
   „gleiche Zeit im Markt gegen das 95. Perzentil von Zufalls-Timing"
   festgelegt, und das Kriterium ist noch nicht gemessen. Dieser Bericht
   liefert die Haltedauer-Verteilung, die eine solche Ziehung braucht: Median
   7 Tage, **zweigipflig** — 79,2 % Stops bei 5 Tagen, 20,8 % Zeitausstiege bei
   131 Tagen. Eine Ziehung mit einer einzigen mittleren Haltedauer (36 Tage)
   träfe den Bot nicht.
5. **`docs/UEBERSICHT_RESEARCH.md` hinkt nach.** Die Übersicht der
   `research`-Urteile hat den Stand **2026-09-12** und führt **18** Ordner;
   `ls research/` listet auf `main` inzwischen **19** (`drawdown_reihenfolge`
   fehlt) und mit dieser Untersuchung **20**. Ein Nachtrag wäre eine kleine,
   eigene Aufgabe — hier bewusst **nicht** ausgeführt, weil die Übersicht eine
   datierte Erhebung mit eigener Methodik ist (jede Zahl aus einem `BERICHT.md`
   zitiert) und nicht nebenbei fortgeschrieben werden sollte.
