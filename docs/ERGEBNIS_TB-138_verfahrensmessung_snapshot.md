# TB-138: Ergebnis. Verfahrensmessung am Snapshot, nur lesend — Kalender „NYSE“ erfüllt R66 (b) bei allen vier Aktien-Bots; eine `_1d`-Reihe (APH) endet einen Tag vor dem letzten Kurstag ihres Marktes; Lock-Fassung 4.6.1 in `trading-env`, 5.4.0 stammt aus der Cloud

**Sitzungstitel:** `TB-138` · **Stand:** 06.10.2026, 16:02 (gemessen mit `date`) · **Auftrag:** `docs/auftraege/MAC_TB-138_verfahrensmessung_snapshot.md` ·
**Belege:** `docs/belege/TB-138/`
**Eingang:** `0c70853` (TB-133 D3). Commits: `5e7037a` (Schritt 0: Stand des steuernden Chats, **⟨S0⟩**), `9833724`
(A: Messskript, Gegenprobe, M1–M3, mit den Belegen aus 0a/0b), `a5cb034` (B: BACKLOG), der Abgabe-Commit (D: dieses
Dokument, Journal EG) und ein kleiner Commit mit `d3_porcelain.txt`. Nach jedem Commit gepusht, jeder Push im ersten Versuch.
**Freigabe:** pauschal für Handwerk ohne Sperrlistennähe (Betreiber 26.09.2026); „Fahre im Backlog fort“ (Betreiber
06.10.2026, 13:22). **Keine Rückfrage an den Betreiber in dieser Sitzung.**
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6), Fassungen gleich `requirements.lock`. Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.** Ein Befund (M2 Nr. 2, R72 (d)) — gemeldet, nicht behoben; er wird vor dem Tag entschieden.

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | `main`, `0c70853`; genau die 3 Einträge | **gleich**, in `$TMPDIR` vor dem Anlegen von `docs/belege/TB-138/`, danach kopiert (`0a_head.txt`, `0a_status.txt`) |
| 0b | Interpreter startet, 3.9.6; Register 11 581 Z. `8d505a38…`; Abbild `46f0ad5d1d83a253…`; Universumsdateien wie belegt; `--pruefen` rc 0; 226 Dateien | **alles gleich** (`0b_ausgang.txt`): 3.9.6, 11 581 Z., `8d505a38…`, `46f0ad5d1d83a253…`, `6acba892…`/`3afc95a4…`, `--pruefen` rc 0 „UNVERAENDERT“, 226 Dateien; Lock `96a5c572…`, Dateiliste `e810849e…` (nur gemessen) |
| Gegenprobe | Unterschied Kopie 1 ↔ Kopie 2 genau die Meldungen aus G1–G8; `m1`/`m2` an Kopie 2 rc 1 | **12/12 Meldungen, keine weitere, keine fehlende**; rc 1/1 an Kopie 2 (rc 0/0 an Kopie 1, kein Soll). Beim ersten Lauf, ohne Berichtigung (`gegenprobe.txt`) |
| M1 | Urteil je Aktien-Bot | **rc 0. Bedingung aus R66 (b) für „NYSE“ bei allen vier Aktien-Bots erfüllt**, und über die ganze Datenspanne 1962-01-02 bis 2026-09-01 (16 275 Tage in H und in K, 0 nur in H, 0 nur in K) |
| M2 | keine früher endende `_1d`-Reihe; Zählungen | **rc 1, Befund:** `APH_1d.csv` endet mit Kurs am 2026-08-31; der letzte Kurstag des Marktes ist 2026-09-01. Lücken: Aktien 2 (`LMT` 1974-06-03, `MNST` 2026-08-10), im Zeitraum je Aktien-Bot 1; Krypto 0. Doppelte `open_time`, doppelte Tage, Zeitanteile: je 0 |
| M3 | Fassungen gleich Lock | **rc 0**: 4/4 gleich `requirements.lock` Z. 37/50/51/52, Interpreter gleich Z. 6–7 |
| B | Anker 1, Text nachher 1, zeichengleich; numstat 6/0 | Anker 1 (Z. 306 von 317), erste Textzeile vorher 0, nachher 1; C3 GLEICH (730 Bytes, 5 Zeilen); `6	0` |
| D0 | `0b` gleich bis auf HEAD | **gleich** bis auf HEAD und Zeitzeile (`0b_nachher.txt`) |

## Gegenprobe (Prüfprinzipien B1)

Kleiner Snapshot in `$TMPDIR/tb138_gegenprobe.*` (nicht committet): Aktien `AAPL`, `MSFT`, `JNJ` (`_1d`), Krypto `BTCUSDT`,
`ETHUSDT` (`_1d`, `_1h`, `_4h`), die zwei Universumsdateien auf diese Symbole gekürzt. Kopie 2 trägt acht Eingriffe:

| | Eingriff | gemeldet (Art, Symbol, Datum) |
|---|---|---|
| G1 | `AAPL` Zeile 2021-03-10 entfernt | `m2 luecke AAPL 2021-03-10` |
| G2 | alle drei Aktien Zeile 2022-06-08 entfernt | `m1 nur_in_H - 2022-06-08`; `m2 luecke` AAPL/MSFT/JNJ 2022-06-08 |
| G3 | `AAPL` Zeile am Samstag 2023-04-15 eingefügt (Kursspalten `x`) | `m1 nur_in_K AAPL 2023-04-15` |
| G4 | `JNJ` letzte fünf Zeilen (2026-08-26 … 2026-09-01) entfernt | `m2 frueher_endend_1d JNJ 2026-08-25` |
| G5 | `JNJ` Zeile 2024-02-14 verdoppelt | `m2 doppelt_open_time JNJ 2024-02-14` |
| G6 | `MSFT` `close` am 2020-11-18 geleert | `m1 close_fehlt_leer MSFT 2020-11-18`; `m2 luecke MSFT 2020-11-18` |
| G7 | `BTCUSDT` `_1d` 2023-03-15 mit ` 05:00:00` | `m2 zeitanteil BTCUSDT 2023-03-15` |
| G8 | `ETHUSDT` `_1d` Zeile 2025-01-22 entfernt | `m2 luecke ETHUSDT 2025-01-22` |

Verglichen wurden nur die FALL-Zeilen (Felder Messung, Art, Symbol, Datum): „nur an Kopie 1“ leer, „nur an Kopie 2“ gleich
dem Soll, Zeile für Zeile. Der Kalender lud; G2, G3 und das Soll für `m1` entfielen also nicht.

## M1 — Bedingung aus R66 (b) für den Kalender „NYSE“, je Aktien-Bot (R74 (e); 54.6 Nr. 1)

Beleg `m1.txt` (rc 0). Kopf: `trading-env/bin/python3`, 3.9.6, `macOS-15.7.9-x86_64-i386-64bit`, `pandas_market_calendars`
4.6.1, `pandas` 2.3.3, `exchange_calendars` 4.5.6, `numpy` 2.0.2, **„Fassungen gleich Lock: ja“** — M1 ist eine Messung
in der Lock-Umgebung nach L2.

| Nr. | Ist |
|---|---|
| 1 K | 150 Symbole, 150 `_1d`-Reihen; erster Tag **1962-01-02**, letzter Tag **2026-09-01**, **16 275** Tage |
| 2 H | Sitzungstage „NYSE“ 1962-01-02 bis 2026-09-01: **16 275** |
| 3 je Jahr | 1962–2026 jedes Jahr H = K; **0** Tage nur in H, **0** Tage nur in K, **0** Symbol-Tage an Tagen, die kein Handelstag sind (`m1.txt` Z. 22–89). Keine Einzelfälle. Frühestes Jahr ohne Abweichung bis zum Ende: **1962** |
| 4 je Bot | siehe Tabelle unten |
| 5 `close` fehlt | **1 Zeile:** `APH` 2026-09-01, Zelle leer. Fehlwert-Text 0, Zeile ohne `close`-Spalte 0, unlesbares Datum 0. Liste der Fehlwert-Texte aus `pandas._libs.parsers.STR_NA_VALUES` im Beleg (Z. 117) |
| 6 verkürzte Sitzungen | 2017-01-01 bis 2026-09-01: 2 429 Sitzungstage, davon **20** mit Schluss vor dem regulären (16:00 America/New_York); `early_closes(schedule)` nennt dieselben 20; alle in H. Beispiele 2017-07-03, 2017-11-24, 2018-07-03 (je 13:00 Ortszeit) |

| Aktien-Bot | Zeitraum (L4–L3) | Sitzungstage | nur H | nur K | Symbol-Tage an Nicht-Handelstagen | erster/letzter Tag aus K | Urteil |
|---|---|---:|---:|---:|---:|---|---|
| `elliott_wave_stocks` | 2017-01-01 … 2026-08-31 | 2 428 | 0 | 0 | 0 | 2017-01-03 / 2026-08-31 | **erfüllt** |
| `rsi2_mean_reversion` | 2018-01-01 … 2026-08-31 | 2 177 | 0 | 0 | 0 | 2018-01-02 / 2026-08-31 | **erfüllt** |
| `turtle_soup_stocks` | 2017-01-01 … 2026-08-31 | 2 428 | 0 | 0 | 0 | 2017-01-03 / 2026-08-31 | **erfüllt** |
| `volatility_breakout` | 2018-01-01 … 2026-08-31 | 2 177 | 0 | 0 | 0 | 2018-01-02 / 2026-08-31 | **erfüllt** |

Der erste Tag aus K liegt bei jedem Bot auf dem ersten Sitzungstag des Jahres (der 1. Januar ist keiner), der letzte auf dem Ende.

**Wie der Kalender in 4.6.1 verkürzte Tage ausweist (vom Werkzeug abhängig):** `schedule` hat nur die Spalten
`market_open` und `market_close` (UTC); ein verkürzter Tag steht als gewöhnliche Zeile mit früherem `market_close` im
Index. Er ist also Sitzungstag nach L6. Die Klasse ist `NYSEExchangeCalendar`, `close_time` 16:00, Zeitzone
`America/New_York`. Die Methode `early_closes(schedule)` liefert dieselbe Menge wie der Vergleich von `market_close` in
Ortszeit mit `close_time`.

## M2 — Reihenenden und Symbol-Tage Lücke (R72 (d); 53.10 Nr. 3), dazu 53.10 Nr. 10

Beleg `m2.txt` (rc 1). Kopf wie M1, „Fassungen gleich Lock: ja“. Der Kalender lud; kein „Ersatz“.

**Nr. 1 Reihen je Zeile.** Aktien: 150 Zeilen, 150 `_1d`-Reihen. Krypto: 25 Zeilen; `_1d` 24, `_1h` 25, `_4h` 24. Nur
`XAUTUSDT` ohne `_1d` und ohne `_4h` — wie unter „Belegt“ erwartet. Reihen ohne Zeile in einer der zwei Dateien: 0.

**Nr. 2 Reihenenden.**

| Markt | letzter Kurstag (L7) | `_1d`-Reihen früher endend |
|---|---|---|
| Aktien | 2026-09-01 | ⚠️ **1 von 150: `APH`, letzter Kurstag 2026-08-31.** Die Zeile 2026-09-01 hat 6 Spalten; leer sind `open`, `high`, `low`, `close` (`m2.txt` Z. 25–28) |
| Krypto | 2026-09-14 | 0 von 24 |

`_1h`/`_4h` ohne Urteil: `_4h` 0 von 24 früher endend; `_1h` 1 von 25, nämlich `XAUTUSDT_1h` mit letztem Tag 2026-08-30
(nach Register Z. 1583–1586 nicht bewertet).

**Befund nach R72 (d):** Eine Kursreihe eines Symbols der Aktien-Datei endet vor dem letzten Kurstag ihres Marktes.
Der letzte Kurstag von `APH` (2026-08-31) ist zugleich das Ende des Zeitraums nach L3; der letzte Kurstag des Marktes
(2026-09-01) liegt einen Tag nach diesem Ende. Woran der Befund hängt: siehe L3, L5 und L7 unten.

**Nr. 3 Symbol-Tage Lücke (L8), `_1d`.**

| Markt | Handelstage | Lücken gesamt | je Jahr | Einzelfälle |
|---|---|---:|---|---|
| Aktien | Sitzungstage „NYSE“ 1962-01-02 … 2026-09-01 (16 275) | **2** | 1974: 1, 2026: 1 | `LMT` 1974-06-03, `MNST` 2026-08-10 |
| Krypto | Kalendertage 2017-08-17 … 2026-09-14 (3 316) | **0** | — | — |

Je Bot im Zeitraum nach R66 (a) (L4 bis L3): `elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks`,
`volatility_breakout` je **1** (`MNST` 2026-08-10); `elliott_wave`, `t3_supertrend`, `rsi2_crypto`, `turtle_soup_crypto`,
`volatility_breakout_crypto` je **0**.

Getrennt, ohne Einzelliste — Symbol-Tage vor dem ersten Kurstag eines Symbols, gezählt ab dem ersten Tag aus K des
Marktes: Aktien ab 1962-01-02 Summe 1 023 691 (je Jahr in `m2.txt` Z. 40; 2017: 2 761, 2018: 2 657, … 2024: 311,
2025: 28, 2026: 0); Krypto ab 2017-08-17 Summe 35 421 (Z. 66; 2018: 6 960, 2019: 5 754, … 2025: 1 255, 2026: 12).

**Nr. 4 (53.10 Nr. 10).** In allen 174 `_1d`-Reihen: doppelte `open_time` **0**, doppelte Tage bei verschiedener
Zeichenkette **0**, `open_time` mit Zeitanteil ungleich Mitternacht **0**. `benchmark.py` wurde nicht geöffnet.

## M3 — Paketfassung des Kalenders (54.6 Nr. 8)

| Nr. | Ist | Beleg |
|---|---|---|
| 1 | `trading-env`: `pandas_market_calendars` 4.6.1, `pandas` 2.3.3, `exchange_calendars` 4.5.6, `numpy` 2.0.2 — **4/4 gleich** Lock Z. 51/52/37/50; Interpreter gleich Z. 6 und Z. 7. `__file__`: `trading-env/lib/python3.9/site-packages/pandas_market_calendars/__init__.py` | `m3.txt`, rc 0 |
| 2 | `trading-env/bin/python3 -B research/snapshotgrenze/erhebung_eingaben.py` ohne `--json`: rc 0, „Paketfassung hier: **4.6.1**“. Keine Datei geschrieben (`git status` danach nur `docs/belege/TB-138/`) | `m3_shell.txt` |
| 3 | `which -a …` findet nur `/usr/bin/python3`: 3.9.6, `pandas_market_calendars` 4.6.1. Kein `python3.9` … `python3.13` im Pfad | `m3_shell.txt` |
| 4 | **Gefunden** in `docs/ERGEBNIS_TB-47_snapshotgrenze.md`: Z. 3 „Ergebnis der Cloud-Sitzung vom 18.09.2026.“; Z. 348 Python „**3.11.15**“; Z. 359 nachinstalliert „`pandas_market_calendars 5.4.0`“ (für Teil 1–4); Z. 122 „in der Cloud war die Fassung **5.4.0**“. Die Commit-Nachricht von `fc38d25` nennt keinen Interpreter. Autor „Claude“, 2026-09-18 05:18:53 +0000 (auch letzter Commit an `eingaben.json`) | `m3_shell.txt` |

`eingaben.json` wurde weder neu erzeugt noch geändert.

## Lesarten L1–L9 und offene Punkte O1–O4: woran welche Aussage hängt

| | Lesart | hängt daran |
|---|---|---|
| L1 | Snapshot = `snapshots/63e4b6c8…/` | alle Messungen. `--pruefen` rc 0 bestätigt Manifest und Hash des Ordners |
| L2 | Lock-Umgebung = `trading-env/` | M1 und M3 Nr. 1. Gemessen: Fassungen gleich Lock |
| L3 | Ende 2026-08-31 | **M1: keine** — über die ganze Spanne bis 2026-09-01 keine Abweichung. **M2 Befund: ja, mittelbar** — `APH` endet genau am Ende nach L3; der spätere Markttag 2026-09-01 liegt ausserhalb des Zeitraums. Lücken je Bot: gleich für jedes Ende ab 2026-08-10 |
| L4 | Beginn je Bot nach 33.2 | **M1: keine** (Spanne ab 1962 ohne Abweichung). M2 Lücken je Bot: gleich für jeden Beginn zwischen 1974-06-04 und 2026-08-10 |
| L5 | „trägt einen Kurs“ = `close` vorhanden | **M2 Befund: ja.** Mit „Zeile vorhanden“ statt „`close` vorhanden“ endete `APH` am 2026-09-01 und es gäbe keinen Befund (so misst Register Z. 11494 „nur Datumsspalten“). M1: keine (am 2026-09-01 tragen 149 andere Symbole `close`) |
| L6 | Sitzungstage = Index von `schedule` | M1, M2 Aktien. Verkürzte Sitzungen stehen im Index (gemessen, Nr. 6) |
| L7 | letzter Kurstag des Marktes über die ganze Reihe | **M2 Befund: ja.** Nähme man den letzten Kurstag des Marktes im Zeitraum nach R66 (a), wäre er 2026-08-31, und keine Reihe endete früher |
| L8 | Lücke zwischen erstem und letztem Kurstag | M2 Nr. 3. `APH` 2026-09-01 ist nach L8 keine Lücke (nach dem letzten Kurstag) |
| L9 | Kursreihe = `_1d` | M2 Nr. 2. `XAUTUSDT_1h` (Ende 2026-08-30) genannt, nicht bewertet |

| | offen | Stand nach TB-138 |
|---|---|---|
| O1 | erste Selektionsfalte nach R53 | unverändert offen; M1 ist von ihr unabhängig (siehe L4) |
| O2 | startet `trading-env`, welche Fassungen | **gemessen:** startet, 3.9.6, alle vier Pakete gleich Lock |
| O3 | woher „5.4.0“ | **Fundstelle:** `ERGEBNIS_TB-47` Z. 3, 348, 359 — Cloud-Sitzung, Python 3.11.15, Paket dort nachinstalliert. Auf dem Mac trägt kein gefundener Interpreter 5.4.0 |
| O4 | `--pruefen` unter `-B` ohne Umgebungsvariablen | **gemessen:** keine der drei Variablen gesetzt (`0b_ausgang.txt`); rc 0, „UNVERAENDERT“, keine Datei geschrieben, kein `__pycache__` |

## Für das Register

*Tatsachen mit Fundstelle im Beleg, ohne Urteil über das Verfahren. Der Eintrag in 54.5 ist eine Einzelfreigabe des Betreibers.*

- **Zu 54.5, Zeile R74 (54.1) (e), und 54.6 Nr. 1:** Am 06.10.2026 in `trading-env/bin/python3` (3.9.6; `pandas_market_calendars` 4.6.1, `pandas` 2.3.3, `exchange_calendars` 4.5.6, `numpy` 2.0.2, gleich `requirements.lock`) am Snapshot `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` gemessen: Für den Kalender „NYSE“ trägt im Zeitraum 2017-01-01 bzw. 2018-01-01 bis 2026-08-31 an jedem Sitzungstag mindestens ein Symbol aus `config/sp500_top150.txt` einen Kurs, und kein Symbol trägt einen Kurs an einem anderen Tag; je Aktien-Bot 0 Tage nur im Kalender, 0 Tage nur in den Daten. Über die ganze Datenspanne 1962-01-02 bis 2026-09-01 gilt dasselbe (16 275 Tage). Verkürzte Sitzungen stehen als Sitzungstage im Index von `schedule` (20 seit 2017). (`docs/belege/TB-138/m1.txt` Nr. 3, 4, 6)
- **Zu 53.10 Nr. 3:** Am Snapshot endet eine `_1d`-Reihe vor dem letzten Kurstag ihres Marktes: `APH`, letzter Tag mit `close` 2026-08-31; die Zeile 2026-09-01 hat leere Zellen in `open`, `high`, `low` und `close`. Der letzte Kurstag des Aktienmarkts im Snapshot ist 2026-09-01, der des Kryptomarkts 2026-09-14; keine Krypto-`_1d`-Reihe endet früher. Symbol-Tage Lücke über die ganze Spanne: Aktien 2 (`LMT` 1974-06-03, `MNST` 2026-08-10), Krypto 0; im Zeitraum nach R66 (a) je Aktien-Bot 1, je Krypto-Bot 0. (`m2.txt` Nr. 2, 3)
- **Zu 53.10 Nr. 10:** In den 174 `_1d`-Reihen des Snapshots: 0 doppelte `open_time`, 0 doppelte Tage, 0 `open_time` mit Zeitanteil ungleich Mitternacht. (`m2.txt` Nr. 4)
- **Zu 54.6 Nr. 8:** In `trading-env` ist `pandas_market_calendars` 4.6.1 installiert, gleich Lock; `erhebung_eingaben.py` meldet dort „Paketfassung hier: 4.6.1“. Der Wert 5.4.0 in `eingaben.json` stammt nach `docs/ERGEBNIS_TB-47_snapshotgrenze.md` Z. 3, 348 und 359 aus der Cloud-Sitzung vom 18.09.2026 mit Python 3.11.15, in der das Paket nachinstalliert wurde. (`m3.txt`, `m3_shell.txt`)
- **Zu Register Z. 11494 („Nicht gemessen: Zeilen ohne `close`“):** Am Snapshot fehlt `close` in genau einer Zeile der Aktien-Reihen (`APH` 2026-09-01, leere Zelle); Fehlwert-Texte 0. Krypto nicht gemessen (M1 liest nur Aktien). (`m1.txt` Nr. 5)

## Für Fable

1. **R72 (d), `APH`:** Ist „der letzte Kurstag ihres Marktes“ über die ganze Reihe gemeint (dann ist `APH` ein Befund) oder im Zeitraum nach R66 (a) (dann endet keine Reihe früher, weil `APH` am Ende 2026-08-31 noch einen Kurs trägt)? Was ist vor dem Tag zu entscheiden?
2. **„trägt einen Kurs“ (R66 (b), R72 (d)):** Reicht eine Zeile, oder muss `close` vorhanden sein? Die Messung am Bestand (Register Z. 11494) las nur Datumsspalten; dort gab es keinen Befund.
3. **Die Zeilen vom 2026-09-01:** Der Snapshot führt für alle 150 Aktien eine Zeile am 2026-09-01, einen Tag nach dem Ende der Bestätigungsperiode. Ob diese Zeilen vollständige Tage sind, ist nicht gemessen (das ginge nur über Werte oder den Abrufzeitpunkt). Spielt das für den Lauf eine Rolle?
4. **`eingaben.json`, Feld `kalender`:** bleibt der Beleg von TB-47 mit einer Tatsachennotiz zur Herkunft, oder wird er in der Lock-Umgebung neu erzeugt?
5. **Der Krypto-Teil von „Zeilen ohne `close`“** ist nicht gemessen (M1 ist nach Auftrag eine Aktienmessung; M2 zählt Lücken mit L5, also gingen fehlende `close` dort als Lücke ein: 0).

## Nicht getan

- Kein Eintrag in Register 54.5 (Einzelfreigabe des Betreibers).
- Kein anderer Kalendername gerechnet oder verglichen.
- Keine Änderung an Code, Tests, Register, Abbild, Lock, `trading-env/`, `snapshots/`, `research/`, `shared/`, `strategies/`, `notifications/`, `docs/werkzeuge/`; `eingaben.json` weder neu erzeugt noch geändert.
- `faltenplan.faltenplan()`, `erste_falte()`, Zellen-Erzeuger, Selektionslauf, Sperrlisten-Sonde, Tests, Basislauf, db-Sicherung: nicht aufgerufen. `benchmark.py` nicht geöffnet.
- Kein Kurs, keine Rendite, keine Kennzahl ausgegeben; `close` nur auf „fehlt“ geprüft, nie in eine Zahl gewandelt. Bei `APH` 2026-09-01 stehen im Beleg nur die Namen der leeren Spalten.
- Die erste Selektionsfalte nicht neu abgeleitet (O1).

## In einfacher Sprache

Der Börsenkalender und die eingefrorenen Aktienkurse passen zusammen: An jedem Börsentag seit 1962 hat mindestens eine der
150 Aktien einen Kurs, und an keinem anderen Tag hat eine einen — das gilt für alle vier Aktien-Bots. Eine Kleinigkeit fällt
auf: Bei der Aktie APH ist die allerletzte Zeile (1. September 2026) leer, alle anderen Aktien haben dort einen Kurs. Weil
der Prüfzeitraum am 31. August endet, berührt das die Rechnung wohl nicht; ob es trotzdem als „Reihe endet zu früh“ zählt,
ist eine Auslegungsfrage, die vor dem Tag entschieden wird. In den Reihen fehlen insgesamt nur zwei einzelne Tage, doppelte
Daten gibt es keine. Und die Kalender-Fassung 5.4.0 aus einer älteren Messung kam aus einer Cloud-Sitzung; auf dem Mac ist
die festgeschriebene 4.6.1 installiert.
