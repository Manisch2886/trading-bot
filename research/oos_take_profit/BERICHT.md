# `elliott_wave_stocks`: Out-of-Sample-Validierung reichte `use_take_profit` nicht durch

**Stand:** 2026-09-08 · **Branch:** `claude/oos-take-profit-fix`
**Ausgangspunkt:** PR #45, Befund 7.1

---

## Kurzfassung

| | |
|---|---|
| Betroffen | `strategies/elliott_wave_stocks/oos_equity_simulation.py`, eine Aufrufstelle |
| Vorher | **Abbruch mit `TypeError`** — kein Ergebnis, keine Zahlen |
| Nachher | läuft durch: **+70,37 %** OOS-Rendite, **−10,11 %** Max Drawdown, Calmar **6,96**, 128 Trades |
| `elliott_wave` (Krypto) | **nicht betroffen** — belegt, nicht behauptet |
| Rückwirkung auf getroffene Entscheidungen | **keine** — belegt, nicht behauptet |
| `forward_test.py` / `live_params.py` | unverändert |
| Tests | 22/22 |

---

## 1. Root Cause — und eine Korrektur an der eigenen Meldung aus PR #45

### Die fehlende Übergabe

`oos_equity_simulation.py` übernahm vom In-Sample-Gewinner drei der vier gesuchten
Dimensionen:

```python
best = train_results.iloc[0]
trades = collect_all_trades(
    test_data,
    deviation_pct=best["deviation_pct"],
    stop_loss_pct=best["stop_loss_pct"],
    take_profit_fib=best["take_profit_fib"],
)                                     # use_take_profit fehlt
```

`collect_all_trades()` hat den Default `use_take_profit: bool = True`
(`equity_simulation.py:66`). Das Suchraster optimiert aber ausdrücklich über diese
Dimension (`multi_symbol_optimise.py:181`), und der Wert steht im Ergebnis (`:154`).

### Das Gegenbeispiel: so sieht es richtig aus

`multi_symbol_walk_forward.py:73-79` macht es seit jeher korrekt — und zwar mit
**beiden** nötigen Teilen:

```python
test_result = evaluate_combination_multi(
    test_data,
    deviation_pct=best["deviation_pct"],
    stop_loss_pct=best["stop_loss_pct"],
    take_profit_fib=best["take_profit_fib"] if best["use_take_profit"] else 0.236,
    use_take_profit=best["use_take_profit"],
)
```

### Korrektur: es waren nicht „falsche Zahlen", es war ein Absturz

PR #45 meldete, die OOS-Prüfung laufe „immer mit Take-Profit". Das war eine
Schlussfolgerung aus dem Code. Der tatsächliche Lauf zeigt etwas anderes — das
Skript **stirbt**:

```
backtest_elliott.py:134
  target_price = entry_price + total_move * TAKE_PROFIT_FIB if use_take_profit else float("inf")
TypeError: unsupported operand type(s) for *: 'float' and 'NoneType'
```

Beide Fehler greifen ineinander. Weil `use_take_profit` nicht durchgereicht wurde,
nahm `collect_all_trades()` seinen Default `True` und ging in den Take-Profit-Zweig —
und der braucht ein Fibonacci-Ziel, das der Optimierer für Kombinationen ohne festes
Ziel bewusst auf `None` setzt (`multi_symbol_optimise.py:153`).

Dazu passt ein Artefakt-Befund: **`results/elliott_wave_stocks/oos_equity_curve.csv`
existiert gar nicht.** Genau diese Datei schreibt das Skript am Ende. Es ist für
diesen Bot also nie durchgelaufen. Die Nachbardateien (`equity_curve.csv`, die
`experiment_*`-CSVs) sind vorhanden.

### Warum `None` und nicht `NaN` — und warum das den Fix bestimmt

Ob aus dem `None` in der Ergebnistabelle ein `NaN` oder ein echtes `None` wird, hängt
davon ab, ob **überhaupt** eine Kombination mit festem Ziel die Mindestfilter besteht:

| Fall | dtype der Spalte | Wert | Folge |
|---|---|---|---|
| mindestens eine Kombination mit Ziel besteht | `float64` | `NaN` | `NaN * float` → still `NaN`, Fehler bliebe **unsichtbar** |
| keine besteht | `object` | `None` | `None * float` → **`TypeError`** |

Beim Aktien-Bot trat der zweite Fall ein. Eine Lösung, die nur an `NaN` denkt, griffe
also zu kurz — deshalb sind es zwei Ergänzungen statt einer.

---

## 2. Der Fix

```python
take_profit_fib=(best["take_profit_fib"] if best["use_take_profit"] else 0.236),
use_take_profit=best["use_take_profit"],
```

Aufgebaut wie `multi_symbol_walk_forward.py:77`. Der Ersatzwert 0.236 ist wirkungslos,
weil `run_backtest()` das Ziel bei `use_take_profit=False` ohnehin auf `float("inf")`
setzt — er verhindert nur, dass ein `None` überhaupt in die Multiplikation gerät.

Zusätzlich zeigt die Parameterausgabe jetzt „**KEIN festes Ziel**" statt einer
Fib-Zahl, die es in diesem Fall gar nicht gibt. Das war das zweite Symptom derselben
Ursache: der Bericht nannte nicht einmal, welche Variante er validiert.

Sonst wurde an der OOS-Logik nichts geändert — `git diff` umfasst genau diese eine
Aufrufstelle plus Kommentare.

---

## 3. Vorher/Nachher

| Kennzahl | Vorher (fehlerhaft) | Nachher (korrigiert) |
|---|---|---|
| Lauf | **`TypeError`, kein Ergebnis** | läuft durch |
| Validierte Variante | — | Zigzag 5,0 % / Stop 2,0 % / **kein festes Ziel** |
| OOS-Zeitraum | — | 2023-08-30 bis 2026-09-01 |
| Startkapital | — | 10.000,00 |
| Endkapital | — | 17.036,74 |
| **Gesamtrendite** | — | **+70,37 %** |
| **Max Drawdown** | — | **−10,11 %** |
| **Calmar** (Rendite / \|MaxDD\|) | — | **6,96** |
| Trades gefunden | — | 128 |
| davon ausgeführt | — | 120 |
| übersprungen (Kapital) | — | 8 |

Calmar hier bewusst über den **gesamten** OOS-Zeitraum, nicht annualisiert — es geht
um die Vergleichbarkeit zwischen den Läufen, nicht um eine absolute Kennzahl.

Beide Läufe erzeugt von `oos_lauf.py`, das das **echte** Skript in einem eigenen
Prozess ausführt (gleichnamige Module der 9 Bots würden sich sonst über `sys.modules`
überschreiben) und `RESULTS_DIR`/`LOGS_DIR`/`DB_FILE` in ein temporäres Verzeichnis
umleitet — die echten `results/`-Dateien bleiben unberührt.

---

## 4. Einordnung und Plausibilitätscheck (Frage 3)

**Ein „bisher berichteter OOS-Wert" existiert nicht.** Das Skript ist nie
durchgelaufen; es gibt also nichts, wovon der korrigierte Wert abweichen könnte. Die
Frage „wie stark weicht er ab" hat für diesen Bot keine Antwort in Zahlen — und das
ist selbst der Befund.

Eine Gegenprobe hätte die fehlende Vergleichszahl liefern können — derselbe Lauf mit
erzwungenem `use_take_profit=True` und Fib 0,236 als Ersatz für das `None`, also das,
was die fehlerhafte Fassung *gemeldet hätte*, wäre sie nicht abgestürzt. Der Modus
steckt als `oos_lauf.py gegenprobe` im Werkzeug. Der Lauf wurde **bewusst abgebrochen**:
er beantwortet eine hypothetische Frage, die die Aufgabe so nicht stellt, und rechtfertigt
keinen weiteren unbeaufsichtigten Hintergrundlauf. Wer die Zahl braucht, startet ihn
mit einem Befehl nach.

**Der Plausibilitätscheck fällt dagegen sehr deutlich aus.** Von 64 geprüften
Kombinationen besteht auf dem In-Sample-Fenster **keine einzige mit festem Kursziel**
die Mindestfilter (`MIN_TRADES=150`, `MIN_SYMBOLS_CONTRIBUTING=22`,
`MIN_AVG_RETURN_PCT`). Die fünf besten:

| Rang | Zigzag | Stop | Ziel | Trades | Score |
|---|---|---|---|---|---|
| 1 | 5,0 % | 2,0 % | **kein** | 372 | 1,018 |
| 2 | 4,0 % | 8,0 % | **kein** | 496 | 0,985 |
| 3 | 5,0 % | 3,0 % | **kein** | 372 | 0,915 |
| 4 | 2,0 % | 8,0 % | **kein** | 1228 | 0,909 |
| 5 | 3,0 % | 8,0 % | **kein** | 767 | 0,905 |

Die Live-Entscheidung `USE_TAKE_PROFIT = False` vom 2026-09-03 deckt sich also exakt
damit, was die Optimierung von sich aus wählt. Das ist kein Beweis — die
Mindestfilter könnten die With-TP-Varianten auch aus anderen Gründen aussieben —,
aber es ist die Gegenkontrolle, die die Aufgabe verlangt, und sie stützt die
getroffene Entscheidung.

---

## 5. Rückwirkung auf bereits getroffene Entscheidungen (Frage 4)

**Keine.** Belegt in drei Schritten:

**a) Niemand ruft das Skript auf oder zitiert es.** Eine Suche über das ganze Repo
nach `oos_equity_simulation` findet drei Treffer: zwei Kommentar-Erwähnungen zu
`ALLOCATION_PCT` (in beiden `live_params.py`) und eine Zeile im Übergabeprotokoll.
Keine davon nennt eine Zahl.

**b) Die Aussage in `live_params.py` stammt aus einer anderen Quelle.** Der Eintrag
vom 2026-09-03 nennt „+204 % statt +108 % OOS" und „+3084 % statt +1500 %
Gesamtzeitraum". Diese Zahlen stehen exakt so in den Artefakten von
`experiment_no_take_profit.py`:

| Variante | Rendite (OOS) | Max DD | Rendite (gesamt) | Max DD |
|---|---|---|---|---|
| MIT Take-Profit | +107,87 % | −1,65 % | +1500,53 % | −1,90 % |
| OHNE Take-Profit | +203,66 % | −5,04 % | +3084,09 % | −9,79 % |

Dieses Skript übergibt `use_take_profit` für **beide** Varianten explizit
(`experiment_no_take_profit.py:54`) und nutzt zusätzlich `MAX_CONCURRENT_POSITIONS`
aus `live_params.py`. Es ist von dem Fehler nicht berührt, und es bildet seine
eigene 70/30-Aufteilung — es hängt nicht an `oos_equity_simulation.py`.

**c) PR #28 hat eine eigene Engine.** `research/elliott_wave_params/` liest
`USE_TAKE_PROFIT` direkt aus `live_params.py` (`engine.py:94`) und reicht es
durchgängig durch (`search.py`, `walkforward.py`, `stability.py`, `summary.py`).
Auch dort keine Abhängigkeit.

**Nebenbefund, mitkorrigiert:** `docs/UEBERGABEPROTOKOLL.md:210` behauptete,
`oos_equity_simulation.py` gebe es „(nur Krypto-Varianten)". Das Skript existiert
auch beim Aktien-Bot. Diese falsche Angabe hat mit dazu beigetragen, dass der Fehler
dort lange unbemerkt blieb — wer nach betroffenen Stellen sucht, hätte den Aktien-Bot
nach dieser Tabelle ausgeschlossen. Die Zeile ist korrigiert; das ist eine reine
Dokumentationsänderung.

---

## 6. `elliott_wave` (Krypto) ist nicht betroffen

Belegt statt behauptet, automatisiert geprüft in `test_oos_take_profit.py`, Gruppe D:

- `run_backtest()` dort hat die Signatur `(price_df, impulses)` — es gibt gar keinen
  `use_take_profit`-Parameter.
- Die Zeichenketten `use_take_profit` / `USE_TAKE_PROFIT` kommen in **keiner einzigen**
  Datei des Bots vor.
- Sein Suchraster ist ein schlichtes `itertools.product` über drei Bereiche
  (`multi_symbol_optimise.py:150`), ohne die zusätzliche „kein Ziel"-Zeile, die der
  Aktien-Bot hat.
- Gegenkontrolle im selben Test: beim Aktien-Bot kommt die Dimension in neun Dateien
  vor — die Prüfung ist also nicht nur trivial grün.

---

## 7. Tests

`python3 research/oos_take_profit/test_oos_take_profit.py` → **22/22**

| Gruppe | Was sie absichert |
|---|---|
| A | Die Übergabe an `collect_all_trades`, **per AST statt Textsuche** — eine Suche nach `use_take_profit` fände auch Docstring und Kommentar |
| B | Die `None`/`NaN`-Falle in beiden Ausprägungen, inklusive des Nachweises, dass `None * float` wirft und `NaN * float` still durchgeht |
| C | Dass der Schalter überhaupt wirkt: `simulate_trade()` steigt mit Ziel bei 110 aus, ohne Ziel erst bei 148 — und der Stop-Loss behält in beiden Fällen Vorrang |
| D | Die Abgrenzung zum Krypto-Bot, mit Gegenkontrolle |
| E | **Der eigentliche Schutz gegen eine Wiederholung** |

Gruppe E ist mir wichtiger als der Einzeilen-Fix. Sie vergleicht für beide
Elliott-Bots, welche Dimensionen das Suchraster **liefern** kann, mit denen, die die
OOS-Simulation **abholt**:

| Bot | Raster liefert | OOS holt ab | fehlt |
|---|---|---|---|
| `elliott_wave` | 3 | 3 | — |
| `elliott_wave_stocks` | 4 | 4 | — |

Der Fix behebt den heutigen Fall. Diese Prüfung fängt den nächsten ab, wenn jemand
eine Dimension ins Raster aufnimmt und den OOS-Aufruf vergisst — genau die
Konstellation, die hier über Monate unbemerkt blieb.

---

## 8. Offener Punkt, bewusst nicht angefasst

`oos_equity_simulation.py` ruft `simulate_portfolio(trades, STARTING_CAPITAL,
ALLOCATION_PCT)` weiterhin **ohne** `max_concurrent_positions` auf — simuliert also
unbegrenzt viele gleichzeitige Positionen, während live 8 gelten und
`equity_simulation.py:195` den Wert korrekt übergibt.

Das ist der separate, niedriger priorisierte Befund aus PR #45 und ausdrücklich nicht
Teil dieser Aufgabe. Für die Einordnung der Zahlen oben ist er trotzdem relevant: er
macht sie nur eingeschränkt mit `experiment_no_take_profit.py` vergleichbar. Im
konkreten Lauf binden allerdings nur 8 von 128 Trades am Kapital, der Effekt dürfte
also klein sein.

---

## 9. Dateien

| Datei | Zweck |
|---|---|
| `oos_lauf.py` | Vorher-/Nachher-/Gegenproben-Lauf des echten Skripts, isolierter Prozess, umgeleitete Ergebnispfade |
| `test_oos_take_profit.py` | Selbsttests, Gruppen A–E |
| `stubs/yfinance.py` | Attrappe — `fetch_stock_data.py` importiert `yfinance` auf Modulebene, obwohl der Lauf nur dessen Konstante `INTERVAL` braucht. Ein echter Abruf wirft, statt still leere Daten zu liefern |
| `results/oos_vorher.json` | Rohdaten des Abbruchs inkl. In-Sample-Gewinner |
| `results/oos_nachher.json` | Rohdaten des korrigierten Laufs |
