# TB-112 — Bündel: 19 auf den Laufbereich (Tag-Vorbedingung), db-Sicherung als Skript, `tb40_test_*` aufräumen

**Sitzungstitel:** `TB-112` · **Angelegt:** 26.09.2026, 07:10, vom steuernden Chat
**Vorgänger:** TB-110 (`6a7996a`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)
**Parallel:** Sitzung B (TB-111) arbeitet, falls gestartet, im Worktree `~/trading-bot-tb111` auf Zweig `tb-111`. ⛔ **Diesen Worktree nicht betreten**, nicht `git worktree prune`, nicht `git branch -D`.

## ⭐⭐ Freigaben des Betreibers, wörtlich

**26.09.2026, ca. 06:40, Auswahlkarten im steuernden Chat (Runde 1 und 2 zu Fable 25f):**

| Frage | Antwort |
|---|---|
| Freigabeklassen (25f Entsch. 6) | **„Handwerk pauschal (Empfohlen)“**: Handwerk ohne Sperrlistennähe (Ablagen, Stummel, Tatsachennotizen, Testdateien) pauschal frei; Registertext, Sperrliste, Live-Code und Reihenfolge einzeln |
| Die billigen Dinge vor dem Tag | **„Alle“** (O6 db-Sicherung, V8/F3, F4, W2) |
| Ziel der db-Sicherung | **„iCloud Drive (Empfohlen)“** |
| Bündelung (25f A3) | **„Ja, Bündel (Empfohlen)“** |

**26.09.2026, ca. 07:00:** *„Der nächste Auftrag für den Hauptordner (TB-112, parallel zu B) soll ein Bündel sein. Welche Teile gebe ich frei?“* ⇒ **„Alles“**:
- **19 auf den Laufbereich**: `shared/paths.py`, nur unter dem Modus;
- **db-Sicherung als Skript**: lesend mit `sqlite3 .backup` und Quersumme nach iCloud; die Cron-Zeile trägt der Betreiber selbst ein;
- **`tb40_test_*` aufräumen** in `test_universum_trockenlauf.py`.

| freigegeben | Pfad | Art |
|---|---|---|
| ✔ | `shared/paths.py`: `ARBEITSBAUM_PFADE` erweitern, Ausnahme für registrierte Protokolle; **nur im Modus-Zweig** | Resolver, **nicht** auf der Sperrliste (Abbild `sperrliste_abbild_2026-09-25b.json`, `40ffe18d…`: `grep -c paths.py` = 0, gemessen 26.09., 07:05) |
| ✔ | `shared/test_startpruefungen.py` und neue Testdatei(en) unter `shared/` | Test |
| ✔ | neu `docs/werkzeuge/db_sicherung/` (Skript, LIESMICH) | Werkzeug |
| ✔ | `research/universum_trockenlauf/test_universum_trockenlauf.py` (Z. 123, 136, 192 `tb40_test_*`; prüfen: Z. 902 `tb44_l_`) | Testdatei |
| ✔ | `docs/belege/TB-112/`, `docs/ERGEBNIS_TB-112_…md`, Journalblock | Belege |

⛔ **Nicht freigegeben:**
- alles unter `research/vorregistrierung/` ausser Lesen;
- `shared/strategy_paths.py`, `regimewache.py`;
- alle `forward_test.py`/`live_params.py`/`equity_simulation.py`;
- die Cron-Wächter;
- **`crontab`** (nur lesen verboten, schreiben erst recht);
- Register und Sperrliste;
- **jede `*.db` zum Schreiben**. Lesen nur über `sqlite3 … ".backup …"` und `PRAGMA integrity_check` an der **Kopie**.

---

## 0. Schritt 0

**0a — Arbeitsbaum des steuernden Chats committen.** Erwartet unter `docs/`:
- `auftraege/MAC_TB-112_19_laufbereich_db_sicherung.md` (dieser Auftrag);
- `auftraege/AKTUELLER_AUFTRAG.md` (Zeiger TB-112, TB-111 bleibt);
- `projektfuehrung/UEBERGABE_2026-09-25.md` (Nachtrag 4);
- `projektfuehrung/ENTSCHEIDUNGEN_2026-09-26_fable25f.md` (die Karten vom Morgen).

Liegt etwas anderes da: nicht committen, melden. Commit-Text „TB-112 Schritt 0: Arbeitsbaum des steuernden Chats (…)“, dann `git push origin main`.

**0b:** `git --no-optional-locks worktree list` notieren; `tb-111` nicht anfassen.

**0c:** Am Eingang festhalten:
- `ARBEITSBAUM_PFADE` (erwartet `shared/paths.py` Z. 225: `("shared", "strategies", LOCK)`);
- `herkunft.register()` (erwartet `c92900a8…`);
- die Sonde gegen `40ffe18d…` (erwartet 25/0/0, (ii) 0);
- `test_startpruefungen` (erwartet 44/44).

---

## Block A — 19 auf den Laufbereich (Register 42.2 E2, 42.3 F8)

**Registertexte, die hier vollzogen werden (Register 19, Kasten „Sauberkeit über den Laufbereich — beschlossen, nicht vollzogen“):**
- **E2:** *„Die Sauberkeitsprüfung des Arbeitsbaums erstreckt sich auf jeden Pfad des Laufbereichs … nicht nur auf `shared/`, `strategies/` und `requirements.lock`; `data/` bleibt ausgenommen … Die Liste der geprüften Pfade steht als Tatsachennotiz neben der Laufbereichsmessung und wird mit ihr am Tag-Commit erneuert.“*
- **F8:** *„Registrierte Protokolle sind von der Sauberkeitsprüfung des Arbeitsbaums ausgenommen wie `data/` … die Ausnahme ist auf die namentlich registrierten Pfade beschränkt, und der Kettenhash ersetzt dort die Sauberkeit.“* Heute genau eines: `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`.

**A1 — Vorher-Probe (belegt den Befund aus E2).** Im frischen Klon am Eingangs-Commit, unter dem Modus: eine uncommittete Änderung (ein Kommentar) in
- `research/vorregistrierung/benchmark.py`,
- `research/faltenplan_neun/faltenplan_neun.py`,
- `notifications/manual_close.py`.

Erwartet: Die Startprüfung hält **nicht** an, rc ≠ 2. Beleg `a1_vorher.txt`. Weicht es ab, **melden**, nicht weiterbauen.

**A2 — Laufbereich neu messen** mit dem Werkzeug aus TB-104 D1 (dieselben drei Lauf-Typen wie TB-107 F1), am Eingangs-Commit.
- Vergleich mit `docs/belege/TB-107/f1_laufbereich_vereinigung.txt` (81 Module).
- Beleg `a2_laufbereich.txt` im selben Format.
- Neue oder weggefallene Module benennen.

**A3 — Bau.** In `shared/paths.py`, nur so weit wie nötig:
- `ARBEITSBAUM_PFADE` deckt **jeden Pfad des Laufbereichs** aus A2 (die Messumschläge unter `docs/belege/` zählen nicht).
  - `shared/` und `strategies/` bleiben als Ordner stehen.
  - Die Module ausserhalb davon (TB-107: 11 unter `research/`, 1 unter `notifications/`) kommen **als einzelne Dateipfade** hinzu, nicht als Ordner. Grund: Ein Ordner wie `research/vorregistrierung/` enthält `ergebnisse/`, in das Läufe schreiben (`--ziel`, Klasse (iii)); die Prüfung darf nicht an der Ausgabe eines früheren Laufs scheitern.
  - Die Wahl im Ergebnis begründen; wer einen besseren Schnitt sieht, **meldet ihn**, statt ihn zu bauen.
- Neue Konstante `REGISTRIERTE_PROTOKOLLE = ("research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl",)`.
  - `git status --porcelain` bekommt sie als `:(exclude)`-Pfadangabe.
  - Das gilt auch, wenn heute kein geprüfter Pfad sie enthält: Die Ausnahme steht **namentlich**, nicht zufällig.
- `data/` bleibt ausgenommen, wie in 19.
- Die Meldung bei Verletzung nennt weiter die geprüften Pfade. Bei vielen reicht die Zahl, dazu ein Verweis auf `paths.ARBEITSBAUM_PFADE`.
- **Ohne Modus ändert sich nichts:** alles im Modus-Zweig. Keine neuen Importe auf Modulebene.

**A4 — Proben** (neue Testdatei, z. B. `shared/test_arbeitsbaum_laufbereich.py`, im frischen Klon, unter dem Modus):

| Probe | erwartet |
|---|---|
| uncommittete Änderung in je einem der 12 Module ausserhalb `shared/`/`strategies/` (alle 12 einzeln) | rc 2, Meldung nennt die Datei |
| `herkunft_protokoll.jsonl` neu angelegt **und** in einem zweiten Fall verändert | rc 0 bzw. kein Abbruch durch die Sauberkeit |
| neue Datei unter `data/` | kein Abbruch (wie 19) |
| neue, nicht versionierte Datei in `research/vorregistrierung/ergebnisse/` (simulierte Ausgabe eines früheren Laufs) | kein Abbruch |
| **Gegenprobe gegen die Messdatei:** jeder Pfad aus A2 ist von `ARBEITSBAUM_PFADE` gedeckt (Präfix oder Datei) | grün |
| Mutation: ein Pfad aus dem Tupel entfernt | die Gegenprobe wird **rot** |
| Mutation: `REGISTRIERTE_PROTOKOLLE` aus der Pfadangabe entfernt und `research/vorregistrierung/ergebnisse/` als Ordner geprüft | die Protokoll-Probe wird **rot** |

Die Gegenprobe liest die Liste **aus der Messdatei**, nicht aus einem Literal (Bauart TB-107 G). Ein Tatsachenkommentar sagt: Am Tag-Commit ersetzt die Tag-Messung die Datei.

**A5 — Abnahme ohne Modus:**
- `test_startpruefungen` grün, darunter **0/0/0 `git`-, Paket- und `os.system`-Aufrufe** (zählende Attrappe) und 144 Pfade zeichengleich;
- `test_paths` grün;
- die 8 Ausgaben aus `docs/belege/TB-109/g2_ausgaben.sh` bytegleich gegen den Eingangs-Commit.

**A6 — Abnahme mit Modus** (nach dem Commit von A3/A4; der Modus verlangt den sauberen Baum):
- Benchmark im Modus, Repo **und** frischer Klon, `64fb2912…`;
- Trockenlauf aller neun: rc 0;
- Sonde vorher = nachher;
- `register()` unverändert;
- **Lese-Audit** (Werkzeug `docs/belege/TB-109/d_auswerten.py`): Zahl der Lesezugriffe unter der Codewurzel **ausserhalb** von `ARBEITSBAUM_PFADE` (Klasse „Code“ ungebunden nach E2). Erwartet 0. Jede Fundstelle ist ein Befund, **melden**, nicht beheben.

**A7 — Tatsachennotiz:** `docs/belege/TB-112/arbeitsbaum_pfade.txt`, die Liste der geprüften Pfade neben `a2_laufbereich.txt`. Das ist die „Tatsachennotiz neben der Laufbereichsmessung“ aus E2. Der Registereintrag folgt in Register 44, nicht hier.

## Block B — db-Sicherung (Fable 25f O6), als Skript

**Zweck:** Die neun `paper_trading_*.db` (dazu die übrigen `*.db` im Repo-Wurzelordner, heute zwölf) existieren nur auf diesem MacBook und sind die einzige Evidenz aus dem Paper-Betrieb (Prüfprinzip D6).

- **B1 — Skript** `docs/werkzeuge/db_sicherung/db_sicherung.sh` (bash, eine Aufgabe):
  - findet die `*.db` im Repo-Wurzelordner und unter `strategies/*/` (heute gemessen: 12 im Wurzelordner, 1 unter `strategies/volatility_breakout/`) und nennt sie im Protokoll;
  - sichert jede mit `sqlite3 <db> ".backup '<ziel>'"`. Das ist lesend und sicher, auch wenn gerade ein Cron schreibt; **kein `cp`**;
  - prüft jede Kopie mit `PRAGMA integrity_check` (erwartet `ok`) und schreibt `sha256` der Kopie in `SHA256SUMS` im Zielordner;
  - Ziel: `~/Library/Mobile Documents/com~apple~CloudDocs/trading-bot-db-sicherung/<JJJJ-MM-TT>/`, als erstes Argument überschreibbar (für Tests);
  - **löscht nie etwas.** Aufbewahrung ist eine offene Frage an den Betreiber; das Ergebnis nennt die Grösse eines Satzes;
  - Rückgabe 0 nur, wenn alle Kopien `ok` sind. Sonst 1, und die Meldung nennt die Datei.
- **B2 — Schlüssel-Prüfung (Fable: „Sicherung enthält keine Schlüssel — prüfen“).** Je Datenbank nur das **Schema** lesen: Tabellen- und Spaltennamen. Zählen, wie viele Spaltennamen wie `key`, `secret`, `token`, `api`, `password` aussehen. ⛔ **Nie einen Wert ausgeben**, nur Namen und Zahlen. Findet sich etwas: Befund, melden. Das Skript sichert diese Datei dann **nicht**, bis der Betreiber entscheidet.
- **B3 — Test mit Testziel** (`$TMPDIR`-Ordner, danach entfernt): zwei Läufe hintereinander; je Datei `integrity_check ok`; `SHA256SUMS` vollständig; Laufzeit. Die Original-`*.db`: `sha256` vorher = nachher, soweit kein Cron dazwischen schrieb; sonst mtime und Cron-Zeit nennen (wie TB-109: Brücke um :05).
- **B4 — Ein Lauf ins echte iCloud-Ziel.** Scheitert er an macOS-Berechtigungen (`Operation not permitted`): **nicht umgehen**, genau so melden. Der Betreiber muss dann Cron oder Terminal „Festplattenvollzugriff“ geben; das steht im LIESMICH.
- **B5 — `LIESMICH.md`** daneben:
  - Zweck;
  - die **eine Cron-Zeile**, die der Betreiber selbst einträgt (Vorschlag täglich 05:20 lokal; die bestehenden Crons liegen um 3:50, 4:10, 4:40 und alle 4 h zur Minute 5);
  - wie man eine Sicherung zurückspielt (nur beschreiben, nicht ausführen);
  - der Hinweis auf „Festplattenvollzugriff“.

## Block C — `tb40_test_*` (Randbefund TB-109)

`test_universum_trockenlauf.py` legt je Lauf 18 Ordner `tb40_test_*` an (Z. 123, 136, 192) und entfernt sie nicht. Umbau: `addCleanup(shutil.rmtree, …)` oder `finally`. Z. 902 `tb44_l_` gleich prüfen. **Abnahme:** `$TMPDIR` vor und nach einem Testlauf gleich; der Test selbst gleich grün, gleiche Probenzahl.

## Block D — Abgabe

**Commits:**
1. A3 und A4 (Code und Tests);
2. B;
3. C;
4. Belege, Ergebnis `docs/ERGEBNIS_TB-112_19_laufbereich_db_sicherung.md` (mit „Für Fable“ und „In einfacher Sprache“) und Journalblock.

Nach jedem Commit `git push origin main`.

## ⚠️ Abbruchkriterien — melden, nicht reparieren

- A1 zeigt, dass die Startprüfung die drei Dateien **heute schon** aufhält (dann beschreibt E2 den Stand nicht mehr).
- A2 findet ein Laufbereichsmodul, das weder unter `shared/`/`strategies/` noch als Datei aufnehmbar ist (z. B. ausserhalb des Repos).
- Ohne Modus ändert sich eine Zahl, ein Pfad oder die Zahl der `git`-Aufrufe.
- Benchmark ≠ `64fb2912…` oder Sonde (ii) ≠ 0.
- B2 findet Schlüsselspalten. Dann B ohne diese Datei abschliessen und melden.

## In einfacher Sprache

Vor dem grossen Lauf prüft das Programm, ob sein Code unverändert und eingecheckt ist, bisher aber nur in zwei Ordnern. Elf Programme aus dem Forschungsordner und eines aus den Benachrichtigungen wurden nicht geprüft. Dieser Auftrag schliesst die Lücke; die eine Protokolldatei, die während des Laufs wachsen muss, bleibt ausdrücklich ausgenommen. Dazu kommt ein kleines Sicherungsskript, das die Paper-Trading-Datenbanken täglich nach iCloud kopiert, denn heute gibt es sie nur auf diesem Laptop. Und ein Test räumt künftig seine Zwischenordner selbst auf.
