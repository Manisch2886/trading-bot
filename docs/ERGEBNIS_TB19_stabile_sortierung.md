# TB-19 — Stabile Sortierung

**Zum Kopieren.** Ausführlich: `docs/UEBERGABE_TB19_stabile_sortierung.md` ·
Prüfanleitung: `docs/TESTAUFTRAG_TB19_stabile_sortierung.md`

---

## Die Zahlen

| Kennzahl | vorher | nachher |
|---|---:|---:|
| Kombinierter Vierer-Drawdown | −9,34 % | **−9,41 %** |
| Montags-Mail / Dashboard, kombinierter Drawdown | −11,29 % | **−11,41 %** |

Beide Werte sind exakt die vorhergesagten.

**Die Dashboard-Portfolio-Sicht zeigt ab jetzt −11,41 % statt −11,29 %.**
Kein neuer Fehler — die Korrektur.

Mit verschoben, ohne dass es angekündigt war: die Einzel-Drawdowns von
`rsi2_crypto` (−13,11 → −13,30 %), `turtle_soup_stocks`
(−18,67 → −18,71 %) und RSI-2 Mean-Reversion (−11,17 → −11,73 %) sowie
21 der 26 bezifferten Korrelationen. Keine überschreitet die Schwelle
0,3 (grösster Betrag: 0,14 → 0,16) — es ändert sich keine Aussage, nur
die Nachkommastellen. Renditen sind unverändert.

## Was der Fehler war

`sort_values("time")` ohne `kind="stable"` vertauscht Zeilen mit gleichem
Zeitstempel. `groupby("date").last()` greift dann einen **Zwischenstand
mitten im Tag** ab statt des Tagesschlusses.

Dass die neuen Zahlen die richtigen sind, hängt nicht an Geschmack:
alle neun `equity_curve.csv` stehen bereits in Ereignisreihenfolge —
nachgemessen — und eine stabile Sortierung lässt sie unverändert.

Betroffen sind **alle neun Bots**, nicht nur die Aktien-Bots: von 1
abweichenden Tag (`elliott_wave`) bis 698 von 2.022 (`turtle_soup_stocks`).

## Geändert

| Datei | |
|---|---|
| `shared/portfolio_overview.py` | nur die Sortierzeile |
| `strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py` | Sortierzeile + Kommentar |
| `shared/test_stabile_sortierung.py` | neu, 46 Prüfungen |

Nicht angefasst: `live_params.py`, `forward_test.py`,
`equity_simulation.py`, `results/*/equity_curve.csv`, die abgelegten
Optimierungsergebnisse, `broker/`, Crontab, `research/`-Berichte.

## Die weiteren `sort_values`-Stellen

**144** Aufrufe auf `main`, **31** schon stabil, **113** ohne `kind=`.
TB-19 stellt **2** um, **111 bleiben**. Drei Befunde daraus:

1. **19 weitere Stellen haben denselben Fehler** — dieselbe
   `build_daily_capital_curve`-Vorlage steht 21-mal im Repo. Nicht
   angefasst, weil ihre Ausgaben in bereits veröffentlichten Experiment-
   und `research/`-Dokumenten stehen. **Folgeaufgabe.**
2. **`elliott_wave_counter.py` entscheidet per Quicksort, welches Muster
   live wird.** `sort_values("fib_score")` läuft über eine Spalte mit
   vielen Gleichständen (8 von 11 Zeilen in der abgelegten BTC-Datei);
   `elliott_wave_stocks/forward_test.py:168` bricht bei
   `MAX_CONCURRENT_POSITIONS = 8` ab. Die einzige gefundene Stelle, die
   bis in den **laufenden Betrieb** durchschlägt. Sperrliste — gemeldet.
3. **`equity_simulation.py` ist gefährdet, heute aber unauffällig.**
   `collect_all_trades` sortiert `entry_time` instabil (fast alle Zeilen
   teilen einen Zeitstempel), liefert bei zwei nachgemessenen Bots aber
   heute dieselbe Reihenfolge wie stabil. Deshalb `9x AKTUELL`.
   Nicht garantiert. Sperrliste — gemeldet.

**Ungefährdet:** die 27 `open_time`-Stellen auf Kursdaten — 0 Dubletten in
allen 242 `data/*.csv`, gemessen.

## Geprüft

* `shared/test_stabile_sortierung.py`: **46 von 46** (`--schnell`: 41 von 41)
* `shared/ergebniskurven.py`: **9x AKTUELL**
* Beide Skripte zweimal: byteweise identisch
* Bestehende Selbsttests: unverändert gegenüber dem Basislauf auf `main`

Der Test prüft **Verhalten, nicht Quelltext**, und weist an mutierten
Kopien der echten Dateien nach, dass er rot werden kann.
