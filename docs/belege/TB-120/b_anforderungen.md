# TB-120 B — Anforderungen an die zwei Erzeuger, aus dem Register gelesen

Register `docs/VORREGISTRIERUNG_neuselektion.md`, sha256 `18e39ee2…` (10 347 Zeilen, unverändert seit `1e11457`),
Ketten über `docs/projektfuehrung/REGISTER_INDEX.md`. Nur gelesen.

**Schreibweise.** Erzeuger: **L** = Listen-Erzeuger (Signalpfad, neun Trade-Listen, 40.6/46.3), **Z** =
Zellen-Erzeuger (Plan-Punkt 10, `zellen.csv`, `tagesreihen/`, `herkunft.json`), **L+Z** = beide. Kurzzitate
stehen zeichengleich in „…“; Hervorhebungen (`**`) des Registers sind im Zitat weggelassen, sonst nichts. Jedes
Zitat ist maschinell gegen das Register geprüft (`b_zitate_pruefen.py`, Ausgabe `b_zitate_pruefen.txt`).
**„vor dem Tag“** heisst hier: muss am Tag-Commit gebaut bzw. (bei L) gelaufen sein. Wo die Fundstelle dafür
nicht im Register, sondern in `PLAN_VOR_DEM_TAG.md` steht, ist das ausgewiesen („PLAN“).

Die Nummern `AN-nn` sind Nummern dieser Bestandsaufnahme, keine Registernummern. `AN-29` ist nicht vergeben (Nummernlücke beim Gliedern, keine fehlende Zeile); 61 Zeilen.

## 1. Listen-Erzeuger (L)

| Nr. | Anforderung | Fundstelle, Kurzzitat | Erz. | vor dem Tag |
|---|---|---|---|---|
| AN-01 | Die neun Trade-Listen werden einmal auf dem registrierten Snapshot mit dem registrierten Code neu erzeugt. | 40.6 (Fable 24a): „vor dem Tag einmal auf dem registrierten Snapshot mit dem registrierten Code neu erzeugt“ | L | ja — dieselbe Stelle |
| AN-02 | Die Erzeugung läuft im Selektionsmodus mit den registrierten heutigen Parametern. | 40.6: „im Selektionsmodus, mit den registrierten heutigen Parametern“ | L | ja — 40.6 |
| AN-03 | Der Erzeuger steht unter 36.1: Ziel nur per Argument, Einmal-Schreibsperre, nie überschreiben. | 40.6: „durch einen Erzeuger unter 36.1 (`--ziel`, Einmal-Schreibsperre)“; 36.1 (2): „Er überschreibt nie, auch nicht mit identischem Inhalt.“ | L | ja — 40.6 |
| AN-04 | Ein vorhandenes Ziel beendet den Erzeuger mit 1 (Befund), nicht mit 2. | 36.1, Marke aus 36.5: „der Wert ist 1“ | L+Z | ja — mit 36.1 |
| AN-05 | Beleg je Liste: Hash, Snapshot-Hash, Commit, als Tatsachennotiz. | 40.6: „mit Beleg, je Liste Hash, Snapshot-Hash und Commit als Tatsachennotiz“ | L | ja — 40.6 |
| AN-06 | Der Parameterstand der Erzeugung wird als Tatsachennotiz zu 5.4 festgehalten (Hashes der Parameterdateien, Commit, Snapshot, Modus). | 40.6 (Folgerung TB-96 aus Fables „Unsicher“): „je Bot die Hashes der Parameterdateien, der Code-Commit, der Snapshot-Hash und der Modus“ | L | ja — 40.6 |
| AN-07 | *Registrierter Code* ist der Signalpfad (`run_backtest`), nicht die Zuteilung. | 41.1 A12: „nicht der Ausführungspfad (Zuteilung)“ | L | ja — mit AN-01 |
| AN-08 | Die Listen enthalten die gefundenen Trades mit `bot`, `symbol`, `entry_time` und den Feldern des Signalpfads. | 41.1 A12: „(`bot`, `symbol`, `entry_time`, dazu die Felder, die der Signalpfad ohnehin liefert)“ | L | ja — mit AN-01 |
| AN-09 | Keine Spalte `ausgefuehrt`, keine Kennzeichnung im Symbolfeld. | 41.1 A12: „ohne Simulationsspalte `ausgefuehrt` und ohne Kennzeichnung im Symbolfeld“ | L | ja — mit AN-01 |
| AN-10 | Das Format ist eine registrierte Feldliste; der Erzeuger schreibt genau diese Felder. | 41.1 A12: „Das Format wird als Feldliste registriert (Bauart 33.3), der Erzeuger schreibt genau diese Felder.“ | L | ja — mit AN-01 |
| AN-11 | Die Feldliste enthält `exit_time` und `haltedauer_balken`. | 41.2 B6/B7: „Die Feldliste der neuen Listen (24b A3) bekommt `exit_time` und `haltedauer_balken` ausdrücklich.“ | L | ja — mit AN-01 |
| AN-12 | Kein Werkzeug schreibt Kennzeichnungen in Felder, die der Laufcode liest. | 41.1 A9: „Kein Messwerkzeug schreibt Kennzeichnungen in Felder, die der Laufcode liest.“ | L | ja — mit AN-01 |
| AN-13 | Reproduzierbarkeitsnachweis: der Modus-Lauf, zweimal, bytegleich. | 40.6: „Der Reproduzierbarkeitsnachweis (23e) ist der Modus-Lauf selbst: zweimal, bytegleich.“ (bestätigt 41.1 A3) | L | ja — 40.6 |
| AN-14 | Herleitungen aus Trades verwenden gefundene Trades, nie ausgeführte. | 41.2 B1: „Herleitungen aus Trades verwenden gefundene Trades (Signalpfad), nie ausgeführte.“ | L | ja — B1 „vor dem Lauf“ |
| AN-15 | Bei `elliott_wave` greift „gefunden“ über die Ausführung (Kapitalschranke), nicht über eine Limitachse. | 41.3 C4: „Der Grundsatz greift dort über das zweite Wort im Registertext aus 24c“ | L | ja — Tatsachennotiz zu 5.4 |
| AN-16 | Die alten Listen (`78e2bc6`) bleiben als historischer Stand liegen. | 40.6: „Die alten Listen (`78e2bc6`) bleiben liegen als historischer Stand mit Tatsachennotiz.“ | L | ja — 40.6 |
| AN-17 | Die neuen Listen kommen als Punkt auf die Sperrliste. | 40.6: „und als Punkt auf die Sperrliste aufgenommen“ | L (Folge) | ja — 40.6 |
| AN-18 | `faltenplan.py` liest die neuen Listen über eine registrierte Pfadkonstante; der Pfad ist heute nicht registriert. | 40.6: „`faltenplan.py` liest sie über einen registrierten Pfad (Konstante, kein Schalter)“; 46.3: „Der Pfad der neuen Listen ist bis dahin nicht registriert (TB-114 B3).“ | L (Folge) | ja — 40.6 |
| AN-19 | `EINGEFROREN` wechselt mit der Neuerzeugung auf die neuen Listen; `herkunft.py` wird dafür geöffnet, nicht davor. | 46.3 R12: „Die Öffnung von `herkunft.py` dafür erfolgt mit der Neuerzeugung, nicht davor.“ | L (Folge) | ja — 46.3 |
| AN-20 | Danach: Faltenlänge je Bot aus den neuen Listen, Vergleich gegen 33.2 (gleich ⇒ Notiz, verschieden ⇒ Berichtigung). | 40.6: „aus den neuen Listen abgeleitet und gegen 33.2 verglichen“ | L (Folge) | ja — 40.6 |
| AN-21 | Danach: Deckel `t3_supertrend` (P95 + 1), Donchian-Untergrenze und Haltedauern für `messgroessen.py` aus den neuen Listen. | 41.3 C2: „Das 95. Perzentil der Haltedauer wird aus den gefundenen Trades gerechnet“; 41.2 B3: „aus `median_balken` der gefundenen Trades, nicht der ausgeführten“; 41.2 B6/B7: „`messgroessen.py` liest die Haltedauern aus der neuen Quelle (Konstante, unter dem Resolver)“ | L (Folge) | ja — 41.2 B1 „vor dem Lauf“ |
| AN-22 | Abbild des Faltenplans erst nach der Ableitung. | 40.6: „Das Abbild wird nach der Ableitung erzeugt, nicht vorher“ | L (Folge) | ja — Plan-Punkt 7 |

## 2. Beide Erzeuger (L+Z) — Weg, Nachweis, Modus

| Nr. | Anforderung | Fundstelle, Kurzzitat | Erz. | vor dem Tag |
|---|---|---|---|---|
| AN-23 | Kein Rückfall auf Voreinstellungen unter dem Modus; fehlende Eingabe ⇒ 2 vor der Rechnung. | 41.1 A10: „Unter dem Selektionsmodus gibt es keinen Rückfall auf eingebaute Voreinstellungen“ | L+Z | ja — Registertext zu 5a/5e |
| AN-24 | Kurs- und Universumspfade nur über den Resolver. | 41.2 B5 (Fundstelle nach 42.1 D1): „Jedes Modul des Laufbereichs, das Kursdaten oder Universumsdateien liest, bezieht seine Pfade über den Resolver“ | L+Z | ja — Ergänzung zu 5a/5e |
| AN-25 | Ein Modus-Lauf ist ein Lauf unter dem Resolver; Hilfsordner tragen keinen Nachweisteil. | 41.3 C6: „ist kein Modus-Lauf und trägt keinen Nachweisteil (b)“ | L+Z | ja — Ergänzung zu 5e |
| AN-26 | Nachweis hat zwei Teile; ohne Leseprotokoll (b) ist er 2. | 41.2 B4: „Fehlt (b) oder zeigt es einen Zugriff ausserhalb, ist der Nachweis 2“ | L+Z | ja — Ersatz für 23e |
| AN-27 | Startprüfung Codeherkunft (Wurzel, Commit, Sauberkeit), Abbruch mit 2, Werte im Lese-Audit. | 19: „Wurzel, Commit und Sauberkeit werden im Lese-Audit protokolliert.“ | L+Z | ja (Code) — 19 |
| AN-28 | Wegwerfbaum-Muster ist im Modus unzulässig. | 19: „ist eine Testtechnik des Regelbetriebs und im Selektionsmodus unzulässig.“ | L+Z | ja (Code) — 19 |

## 3. Zellen-Erzeuger (Z)

| Nr. | Anforderung | Fundstelle, Kurzzitat | Erz. | vor dem Tag |
|---|---|---|---|---|
| AN-30 | Der Zellen-Erzeuger schreibt `zellen.csv`, `tagesreihen/` und `herkunft.json`. | 46.3 R12: „der `zellen.csv`, `tagesreihen/` und `herkunft.json` schreibt“ | Z | ja (Code) — PLAN Stufe V Nr. 10 vor Stufe VI |
| AN-31 | `zellen.csv`: für jede Zelle des Rasters genau eine Zeile. ⚠️ Mengenbegriff siehe `b_offen.md` O-1. | 45.5 R5 (b): „`zellen.csv` enthält für jede Zelle des Rasters genau eine Zeile“ | Z | ja (Code) — R5 ist Abnahme |
| AN-32 | Eine Zelle ohne Trades trägt die Nullzeile, nie nichts. | 45.5 R5 (b): „eine Zelle ohne Trades trägt die Nullzeile“; 43.2 43-7: „Der Erzeuger schreibt für eine Zelle ohne Trades die Nullzeile, nie nichts.“ | Z | ja (Code) — R5 |
| AN-33 | Eine fehlende Zeile ist ein Befund über den Erzeuger. | 45.5 R5 (b): „Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang.“ | Z | ja (Code) — R5 |
| AN-34 | Null Trades ⇒ Ergebnis schreiben, Ausgang 0; unter dem Modus `exit()` ohne Ergebnis ⇒ 2. | 43.2 43-7: „Unter dem Modus endet ein `exit()` ohne geschriebenes Ergebnis mit 2“ | Z | ja (Code) — 43-7 |
| AN-35 | `herkunft.json`: gerechneter Datenstand-Hash, Commit und `herkunft.register()`. | 46.7 R16 (b): „den mit `herkunft.datenstand(<Snapshot-Datenordner>)` gerechneten Datenstand-Hash, nicht den im MANIFEST notierten“ | Z | ja (Code) — R5 (d) |
| AN-36 | `herkunft.json` trägt zusätzlich das Feld `teile` aus `register()`. | 37.4 (Fable 22d Abschn. 3): „schreibt in `herkunft.json` auch das Feld `teile`“ | Z | ja (Code) — PLAN Stufe V Nr. 10 |
| AN-37 | `herkunft.json` je Bot, von `auswertung.py` geprüft (Datei da, Commit = Tag-Commit, Datenstand `d9449faf…`, Register-Hash, neun gleich); der Schreiber prüft sich nicht selbst. | 46.5 R14: „Der Schreiber von `herkunft.json` (Zellen-Erzeuger) prüft sich nicht selbst; der Auswerter prüft ihn.“ | Z | ja (Code) — R14 |
| AN-38 | Nach Einbau: Laufbereich enthält `herkunft.py`, `ARBEITSBAUM_PFADE` nachgezogen. | 45.5 R5 (a): „`ARBEITSBAUM_PFADE` ist danach nachgezogen (R4)“; 45.4 R4: „Die Liste wird vor dem Tag nachgezogen, nie durch ihn.“ | Z | ja — R4 |
| AN-39 | Lese-Audit: alle gelesenen Dateien mit Inhalts-Hash. | 17.4 (5e): „die Liste aller Dateien, die er gelesen hat, mit Inhalts-Hash“ | Z | ja (Code) — PLAN Stufe V Nr. 10 |
| AN-40 | Lauf gültig nur mit Audit, jede Datei im Manifest, Snapshot-Hash vor und nach gleich. | 17.4: „der Snapshot-Hash vor und nach dem Lauf identisch ist“ | Z | ja (Code) — 17.4 |
| AN-41 | Jeder Rasterpunkt auf jeder Selektionsfalte (Verfahren B). | 15.2 (RT 0): „Jeder Rasterpunkt wird auf jeder Selektionsfalte ausgewertet“ | Z | ja (Code) |
| AN-42 | Zellenmenge = Raster aus `registerdaten.py` samt Rasterbedingung; Faltennamen = Faltenplan, Bestätigung eingeschlossen, Bezeichner als Spanne. | `auswertung.py` Docstring/`lies_zellen` (Vertrag); 38.1: „die Spalte `falte` der Bestätigungszeile in `zellen.csv`“ | Z | ja (Code) — Vertrag, Abschnitt 12 |
| AN-43 | Tagesreihe = tägliche Netto-Mark-to-Market-Renditen des Kapitalpfads; flache Tage mit 0. | 15.3 (a) (RT 1a): „Flache Tage stehen mit Rendite 0 in der Reihe.“ | Z | ja (Code) |
| AN-44 | Falten-Sharpe aus täglichen Netto-Renditen, ohne Mindestzahl Trades; Streuung 0 ⇒ 0; √252 bzw. √365. | 15.3 (c) (RT 1c): „Es gibt keine Mindestzahl Trades je Falte.“ | Z | ja (Code) |
| AN-45 | Handelstag gehört zur Falte seines Datums; Positionen über Faltengrenzen werden nicht geschlossen. | 15.4 (a) (RT 2a): „Jeder Handelstag gehört zu der Falte, in die sein Datum fällt.“ | Z | ja (Code) |
| AN-46 | Trades zählen für die Falte ihres Einstiegstags. | 15.4 (b) (RT 2b): „Trades werden für die Zählung der Falte ihres Einstiegstags zugeordnet.“ | Z | ja (Code) |
| AN-47 | Kapital-Drawdown je Falte auf der täglichen MtM-Reihe (TB-30b Posten 2, im Erzeuger). | 24.2: „Der Kapital-Drawdown einer Falte für die Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe“; 11.2: „den Kapital-Drawdown noch nicht mitliefert“ | Z | ja — PLAN Posten 2 „Sperrbedingung“ |
| AN-48 | Der ereignisindizierte Drawdown wird berichtet, nicht bewertet. ⚠️ Ort siehe O-5. | 24.2: „Der ereignisindizierte Drawdown aus `equity_simulation.py` wird berichtet, nicht bewertet.“ | Z | ja (Code) |
| AN-49 | Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte, Startkapital, ohne offene Position. | 29.3: „Kein Einstieg liegt vor diesem Datum.“ | Z | ja (Code) |
| AN-50 | Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“ in allen neun Optimierern; Bericht mit drei Daten. | 29.4 mit 34.5: „wird in allen neun `multi_symbol_optimise.py` eingebaut“ | Z (TB-30b Posten 5) | ja — PLAN Posten 5 |
| AN-51 | Horizont je Bot als absolutes Datum, für alle Symbole gleich (`entry_cutoff`, Aktien-Bots). | 26.2: „Es gilt für alle Symbole des Bots gleich“ | Z (TB-30b Posten 4) | ja — PLAN Posten 4 |
| AN-52 | Zwei Achsen durchreichen: `SMA_TREND_PERIOD` (`rsi2_mean_reversion`), `BB_SQUEEZE_PERCENTILE`/`BB_LOOKBACK` (beide Breakout-Bots). | 11.3: „ist in `backtest_rsi2.py` eine Konstante und muss Parameter werden“; „stehen in `live_params.py`, aber nicht im Optimierer“ | Z (TB-30b Posten 3) | ja — PLAN Posten 3 |
| AN-53 | Regimewache vor dem Lauf eingebaut. | 11.1: „Solange er es nicht ist, darf der Lauf nicht starten.“ | Z (TB-30b Posten 1) | ja — Sperrlisten-Schlusssatz |
| AN-54 | Symbole ohne Historie in einer Falte tragen 0 Trades und 0 Rendite. | 15.5 (a) (RT 3a): „Symbole ohne Historie in einer Falte tragen 0 Trades und 0 Rendite bei.“ | Z | ja (Code) |
| AN-55 | Eine Falte zählt, wenn der Loader mindestens ein Symbol handelbar macht; keine Mindest-Symbolzahl. | 16.7 (a): „Es gibt keine Mindest-Symbolzahl je Falte.“ | Z (Posten 6) | ja — PLAN Posten 6 |
| AN-56 | Bericht je Bot und Falte: Symbolzahl, Anteil, ausgelassene Symbole mit Grund, Faltenkohärenz. ⚠️ Ort siehe O-7. | 16.7 (d): „Liste der ausgelassenen Symbole mit Grund“ | Z? (Posten 6) | ja — PLAN Posten 6 |
| AN-57 | Embargo 2d: Bedingung am Bestand mit Deckel; für den Gewinner auf dessen eigenen Positionen. ⚠️ Ort siehe O-6. | 41.3 C3: „für den Gewinner auf dessen eigenen simulierten Positionen“ | Z? (Posten 6) | ja — PLAN Posten 6 |
| AN-58 | Kill-Test-Berichtswerte (beste Falte, bestes Symbol, fünf beste Trades) für den Plateau-Gewinner. ⚠️ Ort siehe O-3. | 22.2: „Der Lauf berichtet je Bot für den Plateau-Gewinner drei Werte“ | ? | ja — Abschnitt 22 „(vor dem Tag)“ |
| AN-59 | Bootstrap mit berechneter, protokollierter Blocklänge L aus der medianen Haltedauer. ⚠️ Ort siehe O-4. | 15.3 (b) (RT 1b): „L wird berechnet und protokolliert; es ist kein Eingabewert.“ | ? | ja (Code) |
| AN-60 | Kosten 0,30 % und Fill-Konvention; Zuteilungskaskade mit `SEED = 20260913` — gebunden, nicht neu zu bauen. | Sperrliste Punkt 9 und 10 | Z (Import) | ja — Sperrliste |
| AN-61 | Wache: kein `multi_symbol_walk_forward.py` im Lauf. | PLAN, TB-30b Posten 8: „nötig ist nur eine Wache, dass keiner im Lauf aufgerufen wird“; Register 15.1: „werden später ersetzt, nicht umgestellt“ | Z | ja — PLAN Stufe V Nr. 10 („enthält die Wache“) |
| AN-62 | Benchmark-Tagesreihe `benchmark_tagesreihen/<markt>.csv` liegt neben den Rohergebnissen. ⚠️ Schreiber und Menge siehe O-8. | `auswertung.py` Docstring (Vertrag) und `lies_benchmark` | ? | ja (Vertrag) |
