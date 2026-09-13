# Streut das Portfolio über Zeithorizonte? (TB-24)

**Status: reine Untersuchung. KEINE Änderung an Bot-, Backtest- oder
Live-Dateien.** Alle Dateien liegen unter `research/tb24_haltedauern/`;
`git diff origin/main HEAD --name-only` listet nur diesen Ordner und `docs/`.
Es wird **keine Empfehlung umgesetzt** — was aus den Zahlen folgt, entscheidet
der Nutzer.

---

## 1. Die Antwort zuerst

**Die Vermutung trifft zu, auf die Zahl genau.**

> *„Sechs der neun haben Median-Haltedauern zwischen drei und zehn Tagen und
> bespielen ein Fenster."*

Es sind **genau sechs** — und sie liegen sogar in einem engeren Band als
vermutet, zwischen **3,9 und 7,0 Kalendertagen**:

| Bot | Median-Haltedauer | Ertragsquelle |
|---|---:|---|
| `elliott_wave` (1h, Krypto) | **3,90 Tage** | Muster |
| `rsi2_crypto` | **4,00 Tage** | Umkehr |
| `turtle_soup_crypto` | **4,00 Tage** | Umkehr |
| `rsi2_mean_reversion` | **5,00 Tage** | Umkehr |
| `volatility_breakout_crypto` | **6,00 Tage** | Trend |
| `elliott_wave_stocks` | **7,00 Tage** | Muster |

Die drei übrigen liegen nicht weit weg: `t3_supertrend` bei **2,67 Tagen**
(knapp unterhalb des Fensters), `turtle_soup_stocks` bei **14,0** und
`volatility_breakout` bei **21,0 Tagen**.

**Die Medianwerte aller neun Bots liegen zwischen 2,67 und 21,0 Kalendertagen —
das gesamte Portfolio spielt innerhalb von drei Wochen.** Kein Bot hält im
Median länger als drei Wochen; sieben von neun nicht länger als eine Woche. Es
ist derselbe Befund wie bei der Korrelationsmessung: eine Streuung, die
niemand gemessen hatte, und die es nicht gibt.

**Der zweite Befund geht aber über die Frage hinaus und ist der wichtigere.**
Die Untersuchung sollte prüfen, ob der Horizont eine zweite
Diversifikationsdimension ist. Gemessen ist: **der Horizont trennt nichts.**
Was zwei Bots dazu bringt, dasselbe zu tun, ist die Ertragsquelle, nicht der
Horizont:

| Bot-Paar (geordnet, gleiche Anlageklasse) | Median-Überschuss der gleichzeitigen Einstiege gegen Zufall |
|---|---:|
| **gleiche Ertragsquelle** (6 Paare) | **1,94 ×** (Spanne 1,68 bis 3,27) |
| verschiedene Ertragsquelle (26 Paare) | **0,32 ×** (Spanne 0,00 bis 2,19) |
| **gleiche Horizont-Klasse** (16 Paare) | **0,32 ×** |
| verschiedene Horizont-Klasse (16 Paare) | **1,10 ×** |

Gleiche Quelle heisst: die beiden Bots eröffnen im selben Titel rund doppelt
so oft innerhalb von drei Tagen wie bei zufälliger Lage — bei
`rsi2_mean_reversion` und `turtle_soup_stocks` **3,27-mal** so oft, in
absoluten Zahlen **1.523 gemeinsame Einstiegsereignisse**. Gleicher Horizont
heisst dagegen **nichts**: die Zahl liegt dort sogar unter dem Zufallswert.

**Für die Einordnung aus der Aufgabenstellung bedeutet das:** Der Satz
„Horizont-Streuung ohne Quellen-Streuung schützt nicht" ist hier nicht nur
eine Vorsichtsregel — er ist die Messung. Der umgekehrte Fall tritt ebenfalls
auf: `volatility_breakout` und `rsi2_mean_reversion` liegen in
**verschiedenen** Horizont-Klassen (21 gegen 5 Tage) und steigen trotzdem
**seltener** gemeinsam ein als der Zufall (0,15 ×) — weil ihre Quellen
entgegengesetzt sind. Ein Ausbruch und ein Mittelwert-Rücklauf entstehen in
verschiedenen Marktzuständen; das ist echte Streuung, und sie kommt nicht vom
Horizont.

**Und eine Ursache, die mit Markt nichts zu tun hat:** Die obere Grenze jeder
Haltedauer-Verteilung ist ein **Parameter**, kein Marktverhalten. Bei jedem
der acht Bots mit Zeitausstieg liegt der Median der Zeitausstiege exakt auf
`MAX_HOLD_DAYS` bzw. `MAX_HOLD_HOURS` — 10 Tagesbalken bei vier Bots, 15 bei
zwei, 90 bei einem, 240 Stundenbalken (= 10 Tage) bei `elliott_wave`. Das
Portfolio ist bei drei bis zehn Tagen gedrängt, weil **sieben von neun Bots
eine Zeitbremse von 10 bis 15 Tagen bzw. Handelstagen** haben. Der Horizont ist hier nicht
gewachsen, er ist eingestellt worden — jedes Mal einzeln und plausibel, aber
nie mit Blick auf die anderen acht.

---

## 2. Entscheidungsgrundlage

### 2.1 Datenbasis

| Bot | Zeitrahmen | Trades gefunden | ausgeführt | Symbole | erster Einstieg | letzter Ausstieg |
|---|---|---:|---:|---:|---|---|
| `elliott_wave` | 1 h | 130 | 130 | 18 | 2021-09-22 | 2026-08-20 |
| `t3_supertrend` | 4 h | 980 | 656 | 18 | 2021-09-01 | 2026-08-29 |
| `rsi2_crypto` | 1 d | 439 | 392 | 18 | 2022-02-11 | 2026-08-20 |
| `turtle_soup_crypto` | 1 d | 1.599 | 1.414 | 20 | 2021-10-12 | 2026-08-28 |
| `volatility_breakout_crypto` | 1 d | 233 | 207 | 19 | 2022-03-17 | 2026-08-30 |
| `elliott_wave_stocks` | 1 d | 510 | 395 | 127 | 2016-10-28 | 2026-09-01 |
| `rsi2_mean_reversion` | 1 d | 5.391 | 4.232 | 147 | 2016-09-01 | 2026-09-01 |
| `turtle_soup_stocks` | 1 d | 12.069 | 8.915 | 147 | 2016-09-01 | 2026-09-01 |
| `volatility_breakout` | 1 d | 4.510 | 1.454 | 147 | 2016-09-01 | 2026-09-01 |

Zusammen **17.795 ausgeführte Positionen** aus 25.861 gefundenen Trades.
Kursdaten aus `data/`, unvollständige Kerzen über `shared/kursdaten.py`
gestrichen und gezählt (gemeldet: 1 Kerze, `APH` — der bekannte Fall aus
Protokoll 3.3).

Gerechnet wird auf den **ausgeführten** Positionen, also nach
`MAX_CONCURRENT_POSITIONS` und Kapitalprüfung: das ist das Buch, das ein Bot
tatsächlich hält. Die Gegenprobe über **alle** gefundenen Trades — also
einschliesslich der 8.066 übersprungenen — steht in Abschnitt 3.4.

### 2.2 Welche Datenquelle, und warum

**Backtest-Trades, nicht Live-Datenbanken — und das ist keine Wahl, sondern
der Stand.** Die Begründung in zwei Teilen:

*Erstens, was zur Verfügung steht.* Die neun `paper_trading_<bot>.db` sind
laut `.gitignore` nicht im Repo und liegen nur auf dem Rechner des Nutzers; in
einer Cloud-Sitzung sind sie **nicht vorhanden**. Nachgesehen wurde, nicht
angenommen: `live_haltedauern.py` meldet „keine Datenbank gefunden" für 9 von
9 Bots.

*Zweitens, was sie tragen würden.* Selbst auf dem Rechner des Nutzers trägt
die Live-Seite diese Frage nicht. Laut Protokoll 4.3b erreicht **kein** Bot
`MIN_LIVE_CLOSED_TRADES = 10` geschlossene Trades; bei rund zwei Dutzend
geschlossenen Trades über neun Bots wäre ein Median je Bot eine Zahl aus zwei
bis vier Werten, und eine Überlappungsmatrix über neun Bots hätte pro Paar
meist null gemeinsame Positionstage. Die Aufgabenstellung sagt dasselbe
voraus; die Messung bestätigt es.

**Die Live-Seite ist deshalb nicht weggelassen, sondern vorbereitet.**
`live_haltedauern.py` ist auf dem Rechner des Nutzers ohne Vorbereitung
lauffähig, liest jede Datenbank über `file:…?mode=ro` (dieselbe Betriebsart
wie `notifications/monitor.py` und `broker/bot_db.py`) und weist manuelle
Ausstiege (`result = 'manual_close'`) **getrennt** aus — ihre Haltedauer ist
eine Entscheidung des Nutzers, keine Eigenschaft der Strategie. Es schreibt
den Vorbehalt zur Trade-Anzahl in seine eigene Ausgabe, damit die Zahl nicht
irgendwann ohne ihn weiterwandert.

Dass eine Meldung „keine Datenbank gefunden" nichts über die Richtigkeit des
Lesewegs beweist, ist Prinzip 12. Abschnitt 14 der Selbsttests baut deshalb
eine Datenbank mit dem echten Schema auf, füllt sie mit von Hand
nachrechenbaren Trades und prüft das Ergebnis (Median 6,5 Tage aus 3 und 10
Tagen; der offene Trade wird nicht gelesen, der manuelle nicht gemittelt;
`mode=ro` weist einen Schreibversuch ab).

### 2.3 Haltedauern je Bot

Kalendertage als exakte Differenz `exit_time − entry_time`; die Kerzenzahl ist
aus der Kursreihe des Symbols **gezählt**, nicht umgerechnet.
(`ergebnisse/haltedauern_je_bot.csv`)

| Bot | n | P10 | Q1 | **Median** | Q3 | P90 | Max | Mittel | Kerzen (Median) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `elliott_wave` | 130 | 0,21 | 0,68 | **3,90** | 10,0 | 10,0 | 10,1 | 5,07 | 94,5 (1h) |
| `t3_supertrend` | 656 | 0,50 | 1,00 | **2,67** | 6,0 | 9,5 | 22,7 | 3,99 | 17,0 (4h) |
| `rsi2_crypto` | 392 | 1,00 | 2,00 | **4,00** | 5,0 | 7,0 | 10,0 | 4,04 | 5,0 (1d) |
| `turtle_soup_crypto` | 1.414 | 1,00 | 1,00 | **4,00** | 10,0 | 10,0 | 10,0 | 4,98 | 5,0 (1d) |
| `volatility_breakout_crypto` | 207 | 1,00 | 2,00 | **6,00** | 15,0 | 15,0 | 15,0 | 7,52 | 7,0 (1d) |
| `elliott_wave_stocks` | 395 | 1,00 | 2,00 | **7,00** | 47,5 | 131,0 | 134,0 | 36,34 | 6,0 (1d) |
| `rsi2_mean_reversion` | 4.232 | 2,00 | 3,00 | **5,00** | 7,0 | 11,0 | 18,0 | 5,75 | 4,0 (1d) |
| `turtle_soup_stocks` | 8.915 | 14,00 | 14,00 | **14,00** | 15,0 | 15,0 | 18,0 | 14,51 | 11,0 (1d) |
| `volatility_breakout` | 1.454 | 12,00 | 21,00 | **21,00** | 22,0 | 23,0 | 26,0 | 19,82 | 16,0 (1d) |

Drei Dinge, die nur der Median-samt-Perzentilen-Blick zeigt und der
Mittelwert allein verdeckt:

* **`elliott_wave_stocks` ist der einzige Bot mit einem langen Schwanz.**
  Median 7 Tage, P90 **131** Tage, Mittelwert 36 Tage. Wer nur den
  Mittelwert liest, hält ihn für einen Mehrwochen-Bot; wer nur den Median
  liest, für einen Wochen-Bot. Beides ist falsch: er ist beides, in einem
  Verhältnis von 4 zu 1 (siehe 2.4).
* **`turtle_soup_stocks` hat praktisch keine Streuung.** P10 = Q1 = Median =
  14 Tage. Er hat als einziger Bot gar keinen Stop (`STOP_MODE = None`, bewusst
  so validiert), also endet **jeder** seiner 8.915 Trades im Zeitausstieg. Sein
  „Horizont" ist genau eine Zahl aus `live_params.py` und sonst nichts.
* **Die Kerzenzahl und die Kalendertage sagen Verschiedenes.** Bei
  `turtle_soup_stocks` sind 11 Kerzen 14 Kalendertage (Wochenenden), bei
  `elliott_wave` sind 94,5 Kerzen 3,9 Tage (Stundenkerzen, durchlaufend). Nur
  die Kalenderangabe ist zwischen den drei Zeitrahmen vergleichbar; nur die
  Kerzenzahl sagt, wie viele Entscheidungen der Bot getroffen hat.

### 2.4 Die Verteilungsform: acht von neun sind zweigipflig

Jeder Bot mit mehr als einer Ausstiegsart hat **zwei klar getrennte Gruppen**,
und die Trennlinie ist die Ausstiegsart. Geprüft ohne Verteilungsannahme
(`scipy` ist in dieser Umgebung nicht installiert): überschneiden sich die
Quartilsbereiche der beiden häufigsten Ausstiegsarten? Bei acht von neun Bots:
**nein**. (`ergebnisse/verteilungsform.csv`,
`ergebnisse/haltedauern_je_ausstiegsart.csv`)

| Bot | früher Gipfel (Stop) | Anteil | späterer Gipfel (Zeit/Trend) | Anteil |
|---|---:|---:|---:|---:|
| `elliott_wave` | 0,88 T (`stop_loss`) | 53,8 % | 10,00 T (`time_exit`) | 33,8 % |
| `t3_supertrend` | 1,17 T (`stop_loss`) | 53,0 % | 5,33 T (`trend_flip`) | 30,8 % |
| `rsi2_crypto` | 4,00 T (`sma_exit`) | 98,0 % | 10,00 T (`time_exit`) | 2,0 % |
| `turtle_soup_crypto` | 2,00 T (`stop_loss`) | 69,0 % | 10,00 T (`time_exit`) | 31,0 % |
| `volatility_breakout_crypto` | 3,00 T (`stop_loss`) | 71,0 % | 15,00 T (`time_exit`) | 29,0 % |
| `elliott_wave_stocks` | 5,00 T (`stop_loss`) | 79,2 % | **131,00 T** (`time_exit`) | 20,8 % |
| `rsi2_mean_reversion` | 5,00 T (`sma_exit`) | 96,8 % | 14,00 T (`time_exit`) | 3,2 % |
| `turtle_soup_stocks` | — | — | 14,00 T (`time_exit`) | 100,0 % |
| `volatility_breakout` | 12,00 T (`stop_loss`) | 19,8 % | 22,00 T (`time_exit`) | 80,2 % |

**Daraus folgt die Mechanik des Befundes.** Der späte Gipfel ist bei jedem Bot
die eingestellte Zeitbremse, auf den Tag:

| Bot | Zeitbremse (Balken) | ergibt Kalendertage | gemessener Median der Zeitausstiege |
|---|---|---|---:|
| `elliott_wave` | `MAX_HOLD_HOURS = 240` (1h) | 10,0 | **10,00** |
| `rsi2_crypto`, `turtle_soup_crypto` | `MAX_HOLD_DAYS = 10` (Krypto, durchlaufend) | 10 | **10,00** |
| `volatility_breakout_crypto` | `MAX_HOLD_DAYS = 15` | 15 | **15,00** |
| `rsi2_mean_reversion`, `turtle_soup_stocks` | `MAX_HOLD_DAYS = 10` (Handelstage) | ~14 | **14,00** |
| `volatility_breakout` | `MAX_HOLD_DAYS = 15` (Handelstage) | ~21 | **22,00** |
| `elliott_wave_stocks` | `MAX_HOLD_HOURS = 90` (Tagesbalken) | ~130 | **131,00** |

Der **Median eines Bots** ist damit im Wesentlichen die Antwort auf eine
einzige Frage: *wie oft feuert der Stop, bevor die Uhr abläuft?* Bei
`turtle_soup_stocks` nie (kein Stop) — Median 14. Bei `elliott_wave` in 54 %
der Fälle — Median 3,9. Bei `rsi2_mean_reversion` läuft der `sma_exit` dem
Zeitausstieg in 96,8 % der Fälle zuvor — Median 5.

Das ist der Grund, warum das Fenster „drei bis zehn Tage" so besetzt ist: es
ist kein Marktbefund, sondern die Folge von sieben einzeln getroffenen
Entscheidungen, die alle bei 10 bis 15 Balken landeten.

### 2.5 Die Überlappungsmatrix

Beide Zahlen sind aus Sicht von A gerechnet und im **gemeinsamen Fenster**
beider Bots (die Historien starten zwischen 2016 und 2022; ohne Fensterschnitt
sähe jeder spät gestartete Bot künstlich unauffällig aus). Die Zahlen sind
**nicht symmetrisch**: ein Bot mit wenigen Positionstagen kann vollständig in
den Tagen eines Dauer-Investierten liegen, umgekehrt nicht.
(`ergebnisse/ueberlappungsmatrix.csv`)

Kürzel: EW = `elliott_wave`, T3 = `t3_supertrend`, R2c = `rsi2_crypto`,
TSc = `turtle_soup_crypto`, VBc = `volatility_breakout_crypto`,
EWs = `elliott_wave_stocks`, R2s = `rsi2_mean_reversion`,
TSs = `turtle_soup_stocks`, VBs = `volatility_breakout`.

**(a) Anteil der Positionstage von A, an denen auch B eine Position hält (%)**

| A ↓ / B → | EW | T3 | R2c | TSc | VBc | EWs | R2s | TSs | VBs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **EW** | – | 52,1 | 41,8 | 97,0 | 23,5 | 89,5 | 93,2 | **100,0** | **100,0** |
| **T3** | 21,4 | – | 33,7 | 90,3 | 45,4 | 94,2 | 89,5 | **100,0** | 99,7 |
| **R2c** | 20,4 | 42,4 | – | 95,8 | 34,1 | 93,3 | 93,1 | **100,0** | 99,6 |
| **TSc** | 23,4 | 54,0 | 45,9 | – | 32,6 | 95,7 | 91,5 | **100,0** | 99,5 |
| **VBc** | 14,6 | 74,6 | 45,0 | 87,7 | – | 96,1 | 91,5 | **100,0** | 99,8 |
| **EWs** | 21,4 | 55,7 | 43,5 | 92,8 | 34,8 | – | 88,7 | **100,0** | 96,9 |
| **R2s** | 23,3 | 54,7 | 45,6 | 93,2 | 34,9 | 90,6 | – | **100,0** | 98,3 |
| **TSs** | 22,8 | 55,9 | 44,6 | 92,9 | 34,6 | 91,0 | 89,2 | – | 97,0 |
| **VBs** | 22,9 | 56,0 | 44,6 | 92,9 | 34,7 | 90,9 | 90,4 | **100,0** | – |

Der Median über alle 72 geordneten Paare liegt bei **89,5 %**. Die Spalte TSs
steht durchgehend auf 100 %, weil dieser Bot an **allen 3.653** Tagen seines
Zeitraums eine Position hält. Diese Zahl misst darum vor allem, **wie oft ein
Bot überhaupt im Markt ist** — und beantwortet die Frage nach gemeinsamem
Verhalten fast nicht. Sie gehört als Nenner in den Bericht, nicht als Befund.

**(b) Anteil der (Titel, Tag)-Paare von A, die auch B hält (%)** — dieselben
Positionen, aber auf denselben Titel bezogen. Über Anlageklassen hinweg ist
die Zahl per Konstruktion 0 (kein gemeinsames Symbol) und deshalb hier
weggelassen.

| Krypto: A ↓ / B → | EW | T3 | R2c | TSc | VBc |
|---|---:|---:|---:|---:|---:|
| **EW** | – | 13,7 | 7,9 | **25,5** | 0,6 |
| **T3** | 3,4 | – | 0,9 | 23,1 | 12,8 |
| **R2c** | 2,8 | 1,3 | – | **39,3** | 2,0 |
| **TSc** | 2,3 | 8,7 | 9,8 | – | 3,6 |
| **VBc** | 0,2 | **21,7** | 2,3 | 16,1 | – |

| Aktien: A ↓ / B → | EWs | R2s | TSs | VBs |
|---|---:|---:|---:|---:|
| **EWs** | – | 3,1 | **24,9** | 4,8 |
| **R2s** | 1,6 | – | **48,6** | 3,3 |
| **TSs** | 2,7 | 10,0 | – | 3,7 |
| **VBs** | 2,4 | 3,1 | 17,1 | – |

Das stärkste Paar ist **`rsi2_mean_reversion` → `turtle_soup_stocks` mit
48,6 %**: fast jeder zweite Titel-Tag dieses Bots ist ein Titel-Tag, den
`turtle_soup_stocks` gleichzeitig hält. Der Median innerhalb der Anlageklasse
liegt bei 3,7 %, das Mittel bei 10,1 %.

Und hier liegt schon der Hinweis auf das Ergebnis von 2.6: die hohen Werte
stehen bei Paaren **gleicher Quelle** (R2s/TSs, R2c/TSc: Umkehr+Umkehr;
VBc/T3: Trend+Trend), die niedrigsten bei gemischten (VBc/EW mit 0,2 %). Über
alle Paare gleicher Anlageklasse: **gleiche Quelle Median 17,3 %, verschiedene
Quelle Median 3,2 %**. Nach Horizont-Klasse sortiert kommt das Gegenteil
heraus (gleicher Horizont 3,4 %, verschiedener 6,7 %) — der Horizont erklärt
diese Zahlen nicht.

**(c) Die interessantere Zahl: Einstiege im selben Titel innerhalb von drei
Tagen.** (`ergebnisse/naehe_der_einstiege.csv`)

Ein roher Anteil wäre hier unlesbar: ein Bot mit 8.915 Einstiegen in 147
Titeln trifft ein Drei-Tage-Fenster auch ohne jeden Zusammenhang oft.
Gemessen wird deshalb zusätzlich, **was bei zufälliger Lage herauskäme** — die
Einstiegstage von B werden je Symbol auf zufällige Tage im gemeinsamen Fenster
gelegt (200 Ziehungen, feste Saat; Anzahl und Symbolverteilung bleiben
gleich). Der Quotient `Überschuss` ist die eigentliche Zahl: 1,0 heisst „nicht
mehr als Zufall".

Die stärksten und die schwächsten Paare:

| A → B | Treffer / Einstiege A | gemessen | Zufall | **Überschuss** |
|---|---:|---:|---:|---:|
| `rsi2_mean_reversion` → `turtle_soup_stocks` | 1.523 / 4.232 | 36,0 % | 11,0 % | **3,27 ×** |
| `turtle_soup_stocks` → `rsi2_mean_reversion` | 1.523 / 8.915 | 17,1 % | 5,4 % | **3,16 ×** |
| `turtle_soup_crypto` → `elliott_wave` | 81 / 1.414 | 5,7 % | 2,6 % | 2,19 × |
| `elliott_wave` → `turtle_soup_crypto` | 68 / 128 | 53,1 % | 25,5 % | 2,08 × |
| `turtle_soup_crypto` → `rsi2_crypto` | 231 / 1.343 | 17,2 % | 8,6 % | 1,99 × |
| `volatility_breakout_crypto` → `t3_supertrend` | 48 / 207 | 23,2 % | 13,3 % | 1,74 × |
| … | | | | |
| `volatility_breakout` → `rsi2_mean_reversion` | 12 / 1.454 | 0,8 % | 5,3 % | **0,15 ×** |
| `elliott_wave_stocks` → `rsi2_mean_reversion` | **0** / 395 | 0,0 % | 5,1 % | **0,00 ×** |
| `elliott_wave_stocks` → `volatility_breakout` | **0** / 395 | 0,0 % | 1,8 % | **0,00 ×** |

Der Zufallswert ist zweimal gerechnet: über die Ziehung und in geschlossener
Form (`naehe_erwartet_analytisch`, die Wahrscheinlichkeit, dass bei
gleichverteilter Lage mindestens ein B-Einstieg ins Fenster fällt). Beide
stimmen in allen 32 Paaren auf 0,1 Prozentpunkte überein — die Ziehung ist
also keine eigene Annahme, sondern eine Kontrollrechnung derselben Grösse.

### 2.6 Was die Überlappung erklärt: Quelle, nicht Horizont

(`ergebnisse/naehe_der_einstiege.csv`, ausgewertet nach Quellen- und
Horizont-Paaren)

| Quellen-Paar | geordnete Paare | Median-Überschuss | Spanne |
|---|---:|---:|---|
| Umkehr + Umkehr | 4 | **2,58 ×** | 1,89 – 3,27 |
| Trend + Trend | 2 | **1,71 ×** | 1,68 – 1,74 |
| Muster + Umkehr | 8 | 1,43 × | 0,00 – 2,19 |
| **Trend + Umkehr** | 12 | **0,32 ×** | 0,15 – 0,93 |
| **Muster + Trend** | 6 | **0,18 ×** | 0,00 – 1,78 |

Das ist ein sauberes Bild, und es sagt zweierlei:

1. **Gleiche Quelle = gemeinsames Handeln.** Alle sechs Paare gleicher Quelle
   liegen über 1,68 ×. Keine Ausnahme.
2. **Trendfolge und Mean-Reversion schliessen sich gegenseitig aus.** Alle
   zwölf Trend-Umkehr-Paare liegen **unter 0,95** (Spanne 0,15 bis 0,93). Ein
   Bollinger-Ausbruch entsteht, wenn die Bandbreite explodiert; ein
   RSI-2-Signal, wenn der Kurs zwei Tage lang fällt. Diese Zustände treten im
   selben Titel kaum gleichzeitig auf. **Das ist die echte Streuung im
   Portfolio** — sie ist gemessen, und sie hat mit dem Horizont nichts zu tun.

**Der auffälligste Einzelfall ist gleichzeitig die Bestätigung, dass „nicht
gleichzeitig" nicht „unabhängig" heisst.** `elliott_wave_stocks` und
`rsi2_mean_reversion` steigen in **0 von 395** Fällen innerhalb von drei Tagen
gemeinsam ein, obwohl sie 127 Titel teilen und Zufall etwa 20 Treffer erwarten
liesse. Die Verteilung des **Versatzes** zeigt, warum
(`ergebnisse/versatz_der_einstiege.csv`): der nächstgelegene
`rsi2_mean_reversion`-Einstieg liegt im Median **14 Tage vor** dem
Elliott-Einstieg, und die Klassen von −3 bis +3 Tagen sind **leer**:

| Versatz (Tage, negativ = R2s zuerst) | < −30 | −30…−20 | −20…−10 | −10…−3 | **−3…0** | **0…+3** | +3…+10 | +10…+20 | +20…+30 | ≥ +30 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Anzahl (von 395) | 213 | 21 | 36 | 15 | **0** | **0** | 1 | 3 | 7 | 99 |

Die beiden Bots handeln denselben Kursrückgang — nur nacheinander. Das ist
genau die „Scheinstreuung, die eine reine Positionsüberlappung nicht zeigt",
nach der die Aufgabenstellung fragt, in ihrer zweiten Gestalt: nicht
gleichzeitig mit leichtem Versatz, sondern **sequenziell mit festem Versatz**.
Ein Drei-Tage-Fenster allein hätte dieses Paar als unabhängig eingeordnet.

Eine naheliegende Erklärung liefern die Einstiegsregeln: RSI-2 kauft das
Tief selbst (RSI(2) unter 5), während ein Zigzag-Pivot erst dann ein Pivot
ist, wenn der Kurs sich um `DEVIATION_PCT = 5 %` in die Gegenrichtung bewegt
hat — der Elliott-Einstieg liegt also strukturell **nach** der Gegenbewegung.
Diese Erklärung ist **plausibel, aber nicht Teil der Messung**; gemessen ist
der Versatz, nicht seine Ursache.

### 2.7 Wie viele unterscheidbare Zeitfenster bespielt das Portfolio?

Die Klassengrenzen sind **vorab** festgelegt und nicht aus den Daten gewonnen:
die Klasse „3 bis 10 Tage" stammt wörtlich aus der zu prüfenden Vermutung, die
übrigen setzen sie fort. Eine aus den gemessenen Medianen gebildete
Klassierung würde die Vermutung an sich selbst prüfen.

| Horizont-Klasse | Bots | Ertragsquellen darin |
|---|---|---|
| bis 2 Tage | `t3_supertrend` | Trend |
| **3 bis 10 Tage** | **`elliott_wave`, `rsi2_crypto`, `turtle_soup_crypto`, `volatility_breakout_crypto`, `elliott_wave_stocks`, `rsi2_mean_reversion`** | **Muster, Trend, Umkehr** |
| 11 bis 30 Tage | `turtle_soup_stocks`, `volatility_breakout` | Umkehr, Trend |
| 31 bis 90 Tage | — | — |
| über 90 Tage | — | — |

**Drei besetzte Klassen, und die mittlere trägt zwei Drittel der Bots.**
Genauer gesagt sind es nicht einmal drei getrennte Fenster: die Mediane
verteilen sich auf 2,67 / 3,90 / 4,00 / 4,00 / 5,00 / 6,00 / 7,00 / 14,0 /
21,0 Tage. Zwischen dem ersten und dem siebten liegen **4,3 Tage**. Wer die
Klassengrenze bei 2 statt bei 3 Tagen zieht, hat **sieben von neun** in einem
Fenster.

**Ein Nebenbefund zugunsten des Portfolios:** Das gedrängte Fenster ist
quellenseitig **gemischt** — drei Umkehr-, zwei Muster- und ein Trend-Bot. Es
ist also nicht der schlimmste Fall („sechs Trendfolger im selben Fenster"),
und nach 2.6 ist die Quelle das, worauf es ankommt. Die beiden Paare gleicher
Quelle **innerhalb** des Fensters (`rsi2_crypto`/`turtle_soup_crypto`) sind
dann allerdings genau die, die mit 1,89 – 1,99 × überdurchschnittlich oft
zusammen einsteigen.

### 2.8 Wo wäre eine Lücke?

Aus den Zahlen, ohne Empfehlung:

* **Unter 2 Tagen** steht nur `t3_supertrend`, und auch der nur wegen seiner
  Stop-Quote (53 % der Ausstiege sind Stops nach im Median 1,17 Tagen). Ein
  echter Intraday- oder Ein-Tages-Horizont ist nicht besetzt — er wäre
  allerdings auch mit der Cronjob-Infrastruktur schwer vereinbar (Protokoll
  Abschnitt 3.2, die verworfene 15-Minuten-Fassung).
* **Über 30 Tage ist das Portfolio leer.** Keine der neun Median-Haltedauern
  liegt über 21 Tagen. Der einzige Bot, der überhaupt regelmässig Monate hält,
  ist `elliott_wave_stocks` — und nur in den 20,8 % seiner Trades, die im
  Zeitausstieg enden.
* **Zum Strategie-Katalog, so weit hier belegbar:** Der Katalog mit den
  Kennungen B1 und K1 liegt **nicht im Repo** (geprüft: `docs/`, `research/`
  enthalten unter „K1" nur eine gleichnamige Kausalitätsbedingung aus
  `docs/KONZEPT_sentiment_sammelschicht.md`). Einordnen lässt sich deshalb nur
  die in der Aufgabenstellung genannte Frist:
  * **B1 / ETF-Trend, monatlich** — läge ausserhalb aller neun Mediane und
    wäre damit tatsächlich eine **Horizont**ergänzung, nicht nur eine
    Quellenergänzung.
  * **K1, Wochenfrist** — hier ist Vorsicht geboten. Bedeutet „Wochenfrist"
    eine **Haltedauer** von etwa einer Woche, landet K1 **mitten im
    gedrängten Fenster** (5 bis 7 Tage: dort stehen `rsi2_mean_reversion`,
    `elliott_wave_stocks`, `volatility_breakout_crypto`) und ist gerade
    **keine** Horizontergänzung. Bedeutet es einen **wöchentlichen
    Entscheidungstakt** mit mehrwöchiger Haltedauer, liegt es bei
    `turtle_soup_stocks`/`volatility_breakout`. Welches von beidem gilt, ist
    aus dem Repo nicht zu beantworten.

---

## 3. Belastbarkeit

### 3.1 Pflicht-Gegencheck: rechnet diese Untersuchung dasselbe wie die Bots?

Ja, und das ist belegt statt behauptet.

* **Die Bot-Funktionen werden aufgerufen, nicht nachgebaut.**
  `positionen_holen.py` lädt je Bot dessen `equity_simulation.py` in einem
  **eigenen Prozess** (neun gleichnamige Module kollidieren in `sys.modules`)
  und ruft `load_all_symbol_data` und `collect_all_trades` mit genau den
  Argumenten auf, die der `__main__`-Block des jeweiligen Bots verwendet. Die
  bot-spezifische Argumentzuordnung wird **nicht ein zweites Mal
  hingeschrieben**, sondern aus `research/exposure_messung/bot_lauf.py`
  importiert — inklusive des BTC-Regimefilters, den
  `volatility_breakout_crypto` bewusst erst danach anwendet (im Lauf gemeldet:
  126 von 359 Trades entfernt). Eine zweite Kopie dieser Zuordnung wäre genau
  die Doppelführung aus Prinzip 11.
* **Die Zuordnung „welcher Trade wurde ausgeführt" ist exakt, nicht geraten.**
  Übernommen aus `bot_lauf.py`, weil es keinen zweiten korrekten Weg gibt:
  `simulate_portfolio()` gibt seine Liste der offenen Positionen nicht heraus,
  wird deshalb zweimal mit demselben Trade-Satz aufgerufen — einmal
  unverändert, einmal mit einer Zeilenkennung in der `symbol`-Spalte
  (`AAPL#417`), die dort reine Beschriftung ist. Dass die Kennzeichnung
  Kapitalkurve, Allokationen und Trade-Zahlen unverändert lässt, wird geprüft,
  nicht angenommen; ebenso, dass keine Trade-Zeile doppelt ausgeführt wurde und
  kein Einstieg nach seinem Ausstieg liegt.
* **Die Positionen sind dieselben wie in der Exposure-Messung.** Für **alle
  neun** Bots stimmt der hier erzeugte Positionssatz Zeile für Zeile mit
  `research/exposure_messung/daten/<bot>_positionen.csv` überein (Symbol,
  Ein- und Ausstiegszeit, PnL, Allokation) — gemeldet als
  `"abgleich_exposure_messung": {"identisch": true}` in jeder der neun
  `daten/<bot>_meta.json`. Die ausgeführten Trade-Zahlen (130 / 656 / 392 /
  1.414 / 207 / 395 / 4.232 / 8.915 / 1.454) sind dieselben, die
  `research/exposure_messung/BERICHT.md` veröffentlicht hat. Das ist auch der
  Beleg, dass die neuere pandas-Fassung dieser Umgebung (3.0.5) nichts
  verschoben hat.
* **Gegenproben statt grüner Häkchen.** `test_haltedauer_kern.py` prüft jede
  Behauptung des Rechenkerns in beide Richtungen und verfälscht anschliessend
  den Kern absichtlich (siehe 3.2).

### 3.2 Selbsttests: 51 Prüfungen, alle bestanden

`python3 research/tb24_haltedauern/test_haltedauer_kern.py`

| Abschnitt | Inhalt | Prüfungen |
|---|---|---:|
| 1–11 | Gegenproben auf dem echten Rechenkern | 35 |
| 14 | Live-Weg gegen eine **gebaute** Datenbank (Gegenprobe zu „nichts gefunden") | 5 |
| 12 | **Mutationsproben**: Kern gezielt verfälscht, Prüfreihe muss anschlagen | 10 |
| 13 | Wache: keine Änderung ausserhalb `research/tb24_haltedauern/` und `docs/` | 1 |
| | **gesamt** | **51 von 51** |

Zu den Gegenproben — zu jeder Behauptung ein Fall, in dem dieselbe Prüfung
anschlagen **muss**: zur getrennten Verteilung die überlappende; zum Treffer
bei genau 3 Tagen Abstand der Nicht-Treffer bei 4; zur Überlappung im selben
Titel dieselben Tage in einem **anderen** Titel (100 % Tage, 0 % Titel); zur
Richtung der Überlappung die umgekehrte Richtung (40 % gegen 100 % beim
gleichen Paar); zum positiven Versatz der negative. Kein Erwartungswert ist
aus einem Lauf des Kerns übernommen und wiedererkannt — alle sind von Hand
nachrechenbar konstruiert.

Zu den Mutationsproben: der **Quelltext** des Rechenkerns wird an genau einer
Stelle textlich verfälscht, das veränderte Modul frisch geladen und dieselbe
Prüfreihe darauf angewandt. Jede Ersetzung wird vorher darauf geprüft, dass
sie **genau einmal** zutrifft — eine Mutation, die nichts verändert, würde
sonst als bestandene Probe durchgehen. Alle zehn wurden erkannt:

| Mutation | erkannt von |
|---|---:|
| Haltedauer in Stunden statt Tagen | 2 Prüfungen |
| Ausstiegstag nicht mehr als Positionstag gezählt | 5 |
| Nähe-Fenster um einen Tag zu eng | 3 |
| Vorzeichen des Versatzes gedreht | 3 |
| Histogramm-Klassen rechts statt links geschlossen | 2 |
| Zweigipfligkeit immer bejaht | 1 |
| Grenze der Horizont-Klasse verschoben | 1 |
| Überlappung auf B statt auf A bezogen | 2 |
| Titel-Überlappung rechnet mit Tagen statt Titeln | 1 |
| getrennte Zeiträume gelten als überlappend | 1 |

### 3.3 Der Vorbehalt zur Grundlage

**Die Backtest-Trades entstehen aus Parametern, die nach einem Mass gewählt
wurden, das sich als unbrauchbar erwiesen hat.** Der Vorbehalt gehört benannt,
auch wenn er hier wenig ausmacht — und der Grund dafür ist nicht Zuversicht,
sondern Abschnitt 2.4: die Haltedauern hängen an den **Ausstiegsregeln**, und
bei jedem Bot liegt der obere Gipfel exakt auf der eingestellten Zeitbremse.
Eine andere Parameterwahl würde die **Stop-Quote** verschieben und damit den
Median zwischen den beiden Gipfeln wandern lassen — sie würde die Gipfel selbst
aber nicht verschieben, solange `MAX_HOLD_DAYS` steht.

Konkret heisst das für die Vermutung: sie ist gegen die Parameterwahl **nicht
beliebig robust**. Wäre beispielsweise `turtle_soup_stocks` mit einem Stop
konfiguriert (getestet, verworfen), fiele sein Median von 14 in Richtung des
gedrängten Fensters — die Vermutung würde dann *stärker* zutreffen, nicht
schwächer. Umgekehrt liesse ein weiterer Bot ohne Stop seinen Median auf die
Zeitbremse steigen.

Zwei weitere Punkte gehören dazu:

* **Die Look-Ahead-Korrektur ist berücksichtigt, nicht umgangen.** Gerechnet
  wird mit den heutigen `live_params.py` über die heutigen Bot-Funktionen —
  also auf kausal sauberer Grundlage (Protokoll 3.1). Die Zahlen dieses
  Berichts sind nicht mit denen aus
  `results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md` vergleichbar.
* **`docs/DATENLUECKEN.md` betrifft diese Untersuchung nicht.** Das Register
  hält Lücken der **Forward-Test**-Daten fest. Hier wird kein Forward-Test
  ausgewertet, sondern der Backtest über die CSVs in `data/`. Die Live-Seite,
  für die das Register gelten würde, ist in dieser Umgebung nicht vorhanden
  (2.2) — wer `live_haltedauern.py` auf dem Rechner des Nutzers laufen lässt,
  muss dort zuerst hineinsehen.

### 3.4 Gegenprobe: hängt der Befund am Positionslimit?

Nein. Derselbe Median, einmal über die **ausgeführten** Positionen und einmal
über **alle** gefundenen Trades (also einschliesslich der 8.066, die
`simulate_portfolio()` wegen `MAX_CONCURRENT_POSITIONS` oder fehlendem freien
Kapital übersprungen hat):
(`ergebnisse/gegenprobe_positionslimit.csv`)

| Bot | Median ausgeführt | Median alle | übersprungen | Differenz |
|---|---:|---:|---:|---:|
| `elliott_wave` | 3,90 | 3,90 | 0 | 0,00 |
| `t3_supertrend` | 2,67 | 2,42 | 324 | **0,25** |
| `rsi2_crypto` | 4,00 | 4,00 | 47 | 0,00 |
| `turtle_soup_crypto` | 4,00 | 4,00 | 185 | 0,00 |
| `volatility_breakout_crypto` | 6,00 | 6,00 | 26 | 0,00 |
| `elliott_wave_stocks` | 7,00 | 7,00 | 115 | 0,00 |
| `rsi2_mean_reversion` | 5,00 | 5,00 | 1.159 | 0,00 |
| `turtle_soup_stocks` | 14,00 | 14,00 | 3.154 | 0,00 |
| `volatility_breakout` | 21,00 | 21,00 | **3.056** | 0,00 |

Bei `volatility_breakout` werden zwei Drittel aller Signale übersprungen, und
der Median ändert sich um **null Tage**. Die Kapitalmanagement-Einstellungen
wählen also nicht nach Haltedauer aus. Auch die Zuordnung zu den
Horizont-Klassen bleibt für alle neun Bots unverändert.

### 3.5 Scope-Grenzen — was diese Untersuchung ausdrücklich **nicht** beantwortet

* **Ob die Strategien gut sind.** Gemessen wird, *wann* ein Ergebnis anfällt,
  nicht *ob* es gut ist. Kein Satz dieses Berichts ist ein Renditeurteil.
* **Wie hoch die Korrelation der Ergebnisse ist.** Dafür ist
  `research/exposure_messung/` zuständig (+0,112 mittlere Paarkorrelation zu
  Marktpreisen, bis +0,82 gegen Buy-and-Hold). Hier wird die **Lage** von
  Positionen und Einstiegen gemessen, nicht ihr Ertrag.
* **Ob die Ertragsquellen-Einteilung stimmt.** Sie ist eine **Lesart**, offen
  hingeschrieben in `auswertung.py` (`ERTRAGSQUELLE`), nicht gemessen. Die
  externe Analyse zählt „vier Trendfolge, vier Mean-Reversion"; diese
  Untersuchung zählt drei Trend, vier Umkehr und **zwei Muster** (die beiden
  Elliott-Bots, die der Sache nach gegen den vorherigen Trend handeln, aber
  weder einen Mittelwert-Rücklauf noch eine Ausbruchsfortsetzung). Die
  Abweichung ist benannt, nicht aufgelöst. **Die Befunde aus 2.6 hängen
  daran:** stellte man die beiden Elliott-Bots zu „Umkehr", wanderten die acht
  „Muster + Umkehr"-Paare in die Gruppe „gleiche Quelle" und senkten deren
  Median von 1,94 auf etwa 1,5 — die Richtung des Befundes bliebe, die Höhe
  nicht.
* **Wie belastbar der Quellen-Befund ist.** Die Gruppe „gleiche Quelle" besteht
  aus **drei** ungeordneten Paaren (`rsi2_mean_reversion`/`turtle_soup_stocks`,
  `rsi2_crypto`/`turtle_soup_crypto`, `t3_supertrend`/`volatility_breakout_crypto`).
  Alle drei zeigen in dieselbe Richtung und der Abstand zur Gegengruppe ist
  gross (1,68 – 3,27 gegen 0,15 – 0,93 bei Trend+Umkehr), aber drei Paare sind
  drei Paare. Mehr Bots gleicher Quelle in derselben Anlageklasse gibt es
  nicht, und mit neun Bots wird es auch nicht mehr.
* **Die Live-Seite.** Nicht gemessen, weil nicht vorhanden und zu dünn (2.2).
  `live_haltedauern.py` liegt bereit.
* **Warum ein Versatz auftritt.** Gemessen ist der Versatz, nicht seine
  Ursache (2.6).
* **Was daraus folgt.** Keine Empfehlung ist umgesetzt, keine Parameter sind
  angefasst.

### 3.6 Nebenbefund: die Zeitbremse von `elliott_wave_stocks`, in Zahlen

Beim Anbringen der Zeitbremsen-Tabelle in 2.4 aufgefallen, ausdrücklich **kein
Fehler** und **nicht angefasst**:

`elliott_wave_stocks/backtest_elliott.py:70` bremst nach `MAX_HOLD_HOURS = 90`
**Tagesbalken**, `elliott_wave_stocks/forward_test.py:51` nach
`MAX_HOLD_DAYS = 130` **Kalendertagen** — mit dem Kommentar „entspricht ~90
Handelstagen". Die Näherung ist als Näherung gekennzeichnet; jetzt ist sie
beziffert: die 82 Zeitausstiege des Backtests liegen bei **128 bis 134**
Kalendertagen (Median 131, Q1 129, Q3 132). Eine Live-Bremse bei 130 Tagen
schneidet also je Trade bis zu **4 Tage früher** oder **2 Tage später** als die
Backtest-Regel. Bei einer Haltedauer von vier Monaten ist das wenig, und der
Sync-Check kann es nicht sehen, weil die beiden Grössen verschieden sind
(Balken gegen Kalendertage) und nicht gekoppelt werden können.

Die sechs Bots mit `MAX_HOLD_DAYS` in `live_params.py` sind davon **nicht**
betroffen: ihre `forward_test.py` zählt jeweils Balken über die Kursreihe
(`if offset + 1 >= MAX_HOLD_DAYS`), also genau wie ihr Backtest — geprüft für
alle sechs. `elliott_wave` (Krypto) ebenfalls nicht: 240 Stundenbalken sind
bei durchlaufenden Krypto-Kerzen exakt 240 Stunden, und `forward_test.py`
rechnet mit `timedelta(hours=240)`.

---

## 4. Reproduktion

```bash
# 1. Positionen aus dem echten Bot-Code holen (neun Prozesse, ca. 4 Minuten)
python3 research/tb24_haltedauern/alle_bots.py

# 2. Auswertung: alle Tabellen nach ergebnisse/ (ca. 1 Minute)
python3 research/tb24_haltedauern/auswertung.py

# 3. Selbsttests mit Gegen- und Mutationsproben (51 Pruefungen)
python3 research/tb24_haltedauern/test_haltedauer_kern.py

# 4. Live-Seite (nur auf dem Rechner des Nutzers sinnvoll)
python3 research/tb24_haltedauern/live_haltedauern.py

# 5. Nachweis, dass nichts ausserhalb angefasst wurde
git diff origin/main HEAD --name-only
git status --porcelain
```

Einzelne Bots: `python3 research/tb24_haltedauern/alle_bots.py elliott_wave t3_supertrend`.

**Zur Umgebung.** In dieser Cloud-Umgebung fehlen `pandas`, `numpy`, `scipy`,
`yfinance`, `binance` und `fastapi` im System-Python. Das ist **vorbestehend**
und mit einem Basislauf auf unverändertem `main` nachgewiesen:

```
$ python3 -c "import pandas"                                  # unveraendertes main
ModuleNotFoundError: No module named 'pandas'
$ python3 research/exposure_messung/bot_lauf.py elliott_wave   # unveraenderte main-Datei
  File ".../research/exposure_messung/bot_lauf.py", line 53, in <module>
    import pandas as pd
ModuleNotFoundError: No module named 'pandas'
```

Gerechnet wurde deshalb in einer venv mit `pandas` und `numpy` (nur diese
beiden werden gebraucht; `scipy` bewusst nicht — die Zweigipfligkeit ist ohne
Verteilungsannahme gemessen). `yfinance` und `binance` werden nicht gebraucht:
die Bot-Module werden mit den Stubs aus `bot_lauf.py` geladen und lesen
ausschliesslich die vorhandenen CSVs unter `data/`. Auf dem Rechner des
Nutzers (`trading-env`, Python 3.9.6) läuft alles ohne diesen Zwischenschritt.

---

## 5. Dateien

| Datei | Zweck |
|---|---|
| `positionen_holen.py` | ein Bot, ein Prozess: Positionen mit Ausstiegsart und **gezählter** Kerzenzahl aus dem echten Bot-Code; Abgleich gegen `research/exposure_messung/` |
| `alle_bots.py` | alle neun Bots nacheinander |
| `haltedauer_kern.py` | Rechenkern: Haltedauern, Verteilungsform, Überlappung, Nähe, Versatz, Horizont-Klassen |
| `auswertung.py` | schreibt alle Tabellen nach `ergebnisse/` |
| `live_haltedauern.py` | Live-Seite aus den Bot-Datenbanken, schreibgeschützt (`mode=ro`) |
| `test_haltedauer_kern.py` | 51 Prüfungen: Gegenproben, Live-Weg gegen eine gebaute Datenbank, 10 Mutationsproben, Repo-Wache |
| `daten/<bot>_positionen.csv` | ausgeführte Positionen je Bot |
| `daten/<bot>_alle_trades.csv` | alle gefundenen Trades je Bot, mit Spalte `ausgefuehrt` |
| `daten/<bot>_meta.json` | Parameter, Trade-Zahlen, Ausstiegsarten, Abgleichergebnis |
| `ergebnisse/haltedauern_je_bot.csv` | Tabelle aus 2.3 |
| `ergebnisse/haltedauern_je_ausstiegsart.csv` | Tabelle aus 2.4 |
| `ergebnisse/haltedauern_histogramm.csv` | Verteilung in 12 Klassen je Bot |
| `ergebnisse/verteilungsform.csv` | ein- oder zweigipflig, mit Begründung je Bot |
| `ergebnisse/gegenprobe_positionslimit.csv` | Tabelle aus 3.4 |
| `ergebnisse/ueberlappungsmatrix.csv` | 72 geordnete Paare, Tage und Titel |
| `ergebnisse/naehe_der_einstiege.csv` | 32 Paare gleicher Anlageklasse, mit Zufallsvergleich |
| `ergebnisse/versatz_der_einstiege.csv` | Versatz-Verteilung je Paar |
| `ergebnisse/zusammenfassung.json` | maschinenlesbare Kurzfassung samt Datenbasis |

---

## 6. Was aus dem Ergebnis folgen könnte — benannt, nicht ausgeführt

Ohne Empfehlung und ohne Umsetzung, als Anschlussfragen für den Nutzer:

1. **Eine Horizont-Dimension bewusst wählen statt einstellen.** Die
   Zeitbremsen der sieben Tages-Bots liegen alle bei 10 oder 15 Balken. Jede
   ist einzeln validiert; keine wurde je gegen die anderen sechs gesetzt. Die
   Frage „welcher Horizont fehlt dem Portfolio" ist nie gestellt worden —
   sie wäre eine Optimierung auf Portfolio-Ebene, und das Projekt hat bisher
   ausschliesslich je Bot optimiert.
2. **Den Quellen-Befund aus 2.6 als Aufnahmekriterium prüfen.** Der
   Nähe-Überschuss gegen Zufall ist mit vorhandenen Daten für jeden
   Kandidaten vor seiner Aufnahme berechenbar — er braucht keine Live-Historie,
   nur Backtest-Trades. Ob das ein sinnvolles Kriterium ist, ist offen.
3. **Bei K1 zuerst die Haltedauer klären, dann den Takt** (2.8). Ein Kandidat
   mit einer Woche Haltedauer ist keine Horizontergänzung.
4. **Das Kriterium aus Protokoll 9.4 kann sich auf diese Zahlen stützen.** Für
   `elliott_wave_stocks` ist der Prüftermin Oktober 2026 / Januar 2027 auf
   „gleiche Zeit im Markt gegen das 95. Perzentil von Zufalls-Timing"
   festgelegt. Dieser Bericht liefert dazu die Haltedauer-Verteilung, die eine
   solche Zufalls-Ziehung braucht (Median 7 Tage, zweigipflig: 79,2 % Stops bei
   5 Tagen, 20,8 % Zeitausstiege bei 131 Tagen) — eine Ziehung mit einer
   einzigen mittleren Haltedauer träfe den Bot nicht.
