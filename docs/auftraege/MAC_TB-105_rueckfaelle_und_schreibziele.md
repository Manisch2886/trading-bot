# TB-105 — Drei Rückfälle im Live-Code schliessen und die Schreibziele beim Import: Regimewache, `exit()` mit rc 0, leere Symbolliste, `manual_close.py`, Ordneranlage

**Sitzungstitel:** `TB-105` · **Angelegt:** 25.09.2026, 11:15, vom steuernden Chat
**Grundlage:** Fable 24b A2 („kein Fallback unter dem Modus, gleich welcher Art“), 25a Abschnitt 3 (A) (drei Klassen, Klasse (iii) Schreibziele) und Abschnitt 4 (die vier Rückfälle, alle vor den Tag); Register **11.1** (Regimewache)
**Vorgänger:** TB-104 (`516badc`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)
**Nachfolger:** TB-106 = Rückfall (d), Ersatzwerte für Schwellen in `faltenplan.py`, `benchmark.py`, `auswertung.py` (Sperrliste, eigenes Abbild). **Nicht hier.**

> **In einfacher Sprache, vorweg:** Im Code stecken noch Notlösungen: Fehlt etwas, rechnen Programme still weiter, statt abzubrechen. Diese Sitzung schliesst drei davon. Ausserdem sorgt sie dafür, dass ein geschützter Lauf beim Start keine Protokolldatei und keine Ordner mehr im Repo anlegt. Im normalen Betrieb darf sich dabei nichts ändern.

---

## ⭐⭐ Freigabe des Betreibers, wörtlich

**25.09.2026, 10:52, drei Auswahlkarten im steuernden Chat:**

| Frage | Antwort |
|---|---|
| *„TB-105, die vier Notlösungen … Wie schneiden wir es?“* | **„Zwei Aufträge (Empfohlen)“**: TB-105 Live-Code (b), (c), (a); TB-106 danach (d) mit Sperrliste |
| *„Der geschützte Lauf öffnet beim Import logs/notifications/manuelle_eingriffe.log zum Schreiben … Wo soll das behoben werden?“* | **„In manual_close.py (Empfohlen)“**: Ordner und Protokoll erst bei der ersten tatsächlichen Protokollzeile anlegen, nicht beim Import |
| *„… strategy_paths.py und bot_lauf.py legen beim Import Ordner an … Soll das mit in TB-105?“* | **„Ja, mit in TB-105 (Empfohlen)“**: unter dem Modus keine Ordneranlage; ohne Modus Byte für Byte gleich |

| freigegeben | Pfad | was |
|---|---|---|
| ✔ (b) | `strategies/t3_supertrend/equity_simulation.py`, `strategies/t3_supertrend/multi_symbol_optimise.py`, `strategies/volatility_breakout_crypto/equity_simulation.py` | Einbau von `shared/regimewache.py::btc_daten` an den drei Stellen aus `regimewache.EINBAUSTELLEN` (Register 11.1) |
| ✔ (c) | die 9 `strategies/*/equity_simulation.py` und die 5 `strategies/*/multi_symbol_optimise.py` mit „Keine Daten gefunden“ + `exit()` (Liste: `docs/belege/TB-104/d3_vier_rueckfaelle.txt`, Rang 2) | **unter dem Modus** Rückgabe **2** statt 0; ohne Modus unverändert |
| ✔ (a) | `shared/symbols_config.py` | **unter dem Modus**: Liste nach `EXCLUDE_SYMBOLS` leer ⇒ Rückgabe 2; ohne Modus unverändert |
| ✔ Schreibziel | `notifications/manual_close.py` | `os.makedirs` und `RotatingFileHandler` nicht mehr beim Import, sondern beim ersten Schreiben einer Protokollzeile |
| ✔ Schreibziel | `shared/strategy_paths.py`, `research/exposure_messung/bot_lauf.py` | **unter dem Modus** kein `os.makedirs`; ohne Modus unverändert |
| ✔ | die Tests dieser Module (vorhandene erweitern, wo nötig neue unter `shared/` bzw. im jeweiligen Ordner) | — |

⛔ **Nicht freigegeben:** `shared/regimewache.py` (fertige, geprüfte Wache aus TB-30a; nur **importieren**), `shared/paths.py`, `shared/ladeprotokoll.py`, alles unter `research/vorregistrierung/` (auch `faltenplan.py`, `benchmark.py`, `auswertung.py`, `registerdaten.py`: das ist TB-106), `research/universum_trockenlauf/` (die `$TMPDIR`-Ablagen warten auf Fable), alle `forward_test.py` und `live_params.py`, `crontab`, das Register. Braucht eine Änderung eine dieser Dateien: **Auswahlkarte an den Betreiber**, wie TB-103/TB-104; ohne Antwort nicht ändern.

⚠️ **Live-Code:** Die Dateien unter `strategies/`, `shared/` und `notifications/` laufen teils im Cron oder im Papierpfad. **Oberste Bedingung:** Ohne Modus und mit vollständigen Daten rechnet jedes geänderte Modul Byte für Byte dasselbe wie vorher. Der Modus wird über `shared/paths.py::selektionsmodus()` erfragt, nicht über eigene Umgebungsvariablen.

---

## 0. Schritt 0

**0a — Arbeitsbaum des steuernden Chats committen.** Erwartet:

| Datei | Stand |
|---|---|
| `docs/auftraege/MAC_TB-105_rueckfaelle_und_schreibziele.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger auf TB-105 |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-25b_laufbereich_gemessen_fuenf_fragen.md` | neu |
| `docs/projektfuehrung/UEBERGABE_2026-09-25.md` | Nachtrag angehängt |

**0b — nach 7c:** `.git/*.lock` keine; HEAD am Eingang **`516badc`**; Datenstand vorher (Soll `d9449faf…`); Quersummen der `*.db` vorher; Hashes aller freigegebenen und aller gesperrten Dateien vorher (`docs/belege/TB-104/hashes.sh` als Vorlage); Sonde gegen **`sperrliste_abbild_2026-09-25.json`** (`cb4eb1b4…`) vorher.

---

## Block A — Vormessung nachmessen

⚠️ Vormessung des steuernden Chats, aus `docs/belege/TB-104/d3_vier_rueckfaelle.txt` (Stand `f334a7b`) und `shared/regimewache.py`. Nach `A8`: Weicht deine Messung ab, **gilt deine**.

| | zu prüfen | Vormessung |
|---|---|---|
| **A1** | `regimewache.EINBAUSTELLEN` nennt drei Stellen; `pruefe_einbau()` meldet **0 von 3** eingebaut. `t3_supertrend` überspringt den Filter still (`if "BTCUSDT" in all_data:` ohne `else`, `equity_simulation.py::collect_all_trades` und `multi_symbol_optimise.py::evaluate_combination_multi`); `volatility_breakout_crypto` bricht laut Kopf von `regimewache.py` schon heute ab, steht aber als Einbaustelle darin | 0/3 |
| **A2** | Die 14 `exit()`-Stellen nach „Keine Daten gefunden“ liegen alle im Block `if __name__ == "__main__":` | 14, alle `__main__` |
| **A3** | ⭐ **Wer ruft die geänderten Dateien im Betrieb?** Cron (`crontab -l` **nur gefiltert**, K2a: `crontab -l \| grep -c <datei>`), Papierpfad (`forward_test.py` importiert?), Dashboard. Je Datei eine Zeile. **Das bestimmt, wo „ohne Modus unverändert“ gemessen werden muss** | nicht gemessen |
| **A4** | `notifications/manual_close.py`: Wer schreibt Protokollzeilen (`_protokoll.info(...)` o. ä.), und in welchen Prozessen (Telegram, Dashboard, Cron)? Das Format einer Protokollzeile muss unverändert bleiben | nicht gemessen |
| **A5** | `shared/strategy_paths.py::get_strategy_paths()`: Welche Aufrufer **schreiben** in `RESULTS_DIR`/`LOGS_DIR`, und tun sie das in einem Modus-Lauf? (Gibt es unter dem Modus keinen Ordner, bricht ein schreibender Aufrufer mit `FileNotFoundError` ab. Das ist erwünscht, muss aber gemessen sein) | nicht gemessen |
| **A6** | Sperrlistenprüfung wie TB-104 (`a8_sperrliste.py`): Steht eine der freigegebenen Dateien auf einem Punkt, in `EINGEFROREN` oder im Abbild? Punkt 11 nennt „Commit-Hashes von Simulation, Erkennung, Optimierern“: Ist das eine Sperre der Dateien oder nur ihres Commits? Lies den Punkttext und melde den Wortlaut | nicht gemessen |

⛔ **Steht eine freigegebene Datei auf einem Sperrlistenpunkt, der den Datei-Hash sperrt:** diese Datei nicht ändern, Auswahlkarte an den Betreiber.

Belege: `a_vormessung.txt`, `a3_aufrufer.txt`, `a4_manual_close.txt`, `a5_strategy_paths.txt`, `a6_sperrliste.txt`.

---

## Block B — Rückfall (b): die Regimewache einbauen (Register 11.1)

**B1** — An den drei Stellen aus `EINBAUSTELLEN` genau so, wie der Kopf von `shared/regimewache.py` es vorgibt (`from regimewache import btc_daten`, Aufruf mit `bot=` und `holen=`). **`regimewache.py` selbst bleibt unverändert.**
**B2** — Danach meldet `regimewache.pruefe_einbau()` **3 von 3**. Beleg ist die Ausgabe.
**B3** — **Ohne Modus, mit BTCUSDT vorhanden:** Ausgabe bytegleich vor und nach. Genauer: `collect_all_trades` für `t3_supertrend` und `volatility_breakout_crypto` auf `data/` im Speicher, die Trade-Liste als JSON mit sortierten Schlüsseln, Hash vorher = nachher. **Ohne BTCUSDT** (Wegwerfbaum): Abbruch mit der Meldung aus `regimewache`, kein Weiterrechnen. Das gilt nach 11.1 mit und ohne Modus („nicht deterministisch“).
**B4** — Proben: „BTCUSDT fehlt ⇒ Abbruch“ je Einbaustelle; Mutationsprobe „Einbau zurückgenommen“ ⇒ Probe rot; Gegenprobe. Jede Mutationsprobe beisst **allein** (24b B3).

## Block C — Rückfall (c): `exit()` mit rc 0 unter dem Modus

**C1** — An den 14 Stellen: unter dem Modus endet „Keine Daten gefunden“ mit **Rückgabe 2** und der Meldung auf `stderr`. Ohne Modus bleibt es beim bisherigen Verhalten (Text und `exit()` unverändert). ⭐ Eine Hilfsfunktion **an einem Ort** ist erlaubt, wenn sie in einer der freigegebenen Dateien liegt; sonst je Stelle zwei Zeilen. Keine neue Datei unter `shared/` ohne Rückfrage.
**C2** — Probe je Datei: Modus mit leerem Datenbestand (Snapshot-Attrappe ohne Kursdateien) ⇒ rc 2; ohne Modus ⇒ rc 0 wie vorher. Eine Mutationsprobe für die Bauart (nicht 14), mit Gegenprobe.

## Block D — Rückfall (a): leere Liste in `symbols_config.py`

**D1** — Unter dem Modus: Ist die Liste nach `EXCLUDE_SYMBOLS` leer, endet der Import mit `SystemExit(2)` und einer Meldung, **bevor** `DEFAULT_SYMBOLS` greift. Ohne Modus unverändert. ⚠️ Die bisherige Meldung „nicht gefunden“ ist in diesem Fall falsch (TB-103 A3): **ohne Modus nicht ändern**, nur messen und melden.
**D2** — Proben: Attrappe mit einer Universumsdatei, die nur ausgeschlossene Symbole enthält ⇒ Modus rc 2; ohne Modus Standardliste wie bisher. Mutationsprobe mit Gegenprobe.

## Block E — Schreibziele beim Import (Fable 25a (A) (iii))

**E1 — `notifications/manual_close.py`:** `os.makedirs(PROTOKOLL_DIR)` und der `RotatingFileHandler` werden erst beim **ersten Schreiben einer Protokollzeile** angelegt (z. B. eine kleine Funktion, die den Handler bei Bedarf einrichtet und genau einmal anhängt). Das Format jeder Zeile bleibt zeichengleich. Proben: (1) Import allein ⇒ **kein** `mkdir`, **kein** `open(…, "a")` (Haken aus `docs/belege/TB-104/haken/`); (2) eine Protokollzeile ⇒ Datei entsteht, Zeile im alten Format; (3) zwei Zeilen ⇒ ein Handler, nicht zwei. Mutationsprobe „Anlage wieder beim Import“ ⇒ Probe (1) rot, mit Gegenprobe.
**E2 — `shared/strategy_paths.py`:** unter dem Modus kein `os.makedirs` für `RESULTS_DIR`/`LOGS_DIR`; die Pfade werden weiter zurückgegeben. Ohne Modus unverändert. **Ohne Modus 99 Pfade, 0 Unterschiede** (Probe A aus `shared/test_paths.py`) muss grün bleiben, ebenso `shared/test_strategy_paths.py`.
**E3 — `research/exposure_messung/bot_lauf.py:63`:** dasselbe für `research/exposure_messung/daten/`.
**E4 — Proben** im **frischen Klon** (Bauart TB-104 A6: `git clone`, Haken auf `os.mkdir`): Modus-Lauf eines Bots ⇒ **0** angelegte Ordner im Repo; ohne Modus ⇒ die Ordner wie bisher. Mutationsprobe mit Gegenprobe.

**Commits:** (2) Block B · (3) Block C und D · (4) Block E. Jeweils mit Tests.

---

## Block F — Abnahme: der Trockenlauf aller neun und die Benchmark-Tabelle, mit den drei Klassen

**F1** — Trockenlauf aller neun Bots im Modus (Skript `docs/belege/TB-103/d_trockenlauf.py`, Lauf-Typ wie TB-103, Haken aus TB-104), **zweimal: im echten Repo und im frischen Klon**. Soll:
- 9 × rc 0.
- Liste = Universumsdatei.
- Geladene Menge 18/18/20/20/20/147 × 4 (Register 16.1.1).
- Klasse (i) ausserhalb: 0.
- Klasse (ii): die bekannte Liste (5).
- ⭐ **Klasse (iii): leer**, weder `logs/notifications/`, noch `results/<bot>/`, `logs/<bot>/`, `research/exposure_messung/daten/`.

**F2** — `benchmark.py --ziel <scratch>` im Modus ⇒ **bytegleich `64fb2912…`**. Klasse (iii): `manuelle_eingriffe.log` darf **nicht** mehr erscheinen; die `$TMPDIR/tb40_lauf_*`-Ablagen bleiben erwartet (Frage an Fable, nicht Gegenstand).
**F3** — Ohne Modus, mit vollständigen Daten: dieselben 8 Ausgaben wie TB-104 `b0_ausgaben.sh` bytegleich; `benchmark.py` ohne Modus `64fb2912…`.
**F4** — Tests am Ende: `test_paths` 35/35, `test_strategy_paths`, `test_stille_ausfaelle`, `test_startpruefungen`, `test_vorregistrierung` 196/196, dazu alle neuen. **Namen** der neuen Proben im Ergebnisdokument.

⛔ Sichtschutz 27.1: keine Kennzahl, keine Trade-Zahl im Ergebnisdokument; die Hashes der Trade-Listen aus B3 sind zulässig.

## Block G — Abgabe

| | |
|---|---|
| **G1** | Hashes nachher: Geändert sind nur freigegebene Dateien und `docs/`. Gesperrte Dateien, Datenstand, Snapshot, `ergebnisse/` und `*.db` (bis auf den Cron) gleich. Sonde gegen `cb4eb1b4…` vorher = nachher (kein Sperrlistenpfad bewegt) |
| **G2** | Ergebnisdokument `docs/ERGEBNIS_TB-105_rueckfaelle_und_schreibziele.md` mit **„Für Fable“** (27.1): 11.1 erfüllt? (b)/(c)/(a) mit Probenamen; Klasse (iii) nach E leer? Was bleibt für TB-106 |
| **G3** | „Für die Folgesitzung vorbereitet“ (TB-106: die Stellen von (d) am neuen Stand), „In einfacher Sprache“, Journalblock, `git --no-optional-locks status --porcelain` nach dem letzten Commit leer |

## ⚠️ Abbruchkriterien

1. Ohne Modus ändert sich eine Ausgabe (B3, F3) ⇒ die betreffende Änderung zurücknehmen, melden.
2. Die Benchmark-Tabelle ist nicht bytegleich ⇒ nicht weiterbauen, melden.
3. Eine Änderung bräuchte eine nicht freigegebene Datei ⇒ Auswahlkarte.
4. A3 zeigt, dass eine Datei im Cron läuft und B dort einen Abbruch auslösen könnte (BTCUSDT fehlt im Live-Bestand) ⇒ **vor B melden** und per Auswahlkarte fragen, ob die Wache dort ohne Modus greifen soll.

---

## In einfacher Sprache

An drei Stellen rechnen Programme heute still weiter, wenn etwas fehlt.
- Einem Bot fehlt der Bitcoin-Kurs für seinen Marktfilter: Er rechnet dann ohne den Filter weiter und ist in Wahrheit ein anderer Bot.
- Programme ohne Daten melden „fertig“ statt „Fehler“.
- Eine leere Werteliste wird still durch eine Notliste ersetzt.

Alle drei führen künftig zum Abbruch, im geschützten Modus immer.

Ausserdem legen Programme beim blossen Laden eine Protokolldatei und Ordner im Projekt an. Das passiert künftig erst dann, wenn wirklich etwas geschrieben wird, und im geschützten Modus gar nicht.

Zum Schluss laufen alle neun Bots und die Vergleichstabelle noch einmal im geschützten Modus. Im normalen Betrieb darf sich an keiner Zahl etwas ändern.
