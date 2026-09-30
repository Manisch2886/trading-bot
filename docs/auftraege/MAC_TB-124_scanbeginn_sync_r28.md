# TB-124 F1: Scanbeginn der Volatility-Breakout-Bots an `bb_lookback` binden · `test_sync_check` wieder 33/0 · R28-Probe `snapshot.py` gegen Register 18 · Stand 30.09. sichern

**Sitzungstitel:** `TB-124` · **Modell:** Opus, Aufwand hoch (ARBEITSWEISE 22.1) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 30.09.2026, ca. 19:45, vom steuernden Chat
**Vorgänger:** TB-123 (`0034960`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-124_scanbeginn_sync_r28.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** immer `trading-env/bin/python3` (7c). **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15). Richtungsweisend wäre hier nur eine Freigabefrage; ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Prüfwerkzeuge:** Jedes Skript, das diese Sitzung für einen Nachweis schreibt (0d, A4, C1, C2, C3, D3), liegt unter `docs/belege/TB-124/` und wird mitcommittet.
**Grundlagen (in Schritt 0 lesen, nur die genannten Stellen):**
- `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md`: Kopf-Befund, Abschnitt 4 (C1–C5), Abschnitt 5 (F1), Abschnitt 6 (Form der Tatsachennotiz);
- `docs/auftraege/MAC_TB-122_posten3_achsen_durchreichen.md`: Schritte A und C (Bauart), Sichtschutz;
- `docs/belege/TB-122/`: `0b_ausgang.sh`, `a_lauf.py`, `c2_probe.sh`, `c3_tests.sh`, `c4_trockenlauf.sh`;
- `docs/belege/TB-123/a3_sync_probe.py` und `a3_sync_probe.txt`;
- `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md`, Z. 105 und Z. 191 (R28);
- `docs/projektfuehrung/VORMESSUNG_E-2_2026-09-29.md`, Zeile R28 (Z. 16) und Z. 32;
- `research/vorregistrierung/test_ersatzwerte.py`, Z. 1143–1151 (J-r, Vorbild für D).

## ⭐⭐ Freigabe des Betreibers, wörtlich

**30.09.2026, 19:13, im steuernden Chat.** Der Betreiber antwortete auf die Vorschläge des steuernden Chats: *„Wir setzten es wie von dir Vorgeschlagen um“*. Der Sachentscheid dazu steht in `docs/projektfuehrung/UEBERGABE.md`, Nachtrag 30.09.2026, 19:13, Abschnitt „Sachentscheide“:

> *„TB-122 **F1** (Scanbeginn der Breakout-Bots an `WARMUP_PERIOD`) geht in **TB-124**: Nachweis wie in TB-122, Hash-Übergang als Tatsachennotiz.“*

Der Umfang steht im Umzugsblock 30.09., Block 6: *„**Neu frei (30.09.):** F1 in TB-124 (zwei Signalpfad-Dateien `backtest_breakout.py`).“* Der volle Vorschlagstext liegt nur im alten Chat, nicht im Repo.

**Tests (27c R31 (b)) — Nachtrag zur Freigabe, 30.09.2026, ca. 19:44, Auswahlkarte im steuernden Chat.** Frage: *„F1 in TB-124: Die Freigabe vom 30.09. nennt nur die zwei backtest_breakout.py. Nach 27c R31 (b) muss sie die Tests mitnennen. Darf die Sitzung die zwei bestehenden test_posten3_durchreichung.py der Breakout-Bots um die Scanbeginn-Probe erweitern?“* Gewählte Option:

> *„Ja, zwei Testdateien (Empfohlen)“* — „Dauerhafte Wache, dass der Scanbeginn der Stufe folgt. Preis: zwei weitere Dateien unter strategies/ ändern sich (nur Tests).“

Damit dürfen `strategies/volatility_breakout/test_posten3_durchreichung.py` und `strategies/volatility_breakout_crypto/test_posten3_durchreichung.py` **erweitert** werden. Die bestehenden Prüfungen bleiben unverändert, angelegt wird keine neue Datei. Der Docstring-Satz „Nicht Gegenstand: `backtest_breakout.WARMUP_PERIOD` (Scanbeginn) …“ wird nach B wahrheitsgemäss nachgezogen.

**Pauschal frei (Handwerk ohne Sperrlistennähe, Betreiberentscheid 26.09.2026):** Schritt A (`research/sync_check/sync_table.py`) und Schritt D (neue Probe in `shared/`). Das gilt nur, wenn 0d misst, dass diese Dateien in keinem Abbildeintrag und nicht in `herkunft.py::EINGEFROREN` stehen. Sonst: nicht ändern, Befund melden.

⛔ **Nicht freigegeben, mit Grund:**
- `multi_symbol_optimise.py`, `equity_simulation.py`, `live_params.py`, `forward_test.py` und jede andere Datei unter `strategies/` ausser den zwei `backtest_breakout.py` und den zwei `test_posten3_durchreichung.py` der Breakout-Bots. *Grund:* Sperrlistenpunkt 11. Die Freigabe nennt zwei Dateien.
- `research/faltenplan_neun/faltenplan_neun.py`. *Grund:* Der Vorlauf ist Frage 1 der Fable-Anfrage 30a (TB-122 F2). Sein Text wird durch B wörtlich weiter überholt; das wird nur benannt.
- `research/registernachtrag_tb48/pruefe_abschnitt17.py` (drittes Literal `SOLL_DATENSTAND`, Z. 97). *Grund:* Das gehört zur Tatsachennotiz R28 in E-2, hier wird es nur benannt.
- Register und Regelwerk; ein neues Sperrlisten-Abbild. *Grund:* Das ist E-2, nicht freigegeben. Die Tatsachennotiz entsteht nur als Entwurf im Ergebnis.
- `herkunft.py`, `paths.py`, `zuteilung.py`, `auswertung.py`, `kennzahlen.py`. *Grund:* Nach UEBERGABE Block 6 ist jede Öffnung einzeln freizugeben. Zur Einordnung: `auswertung.py` und `kennzahlen.py` stehen in `EINGEFROREN`, `zuteilung.py` in `SPERRLISTE_DATEIEN`.
- Läufe im Modus oder auf dem Snapshot; Schreiben unter `research/**/ergebnisse/` oder `research/**/daten/`; `crontab`; Datenbanken schreiben. *Grund:* Sichtschutz 27 und die OOS-Evidenz (7c).

**Sichtschutz 27.1:** wie TB-122. Die Vergleichsläufe erzeugen Backtest-Ausgaben. Die Sitzung **liest keine Kennzahl, keine Trade- und keine Zeilenzahl daraus**, sie vergleicht nur Bytes (`cmp`, sha256). Die Ausgaben liegen **ausserhalb des Repos** unter `$TMPDIR/tb124_*`; ins Repo kommen nur Hashes. Aus Testausgaben werden nur rc, Dauer und die Schlusszeile genommen.

In einfacher Sprache: TB-122 hat die Einstellung `bb_lookback` bis zur Indikatorberechnung der beiden Breakout-Bots durchgereicht. Der Backtest fängt aber weiterhin erst bei Tag 127 an zu suchen, auch wenn bei den Einstellungen 20 oder 97 schon früher ein Einstieg möglich wäre. Diese Sitzung bindet den Suchbeginn an die Einstellung. Mit den heutigen Werten muss danach jede Ausgabe Byte für Byte gleich bleiben. Nebenbei repariert sie eine Test-Einstufung, die seit TB-122 rot ist, und legt eine fehlende Probe für den verankerten Datenstand an.

## Belegt · erschlossen · offen

**Belegt** (gemessen vom steuernden Chat am 30.09.2026 zwischen 19:24 und 19:40, über die Geräteanbindung, nur lesend):
- HEAD `0034960`. `git worktree list`: `tb123_vorher` und `tb123_vorher2` stehen beide als **`prunable`** (ihre Ordner unter `$TMPDIR` fehlen); die Einträge `.git/worktrees/tb123_vorher{,2}` sind noch da.
- `strategies/volatility_breakout/backtest_breakout.py`: Z. 97 `from live_params import (BB_LOOKBACK as SQUEEZE_LOOKBACK_DAYS, …`; Z. 101 `BB_PERIOD = 20`; Z. 103 `VOLUME_AVG_PERIOD = 20`; Z. 114 `WARMUP_PERIOD = max(BB_PERIOD, SQUEEZE_LOOKBACK_DAYS, VOLUME_AVG_PERIOD)`; Z. 117 `def compute_indicators(price_df, squeeze_lookback_days=SQUEEZE_LOOKBACK_DAYS, squeeze_percentile=…)`; Z. 138 `def run_backtest(price_df, stop_loss_pct=5.0, entry_cutoff=None, max_hold_days=…, use_volume_filter=False, volume_filter_multiplier=…)`, **ohne** Lookback-Parameter; Z. 155 `start_i = WARMUP_PERIOD + 1`.
- `strategies/volatility_breakout_crypto/backtest_breakout.py`: Z. 65 derselbe Import; Z. 69/71 `BB_PERIOD = 20`, `VOLUME_AVG_PERIOD = 20`; Z. 81 `WARMUP_PERIOD = …`; Z. 84 `compute_indicators(…)`; Z. 101 `run_backtest(…)` ohne Lookback-Parameter; Z. 114 `start_i = WARMUP_PERIOD + 1`.
- Aufrufer von `run_backtest` im Signalpfad: `volatility_breakout/multi_symbol_optimise.py:109` und `volatility_breakout_crypto/multi_symbol_optimise.py:92`, je in `get_trades_for_symbol` direkt nach `df_ind = compute_indicators(…, squeeze_lookback_days, squeeze_percentile)`. Keiner übergibt den Lookback an `run_backtest`.
- Leser von `WARMUP_PERIOD` ausserhalb der zwei Dateien: Import in beiden `multi_symbol_optimise.py` (Z. 37 bzw. 30; per `grep` keine weitere Verwendung dort), `research/trailing_stops/run_one_bot.py:203`, `research/vbc_deepdive/run_deepdive.py:121`, `strategies/volatility_breakout/experiment_trailing_stop.py:73–74`, dazu Text in `research/faltenplan_neun/faltenplan_neun.py:195–223`, im Docstring der zwei `test_posten3_durchreichung.py` der Breakout-Bots sowie in den beiden `turtle_soup`-Backtests (dort eine eigene Konstante).
- Register `docs/VORREGISTRIERUNG_neuselektion.md`: **Z. 265** `volatility_breakout_crypto` · `bb_lookback` · `20, 135, 250, 365`; **Z. 280** `volatility_breakout` · `bb_lookback` · `20, 97, 175, 252`. *(Berichtigung: UEBERGABE, Umzugsblock 30.09., Block 4 Nr. 1 nennt „REG:255“ für Krypto. Das ist falsch, Z. 255 ist `t3_supertrend`.)*
- `docs/belege/TB-123/a3_sync_probe.txt`: bei `volatility_breakout` stehen `BB_LOOKBACK` und `BB_SQUEEZE_PERCENTILE` am Stand `dca3096` (ausserhalb `docs/` gleich `0034960`) auf „im Backtest referenziert“ (Hinweis `None`), am Stand `c064405` auf „identisch … wirkt als Default von run_backtest()“ mit Hinweis auf `SQUEEZE_LOOKBACK_DAYS` bzw. `SQUEEZE_PERCENTILE`.
- `research/sync_check/test_sync_check.py` Z. 131–141, Abschnitt 4 hat vier Prüfungen:
  - je für `MAX_HOLD_DAYS`, `BB_LOOKBACK` und `BB_SQUEEZE_PERCENTILE` bei `volatility_breakout`: `status == "identisch"` und `"Default" in hinweis`;
  - `"SQUEEZE_LOOKBACK_DAYS"` im Hinweis zu `BB_LOOKBACK`.
  Rot sind seit `ab31314` die drei Prüfungen zu den zwei BB-Grössen.
- Ursache in `research/sync_check/sync_table.py`: Z. 247–251 (Fall a), „equity_simulation.py referenziert den Namen“) greift vor dem Import-Fall Z. 253–266. Er vergibt „im Backtest referenziert“ ohne Hinweis, weil `volatility_breakout/equity_simulation.py` die zwei Namen seit `ab31314` selbst aus `live_params.py` importiert und dort als Voreinstellung verwendet (z. B. `collect_all_trades`, Z. 71 laut Gegenleser, von der Sitzung nachzumessen).
- Der Hinweistext Z. 266 „wirkt als Default von run_backtest()“ ist generisch für jeden Import-Fall. Für `BB_LOOKBACK` stimmt er schon heute nicht wörtlich: Der Wert ist Default von `compute_indicators`.
- `c3_tests.sh` nimmt `$(ls shared/test_*.py)` mit (Z. 14), aber keine `strategies/*/test_*.py`. `a3_vergleich.py` (Z. 7) bereinigt Log-Ordner nur nach dem Muster `tb12\d_c3_(vorher|nachher)`.
- `docs/werkzeuge/dialog_index.py`: je `FABLE_ANTWORT_*` eine Zeile. Eine Anfrage allein ergibt keine Zeile. `--handfelder` verlangt einen JSON-Pfad.
- `shared/snapshot.py:260–261` `VERANKERTER_DATENSTAND = ("d9449faf…")`. Eine Probe gegen Register 18 gibt es laut Vormessung R28 nicht (`shared/test_snapshot.py:1324ff` prüft nur die Erzwingung des Ankers).
- Journal: letzter Block **DU** ⇒ dieser Auftrag schreibt **DV** (vor dem Schreiben nachmessen, ARBEITSWEISE 14, Journalregel).

**Erschlossen, nicht gemessen:**
- Mit Stufe 20 wäre `max(BB_PERIOD, 20, VOLUME_AVG_PERIOD) + 1 = 21`, mit Stufe 97 wäre es 98, mit der Voreinstellung 126 bleibt es 127.
- **Frühester möglicher Einstieg (Gegenleser, von der Sitzung nachzumessen):**
  - `bb_width` ist ab Balken 19 gültig; `squeeze_thresh` rollt mit Fenster L und ist damit ab Balken L + 18 gültig; der Einstieg braucht den Squeeze-Status von t − 1, also frühestens Balken L + 19.
  - Heute abgeschnitten sind damit die Balken **39–126** bei Stufe 20 und **116–126** bei Stufe 97.
  - Bei der Voreinstellung 126 liegt der früheste Einstieg bei 145. Der Scanbeginn 127 war dort nie bindend, das stützt die Erwartung „bytegleich“.
  - Das berichtigt TB-122 F1 („Balken 21…126“).
- Ein Umbau allein in den zwei Dateien scheint möglich, weil `compute_indicators` und `run_backtest` beide dort stehen und der Signalpfad das Ergebnis des einen direkt an das andere gibt.

**Offen (misst die Sitzung):** ob `backtest_breakout.py`, `sync_table.py` oder `shared/` in einem Abbildeintrag oder in `EINGEFROREN` stehen; die pandas-Fassung in `trading-env`; welche weiteren Aufrufer `run_backtest` Frames ohne Umweg über `compute_indicators` übergeben.

## Schritt 0 — Sicherung und Ausgang

0a. `git status --short` — genau diese Einträge (Reihenfolge ohne Bedeutung). Der steuernde Chat trägt die Liste beim Ablegen ein:
- ` M docs/auftraege/AKTUELLER_AUFTRAG.md`
- ` M docs/projektfuehrung/FABLE_DIALOG_INDEX.md`
- ` M docs/projektfuehrung/UEBERGABE.md`
- `?? docs/auftraege/MAC_TB-124_scanbeginn_sync_r28.md`
- `?? docs/projektfuehrung/FABLE_ANFRAGE_2026-09-30a_vorgepruefte_fragen_e2.md`
- `?? docs/projektfuehrung/UEBERGABE_ARCHIV.md`
- `?? docs/projektfuehrung/VORMESSUNG_E-2_2026-09-29.md`

*Gemessen vom steuernden Chat am 30.09.2026, ca. 19:55 (`git --no-optional-locks diff --name-only HEAD` und `ls-files --others --exclude-standard`). Zu `UEBERGABE.md`: Die Datei wurde am 30.09. geteilt (T5, Betreiberentscheid 19:44). `numstat` zeigt deshalb viele entfernte Zeilen. Das ist beabsichtigt: Die Zeilen stehen byte-gleich in `UEBERGABE_ARCHIV.md`, der Beleg steht im Nachtrag am Ende von `UEBERGABE.md`. Kein Abbruch deswegen.*

Weicht etwas ab ⇒ Abbruch.

0b. Aufräumen, was von TB-123 und vom steuernden Chat liegt:
- `.git/index.lock.verwaist_claude_2026-09-30` (0 Byte): Der steuernde Chat hat sie am 30.09. um 19:24 durch ein verbotenes `git status` über die Brücke erzeugt und umbenannt, weil die Brücke nicht löschen darf. Prüfen, dass sie 0 Byte hat, dann löschen.
- `git worktree prune -v`, danach `git worktree list` ⇒ nur noch der Hauptordner. Beleg: `docs/belege/TB-124/0b_aufraeumen.txt`.

0c. **Nur wenn `docs/projektfuehrung/FABLE_ANTWORT_2026-09-30a_*.md` in 0a steht:**
- `trading-env/bin/python3 docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-124/0c_handfelder.json`, danach `--pruefen`.
- Die JSON-Datei legt der steuernde Chat bei. Fehlt sie, läuft nur der Aufruf ohne `--handfelder`, und `--pruefen` darf dann an genau dieser Zeile scheitern („?“ in den Handfeldern). Das ist ein Befund, kein Abbruch.
- Liegt keine Antwort 30a im Repo, entfällt 0c: Die Anfrage allein ergibt keine Indexzeile.

Danach Commit `TB-124 Schritt 0: Stand 30.09. gesichert` mit allem aus 0a und 0c, dann **pushen**.

0d. Ausgang nach `docs/belege/TB-124/0d_ausgang.txt`, mit Bauart wie `docs/belege/TB-122/0b_ausgang.sh`:
- HEAD;
- sha256 der zwei `backtest_breakout.py`, von `research/sync_check/sync_table.py` und `test_sync_check.py`;
- `herkunft.register()` (Soll `01f5997a…`; messen, nicht annehmen);
- die Sonde gegen `sperrliste_abbild_2026-09-26_tb117.json`, nur lesend, wie TB-122 0b (`git status --porcelain` vor und nach zählen);
- für jede Datei, die dieser Auftrag ändert oder anlegt, ob sie in einem Abbildeintrag steht oder in `EINGEFROREN`, gemessen.

0e. db-Sicherung nach ARBEITSWEISE 7c Schritt 0 ⇒ `docs/belege/TB-124/0e_db_sicherung.txt`.

0f. **Datenstand vorher** nach 7c (Soll `d9449faf…`, 223 Dateien) ⇒ `0f_datenstand.txt`.

0g. **Basislauf vorher:** aus der Repo-Wurzel `bash docs/belege/TB-122/c3_tests.sh "$TMPDIR/tb124_c3_vorher"`, Ausgabe ⇒ `docs/belege/TB-124/0g_basis.txt`. Der Ordnername muss dem Muster aus `a3_vergleich.py` Z. 7 folgen; sonst meldet der Vergleich bei `test_entscheidungskerze` eine Scheinabweichung. Die Zeitgrenzen sind dieselben wie in TB-123. Erwartet ist, was TB-123 nachher gemessen hat (`docs/belege/TB-122/c3_nachher.txt`), also u. a. `test_sync_check` 30/3 rc 1. Kennzeichnen:
- die bekannt roten Tests: `test_drawdown_beide_masse` (Zeitgrenze), `test_stabile_sortierung`, `test_wellenauswahl`, `test_drawdown`, `test_sync_check`;
- `test_kursdaten` hängt am Bezugspunkt `origin/main` (TB-123 A3).

Jede andere Abweichung gegen `c3_nachher.txt` ist ein Befund. Das gilt auch für einen bekannt roten Test, der plötzlich grün ist.

Commit `TB-124 0: Ausgang, db-Sicherung, Datenstand, Basislauf`, pushen.

## Schritt A — `test_sync_check` wieder 33/0, ohne den Test zu schwächen

A1. `test_sync_check.py` Z. 131–141 und `sync_table.py` Z. 228–270 lesen. Nachmessen, was unter „Belegt“ steht: Fall a) greift vor dem Import-Fall, und welche Funktion in `volatility_breakout/equity_simulation.py` die zwei Namen als Voreinstellung nutzt (Datei:Zeile).

A2. `sync_table.py` so ändern, dass Fall a) einen Namen, den `equity_simulation.py` **aus `live_params.py` importiert**, als „identisch“ einstuft. Der Hinweis sagt wahrheitsgemäss, wo der Wert als Default wirkt (Funktion in `equity_simulation.py`) und unter welchem Namen er im `backtest_*.py` steht (bei `BB_LOOKBACK`: `SQUEEZE_LOOKBACK_DAYS`). Ein Name, den `equity_simulation.py` nur referenziert, ohne ihn aus `live_params.py` zu importieren, bleibt „im Backtest referenziert“. **Der Test bleibt unverändert** (sha256 vorher = nachher).

A3. ⚠️ **Jeder Hinweistext muss am Code wahr sein**, auch nach B. Die Sitzung prüft ihn je Zeile gegen den Code. Den generischen Satz Z. 266 „wirkt als Default von run_backtest()“ darf sie für die neuen Fälle nicht übernehmen, wo er nicht stimmt. Ihn für die übrigen Fälle zu berichtigen, ist nicht Gegenstand; er wird nur benannt. Lässt sich 33/0 nur mit einem sachlich falschen Hinweis erreichen, gilt:
- A wird nicht committet, `test_sync_check` bleibt 30/3.
- Befund mit Wortlaut von Test und Code.

A4. Konfigurationsprobe wie `docs/belege/TB-123/a3_sync_probe.py` ⇒ `docs/belege/TB-124/a_sync_probe.txt`, dazu `test_sync_check` ⇒ **33/0 rc 0**.

Commit `TB-124 A: sync_table nachgezogen (test_sync_check 33/0)`, pushen.

## Schritt B — F1: Scanbeginn an die Achse binden

B1. In beiden `backtest_breakout.py` beginnt `run_backtest` bei `max(BB_PERIOD, <Lookback, mit dem die Indikatoren des übergebenen Frames gerechnet sind>, VOLUME_AVG_PERIOD) + 1`. Die Zeilen mit `entry_cutoff` bleiben unverändert.

B2. **Vorgabe zur Bauart:** Der Lookback reist **mit dem Frame**. `compute_indicators` hält fest, mit welchem `squeeze_lookback_days` es gerechnet hat (z. B. in `df.attrs`), und `run_backtest` liest es dort. Fehlt die Angabe, gilt die Voreinstellung `SQUEEZE_LOOKBACK_DAYS`.
- *Grund:* Ein neuer Parameter an `run_backtest` bräuchte Aufrufe aus `multi_symbol_optimise.py`, und diese Datei ist nicht freigegeben.
- Wählt die Sitzung eine andere Bauart innerhalb der zwei Dateien, steht der Grund im Ergebnis.
- Vorher messen: Kommt der Vermerk unter der pandas-Fassung von `trading-env` auf **allen** Wegen des Signalpfads bis zu `run_backtest` an (`get_trades_for_symbol` beider Bots, `load_all_symbol_data` ⇒ `get_trades_for_symbol`, `__main__` der zwei Dateien)?

B3. `WARMUP_PERIOD` bleibt als Modulkonstante mit unverändertem Wert stehen. Es ist die Voreinstellung, und die Leser aus „Belegt“ brauchen sie. Die Leser vorher per `grep` messen und im Ergebnis nennen.

B4. Keine andere Änderung, kein Aufräumen, keine Umbenennung.

Commit `TB-124 B: Scanbeginn an bb_lookback gebunden (F1)`, pushen.

## Schritt C — Nachweis (wie TB-122)

C1. **Voreinstellungen ⇒ bytegleich:** `docs/belege/TB-122/a_lauf.py` am Stand nach 0 (vorher) und nach B (nachher), Ausgaben nach `$TMPDIR/tb124_vorher/` bzw. `$TMPDIR/tb124_nachher/`, `cmp` je Datei ⇒ **13/13** (oder so viele, wie der Lauf erzeugt, dann mit Grund). Belege: `c1_vorher_hashes.txt`, `c1_vergleich.txt`. Eine Abweichung ⇒ Abbruch, `git revert` des B-Commits, pushen, melden.

C2. **Ein anderer Wert kommt im Scanbeginn an:**
- Krypto mit Stufe **20** (Register Z. 265), Aktien mit Stufe **20 und 97** (Register Z. 280). Die Stufen werden aus `registerdaten.raster()` gelesen und stehen nicht als Zahl in der Probe.
- Eine synthetische Kursreihe, kein Lesen aus `data/`. Ein Fall wird so gebaut, dass ein Einstiegssignal im heute abgeschnittenen Bereich liegt (nach „Erschlossen“: Balken 39–126 bei Stufe 20, 116–126 bei Stufe 97; die Sitzung misst den Bereich nach). Mit der Stufe wird es gefunden, am Stand vor B nicht.
- Dazu: Ohne Vermerk im Frame beginnt der Scan bei 127.
- **Gegenprobe (40.7):** Am Stand vor B scheitert dieselbe Probe mit **rc 1**. Bauart wie `docs/belege/TB-122/c2_probe.sh` (`git archive` nach `$TMPDIR/tb124_c2_gegenprobe`). Das Skript wird für TB-124 angepasst, weil es `docs/` nicht mit auspackt und auch `rsi2` fährt; die Fassung für TB-124 liegt als `docs/belege/TB-124/c2_probe.sh`.
- Ort: als Erweiterung der zwei `test_posten3_durchreichung.py` der Breakout-Bots (Freigabe-Nachtrag 30.09., ca. 19:44). Ausgabe beider Läufe und der Gegenprobe ⇒ `docs/belege/TB-124/c2_wertprobe.txt`. Die bestehenden Prüfungen der zwei Dateien müssen nachher weiter bestehen (C3, `c3_posten3.txt`).

C3. **Tests nachher, nach Schritt D:** `bash docs/belege/TB-122/c3_tests.sh "$TMPDIR/tb124_c3_nachher"` ⇒ `c3_nachher.txt`. Vergleich gegen `0g_basis.txt` mit `trading-env/bin/python3 docs/belege/TB-123/a3_vergleich.py docs/belege/TB-124/0g_basis.txt docs/belege/TB-124/c3_nachher.txt` ⇒ `c3_vergleich.txt`. Erwartet:
- `test_sync_check` 30/3 ⇒ 33/0 (falls A committet ist);
- die neue Probe aus D steht **nur nachher**, weil `c3_tests.sh` `shared/test_*.py` mitnimmt;
- alles andere gleich.

Dazu separat die drei `strategies/*/test_posten3_durchreichung.py`, vor B und nach B, rc und Schlusszeile ⇒ `c3_posten3.txt`. `c3_tests.sh` führt sie nicht aus.

`git status --porcelain -- . ':!docs'` vor und nach dem Lauf zählen.

C4. **Trockenlauf ohne Modus:** `docs/belege/TB-122/c4_trockenlauf.sh` vorher (0) und nachher (B) ⇒ zeichengleich, `c4_trockenlauf.txt`.

C5. **Sonde und `register()` nachher** wie 0d ⇒ `c5_nachher.txt`. Erwartet ist die Sondenausgabe byte-gleich zu 0d und `register()` unverändert. TB-122 hat gemessen, dass die Sonde Punkt 11 nicht prüfen kann (`docs/belege/TB-122/befunde.txt`).
- Hat 0d die zwei `backtest_breakout.py` doch in einem Abbildeintrag gefunden, ist ein Befund `1` genau an diesem Eintrag mit dem Übergang alt ⇒ neu nach Register 37.3 zulässig (beauftragte Änderung vor dem Tag) und kein Abbruch; er geht in die Tatsachennotiz.
- Jeder andere Befund und jede Änderung von `register()` ⇒ Abbruchkriterium.

C6. **Hash-Übergang:** sha256 vorher und nachher je geänderter Datei unter `strategies/` ⇒ `c6_hashes.txt`.

Commit `TB-124 C: Nachweis F1` (C1, C2, C4–C6), pushen. C3 läuft erst nach D; seine Belege kommen mit dem D-Commit.

## Schritt D — R28: Probe `VERANKERTER_DATENSTAND` gegen Register 18

D1. Eine neue Probe in `shared/`. Dateiname nach Vorgabe `shared/test_verankerter_datenstand.py`, auch als eigene Probe in `shared/test_snapshot.py` möglich; die Sitzung entscheidet und nennt den Grund. Die Probe prüft nach dem Muster von J-r (`research/vorregistrierung/test_ersatzwerte.py:1143–1151`):
- In `docs/VORREGISTRIERUNG_neuselektion.md` gibt es **genau eine** Zeile, die mit ``| Datenstand (`datenstand_hash`) |`` beginnt.
- Deren 64-stelliger Hexwert ist gleich `snapshot.VERANKERTER_DATENSTAND`.

D2. ⚠️ **Die Probe importiert nichts aus `research/vorregistrierung/`.** Den Registerpfad baut sie selbst aus der Repo-Wurzel. *Grund:* Fable 27c Z. 105 — „`snapshot.py` bleibt draussen: Es ist nicht im Laufbereich, und ein Import zöge es hinein — die Sitzung hat das richtig gesehen.“

D3. **Gegenprobe (40.7):** Mit einem abweichenden Wert (Monkeypatch der Konstante bzw. eine Registerkopie mit zwei Datenstandszeilen unter `$TMPDIR`) scheitert die Probe mit rc 1. Belege: `d_probe.txt`.

D4. Nur benennen, nicht ändern: das dritte Literal `SOLL_DATENSTAND` in `research/registernachtrag_tb48/pruefe_abschnitt17.py:97`, mit gemessenem Wert.

Commit `TB-124 D: Probe VERANKERTER_DATENSTAND gegen Register 18 (R28)`, pushen.

## Schritt E — Abgabe

E1. Datenstand nachher (7c) und db-Identität nach 7c ⇒ `e_datenstand_nachher.txt`, `e_db_identitaet.txt`.

E2. `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` enthält:
- Kopf und Kurz-Tabelle wie TB-122;
- die Schritte mit Nachweisen;
- **Entwurf der Tatsachennotiz** für E-2 nach 37.3. Form wie TB-122 Abschnitt 6: Datei, vorher, nachher, Commit, vollzieht. Dazu `register()` alt und neu, Grund 11.3 (F1), und der neue „Stand 11.3“. Als ENTWURF gekennzeichnet;
- den Satz zu R28 für E-2: welche Kopie jetzt welche Probe hat, mit Fundstelle;
- „Für Fable“, nur falls eine Verfahrensfrage entsteht; der steuernde Chat prüft sie nach dem Fable-Filter vor;
- „Nicht getan“ (u. a. `faltenplan_neun.py`-Text, drittes Literal, der generische Hinweis `sync_table.py` Z. 266);
- „In einfacher Sprache“.

E3. Journalblock **DV** ans Ende von `JOURNAL.md` mit der Quellenzeile auf das Ergebnis. Abgabe-Commit `TB-124 Abgabe: Ergebnis, Journal DV`, pushen. Danach `git status --porcelain` nach dem letzten Commit ⇒ `docs/belege/TB-124/e_porcelain.txt`, als letzter kleiner Commit, pushen.

Den `$TMPDIR/tb124_*`-Ordner nicht löschen, sondern seinen Pfad nennen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab.
- C1 ist nicht bytegleich.
- Eine Datei unter `strategies/` ausser den zwei `backtest_breakout.py` und den zwei `test_posten3_durchreichung.py` der Breakout-Bots müsste geändert werden, damit B oder C2 gelingt.
- Die Sonde zeigt nach B einen Befund ausser dem nach C5 zulässigen, oder `register()` ändert sich.
- `git push` scheitert zweimal.

Bei Abbruch: committen, was an Belegen da ist (nie `JOURNAL.md` mit Platzhalter), Grund in `docs/belege/TB-124/abbruch.txt`, pushen, melden. Ein Befund in A oder D ist **kein** Abbruch; der Teil wird weggelassen und benannt.

## In einfacher Sprache

Drei kleine Dinge in einer Sitzung:
- Die zwei Breakout-Bots fangen künftig so früh an zu suchen, wie ihre Einstellung es erlaubt, statt immer erst an Tag 127. Mit den heutigen Einstellungen ändert sich dabei kein einziges Byte.
- Ein Prüfwerkzeug, das seit TB-122 eine Einstellung falsch einsortiert, wird nachgezogen, ohne den Test aufzuweichen.
- Eine fehlende Wache kommt dazu: Sie schlägt an, wenn der im Code verankerte Datenstand vom Register abweicht.
