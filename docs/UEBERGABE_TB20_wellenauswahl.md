# TB-20 — Wellenauswahl: Übergabe-Zusammenfassung

**Stand:** 2026-09-13 · **Zweig:** `claude/new-session-s0p861` · **Basis:** `main` (a476a98)

---

## 0. Die Antwort vorweg

**Gleichstände sind der Regelfall, nicht die Ausnahme — und sie ändern heute
trotzdem keine einzige Auswahl.**

| Frage aus dem Auftrag | Antwort |
|---|---|
| Wie häufig sind Gleichstände im `fib_score`? | **87 %** (Krypto) bzw. **99 %** (Aktien) aller erkannten Muster stehen in einer Gleichstandsgruppe |
| Ändert ein Gleichstand tatsächlich eine Auswahl? | **Nein.** Die *Menge* der Muster ist reihenfolgeunabhängig; die *Reihenfolge* ändert sich, aber kein Verbraucher wertet sie aus |
| Wie viele Live-Trades wären betroffen? | **Null.** In **0 von 20 114** nachgebildeten Läufen standen je zwei neue Muster desselben Symbols gleichzeitig zur Auswahl |

**Das Verhalten verschiebt sich nicht.** `shared/ergebniskurven.py` meldet
weiterhin **9x AKTUELL**, und `find_causal_waves` — die Funktion, die
Backtest, Optimierung und alle neun Kapitalkurven speist — liefert auf allen
**173** Symbolen beider Bots **Zeile für Zeile** dasselbe wie auf `main`
(2 611 Trades, byteweise verglichen).

Damit ist dies eine **Absicherung**, keine Korrektur. Der Auftrag hatte genau
diesen Ausgang vorgesehen: *„Falls sich zeigt, dass Gleichstände praktisch
folgenlos bleiben, ist das ein Ergebnis."*

Was sich sehr wohl ändert und deshalb hierher gehört: **bei 95 von 173
Symbolen steht nach der Umstellung ein anderes Muster auf Platz 1** als
vorher (7 von 23 Krypto-, 88 von 150 Aktiensymbolen). Vorher entschied das
Quicksort, jetzt eine benannte Regel. Folgenlos ist das nur, solange kein
Verbraucher Platz 1 gesondert behandelt — heute tut es keiner.

---

## 1. Die Messung

### 1a. Warum Gleichstände hier struktureller Natur sind

`fibonacci_score()` addiert drei feste Teilpunkte (0.34 / 0.33 / 0.33) und
rundet auf zwei Stellen. Der Wertebereich ist damit **abgeschlossen**:

    0.0, 0.33, 0.34, 0.66, 0.67, 1.0

Oberhalb von `min_fib_score = 0.3` bleiben **fünf** mögliche Werte. Ein Bot,
der auf einem Symbol 250 Muster findet, verteilt sie zwangsläufig auf fünf
Werte. Gleichstände sind hier kein Datenzufall, sondern eine Eigenschaft der
Bewertungsfunktion.

### 1b. Gemessen über beide Bots, alle Symbole

Datenstand 13.09.2026, Live-Parameter (`DEVIATION_PCT` 10,0 bzw. 5,0),
`min_fib_score = 0.3`.

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---:|---:|
| Symbole mit Kandidaten | 23 | 150 |
| Kandidaten (`find_impulse_waves`) | 315 | 7 206 |
| davon in einer Gleichstandsgruppe | **281 (89,2 %)** | **7 140 (99,1 %)** |
| Muster nach `remove_overlapping` | 283 | 6 439 |
| davon in einer Gleichstandsgruppe | **247 (87,3 %)** | **6 372 (99,0 %)** |
| Symbole mit mindestens einem Gleichstand | **23 von 23** | **150 von 150** |

Verteilung der Werte nach `remove_overlapping`:

| `fib_score` | Krypto | Aktien |
|---:|---:|---:|
| 0,33 | 158 | 3 545 |
| 0,34 | 41 | 979 |
| 0,66 | 29 | 715 |
| 0,67 | 44 | 999 |
| 1,00 | 11 | 201 |

Die grösste Gleichstandsgruppe eines einzelnen Aktiensymbols umfasst **69
Muster**. Die im Auftrag genannten „8 von 11" der abgelegten BTC-Datei sind
also eher die untere als die obere Kante.

### 1c. Führt der Gleichstand zu einer anderen Auswahl?

Drei getrennte Fragen, drei getrennte Messungen.

**(i) Die MENGE der Muster hängt nicht an der Sortierung.**
`remove_overlapping` durchläuft die Kandidaten nach `start_time` und behält
je Überlappungsgruppe den besten. `start_time` ist je Symbol **eindeutig**
(gemessen: 0 Dubletten in allen 173 Symbolen — Kandidat *i* beginnt am Pivot
*i*). Damit ist das Ergebnis der Überlappungsbereinigung von der Reihenfolge
unabhängig. Gegenprobe: fünf zufällige Permutationen der Eingabe je Symbol,
**0 Abweichungen in der Menge** — weder vorher noch nachher.

**(ii) Die REIHENFOLGE hing sehr wohl an der Sortierimplementierung.**
Derselbe Datensatz, einmal mit Quicksort (Stand `main`) und einmal stabil
sortiert:

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---:|---:|
| Symbole mit abweichender Ausgabereihenfolge | **19 von 23** | **147 von 150** |
| davon anderes Muster auf **Platz 1** | 0 | **35** |

Das ist der Befund aus TB-19, bestätigt und beziffert.

**(iii) Kein Verbraucher wertet die Reihenfolge aus.** Das ist der
entscheidende Punkt, und er ist der Grund, warum (ii) heute folgenlos bleibt.

`forward_test.py` beider Bots durchläuft die Liste aus
`remove_overlapping` → Richtungsfilter → Frische-Filter. Die Reihenfolge
*innerhalb eines Symbols* kann nur dann etwas entscheiden, wenn in **einem
Lauf** mehr als ein **noch nicht gehandeltes** Muster desselben Symbols zur
Auswahl steht. Nachgebildet mit `find_causal_waves` — der bot-eigenen,
kausalen Nachbildung von `find_new_signals`, Lauf für Lauf über die gesamte
gespeicherte Kurshistorie, und zwar über das **ganze Optimierungsgitter**,
nicht nur den Live-Wert:

| Bot | `deviation_pct` | Läufe | Läufe mit **>1 neuem** Muster im selben Symbol |
|---|---:|---:|---:|
| `elliott_wave` | 4,0 | 996 | **0** |
| `elliott_wave` | 6,0 | 462 | **0** |
| `elliott_wave` | 8,0 | 240 | **0** |
| `elliott_wave` | **10,0 (live)** | 163 | **0** |
| `elliott_wave_stocks` | 2,0 | 7 276 | **0** |
| `elliott_wave_stocks` | 3,0 | 5 050 | **0** |
| `elliott_wave_stocks` | 4,0 | 3 418 | **0** |
| `elliott_wave_stocks` | **5,0 (live)** | 2 509 | **0** |

**0 von 20 114 Läufen.** Der Grund ist strukturell und nicht Zufall: zwei
Muster, deren Welle 5 innerhalb desselben Frische-Fensters endet (5 Tage
bzw. 48 Stunden), überlappen sich zwangsläufig — ein Muster spannt fünf
Pivot-Abschnitte, und `remove_overlapping` streicht Überlappungen auf einen
Vertreter zusammen.

Bei `deviation_pct = 4,0` (Krypto) stehen in 35 Läufen zwei frische Muster
in der Liste — aber eines davon war bereits gehandelt und wird von der
`UNIQUE(symbol, signal_time)`-Bedingung abgefangen, ohne einen Platz zu
belegen. Auch dort entscheidet die Reihenfolge nichts.

**Momentaufnahme:** auf dem heutigen Datenstand hat **kein einziges** der 173
Symbole ein frisches bearishes Muster. Auch unmittelbar steht also keine
Auswahl an.

### 1d. Wie viele Live-Trades wären betroffen?

**Null.** Mit der Einschränkung, dass die Live-Datenbanken
(`paper_trading_*.db`) auf dem Rechner des Nutzers liegen und nicht im Repo
sind. Die Zahl stützt sich deshalb auf zwei unabhängige Wege:

1. die kausale Nachbildung oben (0 von 20 114 Läufen) — `find_causal_waves`
   bildet laut eigenem Modulkopf ausdrücklich nach, „was
   `forward_test.py::find_new_signals` tatsächlich tut";
2. den Zeile-für-Zeile-Vergleich von `find_causal_waves` vorher/nachher:
   **173 von 173 Symbolen identisch, 2 611 Trades**. Wäre je ein Trade
   verschoben worden, stünde er hier.

---

## 2. Die gewählte Regel — und warum

`kind="stable"` allein macht das Ergebnis reproduzierbar, aber nicht
begründet: es hält die zufällige Eingabereihenfolge fest. Deshalb eine
fachliche Rangfolge, in `elliott_wave_counter.py` an **einer** Stelle
(`RANGFOLGE`) und im Quelltext begründet:

```python
RANGFOLGE = ["fib_score", "end_time", "start_time"]
RANGFOLGE_AUFSTEIGEND = [False, False, False]
```

**Zweitkriterium `end_time` absteigend — das jüngere Muster zuerst.**

Das ist keine neu erfundene Regel, sondern die feinere Fassung einer im
Projekt bereits getroffenen. `forward_test.py` verwirft Muster, deren Welle 5
länger als `SIGNAL_FRESHNESS_HOURS` (48) bzw. `SIGNAL_FRESHNESS_DAYS` (5)
zurückliegt. Die Begründung steht dort im Kommentar: der Einstieg erfolgt zum
**aktuellen** Kurs, nicht zum Kurs am Wellenende. Je weiter das Wellenende
zurückliegt, desto weiter ist der Einstiegskurs vom erkannten Aufbau
weggelaufen. Das Projekt bevorzugt Frische also schon — bisher nur grob
(drin / draussen). Bei gleichem Fibonacci-Urteil dieselbe Präferenz fein
anzulegen, revidiert keine Entscheidung, sondern setzt eine fort.

**Die beiden anderen Kandidaten aus dem Auftrag, und warum nicht:**

* **Grössere Amplitude.** `target_price = entry + total_move * TAKE_PROFIT_FIB`
  — die Amplitude bestimmt das Kursziel. Sie zum Rangkriterium zu machen
  hiesse, systematisch die Muster mit den weitesten Zielen zu bevorzugen.
  Das ist eine Verschiebung des Risikoprofils, also eine Strategieänderung,
  und die steht dem Nutzer zu, nicht einer Sortierkorrektur.
* **Kürzere Dauer.** Hat in diesem Projekt keine dokumentierte Begründung.
  Sie wäre eine erfundene Rangregel — und der Auftrag nennt die zu Recht
  schlechter als eine ehrlich gekennzeichnete Willkür.

**Drittkriterium `start_time` absteigend** — bei gleichem Ende das kürzere
Muster, aus demselben Grund. Innerhalb eines Symbols ist `end_time` bereits
eindeutig (gemessen: 0 Dubletten in 173 Symbolen), dieses Kriterium greift
dort also nie. Es steht da, damit die Rangfolge auch dann benannt bleibt,
wenn Muster mehrerer Symbole gemeinsam sortiert werden — `research/`-Code tut
das.

**Was NICHT geändert wurde: die Überlappungsregel.** Bei einer Überlappung
gewinnt weiterhin das **früher** erkannte Muster (der Vergleich ist `>`,
nicht `>=`). Das sieht wie ein Widerspruch zur Rangfolge aus, ist aber die
andere Frage: bei einer Überlappung geht es darum, welches Muster **ein**
Marktereignis vertritt, und dort darf ein späteres kein früheres
nachträglich verdrängen — genau das begründet der Modulkopf von
`find_causal_waves` als Look-Ahead. Die Rangfolge entscheidet dagegen
zwischen **verschiedenen** Ereignissen, die gleichzeitig zur Auswahl stehen.
Diese Regel anzufassen hätte die Menge der Muster verändert — eine
Verhaltensänderung, und damit eine Entscheidung des Nutzers.

---

## 3. Ein Nebenbefund, der einen Kommentar korrigiert

Beim Bau der Mutationsproben zeigte sich: **`kind="stable"` trägt in
`nach_rangfolge` nichts.** pandas wertet `kind` bei einer **mehrspaltigen**
`sort_values` nicht aus — dieser Pfad läuft über `lexsort` und ist ohnehin
stabil. Nachgemessen mit pandas 3.0.5: `kind="quicksort"` liefert bei
vollständigem Gleichstand dieselbe Reihenfolge wie `kind="stable"`.

Der Parameter bleibt trotzdem stehen, aber **als Absichtserklärung, nicht als
Wache** — und genau so steht es jetzt im Quelltext. Wirksam wird er erst,
wenn `RANGFOLGE` je wieder auf eine Spalte zusammenschrumpft; das ist der
Rückschritt, den der Selbsttest als Mutante „wie main" abfängt.

Das gehört hierher, weil die naheliegende Annahme („da steht `stable`, also
ist es stabil") hier falsch wäre. Die Stabilität kommt vom mehrspaltigen
Pfad, nicht vom Parameter.

---

## 4. Punkt 3 des Auftrags: `elliott_wave_stocks/forward_test.py:168`

**Nur beurteilt, nichts geändert** — die Datei steht auf der Sperrliste.

Zeile 168 ist die Positionslimit-Prüfung innerhalb der Wellenschleife:

```python
if open_count >= MAX_CONCURRENT_POSITIONS:
    print(f"  [UEBERSPRUNGEN] {symbol}: Signal vorhanden, aber "
          f"Positionslimit ({MAX_CONCURRENT_POSITIONS}) erreicht")
    continue
```

**Steckt dort dieselbe Frage? Ja — aber eine Ebene höher, und es ist keine
Sortierinstabilität.**

* **Innerhalb eines Symbols** ist die Frage mit dieser Aufgabe erledigt: bei
  `elliott_wave_stocks` — dem Bot, der das Limit überhaupt durchsetzt — hat
  die Auswahlliste in **allen 18 253** nachgebildeten Läufen die Länge 1
  (Abschnitt 1c). Das Limit kann dort gar nicht zwischen zwei Mustern
  desselben Symbols entscheiden.
* **Zwischen Symbolen** entscheidet die Reihenfolge sehr wohl, wer einen der
  acht Plätze bekommt — sie kommt aus `for symbol, df in price_data.items()`,
  also aus `config/sp500_top150.txt`. Diese Liste ist **absteigend nach
  Marktkapitalisierung** sortiert. Das ist keine Willkür einer
  Sortierimplementierung, sondern eine feste, systematische Ordnung: bei
  vollem Limit bekommen strukturell immer die grössten Werte den Platz.
  `research/order_sensitivity/BERICHT.md` (Abschnitt 7) hat das bereits
  beschrieben und ausdrücklich nicht bewertet. **Hier ebenso** — es wäre eine
  Strategieentscheidung, keine Sortierkorrektur.
* Die Grössenordnung steht ebenfalls dort: bei `elliott_wave_stocks` sind
  **21,8 %** der Trades „umstritten" (Ausführungsstatus über 500 Permutationen
  nicht konstant), die Calmar-Spanne beträgt 476 bis 920.

**Zwei kleinere Beobachtungen an derselben Stelle**, beide kein Fehler:

1. Es ist `continue`, nicht `break`. Wirkung ist dieselbe (`open_count` sinkt
   innerhalb eines Laufs nie), aber ab dem Erreichen des Limits schreibt der
   Lauf **je verbleibendem frischen Signal über alle 150 Aktien** eine
   `[UEBERSPRUNGEN]`-Zeile ins Protokoll. Reine Protokollmenge.
2. `open_count` wird vor der Symbolschleife einmal gelesen und bei jedem
   erfolgreichen `INSERT` hochgezählt — das Limit greift also auch innerhalb
   eines Laufs korrekt. Bereits gehandelte Muster laufen in den
   `IntegrityError` und belegen **keinen** Platz; das ist der Grund, warum
   die 35 Doppel-Läufe aus Abschnitt 1c folgenlos bleiben.

---

## 5. Was geändert wurde

| Datei | Änderung |
|---|---|
| `strategies/elliott_wave/elliott_wave_counter.py` | `RANGFOLGE` + `nach_rangfolge()` neu; die beiden Rangsortierungen und der Überlappungs-Durchlauf rufen sie bzw. sortieren stabil |
| `strategies/elliott_wave_stocks/elliott_wave_counter.py` | identisch (beide Dateien unterscheiden sich weiterhin nur in den zwei Symbolliteralen im `__main__`-Block) |
| `shared/test_wellenauswahl.py` | **neu** — Selbsttest, 323 Prüfungen |

**Nicht geändert:** `forward_test.py`, `live_params.py`, `equity_simulation.py`,
`results/*/equity_curve.csv`, die abgelegten Optimierungsergebnisse,
`broker/`, Crontab, launchd-Vorlagen, `research/`-Berichte.

**Eine Datei, die sich beim nächsten manuellen Lauf ändern wird:**
`results/BTCUSDT_impulse_waves.csv` (und ihr Aktien-Gegenstück) entsteht im
`__main__`-Block von `elliott_wave_counter.py`. Ihre **Zeilen** bleiben
dieselben, ihre **Reihenfolge** folgt künftig der Rangfolge. Sie wurde hier
**nicht** neu geschrieben. Kein Skript liest sie — `backtest_elliott.py`
bestimmt die Wellen ausdrücklich neu, statt sie zu lesen (Look-Ahead).

---

## 6. Prüfungen

| Prüfung | Ergebnis |
|---|---|
| `shared/test_wellenauswahl.py` (neu) | **323 von 323** (`--schnell`: 322 von 322) |
| `shared/ergebniskurven.py` | **9x AKTUELL**, Rückgabewert 0 |
| `shared/test_stabile_sortierung.py` (TB-19) | **46 von 46** |
| `shared/test_drawdown_beide_masse.py` (TB-18) | **253 von 253** |
| `find_causal_waves` vorher/nachher, 173 Symbole | **Zeile für Zeile identisch**, 2 611 Trades |
| Menge nach `remove_overlapping` vorher/nachher | **173 von 173 identisch** |
| Alle 32 Selbsttest-Dateien | siehe unten |

Der neue Test prüft **Verhalten, nicht Quelltext**: er ruft die echten
Funktionen auf und weist an **mutierten Kopien** nach, dass jeder Abschnitt
rot werden kann — und zwar **genau** die vorgesehenen Abschnitte, nicht mehr
und nicht weniger. Neun Mutanten, je mit exakter Erwartung. Einzelheiten im
Testauftrag.

*Messumgebung:* Python 3.11.15, pandas 3.0.5, numpy 2.4.6 — dieselbe wie
TB-19.

### Ein Fehler, den diese Aufgabe selbst gebaut und wieder eingefangen hat

Die erste Fassung des Selbsttests legte ihre Mutantenkopien **im
Strategie-Ordner** ab. Beim Import ruft jede dieser Kopien
`get_strategy_paths(__file__)` auf — und diese Funktion **legt Ordner an**.
So entstanden unbemerkt `strategies/results/` und `strategies/logs/` im Repo.

`git status` meldete nichts: git kennt keine leeren Ordner. Aufgefallen ist
es `research/trend_overlay/test_corrected_curves.py`, das die Bot-Ordner
auszählt und deshalb im Zweiglauf fehlschlug, obwohl es auf `main` bestand.

Behoben: die Kopien liegen jetzt ausserhalb des Repos, in einem nachgebauten
`<temp>/strategies/<name>/`. Und der Test prüft seitdem **zusätzlich zur
`git status`-Probe die Ordnerliste selbst**. Dass diese neue Wache trägt, ist
nachgewiesen, nicht behauptet: gegen eine Fassung mit dem alten Verhalten
bleibt `git status` grün und die Ordnerprobe wird rot
(`neu: ['strategies/logs', 'strategies/results']`).

### Basislauf: was in dieser Umgebung schon auf `main` fehlschlägt

Alle 32 Testdateien liefen zweimal — einmal auf unverändertem `main` in einem
eigenen Arbeitsbaum, einmal auf diesem Zweig. **Acht Dateien schlagen in
beiden Läufen gleichermassen fehl**, keine davon wegen dieser Änderung:

| Datei | Grund |
|---|---|
| `broker/test_ibkr.py` | keine `tzdata` im Container |
| `dashboard/test_dashboard.py` | kein `fastapi` |
| `dashboard/test_portfolio_sicht.py` | kein `fastapi` |
| `research/hrp_portfolio/test_hrp_core.py` | kein `scipy` |
| `shared/test_kursdaten.py` | kein `binance` |
| `research/drawdown_reihenfolge/test_drawdown.py` | braucht einen Bot als Argument (Aufrufhinweis, kein Fehlschlag) |
| `research/elliott_wave_params/test_params.py` | dasselbe |
| `system/test_dienst_plists.py` | Rückgabewert 2 by design — prüft macOS-Dienste |

Die restlichen 24 bestehen auf `main` wie auf dem Zweig.

**Eine scheinbare Abweichung ist keine.** Im ersten Zweiglauf fiel
`research/pnl_2025_fixed_size/test_pnl.py` durch. Der Test prüft, dass
`git diff HEAD -- strategies/` leer ist — und sah genau das: die Änderung war
zu diesem Zeitpunkt noch nicht eingecheckt. Auf dem eingecheckten Stand
wiederholt: **93 von 93**, „kein Bot-Code veraendert — leerer Diff". Das ist
gleichzeitig ein Beleg dafür, dass diese Wache funktioniert.

Dasselbe gilt für `shared/test_drawdown_beide_masse.py`: parallel zu einem
`git commit` gelaufen meldet es 252 von 253 („der Testlauf hat Dateien im
Repo veraendert"), allein gelaufen **253 von 253**. Beide Tests prüfen den
Repo-Zustand und brauchen deshalb einen Lauf ohne Nebenläufer.

---

## 7. Offene Punkte (nicht Teil dieser Aufgabe)

1. **Die Symbolreihenfolge beim Positionslimit** (Abschnitt 4). Bei vollem
   Limit bekommen strukturell die grössten Werte den Platz. Beschrieben in
   `research/order_sensitivity`, hier bestätigt, nirgends entschieden.
2. **`equity_simulation.py::collect_all_trades` sortiert `entry_time`
   instabil** (Zeile 101, Sperrliste). Heute folgenlos — TB-19 hat das für
   zwei Bots nachgemessen — aber nicht zugesichert. Derselbe Befund gilt für
   `research/trailing_stops/run_one_bot.py:306`.
3. **Die 19 weiteren `build_daily_capital_curve`-Stellen** aus TB-19,
   Abschnitt 3a. Unverändert offen.
4. **`research/trailing_stops` und `research/elliott_wave_lookahead`** rufen
   `find_impulse_waves`/`remove_overlapping` direkt auf. Die *Menge* ihrer
   Muster ist unverändert (Abschnitt 1c(i)); ihre *Zeilenreihenfolge* ist es
   nicht. Beide Berichte sind hier weder neu gerechnet noch angefasst —
   `research/`-Zahlen zu verschieben ist nach Projektregel ein eigener,
   ausdrücklich freigegebener Schritt. Ihre Selbsttests
   (`test_atr_core.py`, `test_lookahead.py`) bestehen unverändert.
