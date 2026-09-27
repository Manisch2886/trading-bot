# TB-120 B — Offene Stellen: zwei Wortlaute oder eine unklare Anforderung

Nicht entschieden. Je Stelle die Wortlaute zeichengleich (Hervorhebungen `**` weggelassen, geprüft mit
`b_zitate_pruefen.py`), danach, was offen ist. Ohne Neigung.

## O-1 — Wie viele Zeilen hat `zellen.csv`? (zu AN-31)

- Register 45.5 R5 (b): „`zellen.csv` enthält für jede Zelle des Rasters genau eine Zeile; die Zeilenzahl ist gleich der Zahl der Zellen“
- `research/vorregistrierung/auswertung.py`, Docstring (Datenvertrag): „genau eine Zeile je (Zelle x Falte), fuer ALLE Falten des Faltenplans, Bestaetigungsperiode eingeschlossen.“

**Offen:** R5 (b) zählt Zellen, der Vertrag zählt Zelle × Falte. `lies_zellen` verlangt je Zelle genau die Faltenliste
des Plans. Heisst *genau eine Zeile* in R5 *je Zelle und Falte*?

## O-2 — Die „leere Trade-Liste“ der Nullzeile: in welcher Datei? (zu AN-32)

- Register 45.5 R5 (b): „(Sharpe 0 nach Registertext 1c, leere Trade-Liste)“
- Register 43.2, 43-7: „schreibt dieses Ergebnis (leere Liste, Sharpe 0 nach 1c)“
- Vertrag (`auswertung.py`): drei Dateiarten je Bot (`zellen.csv`, `tagesreihen/<zelle_id>.csv`, `herkunft.json`),
  Pflichtspalten `zelle_id, falte, rolle, n_trades, netto_sharpe, netto_rendite_pct, kapital_drawdown_pct,
  mittlere_exposure`. Eine Trade-Liste je Zelle kommt im Vertrag nicht vor.

**Offen:** Gibt es je Zelle eine Trade-Liste als Rohergebnis (Datei, Felder)? Daran hängen auch O-3 (fünf beste
Trades, bestes Symbol) und O-6 (Positionen des Gewinners).

## O-3 — Kill-Test-Berichtswerte: Erzeuger oder `auswertung.py`? (zu AN-58)

- Register 22.2: „Der Lauf berichtet je Bot für den Plateau-Gewinner drei Werte“ (beste Falte, bestes Symbol, fünf
  beste Trades), ohne Schwelle, vor dem Tag registriert.
- Gemessen: `auswertung.py` enthält dazu nichts (0 Treffer für `kill`, `Ertragsanteil`; `e_schluss.txt`). `auswertung.py` steht auf der Sperrliste (Punkte 3, 5, 14). Die Werte *bestes Symbol* und *fünf
  beste Trades* brauchen Daten je Symbol bzw. je Trade, die der Vertrag nicht führt (O-2).

**Offen:** Wer rechnet die drei Werte — der Zellen-Erzeuger (für welche Zelle, wenn der Gewinner erst in
`auswertung.py` feststeht?) oder `auswertung.py` (eine Öffnung nach 37.3 mit Vertragserweiterung)?

## O-4 — Bootstrap: im Register „im Auswertungsskript“, im Code nirgends (zu AN-59)

- Register 15.3 (a): „Jedes Bootstrap-Intervall im Auswertungsskript wird auf der Reihe der täglichen Netto-Mark-to-Market-Renditen des Kapitalpfads gerechnet“
- Register 15.3 (b): „Mittlere Blocklänge L = max(mediane Haltedauer des Parametersatzes in Handelstagen, ⌈T^(1/3)⌉)“
- Gemessen: `research/vorregistrierung/*.py` enthält kein `bootstrap` (0 Treffer, `e_schluss.txt`). Der Vertrag führt keine mediane
  Haltedauer je Zelle.

**Offen:** Welche Grösse trägt ein Bootstrap-Intervall (Abschnitt 8)? Ist er Teil von `auswertung.py` (Öffnung)?
Liefert der Zellen-Erzeuger die mediane Haltedauer je Zelle in Handelstagen (neue Spalte)?

## O-5 — Welcher Drawdown steht in `kapital_drawdown_pct`, und wo steht der andere? (zu AN-47, AN-48)

- Register 24.2: „Der Kapital-Drawdown einer Falte für die Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe des Kapitalpfads gerechnet (1a)“
  und „Der ereignisindizierte Drawdown aus `equity_simulation.py` wird berichtet, nicht bewertet.“
- `beispieldaten.py`, Docstring: „der Kapital-Drawdown einer Falte steht in `zellen.csv`, weil er im echten Lauf aus `equity_simulation.py` kommt“

**Offen:** Nach 24.2 ist `kapital_drawdown_pct` der MtM-Drawdown; der Docstring von `beispieldaten.py` beschreibt den
Stand vor 24.2. Der Vertrag hat eine einzige Drawdown-Spalte. Wo steht der ereignisindizierte Drawdown (eigene
Spalte, von `auswertung.py` ignoriert, oder anderswo)?

## O-6 — Embargo 2d und Beginn der Bestätigungsperiode (zu AN-57)

- Register 16.6 (2d): „Die Bestätigungsperiode eines Bots beginnt am ersten Handelstag nach Go-Live, an dem keine vor Go-Live eröffnete Position dieses Bots mehr offen ist.“
- Register 41.3 C3: „Die Bedingung wird im Selektionslauf für den Gewinner auf dessen eigenen simulierten Positionen ausgewertet“
- Register 15.6, Faltenliste: „2026-01-01 … 2026-09-01“; dazu „Der Go-Live-Schnitt bleibt 2026-09-01, ausschliesslich“
- Register 38.1: „die letzte Falte heisst die Spanne `2026-01-01/2026-09-01`“
- Gemessen: `faltenplan.py` bildet die Bestätigungsfalte ab ihrem Kalenderbeginn; `auswertung.py::bestaetigungsperiode`
  liest die Zeile dieser Falte und kennt keine Positionen.

**Offen:** (1) Wo wird die Bedingung ausgewertet — im Zellen-Erzeuger (je Zelle, weil der Gewinner dort unbekannt
ist), in einem Schritt nach `auswertung.py` oder in `auswertung.py`? (2) Wie verhält sich „nach Go-Live“ (16.6) zur
Spanne `2026-01-01/2026-09-01` bei einem Go-Live-Schnitt `2026-09-01`?

## O-7 — Bericht nach 3b (d): Ladezeit-Werte und Faltenkohärenz (zu AN-56)

- Register 16.7 (d): „Berichtet je Bot und Falte, ohne dass ein Kriterium daran hängt“ — Symbolzahl, Anteil,
  Auslassungen mit Grund, und „nach dem Lauf die Faltenkohärenz“.
- Register 16.11, Zeile 7: „Der spätere Auswerter tut es noch nicht“
- Gemessen: `auswertung.py` 0 Treffer für `spearman`, `kohaerenz`, `ausgelassen` (`e_schluss.txt`).

**Offen:** Symbolzahl, Anteil und Auslassungen entstehen beim Laden (Erzeuger). Die Faltenkohärenz braucht die
Rangfolge aller Zellen, ist also ein Auswertungsschritt; `auswertung.py` ist gesperrt. Wo steht sie?

## O-8 — Benchmark-Tagesreihe: wer schreibt sie, und je Markt oder je Bot? (zu AN-62)

- Vertrag (`auswertung.py`): `<wurzel>/benchmark_tagesreihen/<markt>.csv`, „das gleichgewichtete point-in-time-Universum, taeglich.“ — Grundlage der Beta-Bereinigung und des Zufalls-Timing-Tests.
- Register 23.3 (3b (c)): „Der Benchmark einer Falte wird tagesgenau aus den Symbolen gebildet, die der Loader des Bots an diesem Tag handelbar macht“
- Register 46.3 nennt als Ausgaben des Zellen-Erzeugers nur `zellen.csv`, `tagesreihen/` und `herkunft.json`.

**Offen:** Wer schreibt `benchmark_tagesreihen/`? Gilt für die Beta-Bereinigung der Markt-Benchmark aus dem Vertrag
oder der Bot-Benchmark aus 23.3 (dort genannt für Drawdown-Nebenbedingung und Rang 3)?

## O-9 — Gilt 36.1 für die Rohergebnisse? (zu AN-03)

- Register 36.1 (1)/(2): „Kein Programm im Repo schreibt an einen Pfad, der auf der Sperrliste steht oder für sie bestimmt ist.“ und „Jeder Erzeuger einer solchen Datei schreibt einmalig“
- `PLAN_VOR_DEM_TAG.md`, Stufe V Nr. 10: „unterliegt der Schreibregel 36.1 von Anfang an“

**Offen:** `zellen.csv`, `tagesreihen/`, `herkunft.json` stehen nicht auf der Sperrliste. Der Plan unterstellt 36.1.
Genügt der Plan, oder braucht es einen Registersatz (z. B. „bestimmt“ im Sinn von 36.1)?

## O-10 — `haltedauer_balken`: Zählregel und Einheit (zu AN-11, AN-21)

- Register 41.2 B6/B7: „jede gefundene Trade-Zeile trägt `entry_time` und `exit_time`, die Haltedauer folgt daraus“
- Register 16.6: Deckel „13 Handelstage“ für `t3_supertrend` (4h-Balken); 41.2 B3: Donchian aus `median_balken`.
- Gemessen: `positionen_holen.py::kerzen_je_trade` zählt Kerzen „beide Enden eingeschlossen“ und schreibt `kerzen`,
  nicht `haltedauer_balken`.

**Offen:** Zählregel (Kerzen inklusive beider Enden wie `kerzen`, oder Differenz), Einheit (Balken des
Bot-Zeitrahmens) und die Umrechnung in Handelstage für den Deckel sind nicht registriert.

## O-11 — Neue Listen: Sperrlistenpunkt und/oder Gruppe `eingefroren`? (zu AN-17, AN-19)

- Register 40.6: „und als Punkt auf die Sperrliste aufgenommen“
- Register 45.3 R3: „gehören mit ihrem Hash in die Gruppe `eingefroren` des Abbilds“; 46.3 R12: bis zur Neuerzeugung
  bindet `EINGEFROREN` die heutigen Listen, „dann treten die neuen Listen an ihre Stelle“.
- Gemessen: Abbild `sperrliste_abbild_2026-09-26_tb117.json` führt 14 Punkte; keiner nennt die Listen.

**Offen:** Braucht es zusätzlich zur Gruppe `eingefroren` einen neuen Punkt in Abschnitt 10, oder ist 40.6 durch R3
erfüllt?

## Schon bei Fable, nur verwiesen

- **T117-6** (Anfrage 27c): Zellen-Erzeuger und Auswertung müssen am selben Commit laufen — Satz in die Reihenfolge am
  Tag? Betrifft den Zellen-Erzeuger unmittelbar.
- **T117-5** (Anfrage 27c): `herkunft.py` fehlt in `ARBEITSBAUM_PFADE`; berührt R5 (a) (AN-38).
- **T117-1** (Anfrage 27c): R14 ohne Modus (Lesart 46.9) — bestimmt, wie Tests ohne Modus mit Nullwerten in
  `herkunft.json` umgehen.
