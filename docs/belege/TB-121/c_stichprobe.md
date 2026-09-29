# TB-121 Schritt C — Stichprobe Text gegen Code

Auswahl: die ersten zwölf Stellen in Textreihenfolge, an denen 0–12 einen Code-Bezeichner (Funktion, Konstante, Feld- oder Parametername) **zusammen mit seiner Datei** nennt. Nachgeschlagen per `grep`/`sed` am HEAD `86e0d5e`, nur die jeweilige Definition gelesen, nichts ausgeführt.

⚠️ Die im Auftrag als Beispiele genannten `auswertung.py::kapitalregel` (Zeile 788) und `registerdaten.SPITZEN_SCHWELLE` (Zeile 926) liegen in Textreihenfolge auf Platz 13 und 14 und sind deshalb **nicht** in der Stichprobe. `SPITZEN_SCHWELLE = 0.50` wurde beim Lesen von `FESTLEGUNGEN` mitgesehen (`registerdaten.py:98`, direkt unterhalb) — nicht geprüft, nur vermerkt. `benchmark.py::erlaubt` ist Nr. 10.

| # | Bezeichner | genannt in Zeile | gefunden (Datei:Zeile am `86e0d5e`) | passt | Satz |
|---:|---|---:|---|---|---|
| 1 | `research/vorregistrierung/registerdaten.py::FESTLEGUNGEN` | 52 | ja, `registerdaten.py:69` | ja | Dict mit zwölf Einträgen, Nummern und Kurztexte entsprechen der Tabelle in 1; Nr. 6 trägt im Code die −28-%-Begründung aus 4.3, Nr. 12 den Satz ohne den kursiven Nachsatz. |
| 2 | `notifications/manual_close.py::allokation()` | 132 | ja, `manual_close.py:458` | ja | Liefert `ALLOCATION_PCT` als Anteil samt Quelldatei; `floor(1/…)` rechnet sie nicht selbst, das Register sagt auch nur „gelesen über“. |
| 3 | `strategies/elliott_wave/equity_simulation.py` ohne `max_concurrent_positions` | 154–155 | ja, Datei vorhanden; `max_concurrent` kommt **0-mal** vor | ja | Die behauptete Abwesenheit stimmt. |
| 4 | `strategies/elliott_wave_stocks/multi_symbol_optimise.py:39` `STOP_LOSS_RANGE` | 173–174 | ja, aber in **Zeile 44** | ja | Wert `[2.0, 3.0, 5.0, 8.0]` mit Kommentar „erweitert (bis 8%) nach Erkenntnis aus compare_exit_rules.py“ wie beschrieben; die Zeilennummer 39 gilt für einen ungenannten Commit (Abschnitt 0 erlaubt das für alte Abschnitte). |
| 5 | `auswertung.py` (`markierungen`) | 178 | ja, `auswertung.py:714` | ja | Schlüssel `markierungen` setzt „Spitze“, „Kante“, „nicht zulaessig“. ⚠️ Randbefund: „ohne Limitachse“ (2.4, 8) steht dort nicht, `grep` findet es in `auswertung.py` 0-mal; ob es anderswo gesetzt wird, ist nicht geprüft. |
| 6 | `backtest_rsi2.py` `SMA_TREND_PERIOD = 200` (rsi2_mean_reversion) | 203 | ja, `strategies/rsi2_mean_reversion/backtest_rsi2.py:88` | ja | Weiterhin Modulkonstante, passt zu „muss durchgereicht werden“ und zur Marke „11.3 offen“. |
| 7 | `live_params.py` `bb_squeeze_percentile`, `bb_lookback` (beide Volatility-Breakout-Bots) | 204–205 | ja, als `BB_SQUEEZE_PERCENTILE`/`BB_LOOKBACK` in `volatility_breakout/live_params.py:22–23` und `volatility_breakout_crypto/live_params.py:40–41` | ja | In beiden `multi_symbol_optimise.py` kommen die Namen 0-mal vor — passt zu „aber nicht im Optimierer“. Der Text schreibt die Namen klein, der Code gross. |
| 8 | `registerdaten.geometrische_stufen()` | 211 | ja, `registerdaten.py:238` | ja | Bricht ab bei Faktor ausserhalb 1,5–2,0 — und zusätzlich bei weniger als 3 oder mehr als 5 Stufen, was der Satz in 2.7 nicht nennt. |
| 9 | `lineare_stufen()` (registerdaten) | 212 | ja, `registerdaten.py:255` | ja | Bricht ab, wenn gerundete Stufen zusammenfallen; ebenfalls Stufenzahl 3–5 erzwungen. |
| 10 | `research/vorregistrierung/benchmark.py::erlaubt` | 447 | ja, `benchmark.py:324` | ja | `min(DD_RELATIVER_FAKTOR × dd_benchmark, dd_toleranz)`; nimmt die beiden Werte, nicht die Falte. |
| 11 | `benchmark.py::nachschlagen` | 465 | ja, `benchmark.py:224` | ja | Lineare Interpolation zwischen Stützstellen wie beschrieben. Der Code regelt zusätzlich, was der Text offen lässt (Befund 70): Exposure wird auf 0–1 begrenzt, bei 0 ist das Ergebnis 0, unter der ersten Stützstelle linear gegen 0. |
| 12 | `beispieldaten.py::jahre_aus_register_5_1_nr_4` | 582 | ja, `beispieldaten.py:68` | ja | Regulärer Ausdruck auf genau die Zeilenform aus 5.1 Nr. 4, genau ein Treffer, sonst `None` — wie die Marke sagt. |

**Ergebnis:** 12 von 12 gefunden, 12 von 12 passen zum beschriebenen Verhalten. Eine Zeilenangabe weicht ab (Nr. 4, 39 → 44), zwei Funktionen tun mehr, als der Text sagt (Nr. 8/9 Stufenzahl, Nr. 11 Randverhalten), und eine Markierung aus dem Text ist im genannten Schlüssel nicht zu sehen (Nr. 5).
