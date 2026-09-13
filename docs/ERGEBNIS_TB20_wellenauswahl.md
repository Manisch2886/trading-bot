# TB-20 — Wellenauswahl: Ergebnis

**Kurzfassung zum Kopieren.** Ausführlich: `docs/UEBERGABE_TB20_wellenauswahl.md`.
Prüfanleitung: `docs/TESTAUFTRAG_TB20_wellenauswahl.md`.

---

## Das Ergebnis in drei Sätzen

Gleichstände im `fib_score` sind bei den Elliott-Wave-Bots kein Randfall,
sondern der Normalfall: **87 %** der Krypto- und **99 %** der Aktien-Muster
teilen ihren Wert mit mindestens einem anderen. Sie haben trotzdem **keine
einzige Auswahl** verschoben — weder live noch im Backtest, weil in **0 von
20 114** nachgebildeten Läufen je zwei neue Muster desselben Symbols
gleichzeitig zur Auswahl standen. Die Umstellung ist deshalb eine
**Absicherung, keine Korrektur**: das Verhalten bleibt, die Abhängigkeit von
der Sortierimplementierung verschwindet.

---

## Die Zahlen

### Wie häufig sind Gleichstände?

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---:|---:|
| Symbole | 23 | 150 |
| Muster nach `remove_overlapping` | 283 | 6 439 |
| **davon in einer Gleichstandsgruppe** | **247 (87,3 %)** | **6 372 (99,0 %)** |
| Symbole mit mindestens einem Gleichstand | 23 von 23 | 150 von 150 |
| grösste Gruppe eines Symbols | 17 | 69 |

Der Grund ist strukturell: `fibonacci_score()` addiert drei feste
Teilpunkte (0.34/0.33/0.33) und rundet auf zwei Stellen. Oberhalb von
`min_fib_score = 0.3` gibt es genau **fünf** mögliche Werte — 0,33, 0,34,
0,66, 0,67 und 1,0. Tausende Muster auf fünf Werte: Gleichstände sind hier
kein Datenzufall.

### Ändert ein Gleichstand die Auswahl?

| Frage | Antwort |
|---|---|
| Hängt die **Menge** der Muster an der Sortierung? | **Nein.** `start_time` ist je Symbol eindeutig (0 Dubletten in 173 Symbolen); fünf Permutationen je Symbol → 0 Abweichungen |
| Hing die **Reihenfolge** an der Sortierimplementierung? | **Ja.** Quicksort gegen stabil: 19 von 23 Krypto- und 147 von 150 Aktiensymbolen weichen ab; bei **35** der 150 Aktiensymbole stand ein anderes Muster auf Platz 1 |
| Wertet ein Verbraucher die Reihenfolge aus? | **Nein** — s. u. |

### Wie viele Live-Trades wären betroffen?

**Null.** Die Reihenfolge innerhalb eines Symbols kann nur wirken, wenn in
einem Lauf mehr als ein **noch nicht gehandeltes** Muster desselben Symbols
zur Auswahl steht. Nachgebildet über die gesamte Kurshistorie und das ganze
Optimierungsgitter:

| Bot | Läufe gesamt | Läufe mit >1 neuem Muster |
|---|---:|---:|
| `elliott_wave` (4 Parameterwerte) | 1 861 | **0** |
| `elliott_wave_stocks` (4 Parameterwerte) | 18 253 | **0** |

Strukturell und nicht zufällig: zwei Muster, deren Welle 5 innerhalb
desselben Frische-Fensters endet (48 Stunden bzw. 5 Tage), überlappen sich
zwangsläufig — und `remove_overlapping` streicht Überlappungen auf einen
Vertreter zusammen.

### Bleibt das Verhalten?

| Prüfung | Ergebnis |
|---|---|
| `find_causal_waves` vorher/nachher, 173 Symbole, 2 611 Trades | **Zeile für Zeile identisch** |
| Menge nach `remove_overlapping` vorher/nachher | **173 von 173 identisch** |
| `shared/ergebniskurven.py` | **9x AKTUELL** |

---

## Die eingeführte Regel

```python
RANGFOLGE = ["fib_score", "end_time", "start_time"]   # alle absteigend
```

| Rang | Kriterium | Bedeutung |
|---:|---|---|
| 1 | `fib_score` | bestes Fibonacci-Urteil zuerst (unverändert) |
| 2 | `end_time` | bei Gleichstand das **jüngere** Muster |
| 3 | `start_time` | bei gleichem Ende das **kürzere** |

**Warum das jüngere Muster.** Keine neue Regel, sondern die feinere Fassung
einer vorhandenen: `forward_test.py` verwirft Muster, deren Welle 5 länger
als 48 Stunden bzw. 5 Tage zurückliegt — weil der Einstieg zum **aktuellen**
Kurs erfolgt, nicht zum Kurs am Wellenende. Je älter das Wellenende, desto
weiter ist der Einstiegskurs vom erkannten Aufbau weggelaufen. Das Projekt
bevorzugt Frische bereits, bisher nur grob. Bei gleichem Fibonacci-Urteil
dieselbe Präferenz fein anzulegen, revidiert keine Entscheidung.

**Warum nicht Amplitude.** Die Amplitude bestimmt über
`target_price = entry + total_move * TAKE_PROFIT_FIB` das Kursziel. Sie zum
Rangkriterium zu machen hiesse, systematisch die weitesten Ziele zu
bevorzugen — eine Verschiebung des Risikoprofils, also eine
Strategieentscheidung des Nutzers, keine Sortierkorrektur.

**Warum nicht Dauer.** Hat im Projekt keine dokumentierte Begründung; wäre
eine erfundene Rangregel.

**Nicht geändert: die Überlappungsregel.** Bei einer Überlappung gewinnt
weiterhin das **früher** erkannte Muster. Das ist die andere Frage — dort
geht es darum, welches Muster **ein** Ereignis vertritt, und ein späteres
darf ein früheres nicht nachträglich verdrängen (Look-Ahead, siehe Modulkopf
von `find_causal_waves`). Diese Regel anzufassen hätte die Menge der Muster
verändert.

---

## Nebenbefund: `kind="stable"` trägt hier nichts

pandas wertet `kind` bei einer **mehrspaltigen** `sort_values` nicht aus —
der Pfad läuft über `lexsort` und ist ohnehin stabil (nachgemessen mit pandas
3.0.5). Der Parameter bleibt stehen, aber **als Absichtserklärung, nicht als
Wache**, und genau so steht es jetzt im Quelltext. Wirksam würde er erst,
wenn `RANGFOLGE` je wieder auf eine Spalte zusammenschrumpft — der Selbsttest
fängt genau diesen Rückschritt als Mutante ab.

---

## `forward_test.py:168` (nur beurteilt, nicht angefasst)

Dieselbe Frage steckt dort — aber **eine Ebene höher und ohne
Sortierinstabilität**:

* **Innerhalb eines Symbols** erledigt: die Auswahlliste hat bei
  `elliott_wave_stocks` in allen 18 253 nachgebildeten Läufen die Länge 1.
* **Zwischen Symbolen** entscheidet die Reihenfolge von
  `config/sp500_top150.txt`, wer einen der acht Plätze bekommt. Diese Liste
  ist **absteigend nach Marktkapitalisierung** sortiert — eine feste,
  systematische Ordnung, keine Willkür einer Sortierimplementierung. Bei
  vollem Limit bekommen strukturell immer die grössten Werte den Platz.
  `research/order_sensitivity/BERICHT.md` (Abschnitt 7) beschreibt das
  bereits und bewertet es ausdrücklich nicht; das gilt hier ebenso. Die
  Grössenordnung steht dort: **21,8 %** der Trades dieses Bots sind
  „umstritten", die Calmar-Spanne reicht von 476 bis 920.

---

## Geänderte Dateien

| Datei | Änderung |
|---|---|
| `strategies/elliott_wave/elliott_wave_counter.py` | `RANGFOLGE` + `nach_rangfolge()`; beide Rangsortierungen und der Überlappungs-Durchlauf |
| `strategies/elliott_wave_stocks/elliott_wave_counter.py` | identisch |
| `shared/test_wellenauswahl.py` | **neu**, 323 Prüfungen |

**Unverändert:** `forward_test.py`, `live_params.py`, `equity_simulation.py`,
`results/*/equity_curve.csv`, abgelegte Optimierungsergebnisse, `broker/`,
Crontab, launchd-Vorlagen, `research/`-Berichte.

---

## Prüfungen

| Prüfung | Ergebnis |
|---|---|
| `shared/test_wellenauswahl.py` | **323 von 323** |
| `shared/ergebniskurven.py` | **9x AKTUELL** |
| `shared/test_stabile_sortierung.py` (TB-19) | 46 von 46 |
| `shared/test_drawdown_beide_masse.py` (TB-18) | 253 von 253 |
| Alle 32 Selbsttest-Dateien | 24 bestanden, 8 vorbestehende Fehlschläge (fehlende Abhängigkeiten; mit Basislauf auf `main` belegt) |

Der neue Test prüft **Verhalten, nicht Quelltext**, und weist an neun
mutierten Kopien nach, dass **genau** die vorgesehenen Abschnitte anschlagen
— nicht mehr und nicht weniger.
