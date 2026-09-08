# Kurslücke: Wurzelkorrektur oder Cronjob-Zeitpunkt?

**Status: reine Untersuchung. KEINE Änderung an `forward_test.py`, `fetch_stock_data.py`, `live_params.py` oder am Cronjob-Verhalten.** Alle Skripte liegen ausschliesslich unter `research/datenluecke_wurzelkorrektur/`.

---

## 0. Entscheidungsgrundlage

### Datenbasis

| | |
|---|---|
| geprüfter Code | `fetch_stock_data.py` (4 identische Kopien), `forward_test.py` der vier Aktien-Bots |
| geprüfte Kursdaten | 150 Aktien-Tagesdateien, **1.417.557 Balken** |
| Signal-Nachspielung | 3 Bots × 150 Symbole × volle Historie, 166.749 Signalbalken insgesamt |
| Zeitzonen-Rechnung | 783 Wochentage, 2023-09-01 bis 2026-09-01 |
| Sanity-Checks | `test_wurzelkorrektur.py`: **25 Checks, alle bestanden** |

### Pflicht-Gegenchecks

- **Die Indikator-Berechnung wurde nicht nachgebaut**, sondern per `compute_indicators` direkt aus dem `forward_test.py` des jeweiligen Bots importiert. Nachgebildet ist nur die eine Signal-Bedingung; sie steht in Abschnitt 4 wörtlich neben dem Original und wird von vier Miniatur-Testfällen je Bot geprüft.
- **Ein Testfall hat einen Fehler in meiner eigenen Vorgabe gefunden** (ein Turtle-Soup-Beispiel, das ich als „kein Setup" gedacht hatte, war eines) — die Bedingung war richtig, die Erwartung falsch. Im Test dokumentiert.
- **Zeitzonen über `zoneinfo`**, nicht über feste Stundenversätze; die Sommerzeit-Übergangsfenster sind ausdrücklich mitgeprüft.
- **Kein Netzwerkzugriff möglich** (siehe Belastbarkeit) — alle Aussagen stammen aus Code, gespeicherten Daten und Kalenderrechnung.

### Belastbarkeit

Die Häufigkeits- und Signalzahlen sind exakte Auszählungen, keine Schätzungen. Drei echte Grenzen:

1. **Yahoo war von hier aus nicht erreichbar** (`HTTP 403` am Proxy). Was `yfinance` während einer laufenden Sitzung genau liefert, konnte ich **nicht** empirisch prüfen — die Aussagen dazu stützen sich auf das beobachtbare Ergebnis in den gespeicherten Dateien, nicht auf einen Live-Test.
2. **Die Crontab liegt auf dem Mac und ist von hier nicht lesbar** (anderer Rechner, kein `crontab`-Binary). Der tatsächliche Cron-Zeitpunkt ist damit **unbekannt**; Abschnitt 5 rechnet deshalb alle plausiblen Kandidaten durch, statt einen anzunehmen.
3. Die gespeicherten CSVs sind **eine** Momentaufnahme (Abruf zwischen dem 2026-09-01er Börsenschluss und dem 2026-09-02, 23:12 Berliner Zeit — per `git log` datiert). Sie zeigen, was bei *diesem* Abruf passiert ist, nicht die Historie aller Cron-Läufe.

### Scope-Grenzen

Keine Code- oder Cronjob-Änderung. Keine Aktivierungsempfehlung. `elliott_wave_stocks` ist in der Signal-Nachspielung nicht enthalten (Begründung in Abschnitt 4); die Preis-Aussage gilt für ihn dennoch, weil er den Einstiegspreis nach demselben Muster bucht.

### Reproduktion

```
cd research/datenluecke_wurzelkorrektur
python3 test_wurzelkorrektur.py      # 25 Sanity-Checks
python3 datenlage.py                 # Häufigkeit unvollständiger Balken
python3 signalverschiebung.py        # Auswirkung auf Signalzeitpunkte und Einstiegspreise
python3 cron_zeitfenster.py          # Börsenschluss gegen Cron-Kandidaten
```

---

## 1. Kurzfassung

**Die Antwort auf die Kernfrage: seltener Einzelfall, kein struktureller Regelfall — aber die Prämisse trifft den beobachteten Fall gar nicht.**

- **Über alle 150 Aktien und 1.417.557 Balken gibt es genau EINEN Balken mit fehlenden Preisen** — den bekannten APH-Fall vom 2026-09-01. Das sind 0,00007 % aller Balken.
- **Dieser Balken war kein laufender Handelstag.** Sein Volumen betrug 7.650.337 Stück, das **1,40-fache** von APHs üblichem Tagesvolumen. Ein während der Sitzung abgerufener Balken hätte einen Bruchteil davon. Es fehlten die Preise bei vollem Volumen — eine Yahoo-seitige Unstimmigkeit für dieses eine Symbol an einem **abgeschlossenen** Handelstag.
- **Auch alle anderen 149 Symbole zeigen einen abgeschlossenen Tag** (Volumen des letzten Balkens im Median beim 1,02-fachen der Vortage, kein einziges unter dem 0,57-fachen). Der Abruf fand nach Börsenschluss statt.
- **Damit greift die Wurzelkorrektur am falschen Hebel.** „Den letzten Balken verwerfen, weil der Handelstag noch läuft" hätte diesen Fall zwar zufällig mit erwischt (er war der letzte Balken), löst aber nicht das beobachtete Problem — und schützt nicht davor, dass derselbe Defekt an einem anderen Tag mitten in der Historie auftritt.

**Und eine Korrektur an der Annahme aus PR #33:** dort steht, die Wurzelkorrektur würde „Signale einen Tag früher auslösen". Der Code sagt das Gegenteil. `find_new_signals()` wertet `df.iloc[-1]` aus — den jüngsten Balken. Fällt dieser weg, entscheidet der Bot an Tag D über Balken D-1, handelt also **einen Börsentag SPÄTER** und bucht als Einstiegspreis den **Schlusskurs des Vortags**. Wie viel das ausmacht, steht in Abschnitt 4.

**Der wunde Punkt liegt woanders — und er ist offen:** Wenn der Cronjob wirklich um **22:00 Berliner Zeit** läuft, wie das Übergabeprotokoll dokumentiert, dann startet er an 92,3 % der Handelstage **exakt zur Schlussglocke** (Abschnitt 5). Ob Yahoo den Tagesbalken zu diesem Zeitpunkt bereits final ausliefert, ist die eigentliche Risikofrage — und die lässt sich nur mit dem echten Cron-Eintrag beantworten, den ich nicht lesen kann.

---

## 2. Frage 1: Der Mechanismus

Alle vier Aktien-Bots rufen dieselbe, in vier identischen Kopien vorliegende Funktion auf (`diff` bestätigt: byte-gleich):

```python
# strategies/<bot>/fetch_stock_data.py
def fetch_historical_data(ticker, period=PERIOD, interval=INTERVAL):
    df = yf.download(ticker, period=period, interval=interval,
                     progress=False, auto_adjust=True)
```

`forward_test.py` ruft sie mit `period="2y"` bzw. `"3y"` und `interval="1d"` auf. **Es gibt keinen `end`-Parameter und keinen Zeitfilter.** Was Yahoo als jüngste Zeile liefert, landet unverändert im DataFrame; `df.iloc[-1]` ist damit der jüngste von Yahoo gelieferte Tagesbalken — unabhängig davon, ob dieser Tag abgeschlossen ist.

**Gibt es eine yfinance-Option, die einen laufenden Tag von vornherein ausschliesst?** `yf.download()` kennt `start`/`end` statt `period`. Ein `end` auf den heutigen Tag würde den laufenden Tag ausschliessen (das `end`-Datum ist exklusiv). Das ist technisch die einzige eingebaute Möglichkeit — **verifizieren konnte ich es nicht**, weil Yahoo von hier nicht erreichbar ist. Es wäre funktional dasselbe wie „letzten Balken verwerfen", mit denselben Folgen für die Signalzeitpunkte (Abschnitt 4).

**Wo der Guard aus PR #33 ansetzt:** `balken_unvollstaendig()` prüft jeden Balken auf fehlende Preise und überspringt ihn mit sichtbarer Meldung. Der Guard wirkt damit **unabhängig davon, wo** in der Historie ein defekter Balken auftritt — die Wurzelkorrektur würde nur den letzten schützen.

---

## 3. Fragen 2 und 3: Häufigkeit — Einzelfall, kein Regelfall

`datenlage.py` über alle 150 Aktien-Tagesdateien:

| | |
|---|---|
| Balken insgesamt | 1.417.557 |
| Balken mit fehlenden Preisen | **1** (0,00007 %) |
| davon der letzte Balken der Datei | ja (APH, 2026-09-01) |
| fehlende Preise | alle vier (Open/High/Low/Close) |
| Volumen dieses Balkens | 7.650.337 — das **1,40-fache** von APHs 20-Tage-Median |

**Der entscheidende Gegencheck: war der letzte Balken ein laufender Handelstag?**

Das sieht man einem Balken nicht direkt an — wohl aber seinem Volumen. Über alle 150 Symbole:

| Volumen des letzten Balkens / Median der 20 Vortage | |
|---|---|
| Median über alle Symbole | **1,019** |
| 5 %-Quantil | 0,731 |
| 95 %-Quantil | 1,760 |
| Minimum | 0,565 |
| Anteil unter 0,5 | **0,0 %** |

Ein während der Sitzung abgerufener Balken trüge einen Bruchteil des Tagesvolumens. Hier liegt das Volumen im normalen Bereich — **der Handelstag war beim Abruf abgeschlossen, bei allen 150 Symbolen**. Alle 150 Dateien enden auf demselben Tag (2026-09-01, Dienstag), 149 davon mit einem vollständigen Balken.

**Schlussfolgerung:** Der APH-Fall ist keine Folge eines zu frühen Abrufs, sondern ein Datenfehler bei Yahoo für ein einzelnes Symbol an einem abgeschlossenen Tag: Volumen geliefert, Preise nicht. Ein struktureller Regelfall liegt **nach dieser Datenlage nicht vor**.

**Zwei Einschränkungen, die diese Aussage nicht überdehnen lassen:**
1. Die CSVs sind eine Momentaufnahme eines einzelnen Abrufs (per `git log` datiert auf den Zeitraum zwischen dem 09-01er Schluss und dem 09-02, 23:12 Berliner Zeit). Sie belegen nicht, dass **kein** Cron-Lauf je einen laufenden Tag erwischt hat.
2. Die Bots rufen bei jedem Lauf frisch ab; diese Dateien stammen aus einem `fetch_stock_data.py`-Sammellauf. Für die Frage, ob der *Cronjob* riskant terminiert ist, ist deshalb Abschnitt 5 massgeblich, nicht dieser hier.

---

## 4. Frage 4: Was die Wurzelkorrektur an den Signalen ändern würde

`signalverschiebung.py` spielt die Live-Signalregel der drei regelbasierten Aktien-Bots über die gesamte Historie aller 150 Symbole nach.

### Die Richtung: einen Tag SPÄTER, nicht früher

`find_new_signals()` entscheidet auf `df.iloc[-1]` und bucht `entry_price = row["close"]`, `entry_time = row["open_time"]` — beides vom **jüngsten** Balken. Fällt dieser weg:

| | heute | mit Wurzelkorrektur |
|---|---|---|
| an Tag D geprüfter Balken | D | **D-1** |
| gebuchter Einstiegspreis | Schluss von D | **Schluss von D-1** |
| gebuchter Einstiegszeitpunkt | D | **D-1** |

**Kein Signal geht verloren** — jeder Balken wird in beiden Varianten genau einmal geprüft; das ist keine Messung, sondern folgt aus der Konstruktion (im Test nachgerechnet). Verschoben wird ausschliesslich, **wann** gehandelt wird und **zu welchem Preis**.

### Die Höhe: gemessen an 166.749 Signalbalken

| Bot | geprüfte Balken | Signalbalken | \|Δ Einstiegspreis\| Median | 90 %-Quantil | > 1 pp | > 3 pp |
|---|---:|---:|---:|---:|---:|---:|
| `rsi2_mean_reversion` | 1.417.557 | 43.578 | **1,33 pp** | 3,92 pp | 61,0 % | 17,5 % |
| `turtle_soup_stocks` | 1.417.557 | 89.871 | **0,82 pp** | 2,87 pp | 42,7 % | 9,2 % |
| `volatility_breakout` | 1.417.557 | 33.300 | **1,82 pp** | 4,83 pp | 74,1 % | 26,1 % |

Lesart: bei `volatility_breakout` läge der gebuchte Einstiegspreis in **74 % aller Signale um mehr als einen Prozentpunkt** neben dem heutigen, in gut einem Viertel der Fälle um mehr als drei. Das ist kein Rundungseffekt — es ist eine andere Handelsentscheidung.

Dass die Ausschläge bei `volatility_breakout` am grössten sind, passt zur Strategie: sie steigt gerade an Ausbruchstagen ein, also an Tagen mit überdurchschnittlicher Bewegung.

**Warum `elliott_wave_stocks` fehlt:** seine Regel hängt an einer Zigzag-Wellenerkennung über die gesamte Historie plus einem Frischefenster von fünf Tagen; eine ehrliche Nachspielung müsste die Wellenerkennung für jeden einzelnen Handelstag neu rechnen. Die **Preis-Aussage gilt für ihn dennoch**: auch er bucht `entry_price` als Schlusskurs des jüngsten Balkens (`latest_price_row.iloc[-1]["close"]`). Sein Frischefenster von fünf Tagen fängt die Verschiebung um einen Tag zusätzlich ab — ein Signal ginge dort mit hoher Wahrscheinlichkeit nicht verloren, nur später ausgeführt.

### Die stille Kehrseite: welcher Preis ist überhaupt der richtige?

Die Backtests aller vier Bots setzen den Einstieg auf den **Schlusskurs des Signaltags** an. Heute trifft der Live-Bot das genau dann, wenn der Abruf nach Börsenschluss erfolgt — dann ist `df.iloc[-1]["close"]` der echte Schlusskurs. Erfolgt der Abruf während der Sitzung, bucht er stattdessen einen Zwischenstand als „Schlusskurs".

Die Wurzelkorrektur würde umgekehrt **immer** einen echten Schlusskurs buchen, aber den vom Vortag — und damit systematisch vom Backtest abweichen, der den Schluss des Signaltags unterstellt.

**Beide Fehlerarten hängen also am selben Punkt: ob zum Abrufzeitpunkt ein abgeschlossener Handelstag vorliegt.** Das führt direkt zu Frage 5.

---

## 5. Frage 5: Die Alternative — Cronjob später laufen lassen

### Wann schliesst die US-Börse in unserer Zeitzone?

`cron_zeitfenster.py`, 783 Wochentage von 2023-09-01 bis 2026-09-01:

| Börsenschluss (16:00 New York) | in Berliner Zeit | Anteil |
|---|---|---|
| an 723 Tagen | **22:00 Uhr** | 92,3 % |
| an 60 Tagen | 21:00 Uhr | 7,7 % |

Die 60 Ausnahmetage sind die Wochen, in denen die USA und Europa nicht gleichzeitig umgestellt haben. Sie machen den Schluss **früher**, sind also die harmlose Richtung.

### Was das für Cron-Kandidaten bedeutet

| Cron-Zeitpunkt | kleinster Abstand zum Schluss | grösster | Tage VOR Schluss | Tage mit < 30 min Abstand |
|---|---:|---:|---:|---:|
| **22:00 Berliner Zeit** (Protokoll: „werktags 22 Uhr") | **0 min** | 60 min | 0 | **723** |
| 22:05 Berliner Zeit | 5 min | 65 min | 0 | 723 |
| **22:30 Berliner Zeit** | **30 min** | 90 min | 0 | **0** |
| 23:00 Berliner Zeit | 60 min | 120 min | 0 | 0 |
| 22:05 UTC (= 00:05 Berliner Zeit) | 65 min | 125 min | 0 | 0 |

**Der wichtige Befund:** Läuft der Cronjob um 22:00 **Berliner Zeit**, startet er an 92,3 % der Handelstage **im selben Moment wie die Schlussglocke**. Kein einziger Lauf liegt vor Börsenschluss — aber der Abstand ist null. Ob Yahoo den Tagesbalken in dieser Minute schon final ausliefert, entscheidet dann darüber, ob der Bot einen echten oder einen vorläufigen Schlusskurs bucht.

**Ab 22:30 Berliner Zeit hat jeder Lauf mindestens 30 Minuten Abstand** — an jedem einzelnen der 783 geprüften Tage.

### Ungeklärt und nur vom Nutzer zu klären

Das Übergabeprotokoll dokumentiert „werktags 22 Uhr" **ohne Zeitzone**. Die Aufgabenstellung nennt „22:05 UTC laut vorheriger Verifikation" — eine solche Verifikation habe ich nicht vorgenommen; ich konnte die Crontab in keiner Sitzung lesen, weil sie auf dem Mac liegt und diese Umgebung ein separater Linux-Container ohne `crontab`-Binary ist. Die beiden Lesarten unterscheiden sich fundamental:

- **22:00 Berliner Zeit** → 0 Minuten Abstand an 92 % der Tage → das wäre der strukturell riskante Fall.
- **22:05 UTC** (= 00:05 Berliner Zeit) → mindestens 65 Minuten Abstand → unbedenklich.

Zu klären mit:

```bash
crontab -l | grep -A0 forward_test          # tatsächliche Zeiten
date                                        # Zeitzone des Mac
```

---

## 6. Gegenüberstellung der beiden Lösungswege

| | **A: Datenabruf-Logik ändern** (letzten Balken verwerfen) | **B: Cronjob später legen** |
|---|---|---|
| behebt die Ursache? | nein — behandelt das Symptom an einer anderen Stelle | **ja**, falls die Ursache ein zu früher Abruf ist |
| Eingriff in Handelsentscheidungen | **hoch**: jedes Signal einen Börsentag später, Einstiegspreis im Median 0,8–1,8 pp anders, bei einem Bot in 74 % der Fälle über 1 pp | **keiner**: identische Signale, identische Preise, nur später abgerufen |
| Verhältnis zum Backtest | **entfernt** sich davon (Backtest unterstellt Schluss des Signaltags, gebucht würde der Vortagsschluss) | **nähert** sich ihm an (echter Schlusskurs des Signaltags) |
| geänderte Dateien | 4 × `fetch_stock_data.py` oder 4 × `forward_test.py` — Live-Code | keine Repo-Datei, nur die Crontab |
| Schutz gegen den APH-Fall | nur wenn der defekte Balken zufällig der letzte ist | **keiner** — dagegen wirkt der Guard aus PR #33, und der greift bereits |
| Risiko bei Fehlbedienung | ein Bot, der einen Tag hinterherhandelt, ohne dass es auffällt | ein späterer Lauf; im schlimmsten Fall verschiebt sich die Meldung um eine halbe Stunde |
| umkehrbar | Code-Änderung mit Nachweisaufwand | eine Zeile in `crontab -e` |

**Unaufgeregte Einschätzung zur Eingriffstiefe:** **Weg B ist die deutlich flachere Änderung.** Er verschiebt keine einzige Handelsentscheidung, sondern nur den Zeitpunkt, zu dem dieselbe Entscheidung getroffen wird — und er bringt den Live-Bot näher an die Annahme des Backtests, statt weiter davon weg. Weg A verändert 166.749 historisch nachgezählte Signalzeitpunkte und den gebuchten Preis in der Mehrzahl der Fälle spürbar; er wäre nur dann die richtige Wahl, wenn sich der Abrufzeitpunkt aus einem anderen Grund nicht verschieben lässt.

**Und keiner der beiden Wege ersetzt den Guard aus PR #33:** Der APH-Fall war ein Datenfehler an einem abgeschlossenen Handelstag. Gegen so etwas hilft weder ein späterer Abruf noch das Verwerfen des letzten Balkens — nur das, was heute schon da ist: den defekten Balken erkennen, überspringen und sichtbar melden.

---

## 7. Offene Punkte

1. **Der tatsächliche Cron-Zeitpunkt** (Abschnitt 5) — die eine Angabe, an der die ganze Bewertung hängt, und die einzige, die ich nicht selbst beschaffen kann.
2. **Yahoos Verhalten während einer laufenden Sitzung** war nicht prüfbar (kein Netzwerkzugang). Falls jemand das nachholt: ein Abruf während der US-Sitzung plus ein zweiter nach Schluss, verglichen auf `close` und `volume` des letzten Balkens, würde die Frage in fünf Minuten klären.
3. **Ob der APH-Defekt bei Yahoo inzwischen behoben ist** — die gespeicherte Datei stammt vom 2026-09-02. Ein erneuter Abruf würde zeigen, ob Yahoo den Balken nachträglich vervollständigt hat; das wäre ein Hinweis darauf, wie langlebig solche Defekte sind.
4. **Die drei Krypto-Bots** sind von der Frage strukturell nicht betroffen (Binance handelt durchgehend, es gibt keinen Börsenschluss) — geprüft wurde das hier nicht, es folgt aus der Datenquelle.

---

## 8. Dateien

| Datei | Zweck |
|---|---|
| `datenlage.py` | zählt unvollständige Balken und prüft per Volumenvergleich, ob der letzte Balken ein abgeschlossener Handelstag war |
| `signalverschiebung.py` | spielt die Live-Signalregel je Bot nach und misst die Preisverschiebung |
| `cron_zeitfenster.py` | stellt Börsenschluss und Cron-Kandidaten gegenüber, inkl. Sommerzeit-Übergängen |
| `test_wurzelkorrektur.py` | 25 Sanity-Checks über alle drei Auswertungen |
| `results/*.json` | Rohergebnisse der drei Auswertungen |
