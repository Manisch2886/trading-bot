# `volatility_breakout_crypto` — Vertiefungsstudie: Vol-Sizing × ATR-Trailing-Stop

**Status: reine Backtest-Untersuchung. KEINE Live-Aktivierung, KEINE Änderung an
Live-Dateien, KEINE Aktivierungsempfehlung.** Alle Skripte liegen ausschliesslich
unter `research/vbc_deepdive/`. Verifiziert per `git status`: keine Datei
ausserhalb dieses Verzeichnisses angefasst — insbesondere nicht
`strategies/volatility_breakout_crypto/live_params.py` oder `forward_test.py`.

---

> ## ⚠ Nachtrag (Fassung 2): diese Studie wurde ohne den BTC-Regimefilter gerechnet
>
> Der Sync-Check (PR #24) hat belegt, dass `equity_simulation.py` den in
> `live_params.py` aktivierten `BTC_REGIME_FILTER_ENABLED = True` **nicht anwendet**.
> Die Abschnitte 0–14 unten beruhen deshalb auf einer Trade-Grundlage, die der
> Live-Bot so nie handelt. Sie bleiben unverändert als Protokoll stehen; **gültig
> für die Live-Konfiguration ist der Nachtrag N0–N9 direkt darunter.**
>
> **Kurz: die Kernaussage der Erstfassung verschärft sich.** Von den vier geprüften
> Behauptungen überlebt nur noch die Drawdown-Reduktion des Trailing-Stops. Der
> einzige positive risikoadjustierte Befund der Erstfassung — Out-of-Sample-Calmar,
> P = 95,0 % — fällt auf **64,6 %** und ist damit von Rauschen nicht mehr zu
> unterscheiden.

---

# Nachtrag N: dieselbe Methodik mit aktiviertem BTC-Regimefilter

## N0. Entscheidungsgrundlage

### Was gerechnet wurde

Die **komplette** Methodik der Erstfassung — vier Kombinationen, IS/OOS,
4 Walk-Forward-Fenster, Quartals-Episoden, Buy-and-Hold, Block-Bootstrap mit
2000 Replikaten, 500 Reihenfolge-Permutationen — noch einmal auf der gefilterten
Trade-Grundlage. Nichts wurde neu optimiert: derselbe ATR-Multiplikator
`k = 0,8956`, dasselbe ATR-14, Vol-90, Clip 4,0, derselbe Trennzeitpunkt,
dieselben Kalenderfenster, derselbe Bootstrap-Seed.

Der Filter wird in **zwei** Anwendungsarten gerechnet, weil sie nicht dasselbe
sind (Begründung in `regime.py`):

| Modus | Was er tut | Rolle |
|---|---|---|
| `posthoc` | vollen Trade-Satz erzeugen, dann die Einstiege im BTC-Abwärtstrend streichen — die **Projekt-Konvention** (`regime_filter.filter_trades_by_regime`, `experiment_btc_regime_filter.py`) | **primär**, weil referenzfähig |
| `sequential` | Einstieg schon im Scan blockieren, Symbol bleibt frei für ein späteres Signal — mechanisch getreu zu `forward_test.py::find_new_signals` | Gegenprobe |

Der Unterschied ist klein: 241 statt 233 Trades, also **8 Ersatz-Trades (3,4 %)**.
Alle Schlussfolgerungen unten gelten in beiden Modi. Die Projekt-Konvention trägt.

### Datenbasis

Unverändert 2022-03-17 bis 2026-08-30 (4,45 Jahre), 20 Symbole, **ein einziger
Krypto-Zyklus**. BTC ist in **48,0 %** aller Balken im Aufwärtstrend, der Filter
sperrt also gut die Hälfte des Zeitraums.

| | ohne Filter | `posthoc` | `sequential` |
|---|---|---|---|
| Trades fester Stop | 359 | **233** (−35,1 %) | 241 (−32,9 %) |
| Trades ATR-Trailing | 396 | **265** (−33,1 %) | 271 (−31,6 %) |
| **OOS ausgeführt, Baseline** | 103 | **64** | 64 |
| **OOS ausgeführt, Trailing** | 140 | **95** | 94 |

**Das ist die wichtigste Zahl dieses Nachtrags.** Der einzige positive Befund der
Erstfassung stand out-of-sample auf 103 bzw. 140 ausgeführten Trades. Mit Filter
sind es **64 bzw. 95** — auf 17 Monaten. Jede Aussage über diesen Zeitraum trägt
entsprechend wenig Gewicht, unabhängig davon, wie die Zahl ausfällt.

### Regressionscheck — zuerst, sonst zählt nichts

`verify_reference.py`: **56/56** Referenzwerte exakt, aus vier unabhängigen Quellen:

1. die bot-eigene `equity_simulation.collect_all_trades` (Trade-Anzahl, PnL-Summe,
   erster Entry / letzter Exit),
2. **50 Werte** aus PR #18 und PR #21 (unverändert aus der Erstfassung),
3. der **Sync-Check PR #24**: gefilterte Baseline **233 Trades, 207 ausgeführt,
   +49,03 %, −16,29 %** — auf die zweite Nachkommastelle getroffen,
4. **`live_params.py` selbst.** Dort ist die Drawdown-Wirkung des Filters als
   Projekt-Entscheidungsgrundlage dokumentiert: *„70/30: -11,33% -> -7,76%"*.
   Beide Seiten dieser Aussage werden hier nachgerechnet und **beide stimmen
   exakt**. Diese Zahl stammt aus einer ganz anderen Rechnung, Monate vor dieser
   Studie — sie ist deshalb der wertvollste der vier Checks.

Zusätzlich: der `off`-Modus reproduziert das committete Ergebnis der Erstfassung
in **allen 2171 Feldern bitgenau** (nur neue Felder kamen hinzu). Der Umbau hat
also nichts an der Erstfassung verändert.

### Belastbarkeit — die Tabelle, die die Frage beantwortet

Block-Bootstrap, 2000 Replikate, gepaart, P(Effekt > 0) in %, gesamt / IS / OOS:

| Behauptung | ohne Filter | **mit Filter (`posthoc`)** | `sequential` | Urteil |
|---|---|---|---|---|
| Trailing senkt den **Drawdown** | 100,0 / 99,9 / 99,2 | **99,2 / 99,3 / 97,3** | 99,0 / 98,9 / 98,0 | **hält** |
| Trailing verbessert die **Calmar** | 73,8 / 48,8 / **95,0** | 61,1 / 50,8 / **64,6** | 56,7 / 44,1 / 67,1 | **fällt weg** |
| Vol-Sizing verbessert irgendetwas | 40,1 / 47,1 / 53,8 | **16,1 / 21,1 / 38,7** | 18,6 / 26,8 / 35,4 | **kippt ins Negative** |
| Kombination schlägt Trailing allein | 31,1 / 27,6 / 71,2 | **13,4 / 9,8 / 50,6** | 22,7 / 14,9 / 51,9 | **kein Beleg, deutlicher** |

### Was diesen Befund umstossen würde

* Ein zweiter Krypto-Zyklus. Der Filter halbiert die Datenbasis; die 17 OOS-Monate
  tragen jetzt 64 Baseline-Trades. Ein zweiter Bärenmarkt könnte das Bild drehen —
  in beide Richtungen.
* Eine andere Regime-Definition. `BTC_ATR_LENGTH = 22`, `BTC_ATR_MULT = 3,0` sind
  Bot-Konstanten und wurden hier **nicht** variiert. Ob der Befund an genau diesem
  SuperTrend hängt, ist ungeprüft.
* Der Reihenfolge-Effekt (N6): der berichtete gefilterte Baseline-Wert liegt im
  **17,6. Perzentil** seiner eigenen Streuung. Wäre er zufällig zentral
  ausgefallen, wäre der Trailing-Vorteil noch kleiner.

### Was dieser Nachtrag nicht leistet

Keine Aussage über andere Bots, keine Aktivierungs- oder Deaktivierungsempfehlung
zum Regimefilter, keine Prüfung, ob der Filter selbst eine gute Idee ist (das ist
in `PROTOTYPE_FINDINGS.md` Abschnitt 9 bereits entschieden und wird hier als
gegeben genommen), keine Parameter-Optimierung.

### Reproduktion

```
python3 verify_reference.py                    # 56/56, Gate für alles Weitere
python3 test_vbc_core.py                       # 56 Sanity-Checks
python3 run_deepdive.py                        # Erstfassung, ohne Filter
python3 run_deepdive.py --regime posthoc       # primäre Fassung 2
python3 run_deepdive.py --regime sequential    # Gegenprobe
python3 compare_modes.py                       # Gegenüberstellung + Zerlegung
```

---

## N1. Die direkte Antwort auf die zentrale Frage

> **Bleibt `volatility_breakout_crypto` nach Korrektur des Regimefilters ein
> überzeugender Kandidat?**

**Nein — als „mehrfach bestätigter" Kandidat trägt er nicht mehr.** Genauer, weil
die Frage zwei Teile hat:

**Die Drawdown-Reduktion des Trailing-Stops verschwindet nicht.** Sie war der
einzige belastbare Befund der Erstfassung und bleibt es: P = 99,2 % über den
Gesamtzeitraum, 97,3 % out-of-sample. Der Punktschätzer sinkt (−16,29 % → −5,41 %
statt −16,77 % → −5,76 %), aber die Aussage steht.

**Die risikoadjustierte Vorteilhaftigkeit verschwindet.** Der eine positive
Calmar-Befund — OOS, P = 95,0 % — fällt auf 64,6 %. Out-of-Sample schrumpft der
Abstand von **+3,25 Calmar** (1,79 → 5,04) auf **+0,81** (2,96 → 3,77), und der
Trailing-Stop liefert dort jetzt sogar **weniger Rendite als die Baseline**
(19,20 % gegen 23,00 %). Was übrig bleibt, ist ein Mechanismus, der Drawdown
gegen Rendite tauscht — genau wie der Filter, den der Bot bereits fährt.

**Und die Vol-Skalierung ist nicht mehr neutral, sondern schädlich.** In der
Erstfassung war sie „von Rauschen ununterscheidbar" (P = 40,1 %). Mit Filter sind
es **16,1 %** — also rund 84 % Wahrscheinlichkeit, dass sie die Calmar-Ratio
*verschlechtert*. Der Bot, der in PR #18 einer von nur zwei Gewinnern war, ist
unter der Live-Konfiguration keiner mehr.

---

## N2. Warum: die beiden Schutzmechanismen überlappen — aber nur dort, wo es zählt

Alle vier Zellen liegen vor, die Zerlegung ist deshalb keine Interpretation,
sondern eine Rechnung (`compare_modes.py`). Prozentpunkte Drawdown, positiv =
Drawdown gesenkt, gegen die ungefilterte Baseline als gemeinsamen Nullpunkt:

| Periode | Filter allein | Trailing allein | beide zusammen | **Überlappung** | Anteil am schwächeren Mechanismus |
|---|---|---|---|---|---|
| Gesamtzeitraum | 0,48 | 11,01 | 11,36 | **0,13** | 27,1 % |
| In-Sample | 0,48 | 11,01 | 11,36 | **0,13** | 27,1 % |
| **Out-of-Sample** | 3,57 | 5,75 | 6,24 | **3,08** | **86,3 %** |

Das erklärt beide Hälften des Befunds auf einmal:

* **Über den Gesamtzeitraum überlappen sie fast gar nicht** (0,13 pp). Der
  Grund ist unspektakulär: der grösste Drawdown des Gesamtzeitraums liegt nicht
  in einer Phase, die der Filter erwischt — er senkt ihn nur um 0,48 pp
  (−16,77 % → −16,29 %). Wo der Filter nichts tut, kann er dem Trailing-Stop
  auch nichts wegnehmen.
* **Out-of-Sample überlappen sie fast vollständig.** Dort wirkt der Filter
  (−11,33 % → −7,76 %, exakt der in `live_params.py` dokumentierte Wert), und
  **86 % dieser Wirkung liefert der Trailing-Stop ohnehin schon**. Man bezahlt
  zwei Versicherungen und bekommt eine.

Genau in dieser Periode stand der einzige positive Befund der Erstfassung. Er
war kein zusätzlicher Effekt — er war der Effekt, den der Live-Bot bereits hatte,
noch einmal gemessen.

Die `sequential`-Gegenprobe zeigt dasselbe Bild und out-of-sample sogar etwas
stärker (Überlappung 3,23 pp, 90,5 %). Über den Gesamtzeitraum liegt sie dort bei
136,6 % — kein Rechenfehler, sondern Gegenläufigkeit: die 8 Ersatz-Trades, die
nur im `sequential`-Modus entstehen können, erzeugen eigenen Drawdown, sodass
beide Mechanismen zusammen schlechter schützen als der Trailing-Stop allein
(−6,46 % gegen −5,76 %).

---

## N3. Die vier Kombinationen mit Filter

Rendite % / Max Drawdown % / **Calmar**, Modus `posthoc`:

| Periode | A Baseline | B Vol-Sizing | C Trailing | D Kombiniert |
|---|---|---|---|---|
| Gesamt | 49,03 / −16,29 / **3,01** | 32,93 / −15,89 / **2,07** | 30,29 / −5,41 / **5,60** | 19,74 / −6,01 / **3,28** |
| In-Sample | 20,47 / −16,29 / **1,26** | 11,65 / −16,09 / **0,72** | 9,29 / −5,41 / **1,72** | 4,65 / −6,25 / **0,74** |
| Out-of-Sample | 23,00 / −7,76 / **2,96** | 18,28 / −6,82 / **2,68** | 19,20 / −5,09 / **3,77** | 18,14 / −4,04 / **4,49** |

Zum Vergleich dieselben Zellen ohne Filter (Erstfassung, Abschnitt 5):

| Periode | A Baseline | B Vol-Sizing | C Trailing | D Kombiniert |
|---|---|---|---|---|
| Gesamt | 71,26 / −16,77 / **4,25** | 61,09 / −14,96 / **4,08** | 45,65 / −5,76 / **7,93** | 37,88 / −5,93 / **6,39** |
| Out-of-Sample | 20,23 / −11,33 / **1,79** | 16,20 / −8,04 / **2,01** | 28,12 / −5,58 / **5,04** | 24,31 / −4,05 / **6,00** |

Bemerkenswert und leicht zu übersehen: **out-of-sample verbessert der Filter die
Baseline** (Calmar 1,79 → 2,96), **über den Gesamtzeitraum verschlechtert er sie**
(4,25 → 3,01). Beides ist in `live_params.py` vorweggenommen — der Filter ist dort
ausdrücklich als Risikomanagement-Massnahme aktiviert, *„NICHT weil er in jedem
Fall die Rendite verbessert"*. Dieser Nachtrag bestätigt die dortige Einschätzung;
er stellt sie nicht in Frage.

**Additivität** (Gesamtzeitraum, `posthoc`): Renditekosten stapeln sich weiterhin
(erwartet 16,21 %, tatsächlich 19,74 %, +3,53 pp), Drawdown-Reduktionen
überlappen weiterhin (erwartet −5,01 %, tatsächlich −6,01 %, −1,00 pp). Die
Grundaussage der Erstfassung — *man zahlt beide Mechanismen voll und bekommt
ihren Schutz nur einmal* — gilt unverändert, jetzt mit einem dritten Mechanismus
im selben Bild.

---

## N4. Buy-and-Hold — unverändert, und deshalb aussagekräftig

Der Gegencheck hängt weder am Stop noch an der Gewichtung noch am Filter (gleiche
Symbole, gleiches Kalenderfenster), er ist in allen drei Modi identisch:

| Periode | beste gefilterte Variante | **Buy-and-Hold** |
|---|---|---|
| Gesamtzeitraum | Trailing 30,29 / −5,41 / **5,60** | 19,45 / −67,90 / **0,29** |
| Out-of-Sample | Kombiniert 18,14 / −4,04 / **4,49** | **68,81** / −59,47 / **1,16** |

Weil der Filter Rendite kostet, rückt die Strategie **näher an stumpfes Halten
heran**: out-of-sample bringt Halten jetzt das **Drei- bis Vierfache** der
Rendite jeder Variante (68,81 % gegen 18–23 %), bei rund fünfzehnfachem Drawdown
(−59,47 % gegen −4,04 %).
Über den Gesamtzeitraum bleibt die Strategie klar überlegen. Die Abwägung ist
dieselbe wie in der Erstfassung — nur ist der Abstand kleiner geworden.

---

## N5. Episoden und Walk-Forward — hier ändert sich am wenigsten

**Walk-Forward** (Calmar, `posthoc`; ohne Filter in Klammern):

| Fenster | Baseline | Trailing |
|---|---|---|
| W1 2022-03-17 .. 2023-04-25 | −0,65 (−0,20) | **0,75** (0,71) |
| W2 2023-04-25 .. 2024-06-03 | **3,22** (3,85) | −0,16 (0,04) |
| W3 2024-06-03 .. 2025-07-12 | 2,25 (3,32) | **6,08** (6,10) |
| W4 2025-07-12 .. 2026-08-21 | 0,45 (0,17) | **1,74** (3,14) |

Der Trailing-Stop ist in 3 von 4 Fenstern besser — **wie ohne Filter**, und mit
demselben Ausreisser W2. Die Walk-Forward-Stabilität ist also nicht das, was sich
ändert; es ändert sich die Unsicherheit um diese Punktschätzer herum.

**Bedingte Struktur** (Quartale): Korrelation zwischen Baseline-Quartalsrendite
und Trailing-Vorteil **−0,88** (ohne Filter −0,88). In Quartalen mit negativer
Baseline war der Trailing-Stop in **90 %** besser (ohne Filter: 100 %), in
Quartalen mit positiver Baseline nur in **14 %**. Das Versicherungsprofil aus
Abschnitt 8 der Erstfassung bleibt exakt bestehen — der Filter ändert die *Art*
des Mechanismus nicht, nur seinen verbleibenden Nutzen.

**Episoden-Konzentration**: Trailing besser in **10 von 17** Quartalen, grösstes
Einzelquartal 2024Q1 mit −25,56 pp = 29,9 % des Gesamtunterschieds, Top-3 = 52,7 %.
Kein einzelnes Quartal reisst die 60-%-Schwelle; der Effekt ist weiterhin nicht
von einer Einzelepisode getragen.

---

## N6. Reihenfolge-Empfindlichkeit — mit Filter unangenehmer als ohne

Methodik aus PR #23, 500 Permutationen der Reihenfolge gleichzeitiger Einstiege.
Gefiltert teilen sich **60,9 %** der Trades einen Einstiegszeitpunkt (ohne Filter
59,6 %) — der Filter entschärft das Problem also nicht.

Calmar über den Gesamtzeitraum, `posthoc`:

| Variante | berichtet | min | Median | max | **Perzentil des berichteten Werts** |
|---|---|---|---|---|---|
| Baseline | **3,01** | 2,78 | 3,85 | 4,58 | **17,6** |
| Vol-Sizing | 2,07 | 1,71 | 2,33 | 3,62 | 31,2 |
| Trailing | 5,60 | 5,03 | 5,82 | 6,70 | 28,4 |
| Kombiniert | 3,28 | 3,20 | 3,79 | 4,42 | **2,6** |

**Das ist ein eigenständiger Befund und er geht gegen den Trailing-Stop.** Der
gefilterte Baseline-Wert 3,01, den der Sync-Check berichtet und den dieser
Nachtrag als Referenz reproduziert hat, liegt im **17,6. Perzentil** seiner
eigenen Streuung: rund 82 % der gleichermassen legitimen Reihenfolgen hätten eine
**bessere** Baseline ergeben (Median 3,85). Die Baseline wird durch die zufällige
Einlese-Reihenfolge also systematisch zu schlecht dargestellt — und damit der
Trailing-Stop zu gut. Beim Median-Vergleich schrumpft der Abstand von
3,01 → 5,60 (+2,59) auf 3,85 → 5,82 (+1,97).

Was **nicht** kippt: die Streubereiche von Baseline (2,78 … 4,58) und Trailing
(5,03 … 6,70) überlappen sich **nicht**. Über den Gesamtzeitraum ist der
Calmar-Unterschied also grösser als die Reihenfolge-Willkür — er ist nur kleiner,
als der berichtete Punktschätzer nahelegt. Und der Drawdown ist wie in der
Erstfassung praktisch invariant (−16,29 % in allen 500 Permutationen).

---

## N7. Getroffene Annahmen dieses Nachtrags (vollständig)

Zusätzlich zu den 12 Annahmen der Erstfassung (Abschnitt 4), die alle
unverändert gelten:

**N-A1 — `posthoc` ist die primäre Variante, `sequential` die Gegenprobe.**
Nachträgliches Streichen ist die Konvention des Projekts (`filter_trades_by_regime`,
`experiment_btc_regime_filter.py`) und die einzige Variante, die gegen den
Sync-Check und gegen `live_params.py` referenzfähig ist. Sie bildet das
Live-Verhalten aber nicht exakt ab, deshalb wird beides gerechnet. Der Unterschied
beträgt 8 Trades (3,4 %) und ändert keine Schlussfolgerung.

**N-A2 — `k` wird NICHT nachkalibriert.** Es bleibt bei `k = 0,8956` aus der
ungefilterten In-Sample-Kalibrierung. Auftragsgemäss wird kein bereits gewählter
Parameter neu optimiert; ausserdem änderten sich sonst Trade-Satz *und*
Stop-Distanz gleichzeitig. Auf dem gefilterten Satz wäre `k = 0,8823` (−1,5 %) —
reine Dokumentationszahl, nicht verwendet.

**N-A3 — Trennzeitpunkt und Kalenderfenster stammen aus dem ungefilterten Satz.**
Gleiche Begründung. Hier fällt die Annahme nicht ins Gewicht: auf dem gefilterten
Satz neu berechnet ergäbe sich derselbe Zeitpunkt (2025-04-22).

**N-A4 — Die Regime-Parameter sind Bot-Konstanten und werden nicht variiert.**
`BTC_ATR_LENGTH = 22`, `BTC_ATR_MULT = 3,0` unverändert aus
`regime_filter.py`. Ob der Befund an dieser Regime-Definition hängt, ist offen.

**N-A5 — Der Bootstrap-Seed bleibt gleich** (20260907), damit die Modi
vergleichbar bleiben und nicht ein Teil des Unterschieds aus einer anderen
Zufallsziehung stammt.

**N-A6 — Balken vor dem ersten BTC-Regime-Eintrag gelten als gesperrt.**
Die vorsichtigere Wahl: ohne bekanntes Regime gäbe es live keinen Einstieg. In
der Praxis liegen diese Balken vor dem Warmup und sind wirkungslos.

---

## N8. Rückwirkung auf PR #18 und PR #21 (Teil B der Aufgabe)

Die punktuellen Korrekturen liegen in den jeweiligen Studien-Verzeichnissen
(`research/volatility_scaled_sizing/NACHTRAG_REGIMEFILTER.md` bzw.
`research/trailing_stops/NACHTRAG_REGIMEFILTER.md`) und stützen sich auf **exakt
dieselbe gefilterte Trade-Grundlage** wie dieser Nachtrag — dieselben 233 bzw.
265 Trades, dieselbe Baseline 49,03 % / −16,29 % / 3,01. Konsistenz ist damit
nicht behauptet, sondern konstruktiv gegeben.

---

## N9. Neue und geänderte Dateien

| Datei | Rolle |
|---|---|
| `regime.py` | **neu** — Filter über die unveränderten Bot-Funktionen, beide Anwendungsarten |
| `compare_modes.py` | **neu** — Gegenüberstellung der drei Modi + Zerlegung der Drawdown-Reduktion |
| `run_deepdive.py` | erweitert um `--regime`; Vorgabe `off` reproduziert die Erstfassung in allen 2171 Feldern bitgenau |
| `verify_reference.py` | erweitert um die Referenzen aus PR #24 und `live_params.py` (jetzt 56/56) |
| `test_vbc_core.py` | erweitert um Abschnitt 11 zum Regimefilter (jetzt 56 Checks) |
| `results/vbc_deepdive_posthoc.json`, `..._sequential.json`, `mode_comparison.json` | **neu** |

---

---

## 0. Entscheidungsgrundlage

*Dieser Abschnitt steht bewusst vorne. Er enthält alles, was jemand braucht, der
auf dieser Studie aufbauen will — nicht nur ihre Befunde, sondern auch ihre
Reichweite.*

### Datenbasis

| | |
|---|---|
| Zeitraum | 2022-03-17 bis 2026-08-30 (**4,45 Jahre**) |
| Symbole | 20 (alle mit Trades) |
| Trades gesamt | 359 (fester Stop) / 396 (ATR-Trailing) |
| davon In-Sample | 219 gefunden, **209 ausgeführt** / 232 gefunden, 231 ausgeführt |
| davon Out-of-Sample | 140 gefunden, **103 ausgeführt** / 164 gefunden, 140 ausgeführt |
| Markt | ausschliesslich Krypto, **ein einziger Zyklus** (Bärenmarkt 2022 → Erholung → 2024er Trends) |

Der einzige klar positive Befund dieser Studie steht auf dem Out-of-Sample-
Abschnitt — und der umfasst **17 Monate und rund 100 bis 140 ausgeführte
Trades**. Das ist wenig.

### Pflicht-Gegenchecks der Projekt-Methodik

| Check | Ergebnis |
|---|---|
| Baseline reproduziert den Bot-Code | **ja** — 359 Trades, PnL-Summe 629,88 %, identische Eckdaten |
| Beide Vorgänger-Studien reproduziert | **ja** — 50 von 50 Referenzwerten exakt |
| **Buy-and-Hold-Vergleich** | **ja, siehe Abschnitt 5** — Strategie schlägt B&H risikoadjustiert deutlich, verliert Out-of-Sample aber klar bei der Rendite |
| Walk-Forward | ja, 4 Fenster, Abschnitt 9 |
| Equity-Simulation | ja, unverändert aus `equity_simulation.py` |

### Belastbarkeit — die wichtigste Tabelle dieser Studie

Zwei unabhängige Unsicherheitsquellen wurden quantifiziert (Details Abschnitt 6):

| Behauptung | Block-Bootstrap, P(Effekt > 0) | überlappen die Reihenfolge-Streubereiche? | Bewertung |
|---|---|---|---|
| Trailing senkt den **Drawdown** | **100,0 %** (gesamt), 99,9 % (IS), 99,2 % (OOS) | nein | **belastbar** |
| Kombination senkt den Drawdown ggü. Trailing allein (OOS) | **99,9 %** | — | belastbar, aber klein (+0,3 bis +2,2 pp) |
| Trailing verbessert die **Calmar-Ratio** | 73,8 % (gesamt), **48,8 % (IS)**, 95,0 % (OOS) | gesamt: nein · OOS: nein | **nur OOS grenzwertig** |
| Vol-Sizing verbessert irgendetwas | 40,1 % / 47,1 % / 53,8 % | ja, fast vollständig | **von Rauschen ununterscheidbar** |
| Kombination schlägt Trailing allein (Calmar) | 31,1 % / 27,6 % / 71,2 % | ja | **kein Beleg** |

Zusätzlich: **60 % der Trades teilen sich einen Einstiegszeitpunkt** mit einem
anderen Trade (Tageskerzen, 20 Symbole). Da die Simulation Kapital sequenziell
vergibt, verschiebt allein diese willkürliche Reihenfolge die berichtete
Baseline-Calmar zwischen **2,98 und 4,90** (berichtet: 4,25). Der Drawdown ist
davon praktisch unberührt.

### Was diesen Befund umstossen würde

- Ein Zeitraum mit einem **zweiten vollständigen Krypto-Zyklus**. Die gesamte
  Historie enthält genau einen; die Trendquartale, in denen der Trailing-Stop
  verliert, sind dieselben, die den Bot profitabel machen.
- Eine **Aktivierung des BTC-Regimefilters** in der Backtest-Kette (siehe
  Annahme 8): er ist ebenfalls ein Risikoreduktions-Mechanismus mit
  Renditekosten und würde vermutlich mit dem Trailing-Stop überlappen.
- Eine **andere Kapitalkonfiguration**. Die Reihenfolge-Empfindlichkeit
  entsteht nur, weil Kapital und Positionslimit knapp sind (in
  `test_vbc_core.py` gezeigt: ohne Engpass ist die Reihenfolge irrelevant).

### Was diese Studie nicht leistet

Keine Aussage über andere Bots. Keine Aussage über die Zukunft — der Bootstrap
misst die Unsicherheit *innerhalb* dieser 4,45 Jahre, nicht die Unsicherheit
über Marktregime, die darin nicht vorkommen. Keine Parametersuche (alle
Parameter unverändert übernommen). Keine Aktivierungsempfehlung.

### Reproduktion

```
cd research/vbc_deepdive
python3 test_vbc_core.py        # 48 Sanity-Checks
python3 verify_reference.py     # 50 Referenzwerte beider Vorgaenger-Studien
python3 run_deepdive.py         # vollstaendige Analyse (~1 min), schreibt results/
```

---

## 1. Kurzfassung

**Die „doppelte Bestätigung" hält der Prüfung nicht stand — und zwar deutlicher,
als die reine Punktschätzung vermuten liess.**

- **Vol-Sizing ist bei diesem Bot von Rauschen nicht zu unterscheiden.**
  P(Verbesserung) = 40 % / 47 % / 54 % je nach Periode — ein Münzwurf. Sein
  Streubereich überlappt fast vollständig mit dem der Baseline, schon allein
  durch die Reihenfolge gleichzeitiger Einstiege. Von einer der beiden
  „Bestätigungen" bleibt damit nichts übrig.
- **Vom Trailing-Stop bleibt genau eine belastbare Aussage: er senkt den
  Drawdown.** Das ist mit P = 100 % (Gesamtzeitraum) das stabilste Ergebnis der
  gesamten Untersuchung und überlebt jede geprüfte Störung. Die daraus
  abgeleitete *Calmar*-Verbesserung ist dagegen nur Out-of-Sample grenzwertig
  belegt (P = 95,0 %) und In-Sample ein Münzwurf (P = 48,8 %).
- **Die Kombination bringt keinen belegbaren Zusatznutzen.** Renditekosten
  stapeln sich vollständig, Drawdown-Reduktionen überlappen sich (rund −2 pp
  Interaktion in jeder Periode). P(Kombination besser als Trailing allein) =
  31 % / 28 % / 71 %.
- **Buy-and-Hold ordnet das Ganze ein:** über den Gesamtzeitraum schlägt die
  Strategie stumpfes Halten klar (Calmar 4,25 vs. 0,29). Out-of-Sample hätte
  Halten aber **+68,81 %** gebracht gegenüber +20,23 % der Baseline — die
  Strategie gewinnt dort ausschliesslich über den Drawdown (−11,33 % vs.
  −59,47 %).

Die ehrliche Gesamtaussage: es waren nie zwei Signale. Es war ein Effekt —
Drawdown-Reduktion durch früheres Aussteigen — plus ein zweiter, der bei
genauer Messung verschwindet.

---

## 2. Baseline-Regressionscheck

`verify_reference.py` bestätigt **50 von 50 Referenzwerten** aus drei
unabhängigen Richtungen:

| Quelle | Ergebnis |
|---|---|
| unveränderte `equity_simulation.py` des Bots | 359 Trades, PnL-Summe 629,88 %, gleicher erster Entry / letzter Exit |
| `research/volatility_scaled_sizing/` (PR #18) | Baseline + Vol-Sizing, IS/OOS + alle 4 WF-Fenster — exakt |
| `research/trailing_stops/` (PR #21) | Baseline + ATR-Trailing, full/IS/OOS + alle 4 WF-Fenster, k = 0,8956, Trade-Anzahlen — exakt |

Nötig, weil beide Vorgänger-Branches nicht gemergt sind: `vbc_core.py` enthält
deren Bausteine als dokumentierte Übernahme, jede Funktion mit Herkunftsangabe.

---

## 3. Methodik

### Die vier Varianten (2 × 2)

| | feste Positionsgrösse | vol-skalierte Grösse |
|---|---|---|
| **fester 5 %-Stop** | **A** `baseline` | **B** `vol_sizing` |
| **ATR-Trailing-Stop** | **C** `trailing` | **D** `combined` |

Zwei Trade-Sätze (359 / 396), auf die je zwei Gewichtungen gelegt werden. Dass
der Trailing-Stop mehr Trades erzeugt, folgt aus der Bot-Logik: kein
Pyramiding, der nächste Scan startet erst nach dem Ausstieg — frühere Ausstiege
setzen Kapazität frei.

### Unverändert übernommene Parameter

ATR-14 · k = 0,8956 (auf den Median der IS-Baseline-Stop-Distanz kalibriert) ·
Vol-Fenster 90 Balken · Clip-Faktor 4,0 · Gewichts-Normierung auf Mittelwert 1,0
je Periode · `TRAIN_SPLIT_RATIO = 0,7` · dieselben 4 Walk-Forward-Fenster ·
Calmar = Rendite % / |Max Drawdown %|. **Kein Parameter wurde neu gesucht.**

### Neu in dieser Studie: zwei Unsicherheitsmasse

**Block-Bootstrap** (`bootstrap.py`): zirkulärer Moving-Block-Bootstrap über
Kalendermonate, Blocklänge 3 Monate, 2000 Replikate, fester Seed. Ein naiver
Trade-Bootstrap wäre falsch — die Simulation ist pfadabhängig und der Max
Drawdown eine Eigenschaft der *Reihenfolge*. Blöcke erhalten lokale Struktur;
die Zeitstempel werden beim Zusammensetzen verschoben, sodass eine gültige
Historie entsteht. **Gepaart:** alle vier Varianten laufen je Replikat auf
derselben gezogenen Zeitachse, sodass sich die Unsicherheit der
Marktphasen-Auswahl aus der Differenz herauskürzt.

**Reihenfolge-Sensitivität**: 500 Permutationen der Reihenfolge gleichzeitiger
Einstiege, sonst nichts verändert. Das ist keine Stichprobenunsicherheit,
sondern eine Implementierungs-Willkür, die in jedem einzelnen Lauf steckt.

Für die 24.000 Simulationen des Bootstraps existiert ein NumPy-Schnellpfad
(54 Sekunden statt gut 30 Minuten). `test_vbc_core.py` prüft, dass er auf
Daten **mit mehrfach belegten Einstiegszeitpunkten** bit-genau dieselben
Ergebnisse liefert wie der Referenzcode — genau daran war ein erster Entwurf
gescheitert (pandas' `sort_values` ist per Default nicht stabil). Alle
Punktschätzer im Bericht stammen weiterhin ausschliesslich aus dem
Referenzpfad.

---

## 4. Getroffene Annahmen (vollständig)

1. **Vendoring statt Import** der Bausteine aus PR #18/#21, abgesichert über den
   50-Punkte-Regressionscheck.
2. **Gewichte je Periode normiert** (Mittelwert 1,0) — Konvention der
   Vol-Sizing-Studie. Für die Trade-Ebenen-Analyse (Abschnitt 8) dagegen über
   den Gesamtzeitraum, weil dort gefragt ist, welche Trades den GESAMTeffekt
   tragen.
3. **`k` einmalig auf den In-Sample-Baseline-Trades kalibriert.**
4. **Quartale als Episoden-Raster**, jedes als eigenständige Simulation ab
   10.000. Nebenwirkung: die Quartalsrenditen verketten sich nicht exakt zum
   Gesamtzeitraum.
5. **Beitragsmasse in PnL-Prozentpunkten, nicht in Kapitaleinheiten** — die
   Kapitalwirkung eines einzelnen Trades ist pfadabhängig und nicht sauber
   zurechenbar.
6. **Renditen additiv im Log-Raum, Drawdown in Prozentpunkten.**
7. **Rangkorrelation als Pearson-Korrelation der Ränge** (kein `scipy` im
   Projekt, und dafür soll keines eingeführt werden).
8. **BTC-Regimefilter NICHT angewendet.** `live_params.py` führt
   `BTC_REGIME_FILTER_ENABLED = True`, die bot-eigene `equity_simulation.py`
   wendet ihn aber nicht an (nur `forward_test.py` tut das). Beide
   Vorgänger-Studien sind der `equity_simulation.py` gefolgt; diese Studie
   ebenfalls, sonst wäre der Regressionscheck unmöglich. Der Filter wirkt nur
   auf Einstiege und damit in allen vier Varianten gleich. **Das bleibt eine
   ungeklärte Divergenz zwischen Live-Konfiguration und Backtest-Kette.**
9. **Schwelle 60 %** für „durch eine Einzelepisode getrieben"; 3-von-4-Regel
   für Walk-Forward-Stabilität — dokumentierte Heuristiken, keine Standardmasse.
10. **Bootstrap-Blocklänge 3 Monate**, 2000 Replikate, Seed 20260907. Die
    Blocklänge ist eine Konvention (ein Quartal), nicht optimiert; sie
    balanciert Erhalt lokaler Struktur gegen Zahl unterscheidbarer Blöcke.
11. **Buy-and-Hold über die unveränderte bot-eigene Funktion** gerechnet
    (`buy_and_hold_benchmark.py::calculate_buy_and_hold`), nur der
    Eingabezeitraum wird zugeschnitten. Der Wert ist für alle vier Varianten
    identisch — genau deshalb ist er die unabhängige Aussenreferenz.
12. **Calmar-Replikate mit |Drawdown| < 0,1 % werden verworfen** (der Nenner
    explodiert). In dieser Studie trat der Fall in keinem einzigen Replikat auf
    — die Zahl wird trotzdem ausgewiesen.

---

## 5. Ergebnisse

### Die vier Kombinationen (Rendite % / Max Drawdown % / **Calmar**)

| Periode | A Baseline | B Vol-Sizing | C Trailing | D Kombiniert | **Buy-and-Hold** |
|---|---|---|---|---|---|
| Gesamtzeitraum | 71,26 / −16,77 / **4,25** | 61,09 / −14,96 / **4,08** | 45,65 / −5,76 / **7,93** | 37,88 / −5,93 / **6,39** | 19,45 / −67,90 / **0,29** |
| In-Sample | 40,89 / −16,77 / **2,44** | 37,86 / −15,17 / **2,50** | 12,96 / −5,76 / **2,25** | 9,78 / −6,10 / **1,60** | 25,34 / −67,90 / **0,37** |
| Out-of-Sample | 20,23 / −11,33 / **1,79** | 16,20 / −8,04 / **2,01** | 28,12 / −5,58 / **5,04** | 24,31 / −4,05 / **6,00** | 68,81 / −59,47 / **1,16** |

**Buy-and-Hold-Einordnung (Pflicht-Gegencheck):** über den Gesamtzeitraum
schlägt jede Variante stumpfes Halten der 20 Coins klar — nicht über die
Rendite (71,26 % vs. 19,45 %, aber die Strategie ist ja nur zeitweise
investiert), sondern vor allem über den Drawdown (−16,77 % vs. −67,90 %).
**Out-of-Sample kippt das Bild bei der Rendite:** Halten hätte +68,81 %
gebracht, die Baseline nur +20,23 %, die beste Variante +28,12 %. Die
Strategie gewinnt dort ausschliesslich über das Risiko. Wer den Drawdown nicht
als Kostenfaktor gewichtet, hätte in diesem Abschnitt mit Nichtstun mehr
verdient — das gehört in jede Abwägung.

### Additivität

| Periode | Rendite erwartet → tatsächlich | Interaktion | Drawdown erwartet → tatsächlich | Interaktion |
|---|---|---|---|---|
| Gesamtzeitraum | 37,00 % → 37,88 % | **+0,88 pp** | −3,95 % → −5,93 % | **−1,98 pp** |
| In-Sample | 10,53 % → 9,78 % | **−0,75 pp** | −4,16 % → −6,10 % | **−1,94 pp** |
| Out-of-Sample | 23,83 % → 24,31 % | **+0,48 pp** | −2,29 % → −4,05 % | **−1,76 pp** |

Die Renditekosten stapeln sich vollständig, die Drawdown-Reduktionen
überlappen sich — in allen drei Perioden um rund 2 Prozentpunkte. Man zahlt
beide Mechanismen voll und bekommt ihren Schutz nur einmal.

---

## 6. Belastbarkeit (neu)

### 6.1 Block-Bootstrap — 95-%-Intervalle der gepaarten Differenz

**Calmar-Differenz:**

| Vergleich | Gesamtzeitraum | In-Sample | Out-of-Sample |
|---|---|---|---|
| Vol-Sizing − Baseline | −4,03 … 2,52 · P = **40,1 %** | −2,88 … 2,27 · P = **47,1 %** | −1,68 … 2,18 · P = **53,8 %** |
| Trailing − Baseline | −10,03 … 14,48 · P = 73,8 % | −11,16 … 6,86 · P = **48,8 %** | −0,56 … 16,14 · P = **95,0 %** |
| Kombiniert − Baseline | −10,95 … 13,58 · P = 70,7 % | −11,38 … 5,19 · P = 41,9 % | −0,68 … 19,15 · P = 94,7 % |
| Kombiniert − Trailing | −4,91 … 2,99 · P = **31,1 %** | −3,41 … 1,00 · P = 27,6 % | −1,80 … 5,94 · P = 71,2 % |

**Drawdown-Differenz** (positiv = geringerer Drawdown, also besser):

| Vergleich | Gesamtzeitraum | In-Sample | Out-of-Sample |
|---|---|---|---|
| Vol-Sizing − Baseline | −2,34 … 6,18 · P = 79,5 % | −2,53 … 6,06 · P = 73,5 % | −0,49 … 5,05 · P = 94,7 % |
| Trailing − Baseline | **+4,67 … +30,57 · P = 100,0 %** | +4,47 … +29,87 · P = 99,9 % | +0,87 … +9,47 · P = 99,2 % |
| Kombiniert − Baseline | **+5,22 … +31,14 · P = 100,0 %** | +4,16 … +30,17 · P = 99,9 % | +1,60 … +10,93 · P = 100,0 % |
| Kombiniert − Trailing | −1,48 … 2,30 · P = 73,8 % | −2,19 … 1,84 · P = 47,5 % | **+0,29 … +2,17 · P = 99,9 %** |

**Das ist der zentrale neue Befund dieser Studie.** Die Drawdown-Reduktion des
Trailing-Stops ist in jeder Periode praktisch sicher (P ≥ 99,2 %) und in der
Grössenordnung erheblich (+4,7 bis +30,6 Prozentpunkte im Gesamtzeitraum). Die
daraus abgeleitete **Calmar**-Verbesserung ist es nicht: über den
Gesamtzeitraum P = 73,8 %, In-Sample **48,8 % — ein exakter Münzwurf**, nur
Out-of-Sample 95,0 % und dort mit einem Intervall, das die Null gerade eben
noch berührt (−0,56).

Der Grund für die Diskrepanz: der Drawdown wird zuverlässig kleiner, die
Rendite aber ebenso zuverlässig auch — und welcher der beiden Effekte in der
Ratio überwiegt, hängt stark von der gezogenen Marktphasen-Mischung ab.

### 6.2 Reihenfolge gleichzeitiger Einstiege

60 % der Trades teilen ihren Einstiegszeitpunkt mit mindestens einem anderen
(grösste Gruppe: 9 Trades an einem Tag). Streubereich über 500 Permutationen,
Gesamtzeitraum:

| Variante | Calmar | Rendite % | Max Drawdown % |
|---|---|---|---|
| Baseline | 2,98 … 4,90 (berichtet **4,25**) | 49,94 … 82,14 | −16,77 … −16,77 |
| Vol-Sizing | 2,50 … 4,75 (berichtet 4,08) | 37,30 … 70,98 | −14,96 … −14,93 |
| Trailing | 6,65 … 8,95 (berichtet 7,93) | 39,02 … 51,55 | −5,96 … −5,76 |
| Kombiniert | 5,33 … 6,93 (berichtet 6,39) | 31,59 … 41,08 | −5,93 … −5,93 |

Drei Schlüsse:

1. **Baseline und Trailing überlappen nicht** (4,90 < 6,65) — die Kernaussage
   „Trailing ist risikoadjustiert besser" übersteht diese Willkür.
2. **Baseline und Vol-Sizing überlappen fast vollständig** — der
   Vol-Sizing-Effekt ist kleiner als die Reihenfolge-Willkür und damit
   inhaltlich nicht interpretierbar.
3. **Trailing und Kombiniert überlappen** (5,33 … 6,93 gegen 6,65 … 8,95) — die
   Aussage „die Kombination ist schlechter als Trailing allein" ist **nicht**
   robust. Sie deckt sich aber mit dem Bootstrap-Befund, dass die Kombination
   auch nicht *besser* ist.

Der **Drawdown ist gegenüber der Reihenfolge praktisch invariant** (Baseline
exakt −16,77 % in allen 500 Permutationen). Erneut dieselbe Trennlinie: die
Risikodimension ist die stabile, die Renditedimension die wackelige.

Die berichtete Baseline-Calmar von 4,25 liegt über dem Permutations-Median von
3,52 — die tatsächlich verwendete Reihenfolge ist also eine eher günstige
Ziehung. Das relativiert den Ausgangspunkt aller Vergleiche leicht zugunsten
der Alternativvarianten.

---

## 7. Episoden-Robustheit (quartalsweise, 19 Quartale)

- **Richtung breit verteilt:** Trailing besser in 12 von 19 Quartalen; kein
  Quartal reisst die 60-%-Schwelle (grösstes 2024Q1 mit 23,2 %).
- **Grössenordnung konzentriert:** die drei grössten Abweichungen (2024Q1
  −24,43, 2024Q4 −22,06, 2023Q1 −11,29 pp) tragen 54,9 % — und sind **alle drei
  Verluste**, in genau den stärksten Trendquartalen.
- **Drawdown-Reduktion in 4 von 4 Walk-Forward-Fenstern vorhanden.**

**Bedingte Struktur** — Korrelation zwischen der Quartalsrendite der Baseline
und dem Vorteil des Mechanismus im selben Quartal:

| Variante | Korrelation | Baseline negativ (10 Q) | Baseline positiv (9 Q) |
|---|---|---|---|
| Vol-Sizing | −0,58 | +0,45 pp, besser in 40 % | −1,90 pp, besser in 22 % |
| Trailing | **−0,88** | **+3,06 pp, besser in 100 %** | −5,77 pp, besser in 22 % |
| Kombiniert | −0,91 | +3,06 pp, besser in 100 % | −6,44 pp, besser in 22 % |

Der Trailing-Stop war in **jedem** der zehn Quartale mit negativer Baseline
besser und in nur zwei der neun mit positiver. Das ist das Profil einer
Versicherung, nicht eines Edges — und es erklärt, warum die Drawdown-Wirkung
belastbar ist, die Calmar-Wirkung aber nicht: ob sich eine Versicherung
„lohnt", hängt davon ab, wie viele Schadensfälle im Betrachtungszeitraum
liegen.

---

## 8. Mechanismus-Unabhängigkeit

| Kennzahl | Wert |
|---|---|
| Korrelation der beiden Volatilitäts-Masse (ATR/Kurs vs. realisierte Vol) | **0,83** (Rang 0,85) |
| Korrelation der Trade- / Quartalsbeiträge | **+0,45** / **+0,57** |
| beide halfen / schadeten / gegenläufig (von 357 gemeinsamen Trades) | 149 / 49 / 159 |
| Überlappung der 20 grössten Beiträge | **0** (Zufallserwartung 1,12) |
| Summe Vol-Sizing- / Trailing-Beitrag | **−40,7 pp** / **−380,8 pp** |

Formal messen die Mechanismen Verschiedenes (True Range über 14 Balken gegen
Standardabweichung der Log-Returns über 90 Balken), empirisch fast dasselbe.
In der Breite überlappen sie sich, an den Extremen sind sie disjunkt.
**Beide Beitragssummen sind negativ** — der gesamte Calmar-Nutzen kommt aus
dem Nenner.

Vol-Sizing wirkt zusätzlich über die Trade-**Auswahl**: die kombinierte
Variante führt 367 statt 370 Trades aus, weil grössere Einzelpositionen
gelegentlich das freie Kapital erschöpfen.

---

## 9. Walk-Forward der kombinierten Variante

Calmar, dieselben 4 Fenster wie in der Trailing-Stop-Studie:

| Fenster | A | B | C | D | D > C? |
|---|---|---|---|---|---|
| W1 2022-03 … 2023-04 | −0,20 | −0,23 | 0,71 | **1,11** | ja |
| W2 2023-04 … 2024-06 | 3,85 | 3,30 | 0,04 | **−0,16** | nein |
| W3 2024-06 … 2025-07 | 3,32 | 3,85 | 6,10 | **5,52** | nein |
| W4 2025-07 … 2026-08 | 0,17 | 0,00 | 3,14 | **4,20** | ja |

Gegenüber der Baseline in 3/4 Fenstern besser; gegenüber dem besseren
Einzelmechanismus nur **2/4** — nach der 3-von-4-Regel nicht stabil. Der
Bootstrap bestätigt das unabhängig (P = 31 % im Gesamtzeitraum).

---

## 10. Die Kernfrage: zwei Signale oder eines, zweimal gemessen?

**Nach der Unsicherheitsrechnung ist die Antwort schärfer als zuvor: es war
nicht einmal ein Signal plus ein zweites — es war ein Effekt plus Rauschen.**

- **Vol-Sizing**: P(Verbesserung) zwischen 40 % und 54 % über alle Perioden.
  Sein Streubereich überlappt fast vollständig mit dem der Baseline, bereits
  durch die Reihenfolge-Willkür allein. Es gibt hier nichts zu bestätigen.
- **Trailing-Stop**: genau ein belastbarer Effekt — die Drawdown-Reduktion
  (P = 100 % im Gesamtzeitraum). Die Calmar-Verbesserung folgt daraus **nicht**
  automatisch und ist statistisch nur Out-of-Sample grenzwertig.
- **Gemeinsamkeit statt Unabhängigkeit**: gemeinsame Eingangsgrösse (0,83),
  gemeinsame bedingte Struktur (−0,88 / −0,58), überlappende statt additive
  Drawdown-Wirkung, kein Kombinationsgewinn.
- **Der einzige Gegenbefund** bleibt die Disjunktheit der 20 grössten
  Einzelbeiträge. Bei 357 Trades und einer Erwartung von 1,12 ist das aber ein
  schwaches Indiz und mit Stichprobenrauschen gut vereinbar.

Und eine Ebene tiefer, unverändert gültig: der gemessene Effekt ist keine
Ertragsverbesserung. Beide Mechanismen senken den summierten PnL und die
Gesamtrendite. Der gesamte Calmar-Gewinn kommt aus dem Nenner.

---

## 11. Gesamteinschätzung (unaufgeregt, ohne Handlungsempfehlung)

Der Anlass war die Vermutung, dieser Bot sei über zwei unabhängige Wege als
verbesserbar bestätigt. Nach Hinzunahme von Buy-and-Hold-Vergleich,
Block-Bootstrap und Reihenfolge-Sensitivität bleibt davon:

- **Eine belastbare Aussage:** der ATR-Trailing-Stop senkt den Drawdown dieses
  Bots deutlich und über jede geprüfte Störung hinweg stabil (−16,77 % →
  −5,76 % im Gesamtzeitraum, P = 100 %).
- **Eine unbelegte Aussage:** dass sich das risikoadjustiert lohnt. In-Sample
  ein Münzwurf, Out-of-Sample grenzwertig, über den Gesamtzeitraum nicht
  gesichert. Der Grund ist nicht Messfehler, sondern Substanz: die Rendite
  sinkt ähnlich verlässlich wie der Drawdown.
- **Eine widerlegte Aussage:** dass Vol-Sizing bei diesem Bot etwas beiträgt.
- **Eine offene Abwägung:** Out-of-Sample hätte stumpfes Halten der 20 Coins
  mehr als das Dreifache der Baseline-Rendite gebracht, bei fünffachem
  Drawdown. Wie diese beiden Grössen gegeneinander stehen, ist eine
  Präferenzfrage und keine Backtest-Frage.

Ob eine Versicherung, die zuverlässig Rendite kostet und deren
risikoadjustierter Nutzen nicht gesichert ist, für dieses Portfolio erwünscht
ist, kann der Backtest nicht entscheiden. Er kann nur zeigen, dass es genau
dieser Tausch ist — und mit welcher Sicherheit. Die Entscheidung liegt bewusst
beim Nutzer in einer separaten, künftigen Session.

---

## 12. Offene Fragen für eine mögliche Vertiefung

- Die **Divergenz zwischen `live_params.py` (`BTC_REGIME_FILTER_ENABLED = True`)
  und `equity_simulation.py`** (Filter nicht angewendet) betrifft sämtliche
  Backtest-Zahlen dieses Bots, auch die der vier Vorgänger-Studien. Da der
  Filter ebenfalls ein Risikoreduktions-Mechanismus mit Renditekosten ist, wäre
  seine Überlappung mit dem Trailing-Stop die naheliegende Fortsetzung.
- Die **Reihenfolge-Empfindlichkeit** (60 % geteilte Zeitstempel) betrifft
  ebenfalls alle bisherigen Studien und alle Bots auf Tageskerzen. Ob die dort
  berichteten Unterschiede grösser sind als diese Willkür, ist bislang für
  keinen anderen Bot geprüft.
- Die **Disjunktheit der grössten Einzelbeiträge** ist der einzige verbliebene
  Hinweis auf zwei Mechanismen. Eine gezielte Betrachtung dieser Trades könnte
  klären, ob dahinter Struktur oder Rauschen steckt.

---

## 13. Explizit ausserhalb des Scopes

Jede Untersuchung anderer Bots, jede Live-Code-Änderung, jede
Aktivierungsempfehlung, jede neue Parameter-Optimierung.

---

## 14. Dateien

| Datei | Inhalt |
|---|---|
| `vbc_core.py` | ATR/Trailing, realisierte Volatilität, inverse Vol-Gewichte, gewichtete Portfolio-Simulation, Kennzahlen — jede Funktion mit Herkunftsangabe |
| `bootstrap.py` | zirkulärer Moving-Block-Bootstrap inkl. NumPy-Schnellpfad |
| `verify_reference.py` | Regressionscheck gegen Bot-Code und beide Vorgänger-Studien (50 Werte) |
| `test_vbc_core.py` | 48 Sanity-Checks inkl. Äquivalenz Schnellpfad ↔ Referenzpfad |
| `run_deepdive.py` | 2×2-Varianten, IS/OOS, 4 WF-Fenster, Quartale, Buy-and-Hold, Additivität, bedingte Struktur, Trade-Überlappung, Bootstrap, Reihenfolge-Sensitivität |
| `results/vbc_deepdive.json` | alle Ergebnisse maschinenlesbar |
| `results/trades_static_stop.csv`, `results/trades_atr_trailing.csv` | beide Trade-Sätze auf Trade-Ebene |
