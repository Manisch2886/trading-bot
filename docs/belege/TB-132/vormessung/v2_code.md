# TB-132 — Messung am Code zu R66–R71 (Prüfhelfer, 02.10.2026)

Stand des Repos: `git rev-parse HEAD` = `077945307bc3f0c3eff9a9e05ba61ec799f4cb5c`.
Gelesen und gemessen wurde nur Code; nichts unter `ergebnisse/`, keine Trade-Listen, kein `BACKLOG*.md`, keine echten Kursdaten.
Im Repo wurde nichts angelegt oder geändert (Probe unter `/tmp/tb132/` der Geräte-Shell; nach dem Lauf `find research shared strategies config docs -newer <Marke>`: 0 Treffer; kein `__pycache__`-Eintrag der Probe).

Hashes der gelesenen Dateien (Repo = Container-Kopie, wo vorhanden):

| Datei | SHA-256 |
|---|---|
| `research/vorregistrierung/auswertung.py` | `8ec45123a9daac5ac711dc4cf40a492bdd450216adb8ec03bf83fcfd9a300c98` (Repo und Kopie gleich) |
| `research/vorregistrierung/benchmark.py` | `aeeec9b89bdadd1b2dc2be76b722dc90c328c9482014bbbbfcabd78edccae219` (Repo und Kopie gleich) |
| `research/vorregistrierung/kennzahlen.py` | `d130e15cf2c9b9c1359610aeac715c39c43823314273d8c9f8c78d555e2ea137` |

Abgrenzung, wie gemessen:
- Sperrliste (Register Abschnitt 10, gelesen mit `shared/sperrlistensonde.py::lies_abschnitt_10`), Code-Pfade: `registerdaten.py`, `faltenplan.py`, `auswertung.py`, `benchmark.py`, `herkunft.py` (alle `research/vorregistrierung/`), `shared/zuteilung.py`. Gruppe „eingefroren“ (`herkunft.py:71-73`) zusätzlich: `kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`.
- Laufbereich: `shared/paths.py:239-253` (`ARBEITSBAUM_PFADE` = `shared`, `strategies`, Lock, 12 Einzeldateien) bzw. `docs/belege/TB-112/a2_laufbereich.txt` (84 Zeilen, davon 3 Messumschläge unter `docs/belege/`; 81 Module, alle vorhanden).

---

## M1 (R66 (e)) — Falten-Sharpe aus der Tagesreihe?

**Ergebnis: Kein Code auf der Sperrliste oder im Laufbereich bildet den Falten-Sharpe aus der Tagesreihe oder rechnet ihn nach.**

1. Treffer `sharpe` (ohne Gross/Klein) im Laufbereich: nur vier Dateien — `auswertung.py` (25), `kennzahlen.py` (13), `registerdaten.py` (3), `faltenplan.py` (1). In `shared/` und `strategies/` (alle `*.py`): **0 Dateien**. Muster ohne das Wort (`np.std(`, `.std(`, `sqrt(252|365)`, `annualis`): ausserhalb von `kennzahlen.py` nur `shared/zuteilung.py:387` (Korrelation) und zwei Bollinger-Indikatoren — kein Sharpe.

2. Die einzige Funktion, die einen Sharpe aus Tagesrenditen bildet — `kennzahlen.py:95-108`:
   ```python
   def sharpe(renditen, perioden_je_jahr: int) -> float:
       r = np.asarray(renditen, dtype=float)
       if r.size < 2:
           return 0.0
       s = float(np.std(r, ddof=1))
       if s == 0.0 or not np.isfinite(s):
           return 0.0
       return float(np.mean(r)) / s * math.sqrt(perioden_je_jahr)
   ```
   - Eingang: irgendeine Reihe, die der Aufrufer übergibt; **kein** Schnitt auf Benchmark-Tage, **kein** Faltenfilter in der Funktion.
   - Annualisierung: `× sqrt(perioden_je_jahr)`; `auswertung.py:264-265` gäbe 252 (`rd.HANDELSTAGE_JE_JAHR`, `registerdaten.py:109`) für Aktien, sonst 365. Passt zur Formelzeile des Registers unter 15.3 (c) (Z. 1449-1450).
   - Standardabweichung 0 (oder nicht endlich) → 0,0; weniger als zwei Werte → 0,0. `ddof=1`.
   - **Kein Aufrufer.** `grep -E 'kz\.sharpe\(|kennzahlen\.sharpe\(|[^_a-z]sharpe\('` über `research/vorregistrierung/*.py` (Tests eingeschlossen) trifft nur die Definition. Wer sonst `kennzahlen` importiert (`research/turn_of_month/…`), lädt ein eigenes Modul gleichen Namens im eigenen Ordner.

3. `auswertung.py` liest `netto_sharpe` **nur aus `zellen.csv`**:
   - `auswertung.py:353-354` `df["netto_sharpe"] = np.where(df["n_trades"].to_numpy() == 0, 0.0, df["netto_sharpe"]…)` (Falte ohne Trade → 0, gesetzt)
   - `:355-357` Abbruch bei Leerwert in Falte mit Trades
   - `:395` `teil.groupby("zelle_id")["netto_sharpe"].median()` (Selektionsstatistik)
   - `:575-578` Pivot für das Clustering (N_eff)
   - `:622-623` Zeile der Bestätigungsperiode
   - `:684` `falten_sharpe` im Bericht
   Nirgends wird der Wert gegen `tagesreihen/` geprüft.

4. Was `auswertung.py` aus der Tagesreihe **tatsächlich** rechnet (nur für den Gewinner, `:665` → `beta_bereinigung`, `:499`):
   - Fenster: alle Selektionsfalten zusammen, halboffen — `:510-511` `return any((d >= a) & (d < b) for a, b in fenster)`.
   - Schnitt auf gemeinsame Tage mit dem Benchmark — `:517` `gemeinsam = s.index.intersection(b.index)`; darauf `sr`, `se`, `br` (`:522-524`).
   - Daraus Alpha/Beta, mittlere Exposure (`:528`), Calmar-Vergleich, Zufalls-Timing, Rendite/Drawdown des Gewinners (`:526-543`).
   - **Ein Sharpe je Beobachtung, nicht annualisiert, im DSR:** `:670` `dsr = dsr_drei_werte(bereinigung["renditen"], buch)` → `kennzahlen.py:226-234` `s = float(np.std(r, ddof=1)) … sr = float(np.mean(r)) / s`. Reihe: `sr` = Netto-Renditen des Gewinners auf den **gemeinsamen Tagen (Tagesreihe ∩ Benchmark) aller Selektionsfalten zusammen**. `s == 0.0` oder weniger als 4 Werte → `dsr 0.0, bestimmt False` (`:227-233`). Das ist kein Falten-Sharpe (gepoolt, nicht je Falte; „Bericht, nicht Tor“, `auswertung.py:815`), aber ein Sharpe aus der Tagesreihe über **andere Tage als R66 (b)**: Tage der Tagesreihe ohne Benchmark-Tag gehen nicht ein. Ob das unter R66 (e) fällt, entscheidet der Verfahrensprüfer.

5. Tests: `test_vorregistrierung.py` reicht `sharpe_fn` an `beispieldaten.erzeuge` und prüft `netto_sharpe` aus `zellen.csv`; `test_ersatzwerte.py` hat 0 Treffer `sharpe`. Kein Test rechnet einen Sharpe aus einer Tagesreihe nach.
   `beispieldaten.py:236-266` (nicht Sperrliste, nicht Laufbereich) baut umgekehrt eine Tagesreihe **zum** Ziel-Sharpe: je Falte halboffen (`:249-250`), `mu = ziel_sharpe * sigma / math.sqrt(pj)` (`:255`), auf allen erfundenen Handelstagen (`freq "B"`/`"D"`, `:219-225`), Benchmark auf denselben Tagen.

6. Bootstrap: `grep -i 'bootstrap|resampl|konfidenz|intervall'` über `research/vorregistrierung/*.py`: **0 Treffer**; im Laufbereich keine Datei mit `bootstrap`. Es gibt also heute kein Intervall, keine Reihe, keine Tage. Deckt sich mit der Tatsachennotiz in R35 (Register Z. 10787: „0 Treffer bootstrap, TB-120“).

Nebenbeobachtung, nicht gefragt und nicht gegen den Registertext geprüft: `dsr_drei_werte` übergibt als `sharpe_varianz` die Varianz der Selektionsstatistik über die Zellen (`auswertung.py:587-588`, Median der Falten-Sharpes aus `zellen.csv`, nach Register-Formel annualisiert), während `deflated_sharpe` den SR **je Beobachtung** bildet („SR wird NICHT annualisiert“, `kennzahlen.py:223`). `sr - sr0` (`kennzahlen.py:243`) zieht damit eine Grösse in Jahres-Einheit von einer in Tages-Einheit ab.

---

## M2 (R68) — liest ein Urteil die mittlere Exposure der Bestätigungsperiode?

**Ergebnis: Nein.** Vollständige Aufzählung von `mittlere_exposure` in `auswertung.py`: Z. 41 (Kopftext), 134 (Pflichtspalte), **405**, 537 (Schlüssel im Ergebnis der Beta-Bereinigung), **626**.

- `:626` `"mittlere_exposure": float(z["mittlere_exposure"])` steht in `bestaetigungsperiode()` (`:608-629`, Docstring „Kein Veto“). Das Ergebnis wird nur in das Berichts-Dict gelegt (`:728`) und gedruckt (`:819-825`: Sharpe, Rendite, DD, Trades — die Exposure nicht einmal gedruckt).
- `:405` `e = float(z["mittlere_exposure"])` in `zulaessigkeit()` läuft nur über `df[df["falte"].isin(selektionsfalten)]` (`:403`). `selektionsfalten` = Falten mit `rolle == "selektion"` (`faltenplan.py:357`); die Bestätigungsperiode ist die letzte Falte mit Rolle `bestaetigung` (`faltenplan.py:330`, `:358`).
- Rang/Gewinner (`plateau`, `gewinner`, `:448-484`): nur `statistik` aus `netto_sharpe` der Selektionsfalten. Abbruchkriterien (`:547-565`): `gew`, `zulaessige`, `bereinigung` (Fenster nur Selektionsfalten, `:502-503`), `bester_nicht_spitze`. `kapitalregel` (`:738-739`): nur `abbruchkriterien.bleibt`. Risikoappetit-Zeile (`:696-700`): `zul`, also Selektionsfalten.

Durch Lesen und Aufzählen gemessen, nicht durch Mutationslauf (siehe „Nicht geprüft“).

---

## M3 (R69 (b)) — `zellenbericht`, Drawdown-Spalten, `bestaetigung_ab_effektiv`

- `zellenbericht` in `auswertung.py`: **0 Treffer** (ohne Gross/Klein).
- In `*.py` des Repos (ohne `ergebnisse/`, `trading-env/`): nur `docs/belege/TB-126/0g_vorpruefung.py:62` und `:65` (ein Belegskript, das Vorkommen zählt). Kein Erzeuger, kein Leser.
- `auswertung.py` führt `kapital_drawdown_pct`: Z. 40, 134 (Pflichtspalte), 413-414 (Zulässigkeit), 625, 681-682, 824.
- `kapital_drawdown_mtm_pct`: **0 Treffer** in `auswertung.py` und in allen `*.py` des Repos.
- `bestaetigung_ab_effektiv`: **0 Treffer** in `auswertung.py` und in allen `*.py` des Repos.
- Zu R69 (a) bestätigt: `auswertung.py:379` `pfad = os.path.join(wurzel, "benchmark_tagesreihen", f"{markt}.csv")`; Aufruf `:498-500` mit `markt = rd.BOTS[bot]["markt"]`.

---

## M4 (R66 (a)) — Symbole und Kurse der Aktien-Bots; Kurstage; Benchmark-Tage

Weg in `benchmark.py::je_bot`:
- `:253` `kurse = {markt: tagesschluss(markt) for markt in ("aktien", "krypto")}` — **einmal je Markt**, für alle vier Aktien-Bots dieselben Reihen.
- Symbole: `:142-145` `symbole(markt)` liest `universumsdatei(markt)` = `os.path.join(CONFIG_DIR, os.path.basename(rd.UNIVERSUM[markt]))` (`:138-139`); `registerdaten.py:142-144` → `config/sp500_top150.txt`. `CONFIG_DIR`/`DATA_DIR` kommen aus `shared/paths.py` (`:120-121`; ohne Modus Repo-`config/`/`data/`, unter dem Modus Snapshot, `paths.py:685-693`). Filter `{"XAUTUSDT", "PAXGUSDT"}` gilt marktunabhängig (für Aktien ohne Wirkung).
- Kurse: `:148-161` `tagesschluss` liest `DATA_DIR/<symbol>_1d.csv` mit `pd.read_csv(pfad, parse_dates=["open_time"])`, `df.dropna(subset=["close"])`, Reihe `close` über `pd.DatetimeIndex(df["open_time"])`. Symbole ohne Datei oder ohne einen `close` fallen still weg (`:153-158`). **Kein Loader des Bots** wird gerufen.
- Der „Loader“ geht nur als Handelbar-Tag ein: `:268-271` `lesart = fsm.loader_lesart(bot)`; `handelbar = {s: pd.Timestamp(d) …}`; `reihen = tagesgenau(kurse[eig["markt"]], handelbar)`. `faltenschranke_messung.py:223-258`: für Zeitspannen-Bots `erster + dt.timedelta(days=n)` (`:253`), `erster` = Datum der ersten Datenzeile von `fp.kursdatei(symbol, eig["zeitrahmen"])` (`faltenplan_neun.py:271-275`, `:286-298`; erste 10 Zeichen der ersten Spalte, ohne Blick auf `close`), `n` = `MIN_HISTORY_DAYS`, per Regex aus `strategies/<bot>/multi_symbol_optimise.py` gelesen (`:147-162`). Das ist eine Nachrechnung nach dem Wortlaut des Loaders (Docstring `:227-228`), kein Aufruf. Symbolliste dort: `faltenplan_neun.py:261-268` (eigene Kopie von `UNIVERSUM`, `:152-158`; dieselbe Datei über `paths.CONFIG_DIR`). Für Aktien-Bots ist der Zeitrahmen `1d` (`registerdaten.py:136-139`), also dieselbe Kursdatei wie im Benchmark.
- `:185` `r = r[r.index >= ab]`; `:204-205` `rahmen = pd.DataFrame(reihen).sort_index()` / `return rahmen.pct_change().mean(axis=1, skipna=True).dropna()`.

Antworten:
1. **Die Menge „Tage, an denen mindestens ein Symbol der Universumsdatei einen Kurs trägt“ lässt sich aus denselben Daten bestimmen**: Vereinigung der Indizes von `tagesschluss("aktien")` (Zeilen mit `close` ≠ leer in `<symbol>_1d.csv`, Symbole der Universumsdatei). Eine Funktion, die diese Menge liefert, gibt es nicht; sie ist je Markt, nicht je Bot (eine Universumsdatei für alle vier Aktien-Bots).
2. **Jeder Tag der Benchmark-Reihe ist nach dem Code zwangsläufig ein solcher Tag.** Der Index von `rahmen` ist die Vereinigung der (auf `>= ab` geschnittenen) Kursreihen; `pct_change`, `mean`, `dropna` fügen keinen Indexwert hinzu. Schärfer: jeder Benchmark-Tag ist ein Tag, an dem ein **handelbares** Symbol einen Kurs trägt. Durch die Probe mitgeprüft (Nebenprüfung: 0 zusätzliche Tage in 17 Läufen, beide pandas-Versionen).
3. Die Umkehrung gilt nicht (Tatsache, für R66 (b)/(d) von Belang): Kurstage des Marktes, die kein Benchmark-Tag des Bots sind, sind (a) alle Tage vor dem ersten Kurstag ab dem frühesten Handelbar-Tag und dieser Tag selbst, (b) jeder Tag, an dem nur noch-nicht-handelbare Symbole (oder Symbole ohne Handelbar-Tag) einen Kurs tragen — Probe, Fall (iii-b).
4. Code-Tatsachen zur „Eindeutigkeit“: „Tag“ ist der Zeitstempel `open_time`, wie `read_csv` ihn liest — er wird nicht auf das Datum normalisiert; ein doppelter Zeitstempel in einer Kursdatei wird in `tagesschluss` nicht geprüft.

---

## M5 (R71) — Probe am Code

Probe: `/home/claude/tb132/r71_probe.py` (SHA-256 `3b8f123c95011d497e71b763daa9d7a3aa362df4aa035d6a326618e6555db0a9`; zeichengleich in der Geräte-Shell unter `/tmp/tb132/r71_probe.py` gelaufen).

Aufruf aus dem Repo-Wurzelverzeichnis: `PYTHONDONTWRITEBYTECODE=1 python3 <pfad>/r71_probe.py` (optional Pfad zu `benchmark.py` als Argument). Rückgabewert 0 = alle A-Fälle bestätigen die Aussage, 1 = Abweichung, 2 = `benchmark.py` nicht gefunden.

Bauart: Die echte `benchmark.py` wird geladen; je Fall läuft `je_bot` (Z. 251-321) mit echtem `tagesschluss` (liest synthetische `<symbol>_1d.csv` aus einem Wegwerfordner), echtem `tagesgenau`, echtem `bh_tagesrenditen` (nur mit Mitschnitt umhüllt) und echtem Faltenschnitt (`:290`, `handelstage` `:304`). Ersetzt sind die vier Importe `faltenplan`/`registerdaten`/`faltenschranke_messung`/`paths` durch Attrappen (synthetischer Faltenplan, synthetischer Bot, synthetische Handelbar-Tage, Pfade des Wegwerfordners). Kurslücken je zweimal: Zeile fehlt / `close` leer.

Fälle A (prüfen die Aussage, bestimmen den Rückgabewert): (i), (ii), (iv), (v) wie verlangt; **(vi), (vii), (viii) sind Zusatzfälle des Prüfhelfers** (Handelbar-Tag von Y auf einer Lücke von X; Y beginnt nach dem letzten Kurs von X; versetzte Lücken). Fälle B (nur Verhalten): (ii), (iii), (iii-b), (iv), (v).

### Ergebnis je pandas-Version

| Fall | pandas 2.3.3 (Geräte-Shell, numpy 2.2.6, Python 3.10.12) | pandas 3.0.5 (Container, numpy 2.5.3, Python 3.13.15) |
|---|---|---|
| A (i) erster Kurstag | OK — fehlt, einmal; Handelstage `{'2021': 9, '2022': 10}` bei 10/10 Kurstagen; liegt er vor der ersten Falte, fehlt in keiner Falte ein Tag | OK — gleich |
| A (ii) Lücke bei X, Y hat Kurs | OK — Lückentag und Folgetag in der Reihe | OK — beide in der Reihe |
| A (iv) nach letztem Kurs von X | OK — 8 von 8 Tagen in der Reihe | OK — 8 von 8 |
| A (v) Handelbar-Tag von Y | OK — Tag in der Reihe | OK |
| A (vi) Zusatz | OK — Tag in der Reihe, Wert 0,000000 (aus dem aufgefüllten X) | **ABWEICHUNG** — Tag fehlt |
| A (vii) Zusatz | OK — Tag in der Reihe, Wert 0,000000 (aus dem aufgefüllten X) | **ABWEICHUNG** — Tag fehlt |
| A (viii) Zusatz | OK | **ABWEICHUNG** — Tag nach der Lücke fehlt |
| B (ii) Beitrag von X | Lückentag: **0, aufgefüllt** (Mittel über X und Y); Folgetag: Rendite über die Lücke | Lückentag und Folgetag: X ausgelassen |
| B (iii) kein Symbol mit Kurs | Tag fehlt; Folgetag trägt die Rendite über die Lücke | gleich |
| B (iii-b) nur nicht-handelbares Y mit Kurs | Tag fehlt (Kurstag des Marktes, kein Benchmark-Tag) | gleich |
| B (iv) Beitrag von X nach letztem Kurs | **0, aufgefüllt**, an allen 8 Folgetagen (Benchmark = halbe Y-Rendite) | X ausgelassen |
| B (v) | Handelbar-Tag: nur X; Folgetag: Mittel über X und Y | gleich |
| Rückgabewert | **0** | **1** |
| FutureWarning `fill_method` | **ja** in (ii), (iv), (vi), (vii), (viii) | keine |

Wortlaut der Warnung (pandas 2.3.3): „The default fill_method='pad' in DataFrame.pct_change is deprecated and will be removed in a future version. Either fill in any non-leading NA values prior to calling pct_change or specify 'fill_method=None' to not fill NA values.“

Volle Ausgaben: `/home/claude/tb132/ausgabe_pandas_2.3.3.txt`, `/home/claude/tb132/ausgabe_pandas_3.0.5.txt`.

### Was daraus folgt (Tatsachen)

1. Unter **pandas 2.3.3** bestätigt der Test die Aussage aus R71 in allen sieben A-Fällen: ausser dem ersten Kurstag ab dem frühesten Handelbar-Tag fehlt kein Tag, an dem ein handelbares Symbol einen Kurs trägt; der Tag fehlt einmal je Bot, nicht je Falte.
2. Die Aussage **hängt in den Zusatzfällen am Auffüllen** von `pct_change()` (`benchmark.py:205`, ohne `fill_method`). Unter pandas 3.0.5 (kein Auffüllen) fehlen dort weitere Tage. Die verlangten Fälle (i), (ii), (iv), (v) bestehen unter beiden Versionen.
3. Unter pandas 2.3.3 trägt ein Symbol **ohne Kurs** an Lückentagen und an allen Tagen nach seinem letzten Kurs eine Rendite von genau 0 zum Mittel bei (B (ii), B (iv)); in (vi)/(vii) besteht der Benchmark-Wert des Tages allein aus dieser 0. Der Docstring von `bh_tagesrenditen` sagt „aller Symbole, die dort eine Rendite haben“ (`:194-195`). Dasselbe Repo setzt an anderer Stelle der Sperrliste ausdrücklich das Gegenteil: `shared/zuteilung.py:306-312` `kurse.pct_change(fill_method=None)` mit dem Kommentar „die Voreinstellung von pandas fuellt Luecken vorwaerts auf und erzeugt damit an jedem fehlenden Tag eine Rendite von exakt 0 %. Das ist keine Beobachtung, sondern eine erfundene“.
4. Kein Warnfilter im Laufbereich (`grep 'filterwarnings|simplefilter|set_option'` über alle 81 Module: 0 Treffer): die FutureWarning erschiene im Lauf auf stderr, sobald ein Rahmen eine Lücke oder ein Reihenende vor dem Rahmenende enthält.

### Festgelegte pandas-Version

- `requirements.lock:52` `pandas==2.3.3` (daneben `:50` `numpy==2.0.2`; Kopf: Interpreter 3.9.6, macOS).
- `requirements.txt`: keine `pandas`-Zeile (nur `:65` `pandas_market_calendars>=4.1,<5`). Kein `pyproject.toml`, `uv.lock`, `poetry.lock` im Repo.
- Unter dem Selektionsmodus prüft `shared/paths.py::_pruefe_lock` (`:529-556`) jede `name==version`-Zeile gegen `importlib.metadata` und bricht bei Abweichung mit 2 ab (Kopftext `:169-173`). Der registrierte Lauf rechnet also mit pandas 2.3.3, dem auffüllenden Verhalten.
- Die Geräte-Shell ist nicht die Lock-Umgebung (pandas 2.3.3 stimmt; numpy 2.2.6 statt 2.0.2, Python 3.10.12 statt 3.9.6).

---

## Nicht geprüft

- **Echte Daten:** Ob im Snapshot Kurslücken, vorzeitig endende Reihen oder die Konstellationen (vi)–(viii) und (iii-b) vorkommen, und wie viele Tage der Benchmark dadurch aufgefüllte Nullen trägt. Ebenso, ob `open_time` in allen `_1d.csv` dieselbe Tageszeit trägt und je Datei eindeutig ist (M4, Punkt 4). Auftrag: nur Code und synthetische Daten.
- **Lauf in der Lock-Umgebung** (Python 3.9.6, numpy 2.0.2, macOS, `trading-env`): in der Geräte-Shell nicht startbar (`trading-env/bin/python` dort nicht ausführbar). pandas 2.3.3 stimmt mit dem Lock überein.
- **Echte Importkette**: Die Probe ersetzt `faltenplan`, `registerdaten`, `faltenschranke_messung`, `paths` durch Attrappen. `fsm.loader_lesart` und `fp.faltenplan` wurden gelesen, nicht ausgeführt (sie lesen echte Kursdateien bzw. `ergebnisse/`).
- **M2 als Mutationslauf** (Exposure der Bestätigungszeile ändern, Bericht vergleichen): unterlassen, weil `auswertung.main()` und `beispieldaten.erzeuge()` über `fp.faltenplan(mess)` Dateien unter `ergebnisse/` und echte Kursdaten lesen. M2 ist durch vollständige Aufzählung der Lesestellen belegt.
- **Mit welcher pandas-Version** die gesperrte Tabelle `benchmark_drawdowns_2026-09-23_nach_wegA.json` gerechnet wurde (`ergebnisse/` nicht gelesen).
- **Der Erzeuger** von `zellen.csv`, `tagesreihen/`, `benchmark_tagesreihen/<bot>.csv` existiert nicht; über ihn ist nichts gemessen.
- **Registertext** nur punktuell gelesen (Abschnitt 10 über die Sonde; 15.3; R35) — keine Prüfung, ob die Nebenbeobachtung zum DSR (M1) oder das Auffüllen (M5) dort schon behandelt ist.
