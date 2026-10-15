# REGISTER-KOPIE Abschnitt 59 (von 0–59) — Register-Z. 12112–12151 — Commit 35dae904145fe3ba4e18b2dfbb6c28e0e2239fb6 — 2026-10-15 — Original sha256 662b12455d65974be5543f247ff33d79716f256c705ff4c3f10473d426a09c65 — KOPIE, nicht das Register

## 59. Tatsachennotiz TB-162 — Kapital-Drawdown E und M je Abschnitt des bot-eigenen Walk-Forward (TB-163)

Reines Eintragen einer Tatsachennotiz, Bauart 24.6 (Betreiberkarte 15.10.2026, 18:17: „Tatsachennotiz TB-162 ins Register, als Schritt im nächsten Mac-Auftrag“; Entscheid F2 des steuernden Chats vom 15.10.2026, 18:25). Quelle ist allein `docs/ERGEBNIS_TB-162_wf_kapital_dd.md`, md5 `210508624458a7287f89888a65304394`, 28 482 B, Z. 199–232 (Abschnitt „Vorschlag Tatsachennotiz“), im Repo seit Commit `16db5e3`; zeichengleich übernommen. Eingetragen am 15.10.2026 mit TB-163 (Stand `cff0de3`). Nichts entfernt, kein bestehender Satz umgeschrieben; keine Marke (R96 (d) führt 24.x ohne Marke).

### 59.1 Tatsachennotiz (zeichengleich aus ERGEBNIS_TB-162 Z. 199–232)

> **Tatsachennotiz zu 24.2, 24.3, R36 und 11.2 mit R43 — Kapital-Drawdown E und M der heutigen Parameter je Abschnitt des bot-eigenen Walk-Forward (TB-162, 15.10.2026).**
> Datiert angehängt. Nichts entfernt, kein bestehender Satz umgeschrieben. Diese Notiz berichtet; sie bewertet nicht, empfiehlt nicht, wägt nicht ab, und keine Zahl hier steht neben einem Grenzwert. Die Zahl entscheidet nichts (24.3). Kein Raster, kein Score, kein IS-Sieger, keine Rangfolge, kein Vergleich gegen andere Parametersätze (R94 (a), (c)).
>
> **Herkunft:** `research/wf_kapital_dd/` (Forschungsmodul ausserhalb des Laufcodes), gemessen am 15.10.2026 auf dem Mac (`trading-env/bin/python3` 3.9.6) am Commit `4ec04df`, mit den Kursdateien in `data/`; Ergebnisdokument `docs/ERGEBNIS_TB-162_wf_kapital_dd.md`. Nichts in `strategies/`, `shared/`, `research/vorregistrierung/`, `research/mtm_drawdown/`, `research/tb24_haltedauern/`, `research/exposure_messung/`, `data/`, `config/` berührt; die 29 Sperrlisten-Hashes vorher = nachher.
>
> **Positionen: Rekonstruktion** (R97 (b); kein Nachweis, keine Probe, keine Definition, R95 (b) und (c)). Ein Lauf von `simulate_portfolio` je Bot mit unveränderten Trades (`trades.equals` vor/nach geprüft), Zuordnung aus Trade-Liste und `equity_curve` nach der Regel: Z1 gleiches Symbol, `exit_time` = `time` der Kurvenzeile (UTC), |Δ pnl_pct| ≤ 1e-9; Z2 bei mehreren Kandidaten Kapitalprobe |allocation − allocation_pct × Kapital beim Einstieg| ≤ 0,01; Z3 inhaltsgleiche Kandidaten: kleinste Zeile; Z4 sonst nicht zuordenbar. Nicht zuordenbare Positionen: **0 bei allen neun Bots**; alle Zuordnungen nach Z1 allein (Z2 0, Z3 0). Der Aufruf von simulate_portfolio ist argumentgleich mit dem __main__ des Bots (am Code geprüft); es gibt keinen zweiten Bot-Lauf zum Abgleich. `positionen_holen.py` wurde weder ausgeführt noch eingebunden (R97 (a)).
>
> | Bot | `final_capital` | `num_executed` | `num_skipped` |
> |---|---|---|---|
> | elliott_wave | 17071.34 | 227 | 0 |
> | elliott_wave_stocks | 51906.95 | 394 | 116 |
> | rsi2_crypto | 25086.91 | 663 | 54 |
> | rsi2_mean_reversion | 13628.4 | 4218 | 1173 |
> | t3_supertrend | 42574.3 | 1031 | 377 |
> | turtle_soup_crypto | 48660.84 | 1971 | 191 |
> | turtle_soup_stocks | 23814.54 | 8914 | 3155 |
> | volatility_breakout | 30958.92 | 1461 | 3049 |
> | volatility_breakout_crypto | 29724.7 | 342 | 31 |
>
> **Was gemessen wurde:** E (ereignisindiziert, je Ausstieg) und M (täglich Mark-to-Market) mit `research/mtm_drawdown/mtm_kern.py` auf dem **einen** durchgehenden Kapitalpfad je Bot (Startkapital 10 000, ohne Neustart, R36), ausgeschnitten in vier Abschnitte aus den Grenzen von `split_all_symbols` des Bots (`train_split_ratio` 0.7): gesamt; IS bis zur frühesten Symbolgrenze; gemischt zwischen frühester und spätester Symbolgrenze; OOS ab der spätesten Symbolgrenze.
>
> | Bot | gesamt E / M | IS E / M | gemischt E / M | OOS E / M |
> |---|---|---|---|---|
> | elliott_wave | −13.97 / −16.42 | −13.97 / −16.42 | −3.90 / −7.02 | −3.11 / −3.34 |
> | elliott_wave_stocks | −22.97 / −20.91 | −22.97 / −20.91 | −3.26 / −6.65 | −8.33 / −12.50 |
> | rsi2_crypto | −16.60 / −25.02 | −16.60 / −25.02 | −13.94 / −17.16 | −3.14 / −4.28 |
> | rsi2_mean_reversion | −19.53 / −22.38 | −19.53 / −22.38 | 0.00 / 0.00 | −5.05 / −7.27 |
> | t3_supertrend | −22.40 / −24.36 | −22.40 / −24.36 | −18.94 / −20.80 | −10.26 / −12.12 |
> | turtle_soup_crypto | −34.85 / −38.55 | −32.90 / −35.30 | −34.85 / −38.55 | −10.29 / −12.72 |
> | turtle_soup_stocks | −29.07 / −33.93 | −29.07 / −33.93 | −0.11 / 0.00 | −13.29 / −18.87 |
> | volatility_breakout | −22.46 / −23.94 | −22.46 / −23.94 | 0.00 / 0.00 | −12.97 / −16.86 |
> | volatility_breakout_crypto | −16.29 / −19.30 | −16.29 / −19.30 | −14.86 / −14.40 | −3.95 / −6.56 |
>
> Angaben in Prozent. **M flacher als E** in vier Abschnitten: elliott_wave_stocks gesamt und IS (+2,06 pp), turtle_soup_stocks gemischt (+0,11 pp), volatility_breakout_crypto gemischt (+0,46 pp). Die Spannweite der Symbolgrenzen beträgt bei rsi2_mean_reversion, turtle_soup_stocks und volatility_breakout 1,0 Tag (Abschnitt „gemischt“ mit 0, 17 und 0 Ausstiegen), bei elliott_wave_stocks 542 Tage, bei den fünf Krypto-Bots 724 bis 831 Tage.
