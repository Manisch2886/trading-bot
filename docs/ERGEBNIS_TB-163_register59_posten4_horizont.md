# ERGEBNIS TB-163 — Register 59 (Tatsachennotiz TB-162) und E-6: Horizont je Bot aus `faltenplan.HORIZONTBEGINN` (TB-30b Posten 4)

**Auftrag:** `docs/auftraege/MAC_TB-163_register59_posten4_horizont.md` · **Sitzung:** Mac, Claude Code (Opus 5.5), 15.10.2026 · **Zweig:** `main`, Ausgang `8517c5f`
**Commits:** ⟨S0⟩ `cff0de3` (Schritt 0) · ⟨N⟩ `35dae90` (Register 59) · ⟨K⟩ `639044c` (Registerkopie, Index) · ⟨E⟩ `11a267f` (E-6) · ⟨F⟩ = der Abgabe-Commit „TB-163 Abgabe: Ergebnis, BACKLOG, Journal EZ“, der diese Datei enthält; danach „TB-163 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-163/` · **Journal:** EZ

## Kurz

Alle Schritte 0, V, N, K, E, A ohne Abbruch, jede Belegdatei endet mit `rc 0`. Register 59 steht append-only am Ende (numstat 41/0). In den vier Aktien-Optimierern kommt das Fenster jetzt aus `faltenplan.horizontbeginn(<bot>)` (19.09.2016) statt aus `df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)`; die synthetische Probe besteht 34 von 34 unter Python 3.9.6 (trading-env), Laufzeit rund 5 s; R81 (d) ist erfüllt. Kein Optimierer, kein Walk-Forward-Rechner, keine equity_simulation lief; `data/` wurde nicht gelesen. Der Hash-Übergang nach 37.3 steht unten als Entwurf, nicht im Register.

## Voraussetzungen (`docs/belege/TB-163/v_voraussetzung.txt`, wörtlich)

```
ja    Sperrliste herkunft.py Z. 102-106 nennt strategies/*/multi_symbol_optimise.py (Punkt 11, 37.3)
ja    sha256 vorher research/vorregistrierung/faltenplan.py = 63dafeb44e027cb5…
ja    sha256 vorher strategies/elliott_wave_stocks/multi_symbol_optimise.py = 275273776fafb245…
ja    sha256 vorher strategies/rsi2_mean_reversion/multi_symbol_optimise.py = 777f5cb0a637bb87…
ja    sha256 vorher strategies/turtle_soup_stocks/multi_symbol_optimise.py = e4277f013be6d0af…
ja    sha256 vorher strategies/volatility_breakout/backtest_breakout.py = 3fd0cef6c284a880…
ja    sha256 vorher strategies/volatility_breakout/multi_symbol_optimise.py = f0a4ee43dca133e8…
ja    faltenplan.py: HORIZONTBEGINN-Literal genau einmal (aktien 2016-09-19)
ja    Register: 58 genau einmal, 59 noch nicht
ja    Register: Voraussetzung R81 (d) genau einmal (Z. [11775])
ja    Register endet mit genau einer Leerzeile
ja    ERGEBNIS_TB-162 md5 210508624458a7287f89888a65304394
ja    ERGEBNIS_TB-162: Notiz Z. 199-232 (Z. 197 Kopf, Z. 233 leer, Z. 234 Abweichungen)
ja    ERGEBNIS_TB-162 zuletzt in Commit 16db5e3
ja    E-6 Anker in strategies/elliott_wave_stocks/multi_symbol_optimise.py genau einmal (Datenuhr-Zeile, def load_all_symbol_data() -> dict:), horizontbeginn_ts noch nicht da
ja    E-6 Anker in strategies/rsi2_mean_reversion/multi_symbol_optimise.py genau einmal (Datenuhr-Zeile, def load_all_symbol_data() -> dict:), horizontbeginn_ts noch nicht da
ja    E-6 Anker in strategies/turtle_soup_stocks/multi_symbol_optimise.py genau einmal (Datenuhr-Zeile, def load_all_symbol_data() -> dict:), horizontbeginn_ts noch nicht da
ja    E-6 Anker in strategies/volatility_breakout/multi_symbol_optimise.py genau einmal (Datenuhr-Zeile, def load_all_symbol_data() -> dict:), horizontbeginn_ts noch nicht da
Pruefungen: 18, NEIN: 0
rc 0
```

## Register 59

- Überschrift `## 59. Tatsachennotiz TB-162 — Kapital-Drawdown E und M je Abschnitt des bot-eigenen Walk-Forward (TB-163)` in **Z. 12112** von `docs/VORREGISTRIERUNG_neuselektion.md`, `### 59.1` in Z. 12116; Notiz zeichengleich aus `docs/ERGEBNIS_TB-162_wf_kapital_dd.md` Z. 199–232 (Werkzeug: „Notiz zeichengleich im Register“).
- `git diff --numstat cff0de3 35dae90 -- docs/VORREGISTRIERUNG_neuselektion.md`: `41	0` — append-only.
- K: `registerkopie.py` legt 59 in `REGISTER_KOPIE_teil6.md` (Abschnitte 58–59, 23 496 B); keine weitere Teildatei; Teile, Abschnittskopien (60 Dateien, 0–59) und `--pruefen` je BYTEGLEICH gegen das Register am `35dae90`. `c2_index_zeilen.py cff0de3 35dae90`: 448 Zeilenangaben, davon geändert 0. `WZ index`: Kopf 0–59, Zeile 59 (T6), Pflegezeile TB-163. `dialog_index.py --pruefen`: 61/61, rc 0.

## E-6: Horizont je Bot

Probe (`docs/belege/TB-163/e_test.txt`, wörtlich):

```
ja    elliott_wave_stocks: Quelltext: kein Fenster aus open_time.max() - DateOffset
ja    elliott_wave_stocks: horizontbeginn_ts() = faltenplan.horizontbeginn = 2016-09-19 · 2016-09-19 00:00:00
ja    elliott_wave_stocks: Wert kommt aus faltenplan.HORIZONTBEGINN (Modul research/vorregistrierung)
ja    elliott_wave_stocks: [naiv] alle drei synthetischen Symbole geladen · ['AAA', 'BBB', 'CCC']
ja    elliott_wave_stocks: [naiv] Anfang der geladenen Zeilen = Horizontbeginn, gleich fuer drei Dateienden · {'AAA': '2016-09-19 00:00:00', 'BBB': '2016-09-19 00:00:00', 'CCC': '2016-09-19 00:00:00'}
ja    elliott_wave_stocks: [naiv] laengere Datei (CCC) beginnt zeilengleich wie AAA
ja    elliott_wave_stocks: [tz UTC] alle drei synthetischen Symbole geladen · ['AAA', 'BBB', 'CCC']
ja    elliott_wave_stocks: [tz UTC] Anfang der geladenen Zeilen = Horizontbeginn, gleich fuer drei Dateienden · {'AAA': '2016-09-19 00:00:00+00:00', 'BBB': '2016-09-19 00:00:00+00:00', 'CCC': '2016-09-19 00:00:00+00:00'}
ja    elliott_wave_stocks: [tz UTC] laengere Datei (CCC) beginnt zeilengleich wie AAA
ja    rsi2_mean_reversion: Quelltext: kein Fenster aus open_time.max() - DateOffset
ja    rsi2_mean_reversion: horizontbeginn_ts() = faltenplan.horizontbeginn = 2016-09-19 · 2016-09-19 00:00:00
ja    rsi2_mean_reversion: Wert kommt aus faltenplan.HORIZONTBEGINN (Modul research/vorregistrierung)
ja    rsi2_mean_reversion: [naiv] alle drei synthetischen Symbole geladen · ['AAA', 'BBB', 'CCC']
ja    rsi2_mean_reversion: [naiv] Fenster (entry_cutoff) = Horizontbeginn in der Spaltenzone, gleich fuer drei Dateienden · {'AAA': '2016-09-19 00:00:00', 'BBB': '2016-09-19 00:00:00', 'CCC': '2016-09-19 00:00:00'}
ja    rsi2_mean_reversion: [tz UTC] alle drei synthetischen Symbole geladen · ['AAA', 'BBB', 'CCC']
ja    rsi2_mean_reversion: [tz UTC] Fenster (entry_cutoff) = Horizontbeginn in der Spaltenzone, gleich fuer drei Dateienden · {'AAA': '2016-09-19 00:00:00+00:00', 'BBB': '2016-09-19 00:00:00+00:00', 'CCC': '2016-09-19 00:00:00+00:00'}
ja    turtle_soup_stocks: Quelltext: kein Fenster aus open_time.max() - DateOffset
ja    turtle_soup_stocks: horizontbeginn_ts() = faltenplan.horizontbeginn = 2016-09-19 · 2016-09-19 00:00:00
ja    turtle_soup_stocks: Wert kommt aus faltenplan.HORIZONTBEGINN (Modul research/vorregistrierung)
ja    turtle_soup_stocks: [naiv] alle drei synthetischen Symbole geladen · ['AAA', 'BBB', 'CCC']
ja    turtle_soup_stocks: [naiv] Fenster (entry_cutoff) = Horizontbeginn in der Spaltenzone, gleich fuer drei Dateienden · {'AAA': '2016-09-19 00:00:00', 'BBB': '2016-09-19 00:00:00', 'CCC': '2016-09-19 00:00:00'}
ja    turtle_soup_stocks: [tz UTC] alle drei synthetischen Symbole geladen · ['AAA', 'BBB', 'CCC']
ja    turtle_soup_stocks: [tz UTC] Fenster (entry_cutoff) = Horizontbeginn in der Spaltenzone, gleich fuer drei Dateienden · {'AAA': '2016-09-19 00:00:00+00:00', 'BBB': '2016-09-19 00:00:00+00:00', 'CCC': '2016-09-19 00:00:00+00:00'}
ja    volatility_breakout: Quelltext: kein Fenster aus open_time.max() - DateOffset
ja    volatility_breakout: horizontbeginn_ts() = faltenplan.horizontbeginn = 2016-09-19 · 2016-09-19 00:00:00
ja    volatility_breakout: Wert kommt aus faltenplan.HORIZONTBEGINN (Modul research/vorregistrierung)
ja    volatility_breakout: [naiv] alle drei synthetischen Symbole geladen · ['AAA', 'BBB', 'CCC']
ja    volatility_breakout: [naiv] Fenster (entry_cutoff) = Horizontbeginn in der Spaltenzone, gleich fuer drei Dateienden · {'AAA': '2016-09-19 00:00:00', 'BBB': '2016-09-19 00:00:00', 'CCC': '2016-09-19 00:00:00'}
ja    volatility_breakout: [naiv] Scanbeginn (Zeilen vor entry_cutoff) gleich fuer drei Dateienden · {'AAA': 2273, 'BBB': 2273, 'CCC': 2273}
ja    volatility_breakout: [naiv] kein Einstieg vor dem Horizontbeginn · 29
ja    volatility_breakout: [naiv] Trades bis 60 Tage vor dem Ende von AAA gleich bei laengerer Datei · 29
ja    volatility_breakout: [tz UTC] alle drei synthetischen Symbole geladen · ['AAA', 'BBB', 'CCC']
ja    volatility_breakout: [tz UTC] Fenster (entry_cutoff) = Horizontbeginn in der Spaltenzone, gleich fuer drei Dateienden · {'AAA': '2016-09-19 00:00:00+00:00', 'BBB': '2016-09-19 00:00:00+00:00', 'CCC': '2016-09-19 00:00:00+00:00'}
ja    volatility_breakout: [tz UTC] Scanbeginn (Zeilen vor entry_cutoff) gleich fuer drei Dateienden · {'AAA': 2273, 'BBB': 2273, 'CCC': 2273}
INFO  volatility_breakout: [tz UTC] run_backtest: Cannot compare tz-naive and tz-aware timestamps - Befund ausserhalb E-6, nicht gezaehlt
34 von 34 Pruefungen bestanden
rc 0
```

R81 (d) (`docs/belege/TB-163/e_r81d.txt`, wörtlich):

```
ja    Testbeleg docs/belege/TB-163/e_test.txt: alle bestanden, rc 0 (34 von 34 Pruefungen bestanden)
ja    elliott_wave_stocks: kein Fenster aus dem Dateiende (open_time.max() - DateOffset)
ja    elliott_wave_stocks: Fenster aus faltenplan.horizontbeginn("elliott_wave_stocks")
ja    rsi2_mean_reversion: kein Fenster aus dem Dateiende (open_time.max() - DateOffset)
ja    rsi2_mean_reversion: Fenster aus faltenplan.horizontbeginn("rsi2_mean_reversion")
ja    turtle_soup_stocks: kein Fenster aus dem Dateiende (open_time.max() - DateOffset)
ja    turtle_soup_stocks: Fenster aus faltenplan.horizontbeginn("turtle_soup_stocks")
ja    volatility_breakout: kein Fenster aus dem Dateiende (open_time.max() - DateOffset)
ja    volatility_breakout: Fenster aus faltenplan.horizontbeginn("volatility_breakout")
ja    elliott_wave_stocks: Anfang der geladenen Zeilen = Horizontbeginn (Kappung an cutoff)
ja    volatility_breakout: Scanbeginn folgt entry_cutoff (backtest_breakout.py unverändert)
ja    faltenplan.py unverändert
R81 (d) Voraussetzung: erfuellt (Fenster, Scanbeginn, Anfang der geladenen Zeilen ohne Dateiende)
INFO Befund (kein Teil von R81 (d)): die Aufnahme eines Symbols (timespan_days = max - min gegen MIN_HISTORY_DAYS) haengt weiter vom Dateiende ab; buy_and_hold_benchmark.py der drei Bots rsi2, turtle, vb bildet cutoff weiter aus .max() (nicht E-6)
Pruefungen: 14, NEIN: 0
rc 0
```

`WZ e6 --probe` und `WZ e6` je `rc 0`; sha256 nachher der vier Dateien gleich dem Soll `NACH` aus dem Bau (`e_e6.txt`). Je Datei: eine Hilfsfunktion `horizontbeginn_ts(spalte=None)` vor `load_all_symbol_data()` (Import von `faltenplan` erst beim Aufruf) und die Datenuhr-Zeile ersetzt durch `… = horizontbeginn_ts(df["open_time"])`; 20 Zeilen dazu, 1 weg je Datei.

### Entwurf Tatsachennotiz Hash-Übergang nach 37.3 (`docs/belege/TB-163/e_uebergang.md`, wörtlich)

Freigabe: dritte Karte des Betreibers, 15.10.2026, 18:24: „Einzelfreigabe nach 37.3 für E-6 (Posten 4, Horizont je Bot, vier Aktien-Optimierer), Auftrag mit R81 (d) und Tatsachennotiz TB-162 als Abschnitt 59 (Ja, Recommended).“

**Hash-Übergänge nach 37.3** (Sperrlistenpunkt 11, „Commit-Hashes von Simulation, Erkennung, Optimierern“) — Entwurf, nicht eingetragen; volle Hashes (39.5):

| Datei | vorher | nachher | Commit | vollzieht |
|---|---|---|---|---|
| `strategies/elliott_wave_stocks/multi_symbol_optimise.py` | `275273776fafb2453cdb41f634b86bacffd5994f8b5508ef034400cd7c5ede9d` | `3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232` | `11a267f` | E-6 (Posten 4; R44, R81 (d)) |
| `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` | `777f5cb0a637bb8770d1cd4a89aac03c6b29db98d13ce47eac6de29db279c661` | `61838aca901cabeace70511b71742d10cba4de6575a999aecf5a492f938ad6dc` | `11a267f` | E-6 (Posten 4; R44, R81 (d)) |
| `strategies/turtle_soup_stocks/multi_symbol_optimise.py` | `e4277f013be6d0af85647f5d32d8cdb60ef086d06c6e041853c6da571c96ddd4` | `29e7f10c3eb79f8316c53c9a31ee3ea0dd450d44bb9904dc2ba9944df003c0cc` | `11a267f` | E-6 (Posten 4; R44, R81 (d)) |
| `strategies/volatility_breakout/multi_symbol_optimise.py` | `f0a4ee43dca133e89272e48d80280d8a22f57d751d2ddac06751fd091198af2d` | `24c182ae1cf7c882c9e3aec31c5088348e2fa44c5cc2e99eab54ecf29b337585` | `11a267f` | E-6 (Posten 4; R44, R81 (d)) |

Neu (kein Vorher), Commit `11a267f`: `research/posten4_horizont/test_posten4_horizont.py` `ed13dd2cbbde0bed0e83f06f363da3f6c1c8d588d25f0fd71c73b4196039534c`.
Unverändert: `research/vorregistrierung/faltenplan.py` `63dafeb44e027cb5d93ac19cddfc7d4e98b468cece116512c2b3f1601bd4a4c7`, `strategies/volatility_breakout/backtest_breakout.py` `3fd0cef6c284a8806cace3663c241295edbb1ef8ee79092abfd0dc55e2bf6a76`.

**`herkunft.register()`** (ohne Lauf auf Kursdaten messbar: SHA-256 über Registerdatei und `EINGEFROREN`, liest `data/` nicht): **nachher** gemessen am `11a267f` = `cdc0ebeffda66e791212f602dd4c2bcc7018392339b25fc97149f10d1c6be23c`, 23 Teile, `fehlend` leer. **Vorher** nicht gesondert gemessen (kein Checkout eines älteren Stands); keiner der 23 Teile kommt in `git diff --name-only 639044c 11a267f` vor, also gilt derselbe Wert am `639044c` — E-6 bewegt `register()` nicht. Die vier Optimierer stehen nicht in `EINGEFROREN`, sondern in `SPERRLISTE_DATEIEN` und werden über den Git-Commit erfasst. Gegenüber `cff0de3` hat sich `register()` durch Abschnitt 59 (Registerdatei, Schritt N) geändert; dieser Wert vor N ist nicht gemessen.

## Offen

- **Der Hash-Übergang nach 37.3 bleibt offen** bis zum Registereintrag (Folgeauftrag, wie TB-122 → Register 50.3) und bis zum neuen Abbild unter neuem Namen (37.3); der Entwurf oben führt die vollen Hashes (39.5). Bis dahin meldet die Sperrlisten-Sonde zu Punkt 11 einen zulässigen Befund `1` (beauftragt, Freigabe dritte Karte).
- Die Neuerzeugung der Listen (E-4) ist nicht Teil dieses Auftrags; mit E-6 ist die Voraussetzung „vor der Neuerzeugung der Listen“ (R44, 55.8 Nr. 3) erledigt.

## Befunde (nicht E-6)

- **MIN_HISTORY_DAYS:** ob ein Symbol aufgenommen wird (`timespan_days` = max − min gegen `MIN_HISTORY_DAYS`), hängt weiter vom Dateiende ab.
- **`buy_and_hold_benchmark.py`** der drei Bots rsi2_mean_reversion, turtle_soup_stocks, volatility_breakout bildet seinen `cutoff` weiter aus `.max()`.
- **Import-Kette:** `import faltenplan` (in `horizontbeginn_ts`, erst beim Aufruf) zieht beim ersten Laden registerdaten, faltenplan_neun, erste_falte_trockenlauf und deren Importe (u. a. `notifications/manual_close.py`) in den Optimierer-Prozess (am Bau erschlossen; unter 3.9.6 lief die Probe damit ohne Fehler).
- **`backtest_breakout.py` Z. 211** (`entry_time >= np.datetime64(entry_cutoff)`) wirft mit tz-behaftetem `open_time` TypeError — am unveränderten Stand ebenso; heute sind alle Aktien-1d-Dateien naiv.
- **`INFO`-Zeilen aus `e_test.txt`:** genau eine — `volatility_breakout: [tz UTC] run_backtest: Cannot compare tz-naive and tz-aware timestamps - Befund ausserhalb E-6, nicht gezaehlt`. Folge: für volatility_breakout mit tz-behaftetem `open_time` sind die zwei Prüfungen „kein Einstieg vor dem Horizontbeginn“ und „Trades bis 60 Tage …“ nicht gelaufen (daher 34 statt 36).

## Abweichungen

- Keine Abbrüche, kein Abbruch in E; die vier Optimierer und `research/posten4_horizont/` sind in ⟨E⟩ committet.
- Den Testlauf habe ich mit vorangestelltem Shell-`time` ausgeführt, um die Laufzeit zu messen (rund 5,1 s real); die Ausgabe von `time` geht nicht in `e_test.txt` (geprüft: erste Zeile `ja …`, keine `real`-Zeile).
- Ausser den Befehlen des Auftrags liefen nur lesende Hilfsaufrufe: `git diff`/`git status`, eine Messung von `herkunft.register()` (liest Register und `EINGEFROREN`, schreibt nichts im Repo; Teileliste nach `$TMPDIR/tb163_register_teile.txt`).
- Das Journal-Werkzeug setzt EZ direkt hinter EY, ohne `---` dazwischen (wie EX hinter EW); das `---` vor „Wiederkehrende Lehren“ bleibt.

## In einfacher Sprache

Zwei Dinge sind erledigt. Erstens steht die Messung aus TB-162 jetzt wortgleich als Abschnitt 59 im Register, nur angehängt; die Kopien und das Inhaltsverzeichnis sind nachgezogen. Zweitens rechnen die vier Aktien-Bots ihr Zehnjahresfenster beim Optimieren nicht mehr vom letzten Kurstag der jeweiligen Datei aus, sondern alle vom selben Datum aus dem Register, dem 19.09.2016. Eine Datei, die ein paar Tage länger ist, verschiebt das Fenster also nicht mehr. Geprüft wurde das nur mit erfundenen Kursreihen; kein Optimierer lief, keine Parameter wurden gesucht. Die alten und neuen Prüfsummen der vier gesperrten Dateien stehen oben als Entwurf; ins Register kommen sie mit einem eigenen Auftrag.
