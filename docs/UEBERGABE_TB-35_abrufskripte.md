# Übergabe TB-35 — Abrufskripte haltbar machen

**Stand 2026-09-15. Branch `claude/new-session-we9a90`, Base `main` bei
`5318795`.**

---

## 1. Welche Abrufskripte geändert wurden — und welche nicht erreichbar waren

**Acht von acht geändert. Keines war unerreichbar.**

| Abrufskript | Markt / Raster | laufende Kerze | `LOOKBACK` | Wache |
|---|---|---|---|---|
| `shared/fetch_multi_data.py` | Krypto 1h | ✅ neu | war schon fest (`1 Jan, 2017`) | ✅ neu |
| `strategies/t3_supertrend/fetch_4h_data.py` | Krypto 4h | ✅ neu | war schon fest | ✅ neu |
| `strategies/rsi2_crypto/fetch_1d_data.py` | Krypto 1d | ✅ neu | **✅ korrigiert** | ✅ neu |
| `strategies/volatility_breakout_crypto/fetch_1d_data.py` | Krypto 1d | ✅ neu | **✅ korrigiert** | ✅ neu |
| `strategies/elliott_wave_stocks/fetch_stock_data.py` | Aktien 1d | ✅ neu | `period="max"`, wandert nicht | ✅ neu |
| `strategies/rsi2_mean_reversion/fetch_stock_data.py` | Aktien 1d | ✅ neu | `period="max"` | ✅ neu |
| `strategies/turtle_soup_stocks/fetch_stock_data.py` | Aktien 1d | ✅ neu | `period="max"` | ✅ neu |
| `strategies/volatility_breakout/fetch_stock_data.py` | Aktien 1d | ✅ neu | `period="max"` | ✅ neu |

**Nicht erreichbar war kein Abrufskript, sondern das Modul, an dem vier von
ihnen hängen:** `shared/fetch_binance_data.py` ist gitignoriert und liegt nur
auf dem Rechner des Betreibers. Es wurde **nicht gelesen, nicht umgangen und
nicht nachgebaut.**

---

## 2. Was ohne `shared/fetch_binance_data.py` offenbleibt

Drei Dinge — und nur diese drei. Alles andere ist erledigt.

**a) Welche Form `open_time` wirklich hat, ist nicht geprüft, sondern
abgedeckt.** Die Kursdateien zeigen `2017-08-17 04:00:00` bzw. `2017-08-17`;
ob das Modul Zeichenketten, pandas-Zeitstempel oder Millisekunden liefert, ist
aus der Cloud nicht feststellbar. `abrufschutz` behandelt deshalb **alle vier
Formen** (Zeichenkette, Zeitstempel, Sekunden, Millisekunden), und jede ist im
Selbsttest belegt. **Zu prüfen bleibt nur, dass es tatsächlich eine davon
ist** — Schritt 4 des Testdokuments zeigt das in einer Zeile, ohne den
Dateiinhalt anzuzeigen.

**b) Ein echter Lauf gegen Binance hat nicht stattgefunden.** Der Endpunkt ist
aus der Cloud gesperrt (403 der Egress-Richtlinie), yfinance ebenso. Alle
Prüfungen liefen gegen erzeugte Beispieldaten. **Der Trockenlauf gegen den
echten Endpunkt steht im Testdokument** (Schritte 6–9), samt der
entscheidenden Kontrolle: der Datenstand-Hash muss danach unverändert sein.

**c) Die Datei existiert genau einmal.** Neun Module hängen an ihr, fünf davon
im täglichen Betrieb. Geht der Rechner verloren, ist der einzige Weg zu
Krypto-Kursdaten weg. **Das ist berichtet, nicht entschieden** — siehe
`research/abrufskripte/BERICHT.md`, Punkt 4a. Enthält sie Zugangsdaten (mit
`grep -c` feststellbar, ohne den Inhalt zu zeigen), ist der richtige Weg eine
Trennung in versionierten Code und eine unversionierte `.env`, **nicht** ein
Commit der ganzen Datei.

---

## 3. Was gebaut wurde

| Datei | Was |
|---|---|
| `shared/abrufschutz.py` | **neu** — die Regel „nur abgeschlossene Zeiträume" **und** die Wache gegen Verkürzung; eigenständiges Werkzeug mit Rückgabewert 1 bei Befund |
| `shared/test_abrufschutz.py` | **neu** — **77/77**, davon zwei Sätze Mutationsproben |
| die acht Abrufskripte | Filter vor dem Schreiben, Wache mitlaufend, Rückgabewert 1 bei Befund |
| `research/abrufskripte/abrufwege.py` | **neu** — stellt über den Syntaxbaum fest, wer an `fetch_binance_data` hängt |
| `research/abrufskripte/BERICHT.md` | **neu** — das Ergebnis dieser Feststellung, samt der Fragen, die berichtet und nicht entschieden werden |
| `docs/TESTAUFTRAG_TB-35_abrufskripte.md` | **neu** — autonom ausführbar am Mac, mit echtem Endpunkt |
| `docs/ERGEBNIS_TB-35_abrufskripte.md` | **neu** — Kurzfassung zum Kopieren |

### 3.1 Die laufende Kerze entsteht gar nicht erst

Vorbild ist `shared/kursdaten_neuaufbau.py`: übernommen wird nur, was als
abgeschlossen gilt. **Mit einem Unterschied, der kein Detail ist:** der
Neuaufbau sieht die rohen Kerzenfelder und liest `close_time` (Feld 6)
unmittelbar. Die Abrufskripte sehen nur den fertigen DataFrame —
`open_time/open/high/low/close/volume`, **ohne `close_time`** (nachgerechnet
an den Kursdateien selbst). Der Schluss wird deshalb aus `open_time` und der
Intervalllänge gerechnet, mit **derselben Formel**:
`schluss = öffnung + länge − 1`, behalten bei `schluss <= Stand`. Die Längen
kommen aus `binance_historie.INTERVALL_MS` — eine zweite Tabelle wäre die
Doppelführung, an der dieses Projekt schon einmal Zahlen verloren hat.

**Strukturell, nicht als Nachbearbeitung:** gefiltert wird der DataFrame
**vor** `to_csv`. Es wird nichts aus einer geschriebenen Datei
herausgeschnitten.

**Wo der Filter sitzt, ist bei den Aktien eine bewusste Entscheidung.** Er
steht im `__main__`-Teil, **nicht** in `fetch_historical_data` — denn diese
Funktion versorgt auch `forward_test.py` mit Live-Daten. Der Filter dort hätte
die Signallogik der laufenden Bots verändert: eine Änderung am
Handelsverhalten, die nach Abschnitt 7 des Übergabeprotokolls durch Backtest,
Walk-Forward und Equity-Simulation muss — und `forward_test.py` steht
ausserdem auf der Sperrliste der Aufgabe. **Die CSV bekommt die Zeile so oder
so nie zu sehen.**

**Warum bei Aktien kein Börsenkalender nötig ist.** Eine NYSE-Tageskerze ist
um 16:00 Ortszeit fertig, also 20:00 UTC (Sommer) bzw. 21:00 UTC (Winter). Die
Regel verlangt `D 23:59:59` und wartet damit drei bis vier Stunden länger als
nötig. Das ist Absicht:

> Das Projekt hat an anderer Stelle eine eigene Zeitregel ausdrücklich
> abgelehnt (`notifications/boersenkalender.py`). Dort lautet die Frage aber
> **„ist die Börse JETZT offen?"** — mit zwei teuren Fehlerrichtungen. Hier
> lautet sie **„ist dieser Zeitraum SICHER vorbei?"** — mit nur einer. Zu früh
> „ja" schreibt eine Teilkerze; zu spät „ja" kostet nichts, die Kerze kommt
> beim nächsten Lauf vollständig dazu. **Eine einseitige Frage braucht keine
> genaue Antwort, sondern eine sichere Schranke**, und `D+1 00:00 UTC` ist
> eine — beweisbar aus der Zeitzone allein, ohne Feiertagsliste, ohne Paket,
> das fehlen kann.

In der Praxis kostet das nichts: der Betreiber ruft die Abrufskripte von Hand
auf, üblicherweise zu europäischen Tageszeiten — also **vor** der US-Eröffnung,
wo die letzte fertige Kerze ohnehin die von gestern ist.

### 3.2 Feste Startdaten statt mitwandernder Fenster

Beide `fetch_1d_data.py` stehen jetzt auf `LOOKBACK = "1 Jan, 2017"`, dem
Stand der übrigen Skripte. Die alte Begründung — *„10 Jahre Vorlauf angefragt
— Binance liefert ohnehin"* — ist **entfernt**, nicht umformuliert: sie war
nachweislich falsch. Sie stimmte nur, solange 3650 Tage vor dem Abruftag noch
vor dem Binance-Start (Juli 2017) lagen. **Ab Sommer 2027 hätte das Fenster
angefangen zu schneiden, und zwar leise** — eine gekürzte Datei sieht aus wie
eine, die nie länger war.

`shared/test_abrufschutz.py` Abschnitt 7 prüft beides: dass kein Abrufskript
mehr ein mitwanderndes Fenster benutzt, und dass die widerlegte Begründung
nirgends mehr steht.

---

## 4. Die zwei Entscheidungen, die die Aufgabe verlangt hat

### 4.1 Anhängen oder überschreiben? → **Überschreiben bleibt.**

Der Einwand aus der Aufgabe hält der Prüfung stand und gibt den Ausschlag:

> Ein anhängendes Werkzeug, das sich irrt, verlängert eine Datei mit falschen
> Zeilen, und der Fehler bleibt dauerhaft stehen. Ein überschreibendes, das
> sich irrt, ist beim nächsten Lauf wieder in Ordnung.

Dazu kommen drei Gründe aus dem Projekt selbst:

1. **Überschreiben war nie das Problem — die Teilkerze am Ende war es.** Mit
   §1 ist die Ursache weg. Ein Formatwechsel obendrein wäre eine zweite,
   grössere Änderung ohne eigenen Anlass.
2. **Das Projekt führt für „verlängern" bereits ein Werkzeug**, und dessen
   ganzer Wert liegt in einer Zusicherung, die ein Abrufskript nicht geben
   kann: `shared/binance_historie.py` verlängert **nach vorn** und schreibt
   jede vorhandene Zeile zeichengleich zurück. `shared/kursdaten_neuaufbau.py`
   baut vollständig neu. Ein drittes Werkzeug mit einem vierten Vertrag wäre
   genau die Unübersichtlichkeit, die TB-34 beklagt hat.
3. **Anhängen braucht eine Konfliktregel, die niemand entscheiden kann.** Was
   gilt, wenn der Endpunkt eine bereits gespeicherte Kerze anders liefert als
   beim letzten Mal? Überschreiben beantwortet das mit „die neue Antwort
   gilt". Anhängen müsste zwischen „alte behalten" und „ersetzen" wählen —
   und beides ist in Einzelfällen falsch.

**Der Preis des Überschreibens wird nicht weggeredet, sondern abgesichert:**
genau deshalb gibt es §4.

### 4.2 Gehört die Wache in die Abrufskripte oder daneben? → **Beides, mit genau einer Umsetzung.**

* **Daneben**, weil die Logik genau einmal existieren soll. Acht Abrufskripte
  mit acht Kopien derselben Prüfung wären wieder die Doppelführung. Und ein
  Werkzeug mit `main()` taugt auch dann noch etwas, wenn eine Datei auf einem
  **anderen** Weg kürzer geworden ist:

  ```
  python3 shared/abrufschutz.py --aufnehmen /tmp/vorher.json
  ...
  python3 shared/abrufschutz.py --vergleiche /tmp/vorher.json   # 1 bei Befund
  ```

* **Trotzdem im Abrufskript**, weil die Wache einen Vergleichswert von **vor**
  dem Lauf braucht. Wer sie erst hinterher von Hand startet, hat nichts mehr,
  womit er vergleichen könnte — die alte Fassung ist dann schon überschrieben.
  Und der Fall, um den es geht, ist gerade der **unangekündigte Handstart**,
  bei dem niemand an eine zweite Prüfung denkt.

**Blockiert wird nie.** Die Wache meldet je Datei sofort, fasst am Ende
zusammen und setzt den Rückgabewert auf 1 — dieselbe Hausregel wie
`shared/kursdaten.py`: *ein Befund ist kein Fehler des Programms, aber etwas,
das ein Cronjob-Aufruf sichtbar machen soll.* Geschrieben wird trotzdem; es
wird nichts zurückgenommen, und die alten Stände stehen im letzten Commit.

**Eine Ausnahme, die keine Blockade ist:** ist nach dem Filtern **nichts**
übrig, wird gar nicht geschrieben. Eine leere Tabelle zu schreiben hiesse,
eine vorhandene Datei auf ihre Kopfzeile zu verkürzen — sicherer Verlust ohne
jeden Gegenwert. Die Aktien-Skripte tun das für den leeren Abruf schon immer.

**Drei Kriterien, weil eines nicht reicht.** Die Wache schlägt an bei
*weniger Zeilen*, *späterem Beginn* und *früherem Ende* (dazu: Datei
verschwunden). Eine Datei kann bei **gleicher** Zeilenzahl später beginnen
oder früher enden — wer nur zählt, sieht das nicht. Sie schlägt ausdrücklich
**nicht** an, wenn nur verlängert wurde, nichts passiert ist oder eine Datei
neu hinzukommt.

---

## 5. Tests

`python3 shared/test_abrufschutz.py` → **77 von 77**.

| Abschnitt | Was geprüft wird |
|---|---|
| 1 | die Regel selbst: Grenzfälle auf die Sekunde, alle vier `open_time`-Formen, unlesbare Zeitstempel, unbekanntes Intervall, **und dass die Spalte nicht umgeschrieben wird** |
| **2** | **die acht Abrufskripte laufen wirklich** — in einem Miniatur-Abbild des Projekts unter `/tmp`, gegen Attrappen für Binance und yfinance. Geprüft wird, was danach in der CSV steht, **nicht der Quelltext** |
| **3** | **Mutationsprobe:** Absicherung zur Durchreiche gemacht → **8 von 8** schreiben die laufende Kerze. Abschnitt 2 prüft also wirklich etwas |
| 4 | zweiter vollständiger Abruflauf, gleiche Daten → **gleicher Datenstand-Hash** (`herkunft.datenstand`) |
| 5 | die Wache: je Kriterium **ein Fall, den kein anderes Kriterium bemerkt**; dazu die Nicht-Befunde |
| **6** | **Mutationsprobe:** jedes Kriterium einzeln abgeschaltet → genau sein Fall geht verloren, **die anderen beiden nicht** |
| 7 | kein mitwanderndes Fenster mehr, widerlegte Begründung entfernt |

Die zwei benannten Fallen sind ausdrücklich adressiert: *eine Probe, deren
Zustand der Test von Hand herstellt, bestätigt sich selbst* → Abschnitte 3
und 6 beobachten den **Ablauf** mit und ohne Absicherung. *Eine zweite Wache
verdeckt das Fehlen der ersten* → Abschnitt 6 schaltet die Kriterien einzeln
ab.

**Keine Prüfung dieser Datei fasst `data/` an.** Die Abrufskripte rechnen
ihren `shared/`-Ordner aus der eigenen Lage aus; im Miniatur-Abbild finden sie
dort ein `DATA_DIR`, das unter `/tmp` liegt.

**Bestehende Tests:** unverändert gegenüber dem Basislauf auf `main` — die
Vergleichstabelle steht in `docs/ERGEBNIS_TB-35_abrufskripte.md`.

---

## 6. Was **nicht** angefasst wurde

`data/` (kein einziger Eintrag in `git diff origin/main HEAD --name-only`) ·
`live_params.py` · `forward_test.py` · `equity_simulation.py` ·
`multi_symbol_optimise.py` · `multi_symbol_walk_forward.py` ·
`research/vorregistrierung/auswertung.py` · `shared/zuteilung.py` ·
`shared/messkette.py` · `shared/regimewache.py` ·
`docs/VORREGISTRIERUNG_neuselektion.md` · `broker/` · Crontab · launchd ·
`results/*.csv` · `shared/fetch_binance_data.py` (nicht lesbar, **und nicht
nachgebaut**)

Der Datenstand-Hash ist unverändert: `d9449faf51bffaaa…` bei 223 Kursdateien.

---

## 7. Nebenbefunde — berichtet, nicht behoben

**N1 — Die fünf Krypto-`forward_test.py` handeln auf der laufenden Kerze.**
`t3_supertrend/forward_test.py` Zeile 132/133: `row = df.iloc[-1]`,
`prev = df.iloc[-2]`. Der Cronjob läuft zur Minute 5 nach der 4h-Grenze; `row`
ist dann eine **fünf Minuten alte Teilkerze einer Vier-Stunden-Strategie**.
Dasselbe Muster in `elliott_wave`, `rsi2_crypto`, `turtle_soup_crypto`,
`volatility_breakout_crypto` — mechanisch festgestellt, siehe
`research/abrufskripte/abrufwege.py`, Abschnitt 2b.

Nicht angefasst: `forward_test.py` steht auf der Sperrliste, und eine Änderung
wäre eine Änderung am Handelsverhalten. **Es kann auch Absicht sein** (Einstieg
zum aktuellen Kurs statt zum Schlusskurs der Vorkerze). Hier steht nur der
Befund.

**N2 — `shared/fetch_binance_data.py` existiert genau einmal.** Siehe
Abschnitt 2c und `research/abrufskripte/BERICHT.md`, Punkt 4a.

**N3 — `docs/UEBERSICHT_RESEARCH.md` ist vom 2026-09-12** und kennt weder
`research/kursdaten_neuaufbau/` (TB-34) noch `research/abrufskripte/` (TB-35).
Das Dokument ist als Erhebung zu einem Stichtag angelegt; es wurde **nicht**
geändert. Wer es fortschreibt, hat jetzt zwei Nachträge.

---

## In einfacher Sprache

**Was wir wissen wollten.** Neun Bots bekommen ihre Kurse aus Dateien, die von
acht kleinen Programmen gefüllt werden. Die Frage war, ob diese acht Programme
haltbar sind — also ob man sie jederzeit starten kann, ohne dass dabei
unbemerkt Schaden entsteht.

**Was herauskam.** Nein, das waren sie nicht. Jedes der acht schrieb die
gerade **laufende** Kursperiode mit in die Datei — eine Zeile, die noch gar
nicht fertig ist und trotzdem aussieht wie jede andere. Und weil jedes Programm
die Datei komplett neu schreibt, hätte ein einziger Start genügt, um den frisch
aufgeräumten Kursbestand vom 15. September wieder zu verunreinigen. Zwei
Programme hatten ausserdem eine Zeitgrenze, die mitwandert und ab Sommer 2027
angefangen hätte, Historie abzuschneiden. Beides ist behoben; dazu gibt es
jetzt einen Wächter, der meldet, wenn eine Datei nach einem Abruf kürzer ist
als vorher.

**Warum das so ist.** Eine Börse liefert immer auch die gerade laufende Periode
mit, mit den Werten, die sie in diesem Augenblick hat. Wer nicht ausdrücklich
nachsieht, ob eine Periode schon zu Ende ist, übernimmt sie. Bisher sah das
niemand nach — an einer einzigen Stelle im Projekt wurde es richtig gemacht,
nämlich beim grossen Neuaufbau, und von dort ist die Regel jetzt in alle acht
Programme übernommen worden.

**Was das für dich heisst.** Du kannst die Abrufprogramme ab jetzt gefahrlos
von Hand starten. Sie schreiben nur fertige Zeiträume, und wenn doch einmal
etwas verlorengeht, sagen sie es dir, statt es still zu tun. Drei Dinge bleiben
offen, alle drei nur auf deinem Rechner erledigbar: ein echter Testlauf gegen
die Börse (Anleitung liegt bei), die Bestätigung eines Detailformats, und die
Frage, was passiert, wenn dein MacBook kaputtgeht — die Datei, die die Kurse
holt, gibt es nämlich nur dort.
