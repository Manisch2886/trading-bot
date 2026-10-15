# Ergebnis TB-162 — Kapital-Drawdown E und M je WF-Abschnitt (R94 (b)), Positionen als Rekonstruktion (R97 (b)); Register R94–R97 als Abschnitt 58

**Auftrag:** `docs/auftraege/MAC_TB-162_wf_kapital_dd.md` · **Sitzung:** Mac, Claude Code, Opus 5.5 · **Datum:** 15.10.2026 · **Interpreter:** `trading-env/bin/python3 -B` (3.9.6)
**Commits:** ⟨S0⟩ `9a1bc7a` · ⟨R⟩ `0e1e662` · ⟨K⟩ `4ec04df` · ⟨M⟩ `ac3e9f2` · ⟨F⟩ = der Commit „TB-162 Abgabe: Ergebnis, Journal EX“ (enthält dieses Dokument und kann seinen eigenen Hash nicht nennen); danach „TB-162 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-162/` · **Journal:** Block `EX`.

## Kurz

Alle Schritte 0 ⇒ V ⇒ R ⇒ K ⇒ M ⇒ E liefen wie im Auftrag, jeder mit `rc 0`; kein Abbruch, kein Aufruf abgelehnt, keine Bestätigung verlangt. Die Voraussetzungen hielten (25/0), Abschnitt 58 mit R94–R97 und den 8 Marken steht im Register, Kopien, Index und Dialog-Index sind nachgezogen (neue Teildatei `REGISTER_KOPIE_teil6.md`, wie in der Simulation). Die Messung lief für alle neun Bots (9 von 9 rc 0, Sperrliste vorher = nachher), die rekonstruierten Positionen sind bei **allen neun Bots vollständig zugeordnet (0 nicht zuordenbar)**. Die Zahlen sind ein Bericht und entscheiden nichts (24.3); sie stehen unten als **Vorschlag einer Tatsachennotiz**, nicht im Register (F3).

## Voraussetzungen

`docs/belege/TB-162/v_voraussetzung.txt`, wörtlich:

```
ja    R94: Sperrliste herkunft.py Z. 102-106 nennt shared/messkette.py
ja    R94: Sperrliste herkunft.py Z. 102-106 nennt shared/zuteilung.py
ja    R94: Sperrliste herkunft.py Z. 102-106 nennt strategies/*/equity_simulation.py
ja    R94: Sperrliste herkunft.py Z. 102-106 nennt strategies/*/multi_symbol_optimise.py
ja    R94: Sperrliste herkunft.py Z. 102-106 nennt strategies/*/multi_symbol_walk_forward.py
ja    R94: neun Walk-Forward-Rechner verfolgt (die sechs Rechner und drei Erben)
ja    R94/R96 (b)/R97 (f): Abschnitt 9 am Stand 3f2e97e zeichengleich mit d950e03
ja    R94/R96 (b)/R97 (f): Abschnitt 11 am Stand 3f2e97e zeichengleich mit d950e03
ja    R94/R96 (b)/R97 (f): Abschnitt 24 am Stand 3f2e97e zeichengleich mit d950e03
ja    R94/R96 (b)/R97 (f): Abschnitt 37 am Stand 3f2e97e zeichengleich mit d950e03
ja    R94/R96 (b)/R97 (f): Abschnitt 41 am Stand 3f2e97e zeichengleich mit d950e03
ja    R94/R96 (b)/R97 (f): Abschnitt 51 am Stand 3f2e97e zeichengleich mit d950e03
ja    R94/R96 (b)/R97 (f): Abschnitt 54 am Stand 3f2e97e zeichengleich mit d950e03
ja    Register seit 3f2e97e unveraendert
ja    F11 (3)/R97 (f): research/tb24_haltedauern/positionen_holen.py am HEAD unveraendert gegen 7b9f9ac (Verhalten nach der Wiedergabe in 14.10.b)
ja    F11 (3)/R97 (f): shared/zuteilung.py am HEAD unveraendert gegen 7b9f9ac (Verhalten nach der Wiedergabe in 14.10.b)
ja    F11 (1)/R56 (b): docs/projektfuehrung/FABLE_ANTWORT_2026-10-14a_wf_kapital_dd_versuch_vor_dem_tag.md verfolgt, gleich HEAD
ja    F11 (1)/R56 (b): docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14a_wf_kapital_dd_vor_dem_tag.md verfolgt, gleich HEAD
ja    F11 (1)/R56 (b): docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14_eroeffnung.md verfolgt, gleich HEAD
ja    F11 (1)/R56 (b): docs/projektfuehrung/FABLE_ANTWORT_2026-10-14b_doppellauf_verstoesst_gegen_a9_positionen_nach_r45.md verfolgt, gleich HEAD
ja    F11 (1)/R56 (b): docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14b_positionen_ohne_kennung.md verfolgt, gleich HEAD
ja    F11 (1)/R56 (b): docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14b_eroeffnung.md verfolgt, gleich HEAD
ja    Fable-Datei 14.10.a md5 c33799567a0205f66c502dbf5aaff5c5
ja    Fable-Datei 14.10.b md5 4b02ae62279294f5b1df4b1472cc2435
ja    R94-R97 und Abschnitt 58 noch nicht im Register
Pruefungen: 25, NEIN: 0
rc 0
```

## Schritt 0

- 0a: Zweig `main`, HEAD `7b9f9aceddc68a5365737683d466671904a42762`, genau die 10 Einträge des Solls (`docs/belege/TB-162/0a_status.txt`).
- Holbefehl: alle sechs sha256 wie Soll (`tb162_werkzeug.py 34e70f6c…72c7`, `fenster.py 203636cb…6572`, `messung.py 04818772…1c21`, `rekonstruktion.py 6a699e62…97a4`, `test_fenster.py be9c8147…76c9`, `test_rekonstruktion.py 6efca888…8d88`).
- ⟨S0⟩ `9a1bc7a` mit genau den 10 Pfaden, gepusht; danach `0a_status.txt` und `tb162_werkzeug.py` kopiert, je `diff` ohne Ausgabe.

## Register

**Eingetragen** in ⟨R⟩ `0e1e662` (Datum 15.10.2026, ⟨S0⟩ `9a1bc7a`):
- Probe `r_probe.txt`: 15 Prüfungen, NEIN 0, rc 0. Eintrag `r_eintrag.txt`: 17 Prüfungen, NEIN 0, rc 0.
- `## 58. Fable 14a und 14b — Registerblock R94–R97 (TB-162)` ab Z. 12043 mit 58.1 (R94), 58.2 (R95), 58.3 (R96), 58.4 (R97), 58.5 (Voraussetzungen und Befunde); R94–R97 mit Quellenzeile je genau einmal zeichengleich.
- 8 Marken an Z. 5238, 5241, 10971, 10974, 11014, 11867, 12059, 12069: 6 am alten Ort (Abschnitt 27 ×2, 48.13 ×2, 48.14, 56.1), 2 in 58 (58.2, 58.3 BERICHTIGT durch R97).

**Schritt K** (⟨K⟩ `4ec04df`), jede Belegdatei endet mit `rc 0`:
- `registerkopie.py`: sechs Teildateien, **neue `REGISTER_KOPIE_teil6.md`** (Abschnitte 58–58, 18 319 Bytes) wie in der Simulation; Bodies aneinander 1 127 111 Bytes, BYTEGLEICH mit dem Register am `0e1e662c92cb`.
- `--abschnitte`: 59 Dateien 0–58, BYTEGLEICH; `--pruefen`: BYTEGLEICH.
- `c2_index_zeilen.py 9a1bc7a 0e1e662`: 432 Zahlen in Zeilenangaben umgeschrieben, davon 251 geändert.
- `WZ index`: 9 Prüfungen, NEIN 0 (8 Marken mit Zeile, 58 in Teil 6, Kopf, Tabelle-4-Zeilen 27/48/56, Zeile 57, Pflegeanker, Pflegezeile).
- `WZ handfelder` und `dialog_index.py --handfelder`: 61 Zeilen = 61 `FABLE_ANTWORT_*.md`; 61 von 61 mit allen sechs Feldern; Status offen 9, ohne Registertext 12, registriert 40. `--pruefen` gleich.
- Handfelder 14a und 14b: Wortlaut des Baus, zur Abnahme durch den steuernden Chat.

## Messung

⟨M⟩ `ac3e9f2`. Proben: `m_test.txt` „9 von 9 Pruefungen bestanden“, rc 0; `m_test_rekonstruktion.txt` „10 von 10 Pruefungen bestanden“, rc 0. `m_messung.txt`:

```
elliott_wave                 rc 0  8.3 s
elliott_wave_stocks          rc 0  16.9 s
rsi2_crypto                  rc 0  1.3 s
rsi2_mean_reversion          rc 0  12.1 s
t3_supertrend                rc 0  3.1 s
turtle_soup_crypto           rc 0  1.8 s
turtle_soup_stocks           rc 0  16.3 s
volatility_breakout          rc 0  13.5 s
volatility_breakout_crypto   rc 0  1.3 s
Sperrliste vorher = nachher: True; Bots rc 0: 9 von 9; Laufzeit 74.5 s
rc 0
```

### `research/wf_kapital_dd/ergebnisse/tabelle.md`, wörtlich

Kapital-Drawdown E und M der heutigen Parameter je Abschnitt des bot-eigenen Walk-Forward (TB-162). Bericht, kein Tor: die Zahl entscheidet nichts (24.3); kein Raster, kein Score, keine Rangfolge (R94). Commit 4ec04df. Sperrliste vorher = nachher: True. Positionen: Rekonstruktion nach R97 (b) (kein Nachweis, R95 (b)); Regel: Z1 gleiches Symbol, exit_time = time (UTC), |pnl_pct-Diff| <= 1e-09; Z2 bei mehreren: Kapitalprobe |allocation - allocation_pct x Kapital beim Einstieg| <= 0.01; Z3 inhaltsgleiche Kandidaten: kleinste Zeile; Z4 sonst nicht zuordenbar (gemeldet).

| Bot | Positionen (Rekonstruktion) | Abschnitt | von | bis (ausschl.) | Ausstiege | E % | M % | M−E pp | Exposure | Grenzen frueh/spaet (Spannweite Tage) | Datenbestand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| elliott_wave | 227 zugeordnet, 0 nicht zuordenbar | gesamt | 2017-08-17 00:00:00 | 2026-09-16 00:00:00 | 227 | -13.97 | -16.42 | -2.45 | 0.0357 | 2023-12-27 02:00:00 / 2025-12-20 13:00:00 (724.46) | 18 Symbole, 07ac28ce6686 |
| elliott_wave | 227 zugeordnet, 0 nicht zuordenbar | IS | 2017-08-17 00:00:00 | 2023-12-27 02:00:00 | 148 | -13.97 | -16.42 | -2.45 | 0.0305 | 2023-12-27 02:00:00 / 2025-12-20 13:00:00 (724.46) | 18 Symbole, 07ac28ce6686 |
| elliott_wave | 227 zugeordnet, 0 nicht zuordenbar | gemischt | 2023-12-27 02:00:00 | 2025-12-20 13:00:00 | 60 | -3.9 | -7.02 | -3.12 | 0.0494 | 2023-12-27 02:00:00 / 2025-12-20 13:00:00 (724.46) | 18 Symbole, 07ac28ce6686 |
| elliott_wave | 227 zugeordnet, 0 nicht zuordenbar | OOS | 2025-12-20 13:00:00 | 2026-09-16 00:00:00 | 19 | -3.11 | -3.34 | -0.23 | 0.0448 | 2023-12-27 02:00:00 / 2025-12-20 13:00:00 (724.46) | 18 Symbole, 07ac28ce6686 |
| elliott_wave_stocks | 394 zugeordnet, 0 nicht zuordenbar | gesamt | 2016-08-31 00:00:00 | 2026-09-02 00:00:00 | 394 | -22.97 | -20.91 | 2.06 | 0.4139 | 2023-08-29 00:00:00 / 2025-02-21 00:00:00 (542.0) | 147 Symbole, 64d19159795a |
| elliott_wave_stocks | 394 zugeordnet, 0 nicht zuordenbar | IS | 2016-08-31 00:00:00 | 2023-08-29 00:00:00 | 278 | -22.97 | -20.91 | 2.06 | 0.399 | 2023-08-29 00:00:00 / 2025-02-21 00:00:00 (542.0) | 147 Symbole, 64d19159795a |
| elliott_wave_stocks | 394 zugeordnet, 0 nicht zuordenbar | gemischt | 2023-08-29 00:00:00 | 2025-02-21 00:00:00 | 28 | -3.26 | -6.65 | -3.39 | 0.3029 | 2023-08-29 00:00:00 / 2025-02-21 00:00:00 (542.0) | 147 Symbole, 64d19159795a |
| elliott_wave_stocks | 394 zugeordnet, 0 nicht zuordenbar | OOS | 2025-02-21 00:00:00 | 2026-09-02 00:00:00 | 88 | -8.33 | -12.5 | -4.17 | 0.5884 | 2023-08-29 00:00:00 / 2025-02-21 00:00:00 (542.0) | 147 Symbole, 64d19159795a |
| rsi2_crypto | 663 zugeordnet, 0 nicht zuordenbar | gesamt | 2017-08-17 00:00:00 | 2026-09-15 00:00:00 | 663 | -16.6 | -25.02 | -8.42 | 0.104 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| rsi2_crypto | 663 zugeordnet, 0 nicht zuordenbar | IS | 2017-08-17 00:00:00 | 2023-12-24 12:00:00 | 359 | -16.6 | -25.02 | -8.42 | 0.0807 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| rsi2_crypto | 663 zugeordnet, 0 nicht zuordenbar | gemischt | 2023-12-24 12:00:00 | 2026-04-03 11:59:59.999999996 | 272 | -13.94 | -17.16 | -3.22 | 0.1665 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| rsi2_crypto | 663 zugeordnet, 0 nicht zuordenbar | OOS | 2026-04-03 11:59:59.999999996 | 2026-09-15 00:00:00 | 32 | -3.14 | -4.28 | -1.14 | 0.0963 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| rsi2_mean_reversion | 4218 zugeordnet, 0 nicht zuordenbar | gesamt | 1962-01-02 00:00:00 | 2026-09-02 00:00:00 | 4218 | -19.53 | -22.38 | -2.85 | 0.3914 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| rsi2_mean_reversion | 4218 zugeordnet, 0 nicht zuordenbar | IS | 1962-01-02 00:00:00 | 2023-08-31 09:36:00 | 2803 | -19.53 | -22.38 | -2.85 | 0.3758 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| rsi2_mean_reversion | 4218 zugeordnet, 0 nicht zuordenbar | gemischt | 2023-08-31 09:36:00 | 2023-09-01 09:36:00 | 0 | 0.0 | 0.0 | 0.0 | 0.05 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| rsi2_mean_reversion | 4218 zugeordnet, 0 nicht zuordenbar | OOS | 2023-09-01 09:36:00 | 2026-09-02 00:00:00 | 1415 | -5.05 | -7.27 | -2.22 | 0.428 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| t3_supertrend | 1031 zugeordnet, 0 nicht zuordenbar | gesamt | 2017-08-17 00:00:00 | 2026-09-16 00:00:00 | 1031 | -22.4 | -24.36 | -1.96 | 0.1471 | 2023-12-26 04:00:00 / 2025-12-20 12:00:00 (725.33) | 18 Symbole, ffc665e0b0d0 |
| t3_supertrend | 1031 zugeordnet, 0 nicht zuordenbar | IS | 2017-08-17 00:00:00 | 2023-12-26 04:00:00 | 631 | -22.4 | -24.36 | -1.96 | 0.1254 | 2023-12-26 04:00:00 / 2025-12-20 12:00:00 (725.33) | 18 Symbole, ffc665e0b0d0 |
| t3_supertrend | 1031 zugeordnet, 0 nicht zuordenbar | gemischt | 2023-12-26 04:00:00 | 2025-12-20 12:00:00 | 290 | -18.94 | -20.8 | -1.86 | 0.1955 | 2023-12-26 04:00:00 / 2025-12-20 12:00:00 (725.33) | 18 Symbole, ffc665e0b0d0 |
| t3_supertrend | 1031 zugeordnet, 0 nicht zuordenbar | OOS | 2025-12-20 12:00:00 | 2026-09-16 00:00:00 | 110 | -10.26 | -12.12 | -1.86 | 0.2053 | 2023-12-26 04:00:00 / 2025-12-20 12:00:00 (725.33) | 18 Symbole, ffc665e0b0d0 |
| turtle_soup_crypto | 1971 zugeordnet, 0 nicht zuordenbar | gesamt | 2017-08-17 00:00:00 | 2026-09-15 00:00:00 | 1971 | -34.85 | -38.55 | -3.7 | 0.3703 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| turtle_soup_crypto | 1971 zugeordnet, 0 nicht zuordenbar | IS | 2017-08-17 00:00:00 | 2023-12-24 12:00:00 | 1085 | -32.9 | -35.3 | -2.4 | 0.3057 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| turtle_soup_crypto | 1971 zugeordnet, 0 nicht zuordenbar | gemischt | 2023-12-24 12:00:00 | 2026-04-03 11:59:59.999999996 | 738 | -34.85 | -38.55 | -3.7 | 0.5137 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| turtle_soup_crypto | 1971 zugeordnet, 0 nicht zuordenbar | OOS | 2026-04-03 11:59:59.999999996 | 2026-09-15 00:00:00 | 148 | -10.29 | -12.72 | -2.43 | 0.5367 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| turtle_soup_stocks | 8914 zugeordnet, 0 nicht zuordenbar | gesamt | 1962-01-02 00:00:00 | 2026-09-02 00:00:00 | 8914 | -29.07 | -33.93 | -4.86 | 0.7569 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| turtle_soup_stocks | 8914 zugeordnet, 0 nicht zuordenbar | IS | 1962-01-02 00:00:00 | 2023-08-31 09:36:00 | 6062 | -29.07 | -33.93 | -4.86 | 0.7382 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| turtle_soup_stocks | 8914 zugeordnet, 0 nicht zuordenbar | gemischt | 2023-08-31 09:36:00 | 2023-09-01 09:36:00 | 17 | -0.11 | 0.0 | 0.11 | 0.7021 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| turtle_soup_stocks | 8914 zugeordnet, 0 nicht zuordenbar | OOS | 2023-09-01 09:36:00 | 2026-09-02 00:00:00 | 2835 | -13.29 | -18.87 | -5.58 | 0.8006 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| volatility_breakout | 1461 zugeordnet, 0 nicht zuordenbar | gesamt | 1962-01-02 00:00:00 | 2026-09-02 00:00:00 | 1461 | -22.46 | -23.94 | -1.48 | 0.8308 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| volatility_breakout | 1461 zugeordnet, 0 nicht zuordenbar | IS | 1962-01-02 00:00:00 | 2023-08-31 09:36:00 | 1004 | -22.46 | -23.94 | -1.48 | 0.8198 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| volatility_breakout | 1461 zugeordnet, 0 nicht zuordenbar | gemischt | 2023-08-31 09:36:00 | 2023-09-01 09:36:00 | 0 | 0.0 | 0.0 | 0.0 | 0.9017 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| volatility_breakout | 1461 zugeordnet, 0 nicht zuordenbar | OOS | 2023-09-01 09:36:00 | 2026-09-02 00:00:00 | 457 | -12.97 | -16.86 | -3.89 | 0.8565 | 2023-08-31 09:36:00 / 2023-09-01 09:36:00 (1.0) | 147 Symbole, 26bc5a0f9faf |
| volatility_breakout_crypto | 342 zugeordnet, 0 nicht zuordenbar | gesamt | 2017-08-17 00:00:00 | 2026-09-15 00:00:00 | 342 | -16.29 | -19.3 | -3.01 | 0.091 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| volatility_breakout_crypto | 342 zugeordnet, 0 nicht zuordenbar | IS | 2017-08-17 00:00:00 | 2023-12-24 12:00:00 | 197 | -16.29 | -19.3 | -3.01 | 0.07 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| volatility_breakout_crypto | 342 zugeordnet, 0 nicht zuordenbar | gemischt | 2023-12-24 12:00:00 | 2026-04-03 11:59:59.999999996 | 110 | -14.86 | -14.4 | 0.46 | 0.1112 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |
| volatility_breakout_crypto | 342 zugeordnet, 0 nicht zuordenbar | OOS | 2026-04-03 11:59:59.999999996 | 2026-09-15 00:00:00 | 35 | -3.95 | -6.56 | -2.61 | 0.2658 | 2023-12-24 12:00:00 / 2026-04-03 11:59:59.999999996 (831.0) | 20 Symbole, 99611ebf791b |

### Rekonstruktion je Bot

Aus `research/wf_kapital_dd/ergebnisse/<bot>.json`, Feld `rekonstruktion`. Eindeutig = Zuordnung nach Z1 allein; Z2 = durch Kapitalprobe; Z3 = inhaltsgleiche Kandidaten. Status bei allen neun: „vollstaendig zugeordnet“; `trades_unveraendert` bei allen `true`.

| Bot | Trades gefunden | Kurvenzeilen | zugeordnet | nicht zuordenbar | eindeutig (Z1) | Z2 | Z3 | `kursdaten_symbole` |
|---|---|---|---|---|---|---|---|---|
| elliott_wave | 227 | 227 | 227 | 0 | 227 | 0 | 0 | 18 |
| elliott_wave_stocks | 510 | 394 | 394 | 0 | 394 | 0 | 0 | 147 |
| rsi2_crypto | 717 | 663 | 663 | 0 | 663 | 0 | 0 | 20 |
| rsi2_mean_reversion | 5391 | 4218 | 4218 | 0 | 4218 | 0 | 0 | 147 |
| t3_supertrend | 1408 | 1031 | 1031 | 0 | 1031 | 0 | 0 | 18 |
| turtle_soup_crypto | 2162 | 1971 | 1971 | 0 | 1971 | 0 | 0 | 20 |
| turtle_soup_stocks | 12069 | 8914 | 8914 | 0 | 8914 | 0 | 0 | 147 |
| volatility_breakout | 4510 | 1461 | 1461 | 0 | 1461 | 0 | 0 | 147 |
| volatility_breakout_crypto | 373 | 342 | 342 | 0 | 342 | 0 | 0 | 20 |

„Trades gefunden“ ist die Länge der Trade-Liste vor der Zuteilung (`trades_gefunden` = `len(trades)`, `rekonstruktion.py` Z. 49); sie ist bei allen neun gleich `num_executed` + `num_skipped`. „Kurvenzeilen“ ist die Zahl der Zeilen der `equity_curve` (= `num_executed`), die zuzuordnen waren.

### Grenzen-Streuung je Bot

Aus `split_all_symbols` des Bots (`train_split_ratio` 0.7 bei allen neun), Feld `grenzen_streuung`. Kein Symbol ohne Grenze.

| Bot | Symbole | frueheste | spaeteste | Median | Spannweite Tage |
|---|---|---|---|---|---|
| elliott_wave | 18 | 2023-12-27 02:00:00 | 2025-12-20 13:00:00 | 2024-09-17 12:00:00 | 724.46 |
| elliott_wave_stocks | 147 | 2023-08-29 00:00:00 | 2025-02-21 00:00:00 | 2023-08-30 00:00:00 | 542.0 |
| rsi2_crypto | 20 | 2023-12-24 12:00:00 | 2026-04-03 11:59:59.999999996 | 2024-11-21 01:12:00 | 831.0 |
| rsi2_mean_reversion | 147 | 2023-08-31 09:36:00 | 2023-09-01 09:36:00 | 2023-09-01 09:36:00 | 1.0 |
| t3_supertrend | 18 | 2023-12-26 04:00:00 | 2025-12-20 12:00:00 | 2024-09-17 00:00:00 | 725.33 |
| turtle_soup_crypto | 20 | 2023-12-24 12:00:00 | 2026-04-03 11:59:59.999999996 | 2024-11-21 01:12:00 | 831.0 |
| turtle_soup_stocks | 147 | 2023-08-31 09:36:00 | 2023-09-01 09:36:00 | 2023-09-01 09:36:00 | 1.0 |
| volatility_breakout | 147 | 2023-08-31 09:36:00 | 2023-09-01 09:36:00 | 2023-09-01 09:36:00 | 1.0 |
| volatility_breakout_crypto | 20 | 2023-12-24 12:00:00 | 2026-04-03 11:59:59.999999996 | 2024-11-21 01:12:00 | 831.0 |

### Datenbestand

Feld `datenbestand`; `TB_SELEKTIONSWURZEL` und `TB_SELEKTIONSHASH` bei allen neun nicht gesetzt (`null`).

| Bot | Symbole | Zeilen | sha256 Kurzbild |
|---|---|---|---|
| elliott_wave | 18 | 999 901 | `07ac28ce668689177e811fc4d7e134c4ce8e0cbf8621348e2f25dea535b3490b` |
| elliott_wave_stocks | 147 | 361 942 | `64d19159795a27e3340cf12b5a8f8d591d5b1b82128ac54e9b101efef76ba761` |
| rsi2_crypto | 20 | 42 848 | `99611ebf791bb8d0928f1dd9434b4116e0f6ca1af51127d0cba4fd4ae22afe5c` |
| rsi2_mean_reversion | 147 | 1 415 398 | `26bc5a0f9fafbaee602667385994369e5c59bab8b8ae1b54f6525c380b942402` |
| t3_supertrend | 18 | 250 110 | `ffc665e0b0d003e5b27d533247e5930a7511cd59e41d7a73b0c26297ae845ec5` |
| turtle_soup_crypto | 20 | 42 848 | `99611ebf791bb8d0928f1dd9434b4116e0f6ca1af51127d0cba4fd4ae22afe5c` |
| turtle_soup_stocks | 147 | 1 415 398 | `26bc5a0f9fafbaee602667385994369e5c59bab8b8ae1b54f6525c380b942402` |
| volatility_breakout | 147 | 1 415 398 | `26bc5a0f9fafbaee602667385994369e5c59bab8b8ae1b54f6525c380b942402` |
| volatility_breakout_crypto | 20 | 42 848 | `99611ebf791bb8d0928f1dd9434b4116e0f6ca1af51127d0cba4fd4ae22afe5c` |

### Parameterdateien und Commit (`ergebnisse/vorher.json`)

Commit `4ec04df1d3dd32cfe4aef8ee0619571aa312a90b` (= ⟨K⟩).

| Bot | Backtest-Modul (sha256) | `live_params.py` (sha256) |
|---|---|---|
| elliott_wave | `backtest_elliott.py` `5358994a2d3d61800a031f14035fdcc516f4cdaa7da0a11ad59394e139e16187` | `a4afe7c179cf20d26ae998204e5d3e0b3ec816ca3077623f068edd027e05b27b` |
| elliott_wave_stocks | `backtest_elliott.py` `174ba29d24ffb9eefa99f7a7466d31df870493cb92d9a69abc1bbbfa6074633c` | `dd2b6afd47c5f282f42455e53edc52c5b2e57e332bd70aae8493939c3c007ba4` |
| rsi2_crypto | `backtest_rsi2.py` `84930445e34940775f6fcc6715616eb77589fc960f988a19b26199f1393e1aca` | `37546218591f26b0a7be600154e15cf21497e6023bc15c524900a3458a06ef6b` |
| rsi2_mean_reversion | `backtest_rsi2.py` `836b032a5962c7766e7ed00a75b90ded4155b769fce54a84fead3c4cd5f3b7fc` | `6a23bbf606f25d3be413138cb6b279f67f3bf2792afe573db86fdacdfa169e06` |
| t3_supertrend | `backtest_trend.py` `7a764353d092e521cc24b80ae97193d624224b38a6a62a45394360fe50cb04bb` | `1425af6743c266bdf82ad2b6526b542036a10c28ccb47e3c49cdd4a4e22faaa3` |
| turtle_soup_crypto | `backtest_turtle_soup.py` `0704c9a96898ede99e9cf2b153da33d0cb885bf16c89e642d8514f277e8a0089` | `28e915726d702ba34ce3a61df225dd1604c103e8ba867f66a5a6c0c87e58e9d8` |
| turtle_soup_stocks | `backtest_turtle_soup.py` `0de39bf20bbbd3c0988b270262728a08cddc79a448fd0300c2f6b94998df50bb` | `a556ffbf3f9de63dff1e2751cd29d40b0fe8a6d13761da412bee40ce79908469` |
| volatility_breakout | `backtest_breakout.py` `3fd0cef6c284a8806cace3663c241295edbb1ef8ee79092abfd0dc55e2bf6a76` | `c1bc00d8627aa66324c98230357ccad8df3694d3ac37fe71b3526db285f75770` |
| volatility_breakout_crypto | `backtest_breakout.py` `3c7ccbe792ea5eb8dcbc76ae27079f4d7c47ca34bd3ad5edd332d4fdad3c403e` | `0cae328c0ed5155ee1a585b7bd96924125440f02303472325814eb74e6a60e86` |

### Sperrliste vorher/nachher

`ergebnisse/vorher.json` führt sha256 von 29 Dateien der Sperrliste (`shared/messkette.py`, `shared/zuteilung.py`, je neun `equity_simulation.py`, `multi_symbol_optimise.py`, `multi_symbol_walk_forward.py`); `ergebnisse/laufprotokoll.json`: `"sperrliste_gleich": true`, `"python": "3.9.6"`, je Bot `rc 0` und leeres `stderr_ende`. Vorher = nachher: **True**. Beispiele: `shared/zuteilung.py` `68a812a0567dec8b72e6d60fd891091aff546d1adaddf03ddd9b4459ca73da47`, `shared/messkette.py` `885697825c4ab81f6140bda866db82067a5d57f3523cdfc0d49ffe37c0782de0`.

## Vorschlag Tatsachennotiz (Bauart 24.6; nicht eingetragen, F3)

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

## Abweichungen

- **Keine Abweichung vom Soll** in 0a, Holbefehl, V, R, K und M; alle Belegdateien enden mit `rc 0`. Die Teildatei 6 entstand wie in der Simulation (Name unverändert).
- **Befund, kein Abbruch („M flacher als E“, 24.6):** elliott_wave_stocks gesamt/IS (M−E +2,06 pp), turtle_soup_stocks gemischt (+0,11 pp), volatility_breakout_crypto gemischt (+0,46 pp).
- **Beobachtung:** Bei den drei Aktien-Bots mit 1-Tag-Spannweite ist der Abschnitt „gemischt“ praktisch leer; bei allen vier Aktien-Bots beginnt der Pfad am frühesten Kursdatum (1962-01-02 bzw. 2016-08-31), die ersten Einstiege liegen aber 2016 (`erster_einstieg` 2016-09-01 bzw. 2016-10-28). Der IS-Abschnitt enthält also bei rsi2_mean_reversion, turtle_soup_stocks und volatility_breakout Jahrzehnte ohne Position; auf E und M hat das keinen Einfluss (kein Drawdown ohne Position), wohl auf die mittlere Exposure des Abschnitts.
- **Laufzeit am Mac:** 74,5 s für alle neun Bots (Python 3.9.6); die Module lesen sich auf 3.9 ohne Fehler (offener Punkt des Baus damit beantwortet).
- **Journal:** Das Werkzeug setzt Block EX vor das abschliessende `---` vor „Wiederkehrende Lehren“; zwischen EW und EX steht damit kein eigener `---`-Trenner (Bauart des Werkzeugs, nicht nachgebessert).

## In einfacher Sprache

Die vier neuen Regeln des Verfahrensprüfers (R94–R97) stehen jetzt im Register, mit allen Querverweisen, und die Kopien und Verzeichnisse dazu sind nachgezogen. Danach wurde für jeden der neun Bots gemessen, wie tief das Konto mit den heutigen Einstellungen zwischendurch fiel — einmal nur an den Verkaufstagen gezählt (E), einmal täglich mit den offenen Positionen (M) —, für die ganze Zeit und getrennt nach den Zeitabschnitten des Walk-Forward. Die gekauften Positionen wurden aus einem einzigen, unveränderten Simulationslauf zurückgerechnet; bei allen neun Bots ging das ohne einen einzigen Rest auf. Meist ist der tägliche Wert tiefer als der an den Verkaufstagen, an vier Stellen ist es umgekehrt. Die Zahlen sind ein Bericht und entscheiden nichts; ob sie als Notiz ins Register kommen, entscheidet der steuernde Chat.
