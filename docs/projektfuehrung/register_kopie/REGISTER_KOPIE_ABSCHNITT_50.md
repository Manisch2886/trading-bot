# REGISTER-KOPIE Abschnitt 50 (von 0–56) — Register-Z. 11105–11293 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 50. Tatsachennotizen zu E-2 (TB-126)

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 27c, 29b und 30a „zu messen“ nennt, dazu die Vollzugsnotizen TB-122 und TB-124 nach 37.3. Gemessen über die Geräteanbindung, nur lesend, am 29. und 30.09.2026 (`docs/projektfuehrung/VORMESSUNG_E-2_2026-09-29.md` samt Nachträgen); die Sitzung TB-126 hat in Schritt 0 gemessen, dass die genannten Code-Dateien seither unverändert sind (`docs/belege/TB-126/0f_unveraendert.txt`). Zeilenangaben gelten am Commit `0f56aeb`. Kein Ergebnis gelesen (27.1). Eine Voraussetzung, deren Messung abweicht, steht hier mit dem Befund. Der Block steht trotzdem in 47–49, wo Fable den Abweichungsfall im Block selbst regelt oder beantwortet hat (R41: 30a, Teil 0; R48 (g): R54). Wo ein Befund eine Lesart des steuernden Chats braucht, steht das ausdrücklich da; sie geht mit der nächsten Anfrage an Fable (R48 (d), 50.5). Die Nummer hat der steuernde Chat vergeben, nicht Fable.

### 50.1 Voraussetzungen und Befunde

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R25 (47.8) | Docstring trägt „unter dem Modus“ seit TB-117 Block D | `research/vorregistrierung/auswertung.py:53–62` (nicht 51–52): „unter dem Selektionsmodus fuer JEDEN der neun Bots geprueft, sonst Abbruch mit 2“ | passt; Fundstelle berichtigt |
| R26 (47.9) | `--bot` läuft unter dem Modus bis zum Bericht (Fable nannte J-7) | Gemessen in TB-117 E (`docs/belege/TB-117/e_auswertung_modus.txt`, HEAD `852f253`, „modus_gut: rc 0“), nicht in J-7; `auswertung.py` seither unverändert (TB-126, 0f). Ein Laufwrapper nach 35.4 wurde nicht gefunden | passt in der Sache am Stand `852f253` (Fundstelle E statt J-7, von Fable bestätigt, 30a, Teil 0); an `0f56aeb` ohne Lauf nicht neu gemessen (50.7) |
| R28 (47.11) | Probe von `snapshot.py` gegen Register 18 | fehlte am 29.09.2026; gebaut in TB-124 D: `shared/test_verankerter_datenstand.py`, 3/3, Commit `7453469` (`docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` Abschnitt 5, `docs/belege/TB-124/d_probe.txt`). Nebenbefund: ein weiteres Literal des Datenstands, `SOLL_DATENSTAND` in `research/registernachtrag_tb48/pruefe_abschnitt17.py:97`, ohne eigene Registerprobe; R28 nennt es nicht | erfüllt; Nebenbefund offen (50.7) |
| R33 (48.1) | der Vertrag führt die Trade-Zahl je (Zelle, Falte) | `n_trades`, `auswertung.py:39`, Pflichtspalte Z. 133 | passt |
| R36 (48.4) | MtM-Drawdown in der Falte, Basis Faltenbeginn | `research/mtm_drawdown/mtm_kern.py:296–304` (Basis: letzter Rastertag vor `von`), Raster Z. 135–139. Der Vertrag führt heute nur `kapital_drawdown_pct`; die zwei Spalten nach R36 kommen mit dem Zellen-Erzeuger | passt |
| R41 (48.9) | Haltedauer in 15.4: Kerzenzahl oder Zeitstempeldifferenz? | Zeitstempeldifferenz: `research/faltenplan_neun/embargo_neun.py:36–37, 236–238` | weicht ab ⇒ Abweichungsfall nach R41, von Fable bestätigt (30a, Teil 0); Marke an 15.4; Neurechnung nach 41.3 C2 offen (50.7) |
| R48 (c) (48.16) | die von `auswertung.py` im Fall Spitze ausgegebene Zelle | `auswertung.py:554–556`; ausgegeben wird immer der Plateau-Gewinner mit Markierung (Z. 710–719) | passt; den Randfall ohne zulässigen Nicht-Spitzen-Punkt regelt R55 (49.3) |
| R48 (d) (48.16) | Bildung von `mittlere_exposure` im Vertrag, in `auswertung.py` und in `mtm_kern.py` | nicht gebildet: `auswertung.py:405` liest sie als Eingabe; `mtm_kern.py` führt keine Exposure (nur `gebunden`, zum Einstand, Z. 186–188); `research/exposure_messung/exposure_kern.py` und `research/exposure_messung/auswertung.py:234` teilen `gebunden / kapital_start`, bewertet zum Einstand | An den drei Orten, die R48 (d) nennt, nicht gebildet; ausserhalb davon zum Einstand bewertet. **Lesart des steuernden Chats:** Wo der Code die Grösse nicht hat, gilt der Registertext (R48 (d): „der Registertext folgt dem Code, wo er ihn hat“). An Fable (50.7); offen bis zum Zellen-Erzeuger |
| R48 (f) (48.16) | Markierungen in `auswertung.py`: Kante einschliesslich der Zusatzstufen | Kante nach Position (`auswertung.py:466`); „kein“ ist immer die letzte Stufe, „structural“ wird nach Weite einsortiert (`research/vorregistrierung/registerdaten.py:574–583`) | passt nach Fables Lesart „eingeschlossen = zählt als Stufe mit“ (30a, Teil 0) |
| R48 (g) (48.16) | Perzentilbildung im Code | T − 1 Verschiebungen (`research/vorregistrierung/kennzahlen.py:197`), `np.percentile` (Z. 201); die Rendite wird verkettet (`np.prod`, Z. 199) | T − 1 und Perzentil passen; „Summe“ berichtigt durch R54 (49.2) |
| R48 (i) (48.16) | `pruefe_grenzsaetze.py` prüft die Satzfelder | `research/vorregistrierung/pruefe_grenzsaetze.py:100–148` | passt |
| R49 (b) (48.17) | eine Funktion in `registerdaten.py` bildet die Quantil-Stufen | gebildet in `research/vorregistrierung/messgroessen.py::je_zeitrahmen` (Z. 169–219); `registerdaten.py:558–565` (`achse_werte`) liest nur. Universum aus `config/sp500_top150.txt` und `config/top25_symbols.txt`; der Zeitraum steht nur in `datenbereiche`, nicht in einem eigenen Feld | gemessen; der Ort weicht ab (nicht `registerdaten.py`) |
| R50 (48.18) | Grenzsatz je Rastergrenze; fasst `registerbericht.py` gleiche Sätze zusammen? | Jede Grenze trägt `satz` über `_grenze` (`registerdaten.py:270`); Dubletten werden zusammengefasst (`research/vorregistrierung/registerbericht.py:111–120`). Der Zellenname steht in `auswertung.py::zelle_id` (Z. 272–274), die Cluster in `kennzahlen.py::cluster_anzahl` | Ob: ja und ja; Orte teils anders als in R50; die Zahl „34“ nicht gemessen (50.7) |
| R53 (49.1) | oberste Stufe jeder Rückblick-Achse und feste Fenster je Bot maschinell aus `registerdaten.py` lesbar? | Stufen: `registerdaten.raster()` über `achse_werte`, die oberste ist der letzte Wert je Achse; Bollinger-Fenster: `regel_wert({"regel": "bollinger_fenster"}, …)` gibt 20.0 (Z. 213–216). Für weitere feste Fenster (`VOLUME_AVG_PERIOD`, fester Warm-up der Turtle-Soup-Bots) gibt es keinen Eintrag; `donchian_period` ist eine Rasterachse | teilweise. R53 sagt „nicht als Literal“; „Literal mit Test nach 32.5 (c)“ nennt Fable nur unter „Unsicher“ (30a) — Reibung, an Fable; entschieden wird mit R53 (a) (50.7). Zählweise: 50.5 |
| R54 (49.2) | liest und rechnet irgendein Code `netto_rendite_pct` aus dem Vertrag? | Pflichtspalte `auswertung.py:134`; gelesen nur für die Bestätigungsperiode (Z. 624), berichtet in Z. 823; `netto_rendite_pct_ueber_selektionsfalten` (Z. 675) kommt aus `bereinigung["strategie_rendite_pct"]`, nicht aus der Spalte | trifft zu: Berichtsgrösse ohne Leser im Urteil |
| R55 (49.3) | Nebenfall „keine Zelle zulässig“ | nicht gemessen; im Hauptfall rechnet der Code `None ⇒ False` | Hauptfall passt; Nebenfall erschlossen, Probe offen (50.7) |

> ⭐ **50.1, Zeile R48 (d) ERGÄNZT durch R60 (51.5) und 51.8** (Fable 01a R60, Unterpunkt (d), nachgetragen nach Fable 02a R65 (b), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 50.2 R39 (48.7) — Feldliste der Ausgaben, gemessen aus dem Docstring von `auswertung.py`

R39 verlangt, die Feldliste jeder Ausgabe des Zellen-Erzeugers als Registertext „aus dem Docstring von auswertung.py gemessen“ einzutragen, nicht abgeschrieben. Gemessen am Commit `0f56aeb`, `research/vorregistrierung/auswertung.py` Z. 36–67, zeichengleich:

```
DIE ROHERGEBNISSE - DER VERTRAG
------------------------------------------------------------------------------
    <wurzel>/<bot>/zellen.csv
        zelle_id, <je Rasterachse eine Spalte>, falte, rolle, n_trades,
        netto_sharpe, netto_rendite_pct, kapital_drawdown_pct,
        mittlere_exposure
        -> genau eine Zeile je (Zelle x Falte), fuer ALLE Falten des
           Faltenplans, Bestaetigungsperiode eingeschlossen.

    <wurzel>/<bot>/tagesreihen/<zelle_id>.csv
        datum, netto_rendite, exposure
        -> Tagesreihe ueber alle Falten. Verlangt wird sie fuer jede
           ZULAESSIGE Zelle; gelesen wird sie nur fuer die Zellen, die das
           Programm braucht (Gewinner, bester Nicht-Spitzen-Punkt).

    <wurzel>/<bot>/herkunft.json
        Commit-Hash, Datenstand-Hash, Register-Hash - siehe herkunft.py.
        -> TB-117 (Fable 27a R14, Register 46.5; Lesart 46.9): unter dem
           Selektionsmodus fuer JEDEN der neun Bots geprueft, sonst Abbruch
           mit 2 - Datei fehlt; Commit nicht der Tag-Commit
           (`TB_SELEKTIONSCOMMIT`, Praefix); Datenstand nicht der
           registrierte (Register 18); Register-Hash nicht
           `herkunft.register()` zur Laufzeit; die neun untereinander
           verschieden. Ohne Modus gelesen, wenn vorhanden, und im Kopf des
           Berichts angezeigt, ohne Abbruch (Beispieldaten und Tests tragen
           Nullwerte). Der Kopf des Berichts traegt Commit, Datenstand und
           Register-Hash in beiden Faellen.

    <wurzel>/benchmark_tagesreihen/<markt>.csv
        datum, netto_rendite
        -> das gleichgewichtete point-in-time-Universum, taeglich. Grundlage
           der Beta-Bereinigung und des Zufalls-Timing-Tests.
```

„`benchmark_tagesreihen/<markt>.csv`“ im Zitat lies „`<bot>.csv`“ (R39). Für `zellenbericht.csv` (R34), `symbole_je_falte.csv` (R38) und das Lese-Audit führt der Docstring heute keine Feldliste; sie kommt mit dem Zellen-Erzeuger (R46) und wird dann hier nachgetragen.

### 50.3 Vollzug TB-122 (Tatsachennotiz nach 37.3)

*Übernommen zeichengleich aus dem Entwurf in `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md` Z. 235–275 (Commit `0f56aeb`). Der „Stand 11.3“ darin ist der vom 29.09.2026; den dort offenen Scanbeginn hat TB-124 geschlossen (50.4).*

> **Vollzug TB-30b Posten 3 (11.3) in TB-122 (Tatsachennotiz nach 37.3)**
>
> **Gemessen in TB-122, 29.09.2026** (Belege `docs/belege/TB-122/`, Ergebnis
> `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md`). Eingang `04f07ef`, Schritt 0 `c064405`. Freigabe des
> Betreibers 27.09.2026, ca. 20:20 (Auswahlkarte „E-1: TB-30b Posten 3“), Nachtrag 29.09.2026, ca. 14:52 (bis zu drei
> Testdateien; 27c R31 (b)). Kein Abbruchkriterium ausgelöst.
>
> **Grund:** 11.3 — `sma_trend_filter` war bei `rsi2_mean_reversion` eine Konstante; `bb_squeeze_percentile` und
> `bb_lookback` erreichten bei beiden Volatility-Breakout-Bots die Indikatorberechnung nicht. Ohne die Durchreichung
> ist das registrierte Raster (Abschnitt 3) für diese drei Bots nicht rechenbar (R49 (h): 11.3 ist E-1).
>
> **Hash-Übergänge nach 37.3** (Sperrlistenpunkt 11, „Commit-Hashes von Simulation, Erkennung, Optimierern“):
>
> | Datei | vorher | nachher | Commit | vollzieht |
> |---|---|---|---|---|
> | `strategies/rsi2_mean_reversion/backtest_rsi2.py` | `c0a59a43…` | `836b032a…` | `ab31314` | 11.3 |
> | `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` | `9b2d2a2f…` | `777f5cb0…` | `ab31314` | 11.3 |
> | `strategies/rsi2_mean_reversion/equity_simulation.py` | `3a29a4f1…` | `864907fb…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout/multi_symbol_optimise.py` | `93799bdd…` | `f0a4ee43…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout/equity_simulation.py` | `fde65dbb…` | `7cbc7f00…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout_crypto/multi_symbol_optimise.py` | `e7710d4d…` | `02548e2e…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout_crypto/equity_simulation.py` | `c760c6b8…` | `11094387…` | `ab31314` | 11.3 |
>
> Neu (kein Vorher), Commit `08153e4`: `strategies/rsi2_mean_reversion/test_posten3_durchreichung.py` `1b4edfbc…`,
> `strategies/volatility_breakout/test_posten3_durchreichung.py` `50e872e2…`,
> `strategies/volatility_breakout_crypto/test_posten3_durchreichung.py` `3f78f6da…`.
>
> **`herkunft.register()`:** `01f5997a…` vorher = nachher. Die sieben Dateien gehören nicht zu den eingefrorenen
> Teilen; die Sonde gegen `46f0ad5d…` ist vorher und nachher byte-gleich (Punkt 11 „nicht prüfbar“). Der Übergang
> steht deshalb nur hier und im Commit.
>
> **Nachweis:** Mit den Voreinstellungen (200; 126 / 25.0) sind die Ausgaben von B6, Signalpfad, Kapitalkurve und
> Optimierer-Kurzlauf **13/13 bytegleich**; der Trockenlauf ohne Modus ist 18/18 zeichengleich. Die erste
> Registerstufe (26; 20 / 5) kommt nachweislich in der Indikatorberechnung an (16/16, 12/12, 12/12); am Stand vor
> dem Umbau scheitert dieselbe Probe (40.7).
>
> **Folge aus R47 (Fable 29b, F-17):** Nach Posten 3 ist `SMA_TREND_PERIOD` bei `rsi2_mean_reversion` **Rasterachse**
> (`sma_trend_filter`), nicht Parameterdatei; der Name in `backtest_rsi2.py` bleibt als Voreinstellung.
>
> **Stand 11.3:** geschlossen bis zur Indikatorberechnung; offen der Scanbeginn der Breakout-Bots
> (`backtest_breakout.py::WARMUP_PERIOD`, TB-122 Befund F1).

### 50.4 Vollzug TB-124 (Tatsachennotiz nach 37.3)

*Übernommen zeichengleich aus dem Entwurf in `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` Z. 289–323 (Commit `0f56aeb`). Abgenommen vom steuernden Chat am 30.09.2026; die Befunde der Abnahme berühren keinen Satz dieses Entwurfs. Der Schlusssatz („Der Scanbeginn der Zelle liegt an ihrem Vorlauf …“) folgt der Lesart in 50.5.*

> **Vollzug TB-30b Posten 3 (11.3), Teil Scanbeginn, in TB-124 (Tatsachennotiz nach 37.3)**
>
> **Gemessen in TB-124, 30.09.2026** (Belege `docs/belege/TB-124/`, Ergebnis
> `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md`). Eingang `0034960`, Schritt 0 `baf18a2`. Freigabe des Betreibers
> 30.09.2026, 19:13 (Sachentscheid „TB-122 F1 … geht in TB-124“), Nachtrag 19:44 (zwei Testdateien; 27c R31 (b)).
> Handwerksvorgabe Nachtrag 1 (steuernder Chat, ca. 20:15) nach Fable 30a R53. Kein Abbruchkriterium ausgelöst.
>
> **Grund:** 11.3 (TB-122 Befund F1) — bei beiden Volatility-Breakout-Bots erreichte `bb_lookback` die
> Indikatorberechnung (TB-122), der Scanbeginn hing aber an der Voreinstellung (`WARMUP_PERIOD + 1` = 127). Bei den
> Stufen 20 und 97 schnitt er mögliche Einstiege ab (Balken 39–126 bzw. 116–126); bei den Stufen über 126 lag er vor dem
> Vorlauf der Zelle.
>
> **Hash-Übergänge nach 37.3** (Sperrlistenpunkt 11):
>
> | Datei | vorher | nachher | Commit | vollzieht |
> |---|---|---|---|---|
> | `strategies/volatility_breakout/backtest_breakout.py` | `8dce183d…` | `3fd0cef6…` | `f90135e` | 11.3 |
> | `strategies/volatility_breakout_crypto/backtest_breakout.py` | `b7923b08…` | `3c7ccbe7…` | `f90135e` | 11.3 |
> | `strategies/volatility_breakout/test_posten3_durchreichung.py` | `50e872e2…` | `9a360566…` | `499d68b` | 11.3 (Probe) |
> | `strategies/volatility_breakout_crypto/test_posten3_durchreichung.py` | `3f78f6da…` | `5a5ad774…` | `499d68b` | 11.3 (Probe) |
>
> **`herkunft.register()`:** `01f5997a…` alt = neu. Die vier Dateien gehören nicht zu den eingefrorenen Teilen; die
> Sonde gegen `46f0ad5d…` ist vorher und nachher byte-gleich (Punkt 11 „nicht prüfbar“). Der Übergang steht deshalb nur
> hier und im Commit.
>
> **Nachweis:** Mit den Voreinstellungen (126 / 25.0) sind B6, Signalpfad, Kapitalkurve und Optimierer-Kurzlauf
> **13/13 bytegleich**; der Trockenlauf ohne Modus ist 18/18 zeichengleich. Für jede Registerstufe von `bb_lookback`
> beginnt der Scan am ersten Index, an dem die Einstiegsbedingung definiert ist (`BB_PERIOD + L − 1`), und ein
> Einstieg genau dort wird über Signal- und Optimierer-Pfad gefunden (43/43, 42/42); am Stand vor dem Umbau scheitert
> dieselbe Probe (40.7).
>
> **Stand 11.3:** geschlossen — `sma_trend_filter` (rsi2_mean_reversion), `bb_squeeze_percentile` und `bb_lookback`
> (beide Breakout-Bots) erreichen Indikatorberechnung und Scanbeginn. **Der Scanbeginn der Zelle liegt an ihrem Vorlauf
> (Fable 30a, R53):** er ist der erste Index, an dem die Einstiegsbedingung der Zelle definiert ist — bei den
> Breakout-Bots `BB_PERIOD + L − 1`, nie früher, nicht später.

> ⭐ **50.4, Schlusssatz ERGÄNZT durch R57 (51.2): der Schlusssatz ist bestätigt** (Fable 01a R57, nachgetragen nach Fable 02a R65 (b), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 50.5 Lesart des steuernden Chats zu R53 (49.1) — Zählweise des Vorlaufs

⚠️ **Vorläufig, bis Fable bestätigt** (Bauart 46.9).

R53 nennt die Regel, nicht die Werte (30a, „Unsicher“ zu Frage 1). Wörtlich addiert ergäbe „oberste Stufe zuzüglich der festen Fenster“ bei den zwei Volatility-Breakout-Bots L + 20 (Bollinger-Fenster 20). Aus dem Code hergeleitet ist der erste Balken, an dem die Einstiegsbedingung einer Zelle definiert ist, `BB_PERIOD + L − 1`, also L + 19. Das Bollinger-Fenster über `close` und das Squeeze-Fenster L über `bb_width` sind zwei hintereinanderliegende rollende Fenster ohne `min_periods`, die sich einen Balken teilen (`docs/belege/TB-124/b1_herleitung.txt`, je Stufe von `bb_lookback` und Voreinstellung; Nachtrag 1 zu TB-124). Dieser Eintrag liest R53 als den hergeleiteten Wert, also den ersten definierten Index, nicht als Summe von Fensterlängen. Das ist eine Lesart des steuernden Chats; sie geht mit der nächsten Anfrage an Fable zur Bestätigung. Für die übrigen sieben Bots ist der Vorlauf noch nicht hergeleitet; das geschieht mit R53 (a) (50.7).

> ⭐ **50.5 ERGÄNZT durch R57 (51.2): die Lesart ist bestätigt** (Fable 01a R57, TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 50.6 Tatsachennotiz zu R24 (47.7) — Entscheid des Betreibers

Zur Entscheidungsvorlage in R24 hat der Betreiber am 29.09.2026 per Auswahlkarte „(a) So lassen“ gewählt, die Empfehlung des Verfahrensprüfers (T116-5; `docs/projektfuehrung/UEBERGABE_ARCHIV.md`, Nachtrag 29.09.2026, 12:25, und Umzug 29.09.2026, 20:48, Block 6). Ein Deckel je Bot vor dem Netting ist damit nicht registriert.

### 50.7 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | R41: Neurechnung von 15.4 nach 41.3 C2 (Kerzenzählung) | Mac-Messung vor dem Tag |
| 2 | R48 (d): `mittlere_exposure` im Vertrag bilden, bewertet wie die MtM-Reihe | mit dem Zellen-Erzeuger (R46) |
| 3 | R50: die Zahl „34“ (Zählweise), die Ausstiegskonvention der neun `backtest_*.py`; Nebenbefund DSR-Einheiten `kennzahlen.py:222–224` (Vormessung 29.09.2026, Abschnitt 2) | vor dem Tag |
| 4 | R53 (a): Vorlauf je Bot aus `registerdaten.py` rechnen; feste Fenster ohne Eintrag; Herleitung für die übrigen sieben Bots | Handwerk (BACKLOG „Aus Fable 30a“) |
| 5 | R55: Probe „leere Menge ⇒ (d) nicht erfüllt“ mit Gegenprobe, dazu der Nebenfall | Handwerk (BACKLOG „Aus Fable 30a“) |
| 6 | R28: das Literal in `pruefe_abschnitt17.py:97` | Fable zur Kenntnis, dann Handwerk |
| 7 | R39: Feldlisten für `zellenbericht.csv`, `symbole_je_falte.csv`, Lese-Audit | mit dem Zellen-Erzeuger |
| 8 | R42: Punkt 15 im Listentext von Abschnitt 10 | vor dem Tag, nach R42 |
| 9 | R21: Anforderung an das Leiter-Skript, Stufe IV | mit dem Leiter-Skript |
| 10 | R8 (d): Verweis aus Register 9 (45.8) | nach dem Tag; die Marke in 9 aus R51 ist eine andere |
| 11 | R31 (b), R49 (e): Regeln für das Regelwerk (Freigabe nennt die Tests; Marken nennen Bezeichner) | Dokumentationsauftrag |
| 12 | Lesarten und Reibung: 50.5 (Zählweise), R48 (d) (Registertext gilt, wo der Code die Grösse nicht hat), R53 („Literal mit Test“ gegen „nicht als Literal“) | nächste Anfrage an Fable |
| 13 | R26: Lauf von `auswertung.py --bot` unter dem Modus an einem Stand nach `0f56aeb` | vor dem Tag, mit den Tag-Vorbedingungen |

