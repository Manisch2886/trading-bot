# TB-55 — Der Snapshot ist gezogen

**Sitzung 19.09.2026, auf dem MacBook des Betreibers.** Zweig `main`, Basis
`7e48e1f`, kein eigener Zweig, kein Pull Request. Auftrag:
`MAC_TB-55_snapshot_ziehen_v3.md` (formuliert 18.09.2026).
Interpreter durchgehend `trading-env/bin/python3` = **Python 3.9.6**.

---

## Die Kurzfassung

| | |
|---|---|
| ⭐⭐ **`snapshot_hash` — die Zahl, die ins Register kommt** | **`63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2`** |
| `datenstand_hash` | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223** Kursdateien |
| Dateien im Snapshot | **225** = 223 Kursdateien + `config/sp500_top150.txt` + `config/top25_symbols.txt` |
| Bytes gesamt (Manifest) | **211 040 678** |
| Zeitpunkt (Manifest, UTC) | **2026-09-19T06:49:32+00:00** |
| Zugelassene Befunde | **36**, alle `rand_erste`, Herkunft *docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3* |
| Nachprüfung (`--pruefen`) | **`UNVERAENDERT`**, Rückgabewert 0 |
| Datenstand vorher / nach dem Ziehen / am Ende | **dreimal `d9449faf…`/223** |
| Datenbanken gesichert | **12** (nicht neun), alle 12 am Ende byteweise identisch |
| `.gitignore` | ⭐ **NICHT geändert** — `snapshots/` war nie erfasst |
| Repo-Zuwachs | **6 Objekte**: 1 Blob (das Manifest), 4 Trees, 1 Commit — **null Kursdatei-Blobs** |
| Commit | `1075dec` auf `main`, gepusht (`7e48e1f..1075dec`) |
| Registerprüfer (`--basis a1e7fb4`) | vorher **und** nachher **KEIN BEFUND** |

Ort des Snapshots: `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/`
(226 Dateien auf der Platte: die 225 aus dem Manifest plus `MANIFEST.json`, 202 MB).

---

## Schritt −1 — Ortsprüfung

Jede Prüfung getroffen, gemessen vor allem anderen:

| Prüfung | Soll | Ist |
|---|---|---|
| `uname -s` | `Darwin` | `Darwin` |
| `test -x trading-env/bin/python3` | vorhanden | rc 0 |
| `trading-env/bin/python3 --version` | 3.9.x | **Python 3.9.6** |
| `*.db` ausserhalb `trading-env/` | 12, davon 9 `paper_trading_*.db` in der Wurzel | **12 / 9** |
| Arbeitsordner, Zweig | `~/trading-bot`, `main` | `/Users/jaquelineloffler/trading-bot`, `main` = `7e48e1f` |

### Cron-Prüfung (maskiert)

Uhrzeit bei der Prüfung: **08:44 CEST = 06:44 UTC**, Samstag.

* `crontab -l | grep -v '^#' | awk '{print $1,$2,$3,$4,$5}'` — **22 aktive Einträge**
  (40 Zeilen insgesamt, Rest Kommentar/leer). Nur die Zeitfelder wurden
  ausgegeben, kein Befehl.
* `crontab -l | grep -ci 'daten\|fetch\|download\|kurse\|yfinance\|binance'` — **0**.

⭐ **Zähler 0 → kein Abrufeintrag → weiter.** Die Regel T46.4 („kein Datencron")
stimmt mit der Wirklichkeit überein.

Was in die Sitzung fiel, ohne Abruf zu sein: `*/5 * * * *` und `*/15 * * * *`
feuerten während der Sitzung (08:45, 08:50 Ortszeit); `0 * * * *` (der
1h-Bot) erst um 09:00, nach der letzten Messung um 08:52. **Keine der 12
Datenbanken hat sich zwischen 06:45 und 06:52 UTC geändert** — die
5-/15-Minuten-Einträge schreiben also in keine `*.db`. Der Datenstand blieb
ebenfalls stehen.

---

## Schritt 0 — Sicherung und Messung

Sicherungsordner: `~/Sicherungen/tb55_snapshot_20260919T064513Z/`, mit
Pfadstruktur, `cp -p`, dazu `quersummen_vorher.txt`,
`quersummen_nach_ziehen.txt`, `quersummen_ende.txt`.

**Alle 12 gefundenen `*.db`, namentlich** (Grösse, Zeitstempel Ortszeit):

| Datei | Bytes | Zeitstempel |
|---|---:|---|
| `benachrichtigungen_schliessung.db` | 32 768 | 18.09. 23:00 |
| `broker_testnet_t3_supertrend.db` | 94 208 | 19.09. 08:05 |
| `paper_trading_elliott_wave_stocks.db` | 16 384 | 18.09. 22:15 |
| `paper_trading_elliott_wave.db` | 16 384 | 16.09. 23:00 |
| `paper_trading_rsi2_crypto.db` | 16 384 | 16.09. 23:20 |
| `paper_trading_rsi2_mean_reversion.db` | 24 576 | 18.09. 22:20 |
| `paper_trading_t3_supertrend.db` | 16 384 | 19.09. 04:00 |
| `paper_trading_turtle_soup_crypto.db` | 16 384 | 18.09. 00:15 |
| `paper_trading_turtle_soup_stocks.db` | 24 576 | 18.09. 23:15 |
| `paper_trading_volatility_breakout_crypto.db` | 16 384 | 16.09. 23:50 |
| `paper_trading_volatility_breakout.db` | 16 384 | 18.09. 22:50 |
| ⚠️ `strategies/volatility_breakout/paper_trading_volatility_breakout.db` | **0** | **05.09. 21:30** |

Die neun OOS-Datenbanken wurden als **Regel** gefasst (`paper_trading_*.db`
in der Wurzel, D5), nicht über eine Namensliste — Zählung 9.

⚠️ **Befund, nur berichtet:** die 0-Byte-Doppelgängerin unter
`strategies/volatility_breakout/` (SHA-256 `e3b0c442…`, die Quersumme der
leeren Datei) ist **mitgesichert, nicht gelöscht, nicht verschoben, nicht
repariert** — Beweismaterial für TB-53.

Die Kopien wurden mit `shasum -a 256 -c` gegen die Quersummenliste geprüft:
**12/12 OK**.

| Messung | Ergebnis |
|---|---|
| Datenstand vorher (`--nur-hash`) | `d9449faf…`, 223 Kursdateien |
| `snapshots/`, `data/snapshots/` | **beide nicht vorhanden** — kein Snapshot existierte |
| `git status --short` | 0 Zeilen |
| `main` gegen `origin/main` | beide `7e48e1f45d3e0c10eb0badf68015f1c95c383802` |

Zwei `MANIFEST.json` liegen anderswo im Arbeitsbaum und sind **keine**
Snapshots: `data_sicherung/2026-09-15_115131/` (die TB-34-Sicherung,
gitignoriert) und `research/hrp_portfolio/corrected_curves_original/`
(versioniert, Forschungsbeleg).

---

## Schritt 1 — Trockenlauf: jeder Sollwert einzeln

`trading-env/bin/python3 shared/snapshot.py --quelle data`

Die beiden Hashes wurden nicht abgelesen, sondern **maschinell gegen die
Literale in der Auftragsdatei verglichen** (`grep -o` auf die 64-stelligen
Werte, je genau ein Treffer im Auftrag; String-Gleichheit).

| Sollwert | Soll | Ist | |
|---|---|---|---|
| `datenstand_hash` | `d9449faf…ea995f84` | identisch | ✅ |
| ⭐⭐ `snapshot_hash` | `63e4b6c8…cb2ceb2` | identisch | ✅ |
| Kursdateien / gesamt | 223 / 225 | `Kursdateien 223 (Dateien gesamt: 225)` | ✅ |
| Weitere Eingaben | `config/sp500_top150.txt`, `config/top25_symbols.txt` | beide, sonst nichts | ✅ |
| Teilkerzen | 36 Datei(en) mit Befund (223 geprüft) | wörtlich so | ✅ |
| davon zugelassen | 36, Abschnitt 17.3 | `36 Befund(e) in 36 Datei(en) - docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3` | ✅ |
| `NICHT zugelassen` | kommt nicht vor | 0 Vorkommen | ✅ |
| Rückgabewert | 0 | 0 | ✅ |
| Schlusszeile | `TROCKENLAUF - nichts kopiert.` | vorhanden | ✅ |

Nach dem Trockenlauf existierte `snapshots/` weiterhin **nicht**.

---

## Schritt 2 — Ziehen

`trading-env/bin/python3 shared/snapshot.py --quelle data --ziehen`
— gestartet 06:47:54 UTC, beendet 06:49:35 UTC.

* Ziel: `snapshots/63e4b6c8…cb2ceb2/` im Projektwurzelverzeichnis ✅
* Meldung: **`GEZOGEN - 225 Datei(en), 211.0 MB, jede byteweise gegen die Quelle geprueft.`** ✅
* Rückgabewert **0** ✅

Danach, ohne Ausnahme:

1. **Nachprüfung** `--pruefen snapshots/63e4b6c8…`: Soll = Ist für beide
   Hashes, **`UNVERAENDERT`**, rc 0.
2. **Datenstand nach dem Ziehen:** `d9449faf…`, 223.
3. **12/12 Datenbanken** quersummiert: `diff` gegen vorher leer.

---

## Schritt 3 — Die Zahlen für das Register, wörtlich aus dem Manifest

Gelesen mit `json.load` aus `snapshots/63e4b6c8…/MANIFEST.json`:

| Schlüssel | Wert |
|---|---|
| `snapshot_hash` | `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` |
| `datenstand_hash` | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` |
| `kursdateien` / `dateien_gesamt` | 223 / 225 |
| `zugelassene_befunde_anzahl` | 36 (alle `art: rand_erste`) |
| `zugelassene_befunde_herkunft.fundstelle` | `docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3` |
| `zeitpunkt_utc` | `2026-09-19T06:49:32+00:00` |
| `bytes_gesamt` | 211 040 678 |
| `werkzeug` | `shared/snapshot.py` |

**Die Nicht-Kursdateien:** von den 225 Einträgen unter `dateien` passen 223
auf `_1d|_1h|_4h.csv`; die übrigen **zwei** sind genau
`config/sp500_top150.txt` und `config/top25_symbols.txt`. **Keine dritte.**

⚠️ Benannt statt still korrigiert: mein erstes Leseskript nahm an, die
Kursdateien stünden im Manifest mit Präfix `data/`. Sie stehen flach
(`AAPL_1d.csv`), und das Skript zählte deshalb alle 225 als „Nicht-Kurs".
Der zweite Lauf mit dem Endungsmuster liefert die 2. Das Manifest selbst war
nie in Frage — nur meine Annahme über seine Form.

**Kein Registertext wurde geändert.** Der Eintrag folgt als eigener Nachtrag.

---

## Schritt 4 — In das Repo

1. **`.gitignore`:** `grep -i snapshot .gitignore` trifft nur die drei
   `results/portfolio_overview/dashboard_snapshot.json*`-Zeilen;
   `git check-ignore -v` auf `snapshots/`, das Manifest, eine Kursdatei und
   eine `config/`-Datei liefert **rc 1, kein Treffer**. `git status` zeigte
   `?? snapshots/`. ⭐ **Keine Änderung an `.gitignore` nötig, keine gemacht.**
2. `git add snapshots/` — 226 Dateien gestaget, **0 ausserhalb `snapshots/`**;
   `data/`, `shared/`, `strategies/`, `.gitignore` ohne Änderung. Keine
   git-Hooks aktiv. Commit `1075dec`, Push `7e48e1f..1075dec  main -> main`
   in einem Zug, rc 0.
3. **Zuwachs, gemessen:**

| | vorher | nachher | Zuwachs |
|---|---:|---:|---:|
| `git count-objects -vH`: `count` (lose Objekte) | 2 612 | 2 618 | **+6** |
| `git count-objects -vH`: `size` | 156,49 MiB | 156,53 MiB | +0,04 MiB ≈ **+0,026 %** |
| `size-pack` | 3,41 MiB | 3,41 MiB | 0 |
| `du -sk .git` | 165 252 KiB | 165 332 KiB | +80 KiB ≈ **+0,048 %** |

`git rev-list --objects 7e48e1f..1075dec` + `cat-file --batch-check`:
**1 commit, 4 trees, 1 blob.** Der eine Blob ist `MANIFEST.json`
(133 370 Bytes). ⭐ **Für keine der 225 kopierten Dateien wurde ein neuer
Blob angelegt** — git hat die Inhalte als gleich erkannt.

⚠️ Zur Abweichung von den +0,001 % aus TB-46, erklärbar und deshalb kein
Befund: TB-46 mass den **Packfile-Zuwachs von 30 Kursdateien plus
byteidentischer Kopie, ohne Manifest**. Hier kommt ein 133-KB-Manifest hinzu,
das es nur einmal gibt, plus vier Tree-Objekte für 226 Einträge mit
64-stelligen Pfadnamen — und der Nenner ist ein Repo, das derzeit zu 156 MiB
aus **losen** Objekten besteht (nur 3,4 MiB gepackt). Die strukturelle
Aussage, auf die es ankam — *gleiche Inhalte einmal* — ist mit „1 Blob" direkt
belegt.

4. `git status --porcelain` nach dem letzten Commit: **0 Zeilen.**

---

## Zum Schluss — die Kontrollen

| # | Kontrolle | Ergebnis |
|---|---|---|
| 1 | Datenstand vorher / nach dem Ziehen / am Ende | **dreimal `d9449faf…`/223** (06:46, 06:49, 06:52 UTC) |
| 2 | Jede gesicherte `*.db` byteweise identisch | **12/12** vorher = nach dem Ziehen = am Ende; keine Abweichung, nichts zu erklären |
| 3 | `git diff --numstat 7e48e1f..1075dec` | **226 Dateien, 2 793 713 Zeilen hinzugefügt, 0 entfernt** |
| 4 | Registerprüfer `--basis a1e7fb4` | **vorher KEIN BEFUND** (auf `7e48e1f`, in einem temporären Worktree im Scratchpad, danach entfernt) · **nachher KEIN BEFUND** (auf `1075dec`) |
| 5 | Dieses Dokument | endet mit „In einfacher Sprache" |
| 6 | ZIP | `~/Downloads/TB-55_snapshot.zip` — mit vollständigem `MANIFEST.json`, ohne die 225 Kursdateien |
| 7 | Mac-Testauftrag | keiner — diese Aufgabe war der Mac-Lauf |

Zu 4: Der „vorher"-Lauf wurde in der Sitzung erst **nach** dem Commit
nachgeholt, weil ich ihn vor dem Commit übersprungen hatte. Statt zu
behaupten, er wäre gleichwertig, habe ich den Stand `7e48e1f` als Worktree
ausgecheckt und den Prüfer dort laufen lassen; Worktree danach mit
`git worktree remove --force` und `prune` entfernt, `git worktree list` zeigt
nur noch das Hauptverzeichnis.

---

## Was ausdrücklich NICHT passiert ist

| | |
|---|---|
| ❌ | **Kein zweiter Snapshot.** Genau ein Aufruf mit `--ziehen`. |
| ❌ | `data/` nicht verändert — dreimal gemessen |
| ❌ | `shared/snapshot.py`, `shared/paths.py` nicht angefasst; Sperrliste unberührt (`git status` auf `shared/`, `strategies/`: leer) |
| ❌ | Kein Registertext geändert |
| ❌ | Kein Datencron eingerichtet, `crontab -e` nicht aufgerufen |
| ❌ | Kein Bot-Lauf, keine Order, kein Kursabruf |
| ❌ | Kein Basislauf — kein Code geändert |
| ❌ | Keine Übergehen-Flagge (`--kein-anker` nicht benutzt) |
| ❌ | `.gitignore` nicht geändert |
| ❌ | Die 0-Byte-Doppelgängerin nicht gelöscht/verschoben/repariert |

---

## Beobachtungen, die NICHT ausgeführt wurden

1. ⚠️ **`BACKLOG_NACHTRAG_2026-09-19i.md` liegt im Auftragsordner**
   (`~/Downloads/tb55_v3/`) mit der Anweisung „Nachzutragen in
   `docs/projektfuehrung/BACKLOG.md`, als Block 2o". Der Sitzungsauftrag
   nennt nur `MAC_TB-55_snapshot_ziehen_v3.md`; der Nachtrag ist **nicht
   eingefügt**. Das ist eine eigene, kleine Handlung, die auf Anweisung folgen
   kann.
2. **Das Repo besteht aus 2 618 losen Objekten (156,5 MiB) bei nur 3,4 MiB
   Packfile.** Ein `git gc` würde es stark verkleinern. Nicht ausgeführt —
   nicht Teil des Auftrags, und es hätte die Zuwachsmessung verfälscht.
3. **`git fetch --dry-run` in Schritt 0** zeigte einen neuen Remote-Zweig
   `claude/new-session-9qrb42` (vermutlich der Cloud-Lauf vom 19.09., der
   nicht ziehen durfte). `origin/main` war unverändert `7e48e1f`. Der Zweig
   wurde nicht geholt, nicht angesehen.
4. **V5 aus der Vorprüfung** (drei Datenbanken seit 16.09. unberührt:
   `elliott_wave`, `rsi2_crypto`, `volatility_breakout_crypto`) bestätigt
   sich in der Sicherungstabelle oben. Nicht untersucht — eigene, rein
   lesende Aufgabe laut Nachtrag.
5. **`broker_testnet_t3_supertrend.db` trägt 08:05** — passt zum Eintrag
   `5 */4 * * *` (Binance-Testnet-Spiegel, Cron alle 4 h zur Minute 5). Erklärbar,
   kein Befund.
6. Die 22 aktiven Cron-Einträge enthalten `0 6 1 1,4,7,10 *`, `15 6 1 1,4,7,10 *`
   und `30 6 1 1,4,7,10 *` (Quartalsläufe am 1. Januar/April/Juli/Oktober) —
   sie fielen nicht in die Sitzung, ihr Inhalt wurde nicht angesehen.
7. Das Worktree für den „vorher"-Registerlauf hat kurzzeitig eine zweite
   Kopie von `data/` (aus dem git-Inhalt) im Scratchpad angelegt; der Prüfer
   mass dort ebenfalls `d9449faf…`/223 — nebenbei ein vierter Beleg, dass
   der versionierte Inhalt gleich dem Arbeitsbaum ist. Wieder entfernt.

---

## Die Antworten auf die Fragen des Auftrags

* **Wie lautet der `snapshot_hash`?**
  `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2`
* **Hat der Trockenlauf jeden Sollwert getroffen?** Ja — neun Sollwerte,
  einzeln in der Tabelle unter Schritt 1, die Hashes maschinell verglichen.
* **225 Dateien byteweise geprüft, Nachprüfung `UNVERAENDERT`?** Ja, beides,
  je rc 0.
* **Welche zwei Nicht-Kursdateien?** `config/sp500_top150.txt` und
  `config/top25_symbols.txt` — genau diese, keine dritte.
* **Datenstand dreimal gemessen, dreimal derselbe?** Ja: `d9449faf…`/223 um
  06:46, 06:49 und 06:52 UTC.
* **Musste `.gitignore` geändert werden?** Nein — `snapshots/` war nie
  erfasst (`check-ignore` rc 1).
* **Wie gross ist der Zuwachs wirklich?** 6 Objekte, davon 1 Blob (das
  Manifest, 133 KB), 0 Kursdatei-Blobs; +0,04 MiB nach `count-objects`,
  +80 KiB nach `du` — 0,026 % bzw. 0,048 % des losen Objektbestands.
* **Beobachtungen, nicht ausgeführt?** Sieben, oben aufgeführt; die
  wichtigste ist der noch nicht eingefügte Backlog-Nachtrag (i).

---

## In einfacher Sprache

**Was gemacht wurde:** Von allen 223 Kursdateien und den zwei Symbollisten
wurde eine eingefrorene Kopie angelegt — auf dem richtigen Rechner, mit dem
richtigen Programm, nachdem jede einzelne Vorbedingung gemessen und getroffen
war. Diese Kopie heisst nach ihrem Inhalt: `63e4b6c8…`. Das ist die Zahl, die
in das Register kommt.

**Woran man sieht, dass es geklappt hat:** Das Programm hat jede der 225
Dateien Byte für Byte mit ihrem Original verglichen und danach die Kopie noch
einmal gegen ihr eigenes Inhaltsverzeichnis geprüft: unverändert. Der Kennwert
der Originaldaten wurde dreimal gemessen — vor dem Ziehen, danach, am Ende —
und war dreimal derselbe. Die zwölf Datenbanken mit den Handelsergebnissen
wurden vorher gesichert und sind am Ende alle unverändert.

**Was das Repo gekostet hat:** fast nichts. git erkennt gleiche Inhalte und
legt sie nur einmal ab; neu hinzugekommen ist im Wesentlichen nur das
Inhaltsverzeichnis der Kopie. Die Zahl weicht von der Schätzung aus TB-46 ab,
aber aus erklärbaren Gründen — dort war kein Inhaltsverzeichnis dabei.

**Was nicht passiert ist:** Nichts wurde gelöscht, nichts an den Kursdaten
verändert, kein zweiter Snapshot gezogen, keine Regel gebogen. Eine leere
Geisterdatei, die ein Bot einmal am falschen Ort angelegt hat, liegt weiter
dort als Beweisstück. Und der Nachtrag für das Backlog, der im Auftragsordner
mitkam, ist noch nicht eingetragen — das wäre der nächste kleine Schritt.
