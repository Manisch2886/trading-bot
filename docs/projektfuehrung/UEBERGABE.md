# UEBERGABE 2026-09-25 — Stand des steuernden Chats

> ⭐ **Fortgeschriebene Übergabe (UMZUG 1). Vorgängerfassungen: UEBERGABE_2026-09-19/24/25.md (Repo).** *Angelegt TB-118 (27.09.2026, Fable 27b B2/G2) als Kopie von `UEBERGABE_2026-09-25.md` (Stand 25.09.2026, 08:15); ab hier wird diese Datei fortgeschrieben, die datierten bleiben unverändert im Repo.*

**Fortgeschrieben am 25.09.2026, 08:15 Ortszeit, an einem sauberen Stand.** Es läuft keine Mac-Sitzung: TB-103 wurde am 25.09. um 00:52 per Schliess-Auslöser beendet, danach waren „0 noch da“. Der Arbeitsbaum ist committet bis auf die Dateien des steuernden Chats in Block 8. Alles gemessen.

⭐ **Dieser Chat ist der steuernde seit 24.09.2026, 22:40.** Er hat vom Chat vom 21.09. übernommen, der zweimal komprimiert worden war. Der Umzug ist gemessen abgeschlossen: Nach 22:47 hat der alte Chat nichts mehr abgelegt. Fable ist ebenfalls umgezogen und hat im neuen Chat 24d und 25a geantwortet.

⚠️ **Ersetzt `UEBERGABE_2026-09-24.md`.** Die alte Fassung bleibt als Stand vom 24.09., 22:40. Jede Aussage hier sagt, ob sie **gemessen** oder **erschlossen** ist (UMZUG Abschnitt 5, Nr. 7).

---

## Block 1 — Der Stand in drei Zeilen

| | |
|---|---|
| **Fertig** | **Tagblocker weg (TB-103):** Resolver-Fix, `messgroessen.py` auf dem Resolver, alle neun Bots im Modus mit rc 0, aus dem Snapshot, 0 Standardlisten · Fable 24d und 25a liegen vor · Registerkopie in drei Teilen, Fable hat das Register ganz gelesen |
| **Läuft** | ⭐ **TB-104** wird mit diesem Stand ausgelöst: alle Leser des Laufbereichs auf den Resolver, Verfahren-A-Felder aus `faltenplan.py`, Laufbereich messen |
| **Als Nächstes** | Nach TB-104: Auswahlkarte für **TB-105** (die vier Rückfälle, Live-Code) · **Register 41/42** (24b, 24c, 24d, 25a) · dann Plan-Punkt 3, der **Erzeuger auf dem Signalpfad** |

---

## Block 2 — `HEAD` und die Commit-Kette

**Gemessen am 25.09.2026, 08:05.** Zweig `main`, **`HEAD 836865f500773edb37994e1f411dbeef99546103`**.

| Zeit | Commit | |
|---|---|---|
| 24.09., 23:32 | `1d2b836` | TB-103 Schritt 0 (Übergabe 24.09., Fable 24b/24c, Anfrage 24e, Registerkopie) |
| 25.09., 00:09 | `d87997e` | TB-103 Block B: Resolver-Fix `shared/paths.py` |
| 25.09., 00:25 | `ae136fd` | TB-103 Block C: `messgroessen.py` auf dem Resolver |
| 25.09., 00:30 | `836865f` | TB-103 Abgabe: Trockenlauf 9/9, Ergebnisdokument |

---

## Block 3 — Die tragenden Zahlen

| Sache | Wert | Fundstelle | |
|---|---|---|---|
| Register | Abschnitte **0–40**, 7993 Zeilen, unverändert seit `d0dc890` | `docs/VORREGISTRIERUNG_neuselektion.md` | gemessen (TB-103 0b) |
| Snapshot | `63e4b6c8…`, `datenstand_hash d9449faf51bffaaa` | `snapshots/` | gemessen |
| Tests | `test_vorregistrierung` **191/191** · `test_paths` **35/35** · `test_startpruefungen` 44/44 · `test_strategy_paths` 23/23 · `test_stille_ausfaelle` 27/27 | TB-103 `b4_tests.txt`, `c4_tests.txt` | gemessen |
| Benchmark-Tabelle | `benchmark_drawdowns_2026-09-23_nach_wegA.json` **`64fb2912…`** | Sperrlistenpunkt 4 | gemessen |
| Abbild | `sperrliste_abbild_2026-09-23.json` `2f23f76c…`; TB-104 zieht ein neues | 39.9 | gemessen |
| `messgroessen.json`-Nachweis | im Modus bytegleich, **Status 2**: `haltedauern_je_bot.csv` kommt aus dem Repo | TB-103 C3 | gemessen |
| Benchmark-Nachweis | **Status 2** aus eigenem Protokoll (39.8): neun Listen und `messgroessen.json` aus dem Repo | TB-92 `a1b_lesequellen_kinder.txt` | gemessen |
| Freie TB-Nummer | **TB-105** (TB-104 vergeben; TB-99 ist die Wächtersonde) | `AKTUELLER_AUFTRAG.md` | gemessen |
| Fable-Buchstabe | Anfragen: 25a vergeben, nächste **25b**. Antworten: 25a vergeben, nächste **25b** | Ablage | gemessen |

---

## Block 4 — Offene Punkte vor dem signierten Tag, in Reihenfolge

⭐ Die Reihenfolge stammt von Fable (24c Abschnitt 6, präzisiert in 24d Abschnitt 4 und 25a).

| | Punkt | Stand |
|---|---|---|
| 1 | Resolver | ✅ TB-103 |
| **2** | **Alle Leser des Laufbereichs auf den Resolver** (`benchmark.py`, `faltenplan_neun.py`, `universum_trockenlauf.py`/`loaderlauf.py`, ggf. `erste_falte_trockenlauf.py`) · **Verfahren-A-Felder aus `faltenplan.py`** (25a (1)) · Laufbereich messen (25a Abschnitt 4) | ⭐ **TB-104** |
| **2b** | **Die vier Rückfälle** (25a Abschnitt 4, alle vor den Tag): (b) BTC-Regimefilter `t3_supertrend` (**Register 11.1, seit 14.09. offen**) · (c) `exit()` mit rc 0 · (d) Ersatzwerte für Schwellen · (a) `EXCLUDE`-leere Liste. Dazu: Ladeprotokoll Teil (4) (Quelle und Zeilenzahl), Schreibziel `manuelle_eingriffe.log` | **TB-105**, Freigabekarte nach TB-104 Block D |
| 3 | Erzeuger auf dem Signalpfad (24b A3; Felder `entry_time`, `exit_time`, `haltedauer_balken`) | offen |
| 4 | Register 41/42 | offen, Stoff siehe Block 7 |
| 5 | Faltenlänge gegen 33.2 · `messgroessen.json` neu · Raster nachziehen · Benchmark-Tabelle neu mit beiden Nachweisteilen · `t3_supertrend`-Deckel aus gefundenen Trades · Abbild des Faltenplans · **Trockenlauf aller neun am Tag-Commit wiederholen** (25a) | offen |

---

## Block 5 — Wartezustände

| wartet | auf | seit |
|---|---|---|
| **Betreiber** | den Einfügesatz TB-104 abschicken, sobald der Wächter ihn ins Fenster gelegt hat | 25.09., ~08:20 |
| **steuernder Chat** | das Ergebnis von TB-104, Nachschau per `send_later` | 25.09., ~08:20 |
| **Fable** | nichts. 25a ist beantwortet; die nächste Anfrage kommt mit dem Ergebnis von TB-104 | — |

---

## Block 6 — Freigaben und Sperrliste

| Freigabe | erteilt | Stand |
|---|---|---|
| `shared/paths.py`, `messgroessen.py` und ihre Tests | 24.09., 22:52 | ✅ verbraucht (TB-103) |
| `shared/test_strategy_paths.py` | 24.09., 23:49, in der Sitzung | ✅ verbraucht (TB-103) |
| `faltenplan.py` (Punkt 2) und ein neues Abbild | 24.09., 11:25 | ⭐ **wird in TB-104 verbraucht** |
| **TB-104:** `benchmark.py` (Punkte 4/6), `faltenplan.py`, `faltenplan_neun.py`, `erste_falte_trockenlauf.py`, `universum_trockenlauf.py`, `loaderlauf.py`, deren Tests und `test_vorregistrierung.py` | **25.09., 07:52** | erteilt, unverbraucht |
| `registerbericht.py` (Anzeige von `purge_tage`) | — | ⚠️ **nicht erteilt**; TB-104 fragt per Auswahlkarte |
| **TB-105** (die vier Rückfälle, Live-Code) | — | Betreiber 07:52: **„Erst messen, dann fragen“** ⇒ Auswahlkarte mit genauer Dateiliste nach TB-104 Block D |

**Sperrliste:** 14 Punkte. Punkt 4 ist vollzogen (39). Punkte 2, 4 und 6 bewegen sich in TB-104 planmässig nach 37.3. `herkunft.py` (Punkte 11/12) bleibt zu: `datenstand()` nimmt das Verzeichnis als Argument (gemessen, 25.09.), damit gilt Fable 25a Fall „Argument“. ⚠️ Aber `block()` ruft `datenstand()` **ohne** Argument; der Erzeuger darf `block()` deshalb nicht benutzen.

---

## Block 7 — Die Fehler dieses Chats und die Regeln daraus

| | Fehler | Regel daraus |
|---|---|---|
| 1 | **„Lesehaken erst seit TB-95“** in Block 5 der alten Übergabe und an Fable weitergegeben. Richtig ist: seit TB-92, das Register hatte recht (39.6/39.8). Ursache: Fables Nummer „TB-91“ übernommen und nur dort gesucht | ⭐ **Eine übernommene Auftragsnummer ist eine Voraussetzung.** Vor dem Suchen in `docs/belege/TB-<n>/` die Nummer gegen das Register prüfen (`grep -n "TB-<n>" VORREGISTRIERUNG…`) |
| 2 | **„Übergabe fortschreiben“** so formuliert, dass der Betreiber einen weiteren Umzug las | Fortschreiben der Übergabe ist **Pflege** (UMZUG Abschnitt 1), kein Umzug. So benennen |
| 3 | Der Betreiber meldete „TB-103 fertig“, als erst Schritt 0 committet war. Ich habe zuerst gemessen und nicht geglaubt; richtig so | ⭐ **„Fertig“ heisst: Abgabe-Commit liegt vor.** Vorher Sonde, Commits, Änderungszeiten im Arbeitsbaum; bei Stillstand nach einer Rückfrage im Fenster fragen |
| 4 | In den eigenen Anfragen stand eine Trade-Zahl (Wert nach 27.5 hier nicht wiederholt), die aus der Vorlage stammte | Jede Anfrage an Fable vor dem Übergeben gegen 27.1 lesen, auch übernommene Blöcke |

**Die Rügen und Regeln aus UEBERGABE_2026-09-24 Block 8 gelten weiter.** Vor allem: `md5sum` und `wc -c` auf beiden Seiten nach jedem Ablegen · eine Fable-Anfrage ist erst übergeben, wenn sie als Kopierblock in der Antwort stand · nach jedem Auslöser eine Nachschau planen · kein `git status`.

---

## Block 8 — Was zwischengelagert und noch nicht committet ist

| Datei | Zielort | Stand |
|---|---|---|
| `FABLE_ANFRAGE_2026-09-25a_tagblocker_weg_zwei_lesarten.md` | `docs/projektfuehrung/` | abgelegt, uncommittet |
| `FABLE_ANTWORT_2026-09-24d_deckel_statt_purge_ein_weg.md`, `FABLE_ANTWORT_2026-09-25a_umgebung_liste_laufbereich.md` | `docs/projektfuehrung/` | ⚠️ aus der Projektablage **abgeschrieben**, nicht bytegeprüft gegen die Ablage (das Werkzeug liefert dort nur Text); uncommittet |
| `UEBERGABE_2026-09-25.md` (dieses Dokument), `UMZUG.md` (Zeiger) | `docs/projektfuehrung/` | uncommittet |
| `MAC_TB-104_…`, `AKTUELLER_AUFTRAG.md` | `docs/auftraege/` | uncommittet |

Alles davon nimmt **TB-104 Schritt 0** mit.

---

## Block 9 — Der Eröffnungstext

Die einzige Fassung steht in `UMZUG.md` Abschnitt 6. Zeile Nr. 1 zeigt ab jetzt auf `projektfuehrung/UEBERGABE_2026-09-25.md`.

---

## ⚠️ Die stehenden Sicherheitsregeln gelten unverändert

Siehe `UEBERGABE_2026-09-24.md`, Abschnitt „Stehende Sicherheitsregeln“: kein Befehl, dessen Ausgabe einen Schlüssel enthalten könnte · kein `git status`/`add`/Commit über die Anbindung · nichts nach `docs/` schreiben, solange eine Sitzung läuft (vorher die Sonde `starte_TB-99`) · nie überschreiben, immer neuer Dateiname · Sichtschutz 27.1 · jede Entscheidung als Auswahlkarte.

---

## In einfacher Sprache

Der grösste Fehler der letzten Tage ist behoben: Im geschützten Modus lesen alle neun Bots jetzt die richtigen Listen aus dem eingefrorenen Bestand. Der Verfahrensprüfer hat alle Messungen angenommen und drei Präzisierungen gesetzt: welche Dateizugriffe erlaubt sind, wogegen die geladenen Werte geprüft werden, und welche Programme überhaupt zum geschützten Lauf gehören.

Als Nächstes werden die übrigen Programme auf die zentrale Pfadstelle umgestellt, und alte Werte aus einem abgeschafften Verfahren kommen aus dem Zeitplan. Danach folgen die vier restlichen Notlösungen im Code. Dafür wird gesondert gefragt, weil sie auch den laufenden Betrieb betreffen.


---

## Nachtrag 1 — fortgeschrieben 25.09.2026, 11:15, sauberer Stand

**Gemessen.** TB-104 ist abgegeben (`516badc`, 10:32) und um 10:53 per Schliess-Auslöser beendet („0 noch da“). HEAD `516badc`. Arbeitsbaum sauber bis auf die Dateien dieses Nachtrags.

| | |
|---|---|
| **Fertig (TB-104)** | Leser auf dem Resolver (`benchmark.py`, `faltenplan_neun.py`, `loaderlauf.py`); Ersatzwurzeln brechen unter dem Modus mit 2 ab · drei Verfahren-A-Felder aus dem gerechneten Plan (9 + 9 + 77 Vorkommen, sonst zeichengleich) · Benchmark-Tabelle im Modus zweimal bytegleich `64fb2912…` · **neues Abbild `sperrliste_abbild_2026-09-25.json`, `cb4eb1b4…`** · Laufbereich gemessen: 80 Module aus drei Lauf-Typen · Tests `test_vorregistrierung` 196/196, `test_faltenplan_neun` 156/156, `test_universum_trockenlauf` 163/163 |
| **Hash-Übergänge (37.3)** | `faltenplan.py` `7aa0b8cc…` → `d57fe9c9…` (Punkt 2) · `benchmark.py` (Punkte 4/6), Hashes in `docs/belege/TB-104/e2_hashes.txt` · `registerbericht.py` `dace1b01…` → `de35a5a0…` (auf keinem Punkt) |
| **Freigaben verbraucht** | TB-104 (07:52) · `faltenplan.py` und Abbild vom 24.09., 11:25 · `registerbericht.py` (09:10, in der Sitzung) |
| **Neu freigegeben, 10:52** | **TB-105**: (b) Regimewache an 3 Stellen, (c) 14 × `exit()` unter dem Modus ⇒ 2, (a) `symbols_config.py`, `manual_close.py` (Log erst bei der ersten Zeile), `strategy_paths.py` und `bot_lauf.py` (keine Ordner unter dem Modus) · **TB-106** (d) als eigener Auftrag danach, Freigabe dort mit Sperrliste zu erfragen |
| **Läuft** | **TB-105**, wird mit diesem Stand ausgelöst |
| **Wartet** | **Fable** auf Anfrage **25b** (fünf Fragen: `$TMPDIR`-Ablagen, Quelltext als Daten, Feldliste `G8` gegen 33.3, weitere Verfahren-A-Reste, `messgroessen.py` im Laufbereich). Wird als Kopierblock übergeben |
| **Freie Nummern** | TB-106 vergeben (geplant), frei ab **TB-107** · Fable-Anfrage frei ab **25c**, Antwort frei ab **25b** |
| **Am Rand** | ⚠️ **Speicher-Export bis 29.09.2026** (nur der Betreiber, `projektfuehrung/ERINNERUNG_2026-09-25_speicher_export.md`) · vier Nachträge in den Projektspeicher (`PRUEFUNG_2026-09-25_drei_festlegungen_im_speicher.md`) |

**Fehler dieses Abschnitts, mit Regel:** Der Name der Anfrage 25b hiess zuerst „sechs_fragen“, der Text zählt fünf. Vor dem Ablegen umbenannt. ⇒ **Dateiname und Inhalt vor dem Ablegen gegeneinander lesen.**


---

## Nachtrag 2 — fortgeschrieben 25.09.2026, 22:40, sauberer Stand

**Gemessen.** TB-105, TB-106 und TB-107 sind abgegeben und per Schliess-Auslöser beendet. **HEAD `f61bd97`** (TB-107 Abgabe, 22:14). Es läuft keine Mac-Sitzung. Uncommittet sind nur, alle unter `docs/projektfuehrung/`: `FABLE_ANFRAGE_2026-09-25e_tb107_abgegeben_drei_fragen.md`, `FABLE_ANFRAGE_2026-09-25f_gesamtanalyse_und_ideen.md` (Gesamtanalyse, vom Betreiber 22:28 beauftragt), `STOFFSAMMLUNG_REGISTER_41_42.md` (Vorbereitung des Registerauftrags), `AUFGABEN_BETREIBER_2026-09-26.md` und dieses Dokument (Nachtrag angehängt). Die nächste Mac-Sitzung nimmt sie in Schritt 0 mit.

| | |
|---|---|
| **Fertig (TB-105, `2e21471`)** | Regimewache an allen drei Einbaustellen, `pruefe_einbau()` 3 von 3 (Register **11.1 erfüllt**; 11.2/11.3 bleiben offen, TB-30b) · 14 × „Keine Daten gefunden“ unter dem Modus rc 2 · `symbols_config.py` unter dem Modus rc 2 bei leerer oder fehlender Liste · `manual_close.py` legt das Log erst bei der ersten Zeile an · `strategy_paths.py`/`bot_lauf.py` ohne Ordner unter dem Modus · Klasse (iii) im Trockenlauf leer, auch im frischen Klon |
| **Fertig (TB-106, `f22f91e`)** | Rückfall (d) in den eingefrorenen Dateien: 7 Ersatzwerte ⇒ rc 2 (`faltenplan.py`, `benchmark.py`, `auswertung.py`), unbekannter `_bedingung`-Text ⇒ rc 2 · `nachschlagen()` `e ≤ 0 ⇒ 0` ist Rechenregel, bleibt · tote Felder `mindesttraining_jahre`/`embargo_nach_falten` und Berichtszeile raus · `herkunft.py` planmässig geöffnet: Datenpfad durch `block()`/`anhaengen()`, unter dem Modus Pflicht; im Modus hasht die Kette `d9449faf…` = registrierter Datenstand · **`register()` `57ec6573…` ⇒ `0ece95e2…`** · **neues Abbild `sperrliste_abbild_2026-09-25b.json`, `40ffe18d…`** |
| **Fertig (TB-107, `f61bd97`)** | `_min_history` genau ein Treffer sonst rc 2 · zweite Kopie in `faltenplan_neun.py` rc 2 (**eigener Commit `f5fdb53`, vor Fables Antwort auf 25d gebaut**) · `getattr` in `strategy_paths.py` raus (Live-Abnahme 101 Aufrufer gleich) · `tb40_lauf_*` werden entfernt · **Laufbereich 81 Module** (neu nur `shared/regimewache.py`) · Gegenprobe `shared/test_main_gegenprobe.py`: 14 Stellen, alle mit Abfrage |
| **Durchgehend** | Benchmark-Tabelle im Modus (Repo und frischer Klon) und ohne Modus **bytegleich `64fb2912…`** · `test_vorregistrierung` 196/196 · Datenstand `d9449faf…`, Snapshot `63e4b6c8…` unverändert · Register unverändert (0–40, 7993 Zeilen) |
| **Fable** | 25b, 25c beantwortet und im Repo. **25d (TB-106, vier Fragen) offen**, im Repo und in der Projektablage. **25e (TB-107, drei Fragen)** und **25f (Gesamtanalyse und Ideen, Recherchefreigabe nur für diesen Vorgang)** geschrieben, im Repo und in der Projektablage, noch nicht übergeben. Antwortnamen: 25d, 25e, 25f je passend zur Anfrage |
| **Offene Punkte vor dem Tag, Reihenfolge** | (1) Fable 25d/25e · (2) **Register 41/42**: Fable-Einträge 24c, 24d, 25a, 25b (a–h), 25c (a–h), dazu 25d/25e · (3) **Auftrag zu 19**: Sauberkeitsprüfung über den Laufbereich, mit der Ausnahme für registrierte Protokolle, die vorher im Register stehen muss (25c 4 (4)(b)) · (4) Plan-Punkt 3, der Erzeuger auf dem Signalpfad (`herkunft.py`: Prüfansicht und `TB30A_BASE_DIR` je nach 25d mit einer Öffnung) · (5) die übrigen Punkte aus Block 4 Zeile 5 |
| **Freie Nummern** | frei ab **TB-108** · Fable-Anfrage frei ab **25g**, Antworten erwartet **25d, 25e, 25f** |
| **Wartet** | **Betreiber**: Aufgabenliste `projektfuehrung/AUFGABEN_BETREIBER_2026-09-26.md` |

**Fehler dieses Abschnitts, mit Regeln:**

| | Fehler | Regel daraus |
|---|---|---|
| 1 | In Anfrage 25c die Fundstelle der Rasterbedingung als „Abschnitt 4“ genannt, **ohne nachzusehen**; richtig ist Abschnitt 6. Fable hat es gefunden | ⭐ **Jede Registerstelle, die ich nenne, vorher im Register nachsehen** (`awk` auf die Überschrift davor), auch wenn sie mir sicher scheint |
| 2 | Im Auftrag TB-106 „13 `Abbruch`-Stellen“ geschrieben, gezählt sind 12 | Zahlen im Auftrag nur aus einer Messung übernehmen, sonst „vermutlich“ schreiben |
| 3 | Ein erster Entwurf von 25d behauptete „von 12 Registerstellen als Abbruch beschrieben“, ohne Messung. Vor dem Ablegen gefunden und ersetzt | ⭐ **Vor dem Ablegen jeden Satz mit einer Zahl oder Fundstelle gegen seine Quelle lesen** |
| 4 | TB-107: Das Terminalfenster des Wächters wurde zweimal geschlossen, bevor der Satz abgeschickt war; erst der dritte Auslöser lief | Nach jedem Start-Auslöser mit der Sonde `starte_TB-99` prüfen, ob `claude-Prozesse: 1 im Repo`; nach 15 Minuten ohne Schritt-0-Commit den Betreiber erinnern |

---

## Nachtrag 3 — fortgeschrieben 25.09.2026, 23:30

**Gemessen.** TB-108 ist abgegeben (`486032d`, 23:12) und um 23:24 per Schliess-Auslöser beendet. **Register jetzt 0–42**: 41 und 42 mit 67 Einträgen aus Fable 24b–25c, 108 Zitate mit `diff` rc 0, `numstat` 1134/0. Sonde vorher = nachher. **`register()` `0ece95e2…` ⇒ `c85dd6c3…`** (die Registerdatei ist Teil). Befund der Sitzung: **H6 ist bis heute nicht eigenständig** (TB-97), in 42.6 als offen eingetragen.

| | |
|---|---|
| **Fable** | **25d und 25e beantwortet** (Projektablage 22:36, abgeschrieben ins Repo mit TB-109 Schritt 0). 25d: TB-106 angenommen, `f5fdb53` steht; `herkunft.py` ein zweites Mal öffnen (Prüfansicht, `TB30A_BASE_DIR`); `auswertung.py` hat nur die Ausgänge 0 und 2. 25e: TB-107 angenommen; zwei weitere Ablagen; „null Trades ist ein Wert“; Stummel in `pfadvergleich.py`. ⚠️ **Fehler in 25e (3):** Stummel `lambda: False` würde den Modus fälschlich einschalten (`strategy_paths` fragt `is not None`); gebaut wird mit `None`, Berichtigung in Register 43 als vorläufig. **25f (Gesamtanalyse) offen** |
| **Freigaben 23:04 und 23:14** | TB-109 (alles aus 25e, inkl. 10 Live-Stellen) · TB-110 (Register 43) · **zwei Sitzungen parallel** · TB-111 (`herkunft.py` und `auswertung.py` nach 25d, neues Abbild) |
| **Nacht** | **Sitzung A** im Hauptordner: TB-109, danach TB-110 in derselben Sitzung. **Sitzung B** im Worktree `~/trading-bot-tb111`, Zweig `tb-111`: TB-111. Der Worktree wird von TB-109 in Schritt 0c angelegt; B startet der Betreiber von Hand. B wird nicht vom Wächter geschlossen und schreibt nicht in `JOURNAL.md` |
| **Danach** | Zusammenführung `tb-111` ⇒ `main` als eigener Auftrag (TB-112) · Register 44 für TB-111 · Fable 25f lesen · Erweiterung von 19 · Erzeuger |
| **Freie Nummern** | frei ab **TB-112** · Fable-Anfrage frei ab **25g** |

**Fehler dieses Abschnitts, mit Regel:** Keiner neu. Beobachtung: Fable hat 25d/25e beantwortet, während ich die Antworten noch als ausstehend meldete. Die Projektablage war dabei aktuell, meine Suche über `project_search` fand sie nicht sofort. ⇒ **Neue Fable-Antworten über `project_info` (Liste) prüfen, nicht über die Suche.**


---

## Nachtrag 4 — fortgeschrieben 26.09.2026, 02:25

**Gemessen.** Sitzung A hat TB-109 (`723281f`, 00:36) und TB-110 (`6a7996a`, 00:57) abgegeben. Um 01:14 wurde sie per Schliess-Auslöser beendet; das Wächter-Log meldet 1 Sitzung mit TERM beendet, 0 noch da. **HEAD `6a7996a`.**

**Sitzung B (TB-111) ist nicht gestartet:**
- Zweig `tb-111` steht auf `f4d6d6d`;
- der Worktree-Index ist unverändert seit 23:42;
- die Sonde um 01:15 meldet „claude-Prozesse: 0 im Repo, 0 ausserhalb“.

Der Betreiber ist per Nachricht informiert. Der Hauptordner ist frei.

| | |
|---|---|
| **Fertig (TB-109)** | 10 × `trades.empty ⇒ exit()` unter dem Modus rc 2, ohne Modus zeichengleich (Trade-Listen, `vergleich.py --pruefen` rc 0, `test_ergebniskurven` 44/44) · `tb40_faltenplan_*`/`tb40_proben_*` werden entfernt · Stummel `None` in `pfadvergleich.py` · Gegenprobe 24 Stellen, alle mit Abfrage · Audit (iv): (i) ausserhalb 11 statt erwartet 21 · A3: kein Cron-Lauf erreicht die Stellen |
| **Fertig (TB-110)** | **Register 0–43**: 15 Einträge aus 25d/25e, 31 Zitate rc 0, 6 Marken, keine in Abschnitt 10, numstat 345/0 · **`register()` `c85dd6c3…` ⇒ `c92900a8…`** · 43.3 = Berichtigung `None` als vorläufig |
| **Durchgehend** | Benchmark `64fb2912…` (Repo, Klon, ohne Modus) · Sonde gegen `40ffe18d…` vorher = nachher · `test_vorregistrierung` 196/196 · Abbild unverändert `40ffe18d…` |
| **Fable** | **25f (Gesamtanalyse) beantwortet**: Projektablage 21:45Z, **noch nicht im Repo**. Kern: 10–14 Aufträge bis zum Tag; drei Bündel statt Einzelaufträge; Binance ist seit 1.7.2026 für EU-Kunden keine Ausführungsstelle; vier Dinge vor dem Tag (db-Sicherung O6, zweiter und kalter Leser V8/F3, Nullbefund-Skizze F4, P1 falls fehlend); acht Betreiberentscheidungen |
| **Gemessen zu 25f** | **P1 steht schon im Register** (16.4 (g)–(m)); offen ist nur der Vollzug (16.11 Nr. 3: kein Leiter-Skript) ⇒ Entscheidung 8 entfällt · **N = 653** zählt deduplizierte Kombinationen einschliesslich Forschungsraster; die Grenzen stehen im Versuchsregister, Abschnitt 5 · Notiz: `ablage/MESSUNG_2026-09-26_fable25f_voraussetzungen.md` |
| **Vorbereitet, nicht abgelegt** | Anfrage an Fable `ENTWURF_FABLE_ANFRAGE_2026-09-26a_…` (TB-109/110, zwei Messungen, drei Fragen: `None`, Reichweite (iv), Gegenprobe über `main()`); Platzhalter für TB-111 und die 25f-Karten |
| **Nächste Schritte** | (1) B starten (Betreiber) oder TB-111 im Hauptordner neu fassen · (2) Karten zu 25f, Entscheidungen 1–7 · (3) 25f ins Repo abschreiben · (4) Anfrage 26a ablegen · (5) TB-112 Zusammenführung + Register 44 · (6) nach Fable-Bündelvorschlag: 19-Auftrag mit F8, Erzeuger |
| **Freie Nummern** | frei ab **TB-112** · Fable-Anfrage frei ab **26a** (25g nicht vergeben) |

**Fehler dieses Abschnitts, mit Regeln:**

| | Fehler | Regel daraus |
|---|---|---|
| 1 | Beim Prüfen vor dem Schliess-Auslöser einmal `git status --porcelain` über die Brücke ausgeführt. Das ist verboten; es gab nur eine Zahl aus und veränderte nichts | ⭐ Vor dem Schliessen nur `git log`, `rev-parse` und das Wächter-Log. Den sauberen Arbeitsbaum belegt die Sitzung selbst im Ergebnis |
| 2 | In einem Entwurf die Lückentabelle „Register 16 (Nr. 3)“ genannt, ohne die Unterüberschrift nachzusehen; richtig ist 16.11. Dazu Zeilennummern vom Stand vor TB-110 (+345 Zeilen) | Fundstellen mit Abschnittsnummer nennen, nicht mit Zeile; Zeilen nur mit Stand-Commit |
| 3 | Sitzung B galt ab „Fertig“ (00:07) als gestartet, ohne Nachweis | Nach dem Start einer App-Sitzung auf einen Nachweis warten (erster Commit oder die Sonde zählt einen Prozess), bevor sie als laufend gemeldet wird |


---

## Nachtrag 5 — fortgeschrieben 26.09.2026, 20:50, sauberer Stand

**Gemessen.** Seit Nachtrag 4 sind fünf Aufträge abgegeben (TB-111 bis TB-115), alle per Schliess-Auslöser beendet; die letzte (TB-115) um 18:36Z, „0 noch da“. **HEAD `10e9697`.** Es läuft keine Mac-Sitzung.

| | |
|---|---|
| **Fertig (TB-111, Zweig, `49f0868`)** | `herkunft.py` im Modus (Prüfansicht `paths.DATA_DIR`, `TB30A_BASE_DIR` ⇒ 2), `auswertung.Abbruch` endet mit 2 · Befund A2b · Abbild `sperrliste_abbild_2026-09-26.json` `e655c1c8…` |
| **Fertig (TB-112, `af6042f`)** | 19 über den Laufbereich: `ARBEITSBAUM_PFADE` 15 Einträge, `REGISTRIERTE_PROTOKOLLE` als `:(exclude)`, Test 26/26, Audit 0 · db-Sicherung täglich 05:20 nach iCloud (Cron vom Betreiber gesetzt, `grep -c` = 1) |
| **Fertig (TB-113, `0df8c64`)** | Merge `257e7db` · Register 44 · Arbeitsweise 22.1 Nachtrag (Wächter startet `claude --effort high --remote-control`) und 22.9 „Sitzung vor dem Satz“ · Worktree entfernt |
| **Fable 26a** | erste gesammelte Tagesanfrage (13 Fragen, Nullbefund-Skizze, Budget, AF-F0) · Antwort `FABLE_ANTWORT_2026-09-26a_dreizehn_fragen_nullbefund_registerblock.md`: alle fünf Aufträge angenommen; Entscheidung 8 entfällt (16.4 (g)–(m) steht, Fables Selbstberichtigung); `None` bestätigt; R1–R8, darunter **R6/R7: nach dem Tag nur registrierte Messbitten** |
| **Fertig (TB-114, `90307cb`)** | **Register 45** (R1–R8 zeichengleich, 45.0–45.10, 11 Marken, numstat 218/0) · dritte Öffnung `herkunft.py`: eine Pfadregel mit der Sonde, neun TB-24-Listen in `EINGEFROREN`, `datenstand(None)` im Modus 2 · `register()` `a0e477fd…` ⇒ `03178075…` (A) ⇒ **`5acb4c19…`** (B3) · `herkunft.py` ⇒ `ed521ac1…` · neues Abbild `sperrliste_abbild_2026-09-26_tb114.json` **`5e5ad109…`** (34/0/0, eingefroren 19) · ⚠️ **Abbruch in Block C**: Die Sonde meldet Zuwachs in `EINGEFROREN` gegen ein altes Abbild nicht einzeln. **45.11 nicht geschrieben, `5e5ad109…` noch nicht als gültig registriert** |
| **Fertig (TB-115, `10e9697`)** | nur lesend. M1: 9/9 geschlossene Kerze (Papier und Selektion); Teilkerze in `XAUTUSDT_1h.csv`, ungelesen · M2: 150 Aktienreihen split- und dividendenbereinigt, keine Bot-Regel mit absolutem Niveau; ⚠️ Zuteilung Stufe 3 vergleicht bereinigtes Dollar-Volumen · M3: Sonde bindet nur `auswertung.py`; ⚠️ `auswertung.py` liest `herkunft.json` nicht |
| **Durchgehend** | Benchmark `64fb2912…` (Repo, Klon) · ohne Modus 8/8 bytegleich · Trockenlauf 9 × rc 0 · `test_vorregistrierung` 196/196 · Register **0–45** |
| **Fable** | Anfrage **27a** geschrieben (14 Fragen aus TB-114/115 + Einordnung des Bündels „Wachen vor dem Tag“), im Repo und in der Projektablage, zusammen mit ERGEBNIS_TB-114/115. **Wird am 27.09. übergeben** (ein Takt je Tag) |
| **Nächste Schritte** | (1) Fable 27a · (2) Bündel „Wachen vor dem Tag“ (Sonde vergleicht `EINGEFROREN`, `fehlend` ⇒ 2, Snapshot nachrechnen, ggf. `auswertung.py` prüft `herkunft.json`) mit 45.11/46 und neuem Abbild · (3) Erzeuger (Stufe V, Abnahme nach R5) · (4) TB-30b Posten, Stufe IV, Block-4-Reste, Kettenlauf, Stufe VI |
| **Offen beim Betreiber** | Karte „TB-114-Rest“ kam ohne Auswahl zurück ⇒ Vorgabe: über Fable 27a. Speicher-Export bis 29.09. · zwei Crontab-Zählungen (`equity_simulation`, `multi_symbol_optimise`) · db-Sicherungslog nach 05:20 mit `grep -c` |
| **Freie Nummern** | frei ab **TB-116** · Journal bis **DN** · Fable-Anfrage 27a vergeben, Antwort erwartet 27a |

**Fehler dieses Abschnitts, mit Regeln:**

| | Fehler | Regel daraus |
|---|---|---|
| 1 | Im Auftrag TB-114 eine Erwartung an die Sonde gesetzt („die neun neuen Einträge“), ohne die Sonde zu lesen. Die Sitzung hat deshalb abgebrochen; der Befund selbst ist echt | ⭐ **Eine Erwartung an ein Werkzeug steht im Auftrag nur mit Fundstelle im Werkzeug.** Sonst: „vom Werkzeug abhängig, im Ergebnis beschreiben“ |
| 2 | Titel der Anfrage 27a zuerst mit „siebzehn Fragen“; gezählt 14 | Vor dem Ablegen zählen (`grep -c`), dann benennen |
| 3 | TB-115: Satz lag 1 h 40 min im Fenster | Nachschau 45 min nach dem Anlegen; ohne Schritt-0-Commit erinnern (so gemacht) |


---

## Stand 27.09.2026 (TB-119)

**Gemessen von der Mac-Sitzung TB-119 am 27.09.2026, 18:20, am `HEAD 4c1650d` (nach TB-119 A1).** Ausnahme: die Zeile „Projektablage“. Sie hat der steuernde Chat gemessen; die Sitzung sieht die Ablage nicht. Belege: `docs/belege/TB-119/`.

| | |
|---|---|
| **Register** | höchster Abschnitt **46**, 10 347 Zeilen, sha256 `18e39ee29b9bd4f03a2ad4953c85c2e59558de3aaab26844ae58fb7590fca93c` (= 0b und TB-118 0) |
| **Gültiges Abbild** | `sperrliste_abbild_2026-09-26_tb117.json`, sha256 `46f0ad5d1d83…`. Sonde dagegen, rein lesend: Pfad-Bestandteile **37/0/0** (Punkte 15, bestimmt 0, `eingefroren` **22**), Mengenvergleich 22/22 ohne Befund, rc 2 nur wegen der zwölf Regel-Bestandteile (wie `ERGEBNIS_TB-117`, Zeile 163). Beleg `a2_sonde.txt`; `git status --porcelain` vorher = nachher |
| **Code-Hashes (sha256)** | `research/vorregistrierung/herkunft.py` `c6c133886299…` · `research/vorregistrierung/auswertung.py` `8ec45123a9da…` · `shared/sperrlistensonde.py` `98c02e0e9b42…` |
| **Fable** | 27a und 27b beantwortet und im Repo (`FABLE_ANTWORT_2026-09-27a_…`, `…27b_…`). **27c offen** (Anfrage im Repo seit `7eadc7a`, keine Antwort). ⚠️ **Kein Fable-Volumen bis Dienstag, 29.09.2026.** Gesammelt wird in `FABLE_SAMMLUNG_fuer_2026-09-29.md` |
| **Projektablage** | gemessen vom steuernden Chat am 27.09. gegen 18:15: **vorher 148 Dateien, 1 570 315 Tokens (79 %), nachher 40 Dateien, 638 044 Tokens (32 %)**. Reihenfolge nach 27b C4: erst 13 Dateien abgelegt, dann 120 entfernt, dann gemessen. *Das ist die eine Zeile, die 27b C4 hier verlangt.* |
| **Plan bis Dienstag** | (1) **TB-119**, Repo nachziehen und Regelwerk-Nachtrag · (2) **TB-120** Erzeuger (Stufe V), Bestandsaufnahme, nur lesend · (3) **TB-121** kalter Leser für Registertext 1–12 (Fable 25f V8/F3). Was an 27c hängt, wartet: Leiter L2–L5, Öffnung `paths.py` (T117-5), Registerauftrag zu 27c |
| **Offen beim Betreiber** | Speicher-Export des alten Projektspeichers, Frist **Dienstag, 29.09.2026** |
| **Freie Nummern** | TB frei ab **122**, sobald TB-120/121 vergeben sind · Fable-Anfrage am Dienstag: **29a** · Journal nach TB-119 frei ab **DS** |

---

## Umzug 29.09.2026, 07:15 — Stand für den neuen steuernden Chat (UMZUG 4, Schritt 3)

*Geschrieben vom steuernden Chat (seit 24.09., 22:40). Jede Zahl ist mit „gemessen“ (heute über die Geräteanbindung) oder „aus Ergebnis“ (mit Fundstelle) gekennzeichnet.*

### Block 1 — Stand in drei Zeilen

- **Fertig (27.09.):**
  - TB-118: Projektwissen, Repo-Seite.
  - Ablage geräumt: 148 → 40 Dateien, 79 % → 32 %.
  - TB-119: Repo nachgezogen, Regelwerk nach Fable 27b Teil E, 13 D2-Regeln.
  - TB-120: Erzeuger-Bestandsaufnahme, nur lesend; 61 Anforderungen, 17 Lücken, Schnitt in neun Aufträge E-1 … E-9, 17 Fragen F-1 … F-17.
- **Läuft:** nichts. Gemessen 05:09Z: 0 claude-Prozesse, nachdem das unbenutzte TB-121-Fenster vom 27.09. geschlossen wurde. TB-121 ist **nie gestartet** worden; der Einfügesatz wurde nicht abgeschickt.
- **Als Nächstes:**
  1. **Fable-Anfrage 29a** aus `FABLE_SAMMLUNG_fuer_2026-09-29.md`. Fable hat ab heute wieder Wochenvolumen.
  2. TB-121, kalter Leser.
  3. TB-122 = E-1, Posten 3, freigegeben.

### Block 2 — HEAD und Commit-Kette

- **HEAD `07fcca7`** (TB-120 Abgabe, 27.09., 19:59 Ortszeit), gemessen, Zweig `main`.
- Commits am 27.09.:
  - TB-118: `f8056ef` … `2a0893b`;
  - TB-119: `7eadc7a`, `4c1650d`, `6126c64`, `df825b6`, `8c6ab75`, `d9e3600`;
  - TB-120: `5f819c1`, `aab641e`, `3265b3a`, `42f507a`, `d173ad4`, `07fcca7`.
- Am 28.09. kein Commit.
- **Uncommittet** (gemessen, `ls-files --others` und `diff --numstat`):

| Datei | Zustand | md5 |
|---|---|---|
| `docs/auftraege/MAC_TB-121_kalter_leser_register_1_12.md` | neu | `f6147088b34eeed7652f62a9eef69da4` |
| `docs/auftraege/MAC_TB-122_posten3_achsen_durchreichen.md` | neu (heute abgelegt, Platzhalter `<<ERWARTET_0A>>` noch offen) | `ad4eca4c255e5cc803be0f785e200c7a` |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | geändert, zeigt auf **TB-121** | `8d1dba47587d45c226a717cec3392598` |
| `docs/projektfuehrung/FABLE_SAMMLUNG_fuer_2026-09-29.md` | geändert, numstat 84/0 | `b363c9485017b00ff42fee5f45585b49` |
| `docs/projektfuehrung/UEBERGABE.md` | geändert (dieser Block) | nach dem Anhängen messen |

✅ **TB-121 Schritt 0a ist nachgezogen (29.09., 07:20):** Die Tabelle in `MAC_TB-121` nennt jetzt alle fünf Dateien; für `UEBERGABE.md` prüft sie „numstat gegen HEAD, entfernt 0“ statt eines md5, weil diese Datei sich bis zum Start noch ändern kann. Die md5 von `MAC_TB-121` in der Tabelle oben ist damit überholt — massgeblich ist die Datei.

### Block 3 — Die tragenden Zahlen

| | Wert | Fundstelle |
|---|---|---|
| Register | Abschnitte 0–46, 10 347 Zeilen, sha256 `18e39ee2…` | aus Ergebnis TB-119 A2, unverändert seit TB-117 |
| Gültiges Abbild | `sperrliste_abbild_2026-09-26_tb117.json` `46f0ad5d…`, Sonde 37/0/0, `eingefroren` 22 | TB-119 A2 |
| `herkunft.py` / `auswertung.py` / `sperrlistensonde.py` | `c6c13388…` / `8ec45123…` / `98c02e0e…` | TB-119 A2 |
| Snapshot / Datenstand / Benchmark | `63e4b6c8…` / `d9449faf…` / `64fb2912…` | Register 18, 39.2 |
| Laufbereich | 81 Module | Register 44-8 |
| Zellen im Raster | 2 416 | Register 3, TB-120 `d_zellenzahl.txt` |
| db-Sicherung | 29.09., 05:20: 12/12, Fehler 0, `docs.tar.gz` am Commit `07fcca7` | gemessen, `logs/system/db_sicherung.log` |
| Projektablage | 40 Dateien, 638 044 Tokens (32 %) am 27.09., 18:15 | gemessen dort; heute neu messen (Schritt 4) |
| **Nummern** | TB frei ab **123** (121, 122 vergeben) · Fable-Anfrage **29a** · Journal frei ab **DT** (TB-120 schrieb DS) | gemessen bzw. aus Ergebnis TB-120 |

### Block 4 — Offene Punkte, in Reihenfolge

1. **Fable 29a:** Die Sammlung wird zu einer Anfrage, gegen 27.1 gelesen, als Kopierblock übergeben. Inhalt:
   - A: 27c vollständig (T116-1…5, T117-1…7);
   - B: neun Punkte aus TB-118;
   - C: Kenntnis Ablage;
   - D: 19/6 gegen 6d, drei Punkte aus TB-119, 27.4 zu `MAC_TB-119`, F-1 … F-17 mit Neigungen;
   - dazu der Schnitt E-1 … E-9.
   - In die Ablage vorher: `ERGEBNIS_TB-118`, `ERGEBNIS_TB-119`, `ERGEBNIS_TB-120` (nach 27.1 lesen) und die Anfrage selbst.
   - Warum zuerst: E-2 … E-9 warten auf die Antworten.
2. **TB-121**, kalter Leser: freigegeben, nur lesend, darf parallel zur Fable-Wartezeit laufen.
3. **TB-122** = E-1, Posten 3: freigegeben (Karte 27.09., ca. 20:20, wörtlich im Auftrag). Vor dem Start den Platzhalter 0a füllen.
4. Nach Fables Antwort: E-2, Registerauftrag mit den Antworten auf 27c und F-1 … F-17, danach E-3 … E-9 nach TB-120 Abschnitt 5.
5. Später:
   - Leiter-Skript und Stufe IV nach 27c L2–L5;
   - Öffnung `paths.py` (T117-5, E-9);
   - Kettenlauf und Stufe VI.

### Block 5 — Wartezustände

| wartet | auf |
|---|---|
| Fable | Anfrage 29a (noch nicht geschrieben) |
| TB-121 | Einfügesatz des Betreibers nach dem Auslöser `starte_TB-121` (Zeiger steht auf TB-121) |
| TB-122 | Abgabe von TB-121, dann Zeiger, Platzhalter und Auslöser |
| E-2 … E-9 | Fable 29a |
| **Betreiber** | ⚠️ **Speicher-Export des alten Projektspeichers — Frist HEUTE, 29.09.2026** (`ERINNERUNG_2026-09-25_speicher_export.md`) |

### Block 6 — Freigaben und Sperrliste

**Freigaben, die noch nicht verbraucht sind:**
- **TB-121:** Karte 27.09., 18:25, „Wir arbeiten alles strukturiert ab“; wörtlich im Auftrag.
- **TB-122:** Karte 27.09., ca. 20:20, „E-1: TB-30b Posten 3 (Empfohlen)“; wörtlich im Auftrag.

**Nicht freigegeben:**
- E-3 … E-9;
- das Register;
- jede Öffnung von `herkunft.py`, `paths.py`, `zuteilung.py`.

**Sperrliste:** 14 Punkte. TB-122 bewegt Punkt 11 (Commit-Hashes der Optimierer und Simulation) planmässig nach 37.3. Kein neues Abbild vor dem nächsten Bündel.

### Block 7 — Fehler dieses Chats und die Regeln daraus

| # | Fehler | ⇒ Regel |
|---|---|---|
| 1 | TB-114: Erwartung an die Sonde gesetzt, ohne die Sonde zu lesen ⇒ Abbruch in Block C | **Eine Erwartung an ein Werkzeug steht im Auftrag nur mit Fundstelle im Werkzeug, sonst „vom Werkzeug abhängig, im Ergebnis beschreiben“.** *Nicht in ARBEITSWEISE (gemessen: 0 Treffer)* |
| 2 | TB-116: Schliess-Auslöser bei 539 s ⇒ vom Wächter abgewiesen | **Alter des Abgabe-Commits vor dem Auslösen messen** (`git log -1 %ct`); erst ab 600 s |
| 3 | TB-117-Auftrag nannte einen 0b-Wert aus TB-116, den TB-116 nicht gemessen hatte | Zahlen aus früheren Ergebnissen nur mit Fundstelle im Ergebnis |
| 4 | TB-119-Auftrag musste den nach 27.5 gestrichenen Wert wörtlich nennen ⇒ Auftrag darf nicht in die Ablage | Frage an Fable in der Sammlung. Bis dahin: **Aufträge, die eine 27.5-Streichung vollziehen, gehen nicht in die Ablage** |
| 5 | TB-120: `faltenplan.faltenplan()` für eine Zählung aufgerufen; es startet einen Loader-Trockenlauf (ohne Folge, abgebrochen) | **`faltenplan.faltenplan()` ist kein Lesen**, wie `faltenplan.py main()`. In nur lesenden Aufträgen verbieten |
| 6 | TB-121 lag ~35 h unabgeschickt im Fenster, zwei Nachschauen ohne Wirkung | Nach dem Auslöser prüfen, ob Schritt 0 committet ist. Ohne Commit ist der Satz nicht angekommen (K3l) ⇒ einmal Push, dann warten; keine Nachschau-Kette |
| 7 | `project_write` mit `local_path` ausserhalb des Arbeitsverzeichnisses abgewiesen | Dateien für die Ablage vorher ins Arbeitsverzeichnis kopieren, md5 prüfen, dann `project_write` |

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Die fünf uncommitteten Dateien aus Block 2. Sie gehen mit dem nächsten Schritt-0-Commit ins Repo.
- `logs/auftraege/`: nur ältere Reste (`NACHTRAG_TB-78*`, `TB-58b_v2.md`, `nachtrag5_anzuhaengen.md`), gemessen; nichts Neues aus diesem Chat.
- Die Regeln aus Block 7, Nr. 1, 5 und 6 stehen noch nicht in ARBEITSWEISE. **Betreiber 29.09., Auswahlkarte beim Umzug: „Ja, mit nächstem Auftrag“.** Sie gehen als kleiner Schritt in TB-122 oder in den Registerauftrag E-2. Auf dieselbe Karte hin sagte der Betreiber zu UMZUG Schritt 2 „Passt so“; die Arbeitsweise bleibt ohne weitere Ergänzung.
- Die Regeln aus Block 7 stehen seit 29.09. auch in der Erinnerung (`preferences.md` des Projekts).
- Neu in der Ablage, **nicht** von diesem Chat: `projektfuehrung/FABLE_UEBERGABE_2026-09-29_neuer_chat.md`. Vermutlich ist Fable ebenfalls umgezogen. Der neue Chat liest die Datei und prüft, ob sie ins Repo gehört.

### Block 9 — Eröffnungstext

Die einzige Fassung steht in `UMZUG.md` Abschnitt 6. Sie zeigt seit TB-120 auf diese Datei.

**Stehende Pflichten des steuernden Chats** (Kurzfassung; massgeblich sind ARBEITSWEISE und UMZUG):
- Aufträge schreiben und per `starte_TB-<n>` auslösen; im Wächter-Log „Satz ins Fenster gelegt“ prüfen; schliessen mit `schliesse_<HEAD>` erst ab 600 s; Sonde `starte_TB-99`; Nachschau per `send_later`.
- Ergebnisse selbst lesen.
- Fable-Anfragen als vollständigen Kopierblock geben; Antworten über `project_info` finden, ins Repo übertragen, md5 prüfen.
- Jede Betreiberentscheidung als Auswahlkarte mit Empfehlung.
- Befehle für den Betreiber je eine Zeile.
- Sitzungen mit Aufwand hoch.
- Eine gesammelte Fable-Anfrage je Tag.
- Die Sicherheitsregeln oben gelten unverändert: kein `git status`, `git add` oder Commit über die Brücke; nie überschreiben; keine Werte von Schlüsseln; kein SQLite über die Brücke; nichts nach `docs/` bei laufender Sitzung.

**Ablage-Abgleich beim Umzug (UMZUG Schritt 4), gemessen 29.09., 07:12:** Ist 40 · Soll 44 · entfernen 0 · ablegen 5. Abgelegt wurden `UEBERGABE.md` (ersetzt), `MAC_TB-121` und `MAC_TB-122`. **Nicht** abgelegt: `MAC_TB-119` (27.4, Block 7 Nr. 4) sowie `KANDIDATEN_DURCHGANG_2.md` und `PROJEKTSTAND_einfache_sprache.md` (fehlen im Repo). `ohne_regel`: `PROJEKTSTAND_2026-09-26_einfache_sprache.md` bleibt (Betreiber 27.09.). Füllstand: `knowledge_size` 660 197 vorher, 670 544 nachher (42 Dateien, 34 %). Werkzeugausgabe in `logs/ablage_soll_2026-09-29/`.


---

## Nachtrag 29.09.2026, 07:55 — Umzugszeitpunkt nach Tokenverbrauch, schlankere Eröffnung

**Betreiberentscheidung 29.09.2026, ca. 07:50, per Auswahlkarte.** Anlass, wörtlich: *„Kannst du mich zukünftig zum passenden Zeitpunkt auf einen Umzug hinweisen damit wir zu einem bestmöglichen Zeitpunkt umziehen um den Verbrauch der beötigten token zu optimieren. Kannst du mir hierfür vorschlage machen und eine Empfehlung geben?“* Wegen „zukünftig“ gilt ARBEITSWEISE 15. Die Karte, wörtlich:
- „Wann soll ich dir künftig einen Umzug vorschlagen?“ ⇒ **„Mitzählen + sauberer Stand (Empfohlen)“**
- „Soll das Einlesen beim Umzug schlanker werden?“ ⇒ **„Ja, Kernlektüre ~40 KB (Empfohlen)“**

**Gemessen 29.09., 07:48** (`wc -c`, HEAD `07fcca7` plus Arbeitsbaum):

| Datei | Bytes |
|---|---|
| `UEBERGABE.md` | 39 691, davon der letzte Block (Umzug 29.09.) 9 827 |
| `UMZUG.md` | 21 605 |
| `ARBEITSWEISE.md` | 130 716, davon Abschnitt 0: 9 018 |
| `PRUEFPRINZIPIEN.md` | 21 472 |
| `BACKLOG.md` | 53 236 |
| **Summe** | **266 720** |

**Erschlossen, nicht gemessen:** Bei rund 3,3 Byte je Token kostet das Einlesen etwa 80 000 Tokens. Die Kernlektüre (letzter Übergabeblock, ARBEITSWEISE 0, UMZUG 3) hat rund 40 KB, also etwa 12 000 Tokens.

**Bringschuld:** Mit TB-122 oder dem Registerauftrag E-2 als Dokumentationsschritt einarbeiten, nach ARBEITSWEISE 5b: Text wörtlich, `numstat` je Datei, nichts umformuliert. Bis dahin gilt beim Umzug der bisherige Eröffnungstext. Der steuernde Chat weist dann darauf hin.

**(1) `UMZUG.md` Abschnitt 3, neue Zeile unter der Tabellenzeile** `| **5** | **Der Betreiber fragt danach** | dann gilt Abschnitt 4 |`:

```
| **6** | ⭐ **Der mitgezählte Verlauf erreicht etwa 200 000–250 000 Tokens** — das Zwei- bis Dreifache der Einlesekosten (Betreiber 29.09.2026) | am nächsten sauberen Stand oder vor dem nächsten grossen Block; Vorschlag mit Uhrzeit. Gezählt wird, was im Chat gelesen und geschrieben wurde (Bytes der Werkzeugausgaben ÷ ~3,3). ⚠️ **Schätzung, kein Messwert** — der Kontextfüllstand ist nicht ablesbar; die Zahl steht bei jedem Hinweis dabei |
```

**(2) `UMZUG.md` Abschnitt 4, Schritt 3, neuer Satz direkt vor der Tabelle „| | Block | ⚠️ |“:**

```
⭐ **Der jüngste Block der Übergabe ist selbsttragend** (Betreiber 29.09.2026): Er enthält alle neun Blöcke und wird beim Umzug als einziger Teil der Übergabe gelesen. Ältere Blöcke werden nur verwiesen, nicht vorausgesetzt.
```

**(3) `UMZUG.md` Abschnitt 6, benannte Ersetzung im Eröffnungstext:** Die Zeilen von `Lies in dieser Reihenfolge, über den Projects-Zugriff (in Klammern der Pfad im` bis einschliesslich `ohnehin über CLAUDE.md.` werden ersetzt durch:

```
Lies zuerst nur die Kernlektüre, über den Projects-Zugriff (in Klammern der
Pfad im Repo, falls du dort liest):

1. projektfuehrung/UEBERGABE.md    — nur den LETZTEN Block (die unterste
                                      „## …“-Überschrift); ältere nur bei Bedarf
                                      (docs/projektfuehrung/UEBERGABE.md)
2. projektfuehrung/ARBEITSWEISE.md — nur Abschnitt 0, die Ausgabe-Checkliste;
                                      die übrigen Abschnitte über ihre Zeiger,
                                      sobald der Anlass kommt
                                      (docs/projektfuehrung/ARBEITSWEISE.md)
3. projektfuehrung/UMZUG.md        — nur Abschnitt 3, die Auslöser
                                      (docs/projektfuehrung/UMZUG.md)

Gezielt nachlesen, sobald der Anlass kommt: PRUEFPRINZIPIEN.md vor jedem
Auftrag und jeder Bewertung (docs/PRUEFPRINZIPIEN.md — NICHT unter
projektfuehrung/) · projektfuehrung/BACKLOG.md bei Backlog-Arbeit
(docs/projektfuehrung/BACKLOG.md) · docs/UEBERGABEPROTOKOLL.md für den
Betrieb (Cronjobs, Neustarts, Schlüsselbund).
```

Der Rest des Eröffnungstexts bleibt unverändert.

**(4) `ARBEITSWEISE.md` Abschnitt 0, Tabelle „Wenn ein Arbeitsabschnitt endet oder ein Verlust droht“, benannte Ersetzung:**
Aus `| ☐ | Ein nötiger Umzug wird frühzeitig angekündigt | 10 |` wird:

```
| ☐ | Ein nötiger Umzug wird frühzeitig angekündigt — auch nach Tokenverbrauch: Verlauf mitzählen, ab ~200–250k am nächsten sauberen Stand vorschlagen, mit Zahl und Uhrzeit | 10; UMZUG 3 |
```

**(5) Backlog, neue Zeile in Abschnitt 4 unter `K4r`:**

```
| **K4s** | ⭐ **UMZUG NACH TOKENVERBRAUCH (29.09.2026, Betreiberentscheidung per Auswahlkarte).** Der steuernde Chat zählt den Verlauf mit und schlägt ab ~200–250k Tokens den Umzug am nächsten sauberen Stand vor (UMZUG 3, Zeile 6). Die Eröffnung liest nur noch die Kernlektüre (~40 KB statt 267 KB, gemessen). ⚠️ Die Zählung ist eine Schätzung, der Kontextfüllstand ist nicht ablesbar. **Preis, benannt:** Eine Regel ausserhalb von ARBEITSWEISE 0 greift erst, wenn ihr Abschnitt nachgeschlagen wird. Wortlaut und Messung: `UEBERGABE.md`, Nachtrag 29.09.2026, 07:55 |
```

**(6) Erinnerung:** eingetragen am 29.09.2026 in `preferences.md` des Projekts.


---

## Nachtrag 29.09.2026, 08:50 — Helfer-Agenten für Recherche, Lesen und Gegenlesen

**Betreiberfrage 29.09.2026, 08:45, wörtlich:** *„Ist es korrekt dass wir keine Helfer-Agenten für Recherchen einsetzen? Falls ja weshalb ist das so?“*

**Gemessen 08:47:** `ARBEITSWEISE.md`, `UMZUG.md`, `PRUEFPRINZIPIEN.md` und `UEBERGABE.md` erwähnen Agenten 0-mal. Es gab also keine Regel. Die Arbeitsteilung war um die drei Rollen Mac-Sitzung, Fable und steuernder Chat gewachsen; Helfer kamen darin nicht vor. Das war eine Lücke, kein Grundsatz.

**Betreiberentscheidung per Auswahlkarte, wörtlich:** „Wie sollen Helfer-Agenten künftig eingesetzt werden?“ ⇒ **„Recherche, Lesen, Gegenlesen (Empfohlen)“**

**Die Regel (Wortlaut für die Dokumente):**

```
### Helfer-Agenten des steuernden Chats (Betreiber 29.09.2026)

Der steuernde Chat setzt Helfer-Agenten ein für:
1. Web-Recherche, parallel wo sinnvoll;
2. grosse Lese- und Suchaufträge im Repo oder in der Ablage, deren Ergebnis eine
   Schlussfolgerung ist — damit das Lesematerial nicht im Chatverlauf landet
   (UMZUG 3, Auslöser 6);
3. Gegenlesen vor dem Übergeben: Ein frischer Helfer, der den Text nicht
   geschrieben hat, prüft jede Fable-Anfrage und jeden Auftrag Satz für Satz —
   jede Zahl, jede Fundstelle, jede Erwartung an ein Werkzeug gegen ihre Quelle
   (Übergabe Block 7; Register 27.1 für Fable-Anfragen). Befunde werden vor dem
   Übergeben eingearbeitet.

Nicht für: Belege — die Aussage eines Helfers ist eine Selbstauskunft (A8); was
als Messung zählt, prüft der steuernde Chat an der Rohausgabe oder die
Mac-Sitzung misst nach (A10). Nicht für Register, Commits, Aufträge schreiben
oder Freigaben. Ein Helfer schreibt nichts ins Repo.

Preis, benannt: mehr Gesamt-Tokens (ein Gegenleser liest seine Quellen selbst,
geschätzt 30 000–80 000 je Durchgang); dafür wächst der Chat langsamer.
```

**Bringschuld:** Mit TB-122 oder E-2 einarbeiten, als neuer Unterabschnitt in `ARBEITSWEISE.md` am Ende von Abschnitt 22 (nach 22.9). Dazu eine Zeile in Abschnitt 0, Tabelle „Wenn ich einen Auftrag schreibe“:

```
| ☐ | Vor dem Übergeben: frischer Helfer liest gegen — jede Zahl, Fundstelle und Werkzeug-Erwartung an der Quelle (auch für Fable-Anfragen) | 22.10 |
```

Backlog, neue Zeile in Abschnitt 4 unter `K4s`:

```
| **K4t** | ⭐ **HELFER-AGENTEN (29.09.2026, Betreiberentscheidung per Auswahlkarte).** Der steuernde Chat setzt Helfer für Web-Recherche, grosse Lese-/Suchaufträge und das Gegenlesen jeder Fable-Anfrage und jedes Auftrags vor dem Übergeben ein. Belege bleiben A8/A10, Register/Commits bei der Mac-Sitzung. Vorher gab es keine Regel (0 Treffer in den Führungsdokumenten). Wortlaut: `UEBERGABE.md`, Nachtrag 29.09.2026, 08:50 |
```

**Erinnerung:** eingetragen am 29.09.2026 in `preferences.md` des Projekts. **Erste Anwendung:** Fable-Anfrage 29a.
