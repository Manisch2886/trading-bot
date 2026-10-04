# TB-132 · V3 — Datenmessung zur Benchmark-Tagesreihe (nur Datumsspalte)

Stand: 02.10.2026 · Repo-HEAD `077945307bc3f0c3eff9a9e05ba61ec799f4cb5c` (Commit-Zeit 2026-10-02T18:11:14+02:00) · rein lesend.

**Gemessen ist der heutige Live-Bestand `data/` und `config/` der Repo-Wurzel — NICHT der spätere Snapshot des Laufs.**
Dateidatum der gelesenen Kursdateien: 150 Aktien-Dateien vom 2026-09-02, 24 Krypto-Dateien vom 2026-09-15. Der Bestand ist also seit rund zweieinhalb bis vier Wochen nicht fortgeschrieben; ein Snapshot aus frischeren Daten kann anders aussehen (v. a. am rechten Rand).

## 1. Was der Code tut (gelesen, nicht ausgeführt)

| Frage | Befund | Fundstelle |
|---|---|---|
| Bots und Märkte | 5 Krypto-Bots (`elliott_wave`, `t3_supertrend`, `rsi2_crypto`, `turtle_soup_crypto`, `volatility_breakout_crypto`), 4 Aktien-Bots (`elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`) | `research/vorregistrierung/registerdaten.py:130–140` |
| Universumsdateien | Krypto `config/top25_symbols.txt`, Aktien `config/sp500_top150.txt` | `registerdaten.py:142–145` |
| Symbolliste | nichtleere Zeilen der Universumsdatei, ohne `XAUTUSDT`/`PAXGUSDT` | `benchmark.py:142–145` |
| Kursdatei | `DATA_DIR/<symbol>_1d.csv` — für ALLE neun Bots die Tagesdatei, auch für den 1h-Bot `elliott_wave` und den 4h-Bot `t3_supertrend` | `benchmark.py:152`, `:253` |
| Datumsspalte | `open_time` | `benchmark.py:155` |
| Bildung des Tagesdatums | `pd.read_csv(pfad, parse_dates=["open_time"])`, dann `pd.DatetimeIndex(df["open_time"])`. **Keine Zeitzonenangabe, kein `normalize()`, kein `floor`, kein Sortieren, keine Entdopplung.** Das Datum ist genau das, was pandas aus der Zeichenkette liest. | `benchmark.py:155`, `:159–160` |
| Zeilenfilter | `dropna(subset=["close"])` — Zeilen ohne Schlusskurs fallen weg; leere Datei und fehlende Datei werden still übersprungen (`continue`) | `benchmark.py:153–158` |
| Pfade | ohne Selektionsmodus `DATA_DIR = <Repo>/data`, `CONFIG_DIR = <Repo>/config`; unter dem Modus Snapshot-Wurzel bzw. `<Snapshot>/config` | `shared/paths.py:685–693` |

Folge für „je Bot“: Innerhalb eines Marktes haben alle Bots **dieselbe** Symbolliste und **dieselben** Dateien. Bot-spezifisch wird die Reihe erst durch den Handelbar-Schnitt (`tagesgenau`, `benchmark.py:164–188`, Datum aus `faltenschranke_messung.loader_lesart`). Dieser Schnitt ist hier **nicht** angewandt (siehe 6).

Format der Datumsspalte, über alle 174 gelesenen Dateien gemessen (Krypto 24 / Aktien 150):

| | Krypto | Aktien |
|---|---|---|
| Zeilen gesamt | 44 163 | 1 417 557 |
| Rohwerte, die nicht `JJJJ-MM-TT` sind | 0 | 0 |
| dtype nach `parse_dates` | `datetime64[ns]` (24/24) | `datetime64[ns]` (150/150) |
| Zeitzone | keine (naiv) | keine (naiv) |
| NaT | 0 | 0 |
| Zeitpunkte ≠ Mitternacht | 0 | 0 |
| Dateien mit nicht monoton steigendem Datum | 0 | 0 |

Die Datumsspalte enthält also durchweg reine Tagesdaten ohne Uhrzeit; dass `tagesschluss` nicht normalisiert, ist am heutigen Bestand folgenlos.

## 2. Je Bot: Symbole und fehlende Dateien

| Bot | Markt | Symbole (nach Ausschluss) | ohne Kursdatei | Datei ohne Zeilen |
|---|---|---|---|---|
| elliott_wave | krypto | 24 | 0 | 0 |
| t3_supertrend | krypto | 24 | 0 | 0 |
| rsi2_crypto | krypto | 24 | 0 | 0 |
| turtle_soup_crypto | krypto | 24 | 0 | 0 |
| volatility_breakout_crypto | krypto | 24 | 0 | 0 |
| elliott_wave_stocks | aktien | 150 | 0 | 0 |
| rsi2_mean_reversion | aktien | 150 | 0 | 0 |
| turtle_soup_stocks | aktien | 150 | 0 | 0 |
| volatility_breakout | aktien | 150 | 0 | 0 |

`top25_symbols.txt` hat 25 Zeilen (Zeile 16 `XAUTUSDT` wird ausgeschlossen → 24); `sp500_top150.txt` hat 150 Zeilen. Beide Dateien enden ohne Zeilenumbruch (`wc -l` zeigt deshalb 24 / 149). Keine doppelten Symbole in den Listen.

## 3. Krypto (Handelstage = Kalendertage) — gilt identisch für alle fünf Krypto-Bots

| Messung | Wert |
|---|---|
| Zeitraum (früheste erste / späteste letzte Zeile) | 2017-08-17 … 2026-09-14 (3 316 Kalendertage) |
| (a) Symbole mit ≥ 1 fehlendem Kalendertag zwischen erster und letzter Zeile | 0 |
| (a) fehlende Symbol-Tage gesamt | 0 |
| (b) Kalendertage im Zeitraum ohne Zeile irgendeines Symbols | 0 |
| (c) Symbole, deren Reihe vor der spätesten letzten Zeile endet | 0 (alle 24 enden am 2026-09-14) |
| (d) doppelte Tagesdaten (Summe über die Dateien) | 0 |

Erste Zeile je Jahr (Zahl der Symbole): 2017: 3 · 2018: 3 · 2019: 3 · 2020: 4 · 2023: 4 · 2024: 1 · 2025: 5 · 2026: 1.

## 4. Aktien — gilt identisch für alle vier Aktien-Bots

Markt-Kurstage = Vereinigung der Tagesdaten aller 150 Symbole.

| Messung | Wert |
|---|---|
| Zeitraum | 1962-01-02 … 2026-09-01 |
| Markt-Kurstage | 16 275 |
| (a) Symbole mit ≥ 1 fehlendem Markt-Kurstag zwischen erster und letzter Zeile | 2 |
| (a) fehlende Symbol-Tage gesamt | 2 |
| (a) Befunde (Datum, Symbol) | 1974-06-03 LMT · 2026-08-10 MNST |
| (b) Symbole, deren Reihe vor dem letzten Markt-Kurstag endet | 0 (alle 150 enden am 2026-09-01) |
| (c) doppelte Tagesdaten (Summe) | 0 |
| (d) Markt-Kurstage mit < 10 Symbolen | 0 (Minimum über alle Markttage: 15 Symbole) |
| Zusatz: Markttage mit < 50 % der „aktiven“ Symbole (erste ≤ Tag ≤ letzte Zeile) | 0 |
| Zusatz: Wochenendtage in den Daten | 0 |
| Zusatz: Wochentage im Zeitraum ohne Markt-Kurstag | 596 (Feiertage / Sonderschliessungen, siehe (e)) |

Zu den zwei Lücken: am 1974-06-03 haben 34 von 35 aktiven Symbolen eine Zeile, am 2026-08-10 149 von 150 — es fehlt jeweils genau das genannte Symbol, der Markttag selbst ist nicht dünn.

Erste Zeile je Jahrzehnt (Zahl der Symbole): 1960er: 17 · 1970er: 22 · 1980er: 44 · 1990er: 25 · 2000er: 19 · 2010er: 15 · 2020er: 8.

### (e) Vergleich mit dem NYSE-Kalender

`import pandas_market_calendars` schlägt in der Geräte-Shell **fehl** (`ModuleNotFoundError`; Python 3.10.12 des Systems). Nach dem Wortlaut des Auftrags entfällt (e) damit.

**Ersatzmessung, ausdrücklich ausserhalb der Regelbedingung:** Das Paket liegt im Repo-venv `trading-env/lib/python3.9/site-packages` (4.6.1, wie `requirements.lock:51`; `exchange_calendars` 4.5.6). Dieser Ordner wurde **hinten** an `sys.path` gehängt (numpy/pandas weiter aus dem System, pandas 2.3.3), nichts installiert, `PYTHONDONTWRITEBYTECODE=1`; geprüft: danach 0 neue Dateien in den betroffenen Paketordnern. Ergebnis `get_calendar("NYSE").valid_days(1962-01-02 … 2026-09-01)`:

| | Tage |
|---|---|
| NYSE-Kalendertage | 16 275 |
| Markt-Kurstage der Daten | 16 275 |
| nur im Kalender | 0 |
| nur in den Daten | 0 |

Einschränkung: Python 3.10 der Shell lädt ein für 3.9 installiertes Paket; das ist nicht die Lock-Umgebung. Die übrigen Messwerte sind mit und ohne diesen Pfad identisch (JSON-Vergleich).

## 5. pandas-Version der Geräte-Shell

pandas **2.3.3**, Python 3.10.12 (System-`/usr/bin/python3`). `requirements.lock:52` nennt ebenfalls `pandas==2.3.3` (und `numpy==2.0.2`); das venv `trading-env` ist ein macOS-venv für Python 3.9 und in der Linux-Shell nicht startbar (`bin/python3` ist dort ein toter Verweis).

Randbeobachtung an **synthetischen** Zahlen (keine Kursdaten): `DataFrame.pct_change()` ohne Argument füllt in 2.3.3 innere und nachlaufende NaN vorwärts (`fill_method='pad'`) — ein fehlender Symbol-Tag ergibt dort Rendite 0,0 statt NaN, der Folgetag trägt die ganze Zweitagesrendite; dazu eine `FutureWarning` („default fill_method='pad' … is deprecated“). Führende NaN bleiben NaN. `benchmark.py:205` ruft `pct_change()` ohne Argument. Betroffen wären am heutigen Bestand genau die zwei Symbol-Tage aus 4 (a).

## 6. Nicht gemessen

1. **Zeilen ohne Schlusskurs.** `tagesschluss` wirft sie weg (`benchmark.py:156`). Da nur die Datumsspalte gelesen wurde, ist unbekannt, ob es solche Zeilen gibt; jede davon wäre eine zusätzliche Lücke, die hier nicht mitgezählt ist.
2. **Handelbar-Schnitt je Bot** (`tagesgenau`, `loader_lesart`). Gemessen ist über die volle Dateilänge. Bot-spezifische Unterschiede innerhalb eines Marktes entstehen erst dort; welche der zwei Aktien-Lücken nach dem Schnitt bzw. in einer Falte liegen, ist nicht geprüft.
3. **Der Snapshot des Laufs.** Gemessen ist der Live-Bestand vom 02.10.2026.
4. **1h-/4h-Dateien** (25 bzw. 24 Stück) und die Datei `XAUTUSDT_1d.csv` — der Benchmark liest sie nicht.
5. (e) im Sinne des Auftrags (reguläre Importierbarkeit) — nur als Ersatzmessung, siehe oben.
6. Projektfunktionen wurden nicht ausgeführt; `ergebnisse/`, Trade-Listen und `BACKLOG*.md` nicht gelesen.

## 7. Verfahren und Gegenprobe

- Skript: `/tmp/tb132/v3_daten.py` in der Geräte-Shell (265 Zeilen, SHA-256 beginnt `53598c0cbbb37a87`); Rohausgaben `/tmp/tb132/v3_ohne_venv.json` und `/tmp/tb132/v3_mit_venv.json`. Liest je Datei `pd.read_csv(pfad, usecols=["open_time"], parse_dates=["open_time"])` (dieselbe Datumsbildung wie `tagesschluss`) und zusätzlich dieselbe Spalte als Text für die Formatprüfung.
- Gegenprobe ohne pandas (`csv`-Modul, nur Feld 0, Datum als Text): Krypto 24 Symbole / 44 163 Zeilen / 0 fehlende Symbol-Tage; Aktien 150 Symbole / 16 275 Markttage / 2 fehlende Symbol-Tage (dieselben zwei). Stimmt überein.
- git nur `--no-optional-locks rev-parse` und `log`; nichts im Repo angelegt oder geändert.
