# ERGEBNIS TB-161 — S-B1-Datenlauf: 14 ETF-Reihen, Historie, Datenstand vorher/nachher

**Stand:** 14.10.2026, Mac-Sitzung TB-161 (Opus 5.5) · **Auftrag:** `docs/auftraege/MAC_TB-161_sb1_datenlauf.md` · **Base:** `main` am HEAD `4979589` · **Commits:** ⟨S0⟩ `d5c51bd` (Stand des steuernden Chats), ⟨M⟩ `725a15a` (Belege Schritt 0–9), ⟨F⟩ = der Commit „TB-161 Abgabe: Ergebnis, Backlog, Journal EW“ (enthält diese Datei) · **Journal:** Block EW · **Belege:** `docs/belege/TB-161/`.

Kein Abbruch. Kein Aufruf abgelehnt, keine Bestätigung verlangt. Kein Code geändert, nichts installiert, nichts unter `data/` geschrieben. Keine Ertrags- oder Sharpe-Zahl gemessen oder berichtet.

## Kurz

Die Antwort auf die Frage des Testauftrags (Z. 151–153): **Ja — die Historie reicht.** Am 2008-01-01 haben 11 von 14 Instrumenten aus 6 Anlageklassen ein Signal (verlangt: 8 Instrumente, 4 Klassen); `historie.py` gibt **rc 0** zurück.

| # | Prüfung | erwartet | beobachtet |
|---|---|---|---|
| 1 | Arbeitsbaum sauber | leer | 0a: genau die 4 Soll-Einträge des Auslegens (3 × ` M`, 1 × `??`), HEAD `4979589`; in ⟨S0⟩ committet |
| 2 | **Datenstand vorher** | `d9449faf…` / 223 Dateien | `d9449faf…5f84`, 223 Dateien, `unveraendert`, rc 0 |
| 3 | Selbsttest vorher | 64/64 | `64/64 Pruefungen bestanden.`, rc 0 |
| 4 | Datenlauf | 14 Dateien | 14 Dateien, rc 0, je 0 unvollständig / 1 verworfen |
| 5 | **Erstes Datum je ETF** | 14 Zeilen, gemessen | 14 Zeilen (Abschnitt „Historie“) |
| 5a | **Untergrenze am 2008-01-01** | erfüllt / nicht erfüllt | **erfüllt** (11 von 8 Instrumenten, 6 von 4 Klassen) |
| 5b | **Rückgabewert `historie.py`** | 0 oder 1 (beides zulässig) | **0** |
| 5c | Tragende Selektionsfalten | ≥ 3 | 18 |
| 5d | Abweichungen zur Erwartung | Liste (darf leer sein) | leer (kein Block gedruckt) |
| 6 | N | 5 | 5 (N_historisch 653, N gesamt nominal 658) |
| 7 | Obere Kostenschranke | 1,80 pp/Jahr | 1.80 pp/Jahr (Massstab voller Round Trip 3.60) |
| 8 | Selbsttest nachher | 64/64 | `64/64 Pruefungen bestanden.`, rc 0; Beleg bytegleich mit Schritt 3 |
| 9 | **Datenstand nachher** | `IDENTISCH` | `IDENTISCH` (`d9449faf…5f84`, 223 Dateien) |
| 9a | `git status data/` | leer | leer (`09_git_data.txt` nur `rc 0`) |
| 10 | `git status` gesamt | leer | gemessen nach ⟨F⟩ in `f_porcelain.txt` (Commit „TB-161 F“); Soll 0 B |
| 10a | Dateien in `daten/` | 15 | 15 |
| 11 | Bestehende Tests | bestanden | nicht Teil von TB-161 |

## Historie

Wörtlich aus `docs/belege/TB-161/05_historie.txt`:

```
  Symbol Klasse      erstes Datum  Signal ab       Tage   Erwartung
  ------------------------------------------------------------------------
  SPY    Aktien      1993-01-29    1994-01-26      8484   1993-01-29
  IWM    Aktien      2000-05-26    2001-05-25      6634   2000-05-26
  EFA    Aktien      2001-08-27    2002-08-30      6319   2001-08-21
  EEM    Aktien      2003-04-14    2004-04-13      5913   2003-04-14
  IEF    Zinsen      2002-07-30    2003-07-29      6091   2002-07-26
  TLT    Zinsen      2002-07-30    2003-07-29      6091   2002-07-26
  LQD    Kredit      2002-07-30    2003-07-29      6091   2002-07-26
  HYG    Kredit      2007-04-11    2008-04-09      4909   2007-04-11
  GLD    Metalle     2004-11-18    2005-11-16      5509   2004-11-18
  SLV    Metalle     2006-04-28    2007-04-30      5147   2006-04-28
  DBC    Rohstoffe   2006-02-06    2007-02-06      5204   2006-02-03
  DBA    Rohstoffe   2007-01-05    2008-01-04      4974   2007-01-05
  FXE    Waehrungen  2005-12-12    2006-12-11      5241   2005-12-09
  FXY    Waehrungen  2007-02-13    2008-02-12      4948   2007-02-13

  Untergrenze am 2008-01-01:
    Instrumente    11 von 8 verlangt   erfuellt
    Anlageklassen   6 von 4 verlangt   erfuellt
    dabei: SPY, IWM, EFA, EEM, IEF, TLT, LQD, GLD, SLV, DBC, FXE
    Klassen: Aktien, Kredit, Metalle, Rohstoffe, Waehrungen, Zinsen

  Selektionsfalten, die die Untergrenze tragen: 18 (Mindestzahl 3)
```

Jahrestabelle: 2008 11 Instrumente / 6 Klassen, 2009–2025 je 14 / 6, jedes Jahr „traegt ja“. Vorlauf 252 Handelstage. **rc 0.**

Abweichungen zur Erwartung: `historie.py` druckt keinen Block „Abweichungen zur Erwartung (die MESSUNG gilt)“ — die Liste ist leer. Sechs Symbole liegen zwei bis sechs Kalendertage hinter der Spalte „Erwartung“ (EFA, IEF, TLT, LQD, DBC, FXE); das Programm wertet das nicht als Abweichung. Nur zur Kenntnis: am Stichtag fehlen HYG, DBA und FXY (Signal ab 2008-01-04 bis 2008-04-09); die Untergrenze trägt ohne sie.

## Manifest

Aus `docs/belege/TB-161/04_manifest.txt` (das Manifest selbst bleibt gitignoriert in `research/etf_trendfolge/daten/`):

```
manifest.json · 3511 B · sha256 24d7624f034f7a894f42a24759dcad963390f4b092093de30863eca41cd5dff3 · erzeugt 2026-10-14T18:50:31Z · auto_adjust True · intervall 1d
Kursdateien (*.csv) in research/etf_trendfolge/daten: 14 · Eintraege im Manifest: 14 · davon vorhanden: 14
```

Je Symbol erstes und letztes Datum (letztes durchweg 2026-10-13), Grösse und sha256 stehen in der Belegdatei. Datenlauf: 18:50:21Z bis 18:50:31Z, rund 10 s.

## Datenstand

| | Ist | Dateien | rc |
|---|---|---|---|
| vorher (Schritt 2) | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` | 223 | 0 |
| nachher (Schritt 9) | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` | 223 | 0 |
| Vergleich | `IDENTISCH` | | |

Beide Läufe melden `liegt ausserhalb von data/ - richtig so.`; die beiden JSON-Belege sind bytegleich. `git status --porcelain data/` ist leer.

## Belege

Alle unter `docs/belege/TB-161/`; Bytes und md5 vor dem Commit ⟨F⟩ gemessen. `f_porcelain.txt` und `f_numstat.txt` entstehen erst danach (Commit „TB-161 F“).

| Datei | Befehl | Bytes | md5 |
|---|---|---|---|
| `0a_status.txt` | `git status --porcelain` (0a), nach ⟨S0⟩ `cp` | 176 | `6d14c6f8a12990669c120606a9b5493b` |
| `tb161_werkzeug.py` | Holbefehl (0a), nach ⟨S0⟩ `cp` | 5072 | `125f94772cb56a2ee4533463d1df37bb` |
| `0b_ausgang.txt` | Block 0b | 505 | `d74964ac6149a70f44ef764619e24e13` |
| `0c_db_sicherung.txt` | `md5 …` (0c) | 1903 | `a91387dc62bcd753d0178cafe6d6f343` |
| `02_datenstand_vorher.json` | `datenstand.py --json` (2) | 409 | `694dffe73916135fc2c9666b06667246` |
| `02_datenstand_vorher.txt` | `datenstand.py` (2) | 429 | `e3ca50a0ae4ce376f85972c638712a26` |
| `0d_umgebung.txt` | zwei Importbefehle (0d) | 359 | `64db9ff7a392c7a9222579517adf5723` |
| `03_selbsttest.txt` | `test_etf_trendfolge.py` (3) | 361 | `b116f55b87f7d1a70c826b5300056225` |
| `04_datenlauf.txt` | `datenlauf.py` (4) | 4416 | `6ae56de037c91c8a2b005d039888cf87` |
| `04_manifest.txt` | `WZ manifest` (4) | 1947 | `599234996b91861e94a90846f440f914` |
| `05_historie.json` | `historie.py --json` (5) | 17067 | `952c70c1815a01fedb6699de0e2c643a` |
| `05_historie.txt` | `historie.py` (5) | 2372 | `46b1068b54912b47a73d33a47e493a08` |
| `06_raster.json` | `raster.py --was-waere-wenn --json` (6) | 1780 | `26ac3c089f777cbde86ad105fad7c642` |
| `06_raster.txt` | `raster.py` (6) | 1433 | `adc8bea31c577e60c7ecb77629594353` |
| `07_kosten.json` | `kosten.py --json` (7) | 5313 | `100438433791f3f01a8b6df459622a45` |
| `07_kosten.txt` | `kosten.py` (7) | 1463 | `67337361978f8fbf0982dae237887930` |
| `08_selbsttest_nachher.txt` | `test_etf_trendfolge.py` (8) | 361 | `b116f55b87f7d1a70c826b5300056225` |
| `09_datenstand_nachher.json` | `datenstand.py --json` (9) | 409 | `694dffe73916135fc2c9666b06667246` |
| `09_datenstand_nachher.txt` | `datenstand.py` (9) | 430 | `1a8f0c08c6530475de1600fe32246c7f` |
| `09_vergleich.txt` | `diff` der Ist-Zeilen (9) | 10 | `74e0ae81047b125b120aa2eae9c68f77` |
| `09_git_data.txt` | `git status --porcelain data/` (9) | 5 | `896d2b97148143c95ddcbd256a6c6131` |
| `10_dateizahl.txt` | `ls … \| wc -l` (9) | 14 | `6f8749947b355c20452062e4eda54f1d` |
| `e_backlog_probe.txt` | `WZ backlog --probe` (E) | 166 | `3d07ea18520adb0d86d60bd989aa73ec` |
| `e_backlog.txt` | `WZ backlog` (E) | 172 | `eddde9f20f1b8e01914663646ddeb365` |
| `e_kennung.txt` | `WZ kennung` (E) | 57 | `ead9fd26991096103356b3978aca784b` |
| `e_block.md` | Schreibwerkzeug (E) | 3160 | `c888987ba55851413dc1bbd8e7ce0072` |
| `e_journal_probe.txt` | `WZ journal … --probe` (E) | 251 | `24abe3ab24c063d9d1339df8e416dc47` |
| `e_journal.txt` | `WZ journal …` (E) | 256 | `6c548331a7acd37b2801ca4f176c7696` |

## Abweichungen

Keine erreicht ein Abbruchkriterium.

1. **0d:** Vor der Zeile `yfinance 1.2.0 pandas 2.3.3` stehen zwei Zeilen einer `NotOpenSSLWarning` von urllib3 (`ssl` gegen LibreSSL 2.8.3 gebaut) auf stderr; dieselbe Warnung steht am Kopf von `04_datenlauf.txt`. Import und Netzabruf gelangen trotzdem (rc 0). Der Auftrag verlangte die Versionszeile als erste Zeile.
2. **F6 widerlegt:** F6 meldete „yfinance fehlt in trading-env“; gemessen ist `yfinance 1.2.0` importierbar unter Python 3.9 (wie im Auftrag unter „Widerspruch zu F6“ erwartet).
3. **Laufzeit Schritt 4:** rund 10 s statt „rund 15 Minuten“ (Testauftrag Z. 39).
4. **Verworfen:** je Symbol genau 1 Kerze nach der Entscheidungskerze verworfen — die laufende Kerze des 14.10.2026; der Lauf fiel in die US-Handelszeit (18:50Z). Nicht grösser als 1, also kein Befund nach Testauftrag Z. 136.
5. **0c:** alle neun `*.db` je zwei gleiche md5 — kein Cronjob schrieb während der Sicherung.

## Offen

- **UCITS-Paare** (Register S-B1 Abschnitt 10a, Proxy-Tabelle 10a.4 leer): Kurse, Korrelation, Zulassung je Instrument brauchen den Betreiber (F4); nicht Teil von TB-161.
- **Backtest erst nach Rang 1** (BACKLOG Rang 4).
- Die 14 Kursdateien liegen nur am Mac unter `research/etf_trendfolge/daten/` (gitignoriert) und sind wegen `auto_adjust=True` nicht bit-reproduzierbar; ein späterer Neuabruf liefert andere sha256.
- Die Bestandstests (Testauftrag Schritt 11) und die ZIP (Schritt 12) sind nicht Teil von TB-161.

## In einfacher Sprache

Die Kurse der vierzehn ETFs wurden einmal von Yahoo geholt; das dauerte zehn Sekunden. Die Frage war, ob sie bis vor die Finanzkrise 2008 zurückreichen. **Sie tun es:** Anfang 2008 gibt es schon elf der vierzehn Reihen, aus sechs verschiedenen Bereichen (Aktien, Zinsen, Kredit, Metalle, Rohstoffe, Währungen) — verlangt waren acht aus vier. Ab 2009 sind alle vierzehn dabei. Der Kursordner der Aktien-Bots (`data/`) ist vorher und nachher bit für bit derselbe. Gewinn wurde keiner ausgerechnet. Offen bleibt, welche in Europa handelbaren Gegenstücke (UCITS) zu den US-ETFs du zulässt; und der Backtest kommt erst, wenn Rang 1 durch ist.
