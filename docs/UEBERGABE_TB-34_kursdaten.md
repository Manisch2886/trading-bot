# Übergabe TB-34 — Kursdaten neu aufbauen

---

## 1. Was der Neuaufbau je Datei ändert

Die Zeilenzahl **nach** dem Lauf steht erst nach dem Lauf fest — der
Binance-Endpunkt ist aus der Cloud gesperrt (HTTP 403 der Egress-Richtlinie,
in TB-31 festgestellt). Schritt 11 des Testauftrags erzeugt die Vorher/Nachher-
Tabelle aus dem Bericht des Laufs.

Gemessen und hier belegt ist dagegen, **was heute in jeder Datei falsch ist** —
nachgerechnet von `shared/zeitabdeckung.py` aus den Dateien selbst, ohne Netz
und mit einem anderen Verfahren als TB-31:

| | Wieviele | Ausmass | Wird der Lauf ändern |
|---|---|---|---|
| `*_1d.csv`, **erste** Kerze | **24 von 24** | **6 bis 16 von 24 Stunden**; auf die letzte Stelle das Aggregat genau dieser Stunden, also **abgeleitet** | die native Tageskerze, plus Historie davor |
| `*_1d.csv`, **letzte** Kerze | **24 von 24** | **13 von 24 Stunden**, ebenfalls abgeleitet | die abgeschlossene Tageskerze |
| `*_4h.csv`, **letzte** Kerze | **24 von 24** | 1h-Datei belegt **1 von 4** Stunden, und die 4h-Kerze passt **nicht** zu deren Aggregat | die abgeschlossene 4h-Kerze |
| `*_4h.csv`, **erste** Kerze | **5 von 24** | `BMTUSDT` 1/4, `PEPEUSDT` 2/4, `ZKCUSDT` 2/4, `ENSOUSDT` 3/4, `WLDUSDT` 3/4 | voraussichtlich **nichts** — das sind Listing-Ränder |
| `*_1h.csv`, **letzte** Kerze | 24 von 24 | aus den Dateien allein **nicht belegbar**; folgt aus dem 4h-Befund | die abgeschlossene Stundenkerze |

**Abweichungen ausserhalb der Ränder sind der eigentliche Befund**, auf den der
Trockenlauf wartet. Der Probelauf gegen die echten 72 Dateien zeigt: alles, was
sich unterscheidet, sitzt an den Rändern. Fände der echte Lauf etwas
dazwischen, schreibt er die Datei **nicht** und stellt es an den Anfang der
Zusammenfassung. Dafür gibt es bewusst **keinen** Schalter.

Die vollständige Tabelle je Symbol steht in
[`research/kursdaten_neuaufbau/BERICHT.md`](../research/kursdaten_neuaufbau/BERICHT.md),
Abschnitt 2. Sie bestätigt die TB-31-Messung („6 bis 16 Stunden", „13
Stunden") unabhängig.

**Erwartete Grössenordnung des Zugewinns:** die dreizehn langen Historien
beginnen heute alle am 2021-09-01 — dem Rand des Fensters
`LOOKBACK = "1825 day ago UTC"`, nicht einem Listing-Datum. Danach sollten sie
beim jeweiligen Listing-Datum beginnen, für `BTCUSDT` und `ETHUSDT` im Jahr
**2017**. Die elf spät gelisteten Symbole ändern ihren Beginn nicht (er ist
schon das Listing-Datum), gewinnen aber zwei Wochen am Ende.

---

## 2. Welche Programme heute auf dem veralteten Stand rechnen

> **37 Module lesen `data/` unmittelbar, 64 weitere über
> `load_all_symbol_data()` — zusammen 101.** Kein einziges prüft, wie alt der
> Stand ist.

Mechanisch festgestellt durch
[`research/kursdaten_neuaufbau/datenwege.py`](../research/kursdaten_neuaufbau/datenwege.py),
über den Syntaxbaum statt per Textsuche.

**Der Stand von `data/`,** gemessen am jüngsten Zeitstempel *in* den Dateien
(nicht an `mtime` — ein frischer Klon setzt die zurück):

| Letzte Kerze | Dateien |
|---|---|
| 2026-08-30 | 1 (`XAUTUSDT_1h.csv`, ausgeschlossenes Symbol) |
| 2026-08-31 | 91 (Krypto) |
| 2026-09-01 | 150 (Aktien) |

Heute ist der **2026-09-15**.

**Die unmittelbaren Leser, nach Gruppen:**

| Gruppe | Module |
|---|---:|
| `multi_symbol_optimise.py` — die **Haupt-Optimierung** jedes Bots | 9 |
| `backtest_*.py` (Demo-Block) | 8 |
| `research/` — u.a. `vorregistrierung/benchmark.py`, `vorregistrierung/messgroessen.py` | 6 |
| `optimise_*.py`, `walk_forward.py` | 4 |
| `experiment_*.py` (BTC-Regimefilter) | 4 |
| `buy_and_hold_benchmark.py` | 3 |
| `zigzag_indicator.py` (Demo-Block) | 2 |
| `shared/build_daily_crypto_data.py` | 1 |

**Die 64 mittelbaren** hängen an `load_all_symbol_data()` — dem Trichter, durch
den fast alles an die Kursdateien kommt: die neun `equity_simulation.py`, die
`multi_symbol_walk_forward.py`, `shared/kurven_lauf.py`,
`shared/determinismus_lauf.py` und der Grossteil der Untersuchungen unter
`research/`.

**Und warum es nie aufgefallen ist:** die neun `forward_test.py` sind **nicht**
dabei. Alle neun holen ihre Daten **live** beim Lauf (Krypto über
`fetch_binance_data`, Aktien über `yfinance`), keiner liest eine Datei aus
`data/`. Der Teil des Systems, der täglich läuft, fragt `data/` nie — also
meldet auch nichts, wenn es steht.

---

## 3. Was geliefert ist

| Datei | Was |
|---|---|
| `shared/kursdaten_neuaufbau.py` | der Neuaufbau: messen, laden, sichern, vergleichen, ersetzen, zurückspielen |
| `shared/test_kursdaten_neuaufbau.py` | **67/67**, davon drei zweistufige Mutationsproben |
| `shared/zeitabdeckung.py` | die Teilkerzen-Wache — nur stdlib, Rückgabewert 1 bei Befund |
| `shared/test_zeitabdeckung.py` | **40/40**, davon zwei zweistufige Mutationsproben |
| `shared/README_KURSDATEN.md` | beide Werkzeuge, Sicherungskonzept, **Cron-Zeile als Vorschlag** |
| `research/kursdaten_neuaufbau/probelauf.py` | der Neuaufbau gegen die **echten** 72 Dateien, **295/295** |
| `research/kursdaten_neuaufbau/datenwege.py` | wer liest `data/`, wer holt live, wer schreibt hinein |
| `research/kursdaten_neuaufbau/BERICHT.md` | die Untersuchung |
| `research/kursdaten_neuaufbau/daten/` | Teilkerzen-Messung, Datenwege, Probelauf als JSON |
| `docs/TESTAUFTRAG_TB-34_kursdaten.md` | 18 Schritte; 1–7 überall, 8–18 auf dem Mac |
| `docs/ERGEBNIS_TB-34_kursdaten.md` | kurzes Ergebnisdokument zum Kopieren |

Dazu zwei kleine Ergänzungen an Bestehendem:

* `shared/binance_historie.py` — **zwei öffentliche Namen** für die beiden
  Schreibbausteine (`zeilen_aus_dataframe`, `schreibe_datei`). Die Funktionen
  selbst sind unverändert; der Neuaufbau muss dieselbe Schreibweise treffen wie
  die vorhandenen Dateien, und eine zweite Formatierung im Projekt wäre genau
  die Art doppelt geführter Wahrheit, die hier schon mehrfach eingesammelt
  wurde.
* `.gitignore` — `data_sicherung/`.

**Keine Kursdatei verändert.** `git diff origin/main HEAD --name-only` listet
keine Datei unter `data/`. Kein `live_params.py`, kein `forward_test.py`, kein
`equity_simulation.py`, kein `multi_symbol_optimise.py`, kein
`multi_symbol_walk_forward.py`. `shared/zuteilung.py`, `shared/messkette.py`,
`shared/regimewache.py` und `research/vorregistrierung/auswertung.py` sind
unberührt. Nichts unter `broker/`, keine Crontab, keine launchd-Vorlage, kein
`results/*.csv` überschrieben.

---

## 4. Die beiden Entwurfsfragen, die der Auftrag offengelassen hat

### 4.1 Erweiterung von `binance_historie.py` oder ein eigener Weg?

**Ein eigener Weg — `shared/kursdaten_neuaufbau.py`.**

`binance_historie.py` **verlängert** nach vorn und schreibt jede vorhandene
Zeile zeichengleich zurück. Sein ganzer Wert liegt darin, **niemals** zu
überschreiben. Ein Werkzeug, das den Bestand ersetzt, hat den entgegengesetzten
Vertrag. Beides in eine Datei zu legen hiesse, die Zusicherung „es überschreibt
nie" von einem Laufzeitschalter abhängig zu machen — genau die Bauform, die
dieses Projekt bei der Binance-Brücke schon einmal verworfen hat (`testnet=True`
als Flag im Aufrufpfad, Protokoll 4.4). Eine Zusicherung, die an einem Argument
hängt, ist keine.

Die stdlib-Grundlage von TB-31 ist trotzdem die richtige, und sie wird nicht
abgeschrieben, sondern **benutzt**: `Drossel`, `Abrufer`, `kerzen_laden`,
`erste_kerze_ms`, `als_dataframe`, `zeilen_aus_dataframe`, `schreibe_datei`,
`ZEITFORMAT`, `Kursdatei` und die 418-Behandlung kommen von dort. Es gibt
**eine** Netzstelle und **eine** Schreibweise im Projekt.

### 4.2 Gehört die Wache in `kursdaten.py` oder daneben?

**Daneben — `shared/zeitabdeckung.py`.** Drei Gründe, in dieser Reihenfolge:

1. **Laufzeit.** `kursdaten.entferne_unvollstaendige()` läuft in **allen neun
   Bots** bei jedem Laden und arbeitet zeilenweise auf einem DataFrame im
   Speicher. Die Deckungsprüfung braucht **andere Dateien** (die feinere
   Zeitreihe desselben Symbols) und einen Stichzeitpunkt. Beides wäre in einer
   Zeilenmaske fehl am Platz und kostete jeden Botlauf zusätzliche
   Lesevorgänge.
2. **Verhalten.** `kursdaten.py` **streicht und zählt**. Eine Teilkerze darf
   nicht stillschweigend gestrichen werden: die letzte Tageskerze zu streichen
   verschöbe das Ende jedes Backtests um einen Tag. Sie gehört gemeldet und von
   einem Menschen entschieden.
3. **Der Live-Betrieb darf nie an einer Datenprüfung hängenbleiben.** Ein
   eigenständiges Werkzeug mit Rückgabewert 1 kann ein Cronjob sichtbar machen,
   ohne dass ein Bot davon abhängt — dasselbe Muster wie
   `shared/ergebniskurven.py` und `shared/determinismus.py`.

**Die Wache benutzt nur die Standardbibliothek** und streamt die Dateien
zeilenweise. Sie läuft damit auch dort, wo pandas fehlt, hält nie eine ganze
Kursdatei im Speicher und braucht rund 40 Sekunden für alle 242 Dateien.

---

## 5. Wie die Wache funktioniert — und was sie nicht kann

Eine Kursdatei enthält nur `open_time` und OHLCV. Ob die Kerze `2021-09-01` 24
oder 11 Stunden umfasst, **steht nicht darin**. Die Prüfung braucht einen
Zeugen und benutzt drei, jeden mit benannter Reichweite:

| | Zeuge | Immer möglich? |
|---|---|---|
| **R** | **Raster** — jede `open_time` auf dem Raster ihres Intervalls, jeder Abstand ein ganzes Vielfaches | ja |
| **D** | **Deckung** — die feinere Datei desselben Symbols belegt den Zeitraum der ersten und letzten groben Kerze | nur wo eine feinere Datei existiert |
| **S** | **Stand** — der Zeitraum der letzten Kerze muss zum Stichzeitpunkt abgelaufen sein | ja |

Die Deckungsprüfung vergleicht die grobe Kerze zusätzlich mit dem **Aggregat
genau der vorliegenden** feineren Kerzen. Stimmt es auf die letzte Stelle, ist
die grobe Kerze daraus **abgeleitet** — ein Nachweis, kein Verdacht. Genau so
sind die 48 Tagesbefunde belegt.

> **Was sie nicht kann, und das steht auch im Bericht:** die letzte Kerze der
> **feinsten** Datei eines Symbols (`X_1h.csv`) hat keinen feineren Zeugen. War
> sie beim Abruf angeschnitten, steht das nirgends in den Dateien. Der Bericht
> sagt deshalb je Datei, welche Zeugen greifen konnten — **eine Datei ohne
> Befund ist nicht dasselbe wie eine geprüft vollständige.** Dagegen helfen nur
> der Stand-Zeuge kurz nach dem Abruf und `kursdaten_neuaufbau.py`, das eine
> laufende Kerze gar nicht erst schreibt.

**Die erste Kerze einer Historie** ist der eine Fall, der aussen bleiben muss:
eine kurze erste Kerze kann ein beschneidendes Abruffenster sein (Fehler) oder
der Listing-Tag (richtig), und offline ist das nicht entscheidbar.
Voreinstellung: **melden**. Mit `--datenbeginn <bericht.json>` — dem
JSON-Bericht des Neuaufbaus, der den **gemessenen** Datenbeginn je Symbol
enthält — gilt eine kurze erste Kerze am gemessenen Datenbeginn als richtig.
Ohne diese Datei wird gemeldet statt geraten.

---

## 6. Die Sicherung: wohin, wie lange, und wie zurück

**Wohin:** `data_sicherung/<JJJJ-MM-TT_HHMMSS>/` neben `data/`, in
`.gitignore`. Jede Datei wird kopiert, **bevor** sie ersetzt wird; das
`MANIFEST.json` führt SHA-256 und Grösse je Datei und wird **nach jeder Datei**
fortgeschrieben — ein abgebrochener Lauf hinterlässt also eine gültige
Sicherung des bereits Ersetzten.

**Wie lange:** **nichts wird automatisch gelöscht.** Die Log-Rotation hält fünf
Stände und löscht ältere (Protokoll 4.6); dort ist das richtig. Hier fällt
dieselbe Abwägung anders aus: ein Kursdatenstand ist **nicht
wiederherstellbar**, wenn der Endpunkt ihn nicht mehr so liefert.

**Vorschlag:** die Sicherung behalten, bis der neue Bestand angenommen ist —
also bis `zeitabdeckung.py` sauber meldet, der Faltenplan neu gerechnet ist und
die Ergebniskurven bewusst neu erzeugt wurden. Dann von Hand
`rm -rf data_sicherung/<Zeitstempel>`. Der Lauf meldet Pfad und Grösse
(rund 184 MB).

**Wie zurück:** `--zurueckspielen <ordner>`. Geprüft wird **zweimal** — die
Kopie gegen das Manifest (hat jemand daran gedreht?) und die zurückgespielte
Datei gegen dasselbe Manifest (ist sie heil angekommen?). Ohne die zweite
Prüfung wäre „zurückgespielt" nur eine Behauptung. Ein **belegter**
Sicherungsordner wird beim Schreiben abgelehnt statt überschrieben.

---

## 7. Was nicht geliefert ist, und warum

**Der Ladelauf selbst.** `api.binance.com` ist aus dieser Umgebung gesperrt;
das ist eine Richtlinienentscheidung und wird nicht umgangen. Der Lauf ist
Schritt 10 des Testauftrags, Dauer rund 10–20 Minuten.

**Die Nachher-Zeilenzahlen je Datei.** Sie brauchen den Lauf. Geliefert ist
stattdessen die **Vorher-Messung** (Abschnitt 1 und `BERICHT.md` Abschnitt 2)
und in Schritt 11 ein Befehl, der die Vorher/Nachher-Tabelle aus dem Bericht
des Laufs erzeugt.

**Die neuen Faltenpläne.** Sie brauchen die geladenen Daten.
`research/krypto_historie/faltenplan.py` rechnet sie; Schritt 15 des
Testauftrags. **Die TB-31-Zahlen sind danach überholt** — sie beruhten auf
angenommenen Listing-Daten
(`research/krypto_historie/daten/annahme_listing.json`), die dann durch
gemessene ersetzt sind.

**Die Korrektur der beiden `fetch_1d_data.py`.** Sie stehen weiterhin auf
`LOOKBACK = "3650 day ago UTC"` (siehe Abschnitt 8). Das ist Abruflogik und
eine eigene, ausdrückliche Entscheidung des Betreibers — TB-34 fasst sie nicht
an.

---

## 8. Drei Nebenbefunde, die im Auftrag nicht standen

1. ⚠️ **Zwei Abrufskripte haben weiterhin ein relatives Zeitfenster.** Der
   Betreiber hat am 14.09.2026 `shared/fetch_multi_data.py` und
   `strategies/t3_supertrend/fetch_4h_data.py` von `"1825 day ago UTC"` auf
   `"1 Jan, 2017"` gestellt (die Änderung ist noch nicht auf `main`). Die
   **beiden nativen Tagesabrufe** —
   `strategies/rsi2_crypto/fetch_1d_data.py` und
   `strategies/volatility_breakout_crypto/fetch_1d_data.py` — stehen weiterhin
   auf `"3650 day ago UTC"`. Heute schneidet das nichts weg, weil Binance erst
   seit Juli 2017 existiert. **Ab Sommer 2027 schneidet es**, und es ist
   derselbe Fehlertyp: ein Fenster, das sich mit dem Abruftag mitbewegt.

2. **Keines der acht Abrufskripte schliesst die laufende Kerze aus**, und alle
   überschreiben ihre Datei vollständig (`df.to_csv(...)`). Das ist die
   Ursache dafür, dass alle 72 Krypto-Dateien mit einer Teilkerze enden — und
   es wäre nach jedem künftigen Abruf wieder so. `shared/fetch_binance_data.py`
   ist gitignoriert und hier nicht lesbar; am Ergebnis ist es trotzdem
   bewiesen.

3. **Eine echte Datenlücke und 19 verwaiste Dateien.** 13 Krypto-1h-Dateien
   fehlen **drei** Stunden ab dem **2021-09-29 07:00**, `PROMUSDT_1h.csv`
   **eine** ab dem 2023-03-24 13:00 — eine Lücke mitten in der Reihe, die
   **nicht** in `docs/DATENLUECKEN.md` steht (das führt nur
   Forward-Test-Ausfälle). Ausserdem liegen **19 `*_15m.csv`** in `data/`,
   Reste des verworfenen 15-Minuten-Versuchs; kein Programm liest sie. Beides
   nur benannt, nichts angefasst.

---

## 9. Was nach dem Lauf zu erwarten ist — und benannt gehört

| Was | Erwartung |
|---|---|
| `shared/zeitabdeckung.py --datenbeginn <bericht>` | **kein Befund** für die 72 Krypto-Dateien |
| `shared/ergebniskurven.py` | **5× ABWEICHEND** (Krypto), **4× AKTUELL** (Aktien) |
| `research/krypto_historie/faltenplan.py` | **neu zu rechnen** |
| Datenstand-Hash der Vorregistrierung | **ändert sich** |

> ⚠️ **Der Datenstand-Hash der Vorregistrierung ändert sich — und das ist kein
> Amendment.** Er steht in `docs/VORREGISTRIERUNG_neuselektion.md` auf der
> Sperrliste. Änderte er sich **nach** dem Selektionslauf, wäre das ein Bruch
> des Registers. Er ändert sich **vorher** — und genau das ist der Grund, warum
> TB-34 **vor** TB-30b kommt. Wäre erst selektiert und dann geladen worden,
> hätte die Selektion auf einer Historie stattgefunden, die es danach nicht
> mehr gibt.

> **`shared/ergebniskurven.py` wird ABWEICHEND melden, und das ist korrekt.**
> Mehr Historie heisst andere Backtests, korrigierte Teilkerzen heissen andere
> Randwerte. **Die Kurven bitte nicht vorschnell neu erzeugen** — ob und wann,
> entscheidet der Betreiber, und es gehört in denselben Schritt wie die
> Neuselektion. Meldet ein **Aktien**-Bot ABWEICHEND, hat der Lauf etwas
> angefasst, was er nicht durfte.

---

## 10. Offene Punkte — Entscheidungen des Betreibers

1. **Soll `data/` täglich abgerufen werden?** Berichtet in
   `BERICHT.md` Abschnitt 4, nicht entschieden. Die Kurzfassung: dafür spricht
   der zwei Wochen alte Stand und die 101 Module, die darauf rechnen; dagegen
   spricht, dass es **kein Werkzeug gibt, das anhängt** — die heutigen
   `fetch_*.py` überschreiben samt laufender Kerze und machten den Fehler
   damit zur täglichen Gewohnheit. Eine Cron-Zeile für die **Wache** steht als
   Vorschlag im README; eine für den **Abruf** bewusst nicht.
2. **Sollen die beiden `fetch_1d_data.py` ebenfalls auf ein festes Startdatum
   gestellt werden?** Siehe Abschnitt 8, Punkt 1.
3. **Sollen die `fetch_*.py` die laufende Kerze ausschliessen?** Die
   Wiederholung des Fehlers hängt daran. `kursdaten_neuaufbau.py` zeigt, wie es
   geht (`close_time <= Stand`); die Abrufskripte übernehmen es nicht von
   selbst.
4. **Kommt der neue Kursdatenbestand ins Repo?** Der Lauf findet auf dem Mac
   statt; der Branch enthält bewusst keine Änderung unter `data/`. 184 MB
   Änderung in einem Commit ist eine eigene Entscheidung.
5. **Die 19 verwaisten `*_15m.csv`** — löschen oder behalten?
6. **Die Datenlücke vom 2021-09-29** gehört nach `docs/DATENLUECKEN.md`, wenn
   der Lauf zeigt, dass der Endpunkt sie auch nicht kennt.

**Es wurde kein Raster gerechnet, kein Parameter übernommen und keine Kursdatei
verändert.**
