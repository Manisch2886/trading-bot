# `rsi2_crypto`: `MAX_HOLD_DAYS` zentralisieren — inkl. `forward_test.py`

**Stand:** 2026-09-08 · **Branch:** `claude/forward-test-sync-rsi2` (neu von `main` @ `b429ea5`)

> **Dieser PR ändert das Live-Skript.** `forward_test.py` läuft per Cron.
> Der **Wert bleibt unverändert 10** — nur seine Quelle wird vereinheitlicht.

**Ersetzt den geschlossenen PR #50.** Dessen Branch trug noch die einfache, nur auf
`rsi2_crypto` zugeschnittene Fassung des Prüfwerkzeugs; die verallgemeinerte Fassung
kam mit PR #51 nach `main`. Der Branch ist deshalb neu von `main` aufgesetzt und der
Nachweis vollständig mit dem **Werkzeug aus `main`** wiederholt — kein Konflikt, keine
zweite Werkzeugfassung im Repo.

---

## 1. Was geändert wurde

| Datei | Änderung |
|---|---|
| `live_params.py` | `MAX_HOLD_DAYS = 10` **neu aufgenommen** — Wert unverändert |
| `backtest_rsi2.py` | eigene Zahl → `from live_params import MAX_HOLD_DAYS` |
| `forward_test.py` | eigene Zahl → Import (bestehender `live_params`-Import erweitert) |

Vorher stand `= 10` zweimal unabhängig im Bot (`backtest_rsi2.py:49`,
`forward_test.py:50`), und `live_params.py` kannte den Wert gar nicht — der einzige der
drei Zeit-Exit-Bots ohne gemeinsame Quelle.

---

## 2. Nachweis: die Werte sind unverändert

Nicht per Augenschein, sondern maschinell — Modulkonstanten aus `origin/main` gegen den
neuen Stand:

| Datei | geänderte Werte | entfernte Namen | neue Namen |
|---|---|---|---|
| `live_params.py` | **keine** | keine | `MAX_HOLD_DAYS: 10` |
| `backtest_rsi2.py` | **keine** | `MAX_HOLD_DAYS: 10` | keine |
| `forward_test.py` | **keine** | `MAX_HOLD_DAYS: 10` | keine |

Die „entfernten" Namen sind genau der Punkt: sie kommen jetzt per Import statt als
eigene Zahl. Zur Laufzeit angekommen:

```
backtest_rsi2.MAX_HOLD_DAYS = 10
forward_test.MAX_HOLD_DAYS  = 10
live_params.MAX_HOLD_DAYS   = 10
```

---

## 3. Nachweis: `forward_test.py` verhält sich identisch

`research/forward_test_sync/vergleich.py` (Fassung aus `main`) lädt die **alte Fassung
aus git** und die **neue aus dem Arbeitsbaum** als zwei getrennte Module **im selben
Prozess** und ruft beide mit identischen Eingaben auf.

| # | Weg | Ergebnis |
|---|---|---|
| 1 | **Namensraum** — alle 13 Modulkonstanten | identisch |
| 2 | **Syntaxbaum** — Modulrumpf ohne die betroffenen Zuweisungen/Importe | identisch |
| 3 | **Verhalten** — `check_open_trades()` + `find_new_signals()` auf echten Tagesdaten | DB-Inhalt **und** Bildschirmausgabe zeichengenau identisch |

**11/11 Prüfungen bestanden** — dieselbe Zahl wie im geschlossenen PR #50.

### Die drei Zustände, vollständig wiederholt

| Lauf | Erwartung | Ergebnis |
|---|---|---|
| **Leerprobe** (vor der Änderung) | meldet identisch | 10/11 — nur „es gibt einen Unterschied" schlägt fehl, korrekt |
| **Empfindlichkeitsprobe** (`--stoere MAX_HOLD_DAYS=9`, vor der Änderung) | **muss** anschlagen | 7/11 — Namensraum, DB-Inhalt und Ausgabe weichen ab, 16 Zeit-Exits |
| **Echte Umstellung** | identisch, bei vorhandenem Code-Unterschied | **11/11** |

Beide Vorproben wurden **vor** der inhaltlichen Änderung gefahren, mit dem Werkzeug aus
`main`. Erst die mittlere Zeile macht die anderen aussagekräftig: ohne sie wäre
„identisch" auch mit einem blinden Test zu bekommen — genau das war die erste Fassung
des Werkzeugs (siehe unten).

### Warum die Empfindlichkeitsprobe unverzichtbar ist

Die ursprüngliche Fassung des Werkzeugs setzte einen Einstieg 200 Kerzen vor dem Ende
und prüfte, dass Positionen geschlossen wurden. Sie wurden geschlossen — aber über den
**SMA-Exit**. Der Zeit-Exit, der einzige Pfad, in dem `MAX_HOLD_DAYS` überhaupt
vorkommt, wurde nie durchlaufen. Auf echten Tagesdaten führen nur rund 1 % der
Einstiegspunkte dorthin (bei BTCUSDT 15 von ~1600).

Die in `main` liegende Fassung sucht die Einstiege deshalb gezielt und zählt
`time_exit`-Ergebnisse statt bloß geschlossener Zeilen — im Lauf oben: **16 Zeit-Exits**.

---

## 4. Backtest-Regression

Gegen `origin/main`, alte Fassung per `git show` in einen Symlink-Baum, beide Läufe
gegen dieselben Kursdaten:

| | |
|---|---|
| Trades gefunden | 439 |
| Endkapital (Start 10.000) | 12.837,09 (**+28,37 %**) |
| ausgeführt / übersprungen | 392 / 47 |
| Max Drawdown | −13,30 % |
| stdout-Hash und `equity_curve.csv`-Hash | **identisch** |

Identisch zu den Zahlen aus dem geschlossenen PR #50 — die Neuaufsetzung hat nichts
verschoben.

---

## 5. Trockentest

`trockentest.py` importiert `forward_test.py` und durchläuft `init_db()`,
`compute_indicators()`, `check_open_trades()`, `find_new_signals()`, `print_summary()`
— dieselbe Kette wie im Cronjob, mit temporärer Datenbank und werfender Netz-Attrappe.
Kein Laufzeitfehler; `MAX_HOLD_DAYS=10` kommt korrekt an.

Das ist die Ergänzung zu `py_compile`: ein fehlerhafter Import fällt erst beim Ausführen
auf, nicht beim Übersetzen.

---

## 6. Was der Nachweis nicht abdeckt

Netzabruf und Cron-Einbettung — beide von der Änderung nicht berührt. Damit das nicht
stillschweigend bleibt: die Attrappen **werfen**, sobald jemand doch einen echten Abruf
oder eine Binance-Verbindung versucht. Ein versehentlich echter Aufruf würde den Lauf
abbrechen, nicht still durchgehen.

---

## 7. Entscheidungsgrundlage

**Warum:** derselbe strukturelle Fehler wie bei `elliott_wave_stocks/USE_TAKE_PROFIT`,
wo die Doppelführung tatsächlich auseinanderlief und ein Backtest monatelang eine andere
Strategie beschrieb als die laufende. Hier stimmten die Zahlen noch überein — die
Umstellung schließt die Lücke, bevor sie zuschnappt.

**Warum `live_params.py`:** die anderen beiden Zeit-Exit-Bots machen es bereits so.

**Warum das Live-Skript angefasst werden musste:** `forward_test.py` ist selbst eine der
beiden redundanten Quellen.

**Was nicht passiert ist:** keine Wertänderung, keine Änderung an Handelsregeln, keine
Aktivierungsempfehlung. `LAST_UPDATED` bleibt `2026-09-03` — der Wert bezeichnet den
Stand der Parameter, und der ist unverändert.
