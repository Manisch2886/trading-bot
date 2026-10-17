# ERGEBNIS TB-172 — Verfahrensmessung R102 (d) (Indikatorwerte vor dem Horizontbeginn, drei Aktien-Bots, nur das Ob) und R92 (c) (Form von open_time am Snapshot; R86 (e) für die Aktien-Bots)

**Sitzung:** TB-172, Mac (Claude Code, Opus 5.5), 17.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-172_verfahrensmessung_r102d_r92c.md` · **Zweig:** `main`
**Commits:** `304ee71` (S0, Schritt 0) · `9bfa50c` (M, Messung und Belege) · der Abgabe-Commit „TB-172 Abgabe: Ergebnis, BACKLOG, Journal FI“, der dieses Ergebnis enthält · danach „TB-172 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-172/` · **Journal:** FI · **Kein Abbruch.** · **Kein Registereintrag.**

## Kurz

Zwei Messungen, beide nur durch Lesen. Das Werkzeug `tb172_werkzeug.py` (sha256 `5f712255…` wie Anhang A) liest Quelltext per `ast` und Text; es importiert und startet kein Programm des Repos. **M1 (R102 (d)):** `rsi2_mean_reversion`, `turtle_soup_stocks` und `volatility_breakout` bilden ihre Indikatorwerte **aus Zeilen vor dem Horizontbeginn**, Urteil je Bot „ja“. Die Kontrolle `elliott_wave_stocks` (Zeilenschnitt E-6/TB-163) wurde als „nein“ erkannt. **M2 (R92 (c)):** Am Snapshot `63e4b6c8…` steht `open_time` in 150 von 150 Aktien-Tagesreihen als reines Kalenderdatum (1 417 557 Zeilen, alle Klasse D). Es gibt keine Zone, keine Uhrzeit und keinen doppelten Tag, und sha256 stimmt 150 von 150 mit dem MANIFEST. **R92 (c) ist erfüllt.** Gelesen wurde nur das Feld `open_time`, kein Kurs. Die 14 md5 der gelesenen Dateien sind vor und nach der Messung gleich. `data/` wurde nicht berührt, es gab keine Neuerzeugung der Listen, kein Live und keinen Broker.

## Schritt 0

`git status --porcelain` zeigte genau die zwei Soll-Einträge (`docs/belege/TB-172/0a_status.txt`). HEAD und origin/main standen auf `12a47f89bb458aacf690a2ae0d6a708bbea1935f`, Zweig `main`, die Karte war gefüllt; letzte Zeile `0a gut (2 Eintraege)`. Der Holbefehl lieferte `tb172_werkzeug.py 5f712255e6027c14b05a01bf807e29f4c22a4744ef81a59d6368c50067c2dd29` und `Dateien 1`. S0 = `304ee71`, gepusht, porcelain danach leer.

## Voraussetzungen (`v_voraussetzung.txt`, letzte Zeilen wörtlich)

```
ja    Messbelege m1/m2 noch nicht da
ja    Register: R102 genau einmal, (d) im Wortlaut
ja    Register: R92 genau einmal, (c) im Wortlaut
ja    BACKLOG Rang 1 genau einmal, Stand TB-171
ja    Journal: hoechste FH (naechste FI)
ja    Snapshot mit MANIFEST.json: snapshots/63e4b6c8bb71…
Pruefungen: 20, NEIN: 0
rc 0
```

Davor stehen 14 Zeilen „unveraendert seit dem Bau“: je eine md5 für die neun Bot-Dateien (Optimierer, Backtest-Modul, Equity-Simulation der drei Bots), den Optimierer von `elliott_wave_stocks`, die zwei Erzeuger-Dateien sowie `MANIFEST.json` und `config/sp500_top150.txt` des Snapshots.

## M1 — R102 (d), nur das Ob

Urteilszeilen und Kontrollzeile aus `m1_r102d.txt`, wörtlich:

```
URTEIL R102 (d) rsi2_mean_reversion: ja
URTEIL R102 (d) turtle_soup_stocks: ja
URTEIL R102 (d) volatility_breakout: ja
KONTROLLE elliott_wave_stocks: nein (Zeilenschnitt Z. 119)
```

10 Prüfungen, NEIN 0, rc 0. Die Fundstellen stehen als Tabelle (Bot, Datei, Zeile, Rolle, Wortlaut) in `docs/belege/TB-172/m1_r102d.md`.

- **Belegt (Fundstellen):** Bei allen drei Bots liest `load_all_symbol_data` die volle CSV (`pd.read_csv`), setzt `entry_cutoff = horizontbeginn_ts(...)` und übergibt `data[symbol] = (…, entry_cutoff)` ohne Zeilenschnitt an `open_time >=`. `rsi2_mean_reversion` und `volatility_breakout` rufen `compute_indicators` schon beim Laden auf, alle drei dann je Lauf in `get_trades_for_symbol`. In `run_backtest` setzt `entry_cutoff` nur `start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))` (rsi2 Z. 131, turtle_soup Z. 122, breakout Z. 172). Bei `elliott_wave_stocks` steht Z. 119 `df = df[df["open_time"] >= cutoff]` vor der Übergabe Z. 121. Die Erzeuger-Wege schneiden nicht am Horizontbeginn: `positionen_holen.py::lesesicht_an` (Z. 290) schneidet nur am Schnitt (`_vor_schnitt`), und `bot_lauf.py::_schranke_je_symbol` (Z. 125) gibt `df` unverändert weiter.
- **Erschlossen am Code (nicht durch Lauf):** Die Indikatorwerte der drei Bots stützen sich auf Zeilen vor dem Horizontbeginn, gehandelt wird erst ab `start_i`. Der Docstring in `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` Z. 75–79 nennt das ausdrücklich: „KEINE Kappung auf RECENT_YEARS_ONLY vor der Indikator-Berechnung … entry_cutoff filtert nur die generierten TRADES“. Das habe ich in dieser Sitzung selbst nachgelesen.
- **Offen:** Die Wirkung auf 28.6/R57 ist hier nicht entschieden. Sie geht als Frage an den Verfahrensprüfer.

## M2 — R92 (c), nur die Form

Summen- und Urteilszeile aus `m2_r92c.txt`, wörtlich:

```
Summe: Dateien 150, Zeilen 1417557, D 1417557, M 0, Z 0, U 0, X 0, doppelte Tage 0
URTEIL R92 (c): erfüllt (150 von 150 Dateien: open_time Kalenderdatum, ohne Zone, ohne verschiebende Uhrzeit; D 1417557, M 0)
```

2 Prüfungen, NEIN 0, rc 0 (MANIFEST: 150 Aktien-Tagesreihen, Art `Kursdatei`; sha256 je Datei = MANIFEST, 150 von 150).

- **Belegt (Zählung):** Die Tabelle je Datei steht in `docs/belege/TB-172/m2_r92c.md`. Abweichungen je Datei gibt es keine (Form „ja“ bei 150 von 150). Der Abgleich mit `config/sp500_top150.txt` ergibt „nur im MANIFEST []“ und „nur in der Liste []“.
- Gelesen wurde je Zeile nur das Feld `open_time` mit dem `csv`-Modul der Standardbibliothek. Kein Kurs wurde gelesen, ausgegeben oder genannt.

**R86 (e) für die vier Aktien-Bots, Stand nach M2:** Die Form von `open_time` ist für jede Aktien-Tagesreihe des Snapshots erfüllt. Diese Reihen nutzen alle vier Aktien-Bots (`elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`). Ob R86 (e) damit für sie geschlossen ist, entscheidet der Verfahrensprüfer.

`WZ nachher` (`m_nachher.txt`): 18 Prüfungen, NEIN 0, rc 0. Die 14 md5 sind unverändert, beide Belege enden mit `rc 0`, und es gibt 3 bzw. 1 Urteilszeile. M = `9bfa50c`, gepusht.

## BACKLOG und Journal

`WZ kennung` meldet „Kennung FI (hoechste FH)“. `WZ backlog 17.10.2026 FI` hängt den TB-172-Stand an Rang 1 an: beide Urteile und den Hinweis, dass die Befunde als Frage an den Verfahrensprüfer gehen. Der Journal-Block `docs/belege/TB-172/a_block.md` steht vor `## Wiederkehrende Lehren`. Belege: `a_*.txt`.

## Befunde für den Verfahrensprüfer (nur gemeldet, nicht entschieden)

1. **R102 (d) „ja“ bei allen drei Bots** (`rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`): Die Indikatorwerte werden aus Zeilen vor dem Horizontbeginn gebildet, gehandelt wird erst ab dem Horizontbeginn. Bei `rsi2_mean_reversion` ist das laut Docstring der gewollte Vorlauf (SMA(200)). Das ist ein Befund zu 28.6/R57. `elliott_wave_stocks` schneidet dagegen vor der Indikatorbildung (E-6/TB-163). Die vier Aktien-Bots verhalten sich hier also nicht gleich.
2. **R92 (c):** erfüllt, kein Befund.
3. **Zur Kenntnis (1):** R102 (c) (Z. 12320) nennt als Bauart „rsi2_mean_reversion, Z. 106 vor Z. 112“ und „der Zeilenschnitt am Horizontbeginn bleibt“. Am Code steht bei `rsi2_mean_reversion` Z. 112 aber kein Zeilenschnitt, sondern nur `entry_cutoff = horizontbeginn_ts(df["open_time"])`. Z. 106 ist die Prüfung `timespan_days < MIN_HISTORY_DAYS`. Der Docstring Z. 75–79 sagt „KEINE Kappung … vor der Indikator-Berechnung“. Das habe ich in dieser Sitzung selbst nachgelesen.
4. **Zur Kenntnis (2):** TB-148 hielt `snapshots/` aus dem Lesen heraus (Sichtschutz 27.1). R92 (c) verlangt die Messung am Datenbestand des Snapshots, nur die Form. Das Werkzeug las dort nur `open_time` und nennt keine Kurse. Gezählt hat es aber über alle Zeilen, also über den vollen Zeitraum jeder Datei.

## Offen

- **An den Verfahrensprüfer, mit der nächsten Anfrage:** Befund 1 (R102 (d), 28.6/R57) und die Punkte 3 und 4. Ausserdem die Frage, ob R86 (e) für die Aktien-Bots mit M2 geschlossen ist.
- **R105 (d)** `t3_supertrend` bleibt unberührt.
- Die Neuerzeugung der Listen (R44) ist hier nicht begonnen.

## Abweichungen

Keine vom Auftrag. Beobachtungen:

- Unter der vorgegebenen ersten Zeile tragen die Commit-Nachrichten die Zuschreibungszeilen (Co-Authored-By, Claude-Session), wie in den bisherigen TB-Commits.
- Vor dem M-Commit habe ich `git status --porcelain` zusätzlich angesehen, um den Satz der vorgemerkten Dateien zu prüfen (genau die acht Belege, nichts sonst).
- Neben dem Werkzeug habe ich `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` Z. 70–119 mit dem Lesewerkzeug angesehen, um Punkt 3 zu bestätigen. Ausgeführt wurde dabei nichts, und die md5 ist nach `WZ nachher` unverändert.

## In einfacher Sprache

Vor dem Neuerzeugen der Trade-Listen wurden zwei Dinge nur durch Lesen geprüft, ohne etwas zu rechnen. Erstens: Die drei Aktien-Bots RSI-2, Turtle Soup und Volatility Breakout berechnen ihre Kennzahlen (RSI, Donchian, Bollinger) auch aus Kurstagen vor dem Beginn ihres Zeitraums. Erst ab dem Beginn dürfen sie handeln. Der Elliott-Aktien-Bot schneidet die Tage davor ab, und das Werkzeug hat diesen Unterschied richtig erkannt. Ob dieser Unterschied so bleiben soll, ist eine Frage an den Prüfer. Zweitens: In allen 150 Aktien-Kursdateien des eingefrorenen Datenstands steht das Datum als reiner Kalendertag, ohne Uhrzeit und ohne Zeitzone, die den Tag verschieben könnte. Diese Bedingung ist erfüllt. Kein Kurs wurde angesehen, und am Handelscode hat sich nichts geändert.
