# TB-120 D — Plan und Fragen

Grundlage: `b_anforderungen.md` (AN-01 … AN-62), `b_offen.md` (O-1 … O-11), `c_bestand.md`, `d_zellenzahl.txt`.
Die Fragen **F-1 … F-17** stehen an einem Ort: `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md`, Abschnitt „Für Fable“
(F-1 … F-11 = O-1 … O-11).
Alle Umfangsangaben sind **geschätzt** (K2o) — in Anzahl berührter Dateien und grob klein/mittel/gross, nicht in
Zeit (ARBEITSWEISE 6c). Kein Satz hier ist eine Erwartung über den Ausgang des Laufs (27.1).

## D1. Lückenliste

Alle Lücken sind **vor dem Tag** zu schliessen (Fundstellen in `b_anforderungen.md`). Sortiert nach Abhängigkeit;
„wartet“ nennt, woran.

| # | Lücke | AN | wartet auf |
|---|---|---|---|
| G1 | Durchreichung `SMA_TREND_PERIOD` (`rsi2_mean_reversion`) und Squeeze-Achsen (beide Breakout-Bots), Voreinstellung = heutiger Wert | AN-52 | — |
| G2 | Walk-Forward-Wache im Lauf (Posten 8) | AN-61 | — (Ort: Laufwrapper = Erzeuger, PLAN) |
| G3 | Herkunftsnotiz des Listen-Erzeugers um Parameterdateien-Hashes ergänzen | AN-06 | F-17 (welche Dateien) |
| G4 | Listen-Erzeuger nur Signalpfad: ohne `simuliere()`, ohne `ausgefuehrt`, ohne Kennzeichnung, mit `bot`, `haltedauer_balken`, registrierte Feldliste | AN-07–AN-12 | Registertext Feldliste; F-10 (Zählregel `haltedauer_balken`) |
| G5 | Registrierter Pfad der neuen Listen; Sperrlistenpunkt oder Gruppe | AN-17, AN-18 | F-11; Registerauftrag |
| G6 | Neuerzeugung der neun Listen im Modus, zweimal bytegleich, mit Leseprotokoll | AN-01, 02, 05, 13, 26 | G4, G5, F-13 (Reihenfolge zu Posten 4); Betreiberfreigabe für den Lauf |
| G7 | Folgen der neuen Listen: `EINGEFROREN` (Öffnung `herkunft.py`), `faltenplan.py::TB24_DATEN` (Punkt 2), zweite Konstante in `faltenplan_neun.py`, Faltenlänge gegen 33.2, Deckel `t3_supertrend`, Donchian-Untergrenze, Haltedauern in `messgroessen.py`, Abbild Faltenplan (Plan-Punkt 7) | AN-16–AN-22 | G6 |
| G8 | `entry_cutoff` je Bot aus `faltenplan.HORIZONTBEGINN` statt je Symbol (vier Aktien-Bots) | AN-51 | F-13 (verändert den Signalpfad der Listen) |
| G9 | Ausgeführte Positionen aus der Simulation (heute nicht zurückgegeben) | AN-43, AN-47, AN-57 | F-14 (Öffnung `shared/zuteilung.py`, Punkt 10) |
| G10 | Zellen-Kern: Zellparameter → Signalpfad → Simulation mit Limit → Positionen → tägliche MtM-Reihe → je Falte `n_trades` (Einstiegstag), Sharpe, Rendite, MtM-Drawdown, Exposure; Kapitalpfad ab 1. Januar erste Falte; nie `return None` | AN-41, 43–49, 54, 55; Posten 2 | G1, G8, G9, F-12 (Ort des Kerns) |
| G11 | Wache 29.4 („frühester Einstieg ≥ Beginn der ersten Falte“) mit Bericht der drei Daten | AN-50 | F-12 (Ort) |
| G12 | Schreiber: `zellen.csv`, `tagesreihen/`, `herkunft.json` mit gerechnetem Datenstand, Commit, Register-Hash, `teile`; Nullzeile; 36.1; Ausgänge 0/1/2; 43-7 | AN-30–AN-37 | Gerüst: — ; Zeilenbegriff F-1, Trade-Liste F-2 |
| G13 | Lese-Audit mit Inhalts-Hash, Manifest-Abgleich, Snapshot-Hash vor/nach, Startzeilen aus `paths.audit_zeilen()` | AN-26, AN-27, AN-39, AN-40 | — |
| G14 | Laufbereich neu messen, `ARBEITSBAUM_PFADE` nachziehen (`herkunft.py`, Erzeuger, ggf. `mtm_kern.py`) | AN-38 | T117-5 (Anfrage 27c) |
| G15 | Offene Orte: Benchmark-Tagesreihe, Kill-Test-Werte, Bootstrap, 3b (d), Embargo 2d, ereignisindizierter Drawdown | AN-48, 56–59, 62 | F-3–F-8 |
| G16 | Abnahme vor dem Tag ohne Ergebnis | R5, R16 | F-15 |
| G17 | Letztes Sperrlisten-Abbild nach der letzten Codeänderung (37.3) | — | alles oben |

## D2. Schnitt in Aufträge — Vorschlag

Neun Aufträge. Reihenfolge nach Abhängigkeit; E-1, E-4 (Gerüst) und E-2 (Register, sobald Fable geantwortet hat)
können nebeneinander vorbereitet werden, laufen aber nach der Regel „nie zwei Aufträge im selben Arbeitsbaum“
nacheinander.

| Auftrag | Gegenstand | Abnahme (R5/R16 und AN) | zu öffnende Dateien | Sperrliste / `EINGEFROREN` (37.3) | Umfang (geschätzt) |
|---|---|---|---|---|---|
| **E-1** TB-30b Posten 3 | G1: Achsen als Parameter mit heutigem Wert als Voreinstellung; Ausgabevergleich bytegleich je Bot mit Voreinstellungen (Bauart TB-90 B6) | AN-52; Ausgabe unverändert | `strategies/rsi2_mean_reversion/{backtest_rsi2,multi_symbol_optimise,equity_simulation}.py`; `strategies/volatility_breakout{,_crypto}/{multi_symbol_optimise,equity_simulation}.py` (Indikatoren heute ohne Squeeze-Argumente: `volatility_breakout` beim Laden, `volatility_breakout_crypto` in `get_trades_for_symbol`) | Punkt 11 (Commit von Simulation, Erkennung, Optimierern) — beauftragte Änderung vor dem Tag nach 37.3; kein Abbild-Pfad | mittel — 7 Dateien |
| **E-2** Registerauftrag | Antworten auf F-1 … F-17 als Registertext; Feldliste der neuen Listen (Bauart 33.3) samt `haltedauer_balken`; Pfadkonstante der neuen Listen; ggf. Sperrlistenpunkt (F-11) | Register-Einsetzskript, Zitate zeichengleich | `docs/VORREGISTRIERUNG_neuselektion.md`, `REGISTER_INDEX.md` | Register (kein Codepfad) | mittel |
| **E-3** Listen-Erzeuger umbauen | G3, G4: nur Signalpfad, Feldliste, `bot`, `haltedauer_balken`, Parameterdateien-Hashes; Kennzeichnung und `simuliere()` entfernt; Tests ohne Lauf auf Echtdaten | AN-03–AN-12 | `research/tb24_haltedauern/positionen_holen.py`, `alle_bots.py`; liest `research/exposure_messung/bot_lauf.py` (Laufbereich, nicht ändern) | keine | klein — 2–3 Dateien |
| **E-4** Listen neu erzeugen (Lauf) | G6: Modus-Lauf zweimal, `cmp`, Leseprotokoll; Tatsachennotiz Hash/Snapshot/Commit/Parameter | AN-01, 02, 05, 06, 13, 26 | neuer Zielordner (Pfad aus E-2) | Ziel wird Eingabe nach 23d | klein (Code), Laufzeit ungemessen; **Lauf braucht Freigabe** |
| **E-5** Folgen der Listen | G7: `herkunft.py::EINGEFROREN` tauschen; `faltenplan.py::TB24_DATEN` und `faltenplan_neun.py::TB24_DATEN`; `messgroessen.py` Haltedauerquelle; Faltenlänge gegen 33.2 (nur das Ob); Deckel und Donchian neu; neues Abbild; Plan-Punkt 7 | AN-16–AN-22; R12 | `herkunft.py`, `faltenplan.py`, `faltenplan_neun.py`, `messgroessen.py`, ggf. `ergebnisse/messgroessen.json`, Register | ⚠️ `herkunft.py` (Punkte 11/12), `faltenplan.py` (Punkt 2), `messgroessen.py` und `ergebnisse/messgroessen.json` in `EINGEFROREN`; `ergebnisse/faltenplan.json` (Punkt 2) bleibt; je Datei Hash-Übergang nach 37.3 | gross — Kaskade, mehrere Hash-Übergänge |
| **E-6** Posten 4 | G8: Horizont je Bot aus `faltenplan.HORIZONTBEGINN` in den vier Aktien-Optimierern | AN-51 | `strategies/{elliott_wave_stocks,rsi2_mean_reversion,turtle_soup_stocks,volatility_breakout}/multi_symbol_optimise.py` | Punkt 11 | klein — 4 Dateien; ⚠️ Reihenfolge zu E-4 nach F-13 |
| **E-7** Zellen-Kern | G9, G10, G11: Rückgabe der ausgeführten Positionen; Kern je Zelle mit MtM-Tagesreihe (Übernahme aus `mtm_kern.py`), Kapitalpfad ab erster Falte, Wache 29.4, Posten 2 | AN-41, 43–51, 54, 55; R5 (b) Nullzeile | `shared/zuteilung.py`; Ort des Kerns nach F-12 (neun `multi_symbol_optimise.py` oder neues Modul); `research/mtm_drawdown/mtm_kern.py` (Import oder Verlagerung) | ⚠️ `shared/zuteilung.py` = Punkt 10 (im Abbild mit Hash) → Hash-Übergang nach 37.3; neun Optimierer Punkt 11 | gross — 10–12 Dateien |
| **E-8** Zellen-Erzeuger: Schreiber, Audit, Wachen | G12, G13, G2: Schreiber gegen die Gestalt aus `beispieldaten.py`, `herkunft.json` mit `teile` und gerechnetem Datenstand, 36.1, Ausgänge; Lese-Audit; Startprüfung; Walk-Forward-Wache; Prüfung gegen `auswertung.py` auf synthetischen Eingaben | R5 (b), R16 (b), R14 (Prüferseite besteht), AN-30–AN-40, AN-61 | neues Modul (Pfad festzulegen); liest `herkunft.py`, `auswertung.py` (nur Import) | neues Modul wird nach R4 Laufbereich; `herkunft.py` nur gelesen | gross — neues Modul plus Tests |
| **E-9** Laufbereich und letztes Abbild | G14, G17: Laufbereich mit echtem Lauf-Typ messen, `ARBEITSBAUM_PFADE` nachziehen, neues Sperrlisten-Abbild | R5 (a), R4 | `shared/paths.py`, `shared/test_arbeitsbaum_laufbereich.py` | `paths.py` Laufbereich; Abbild neu unter neuem Namen (37.3) | klein — 2 Dateien plus Abbild |

Offene Orte aus G15 (F-3 bis F-8) können je nach Antwort in E-8 aufgehen oder eine Öffnung von `auswertung.py`
(Punkte 3/5/14) verlangen — dann ein zehnter Auftrag; Umfang erst nach der Antwort schätzbar.

## D3. Was ohne Fable gebaut werden kann — und was wartet

**Ohne Fable** (berührt keine offene Lesart; Freigabe des Betreibers nötig, weil Code):

- **E-1** (Posten 3): Die Achsen stehen im registrierten Raster (Abschnitt 2), 11.3 ist eindeutig; mit
  Voreinstellung = heutiger Wert ändert sich keine Ausgabe (vor und nach messbar, ohne Ergebnisgrösse zu lesen: `cmp`).
- **E-8 als Gerüst**: Schreiber mit Einmal-Sperre und Ausgängen, `herkunft.json` mit `teile` und gerechnetem
  Datenstand, Lese-Audit, Startprüfung, Walk-Forward-Wache — gegen die Gestalt aus `beispieldaten.py`, mit einem
  austauschbaren Kern, geprüft an synthetischen Eingaben. Offen bleiben dort nur die Stellen aus F-1, F-2, F-8.
- **E-3 zum Teil**: Entfernen von `simuliere()` und Kennzeichnung, Feld `bot` — A12 und A9 sind eindeutig. Die
  endgültige Feldliste und `haltedauer_balken` warten auf E-2 (F-10).

**Wartet auf Fable:**

| Auftrag | wartet auf |
|---|---|
| E-2 | F-1 … F-17 insgesamt |
| E-3 (Rest), E-4 | F-10, F-11, F-13, F-17 |
| E-5 | E-4 |
| E-6 | F-13 (Reihenfolge zur Listen-Erzeugung) |
| E-7 | F-12 (Ort des Kerns), F-14 (Öffnung `zuteilung.py`), F-5 |
| E-8 (Rest) | F-1, F-2, F-3, F-4, F-6, F-7, F-8, F-15 |
| E-9 | T117-5 (Anfrage 27c) |

**27c im Einzelnen:**

- **L2–L5 (T116-1 bis T116-5, Leiter 16.4):** berühren den Erzeuger **nicht**. Die Leiter ist Plan-Punkt L
  (Stufe IV, Budgetstufen nach dem Lauf); kein AN in B hängt daran.
- **T117-5 (`paths.py`, `ARBEITSBAUM_PFADE`):** berührt R5 (a) und damit E-9 unmittelbar. E-9 wartet.
- **T117-6 (Zellen-Erzeuger und Auswertung am selben Commit):** berührt E-8 (Reihenfolge am Tag), nicht den Bau.
- **T117-1 (R14 ohne Modus):** berührt die Tests von E-8 (Nullwerte ohne Modus), nicht den Bau.
