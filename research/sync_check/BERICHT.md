# Sync-Check `equity_simulation.py` vs. `live_params.py` — alle 9 Bots

**Status: reine Untersuchung. KEINE Code-Änderung an `equity_simulation.py`,
`live_params.py` oder `forward_test.py`.** Alle Skripte liegen ausschliesslich
unter `research/sync_check/`. Verifiziert per `git status`.

---

## 0. Entscheidungsgrundlage

### Datenbasis

| | |
|---|---|
| geprüfte Bots | 9 von 9, jede Konstante in beiden Dateien |
| zusätzlich geprüft | Werte, die erst über `backtest_*.py`-Defaults wirksam werden |
| Baseline-Vergleiche | 5 abweichende Bots, je 2 Konfigurationen |
| geprüfte Studien | 5, Konfigurationsquelle je Studie am Quelltext belegt |

### Pflicht-Gegenchecks

- **Einheiten und Namen normalisiert.** `ALLOCATION_PCT` steht live in
  **Prozent** (10, 5, 2), im Backtest als **Anteil** (0.10). Ohne
  Normalisierung wären alle 6 Bots mit dokumentierter Allokation
  fälschlich als abweichend gemeldet worden. Ebenso für Namenspaare
  (`T3_FAST`/`T3_FAST_LENGTH`, `SMA_TREND_PERIOD`/`SMA_TREND_FILTER`).
- **Backtest-Defaults aufgelöst.** `MAX_HOLD_DAYS`, `BB_LOOKBACK` und
  `BB_SQUEEZE_PERCENTILE` stehen nicht in `equity_simulation.py`, kommen
  aber über die Defaults des jeweiligen `backtest_*.py` — und stimmen dort
  mit den Live-Werten überein. Ein erster Entwurf dieses Checks meldete sie
  als „wirkungslos"; das war falsch und ist korrigiert.
- **Baseline-Reproduktion:** die berechneten Live-Varianten stimmen mit den
  dokumentierten Entscheidungszahlen überein — `rsi2_mean_reversion`
  **+36,75 %** (PROTOTYPE_FINDINGS Abschnitt 6), `elliott_wave_stocks`
  **+3084,09 % / −9,79 %** und **+1500,53 % / −1,90 %**
  (EXPERIMENT_FINDINGS Abschnitt 2), `volatility_breakout` **+224,41 %**.
- **Studien-Belege nachgeprüft:** `study_exposure.py --verify` prüft jedes
  Beleg-Zitat gegen den jeweiligen Studien-Branch — **5 von 5 bestätigt**.
- `test_sync_check.py`: **21 Checks**, alle bestanden.

### Belastbarkeit

Die Sync-Tabelle ist ein exakter Vergleich, keine Schätzung. Die
Baseline-Vergleiche sind deterministische Neuberechnungen mit den
unveränderten Bot-Funktionen. Die einzige Unschärfe liegt in Schritt 3: ob
eine verschobene Baseline die *Schlussfolgerung* einer Studie kippt, lässt
sich ohne Wiederholung der jeweiligen Analyse nicht beweisen — dort wird
auftragsgemäss nur eingeschätzt und gegebenenfalls eine Wiederholung
empfohlen.

### Scope-Grenzen

Keine Änderung an bestehenden Dateien. Keine Wiederholung einer kompletten
Bootstrap- oder Permutations-Analyse. Keine Aktivierungsempfehlung. Nicht
geprüft: ob `forward_test.py` seinerseits mit `live_params.py` synchron ist
(es liest sie direkt, siehe Abschnitt 4).

### Reproduktion

```
cd research/sync_check
python3 test_sync_check.py          # 21 Sanity-Checks
python3 run_all.py                  # Sync-Tabelle + Baseline-Vergleiche + Studien
python3 sync_table.py --json        # nur die Tabelle
python3 impact.py <bot>             # nur ein Baseline-Vergleich
python3 study_exposure.py --verify  # nur die Studien-Zuordnung, mit Beleg-Pruefung
```

---

## 1. Kurzfassung

**Die Prämisse der Aufgabe bestätigt sich in der Sache, aber nicht in der
Reichweite.**

- **Bestätigt:** 5 der 9 Bots sind abweichend konfiguriert, 4 sind sauber.
  Die Abweichungen sind real und teils gross — bei `elliott_wave_stocks`
  verdoppelt sich die Baseline-Rendite (1500 % → 3084 %), bei
  `volatility_breakout` steigt sie um 58 %.
- **Nicht bestätigt:** die Annahme, alle fünf Profitabilitäts-Studien seien
  betroffen. **Drei der fünf Studien (#18, #21, #22) haben ihre Parameter
  aus `live_params.py` gelesen**, nicht aus `equity_simulation.py` — die
  Konstanten-Abweichungen wirken sich dort nicht aus. Belegt am Quelltext
  der jeweiligen Branches.
- **Neu und wichtiger als erwartet:** die eine Abweichung, die **alle fünf
  Studien** durchdringt, ist der **BTC-Regimefilter** bei
  `volatility_breakout_crypto` — weil er kein Parameter ist, sondern
  fehlendes Verhalten in `equity_simulation.py`. Mit Filter fallen 35 % der
  Trades weg, die Rendite sinkt um 31 % und die Calmar-Ratio von **4,25 auf
  3,01**.
- **Zwei Studien sind voll betroffen:** #19 (HRP) und #20 (Trend-Overlay)
  bauen auf den gespeicherten `equity_curve.csv` auf, die aus der
  Backtest-Konfiguration stammen. Dort gehen alle fünf abweichenden Bots mit
  der falschen Konfiguration ein.

**Empfehlung für Folgeaufgaben (nicht hier durchgeführt):** Wiederholung von
#22 und der `volatility_breakout_crypto`-Zeilen aus #18 und #21 mit
aktiviertem Regimefilter; Wiederholung von #19 und #20 auf neu erzeugten
Kapitalkurven.

---

## 2. Schritt 1: vollständige Sync-Tabelle aller 9 Bots

### Die 4 synchronen Bots — explizit bestätigt

| Bot | geprüfte Grössen | Ergebnis |
|---|---|---|
| `elliott_wave` | `DEVIATION_PCT`, `STOP_LOSS_PCT`, `TAKE_PROFIT_FIB` | alle identisch |
| `t3_supertrend` | `T3_FAST(_LENGTH)`, `T3_SLOW(_LENGTH)`, `ADX_THRESHOLD`, `STOP_LOSS_PCT`, `MAX_CONCURRENT_POSITIONS`, `ALLOCATION_PCT` | alle identisch |
| `rsi2_crypto` | `SMA_TREND_PERIOD`/`FILTER`, `RSI_THRESHOLD`, `STOP_LOSS_PCT`, `ALLOCATION_PCT`, `MAX_CONCURRENT_POSITIONS` | alle identisch |
| `turtle_soup_crypto` | `DONCHIAN_PERIOD`, `STOP_MODE`, `MAX_HOLD_DAYS`, `ALLOCATION_PCT`, `MAX_CONCURRENT_POSITIONS` | alle identisch |

`elliott_wave` und `elliott_wave_stocks` dokumentieren in `live_params.py`
**keine** Allokation; der Backtest verwendet dort 10 %. Das ist keine
Abweichung, aber eine Lücke — dieselbe, die schon in der
Vol-Sizing-Untersuchung als Annahme 2 auffiel.

### Die 5 abweichenden Bots

| Bot | Grösse | `live_params.py` | `equity_simulation.py` | Art |
|---|---|---|---|---|
| `elliott_wave_stocks` | `USE_TAKE_PROFIT` | **False** | **True** | Konstante |
| `rsi2_mean_reversion` | `ALLOCATION_PCT` | **5 %** | **10 %** | Konstante |
| | `MAX_CONCURRENT_POSITIONS` | **20** | **8** | Konstante |
| `turtle_soup_stocks` | `ALLOCATION_PCT` | **2 %** | **10 %** | Konstante |
| | `MAX_CONCURRENT_POSITIONS` | **unbegrenzt** | **8** | Konstante |
| `volatility_breakout` | `MAX_CONCURRENT_POSITIONS` | **15** | **8** | Konstante |
| `volatility_breakout_crypto` | `BTC_REGIME_FILTER_ENABLED` | **True** | *keine Entsprechung* | **Verhalten** |

Der letzte Fall ist der einzige, der **kein** Konstanten-Vergleich ist:
`equity_simulation.py` dieses Bots kennt das Flag gar nicht und wendet den
Filter nirgends an. Nur `forward_test.py` tut es. Deshalb schlägt er auch auf
Studien durch, die ihre Parameter aus `live_params.py` beziehen.

(Vollständige Tabelle mit allen Zeilen: `results/sync_table.json` bzw.
`python3 sync_table.py`.)

---

## 3. Schritt 2: quantitative Auswirkung je abweichendem Bot

Beide Varianten mit den **unveränderten** Bot-Funktionen gerechnet,
Startkapital 10.000.

| Bot | Variante | Allok. | Limit | ausgeführt | Rendite | Max DD | **Calmar** |
|---|---|---|---|---|---|---|---|
| `elliott_wave_stocks` | Backtest | 10 % | 8 | 469 | 1500,53 % | −1,90 % | **789,75** |
| | **Live** | 10 % | 8 | **288** | **3084,09 %** | **−9,79 %** | **315,02** |
| `rsi2_mean_reversion` | Backtest | 10 % | 8 | 2641 | 29,91 % | −21,82 % | **1,37** |
| | **Live** | **5 %** | **20** | **4232** | **36,75 %** | −21,05 % | **1,75** |
| `turtle_soup_stocks` | Backtest | 10 % | 8 | 1887 | 133,01 % | −32,54 % | **4,09** |
| | **Live** | **2 %** | **unbegr.** | **8915** | **145,59 %** | −29,91 % | **4,87** |
| `volatility_breakout` | Backtest | 10 % | 8 | 1236 | 142,06 % | −22,39 % | **6,34** |
| | **Live** | 10 % | **15** | **1454** | **224,41 %** | −23,97 % | **9,36** |
| `volatility_breakout_crypto` | Backtest | 10 % | 8 | 310 | 71,26 % | −16,77 % | **4,25** |
| | **Live** (Filter an) | 10 % | 8 | **207** | **49,03 %** | −16,29 % | **3,01** |

**Die Verschiebungen sind erheblich und nicht alle in dieselbe Richtung:**

- `elliott_wave_stocks`: Rendite **×2,06**, Drawdown **fünffach** schlechter,
  Calmar **halbiert**. Die grösste absolute Verschiebung — der Backtest zeigt
  einen ganz anderen Bot als den live laufenden.
- `volatility_breakout`: Rendite **×1,58**, Calmar 6,34 → **9,36**.
- `turtle_soup_stocks` und `rsi2_mean_reversion`: moderat besser
  (Calmar +0,78 bzw. +0,38), aber mit stark veränderter Trade-Zahl (1887 →
  8915 bzw. 2641 → 4232).
- **`volatility_breakout_crypto`: als einziger Bot verschlechtert sich die
  Live-Konfiguration** — 359 → 233 gefundene Trades, Rendite **×0,69**,
  Calmar 4,25 → **3,01**. Der Regimefilter kostet hier deutlich Rendite und
  verbessert den Drawdown kaum (−16,77 % → −16,29 %).

Der letzte Punkt ist bemerkenswert, weil `live_params.py` den Filter
ausdrücklich **nicht** als Rendite-Hebel, sondern als
Risikomanagement-Massnahme begründet (dokumentierte
2022-Krypto-Winter-Wirkung). Über den Gesamtzeitraum bestätigt sich das
Rendite-Opfer, die Drawdown-Verbesserung fällt hier aber gering aus.

---

## 4. Schritt 3: Rückwirkung auf die fünf Studien — bot-genau

Entscheidend ist, **woher jede Studie ihre Konfiguration bezieht**. Das ist
nicht einheitlich; jede Zuordnung ist am Quelltext des jeweiligen Branches
belegt und per `--verify` nachgeprüft.

| PR | Studie | Konfigurationsquelle | betroffene Bots | Stufe |
|---|---|---|---|---|
| #18 | Vol-Sizing | `live_params.py` (Beleg: `allocation_pct = lp.ALLOCATION_PCT`) | nur `volatility_breakout_crypto` | gering |
| #19 | HRP | `results/<bot>/equity_curve.csv` über `portfolio_overview.py` | **alle 5** | **hoch** |
| #20 | Trend-Overlay | dieselbe Quelle | **alle 5** | **hoch** |
| #21 | Trailing-Stops | `live_params.py` (Beleg: `import live_params as lp`) | nur `volatility_breakout_crypto` | gering |
| #22 | VBC-Vertiefung | `live_params.py` | nur `volatility_breakout_crypto` | gering |

### Einzelbewertung je Studie

**#18 Vol-Sizing — Kernaussage bleibt, eine Zeile braucht Wiederholung.**
Die Studie las Stop-Loss, Allokation, Positionslimit und `USE_TAKE_PROFIT`
aus `live_params.py`. Die vier Konstanten-Abweichungen wirkten sich nicht
aus. Ihre zentrale Aussage — Vol-Skalierung schadet bei 7 von 9 Bots — ist
davon unberührt. **Aber:** einer der beiden „Gewinner" war
`volatility_breakout_crypto`, und dessen Baseline verschiebt sich mit dem
Regimefilter um Faktor 0,69. Die Aussage „Verbesserung: ja" für diesen Bot
steht damit auf einer Baseline, die nicht der Live-Konfiguration entspricht.
**Empfehlung: diese eine Zeile mit aktiviertem Filter nachrechnen.**

**#19 HRP — Kernaussage vermutlich robust, Zahlen aber neu zu erzeugen.**
Die Studie baut auf den gespeicherten Kapitalkurven auf; 4 der 8
beitragenden Kurven stammen aus einer abweichenden Konfiguration, mit
Renditefaktoren zwischen 1,10 und 2,06. Ihre Kernaussage war struktureller
Natur („die Verbesserungsmarge ist klein, weil das 9-Bot-Portfolio bereits
stark diversifiziert ist"; Portfolio-Drawdown −6,33 % gegen −32,4 % beim
schlechtesten Einzel-Bot). Ein Argument über Diversifikation dürfte
robust bleiben — die konkreten Zahlen sind es nicht.
**Empfehlung: mit neu erzeugten Kurven wiederholen; Kernaussage vermutlich
unverändert.**

**#20 Trend-Overlay — dieselbe Lage.** Die Kernaussage („der gesamte Effekt
stammt aus der 2022-Episode, Out-of-Sample wirkungslos") hängt an der
zeitlichen Verteilung, nicht an den Niveaus, und dürfte robust bleiben. Die
Niveaus verschieben sich aber. **Empfehlung: mit neu erzeugten Kurven
wiederholen.**

**#21 Trailing-Stops — Kernaussage robust, eine Zeile braucht Wiederholung.**
Parameter aus `live_params.py`; die Befunde zu `t3_supertrend` (belastbare
Verschlechterung) und `volatility_breakout` (Vorzeichen unbestimmt) sind
nicht betroffen. Die Zeile `volatility_breakout_crypto` steht auf der
Baseline 4,25, die live 3,01 lautet. **Empfehlung: diese Zeile mit Filter
nachrechnen.**

**#22 VBC-Vertiefungsstudie — hier ist eine Neubewertung am ehesten
gerechtfertigt.** Die gesamte Studie betrifft genau diesen Bot, und ihre
Baseline verschiebt sich von Calmar 4,25 auf 3,01 (−29 %), bei 35 % weniger
Trades. Ihre zentrale Aussage lautete: *die einzige belastbare Wirkung des
ATR-Trailing-Stops ist die Drawdown-Reduktion; die Calmar-Verbesserung ist
nur Out-of-Sample grenzwertig belegt.*

Diese Aussage könnte sich in beide Richtungen verschieben, und der Grund
lässt sich benennen: der Regimefilter blockiert Einstiege in
BTC-Abwärtsphasen — **genau in den Phasen, in denen der Trailing-Stop laut
jener Studie am meisten half** (er war in 10 von 10 Quartalen mit negativer
Baseline besser). Filter und Trailing-Stop greifen also an derselben Stelle
an. Es ist plausibel, dass sie sich überlagern, wie es die Studie bereits
für Vol-Sizing und Trailing-Stop gezeigt hat — bewiesen ist das hier
**nicht**, und es ist auftragsgemäss nicht Teil dieser Untersuchung.
**Empfehlung: #22 mit aktiviertem Regimefilter vollständig wiederholen.**

### Zusammenfassende Antwort auf die Kernfrage

`volatility_breakout_crypto` kam in allen fünf Studien vor und ist in allen
fünf mit einer Baseline gerechnet worden, die nicht der Live-Konfiguration
entspricht. Die Verschiebung ist mit −29 % Calmar gross genug, dass die
„doppelt bestätigte" Einschätzung dieses Bots **eine Neubewertung braucht**.
Für die übrigen Bots gilt das nur bei #19 und #20.

---

## 5. Schritt 4: Herkunft der Abweichungen

Ein Blick in die Commit-Historie genügt — das Muster ist bei allen fünf Bots
identisch:

| Bot | `equity_simulation.py` zuletzt geändert in | `live_params.py` zuletzt geändert in |
|---|---|---|
| `elliott_wave_stocks` | „Initial commit" (2026-09-02) | „Take-Profit deaktivieren" (2026-09-03) |
| `rsi2_mean_reversion` | „Vierten Bot prototypisieren" (2026-09-03) | „Add live paper-trading infrastructure" (2026-09-03) |
| `turtle_soup_stocks` | „Add ninth bot prototype" (2026-09-04) | „Add live paper-trading infrastructure" (2026-09-04) |
| `volatility_breakout` | „Add Volatility Breakout prototype" (2026-09-03) | „Add live paper-trading infrastructure" (2026-09-03) |
| `volatility_breakout_crypto` | „Add two crypto prototypes" (2026-09-03) | „Add live paper-trading infrastructure" (2026-09-04) |

**Eindeutiger Befund: `equity_simulation.py` ist in allen fünf Fällen auf dem
Stand des Prototyp-Commits.** Es wurde geschrieben, als der Bot gebaut
wurde, und danach nie wieder angefasst. Die validierten Werte aus der
anschliessenden Kapitalmanagement- und Exit-Optimierung landeten
ausschliesslich in `live_params.py`.

Das erklärt auch die vier synchronen Bots: bei `t3_supertrend`,
`rsi2_crypto` und `turtle_soup_crypto` steht in `live_params.py`
ausdrücklich, dass das Kapitalmanagement **unverändert** aus dem Prototyp
übernommen wurde (bei `turtle_soup_crypto` sogar mit Begründung: „jede
getestete Lockerung verschlechtert das Ergebnis"). `elliott_wave` hat gar
kein Positionslimit. **Die vier Bots sind also nicht synchron, weil jemand
sie synchronisiert hätte, sondern weil sich bei ihnen nichts geändert hat.**

Es handelt sich damit nicht um einen Fehler in einer einzelnen Datei,
sondern um eine fehlende Kopplung: die beiden Dateien haben nie einen
gemeinsamen Bezugspunkt gehabt. Auch die gespeicherten
`results/<bot>/equity_curve.csv` stammen aus dieser Prototyp-Phase — bei
`elliott_wave_stocks` und `volatility_breakout_crypto` datieren sie
nachweislich **vor** der jeweiligen Live-Parameter-Änderung.

`forward_test.py` ist von alledem nicht betroffen: es importiert direkt aus
`live_params.py` und läuft damit auf der richtigen Konfiguration.

---

## 6. Gesamteinschätzung (unaufgeregt, ohne Handlungsempfehlung)

Der Befund ist real, aber schmaler als die Ausgangsvermutung. Fünf von neun
Bots sind betroffen, die Verschiebungen sind teils erheblich — und der
tatsächlich live laufende Betrieb ist nicht betroffen, weil
`forward_test.py` direkt aus `live_params.py` liest. Was betroffen ist, sind
Backtest-Läufe von `equity_simulation.py` und die daraus abgeleiteten
gespeicherten Kapitalkurven.

Von den fünf Studien haben drei ihre Parameter aus `live_params.py` gelesen
und sind dadurch weitgehend geschützt. Die beiden portfolioweiten Studien
(#19, #20) sind es nicht.

Die eine Abweichung, die alle fünf durchdringt, ist der BTC-Regimefilter —
und zwar gerade deshalb, weil er kein Parameter ist. Eine Sync-Prüfung, die
nur Konstanten vergleicht, hätte ihn nicht gefunden. Für den Bot, der als
einziger in allen fünf Studien vorkam und dort als „doppelt bestätigt" galt,
ist das die relevanteste Einzelerkenntnis dieser Untersuchung.

Ob und in welcher Reihenfolge die empfohlenen Wiederholungen sinnvoll sind,
ist eine Entscheidung des Nutzers.

---

## 7. Empfohlene Folgeaufgaben (Vorschlag, hier nicht durchgeführt)

1. **#22 vollständig wiederholen** mit aktiviertem BTC-Regimefilter — grösste
   erwartete Wirkung, betrifft die zentrale Aussage der Studie.
2. **`volatility_breakout_crypto`-Zeilen aus #18 und #21 nachrechnen.**
3. **#19 und #20 mit neu erzeugten Kapitalkurven wiederholen** — Kernaussagen
   vermutlich robust, Zahlen aber überholt.
4. Unabhängig davon offen: die fehlende `ALLOCATION_PCT`-Dokumentation bei
   `elliott_wave` und `elliott_wave_stocks`.

## 8. Explizit ausserhalb des Scopes

Jede Code-Änderung an `equity_simulation.py`, `live_params.py` oder
`forward_test.py`; jede Wiederholung einer kompletten Bootstrap- oder
Permutations-Analyse; jede Aktivierungsempfehlung; die Frage, welche der
beiden Konfigurationen „richtig" ist.

## 9. Dateien

| Datei | Inhalt |
|---|---|
| `sync_table.py` | vollständiger Konstanten-Vergleich aller 9 Bots, inkl. Einheiten, Aliase und Backtest-Defaults |
| `impact.py` | Baseline-Vergleich Backtest- gegen Live-Konfiguration je abweichendem Bot |
| `study_exposure.py` | Konfigurationsquelle je Studie, mit Beleg und `--verify` |
| `run_all.py` | alle drei Schritte nacheinander |
| `test_sync_check.py` | 21 Sanity-Checks |
| `results/` | `sync_table.json`, `impact_<bot>.json`, `study_exposure.json` |
