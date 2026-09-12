# Was misst der kombinierte Drawdown von −1,43 %?

**Status: reine Untersuchung. KEINE Änderung an Bot-, Backtest- oder
Live-Dateien.** Alle Dateien liegen ausschliesslich unter
`research/exposure_messung/`; `git diff origin/main HEAD --name-only` listet
nichts anderes. Es wird **keine Empfehlung umgesetzt** — was aus den Zahlen
folgt, entscheidet der Nutzer.

---

## 1. Die Antwort zuerst

**Der Verdacht trifft teilweise zu — aber nicht aus dem genannten Grund.**

Gemessen an der vorab festgelegten Entscheidungsschwelle fällt das Ergebnis in
die **mittlere Zeile**, und zwar für beide Zusammenstellungen:

| | mittlere Brutto-Exposure | Exposure 2022 | Tage ohne Position | Schwelle sagt |
|---|---|---|---|---|
| ursprüngliche **vier** Bots | **25,85 %** | 23,10 % | **0 von 1.794** | dazwischen |
| heutige **neun** Bots | **37,91 %** | 31,09 % | **0 von 1.618** | dazwischen |

Weder ist die mittlere Brutto-Exposure unter 20 % (das wäre „Verdacht
bestätigt"), noch erreicht sie 40 % bei gleichzeitig winzigem Drawdown (das
wäre „widerlegt").

**Die konkrete Vermutung — „das gemeinsame Buch besteht die meiste Zeit
überwiegend aus Kasse" — ist falsch.** Das Neuner-Buch war an **keinem
einzigen** der 1.618 Tage flach, und an keinem einzigen Tag unter 10 %
Exposure; das kleinste Monatsmittel über die gesamte Messung liegt bei
27,1 %. Das Buch ist dauerhaft investiert.

**Die Schlussfolgerung — „−1,43 % ist keine Risikokennzahl" — stimmt
trotzdem**, aus drei anderen, gemessenen Gründen:

1. **Die Zahl ist veraltet.** Dieselbe Formel, dieselben vier Bots, aber mit
   den heutigen `live_params.py` gerechnet, ergibt **−9,41 %** statt −1,43 %.
   Die abgelegten `results/*/equity_curve.csv`, aus denen −1,43 % stammt,
   beschreiben bei **fünf von neun** Bots nicht mehr den Bot, der heute läuft.
2. **Der Nenner ist tatsächlich falsch — nur anders als vermutet.** Nicht
   „Kasse statt Risiko", sondern „Gesamtkapital statt eingesetztem Kapital".
   Dasselbe Vierer-Buch verliert, gemessen am jeweils **investierten**
   Kapital, **−32,12 %**.
3. **Der Korrelationsbefund, auf dem die Diversifikations-These ruht, ist ein
   Messartefakt.** Die Kapitalkurve eines Bots bewegt sich nur an
   Ausstiegstagen. Zwei überwiegend aus Nullen bestehende Reihen korrelieren
   mechanisch nahe null. Bewertet man dieselben Bots täglich zu
   Marktpreisen, tritt genau das gemeinsame Beta hervor, das der Einwand
   vermutet: bis **+0,82** gegen einen gleichgewichteten Buy-and-Hold.

Und der Grund, warum die kombinierte Zahl überhaupt kleiner ist als der
schlechteste Einzelbot, ist zum grössten Teil **Gewichtung, nicht
Kompensation**: bei 1/N-Gewichtung trägt ein Bot mit −32 % nur mit −3,6 % zum
Buch bei. Der mittlere Einzel-Bot-Drawdown im Neuner-Fenster beträgt
−17,93 %, das kombinierte Buch −11,47 %. Das ist ein realer, aber
gewöhnlicher Diversifikationseffekt — nicht der Sprung von −22,20 % auf
−1,43 %.

---

## 2. Entscheidungsgrundlage

### Datenbasis

Alle neun Bots, jeweils mit dem **unveränderten Original-Trade-Satz** aus
ihrem eigenen `equity_simulation.py` und den heutigen `live_params.py`.

| Bot | ausgeführte Trades | Symbole | erster Einstieg | letzter Ausstieg | Allokation | Limit |
|---|---:|---:|---|---|---:|---:|
| `elliott_wave` | 130 | 18 | 2021-09-22 | 2026-08-20 | 10 % | – |
| `t3_supertrend` | 656 | 18 | 2021-09-01 | 2026-08-29 | 10 % | 5 |
| `elliott_wave_stocks` | 395 | 127 | 2016-10-28 | 2026-09-01 | 10 % | 8 |
| `rsi2_mean_reversion` | 4.232 | 147 | 2016-09-01 | 2026-09-01 | 5 % | 20 |
| `rsi2_crypto` | 392 | 18 | 2022-02-11 | 2026-08-20 | 10 % | 8 |
| `turtle_soup_crypto` | 1.414 | 20 | 2021-10-12 | 2026-08-28 | 10 % | 8 |
| `turtle_soup_stocks` | 8.915 | 147 | 2016-09-01 | 2026-09-01 | 2 % | – |
| `volatility_breakout` | 1.454 | 147 | 2016-09-01 | 2026-09-01 | 10 % | 15 |
| `volatility_breakout_crypto` | 207 | 19 | 2022-03-17 | 2026-08-30 | 10 % | 8 |

Zusammen **17.795 ausgeführte Positionen**. Kursdaten aus `data/`,
unvollständige Kerzen über `shared/kursdaten.py` gestrichen und gezählt
(gemeldet: 1 Kerze, `APH` — der bekannte Fall aus Protokoll 3.3).

### Pflicht-Gegencheck: rechnet diese Untersuchung dasselbe wie die Bots?

Ja, und das ist belegt statt behauptet.

* **Die Bot-Funktionen werden aufgerufen, nicht nachgebaut.** `bot_lauf.py`
  importiert je Bot dessen `equity_simulation.py` in einem **eigenen Prozess**
  (neun gleichnamige Module kollidieren in `sys.modules`) und ruft
  `load_all_symbol_data`, `collect_all_trades`, `simulate_portfolio` und
  `calculate_max_drawdown` mit genau den Argumenten auf, die der
  `__main__`-Block des jeweiligen Bots verwendet — inklusive des
  BTC-Regimefilters, den `volatility_breakout_crypto` bewusst erst danach
  anwendet. Vorbild: `shared/portfolio_overview.py` (Subprozess je Bot) und
  `research/order_sensitivity/run_one_bot.py` (Argumentzuordnung, Stubs).
* **Die ursprüngliche Zahl wird exakt reproduziert.** `auswertung.py` rechnet
  −1,43 % aus den abgelegten Kurven nach, nach der Methodik von
  `strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py`:
  Ergebnis **−1,43 %**, auf die zweite Nachkommastelle. Ohne diesen
  Nachweis wäre nicht belegt, dass hier dieselbe Grösse untersucht wird.
* **Die Zuordnung „welcher Trade wurde ausgeführt" ist exakt, nicht
  geraten.** `simulate_portfolio()` gibt seine interne Liste der offenen
  Positionen nicht heraus. Statt die Funktion nachzubauen, wird sie zweimal
  mit demselben Trade-Satz aufgerufen: einmal unverändert, einmal mit einer
  Trade-Tabelle, deren `symbol`-Spalte um die Zeilennummer ergänzt ist
  (`AAPL#417`). `symbol` ist dort reine Beschriftung — jede Rechnung hängt an
  `pnl_pct`. Geprüft wird, dass beide Läufe in Kapitalkurve, Allokationen und
  Trade-Zahlen **identisch** sind; erst dann wird die Kennzeichnung
  ausgelesen. Zusätzlich wird geprüft, dass keine Zeile doppelt ausgeführt
  wurde und kein Einstieg nach seinem Ausstieg liegt.
* **Gegenproben statt grüner Häkchen.** `test_exposure_kern.py` prüft jede
  Behauptung des Rechenkerns in beide Richtungen (Prinzip 12): zum flachen
  Buch gehört das dauerhaft volle, zum „−2 % am Gesamtkapital sind −20 % am
  eingesetzten" gehört der Fall, in dem beide Masse dasselbe sagen müssen.
  23 Prüfungen, alle bestanden.

### Scope-Grenzen — was diese Untersuchung ausdrücklich **nicht** beantwortet

* Ob die Strategien gut sind. Gemessen wird, **was die Kennzahl misst**, nicht
  ob die Bots taugen.
* **Survivorship-Bias im Aktienuniversum** (Top 150 nach *heutiger*
  Marktkapitalisierung). Er ist im Projekt bekannt und dokumentiert
  (Protokoll 3.3 und Prinzip 7.3); er wirkt auf alle vier Aktien-Bots und auf
  die Buy-and-Hold-Referenz gleichermassen. Hier nur benannt, nicht
  untersucht — das ist eine eigene Aufgabe.
* **Look-ahead in adjustierten Kursen** und **Fill-Annahmen**. Ebenfalls nur
  benannt. Der bekannte Look-Ahead-Fund betrifft die Elliott-Bots und ist
  behoben (`research/elliott_wave_lookahead/`).
* **Forward-Test-Daten.** Alles hier ist Backtest. Stand 12.09.2026 liegen
  alle neun Bots unter `MIN_LIVE_CLOSED_TRADES = 10` (Protokoll 4.3b), es gibt
  also gar keine belastbare Live-Alternative. `docs/DATENLUECKEN.md` ist
  deshalb für diese Messung ohne Belang — sie enthält keine Forward-Test-Zahl.
* **Keine Parameteränderung, keine Neubewertung von Entscheidungen.**

### Berührung mit der parallel laufenden Untersuchung

Es läuft eine zweite Untersuchung zur Drawdown-Reihenfolge in
`multi_symbol_optimise` (Symbol-Blöcke gegen chronologisch). **Diese Messung
ist davon nicht betroffen**: `simulate_portfolio()` sortiert seine Ereignisse
ausdrücklich chronologisch (`events.sort(key=lambda e: (e[0], e[1] != "exit"))`),
und alle Zahlen hier stammen aus dieser Funktion. Der Exposure-Verlauf ist
damit der chronologische — der, der einen erlebbaren Verlauf beschreibt.
Berührt ist nur, **welcher** Trade bei gleichzeitigen Signalen einen
knappen Platz bekommt; dazu siehe `research/order_sensitivity/`.

### Reproduktion

```bash
cd research/exposure_messung
python3 test_exposure_kern.py     # 23 Prüfungen mit Gegenproben
python3 alle_bots.py              # neun Bots, je ein Prozess  (~6 min)
python3 auswertung.py             # alle Zahlen dieses Berichts (~3 min)
```

Benötigt `pandas` und `numpy`. Ergebnisse landen unter `ergebnisse/`,
Zwischenstände unter `daten/`. Nichts davon schreibt ausserhalb des eigenen
Ordners.

---

## 3. Was hier „Exposure" heisst — und warum die Definition wichtig ist

```
Brutto-Exposure(Tag) = Summe der Positionsgrössen aller an diesem Kalendertag
                       offenen Positionen
                       ────────────────────────────────────────────────────
                       angenommenes Gesamtkapital zu Beginn des Tages
```

Drei Festlegungen, ohne die die Zahl nicht lesbar ist:

1. **Die Positionsgrössen sind Backtest-Annahmen, kein getracktes Kapital.**
   Sie entstehen in `simulate_portfolio()` als `kapital * ALLOCATION_PCT` —
   2 % bis 10 % je Bot aus `live_params.py`. Es gibt im Projekt bewusst **kein
   gemeinsames Kapitalkonto** (Protokoll 2 und 8); „Gesamtkapital" ist
   deshalb ebenfalls eine Annahme, nämlich die hypothetische
   Gleichgewichtung. Die Zahl beschreibt, wie viel Kapital ein so
   aufgesetztes Buch **binden würde**, nicht wie viel gebunden **ist**.
2. **Kalendertage, nicht Handelstage.** Eine Position, die Freitag offen ist
   und Montag schliesst, trägt das Wochenendrisiko. Wer Wochenenden
   herausrechnet, misst die Exposure der Aktien-Bots systematisch zu hoch.
3. **Der Nenner ist das Kapital zu Tagesbeginn.** Sonst teilte man die am
   Morgen eingegangene Bindung durch ein Kapital, das die Gewinne desselben
   Tages schon enthält. (Nebeneffekt: die Exposure kann kurzzeitig über
   100 % liegen — gemessen 100,21 % beim Aktien-Buch —, wenn Positionen zu
   einem höheren Kapitalstand eröffnet wurden, als am Messtag gilt.)

Die gleichgewichtete Zusammenfassung entspricht genau der ursprünglichen
Rechnung: jede Bot-Kurve auf ihren Stand zu Fensterbeginn normiert, Gewicht
1/N, danach **kein** Umschichten.

---

## 4. Frage 1: Brutto-Exposure des Gesamtbuchs

| | vier Bots (Original) | neun Bots (heute) | vier Aktien-Bots |
|---|---:|---:|---:|
| Fenster | 2021-09-22 … 2026-08-20 | 2022-03-17 … 2026-08-20 | 2016-10-28 … 2026-09-01 |
| Kalendertage | 1.794 | 1.618 | 3.596 |
| **Mittel** | **25,85 %** | **37,91 %** | **61,19 %** |
| Median | 25,50 % | 38,03 % | 61,38 % |
| 10. Perzentil | 13,08 % | 26,35 % | 43,74 % |
| 90. Perzentil | 38,72 % | 48,59 % | 78,89 % |
| Maximum | 61,84 % | 68,46 % | 100,21 % |
| **Tage mit null Positionen** | **0** (0,00 %) | **0** (0,00 %) | **0** (0,00 %) |
| Tage unter 10 % Exposure | 83 (4,6 %) | **0** | 2 (0,1 %) |
| Tage über 50 % Exposure | 1,56 % | 7,05 % | 79,84 % |

**Der Verlauf** (Jahresmittel der Monatsmittel, Neuner-Buch; die vollständige
Tages- und Monatsreihe liegt als CSV bei):

| 2022 | 2023 | 2024 | 2025 | 2026 |
|---:|---:|---:|---:|---:|
| 31,3 % | 38,9 % | 38,6 % | 38,7 % | 42,7 % |

Kein Monatsmittel der gesamten Messung liegt unter 27,1 % oder über 51,0 %.
Das Buch ist weder zeitweise flach noch schwankt es zwischen den Extremen —
es ist **durchgehend zu rund einem Drittel investiert**.

**Die einzelnen Bots sind sehr wohl oft flach — das gemeinsame Buch nie.**
Genau hier liegt der Denkfehler, der die Vermutung nahegelegt hat:

| Bot | Zeit im Markt | mittlere Exposure | Ø Positionen, wenn offen | max. Positionen |
|---|---:|---:|---:|---:|
| `elliott_wave` | 21,3 % | 3,8 % | 1,8 | 7 |
| `volatility_breakout_crypto` | 34,2 % | 10,8 % | 3,2 | 9 |
| `rsi2_crypto` | 45,2 % | 12,2 % | 2,7 | 9 |
| `t3_supertrend` | 56,5 % | 18,2 % | 3,2 | 8 |
| `rsi2_mean_reversion` | 90,7 % | 39,3 % | 8,7 | 26 |
| `turtle_soup_crypto` | 92,9 % | 48,2 % | 5,2 | 15 |
| `elliott_wave_stocks` | 95,4 % | 47,6 % | 5,1 | 9 |
| `volatility_breakout` | 99,4 % | 84,0 % | 8,5 | 14 |
| `turtle_soup_stocks` | 100,0 % | 79,5 % | 39,8 | 63 |

(Neuner-Fenster. „mittlere Exposure" ist hier die Exposure **des jeweiligen
Bots am eigenen Kapital**, nicht sein Beitrag zum Gesamtbuch.)

Vier Bots sind die meiste Zeit flach, vier praktisch immer investiert. Neun
solche Bätter übereinandergelegt ergeben ein Buch, das nie Pause macht.

---

## 5. Frage 2: Exposure unter Stress

| Zeitraum | vier Bots | neun Bots | vier Aktien-Bots |
|---|---:|---:|---:|
| Corona-Einbruch (Feb–Apr 2020) | *nicht messbar* | *nicht messbar* | **36,17 %** |
| Gesamtjahr 2022 | 23,10 % | 31,09 % | 58,58 % |
| 10 % schlechteste B&H-Tage (Aktien) | 26,97 % | 38,08 % | 61,00 % |
| 10 % schlechteste B&H-Tage (Krypto) | 25,44 % | 38,45 % | 64,65 % |
| Anteil flacher Tage in jedem dieser Fenster | 0,0 % | 0,0 % | 0,0 % |

**Februar bis April 2020 ist für das gemeinsame Buch nicht messbar** — die
Krypto-Kursdaten des Projekts beginnen im September 2021, das gemeinsame
Fenster kann 2020 gar nicht enthalten. Deshalb ist die Gruppe der **vier
Aktien-Bots** zusätzlich gerechnet: sie reicht bis 2016 zurück und deckt 2020
und 2022 ab. Dort sank die Exposure im Corona-Quartal von 61,2 % (Mittel) auf
36,2 % — das Buch hat spürbar abgebaut, war aber weiter zu gut einem Drittel
im Markt. Im Bärenjahr 2022 blieb es bei 58,6 %, praktisch unverändert.

**An den schlechtesten Tagen ist die Exposure nicht niedriger als sonst,
sondern etwas höher** (38,1 % bzw. 38,5 % gegen 37,9 % im Mittel). Das Buch
weicht dem Stress nicht aus. Der Satz aus der Aufgabenstellung — „ein Buch,
das im Stress flach ist, hat keinen Drawdown, aber auch keine Absicherung
geleistet" — beschreibt dieses Buch **nicht**: es ist im Stress voll dabei.

Die Dezilgrenzen werden **innerhalb des jeweiligen Messfensters** bestimmt.
Ein Dezil aus der vollen Kurshistorie (Aktien: ab 1962) beschriebe eine andere
Marktphase als die gemessene.

---

## 6. Frage 3: Drawdown auf investiertem Kapital

Die zweite Kapitalkurve enthält nur Tage mit offenen Positionen und misst die
Veränderung am **tatsächlich gebundenen** Kapital statt am Gesamtkapital:
`r(Tag) = Kapitalveränderung(Tag) / gebundenes Kapital(Tag)`, verkettet.

| | vier Bots | neun Bots | vier Aktien-Bots |
|---|---:|---:|---:|
| ursprünglich berichtet | **−1,43 %** | – | – |
| am Gesamtkapital, heutige Parameter | −9,41 % | −11,47 % | −17,54 % |
| **am investierten Kapital** | **−32,12 %** | **−27,28 %** | **−30,30 %** |
| zusätzlich: zu Marktpreisen bewertet | −10,12 % | −13,80 % | −19,07 % |
| zum Vergleich: mittlerer Einzel-Bot-DD | −16,32 % | −17,93 % | −24,31 % |
| zum Vergleich: schlechtester Einzel-Bot | −22,20 % | −31,91 % | −29,79 % |

**Das ist die eigentliche Antwort.** Der Unterschied zwischen −1,43 % und
−32,12 % zerfällt in zwei sauber getrennte Teile:

* **−1,43 % → −9,41 %** ist *Veralterung*: dieselbe Formel, aber die heutigen
  Parameter (Abschnitt 7).
* **−9,41 % → −32,12 %** ist *der Nenner*: derselbe Verlust, einmal am ganzen
  Buch gemessen, einmal an dem Teil davon, der im Markt war.

Die dritte Zeile („zu Marktpreisen") beantwortet einen Einwand, der sonst
offen bliebe: die Kapitalkurve der Bots kennt **nur realisierte** Gewinne —
eine offene Position steht bis zum Ausstieg zum Einstandswert, ihr
Buchverlust ist unsichtbar. Bewertet man alle offenen Positionen täglich zu
Schlusskursen, vertieft sich der Drawdown um 0,7 bis 2,3 Prozentpunkte. Das
ist real, aber **nicht** die Erklärung für die Lücke. *(Näherung: als
Bezugspunkt dient der Schlusskurs des Einstiegstages, auch bei den beiden
Bots auf Stunden- bzw. 4-Stunden-Kerzen; am Ausstiegstag wird der tatsächlich
realisierte Wert eingesetzt. Die Naht dazwischen beträgt im Median 0,3
Prozentpunkte, im 90. Perzentil 0,9 bzw. 2,0.)*

**Und der Rest ist Gewichtung, nicht Kompensation.** Bei 1/N-Gewichtung
schlägt ein Bot mit −31,9 % nur mit −3,5 % aufs Buch durch. Der mittlere
Einzel-Bot-Drawdown von −17,93 % ist die Grösse, gegen die man −11,47 %
halten sollte — nicht der schlechteste Einzelbot. Diversifikation bringt hier
also rund 6 Prozentpunkte; der Vergleich „−22,20 % gegen −1,43 %" hat nie
zwei vergleichbare Grössen nebeneinandergestellt.

---

## 7. Der Befund, der nicht bestellt war: fünf von neun abgelegten Kurven sind veraltet

Die −1,43 % stammen aus vier `results/*/equity_curve.csv`. Diese Dateien
werden nur geschrieben, wenn jemand `python3 equity_simulation.py` von Hand
aufruft. Rechnet man sie mit den **heutigen** `live_params.py` neu:

| Bot | Zeilen abgelegt | Zeilen neu | identisch? | Allokation | Limit |
|---|---:|---:|:---:|---:|---:|
| `elliott_wave` | 144 | 130 | **nein** | 10 % | – |
| `t3_supertrend` | 656 | 656 | ja | 10 % | 5 |
| `elliott_wave_stocks` | 469 | 395 | **nein** | 10 % | 8 |
| `rsi2_mean_reversion` | 2.641 | 4.232 | **nein** | 5 % | 20 |
| `rsi2_crypto` | 392 | 392 | ja | 10 % | 8 |
| `turtle_soup_crypto` | 1.414 | 1.414 | ja | 10 % | 8 |
| `turtle_soup_stocks` | 1.887 | 8.915 | **nein** | 2 % | – |
| `volatility_breakout` | 1.236 | 1.454 | **nein** | 10 % | 15 |
| `volatility_breakout_crypto` | 207 | 207 | ja | 10 % | 8 |

Bei `rsi2_mean_reversion` ist die Ursache im Code dokumentiert: die abgelegte
Kurve stammt aus der Zeit **vor** der Sync-Korrektur (10 % Allokation und
Limit 8 statt der Live-Werte 5 % und 20; siehe Kommentarblock in
`strategies/rsi2_mean_reversion/equity_simulation.py`). Die Sync-Reihe hat den
**Code** in Ordnung gebracht — die daneben liegenden **Ergebnisdateien** hat
sie nicht mit erneuert, und sie werden weiterhin gelesen: von
`portfolio_correlation_analysis.py`, und laut Protokoll 4.3b auch von
`shared/portfolio_overview.py`, also von der Montags-Mail und der
Dashboard-Portfolio-Sicht.

Dieselbe Formel auf frisch gerechnete Kurven angewandt:

| | abgelegte Kurve | heutige `live_params.py` |
|---|---:|---:|
| `elliott_wave` | −0,23 % | **−10,17 %** |
| `t3_supertrend` | −22,20 % | −22,20 % |
| `elliott_wave_stocks` | −1,65 % | **−21,16 %** |
| `rsi2_mean_reversion` | −12,72 % | −11,73 % |
| **kombiniert (25/25/25/25)** | **−1,43 %** | **−9,41 %** |

Einzeltausch zeigt, woher die Verschiebung kommt: nur `elliott_wave_stocks`
getauscht → −4,93 %, nur `elliott_wave` → −2,66 %, die beiden anderen ändern
nichts (−1,43 %). Die beiden Elliott-Bots sind es, deren abgelegte Kurven mit
−0,23 % und −1,65 % so aussergewöhnlich flach waren, dass sie das kombinierte
Ergebnis getragen haben — und beide sind genau die Bots, deren Zahlen durch
die Look-Ahead-Korrektur (PR #26) Geschichte wurden.

---

## 8. Frage 4: je Bot — echte Kompensation oder blosse Nichtüberlappung?

**Weder noch: es gibt schlicht keine Tage, an denen die anderen acht flach
sind.**

| Bot | Zeit im Markt | eigener Max-DD im Fenster | DD-Phase | Anteil der Tage, an denen alle anderen flach waren | davon getragener Verlustanteil |
|---|---:|---:|---|---:|---:|
| `elliott_wave` | 21,3 % | −10,17 % | 2022-03-24 … 2022-11-17 | 0,00 % | 0,00 % |
| `t3_supertrend` | 56,5 % | −22,20 % | 2022-04-03 … 2023-10-19 | 0,00 % | 0,00 % |
| `elliott_wave_stocks` | 95,4 % | −16,23 % | 2022-03-17 … 2022-10-11 | 0,00 % | 0,00 % |
| `rsi2_mean_reversion` | 90,7 % | −8,60 % | 2023-08-01 … 2023-10-04 | 0,00 % | 0,00 % |
| `rsi2_crypto` | 45,2 % | −13,30 % | 2024-03-16 … 2024-10-04 | 0,00 % | 0,00 % |
| `turtle_soup_crypto` | 92,9 % | −31,91 % | 2024-12-10 … 2025-04-09 | 0,00 % | 0,00 % |
| `turtle_soup_stocks` | 100,0 % | −18,71 % | 2022-03-30 … 2022-10-12 | 0,00 % | 0,00 % |
| `volatility_breakout` | 99,4 % | −23,97 % | 2022-04-11 … 2022-10-19 | 0,00 % | 0,00 % |
| `volatility_breakout_crypto` | 34,2 % | −16,29 % | 2022-04-07 … 2023-11-02 | 0,00 % | 0,00 % |

An **keinem** der 1.618 Tage waren acht von neun Bots gleichzeitig flach —
`turtle_soup_stocks` ist an 100 % der Tage im Markt, `volatility_breakout` an
99,4 %. Die Frage „fiel der Drawdown eines Bots auf Tage, an denen die
anderen flach waren" hat deshalb dieselbe Antwort für alle neun: nein, weil
es solche Tage nicht gibt. Im **Vierer**-Fenster, in dem
`elliott_wave_stocks` an 2,2 % der Tage allein im Markt war, trug es dort
3,5 % seines Drawdowns; bei den Aktien-Bots erreicht `turtle_soup_stocks`
6,5 % an 0,08 % der Tage. Grössenordnung: vernachlässigbar.

Was den kombinierten Drawdown klein hält, ist also **nicht** zeitliche
Nichtüberlappung. Es ist, dass die tiefsten Phasen der Bots in
**verschiedenen Jahren** liegen (2022 für fünf Bots, 2023, 2024 und
2024/25 für je einen) — plus die 1/N-Gewichtung.

---

## 9. Frage 5: Konzentration

**Gleichzeitig offene Positionen im Neuner-Buch** (Perzentile über 1.618
Tage):

| 10. | 25. | 50. | 75. | 90. | 99. |
|---:|---:|---:|---:|---:|---:|
| 44 | 59 | **72** | 83 | 92 | 103 |

Das Buch hält im Median **72 Positionen gleichzeitig**. Davon kommen im
Schnitt knapp 40 von `turtle_soup_stocks` allein (2 % Allokation, kein
Positionslimit — bewusst so entschieden, Protokoll 3.4).

**Titelüberlappung — halten zwei Bots dasselbe Symbol gleichzeitig?**

| Bot A | Bot B | max. gleiche Symbole | Tage mit Überlappung | Anteil Tage |
|---|---|---:|---:|---:|
| `rsi2_mean_reversion` | `turtle_soup_stocks` | **19** | 1.284 | **79,4 %** |
| `turtle_soup_stocks` | `volatility_breakout` | 9 | 1.181 | 73,0 % |
| `rsi2_crypto` | `turtle_soup_crypto` | 7 | 420 | 26,0 % |
| `elliott_wave_stocks` | `turtle_soup_stocks` | 5 | 1.058 | 65,4 % |
| `t3_supertrend` | `turtle_soup_crypto` | 5 | 442 | 27,3 % |
| `elliott_wave` | `turtle_soup_crypto` | 5 | 143 | 8,8 % |
| `t3_supertrend` | `volatility_breakout_crypto` | 5 | 207 | 12,8 % |
| `turtle_soup_crypto` | `volatility_breakout_crypto` | 5 | 186 | 11,5 % |

(vollständig in `ergebnisse/titelueberlappung.csv`; **alle 16** Bot-Paare mit
gemeinsamem Universum überlappen mindestens an einzelnen Tagen)

* An **98,4 %** der Tage hält mindestens ein Symbol mehr als einen Bot.
* Bis zu **vier** Bots halten am selben Tag dasselbe Symbol.

Die Diversifikation ist damit kleiner, als die Zahl neun suggeriert: die
Aktien-Bots greifen auf **dasselbe** Universum von 150 Titeln zu, die
Krypto-Bots auf dieselben ~20 Paare.

---

## 10. Der Korrelationsbefund, auf dem die These ruhte

Die ursprüngliche Analyse berichtete Korrelationen zwischen −0,02 und +0,01 —
„praktisch unkorreliert" — und nannte selbst schon den Vorbehalt, das könne
„teils ein mechanischer Effekt seltener Handelstage" sein. Er ist es.

| gemessen an | mittlere Paar-Korrelation (Neuner-Buch) | Spanne |
|---|---:|---|
| realisierter Kapitalkurve (bisherige Methode) | ≈ 0,00 | −0,02 … +0,02 |
| **täglicher Bewertung zu Marktpreisen** | **+0,112** | −0,015 … **+0,475** |

Und gegen einen gleichgewichteten Buy-and-Hold des jeweiligen Universums,
ebenfalls zu Marktpreisen:

| Bot | gegen B&H Aktien | gegen B&H Krypto |
|---|---:|---:|
| `turtle_soup_stocks` | **+0,82** | +0,33 |
| `volatility_breakout` | +0,49 | +0,21 |
| `elliott_wave_stocks` | +0,46 | +0,17 |
| `rsi2_mean_reversion` | +0,47 | +0,18 |
| `turtle_soup_crypto` | +0,26 | **+0,54** |
| `rsi2_crypto` | +0,12 | +0,38 |
| `t3_supertrend` | +0,04 | +0,24 |
| `elliott_wave` | +0,15 | +0,24 |
| `volatility_breakout_crypto` | +0,07 | +0,21 |

**Das gemeinsame Beta, das der Einwand vermutet hat, ist vorhanden und
messbar.** Es war nur unsichtbar, weil die Kapitalkurve eines Bots sich an
den meisten Tagen gar nicht bewegt: an Tagen ohne Ausstieg ist ihre
„Tagesrendite" exakt 0, und zwei überwiegend aus Nullen bestehende Reihen
korrelieren mechanisch nahe null — unabhängig davon, was die Märkte tun und
was die Bots halten.

Das ist derselbe Fehlertyp wie in Prinzip 12 des Protokolls: eine Messung,
die etwas anderes misst als gemeint, und deren Ergebnis genau deshalb so
beruhigend aussieht.

---

## 11. Einordnung

Was sich aus den Zahlen sagen lässt, ohne etwas zu entscheiden:

1. **−1,43 % ist keine Aussage über Risiko.** Die Zahl ist auf drei Ebenen
   nicht das, wofür sie gehalten wurde: veraltet (−9,41 % mit heutigen
   Parametern), am falschen Nenner gemessen (−32,12 % am eingesetzten
   Kapital) und gegen die falsche Vergleichsgrösse gestellt (−17,93 %
   mittlerer Einzel-Bot-Drawdown, nicht −22,20 % schlechtester).
2. **Der Mechanismus hinter dem Verdacht stimmt aber nicht.** Das Buch ist
   nicht überwiegend Kasse — es ist dauerhaft zu rund einem Drittel
   investiert und an keinem einzigen gemessenen Tag flach. Wer den Verdacht
   als „bestätigt" weitergäbe, gäbe eine falsche Begründung weiter.
3. **Diversifikation gibt es, in gewöhnlicher Grössenordnung.** −17,93 % im
   Mittel gegen −11,47 % kombiniert. Das ist ein Effekt, kein Wunder, und er
   ist zu einem erheblichen Teil schlichte 1/N-Gewichtung.
4. **Die Nennerfrage berührt die anderen Vergleiche des Projekts.** Der
   Hinweis in der Aufgabenstellung trifft zu: `elliott_wave_stocks` war im
   gemessenen Zeitraum an 95,4 % der Tage im Markt, bei 47,6 % mittlerer
   eigener Exposure. Sein +330 % gegen +756 % Buy-and-Hold ist also **kein**
   Vergleich zwischen „selten investiert" und „immer investiert" — die
   Zeitpräsenz ist ähnlich, die Kapitalbindung nur etwa halb so hoch. Was das
   für die Bewertung bedeutet, ist eine eigene Rechnung und hier nicht
   gemacht.
5. **Fünf von neun abgelegten Ergebniskurven beschreiben nicht mehr den Bot,
   der läuft.** Das betrifft mehr als diese Untersuchung: dieselben Dateien
   speisen laut Protokoll 4.3b die Montags-Mail und die
   Dashboard-Portfolio-Sicht, solange ein Bot unter zehn geschlossenen
   Live-Trades liegt — und das tun derzeit alle neun.

**Naheliegende Folgeaufgaben — benannt, nicht ausgeführt:**

* Die abgelegten `results/*/equity_curve.csv` neu erzeugen und prüfen, welche
  Aussagen im Projekt sich dadurch verschieben (betrifft
  `portfolio_overview.py`, Montags-Mail, Dashboard-Portfolio-Sicht).
* Die Korrelations- und Drawdown-Angaben der Beobachtungsebene auf eine
  Bewertung zu Marktpreisen umstellen, statt sie aus der realisierten
  Kapitalkurve zu ziehen.
* Buy-and-Hold-Vergleiche um die Exposure-Dimension ergänzen
  (Punkt 4 oben).
* Survivorship im Aktienuniversum — die in der Aufgabenstellung genannte
  eigene Aufgabe.

---

## 12. Dateien

| Datei | Inhalt |
|---|---|
| `bot_lauf.py` | ein Bot, ein Prozess: ruft die Original-Funktionen auf, schreibt den Positionsverlauf |
| `alle_bots.py` | Treiber über alle neun Bots |
| `exposure_kern.py` | Rechenkern: Tagesreihen, Zusammenfassung, Drawdown-Masse, B&H-Referenz |
| `test_exposure_kern.py` | 23 Selbsttests mit Gegenproben |
| `auswertung.py` | alle Zahlen dieses Berichts |
| `daten/<bot>_positionen.csv` | ausgeführte Positionen je Bot |
| `daten/<bot>_meta.json` | Parameter, Trade-Zahlen, Abgleich mit der abgelegten Kurve |
| `ergebnisse/zeitreihe_<gruppe>.csv` | tägliche Exposure, gebundenes Kapital, Positionszahl |
| `ergebnisse/monatlich_<gruppe>.csv` | Monatsmittel der Exposure |
| `ergebnisse/mtm_<gruppe>.csv` | Kapitalkurve zu Marktpreisen |
| `ergebnisse/je_bot_<gruppe>.csv` | Zeit im Markt, Drawdown-Phasen, Alleinstellungsanteile |
| `ergebnisse/titelueberlappung.csv` | alle Bot-Paare mit gemeinsam gehaltenen Symbolen |
| `ergebnisse/abgleich_abgelegte_kurven.csv` | abgelegte gegen frisch gerechnete Kurven |
| `ergebnisse/kennzahlen.json` | sämtliche Kennzahlen maschinenlesbar |
| `ergebnisse/konsole.txt` | vollständige Ausgabe des Auswertungslaufs |
