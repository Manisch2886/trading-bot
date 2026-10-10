# TB-148 M3 — Träger der Ausstiege: Fundstellen

**Frage** (Antwort 09.10.a Z. 216, R84 (e), Teil in eckigen Klammern): ob `ereignisreihenfolge` in `research/mtm_drawdown/mtm_kern.py` die Reihenfolge der Ausstiege aus `capital_after` zurückgewinnt; ob eine ausgeführte Position bei jedem der neun Bots genau einen Ausstieg hat. Nur das Wie. Die zwei Schlusssätze der Klammer wendet die Sitzung nicht an.

Gelesen am HEAD ⟨S0⟩ `4ebd251` (Code unverändert gegenüber `3ecde87`). Die Trade-Liste, die `ereignisreihenfolge` bekommt, wurde nicht geöffnet.

## (a) Woher `ereignisreihenfolge` die Reihenfolge der Ausstiege nimmt

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| M3-1 | Zwischen verschiedenen Ausstiegszeitpunkten nimmt die Funktion die Reihenfolge aus `exit_time`: stabile Sortierung, dann Gruppen je `exit_time` aufsteigend. | `research/mtm_drawdown/mtm_kern.py` Z. 99; Z. 103 | `pos = pos.sort_values("exit_time", kind="stable").reset_index(drop=True)` / `for _, gruppe in pos.groupby("exit_time", sort=True):` | belegt |
| M3-2 | Innerhalb eines Zeitstempels gewinnt sie die Reihenfolge aus `capital_after` zurück: genommen wird die Position, deren Schritt `allocation * pnl_pct / 100` vom bisherigen Stand innerhalb `KETTEN_TOLERANZ` auf ihr `capital_after` führt; danach wird ihr `capital_after` der neue Stand. | Z. 105–119 | `schritt = pos.at[i, "allocation"] * pos.at[i, "pnl_pct"] / 100.0` / `if abs(kapital + schritt - pos.at[i, "capital_after"]) <= KETTEN_TOLERANZ:` / `kapital = float(pos.at[treffer, "capital_after"])` | belegt |
| M3-3 | Schliesst die Kette für keinen Kandidaten, bricht die Funktion mit `ValueError` ab. | Z. 112–116 | `if treffer is None:` / `raise ValueError(` / `f"Kapitalkette schliesst nicht bei exit_time "` | belegt |
| M3-4 | Die Toleranz ist eine Konstante des Kerns, begründet mit der Rundung von `capital_after` und `allocation` auf zwei Stellen. | Z. 66–72 | `KETTEN_TOLERANZ = 0.02` | belegt |
| M3-5 | Der Docstring sagt dasselbe: Die Reihenfolge bei gleichem Zeitstempel ist in der Liste nicht vermerkt und wird aus der Kette rekonstruiert. | Z. 83–92 | `Die ist in der Liste nicht vermerkt - aber die Kette` / `capital_after[k] = capital_after[k-1] + allocation[k] * pnl_pct[k] / 100` / `laesst sie rekonstruieren` | belegt |
| M3-6 | Die Ereigniskurve ist `capital_after` je Ausstieg in dieser Reihenfolge. | Z. 123–128 | `return pd.Series(ereignisse["capital_after"].to_numpy(dtype=float), index=pd.DatetimeIndex(ereignisse["exit_time"]), name="capital_after")` | belegt |
| M3-7 | Die Positionen kommen aus einer gespeicherten Trade-Liste mit den Pflichtspalten `allocation` und `capital_after` (Liste aus TB-24), nicht aus einem Aufruf von `simuliere_portfolio`. | `research/mtm_drawdown/grundlage.py` Z. 58–59; Z. 62–71 | `PFLICHTSPALTEN = ("symbol", "entry_time", "exit_time", "entry_price", "exit_price", "pnl_pct", "allocation", "capital_after")` / `pos = pd.read_csv(pfad, parse_dates=["entry_time", "exit_time"])` | belegt |
| M3-8 | `simuliere_portfolio` schreibt je verbuchtem Ausstieg genau eine Zeile mit `capital_after` in die `equity_curve`; die Reihenfolge der Ausstiege bei gleichem Zeitstempel kommt dort aus `ausstiegsreihenfolge` (seeded Zufall, M1). | `shared/zuteilung.py` Z. 724–735; Z. 540 | `for pos in zuteiler.ausstiegsreihenfolge(ausstiege_je_zeit.get(zeit, ())):` / `"capital_after": round(capital, 2),` | belegt |
| M3-9 | Aufrufer von `ereignisreihenfolge`: `grundlage.pruefe_bot`, `messung.main`, `richtungsfall.fall`, der Test (Gegenprobe K1 mit vertauschter Reihenfolge). | `research/mtm_drawdown/grundlage.py` Z. 198; `research/mtm_drawdown/messung.py` Z. 142; `research/mtm_drawdown/richtungsfall.py` Z. 65; `research/mtm_drawdown/test_mtm_kern.py` Z. 41–43, 101, 231–232, 236 | `ereignisse = mtm_kern.ereignisreihenfolge(pos, float(meta["startkapital"]))` / `pruefe(e["symbol"].tolist() == ["Q", "P"], "K1: Reihenfolge aus der Kette rekonstruiert (Q vor P)")` | belegt |

**Antwort zu (a):** Ja — `ereignisreihenfolge` gewinnt die Reihenfolge der Ausstiege **bei gleichem Zeitstempel** aus `capital_after` zurück (zusammen mit `allocation` und `pnl_pct`, Toleranz `KETTEN_TOLERANZ`); zwischen verschiedenen Zeitstempeln nimmt sie sie aus `exit_time` (Z. 99–119).

## (b) Hat eine ausgeführte Position genau einen Ausstieg? — je Bot

Gemeinsame Kette für alle neun Bots (in `shared/zuteilung.py`):

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| M3-10 | Jede Zeile der Trade-Tabelle hat genau eine `exit_time`; sie wird genau einmal in die Ausstiegsliste ihres Zeitpunkts eingetragen. | `shared/zuteilung.py` Z. 704; Z. 710–712 | `ausstieg = pd.to_datetime(trades["exit_time"]).to_numpy()` / `ausstiege_je_zeit.setdefault(ausstieg[pos], []).append(pos)` | belegt |
| M3-11 | Beim Ausstieg wird die ganze Allokation aus `open_positions` entfernt (`pop`); einen Teilausstieg gibt es nicht, ein zweiter Ausstieg derselben Position wird übersprungen. | Z. 725–730 | `if pos not in open_positions:` / `continue` / `allocation = open_positions.pop(pos)` | belegt |
| M3-12 | Ausstiege werden je Zeitpunkt vor Einstiegen verbucht. | Z. 722–724, 737 | `# --- Ausstiege zuerst: das Kapital wird frei -----------------------` | belegt |

| Bot | Antwort | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| `elliott_wave` | **genau einer** — `simulate_trade` gibt je Trade genau ein Ergebnis mit einer `exit_time` zurück (erste Stop-/Ziel-Kerze oder letzte Kerze der Haltedauer, nur Kerzen nach `entry_time`); ohne Ausstieg (`no_data`) entsteht kein Trade. Dazu M3-10/M3-11. | `strategies/elliott_wave/backtest_elliott.py` Z. 82–100; Z. 139–140; Z. 151–162 | `future = price_df[price_df["open_time"] > entry_time].head(max_hold_hours)` / `if outcome["exit_price"] is None or outcome["result"] == "no_data": continue` | erschlossen |
| `t3_supertrend` | **genau einer** — Zustandsmaschine mit höchstens einer offenen Position; beim ersten Ausstiegssignal eine Zeile, dann `position = None`; eine am Datenende offene Position wird nicht als Trade geschrieben. | `strategies/t3_supertrend/backtest_trend.py` Z. 105–135 | `if stop_hit or trend_flip or t3_crossed_down:` / `"exit_time": open_time[i],` / `position = None` | erschlossen |
| `rsi2_crypto` | **genau einer** — die innere Schleife bricht beim ersten Ausstieg ab; ohne Ausstieg endet der Scan (`break`), der Scan geht nach dem Ausstieg weiter. | `strategies/rsi2_crypto/backtest_rsi2.py` Z. 106–121; Z. 127–134 | `exit_idx, exit_price, result = idx, stop_price, "stop_loss"` / `break` / `if exit_idx is None: break` / `i = exit_idx + 1` | erschlossen |
| `turtle_soup_crypto` | **genau einer** — gleiche Bauart. | `strategies/turtle_soup_crypto/backtest_turtle_soup.py` Z. 153–165; Z. 171–178 | `if exit_idx is None:` / `break` / `i = exit_idx + 1` | erschlossen |
| `volatility_breakout_crypto` | **genau einer** — gleiche Bauart. | `strategies/volatility_breakout_crypto/backtest_breakout.py` Z. 156–168; Z. 174–181 | `if exit_idx is None:` / `break` / `i = exit_idx + 1` | erschlossen |
| `elliott_wave_stocks` | **genau einer** — wie `elliott_wave`. | `strategies/elliott_wave_stocks/backtest_elliott.py` Z. 91–109; Z. 151–152; Z. 163–174 | `future = price_df[price_df["open_time"] > entry_time].head(max_hold_hours)` / `continue` | erschlossen |
| `rsi2_mean_reversion` | **genau einer** — wie `rsi2_crypto`. | `strategies/rsi2_mean_reversion/backtest_rsi2.py` Z. 149–164; Z. 170–177 | `break  # nicht genug Restdaten, um diese Position zu schliessen - Scan beenden` / `i = exit_idx + 1  # kein Pyramiding` | erschlossen |
| `turtle_soup_stocks` | **genau einer** — wie `turtle_soup_crypto`. | `strategies/turtle_soup_stocks/backtest_turtle_soup.py` Z. 149–161; Z. 167–174 | `if exit_idx is None:` / `break` / `i = exit_idx + 1` | erschlossen |
| `volatility_breakout` | **genau einer** — wie `volatility_breakout_crypto`. | `strategies/volatility_breakout/backtest_breakout.py` Z. 197–209; Z. 215–222 | `break  # nicht genug Restdaten, um diese Position zu schliessen - Scan beenden` / `i = exit_idx + 1  # kein Pyramiding` | erschlossen |

Kette je Bot: Backtest-Modul (eine Zeile, eine `exit_time` je Trade) → `collect_all_trades` hängt die Zeilen nur zusammen (je `strategies/<Bot>/equity_simulation.py`, z. B. `elliott_wave` Z. 76–90; bei `t3_supertrend` und `volatility_breakout_crypto` filtert der Regimefilter nur ganze Zeilen weg, `t3_supertrend/equity_simulation.py` Z. 82–85, `volatility_breakout_crypto/equity_simulation.py` Z. 112–122; bei den vier Aktien-Bots werden Zeilen ohne Kurs ganz gestrichen, z. B. `rsi2_mean_reversion/equity_simulation.py` Z. 95–101) → `simuliere_portfolio` (M3-10, M3-11).

**Antwort zu (b):** Bei allen neun Bots hat eine ausgeführte Position **genau einen** Ausstieg (erschlossen aus den zitierten Zeilen; kein Lauf).
