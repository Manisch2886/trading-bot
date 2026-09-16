# Ergebnis TB-38 — Gemeinsame Abrufschicht

**Stand: 15.09.2026.** Basis `main` (`0f696b0`, TB-37/PR #110 enthalten — geprüft).
Testauftrag: `docs/TESTAUFTRAG_TB-38_abrufschicht.md`.
Übergabe: `docs/UEBERGABE_TB-38_abrufschicht.md`.

---

## Die drei Antworten zuerst

### 1. Welche Kerze nahm jeder Bot vorher, welche jetzt?

Cron läuft in **Ortszeit** (Europe/Berlin), die Kerzen liegen auf dem **UTC**-Raster. Die Spalte „Füllstand" sagt deshalb, wie weit die alte Entscheidungskerze zum Laufzeitpunkt schon gefüllt war (Sommerzeit / Winterzeit).

| Bot | Takt | Cron (Ortszeit) | **vorher** | Füllstand | **jetzt** | geändert? |
|---|---|---|---|---|---|---|
| `elliott_wave` | 1 h | `0 * * * *` | die **laufende** Stundenkerze | **0 %** — 0 Minuten alt | die vorige, **abgeschlossene** Stundenkerze | **ja** |
| `t3_supertrend` | 4 h | `0 */4 * * *` | die **laufende** Vier-Stunden-Kerze | **50 % / 75 %** — 2 bzw. 3 von 4 Stunden ² | die vorige, **abgeschlossene** Vier-Stunden-Kerze | **ja** |
| `rsi2_crypto` | 1 d | einer von `20 23`, `50 23`, `15 0` ¹ | die **laufende** Tageskerze | **89 % – 97 %** — 21 h 20 bis 23 h 15 von 24 h | die Tageskerze des **Vortags**, vollständig | **ja** |
| `turtle_soup_crypto` | 1 d | ¹ | dito | dito | dito | **ja** |
| `volatility_breakout_crypto` | 1 d | ¹ | dito | dito | dito | **ja** |
| `elliott_wave_stocks` | 1 d | werktags **22:15** | die Tageskerze von **heute** | **100 %** — US-Schluss war 15 min vorher | **dieselbe** Tageskerze von heute | **nein** |
| `rsi2_mean_reversion` | 1 d | werktags 22:15 | dito | dito | dito | **nein** |
| `turtle_soup_stocks` | 1 d | werktags 22:15 | dito | dito | dito | **nein** |
| `volatility_breakout` | 1 d | werktags 22:15 | dito | dito | dito | **nein** |

¹ Die drei täglichen Krypto-Einträge sind belegt (`crontab -l`, 11.09.2026, `docs/DATENLUECKEN.md`), **welcher zu welchem Bot gehört, wurde nie erhoben**. Für die Aussage hier genügt, dass alle drei die laufende Tageskerze trafen.

² ⚠️ **Nebenbefund — die Zahl aus der Aufgabenbeschreibung stimmt nicht.** Dort heisst es, der `t3_supertrend`-Cron laufe „zur Minute 5 nach der Vier-Stunden-Grenze", die Teilkerze sei also „fünf Minuten alt". Das trifft auf den **Bot** nicht zu: `5 */4 * * *` ist die Zeile der **Broker-Brücke** (`broker/README.md`), der Bot steht auf `0 */4 * * *` (`docs/DATENLUECKEN.md`). Und weil Cron in Ortszeit zündet, fällt `0 */4` in Europe/Berlin auf die **UTC**-Stunden 22/02/06/10/14/18 (Sommer) bzw. 23/03/07/… (Winter) — also **nicht** auf das UTC-Vier-Stunden-Raster 00/04/08/12/16/20. Die gelesene Teilkerze war damit 2 (Sommer) bzw. 3 Stunden (Winter) alt, nicht 5 Minuten. **Am Befund selbst ändert das nichts** — eine halbfertige Kerze ist eine halbfertige Kerze —, wohl aber an seiner Grössenordnung. Nachprüfbar mit `crontab -l` und `date +%Z`.

**Der Kern in einem Satz:** Fünf Krypto-Bots entschieden auf einer Teilkerze und tun es nicht mehr; vier Aktien-Bots entschieden schon vorher richtig — **aber durch Timing, nicht durch Regel**, und jetzt durch Regel.

### 2. Wie gross ist der Diff je `forward_test.py`?

**+14 / −1 Zeilen** bei den fünf Krypto-Bots, **+15 / −1** bei den vier Aktien-Bots. Davon sind **9 Zeilen Kommentar**; die eigentliche Änderung sind **5 bis 6 Zeilen**:

```diff
  from fetch_binance_data import fetch_historical_data
+ import entscheidungskerze

-         df = fetch_historical_data(symbol, INTERVAL, LOOKBACK)
+         df = entscheidungskerze.lade(
+             symbol, INTERVAL, entscheidungskerze.KRYPTO,
+             abruf=lambda: fetch_historical_data(symbol, INTERVAL, LOOKBACK))

+     entscheidungskerze.melde()
      print_summary(conn)
```

Keine Signallogik, keine Schwelle, keine Positionsgrösse, kein Stop. `df.iloc[-1]` bleibt überall stehen und bedeutet ab jetzt das, was es immer bedeuten sollte.

### 3. Laufen die Aktien-Crons nach US-Schluss?

**Ja — mit 15 Minuten Abstand.**

| | Sommerzeit | Winterzeit |
|---|---|---|
| NYSE-Schluss | 20:00 UTC | 21:00 UTC |
| Cron (22:15 Ortszeit) | 20:15 UTC | 21:15 UTC |
| Abstand | **+15 min** | **+15 min** |

Der Abstand bleibt über die Zeitumstellung konstant, weil Berlin und New York beide umstellen — an unterschiedlichen Terminen, aber in derselben Richtung. **In den zwei bis drei Wochen im Jahr, in denen die Termine auseinanderliegen, bleibt der Abstand +15 oder wird +75 Minuten, nie negativ.** Verkürzte Handelstage (Schluss 13:00 Ortszeit) liegen erst recht davor.

Dass der Mac auf **Europe/Berlin** läuft, ist damit auch intern belegt: „22:15" ergibt als „15 Minuten nach US-Schluss" nur in dieser Zeitzone Sinn — und zwar in **beiden** Zeitzonenlagen.

Belegt: `crontab -l` vom 11.09.2026 (`docs/DATENLUECKEN.md`, Zeile 133 und Abschnitt „Was nachträglich geprüft wurde"), `docs/UEBERGABEPROTOKOLL.md` Abschnitt 2. Nachgerechnet gegen den echten NYSE-Kalender in `shared/test_entscheidungskerze.py`, Abschnitt 4 (Sommer **und** Winter).

**Und genau das ist die Prüfung, dass der Filter richtig gebaut ist:** die vier Aktien-Bots nehmen dieselbe Kerze wie vorher. Hätte der Filter die konservative `D 23:59:59`-Schranke aus `abrufschutz` benutzt, wären sie auf die Kerze von **gestern** gefallen — jedes Signal einen Handelstag zu spät. Deshalb der echte Börsenkalender (siehe unten).

---

## Die Regel

> **Entscheidungskerze ist die letzte Kerze, deren `close_time` vor der Startzeit des Laufs liegt.**

Ausgeschrieben: `schluss < startzeit`, wobei `schluss` der **letzte Augenblick ist, der noch zur Kerze gehört** — bei Binance `open + Länge − 1 ms` (Feld 6 der Rohkerze), bei einer NYSE-Tageskerze der Sitzungsschluss.

Eine Kerze, deren `close_time` **genau** auf der Startzeit liegt, wird **nicht** genommen.

⚠️ **Die Lesart von `close_time` ist der Kern, nicht ein Detail.** Mit der „natürlichen" Lesart (`open + Länge`, die 08:00-Kerze endet um 12:00:00) dürfte ein Lauf um 12:00:00 die soeben fertige 08:00-Kerze **nicht** nehmen und müsste auf die 04:00-Kerze zurückgreifen — acht Stunden alt, und die Gleichheit mit dem Backtest wäre gerade zerstört. Gebaut ist die **Binance-Lesart**, weil sie die Lesart der Datenquelle dieses Projekts ist. → Offener Punkt 26 im Übergabeprotokoll, zur einmaligen Bestätigung.

---

## Wo die Schicht sitzt — und warum sie keine zweite Regel ist

`shared/entscheidungskerze.py`, 9 KB Code plus Begründung im Kopf.

| Frage | Entscheidung | Grund |
|---|---|---|
| Eigenes Modul oder `abrufschutz` erweitern? | **eigenes Modul, das `abrufschutz` benutzt** | Die **Regel** steht weiter genau einmal (`abrufschutz.abgeschlossen_maske`, TB-35, zeichengleich mit `kursdaten_neuaufbau`, TB-34) und wird hier **aufgerufen, nicht nachgerechnet**. Neu ist die **Tür**, nicht die Regel. Getrennt, weil `abrufschutz` den **Schreibpfad** schützt (zu langes Warten kostet nichts) und diese Schicht den **Lesepfad** (zu langes Warten kostet einen Handelstag) — zwei entgegengesetzte Risikoprofile gehören nicht in eine Datei |
| Oder `shared/kursdaten.py`? | **nein** | Das beantwortet eine andere Frage: „fehlen dieser Kerze die Kurse?", nicht „ist ihr Zeitraum vorbei?". Beide werden hier nacheinander gestellt, über die **vorhandenen** Funktionen |
| Wie kommt die Startzeit herein? | **Argument, im Prozess einmal eingefroren. Keine Umgebungsvariable** | Ein Wert, der sich während des Laufs ändert, gäbe den ersten Symbolen Kerze N und den restlichen N+1 — und weil alle neun Bots `open_count += 1` laufend hochzählen, hinge das Ergebnis dann von der Symbolreihenfolge ab. Eine vergessene `export`-Zeile wiederum fröre neun Bots lautlos auf einer alten Kerze ein, und das sieht in den Zahlen aus wie „kein Signal" |

---

## Aktien: dieselbe Regel, **andere Schranke**

`abrufschutz` setzt den Schluss einer Tageskerze auf `D 23:59:59` — für den Schreibpfad richtig und dort ausführlich begründet: die Frage „ist dieser Zeitraum **sicher** vorbei?" hat nur eine teure Fehlerrichtung, also genügt eine sichere Schranke.

Für den Entscheidungspfad ist dieselbe Frage **zweiseitig teuer**: zu früh „ja" heisst Teilkerze, zu spät „ja" heisst ein verlorener Handelstag. Das ist genau der Fall, für den `notifications/boersenkalender.py` gebaut wurde und für den das Projekt eine eigene Zeitregel ausdrücklich **abgelehnt** hat.

Also: der Schluss einer Aktien-Tageskerze ist der **echte Sitzungsschluss** — mit Feiertagen, verkürzten Handelstagen und US-Zeitumstellung. Kosten: **eine** Kalenderabfrage je Lauf (`status(startzeit)["letzter_handelstag"]` ist bereits „die letzte Sitzung, deren `market_close <= jetzt` liegt"), nicht eine je Zeile.

**Kann der Kalender nicht antworten** (`pandas_market_calendars` fehlt), wird **nicht geraten** — der Kopf von `boersenkalender.py` verbietet eine Faustregel als Rückfallebene ausdrücklich („sie würde genau in dem Moment zuschlagen, in dem niemand mehr hinsieht"). Stattdessen gilt die sichere Schranke aus `abrufschutz`, **und der Lauf meldet, dass er sie benutzt hat**. Preis: ein um einen Tag verspätetes Signal. Gewinn: nie eine Teilkerze, und die Abweichung ist sichtbar.

---

## Die Quelle: `data/` mit Rückfall

1. `data/<symbol>_<intervall>.csv` lesen
2. Kerzen ohne Kurse streichen (`kursdaten.entferne_unvollstaendige`)
3. Frische prüfen — fehlt die erwartete Entscheidungskerze: **`abruf()`**, also genau der bisherige Live-Abruf des Bots
4. ⚠️ **auf beide Quellen dieselbe Regel anwenden**

Schritt 4 ist der wichtigste: hätte der Ausnahmefall ein anderes Verhalten als der Normalfall, wäre ausgerechnet der Fall ungeprüft, den niemand ansieht. Geprüft am Ablauf, und einzeln abgeschaltet (Mutationsprobe 12.4).

### ⚠️ Befund: heute greift der Rückfall bei **sechs von neun** Bots

`data/` wird von **keinem Cronjob aktuell gehalten.** Für keinen der acht `fetch_*.py` gibt es einen Crontab-Eintrag — sie wurden nur für Backtests von Hand gestartet, weil die Bots ohnehin live abriefen.

Gemessen am 15.09.2026, `python3 shared/entscheidungskerze.py`:

| | Dateien | Stand | Folge |
|---|---|---|---|
| `_1h` (Krypto) | **25 von 25 veraltet** | endet `2026-09-15 08:00`, erwartet `19:00` | `elliott_wave` fällt zurück |
| `_4h` (Krypto) | **24 von 24 veraltet** | endet `2026-09-15 04:00`, erwartet `16:00` | `t3_supertrend` fällt zurück |
| `_1d` (Krypto) | **24 von 24 frisch** | endet `2026-09-14` | die drei täglichen Krypto-Bots lesen `data/` |
| `_1d` (Aktien) | **150 von 150 veraltet** | endet `2026-09-01` (APH: `2026-08-31`) | alle vier Aktien-Bots fallen zurück |
| **gesamt** | **199 von 223 ohne die erwartete Kerze** | | |

**Das ist kein Schaden.** Die Bots laufen weiter, rufen live ab wie bisher, und der Filter greift auf **beiden** Wegen gleich. Es heisst nur, dass der beabsichtigte Datenweg noch nicht wirkt. → **Offener Punkt 24**: Crontab-Einträge für die `fetch_*.py`, zeitlich **vor** den Bot-Läufen. TB-38 durfte die Crontab nicht anfassen; ein Vorschlag steht im Testauftrag, eingetragen ist er nicht.

---

## Die Meldung

Eine Meldung in `logs/` ist keine Meldung. Gemeldet wird deshalb über **`notify.send_alert()`** — die eine Telegram-Leitung des Projekts, dieselbe, die TB-32 benutzt. Keine zweite Anbindung, keine Änderung an `notify.py`, kein Crontab-Eintrag.

Gedämpft wird mit den **Funktionen** aus `notifications/waechter_melden.py`, nicht mit einer zweiten Fassung derselben vier Regeln: *neu* → melden; *geändert* → melden; *Nachholung* → melden; *Erinnerung* (unverändert, ≥ 7 Tage) → melden; sonst **schweigen**.

Ohne Dämpfung wären es bei dauerhaft veraltetem `data/` bis zu sechs Nachrichten am Tag, dauerhaft — nach einer Woche dasselbe wie keine Meldung.

Drei harte Bedingungen, alle aus TB-32 übernommen:

* **Genau einmal je Lauf**, alle betroffenen Symbole in **einer** Nachricht — nicht 25.
* Der Meldeteil **bringt den Bot nie zum Scheitern** (alles in einem `try`).
* Ein fehlgeschlagener Versand gilt als **nicht zugestellt** und wird nachgeholt.

Fehlt `waechter_melden`, wird **ungedämpft** gemeldet statt gar nicht: eine Nachricht zu viel, nie eine verschluckte. Zustand: `notifications/rueckfall_zustand.json` (in `.gitignore`).

---

## Der Umstellungstag

| | |
|---|---|
| **Journal** | `docs/DATENLUECKEN.md` — eigener Zäsur-Eintrag plus ein neuer Abschnitt „Eine **dritte** Art, warum ein Zeitraum nicht auswertbar ist" |
| **maschinenlesbar** | **`docs/umstellungstag_entscheidungskerze.json`** |
| **geschrieben von** | `shared/umstellungstag.py --festhalten --alle` (Schritt 9 des Testauftrags) |
| **gelesen von** | dem Vergleich — **nicht** von den Bots |

**Warum `docs/`:** nicht `shared/` oder `strategies/` (eine Datei neben dem Bot-Code lockt den nächsten Leser dazu, sie im Live-Pfad zu benutzen — dann wäre eine Aufzeichnung *über* den Betrieb zu einem Eingang *des* Betriebs geworden); nicht `data/` (das sind Kursdateien, und ihr SHA-256 ist der Datenstand-Hash der Vorregistrierung); nicht `results/` (überschreibt der nächste Lauf). In `docs/` steht die Prosa-Fassung derselben Zäsur ein Verzeichnislisting weiter.

**Ein zweiter Aufruf rückt den Zeitpunkt nicht vor.** Der Umstellungstag ist eine Tatsache, kein Zustand; ein stilles Vorrücken würde den Anfang des Vergleichsfensters verschieben, ohne dass es jemandem auffiele. `--erneut` überschreibt ausdrücklich und bewahrt den alten Wert als `frueher`.

⚠️ **Papierpfade vor diesem Tag gelten für den Vergleich Backtest gegen Live als nicht vergleichbar.** Der Vergleich beginnt für diese Bots **neu**. Bis zum Stichtag der Neuselektion am **13.12.2026** ist das das gesamte verfügbare Fenster.

---

## Prüfungen

| | |
|---|---|
| `python3 shared/test_entscheidungskerze.py` | **130 Prüfungen**, alle bestanden |
| `python3 shared/test_umstellungstag.py` | **25 Prüfungen**, alle bestanden |
| bestehende Selbsttests | **unverändert** gegenüber dem Basislauf auf `main` (siehe unten) |

### Der Nachweis, der zählt: drei Bots wirklich gestartet

Drei der neun `forward_test.py` laufen im Test **tatsächlich**, in einem Miniatur-Abbild des Projekts unter `/tmp`, gegen erzeugte Beispieldaten. Beobachtet wird, was danach in ihrer **Datenbank** steht — nicht, ob im Quelltext ein Aufruf vorkommt.

Der Zustand wird dabei **nicht von Hand hergestellt**: die Kursreihe trägt eine laufende Kerze mit einem Tief, das einen Stop reissen *würde*, und ein Signal, das ein Bot eröffnen *würde*. Ob das passiert, entscheidet der **Ablauf**.

**Dieselben Prüfungen gegen die unveränderten Bots von `main` — 7 von 13 fallen durch, und zwar genau so, wie der Befund es vorhersagt:**

| Prüfung | auf `main` | nach TB-38 |
|---|---|---|
| `t3_supertrend`: Position bleibt offen | ❌ geschlossen als `stop_loss`, Ausstiegszeit `2026-09-15 20:00:00` — **die laufende Kerze** | ✅ offen |
| `t3_supertrend`: kein Live-Abruf bei frischem `data/` | ❌ ruft ab (`binance TESTUSDT 4h`) | ✅ liest `data/` |
| `turtle_soup_crypto`: kein Trade aus der laufenden Kerze | ❌ eröffnet `2026-09-15 00:00:00` | ✅ kein Trade |
| `turtle_soup_crypto`: auch beim **Rückfall** kein Trade | ❌ eröffnet | ✅ kein Trade |
| `turtle_soup_crypto`: genau einmal gemeldet | ❌ keine Meldung | ✅ genau eine |
| `turtle_soup_stocks`: kein Live-Abruf | ❌ ruft ab | ✅ liest `data/` |
| `turtle_soup_stocks`: kein Trade aus der laufenden Tageszeile | ❌ eröffnet `2026-09-16` | ✅ kein Trade |

### Backtest und Forward-Test wählen dieselbe Kerze

Geprüft **nicht** gegen eine nachgebaute Backtest-Regel, sondern gegen den **echten Schreibweg** des Projekts: was der Backtest liest, ist die CSV, die `fetch_*.py` geschrieben hat, und die schreibt seit TB-35 genau das, was `abrufschutz.nur_abgeschlossene` durchlässt — eine Regel, die **unabhängig** von dieser Schicht geschrieben wurde und sie nicht kennt.

Über **alle** Zeitpunkte von drei Intervallen (1 h, 4 h, 1 d) × je 95–195 Kerzen × je 4 Zeitversätze — rund **1 500 Vergleiche** — nennen beide Wege **dieselbe** letzte Kerze.

⚠️ **Mit genau einer Ausnahme, und die ist Absicht:** auf der Millisekunde des Kerzenschlusses nimmt der Schreibpfad die Kerze (`<=`), der Lesepfad nicht (`<`). Das ist die Vorgabe der Aufgabe. Kein Cron-Eintrag trifft diesen Zeitpunkt. → Offener Punkt 25, festgehalten als Test (11.2), damit es niemand für eine Panne hält.

### Mutationsproben

Neun Stück. Jede schaltet **eine** Absicherung ab und prüft nach, dass genau die zugehörige Prüfung daraufhin **fehlschlägt** — und die anderen nicht:

| # | abgeschaltet | erwartet |
|---|---|---|
| 12.1 / 12.2 | der Filter ganz | Normalfall **und** Rückfall fallen durch |
| 12.3 / 12.4 | der Filter **nur im Rückfall** | Normalfall bleibt grün, **Rückfall fällt durch** — die eine Wache verdeckt das Fehlen der anderen nicht |
| 12.5 | die Frischeprüfung (sagt immer „frisch") | der Rückfall greift nicht mehr |
| 12.6 | das strikte `<` wird ein `<=` | die Grenzprüfung fällt durch |
| 12.7 | die Dämpfung | die Dämpfungsprüfung fällt durch |
| 12.8 | `entscheidung()` sagt immer „melden" | es **wird** gemeldet, auch bei leerem Sammler → es gibt keine zweite Wache daneben |

Vorher wird geprüft, dass **alle sechs Proben ohne Mutation grün sind** — sonst sagt eine rote Mutationsprobe nichts aus.

### Basislauf (Cloud, `main` unverändert) — und danach

Identisch. Rot sind vorher wie nachher dieselben vier, alle als TB-38-fremd bekannt:

| Test | Grund |
|---|---|
| `shared/test_drawdown_beide_masse.py` | Zeitüberschreitung (124) |
| `shared/test_kursdaten.py` | vorbestehend |
| `shared/test_stabile_sortierung.py` | zwei Bots über `MIN_LIVE_CLOSED_TRADES`, gemeinsames Fenster leer |
| `shared/test_wellenauswahl.py` | `ergebniskurven.py` nach TB-34 |

Alle übrigen 20 grün, vorher wie nachher — einschliesslich `shared/test_abrufschutz.py` (TB-35 unberührt) und `notifications/test_waechter_melden.py` (TB-32 unberührt).

*Abweichung zur Umgebungsnotiz der Aufgabe:* `pandas`, `numpy` und `pandas_market_calendars` wurden in dieser Cloud-Sitzung nachinstalliert, damit die Aktien-Prüfungen gegen den **echten** Kalender laufen konnten. Der Basislauf oben wurde **mit** diesen Paketen und auf **unverändertem** `main` erhoben, ist also eine gültige Vergleichsbasis.

---

## Randbedingungen — nachgeprüft

| Auflage | Stand |
|---|---|
| Basis enthält `0f696b0` | ✅ `git merge-base --is-ancestor 0f696b0 origin/main` |
| keine Kursdatei verändert | ✅ `git status --porcelain data/` leer; Datenstand `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223** Dateien — unverändert |
| `live_params.py` unberührt | ✅ neun Dateien, keine im Diff |
| `research/vorregistrierung/auswertung.py`, `docs/VORREGISTRIERUNG_neuselektion.md` | ✅ nicht im Diff |
| keine `equity_simulation.py`, `multi_symbol_optimise.py`, `multi_symbol_walk_forward.py` | ✅ nicht im Diff |
| `shared/zuteilung.py`, `messkette.py`, `regimewache.py`, `binance_historie.py`, `kursdaten_neuaufbau.py`, `zeitabdeckung.py`, `fetch_binance_data.py` | ✅ alle unberührt |
| nichts unter `broker/`, keine Crontab, kein `results/*.csv` | ✅ nicht im Diff |
| Bot-Dateien gelesen, nie importiert | ✅ die drei gestarteten Bots laufen als **Unterprozess** in einem eigenen Baum |
| Diff je `forward_test.py` klein und lesbar | ✅ +14/−1 bzw. +15/−1, davon 9 Kommentarzeilen |

**`shared/abrufschutz.py` wurde angefasst** — additiv, ohne Verhaltensänderung: ein öffentlicher Name (`oeffnungszeiten_ms`) für eine bereits vorhandene private Funktion, damit die Umrechnung nicht ein zweites Mal geschrieben werden muss. `shared/test_abrufschutz.py` läuft unverändert grün.

---

## Was offen bleibt

| # | Punkt |
|---|---|
| **24** | **`data/` wird von keinem Cronjob aktuell gehalten** → sechs von neun Bots fallen zurück. Crontab-Einträge für die `fetch_*.py` sind zu entscheiden (Vorschlag im Testauftrag, **nicht** eingetragen) |
| **25** | Schreibpfad (`<=`) und Lesepfad (`<`) unterscheiden sich um **eine Millisekunde** je Kerze. Bewusst nicht angeglichen — eine Änderung an `abrufschutz` wäre eine Änderung am Datenstand-Hash |
| **26** | Die **Lesart von `close_time`** ist eine Auslegung (Binance-Feld 6). Sie sollte einmal bewusst bestätigt werden |
| — | **Nebenbefund:** die Angabe „Minute 5 nach der Vier-Stunden-Grenze, fünf Minuten alt" aus der Aufgabenbeschreibung trifft nicht zu — `5 */4` ist die Broker-Brücke, der Bot steht auf `0 */4`, und Cron zündet in Ortszeit. Die Teilkerze war 2–3 Stunden alt. Mit `crontab -l` und `date +%Z` zu bestätigen (Schritt 2 des Testauftrags) |
| — | Wie viele Trades der bisherige Papierpfad durch die Teilkerze anders eröffnet oder geschlossen hat, ist **nicht rekonstruierbar**: welche Werte eine Teilkerze im Augenblick des Laufs hatte, steht nirgends |

---

## In einfacher Sprache

**Was wir wissen wollten.**
Die neun Handelsprogramme („Bots") schauen sich Kursverläufe an und entscheiden dann: kaufen, verkaufen oder nichts tun. Kursverläufe werden in **Kerzen** dargestellt — jede Kerze fasst einen Zeitabschnitt zusammen, zum Beispiel vier Stunden oder einen Tag. Eine Kerze ist erst dann vollständig, wenn ihr Zeitabschnitt abgelaufen ist. Die Frage war: **Schauen die Bots auf fertige Kerzen — oder auf eine, die gerade erst angefangen hat?**

**Was herauskam.**
Fünf der neun Bots schauten auf eine Kerze, die gerade erst angefangen hatte. Beim Vier-Stunden-Bot war sie im Extremfall nur wenige Minuten alt: der Kurs war eben erst aufgeschlagen, es war praktisch noch nichts passiert. Die Bots trafen also Entscheidungen auf einem Bild, das noch gar nicht fertig gemalt war. Die vier Aktien-Bots machten es zufällig richtig — aber nur, **weil sie zu einer günstigen Uhrzeit laufen**, nicht weil es ihnen jemand vorgeschrieben hätte.

**Warum das so ist.**
Beim Prüfen einer Strategie („Backtest") rechnet man immer mit fertigen Kerzen — man geht ja die Vergangenheit durch, dort ist alles abgeschlossen. Im laufenden Betrieb war es anders. Damit wurde zwei Mal Verschiedenes gerechnet, und die Ergebnisse des laufenden Betriebs konnten die Prüfung gar nicht bestätigen. Das ist deshalb wichtig, weil der laufende Betrieb der **einzige** unabhängige Beweis dafür ist, dass eine Strategie taugt.

**Was das für dich heisst.**
Ab jetzt schauen alle neun Bots auf die zuletzt **fertige** Kerze. Die vier Aktien-Bots verhalten sich dadurch genau wie bisher — das war die Probe, dass die neue Regel stimmt. Die fünf Krypto-Bots verhalten sich anders als vorher, und zwar richtiger.

Drei Dinge solltest du wissen:

1. **Der Vergleich „Prüfung gegen Wirklichkeit" fängt für diese Bots neu an.** Alles, was vorher im laufenden Betrieb passiert ist, zählt für diesen Vergleich nicht mehr. Der Tag, ab dem es zählt, wird beim Umstellen automatisch aufgeschrieben.
2. **Es bleibt wenig Zeit.** Bis zum 13.12.2026 sind es 89 Tage, und ein zweites Vergleichsfenster gibt es nicht.
3. **Eine Sache musst du selbst noch entscheiden.** Die Bots sollen ihre Kurse aus einem gespeicherten Ordner lesen statt jedes Mal im Internet nachzufragen. Dieser Ordner wird aber momentan von nichts automatisch aufgefrischt. Solange das so ist, fragen sechs der neun Bots weiter im Internet nach — **sie laufen also ganz normal weiter**, aber du bekommst eine Telegram-Nachricht, die dich darauf hinweist. Ein Vorschlag, wie man den Ordner automatisch auffrischt, steht in der Testanleitung. Eintragen musst du ihn selbst — an deinem Zeitplan wurde bewusst nichts verändert.
