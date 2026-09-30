# TB-124: Ergebnis. F1 — Scanbeginn der Volatility-Breakout-Bots an `bb_lookback` gebunden, nach Nachtrag 1 (Fable 30a, R53) am Vorlauf der Zelle; mit Voreinstellungen 13/13 bytegleich, Wertprobe 43/43 und 42/42 mit Gegenprobe rc 1; `test_sync_check` wieder 33/0; R28-Probe `snapshot.py` gegen Register 18

**Sitzungstitel:** `TB-124` · **Stand:** 30.09.2026 · **Auftrag:** `docs/auftraege/MAC_TB-124_scanbeginn_sync_r28.md`,
dazu `docs/auftraege/NACHTRAG_1_MAC_TB-124_scanbeginn_vorlauf.md` (während des Laufs eingegangen, vor Schritt B
gelesen und umgesetzt) · **Belege:** `docs/belege/TB-124/`
**Eingang:** `0034960` (TB-123). **Commits:** `baf18a2` (Schritt 0), `808aa47` (Nachtrag 1: Fable 30a, 0c, BACKLOG,
Herleitung), `f6aaf33` (0: Ausgang, db, Datenstand, Basislauf), `105419e` (A), `f90135e` (B), `499d68b` (C), `7453469`
(D), `65fcaf0` (C3-Belege), der Abgabe-Commit und `e_porcelain.txt`. Alle gepusht.
**Freigabe** (wörtlich im Auftrag): 30.09.2026, 19:13 (*„Wir setzten es wie von dir Vorgeschlagen um“*), Nachtrag
19:44 (Auswahlkarte „Ja, zwei Testdateien (Empfohlen)“). **Handwerksvorgabe:** Nachtrag 1 des steuernden Chats,
30.09.2026, ca. 20:15, nach Fable 30a R53.
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6, pandas 2.3.3), ohne Modus. **Kein Abbruchkriterium ausgelöst.**
**Rückfragen an den Betreiber: keine.** **Sichtschutz 27.1:** Vergleichsausgaben nur unter `$TMPDIR/tb124_*`
(`TMPDIR=/var/folders/b_/yqcfpq996cxb1_v02m180f580000gn/T/`), davon nur `cmp` und sha256. Keine Kennzahl, keine
Trade- oder Zeilenzahl aus echten Kursdaten gelesen oder gedruckt. Die Probe-Trades in C2 stammen aus synthetischen
Reihen.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | 0a genau die sieben Einträge ⇒ `baf18a2`. ⚠️ **0b Befund:** Die zwei TB-123-Worktrees existieren auf dem Mac (je 458 MB, nicht `prunable`); `prune` entfernt nichts, **nicht gelöscht**. Sperrdatei (0 Byte) per `mv` entfernt (`rm` abgelehnt). 0c nachgeholt nach Nachtrag 1: rc 0 / rc 0, 50/50. 0d: `register()` `01f5997a…` = Soll, Sonde `dd4b4b95…` (= TB-122), alle betroffenen Dateien in **keinem** Abbildeintrag und **nicht** in `EINGEFROREN`. 0e db 12/12. 0f `d9449faf…`/223. 0g 52 Testdateien, **52/52 gleich** `c3_nachher.txt` von TB-123 |
| **A** | `sync_table.py` +47/0. `test_sync_check` **30/3 ⇒ 33/0 rc 0**, Test unverändert (sha256 `3e1567af…`). Regel **enger als der Auftragswortlaut** (siehe A), sonst wäre Abschnitt 3 rot geworden |
| ⭐⭐ **B** | Zwei `backtest_breakout.py`, je 16/1. Der Lookback reist in `df.attrs`; Scanbeginn = **`BB_PERIOD + L − 1`** (Nachtrag 1, am Code hergeleitet und je Stufe gemessen). Mit Voreinstellung 145 statt 127. `WARMUP_PERIOD` bleibt, `entry_cutoff`-Zeile unverändert. Vermerk kommt auf allen fünf Wegen an |
| ⭐⭐ **C1** | **13/13 `cmp` identisch** (Vorher zweimal hashgleich und gleich TB-122 A3) |
| ⭐⭐ **C2** | Teil D in den zwei `test_posten3_durchreichung.py`: **43/43** (Aktien), **42/42** (Krypto); Gegenprobe am Stand `105419e` (vor B) **rc 1 / rc 1** (14 bzw. 12 Prüfungen rot, nur in Teil D) |
| **C3** | 53 Testdateien nachher: **51 gleich**, `test_sync_check` 30/3 ⇒ **33/0**, `test_verankerter_datenstand` nur nachher 3/3; `test_vorregistrierung` 196/196; Porcelain 0/0. E1: Datenstand gleich, 11/12 DBs identisch, die zwölfte (`broker_testnet_…`) durch den Brücken-Cron 20:05 |
| **C4** | Trockenlauf ohne Modus 9/9 rc 0, **18/18 zeichengleich** (auch gleich TB-122 C4) |
| **C5** | Sondenausgabe **byte-gleich** (`cmp` rc 0), `register()` unverändert `01f5997a…`, kein Befund |
| **D** | `shared/test_verankerter_datenstand.py` **3/3 rc 0**; Gegenprobe 5/5 Fälle mit Soll-rc (F1–F4 rc 1); lädt kein Modul aus `research/vorregistrierung/` |

---

## 1. Schritt 0 — Sicherung und Ausgang

- **0a** (`git status --short`): genau die sieben erwarteten Einträge ⇒ Commit `baf18a2`, gepusht.
- **0b** (`0b_aufraeumen.txt`): `.git/index.lock.verwaist_claude_2026-09-30` hatte 0 Byte. `rm` wurde vom Werkzeug
  abgelehnt; die Datei ist per `mv` in den Sitzungs-Scratchpad verschoben (Bauart TB-91), `.git/index.lock*` ist leer.
  ⚠️ **Befund:** `git worktree prune -v` entfernt nichts. Die Ordner `$TMPDIR/tb123_vorher` und `…_vorher2` **existieren
  auf dem Mac** (je 458 MB, mit Verknüpfungen auf die echten DBs, `.env`, `trading-env`). Der steuernde Chat hatte sie
  aus der Brücken-VM als `prunable` gesehen; dort ist das `$TMPDIR` des Mac nicht sichtbar. `git worktree remove --force`
  hätte die Ordner gelöscht. Das nennt der Auftrag nicht, darum ist es nicht getan. Soll „nur noch der Hauptordner“
  ist **nicht erreicht**. Kein Abbruchkriterium.
- **0c:** entfiel beim Start (keine Antwort 30a im Repo). Nach Nachtrag 1 nachgeholt (`0c_dialog_index.txt`):
  `--handfelder docs/belege/TB-124/0c_handfelder.json` rc 0, `--pruefen` rc 0, 50/50 Zeilen, Zeile 30a eingetragen.
  Antwort 30a: 12 925 B, md5 `f9cdbbef…` (= Angabe im Nachtrag), sha256 `0ddc17f7…`. Commit `808aa47`.
- **0d** (`0d_ausgang.sh`, `0d_ausgang.txt`): HEAD `baf18a2`. `herkunft.register()` `01f5997a…`, `fehlend` leer.
  Sonde gegen `sperrliste_abbild_2026-09-26_tb117.json` (`46f0ad5d…`) rc 2, 84 Zeilen, sha256 `dd4b4b95…` wie in TB-122,
  Pfad-Bestandteile 37/0/0, `git status --porcelain` vor und nach der Sonde gleich. Die zwei `backtest_breakout.py`,
  die zwei `test_posten3_durchreichung.py`, `sync_table.py`, `test_sync_check.py`, die neue
  `shared/test_verankerter_datenstand.py` und `snapshot.py`: in **keinem** Abbildeintrag (auch nicht über den Dateinamen
  allein) und **nicht** in `EINGEFROREN` (22 Einträge, keiner deckt `shared/`, `strategies/` oder `research/sync_check/`
  ab). A und D sind damit pauschal frei.
- **0e:** `db_sicherung.sh` 12/12, rc 0 (`0e_db_sicherung.txt`).
- **0f:** Datenstand `d9449faf…` bei 223 Dateien = Soll; sha256 der zwölf `*.db` (`0f_datenstand.txt`, Skript
  `datenstand_db.sh`).
- **0g:** `c3_tests.sh` nach `$TMPDIR/tb124_c3_vorher`, 19:53–20:58 (`0g_basis.txt`). Gegen
  `docs/belege/TB-122/c3_nachher.txt`: **52/52 gleich** in rc und Schlusszeile (`0g_vergleich.txt`). Bekannt rot und
  unverändert: `test_drawdown_beide_masse` (rc 142, Zeitgrenze), `test_stabile_sortierung`, `test_wellenauswahl`,
  `test_drawdown`, `test_sync_check` (30/3). `test_kursdaten` 82/82 (Bezugspunkt `origin/main`). Kein bekannt roter
  Test grün geworden. Commit `f6aaf33`.

## 2. Schritt A — `test_sync_check` wieder 33/0

**A1 (gemessen):** In `compare_bot` greift Fall a) („`live_name in es_namen`“ ⇒ „im Backtest referenziert“) vor dem
Import-Fall. Seit `ab31314` importiert `volatility_breakout/equity_simulation.py` beide Namen selbst (Z. 59
`from live_params import BB_LOOKBACK, BB_SQUEEZE_PERCENTILE`) und setzt sie als Voreinstellung von
`collect_all_trades` ein (Z. 71/72). Beim Krypto-Zwilling ist es gleich (Z. 55, 69/70).

**A2, und warum die Regel enger ist als der Auftragswortlaut:** Wörtlich verlangt A2, jeden Namen, den
`equity_simulation.py` aus `live_params.py` importiert, als „identisch“ einzustufen. Das habe ich über alle neun Bots
gemessen: 35 Zeilen stehen auf „im Backtest referenziert“, und **alle 35** sind importiert (z. B. `STOP_LOSS_PCT`,
`MAX_CONCURRENT_POSITIONS`, `T3_FAST_LENGTH`). Nur **vier** davon wirken dort als Voreinstellung eines Parameters, nämlich
`BB_LOOKBACK` und `BB_SQUEEZE_PERCENTILE` bei beiden Breakout-Bots. Wörtlich umgesetzt hätte das zwei Folgen gehabt:
- Test Abschnitt 3 („`T3_FAST_LENGTH` wird als im Backtest referenziert gemeldet“) wäre rot geworden.
- Der Hinweis „wo der Wert als Default wirkt“ wäre für 31 Zeilen falsch gewesen.

Die umgesetzte Regel: **importiert und als Default eines Parameters eingesetzt ⇒ „identisch“.** Die Stellen findet eine
neue Hilfsfunktion `default_parameter(path, name)` per AST. Der Hinweis nennt beide Orte. Beispiel `BB_LOOKBACK`:
> aus live_params importiert (equity_simulation.py), wirkt als Default von collect_all_trades(squeeze_lookback_days=…);
> ebenso importiert in backtest_breakout.py, dort `SQUEEZE_LOOKBACK_DAYS`, Default von compute_indicators(squeeze_lookback_days=…)

Ein Name, der nur importiert und benutzt wird, bleibt „im Backtest referenziert“.

**A3:** Jeder neue Hinweis ist am Code belegt, Datei:Zeile in `a_sync_probe.txt`. Er bleibt nach B wahr: Die
Voreinstellung von `compute_indicators` hat sich nicht geändert. `run_backtest` liest den Lookback aus dem Frame und
nennt ihn nicht als Default, darum steht es auch nicht im Hinweis. Der generische Satz „wirkt als Default von
run_backtest()“ (jetzt `sync_table.py:313`) ist für `MAX_HOLD_DAYS` wahr (`run_backtest(max_hold_days=MAX_HOLD_DAYS)`).
Für andere Import-Fälle ist er nicht geprüft, das war nicht Gegenstand; er wird nur benannt.

**A4** (`a_sync_probe.py`/`.txt`): Die volle Tabelle aller neun Bots, 73 Zeilen, vorher gegen nachher ergibt einen Diff
von **genau den vier BB-Zeilen**. `test_sync_check.py` ist sha256-gleich, Ergebnis **33 bestanden, 0 fehlgeschlagen, rc 0**.
Commit `105419e`.

## 3. Schritt B — Scanbeginn an die Achse (nach Nachtrag 1)

### Nachtrag 1 (Fable 30a, R53)

Wortlaut des Nachtrags: `docs/auftraege/NACHTRAG_1_MAC_TB-124_scanbeginn_vorlauf.md` (committet in `808aa47`). Kern:
*„B1 im Auftrag setzt den Scanbeginn auf `max(BB_PERIOD, L, VOLUME_AVG_PERIOD) + 1`, also L + 1. Das liegt **vor** dem
Vorlauf der Zelle … B1 wird deshalb ersetzt.“* — *„Scanbeginn: Er ist der erste Index, an dem die Einstiegsbedingung der
Zelle definiert ist.“* Fable 30a, R53: *„Der Scanbeginn einer Zelle liegt nie vor ihrem Vorlauf (TB-122 F1, Handwerk).“*
Zeitpunkt: Der Nachtrag kam, als B noch nicht committet war. Den Kandidaten nach dem ursprünglichen B1
(`max(…) + 1`) hatte ich im Scratchpad gebaut und geprüft (13/13 hashgleich); ins Repo kam **nur** die Fassung nach
Nachtrag 1.

**Herleitung, am Code gemessen** (`b1_herleitung.py`/`.txt`; 0-basiert, `rolling` ohne `min_periods` in beiden
`indicators.py`):
- `bb_width` ist ab Index `BB_PERIOD − 1` = 19 definiert.
- `squeeze_thresh` (Fenster L über `bb_width`) ist ab `19 + L − 1` definiert.
- Der Einstieg bei i braucht `is_squeeze[i − 1]` und `close[i] > bb_upper[i]`.
- Also gilt i ≥ **`BB_PERIOD + L − 1`**.
- `vol_avg` ist ab 19 definiert und nicht Teil der Einstiegsbedingung. Mit `use_volume_filter` wird ein NaN in der
  Schleife übersprungen.

Die Herleitung stimmt mit dem Nachtrag überein; es gibt keine Abweichung.

| Bot | Stufe L | hergeleiteter Scanbeginn (= gemessener erster Einstiegsindex) | wörtlich addiert L + BB_PERIOD | bisher `WARMUP_PERIOD + 1` |
|---|---|---|---|---|
| `volatility_breakout` | 20 | **39** | 40 | 127 |
| | 97 | **116** | 117 | 127 |
| | 175 | **194** | 195 | 127 |
| | 252 | **271** | 272 | 127 |
| | 126 (Voreinstellung) | **145** | 146 | 127 |
| `volatility_breakout_crypto` | 20 | **39** | 40 | 127 |
| | 135 | **154** | 155 | 127 |
| | 250 | **269** | 270 | 127 |
| | 365 | **384** | 385 | 127 |
| | 126 (Voreinstellung) | **145** | 146 | 127 |

Heute abgeschnitten waren damit die Balken **39–126** bei Stufe 20 und **116–126** bei Stufe 97. Das deckt sich mit
„Erschlossen“ im Auftrag und berichtigt TB-122 F1 („21…126“). Bei allen Stufen über 126 lag der alte Scanbeginn
**vor** dem Vorlauf, war aber folgenlos: Bis dahin ist `squeeze_thresh` NaN und `bb_width <= NaN` falsch.

**B2 (Bauart wie vorgegeben):** `compute_indicators` setzt `df.attrs["squeeze_lookback_days"] = squeeze_lookback_days`.
`run_backtest` liest `df.attrs.get("squeeze_lookback_days", SQUEEZE_LOOKBACK_DAYS)`, also ohne Vermerk die
Voreinstellung (⇒ 145), und rechnet `start_i = BB_PERIOD + squeeze_lookback_days - 1`. Die Herleitung steht als
Kommentar im Code. **Vorher gemessen** (`b2_vermerk_probe.py`/`b2_vermerk.txt`, per `sys.setprofile`, ohne
Monkeypatch), unter pandas 2.3.3: Am Kandidaten und nach B kommt der Vermerk auf allen Wegen an, am Stand vor B auf
keinem:
- W1 `collect_all_trades` mit 20/97 und ohne Argument;
- W2 `get_trades_for_symbol` direkt;
- W3 `evaluate_combination_multi`;
- W4 `load_all_symbol_data` ⇒ `get_trades_for_symbol` mit echten Kursen (zwei Symbole, nur Vermerk gedruckt);
- W5 `__main__` beider Dateien;
- W6: Ein Aufruf mit 20 lässt den Vermerk 126 des vorberechneten Frames unverändert (`attrs` wird beim Kopieren
  getrennt).

**Weitere Aufrufer** (gemessen): Alle anderen Leser gehen über `get_trades_for_symbol`, das `compute_indicators`
unmittelbar vor `run_backtest` aufruft. Direkt rufen `run_backtest` nur die zwei `__main__` und die Belegskripte
TB-90 `b6_backtest_lauf.py` und TB-122 `a_lauf.py` auf, jeweils mit `compute_indicators` davor.
**B3 — Leser von `WARMUP_PERIOD`** (`b3_leser.txt`):
- Import in beiden `multi_symbol_optimise.py`;
- `research/trailing_stops/run_one_bot.py:203`, `research/vbc_deepdive/run_deepdive.py:121`;
- `strategies/volatility_breakout/experiment_trailing_stop.py:73–74`, eine eigene Scan-Schleife mit
  `WARMUP_PERIOD + 1`: **nicht Signalpfad, nicht geändert**, sie beginnt weiter bei 127;
- Text in `faltenplan_neun.py`;
- die zwei `turtle_soup`-Backtests (eigene Konstante).

`WARMUP_PERIOD` bleibt mit dem Wert 126.
**B4:** Keine weitere Änderung. numstat je Datei 16/1 (`b_diff.txt`, Einbauskript `b_einbau.py`). Commit `f90135e`.

## 4. Schritt C — Nachweis

**C1** (`c1_vorher_hashes.txt`, `c1_vergleich.txt`): `docs/belege/TB-122/a_lauf.py` vor B (`baf18a2`, zweimal
hashgleich, dazu gleich TB-122 A3) und nach B (`f90135e`) ⇒ **13/13 IDENTISCH**. Das sind B6 3/3 sowie `trades`,
`trades_regimefilter`, `equity_curve` und `optimierer`. Scanbeginn 145 statt 127 ändert mit Voreinstellungen kein Byte.

**C2** (`c2_wertprobe.txt`, Einsetzskript `c2_tests_einbau.py`, Probe `c2_probe.sh`): Teil D in den zwei
`test_posten3_durchreichung.py`. Die Stufen kommen aus `registerdaten.raster()` und stehen nicht als Zahl im Test. Der
Docstring-Satz „Nicht Gegenstand: `WARMUP_PERIOD` …“ ist durch die Beschreibung von Teil D ersetzt. Teil A–C sind
unverändert (numstat 91/4 bzw. 90/4, die 4 sind der Docstring).
- **D0/D0b:** Es gibt Stufen, bei denen der alte Scanbeginn abschnitt (Aktien 20, 97; Krypto 20, genau die im Auftrag
  genannten). `WARMUP_PERIOD` ist unverändert die Voreinstellung.
- **(i) knapp am Vorlauf, jede Stufe und die Voreinstellung:**
  - **D1:** Ein Frame mit Dauersignal und Vermerk L zeigt den ersten Einstieg genau bei `BB_PERIOD + L − 1`.
  - **D1b:** `compute_indicators` mit L lässt den Squeeze-Status des Vortags am Index davor NaN und ab dem Scanbeginn
    definiert.
  - **D2:** Ohne Vermerk ist der Scanbeginn 145.
- **(ii) Einstiegsfall, jede Stufe:** Eine synthetische Reihe hat eine Schwingung der Periode 4 mit fallender
  Amplitude (die Bandbreite fällt stetig) und den Ausbruch genau am ersten zulässigen Index.
  - **D3:** Der Signalpfad (`collect_all_trades`) findet den Einstieg dort.
  - **D3b:** Ohne Stufe findet er ihn nicht; geprüft nur für Stufen unter der Voreinstellung.
  - **D3c:** Liegt der Ausbruch einen Balken früher, gibt es dort keinen Einstieg.
  - **D4:** Der Optimierer-Pfad (`get_trades_for_symbol`) findet den Einstieg.
  - **D5:** Der Vermerk kommt per Spion in `run_backtest` an.
- **Nachher:** 43/43 (Aktien), 42/42 (Krypto), im Hauptordner und ausgepackt (`git archive f90135e`).
- **(iii) Gegenprobe (40.7):** Dieselben Testdateien am Stand `105419e` (nach A, vor B) ⇒ **rc 1 / rc 1**.
  - Aktien 29 bestanden, 14 rot: D1 ×5 (ist 127), D2, D3/D4 bei 20 und 97, D5 ×4.
  - Krypto 30 bestanden, 12 rot.
  - Teil A–C bleiben dort grün.

`c2_probe.sh` ist gegenüber TB-122 angepasst: Es packt `docs/VORREGISTRIERUNG_neuselektion.md` mit aus und fährt nur
die zwei Breakout-Bots.

**C3-posten3** (`c3_posten3.txt`):

| Stand | `rsi2_mean_reversion` | `volatility_breakout` | `volatility_breakout_crypto` |
|---|---|---|---|
| vor B | 16/16 | 12/12 | 12/12 |
| nach B | 16/16 | 43/43 | 42/42 |

Alle rc 0.

**C3:** siehe den Abschnitt „C3 — Tests nachher“ unten.

**C4** (`c4_trockenlauf.txt`): TB-103-Trockenlauf ohne Modus. Vorher (`f6aaf33`, zweimal hashgleich) und nachher: 9/9
rc 0, **18/18 zeichengleich**, dazu gleich TB-122 C4 nachher.

**C5** (`c5_nachher.txt`): Die Sonde liefert nach B **Byte für Byte** dieselbe Ausgabe wie 0d (`cmp` rc 0, `dd4b4b95…`).
`register()` bleibt `01f5997a…`. Kein Befund, auch nicht der nach C5 zulässige, weil die zwei `backtest_breakout.py` in
keinem Abbildeintrag stehen (0d). Wie in TB-122 heisst das: Der Hash-Übergang steht **nur** im Commit und im Entwurf
unten (TB-122 F4).

**C6** (`c6_hashes.txt`): siehe Tabelle in Abschnitt 6.

## C3 — Tests nachher

`c3_tests.sh` am HEAD `7453469` (nach D, Arbeitsbaum ausserhalb `docs/` leer), 21:05–22:11, Log unter
`$TMPDIR/tb124_c3_nachher` ⇒ `c3_nachher.txt`. Vergleich gegen `0g_basis.txt` (`c3_vergleich.txt`):
- vorher 52, nachher 53 Testdateien;
- **51 gleich** in rc und Schlusszeile, darunter `test_vorregistrierung` 196/196 (1123 s), `test_snapshot` 164/164 und
  die bekannt roten unverändert;
- `test_sync_check` **30/3 rc 1 ⇒ 33/0 rc 0** (A);
- `test_verankerter_datenstand` **nur nachher**, 3/3 rc 0 (D).

Das ist genau die Erwartung des Auftrags. `git status --porcelain -- . ':!docs'` vor und nach dem Lauf **0/0**.
**Abweichung in der Commit-Folge:** Ich habe D **vor** dem C3-Lauf committet (`7453469`), damit C3 an einem sauberen
Arbeitsbaum läuft statt mit einer unversionierten Datei in `shared/`. Die C3-Belege stehen deshalb in einem eigenen
Commit (`65fcaf0`) und nicht im D-Commit.

**E1** (`e_datenstand_nachher.txt`, `e_db_identitaet.txt`):
- Datenstand nachher `d9449faf…`/223 = vorher.
- **11 von 12 DBs** sind sha256-identisch.
- `broker_testnet_t3_supertrend.db` hat sich geändert, und zwar durch den **Cron-Lauf der Binance-Brücke um 20:05:00**
  (mtime 20:05:00; `logs/broker/testnet_spiegel.log` hat Einträge 20:05:00,9; Cron-Zeile `broker/README.md:237`).
  Nicht durch die Sitzung, die `broker/` nie aufgerufen hat. Die elf Paper-Trading-DBs sind unverändert.

## 5. Schritt D — R28: Probe `VERANKERTER_DATENSTAND` gegen Register 18

**D1:** Die Probe ist eine **eigene Datei** `shared/test_verankerter_datenstand.py` und kein Abschnitt in
`test_snapshot.py`. Gründe:
- `c3_tests.sh` nimmt `shared/test_*.py` mit, die Probe erscheint also wie erwartet „nur nachher“.
- `test_snapshot.py` bleibt in C3 unverändert und damit vergleichbar.
- Die Probe braucht nichts von dessen Aufbau (Mutationsprobe am Snapshot).

Muster J-r:
- **R28-1:** Es gibt genau eine Zeile, die mit ``| Datenstand (`datenstand_hash`) |`` beginnt (Register Z. 2852,
  Abschnitt 18).
- **R28-2:** Sie trägt genau einen 64-stelligen Hexwert.
- **R28-3:** Dieser ist gleich `snapshot.VERANKERTER_DATENSTAND`.

Ergebnis **3/3, rc 0** (`d_probe.txt`).
**D2:** Die Probe importiert `os`, `re`, `sys` und `snapshot` (aus `shared/`, Pfad aus dem eigenen Ort). Den
Registerpfad baut sie aus der Repo-Wurzel. Gemessen: `import snapshot` lädt aus dem Repo nur `snapshot` selbst. Nach
`main()` ist kein Modul aus `research/vorregistrierung/` geladen (in allen fünf Gegenprobe-Fällen).
**D3** (`d_gegenprobe.py`, je Fall ein Prozess):

| Fall | rc |
|---|---|
| F0 unverändert | 0 |
| F1 Konstante im Speicher auf 64 × „0“ | 1 |
| F2 Registerkopie mit zwei Datenstandszeilen | 1 |
| F3 Registerkopie mit abweichendem Hexwert | 1 |
| F4 Registerkopie ohne Datenstandszeile | 1 |

Das ist 5/5 wie gefordert. Die Kopien liegen unter `$TMPDIR/tb124_d_gegenprobe`.
**D4, nur benannt:** Das dritte Literal `research/registernachtrag_tb48/pruefe_abschnitt17.py:97`
`SOLL_DATENSTAND = "d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84"` ist gleich dem Registerwert. Es
wird dort gegen den **gemessenen** Datenstand verglichen (Z. 213), nicht gegen den Registertext. Nicht geändert.
Commit `7453469`.

**Satz zu R28 für E-2:** Der Datenstand `d9449faf…` steht in Register 18 (Z. 2852) als Quelle und in drei Codekopien.
- Zwei davon haben jetzt je eine Probe gegen den Registertext:
  - `research/vorregistrierung/auswertung.py:129` `REGISTRIERTER_DATENSTAND` ⇒ J-r in
    `research/vorregistrierung/test_ersatzwerte.py:1143–1151` (TB-117);
  - `shared/snapshot.py:260` `VERANKERTER_DATENSTAND` ⇒ `shared/test_verankerter_datenstand.py` R28-1…3 (TB-124,
    `7453469`), ohne Import aus dem Laufbereich.
- Die dritte Kopie, `research/registernachtrag_tb48/pruefe_abschnitt17.py:97` `SOLL_DATENSTAND`, hat keine Probe gegen
  das Register.
- Ebenfalls ohne Probe: `snapshot.VERANKERTE_KURSDATEIEN = 223` gegen „bei **223** Kursdateien“ derselben Zeile. Das war
  nicht Gegenstand von D1 und wird nur benannt.

## 6. Entwurf der Tatsachennotiz für den Registerauftrag E-2

> ⚠️ **ENTWURF — nicht im Register.** Wortlaut zur Übernahme durch E-2; Register und Regelwerk waren in TB-124 nicht
> freigegeben.
>
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

## 7. Befund für E-2 (nur benannt): R53-Zählweise

R53 beschreibt den Vorlauf als „die oberste registrierte Stufe … zuzüglich der festen Fenster des Bots (etwa
Bollinger-Fenster …)“. Wörtlich addiert wären das **L + 20** Balken. Aus dem Code hergeleitet ist der erste zulässige
Index **L + 19** (0-basiert): Die zwei hintereinanderliegenden rollenden Fenster (Bollinger 20 über `close`, Squeeze L
über `bb_width`) teilen sich einen Balken. Das ergibt **19 + L Balken Vorlauf** vor dem ersten möglichen Einstieg.
Oberste Stufe: Aktien L = 252 ⇒ hergeleitet 271, wörtlich 272; Krypto L = 365 ⇒ hergeleitet 384, wörtlich 385.
Einordnung durch den steuernden Chat in E-2 (BACKLOG „R53, Zählweise“).

## 8. Für Fable

Keine neue Verfahrensfrage. Die Zählweise in Abschnitt 7 ist nach Nachtrag 1 ein Befund für E-2 und keine Frage.

## 9. Nicht getan

- **`research/faltenplan_neun/faltenplan_neun.py`**: Text und `vorlauf_balken` 127 der zwei Breakout-Bots
  (Z. 195–223) sind nach B wörtlich weiter überholt. Das zitierte `start_i = WARMUP_PERIOD + 1` gibt es nicht mehr, der
  Vorlauf je Stufe ist jetzt `BB_PERIOD + L − 1`. Nicht geändert (Frage 1 aus 30a, BACKLOG R53 (a)).
- **Drittes Literal** `pruefe_abschnitt17.py:97`: nur benannt (D4).
- **Generischer Hinweis** `sync_table.py:313` „wirkt als Default von run_backtest()“: für andere Import-Fälle nicht
  geprüft, nur benannt.
- **`experiment_trailing_stop.py`**: eigene Scan-Schleife mit `WARMUP_PERIOD + 1`, kein Signalpfad, nicht geändert
  (ausserhalb der Freigabe).
- **Worktrees `tb123_vorher*`**: nicht entfernt (0b).
- **`VERANKERTE_KURSDATEIEN`**: ohne Registerprobe, nur benannt.
- Register, Regelwerk, Abbild: nicht angefasst.

## 10. Dateien des steuernden Chats, mitgenommen

In `808aa47`:
- `docs/auftraege/NACHTRAG_1_MAC_TB-124_scanbeginn_vorlauf.md`;
- `docs/projektfuehrung/FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md`;
- `docs/belege/TB-124/0c_handfelder.json`;
- der Nachtrag am Ende von `docs/projektfuehrung/UEBERGABE.md` (15/0).

In `f6aaf33`: der Nachtrag an `docs/projektfuehrung/VORMESSUNG_E-2_2026-09-29.md` (9/0, R53/R54-Messbitten), der
während des Laufs dazukam.

Im Abgabe-Commit (ebenfalls während des Laufs abgelegt):
- ein weiterer angehängter Nachtrag an `docs/projektfuehrung/UEBERGABE.md` (25/0);
- der neue Auftrag `docs/auftraege/MAC_TB-125_regelwerk_nachtrag_29_30_09.md` (33 673 B), nicht gelesen ausser
  dem Kopf, nicht bearbeitet.

Der BACKLOG-Block „Aus Fable 30a“ ist wortgleich aus dem Codeblock des Nachtrags übernommen, vor
„## 6 — Geparkt …“, numstat **8/0** (`n1_backlog_numstat.txt`).

## 11. In einfacher Sprache

- **Scanbeginn:** Die zwei Breakout-Bots suchen jetzt ab dem ersten Tag nach Einstiegen, an dem ihre Einstellung das
  überhaupt erlaubt. Das ist nicht mehr fest Tag 127, und es ist auch nicht früher, als die Indikatoren fertig sind.
  Mit den heutigen Einstellungen ändert sich dadurch kein einziges Byte (13 Ausgaben verglichen). Mit den kurzen
  Einstellungen des Registers (20, 97) findet der Backtest jetzt Einstiege, die vorher abgeschnitten waren. Die Tests
  zeigen das an einer künstlichen Kursreihe und schlagen am alten Stand an.
- **Prüfwerkzeug:** Das Werkzeug, das Einstellungen zwischen Live und Backtest vergleicht, sortiert zwei Einstellungen
  wieder richtig ein. Sein Test ist wieder ganz grün, ohne dass am Test etwas geändert wurde.
- **Neue Wache:** Sie schlägt an, wenn der im Snapshot-Werkzeug verankerte Datenstand vom Register abweicht.
- **Offen:** Zwei alte Arbeitskopien von gestern liegen noch im Zwischenspeicher des Mac. Ich habe sie nicht gelöscht,
  weil der Auftrag davon ausging, dass sie schon weg sind.
