# UEBERGABE 2026-09-25 — Stand des steuernden Chats

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
| 4 | In den eigenen Anfragen stand eine Trade-Zahl (656), die aus der Vorlage stammte | Jede Anfrage an Fable vor dem Übergeben gegen 27.1 lesen, auch übernommene Blöcke |

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
