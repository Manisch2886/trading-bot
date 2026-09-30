# UEBERGABE_ARCHIV — ältere Blöcke von UEBERGABE.md (bis 30.09.2026, vor 19:13)

> Abgetrennt am 30.09.2026, ca. 19:50, vom steuernden Chat (Betreiberentscheid T5 per Auswahlkarte, 30.09.2026, ca. 19:44: „Wie vorgeschlagen (Empfohlen)“). Nur im Repo, nicht in der Fable-Ablage. Der Inhalt unter der Linie ist byte-gleich zu `UEBERGABE.md` Z. 1–1026 vor der Teilung (md5 der ganzen alten Datei `a0227fd6b8221f98f3fa98142c1d2b9f`, 105 480 B). Fundstellen der Form „UEBERGABE.md, Nachtrag/Block … “ mit Datum vor dem 30.09.2026, 19:13 stehen hier.

---

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


---

## Nachtrag 29.09.2026, 09:20 — Helfer-Agenten: ein Regelwerk für alle drei Rollen · Umzugsampel im steuernden Chat · TB-121 abgegeben

**Betreiberfrage 09:12, wörtlich:** *„Was würdest du empfehlen wie wir die agents zukünftig integrieren?“* Vorher war Fables Antwort `FABLE_ANTWORT_2026-09-29a_betreiberentscheid_umzugstakt_ampel_agenten.md` eingegangen (Projektablage 07:11Z, noch nicht im Repo). Darin: Umzugstakt, Umzugsampel und Helfer-Agenten für Fables Rolle, Grundsatz *„finden, zählen, belegen — nie deuten“*.

**Betreiberentscheidungen per Auswahlkarte, wörtlich:**
- „Wie sollen die Helfer-Agenten künftig integriert werden?“ ⇒ **„Ein Regelwerk, alle 3 Rollen (Empfohlen)“**
- „Soll auch dieser Chat eine Umzugsampel am Ende jeder Antwort führen?“ ⇒ **„Ja, wie bei Fable (Empfohlen)“**

⚠️ **Ersetzt den Regeltext des Nachtrags 08:50** (Block „Die Regel“ und die Zeile `K4t`). Grund: Dessen Punkt 2 erlaubte eine Zusammenfassung als Ergebnis und ist damit schwächer als Fables Grundsatz. Bei der Einarbeitung gilt nur der Text unten.

**Regeltext (für `ARBEITSWEISE.md`, neuer Abschnitt 22.10; ein Abschnitt für alle Rollen statt zwei Fassungen, DOKUMENTATIONSSTANDARD 9):**

```
### 22.10 Helfer-Agenten — ein Regelwerk für alle drei Rollen (Betreiber 29.09.2026)

Grundsatz (Fable 29a, Abschnitt 3): Ein Helfer darf finden, zählen und belegen —
nie deuten. Seine Ausgabe ist Fundstelle, Zahl oder Quelle. Eine Zusammenfassung
dient höchstens der Orientierung („wo steht was“); was in eine Anfrage, einen
Auftrag, einen Bericht oder eine Entscheidung eingeht, liest der Auftraggeber
selbst im Wortlaut an der Fundstelle. Jeder Einsatz bekommt eine Protokollzeile
(Art, Suchwort oder Frage, erlaubte Dateien, Ergebnis); jeder Auftrag an einen
Helfer nennt die erlaubten Dateien und das Leseverbot.

Steuernder Chat: (1) Web-Recherche — Quellen mit URL, selbst gegengelesen;
(2) Fundstellen- und Zählaufträge in Repo und Ablage; (3) Gegenleser vor jedem
Übergeben einer Fable-Anfrage und eines Auftrags: ein frischer Helfer, der den
Text nicht geschrieben hat, liefert eine Liste Satz · Behauptung · Quelle ·
stimmt/weicht ab — für jede Zahl, Fundstelle und Werkzeug-Erwartung; bei
Fable-Anfragen zusätzlich gegen Register 27.1 (steht ein Wert darin, den Fable
nicht sehen darf?). Befunde werden vor dem Übergeben eingearbeitet.

Fable: wie FABLE_ANTWORT_2026-09-29a, Abschnitt 3 (Fundstellen, Mechanik,
Websuche mit Einzelfreigabe; Leseverbot `docs/belege/`, `ergebnisse/`,
Trade-Listen, `BACKLOG*.md`).

Mac-Sitzungen: Helfer nur zum Suchen und Lesen innerhalb der Sitzung. Messung,
Beleg und Commit macht die Sitzung selbst; jeder Helfereinsatz steht im
Ergebnisdokument. Nicht gemessen: ob Sperrliste und `deny` aus
`.claude/settings.local.json` auch für die Helfer der Sitzung greifen — die
erste Sitzung, die einen Helfer einsetzt, prüft das als Schritt 0 und bricht
ab, wenn nicht.

Belege bleiben A8/A10: die Aussage eines Helfers ist eine Selbstauskunft.
Nie für Register, Commits, Aufträge schreiben oder Freigaben; ein Helfer
schreibt nichts ins Repo.

Probe statt Regel (Fable 29a: „Die Entscheidung fällt an der Messung, nicht an
der Ersparnis“): Über die ersten drei Gegenlese-Durchgänge zählt der steuernde
Chat je Durchgang die Befunde, die er selbst übersehen hätte, und die
geschätzten Tokens. Hat keiner der drei einen solchen Befund, fällt das
Gegenlesen weg; sonst wird es Regel. Das Ergebnis steht in der Übergabe.
```

**Umzugsampel im steuernden Chat (für `UMZUG.md` Abschnitt 3, unter der neuen Zeile 6 aus dem Nachtrag 07:55):**

```
⭐ **Umzugsampel** (Betreiber 29.09.2026, Form wie Fable 29a Abschnitt 2): letzte Zeile jeder Antwort des steuernden Chats —
`Umzugsampel: <Farbe> · <geschätzte Tokens im Verlauf> · <Empfehlung>`
🟢 unter 200 000 — bleiben · 🟡 200 000–300 000 — Umzug am nächsten sauberen Stand oder vor dem nächsten grossen Block, mit Uhrzeit · 🔴 über 300 000, nach einer Komprimierung, oder wenn der Chat merkt, dass er Gelesenes verliert — Umzug vor dem nächsten Auftrag. Schätzung (Bytes ÷ ~3,3), kein Messwert.
```

Dazu in `ARBEITSWEISE.md` Abschnitt 0, Tabelle „Am Ende jeder Antwort“: `| ☐ | Letzte Zeile: Umzugsampel (Farbe · Tokens · Empfehlung) | UMZUG 3 |`.

**Backlog (Abschnitt 4, unter `K4s`), ersetzt die `K4t`-Zeile des Nachtrags 08:50:**

```
| **K4t** | ⭐ **HELFER-AGENTEN, EIN REGELWERK FÜR ALLE DREI ROLLEN, UND UMZUGSAMPEL (29.09.2026, zwei Auswahlkarten).** Grundsatz „finden, zählen, belegen — nie deuten“ (Fable 29a) für steuernden Chat, Fable und Mac-Sitzungen; Gegenleser vor jeder Übergabe als Probe über drei Durchgänge. Offen: ob `deny` für Helfer der Mac-Sitzung greift (erste Nutzung misst). Umzugsampel als letzte Zeile jeder Antwort des steuernden Chats. Wortlaut: `UEBERGABE.md`, Nachtrag 29.09.2026, 09:20 |
```

**Bringschuld:** Mit TB-122 oder E-2 einarbeiten: `ARBEITSWEISE.md` 22.10 und Abschnitt 0, `UMZUG.md` 3, Backlog `K4t`. Dazu `FABLE_ANTWORT_2026-09-29a_…` aus der Ablage ins Repo abschreiben und md5 prüfen.

**Nummern:** Fable hat den Buchstaben 29a für seine Antwort vergeben. ⇒ **Die heutige Tagesanfrage heisst 29b.**

### TB-121 abgegeben (gemessen 09:14)

- `86e0d5e` Schritt 0 (06:48Z) und `04f07ef` Abgabe (07:00Z, Journal **DT**). Um 07:14Z per `schliesse_04f07ef…` geschlossen: 1 mit TERM beendet, 0 übrig. **HEAD `04f07ef`**; die Nachträge 07:55 und 08:50 sind in Schritt 0 mitcommittet (numstat 256/0).
- Ergebnis `docs/ERGEBNIS_TB-121_kalter_leser_register_1_12.md`, 85 Befunde (B 19 · V 19 · W 8 · M 16 · A 15 · Z 8). Vollständigkeitstest: 3 von 12 Bausteinen aus 0–12 schreibbar, 2 teilweise, 7 nicht. Stichprobe Code: 12/12 gefunden und passend.
- Die 39 Fragen der Arten W, M und A (Nr. 39–77) gehen mit **29b** an Fable, nach dem Gegenleser gegen 27.1.
- ⚠️ **Befund zum Verfahren:** Die Sitzung war **nicht vollständig kalt**. Claude Code lädt sein Gedächtnisverzeichnis (`MEMORY.md`) von selbst, mit Zusammenfassungen zu den Registerabschnitten 15–46. Für künftige kalte Leser gehört dieses Gedächtnis vor dem Start ausgeschaltet oder umgangen. Offen, eigener kleiner Punkt; die Frage an Fable, ob das TB-121 entwertet, kommt in 29b.


---

## Nachtrag 29.09.2026, 12:25 — Anfrage 29b abgelegt · Betreiberentscheid T116-5 · Gegenlesen Durchgang 1

**Betreiberentscheid per Auswahlkarte (ca. 12:15), wörtlich:** „T116-5 / R24: Soll ein einzelner Bot bis zum Netting bis zu zwei Fünftel des Buchs tragen dürfen?“ ⇒ **„(a) So lassen (Empfohlen)“**. Das ist die Empfehlung von Fable (27c, R24) und des steuernden Chats. Kein Deckel je Bot vor dem Netting; R24 geht als Tatsachennotiz in E-2.

**Fable-Anfrage 29b** `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-29b_tagesanfrage_sammlung_erzeuger_kalter_leser.md`:
- 31 946 B, md5 `e189f941…`, gleich im Repo (uncommittet) und in der Ablage.
- Aufbau:
  - Teil 0: Kenntnis 27c/29a, T116-5, Freigabe `BACKLOG*` nicht erteilt, was mitgeht.
  - Teil 1: Sammlung B/C/D, zeichengleich, Z. 16–192.
  - Teil 2: TB-121, Fragen 39–77, zeichengleich, Z. 74–125.
  - Teil 3: Frage 78 (kalter Leser nicht ganz kalt).
- Als Kopierblock übergeben; die Antwort erwartet als 29b.
- Abschnitt A der Sammlung ist durch 27c erledigt.

**Mit der Anfrage abgelegt:** `ERGEBNIS_TB-118/119/120`.
- md5 `41fcd03b…`, `be616ba8…`, `95e83c61…`, gleich wie auf dem Mac.
- Sichtschutz-Zeile im Kopf geprüft; der Gegenleser hat gegen 27.1 gelesen.
- Ein Verdachtsfall (TB-118 Z. 106) war eine Kettenrang-Nummer, kein Ergebnis.
- `ERGEBNIS_TB-121` nicht abgelegt: Der Kopf hat keine Sichtschutz-Zeile (G5).

**Füllstand der Ablage, gemessen 12:23:** 49 Dateien, `knowledge_size` 745 654 (37 %). Vorher (07:12) 670 544.

**Gegenlesen, Probe Durchgang 1 von 3:** Der Helfer fand 6 Fehler in den neuen Teilen, die ich übersehen hatte, alle vor dem Übergeben berichtigt:
1. Gegenleser-Regel fälschlich Fables 29a zugeschrieben.
2. Angekündigte Protokollzeile fehlte.
3. Verweis auf „Teil C“ statt Abschnitt D.
4. Buchstaben der Teile doppelt belegt.
5. „`BACKLOG*.md` geht nicht mit“ falsch; beide liegen seit TB-118 in der Ablage.
6. Neigung unter der Überschrift „ohne Neigung“.

Dazu: beide übernommenen Blöcke `diff` rc 0. Kosten: Helfer rund 220 000 Tokens (eigene Zählung des Werkzeugs), ausserhalb dieses Chats. ⇒ Der Durchgang hat Befunde, die sonst übersehen worden wären.

**Offen, Reihenfolge:**
1. Fable 29b abwarten.
2. TB-122 vorbereiten: Platzhalter 0a, Zeiger, Sitzung anlegen.
3. `FABLE_ANTWORT_2026-09-27c_…` und `…29a_…` aus der Ablage ins Repo, md5 prüfen.
4. Indexzeilen in `FABLE_DIALOG_INDEX.md`.
5. E-2 nach der Antwort auf 29b.

**Berichtigung zum Nachtrag 12:25 (12:40):**
- Die erste Fassung von 29b (`e189f941…`, 31 946 B) war um die Tabellenzeile F-17 zu kurz. Ursache: Der Übernahmebereich der Sammlung war mit Z. 16–192 vorgegeben, die Datei hat 193 Zeilen.
- Der Gegenleser prüfte gegen denselben Bereich und konnte den Fehler nicht sehen.
- Gültige Fassung: **`bb6a9606…`, 32 597 B, 311 Zeilen**. Repo (eigene uncommittete Datei, ersetzt) und Ablage sind gleich; übergeben wurde nur diese Fassung.
- ⇒ **Regel:** Ein übernommener Block wird bis zu einer Grenze übernommen, die aus der Datei gemessen ist (Dateiende oder nächste Überschrift), nicht aus einer Zeilenzahl. Der Gegenleser bekommt die Grenze als Überschrift, nicht als Zeilennummer.

---

## Nachtrag 29.09.2026, 13:20 — Fable-Filter · 29b gekürzt (Fassung 2) · Gegenlesen Durchgang 2

**Betreiberfrage 12:45, wörtlich:** *„Da wir ein recht beschränktes fable Kontingent haben, müssen wir klar überlegen wie wir in diesem hiermit sinnvoll umgehen. Gebe mir hierzu eine Empfehlung aus wie Fable wirklich nur fable spezifische Tätigkeiten ausführt die wir in Opus nicht in dieser Qualität erreichen.“*

**Betreiberentscheide per Auswahlkarte, wörtlich:**
- „Wie soll das Fable-Kontingent künftig eingesetzt werden?“ ⇒ **„Filter + Vorprüfung + Form (Empfohlen)“**
- „Was passiert mit der Anfrage 29b?“ ⇒ **„Gekürzt senden (Empfohlen)“**

**Die Regel (Fable-Filter), Wortlaut für `ARBEITSWEISE.md` (neuer Abschnitt 22.11) und `UMZUG.md`, bei E-2 oder TB-122 einzuarbeiten:**

```
### 22.11 Fable-Filter — nur Verfahrensfragen, vorgeprüft (Betreiber 29.09.2026)

1. An Fable gehen nur Verfahrensfragen vor dem signierten Tag: Registertext,
   seine Lesart, der Sichtschutz (27). Handwerk nach 6d — Arbeitsweise, Ablage,
   Umzug, Agenten, Dateinamen, Lesarten eigener Werkzeuge — entscheiden der
   steuernde Chat und der Betreiber (Auswahlkarte). Reine Kenntnis geht nicht
   hin oder als eine Zeile.
2. Vorprüfung durch Opus (Mac-Sitzung oder Helfer nach 22.10): Jede Frage wird
   vorher gegen das ganze Register und den Code geprüft. Fable bekommt nur, was
   dort offen ist — je Frage mit Fundstelle und Neigung des steuernden Chats.
3. Form: nur Fragen mit Fundstellen, keine kopierten Sammlungen; Antwort je
   Frage „einverstanden“ oder „anders, weil …“, Registertext nur als R-Block;
   „In einfacher Sprache“ schreibt der steuernde Chat.
4. Takt nach Bedarf: wenn eine Frage einen Auftrag blockiert oder genug echte
   Verfahrensfragen beisammen sind — nicht täglich.
5. Fables Probe aus 29a (Register Teil 1–3 über einen Fundstellen-Helfer) wird
   unterstützt; die Übergabe an einen neuen Fable-Chat nennt sie.
```

Warum (gemessen bzw. aus den Antworten):
- Fable schätzt sein Anfangswissen je Chat auf etwa 350 000 Tokens (29a).
- 29a war nach seinem eigenen Satz „alles Handwerk“.
- In 29b Fassung 1 waren Teil 1 B, C und drei der vier Punkte in D Handwerk oder Kenntnis.
- Die 39 TB-121-Fragen waren nicht gegen Register 13–46 vorgeprüft.

**29b, Fassung 2:** `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-29b_erzeuger_und_kalter_leser.md`, md5 `0d69a243…`, 13 828 B, 146 Zeilen.
- Inhalt: F-1 … F-17 samt Neigungen (Sammlung von der Überschrift „27.09., TB-120: …“ bis zum Dateiende, zeichengleich) und die Frage KL (kalter Leser, bisher „78“).
- Fassung 1 (`…29b_tagesanfrage_sammlung_erzeuger_kalter_leser.md`, `bb6a9606…`) stand im Chat als Kopierblock bereit, ging aber **nicht** an Fable. Sie ist im Repo umbenannt und ersetzt (eigene uncommittete Datei) und aus der Ablage entfernt. Berichtigt damit die Zeile „Als Kopierblock übergeben“ im Nachtrag 12:25.
- Kopie von Fassung 1 nur im Brücken-Arbeitsordner (kein Träger); Inhalt vollständig beschrieben im Nachtrag 12:25.

**Gegenlesen, Probe Durchgang 2 von 3:** Der Helfer fand 7 Befunde in den neuen Teilen, alle berichtigt:
1. Protokollzeile fehlte erneut. Derselbe Fehler wie in Durchgang 1, meiner.
2. „blockieren E-2 … E-9“ zu pauschal (E-3/E-8 nur zum Teil, E-9 an T117-5).
3. „Fassung 1 nicht übergeben“ missverständlich.
4. Nummer 78 kollidierte mit Befund 78 in TB-121.
5. „ohne Neigung“ im Block unerklärt.
6. Verweise auf Belege und auf TB-121, die nicht in der Ablage liegen.
7. Eine leere Ankündigung „als Kenntnis“.

Mechanik: `cmp` rc 0. 27.1: keine Verdachtsfälle. ⇒ Stand der Probe: 2 von 2 Durchgängen mit Befunden, die sonst übergeben worden wären.

**Offen aus der Sammlung, jetzt beim steuernden Chat und beim Betreiber (Handwerk, per Karte):**
- TB-118 B1–B9;
- TB-119 Nr. 1–3;
- 19/6 gegen 6d (Neigung: 6d gilt);
- 27.4 bei `MAC_TB-119` (Neigung: nur Fundstelle, Zeile per Muster).

**Neu offen: Vorprüfung der 39 TB-121-Fragen gegen Register 13–46** (Helfer oder Mac-Sitzung, nur lesend). Danach gehen nur die offenen an Fable.

---

## Umzug 29.09.2026, 14:00 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

*Geschrieben vom steuernden Chat (seit 29.09., 07:26). Anlass des Umzugs: die Umzugsampel des Chats, geschätzt rund 290 000 Tokens (Schwelle 🔴 300 000). ⚠️ **Ausnahme von UMZUG 3:** Zwei Dateien sind uncommittet (Block 2). Sie liegen auf dem Mac und in der Ablage; Schritt 0 von TB-122 committet sie. Gemessen heisst über die Geräteanbindung heute gemessen.*

### Block 1 — Stand in drei Zeilen

- **Fertig heute:**
  - TB-121 (kalter Leser Register 0–12): Abgabe `04f07ef`, per Wächter geschlossen.
  - Fable 27c (R18–R32), 29a (Umzugstakt, Ampel, Agenten, alles Handwerk) und **29b (R33–R52)** sind beantwortet und liegen in der Ablage.
  - Neue Regeln per Betreiberkarte: Umzugsampel, Helfer-Agenten, Fable-Filter (Nachträge 07:55, 09:20, 13:20).
- **Läuft:** nichts. Keine Mac-Sitzung (Wächter 07:14Z: 0 übrig).
- **Als Nächstes:**
  1. TB-122 anlegen (E-1, freigegeben).
  2. 27c, 29a und 29b ins Repo abschreiben.
  3. 29b bewerten.
  4. E-2 vorbereiten (Registerauftrag mit R18–R52), Freigabe per Karte.

### Block 2 — HEAD und Commits

- **HEAD `04f07ef`** (TB-121 Abgabe, 09:00 Ortszeit), Zweig `main`, gemessen. Commits heute: `86e0d5e` (TB-121 Schritt 0), `04f07ef`.
- **Uncommittet, gemessen:**
  - `docs/projektfuehrung/UEBERGABE.md` (geändert, nur angehängt; numstat gegen HEAD mit 0 entfernten Zeilen).
  - `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-29b_tagesanfrage_sammlung_erzeuger_kalter_leser.md` (neu, md5 `bb6a9606…`). **Das ist die an Fable gesendete Fassung** (Fable 29b nennt sie).
- Nicht im Repo und nicht zu committen: `logs/auftraege/NICHT_GESENDET_FABLE_ANFRAGE_2026-09-29b_erzeuger_und_kalter_leser.md` (Fassung 2, nie gesendet, gitignoriert).

### Block 3 — Tragende Zahlen

| | Wert | Fundstelle |
|---|---|---|
| Register | 0–46, sha256 `18e39ee2…`, unverändert | TB-121 Z. 3, gemessen |
| Gültiges Abbild | `sperrliste_abbild_2026-09-26_tb117.json` `46f0ad5d…` | TB-119 A2 |
| Snapshot / Datenstand / Benchmark | `63e4b6c8…` / `d9449faf…` / `64fb2912…` | Register 18, 39.2 |
| Ablage | 50 Dateien; `knowledge_size` 745 654 (37 %) um 12:23, danach +29b-Antwort und Fassung-Tausch | gemessen |
| Nummern | TB frei ab **123** · Journal frei ab **DU** (TB-121 schrieb DT) · R-Blöcke frei ab **R53** · Fable-Anfrage frei ab **29c** bzw. am nächsten Tag **a**; Antwortbuchstaben 29a/29b vergeben | gemessen / aus Antworten |

### Block 4 — Offene Punkte, in Reihenfolge

1. **TB-122 (E-1, Posten 3)** ist freigegeben (Karte 27.09., ca. 20:20).
   - Vorher im Auftrag `docs/auftraege/MAC_TB-122_posten3_achsen_durchreichen.md`, Z. 47, den Platzhalter `<<ERWARTET_0A>>` durch die gemessene `git status --short`-Liste ersetzen: die zwei Dateien aus Block 2, dazu alles, was bis zum Start noch abgelegt wird.
   - `docs/auftraege/AKTUELLER_AUFTRAG.md` bekommt eine Zeile TB-122; vorher lesen (98 Zeilen, Tabelle ab etwa Z. 39).
   - Dann `starte_TB-122` und den Einfügesatz ausgeben.
2. **27c, 29a und 29b aus der Ablage ins Repo abschreiben** (`docs/projektfuehrung/`), möglichst **vor** dem Start von TB-122, damit Schritt 0 sie mitnimmt. Die Liste in 0a entsprechend setzen. md5 gegen die Ablage ist nicht möglich (das Werkzeug liefert nur Text); das so vermerken.
   - ⚠️ 29b hat rund 70 000 Zeichen. Nicht im Chat lesen, sondern per Helfer.
3. **29b bewerten.** Kern nach Helferauszug:
   - Die Sammlung ist als Handwerk entschieden und deckt sich weitgehend mit den Neigungen:
     - B4: B6 gilt.
     - B5: „zwei jüngste Anfrage-Tage“; `ablage_soll.py` nachziehen.
     - B6: Austritt nach Wortlaut (Annahme).
     - 19/6: 6d gilt; K2h umformulieren, K2f nach PRUEFPRINZIPIEN Reihe C, Nummer messen (Fable vermutet C9).
     - TB-119 Nr. 1–3 wie Neigung.
     - 27.4: Aufträge nennen Streichwerte nur per Muster.
   - F-1 … F-17 sind in R33–R47 beantwortet, F-16 als Handwerk.
   - Die 39 Fragen des kalten Lesers sind in R48–R51 beantwortet. Die Vorprüfung gegen Register 13–46 **entfällt**, Fable hat alle beantwortet.
   - Frage 78: TB-121 trägt als Untergrenze. Künftige kalte Leser laufen ohne Gedächtnis, mit Beleg in Schritt 0.
   - R52 ist eine Tatsachennotiz.
   - Zur Bewertung gehören: Indexzeilen in `FABLE_DIALOG_INDEX.md` für 27c, 29a und 29b sowie der Backlog- und Journal-Nachtrag (ARBEITSWEISE 5b).
4. **E-2, der Registerauftrag.**
   - R18–R52 zeichengleich eintragen, jeder Block mit Marken.
   - **Vorher messen**, was Fable als Voraussetzung nennt:
     - R25 (Docstring `auswertung.py` „unter dem Modus“), R26 (`--bot` unter dem Modus), R28 (Probe in `snapshot.py`);
     - R33 (Feld für die Trade-Zahl im Vertrag), R36/R48 (d) (`mittlere_exposure`, `mtm_kern.py`), R41 (Haltedauer TB-24: Kerzenzahl oder Zeitdifferenz);
     - R48 (c), (f), (g) (`auswertung.py`: Spitze, `markierungen`, Perzentil), R48 (i) (`pruefe_grenzsaetze.py`).
   - Messbitten: R49 (b) (Quantil-Stufen), R50 (34 Grenzsätze; Kennzahlen-Tatsachennotizen je Datei und Bezeichner).
   - Weicht eine Messung ab, wird sie gemeldet, nicht eingetragen.
   - **Freigabe: Registertext ist Einzelfreigabe**, also Karte an den Betreiber.
   - In denselben Auftrag oder direkt danach die Regelwerksnachträge:
     - ARBEITSWEISE 22.10 (Helfer), 22.11 (Fable-Filter), Abschnitt 0 (Ampel, Gegenleser);
     - UMZUG 3 (Auslöser 6, Ampel) und 6 (Eröffnung mit Kernlektüre);
     - die Regeln aus Block 7 unten und aus dem Umzugsblock vom 07:15 (Nr. 1, 5, 6), Fables 29a Abschnitt 1–3, K2h/K2f, die drei Trägerstellen (TB-119 Nr. 2);
     - kalter Leser ohne Gedächtnis; Backlog K4s und K4t.
5. **Fable-Umzug** nach E-2 (Fables Ampel: 🟡, rund 380 000, einmal verdichtet). Die Übergabe-Vorlage vom 29.09. braucht nur Abschnitt 6 und 7 neu (Fable 29b, Ampelzeile).
6. Später:
   - E-3 … E-9 nach TB-120 Abschnitt 5 und der Reihenfolge aus R44 (E-1, dann E-6, dann E-3/E-4);
   - Posten 5 des Plans nach R43 neu fassen;
   - Leiter-Skript und Stufe IV;
   - Öffnung von `paths.py` (T117-5, E-9).

### Block 5 — Wartezustände

| wartet | auf |
|---|---|
| TB-122 | Platzhalter 0a, Zeiger, Auslöser (steuernder Chat), dann Abschicken des Satzes (Betreiber) |
| E-2 | Bewertung von 29b, Vormessungen, Freigabekarte |
| Fable | nichts offen. Die nächste Anfrage erst nach E-2 und nach dem Fable-Filter (nur Verfahrensfragen, vorgeprüft) |
| Betreiber | Speicher-Export des alten Projektspeichers, Frist 29.09.; ob erledigt, ist nicht gemessen |

### Block 6 — Freigaben

- **Nicht verbraucht:** TB-122 (Karte 27.09., ca. 20:20, wörtlich im Auftrag).
- **Heute entschieden, per Karte:**
  - T116-5/R24: „(a) So lassen“.
  - Umzug nach Tokenverbrauch und Kernlektüre.
  - Helfer: ein Regelwerk für alle drei Rollen; Ampel im steuernden Chat.
  - Fable-Filter; 29b „gekürzt senden“ (überholt, weil Fassung 1 schon bei Fable war).
- **Nicht freigegeben:** E-2 (Register), E-3 … E-9, jede Öffnung von `herkunft.py`, `paths.py`, `zuteilung.py` und `auswertung.py`.
- **Sperrliste:** 14 Punkte, unverändert. Kein neues Abbild vor dem nächsten Bündel.

### Block 7 — Fehler dieses Chats und die Regeln daraus

| # | Fehler | ⇒ Regel |
|---|---|---|
| 1 | 29b Fassung 1: Die Zeile F-17 fehlte, weil der Übernahmebereich als Zeilenzahl (16–192) vorgegeben war; der Gegenleser prüfte gegen denselben Bereich | Übernahmegrenzen werden aus der Datei gemessen (Überschrift, Dateiende). Der Gegenleser prüft gegen die **Quelle**, nicht gegen den Bereich (so auch Fable 29b, Teil 0 Nr. 4, B3-Klasse) |
| 2 | Angekündigte Protokollzeile zweimal vergessen, einmal falsche Herkunft einer Regel (Fable 29a statt Betreiber 09:20); beides fand der Gegenleser | Gegenlesen bleibt; Probe 2 von 2 mit Befunden. Durchgang 3 ist die nächste Übergabe |
| 3 | In der Übergabe erst „als Kopierblock übergeben“, dann „nicht übergeben“ geschrieben; beides war eine Annahme über das Handeln des Betreibers | Was der Betreiber abgeschickt hat, wird nicht behauptet. Richtig ist „als Kopierblock ausgegeben“; ob gesendet, zeigt erst die Antwort. Vor einer Karte, die einen versendeten Stand ändern will, zuerst fragen, ob schon gesendet |
| 4 | Fables 70 000 Zeichen grosse Antwort 29b direkt in den Chat gelesen (rund 20 000 Tokens), dadurch Umzug früher als nötig | Grosse Ablage-Dateien liest ein Helfer (Fundstellen). Der Chat liest nur, was er für eine Entscheidung im Wortlaut braucht |
| 5 | TB-121 lag 57 min unabgeschickt; die Nachschau fand keinen Commit, die Erinnerung ging raus, danach lief die Sitzung | So richtig (Regel 5 vom Umzug 07:15). Kein neuer Fehler, bestätigt |

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Die zwei uncommitteten Dateien aus Block 2 gehen mit Schritt 0 von TB-122 ins Repo.
- Die Regeltexte der Nachträge 07:55, 09:20 und 13:20 sind noch nicht in `ARBEITSWEISE.md` und `UMZUG.md` (siehe Block 4 Nr. 4). Die Erinnerung (`preferences.md` des Projekts) trägt sie schon.
- Fable 27c, 29a und 29b liegen nur in der Ablage (Block 4 Nr. 2).
- `FABLE_UEBERGABE_2026-09-29_neuer_chat.md` liegt nur in der Ablage (nicht von diesem Chat). Prüfen, ob die Datei ins Repo gehört (Fable-Übergaben sind Vorgangsdokumente, B6).

### Block 9 — Eröffnungstext

Die Kernlektüre ist Betreiberentscheid (Nachtrag 07:55), in `UMZUG.md` Abschnitt 6 aber noch nicht eingearbeitet. Für diesen Umzug gilt der Text, den der steuernde Chat im Chat als Kopierblock ausgibt: Kernlektüre = **dieser Block** + ARBEITSWEISE Abschnitt 0 + UMZUG Abschnitt 3 + die Erinnerung. Die Einarbeitung in UMZUG 6 folgt mit E-2.

**Stehende Pflichten:**
- Umzugsampel als letzte Zeile jeder Antwort.
- Helfer-Agenten nach 22.10, Gegenleser vor jeder Übergabe.
- An Fable nur vorgeprüfte Verfahrensfragen (22.11).
- Sonst unverändert wie im Umzugsblock 07:15, Block 9: Auslöser, Nachschau, Karten, Sicherheitsregeln, kein `git status`/`add`/Commit über die Brücke.

**Nachtrag zum Umzugsblock, 14:05: Sonnet 5.5.** Betreiberfrage 13:46, wörtlich: *„Wäre es sinnvoll einen teil der Aufgaben auch noch an Sonet5.5 auszulagern? Dies aber ausdrücklich nur wenn die Qualität des Projektes darunter nicht leidet?“* Karte, wörtlich: „Sollen Teile der Arbeit an Sonnet 5.5 gehen?“ ⇒ **„Nur Mechanik, erst Probe (Empfohlen)“**.

Das heisst:
- Sonnet übernimmt Fundstellen- und Zählhelfer (Agent mit `model: sonnet`) und reine Dokumentationsaufträge mit wörtlich vorgegebenem Text.
- Zuerst läuft **ein** Probeauftrag, abgenommen mit numstat, `diff` gegen den Auftragstext und der Zahl der Treffer je Einfügestelle. Hält er, wird es Regel für diese Klasse.
- Register, Code, Messungen, Gegenleser, Bewertung und steuernder Chat bleiben Opus mit Aufwand hoch.
- Kandidat für die Probe: der Regelwerksnachtrag aus Block 4 Nr. 4, getrennt vom Registerteil von E-2.
- Einzuarbeiten als ARBEITSWEISE 22.12 und Abschnitt 3 (Modellwahl), zusammen mit 22.10/22.11.
- **Ergänzung 14:10:** Es gibt **keinen eigenen Sonnet-Chat**; Betreiber 14:06 fragte nach einem Eröffnungstext, der steuernde Chat hat verneint, mit Begründung. Sonnet läuft nur (a) als Helfer (Agent mit `model: sonnet`), mit allem Nötigen im Helferauftrag, und (b) als Mac-Sitzung je Auftrag, mit dem Modell im Kopf des Auftrags (ARBEITSWEISE 3). Umzug und Ampel betreffen beide nicht. ⚠️ **Lücke:** `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` startet `claude --effort high --remote-control` ohne Modellwahl, also mit Opus. Vor der Sonnet-Probe prüfen (`claude --help`), ob es einen Modellschalter gibt, und den Wächter je Auftrag steuerbar machen. Das ist Handwerk mit Freigabe, weil der Wächter geändert wird.
- **Ergänzung 14:15, „zukünftig“ (ARBEITSWEISE 15):** Betreiber 14:10, wörtlich: *„Schicke mir zukünftig immer den Text der Übergabe für den neuen Chat als erste Nachricht direkt im laufenden Chat zum kopieren“*. Bei jedem Umzug geht der Eröffnungstext als **erste** Nachricht im laufenden Chat raus, als Kopierblock in einer eigenen Nachricht vor allen Erläuterungen. Einzuarbeiten in `UMZUG.md` Schritt 6 und in ARBEITSWEISE Abschnitt 0 („Wenn ein Arbeitsabschnitt endet“), zusammen mit E-2 oder der Sonnet-Probe. Erinnerung: eingetragen.


---

## Nachtrag 29.09.2026, 14:52 — neuer steuernder Chat: Übernahme, Abschriften, TB-122 gegengelesen und ausgelöst

*Geschrieben vom steuernden Chat seit 29.09.2026, 14:11. Gemessen heisst über die Geräteanbindung heute gemessen.*

- **Übernahme gemessen 14:12:** HEAD `04f07ef`, `BACKLOG.md` 220 Zeilen, Arbeitsbaum wie im Umzugsblock 14:00, Block 2.
- **Aus der Ablage ins Repo abgeschrieben** (`docs/projektfuehrung/`, uncommittet, TB-122 Schritt 0 nimmt sie mit):

| Datei | Bytes | md5 |
|---|---|---|
| `FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md` | 48 420 | `ff96392ed654fdcae2e991e51e424dc5` |
| `FABLE_ANTWORT_2026-09-29a_betreiberentscheid_umzugstakt_ampel_agenten.md` | 6 250 | `52b6b7f609df6dcb0ee64c58884d75aa` |
| `FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md` | 73 703 | `898d5bd53b6617209b7ce4f7e8992941` |
| `FABLE_UEBERGABE_2026-09-29_neuer_chat.md` | 21 705 | `c2bfca14a12064213a59f32e05125f70` |

  Verfahren: je Datei zwei unabhängige Abschriften durch Helfer, `cmp` rc 0. ⚠️ Bytegleichheit mit der Ablage ist **nicht messbar**: Das Werkzeug liefert nur Text; geschützte Leerzeichen und U+FE0F sind darin nicht unterscheidbar (0 × U+00A0 in allen vier Dateien). Eine dritte Abschrift von 29b brach mittendrin ab (18 987 B) und ist verworfen.
- **Gegenlesen, Probe Durchgang 3 von 3** (TB-122 gegen 27c, 29b und das Register): Befunde 7 abweichend, 21 berührt, 3 veraltet. Vor dem Auslösen eingearbeitet (numstat im Auftrag):
  1. Fable-Stand statt „Kein Fable bis Dienstag“;
  2. Fundstelle des Vorbilds `rsi2_crypto` (`docs/belege/TB-120/c_bestand.md`, C4);
  3. Fundstelle des Sollwerts `register()` (`ERGEBNIS_TB-117`, Zeile F);
  4. neuer Schritt B4 nach R43: In `multi_symbol_optimise.py` nur die Funktionen, die `collect_all_trades` importiert; `evaluate_combination_multi` bleibt unverändert;
  5. Überschrift C berichtigt: 24c / 41.2 B4 verlangt einen Modus-Lauf;
  6. Entwurf der Tatsachennotiz nach 37.3 (Auftrag, Freigabe, Commit, Form 46.11) und R47.
  ⇒ **3 von 3 Durchgängen mit Befunden, die sonst übergeben worden wären: Das Gegenlesen wird Regel** (Nachtrag 09:20, Probe). Einzuarbeiten mit E-2.
- **Betreiberentscheid per Auswahlkarte, ca. 14:52:** „TB-122 soll je Bot eine neue Testdatei `test_posten3_durchreichung.py` anlegen … Freigabe erweitern?“ ⇒ **„Ja, bis 3 Testdateien (Empfohlen)“**. Steht wörtlich im Auftrag.
- **Fehler dieses Chats mit Regel:** Die Kernlektüre wurde über `project_read` gelesen. Das liefert immer die ganze Datei; `UEBERGABE.md` und `ARBEITSWEISE.md` kamen vollständig in den Chat, rund 190 KB statt 40 KB. ⇒ **Die Kernlektüre wird künftig mit Abschnittsfilter aus dem Repo über die Geräteanbindung gelesen** (etwa `awk` ab der letzten `## `-Überschrift). Einzuarbeiten in UMZUG 6 mit E-2.
- **Nummern:** TB frei ab **123**, sonst wie im Umzugsblock 14:00, Block 3.
- **Als Nächstes:** TB-122 läuft nach dem Abschicken des Satzes. Danach 29b bewerten (Indexzeilen 27c/29a/29b, Backlog- und Journal-Nachtrag), dann E-2 mit Freigabekarte.


---

## Nachtrag 29.09.2026, 20:35 — TB-122 und TB-123 abgegeben, Bote pausiert, Index nachgezogen

*Geschrieben vom steuernden Chat. Gemessen heisst über die Geräteanbindung heute gemessen.*

**Stand:** HEAD **`0034960`** = `origin/main`, Arbeitsbaum sauber bis auf `UEBERGABE.md` (dieser Nachtrag) und `FABLE_DIALOG_INDEX.md`. Keine Mac-Sitzung (TB-123 um 20:34 per `schliesse_0034960…` beendet, 1 mit TERM, 0 übrig).

- **TB-122 (E-1, Posten 3), abgegeben mit `b116878`:** Achsen durchgereicht (`ab31314`, 7 Dateien, numstat 63/17; nach R43 `evaluate_combination_multi` und `load_all_symbol_data` unverändert) · C1 13/13 bytegleich · C2 Wertprobe 16/16, 12/12, 12/12, Gegenprobe rc 1 · C4 Trockenlauf 18/18 zeichengleich · C5 Sonde vorher = nachher, `register()` unverändert `01f5997a…`. Die Sitzung TB-122 endete nach 16:12 ohne Abgabe; Ursache nicht gemessen.
- **TB-123 (Abschluss TB-122):** `dca3096`, `68eb778`, `b116878`, `0034960`. C3 **50 von 52 gleich**. Abweichungen: ⚠️ `test_sync_check` 33/0 ⇒ 30/3, **Folge von `ab31314`** (`research/sync_check/sync_table.py` erkennt `BB_LOOKBACK`/`BB_SQUEEZE_PERCENTILE` nicht mehr als Voreinstellung von `run_backtest()`, Beleg `docs/belege/TB-123/a3_sync_probe.txt`); `test_kursdaten` nur Bezugspunkt `origin/main`, kein Befund. Vier Tests rot auf beiden Seiten (unverändert).
- **Befunde aus TB-122 (`befunde.txt`, Ergebnis Abschnitt 5):** F1 Scanbeginn der Breakout-Bots hängt an `WARMUP_PERIOD` (126) in `backtest_breakout.py`, nicht an `bb_lookback` · F2 `vorlauf_balken` in `faltenplan_neun.py` fest, nach Posten 3 bei `rsi2_mean_reversion` achsenabhängig (Stufen bis 252) · F3 `SMA_TREND_PERIOD` doppelt, nicht in `live_params.py` · **F4 Sonde kann Punkt 11 nicht prüfen; Hash-Übergang der sieben Dateien nur im Commit und im Entwurf der Tatsachennotiz**. F1, F2, F4 sind Kandidaten für die Vorprüfung nach dem Fable-Filter (22.11).
- **Reste für den nächsten Mac-Auftrag (Handwerk ohne Sperrlistennähe, pauschal frei seit 26.09.):** (1) `research/sync_check/sync_table.py` so nachziehen, dass `test_sync_check` wieder 33/0 zeigt, ohne den Test zu schwächen · (2) die zwei Worktrees `$TMPDIR/tb123_vorher` und `$TMPDIR/tb123_vorher2` entfernen (`git worktree remove --force`, sie verknüpfen auf echte Datenbanken; vorher prüfen, dass nur Verknüpfungen gelöscht werden) · (3) Datenstand messen (Soll `d9449faf…`, 223 Dateien) — in TB-123 **nicht gemessen**, siehe Fehler unten.
- **Betreiberentscheid per Auswahlkarte, ca. 15:38:** „Der stündliche „Bote“ … Was soll mit ihm passieren?“ ⇒ **„Pausieren (Empfohlen)“**. Geplante Aufgabe `trig_017e7DNBCBRuzXVt9KtHqpkB` deaktiviert, nicht gelöscht. Grund: 24 Opus-Läufe am Tag, doppelt zu den Nachschauen des steuernden Chats, und Teil A/B committen über die Brücke (Widerspruch zur Sicherheitsregel).
- **Index nachgezogen:** `FABLE_DIALOG_INDEX.md` 49 Zeilen, `--pruefen` rc 0; neu 22f, 25f, 27c, 29a, 29b (Handfelder aus den Blöcken **Kurz:**).

**Fehler dieses Chats mit Regel:**

| # | Fehler | ⇒ Regel |
|---|---|---|
| 1 | Die gegengelesene Fassung von `MAC_TB-123` (7 580 B, md5 `fa4c6a72…`) kam **nicht** auf dem Mac an; `device_commit_files` schrieb die erste Fassung (6 191 B, md5 `2c906298…`), obwohl die Datei davor lokal geändert war. Ich habe nach dem Ablegen nicht verglichen. Folgen: TB-123 lief ohne die sechs Gegenleser-Befunde — kein Datenstand-Schritt, Abschnitt „Abschluss“ als 10 hinter „In einfacher Sprache“, `porcelain` als Datei mit Zusatz-Commit. Das Skript-Problem im Worktree hat die Sitzung selbst gelöst | ⭐ **Nach jedem `device_commit_files` md5 und `wc -c` auf beiden Seiten, vor dem Auslöser** (stehende Regel aus UEBERGABE_2026-09-24 Block 8, hier nicht befolgt). Eine überarbeitete Fassung wird unter **neuem Stage-Pfad** bereitgestellt, nicht unter dem alten |
| 2 | Die Übergabe nannte TB-123 „unter der Freigabe von TB-122“; das trug, weil kein Code geändert wurde | — |

**Nummern:** TB frei ab **124** · Journal frei ab **DV** · R-Blöcke frei ab R53 · Fable-Anfrage frei ab **29c** bzw. am nächsten Tag **a**.

**Als Nächstes:** (1) E-2 vorbereiten: Registertext R18–R52 zeichengleich, Vormessungen nach 29b (R25, R26, R28, R33, R36/R48 (d), R41, R48 (c)(f)(g)(i)), Messbitten R49 (b)/R50, Tatsachennotiz TB-122 (Entwurf Ergebnis Abschnitt 6), Regelwerksnachträge (22.10 jetzt Regel, 22.11, 22.12, UMZUG 3/6, Kernlektüre mit Abschnittsfilter, Eröffnungstext als erste Nachricht) · Freigabe Registertext per Karte · (2) die drei Reste oben · (3) Backlog- und Journal-Nachtrag zu 27c/29a/29b (Bewertung).


---

## Umzug 29.09.2026, 20:48 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

*Geschrieben vom steuernden Chat (seit 29.09., 14:11). Anlass: Betreiberentscheid per Auswahlkarte, ca. 20:48: „E-2 … ist ein mehrstündiger Block. Wann soll der steuernde Chat umziehen?“ ⇒ **„Jetzt, vor E-2 (Empfohlen)“**; Ampel des Chats geschätzt rund 175 000 Tokens. „Gemessen“ heisst über die Geräteanbindung heute gemessen. ⚠️ Ausnahme von UMZUG 3: zwei Dateien sind uncommittet (Block 2), der nächste Schritt 0 nimmt sie mit.*

### Block 1 — Stand in drei Zeilen

- **Fertig heute:** TB-121 (kalter Leser) · Fable 27c, 29a, 29b und `FABLE_UEBERGABE_2026-09-29_neuer_chat.md` im Repo (je zwei unabhängige Helfer-Abschriften, `cmp` rc 0; Bytegleichheit mit der Ablage nicht messbar) · **TB-122 (E-1, TB-30b Posten 3)** abgegeben über den Abschlussauftrag **TB-123** (`b116878`): drei Achsen bis zur Indikatorberechnung durchgereicht, C1 13/13 bytegleich, C2 Wertprobe mit Gegenprobe, C3 50/52 gleich, C4 18/18, C5 Sonde vorher = nachher · `FABLE_DIALOG_INDEX.md` 49/49, `--pruefen` rc 0 · Bote pausiert · neue Regeln per Karte (Block 6).
- **Läuft:** nichts. Keine Mac-Sitzung (TB-123 um 20:34 per `schliesse_0034960…`, 0 übrig). Keine Nachschau geplant.
- **Als Nächstes:** **E-2** vorbereiten (Block 4 Nr. 1), Freigabe Registertext per Karte.

### Block 2 — HEAD und Commits

- **HEAD `0034960` = `origin/main`**, Zweig `main`, gemessen.
- Commits heute: `86e0d5e`, `04f07ef` (TB-121) · `c064405`, `ab31314`, `08153e4` (TB-122) · `dca3096`, `68eb778`, `b116878`, `0034960` (TB-123).
- **Uncommittet, gemessen:** `docs/projektfuehrung/UEBERGABE.md` (nur angehängt, numstat gegen HEAD mit 0 entfernten Zeilen) · `docs/projektfuehrung/FABLE_DIALOG_INDEX.md` (6/1, erzeugt von `dialog_index.py --handfelder`, `--pruefen` rc 0).
- ⚠️ Auf dem Mac liegen zwei nicht entfernte Worktrees von TB-123: `$TMPDIR/tb123_vorher`, `$TMPDIR/tb123_vorher2` (verknüpfen auf echte Datenbanken). Siehe Block 4 Nr. 2.

### Block 3 — Tragende Zahlen

| | Wert | Fundstelle |
|---|---|---|
| Register | 0–46, sha256 `18e39ee2…`, unverändert | TB-121/TB-122 ändern es nicht |
| Gültiges Abbild | `sperrliste_abbild_2026-09-26_tb117.json` `46f0ad5d…`, Sonde 37/0/0 | TB-122 0b/C5 |
| `herkunft.register()` | `01f5997a…`, vor und nach TB-122 | `ERGEBNIS_TB-117` Zeile F; TB-122 C5 |
| Snapshot / Datenstand / Benchmark | `63e4b6c8…` / `d9449faf…` (223 Dateien) / `64fb2912…` | Register 18, 39.2. ⚠️ Datenstand in TB-123 **nicht** gemessen |
| Laufbereich / Zellen | 81 Module / 2 416 | Register 44-8 / Abschnitt 3 |
| Fable-Abschriften (md5) | 27c `ff96392e…` · 29a `52b6b7f6…` · 29b `898d5bd5…` · Fable-Übergabe `c2bfca14…` | Nachtrag 14:52 |
| Ablage | 50 Dateien; `knowledge_size` zuletzt 745 654 (37 %) um 12:23, seither nicht neu gemessen | — |
| **Nummern** | TB frei ab **124** · Journal frei ab **DV** · R-Blöcke frei ab **R53** · Fable-Anfrage frei ab **29c** bzw. am nächsten Tag **a** | gemessen |

### Block 4 — Offene Punkte, in Reihenfolge

1. **E-2, Registerauftrag** (Register ist Einzelfreigabe ⇒ Karte). Inhalt:
   - R18–R52 zeichengleich mit Marken (Quelle: 27c, 29b im Repo);
   - **Vormessungen**, die Fable als Voraussetzung nennt: R25 (Docstring `auswertung.py` „unter dem Modus“), R26 (`--bot` unter dem Modus), R28 (Probe in `snapshot.py`), R33 (Feld Trade-Zahl im Vertrag), R36/R48 (d) (`mittlere_exposure`, `mtm_kern.py`), R41 (Haltedauer TB-24), R48 (c)(f)(g)(i). Messbitten R49 (b), R50. Weicht eine Messung ab: melden, nicht eintragen;
   - Tatsachennotiz TB-122 nach 37.3 (Entwurf: `ERGEBNIS_TB-122`, Abschnitt 6) samt Befund F4 (Sonde prüft Punkt 11 nicht);
   - **Regelwerksnachträge** (Wortlaute in den UEBERGABE-Nachträgen 07:55, 09:20, 13:20 und im Umzugsblock 14:00): ARBEITSWEISE 22.10 (Helfer; **Gegenleser ist Regel**, Probe 3/3), 22.11 (Fable-Filter), 22.12 (Sonnet nur Mechanik; Lücke: Wächter hat keinen Modellschalter), Abschnitt 0 (Ampel, Gegenleser, Umzug nach Tokens, Eröffnungstext als erste Nachricht); UMZUG 3 (Auslöser 6, Ampel) und 6 (Eröffnungstext unten, Block 9); die Regeln aus den Blöcken 7 (07:15 Nr. 1, 5, 6; 14:00; unten); K2h/K2f; die drei Trägerstellen (TB-119 Nr. 2); kalter Leser ohne Gedächtnis; Backlog K4s, K4t;
   - Backlog- und Journal-Nachtrag zur Bewertung von 27c/29a/29b (ARBEITSWEISE 5b);
   - Registerkopie Teil 1–4 neu erzeugen, danach Ablage-Abgleich (UMZUG 4).
   - Vor dem Übergeben: Gegenleser. Nach dem Ablegen: md5 auf beiden Seiten.
2. **Reste aus TB-122/123** (Handwerk ohne Sperrlistennähe, pauschal frei seit 26.09.): `research/sync_check/sync_table.py` nachziehen, bis `test_sync_check` wieder 33/0 zeigt (Test nicht schwächen; Beleg `docs/belege/TB-123/a3_sync_probe.txt`) · die zwei Worktrees entfernen · Datenstand messen. Am besten in Schritt 0 von E-2 oder als kleiner eigener Auftrag davor.
3. **Vorprüfung nach dem Fable-Filter** für die TB-122-Befunde F1 (Scanbeginn Breakout an `WARMUP_PERIOD` 126), F2 (`vorlauf_balken` in `faltenplan_neun.py` nach Posten 3 achsenabhängig), F4. Nur was danach Verfahrensfrage bleibt, geht an Fable.
4. **Fable-Umzug** nach E-2 (Fables Ampel 🟡, ~380 000).
5. Später: E-6 (Posten 4), dann E-3/E-4 (R44) · Posten 5 neu fassen (R43) · Leiter-Skript, Stufe IV · Öffnung `paths.py` (T117-5, E-9).

### Block 5 — Wartezustände

| wartet | auf |
|---|---|
| E-2 | Vorbereitung durch den steuernden Chat, dann Freigabekarte |
| Fable | nichts offen; nächste Anfrage erst nach Vorprüfung (Block 4 Nr. 3) |
| Mac | nichts; keine Sitzung, kein Auslöser |
| Betreiber | Speicher-Export des alten Projektspeichers (Frist 29.09.); ob erledigt, ist nicht gemessen |

### Block 6 — Freigaben und Entscheide

- **Verbraucht:** TB-122 (Karte 27.09., ca. 20:20) samt Nachtrag „Ja, bis 3 Testdateien (Empfohlen)“ (29.09., ca. 14:52); TB-123 lief darunter ohne Codeänderung.
- **Pauschal frei:** Handwerk ohne Sperrlistennähe (Betreiber 26.09.).
- **Nicht freigegeben:** E-2 (Register), E-3 … E-9, jede Öffnung von `herkunft.py`, `paths.py`, `zuteilung.py`, `auswertung.py`.
- **Sperrliste:** 14 Punkte. TB-122 hat die sieben Dateien unter Punkt 11 geändert; kein neues Abbild (37.3 „nach Bündeln“); die Sonde prüft Punkt 11 nicht (F4).
- **Heute per Karte entschieden:** T116-5/R24 „(a) So lassen“ · Umzug nach Tokenverbrauch, Kernlektüre · Helfer ein Regelwerk für alle drei Rollen, Ampel · Fable-Filter · Sonnet nur Mechanik, erst Probe · TB-122 Testdateien · **Bote pausieren** (`trig_017e7DNBCBRuzXVt9KtHqpkB` deaktiviert, nicht gelöscht) · Umzug vor E-2.

### Block 7 — Fehler dieses Chats und die Regeln daraus

| # | Fehler | ⇒ Regel |
|---|---|---|
| 1 | Kernlektüre über `project_read` gelesen: liefert immer ganze Dateien (~190 KB statt ~40 KB) | Kernlektüre aus dem Repo mit Abschnittsfilter (`awk`); Ablage nur als Rückfall |
| 2 | `device_commit_files` schrieb die alte Fassung von `MAC_TB-123` (6 191 statt 7 580 B); nicht verglichen ⇒ Gegenleser-Befunde kamen nicht an | Nach jedem Ablegen md5 und `wc -c` auf beiden Seiten, **vor** dem Auslöser; überarbeitete Fassung unter neuem Stage-Pfad |
| 3 | Nach der Übernahmebestätigung auf ein Startzeichen gewartet; der Betreiber musste fragen „wie geht es nun weiter“ | Nach der Bestätigung in derselben Antwort mit dem ersten Handwerksschritt beginnen (ARBEITSWEISE 13); der Eröffnungstext sagt das jetzt ausdrücklich |
| 4 | Eine Helfer-Abschrift von 29b brach mittendrin ab (18 987 statt 73 703 B) | Abschriften aus der Ablage immer zweifach unabhängig, lange Texte in Teilen, `cmp` vor dem Ablegen |

**Weiter gültig aus den Blöcken 7 vom 07:15 und 14:00 (Kurzfassung):** Werkzeug-Erwartung im Auftrag nur mit Fundstelle · `schliesse_<HEAD>` erst ab 600 s · neue Fable-Antworten über `project_info` finden · `faltenplan.faltenplan()` ist kein Lesen · ohne Schritt-0-Commit einmal erinnern, dann warten · Ablage-Dateien übers Arbeitsverzeichnis mit md5 · Übernahmegrenzen aus der Datei messen, nicht als Zeilenzahl · nicht behaupten, was der Betreiber gesendet hat · grosse Ablage-Dateien per Helfer lesen · kein `git status`/`add`/Commit über die Brücke.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Die zwei uncommitteten Dateien aus Block 2 (nächster Schritt 0).
- Alle Regeltexte vom 29.09. stehen nur in UEBERGABE und Erinnerung, nicht in ARBEITSWEISE/UMZUG (Block 4 Nr. 1).
- Nichts in `logs/auftraege/` aus diesem Chat.

### Block 9 — Eröffnungstext

`UMZUG.md` Abschnitt 6 ist noch nicht nachgezogen. Für diesen Umzug gilt der folgende Text; er ist zugleich der Wortlaut für UMZUG 6 bei E-2:

```
Neue Sitzung zum Trading-Bot-Projekt (steuernder Chat). Das Projekt "Trading Bots" ist angehängt.

Prüfe als Erstes, ob du über die Geräteanbindung auf ~/trading-bot lesen kannst — nenne mir HEAD und die Zeilenzahl von docs/projektfuehrung/BACKLOG.md als Beleg. Wenn das nicht geht, sag es ausdrücklich, denn dann müssen wir Messungen wieder über mich laufen lassen.

Lies dann nur die Kernlektüre, aus dem Repo über die Geräteanbindung mit Abschnittsfilter (project_read liefert immer die ganze Datei — Regel vom 29.09.2026):
1. docs/projektfuehrung/UEBERGABE.md — nur den letzten Block, ab der Überschrift „## Umzug 29.09.2026, 20:48 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)“ bis Dateiende. Ältere Blöcke nur bei Bedarf.
2. docs/projektfuehrung/ARBEITSWEISE.md — nur Abschnitt 0 (von „## 0.“ bis vor „## 1.“).
3. docs/projektfuehrung/UMZUG.md — nur Abschnitt 3 (von „## 3.“ bis vor „## 4.“).
Nur wenn die Geräteanbindung fehlt: dieselben Stellen über den Projects-Zugriff (projektfuehrung/…).

Die Regeln vom 29.09. (Umzugsampel, Helfer-Agenten mit Gegenleser als Regel, Fable-Filter, Sonnet nur Mechanik, Eröffnungstext als erste Nachricht, Kernlektüre mit Abschnittsfilter, md5 nach jedem Ablegen) stehen in der Erinnerung und im letzten Übergabeblock; in ARBEITSWEISE und UMZUG sind sie noch nicht eingearbeitet — das ist Teil von E-2. PRUEFPRINZIPIEN.md (docs/PRUEFPRINZIPIEN.md) und BACKLOG.md gezielt nachlesen, wenn der Anlass kommt. Grosse Dateien (Fable-Antworten, Register) über einen Helfer lesen, nicht direkt.

Sag mir in wenigen Sätzen, was du verstanden hast — Stand, nächster Schritt, und was gerade auf wen wartet. Fang danach in derselben Antwort mit dem ersten Handwerksschritt an.
```

**Stehende Pflichten (Kurzfassung):** Umzugsampel als letzte Zeile · Helfer nach 22.10, Gegenleser vor jeder Übergabe · an Fable nur vorgeprüfte Verfahrensfragen · Aufträge per `starte_TB-<n>`, Wächter-Log prüfen, Nachschau per `send_later` · jede Betreiberentscheidung als Karte mit Empfehlung · Befehle für den Betreiber je eine Zeile · Einfügesatz am Schluss im Kopierfeld · Sitzungen mit Aufwand hoch.

