# Vorregistrierung der Neuselektion (TB-30a)

**Stand: 14.09.2026. Dies ist das Register. Es wird vor dem Lauf eingefroren
und danach nicht mehr verhandelt.**

> **Hier wurde kein Selektionslauf gestartet.** Kein Raster gerechnet, kein
> Parametersatz bewertet, kein Ergebnis erzeugt. Wer in diesem Dokument oder
> in `research/vorregistrierung/ergebnisse/` ein Rasterergebnis sucht, sucht
> vergeblich — dort liegen ausschliesslich Vorab-Berechnungen aus Kursdaten
> und Handelskosten.

---

## 0. Warum es dieses Dokument gibt

Die anstehende Neuselektion ist die **erste echte Optimierung in der
Geschichte dieses Projekts**. Bis hierher wurde auf einem Mass ausgewählt,
das mit dem Zielmass unkorreliert (sechs Bots) oder **negativ** korreliert
war (drei Bots, gemessen in `research/drawdown_reihenfolge/`).

> Datenausbeutung entsteht nicht dort, wo ein Mensch die Zukunft kennt,
> sondern dort, wo ein Mensch **nach** dem Ergebnis noch eine Wahl hat. Jede
> Stelle, an der nach dem Lauf jemand entscheidet — eine Schwelle
> „nachjustiert", ein Rastersegment „ergänzt", ein Bot „vorerst behalten" —,
> ist eine zusätzliche Selektion, **die in keinem N auftaucht**.
>
> **Ziel: Nach dem Lauf gibt es keine Entscheidung mehr, nur eine Lektüre.**

Der Weg dorthin ist Code. Das Skript, das aus den Rohergebnissen die Auswahl
und die Bleibt-Geht-Liste berechnet, ist **vor** dem Lauf geschrieben und
eingefroren: `research/vorregistrierung/auswertung.py`.

**Der Vollständigkeitstest lautete:** *Lässt sich das Auswertungsskript
fertig schreiben, ohne ein einziges Ergebnis gesehen zu haben?* Die Antwort
und die Stellen, an denen dafür eine Lesart festgelegt werden musste, stehen
in Abschnitt 12.

---

## 1. Die zwölf Festlegungen des Betreibers (14.09.2026)

Nicht neu verhandelt — eingetragen. Sie stehen maschinenlesbar in
`research/vorregistrierung/registerdaten.py::FESTLEGUNGEN`.

| # | Festlegung | Wert |
|---|---|---|
| 1 | Führendes Mass | **Kapital-Drawdown** aus `equity_simulation.py` |
| 2 | Selektionsstatistik | **Median des Netto-Sharpe über die Selektionsfalten** |
| 3 | Beurteilung | Netto-Calmar, daneben Mittelwert der **drei tiefsten** Drawdowns und Netto-Sharpe |
| 4 | Drawdown-Bedingung je Falte | **`erlaubt(f) = min(1,25 × DD_Benchmark(f), DD_Toleranz)`** — beide negativ, `min` ist der **tiefere** und damit grosszügigere Wert |
| 5 | `DD_Toleranz` | **Median der Benchmark-Drawdowns über alle Selektionsfalten, je Bot** |
| 6 | **Keine absolute Drawdown-Grenze** | Begründung in Abschnitt 4.3 |
| 7 | Schwelle für Zweijahres-Falten | **30 Trades je Jahr** |
| 8 | Spitzen-Schwelle der Plateau-Regel | **50 %** über dem Nachbarschaftsmittel |
| 9 | Cluster-Schwelle für N_eff | Korrelation **0,9** |
| 10 | DSR-Basis | **N = 653**, dieser Lauf zählt dazu |
| 11 | **DSR ist Bericht, nicht Tor** | Bleibt-Geht läuft über die Abbruchkriterien |
| 12 | Das zulässige Ergebnis | siehe unmittelbar unten — **wörtlich** |

### Festlegung 12, wörtlich

> **Dieses Ergebnis ist zulässig: Es kann sein, dass kein einziger Bot die
> Schwelle erreicht.** Eine Aussage über den **Backtest**, nicht über die
> Bots. *Wer das vorher nicht aufschreibt, wird es nachher nicht
> akzeptieren.*

Der Satz steht als Zeichenkette in `registerdaten.py`, wird von
`auswertung.py` am Ende jeder Bleibt-Geht-Liste ausgegeben und ist damit
Bestandteil jedes Berichts — auch desjenigen, in dem er unangenehm ist.

---

## 2. Die Rastergrenzen

### 2.1 Wie sie entstehen — und warum keine von ihnen getippt ist

**Der heutige Live-Wert ist kein Bezugspunkt.** Um das nicht nur zu
behaupten, ist in diesem Register **keine Rastergrenze eine Zahl**, sondern
eine Regel über eine gemessene Grösse:

```python
{"regel": "sigma_vielfaches", "zeitrahmen": "krypto_1d", "faktor": 0.5}
```

`research/vorregistrierung/pruefe_grenzsaetze.py` rechnet jede Regel nach,
vergleicht sie mit dem ausgewiesenen Wert und prüft zusätzlich, dass keine
Zahl im Begründungssatz mit einem Live-Wert dieses Bots zusammenfällt. Ein
Live-Wert kann so nur noch **durch Zufall** in einer Grenze landen — und
dieser Zufall fällt auf.

**Das ist keine Theorie.** Beim Schreiben dieses Registers hat die Prüfung
angeschlagen: der Satz zur Obergrenze der T3-Längen enthielt die Ziffernfolge
„20-Balken-Spanne", und `t3_supertrend` führt `ADX_THRESHOLD = 20.0`. Der
Satz ist deshalb umformuliert („Zwanzig-Balken-Spanne"). Die Übereinstimmung
war unschuldig — und genau deshalb ist sie ein guter Beleg dafür, dass die
Wache etwas tut.

**Nicht geprüft wird, ob ein Stufenwert mit einem Live-Wert zusammenfällt.**
Das darf er: die Stufen sind *gerechnet*, nicht gewählt. Verboten ist allein,
einen Live-Wert im *Satz* zu nennen — denn das lüde zum Rückschluss ein.
`pruefe_grenzsaetze.py` hält diesen Unterschied ausdrücklich fest, damit er
nicht später versehentlich verschärft wird.

### 2.2 Die vier zulässigen Grundlagen — und zwei benannte Ausnahmen

Zulässig sind `kosten`, `datenfrequenz`, `volatilitaet`, `haltedauer`.

Zwei Grenzen stützen sich auf keine davon. Das steht hier ausdrücklich statt
verdeckt:

| Kennzeichnung | Wo | Warum keine der vier |
|---|---|---|
| `ableitung` | Obergrenze des Positionslimits | `floor(1 / ALLOCATION_PCT)` ist keine Wahl, sondern eine Identität: ein Rasterpunkt darüber **ist derselbe Punkt**. Die Regel steht so in der Aufgabenstellung. |
| `methode` | Fibonacci-Leiter, Bollinger-Fenster | Eigenschaften des Verfahrens, nicht Einstellungen — dieselbe Rolle wie die Kostenkonvention von 0,30 %. |

Beide Sätze nennen **keine Zahl**; die Werte stehen in einem getrennten Feld.

### 2.3 Die abgeleitete Obergrenze des Positionslimits

`floor(1 / ALLOCATION_PCT)`, gelesen über
`notifications/manual_close.py::allokation()` — dieselbe Quelle, die auch der
schreibende Schliess-Dialog benutzt, damit die Zahl nicht zweimal im Repo
steht.

| Bot | `ALLOCATION_PCT` | Obergrenze | heutiger Live-Wert | greift das Live-Limit? |
|---|---:|---:|---:|---|
| `t3_supertrend` | 10 % | 10 | 5 | ja |
| `rsi2_crypto` | 10 % | 10 | 8 | ja |
| `turtle_soup_crypto` | 10 % | 10 | 8 | ja |
| `volatility_breakout_crypto` | 10 % | 10 | 8 | ja |
| `elliott_wave_stocks` | 10 % | 10 | 8 | ja |
| `volatility_breakout` | 10 % | 10 | **15** | **nein — es greift nie** |
| `rsi2_mean_reversion` | 5 % | 20 | 20 | genau an der Grenze |
| `turtle_soup_stocks` | 2 % | 50 | unbegrenzt | „unbegrenzt" **ist** 50 |

*(Die Live-Werte stehen hier zur Einordnung des Lesers, nicht als
Bezugspunkt: keiner von ihnen geht in eine Rastergrenze ein. Die Spalte
existiert, weil `volatility_breakout` sonst weiter mit einem Limit geführt
würde, das rechnerisch nichts tut.)*

### 2.4 Die eingetragene Ausnahme: `elliott_wave` ohne Limitachse

`strategies/elliott_wave/equity_simulation.py` führt als einziger der neun
**kein** `max_concurrent_positions`. Zwölf Stellen im Repo erkennen an genau
dieser Signatur, welcher Bot keines hat; das Übergabeprotokoll (Abschnitt 8,
TB-26/TB-28) hat die Signatur ausdrücklich so entschieden.

**Folge, eingetragen:** Der Bot wird mit der Kapitalschranke
`floor(1/ALLOCATION_PCT) = 10` gerechnet und in der Beurteilung mit der
Markierung *„ohne Limitachse"* geführt. Sein gemessenes Maximum liegt bei
sieben gleichzeitigen Positionen (`research/exposure_messung/`), die
Schranke bindet also ohnehin nicht.

### 2.5 Die Kantenregel

> Liegt der Gewinner auf einer Rasterkante, wird **nicht erweitert.** Der
> Kantenwert gilt, der Bot bekommt die Markierung „Kante". Eine Erweiterung
> wäre ein **neuer vorregistrierter Lauf**, dessen Zellen zu N addiert
> werden.

*Genau das ist in der Vergangenheit unterblieben: eine verschobene
Rastergrenze in `strategies/elliott_wave_stocks/multi_symbol_optimise.py:39`
(`STOP_LOSS_RANGE`, „erweitert (bis 8%)"), begründet mit einer „Erkenntnis
aus `compare_exit_rules.py`" — einer Datei, die nie im Repo lag. Die
Rastergrenzen dieses Registers ersetzen sie.*

Die Markierung setzt `auswertung.py` selbst (`markierungen`), und
`test_vorregistrierung.py` Teil C hält fest, dass das Raster dabei
unverändert bleibt.

### 2.6 Was **nicht** im Raster steht

Aufgenommen sind genau die Parameter, die der jeweilige Bot heute schon
rastert, dazu das Positionslimit — und dort, wo die Aktien- und die
Krypto-Variante bisher verschiedene Parameter rasterten, die Vereinigung
beider, damit überall **dieselbe Regel** gilt.

Bewusst **draussen** bleiben Parameter, die dieses Projekt noch nie
ausgewählt hat, insbesondere die **Zeitbremse** (`MAX_HOLD_DAYS`,
`MAX_HOLD_HOURS`). Sie behalten ihre heutige Einstellung, und zwar als
*festgeschriebene Konstante des Laufs*, nicht als Bezugspunkt einer Grenze.

**Der Grund ist nicht Bequemlichkeit, sondern N.** Jede zusätzliche Achse
multipliziert die Zellenzahl, und jede Zelle erhöht den Abschlag der
Deflated Sharpe Ratio. Ein Raster, das alles mitnimmt, gewinnt Auflösung und
verliert Aussagekraft. TB-24 hat zudem gemessen, dass die Zeitbremse der
stärkste Einzelhebel auf die Haltedauer-Verteilung ist — sie zu rastern wäre
eine eigene, eigens vorzuregistrierende Untersuchung.

**Zwei Achsen verlangen eine Vorarbeit in TB-30b** (siehe Abschnitt 11):
`sma_trend_filter` ist bei `rsi2_mean_reversion` heute eine Konstante
(`SMA_TREND_PERIOD = 200` in `backtest_rsi2.py`) und muss durchgereicht
werden; `bb_squeeze_percentile` und `bb_lookback` stehen bei beiden
Volatility-Breakout-Bots in `live_params.py`, aber nicht im Optimierer.

### 2.7 Stufung

**Geometrisch** für Skalenparameter (Faktor 1,5 bis 2,0, drei bis fünf
Stufen), **linear und ganzzahlig** für Zählparameter. Beides wird beim Bauen
des Rasters erzwungen: `registerdaten.geometrische_stufen()` bricht ab, wenn
der Faktor ausserhalb von 1,5 bis 2,0 fällt, und `lineare_stufen()` bricht
ab, wenn zwei Stufen nach dem Runden zusammenfallen.

**Ein Raster je Bot, identisch über alle Falten.** Gleiche Parameter in
Aktien- und Krypto-Variante mit **derselben Regel**, nicht demselben Wert —
deshalb stehen die Grenzsätze in Abschnitt 3 nur einmal, obwohl sie für zwei
Bots gelten.

---

## 3. Der Zahlenteil — erzeugt, nicht abgetippt

Alles Folgende bis zur Endmarkierung erzeugt
`research/vorregistrierung/registerbericht.py`.
`registerbericht.py --pruefen` meldet mit Rückgabewert 1, sobald der Block
hier nicht mehr wörtlich mit dem Code übereinstimmt — dann ist dieses
Dokument veraltet, und das fällt auf, statt zu wirken.

<!-- ERZEUGT: registerbericht.py -- nicht von Hand aendern -->

### Die gemessenen Groessen, auf denen jede Grenze ruht

Erzeugt von `research/vorregistrierung/messgroessen.py` aus `data/` und `config/` — **keine Bot-Ergebnisse.**

| Zeitrahmen | Titel | σ je Balken | Median 20-Balken-Spanne | ATR(14) | Median Schluss→Tief |
|---|---:|---:|---:|---:|---:|
| `aktien_1d` | 150 | 2,2218 % | 11,381 % | 2,34 % | 0,9158 % |
| `krypto_1d` | 23 | 5,2782 % | 34,2726 % | 7,2669 % | 2,6836 % |
| `krypto_1h` | 24 | 1,1082 % | 5,846 % | 1,2662 % | 0,501 % |
| `krypto_4h` | 24 | 2,178 % | 12,1902 % | 2,6952 % | 1,0537 % |

Round-Trip-Kosten: **0,3 %** (0,1 % Gebühr + 0,05 % Slippage je Order, Ein- und Ausstieg).

### Die neun Raster

| Bot | Achse | Stufen | Untergrenze | Obergrenze |
|---|---|---|---|---|
| `elliott_wave` | `deviation_pct` | 1,108, 1,929, 3,358, 5,846 | *kosten* | *volatilitaet* |
| `elliott_wave` | `stop_loss_pct` | 2,639, 4,796, 8,714, 15,835 | *volatilitaet* | *volatilitaet* |
| `elliott_wave` | `take_profit_fib` | 0,236, 0,382, 0,5, 0,618, kein | *methode* | *methode* |
| `t3_supertrend` | `t3_fast_length` | 2, 12, 21, 31 | *datenfrequenz* | *volatilitaet* |
| `t3_supertrend` | `t3_slow_length` | 2, 12, 21, 31 | *datenfrequenz* | *volatilitaet* |
| `t3_supertrend` | `adx_threshold` | 24,948, 27,825, 31,492, 36,492 | *volatilitaet* | *volatilitaet* |
| `t3_supertrend` | `stop_loss_pct` | 2,639, 4,796, 8,714, 15,835 | *volatilitaet* | *volatilitaet* |
| `t3_supertrend` | `max_concurrent_positions` | 2, 5, 7, 10 | *volatilitaet* | *ableitung* |
| `rsi2_crypto` | `rsi_threshold` | 0,899, 1,729, 3,728, 7,655 | *volatilitaet* | *volatilitaet* |
| `rsi2_crypto` | `sma_trend_filter` | 42, 123, 204, 284, 365 | *volatilitaet* | *datenfrequenz* |
| `rsi2_crypto` | `stop_loss_pct` | 2,639, 4,796, 8,714, 15,835, kein | *volatilitaet* | *volatilitaet* |
| `rsi2_crypto` | `max_concurrent_positions` | 2, 5, 7, 10 | *volatilitaet* | *ableitung* |
| `turtle_soup_crypto` | `donchian_period` | 5, 17, 30, 42 | *haltedauer* | *volatilitaet* |
| `turtle_soup_crypto` | `stop_mode` | 2,639, structural, 4,796, 8,714, 15,835, kein | *volatilitaet* | *volatilitaet* |
| `turtle_soup_crypto` | `max_concurrent_positions` | 2, 5, 7, 10 | *volatilitaet* | *ableitung* |
| `volatility_breakout_crypto` | `bb_squeeze_percentile` | 5, 20, 35, 50 | *datenfrequenz* | *ableitung* |
| `volatility_breakout_crypto` | `bb_lookback` | 20, 135, 250, 365 | *methode* | *datenfrequenz* |
| `volatility_breakout_crypto` | `stop_loss_pct` | 2,639, 4,796, 8,714, 15,835, kein | *volatilitaet* | *volatilitaet* |
| `volatility_breakout_crypto` | `max_concurrent_positions` | 2, 5, 7, 10 | *volatilitaet* | *ableitung* |
| `elliott_wave_stocks` | `deviation_pct` | 2,222, 3,83, 6,602, 11,381 | *kosten* | *volatilitaet* |
| `elliott_wave_stocks` | `stop_loss_pct` | 1,111, 2,019, 3,668, 6,665 | *volatilitaet* | *volatilitaet* |
| `elliott_wave_stocks` | `take_profit_fib` | 0,236, 0,382, 0,5, 0,618, kein | *methode* | *methode* |
| `elliott_wave_stocks` | `max_concurrent_positions` | 2, 5, 7, 10 | *volatilitaet* | *ableitung* |
| `rsi2_mean_reversion` | `rsi_threshold` | 0,767, 1,527, 3,906, 8,225 | *volatilitaet* | *volatilitaet* |
| `rsi2_mean_reversion` | `sma_trend_filter` | 26, 82, 139, 196, 252 | *volatilitaet* | *datenfrequenz* |
| `rsi2_mean_reversion` | `stop_loss_pct` | 1,111, 2,019, 3,668, 6,665, kein | *volatilitaet* | *volatilitaet* |
| `rsi2_mean_reversion` | `max_concurrent_positions` | 2, 8, 14, 20 | *volatilitaet* | *ableitung* |
| `turtle_soup_stocks` | `donchian_period` | 11, 16, 21, 26 | *haltedauer* | *volatilitaet* |
| `turtle_soup_stocks` | `stop_mode` | structural, 1,111, 2,019, 3,668, 6,665, kein | *volatilitaet* | *volatilitaet* |
| `turtle_soup_stocks` | `max_concurrent_positions` | 2, 18, 34, 50 | *volatilitaet* | *ableitung* |
| `volatility_breakout` | `bb_squeeze_percentile` | 5, 20, 35, 50 | *datenfrequenz* | *ableitung* |
| `volatility_breakout` | `bb_lookback` | 20, 97, 175, 252 | *methode* | *datenfrequenz* |
| `volatility_breakout` | `stop_loss_pct` | 1,111, 2,019, 3,668, 6,665, kein | *volatilitaet* | *volatilitaet* |
| `volatility_breakout` | `max_concurrent_positions` | 2, 5, 7, 10 | *volatilitaet* | *ableitung* |

### Die Grenzsätze

Ein Satz je Grenze, der **kein Ergebnis nennt** — gestützt nur auf Handelskosten, Datenfrequenz, Volatilität des Universums oder die Haltedauer-Hypothese des Bots. Gleiche Achsen tragen in der Aktien- und der Krypto-Variante **dieselbe Regel**, nicht denselben Wert; sie stehen deshalb nur einmal.

**`deviation_pct` — unten** *(Grundlage: kosten)*

> Eine Deviation unter dem Zweifachen der Round-Trip-Kosten ist Rauschen, dessen Bewegung die Kosten nicht traegt; unter einem Balken-Sigma laesst sich ein Wendepunkt ausserdem nicht vom einzelnen Balken trennen. Es gilt die hoehere der beiden Schranken.

**`deviation_pct` — oben** *(Grundlage: volatilitaet)*

> Eine Deviation ueber dem Median der Zwanzig-Balken-Spanne erzeugt kaum noch Muster - die Bewegung, die sie verlangt, kommt im typischen Fenster nicht vor.

**`stop_loss_pct` — unten** *(Grundlage: volatilitaet)*

> Ein Stop enger als ein halbes Tages-Sigma des Universums wird vom gewoehnlichen Tagesrauschen ausgeloest und misst keine Strategieannahme mehr.

**`stop_loss_pct` — oben** *(Grundlage: volatilitaet)*

> Ein Stop weiter als drei Tages-Sigma des Universums wird im typischen Verlauf nicht mehr erreicht - er ist dann keine Begrenzung, sondern eine Verzierung.

**`take_profit_fib` — achse** *(Grundlage: methode)*

> Die Stufen sind die Retracement-Verhaeltnisse der Elliott-Methode, aufsteigend, und als Grenzfall nach oben das Weglassen des Ziels. Sie sind eine Eigenschaft des Verfahrens, keine Einstellung.

**`t3_fast_length` — unten** *(Grundlage: datenfrequenz)*

> Unter zwei Balken glaettet eine Glaettung nicht mehr - sie wiederholt den Kurs.

**`t3_fast_length` — oben** *(Grundlage: volatilitaet)*

> Ueber diesen Horizont ist eine typische Bewegung ausgespielt: so viele Balken braucht das Balken-Sigma, um auf den Median der Zwanzig-Balken-Spanne anzuwachsen. Die Zahl steht bewusst ausgeschrieben - eine Ziffer im Grenzsatz koennte mit einem Live-Wert zusammenfallen, und die maschinelle Pruefung nimmt das nicht hin.

**`adx_threshold` — achse** *(Grundlage: volatilitaet)*

> Die Schwelle ist als Quantil der gemessenen ADX-Verteilung des Universums gesetzt: unter dem Median verwirft der Filter nichts, ueber dem Vierfuenftel-Quantil verwirft er mehr als vier Fuenftel aller Balken und laesst zu wenige Einstiege uebrig, um ihn zu bewerten.

**`max_concurrent_positions` — unten** *(Grundlage: volatilitaet)*

> Bei einem Limit von einer Position ist die Kapitalkurve die Kurve eines einzelnen Titels; die Volatilitaet des Universums geht dann ungedaempft durch, und das Limit misst die Titelauswahl statt der Streuung.

**`max_concurrent_positions` — oben** *(Grundlage: ableitung)*

> Mehr Positionen als Kehrwert der Positionsgroesse sind nicht finanzierbar; ein Rasterpunkt darueber ist derselbe Punkt.

**`rsi_threshold` — achse** *(Grundlage: volatilitaet)*

> Die Schwelle ist als Quantil der gemessenen RSI(2)-Verteilung des Universums gesetzt: unten das Quantil, unter dem im Mittel nur jeder hundertste Balken liegt (seltener laesst sich kein Einstieg mehr bewerten), oben das Quantil, ab dem jeder zehnte Balken ein Signal waere und die Schwelle nichts mehr aussortiert.

**`sma_trend_filter` — unten** *(Grundlage: volatilitaet)*

> Ein Trendfilter kuerzer als der Horizont, ueber den eine typische Bewegung ausgespielt ist, folgt dem eigenen Trade statt dem Marktzustand.

**`sma_trend_filter` — oben** *(Grundlage: datenfrequenz)*

> Ein Trendfilter ueber mehr als ein Kalenderjahr misst kein Regime mehr, sondern die Gesamtdrift des Universums.

**`stop_loss_pct` — zusatzstufe** *(Grundlage: methode)*

> Die Strategie ist in ihrer Urfassung ohne Stop beschrieben; 'kein Stop' ist der Grenzfall der Achse nach oben und steht deshalb als oberste Stufe, nicht als eigene Dimension.

**`donchian_period` — unten** *(Grundlage: haltedauer)*

> Ein Rueckblick kuerzer als die gemessene Median-Haltedauer dieses Bots ueberlebt die eigene Position nicht - das Muster, das den Einstieg begruendet, ist beim Ausstieg schon nicht mehr im Fenster.

**`stop_mode` — zusatzstufe_gemessen** *(Grundlage: volatilitaet)*

> Der Stop auf dem Tief des Setup-Balkens hat keine eingestellte Weite; er steht auf der Achse an der Stelle, die seiner GEMESSENEN Median-Weite entspricht - dem Median des Abstands Schluss zu Tief desselben Balkens. Wo das ist, rechnet das Register aus, es behauptet es nicht.

**`bb_squeeze_percentile` — unten** *(Grundlage: datenfrequenz)*

> Unterhalb von hundert geteilt durch das Bollinger-Fenster waehlt das Quantil weniger als einen Balken aus - dort ist 'Verengung' keine Aussage ueber das Fenster mehr.

**`bb_squeeze_percentile` — oben** *(Grundlage: ableitung)*

> Ueber dem Median ist die Verengung keine mehr: die Haelfte aller Balken erfuellte die Bedingung.

**`bb_lookback` — unten** *(Grundlage: methode)*

> Ein Rueckblick, der kuerzer ist als das Bollinger-Fenster selbst, vergleicht die Bandbreite mit sich selbst.

**`bb_lookback` — oben** *(Grundlage: datenfrequenz)*

> Ueber ein Kalenderjahr hinaus vergleicht der Rueckblick Marktphasen, nicht Verengungen.


| Bot | Zellen dieses Laufs | N historisch | N nominal |
|---|---:|---:|---:|
| `elliott_wave` | 80 | 252 | 332 |
| `t3_supertrend` | 384 | 81 | 465 |
| `rsi2_crypto` | 400 | 18 | 418 |
| `turtle_soup_crypto` | 96 | 12 | 108 |
| `volatility_breakout_crypto` | 320 | 4 | 324 |
| `elliott_wave_stocks` | 320 | 264 | 584 |
| `rsi2_mean_reversion` | 400 | 6 | 406 |
| `turtle_soup_stocks` | 96 | 12 | 108 |
| `volatility_breakout` | 320 | 4 | 324 |
| **Summe** | **2416** | **653** | **3069** |

### Der Faltenplan

> ⚠️ **ERSETZT durch Abschnitt 15 (Registernachtrag TB-36, 15.09.2026), Registertext 2 und 4.**
> Der Text bleibt hier stehen — der Verlauf soll lesbar bleiben; das ist der
> Sinn eines Registers. Massgeblich ist der Nachtrag.
> Die Spalte *Purge = Embargo* entfällt: zwischen Selektionsfalten gibt es unter
> Verfahren B weder Purge noch Embargo. Das Embargo bleibt nur an **einer** Stelle —
> vor der Bestätigungsperiode — und wird dort neu gerechnet (Registertext 2d). Die
> Krypto-Platzhalter sind durch Zahlen ersetzt.

Go-Live-Schnitt: **2026-09-01** (ausschliesslich). Mindesttraining vor der ersten Falte: **4 Jahre**.

| Bot | Markt | Faltenlänge | gefundene Trades/Jahr | Purge = Embargo | Selektionsfalten | Bestätigungsperiode |
|---|---|---:|---:|---:|---|---|
| `elliott_wave` | krypto | 2 J | 26 | 11 Tage | *Platzhalter (TB-31)* | *Platzhalter (TB-31)* |
| `t3_supertrend` | krypto | 1 J | 193,2 | 23 Tage | *Platzhalter (TB-31)* | *Platzhalter (TB-31)* |
| `rsi2_crypto` | krypto | 1 J | 134 | 10 Tage | *Platzhalter (TB-31)* | *Platzhalter (TB-31)* |
| `turtle_soup_crypto` | krypto | 1 J | 314,5 | 10 Tage | *Platzhalter (TB-31)* | *Platzhalter (TB-31)* |
| `volatility_breakout_crypto` | krypto | 1 J | 53,3 | 15 Tage | *Platzhalter (TB-31)* | *Platzhalter (TB-31)* |
| `elliott_wave_stocks` | aktien | 1 J | 50,9 | 134 Tage | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 2026 |
| `rsi2_mean_reversion` | aktien | 1 J | 537,3 | 18 Tage | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 2026 |
| `turtle_soup_stocks` | aktien | 1 J | 1202,2 | 18 Tage | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 2026 |
| `volatility_breakout` | aktien | 1 J | 456,7 | 26 Tage | 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 2026 |

### Die vorab berechneten Benchmark-Drawdowns

Je Falte, je Exposure-Stufe. Die vollständige Tabelle (1 % bis 100 % in Schritten von 1 %) steht in `research/vorregistrierung/ergebnisse/benchmark_drawdowns.json`; hier vier Stützstellen.

**aktien** (`config/sp500_top150.txt`) — gilt für alle Bots dieses Marktes mit gleichem Faltenplan:

| Falte | Rolle | Titel (point-in-time) | Handelstage | DD @ 25 % | DD @ 50 % | DD @ 75 % | DD @ 100 % |
|---|---|---:|---:|---:|---:|---:|---:|
| 2019 | selektion | 137 | 252 | -1,86 % | -3,69 % | -5,51 % | -7,3 % |
| 2020 | selektion | 137 | 253 | -9,77 % | -18,93 % | -27,48 % | -35,42 % |
| 2021 | selektion | 139 | 252 | -1,19 % | -2,38 % | -3,56 % | -4,74 % |
| 2022 | selektion | 139 | 251 | -5,07 % | -10,09 % | -15,06 % | -19,96 % |
| 2023 | selektion | 140 | 250 | -2,18 % | -4,33 % | -6,45 % | -8,55 % |
| 2024 | selektion | 142 | 252 | -1,74 % | -3,47 % | -5,17 % | -6,86 % |
| 2025 | selektion | 145 | 250 | -4,52 % | -8,89 % | -13,13 % | -17,23 % |
| 2026 | bestaetigung | 147 | 166 | -1,63 % | -3,23 % | -4,83 % | -6,4 % |
| **DD_Toleranz** | *Median über die Selektionsfalten* | | | -2,18 % | -4,33 % | -6,45 % | -8,55 % |

`rsi2_mean_reversion` teilt Universum und Faltenplan mit den übrigen aktien-Bots — dieselbe Tabelle.

`turtle_soup_stocks` teilt Universum und Faltenplan mit den übrigen aktien-Bots — dieselbe Tabelle.

`volatility_breakout` teilt Universum und Faltenplan mit den übrigen aktien-Bots — dieselbe Tabelle.

<!-- ENDE ERZEUGT -->

---

## 4. Die Drawdown-Bedingung

### 4.1 Die Regel

```
erlaubt(f) = min(1,25 × DD_Benchmark(f), DD_Toleranz)
```

Beide Werte sind negativ; `min` liefert den **tieferen** und damit die
**grosszügigere** Grenze. Ein Parametersatz besteht eine Falte, wenn sein
Kapital-Drawdown in dieser Falte nicht tiefer liegt als `erlaubt(f)`. Ein
Satz ist **zulässig**, wenn er **alle** Selektionsfalten besteht.

Die Regel steht als Funktion in `research/vorregistrierung/benchmark.py::erlaubt`
— an einer Stelle, damit sie nicht in Bericht und Rechnung auseinanderlaufen
kann.

### 4.2 Warum `DD_Benchmark` und `DD_Toleranz` ein Exposure-Argument tragen

Der Benchmark ist eine **statische Position** in Höhe der mittleren Exposure
im gleichgewichteten point-in-time-Universum. Im Lauf gilt die mittlere
Exposure des **jeweiligen Parametersatzes in der jeweiligen Falte**, nicht
die heute gemessene des Bots. Damit verweist keine Zahl dieses Registers auf
den Live-Zustand — und die Zahl liegt ohnehin vor, weil der Kapitalpfad sie
erzeugt.

Vorab berechenbar ist deshalb nicht *eine* Zahl je Falte, sondern die
**Funktion** `DD_Benchmark(f, e)` für `e = 1 %, 2 %, …, 100 %`. Diese Tabelle
steht auf der Sperrliste; im Lauf wird darin nachgeschlagen und zwischen den
beiden benachbarten Stützstellen **linear interpoliert**. Die
Interpolationsregel steht in derselben Datei wie die Tabelle
(`benchmark.py::nachschlagen`), damit beides zusammen gesperrt ist.

Festlegung 5 sagt: `DD_Toleranz` ist der **Median der Benchmark-Drawdowns
über alle Selektionsfalten, je Bot**. Da der Benchmark-Drawdown nach
Festlegung 4 selbst von der Exposure abhängt, **erbt der Median dieses
Argument**:

```
DD_Toleranz(e) = Median über die Selektionsfalten von DD_Benchmark(f, e)
```

Das ist keine zusätzliche Entscheidung, sondern die einzige Lesart, die mit
Festlegung 4 zusammenpasst — und sie erfüllt genau, was Festlegung 5
bezweckt: *„Je Bot, zwingend — ein Bot mit 21 % Zeit im Markt liegt auf einer
anderen Skala als einer mit 100 %."* Die Skala kommt jetzt aus der Exposure
selbst statt aus einem heute gemessenen Live-Zustand.

**Dass vier Aktien-Bots dieselbe Tabelle haben, ist kein Fehler.** Sie teilen
Universumsdatei und Faltenplan; ihre Skalen unterscheiden sich über das
Exposure-Argument, nicht über die Tabelle.

### 4.3 Warum es keine absolute Grenze gibt (Festlegung 6)

Eine feste Untergrenze bindet **nur**, wenn `1,25 × DD_Benchmark` tiefer
liegt — also wenn der Benchmark selbst unter **−28 %** fällt. Das passiert
bei Bots mit hoher Exposure in der Krisenfalte. Dort bindet sie dann aber für
**alle** Parametersätze gleichzeitig und **wirft den Bot aus, bevor gewählt
wurde**.

> *„Ein Bot, der bei voller Exposure in 2022 −33 % macht, hat kein
> Parameterproblem, sondern ein Beta-Problem — und das entscheidet Rang 3,
> nicht eine Nebenbedingung der Rasterselektion. Eine Grenze, die entweder
> redundant ist oder einen ganzen Bot vorab erledigt, gehört nicht ins
> Selektionsregister."*

**Der Risikoappetit kommt an zwei anderen Stellen zu seinem Recht:** als
Deckel je Bot im Netting (Rang 5), und als **berichtete Zeile** in der
Beurteilung. `auswertung.py` gibt sie aus, sobald der Gewinner in einer
Selektionsfalte tiefer als −30 % fällt:

```
! Risikoappetit     Parametersatz verletzt -30 % in Falte 2022 (-33.10 %)
```

### 4.4 Ist die Bedingung in 2020 und 2022 überhaupt erfüllbar?

Ja, und mit Luft. Gerechnet auf den Tabellen aus Abschnitt 3, bei 50 %
Exposure:

| Falte | `DD_Benchmark` | `1,25 ×` | `DD_Toleranz` | **erlaubt** | wer bindet |
|---|---:|---:|---:|---:|---|
| 2019 | −3,69 % | −4,61 % | −4,33 % | **−4,61 %** | die relative Grenze |
| **2020** | −18,93 % | **−23,66 %** | −4,33 % | **−23,66 %** | die relative Grenze |
| 2021 | −2,38 % | −2,98 % | −4,33 % | **−4,33 %** | `DD_Toleranz` |
| **2022** | −10,09 % | **−12,61 %** | −4,33 % | **−12,61 %** | die relative Grenze |
| 2023 | −4,33 % | −5,41 % | −4,33 % | **−5,41 %** | die relative Grenze |
| 2024 | −3,47 % | −4,34 % | −4,33 % | **−4,34 %** | die relative Grenze (knapp) |
| 2025 | −8,89 % | −11,11 % | −4,33 % | **−11,11 %** | die relative Grenze |

**Die Krisenfalten sind die grosszügigsten des ganzen Plans** — in 2020 darf
ein Parametersatz bei halber Exposure fast 24 % verlieren. Die Bedingung
bindet dort, wo sie soll: in den ruhigen Jahren, und auch dort nur oberhalb
der Rauschgrenze, weil `DD_Toleranz` 2021 die relative Grenze ablöst.

**Die eigentliche Lücke, die Festlegung 5 schliesst, ist in Zeile 2021
sichtbar:** ohne `DD_Toleranz` läge die Grenze dort bei −2,98 %, und drei
schlechte Tage entschieden über die Zulässigkeit eines Parametersatzes. Bei
so kleinen Zahlen ist das Verhältnis Rauschen.

`test_vorregistrierung.py` Teil D prüft beide Richtungen am Ablauf: einen
Satz, der die ruhige Falte um eine Spur reisst, und denselben Satz eine Spur
darüber.

---

## 5. Der Faltenplan

### 5.1 Die Regeln

> ⚠️ **ERSETZT durch Abschnitt 15 (Registernachtrag TB-36, 15.09.2026), Registertext 0, 2 und 4.**
> Der Text bleibt hier stehen — der Verlauf soll lesbar bleiben; das ist der
> Sinn eines Registers. Massgeblich ist der Nachtrag.
> Betroffen sind **Nr. 1** (verankert, expandierend), **Nr. 2** (Aktien: Training
> mindestens vier Jahre), **Nr. 3** zusammen mit 5.3 (Krypto-Platzhalter) und
> **Nr. 5** (Purge und Embargo zwischen den Falten). Sie stammen aus **Verfahren A**
> (faltenweise Auswahl mit Trainingsfenster); es gilt **Verfahren B** — eine
> einmalige Auswahl über das ganze Raster, ohne Trainingsfenster.
> **Unberührt** bleiben Nr. 4 (2020 und 2022 sind keine Trainingsjahre — unter
> Verfahren B gibt es gar kein Training), Nr. 6 (Faltenlänge, siehe 5.4),
> Nr. 7 (die letzte Falte ist die Bestätigungsperiode) und Nr. 8 (Falten ohne
> Trade zählen mit Sharpe 0 — Registertext 1c schärft das nur nach).

1. **Verankert, expandierend** (nicht rollierend). Das Training beginnt immer
   am Datenbeginn und endet am Faltenrand, abzüglich der Purge-Länge. Ein
   Verfahren, das alte Jahre vergisst, wählt im Zweifel die Parameter des
   letzten Marktzustands.
2. **Aktien:** Testfalten sind die Kalenderjahre **2019 bis zum
   Go-Live-Schnitt**, Training ab Datenbeginn, mindestens **vier Jahre** vor
   der ersten Falte.
3. **Krypto: Platzhalter mit Regel, keine Jahreszahlen** — siehe 5.3.
4. **2020 und 2022 sind Testfalten, keine Trainingsjahre.** Der Satz steht
   hier, weil dies die einzige Stelle wäre, an der die Versuchung entstünde,
   ein schweres Jahr ins Training zu schieben. `test_vorregistrierung.py`
   Teil G prüft es maschinell.
5. **Purge und Embargo** in Höhe der **maximalen gemessenen Haltedauer** des
   Bots, aus `research/tb24_haltedauern/`. Purge: der Rand vor der Falte
   fällt aus dem Training. Embargo: nach dem Ende einer Falte fällt dieselbe
   Länge aus dem Training aller **späteren** Falten — sonst lernt Falte *f+1*
   auf Positionen, die in Falte *f* noch offen waren.
6. **Faltenlänge ein Jahr, zwei Jahre bei unter 30 gefundenen Trades je
   Jahr.** Welche Bots das trifft, steht vorher fest (5.4).
7. **Die letzte Falte wird NICHT selektiert.** Sie ist die
   **Bestätigungsperiode**: einmal ausgewertet, nachdem die Auswahl steht,
   berichtet wie sie ausfällt. Kein Veto, aber die einzige Zahl ohne
   Selektion. **Und sie wächst jeden Monat.**
8. **Falten ohne Trade zählen mit Sharpe 0.** *„Auslassen belohnt Sätze, die
   in schweren Jahren nicht handeln."*

Zu 8 eine Eigenschaft, die auffallen sollte, bevor sie jemand für einen
Fehler hält: die Selektionsstatistik ist ein **Median**. Bei sieben
Selektionsfalten verschiebt eine einzelne gesetzte Null ihn oft gar nicht.
Das ist kein Grund, die Regel wegzulassen — sie wirkt, sobald mehrere Falten
leer bleiben, und das ist genau der Fall, den sie treffen soll.

### 5.2 Der Go-Live-Schnitt

**`2026-09-01`, ausschliesslich.** Alle neun Bots laufen seit Anfang
September 2026 im Paper-Trading; die Kursdateien dieses Repos enden am
2026-09-01 (Aktien) bzw. 2026-08-31 (Krypto). Alles davor ist
Backtest-Material, alles ab diesem Tag ist Forward-Test und geht in **keine**
Selektion ein — auch nicht in die Bestätigungsperiode.

### 5.3 Krypto: Platzhalter mit Regel

> ⚠️ **ERSETZT durch Abschnitt 15 (Registernachtrag TB-36, 15.09.2026), Registertext 3 und 4.**
> Der Text bleibt hier stehen — der Verlauf soll lesbar bleiben; das ist der
> Sinn eines Registers. Massgeblich ist der Nachtrag.
> Der Platzhalter ist eingelöst: die Krypto-Faltenpläne stehen im Nachtrag mit
> Jahreszahlen. Die hier zitierte Regel („mindestens vier Jahre Kursdaten je
> Symbol", point-in-time-Ausschluss) gilt **nicht mehr** — es gibt kein
> Mindesttraining, und kein Symbol wird aus einer Falte ausgeschlossen.

Die Kursdaten dieses Repos beginnen für Krypto am **2021-09-01**. Nach vier
Jahren Mindesttraining blieben **zwei** Testfalten — zu wenig für einen
Median über Falten. **TB-31** lädt die Historie über `/api/v3/klines` zurück.

**Der Krypto-Faltenplan wird geschrieben, sobald TB-31 gemeldet hat, ab wann
die Daten je Symbol reichen.** Bis dahin steht hier die Regel:

> Erste Testfalte ist das erste volle Kalenderjahr, vor dem **je Symbol**
> mindestens vier Jahre Kursdaten liegen, frühestens 2019. Danach lückenlose
> Falten der jeweiligen Länge bis zum Go-Live-Schnitt; die letzte Falte ist
> die Bestätigungsperiode. Ein Symbol geht in eine Falte nur ein, wenn seine
> Kursdaten mindestens vier Jahre vor Faltenbeginn einsetzen
> (point-in-time).

`auswertung.py` weigert sich, einen Bot mit Platzhalter-Faltenplan
auszuwerten — es gibt dann keine Zahl, die so tut, als gäbe es eine.

### 5.4 Welche Bots Zweijahres-Falten bekommen

Gerechnet aus den **gefundenen** Trades je vollem Kalenderjahr
(`research/tb24_haltedauern/daten/<bot>_alle_trades.csv`). Gefunden, nicht
ausgeführt: ob ein Trade ausgeführt wird, hängt am Positionslimit — und das
ist in diesem Lauf ein Rasterparameter. Eine Faltenlänge, die vom
Positionslimit abhinge, wäre keine Festlegung vor dem Lauf.

Angeschnittene Randjahre zählen nicht mit; sie zögen die Trades je Jahr nach
unten und schöben einen Bot fälschlich in die Zweijahres-Falten.

**Ergebnis: genau ein Bot.** `elliott_wave` liegt bei **26,0** gefundenen
Trades je Jahr und bekommt Zweijahres-Falten; die übrigen acht liegen
zwischen 50,9 und 1.202,2. Die Zahlen stehen in der Faltenplan-Tabelle in
Abschnitt 3.

---

## 6. Die Plateau-Regel

> Gewinner ist **nicht das Maximum**, sondern der Rasterpunkt, dessen
> **Nachbarschaft** (Punkte, die sich in genau **einer** Dimension um eine
> Stufe unterscheiden) den höchsten **Mittelwert** der Selektionsstatistik
> hat. Ein Punkt mehr als **50 %** über dem Nachbarschaftsmittel ist eine
> **Spitze** und wird markiert.

Zwei Lesarten mussten festgelegt werden, weil sie sonst schweigend
auseinanderlaufen:

**Das Plateau-Mittel zählt den Punkt selbst mit** — Mittelwert über
`{x} ∪ N(x)`. Der Punkt ist der Punkt, der gespielt wird; ein Punkt mit
hervorragenden Nachbarn und katastrophalem eigenem Wert darf nicht gewinnen.

**Der Spitzentest vergleicht ohne den Punkt selbst** — `M` = Mittel über
`N(x)` ohne `x`. Die Frage ist, ob der Punkt aus seiner Umgebung *herausragt*;
ein Punkt, der in seiner eigenen Vergleichsgrundlage steckt, dämpft genau
das, was gemessen werden soll. Formal:

```
x ist eine Spitze  ⟺  S(x) − M > 0,5 · |M|
```

Für `M > 0` ist das wörtlich „mehr als 50 % über dem Nachbarschaftsmittel".
Für `M ≤ 0` ist es dieselbe Bedingung, weiterhin monoton und definiert — die
Formel hat **keinen undefinierten Fall**. Ist `N(x)` leer, ist `x` keine
Spitze: aus nichts kann nichts herausragen.

**Zellen, in denen die Strategie nicht definiert ist, existieren nicht.** Bei
`t3_supertrend` sind das alle Zellen mit `t3_fast_length ≥ t3_slow_length`;
sie können weder gewinnen noch in ein Nachbarschaftsmittel eingehen. Von den
4 × 4 = 16 Längenpaaren bleiben 6, die Zellenzahl fällt entsprechend von
1.024 auf 384.

**Die Nachbarschaft ist geometrisch, nicht zulässigkeitsgefiltert.** Ein
unzulässiger Nachbar geht in das Plateau-Mittel ein, denn die Plateau-Regel
misst die *Glattheit der Fläche*, nicht die Zulässigkeit. **Gewinnen** kann
nur ein zulässiger Punkt.

**Gleichstand** wird reproduzierbar aufgelöst: erst höhere eigene Statistik,
dann der alphabetisch erste Zellenname. Ein Zufall wäre hier eine Wahl, die
in keinem N auftaucht.

---

## 7. Die Abbruchkriterien

Ein Bot bleibt **nicht**, wenn für den Plateau-Gewinner gilt:

| | |
|---|---|
| **(a)** | Falten-Median des Netto-Sharpe **≤ 0** |
| **(b)** | **Kein** Parametersatz erfüllt die Drawdown-Bedingung in allen Falten |
| **(c)** | **Beta-Bereinigung:** Netto-Alpha gegen das gleichgewichtete point-in-time-Universum **≤ 0 UND** Calmar unter dem der konstanten Exposure |
| **(d)** | Der Gewinner ist eine **Spitze** **und** der beste Nicht-Spitzen-Punkt erfüllt (a) |

Präzisierungen, die das eingefrorene Skript umsetzt:

* **(b) und der Gewinner.** Gewinnen kann nur ein zulässiger Punkt. Ist keiner
  zulässig, greift (b); berichtet wird dann der Plateau-Gewinner über *alle*
  Zellen, ausdrücklich mit der Markierung **„nicht zulässig"**.
* **(c), erste Hälfte.** Kleinste Quadrate auf den **Tagesrenditen** des
  Gewinners über die Selektionsfalten gegen die Tagesrenditen des
  gleichgewichteten point-in-time-Universums; `alpha` annualisiert. Beide
  Reihen werden auf gemeinsame Tage gebracht; weniger als drei gemeinsame
  Tage sind ein Abbruch, keine Annahme.
* **(c), zweite Hälfte.** „Konstante Exposure" ist die statische
  Benchmark-Position in Höhe der mittleren Exposure des Gewinners über
  dieselben Tage. Verglichen wird Calmar gegen Calmar.
* **(c) verlangt BEIDES.** Ein Satz mit `alpha ≤ 0`, aber besserem Calmar
  fällt **nicht** durch. `test_vorregistrierung.py` Teil E prüft genau diese
  Gegenprobe.
* **(d).** „Der beste Nicht-Spitzen-Punkt" ist der zulässige Nicht-Spitzen-Punkt
  mit dem höchsten Plateau-Mittel.
* **Calmar bei Drawdown 0** ist 0,0, nicht unendlich — sonst gewönne ein
  Satz, der gar nicht handelt.
* **Sharpe ohne Zinsabzug.** Eine Zinsannahme wäre eine weitere Wahl.

### 7.1 Die drei Regeln für mehrere Ausfälle — wörtlich

- ⚠️ **Die Anzahl ausscheidender Bots ist KEIN Grund, eine Schwelle zu
  ändern.**
- Das **Kapital** geht in eine **statische Benchmark-Position** in Höhe des
  mittleren Exposures — nicht in Kasse, nicht zu den Überlebenden.
- Der Bot läuft **als Schatten weiter**, kehrt nur über einen **neuen
  vorregistrierten Lauf mit veränderter Hypothese** zurück. **Kein „vorerst
  behalten".**

Alle drei stehen als Zeichenketten in
`research/vorregistrierung/auswertung.py::kapitalregel` und werden am Ende
jeder Bleibt-Geht-Liste ausgegeben — auch dann, wenn kein Bot ausscheidet.

---

## 8. Die Beurteilung — und die Regel, dass alles berichtet wird

Berichtet wird je Bot, unabhängig davon, ob er bleibt oder geht:

| Kennzahl | Quelle |
|---|---|
| Netto-Sharpe, Median über die Selektionsfalten | Selektionsstatistik |
| Netto-Sharpe je Falte | Rohergebnisse |
| Netto-Calmar über die Selektionsfalten | Tagesreihe des Gewinners |
| Mittelwert der **drei tiefsten** Falten-Drawdowns | Rohergebnisse |
| Kapital-Drawdown je Falte | Rohergebnisse |
| Falten ohne Trade | Rohergebnisse |
| Alpha (p. a.) und Beta gegen das point-in-time-Universum | Beta-Bereinigung |
| Rendite, Drawdown und Calmar der **konstanten Exposure** | Beta-Bereinigung |
| **Zufalls-Timing:** 95. Perzentil bei gleicher Zeit im Markt | siehe unten |
| Markierungen: Spitze, Kante, nicht zulässig, ohne Limitachse | Plateau-Regel |
| Verletzungen des Risikoappetits (−30 % je Falte) | Festlegung 6 |
| N_eff, N_nominal, 2 × N_nominal und die drei DSR-Werte | N-Buchführung |
| Bestätigungsperiode: Sharpe, Rendite, Drawdown, Trades | zuletzt |

**Die Regel: alle werden berichtet, auch die unangenehmen.** Sie steht auf
der Sperrliste. `auswertung.py` hat keinen Schalter, der eine Zeile
unterdrückt.

### 8.1 Der Zufalls-Timing-Test

Die Exposure-Reihe des Parametersatzes wird **zyklisch verschoben** und auf
die Benchmark-Tagesrenditen gelegt: Zeit im Markt, Exposure-Verteilung und
Zahl der Positionstage bleiben Balken für Balken erhalten, allein die **Lage**
ändert sich. Gerechnet werden **alle** nichttrivialen Verschiebungen — kein
Ziehen, kein Startwert, keine Wahl. Berichtet wird das **95. Perzentil** der
so erzeugten Renditen gegen die Rendite des Satzes.

Damit ist das Kriterium, das das Übergabeprotokoll für den Prüftermin des
Elliott-Aktien-Bots vorgemerkt hat (*„gleiche Zeit im Markt gegen das
95. Perzentil von Zufalls-Timing"*, Abschnitt 9 Punkt 4), erstmals als Code
vorhanden — hier als **berichtete Zeile**, nicht als Tor. Ein Tor wäre eine
dreizehnte Festlegung, und die hat niemand getroffen.

*Eigenschaft, die man kennen muss:* bei **konstanter** Exposure liefert jede
Verschiebung denselben Wert, und das Perzentil ist keine Verteilung mehr. Der
Test trägt also nur, wo die Exposure über die Zeit schwankt — bei allen neun
Bots tut sie das.

---

## 9. Die DSR-Buchführung

**N = 653 plus die Zellen dieses Laufs, je Bot getrennt.** Die 653 stehen in
`research/versuchsregister/REGISTER.md` (Stand 13.09.2026, Spalte
„verschiedene Kombinationen"); die Aufteilung je Bot steht in
`registerdaten.N_HISTORISCH_JE_BOT` und summiert sich auf 653.

**Drei Werte werden berichtet:**

| | woraus |
|---|---|
| bei **N_eff** | `N_historisch` + Zahl der Cluster dieses Laufs bei Korrelation **0,9** |
| bei **N_nominal** | `N_historisch` + alle Zellen dieses Laufs |
| bei **2 × N_nominal** | das Doppelte — **als Sicherheitsabstand gekennzeichnet, nicht als Wissen** |

Der dritte Wert trägt in der Ausgabe einen Satz, der genau das sagt: *„Der
Wert bei 2 × N_nominal ist ein Sicherheitsabstand, kein Wissen: er behauptet
nicht, dass doppelt so viele Versuche stattgefunden hätten."*

**Das Clustering** läuft über die Korrelation der **Falten-Sharpe-Vektoren**
zweier Zellen, transitiv fortgesetzt (Einfachverkettung). Zellen ohne
Streuung über die Falten haben keine definierte Korrelation; sie bilden
**einen** gemeinsamen Cluster — sie sind ununterscheidbar, und jede einzeln
zu zählen bliese N_eff genau in die falsche Richtung auf. Geclustert werden
nur die Zellen **dieses** Laufs; für die 653 historischen liegen keine
Falten-Vektoren vor, sie gehen ungeclustert ein.

**Die DSR ist Bericht, nicht Tor** (Festlegung 11). Sie erscheint in der
Ausgabe mit genau diesem Zusatz, und keines der vier Abbruchkriterien liest
sie.

Gerechnet wird nach Bailey/López de Prado, ohne `scipy` (das fehlt in der
Umgebung des Nutzers): Normalverteilung über `math.erf`, ihre Umkehrung nach
Acklam.

---

## 10. Die Sperrliste

Ab dem signierten Tag sind unveränderlich:

1. **Rastergrenzen und Grenzsätze** — `registerdaten.py`, Abschnitt 3 dieses
   Registers
2. **Faltengrenzen, Go-Live-Schnitt, Purge-Längen, Faltenlängen** —
   `faltenplan.py`, `ergebnisse/faltenplan.json`
3. **Selektionsstatistik, Plateau-Regel, Spitzen-Schwelle** —
   `auswertung.py`, `registerdaten.SPITZEN_SCHWELLE`
4. **Drawdown-Bedingung, `DD_Toleranz` und die vorab berechneten
   Benchmark-Drawdowns** — `benchmark.py`,
   `ergebnisse/benchmark_drawdowns.json`, **einschliesslich der
   Interpolationsregel**
5. **Abbruchkriterien und Kapitalregel** — `auswertung.py`
6. **Benchmark-Definitionen** — gleichgewichtete Tagesrenditen,
   point-in-time, `benchmark.py::bh_tagesrenditen`
7. **N-Buchführung und Clusterschwelle** —
   `registerdaten.N_HISTORISCH_JE_BOT`, `CLUSTER_SCHWELLE = 0,9`
8. **Universumsdateien und point-in-time-Regel** — `config/top25_symbols.txt`,
   `config/sp500_top150.txt`, vier Jahre Vorlauf je Symbol
   > ⚠️ Der Halbsatz „vier Jahre Vorlauf je Symbol" ist **ersetzt** (Abschnitt 15,
   > Registertext 3). Die beiden Universumsdateien selbst bleiben unverändert auf
   > der Sperrliste, jetzt mit Hash im Nachtrag.
9. **Kosten (0,30 %) und Fill-Konvention** — `TRADING_FEE_PCT = 0,1` und
   `SLIPPAGE_PCT = 0,05` je Order, Ein- und Ausstieg; Einstieg zum
   Schlusskurs des Bestätigungsbalkens
10. **Zuteilungskaskade inklusive Seed** — `shared/zuteilung.py`,
    `SEED = 20260913`
11. **Commit-Hashes von Simulation, Erkennung, Optimierern und
    Auswertungsskript** — `herkunft.py::register()` und der Repo-Commit
12. **Hash des Datenstands** — `herkunft.py::datenstand()`
13. **Die Liste der berichteten Kennzahlen und die Regel, dass alle
    berichtet werden, auch die unangenehmen** — Abschnitt 8
14. **Die Reihenfolge Selektion → Bestätigungsperiode → Bericht** — im
    Kopftext von `auswertung.py` als Ablauf festgeschrieben

Zusätzlich gilt: **Der Lauf darf nicht beginnen, bevor die beiden Bug-Fixes
aus Abschnitt 11 eingebaut sind.**

*Tatsache zu Punkt 12 (15.09.2026, TB-34):* Der Datenstand-Hash hat sich
**vor** jedem Selektionslauf geändert — durch den nativen Neuaufbau der 72
Krypto-Kursdateien (`shared/kursdaten_neuaufbau.py`, Stand 2026-09-15
09:51:31 UTC, Sicherung `data_sicherung/2026-09-15_115131`). Vorher
`6258cbc38872f9d6dd2b0315e9ea15a68148b133e97996cf5dbb18c82758c1f0`, nachher
`97498f14527651a28323c1f273be24d2252595840b1b57364d263d7ff87eef1c` (je 242
Dateien). Das ist **kein Amendment**: es gab keinen Lauf, dessen Ergebnisse
davon berührt wären; genau deshalb kam TB-34 vor TB-30b. Die Aktiendateien
sind unverändert. Der daraus folgende Krypto-Faltenplan (5.3) ist gerechnet
(`research/krypto_historie/daten/faltenplan_nach_tb34.json`), aber **nicht**
eingetragen — Lesart von „je Symbol" und Eintrag bleiben Betreiberentscheidung.

*Fortschreibung derselben Tatsache (15.09.2026, nach dem Lauf):* Der oben
genannte Stand `97498f14…` bestand nur kurz. Anschliessend wurden die **19
verwaisten `*_15m.csv`** aus `data/` entfernt — Reste eines verworfenen
15-Minuten-Versuchs, von **keinem** Programm gelesen (geprüft über den gesamten
Python-Quelltext; die einzigen beiden Fundstellen sind `shared/zeitabdeckung.py`
und ihr Test, und dort steht `_15m` als **Beispiel für einen nicht geführten
Zeitrahmen**). Beides zusammen liegt in Commit `90e3cbd`.

**Der Datenstand, der für den Selektionslauf gilt, ist damit:**
`d9449faf51bffaaa…` bei **223** Kursdateien (223 = 72 Krypto + 150 Aktien +
`XAUTUSDT_1h`), erfasst mit `research/vorregistrierung/herkunft.py`.

*Nachtrag zu derselben Tatsachennotiz (18.09.2026, TB-48 — angehängt, nichts
entfernt):* ⚠️ **Ab Registertext 5a (neu, Abschnitt 17.1) bezeichnet
`d9449faf…` den Kursdatenteil des Snapshots — den Datenstand-Hash —, nicht den
Snapshot selbst; der Snapshot-Hash ist ein eigener Wert.** **Der hier
festgehaltene Wert bleibt in jedem Wort gültig**: er misst den Bestand, und den
misst er weiterhin. Benannt wird nur sein Referent. Beide Werte nebeneinander
in **17.9**.

*Warum beides in einem Zug geschah:* Die 19 Dateien waren im Hash mitgezählt.
Sie später zu entfernen hätte einen **zweiten** Hash-Wechsel erzeugt — und wäre
er nach dem Selektionslauf erfolgt, wäre er kein Tatsachenvermerk mehr gewesen,
sondern ein Bruch der Sperrliste. Es gibt daher genau **einen** Übergang:
`6258cbc3…` (242 Dateien) → `d9449faf…` (223 Dateien), vollzogen vor jedem Lauf.

### 10.1 Die Amendment-Regel

> Ein **Bug-Fix ist ein Amendment**: dokumentiert, **der Lauf beginnt von
> vorn**, und die Ergebnisse davor werden **nicht** neben die danach gelegt.
> *Wer Vorher und Nachher vergleicht, hat wieder eine Wahl.*
>
> **Erlaubt sind nur** Laufzeit-Optimierungen mit **bitidentischen**
> Ergebnissen — nachzuweisen über `shared/determinismus.py` und einen
> Stichproben-Hash-Vergleich.

Ein Amendment wird im append-only-Protokoll
(`ergebnisse/herkunft_protokoll.jsonl`) mit eigenem Anlass eingetragen. Der
Register-Hash ändert sich dabei zwangsläufig, und genau daran ist im
Protokoll zu sehen, dass zwei Läufe **nicht** unter derselben
Vorregistrierung liefen.

---

## 11. Voraussetzungen des Laufs (zwei Bug-Fixes, beide TB-30b)

TB-30a darf `strategies/*/equity_simulation.py`,
`strategies/*/multi_symbol_optimise.py` und
`strategies/*/multi_symbol_walk_forward.py` **nicht** anfassen. Die
Entscheidungen sind hier getroffen und die Mechanik ist hier gebaut und
geprüft; der Einbau ist TB-30b.

### 11.1 AB2/U5 — der stillschweigend übersprungene BTC-Regimefilter

`t3_supertrend` überspringt seinen BTC-Regimefilter **stillschweigend**, wenn
`BTCUSDT` fehlt; `volatility_breakout_crypto` bricht ab.

**Entscheidung: abbrechen.** Ein Lauf, in dem ein Bot still ohne Filter
rechnet, ist nicht deterministisch — dieselben Parameter liefern je nach
Inhalt von `data/` verschiedene Ergebnisse, und nichts in der Ausgabe sagt,
welcher Fall vorlag. Der Filter ist zudem keine Nebensache: beim T3-Bot senkt
er den Max Drawdown von −31,2 % auf −22,2 % (Protokoll 3.2). Ein Lauf ohne
ihn beschreibt eine **andere Strategie**.

Die Wache steht fertig und geprüft in **`shared/regimewache.py`**
(`shared/test_regimewache.py`: 16 Prüfungen). Einzubauen an drei Stellen:

| Datei | heute | einzubauen |
|---|---|---|
| `strategies/t3_supertrend/equity_simulation.py:77` | `if "BTCUSDT" in all_data:` ohne Gegenzweig | `btc_daten(all_data, bot="t3_supertrend", holen="python3 fetch_4h_data.py")` |
| `strategies/t3_supertrend/multi_symbol_optimise.py:123` | dito | dito |
| `strategies/volatility_breakout_crypto/equity_simulation.py:103` | bricht bereits ab | auf die gemeinsame Wache umstellen |

`regimewache.pruefe_einbau()` beantwortet maschinell, ob der Einbau erfolgt
ist. Solange er es nicht ist, darf der Lauf nicht starten.

### 11.2 Agent 2 — Auswahl auf dem führenden Mass

Agent 2 (`shared/param_search_agent.py`) optimierte seit dem 13.09. auf dem
**chronologischen** Drawdown, und der Satz *„es gilt das chronologische"* war
im Prompt fest verdrahtet — seit Festlegung 1 falsch.

**Umgestellt, in `shared/`, ohne Bot-Code anzufassen.** An die Stelle des
fest verdrahteten Satzes tritt eine dreistufige Kaskade
(`ZIELMASS_KASKADE`), die in jeder Stufe sagt, welches Mass gilt und warum
nicht das führende:

1. `robustness_score_kapital` auf `max_drawdown_kapital_pct` — **das führende
   Mass**
2. `robustness_score_chronologisch` — der Stellvertreter
3. `robustness_score` — der Notweg

**Heute greift Stufe 2**, weil `multi_symbol_optimise.evaluate_combination_multi`
den Kapital-Drawdown noch nicht mitliefert. Das nachzurüsten ist TB-30b. Der
Unterschied zu vorher ist nicht die Zahl, sondern dass der Agent den Ersatz
**als Ersatz ausweist** statt ihn als Zielgrösse zu behaupten — und dass er
von selbst umschaltet, sobald das Feld da ist, ohne dass jemand daran denken
muss. Geprüft in `shared/test_agent2_kapitalmass.py` (34 Prüfungen); die 41
Prüfungen aus TB-22 bestehen unverändert.

### 11.3 Zwei Achsen brauchen eine Durchreichung

* `rsi2_mean_reversion`: `SMA_TREND_PERIOD = 200` ist in
  `backtest_rsi2.py` eine Konstante und muss Parameter werden — sonst gilt
  für die Aktien- und die Krypto-Variante nicht dieselbe Regel.
* `volatility_breakout` und `volatility_breakout_crypto`:
  `BB_SQUEEZE_PERCENTILE` und `BB_LOOKBACK` stehen in `live_params.py`, aber
  nicht im Optimierer.

---

## 12. Der Vollständigkeitstest

**Ja — das Auswertungsskript liess sich fertig schreiben, ohne ein Ergebnis
gesehen zu haben.** Es läuft gegen erzeugte Beispieldaten mit frei
erfundenen Werten (`beispieldaten.py`), und `test_vorregistrierung.py` prüft
jede Regel einzeln am Ablauf: 150 Prüfungen, davon acht Mutationsproben.

Fertigschreiben hiess allerdings an **sieben** Stellen: eine Lesart
festlegen, wo die Festlegungen zwei zuliessen. Jede steht oben im Text; hier
die Liste, damit keine davon unbemerkt bleibt.

| # | Offene Stelle | Festgelegte Lesart | Abschnitt |
|---|---|---|---|
| 1 | Trägt `DD_Toleranz` ein Exposure-Argument? | Ja — sonst passt Festlegung 5 nicht zu Festlegung 4 | 4.2 |
| 2 | Zählt das Plateau-Mittel den Punkt selbst mit? | Ja | 6 |
| 3 | Zählt der Spitzentest den Punkt selbst mit? | Nein | 6 |
| 4 | Was ist eine Spitze, wenn das Nachbarmittel ≤ 0 ist? | `S(x) − M > 0,5·|M|`, total definiert | 6 |
| 5 | Muss der Gewinner zulässig sein, und was gilt bei (b)? | Ja; bei (b) Bericht des Gesamt-Gewinners mit Markierung | 7 |
| 6 | Gehen unzulässige Nachbarn ins Plateau-Mittel ein? | Ja — die Regel misst Glattheit, nicht Zulässigkeit | 6 |
| 7 | Wie wird Gleichstand aufgelöst? | Statistik, dann Zellenname — kein Zufall | 6 |

Zwei weitere Stellen betreffen **nicht** die Auswertung, sondern den Lauf,
und sind deshalb als Voraussetzung eingetragen statt als Lesart: die beiden
Bug-Fixes aus Abschnitt 11.

**Was die Vollständigkeit trägt, ist nicht die Länge dieses Dokuments,
sondern dass `auswertung.py` keinen Schalter hat.** Es gibt keine Option, die
eine Schwelle verschiebt, keine, die einen Bot ausnimmt, und keine, die eine
Kennzahl unterdrückt. Wo die Rohergebnisse den Vertrag verletzen, bricht es
ab — es füllt nichts auf und überspringt nichts.

---

## 13. Die Verankerung

| | Stand |
|---|---|
| **Das Urteil ist Code** — `auswertung.py`, eingefroren, 150 Prüfungen | **erledigt** |
| **Herkunft in jeder Ergebnisdatei** — Commit-, Datenstand- und Register-Hash, append-only-Protokoll mit Kettenhash | **erledigt** (`herkunft.py`) |
| **Signierter Tag** (GPG) | **offen — Betreiber**, Anleitung im Testauftrag |
| **Externer Zeitanker** (OpenTimestamps) für Register-Hash + Datenstand-Hash | **offen — Betreiber**, Anleitung im Testauftrag |

`python3 research/vorregistrierung/herkunft.py` meldet den Stand aller vier.
Die beiden offenen brauchen den GPG-Schlüssel bzw. den Netzzugang des
Betreibers; die kopierbare Anleitung steht in
`docs/TESTAUFTRAG_TB-30a_vorregistrierung.md`, Schritte 8 und 9.

---

## 14. Der Nulltest S-E1

`S-E1` (Turn-of-Month) hat einen **eigenen** Registereintrag:
[`docs/VORREGISTRIERUNG_S-E1_nulltest.md`](VORREGISTRIERUNG_S-E1_nulltest.md).

Er ist von „Kandidaten nach Rang 3" ausgenommen, berührt weder die neun Bots
noch das Mass in Reparatur und prüft **den Weg**, nicht die Strategie.

---

*Erstellt in TB-30a. Kein Selektionslauf, keine Parameterübernahme, keine
Änderung an Bot-Code.*

---

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

*Formel für den Falten-Sharpe: Mittel / Standardabweichung der täglichen
Netto-Renditen der Falte × √252 (Krypto: √365 auf Kalendertagen).*

> **Tatsachennotiz zu 1c.** Eine Fassung „mit Mindestzahl 10 Trades" hat in
> **diesem** Dokument nie gestanden — sie stammt aus einer früheren
> Beratungsrunde und war nie eingetragen (geprüft über den gesamten Quelltext
> des Registers und `research/vorregistrierung/`). Der Klammerzusatz bleibt
> trotzdem wörtlich stehen: er sagt, gegen welche Fassung entschieden wurde.
> 1c ist damit kein Widerruf, sondern die **Schärfung von Regel 5.1 Nr. 8**
> („Falten ohne Trade zählen mit Sharpe 0"), die hier unberührt weitergilt.

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

---

### 15.6 Registertext 4 — Falten

> **(a)** Es gibt **kein Trainingsfenster**. Selektionsfalten sind alle
> vollständigen Kalenderjahre (bzw. Doppeljahre) vom ersten Jahr, in dem am 1.
> Januar Daten für Universum und Indikator-Vorlauf vorliegen, bis zum letzten
> vollständigen Jahr vor Go-Live.
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

## 16. Registernachtrag (TB-41, 16.09.2026)

### 16.0 Was das ist — und was es ausdrücklich nicht ist

**Das ist kein Amendment.** Es hat **kein Selektionslauf stattgefunden**: kein
Raster gerechnet, kein Parametersatz bewertet, kein Ergebnis erzeugt — derselbe
Stand wie am Kopf dieses Dokuments und wie am Kopf von Abschnitt 15. Die
Sperrliste (Abschnitt 10) gilt laut ihrem eigenen ersten Satz **„ab dem
signierten Tag"**, und der steht in Abschnitt 13 weiterhin als *offen —
Betreiber*. Es ist deshalb nichts aufzubrechen; es wird nachgetragen, bevor
gerechnet wird.

Seit TB-36 sind **zwölf weitere Festlegungen** entstanden, und **drei der
eingetragenen Tatsachennotizen haben sich als falsch erwiesen**. Dieser
Abschnitt trägt beides **in einem Zug** nach. Danach wird nichts mehr geändert,
bevor der Snapshot gezogen und der signierte Tag gesetzt ist.

**Bestehender Text wird nicht umgeschrieben.** Die betroffenen Passagen
(15.4 Registertext 2d, 15.5 Registertext 3 mit seinen Tatsachennotizen, 15.7
Registertext 5) bleiben **vollständig stehen** und tragen nur einen eingefügten
Verweis hierher. Der Verlauf soll lesbar bleiben — das ist der Sinn eines
Registers. Am Diff dieser Arbeit sind **null Zeilen entfernt**.

**Herkunft der Zahlen.**

| | |
|---|---|
| Symbolzahl je Falte, Symbole ohne Faltenevidenz | `research/universum_trockenlauf/` (TB-40), Ergebnis in `docs/ERGEBNIS_TB-40_universum_trockenlauf.md` |
| `MIN_HISTORY_*` je Bot | `strategies/<bot>/multi_symbol_optimise.py`, **gelesen** |
| Umstellungstag der Entscheidungskerze | `docs/umstellungstag_entscheidungskerze.json` (TB-38) |
| Zeilenzahl und Hash der Universumsdatei | `config/top25_symbols.txt`, `shared/symbols_config.py` |
| Datenstand | `d9449faf51bffaaa…`, 223 Kursdateien — vor und nach dieser Arbeit identisch |
| Prüfwerkzeug dieses Nachtrags | `research/registernachtrag_tb41/` |

⚠️ **Die Zahlen sind nicht abgetippt.** `research/registernachtrag_tb41/pruefe_register.py`
vergleicht die hier eingetragenen Zahlen **maschinell** gegen ihre Quelle und
meldet jede Abweichung; auf einer Maschine mit Bot-Abhängigkeiten vergleicht es
zusätzlich gegen einen frischen Trockenlauf des Laufcodes.

---

### 16.1 Die drei falschen Tatsachennotizen — korrigiert

#### 16.1.1 Symbolzahl je Falte (Tatsachennotiz zu Registertext 3b)

**Gemessen in TB-40 durch Trockenlauf des Laufcodes** — der Loader des Bots
entscheidet, nicht ein nachgebautes Werkzeug. **Acht der neun Reihen** in der
Tabelle von 15.5 sind **zu hoch**; `elliott_wave` stimmt. **Es kommt nirgends
ein Symbol hinzu** — in keiner Falte eines Bots: die gemessenen Mengen sind
überall Teilmengen der eingetragenen (F ⊆ H ⊆ A).

> **Die Symbolzahl je Falte** (Tatsachennotiz zu 3b, **ersetzt die Fassung aus
> 15.5**; Lesart H, gemessen am Loader):
>
> | Bot | Symbolzahl je Selektionsfalte | Bestätigung | Universum |
> |---|---|---:|---:|
> | `elliott_wave` | 6 / 13 / 13 | 18 | 24 |
> | `t3_supertrend` | 3 / 6 / 9 / 13 / 13 / 13 / 17 | 18 | 24 |
> | `rsi2_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
> | `turtle_soup_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
> | `volatility_breakout_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
> | `elliott_wave_stocks` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
> | `rsi2_mean_reversion` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
> | `turtle_soup_stocks` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
> | `volatility_breakout` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
>
> `elliott_wave` hat Doppeljahr-Falten; seine drei Zahlen stehen für 2019–2020,
> 2021–2022 und 2023–2024. Die vier Aktien-Bots teilen eine Reihe, weil sie
> dieselbe Symbolliste und dieselbe Schranke haben.

**Was die Korrektur an den Regeln ändert — und was nicht:**

* **Regel 4b (mindestens 3 Selektionsfalten) bleibt für alle neun erfüllt.**
  Kein Bot verliert eine Falte; keine Falte ist leer. Regel 4c
  („unterbestimmt") greift weiterhin für keinen der neun.
* ⚠️ **`t3_supertrend` hat in seiner Falte 2019 nur drei Symbole.** Die Falte
  zählt — Registertext 3b (a) unten sagt das jetzt ausdrücklich —, aber sie ist
  dünn, und das gehört berichtet, nicht versteckt.
* **Die Bestätigungsperiode wird bei sechs Bots kleiner** (Krypto-Tagesbots
  23 → 20, `t3_supertrend` 23 → 18, Aktien-Bots 150 → 147). Das ist keine
  Verschlechterung der Strategie, sondern die Korrektur einer Fehlmessung.

#### 16.1.2 „Symbole ohne Faltenevidenz" sind Listen **je Bot**

Heute steht in 15.5 **eine Liste je Markt** (krypto 6, aktien 1). Das ist
falsch: was der Loader nicht lädt, liefert auch keine Evidenz — und die Loader
haben **fünf verschiedene Schranken**. Die Listen fallen deshalb je Bot
auseinander.

> **Symbole ohne Faltenevidenz** (Tatsachennotiz zu 3b, **ersetzt die Fassung
> aus 15.5**; Lesart H, je Bot):
>
> | Bot | # | Symbole ohne Faltenevidenz |
> |---|---:|---|
> | `elliott_wave` | 11 | `BMTUSDT`, `ENAUSDT`, `ENSOUSDT`, `PEPEUSDT`, `PROMUSDT`, `PUMPUSDT`, `SUIUSDT`, `TRUMPUSDT`, `UUSDT`, `WLDUSDT`, `ZKCUSDT` |
> | `t3_supertrend` | 7 | `BMTUSDT`, `ENAUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT` |
> | `rsi2_crypto` | 6 | `BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT` |
> | `turtle_soup_crypto` | 6 | `BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT` |
> | `volatility_breakout_crypto` | 6 | `BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT` |
> | `elliott_wave_stocks` | 5 | `APP`, `CEG`, `GEV`, `HOOD`, `SNDK` |
> | `rsi2_mean_reversion` | 5 | `APP`, `CEG`, `GEV`, `HOOD`, `SNDK` |
> | `turtle_soup_stocks` | 5 | `APP`, `CEG`, `GEV`, `HOOD`, `SNDK` |
> | `volatility_breakout` | 5 | `APP`, `CEG`, `GEV`, `HOOD`, `SNDK` |
>
> Für diese Symbole gilt der gewählte Parametersatz live **ohne
> Faltenevidenz**. Das ist keine Nachlässigkeit, sondern die Kehrseite von 3d:
> wer sie hätte, hätte ein point-in-time-Universum und damit einen anderen Lauf.

⚠️ Bei den Aktien-Bots waren es **eingetragen `SNDK` allein**, gemessen sind es
**fünf**. Die vier zusätzlichen (`APP`, `CEG`, `GEV`, `HOOD`) sind nicht neu im
Universum — sie fallen an `MIN_HISTORY_DAYS = 1825` heraus, und das war in der
alten Notiz nicht abgebildet, weil die alte Messung diese Schranke nicht kannte.

#### 16.1.3 Die Klammer in 15.5 rechnet falsch — Rechenweg korrigiert

In der Tabelle *„Die Universumsdateien"* steht für `config/top25_symbols.txt`
**„24 (26 Zeilen abzüglich `XAUTUSDT`, `PAXGUSDT`)"**.

**Ergebnis 24 richtig, Rechenweg falsch.** Nachgemessen an der Datei mit dem
**eingetragenen** Hash `3afc95a4…`:

* Sie hat **25** nichtleere Zeilen, nicht 26.
* **`PAXGUSDT` steht nicht darin.** `shared/symbols_config.py:23` führt beide
  Namen in `EXCLUDE_SYMBOLS`, aber nur `XAUTUSDT` kommt in der Datei vor und
  wird tatsächlich gestrichen.

> **Korrigierter Rechenweg** (**ersetzt die Klammer in der Tabelle von 15.5**,
> die dort unverändert stehen bleibt):
>
> | Markt | Datei | SHA-256 | Symbole |
> |---|---|---|---:|
> | krypto | `config/top25_symbols.txt` | `3afc95a4f6b5ebc3a8f7bb7854b5dd59c4ecc4e3d86aa7b93c08066a3fccf810` | **24 (25 Zeilen abzüglich `XAUTUSDT`)** |
> | aktien | `config/sp500_top150.txt` | `6acba892f38e998cf43ae9e5594c4707945143aba481429c44a5c6005339f607` | 150 |
>
> Der Hash ist geprüft und unverändert — es ist **dieselbe Datei**, nur die
> Beschreibung daneben stimmte nicht.

---
#### 16.1.4 Eine vierte, in dieser Arbeit gefundene: „die fünf Werte"

Die Aufgabenstellung nennt drei falsche Tatsachennotizen. Beim maschinellen
Nachzählen ist eine **vierte** aufgefallen, und sie wird hier genannt statt
stillschweigend geglättet: Registertext 3b (b) spricht von **„den fünf
Werten"** von `MIN_HISTORY_*`. **Gezählt sind es vier** — 17 520 · 730 · 500 ·
1 825 — in zwei Einheiten. Die Zahl stammt aus TB-40 und ist dort schon falsch.

**Der Wortlaut bleibt unverändert**, weil er der registrierte ist; die
Tatsachennotiz daneben (in 16.7) sagt, was gezählt wurde. Das ist derselbe
Umgang wie bei 16.1.3: **Rechenweg korrigieren, Wortlaut stehen lassen.**

---

### 16.2 Die Lesart, die gilt: **H**

**Es gilt Lesart H: „an mindestens einem Handelstag der Falte handelbar."**

⚠️ **Das ist eine Bestätigung, keine Änderung** — es ist der Wortlaut von
Registertext 3b. TB-40 hat zusätzlich die Alternative **F** („am Faltenbeginn
geprüft") gemessen, weil die TB-40-Aufgabenstellung sie verlangte. Beides gehört
ins Journal, **in dieser Reihenfolge:**

1. **H wurde behalten, weil es registriert war.** Zum Zeitpunkt der Entscheidung
   war bekannt, dass F `elliott_wave` auf **2 von 3** Falten drücken (erste
   Falte: 0 Symbole) und ihn damit nach Regel 4c „unterbestimmt" machen würde.
   *Eine Wahl nach dem Ergebnis wurde bewusst vermieden.* Die Reihenfolge ist
   der Punkt: erst gilt, was registriert war; die Sachfrage kommt danach.
2. **H ist zusätzlich in der Sache richtig.** F beschreibt eine Strategie, die
   der Bot nicht handelt: ein Symbol, das im März handelbar wird, wird ab März
   gehandelt — F würde es für das **ganze Jahr** streichen. Die Falte ist ein
   Berichtszeitraum, kein Zulassungsstichtag.

Die Zahlenreihe unter F steht vollständig in
`docs/ERGEBNIS_TB-40_universum_trockenlauf.md`. Sie ist **nicht** eingetragen
und hat keinen Weg ins Urteil.

---

### 16.3 Registertext 5 — Datenstand *(ersetzt die Fassung aus 15.7 vollständig)*

> **(a)** Es gibt **zwei Kursdatenbestände**. `data/live/` wird täglich vor den
> Bot-Läufen von einem Cron aktualisiert und auf Frische geprüft (letzte
> abgeschlossene Kerze vorhanden, keine Teilkerze); **Forward-Tests und der
> Backtester-Vergleich (Registertext 7) lesen ausschliesslich daraus**.
> `data/snapshots/<hash>/` ist eine einmal erzeugte, danach **unveränderliche**
> Kopie; **der Selektionslauf liest ausschliesslich daraus**. Kein Modul eines
> Laufs ruft Kurse über das Netz ab.
>
> ⚠️ **ERSETZT durch Abschnitt 17 (Registernachtrag TB-48, 18.09.2026), 17.1.**
> Registertext 5a führt dort **Bestand** und **Snapshot** als Rollen statt als
> Pfade (`data/` und `snapshots/<hash>/` nur noch als Tatsachennotiz), nennt den
> Umfang der Eingaben (⭐ neben den Kursdateien **genau zwei**:
> `config/top25_symbols.txt`, `config/sp500_top150.txt`) und trennt
> **Snapshot-Hash** und **Datenstand-Hash**. Der Kern dieses Absatzes — der
> Selektionslauf liest ausschliesslich den Snapshot, kein Modul ruft Kurse über
> das Netz ab — **bleibt unverändert gültig** und ist dort wörtlich
> übernommen. ⭐ Neu hinzu kommt die Ausnahme `rand_erste` (17.3).
>
> **(b)** **Der Registerhash bezeichnet den Snapshot.** Der Live-Bestand wird
> nicht registriert; jede Auswertung, die ihn liest, protokolliert den Hash
> dessen, was sie gelesen hat, im Ergebnis.
>
> ⚠️ **PRÄZISIERT durch Abschnitt 17, 17.9** — nicht ersetzt. Als dieser Satz
> geschrieben wurde, gab es **einen** Hash. Seit TB-47 gibt es **zwei**;
> `d9449faf…` ist der **Datenstand-Hash** (der Kursdatenteil), der
> **Snapshot-Hash** ist ein eigener Wert
> (`4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608`,
> TB-47-Maclauf). Der Satz selbst bleibt gültig; 17.9 sagt nur, **welcher**
> Hash gemeint ist.
>
> **(c)** Der Snapshot wird **am Tag des signierten Tags** aus `data/live/`
> gezogen, danach nicht mehr. **Ein zweiter Snapshot ist ein neuer Lauf.**
>
> ⚠️ **ERSETZT durch Abschnitt 17 (Registernachtrag TB-48, 18.09.2026), 17.2.**
> „Am Tag des signierten Tags" liess die **Reihenfolge** offen. Korrigiert
> gilt: **der Snapshot wird VOR dem signierten Tag gezogen, und der Tag
> referenziert seinen Hash.** Der zweite Satz — ein zweiter Snapshot ist ein
> neuer Lauf — bleibt unverändert.
>
> **(d)** **Alle Daten- und Bot-Cronjobs laufen in UTC** (`TZ=UTC` in der
> Crontab oder launchd mit UTC), in der Reihenfolge Datenaktualisierung →
> Frischeprüfung → Bots.

**Dazu eine Prüfung, kein Abbruchkriterium:** Der Selektionslauf auf dem
Snapshot muss **auf einer zweiten Maschine bitidentisch reproduzieren**. Tut er
das nicht, ist der Snapshot unvollständig — ein Modul liest von woanders. *Das
ist vor dem Tag zu finden, nicht danach.* Die Prüfung erzeugt kein Urteil; sie
erzeugt einen Befund.

⚠️ **Der Umbau selbst ist nicht Teil dieses Nachtrags.** Er ist eine eigene,
grosse Aufgabe: **101 Module lesen heute `data/`.** Hier wird nur der
Registertext eingetragen. Bis der Umbau erfolgt ist, **fallen Registertext und
Umsetzung auseinander** — siehe 16.11, Zeile 1.

**Die alte Fassung (15.7) bleibt gültig, soweit sie Tatsachen festhält**, die
der neue Text nicht widerruft: der Hash über Binance-Dateien ist stabil, der
über yfinance-Dateien konstruktionsbedingt nicht (`auto_adjust=True`). Genau
diese Instabilität ist der Grund, warum (a) einen unveränderlichen Snapshot
verlangt: ein Bestand, der sich bei jedem Abruf um 10⁻⁶ verschiebt, kann nicht
zugleich die Grundlage eines registrierten Laufs sein.

---

### 16.4 Registertext 6 — Budgetstufen und Zellenbudget *(neu)*

**Die Budgetstufen-Leiter stand bisher nirgends im Repo.** Das ist ein Befund
aus TB-39: eine Sitzung musste sie **nachbauen**, um mit ihr arbeiten zu können.
*Jede Aufgabe, die sie nicht vorfindet, rät sie neu — und jede rät anders.*
Dieser Registertext beendet das.

#### Die Stufen

> **(a)** Jeder Bot steht auf einer von drei Stufen: **Schatten** (läuft, kein
> Portfoliogewicht, nicht in Portfolio-Zahlen und nicht am Crash-Knopf),
> **Grundbudget** (im Buch), **Bestätigt** (im Buch, Rang-5-Gewichtung, sobald
> Netting existiert).
>
> **(b)** Nach dem Selektionslauf steht jeder Bot, der **kein** Abbruchkriterium
> erfüllt, auf **Grundbudget**; jeder, der eines erfüllt, auf **Schatten** —
> sein Budgetanteil hält die statische Benchmark-Position in Höhe seines
> mittleren Exposures. **Die Zuweisung ist Ergebnis des eingefrorenen Skripts,
> keine Lesung.**
>
> **(c)** **Aufstieg** Grundbudget → Bestätigt, geprüft am Ende jedes
> Kalenderquartals durch dasselbe Skript, frühestens nach **30 geschlossenen
> Trades und sechs Monaten** Bestätigungsperiode: Netto-Sharpe der
> Bestätigungsperiode > 0, **und** Netto-Calmar ≥ **0,5 ×** Netto-Calmar des
> Gewinners über die Selektionsfalten, **und** Max-Drawdown der
> Bestätigungsperiode nicht tiefer als die tiefste Selektionsfalte des
> Gewinners. *(30 Trades, sechs Monate und 0,5 sind **willkürlich**; 0,5 ist
> eine fremde Faustregel, keine Messung dieses Projekts.)*
>
> **(d)** **Abstieg** auf Schatten, quartalsweise: Max-Drawdown tiefer als
> **1,25 ×** die tiefste Selektionsfalte des Gewinners, **oder** Netto-Sharpe
> < 0 nach **60** geschlossenen Trades. **Rückkehr nur über einen neuen
> registrierten Lauf.**
>
> **(e)** Zwischen den Quartalsprüfungen ändert sich keine Stufe. **Kein
> Betreiberentscheid setzt eine Stufe hinauf; der Betreiber kann einen Bot
> jederzeit auf Schatten setzen (Notbremse), aber nie hinauf.**
>
> **(f)** **D5 (Echtgeld)** setzt für jeden beteiligten Bot die Stufe
> **Bestätigt seit mindestens zwei Quartalsprüfungen in Folge** voraus.

#### Das Zellenbudget

> **(g)** **Zellen sind Quelle × Anlage.** Heute:
>
> | Zelle | Bots |
> |---|---|
> | Fortsetzung × Aktien | `volatility_breakout` |
> | Umkehr × Aktien | `rsi2_mean_reversion`, `turtle_soup_stocks`, `elliott_wave_stocks` |
> | Fortsetzung × Krypto | `t3_supertrend`, `volatility_breakout_crypto` |
> | Umkehr × Krypto | `rsi2_crypto`, `turtle_soup_crypto`, `elliott_wave` |
>
> Jeder Bot gehört zu **genau einer** Zelle; **die Zuordnung steht im Register
> und ändert sich nur mit dem Bot.**
>
> **(h)** Eine Zelle ist **aktiv**, wenn mindestens ein Bot darin auf
> Grundbudget oder Bestätigt steht. **Aktive Zellen teilen das Buch zu gleichen
> Teilen.** *Gleichteilung ist willkürlich; sie ist die einzige Aufteilung, die
> kein Ergebnis verwendet.*
>
> **(i)** Innerhalb einer Zelle teilen die Bots nach **Stufenfaktor: Schatten 0,
> Grundbudget 1, Bestätigt 2** *(Faktor 2 willkürlich)*. Anteil = eigener Faktor
> / Summe der Faktoren der Zelle.
>
> **(j)** **Aufstieg:** mehr vom **Zellenbudget**; das Zellenbudget ändert sich
> nicht. **Abstieg:** Zellenbudget **bleibt**, die übrigen teilen es nach (i).
> **Wird die Zelle inaktiv, geht ihr Budget in die statische
> Benchmark-Position ihrer Anlage — nicht an andere Zellen.**
>
> **(k)** Wird eine **neue Zelle aktiv**, steigt die Zahl aktiver Zellen und
> alle Zellenanteile sinken entsprechend. **Das ist die einzige Umverteilung
> zwischen Zellen, und sie folgt aus Zulassung, nicht aus Ergebnis.**
>
> **(l)** ⭐ **Anlageklassen-Schlüssel, Betreiberentscheid vom 16.09.2026:
> Aktien 80 / Krypto 20.** Er skaliert die Zellen einer Anlage gemeinsam und
> gilt, bis Netting (Rang 5) existiert.
>
> **(m)** **Umsetzung ohne gemeinsames Konto:** Das Leiter-Skript berechnet
> quartalsweise je Bot einen Multiplikator auf dessen heutige statische
> Positionsgrösse:
>
> `m_b = (Zellenanteil × Klassenschlüssel × Bot-Anteil in der Zelle) / (1/9)`
>
> **Die Bots lesen `m_b`; sonst ändert sich nichts.**

#### ⭐ Das Prinzip, das (j) und (k) trägt

> **Die Leiter bewegt Bots. Sie bewegt keine Zellen.** Out-of-Sample-Evidenz
> über einen Bot ist Evidenz über eine **Implementierung**, nicht darüber, dass
> die Ertragsquelle seiner Zelle mehr Kapital verdient. Schrumpfte die Zelle
> beim Abstieg, würde ein Bot für das Versagen eines anderen bestraft — **und
> das Kapital ginge dorthin, wo es zufällig besser lief.**

#### Die Begründung des Schlüssels 80/20 — mit ihrer Messung

Gemessen über **2 271 gemeinsame Handelstage**, 2017-08-18 bis 2026-09-01:

| | Krypto | Aktien |
|---|---:|---:|
| Jahresschwankung | **74,7 %** | **19,6 %** |
| Verhältnis | **3,82 ×** | |
| Korrelation | **0,32** | |

**Bei 60/40 kämen 80 % des Risikos aus Krypto.** Gleicher Risikobeitrag läge bei
**79/21**; 80/20 ist die gerundete Fassung davon und als Betreiberentscheid
eingetragen, nicht als Rechenergebnis.

⚠️ **Der Ertrag wurde bewusst nicht gemessen.** Der Zeitraum enthält einen der
grössten Krypto-Aufschwünge; eine Ertragszahl daraus würde den Schlüssel nach
dem Ergebnis setzen, und genau das soll die Vorregistrierung verhindern.

#### Prüfung vor dem Tag

Das Leiter-Skript muss aus **jeder** möglichen Stufentabelle — **3⁹ = 19 683**,
trivial aufzählbar — einen **eindeutigen** Multiplikatorvektor erzeugen,
**ohne Eingabe des Betreibers**. *Ein Fall, in dem es fragt, ist ein Fall, in
dem das Register unvollständig ist.* Auch das ist eine Prüfung mit Befund, kein
Abbruchkriterium.

⚠️ **Das Leiter-Skript existiert noch nicht.** Siehe 16.11, Zeile 3.

---

### 16.5 Registertext 7 — Backtester-Prüfung *(neu)*

> Vor dem Selektionslauf wird für jeden Bot der **simulierte Kapitalpfad mit
> heutigen Parametern** gegen den **Papierpfad seit dem Umstellungstag**
> gestellt (gleiche Kerzen, gleiche Kosten). Berichtet werden: Anteil
> übereinstimmender Signale, Korrelation der Tagesrenditen, Summe der
> Abweichung. Ein Bot, dessen Signalübereinstimmung unter **95 %** liegt
> *(willkürlich)*, wird im Selektionslauf ausgewertet, aber mit dem Vermerk
> **„Backtester nicht bestätigt"**, und kann bis zur Klärung **nicht über
> Schatten hinaus**.

**Ergänzung — der Boden unter der Schwelle:**

> **Unterhalb einer Mindestzahl von Signalen wird die Übereinstimmung
> berichtet, aber nicht bewertet.** Der Bot gilt dann als **„Backtester nicht
> geprüft"**, nicht als „nicht bestätigt".
>
> *Begründung: `volatility_breakout` (Aktien) erzeugt bei 21 Tagen
> Median-Haltedauer in drei Monaten möglicherweise zwölf Signale; bei acht
> reisst ein einziger Unterschied die 95 % (8/9 = 88,9 %, 7/8 = 87,5 %). Eine
> Schwelle ohne Boden trifft nach **Handelsfrequenz** statt nach **Qualität** —
> derselbe Fehler wie die gestrichene 10-Trades-Regel (Registertext 1c).*
>
> ⚠️ **Die Mindestzahl ist vom Betreiber festzulegen und als willkürlich zu
> kennzeichnen.** Sie steht bis dahin als **offen** im Register; ohne sie ist
> Registertext 7 nicht anwendbar, sondern nur berichtsfähig.

**Die Abweichung zwischen Live- und Snapshot-Bestand:**

> Live- und Snapshot-Bestand weichen in adjustierten Aktienkursen bis **10⁻⁵**
> relativ voneinander ab; Signalabweichungen an Schwellen sind dadurch möglich
> **und werden gezählt** — nicht weggerechnet, nicht als Rauschen abgetan.

**Der Umstellungstag** ist **`2026-09-16T04:42:24Z`**, für **alle neun Bots**
derselbe, belegt in `docs/umstellungstag_entscheidungskerze.json` (TB-38).

> ⚠️ **Papierpfade vor diesem Tag gelten für den Vergleich Backtest gegen Live
> als nicht vergleichbar.** Vor dem Umstellungstag entschieden die Bots auf der
> **laufenden** Kerze (Teilkerze), danach auf der **Entscheidungskerze**. Das
> ist eine andere Regel, nicht dasselbe Verfahren mit Rauschen.

⚠️ **Der Vergleich ist heute noch nicht gebaut.** Siehe 16.11, Zeile 4.

⚠️ **ERGÄNZT durch Abschnitt 17 (Registernachtrag TB-48, 18.09.2026) — an drei
Stellen; dieser Registertext bleibt im Wortlaut stehen:**

| | |
|---|---|
| **17.6** | Der **Kein-Entscheid-Tag**: ein Tag ohne bestimmbare Entscheidungskerze zählt **nicht** in die Quote, offene Positionen bleiben unverändert; über **5 %** der Handelstage gilt das Fenster als „Holdout beeinträchtigt" |
| **17.7** | ⭐ **Die oben als „vom Betreiber festzulegen" offen gelassene Mindestzahl ist festgelegt: n = \|Vereinigung\| ≥ 20**, abgeleitet aus der 95-%-Schwelle als 1 / (1 − 0,95) und nachgerechnet (18/19 = 94,7 % reisst sie, 19/20 = 95,0 % nicht). Dort ist auch die **Vergleichsmenge** benannt — Ereignispaare (Symbol, Tag), Ein- und Ausstiege, Quote als \|Schnitt\| / \|Vereinigung\| — und das Urteil unterhalb der Mindestzahl heisst **„unbestimmt"** |
| **17.8** | **Drift**: weicht der Bestand zum Vergleichszeitpunkt vom protokollierten Datenstand-Hash ab, ist die Abweichung je Symbol **Drift**, keine Verfahrensabweichung. ⚠️ Die Zählregel oben (bis 10⁻⁵ zwischen Live- und Snapshot-Bestand **werden gezählt**) bleibt davon unberührt — 17.8 betrifft **denselben** Bestand zu **zwei Zeitpunkten** |

---

### 16.6 Registertext 2d — Embargo *(ersetzt die Fassung aus 15.4 vollständig)*

> Die Bestätigungsperiode eines Bots beginnt am **ersten Handelstag nach
> Go-Live, an dem keine vor Go-Live eröffnete Position dieses Bots mehr offen
> ist.** Der Tag wird aus den Positionsdaten bestimmt und im Journal vermerkt.
> **Obere Schranke** ist die Zeitbremse des Bots, falls vorhanden; **für Bots
> ohne Zeitbremse das 95. Perzentil der Haltedauer plus 1** — für
> `t3_supertrend` **13 Handelstage** (P95 = 11,21).
>
> ⚠️ **Ist am Deckeltag noch eine vor Go-Live eröffnete Position offen, beginnt
> die Bestätigungsperiode trotzdem — diese Position wird in der
> Bestätigungsstatistik jedoch nicht gezählt** (Attribution je Position,
> ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel).

**Was sich gegenüber 15.4 ändert:** Das Embargo war dort eine **feste Frist**
(Zeitbremse + 1, Tage im Embargo gehören zu keiner Periode). Jetzt ist es eine
**Bedingung am Bestand** mit der alten Frist als **Deckel**. Der Grund: die
feste Frist verschenkt Bestätigungstage, wenn der Bot früher flach ist, und sie
reicht nicht, wenn er es nicht ist — beides ohne Not.

**Die gemessenen Embargo-Werte aus 15.4 bleiben** als obere Schranken gültig,
soweit sie der neuen Fassung nicht widersprechen; die Tabelle dort ist
unverändert weiterzulesen.

⚠️ **`elliott_wave_stocks` = 91 Handelstage ist bestätigt.** `MAX_HOLD_HOURS =
90` wird bei diesem Bot als **90 Tagesbalken** gelesen — der Kommentar im Bot
sagt es ausdrücklich („entspricht ~90 Handelstage"), und 15.4 Anmerkung 3 hat
es an der Kursreihe nachgemessen.

> **Folge, die ins Register gehört:** Die Bestätigungsperiode beginnt für
> `elliott_wave_stocks` **rund vier Monate später als für die anderen acht**
> (91 Handelstage Deckel gegen 11 bis 16). Wer die neun Bestätigungsperioden
> nebeneinander liest, liest für diesen einen Bot einen deutlich kürzeren
> Zeitraum — das ist kein Fehler, sondern seine Haltedauer.

---

### 16.7 Registertext 3b — Ergänzungen (a) bis (e) *(neu; die Fassung in 15.5 bleibt stehen)*

> **(a)** Eine Selektionsfalte zählt, wenn der Loader des Bots in ihr
> **mindestens ein Symbol** an mindestens einem Handelstag handelbar macht. **Es
> gibt keine Mindest-Symbolzahl je Falte.**
>
> **(b)** `MIN_HISTORY_*` ist **je Bot mit seinem Namen und seiner Einheit**
> fest auf dem heutigen Wert; **die fünf Werte stehen im Register**:
>
> | Bot | Name | Wert | misst |
> |---|---|---:|---|
> | `elliott_wave` | `MIN_HISTORY_HOURS` | **17 520** | **Kerzenzahl** (`len(df)`) |
> | `t3_supertrend` | `MIN_HISTORY_DAYS` | **730** | Zeitspanne in Tagen |
> | `rsi2_crypto` | `MIN_HISTORY_DAYS` | **500** | Zeitspanne in Tagen |
> | `turtle_soup_crypto` | `MIN_HISTORY_DAYS` | **500** | Zeitspanne in Tagen |
> | `volatility_breakout_crypto` | `MIN_HISTORY_DAYS` | **500** | Zeitspanne in Tagen |
> | `elliott_wave_stocks` | `MIN_HISTORY_DAYS` | **1 825** | Zeitspanne in Tagen |
> | `rsi2_mean_reversion` | `MIN_HISTORY_DAYS` | **1 825** | Zeitspanne in Tagen |
> | `turtle_soup_stocks` | `MIN_HISTORY_DAYS` | **1 825** | Zeitspanne in Tagen |
> | `volatility_breakout` | `MIN_HISTORY_DAYS` | **1 825** | Zeitspanne in Tagen |
>
> ⚠️ **Bei Kerzenzählung hängt die Handelbarkeit eines Symbols von der
> Lückenfreiheit der Reihe ab** — eine Reihe mit derselben Zeitspanne, aber
> Lücken, fällt bei `elliott_wave` heraus und bei den anderen acht nicht (in
> TB-40 am Verhalten gemessen, Fall *luecke_gleiche_spanne*). Der Snapshot
> friert das ein, der Live-Bestand kann abweichen — **Registertext 7 zählt
> solche Fälle.**

⚠️ **Tatsachennotiz zu 3b (b) — eine vierte falsche Zahl, in TB-41 gefunden und
hier festgehalten statt stillschweigend geglättet:** Der Wortlaut sagt „die
**fünf** Werte". **Gezählt sind es über die neun Bots vier verschiedene
Zahlenwerte** — **17 520 · 730 · 500 · 1 825** — in **zwei** Einheiten
(Kerzenzahl und Zeitspanne). Die Zahl „fünf" stammt aus
`docs/ERGEBNIS_TB-40_universum_trockenlauf.md` („Fünf verschiedene Werte und
zwei verschiedene Grössen") und ist dort schon falsch; die Tabelle darunter
zeigt in beiden Dokumenten dieselben vier Werte. **Der Wortlaut bleibt
unverändert stehen, weil er der registrierte ist; massgeblich ist die
Tabelle.** `research/registernachtrag_tb41/pruefe_register.py` zählt die Werte
in den neun Bot-Dateien nach und meldet jede Abweichung von **vier Werten in
zwei Einheiten**.
>
> **(c)** ⭐ **Der Benchmark einer Falte** — für die Drawdown-Nebenbedingung
> (Abschnitt 4) und für Rang 3 — **wird auf den in dieser Falte geladenen
> Symbolen des Bots gerechnet, nicht auf dem vollen Universum. Bot und
> Benchmark leben in derselben Menge.**
>
> **(d)** **Berichtet je Bot und Falte, ohne dass ein Kriterium daran hängt:**
> Symbolzahl, Anteil am Universum, **Liste der ausgelassenen Symbole mit Grund**
> (Historie zu kurz / Kursdatei fehlt / Kerzenzahl zu klein), und nach dem Lauf
> die **Faltenkohärenz** — Spearman-Rangkorrelation der
> Parametersatz-Rangfolge dieser Falte gegen die Rangfolge nach dem Median der
> übrigen Falten. *Eine Falte mit Kohärenz nahe null hat als Rauschen gewirkt;
> das steht im Bericht, damit der I10-Lauf es gegen eine Zahl prüfen kann.*
>
> **(e)** Die Listen **„Symbole ohne Faltenevidenz" werden je Bot geführt**
> (Tatsachennotiz in 16.1.2).

**Die Einordnung, die dazugehört:**

> Die drei Symbole der Falte 2019 von `t3_supertrend` sind **BTC, ETH und BNB**
> — die drei, die aus der 2019er-Landschaft in die heutige Liste überlebt
> haben. **Die frühen dünnen Falten sind die Stelle, an der die in Registertext
> 3c eingetragene Survivorship-Verzerrung am grössten ist** — kein neues
> Problem, sondern das bekannte in seiner sichtbarsten Form. Wer 2019 mit drei
> Symbolen rechnet, rechnet mit den drei Gewinnern von 2019.

---

### 16.8 Kandidatenregeln *(neuer Registertext)*

> **(a)** **Kandidaten werden nie gegeneinander gerankt.** Zulassung ist je
> Kandidat **absolut**, gegen die **Null** — das Buch ohne diesen Kandidaten —,
> nie gegen einen anderen Kandidaten. *Die Null ist kein Kandidat, sondern der
> Vergleich, den jeder Kandidat hat.*
>
> **(b)** **N ist die Rastergrösse. Neue Kandidaten bekommen kein Raster** — sie
> treten mit einem festen Satz aus der Literatur an (N = 1). Ein Raster
> frühestens **nach der ersten Bestätigungsperiode**, als eigener registrierter
> Lauf.
>
> **(c)** **Familienbuchführung:** Im Register werden geführt — geprüfte
> Kandidaten, zugelassene, und die erwarteten Fehlzulassungen als Summe.
>
> **(d)** Eine **Reihenfolge nach Prior** ist zulässig: Sie ist eine
> Ressourcenentscheidung, keine Schwelle. **Sie steht im Register, bevor der
> erste Kandidat läuft.**
>
> **(e)** ⭐ **Overlay-Kandidaten** — Regeln, die auf bereits selektierte Bots
> wirken — werden **erst nach dem Selektionslauf registriert**; ihre Zulassung
> hängt an der **Bestätigungsperiode**, nicht an den Falten. *Begründung:
> gestapelte Selektion — ein Overlay wird auf denselben Daten geprüft, auf denen
> die Bots gewählt wurden, und sein Ergebnis hängt von dieser Wahl ab. Die
> Falten sind für ein Overlay kein unabhängiger Boden mehr.*

---

### 16.9 Vorab-Filter *(neuer Registertext)*

> Vor jeder Methodikprüfung und vor jedem Backtest eines Kandidaten:
>
> **(a) Darf der Betreiber das überhaupt handeln?** *(Regulierung am Wohnsitz.
> Diese Klausel hat am 16.09.2026 den Funding-Carry erledigt: keine
> Binance-Derivate für Privatanleger mit Wohnsitz in Deutschland.)*
>
> **(b) Ist das konkrete Instrument für ihn zugelassen?** *(Diese Klausel hätte
> `S-B1` und `S-A2` erledigt: US-domizilierte ETFs sind für EU-Privatanleger
> wegen fehlendem PRIIPs-Basisinformationsblatt gesperrt — auch die gehebelten
> und inversen.)*
>
> **(c) Ko-Einstiegsquote** der Signale gegen jeden vorhandenen Bot derselben
> Anlage. **Über 1,5 ⇒ gleiche Zelle ⇒ Variante, kein Kandidat.**

*Warum das ein Filter und keine Kennzahl ist: (a) und (b) kosten nichts, wenn
man sie zuerst stellt, und kosten einen ganzen Lauf, wenn man sie zuletzt
stellt. Beide Beispiele sind keine Konstruktionen — sie sind an je einem
Kandidaten nachträglich aufgefallen.*

---

### 16.10 Vorbedingung für short-fähige Sleeves *(neuer Registertext)*

> **(a)** Eine Short-Position ist **nur in Indexinstrumenten** zulässig, **nie
> in Einzelaktien**. *Begründung: grösster Tagesanstieg S&P 500 rund **+12 %**
> (13.10.2008), Einzelaktien **+50 %** und mehr (Squeeze). Nur im ersten Fall
> ist der Verlust je Tag mit einer Notional-Grenze beherrschbar.*
>
> **(b)** Je Short-Position **Notional-Obergrenze 20 % des Sleeve-Budgets**
> *(willkürlich)*; der registrierte **Stress-Tagesverlust** ist Notional ×
> grösster historischer Tagesanstieg des Underlyings — **aus den Daten, nicht
> gesetzt**.
>
> **(c)** Ein **Stop liegt als Order beim Broker**, nicht im Cron; die
> Simulation nimmt den Fill **zum Stress-Sprung** an, nicht zum Stop-Kurs.
>
> **(d)** Short-Notional zählt im Netting als **Brutto-Exposure der
> Anlageklasse**.
>
> **(e)** ⭐ **Abbruch, unabhängig von jeder Kennzahl:** Ein realisierter
> Tagesverlust einer Short-Position **über dem registrierten
> Stress-Tagesverlust** setzt den Sleeve auf **Schatten**. *Das ist keine
> Leistungsprüfung, sondern die Feststellung, dass das Risikomodell verletzt
> wurde.*

⚠️ **Registertext 6 braucht dafür keine eigene Stufe.** Der Kapitalpfad ist
durch (b) und den Stress-Sprung nach unten begrenzt; eine vierte Stufe „Short"
würde eine Grenze verdoppeln, die schon steht.

---

### 16.11 Wo Registertext und Umsetzung auseinanderfallen

**Ein Register, das etwas beschreibt, das der Code noch nicht kann, ist in
Ordnung — solange es benannt ist.** Hier ist die vollständige Liste, Stand
16.09.2026:

| # | Registertext | Was der Code heute tut | Wer schliesst die Lücke |
|---:|---|---|---|
| 1 | **5 (a)–(c)** — `data/live/` und `data/snapshots/<hash>/` | Es gibt **einen** Ordner `data/`; **101 Module** lesen ihn direkt. Kein Snapshot, keine Frischeprüfung, kein Live/Snapshot-Schnitt. | eigene Aufgabe (Datenordner-Umbau) |
| 2 | **5 (d)** — alle Cronjobs in UTC | Die Crontab ist in dieser Aufgabe **nicht angefasst** worden; ob `TZ=UTC` gesetzt ist, ist hier nicht geprüft. | Betreiber, beim Umbau |
| 3 | **6 (a)–(m)** — Budgetstufen, Zellen, `m_b` | **Kein Leiter-Skript.** Kein Bot liest einen Multiplikator; alle neun rechnen mit fester Positionsgrösse (faktisch 1/9). Die 3⁹-Prüfung kann noch nicht laufen. | eigene Aufgabe (`m_b` in die `forward_test.py`) |
| 4 | **7** — Backtester-Prüfung | **Kein Vergleichswerkzeug.** Papierpfad und simulierter Pfad werden heute nirgends gegeneinander gestellt; die 95-%-Schwelle hat nichts zu messen. | eigene Aufgabe |
| 5 | **7, Mindestzahl Signale** | **Offen — Betreiber.** Bis die Zahl feststeht, ist Registertext 7 berichtsfähig, aber nicht anwendbar. | Betreiber |
| 6 | **2d** — Embargo als Bedingung am Bestand | `research/vorregistrierung/auswertung.py` kennt nur das **alte** feste Embargo (und rechnet ohnehin nach Verfahren A, 15.8 Nr. 3). Die Datei ist **eingefroren**. | TB-30b |
| 7 | **3b (a)–(e)** — Loader entscheidet, Benchmark auf geladenen Symbolen, Faltenkohärenz | Gemessen ist das nur **einmal**, im Trockenlauf von TB-40. Der spätere Auswerter tut es noch nicht; `faltenplan_neun` beantwortet dieselbe Frage weiter nach Lesart A. | TB-30b |
| 8 | **3b (d)** — Liste der ausgelassenen Symbole mit Grund | **Drei Bots sortieren lautlos aus** (`rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout` melden bei zu kurzer Historie und fehlender Kursdatei **keine Zeile**, TB-40 Abschnitt 4). Die Liste liesse sich heute nicht aus den Logs erzeugen. | eigene Aufgabe (Logging-Fix, freigegeben) |
| 9 | **6, Zellenzuordnung** | Steht jetzt im Register, aber **nirgends im Code** — kein Modul kennt Zellen. | mit dem Leiter-Skript |
| 10 | **16.10** — short-fähige Sleeves | **Kein Bot kann short.** Der Registertext ist reine Vorbedingung für einen Kandidaten, den es noch nicht gibt. | wenn der erste Short-Kandidat antritt |
| 11 | **16.1.1** — die korrigierte Symbolzahl | `research/universum_trockenlauf/universum_trockenlauf.py` liest als „eingetragene" Zahl weiter die **erste** Tabelle mit der Kopfzeile „Symbolzahl je Selektionsfalte" — das ist die **historische** Fassung in 15.5. Ein erneuter Lauf meldet deshalb wieder acht Abweichungen, obwohl das Register jetzt stimmt. Das Werkzeug ist in dieser Aufgabe **unberührt** (Belegquelle). | mit TB-30b, wenn der Auswerter das Werkzeug übernimmt |

**Zwei Stellen, an denen es *nicht* auseinanderfällt** — beide geprüft, nicht
angenommen:

⚠️ **Fortschreibung (18.09.2026, TB-48 — angehängt, nichts entfernt):**
**Zeile 5 dieser Tabelle ist erledigt.** Die Mindestzahl Signale ist in
**17.7** festgelegt (n ≥ 20, als willkürlich abgeleitet aus der 95-%-Schwelle);
Registertext 7 ist damit nicht mehr „offen — Betreiber". *Die übrigen zehn
Zeilen stehen unverändert.* **Sieben weitere Lücken kommen mit Abschnitt 17
hinzu** — sie stehen in **17.10**, nicht hier, damit diese Tabelle den Stand
vom 16.09.2026 behält. ⚠️ **Die dringendste davon:** `shared/snapshot.py`
**kann den Snapshot heute nicht ziehen** — es wirft bei jedem
Teilkerzen-Befund, und es gibt 36 (17.10, Zeile 2).


* **Die fünf `MIN_HISTORY_*`-Werte** in 16.7 (b) sind aus den neun Bot-Dateien
  **gelesen** und werden maschinell dagegen geprüft.
* **Der Umstellungstag** `2026-09-16T04:42:24Z` in 16.5 stimmt für **alle neun**
  Bots mit `docs/umstellungstag_entscheidungskerze.json` überein.

---

### 16.12 Was dieser Nachtrag nicht tut

* **Kein Selektionslauf.** Es ist weiterhin kein Raster gerechnet, kein
  Parametersatz bewertet, kein Ergebnis erzeugt. **Kein Amendment.**
* **Kein Datenordner-Umbau.** `data/live/` und `data/snapshots/` sind
  **Registertext**, nicht Wirklichkeit — 101 Module lesen weiter `data/`.
* **Kein Logging-Fix** für die drei lautlos aussortierenden Bots (freigegeben,
  eigene Aufgabe).
* **Kein `m_b` in den `forward_test.py`** (freigegeben, eigene Aufgabe).
* **Keine Umstellung von `auswertung.py` auf Verfahren B** — die Datei ist
  **unberührt** und bleibt eingefroren.
* **Kein Snapshot, kein signierter Tag, kein Zeitanker.** Das ist der nächste
  Schritt und gehört dem Betreiber.
* **Keine Parameterübernahme.** `live_params.py`, `forward_test.py`,
  `equity_simulation.py`, `multi_symbol_optimise.py` und
  `multi_symbol_walk_forward.py` sind in dieser Arbeit nur **gelesen** worden.
* **Keine Kursdatei angefasst.** Der Datenstand ist unverändert
  `d9449faf51bffaaa…` bei 223 Dateien — als Test nachgewiesen.
* **`research/faltenplan_neun/`, `research/universum_trockenlauf/`,
  `research/etf_trendfolge/` unberührt** — sie sind die Belegquellen.
* **Nichts unter `broker/` oder `shared/`, keine Crontab, kein
  `results/*.csv`.**

*Nachgetragen in TB-41, 16.09.2026. Kein Amendment: kein Selektionslauf, kein
signierter Tag, keine Parameterübernahme.*

---

## 17. Registernachtrag (TB-48, 18.09.2026)

### 17.0 Was das ist — und was es ausdrücklich nicht ist

**Das ist kein Amendment.** Wie bei den Nachträgen TB-36 (Abschnitt 15) und
TB-41 (Abschnitt 16) gilt: es hat **kein Selektionslauf stattgefunden**, kein
Raster ist gerechnet, kein Parametersatz bewertet. Die Sperrliste (Abschnitt 10)
gilt „ab dem signierten Tag", und der steht in Abschnitt 13 weiterhin als
*offen — Betreiber*. Es ist nichts aufzubrechen; es wird nachgetragen, **bevor**
gerechnet wird.

**Seit dem TB-41-Nachtrag sind neun Festlegungen getroffen worden, die im
Register noch nicht standen.** Der Snapshot soll unmittelbar danach gezogen
werden — und er darf nur auf einem Register stehen, das ihn deckt. Das ist der
Anlass dieses Abschnitts.

**Bestehender Text wird nicht umgeschrieben.** Ersetzte Fassungen bleiben
**wörtlich stehen** und tragen einen eingefügten Vermerk — dieselbe Form, die
15.7 und 16.1/16.3/16.6 schon benutzen. *Der Verlauf soll lesbar bleiben; das
ist der Sinn eines Registers.* Die harte Auflage dieses Nachtrags ist
**null entfernte Zeilen**, maschinell nachgewiesen
(`research/registernachtrag_tb41/pruefe_register.py`, Prüfung
`null_entfernte_zeilen`).

**Herkunft der Zahlen.** Keine Zahl dieses Abschnitts ist abgeschrieben; jede
ist in dieser Arbeit **an ihrer Quelle im Repo nachgerechnet** worden. Die
Einzelnachweise stehen in `docs/ERGEBNIS_TB-48_registernachtrag.md`, Abschnitt
„Welche Zahl wurde wo nachgerechnet".

| | |
|---|---|
| Die zwei Nicht-Kurs-Eingaben | `research/snapshotgrenze/ergebnisse/eingaben.json` |
| Teilkerzen-Befunde, Arten, letzte Kerze | `shared/snapshot.py::teilkerzen` über `data/`, neu ausgeführt |
| Jahresaufteilung 20 / 16 und die 11 Symbole | aus denselben Befunden **selbst nachgezählt** |
| Die Gegenprobe zu den 11 Symbolen | `docs/projektfuehrung/BACKLOG.md`, T34.9 |
| `pandas_market_calendars` 4.6.1, beide Hashes | `docs/MACLAUF_TB-47_snapshotgrenze.md` (TB-47-Maclauf) |
| Re-Adjustierung 9 766 / 1,2e-6 | `docs/projektfuehrung/BACKLOG.md`, T35.4 |
| Datenstand | `d9449faf51bffaaa…`, 223 Kursdateien — vor und nach dieser Arbeit identisch |

---

### 17.1 Registertext 5a — Bestand und Snapshot *(ersetzt die Fassung aus 16.3 (a) vollständig)*

> Es gibt einen **fortgeschriebenen Bestand** (Tatsachennotiz: `data/`) und je
> Lauf einen **eingefrorenen Snapshot** (Tatsachennotiz: `snapshots/<hash>/`),
> der **neben** dem Bestand liegt und nach seiner Erzeugung nicht mehr
> geschrieben wird.
>
> Der Snapshot enthält **alle Eingaben des Laufs, die nicht Code unter dem
> registrierten Commit sind**. ⭐ **Gemessen (TB-47): neben den Kursdateien
> genau zwei** — `config/top25_symbols.txt` und `config/sp500_top150.txt`.
>
> Sein `MANIFEST.json` führt jede Datei mit Inhalts-Hash. Der **Snapshot-Hash**
> ist der Hash der nach Pfad sortierten (Pfad, Inhalts-Hash)-Paare **der
> Dateien** — ⚠️ **nicht des Manifests**, sonst hinge der Name von der
> Metadaten-Formatierung ab.
>
> Der **Datenstand-Hash** wird im Manifest als eigenes Feld geführt, mit der
> unveränderten Regel: `*.csv` der obersten Ebene, Name + Grösse + SHA-256,
> sortiert.
>
> Forward-Tests und Registertext 7 lesen **den Bestand**; der Selektionslauf
> liest **ausschliesslich den Snapshot**. Kein Modul des Laufs ruft Kurse über
> das Netz ab. Das Bezugsdatum des Laufs (`asof`) kommt aus dem Register, **nie
> aus der Uhr**.

⚠️ **Befund zur Fundstelle, nicht stillschweigend geglättet.** Der Auftrag
dieses Nachtrags nennt als ersetzte Stelle „Registertext 5a in **Abschnitt
15**". **Dort steht sie nicht.** Abschnitt 15.7 führt Registertext 5 **ohne
Untergliederung** und ist seinerseits bereits **vollständig durch 16.3
ersetzt** (Vermerk seit TB-41 an Ort und Stelle). Die Fassung mit dem
Buchstaben **(a)** — `data/live/` gegen `data/snapshots/<hash>/` — steht in
**16.3**. Der Ersetzungsvermerk ist deshalb **dort** gesetzt worden, wo der
abgelöste Text tatsächlich steht. Hätte er in 15 gestanden, hätte er auf eine
Stelle gezeigt, die es nicht gibt.

**Was sich gegenüber 16.3 (a) sachlich ändert:** Die Ordnernamen `data/live/`
und `data/snapshots/<hash>/` werden zu **Tatsachennotizen** (`data/` und
`snapshots/<hash>/`) herabgestuft — der Registertext bindet sich nicht mehr an
den Pfad, sondern an die **Rolle**; der Snapshot liegt **neben** dem Bestand,
nicht in ihm. Neu hinzu kommen der Umfang der Eingaben (nicht nur Kursdateien),
die Trennung der **beiden** Hashes samt Bildungsregel und die Herkunft des
Bezugsdatums `asof`. Unverändert bleibt der Kern: **der Selektionslauf liest
ausschliesslich den Snapshot, kein Modul ruft Kurse über das Netz ab.**

---

### 17.2 Registertext 5c — Reihenfolge von Snapshot und Tag *(ersetzt die Fassung aus 16.3 (c))*

> Der Snapshot wird **vor** dem signierten Tag gezogen; **der Tag referenziert
> seinen Hash.** Ein zweiter Snapshot ist ein neuer Lauf.

**Was sich ändert:** 16.3 (c) sagte „**am Tag** des signierten Tags". Das liess
offen, was zuerst geschieht, und machte den Tag nicht überprüfbar. Die
korrigierte Fassung legt die **Reihenfolge** fest und gibt dem Tag einen
Inhalt: er nennt den Hash, den er signiert. *Ein Tag, der auf nichts zeigt,
signiert nichts.* Der zweite Satz ist unverändert.

⚠️ **Fundstelle wie bei 17.1:** der Auftrag nennt Abschnitt 15, die Fassung
„am Tag des signierten Tags" steht in **16.3 (c)**. Der Vermerk ist dort
gesetzt.

---

### 17.3 Registertext 5a, Zusatz — Ausnahme `rand_erste` bei der Teilkerzen-Prüfung

*Wörtlich übernommen aus dem Registereintrag vom 18.09.2026, einschliesslich
Herleitung und der beiden Vorbehalte.*

> **Registertext 5a, Zusatz — Ausnahme `rand_erste`.**
>
> Die vor dem Ziehen eines Snapshots vorgeschriebene Teilkerzen-Prüfung schlägt
> bei **36 der 223 Kursdateien** an, Art **`rand_erste`**: Die **erste** Kerze
> dieser Dateien deckt ihren Zeitraum nicht vollständig ab, weil die Historie
> des Symbols innerhalb der Periode beginnt.
>
> **Diese Befundart ist für das Ziehen eines Snapshots zugelassen**, wenn alle
> drei Bedingungen erfüllt sind:
>
> **(a)** Der Befund betrifft ausschliesslich die **erste** Kerze der Datei.
> ⚠️ **Für `rand_letzte` gilt diese Ausnahme nicht.**
> **(b)** Die Kerze ist nachweislich **das Aggregat genau der vorhandenen
> feineren Kerzen** — sie ist daraus abgeleitet, nicht unvollständig
> geschrieben. Die Prüfung stellt das je Datei fest.
> **(c)** Die Ausnahme wird im **Manifest des Snapshots** je Datei aufgeführt,
> mit Art und erster Kerze.
>
> ⚠️ **Die Prüfung selbst wird nicht abgeschwächt.** Sie schlägt weiter an und
> liefert weiterhin Rückgabewert 1; das Ziehen erfolgt gegen diesen Eintrag,
> nicht gegen ein Schweigen der Prüfung.

#### Die Begründung, als Tatsachennotiz

**1. Der Befund betrifft die Abdeckung, nicht die Richtigkeit.** Die Prüfung
selbst stellt je Datei fest: *„die Kerze ist auf die letzte Stelle das Aggregat
genau dieser Teilmenge: sie ist daraus **abgeleitet**."* Ein Symbol, dessen
erster Handel mitten in der Periode liegt, hat an diesem Tag zwangsläufig
weniger Stunden.

**2. Der gefährliche Rand ist sauber.** Gemessen auf beiden Rechnern:
`LETZTE Kerze betroffen: False` bei **allen 223** Dateien. Die Kerze, in die
ein Abruf mitten hineingeschrieben haben könnte, gibt es hier nicht.

**3. ⭐ Die Ausnahme ist für den Selektionslauf folgenlos — hergeleitet:**

| | |
|---:|---|
| **20 von 36** | erste Kerze **2017–2020**. Die erste Selektionsfalte beginnt **2022** — reiner Vorlauf |
| **16 von 36** | erste Kerze **ab 2023**, gehörend zu **genau 11 Symbolen**: `BMT ENA ENSO PEPE PROM PUMP SUI TRUMP U WLD ZKC` |
| ⭐ | **Diese Menge ist identisch mit der Liste aus T34.9** — den Symbolen, die **in keiner Selektionsfalte vorkommen** |

**Kein Symbol-Jahr-Beitrag des Selektionslaufs hängt an einer der 36 kurzen
ersten Kerzen.**

⭐ **Die Mengengleichheit ist gezeigt, nicht behauptet** (TB-48, beide Mengen
gebildet und gegeneinander gestellt): Differenz in **beide** Richtungen leer,
je **11** Elemente. Nachweis in `docs/ERGEBNIS_TB-48_registernachtrag.md`.
⚠️ Zwischen 2020 und 2023 liegt **keine** erste Kerze — die beiden Gruppen
20 und 16 sind daher lückenlos die vollen 36, nicht zwei Ausschnitte.

⚠️⚠️ **BEFUND zur Begründung in Zeile 1 der Tabelle — gemeldet, nicht
stillschweigend korrigiert (TB-48, 18.09.2026).** Der beschlossene Wortlaut
sagt: *„Die erste Selektionsfalte beginnt **2022** — reiner Vorlauf."*
**Beide Hälften dieses Satzes halten der Nachrechnung nicht stand**; der
Wortlaut bleibt als der beschlossene stehen, massgeblich ist diese Notiz.

| | |
|---|---|
| ⚠️ **Die erste Selektionsfalte beginnt nicht 2022, sondern 2019.** | `research/faltenplan_neun/daten/faltenplan.json`: `frueheste_falte: 2019`; die erste Falte läuft bei **allen neun** Bots von `2019-01-01` bis `2021-01-01` |
| ⚠️ **„Reiner Vorlauf" trifft nur auf 6 der 13 Symbole der Gruppe zu.** | Vor dem 01.01.2019 liegt die erste Kerze nur bei `ADA BNB BTC ETH TRX XRP`. Bei **sieben** Symbolen — `AAVE DOGE LINK NEAR SOL UNI ZEC` — liegt sie **innerhalb** des Fensters der ersten Falte |

⭐ **Die Schlussfolgerung trägt trotzdem — sie trägt nur aus einem anderen
Grund.** Nachgerechnet über **alle neun Bots und alle Falten** (TB-48): Es gibt
**null** Fälle, in denen eine der 36 kurzen ersten Kerzen in ein Faltenfenster
fällt, in dem ihr Symbol **geladen** ist. Die sieben Symbole oben stehen in der
ersten Falte bei allen fünf Krypto-Bots in `symbole_ohne_historie` — der Loader
lässt sie dort gar nicht erst zu. **Nicht der Vorlauf schützt, sondern die
Mindesthistorie des Loaders** (Registertext 3b (a)). Der Satz
*„Kein Symbol-Jahr-Beitrag des Selektionslaufs hängt an einer der 36 kurzen
ersten Kerzen"* ist damit **bestätigt**, und zwar maschinell über den
Faltenplan statt über eine Jahreszahl.

⚠️ **Warum das mehr ist als ein Tippfehler:** Die Begründung „Vorlauf" hängt an
einer **Jahreszahl** und wäre beim nächsten Faltenplan lautlos falsch geworden.
Die Begründung „der Loader lädt das Symbol dort nicht" hängt an einer **Regel,
die im Register steht** — und die sich nachrechnen lässt. Der Vorbehalt am Ende
dieses Zusatzes (*„fällt ein `rand_erste`-Befund an einer Datei an, deren Symbol
in einer Selektionsfalte vorkommt…"*) meint genau diese Prüfung.

**4. Reparieren wäre teurer und nicht dauerhaft.**

| | |
|---|---|
| ⚠️ **Teurer** | Abschneiden oder Neuaufbau ändert `data/` — und damit **`d9449faf…`**, die Tatsachennotiz vom 15.09., **samt der darauf gemessenen Symbolzahlen je Falte (3b)** |
| ⚠️ **Nicht dauerhaft** | **Jedes neu gelistete Symbol bringt den Befund wieder mit.** Eine Reparatur räumt den Bestand einmal auf und setzt die Uhr auf das nächste Listing zurück |

#### Die Messwerte zum Eintrag

| | |
|---|---|
| Gemessen am | **18.09.2026**, Cloud (Python 3.11.15) **und** MacBook (3.9.6) — **beide 36 von 223** |
| Arten | `{'rand_erste': 36}`, keine andere |
| Letzte Kerze betroffen | **nein**, bei keiner Datei |
| Datenstand | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223 Dateien |
| Werkzeug | `shared/snapshot.py`, Prüfung vor dem Ziehen, Rückgabewert 1 bei Befund |
| Rohdaten | `research/snapshotgrenze/ergebnisse/` (Cloud) · TB-47-Maclauf `04_teilkerzen.json` |

⚠️ **Zwei Angaben, die eine Prüfung NICHT abdeckt** und die hier stehen, damit
niemand sie später für gemessen hält:

| | |
|---|---|
| **175 von 223** Dateien tragen den Vermerk **`kein_zeuge`** | 150 Aktien und 25 Krypto-1h. *„Die Abdeckung der Randkerzen ist aus den Dateien nicht belegbar"* — es gibt keine feinere Datei zum Vergleich. **Das ist „kein Befund", nicht „geprüft"** |
| Die Vollständigkeit der **letzten** Kerze dieser 175 | ruht auf `shared/abrufschutz.py` (TB-35), **nicht** auf dieser Prüfung. Eine andere Zusicherung, die trägt — aber eine andere |

#### Was dieser Zusatz ausdrücklich NICHT tut

| | |
|---|---|
| ❌ | Er ändert `data/` nicht |
| ❌ | Er schwächt die Prüfung nicht ab — es gibt **keine Übergehen-Flagge** |
| ❌ | Er erlaubt **keinen** Befund ausser `rand_erste` an der **ersten** Kerze |
| ❌ | Er berührt `d9449faf…` nicht — der Wert bleibt unverändert gültig |

> ⚠️ **Fällt in einem künftigen Bestand ein `rand_erste`-Befund an einer Datei
> an, deren Symbol in einer Selektionsfalte vorkommt, greift diese Ausnahme
> nicht automatisch.** Dann ist neu zu entscheiden, und die Herleitung oben ist
> neu zu rechnen.

---

### 17.4 Registertext 5e — der Lese-Audit *(neu)*

> Der Selektionslauf erzeugt einen **Lese-Audit**: die Liste aller Dateien, die
> er gelesen hat, mit Inhalts-Hash. **Ein Lauf ist nur gültig, wenn der Audit
> vorliegt, jede Datei darin im Manifest des Snapshots steht und der
> Snapshot-Hash vor und nach dem Lauf identisch ist.** Ein Lauf ohne Audit oder
> mit einer Datei ausserhalb des Manifests ist **kein Lauf dieses Registers**.
> **Wie der Audit erzeugt wird, ist Umsetzung.**

*Warum das neben 5a steht und nicht in ihm aufgeht:* 5a sagt, **woraus** der
Lauf liest. Der Lese-Audit sagt, **woraus er nachweislich gelesen hat**. Das
erste ist eine Vorschrift, das zweite ein Beleg — und nur das zweite fällt auf,
wenn ein Modul still an `data/` vorbeigreift. ⚠️ Die Prüfung „Snapshot-Hash vor
und nach dem Lauf identisch" deckt zusätzlich den Fall ab, dass der Lauf in
seine eigene Eingabe schreibt.

---

### 17.5 Registertext 5f — die registrierte Umgebung *(neu)*

> Der Selektionslauf findet auf einer **registrierten Umgebung** statt:
> **Python-Fassung** (Tatsachennotiz: 3.9.6), ein **`requirements.lock`** mit
> exakten Versionen aller Pakete, dessen Hash im Register steht, und die
> **Plattform**. Der Lauf beginnt mit einer Prüfung dieser drei Angaben und
> **bricht bei Abweichung ab (Rückgabewert 2)**.
>
> ⭐ **Tatsachennotiz:** Der Handelskalender kommt **nicht aus einer Datei**,
> sondern aus dem Paket **`pandas_market_calendars`** (gemessen TB-47:
> Fassung **4.6.1** auf dem Betriebsrechner). Er ist damit **Umgebung, nicht
> Eingabe**, und liegt im Lock.
>
> Der Reproduktionstest gilt als bestanden, wenn ein zweiter Lauf **auf
> derselben registrierten Umgebung** auf einer anderen Maschine bitidentisch
> ist. Eine Reproduktion auf anderer Umgebung wird **berichtet**, ist aber
> weder Bedingung noch Widerlegung.

⚠️ **Das schärft die Prüfung aus 16.3 nach.** Dort stand: der Lauf „muss auf
einer zweiten Maschine bitidentisch reproduzieren". **Ohne Umgebungsbegriff war
das nicht entscheidbar** — eine Abweichung konnte am Snapshot liegen oder an
einer anderen Paketfassung, und beides sah gleich aus. Erst mit der
registrierten Umgebung trennt der Test die beiden Fälle. Der Satz in 16.3
bleibt stehen und gilt weiter; 17.5 sagt, **auf welcher Grundlage** er gemessen
wird.

⭐ **Warum der Kalender eigens genannt ist:** Er ist die einzige Eingabe des
Laufs, die **wie eine Datei aussieht und keine ist**. Wäre er Eingabe, gehörte
er in den Snapshot; als Paket gehört er in den Lock. Die Einordnung ist
gemessen worden (TB-47, `eingaben.json`, Feld `kalender`) und nicht geraten.

---

### 17.6 Registertext 7, Ergänzung I — der Kein-Entscheid-Tag *(neu)*

> Ein Tag, an dem ein Bot seine Entscheidungskerze nicht bestimmen konnte, ist
> ein **Kein-Entscheid-Tag**: keine Einstiege, keine Ausstiege, **offene
> Positionen unverändert**, ein **Lauf-Datensatz mit Grund**.
> Kein-Entscheid-Tage gehen **nicht** in die Übereinstimmungsquote ein und
> werden je Bot gezählt. Übersteigt ihr Anteil im Vergleichsfenster **5 %** der
> Handelstage (**als willkürlich gekennzeichnet**), gilt das Fenster als
> „Holdout beeinträchtigt" und wird so berichtet.

*Warum das nötig ist:* Ohne diese Festlegung sieht ein Tag ohne
Entscheidungskerze in den Zahlen **genauso aus wie „kein Signal"** — derselbe
Fehler, den `docs/DATENLUECKEN.md` für ausgefallene Cron-Läufe schon
festhält. Ein solcher Tag zählte dann als Übereinstimmung, wo gar nichts
verglichen wurde. Die Regel macht den Unterschied sichtbar **und** hält fest,
dass ein Kein-Entscheid-Tag am Bestand nichts ändert: **offene Positionen
bleiben offen**, es wird nicht vorsichtshalber geschlossen.

---

### 17.7 Registertext 7, Ergänzung II — Ereignismenge und Mindestzahl *(neu; schliesst die offene Stelle aus 16.11, Zeile 5)*

> Vergleichsmenge sind die **Einstiegs- und Ausstiegsereignisse (Symbol, Tag)
> beider Seiten** im Vergleichsfenster, ohne Kein-Entscheid-Tage.
> Übereinstimmung = |Schnitt| / |Vereinigung|.
> **Mindestzahl n = |Vereinigung| ≥ 20, abgeleitet als 1 / (1 − Schwelle).**
> Unter 20 lautet das Urteil **„unbestimmt"**: Der Bot wird selektiert und nach
> Registertext 6 eingestuft, im Bericht mit dem Vermerk „Backtester unbestimmt
> (n = …)"; ein Aufstieg auf **Bestätigt** setzt n ≥ 20 **und** Übereinstimmung
> ≥ 95 % voraus.

**Die Ableitung, nachgerechnet und Teil des Registertextes:**

> Die Schwelle aus 16.5 ist **95 %**. Gesucht ist das kleinste n, bei dem **eine
> einzige** Abweichung die Schwelle nicht schon reisst. Bei **n = 19** ergibt
> eine Abweichung **18/19 = 94,7 %** — unter der Schwelle. Bei **n = 20** ergibt
> eine Abweichung **19/20 = 95,0 %** — auf der Schwelle, also nicht darunter.
> **n = 20 = 1 / (1 − 0,95).** Unterhalb davon entscheidet ein einzelnes
> Ereignis über das Urteil, und die Schwelle misst dann **Handelsfrequenz statt
> Qualität.**

⚠️ **Damit ist die in 16.5 und in 16.11, Zeile 5, als *offen — Betreiber*
geführte Mindestzahl festgelegt.** Registertext 7 ist ab hier nicht mehr nur
berichtsfähig, sondern **anwendbar** — soweit das Vergleichswerkzeug existiert
(siehe 17.10).

⭐ **Der Unterschied zur Fassung aus 16.5 ist mehr als eine Zahl.** 16.5 kannte
zwei Urteile („bestätigt" / „nicht bestätigt") und darunter den Zustand
**„Backtester nicht geprüft"**. 17.7 benennt den Zustand unterhalb der
Mindestzahl als **„unbestimmt"** und sagt zusätzlich, **was mit dem Bot
geschieht**: er wird selektiert und eingestuft, er bleibt nicht liegen. Die
Sperre wirkt allein am **Aufstieg auf Bestätigt**. *Eine fehlende Messung ist
kein schlechtes Ergebnis — aber sie trägt auch keine Beförderung.*

⚠️ **Und der Vergleichsgegenstand ist jetzt benannt.** 16.5 sprach von
„Anteil übereinstimmender Signale", ohne zu sagen, was ein Signal ist. 17.7
legt ihn fest: **Ereignispaare (Symbol, Tag)**, Einstiege und Ausstiege, beide
Seiten, und die Quote als **Jaccard-Mass** |Schnitt| / |Vereinigung| — nicht als
Anteil an einer der beiden Seiten. *Ein Mass, das nur durch die eine Seite
teilt, belohnt die Seite, die weniger Ereignisse erzeugt.*

---

### 17.8 Registertext 7, Ergänzung III — Drift *(neu)*

> Jeder Forward-Test-Lauf protokolliert **den Datenstand-Hash des Bestands, den
> er gelesen hat**, und **die Werte seiner Entscheidungskerze je Symbol**. Der
> Backtester-Vergleich läuft auf **diesen protokollierten Werten**; weicht der
> Bestand zum Vergleichszeitpunkt vom protokollierten Hash ab, wird die
> Abweichung je Symbol als **„Drift"** ausgewiesen und **nicht** als
> Verfahrensabweichung gezählt.

⭐ **Die Begründung gehört in den Text:** Aktienkurse werden nach jeder
Dividende re-adjustiert. **Gemessen (T35.4, Mac-Lauf TB-35): 9 766 von rund
11 000 Bestandszeilen wichen bei einem einzigen echten Abruf ab, maximal
1,2 × 10⁻⁶ relativ, ausschliesslich vor dem letzten Ex-Dividenden-Tag.** Ohne
diese Regel zählte **jede Dividende im Vergleichsfenster als
Verfahrensabweichung** — der Backtester bekäme eine schlechte Note für ein
Ereignis, das mit seiner Rechenweise nichts zu tun hat.

⚠️ **Das hebt die Zählregel aus 16.5 nicht auf, sondern grenzt sie ab.** 16.5
sagt: Signalabweichungen zwischen Live- und Snapshot-Bestand bis 10⁻⁵ „werden
gezählt — nicht weggerechnet, nicht als Rauschen abgetan". Das bleibt. 17.8
betrifft einen **anderen** Fall: nicht zwei Bestände nebeneinander, sondern
**denselben Bestand zu zwei Zeitpunkten**. Die Unterscheidung ist am
protokollierten Hash **entscheidbar** — genau deshalb verlangt der Text ihn.
*Eine Abweichung, die man erst nachträglich erklärt, ist eine Auslegung; eine,
die am Hash hängt, ist ein Befund.*

---

### 17.9 Nachtrag zur Tatsachennotiz vom 15.09.2026 — was `d9449faf…` bezeichnet

**Datiert angehängt. Nichts entfernt. Der Wert bleibt gültig — nur sein
Referent wird benannt.**

> **Ab Registertext 5a (neu) bezeichnet
> `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`
> den Kursdatenteil des Snapshots (Datenstand-Hash), nicht den Snapshot selbst;
> der Snapshot-Hash ist ein eigener Wert.**

⭐ **Gemessen im TB-47-Maclauf, beide Werte nebeneinander über dieselben 223
Dateien:**

| | |
|---|---|
| `datenstand_hash` | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` — **trifft den verankerten Wert** |
| `snapshot_hash` | `4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608` |
| verschieden | **ja** — wie vorgesehen, die beiden Hashes beantworten verschiedene Fragen |

⚠️ **Warum das aufgeschrieben werden musste.** 16.3 (b) sagt: „**Der
Registerhash bezeichnet den Snapshot.**" Zu diesem Zeitpunkt gab es nur *einen*
Hash, und der war `d9449faf…`. Seit TB-47 gibt es **zwei**, und der Satz aus
16.3 (b) liesse sich ohne diesen Nachtrag so lesen, als sei `d9449faf…` der
Snapshot-Hash. Er ist es nicht. **Die Tatsachennotiz vom 15.09.2026
(Abschnitt 10) bleibt in jedem Wort gültig**; sie hat den Bestand gemessen, und
den misst `d9449faf…` weiterhin.

---

### 17.10 Wo Registertext und Umsetzung auseinanderfallen

**Ein Register, das etwas beschreibt, das der Code noch nicht kann, ist in
Ordnung — solange es benannt ist.** Dieselbe Form wie 16.11; hier die Stellen,
die **mit Abschnitt 17** hinzukommen, Stand 18.09.2026. Die elf Zeilen aus
16.11 bleiben davon unberührt und gelten weiter.

| # | Registertext | Was der Code heute tut | Wer schliesst die Lücke |
|---:|---|---|---|
| 1 | **5a (neu)** — Snapshot **neben** dem Bestand, `snapshots/<hash>/` | Es gibt **einen** Ordner `data/`; kein Snapshot ist gezogen. Unverändert 16.11, Zeile 1 | eigene Aufgabe (Datenordner-Umbau) |
| 2 | ⚠️ **5a, Zusatz (17.3)** — `rand_erste` ist zum Ziehen **zugelassen** | **Der Code kann den Snapshot heute nicht ziehen.** `shared/snapshot.py::ziehen` wirft bei **jedem** Teilkerzen-Befund (`Snapshotfehler`, vor dem Kopieren) — bei 36 Befunden also immer. Eine registrierte Ausnahme kennt er nicht, und eine Übergehen-Flagge soll es nach 17.3 auch nicht geben. ⭐ **Das Manifest trägt das Feld `teilkerzen` bereits**, es wird nur nie geschrieben, weil der Lauf vorher abbricht | eigene Aufgabe: die Ausnahme **gegen den Registereintrag** prüfen, nicht gegen eine Flagge |
| 3 | **5e (17.4)** — Lese-Audit | **Nicht vorhanden.** Kein Modul führt Buch über gelesene Dateien; im ganzen Quelltext gibt es keine solche Stelle | eigene Aufgabe |
| 4 | **5f (17.5)** — registrierte Umgebung, Abbruch mit Rückgabewert 2 | **Nicht vorhanden.** Es gibt **kein `requirements.lock`** (nur `requirements.txt` ohne feste Versionen), keine Fassungsprüfung und keinen Abbruchpfad. ⚠️ **Auch die Mindestfassung des Projekts steht nirgends** (`docs/UMGEBUNGEN.md`, offen) | eigene Aufgabe, zusammen mit dem Lock |
| 5 | **7, Ergänzung I (17.6)** — Kein-Entscheid-Tag | **Nicht vorhanden.** Die neun `forward_test.py` kennen den Begriff nicht und schreiben keinen Lauf-Datensatz mit Grund | eigene Aufgabe (Änderung am Live-Pfad, eigene Freigabe) |
| 6 | **7, Ergänzung II (17.7)** — Ereignismenge, n ≥ 20 | **Kein Vergleichswerkzeug** — unverändert 16.11, Zeile 4. ⭐ **Zeile 5 aus 16.11 ist mit 17.7 erledigt:** die Mindestzahl ist nicht mehr offen | eigene Aufgabe |
| 7 | **7, Ergänzung III (17.8)** — Drift | **Nicht vorhanden.** Kein `forward_test.py` protokolliert den Datenstand-Hash oder die Werte seiner Entscheidungskerze je Symbol | eigene Aufgabe |

⚠️ **Zeile 2 ist die dringendste.** Sie ist die einzige, die einen Schritt
blockiert, der unmittelbar bevorsteht: **der Snapshot soll gezogen werden, und
mit dem heutigen Code lässt er sich nicht ziehen.** Die übrigen beschreiben
Vorhaben, deren Zeitpunkt offen ist.

---

### 17.11 Was dieser Nachtrag nicht tut

* **Kein Selektionslauf.** Weiterhin kein Raster gerechnet, kein Parametersatz
  bewertet, kein Ergebnis erzeugt. **Kein Amendment.**
* **Kein Snapshot gezogen, kein signierter Tag, kein Zeitanker.** Das ist der
  nächste Schritt und gehört dem Betreiber.
* **Kein Code geändert.** Nichts unter `shared/`, `strategies/`, `research/`,
  `broker/`, `dashboard/`, `notifications/` oder `system/`; keine Crontab.
  Die in 17.10 genannten Lücken sind **Befunde**, nicht Reparaturen.
* **Keine Kursdatei angefasst.** Der Datenstand ist vor und nach dieser Arbeit
  `d9449faf51bffaaa…` bei 223 Dateien — gemessen, nicht angenommen.
* **Keine Parameterübernahme.** `live_params.py` ist in dieser Arbeit nicht
  einmal gelesen worden.
* **Keine Zeile entfernt.** `git diff --numstat` auf dieses Dokument weist die
  Null aus; der Nachweis steht in
  `docs/ERGEBNIS_TB-48_registernachtrag.md`.
* **Nichts zum zweiten Umstellungstag.** ⚠️ **Sein Datum existiert noch
  nicht** — es entsteht erst am ersten Tag, an dem alle neun Bots ohne Rückfall
  aus `data/` lesen. Eigener Eintrag, danach.
* **Keine Gleichheitsprüfung der Entscheidungskerze, kein Datencron, kein
  Resolver-Modus.** Alle drei sind Änderungen am Live-Pfad beziehungsweise der
  grosse Umbau — eigene Aufgaben mit eigener Freigabe.

*Nachgetragen in TB-48, 18.09.2026. Kein Amendment: kein Selektionslauf, kein
signierter Tag, keine Parameterübernahme.*

---

## 18. Tatsachennotiz zu Registertext 5 / 5a — der gezogene Snapshot (TB-55, 19.09.2026)

**Datiert angehängt. Nichts entfernt. Kein Registertext wird geändert — hier
wird eine Messung festgehalten**, in der Form der Tatsachennotiz zu 4d
(Abschnitt 15.6). Das ist der Nachtrag, den `docs/ERGEBNIS_TB-55_snapshot.md`
angekündigt hat: TB-55 hat den Snapshot gezogen und ausdrücklich keinen
Registertext angefasst.

**Der gezogene Snapshot** (Tatsachennotiz zu 5 / 5a; jede Zahl aus
`snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/MANIFEST.json` gelesen, nicht abgeschrieben):

| | |
|---|---|
| Gezogen (`zeitpunkt_utc`) | **2026-09-19T06:49:32+00:00** |
| Name (`snapshot_hash`) | **`63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2`** |
| Ort | `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/` |
| Versioniert | Commit **`1075dec`** auf `main` (`git log --oneline -- snapshots/ \| tail -1`; liegt auf `origin/main`) |
| Dateien gesamt (`dateien_gesamt`) | **225** — 223 Kursdateien sowie `config/sp500_top150.txt` und `config/top25_symbols.txt` |
| Bytes gesamt (`bytes_gesamt`) | **211 040 678** |
| Datenstand (`datenstand_hash`) | **`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`** bei **223** Kursdateien — dreimal gemessen (vor dem Ziehen, danach, am Ende), dreimal gleich |
| Zugelassene Befunde der Zeitabdeckungsprüfung (`zugelassene_befunde_anzahl`) | **36**, sämtlich der Art `rand_erste`, nach der Ausnahme in **Abschnitt 17.3** (`zugelassene_befunde_herkunft.fundstelle` = `docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3`) |
| Übergangene Befunde (`teilkerzen.nicht_zugelassen`) | **leer** — kein Befund wurde übergangen |
| Nachprüfung (`shared/snapshot.py --pruefen`) | **`UNVERAENDERT`**, Rückgabewert 0 |

⭐ **Der Datenstand `d9449faf…` ist derselbe wie in der Tatsachennotiz vom
15.09.2026 (Abschnitt 10) und im Nachtrag 17.9** — der Snapshot enthält den
Bestand, den das Register seit dem 15.09. verankert. Der Name `63e4b6c8…`
läuft über die 225 Dateien des Laufs (Kursdateien plus die zwei
Symbollisten); der Wert `4fee547d…` aus 17.9 lief nur über die 223 Kursdateien
und bezeichnet **nicht** diesen Snapshot. Beide Werte bleiben richtig; sie
beantworten verschiedene Fragen.

Vier Punkte, die diese Tabelle tragen:

1. **Jede der 225 Dateien wurde beim Kopieren byteweise gegen die Quelle
   geprüft**; die anschliessende Nachprüfung meldet `UNVERAENDERT`. Beim
   Einchecken legte git **keinen neuen Blob für eine der 225 Dateien** an —
   ein Blob (das Manifest), vier Trees, ein Commit. Die Inhalte sind identisch
   mit `data/`; Nachweis in `docs/ERGEBNIS_TB-55_snapshot.md`.
2. **Der Name wurde viermal unabhängig gerechnet**: TB-49 in der Cloud
   (Python 3.11, echter Zug in ein Wegwerfverzeichnis), TB-49 auf dem MacBook
   (Python 3.9.6, Trockenlauf), TB-55 in der Cloud (3.11.15, Trockenlauf) und
   TB-55 auf dem MacBook (3.9.6, dieser Zug) — viermal derselbe. Er hängt weder
   an der Maschine noch am Python-Zweig.
3. **Die 36 Befunde sind keine Lücke im Register, sondern seine Anwendung.**
   Die Ausnahme in 17.3 verlangt drei Bedingungen; das Manifest führt jeden
   Befund je Datei mit Art und erster Kerze auf (17.3 (c)). `nicht_zugelassen`
   ist leer, das Werkzeug hätte sonst nicht gezogen (Registertext 5a, Zusatz).
4. ⚠️ **Dieser Snapshot ist der Eingabezustand des Selektionslaufs. Ein
   zweiter Snapshot ist ein neuer Lauf** (Registertext 5 in 16.3, 5a in 17.1;
   Backlog F1a). `snapshots/` wird von hier an nur gelesen.

**Was diese Notiz nicht tut:** kein Selektionslauf, kein signierter Tag, kein
Zeitanker, kein Amendment — nichts an Registertext 5, 5a oder 5c ist
umformuliert. Der signierte Tag bleibt der nächste Schritt und gehört dem
Betreiber (Abschnitt 13).

*Nachgetragen in TB-55b, 19.09.2026. Tatsachennotiz: eine Messung, keine
Festlegung.*

---

## 19. Registertext 5e, Ergänzung — die Codeherkunft (TB-58b, 19.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Registertext wird
umgeschrieben — hier wird Registertext 5e (Abschnitt 17.4) ergänzt**, in der
Form von Abschnitt 18. Das ist der Nachtrag, den
`docs/ERGEBNIS_TB-58_startpruefungen.md` angekündigt hat: TB-58 hat die
Prüfungen gebaut und ausdrücklich keinen Registertext angefasst.

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Entscheidung.**
Sie trifft etwas, das im Register offen war — 5e sagt, welche **Daten** ein
Lauf gelesen hat; nichts sagte, welcher **Code** sie gelesen hat. Sie ist vor
dem Tag zulässig, ihre Begründung nennt kein Ergebnis, und sie hat keine
bekannte Wirkung auf die Zulassung eines Bots: sie entscheidet, wann ein
**Lauf** ein Lauf dieses Registers ist, nicht, welcher Bot durchkommt.

> **Registertext 5e, Ergänzung Codeherkunft. Datum: 19.09.2026.**
>
> Der Selektionslauf prüft bei Start, dass sein **Einstiegspunkt** und der
> **Resolver** unter derselben Git-Wurzel liegen, dass deren `HEAD` der
> registrierte Commit ist und dass der **Arbeitsbaum sauber** ist; bei
> Verletzung bricht er ab (**Rückgabewert 2**). Wurzel, Commit und Sauberkeit
> werden im Lese-Audit protokolliert. **Ein Lauf ohne diese Angaben oder mit
> abweichender Wurzel ist kein Lauf dieses Registers.**
> ⚠️ **Im Regelbetrieb gilt keine dieser Bedingungen.**
>
> **Begründung:** Liegen Aufrufer und Resolver in verschiedenen Bäumen,
> beschreibt kein einzelner Commit den gelaufenen Code. Das Lese-Audit belegt,
> **welche Daten** gelesen wurden; es sagt nichts darüber, **welcher Code**
> gelesen hat.
>
> ⭐ **Das Wegwerfbaum-Muster** — eine Bot-Kopie in einem temporären Verzeichnis
> mit der echten `shared/` — **ist eine Testtechnik des Regelbetriebs und im
> Selektionsmodus unzulässig.**

**Was der Code am Tag dieses Eintrags tut** (`shared/paths.py`, Commit
`6518e413b17dd4b7f5c624549aa145f94fca3a96` auf `main`; jede Zeile gemessen,
Nachweise in `docs/ERGEBNIS_TB-58_startpruefungen.md` und
`shared/test_startpruefungen.py`, 44 Proben mit Mutationsgegenprobe):

| Satz des Registertexts | Umsetzung | Gemessen |
|---|---|---|
| Einstiegspunkt und Resolver unter derselben Git-Wurzel | `sys.modules["__main__"].__file__` und `shared/paths.py`, beide über `realpath` und `git rev-parse --show-toplevel` | gespaltener Baum aus einem anderen Repo **und** aus einem Ordner ohne Git: rc 2, die Meldung nennt beide Wurzeln; `python -c` (kein Einstiegspunkt): rc 2 |
| `HEAD` ist der registrierte Commit | der Modus **trägt** den erwarteten Commit in der dritten Umgebungsvariablen `TB_SELEKTIONSCOMMIT` (7–40 Hex-Zeichen; Zweignamen wie `main` werden abgewiesen); `git rev-parse HEAD` muss damit beginnen | falscher Commit rc 2; fehlende Variable bei gesetzten anderen beiden rc 2; Variable allein `Selektionsfehler` |
| Arbeitsbaum sauber | `git status --porcelain` über `shared/`, `strategies/` und `requirements.lock` (`ARBEITSBAUM_PFADE`), untracked zählt; ⚠️ **nicht** über `data/` — die ist versioniert und wird vom Abruf-Cron laufend verändert, ein Lauf aus dem Snapshot darf daran nicht scheitern | veränderte Datei unter `shared/`, neue Datei unter `strategies/`, veränderter Lock: je rc 2 mit Nennung; neue Datei unter `data/` stört nicht |
| Rückgabewert 2 | `SystemExit(2)` beim Import, nicht `Exception` — ein `except Exception` im Aufrufer kann den Abbruch nicht in einen stillen Weiterlauf verwandeln; der Wert steht genau einmal | rc 2 in jeder Probe, `stdout` leer |
| Wurzel, Commit, Sauberkeit protokolliert | drei der acht Auditzeilen `[paths] codewurzel / commit / arbeitsbaum` auf `stderr` nach bestandener Prüfung, dieselben Werte über `paths.startpruefung()` und `paths.audit_zeilen()` | `stderr`-Zeilen == `audit_zeilen()`; gegen den echten Arbeitsbaum 9 / 9 Bot-Einstiegspunkte |
| Im Regelbetrieb gilt nichts davon | alles im `else`-Zweig des Modus; `subprocess`, `importlib.metadata`, `platform`, `hashlib` werden erst innerhalb der Prüffunktionen importiert | ohne Modus **0 / 0 / 0** `git`-, Paket- und `os.system`-Aufrufe (zählende Attrappe), 144 Pfade über 9 Bots zeichengleich wie vor TB-58 |

Drei Punkte, die diese Tabelle tragen:

1. **„Der registrierte Commit" ist heute der Wert, den der Modus mitbringt.**
   Der signierte Tag (Abschnitt 13) existiert noch nicht; bis dahin sagt
   `TB_SELEKTIONSCOMMIT`, welcher Commit verlangt ist, und die Prüfung misst,
   ob der Baum ihn hat. Sobald der Tag steht, ist es sein Commit. Die Bauart
   ist dieselbe wie beim Snapshot-Hash: der Modus **trägt** den Sollwert, statt
   ihn irgendwo zu suchen, und ein Kindprozess erbt ihn.
2. ⚠️ **Der Lese-Audit als Ganzes (5e, 17.4) ist weiterhin nicht gebaut** —
   17.10, Zeile 3 gilt fort. Was heute existiert, sind die acht Auditzeilen des
   Starts; der spätere Lese-Audit übernimmt sie über `audit_zeilen()`, ohne
   eine zweite Fassung zu pflegen. Der Registertext beschreibt damit etwas, das
   der Code zum Teil noch nicht kann — benannt, nicht verschwiegen (dieselbe
   Regel wie 16.11 und 17.10).
3. **Das Wegwerfbaum-Muster** wird von Bedingung 1 getroffen: eine Bot-Kopie in
   einem temporären Ordner, die die echte `shared/` importiert, hat einen
   anderen Einstiegspunkt als Resolver-Wurzel — im Selektionsmodus rc 2. Im
   Regelbetrieb bleibt es erlaubt und wird weiter gemessen
   (`shared/test_strategy_paths.py`, Probe E, ohne Modus).

**Was diese Ergänzung nicht tut:** kein Selektionslauf, kein signierter Tag,
kein Amendment; der Wortlaut von 5e in 17.4 bleibt stehen und gilt weiter;
17.10 wird nicht umgeschrieben — seine Zeilen beschreiben den Stand vom
18.09.2026, und ob eine davon inzwischen geschlossen ist, steht hier und in
Abschnitt 20, nicht dort.

*Nachgetragen in TB-58b, 19.09.2026. Entscheidung nach F17: vor dem Tag, ohne
Ergebnis in der Begründung, ohne Wirkung auf die Zulassung eines Bots.*

---

## 20. Tatsachennotiz zu Registertext 5f — der Lock (TB-58b, 19.09.2026)

**Datiert angehängt. Nichts entfernt. Kein Registertext wird geändert — hier
wird eine Messung festgehalten**, in der Form von Abschnitt 18. Registertext 5f
(Abschnitt 17.5) verlangt ein `requirements.lock`, „dessen Hash im Register
steht"; bis zu diesem Eintrag stand er nirgends, und 17.10, Zeile 4 hielt
fest, dass es die Datei nicht gab. Seit TB-58 gibt es sie; hier ist ihr Hash.

> **Tatsachennotiz zu Registertext 5f — der Lock. Datum: 19.09.2026.**
>
> Die Umgebung, in der der Selektionslauf rechnet, ist in
> **`requirements.lock`** im Projektwurzelverzeichnis festgehalten, versioniert
> unter Commit `d852bce637ba82ddb60330a7219c6e36a40539c3`.
>
> | | |
> |---|---|
> | SHA-256 der Datei | **`96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5`** |
> | Pakete | **67**, sämtlich mit `==` |
> | Interpreter | `3.9.6 (default, Apr 30 2025, 02:07:18) [Clang 17.0.0 (clang-1700.0.13.5)]` |
> | Plattform | `macOS-15.7.9-x86_64-i386-64bit` |
>
> Der Lauf prüft bei Start Interpreter, Paketfassungen und Plattform gegen
> diese Datei und bricht bei Abweichung ab (**Rückgabewert 2**).
>
> ⚠️ **`requirements.txt` ist kein Lock** — es nennt, was installierbar ist;
> `requirements.lock` nennt, was gelaufen ist.

**Jede Zahl der Tabelle wurde in TB-58b selbst gemessen, keine abgeschrieben:**

| | Messung |
|---|---|
| SHA-256 | zweimal unabhängig gerechnet — `shasum -a 256` und `hashlib.sha256` unter `trading-env/bin/python3` — beide `96a5c572…`; derselbe Wert steht in der Auditzeile `lock_sha256` eines bestandenen Starts |
| Versioniert | `git log -- requirements.lock` nennt genau einen Commit, `d852bce`, auf `origin/main`; der Blob im Arbeitsbaum ist byteweise der Blob unter `HEAD` (`git hash-object` = `git rev-parse HEAD:requirements.lock`, `863197fb…`) |
| 67 Pakete, sämtlich `==` | 83 Zeilen, davon 67 Paketzeilen; 0 Paketzeilen ohne `==`; gegen `importlib.metadata` unter `trading-env/bin/python3`: **0 Abweichungen** |
| Interpreter, Plattform | Kopfzeilen `interpreter_voll` und `plattform` der Datei, gleichlautend mit `sys.version` und `platform.platform()` des Betriebsinterpreters; dazu `maschine x86_64` |
| Der Kalender | `pandas-market-calendars==4.6.1` — dieselbe Fassung, die die Tatsachennotiz in 17.5 (gemessen TB-47) nennt; `pandas==2.3.3` |

**Die Probe, die diesen Eintrag erst wahr macht** — in einem Wegwerf-Klon des
Repos (kein Objekt und keine Datei im Arbeitsbaum von `~/trading-bot`
berührt), Interpreter `trading-env/bin/python3`, Snapshot `63e4b6c8…`,
`TB_SELEKTIONSCOMMIT` = `HEAD` des Klons, Einstiegspunkt eine committete
Datei:

| Zustand | Rückgabewert | Meldung |
|---|---|---|
| Lock unverändert (Kontrolle) | **0** | acht Auditzeilen, `lock_sha256 96a5c572…` |
| eine Zeile verfälscht (`pandas==0.0.1`), **committet**, Baum sauber | **2** | „1 Abweichung/en … pandas: Lock 0.0.1, installiert 2.3.3" |
| dieselbe Verfälschung **nicht** committet | **2** | „Arbeitsbaum … nicht sauber (1 Eintrag …  M requirements.lock)" — Abschnitt 19, Bedingung 3, greift **vor** der Lock-Prüfung |
| Lock gelöscht und committet | **2** | „requirements.lock fehlt … `nicht pruefbar` ist nicht gruen" |
| Lock richtig, Interpreter `/usr/bin/python3` (gleicher Build, andere Pakete) | **2** | „24 Abweichung/en", die ersten drei „installiert NICHT" |

Drei Punkte, die diese Tabellen tragen:

1. **Was geprüft wird, ist die Umgebung gegen die Datei — nicht die Datei gegen
   diesen Eintrag.** Der Lauf liest den Lock, der unter dem verlangten Commit
   im Baum liegt, vergleicht Interpreter, Plattform und jede Paketzeile mit
   dem, was `importlib.metadata` tatsächlich findet (kein `pip`, kein
   Kindprozess, keine Netzverbindung), und schreibt den SHA-256 der Datei in
   die Auditzeile `lock_sha256`. Ob diese Zeile `96a5c572…` lautet, ist am
   Audit abzulesen; ein anderer Lock wäre ein anderer Commit und scheiterte
   schon an Abschnitt 19.
2. ⚠️ **Nichts wird installiert, nachgezogen oder repariert.** Der Lauf meldet
   die Zahl der Abweichungen und die ersten drei, dann bricht er ab.
3. **Die Interpreter- und die Plattformzeile allein hätten den fremden
   Interpreter nicht bemerkt** — `/usr/bin/python3` ist derselbe Build wie
   `trading-env/bin/python3`; erst die Paketzeilen unterscheiden die beiden
   (24 Abweichungen). Deshalb sind alle drei Achsen im Lock, nicht nur die
   Fassung.

**Was diese Notiz nicht tut:** kein Selektionslauf, kein signierter Tag, kein
Amendment, kein `pip install`; der Wortlaut von 5f in 17.5 ist nicht
umformuliert. 17.10, Zeile 4 bleibt als Befund vom 18.09.2026 stehen; dass sie
mit `d852bce` und `6518e41` geschlossen ist, steht hier. Die Mindestfassung des
Projekts (`docs/UMGEBUNGEN.md`, in 17.10, Zeile 4 mitgenannt) ist **nicht**
Gegenstand dieser Notiz und bleibt offen.

*Nachgetragen in TB-58b, 19.09.2026. Tatsachennotiz: eine Messung, keine
Festlegung.*

---

## 21. Berichtigung zu Registertext 4 — die Faltenschranke (TB-56b, 19.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben —
der berichtigte Satz bleibt in Abschnitt 15.6 stehen** und wird hier wörtlich
zitiert, gefolgt von der Messung und dem Ersatztext. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und dieselbe Form,
in der die Abschnitte 18 bis 20 angehängt wurden.

**Anlass:** `docs/ERGEBNIS_TB-56_faltenschranke.md` hat gemessen und die Schranke
aus dem Code entfernt, ausdrücklich **ohne** einen Registertext anzufassen. Die
Berichtigung war als eigene Aufgabe angekündigt; dies ist sie.

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Berichtigung.**
Der Grund stammt aus einer Messung an der Datenlage (TB-56, Teil A, rein lesend,
**vor** jeder Änderung am Code), nicht aus der Kenntnis eines Selektionsergebnisses
— es hat kein Selektionslauf stattgefunden. *„Die Grenze zwischen Berichtigung und
nachträglicher Wahl ist nicht die Zeit, sondern die Quelle des Grundes."*

---

### 21.1 Der berichtigte Satz, wörtlich

Aus **Abschnitt 15.6**, Punkt 2 der vier Punkte, die die Faltentabelle tragen:

> **Die erste Falte ist 2019, und die Schranke dafür ist das Register, nicht
> die Datenlage.** `ERSTE_MOEGLICHE_FALTE = 2019` gilt unverändert. Ohne diese
> Schranke begänne der Plan bei acht der neun Bots schon 2017 oder 2018 —
> Bitcoin-Daten reichen bis 2017-08-17 zurück. Nur bei `rsi2_crypto` bindet die
> Datenlage selbst (150 Tagesbalken Vorlauf, erst ab 2019 erfüllt); bei den
> anderen acht bindet die Registerschranke.

⚠️ **Was daran falsch ist — und was ausdrücklich nicht.** Der Satz beschreibt
richtig, **dass** eine Schranke wirkte, und er sagt richtig voraus, **dass** der
Plan ohne sie früher begänne; beides hat TB-56 bestätigt. Falsch ist seine
**Gegenwartsform und seine Begründung**:

| | |
|---|---|
| ⚠️ **Gegenwartsform** | `ERSTE_MOEGLICHE_FALTE` ist seit Commit `7387cc5` (19.09.2026, 18:58 UTC) aus `research/vorregistrierung/registerdaten.py` entfernt. Der Satz behauptet eine Schranke, die es im Code nicht mehr gibt |
| ⚠️⚠️ **Begründung** | *„die Schranke dafür ist das Register"* — **gemessen: kein Registertext nennt eine Jahreszahl.** Registertext 4a (Abschnitt 15.6) sagt *„vom ersten Jahr, in dem am 1. Januar Daten für Universum und Indikator-Vorlauf vorliegen"*, Registertext 3b (a) (Abschnitt 16.7) sagt *„ab einem handelbaren Symbol"*. Die Zahl 2019 stand **nur im Code und in diesem Begründungssatz** |

⭐ **Damit trug die Faltentabelle in 15.6 eine Begründung, die auf sich selbst
zeigte.** Das ist die Fehlerklasse, gegen die Prüfprinzip C4 geschrieben ist:
eine Angabe, die nicht sagt, gegen **was** sie prüft.

---

### 21.2 Die Messung, auf der die Berichtigung ruht

**Fundstelle:** `docs/ERGEBNIS_TB-56_faltenschranke.md`, Teil A (Messung
18:11–18:15 UTC am 19.09.2026), Werkzeug
`research/faltenplan_neun/faltenschranke_messung.py`. Die Schranke wurde **im
Speicher** ausgeschaltet, die Datei auf der Platte blieb unverändert; vorab wurde
geprüft, dass das Werkzeug **mit** Schranke denselben Plan liefert wie die
festgehaltene Messung `daten/faltenplan.json` — **9/9 gleich**. Ohne diese
Kontrolle hätte die Messung ein anderes Werkzeug gemessen als das, das die
Tatsachennotiz erzeugt hat.

| | gemessen |
|---|---|
| Schranke bindet bei | **8 von 9** Bots |
| Faltenzahl ändert sich bei | **8 von 9** |
| Bestätigungsperiode ändert sich bei | **1** (`elliott_wave`) |
| ⭐ **Zulassung nach Registertext 4b ändert sich bei** | **keinem** — alle neun erreichen die Mindestzahl 3 vorher wie nachher |
| Frühestes Datum in den Krypto-Daten | **2017-08-17** (BTC/ETH) |
| H-Reihen ab 2019 | **zeichengleich mit der Tatsachennotiz 16.1.1** — derselbe Trockenlauf misst dasselbe wie damals, nur mit den frühen Falten davor |

---

### 21.3 Der Ersatztext

> **Berichtigung zu Abschnitt 15.6, Punkt 2 (19.09.2026).**
>
> **(a)** Die erste Selektionsfalte je Bot folgt **allein aus Registertext 4a
> und Registertext 3b (a)**. Es gibt **keine Registerschranke auf ein
> Kalenderjahr.** Die frühere Konstante `ERSTE_MOEGLICHE_FALTE = 2019` war eine
> Festlegung im Code **ohne Entsprechung in einem Registertext**; sie ist mit
> Commit `7387cc5` entfernt.
>
> **(b)** Ergeben 4a und 3b (a) für einen Bot **verschiedene** erste Falten,
> bindet **3b (a)**. *Begründung: Eine Falte, in der der Loader kein Symbol
> handelbar macht, erzeugt keinen Trade und damit keinen Falten-Sharpe; sie
> könnte zum Faltenmedian nichts beitragen. Die Begründung folgt aus der
> Struktur des Selektionsmasses, nicht aus einem erwarteten Ergebnis.*
> *(Betreiberentscheidung 19.09.2026, auf Entscheidungsvorlage mit gemessenen
> Zahlen und benannter Empfehlung.)*
>
> **(c)** Die erste Falte ist damit **je Bot verschieden** und hängt am
> Indikator-Vorlauf und an `MIN_HISTORY_*` des jeweiligen Loaders. Die Aussage
> *„alle Bots eines Marktes teilen einen Faltenplan"* gilt **nicht mehr**;
> siehe 21.5.

---

### 21.4 Die berichtigte Faltenliste — Tatsachennotiz zu 4d

⚠️ **Diese Tabelle ersetzt die Tatsachennotiz-Tabelle in Abschnitt 15.6.** Die
dortige Tabelle bleibt stehen und gilt als **ERSETZT**; sie wird nicht entfernt.

Erste Falte und Faltenzahl nach **3b (a)** (Trockenlauf des Laufcodes, Spalte „H"
in TB-56 Teil A). Bestätigungsperiode unverändert bis `2026-09-01`,
ausschliesslich (Abschnitt 5.2).

| Bot | Markt | Faltenlänge | erste Falte | # Selektionsfalten | Bestätigung ab | 4b erfüllt |
|---|---|---:|---:|---:|---|---|
| `elliott_wave` | krypto | 2 J | **2018–2019** | **4** | ⚠️ **2026-01-01** | ja |
| `t3_supertrend` | krypto | 1 J | **2019** | **7** | 2026-01-01 | ja |
| `rsi2_crypto` | krypto | 1 J | 2019 | 7 | 2026-01-01 | ja |
| `turtle_soup_crypto` | krypto | 1 J | **2018** | **8** | 2026-01-01 | ja |
| `volatility_breakout_crypto` | krypto | 1 J | **2018** | **8** | 2026-01-01 | ja |
| `elliott_wave_stocks` | aktien | 1 J | **2017** | **9** | 2026-01-01 | ja |
| `rsi2_mean_reversion` | aktien | 1 J | **2018** | **8** | 2026-01-01 | ja |
| `turtle_soup_stocks` | aktien | 1 J | **2017** | **9** | 2026-01-01 | ja |
| `volatility_breakout` | aktien | 1 J | **2018** | **8** | 2026-01-01 | ja |

⭐ **`t3_supertrend` steht unverändert bei 2019 und 7 Falten.** Nach 4a begänne
sein Plan 2018; sein Loader verlangt jedoch `MIN_HISTORY_DAYS = 730`, und BTC/ETH
(Daten ab 2017-08-17) erreichen das erst am **2019-08-17** — in der Falte 2018
macht er **kein** Symbol handelbar (Trockenlauf: 0 Symbole). Nach (b) bindet
3b (a); seine Zeile bleibt, wie sie war. **Die Berichtigung ändert für diesen Bot
nichts ausser der Begründung.**

⚠️ **Die dünnste Falte des ganzen Plans**, ausdrücklich benannt, damit sie
niemand für einen Fehler hält: `turtle_soup_crypto` und
`volatility_breakout_crypto` haben in der Falte **2018 zwei Symbole an zwei
Tagen** — BTC und ETH werden am **2018-12-30** handelbar (2017-08-17 + 500 Tage).
Nach 3b (a) („an mindestens einem Handelstag") zählt die Falte. **Eine
Mindest-Symbolzahl wird ausdrücklich nicht eingeführt**; Fable hat sie am
16.09.2026 als *„die Schranke durch die Hintertür"* verworfen (Registertext 3b,
Ergänzung (a), Abschnitt 16.7), und sie träfe genau die frühen Falten, die als
einzige eine Bärenmarkt-Vorgeschichte haben. Registertext 3b (d)
(Faltenkohärenz) misst die Folge **nach** dem Lauf, ohne dass vorher jemand eine
Falte für unwürdig erklärt.

---

### 21.5 Was sich dadurch ändert — vollständig, auch das Unangenehme

| | Änderung | ⚠️ |
|---|---|---|
| **Zulassung nach 4b** | **keine** — alle neun erreichen die Mindestzahl 3 vorher wie nachher | der Grund, warum diese Berichtigung keine Auswahl trifft |
| ⚠️ **Bestätigungsperiode `elliott_wave`** | **2025-01-01 → 2026-01-01**, also **12 Monate kürzer** | Folge der Doppeljahr-Parität. **Berichtet, nicht als Grund benutzt** — eine kürzere Bestätigungsperiode ist ein Nachteil, und ihn zum Argument für die alte Schranke zu machen hiesse, das Register nach erwartetem Effekt zu schreiben |
| ⚠️⚠️ **Die vier Aktien-Bots teilen keinen Faltenplan mehr** | `elliott_wave_stocks` und `turtle_soup_stocks` beginnen **2017**, `rsi2_mean_reversion` und `volatility_breakout` **2018** | Abschnitt 3 sagt heute: *„gilt für alle Bots dieses Marktes mit gleichem Faltenplan"* und dreimal *„teilt Universum und Faltenplan mit den übrigen aktien-Bots — dieselbe Tabelle"*. **Diese Prämisse trägt nicht mehr.** Siehe 21.6 |
| **Krypto-Benchmark** | unverändert offen | Die Benchmark-Tabelle führt die fünf Krypto-Bots als `status: platzhalter` mit **leerer** `dd_toleranz` — gemessen in beiden Tabellenfassungen. Das hängt an TB-31 und ist **nicht** Gegenstand dieser Berichtigung, gehört aber vor den Tag |

---

### 21.6 Die Folge für Sperrliste Punkt 4 — Entscheidungsvorlage, nicht vollzogen

⚠️⚠️ **Hier wird nichts entschieden. Dieser Abschnitt legt die gemessenen Zahlen
vor; die Entscheidung gehört dem Betreiber.** Grund: `DD_Toleranz` und die vorab
berechneten Benchmark-Drawdowns stehen auf der Sperrliste (Abschnitt 10,
Punkt 4), und eine Änderung dort ist ein **Amendment** nach 10.1.

**Was TB-56 getan hat (Betreiberentscheidung 19.09.2026, Option a):** die neu
gerechnete Tabelle liegt als **eigene Datei** daneben
(`research/vorregistrierung/ergebnisse/benchmark_drawdowns_ohne_schranke.json`);
die gesperrte Datei ist **byteweise unverändert** — gemessen: SHA-256
`a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee`, letzte
Änderung 14.09.2026, letzter Commit `a2fcf01` (TB-30a). `test_vorregistrierung.py`
ist seither rot, geführt als **„offen durch eigene Änderung — blockierend für den
Tag"**, ausdrücklich **nicht** als „bekannt rot".

**Die gemessene Differenz**, gerechnet über beide JSON-Dateien:

| Bot | Selektionsfalten alt → neu | `DD_Toleranz` |
|---|---|---|
| `elliott_wave_stocks` | 2019–2025 (7) → **2017–2025 (9)** | **unverändert** |
| `turtle_soup_stocks` | 2019–2025 (7) → **2017–2025 (9)** | **unverändert** |
| ⚠️ `rsi2_mean_reversion` | 2019–2025 (7) → **2018–2025 (8)** | **ändert sich auf allen 100 Exposure-Stufen** |
| ⚠️ `volatility_breakout` | 2019–2025 (7) → **2018–2025 (8)** | **ändert sich auf allen 100 Exposure-Stufen** |

**Die Richtung, unbequem und deshalb zuerst genannt:** Die Toleranz wird bei
beiden Bots **tiefer, also nachgiebiger**.

| Exposure-Stufe | gesperrt | neu | Delta |
|---:|---:|---:|---:|
| 25 % | −2,18 | −3,35 | **−1,17** |
| 50 % | −4,33 | −6,61 | **−2,28** |
| 100 % | −8,55 | −12,89 | **−4,34** |

⚠️⚠️ **Das ist eine Lockerung einer Zulassungsschranke, und sie muss als solche
entschieden werden.** Der Grund dafür ist **strukturell** — 2018 war für den
Aktien-Benchmark ein schlechtes Jahr und zieht den Median nach unten —, und er
darf **nicht** damit begründet werden, dass eine nachgiebigere Schranke mehr
Parametersätze durchlässt. *Warum die beiden anderen Aktien-Bots unverändert
bleiben, ist **erschlossen, nicht gemessen**: sie gewinnen zwei Falten (7 → 9),
und der Median sitzt danach zwischen denselben beiden Werten; die anderen beiden
gewinnen eine (7 → 8), und der Median wird zum Mittel aus zwei anderen.*

**Die drei Wege, mit dem Preis jedes einzelnen:**

| | Weg | Preis |
|---|---|---|
| ⭐ **A** *(Empfehlung)* | **Amendment vollziehen**: die neue Tabelle wird die registrierte, die alte bleibt als ERSETZT stehen, `benchmark_drawdowns.json` wird **nicht** überschrieben, sondern der Registertext verweist auf die neue Datei | Eine gesperrte Zahl ändert sich vor dem Tag. **Kein Lauf ist davon berührt** — es hat keinen gegeben, also beginnt auch keiner von vorn (10.1 greift ins Leere). Der Preis ist Aufmerksamkeit, nicht Evidenz |
| **B** | **Alte Tabelle behalten**, Faltenliste berichtigen, Benchmark auf dem alten Stand lassen | ⚠️ **Widerspruch bleibt bestehen**, nur an anderer Stelle: der Plan kennt 2017/2018, die Benchmark-Tabelle nicht — und `test_vorregistrierung.py` bliebe dauerhaft rot. **Ein dauerhaft roter Test ist keine Wache** (Prüfprinzip A4) |
| **C** | **An Fable** | Kostet eine Runde. Inhaltlich ist es dieselbe Frage wie seine Frage 2 aus der laufenden Anfrage, nur vor dem Tag statt danach |

**Warum A empfohlen wird, und was daran schlechter ist als an B:** A stellt die
Übereinstimmung zwischen Register und Rechnung wieder her und lässt den Prüfer
wieder beissen. Schlechter ist A darin, dass eine Zahl der Sperrliste sich
bewegt, **bevor** der Tag sie einfriert — und wer das einmal tut, hat den Vorgang
normalisiert. ⚠️ **Genau deshalb steht hier eine Vorlage und keine Ausführung.**

---

### 21.7 Prüfung der Abschnitte 18 und 20 gegen den Tatsachennotiz-Test

**Der Test, wörtlich (Fable):** *„Eine Tatsachennotiz hält fest, sie schafft
nicht."* Jeder Satz ist Messwert mit Herkunft oder Verweis.

| Abschnitt | Prüfung | Ergebnis |
|---|---|---|
| **18** (Snapshot, TB-55) | Jede Zahl der Tabelle nennt ihr Feld im `MANIFEST.json` und ist „gelesen, nicht abgeschrieben". Der Name wurde **viermal unabhängig** gerechnet. Die Abgrenzung gegen `4fee547d…` steht im Abschnitt selbst. Der Schlussabsatz nennt ausdrücklich, was die Notiz **nicht** tut | ⭐ **besteht** |
| **20** (Lock, TB-58b) | SHA-256 zweimal unabhängig gerechnet; jede Tabellenzeile mit Messung hinterlegt; die Probe-Tabelle führt fünf Zustände mit Rückgabewert und Meldung; Schlussabsatz nennt die Grenzen | ⭐ **besteht** |

⚠️ **Ein Befund an der Form, kein Fehler an den Zahlen:** Beide Abschnitte sind
mit *„in der Form von Abschnitt 18"* bzw. *„in der Form der Tatsachennotiz zu 4d
(Abschnitt 15.6)"* aufeinander bezogen. **Die Tatsachennotiz zu 4d in 15.6 ist
diejenige, die diese Berichtigung soeben ersetzt.** Der Formverweis bleibt
gültig — er zeigt auf die *Form*, nicht auf den *Inhalt* —, aber wer ihm folgt,
landet ab heute in einer als ERSETZT gekennzeichneten Tabelle. **Hier
festgehalten, damit der Verweis nicht stillschweigend in die Irre führt.**

---

### 21.8 Was diese Berichtigung ausdrücklich NICHT tut

| | |
|---|---|
| ⚠️ | **Kein Amendment.** Sperrliste Punkt 4 ist unberührt; `benchmark_drawdowns.json` ist byteweise dieselbe Datei. 21.6 ist eine Vorlage |
| ⚠️ | **Keine Codeänderung.** Die drei Kopien der Schranke werden hier **benannt, nicht angefasst**: `research/faltenplan_neun/faltenplan_neun.py:120` (`FRUEHESTE_FALTE = 2019`, mit einem Kommentar in Zeile 119, der auf die entfernte Konstante verweist) und `research/krypto_historie/faltenplan.py:64`. *Grund für die Reihenfolge: Das Register sagt, was der Code tun soll — also wird zuerst das Register berichtigt und danach der Code nachgezogen, mit Mac-Lauf. Umgekehrt hiesse es, den Code zum Massstab des Registers zu machen* |
| ⚠️ | **Kein Registertext 0.** Die Drei-Kategorien-Regel (F17) als allgemeine Registeranforderung einzutragen, hängt an **Fables Fragen 1 und 3** (`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-19_pruefungsregistrierung.md`), die genau entscheiden, ob das ein Registertext wird. Sie ist heute **einmal** im Register genannt (Abschnitt 19, als Einordnung einer Änderung), nicht als Regel |
| ⚠️ | **Keine Änderung an Registertext 5f.** Die Übergabe vom 19.09. nennt sie als Punkt; **gemessen: im gesamten Repo steht nirgends, worin sie bestehen soll.** Was an 5f offen war — der fehlende Lock-Hash — ist mit Abschnitt 20 geschlossen. **Bis eine Spezifikation vorliegt, wird hier nichts an 5f geändert**, statt eine zu erfinden |
| | **Kein Selektionslauf, kein signierter Tag, kein Zeitanker.** Der Tag bleibt der nächste Meilenstein und gehört dem Betreiber (Abschnitt 13) |

---

### In einfacher Sprache

**Im Regelwerk stand ein Satz, der sich selbst begründete.** Er sagte: Die
Auswertung beginnt 2019, und zwar weil das Regelwerk es so will. Nachgesehen
wurde: **Kein einziger Regeltext nennt eine Jahreszahl.** Die 2019 stand nur im
Programm — und in diesem Satz, der auf sie zeigte.

**Das Programm ist gestern korrigiert worden, der Satz bis heute nicht.** Solange
beides nebeneinandersteht, widerspricht das Programm dem Regelwerk, und niemand
kann sagen, welches von beiden gilt. Dieser Abschnitt schliesst die Lücke: Der
alte Satz bleibt stehen, damit nachvollziehbar ist, was dastand; daneben steht,
was gemessen wurde und was künftig gilt.

**Was sich praktisch ändert:** Die meisten Bots dürfen jetzt ein oder zwei Jahre
früher ausgewertet werden, weil ihre Daten so weit zurückreichen. **Kein einziger
Bot verliert dadurch seine Zulassung** — jeder hat mehr Auswertungsjahre als
vorher, nicht weniger. Ein Bot bekommt dadurch einen kürzeren Bewährungszeitraum;
das steht hier, obwohl es unangenehm ist, und es ist ausdrücklich **kein**
Argument gegen die Korrektur gewesen.

**Was offen bleibt und warum:** Zwei Bots bekämen durch das zusätzliche Jahr eine
**nachgiebigere** Verlustschranke. Eine Schranke zu lockern, nachdem man weiss,
dass sie sich lockern würde, ist genau die Art Entscheidung, die dieses Regelwerk
verhindern soll. Deshalb steht hier eine Vorlage mit Zahlen und einer Empfehlung
— entschieden wird sie vom Betreiber, nicht von mir.

*Nachgetragen in TB-56b, 19.09.2026. Berichtigung: sie nennt den falschen Satz,
die Messung und den Ersatztext — und entfernt nichts.*

---

### 21.9 Ergänzung — die Entscheidung zu 21.6 (Betreiber, 19.09.2026)

**Datiert angehängt. Nichts entfernt.** Abschnitt 21.6 hat drei Wege vorgelegt
und ausdrücklich nichts entschieden. Hier steht die Entscheidung.

> **Betreiberentscheidung 19.09.2026 zu Sperrliste Punkt 4.** Das Amendment wird
> **einmal** vollzogen, **nach** der Berechnung der Krypto-Falten (TB-31), und
> umfasst dann **alle neun Bots**. Bis dahin bleibt
> `research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` byteweise
> unverändert; die neu gerechnete Tabelle liegt als eigene Datei daneben.

**Der Grund — und ausdrücklich nicht der andere:**

| ⭐ Der Grund | ⚠️ NICHT der Grund |
|---|---|
| **Gemessen:** Die fünf Krypto-Bots stehen in **beiden** Tabellenfassungen als `status: platzhalter` mit **leerer** `dd_toleranz`. Die Drawdown-Bedingung (Abschnitt 4) ist damit für fünf von neun Bots nicht auswertbar; *erschlossen, nicht gemessen: der signierte Tag kann davor nicht kommen.* Ein Amendment jetzt bewegte eine gesperrte Zahl, die kurz darauf erneut bewegt werden müsste — **einmal statt zweimal** | **Die Lockerung zu vermeiden oder hinauszuzögern.** Sie steht so oder so; die Zahlen liegen gemessen in 21.6 und werden durch Warten nicht kleiner. Eine Verfahrensfrage nach ihrem erwarteten Effekt zu entscheiden, ist genau der Fehler, den dieses Register ausschliessen soll |

**Die Folgen, benannt statt in Kauf genommen:**

| | |
|---|---|
| `test_vorregistrierung.py` | bleibt **rot**, weiterhin geführt als **„offen durch eigene Änderung — blockierend für den Tag"**, ausdrücklich nicht als „bekannt rot". ⚠️ Zulässig ist das, **weil die Marke den Grund nennt und den Tag blockiert** — nicht, weil ein dauerhaft roter Test hinnehmbar wäre (Prüfprinzip A4) |
| Der Widerspruch zwischen berichtigtem Faltenplan und gesperrter Benchmark-Tabelle | **bleibt offen und ist hier benannt.** Er wird mit demselben Amendment geschlossen |
| Abschnitt 3, *„teilt Universum und Faltenplan mit den übrigen aktien-Bots — dieselbe Tabelle"* | wird im selben Zug berichtigt; die Prämisse trägt seit 21.5 nicht mehr |

⚠️ **Was diese Ergänzung nicht tut:** kein Amendment, keine Zahl der Sperrliste
bewegt, kein Registertext umgeschrieben. Sie hält eine **Reihenfolge**-Entscheidung
fest, nicht eine Sachentscheidung über die Tabelle.

*Nachgetragen in TB-56b, 19.09.2026.*
