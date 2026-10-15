# ERGEBNIS TB-164 — Register 60: Vollzug TB-163 (Hash-Übergang nach 37.3) und Tatsachennotiz Posten 5 (R43)

**Sitzung:** TB-164, Mac (Claude Code, Opus 5.5), 15.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-164_register60_vollzug_tb163.md` · **Zweig:** `main`
**Commits:** `1d037f9` (S0, Schritt 0) · `92cb637` (N, Register 60) · `3dfa3ba` (K, Registerkopie, Index) · F = der Abgabe-Commit „TB-164 Abgabe: Ergebnis, BACKLOG, Journal FA“, der dieses Ergebnis enthält · danach „TB-164 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-164/` · **Journal:** FA · **Kein Abbruch.**

## Kurz

Register 60 ist angehängt (append-only, numstat 42/0). 60.1 übernimmt den Entwurf des Hash-Übergangs aus `docs/ERGEBNIS_TB-163_register59_posten4_horizont.md` Z. 111–123 zeichengleich (Bauart 50.3), mit dem Satz zur Sonde. 60.2 ist die Tatsachennotiz zu Posten 5 nach R43 mit den sha256 der neun Optimierer am `1d037f9`. Die Sperrlisten-Sonde lief einmal lesend und meldet zu Punkt 11 `2` „nicht prüfbar“, nicht `1`. Die Erwartung in ERGEBNIS_TB-163 Z. 129 ist damit unten richtiggestellt, die Datei selbst bleibt unverändert. Alle Schritte in K endeten mit rc 0. BACKLOG (Rang 1 und zwei neue Zeilen) und Journal FA sind eingetragen. Kein neues Abbild, kein Lauf auf Kursdaten, kein Code geändert.

## Schritt 0

`git status --porcelain` zeigte genau die zwei Soll-Einträge (`docs/belege/TB-164/0a_status.txt`); HEAD war `89e58efc6973e2c6471df5720b84208fbb900fac` auf `main`. Holbefehl: `tb164_werkzeug.py 7628b47e71404971b7ca9388e0a35c53e2ef9f4f1fd0b4e9e2a0df564a5f1319`, wie Soll. S0 = `1d037f9`, gepusht. Beide Kopien (`0a_status.txt`, `tb164_werkzeug.py`) waren laut `diff` gleich (keine Ausgabe).

## Voraussetzungen (`v_voraussetzung.txt`, wörtlich)

```
ja    Register: 59 genau einmal, 60 noch nicht
ja    Register endet mit genau einer Leerzeile
ja    Register: Vorbild 50.3 genau einmal, Z. 11198–11242
ja    Register: R43-Wortlaut (Wache, „nicht im Laufpfad“, Posten 5 neu zu fassen) genau einmal (Z. 10942)
ja    Register: 37.3 „Ein Befund 1 der Sperrlisten-Sonde“ genau einmal
ja    ERGEBNIS_TB-163 md5 9e4c8f7df087bb25f3b7dba93e51119e
ja    ERGEBNIS_TB-163 zuletzt in Commit d81dc88
ja    ERGEBNIS_TB-163: Grenzen Z. 109 Kopf, Z. 111-123 Entwurf, Z. 124 leer, Z. 125 herkunft.register()
ja    ERGEBNIS_TB-163 Z. 113-123 = docs/belege/TB-163/e_uebergang.md
ja    ERGEBNIS_TB-163 Z. 129 enthält den Satz zur Sonde
ja    sha256 heute = nachher strategies/elliott_wave_stocks/multi_symbol_optimise.py (3b7757004b1c2db5…, 11a267f)
ja    sha256 heute = nachher strategies/rsi2_mean_reversion/multi_symbol_optimise.py (61838aca901cabea…, 11a267f)
ja    sha256 heute = nachher strategies/turtle_soup_stocks/multi_symbol_optimise.py (29e7f10c3eb79f83…, 11a267f)
ja    sha256 heute = nachher strategies/volatility_breakout/multi_symbol_optimise.py (24c182ae1cf7c882…, 11a267f)
ja    Commit 11a267f vorhanden
ja    sha256 Abbild 46f0ad5d1d83a253… und Sonde 98c02e0e9b42831d…
ja    Abbild führt keinen Optimierer
ja    neun Optimierer verfolgt
ja    Posten 5 alt (MAC_TB-120 Z. 128), Bestand 0/9 (ERGEBNIS_TB-120 Z. 101)
ja    backtest_breakout.py Z. 211 enthält entry_time >= np.datetime64(entry_cutoff)
ja    Index: Kopf 0–59, Zeile 59, Pflegezeile TB-163 je genau einmal
ja    BACKLOG: Rang 1 (Stand TB-163) und Scan-Schleifen je genau einmal
ja    Journal: höchste Kennung EZ, nächste FA frei
Pruefungen: 23, NEIN: 0
rc 0
```

## Sonde (Schritt S)

Aufruf (genau einmal, lesend, am Stand `1d037f9`):

```
trading-env/bin/python3 -B -W ignore shared/sperrlistensonde.py --abbild research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json
```

Aus `docs/belege/TB-164/s_sonde.txt`, wörtlich:

```
  Punkt 11  [2 NICHT PRUEFBAR]  Commit-Hashes von Simulation, Erkennung, Optimierern und Auswertungsskript
(ii) Abbild gegen den Registertext von Abschnitt 10:  [0 in Ordnung]
Pfad-Bestandteile: 37 geprueft, davon 37 mit 0 / 0 mit 1 / 0 mit 2  (punkte 15, bestimmt 0, eingefroren 22)
RUECKGABEWERT 2 NICHT PRUEFBAR - NICHT PRUEFBAR: Punkt(e) [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14]
rc 2
```

`docs/belege/TB-164/s_auswahl.txt`, wörtlich:

```
Fassung: nicht prüfbar
Satz 60.1 (⟨S0⟩ setzt WZ register): **Sperrlisten-Sonde zu Punkt 11** (gemessen in TB-164 am Stand `⟨S0⟩`; Aufruf wie TB-122 0b: `trading-env/bin/python3 -B -W ignore shared/sperrlistensonde.py --abbild research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`, Abbild `46f0ad5d…`; Beleg `docs/belege/TB-164/s_sonde.txt`): Punkt 11 „nicht prüfbar“ (`2`). Das Abbild führt keinen der Optimierer (kein Pfad `strategies/*/multi_symbol_optimise.py` darin) — wie bei 50.3. Der Übergang steht deshalb nur hier und in den Commits.
Richtigstellung zu `docs/ERGEBNIS_TB-163_register59_posten4_horizont.md` Z. 129 (dort: „Bis dahin meldet die Sperrlisten-Sonde zu Punkt 11 einen zulässigen Befund `1` (beauftragt, Freigabe dritte Karte).“): gemessen in TB-164 (`docs/belege/TB-164/s_sonde.txt`) meldet die Sonde zu Punkt 11 `2` „nicht prüfbar“, nicht `1`: das Abbild `sperrliste_abbild_2026-09-26_tb117.json` führt die Optimierer nicht (wie Register 50.3). Der Satz in Z. 129 war erschlossen, nicht gemessen. Der Übergang steht mit Register 60 im Register; ein neues Abbild zieht TB-164 nicht (Karte 15.10.2026, 19:27; 37.3, Register Z. 7022). ERGEBNIS_TB-163 bleibt unverändert.
ja    git status --porcelain vor und nach der Sonde gleich (1 Zeilen)
ja    sha256 Abbild 46f0ad5d1d83a253… und Sonde 98c02e0e9b42831d…
ja    Punkt 11 im Beleg: ['2'] · RUECKGABEWERT 2 NICHT PRUEFBAR - NICHT PRUEFBAR: Punkt(e) [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14] · rc 2
Pruefungen: 3, NEIN: 0
rc 0
```

## Richtigstellung zu ERGEBNIS_TB-163 Z. 129

Richtigstellung zu `docs/ERGEBNIS_TB-163_register59_posten4_horizont.md` Z. 129 (dort: „Bis dahin meldet die Sperrlisten-Sonde zu Punkt 11 einen zulässigen Befund `1` (beauftragt, Freigabe dritte Karte).“): gemessen in TB-164 (`docs/belege/TB-164/s_sonde.txt`) meldet die Sonde zu Punkt 11 `2` „nicht prüfbar“, nicht `1`: das Abbild `sperrliste_abbild_2026-09-26_tb117.json` führt die Optimierer nicht (wie Register 50.3). Der Satz in Z. 129 war erschlossen, nicht gemessen. Der Übergang steht mit Register 60 im Register; ein neues Abbild zieht TB-164 nicht (Karte 15.10.2026, 19:27; 37.3, Register Z. 7022). ERGEBNIS_TB-163 bleibt unverändert.

## Register 60 (Schritt N)

Datum `15.10.2026`, S0 `1d037f9`. `WZ register … --probe` endete mit 6 Prüfungen, NEIN 0, rc 0 (`n_probe.txt`). `WZ register` endete mit 9 Prüfungen, NEIN 0, rc 0 (`n_eintrag.txt`): „nachher: altes Register unverändert vorn (append-only), 60 genau einmal, Z. 12153“, „Z. 111-123 zeichengleich im Register“. `## 60. Vollzug TB-163 (Tatsachennotiz nach 37.3) und Tatsachennotiz Posten 5 (TB-164)` steht ab **Z. 12153**, mit 60.1 (Sondensatz in der Fassung „nicht prüfbar“) und 60.2. `git diff --numstat` Register: **42 / 0**. Commit `92cb637`.

## K — Kopien, Index, Dialog-Index

| Schritt | Beleg | rc |
|---|---|---|
| `registerkopie.py` | `k_registerkopie.txt` | 0 |
| `registerkopie.py --abschnitte` | `k_abschnitte.txt` | 0 (Abschnitte 0–60: 61 Dateien, BYTEGLEICH) |
| `registerkopie.py --pruefen` | `k_pruefen.txt` | 0 (T6: Abschnitte 58–60, 29 416 B; Bodies 1 138 208 B, BYTEGLEICH am `92cb637`) |
| `c2_index_zeilen.py 1d037f9 92cb637` | `k_index_zeilen.txt` | 0 (450 Zeilenangaben, davon geändert 0) |
| `WZ index 1d037f9 15.10.2026` | `k_index.txt` | 0 (60 in T6; Kopf 0–60, Zeile 60, Pflegezeile TB-164) |
| `dialog_index.py --pruefen` | `k_dialog_pruefen.txt` | 0 (61/61) |

Keine neue Teildatei, neu ist nur `register_kopie/REGISTER_KOPIE_ABSCHNITT_60.md`. Commit `3dfa3ba`.

## BACKLOG

`a_kennung.txt`: „Kennung FA (letzte EZ)“, rc 0. `WZ backlog 15.10.2026 FA --probe` und `WZ backlog` endeten je mit rc 0, numstat 3/1.
- Rang 1 (TB-30b) ergänzt um „· Register 60 (Vollzug TB-163 nach 37.3; Posten 5 nach R43 neu gefasst) mit TB-164 (15.10.2026, Journal FA)“.
- Neue Zeile unter „Scan-Schleifen in `research/`“: Die Bindung ist offen. „Vor E-6“ ist überholt, offen bleibt „vor Posten 5“, also die Wache im Zellen-Erzeuger nach Register 60.2.
- Neue Zeile: TypeError in `backtest_breakout.py` Z. 211 bei tz-behaftetem `open_time` (Befund TB-163, Abnahme B1).

Journal: `WZ journal … --probe` und `WZ journal` endeten je mit rc 0, Block FA (`a_block.md`) steht vor „Wiederkehrende Lehren“.

## Offen

- Ein neues Sperrlisten-Abbild unter neuem Namen (37.3). Es ist nicht Teil dieses Auftrags (Karte 15.10.2026, 19:27).
- Der Bau des Zellen-Erzeugers mit der Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“ (Posten 5 nach R43).
- Nach der zweiten Karte folgt ein neuer Fable-Chat zu Register 57.6 Nr. 4/5 (R90 (c), Rückfrage F1). Er ist nicht Teil von TB-164.

## Abweichungen

Keine Abweichung vom Ablauf. Vermerk: Die Fassung des Sondensatzes ist „nicht prüfbar“. Das hatte der Auftrag so vorhergesagt („Erschlossen“, Simulation an einer Kopie unter Python 3.10); ERGEBNIS_TB-163 Z. 129 hatte dagegen `1` erwartet. In K hat sich bei den sechs Teildateien und den 60 alten Abschnittskopien je nur die erste Zeile geändert (Kopf mit Commit `92cb637`, Original-sha256 und Bereich „von 0–60“), wie in TB-163 K.

## In einfacher Sprache

Im Register stehen jetzt die alten und neuen Prüfsummen der vier Aktien-Optimierer, die TB-163 mit Freigabe geändert hat. Sie sind Wort für Wort aus dem Ergebnis von TB-163 übernommen. Dazu steht im Register, dass die neun Optimierer im späteren Auswahllauf nicht vorkommen und dass die Wache gegen zu frühe Einstiege deshalb in einen neuen, noch zu bauenden Baustein gehört. Die Prüfung der Sperrliste lief einmal, nur lesend, und meldet für diesen Punkt „nicht prüfbar“ statt „Befund“, wie TB-163 vermutet hatte. Es lief nichts auf Kursdaten, und kein Programmcode wurde geändert.
