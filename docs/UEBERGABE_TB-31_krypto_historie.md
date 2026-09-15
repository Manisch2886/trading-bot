# Übergabe TB-31 — Krypto-Historie zurückladen

## Die zwei Zahlen zuerst

**Ab wann reicht die Historie je Symbol zurück?**

**13 der 24 Symbole beginnen heute alle am selben Tag, dem 2021-09-01** — das
ist **kein Listing-Datum**, sondern der Rand des Fensters
`LOOKBACK = "1825 day ago UTC"` in den Abrufskripten. Ihr tatsächlicher
Datenbeginn ist **noch nicht gemessen**: `api.binance.com` ist aus der
Cloud-Umgebung durch die Egress-Richtlinie gesperrt (HTTP 403 auf den
CONNECT, im Proxy-Status als `connect_rejected` protokolliert). Die Messung
ist Schritt 10 des Testauftrags und dauert rund eine Minute.

**Die übrigen 11 sind gemessen** — bei ihnen *ist* der Dateibeginn das
Listing-Datum, weil sie nach dem 2021-09-01 gelistet wurden und das Fenster
sie deshalb nicht beschnitten hat: `PROMUSDT` 2023-03-17, `SUIUSDT`
2023-05-03, `PEPEUSDT` 2023-05-05, `WLDUSDT` 2023-07-24, `ENAUSDT`
2024-04-02, `TRUMPUSDT` 2025-01-19, `BMTUSDT` 2025-03-18, `PUMPUSDT`
2025-09-11, `ZKCUSDT` 2025-09-15, `ENSOUSDT` 2025-10-14, `UUSDT` 2026-01-13.

**Wie viele Testfalten sind je Krypto-Bot möglich?**

| Bot | Faltenlänge | heute | nach dem Laden |
|---|---|---|---|
| `elliott_wave` | 2 J | **0** | **2** |
| `t3_supertrend` | 1 J | **0** | **4** |
| `rsi2_crypto` | 1 J | **0** | **4** |
| `turtle_soup_crypto` | 1 J | **0** | **4** |
| `volatility_breakout_crypto` | 1 J | **0** | **4** |

**Heute sind es null, nicht zwei.** Die im Auftrag genannten „zwei Testfalten
(2024, 2025)" ergeben sich bei **zwei** Jahren Mindesttraining; das Register
legt in Abschnitt 5.1 Regel 2 **vier** fest. Bleibt nur eine Falte, ist sie
nach Regel 7 die Bestätigungsperiode — es wird nichts selektiert. Die Lage
ist also **schlechter als angenommen**, nicht besser. Beide Rechnungen sind
mit einem Schalter nachvollziehbar (`faltenplan.py --mindesttraining 2`).

Die Nachher-Zahlen hängen **nicht am genauen Listing-Tag**: für jeden Tag
zwischen dem 2017-07-01 und dem 2017-12-31 ist das erste zulässige Faltenjahr
**2022**. Erst ein Listing vor dem 2017-01-01 verschöbe sie — Binance gibt es
seit Juli 2017.

---

## Welche Symbole haben eine kürzere Historie — und wie groß ist die Verzerrung?

Kürzere Historie haben die **11** oben genannten Symbole. Die Verzerrung
entsteht aber nicht durch sie allein, sondern durch den point-in-time-Satz der
Faltenregel: *„Ein Symbol geht in eine Falte nur ein, wenn seine Kursdaten
mindestens vier Jahre vor Faltenbeginn einsetzen."*

| Selektionsfalte | Symbole in der Falte |
|---|---|
| 2022 | **3** von 24 |
| 2023 | 6 von 24 |
| 2024 | 9 von 24 |
| 2025 | 13 von 24 |

Zwei Sätze, auf die es ankommt:

1. **Die früheste Selektionsfalte wird von drei Coins entschieden** —
   `BTCUSDT`, `ETHUSDT`, `BNBUSDT`. Nicht von 25, nicht von 24.
2. **11 von 24 Symbolen kommen in KEINER Selektionsfalte vor**, auch nach dem
   Laden nicht. Das früheste unter ihnen (`PROMUSDT`) wäre erst ab einer Falte
   2028 zulässig.

Die Parameter werden also auf den Paaren ausgewählt, die lange genug gelistet
sind und den Zyklus 2018 sowie den Bärenmarkt 2022 überlebt haben; gehandelt
wird anschließend ein Universum, das **zur Hälfte aus Paaren besteht, die in
der Auswahl nie vorkamen**. Das ist die survivorship-nahe Verzerrung in
Zahlen. **Mehr Historie macht sie nicht kleiner — sie macht sie messbar.**
Glätten lässt sich das nicht; `faltenplan.py` weist es bei jedem Lauf aus.

*(Die Zahlen der Spalte „Symbole in der Falte" für 2022–2025 beruhen auf
angenommenen Listing-Daten für die 13 beschnittenen Symbole — siehe
`research/krypto_historie/daten/annahme_listing.json`. Die Aussage „11 von 24
in keiner Falte" ist dagegen **gemessen**; sie hängt nur an den elf
Dateibeginn-Daten, die das Fenster nicht beschnitten hat.)*

---

## Der Befund, der vor dem Laden geklärt sein muss

> **Der überlappende Bereich stimmt bei den `*_1d.csv` nicht überein — und das
> ist ein Fehler des Altbestands, nicht des Endpunkts.**

Alle **24** Krypto-Tagesdateien sind **abgeleitet**, nicht abgerufen:
`shared/build_daily_crypto_data.py` hat sie aus den 1h-Daten resampelt. Das
ist gemessen — bei allen 24 ist der Eröffnungskurs der ersten Tageskerze auf
die letzte Stelle identisch mit dem der ersten Stundenkerze. Daraus folgen
drei Teilkerzen, die in den Dateien wie normale Kerzen aussehen:

| Was | Wieviele | Ausmaß |
|---|---|---|
| **erste** Tageskerze | 24 von 24 | **6 bis 16** statt 24 Stunden (bei den 13 langen Historien: 2021-09-01 mit **11** Stunden) |
| **letzte** Tageskerze | 24 von 24 | am 2026-08-31 **13** statt 24 Stunden |
| **letzte** 4h-Kerze | 23 von 24 | enthält Kursbewegung, die in der 1h-Datei fehlt |

`shared/kursdaten.py` findet das **nicht**: es prüft auf *fehlende* Kurse, und
eine Teilkerze hat vier gefüllte Kursspalten. Sie ist nicht leer, sie ist
falsch.

**Warum das gerade jetzt zählt:** Solange die Datei dort beginnt, sitzt die
Teilkerze am **Rand**. Sobald Historie davorgesetzt wird, sitzt sie **mitten**
in der Reihe — ein stillschweigender 11-Stunden-Tag zwischen lauter
24-Stunden-Tagen, mitten im Trainingsbereich der Neuselektion.

**Der Lader schreibt deshalb in der Voreinstellung nicht**, sondern meldet die
Abweichung und nennt den Schalter. `--teilkerze-ersetzen` ersetzt **genau
diese eine Zeile** durch die native Tageskerze — ausdrücklich, gezählt,
berichtet.

Für die **11 spät gelisteten** Symbole ist die erste Tageskerze zwar ebenfalls
angeschnitten, aber **richtig** angeschnitten: ihr Listing-Tag hat auch nativ
keine 24 Stunden Handel. Dort sollte der Vergleich aufgehen. Entschieden wird
das nicht vorab, sondern beim Lauf gegen den echten Endpunkt — je Datei.

---

## Was geliefert ist

| Datei | Was |
|---|---|
| `shared/binance_historie.py` | der Lader: messen, laden, Zeile für Zeile vergleichen, verlängern |
| `shared/test_binance_historie.py` | **75/75**, davon drei zweistufige Mutationsproben |
| `research/krypto_historie/faltenplan.py` | rechnet die Faltenregel aus Registerabschnitt 5.3 nach |
| `research/krypto_historie/test_faltenplan.py` | **38/38**, davon zwei zweistufige Mutationsproben |
| `research/krypto_historie/probelauf.py` | der Lader gegen die **echten** Repo-Dateien, **453/453** |
| `research/krypto_historie/BERICHT.md` | die Untersuchung |
| `research/krypto_historie/daten/` | Teilkerzen-Messung, Listing-Annahmen, eingefrorene Kennzahlen |
| `docs/TESTAUFTRAG_TB-31_krypto_historie.md` | autonom ausführbar, Schritte 1–9 überall, 10–14 auf dem Mac |
| `docs/ERGEBNIS_TB-31_krypto_historie.md` | kurzes Ergebnisdokument zum Kopieren |

**Der Lader benutzt ausschließlich `https://api.binance.com/api/v3/klines`** —
öffentlich, ohne Schlüssel, kein `/sapi/`, kein `/fapi/`. Das gitignorierte
`shared/fetch_binance_data.py` (enthält Zugangsdaten) wird **nicht**
eingebunden; der Selbsttest prüft, dass keine Anfrage `signature`, `apiKey`
oder `timestamp` mitträgt.

**Ratenbegrenzung:** Mindestpause 0,25 s (≙ 480 Gewicht/min bei einem Budget
von 6000, `/api/v3/klines` wiegt 2), Auswertung des Kopffelds
`x-mbx-used-weight-1m` mit Pause ab 70 % des Budgets, `429` mit `Retry-After`
abwarten und wiederholen, `418` **abbrechen** statt weiterprobieren.

**Wiederholbarkeit:** Beginnt eine Datei bereits am gemessenen Datenbeginn,
wird **gar nicht geschrieben**. Ein zweiter Lauf lässt sie byte-identisch —
im Probelauf über alle 24 Symbole und drei Zeitrahmen geprüft.

---

## Was nicht geliefert ist, und warum

**Der Ladelauf selbst.** `api.binance.com` ist aus dieser Umgebung gesperrt;
das ist eine Richtlinienentscheidung und wird nicht umgangen. Der Lauf ist
Schritt 12 des Testauftrags, Dauer rund 10–15 Minuten.

**Die Nachher-Kennzahlen je Bot.** Sie brauchen die geladenen Daten. Geliefert
ist stattdessen der **eingefrorene Vorher-Stand** aller neun Bots
(`daten/kennzahlen_vorher.json`, Tabelle in `BERICHT.md` Abschnitt 6) und in
Schritt 13 ein Befehl, der die Vorher/Nachher-Tabelle daraus erzeugt.

**Die überprüfbare Vorhersage dazu:** `shared/ergebniskurven.py` meldet heute
**9× AKTUELL**. Nach dem Laden muss es **5× ABWEICHEND** (die Krypto-Bots) und
**4× AKTUELL** (die Aktien-Bots) melden. Meldet ein Aktien-Bot ABWEICHEND, hat
der Lauf etwas angefasst, was er nicht durfte.

> **Die Kurven bitte NICHT neu erzeugen.** `ABWEICHEND` ist nach dem Laden
> richtig. Ob und wann neu gerechnet wird, entscheidet der Betreiber, und es
> gehört in denselben Schritt wie die Neuselektion.

---

## Randnotizen

* **Zum Hinweis im Auftrag,** die Ergebniskurven auf `main` seien veraltet,
  weil ein lokaler Commit `94b2e3c` nicht gepusht sei: auf dem Stand
  `9afac63`, auf dem diese Arbeit aufsetzt, melden sie **9× AKTUELL**. Der
  Commit „Ergebniskurven nach der Zuteilungskaskade (TB-26) neu erzeugt" ist
  auf `main`. Es war nichts nachzuziehen, und es wurde nichts nachgezogen.
* **Eine Mutationsprobe hat beim Schreiben selbst einen Fehler gefunden:** sie
  prüfte zunächst auf die Zeichenfolge `nan` in der Kursdatei und blieb grün,
  obwohl die Wache abgeschaltet war — `pandas.to_csv` schreibt ein fehlendes
  Feld als **leeres** Feld (`2026-09-01,,,,,1234.0`), genau die Form des
  APH-Falls, der `shared/kursdaten.py` ausgelöst hat. Die Probe prüft jetzt
  auf leere Kursspalten und hält zusätzlich fest, dass `nan` dort **nicht**
  steht.

---

## Offene Punkte — Entscheidungen des Betreibers

1. **Der Krypto-Faltenplan gehört ins Register**, sobald Schritt 10 gelaufen
   ist. Mit hinein gehört die **Lesart von „je Symbol"**: die Regel lässt
   offen, ob ein oder alle Symbole die vier Jahre erfüllen müssen. Bei „alle"
   schöbe `UUSDT` (2026-01-13) die erste Falte auf **2031** — es gäbe nie eine
   Selektion. Gerechnet wurde deshalb mit „mindestens ein Symbol", zusammen
   mit dem point-in-time-Filter; die Festlegung steht im Modulkopf von
   `faltenplan.py` und ist bisher **nicht** registriert.
2. **`elliott_wave` bleibt bei zwei Selektionsfalten** — wegen seiner
   Faltenlänge von zwei Jahren (26,0 gefundene Trades je Jahr, unter der
   30er-Schwelle), nicht wegen der Daten. Ein Median über zwei Falten ist
   dasselbe Problem wie vorher, nur eine Etage höher.
3. **11 von 24 Symbolen kommen in keiner Selektionsfalte vor.** Dürfen
   Selektions- und Handelsuniversum auseinanderfallen?
4. **Die Tagesdateien sind nach dem Laden vorn nativ und hinten abgeleitet.**
   `strategies/rsi2_crypto/fetch_1d_data.py` und
   `strategies/volatility_breakout_crypto/fetch_1d_data.py` sind die nativen
   Abrufwege. Ob sie den täglichen Cronjob-Pfad ersetzen sollen, ist eine
   getrennte Frage und hier bewusst **nicht** angefasst.

**Es wurde kein Raster gerechnet, kein Parameter übernommen und keine
Kursdatei verändert.**
