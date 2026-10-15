## EZ — TB-163: Register 59 (Tatsachennotiz TB-162) und E-6 Horizont je Bot aus faltenplan.HORIZONTBEGINN
*Quelle: `docs/ERGEBNIS_TB-163_register59_posten4_horizont.md`, Commits `cff0de3` (S0), `35dae90` (N), `639044c` (K), `11a267f` (E), F = der Abgabe-Commit „TB-163 Abgabe: Ergebnis, BACKLOG, Journal EZ“, der diesen Block enthält.*

**Quelle:** Am Registerende steht Abschnitt 59 mit der Tatsachennotiz aus `docs/ERGEBNIS_TB-162_wf_kapital_dd.md` Z. 199–232, zeichengleich und nur angehängt; Kopien, Index und Dialog-Index sind nachgezogen. In den vier Aktien-Optimierern (`elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`) kommt das Fenster jetzt aus `faltenplan.horizontbeginn(<bot>)` (19.09.2016) statt aus `open_time.max() - RECENT_YEARS_ONLY` — eingesetzt vom Werkzeug `tb163_werkzeug.py e6` aus dem Auftrag, Einzelfreigabe nach 37.3 durch die Betreiberkarte vom 15.10.2026, 18:24.

### Was gemessen ist
- 0a: Zweig `main`, HEAD `8517c5f`, vier Einträge wie Soll; Werkzeug und Probe sha256 wie Soll.
- V: 18 Prüfungen, NEIN 0, rc 0.
- N: Probe und Eintrag rc 0; 59 ab Z. 12112; numstat Register 41/0.
- K: alle sechs Schritte rc 0; 59 in T6 (Abschnitte 58–59, 23 496 B), keine neue Teildatei; Kopien bytegleich; Index 0–59; Dialog-Index 61/61.
- E: `e6 --probe` und `e6` rc 0, sha256 nachher gleich dem Soll aus dem Bau; Probe auf synthetischen Kursen 34 von 34, rc 0, rund 5 s unter Python 3.9.6; `r81d` 14 Prüfungen, NEIN 0: „R81 (d) Voraussetzung: erfuellt“.
- Eine `INFO`-Zeile: `volatility_breakout` `[tz UTC] run_backtest` wirft TypeError in `backtest_breakout.py` (nicht E-6, unverändert, nicht gezählt).

### Was offen bleibt
- Der Hash-Übergang nach 37.3 steht nur als Entwurf im Ergebnis (`docs/belege/TB-163/e_uebergang.md`); Registereintrag und neues Abbild unter neuem Namen folgen in einem eigenen Auftrag.
- Befunde ausserhalb von E-6: die Aufnahme eines Symbols (`MIN_HISTORY_DAYS`) hängt weiter vom Dateiende ab; `buy_and_hold_benchmark.py` (rsi2, turtle, vb) bildet `cutoff` weiter aus `.max()`; `import faltenplan` zieht seine Importkette in den Optimierer-Prozess; `backtest_breakout.py` Z. 211 mit tz-behaftetem `open_time`.

### In einfacher Sprache
Die Messung aus TB-162 steht jetzt wortgleich im Register. Die vier Aktien-Optimierer rechnen ihr Zehnjahresfenster nicht mehr vom letzten Kurstag jeder Datei aus, sondern alle vom selben Datum aus dem Register. Geprüft wurde das nur mit erfundenen Kursreihen; kein Optimierer lief.

*Geschrieben 15.10.2026 von der Mac-Sitzung TB-163. Quellenvermerk: siehe Kopf.*
