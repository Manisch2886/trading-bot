# UEBERGABE 2026-09-24 — Stand des steuernden Chats vor dem Umzug

**Fortgeschrieben 24.09.2026, 22:40 Ortszeit, an einem sauberen Stand:** keine
Sitzung läuft (Wächter 20:33:50Z: *„claude-Prozesse: 0 im Repo, 0 ausserhalb"*),
Arbeitsbaum ohne uncommittete und ohne unverfolgte Datei (gemessen).

⚠️ **Anlass:** Der steuernde Chat vom 21.09.2026, 18:53 wurde **zweimal
komprimiert**. Nach `UMZUG.md` Abschnitt 3 greifen Auslöser **1** (Sitzung
fertig und committet) und **3** (schon einmal komprimiert).

⚠️⚠️ **Jede Aussage hier sagt, ob sie gemessen oder erschlossen ist** —
`UMZUG.md` Abschnitt 5, Verlustkandidat 7.

---

## Block 1 — Der Stand in drei Zeilen

| | |
|---|---|
| **Fertig** | Register bis **Abschnitt 40** · Plan-Punkt 8 vollzogen (Code TB-92, Register TB-94) · Test **188/188** grün · Sitzungswächter mit **Start- und Schliess-Auslöser** · TB-95 bis TB-102 abgegeben · **Fable 24c liegt vor und ist gegengemessen** |
| **Läuft** | ⛔ **nichts.** Kein Fenster offen, kein Auslöser gelegt, Arbeitsbaum sauber |
| **Als Nächstes** | ⭐⭐ **Anfrage 24f an Fable** (drei Messantworten, Block 5 — Text steht dort fertig) · dann **TB-103**: Resolver-Fix und Trockenlauf aller neun Bots im Modus mit Lesehaken |

---

## Block 2 — `HEAD`, Zweig und die Commit-Kette des Tages

**Gemessen am 24.09.2026, 22:33 Ortszeit.**

| | |
|---|---|
| **Zweig** | `main` |
| **`HEAD`** | `d05e3ff3417f617b79bb82e93d3b0592270414ba` (kurz `d05e3ff`) |
| **Alter** | Commit-Zeit 21:32 Ortszeit |
| **Uncommittet** | nur die zwei Dateien aus Block 8 |

⚠️ **Gemessen mit `git --no-optional-locks`, ohne `git status`** — stehende
Regel des Betreibers.

### Die Kette des 24.09.2026 (Ortszeit)

| Zeit | Commit | |
|---|---|---|
| 09:12 | `fc8d44c` | TB-96 Schritt 0 |
| 09:21 | `d0dc890` | TB-96 Block B+C: **Register Abschnitt 40** nach Fable 24a |
| 09:24 | `4777d18` | TB-96 Abgabe (`numstat` 463/0) |
| 09:52 | `79eda3c` | TB-97 Schritt 0 |
| 10:49 | `ae8db0b` | TB-97 Block B+C+D: `F4` beisst |
| 10:49 | `3b60ca8` | TB-97 Block E |
| 10:50 | `e87b06f` | TB-97 Abgabe: **sieben** Mutationsproben statt acht |
| 15:00 | `a58ed1d` | TB-98 Schritt 0 |
| 15:15 | `46e3ed0` | TB-98 Block B: `positionen_holen.py` nach **36.1** |
| 15:16 | `c25a91f` | TB-98 Block A |
| 15:19 | `bba6f25` | TB-98 Abgabe: ⚠️⚠️ **der stille Rückfall** |
| 21:14 | `1c09f3e` | TB-102 Schritt 0 |
| 21:32 | `d05e3ff` | TB-102 Abgabe: ⚠️⚠️ **bytegleich ohne Snapshot** |

---

## Block 3 — Die tragenden Zahlen, jede mit ihrer Fundstelle

| Sache | Wert | Fundstelle | |
|---|---|---|---|
| **Register** | **7993 Zeilen**, Abschnitte **0–40** | `docs/VORREGISTRIERUNG_neuselektion.md` | gemessen |
| Abschnitt 39 | Z. 7139 — Vollzug Sperrlistenpunkt 4 | ebenda | gemessen |
| Abschnitt 40 | Z. 7632 — Testannahmen, neun Listen als Eingabedateien | ebenda | gemessen |
| **Sperrliste** | **14 Punkte** | ebenda, Abschnitt 10, Z. **843–1050** | gemessen |
| **Snapshot** | `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` | `snapshots/` | gemessen |
| Snapshot-Dateien | **225** | ebenda | gemessen |
| **`datenstand_hash`** | `d9449faf51bffaaa` | Register | gemessen |
| **Test** | **188 / 188** grün (vorher 163 / 2) | TB-92, TB-94 | gemessen |
| **`BACKLOG.md`** | 603 Zeilen | `docs/projektfuehrung/BACKLOG.md` | gemessen |
| **`ARBEITSWEISE.md`** | Abschnitte bis **22.8** | ebenda Z. 1818 ff. | gemessen |
| ⭐ **Freie TB-Nummer** | **TB-103** | höchste vergebene: TB-102 | gemessen |
| Anmerkung | TB-99 ist **keine Auftragsnummer**, sondern die **Wächtersonde** | ARBEITSWEISE 22.2 | — |

⚠️ **Sperrlistenpunkte im Text unten:** **2** (Faltengrenzen, Go-Live-Schnitt,
Purge-Längen, Faltenlängen) · **4** (Drawdown-Bedingung) · **8**
(Universumsdateien) · **10** (Zuteilungskaskade inkl. Seed).
`shared/paths.py` steht auf **keinem** Punkt (gemessen, TB-98).

---

## Block 4 — Offene Punkte vor dem signierten Tag, in Reihenfolge

⭐ **Die Reihenfolge ist Fables** — seine Antwort **24c, Abschnitt 6**. Sie
ersetzt die Reihenfolge aus 24b D.

| | Punkt | Warum an dieser Stelle |
|---|---|---|
| ⭐⭐ **1** | **Resolver** (24b A2) — `shared/paths.py`: unter dem Modus `CONFIG_DIR = <snapshot>/config`, ohne Fallback, Rückgabe `2`, **Abbruch statt Warnung** | ⚠️⚠️ **Tagblocker.** Fable: *„vorher nichts anderes"* |
| **2** | **`messgroessen.py` auf den Resolver** + Haltedauer-Quelle auf die neuen Listen | `TB30A_BASE_DIR` ist **kein** Snapshot-Weg mehr |
| **3** | **Erzeuger auf dem Signalpfad** (24b A3, **erweitert um `exit_time` und `haltedauer_balken`**) — eine Eingabe, zwei Herleitungen; Modus-Lauf mit **beiden** Nachweisteilen | |
| **4** | **Register 41 / 42** | Reichweite 5.4 · Berichtigung 2d-Herleitung · Donchian-Herleitung · Nachweis mit zwei Teilen · Resolver-Pflicht · drei Tatsachennotizen |
| **5** | **Danach** | Faltenlänge gegen 33.2 · `messgroessen.json` neu · Raster nachziehen · `purge_tage` gegen das heutige als Tatsachennotiz · Abbild |

### ⚠️⚠️ Der Tagblocker (TB-98 Befund 1, gemessen)

Unter dem Selektionsmodus (`TB_SELEKTIONSWURZEL`) finden **alle neun Bots** ihre
Symbolliste nicht: Der Snapshot legt die zwei Universumsdateien unter `config/`
ab, `shared/paths.py` setzt `CONFIG_DIR` auf die **flache** Snapshot-Wurzel.
`symbols_config.py` und `stocks_symbols_config.py` finden nichts — und nehmen
**still** ihre eingebaute Fünf-Symbol-Standardliste.

⛔ **Das Protokoll meldet dabei:** *„Geladen: 5 von 5 Symbolen. Keines
ausgelassen."*

| | mit Modus | ohne Modus |
|---|---|---|
| Kursdaten | ⭐ aus dem Snapshot, 9/9, 0 Zugriffe auf `data/` | `data/` |
| Symbolliste | ⛔ **9× Standardliste (5)** | Krypto 18/24 bzw. 20/24, Aktien 147/150 |

⚠️ **Reichweite:** jeder Lauf unter dem Modus, also auch **der signierte Tag**.
Vor TB-98 hat **kein** Bot-Lauf unter dem Modus gegen den echten Snapshot
stattgefunden — **es ist niemandem aufgefallen, weil es niemand getan hat.**

⚠️⚠️ **Die Freigabe des Betreibers für `shared/paths.py` steht noch aus.** Sie
ist das Erste, was der neue Chat als Auswahlkarte stellt.

### ⭐⭐ Was Fable in 24c neu entschieden hat

| | Entscheidung | Folge |
|---|---|---|
| **1** | **Ein Nachweis hat ZWEI Teile:** (a) bytegleich **und** (b) **Leseprotokoll** — alle Lesezugriffe innerhalb `snapshots/<hash>/` oder auf registrierten Eingabedateien, **null** im Repo-Arbeitsstand. Fehlt (b) oder zeigt es einen Zugriff ausserhalb ⇒ **Befund 2**, gleich was (a) sagt | ⛔ *„Bytegleich ohne Leseprotokoll ist kein Nachweis, sondern ein Zufall, der heute stimmt."* ⇒ **Der TB-93/TB-102-Nachweis für `messgroessen.json` ist Befund 2 — nicht geführt** |
| **2** | **Resolver-Pflicht:** Jedes Modul des Laufbereichs, das Kursdaten oder Universumsdateien liest, bezieht seine Pfade über `shared/paths.py::get_strategy_paths()`. Eigene Pfadlogik ⇒ Befund **1** der Lesequellen-Sonde | Es gibt **eine** Anordnung, die der Snapshot vorgibt |
| **3** | ⭐⭐ **Reichweite des Grundsatzes aus 5.4:** **Keine** Festlegung vor dem Lauf (Faltenlänge, Purge, Embargo, Trainingsende, Rastergrenzen) wird aus Grössen hergeleitet, die vom **Positionslimit** oder von der **Ausführung** abhängen. Herleitungen aus Trades verwenden **gefundene** Trades | ⭐ *„Nicht zirkulär im Lauf, aber inkonsistent in der Herleitung"* |
| **4** | **`purge_tage` neu:** nicht aus der maximalen Haltedauer eines Parameterstands, sondern als **Schranke über das registrierte Raster** | Begründung: ein zu kurzes Purge **bevorzugt systematisch Zellen mit langen Haltedauern** |
| **5** | **Donchian-Untergrenze** (zwei Bots): aus `median_balken` der **gefundenen** Trades | Rastergrenze bleibt gemessen, nur die Eingabe wechselt |
| **6** | **Eine Eingabe, zwei Herleitungen:** Haltedauern kommen aus denselben neuen Listen wie die Faltenlänge. `haltedauern_je_bot.csv` **und** `tb24_haltedauern/auswertung.py` werden **historischer Stand mit Tatsachennotiz** | Die neuen Listen bekommen `exit_time` und `haltedauer_balken` |

---

## Block 5 — ⭐⭐ Vormessung zu Fable 24c: seine drei offenen Punkte, gemessen

⚠️⚠️ **Dieser Block ist der Text der Anfrage 24f.** Er ist vollständig gemessen
am 24.09.2026, 22:25–22:35, `HEAD d05e3ff`. Der neue Chat muss ihn nur noch
formatieren und als Kopierblock ausgeben. **Sichtschutz 27.1 gewahrt** — keine
Ergebnisgrösse des Selektionsraums.

### (1) Fables Unsicherheit: steht die Purge-Herleitung im Registertext oder im Code?

⭐ **Im Registertext — deine Berichtigung ist also eine Berichtigung des
Registertexts.** Gemessen, Register **5.1 Nr. 5** (Z. 579–583), wörtlich:

> **Purge und Embargo** in Höhe der **maximalen gemessenen Haltedauer** des
> Bots, aus `research/tb24_haltedauern/`.

⚠️⚠️ **Aber der Befund geht weiter, und er verkleinert deine Berichtigung:**

| Stelle | Herleitung heute, gemessen | hängt an ausgeführten Trades? |
|---|---|---|
| **5.1 Nr. 5** (Purge/Embargo zwischen Falten) | max. gemessene Haltedauer | ⚠️ ja — ⭐ **aber bereits überholt**: Der Nachtrag darüber (Z. 549–551) stellt Nr. 5 ausdrücklich als **Verfahren-A-Relikt** fest, und 2d (c) sagt: *„Zwischen Selektionsfalten gibt es weder Purge noch Embargo."* |
| **2d (d)** Embargo vor der Bestätigungsperiode, **8 Bots** | Konstante `MAX_HOLD_DAYS` / `MAX_HOLD_HOURS` **im Code** | ⭐ **nein** — rasterunabhängig, über alle Zellen dieselbe Schranke |
| **2d (d)**, `t3_supertrend` | P95 der Haltedauer aus **656 ausgeführten Positionen** | ⚠️⚠️ **ja — die einzige Stelle** |
| **Donchian-Untergrenze** (zwei Bots) | `median_balken` aus ausgeführten Trades | ⚠️⚠️ **ja** |
| **`purge_tage`** in `messgroessen.json` → Trainingsende | `max_tage` aus ausgeführten Trades | ⚠️ ja |

⇒ ⭐ **Deine Sorge „ein Purge, das für genau einen Rasterpunkt bemessen ist"
trifft nicht überall.** Bei acht von neun Bots ist die Schranke eine
**Code-Konstante**, hängt also weder am Positionslimit noch an der Ausführung.
Sie trifft an **genau zwei** Stellen: `t3_supertrend` und der
Donchian-Untergrenze.

⚠️ **Und eine Frage zurück:** 2d (d) ist selbst **ersetzt** durch Abschnitt 16
(TB-41), 16.6 — das Embargo ist dort keine feste Frist mehr, sondern eine
**Bedingung am Positionsbestand** mit dieser Frist als **Deckel**; die
Embargo-Tabelle gilt als **obere Schranke** weiter. **Zielt deine Berichtigung
auf die obere Schranke oder auf die Bedingung?**

### (2) Fables Unsicherheit: haben alle neun Strategien einen begrenzten Ausstiegshorizont als Rasterachse?

⛔ **Nein — und zwar bei keinem einzigen.** Gemessen über
`registerdaten.py::raster_definition()`, alle neun Achsenlisten:

| Bot | Rasterachsen (gemessen) |
|---|---|
| `elliott_wave` | `deviation_pct`, `stop_loss_pct`, `take_profit_fib` |
| `elliott_wave_stocks` | + `max_concurrent_positions` |
| `t3_supertrend` | `adx_threshold`, `max_concurrent_positions`, `stop_loss_pct`, `t3_fast_length`, `t3_slow_length` |
| `rsi2_crypto` / `rsi2_mean_reversion` | `max_concurrent_positions`, `rsi_threshold`, `sma_trend_filter`, `stop_loss_pct` |
| `turtle_soup_crypto` / `turtle_soup_stocks` | `donchian_period`, `max_concurrent_positions`, `stop_mode` |
| `volatility_breakout` / `volatility_breakout_crypto` | `bb_lookback`, `bb_squeeze_percentile`, `max_concurrent_positions`, `stop_loss_pct` |

⇒ ⛔ **`max_hold_days` / `max_hold_hours` ist in keiner Achsenliste.** Deine
Anordnung *„aus den registrierten Rastergrenzen der Ausstiegsachsen"* lässt sich
für **keinen** Bot so ausführen — diese Rastergrenzen gibt es nicht.

⭐ **Die gute Nachricht:** Genau deshalb ist die Sache einfacher. Ist die
Zeitbremse eine **Konstante**, hängt die maximale Haltedauer gar nicht am
Positionslimit — sie ist über alle Rasterzellen dieselbe Schranke, also schon
das, was du verlangst.

⚠️ **Genau ein Bot hat keine Zeitbremse: `t3_supertrend`.** Das steht bereits
als gemessene Tatsachennotiz im Register (2d, Anmerkung 2), belegt über TB-24
und `research/tb24_haltedauern/BERICHT.md` Abschnitt 1 (*„acht Bots mit
Zeitausstieg"*). ⇒ **Dein Zusatz greift bei genau diesem einen Bot.**

⭐ **Ein Nebenbefund:** `elliott_wave` führt `max_concurrent_positions` **nicht**
als Rasterachse. Bei ihm ist das Positionslimit also gar kein Rasterparameter —
der Grundsatz aus 5.4 greift dort aus einem anderen Grund als bei den acht
übrigen.

### (3) Fables Frage: hatte TB-91 A1b ein Leseprotokoll? — **Nein**

| | gemessen |
|---|---|
| **TB-91** (`docs/belege/TB-91/`, 21 Dateien) | ⛔ **null Treffer** für „Lesehaken", „Leseprotokoll", `addaudithook`. Der Lesehaken entstand erst mit **TB-95** (`docs/belege/TB-95/haken/sitecustomize.py`) |
| **TB-95 D1** | ⭐ **hat eines** — `benchmark.py` im Modus-Lauf, mit Aufrufstapel |
| ⚠️ **Aber der Lauf-Typ ist ein anderer** | TB-95 lief über einen **Hilfsordner**: `data/` → Verknüpfungen auf die Snapshot-CSV, `config/` → `<Snapshot>/config/`, alles Übrige → Repo (`d_lauf.sh`). Das ist TB-102 **Lesart 3** („Snapshot-Inhalt in Repo-Anordnung"), **nicht** `TB_SELEKTIONSWURZEL` |
| ⚠️⚠️ **Und es weist einen Zugriff ausserhalb NACH** | TB-95 Abschnitt 3, wörtlich: *„Liegen sie im Snapshot? **Nein.** … die Listen kommen im Modus-Lauf aus dem Repo"* — und sie sind **keine registrierten Eingabedateien** (Register **39.8**, *„zwei Eingaben ohne registrierten Eingabestand"*) |

⇒ ⚠️⚠️ **Nach deiner Zwei-Teile-Regel ist TB-91 A1b ebenfalls Befund 2** — nicht
weil das Leseprotokoll fehlt, sondern weil das spätere Leseprotokoll einen
Zugriff ausserhalb **belegt**: die neun Listen aus dem Repo.

⭐ **Das ist konsistent und behebbar:** Genau diese neun Listen werden nach 24b
A3 neu erzeugt und bekommen einen registrierten Eingabestand. **Danach** ist der
Benchmark-Nachweis führbar — vorher nicht. ⇒ Er gehört als eigener Punkt hinter
deinen Plan-Punkt 3.

⚠️ **Eine Frage dazu:** Ist der **Hilfsordner-Weg** (Snapshot-Inhalt über
Verknüpfungen in Repo-Anordnung) nach der Resolver-Pflicht noch ein zulässiger
Modus-Lauf — oder ist künftig nur `TB_SELEKTIONSWURZEL` zulässig? ⭐ *Wir neigen
zum Zweiten: Nach dem Resolver-Fix wird der Hilfsordner überflüssig, und zwei
zulässige Wege sind wieder einer zu viel.*

---

## Block 6 — Wartezustände: was auf wen wartet

| wartet | auf | seit |
|---|---|---|
| ⭐⭐ **Der Betreiber** | **Freigabe für `shared/paths.py`** (Resolver-Fix) — Auswahlkarte, noch nicht gestellt | 24.09., 22:05 |
| ⭐⭐ **Fable** | **Anfrage 24f** — der Text steht fertig in Block 5, noch nicht übergeben | 24.09., 22:40 |
| **Eine Mac-Sitzung** | ⛔ **keine.** Kein Fenster offen | — |
| ✅ **Erledigt** | Anfrage 24e ist beantwortet (**24c**, 24.09., 22:16) | — |

---

## Block 7 — Freigaben und Sperrlisten-Stand

⚠️⚠️ **Freigaben verfallen nicht von selbst. Diese beiden sind erteilt und
UNVERBRAUCHT:**

| | Freigabe | erteilt | Stand |
|---|---|---|---|
| **1** | **`research/vorregistrierung/faltenplan.py`** — Sperrlistenpunkt **2**, Registerabschnitt **37.3** | 24.09.2026, 11:25, Betreiber: *„Ja, beides freigegeben"* | ⭐ **unverbraucht** |
| **2** | **Ein neues Sperrlisten-Abbild** | ebenda | ⭐ **unverbraucht** |

| | offen | |
|---|---|---|
| ⚠️⚠️ | **`shared/paths.py`** (Resolver-Fix, TB-103) | steht auf **keinem** Sperrlistenpunkt (gemessen) — die Entscheidung liegt trotzdem beim Betreiber |
| ⚠️ | **`messgroessen.py`** (Umstellung auf den Resolver, Fable 24c Abschnitt 2) | ebenfalls zu erfragen |

### Sperrlisten-Stand

| Punkt | Stand |
|---|---|
| **4** (Drawdown-Bedingung) | ⭐ **vollzogen**, Register Abschnitt 39, Form (ii) |
| **2** (Faltengrenzen u. a.) | Freigabe erteilt, **noch nicht vollzogen** |
| **10** (Zuteilungskaskade) | gesperrt — ⚠️ **deshalb muss sich der Erzeuger ändern, nicht die Zuteilung** (TB-98 Befund 2) |
| **8** (Universumsdateien) | gesperrt — ⭐ der Resolver-Weg lässt ihn unberührt |

---

## Block 8 — ⭐ Die Fehler dieses Chats und die Regeln daraus

**Ohne diesen Block wiederholt der neue Chat sie.**

| | Fehler | ⭐ Die Regel daraus |
|---|---|---|
| **1** | **Doppelte Abschnittsnummern** in `ARBEITSWEISE.md` (15/16/17 zweimal) | Vor jeder neuen Nummer die vorhandenen **messen**, nicht erinnern |
| **2** | ⚠️⚠️ **Abschnitt 22.6 mit falschem Kriterium geschrieben** („Rechenzeit klein gegen Laufzeit = untätig"). Gegenprobe: TB-95 **untätig 1,6 %**, TB-92 **arbeitend 4,8 %** — beide `S+` | **Aus zwei Zahlen derselben Sitzung folgt keine Regel.** Ein Kriterium braucht einen **Gegenfall**. Berichtigt in **22.7** und im Wächter-Hinweistext (Z. 232) |
| **3** | **`git status` benutzt**, obwohl die stehende Regel es verbietet | Ersatz: `git --no-optional-locks diff --stat HEAD` und `git --no-optional-locks ls-files -o --exclude-standard` |
| **4** | ⚠️ **„von Befund 1 nicht betroffen" behauptet** für `messgroessen.json` nach nur **einem** geprüften Pfad — die zweite Kette lag daneben | **Eine Kette ist erst geprüft, wenn alle ihre Eingaben geprüft sind** |
| **5** | **Vormessung falsch:** „`G8` prüft `median_balken`" — gemessen prüft es `max_tage` | ⭐ **Genau dafür ist die Vormessung da** (`A8`): bei Abweichung gilt die Nachmessung. Die falsche Vormessung ist kein Schaden, sondern der Beweis, dass das Verfahren greift |
| **6** | **Hilfsdateien im Repo gelassen** | Aufräumen über `device_request_delete_permission` |
| **7** | ⚠️⚠️ **Das Ablagewerkzeug meldete „written" und schrieb die ALTE Fassung** — dieses Dokument lag nach einer Korrektur mit 23 769 statt 24 008 Bytes auf dem Gerät. Erst die Byteprüfung hat es gezeigt | ⭐ **Nach JEDEM Ablegen `md5sum` und `wc -c` auf beiden Seiten vergleichen** — nie auf die Erfolgsmeldung vertrauen (`UMZUG.md` Schritt 1, seit 19.09. bekannt, hier zum zweiten Mal eingetreten). **Abhilfe:** unter einem frischen Quelldateinamen neu ablegen; ein zweites Ablegen desselben Quellpfads wirkte nicht |

### ⚠️⚠️ Die zwei Rügen des Betreibers — beide strukturell

| | Rüge | ⭐ Ursache und Abhilfe |
|---|---|---|
| **1** | *„Wieso holst du dir das Ergebnis TB 95 nicht selbstständig ab?"* (07:07) | **Es gibt kein Signal, wenn eine Mac-Sitzung fertig ist.** ⇒ Nach jedem Auslöser die **Nachschau planen** (`send_later`) — ARBEITSWEISE **22.5**. ⭐ Gleiches gilt für Fable-Antworten in der Projektablage |
| **2** | *„wieso schickst du mir die fable anfragen nicht?"* (21:15) | ⚠️⚠️ **Das Ablegen fühlt sich wie Erledigung an.** Es ist keine. ⇒ **Eine Fable-Anfrage ist erst übergeben, wenn sie als Kopierblock in der Antwort stand** |

---

## Block 9 — Was zwischengelagert und noch nicht eingearbeitet ist

| Datei | Zielort | Stand |
|---|---|---|
| `FABLE_ANFRAGE_2026-09-24e_richtiges_ergebnis_falscher_ort.md` | `docs/projektfuehrung/` | ⚠️ **abgelegt, uncommittet** |
| `UEBERGABE_2026-09-24.md` (dieses Dokument) | `docs/projektfuehrung/` | ⚠️ ebenso |
| ⚠️⚠️ `FABLE_ANTWORT_2026-09-24b_rueckfall_mutationen_erzeuger.md` **und** `FABLE_ANTWORT_2026-09-24c_nachweis_hat_zwei_teile.md` | `docs/projektfuehrung/` | ⚠️ liegen **nur in der Projektablage**. Gemessen: **33** Fable-Antworten im Repo, die letzte ist **24a** — diese zwei fehlen. ⇒ **Aufgabe für TB-103 Schritt 0:** aus der Projektablage lesen und im Repo ablegen |
| `logs/auftraege/` | — | ⭐ leer im Sinn der Bringschuld |

⚠️ **Warum nicht committet:** stehende Regel — *„Kein `git add`, kein Commit
über die Anbindung."* Der steuernde Chat legt ab, die Mac-Sitzung committet
(Schritt 0 von TB-103).

---

## Block 10 — Der Eröffnungstext

⭐ **Die einzige Fassung steht in `UMZUG.md`, Abschnitt 6.** Hier steht bewusst
**keine Kopie**. ⚠️ Zeile Nr. 1 wurde für diesen Umzug auf
`projektfuehrung/UEBERGABE_2026-09-24.md` mitgezogen.

---

## Die Werkzeuge, die der neue Chat sofort hat

| Werkzeug | Wie | steht in |
|---|---|---|
| ⭐⭐ **Sitzungswächter, Start** | Datei `docs/auftraege/_ausloeser/starte_TB-<Nummer>` | ARBEITSWEISE **19** |
| ⭐⭐ **Sitzungswächter, Schliessen** | Datei `docs/auftraege/_ausloeser/schliesse_<40 Hex-Zeichen des gelesenen HEAD>` | ARBEITSWEISE **22.8** |
| ⭐ **Sonde ohne Start** | `starte_TB-99` — misst, ob eine Sitzung läuft, startet nichts | ARBEITSWEISE **22.2** |
| ⭐ **Wächterprotokoll** | `logs/sitzungswaechter/waechter.log` — über die Anbindung lesbar | — |
| ⭐ **Nachschau** | `send_later` nach **jedem** Auslöser | ARBEITSWEISE **22.5** |
| **Aufwandsstufe** | **hoch** | ARBEITSWEISE **22.1** |
| **Der Einfügesatz** | **immer** im Kopierfeld am **Schluss** der Antwort, mit iPhone-Alternative zu `Strg`+`D` | ARBEITSWEISE **22.4** |

⚠️ **Schliess-Bedingungen, dreifach geprobt:** 40 gültige Hex-Zeichen im Namen ·
Name **gleich `HEAD`** · letzter Commit **mindestens 600 s** alt. ⛔ Nach `TERM`
wird **nicht** nachgetreten.

---

## ⚠️ Stehende Sicherheitsregeln — sie gelten unverändert weiter

| | |
|---|---|
| ⛔ | **Es wird gar kein Befehl vorgeschlagen, dessen Ausgabe einen Schlüssel enthalten KÖNNTE.** Nie: `cat`, `head`, `tail`, `less`, `more`, `env`, `printenv`, `echo $VAR`, `set` auf `.env`, Konfigurationsdateien, Schlüsselablagen oder Logs; `git diff`/`git show` auf solchen Dateien; `security find-generic-password`; jedes `curl` mit Header im Klartext. Stattdessen `grep -c`, `test -f`, `wc -l`. ⭐ **Geprüft wird die Existenz, nie der Wert** |
| ⛔ | `crontab -l` wird **nie ungefiltert** ausgegeben (`K2a`) |
| ⛔ | **Kein `git status`, kein `git add`, kein Commit über die Anbindung.** Lesende git-Befehle nur mit `--no-optional-locks` |
| ⛔ | **Keine SQLite-Datei öffnen** über die Brücke |
| ⛔ | **Nichts nach `docs/` schreiben, solange eine Sitzung läuft** ⇒ vorher die Sonde `starte_TB-99` |
| ⛔ | **Nie überschreiben, immer neuer Dateiname**, danach mit `wc -c` und `grep` nachprüfen |
| ⛔ | Befehle für den Betreiber sind **EINE ZEILE** — Termius zerlegt mehrzeilige Blöcke |
| ⛔ | **Sichtschutz 27.1:** keine Ergebnisgrössen des Selektionsraums an Fable vor dem signierten Tag. **27.2** erlaubt Verfahrensmessungen |
| ⭐ | **Jede Entscheidung des Betreibers kommt als anklickbare Multiple-Choice-Frage** — dreimal angemahnt (ARBEITSWEISE **20**) |

---

## ⚠️ Die Brücken-VM ist NICHT der Mac

**Gemessen, mehrfach:** Die Geräteanbindung führt in eine **isolierte Linux-VM**
mit einem FUSE-Mount des Repos unter `$HOME/mnt/trading-bot`. ⛔ **Mac-Prozesse
sind von dort nicht messbar** — deshalb existiert der Sitzungswächter.

---

## In einfacher Sprache

**Wo wir stehen:** Das Register ist bis Abschnitt 40 geschrieben, der Test ist
grün, Punkt 8 des Plans ist erledigt. Es läuft gerade nichts, alles ist
gesichert.

**Was heute Abend dazugekommen ist:** Fable hat auf die letzte Anfrage
geantwortet, und seine Antwort ist die folgenreichste bisher. Sie enthält drei
Dinge. Erstens: Ein Nachweis besteht ab jetzt aus zwei Teilen — das Ergebnis
muss stimmen **und** es muss protokolliert sein, woher gelesen wurde. Damit ist
ein bisher als erfüllt geltender Nachweis nicht mehr erfüllt. Zweitens: Alle
Programme, die Kursdaten lesen, bekommen denselben zentralen Pfadgeber — das
behebt zugleich den Fehler, durch den alle neun Bots im geschützten Modus still
auf fünf statt auf 24 beziehungsweise 150 Symbole zurückfallen. Drittens, und
das ist der grösste Punkt: Das Regelwerk begründet an einer Stelle, warum eine
Festlegung nicht von den tatsächlich ausgeführten Geschäften abhängen darf.
Fable entscheidet, dass dieser Grundsatz überall gilt.

**Was wir dazu schon gemessen haben:** Fable hat selbst gesagt, wo er unsicher
ist. Alle drei Punkte sind nachgemessen, und zwei davon fallen kleiner aus, als
er annahm: Bei acht der neun Bots steht die fragliche Grösse als feste Zahl im
Programm und hängt gar nicht an dem, was er befürchtet — betroffen sind genau
zwei Stellen. Dafür fällt der dritte Punkt grösser aus: Auch der zweite,
bislang als erfüllt geltende Nachweis ist es nach der neuen Regel nicht.

⚠️ **Das Erste im neuen Chat ist deshalb eine Entscheidung:** ob die zentrale
Pfadstelle geändert werden darf. **Ohne das läuft der signierte Tag auf fünf
Symbolen statt auf allen.**
