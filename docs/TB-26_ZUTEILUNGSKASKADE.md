# TB-26 — Die Zuteilungskaskade

**Stand: 13.09.2026.** Behebt den Befund aus TB-23: acht von neun Bots waren
nicht deterministisch, weil bei knappem Platz die Zeilenreihenfolge des
Trade-DataFrames entschied — und die ist die Symbolreihenfolge von
`config/sp500_top150.txt` bzw. `config/top25_symbols.txt`.

---

## 1. Meldet der Determinismus-Test neunmal grün?

**Ja.**

```
python3 shared/determinismus.py --voll --perms 20
```

| Bot | vorher | nachher | umstrittene Trades |
|---|---|---|---:|
| `elliott_wave` | NUR REIHENFOLGE | **DETERMINISTISCH** | 0,0 % *(war 0,0 %)* |
| `elliott_wave_stocks` | NICHT DETERMINISTISCH | **DETERMINISTISCH** | 0,0 % *(war 28,2 %)* |
| `rsi2_crypto` | NICHT DETERMINISTISCH | **DETERMINISTISCH** | 0,0 % *(war 14,4 %)* |
| `rsi2_mean_reversion` | NICHT DETERMINISTISCH | **DETERMINISTISCH** | 0,0 % *(war 27,1 %)* |
| `t3_supertrend` | NICHT DETERMINISTISCH | **DETERMINISTISCH** | 0,0 % *(war 14,6 %)* |
| `turtle_soup_crypto` | NICHT DETERMINISTISCH | **DETERMINISTISCH** | 0,0 % *(war 30,6 %)* |
| `turtle_soup_stocks` | NICHT DETERMINISTISCH | **DETERMINISTISCH** | 0,0 % *(war 36,4 %)* |
| `volatility_breakout` | NICHT DETERMINISTISCH | **DETERMINISTISCH** | 0,0 % *(war 46,6 %)* |
| `volatility_breakout_crypto` | NICHT DETERMINISTISCH | **DETERMINISTISCH** | 0,0 % *(war 11,6 %)* |

Rückgabewert 0, Laufzeit 781 s (vorher 616 s). Alle drei Vergleichsebenen —
Signalmenge, ausgeführte Trades, Kapitalpfad — sind über alle 20 Permutationen
identisch.

`elliott_wave` stand vorher auf **NUR REIHENFOLGE**, nicht auf
„deterministisch": dieselben Trades, aber bei gleichem Zeitstempel in anderer
Abrechnungsreihenfolge. Das ist mit derselben Änderung erledigt (die
Ausstiegsreihenfolge ist jetzt ebenfalls festgelegt).

---

## 2. Welche Kennzahl hat sich je Bot wie verschoben?

**Die Menge der erzeugten Trades ist bei allen neun unverändert** — also keine
Strategieänderung. Verändert ist, welche davon Kapital bekommen, wenn es knapp
wird.

Die „vorher"-Spanne ist die Streuung über 20 Permutationen; die Spalte
**„bisher abgelegt"** ist die Zahl, die im Repo steht (Lauf mit der
Originalreihenfolge) — sie war eine von zwanzig.

### Rendite

| Bot | Spanne vorher | bisher abgelegt | **nachher** | Lage in der Spanne |
|---|---|---:|---:|---:|
| `elliott_wave` | 67,77 (ein Wert) | 67,77 % | **67,77 %** | unverändert |
| `elliott_wave_stocks` | 321,80 … 424,42 | 352,72 % | **419,07 %** | 95 % |
| `rsi2_crypto` | 25,58 … 34,07 | 28,37 % | **27,19 %** | 19 % |
| `rsi2_mean_reversion` | 27,90 … 45,62 | 36,75 % | **36,28 %** | 47 % |
| `t3_supertrend` | 117,87 … 138,12 | 129,64 % | **121,70 %** | 19 % |
| `turtle_soup_crypto` | 123,77 … 190,23 | 177,59 % | **152,84 %** | 44 % |
| `turtle_soup_stocks` | 121,84 … 164,68 | 145,59 % | **138,15 %** | 38 % |
| `volatility_breakout` | 145,16 … 269,47 | 224,41 % | **209,59 %** | 52 % |
| `volatility_breakout_crypto` | 46,29 … 73,45 | 49,03 % | **68,13 %** | 80 % |

Alle neun neuen Werte liegen **innerhalb** der gemessenen Spanne. Der Median
der Lagen ist 44 % — die Kaskade landet also nicht systematisch am oberen
Rand. Zwei Ausreißer nach oben (`elliott_wave_stocks` 95 %,
`volatility_breakout_crypto` 80 %) und keiner nach unten.

### Maximaler Drawdown

| Bot | Spanne vorher | bisher abgelegt | **nachher** | Lage |
|---|---|---:|---:|---:|
| `elliott_wave` | −10,17 (ein Wert) | −10,17 % | **−10,17 %** | unverändert |
| `elliott_wave_stocks` | −23,22 … −22,19 | −22,44 % | **−22,97 %** | 24 % |
| `rsi2_crypto` | −13,96 … −12,66 | −13,30 % | **−13,94 %** | 2 % |
| `rsi2_mean_reversion` | −22,15 … −18,93 | −21,05 % | **−19,53 %** | 81 % |
| `t3_supertrend` | −22,57 … −22,14 | −22,20 % | **−22,40 %** | 40 % |
| `turtle_soup_crypto` | −41,24 … −32,40 | −32,40 % | **−34,85 %** | 72 % |
| `turtle_soup_stocks` | −30,58 … −28,45 | −29,91 % | **−29,07 %** | 71 % |
| `volatility_breakout` | −25,64 … −22,89 | −23,97 % | **−22,46 %** | **außerhalb** |
| `volatility_breakout_crypto` | −16,29 (ein Wert) | −16,29 % | **−16,29 %** | unverändert |

> **`volatility_breakout` fällt aus der Spanne** — sein Drawdown ist mit
> −22,46 % **flacher als in jeder** der zwanzig gemessenen Permutationen
> (beste vorher: −22,89 %). Das ist kein Fehler, aber es gehört benannt: es
> ist genau die Wirkung, die Stufe 2 haben soll — wer bei gleichem Rang den
> unkorrelierteren Kandidaten nimmt, baut weniger Klumpen auf, und ein
> Klumpen ist die Hauptursache eines tiefen Drawdowns. Zwanzig Permutationen
> sind allerdings eine Stichprobe und keine Randverteilung; dass die Kaskade
> den Drawdown *systematisch* senkt, ist damit **nicht** gezeigt. Bei drei
> anderen Bots liegt der neue Drawdown in der schlechteren Hälfte.

**Keine dieser Zahlen ist eine Verbesserung der Strategie.** Vorher gab es
keine einzelne richtige Zahl, sondern eine Spanne, von der die
Dateisortierung eine auswählte. Jetzt gibt es eine, und sie hat einen
benannten Grund.

---

## 3. Die Regel

Vier Stufen, lexikographisch; jede bekommt nur, was auf allen vorherigen
gleichauf liegt. Sie steht **an einer einzigen Stelle**:
`shared/zuteilung.py`.

| Rang | Kriterium | Richtung | wo definiert |
|---:|---|---|---|
| 1 | strategieeigene stetige **Signalstärke**, falls vorhanden | stärker zuerst | `SIGNALSPALTE` in der `equity_simulation.py` des Bots |
| 2 | **Diversifikationsbeitrag** — 60-Tage-Korrelation mit dem allokationsgewichteten Buch | niedriger zuerst; entfällt bei leerem Buch | `shared/zuteilung.py` |
| 3 | **Liquidität** — Median des Dollar-Volumens der letzten 20 Tage | höher zuerst | `shared/zuteilung.py` |
| 4 | **seeded Zufall**, Startwert `SEED = 20260913` | — | `shared/zuteilung.py` |

Dieselbe Regel legt jetzt auch die **Reihenfolge gleichzeitiger Ausstiege**
fest (nach Stufe 4). Sie entscheidet über niemandes Platz, aber über die
Zwischenstände der Kapitalkurve und damit über den gemessenen Drawdown; vorher
galt auch dort die Dateireihenfolge.

**Fehlende Angaben** bekommen auf jeder Stufe den **Median der Kandidaten, für
die der Wert vorliegt** — nicht das Ende (benachteiligte junge Symbole) und
nicht die 0 (bevorzugte sie). Liegt für niemanden ein Wert vor, entfällt die
Stufe.

### Welcher Bot hat einen Primärschlüssel?

Gemessen mit `research/zuteilungskaskade/messung_primaerschluessel.py`;
Einzelheiten und Begründungen in `research/zuteilungskaskade/BERICHT.md`.

| Bot | Primärschlüssel | Grund |
|---|---|---|
| `rsi2_crypto` | **`rsi_at_entry`**, aufsteigend | 330 verschiedene Werte, 0,0 % Gleichstände |
| `rsi2_mean_reversion` | **`rsi_at_entry`**, aufsteigend | 442 Werte, 2,1 % Gleichstände — knapp über der 2-%-Marke, Ermessensentscheidung |
| `elliott_wave` | keiner | `fib_score`: nur 5 Werte, 38,6 % bleiben gleichauf |
| `elliott_wave_stocks` | keiner | `fib_score`: nur 5 Werte, 72,7 % bleiben gleichauf |
| `turtle_soup_crypto` | keiner | `setup_day_low` ist ein Kursniveau, keine Signalstärke — und nicht skalenfrei |
| `turtle_soup_stocks` | keiner | dito |
| `t3_supertrend` | keiner | die Trade-Tabelle führt keine passende Größe |
| `volatility_breakout` | keiner | dito |
| `volatility_breakout_crypto` | keiner | dito |

> **Das weicht vom Auftrag ab**, der „sieben führen keine" annahm. Es sind
> fünf ohne und zwei mit untauglichem Kandidaten — und **zwei mit einer
> brauchbaren**: der RSI(2) zum Einstieg. Er ist keine neue Größe
> (`backtest_rsi2.py` schreibt ihn seit jeher mit), er ist die Signalstärke
> dieser Strategie (tiefer = überverkaufter = stärker), und die Richtung kommt
> aus der Strategielogik, nicht aus dem Backtest-Ergebnis.
>
> **Umkehrbar in einer Zeile:** `SIGNALSPALTE = None` in der
> `equity_simulation.py` des jeweiligen Bots. Dann beginnt die Kaskade dort
> bei Stufe 2, und sonst ändert sich nichts.

---

## 4. Wie oft welche Stufe entscheidet

Aus dem Protokoll, das jeder Bot am Ende seines Laufs ausgibt (Startwert
20260913, Datenstand 13.09.2026):

| Bot | umstrittene Zuteilungen | Stufe 1 | Stufe 2 | Stufe 3 | Stufe 4 | Korrelationen | Rechenzeit |
|---|---:|---:|---:|---:|---:|---:|---:|
| `elliott_wave` | 0 | – | – | – | – | 0 | 0,00 s |
| `elliott_wave_stocks` | 59 | 0 | 57 | 2 | 0 | 523 | 0,05 s |
| `rsi2_crypto` | 42 | **42** | 0 | 0 | 0 | 0 | 0,00 s |
| `rsi2_mean_reversion` | 712 | **702** | 10 | 0 | 0 | 20 | 0,03 s |
| `t3_supertrend` | 63 | 0 | 58 | 0 | **5** | 190 | 0,02 s |
| `turtle_soup_crypto` | 312 | 0 | 292 | 20 | 0 | 1 997 | 0,23 s |
| `turtle_soup_stocks` | 1 952 | 0 | 1 952 | 0 | 0 | 27 854 | 2,82 s |
| `volatility_breakout` | 555 | 0 | 554 | 0 | **1** | 2 484 | 0,29 s |
| `volatility_breakout_crypto` | 9 | 0 | 9 | 0 | 0 | 42 | 0,01 s |
| **Summe** | **3 704** | **744** | **2 932** | **22** | **6** | 33 110 | 3,45 s |

Drei Beobachtungen dazu:

* **Der Zufall entscheidet sechsmal** — bei 3 704 umstrittenen Zuteilungen
  über neun Bots, also in 0,16 % der Fälle. Die Stufen davor tragen praktisch
  alles. Das ist die Antwort auf den naheliegenden Einwand, eine Regel mit
  Zufall auf der letzten Stufe sei „doch auch nur willkürlich": sie ist es an
  0,16 % der Entscheidungen, und dort sichtbar und protokolliert.
* **Stufe 2 trägt die Hauptlast** (79 %), genau wie erwartet: sieben der neun
  Bots haben keinen Primärschlüssel.
* **Die Zahl der umstrittenen Zuteilungen ist viel kleiner als die Zahl der
  gleichzeitigen Trades** (3 704 gegen zehntausende). Passen alle Kandidaten
  eines Zeitpunkts ohnehin hinein, ist ihre Reihenfolge für das Ergebnis
  bedeutungslos — dann wird die Kaskade gar nicht erst befragt.

Der Aufwand ist damit vernachlässigbar: 3,45 s Kaskade über alle neun Bots,
dazu 8,1 s für den einmaligen Aufbau der Tagesreihen. Der Gesamtlauf von
`shared/determinismus.py --voll --perms 20` (der alles zwanzigmal rechnet)
steigt von 616 s auf 781 s.

---

## 5. Wo die Änderung sitzt

| Datei | Art |
|---|---|
| `shared/zuteilung.py` | **neu** — die Kaskade und die Kapitalsimulation, an einer Stelle für alle neun Bots |
| `shared/test_zuteilung.py` | **neu** — Selbsttest, je Stufe ein Prüffall plus sechs Mutationsproben |
| `research/zuteilungskaskade/` | **neu** — Messung der Primärschlüssel und die Festlegungen dazu |
| `strategies/*/equity_simulation.py` (9×) | `simulate_portfolio()` ruft die gemeinsame Fassung auf; neu ist je Bot nur die Zeile `SIGNALSPALTE` |
| `shared/portfolio_overview.py` | Live-Trades führen keine Signalstärke — das wird jetzt ausdrücklich gesagt statt auf einen Fehler ankommen zu lassen |
| `shared/test_determinismus.py` | dreht die Erwartung um: der unveränderte Bot ist jetzt der grüne Fall, der rote ist eine Kopie mit zurückgedrehter Zuteilung |
| `docs/TESTAUFTRAG_TB-26_zuteilungskaskade.md` | **neu** — eigenständig ausführbarer Testauftrag |

**Nicht angefasst:** `live_params.py`, `forward_test.py`, `multi_symbol_optimise.py`,
`results/*/equity_curve.csv`, `multi_symbol_optimisation_results.csv`, die
Symboldateien, alles unter `broker/`, Crontab und launchd-Vorlagen.

**Kein Parameter geändert** — auch nicht `MAX_CONCURRENT_POSITIONS` bei
`volatility_breakout`, wo TB-23 gefunden hat, dass das Limit 15 bei
rechnerisch höchstens 10 finanzierbaren Positionen nie greift. Der Lauf
bestätigt das erneut: 0 von 20 Permutationen erreichen das Limit, alle 3 049
abgelehnten Trades gehen auf fehlendes Kapital zurück. Eigener Punkt, hier nur
erwähnt.

### Warum die Kaskade nicht neunmal, sondern einmal steht

Die neun `simulate_portfolio()` waren bis auf Kommentare und Zeilenumbrüche
identisch; die einzige sachliche Abweichung ist, dass `elliott_wave` bewusst
kein Positionslimit-Argument kennt. Die Regel neunmal einzubauen hätte den
Befund von TB-23 neunmal reproduzierbar gemacht. Also steht sie einmal, in
`shared/zuteilung.py`, und die Bots behalten davon genau das, was bot-eigen
ist: den Primärschlüssel.

**Die ganzen `equity_simulation.py` zusammenzulegen wäre weiter gegangen, als
diese Aufgabe tragen kann** — und ist bewusst unterblieben. Ihre
`collect_all_trades()` haben verschiedene Signaturen (jede Strategie hat
andere Parameter), und ihre `__main__`-Blöcke unterscheiden sich sachlich
(`volatility_breakout_crypto` wendet seinen BTC-Regimefilter dort an, nicht in
`collect_all_trades()` — PR #57). Vor allem aber hängen
`shared/determinismus.py`, `shared/ergebniskurven.py`,
`shared/portfolio_overview.py` und mehrere `research/`-Programme an der
heutigen Form: ein `equity_simulation.py` je Bot, je Unterprozess importiert,
mit `inspect.signature`-Abfragen darauf. Eine Zusammenlegung hätte all das
mitgezogen und die eine Zusicherung, um die es geht, schwerer prüfbar
gemacht. `elliott_wave` behält aus demselben Grund seine Signatur **ohne**
`max_concurrent_positions`: `shared/portfolio_overview.py` und
`research/order_sensitivity/run_one_bot.py` erkennen genau daran, welcher Bot
kein Limit hat.

---

## 6. Was als Nächstes ansteht — und hier bewusst nicht getan wurde

**`shared/ergebniskurven.py` meldet jetzt 9 × ABWEICHEND. Das ist richtig.**
Die abgelegten `results/<bot>/equity_curve.csv` beschreiben die Zuteilung vor
TB-26.

| Bot | abgelegt | heute |
|---|---:|---:|
| `elliott_wave` | 67,77 % / −10,17 % | 67,77 % / −10,17 % — **gleiche Zahlen**, 21 von 130 Zeilen in anderer Reihenfolge |
| `elliott_wave_stocks` | 352,72 % / −22,44 % | 419,07 % / −22,97 % |
| `rsi2_crypto` | 28,37 % / −13,30 % | 27,19 % / −13,94 % |
| `rsi2_mean_reversion` | 36,75 % / −21,05 % | 36,28 % / −19,53 % |
| `t3_supertrend` | 129,64 % / −22,20 % | 121,70 % / −22,40 % |
| `turtle_soup_crypto` | 177,59 % / −32,40 % | 152,84 % / −34,85 % |
| `turtle_soup_stocks` | 145,59 % / −29,91 % | 138,15 % / −29,07 % |
| `volatility_breakout` | 224,41 % / −23,97 % | 209,59 % / −22,46 % |
| `volatility_breakout_crypto` | 49,03 % / −16,29 % | 68,13 % / −16,29 % |

**Empfehlung: die Kurven erst nach dem Merge neu erzeugen, und dann alles
gemeinsam, was an ihnen hängt.**

* *Nicht jetzt*, weil `results/*/equity_curve.csv` ausdrücklich nicht Teil
  dieser Änderung ist: die Kurven sind der Vergleichsmaßstab, an dem der Merge
  selbst geprüft wird. Wer sie mit-committet, nimmt dem Reviewer genau die
  Datei weg, an der er die Wirkung ablesen kann.
* *Bald*, weil `shared/ergebniskurven.py` bis dahin auf jedem Lauf rot ist —
  und eine Prüfung, die dauerhaft rot steht, liest bald niemand mehr.
* *Gemeinsam*, weil an den Kurven die Portfolio-Übersicht
  (`shared/portfolio_overview.py`), die Wochenmail und die Dashboard-Ansicht
  hängen. Zwei Nachzüge im Abstand von Tagen erzeugen eine Woche lang
  Zahlen, die zu nichts passen.

Der Befehl dafür ist `python3 shared/ergebniskurven.py --erzeugen`. Solange
das nicht geschehen ist, meldet auch `shared/test_stabile_sortierung.py`
(Abschnitt 6) einen Fehlschlag — dieselbe Ursache, dieselbe Behebung.

**Ebenfalls offen und hier nicht angefasst:**

* **TB-25** — ob unter dem `fib_score` stetige Abstände liegen. Erst danach
  wäre ein Primärschlüssel für die beiden Elliott-Bots zu erwägen.
* **`MAX_CONCURRENT_POSITIONS` bei `volatility_breakout`** — greift nie.
* **`multi_symbol_optimise.py`** — die Zielfunktion ist eine eigene Aufgabe.
  Diese hier behebt die Zuteilung. Beachtenswert: die Parametersuche läuft
  weiterhin über eine Zielfunktion, die auf derselben Kapitalsimulation
  aufsetzt — sie profitiert also von der Kaskade, ohne dass an ihr etwas
  geändert wurde.
* **Eine Neuselektion der Symbole** ist ab jetzt möglich, ohne das Artefakt
  einzubauen. Das war der Zweck dieser Aufgabe.
