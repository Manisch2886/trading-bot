# TB-31 — Krypto-Historie: Ergebnis

**Datenaufgabe. Kein Bot-Code, keine Parametrisierung, keine Kursdatei
verändert.** Der Binance-Endpunkt ist aus der Cloud gesperrt (403 der
Egress-Richtlinie); geliefert sind das geprüfte Ladeskript und die Messungen,
die ohne Endpunkt möglich waren. Der Ladelauf ist Schritt 12 des Testauftrags.

---

## Die zwei Zahlen

**1. Ab wann reicht die Historie je Symbol zurück?**

| | Anzahl | Beginn | gemessen? |
|---|---|---|---|
| vom 1825-Tage-Fenster **beschnitten** | **13** | alle am 2021-09-01 | **nein** — Messung steht aus (Schritt 10) |
| **nicht** beschnitten | **11** | 2023-03-17 bis 2026-01-13 | **ja** |

Der gemeinsame Beginn 2021-09-01 ist **kein Listing-Datum**, sondern der Rand
des Fensters `LOOKBACK = "1825 day ago UTC"` in `shared/fetch_multi_data.py`
und `strategies/t3_supertrend/fetch_4h_data.py`.

**2. Wie viele Testfalten sind je Krypto-Bot möglich?**

| Bot | Faltenlänge | heute | nach dem Laden |
|---|---|---|---|
| `elliott_wave` | 2 J | **0** | **2** (2022-2023, 2024-2025) |
| `t3_supertrend` | 1 J | **0** | **4** (2022 … 2025) |
| `rsi2_crypto` | 1 J | **0** | **4** |
| `turtle_soup_crypto` | 1 J | **0** | **4** |
| `volatility_breakout_crypto` | 1 J | **0** | **4** |

Gerechnet nach der Regel des Registers (Abschnitt 5.3): Mindesttraining
**4 Jahre**, früheste Falte 2019, Go-Live-Schnitt 2026-09-01, letzte Falte
ist die Bestätigungsperiode.

---

## Drei Dinge, die anders sind als im Auftrag angenommen

**1. Heute sind es null Testfalten, nicht zwei.** Die „zwei Falten (2024,
2025)" ergeben sich bei **zwei** Jahren Mindesttraining; das Register legt
**vier** fest. Bleibt nur eine Falte, ist sie nach Regel 7 die
Bestätigungsperiode — es wird nichts selektiert. Beide Rechnungen sind
nachvollziehbar (`faltenplan.py`, mit und ohne `--mindesttraining 2`).

**2. Der überlappende Bereich stimmt bei den Tagesdateien nicht — und das ist
ein Befund über den Altbestand.** Alle **24** `*_1d.csv` sind aus den 1h-Daten
abgeleitet, nicht abgerufen (gemessen: der Eröffnungskurs der ersten
Tageskerze ist bei allen 24 auf die letzte Stelle identisch mit dem der ersten
Stundenkerze). Daraus folgen Teilkerzen, die wie normale Kerzen aussehen:

* die **erste** Tageskerze jeder Datei deckt **6 bis 16** statt 24 Stunden ab
  (bei den 13 langen Historien: der 2021-09-01 mit **11** Stunden),
* die **letzte** deckt am 2026-08-31 **13** Stunden ab,
* bei **23 von 24** Symbolen enthält die letzte 4h-Kerze Kursbewegung, die in
  der 1h-Datei fehlt — die beiden Dateien enden zu **verschiedenen realen
  Zeitpunkten**.

`shared/kursdaten.py` findet das nicht: es prüft auf **fehlende** Kurse, und
eine Teilkerze hat vier gefüllte Kursspalten. Sie ist nicht leer, sie ist
falsch. Solange die Datei dort beginnt, sitzt die Teilkerze am Rand; wird
Historie davorgesetzt, sitzt sie **mitten im Trainingsbereich**.

**3. `elliott_wave` bleibt auch nach dem Laden bei zwei Selektionsfalten** —
nicht wegen der Daten, sondern wegen seiner Faltenlänge von zwei Jahren
(26,0 gefundene Trades je Jahr, unter der 30er-Schwelle des Registers).

---

## Die Verzerrung, gemessen

| Selektionsfalte | Symbole in der Falte |
|---|---|
| 2022 | **3** von 24 |
| 2023 | 6 von 24 |
| 2024 | 9 von 24 |
| 2025 | 13 von 24 |

* **Die früheste Selektionsfalte wird von drei Coins entschieden** —
  `BTCUSDT`, `ETHUSDT`, `BNBUSDT`.
* **11 von 24 Symbolen kommen in KEINER Selektionsfalte vor**, auch nach dem
  Laden nicht: `PROMUSDT`, `SUIUSDT`, `PEPEUSDT`, `WLDUSDT`, `ENAUSDT`,
  `TRUMPUSDT`, `BMTUSDT`, `PUMPUSDT`, `ZKCUSDT`, `ENSOUSDT`, `UUSDT`. Das
  früheste unter ihnen wäre erst ab einer Falte 2028 zulässig.

Ausgewählt wird also auf den Paaren, die lange genug gelistet sind und den
Zyklus 2018 sowie den Bärenmarkt 2022 überlebt haben; gehandelt wird
anschließend ein Universum, das zur Hälfte aus Paaren besteht, die in der
Auswahl nie vorkamen. **Mehr Historie macht diese Verzerrung nicht kleiner —
sie macht sie messbar.**

---

## Marktphasen

| Phase | heute | nach dem Laden |
|---|---|---|
| Zyklus 2018 | fehlt | vorhanden (nur BTC, ETH, BNB) |
| Einbruch März 2020 | fehlt | vorhanden |
| Bärenmarkt 2022 | vorhanden | vorhanden |

Beide neu hinzukommenden Phasen liegen im **Trainings**bereich, nicht in einer
Testfalte — die erste Testfalte ist 2022.

---

## Der Lader

`shared/binance_historie.py`, ausschließlich
`https://api.binance.com/api/v3/klines`, öffentlich, **ohne Schlüssel** (kein
`/sapi/`, kein `/fapi/`, kein Einbinden des gitignorierten
`fetch_binance_data.py`).

* **Ratenbegrenzung:** Mindestpause 0,25 s (≙ 480 Gewicht/min bei einem
  Budget von 6000), Auswertung des Kopffelds `x-mbx-used-weight-1m` mit Pause
  ab 70 % des Budgets, `429` mit `Retry-After` abwarten und wiederholen,
  `418` **abbrechen**.
* **Verlängern statt überschreiben:** vorhandene Zeilen werden als Rohtext
  gelesen und **zeichengleich** zurückgeschrieben; nur davor kommt etwas dazu.
* **Überlappungsbeweis:** geladen wird vom gemessenen Datenbeginn bis zur
  letzten vorhandenen Kerze, verglichen wird **Zeile für Zeile**. Eine
  Kursabweichung verhindert das Schreiben.
* **Teilkerzen-Sonderfall:** in der Voreinstellung wird **nicht** geschrieben;
  `--teilkerze-ersetzen` ersetzt **genau die eine** führende Zeile.
* **`shared/kursdaten.py`** streicht und zählt unvollständige Kerzen im
  vorangestellten Teil.
* **Wiederholbar:** beginnt die Datei bereits am Datenbeginn, wird gar nicht
  geschrieben. Zweiter Lauf: byte-identisch.

---

## Geprüft

| | |
|---|---|
| `shared/test_binance_historie.py` | **75/75** |
| `research/krypto_historie/test_faltenplan.py` | **38/38** |
| `research/krypto_historie/probelauf.py --alle` (24 Symbole × 3 Zeitrahmen, echte Repo-Dateien) | **453/453** |
| `shared/determinismus.py --schnell` | **9× DETERMINISTISCH** |
| `shared/kursdaten.py` | unverändert **ein** Befund (`APH_1d.csv`) |
| `shared/ergebniskurven.py` | unverändert **9× AKTUELL** |
| alle bestehenden Tests | unverändert (vorbestehende Fehlschläge mit Basislauf belegt) |

Der Faltenplan-Rechner reproduziert den von Hand geschriebenen
**Aktien**-Faltenplan des Registers — und liest ihn dafür aus der
Registerdatei, nicht aus einer Kopie im Test.

Der Probelauf läuft gegen die **echten** Kursdateien dieses Repos: im
überlappenden Bereich liefert die nachgebildete Gegenstelle Zeile für Zeile
das, was in `data/` steht. Erzeugt ist nur die Vorgeschichte davor. Belegt ist
damit der **Ablauf**, nicht der Kursinhalt.

---

## Nach dem Ladelauf: die überprüfbare Vorhersage

`shared/ergebniskurven.py` meldet heute **9× AKTUELL**. Nach dem Laden muss es
**5× ABWEICHEND** (die Krypto-Bots) und **4× AKTUELL** (die Aktien-Bots)
melden. Meldet ein Aktien-Bot ABWEICHEND, hat der Lauf etwas angefasst, was er
nicht durfte.

> **Die Kurven bitte NICHT neu erzeugen.** `ABWEICHEND` ist dann richtig. Ob
> und wann, entscheidet der Betreiber — und es gehört in denselben Schritt wie
> die Neuselektion.

Der eingefrorene Vergleichsstand (alle neun Bots, Zeitraum, Trades,
Endkapital, Rendite, MaxDD) liegt als
`research/krypto_historie/daten/kennzahlen_vorher.json`; die Tabelle steht in
`research/krypto_historie/BERICHT.md` Abschnitt 6.

---

## Offen — Entscheidungen des Betreibers

1. **Der Krypto-Faltenplan gehört ins Register.** Abschnitt 5.3 enthält noch
   die Platzhalter. Mit hinein gehört die **Lesart von „je Symbol"**: die
   Regel lässt offen, ob ein oder alle Symbole die vier Jahre erfüllen müssen.
   Bei „alle" schöbe `UUSDT` (2026-01-13) die erste Falte auf 2031 — gerechnet
   wurde deshalb mit „mindestens ein Symbol", zusammen mit dem
   point-in-time-Filter.
2. **Zwei Selektionsfalten für `elliott_wave`** — genügt das, oder soll die
   Faltenlänge neu bedacht werden?
3. **11 von 24 Symbolen in keiner Selektionsfalte** — dürfen Selektions- und
   Handelsuniversum auseinanderfallen?
4. **Die Tagesdateien sind nach dem Laden vorn nativ und hinten abgeleitet.**
   Ob der tägliche Cronjob-Pfad auf die nativen `fetch_1d_data.py` umgestellt
   wird, ist eine getrennte Frage — hier bewusst nicht angefasst.
