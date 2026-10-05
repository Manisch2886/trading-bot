# REGISTER-KOPIE Abschnitt 11 (von 0–54) — Register-Z. 1172–1254 — Commit 9b7b06065ebdae3f36f3102306c76bb844300e90 — 2026-10-05 — Original sha256 8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc — KOPIE, nicht das Register

## 11. Voraussetzungen des Laufs (zwei Bug-Fixes, beide TB-30b)

TB-30a darf `strategies/*/equity_simulation.py`,
`strategies/*/multi_symbol_optimise.py` und
`strategies/*/multi_symbol_walk_forward.py` **nicht** anfassen. Die
Entscheidungen sind hier getroffen und die Mechanik ist hier gebaut und
geprüft; der Einbau ist TB-30b.

### 11.1 AB2/U5 — der stillschweigend übersprungene BTC-Regimefilter

`t3_supertrend` überspringt seinen BTC-Regimefilter **stillschweigend**, wenn
`BTCUSDT` fehlt; `volatility_breakout_crypto` bricht ab.

**Entscheidung: abbrechen.** Ein Lauf, in dem ein Bot still ohne Filter
rechnet, ist nicht deterministisch — dieselben Parameter liefern je nach
Inhalt von `data/` verschiedene Ergebnisse, und nichts in der Ausgabe sagt,
welcher Fall vorlag. Der Filter ist zudem keine Nebensache: beim T3-Bot senkt
er den Max Drawdown von −31,2 % auf −22,2 % (Protokoll 3.2). Ein Lauf ohne
ihn beschreibt eine **andere Strategie**.

Die Wache steht fertig und geprüft in **`shared/regimewache.py`**
(`shared/test_regimewache.py`: 16 Prüfungen). Einzubauen an drei Stellen:

| Datei | heute | einzubauen |
|---|---|---|
| `strategies/t3_supertrend/equity_simulation.py:77` | `if "BTCUSDT" in all_data:` ohne Gegenzweig | `btc_daten(all_data, bot="t3_supertrend", holen="python3 fetch_4h_data.py")` |
| `strategies/t3_supertrend/multi_symbol_optimise.py:123` | dito | dito |
| `strategies/volatility_breakout_crypto/equity_simulation.py:103` | bricht bereits ab | auf die gemeinsame Wache umstellen |

`regimewache.pruefe_einbau()` beantwortet maschinell, ob der Einbau erfolgt
ist. Solange er es nicht ist, darf der Lauf nicht starten.

### 11.2 Agent 2 — Auswahl auf dem führenden Mass

Agent 2 (`shared/param_search_agent.py`) optimierte seit dem 13.09. auf dem
**chronologischen** Drawdown, und der Satz *„es gilt das chronologische"* war
im Prompt fest verdrahtet — seit Festlegung 1 falsch.

**Umgestellt, in `shared/`, ohne Bot-Code anzufassen.** An die Stelle des
fest verdrahteten Satzes tritt eine dreistufige Kaskade
(`ZIELMASS_KASKADE`), die in jeder Stufe sagt, welches Mass gilt und warum
nicht das führende:

1. `robustness_score_kapital` auf `max_drawdown_kapital_pct` — **das führende
   Mass**
2. `robustness_score_chronologisch` — der Stellvertreter
3. `robustness_score` — der Notweg

**Heute greift Stufe 2**, weil `multi_symbol_optimise.evaluate_combination_multi`
den Kapital-Drawdown noch nicht mitliefert. Das nachzurüsten ist TB-30b. Der
Unterschied zu vorher ist nicht die Zahl, sondern dass der Agent den Ersatz
**als Ersatz ausweist** statt ihn als Zielgrösse zu behaupten — und dass er
von selbst umschaltet, sobald das Feld da ist, ohne dass jemand daran denken
muss. Geprüft in `shared/test_agent2_kapitalmass.py` (34 Prüfungen); die 41
Prüfungen aus TB-22 bestehen unverändert.

> ⭐ **11.2 ERGÄNZT durch R43 (48.11)** (Fable 29b R43, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 11.3 Zwei Achsen brauchen eine Durchreichung

* `rsi2_mean_reversion`: `SMA_TREND_PERIOD = 200` ist in
  `backtest_rsi2.py` eine Konstante und muss Parameter werden — sonst gilt
  für die Aktien- und die Krypto-Variante nicht dieselbe Regel.
* `volatility_breakout` und `volatility_breakout_crypto`:
  `BB_SQUEEZE_PERCENTILE` und `BB_LOOKBACK` stehen in `live_params.py`, aber
  nicht im Optimierer.

> ⭐⭐ **Stand der Voraussetzungen aus Abschnitt 11 (42.3 F3, 42.4 G1, Fable 25c,
> TB-108, 25.09.2026):** **11.1 ist geschlossen** (TB-105, `f524327`:
> `regimewache.pruefe_einbau()` 3 von 3; vorher rechnete `t3_supertrend` ohne
> BTCUSDT still weiter, gemessen). **11.2 und 11.3 sind offen** (TB-30b). Wer
> „Abschnitt 11 erfüllt" liest, liest zu viel. Der Text oben bleibt
> zeichengleich.

> ⭐ **Abschnitt 11 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (h), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **11.3 ERGÄNZT durch 50.3 und 50.4** (Tatsachennotiz, Vollzug TB-122 und TB-124 nach 37.3, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

