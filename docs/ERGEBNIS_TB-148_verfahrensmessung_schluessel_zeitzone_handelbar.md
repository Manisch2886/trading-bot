# ERGEBNIS TB-148 — Verfahrensmessung durch Lesen: Schlüssel der Zuteilung, Zeitzone des Schnitts, Träger der Ausstiege, Handelbar-Tag

**Stand:** 10.10.2026, Mac-Sitzung TB-148 (Hauptordner, lokal), Opus 5.5, Aufwand hoch. Auftrag: `docs/auftraege/MAC_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md`. Belege: `docs/belege/TB-148/`.
**Eingang:** HEAD `3ecde8747cb94b6ec14b70aa07e8c735fbea11e6` (in 0a gemessen). **Commits:** ⟨S0⟩ `4ebd2510dec3905952bf6835344192e0635678dc` (Schritt 0) · `40fbfcd` (M1, mit den Belegen aus 0a und A) · `050e95e` (M2) · `80e630d` (M3) · `9100da5` (M4) · `505b216` (M5). Die Kennung des Abgabe-Commits ⟨F⟩ und des letzten Commits nennt die Schlussmeldung.
**Bauart:** Verfahrensmessung nach Register 27.2, nur durch Lesen mit dem Lesewerkzeug von Claude Code. Kein Programm des Repos ausgeführt oder importiert, keine Trade-Liste und nichts unter `ergebnisse/`, `data/`, `snapshots/`, `logs/` geöffnet, keine Ergebniszahl eines Laufs genannt, keine Unter-Agenten. Geändert wurde nur unter `docs/` (Belege, dieses Ergebnis, ein Journalblock).
**Rückfragen an den Betreiber:** keine.

## Kurz

| | Soll | Ist |
|---|---|---|
| **0a** | HEAD `3ecde87…`, genau drei Einträge (`AKTUELLER_AUFTRAG.md` und `UEBERGABE.md` geändert, Auftrag TB-148 neu) | wie Soll (`0a_status.txt`, 156 B; `cmp` ohne Ausgabe) |
| **A** | Prozesszeile mit `--permission-mode manual` | `claude --permission-mode manual --effort high --remote-control --no-chrome` (EIGEN 91560, `a_modus.txt`) |
| **M1** | Wie bildet `shared/zuteilung.py` den Schlüssel? | **Streuwert**: blake2b (16 Byte, hex) über `str(SEED)` und die Textform von `symbol`, `entry_time`, `exit_time`, `entry_price`, `exit_price`, `pnl_pct` (soweit vorhanden); geordnet wird nach dem Streuwert (`zuteilung.py` Z. 425–426, 492–497, 540, 577) |
| **M2** | Zeitzone von `open_time` und Go-Live-Schnitt | beide **zonenlos** gelesen, nirgends eine Zeitzone zugewiesen oder umgerechnet; `open_time` Krypto = UTC (Erzeuger-Vertrag), Schnitt ohne Zeitzone, `open_time` Aktien von yfinance bestimmt → **durch Lesen nicht entscheidbar** |
| **M3** | (a) Reihenfolge aus `capital_after`? (b) genau ein Ausstieg je Bot? | (a) **ja** bei gleichem Zeitstempel (Kette `capital_after` mit `allocation`, `pnl_pct`, `KETTEN_TOLERANZ`), sonst nach `exit_time` (`mtm_kern.py` Z. 99–119); (b) **genau einer** bei allen neun Bots (erschlossen) |
| **M4** | Kann der Scan vor dem Handelbar-Tag einsteigen? je Bot | **kann** bei allen neun Bots (erschlossen) |
| **M5** | Gibt die Benchmark-Rechnung den Handelbar-Tag je Symbol heraus? | **ja**, aber nicht über `bh_tagesrenditen`: `benchmark.py::je_bot` Z. 276 (Feld `handelbar_ab`, Symbol → ISO-Datum) und über `main`/`schreibe_tabellen` in der JSON-Datei; gehalten von `faltenschranke_messung.py::loader_lesart`; keine der beiden `bh_tagesrenditen` gibt ihn heraus |
| **D0** | je Block Schlusszeile `rc 0` | `lese_zeilen.txt` rc 0, `lese_md5.txt` rc 0 (70 Dateien: 63 Startdateien und 7 weitere) |
| **D3** | `f_porcelain.txt` 0 B; `f_numstat.txt` `rc 0`, nur Pfade unter `docs/belege/TB-148/`, Ergebnis und `JOURNAL.md`, 0 entfernte Zeilen | nach der Abgabe gemessen, siehe Beleg; die Werte nennt die Schlussmeldung |

## M1 — Schlüssel der Zuteilung

**Frage** (Register Z. 11722, 55.8 Nr. 5): wie `shared/zuteilung.py` den Schlüssel aus `exit_time`, `exit_price` und `pnl_pct` bildet — als Streuwert über die Felder oder als Ordnung nach einem von ihnen; nur das Wie. `shared/zuteilung.py` wurde nur gelesen (Punkt 10 bleibt zu).

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| M1-1 | Bauart: **Streuwert über die Felder** — der Schlüssel ist ein blake2b-Fingerabdruck (16 Byte, hexadezimal) einer Zeichenkette aus Startwert und Feldern, nicht eine Ordnung nach einem Feld. | `shared/zuteilung.py` Z. 425–426 | `roh = "\|".join([str(seed)] + [str(f) for f in felder])` / `return hashlib.blake2b(roh.encode("utf-8"), digest_size=16).hexdigest()` | belegt |
| M1-2 | Die Felder sind nicht nur `exit_time`, `exit_price`, `pnl_pct`, sondern sechs Spalten in fester Reihenfolge: `symbol`, `entry_time`, `exit_time`, `entry_price`, `exit_price`, `pnl_pct` — jeweils nur, soweit die Trade-Tabelle die Spalte führt. | Z. 492–493 | `felder = [s for s in ("symbol", "entry_time", "exit_time", "entry_price", "exit_price", "pnl_pct") if s in trades.columns]` | belegt |
| M1-3 | Jedes Feld geht als Text ein (`astype(str)` der Spalte), dann je Trade zeilenweise zusammengefasst und an `zufallsschluessel` gegeben; der Startwert ist `self.seed`. | Z. 494–496 | `texte = [trades[s].astype(str).tolist() for s in felder]` / `self._zufall = [zufallsschluessel(self.seed, werte) for werte in zip(*texte)] if texte else [` | belegt |
| M1-4 | Führt die Tabelle keine der sechs Spalten, wird der Schlüssel aus der Zeilennummer `i` gebildet (Rückfall). | Z. 496–497 | `zufallsschluessel(self.seed, [i]) for i in range(len(trades))]` | belegt |
| M1-5 | Der Startwert ist die Modulkonstante `SEED`; `Zuteiler` und `simuliere_portfolio` haben ihn als Vorbelegung. | Z. 174; Z. 462; Z. 661 | `SEED = 20260913` / `signalspalte=None, seed: int = SEED):` / `seed: int = SEED) -> dict:` | belegt |
| M1-6 | Keiner der neun Bots übergibt einen eigenen Startwert: jede `simulate_portfolio` ruft `simuliere_portfolio` ohne `seed`, also mit `SEED`. | `strategies/elliott_wave/equity_simulation.py` Z. 137–138; `t3_supertrend` Z. 130–132; `rsi2_crypto` Z. 124–126; `turtle_soup_crypto` Z. 107–109; `volatility_breakout_crypto` Z. 162–164; `elliott_wave_stocks` Z. 159–161; `rsi2_mean_reversion` Z. 159–161; `turtle_soup_stocks` Z. 146–148; `volatility_breakout` Z. 147–149 (je `strategies/<Bot>/equity_simulation.py`) | `return simuliere_portfolio(trades, starting_capital, allocation_pct, max_concurrent_positions, kursdaten, signalspalte=signalspalte)` (elliott_wave: `None` statt `max_concurrent_positions`) | erschlossen (aus M1-5 und den neun Aufrufen) |
| M1-7 | Verwendung auf Stufe 4: gewählt wird der Kandidat mit dem kleinsten Schlüssel, d. h. Ordnung nach dem Streuwert (lexikographisch über die Hex-Zeichenkette), erst nachdem Stufe 1 bis 3 keinen Einzelnen ergaben. | Z. 576–578 | `# Stufe 4 - seeded Zufall` / `gewinner = min(gruppe, key=lambda i: self._zufall[i])` | belegt |
| M1-8 | Derselbe Schlüssel ordnet die Ausstiege mit gleichem Zeitstempel (aufsteigend). | Z. 529–540 | `def ausstiegsreihenfolge(self, positionen):` … `return sorted(positionen, key=lambda p: self._zufall[p])` | belegt |
| M1-9 | In `simuliere_portfolio` wird der Schlüssel an drei Stellen benutzt: Reihenfolge der Ausstiege je Zeitpunkt, Reihenfolge der Einstiege eines nicht umstrittenen Zeitpunkts, und `waehle` bei umstrittenem Zeitpunkt. | Z. 724; Z. 765–766; Z. 781–782 | `for pos in zuteiler.ausstiegsreihenfolge(ausstiege_je_zeit.get(zeit, ())):` / `if not umstritten: rest = zuteiler.ausstiegsreihenfolge(rest)` / `else zuteiler.waehle(rest, _buch(open_positions, symbole), zeit))` | belegt |
| M1-10 | Der Kopftext beschreibt dieselbe Bauart: Fingerabdruck aus dem Inhalt des Trades und `SEED`, nicht aus der Zeilennummer. | Z. 45–46; Z. 412–418 | `4. **Seeded Zufall** - ein Fingerabdruck aus dem Inhalt des Trades und dem protokollierten Startwert `SEED`.` / `Ein reproduzierbarer Fingerabdruck aus dem INHALT eines Trades.` | belegt |
| M1-11 | Konstante `STUFE_ZUFALL` ist nur der Protokollname der Stufe; sie geht nicht in den Schlüssel ein. | Z. 207; Z. 578 | `STUFE_ZUFALL = "zufall"` / `return self._fertig(gewinner, STUFE_ZUFALL, begonnen)` | belegt |

**Antwort:** `shared/zuteilung.py` bildet den Schlüssel als **Streuwert** (blake2b, 16 Byte, hex) über die Textform von `str(SEED)` und sechs Feldern — `symbol`, `entry_time`, `exit_time`, `entry_price`, `exit_price`, `pnl_pct`, soweit vorhanden —, nicht als Ordnung nach einem dieser Felder; geordnet wird danach nach dem Streuwert selbst (Z. 425–426, 492–497, 540, 577).

## M2 — Zeitzone von `open_time` und Go-Live-Schnitt

**Frage** (Register Z. 11722; Antwort 09.10.a Z. 222, R86 (e)): ob `open_time` und der Go-Live-Schnitt in derselben Zeitzone gelesen werden; nur das Wie.

### (a) Wie der Go-Live-Schnitt gelesen wird

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| M2-1 | Der Schnitt ist eine Zeichenkette, ein Kalenderdatum ohne Uhrzeit und ohne Zeitzone. | `research/vorregistrierung/registerdaten.py` Z. 102 | `GO_LIVE_SCHNITT = "2026-09-01"      # siehe Abschnitt "Faltenplan" im Register` | belegt |
| M2-2 | `faltenplan.py` liest ihn als `datetime.date` (zonenlos) und bildet daraus die Faltengrenzen als ISO-Datum. | `research/vorregistrierung/faltenplan.py` Z. 285; Z. 326; Z. 308–315 | `schnitt = date.fromisoformat(rd.GO_LIVE_SCHNITT)` / `"bis_ausschliesslich": ende.isoformat(),` | belegt |
| M2-3 | `faltenplan_neun.py` führt den Schnitt als eigenes zonenloses `dt.date`-Literal (Kopie, nicht gelesen aus `registerdaten.py`) und vergleicht ihn mit Jahren und Daten. | `research/faltenplan_neun/faltenplan_neun.py` Z. 137–139; Z. 444; Z. 466–472 | `GO_LIVE = dt.date(2026, 9, 1)             # ausschliesslich` / `ende = min(dt.date(jahr + laenge, 1, 1), GO_LIVE)` | belegt |
| M2-4 | `erste_falte_trockenlauf.py` liest ihn wie M2-2 als zonenloses `date`. | `research/faltenplan_neun/erste_falte_trockenlauf.py` Z. 197; Z. 215 | `schnitt = dt.date.fromisoformat(rd.GO_LIVE_SCHNITT)` | belegt |
| M2-5 | `faltenschranke_messung.py` gibt den Schnitt nur als ISO-Text weiter (`fp.GO_LIVE.isoformat()`), ohne Zeitzone. | `research/faltenplan_neun/faltenschranke_messung.py` Z. 298; Z. 341; Z. 507 | `"go_live": fp.GO_LIVE.isoformat(),` | belegt |
| M2-6 | `registerbericht.py` gibt den Schnitt nur als Text aus. | `research/vorregistrierung/registerbericht.py` Z. 137 | `f"Go-Live-Schnitt: **{rd.GO_LIVE_SCHNITT}** (ausschliesslich).", "",` | belegt |
| M2-7 | Aus dem Faltenende (ISO-Datum) wird ein zonenloser Zeitpunkt eine Sekunde vor Mitternacht gebildet. | `research/universum_trockenlauf/universum_trockenlauf.py` Z. 292–301 (aufgerufen aus `erste_falte_trockenlauf.py` Z. 91–94) | `b = dt.datetime.strptime(bis_ausschliesslich, "%Y-%m-%d") - dt.timedelta(seconds=1)` | belegt |

### (b) Wo `open_time` gewandelt, mit einer Zeitzone versehen oder mit einem Datum verglichen wird

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| M2-8 | Alle neun Lader lesen `open_time` mit `parse_dates`, ohne `utc=` und ohne Zeitzonenangabe: zonenlos, so wie der Text der Datei es hergibt. | je `strategies/<Bot>/multi_symbol_optimise.py`: `elliott_wave` Z. 63; `t3_supertrend` Z. 59; `rsi2_crypto` Z. 66; `turtle_soup_crypto` Z. 49; `volatility_breakout_crypto` Z. 51; `elliott_wave_stocks` Z. 72; `rsi2_mean_reversion` Z. 67; `turtle_soup_stocks` Z. 56; `volatility_breakout` Z. 63 | `df = pd.read_csv(csv_path, parse_dates=["open_time"])` | belegt |
| M2-9 | Krypto-Erzeuger (Abruf): `open_time` kommt als UTC-Millisekunden, wird als UTC gelesen und die Zone dann entfernt — zonenloser UTC-Zeitstempel. | `shared/fetch_binance_data.py` Z. 98; Z. 339–340 | `` `open_time` ist ein zeitzonenfreier UTC-Zeitstempel`` / `df["open_time"] = (pd.to_datetime(df["open_time"], unit="ms", utc=True).dt.tz_localize(None))` | belegt |
| M2-10 | Krypto-Erzeuger (Historie): dieselbe Wandlung; geschrieben wird mit festem Format ohne Offset. | `shared/binance_historie.py` Z. 331; Z. 104–108; Z. 488 | `df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).dt.tz_localize(None)` / `"1d": "%Y-%m-%d",` | belegt |
| M2-11 | `abrufschutz.py` legt `open_time` als naive UTC aus; ein zonenbehafteter Wert würde nach UTC gebracht und naiv gelesen. | `shared/abrufschutz.py` Z. 145–150; Z. 200–205 | `Naiv und in UTC, weil die Kursdateien dieses Repos ihre Zeitstempel so fuehren (`2017-08-17 04:00:00`, ohne Offset)` / `umgerechnet.dt.tz_convert("UTC").dt.tz_localize(None)` | belegt |
| M2-12 | Aktien-Erzeuger: `open_time` ist die Spalte `Date`/`Datetime` von `yf.download`, unverändert umbenannt und mit `to_csv` geschrieben; der Code des Repos setzt oder entfernt keine Zeitzone. | `strategies/elliott_wave_stocks/fetch_stock_data.py` Z. 75; Z. 84–93; Z. 136 | `date_col = "Date" if "Date" in df.columns else "Datetime"` / `date_col: "open_time",` / `df.to_csv(output_file, index=False)` | belegt |
| M2-13 | Welche Zeitzone (und welchen Kalendertag) `open_time` in den Aktien-Dateien trägt, bestimmt yfinance, nicht der Code des Repos: **durch Lesen nicht entscheidbar** (Verhalten einer Fremdbibliothek; die Kursdateien dürfen nicht geöffnet werden). | wie M2-12 | — | offen |
| M2-14 | Die Aktien-Lader schneiden auf `RECENT_YEARS_ONLY` mit `open_time.max() - DateOffset`: Vergleich `open_time` gegen einen aus `open_time` selbst gebildeten Zeitpunkt, beide zonenlos. | `elliott_wave_stocks/multi_symbol_optimise.py` Z. 93–94; `rsi2_mean_reversion` Z. 93; `turtle_soup_stocks` Z. 81; `volatility_breakout` Z. 89 | `cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)` | belegt |
| M2-15 | In den Backtest-Modulen wird `entry_cutoff` gegen `open_time` verglichen (Scanbeginn und Filter), beide aus derselben Spalte, zonenlos. | z. B. `strategies/rsi2_crypto/backtest_rsi2.py` Z. 87–88, 123; gleich gebaut `turtle_soup_crypto/backtest_turtle_soup.py` Z. 125–126, 167; `volatility_breakout_crypto/backtest_breakout.py` Z. 130–131, 170; `rsi2_mean_reversion/backtest_rsi2.py` Z. 130–131, 166; `turtle_soup_stocks/backtest_turtle_soup.py` Z. 121–122, 163; `volatility_breakout/backtest_breakout.py` Z. 171–172, 211 | `start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))` / `if entry_cutoff is None or entry_time >= np.datetime64(entry_cutoff):` | belegt |
| M2-16 | Die Walk-Forward-Teilung bildet `split_time` aus `open_time.min()`/`.max()` (bzw. `entry_cutoff`) und vergleicht `entry_time` dagegen — zonenlos, aus derselben Spalte. | z. B. `strategies/rsi2_crypto/multi_symbol_walk_forward.py` Z. 28–30, 54; `rsi2_mean_reversion` Z. 37–39, 68; `volatility_breakout` Z. 28–30, 55; `volatility_breakout_crypto` Z. 22–24, 45; `turtle_soup_crypto` Z. 22–24; `turtle_soup_stocks` Z. 22–24 | `split_time = window_start + (window_end - window_start) * ratio` / `trades = trades[trades["entry_time"] < cutoff_end]` | belegt |
| M2-17 | Die übrigen `open_time`-Zeilen der fünf anderen `wf` sind Ausgaben (`min()`/`max()` im Text). | `strategies/elliott_wave/multi_symbol_walk_forward.py` Z. 47, 49; `t3_supertrend` Z. 42, 44; `elliott_wave_stocks` Z. 47, 49 | `f"{train_data[example_symbol]['open_time'].min()} bis {train_data[example_symbol]['open_time'].max()}")` | belegt |
| M2-18 | Regimefilter: `entry_time` gegen BTC-`open_time` per `merge_asof`, beide aus Kursdateien desselben Erzeugers, zonenlos. | `strategies/t3_supertrend/regime_filter.py` Z. 37–44; `strategies/volatility_breakout_crypto/regime_filter.py` Z. 33–40 | `left_on="entry_time", right_on="open_time", direction="backward",` | belegt |
| M2-19 | `shared/zuteilung.py` verdichtet `open_time` auf Kalendertage (`normalize`) und vergleicht Einstiegszeit dagegen, beides zonenlos; kein Bezug zum Schnitt. | `shared/zuteilung.py` Z. 268; Z. 333–334 | `tag = pd.to_datetime(df["open_time"]).dt.normalize()` / `tag = pd.Timestamp(zeit).normalize().to_datetime64()` | belegt |
| M2-20 | `shared/kursdaten.py` gibt `open_time` nur als Text in einen Befund (`str(z)`), ohne Wandlung. | `shared/kursdaten.py` Z. 134; Z. 147–148 | `"zeitpunkte": [str(z) for z in df.loc[maske, "open_time"].tolist()[:5]]` | belegt |
| M2-21 | Indikatoren und Zigzag reichen `open_time` nur durch (`df[["open_time"]]`, `.values`). | `strategies/rsi2_crypto/indicators.py` Z. 98; `strategies/volatility_breakout_crypto/indicators.py` Z. 85; `strategies/elliott_wave/zigzag_indicator.py` Z. 40, 136; `strategies/elliott_wave_stocks/zigzag_indicator.py` Z. 40, 136 | `result = df[["open_time"]].copy()` / `times = df["open_time"].values` | belegt |

### (c) Wo `open_time` gegen eine aus dem Schnitt gebildete Grenze verglichen wird

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| M2-22 | Trockenlauf des Laufcodes: Der Stichtag (aus M2-7) wird als zonenloses `pd.Timestamp` gebildet und gegen die vom Lader mit `parse_dates` gelesene `open_time` verglichen — beide Seiten zonenlos, keine Umrechnung. | `research/universum_trockenlauf/loaderlauf.py` Z. 618; Z. 503–505 | `_STICHTAG[0] = pd.Timestamp(s) if s else None` / `df = df[df["open_time"] <= stichtag]` | belegt |
| M2-23 | Benchmark-Rechnung: Der Index der Renditen (`open_time`, mit `parse_dates` gelesen) wird gegen die Faltengrenzen (aus M2-2, als zonenloses `pd.Timestamp`) verglichen. | `research/vorregistrierung/benchmark.py` Z. 155, 160; Z. 279–280, 290 | `von = pd.Timestamp(f["von"])` / `bis = pd.Timestamp(f["bis_ausschliesslich"])` / `fenster = renditen[(renditen.index >= von) & (renditen.index < bis)]` | belegt |
| M2-24 | `faltenplan_neun.py` liest aus jeder Kurszeile die ersten zehn Zeichen von `open_time` als Kalenderdatum (zonenlos) und vergleicht mit Datumswerten; der Schnitt geht dort nur als Jahr und Faltenende ein. | `research/faltenplan_neun/faltenplan_neun.py` Z. 278–283; Z. 313 | `return dt.date.fromisoformat(zeile.split(",")[0][:10])` | belegt |
| M2-25 | In den gelesenen Dateien des Signalpfads (neun `mso`, neun Backtest-Module, neun `wf`, neun `es` in den gelesenen Bereichen, die unter (b) genannten Dateien aus `shared/` und den Bot-Ordnern) steht keine Stelle, die `open_time` gegen den Go-Live-Schnitt vergleicht; der Schnitt erreicht den Signalpfad nur über die Kursdaten, die `loaderlauf.py` bis zum Stichtag durchreicht (M2-22). | Leseprotokoll; M2-8 bis M2-21 | — | erschlossen (gelesen nicht jede Zeile aller 78 Dateien des Importbaums; ohne Suchwerkzeug kein vollständiger Nachweis) |

**Satz am Schluss:** Beide Seiten werden **zonenlos** gelesen — der Schnitt als Kalenderdatum (`registerdaten.py` Z. 102, `faltenplan.py` Z. 285), `open_time` mit `parse_dates` ohne Zeitzone (neun Lader, M2-8); an keiner der gelesenen Vergleichsstellen (M2-22 bis M2-24) wird einer Seite eine Zeitzone zugewiesen oder umgerechnet. Welche Zeitzone der zonenlose Wert bedeutet, ist für `open_time` der Krypto-Dateien UTC (M2-9 bis M2-11), für den Schnitt im Code nirgends festgelegt und für `open_time` der Aktien-Dateien von yfinance bestimmt (M2-12, M2-13). Ob beide „in derselben Zeitzone“ gelesen werden, ist deshalb **durch Lesen nicht entscheidbar** — für die Krypto-Bots gilt: dieselbe zonenlose Lesart, `open_time` als UTC; für die Aktien-Bots fehlt die Zeitzone von `open_time` im Code.

## M3 — Träger der Ausstiege

**Frage** (Antwort 09.10.a Z. 216, R84 (e)): ob `ereignisreihenfolge` die Reihenfolge der Ausstiege aus `capital_after` zurückgewinnt; ob eine ausgeführte Position bei jedem der neun Bots genau einen Ausstieg hat. Nur das Wie. Die zwei Schlusssätze der Klammer sind Entscheide des Verfahrensprüfers und wurden nicht angewandt.

### (a) Woher `ereignisreihenfolge` die Reihenfolge der Ausstiege nimmt

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| M3-1 | Zwischen verschiedenen Ausstiegszeitpunkten nimmt die Funktion die Reihenfolge aus `exit_time`: stabile Sortierung, dann Gruppen je `exit_time` aufsteigend. | `research/mtm_drawdown/mtm_kern.py` Z. 99; Z. 103 | `pos = pos.sort_values("exit_time", kind="stable").reset_index(drop=True)` / `for _, gruppe in pos.groupby("exit_time", sort=True):` | belegt |
| M3-2 | Innerhalb eines Zeitstempels gewinnt sie die Reihenfolge aus `capital_after` zurück: genommen wird die Position, deren Schritt `allocation * pnl_pct / 100` vom bisherigen Stand innerhalb `KETTEN_TOLERANZ` auf ihr `capital_after` führt; danach wird ihr `capital_after` der neue Stand. | Z. 105–119 | `schritt = pos.at[i, "allocation"] * pos.at[i, "pnl_pct"] / 100.0` / `if abs(kapital + schritt - pos.at[i, "capital_after"]) <= KETTEN_TOLERANZ:` / `kapital = float(pos.at[treffer, "capital_after"])` | belegt |
| M3-3 | Schliesst die Kette für keinen Kandidaten, bricht die Funktion mit `ValueError` ab. | Z. 112–116 | `if treffer is None:` / `raise ValueError(` / `f"Kapitalkette schliesst nicht bei exit_time "` | belegt |
| M3-4 | Die Toleranz ist eine Konstante des Kerns, begründet mit der Rundung von `capital_after` und `allocation` auf zwei Stellen. | Z. 66–72 | `KETTEN_TOLERANZ = 0.02` | belegt |
| M3-5 | Der Docstring sagt dasselbe: Die Reihenfolge bei gleichem Zeitstempel ist in der Liste nicht vermerkt und wird aus der Kette rekonstruiert. | Z. 83–92 | `Die ist in der Liste nicht vermerkt - aber die Kette` / `capital_after[k] = capital_after[k-1] + allocation[k] * pnl_pct[k] / 100` / `laesst sie rekonstruieren` | belegt |
| M3-6 | Die Ereigniskurve ist `capital_after` je Ausstieg in dieser Reihenfolge. | Z. 123–128 | `return pd.Series(ereignisse["capital_after"].to_numpy(dtype=float), index=pd.DatetimeIndex(ereignisse["exit_time"]), name="capital_after")` | belegt |
| M3-7 | Die Positionen kommen aus einer gespeicherten Trade-Liste mit den Pflichtspalten `allocation` und `capital_after` (Liste aus TB-24), nicht aus einem Aufruf von `simuliere_portfolio`. | `research/mtm_drawdown/grundlage.py` Z. 58–59; Z. 62–71 | `PFLICHTSPALTEN = ("symbol", "entry_time", "exit_time", "entry_price", "exit_price", "pnl_pct", "allocation", "capital_after")` / `pos = pd.read_csv(pfad, parse_dates=["entry_time", "exit_time"])` | belegt |
| M3-8 | `simuliere_portfolio` schreibt je verbuchtem Ausstieg genau eine Zeile mit `capital_after` in die `equity_curve`; die Reihenfolge der Ausstiege bei gleichem Zeitstempel kommt dort aus `ausstiegsreihenfolge` (seeded Zufall, M1). | `shared/zuteilung.py` Z. 724–735; Z. 540 | `for pos in zuteiler.ausstiegsreihenfolge(ausstiege_je_zeit.get(zeit, ())):` / `"capital_after": round(capital, 2),` | belegt |
| M3-9 | Aufrufer von `ereignisreihenfolge`: `grundlage.pruefe_bot`, `messung.main`, `richtungsfall.fall`, der Test (Gegenprobe K1 mit vertauschter Reihenfolge). | `research/mtm_drawdown/grundlage.py` Z. 198; `research/mtm_drawdown/messung.py` Z. 142; `research/mtm_drawdown/richtungsfall.py` Z. 65; `research/mtm_drawdown/test_mtm_kern.py` Z. 41–43, 101, 231–232, 236 | `ereignisse = mtm_kern.ereignisreihenfolge(pos, float(meta["startkapital"]))` / `pruefe(e["symbol"].tolist() == ["Q", "P"], "K1: Reihenfolge aus der Kette rekonstruiert (Q vor P)")` | belegt |

**Antwort zu (a):** Ja — `ereignisreihenfolge` gewinnt die Reihenfolge der Ausstiege **bei gleichem Zeitstempel** aus `capital_after` zurück (zusammen mit `allocation` und `pnl_pct`, Toleranz `KETTEN_TOLERANZ`); zwischen verschiedenen Zeitstempeln nimmt sie sie aus `exit_time` (Z. 99–119).

### (b) Hat eine ausgeführte Position genau einen Ausstieg? — je Bot

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| M3-10 | Jede Zeile der Trade-Tabelle hat genau eine `exit_time`; sie wird genau einmal in die Ausstiegsliste ihres Zeitpunkts eingetragen. | `shared/zuteilung.py` Z. 704; Z. 710–712 | `ausstieg = pd.to_datetime(trades["exit_time"]).to_numpy()` / `ausstiege_je_zeit.setdefault(ausstieg[pos], []).append(pos)` | belegt |
| M3-11 | Beim Ausstieg wird die ganze Allokation aus `open_positions` entfernt (`pop`); einen Teilausstieg gibt es nicht, ein zweiter Ausstieg derselben Position wird übersprungen. | Z. 725–730 | `if pos not in open_positions:` / `continue` / `allocation = open_positions.pop(pos)` | belegt |
| M3-12 | Ausstiege werden je Zeitpunkt vor Einstiegen verbucht. | Z. 722–724, 737 | `# --- Ausstiege zuerst: das Kapital wird frei -----------------------` | belegt |

| Bot | Antwort | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| `elliott_wave` | **genau einer** — `simulate_trade` gibt je Trade genau ein Ergebnis mit einer `exit_time` zurück (erste Stop-/Ziel-Kerze oder letzte Kerze der Haltedauer, nur Kerzen nach `entry_time`); ohne Ausstieg (`no_data`) entsteht kein Trade. Dazu M3-10/M3-11. | `strategies/elliott_wave/backtest_elliott.py` Z. 82–100; Z. 139–140; Z. 151–162 | `future = price_df[price_df["open_time"] > entry_time].head(max_hold_hours)` / `if outcome["exit_price"] is None or outcome["result"] == "no_data": continue` | erschlossen |
| `t3_supertrend` | **genau einer** — Zustandsmaschine mit höchstens einer offenen Position; beim ersten Ausstiegssignal eine Zeile, dann `position = None`; eine am Datenende offene Position wird nicht als Trade geschrieben. | `strategies/t3_supertrend/backtest_trend.py` Z. 105–135 | `if stop_hit or trend_flip or t3_crossed_down:` / `"exit_time": open_time[i],` / `position = None` | erschlossen |
| `rsi2_crypto` | **genau einer** — die innere Schleife bricht beim ersten Ausstieg ab; ohne Ausstieg endet der Scan (`break`), der Scan geht nach dem Ausstieg weiter. | `strategies/rsi2_crypto/backtest_rsi2.py` Z. 106–121; Z. 127–134 | `exit_idx, exit_price, result = idx, stop_price, "stop_loss"` / `break` / `if exit_idx is None: break` / `i = exit_idx + 1` | erschlossen |
| `turtle_soup_crypto` | **genau einer** — gleiche Bauart. | `strategies/turtle_soup_crypto/backtest_turtle_soup.py` Z. 153–165; Z. 171–178 | `if exit_idx is None:` / `break` / `i = exit_idx + 1` | erschlossen |
| `volatility_breakout_crypto` | **genau einer** — gleiche Bauart. | `strategies/volatility_breakout_crypto/backtest_breakout.py` Z. 156–168; Z. 174–181 | `if exit_idx is None:` / `break` / `i = exit_idx + 1` | erschlossen |
| `elliott_wave_stocks` | **genau einer** — wie `elliott_wave`. | `strategies/elliott_wave_stocks/backtest_elliott.py` Z. 91–109; Z. 151–152; Z. 163–174 | `future = price_df[price_df["open_time"] > entry_time].head(max_hold_hours)` / `continue` | erschlossen |
| `rsi2_mean_reversion` | **genau einer** — wie `rsi2_crypto`. | `strategies/rsi2_mean_reversion/backtest_rsi2.py` Z. 149–164; Z. 170–177 | `break  # nicht genug Restdaten, um diese Position zu schliessen - Scan beenden` / `i = exit_idx + 1  # kein Pyramiding` | erschlossen |
| `turtle_soup_stocks` | **genau einer** — wie `turtle_soup_crypto`. | `strategies/turtle_soup_stocks/backtest_turtle_soup.py` Z. 149–161; Z. 167–174 | `if exit_idx is None:` / `break` / `i = exit_idx + 1` | erschlossen |
| `volatility_breakout` | **genau einer** — wie `volatility_breakout_crypto`. | `strategies/volatility_breakout/backtest_breakout.py` Z. 197–209; Z. 215–222 | `break  # nicht genug Restdaten, um diese Position zu schliessen - Scan beenden` / `i = exit_idx + 1  # kein Pyramiding` | erschlossen |

Kette je Bot: Backtest-Modul (eine Zeile, eine `exit_time` je Trade) → `collect_all_trades` hängt die Zeilen nur zusammen (je `strategies/<Bot>/equity_simulation.py`, z. B. `elliott_wave` Z. 76–90; bei `t3_supertrend` und `volatility_breakout_crypto` filtert der Regimefilter nur ganze Zeilen weg, `t3_supertrend/equity_simulation.py` Z. 82–85, `volatility_breakout_crypto/equity_simulation.py` Z. 112–122; bei den vier Aktien-Bots werden Zeilen ohne Kurs ganz gestrichen, z. B. `rsi2_mean_reversion/equity_simulation.py` Z. 95–101) → `simuliere_portfolio` (M3-10, M3-11).

**Antwort zu (b):** Bei allen neun Bots hat eine ausgeführte Position **genau einen** Ausstieg (erschlossen aus den zitierten Zeilen; kein Lauf).

## M4 — Einstieg vor dem Handelbar-Tag

**Frage** (Antwort 09.10.a Z. 225, R87 (d)): ob der Scan eines geladenen Symbols vor dessen Handelbar-Tag einen Einstieg bilden kann. Nur das Ob, je Bot. Ob ein Fund Tatsachennotiz oder Register-Code-Widerspruch ist, sagt dieses Ergebnis nicht.

### Zugrunde gelegter Handelbar-Tag

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| M4-1 | Definition nach R87 (a): erster Tag, an dem die Historie des Symbols bis zu diesem Tag die Schranke des Bots nach 16.7 (b) erreicht. | `docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md` Z. 225, R87 (a) | `Handelbar-Tag eines Symbols für einen Bot ist der erste Tag, an dem seine Historie bis zu diesem Tag die Schranke des Bots nach 16.7 (b) erreicht (23.3)` | belegt |
| M4-2 | R87 (b): Die Lader entscheiden die Aufnahme einmal, an der ganzen Datei; ob der Signalpfad danach Einstiege vor dem Handelbar-Tag bildet, ist nicht gemessen. | dieselbe Datei Z. 225, R87 (b) | `Die Lader entscheiden die Aufnahme eines Symbols einmal, an der ganzen Datei (R83 (b))` | belegt |
| M4-3 | **Zugrunde gelegte Code-Stelle:** `faltenschranke_messung.loader_lesart` — Tagesspannen-Bots: erster Kurstag der Datei plus `MIN_HISTORY_DAYS`; `elliott_wave`: Tag der N-ten 1h-Kerze (`MIN_HISTORY_HOURS`). Die Schranke wird aus der `mso` des Bots gelesen. | `research/faltenplan_neun/faltenschranke_messung.py` Z. 223–258; Z. 147–162; Z. 165–217 | `aus["handelbar_ab"][symbol] = (erster + dt.timedelta(days=n)).isoformat()` / `aus["handelbar_ab"] = {s: (w["n_te_kerze_am"] if w else None)` | belegt |
| M4-4 | Für Aktien zählt dort der erste Kurstag der Datei, nicht der Zehnjahresanker. | dieselbe Datei Z. 248–253 | `Fuer "ab wann handelbar" zaehlt deshalb der erste Kurstag der Datei, nicht der Fensteranker - der Anker wird nur ausgewiesen.` | belegt |
| M4-5 | `benchmark.py` nimmt den Handelbar-Tag von dort und nennt dieselbe Definition. | `research/vorregistrierung/benchmark.py` Z. 50–60; Z. 102–104; Z. 268–271 | `Handelbar ist ein Symbol ab dem Tag, an dem seine Historie die registrierte Loader-Schranke erreicht` / `lesart = fsm.loader_lesart(bot)` | belegt |
| M4-6 | `faltenplan_neun.warm_ab` / `symbolbeginn` bestimmen den Tag des vollen **Indikator-Vorlaufs** (Lesart B), nicht den Handelbar-Tag nach der Loader-Schranke; sie werden hier nicht zugrunde gelegt. | `research/faltenplan_neun/faltenplan_neun.py` Z. 402–412; Z. 415–428 | `"""Ab wann das Symbol fuer diesen Bot handelbar ist (Lesart B).` / `Das Datum des Balkens, ab dem der Indikator-Vorlauf des Bots voll ist.` | belegt |
| M4-7 | `shared/kursdaten.py` streicht nur Zeilen ohne Kurse und zählt sie; ein Bezug zum Handelbar-Tag besteht nicht (das Wort steht nur im Docstring). | `shared/kursdaten.py` Z. 57–70; Z. 73–92; Z. 95–122 | `"""True je Zeile, in der mindestens eine der vier Kursspalten fehlt.` / `eine Kerze ohne Volumen, aber mit Kursen ist handelbar beschreibbar` | belegt |

### Je Bot: Lader → Scan → Einstieg

| Bot | Antwort | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| `elliott_wave` | **kann** — Lader prüft nur die Kerzenzahl der ganzen Datei; der Zigzag beginnt bei Balken 0, die Wellensuche hat keinen Startversatz, Einstieg am Bestätigungsbalken (`entry_idx`) ohne Prüfung gegen den Tag der N-ten Kerze; `collect_all_trades` übergibt keinen Schnitt. | `strategies/elliott_wave/multi_symbol_optimise.py` Z. 83–85, 101–112; `strategies/elliott_wave/zigzag_indicator.py` Z. 159–163; `strategies/elliott_wave/elliott_wave_counter.py` Z. 180, 342–358; `strategies/elliott_wave/backtest_elliott.py` Z. 123–126; `strategies/elliott_wave/equity_simulation.py` Z. 77–78 | `if len(df) < MIN_HISTORY_HOURS:` / `for i in range(len(zigzag) - 5):` / `row["entry_idx"] = int(run_bar)` / `entry_time = pd.to_datetime(price_df["open_time"].iloc[entry_idx])` | erschlossen |
| `t3_supertrend` | **kann** — Lader prüft die Zeitspanne der ganzen Datei; der Scan läuft ab Balken 1, Einstieg sobald Kreuzung und ADX-Bedingung gelten; der Regimefilter streicht nur nach dem BTC-Regime. | `strategies/t3_supertrend/multi_symbol_optimise.py` Z. 79–82, 94–100; `strategies/t3_supertrend/backtest_trend.py` Z. 101–114; `strategies/t3_supertrend/equity_simulation.py` Z. 64–65, 82–85 | `timespan_days = (df["open_time"].max() - df["open_time"].min()).days` / `for i in range(1, len(data)):` / `"entry_time": open_time[i],` | erschlossen |
| `rsi2_crypto` | **kann** — Lader prüft die Zeitspanne der ganzen Datei (`MIN_HISTORY_DAYS = 500`); der Scan beginnt bei Balken `sma_trend_period` (Rasterwerte 100/150/200 Balken); `collect_all_trades` übergibt keinen `entry_cutoff`. | `strategies/rsi2_crypto/multi_symbol_optimise.py` Z. 47, 56, 85–88, 96–99; `strategies/rsi2_crypto/backtest_rsi2.py` Z. 86–88, 91–101; `strategies/rsi2_crypto/equity_simulation.py` Z. 63 | `MIN_HISTORY_DAYS = 500` / `start_i = sma_trend_period` / `trades = get_trades_for_symbol(price_df, rsi_threshold, sma_trend_period, stop_loss_pct)` | erschlossen |
| `turtle_soup_crypto` | **kann** — Lader wie `rsi2_crypto` (`MIN_HISTORY_DAYS = 500`); Scan ab `WARMUP_PERIOD + donchian_period` Balken; kein `entry_cutoff`. | `strategies/turtle_soup_crypto/multi_symbol_optimise.py` Z. 33, 39, 67–70, 77–80; `strategies/turtle_soup_crypto/backtest_turtle_soup.py` Z. 100, 104, 124–126, 129–142; `strategies/turtle_soup_crypto/equity_simulation.py` Z. 54 | `start_i = WARMUP_PERIOD + donchian_period` / `trades = get_trades_for_symbol(price_df, donchian_period, stop_mode)` | erschlossen |
| `volatility_breakout_crypto` | **kann** — Lader wie oben (`MIN_HISTORY_DAYS = 500`); Scan ab `BB_PERIOD + squeeze_lookback_days - 1` Balken (Vorlauf in Balken laut `faltenplan_neun.py` Z. 197–201 kleiner als die Schranke in Tagen); kein `entry_cutoff`. | `strategies/volatility_breakout_crypto/multi_symbol_optimise.py` Z. 41, 70–73, 81–93; `strategies/volatility_breakout_crypto/backtest_breakout.py` Z. 128–131, 134–152; `strategies/volatility_breakout_crypto/equity_simulation.py` Z. 73–75; `research/faltenplan_neun/faltenplan_neun.py` Z. 197–201 | `start_i = BB_PERIOD + squeeze_lookback_days - 1` / `trades = get_trades_for_symbol(price_df, stop_loss_pct, max_hold_days, use_volume_filter,` | erschlossen |
| `elliott_wave_stocks` | **kann** — Lader schneidet auf die letzten `RECENT_YEARS_ONLY` Jahre und prüft dann die Zeitspanne (`MIN_HISTORY_DAYS = 1825`); beginnt die Datei innerhalb dieses Fensters, bleibt sie ganz, und Zigzag/Wellensuche beginnen bei Balken 0 ohne Prüfung gegen „erster Kurstag + 1825 Tage“ (M4-4). | `strategies/elliott_wave_stocks/multi_symbol_optimise.py` Z. 52, 54, 92–99, 115–126; `strategies/elliott_wave_stocks/zigzag_indicator.py` Z. 134–136; `strategies/elliott_wave_stocks/elliott_wave_counter.py` Z. 180, 342–358; `strategies/elliott_wave_stocks/backtest_elliott.py` Z. 132–135; `strategies/elliott_wave_stocks/equity_simulation.py` Z. 85 | `df = df[df["open_time"] >= cutoff].reset_index(drop=True)` / `if timespan_days < MIN_HISTORY_DAYS:` / `row["entry_idx"] = int(run_bar)` | erschlossen |
| `rsi2_mean_reversion` | **kann** — Lader prüft die Zeitspanne der ganzen Datei (`MIN_HISTORY_DAYS = 1825`), `entry_cutoff` = letzter Kurstag minus `RECENT_YEARS_ONLY`; der Scan beginnt bei `max(sma_trend_period, Zeilen vor entry_cutoff)`. Liegt der erste Kurstag nach `entry_cutoff`, beginnt der Scan bei Balken `sma_trend_period`. | `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` Z. 51–52, 86–96, 110–112; `strategies/rsi2_mean_reversion/backtest_rsi2.py` Z. 129–131, 134–146, 166; `strategies/rsi2_mean_reversion/equity_simulation.py` Z. 73–75 | `entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)` / `start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))` | erschlossen |
| `turtle_soup_stocks` | **kann** — Lader wie `rsi2_mean_reversion`; Scan ab `max(WARMUP_PERIOD + donchian_period, Zeilen vor entry_cutoff)`. | `strategies/turtle_soup_stocks/multi_symbol_optimise.py` Z. 45–46, 74–83, 89–92; `strategies/turtle_soup_stocks/backtest_turtle_soup.py` Z. 120–122, 125–138, 163; `strategies/turtle_soup_stocks/equity_simulation.py` Z. 78–79 | `start_i = WARMUP_PERIOD + donchian_period` / `start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))` | erschlossen |
| `volatility_breakout` | **kann** — Lader wie `rsi2_mean_reversion`; Scan ab `max(BB_PERIOD + squeeze_lookback_days - 1, Zeilen vor entry_cutoff)` (Vorlauf in Balken laut `faltenplan_neun.py` Z. 220–224). | `strategies/volatility_breakout/multi_symbol_optimise.py` Z. 49–50, 82–92, 107–110; `strategies/volatility_breakout/backtest_breakout.py` Z. 169–172, 176–194, 211; `strategies/volatility_breakout/equity_simulation.py` Z. 74–77; `research/faltenplan_neun/faltenplan_neun.py` Z. 220–224 | `start_i = BB_PERIOD + squeeze_lookback_days - 1` / `if entry_cutoff is None or entry_time >= np.datetime64(entry_cutoff):` | erschlossen |

**Kette, die für alle neun gilt:** Der Lader entscheidet an der ganzen (bei `elliott_wave_stocks`: auf das Zehnjahresfenster geschnittenen) Reihe, ob das Symbol aufgenommen wird; danach kennt der Scan nur seinen Indikator-Vorlauf (`start_i` bzw. Balken 0/1) und — bei den Aktien-Bots — `entry_cutoff`. Keine der gelesenen Stellen von Scan und Einstieg vergleicht `entry_time` mit dem Tag „erster Kurstag + Schranke“. Der Vorlauf in Balken ist bei jedem Bot kürzer als die Schranke in Tagen bzw. Kerzen (Vorlauf je Bot in `research/faltenplan_neun/faltenplan_neun.py` Z. 173–226; bei den zwei Breakout-Bots mit der Voreinstellung von `squeeze_lookback_days`), also kann der Scan eines geladenen Symbols vor dessen Handelbar-Tag einen Einstieg bilden.

**Antwort:** **kann** — bei allen neun Bots (erschlossen aus den zitierten Zeilen; ob ein solcher Einstieg in den Daten tatsächlich vorkommt, beantwortet nur ein Lauf und ist nicht gefragt).

## M5 — Quelle des Handelbar-Tags

**Frage** (Antwort 09.10.a, „Unsicher“ Nr. 7, Z. 206), in der vorläufigen Lesart des steuernden Chats: ob die vorhandene Benchmark-Rechnung den Handelbar-Tag je Symbol herausgibt, und wo; für beide Funktionen `bh_tagesrenditen`.

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|
| M5-1 | `benchmark.bh_tagesrenditen` gibt den Handelbar-Tag **nicht** heraus: Eingabe ist ein Dict von Kursreihen, Rückgabe eine `pd.Series` der gleichgewichteten Tagesrenditen. | `research/vorregistrierung/benchmark.py` Z. 191; Z. 204–205 | `def bh_tagesrenditen(reihen: dict) -> pd.Series:` / `return rahmen.pct_change().mean(axis=1, skipna=True).dropna()` | belegt |
| M5-2 | Der Handelbar-Tag wirkt dort nur mittelbar: Die Reihen sind vorher in `tagesgenau` ab dem Handelbar-Tag geschnitten; auch `tagesgenau` gibt den Tag nicht zurück, nur die geschnittenen Reihen. | Z. 164; Z. 180–188 | `def tagesgenau(reihen: dict, handelbar: dict) -> dict:` / `r = r[r.index >= ab]` / `return aus` | belegt |
| M5-3 | Den Tag **hält** `faltenschranke_messung.loader_lesart`: Rückgabe-Dict mit dem Feld `handelbar_ab` (Symbol → ISO-Datum oder `None`). | `research/faltenplan_neun/faltenschranke_messung.py` Z. 223; Z. 232; Z. 235–236; Z. 253; Z. 258 | `aus = {"schranke": name, "wert": n, "handelbar_ab": {}}` / `aus["handelbar_ab"][symbol] = (erster + dt.timedelta(days=n)).isoformat()` / `return aus` | belegt |
| M5-4 | `benchmark.je_bot` ruft `loader_lesart` je Bot, bildet daraus `handelbar` (Symbol → `pd.Timestamp`), schneidet mit `tagesgenau` und ruft dann die eigene `bh_tagesrenditen`. | `research/vorregistrierung/benchmark.py` Z. 268–272 | `lesart = fsm.loader_lesart(bot)` / `handelbar = {s: pd.Timestamp(d) for s, d in lesart["handelbar_ab"].items() if d}` / `renditen = bh_tagesrenditen(reihen)` | belegt |
| M5-5 | **Ja, die Benchmark-Rechnung gibt den Tag je Symbol heraus:** `je_bot` legt `handelbar_ab` in den Eintrag des Bots (Symbol → ISO-Datum, sortiert); der Eintrag ist Teil des Rückgabewerts von `je_bot`. | Z. 276; Z. 320–321 | `eintrag["handelbar_ab"] = dict(sorted(lesart["handelbar_ab"].items()))` / `aus[bot] = eintrag` / `return aus` | belegt |
| M5-6 | Form in der Datei: `main` gibt den Rückgabewert von `je_bot` an `schreibe_tabellen`, das ihn als JSON schreibt — `handelbar_ab` steht damit je Bot in der geschriebenen Tabellendatei (Voreinstellung `ergebnisse/benchmark_drawdowns_<UTC-Stempel>.json`). | Z. 436–437; Z. 397–398; Z. 359–360 | `tabellen = je_bot(mess)` / `rc, text = schreibe_tabellen(tabellen, ziel)` / `json.dump(tabellen, f, indent=1, ensure_ascii=False, sort_keys=True)` | erschlossen (aus M5-5 und diesen Zeilen; keine Ergebnisdatei geöffnet) |
| M5-7 | `exposure_kern.bh_tagesrenditen` gibt den Handelbar-Tag ebenfalls **nicht** heraus und kennt ihn nicht: Eingabe ein Dict von Kursreihen, Rückgabe eine `pd.Series`; kein Schnitt nach einem Handelbar-Tag. | `research/exposure_messung/exposure_kern.py` Z. 211; Z. 220–222 | `def bh_tagesrenditen(kurse_je_symbol: dict) -> pd.Series:` / `renditen = rahmen.pct_change()` / `return renditen.mean(axis=1, skipna=True).dropna()` | belegt |
| M5-8 | Ihre Aufrufer sind die Exposure-Auswertung (Kurse aus `lade_kurse`, ohne Handelbar-Tag) und der Test. | `research/exposure_messung/auswertung.py` Z. 454–456; `research/exposure_messung/test_exposure_kern.py` Z. 146 | `kurse, fehlend = lade_kurse(symbolliste(datei))` / `renditen = ek.bh_tagesrenditen(kurse)` / `r_bh = ek.bh_tagesrenditen(kurse)` | belegt |
| M5-9 | **Welche Funktion die Benchmark-Rechnung ruft:** die eigene `benchmark.bh_tagesrenditen` (Aufruf ohne Modulpräfix in `je_bot`), nicht die aus `exposure_kern`; `benchmark.py` importiert `exposure_kern` nicht. | `research/vorregistrierung/benchmark.py` Z. 82–104 (Importe); Z. 272 | `renditen = bh_tagesrenditen(reihen)` | belegt |
| M5-10 | Der Docstring von `benchmark.bh_tagesrenditen` nennt die Rechnung „zeichengleich“ zu `exposure_kern.py`; der Wortlaut der Rümpfe ist verschieden gesetzt (eine Zeile gegen zwei), die Aufrufkette `pct_change` → `mean(axis=1, skipna=True)` → `dropna()` ist dieselbe. | `research/vorregistrierung/benchmark.py` Z. 200–205; `research/exposure_messung/exposure_kern.py` Z. 220–222 | `Zeichengleich zu research/exposure_messung/exposure_kern.py - dieselbe Rechnung` | belegt |

**Antwort:** Die vorhandene Benchmark-Rechnung gibt den Handelbar-Tag je Symbol heraus — **nicht** über `bh_tagesrenditen` (keine der beiden gleichnamigen Funktionen tut es), sondern in `research/vorregistrierung/benchmark.py::je_bot` Z. 276 als Feld `handelbar_ab` (Symbol → ISO-Datum) im Rückgabewert und, über `main` Z. 436–437 und `schreibe_tabellen` Z. 398, in der geschriebenen JSON-Datei. Gehalten wird der Tag von `research/faltenplan_neun/faltenschranke_messung.py::loader_lesart` (Feld `handelbar_ab`, Z. 232–258). Die Benchmark-Rechnung ruft ihre eigene `bh_tagesrenditen` (Z. 272).

## Leseprotokoll

Wie der Beleg `docs/belege/TB-148/leseprotokoll.md`; Zeilen und md5 aus D0 (`lese_zeilen.txt`, `lese_md5.txt`, je `rc 0`).

| Datei | Zeilenbereich | Messpunkt | Zeilen | md5 |
|---|---|---|---:|---|
| `shared/zuteilung.py` | 1–798 (ganz) | M1 (auch M2, M3) | 798 | `ecb2af91a29577914b052feb5574e279` |
| `strategies/elliott_wave/equity_simulation.py` | 1–195 (ganz) | M1 (auch M3, M4) | 195 | `d420d096e9e14832816ca055cfcb39cd` |
| `strategies/t3_supertrend/equity_simulation.py` | 25–139 | M1 (auch M3, M4) | 187 | `e65e06cef898272187138cd84467b7c5` |
| `strategies/rsi2_crypto/equity_simulation.py` | 25–134 | M1 (auch M3, M4) | 177 | `62a78c697cb30ccd18d44605083ec137` |
| `strategies/turtle_soup_crypto/equity_simulation.py` | 25–119 | M1 (auch M3, M4) | 160 | `a2ac6fa97c8d9eadf072b36054dd2ad7` |
| `strategies/volatility_breakout_crypto/equity_simulation.py` | 1–170 | M1 (auch M3, M4) | 227 | `91d6568fc034dec82b32dbb29af07096` |
| `strategies/elliott_wave_stocks/equity_simulation.py` | 1–165 | M1 (auch M3, M4) | 235 | `9f0fe8aa04224cfcffadbcdd08d1fa0c` |
| `strategies/rsi2_mean_reversion/equity_simulation.py` | 1–165 | M1 (auch M3, M4) | 212 | `774e7fecad93bdad38bcba5e568b7243` |
| `strategies/turtle_soup_stocks/equity_simulation.py` | 1–150 | M1 (auch M3, M4) | 199 | `f45e55aadcb9d03b4342ec32e8644914` |
| `strategies/volatility_breakout/equity_simulation.py` | 1–150 | M1 (auch M3, M4) | 200 | `dd5fa96bb927aecb26051fbaefb4a0cd` |
| `research/vorregistrierung/registerdaten.py` | 80–144 | M2 | 633 | `b1df43ac7b4408dcf8780bb44c97110f` |
| `research/faltenplan_neun/faltenplan_neun.py` | 80–484; 555–629 | M2 (auch M4) | 634 | `329f671da5b7cd6d6179b22a16c59537` |
| `research/vorregistrierung/faltenplan.py` | 1–490 | M2 | 491 | `27c2d93577227a0199e266dbee7097cd` |
| `research/faltenplan_neun/erste_falte_trockenlauf.py` | 1–331 (ganz) | M2 | 331 | `fb320cfc5c1380d322d91349f97102a1` |
| `research/faltenplan_neun/faltenschranke_messung.py` | 1–533 (ganz) | M2 (auch M4, M5) | 533 | `6a72fd8833290860b9dad8929782cd38` |
| `research/vorregistrierung/registerbericht.py` | 115–154 | M2 | 218 | `dcc23096e84558c357cac6ca52667737` |
| `research/universum_trockenlauf/universum_trockenlauf.py` (weitere Datei) | 1–400 | M2 | 810 | `923ef7758c349cd8903f464758d8b09d` |
| `research/universum_trockenlauf/loaderlauf.py` (weitere Datei) | 1–645 (ganz) | M2 | 645 | `5032ace22ceb41efda2460a0b22026ea` |
| `strategies/elliott_wave/multi_symbol_optimise.py` | 1–120 | M2 (auch M4) | 242 | `dc458cde8374d1a7d05c74ca81444484` |
| `strategies/t3_supertrend/multi_symbol_optimise.py` | 1–105 | M2 (auch M4) | 239 | `bd9259fcbb4357663d1759d11aa5e9d6` |
| `strategies/rsi2_crypto/multi_symbol_optimise.py` | 1–105 | M2 (auch M4) | 193 | `d4fdbd57a35f95babbd5127ff24d896a` |
| `strategies/turtle_soup_crypto/multi_symbol_optimise.py` | 1–85 | M2 (auch M4) | 167 | `442032ab0eb268e2b9b7f21b9be9815d` |
| `strategies/volatility_breakout_crypto/multi_symbol_optimise.py` | 1–96 | M2 (auch M4) | 179 | `4f32fc9e0396c6adbffd6067dea16202` |
| `strategies/elliott_wave_stocks/multi_symbol_optimise.py` | 1–130 | M2 (auch M4) | 267 | `32aabbda9d3a4fbc297ea7bb423a5152` |
| `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` | 1–115 | M2 (auch M4) | 218 | `57ab12ab0a357bfb1a5c0241071ccc1e` |
| `strategies/turtle_soup_stocks/multi_symbol_optimise.py` | 1–95 | M2 (auch M4) | 179 | `77cfcfe57c391b5ff626a5ad56fb317a` |
| `strategies/volatility_breakout/multi_symbol_optimise.py` | 1–112 | M2 (auch M4) | 214 | `66ce8cc780e7277e155f4a2f003e3896` |
| `shared/fetch_binance_data.py` | 85–129; 300–349 | M2 | 384 | `528f59408a99ead52ffb4e9524693b79` |
| `shared/binance_historie.py` | 90–109; 260–339; 475–599 | M2 | 830 | `8cbad1fe58ca908e90578c930b93ae1b` |
| `strategies/elliott_wave_stocks/fetch_stock_data.py` | 1–147 (ganz) | M2 | 147 | `46f4fe6fedf830aebea6a55a9bf08fe0` |
| `shared/abrufschutz.py` | 1–230 | M2 | 574 | `f8f7c5c470b81eabd103f3819c31ac67` |
| `shared/kursdaten.py` | 1–170 | M2 (auch M4) | 189 | `764318a64279c9a28e09beae0ed0da10` |
| `strategies/elliott_wave/backtest_elliott.py` | 1–215 | M2 (auch M3, M4) | 230 | `df5c314e9268bf5c51a5210113e27082` |
| `strategies/t3_supertrend/backtest_trend.py` | 1–140 | M2 (auch M3, M4) | 159 | `689d648d2599d2e54eb77dca26ced888` |
| `strategies/rsi2_crypto/backtest_rsi2.py` | 55–154 | M2 (auch M3, M4) | 156 | `35929d647c8b62ca7d59ec6e79120b37` |
| `strategies/turtle_soup_crypto/backtest_turtle_soup.py` | 95–194 | M2 (auch M3, M4) | 201 | `9ed99ea5d2fe16f9aed85b51752613a4` |
| `strategies/volatility_breakout_crypto/backtest_breakout.py` | 60–199 | M2 (auch M3, M4) | 203 | `4dcc955886faecf61c138e74506f7237` |
| `strategies/elliott_wave_stocks/backtest_elliott.py` | 60–179 | M2 (auch M3, M4) | 242 | `f1979557a945822dfbe623e0d80ca531` |
| `strategies/rsi2_mean_reversion/backtest_rsi2.py` | 90–184 | M2 (auch M3, M4) | 199 | `1fb6254c25aa2b169c3444b891842af5` |
| `strategies/turtle_soup_stocks/backtest_turtle_soup.py` | 95–179 | M2 (auch M3, M4) | 197 | `14f1c0f899975d196907b6579ad09dab` |
| `strategies/volatility_breakout/backtest_breakout.py` | 110–239 | M2 (auch M3, M4) | 244 | `8453b945e83ffe400d80ada6bff0ff2d` |
| `strategies/elliott_wave/multi_symbol_walk_forward.py` | 38–57 | M2 | 107 | `cd62a4af8a07f097f9952661dd07fea8` |
| `strategies/t3_supertrend/multi_symbol_walk_forward.py` | 34–51 | M2 | 90 | `8cb107ed60f5772dc6ec51d052be52d5` |
| `strategies/rsi2_crypto/multi_symbol_walk_forward.py` | 1–60 | M2 | 157 | `25f79142a9e28848df2e1a116ab9436c` |
| `strategies/turtle_soup_crypto/multi_symbol_walk_forward.py` | 14–31 | M2 | 138 | `22efed0c3b0d15f37f737b639b63884e` |
| `strategies/volatility_breakout_crypto/multi_symbol_walk_forward.py` | 1–50 | M2 | 142 | `13222d1647e90347bcb4da942abaece1` |
| `strategies/elliott_wave_stocks/multi_symbol_walk_forward.py` | 38–57 | M2 | 109 | `4f22493439d1d1b884e68ec2e4b81ac8` |
| `strategies/rsi2_mean_reversion/multi_symbol_walk_forward.py` | 1–70 | M2 | 168 | `19355e0d57c3b24e581c67f863ad7c40` |
| `strategies/turtle_soup_stocks/multi_symbol_walk_forward.py` | 14–31 | M2 | 138 | `edb6f88ed1a9e185414829b814816423` |
| `strategies/volatility_breakout/multi_symbol_walk_forward.py` | 1–60 | M2 | 153 | `0ab5fc0cd110e6181651fd34fd2baa1a` |
| `strategies/t3_supertrend/regime_filter.py` | 1–47 (ganz) | M2 (auch M3, M4) | 47 | `b02087926d7d6b376a47b19115f1ca58` |
| `strategies/volatility_breakout_crypto/regime_filter.py` | 1–43 (ganz) | M2 (auch M3, M4) | 43 | `9de449f6a4a63d73efafc9126a2c5145` |
| `strategies/rsi2_crypto/indicators.py` | 80–101 | M2 | 101 | `a34eb5905969d19827b0f93b6b154132` |
| `strategies/volatility_breakout_crypto/indicators.py` | 68–88 | M2 | 88 | `f44634e6226adaea67646de28903a012` |
| `strategies/elliott_wave/zigzag_indicator.py` | 25–214 | M2 (auch M4) | 216 | `6e9a91ccc131937079b602be875fa0dd` |
| `strategies/elliott_wave_stocks/zigzag_indicator.py` | 36–43; 132–137; 204–208 | M2 (auch M4) | 216 | `407cd69fb5c2181c5316e008ea7b7d81` |
| `research/vorregistrierung/benchmark.py` | 1–460 | M2 (auch M4, M5) | 463 | `6ca4ede617165d881623465244649c1d` |
| `research/mtm_drawdown/mtm_kern.py` | 1–135 | M3 | 339 | `fcf7a1ef7585d1ec78247031851fa85e` |
| `research/mtm_drawdown/grundlage.py` | 1–214 | M3 | 272 | `81cf1c93243a8248b96cf072e07fc289` |
| `research/mtm_drawdown/messung.py` | 60–159 | M3 | 240 | `00eb23079f1b92532f48f099f74dbe2f` |
| `research/mtm_drawdown/richtungsfall.py` | 50–79 | M3 | 150 | `77a7c08dc6094818d01d0667a9ccf4ab` |
| `research/mtm_drawdown/test_mtm_kern.py` | 30–109; 220–244 | M3 | 264 | `80f1511a18d26a61537748c2739d0d79` |
| `strategies/elliott_wave/elliott_wave_counter.py` (weitere Datei) | 1–381 (ganz) | M4 | 381 | `e483aad3e62483cb6f730f255b0ae12e` |
| `strategies/elliott_wave_stocks/elliott_wave_counter.py` (weitere Datei) | 160–189; 305–374 | M4 | 381 | `b5dcf72fa38abc7c4ddeeb8f3a84b42f` |
| `research/exposure_messung/exposure_kern.py` | 195–226 | M5 | 228 | `5d182d05464fea15cef5c40211eba45b` |
| `research/exposure_messung/auswertung.py` | 420–479 | M5 | 561 | `bf011dee838beb9c8b770ed85fa6c0dd` |
| `research/exposure_messung/test_exposure_kern.py` | 135–154 | M5 | 161 | `68bec9c679926e97136e2a87ec643f39` |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md` (weitere Datei) | 195–233 | M3, M4, M5 | 233 | `a6e5d3d277c5d4069b443a8f8f9df17f` |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` (Steuerdatei) | 1–98 (ganz) | — | 98 | `8f0a1160a0db9c0faab59f8e486a4c1d` |
| `docs/auftraege/MAC_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md` (Auftrag) | 1–373 (ganz) | — | 373 | `9c14bb54a59170893d316ac22af29e3e` |

Vermerke ‚Ergebniszahl im Quelltext, nicht wiedergegeben‘ (Datei:Zeile): `shared/zuteilung.py:18–19, 112, 151, 490, 589–591, 597`; `strategies/elliott_wave/equity_simulation.py:103–104`; `strategies/t3_supertrend/equity_simulation.py:50`; `strategies/rsi2_crypto/equity_simulation.py:91`; `strategies/turtle_soup_crypto/equity_simulation.py:78`; `strategies/elliott_wave_stocks/equity_simulation.py:125–127`; `strategies/rsi2_mean_reversion/equity_simulation.py:119–127`; `strategies/turtle_soup_stocks/equity_simulation.py:57`; `research/faltenplan_neun/faltenplan_neun.py:92–93`; `research/vorregistrierung/faltenplan.py:38–41, 55–59`; `research/universum_trockenlauf/universum_trockenlauf.py:20, 25–26`; `shared/abrufschutz.py:20`; `shared/kursdaten.py:15–16, 21–22`; `strategies/elliott_wave/backtest_elliott.py:26`; `research/vorregistrierung/benchmark.py:38, 43–46, 58`; `strategies/elliott_wave/elliott_wave_counter.py:34–35, 41–43, 61, 223`. Parameterwerte in Kommentaren (aus oder gegen `live_params.py`) sind im Beleg mit Ort genannt und nirgends wiedergegeben.

## Belege

| Datei | Befehl | Bytes | md5 |
|---|---|---:|---|
| `docs/belege/TB-148/0a_status.txt` | `git status --porcelain > "$TMPDIR/tb148_0a.txt"`, dann `cp` (Schritt A), `cmp` ohne Ausgabe | 156 | `987c5f2ff02666d72f30e8b84467892d` |
| `docs/belege/TB-148/a_modus.txt` | Prozesskette (Schritt A), Ausgabe wörtlich mit dem Schreibwerkzeug abgelegt, dazu die Aussage der Sitzung | 274 | `563de10414cad08902dc0bd1a27a561b` |
| `docs/belege/TB-148/m1_fundstellen.md` | Schreibwerkzeug | 5092 | `19b648f92c9d8a8981460e2aaa17a814` |
| `docs/belege/TB-148/m2_fundstellen.md` | Schreibwerkzeug | 11139 | `658c8c87afe74adc0eb94e23a01a1efd` |
| `docs/belege/TB-148/m3_fundstellen.md` | Schreibwerkzeug | 9186 | `1762806eab0f4b76fa352b1007d7d4ed` |
| `docs/belege/TB-148/m4_fundstellen.md` | Schreib- und Bearbeitungswerkzeug | 10416 | `5b46e3743062a3015736a21c1da98816` |
| `docs/belege/TB-148/m5_fundstellen.md` | Schreibwerkzeug | 5315 | `563f82f1b62a8eb6231113901b74b014` |
| `docs/belege/TB-148/leseprotokoll.md` | Schreib- und Bearbeitungswerkzeug, nach jedem Messpunkt fortgeschrieben, Zeilen und md5 aus D0 nachgetragen | 13064 | `a1a324e02f06e2fc311ec26ca3b0ba74` |
| `docs/belege/TB-148/lese_zeilen.txt` | D0, erster Block (`wc -l` über 63 Startdateien und 7 weitere) | 4050 | `24f78596964303ff289886ef192a6129` |
| `docs/belege/TB-148/lese_md5.txt` | D0, zweiter Block (`md5` über dieselben 70 Dateien) | 6275 | `15e0a0795b78646ebd6b0afb568563c2` |
| `docs/belege/TB-148/f_porcelain.txt` | D3, nach der Abgabe | siehe Schlussmeldung | — |
| `docs/belege/TB-148/f_numstat.txt` | D3, nach der Abgabe (`git diff --numstat ⟨S0⟩ ⟨F⟩`) | siehe Schlussmeldung | — |

## Abweichungen vom Auftrag

1. **Suchwerkzeug nicht verfügbar.** Der Auftrag sieht vor, mit dem Suchwerkzeug von Claude Code zu suchen. Der Aufruf ergab: „No such tool available: Grep. Grep is not available in this session — search file contents with `grep` via the Bash tool instead.“ Ein `grep`-Befehl über die Shell steht im Auftrag nicht wörtlich und wäre ein selbst gebauter Befehl gewesen (verboten unter „Nicht erlaubt“). Die Sitzung hat deshalb **nicht gesucht, sondern gelesen** (Lesewerkzeug, Datei und Zeilenbereich). Folge: Aussagen der Form „an keiner Stelle“ stützen sich auf die gelesenen Bereiche und stehen als „erschlossen“ (M2-25; Kette in M4).
2. **Weitere gelesene Dateien unter `research/`, die der Auftrag nicht nennt:** `research/universum_trockenlauf/universum_trockenlauf.py` und `research/universum_trockenlauf/loaderlauf.py` (Aufrufen aus `erste_falte_trockenlauf.py` gefolgt), dazu `strategies/elliott_wave/elliott_wave_counter.py`, `strategies/elliott_wave_stocks/elliott_wave_counter.py` und `docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_…md` (Z. 195–233, Quelle von R87 (a), (b)). Gelesen, nicht durchsucht; in beiden Blöcken von D0 hinter der letzten Startdatei angehängt, ebenso die zwei Steuerdateien `AKTUELLER_AUFTRAG.md` und der Auftrag selbst. Keine liegt auf dem gültigen Sperrlisten-Abbild als Schreibziel; geändert wurde keine.
3. **Zeilenangaben des Auftrags:** An allen angesteuerten Stellen stand der genannte Name an der genannten Zeile; keine Abweichung gefunden.

Geprüfte Sollwerte ohne Abweichung: 0a (HEAD und drei Einträge), `cmp` in A ohne Ausgabe, Modus `manual` in A, je Messpunkt ein Commit mit Push (M1 bis M5), D0 je `rc 0`, Journal-Kennung EN wie erwartet (letzter Block EM an Z. 10332, `## Wiederkehrende Lehren` an Z. 10376). D3 wird nach der Abgabe gemessen; Abweichungen dort nennt die Schlussmeldung.

## Nicht getan

- Kein Programm des Repos ausgeführt oder importiert; kein Interpreter.
- Keine Trade-Liste, nichts unter `ergebnisse/`, `data/`, `snapshots/`, `logs/`, `research/tb24_haltedauern/daten/` geöffnet; keine Ergebniszahl eines Laufs genannt; aus `live_params.py` kein Text.
- Keine Datei ausserhalb von `docs/` geändert; `shared/zuteilung.py` (Punkt 10) und die übrigen Dateien der Sperrliste nur gelesen.
- Keine Unter-Agenten, kein Hilfsskript, nichts ins Scratchpad geschrieben (nur `$TMPDIR/tb148_*.txt` wie vorgegeben).
- Kein Urteil über Folgen: ob M4 eine Tatsachennotiz oder ein Register-Code-Widerspruch ist, ob der Erzeuger `ereignisreihenfolge` übernimmt (M3) oder was aus M2 folgt, entscheidet der Verfahrensprüfer.
- Nicht in TB-148 (Auftrag): Registereintrag R84 bis R89, Bau der zwei Erzeuger, Neuerzeugung der Listen, Frage an den Verfahrensprüfer, `BACKLOG.md`, Dialog-Index, Registerkopie, `UEBERGABE.md` nach Schritt 0, wie oft der Schlüssel aus M1 entscheidet.

## In einfacher Sprache

Fünf Fragen des Verfahrensprüfers sind jetzt durch Lesen des Codes beantwortet, jede mit den Zeilen, an denen es steht. **Gleichstand:** Wenn mehrere Käufe gleichzeitig um den letzten Platz konkurrieren und alles andere gleich ist, entscheidet ein fester „Würfel“ — ein Prüfwert, gebildet aus den Daten des Trades und einer festen Startzahl, nicht aus einem einzelnen Feld wie dem Ausstiegskurs. **Zeitzone:** Weder die Kurszeiten noch der Stichtag des Echtbetriebs tragen im Code eine Zeitzone; bei Krypto sind die Kurszeiten UTC, bei Aktien legt das die Datenquelle fest, und der Stichtag ist ein blosses Datum — ob beide dieselbe Zeitzone meinen, lässt sich durch Lesen nicht entscheiden. **Verkäufe:** Die Messrechnung findet die Reihenfolge gleichzeitiger Verkäufe, indem sie die Kapitalstände nachrechnet; jede Position hat bei allen neun Bots genau einen Verkauf. **Handelbar-Tag:** Jeder der neun Bots kann eine Münze oder Aktie kaufen, bevor sie nach der Regel als handelbar gilt, weil der Lader nur einmal auf die ganze Datei schaut und der Scan danach früher beginnt. **Quelle des Tags:** Die Vergleichsrechnung gibt diesen Tag je Wert heraus — aber nicht in der Funktion, die im Antworttext genannt ist, sondern ein Stück daneben, in ihrer Tabelle je Bot. Was daraus folgt, entscheidet der Verfahrensprüfer.
