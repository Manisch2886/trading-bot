# TB-24 — Haltedauern und Zeithorizonte: Ergebnis

**Kurzfassung zum Kopieren.** Vollständiger Bericht:
`research/tb24_haltedauern/BERICHT.md`. Übergabe:
`docs/UEBERGABE_TB24_haltedauern.md`.

**Untersuchung, keine Änderung.** Kein Produktivcode, keine Parametrisierung,
keine umgesetzte Empfehlung. Geändert wurden nur Dateien unter
`research/tb24_haltedauern/` und `docs/`.

---

## Das Ergebnis in vier Sätzen

Die Vermutung trifft **auf die Zahl genau zu**: **genau sechs der neun Bots**
haben Median-Haltedauern zwischen drei und zehn Kalendertagen, und zwar in
einem noch engeren Band als vermutet — **3,9 bis 7,0 Tage**. Die Mediane aller
neun liegen zwischen **2,67 und 21,0 Tagen**, das ganze Portfolio spielt also
innerhalb von drei Wochen; über 30 Tage ist es leer. Der Grund ist keine
Markteigenschaft, sondern eine **Parametereinstellung**: sieben von neun Bots
haben eine Zeitbremse von 10 bis 15 Tagen bzw. Handelstagen, und bei jedem Bot
liegt der Median seiner Zeitausstiege exakt darauf. **Aber:** der Horizont ist nicht die
Dimension, an der gemeinsames Verhalten hängt — das ist die Ertragsquelle, und
das ist gemessen, nicht vermutet.

---

## 1. Haltedauern je Bot (Kalendertage, ausgeführte Positionen)

| Bot | Zeitrahmen | n | P10 | Q1 | **Median** | Q3 | P90 | Horizont-Klasse |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `t3_supertrend` | 4 h | 656 | 0,50 | 1,00 | **2,67** | 6,0 | 9,5 | bis 2 Tage |
| `elliott_wave` | 1 h | 130 | 0,21 | 0,68 | **3,90** | 10,0 | 10,0 | **3 bis 10 Tage** |
| `rsi2_crypto` | 1 d | 392 | 1,00 | 2,00 | **4,00** | 5,0 | 7,0 | **3 bis 10 Tage** |
| `turtle_soup_crypto` | 1 d | 1.414 | 1,00 | 1,00 | **4,00** | 10,0 | 10,0 | **3 bis 10 Tage** |
| `rsi2_mean_reversion` | 1 d | 4.232 | 2,00 | 3,00 | **5,00** | 7,0 | 11,0 | **3 bis 10 Tage** |
| `volatility_breakout_crypto` | 1 d | 207 | 1,00 | 2,00 | **6,00** | 15,0 | 15,0 | **3 bis 10 Tage** |
| `elliott_wave_stocks` | 1 d | 395 | 1,00 | 2,00 | **7,00** | 47,5 | 131,0 | **3 bis 10 Tage** |
| `turtle_soup_stocks` | 1 d | 8.915 | 14,00 | 14,00 | **14,00** | 15,0 | 15,0 | 11 bis 30 Tage |
| `volatility_breakout` | 1 d | 1.454 | 12,00 | 21,00 | **21,00** | 22,0 | 23,0 | 11 bis 30 Tage |

Die Klassengrenzen sind **vorab** festgelegt; „3 bis 10 Tage" stammt wörtlich
aus der zu prüfenden Vermutung.

## 2. Wie viele Zeitfenster? Drei besetzte, eines trägt zwei Drittel

| Horizont-Klasse | Bots | Ertragsquellen darin |
|---|---:|---|
| bis 2 Tage | 1 | Trend |
| **3 bis 10 Tage** | **6** | Muster, Trend, Umkehr (gemischt) |
| 11 bis 30 Tage | 2 | Umkehr, Trend |
| 31 bis 90 Tage | **0** | — |
| über 90 Tage | **0** | — |

Es sind nicht einmal drei getrennte Fenster: die Mediane lauten 2,67 / 3,90 /
4,00 / 4,00 / 5,00 / 6,00 / 7,00 / 14,0 / 21,0 Tage. Zwischen dem ersten und
dem siebten liegen **4,3 Tage**; bei einer Klassengrenze von 2 statt 3 Tagen
wären es **sieben von neun** in einem Fenster.

## 3. Die Verteilungsform: acht von neun sind zweigipflig

Die Trennlinie ist die Ausstiegsart, nicht der Markt — und bei jedem Bot mit
Zeitbremse liegt der spätere Gipfel **exakt darauf**:

| Bot | früher Gipfel | Anteil | späterer Gipfel (= Zeitbremse, wo es eine gibt) | Anteil |
|---|---:|---:|---:|---:|
| `elliott_wave` | 0,88 T Stop | 53,8 % | 10,0 T (240 Stundenbalken) | 33,8 % |
| `t3_supertrend` | 1,17 T Stop | 53,0 % | 5,33 T Trendwechsel (keine Bremse) | 30,8 % |
| `rsi2_crypto` | 4,00 T SMA-Exit | 98,0 % | 10,0 T (`MAX_HOLD_DAYS = 10`) | 2,0 % |
| `turtle_soup_crypto` | 2,00 T Stop | 69,0 % | 10,0 T (`= 10`) | 31,0 % |
| `volatility_breakout_crypto` | 3,00 T Stop | 71,0 % | 15,0 T (`= 15`) | 29,0 % |
| `elliott_wave_stocks` | 5,00 T Stop | 79,2 % | **131,0 T** (90 Tagesbalken) | 20,8 % |
| `rsi2_mean_reversion` | 5,00 T SMA-Exit | 96,8 % | 14,0 T (`= 10` Handelstage) | 3,2 % |
| `turtle_soup_stocks` | — (kein Stop) | — | 14,0 T (`= 10` Handelstage) | **100,0 %** |
| `volatility_breakout` | 12,00 T Stop | 19,8 % | 22,0 T (`= 15` Handelstage) | 80,2 % |

Der Median eines Bots ist damit im Wesentlichen die Antwort auf eine Frage:
*wie oft feuert der Stop, bevor die Uhr abläuft?*

## 4. Die Überlappung — und was sie erklärt

**Tages-Überlappung** (Anteil der Positionstage von A, an denen auch B hält):
Median über alle 72 geordneten Paare **89,5 %**, Spalte `turtle_soup_stocks`
durchgehend **100 %** (dieser Bot hält an allen 3.653 Tagen). Die Zahl misst
vor allem, wie oft ein Bot im Markt ist — sie ist Nenner, nicht Befund.

**Titel-Überlappung** (Anteil der (Titel, Tag)-Paare von A, die auch B hält),
stärkste Paare:

| A → B | Anteil |
|---|---:|
| `rsi2_mean_reversion` → `turtle_soup_stocks` | **48,6 %** |
| `rsi2_crypto` → `turtle_soup_crypto` | 39,3 % |
| `elliott_wave` → `turtle_soup_crypto` | 25,5 % |
| `elliott_wave_stocks` → `turtle_soup_stocks` | 24,9 % |
| `volatility_breakout_crypto` → `t3_supertrend` | 21,7 % |

**Gemeinsame Einstiege im selben Titel innerhalb von drei Tagen**, gemessen
gegen den Zufallswert (Einstiegstage von B je Symbol zufällig neu gelegt, 200
Ziehungen; zusätzlich in geschlossener Form nachgerechnet — beide stimmen in
allen 32 Paaren auf 0,1 Prozentpunkte überein):

| Quellen-Paar | Paare | Median-Überschuss gegen Zufall | Spanne |
|---|---:|---:|---|
| Umkehr + Umkehr | 4 | **2,58 ×** | 1,89 – 3,27 |
| Trend + Trend | 2 | **1,71 ×** | 1,68 – 1,74 |
| Muster + Umkehr | 8 | 1,43 × | 0,00 – 2,19 |
| **Trend + Umkehr** | 12 | **0,32 ×** | 0,15 – 0,93 |
| **Muster + Trend** | 6 | **0,18 ×** | 0,00 – 1,78 |

| Trennt der Horizont? | Median-Überschuss |
|---|---:|
| **gleiche** Ertragsquelle (6 Paare) | **1,94 ×** |
| verschiedene Ertragsquelle (26 Paare) | 0,32 × |
| **gleiche** Horizont-Klasse (16 Paare) | **0,32 ×** |
| verschiedene Horizont-Klasse (16 Paare) | 1,10 × |

**Alle sechs Paare gleicher Quelle liegen über 1,68 ×, alle zwölf
Trend-Umkehr-Paare unter 0,95 ×.** Die Ertragsquelle erklärt gemeinsames
Verhalten, der Horizont nicht.

## 5. Der auffälligste Einzelfall: gleichzeitig ist nicht dasselbe wie abhängig

`elliott_wave_stocks` und `rsi2_mean_reversion` steigen in **0 von 395** Fällen
innerhalb von drei Tagen gemeinsam ein, obwohl sie 127 Titel teilen und der
Zufall etwa 20 Treffer erwarten liesse. Der Grund ist ein **systematischer
Versatz**: der nächstgelegene RSI-2-Einstieg liegt im Median **14 Tage vor**
dem Elliott-Einstieg, und die Klassen von −3 bis +3 Tagen sind **leer**.

| Versatz (Tage, negativ = RSI-2 zuerst) | < −30 | −30…−20 | −20…−10 | −10…−3 | **−3…+3** | +3…+10 | +10…+20 | +20…+30 | ≥ +30 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Anzahl (von 395) | 213 | 21 | 36 | 15 | **0** | 1 | 3 | 7 | 99 |

Die beiden handeln denselben Kursrückgang — nur nacheinander. Ein
Drei-Tage-Fenster allein hätte das Paar als unabhängig eingeordnet.

## 6. Wo wäre eine Lücke?

* **Über 30 Tage ist das Portfolio leer.** Keine der neun Mediane liegt über
  21 Tagen.
* **B1 / ETF-Trend (monatlich)** läge ausserhalb aller neun Mediane — eine
  echte **Horizont**ergänzung.
* **K1 (Wochenfrist)** ist zweideutig: heisst es *Haltedauer* eine Woche,
  landet K1 **mitten im gedrängten Fenster** und ist keine
  Horizontergänzung; heisst es *wöchentlicher Entscheidungstakt* mit
  mehrwöchiger Haltedauer, liegt es bei
  `turtle_soup_stocks`/`volatility_breakout`. Der Strategie-Katalog liegt nicht
  im Repo; aus dem Repo ist das nicht zu klären.

## 7. Belastbarkeit in Zahlen

| | |
|---|---|
| Datenbasis | **17.795 ausgeführte Positionen** aus 25.861 gefundenen Trades, 9 Bots, 2016-09-01 bis 2026-09-01 |
| Quelle | Backtest-Trades über die **Original-Bot-Funktionen** und die heutigen `live_params.py` |
| Live-Seite | **nicht gemessen** — die neun `paper_trading_*.db` sind gitignored und in der Cloud nicht vorhanden; ausserdem erreicht kein Bot `MIN_LIVE_CLOSED_TRADES = 10`. `live_haltedauern.py` liegt lauffähig bereit |
| Pflicht-Gegencheck | für **alle neun** Bots stimmt der Positionssatz Zeile für Zeile mit `research/exposure_messung/daten/` überein |
| Gegenprobe Positionslimit | Median über **alle** Trades statt nur der ausgeführten: Abweichung **0,00 Tage** bei acht Bots, 0,25 bei `t3_supertrend`; keine Klassenzuordnung ändert sich |
| Selbsttests | **51 von 51** — 35 Gegenproben, 5 zum Live-Weg gegen eine gebaute Datenbank, **10 Mutationsproben** (alle erkannt), 1 Repo-Wache |

**Der Vorbehalt zur Grundlage:** Die Backtest-Trades entstehen aus Parametern,
die nach einem inzwischen als unbrauchbar erkannten Mass gewählt wurden. Für
Haltedauern wirkt das wenig — sie hängen an den Ausstiegsregeln, und die
Gipfel liegen auf den Zeitbremsen. Eine andere Parameterwahl würde die
**Stop-Quote** verschieben und den Median zwischen den beiden Gipfeln wandern
lassen, die Gipfel selbst aber nicht.

## 8. Was NICHT beantwortet ist

Ob die Strategien gut sind · wie hoch die Ergebniskorrelation ist (das steht in
`research/exposure_messung/`) · ob die Ertragsquellen-Einteilung stimmt (sie ist
eine offen hingeschriebene **Lesart**, und die Befunde aus Abschnitt 4 hängen
daran) · wie belastbar der Quellen-Befund ist (die Gruppe „gleiche Quelle"
besteht aus **drei** ungeordneten Paaren) · die Live-Seite · warum der Versatz
auftritt.

**Keine Empfehlung ist umgesetzt.** Was aus den Zahlen folgt, entscheidet der
Nutzer.
