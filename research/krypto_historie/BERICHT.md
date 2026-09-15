# TB-31 — Krypto-Historie zurückladen

**Untersuchung und Werkzeug. Kein Bot-Code, keine Parametrisierung, keine
Kursdatei unter `data/` verändert.** Der eigentliche Ladelauf gehört auf den
Mac des Nutzers; warum, steht in Abschnitt 6.

---

## 0. Der Befund, der zuerst kommen muss

> **Der überlappende Bereich stimmt bei den `*_1d.csv` nicht überein — und
> das ist kein Fehler des Endpunkts, sondern einer des Altbestands.**

Alle **24** Krypto-Tagesdateien sind **abgeleitet**, nicht abgerufen:
`shared/build_daily_crypto_data.py` hat sie aus den 1h-Daten resampelt. Das
ist gemessen, nicht vermutet — bei allen 24 ist der Eröffnungskurs der ersten
Tageskerze auf die letzte Stelle identisch mit dem der ersten Stundenkerze
(`daten/teilkerzen.json`).

Daraus folgen drei Teilkerzen, die in den Dateien wie normale Kerzen aussehen:

| Was | Wieviele | Ausmaß |
|---|---|---|
| **erste** Tageskerze jeder `*_1d.csv` | 24 von 24 | deckt **6 bis 16** statt 24 Stunden ab |
| **letzte** Tageskerze jeder `*_1d.csv` | 24 von 24 | deckt am 2026-08-31 **13** statt 24 Stunden ab |
| **letzte** 4h-Kerze | 23 von 24 | enthält Kursbewegung, die in der 1h-Datei fehlt — die beiden Dateien enden zu **verschiedenen realen Zeitpunkten** |

Für die 13 Symbole mit langer Historie ist die erste Tageskerze der
**2021-09-01 mit 11 Stunden** — die 1h-Reihe beginnt an jenem Tag erst um
13:00 UTC, weil die Abrufskripte mit `LOOKBACK = "1825 day ago UTC"` arbeiten
und der Abruf nachmittags lief.

**Warum das gerade jetzt wichtig ist:** Solange die Datei dort beginnt, sitzt
die Teilkerze am **Rand**. Sobald Historie davorgesetzt wird, sitzt sie
**mitten** in der Reihe — ein stillschweigender 11-Stunden-Tag zwischen
lauter 24-Stunden-Tagen, mitten im Trainingsbereich der Neuselektion.

`shared/kursdaten.py` findet das **nicht**: es prüft auf fehlende Kurse, und
eine Teilkerze hat vier gefüllte Kursspalten. Sie ist nicht leer, sie ist
falsch.

**Wie der Lader damit umgeht:** Er findet die Abweichung beim
Zeile-für-Zeile-Vergleich, **schreibt die Datei nicht** und nennt den Grund.
Erst `--teilkerze-ersetzen` ersetzt **genau diese eine Zeile** durch die
native Tageskerze — ein ausdrücklicher, gezählter, berichteter Schritt.
Voreinstellung bleibt: nicht anfassen, melden.

> **Nebenbefund zur Abgrenzung.** Für die **11 spät gelisteten** Symbole ist
> die erste Tageskerze zwar ebenfalls angeschnitten, aber **richtig
> angeschnitten**: ihr Listing-Tag hat bei Binance auch nativ keine 24
> Stunden Handel. Dort sollte der Vergleich aufgehen. Die Unterscheidung ist
> nicht vorab entschieden, sondern fällt beim Lauf gegen den echten
> Endpunkt — der Lader meldet sie je Datei.

---

## 1. Die zwei Zahlen

### Ab wann reicht die Historie je Symbol zurück?

**Heute:** 13 der 24 Symbole beginnen am **2021-09-01**, alle am selben Tag —
das ist kein Listing-Datum, sondern der Rand des 1825-Tage-Fensters. Die
übrigen 11 beginnen später; bei ihnen **ist** der Dateibeginn das
Listing-Datum, weil sie nach dem 2021-09-01 gelistet wurden und das Fenster
sie daher nicht beschnitten hat.

| Gruppe | Anzahl | Dateibeginn | Ist das das Listing-Datum? |
|---|---|---|---|
| vom 1825-Tage-Fenster **beschnitten** | 13 | 2021-09-01 | **nein** — Messung steht aus |
| **nicht** beschnitten | 11 | 2023-03-17 bis 2026-01-13 | **ja**, gemessen |

Die elf gemessenen: `PROMUSDT` 2023-03-17, `SUIUSDT` 2023-05-03, `PEPEUSDT`
2023-05-05, `WLDUSDT` 2023-07-24, `ENAUSDT` 2024-04-02, `TRUMPUSDT`
2025-01-19, `BMTUSDT` 2025-03-18, `PUMPUSDT` 2025-09-11, `ZKCUSDT`
2025-09-15, `ENSOUSDT` 2025-10-14, `UUSDT` 2026-01-13.

Für die 13 beschnittenen steht die Messung aus — sie braucht den Endpunkt
(Abschnitt 6). `shared/binance_historie.py --messen` erledigt sie mit **einer
Anfrage je Symbol und Zeitrahmen** (`startTime=0, limit=1`).

### Wie viele Testfalten sind je Krypto-Bot möglich?

Gerechnet mit `faltenplan.py`, das die Regel aus Abschnitt 5.3 der
Vorregistrierung nachrechnet (Mindesttraining **4 Jahre**, früheste Falte
2019, Go-Live-Schnitt 2026-09-01, letzte Falte ist die Bestätigungsperiode).

| Bot | Faltenlänge | **heute** | **nach dem Laden** |
|---|---|---|---|
| `elliott_wave` | 2 J | **0** | **2** (2022-2023, 2024-2025) |
| `t3_supertrend` | 1 J | **0** | **4** (2022, 2023, 2024, 2025) |
| `rsi2_crypto` | 1 J | **0** | **4** |
| `turtle_soup_crypto` | 1 J | **0** | **4** |
| `volatility_breakout_crypto` | 1 J | **0** | **4** |

**Heute sind es null, nicht zwei.** Der Auftrag nennt „zwei Testfalten (2024,
2025)"; diese Zahl ergibt sich bei **zwei** Jahren Mindesttraining. Das
Register legt in Abschnitt 5.1 Regel 2 aber **vier** Jahre fest. Beide
Rechnungen sind nachvollziehbar:

```
python3 research/krypto_historie/faltenplan.py                    # 4 Jahre -> 0 Falten
python3 research/krypto_historie/faltenplan.py --mindesttraining 2  # 2 Jahre -> 2 Falten
```

Die Lage ist also **schlechter als im Auftrag angenommen**, nicht besser: Es
bleibt nach der geltenden Regel nicht eine dünne Selektionsstatistik übrig,
sondern **gar keine**. Bleibt nur eine Falte, ist sie nach Regel 7 die
Bestätigungsperiode — es wird nichts selektiert.

**Die Zahl „nach dem Laden" hängt nicht am genauen Listing-Tag.** Sie folgt
allein daraus, dass `BTCUSDT` irgendwann im zweiten Halbjahr 2017 gelistet
wurde: für jeden Tag zwischen dem 2017-07-01 und dem 2017-12-31 ist das erste
zulässige Faltenjahr **2022** (`test_faltenplan.py`, Teil B, prüft genau
das). Erst ein Listing vor dem 2017-01-01 verschöbe sie — Binance gibt es
seit Juli 2017.

**`elliott_wave` bleibt auch nach dem Laden bei zwei Selektionsfalten.** Nicht
wegen der Daten, sondern wegen seiner **Faltenlänge**: zwei Jahre, weil er mit
26,0 gefundenen Trades je Jahr unter der 30er-Schwelle liegt (Register
Abschnitt 5.4). Ein Median über zwei Falten ist dasselbe Problem wie vorher,
nur eine Etage höher. **Das ist eine Entscheidung des Betreibers, keine
dieser Aufgabe** — hier steht nur die Zahl.

---

## 2. Die Verzerrung: wer kommt in den Falten überhaupt vor?

Der point-in-time-Satz der Regel — *„Ein Symbol geht in eine Falte nur ein,
wenn seine Kursdaten mindestens vier Jahre vor Faltenbeginn einsetzen"* — ist
die eigentliche Nachricht dieser Untersuchung.

| Selektionsfalte | Symbole in der Falte |
|---|---|
| 2022 | **3** von 24 |
| 2023 | **6** von 24 |
| 2024 | **9** von 24 |
| 2025 | **13** von 24 |
| *2026 (Bestätigung)* | *13 von 24* |

*(Die Zahlen für 2022–2025 beruhen auf angenommenen Listing-Daten für die 13
beschnittenen Symbole, siehe `daten/annahme_listing.json`. Die Spalte „11 von
24 in keiner Falte" ist dagegen **gemessen** — sie hängt nur an den elf
Dateibeginn-Daten, die das 1825-Tage-Fenster nicht beschnitten hat.)*

Zwei Sätze, die dabei stehen bleiben müssen:

1. **Die früheste Selektionsfalte wird von drei Coins entschieden.** Nicht von
   25, nicht von 24 — von `BTCUSDT`, `ETHUSDT`, `BNBUSDT`.
2. **Elf von 24 Symbolen kommen in KEINER Selektionsfalte vor**, auch nach
   dem Laden nicht. Das früheste unter ihnen (`PROMUSDT`, 2023-03-17) wäre
   erst ab einer Falte 2028 zulässig.

Das ist die **survivorship-nahe Verzerrung** in Zahlen: Die Parameter werden
auf den Paaren ausgewählt, die den Zyklus 2018 und den Bärenmarkt 2022
überlebt haben und lange genug gelistet sind — gehandelt wird anschließend
ein Universum, das zur Hälfte aus Paaren besteht, die in der Auswahl nie
vorkamen. Mehr Historie macht diese Verzerrung **nicht kleiner**; sie macht
sie nur messbar und sie verschiebt sie nach vorn.

**Glätten lässt sich das nicht.** Benennen schon, und `faltenplan.py` weist
es bei jedem Lauf aus.

### Eine Lesart, die ausdrücklich getroffen werden musste

Die Regel sagt „vor dem **je Symbol** mindestens vier Jahre Kursdaten
liegen". Das lässt offen, ob das für **ein** oder für **alle** Symbole gelten
muss. Bei „alle" schöbe das jüngste Paar (`UUSDT`, 2026-01-13) die erste
Falte auf **2031** — es gäbe nie eine Selektion. Gerechnet wird deshalb mit
„mindestens ein Symbol", zusammen mit dem point-in-time-Satz. Die Festlegung
steht im Modulkopf von `faltenplan.py`; **sie gehört in das Register, wenn
der Krypto-Faltenplan dort geschrieben wird.**

---

## 3. Marktphasen

| Phase | heute | nach dem Laden |
|---|---|---|
| Zyklus 2018 (Hoch 2017-12, Bärenmarkt 2018) | **fehlt** | vorhanden (nur `BTCUSDT`, `ETHUSDT`, `BNBUSDT`) |
| Einbruch März 2020 | **fehlt** | vorhanden |
| Bärenmarkt 2022 | vorhanden | vorhanden |

Beide heute fehlenden Phasen liegen nach dem Laden **im Trainingsbereich**,
nicht in einer Testfalte: die erste Testfalte ist 2022. Sie verbessern also
die Schätzung der Parameter, nicht die Zahl der Falten — was genau der Zweck
eines verankerten, expandierenden Trainings ist (Register, Regel 1).

---

## 4. Der Lader — `shared/binance_historie.py`

**Endpunkt.** Ausschließlich `https://api.binance.com/api/v3/klines`,
öffentlich, **ohne Schlüssel**. Kein `/sapi/`, kein `/fapi/`. Das
gitignorierte `shared/fetch_binance_data.py` (enthält Zugangsdaten) wird
**nicht** eingebunden — der Lader benutzt `urllib` direkt. Der Selbsttest
prüft, dass keine Anfrage `signature`, `apiKey` oder `timestamp` mitträgt.

**Ratenbegrenzung.** Binance begrenzt nach Anfragegewicht je IP und Minute
(Standard 6000); `/api/v3/klines` wiegt 2. Drei Vorkehrungen:

1. **Mindestpause** zwischen zwei Anfragen, Voreinstellung 0,25 s — rund 240
   Anfragen/min ≙ 480 Gewicht/min, **unter einem Zehntel** des Budgets.
2. Das Antwort-Kopffeld **`x-mbx-used-weight-1m`** wird gelesen; ab 70 % des
   Budgets wird bis zum Beginn der nächsten Minute ausgesetzt.
3. **429** wird mit `Retry-After` abgewartet und wiederholt; **418**
   (IP-Sperre) **bricht ab** — weiterprobieren verlängert nur die Sperre.

Der Lauf meldet am Ende Anfragen, Wartezeit und Gewichtspausen.

**Verlängern statt überschreiben.** Die vorhandenen Zeilen werden als
**Rohtext** gelesen und **zeichengleich** zurückgeschrieben; nur davor kommt
etwas dazu. Neue Zeilen entstehen über `pandas.to_csv` — dasselbe Werkzeug,
mit dem der Altbestand geschrieben wurde —, damit die Schreibweise nicht
auseinanderläuft. Geschrieben wird erst vollständig daneben, dann umbenannt.

**Der Überlappungsbeweis.** Geladen wird **vom gemessenen Datenbeginn bis zur
letzten vorhandenen Kerze**, also einschließlich des ganzen überlappenden
Bereichs, und dieser wird **Zeile für Zeile** verglichen. Vier Befundarten:

| Art | hart? | Bedeutung |
|---|---|---|
| `fehlt` | ja | die vorhandene Zeile kennt der Endpunkt nicht |
| `kurs` | ja | eine der vier Kursspalten weicht ab |
| `volumen` | ja | Volumen weicht über die Toleranz hinaus ab |
| `volumen_rundung` | nein | Volumen weicht innerhalb 1e-9 relativ ab |

Die Toleranz gilt **nur** für das Volumen und hat einen gemessenen Grund: die
abgeleiteten Tagesdateien führen es als Gleitkomma-Summe von 24
Stundenwerten, sichtbar an Werten wie `7565.2410899999995`. Die vier
Kursspalten werden **exakt** verglichen. Jede Rundungsabweichung wird
trotzdem gezählt und gemeldet.

**Lücken.** Zeitpunkte, die der Endpunkt im vorhandenen Bereich kennt und die
Datei nicht, werden gemeldet — aber **nicht gefüllt**. Dieses Modul
verlängert nach vorn, es flickt nicht.

**`shared/kursdaten.py`** streicht und zählt unvollständige Kerzen im
vorangestellten Teil. Diese Wache steht dort **allein**: den neuen Teil
vergleicht niemand, es gibt ihn ja noch nicht.

**Wiederholbarkeit.** Beginnt die Datei bereits am gemessenen Datenbeginn,
wird **gar nicht geschrieben**. Ein zweiter Lauf lässt sie byte-identisch.

---

## 5. Was geprüft ist

| Datei | Prüfungen | Stand |
|---|---|---|
| `shared/test_binance_historie.py` | **75** | bestanden |
| `research/krypto_historie/test_faltenplan.py` | **38** | bestanden |
| `research/krypto_historie/probelauf.py` (24 Symbole × 3 Zeitrahmen, echte Repo-Dateien) | **453** | bestanden |

Zwei Zusicherungen tragen den Rest:

* **Der Faltenplan-Rechner reproduziert den von Hand geschriebenen
  Aktien-Faltenplan des Registers** (2019–2025 Selektion, 2026 Bestätigung) —
  und liest ihn dafür **aus der Registerdatei**, nicht aus einer Kopie im
  Test. Ändert der Betreiber den Plan, wird der Test rot.
* **Der Probelauf läuft gegen die echten Kursdateien dieses Repos**, nicht
  gegen Spielzeugdaten: im überlappenden Bereich liefert die nachgebildete
  Gegenstelle Zeile für Zeile das, was in `data/` steht. Erzeugt ist nur die
  Vorgeschichte davor.

**Zu den Mutationsproben.** Jede ist zweistufig (ohne Mutation das Richtige,
mit Mutation das Verfälschte) und greift **eine** Wache an, damit keine
zweite das Fehlen der ersten verdeckt. Die drei Wachen des Laders sind
unabhängig geprüft: der Überlappungsvergleich, die enge Bedingung des
Teilkerzen-Sonderfalls, und `kursdaten.entferne_unvollstaendige`.

Eine der Proben hat beim Schreiben **selbst einen Fehler gefunden**: sie
prüfte zunächst auf die Zeichenfolge `nan` in der Kursdatei und blieb grün,
obwohl die Wache abgeschaltet war — `pandas.to_csv` schreibt ein fehlendes
Feld als **leeres** Feld (`2026-09-01,,,,,1234.0`), genau die Form des
APH-Falls, der `shared/kursdaten.py` ausgelöst hat. Die Probe prüft jetzt auf
leere Kursspalten und hält zusätzlich fest, dass `nan` dort **nicht** steht.

Unverändert bestanden: `shared/determinismus.py --schnell` meldet weiterhin
**9× DETERMINISTISCH**, `shared/kursdaten.py` weiterhin genau **einen**
Befund (`APH_1d.csv`, letzte Kerze — ein Aktien-Symbol, von TB-31 unberührt).

---

## 6. Was in der Cloud nicht ging — und was daraus folgt

`api.binance.com` ist aus dieser Umgebung **nicht erreichbar**: die
Egress-Richtlinie beantwortet den CONNECT mit **403**, protokolliert im
Proxy-Status als `connect_rejected` für `api.binance.com:443`. Das ist eine
Richtlinienentscheidung, kein Netzfehler; sie wird nicht umgangen.

**Daraus folgt für die Abgabe:**

* Das **Ladeskript** ist fertig und geprüft — gegen eine nachgebildete
  Gegenstelle, die die echten Repo-Zeilen ausliefert.
* Die **Messung der 13 beschnittenen Startdaten** steht aus. Sie ist
  Schritt 4 des Testauftrags und dauert rund eine Minute.
* Der **Ladelauf** ist Schritt 6 des Testauftrags.
* **Keine Kursdatei unter `data/` wurde verändert.** `git diff` listet dort
  nichts.

### Die Kennzahlen vorher — der eingefrorene Vergleichsstand

Mehr Historie heißt andere Zahlen; das ist erwartet und muss je Bot
ausgewiesen werden. Die **Nachher**-Spalte kann erst der Lauf auf dem Mac
füllen. Hier steht die **Vorher**-Spalte, gemessen auf diesem Stand mit
`python3 shared/ergebniskurven.py`:

| Bot | Markt | Zeitraum der Kurve | Trades | Endkapital | Rendite | MaxDD |
|---|---|---|---|---|---|---|
| `elliott_wave` | krypto | 2021-09-24 bis 2026-08-20 | 130 | 16.777,45 | 67,77 % | −10,17 % |
| `rsi2_crypto` | krypto | 2022-02-15 bis 2026-08-20 | 392 | 12.719,18 | 27,19 % | −13,94 % |
| `t3_supertrend` | krypto | 2021-09-02 bis 2026-08-29 | 656 | 22.169,92 | 121,70 % | −22,40 % |
| `turtle_soup_crypto` | krypto | 2021-10-22 bis 2026-08-28 | 1415 | 25.283,53 | 152,84 % | −34,85 % |
| `volatility_breakout_crypto` | krypto | 2022-03-18 bis 2026-08-30 | 207 | 16.812,68 | 68,13 % | −16,29 % |
| `elliott_wave_stocks` | aktien | 2016-11-11 bis 2026-09-01 | 394 | 51.906,95 | 419,07 % | −22,97 % |
| `rsi2_mean_reversion` | aktien | 2016-09-06 bis 2026-09-01 | 4218 | 13.628,40 | 36,28 % | −19,53 % |
| `turtle_soup_stocks` | aktien | 2016-09-16 bis 2026-09-01 | 8914 | 23.814,54 | 138,15 % | −29,07 % |
| `volatility_breakout` | aktien | 2016-09-19 bis 2026-09-01 | 1461 | 30.958,92 | 209,59 % | −22,46 % |

Der volle Stand liegt als `daten/kennzahlen_vorher.json`.

**Eine überprüfbare Vorhersage für den Lauf auf dem Mac:**
`shared/ergebniskurven.py` meldet heute **9× AKTUELL**. Nach dem Ladelauf muss
es **5× ABWEICHEND** (die fünf Krypto-Bots) und **4× AKTUELL** (die vier
Aktien-Bots) melden. Meldet ein Aktien-Bot ABWEICHEND, hat der Lauf etwas
angefasst, was er nicht anfassen durfte.

> **Die Kurven bitte NICHT neu erzeugen.** `ABWEICHEND` ist nach dem Laden
> richtig. Ob und wann neu gerechnet wird, entscheidet der Betreiber, und es
> gehört in denselben Schritt wie die Neuselektion.

*(Randnotiz zum Auftragstext: Er vermerkt, die Ergebniskurven auf `main`
seien veraltet, weil ein lokaler Commit `94b2e3c` nicht gepusht sei. Auf dem
Stand `9afac63`, auf dem diese Arbeit aufsetzt, melden sie **9× AKTUELL** —
der Commit „Ergebniskurven nach der Zuteilungskaskade (TB-26) neu erzeugt"
ist auf `main`. Es war nichts nachzuziehen, und es wurde nichts nachgezogen.)*

---

## 7. Dateien dieser Untersuchung

| Datei | Was |
|---|---|
| `shared/binance_historie.py` | der Lader (messen, laden, vergleichen, verlängern) |
| `shared/test_binance_historie.py` | 75 Prüfungen, davon 3 zweistufige Mutationsproben |
| `research/krypto_historie/faltenplan.py` | rechnet die Faltenregel aus Abschnitt 5.3 nach |
| `research/krypto_historie/test_faltenplan.py` | 38 Prüfungen, davon 2 zweistufige Mutationsproben |
| `research/krypto_historie/probelauf.py` | Lader gegen echte Repo-Dateien + erzeugte Vorgeschichte |
| `research/krypto_historie/daten/teilkerzen.json` | die gemessenen Teilkerzen je Symbol |
| `research/krypto_historie/daten/annahme_listing.json` | 11 gemessene, 13 **angenommene** Startdaten |
| `research/krypto_historie/daten/kennzahlen_vorher.json` | der eingefrorene Vergleichsstand |
| `docs/TESTAUFTRAG_TB-31_krypto_historie.md` | autonom ausführbar, inkl. der Mac-Schritte |
| `docs/ERGEBNIS_TB-31_krypto_historie.md` | kurzes Ergebnisdokument zum Kopieren |
| `docs/UEBERGABE_TB-31_krypto_historie.md` | Übergabe-Zusammenfassung |

**Diese Untersuchung fasst keinen Bot-Code an.** Die Übernahme der geladenen
Historie in eine Neuselektion ist ein getrennter, ausdrücklich freizugebender
Schritt.
