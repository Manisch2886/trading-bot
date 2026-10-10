# REGISTER-KOPIE Abschnitt 15 (von 0–56) — Register-Z. 1369–1825 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 15. Registernachtrag (TB-36, 15.09.2026)

### 15.0 Was das ist — und was es ausdrücklich nicht ist

**Das ist kein Amendment.** Es hat **kein Selektionslauf stattgefunden**, dessen
Ergebnisse davon berührt wären: kein Raster gerechnet, kein Parametersatz
bewertet, kein Ergebnis erzeugt — derselbe Stand wie am Kopf dieses Dokuments.
Die Sperrliste (Abschnitt 10) gilt laut ihrem eigenen ersten Satz **„ab dem
signierten Tag"**, und der steht in Abschnitt 13 weiterhin als *offen —
Betreiber*. Es ist deshalb nichts aufzubrechen; es wird nachgetragen, bevor
gerechnet wird. Genau deshalb kommt diese Arbeit **vor** TB-30b.

Vier Stellen der Vorregistrierung hatten sich als unvollständig oder
widersprüchlich erwiesen. Sie sind in zwei Runden mit dem Beratungsmodell
(15.09.2026) geklärt; dieser Abschnitt trägt die Klärung ein und rechnet die
Zahlen, die dafür feststehen müssen.

**Bestehender Text wird nicht umgeschrieben.** Die betroffenen Passagen
(Abschnitt 3 „Der Faltenplan", 5.1 Nr. 1/2/3/5, 5.3, Sperrliste Nr. 8) bleiben
stehen und tragen nur einen Verweis hierher. Der Verlauf soll lesbar bleiben —
das ist der Sinn eines Registers.

**Herkunft der Zahlen.** Alle Zahlen dieses Nachtrags stammen aus
`research/faltenplan_neun/` (rein lesend, reine Standardbibliothek; Bot-Dateien
werden gelesen, nie importiert):

| | |
|---|---|
| Faltenplan und Symbolzahlen | `research/faltenplan_neun/faltenplan_neun.py` → `daten/faltenplan.json` |
| Embargo je Bot | `research/faltenplan_neun/embargo_neun.py` → `daten/embargo.json` |
| Selbsttest, einschliesslich Gegenprobe gegen TB-31 | `research/faltenplan_neun/test_faltenplan_neun.py` |
| Datenstand | `d9449faf51bffaaa…`, 223 Kursdateien — unverändert |

---

### 15.1 Die Vorabklärung: es gilt Verfahren B

Die bisherige Festlegung enthielt **zwei sich ausschliessende Verfahren**
nebeneinander:

| | Verfahren A (Walk-Forward) | **Verfahren B (gilt)** |
|---|---|---|
| Auswahl | je Falte ein Gewinner | **einmalig über das ganze Raster** |
| N | vervielfacht sich | **N = Rastergrösse** |
| Out-of-Sample | die Testfalten | **allein die Bestätigungsperiode** |

**Es gilt Verfahren B.** Die Trainingsfenster-Sprache stammt aus A und ist
gestrichen. Daraus folgt dreierlei, und alle drei Folgen stehen unten in den
Registertexten: Es gibt **kein Mindesttraining**; die Selektionsfalten sind
**keine** OOS-Falten und brauchen untereinander keine Purge; die sechs
bot-eigenen Walk-Forward-Rechner werden später **ersetzt**, nicht umgestellt —
das ist TB-30b und **nicht** dieser Nachtrag.

---

### 15.2 Registertext 0 — Verfahren

> Die Selektion ist eine einmalige Auswahl über das vollständige Raster. Jeder
> Rasterpunkt wird auf jeder Selektionsfalte ausgewertet; Selektionsstatistik
> ist der Median der Falten-Sharpes; Gewinner nach Plateau-Regel. Es gibt kein
> Trainingsfenster und keine faltenweise Auswahl. Out-of-Sample ist allein die
> Bestätigungsperiode.

---

### 15.3 Registertext 1 — Bootstrap

> **(a)** Jedes Bootstrap-Intervall im Auswertungsskript wird auf der Reihe der
> täglichen Netto-Mark-to-Market-Renditen des Kapitalpfads gerechnet, nie auf
> Trade-Listen. Flache Tage stehen mit Rendite 0 in der Reihe.
>
> **(b)** Verfahren: stationärer Block-Bootstrap, 2 000 Ziehungen. Mittlere
> Blocklänge L = max(mediane Haltedauer des Parametersatzes in Handelstagen,
> ⌈T^(1/3)⌉), T = Länge der Reihe. **L wird berechnet und protokolliert; es ist
> kein Eingabewert.**
>
> **(c)** *[ersetzt die frühere Fassung mit Mindestzahl 10 Trades]* Der
> Falten-Sharpe wird für jeden Parametersatz in jeder Falte aus den täglichen
> Netto-Renditen des Kapitalpfads gerechnet, **unabhängig von der Anzahl
> Trades**. Ist die Standardabweichung 0 (kein Trade in der Falte), ist der
> Falten-Sharpe 0. **Es gibt keine Mindestzahl Trades je Falte.** Die Anzahl
> Trades je Falte wird für den Gewinner **berichtet, nicht bewertet.**

> ⭐ **15.3 (b) ERGÄNZT durch R41 (48.9)** (Fable 29b R41, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **15.3 (a) PRÄZISIERT durch R66 (53.1)** (Fable 02c R66, Unterpunkte (a) und (b), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **15.3 (c) PRÄZISIERT durch R66 (53.1)** (Fable 02c R66, Unterpunkt (c), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

*Formel für den Falten-Sharpe: Mittel / Standardabweichung der täglichen
Netto-Renditen der Falte × √252 (Krypto: √365 auf Kalendertagen).*

> **Tatsachennotiz zu 1c.** Eine Fassung „mit Mindestzahl 10 Trades" hat in
> **diesem** Dokument nie gestanden — sie stammt aus einer früheren
> Beratungsrunde und war nie eingetragen (geprüft über den gesamten Quelltext
> des Registers und `research/vorregistrierung/`). Der Klammerzusatz bleibt
> trotzdem wörtlich stehen: er sagt, gegen welche Fassung entschieden wurde.
> 1c ist damit kein Widerruf, sondern die **Schärfung von Regel 5.1 Nr. 8**
> („Falten ohne Trade zählen mit Sharpe 0"), die hier unberührt weitergilt.

> ⭐ **Folge für den Lauf (43.2, 43-7, Fable 25e, TB-110, 26.09.2026):** 1c
> und 5.1 Nr. 8 machen „keine Trades" zu einem **Wert**, der in die Statistik
> eingeht — nicht zu einem Grund, aufzuhören. Deshalb schreibt ein Lauf, der
> keine Trades findet, dieses Ergebnis und endet nie ohne Ausgabe (Wortlaut in
> **43.2, 43-7**). Registertext und Tatsachennotiz oben bleiben
> zeichengleich.

> ⭐ **15.3 ERGÄNZT durch R35 (48.3)** (Fable 29b R35, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

### 15.4 Registertext 2 — Faltenzuordnung

> **(a)** Selektionsfalten sind Kalenderjahre (bzw. Doppeljahre nach der
> bestehenden Regel). **Jeder Handelstag gehört zu der Falte, in die sein Datum
> fällt.** Die Falten-Rendite ist die Summe der täglichen
> Netto-Mark-to-Market-Renditen dieser Tage. Positionen, die eine Faltengrenze
> überschreiten, werden **nicht zugeordnet, geschlossen oder ausgeschlossen**.
>
> **(b)** Trades werden für die **Zählung** der Falte ihres **Einstiegstags**
> zugeordnet.
>
> **(c)** Zwischen Selektionsfalten gibt es weder Purge noch Embargo.
>
> **(d)** Die Bestätigungsperiode beginnt am Go-Live-Tag plus Embargo; Embargo =
> längste Zeitbremse des Bots in Handelstagen plus 1 (Bots ohne Zeitbremse: 95.
> Perzentil der Haltedauer plus 1). **Tage im Embargo gehören zu keiner
> Periode.**
>
> ⚠️ **ERSETZT durch Abschnitt 16 (Registernachtrag TB-41, 16.09.2026), 16.6.**
> Das Embargo ist dort keine feste Frist mehr, sondern eine Bedingung am
> Positionsbestand mit dieser Frist als Deckel. Die Embargo-Tabelle unten gilt
> als **obere Schranke** weiter.

> ⭐ **2a (15.4 (a)) BERICHTIGT durch R54 (49.2)** (Fable 30a R54, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Das Embargo je Bot** (Tatsachennotiz zu 2d, berechnet vor dem Lauf):

| Bot | Grundlage | Herkunft der Zahl | Handelstage | **Embargo** |
|---|---|---|---:|---:|
| `elliott_wave` | `MAX_HOLD_HOURS` = 240 (Stundenbalken) | `strategies/elliott_wave/backtest_elliott.py:70`, gleichlautend `forward_test.py:51` | 10 | **11** |
| `t3_supertrend` | **keine Zeitbremse** → P95 der Haltedauer = 11,21 Tage | `research/tb24_haltedauern/daten/t3_supertrend_positionen.csv` (656 Positionen) | 11,21 | **13** |
| `rsi2_crypto` | `MAX_HOLD_DAYS` = 10 (Tagesbalken) | `strategies/rsi2_crypto/live_params.py:34` | 10 | **11** |
| `turtle_soup_crypto` | `MAX_HOLD_DAYS` = 10 (Tagesbalken) | `strategies/turtle_soup_crypto/live_params.py:33` | 10 | **11** |
| `volatility_breakout_crypto` | `MAX_HOLD_DAYS` = 15 (Tagesbalken) | `strategies/volatility_breakout_crypto/live_params.py:43` | 15 | **16** |
| `elliott_wave_stocks` | `MAX_HOLD_HOURS` = 90 (Tagesbalken) | `strategies/elliott_wave_stocks/backtest_elliott.py:70` | 90 | **91** |
| `rsi2_mean_reversion` | `MAX_HOLD_DAYS` = 10 (Tagesbalken) | `strategies/rsi2_mean_reversion/live_params.py:21` | 10 | **11** |
| `turtle_soup_stocks` | `MAX_HOLD_DAYS` = 10 (Tagesbalken) | `strategies/turtle_soup_stocks/live_params.py:53` | 10 | **11** |
| `volatility_breakout` | `MAX_HOLD_DAYS` = 15 (Tagesbalken) | `strategies/volatility_breakout/live_params.py:25` | 15 | **16** |

Vier Anmerkungen, ohne die diese Tabelle nicht prüfbar wäre:

1. **„Handelstage" heisst bei Krypto Kalendertage** — der Markt läuft durch.
   Ein Tagesbalken ist dort ein Kalendertag, 240 Stundenbalken sind 10 Tage.
2. **Genau ein Bot hat keine Zeitbremse: `t3_supertrend`.** Das ist nicht
   geraten, sondern gemessen: TB-24 weist für ihn die Ausstiegsarten
   `stop_loss`, `trend_flip` und `t3_crossunder` aus — keine Uhr darunter —,
   und `research/tb24_haltedauern/BERICHT.md` Abschnitt 1 nennt ausdrücklich
   **acht** Bots mit Zeitausstieg.
3. **`elliott_wave_stocks` führt zwei Zeitbremsen**, und die Regel verlangt die
   längste: `MAX_HOLD_HOURS = 90` Tagesbalken im Backtest, `MAX_HOLD_DAYS = 130`
   **Kalendertage** im Live-Lauf. Die 130 Kalendertage sind an der Kursreihe
   nachgemessen **89 Handelstage** (Median über alle Startpunkte im
   Auswertungsfenster, Feiertage eingerechnet) — die 90 Balken sind also die
   längere der beiden. Der Kommentar im Bot („entspricht ~90 Handelstage")
   trifft damit auf einen Tag genau.
4. **Ein gebrochenes Perzentil wird aufgerundet**, bevor die 1 dazukommt: ein
   Embargo ist eine Zahl von Tagen, und abrunden machte den Rand kürzer, als
   die Messung ihn ausweist. Bei `t3_supertrend`: 11,21 → 12 → **13**.

> ⭐ **Der Deckel von `t3_supertrend` wird aus gefundenen Trades neu gerechnet
> (41.3 C2, Fable 24d, TB-108, 25.09.2026):** Die Zeile `t3_supertrend` oben
> stammt aus **ausgeführten** Positionen. Nach Fables Präzisierung zu 2d
> (Fassung 16.6) wird das 95. Perzentil der Haltedauer aus den **gefundenen**
> Trades gerechnet (Signalpfad), plus 1, aufgerundet nach Anmerkung 4; **kein**
> Maximum über das Raster. Neu gerechnet wird, wenn die neuen Listen vorliegen
> (42.6 (5)). Die Tabelle bleibt zeichengleich.

> ⭐ **15.4 ERGÄNZT durch R41 (48.9) und 50.1** (Fable 29b R41, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

### 15.5 Registertext 3 — Universum *(ersetzt die frühere Fassung vollständig)*

> **(a)** Das Universum je Bot ist **seine heutige Symbolliste** (Datei und Hash
> im Register). Je Selektionsfalte werden die Symbole dieser Liste ausgewertet,
> für die am 1. Januar der Falte Kursdaten einschliesslich Indikator-Vorlauf
> vorliegen. Symbole ohne Historie in einer Falte tragen 0 Trades und 0 Rendite
> bei.
>
> **(b)** Die **Symbolzahl je Falte** wird vor dem Lauf berechnet und als
> Tatsachennotiz eingetragen. Symbole, die in **keiner** Selektionsfalte
> vorkommen, werden namentlich vermerkt; der gewählte Parametersatz gilt für sie
> live **ohne Faltenevidenz**.
>
> **(c)** Vorbehalt, wörtlich: „Das Aktienuniversum ist nach heutiger
> Marktkapitalisierung, das Krypto-Universum nach heutigem Volumen gebildet.
> Beide sind survivorship-behaftet. **Erwartete Richtung: Bevorzugung von Sätzen
> mit weiten oder fehlenden Stops und langen Zeitbremsen**; Grösse unbekannt.
> Die Bestätigungsperiode unterliegt dieser Verzerrung nicht."
>
> ⭐ **(c) ERGÄNZT durch Abschnitt 26 (TB-77, 21.09.2026), 26.4 — der Wortlaut bleibt stehen:** der Vorbehalt gilt für die Jahre im Horizont; der Zehnjahres-Horizont begrenzt seine Reichweite, ändert ihn nicht.
>
> **(d)** Ein Wechsel auf ein point-in-time-Universum ist eine
> **Strategieänderung und ein neuer registrierter Lauf mit eigenem N**. Er ist
> **kein Amendment** dieses Laufs.

**Die Universumsdateien** (Tatsachennotiz zu 3a):

| Markt | Datei | SHA-256 | Symbole |
|---|---|---|---:|
| krypto | `config/top25_symbols.txt` | `3afc95a4f6b5ebc3a8f7bb7854b5dd59c4ecc4e3d86aa7b93c08066a3fccf810` | 24 (26 Zeilen abzüglich `XAUTUSDT`, `PAXGUSDT`) |
| aktien | `config/sp500_top150.txt` | `6acba892f38e998cf43ae9e5594c4707945143aba481429c44a5c6005339f607` | 150 |

> ⚠️ **Die Klammer in der Krypto-Zeile rechnet falsch und ist KORRIGIERT in
> Abschnitt 16 (TB-41), 16.1.3:** Die Datei mit dem eingetragenen Hash hat **25**
> nichtleere Zeilen, nicht 26, und `PAXGUSDT` steht nicht darin. Richtig ist
> **24 (25 Zeilen abzüglich `XAUTUSDT`)**. Das Ergebnis 24 und der Hash bleiben.

Alle vier Aktien-Bots lesen **dieselbe** Datei
(`strategies/<bot>/stocks_symbols_config.py`), alle fünf Krypto-Bots dieselbe
(`shared/symbols_config.py`). Es gibt also zwei Universen, nicht neun.

**Die Symbolzahl je Falte** (Tatsachennotiz zu 3b):

| Bot | Symbolzahl je Selektionsfalte | Bestätigung | Universum |
|---|---|---:|---:|
| `elliott_wave` | 6 / 13 / 13 | 18 | 24 |
| `t3_supertrend` | 6 / 9 / 13 / 13 / 13 / 17 / 18 | 23 | 24 |
| `rsi2_crypto` | 6 / 9 / 13 / 13 / 13 / 17 / 18 | 23 | 24 |
| `turtle_soup_crypto` | 6 / 9 / 13 / 13 / 13 / 17 / 18 | 23 | 24 |
| `volatility_breakout_crypto` | 6 / 9 / 13 / 13 / 13 / 17 / 18 | 23 | 24 |
| `elliott_wave_stocks` | 140 / 142 / 145 / 147 / 148 / 148 / 149 | 150 | 150 |
| `rsi2_mean_reversion` | 140 / 142 / 145 / 147 / 148 / 148 / 149 | 150 | 150 |
| `turtle_soup_stocks` | 140 / 142 / 145 / 147 / 148 / 148 / 149 | 150 | 150 |
| `volatility_breakout` | 140 / 142 / 145 / 147 / 148 / 148 / 149 | 150 | 150 |

> ⚠️ **ERSETZT durch Abschnitt 16 (Registernachtrag TB-41, 16.09.2026), 16.1.1.**
> Acht der neun Reihen dieser Tabelle sind **zu hoch**; gemessen wurde in TB-40
> am Loader des Bots. Nur `elliott_wave` stimmt. Es kommt nirgends ein Symbol
> hinzu.

`elliott_wave` hat Doppeljahr-Falten; seine drei Zahlen stehen für 2019–2020,
2021–2022 und 2023–2024, seine Bestätigungsperiode beginnt am 1. Januar 2025.

**Symbole ohne Faltenevidenz** (Tatsachennotiz zu 3b, namentlich):

* **krypto (6 von 24):** `BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`,
  `UUSDT`, `ZKCUSDT`. Alle sind erst 2025 oder 2026 gelistet;
  `TRUMPUSDT` (19.01.2025) verfehlt die letzte Selektionsfalte um 18 Tage und
  ist in der Bestätigungsperiode dabei, `UUSDT` (13.01.2026) in keiner von
  beiden.
* **aktien (1 von 150):** `SNDK` (ab 13.02.2025).

> ⚠️ **ERSETZT durch Abschnitt 16 (Registernachtrag TB-41, 16.09.2026), 16.1.2.**
> Diese Listen werden **je Bot** geführt, nicht je Markt: `elliott_wave` 11,
> `t3_supertrend` 7, die drei Krypto-Tagesbots 6, die vier Aktien-Bots **5**
> (nicht nur `SNDK`).

Für diese sieben Symbole gilt der gewählte Parametersatz live **ohne
Faltenevidenz**. Das ist keine Nachlässigkeit, sondern die Kehrseite von 3d:
wer sie hätte, hätte ein point-in-time-Universum und damit einen anderen Lauf.

**Wie „einschliesslich Indikator-Vorlauf" gerechnet ist** — und was es kostet:

Der Halbsatz lässt zwei Lesarten zu. Eingetragen ist **Lesart A**: am 1. Januar
liegen Kursdaten vor; der Indikator-Vorlauf speist sich aus der eigenen
Historie des Symbols und läuft, wo er noch nicht voll ist, in die Falte hinein —
das Symbol handelt dort ein paar Tage später und trägt für diese Tage 0 bei,
genau wie es der nächste Satz von 3a vorschreibt. **Lesart B** (voller Vorlauf
schon am 1. Januar, sonst zählt das Symbol nicht mit) ergibt andere Zahlen. Sie
stehen hier nachrichtlich, weil ein Preis, den eine Festlegung kostet, neben der
Festlegung stehen gehört und nicht in einer Fussnote:

| Bot | Indikator-Vorlauf | Lesart B je Selektionsfalte | Bestätigung | gegen A |
|---|---:|---|---:|---|
| `elliott_wave` | 0 Balken *(Zigzag, kein Fenster)* | 6 / 13 / 13 | 18 | gleich |
| `t3_supertrend` | 1 Balken *(EWM ohne Mindestfenster)* | 6 / 9 / 13 / 13 / 13 / 17 / 18 | 23 | gleich |
| `rsi2_crypto` | 150 Balken *(SMA-Trendfilter)* | 6 / 9 / **9** / 13 / 13 / 17 / 18 | **20** | abweichend |
| `turtle_soup_crypto` | 30 Balken *(Donchian)* | 6 / 9 / 13 / 13 / 13 / 17 / 18 | 23 | gleich |
| `volatility_breakout_crypto` | 127 Balken *(Squeeze)* | 6 / 9 / **10** / 13 / 13 / 17 / 18 | **20** | abweichend |
| `elliott_wave_stocks` | 0 Balken *(Zigzag, kein Fenster)* | 140 / 142 / 145 / 147 / 148 / 148 / 149 | 150 | gleich |
| `rsi2_mean_reversion` | 200 Balken *(SMA 200)* | **139 / 140 / 142 / 145** / 148 / 148 / **148** | 150 | abweichend |
| `turtle_soup_stocks` | 30 Balken *(Donchian)* | 140 / 142 / **143** / 147 / 148 / 148 / 149 | 150 | abweichend |
| `volatility_breakout` | 127 Balken *(Squeeze)* | **139** / 142 / **142** / **146** / 148 / 148 / 149 | 150 | abweichend |

Die Vorlaufzahlen sind aus dem Bot-Code **gelesen**, je Bot mit Fundstelle im
Kopf von `research/faltenplan_neun/faltenplan_neun.py`. Dass Lesart A gilt,
entscheidet nicht dieses Werkzeug, sondern der Registertext selbst: 3b nennt
**eine** Zahlenreihe für **alle** Krypto-Tagesbots — hinge die Zahl am Vorlauf,
hätte jeder Bot seine eigene, wie die Tabelle zeigt.

> ⭐ **15.5 ERGÄNZT durch R53 (49.1)** (Fable 30a R53, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

### 15.6 Registertext 4 — Falten

> **(a)** Es gibt **kein Trainingsfenster**. Selektionsfalten sind alle
> vollständigen Kalenderjahre (bzw. Doppeljahre) vom ersten Jahr, in dem am 1.
> Januar Daten für Universum und Indikator-Vorlauf vorliegen, bis zum letzten
> vollständigen Jahr vor Go-Live.
>
> ⚠️ **(a) ERSETZT durch Abschnitt 25 (Berichtigung TB-72, 20.09.2026), 25.3 — der Wortlaut bleibt stehen.** Die Neufassung führt (a) und 21.3 (b) als Konjunktion in einem Satz zusammen.
>
> **(b)** *[ersetzt „mindestens 4"]* Mindestzahl Selektionsfalten je Bot: **3**,
> unabhängig von der Faltenlänge. *Begründung: Ein Median braucht mindestens
> einen Wert auf jeder Seite des mittleren. Bei drei Falten ist der Median der
> mittlere Wert; bei vier ist er das Mittel aus zweien.*
>
> **(c)** *[ersetzt „behält seine heutigen Parameter"]* Ein Bot mit weniger als
> 3 Selektionsfalten wird nicht selektiert. Er wird als „unterbestimmt" mit
> Faltenzahl berichtet, läuft mit den heutigen Parametern **als Schatten
> ausserhalb des Buchs** weiter, und sein Budget hält eine **statische
> Benchmark-Position in Höhe seines gemessenen mittleren Exposures**. Die
> Selektion wird für ihn als eigener registrierter Lauf nachgeholt, sobald 3
> Falten vorliegen.
>
> **(d)** Die Faltenliste je Bot wird vor dem Lauf berechnet und ins Register
> geschrieben.

> ⭐ **15.6 (c) PRÄZISIERT durch R23 (47.6)** (Fable 27c R23, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Die Faltenliste je Bot** (Tatsachennotiz zu 4d):

| Bot | Markt | Faltenlänge | Selektionsfalten | # | Bestätigungsperiode |
|---|---|---:|---|---:|---|
| `elliott_wave` | krypto | 2 J | 2019–2020, 2021–2022, 2023–2024 | 3 | 2025-01-01 … 2026-09-01 |
| `t3_supertrend` | krypto | 1 J | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 7 | 2026-01-01 … 2026-09-01 |
| `rsi2_crypto` | krypto | 1 J | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 7 | 2026-01-01 … 2026-09-01 |
| `turtle_soup_crypto` | krypto | 1 J | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 7 | 2026-01-01 … 2026-09-01 |
| `volatility_breakout_crypto` | krypto | 1 J | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 7 | 2026-01-01 … 2026-09-01 |
| `elliott_wave_stocks` | aktien | 1 J | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 7 | 2026-01-01 … 2026-09-01 |
| `rsi2_mean_reversion` | aktien | 1 J | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 7 | 2026-01-01 … 2026-09-01 |
| `turtle_soup_stocks` | aktien | 1 J | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 7 | 2026-01-01 … 2026-09-01 |
| `volatility_breakout` | aktien | 1 J | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 7 | 2026-01-01 … 2026-09-01 |

Der Go-Live-Schnitt bleibt **2026-09-01, ausschliesslich** (Abschnitt 5.2,
unberührt). Die Bestätigungsperiode ist deshalb angeschnitten und wächst jeden
Monat; ihr Beginn verschiebt sich zusätzlich um das Embargo aus 2d.

**Kein Bot ist unterbestimmt.** Der niedrigste Wert ist 3 (`elliott_wave`) und
erreicht die Schwelle aus 4b genau. Regel 4c greift heute für keinen der neun —
sie steht für den Fall, dass sich das ändert.

Vier Punkte, die diese Tabelle tragen:

1. **Doppeljahre bekommt genau ein Bot.** Das ist die bestehende Registerregel
   5.1 Nr. 6 (Festlegung 7: „ein Jahr, zwei Jahre bei unter 30 gefundenen Trades
   je Jahr"), ausgewertet wie in 5.4 beschrieben — auf den **gefundenen** Trades
   aus `research/tb24_haltedauern/`, angeschnittene Randjahre ausgenommen. Sie
   ist hier **nachgerechnet, nicht abgeschrieben**, und kommt auf dieselbe
   Antwort wie 5.4: `elliott_wave` mit 26,0 Trades je vollem Kalenderjahr; die
   übrigen acht liegen zwischen 50,9 und 1.202,2.
2. **Die erste Falte ist 2019, und die Schranke dafür ist das Register, nicht
   die Datenlage.** `ERSTE_MOEGLICHE_FALTE = 2019` gilt unverändert. Ohne diese
   Schranke begänne der Plan bei acht der neun Bots schon 2017 oder 2018 —
   Bitcoin-Daten reichen bis 2017-08-17 zurück. Nur bei `rsi2_crypto` bindet die
   Datenlage selbst (150 Tagesbalken Vorlauf, erst ab 2019 erfüllt); bei den
   anderen acht bindet die Registerschranke.
3. **Aktien: Zeitfenster `RECENT_YEARS_ONLY = 10`**, gemessen vom letzten
   Kurstag (2026-09-01) zurück auf **2016-09-01** — so rechnen die vier
   Aktien-Bots selbst. Das Fenster bindet die Faltenliste nicht: die erste
   mögliche Falte läge auch danach vor 2019.
4. **Symbole ohne Historie in einer Falte werden nicht ausgeschlossen.** Die
   Symbolzahl aus 3b ist eine **Berichtszahl** — wie viele Symbole in dieser
   Falte überhaupt Evidenz liefern können —, keine Auswahl. In jeder Falte gilt
   „Symbole mit Historie + Symbole ohne Historie = volles Universum"; das
   Werkzeug führt beide Listen und der Selbsttest prüft die Summe je Falte.

> ⭐ **15.6 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

### 15.7 Registertext 5 — Datenstand *(neu, aus dem TB-35-Mac-Lauf)*

> Der Datenstand-Hash über **Binance-Dateien** ist stabil und reproduzierbar
> (TB-35, Schritt 7: 0 abweichende Zeilen bei einem echten Abruf).
>
> ⚠️ Der Hash über **yfinance-Dateien ist es nicht, und zwar
> konstruktionsbedingt.** `auto_adjust=True` rechnet die gesamte Historie mit
> einem Bereinigungsfaktor um; dessen Rundung schwankt von Abruf zu Abruf
> (gemessen: bis 1,2 × 10⁻⁶ relativ, zwei Läufe im Abstand von Minuten ergaben
> verschieden viele abweichende Zeilen). Unabhängig davon wird die Reihe bei
> **jeder Dividendenzahlung** zu Recht neu skaliert.
>
> **Der Datenstand-Hash über Aktiendateien ist deshalb eine Momentaufnahme des
> committeten Zustands, keine Festschreibung einer unveränderlichen Wahrheit.**
> Der für den Selektionslauf massgebliche Zustand ist der im Repo committete.
> Ein Aktien-Abruf zwischen Registereintrag und Selektionslauf ändert den Hash
> und ist zu unterlassen.
>
> ⚠️ **ERSETZT durch Abschnitt 16 (Registernachtrag TB-41, 16.09.2026), 16.3.**
> Registertext 5 trennt dort `data/live/` und `data/snapshots/<hash>/`; der
> Registerhash bezeichnet den **Snapshot**. Die hier festgehaltenen Tatsachen
> zur Hash-Stabilität bleiben gültig — sie sind der Grund für die Trennung.

---

### 15.8 Befunde am Rande — vier Stellen, an denen der Nachtrag auf Widerstand stiess

Keiner dieser vier ändert eine Zahl. Sie stehen hier, weil sie sonst beim
nächsten Lesen erneut Zeit kosten.

1. **Die Bezeichnung „AF.2 Nr. 6" gibt es in diesem Repo nicht.** Gemeint — und
   angewandt — ist die Doppeljahr-Regel aus **Abschnitt 5.1 Nr. 6** zusammen mit
   ihrer Auswertung in **5.4** (Festlegung 7,
   `registerdaten.ZWEIJAHRES_SCHWELLE_TRADES = 30`). Die Regel wurde
   nachgelesen, nicht erfunden; nur ihr Aktenzeichen stimmt nicht.
2. **Drei „ersetzte Fassungen" haben hier nie gestanden** — die Mindestzahl 10
   Trades (1c), „mindestens 4" Selektionsfalten (4b) und „behält seine heutigen
   Parameter" (4c). Gesucht wurde im ganzen Register, in
   `research/vorregistrierung/` und in `docs/`. Sie stammen aus früheren
   Beratungsrunden. Die Klammerzusätze bleiben wörtlich stehen, weil sie
   festhalten, **wogegen** entschieden wurde; eingetragen sind sie hier als
   **Erstfassung**, nicht als Widerruf.
3. **`research/vorregistrierung/auswertung.py` rechnet weiterhin nach Verfahren
   A** — es liest `faltenplan.py` mit Trainingsfenstern, Purge und Embargo
   zwischen den Falten, und es kennt für Krypto nur Platzhalter. Das ist kein
   Versehen dieses Nachtrags: die Datei ist **eingefroren** und wurde nicht
   angefasst. Ihre Umstellung ist **TB-30b**. Bis dahin gilt: der Nachtrag
   beschreibt, was gerechnet wird, und `auswertung.py` kann es noch nicht.
4. **Die Bots selbst überspringen kurze Historien** (`MIN_HISTORY_DAYS`: 1825
   Tage bei allen vier Aktien-Bots, 500 bei drei Krypto-Bots). Ein Symbol mit zu
   kurzer Historie wird dort gar nicht erst geladen. Die Symbolzahlen aus 3b
   sagen also, wie viele Symbole **Evidenz liefern können**, nicht wie viele der
   heutige Bot-Code tatsächlich lädt. Bei den vier Aktien-Bots betrifft das drei
   Titel (`GEV`, `SNDK`, `CEG` — alle erst 2022 oder später gelistet), bei Krypto
   vier der sechs aus 3b (`ENSOUSDT`, `PUMPUSDT`, `ZKCUSDT`, `UUSDT`). Auch diese
   Angleichung gehört in TB-30b.

---

### 15.9 Was dieser Nachtrag nicht tut

* **Kein Selektionslauf.** Es ist weiterhin kein Raster gerechnet.
* **Keine Parameterübernahme.** `live_params.py` ist in dieser Arbeit nur
  **gelesen** worden, ebenso `forward_test.py` und die Backtest-Dateien; keine
  Bot-Datei wurde importiert oder verändert.
* **Keine Kursdatei angefasst.** Der Datenstand ist unverändert
  `d9449faf51bffaaa…` bei 223 Dateien.
* **`auswertung.py` unberührt** — eingefroren, siehe 15.8 Nr. 3.

*Nachgetragen in TB-36, 15.09.2026. Kein Amendment: kein Selektionslauf, kein
signierter Tag, keine Parameterübernahme.*

---

