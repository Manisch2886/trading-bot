# `t3_supertrend`: fünf Indikatorwerte zentralisieren — inkl. `forward_test.py`

**Stand:** 2026-09-08 · **Branch:** `claude/forward-test-sync-t3`

> **Dieser PR ändert das Live-Skript.** `forward_test.py` läuft per Cron. Der
> Nachweis, dass sich sein Verhalten nicht ändert, ist der eigentliche Inhalt
> dieses Berichts.

---

## 1. Was geändert wurde

| Datei | Änderung |
|---|---|
| `live_params.py` | `T3_FACTOR` 0.7, `DI_LENGTH` 14, `ADX_LENGTH` 14, `ATR_LENGTH` 22, `ATR_MULT` 3.0 **neu aufgenommen** — Werte unverändert |
| `backtest_trend.py` | eigene Zahlen → Import |
| `forward_test.py` | eigene Zahlen → Import (bestehender `live_params`-Import erweitert) |

Der Dokumentationsblock aus PR #49, der die Doppelführung als offene Falle
beschrieb, ist entsprechend umgeschrieben — die Falle ist geschlossen.

**Ein Punkt daraus bleibt bewusst offen:** die ATR-Literale in `regime_filter.py:19`
(22 / 3.0) sind **nicht** mitumgestellt. Der Regime-Filter rechnet den SuperTrend auf
BTC, nicht auf dem Handelssymbol — dass die Zahlen zufällig gleich sind, macht sie
nicht zur selben Größe. Sie gleichzusetzen wäre eine inhaltliche Entscheidung, keine
Aufräumarbeit; das steht so auch im Kommentar.

---

## 2. Der Nachweis für `forward_test.py`

`research/forward_test_sync/vergleich.py` lädt die **alte Fassung aus git** und die
**neue aus dem Arbeitsbaum** als zwei getrennte Module **im selben Prozess** und ruft
beide mit identischen Eingaben auf.

| # | Weg | Ergebnis |
|---|---|---|
| 1 | **Namensraum** — alle 16 Modulkonstanten | identisch |
| 2 | **Syntaxbaum** — Modulrumpf ohne die betroffenen Zuweisungen/Importe | identisch |
| 3 | **Verhalten** — Indikatoren, `check_open_trades()`, `find_new_signals()` auf echten 4h-Daten | Indikatoren, DB-Inhalt **und** Bildschirmausgabe identisch |

**15/15 Prüfungen bestanden.**

### Warum der Nachweis hier besonders scharf ist

Bei `rsi2_crypto` wirkte der umgestellte Wert nur in einem seltenen Ausstiegspfad, der
gezielt gesucht werden musste. Hier ist es umgekehrt: die fünf Werte gehen **direkt in
die Indikatorberechnung** ein (`compute_indicators(df, T3_FAST_LENGTH, T3_SLOW_LENGTH,
T3_FACTOR, DI_LENGTH, ADX_LENGTH, ATR_LENGTH, ATR_MULT)`, `forward_test.py:194/195`).
Jede noch so kleine Abweichung schlägt sofort auf **alle Spalten aller Symbole** durch.

Belegt durch die Empfindlichkeitsprobe: mit `--stoere ATR_MULT=2.5` meldet der
Vergleich bereits bei `Indikatoren fuer BNBUSDT identisch` einen Fehler — der Test
merkt eine Änderung also am ersten Symbol, nicht erst irgendwo im Ergebnis.

### Die drei Zustände des Werkzeugs

| Lauf | Erwartung | Ergebnis |
|---|---|---|
| **Leerprobe** (nichts geändert) | meldet identisch | 14/15 — nur „es gibt einen Unterschied" schlägt fehl, korrekt |
| **Empfindlichkeitsprobe** (`ATR_MULT=2.5`) | **muss** anschlagen | 7/10 — Namensraum und Indikatoren weichen ab |
| **Echte Umstellung** | identisch, bei vorhandenem Code-Unterschied | **15/15** |

---

## 3. Backtest-Regression

| | |
|---|---|
| Endkapital (Start 10.000) | 22.963,95 (**+129,64 %**) |
| ausgeführt / übersprungen | 656 / 324 |
| Max Drawdown | −22,20 % |
| stdout-Hash und `equity_curve.csv`-Hash | **identisch** |

---

## 4. Trockentest

`forward_test.py` importiert und bis `print_summary()` durchlaufen — dieselbe Kette wie
im Cronjob (`init_db`, `compute_indicators`, `check_open_trades`, `find_new_signals`),
mit temporärer Datenbank und werfender Netz-Attrappe. Kein Laufzeitfehler; alle fünf
Werte kommen korrekt an (0.7 / 14 / 14 / 22 / 3.0).

---

## 5. Zwei Anpassungen am Prüfwerkzeug

Die beiden Bots sind unterschiedlich gebaut; das Werkzeug bekam dafür Profile statt
Verzweigungen im Code. Zwei Unterschiede waren nicht offensichtlich:

- **Schema.** `rsi2_crypto` führt eine Spalte `rsi_at_entry`, `t3_supertrend` nicht. Das
  Werkzeug liest das Schema jetzt per `PRAGMA table_info` aus, statt Spalten anzunehmen —
  eine Annahme wäre hier ein Testaufbau-Fehler, der wie ein Befund ausgesehen hätte.
- **Stop-Preis.** `rsi2_crypto` fängt einen fehlenden Stop ab (dort ist `STOP_LOSS_PCT
  = None` die validierte Wahl), `t3_supertrend` rechnet ungeschützt
  `row["low"] <= trade["stop_price"]`. Der Vergleich setzt deshalb für t3 einen Stop mit
  demselben Abstand, den `forward_test.py` live verwendet.

Dass die Verallgemeinerung den `rsi2`-Nachweis nicht beschädigt hat, ist mitgeprüft:
die Leerprobe für `rsi2_crypto` läuft mit dem neuen Werkzeug unverändert durch.

---

## 6. Entscheidungsgrundlage

**Warum überhaupt:** dieselbe strukturelle Falle wie bei
`elliott_wave_stocks/USE_TAKE_PROFIT`, wo sie tatsächlich zuschnappte. PR #49 hatte sie
für diesen Bot nur dokumentiert; hier wird sie geschlossen.

**Warum eine Kopplung hier unbedenklich ist:** anders als `T3_FAST_LENGTH`,
`T3_SLOW_LENGTH`, `ADX_THRESHOLD` und `STOP_LOSS_PCT` werden diese fünf von **keinem**
Suchraster variiert (belegt in PR #45). Eine Kopplung nimmt den Optimierungs-Skripten
also keine Freiheit — genau der Unterschied, der die anderen vier bewusst ungekoppelt
lässt.

**Was nicht passiert ist:** keine Wertänderung, keine Änderung an Handelsregeln, keine
Aktivierungsempfehlung, keine Umstellung des Regime-Filters. `LAST_UPDATED` bleibt auf
`2026-08-31` — der Wert bezeichnet den Stand der Parameter, und der ist unverändert.
