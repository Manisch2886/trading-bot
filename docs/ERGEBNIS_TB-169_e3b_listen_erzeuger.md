# ERGEBNIS TB-169 — E-3b Listen-Erzeuger (Schnitt an der Eingabe, Wachen, Doppellauf weg), Abnahme E-3a nach R98 (d), Register 64 (Vollzug TB-166 nach 37.3)

**Sitzung:** TB-169, Mac (Claude Code, Opus 5.5), 16.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-169_e3b_listen_erzeuger.md` · **Zweig:** `main`
**Commits:** `69539db` (S0, Schritt 0) · `8520d9e` (E, E-3b und Abnahme) · `3cbcdee` (N, Register 64) · `fd70e54` (K, Registerkopie, Index) · F = der Abgabe-Commit „TB-169 Abgabe: Ergebnis, BACKLOG, Journal FF“, der dieses Ergebnis enthält · danach „TB-169 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-169/` · **Journal:** FF · **Kein Abbruch.**

## Kurz

E-3b ist eingespielt: `research/tb24_haltedauern/positionen_holen.py` (numstat 79/112) und `alle_bots.py` (7/2) haben die sha256 aus dem Bau, der neue Test `test_listen_erzeuger.py` (182 Zeilen) ebenfalls. Die Abnahme nach R98 (d) am Erzeuger ist grün: **117 von 117**, rc 0, 9 × 13 ja. Die Kerzen-Probe lief zum ersten Mal in `trading-env` (Python 3.9.6) und ergab für alle 25 861 Trades der neun Listen dieselben Kerzenzahlen (0 abweichend). Der alte Test `test_haltedauer_kern.py` ist vorher wie nachher in Prüfung 13 rot (dieselbe Fehlzeile, rc 1), wie im Auftrag erwartet. Weil die Abnahme grün war, ist Register 64 angehängt (append-only, 46/0, ab Z. 12390). 64.1 übernimmt `docs/belege/TB-166/e_notiz.md` zeichengleich (20 Hash-Übergänge, Commit `15f28e4`). Die Sonde meldet zu Punkt 11 „nicht prüfbar“. Registerkopie und Index sind nachgezogen, BACKLOG Rang 1 und Journal FF eingetragen. Keine Liste neu erzeugt, kein Lauf auf Kursdaten aus `data/`, kein neues Abbild.

## Schritt 0

`git status --porcelain` zeigte genau die vier Soll-Einträge (`docs/belege/TB-169/0a_status.txt`), HEAD `b9a620273e2d412d0fc6d12d55fbecfd04bd9ac8` auf `main`, Karte gefüllt; letzte Zeile `0a gut (4 Eintraege)`. Holbefehl: alle fünf sha256 wie Soll, `Dateien 5`. S0 = `69539db`, gepusht, porcelain danach leer.

## Voraussetzungen (`v_voraussetzung.txt`, wörtlich)

```
ja    Register: 63 genau einmal, 64 noch nicht
ja    Register endet mit genau einer Leerzeile
ja    Vorbild 63.1 genau einmal, Z. [12372]
ja    37.3 zuerst Z. 7025
ja    vorher research/tb24_haltedauern/alle_bots.py: 6e9ddce913b555a1
ja    Anhang docs/belege/TB-169/e3b_alle_bots.py = nachher 4246b577bfc486e3…
ja    vorher research/tb24_haltedauern/positionen_holen.py: a9e81f02dd69d946
ja    Anhang docs/belege/TB-169/e3b_positionen_holen.py = nachher b6d1e2d66eae02a8…
ja    vorher research/tb24_haltedauern/test_listen_erzeuger.py: fehlt
ja    Anhang docs/belege/TB-169/e3b_test_listen_erzeuger.py = nachher e196884a152796e4…
ja    e_notiz.md md5 e28885ae5e10e158860fb457671ce900, Commit 4a51876
ja    e_notiz.md: 20 Zeilen, 20 Dateien
ja    heute = nachher, zuletzt in 15f28e4: research/exposure_messung/bot_lauf.py
ja    heute = nachher, zuletzt in 15f28e4: research/faltenplan_neun/faltenschranke_messung.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/elliott_wave/elliott_wave_counter.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/elliott_wave/equity_simulation.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/elliott_wave/multi_symbol_optimise.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/elliott_wave_stocks/elliott_wave_counter.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/elliott_wave_stocks/equity_simulation.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/elliott_wave_stocks/multi_symbol_optimise.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/rsi2_crypto/backtest_rsi2.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/rsi2_crypto/equity_simulation.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/rsi2_mean_reversion/backtest_rsi2.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/t3_supertrend/backtest_trend.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/t3_supertrend/equity_simulation.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/t3_supertrend/multi_symbol_optimise.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/turtle_soup_crypto/backtest_turtle_soup.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/turtle_soup_crypto/equity_simulation.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/turtle_soup_stocks/backtest_turtle_soup.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/volatility_breakout/backtest_breakout.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/volatility_breakout_crypto/backtest_breakout.py
ja    heute = nachher, zuletzt in 15f28e4: strategies/volatility_breakout_crypto/equity_simulation.py
ja    sha256 Abbild 46f0ad5d1d83a253… und Sonde 98c02e0e9b42831d…
ja    Abbild fuehrt keine der 20 Dateien
ja    Karte TB-166: Z. 14, md5 57d05b949318d95e5ef28a5692ef1241, Commit 57a1062
ja    Karte TB-169 gefuellt
ja    Index: Kopf 0–63, Zeile 63, Pflegezeile TB-168
ja    BACKLOG Rang 1 (Stand TB-166) genau einmal
ja    Journal hoechste FE, naechste FF frei
Pruefungen: 39, NEIN: 0
rc 0
```

## Schritt E — E-3b und Abnahme nach R98 (d)

Letzte Zeilen je Beleg:

| Beleg | letzte Zeilen |
|---|---|
| `e_alt_vorher.txt` | `  - wer schreibt, schreibt in den eigenen Ordner (aussen vor: ['positionen_holen.py'])` · `rc 1` (erwartet: Prüfung 13 schon am HEAD rot) |
| `e_e3b_probe.txt` | `Pruefungen: 6, NEIN: 0` · `rc 0` |
| `e_e3b.txt` | `ja    nachher research/tb24_haltedauern/test_listen_erzeuger.py e196884a…` · `Pruefungen: 9, NEIN: 0` · `rc 0` |
| `e_alt_nachher.txt` | `  - wer schreibt, schreibt in den eigenen Ordner (aussen vor: ['positionen_holen.py'])` · `rc 1` (wie vorher) |
| `e_alt_vergleich.txt` | `ja    Fehlzeilen vorher 1 = nachher 1: …` · `Pruefungen: 2, NEIN: 0` · `rc 0` |
| `e_kerzen.txt` | `Ergebnis: 25861 Trades verglichen, 0 abweichend oder ohne Kursreihe` · `rc 0` |
| `e_abnahme.txt` | `Ergebnis: 117 von 117 bestanden` · `rc 0` |
| `e_abnahme_pruefung.txt` | `ja    Ergebnis 117 von 117, rc 0` · `Pruefungen: 11, NEIN: 0` · `rc 0` |

Kerzen-Probe je Bot (`e_kerzen.txt`): alle neun `ja`, volle Abdeckung (jeder Trade mit Kursreihe im Snapshot) — elliott_wave 130, t3_supertrend 980, rsi2_crypto 439, turtle_soup_crypto 1 599, volatility_breakout_crypto 233, elliott_wave_stocks 510, rsi2_mean_reversion 5 391, turtle_soup_stocks 12 069, volatility_breakout 4 510. Damit ist die Änderung an `kerzen_je_trade` (`.to_datetime64()`) zum ersten Mal unter Python 3.9.6 / `trading-env` gemessen.

Abnahme (`e_abnahme.txt`): je Bot 13 Prüfungen ja (0, 1, 2a, 2b, 2c, 3a, 3b, 4, 5a, 5b, 6, 7, 8), keine NEIN-Zeile. Die Wachen beissen je allein mit Ausgang 2 (2a Wache 1, 2c Wache 2, 4 Wache 3 nach R87 (c), 5b R81 (c)); Prüfung 3a trägt für t3_supertrend und die zwei Elliott-Bots den Wortlaut der Tatsachennotiz nach R90 (g). Der Test hat ausser den drei eigenen Dateien nichts im Arbeitsbaum hinterlassen (porcelain nach E: nur die zwei geänderten Dateien, der Test und `docs/belege/TB-169/`).

E = `8520d9e`, gepusht; numstat `69539db`..`8520d9e` unter `research/`: genau `alle_bots.py` 7/2, `positionen_holen.py` 79/112, `test_listen_erzeuger.py` 182/0.

## Sonde (Schritt S)

Einmal lesend, Aufruf wie TB-168 Schritt S. `s_sonde.txt` endet mit `RUECKGABEWERT 2 NICHT PRUEFBAR - NICHT PRUEFBAR: Punkt(e) [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14]` · `rc 2`. `s_auswahl.txt`: **`Fassung: nicht prüfbar`**, porcelain vor/nach gleich, sha256 Abbild und Sonde wie Soll, Punkt 11 = `2`; `Pruefungen: 3, NEIN: 0`, `rc 0`.

## Register 64 (Schritt N)

`WZ register 16.10.2026 69539db 8520d9e … --probe` rc 0 (33 Prüfungen), danach der Eintrag rc 0 (35 Prüfungen, u. a. „nachher: append-only, 64 genau einmal, Z. 12390“, „e_notiz.md zeichengleich“). Titel an **Z. 12390**:

```
## 64. Vollzug TB-166 (Tatsachennotiz nach 37.3; E-3a Schranke je Symbol) mit Abnahme nach R98 (d) (TB-169)
```

numstat `8520d9e`..`3cbcdee`: `46	0	docs/VORREGISTRIERUNG_neuselektion.md`. N = `3cbcdee`. Keine Marke.

## Schritt K

| Schritt | Beleg | rc |
|---|---|---|
| `registerkopie.py` | `k_registerkopie.txt` | 0 |
| `registerkopie.py --abschnitte` | `k_abschnitte.txt` | 0 |
| `registerkopie.py --pruefen` | `k_pruefen.txt` | 0 |
| `c2_index_zeilen.py 69539db 3cbcdee` | `k_index_zeilen.txt` | 0 |
| `WZ index 69539db 16.10.2026` | `k_index.txt` | 0 |

64 liegt in T6 (Abschnitte 58–64, 79 024 B ≤ 240 000); neue Abschnittskopie `REGISTER_KOPIE_ABSCHNITT_64.md` (10 852 B). Bodies aneinander 1 189 202 B, sha256 `f5510c4b330c769e…`, BYTEGLEICH mit dem Register am `3cbcdee`. Zeilenangaben: 466 umgeschrieben, 0 geändert. Die übrigen Kopien ändern nur die Kopfzeile (Commit, Bereich 0–64, sha256). K = `fd70e54`.

## BACKLOG und Journal

`WZ kennung`: „Kennung FF (letzte FE)“. `WZ backlog 16.10.2026 FF` hängt an Rang 1 an (E-3b und Abnahme mit TB-169, Register 64; vor der Neuerzeugung: `auswertung.py`, `embargo_neun.py`, Abbild tb117, R102 (d), R92 (c)). Journal-Block `docs/belege/TB-169/a_block.md` vor `## Wiederkehrende Lehren`. Belege `a_*.txt`.

## Offen

Vor der Neuerzeugung der neun Listen:

- R102 (d) und R92 (c).
- `research/tb24_haltedauern/auswertung.py` Z. 71 liest `<bot>_positionen.csv`, Z. 325 `meta[bot]["trades_ausgefuehrt"]`; beides entfällt mit E-3b (C1).
- `research/faltenplan_neun/embargo_neun.py` Z. 35 nennt `daten/<bot>_positionen.csv` (Docstring); die eigentliche Lesestelle ist Z. 232.
- Das Abbild tb117 führt die neun `daten/<bot>_alle_trades.csv`, die Neuerzeugung trifft das Abbild (C3); ein neues Abbild unter neuem Namen vor dem Tag (37.3).

## Abweichungen

Keine vom Auftrag. Beobachtungen, nicht angefasst:

- **Stand im Sondensatz von 64:** `WZ register` setzt in den Satz zur Sonde „gemessen in TB-169 am Stand `69539db`“ (⟨S0⟩). Nach der Reihenfolge des Auftrags lief die Sonde in S aber nach dem E-Commit, am HEAD `8520d9e`. Für Punkt 11 ändert das nichts: das Abbild führt keine der 20 Dateien und keine der drei E-3b-Dateien. Der Satz ist trotzdem ungenau. Vorschlag: im nächsten Registerabschnitt als Tatsachennotiz berichtigen, nicht in 64 selbst (append-only).
- **Weitere Leserin von `<bot>_positionen.csv`, im Auftrag nicht genannt:** `research/mtm_drawdown/grundlage.py` Z. 65 liest `research/tb24_haltedauern/daten/<bot>_positionen.csv` (ebenso `messung.py` Z. 190 als Herkunftsangabe). Das gehört zur Liste vor der Neuerzeugung, zusammen mit `auswertung.py` und `embargo_neun.py`. `WZ backlog` nennt sie nicht; ich habe den Eintrag nicht erweitert.
- Prüfung 7 bei `t3_supertrend` meldet als Detail `['kein Trade']` (keine offene Position am Ende von B im Test-Snapshot dieses Bots). Die Prüfung zählt als bestanden, wie im Bau.

## In einfacher Sprache

Das Programm, das die Handelslisten der neun Bots erzeugt, liest jetzt nur noch Kurse vor dem Go-Live-Tag. Es hält mit einem Fehler an, sobald etwas Späteres oder ein zu früher Einstieg durchrutscht. Ein neuer Test auf erfundenen Kursen prüft das an den fertigen Listen und besteht alle 117 Prüfungen. Die Zählung der Kerzen je Trade musste an einer Stelle an die pandas-Fassung auf dem Mac angepasst werden; sie liefert für alle 25 861 alten Trades genau dieselben Zahlen wie vorher. Weil der Test grün war, stehen die 20 Prüfsummen-Wechsel aus TB-166 jetzt im Register (Abschnitt 64). Die echten Listen wurden noch nicht neu erzeugt. Vorher müssen noch einige Auswertungen umgestellt werden, die eine Datei lesen, die es künftig nicht mehr gibt.
