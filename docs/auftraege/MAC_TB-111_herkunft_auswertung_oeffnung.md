# TB-111 — Die gesperrte Öffnung aus Fable 25d: `herkunft.py` (Prüfansicht, `TB30A_BASE_DIR` unter dem Modus) und `auswertung.py` (`Abbruch` ⇒ 2); neues Abbild — **im eigenen Worktree, parallel zu TB-109**

**Sitzungstitel:** `TB-111` · **Angelegt:** 25.09.2026, 23:30, vom steuernden Chat
**Grundlage:** Fable 25d 2 (2), (3) und (4) mit dem Registertext „Ergänzung zu 36.5 — Ausgänge von `auswertung.py`“; Fable 25c 2 (a) („planmässig geöffnet heisst nicht offen“); Register 37.3.
**Aufwand:** hoch (ARBEITSWEISE 22.1)

> **In einfacher Sprache, vorweg:** Zwei gesperrte Programme werden für je zwei kleine, genau beschriebene Änderungen geöffnet. Das Herkunftsprogramm soll im geschützten Modus seine Prüfansicht zeigen können und eine alte Test-Abkürzung verweigern. Die Auswertung soll „konnte nicht rechnen“ mit dem Wert 2 statt 1 melden. Danach wird ein neues Schutzabbild gezogen. Diese Sitzung läuft **gleichzeitig** mit TB-109, aber in einer eigenen Kopie des Repos auf einem eigenen Zweig.

---

## ⭐⭐ Freigabe des Betreibers, wörtlich

**25.09.2026, 23:14, zwei Auswahlkarten im steuernden Chat:**

| Frage | Antwort |
|---|---|
| *„Parallel geht sicher nur mit zwei Sitzungen: eine im Repo, eine in einem eigenen Git-Arbeitsbaum (worktree, eigener Zweig). … Wie viele Sitzungen sollen über Nacht laufen?“* | **„Zwei parallel (Empfohlen)“**: Sitzung A im Repo, TB-109 und danach TB-110. Sitzung B im Worktree `trading-bot-tb111`: TB-111, die eine gesperrte Öffnung aus Fable 25d, `herkunft.py` (Prüfansicht, `TB30A_BASE_DIR` unter dem Modus rc 2) und `auswertung.py` (`Abbruch` rc 2 statt 1), dazu ein neues Abbild. Die Dateien überschneiden sich nicht; der Zweig wird später zusammengeführt |
| *„Nur für Sitzung B: Gibst du die gesperrten Dateien herkunft.py (Punkte 11/12) und auswertung.py (Punkte 3/5/14) für genau diese Änderungen frei, samt neuem Abbild?“* | **„Ja, freigeben (Empfohlen)“**: `herkunft.py`: Prüfansicht übergibt unter dem Modus `paths.DATA_DIR`, `TB30A_BASE_DIR` unter dem Modus rc 2 vor dem Lesen. `auswertung.py`: die Klasse `Abbruch` endet mit 2 statt 1. Sonst nichts. Danach ein neues Abbild |

| freigegeben | Pfad | Sperrliste | was |
|---|---|---|---|
| ✔ | `research/vorregistrierung/herkunft.py` | 11/12 | Block B, **nur** Prüfansicht und `TB30A_BASE_DIR` |
| ✔ | `research/vorregistrierung/auswertung.py` | 3/5/14, `EINGEFROREN` | Block C, **nur** der Rückgabewert von `Abbruch` |
| ✔ | die Tests dieser Module (`test_vorregistrierung.py`, `test_ersatzwerte.py`), neue Proben im selben Ordner | — | — |
| ✔ | **ein** neues Abbild unter neuem Namen (`sperrliste_abbild.py --ziel`) | 36.6 | Block D |

⛔ **Nicht freigegeben:** jede andere Datei. Vor allem nicht die Dateien von TB-109 (`strategies/*/equity_simulation.py`, `universum_trockenlauf.py`, `pfadvergleich.py`, `shared/test_main_gegenprobe.py`), nicht das Register, **nicht `docs/auftraege/AKTUELLER_AUFTRAG.md` und nicht `docs/projektfuehrung/JOURNAL.md`** (siehe Worktree-Regeln).

---

## ⚠️⚠️ Worktree-Regeln — diese Sitzung läuft nicht im Repo, sondern daneben

| | |
|---|---|
| Ordner | **`~/trading-bot-tb111`**, ein `git worktree` des Repos, Zweig **`tb-111`**, angelegt von TB-109 in Schritt 0c auf dem Schritt-0-Commit von TB-109. Prüfe als Erstes: `git --no-optional-locks rev-parse --abbrev-ref HEAD` = `tb-111`, und `pwd` endet auf `trading-bot-tb111`. **Stimmt eines nicht: abbrechen, melden** |
| Python | Die Umgebung liegt nur im Hauptordner: **`~/trading-bot/trading-env/bin/python3`**. Alle Läufe damit, aus dem Worktree heraus |
| Snapshot | `snapshots/63e4b6c8…/` ist versioniert und liegt im Worktree. Modus-Läufe mit `TB_SELEKTIONSWURZEL` auf **den Snapshot im Worktree** |
| Commits | nur auf `tb-111`; `git push -u origin tb-111`. ⛔ **Kein Merge nach `main`, kein Push auf `main`, kein Rebase.** Das Zusammenführen ist ein eigener Auftrag |
| Journal | ⛔ **`docs/projektfuehrung/JOURNAL.md` nicht anfassen**, sonst gibt es beim Zusammenführen einen Konflikt mit TB-109/TB-110. Der Journalblock steht **am Ende des Ergebnisdokuments** und wird beim Zusammenführen übertragen |
| Zeiger | `AKTUELLER_AUFTRAG.md` nicht anfassen |
| Sitzungswächter | Der Wächter kennt nur den Hauptordner. Diese Sitzung wird nicht vom Wächter geschlossen; nach der Abgabe einfach stehen lassen |
| Cron | Die nächtlichen Cron-Läufe (3:50, 4:10, 4:40) laufen im **Hauptordner**, nicht hier. Nichts im Hauptordner ändern |

---

## 0. Schritt 0

- **0a:** Worktree-Prüfung wie oben. `git --no-optional-locks log -1 --format=%H` notieren (= Schritt-0-Commit von TB-109). Der Arbeitsbaum ist leer (`git --no-optional-locks status --porcelain`); ist er es nicht, abbrechen.
- **0b:** Hashes vorher von `herkunft.py` (erwartet `351f24c2…`), `auswertung.py` (erwartet `83c6bc3c…`) und allen Sperrlistendateien. `herkunft.register()` vorher (erwartet `c85dd6c3…`, nach TB-108). Sonde gegen `sperrliste_abbild_2026-09-25b.json` (`40ffe18d…`): erwartet 25/0/0, (ii) 0.

## Block A — Vormessung

| | zu messen |
|---|---|
| A1 | `herkunft.py main()`: Welcher Zweig ruft `block("pruefung")` ohne `daten_dir` (Prüfansicht, `--json`, `--pruefen`)? Seit TB-106 endet er unter dem Modus mit 2 (Ergebnis TB-106 Abschnitt 5) |
| A2 | `herkunft.py:51` `BASE_DIR = os.environ.get("TB30A_BASE_DIR") or …`: Wer setzt die Variable? Laut TB-106 A11 nur Tests. **Setzt ein Test sie zusammen mit den Modus-Variablen?** Dann bricht er nach Block B mit 2 ab: melden, Test anpassen (freigegeben) |
| A3 | `auswertung.Abbruch`: die 12 Stellen `raise Abbruch(…)` (TB-106: 12, nicht 13). Welche Tests prüfen den Rückgabewert 1 von `auswertung.py` oder fangen `Abbruch` mit einem erwarteten Code? (`grep` in `test_vorregistrierung.py`, `test_ersatzwerte.py`, `beispieldaten.py`) |
| A4 | Ist `herkunft.py` beim Import unter dem Modus heute ohne `TB30A_BASE_DIR` unverändert lauffähig (`etf_trendfolge/datenstand.py`, `shared/snapshot.py` importieren es)? |

## Block B — `herkunft.py`

- **B1 — Prüfansicht:** Wo `main()` `block(...)` ohne `daten_dir` ruft (A1), übergibt es **unter dem Modus** `paths.DATA_DIR`, genau wie `--anhaengen` seit TB-106 (E2). Ohne Modus unverändert (`None`, Voreinstellung).
- **B2 — `TB30A_BASE_DIR`:** Unter dem Modus bricht `herkunft.py` mit rc 2 ab, **bevor** `BASE_DIR`, `REGISTERDATEI` oder `commit()` die Variable benutzen (24d Abschnitt 3: erst 2, dann lesen). Die Meldung nennt die Variable. Ohne Modus unverändert; die Tests setzen sie weiter.
  - Bauart: `paths` wird **erst bei Bedarf** geladen wie seit TB-106 (`_paths()`), damit der Import von `herkunft.py` unverändert bleibt (A4).
  - Die Prüfung sitzt daher dort, wo `BASE_DIR` zum ersten Mal **benutzt** wird, oder in einer kleinen Funktion, die `commit()`/`register()`/`block()` vor dem Lesen rufen. Die Wahl im Ergebnis begründen.
- **B3 — sonst nichts:** `EINGEFROREN`, `register()`, `datenstand()`, `kette_pruefen()`, `anhaengen()` bleiben zeichengleich, bis auf die Durchleitung aus B1.
- **B4 — Proben** (Wegwerfbaum, echtes Protokoll unberührt; Bauart `test_ersatzwerte.py` E):
  - Prüfansicht im Modus ⇒ rc 0, `datenstand` = `d9449faf…`;
  - Modus + `TB30A_BASE_DIR` ⇒ rc 2, kein Lesezugriff unter der Ersatzwurzel (Lesehaken);
  - ohne Modus + `TB30A_BASE_DIR` ⇒ wie vorher;
  - Mutationsproben „Prüfansicht ohne Pfad“ und „Prüfung von `TB30A_BASE_DIR` weg“, je allein, mit Gegenprobe.

## Block C — `auswertung.py`

- **C1:** Die Klasse `Abbruch` endet mit **Rückgabewert 2** (`paths.RUECKGABEWERT_STARTPRUEFUNG`), die Meldung weiter auf stderr, **wortgleich**. Die 12 `raise Abbruch(…)`-Stellen bleiben zeichengleich. Bauart zum Beispiel: `__init__`, das die Meldung nach stderr schreibt und `code = 2` setzt. Im Ergebnis zeigen, dass die Meldung vorher und nachher gleich ausgegeben wird.
- **C2:** Kommentar an der Klasse: „Ausgänge von `auswertung.py`: 0 oder 2, kein 1 (Fable 25d (4), Ergänzung zu 36.5)“.
- **C3 — Proben:**
  - `auswertung.py --rohergebnisse <leer>` ⇒ rc 2 (vorher 1);
  - je eine Probe für drei der zwölf Stellen (fehlende Spalte, Zelle ausserhalb des Rasters, zu wenige gemeinsame Tage) ⇒ rc 2;
  - Mutation „Code 1 zurück“ ⇒ rot, mit Gegenprobe.

  Tests, die heute rc 1 erwarten (A3), auf 2 umstellen und im Ergebnis nennen.
- **C4 — Abnahme:** Auswertung auf den Beispieldaten aller neun Bots zeichengleich **`fc178106…`** (Bauart TB-106 G3).

## Block D — Abbild und Sonde

- **D1:** Nach dem letzten Code-Commit: `sperrliste_abbild.py --ziel research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26.json` (Name frei, wenn belegt), eigener Commit.
- **D2:** Sonde gegen das alte `40ffe18d…`: erwartet Befund genau an **3, 5, 11, 12, 14** und in der Gruppe `eingefroren`. **Jeder andere Punkt ⇒ melden.** Gegen das neue: 25/0/0, (ii) 0.
- **D3:** `herkunft.register()` vorher/nachher (ändert sich, weil `auswertung.py` in `EINGEFROREN` steht); Hash-Übergänge von `herkunft.py` und `auswertung.py`, alt und neu **voll**.

## Block E — Abnahme

| | Soll |
|---|---|
| E1 | `benchmark.py --ziel <scratch>` **im Modus** aus dem Worktree: bytegleich **`64fb2912…`** |
| E2 | Ohne Modus: die 8 Ausgaben (`docs/belege/TB-106/g2_ausgaben.sh`) bytegleich gegen den Eingangsstand |
| E3 | Trockenlauf aller neun im Modus: 9 × rc 0 |
| E4 | Tests: `test_vorregistrierung` 196/196 (oder mit neuen Proben, Zahl nennen), `test_ersatzwerte` (Zahl), `test_paths` 35/35, `test_startpruefungen` 44/44, neue Proben mit Namen |
| E5 | Hashes: geändert nur `herkunft.py`, `auswertung.py`, ihre Tests, das neue Abbild und `docs/`. Datenstand, Snapshot und `*.db` gleich. Das echte `herkunft_protokoll.jsonl` existiert nicht und wird nicht angelegt |

⛔ Sichtschutz 27.1 wie immer.

## Block F — Abgabe

- Ergebnis `docs/ERGEBNIS_TB-111_herkunft_auswertung_oeffnung.md`. Darin „Für Fable“, „Für die Zusammenführung“ und „In einfacher Sprache“. **Am Ende der Journalblock**, nicht in `JOURNAL.md`.
  - „Für Fable“: A2, A3; die Wahl in B2; C1 Meldung gleich; Hash-Übergänge; Abbild; Sonde.
  - „Für die Zusammenführung“: welche Dateien auf `tb-111` geändert sind; erwartete Konflikte mit `main` (keine, ausser wenn TB-109/TB-110 eine der Dateien berührt haben); der Journalblock zum Übertragen.
- **Commits auf `tb-111`:** (1) Block B · (2) Block C · (3) Abbild · (4) Belege und Ergebnis. Nach jedem `git push origin tb-111`.

## ⚠️ Abbruchkriterien

1. Der Worktree ist nicht `tb-111` oder nicht sauber (0a).
2. Die Benchmark-Tabelle ist nicht bytegleich.
3. Die Sonde meldet einen Punkt ausserhalb 3/5/11/12/14 ⇒ kein neues Abbild, melden.
4. Eine Änderung bräuchte eine nicht freigegebene Datei ⇒ melden.
5. Ein Test schreibt das echte `herkunft_protokoll.jsonl` ⇒ sofort anhalten.

---

## In einfacher Sprache

Diese Sitzung arbeitet in einer Kopie des Projekts neben dem Hauptordner, damit sie der gleichzeitig laufenden Sitzung nicht in die Quere kommt. Sie ändert genau zwei gesperrte Programme, jedes an genau den Stellen, die der Prüfer benannt hat:
- **Das Herkunftsprogramm** kann seine Prüfansicht auch im geschützten Modus zeigen und verweigert dort eine alte Abkürzung aus den Tests.
- **Die Auswertung** meldet „konnte nicht rechnen“ künftig mit dem Wert 2.

Danach wird das Schutzabbild neu gezogen. Die Vergleichstabelle muss Byte für Byte gleich bleiben. Zusammengeführt wird später in einem eigenen Schritt.
