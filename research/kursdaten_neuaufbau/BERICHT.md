# TB-34 — Kursdaten neu aufbauen: die Untersuchung

**Stand: 2026-09-15.** Rein lesend. Es wurde **keine Kursdatei verändert**,
kein Bot-Code angefasst, kein Parameter übernommen und kein Raster gerechnet.

---

## 0. Die beiden Zahlen zuerst

**Was ändert der Neuaufbau je Datei?** Die Zeilenzahl nach dem Lauf steht
erst nach dem Lauf fest — der Endpunkt ist aus der Cloud gesperrt. Gemessen
und hier belegt ist dagegen, **was heute falsch ist**, je Datei:

| | Wieviele | Ausmass |
|---|---|---|
| `*_1d.csv`, **erste** Kerze | **24 von 24** | deckt **6 bis 16 von 24 Stunden** ab, und ist auf die letzte Stelle das Aggregat genau dieser Stunden — also **abgeleitet**, nicht abgerufen |
| `*_1d.csv`, **letzte** Kerze | **24 von 24** | deckt **13 von 24 Stunden** ab, ebenfalls abgeleitet |
| `*_4h.csv`, **letzte** Kerze | **24 von 24** | die 1h-Datei belegt **1 von 4** Stunden, und die 4h-Kerze stimmt mit deren Aggregat **nicht** überein — beide Dateien sind am Rand angeschnitten, verschieden weit |
| `*_4h.csv`, **erste** Kerze | **5 von 24** | `BMTUSDT` 1/4, `PEPEUSDT` 2/4, `ZKCUSDT` 2/4, `ENSOUSDT` 3/4, `WLDUSDT` 3/4 — das sind Listing-Ränder und nach dem Neuaufbau voraussichtlich **richtig** |
| `*_1h.csv`, **letzte** Kerze | unbelegbar | es gibt keine feinere Datei. Dass sie angeschnitten ist, folgt aus dem 4h-Befund, nicht aus der Datei selbst |

**Welche Programme rechnen heute auf dem veralteten Stand?**

> **37 Module lesen `data/` unmittelbar, 64 weitere über
> `load_all_symbol_data()` — zusammen 101.** Keines von ihnen prüft, wie alt
> der Stand ist. **Die neun `forward_test.py` sind nicht dabei:** alle neun
> holen live, keiner liest eine Datei aus `data/`.

Der Stand von `data/`, gemessen am jüngsten Zeitstempel **in** den Dateien
(nicht an `mtime` — ein frischer Klon setzt die zurück):

| Letzte Kerze | Dateien |
|---|---|
| 2026-08-30 | 1 (`XAUTUSDT_1h.csv`, ausgeschlossenes Symbol) |
| 2026-08-31 | 91 (Krypto) |
| 2026-09-01 | 150 (Aktien) |

Heute ist der **2026-09-15**. Der Krypto-Bestand ist **zwei Wochen** alt, der
Aktienbestand zwei Wochen minus einen Tag.

---

## 1. Wie das gemessen wurde

Zwei Werkzeuge, beide in diesem Ordner bzw. unter `shared/`, beide ohne Netz:

| Werkzeug | Was es beantwortet |
|---|---|
| [`shared/zeitabdeckung.py`](../../shared/zeitabdeckung.py) | Deckt die erste und letzte Kerze jeder Datei ihren Zeitraum ab? |
| [`datenwege.py`](datenwege.py) | Wer liest `data/`, wer holt live, wer schreibt hinein? |
| [`probelauf.py`](probelauf.py) | Verhält sich der Neuaufbau auf den **echten** 72 Dateien so wie auf Kunstreihen? |

Alle drei sind wiederholbar und lesen den Quelltext bzw. die Dateien, nicht
die Dokumentation. `datenwege.py` sucht über den **Syntaxbaum**, damit ein
`read_csv` in einem Kommentar nicht mitzählt.

```bash
python3 shared/zeitabdeckung.py --json research/kursdaten_neuaufbau/daten/zeitabdeckung_vorher.json
python3 research/kursdaten_neuaufbau/datenwege.py --json daten/datenwege.json
python3 research/kursdaten_neuaufbau/probelauf.py --json daten/probelauf.json
```

---

## 2. Der Teilkerzen-Befund, Symbol für Symbol

Gemessen von `zeitabdeckung.py`, Rohdaten in
[`daten/teilkerzen_gemessen.json`](daten/teilkerzen_gemessen.json).
Gelesen wird `11/24` als „die 1h-Datei belegt 11 der 24 Stunden dieses Tages".

| Symbol | 1d Zeilen | 1d erste | 1d letzte | 4h erste | 4h letzte |
|---|---:|---:|---:|---:|---:|
| AAVEUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| ADAUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| BMTUSDT | 532 | 9/24 | 13/24 | **1/4** | 1/4 |
| BNBUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| BTCUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| DOGEUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| ENAUSDT | 882 | 16/24 | 13/24 | 4/4 | 1/4 |
| ENSOUSDT | 322 | 15/24 | 13/24 | **3/4** | 1/4 |
| ETHUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| LINKUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| NEARUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| PEPEUSDT | 1215 | **6/24** | 13/24 | **2/4** | 1/4 |
| PROMUSDT | 1264 | 16/24 | 13/24 | 4/4 | 1/4 |
| PUMPUSDT | 355 | 12/24 | 13/24 | 4/4 | 1/4 |
| SOLUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| SUIUSDT | 1217 | 12/24 | 13/24 | 4/4 | 1/4 |
| TRUMPUSDT | 590 | 16/24 | 13/24 | 4/4 | 1/4 |
| TRXUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| UNIUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| UUSDT | 231 | 16/24 | 13/24 | 4/4 | 1/4 |
| WLDUSDT | 1135 | 15/24 | 13/24 | **3/4** | 1/4 |
| XRPUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| ZECUSDT | 1826 | 11/24 | 13/24 | 4/4 | 1/4 |
| ZKCUSDT | 351 | 10/24 | 13/24 | **2/4** | 1/4 |

**Das bestätigt TB-31 unabhängig** — dort stand „6 bis 16 Stunden" für die
erste und „13 Stunden" für die letzte Tageskerze, gemessen mit einem ganz
anderen Verfahren. Hier ist es aus den Dateien selbst nachgerechnet, ohne
Netz und ohne Vorwissen.

**Der Nachweis, nicht nur der Verdacht:** in allen 48 Tagesfällen stimmt die
Tageskerze **auf die letzte Stelle** mit dem Aggregat genau der vorhandenen
Stunden überein (open = erste Stunde, high = Max, low = Min, close = letzte
Stunde, volume = Summe — die Rechnung aus `build_daily_crypto_data.py`). Eine
nativ abgerufene Tageskerze könnte das nur zufällig.

Bei den **4h-Dateien** ist es umgekehrt: dort stimmt die letzte Kerze mit dem
Aggregat der einen vorhandenen Stunde **nicht** überein. Sie enthält
Kursbewegung, die in der 1h-Datei fehlt — beide wurden angeschnitten, aber zu
leicht verschiedenen Zeitpunkten.

### Zwei Nebenbefunde

**Eine echte Datenlücke.** 13 Krypto-1h-Dateien fehlen **drei** Stunden ab
dem **2021-09-29 07:00**, `PROMUSDT_1h.csv` fehlt **eine** ab dem
2023-03-24 13:00. Das ist keine Teilkerze, sondern eine Lücke mitten in der
Reihe — und sie steht **nicht** in `docs/DATENLUECKEN.md`, das nur
Forward-Test-Ausfälle führt. Ob der Endpunkt sie kennt, entscheidet sich beim
Lauf; `kursdaten_neuaufbau.py` weist gefüllte Lücken gesondert aus.

**19 verwaiste Dateien.** `data/` enthält `*_15m.csv` für 19 Symbole —
Reste des 2026 verworfenen 15-Minuten-Versuchs (Protokoll 3.2: `fetch_15m_data.py`
existiert nicht mehr). Kein Programm liest sie. Sie werden hier nur benannt,
nicht angefasst.

---

## 3. Woher die Daten wirklich kommen

### 3.1 Die neun `forward_test.py`: **alle neun live, keiner aus `data/`**

Mechanisch festgestellt (kein `read_csv` auf `DATA_DIR` in irgendeinem der
neun Module):

| Bot | Quelle | Fenster |
|---|---|---|
| `elliott_wave` | `fetch_binance_data.fetch_historical_data`, 1h | 90 Tage |
| `t3_supertrend` | dieselbe, 4h | 120 Tage |
| `rsi2_crypto` | dieselbe, 1d | 400 Tage |
| `turtle_soup_crypto` | dieselbe, 1d | 400 Tage |
| `volatility_breakout_crypto` | dieselbe, 1d | 400 Tage |
| `elliott_wave_stocks` | `fetch_stock_data.fetch_historical_data` (yfinance), 1d | 3 Jahre |
| `rsi2_mean_reversion` | dieselbe | 3 Jahre |
| `turtle_soup_stocks` | dieselbe | 2 Jahre |
| `volatility_breakout` | dieselbe | 3 Jahre |

**Daraus folgt zweierlei.** Erstens: der **Live-Betrieb** ist vom veralteten
`data/` nicht betroffen — die Paper-Trades entstehen auf frischen Daten.
Zweitens: deshalb ist es niemandem aufgefallen. Der Teil des Systems, der
täglich läuft, fragt `data/` nie.

### 3.2 Wer `data/` liest

**37 Module unmittelbar.** Nach Gruppen:

| Gruppe | Module | Was sie rechnen |
|---|---:|---|
| `multi_symbol_optimise.py` | 9 | die **Haupt-Optimierung** jedes Bots |
| `backtest_*.py` (Demo-Block) | 8 | Einzelsymbol-Backtests von Hand |
| `research/` | 6 | `vorregistrierung/benchmark.py`, `vorregistrierung/messgroessen.py`, `exposure_messung/auswertung.py`, `hrp_portfolio/bh_reference.py`, `trend_overlay/market_proxies.py`, `datenluecke_wurzelkorrektur/signalverschiebung.py` |
| `optimise_*.py`, `walk_forward.py` | 4 | Einzelsymbol-Raster |
| `experiment_*.py` (BTC-Regimefilter) | 4 | Regimefilter-Versuche |
| `buy_and_hold_benchmark.py` | 3 | der Pflicht-Gegencheck jeder Parameterbewertung |
| `zigzag_indicator.py` (Demo-Block) | 2 | Indikator-Demonstration |
| `shared/build_daily_crypto_data.py` | 1 | liest 1h, schreibt 1d |

**64 Module mittelbar** über `load_all_symbol_data()` — den Trichter, durch
den in diesem Projekt fast alles an die Kursdateien kommt: die neun
`equity_simulation.py`, die `multi_symbol_walk_forward.py`, `shared/kurven_lauf.py`,
`shared/determinismus_lauf.py` und der Grossteil der Untersuchungen unter
`research/`.

**Zusammen 101 Module.** Kein einziges prüft, wie alt der Stand ist. Die
`shared/ergebniskurven.py` merkt es indirekt (eine längere Kurve heisst
VERALTET) — aber nur, wenn `data/` sich *ändert*, nicht, wenn es stehen
bleibt.

### 3.3 Wer `data/` schreibt

**8 Abrufskripte und 1 Ableitungsskript.** Zwei Eigenschaften teilen sie
alle:

1. **Sie überschreiben die Datei vollständig** (`df.to_csv(pfad, index=False)`).
   Keines hängt an.
2. **Keines schliesst die laufende Kerze aus.** Das ist der Grund, warum alle
   72 Krypto-Dateien mit einer Teilkerze enden — und es würde nach jedem
   künftigen Abruf wieder so sein.

Dazu die Fenster:

| Skript | Fenster | Anmerkung |
|---|---|---|
| `shared/fetch_multi_data.py` (1h) | `"1825 day ago UTC"` | **vom Betreiber am 14.09.2026 lokal auf `"1 Jan, 2017"` geändert** — die Änderung ist noch nicht auf `main` |
| `strategies/t3_supertrend/fetch_4h_data.py` | `"1825 day ago UTC"` | dasselbe |
| `strategies/rsi2_crypto/fetch_1d_data.py` | `"3650 day ago UTC"` | **unverändert relativ** |
| `strategies/volatility_breakout_crypto/fetch_1d_data.py` | `"3650 day ago UTC"` | **unverändert relativ** |
| 4× `fetch_stock_data.py` | `period="max"` | schneidet nicht ab |
| `shared/build_daily_crypto_data.py` | — | leitet aus 1h ab |

> ⚠️ **Ein Befund, der im Auftrag nicht stand.** Der Betreiber hat die beiden
> Skripte mit dem Fünf-Jahres-Fenster korrigiert. Die **beiden nativen
> Tagesabrufe** stehen weiterhin auf `"3650 day ago UTC"`. Heute schneidet
> das nichts weg — Binance gibt es erst seit Juli 2017, also weniger als zehn
> Jahre. **Ab Sommer 2027 schneidet es.** Und es ist derselbe Fehlertyp, der
> gerade behoben wird: ein Zeitfenster, das sich mit dem Abruftag mitbewegt.
> Hier nur benannt; die Dateien werden in TB-34 nicht angefasst (sie gehören
> zur Abruflogik, und die Änderung ist eine eigene, ausdrückliche
> Entscheidung des Betreibers).

`shared/fetch_binance_data.py` enthält Zugangsdaten und ist gitignoriert; ob
es die laufende Kerze streicht, lässt sich hier nicht am Quelltext prüfen.
**Es ist aber am Ergebnis bewiesen:** die Dateien enden mit einer Teilkerze,
also streicht es sie nicht.

---

## 4. Die Cron-Frage — berichtet, nicht entschieden

### Was für einen täglichen Abruf spricht

1. **Der Stand ist zwei Wochen alt, und 101 Module rechnen darauf.** Es gibt
   keine Stelle im System, die das meldet.
2. **Eine Lücke sieht in den Zahlen genauso aus wie „kein Signal"** — das
   steht seit dem Vorfall vom 11.09.2026 in `CLAUDE.md`, und es gilt für
   veraltete Kursdaten genauso.
3. **Die anstehende Neuselektion** (TB-30b) rechnet auf `data/`. Je frischer
   und je vollständiger, desto weniger muss hinterher nachgezogen werden.

### Was dagegen spricht — in dieser Form

1. **Es gibt kein Werkzeug, das anhängt.** `binance_historie.py` verlängert
   nach **vorn**. `kursdaten_neuaufbau.py` baut **vollständig** neu. Die
   `fetch_*.py` **überschreiben**. Ein täglicher Cronjob müsste also eines
   von beiden tun: entweder 72 Dateien neu schreiben (rund 3000 Anfragen,
   184 MB Sicherung, jedes Mal) oder mit den vorhandenen `fetch_*.py`
   überschreiben — und die schreiben die **laufende Kerze** mit.
2. **Ein täglicher Abruf mit den heutigen Skripten macht den Fehler zur
   Gewohnheit.** Heute steht eine einzelne Teilkerze am Rand, weil einmal von
   Hand abgerufen wurde. Ein Cronjob um 04:00 Uhr schriebe **jeden Tag** eine
   Teilkerze ans Ende — und beim nächsten Lauf säße sie mitten in der Reihe.
3. **Die Vorregistrierung hat einen Datenstand-Hash auf der Sperrliste**
   (`docs/VORREGISTRIERUNG_neuselektion.md`). Ein täglich wechselnder
   Kursdatenbestand wechselt ihn täglich mit.
4. **`ergebniskurven.py` meldete dann täglich VERALTET.** Das ist genau die
   Lage, vor der sein eigener Modulkopf warnt: „eine Prüfung, die deshalb
   jeden Tag anschlägt, meldet nicht mehr, sondern verdeckt." Es gibt dafür
   `--nur-abweichung`, aber die Abwägung gehört benannt.
5. **Ein Abruf, der 72 Dateien neu schreibt, ist etwas anderes als einer, der
   sie verlängert** — so steht es im Auftrag, und die Messung bestätigt es:
   der Neuaufbau ändert *jede* Zeile der Tagesdateien (sie werden nativ statt
   abgeleitet), eine Verlängerung ändert *eine*.

### Was daraus folgt

Die Reihenfolge, nicht die Entscheidung:

1. **Zuerst der Neuaufbau von Hand** (TB-34, dieser Schritt) — einmalig, mit
   Sicherung, mit Vergleich.
2. **Dann die Wache per Cron** — `zeitabdeckung.py`, rein lesend, 40 Sekunden,
   Vorschlagszeile in `shared/README_KURSDATEN.md` Abschnitt 5.
3. **Ein anhängendes Abrufwerkzeug**, falls der Betreiber einen täglichen
   Abruf will. Es gibt es noch nicht, und es zu bauen ist eine eigene
   Aufgabe — kein Nebenprodukt von TB-34.

Eine Cron-Zeile für den **Abruf** steht deshalb bewusst **nicht** im README.
Sie einzutragen, bevor es ein Werkzeug gibt, das anfügt statt zu ersetzen,
wäre die falsche Reihenfolge.

---

## 5. Was der Probelauf zeigt

`probelauf.py` fährt den Neuaufbau im Trockenlauf gegen **alle 72 echten
Kursdateien** — mit einer Gegenstelle, die aus der jeweiligen Datei selbst
gebaut wird (dieselben Kerzen, davor 500 zusätzliche, an den Rändern
abweichende Werte). **295 von 295 Prüfungen bestehen:**

* je Datei **0** Abweichungen im Innern,
* **1** Randabweichung bei `1h`/`4h`, **2** bei `1d` — genau dort, wo die
  Teilkerzen sitzen,
* die Zeilenzahl wächst um genau den Vorlauf,
* im Trockenlauf wird nichts geschrieben, und
* eine künstlich gesetzte Abweichung **mitten** in `BTCUSDT_1d.csv`
  verhindert das Schreiben, ohne die Repo-Datei anzufassen.

Die Schreibprobe läuft auf einer **Kopie** in einem temporären Ordner: zweimal
schreiben ergibt byte-identische Dateien, die Sicherung hält den alten Stand
zeichengleich, und `--zurueckspielen` stellt ihn wieder her.

`git diff origin/main HEAD --name-only` listet **keine** Datei unter `data/`.

---

## 6. Was nach dem Lauf neu zu rechnen ist

| Was | Womit | Erwartung |
|---|---|---|
| Teilkerzen-Wache | `python3 shared/zeitabdeckung.py --datenbeginn <bericht.json>` | **kein Befund** für die 72 Krypto-Dateien |
| Faltenpläne | `python3 research/krypto_historie/faltenplan.py --json ...` | **neue Zahlen** — die Platzhalter aus TB-31 sind überholt |
| Ergebniskurven | `python3 shared/ergebniskurven.py` | **5× ABWEICHEND** (Krypto), **4× AKTUELL** (Aktien). Meldet ein Aktien-Bot ABWEICHEND, hat der Lauf etwas angefasst, was er nicht durfte |
| Datenstand-Hash der Vorregistrierung | — | **ändert sich** (siehe unten) |

> ⚠️ **Der Datenstand-Hash der Vorregistrierung ändert sich — und das ist
> kein Amendment.** Er steht in `docs/VORREGISTRIERUNG_neuselektion.md` auf
> der Sperrliste. Änderte er sich **nach** dem Selektionslauf, wäre das ein
> Bruch des Registers. Er ändert sich **vorher** — und genau das ist der
> Grund, warum TB-34 **vor** TB-30b kommt. Wäre erst selektiert und dann
> geladen worden, hätte die Selektion auf einer Historie stattgefunden, die
> es danach nicht mehr gibt.

**Die Ergebniskurven bitte NICHT vorschnell neu erzeugen.** `ABWEICHEND` ist
nach dem Laden richtig. Ob und wann neu gerechnet wird, entscheidet der
Betreiber, und es gehört in denselben Schritt wie die Neuselektion.
