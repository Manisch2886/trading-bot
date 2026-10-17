## FI — TB-172: Verfahrensmessung R102 (d) (Indikatorwerte vor dem Horizontbeginn, drei Aktien-Bots, nur das Ob) und R92 (c) (Form von open_time am Snapshot), nur Lesen
*Quelle: `docs/ERGEBNIS_TB-172_verfahrensmessung_r102d_r92c.md`, Commits `304ee71` (S0), `9bfa50c` (M, Messung und Belege), danach der Abgabe-Commit „TB-172 Abgabe: Ergebnis, BACKLOG, Journal FI“, der diesen Block enthält.*

**Quelle:** R102 (d) (Register Z. 12320), R92 (c) (Z. 12020), R86 (e) (Z. 11896), 27.2; Vorbild TB-148; BACKLOG Rang 1. Alles nur über `WZ` (Anhang A des Auftrags, sha256 `5f712255…`), das Quelltext per `ast` und Text liest und nichts startet. Freigabe: Karte des Betreibers im Chat 33, 17.10.2026, 15:21 („Freigeben“). Kein Registereintrag.

### Was gemessen ist
- 0a: Zweig `main`, HEAD = origin/main = `12a47f8`, genau zwei Einträge wie Soll, Karte gefüllt; Anhang mit Soll-sha256 (`Dateien 1`). S0 = `304ee71`, porcelain danach leer.
- V: 20 Prüfungen, NEIN 0, rc 0 (14 gelesene Dateien je md5 = Bau, Messbelege noch nicht da, R102 (d) und R92 (c) im Wortlaut, BACKLOG Rang 1 Stand TB-171, Journal FH, Snapshot da).
- M1 R102 (d), am Code erschlossen: `rsi2_mean_reversion: ja`, `turtle_soup_stocks: ja`, `volatility_breakout: ja`; Kontrolle `elliott_wave_stocks: nein (Zeilenschnitt Z. 119)` erkannt. Bei allen drei läuft die volle eingelesene Reihe in `compute_indicators`; `entry_cutoff` setzt in `run_backtest` nur `start_i`. Die beiden Erzeuger-Wege schneiden nicht an `open_time >=`. 10/0, rc 0.
- M2 R92 (c), am Snapshot `63e4b6c8…`, nur `open_time`: 150 Aktien-Dateien, 1 417 557 Zeilen, alle Klasse D (reines Kalenderdatum), M/Z/U/X je 0, doppelte Tage 0, sha256 150 von 150 = MANIFEST, MANIFEST und `sp500_top150.txt` decken sich. **R92 (c) erfüllt.** 2/0, rc 0.
- `WZ nachher` 18/0, rc 0: die 14 md5 unverändert, Urteilszeilen 3 und 1.

### Was offen bleibt
- An den Verfahrensprüfer: R102 (d) „ja“ bei allen drei Bots, Befund zu 28.6/R57 (laut Docstring von `rsi2_mean_reversion` gewollter Vorlauf, „KEINE Kappung … vor der Indikator-Berechnung“).
- Zur Kenntnis: R102 (c) nennt bei `rsi2_mean_reversion` „Z. 106 vor Z. 112“ und einen Zeilenschnitt am Horizontbeginn; Z. 112 setzt aber nur `entry_cutoff`. TB-148 hatte `snapshots/` aus dem Lesen herausgehalten (27.1); R92 (c) verlangt die Messung dort, gelesen wurde nur `open_time`.
- R86 (e) für die Aktien-Bots: Form von open_time ist nach M2 erfüllt; ob R86 (e) damit geschlossen ist, entscheidet der Verfahrensprüfer. R105 (d) `t3_supertrend` unberührt.

### In einfacher Sprache
Vor dem Neuerzeugen der Trade-Listen wurden zwei Dinge nur durch Lesen geprüft. Erstens: Die drei Aktien-Bots RSI-2, Turtle Soup und Volatility Breakout berechnen ihre Kennzahlen auch aus Kurstagen vor dem Beginn ihres Zeitraums. Erst ab dem Beginn dürfen sie handeln. Der Elliott-Aktien-Bot schneidet die Tage davor dagegen ab, und das Werkzeug hat diesen Unterschied erkannt. Ob das so bleiben soll, ist eine Frage an den Prüfer. Zweitens: In allen 150 Aktien-Kursdateien des eingefrorenen Datenstands steht das Datum als reiner Kalendertag, ohne Uhrzeit und ohne Zeitzone. Damit ist diese Bedingung erfüllt. Es wurde kein Kurs angesehen und nichts geändert.

*Geschrieben 17.10.2026 von der Mac-Sitzung TB-172. Quellenvermerk: siehe Kopf.*
