# ERGEBNIS TB-170 — Register 65: Fable 16c (R104–R105 zeichengleich), fünf Marken, 65.3 Voraussetzungen und Befunde; BACKLOG-Nachträge

**Sitzung:** TB-170, Mac (Claude Code, Opus 5.5), 17.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-170_register65_fable16c.md` · **Zweig:** `main`
**Commits:** `801a055` (S0, Schritt 0) · `7aecfe6` (R, Register 65 und fünf Marken) · `c602a2f` (K, Registerkopie, Index, Dialog-Index) · der Abgabe-Commit „TB-170 Abgabe: Ergebnis, BACKLOG, Journal FG“, der dieses Ergebnis enthält · danach „TB-170 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-170/` · **Journal:** FG · **Kein Abbruch.**

## Kurz

Die drei Fable-Dateien vom 16.10.c sind zusammen mit UEBERGABE und EROEFFNUNG unverändert in S0 `801a055` committet. Die md5 vorher (`0a_md5.txt`) und nachher (V, „verfolgt, gleich HEAD“) stimmen überein. Die Voraussetzungen sind grün (35/0). Register 65 ist angehängt, ab Z. 12451: R104 und R105 stehen mit ihrer Quellenzeile je genau einmal zeichengleich zum Codeblock der Antwort (Z. 21–26) da, dazu 65.3 mit dem V-Beleg wörtlich und den Tatsachennotizen (a) bis (d). Die fünf Marken sind gesetzt, 57.1 als PRÄZISIERT, die anderen vier als ERGÄNZT. Bis auf diese Marken ist alles append-only (numstat 83/0). Registerkopie, Index (Kopf 0–65, Zeile 65, neuer Abschnitt 16) und Dialog-Index (16c) sind nachgezogen, alle K-Schritte enden mit rc 0. Im BACKLOG hängen an Rang 1 jetzt Register 65, R105 (c) Weg 1 als eigener Handelscode-Punkt vor dem Tag und die vier Nachträge. Kein Handelscode geändert, kein Lauf auf Kursdaten, `data/` nicht gelesen, kein Test, keine Sonde, kein neues Abbild.

## Schritt 0

`git status --porcelain` zeigte genau die sieben Soll-Einträge (`docs/belege/TB-170/0a_status.txt`). HEAD und origin/main standen auf `eff5b5a87787fb939183097c4317667c78d67d9b`, Zweig `main`, die Karte war gefüllt; letzte Zeile `0a gut (7 Eintraege)`. Der Holbefehl lieferte `tb170_werkzeug.py a75dc80917dc69a43b2e6e1502119d6a7da532c967803cb21baa852fbe733da4` und `Dateien 1`. S0 = `801a055`, gepusht, porcelain danach leer.

`0a_md5.txt`, wörtlich:

```
ja    md5 docs/projektfuehrung/FABLE_ANTWORT_2026-10-16c_r100c_elliott_abnahme.md = ebde5e999690f5c8ab0e1930ffb81783
ja    md5 docs/projektfuehrung/FABLE_ANFRAGE_2026-10-16c_r100c_leseprotokoll_elliott_abnahme.md = 4021b20db4e9b9899e040fa5b2236b35
ja    md5 docs/projektfuehrung/FABLE_UEBERGABE_2026-10-16c_eroeffnung.md = 7f767820b48fd139690ace13f8ae81e7
ja    md5 docs/projektfuehrung/UEBERGABE.md = a5a81d372183bd8127102917df8c1d61
ja    md5 docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md = 14db36f1fe8f03eebcd75a28dafa1f6e
Pruefungen: 5, NEIN: 0
rc 0
```

## Voraussetzungen (`v_voraussetzung.txt`, wörtlich)

```
ja    R56 (b)/0a-Datei: docs/projektfuehrung/FABLE_ANTWORT_2026-10-16c_r100c_elliott_abnahme.md verfolgt, gleich HEAD, md5 ebde5e999690f5c8ab0e1930ffb81783
ja    R56 (b)/0a-Datei: docs/projektfuehrung/FABLE_ANFRAGE_2026-10-16c_r100c_leseprotokoll_elliott_abnahme.md verfolgt, gleich HEAD, md5 4021b20db4e9b9899e040fa5b2236b35
ja    R56 (b)/0a-Datei: docs/projektfuehrung/FABLE_UEBERGABE_2026-10-16c_eroeffnung.md verfolgt, gleich HEAD, md5 7f767820b48fd139690ace13f8ae81e7
ja    R56 (b)/0a-Datei: docs/projektfuehrung/UEBERGABE.md verfolgt, gleich HEAD, md5 a5a81d372183bd8127102917df8c1d61
ja    R56 (b)/0a-Datei: docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md verfolgt, gleich HEAD, md5 14db36f1fe8f03eebcd75a28dafa1f6e
ja    Registerblock 16c: genau R104, Quelle, R105, Quelle im Codeblock (Z. 21–26)
ja    Register: 64 da, 65 nicht; R104/R105 0 Treffer
ja    Register endet mit genau einer Leerzeile
ja    Ort 62.1: Einfuegestelle nach Z. 12298 eindeutig, R104/R105 dort noch nicht genannt
ja    Ort 62.5 (c): Einfuegestelle nach Z. 12353 eindeutig, R104/R105 dort noch nicht genannt
ja    Ort 57.1: Einfuegestelle nach Z. 12001 eindeutig, R104/R105 dort noch nicht genannt
ja    Ort 61.1: Einfuegestelle nach Z. 12229 eindeutig, R104/R105 dort noch nicht genannt
ja    Ort 64.1: Einfuegestelle nach Z. 12432 eindeutig, R104/R105 dort noch nicht genannt
ja    R104 (a): Leseprotokoll docs/belege/TB-148/leseprotokoll.md md5 a1a324e02f06e2fc311ec26ca3b0ba74 (= Stand d9f8489)
info  Leseprotokoll zuletzt geaendert in Commit d9f8489
ja    R104 (a) Voraussetzung, elliott_wave: M3 ausserhalb multi_symbol_optimise.py: strategies/elliott_wave/equity_simulation.py (Z. 10); strategies/elliott_wave/backtest_elliott.py (Z. 41)
ja    R104 (a) Voraussetzung, t3_supertrend: M3 ausserhalb multi_symbol_optimise.py: strategies/t3_supertrend/equity_simulation.py (Z. 11); strategies/t3_supertrend/backtest_trend.py (Z. 42); strategies/t3_supertrend/regime_filter.py (Z. 59)
ja    R104 (a) Voraussetzung, rsi2_crypto: M3 ausserhalb multi_symbol_optimise.py: strategies/rsi2_crypto/equity_simulation.py (Z. 12); strategies/rsi2_crypto/backtest_rsi2.py (Z. 43)
ja    R104 (a) Voraussetzung, turtle_soup_crypto: M3 ausserhalb multi_symbol_optimise.py: strategies/turtle_soup_crypto/equity_simulation.py (Z. 13); strategies/turtle_soup_crypto/backtest_turtle_soup.py (Z. 44)
ja    R104 (a) Voraussetzung, volatility_breakout_crypto: M3 ausserhalb multi_symbol_optimise.py: strategies/volatility_breakout_crypto/equity_simulation.py (Z. 14); strategies/volatility_breakout_crypto/backtest_breakout.py (Z. 45); strategies/volatility_breakout_crypto/regime_filter.py (Z. 60)
ja    R104 (a) Voraussetzung, elliott_wave_stocks: M3 ausserhalb multi_symbol_optimise.py: strategies/elliott_wave_stocks/equity_simulation.py (Z. 15); strategies/elliott_wave_stocks/backtest_elliott.py (Z. 46)
ja    R104 (a) Voraussetzung, rsi2_mean_reversion: M3 ausserhalb multi_symbol_optimise.py: strategies/rsi2_mean_reversion/equity_simulation.py (Z. 16); strategies/rsi2_mean_reversion/backtest_rsi2.py (Z. 47)
ja    R104 (a) Voraussetzung, turtle_soup_stocks: M3 ausserhalb multi_symbol_optimise.py: strategies/turtle_soup_stocks/equity_simulation.py (Z. 17); strategies/turtle_soup_stocks/backtest_turtle_soup.py (Z. 48)
ja    R104 (a) Voraussetzung, volatility_breakout: M3 ausserhalb multi_symbol_optimise.py: strategies/volatility_breakout/equity_simulation.py (Z. 18); strategies/volatility_breakout/backtest_breakout.py (Z. 49)
ja    R105 (c) Code strategies/elliott_wave/elliott_wave_counter.py: Z. 192 end_time = times[i + 5]; 341 traded; 352–353 Schluessel end_time; 358–360 Kommentar; 361 Schranke; 363 traded.add(end_time)
ja    R105 (c) Code strategies/elliott_wave_stocks/elliott_wave_counter.py: Z. 192 end_time = times[i + 5]; 341 traded; 352–353 Schluessel end_time; 358–360 Kommentar; 361 Schranke; 363 traded.add(end_time)
ja    BACKLOG-Nachtrag: research/mtm_drawdown/grundlage.py Z. 65 liest <bot>_positionen.csv
ja    BACKLOG-Nachtrag: research/tb24_haltedauern/test_haltedauer_kern.py Z. 362 Pruefung 13 (Wache)
ja    BACKLOG-Nachtrag: docs/belege/TB-169/e_alt_vergleich.txt zeigt den Alt-Test rot (rc 1 vorher und nachher)
ja    BACKLOG-Nachtrag: docs/belege/TB-169/f_porcelain.txt nennt nur sich selbst (Selbstbezug)
ja    BACKLOG-Nachtrag: Index-Kopf Z. 3 nennt 0–64 und 12 023 Zeilen/459be94e (gemischter Stand)
ja    BACKLOG: grundlage.py und test_haltedauer_kern noch nicht genannt
ja    BACKLOG: Rang 1 (Stand TB-169) genau einmal
ja    Index: Zeile 64, Pflegezeile TB-169, Pflege-Anker je genau einmal; kein Abschnitt 16
ja    Dialog-Index: 16c noch nicht
ja    Journal: hoechste FF, naechste FG frei
Pruefungen: 35, NEIN: 0
rc 0
```

## Register 65 (Schritt R)

`WZ register 17.10.2026 801a055 docs/belege/TB-170/v_voraussetzung.txt --probe`: 6/0, rc 0. Danach der Eintrag: 9/0, rc 0, u. a. „R104, R105 mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)“ und „append-only bis auf die fuenf Marken“. Titel an **Z. 12451** (`r_daten.json`):

```
## 65. Fable 16c — Registerblock R104–R105 (TB-170)
```

Die fünf Marken nach `r_daten.json`, in Registerreihenfolge:

| Ort | Zeile | Kopf der Marke |
|---|---|---|
| 57.1 | 12003 | 57.1 R90 PRÄZISIERT durch R105 (65.2) |
| 61.1 | 12234 | 61.1 R98 ERGÄNZT durch R105 (65.2) |
| 62.1 | 12306 | 62.1 R100 ERGÄNZT durch R104 (65.1) |
| 62.5 (c) | 12364 | 62.5, Absatz (c) ERGÄNZT durch R104 (65.1) |
| 64.1 | 12446 | 64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R105 (65.2) |

numstat `801a055`..`7aecfe6`: `83	0	docs/VORREGISTRIERUNG_neuselektion.md` (5 × 3 Markenzeilen und 68 Zeilen Abschnitt 65). Ohne Marke wie vorgegeben: 56.4, 55.4, 54.2, 48.14, Abschnitt 10. R = `7aecfe6`.

## Schritt K

| Schritt | Beleg | rc |
|---|---|---|
| `registerkopie.py` | `k_registerkopie.txt` | 0 |
| `registerkopie.py --abschnitte` | `k_abschnitte.txt` | 0 |
| `registerkopie.py --pruefen` | `k_pruefen.txt` | 0 |
| `c2_index_zeilen.py 801a055 7aecfe6` | `k_index_zeilen.txt` | 0 |
| `WZ index 801a055 17.10.2026` | `k_index.txt` | 0 |
| `WZ handfelder k_handfelder.json` | `k_handfelder.txt` | 0 |
| `dialog_index.py --handfelder …` | `k_dialog_index.txt` | 0 |
| `dialog_index.py --pruefen` | `k_dialog_pruefen.txt` | 0 |

65 liegt in T6 (Abschnitte 58–65, 93 188 B ≤ 240 000). Keine neue Teildatei, neue Abschnittskopie `REGISTER_KOPIE_ABSCHNITT_65.md` (13 725 B). Bodies aneinander 1 203 527 B, sha256 `08b072674617cbf7…`, BYTEGLEICH mit dem Register am `7aecfe6`. Zeilenangaben: 466 umgeschrieben, davon 7 geändert, weil die Marken die Zeilen nach 57.1 verschieben. Index: Kopf 0–65, Zeile 65 (T6), neuer Abschnitt 16 mit den fünf Marken, Pflegezeile TB-170. Dialog-Index: 16c eingetragen, 66 von 66 Zeilen mit allen sechs Feldern (offen 13, ohne Registertext 13, registriert 40). K = `c602a2f`.

## BACKLOG und Journal

`WZ kennung` meldet „Kennung FG (hoechste FF)“. `WZ backlog 17.10.2026 FG` hängt an Rang 1 an:

- Register 65 mit TB-170.
- **Handelscode, eigener Auftrag, vor dem Tag:** R105 (c) Weg 1 bei `elliott_wave` und `elliott_wave_stocks`. Weg 2 trägt am Code nicht (65.3 (c)); bei R105 (d) `t3_supertrend` ist nichts entschieden.
- Nachträge:
  - `research/mtm_drawdown/grundlage.py` Z. 65 liest `<bot>_positionen.csv`.
  - Der Alt-Test `test_haltedauer_kern.py` ist in Prüfung 13 rot.
  - Der Kopf von `REGISTER_INDEX.md` mischt Stände.
  - `f_porcelain.txt` bezieht sich selbst ein (TB-166/TB-169).

Der Journal-Block `docs/belege/TB-170/a_block.md` steht vor `## Wiederkehrende Lehren`. Belege: `a_*.txt`.

## Offen

- **R105 (c) Weg 1** (Handelscode, eigener Auftrag mit Bau-Helfer und frischem Gegenleser): den Fall nach R90 (g) auf dem Test-Snapshot herbeiführen, mit Gegenprobe nach 40.7.
- **R105 (d)** `t3_supertrend`.
- **Vor der Neuerzeugung der Listen:** R102 (d) und R92 (c)/R86 (e).
- **Index-Kopf:** Die Berichtigung selbst steht aus, sie ist nur im BACKLOG vermerkt.
- **Zur Kenntnis an Fable mit der nächsten Anfrage:** R105 (c) Weg 2 trägt am Code nicht. Der Schlüssel von `traded` ist `end_time` der Welle, ohne Schranke würde dieselbe Welle verdrängt, keine andere (65.3 (c)).

## Abweichungen

Keine vom Auftrag. Beobachtungen:

- Die Commit-Nachrichten tragen unter der vorgegebenen ersten Zeile die Zuschreibungszeilen (Co-Authored-By, Claude-Session), wie in den bisherigen TB-Commits.
- `c2_index_zeilen.py` meldet diesmal 7 geänderte Zeilenangaben (TB-169: 0). Das ist erwartet, weil die Marken in 57.1, 61.1, 62.1 und 62.5 die nachfolgenden Zeilen um je 3 verschieben.

## In einfacher Sprache

Die neue Antwort des Verfahrensprüfers liegt jetzt mit Anfrage und Übergabe im Repo, und ihre zwei Regeltexte stehen wortgleich als neuer Abschnitt 65 im Register. An fünf älteren Stellen weist ein kurzer Vermerk auf die neuen Regeln hin, sonst blieb das Register unverändert. Die Messungen vorab haben bestätigt, was die neuen Regeln voraussetzen. Nur ein vorgeschlagener zweiter Prüfweg für die beiden Elliott-Bots passt nicht zum Code, deshalb steht der erste Weg jetzt als eigener Code-Auftrag in der Aufgabenliste. Es lief nichts auf Kursdaten, und kein Handelscode wurde geändert.
