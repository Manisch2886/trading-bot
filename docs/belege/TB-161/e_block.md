## EW — TB-161: S-B1-Datenlauf, Historie erfuellt (historie.py rc 0)
*Quelle: `docs/ERGEBNIS_TB-161_sb1_datenlauf.md`, Commits ⟨S0⟩ `d5c51bd`, ⟨M⟩ `725a15a`, ⟨F⟩ = der Commit „TB-161 Abgabe: Ergebnis, Backlog, Journal EW“ (er enthält diesen Block und kann seinen eigenen Hash nicht nennen).*

**Quelle:** Die Mac-Sitzung TB-161 hat am 14.10.2026 die offenen Schritte 2–9 aus `docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md` am aktuellen `main` ausgeführt: Datenstand vorher, Umgebungsprüfung, Selbsttest, den einzigen Netzschritt `datenlauf.py` (14 Signal-ETFs von Yahoo nach `research/etf_trendfolge/daten/`, gitignoriert), `historie.py`, `raster.py`, `kosten.py`, Selbsttest nachher, Datenstand nachher. Belegt unter `docs/belege/TB-161/`. Kein Backtest, keine Ertrags- oder Sharpe-Zahl, kein Code geändert. Kein Abbruch; kein Aufruf abgelehnt, keine Bestätigung verlangt.

### Was gemessen ist
- **0a/0b/0c:** HEAD `4979589` und die vier Einträge wie Soll; sha256 des Werkzeugs `979d8e83…e4fa` wie Soll; `BACKLOG.md` 498 Z. und `JOURNAL.md` 10999 Z. mit md5 wie Soll, `daten/` lag nicht vor; neun `*.db` gesichert, je zwei gleiche md5.
- **0d:** `yfinance 1.2.0 pandas 2.3.3`, `pandas_market_calendars 4.6.1`, je rc 0; davor eine `NotOpenSSLWarning` von urllib3 (LibreSSL 2.8.3) auf stderr.
- **Datenstand:** vorher und nachher `d9449faf…5f84` (223 Dateien), rc 0; Vergleich `IDENTISCH`; `git status --porcelain data/` leer.
- **Selbsttest:** vorher und nachher `64/64 Pruefungen bestanden.`, rc 0, beide Belege bytegleich.
- **Datenlauf:** rc 0, rund 10 s (18:50:21Z–18:50:31Z, nicht rund 15 Minuten); 14 Dateien, je 0 unvollständig und 1 Kerze nach der Entscheidungskerze verworfen (die laufende Kerze des 14.10.); letztes Datum je Symbol 2026-10-13; Manifest 14/14 vorhanden, sha256 `24d7624f…dff3`; 15 Dateien in `daten/`.
- **Erstes Datum je Symbol:** SPY 1993-01-29, IWM 2000-05-26, EFA 2001-08-27, EEM 2003-04-14, IEF 2002-07-30, TLT 2002-07-30, LQD 2002-07-30, HYG 2007-04-11, GLD 2004-11-18, SLV 2006-04-28, DBC 2006-02-06, DBA 2007-01-05, FXE 2005-12-12, FXY 2007-02-13.
- **Untergrenze am 2008-01-01:** 11 von 8 Instrumenten, 6 von 4 Klassen, erfüllt; **`historie.py` rc 0**; tragende Selektionsfalten 18 (Mindestzahl 3), ab 2009 alle 14 Instrumente; kein Block „Abweichungen zur Erwartung“ (Liste leer).
- **Raster:** N 5, N_historisch 653, N gesamt nominal 658, rc 0. **Kosten:** obere Schranke 1.80, Massstab 3.60 Prozentpunkte je Jahr, rc 0.

### Was offen bleibt
- UCITS-Paare (Register S-B1 Abschnitt 10a, Proxy-Tabelle 10a.4 leer): brauchen die Zulassung je Instrument durch den Betreiber.
- Der Backtest erst nach Rang 1.
- Die Kursdateien liegen nur am Mac (gitignoriert) und sind nicht bit-reproduzierbar (yfinance `auto_adjust=True`).

### In einfacher Sprache
Die Kurse der vierzehn ETFs wurden einmal geholt. Sie reichen weit genug zurück: Anfang 2008 gibt es schon elf von ihnen aus sechs Bereichen, verlangt waren acht aus vier. Der Kursordner der Aktien-Bots blieb unberührt. Gewinn wurde keiner ausgerechnet.

*Geschrieben 14.10.2026 von der Mac-Sitzung TB-161. Quellenvermerk: siehe Kopf.*
