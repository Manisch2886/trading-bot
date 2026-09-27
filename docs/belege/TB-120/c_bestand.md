# TB-120 C — Bestand im Code, gemessen

Stand `HEAD` bei der Messung: `3265b3a` (Code unverändert seit `d9e3600`; diese Sitzung hat keinen Code angefasst).
Nur gelesen: `c_messung.py` → `c_messung.txt` (ast/Text, kein Import von Laufcode), `c2_suche.txt` (grep über
`git ls-files`), `c1_listen_hashes.txt` (sha256). Einzige Ausführung von Projektcode: `regimewache.pruefe_einbau()`
(liest Quelltext, importiert nichts) und `registerdaten.raster_definition()` (liest die Achsen); `git status` danach
unverändert. Kein Optimierer, keine Simulation, kein Erzeuger gelaufen.

Einordnung: **vorhanden** · **teilweise** (was fehlt) · **fehlt** · **nicht prüfbar ohne Lauf**.
Fundstellen als Datei und Bezeichner (38.2), Commit = letzter Commit der Datei.

## 1. Listen-Erzeuger — `research/tb24_haltedauern/positionen_holen.py` (`46e3ed0`)

| AN | Bestand | Einordnung |
|---|---|---|
| AN-01, AN-02 | Erzeuger existiert (`positionen_holen.py::main`, über `alle_bots.py` `46e3ed0`); Kursdaten über `equity_simulation.load_all_symbol_data` → `strategy_paths` (Resolver), Parameter aus `live_params.py` der Bots. ⚠️ Nach TB-98 Befund 2 bricht der Lauf 9/9 an der Kennzeichnungsprobe ab („Kennzeichnung hat die Simulation verändert“), mit und ohne Modus. Heute nicht neu gelaufen. | **teilweise** — Lauf kommt nicht bis zum Schreiben; heutiger Stand **nicht prüfbar ohne Lauf** |
| AN-03, AN-04 | `--ziel` Pflicht ohne Voreinstellung (`_aufruf`), Zielordner muss bestehen (sonst 2), `sperre_vor_der_rechnung()` (1), `_schreibe_einmal()` mit `O_CREAT\|O_EXCL` (1) | **vorhanden** |
| AN-05 | `_schreibe_herkunft()`: `code_commit`, `selektionsmodus` = `paths.startpruefung()` (enthält `snapshot_hash`, `commit`, `arbeitsbaum`, `lock_sha256` u. a., `paths.AUDIT_SCHLUESSEL`), `dateien_sha256` je Datei | **vorhanden** (die Tatsachennotiz selbst ist Registerarbeit) |
| AN-06 | Keine Hashes von `live_params.py`/`backtest_*.py` in der Herkunftsnotiz; nur der Commit | **teilweise** — Parameterdateien-Hashes fehlen |
| AN-07 | `alle_trades` = alle Zeilen aus `bot_lauf.hole_trades()` → `collect_all_trades()` (Signalpfad). Zusätzlich zwei Läufe `simuliere()` (Zuteilung) für `ausgefuehrt` und `positionen.csv` | **teilweise** — Signalpfad da, Zuteilungspfad noch eingebaut |
| AN-08 | Spalten `trade_zeile, symbol, entry_time, exit_time, result, pnl_pct, entry_price, exit_price, kerzen, ausgefuehrt`; **kein `bot`** | **teilweise** |
| AN-09, AN-12 | Spalte `ausgefuehrt` wird geschrieben; Lauf 2 schreibt `symbol#zeile` in das Feld `symbol`, das seit TB-26 der Zufallsschlüssel der Zuteilung liest (A8) | **fehlt** — der Code tut das Gegenteil |
| AN-10 | Keine registrierte Feldliste (Register: 0 Treffer; Code: `ausgabespalten` als Literal) | **fehlt** |
| AN-11 | `exit_time` vorhanden; `haltedauer_balken` fehlt — `kerzen_je_trade()` liefert `kerzen` (Kerzen inkl. beider Enden), Zählregel nicht registriert (O-10) | **teilweise** |
| AN-13 | Zweimaliger Modus-Lauf bytegleich | **nicht prüfbar ohne Lauf** |
| AN-14 | `faltenplan.py::gefundene_trades_je_jahr` zählt alle Zeilen der Liste (gefundene); Deckel `t3_supertrend` steht noch aus `t3_supertrend_positionen.csv` (ausgeführte, 15.4/41.3 C2) | **teilweise** |
| AN-15 | Bei `elliott_wave` ist `hat_limit` False (`bot_lauf._KEIN_LIMIT_PARAMETER`); `alle_trades` wird vor der Simulation gebildet, zählt also gefundene | **vorhanden** (Logik); Tatsachennotiz Registerarbeit |
| AN-16 | Neun heutige Listen hash-gleich mit `docs/belege/TB-114/b3_register.txt` (9/9 GLEICH, letzter Commit je `78e2bc6`, `c1_listen_hashes.txt`) | **vorhanden** |
| AN-17 | Abbild `sperrliste_abbild_2026-09-26_tb117.json`: 14 Punkte, keiner nennt die Listen | **fehlt** (Register, nach O-11) |
| AN-18 | `faltenplan.py::TB24_DATEN` (`abeca36`) ist eine Konstante, zeigt auf den alten Ordner `research/tb24_haltedauern/daten`; zweite Konstante gleichen Namens in `faltenplan_neun.py` (`f5fdb53`) | **teilweise** — Konstante da, neuer Pfad nicht registriert |
| AN-19 | `herkunft.py::EINGEFROREN` (`ff2f254`) führt die neun alten Listen | **teilweise** — Wechsel steht mit der Neuerzeugung aus |
| AN-20, AN-21, AN-22 | Folgeschritte; hängen an neuen Listen | **fehlt** |

## 2. Beide Erzeuger — Weg und Nachweis

| AN | Bestand | Einordnung |
|---|---|---|
| AN-23 | `shared/paths.py` (`9d711dc`): `SystemExit(2)` bei fehlender Eingabe unter dem Modus, vier Rückfälle geschlossen (TB-105–107). `shared/ladeprotokoll.py` (`55b991d`) nennt Zeilenzahl und Quelle der Universumsdatei nicht (41.1 A10, Stand) | **teilweise** — für neuen Erzeuger-Code neu einzuhalten |
| AN-24, AN-25 | Neun `equity_simulation.py` und neun `multi_symbol_optimise.py` über `strategy_paths.get_strategy_paths` (Resolver); `bot_lauf.py` (`d48a195`) importiert `paths` | **vorhanden** |
| AN-26 | Leseprotokoll nur als Messwerkzeug ausserhalb des Laufcodes: `docs/belege/TB-92/a1b_lesehaken.py`, `docs/belege/TB-104/haken/sitecustomize.py` | **teilweise** — kein Leseprotokoll im Laufcode |
| AN-27 | `paths.startpruefung()`, `paths.audit_zeilen()` (acht Zeilen, `AUDIT_SCHLUESSEL`) | **teilweise** — Startprüfung da, Lese-Audit, in das sie gehören, fehlt |
| AN-28 | Bedingung 1 der Startprüfung trifft den Wegwerfbaum (`shared/test_startpruefungen.py`) | **vorhanden** |

## 3. Zellen-Erzeuger

**C2 — gibt es einen Ansatz?** Nein. `zellen.csv` und `tagesreihen` stehen in genau vier `.py`-Dateien:
`auswertung.py` (liest), `beispieldaten.py` (schreibt erfundene Werte), `test_vorregistrierung.py`,
`test_ersatzwerte.py` (`c2_suche.txt`). `herkunft.json` schreibt ausserdem nur `positionen_holen.py` (eigene
Notiz `<bot>_herkunft.json`). Das Feld `teile` liefert `herkunft.py::register()` (Z. 207) und liest nur
`test_ersatzwerte.py`. Lese-Audit: nur `paths.audit_zeilen()` und Kommentare dazu.

**Gestalt aus `beispieldaten.py::erzeuge`** (`ae8db0b`) — vollständig für den Vertrag, soweit er reicht:
`zellen.csv` mit `zelle_id`, je Achse eine Spalte (`aw._wert_text`, Achsen alphabetisch), `falte`, `rolle`,
`n_trades`, `netto_sharpe` (roh, auch bei 0 Trades), `netto_rendite_pct`, `kapital_drawdown_pct`,
`mittlere_exposure`; Zellen über `aw.alle_zellen(achsen, aw.bedingung_fuer(bot))`, Namen über `aw.zelle_id`;
je Zelle × Falte eine Zeile. `tagesreihen/<aw._dateiname(zid)>.csv` mit `datum, netto_rendite, exposure`.
`benchmark_tagesreihen/<markt>.csv` mit `datum, netto_rendite`. `herkunft.json` mit `commit, datenstand, register`
(Nullwerte, Hinweis). ⇒ Gegen diese Gestalt lässt sich bauen. **Nicht vorgegeben**: `teile` (AN-36), Lese-Audit
(AN-39), eine Trade-Liste je Zelle (O-2), mediane Haltedauer (O-4), ereignisindizierter Drawdown (O-5), Werte nach
22.2 und 16.7 (d) (O-3, O-7).

**C3 — Rechenkern heute** (`c_messung.txt`):

- `evaluate_combination_multi` (neun `multi_symbol_optimise.py`): ruft **keine** Simulation, rechnet Kennzahlen auf
  der aneinandergehängten Trade-Liste über die ganze Historie (Summen von `pnl_pct`), gibt eine Zeile ohne Trades
  zurück und **verwirft Zellen** (`return None` 3- bis 4-mal je Bot: `MIN_TRADES`, `MIN_SYMBOLS_CONTRIBUTING`,
  `MIN_AVG_RETURN_PCT`, keine Trades). Kein Kapital-Drawdown (`max_drawdown_kapital_pct` 0 Treffer in allen neun),
  keine Tagesreihe, keine Faltenaufteilung. Die Optimierer laufen über eigene `*_RANGE`-Listen, nicht über das
  registrierte Raster (`registerdaten.raster()`).
- `equity_simulation.py` (neun, `53896e4`): `collect_all_trades` (Signalpfad) nimmt je Bot Achsenwerte als
  Argumente, `simulate_portfolio` → `shared/zuteilung.py::simuliere_portfolio` (`f6d9a28`, Sperrlistenpunkt 10).
- `simuliere_portfolio` liefert `final_capital, num_executed, num_skipped, equity_curve, zuteilung`;
  `equity_curve` hat je **Ausstieg** eine Zeile `time, symbol, pnl_pct, allocation, capital_after`. Die Liste der
  ausgeführten Positionen gibt es nicht heraus (Grund für die Kennzeichnung in TB-24).
- Bausteine ausserhalb des Laufbereichs: `research/mtm_drawdown/mtm_kern.py` (`5e9ef2b`, TB-73):
  `ereignisreihenfolge`, `tagesraster`, `kurse_auf_raster`, `mtm_pfad`, `drawdown_falte`, `messe_falten` —
  tägliche MtM-Bewertung je Falte aus **ausgeführten Positionen**; `research/exposure_messung/exposure_kern.py`
  (`cb40c07`) `taegliche_reihen`. Im Laufbereich: `kennzahlen.py::sharpe` (0 bei Streuung 0), `max_drawdown_pct`;
  `benchmark.py::bh_tagesrenditen`; `shared/messkette.py::max_drawdown_ungerundet`.

Je Bot (Registerachsen aus `registerdaten.raster_definition()`; Kern = `collect_all_trades` + `simulate_portfolio`):

| Bot | Achsen im Register | nimmt der Kern jede Achse? | Kapital-DD (11.2) | Tagesreihe MtM (15.3, 24) | Trades mit Ein-/Ausstieg und `haltedauer_balken` |
|---|---|---|---|---|---|
| `elliott_wave` | deviation, stop, take_profit (keine Limitachse, `_ausnahme`) | ja (Stop/TP über Modulglobale `backtest_elliott.STOP_LOSS_PCT`/`TAKE_PROFIT_FIB`) | fehlt | fehlt | teilweise — `entry_time`, `exit_time` ja, Balkenzahl nein |
| `t3_supertrend` | t3_fast, t3_slow, adx, stop, limit (+ Bedingung) | ja | fehlt | fehlt | teilweise, dito |
| `rsi2_crypto` | rsi, sma_trend_filter, stop, limit | ja | fehlt | fehlt | teilweise (`holding_days` in Kalendertagen) |
| `turtle_soup_crypto` | donchian, stop_mode, limit | ja | fehlt | fehlt | teilweise (`holding_days`) |
| `volatility_breakout_crypto` | bb_squeeze_percentile, bb_lookback, stop, limit | **nein** — Squeeze-Achsen nur in `compute_indicators`; `get_trades_for_symbol` ruft es ohne diese Argumente (Posten 3) | fehlt | fehlt | teilweise (`holding_days`) |
| `elliott_wave_stocks` | deviation, stop, take_profit, limit | ja | fehlt | fehlt | teilweise |
| `rsi2_mean_reversion` | rsi, sma_trend_filter, stop, limit | **nein** — `SMA_TREND_PERIOD = 200` Konstante in `backtest_rsi2.py`, `compute_indicators(price_df)` ohne Argument (Posten 3) | fehlt | fehlt | teilweise (`holding_days`) |
| `turtle_soup_stocks` | donchian, stop_mode, limit | ja | fehlt | fehlt | teilweise |
| `volatility_breakout` | bb_squeeze_percentile, bb_lookback, stop, limit | **nein** — `load_all_symbol_data` ruft `compute_indicators(df)` beim Laden ohne Squeeze-Argumente (Posten 3) | fehlt | fehlt | teilweise (`holding_days`) |

„Tagesreihe MtM fehlt“ heisst: im Laufcode. `mtm_kern.mtm_pfad` kann sie bilden, braucht aber die ausgeführten
Positionen, die `simuliere_portfolio` nicht herausgibt — die Stelle liegt in `shared/zuteilung.py` (Punkt 10).

| AN | Bestand | Einordnung |
|---|---|---|
| AN-30 | kein Schreiber | **fehlt** |
| AN-31–AN-34 | kein Schreiber; der heutige Kern verwirft Zellen (`return None`) statt eine Nullzeile zu liefern | **fehlt** |
| AN-35 | `herkunft.datenstand(daten_dir)` und `herkunft.register()` vorhanden (`ff2f254`) | **teilweise** — Funktionen da, Schreiber fehlt |
| AN-36 | `register()` liefert `teile` | **teilweise** — Schreiber fehlt |
| AN-37 | Prüfer `auswertung.py::herkunft_pruefen` (`852f253`) | **vorhanden** (Prüferseite) |
| AN-38 | `herkunft.py` nicht in der Laufbereichsmessung (81 Module, `docs/belege/TB-112/a2_laufbereich.txt`), nicht in `ARBEITSBAUM_PFADE` (T117-5) | **fehlt** |
| AN-39, AN-40 | nur die acht Startzeilen; kein Audit mit Inhalts-Hash, kein Manifest-Abgleich, kein Snapshot-Hash nach dem Lauf | **fehlt** |
| AN-41 | kein Durchlauf über das registrierte Raster × Falten | **fehlt** |
| AN-42 | `auswertung.alle_zellen`, `zelle_id`, `bedingung_fuer`, `registerdaten.raster`, `faltenplan.faltenplan` | **vorhanden** (Bausteine) |
| AN-43 | `mtm_kern.mtm_pfad` (Research) | **teilweise** — ausserhalb des Laufbereichs, Eingabe fehlt (ausgeführte Positionen) |
| AN-44 | `kennzahlen.sharpe(renditen, perioden_je_jahr)` (0 bei Streuung 0) | **vorhanden** (Baustein) |
| AN-45, AN-46 | `mtm_kern.messe_falten` (Research); Zählung nach Einstiegstag nicht im Laufcode | **teilweise** |
| AN-47 | `mtm_kern.drawdown_falte` (Research); in `evaluate_combination_multi` 0/9 | **teilweise** |
| AN-48 | `mtm_kern.ereigniskurve` + `messkette.max_drawdown_ungerundet` | **teilweise** — Ort offen (O-5) |
| AN-49 | kein Code setzt den Kapitalpfad auf den 1. Januar der ersten Falte | **fehlt** |
| AN-50 | Wache 0/9 (`c_messung.txt`, wie TB-82 M4) | **fehlt** (9/9) |
| AN-51 | Aktien-Bots: `entry_cutoff` je Symbol ab dem letzten Kurs der Datei (`elliott_wave_stocks` kappt die Reihe, Z. 93–94); Wert `faltenplan.HORIZONTBEGINN` (`aktien` 2016-09-19) existiert, wird von den Bots nicht gelesen. Krypto: kein Horizont (26.2) | **fehlt** (4/4 Aktien); Krypto **nicht betroffen** |
| AN-52 | `rsi2_mean_reversion` **fehlt**; `volatility_breakout`, `volatility_breakout_crypto` **teilweise** (Backtest nimmt die Argumente, Optimierer und Simulation reichen nicht durch) | siehe links |
| AN-53 | `regimewache.pruefe_einbau()`: vollständig, 3/3 eingebaut | **vorhanden** |
| AN-54, AN-55 | Loader der Bots (`MIN_HISTORY_*`), Lesart A in `faltenplan_neun.py`; ob der Lauf je Falte richtig zählt | **nicht prüfbar ohne Lauf** |
| AN-56 | `shared/ladeprotokoll.py::Ladeprotokoll` (Laden); Kohärenz 0 Treffer | **teilweise** (Ort offen, O-7) |
| AN-57 | nichts | **fehlt** (Ort offen, O-6) |
| AN-58 | nichts | **fehlt** (Ort offen, O-3) |
| AN-59 | nichts | **fehlt** (Ort offen, O-4) |
| AN-60 | `shared/handelskosten.py` (`04d6ce6`): `TRADING_FEE_PCT = 0.1`, `SLIPPAGE_PCT = 0.05`; `zuteilung.SEED = 20260913` | **vorhanden** |
| AN-61 | siehe C5 | **fehlt** |
| AN-62 | nur `beispieldaten._benchmark` (erfunden); Baustein `benchmark.py::bh_tagesrenditen` (Punkt 6) | **teilweise** — Schreiber fehlt (O-8) |

## 4. C4 — TB-30b Posten 3–5 je Bot

| Bot | Posten 3 (Durchreichung) | Posten 4 (`entry_cutoff`, 26.1) | Posten 5 (Wache 29.4) |
|---|---|---|---|
| `elliott_wave` | — | nicht betroffen (kein Horizont) | fehlt |
| `t3_supertrend` | — | nicht betroffen | fehlt |
| `rsi2_crypto` | — (Achse wird schon durchgereicht) | nicht betroffen | fehlt |
| `turtle_soup_crypto` | — | nicht betroffen | fehlt |
| `volatility_breakout_crypto` | teilweise | nicht betroffen | fehlt |
| `elliott_wave_stocks` | — | fehlt | fehlt |
| `rsi2_mean_reversion` | fehlt | fehlt | fehlt |
| `turtle_soup_stocks` | — | fehlt | fehlt |
| `volatility_breakout` | teilweise | fehlt | fehlt |

## 5. C5 — Posten 8, Walk-Forward im Modus

Keine Wache. Die neun `multi_symbol_walk_forward.py` enthalten `selektionsmodus` 0-mal; `shared/paths.py` und
`shared/strategy_paths.py` nennen `walk_forward` 0-mal. Die Walk-Forward-Skripte importieren
`multi_symbol_optimise` und damit den Resolver — im Modus liefen sie also auf dem Snapshot durch. **fehlt.**

## 6. C6 — Laufbereich (44-8), gelesen, nicht neu gemessen

`docs/belege/TB-112/a2_laufbereich.txt`: 81 Module ohne Messumschläge. Ein Zellen-Erzeuger, der auf dem heutigen
Bestand aufsetzt, würde nach C3 importieren:

- **schon im Laufbereich:** die neun `equity_simulation.py`, `multi_symbol_optimise.py`, `backtest_*.py`,
  `live_params.py`, `indicators.py` (bzw. `elliott_wave_counter.py`, `zigzag_indicator.py`, `regime_filter.py`),
  `stocks_symbols_config.py`; `shared/zuteilung.py`, `messkette.py`, `handelskosten.py`, `paths.py`,
  `strategy_paths.py`, `regimewache.py`, `kursdaten.py`, `ladeprotokoll.py`, `symbols_config.py`;
  `research/vorregistrierung/registerdaten.py`, `faltenplan.py`, `kennzahlen.py`, `benchmark.py`, `auswertung.py`;
  `research/exposure_messung/bot_lauf.py`.
- **neu in den Laufbereich (R4/R5 (a)):** das Erzeuger-Modul selbst, `research/vorregistrierung/herkunft.py`
  (R5 (a), T117-5) und — falls übernommen statt nachgebaut — `research/mtm_drawdown/mtm_kern.py`.
  `research/tb24_haltedauern/positionen_holen.py` läuft vor dem Tag einmal und gehört nicht zum Lauf am Tag.
