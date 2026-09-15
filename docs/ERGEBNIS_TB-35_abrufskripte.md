# Ergebnis TB-35 — Abrufskripte haltbar machen

**Kurzfassung zum Kopieren. Stand 2026-09-15.**

---

## Die zwei Sätze zuerst

> **Alle acht Abrufskripte schrieben die laufende Kerze, und alle acht
> überschrieben ihre Datei vollständig.** Ein einziger Handstart genügte, um
> den am 15.09.2026 frisch geladenen Kursdatenbestand wieder zu verunreinigen
> und den Datenstand-Hash der Vorregistrierung unbemerkt zu ändern.

> **Acht von acht sind geändert. Keines war unerreichbar.** Die laufende Kerze
> entsteht in der Datei gar nicht erst; die zwei mitwandernden Zeitfenster sind
> weg; eine Wache meldet, wenn ein Abruf eine Datei kürzer zurücklässt.

---

## 1. Was geändert wurde

| Abrufskript | Raster | laufende Kerze | `LOOKBACK` | Wache |
|---|---|---|---|---|
| `shared/fetch_multi_data.py` | Krypto 1h | ✅ | war fest | ✅ |
| `strategies/t3_supertrend/fetch_4h_data.py` | Krypto 4h | ✅ | war fest | ✅ |
| `strategies/rsi2_crypto/fetch_1d_data.py` | Krypto 1d | ✅ | **korrigiert** | ✅ |
| `strategies/volatility_breakout_crypto/fetch_1d_data.py` | Krypto 1d | ✅ | **korrigiert** | ✅ |
| `strategies/elliott_wave_stocks/fetch_stock_data.py` | Aktien 1d | ✅ | `period="max"` | ✅ |
| `strategies/rsi2_mean_reversion/fetch_stock_data.py` | Aktien 1d | ✅ | `period="max"` | ✅ |
| `strategies/turtle_soup_stocks/fetch_stock_data.py` | Aktien 1d | ✅ | `period="max"` | ✅ |
| `strategies/volatility_breakout/fetch_stock_data.py` | Aktien 1d | ✅ | `period="max"` | ✅ |

**Nicht erreichbar war kein Abrufskript**, sondern das Modul, an dem vier von
ihnen hängen: `shared/fetch_binance_data.py` ist gitignoriert und liegt nur auf
dem Rechner des Betreibers. Es wurde **nicht gelesen, nicht umgangen, nicht
nachgebaut.**

---

## 2. Was ohne diese Datei offenbleibt — genau drei Dinge

| # | Was | Wo es erledigt wird |
|---|---|---|
| 1 | **In welcher Form `open_time` wirklich kommt.** `abrufschutz` deckt alle vier denkbaren Formen ab (Zeichenkette, Zeitstempel, Sekunden, Millisekunden), jede im Selbsttest belegt. Welche es ist, kann nur der Mac zeigen. | Testauftrag Schritt 7, Zeile `letzte Kerze abgeschlossen: True` |
| 2 | **Ein echter Lauf gegen Binance/yfinance.** Aus der Cloud gesperrt (403). | Testauftrag Schritte 7–8, über `echtlauf.py` in einen Wegwerf-Ordner |
| 3 | **Dass sie genau einmal existiert.** Neun Module hängen daran, fünf im täglichen Betrieb. | **Entscheidung des Betreibers** — `research/abrufskripte/BERICHT.md`, Punkt 4a |

---

## 3. Was geliefert ist

| Datei | Was |
|---|---|
| `shared/abrufschutz.py` | **neu** — die Regel „nur abgeschlossene Zeiträume" **und** die Wache; eigenständiges Werkzeug, Rückgabewert 1 bei Befund |
| `shared/test_abrufschutz.py` | **neu** — **77/77**, zwei Sätze Mutationsproben |
| die acht Abrufskripte | Filter **vor** dem Schreiben, Wache mitlaufend |
| `research/abrufskripte/abrufwege.py` | **neu** — stellt über den Syntaxbaum fest, wer an `fetch_binance_data` hängt |
| `research/abrufskripte/echtlauf.py` | **neu** — echter Abruf gegen den echten Endpunkt, **ohne `data/` zu erreichen** |
| `research/abrufskripte/BERICHT.md` | **neu** — das Ergebnis, samt der Fragen, die berichtet und nicht entschieden werden |
| `docs/UEBERGABE_TB-35_abrufskripte.md` | Übergabe-Zusammenfassung |
| `docs/TESTAUFTRAG_TB-35_abrufskripte.md` | autonom ausführbar am Mac |

---

## 4. Die zwei Entscheidungen, mit Begründung

### 4.1 Anhängen oder überschreiben? → **Überschreiben bleibt**

Der Einwand aus der Aufgabe gibt den Ausschlag: *ein anhängendes Werkzeug, das
sich irrt, lässt den Fehler dauerhaft stehen; ein überschreibendes ist beim
nächsten Lauf wieder in Ordnung.* Dazu drei Gründe aus dem Projekt:

1. **Überschreiben war nie das Problem — die Teilkerze am Ende war es.** Mit
   §1 ist die Ursache weg.
2. **Für „verlängern" gibt es schon ein Werkzeug**, und dessen Wert liegt in
   einer Zusicherung, die ein Abrufskript nicht geben kann:
   `shared/binance_historie.py` schreibt jede vorhandene Zeile zeichengleich
   zurück. Ein drittes Werkzeug mit einem vierten Vertrag wäre die
   Unübersichtlichkeit, die TB-34 beklagt hat.
3. **Anhängen braucht eine Konfliktregel, die niemand entscheiden kann:** was
   gilt, wenn der Endpunkt eine gespeicherte Kerze anders liefert als beim
   letzten Mal?

Der Preis wird nicht weggeredet, sondern abgesichert — dafür gibt es §4.

### 4.2 Wache im Abrufskript oder daneben? → **Beides, mit genau einer Umsetzung**

* **Daneben**, weil die Logik genau einmal existieren soll (acht Kopien wären
  die Doppelführung), und weil das Werkzeug auch dann taugt, wenn eine Datei
  auf einem **anderen** Weg kürzer geworden ist.
* **Trotzdem im Abrufskript**, weil die Wache einen Vergleichswert von **vor**
  dem Lauf braucht. Wer sie erst hinterher startet, hat nichts mehr zum
  Vergleichen. Und der gefährliche Fall ist gerade der **unangekündigte
  Handstart**, bei dem niemand an eine zweite Prüfung denkt.

**Blockiert wird nie.** Gemeldet wird je Datei sofort, am Ende zusammengefasst,
Rückgabewert 1 — dieselbe Hausregel wie `shared/kursdaten.py`. Geschrieben wird
trotzdem.

**Drei Kriterien**, weil eines nicht reicht: *weniger Zeilen*, *späterer
Beginn*, *früheres Ende* (dazu: Datei verschwunden). Eine Datei kann bei
gleicher Zeilenzahl später beginnen oder früher enden.

---

## 5. Warum bei Aktien **kein** Börsenkalender

Das Projekt hat eine eigene Zeitregel an anderer Stelle ausdrücklich abgelehnt
(`notifications/boersenkalender.py`). Der Unterschied liegt in der Frage:

| | Frage | Fehlerrichtungen |
|---|---|---|
| `boersenkalender.py` | „Ist die Börse **jetzt offen**?" | **zwei** teure. Zu spät „geschlossen" verschleppt einen Ausstieg; zu spät „offen" handelt zu einem Kurs, den es nicht gibt. |
| `abrufschutz.py` | „Ist dieser Zeitraum **sicher vorbei**?" | **eine.** Zu früh „ja" schreibt eine Teilkerze. Zu spät „ja" kostet nichts — die Kerze kommt beim nächsten Lauf vollständig dazu. |

**Eine einseitige Frage braucht keine genaue Antwort, sondern eine sichere
Schranke.** `D+1 00:00 UTC` liegt garantiert nach jedem NYSE-Schluss des Tages
D (16:00 ET = 20:00/21:00 UTC) — beweisbar aus der Zeitzone allein, ohne
Feiertagsliste, ohne verkürzte Handelstage, ohne ein Paket, das fehlen kann.
Die Regel wartet drei bis vier Stunden länger als nötig; in der Praxis kostet
das nichts, weil der Betreiber die Abrufe zu europäischen Tageszeiten startet,
also **vor** der US-Eröffnung.

---

## 6. Tests

`python3 shared/test_abrufschutz.py` → **77 von 77**

| # | Was |
|---|---|
| 1 | die Regel: Grenzfälle auf die Sekunde, vier `open_time`-Formen, unlesbare Zeitstempel, unbekanntes Intervall, **Spalte wird nicht umgeschrieben** |
| **2** | **die acht Abrufskripte laufen wirklich** — Miniatur-Abbild unter `/tmp`, Attrappen für Binance und yfinance. Geprüft wird die CSV, **nicht der Quelltext** |
| **3** | **Mutationsprobe:** Absicherung zur Durchreiche → **8 von 8** schreiben die laufende Kerze |
| 4 | zweiter vollständiger Abruflauf, gleiche Daten → **gleicher Datenstand-Hash** |
| 5 | die Wache: je Kriterium **ein Fall, den kein anderes bemerkt**; dazu die Nicht-Befunde |
| **6** | **Mutationsprobe:** jedes Kriterium einzeln ab → genau sein Fall geht verloren, die anderen nicht |
| 7 | kein mitwanderndes Fenster mehr, widerlegte Begründung entfernt |

**Bestehende Tests:** 50 auf `main`, 51 auf dem Branch. **Dieselben elf
Fehlschläge in beiden Läufen** — alle aus fehlenden Abhängigkeiten in der Cloud
(`binance`, `scipy`, `fastapi`, `yfinance`, Zeitzone `US/Eastern`), aus Tests,
die ein Argument verlangen, oder aus einer Zeitüberschreitung.
`shared/test_abrufschutz.py` ist die einzige neue Zeile, und sie ist grün.

**Keine Prüfung fasst `data/` an.** `git diff origin/main HEAD --name-only`
listet **keine** Datei unter `data/`; der Datenstand-Hash ist unverändert
`d9449faf51bffaaa…` bei 223 Dateien.

---

## 7. Nebenbefunde — berichtet, nicht behoben

**N1 — Die fünf Krypto-`forward_test.py` handeln auf der laufenden Kerze.**
`t3_supertrend/forward_test.py` Zeile 132/133: `row = df.iloc[-1]`,
`prev = df.iloc[-2]`. Der Cronjob läuft zur Minute 5 nach der 4h-Grenze — `row`
ist dann eine **fünf Minuten alte Teilkerze einer Vier-Stunden-Strategie**.
Dasselbe Muster in vier weiteren Bots. `forward_test.py` steht auf der
Sperrliste, und eine Änderung wäre eine Änderung am Handelsverhalten.
**Es kann auch Absicht sein.**

**N2 — `shared/fetch_binance_data.py` existiert genau einmal**, auf einem
MacBook, unversioniert. Dieselbe Klasse von Risiko wie G1. Enthält sie
Zugangsdaten (mit `grep -c` feststellbar, **ohne** den Inhalt zu zeigen), ist
der Weg eine Trennung in versionierten Code und eine unversionierte `.env` —
**nicht** ein Commit der ganzen Datei.

**N3 — `docs/UEBERSICHT_RESEARCH.md` ist vom 2026-09-12** und kennt weder
`research/kursdaten_neuaufbau/` (TB-34) noch `research/abrufskripte/` (TB-35).
Nicht geändert — das Dokument ist als Erhebung zu einem Stichtag angelegt.

---

## 8. Was **nicht** angefasst wurde

`data/` · `live_params.py` · `forward_test.py` · `equity_simulation.py` ·
`multi_symbol_optimise.py` · `multi_symbol_walk_forward.py` ·
`research/vorregistrierung/auswertung.py` · `shared/zuteilung.py` ·
`shared/messkette.py` · `shared/regimewache.py` ·
`docs/VORREGISTRIERUNG_neuselektion.md` · `broker/` · Crontab · launchd ·
`results/*.csv` · `shared/fetch_binance_data.py`

---

## 9. Was als Nächstes zu tun ist

1. **`docs/TESTAUFTRAG_TB-35_abrufskripte.md` am Mac abarbeiten** — zehn
   Schritte, die ersten sechs laufen überall. Am Ende liegt ein ZIP in
   `~/Downloads`.
2. **Nur die Zahl aus Schritt 6 notieren** (`grep -c` auf
   `shared/fetch_binance_data.py`) — nicht den Inhalt.
3. **Danach entscheiden**, ob `shared/fetch_binance_data.py` in versionierten
   Code und eine `.env` getrennt werden soll. Diese Sitzung hat die Frage
   aufgeschrieben, nicht beantwortet.
4. **Offen lassen oder aufgreifen:** N1 — ob die Krypto-Bots auf der laufenden
   oder auf der letzten abgeschlossenen Kerze handeln sollen. Das ist eine
   Frage ans Handelsverhalten, kein Abrufthema.

---

## In einfacher Sprache

**Was wir wissen wollten.** Neun Bots bekommen ihre Kurse aus Dateien, die acht
kleine Programme füllen. Die Frage war, ob man diese acht Programme jederzeit
starten kann, ohne dass dabei unbemerkt Schaden entsteht.

**Was herauskam.** Konnte man nicht. Jedes der acht schrieb die gerade
**laufende** Kursperiode mit — eine Zeile, die noch nicht fertig ist und
trotzdem aussieht wie jede andere. Und weil jedes Programm seine Datei komplett
neu schreibt, hätte ein einziger Start genügt, um den am 15. September frisch
aufgeräumten Kursbestand wieder zu verunreinigen. Zwei Programme hatten
ausserdem eine Zeitgrenze, die mitwandert und ab Sommer 2027 angefangen hätte,
Historie abzuschneiden — leise, ohne Fehlermeldung. Alles drei ist behoben.

**Warum das so ist.** Eine Börse liefert immer auch die laufende Periode mit,
mit den Werten, die sie in diesem Augenblick hat. Wer nicht ausdrücklich
nachsieht, ob eine Periode zu Ende ist, übernimmt sie. An einer einzigen Stelle
im Projekt wurde das schon richtig gemacht — beim grossen Neuaufbau im
September. Von dort ist die Regel jetzt in alle acht Programme übernommen
worden, statt sie neu zu erfinden.

**Was das für dich heisst.** Du kannst die Abrufprogramme ab jetzt von Hand
starten, ohne den Kursbestand zu gefährden: sie schreiben nur fertige
Zeiträume, und wenn doch einmal etwas verlorengeht, sagen sie es dir. Drei
Dinge bleiben offen, alle nur auf deinem Rechner erledigbar — ein echter
Testlauf gegen die Börse (Anleitung liegt bei), die Bestätigung eines
Detailformats, und die Frage, was passiert, wenn dein MacBook kaputtgeht: die
Datei, die die Kurse holt, gibt es nämlich nur dort.
