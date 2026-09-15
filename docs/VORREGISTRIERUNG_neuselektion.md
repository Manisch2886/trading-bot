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
