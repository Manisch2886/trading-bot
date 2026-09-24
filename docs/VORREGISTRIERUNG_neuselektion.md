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

> ⭐ **Registertext, Ersteintrag — Fundstellen (38.2, Fable 22h, TB-89,
> 23.09.2026):** Ein Registertext nennt Fundstellen im Code als **Datei und
> Bezeichner** (Funktion, Konstante, Zuweisung, Feldname), nicht als
> Zeilennummer. Zeilennummern stehen nur in Tatsachennotizen, zusammen mit dem
> Commit, an dem sie gemessen wurden. *Eine Zeilennummer ohne Commit ist keine
> Fundstelle.* Gilt für jeden Registertext ab Abschnitt 38; ältere Abschnitte
> bleiben zeichengleich, ihre Zeilenangaben gelten für ihren Commit-Stand
> (30.3). Wortlaut, Herkunft und Grund in **38.2**.

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

> ⭐ **Festlegung 1 PRÄZISIERT durch Abschnitt 24 (TB-71, 20.09.2026, Betreiberentscheidung 18:15) — der Wortlaut bleibt stehen.** Führendes Mass bleibt der Kapital-Drawdown; gerechnet wird er für die Nebenbedingung auf der täglichen Mark-to-Market-Reihe des Kapitalpfads (Registertext 1a), nicht auf der ereignisindizierten Kurve aus `equity_simulation.py`, die Berichtswert bleibt.

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

   > ⭐⭐ **`G6` liest diese Zeile maschinell — Wortlaut nicht ändern (40.2,
   > Fable 24a, TB-96, 24.09.2026).** `test_vorregistrierung.py`
   > (`_testjahre_aus_register`, Teil G) sucht im ganzen Register genau eine
   > Zeile, die mit `4. **JJJJ und JJJJ sind Testfalten, keine Trainingsjahre.**`
   > beginnt, und liest die Jahre daraus. Umformuliert — auch nur Satzzeichen
   > oder Hervorhebung — oder eine zweite Zeile mit diesem Anfang ⇒ `None` ⇒
   > `G6` rot für alle neun Bots. Eine Änderung der Sache braucht einen eigenen
   > Registereintrag **und** die Anpassung von `G6` im selben Auftrag.

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

> ⭐⭐ **Eingabedateien nach 23d (40.6, Fable 24a, TB-96, 24.09.2026):** Die
> neun Listen oben (`78e2bc6`, 13.09.2026) sind Eingabe einer Herleitung von
> Registertext (33.2) und fallen unter 23d in voller Form. Sie werden vor dem
> Tag **einmal auf dem registrierten Snapshot mit dem registrierten Code neu
> erzeugt** (Erzeuger unter 36.1), kommen als Punkt auf die Sperrliste, und die
> Faltenlänge wird danach nach dieser Regel neu abgeleitet und gegen 33.2
> verglichen (TB-98). Die alten Listen bleiben als historischer Stand liegen.
> ⚠️ **Nicht registriert ist der Parameterstand, mit dem die Listen erzeugt
> wurden** — dieser Abschnitt nennt ihn nicht; die Neu-Erzeugung trägt ihn als
> Tatsachennotiz hierher (Parameterdateien, Commit, Snapshot, Modus, Hash je
> Liste). Die Schwelle selbst ist registriert (Festlegung 7, 5.1 Nr. 6). Der
> Regeltext oben bleibt zeichengleich.

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

> ⚠️ **Hinweis (36.2 und 36.6, Fable 22b/22c, TB-84, 22.09.2026):** Ab 36.2 prüft
> eine Sonde diese Liste — für jeden Punkt Pfad und Hash gegen diesen
> Registertext, mit drei Ausgängen (36.5). **Die maschinenlesbare Fassung ist
> Abbild, nicht Quelle**; das Abbild ist nach 36.6 eine **eigene, neue Datei**,
> einmalig geschrieben und selbst mit Hash im Register. `herkunft.py`
> `EINGEFROREN` (Z. 57) und `SPERRLISTE_DATEIEN` (Z. 66) sind **nicht** das
> Abbild und werden es nicht; ihre Tatsachennotiz steht bei Fable aus
> (Anfrage 22c). Sonde und Abbild sind nicht gebaut (36.7).

> ⚠️ **Hinweis (37.1–37.5, Fable 22d/22g, TB-87, 22.09.2026):** Die
> Tatsachennotiz zu `EINGEFROREN` und `SPERRLISTE_DATEIEN` steht jetzt in
> **37.4**: `EINGEFROREN` bildet die Abschnitt-0-Menge ab, nicht diese Liste;
> `SPERRLISTE_DATEIEN` liest niemand; `herkunft.py` wird nicht geöffnet. Sonde
> und Abbild sind seit TB-85 gebaut (`shared/sperrlistensonde.py`, Abbild
> `sperrliste_abbild_2026-09-22.json`, `6a1b732e…`); nach 37.1 meldet sie
> künftig je Bestandteil, nach 37.2 führt das Abbild Punkte und bestimmte Pfade.
> ⭐⭐ **Was ein Befund `1` bedeutet, hängt vom Tag ab (37.3):** Diese Liste gilt
> „ab dem signierten Tag"; vorher ist ein beauftragter Befund planmässig und
> wird mit Tatsachennotiz und neuem Abbild geschlossen, danach ist er ein
> Bruch nach 10.1. Punkte 7 und 9 nennen Werte ohne Ort (37.5).

Ab dem signierten Tag sind unveränderlich:

1. **Rastergrenzen und Grenzsätze** — `registerdaten.py`, Abschnitt 3 dieses
   Registers
2. **Faltengrenzen, Go-Live-Schnitt, Purge-Längen, Faltenlängen** —
   `faltenplan.py`, `ergebnisse/faltenplan.json`
   > ⚠️ **Tatsachennotiz (Abschnitt 30, 21.09.2026):** `ergebnisse/faltenplan.json`
   > (`0e54ac5c…`) bleibt gesperrt und unverändert. Er ist der **registrierte
   > historische Stand** eines früheren Verfahrensstands (Trainingsfenster,
   > Embargo) und **nicht** der Faltenplan nach 4a; der Lauf liest ihn nicht.
   > Kein Ersatz, keine Streichung — **die Sperrliste beweist, dass nichts
   > bewegt wurde.** Der Plan nach 4a ist Registertext; genau eine Abbild-Datei
   > kommt vor dem Tag mit Hash als **neuer Punkt** auf diese Liste.
   >
   > ⚠️ **Schreibregel (Abschnitt 36.1, Fable 22b, TB-84, 22.09.2026):** Kein
   > Programm im Repo schreibt an einen Pfad, der auf dieser Liste steht oder
   > für sie bestimmt ist; Erzeuger schreiben **einmalig** und brechen bei
   > vorhandener Zieldatei ab (Rückgabewert 1 nach 36.5), auch bei gleichem
   > Inhalt. `faltenplan.py main()` schreibt heute ohne Abfrage genau hierher
   > (Z. 372–374, nur gelesen) — Voreinstellung und Schreibsperre sind nach
   > 36.1 (4) zu ändern, **vor** Z. 336, Reihenfolge 36.3; Freigabe steht aus.
   > Hash `0e54ac5c…` am 22.09.2026 vor und nach TB-84 gemessen und gleich.
3. **Selektionsstatistik, Plateau-Regel, Spitzen-Schwelle** —
   `auswertung.py`, `registerdaten.SPITZEN_SCHWELLE`
4. **Drawdown-Bedingung, `DD_Toleranz` und die vorab berechneten
   Benchmark-Drawdowns** — `benchmark.py`,
   `ergebnisse/benchmark_drawdowns.json`, **einschliesslich der
   Interpolationsregel**
   — und, als die Tabelle, die der Lauf liest,
   `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (Vollzug der
   Form (ii), 39.2, 23.09.2026)
   > ⭐ **Form (ii) (38.4, Fable 22h, TB-89, 23.09.2026) — Form steht fest,
   > Vollzug steht aus:** Punkt 4 nennt künftig **beide** Dateien;
   > `ergebnisse/benchmark_drawdowns.json` (`a163c498…`) bleibt gesperrt und
   > unverändert als **registrierter historischer Stand** mit Tatsachennotiz,
   > wie Punkt 2 (30.3); `ergebnisse/benchmark_drawdowns_vt.json` ist die
   > Tabelle, die der Lauf liest. Nicht (i) (Streichen) und nicht (iii)
   > (ERSETZT-Marke). ⛔ **Der Punkttext oben ist NICHT geändert** — der Vollzug
   > ist Plan-Punkt 8 (37.3, kein Amendment, 38.3) und wartet auf zwei offene
   > Fragen an Fable (Anfrage 22i: „grün" als Fertigkriterium; welche Tabelle
   > für `t3_supertrend`).
   >
   > ⭐⭐ **VOLLZOGEN (39.2, TB-94, 23.09.2026).** Der Punkt nennt jetzt beide
   > Dateien. ⚠️ **Zwei Berichtigungen am Kasten darüber:** (1) Die Tabelle,
   > die der Lauf liest, ist **nicht** `benchmark_drawdowns_vt.json`, sondern
   > die Neurechnung `benchmark_drawdowns_2026-09-23_nach_wegA.json`
   > (`64fb2912…`) — so entschieden in **23b**, nachdem 23a die Bedingung
   > „die Tabelle folgt dem registrierten Faltenplan" gesetzt hatte; `_vt.json`
   > trägt bei `t3_supertrend` eine Falte `2018`, die der Plan seit TB-72 nicht
   > mehr hat. (2) Die zwei offenen Fragen aus 22i sind **beide beantwortet**:
   > das Fertigkriterium in **23a** (berichtigt in 39.1), die Tabelle in
   > **23a/23b** (vollzogen hier). Der Kasten oben ist als Zitat richtig und
   > bleibt unverändert; überholt ist an ihm nur der Dateiname und der Satz
   > „Vollzug steht aus".
5. **Abbruchkriterien und Kapitalregel** — `auswertung.py`
6. **Benchmark-Definitionen** — gleichgewichtete Tagesrenditen,
   point-in-time, `benchmark.py::bh_tagesrenditen`
7. **N-Buchführung und Clusterschwelle** —
   `registerdaten.N_HISTORISCH_JE_BOT`, `CLUSTER_SCHWELLE = 0,9`
   > ⚠️ **Ort registrierter Werte (37.5, Fable 22d, TB-87, 22.09.2026):**
   > `CLUSTER_SCHWELLE` steht hier ohne Ort, `N_HISTORISCH_JE_BOT` mit Modulnamen,
   > aber ohne Pfad und Hash (Sonde: „kein Dateipfad“). Nach 37.5 (1)–(3) bekommen
   > `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` **genau ein** Modul, das mit
   > Hash auf die Sperrliste kommt (Handwerk mit Freigabe, offen). Heute
   > gemessen (37.5 (4)): `registerdaten.py:99` `CLUSTER_SCHWELLE = 0.90`,
   > `registerdaten.py:115` `N_HISTORISCH_JE_BOT` — keiner davon steht mit Hash
   > auf dieser Liste; bis zur Umsetzung **ungeschützt**. Die Werte ändern sich
   > nicht.
   >
   > ⭐ **Der Ort steht schon (38.5, Fable 22h, TB-89, 23.09.2026):**
   > `registerdaten.py` ist ein Modul, ein Ort, und steht als Punkt 1 auf der
   > Sperrliste — **hier ist nichts zu verschieben.** Punkt 7 bekommt den Ort
   > nachgetragen (`registerdaten.py`, `CLUSTER_SCHWELLE` und
   > `N_HISTORISCH_JE_BOT`); die Sonde prüft Datei plus Wert. Fables Kandidat
   > aus 22d war für Punkt 7 keiner. Der Nachtrag selbst ist Handwerk (TB-90).
8. **Universumsdateien und point-in-time-Regel** — `config/top25_symbols.txt`,
   `config/sp500_top150.txt`, vier Jahre Vorlauf je Symbol
   > ⚠️ Der Halbsatz „vier Jahre Vorlauf je Symbol" ist **ersetzt** (Abschnitt 15,
   > Registertext 3). Die beiden Universumsdateien selbst bleiben unverändert auf
   > der Sperrliste, jetzt mit Hash im Nachtrag.
9. **Kosten (0,30 %) und Fill-Konvention** — `TRADING_FEE_PCT = 0,1` und
   `SLIPPAGE_PCT = 0,05` je Order, Ein- und Ausstieg; Einstieg zum
   Schlusskurs des Bestätigungsbalkens
   > ⚠️ **Ort registrierter Werte (37.5, Fable 22d, TB-87, 22.09.2026):** Dieser
   > Punkt nennt Werte, aber keinen Ort — *„Ein Sperrlistenpunkt, der einen Wert
   > nennt und keinen Ort, sperrt nichts — er legt fest."* Nach 37.5 (1)–(3)
   > bekommt er **genau ein** Modul mit `TRADING_FEE_PCT` und `SLIPPAGE_PCT`,
   > das mit Hash auf die Sperrliste kommt (Handwerk mit Freigabe, offen).
   > Heute gemessen (37.5 (4)): je eine Kopie in neun `forward_test.py` und
   > neun `backtest_*.py`; `messgroessen.py:59` `SLIPPAGE_PCT`, die Gebühr dort
   > als `GEBUEHR_PCT` (Z. 58) — keinen davon nennt dieser Text; bis zur
   > Umsetzung **ungeschützt**. Die Werte `0,1` / `0,05` ändern sich nicht.
   >
   > ⭐⭐ **Neun Importe, nicht neun überwachte Kopien (38.5, Fable 22h, TB-89,
   > 23.09.2026):** Kein Laufmodul trägt eine eigene Kopie — die neun
   > `backtest_*.py` ersetzen ihre Zuweisung durch den **Import** aus einem
   > neuen Modul, das mit Hash auf diese Liste kommt. Fable: *„Ein Import ist
   > keine Prüfung, sondern eine **Struktur**"* (38.5). Der Papierpfad (`forward_test.py`) und
   > `messgroessen.py` (`GEBUEHR_PCT`) bleiben **überwachte** Kopien. Modul und
   > Importe: TB-90; bis dahin gilt die Marke oben.
   >
   > ⭐ **Tatsachennotiz (38.7 (b), Slippage):** **9 von 9** `backtest_*.py`
   > tragen `SLIPPAGE_PCT = 0.05` und rechnen `2 * (TRADING_FEE_PCT +
   > SLIPPAGE_PCT)` = **0,30 %** — genau die Summe dieses Punktes, Ein- und
   > Ausstieg. Formabweichung ohne Wertunterschied bei `t3_supertrend`
   > (`pnl_pct -= …`). Gemessen in Anfrage 22i (HEAD `ec54618`), in TB-89 lesend
   > nachgemessen am Stand `da251da`, gleich.
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

> ⭐⭐ **Tatsachennotiz (38.3, Fable 22h, TB-89, 23.09.2026):** Diese Regel
> betrifft Bug-Fixes **nach** Beginn des Laufs; das Protokoll ist der Ort der
> **Läufe** und ihrer Amendments, und vor dem ersten Lauf gibt es nichts, was
> dort stünde. Der Vollzug von Sperrlistenpunkt 4 vor dem Tag ist daher **kein
> Amendment nach 10.1** und erzeugt **keinen Protokolleintrag**, sondern ist
> eine beauftragte Änderung nach 37.3. Das Protokoll entsteht mit dem Erzeuger
> und beginnt mit dem Stand des Tags. Wortlaut und Grund in **38.3**.

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

> ⭐ **Ergänzung (40.7, Fable 24a, TB-96, 24.09.2026) — jede Mutationsprobe
> hat eine Gegenprobe**, die zeigt, dass sie rot werden kann; eine
> Mutationsprobe ohne Gegenprobe zählt nicht als Prüfung. Vor dem Tag wird
> die Gegenprobe für alle acht einmal geführt und als Tatsachennotiz
> festgehalten (TB-97). Anlass: `F4` hat mit `<=` statt `<` drei Wochen
> „bestanden", ohne je gemessen zu haben. Wortlaut in **40.7**. Die Zahlen
> oben („150 Prüfungen, davon acht Mutationsproben") bleiben zeichengleich;
> der Test zählt heute 165 Prüfungen (40.1).

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
> ⚠️ **(c) ERSETZT durch Abschnitt 23 (Berichtigung TB-66, 20.09.2026), 23.3 — der Wortlaut bleibt stehen.**
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
> ⚠️ **(b) ERSETZT durch Abschnitt 25 (Berichtigung TB-72, 20.09.2026), 25.3 — der Wortlaut bleibt stehen.** Der Satz hatte keine Richtung; seine Begründung deckt nur den Fall, dass der Trockenlauf **später** liegt. Die Neufassung als Konjunktion enthält genau diesen Fall und keinen anderen.
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

> ⚠️ **Tatsachennotiz zu dieser Tabelle (36.4, Fable 22b, TB-84, 22.09.2026):**
> ⚠️ bei `elliott_wave`, Spalte Bestätigung ab, trägt keine Erklärung; nicht
> als Beleg verwendbar. Die Zeile bleibt zeichengleich stehen, samt `⚠️`; die
> Deutung aus Anfrage 21g Punkt 3 ist zurückgezogen (36.4).

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

> ⭐⭐ **Tatsachennotiz (38.3, Fable 22h, TB-89, 23.09.2026):** Der Vollzug von
> Sperrlistenpunkt 4 vor dem Tag ist eine **beauftragte Änderung nach 37.3** —
> Registertext, Tatsachennotiz mit altem und neuem Hash, neues Abbild. **Kein
> Amendment nach 10.1, kein Protokolleintrag**; das Protokoll entsteht mit dem
> Erzeuger. Das Wort „Amendment" oben bleibt zeichengleich; es stammt aus einer
> Zeit, in der der Begriff für beides stand (23.6). Die Reihenfolge-Entscheidung
> gilt weiter. Die Form des Vollzugs steht in **38.4**.

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

> ⚠️⚠️ **Tatsachennotiz zur ersten Zeile (38.7 (d), TB-88, Messstand
> `8851f67`):** „rot" heisst heute: `test_vorregistrierung.py` **stürzt ab**
> (`KeyError: '2017'` in `auswertung.py`, Funktion `zulaessigkeit`), **0
> bestanden, 0 gescheitert**. Nach dem simulierten Vollzug: **163 bestanden,
> 2 gescheitert** (`G6`, `H3`) — beide hängen am Faltenplan, nicht an der
> Tabelle. ⚠️ **OFFENE FRAGE bei Fable (Anfrage 22i, Abschnitt 3), nicht
> entschieden:** ob „grün" Fertigkriterium des Vollzugs bleibt. Bis dahin gilt
> die Zeile oben unverändert: offen durch eigene Änderung, blockierend für den
> Tag. Einzelheiten in **38.7 (d)**.

> ⭐⭐ **Berichtigung des Fertigkriteriums (39.1, Fable 23a/23f, TB-94,
> 23.09.2026):** Die offene Frage der Tatsachennotiz darüber ist beantwortet —
> „grün" ist **nicht** Fertigkriterium des Vollzugs, sondern
> **Tag-Vorbedingung**. Der Vollzug (Plan-Punkt 8) ist fertig, wenn unter
> anderem der Absturz weg ist und der Test bis zur Schlusszeile läuft; beides
> ist seit TB-92 erfüllt (`0292e92`: 163/2, `G6`, `H3`). ⚠️ **Die erste Zeile
> der Tabelle oben gilt für den Tag unverändert:** `test_vorregistrierung.py`
> ist rot, offen durch eigene Änderung, blockierend für den Tag — geschlossen
> wird das mit dem Planpunkt „Testannahmen folgen dem Register" (23a; TB-95),
> nicht mit Punkt 8. Die zweite Zeile (Widerspruch zwischen Faltenplan und
> Tabelle) ist mit dem Vollzug geschlossen (39.2, 39.4). Die dritte Zeile ist
> mit 39 **nicht** erledigt (der ERZEUGT-Block in Abschnitt 3 ist nicht neu
> erzeugt, TB-92 A4). Ersatztext in **39.1**.

> ⭐⭐ **Tag-Vorbedingung für diesen Test erfüllt (40.1, TB-95/TB-96,
> 24.09.2026):** `test_vorregistrierung.py` (`73c9b837…`, `9e2a071`) läuft
> **165/165, rc 0** — die erste Zeile der Tabelle oben („bleibt **rot** …
> blockierend für den Tag") ist für den Stand vom 23.09.2026 **geschlossen**,
> mit dem Planpunkt „Testannahmen folgen dem Register" (`G6`, `H3`). ⚠️ Weitere
> Änderungen an diesem Test sind beschlossen (40.8 (a)–(c), TB-97); jede muss
> ihn grün hinterlassen. Die Tabelle bleibt zeichengleich.

⚠️ **Was diese Ergänzung nicht tut:** kein Amendment, keine Zahl der Sperrliste
bewegt, kein Registertext umgeschrieben. Sie hält eine **Reihenfolge**-Entscheidung
fest, nicht eine Sachentscheidung über die Tabelle.

*Nachgetragen in TB-56b, 19.09.2026.*

---

## 22. Registertexte aus der Methodenantwort vom 19.09.2026 (vor dem Tag)

**Datiert angehängt. Nichts entfernt. Kein bestehender Registertext wird
umgeschrieben.** Herkunft: Fables Antwort auf die vier Fragen aus
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-19_pruefungsregistrierung.md`,
eingegangen am 19.09.2026.

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Entscheidung.**
Sie entsteht **vor** dem signierten Tag und ohne Kenntnis eines
Selektionsergebnisses — es hat keinen Lauf gegeben, dessen Sieger jemand kennen
könnte.

⚠️ **Fables Formulierungen stehen wörtlich; die Präzisierungen dieser Sitzung
stehen getrennt davon** (22.6), damit niemand sie später für seine hält.

---

### 22.1 Registertext, allgemeine Prüfregel *(neu)*

> **Jede Prüfung, deren Ergebnis eine registrierte Entscheidung ändern oder eine
> Zulassung beeinflussen kann, ist vor ihrem Lauf mit Zahl, Identität und
> Nullmodell registriert und zählt zur Familie. Jede andere Prüfung ist
> Bericht.**

**Fables Begründung, wörtlich:** *„Zahl und Identität der Prüfungen stehen vor
dem Lauf fest"* ist keine Eigenschaft von Verfahren B, *„sondern das, was ein
Register ist: die Vorfestlegung der Prüfmenge, damit Vielfachheit zählbar
bleibt."* Verfahren B ist eine Instanz (Prüfungen = Raster × Falten ×
Kriterien); Hypothesen, Graphkanten und Kill Tests sind andere Instanzen mit
anderem Index.

⭐ **Warum das Nullmodell in die Registrierung gehört:** *„weil eine Prüfung ohne
Null keine Prüfung ist."*

⭐ **Warum vor dem Tag:** *„weil der Tag festlegt, was nach ihm die Selektion
noch berühren darf."*

⇒ **Damit ist der Registerbaustein benannt, der in allen fünf eingereichten
Forschungsschichten unter fünf verschiedenen Namen vorkam** (Prediction Ledger,
Data Lineage, Research Ledger, Hypothesis Registry, Versuchsregister). **Fünf
Namen, ein Baustein.**

---

### 22.2 Registertext, Kill-Test-Berichtswerte *(neu)*

> Der Lauf berichtet je Bot für den Plateau-Gewinner drei Werte:
> **Ertragsanteil der besten Falte**, **Ertragsanteil des besten Symbols**,
> **Ertragsanteil der fünf besten Trades**.
>
> ⚠️ **Sie tragen keine Schwelle und sind kein Abbruchkriterium.** Sie sind
> Bericht im Sinne von 22.1; **N bleibt unverändert.**

**Betreiberentscheidung 19.09.2026**, auf Entscheidungsvorlage mit drei Wegen
und benannter Empfehlung: ohne Schwelle. Fables Begründung, wörtlich: *„Ohne
Schwelle sind sie kein Kriterium, N bleibt, und nach dem Lauf steht die Zahl da,
statt dass jemand sie sucht."*

⚠️ **Die Folge, die dazugehört und die nicht verschwiegen wird:** Wer diese
Werte nach dem Tag zu einem Tor machen will, trifft damit eine **nachträgliche
Wahl** (22.5, Kategorie B). Die Schwelle jetzt wegzulassen heisst, sie später
nicht mehr als Zulassungskriterium nutzen zu können, ohne den Lauf neu zu
registrieren. **Das ist kein Nachteil dieser Regel, sondern ihr Zweck.**

---

### 22.3 Registertext, Abschalt- und Zuschaltregeln *(neu)*

> Eine Regel, die einen Bot bei Leistungsabweichung **abschaltet oder wieder
> zuschaltet**, ist **keine Betriebsentscheidung**. Sie ist eine Strategie über
> Strategien, mit Rückblick und Schwelle als Parametern, gewählt auf denselben
> Daten.
>
> Sie ist entweder
> **(a)** eine **Konkurrentin von 6d** — dann Overlay-Kandidat: feste
> Parameter, absolute Prüfung gegen die Null (keine Regel), **nach** dem Tag,
> Zulassung an die Bestätigungsperiode geknüpft; oder
> **(b)** eine **Notbremse nach 6e** — manuell, protokolliert, nie aufwärts.
>
> **6d und 6e werden dadurch nicht ersetzt.**
>
> ⛔ Ein **automatisches Wiederzuschalten** („Self-Healing Pool") ist mit dem
> Register **unvereinbar**, nicht nur unregistriert: **6d, letzter Satz** —
> *„Rückkehr nur über einen neuen registrierten Lauf."*

**Fables Begründung, wörtlich:** *„Auf einem Random Walk verkauft die Regel
Verlierer, kauft Gewinner zurück und bezahlt beides."*

---

### 22.4 Registertext 6, Ergänzung — die Notbremse auf einen In-Sample-Befund *(neu)*

> Die **Notbremse aus 6e bleibt jederzeit zulässig.** Wird sie auf einen Befund
> **aus dem Selektionslauf selbst** gezogen, ist das eine **nachträgliche
> Wahl**: Sie wird als solche im Protokoll vermerkt, und **kein anderer Bot und
> kein anderer Parametersatz steigt dadurch auf.** Ein Aufstieg entsteht allein
> aus **6c** auf Bestätigungsdaten oder aus einem **neuen registrierten Lauf**.

⭐ **Diese Zeile schliesst eine Falltür, die Fable selbst aufgemacht hat**, mit
seinen Worten: *„Wer sie auf einen In-Sample-Befund zieht, trifft die
nachträgliche Wahl in Verkleidung — zulässig, aber als Wahl zu protokollieren,
und der Zweitplatzierte steigt dadurch nicht auf."*

---

### 22.5 Die Antwort auf den Anlassfall — Kategorie (B)

**Die Frage war:** Nach dem Tag zeigt ein Kill Test, dass die Leistung des
gewählten Bots an einem Jahr hängt. Berichtigung, nachträgliche Wahl, oder
Quelle des Grundes?

> **Die Kategorie betrifft die HANDLUNG, nicht den Befund.** Der Befund ist ein
> Messwert und wird berichtet wie jeder andere. **Den Zweitplatzierten zu
> nehmen, ist eine nachträgliche Wahl — Kategorie (B).**

**Warum (A) ausscheidet, wörtlich:** *„Eine Berichtigung löst einen Widerspruch
im Register auf oder gleicht an eine Quelle an; hier war nichts falsch, der
Sieger wurde nach den registrierten Kriterien richtig gewählt. Ein Kriterium,
das nicht registriert war, kann ihn nicht rückwirkend disqualifizieren — sonst
ist jedes Kriterium, das jemand nach dem Lauf einfällt, eine ‚Berichtigung'."*

**Und (C) kollabiert** — aber nicht in *„vorher registrieren oder nie"*, sondern
in **„oder Bericht, und registriert für den nächsten Lauf"**. Der Weg, in vier
Schritten: der Befund geht in den Bericht · der Kill Test wird Kriterium eines
**neuen registrierten Laufs**, mit dem Vermerk, dass seine Wirkung auf den
heutigen Sieger bekannt war · der neue Lauf wertet das ganze Raster unter den
erweiterten Kriterien aus, N wächst, Familienbuchführung · **der
Zweitplatzierte wird nicht gewählt — er gewinnt, oder er gewinnt nicht.**

⚠️ **Abgrenzung, damit sie nicht verlorengeht:** Der offene Punkt der Übergabe
lautet *„die Drei-Kategorien-Regel in Registertext 0"*. **Fable liefert etwas
anderes und Breiteres** — die allgemeine Prüfregel aus 22.1 über die
**Prüfmenge**. **F17 bleibt, was es war:** eine Einordnungsregel für Änderungen,
im Register einmal genannt (Abschnitt 19) und hier erneut angewandt. Beides
zusammenzuwerfen wäre bequem und falsch.

---

### 22.6 Zwei Präzisierungen an Fables Begründungen — dieser Sitzung, nicht seine

**Nach Prüfprinzip C1 an der Quelle nachgelesen, nicht übernommen.** Drei seiner
vier Registerbezüge halten wörtlich: 6d (quartalsweise, Schwellen vorab: 1,25 ×
die tiefste Selektionsfalte **oder** Netto-Sharpe < 0 nach 60 Trades), 6e
(*„jederzeit auf Schatten … aber nie hinauf"*) und Abbruchkriterium (a)
(*„Falten-Median des Netto-Sharpe ≤ 0"*). Zwei Stellen sind ungenau:

| | Fables Satz | ⚠️ gemessen |
|---|---|---|
| **1** | *„Der ‚Self-Healing Pool' schaltet wieder zu — das ist der Aufstieg ohne Bestätigung, den 6e ausschliesst."* | **Fundstelle ungenau, Schluss überlebt.** 6e verbietet dem **Betreiber** das Hinaufsetzen. Ein **automatisches** Wiederzuschalten trifft **6d, letzter Satz**. Beide sperren; 6d ist die schärfere Fundstelle, und 22.3 zitiert sie |
| **2** | *„sechs Falten nahe null ergeben Median ≤ 0, Abbruchkriterium (a)"* | **nicht zwingend.** „Nahe null" ist nicht „≤ 0": sind die sechs leicht **positiv**, ist der Median leicht positiv und (a) greift nicht. ⭐ Der Faltenmedian ist gegen *„hängt an einem Jahr"* ein **schwacher**, kein exakter Kill Test. **Fable räumt die Lücke im nächsten Satz selbst ein** — der Schluss überlebt, die Begründung ist schwächer, als sie klingt |

⚠️⚠️ **Und ein Befund aus der Reihenfolge der Ereignisse:** Fables Antwort ist
**vor** der Berichtigung in Abschnitt 21 entstanden. Die Faltenzahlen haben sich
am Abend des 19.09. geändert — `elliott_wave` **4**, `t3_supertrend` und
`rsi2_crypto` **7**, vier Bots **8**, zwei Bots **9** (21.4). ⇒ **„Ertragsanteil
der besten Falte" ist über die neun Bots nicht gleich skaliert:** bei vier
Falten ist der Anteil strukturell grösser als bei neun, ohne dass der Bot
schlechter wäre. **Als Berichtswert ohne Schwelle ist das unschädlich; als Tor
wäre es ein Fehler gewesen.** ⭐ Das stützt die Entscheidung aus 22.2 im
Nachhinein — es war ausdrücklich **nicht** ihr Grund, sondern ein Fund danach.

---

### 22.7 Was dieser Abschnitt NICHT tut

| | |
|---|---|
| ⚠️ | **Keine Schwelle gesetzt.** Die drei Werte aus 22.2 sind Bericht, kein Kriterium; **N bleibt bei 653** |
| ⚠️ | **Kein bestehender Registertext umgeschrieben.** 6c, 6d und 6e stehen unverändert; 22.4 ergänzt 6e, ersetzt es nicht |
| ⚠️ | **Kein Amendment.** Sperrliste Punkt 4 bleibt unberührt; die Entscheidung dazu steht in 21.9 |
| ⚠️ | **Kein Registertext 0 zur Drei-Kategorien-Regel.** Siehe die Abgrenzung in 22.5 — dieser Punkt der Übergabe ist damit **nicht** erledigt, sondern als etwas anderes erkannt |
| | **Kein Selektionslauf, kein signierter Tag, kein Zeitanker** |

---

### In einfacher Sprache

**Was wir wissen wollten:** Gilt „vorher festlegen, was geprüft wird" nur für
unser eines Auswahlverfahren — oder immer? Und was passiert, wenn nach dem
Einfrieren ein echter Mangel am Gewinner auffällt?

**Was herauskam:** Die Regel gilt immer, und sie steht ab jetzt als eigener Satz
im Regelwerk. Und der unangenehme Teil ist bestätigt: Fällt der Mangel
**nachher** auf, darf er den Gewinner nicht absetzen. Der Befund wird berichtet,
der Zweitplatzierte rückt **nicht** nach — er müsste einen neuen, erneut
angemeldeten Durchgang gewinnen.

**Warum das so ist:** Jeder Test, der nach dem Lauf erfunden wird, ist in
Kenntnis des Siegers erfunden worden. Dass er trotzdem unabhängig sei, kann
niemand belegen.

**Was das bedeutet:** Drei neue Kennzahlen werden künftig mitberichtet — wie
viel des Ertrags am besten Jahr, am besten Symbol und an den fünf besten
Geschäften hängt. Sie haben **bewusst keine Grenze**, sind also kein
Ausschlusskriterium; sie stehen einfach da, damit später niemand danach suchen
muss. Und eine Hintertür ist zugemacht: Der Betreiber darf jeden Bot jederzeit
abschalten — aber wenn er das wegen einer Zahl aus dem Auswahllauf tut, wird
das als Wahl protokolliert, und es steigt dadurch niemand auf.

*Nachgetragen 19.09.2026, nach Fables Methodenantwort. Die wörtlichen Zitate
sind seine; die Präzisierungen in 22.6 sind es nicht.*

---

## 23. Berichtigung zu Registertext 3b (c) — der Benchmark wird tagesgenau (TB-66, 20.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben —
der berichtigte Satz bleibt in Abschnitt 16.7 stehen** (dort seit heute mit der
Marke *„(c) ERSETZT durch Abschnitt 23"*), wird hier wörtlich zitiert und von
der Festlegung, der Messung und dem Ersatztext gefolgt. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und die Form von
Abschnitt 21.

**Anlass:** `docs/ERGEBNIS_TB-65_benchmarkschranke.md` hat gemessen, dass der
Wortlaut *„in dieser Falte geladen"* zwei Lesarten zulässt — **VH** (geladen,
ganze Falte) und **VT** (geladen, ab dem Tag, an dem der Loader das Symbol
handelbar macht) — und dass beide in den frühen Krypto-Falten weit
auseinanderliegen (`turtle_soup_crypto` 2018: **−87,92 %** gegen **−3,60 %**
bei 100 % Exposure). Die Frage ging an Fable
(`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20_benchmarkfenster.md`); seine
Antwort vom 20.09.2026, 15:19 Ortszeit, liegt wörtlich in
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-20_benchmarkfenster.md`. **Er legt
VT fest.** Die Umsetzung ist `docs/auftraege/MAC_TB-66_benchmark_tagesgenau.md`,
das Ergebnis `docs/ERGEBNIS_TB-66_benchmark_tagesgenau.md`.

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Berichtigung.**
Der Grund kommt aus dem Registertext selbst — aus seinem eigenen Zweck-Satz
*„Bot und Benchmark leben in derselben Menge"* —, nicht aus der Wirkung. ⚠️
**Die Wirkung ist bekannt und geht gegen die Bots** (VT ist in den frühen
Krypto-Falten die strengere Lesart); sie steht in 23.4 vermerkt. **Sie ist nicht
der Grund.** Es hat kein Selektionslauf stattgefunden; kein Parametersatz ist
bewertet, kein Ergebnis erzeugt.

---

### 23.1 Der berichtigte Satz, wörtlich

Aus **Abschnitt 16.7**, Registertext 3b, Ergänzung (c) (Commit `1bc2d57`,
16.09.2026):

> **(c)** ⭐ **Der Benchmark einer Falte** — für die Drawdown-Nebenbedingung
> (Abschnitt 4) und für Rang 3 — **wird auf den in dieser Falte geladenen
> Symbolen des Bots gerechnet, nicht auf dem vollen Universum. Bot und
> Benchmark leben in derselben Menge.**

⚠️ **Was daran unpräzise ist — und was ausdrücklich nicht.** Richtig und
unverändert ist die Menge: die vom Loader des Bots geladenen Symbole, nicht das
volle Universum. Richtig und unverändert ist der Zweck-Satz. **Unpräzise ist
der Zeitbezug** *„in dieser Falte geladen"*: er sagt nicht, ob ein Symbol, das
der Loader am 30. Dezember handelbar macht, für den 30. und 31. Dezember zählt
oder für das ganze Jahr. Fable dazu, wörtlich: *„Der Wortlaut ‚in dieser Falte
geladen' war meiner, und er war unpräzise. Der Begründungssatz war es nicht."*

---

### 23.2 Die Festlegung und ihre Gründe (Fable, 20.09.2026)

> **VT — und der Grund steht im Registertext selbst, nicht in der Wirkung.**
>
> *Die Menge, in der ein Bot lebt, ist tagesgenau — er kann ein Symbol an
> keinem Tag halten, an dem sein Loader es nicht geladen hat. Ein Benchmark,
> der es für die ganze Falte hält, ist eine Alternative, die dem Bot nicht
> offenstand, und genau dagegen war 3b (c) geschrieben.*

**Zwei Gründe, beide aus dem Register, keiner aus der Messung:**

| | |
|---|---|
| **1** | ⚠️ **Unter VH ist die Nebenbedingung dort leer, wo sie binden soll.** In Falte 2018 hat der Bot vor dem 30.12. keine Position, sein Drawdown ist nahe null; der zulässige wäre 1,25 × −87,9 % — **jeder Parametersatz besteht, egal was er tut.** Eine Nebenbedingung, die in dünnen Falten automatisch erfüllt ist, prüft nichts — und die dünnen Falten sind genau die, in denen 3b (d) Rauschen erwartet |
| **2** | ⚠️⚠️ **Unter VH erzeugt Rang 3 Alpha aus Nichtteilnahme.** Benchmark −88 %, Bot ≈ 0 ⇒ **+88 Prozentpunkte Alpha daraus, dass der Bot nichts halten *konnte*.** Rang 3 misst dann, wie lange der Loader gebraucht hat — die Nullen-als-Diversifikation-Fehlerklasse aus `L1` in neuer Kleidung |

**Zu Lesart H (16.2) — kein Widerspruch:** H beantwortet, **ob** eine Falte
zählt (ab einem handelbaren Tag). VT beantwortet, **was der Benchmark an jedem
Tag hält**. H mit VH zusammen wäre der Widerspruch: eine Falte, die wegen eines
Tages zählt, bekäme einen Benchmark aus 365 Tagen, an denen der Bot nicht dabei
war.

**Rang 3 — dieselbe Lesart, zwingend:** *„Es ist ein Benchmark-Objekt mit zwei
Verwendungen, nicht zwei Benchmarks."* Ein Satz in 3b (c) genügt; keine eigene
Festlegung.

**Form — Registertext, nicht Tatsachennotiz:** *„Eine Tatsachennotiz kann sie
festhalten, nicht schaffen"* (Fable, 19.09.2026, Frage c). 3b (c) selbst wird neu
gefasst; die gemessenen Zahlen kommen in die Berichtigungsnotiz (23.4).

---

### 23.3 Der Ersatztext

> **Registertext 3b (c), Fassung 20.09.2026 — ersetzt die Fassung in 16.7.**
>
> Der Benchmark einer Falte wird **tagesgenau** aus den Symbolen gebildet, die
> der Loader des Bots an diesem Tag handelbar macht: gleichgewichtet, täglich
> rebalanciert (Konvention; sie ist die einzige Gewichtung, die bei wechselnder
> Menge ohne weitere Regel auskommt). Der Benchmark einer Falte ist an genau
> den Tagen definiert, an denen mindestens ein Symbol des Bots nach 3b (b)
> handelbar ist. Ein Tag, an dem kein Symbol handelbar ist, gehört nicht zum
> Benchmark — er wird nicht mit Rendite 0 geführt, sondern gar nicht.
> Derselbe Benchmark gilt für die
> Drawdown-Nebenbedingung (Abschnitt 4) und für Rang 3. Bot und Benchmark leben
> an jedem Tag in derselben Menge.

⭐ **Geschlossen in TB-71, 20.09.2026 — der Platzhalter ist gefallen.** An
seiner Stelle steht der Satz zur Zeitachse, verankert an Registertext 3b (b),
der Grösse, die es gibt und die registriert ist. Er ist **nicht** Fables erste
Fassung: seine lautete *„Tage, an denen kein Symbol handelbar ist, tragen
Rendite 0"* und wurde von ihm selbst zurückgezogen, weil sie einen Mechanismus
vorschrieb statt ein Prinzip (`docs/projektfuehrung/FABLE_ANTWORT_2026-09-20b_kalender.md`,
Teil 2). Seine zweite Fassung band den Benchmark an den Kalender des
Bot-Kapitalpfades — **den es nicht gibt**: der Pfad ist ereignisindiziert
(`shared/zuteilung.py:720–735`, gemessen 20.09.2026). Die dritte Fassung, die
jetzt hier steht, wurde in `FABLE_ANFRAGE_2026-09-20c_kapitalpfad.md`
vorgeschlagen und von Fable übernommen (`FABLE_ANTWORT_2026-09-20c_kapitalpfad.md`,
Teil 1): *„Meine Fassung hat einen Kalender vorausgesetzt, den der Kapitalpfad
nicht hat; eure setzt nichts voraus."* Die Absätze und die Tabelle W/C darunter
bleiben als Vorgeschichte stehen (append-only); die Tabelle trägt die Marke
ERSETZT.

**Tatsachennotiz zu 3b (c), Satz zur Zeitachse (TB-71, 20.09.2026):**

> Die Umsetzung lässt den ersten Kurstag je Falte aus, weil `pct_change` dort
> keine Rendite liefert. Abweichung gegenüber dem Satz: höchstens ein Tag je
> Falte. Wirkung auf jede registrierte Zahl: null — 0 abweichende Stufen in
> Drawdown und `DD_Toleranz` über 78 × 100 (TB-66, Nachweis 4). Wird
> `bh_tagesrenditen` je aus anderem Grund angefasst, ist `fillna(0)` auf diesem
> Tag eine Berichtigung des Codes an den Satz.

**`handelstage`** bleibt unverändert die **W-Spalte** — die Länge des
gemeinsamen Kalenders.

**Der Wortlaut ist Fables**, mit einer Ausnahme, die er selbst verlangt hat:
*„nur eines darf im Register stehen, und es muss das sein, was der Code tut.
Vor dem Eintrag nachsehen."* Nachgesehen: Fables Satz *„Tage, an denen kein
Symbol handelbar ist, tragen Rendite 0"* **trifft den Code nicht** —
`benchmark.py::bh_tagesrenditen` schliesst mit `.dropna()` solche Tage aus,
statt sie mit 0 zu führen. ⚠️ **Ein Registertext, der etwas anderes sagt als
der Code, ist genau der Fehler, den Abschnitt 21 berichtigt hat.** Deshalb steht
an dieser Stelle ein sichtbarer Platzhalter und keine der beiden Fassungen, bis
der Betreiber entscheidet:

> ⚠️ **ERSETZT (TB-71, 20.09.2026) durch den Satz zur Zeitachse oben — keine der beiden Fassungen ist gewählt worden.** Die Tabelle bleibt stehen: sie hält fest, wogegen entschieden wurde, und sie enthält die Messung, die C_voll ausgeschlossen hat (`t3_supertrend` 2018 hätte 365 Handelstage statt 0; 23.4, Wirkung 3).

| | Fassung | Folge |
|---|---|---|
| **W** | Wortlaut an den Code: *„Tage, an denen kein Symbol handelbar ist, gehen nicht in den Benchmark ein."* | keine Codeänderung; `handelstage` zählt nur Tage mit Rendite |
| **C** | Code an den Wortlaut: *„Tage, an denen kein Symbol handelbar ist, tragen Rendite 0."* — `.dropna()` durch `.fillna(0)` ersetzt | ⚠️ ändert `bh_tagesrenditen` (Sperrliste Punkt 6) und die berichtete `handelstage`-Zahl; `.fillna(0)` allein setzt den Wortlaut nur teilweise um (23.4, Tabelle) |

**Gemessen, ob es einen Zahlenunterschied macht (23.4):** für den **Drawdown
keinen** — auf keiner der 7 800 Falte-Stufen-Kombinationen, bei keinem Bot in
der `DD_Toleranz`; für **`handelstage` einen**, in vier bzw. fünf frühen
Krypto-Falten. **Hier wird nicht entschieden.**

**Was „handelbar an diesem Tag" heisst — Registertext 3b (b), nicht neu:** Ein
Symbol ist an einem Tag handelbar, wenn seine Historie bis zu diesem Tag die
registrierte Loader-Schranke erreicht — `MIN_HISTORY_DAYS` **500 / 730 / 1 825**
als Zeitspanne, bei `elliott_wave` `MIN_HISTORY_HOURS` **17 520** als
Kerzenzahl. Das ist die Schranke aus 3b (b), tagesgenau gelesen; sie wird hier
angewendet, nicht neu festgelegt.

---

### 23.4 Die Berichtigungsnotiz — Lesart, Wirkung, Grund, Herkunft

| | |
|---|---|
| **Lesart** | **VT** — geladen, ab dem Tag, an dem der Loader das Symbol handelbar macht; innerhalb der Falte wechselt die Menge |
| **Grund** | der Zweck-Satz von 3b (c): *„Bot und Benchmark leben in derselben Menge"* — die Menge des Bots ist tagesgenau |
| **Herkunft** | Fables Antwort vom 20.09.2026 (`FABLE_ANTWORT_2026-09-20_benchmarkfenster.md`), umgesetzt in TB-66 |
| **Wirkung, gemessen** | siehe die drei Tabellen unten; Lauf `research/vorregistrierung/benchmark.py` (Commit `19a1996`, 20.09.2026, 14:30 UTC), Ergebnis `research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json` **daneben** — `benchmark_drawdowns.json` (`a163c498…36d1ee`) und `benchmark_drawdowns_neu.json` (`e06812d2…4a062`) byteweise unverändert |

**Wirkung 1 — die Falte, um die es ging** (100 % Exposure): `turtle_soup_crypto`
und `volatility_breakout_crypto` 2018: **−3,60 %** (VT, **1** Handelstag, BTC
und ETH handelbar ab 2018-12-30) statt **−87,92 %** (VH, 365 Tage). `elliott_wave`
2018–2019: **−42,14 %** (133 Tage) statt −84,67 %; `t3_supertrend` 2019:
**−42,21 %** (136 Tage) statt −59,56 %; `t3_supertrend` 2018 bleibt **leer**
(kein Symbol erreicht 730 Tage vor 2019-08-17; Register 21.3 (b), 21.4).

**Wirkung 2 — `DD_Toleranz` je Bot, drei Fassungen nebeneinander** (25 / 50 /
100 % Exposure; gesperrt = TB-30a, TB-61 = `_neu.json` mit Vierjahresfilter, TB-66
= VT):

| Bot | Sel.-Falten gesperrt / TB-61 / TB-66 | gesperrt | TB-61 | **TB-66 (VT)** | Faktor TB-66 / TB-61 bei 25 / 50 / 100 % |
|---|---|---|---|---|---|
| `elliott_wave` | 0 / 4 / 4 | *Platzhalter* | −6,07 / −11,89 / −22,42 | **−16,42 / −31,21 / −55,91** | ×2,71 / ×2,62 / ×2,49 |
| `t3_supertrend` | 0 / 8 / 8 | *Platzhalter* | −3,24 / −6,32 / −12,01 | **−12,89 / −24,73 / −45,16** | ×3,98 / ×3,91 / ×3,76 |
| `rsi2_crypto` | 0 / 7 / 7 | *Platzhalter* | −6,48 / −12,64 / −24,02 | **−17,26 / −32,59 / −57,29** | ×2,66 / ×2,58 / ×2,39 |
| `turtle_soup_crypto` | 0 / 8 / 8 | *Platzhalter* | −3,24 / −6,32 / −12,01 | **−16,13 / −30,52 / −54,05** | ×4,98 / ×4,83 / ×4,50 |
| `volatility_breakout_crypto` | 0 / 8 / 8 | *Platzhalter* | −3,24 / −6,32 / −12,01 | **−16,13 / −30,52 / −54,05** | ×4,98 / ×4,83 / ×4,50 |
| `elliott_wave_stocks` | 7 / 9 / 9 | −2,18 / −4,33 / −8,55 | −2,18 / −4,33 / −8,55 | **−2,18 / −4,33 / −8,55** | ×1,00 |
| `rsi2_mean_reversion` | 7 / 8 / 8 | −2,18 / −4,33 / −8,55 | −3,35 / −6,61 / −12,89 | **−3,32 / −6,55 / −12,77** | ×0,99 |
| `turtle_soup_stocks` | 7 / 9 / 9 | −2,18 / −4,33 / −8,55 | −2,18 / −4,33 / −8,55 | **−2,18 / −4,33 / −8,55** | ×1,00 |
| `volatility_breakout` | 7 / 8 / 8 | −2,18 / −4,33 / −8,55 | −3,35 / −6,61 / −12,89 | **−3,32 / −6,55 / −12,77** | ×0,99 |

⚠️ **Die Krypto-Toleranzen werden gegenüber TB-61 um das 2,4- bis 5,0-fache
tiefer** (gemessen ×2,39 bis ×4,98 je nach Bot und Stufe). Das ist die in TB-65
vorgerechnete Richtung: TB-61 hatte in 17 der 35 Krypto-Selektionsfalten einen
**leeren** Benchmark (Vierjahresfilter, Drawdown 0,00), der den Median nach oben
zog. ⚠️ **Die Toleranz wird damit nachgiebiger — und das ist die Wirkung, nicht
der Grund** (F17, siehe Kopf dieses Abschnitts).

⚠️ **Die vier Aktien-Bots sind gegenüber TB-61 NICHT auf allen Stufen
unverändert** — anders als der Auftrag erwartete, der die Zeichengleichheit
aus TB-65 auf VT übertrug; zeichengleich war dort **VH**. Unter VT ändern sich
bei allen vier die Falten **2019** (92 Stufen; 100 %: −7,30 → **−7,23**), **2025**
(99 Stufen; −17,23 → **−16,99**) und **2026** (97 Stufen; −6,40 → **−6,31**),
weil `ANET` (handelbar ab 2019-06-05), `PLTR`/`DASH`/`ABNB` (2025-09-29 /
2025-12-08 / 2025-12-09) und `APP` (2026-04-14) **mitten in der Falte** handelbar
werden und TB-61 sie — Kursdaten vier Jahre vor Faltenbeginn — für die ganze
Falte mitzählte, also auch während der Peak-Trough-Episode davor. In 2021, 2023
und 2024 liegen die Eintritte **vor** der Episode, dort sind beide Pfade
identisch; 2018 fällt `ABBV` genau auf den Faltenbeginn. **`DD_Toleranz` ändert
sich dadurch bei `rsi2_mean_reversion` und `volatility_breakout`** (acht Falten,
Median als Mittel aus 2019 und 2023) **auf 98 von 100 Stufen** — von −12,89 auf
−12,77 bei 100 %, also **strenger** als TB-61 und weiterhin nachgiebiger als die
gesperrte Tabelle —, bei `elliott_wave_stocks` und `turtle_soup_stocks` (neun
Falten, Median = 2023) **auf keiner**. Beleg:
`docs/belege/TB-66/schritt4_aktien_gegenprobe.txt`.

**Wirkung 3 — die Messung zur offenen Formulierung (W gegen C):**

| Fassung | Drawdown, alle 78 Falten × 100 Stufen | `DD_Toleranz`, 9 Bots × 100 Stufen | `handelstage` |
|---|---|---|---|
| **C_lit** — `.fillna(0)` wörtlich | **0** Abweichungen | **0** Abweichungen | **4 Falten** um je +1: `elliott_wave` 2018–2019 133 → 134, `t3_supertrend` 2019 136 → 137, `turtle_soup_crypto` und `volatility_breakout_crypto` 2018 1 → 2 (der Tag des ersten Kurses, an dem noch keine Rendite vorliegt) |
| **C_voll** — der Wortlaut ganz: Kalender der Falte, fehlende Tage 0 | **0** Abweichungen | **0** Abweichungen | **5 Falten**: `elliott_wave` 2018–2019 133 → 730, `t3_supertrend` 2018 0 → 365 und 2019 136 → 365, `turtle_soup_crypto` und `volatility_breakout_crypto` 2018 1 → 365 |

⭐ **Die Differenz ist überall null ausser bei `handelstage`** — bei den vier
Aktien-Bots auch dort. ⚠️ Ein Tag mit Rendite 0 bewegt den Kapitalpfad nicht;
das ist der Grund, kein Zufall. **Und `.fillna(0)` allein setzt Fables Satz nur
teilweise um**: der Rahmen kennt nur Tage, an denen mindestens ein Symbol einen
Kurs hat; Tage **vor** dem ersten Handelbar-Tag eines Bots stehen gar nicht darin.
Wer C wählt, wählt zwischen C_lit und C_voll mit. Werkzeug und Rohausgabe:
`docs/belege/TB-66/tb66_dropna_gegen_fillna.py`, `schritt3_dropna_gegen_fillna.txt`,
`schritt3_dropna_gegen_fillna.json`.

---

### 23.5 Was der Code seit heute tut — Tatsachennotiz

| | gemessen / gelesen |
|---|---|
| `research/vorregistrierung/benchmark.py`, Commit `19a1996` | Der Vierjahresfilter `point_in_time(…, MINDESTTRAINING_JAHRE)` ist **entfernt** (Fable: *„das Verfahren-A-Artefakt, das mit `MINDESTTRAINING` schon einmal gegangen ist; Code an registrierte Regel, Berichtigung"*). Neu: `tagesgenau(reihen, handelbar)` schneidet jede Kursreihe ab ihrem Handelbar-Tag ab; die erste Tagesrendite eines Symbols ist die vom Handelbar-Tag auf den Folgetag |
| Das Handelbar-Datum | **gelesen, nicht nachgebaut**: `research/faltenplan_neun/faltenschranke_messung.py::loader_lesart` (TB-56-Werkzeug; liest `MIN_HISTORY_*` aus der Bot-Datei; TB-65: Mengen in **78 von 78** Falten gleich der Trockenlauf-Spalte H). Erster Kurstag + `MIN_HISTORY_DAYS`; `elliott_wave`: Tag der 17 520. 1h-Kerze. Vorab geprüft: keine 1h-Datei enthält unvollständige Kerzen, keine 1d/4h-Datei beginnt mit einer — Zählung und erster Kurstag des Werkzeugs sind die des Loaders (`entferne_unvollstaendige`) |
| Die vier gesperrten Rechenfunktionen | `bh_tagesrenditen`, `drawdown_bei_exposure`, `nachschlagen`/`erlaubt`, Medianbildung: **im Code unverändert** (Diff-Hunks berühren keine Zeile ihrer Körper) |
| `bh_tagesrenditen`, Docstring | *„Gleichgewichteter Buy-and-Hold"* → *„Gleichgewichtet, täglich rebalanciert"*. Der Mittelwert der Tagesrenditen ist ein täglich auf Gleichgewicht zurückgesetztes Portfolio, kein Buy-and-Hold; Fable hat es als Unsicherheit benannt, nachgesehen am 20.09.: seine Formulierung trifft den Code. ⚠️ Dieselbe Fehlerklasse wie `K1h` und `T44.10` — ein Name, der etwas anderes verspricht als das Verhalten. `research/exposure_messung/exposure_kern.py::bh_tagesrenditen` trägt denselben Docstring **weiter** (ausserhalb dieses Auftrags, benannt) |
| Ausgabe | `benchmark_drawdowns_vt.json`: **neunmal `status: endgueltig`**; je Bot neu `benchmark`, `loader_schranke`, `handelbar_ab` je Symbol; je Falte `symbole_handelbar_in_falte` statt `symbole_point_in_time`. ⚠️ `registerbericht.py:178` liest den alten Schlüssel aus der **gesperrten** Datei und läuft deshalb heute unverändert; **beim Vollzug der Sperrlisten-Änderung ist er nachzuziehen** |
| Gegen TB-65, Spalte VT | **78 / 78** Falten gleich — alle 100 Stufen, `handelstage`, Symbolzahl; `DD_Toleranz` bei allen neun Bots auf allen Stufen gleich (`docs/belege/TB-66/schritt4_vergleich_tb65_vt.txt`) |
| `research/krypto_historie/faltenplan.py:65` (`MINDESTTRAINING_JAHRE = 4`, `K4f`) | **nicht angefasst**; gemessen: wird von nichts importiert, was hier rechnet (`research/vorregistrierung/`, `research/faltenplan_neun/faltenplan_neun.py`, `faltenschranke_messung.py`) — nur `test_faltenplan_neun.py` nennt den Pfad als Werkzeug. Gehört zu `T56b.6` |
| `registerdaten.MINDESTTRAINING_JAHRE` | bleibt stehen — `faltenplan.py:208` schreibt sie weiter in jeden Plan, `registerbericht.py:140` druckt sie als *„Mindesttraining vor der ersten Falte"*. Beides ist der ersetzte Verfahren-A-Satz (TB-65, Beobachtung 2); ausserhalb dieses Auftrags |

---

### 23.6 Begriffsberichtigung — „Amendment" gehört zur Sperrliste des Codes, nicht zum Register

**Fable, 20.09.2026, wörtlich:** *„Vor dem Tag ist es eine **Berichtigung des
Registers** und ein **Bug-Fix am Auswerter**; ‚Amendment' gehört zur Sperrliste
des Codes, nicht zum Register — die Unterscheidung bleibt wichtig, sobald der
Tag steht."*

**Gemessen** (Stand Commit `ec7eff4`, vor diesem Eintrag): „Amendment" steht
**24×** in diesem Register (24 Zeilen) und **11×** in `docs/projektfuehrung/BACKLOG.md` (10 Zeilen; `T56b.3` trägt zwei).
**Die meisten Stellen sind richtig** — sie sagen *„kein Amendment"* (Zeilen 855,
1040, 1212, 1442, 1451, 2096, 2116, 2125, 2550, 2570, 2628, 2706, 2786, 3027,
3091, 3268: kein Lauf, also kein Amendment) oder sie beschreiben die Regel selbst
(887–897, 10.1). ⚠️ **Zu berichtigen sind die Stellen, die den bevorstehenden
Vorgang — die neue Benchmark-Tabelle wird die registrierte, der Registertext
verweist auf sie — als „Amendment" bezeichnen.** Nach Fable ist dieser Vorgang
vor dem Tag eine **Berichtigung des Registers** (der Registertext) und ein
**Bug-Fix am Auswerter** (`benchmark.py`); „Amendment" bleibt der Begriff für
die Sperrliste **nach** dem Tag (10.1: *„der Lauf beginnt von vorn"*).

**Das Register ist append-only; die alten Sätze bleiben stehen. Hier steht je
Stelle der Satz, wie er dasteht, und der Satz, wie er zu lesen ist:**

| Fundstelle (Zeile, Stand `ec7eff4`) | Satz, wie er dasteht | Satz, wie er seit dieser Berichtigung zu lesen ist |
|---|---|---|
| **21.6**, Z. 2947–2949 | *„`DD_Toleranz` und die vorab berechneten Benchmark-Drawdowns stehen auf der Sperrliste (Abschnitt 10, Punkt 4), und eine Änderung dort ist ein **Amendment** nach 10.1."* | *„… und eine Änderung dort ist **vor dem Tag eine Berichtigung** (Register) samt **Bug-Fix am Auswerter** (`benchmark.py`), **nach dem Tag ein Amendment** nach 10.1."* |
| **21.6**, Z. 2991, Weg A | *„**Amendment vollziehen**: die neue Tabelle wird die registrierte, die alte bleibt als ERSETZT stehen, …"* | *„**Berichtigung vollziehen**: die neue Tabelle wird die registrierte, …"* — der Weg selbst ist unverändert, nur sein Name |
| **21.9**, Z. 3071–3073 | *„Das Amendment wird **einmal** vollzogen, **nach** der Berechnung der Krypto-Falten (TB-31), und umfasst dann **alle neun Bots**."* | *„Die **Berichtigung der Benchmark-Tabelle** (Sperrliste Punkt 4) wird **einmal** vollzogen, nach der Berechnung der Krypto-Falten, und umfasst dann alle neun Bots."* — die Reihenfolge-Entscheidung des Betreibers ist unberührt |
| **21.9**, Z. 3081 | *„Ein Amendment jetzt bewegte eine gesperrte Zahl, die kurz darauf erneut bewegt werden müsste"* | *„Eine Berichtigung jetzt bewegte …"* |
| **21.9**, Z. 3088 | *„Er wird mit demselben Amendment geschlossen"* | *„Er wird mit derselben Berichtigung geschlossen"* |

**Ausdrücklich unverändert und richtig:** *„Kein Amendment"* in 21.8, 21.9
(Z. 3091) und 22.7 — es hat keinen Lauf gegeben. ⚠️ **`benchmark_drawdowns.json`
selbst** steht auf der Sperrliste (Punkt 4); dass ihre Änderung **nach dem Tag**
ein Amendment wäre, bleibt richtig und ist der Grund, warum die neue Tabelle bis
zur Betreiberfreigabe **daneben** liegt.

**Im Backlog** (kein append-only-Dokument; dort ist der Wortlaut geändert, die
alte Fassung entfernt nach `DOKUMENTATIONSSTANDARD.md` Regel 9):
`T56b.3` und der Satz *„Das Amendment selbst braucht danach eine eigene
Betreiberfreigabe"* im Schlussblock von Abschnitt 2 — je Stelle mit Satz davor
und danach in `docs/ERGEBNIS_TB-66_benchmark_tagesgenau.md`, Nachweis 7.

---

### 23.7 Was diese Berichtigung ausdrücklich NICHT tut

| | |
|---|---|
| ⚠️ | **Die Sperrlisten-Änderung nicht vollzogen.** `benchmark_drawdowns.json` ist byteweise dieselbe Datei; `benchmark_drawdowns_vt.json` liegt daneben. Der Vollzug braucht die eigene Betreiberfreigabe aus 21.9 — **und die Entscheidung W oder C aus 23.3 davor**, weil bei C der Lauf wiederholt werden muss (andere `handelstage`) |
| ⚠️ | **Die Formulierungsfrage nicht entschieden.** Der Platzhalter in 23.3 ist sichtbar und bleibt, bis der Betreiber entscheidet; die Messung liegt in 23.4 |
| ⚠️ | **Registertext 3b (a), (b), (d), (e) unverändert.** Ebenso 4.2 und Sperrliste Punkt 6, die den Benchmark weiter *„point-in-time"* nennen: **die Menge bestimmt seit dem 16.09. 3b (c)**, und 3b (c) sagt jetzt, wann ein Symbol dazugehört. Der Begriff *point-in-time* bleibt richtig — tagesgenau ist die genauere Zeitauflösung desselben Prinzips |
| ⚠️ | **Kein Registertext zur ersten Falte.** Register 21.3 (b) lässt 3b (a) binden; `faltenplan.py` rechnet weiter nur 4a, `t3_supertrend` trägt deshalb weiter die leere Falte 2018 (TB-61 Befund 2). Der Median in 23.4 ist **mit** dieser Falte gerechnet — ohne sie (21.4) läge er bei −13,90 / −26,57 / −48,10 (TB-65, Tabelle C1, VT) |
| ⚠️ | **`T56b.6` nicht erledigt** (die Konstantenkopien `MINDESTTRAINING_JAHRE`, `FRUEHESTE_FALTE`); **G6/H3 aus TB-61 nicht repariert**; `docs/VORREGISTRIERUNG_S-E1_nulltest.md` nicht geändert (`K4f`) |
| ⚠️ | **`registerbericht.py` nicht angefasst** — es liest die gesperrte Datei; der neue Schlüssel `symbole_handelbar_in_falte` ist beim Vollzug nachzuziehen (23.5) |
| | **Kein Selektionslauf, kein signierter Tag, kein Zeitanker.** Der Tag bleibt der nächste Meilenstein und gehört dem Betreiber (Abschnitt 13) |

⭐ *Nachtrag TB-71, 20.09.2026: Die erste und die zweite Zeile dieser Tabelle
sind überholt — der Platzhalter in 23.3 ist gefallen, die Wahl W oder C ist
durch den Satz zur Zeitachse gegenstandslos (keine der beiden Fassungen, keine
Codeänderung, kein wiederholter Lauf); der Vollzug der Sperrlisten-Änderung
braucht nur noch die Betreiberfreigabe aus 21.9. Die vierte Zeile (die leere
Falte `t3_supertrend` 2018) ist als Berichtigung nach 21.3 (b) entschieden und
wird in TB-72 vollzogen (`FABLE_ANTWORT_2026-09-20c_kapitalpfad.md`, Teil 2).
Die Bewertungsachse des Bot-Drawdowns, die 23 nicht behandelt, steht in
Abschnitt 24.*

> ⚠️⚠️ **Tatsachennotiz (38.7 (d), TB-88, Messstand `8851f67`, eingetragen
> TB-89, 23.09.2026):** Der Vollzug der Sperrlisten-Änderung braucht nach 38.3
> kein Amendment (37.3) und hat seit 38.4 seine Form (ii). Fables
> Fertigkriterium „`test_vorregistrierung.py` grün" ist heute **nicht
> erreichbar**: der Test stürzt ab (`KeyError: '2017'`), nach dem simulierten
> Vollzug bleibt er **163/2** (`G6`, `H3`, beide am Faltenplan). Die fünfte
> Zeile oben („G6/H3 aus TB-61 nicht repariert") gilt fort. ⚠️ **OFFENE FRAGE
> bei Fable (Anfrage 22i), nicht entschieden.** Einzelheiten in **38.7 (d)**.

> ⭐⭐ **Die Tabelle folgt dem Plan (39.2–39.4, Fable 23a/23b, TB-94,
> 23.09.2026):** Die Sperrlisten-Änderung ist vollzogen — in Form (ii), aber
> **nicht** mit `benchmark_drawdowns_vt.json`: Nach 23a ist die Tabelle, die
> der Lauf liest, auf dem registrierten Faltenplan (33.2) gerechnet, für alle
> neun Bots, ohne Mischung; `_vt.json` trägt bei `t3_supertrend` die leere
> Falte 2018 (vierte Zeile oben). Gelesen wird die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`),
> die `_tb72.json` in allen 9750 Blattwerten reproduziert (39.4). Erledigt sind
> damit die erste Zeile (Vollzug) und die sechste (`registerbericht.py` liest
> `symbole_handelbar_in_falte`, TB-92); aus der fünften ist `G6`/`H3` der
> eigene Planpunkt „Testannahmen folgen dem Register" (39.1, TB-95).
> `benchmark_drawdowns.json` ist byteweise dieselbe Datei (`a163c498…`).

---

### In einfacher Sprache

**Worum es ging:** Jeder Bot wird an einem Vergleichswert gemessen — einem
einfachen Korb aus den Kursen, die er handeln darf. Bisher stand im Regelwerk
nur, dass der Korb aus den Kursen besteht, die der Bot „in diesem Jahr" laden
kann. Nicht gesagt war, was mit einem Kurs geschieht, den der Bot erst am
30. Dezember laden darf: zählt er für zwei Tage oder für das ganze Jahr?

**Was entschieden ist:** Er zählt ab dem Tag, an dem der Bot ihn laden darf —
nicht rückwirkend. Fable hat das festgelegt, und zwar aus dem Satz, der schon im
Regelwerk stand: Bot und Vergleichskorb leben in derselben Menge. Ein Korb, der
ein Jahr lang etwas hält, das der Bot nicht halten durfte, ist nicht sein Korb.

**Warum das wichtig ist:** Unter der anderen Lesart wäre die Verlustgrenze in
den frühen Krypto-Jahren wirkungslos gewesen — der Korb hätte 88 % verloren,
der Bot hätte nichts gehalten, und jeder Parametersatz hätte bestanden. Und der
Bot hätte sich 88 Prozentpunkte Vorsprung anrechnen lassen, nur weil er nicht
dabei war.

**Was jetzt anders ist:** Der alte Satz bleibt stehen und ist als ersetzt
markiert; der neue steht hier. Das Programm rechnet den Korb seit heute
tagesgenau, die gesperrte Tabelle ist unberührt, die neue liegt daneben. Die
Verlustgrenzen der fünf Krypto-Bots werden dadurch **deutlich nachgiebiger** als
in der Rechnung vom Vormittag — das steht hier, obwohl es unbequem ist, und es
war nicht der Grund.

**Was offen bleibt und warum:** Eine einzige Formulierung. Fable hat geschrieben,
Tage ohne handelbaren Kurs sollen „Rendite 0 tragen"; das Programm lässt sie
stattdessen weg. Für die Verlustzahlen ist das gleichwertig — gemessen, nicht
vermutet —, für die Angabe, wie viele Handelstage ein Jahr hatte, nicht. Im
Regeltext steht an dieser Stelle ein sichtbarer Platzhalter, bis der Betreiber
gewählt hat.

*Nachgetragen in TB-66, 20.09.2026. Berichtigung: sie nennt den unpräzisen Satz,
die Festlegung, die Messung und den Ersatztext — und entfernt nichts.*

---

## 24. Präzisierung zu Registertext 4 und zu Festlegung 1 — der Drawdown der Nebenbedingung wird Mark-to-Market gerechnet, und die Regel steht vor der Messung (TB-71, 20.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben**
— Festlegung 1 bleibt in Abschnitt 1 stehen (Z. 47, dort seit heute mit der
Marke *„PRÄZISIERT durch Abschnitt 24"*), Registertext 1a bleibt in 15.3,
Registertext 4 in 15.6 und 21. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und die Form der
Abschnitte 21 und 23.

**Anlass:** Bei der Messung zu Abschnitt 23 (Kalender des Bot-Kapitalpfades,
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20c_kapitalpfad.md`) fiel auf,
dass der Kapitalpfad, aus dem `equity_simulation.py` den Drawdown rechnet,
**keinen Tageskalender hat** — er ist ereignisindiziert. Fables dritte Antwort
vom 20.09.2026, 18:00 Ortszeit (`FABLE_ANTWORT_2026-09-20c_kapitalpfad.md`,
Teil 1) benennt daraus einen Widerspruch **innerhalb des Registers**: Festlegung
1 (*„Führendes Mass: Kapital-Drawdown aus `equity_simulation.py`"*, Z. 47) gegen
Registertext 1a (*„Reihe der täglichen Netto-Mark-to-Market-Renditen des
Kapitalpfads"*, 15.3, Z. 1102–1104 im Stand `cc096e1`) und 2a (*„Summe der täglichen
Netto-Mark-to-Market-Renditen"*, 15.4). Seine vierte Antwort vom 20.09.2026,
18:08 (`FABLE_ANTWORT_2026-09-20d_mtm_messung.md`) macht die **Reihenfolge**
zur Bedingung: die Entscheidungsregel steht im Register, **bevor** jemand einen
Mark-to-Market-Pfad rechnet. Umsetzung: `docs/auftraege/MAC_TB-71_register_schliessen.md`,
Ergebnis `docs/ERGEBNIS_TB-71_register_schliessen.md`.

**Art der Änderung nach der Drei-Kategorien-Regel (F17):** Fable ordnet den
Registerwiderspruch als **Berichtigung** ein (*„aufzulösen zugunsten der Seite
mit dem Grund (L1)"*). Weil Festlegung 1 aber eine der zwölf
Betreiberfestlegungen vom 14.09.2026 ist, wurde sie **dem Betreiber vorgelegt,
nicht als Berichtigung vollzogen** — Fable: *„Sie wird ihm vorgelegt, nicht als
Berichtigung vollzogen. Beides übernehme ich."* **Betreiberentscheidung
20.09.2026, 18:15 Ortszeit, per anklickbarer Frage: erst die Regel, dann die
Messung** (überliefert in `docs/auftraege/MAC_TB-71_register_schliessen.md`, Abschnitt 3; Einzelheiten in 24.4). ⚠️ **Die
Richtung der Wirkung ist bekannt und geht gegen alle neun Bots** — der tägliche
Drawdown ist nie flacher als der ereignisweise; **ihre Grösse ist nicht
gemessen** und ist nach 24.3 für die Entscheidung ohne Belang. Es hat kein
Selektionslauf stattgefunden; kein Parametersatz ist bewertet, kein Ergebnis
erzeugt; der Laufcode, der die Tagesreihe je Zelle erzeugt, **existiert nicht**
(24.5).

---

### 24.1 Der Befund

**Wörtlich aus Fables dritter Antwort (20.09.2026, 18:00):**

> Der Drawdown der Nebenbedingung wird auf einem Objekt gerechnet, das das
> Register ausschliesst. `calculate_max_drawdown` läuft über `capital_after` je
> Ereignis — eine Kurve, die sich nur an Ein- und Ausstiegen bewegt. … **Sie
> sieht keinen unrealisierten Verlust.** Eine Position, die zwischen Einstieg und
> Ausstieg 20 % unter Wasser war und mit −3 % geschlossen wurde, trägt −3 % zum
> Drawdown bei. Der Benchmark daneben ist tagesgenau bewertet. … „Bot und
> Benchmark leben in derselben Menge" gilt dann auf der Symbol- und Zeitachse,
> aber nicht auf der Bewertungsachse.

**Die Fundstellen, gemessen am 20.09.2026** (Stand Commit `cc096e1`; gelesen,
nicht ausgeführt):

| Fundstelle | was dort steht |
|---|---|
| `shared/zuteilung.py:720–735` | `equity_curve.append({"time": …, "capital_after": …})` je Ereignis (Ausstieg). Kein Tageskalender |
| `shared/messkette.py:139–153` | `calculate_max_drawdown` rechnet über `equity_df["capital_after"]` — die Funktion, die bis TB-28 neunmal zeichengleich in den `strategies/*/equity_simulation.py` stand |
| `research/vorregistrierung/beispieldaten.py:24–26` | *„der Kapital-Drawdown einer Falte steht in `zellen.csv`, weil er im echten Lauf aus `equity_simulation.py` kommt, und **nicht aus der Tagesreihe** nachgerechnet wird. Das ist auch im echten Lauf so."* |
| `research/vorregistrierung/auswertung.py:246–247` | die Nebenbedingung vergleicht genau dieses `kapital_drawdown_pct` gegen die Benchmark-Grenze (`dd_satz`, `bestanden`) |
| Register Z. 47 (Festlegung 1) | *„Führendes Mass — Kapital-Drawdown aus `equity_simulation.py`"* |
| Register 15.3, Registertext 1a (Z. 1102–1104 im Stand `cc096e1`) | *„auf der Reihe der täglichen Netto-Mark-to-Market-Renditen des Kapitalpfads gerechnet, nie auf Trade-Listen. Flache Tage stehen mit Rendite 0 in der Reihe."* |
| Register 15.4 (Registertext 2a) | *„Die Falten-Rendite ist die Summe der täglichen Netto-Mark-to-Market-Renditen dieser Tage."* |

**Was der Widerspruch bedeutet, in Fables Worten:** *„Sonst wird auf einem
Objekt selektiert (Sharpe, täglich) und auf einem anderen beschränkt (Drawdown,
ereignisweise) — genau die Inkonsistenz aus M.3, eine Ebene tiefer."* Und:
*„Der Drawdown gehört aus derselben Tagesreihe wie der Sharpe."*

---

### 24.2 Der Registertext — Präzisierung zu Registertext 4

**Fables Wortlaut, unverändert:**

> **Registertext 4, Präzisierung.** Der Kapital-Drawdown einer Falte für die
> Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe des Kapitalpfads
> gerechnet (1a), auf denselben Tagen wie der Benchmark (3b (c)). Der
> ereignisindizierte Drawdown aus `equity_simulation.py` wird berichtet, nicht
> bewertet.

**Was der Satz festlegt und was nicht:** Er legt die **Bewertungsachse** fest
(täglich, zum Marktpreis, 1a) und die **Zeitachse** (dieselben Tage wie der
Benchmark, 3b (c) in der Fassung aus 23.3). Er ändert nichts an der Formel der
Nebenbedingung (Festlegung 4, Abschnitt 4), nichts an `DD_Toleranz`
(Festlegung 5), nichts am Benchmark (Abschnitt 23). Der ereignisindizierte
Drawdown bleibt als **Berichtswert** bestehen — er verschwindet nicht, er
entscheidet nicht.

---

### 24.3 ⭐⭐ Die Entscheidungsregel — vor jeder Messung

**Wörtlich (Fable, vierte Antwort, Punkt 1 seiner empfohlenen Reihenfolge) —
und sie steht hier, bevor jemand einen Mark-to-Market-Pfad gerechnet hat:**

> Der Drawdown der Nebenbedingung wird auf der täglichen
> Mark-to-Market-Reihe gerechnet (1a); die Grösse der Abweichung zur
> ereignisindizierten Kurve wird gemessen und berichtet und ist für die
> Entscheidung ohne Belang.

**Warum die Reihenfolge zählt — Fable wörtlich:**

> Eure Lesart ist richtig: Der Grund kommt aus 1a und L1 und steht fest, bevor
> die Zahl existiert. Die Zahl beziffert, sie entscheidet nicht. Aber das ist nur
> dann wahr, wenn es **vor** der Messung aufgeschrieben ist — sonst ist die Zahl,
> sobald sie da ist, ein Argument, und zwar in beide Richtungen: „ändert wenig,
> also nicht die Mühe" oder „ändert viel, also zu riskant vor dem Tag". … **Eine
> Zahl, die nichts entscheiden darf, sollte nicht auf dem Tisch liegen, während
> entschieden wird.**

⚠️ **Die Warnung, die dazugehört — Fable wörtlich:**

> Eine kleine Abweichung im Mittel sagt nichts über die Falten, in denen die
> Nebenbedingung binden soll — 2020 und 2022 sind die Falten mit den grössten
> unrealisierten Verlusten innerhalb offener Positionen.

**Was daraus für die Messung folgt:** Sie ist zulässig und vorgesehen — **nach**
diesem Eintrag, als Forschungsskript ausserhalb des Laufcodes, je Bot an den
TB-24-Trade-Listen und den Kursdateien (`AKTUELLER_AUFTRAG.md`: TB-73, *„erst
nach TB-71 (b)"*). Ihr Ergebnis geht als bekannte Wirkung in die Notiz zu
Festlegung 1 (24.4) — **nie in eine Entscheidung**. Wer die Zahl später liest
und daraus *„zu klein für die Mühe"* oder *„zu gross vor dem Tag"* folgert,
trifft die nachträgliche Wahl, gegen die F17 steht.

---

### 24.4 Was mit Festlegung 1 geschieht

⭐ **Sie wird nicht gestrichen, sie wird präzisiert.** Register Z. 47 bleibt
stehen; hier steht daneben:

| | |
|---|---|
| **Führendes Mass bleibt der Kapital-Drawdown** | unverändert |
| ⭐ **Präzisiert ist, worauf er gerechnet wird** | auf der täglichen Mark-to-Market-Reihe des Kapitalpfads (1a), nicht auf der Ereigniskurve |
| **Der ereignisweise Drawdown** aus `equity_simulation.py` | bleibt **Berichtswert** |
| **Betreiberentscheidung** | 20.09.2026, 18:15 Ortszeit, per anklickbarer Frage: erst die Regel (dieser Abschnitt), dann die Messung (TB-73) |
| **Wirkung, gemessen** | *noch nicht* — der Eintrag steht absichtlich vor der Zahl (24.3). Bekannt ist die Richtung: gegen alle neun Bots, am stärksten bei langen Haltedauern und hoher Exposure (`turtle_soup_stocks`: 100 % im Markt, 14 Tage Median). Die Zahl wird hier nachgetragen, wenn TB-73 gelaufen ist |

> ⭐ **NACHGETRAGEN in Abschnitt 24.6 (TB-73, 20.09.2026):** die Wirkung ist gemessen — je Bot und je Falte, mit den fünf Falten, in denen die Richtung *nicht* gegen den Bot geht. Die Zeile oben bleibt, wie sie war.

**Die Vorgeschichte gehört ausdrücklich dazu, sonst liest sich dieser Abschnitt
wie ein Widerruf:** `research/drawdown_reihenfolge/` (Commits vom 12.09.2026,
`26bdd97`, `971c001`, `027fe2b`) hat **drei** Drawdown-Begriffe verglichen —
Symbol-Blockreihenfolge, chronologisch auf der kumulierten PnL-Summe,
Kapitalkurve aus `equity_simulation.py` — und die Kapitalkurve als *„den
erlebbaren Verlauf"* gewählt (`BERICHT.md`, Abschnitt 0). Daher Festlegung 1.
**Mark-to-Market war unter den dreien nicht dabei.** Fable dazu, wörtlich:

> Das Kriterium war richtig; nur war die vierte Definition nicht im Vergleich —
> und sie ist die, die das Kriterium am besten erfüllt. **Erlebbar ist, was das
> Konto an jedem Tag zeigt, und das Konto zeigt offene Positionen zum
> Marktpreis, nicht zum Einstandskurs.** Die Ereigniskurve ist der *realisierte*
> Verlauf; der erlebbare ist der bewertete.

Und, ebenfalls Fable: *„Meine Kritik widerspricht der Messung nicht, sie
ergänzt den Vergleich um das Objekt, das 1a schon vorschreibt."* — Das ist
dieselbe Lehre wie `L1` im Journal (12.09.2026): Die Ereigniskurve erzeugte
Korrelationen nahe null, bis zu Marktpreisen bewertet wurde; für den Drawdown
tut sie dasselbe mit umgekehrtem Vorzeichen.

---

### 24.5 Was dieser Abschnitt ausdrücklich NICHT tut — und was ihm folgen muss

| | |
|---|---|
| ⚠️ | **Kein Code geändert.** `auswertung.py` ist eingefroren (15.8 Nr. 3, TB-30b) und bleibt es, auch ihr Docstring; `beispieldaten.py`, `registerdaten.py`, `benchmark.py`, `shared/zuteilung.py`, `shared/messkette.py` sind unberührt |
| ⚠️ | **Nichts gerechnet.** Kein Mark-to-Market-Pfad, keine Tabelle, kein Lauf; `benchmark_drawdowns.json` (`a163c498…36d1ee`) und `benchmark_drawdowns_vt.json` (`4549395f…8745d`) byteweise unverändert |
| ⭐ | **Drei Code-Stellen müssen 24.2 folgen, sobald der Laufcode geschrieben wird** — geführt als **eine** Backlog-Zeile (`K4j`, `docs/projektfuehrung/BACKLOG.md` Abschnitt 4): **(1)** `auswertung.py`, Datenvertrag Z. 40–58 — `kapital_drawdown_pct` kommt aus derselben Tagesreihe wie der Sharpe (eingefroren, gehört zu TB-30b); **(2)** `beispieldaten.py` Z. 24–26 und Z. 125 — rechnet den Drawdown heute ausdrücklich **nicht** aus der Tagesreihe und sagt im Kopf, das sei auch im echten Lauf so; **(3)** `registerdaten.py:70`, `FESTLEGUNGEN[1]` — Text präzisieren, sobald 1 und 2 stehen |
| ⭐ | **Der Laufcode selbst existiert nicht** — gemessen am 20.09.2026 (`FABLE_ANFRAGE_2026-09-20d_tagesreihe.md`): kein Code im Repo schreibt `zellen.csv` oder `tagesreihen/<zelle_id>.csv` ausser `beispieldaten.py` (erfundene Werte). Deshalb ist 24.2 eine **Spezifikation** für ungeschriebenen Code, kein Umbau — und *„Lauf wiederholen"* kostet nichts, weil der Lauf nicht begonnen hat |
| ⚠️ | **`t3_supertrend` nicht auf 2019 umgestellt** — das ist TB-72 (Berichtigung nach 21.3 (b) plus Ableitung der ersten Falte aus dem Trockenlauf; Fable, dritte Antwort Teil 2, vierte Antwort Punkt (2)) |
| ⚠️ | **Die MtM-Wirkung nicht gemessen** — das ist TB-73, und es darf erst nach diesem Abschnitt laufen (24.3) |
| ⚠️ | **Die Sperrlisten-Änderung nicht vollzogen** (21.9, 23.7): `benchmark_drawdowns_vt.json` liegt weiter daneben |
| | **Kein Selektionslauf, kein signierter Tag, kein Zeitanker.** Der Tag bleibt der nächste Meilenstein und gehört dem Betreiber (Abschnitt 13) |

---

### In einfacher Sprache

**Worum es ging:** Jeder Bot muss eine Verlustgrenze einhalten — er darf in
einem Jahr nicht tiefer fallen als ein Vielfaches des Vergleichskorbs. Dafür
muss man messen, wie tief der Bot gefallen ist. Im Regelwerk standen dazu zwei
Sätze, die sich widersprachen: Der eine sagte, der Verlust wird jeden Tag zum
Marktpreis gemessen. Der andere nannte ein Programm, das nur bei Käufen und
Verkäufen misst — und dazwischen nichts sieht. Eine Position, die zwischendurch
20 % im Minus war und mit −3 % verkauft wurde, zählt dort als −3 %.

**Was entschieden ist:** Die tägliche Messung gilt — weil nur sie zeigt, was
das Konto an einem Tag wirklich wert ist. Das alte Mass verschwindet nicht,
es wird weiter berichtet; nur entscheiden tut es nichts mehr. Die frühere
Untersuchung, aus der die alte Festlegung kam, war nicht falsch: Sie hatte
drei Messarten verglichen, und die vierte — die tägliche — war nur nicht
dabei.

**Warum dieser Abschnitt vor der Zahl steht:** Wie gross der Unterschied
zwischen beiden Messarten ist, weiss noch niemand. Das wird gemessen — aber
erst jetzt, nachdem hier steht, dass die Grösse für die Entscheidung keine
Rolle spielt. Sonst würde die Zahl, sobald sie da ist, zum Argument: „ändert
wenig, also nicht der Mühe wert" oder „ändert viel, also zu riskant". Eine Zahl,
die nichts entscheiden darf, soll nicht auf dem Tisch liegen, während
entschieden wird.

**Was jetzt anders ist:** Nichts am Programm — der Teil, der diese Zahlen
einmal berechnen wird, ist noch nicht geschrieben. Drei Stellen, die ihm
folgen müssen, stehen im Backlog. Und was bekannt ist, steht hier, obwohl es
unbequem ist: Die neue Messung ist für alle neun Bots strenger, nie milder.

*Nachgetragen in TB-71, 20.09.2026. Präzisierung nach Betreiberentscheidung:
sie nennt den Widerspruch, die Fundstellen, den Registertext, die
Entscheidungsregel und die Vorgeschichte — und entfernt nichts.*

---

### 24.6 Tatsachennotiz zu 24.3 und 24.4 — die gemessene Wirkung (TB-73, 20.09.2026)

**Datiert angehängt. Nichts entfernt, kein bestehender Satz umgeschrieben.**
Die Zeile *„Wirkung, gemessen — noch nicht"* in 24.4 bleibt stehen; hier steht
die Zahl, die sie ankündigt. **Diese Notiz berichtet. 24.3 hat entschieden,
bevor sie existierte, und sie wirft nichts erneut auf.** Kein Satz hier ist
eine Bewertung, eine Empfehlung oder eine Abwägung; keine Bot-Zahl steht neben
`erlaubt(f)`, `DD_Benchmark` oder `DD_Toleranz`.

**Herkunft:** `research/mtm_drawdown/` (Forschungsskript ausserhalb des
Laufcodes, `BERICHT.md` dort), gemessen am 20.09.2026 auf dem Mac
(`trading-env/bin/python3` 3.9.6) an den TB-24-Trade-Listen
(`research/tb24_haltedauern/daten/<bot>_positionen.csv`) und den Kursdateien in
`data/`; Falten aus `research/vorregistrierung/ergebnisse/faltenplan_tb72.json`
(TB-72). Ergebnisdokument `docs/ERGEBNIS_TB-73_mtm_wirkung.md`. Nichts in
`research/vorregistrierung/`, `shared/`, `strategies/` berührt; die drei
Sperrlisten-Hashes (`a163c498…`, `4549395f…`, `0e54ac5c…`) und die beiden
`_tb72`-Dateien byteweise unverändert.

**Was gemessen wurde, in einem Satz je Grösse:**

| | |
|---|---|
| **E** | der ereignisindizierte Drawdown je Falte — `capital_after` je Ausstieg aus `shared/zuteilung.py::simuliere_portfolio` (TB-24-Liste), Drawdown mit `shared/messkette.py::max_drawdown_ungerundet`, Basis der Kapitalstand vor Faltenbeginn. Das ist die Grösse, die Festlegung 1 bis 24.2 meinte |
| **M** | der tägliche Mark-to-Market-Drawdown je Falte auf **denselben ausgeführten Positionen**: an jedem Kurstag der 1d-Dateien Buchwert plus Bewertung der am Tagesschluss offenen Positionen zum Schlusskurs (`allocation · (close/entry − 1 − Kosten_Seite)`), Ausstiege mit dem realisierten `pnl_pct`; Kosten aus dem Backtest-Modul des Bots importiert. Das ist die Grösse aus 24.2 / Registertext 1a |
| **Grundlage** | die neun TB-24-Listen: Kapitalkette schliesst bei allen neun, `entry_price` = Schlusskurs der Einstiegskerze (max. Abweichung 2,2e-16), 1d-Kurse decken jeden Tagesschluss mit offener Position (0 fortgeschriebene Kurstage bei 149 000 Positionstagen) |

⚠️ **Was nicht messbar ist:** Die fünf Krypto-Listen beginnen zwischen
2021-09-01 und 2022-03-17 (Datenstand vor dem TB-34-Neuaufbau, 1 826
Tageszeilen). **Die Falten 2018, 2019 und 2020 aller Krypto-Bots haben keine
Grundlage** (dazu 2021 bei `rsi2_crypto` und `volatility_breakout_crypto`), je
eine Falte ist nur teilweise gedeckt. **2020 ist bei keinem Krypto-Bot
messbar.** Diese Falten tragen keine Zahl. Die Aktien-Listen (ab 2016-09-01)
decken alle Falten.

**Die Wirkung, je Bot und je Falte** (E → M, Prozent; **fett: 2020 und 2022**;
ᵗ = Liste beginnt in der Falte; ⚠️ = M flacher als E; „keine" = keine
Grundlage; „″" = zweites Jahr einer Zweijahresfalte; 2026 = Bestätigungsperiode
bis 2026-09-01 ausschliesslich, nicht im Median):

| Bot | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | Median Sel. E → M |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `elliott_wave` | · | keine | ″ | **-2,81** → **-4,48** ᵗ | ″ | **-10,17** → **-15,40** | ″ | -4,51 → -7,43 | ″ | -3,11 → -3,34 | -4,51 → -7,43 |
| `t3_supertrend` | · | · | keine | keine | -5,58 → -8,67 ᵗ | **-12,28** → **-14,11** | -11,55 → -11,25 ⚠️ | -6,20 → -10,79 | -16,41 → -19,61 | -9,92 → -11,79 | -11,55 → -11,25 |
| `rsi2_crypto` | · | · | keine | keine | keine | **-8,65** → **-10,15** ᵗ | -2,75 → -4,01 | -13,30 → -16,53 | -11,43 → -12,71 | -3,14 → -4,28 | -10,04 → -11,43 |
| `turtle_soup_crypto` | · | keine | keine | keine | -15,29 → -16,43 ᵗ | **-27,86** → **-30,38** | -20,68 → -21,53 | -18,00 → -19,42 | -27,42 → -35,29 | -16,03 → -22,25 | -20,68 → -21,53 |
| `volatility_breakout_crypto` | · | keine | keine | keine | keine | **-6,07** → **-10,39** ᵗ | -12,90 → -12,84 ⚠️ | -14,40 → -15,42 | -5,22 → -7,86 | -7,27 → -9,63 | -9,48 → -11,62 |
| `elliott_wave_stocks` | -0,99 → -5,26 | -4,85 → -9,22 | -4,86 → -8,61 | **-13,35** → **-9,45** ⚠️ | -3,88 → -5,34 | **-19,31** → **-18,11** ⚠️ | -1,96 → -4,53 | -3,26 → -6,14 | -8,92 → -11,91 | -5,74 → -11,71 | -4,85 → -8,61 |
| `rsi2_mean_reversion` | · | -11,49 → -14,92 | -6,46 → -7,66 | **-9,01** → **-11,28** | -3,53 → -5,53 | **-10,52** → **-11,93** | -8,69 → -9,21 | -4,45 → -5,48 | -5,33 → -7,49 | -3,84 → -5,51 | -7,57 → -8,44 |
| `turtle_soup_stocks` | -1,26 → -2,42 | -12,15 → -14,93 | -4,74 → -6,86 | **-29,91** → **-34,45** | -3,30 → -6,39 | **-18,73** → **-20,69** | -4,54 → -7,07 | -5,19 → -7,42 | -12,02 → -18,74 | -3,81 → -6,24 | -5,19 → -7,42 |
| `volatility_breakout` | · | -14,78 → -15,36 | -7,85 → -9,05 | **-9,41** → **-12,60** | -3,38 → -5,55 | **-23,97** → **-25,80** | -10,70 → -12,08 | -5,39 → -6,15 | -12,31 → -15,36 | -4,90 → -4,37 ⚠️ | -10,05 → -12,34 |

**Die beiden Falten aus Fables Warnung (24.3), einzeln:**

| Bot | 2020: E → M | Differenz | Faktor M/E | 2022: E → M | Differenz | Faktor M/E |
|---|---|---:|---:|---|---:|---:|
| `elliott_wave` | 2020-2021 (ab 2021-09-22): −2,81 → −4,48 | −1,67 pp | 1,59 | 2022-2023: −10,17 → −15,40 | −5,23 pp | 1,51 |
| `t3_supertrend` | keine Grundlage | | | −12,28 → −14,11 | −1,83 pp | 1,15 |
| `rsi2_crypto` | keine Grundlage | | | (ab 2022-02-11) −8,65 → −10,15 | −1,50 pp | 1,17 |
| `turtle_soup_crypto` | keine Grundlage | | | −27,86 → −30,38 | −2,52 pp | 1,09 |
| `volatility_breakout_crypto` | keine Grundlage | | | (ab 2022-03-17) −6,07 → −10,39 | −4,32 pp | 1,71 |
| `elliott_wave_stocks` | −13,35 → −9,45 ⚠️ | +3,90 pp | 0,71 | −19,31 → −18,11 ⚠️ | +1,20 pp | 0,94 |
| `rsi2_mean_reversion` | −9,01 → −11,28 | −2,27 pp | 1,25 | −10,52 → −11,93 | −1,41 pp | 1,13 |
| `turtle_soup_stocks` | −29,91 → −34,45 | −4,54 pp | 1,15 | −18,73 → −20,69 | −1,96 pp | 1,11 |
| `volatility_breakout` | −9,41 → −12,60 | −3,19 pp | 1,34 | −23,97 → −25,80 | −1,83 pp | 1,08 |

**Die Zahlen, zusammengefasst — und nur neben den Faltenwerten oben gültig:**
In **59 von 64** Falten mit Grundlage ist M tiefer als E. Der Median der
Differenzen je Bot über seine Selektionsfalten mit Grundlage liegt zwischen
**−1,39 pp** (`rsi2_crypto`) und **−3,09 pp** (`t3_supertrend`); der Faktor
M/E je Falte zwischen 1,04 (10.-Perzentil) und 1,88 (90.-Perzentil), Median
1,30. Die grössten Differenzen in Prozentpunkten liegen nicht in 2020 oder
2022, sondern in 2025 (`turtle_soup_crypto` −7,87 pp, `turtle_soup_stocks`
−6,72 pp) und in der Bestätigungsperiode 2026 (`turtle_soup_crypto` −6,22 pp,
`elliott_wave_stocks` −5,97 pp). Bei den vier Aktien-Bots ist 2020 in drei
Fällen die Falte mit der grössten oder zweitgrössten Differenz des Bots.

⚠️ **Tatsachennotiz zur Richtung — der Satz im Kopf dieses Abschnitts
(*„der tägliche Drawdown ist nie flacher als der ereignisweise"*) ist eine
Näherung, keine Eigenschaft der Rechnung.** Gemessen: in **5 von 64** Falten
ist M flacher als E — `t3_supertrend` 2023 (+0,30 pp),
`volatility_breakout_crypto` 2023 (+0,06 pp), `elliott_wave_stocks` **2020**
(+3,90 pp) und **2022** (+1,20 pp), `volatility_breakout` 2026 (+0,53 pp).
In jedem der fünf Fälle liegen am Tiefpunkt der Ereigniskurve **unrealisierte
Gewinne** in offenen Positionen (`elliott_wave_stocks` 2020: +2 055 in sechs
März-Einstiegen, die E erst beim Ausstieg im Juli/August sieht; das Tief von M
liegt am 18.03.2020 bei −9,45 %, das von E am 13.05.2020 bei −13,35 %). Die
Ereigniskurve bewertet offene Positionen zum Einstand — das lässt sie
unrealisierte Verluste **und** unrealisierte Gewinne nicht sehen; welche
Richtung die Abweichung nimmt, hängt davon ab, was am Tiefpunkt im Buch liegt.
Von Hand nachgerechnet in `research/mtm_drawdown/test_mtm_kern.py`, Probe 3;
jeder Fall zerlegt in `research/mtm_drawdown/ergebnisse/richtungsfaelle.md`.
Der Pfad ist in keinem der fünf Fälle falsch: ein Pfad, der „M ≤ E" erzwänge,
müsste unrealisierte Gewinne ignorieren und wäre nicht mehr Mark-to-Market.
Gegenprobe: in 0 von 64 Falten ist E flacher als die Ereigniskurve am
Tagesende (E_tag) — erwartet, jeder Tagesendwert ist ein E-Punkt.

**Zwei Feststellungen zum Auftrag, gemessen statt übernommen:** (a) Der
Auftrag verlangte E gegen M *„bei 25 / 50 / 100 % Exposure"*. Diese Stufen
sind das Argument des **Benchmarks** (`DD_Benchmark(f, e)`, Abschnitt 4.2); ein
Bot hat je Falte **eine** Exposure, die aus seinen Positionen folgt — sie
steht in `research/mtm_drawdown/ergebnisse/messung.md` neben jeder Falte (z. B.
`turtle_soup_stocks` 0,66–0,86; `elliott_wave` 0,04–0,06). Sie auf drei Stufen
zu setzen hiesse andere Positionen oder Hebel; beides wäre eine erfundene
Zahl. (b) Der Bot-Median über die Selektionsfalten führt zu keiner Grösse
dieses Registers — `DD_Toleranz` ist der Median der **Benchmark**-Drawdowns
(Festlegung 5). Er steht oben als Beschreibung, nicht als Grösse der Regel.

**Was diese Notiz ausdrücklich NICHT tut:** Sie bewertet nichts, empfiehlt
nichts, wirft 24.3 nicht erneut auf. Sie vergleicht keine Bot-Zahl mit einer
Grenze. Sie ändert keinen Code, keine Sperrlisten-Datei, keinen Registertext;
`K4j` (drei Code-Stellen, sobald der Laufcode geschrieben wird) bleibt, wie
es ist, und die Grösse der Abweichung ist für keine dieser Stellen ein
Argument (24.3). Sie ersetzt die fehlenden Krypto-Falten 2018–2020 nicht durch
neue Backtests. Sie setzt keinen Tag.

*Nachgetragen in TB-73, 20.09.2026. Tatsachennotiz: sie nennt die Grundlage,
die Lücke, die Zahlen je Falte, die fünf Gegenfälle mit ihrem Grund — und
entscheidet nichts.*

> ⭐ **Nachtrag zur Lücke (TB-77, 21.09.2026; Fable, Kurzfassung vom 21.09., Teil 2 (5)):** Die Lücke *„Krypto 2018–2020 nicht messbar"* betrifft **nur die TB-24-Trade-Listen dieser Messung**, nicht den Lauf. Fable stellt klar: *„der Snapshot enthält Krypto 2018–2020, die Nebenbedingung wird dort gerechnet."* Nachgemessen 21.09.2026 am gezogenen Snapshot `63e4b6c8…` (Abschnitt 18): `BTCUSDT_1d.csv` und `ETHUSDT_1d.csv` beginnen am **2017-08-17** (3 317 Zeilen bis 2026-09-14); **6 der 24** Krypto-1d-Dateien beginnen vor dem 01.01.2019. Der Selektionslauf rechnet die Nebenbedingung in den Falten 2018–2020 auf diesem Bestand; was oben fehlt, ist allein die Vorab-Messung der MtM-Wirkung für diese Falten. Die Tabelle oben bleibt, wie sie ist.

---

## 25. Berichtigung zu Registertext 4a und zu 21.3 (b) — die erste Falte ist eine Konjunktion, und der Plan leitet sie aus dem Trockenlauf ab (TB-72, 20.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben**
— Registertext 4a bleibt in Abschnitt 15.6 stehen (dort seit heute mit der
Marke *„(a) ERSETZT durch Abschnitt 25"*), der Ersatztext 21.3 (b) bleibt in
Abschnitt 21 stehen (Marke *„(b) ERSETZT durch Abschnitt 25"*), die
Tatsachennotiz 21.4 bleibt unverändert gültig. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und die Form der
Abschnitte 21, 23 und 24.

**Anlass:** Zwei Implementierungen derselben Frage liefen auseinander, und eine
davon war die registrierte Regel. `research/vorregistrierung/faltenplan.py`
rechnete die erste Falte allein nach 4a nach und sagte in seinem Modulkopf
selbst, dass es 21.3 (b) nicht umsetzt (25.1). Fables vierte Antwort vom
20.09.2026 (`FABLE_ANTWORT_2026-09-20d_mtm_messung.md`, Abschnitt 2) entschied
beides: die Berichtigung für `t3_supertrend` (die *Instanz*) und die Ableitung
des Plans aus dem Trockenlauf (die *Schliessung der Klasse*) — *„dieselbe
Berichtigung, zwei Notizen, ein Vorgang"*. Die Messung in Schritt 1 von TB-72
(`docs/ERGEBNIS_TB-72_schritt1_erste_falte.md`) hat den Auftrag angehalten:
das Auseinanderlaufen war nicht einseitig. Fables fünfte Antwort vom 20.09.2026,
19:54 (`FABLE_ANTWORT_2026-09-20e_konjunktion.md`) nimmt seinen Vorschlag
zurück und fasst 4a und 21.3 (b) als **Konjunktion** neu (25.3). Umsetzung
`docs/auftraege/MAC_TB-72_erste_falte_aus_trockenlauf.md`, Ergebnis
`docs/ERGEBNIS_TB-72_erste_falte_aus_trockenlauf.md`.

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Berichtigung mit
Ersatztext.** Fable, wörtlich: *„21.3 (b) ist registrierte Regel … Plan an
registrierte Regel: `t3_supertrend` beginnt 2019, sieben Falten. … Dass die
Richtung diesmal zugunsten des Bots geht, ändert an der Kategorie nichts — die
Quelle des Grundes ist die Regel."* ⚠️ **Die Wirkung ist bekannt und geht
zugunsten des Bots** — `DD_Toleranz` von `t3_supertrend` wird nachgiebiger
(25.4). **Sie ist nicht der Grund.** Es hat kein Selektionslauf stattgefunden;
kein Parametersatz ist bewertet, kein Ergebnis erzeugt.

---

### 25.1 Der Befund — zwei Rechenwege, eine Regel, kein Code

| | |
|---|---|
| **Registertext 4a** (15.6) | erste Falte = erstes Kalenderjahr, in dem am 1. Januar Daten für Universum und Indikator-Vorlauf vorliegen. `faltenplan.py::erste_falte` rechnete das aus der Datenlage nach (`erste_falte_quelle`: *„Datenlage nach Registertext 4a … keine Konstante"*) |
| **Registertext 3b (a)** (16.7) | eine Falte zählt, wenn der Loader des Bots in ihr mindestens ein Symbol an mindestens einem Handelstag handelbar macht — über den Trockenlauf des Laufcodes (TB-40) |
| **Register 21.3 (b)** | ergeben beide verschiedene erste Falten, bindet 3b (a) |
| ⛔ **Gemessen: kein Code setzte 21.3 (b) um** | `faltenplan.py`, Modulkopf Z. 38–42 im Stand `7b73584`, wörtlich: *„⚠️ Diese Regel ist Registertext 4a allein. Register 21.3 (b) laesst bei Abweichung 3b (a) binden (Trockenlauf des Laufcodes); das rechnet dieses Modul nicht, und fuer `t3_supertrend` weichen beide ab (4a: 2018, 3b (a): 2019, weil `MIN_HISTORY_DAYS = 730` in der Falte 2018 kein Symbol handelbar macht)"* |
| **Die Folge** | `benchmark_drawdowns_vt.json` führte für `t3_supertrend` eine Selektionsfalte **2018 mit 0 Symbolen und 0 Handelstagen** (Drawdown 0,00 auf allen 100 Stufen), und der Median `DD_Toleranz` war mit ihr gerechnet. ⚠️ **Register 21.4 sagte für denselben Bot seit TB-56b „2019, 7 Falten"** — der Code hinkte der eigenen Tatsachennotiz hinterher |

**Was Schritt 1 dazu gemessen hat** (`ERGEBNIS_TB-72_schritt1_erste_falte.md`,
Trockenlauf des Laufcodes in beide Richtungen, zwei Anläufe byteweise gleich,
zweite Methode `loader_lesart` 9/9): 4a und 3b (a) laufen bei **sechs** Bots
auseinander — `t3_supertrend` **später** (2018 → 2019), `rsi2_crypto`
**früher** (2019 → 2018, `H = 2`), die vier Aktien-Bots **früher** (2017/2018 →
**1967**, `H = 16`). 21.3 (b) *„bindet 3b (a)"* hatte keine Richtung; seine
Begründung deckte nur die leere Falte. Wörtlich umgesetzt hätte die Ableitung
vier Aktien-Bots Selektionsfalten ab 1967 gegeben. **Das war nicht gemeint, und
es war nicht von der ausführenden Sitzung zu entscheiden** — deshalb der Halt
und die Anfrage an Fable.

---

### 25.2 Die Instanz — `t3_supertrend` beginnt 2019

| | vorher (Plan nach 4a allein) | nachher (25.3) |
|---|---|---|
| erste Falte | 2018 | **2019** |
| Selektionsfalten | 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 (**8**) | 2019, 2020, 2021, 2022, 2023, 2024, 2025 (**7**) |
| Bestätigungsperiode | 2026 (ab 2026-01-01) | 2026 — unverändert |
| Falte 2018 | Selektionsfalte, `H = 0` (Trockenlauf), 0 Handelstage, Benchmark-Drawdown 0,00 | **entfällt** — sie erfüllt Bedingung (ii) nicht |
| Zulassung nach 4b | erfüllt (8 ≥ 3) | erfüllt (7 ≥ 3) |

Gemessen: `H` je 4a-Kandidatenfalte **0** / 3 / 6 / 9 / 13 / 13 / 13 / 17 / 18
(2018 … 2026; `docs/belege/TB-72/schritt1_erste_falte_trockenlauf.txt`,
bestätigt im Test `research/faltenplan_neun/test_erste_falte_trockenlauf.py`
durch einen eigenen Aufruf von `universum_trockenlauf.messe_bot`). BTC und ETH
(Daten ab 2017-08-17) erreichen `MIN_HISTORY_DAYS = 730` am 2019-08-17. **Die
Zeile in 21.4 war schon richtig; der Plan folgt ihr jetzt.** Bei den acht
anderen Bots ändert sich nichts (25.4, Gegenprobe) — bei ihnen liegt (ii) nicht
später als (i).

⭐ **`rsi2_crypto` bleibt 2019**, an der Konjunktion nachgemessen
(`docs/belege/TB-72/schritt2_rsi2_crypto_bedingung_i.txt`): (ii) ist 2018
erfüllt (`H = 2`, BTC/ETH ab 2018-12-30), **(i) nicht** — 150 Tagesbalken
Vorlauf am 1. Januar 2018 brauchen Daten ab August 2017, BTC/ETH beginnen am
17.08.2017 und haben bis zum 31.12.2017 **137** Balken; der 150. Balken liegt am
**2018-01-14**. Fables Nachrechnung trifft.

---

### 25.3 Der Ersatztext — die Schliessung der Klasse

**Fables Wortlaut, zeichengleich übernommen** (`FABLE_ANTWORT_2026-09-20e_konjunktion.md`, Abschnitt (1)) —
**ersetzt Registertext 4a in 15.6 und den Ersatztext 21.3 (b); beide bleiben
als ersetzt stehen:**

> **Registertext 4a / 21.3 (b), Neufassung als ein Satz.** Ein Kalenderjahr ist
> Selektionsfalte eines Bots, wenn (i) es im registrierten Datenhorizont des
> Bots liegt und am 1. Januar der Indikator-Vorlauf erfüllt ist, **und** (ii)
> der Loader des Bots in ihm an mindestens einem Handelstag mindestens ein
> Symbol handelbar macht (Trockenlauf, 3b (b)). Die erste Selektionsfalte ist
> das erste Jahr, das beide Bedingungen erfüllt.
>
> ⭐ **(i) „im registrierten Datenhorizont des Bots" PRÄZISIERT durch Abschnitt 26 (TB-77, 21.09.2026), 26.2 — der Wortlaut bleibt stehen.** Der Horizont ist ein absolutes Datum je Bot (`asof` minus `RECENT_YEARS_ONLY`), nicht je Symbol; sein Wert ist ein Platzhalter, bis `asof` gesetzt ist (26.3).

**Herkunft — seine Rücknahme, wörtlich:** *„‚Der Plan bezieht die erste Falte
aus dem Trockenlauf' hätte den Aktien-Bots 1967 gegeben. Ich hatte den
Mechanismus als einseitig angenommen (der Loader verschiebt nach hinten) und
nicht bedacht, dass der Trockenlauf gegen den ganzen Kursbestand misst — und
der reicht bei yfinance bis 1962. Die Messung in beide Richtungen war die
richtige Reihenfolge; zurückgenommen."* Und warum die Konjunktion stärker ist
als die vorgelegte Lesart `max(4a, 3b (a))`: *„Damit kann (ii) den Beginn nie
vorziehen, weil (i) weiter gelten muss — und (i) kann ihn nie vorziehen, weil
(ii) weiter gelten muss. 21.3 (b) ist der Sonderfall, in dem (ii) später liegt;
seine Begründung beschreibt genau diesen Fall und keinen anderen."* Und: *„Es
gibt keine Lesart, in der 3b (a) allein bindet; sie war nie gemeint, und sie ist
nach der Neufassung auch nicht mehr formulierbar."*

**Was der Code seit heute tut — Tatsachennotiz** (Commit `e7a4108`, 20.09.2026):

| | |
|---|---|
| `research/vorregistrierung/faltenplan.py::erste_falte` | ist die Konjunktion: Kandidaten sind die Kalenderjahr-Falten ab `erste_falte_4a` (Bedingung (i), bisher `erste_falte`, Rechnung unverändert: Datenlage über `faltenplan_neun`, keine Konstante) bis zum Go-Live-Schnitt; die erste Kandidatenfalte, in der der Loader mindestens ein Symbol handelbar macht, ist die erste Falte |
| Bedingung (ii) | **gemessen, nicht nachgerechnet**: `research/faltenplan_neun/erste_falte_trockenlauf.py::erste_falte_nach_3b` ruft den Loader des Bots im Kindprozess des TB-40-Werkzeugs (`universum_trockenlauf.messe_bot`, mit Schreibschutz) am letzten Zeitpunkt der Falte auf (Lesart H, 16.2). `MIN_HISTORY_*` steht nirgends im Plan — es wirkt im Bot-Code, im Kindprozess (`T56b.6`: keine Konstantenkopie) |
| Bedingung (i) | **bleibt, wie der Plan sie heute rechnet** — Fables Präzisierung (*„im Datenhorizont" = `asof` minus `RECENT_YEARS_ONLY`*) und der Befund *je Symbol gegen je Markt* sind **TB-74** und nicht Gegenstand dieser Berichtigung. Für `t3_supertrend` ändert die Präzisierung nichts |
| Der Plan | trägt je Bot neu `erste_falte_4a` und `erste_falte_trockenlauf_H` (die Menge H je geprüfter Kandidatenfalte) — damit steht im Plan, **warum** er dort beginnt; `erste_falte_quelle` nennt die Neufassung |
| `ergebnisse/faltenplan_tb72.json` | der neue Plan, **daneben**; `faltenplan.json` (`0e54ac5c…`) unberührt — die Datei ist TB-30a-Stand (`K4k`) |
| Der Test | `research/faltenplan_neun/test_erste_falte_trockenlauf.py`, 50/50: neun Zahlen Plan = Trockenlauf (eigener `messe_bot`-Aufruf) = Register 21.4; erste Falte ≥ 4a; Mutationsprobe im eigenen Prozess (4a-Nachrechnung statt Ableitung → `t3_supertrend` 2018, rot). Fable: er ist *„nicht mehr eine Wache gegen Abweichung, sondern der Nachweis, dass die Ableitung nicht regrediert"* — so steht es in seinem Docstring |

⭐ *Fables Schluss zum Plan: „(i) ist keine Nachrechnung des Loaders, sondern
Arithmetik auf registrierten Konstanten; (ii) kommt aus dem Trockenlauf und
wird nicht nachgerechnet. Der Plan führt beide in einer Funktion zusammen — eure
Form — und kann in keiner Richtung verfehlen, weil er nichts selbst misst."*

---

### 25.4 Die Wirkung — gemessen und bekannt

**Lauf:** `research/vorregistrierung/benchmark.py --ziel ergebnisse/benchmark_drawdowns_tb72.json`
(Commit `27c58a2`, 20.09.2026, 20:29–20:31 Ortszeit, `trading-env` 3.9.6, `rc 0`),
Ergebnis **daneben**. `benchmark_drawdowns.json` (`a163c498…36d1ee`) und
`benchmark_drawdowns_vt.json` (`4549395f…8745d`) **byteweise unverändert**,
vorher wie nachher gemessen (`docs/belege/TB-72/nachweis3_sha256_*`).

**Gegenprobe der acht anderen Bots** (`docs/belege/TB-72/schritt4_gegenprobe_vt.txt`):
gegen `_vt.json` **zeichengleich** — 69 Falten × 100 Stufen = **6 900** Stufen,
`handelstage` und Symbolzahl je Falte, `handelbar_ab`, `DD_Toleranz` 8 × 100;
`json.dumps(sort_keys=True)` je Bot identisch. **Genau ein Bot ändert sich.**

**`t3_supertrend`** — Falten 2019 bis 2026 auf allen 100 Stufen gleich wie in
`_vt.json`; die Falte 2018 (0 Tage, 0 Symbole, 0,00) entfällt; der Median
`DD_Toleranz` über die Selektionsfalten:

| Exposure | `_vt.json` (mit 2018) | **`_tb72.json` (ohne 2018)** | Erwartung TB-65, Tabelle C1 *„ohne 2018"* |
|---|---|---|---|
| 25 % | −12,89 | **−13,90** | −13,90 ✅ |
| 50 % | −24,73 | **−26,57** | −26,57 ✅ |
| 100 % | −45,16 | **−48,10** | −48,10 ✅ |

**100 von 100 Stufen** verschieden; die Erwartung aus TB-65 trifft auf allen
drei ausgewiesenen Stufen.

⚠️ **`DD_Toleranz` wird damit nachgiebiger** — die Grenze, die ein
Parametersatz von `t3_supertrend` einhalten muss, liegt tiefer, weil der Median
nicht mehr eine Falte mit Drawdown 0,00 enthält. **Die Richtung geht zugunsten
des Bots, und das ändert an der Kategorie nichts: die Quelle des Grundes ist
die Regel** (F17; Fable wörtlich, siehe Kopf). Die Regel stand fest, bevor die
Zahl gerechnet wurde — in 21.3 (b) seit dem 19.09., in 21.4 mit genau dieser
Zeile, und in Fables Antwort (d), die *„Wirkung bekannt"* schreibt, bevor sie
den Vollzug anordnet.

---

### 25.5 Was diese Berichtigung ausdrücklich NICHT tut

| | |
|---|---|
| ⛔ | **Die Sperrlisten-Änderung nicht vollzogen** — `benchmark_drawdowns.json` und `benchmark_drawdowns_vt.json` sind byteweise dieselben Dateien, die neue Tabelle heisst `benchmark_drawdowns_tb72.json` und liegt daneben. Der Vollzug braucht die eigene Betreiberfreigabe aus 21.9 |
| ⛔ | **Den Tag nicht gesetzt.** Kein Selektionslauf, kein signierter Tag, kein Zeitanker |
| ⛔ | **`faltenplan.json` nicht überschrieben** (`0e54ac5c…`); der neue Plan heisst `faltenplan_tb72.json` |
| ⛔ | **Die MtM-Wirkung nicht gemessen** — TB-73, nach 24.3 |
| ⚠️ | **Bedingung (i) nicht präzisiert** — *„Datenhorizont"*, `RECENT_YEARS_ONLY = 10` als Datenuhr, `entry_cutoff` je Symbol gegen `fensteranker` je Markt: **TB-74** (Fables Antwort (3) und der dritte Befund). Bis dahin rechnet der Plan (i) wie bisher |
| ⚠️ | **`auswertung.py` eingefroren** (15.8 Nr. 3); die vier gesperrten Rechenfunktionen in `benchmark.py` unverändert; `T56b.6` (`registerdaten.MINDESTTRAINING_JAHRE`), G6/H3 aus TB-61, `registerbericht.py:178` (23.5) unverändert offen |

---

### In einfacher Sprache

**Was schiefstand:** Das Regelwerk sagt seit dem 19.09., wann das erste Jahr
eines Bots zählt — sobald sein Programm wenigstens einen Kurs überhaupt handeln
darf. Das Programm, das den Plan schreibt, rechnete das aber auf einem zweiten,
eigenen Weg nach und sagte in seinem eigenen Kopf, dass es die Regel nicht
anwendet. Bei einem Bot kamen beide Wege zu verschiedenen Ergebnissen: Er führte
ein Jahr, in dem er gar nichts handeln konnte.

**Was gemessen wurde, bevor etwas geändert wurde:** Ob es wirklich nur ein Bot
ist. In der erwarteten Richtung ja. In der anderen Richtung — das Programm dürfte
früher handeln, als das Regelwerk meint — sind es fünf Bots, vier davon ab 1967.
Das war nicht gemeint. Fable hat seinen eigenen Vorschlag daraufhin
zurückgenommen und die Regel neu gefasst: Ein Jahr zählt nur, wenn **beide**
Bedingungen gelten — die Datenlage **und** das Programm. Dann kann keine der
beiden den Beginn nach vorn ziehen.

**Was jetzt anders ist:** Der eine Bot beginnt 2019 statt 2018, mit sieben
Jahren statt acht. Und der zweite Rechenweg ist abgeschafft: Der Plan fragt das
Programm, was es kann, statt es nachzurechnen. Die beiden können nicht mehr
auseinanderlaufen; ein Test beweist das, indem er die alte Rechnung künstlich
wieder einsetzt und dabei rot wird.

**Was sich an Zahlen ändert:** Die Verlustgrenze dieses einen Bots wird etwas
weiter — von −45,2 auf −48,1 Prozent bei voller Investition. Das ist die
Wirkung, nicht der Grund; der Grund ist die Regel, und die stand vorher fest.
Die gesperrten Tabellen sind unberührt, die neue liegt daneben, und ob sie die
gesperrte ablöst, entscheidet der Betreiber.

*Nachgetragen in TB-72, 20.09.2026. Berichtigung mit Ersatztext: sie nennt den
Befund, die Instanz, den Ersatztext mit seiner Herkunft, die gemessene Wirkung
und das, was nicht getan wird — und entfernt nichts.*

---

## 26. Präzisierung zu Registertext 4a, Bedingung (i) — der Datenhorizont ist ein absolutes Datum je Bot, nicht je Symbol (TB-77, 21.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben**
— die Neufassung 4a / 21.3 (b) in 25.3 bleibt stehen (dort seit heute mit der
Marke *„(i) PRÄZISIERT durch Abschnitt 26"*), Registertext 3 (c) in 15.5 bleibt
stehen (Marke *„ERGÄNZT durch Abschnitt 26, 26.4"*), die Tatsachennotiz 21.4
bleibt unverändert gültig. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und die Form der
Abschnitte 21, 23, 24 und 25.

**Anlass:** Fables fünfte Antwort vom 20.09.2026
(`FABLE_ANTWORT_2026-09-20e_konjunktion.md`, Abschnitt (3)) hatte *„im
Datenhorizont"* als `asof` minus `RECENT_YEARS_ONLY` präzisiert und einen
dritten, ungefragten Befund danebengelegt: die Bots rechnen das Fenster **je
Symbol**, der Faltenplan **je Markt**. Abschnitt 25 hat beides ausdrücklich
offen gelassen (25.3, Tatsachennotiz Zeile „Bedingung (i)"; 25.5: *„Bedingung
(i) nicht präzisiert — TB-74"*). Die Anfrage
`FABLE_ANFRAGE_2026-09-21a_horizont_und_grenzfall.md` (Teil 1, Fragen (1) und
(2)) hat die Entscheidung erbeten; Fable hat sie am 21.09.2026 getroffen.

⚠️ **Herkunft des Wortlauts, nicht geglättet:** Fables Antwort vom 21.09. liegt
**nicht im Repo** — gemessen 21.09.2026 (`find` über das Repo: 0 Treffer für
`FABLE_ANTWORT_2026-09-21a*`; die Anfrage hatte um Ablage in der Projektablage
gebeten, `FABLE_UEBERGABE_2026-09-21_neuer_chat.md` Z. 9: *„sie kam als Datei
zurück"*). Der Wortlaut in 26.1 und 26.2 ist **zeichengleich aus
`docs/auftraege/MAC_TB-77_horizont_je_bot.md`, Abschnitt 0**, übernommen, das
ihn aus der Antwort zitiert. Das ist der einzige Träger im Repo; die Ablage der
Antwort selbst ist eine offene Bringschuld des steuernden Chats (26.6).

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Präzisierung,
Quelle des Grundes ist die Regel** — Registertext 4a (*„im registrierten
Datenhorizont"*) und Registertext 5e (der Lese-Audit, 17.4: kein Lesezugriff
ausserhalb des registrierten Horizonts). Eine Wirkung auf eine Zahl ist **nicht
bekannt und nicht gemessen** (26.6): es hat kein Selektionslauf stattgefunden,
kein Parametersatz ist bewertet, kein Ergebnis erzeugt. ⛔ **Dieser Abschnitt
rechnet nicht und fasst keinen Code an** — die vier `multi_symbol_optimise.py`
und `auswertung.py` sind unberührt (Nachweis: `git diff --numstat` in
`docs/ERGEBNIS_TB-77_horizont_je_bot.md`).

---

### 26.1 Der Befund — das Fenster je Symbol erzeugt Einstiege ausserhalb aller Falten, und sie laufen durch den Kapitalpfad

**Was der Code tut, gemessen 21.09.2026 (Stand `2e9cdf9`):**

| | Fundstelle | Wortlaut |
|---|---|---|
| Die Konstante | `strategies/elliott_wave_stocks/multi_symbol_optimise.py:54`, `rsi2_mean_reversion/…:52`, `turtle_soup_stocks/…:46`, `volatility_breakout/…:49` | `RECENT_YEARS_ONLY = 10`, bei allen vier Aktien-Bots, in Jahren (`pd.DateOffset(years=…)`). Die fünf Krypto-Bots haben keine |
| Der Bezug | dieselben Dateien, Z. 93 / 93 / 81 / 88 | `entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)` — relativ zum **letzten Kurs der Datei**, nicht zum Laufdatum (Datenuhr) |
| ⚠️ **Je Symbol** | dieselben Zeilen, **innerhalb der Ladeschleife** `for symbol in SYMBOLS`; abgelegt je Symbol (`data[symbol] = (df_ind, entry_cutoff)`, Z. 96 / 83 / 91; `elliott_wave_stocks` kappt in Z. 94 die Kursreihe des Symbols selbst) | Jedes Symbol bekommt sein eigenes Fenster, das an **seinem** letzten Kurstag hängt |
| Der Plan | `research/faltenplan_neun/faltenplan_neun.py::fensteranker`, Z. 271, Docstring Z. 272–278 | *„Genommen wird der SPAETESTE letzte Kurstag des Marktes, damit alle Symbole desselben Bots auf demselben Fenster liegen."* — **je Markt** |

**Das ist nicht dasselbe.** Ein Symbol, dessen Datei früher endet — delistet,
Datenlücke, stehengebliebene Datei —, bekommt beim Bot ein früheres Fenster und
liefert Trades aus einem Zeitraum, den der Plan für ausgeschlossen hält (so
gestellt in `FABLE_ANFRAGE_2026-09-21a…`, Teil 1 (c)).

⭐⭐ **Fables Begründung, und sie ist der eigentliche Befund — wörtlich** (aus
seiner Antwort vom 21.09.2026, zitiert nach `MAC_TB-77_horizont_je_bot.md`,
Abschnitt 0): Ein Symbol mit früherem Fenster erzeugt Trades aus Jahren **vor
der ersten Falte**. Die tauchen in keiner Falte auf —

> *„aber sie laufen durch den Kapitalpfad, belegen Plätze, verändern das
> Kapital, mit dem die erste Falte beginnt. Das ist ein Lesezugriff auf Zeiten
> ausserhalb des registrierten Horizonts, nur nicht über eine Datei, sondern
> über ein Fenster. Der Lese-Audit (5e) sieht ihn nicht, weil die Datei im
> Manifest steht."*

Deshalb ist die Frage *„je Bot oder je Symbol"* keine Handwerksfrage: Ein
Fenster je Symbol ist eine Lücke in Registertext 5e, die keine Datei und kein
Hash sichtbar macht — der Kapitalpfad (Registertext 1a) beginnt die erste
Falte mit einem Kapitalstand, der aus nicht registrierten Jahren stammt.

---

### 26.2 Der Registertext — Fables Präzisierung vom 21.09.2026, zeichengleich

**Ersetzt seine Fassung vom 20.09.2026** (`FABLE_ANTWORT_2026-09-20e_konjunktion.md`,
Abschnitt (3): *„4a, Präzisierung. ‚Im Datenhorizont' heisst: ab dem
Horizontbeginn des Bots, berechnet als registriertes `asof` (5a) minus
`RECENT_YEARS_ONLY` des Bots; das Ergebnis steht je Bot als absolutes Datum in
der Tatsachennotiz zu 4d. Der Vorlauf wird gegen dieses Datum gerechnet, nicht
gegen den ersten Kurs im Bestand."*). ⭐ **Gemessen 21.09.2026: diese Fassung
vom 20.09. ist nie in einen Registertext übernommen worden** — `grep -c` im
Register: `Horizontbeginn` **0**, `4a, Präzisierung` **0**; 25.3 und 25.5
verweisen sie ausdrücklich an TB-74. Es gibt darum im Register keine Stelle,
die als ERSETZT zu markieren wäre; ersetzt wird ein Wortlaut, der nur in
Fables Antwortdatei steht. Präzisiert wird die Neufassung in **25.3**,
Bedingung (i) *„im registrierten Datenhorizont des Bots"*, die stehen bleibt.

> **4a, Präzisierung (ersetzt die Fassung vom 20.09.).** Der Datenhorizont eines
> Bots ist ein absolutes Datum je Bot: Horizontbeginn = `asof` (5a) minus
> `RECENT_YEARS_ONLY` des Bots; Bots ohne diese Konstante haben keinen Horizont
> (Krypto). Das Datum steht je Bot in der Tatsachennotiz zu 4d. Es gilt für alle
> Symbole des Bots gleich; ein Symbol trägt vor dem Horizontbeginn keinen
> Einstieg bei, unabhängig davon, wann seine Kursdatei beginnt oder endet. Das
> Ende der Kursdatei eines Symbols bestimmt nach 3b (b), an welchen Tagen es
> handelbar ist — nie sein Fenster.

**Was der Text festlegt, in drei Sätzen:** Das Fenster ist eine Zahl **je
Bot**, und der Code muss nachgeben, nicht der Plan (Antwort auf Frage (1) der
Anfrage). Es hängt an `asof` aus Registertext 5a — dem Bezugsdatum, das *„aus
dem Register, nie aus der Uhr"* kommt (17.1) —, nicht am letzten Kurs einer
Datei. Und das Ende einer Kursdatei behält genau eine Rolle: es entscheidet
nach 3b (b), an welchen Tagen das Symbol handelbar ist.

⚠️ **Was der Text braucht und was es heute nicht gibt:** `asof`. Registertext
5a sagt seit TB-48, woher es kommt; **es steht nirgends als Wert** — gemessen
21.09.2026 in allen `.py` (8 Zeilen, alle pandas `merge_asof`), allen `.json`
(1 Eintrag, derselbe Bezeichner), im Register (3 Zeilen, Formel und Herkunft),
in `ergebnisse/`, im Snapshot-Manifest (15 Schlüssel, keiner `asof`), in
`registerdaten.py` und in `docs/` (`docs/belege/TB-77/schritt1_blocker_nachgemessen.md`,
Nachweis 2). *Ein Registertext, der auf einen Wert zeigt, den es nicht gibt,
ist kein Fehler — solange er sagt, dass es ihn nicht gibt.* Das tut 26.3.

---

### 26.3 Tatsachennotiz zu 4d — der Horizontbeginn je Bot: ⚠️ Platzhalter, weil `asof` nicht gesetzt ist

Nach 26.2 steht das Datum je Bot in der Tatsachennotiz zu 4d (21.4). **Es kann
heute nicht eingetragen werden**, weil der Minuend fehlt. Nach dem Muster von
23.3 (Fassung TB-66) steht hier ein sichtbarer Platzhalter und **keine
erfundene Zahl**:

| Bot | Markt | `RECENT_YEARS_ONLY` | Horizontbeginn = `asof` − Konstante |
|---|---|---:|---|
| `elliott_wave` | krypto | keine | **kein Horizont** (26.2) |
| `t3_supertrend` | krypto | keine | **kein Horizont** |
| `rsi2_crypto` | krypto | keine | **kein Horizont** |
| `turtle_soup_crypto` | krypto | keine | **kein Horizont** |
| `volatility_breakout_crypto` | krypto | keine | **kein Horizont** |
| `elliott_wave_stocks` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |
| `rsi2_mean_reversion` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |
| `turtle_soup_stocks` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |
| `volatility_breakout` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |

Die Konstante je Bot ist aus dem Code **gelesen** (Fundstellen 26.1), nicht
registriert; ob sie als registrierte Grösse in `registerdaten.py` gehört, ist
Teil von 26.6.

⚠️ **Abgegrenzt, damit es niemand für den Wert hält:** 15.6, Punkt 3, nennt
seit dem 15.09.2026 *„gemessen vom letzten Kurstag (2026-09-01) zurück auf
2016-09-01 — so rechnen die vier Aktien-Bots selbst."* Das ist die **Datenuhr**
(letzter Kurs im damaligen Bestand), also genau der Bezug, den 26.2 ablöst —
**kein `asof`** und kein Horizontbeginn im Sinne dieses Abschnitts. Der Wert
wandert nicht in die Tabelle. Wann und wodurch `asof` gesetzt wird, ist als
Frage (1) in `FABLE_UEBERGABE_2026-09-21_neuer_chat.md`, Abschnitt 4, an Fable
gestellt (Lesart des steuernden Chats dort: *„mit dem Snapshot und dem
signierten Tag zugleich"* — **nicht entschieden, hier nicht vorweggenommen**).

**Was der Platzhalter für den Faltenplan bedeutet:** Bedingung (i) wird bis
zum Eintrag *„wie bisher"* gerechnet (25.3, Tatsachennotiz), also mit dem
Fenster aus `faltenplan_neun.fensteranker` (je Markt, Datenuhr). Die
Faltenliste 21.4 ist damit **vorläufig in (i)** und **endgültig in (ii)**; nach
15.6 Punkt 3 *„bindet das Fenster die Faltenliste nicht"* — ob das mit einem
registrierten `asof` so bleibt, ist erst mit dem Wert prüfbar.

---

### 26.4 Ergänzung zu Registertext 3 (c) — die Reichweite des Survivorship-Vorbehalts

Registertext 3 (c) (15.5) trägt den Vorbehalt *„Beide sind
survivorship-behaftet … Grösse unbekannt"*. Er bleibt zeichengleich stehen und
wird ergänzt:

> **3 (c), Ergänzung (TB-77, 21.09.2026):** Der Survivorship-Vorbehalt gilt für
> die Jahre im Horizont; dass der Horizont zehn Jahre umfasst, begrenzt die
> Reichweite des Vorbehalts, ändert ihn nicht.

*Warum die Ergänzung nötig ist:* `RECENT_YEARS_ONLY` steht im Code als
Gegenmassnahme gegen den Survivorship-Bias (`multi_symbol_optimise.py:52`
und `:49`: *„reduziert Survivorship Bias"*; `UEBERGABEPROTOKOLL.md` Z. 170).
Ein Leser könnte den Horizont darum für eine **Milderung** des Vorbehalts
halten. Er ist keine: Innerhalb der zehn Jahre ist das Universum dieselbe
heutige Liste, mit derselben erwarteten Richtung (*„Bevorzugung von Sätzen mit
weiten oder fehlenden Stops und langen Zeitbremsen"*). Der Horizont sagt nur,
**für welche Jahre** der Vorbehalt ausgesprochen wird.

---

### 26.5 Tatsachennotiz zur Herkunft — alle bisherigen Ergebnisdateien der vier Aktien-Bots sind mit Fenstern je Symbol gerechnet

Gemessen 21.09.2026 (`docs/belege/TB-77/schritt1_blocker_nachgemessen.md`,
letzter Abschnitt): `results/<bot>/multi_symbol_optimisation_results.csv` hat
bei jedem der vier Aktien-Bots genau **einen** Commit und ist seitdem
unverändert; im selben Commit steht der Optimierer bereits mit
`df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)` innerhalb der
Ladeschleife, und `git log -S` kennt keinen älteren Stand des Ausdrucks:

| Bot | Ergebnisdatei (Commit) | Optimierer je Symbol seit |
|---|---|---|
| `elliott_wave_stocks` | `0f6491b`, 02.09.2026 | `0f6491b` |
| `rsi2_mean_reversion` | `f56c6d2`, 03.09.2026 | `f56c6d2` |
| `turtle_soup_stocks` | `88b9050`, 04.09.2026 | `88b9050` |
| `volatility_breakout` | `b603861`, 03.09.2026 | `b603861` |

**Folge:** Jede dieser Tabellen ist mit einem Fenster **je Symbol** an dessen
letztem Kurstag gerechnet — nicht mit dem Horizont aus 26.2. Das ist **ein
Grund mehr**, warum sie mit den Zahlen des Laufs nicht vergleichbar sind; die
anderen Gründe stehen in Registertext 7 (Backtester-Prüfung, 16.5) und in der
Warnung zu den Papierpfaden vor dem Umstellungstag (`CLAUDE.md`, TB-38). Sie
bleiben liegen, wo sie liegen, und werden nicht neu gerechnet (26.6). *Nicht
gemessen:* ob weitere, abgeleitete Ergebnisse unter `research/` dieselben
Loader importiert haben; wo sie es taten, gilt dasselbe.

---

### 26.6 Was folgen muss — und hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **`asof` setzen.** Wann und wodurch, ist Fables Frage (1) im neuen Chat; die Lesart *„mit Snapshot und Tag zugleich"* ist nicht entschieden. Bis dahin bleibt 26.3 ein Platzhalter | Betreiber / Fable, vor dem Tag |
| ⛔ | **Tatsachennotiz 4d füllen:** vier Daten in 26.3, je `asof` minus zehn Jahre, mit Fundstelle des `asof`-Wertes. Danach prüfen, ob das Fenster die Faltenliste 21.4 in (i) weiterhin nicht bindet | Registernachtrag, sobald `asof` steht |
| ⛔ | **Die vier Optimierer:** `entry_cutoff` **einmal je Bot aus dem Register** statt je Symbol aus `df["open_time"].max()` (Fundstellen 26.1). Sie brauchen denselben Wert; ohne `asof` gibt es nichts einzutragen | **TB-30b** (Umstellung des Laufcodes) |
| ⛔ | **Die Wache** *„kein Einstieg eines Bots liegt vor dessen Horizontbeginn"* — Fable schlägt sie *„billig, in den Auswerter"* vor. `auswertung.py` ist **eingefroren** (Abschnitt 0, Z. 31; 15.8 Nr. 3; Sperrliste 10 Nr. 5); ein eingefrorenes Skript, das einmal geöffnet wird, ist nicht mehr eingefroren. **Samt Mutationsprobe:** Fenster je Symbol wieder einschalten → die Wache muss rot werden | **TB-30b**, mit den Optimierern |
| ⛔ | **Fables Antwort vom 21.09. ablegen** (`FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md`) — sie liegt in keinem Träger; bis dahin trägt Abschnitt 0 des Auftrags den Wortlaut | steuernder Chat |
| ⚠️ | **`RECENT_YEARS_ONLY` als registrierte Grösse** (`registerdaten.py`) statt als Codekonstante, die aus vier Dateien gelesen wird — Fable nennt sie *„registrierte Konstante"* (20.09., Abschnitt (3)); eingetragen ist sie nur als Tatsachennotiz (15.6 Punkt 3, 26.3). Ob das eine Registeränderung oder eine Codekopie ist, entscheidet der Betreiber (vgl. `T56b.6`: keine Konstantenkopien) | Entscheidungsvorlage, nicht vollzogen |
| ⚠️ | **Nicht gemessen:** ob und wie viele Einstiege in den bisherigen Ergebnisdateien vor einem Horizontbeginn liegen. Ohne `asof` gibt es die Grenze nicht, gegen die man zählen könnte; und die Zahl wäre eine Aussage über Ergebnisse, die mit dem Lauf ohnehin nicht vergleichbar sind (26.5) | — |

⛔ **Nicht getan:** kein Bot-Code, kein `auswertung.py` (auch nicht der
Docstring), kein `registerdaten.py`, keine Sperrlisten-Datei
(`benchmark_drawdowns.json` `a163c498…`, `faltenplan.json` `0e54ac5c…`
byteweise unverändert), kein Tag, kein Lauf.

---

### 26.7 Der Grenzfall — was gilt, wenn für einen Bot kein Parametersatz besteht: die Kette (b) → Festlegung 11 → Registertext 6 (b) → Schatten

**Das ist ein Verweis, keine Berichtigung.** Fables Teil 2 vom 21.09.2026
(Antwort auf `FABLE_ANFRAGE_2026-09-21a…`, Teil 2, Fragen (3) und (4))
entscheidet den Fall, den die Anfrage für ungeregelt hielt — und die
Entscheidung steht bereits im Register, an vier Stellen, die bisher niemand als
Kette gelesen hat. **Jede Stelle nachgemessen 21.09.2026 (Stand `2e9cdf9`):**

| Glied | Fundstelle | Wortlaut |
|---|---|---|
| **1. Der Fall ist ein Abbruchkriterium** | Abschnitt 7, **(b)**, Z. 686; Präzisierung Z. 692–694 | *„**(b)** Kein Parametersatz erfüllt die Drawdown-Bedingung in allen Falten"* — *„Gewinnen kann nur ein zulässiger Punkt. Ist keiner zulässig, greift (b); berichtet wird dann der Plateau-Gewinner über alle Zellen, ausdrücklich mit der Markierung ‚nicht zulässig'."* |
| **2. Bleibt/Geht läuft über die Abbruchkriterien** | Abschnitt 1, **Festlegung 11** (`registerdaten.FESTLEGUNGEN[11]`) | *„DSR ist Bericht, nicht Tor — Bleibt-Geht läuft über die Abbruchkriterien."* Ein Bot, der (b) erfüllt, **bleibt nicht** |
| **3. Die Stufe** | 16.4, **Registertext 6, Buchstabe (b)** | *„jeder, der eines erfüllt, auf **Schatten** — sein Budgetanteil hält die statische Benchmark-Position in Höhe seines mittleren Exposures. Die Zuweisung ist Ergebnis des eingefrorenen Skripts, keine Lesung."* |
| **4. Was Schatten heisst, und der Weg zurück** | Registertext 6 (a) und (d), 16.4; Abschnitt 7.1 | Schatten: *„läuft, kein Portfoliogewicht, nicht in Portfolio-Zahlen und nicht am Crash-Knopf"* — mit seinen heutigen Parametern. Kapital: *„statische Benchmark-Position in Höhe des mittleren Exposures — nicht in Kasse, nicht zu den Überlebenden."* Rückkehr: *„nur über einen neuen registrierten Lauf"* (6 (d)); *„Kein ‚vorerst behalten'"* (7.1) |
| **5. Das Ergebnis ist zulässig, auch bei mehreren oder allen** | **Festlegung 12** (wörtlich, Abschnitt 1) und 7.1 | *„Es kann sein, dass kein einziger Bot die Schwelle erreicht."* — *„Die Anzahl ausscheidender Bots ist KEIN Grund, eine Schwelle zu ändern."* |

**Die Kette ist im eingefrorenen Skript bereits Code:** `auswertung.py::kapitalregel`
(Z. 554–576) gibt `kapitalregel`, `schattenregel`, `schwellenregel` und
`zulaessiges_ergebnis` (`rd.FESTLEGUNGEN[12][1]`) am Ende jeder Bleibt-Geht-Liste
aus; `test_vorregistrierung.py` Teil D prüft
`b_kein_satz_besteht_die_drawdown_bedingung` (Z. 288, 348–350). **Fällt ein
Bot nach (b), gibt es nach dem Lauf keine Entscheidung, nur eine Lektüre**
(Abschnitt 0).

⚠️ **Zwei Aktenzeichen aus Fables Antwort, nachgemessen und nicht übernommen**
(`registerdaten.FESTLEGUNGEN`, `docs/belege/TB-77/schritt1_blocker_nachgemessen.md`,
Nachweis 4): Fable nannte *„Festlegung 10"* für Bleibt/Geht über die
Abbruchkriterien — das ist **11** (10 ist die DSR-Basis, N = 653); und
*„Festlegung 11"* für „mehrere oder alle" — das ist **12**. Sein Vorbehalt
*„fehlt (b) im Registertext"* ist gegenstandslos: (b) steht in Abschnitt 7,
wörtlich.

⚠️ **Quelle, nicht geglättet:** Fable verweist für Teil 2 auf ein Dokument
`FABLE_ANTWORT_2026-09-20a_grenzfall`. **Es existiert nicht** — weder im Repo
(gemessen 21.09.2026, 13:50 durch den steuernden Chat; hier nachgemessen:
`find` 0 Treffer für `*grenzfall*` ausser der Anfrage vom 21.09.) noch in der
Projektablage (`FABLE_UEBERGABE_2026-09-21_neuer_chat.md`, Abschnitt 4 (3)).
Vom 20.09. liegen vier Antworten vor: Kalender, Kapitalpfad, MtM-Messung,
Konjunktion. **Quelle dieses Abschnitts ist allein seine Kurzfassung vom
21.09.2026**, wie sie der Auftrag (`MAC_TB-77_horizont_je_bot.md`, Schritt 3)
und die Übergabe an den neuen Chat (`FABLE_UEBERGABE…`, Abschnitt 3 (e))
wiedergeben — das fehlende Dokument wird nicht zitiert.

⭐ **Und die Antwort auf Frage (4) der Anfrage — ob vorab gemessen werden darf,
wie viele Sätze die härtere Bedingung kostet:** *nein.* Fable, nach
`FABLE_UEBERGABE…` Abschnitt 3 (e): *„Die Zahl der zulässigen Sätze je Bot ist
der Ausgang des Laufs — die erste Hälfte des Laufs selbst."* Das ist dieselbe
Linie wie 24.3 (*„vor jeder Messung"*), nur eine Stufe strenger: dort war die
Zahl folgenlos, hier wäre sie eine Aussage über den Ausgang. **Es wird nicht
gemessen.** Diese Sitzung hat es nicht getan (26.6, letzte Zeile).

---

### In einfacher Sprache

**Was entschieden ist:** Die „letzten zehn Jahre", auf die ein Aktien-Bot bei
der Auswahl schaut, gelten künftig für den ganzen Bot — nicht für jedes
Wertpapier einzeln. Heute rechnet jeder Bot das Fenster für jedes Wertpapier
von dessen letztem Kurs aus zurück. Endet die Kursdatei eines Wertpapiers
früher, liegt sein Fenster früher — und der Bot handelt darin in Jahren, die
offiziell gar nicht ausgewertet werden. Diese Geschäfte tauchen in keiner
Jahresfalte auf, aber sie verändern still das Kapital, mit dem das erste
ausgewertete Jahr beginnt. Der Lesewächter merkt das nicht, weil die Datei
selbst erlaubt ist.

**Was dabei auffiel:** Die neue Regel braucht ein Stichtagsdatum (`asof`), von
dem aus die zehn Jahre zurückgerechnet werden. Das Regelwerk sagt seit dem
18.09., dass es dieses Datum aus dem Register bekommt — **aber es steht
nirgends.** Gesucht wurde im ganzen Code, in allen Ergebnisdateien, im
Datenschnappschuss und im Register selbst. Und die Wache, die Fable
vorschlägt, gehört in eine Datei, die eingefroren ist und bis zum Umbau
(TB-30b) nicht angefasst wird.

**Was dieser Abschnitt deshalb tut:** Er schreibt die Regel wörtlich auf und
setzt dort, wo das Datum stehen müsste, einen sichtbaren Platzhalter — statt
eine Zahl zu erfinden. Das Datum, das dem Wert am nächsten kommt (2016-09-01
aus dem Jahr 2026 zurück), steht ausdrücklich daneben als das, was es ist: der
alte Bezug, nicht der neue. Ausserdem hält er fest, dass alle bisherigen
Auswahltabellen der vier Aktien-Bots noch mit dem alten Fenster je Wertpapier
gerechnet sind — ein Grund mehr, sie nicht mit dem Lauf zu vergleichen.

**Und der Grenzfall:** Was passiert, wenn für einen Bot am Ende gar keine
Einstellung die Verlustgrenze in allen Jahren einhält? Die Antwort stand
schon da, verteilt auf vier Stellen: Das ist Abbruchkriterium (b); der Bot
bleibt nicht; er läuft mit seinen heutigen Einstellungen als Schatten ohne
Geld weiter; sein Geld geht in eine feste Marktposition; zurück kommt er nur
über einen neuen, vorher registrierten Lauf. Und vorher nachzuzählen, wie
viele Einstellungen die härtere Grenze kostet, ist verboten — die Zahl verriete
den Ausgang.

*Nachgetragen in TB-77, 21.09.2026. Präzisierung mit Registertext, Platzhalter
und Verweis: sie nennt den Befund mit seinen Fundstellen, den Registertext mit
seiner Herkunft, den fehlenden Wert als fehlend, die Ergänzung zu 3 (c), die
Herkunft der bisherigen Ergebnisse, die Kette des Grenzfalls und das, was
nicht getan wird — und entfernt nichts.*

---

## 27. Sichtschutz des Verfahrensprüfers (Fable 21g, 21.09.2026)

⭐ **Neuer Registertext, keine Berichtigung.** Er regelt, was der
Verfahrensprüfer vor dem signierten Tag wissen darf — und damit, ob seine
Registerentscheidungen nachträgliche Wahlen sein können. Quelle des Grundes
nach F17; die Regel nennt kein Ergebnis.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21g_sichtschutz_nullpunkt.md`,
Abschnitt 3, zeichengleich übernommen. Vorgeschichte: 21d (Fables Vorschlag),
dazu zwei Messungen des steuernden Chats vom 21.09. — das Register ist rein
(24 Sharpe-Erwähnungen, alle Regeltext, keine gemessene Kennzahl je
Parametersatz), `BACKLOG.md` ist es nicht (Z. 190 `W14`, Z. 170 `T39.2`).

### 27.1 bis 27.5 — der Registertext, zeichengleich

> **27. Sichtschutz des Verfahrensprüfers**
>
> **27.1** Der Verfahrensprüfer erhält vor dem signierten Tag keine Ergebnisgrössen des Selektionsraums: keine Kennzahl eines Parametersatzes (Sharpe, Rendite, Drawdown, Trefferquote, Anzahl Trades), keine Aussage, welche oder wie viele Sätze eine Bedingung erfüllen, keine Rangfolge, keine Plateau-Lage — **und keine Erwartung, Schätzung oder Prognose über den Ausgang des Laufs**, gleich ob als Zahl oder als Satz.
>
> **27.2** Zulässig sind Verfahrensmessungen — Kalender, Datenbestand, Faltenzahl, Handelbarkeit, Benchmark-Seite — und Wirkungen einer Regel auf die registrierten heutigen Parameter, wenn die Regel vor der Messung geschrieben stand (Bauart 24.3).
>
> **27.3** Das Register darf der Verfahrensprüfer vollständig lesen; was darin steht, hat dieses Tor bereits passiert (gemessen 21.09.: keine Kennzahl je Parametersatz im Registertext). Eine Ablage-Kopie trägt Commit-Hash, Datum und die Kennzeichnung KOPIE.
>
> **27.4** Der Verfahrensprüfer führt in jeder Antwort ein Leseprotokoll (welche Dateien er in diesem Chat gelesen hat). Das Protokoll ist Selbstauskunft. Die Prüfung, ob seine Begründungen Grössen nach 27.1 enthalten, ist Pflicht des steuernden Chats (Prüfprinzipien).
>
> **27.5** Wer dem Verfahrensprüfer einen Treffer nach 27.1 in einer Datei meldet, nennt Datei und Fundstelle, nicht den Inhalt.
>
> **Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim Inkrafttreten (21.09.2026):**
> Der Chat des Verfahrensprüfers wurde am 21.09. neu begonnen; er kennt aus dem Vorgängerchat nichts. Sein Wissensstand beim Inkrafttreten ist vollständig: der Wortlaut von `FABLE_UEBERGABE_2026-09-21_neuer_chat.md` (Fassung 2) und die Dateien `FABLE_ANTWORT_2026-09-20e_konjunktion.md`, `FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md`, `FABLE_ANTWORT_2026-09-21b_asof_und_wache.md`, alle in der Projektablage. Darin enthaltene Grössen, die an 27.1 grenzen: die Wirkung von Abschnitt 23 auf die DD-Toleranz der fünf Krypto-Bots (2,4- bis 5,0-fach); die Zahlen aus 24.6 (59 von 64 Falten tiefer, Mediane je Bot −1,39 bis −3,09 Prozentpunkte, fünf Falten flacher; Krypto 2018–2020 nicht enthalten). Beides sind Wirkungen auf die heutigen Parameter, gemessen nach der jeweils vorher geschriebenen Regel (27.2). Dazu, am 21.09. durch eine Treffermeldung mitgeteilt: der Wortlaut der Erwartung in `BACKLOG.md` Zeile 190 (W14) über die Zahl der Bots auf Schatten — eine Erwartung nach 27.1, keine Messung; sie lag nach Festlegung 12 als Möglichkeit bereits vor. Weitere Grössen nach 27.1 kennt der Verfahrensprüfer nicht.

### 27.6 Wo der Nullpunkt liegt

⭐ **Die Protokollkette beginnt nicht mit 21d, sondern mit der Tatsachennotiz
oben.** Fable, 21g Abschnitt 4: *„Der Sichtschutz regelt den Grund, nicht den
Zugriff — und ein Grund lässt sich nicht rückwirkend entkennen."* Die
Rückwirkung ist deshalb **Bestandsaufnahme, kein Pflichtenrückbau**: *„Was ich
beim Inkrafttreten wusste, wird festgehalten, nicht bewertet."*

**Für den Vorgängerchat des Verfahrensprüfers** gilt: seine Entscheidungen
(Abschnitte 23–26) sind registriert, und die Reihenfolge Regel → Messung ist im
Register selbst dokumentiert (24.3 vor 24.6). Was er sonst wusste, ist nicht
mehr feststellbar und muss es nicht sein — die Prüfung nach 27.4 ist auf seine
Begründungen genauso anwendbar, und sie liegen vollständig vor.

### 27.7 Ein Verstoss beim Melden des Verstosses — festgehalten, nicht geglättet

⚠️ Der steuernde Chat hat Fable am 21.09. den **Inhalt** des Sichtschutz-Treffers
zitiert (`BACKLOG.md` Z. 190 wörtlich) statt seiner Fundstelle. Fable hat es
selbst gemeldet und in die Tatsachennotiz eingetragen: *„Durch das Zitat kenne
ich die Zeile jetzt."*

⭐ **Daraus ist 27.5 entstanden.** Der Fehler steht hier, weil er die Regel
erzeugt hat und weil die Fehlerklasse benannt gehört: **wer prüft, fasst an** —
dieselbe Klasse, gegen die `A1` und `B1` gebaut sind.

### 27.8 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Register-KOPIE in die Projektablage legen** (mit Commit-Hash, Datum, Kennzeichnung KOPIE nach 27.3). Sie wird erst gezogen, **nachdem** alle Abschnitte dieser Aufgabe stehen — eine Kopie des Zwischenstands liefe sofort auseinander | steuernder Chat, nach TB-78 |
| ⛔ | **`BACKLOG.md` bereinigen oder verschieben.** 27.1 verlangt es nicht; die Regel liegt beim Leser, nicht bei der Datei | — |
| ⚠️ | **Die Prüfung nach 27.4** (Fables Begründungen gegen verbotene Grössen lesen) ist eine stehende Pflicht des steuernden Chats, kein Schritt dieser Aufgabe. Sie steht ab jetzt als Prüfprinzip `A8` (Schritt 4) | laufend |

---

## 28. `asof` ist gesetzt — Berichtigung zu 26.3 und 26.6, und der Vorlauf-Satz gilt fort (TB-78, 21.09.2026)

⭐ **Drei Berichtigungen, Kategorie „Berichtigung" nach F17** (Registertext an
Registertext; die Quelle des Grundes ist eine Entscheidung des
Verfahrensprüfers, kein Ergebnis).

⚠️ **Abschnitt 26 bleibt zeichengleich stehen.** Was dort überholt ist, wird
hier benannt und trägt seine ERSETZT-Marke an dieser Stelle.

### 28.1 Warum es eine Berichtigung braucht — der Auftrag lief mit überholter Prämisse

**Gemessen 21.09.2026:** TB-77 hat durchgehend gegen die ursprüngliche
Auftragsfassung gearbeitet; der Nachtrag, der zwei Blocker aufhob, ist nie
angekommen (`grep` über Ergebnisdokument und `docs/belege/TB-77/` nach
*„Nachtrag zu TB-77"* und `FABLE_ANTWORT_2026-09-21b`: **0 Treffer**).

⭐ **Regel daraus, festgehalten, weil sie teuer war:** *Nach jeder Antwort des
Verfahrensprüfers werden die **laufenden** Aufträge gegen sie geprüft, nicht nur
die kommenden. Ein Nachtrag in eine laufende Sitzung ist billiger als eine
Berichtigung im Register.*

### 28.2 Registertext 5a, Ergänzung — woher `asof` kommt

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21b_asof_und_wache.md`,
Abschnitt (2), zeichengleich.

> **Registertext 5a, Ergänzung:** asof ist das UTC-Datum des Erstellungszeitpunkts des registrierten Snapshots. Es wird im `MANIFEST.json` als Feld `asof` geführt und im Register als Tatsachennotiz neben dem Snapshot-Hash eingetragen. Ein neuer Snapshot (5c) setzt ein neues asof.

**Fables Begründung, warum das Erstellungsdatum und nicht das Datenende** — im
Wortlaut, weil sie den Unterschied trägt:

> *„Das Datenende (grösstes `open_time` über alle Kursdateien) wäre eine zweite aus dem Inhalt abgeleitete Grösse — genau die Bauart, die ich bei `fensteranker` abgelehnt habe, weil sie mit den Daten wandert. […] Dieser Abstand ist eine Frische-Tatsache und gehört als eigenes Manifest-Feld (`datenende`) dorthin, nicht in asof. Das Erstellungsdatum ist bereits registriert, von niemandem anders berechenbar und unabhängig davon, welches Symbol zuletzt eine Kerze hatte."*

**Bekannte Wirkung auf die Zulässigkeit, aus derselben Quelle:** Der
Horizontbeginn verschiebt sich gegenüber dem Datenende um vier Tage (19.09.
statt 15.09.). Die erste Falte nach 4a beginnt am 1. Januar eines Jahres; eine
Verschiebung im September ändert das Jahr nicht. ⭐ *Das ist eine
Kalenderaussage, keine Ergebnisaussage.*

### 28.3 Tatsachennotiz — der Wert von `asof`

| | Wert | Fundstelle |
|---|---|---|
| **`asof`** | **`2026-09-19`** | Abschnitt 18, `zeitpunkt_utc` = `2026-09-19T06:49:32+00:00`, gelesen aus `snapshots/63e4b6c8…/MANIFEST.json` |
| Snapshot | `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` | Abschnitt 18, Commit `1075dec` |

⭐ **Der Wert ist keine neue Messung.** Er stand seit dem 19.09. als Tatsache im
Register; was fehlte, war die Zeile, die ihn `asof` nennt.

### 28.4 ⚠️ ERSETZT: die Platzhalter-Tabelle in 26.3

**Die vier Platzhalter-Zeilen in 26.3** — *„[PLATZHALTER — `asof` ist nicht
gesetzt; Datum folgt, sobald 5a einen Wert hat]"* — **gelten als ERSETZT.** Sie
bleiben dort zeichengleich stehen (append-only). Die gültige Fassung:

| Bot | Markt | `RECENT_YEARS_ONLY` | Horizontbeginn = `asof` − Konstante |
|---|---|---:|---|
| `elliott_wave` | krypto | keine | **kein Horizont** (26.2) |
| `t3_supertrend` | krypto | keine | **kein Horizont** |
| `rsi2_crypto` | krypto | keine | **kein Horizont** |
| `turtle_soup_crypto` | krypto | keine | **kein Horizont** |
| `volatility_breakout_crypto` | krypto | keine | **kein Horizont** |
| `elliott_wave_stocks` | aktien | 10 Jahre | **2016-09-19** |
| `rsi2_mean_reversion` | aktien | 10 Jahre | **2016-09-19** |
| `turtle_soup_stocks` | aktien | 10 Jahre | **2016-09-19** |
| `volatility_breakout` | aktien | 10 Jahre | **2016-09-19** |

⚠️ **Die Konstante ist aus dem Code gelesen** (Fundstellen 26.1), nicht
registriert. Ob sie als registrierte Grösse nach `registerdaten.py` gehört,
bleibt offen — siehe 28.7.

⚠️ **Abgegrenzt, damit es niemand verwechselt:** 15.6 Punkt 3 nennt
*„gemessen vom letzten Kurstag (2026-09-01) zurück auf 2016-09-01"*. Das ist die
**Datenuhr**, genau der Bezug, den 26.2 ablöst — **kein `asof`**. Die
Ähnlichkeit der beiden Daten (2016-09-01 gegen 2016-09-19) ist Zufall des
Kalenders und kein Hinweis darauf, dass es dasselbe wäre.

### 28.5 ⚠️ ERSETZT: die zwei Zeilen in 26.6, die `asof` als offen führen

**Zeile 1 von 26.6** — *„`asof` setzen. Wann und wodurch, ist Fables Frage (1)
im neuen Chat; die Lesart ‚mit Snapshot und Tag zugleich' ist nicht entschieden.
Bis dahin bleibt 26.3 ein Platzhalter"* — **ist ERSETZT.** Entschieden seit
21b: **durch den Snapshot, nicht durch den Tag.** Fable, wörtlich: *„Nicht mit
dem signierten Tag — der Tag friert ein, was das Register sagt; er erzeugt keine
Zahl."*

**Zeile 2 von 26.6** — *„Tatsachennotiz 4d füllen: vier Daten in 26.3"* — **ist
mit 28.4 erledigt.**

**Zeile 4 von 26.6** (die Wache in `auswertung.py`) — **ist ERSETZT.** Fable hat
seinen eigenen Vorschlag am 21.09. zurückgezogen: *„Mein Vorschlag ‚in den
Auswerter' war falsch adressiert."* Die Wache geht in die vier
`multi_symbol_optimise.py` (TB-30b). ⚠️ **Und sie prüft nicht gegen den
Horizontbeginn, sondern gegen den Beginn der ersten Selektionsfalte** —
siehe Abschnitt 29.

**Zeile 5 von 26.6** (`FABLE_ANTWORT_2026-09-21a` liegt in keinem Träger) — **ist
mit Schritt 0 dieser Aufgabe erledigt**; die Datei liegt unter
`docs/projektfuehrung/`.

⭐ **Unverändert offen bleiben:** Zeile 3 (die vier Optimierer, TB-30b), Zeile 6
(`RECENT_YEARS_ONLY` als registrierte Grösse, Entscheidungsvorlage) und Zeile 7
(nicht gemessen, wie viele Einstiege vor einem Horizontbeginn liegen).

### 28.6 Registertext 4a, Präzisierung, Ergänzung — der Vorlauf-Satz gilt fort

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21c_uebergabe_und_vorlauf.md`,
Abschnitt 3.1, zeichengleich.

> **4a, Präzisierung, Ergänzung:** Der Indikator-Vorlauf nach (i) wird gegen den Horizontbeginn des Bots gerechnet, nicht gegen den ersten Kurs im Bestand. Der Satz aus der Fassung vom 20.09. gilt fort; die Fassung vom 21.09. hat ihn nicht ersetzt, sondern ausgelassen.

**Quelle des Grundes,** Fable wörtlich: *„Ein Vorlauf, der auf Kursen vor dem
Horizontbeginn rechnet, ist derselbe Zugriff"*, den Abschnitt 26 verbietet.
Kategorie: **Berichtigung** (Registertext an Registertext). Kein Ergebnis.

**Die Messung dazu, 21.09.2026, 17:48 durch den steuernden Chat:** Der Satz
*„Der Vorlauf wird gegen dieses Datum gerechnet, nicht gegen den ersten Kurs im
Bestand"* steht im Register **genau einmal**, in **Z. 4307** — und zwar
**innerhalb des Zitats der als ersetzt markierten Fassung** in 26.2. Er steht
also im Register ausschliesslich als Teil dessen, was ausser Kraft ist.

⭐ **Und die Tatsache, die Fables Unsicherheit auflöst** (*„ob ich den Satz
absichtlich gestrichen habe"*): Die Fassung vom 20.09. ist **nie** in einen
Registertext übernommen worden — gemessen, `grep` im Register: *„Horizontbeginn"*
**0 Treffer**, *„4a, Präzisierung"* **0 Treffer**. Es gab nichts zu streichen;
der Satz ist zwischen zwei Antworten verlorengegangen, nicht im Register.

### 28.7 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Das Feld `asof` ins `MANIFEST.json` schreiben.** 28.2 verlangt es, aber der Snapshot ist nach 17.1 *„nach seiner Erzeugung nicht mehr geschrieben"*. Ob das Manifest Teil dieses Schreibverbots ist, sagt kein Registertext. ⭐ *Fable hält in 21b fest, dass der Snapshot-Hash über den Dateien liegt und nicht über dem Manifest — eine Ergänzung änderte den Hash also nicht.* **Das ist eine Verfahrensfrage vor dem Tag und wird nicht nebenbei entschieden** | Verfahrensprüfer / Betreiber |
| ⛔ | **Das Feld `datenende` ins `MANIFEST.json`** — derselbe Grund | dito |
| ⛔ | **`registerdaten.py` anfassen** | — |
| ⛔ | **Den Faltenplan nach 4a ableiten.** Er hängt an einer offenen Frage an den Verfahrensprüfer (Status des gesperrten `faltenplan.json`, `FABLE_ANFRAGE_2026-09-21b`, Abschnitt C) | eigene Aufgabe, nach seiner Antwort |

---

## 29. Der Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte (TB-78, 21.09.2026)

⭐ **Neuer Registertext, keine Berichtigung** — gemessen: das Register regelt
den Beginn des Kapitalpfads bisher nicht (siehe 29.2).
⭐ **Bauart 24.3: die Regel steht vor der Messung.**

### 29.1 Der Befund — eine Lücke zwischen Horizontbeginn und erster Falte

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21c_uebergabe_und_vorlauf.md`,
Abschnitt 3.2.

Abschnitt 26 verbietet Einstiege **vor dem Horizontbeginn** (28.4: `2016-09-19`
für die vier Aktien-Bots). Die erste Selektionsfalte beginnt nach 4a am
**1. Januar**. Dazwischen liegen dreieinhalb bis fünfzehn Monate, in denen ein
Einstieg nach 26 **zulässig** ist, in **keiner Falte** auftaucht — und durch den
Kapitalpfad läuft.

⭐ **Fable, wörtlich:** *„Das ist genau der Schaden, mit dem (d) begründet wurde
(‚verändern das Kapital, mit dem die erste Falte beginnt'), nur kürzer."*

⚠️ **Dasselbe kann bei Krypto auftreten**, wo Bedingung (i) wegen des Vorlaufs
später liegt als der erste handelbare Tag — `rsi2_crypto`: 2018 handelbar, erste
Falte 2019.

⚠️⚠️ **Und die Wache aus 21b sieht es nicht**, weil sie gegen den Horizontbeginn
prüft. Deshalb ändert sich mit diesem Abschnitt auch die Wache (29.4).

### 29.2 Die Messung — das Register regelt es nicht

| gesucht | Treffer | was der Treffer sagt |
|---|---:|---|
| `Kapitalpfad` + Beginn/Start/1. Januar/erste Falte | **1** (Z. 4296) | beschreibt den **Schaden**: *„der Kapitalpfad (Registertext 1a) beginnt die erste Falte mit einem Kapitalstand, der aus nicht registrierten Jahren stammt"* |
| `Startkapital` | **0** | — |

⇒ **Der Text unten ist eine Neuaufnahme.** *Fable hatte das in 21c ausdrücklich
offengelassen: „Steht im Register bereits ein Satz, der den Beginn des
Kapitalpfads festlegt, legt ihn mir im Wortlaut vor — dann ist mein Vorschlag
gegenstandslos oder eine Berichtigung dazu, und das kann ich von hier nicht
sehen."*

### 29.3 Der Registertext, zeichengleich

> **Zu 4a / 26:** Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten Selektionsfalte mit dem registrierten Startkapital und ohne offene Position. Kein Einstieg liegt vor diesem Datum. Die Grösse der Wirkung ist für diese Regel ohne Belang.

**Quelle des Grundes:** 4a (Falten sind ganze Kalenderjahre) und der Grund von
26 (kein Trade ausserhalb aller Falten im Kapitalpfad). Kein Ergebnis.

⭐ **Der letzte Satz ist Absicht.** Er schliesst aus, dass die Regel später mit
dem Hinweis *„die Wirkung ist ja klein"* aufgeweicht wird — dieselbe Bauart wie
24.3.

### 29.4 Die Wache in TB-30b — geändert gegenüber 21b

⚠️ **Die Fassung aus 21b (Prüfung gegen den Horizontbeginn) ist ERSETZT.** Es
gilt:

> **Wache (TB-30b), angepasst:** frühester Einstieg ≥ **Beginn der ersten Selektionsfalte** (nicht nur ≥ Horizontbeginn). Der Bericht führt je Bot drei Daten nebeneinander: Horizontbeginn, Beginn der ersten Falte, frühester Einstieg.

⚠️ **Ort der Wache unverändert:** in den vier `multi_symbol_optimise.py`, **nicht**
in `auswertung.py` (eingefroren, Abschnitt 0 Z. 31; Fables Rücknahme in 21b).

> ⚠️ **Berichtigt (34.5, TB-82, 22.09.2026):** „in den vier `multi_symbol_optimise.py`"
> lies **„in allen neun"** — Fable 21l, Punkt 4 (b), zeichengleich: *„Die Wache
> „frühester Einstieg ≥ Beginn der ersten Selektionsfalte" wird in **allen neun**
> `multi_symbol_optimise.py` eingebaut, nicht nur in den vier Aktien-Optimierern."*
> Der Absatz oben bleibt zeichengleich; unverändert gilt: **nicht** in `auswertung.py`.
> Gemessen (TB-82, Beleg M4): heute in keinem der neun eine Wache — Ersteinbau, TB-30b.

### 29.5 Was noch zu messen ist — nur das Ob, nicht die Wirkung

| | zu messen | ⚠️ |
|---|---|---|
| 1 | Wo der Kapitalpfad der neun Optimierer **heute** beginnt | — |
| 2 | Ob es in den vorhandenen Trade-Listen Einstiege zwischen Horizontbeginn (bzw. erstem handelbarem Tag) und dem 1. Januar der ersten Falte **gibt** | ⛔ **Nur das Ob, nicht die Wirkung auf Kennzahlen** — eine Zahl über Kennzahlen fiele unter 27.1 |
| | | ⚠️ **Und jede Messung an den neun `paper_trading_*.db` läuft auf einer KOPIE** |

⛔ **Nicht Gegenstand dieser Aufgabe.** Eigene Aufgabe, nach TB-78.

---

## 30. Was der gesperrte Faltenplan ist — und was der Plan nach 4a ist (Fable 21i, 21.09.2026)

⭐ **Neuer Registertext.** Er trennt zwei Dinge, die bis heute denselben Namen
trugen: die **gesperrte Datei** `ergebnisse/faltenplan.json` und den
**Faltenplan nach 4a**. Dazu zwei Präzisierungen zu den Abschnitten 28 und 29,
die aus derselben Antwort stammen (30.6, 30.7).

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21i_gesperrter_faltenplan.md`,
zeichengleich. Anlass: die Messmeldung
`FABLE_ANFRAGE_2026-09-21b_messmeldung_vorlauf_und_kapitalpfad.md`, Abschnitt (C).

### 30.1 Der Befund — die gesperrte Datei stammt aus einem anderen Verfahrensstand

**Gemessen 21.09.2026 an
`research/vorregistrierung/ergebnisse/faltenplan.json` (`0e54ac5c…`):**

| | |
|---|---|
| ⚠️ | Die Datei führt je Falte ein Feld **`training_bis_ausschliesslich`** (Beispiel `2018-12-14`) und ein Feld **`embargo_tage: 18`**. ⭐⭐ **Verfahren B hat ausdrücklich KEIN Trainingsfenster** (V5c, Fable 15.09.2026) |
| ⚠️ | Erste Selektionsfalte `turtle_soup_stocks` im gesperrten Plan: **2019** — nicht 2017 oder 2018 |
| ⚠️ | TB-72 hat einen neuen Plan **daneben** gelegt (`ergebnisse/faltenplan_tb72.json`); der gesperrte ist unberührt, aber er ist **nicht** der Plan nach 4a |

⇒ **Die Frage, die Fable stellte, war an dieser Datei nicht beantwortbar.** Nach
`A2` ist *„konnte nicht messen"* ein eigenes Ergebnis, nicht grün und nicht rot.

### 30.2 Der Registertext, zeichengleich

> **Registertext (zu 26 / Sperrliste):**
> **(1)** `faltenplan.json` (0e54ac5c…) bleibt gesperrt und unverändert. Er ist der **registrierte historische Stand** eines früheren Verfahrensstands (Trainingsfenster, Embargo); er ist **nicht** der Faltenplan nach 4a und wird vom Lauf nicht gelesen. Sperrlistenpunkt 2 erhält eine Tatsachennotiz mit diesem Satz — kein Ersatz, keine Streichung.
> **(2)** Der Faltenplan nach 4a ist **Registertext**: je Bot die Liste der Selektionsfalten (Kalenderjahre), abgeleitet aus asof, `RECENT_YEARS_ONLY`, dem Indikator-Vorlauf gegen den Horizontbeginn und dem Trockenlauf nach 3b (b). Der Registertext ist die Quelle; jede Datei, die ihn maschinenlesbar wiedergibt, ist Abbild.
> > ⚠️ **Berichtigt (34.3, TB-82, 22.09.2026):** „Trockenlauf nach 3b (b)" lies **„3b (a)"** — Fable 21m, Frage 3, zeichengleich: *„Gemeint ist der Trockenlauf aus 3b (a), der die `MIN_HISTORY_*`-Tabelle aus 3b (b) anwendet; ein zweiter Trockenlauf existiert nicht."* Der Satz oben bleibt zeichengleich stehen; 16.7: 3b (a) ist der Trockenlauf-Satz, 3b (b) die `MIN_HISTORY_*`-Tabelle.
> **(3)** Genau **eine** solche Datei wird vor dem Tag mit Hash in die Sperrliste aufgenommen (neuer Punkt), und der Lauf liest genau diese. Ihr Inhalt muss dem Registertext aus (2) entsprechen; der Abgleich (Datei gegen Registertext, je Bot, je Jahr) ist eine Prüfung vor dem Tag und wird als Tatsachennotiz mit Ergebnis eingetragen. Trägt eine Datei Felder, die 4a nicht kennt (Trainingsgrenzen, Embargo), ist sie nicht dieses Abbild.
> > ⭐ **Präzisiert (35.4, TB-83, 22.09.2026):** „und der Lauf liest genau diese" — Fable 22a, zeichengleich: *„Der Lauf verwendet den Plan, den `faltenplan.py` zur Laufzeit bildet. Die Sonde vergleicht diesen Plan **vor dem Start des Laufs** mit dem Abbild (Feldmenge und Werte); bei Abweichung bricht der Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Das Abbild ist damit der registrierte Sollzustand, gegen den der gerechnete Plan geprüft wird — nicht die Datei, die `auswertung.py` öffnet."* Gemessen (Beleg M3): `auswertung.py` rechnet den Plan über genau einen Aufruf, `fp.faltenplan(mess)`, Z. 589. Der Satz oben bleibt zeichengleich; Sonde und Wrapper sind nicht geschrieben.
> **(4)** Ob `faltenplan_tb72.json` diese Datei ist, entscheidet allein der Abgleich nach (3) — nicht ihre Herkunft.

**Quelle des Grundes,** Fable wörtlich: *„Das Register ist append-only …
Ersetztes bleibt mit Marke stehen — das gilt für Dateien in der Sperrliste
genauso wie für Sätze. Und 4a definiert die Falten als Funktion registrierter
Konstanten plus Trockenlauf … ein Plan, der ein Trainingsfenster kennt, kann
diese Funktion nicht sein."* Kein Ergebnis; **welche Jahre herauskommen, spielt
für die Regel keine Rolle.**

⭐⭐ **Warum nicht „ersetzen und den alten von der Sperrliste nehmen",** wörtlich:

> *„Die Sperrliste beweist, dass nichts bewegt wurde. Einen Punkt zu entfernen, weil er obsolet ist, öffnet die Frage, wer ‚obsolet' entscheidet — und das ist genau die Stelle, an der später jemand einen unbequemen Punkt für obsolet erklären könnte. Ergänzen, markieren, stehen lassen."*

### 30.3 Die Tatsachennotiz zu Sperrlistenpunkt 2 — und warum sie dort steht

⭐ **Handwerksentscheidung, gemessen:** Die Sperrliste kennt die Form bereits.
**Punkt 8** trägt seit Abschnitt 15 eine eingerückte Notiz unter dem Punkt
(*„⚠️ Der Halbsatz ‚vier Jahre Vorlauf je Symbol' ist ersetzt (Abschnitt 15,
Registertext 3) …"*). **Kein neues Element** — Punkt 2 bekommt dieselbe Form.
*Fable hatte das offengelassen: „ob die Sperrliste heute schon eine Form für
‚Tatsachennotiz zu einem Punkt' kennt … Handwerk, eure Wahl."*

⚠️ **Es ist ein reiner Zusatz** — Abschnitt 10 verliert keine Zeile.

⚠️ **Folge der Einfügung, gemessen beim Eintragen (TB-78):** Die sieben
Notizzeilen unter Punkt 2 verschieben jede Zeilennummer unterhalb von Z. 818
um **+7**. Alle Zeilenangaben in den Abschnitten 26 bis 29 (etwa Z. 4296,
Z. 4307, Z. 3897) gelten für den Stand `83e3a85`; im aktuellen Stand liegen
sie sieben Zeilen tiefer. *Eine Zeilenangabe im Register trägt ab hier ihren
Commit-Stand mit.*

### 30.4 Fables Rückfrage nach der Herkunft der Faltenmenge — beantwortet: steht

Er fragt, **nur das Ob**, gegen welchen Plan die 64 Falten aus 24.6 und die
„sieben statt acht" für `t3_supertrend` aus 25 gezählt wurden — *„damit die
Zahlen dort nicht mit dem Plan nach 4a verwechselt werden"*.

| | steht dort schon? | Fundstelle |
|---|---|---|
| **24.6** | ✅ **ja, wörtlich** | Z. 3897 (Stand `83e3a85`): *„Falten aus `research/vorregistrierung/ergebnisse/faltenplan_tb72.json` (TB-72)"* |
| **25** | ✅ **ja, und stärker** | Abschnitt 25 ist der Abschnitt, der `faltenplan_tb72.json` **erzeugt** hat (25.4; *„der neue Plan, daneben; `faltenplan.json` (`0e54ac5c…`) unberührt"*) |

⇒ ⭐ **Seine Bedingung ist erfüllt** (*„Wenn sie schon dort steht, genügt
‚steht'"*). **Keine Nachtragszeile an 24.6 oder 25** — beide sind append-only
abgeschlossen.

⚠️ **Festgehalten, weil es die Verwechslung benennt:** Weder 24.6 noch 25 zählt
gegen den **gesperrten** Plan (`0e54ac5c…`); beide zählen gegen
`faltenplan_tb72.json`. ⛔ **Und keiner von beiden ist der Plan nach 4a** — der
existiert noch nicht.

### 30.5 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Den Faltenplan nach 4a ableiten und als Registertext eintragen** (30.2 (2)) | eigene Aufgabe, nächster Schritt vor dem Tag |
| ⛔ | **Eine Abbild-Datei auf die Sperrliste nehmen** (30.2 (3)) — setzt (2) voraus | dieselbe Aufgabe |
| ⛔ | **Den Abgleich `faltenplan_tb72.json` gegen den Registertext** — es gibt noch keinen Registertext, gegen den abzugleichen wäre. ⚠️ **Gemessen 21.09.2026 (TB-78, beim Eintragen):** die Datei trägt `training_bis_ausschliesslich` (77 Vorkommen) und `embargo_tage` (9 Vorkommen) — dieselben Felder wie der gesperrte Plan. *Der Nachtrag v2 hatte „trägt keine Trainingsfelder" angenommen; das ist an der Datei widerlegt und nicht übernommen.* Ob sie das Abbild ist, entscheidet nach 30.2 (4) allein der Abgleich; 30.2 (3) spricht in ihrer heutigen Form dagegen | dieselbe Aufgabe |
| ⛔ | **`faltenplan.json` anfassen** — byteweise `0e54ac5c…` | nie |

### 30.6 Präzisierung zu 28.6 — der Vorlauf-Satz ist ein Ersteintrag

⚠️ **28.6 trägt die Kategorie „Berichtigung (Registertext an Registertext)".
Sie ist präzisiert, und 28.6 bleibt zeichengleich stehen.**

**Fable, 21i Abschnitt 1 (A), wörtlich:**

> *„Eure Tatsache aus 26.2 löst meine Unsicherheit: Es gab im Register nichts zu streichen, der Satz ist zwischen zwei meiner Antworten verlorengegangen. Damit ist auch die Kategorie präziser als in 21c: kein Berichtigung *eines Registersatzes*, sondern **Ersteintrag** — der Satz kommt mit der 4a-Präzisierung erstmals in Registertext (26). Quelle des Grundes unverändert 4a/26; F17 ist erfüllt, die Kategorie ist Handwerk."*

⇒ **Gültig ist: Ersteintrag.** ⭐ **Die Einordnung folgt damit der Messung des
steuernden Chats** (*„Horizontbeginn" 0 Treffer, „4a, Präzisierung" 0 Treffer im
Register*) **und nicht der ersten Vermutung — auch nicht Fables eigener.**

⚠️ **Warum das mehr ist als ein Etikett:** Eine Berichtigung setzt einen Satz
voraus, der berichtigt wird. Gäbe es ihn, wäre er irgendwo in Kraft gewesen —
und dann müsste geprüft werden, was auf ihm ruht. **Es gab ihn nie.** *Die
Kategorie ist die Frage, ob etwas ersetzt wurde oder zum ersten Mal gilt.*

### 30.7 Ergänzung zu 29.2 — die Reihenfolge ist der Beleg, nicht die Zahl

**Fable, 21i Abschnitt 1 (B), wörtlich:**

> *„Die Zeile 4296 ist der Beleg, dass der Schaden im Register benannt war, bevor die Regel dagegen stand — das ist die richtige Reihenfolge, und sie soll so in der Tatsachennotiz zu 26 stehen."*

⭐⭐ **Damit ist Z. 4296 nicht bloss der einzige Treffer einer Suche, sondern
der Nachweis der Bauart 24.3:** *eine Regel, die vor der Messung steht, kann
durch die Messung nicht gewählt worden sein.* ⚠️ **Wäre es umgekehrt** — erst
die Wirkung gemessen, dann die Regel geschrieben —, **wäre 29.3 eine
nachträgliche Wahl**, gleich wie gut sie begründet wäre.

⚠️ **Und die Grenze, damit der Beleg nicht überdehnt wird:** Z. 4296 belegt,
dass der **Schaden** benannt war. Sie belegt **nicht**, dass jemand seine Grösse
kannte — die ist bis heute nicht gemessen (29.5) und soll es nach 27.1 vor dem
Tag auch nicht werden.

---

## 31. Berichtigung zu 28.2 — das Manifest bekommt kein Feld `asof` (Fable 21j, 21.09.2026)

⭐ **Berichtigung eines Registersatzes, der am selben Tag eingetragen wurde**,
plus eine Präzisierung zu 5a / 17.1 (Ersteintrag) und zwei Tatsachennotizen.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21j_manifest_asof.md`,
Abschnitt 2, zeichengleich. Anlass:
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21c_einarbeitung_21i_und_manifest.md`,
Punkt 5.

⚠️ **28.2 bleibt zeichengleich stehen.** Der Halbsatz, der ersetzt wird, ist
hier benannt.

### 31.1 Der Befund — der Wert steht im Manifest, unter einem anderen Namen

**Gemessen am `MANIFEST.json` des registrierten Snapshots
(`snapshots/63e4b6c8…/MANIFEST.json`):**

| | |
|---|---|
| Das Feld, das `asof` tragen sollte | existiert bereits als **`zeitpunkt_utc`** = `2026-09-19T06:49:32+00:00` |
| Ein Feld `asof` | **gibt es nicht** |

⇒ **Es fehlte kein Wert, nur ein zweiter Feldname für denselben Wert.**

### 31.2 Der Ersatztext zu 28.2, zeichengleich

> **Berichtigung zu 28.2 (Registertext 5a, Ergänzung), Ersatztext:**
> asof ist das UTC-Datum des Felds `zeitpunkt_utc` im `MANIFEST.json` des registrierten Snapshots. Es wird im Register als Tatsachennotiz neben dem Snapshot-Hash eingetragen. Ein neuer Snapshot (5c) setzt ein neues asof. **Das Manifest erhält kein Feld `asof`**; der Halbsatz „Es wird im `MANIFEST.json` als Feld `asof` geführt" ist ersetzt.

⚠️ **Der ersetzte Halbsatz steht in 28.2 und bleibt dort stehen**, mit dieser
Marke. **Der Wert von `asof` ändert sich nicht:** weiterhin **2026-09-19**.

### 31.3 Präzisierung zu 5a / 17.1 — Ersteintrag, zeichengleich

> **Präzisierung zu 5a / 17.1 (Ersteintrag):** „Wird nach seiner Erzeugung nicht mehr geschrieben" gilt für den Snapshot **einschliesslich seines Manifests**. Tatsachen über einen Snapshot, die nach seiner Erzeugung festgestellt werden — darunter `datenende` (grösstes `open_time` über alle Kursdateien des Snapshots) — stehen als Tatsachennotiz im Register, nicht im Snapshot. Ein Manifest darf `datenende` nur tragen, wenn es **bei der Erzeugung** geschrieben wird (5c, künftige Snapshots).

**Quelle des Grundes,** Fable wörtlich: *„17.1 im Wortlaut … und die Rolle des
Manifests als Träger, aus dem Abschnitt 18 seine Zahlen liest — ein Träger, der
nach der Registrierung noch beschrieben wird, kann nicht mehr bezeugen, was bei
der Registrierung galt, auch wenn der Hash ihn nicht deckt. Und der Grundsatz
ein Wert, ein Ort."* Kein Ergebnis.

**Seine Begründung gegen die drei vorgelegten Wege, wörtlich:**

> *„Warum nicht a: a lässt 28.2 stehen und liest es ‚für den nächsten Snapshot' — ein Registertext, der den Bestand nicht beschreibt, mit einer Lesart daneben. Das ist derselbe Zustand wie beim Vorlauf-Satz heute Vormittag, nur absichtlich. Warum nicht b: Der Preis ist genau der, den ihr nennt: ‚unverändert seit Erzeugung' gilt danach nicht mehr wörtlich, und ein Register, das wörtlich gelesen wird, verträgt keine folgenlosen Ausnahmen. Warum nicht c: zweiter Träger."*

### 31.4 Tatsachennotiz — seine Unsicherheit, gemessen

Fable markiert in 21j als unsicher, *„ob 17.1 den Begriff ‚Snapshot' an anderer
Stelle so verwendet, dass das Manifest ausdrücklich ausgenommen ist — dann wäre
meine Präzisierung eine Berichtigung dazu, und ihr seht das im Register, ich
nicht."*

**Gemessen 21.09.2026 im Register und am Dateisystem:**

| | Befund |
|---|---|
| 17.1 definiert den Snapshot als | **Ordner**: *„je Lauf einen eingefrorenen Snapshot (Tatsachennotiz: `snapshots/<hash>/`), der neben dem Bestand liegt und nach seiner Erzeugung nicht mehr geschrieben wird"* |
| Ort des Manifests | `snapshots/63e4b6c8…/MANIFEST.json` — **im Ordner** |
| Stelle, die es ausnimmt | **keine.** Alle Manifest-Erwähnungen im Register betreffen seine *Rolle* (führt Dateien mit Inhalts-Hash, trägt `datenstand_hash`, `teilkerzen`, zugelassene Befunde), nicht seine Unantastbarkeit |
| ⭐ **Die einzige Ausnahme, und sie ist eine andere Frage** | Der **Snapshot-Hash** deckt das Manifest nicht (17.1: *„der Hash der … (Pfad, Inhalts-Hash)-Paare **der Dateien** — nicht des Manifests"*) |

⇒ ⭐⭐ **Seine Präzisierung ist ein Ersteintrag, keine Berichtigung — und der
Wortlaut von 17.1 stützt sie.** ⚠️ *„Gehört zum Snapshot-Ordner" und „wird vom
Snapshot-Hash gedeckt" sind **zwei Fragen**, nicht eine (`C7`). Das Manifest
gehört dazu und wird nicht gedeckt; genau deshalb wäre eine Ergänzung folgenlos
für den Hash — und genau deshalb ist sie trotzdem ausgeschlossen.*

### 31.5 Tatsachennotiz — `datenende` des registrierten Snapshots

| | Wert | Herkunft |
|---|---|---|
| **`datenende`** | **2026-09-15** — grösstes `open_time` über alle **223** Kursdateien in `snapshots/63e4b6c8…/` (letzte Kerze `2026-09-15 08:00:00`, in 24 Krypto-1h-Dateien) | Mac-Lauf, `trading-env/bin/python3` (Python 3.9.6, macOS 15.7.9), Mac-Sitzung TB-79, 21.09.2026; zwei Zählungen (`csv`-Modul und pandas 2.3.3) gleich — `docs/belege/TB-78/schritt3c_messung_31_5_31_6.txt` |
| **`asof`** | **2026-09-19** | `zeitpunkt_utc` im Manifest, Abschnitt 18 |
| Abstand | **4 Tage** (2026-09-19 − 2026-09-15) | — |

⭐ **Messnotiz der Mac-Sitzung (TB-79), nicht Teil des Nachtrags:** Die 223
Kursdateien enden nicht am selben Tag — die **150 Aktien-Tagesdateien** enden
am **2026-09-01**, die 24 Krypto-Tagesdateien am 2026-09-14, die 48
Krypto-4h- und -1h-Dateien am 2026-09-15 (Ausnahme `XAUTUSDT_1h.csv`:
2026-08-30). `datenende` ist das Maximum über alle Dateien; das Datenende der
vier Aktien-Bots liegt **18 Tage** vor `asof`. Eine Kalenderaussage, keine
Ergebnisaussage.

### 31.6 ⚠️ Berichtigung einer Zahl aus Abschnitt 26 — 15 Schlüssel sind 16

**Abschnitt 26 (TB-77) sagt:** *„es steht nirgends als Wert — gemessen
21.09.2026 in allen `.py` …, im **Snapshot-Manifest (15 Schlüssel, keiner
`asof`)**, in `registerdaten.py` und in `docs/`"*.

**Nachgemessen 21.09.2026 am selben Manifest:** **16 Schlüssel.**

```
bytes_gesamt · dateien · dateien_gesamt · datenstand_hash · eingabeliste ·
kursdateien · quelle · snapshot_hash · teilkerzen · verfahren · werkzeug ·
wurzel · zeitpunkt_utc · zugelassene_befunde · zugelassene_befunde_anzahl ·
zugelassene_befunde_herkunft
```

⭐ **Eigene Nachmessung der Mac-Sitzung (TB-79), Zählweise genannt:** gezählt
sind die Schlüssel der **obersten Ebene** des JSON-Objekts, `dateien` (die
Dateiliste mit 225 Einträgen) **mitgezählt** — **16**; ohne `dateien` **15**.
Zwei Zählungen (`json.load`, Textmuster auf Einrückung 2) gleich; `asof` kommt
weder als Schlüssel noch sonst im Text vor. `trading-env/bin/python3`
(Python 3.9.6), 21.09.2026.

| | |
|---|---|
| ✅ **Die Aussage trifft** | **keiner** der Schlüssel heisst `asof` — der Befund von TB-77 steht |
| ⚠️ **Die Zahl trifft nicht** | 16, nicht 15 |
| ⭐ **Mutmassliche Ursache, nicht gemessen** | `dateien` ist die Dateiliste, die übrigen 15 sind Metadaten. Wer die Liste nicht mitzählt, kommt auf 15 — **aber die Zählweise steht nicht dabei** |

⭐⭐ **Fehlerklasse `K4d`: eine Kennzahl, die ihre Bezugsmenge nicht nennt.**
*Die Zahl war womöglich richtig gerechnet — über eine Menge, die niemand
benennt. Eine Kennzahl nennt die Menge, über die sie läuft.*

⚠️ **Abschnitt 26 bleibt zeichengleich stehen**; die Zahl gilt als berichtigt
durch diesen Unterabschnitt.

### 31.7 Was hier ausdrücklich NICHT getan wird

| | | |
|---|---|---|
| ⛔ | **Das Manifest anfassen** — weder `asof` noch `datenende` | 31.2, 31.3 |
| ⛔ | **Ein Beiblatt neben dem Manifest anlegen** (Weg c der Vorlage) — zweiter Träger | Fable 21j |
| ⛔ | **28.2 oder Abschnitt 26 umschreiben** — append-only | — |
| ⛔ | **Den Snapshot neu ziehen** | — |
| ⭐ | **Was entfällt:** die Manifest-Ergänzung, die in 28.7 als *„nicht getan"* geführt war, ist jetzt *„nicht zu tun"* | Fable 21j |

---

## 32. Bedingung (i) rechnet gegen den Horizontbeginn aus 28.4 — Umstellung des Faltenplans von der Datenuhr auf das absolute Datum (TB-80, 21.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben.**
Kein neuer Registertext: 25.3 (Konjunktion), 26.2 (Horizont als absolutes
Datum je Bot) und 28.4 (die vier Daten) bleiben zeichengleich stehen und
werden hier **umgesetzt**, nicht geändert. Was dieser Abschnitt trägt, sind
ein Befund, drei Tatsachennotizen und eine Entscheidungsvorlage.

**Anlass:** `docs/auftraege/MAC_TB-80_bedingung_i_auf_asof.md`. Betreiberfreigabe
vom 21.09.2026, 21:47 Ortszeit, für **genau eine** Datei:
`research/vorregistrierung/faltenplan.py`. Ergebnis
`docs/ERGEBNIS_TB-80_bedingung_i_auf_asof.md`, Belege `docs/belege/TB-80/`.

⭐⭐ **Die Regel stand vor der Messung.** Gemessen an der Git-Historie:
Abschnitt 26.2 ist mit Commit `729443c` am 21.09.2026, **17:13** Ortszeit
eingetragen worden (der Auftrag nennt 19:19; der Commit liegt früher), 28.4
mit Commit `003f894` um **19:20** Ortszeit; die Messung in 32.2 lief am
21.09.2026 ab 20:17 UTC (**22:17** Ortszeit). **Was herauskommt, ist keine
Wahl** — Bauart 24.3.

---

### 32.1 Der Befund — Bedingung (i) rechnete gegen die Datenuhr, 26.2 verlangt das absolute Datum

**Gemessen 21.09.2026 am Stand `41db199` (vor Schritt 1), Fundstellen:**

| | Fundstelle | Wortlaut / Wert |
|---|---|---|
| Was das Register verlangt | **26.2**, Z. 4323–4329 (Registertext 4a, Präzisierung) | *„Der Datenhorizont eines Bots ist ein absolutes Datum je Bot: Horizontbeginn = `asof` (5a) minus `RECENT_YEARS_ONLY` des Bots; Bots ohne diese Konstante haben keinen Horizont (Krypto). […] Es gilt für alle Symbole des Bots gleich"* |
| Der Wert | **28.4**, Z. 4684–4687 (gültige Fassung der Tatsachennotiz zu 4d) | `elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`: **2016-09-19**; die fünf Krypto-Bots: **kein Horizont** (Z. 4679–4683) |
| Woher der Wert kommt | **28.3** | `asof` = **2026-09-19** (`zeitpunkt_utc` des Snapshots `63e4b6c8…`, Abschnitt 18) |
| Was der Code tat | `research/vorregistrierung/faltenplan.py::erste_falte_4a`, Z. 175 (Stand `41db199`) | `beginn = fn.symbolbeginn(bot, fn.fensteranker(eig["markt"]))` |
| Was `fensteranker` ist | `research/faltenplan_neun/faltenplan_neun.py:271–295` | zehn Jahre vor dem **spätesten letzten Kurstag des Marktes** — die **Datenuhr**; gemessen am 21.09.2026: `aktien` **2016-09-01**, `krypto` `None` (`docs/belege/TB-80/schritt0_ausgangsstand.txt`) |
| Der Abstand | — | **18 Tage** (2016-09-01 → 2016-09-19). 28.4, „Abgegrenzt": *„Die Ähnlichkeit der beiden Daten (2016-09-01 gegen 2016-09-19) ist Zufall des Kalenders"* |

**Was geändert wurde (Commit `76c20ec`, Diff vollständig im Ergebnisdokument):**
`erste_falte_4a()` nimmt den Anker aus `HORIZONTBEGINN = {"aktien":
date(2016, 9, 19), "krypto": None}` — ein **benanntes Literal je Markt mit der
Registerfundstelle (26.2 / 28.4) im Kommentar**, wie der Auftrag es vorgibt:
**nicht** `asof` minus Konstante gerechnet, **nicht** aus den vier
`multi_symbol_optimise.py` gelesen (Sperrliste; `T56b.6`, keine
Konstantenkopie). Neu daneben `horizontbeginn(bot)` und
`erste_falte_4a_messung(bot)`; der Plan trägt je Bot die zwei neuen Felder
`horizontbeginn` und `erste_falte_4a_warm_ab` (das früheste Warm-Datum, auf
Tagesebene — damit im Plan steht, gegen welches Datum (i) gerechnet wurde).
**Unverändert:** Bedingung (ii) (`erste_falte_trockenlauf.erste_falte_nach_3b`),
die Konjunktion in `erste_falte()` (25.3), die Signaturen von `erste_falte_4a`
und `erste_falte`. **`fensteranker` bleibt bestehen** — gemessen, wer ihn
sonst benutzt: `faltenplan_neun.py::plan_fuer_bot` (Z. 415, 445),
`embargo_neun.py:176`, `faltenschranke_messung.py:220, 236`.

---

### 32.2 Tatsachennotiz — die Wirkung je Bot

**Gemessen 21.09.2026, `trading-env/bin/python3` (Python 3.9.6), vorher am
Stand `41db199` (`docs/belege/TB-80/schritt0_ausgangsstand.txt`,
`schritt0_warm_ab.txt`), nachher am Stand `76c20ec`
(`docs/belege/TB-80/schritt2_wirkung.txt`). Beides aus dem Code gerechnet,
nicht aus einer Datei gelesen.**

| Bot | Markt | `erste_falte_4a` vorher | nachher | `erste_falte` vorher | nachher | Zahl der Selektionsfalten vorher → nachher |
|---|---|---:|---:|---:|---:|---|
| `elliott_wave` | krypto | 2018 | 2018 | 2018 | 2018 | 4 → 4 |
| `t3_supertrend` | krypto | 2018 | 2018 | 2019 | 2019 | 7 → 7 |
| `rsi2_crypto` | krypto | 2019 | 2019 | 2019 | 2019 | 7 → 7 |
| `turtle_soup_crypto` | krypto | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `volatility_breakout_crypto` | krypto | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `elliott_wave_stocks` | aktien | 2017 | 2017 | 2017 | 2017 | 9 → 9 |
| `rsi2_mean_reversion` | aktien | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `turtle_soup_stocks` | aktien | 2017 | 2017 | 2017 | 2017 | 9 → 9 |
| `volatility_breakout` | aktien | 2018 | 2018 | 2018 | 2018 | 8 → 8 |

**Bots mit Änderung an `erste_falte_4a`, `erste_falte` oder Selektionsfalten:
0. Geänderte, neue oder entfallene Falten (Grenzen, Rolle, Training, Embargo):
0.** Die neun Zahlen stimmen mit 21.4 überein.

**Dieselbe Messung eine Ebene tiefer** — das früheste Datum, an dem ein Symbol
des Bots ab dem Anker warm ist (die Grösse hinter `erste_falte_4a`):

| Bot | Anker vorher (Datenuhr) | Horizontbeginn nachher | warm ab vorher | warm ab nachher | Verschiebung |
|---|---|---|---|---|---:|
| fünf Krypto-Bots | `None` | `None` | 2017-08-17 / 2017-08-17 / 2018-01-14 / 2017-09-16 / 2017-12-22 | unverändert | **+0 Tage** |
| `elliott_wave_stocks` | 2016-09-01 | 2016-09-19 | 2016-09-01 | 2016-09-19 | +18 Tage |
| `rsi2_mean_reversion` | 2016-09-01 | 2016-09-19 | 2017-06-20 | 2017-07-06 | +16 Tage |
| `turtle_soup_stocks` | 2016-09-01 | 2016-09-19 | 2016-10-14 | 2016-10-31 | +17 Tage |
| `volatility_breakout` | 2016-09-01 | 2016-09-19 | 2017-03-07 | 2017-03-22 | +15 Tage |

⭐ **Die fünf Krypto-Bots haben keinen Horizont (26.2), und bei ihnen ändert
sich nichts** — weder ein Jahr noch ein Tag. Das ist der Nachweis, dass die
Umstellung nur (i) trifft (Abbruchkriterium 4 des Auftrags, nicht
eingetreten). Ihre Einträge im neuen Plan unterscheiden sich vom
Ausgangsstand ausschliesslich im Text `erste_falte_quelle` und in den zwei
neuen Feldern.

⛔ **Nicht gemessen und nicht zu messen:** wie sich die Umstellung auf eine
Kennzahl eines Parametersatzes auswirkt (27.1, vor dem Tag).

---

### 32.3 Tatsachennotiz — der neue Plan daneben, die gesperrten Dateien unverändert

| Datei | SHA-256 | Stand |
|---|---|---|
| **`research/vorregistrierung/ergebnisse/faltenplan_tb80.json`** (neu, Commit `cadb968`) | **`2dd28291497e1233f6854651688f77d5d0a268370ef1ce423a42820917316794`** | Plan nach der Umstellung; zwei Läufe byteweise gleich; geschrieben vom Belegskript `docs/belege/TB-80/schritt2_faltenplan_tb80.py`, **nicht** von `faltenplan.py::main` (das schreibt immer nach `faltenplan.json`) |
| `research/vorregistrierung/ergebnisse/faltenplan.json` (Sperrliste Punkt 2) | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` | **byteweise unverändert**, vorher und nachher gemessen |
| `research/vorregistrierung/ergebnisse/faltenplan_tb72.json` | `19e8cbca874d6e7455f2f3bc0723def9ea058d0b314fa1772e04cd64ff1c9d24` | **byteweise unverändert**; der Speicherstand vor TB-80 (`docs/belege/TB-80/faltenplan_stand_vor_tb80.json`, aus dem Code gerechnet) hat **denselben Hash** — der Plan von TB-72 war am Ausgang reproduzierbar |
| `research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` (Sperrliste) | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` | unverändert |
| `research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json` (Sperrliste) | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` | unverändert |

⚠️ **`faltenplan_tb80.json` ist kein Sperrlistenpunkt und kein Registertext.**
Was der Plan nach 4a ist und wie er ins Register kommt, regelt Abschnitt 30
(genau eine Abbild-Datei, als neuer Sperrlistenpunkt, Betreiber). Diese Datei
liegt daneben, wie `faltenplan_tb72.json` daneben liegt.

---

### 32.4 Die Mutationsprobe — in beide Richtungen

**`docs/belege/TB-80/schritt3_mutationsprobe.py` / `.txt`, 21.09.2026, 20:25 UTC,
im Speicher (`HORIZONTBEGINN` ersetzt, `faltenplan.py` unverändert, nichts
committet), 49/49 Proben, `rc 0`.**

| Richtung | Eingriff | Ergebnis |
|---|---|---|
| **1 — die Datenuhr wieder eingesetzt** | `HORIZONTBEGINN = {markt: fn.fensteranker(markt)}` = `aktien 2016-09-01`, `krypto None` | Der Plan liefert **Bot für Bot den alten Stand** aus Schritt 0: `erste_falte_4a`, `erste_falte`, Selektionsfalten, alle Falten (Grenzen/Rolle/Training/Embargo) **und** die Warm-Daten auf Tagesebene (9 × 3 Proben). Gegen den neuen Plan weichen **alle vier Aktien-Bots** in `horizontbeginn` und `erste_falte_4a_warm_ab` ab; die fünf Krypto-Bots sind zeichengleich |
| ⚠️ **Wo Richtung 1 nicht beisst** | — | **Auf Jahresebene sind alter und neuer Stand gleich** (32.2: 0 Bots mit Änderung). Dort kann diese Richtung nichts verwerfen. **Sie beisst auf Tagesebene** — deshalb trägt der Plan seit TB-80 das Warm-Datum, und deshalb wurde es in Schritt 0 vor der Änderung gemessen |
| **2 — der Horizontbeginn ein Jahr nach hinten** | `aktien 2017-09-19` | **Alle vier Aktien-Bots bewegen sich um ein Jahr**: `erste_falte_4a` und `erste_falte` `elliott_wave_stocks` 2017 → 2018, `rsi2_mean_reversion` 2018 → 2019, `turtle_soup_stocks` 2017 → 2018, `volatility_breakout` 2018 → 2019; die Konjunktion hält (`erste_falte ≥ erste_falte_4a`, `H` in der ersten Kandidatenfalte 136/137); Krypto unverändert |
| Original wiederhergestellt | `{"aktien": 2016-09-19, "krypto": None}` | `erste_falte_4a_messung` je Bot = `faltenplan_tb80.json` (9/9) |

**Der Test** `research/faltenplan_neun/test_horizontbeginn.py` (Commit
`cb7f495`, 61/61 auf `trading-env/bin/python3` 3.9.6) prüft dauerhaft: die vier Aktien-Bots gegen 2016-09-19 und nicht
gegen die Datenuhr; die fünf Krypto-Bots gegen den Ausgangsstand aus Schritt 0;
die Konjunktion; und **das Literal gegen den Registertext 28.4** — der Test
liest die Tabelle in 28.4 und vergleicht sie mit `faltenplan.horizontbeginn(bot)`.
Gegenprobe: mit dem Literal auf 2016-09-01 wird er rot (15 Prüfungen,
`docs/belege/TB-80/schritt4_gegenprobe_test_rot.txt`).

---

### 32.5 ⭐ Entscheidungsvorlage, nicht vollzogen — wo der Horizontbeginn dauerhaft leben soll

**Heute (Zwischenstand, so benannt):** ein Literal je Markt in
`research/vorregistrierung/faltenplan.py` (`HORIZONTBEGINN`), mit der
Registerfundstelle im Kommentar und einem Test, der es gegen den Registertext
28.4 hält. Register 26.6 (letzte Zeile, „Entscheidungsvorlage, nicht
vollzogen") und 28.7 führen die Frage *„`RECENT_YEARS_ONLY` als registrierte
Grösse"* seit TB-77 offen; sie ist mit dieser Aufgabe nicht entschieden.

| Möglichkeit | Was es ist | Preis |
|---|---|---|
| **(a) `registerdaten.py` als registrierte Grösse** | `HORIZONTBEGINN` (oder `asof` und `RECENT_YEARS_ONLY` getrennt, mit dem Datum als Ableitung) wandert in das Modul, das *„die einzige Quelle für alles, was die Vorregistrierung festschreibt"* ist; `faltenplan.py` importiert es wie `GO_LIVE_SCHNITT` | Eine **Registeränderung** — `registerdaten.py` ist Träger der Festlegungen, die Änderung braucht den Betreiber (26.6). Und es entsteht die Frage, ob dort das Datum steht (eine Zahl, wie 28.4) oder die Formel (zwei Zahlen, eine davon aus den gesperrten Bot-Dateien — `T56b.6`) |
| **(b) aus dem Registertext gelesen** | Der Faltenplan liest die Tabelle in 28.4 zur Laufzeit, so wie der Test es heute tut | **Ein Parser auf Fliesstext** im Rechenpfad: das Register ist append-only, eine spätere Berichtigung stünde in einem neuen Abschnitt, und der Parser müsste wissen, welche Tabelle gilt. Was heute eine Prüfung ist, würde eine Abhängigkeit |
| **(c) Literal mit Test gegen das Register** | der heutige Stand | Die Zahl steht **zweimal** (Register, Code); der Test hält beide zusammen, solange er läuft. Läuft er nicht, ist es eine Konstante, die niemand gegenprüft |

⛔ **Keine Empfehlung nach Aufwand.** Die Vorlage nennt die drei Wege mit ihrem
Preis; die Wahl liegt beim Betreiber, gegebenenfalls nach Rückfrage beim
Verfahrensprüfer.

---

### 32.6 Was ausdrücklich NICHT getan wurde

| | |
|---|---|
| ⛔ | **Kein Bot-Code** — `strategies/`, `shared/` unberührt; die vier `multi_symbol_optimise.py` (TB-30b) unverändert |
| ⛔ | **Keine Sperrlisten-Datei** — `faltenplan.json`, `benchmark_drawdowns.json`, `benchmark_drawdowns_vt.json` byteweise unverändert (32.3); `faltenplan_tb72.json` unverändert; `auswertung.py` unberührt (auch nicht der Docstring) |
| ⛔ | **Kein `registerdaten.py`** — die Vorlage 32.5 ist nicht vollzogen |
| ⛔ | **Kein Tag, kein Lauf** — kein Selektionslauf, kein Parametersatz bewertet, keine Kennzahl gemessen (27.1) |
| ⛔ | **`fensteranker` nicht entfernt** — drei andere Aufrufer (32.1); ob er dort noch die richtige Grösse ist, ist eine andere Aufgabe |
| ⛔ | **Der Plan nach 4a nicht ins Register** — `faltenplan_tb80.json` liegt daneben; die Abbild-Datei nach Abschnitt 30 ist eine eigene, freizugebende Aufgabe |

---

### In einfacher Sprache

**Was schiefstand:** Das Regelwerk sagt seit dem Abend des 21.09., ab welchem
Tag jeder Aktien-Bot rechnen darf — dem 19. September 2016. Das Programm, das
die Auswertungsjahre bestimmt, nahm dafür noch ein anderes Datum: den letzten
Tag, für den Kursdaten vorliegen, zehn Jahre zurück, also den 1. September
2016. Achtzehn Tage Unterschied.

**Was gemacht wurde:** Das Datum aus dem Regelwerk steht jetzt im Programm,
mit Verweis auf die Stelle, aus der es kommt. Es wird nicht ausgerechnet und
nicht aus den Bot-Programmen abgeschrieben, sondern so genommen, wie das
Regelwerk es nennt. Ein Test liest die Tabelle im Regelwerk und prüft, dass
beide übereinstimmen.

**Was sich dadurch ändert:** Bei den Jahren — nichts. Alle neun Bots beginnen
in denselben Jahren wie vorher, mit denselben Auswertungsjahren. Achtzehn Tage
weniger Vorlauf haben bei keinem Bot gereicht, um ein Jahr zu verlieren. Auf
Tagesebene sieht man die Verschiebung: der Tag, an dem das erste Wertpapier
eines Aktien-Bots bereit ist, liegt jetzt 15 bis 18 Tage später. Bei den fünf
Krypto-Bots, die kein solches Fenster haben, ändert sich nicht einmal ein Tag.

**Warum das eine Zahl ist und keine Wahl:** Die Regel stand im Regelwerk,
bevor gemessen wurde, was sie kostet. Dass sie nichts kostet, ist ein
Ergebnis — es hätte auch anders ausgehen können, und dann hätte es genauso
dagestanden.

**Was noch offen ist:** Wo das Datum dauerhaft hingehört — in das Modul, das
alle Festlegungen trägt, oder als Literal mit Test. Das ist eine Entscheidung
des Betreibers; hier stehen die Wege mit ihrem Preis, ohne Empfehlung.

*Nachgetragen in TB-80, 21.09.2026. Umsetzung mit Befund, Tatsachennotizen,
Mutationsprobe und Entscheidungsvorlage: sie nennt, was der Code tat, was das
Register verlangt, was sich dadurch ändert (nichts an den Jahren, 15 bis 18
Tage darunter), was gesperrt bleibt und was offen ist — und entfernt nichts.*

---

## 33. Der Faltenplan als Registertext, und was die Abbild-Datei tragen muss (Fable 21k, 21.09.2026)

⭐ **Zwei Dinge in einem Abschnitt:** der Faltenplan nach 4a als Registertext
(Fables 30.2 (2)) und die **Berichtigung** seines Kriteriums aus 30.2 (3), das
er selbst zurückgenommen hat.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21k_abbild_schema.md`,
zeichengleich. Anlass: `FABLE_ANFRAGE_2026-09-21e_abbilddatei_felder.md`.

### 33.1 Berichtigung zu 30.2 (3) — ein Symptom war zum Kriterium geworden

⚠️ **Der Satz in 30.2 (3)** — *„Trägt eine Datei Felder, die 4a nicht kennt
(Trainingsgrenzen, Embargo), ist sie nicht dieses Abbild"* — **ist ERSETZT.**
Er bleibt dort zeichengleich stehen.

**Der Anlass, gemessen 21.09.2026:** Alle drei vorhandenen Pläne tragen
`training_bis_ausschliesslich` (60 verschiedene Werte) und `embargo_nach_falten`
(29 verschiedene) — der gesperrte `faltenplan.json`, `faltenplan_tb72.json`
**und** der am selben Abend erzeugte `faltenplan_tb80.json`. ⭐ **Und: kein
Laufcode liest sie** — `training_bis_ausschliesslich` hat genau einen Treffer im
Repo, `faltenplan.py:306`, und das ist die Stelle, die es **schreibt**.

⭐⭐ **Fables Grund, warum „die Felder wirken ja nicht" trotzdem kein Kriterium
ist — wörtlich:**

> *„Das ist eine Aussage über Code, der **noch nicht eingefroren ist** (TB-30b
> steht aus). Ein Registertext, der davon abhängt, was der Code heute nicht
> liest, wandert mit dem Code — dieselbe Klasse wie die Datenuhr. Und: Ein
> Abbild ist nicht nur für den Lauf da, sondern für jeden, der später nachliest,
> was der Plan war. Sechzig verschiedene Trainingsgrenzen in einer Datei
> beschreiben ein Verfahren mit Trainingsfenster. Dass niemand sie liest, sieht
> man der Datei nicht an."*

### 33.2 Der Registertext — der Faltenplan nach 4a

> **Registertext (30.2 (2)), Faltenplan.** Der Faltenplan ist Registertext. Je
> Bot gelten: der Horizontbeginn (absolutes Datum oder ausdrücklich „kein
> Horizont"), die Faltenlänge in Jahren, die erste Selektionsfalte und die
> vollständige Liste der Selektionsfalten. Die Falten sind zusammenhängende
> Kalenderjahre in Schritten der Faltenlänge, aufsteigend und lückenlos vom
> Beginn der ersten Falte bis zum Go-Live-Schnitt. Eine Datei, die diesen Text
> maschinenlesbar wiedergibt, ist sein **Abbild** (33.3); der Registertext ist
> die Quelle.

> ⭐ **Ergänzt (34.1 und 34.2, TB-82, 22.09.2026):** Zwei Sätze von Fable (21m,
> Frage 1) schliessen diesen Registertext, Wortlaut in 34: **34.1** — bei
> Faltenlänge L > 1 werden (i) und (ii) am **ersten Jahr** der Falte geprüft, die
> Falte umfasst J bis J + L − 1, die folgenden schliessen lückenlos an; **34.2** —
> ein Rest von weniger als L Kalenderjahren zwischen der letzten vollen Falte und
> dem Go-Live-Schnitt ist **keine** Selektionsfalte. Der Text oben bleibt
> zeichengleich; die Tabelle unten ändert sich um nichts (Beleg M5).

> ⭐ **Ergänzt (35.1, TB-83, 22.09.2026):** Fable 22a fügt diesem Registertext die
> **Bestätigungsperiode** hinzu, Wortlaut in 35.1: die Datumsspanne von „Bestätigung
> ab" (21.4) bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich; keine Falte im Sinn
> von 4a, (1b)/34.2 betrifft sie nicht. Ihr **Bezeichner** in Plan, Abbild,
> `zellen.csv` und Berichten ist die Spanne selbst, `JJJJ-MM-TT/JJJJ-MM-TT` — für
> alle neun Bots `2026-01-01/2026-09-01` (gemessen, Beleg M1/M2). Der heutige
> Faltenname in `faltenplan.py:336` ist danach unzulässig; die Umstellung ist nicht
> Teil von TB-83. Text und Tabelle oben bleiben zeichengleich (Beleg M5).

**Tatsachennotiz — der Plan, gemessen am 21.09.2026 (TB-81, HEAD `a0c6eb0`) aus
`research/vorregistrierung/ergebnisse/faltenplan_tb80.json` (Commit `cadb968`,
SHA-256 `2dd28291497e1233f6854651688f77d5d0a268370ef1ce423a42820917316794`;
Messung `docs/belege/TB-81/schritt1_faltenlisten.txt`, zwei unabhängige
Zählungen — aus `selektionsfalten` und aus `falten` mit `rolle == "selektion"` —
mit 0 Abweichungen, gegen 21.4 0 Abweichungen):**

| Bot | Markt | Horizontbeginn | Faltenlänge | erste Falte | Selektionsfalten | # |
|---|---|---|---:|---:|---|---:|
| `elliott_wave` | krypto | kein Horizont | 2 J | 2018–2019 | 2018–2019 · 2020–2021 · 2022–2023 · 2024–2025 | 4 |
| `t3_supertrend` | krypto | kein Horizont | 1 J | 2019 | 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 7 |
| `rsi2_crypto` | krypto | kein Horizont | 1 J | 2019 | 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 7 |
| `turtle_soup_crypto` | krypto | kein Horizont | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |
| `volatility_breakout_crypto` | krypto | kein Horizont | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |
| `elliott_wave_stocks` | aktien | 2016-09-19 | 1 J | 2017 | 2017 · 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 9 |
| `rsi2_mean_reversion` | aktien | 2016-09-19 | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |
| `turtle_soup_stocks` | aktien | 2016-09-19 | 1 J | 2017 | 2017 · 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 9 |
| `volatility_breakout` | aktien | 2016-09-19 | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |

*Lesehilfe zur Tabelle:* „kein Horizont" steht in der gemessenen Datei als
JSON-`null` unter dem Schlüssel `horizontbeginn` (Schlüssel gesetzt, Wert
null); der Go-Live-Schnitt ist bei allen neun Bots `2026-09-01`
(ausschliesslich, 5.2). Bei `t3_supertrend` trägt die Datei daneben
`erste_falte_4a = 2018`: Bedingung (i) allein ergäbe 2018, die Konjunktion mit
dem Trockenlauf (25.3) hebt die erste Selektionsfalte auf 2019 — der in 21.4
beschriebene Fall.

⚠️ **Zur Herkunft:** Die Werte ruhen auf `asof` = 2026-09-19 (28.3), dem
Horizontbeginn je Bot (28.4), dem Vorlauf gegen den Horizontbeginn (28.6), der
Konjunktion aus 25.3 und dem Trockenlauf nach 3b (b). ⭐ **Abschnitt 32 hat
gemessen, dass die Umstellung von der Datenuhr auf `asof` keine einzige Falte
bewegt** — die Liste ist also dieselbe wie vor der Umstellung, und das ist
belegt, nicht angenommen.

*Zitierhinweis (TB-81, gemessen):* „Trockenlauf nach 3b (b)" übernimmt den
Wortlaut aus 30.2 (2). In 16.7 ist **3b (a)** der Satz zum Trockenlauf („ein
Symbol an mindestens einem Handelstag handelbar"), **3b (b)** die
`MIN_HISTORY_*`-Tabelle, die der Trockenlauf anwendet; 21.3 (a), 21.4 und
`erste_falte_quelle` in der Datei zitieren den Trockenlauf als 3b (a). Gemeint
ist an beiden Stellen derselbe Trockenlauf; der Wortlaut von 30.2 (2) wird hier
nicht geändert (append-only), der Hinweis steht, damit niemand nach einem
zweiten Trockenlauf sucht.
⭐ *Nachtrag (TB-82, 22.09.2026):* Die ausdrückliche Berichtigung — „3b (b)" lies
„3b (a)" — steht jetzt als eigener Registersatz in **34.3** (Fable 21m, Frage 3);
die Marke am Satz selbst steht unter 30.2 (2).

> ⭐⭐ **Die Benchmark-Tabelle folgt diesem Plan (39.2/39.4, Fable 23a, TB-94,
> 23.09.2026):** Registertext zu Sperrlistenpunkt 4 / 23 / 33 (23a, Wortlaut in
> **39.2**): Die Tabelle, die der Lauf liest, hat je Bot genau die
> Selektionsfalten dieses Registertexts (plus Bestätigungsperiode) — nicht
> mehr, nicht weniger. Gemessen an der vollzogenen Tabelle gegen den Plan aus
> `faltenplan.py` (`7aa0b8cc…`) im Speicher (TB-91 Block D): **18/18 gleich**,
> Bestätigungszeile 9/9 `2026-01-01/2026-09-01`. Text und Tabelle oben bleiben
> zeichengleich.

> ⭐⭐ **Die Faltenlänge wird neu abgeleitet und gegen diesen Text verglichen
> (40.6, Fable 24a, TB-96, 24.09.2026):** Die Faltenlänge je Bot oben ruht auf
> den neun TB-24-Listen (`78e2bc6`), die nicht auf dem registrierten Snapshot
> erzeugt sind. Sie werden neu erzeugt (TB-98), die Faltenlänge wird nach 5.4
> abgeleitet und **gegen diesen Text verglichen**: gleich ⇒ Tatsachennotiz;
> verschieden ⇒ **Berichtigung dieses Texts** und allem, was daran hängt
> (Benchmark-Tabelle, Abbild), mit dem Grund „Eingabe war auf nicht-registriertem Datenstand erzeugt"
> — keine Wahl. Text und Tabelle oben bleiben bis dahin zeichengleich.

### 33.3 Die Feldliste des Abbilds — abschliessend

**Fables Ersatztext für 30.2 (3), zeichengleich:**

> Das Abbild trägt **genau** die Grössen, die der Registertext des Faltenplans nach 30.2 (2) nennt — nicht mehr, nicht weniger. Der Registertext 30.2 (2) zählt diese Grössen **abschliessend** auf (die Feldliste). Eine Datei ist das Abbild, wenn (i) ihre Feldmenge gleich der Feldliste ist und (ii) ihre Werte je Bot und je Jahr dem Registertext entsprechen. Beides prüft die Sonde nach 30.2 (3); ein zusätzliches Feld ist ein Fehlschlag wie ein fehlendes. Wie die Datei erzeugt wird, ist Handwerk; der erzeugende Code wird mit der Datei registriert (5e).

**Die Feldliste:**

| | Feld | Inhalt |
|---|---|---|
| | `asof` | das Datum aus 28.2/28.3 |
| je Bot | `bot` | der Name |
| je Bot | `horizontbeginn` | Datum **oder** ausdrücklich „kein Horizont" — ⭐ **gesetzt, nicht weggelassen** |
| | ↳ ⭐ **Ergänzt (34.4, TB-82, 22.09.2026)** | Der Wert ist entweder ein Datum im Format `JJJJ-MM-TT` oder die Zeichenkette `"kein Horizont"` — genau eine der beiden Formen; JSON-`null`, ein fehlender Schlüssel oder eine leere Zeichenkette sind Fehlschläge der Sonde, die den Wert **positiv** gegen die zwei Formen prüft (Fable 21m, Frage 4, Wortlaut in 34.4). `faltenplan_tb80.json` (`null`) ist auch daran kein Abbild |
| je Bot | ⭐ **`faltenlaenge_jahre`** | ⚠️ **Ergänzung gegenüber Fables Vorschlag — Begründung in 33.4** |
| je Bot | `erste_selektionsfalte` | die erste Falte |
| je Bot | `selektionsfalten` | die Liste, aufsteigend und lückenlos |
| | `quelle` | der Registerabschnitt, dessen Wortlaut die Datei abbildet |
| je Bot | ⭐ **`bestaetigungsperiode`** | ⚠️ **Angefügt (35.2, TB-83, 22.09.2026)** — der Bezeichner nach 33.2/35.1, genau in der Form `JJJJ-MM-TT/JJJJ-MM-TT` (Beginn/Ende, Ende ausschliesslich; registrierter Bestand: `2026-01-01/2026-09-01` bei allen neun); die Sonde prüft ihn positiv gegen die aus 21.4 und 5.2 gebildete Spanne. Fable 22a; Grund in 35.3 — ersetzt 33.4 Punkt 3 |

⛔ **Nicht in der Liste und damit nicht in der Datei:** Trainingsgrenzen,
Embargo, Purge. ⭐ *Fable, zwei Sätze aus 21k, je wörtlich:* *„Verfahren B hat
kein Trainingsfenster (Übergabe Abschnitt 1); eine Grösse, die das Verfahren
nicht kennt, kann nicht im Registertext stehen und darf deshalb nicht in der
Datei stehen."* — und zur Feldliste: *„das ist die Folge der Regel, nicht die
Regel."*

⇒ ⚠️ **Keine der drei vorhandenen Dateien ist danach das Abbild** — auch
`faltenplan_tb80.json` nicht, und zwar **nicht wegen ihrer Herkunft**, sondern
weil ihre Feldmenge nicht die Feldliste ist. *Nachgemessen (TB-81, Beleg
Schritt 1): `faltenplan_tb80.json` trägt je Bot 18 Felder und auf oberster
Ebene weder `asof` noch `quelle`.*

### 33.4 ⚠️ Zwei Anpassungen an Fables Feldliste, und warum

**Er hat sie ausdrücklich zur Prüfung gestellt** (*„ich prüfe dann Text und
Feldliste zusammen"*) und eine Unsicherheit benannt.

| | Befund | Folge |
|---|---|---|
| **1** | ⚠️⚠️ **`selektionsfalten` als „Liste von Kalenderjahren" deckt `elliott_wave` nicht ab.** Gemessen: Seine vier Falten sind **Doppeljahre** (`2018-2019`, `2020-2021`, `2022-2023`, `2024-2025`), die der acht übrigen Bots Einzeljahre | Der Registertext in 33.2 sagt **„zusammenhängende Kalenderjahre in Schritten der Faltenlänge"** statt „Kalenderjahre" |
| **2** | ⭐ **Ohne `faltenlaenge_jahre` ist die Liste nicht prüfbar.** Aus `['2018-2019', …]` allein folgt nicht, ob die Faltenlänge 2 ist oder ob zwei Einzeljahre zusammengeschrieben wurden | Das Feld kommt in die Liste |
| **3** | **Seine Unsicherheit — die Bestätigungsperiode je Bot:** Sie steht **bereits** in Register 21.4 und folgt aus Faltenlänge und Go-Live-Schnitt (`elliott_wave` `2026-2027`, die acht übrigen `2026`) | ⭐ **Nicht in die Feldliste.** *Ein Abbild bildet ab, was sein Abschnitt sagt; eine Grösse, die anderswo registriert ist, wäre ein zweiter Ort für denselben Wert* — die Bauart, die er in 21j selbst abgelehnt hat |
| | ⚠️ **Berichtigt (34.6, TB-82, 22.09.2026):** Die Fundstelle „21.4" trägt den Satz nicht — 21.4 führt „Bestätigung ab" `2026-01-01` bei allen neun Bots (gemessen, Beleg M3); `2026-2027` und `2026` sind Faltennamen aus `faltenplan.py:336`, nicht aus dem Register (Beleg M2). Registriert ist die Bestätigungsperiode als **Datumsspanne**: Beginn 21.4 (`2026-01-01`), Ende 5.2 (`2026-09-01`, ausschliesslich) | Die Folge bleibt: **kein Feld** — Fables Halbsatz *„33.2 nennt sie nicht"* trägt allein. ⚠️ Welche der zwei Formen (Datumsspanne / Faltenname) gilt, ist **offen** — bei Fable, Anfrage 21g Punkt 3 (34.6) |
| | ⚠️ **ERSETZT (35.3, TB-83, 22.09.2026):** „Nicht in die Feldliste" gilt nicht mehr — Fable 22a, zeichengleich: *„Die Bestätigungsperiode ist Feld des Abbilds — weil 33.2 sie nennen muss (siehe 3), nicht weil 21.4 sie registriert. Mein Massstab bleibt; seine Anwendung ändert sich mit der Tatsache, dass der Name operativ ist."* Der Name ist ein Schlüssel, den `auswertung.py` (Z. 432) und der Erzeuger teilen (sechste Rücknahme). Feld `bestaetigungsperiode` in 33.3 angefügt (35.2); Punkt 3 oben bleibt zeichengleich | — |

⚠️ **Alle drei sind dem Verfahrensprüfer vorzulegen.** Punkt 1 und 2 ändern
seinen Wortlaut; Punkt 3 beantwortet seine Unsicherheit. ⛔ **Der Abschnitt gilt
bis dahin mit diesem Vermerk** — er ist nicht vorläufig, aber die Prüfung steht
aus.

### 33.5 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Abbild-Datei erzeugen** | eigene Aufgabe, nach Fables Prüfung von 33.2/33.3 und mit Betreiberfreigabe |
| ⛔ | **Die Sonde schreiben** (Feldmenge und Werte gegen den Registertext) | dieselbe Aufgabe |
| ⛔ | **Eine Datei mit Hash auf die Sperrliste nehmen** | dieselbe Aufgabe |
| ⛔ | **`faltenplan.py` ändern** — die Freigabe vom 21.09. galt für Bedingung (i) und ist verbraucht | — |
| ⚠️ | **Entscheidungsvorlage, nicht vollzogen:** ob die Abbild-Datei aus einem geänderten `faltenplan.py` entsteht oder aus einem **neuen, kleinen Schreiber**, der genau die Feldliste ausgibt. ⭐ *Fable: „gleichwertig, solange der Code registriert ist."* Beides berührt Sperrlisten-nahen Code und braucht eine eigene Freigabe | Betreiber |

> ⭐⭐ **Plan-Punkt 7 rückt vor (40.6/40.8 (g), Fable 24a, TB-96,
> 24.09.2026):** Das Abbild des Faltenplans (33.3) und die Faltenplan-Sonde
> sind die Wache gegen einen Schwellenübertritt, der den Faltenplan eines Bots
> verschiebt — und sie fehlen. ⚠️ **Erzeugt wird das Abbild NACH der
> Neu-Ableitung der Faltenlänge (TB-98), nicht vorher** — sonst bildet es einen
> Stand ab, der gerade geprüft wird (TB-100). Die Tabelle oben bleibt
> zeichengleich; die Freigaben, die sie verlangt, gelten weiter.

---

## 34. Fünf Einträge des Verfahrensprüfers aus 21l/21m und eine Berichtigung eines eigenen Satzes — Faltenregeln, `horizontbeginn`, „vier" → „neun" (TB-82, 22.09.2026)

⭐ **Reines Eintragen von Registertext.** Fünf Einträge sind zeichengleich von
Fable (vier aus 21m, einer aus 21l), der sechste berichtigt einen Satz des
steuernden Chats in 33.4. **Kein Code, keine Abbild-Datei, keine Sonde, kein
Hash, keine Wache** — 34.7.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21m_faltenplan_pruefung.md`
(34.1–34.4) und `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21l_standpruefung.md`
(34.5), zeichengleich; 34.6 aus
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21g_berichtigung_und_bestaetigungsperiode.md`
Punkt 2 und 3. Auftrag `docs/auftraege/MAC_TB-82_register_34.md`; Messungen
`docs/belege/TB-82/` (M1–M5), alle **vor** dem Eintrag gemessen, HEAD `9614624`.

⭐⭐ **Neu in diesem Abschnitt — die Marke steht AM ALTEN ORT.** Jeder der sechs
Einträge ist an zwei Stellen sichtbar: hier mit vollem Text, Herkunft und Grund,
und **direkt unter dem berichtigten Satz** als eingerückter Hinweisblock mit
Verweis auf 34.x. Der alte Satz bleibt zeichengleich; die Marke fügt nur hinzu
(dieselbe Bauart wie die Tatsachennotiz unter Sperrlistenpunkt 2, Abschnitt 10
und 30.3). *Fables Grund, 21m Frage 3, wörtlich:* *„Wer 30.2 (2) liest und
abschreibt, sieht 33.2 nicht — genau der Fehler aus 21h. Eine Marke am falschen
Satz kostet eine Zeile; ein Hinweis drei Abschnitte weiter kostet irgendwann
eine Rücknahme."* Prüfbar: `git diff --numstat` auf dieses Register zeigt für
TB-82 in der zweiten Spalte `0`.

⭐ **Fables Regel aus dem Vorab von 21m, die ab hier für jeden seiner Texte gilt,
wörtlich:** *„Wo mein Registertext eine Tatsache über den Bestand voraussetzt (ein Feld, eine Datei, eine Zahl von Modulen), nenne ich sie als Voraussetzung, und ihr messt sie, bevor der Text eingetragen wird."* — deshalb tragen 34.1, 34.2, 34.5 und 34.6 je eine
Tatsachennotiz mit der Messung, die der Text voraussetzt.

### 34.1 Ergänzung zu 33.2 — Falten mit Faltenlänge L > 1

**Fable, 21m Frage 1 (1a), zeichengleich:**

> **Ergänzung zu 33.2:** Bei Faltenlänge L > 1 ist ein Kalenderjahr J erstes Jahr einer Selektionsfalte, wenn J die Bedingungen (i) und (ii) nach 25 erfüllt; die Falte umfasst J bis J + L − 1. Die erste Selektionsfalte beginnt mit dem ersten Kalenderjahr, das (i) und (ii) erfüllt; die folgenden Falten schliessen lückenlos an.

**Fables Grund, zeichengleich:**

> *Grund:* (i) prüft den Vorlauf am 1. Januar — der einzige 1. Januar, an dem eine Falte beginnt, ist der ihres ersten Jahres. (ii) muss am ersten Jahr geprüft werden, weil die Falte sonst mit Jahren beginnen könnte, in denen der Bot nichts handelt — der Kapitalpfad (29) startet am 1. Januar der ersten Falte und braucht dort Handelbarkeit.

**Tatsachennotiz (TB-82, gemessen vor dem Eintrag, `m5_faltenlisten.txt`):**
Betroffen ist nur `elliott_wave` (L = 2); die acht übrigen Bots haben L = 1,
für sie ist 34.1 die Regel aus 25 unverändert. Für `elliott_wave` ergibt der
Text, auf das erste Jahr 2018 angewandt und lückenlos fortgesetzt, genau die
vier Falten aus 33.2 (2018–2019 · 2020–2021 · 2022–2023 · 2024–2025).
⭐ **Die Faltenliste in 33.2 ändert sich durch diese Ergänzung nicht** — die
neun Tabellenzeilen sind vor und nach dem Eintrag zeichengleich (SHA-256 der
Zeilen im Beleg) und gegen 21.4 mit 0 Abweichungen.

**Marke am alten Ort:** unter 33.2, nach dem Registertext-Block.

### 34.2 Ergänzung zu 33.2 — der Rest vor dem Go-Live-Schnitt

**Fable, 21m Frage 1 (1b), zeichengleich:**

> **Ergänzung zu 33.2:** Ein Rest von weniger als L Kalenderjahren zwischen der letzten vollen Selektionsfalte und dem Go-Live-Schnitt ist keine Selektionsfalte. Sein Verhältnis zur Bestätigungsperiode regelt 21.4; 33.2 trifft dazu keine Aussage.

**Fables Grund, zeichengleich:**

> *Grund:* 4a kennt nur ganze Falten; eine Teilfalte hätte weniger Beobachtungen als die übrigen und ginge mit gleichem Gewicht in den Faltenmedian — eine Verzerrung, die 4a nirgends zulässt. Kein Ergebnis: Für den registrierten Bestand tritt der Fall nicht ein; die Faltenliste ändert sich um nichts.

⭐⭐ **Tatsachennotiz — Antwort auf Fables ausdrückliche Unsicherheit** (21m:
*„ob 21.4 den Rest vor Go-Live bereits regelt — dann ist (1b) ein Verweis statt
einer Regel"*), **gemessen von TB-82 vor dem Eintrag** (`m1_rest.txt`, HEAD
`9614624`; die Zahl des steuernden Chats vom 21.09. an `ad020b5` wurde nicht
übernommen, sondern nachgemessen): Gesucht wurde im ganzen Register nach
`Rest` (als ganzes Wort, mit Positivkontrolle der Wortgrenze), `Teilfalte` und
`angebrochene` — **null Treffer**, in zwei Lesungen (`\b` und `-w`). 21.4 führt
je Bot ausschliesslich Markt, Faltenlänge, erste Falte, Anzahl der
Selektionsfalten, „Bestätigung ab" und „4b erfüllt" (`m3_bestaetigung_ab.txt`).
⇒ **(1b) ist eine Regel, kein Verweis.** Für den registrierten Bestand tritt
der Fall nicht ein: Bei allen neun Bots enden die Selektionsfalten mit 2025;
zwischen der letzten vollen Falte und dem Go-Live-Schnitt `2026-09-01` liegt bei
allen neun derselbe Rest, `2026-01-01` bis `2026-09-01` — kürzer als L bei
jedem Bot, also nach 34.2 keine Selektionsfalte. Die Faltenliste ändert sich
um nichts (34.1, Beleg M5).

**Marke am alten Ort:** unter 33.2, zusammen mit 34.1.

### 34.3 Berichtigung zu 30.2 (2) — `3b (b)` lies `3b (a)`

**Fable, 21m Frage 3, zeichengleich:**

> **Berichtigung zu 30.2 (2):** Die Fundstelle „Trockenlauf nach 3b (b)" lies „3b (a)". Gemeint ist der Trockenlauf aus 3b (a), der die `MIN_HISTORY_*`-Tabelle aus 3b (b) anwendet; ein zweiter Trockenlauf existiert nicht.

**Fables Grund, warum ein eigener Satz und nicht nur der Zitierhinweis in 33.2,
zeichengleich:**

> *Warum nicht nur der Hinweis in 33.2:* Wer 30.2 (2) liest und abschreibt, sieht 33.2 nicht — genau der Fehler aus 21h. Eine Marke am falschen Satz kostet eine Zeile; ein Hinweis drei Abschnitte weiter kostet irgendwann eine Rücknahme. Meine Zitierregel (nur vorgelegte Fundstellen) hat hier versagt, weil ich „3b (b)" aus 20e übernommen hatte, wo es um die Handelbarkeitstage ging — dieselbe Unternummer, andere Sache.

⚠️⚠️ **Der Satz „Trockenlauf nach 3b (b)" in 30.2 (2) bleibt zeichengleich
stehen** (append-only) und trägt die Marke **direkt unter 30.2 (2)** — genau
dieser Eintrag ist der Anlass für die Regel „Marke am alten Ort" im Kopf dieses
Abschnitts. Der Zitierhinweis in 33.2 (TB-81) bleibt ebenfalls zeichengleich
stehen und bekommt einen Satz, dass die ausdrückliche Berichtigung in 34.3
steht. Gemessen (TB-81, Beleg Schritt 2, unverändert): In 16.7 ist **3b (a)**
der Trockenlauf-Satz, **3b (b)** die `MIN_HISTORY_*`-Tabelle; 21.3 (a), 21.4
und `erste_falte_quelle` zitieren 3b (a).

### 34.4 Ergänzung zu 33.3, Feld `horizontbeginn` — Zeichenkette oder Datum

**Fable, 21m Frage 4, zeichengleich:**

> **Ergänzung zu 33.3, Feld `horizontbeginn`:** Der Wert ist entweder ein Datum im Format `JJJJ-MM-TT` oder die Zeichenkette `"kein Horizont"` — genau eine der beiden Formen. JSON-`null`, ein fehlender Schlüssel oder eine leere Zeichenkette sind Fehlschläge der Sonde. Die Sonde prüft den Wert positiv gegen diese zwei Formen, nicht das Vorhandensein des Schlüssels.

**Fables Grund, zeichengleich:**

> *Grund:* Derselbe wie bei der Feldliste — eine **positive** Prüfung gegen eine abschliessende Menge ersetzt ein Urteil über Abwesenheit. `null` ist genau das Gegenteil: ein Wert, der „nichts" bedeutet und in einer Bibliothek von „fehlt" unterscheidbar ist, in der nächsten nicht (euer Befund). „Gesetzt, nicht weggelassen" hiess: Wer die Datei liest, soll *lesen*, dass der Bot keinen Horizont hat — nicht schliessen, dass ihm einer fehlt. Eine Zeichenkette tut das; `null` verlangt Kenntnis der Konvention. Folge: `faltenplan_tb80.json` (Schlüssel mit `null`) ist auch daran kein Abbild; das war es nach 33.3 schon nicht.

⭐ **Folge, die Fable selbst zieht und die hier eingetragen wird:**
`research/vorregistrierung/ergebnisse/faltenplan_tb80.json` — Schlüssel
`horizontbeginn` mit JSON-`null` bei den fünf Krypto-Bots (33.2, Lesehilfe;
TB-81 Schritt 1) — ist **auch daran** kein Abbild; *„das war es nach 33.3 schon
nicht"* (Feldmenge 18 statt der Feldliste). Damit ist die in TB-81 offen
gelassene Frage, ob `null` das „ausdrücklich gesetzt" aus 33.3 ist,
**entschieden: nein.** Die Zeile in 33.2 („kein Horizont" steht in der
gemessenen Datei als JSON-`null`) bleibt als Tatsachennotiz zur gemessenen
Datei richtig; für das Abbild gilt 34.4.

**Marke am alten Ort:** in der Feldliste 33.3, als eigene Zeile direkt unter
`horizontbeginn`.

### 34.5 Berichtigung zu 29.4 — „vier" → „neun" `multi_symbol_optimise.py`

**Fable, 21l Punkt 4 (b), zeichengleich:**

> **Berichtigung zu 29.4:** Die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte" wird in **allen neun** `multi_symbol_optimise.py` eingebaut, nicht nur in den vier Aktien-Optimierern. Der Bericht führt je Bot Horizontbeginn (oder „kein Horizont"), Beginn der ersten Selektionsfalte und frühesten Einstieg nebeneinander auf.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* Die Regel 29 (Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte) gilt je Bot für alle neun; 21c 3.2 hat den Fall für Krypto ausdrücklich benannt („rsi2_crypto: 2018 handelbar, erste Falte 2019"). „Die vier" stammt aus 21b, als die Wache noch gegen den Horizontbeginn prüfte, den nur Aktien-Bots haben. Mit dem Wechsel des Prüfdatums in 21c/29.4 hätte die Zahl mitwandern müssen; sie ist es nicht — mein Versehen, dieselbe Art wie der verlorene Vorlauf-Satz. Kein Ergebnis: Ob die Wache bei einem Krypto-Bot je anschlägt, ist für die Regel gleichgültig.

*Fables Einordnung, 21l, zeichengleich:* *„Kategorie: Berichtigung mit Ersatzwort, „vier" → „neun"; 29.4 bleibt stehen, Marke wie üblich."*

⭐ **Tatsachennotiz (TB-82, gemessen vor dem Eintrag, `m4_wachen_optimierer.txt`,
nur lesend):** In **keinem** der neun `strategies/<bot>/multi_symbol_optimise.py`
steht heute eine Wache — `assert `, `raise `, „Wache" je Datei **0**, in einer
zweiten, weiter gefassten Lesung (`assert`, `raise`, `wache` ohne Rücksicht auf
Gross-/Kleinschreibung, `Selektionsfalte`) ebenfalls **0**; neun Dateien, alle
vorhanden, SHA-256 je Datei im Beleg. ⇒ Der Einbau ist ein **Ersteinbau**, keine
Änderung — und er gehört zu **TB-30b**, nicht zu diesem Auftrag. Der Satz
„Ort der Wache unverändert: in den vier `multi_symbol_optimise.py`" in 29.4
bleibt zeichengleich stehen und trägt die Marke; unverändert gilt daraus:
**nicht** in `auswertung.py`.

**Marke am alten Ort:** unter 29.4, direkt am Absatz „in den vier
`multi_symbol_optimise.py`".

### 34.6 ⚠️ Berichtigung zu 33.4 Punkt 3 — eine Fundstelle des steuernden Chats trug ihren Satz nicht

⚠️ **Kein Fable-Eintrag, sondern die Berichtigung eines eigenen Satzes.** Was
in 33.4 Punkt 3 steht, bleibt zeichengleich: *„Sie steht **bereits** in
Register 21.4 und folgt aus Faltenlänge und Go-Live-Schnitt (`elliott_wave`
`2026-2027`, die acht übrigen `2026`)."*

> **Berichtigung zu 33.4 Punkt 3 (steuernder Chat, 21.09.2026; nachgemessen
> von TB-82 vor dem Eintrag, `m2_2026-2027.txt` und `m3_bestaetigung_ab.txt`).**
> Die Fundstelle „21.4" trägt den Satz nicht. **Gemessen:** 21.4 führt die
> Spalte **„Bestätigung ab"** mit dem Wert `2026-01-01` **für alle neun Bots**
> (9/9); die Werte `2026-2027` und `2026` als Faltenname kommen dort nicht vor
> (0 Treffer in den neun Zeilen, beide Strichformen). Gegenprobe über das ganze
> Register: `2026-2027` hat **genau einen** Treffer (Z. 5431 im Stand
> `9614624`), und das ist der berichtigte Satz selbst. **Die Werte stammen aus
> `research/vorregistrierung/faltenplan.py:336`** (`falten[-1]["name"]`, nur
> gelesen), also aus dem Code. **Registriert ist die Bestätigungsperiode
> gleichwohl** — ihr **Beginn** in 21.4 (`2026-01-01`), ihr **Ende** in 5.2
> (Go-Live-Schnitt `2026-09-01`, ausschliesslich), also als **Datumsspanne
> statt als Faltenname**. ⭐ **Fables Schluss in 21m Frage 2 (3) bleibt davon
> unberührt:** Sein erster Halbsatz — *„33.2 nennt sie nicht"* — trägt allein;
> die Bestätigungsperiode ist **kein Feld** der Feldliste.

⚠️⚠️ **Offen — hier eingetragen, nicht entschieden:**

> **Offen (an Fable, Anfrage 21g Punkt 3):** Der Begriff „Bestätigungsperiode"
> trägt zwei Formen — im Register eine **Datumsspanne** (`2026-01-01` bis
> `2026-09-01`), in `faltenplan.py` einen **Faltennamen**. Für `elliott_wave`
> klaffen sie: Der Name lautet `2026-2027`, die Periode endet am `2026-09-01`.
> ⚠️ **Welche Form gilt, ist nicht registriert.** Die Frage liegt bei Fable
> (Anfrage 21g); **dieser Abschnitt entscheidet sie nicht.**

> ⭐ **Beantwortet und ersetzt (35.1 / 35.3, TB-83, 22.09.2026):** Fable 22a hat
> entschieden — **die Datumsspanne gilt**; der Bezeichner ist die Spanne selbst,
> `JJJJ-MM-TT/JJJJ-MM-TT`, für alle neun Bots `2026-01-01/2026-09-01`; der Faltenname
> `2026-2027` ist unzulässig (35.1). Und der Schluss oben *„die Bestätigungsperiode
> ist **kein Feld** der Feldliste"* ist **ERSETZT**: `bestaetigungsperiode` ist Feld
> (35.2/35.3, Fables sechste Rücknahme — der Name ist ein Schlüssel, den
> `auswertung.py` und der Erzeuger teilen). Der Block oben bleibt zeichengleich.

**Marke am alten Ort:** in der Tabelle 33.4, als eigene Zeile direkt unter
Punkt 3.

### 34.7 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Abbild-Datei erzeugen** | eigene Aufgabe, eigene Betreiberfreigabe (33.5) |
| ⛔ | **Die Sonde schreiben** — auch nicht die positive Prüfung aus 34.4 | dieselbe Aufgabe |
| ⛔ | **Einen Hash auf die Sperrliste nehmen** | dieselbe Aufgabe |
| ⛔ | **`faltenplan.py` oder irgendeine `.py` ändern** — keine Freigabe; die vom 21.09. galt für Bedingung (i) und ist verbraucht | — |
| ⛔ | **Die Wache aus 29.4/34.5 einbauen** — sie ist Ersteinbau in allen neun Optimierern | TB-30b |
| ⛔ | **Die offene Frage aus 34.6 beantworten** | Fable (Anfrage 21g) |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (Beleg M5); die drei Sperrlisten-Hashes `0e54ac5c…`, `a163c498…`, `4549395f…` unverändert | — |

*Dieser Abschnitt ist rein additiv: Er trägt fünf Texte des Verfahrensprüfers
zeichengleich ein, berichtigt einen eigenen Satz, setzt zu jedem der sechs eine
Marke am alten Ort — und entfernt nichts.*

---

## 35. Die Bestätigungsperiode bekommt ihren Bezeichner und wird Feld des Abbilds, und 30.2 (3) wird präzisiert — die Sonde prüft den gerechneten Plan vor dem Start (Fable 22a, TB-83, 22.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34. Vier Einträge, alle
zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22a_bestaetigungsperiode.md` (Antwort
auf die Anfrage 21g des steuernden Chats, Punkte 2 und 3). Auftrag
`docs/auftraege/MAC_TB-83_register_35.md`; Messungen `docs/belege/TB-83/`
(M1–M6), alle **vor** dem Eintrag gemessen, HEAD `9dac8d4`. ⛔ **Kein Code,
kein Aufruf von `faltenplan.py`, keine Abbild-Datei, keine Sonde, kein
Wrapper, kein Hash** — 35.5.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text, Herkunft
und Grund **und** als Marke direkt beim alten Satz (33.2, 33.3, 33.4 Punkt 3,
34.6, 30.2 (3)). Die alten Sätze bleiben zeichengleich; `git diff --numstat`
auf dieses Register zeigt für TB-83 in der zweiten Spalte `0`.

⭐ **Damit ist die in 34.6 offen eingetragene Frage entschieden** — welche der
zwei Formen der Bestätigungsperiode gilt: **die Datumsspanne** (35.1). Und
**33.4 Punkt 3 („Nicht in die Feldliste") ist ERSETZT** (35.3) — Fables sechste
Rücknahme, aus einem Grund, den weder 21m noch 34.6 kannten: der Name ist ein
Schlüssel, den zwei Programme teilen.

### 35.1 Ergänzung zu 33.2 — die Bestätigungsperiode und ihr Bezeichner

**Fable, 22a Abschnitt 3, zeichengleich:**

> **Ergänzung zu 33.2 (Bestätigungsperiode):** Die Bestätigungsperiode eines Bots ist die Datumsspanne von „Bestätigung ab" (21.4) bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich. Sie ist keine Selektionsfalte und keine Falte im Sinn von 4a; ihre Länge ist von der Faltenlänge des Bots unabhängig, und dass sie kürzer als eine Faltenlänge ist, ist gewollt — (1b) betrifft sie nicht. Ihr **Bezeichner** in Plan, Abbild, `zellen.csv` und Berichten ist die Spanne selbst in der Form `JJJJ-MM-TT/JJJJ-MM-TT` (Beginn/Ende, Ende ausschliesslich); für den registrierten Bestand bei allen neun Bots `2026-01-01/2026-09-01`. Ein Bezeichner, der Kalenderjahre ausserhalb der Spanne nennt, ist unzulässig.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 21.4 und 5.2 registrieren die Spanne; Verfahren B definiert die Bestätigungsperiode als den einzigen Out-of-Sample-Zeitraum (Übergabe Abschnitt 1). Ein Name, der mehr verspricht als die Spanne, würde beim Lesen der Ergebnisse — nach dem Lauf, wenn niemand mehr nachrechnet — als Zeitraum verstanden. Kein Ergebnis: Die Spanne ist unverändert, es ändert sich nur, wie sie heisst.

**Tatsachennotiz (TB-83, gemessen vor dem Eintrag — die Grundlage des
Bezeichners wird nicht übernommen, sondern gemessen):** 21.4 führt in der
Spalte „Bestätigung ab" bei **allen neun** Bots `2026-01-01` (9/9, Tabellenkopf
Z. 2917, Datenzeilen 2919–2927; `m1_bestaetigung_ab.txt`); 5.2 setzt den
Go-Live-Schnitt `2026-09-01`, **ausschliesslich** (`m2_go_live_schnitt.txt`),
und 21.4 wiederholt ihn im Vorsatz („Bestätigungsperiode unverändert bis
`2026-09-01`, ausschliesslich"). ⇒ Der Bezeichner nach 35.1 lautet für den
registrierten Bestand bei allen neun Bots **`2026-01-01/2026-09-01`** — aus 21.4
und 5.2 gebildet.

⚠️ **Ausdrücklich eingetragen:** Der **heutige** Bezeichner in
`research/vorregistrierung/faltenplan.py:336` ist der **Faltenname**
(`falten[-1]["name"]`: `2026-2027` bei `elliott_wave`, `2026` bei den acht
übrigen; gemessen, nur gelesen, `m4_faltenplan_bezeichner.txt` — zwei
Fundstellen, Z. 336 Erzeugung und Z. 368 Konsolenausgabe in `main()`) und damit
nach diesem Registertext **unzulässig**, weil er Kalenderjahre ausserhalb der
Spanne nennt. ⛔ **Die Umstellung ist Handwerk mit eigener Freigabe und nicht
Teil von TB-83**; sie hängt an Fables Antwort auf
`FABLE_ANFRAGE_2026-09-22a_sperrlistenfalle.md` (35.5). *Fable dazu,
zeichengleich:*

> *Folge, Handwerk:* `faltenplan.py:336` bildet den Namen heute aus dem Faltennamen; die Änderung ist eine Zeile und braucht eine Betreiberfreigabe. `auswertung.py` bleibt unberührt — es liest den Namen aus dem Plan, wie auch immer er lautet. Der Erzeuger schreibt denselben Bezeichner in `zellen.csv`; er ist noch nicht geschrieben, es kostet dort nichts. Die ⚠️-Markierung in 21.4 bei `elliott_wave`: bitte den ganzen Eintrag vorlegen, bevor jemand sie als Beleg nimmt — ich habe nur eure Vermutung dazu.

> ⚠️ **Marke (36.1 (4) und 36.3, Fable 22b, TB-84, 22.09.2026):** Die Umstellung
> von `faltenplan.py:336` (und der Ausgabe Z. 368) auf den Bezeichner ist
> **Schritt 3** der Reihenfolge in 36.3 und kommt **erst nach Schritt 2** —
> Voreinstellung von `main()` weg von `ergebnisse/faltenplan.json` und
> Einmal-Schreibsperre (36.1 (4)); davor Schritt 1, die Sperrlisten-Sonde.
> Fable, 22b: *„Wer Schritt 3 vor Schritt 2 macht, hat genau den Fall, den ihr beschreibt."*
> Betreiberfreigabe für alle vier Schritte steht aus (Stand 22.09.2026). Bis
> dahin: `python3 faltenplan.py` nicht aufrufen.

> ⭐⭐ **Berichtigung (38.1, Fable 22h, TB-89, 23.09.2026) — Weg (A):** Der
> Satz „die Änderung ist eine Zeile" im Handwerkszitat oben ist berichtigt.
> Der Bezeichner entsteht **dort, wo die letzte Falte ihren Namen bekommt**
> (`faltenplan.py`, Funktion `_plan`, Zuweisung der Rolle `bestaetigung`): die
> letzte Falte **heisst** die Spanne `2026-01-01/2026-09-01`; Faltenname,
> `bestaetigungsperiode`, Spalte `falte` und Bericht tragen denselben String
> aus derselben Quelle. Weg (B) — zwei Namen für dieselbe Periode — ist
> unzulässig. Umsetzung: TB-90, Freigabe liegt vor.

> ⚠️ **Tatsachennotiz zu den Zeilennummern oben (38.7 (a), TB-88, belegt
> 38.2):** Am Stand `8851f67` steht die Erzeugung auf **Z. 338**, die
> Konsolenausgabe auf **Z. 460** von `faltenplan.py` (Funktionen `_plan` und
> `main`); verschoben durch **`4daa254`** (TB-86 Schritt 2/3). Die Zahlen 336
> und 368 oben bleiben zeichengleich; sie gelten für den Stand, an dem TB-83
> sie gemessen hat.

> ⚠️⚠️ **Tatsachennotiz (38.7 (c), TB-88, Messstand `8851f67`):** Weg (B)
> hätte einen Sperrlistenpunkt berührt — `auswertung.py`, Funktion
> `lies_zellen`, vergleicht die Menge der `falte`-Werte gegen die Faltennamen
> des Plans und bricht unter (B) ab (Sperrlistenpunkt 5). Weg (A) läuft in der
> Probe durch. Einzelheiten in **38.1**.

⚠️ Zur ⚠️-Markierung bei `elliott_wave` in 21.4: Die Zelle lautet wörtlich
`⚠️ **2026-01-01**`; 21.4 trägt keinen Satz, der sie begründet. Fable bat, den
ganzen Eintrag vorzulegen, bevor jemand sie als Beleg nimmt (Anfrage 22a
Punkt 1) — hier nur gemessen, nicht gedeutet.

**Marke am alten Ort:** unter 33.2, nach der Marke aus 34. **Kein** Eintrag in
21.4 — 21.4 bleibt unberührt, 35.1 zitiert es nur.

### 35.2 Ergänzung zu 33.3 — `bestaetigungsperiode` wird Feld

**Fable, 22a Abschnitt 3, zeichengleich:**

> **Ergänzung zu 33.3 (Feldliste), je Bot:** `bestaetigungsperiode` — der Bezeichner nach 33.2, genau in dieser Form; die Sonde prüft ihn positiv gegen die aus 21.4 und 5.2 gebildete Spanne.

Die Feldliste in 33.3 wächst damit um **eine Zeile je Bot**; die Sonde prüft
den Wert **positiv** gegen die aus 21.4 und 5.2 gebildete Spanne — dieselbe
Bauart wie bei `horizontbeginn` (34.4). Der Grund, warum die Bestätigungsperiode
nun doch Feld ist, steht in 35.3.

**Marke am alten Ort:** in der Feldliste 33.3, als neue, angefügte
Tabellenzeile — keine bestehende Zeile geändert.

### 35.3 ⭐⭐ Fables sechste Rücknahme — warum die Bestätigungsperiode doch Feld ist

⚠️ **Das ERSETZT 33.4 Punkt 3 („Nicht in die Feldliste") und den Schluss von
34.6 („kein Feld der Feldliste").** Beide Sätze bleiben dort zeichengleich
stehen und tragen die Marke.

**Fables Begründung, 22a Abschnitt 2, zeichengleich:**

> **Aber Punkt 3 eurer Anfrage liefert eine Tatsache, die (3) trotzdem kippt** — nicht die Fundstelle, sondern die Rolle des Namens: Nach Nachtrag 2 (Z. 432–435) liest `auswertung.py` den Namen der Bestätigungsperiode aus dem Plan und sucht damit die Zeile in `zellen.csv`. **Der Name ist ein Schlüssel, den zwei Programme teilen müssen** — das eingefrorene `auswertung.py` und der noch zu schreibende Erzeuger. Ein Schlüssel, den zwei registrierte Programme teilen, ist eine Grösse des Verfahrens und gehört in den Registertext; und was 33.2 nennt, ist nach 33.3 Feld. Damit:

**Und der Registersatz, zeichengleich:**

> **(3), berichtigt:** Die Bestätigungsperiode ist Feld des Abbilds — weil 33.2 sie nennen muss (siehe 3), nicht weil 21.4 sie registriert. Mein Massstab bleibt; seine Anwendung ändert sich mit der Tatsache, dass der Name operativ ist.

**Fable selbst dazu, zeichengleich:**

> Das ist die sechste Rücknahme, und sie hat denselben Grund wie die fünf davor: Ich kannte den Bestand nicht — hier, dass der Name als Schlüssel dient.

**Tatsachennotiz (TB-83, gemessen, nur gelesen, `m3_auswertung_faltenplan.txt`):**
Der Schlüssel ist im eingefrorenen `auswertung.py` sichtbar — Z. 432
`name = plan[bot]["bestaetigungsperiode"]` in der Funktion
`bestaetigungsperiode()` (Z. 430), weitergereicht in Z. 550 und Z. 638. Der
Massstab aus 21m („ein Abbild trägt genau die Grössen seines Abschnitts") bleibt;
was sich ändert, ist die Tatsache, dass 33.2 die Bestätigungsperiode seit 35.1
nennt.

**Marken am alten Ort — zwei:** bei 33.4 Punkt 3 (als eigene Tabellenzeile
unter der Marke aus 34.6) und unter dem Offen-Block in 34.6.

### 35.4 Präzisierung zu 30.2 (3) — wann die Sonde prüft

**Fable, 22a Abschnitt 4, zeichengleich:**

> **Präzisierung zu 30.2 (3):** Der Lauf verwendet den Plan, den `faltenplan.py` zur Laufzeit bildet. Die Sonde vergleicht diesen Plan **vor dem Start des Laufs** mit dem Abbild (Feldmenge und Werte); bei Abweichung bricht der Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Das Abbild ist damit der registrierte Sollzustand, gegen den der gerechnete Plan geprüft wird — nicht die Datei, die `auswertung.py` öffnet.

**Fables Grund, zeichengleich (zwei Absätze aus 22a):**

> *Quelle des Grundes:* 21b (3) — das Einfrieren von `auswertung.py` hat Vorrang; die Prüfung wandert dorthin, wo geändert werden darf (Wrapper, `faltenplan.py`), wie schon bei der Wache. Kein Ergebnis.

> Ohne diese Präzisierung wäre 30.2 (3) beim ersten Lauf falsch: Es gäbe eine gesperrte Datei, die niemand liest, und einen gerechneten Plan, den niemand prüft.

**Tatsachennotiz (TB-83, aus Nachtrag 1 bestätigt, `m3_auswertung_faltenplan.txt`):**
`auswertung.py` bezieht den Plan über **genau einen** Aufruf,
`plan = fp.faltenplan(mess)` in **Z. 589** (`import faltenplan as fp`, Z. 96) —
es **rechnet** ihn zur Laufzeit; die einzige Plandatei, die es öffnet, ist
`benchmark_drawdowns.json` (Z. 590, Sperrlistenpunkt 4), keine
`faltenplan*.json`. ⇒ 30.2 (3) „der Lauf liest genau diese" ist ab hier so zu
lesen, wie 35.4 es sagt: Das Abbild ist der **Sollzustand**, gegen den der
gerechnete Plan **vor dem Start** geprüft wird; bei Abweichung bricht der
Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Sonde und Wrapper sind
**nicht** geschrieben (35.5).

**Marke am alten Ort:** direkt unter 30.2 (3), innerhalb des
Registertext-Blocks — wie die Marke aus 34.3 unter (2).

### 35.5 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **`faltenplan.py:336` auf den neuen Bezeichner umstellen** — keine Freigabe; hängt an Fables Antwort auf die Sperrlistenfalle (Anfrage 22a Punkt 3: `main()` schreibt nach `ergebnisse/faltenplan.json`, Sperrlistenpunkt 2) | Betreiber, nach Fable |
| ⛔ | ⚠️⚠️ **`python3 faltenplan.py` ausführen** — in dieser Sitzung **nicht geschehen**; der Hash von `ergebnisse/faltenplan.json` ist vor **und** nach der Arbeit `0e54ac5c…` (`m6_sperrlisten_hash.txt`) | — |
| ⛔ | **Die Abbild-Datei erzeugen** — jetzt mit dem Feld `bestaetigungsperiode` | eigene Aufgabe, Betreiberfreigabe (33.5) |
| ⛔ | **Die Sonde schreiben** — Feldmenge, Werte, die positiven Prüfungen aus 34.4 und 35.2, der Zeitpunkt aus 35.4 | dieselbe Aufgabe |
| ⛔ | **Den Laufwrapper mit dem Abbruch aus 35.4 bauen** | dieselbe Aufgabe |
| ⛔ | **Einen Hash auf die Sperrliste nehmen** | dieselbe Aufgabe |
| ⛔ | **Irgendeine `.py` ändern** | — |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (Beleg M5); die drei Sperrlisten-Hashes unverändert | — |
| ⚠️ | **Offen bei Fable:** *„**Unsicher:** ob `faltenplan.py` den Namen der Bestätigungsperiode noch an anderer Stelle verwendet als Z. 336 (dann mehr als eine Zeile) — Handwerk, zu messen vor der Freigabe."* — die Anfrage 22a Punkt 2 hat dazu gemessen (zwei Fundstellen in `faltenplan.py`, Z. 336 und 368; im Laufkreis zieht alles mit); seine Antwort steht aus | Fable |

*Dieser Abschnitt ist rein additiv: Er trägt vier Texte des Verfahrensprüfers
zeichengleich ein, setzt fünf Marken am alten Ort, entscheidet die in 34.6
offene Frage durch Fables Text — und entfernt nichts.*

---

## 36. Die Schreibregel für Sperrlistenpfade, die Sperrlisten-Sonde mit drei Ausgängen, das Abbild der Sperrliste als neue Datei und die Reihenfolge der Handwerksschritte — und eine Tatsachennotiz zur ⚠️-Markierung in 21.4 (Fable 22b und 22c, TB-84, 22.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34 und 35. Sechs Einträge — vier
Ersteinträge (36.1, 36.2, 36.5, 36.6), eine Reihenfolge (36.3) und eine
Tatsachennotiz (36.4) —, alle Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22b_schreibregel_sperrliste.md`
(Antwort auf die Anfrage 22a des steuernden Chats, die Sperrlistenfalle:
`faltenplan.py main()` schreibt nach `ergebnisse/faltenplan.json`,
Sperrlistenpunkt 2) und
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22c_drei_ausgaenge_und_abbild.md`
(Antwort auf die Anfrage 22b, Frage 1 und 2; **berichtigt einen Satz aus 22b
am selben Tag**, 36.5). Auftrag `docs/auftraege/MAC_TB-84_register_36.md`
(erweitert um 36.5 und 36.6, bevor Abschnitt 36 eingetragen war); Messungen
`docs/belege/TB-84/` (M1–M6), alle **vor** dem Eintrag gemessen, HEAD `4bbd720`.
⛔ **Kein Code, keine Sonde, kein Umbau von `main()`, kein Aufruf von
`faltenplan.py`, keine Abbild-Datei, kein Hash, keine Freigabe** — 36.7.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (Sperrliste
Punkt 2, Überschrift von Abschnitt 10, 35.1, 21.4 — und für die Berichtigung
aus 36.5 an den zwei Sätzen in 36.1 und 36.2, die sie berichtigt). Die alten
Sätze bleiben zeichengleich; `git diff --numstat` auf dieses Register zeigt für
TB-84 in der zweiten Spalte `0`.

⚠️ **Was dieser Abschnitt ist:** Er schliesst die Lücke, die die Anfrage 22a
gemessen hat — *Fable, 22b Abschnitt 2, zeichengleich:* *„Was ihr gemessen habt, ist nicht ein Fehler in `faltenplan.py`, sondern **das Fehlen einer Regel**: Nirgends steht, dass ein Programm eine gesperrte Datei nicht schreiben darf. Die Sperrliste sagt, *was* unverändert bleiben muss; sie sagt nicht, *wer* es sicherstellt. Acht Tage lang war das der Zufall."* Die Regel steht ab hier
(36.1); wer sie ausführt, steht ebenfalls (36.2), mit welchen Ausgängen (36.5)
und gegen welches Abbild (36.6); und in welcher Reihenfolge das Handwerk folgt,
steht in 36.3. ⚠️ **Gebaut ist davon nichts** — die Freigabe des Betreibers
für die vier Handwerksschritte steht aus (36.3, 36.7), und bei Fable stehen
eine Tatsachennotiz und eine Frage aus (36.6).

### 36.1 Schreibregel für Sperrlistenpfade — Ersteintrag

**Fable, 22b Abschnitt 2, zeichengleich:**

> **Registertext, Ersteintrag — Schreibregel für Sperrlistenpfade:**
> **(1)** Kein Programm im Repo schreibt an einen Pfad, der auf der Sperrliste steht oder für sie bestimmt ist. **(2)** Jeder Erzeuger einer solchen Datei schreibt **einmalig**: Existiert die Zieldatei bereits, bricht er ab (Rückgabewert ≠ 0), nennt Pfad und Hash der vorhandenen Datei und schreibt nichts. Er überschreibt nie, auch nicht mit identischem Inhalt. **(3)** Ein anderes Ziel nur durch ausdrückliches Argument; die Voreinstellung eines Erzeugers ist nie ein Pfad, der auf der Sperrliste steht. **(4)** Für `faltenplan.py main()`: Voreinstellung weg von `ergebnisse/faltenplan.json` (Sperrlistenpunkt 2) auf einen nicht gesperrten Pfad, und die Einmal-Schreibsperre nach (2). Beides vor jeder weiteren Änderung an `faltenplan.py`, insbesondere vor Z. 336.
>
> > ⚠️ **Präzisiert durch 36.5 (Fable 22c, TB-84, 22.09.2026):** „bricht er ab (Rückgabewert ≠ 0)" in (2) — der Wert ist **1**: der Erzeuger hat geprüft und einen Befund („Ziel existiert, Hash …"), nicht 2. Der Satz oben bleibt zeichengleich stehen.

**Fables Abwägung der drei Wege aus der Anfrage 22a, zeichengleich:**

> **Zu den drei Wegen:** (c) fällt nach A8 — eine Regel, die niemand ausführt, ist keine Wache; ihr sagt es selbst. (a) allein beseitigt den Fall, nicht die Klasse: Der neue Zielname landet, sobald er Abbild ist, selbst auf der Sperrliste — und `main()` überschreibt ihn beim nächsten Aufruf genauso. (b) allein lässt ein Programm stehen, dessen **Voreinstellung** eine gesperrte Datei ist, mit einer Sicherung davor; die Sicherung muss dann die Sperrliste kennen, und das ist ein zweiter Ort, an dem die Sperrliste steht.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* Zweck der Sperrliste („nichts Gesperrtes ist bewegt worden", Übergabe Abschnitt 5) und A8 (eine Wache ist, was jemand ausführt). Die Einmal-Schreibsperre braucht keine Sperrlistenkenntnis — sie schützt auch die Abbild-Datei, die noch nicht auf der Liste steht, und sie schützt gegen den Fall, den niemand vorausgesehen hat. 21b (3): Prüfungen wandern dorthin, wo geändert werden darf. Kein Ergebnis: Kein Inhalt einer Datei ist berührt; es geht darum, dass keiner berührt werden kann.

**Und sein Satz zur Härte der Sperre, zeichengleich:**

> *Warum „nie überschreiben, auch nicht mit identischem Inhalt":* Eine Sperre, die bei gleichem Inhalt durchlässt, muss den Inhalt vergleichen — und wer den Vergleich programmiert, entscheidet, was „gleich" heisst (Schlüsselreihenfolge, Zeilenende, `sort_keys`). Die Sperre ist stärker, wenn sie dümmer ist.

⭐ **Fables Tatsachennotiz, zeichengleich:**

> **Tatsachennotiz dazu:** `ergebnisse/faltenplan.json` (Hash `0e54ac5c…`) ist seit dem 14.09. unverändert, obwohl `faltenplan.py main()` seit demselben Tag bei jedem Aufruf dorthin schreibt; TB-72 und TB-80 haben eigene Belegskripte verwendet. Der Bestand hielt durch Übung, nicht durch Regel. Der Hash ist am 22.09. gemessen und stimmt.

**Tatsachennotiz (TB-84, gemessen vor dem Eintrag, `m2_sperrlisten_hash.txt`
— Fables Notiz wird nicht übernommen, sondern nachgemessen):**
`research/vorregistrierung/ergebnisse/faltenplan.json` hat SHA-256
`0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339`, mtime
14.09.2026 17:55, letzter berührender Commit `a2fcf01` (TB-30a, 14.09.2026) —
**keine** Änderung seit dem Ersteintrag, obwohl `faltenplan.py` selbst seither
geändert wurde (letzter Commit `76c20ec`, 21.09.2026, TB-80). Die Schreibstelle
in `main()` ist, nur gelesen: Z. 372 `ziel = os.path.join(_HIER, "ergebnisse",
"faltenplan.json")`, Z. 373 `with open(ziel, "w", …)`, Z. 374 `json.dump(…)` —
Voreinstellung ohne Argument, ohne Abfrage, ob die Datei besteht: genau der
Fall, den (2), (3) und (4) ausschliessen. Der Hash ist **nach** dem Eintrag
erneut gemessen und gleich (36.7). ⇒ Fables Notiz stimmt in jedem Wort: *Der
Bestand hielt durch Übung, nicht durch Regel.*

⚠️ **Was (4) heute bedeutet, ausdrücklich:** Die in 35.1 eingetragene
Umstellung von `faltenplan.py:336` auf den Bezeichner `JJJJ-MM-TT/JJJJ-MM-TT`
darf nach (4) **erst nach** der Voreinstellungs-Änderung und der
Einmal-Schreibsperre in `main()` kommen — das ist Schritt 3 nach Schritt 2 in
36.3. Bis dahin gilt weiter: `python3 faltenplan.py` wird nicht aufgerufen.

**Marke am alten Ort:** unter **Sperrliste Punkt 2** (Abschnitt 10), als
eingerückter Block **unter** der Tatsachennotiz aus Abschnitt 30 — diese bleibt
zeichengleich stehen. Dazu die Marke aus 36.5 direkt unter dem Registertext
oben, am „(Rückgabewert ≠ 0)" in (2).

### 36.2 Die Sperrlisten-Sonde — Ersteintrag

**Fable, 22b Abschnitt 2, zeichengleich:**

> **Registertext, Ersteintrag — Sperrlisten-Sonde:**
> Vor dem signierten Tag existiert ein Prüfskript, das für **jeden** Sperrlistenpunkt Pfad und Hash gegen den Registertext prüft und bei einer Abweichung mit Rückgabewert ≠ 0 endet und den Punkt nennt. Der Registertext der Sperrliste ist die Quelle; eine maschinenlesbare Fassung ist Abbild und wird von der Sonde selbst gegen den Registertext geprüft (Bauart 33.3). Die Sonde läuft (a) als Nachweis vor dem Tag, (b) im Laufwrapper vor `auswertung.py`, (c) am Ende jedes Auftrags, der Sperrlisten-nahen Code berührt. Ein Sperrlistenbruch, den die Sonde findet, ist eine Tatsachennotiz — nie eine stille Reparatur.
>
> > ⚠️ **Berichtigt durch 36.5 (Fable 22c, TB-84, 22.09.2026):** „mit Rückgabewert ≠ 0 endet und den Punkt nennt" lies „mit Rückgabewert 1 endet und den Punkt nennt; kann ein Punkt nicht geprüft werden (Datei fehlt, Registertext nicht lesbar), endet sie mit 2 und nennt ihn". Der Satz oben bleibt zeichengleich stehen; die drei Ausgänge gelten nach 36.5 für jede Sonde und jede Wache.
>
> > ⚠️⚠️ **Ergänzt durch 37.3 (Fable 22g, TB-87, 22.09.2026):** „bei einer Abweichung … endet" — **was ein Befund bedeutet, hängt vom Tag ab.** Vor dem signierten Tag ist ein Befund `1` zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz), und wird durch ein neues Abbild unter neuem Namen geschlossen; **nach** dem Tag ist er ein Sperrlistenbruch und wird nach 10.1 behandelt (Amendment, Lauf von vorn). Der Satz oben bleibt zeichengleich stehen.

**Fables Unsicherheit dazu, 22b, zeichengleich:**

> **Unsicher:** ob es bereits ein Prüfskript für die Sperrliste gibt (etwa nach dem Muster `snapshot.py --pruefen`) — dann ist Schritt 1 eine Erweiterung, kein Neubau; ihr seht es im Repo.

⭐⭐ **Drei Tatsachennotizen des steuernden Chats (Anfrage 22b, 22.09.2026,
07:35), von TB-84 vor dem Eintrag nachgemessen (M3–M5, `m3_snapshot_ausgaenge.txt`,
`m4_herkunft_listen.txt`, `m5_vt_in_listen.txt`, HEAD `4bbd720`).** Sie waren
Fable mit `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-22b_sonde_bestand.md`
vorgelegt; seine Antwort (22c) liegt vor und ist in 36.5 und 36.6 eingetragen:

> **(a) Das Muster existiert, die Sache nicht.** `shared/snapshot.py --pruefen`
> (1306 Zeilen) prüft **Datenstände**, nicht die Sperrliste, und hat **drei**
> Ausgänge — gemessen im Kopf der Datei, Z. 217–219: `0` *„in Ordnung: gezogen,
> oder `--pruefen` findet den Stand unveraendert"*, `1` *„Befund: `--pruefen`
> findet den Snapshot VERAENDERT"*, **`2` *„NICHT PRUEFBAR / abgebrochen"***.
> Begründung ebendort (Z. 221–224), wörtlich: *„Die 2 ist der Grund, warum es
> sie gibt. In TB-45 haben zwei Wachen "bestanden" gemeldet, ohne etwas gemessen
> zu haben - ein gescheiterter Aufruf und ein leeres Ergebnis sahen gleich aus.
> Hier nicht: wer nicht messen konnte, sagt es mit einem eigenen Wert."*
> ⚠️ Der Registertext oben sagt nur „Rückgabewert ≠ 0" und unterscheidet die
> beiden roten Fälle nicht — nach `A2` („konnte nicht messen" ist ein eigenes
> Ergebnis, nicht grün und nicht rot) und `A8` sind sie verschieden.
> **Frage 1 an Fable** (drei Ausgänge?) — ⭐ **beantwortet: ja, in 36.5.**
>
> **(b) `herkunft.py` scheidet als Ort aus.** `research/vorregistrierung/herkunft.py`
> (260 Zeilen): sein `--pruefen` meldet die vier Verankerungen (append-only-Kette,
> GPG, OpenTimestamps), nicht Sperrlisten-Hashes — **und die Datei steht selbst
> auf der Sperrliste** (Punkte **11** `herkunft.py::register()` und **12**
> `herkunft.py::datenstand()`, gemessen M1: 14 Punkte in Abschnitt 10). Die
> Sonde kann dort nicht eingebaut werden, ohne gesperrten Code zu öffnen; sie
> braucht eine **eigene Datei**. ⇒ Schritt 1 in 36.3 ist ein **Neubau nach
> vorhandenem Muster**, keine Erweiterung. ⭐ Fable 22c, Abschnitt 0: *„angenommen, und es bestätigt die Bauart aus 22b (Sonde als eigene, nicht gesperrte Datei)"*.
>
> **(c) ⚠️ Zwei maschinenlesbare Listen liegen bereits in `herkunft.py`** und
> decken sich **nicht** mit dem Registertext: `EINGEFROREN` (Z. 57, **zehn**
> Einträge: `registerdaten.py`, `faltenplan.py`, `benchmark.py`, `kennzahlen.py`,
> `auswertung.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`,
> `ergebnisse/messgroessen.json`, `ergebnisse/faltenplan.json`,
> `ergebnisse/benchmark_drawdowns.json`) und `SPERRLISTE_DATEIEN` (Z. 66,
> **fünf** Muster: `shared/messkette.py`, `shared/zuteilung.py`,
> `strategies/*/equity_simulation.py`, `strategies/*/multi_symbol_optimise.py`,
> `strategies/*/multi_symbol_walk_forward.py`) gegen **14** Registerpunkte (M1).
> Gemessen (M5, 0 Treffer, Positivkontrolle `faltenplan.json` 1 Treffer):
> `ergebnisse/benchmark_drawdowns_vt.json` (Sperrlisten-Hash `4549395f…`) steht
> in **keiner** der beiden Listen, ebenso wenig die beiden Universumsdateien aus
> Punkt 8 (`config/top25_symbols.txt`, `config/sp500_top150.txt`); umgekehrt
> führt `EINGEFROREN` Dateien, die der Registertext nicht als eigene Punkte nennt
> (`kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`,
> `ergebnisse/messgroessen.json`). ⛔ **Nicht bewertet** — ob `EINGEFROREN`
> überhaupt als Sperrlisten-Abbild gemeint war oder für Abschnitt 0 („vor dem
> Lauf geschrieben und eingefroren"), steht nirgends. Genau der Zustand, gegen
> den die Sonde nach 36.2 schützen soll — eine maschinenlesbare Fassung, die vom
> Registertext abweicht und nie dagegen geprüft wurde —, besteht damit heute
> schon. **Frage 2 an Fable** (welche Liste wird Abbild?) — ⭐ **beantwortet:
> keine, in 36.6**; die Tatsachennotiz zu den beiden Listen steht bei Fable aus.

⭐ Die Antwort auf Fables Unsicherheit lautet damit, gemessen: **Das Muster
gibt es, die Sache nicht.** Die Sonde selbst ist Schritt 1 in 36.3 und
**nicht** freigegeben.

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**, als
Hinweisblock, zusammen mit der Marke aus 36.6.

### 36.3 Die Reihenfolge der Handwerksschritte

**Fable, 22b Abschnitt 3, zeichengleich — Vorsatz und die vier Schritte:**

> Alle mit Betreiberfreigabe; die Reihenfolge ist Verfahren, weil jeder Schritt den nächsten absichert:
>
> 1. **Sperrlisten-Sonde** schreiben und einmal laufen lassen — Nachweis, dass heute alles stimmt (der Nullpunkt).
> 2. **`faltenplan.py main()`:** Voreinstellung ändern, Einmal-Schreibsperre einbauen. **Mutationsprobe:** `main()` gegen eine Kopie von `faltenplan.json` am neuen Zielpfad aufrufen → muss abbrechen; Sonde danach → grün.
> 3. **Erst jetzt** Z. 336 (Bezeichner der Bestätigungsperiode, 22a). Prüfen über `main()` ist ab jetzt ungefährlich; Sonde danach → grün.
> 4. Abbild-Datei, Faltenplan-Sonde (33.3), Hash auf die Sperrliste — wie geplant; der Erzeuger des Abbilds unterliegt der Schreibregel von Anfang an.

**Fables Satz dazu, zeichengleich:**

> Wer Schritt 3 vor Schritt 2 macht, hat genau den Fall, den ihr beschreibt. Deshalb steht die Reihenfolge hier und nicht nur im Auftrag.

⛔ **Eingetragen, ausdrücklich:** Alle vier Schritte brauchen
**Betreiberfreigabe**. Am 22.09.2026, 07:40 (Erstellung des Auftrags TB-84)
ist **keine** erteilt; TB-84 hat keine erhalten und keinen der vier Schritte
begonnen (36.7). Die Reihenfolge ist **Verfahren**, nicht Empfehlung: Schritt 3
(Z. 336, 35.1) ist ohne Schritt 2 genau die in Anfrage 22a gemessene Falle, und
Schritt 2 ohne Schritt 1 hat keinen Nullpunkt, gegen den seine Mutationsprobe
gemessen würde. Der Erzeuger der Abbild-Datei (Schritt 4, 33.3/35.2)
unterliegt der Schreibregel 36.1 von seinem ersten Aufruf an; seine Ausgänge
regelt 36.5, das Abbild der Sperrliste 36.6.

**Marke am alten Ort:** in **35.1**, direkt beim Absatz über den heutigen
unzulässigen Bezeichner (*„Die Umstellung ist Handwerk mit eigener Freigabe"*)
— Verweis, dass die Umstellung nach 36.3 erst nach Schritt 2 kommt.

### 36.4 Tatsachennotiz zu 21.4 — die ⚠️-Markierung ohne Erklärung

**Fable, 22b Abschnitt 1 (Kenntnisnahme zu Punkt 1 der Anfrage 22a),
zeichengleich:**

> Die ⚠️-Markierung in 21.4 hat keinen Text. Dann ist sie eine Markierung ohne Bedeutung, und das gehört als Tatsachennotiz zu 21.4: „⚠️ bei `elliott_wave`, Spalte Bestätigung ab, trägt keine Erklärung; nicht als Beleg verwendbar." Sonst nimmt sie in einem Jahr jemand für einen Vorbehalt, den es nie gab.

**Tatsachennotiz zu 21.4 (TB-84, 22.09.2026; Messung `m1_bestaetigung_ab.txt`
aus TB-83, unverändert):** Die Zelle bei `elliott_wave` in der Spalte
„Bestätigung ab" lautet wörtlich `⚠️ **2026-01-01**`; 21.4 trägt keinen Satz,
der die Markierung begründet, und kein anderer Abschnitt des Registers
erklärt sie. **⚠️ bei `elliott_wave`, Spalte Bestätigung ab, trägt keine
Erklärung; nicht als Beleg verwendbar.**

⭐ **Rücknahme des steuernden Chats, eingetragen:** Die Deutung aus
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21g_berichtigung_und_bestaetigungsperiode.md`
Punkt 3 — zeichengleich: **(Möglicherweise ist das der Grund für die ⚠️-Markierung, die 21.4 ausgerechnet bei `elliott_wave` in der Spalte „Bestätigung ab" trägt.)** — ist **zurückgezogen.** Sie war eine
Vermutung und taugt nicht als Beleg; Fable hatte in 22a ausdrücklich gebeten,
den ganzen Eintrag vorzulegen, bevor jemand sie als Beleg nimmt (35.1). Die
Tabellenzeile in 21.4 bleibt zeichengleich stehen, **samt `⚠️`** — die
Markierung wird nicht entfernt, sondern erklärt: sie erklärt nichts.

**Marke am alten Ort:** ⚠️ **direkt in 21.4**, als Zeile unter der Tabelle —
die Tabellenzeile selbst bleibt zeichengleich, samt `⚠️`.

### 36.5 ⭐⭐ Drei Ausgänge für jede Sonde und jede Wache — Ersteintrag, und die Berichtigung zu 36.2

⚠️ **Fable berichtigt hier seinen eigenen Text aus 22b (36.2), nachdem ihm
`shared/snapshot.py` vorgelegt war (Anfrage 22b, Frage 1; Messung M3).**
*Seine Begründung, 22c Frage 1, zeichengleich:*

> Mein „Rückgabewert ≠ 0" war zu grob, und der Kopf von `snapshot.py` sagt genau, warum: Ein gescheiterter Aufruf und ein Befund sahen in TB-45 gleich aus. A2 verlangt, dass „konnte nicht messen" ein eigenes Ergebnis ist; ein Rückgabewert, der Befund und Nichtprüfbarkeit zusammenlegt, ist keine Wache im Sinn von A8, weil niemand am Wert erkennen kann, ob gemessen wurde.

**Fable, 22c Frage 1, zeichengleich — Registertext und Berichtigung:**

> **Registertext, Ersteintrag — Ausgänge von Sonden und Wachen:**
> Jede Sonde und jede Wache des Verfahrens (Sperrlisten-Sonde, Faltenplan-Sonde nach 33.3, Einmal-Schreibsperre der Erzeuger, Wache nach 29.4, Laufwrapper) endet mit genau einem von drei Rückgabewerten, Bauart `snapshot.py --pruefen`: **0** = geprüft und in Ordnung; **1** = geprüft und **Befund** (Abweichung, Verweigerung, Abbruch nach Regel); **2** = **nicht prüfbar** (Eingabe fehlt, Quelle nicht lesbar, Aufruf gescheitert). Ein Wrapper behandelt 1 und 2 verschieden: 1 ist eine Tatsachennotiz mit dem genannten Punkt; 2 ist kein Ergebnis und darf nirgends als „bestanden" oder „nicht bestanden" geführt werden. Kein Aufruf endet mit 0, ohne dass gemessen wurde.
>
> **Berichtigung zu 22b, Sperrlisten-Sonde:** „mit Rückgabewert ≠ 0 endet und den Punkt nennt" lies „mit Rückgabewert 1 endet und den Punkt nennt; kann ein Punkt nicht geprüft werden (Datei fehlt, Registertext nicht lesbar), endet sie mit 2 und nennt ihn".
>
> > ⚠️ **Präzisiert durch 37.1 (Fable 22d, TB-87, 22.09.2026):** Die Sperrlisten-Sonde meldet **je Punkt je Bestandteil** — für jeden genannten Pfad 0 oder 1, für jeden nicht messbaren Bestandteil 2 unter Nennung des Wortlauts; der Punkt ist 1, wenn ein Bestandteil 1 ist, sonst 2, wenn einer 2 ist, sonst 0. Am Tag: kein Pfad-Bestandteil mit 1, jede 2 mit Tatsachennotiz. Der Text oben bleibt zeichengleich stehen.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* A2 und A8, im Register vorhanden; der Vorfall TB-45, im Kopf von `snapshot.py` dokumentiert. Kein Ergebnis.

**Und sein Zusatz zur Einmal-Schreibsperre (36.1 (2)), zeichengleich:**

> *Zur Einmal-Schreibsperre:* Der Erzeuger, der wegen vorhandener Zieldatei nicht schreibt, endet mit **1** — er hat geprüft und einen Befund („Ziel existiert, Hash …"). Nicht mit 2: Er konnte prüfen. Das ist die Wache, die ihre Arbeit tut; der Wert 1 sagt es dem Aufrufer.

**Tatsachennotiz (TB-84, M3, `m3_snapshot_ausgaenge.txt`):** Die Bauart, auf
die der Registertext verweist, ist im Kopf von `shared/snapshot.py` Z. 217–219
(`0` in Ordnung · `1` Befund · `2` NICHT PRUEFBAR / abgebrochen) mit der
Begründung Z. 221–224 (TB-45: *„wer nicht messen konnte, sagt es mit einem
eigenen Wert"*) — gemessen, nur gelesen. Der Registertext dehnt sie auf **jede**
Sonde und Wache des Verfahrens aus; keine davon ist gebaut (36.7).

**Marken am alten Ort — zwei, beide in diesem Abschnitt:** in **36.2**, direkt
unter dem Registertext, am Satz *„mit Rückgabewert ≠ 0 endet und den Punkt
nennt"* — **berichtigt durch 36.5**, der Satz bleibt zeichengleich stehen; und
in **36.1**, direkt unter dem Registertext, am *„bricht er ab (Rückgabewert
≠ 0)"* in (2) — dasselbe, der Wert ist **1**.

### 36.6 Das Abbild der Sperrliste ist eine neue Datei — Ersteintrag

**Fable, 22c Frage 2, zeichengleich:**

> **Registertext, Ersteintrag — Abbild der Sperrliste:**
> Das Abbild der Sperrliste ist eine **eigene, neue Datei** (Handwerk: Name, Form), die genau die Punkte des Registerabschnitts 10 mit Pfad und Hash trägt — nicht mehr, nicht weniger (Bauart 33.3). Sie wird einmalig geschrieben (Schreibregel 22b); jede Fortschreibung der Sperrliste vor dem Tag erzeugt ein neues Abbild unter neuem Namen, das alte bleibt. Das aktuelle Abbild steht selbst mit Hash im Register. Die Sperrlisten-Sonde prüft (i) jeden Punkt des Abbilds gegen die Datei im Repo und (ii) das Abbild gegen den Registertext von Abschnitt 10; weicht das Abbild vom Registertext ab, ist das ein Befund (1), kein Anlass zur Anpassung des Abbilds ohne Registereintrag.
>
> `herkunft.py` `EINGEFROREN` (Z. 57) und `SPERRLISTE_DATEIEN` (Z. 66) sind **nicht** das Abbild der Sperrliste und werden nicht dazu. Beide erhalten eine Tatsachennotiz zu Abschnitt 10: Was sie sind, wer sie liest, was daraus entsteht, und dass sie mit dem Registertext an fünf Stellen nicht übereinstimmen (zwei Dateien fehlen, drei stehen zusätzlich).
>
> > ⚠️ **Ergänzt durch 37.2 (Fable 22d, TB-87, 22.09.2026):** Das Abbild führt **zwei Gruppen** — die **Punkte** des Abschnitts 10 und die **bestimmten** Pfade (heute `ergebnisse/benchmark_drawdowns_vt.json`); die Sonde prüft beide gleich und weist die Gruppe aus; am Tag ist die zweite Gruppe leer. Der Satz oben bleibt zeichengleich stehen.
>
> > ⚠️⚠️ **Ergänzt durch 37.3 (Fable 22g, TB-87, 22.09.2026):** „jede Fortschreibung … erzeugt ein neues Abbild unter neuem Namen, das alte bleibt" — ein Befund `1` **vor** dem signierten Tag ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz), und wird durch ein **neues** Abbild geschlossen, nie durch Anpassung des alten; **nach** dem Tag ist derselbe Befund ein Sperrlistenbruch nach 10.1. Das letzte Abbild vor dem Tag trägt die Hashes des Tag-Commits. Erster Anwendungsfall: `faltenplan.py` in TB-86 (37.3).
>
> > ⭐ **Ergänzt durch 40.8 (e) (Fable 24a, TB-96, 24.09.2026):** Die Sonde liest **alle drei Gruppen** — die Punkte des Abschnitts 10, die Gruppe „bestimmt" (37.2) und `herkunft.py::EINGEFROREN` (39.7) — **aus dem Abbild**, nicht aus ihrem eigenen Code; „Eine Gruppe, die im Code der Sonde steht, ist ein Literal in einer Wache". Vollzug TB-97, mit Gegenprobe. Der Satz oben bleibt zeichengleich.

**Seine drei Gründe, zeichengleich:**

> *Quelle des Grundes — drei, alle aus dem Bestand:* **(1)** Beide Listen liegen in `herkunft.py`, das mit Punkt 11/12 auf der Sperrliste steht. Ein Abbild, das mit der Sperrliste wachsen muss (Abbild-Datei, Erzeuger, Sonde kommen noch hinzu), kann nicht in einer Datei liegen, die nicht geöffnet werden darf. **(2)** Sie weichen heute vom Registertext ab, und ihr Zweck ist nirgends registriert — eine Liste, von der man nicht weiss, was sie darstellen soll, kann nicht zum Abbild von etwas erklärt werden. **(3)** Der Registertext ist die Quelle (30.2 (2) sinngemäss): Ein Abbild wird aus ihm gebildet und gegen ihn geprüft, nicht aus einer vorhandenen Datei übernommen, weil sie schon da ist. Kein Ergebnis.

**Was der Fund aus 36.2 (c) bedeutet und was nicht — Fable, zeichengleich:**

> **Was der Fund bedeutet, und was er nicht bedeutet:** Der Zustand „maschinenlesbare Fassung weicht vom Registertext ab, und niemand hat sie geprüft" besteht — ihr sagt es richtig — heute schon. Er ist **kein Sperrlistenbruch**: Die Dateien selbst sind unverändert (Hashes stimmen). Er ist eine **Lücke im Nachweis**, wenn `herkunft.py` aus diesen Listen die Hashes bildet, die in `herkunft.json` als Herkunft des Laufs stehen — dann fehlen dort `benchmark_drawdowns_vt.json` und die beiden Universumsdateien, und drei Dateien stehen drin, die kein Sperrlistenpunkt sind. Ob das so ist, weiss ich nicht — **das ist die Messung, die ich brauche:**

⚠️⚠️ **Die Tatsachennotiz zu den zwei Listen (`EINGEFROREN`,
`SPERRLISTE_DATEIEN`), die der Registertext oben verlangt, wird in diesem
Abschnitt NOCH NICHT geschrieben.** Fable hat dafür eine Messung erbeten,
zeichengleich:

> **Nur das Ob:** Welche Funktionen von `herkunft.py` lesen `EINGEFROREN` und `SPERRLISTE_DATEIEN`, und in welche Ausgabe (Datei, Feld) gehen die daraus gebildeten Hashes ein? Läuft `register()` oder `datenstand()` (Punkt 11/12) über diese Listen?

⭐ Die Messung ist am 22.09.2026 vom steuernden Chat gemacht und Fable mit
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-22c_herkunft_gemessen.md` vorgelegt;
**seine Tatsachennotiz folgt** und wird als eigener Eintrag eingetragen.
Eingetragen ist hier nur, **dass** sie aussteht — mit dieser Fundstelle. Die
beiden Listen selbst bleiben unberührt: `herkunft.py` steht auf der Sperrliste
(Punkte 11, 12), und ob es vor dem Tag geöffnet werden muss, entscheidet Fable
nach der Messung — 22c, zeichengleich:
„**Meine Linie dazu, vorab und nicht als Entscheidung:** Nach 21b (3) nicht öffnen, wenn die Sperrlisten-Sonde die Lücke schliesst".

**Fables Unsicherheit, 22c, zeichengleich:**

> **Unsicher:** ob Abschnitt 10 in einer Form vorliegt, aus der ein Programm Pfad und Hash je Punkt zuverlässig lesen kann (Prüfung (ii) der Sonde). Wenn nicht, ist der Abgleich Abbild↔Registertext eine Prüfung mit Beleg im Auftrag statt einer Codezeile — Handwerk, aber ihr müsst es wissen, bevor ihr die Sonde beauftragt.

⚠️ Auch dazu liegt Fable eine Messung vor (Anfrage 22c Abschnitt 3,
`docs/projektfuehrung/VORARBEIT_sperrlisten_sonde.md`, lesend, HEAD `fdb181a`);
sie ist hier **nicht** eingetragen — sie gehört zur ausstehenden Antwort.

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**, zusammen
mit der Marke aus 36.2.

### 36.7 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Sperrlisten-Sonde schreiben** (Schritt 1 in 36.3) — keine Freigabe; ihre Ausgänge sind seit 36.5 festgelegt, ihr Gegenstand (das Abbild) seit 36.6 | Betreiber |
| ⛔ | **`faltenplan.py main()` absichern** — Voreinstellung, Einmal-Schreibsperre (Ausgang 1 nach 36.5), Mutationsprobe (Schritt 2) — keine Freigabe | Betreiber |
| ⛔ | **`faltenplan.py:336` umstellen** (Schritt 3) — nach 36.1 (4) und 36.3 **erst nach Schritt 2** | Betreiber, nach Schritt 2 |
| ⛔ | **Abbild-Datei der Sperrliste (36.6), Abbild des Faltenplans, Faltenplan-Sonde (33.3), Hash auf die Sperrliste** (Schritt 4) | eigene Aufgabe, Betreiberfreigabe (33.5) |
| ⛔ | ⚠️⚠️ **`python3 faltenplan.py` ausführen** — in dieser Sitzung **nicht geschehen**; der Hash von `ergebnisse/faltenplan.json` ist vor **und** nach der Arbeit `0e54ac5c…` (`m2_sperrlisten_hash.txt`). Ein Hashbruch wäre nach 36.2 eine Tatsachennotiz, nie eine stille Reparatur | — |
| ⛔ | **`herkunft.py` anfassen** — auch nicht die beiden Listen aus 36.2 (c); die Datei steht selbst auf der Sperrliste (Punkte 11, 12) | Fable (Tatsachennotiz), dann Betreiber |
| ⛔ | **Die Tatsachennotiz zu `EINGEFROREN` und `SPERRLISTE_DATEIEN` schreiben** (36.6) — nur eingetragen, dass sie aussteht | Fable (Anfrage 22c) |
| ⛔ | **Irgendeine `.py` ändern** | — |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (Beleg M6); die drei Sperrlisten-Hashes `0e54ac5c…`, `a163c498…`, `4549395f…` unverändert | — |
| ⚠️ | **Offen bei Fable:** die Tatsachennotiz zu den zwei Listen (36.6); die Frage der Anfrage 22c, ob die Sonde auch Pfade prüft, die für die Sperrliste **bestimmt** sind (`benchmark_drawdowns_vt.json`, 21.9/23.7 — von 36.1 (1) gedeckt, vom Wortlaut in 36.2 „für jeden Sperrlistenpunkt" nicht); seine Unsicherheit aus 22c, ob Abschnitt 10 maschinenlesbar ist (Messung vorgelegt); seine Unsicherheit aus 35.5 (weitere Fundstellen des Bezeichners, in Anfrage 22a Punkt 2 gemessen) | Fable |
| ⚠️ | **Offen beim Betreiber:** die Freigabe für die vier Schritte aus 36.3 — keine erteilt | Betreiber |

*Dieser Abschnitt ist rein additiv: Er trägt vier Ersteinträge, eine
Reihenfolge und eine Tatsachennotiz des Verfahrensprüfers zeichengleich ein,
darunter eine Berichtigung, die er am selben Tag an seinem eigenen Text
vorgenommen hat; setzt sechs Marken am alten Ort; hält drei nachgemessene
Tatsachen zum Bestand und das Ausstehende fest — und entfernt nichts. Gebaut
wird nichts.*

## 37. Die Sonde meldet je Bestandteil, das Abbild führt zwei Gruppen, was ein Befund `1` bedeutet, hängt vom Tag ab, die Tatsachennotiz zu den zwei Listen in `herkunft.py` und der Ort registrierter Werte (Fable 22d und 22g, TB-87, 22.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34 bis 36. Fünf Einträge — zwei
Präzisierungen bzw. Ergänzungen zu 36.5 und 36.6 (37.1, 37.2), eine Ergänzung
zu 36.2/36.6 (37.3), eine Tatsachennotiz zu Abschnitt 10 (37.4) und ein
Ersteintrag (37.5) —, alle Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22d_wert_ohne_ort.md` (Antwort auf
die Anfragen 22c und 22d) und
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22g_sonde_vor_dem_tag.md` (Antwort
auf die Meldung des steuernden Chats zu TB-86 und zum Sondenbefund an
Sperrlistenpunkt 2). Auftrag `docs/auftraege/MAC_TB-87_register_37.md` (Stufe I,
Punkt 4 aus `PLAN_VOR_DEM_TAG.md`); Messungen `docs/belege/TB-87/` (M1–M6),
M1–M4 **vor** dem Eintrag gemessen, HEAD `40aa715`. ⛔ **Keine `.py` geändert,
kein neues Abbild, keine Sonde angepasst, keine Werte verschoben** — 37.6.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (36.5; 36.6 zweimal;
36.2; Überschrift von Abschnitt 10; Sperrlistenpunkte 7 und 9). Die alten Sätze
bleiben zeichengleich; `git diff --numstat` auf dieses Register zeigt für TB-87
in der zweiten Spalte `0`. ⚠️ Die Marken in Abschnitt 10 stehen als eingerückte
`>`-Zeilen **ohne Leerzeile** unter dem Punkt — so liest die Sperrlisten-Sonde
sie als Notiz und nicht als Punkttext (`shared/sperrlistensonde.py`
`lies_abschnitt_10`, R2); die Sonde ist vor und nach dem Eintrag lesend
gelaufen, Prüfung (ii) beide Male `0`, Listentext wie bei Erzeugung (37.6).

⚠️ **Die Fable-Texte stehen hier in voller Quellform**, auch wo der Auftrag sie
gekürzt zitiert (der Zusatz „, Vorschlag" in den Kopfzeilen von 22d Abschnitt 1
und 22g; „Folge für `herkunft.py`, Entscheidung:"; zwei Begründungen mit „…"):
Eingetragen wird der Quellwortlaut, nicht die Kurzform.

### 37.1 Präzisierung zu 36.5 — die Sonde meldet je Punkt je Bestandteil

**Fable, 22d Abschnitt 1, zeichengleich:**

> **Präzisierung zu 36.5 (Sonden-Ausgänge), Vorschlag:** Die Sperrlisten-Sonde meldet **je Punkt je Bestandteil**: für jeden genannten Pfad 0 oder 1 (Hash gegen Abbild), für jeden nicht messbaren Bestandteil 2 unter Nennung des Wortlauts. Der Gesamtwert eines Punktes ist 1, wenn ein Bestandteil 1 ist; sonst 2, wenn ein Bestandteil 2 ist; sonst 0. Der Gesamtwert des Laufs entsprechend. Am Tag gilt: Kein Pfad-Bestandteil darf 1 sein, und jeder Bestandteil mit 2 hat eine Tatsachennotiz, die sagt, wie er stattdessen geprüft wurde (Lesen, Beleg im Auftrag) — oder der Punkt wird bis zum Tag so nachgetragen, dass er messbar ist.

**Fables Grund, 22d Abschnitt 1, zeichengleich:**

> **Eine Präzisierung zur Sonde, damit die `2` nicht mehr verdeckt als sie zeigt:** Ein Punkt wie 14 („`auswertung.py` … Docstring") hat einen messbaren Teil (der Datei-Hash) und einen unmessbaren (der Docstring-Anteil). Eine Sonde, die den ganzen Punkt mit `2` meldet, macht den messbaren Teil unsichtbar.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* A2 (nicht prüfbar ist ein eigenes Ergebnis — aber je Sache, nicht je Punkt) und 22c. Kein Ergebnis.

**Tatsachennotiz (TB-87, M1, `m1_sonde_je_bestandteil.txt`):** Die Sonde aus
TB-85 (`shared/sperrlistensonde.py`) **gibt bereits je Bestandteil aus** — im
Nullpunkt-Lauf `docs/belege/TB-85/nullpunkt.txt` zeigt Punkt 1 in einer Zeile
den Datei-Hash (`research/vorregistrierung/registerdaten.py`, `gleich`,
`141fa14b…`) und in der nächsten daneben den unmessbaren Teil (`-> nennt
Nicht-Dateibezogenes - nicht messbar: …`). ⚠️ **Was ihr fehlt, ist der
Rückgabewert je Bestandteil:** Sie meldet den Ausgang je Punkt (Punkt 1 steht
auf `2 NICHT PRUEFBAR`, obwohl sein einziger Pfad `gleich` ist) und einmal je
Lauf. Genau das ist der Fall, den Fables Grund beschreibt — der messbare Teil
verschwindet im Ausgang hinter dem unmessbaren. Das nachzuziehen ist Handwerk
mit eigener Freigabe, **nicht** dieser Eintrag.

**Marke am alten Ort:** in **36.5**, direkt unter dem Registertext.

### 37.2 Ergänzung zu 36.6 — das Abbild führt zwei Gruppen

**Fable, 22d Abschnitt 2, zeichengleich:**

> **Ergänzung zu 36.6 (Abbild der Sperrliste):** Das Abbild führt zwei Gruppen: die **Punkte** des Abschnitts 10 und die **bestimmten** Pfade — Dateien, die das Register für die Sperrliste vorsieht, deren Vollzug aber aussteht (heute: `ergebnisse/benchmark_drawdowns_vt.json`, 21.9/23.7). Die Sonde prüft beide Gruppen gleich (Hash gegen Abbild) und weist die Gruppe im Bericht aus. **Am Tag ist die zweite Gruppe leer:** Jeder bestimmte Pfad hat bis dahin seinen Punkt in Abschnitt 10, oder das Register sagt, warum nicht.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* Schreibregel 22b (1) („oder für sie bestimmt ist") — was die Schreibregel schützt, muss die Sonde sehen; sonst ist der Schutz eine Regel ohne Wache (A8). Und die Sperrliste ist am Tag vollständig oder sie ist keine. Kein Ergebnis.

**Tatsachennotiz (TB-87, M1):** Das Abbild `sperrliste_abbild_2026-09-22.json`
(`6a1b732e…`) führt heute die Punkte; die Sonde **nennt** den bestimmten Pfad
`ergebnisse/benchmark_drawdowns_vt.json` am Ende ihres Berichts mit Hash
`4549395f…`, **prüft ihn aber nicht** — ihr eigener Wortlaut: „Bestimmt, nicht
eingetragen (kein Punkt des Abschnitts 10; nicht geprueft, nur genannt)".
Der Unterschied zum Registertext oben (beide Gruppen gleich prüfen, Gruppe
ausweisen) ist Handwerk mit eigener Freigabe; hier nur festgehalten.

> ⭐ **Gruppenwechsel und Vollzug (39.3/39.2, Fable 23a/23b, TB-94,
> 23.09.2026):** Die Gruppe „bestimmt" **wechselt** von
> `ergebnisse/benchmark_drawdowns_vt.json` auf die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`) —
> und deren Pfad steht seit 39.2 in Sperrlistenpunkt 4. **Nach dem
> Registertext ist die Gruppe damit leer.** `_vt.json` und `_tb72.json` kommen
> nicht auf die Liste (Tatsachennotizen in 39.3). ⚠️ Die Sonde führt die
> Gruppe als feste Konstante und nennt weiter `_vt.json` mit „Vollzug steht
> aus" (39.3, Ausgabe in 39.9); das zu ändern ist Handwerk mit eigener
> Freigabe.

> ⭐ **Die Gruppen kommen aus dem Abbild (40.8 (e), Fable 24a, TB-96,
> 24.09.2026):** Dass die Sonde die Gruppe „bestimmt" als feste Konstante führt
> (`BESTIMMT_NICHT_EINGETRAGEN`), ist nach Fable „ein Befund, vor dem Tag zu beheben"
> — nicht mehr Handwerk ohne Frist. Die Sonde liest alle drei Gruppen aus dem
> Abbild; das Abbild führt „bestimmt" heute leer (39.3). Gegenprobe: Abbild mit
> erfundenem „bestimmt"-Pfad ⇒ Sonde meldet ihn. TB-97.

**Marke am alten Ort:** in **36.6**, direkt unter dem Registertext.

### 37.3 ⭐⭐ Ergänzung zu 36.2/36.6 — was ein Befund `1` bedeutet, hängt vom Tag ab

⚠️ **Das ist die Lücke, die TB-86 sichtbar gemacht hat:** Die Sonde meldet
seit TB-86 an Sperrlistenpunkt 2 den Befund `1` — und bis hier stand nirgends,
ob das ein Sperrlistenbruch ist.

**Fable, 22g, zeichengleich:**

> **Ergänzung zu 36.2/36.6, Vorschlag:** Ein Befund 1 der Sperrlisten-Sonde **vor dem signierten Tag** ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz); er wird durch ein **neues Abbild unter neuem Namen** geschlossen, nie durch Anpassung des alten. Ein Befund 1 **nach dem Tag** ist ein Sperrlistenbruch und wird nach 10.1 behandelt (Amendment, Lauf von vorn). Das **letzte Abbild vor dem Tag** wird nach der letzten Codeänderung erzeugt, trägt die Hashes des Tag-Commits und steht selbst mit Hash im Register; der Tag setzt voraus, dass die Sonde gegen dieses Abbild 0 liefert (oder 2 mit Tatsachennotiz nach 22d).

**Fables Grund, 22g, zeichengleich:**

> **Der Satz, der fehlt — und den der Befund verlangt:** Die Sperrliste sagt „**ab dem signierten Tag** sind unveränderlich". Vor dem Tag ändern sich Sperrlistenpfade planmässig (TB-86 heute, Z. 336 morgen, die Werte-Module nach 22d). Die Sonde kann diesen Unterschied nicht kennen; sie meldet 1, und was 1 **bedeutet**, hängt vom Datum ab. Das gehört ins Register, sonst liest jemand den heutigen Befund als Bruch — oder, schlimmer, einen Bruch nach dem Tag als „planmässig".

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* der Wortlaut von Abschnitt 10 („ab dem signierten Tag") und 36.6 (Abbild einmalig, neu statt angepasst). Kein Ergebnis.

⭐ **Und sein Satz zur Sonde, 22g, zeichengleich:**

> *„Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde."*

(Aus 22g, Absatz „Punkt 2b — ja, genauso", voller Absatz:)

> **Punkt 2b — ja, genauso:** Sperrlistenpunkt 2 nennt zwei Pfade; `faltenplan.py` hat sich durch beauftragte Änderung bewegt; die Sonde meldet 1 und repariert nichts — richtig, denn das Abbild trägt den alten Hash, und ein Abbild wird nach 36.6 nicht angepasst, sondern **neu** geschrieben, unter neuem Namen, das alte bleibt. Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde.

**Sein Hinweis zum Handwerk, ausdrücklich nicht Verfahren, zeichengleich:**

> *Handwerk daraus, nicht Verfahren:* Nicht nach jeder Änderung ein neues Abbild ziehen, sondern nach Bündeln (etwa nach 2+3 zusammen, nach 6, vor 11) — jedes Abbild bleibt ohnehin liegen. Wie viele es werden, ist gleichgültig; dass das letzte zum Tag-Commit passt, ist alles.

⭐⭐ **Tatsachennotiz — der erste Anwendungsfall (TB-87, M2,
`m2_faltenplan_hash.txt`):** TB-86 hat `research/vorregistrierung/faltenplan.py`
**beauftragt und freigegeben** geändert — Auftrag
`docs/auftraege/MAC_TB-86_faltenplan_schreibsperre.md`, Betreiberfreigabe
22.09.2026, 07:50 (Schritt 1 und 2 aus 36.3), Commit `4daa254`. Der Hash ging
von **`6f96b95d13563f73b11be69c2bd6996037854df794da61315029216ad0b22bd9`** (so im
Abbild `sperrliste_abbild_2026-09-22.json`, `6a1b732e…`, Punkt 2) auf
**`fd3e5018ae930c2e29747562a140506d5d9a6bb70b87e96cf5c0089e09afdd79`** (heute,
gemessen). Die Sonde meldet seither an Punkt 2 **`1 BEFUND`**, Lauf gesamt `1`
(`docs/belege/TB-86/schritt8_sonde.txt`; lesend wiederholt vor diesem Eintrag,
`docs/belege/TB-87/sonde_vorher.txt`). ⭐ **Nach dem Registertext oben ist das
der planmässige Fall vor dem Tag** — Auftrag, Freigabe, alter und neuer Hash
stehen hiermit als Tatsachennotiz. **Geschlossen wird er mit einem neuen Abbild
unter neuem Namen** (Plan Punkt 2b); das ist **nicht** Gegenstand dieses
Eintrags, und das alte Abbild bleibt.

> ⭐⭐ **Die weiteren Übergänge und ihr Abbild (39.5/39.9, TB-94,
> 23.09.2026):** Nach TB-86 haben sich planmässig bewegt: `faltenplan.py`
> `fd3e5018…` → `7aa0b8cc…` (TB-90, `303a7fd`, Punkt 2), `benchmark.py`
> `3960375a…` → `d6bdd558…` (TB-91, `31008b6`, Punkte 4 und 6),
> `auswertung.py` `1c2e2dae…` → `c3b4e69d…` (TB-92, `0292e92`, Punkte 3, 5
> und 14); dazu `registerbericht.py` und `test_vorregistrierung.py` (TB-92,
> auf keinem Punkt). Auftrag, Freigabe und volle Hashes stehen in **39.5**.
> Geschlossen werden der Fall oben und diese Übergänge mit **einem** neuen
> Abbild (**39.9**); `sperrliste_abbild_2026-09-22.json` bleibt.

**Marken am alten Ort — zwei:** in **36.2**, direkt unter dem Registertext
(unter der Marke aus 36.5), und in **36.6**, direkt unter dem Registertext
(unter der Marke aus 37.2).

### 37.4 Tatsachennotiz zu Abschnitt 10 — die zwei Listen in `herkunft.py`

⭐ Das ist die Tatsachennotiz, die 36.6 als **ausstehend** eingetragen hat
(„wird in diesem Abschnitt NOCH NICHT geschrieben"). **Fables eigene
Tatsachennotiz, 22d Abschnitt 3, zeichengleich:**

> **Tatsachennotiz zu Abschnitt 10 (22.09.2026):** `research/vorregistrierung/herkunft.py` trägt zwei Listen. **`EINGEFROREN`** (Z. 57, zehn Einträge) ist die Eingabe von `register()` (Z. 114): ein Gesamthash über die Registerdatei plus diese zehn Dateien, laut Docstring „über die eingefrorenen Festlegungen" — sie bildet die Menge aus **Abschnitt 0** ab, nicht die Sperrliste aus Abschnitt 10, und weicht von dieser an fünf Stellen ab (fehlend: `benchmark_drawdowns_vt.json`, `config/top25_symbols.txt`, `config/sp500_top150.txt`; zusätzlich: `kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`). **`SPERRLISTE_DATEIEN`** (Z. 66) wird von keiner Stelle gelesen — toter Code. Keine der beiden Listen ist das Abbild der Sperrliste (36.6). `herkunft.py` wird in `research/vorregistrierung/` von keinem Modul importiert; `herkunft.json` und `herkunft_protokoll.jsonl` existieren nicht; die einzigen Aufrufer von `block()` gehören zu `research/turn_of_month/`. Sperrlistenpunkte 11 und 12 verweisen damit auf Funktionen, die im Laufbereich heute niemand aufruft; der Datenvertrag (`auswertung.py` Z. 41) verlangt `herkunft.json` als Pflichteingabe. Der Erzeuger (Nachtrag 2) ist die Stelle, an der `register()` und `datenstand()` erstmals aufgerufen werden.

> ⚠️ **ERSETZT (38.6, Fable 22h, TB-89, 23.09.2026) — zwei Stellen dieses
> Satzes, der Satz selbst bleibt zeichengleich:** (a) „`auswertung.py` Z. 41"
> lies **Z. 51** (Fables Berichtigung (a)). (b) Der Halbsatz „weicht von dieser
> an fünf Stellen ab (fehlend: …; zusätzlich: …)" ist ersetzt durch Fables
> Ersatzsatz — acht Stellen, vier fehlend und vier zusätzlich; der Wortlaut
> steht zeichengleich in **38.6**. Beleg ist die Tatsachennotiz TB-87 (M3)
> unten.

**Und seine Entscheidung dazu, zeichengleich:**

> **Folge für `herkunft.py`, Entscheidung:** **Nicht öffnen.** Der Erzeuger ruft `register()` auf und schreibt in `herkunft.json` **auch das Feld `teile`** (das `register()` liefert und `block()` weglässt) — dann ist lesbar, welche Dateien in den Gesamthash eingingen, ohne dass `block()` oder `herkunft.py` geändert wird. `herkunft.json` bezeugt damit die Abschnitt-0-Menge (zehn Dateien plus Register); die Sperrlisten-Sonde bezeugt Abschnitt 10; die Tatsachennotiz oben sagt, welches Dokument was bezeugt. Zwei Nachweise mit verschiedenem Gegenstand sind kein Widerspruch — zwei Nachweise mit demselben Gegenstand und verschiedenem Inhalt wären einer. *Quelle des Grundes:* 21b (3), Einfrieren vor Umbau; der Erzeuger ist neuer Code, dort darf alles stehen. Kein Ergebnis.

**Tatsachennotiz (TB-87, M3, `m3_herkunft_listen.txt`) — nachgemessen, nicht
übernommen:**

| Aussage in Fables Notiz | gemessen | |
|---|---|---|
| `EINGEFROREN` Z. 57, zehn Einträge | **Z. 57**, zehn Einträge | ✔ |
| `SPERRLISTE_DATEIEN` Z. 66, von keiner Stelle gelesen | **Z. 66**, fünf Muster; ausser der Definition nur in einem **Kommentar** von `shared/sperrlistensonde.py:70` genannt, nirgends gelesen | ✔ |
| Eingabe von `register()` (Z. 114) | **Z. 114** `for rel in ([…REGISTERDATEI…] + EINGEFROREN):` | ✔ |
| `herkunft.py` in `research/vorregistrierung/` von keinem Modul importiert | **0** `import`/`from`; zwei Textfundstellen (Docstring `auswertung.py`, Beispieldaten-Schreiber `beispieldaten.py:142/145`) | ✔ |
| `herkunft.json`, `herkunft_protokoll.jsonl` existieren nicht | **existieren nicht** | ✔ |
| einzige Aufrufer von `block()` in `research/turn_of_month/` | **`auswertung.py:206`, `staging.py:127`**, beide dort | ✔ |
| Datenvertrag `auswertung.py` **Z. 41** | ⚠️ **Z. 51** (`<wurzel>/<bot>/herkunft.json`), Z. 52 „siehe herkunft.py"; Z. 41 ist `mittlere_exposure` | **abweichend** |
| „weicht … an **fünf** Stellen ab (fehlend: drei; zusätzlich: drei)" | ⚠️ siehe unten | **abweichend** |

⚠️ **Die Abweichungszahl, gemessen:** Fable schreibt „fünf Stellen" und nennt
sechs Namen. Der mechanische Mengenvergleich der zehn `EINGEFROREN`-Einträge
(auf Repo-Pfade aufgelöst) gegen die zehn Pfade der vierzehn Punkte (aus dem
Abbild `6a1b732e…`, das die Sonde mit Prüfung (ii) `0` gegen Abschnitt 10 prüft)
ergibt:

- **in Abschnitt 10, nicht in `EINGEFROREN` — vier:** `config/top25_symbols.txt`,
  `config/sp500_top150.txt`, `research/vorregistrierung/herkunft.py` (Punkte 11,
  12), `shared/zuteilung.py` (Punkt 10); **dazu** der bestimmte Pfad
  `ergebnisse/benchmark_drawdowns_vt.json` (kein Punkt, 37.2);
- **in `EINGEFROREN`, kein Pfad eines Punktes — vier:** `kennzahlen.py`,
  `messgroessen.py`, `pruefe_grenzsaetze.py` **und**
  `ergebnisse/messgroessen.json`.

Alle sechs Namen in Fables Notiz stimmen; **nicht genannt** sind dort
`herkunft.py`, `shared/zuteilung.py` und `ergebnisse/messgroessen.json`. Das
ändert seine Folgerung nicht — `EINGEFROREN` bildet die Abschnitt-0-Menge ab,
nicht Abschnitt 10 —, aber die Zahl „fünf" gilt so nicht; **eingetragen ist,
was gemessen ist**, Fables Satz bleibt zeichengleich stehen. Gemeldet im
Ergebnisdokument.

**Randbefund aus TB-84, nachgemessen:** `research/etf_trendfolge/datenstand.py`
Z. 43–49 lädt `research/vorregistrierung/herkunft.py` über
`reg.lade_fremdes_modul(…)` und ruft `herkunft.datenstand(…)` auf — ein Nutzer
ausserhalb von `turn_of_month/` und ausserhalb des Laufbereichs der
Vorregistrierung. Fables Satz über den **Laufbereich** bleibt damit richtig;
vollständig beantwortet „wer liest `herkunft.py`" er nicht.

> ⚠️ **Ergänzung (39.7, Fable 23d, TB-94, 23.09.2026) — `EINGEFROREN` ist nach
> dem Vollzug nicht vollständig:** `EINGEFROREN` hasht weiter
> `ergebnisse/benchmark_drawdowns.json` (historischer Stand), **nicht** die
> Tabelle, die der Lauf liest (`ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`,
> 39.2). `herkunft.py` bleibt ungeöffnet (`56a1c2e1…`). Der Satz, um den Fable
> diese Tatsachennotiz ergänzt (23d Abschnitt 1 (2)), zeichengleich:
> „`register()` bezeugt die Abschnitt-0-Menge vom 14.09.; die vollzogene Benchmark-Tabelle bezeugt Sperrlistenpunkt 4 über die Sonde."
> Nach Fables Präzisierung zu 36.1 (1) (23c) ist auch jeder Pfad in
> `EINGEFROREN` gesperrt — Wortlaut in **39.7**.

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**, unter dem
Hinweis aus 36.2/36.6 (der „ihre Tatsachennotiz steht bei Fable aus" sagt —
bleibt zeichengleich stehen).

### 37.5 Registertext „Ort registrierter Werte" — Ersteintrag

**Fable, 22d Abschnitt 4, zeichengleich:**

> **Registertext, Ersteintrag — Ort registrierter Werte:**
> **(1)** Jeder Sperrlistenpunkt, der einen Zahlenwert registriert (heute 7 und 9), nennt **genau ein** Modul und dort **genau eine** Konstante, aus der der Lauf diesen Wert liest. Dieses Modul steht mit Hash auf der Sperrliste; die Sonde prüft für den Punkt Datei-Hash **und** Wert der Konstante (Bauart „Datei plus Konstante", wie Punkte 3, 4, 10).
> **(2)** Der Laufpfad (Optimierer, Equity-Simulation, Erzeuger) liest registrierte Werte ausschliesslich aus diesem Modul — kein Laufmodul trägt eine eigene Kopie. Für den Papierpfad (`forward_test.py`) gilt das nicht als Sperre, aber als Konsistenzprüfung: Die Sonde meldet als Befund, wenn eine Kopie dort vom registrierten Wert abweicht.
> **(3)** Für Punkt 9: `TRADING_FEE_PCT` und `SLIPPAGE_PCT` in einem Modul; für Punkt 7: `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` in einem Modul. Welche Module (Kandidaten nach heutiger Messung: `messgroessen.py` für 9, `registerdaten.py` für 7) und ob eines der beiden Module bereits Abschnitt-0-eingefroren ist und deshalb ein neues kleines Modul die Werte tragen muss — **Handwerk mit Freigabe**, aber die Tatsachennotiz zu 7 und 9 nennt am Ende Modul, Zeile und Wert.
> **(4)** Tatsachennotiz zu 7 und 9, jetzt: die heute gemessenen Orte (neun `forward_test.py`; `messgroessen.py:59`; `registerdaten.py:99`, `:115`) mit dem Vermerk, dass der Registertext keinen davon nennt und der Zustand bis zur Umsetzung von (1)–(3) ungeschützt war.

> ⭐⭐ **Entscheidung zu (2) und (3) (38.5, Fable 22h, TB-89, 23.09.2026):** Es
> bleibt bei (2) — **kein Laufmodul trägt eine eigene Kopie.** Die neun
> `backtest_*.py` beziehen `TRADING_FEE_PCT` / `SLIPPAGE_PCT` künftig per
> Import aus einem **neuen** Modul (die Kandidaten aus (3) sind blockiert); der
> Papierpfad und `messgroessen.py` / `GEBUEHR_PCT` bleiben überwachte Kopien.
> **Für Punkt 7 ist (3) schon erfüllt:** `registerdaten.py` ist der Ort, nichts
> wird verschoben. Wortlaut und Begründung in **38.5**.

**Fables Befund, aus dem der Eintrag folgt, zeichengleich** (darin sein
Kernsatz *„Ein Sperrlistenpunkt, der einen Wert nennt und keinen Ort, sperrt
nichts — er legt fest."*):

> **Der Befund in einem Satz:** Ein Sperrlistenpunkt, der einen Wert nennt und keinen Ort, sperrt nichts — er legt fest. Festlegen ist Aufgabe der Festlegungen und des Registertexts; die Sperrliste soll sagen, **was unverändert bleibt**, und das ist immer eine Datei (oder ein Ort in einer). „Ändert jemand `TRADING_FEE_PCT` in einer der neun `forward_test.py`, merkt es kein Sperrlistenpunkt" ist genau der Zustand, den der Tag ausschliessen soll.

**Seine Abwägung der drei Wege, zeichengleich:**

> **Zu den drei Wegen:** *(iii) so lassen und Notiz* — nein: eine Tatsachennotiz macht eine Lücke sichtbar, sie schliesst sie nicht; der Tag friert dann eine Sperrliste ein, von der man weiss, dass sie zwei Werte nicht schützt. *(i) Ort je Punkt nachtragen* allein — nicht ausreichend, denn der Ort, den man heute misst (neun `forward_test.py`), ist nicht notwendig der Ort, aus dem der **Lauf** den Wert liest: `forward_test.py` ist der Papierpfad; die Optimierer und der noch zu schreibende Erzeuger sind der Laufpfad. Neun Kopien eines Werts als Sperrlistenorte einzutragen registriert die Kopien, nicht die Quelle. *(ii) Werte in eine Datei ziehen und sperren* — das ist der Kern, aber „ziehen" darf keine Kopie mehr erzeugen.

**Seine Quelle des Grundes — und der Satz, der Missverständnisse ausschliesst,
zeichengleich:**

> *Quelle des Grundes:* Zweck der Sperrliste (Übergabe Abschnitt 5) und A8; der Grundsatz ein Wert, ein Ort aus 21j. **Kein Ergebnis — und das ist hier wichtig zu sagen:** Die Werte selbst (0,1 / 0,05 / die beiden aus Punkt 7) ändern sich nicht um ein Zeichen; es ändert sich nur, wo sie stehen und dass jemand es merkt, wenn sie sich ändern.

**Tatsachennotiz zu Punkt 7 und 9 nach (4) (TB-87, M4, `m4_werte_orte.txt`) —
die heute gemessenen Orte:**

| Wert (Punkt) | Ort | Zeile | Wert im Code |
|---|---|---|---|
| `TRADING_FEE_PCT` (9) | neun `strategies/*/forward_test.py` | je eine Zuweisung (Z. 57–72) | `0.1` |
| `SLIPPAGE_PCT` (9) | neun `strategies/*/forward_test.py` | je eine Zuweisung (Z. 58–73) | `0.05` |
| `SLIPPAGE_PCT` (9) | `research/vorregistrierung/messgroessen.py` | **:59** | `0.05` |
| ⚠️ Gebühr (9) | `research/vorregistrierung/messgroessen.py` | **:58**, Name **`GEBUEHR_PCT`** — nicht `TRADING_FEE_PCT` | `0.1` |
| `CLUSTER_SCHWELLE` (7) | `research/vorregistrierung/registerdaten.py` | **:99** | `0.90` |
| `N_HISTORISCH_JE_BOT` (7) | `research/vorregistrierung/registerdaten.py` | **:115** (neun Einträge bis Z. 125, Summe 653) | Wörterbuch |

⚠️ **Zwei Abweichungen von Fables (4), gemessen:** (a) `messgroessen.py:59`
trägt nur `SLIPPAGE_PCT`; die Gebühr steht eine Zeile davor unter **anderem
Namen** (`GEBUEHR_PCT`) — für (3) heisst das: in `messgroessen.py` gibt es heute
**keine** Konstante `TRADING_FEE_PCT`. (b) **Nicht genannt, aber gemessen:**
Auch die neun `backtest_*.py` der Bots tragen je eine eigene Zuweisung
`TRADING_FEE_PCT = 0.1` / `SLIPPAGE_PCT = 0.05`
(`elliott_wave/backtest_elliott.py:73–74`,
`elliott_wave_stocks/backtest_elliott.py:77–78`, `rsi2_crypto/backtest_rsi2.py:58–59`,
`rsi2_mean_reversion/backtest_rsi2.py:85–86`, `t3_supertrend/backtest_trend.py:27–28`,
`turtle_soup_crypto/backtest_turtle_soup.py:96–97`,
`turtle_soup_stocks/backtest_turtle_soup.py:92–93`,
`volatility_breakout/backtest_breakout.py:105–106`,
`volatility_breakout_crypto/backtest_breakout.py:73–74`), dazu
`elliott_wave_stocks/signal_quality_test.py:37–38` als Verweis auf
`backtest_elliott`. **Ob der Laufpfad daraus liest, ist die Messung aus Plan
Punkt 5 — hier nicht gemessen.** Alle gemessenen Werte sind zeichengleich
`0.1` / `0.05` / `0.90`.

⚠️ **Vermerk nach (4):** Der Registertext von Punkt 7 und 9 nennt **keinen**
dieser Orte; der Zustand war bis zur Umsetzung von (1)–(3) **ungeschützt**.

**Fables Frage vor der Umsetzung, zeichengleich:**

> *Warum die Optimierer die Kosten heute vielleicht gar nicht aus `forward_test.py` lesen:* Das habe ich nicht gemessen und ihr nicht gefragt. **Nur das Ob, vor der Umsetzung:** Woher beziehen die neun `multi_symbol_optimise.py` und `equity_simulation.py` heute Kosten und Slippage — aus einer eigenen Konstante, aus `forward_test.py`, aus `messgroessen.py`, oder gar nicht? Wenn die Antwort „aus einer eigenen Konstante je Bot" lautet, gibt es neun weitere Kopien, und (2) ist grösser als eine Zeile.

⚠️⚠️ **Offen (Fable 22d), zeichengleich:**

> **Unsicher:** ob `messgroessen.py` und `registerdaten.py` als Abschnitt-0-eingefrorene Dateien für (3) noch geändert werden dürfen — wenn nicht, trägt ein neues kleines Modul die vier Werte, und die eingefrorenen Dateien bleiben stehen. Das seht ihr im Register (Abschnitt 0 und 15.8), ich nicht.

⭐ **Dazu gehört die Messung aus Plan Punkt 5:** woher beziehen die neun
`multi_symbol_optimise.py` und `equity_simulation.py` heute Kosten und
Slippage? ⛔ **Beides nicht Gegenstand dieses Eintrags.** Die Werte bleiben, wo
sie sind; Fables Kandidaten-Module (`messgroessen.py`, `registerdaten.py`)
sind Abschnitt-0-eingefroren (`herkunft.py` `EINGEFROREN`, 37.4) — ob sie für
(3) geändert werden dürfen, entscheidet nicht dieser Abschnitt.

**Marken am alten Ort:** bei **Sperrlistenpunkt 7** und bei **Punkt 9**.

### 37.6 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Sonde ändern** — sie meldet ihren Ausgang heute je Punkt; 37.1 verlangt ihn je Bestandteil, 37.2 die Prüfung der Gruppe „bestimmt" | Handwerk, eigene Freigabe |
| ⛔ | **Ein neues Abbild erzeugen** (Plan Punkt 2b) — der Befund `1` an Punkt 2 (37.3) bleibt bis dahin stehen; das Abbild `6a1b732e…` bleibt | eigene Aufgabe |
| ⛔ | **Werte verschieben** („ein Wert, ein Ort", 37.5 (1)–(3), Plan Punkt 6) — braucht erst die Messung aus Plan Punkt 5 | Betreiber, Freigabe |
| ⛔ | **`herkunft.py` öffnen** — Fables Entscheidung 37.4: nicht öffnen | — |
| ⛔ | **Irgendeine `.py` ändern** · ⚠️ `python3 faltenplan.py` — nicht aufgerufen | — |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (M5); die drei Sperrlisten-Hashes `0e54ac5c…`, `a163c498…`, `4549395f…` unverändert (M6); die Sperrlisten-Sonde lesend vor und nach dem Eintrag: Prüfung (ii) `0`, Listentext wie bei Erzeugung, unverändert `1` nur an Punkt 2 | — |
| ⚠️ | **Offen:** die Sonde muss je Bestandteil **zurückgeben** (37.1) · die Gruppe „bestimmt" **prüfen** (37.2) · das neue Abbild (Plan 2b, schliesst 37.3) · die Messung aus Plan 5 (woher lesen die Optimierer Kosten?) · Fables Unsicherheit zu den eingefrorenen Modulen (37.5) · die zwei Messabweichungen in 37.4 (Z. 51 statt 41; vier/vier statt „fünf") und in 37.5 (`GEBUEHR_PCT`; neun `backtest_*.py`) — Fable zur Kenntnis | Betreiber / Fable |

*Dieser Abschnitt ist rein additiv: Er trägt zwei Präzisierungen bzw.
Ergänzungen, eine Ergänzung zur Bedeutung eines Sondenbefunds, eine
Tatsachennotiz und einen Ersteintrag des Verfahrensprüfers zeichengleich ein;
setzt sieben Marken am alten Ort; hält die nachgemessenen Tatsachen samt vier
Abweichungen fest — und entfernt nichts. Gebaut wird nichts.*

## 38. Weg (A) — die letzte Falte heisst die Spanne, Fundstellen als Datei und Bezeichner, der Vollzug von Punkt 4 nach 37.3 in Form (ii), neun Importe statt überwachter Kostenkopien, zwei Berichtigungen des Verfahrensprüfers an sich selbst und die Messungen aus TB-88 (Fable 22h, TB-89, 23.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34 bis 37. Sechs Einträge des
Verfahrensprüfers — eine Berichtigung zu 35.1 (38.1), ein Ersteintrag für alle
künftigen Registertexte (38.2), eine Tatsachennotiz zu 21.9 und 10.1 (38.3),
die Form von Sperrlistenpunkt 4 (38.4), die Entscheidung zu den Kostenkopien
(38.5) und zwei Berichtigungen an seinem eigenen Text (38.6) —, alle Fable-Texte
zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22h_schluessel_und_vollzug.md`
(Antwort auf die Anfragen 22f und 22h). Dazu die Tatsachennotizen aus TB-88
(38.7; `docs/belege/TB-88/ERGEBNIS_TB-88.md`, Messstand `8851f67`) und der
Schlussteil (38.8). Auftrag `docs/auftraege/MAC_TB-89_register_38.md`; Belege
`docs/belege/TB-89/`; Eingang `c140ca9`, Schritt-0-Commit `da251da`.
⛔ **Keine `.py` geändert, kein neues Modul, kein Import, kein neues Abbild,
keine Sonde angepasst, kein Vollzug, kein Wert verschoben** — 38.8.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (Kopf von
Abschnitt 0; 35.1 dreimal; 21.9 zweimal; 10.1; Sperrlistenpunkte 4 und 7,
Punkt 9 zweimal; 23.7; 37.4; 37.5 — vierzehn). Die alten Sätze bleiben zeichengleich; `git diff --numstat`
auf dieses Register zeigt für TB-89 in der zweiten Spalte `0`. Die Marken in
Abschnitt 10 stehen, wie seit 37, als eingerückte `>`-Zeilen **ohne
Leerzeile** unter dem Punkt; die Sperrlisten-Sonde ist vor und nach dem
Eintrag **lesend** gelaufen (38.8).

⭐ **Dieser Abschnitt wendet 38.2 schon auf sich selbst an:** Fundstellen im
Code stehen hier als Datei und Bezeichner; wo eine Zeilennummer steht, steht
sie in einer Tatsachennotiz und trägt den Commit, an dem sie gemessen wurde.
In den **Zitaten** stehen Zeilennummern, wie Fable sie geschrieben hat —
zeichengleich heisst zeichengleich.

### 38.1 ⭐⭐ Berichtigung zu 35.1 (Folge/Handwerk) — Weg (A): die letzte Falte heisst die Spanne

**Fable, 22h Abschnitt 3, zeichengleich — sein Befund:**

> Ihr habt recht, und der Befund ist meiner: 35.3 nennt den Bezeichner einen Schlüssel, den zwei Programme teilen, und 35.1 sagt trotzdem „eine Zeile". Ein Schlüssel, der an einer Stelle gebildet und an einer anderen verglichen wird, ist nie eine Zeile.

**Die Entscheidung, zeichengleich:**

> **Berichtigung zu 35.1 (Folge/Handwerk):** Der Bezeichner der Bestätigungsperiode entsteht **an der Stelle, an der die letzte Falte ihren Namen bekommt** (heute `faltenplan.py`, die Zuweisung der Rolle `bestaetigung`, Umgebung Z. 307) — die letzte Falte **heisst** die Spanne `2026-01-01/2026-09-01`. `falten[-1]["name"]`, `plan[bot]["bestaetigungsperiode"]`, die Spalte `falte` der Bestätigungszeile in `zellen.csv` und der Bericht tragen damit denselben String aus derselben Quelle; `auswertung.py`, `beispieldaten.py` und `registerbericht.py` bleiben unberührt. Weg (B) — zwei Namen für dieselbe Periode — ist unzulässig.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 35.3 (ein Schlüssel, zwei Programme) und der Grundsatz ein Wert, ein Ort (21j, 37). Weg (B) erzeugt genau das Paar, das 35 abschaffen sollte: einen Faltennamen `2026`, der siebzehn Monate verspricht, und einen Bezeichner daneben, der es richtigstellt. Kein Ergebnis.

**Zu dem Einwand des steuernden Chats gegen (A), zeichengleich** (33.3 führt
die Selektionsfalten als Feld, die Bestätigungsperiode als eigenes Feld; der
Schrägstrich ist mit Absicht kein Bindestrich):

> *Zu eurem Einwand gegen (A)* („der Faltenname einer Falte trägt dann eine Spanne, die übrigen Jahre — und 33.3 führt den Faltennamen als Feld"): 33.3 führt die **Selektionsfalten** als Feld (`selektionsfalten`, Liste von Kalenderjahren) und die Bestätigungsperiode als **eigenes** Feld (35). Die Bestätigungsperiode ist keine Selektionsfalte (35) und steht deshalb nicht in der Liste — die Sonde prüft, dass `selektionsfalten` nur Kalenderjahre enthält und der Spannen-Bezeichner nur im Feld `bestaetigungsperiode` steht. Dass die Bestätigungsfalte im Code als letztes Element der Faltenliste mit Rolle `bestaetigung` geführt wird, ist Umsetzung und kein Widerspruch, solange das Abbild die Rollen trennt. Und der Schrägstrich in `JJJJ-MM-TT/JJJJ-MM-TT` ist mit Absicht kein Bindestrich: Ein Doppeljahr heisst `2018-2019`, eine Spanne heisst `…/…` — zwei Formen, die sich nicht verwechseln lassen.

**Sein Handwerk daraus, zeichengleich** (das Fertigkriterium darin betrifft
38.7 (d)):

> *Handwerk daraus:* Die Änderung ist eine Stelle in `faltenplan.py` (Namensbildung der Bestätigungsfalte), nicht Z. 338; danach Ausgabevergleich wie bei TB-86: alle Selektionsfalten zeichengleich, genau ein String verändert, je Bot; `test_vorregistrierung.py` grün, gemessen auf dem Mac (TB-88).

**Seine Unsicherheit, zeichengleich:**

> **Unsicher:** ob `test_vorregistrierung.py` eine Prüfung enthält, die den Faltennamen der Bestätigungsfalte als Jahr erwartet — dann wird sie unter (A) rot und muss als Prüfung an 35 angepasst werden (der Test folgt dem Register, nicht umgekehrt); TB-88 sieht es.

⚠️⚠️ **Tatsachennotiz — Weg (B) hätte einen Sperrlistenpunkt berührt (TB-88,
M2b, `m2b_wege_a_b_probe.py`, nur im Speicher, Messstand `8851f67`):**
`research/vorregistrierung/auswertung.py`, Funktion `lies_zellen`, vergleicht
die **Menge** der `falte`-Werte je Zelle gegen die Faltennamen des Plans
(`[f["name"] for f in plan[bot]["falten"]]`, Z. 177–182 am Stand `8851f67`).
Schreibt der Erzeuger unter (B) den Bezeichner in die Spalte `falte`, bricht
die Auswertung **dort** ab (*„Falten stimmen nicht mit dem Faltenplan
ueberein"*); schreibt er den Faltennamen (B′), bricht sie in der Funktion
`bestaetigungsperiode` ab. Weg (A) läuft in derselben Probe durch
(`falte: '2026-01-01/2026-09-01'`, gemessen für `turtle_soup_stocks` mit den
Tabellen aus `_vt.json`). ⇒ Weg (B) hätte eine Änderung an `auswertung.py`
verlangt — **Sperrlistenpunkt 5** (Abschnitt 10). *Damit steht Fables
Entscheidung nicht nur auf einem Grund, sondern auf einer Messung.* ⚠️ Fables
Begründung nennt diese Messung nicht; sie ist nicht sein Grund, sondern steht
daneben. Nicht gemessen ist, was in Registertext, Abbild und Berichten sonst
an Faltennamen hängt (TB-88, Antwort 1).

**Tatsachennotiz zu Fables Unsicherheit (TB-88, M1 (e), Messstand
`8851f67`):** Die einzige Prüfung in `test_vorregistrierung.py`, die den
Bezeichner der Bestätigungsperiode vergleicht, ist `A3`
(`bp["falte"] not in selektionsfalten`, in `teil_a`); sie bleibt mit jeder
Spanne wahr. Die Fehlerklasse, die Fable befürchtet, ist dort an der
Bestätigungsfalte **nicht** gemessen — an den Selektionsfalten ist sie schon
eingetreten (`G6`, 38.7 (d)).

**Marken am alten Ort:** bei **35.1**, unter der bestehenden Marke aus 36.1 (4)
und 36.3 — eine für 38.1, eine für 38.7 (c).

### 38.2 ⭐ Registertext, Ersteintrag — Fundstellen: Datei und Bezeichner, Zeilennummern nur mit Commit

**Fable, 22h Abschnitt 4, zeichengleich — der Anlass:**

> Tatsachennotiz zu 35.1: „Z. 336 → 338, Z. 368 → 460 nach TB-86 (Commit …)". 35.1 selbst nicht neu fassen — aber eine Regel für alle künftigen Registertexte, weil das sonst jede Woche wiederkommt:

**Der Registertext, zeichengleich:**

> **Registertext, Ersteintrag — Fundstellen:** Ein Registertext nennt Fundstellen im Code als **Datei und Bezeichner** (Funktion, Konstante, Zuweisung, Feldname), nicht als Zeilennummer. Zeilennummern stehen nur in Tatsachennotizen, zusammen mit dem Commit, an dem sie gemessen wurden. Eine Zeilennummer ohne Commit ist keine Fundstelle.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* append-only — ein Registertext, der altert, sobald jemand eine Datei anfasst, erzeugt Berichtigungen ohne Sachgrund. Kein Ergebnis.

**Belegt durch 38.7 (a):** Die Fundstellen in 35.1 (Z. 336 und Z. 368) waren
noch am Tag des Eintrags um zwei bzw. zweiundneunzig Zeilen gewandert —
durch einen Commit, der den Registertext nicht berührte (`4daa254`). Schon 30.3 hatte
festgehalten: *„Eine Zeilenangabe im Register trägt ab hier ihren
Commit-Stand mit."* 38.2 macht aus dieser Beobachtung eine Regel.

⭐ **Wo die Regel steht, und warum dort:** als Marke **im Kopf von
Abschnitt 0** dieses Registers — nicht bei den Prüfprinzipien
(`docs/projektfuehrung/`). Drei Gründe: (1) Sie ist **Registertext** und
bindet jeden künftigen Registertext; ein Registertext gehört ins Register,
das append-only ist und mit seinem Hash in `herkunft.py::register()`
eingeht — die Prüfprinzipien sind ein Arbeitsdokument des steuernden Chats,
nicht registriert und nicht append-only. (2) Wer einen Registertext schreibt,
schreibt ihn in dieser Datei; der Kopf von Abschnitt 0 ist die Stelle, an der
jeder Leser und jeder Schreiber vorbeikommt, bevor er einen Abschnitt öffnet.
(3) Die Prüfprinzipien regeln, wie geprüft wird; diese Regel regelt, wie
geschrieben wird — geprüft wird sie nach den Prüfprinzipien wie jeder andere
Registertext. *Eine Kopie bei den Prüfprinzipien wäre eine zweite Fassung
derselben Regel an einem zweiten Ort — genau das, was 21j und 37.5 für Werte
ausschliessen.*

**Marken am alten Ort:** im **Kopf von Abschnitt 0** (die Regel) und bei
**35.1** (die Tatsachennotiz 38.7 (a), an der sie belegt ist).

### 38.3 ⭐⭐ Tatsachennotiz zu 21.9 und 10.1 — der Vollzug von Punkt 4 vor dem Tag ist eine beauftragte Änderung nach 37.3

**Fable, 22h Abschnitt 5, zeichengleich — welcher Satz gilt, und warum 10.1
hier nicht greift:**

> **Welcher Satz gilt:** 37.3. Die Sperrliste bindet ab dem signierten Tag; 10.1 regelt, was ein Bug-Fix **nach** Beginn des Laufs ist („der Lauf beginnt von vorn") — das Protokoll `herkunft_protokoll.jsonl` ist der Ort, an dem **Läufe** und ihre Amendments stehen, und vor dem ersten Lauf gibt es nichts, was dort stünde. 21.9 nennt den Vollzug „Amendment", weil der Begriff am 19.09. noch für beides stand; 23.6 hat ihn danach der Sperrliste des Codes zugeordnet, und 37.3 hat den Zeitpunkt geklärt. Die **Reihenfolge**-Entscheidung aus 21.9 (einmal, nach TB-31, alle neun Bots) gilt weiter und ist erfüllt — `_vt.json` trägt neunmal `endgueltig` (23.5).

**Die Tatsachennotiz, zeichengleich:**

> **Tatsachennotiz zu 21.9 und 10.1:** Der Vollzug von Sperrlistenpunkt 4 vor dem Tag ist eine beauftragte Änderung nach 37.3 — Registertext, Tatsachennotiz mit altem und neuem Hash, neues Abbild. Kein Amendment nach 10.1, kein Protokolleintrag; das Protokoll entsteht mit dem Erzeuger und beginnt mit dem Stand des Tags.

⭐ **Was sich damit für 21.9 ändert:** Das Wort „Amendment" in der
Betreiberentscheidung 21.9 bleibt zeichengleich stehen; es bezeichnet nach
diesem Eintrag **keinen** Vorgang nach 10.1. Die **Reihenfolge**-Entscheidung
aus 21.9 gilt weiter und ist nach Fable erfüllt. **Tatsachennotiz (TB-88, M5,
Messstand `8851f67`):** `_vt.json` trägt für alle neun Bots `status:
endgueltig`; `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`
existiert nicht (`test -f`) — es gibt vor dem ersten Lauf kein Protokoll, in
das ein Amendment einzutragen wäre, wie Fables Grund voraussetzt.

**Marken am alten Ort:** bei **21.9**, unter der Betreiberentscheidung, und
bei **10.1**, unter dem Absatz zum append-only-Protokoll.

### 38.4 ⭐ Sperrlistenpunkt 4 — Form (ii): Form steht fest, Vollzug steht aus

**Fable, 22h Abschnitt 5, zeichengleich — die Form und seine Ablehnung von (i)
und (iii):**

> **Form: (ii).** Punkt 4 nennt beide Dateien; `benchmark_drawdowns.json` bleibt gesperrt und unverändert als registrierter historischer Stand mit Tatsachennotiz — wörtlich die Bauart von Punkt 2 (30.3) — und `benchmark_drawdowns_vt.json` ist die Tabelle, die der Lauf liest. *(i)* entfernt etwas aus der Liste; die Sperrliste beweist, dass nichts bewegt wurde, und das kann sie nur für Dateien, die auf ihr stehen. *(iii)* setzt eine ERSETZT-Marke an einen Punkt, dessen Datei weiter geprüft werden soll — die Marke sagt dann das Falsche. Kein Ergebnis: keine Zahl der Tabelle ist berührt.

**Sein Fertigkriterium für den Vollzug, zeichengleich:**

> Vollzug fertig, wenn (Plan-Punkt 8 erweitert): Registertext eingetragen, `registerbericht.py` liest `symbole_handelbar_in_falte` (23.5), `test_vorregistrierung.py` grün — die roten Prüfungen misst TB-88 —, neues Abbild, Sonde gegen das Abbild 0 für die Pfade.

> ⚠️⚠️ **ERSETZT (39.1, Fable 23f, TB-94, 23.09.2026) — das Fertigkriterium im
> Zitat oben:** Fable hat es in **23a** zurückgenommen und in **23f** als
> Berichtigung zu 38.4 adressiert. Es gilt der Ersatztext in **39.1**: Punkt 8
> ist fertig, wenn Registertext (Form (ii)), Tatsachennotiz mit altem und
> neuem Hash, die drei Leser über eine Konstante, der Absturz weg und
> `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**,
> Modus-Nachweis bytegleich, neues Abbild, Sonde 0 für die Pfade. **Der
> Ausgang einzelner Prüfungen ist nicht Fertigkriterium von Punkt 8**; „null
> rote Prüfungen" bleibt Tag-Vorbedingung (21.9, 23a). Das Zitat oben bleibt
> zeichengleich. TB-92 hat sich an dieses Zitat gehalten und abgebrochen —
> richtig (39.1).

⛔ **Festgelegt ist die Form, nicht vollzogen.** Punkt 4 in Abschnitt 10 bleibt
zeichengleich; `benchmark_drawdowns.json` (`a163c498…`) und
`benchmark_drawdowns_vt.json` (`4549395f…`) sind vor und nach diesem Eintrag
gleich (38.8). Der Vollzug ist **Plan-Punkt 8** und hängt an **zwei offenen
Fragen** an Fable (`FABLE_ANFRAGE_2026-09-22i_slippage_ja_und_gruen_nein.md`):
(1) ob „`test_vorregistrierung.py` grün" Fertigkriterium bleibt (Abschnitt 3
der Anfrage, hier 38.7 (d)); (2) welche Tabelle Punkt 4 für `t3_supertrend`
vollzieht — `_vt.json` trägt dort eine Falte `2018`, die der Plan seit TB-72
nicht mehr hat, und `dd_toleranz` ist in `_vt.json` und
`benchmark_drawdowns_tb72.json` verschieden (TB-88, M5; Werte nach 27.1 nicht
wiedergegeben) (Abschnitt 4 der Anfrage). **Beide sind hier nicht
beantwortet.**

**Tatsachennotiz (TB-88, M5, Messstand `8851f67`) — was der Vollzug berührt,
lesend:** `test_vorregistrierung.py` (Funktion `_tabellen`),
`auswertung.py` (`main`) und `registerbericht.py` lesen heute
`ergebnisse/benchmark_drawdowns.json`; `registerbericht.py` liest dort den
Schlüssel `symbole_point_in_time`, den `_vt.json` nicht trägt (23.5:
`symbole_handelbar_in_falte`). `auswertung.py` steht als Punkt 3 und 5 auf der
Sperrliste.

**Marke am alten Ort:** bei **Abschnitt 10, Punkt 4** — ⚠️ ausdrücklich
*„Form steht fest, Vollzug steht aus"*.

> ⭐⭐ **VOLLZOGEN (39.2, TB-94, 23.09.2026):** Form (ii) ist vollzogen — Punkt
> 4 nennt `ergebnisse/benchmark_drawdowns.json` (`a163c498…`, historischer
> Stand, unverändert) **und** die Tabelle, die der Lauf liest: ⚠️ **nicht**
> `_vt.json`, wie Fables Formtext oben sagt, sondern die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`,
> 23a/23b, TB-91). Beide offenen Fragen dieses Abschnitts sind beantwortet:
> „grün" (39.1) und die Tabelle für `t3_supertrend` (39.2). Die Tatsachennotiz
> TB-88 oben (die drei Leser lesen die alte Datei, alter Schlüssel) ist durch
> TB-92 (`0292e92`) überholt: sie lesen die Neurechnung über
> `auswertung.BENCHMARK_TABELLE`, `registerbericht.py` liest
> `symbole_handelbar_in_falte` (39.2). Der Text oben bleibt zeichengleich.

### 38.5 ⭐⭐ Kosten — kein Laufmodul trägt eine eigene Kopie: neun Importe, nicht neun überwachte Kopien

**Fable, 22h Abschnitt 2, zeichengleich — die Entscheidung:**

> **Entscheidung (Begründung nennt kein Ergebnis):** Es bleibt bei 37 (2) — **kein Laufmodul trägt eine eigene Kopie.** Die neun `backtest_*.py` ersetzen ihre Zuweisung durch den Import aus dem neuen Modul. Der Papierpfad (`forward_test.py`) behält seine Kopien und wird von der Sonde auf Gleichheit geprüft — wie in 22d (2) gesagt, und aus dem dort genannten Grund: Er ist Live-Code, seine Änderung braucht eine eigene Freigabe, und er ist nicht Teil des Laufs.

**Seine Begründung, zeichengleich** (darin der Kernsatz *„Ein Import ist keine
Prüfung, sondern eine **Struktur**"*):

> *Warum beseitigen und nicht überwachen:* Eine Sonde, die neun Kopien auf Gleichheit prüft, muss die Konstante **im Quelltext finden** — und wer den Finder schreibt, entscheidet, was gefunden wird (eine lokale Variable gleichen Namens, eine Zuweisung in einem Kommentar, eine Berechnung statt eines Literals). Ein Import ist keine Prüfung, sondern eine **Struktur**: Der Wert kann im Laufmodul nicht anders sein als im Modul, weil er dort nicht steht. Dieselbe Regel wie bei der Schreibsperre — die Sicherung ist stärker, wenn sie nicht vergleichen muss. Kein Ergebnis: alle achtzehn tragen heute dieselbe Zahl, sie ändert sich nicht.

**Zu Punkt 7, zeichengleich — seine Rücknahme des 22d-Kandidaten:**

> *Zu Punkt 7:* `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` stehen in `registerdaten.py` — das **ist** ein Modul, ein Ort, und es steht als Punkt 1 auf der Sperrliste. Hier ist nichts zu verschieben; Punkt 7 bekommt den Ort nachgetragen (`registerdaten.py`, die beiden Konstanten), und die Sonde prüft Datei plus Wert. Mein „Kandidat" aus 22d war für Punkt 7 gar keiner — der Ort existiert schon.

**Zu `messgroessen.py` / `GEBUEHR_PCT`, zeichengleich:**

> *Zu `messgroessen.py` / `GEBUEHR_PCT`:* bleibt, wie es ist (eingefroren), mit Tatsachennotiz: eine Kopie unter anderem Namen, kein Laufort, von der Sonde auf Gleichheit geprüft wie der Papierpfad.

⭐ **Was damit gilt, zusammengefasst — die Zitate oben sind massgeblich:**

| Ort | Stellung nach 38.5 |
|---|---|
| neun `strategies/*/backtest_*.py` (Laufpfad) | ersetzen ihre Zuweisung von `TRADING_FEE_PCT` / `SLIPPAGE_PCT` durch einen **Import** aus einem neuen Modul — **kein Laufmodul trägt eine eigene Kopie** (37.5 (2)) |
| neun `strategies/*/forward_test.py` (Papierpfad) | behalten ihre Kopien; **überwachte** Kopie, die Sonde prüft auf Gleichheit |
| `research/vorregistrierung/messgroessen.py`, `GEBUEHR_PCT` | bleibt eingefroren; **überwachte** Kopie unter anderem Namen, kein Laufort |
| Punkt 7: `registerdaten.py`, `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` | **nichts zu verschieben** — der Ort existiert; Punkt 7 bekommt ihn nachgetragen, die Sonde prüft Datei plus Wert |

⛔ **Nicht Gegenstand dieses Eintrags:** das neue Modul, die neun Importe, der
Nachtrag des Orts bei Punkt 7 und 9 und die Gleichheitsprüfung der Sonde —
Handwerk, TB-90 (Freigabe des Betreibers liegt nach dem Auftrag vor,
22.09.2026). Die Werte `0,1` / `0,05` / `0,90` ändern sich nicht.

**Marken am alten Ort:** bei **Abschnitt 10, Punkt 9** und **Punkt 7**, je
unter der Marke aus 37.5, die zeichengleich bleibt; bei **37.5**, direkt unter
dem Registertext.

### 38.6 ⚠️ Fables zwei Berichtigungen an sich selbst — Z. 51, und acht statt fünf Stellen

**Fable, 22h Abschnitt 1, zeichengleich:**

> **(a)** „`auswertung.py` Z. 41" lies **Z. 51**. Die Zahl kam aus Nachtrag 2; ich habe sie übernommen statt sie als Voraussetzung zu nennen — mein Verstoss gegen meine eigene Regel aus 21m. Berichtigung als Tatsachennotiz zu 37.4 genügt.

> **(b)** „an fünf Stellen" — ich habe fünf angekündigt und sechs aufgezählt; das war kein Messfehler, sondern ein Zählfehler beim Schreiben, und er ist meiner. Gemessen acht. **Ersatzsatz für 37.4:**

**Der Ersatzsatz für 37.4, zeichengleich:**

> … und weicht von dieser an **acht** Stellen ab — **vier fehlen** (`config/top25_symbols.txt`, `config/sp500_top150.txt`, `research/vorregistrierung/herkunft.py`, `shared/zuteilung.py`; dazu der bestimmte Pfad `benchmark_drawdowns_vt.json`, der kein Punkt ist), **vier stehen zusätzlich** (`kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`, `ergebnisse/messgroessen.json`).

> Der alte Satz bleibt mit Marke; eure Tatsachennotiz daneben ist der Beleg.

⭐ **Der alte Satz in 37.4 bleibt stehen** — Fables Tatsachennotiz aus 22d,
zeichengleich, mit „Z. 41" und „an fünf Stellen". Er bekommt die
ERSETZT-Marke; die Tatsachennotiz TB-87 (M3) in 37.4, die beides gemessen
hatte, ist der Beleg. Fables Ersatzsatz nennt dieselben acht Abweichungen,
die 37.4 gemessen aufgezählt hat (vier fehlend, dazu der bestimmte Pfad; vier
zusätzlich) — gegen die Liste in 37.4 verglichen: dieselben neun Dateien;
einziger Schreibunterschied, dass 37.4 den bestimmten Pfad als
`ergebnisse/benchmark_drawdowns_vt.json` führt, Fable ohne Ordner.

**Marke am alten Ort:** bei **37.4**, direkt unter Fables Tatsachennotiz.

### 38.7 ⭐ Tatsachennotizen aus TB-88

Quelle: `docs/belege/TB-88/ERGEBNIS_TB-88.md`, Messstand `8851f67`, soweit
nicht anders gesagt. Zwischen `8851f67` und dem Eingang dieses Auftrags hat
sich unter `research/` keine Datei geändert (`git diff --quiet 8851f67 HEAD --
research/`, gemessen in TB-89).

**(a) Die Fundstellen aus 35.1, heute.** Die Erzeugung des Bezeichners
(`"bestaetigungsperiode": falten[-1]["name"] …`, in
`research/vorregistrierung/faltenplan.py`, Funktion `_plan`) steht am Stand
`8851f67` auf **Z. 338**, die Konsolenausgabe (`best =
p["bestaetigungsperiode"]`, Funktion `main`) auf **Z. 460**. 35.1 nennt Z. 336
und Z. 368 (gemessen in TB-83, HEAD `9dac8d4`; so gültig seit `76c20ec`,
TB-80). Verschoben hat sie
**`4daa254`** (TB-86 Schritt 2 und 3: `--ziel`, Voreinstellung,
Einmal-Schreibsperre) — nicht `ee4e65c`, das ist der Abschlussbeleg von TB-86.
⭐ *Damit ist 38.2 belegt.* Die Namensbildung der Bestätigungsfalte — die
Stelle, die Fable in 38.1 meint — ist die Zuweisung der Rolle `bestaetigung`
in derselben Funktion `_plan` (Z. 307 am Stand `8851f67`).

**(b) ⭐⭐ Slippage — Fables Messbitte aus 22h Abschnitt 2, zeichengleich:**

> **Eine Messbitte, nur das Ob, bevor der Auftrag geschrieben wird:** Eure Tabelle nennt in den neun `backtest_*.py` nur `TRADING_FEE_PCT`. Sperrlistenpunkt 9 registriert **auch** `SLIPPAGE_PCT = 0,05 je Order` und die Summe 0,30 %. **Wenden die neun `backtest_*.py` Slippage an — und unter welchem Namen?** Wenn nein, rechnet der Laufpfad mit anderen Kosten, als das Register registriert; das wäre ein eigener Befund, grösser als die Frage der Kopien, und er müsste vor dem Tag ins Register — als Berichtigung des Codes an den Registertext, nicht umgekehrt.

**Gemessen: ja.** **9 von 9** `strategies/*/backtest_*.py` tragen
`SLIPPAGE_PCT = 0.05` (derselbe Name, derselbe Wert) neben
`TRADING_FEE_PCT = 0.1` und rechnen `2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)` —
**0,30 %** je Rundlauf, genau die Summe aus Punkt 9, Ein- und Ausstieg. ⚠️
**Formabweichung ohne Wertunterschied:** `t3_supertrend/backtest_trend.py`
zieht die Kosten als `pnl_pct -= 2 * (…)` ab statt über `total_cost_pct = 2 *
(…)`. ⇒ **Der Befund, den Fable befürchtet hat, tritt nicht ein**; die
Voraussetzung aus 22h Abschnitt 6 ist erfüllt. ⚠️ *Herkunft:* Diese Messung
steht **nicht** in `ERGEBNIS_TB-88.md`, sondern in der Anfrage 22i des
steuernden Chats (Abschnitt 1, HEAD `ec54618`); in TB-89 lesend nachgemessen
am Stand `da251da` (`docs/belege/TB-89/m_slippage_backtest.txt`), gleich.

**(c) ⚠️⚠️ Weg (B) hätte einen Sperrlistenpunkt berührt.** Steht in 38.1;
Marke bei 35.1.

**(d) ⚠️⚠️ „rot" heisst heute: der Test stürzt ab — und nach dem Vollzug
bleibt er 163/2.** `research/vorregistrierung/test_vorregistrierung.py` läuft
am Stand `8851f67` **keine einzige Prüfung**: Mit aktiviertem `trading-env`
endet er in `teil_a` mit `KeyError: '2017'` in `auswertung.py`, Funktion
`zulaessigkeit` — **0 bestanden, 0 gescheitert**, die Schlusszeile wird nie
gedruckt, rc `1`. Ursache: der Test liest `ergebnisse/benchmark_drawdowns.json`
(TB-30a-Stand, für `turtle_soup_stocks` Falten `2019`–`2026`), der Plan beginnt
bei `2017`. Ohne venv scheitert er schon früher am fehlenden Paket `binance`.
Die **Simulation des Vollzugs** (Kopie des Ordners, nur dort die Tabelle
getauscht; `m4_simulation_punkt8.sh`) ergibt **163 bestanden, 2 gescheitert**:

| Prüfung | hängt an |
|---|---|
| `G6` (*„2020 und 2022 sind Testfalten, keine Trainingsjahre"*) | **nicht an Punkt 4.** Sucht die Faltennamen `2020` und `2022`; `elliott_wave` hat seit TB-61 Zweijahresfalten `JJJJ-JJJJ` — eine Annahme aus TB-30a |
| `H3` (*„ohne die gesetzte Null aendert sich die Statistik"*) | **nicht an Punkt 4.** Die Probe setzt vier Falten ohne Trade und rechnet laut eigenem Kommentar mit sieben Selektionsfalten; seit der ersten Falte `2017` sind es neun, der Median kippt nicht mehr |

⇒ Beide hängen am **Faltenplan** (TB-56/TB-61/TB-72), nicht an der
Benchmark-Tabelle. ⚠️ **Damit ist Fables Fertigkriterium
„`test_vorregistrierung.py` grün" (22h Abschnitt 5, zitiert in 38.4, und
Abschnitt 3, zitiert in 38.1) heute nicht erreichbar.**

⚠️⚠️ **OFFENE FRAGE — eingetragen, nicht entschieden:** Bleibt „grün"
Fertigkriterium von Plan-Punkt 8? Die Anfrage 22i (Abschnitt 3) legt Fable
drei Lesarten vor — (1) fertig, wenn der Absturz weg ist, `G6`/`H3` werden ein
eigener Punkt; (2) Punkt 8 umfasst `G6`/`H3`; (3) „grün" bleibt, beide als
bekannt rot mit Grund, was A4 und 21.9 widerspräche. **Die Frage liegt bei
Fable; dieses Register beantwortet sie nicht**, auch nicht durch die
Reihenfolge der Lesarten oder die Neigung des steuernden Chats, die dort
steht. Bis zu seiner Antwort gilt 21.9 unverändert: der Test ist **„offen
durch eigene Änderung — blockierend für den Tag"**; neu ist nur die gemessene
Tatsache, dass „rot" dort einen Absturz bezeichnet. *Ein Registerabschnitt
darf eine offene Frage tragen — 21.6 hat es vorgemacht.*

> ⭐⭐ **BEANTWORTET (39.1, Fable 23a/23f, TB-94, 23.09.2026):** Lesart **(1)**
> — Plan-Punkt 8 ist fertig, wenn der Absturz weg ist und der Test bis zur
> Schlusszeile läuft; `G6`/`H3` sind der eigene Planpunkt „Testannahmen folgen
> dem Register" (23a), Tag-Vorbedingung, nicht Punkt 8. Das Fertigkriterium in
> 38.4 ist durch den Ersatztext in 39.1 berichtigt. Gemessen am echten Stand
> (TB-92, `0292e92`): Absturz weg, Schlusszeile erreicht, **163/2** (`G6`,
> `H3`) — dieselben zwei wie in der Simulation oben. Die Frage oben bleibt
> zeichengleich stehen.

**Marken am alten Ort:** (a) und (c) bei **35.1**; (b) bei **Abschnitt 10,
Punkt 9**; (d) bei **21.9**, unter der Tabelle der Folgen (wo der rote Test
geführt wird), und bei **23.7**, unter dem Nachtrag TB-71.

### 38.8 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert** — weder `faltenplan.py` (Namensbildung, 38.1) noch die neun `backtest_*.py` (Importe, 38.5); **kein neues Modul**, kein Import gesetzt | TB-90 |
| ⛔ | **Kein Vollzug von Punkt 4** — nur die Form (38.4); `benchmark_drawdowns.json` bleibt byteweise dieselbe Datei | Plan-Punkt 8, nach Fables Antwort auf 22i |
| ⛔ | **Kein neues Abbild**, keine Sonde angepasst, `python3 faltenplan.py` nicht aufgerufen; `registerbericht.py` und `test_vorregistrierung.py` nicht angefasst | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — der alte Satz in 37.4, die Zeilennummern in 35.1 und das Wort „Amendment" in 21.9 bleiben zeichengleich; ERSETZT- und Hinweis-Marken, nichts entfernt | — |
| ⛔ | **Keine offene Frage beantwortet** — weder „grün" als Fertigkriterium (38.7 (d)) noch die Tabelle für `t3_supertrend` (38.4) | Fable |
| ⭐ | **Keine Zahl bewegt:** die drei Sperrlisten-Hashes `a163c498…` (`benchmark_drawdowns.json`), `0e54ac5c…` (`faltenplan.json`), `4549395f…` (`benchmark_drawdowns_vt.json`) vor und nach dem Eintrag gleich; die Sperrlisten-Sonde lesend vor und nach dem Eintrag gegen `sperrliste_abbild_2026-09-22.json`: Prüfung (ii) `0`, Listentext wie bei Erzeugung, unverändert `1` nur an Punkt 2 (37.3) | — |
| ⚠️ | **Offen:** 22i Abschnitt 3 (grün), Abschnitt 4 (`t3_supertrend`), und ob `G6`/`H3` als eigener Punkt in den Plan vor dem Tag gehören · das neue Modul und die neun Importe (38.5) · die Namensbildung (38.1) · der Vollzug von Punkt 4 (38.4) · das neue Abbild danach — ein Abbild für alle drei Dateigruppen (22h Abschnitt 6) | Fable / Betreiber / TB-90 |

*Dieser Abschnitt ist rein additiv: Er trägt eine Berichtigung, einen
Ersteintrag, eine Tatsachennotiz, eine Formfestlegung, eine Entscheidung und
zwei Selbstberichtigungen des Verfahrensprüfers zeichengleich ein; setzt
vierzehn Marken am alten Ort; hält die Messungen aus TB-88 samt einer offenen
Frage fest — und entfernt nichts. Gebaut wird nichts.*

## 39. Der Vollzug von Sperrlistenpunkt 4 im Register — Berichtigung des Fertigkriteriums in 38.4, Form (ii) vollzogen, Determinismus- und Modus-Nachweis, fünf Hash-Übergänge nach 37.3, zwei Eingaben ohne registrierten Eingabestand und das neue Abbild (Fable 23a–23f, TB-94, 23.09.2026)

⭐ **Reines Eintragen von Registertext und Tatsachen**, wie 34 bis 38. Der
Vollzug von Plan-Punkt 8 ist **im Code** seit `0292e92` (TB-92) erbracht und
belegt; TB-92 hat danach **richtig abgebrochen**, weil 38.4 „grün" verlangte.
Dieser Abschnitt trägt den Vollzug **ins Register** nach: die Berichtigung des
Fertigkriteriums in 38.4 (39.1), den Vollzug der Form (ii) an Punkt 4 (39.2),
die Tatsachennotizen zu `_vt.json` und `_tb72.json` (39.3), den
Determinismusnachweis (39.4), die fünf Hash-Übergänge nach 37.3 (39.5), den
Modus-Nachweis (39.6), die Tatsachennotiz zu `herkunft.py::EINGEFROREN`
(39.7), die zwei Eingaben ohne registrierten Eingabestand (39.8), das neue
Abbild (39.9) und den Schlussteil (39.10). Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-23a_gruen_und_tabelle.md`, `…23b_neurechnung_nach_a.md`,
`…23c_messgroessen_und_vollzug.md`, `…23d_dritte_leserin_und_eingabestand.md`,
`…23e_nachweislauf_im_modus.md`, `…23f_fertigkriterium_38_4.md` und
`…22g_sonde_vor_dem_tag.md` — **eingesetzt, nicht abgetippt** (Beleg
`docs/belege/TB-94/e2_zitate.txt`, je Zitat `diff` rc 0). Auftrag
`docs/auftraege/MAC_TB-94_register_39.md`; Belege `docs/belege/TB-94/`; Eingang
`fcc3265`, Schritt-0-Commit `12f6089`. Messungen der Vorgänger: TB-91
(`docs/ERGEBNIS_TB-91_benchmark_absichern_und_neurechnung.md`, Belege
`docs/belege/TB-91/`) und TB-92 (`docs/ERGEBNIS_TB-92_vollzug_punkt8.md`,
Belege `docs/belege/TB-92/`), in TB-94 an den Belegen und an den Hashes
nachgemessen (`a1_hashes.txt`).
⛔ **Keine `.py` geändert, nichts gerechnet** — 39.10.

⭐ **Zum Zwischenstand zwischen `fcc3265` und diesem Eintrag** (Repo vollzogen,
Register nicht), Fable 23f Abschnitt 3, zeichengleich:

> **Zum Zwischenzustand über Nacht:** Er ist zulässig, weil er **benannt** ist — diese Anfrage und diese Antwort liegen beide in der Ablage, der Commit `fcc3265` ist der Stand, und der Registerauftrag ist der nächste Schritt. Was das Verfahren nicht duldet, ist ein **stiller** Abstand zwischen Repo und Register; ein benannter mit Datum und Folgeauftrag ist ein Zwischenstand wie jeder andere vor dem Tag. Nichts zurücknehmen.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (Abschnitt 10
Punkt 4; 38.4 zweimal; 21.9; 38.7 (d); 37.2; 37.3; 23.7; 33.2; 37.4 — zehn).
Die alten Sätze bleiben zeichengleich — **auch der Satz mit „grün" in 38.4**;
`git diff --numstat` auf dieses Register zeigt für TB-94 in der zweiten Spalte
`0`. ⭐ **Neu gegenüber 34–38:** Punkt 4 in Abschnitt 10 bekommt eine
**Pfadzeile** — drei eingerückte Folgezeilen **nach** der Zeile
`   Interpolationsregel**`, die vier Zeilen davor zeichengleich. Das ist der
Vollzug selbst (39.2), keine Marke; er ist additiv, weil die Sperrliste nach
Form (ii) nichts streicht. Fundstellen stehen nach 38.2 als Datei und
Bezeichner; Zeilennummern nur in Tatsachennotizen, mit Commit.

### 39.1 ⭐⭐ Berichtigung zu 38.4 — das Fertigkriterium von Plan-Punkt 8

⚠️ **Der Anlass:** 38.4 trägt als Fertigkriterium Fables Satz aus **22h**
(„`test_vorregistrierung.py` grün — die roten Prüfungen misst TB-88 —"). Fable
hat dieses Kriterium in **23a** zurückgenommen und ersetzt; **die Rücknahme ist
nie als Ersatztext an 38.4 eingetragen worden.** TB-92 hat sich an das
Register gehalten: Der Test lief bis zur Schlusszeile, war aber **163/2**
(`G6`, `H3`) — nicht grün —, und TB-92 hat abgebrochen, statt zwischen
Register und Antwortdatei zu wählen (`docs/ERGEBNIS_TB-92_vollzug_punkt8.md`,
Abschnitt 3). ⭐ **Das war das richtige Verhalten und wird hier ausdrücklich so
festgehalten.**

**Fable, 23f Abschnitt 2, zeichengleich — der Befund an sich selbst:**

> Der Widerspruch ist meiner, und er hat eine einfache Geschichte: 38.4 trägt meinen Text aus **22h** („grün — die roten Prüfungen misst TB-88"). **23a** hat dieses Kriterium ausdrücklich zurückgenommen — „Mein Satz ‚fertig, wenn `test_vorregistrierung.py` grün' hat zwei Dinge vermischt: eine Tag-Vorbedingung und ein Fertigkriterium für einen Punkt" — und ersetzt: fertig, wenn der Absturz weg ist und der Test bis zur Schlusszeile läuft; G6/H3 eigener Punkt. 23d hat das wiederholt. **Was fehlt, ist die Berichtigung von 38.4 im Register** — 23a ist als Antwort abgelegt, aber nie als Ersatztext an 38.4 eingetragen worden. Die Mac-Sitzung hat den Registertext gelesen, nicht meine Antwortdatei, und das ist richtig so: **Für eine ausführende Sitzung gilt das Register, nicht Fable.** Der Fehler liegt darin, dass 23a eine Berichtigung enthielt, ohne sie als solche zu adressieren; ich habe „Fertigkriterium" geschrieben und nicht „Berichtigung zu 38.4".

⭐ **Die Rangfolge, die daraus folgt, zeichengleich:** *„Für eine ausführende Sitzung gilt das Register, nicht Fable."*

**Der Ersatztext, zeichengleich:**

> **Berichtigung zu 38.4, Ersatztext (aus 23a, zeichengleich in der Sache):** Punkt 8 ist fertig, wenn: Registertext eingetragen (Form (ii)), Tatsachennotiz mit altem und neuem Hash, alle drei Leser (`auswertung.py`, `registerbericht.py`, `test_vorregistrierung.py`) lesen die vollzogene Tabelle über eine Konstante, der Absturz ist weg und `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**, Modus-Nachweis bytegleich (23e), neues Abbild, Sonde 0 für die Pfade. **Der Ausgang einzelner Prüfungen ist nicht Fertigkriterium von Punkt 8.** „Null rote Prüfungen" ist Tag-Vorbedingung (21.9, A4) und wird durch den eigenen Punkt „Testannahmen folgen dem Register" erreicht. Der Einschub „die roten Prüfungen misst TB-88" in der alten Fassung war der Hinweis in diese Richtung; das Wort „grün" davor war der Fehler.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 23a, Abschnitt 2 — ein Fertigkriterium hängt an dem, was der Punkt ändert; sonst haftet ein Punkt für fremde Fehler und wird nie fertig. Kein Ergebnis.

**Seine Regel an sich selbst, zeichengleich:**

> **Und eine Regel für mich, damit das nicht wieder passiert:** Wenn eine Antwort von mir einen Registertext ändert, den eine frühere Antwort gesetzt hat, **nennt sie ihn als Berichtigung mit Abschnittsnummer** — nicht als neue Entscheidung. Eure Regel „nicht übernehmen, nachmessen" gilt für meine Texte gegen das Register genauso wie für eure gegen den Code.

**Die Entscheidung in 23a, auf die der Ersatztext zurückgeht, zeichengleich**
(Abschnitt 2 — die Entscheidung und der neue Planpunkt):

> **Punkt 8 ist fertig, wenn:** Registertext eingetragen (Form (ii)), Tatsachennotiz mit altem und neuem Hash, `registerbericht.py` liest `symbole_handelbar_in_falte` (23.5), **der Absturz (`KeyError` an der Faltenzuordnung) ist weg** und `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**, neues Abbild, Sonde 0 für die Pfade. Der Ausgang der einzelnen Prüfungen ist nicht Fertigkriterium von Punkt 8.
>
> **Neuer Planpunkt vor dem Tag — „Testannahmen folgen dem Register":** `test_vorregistrierung.py` ist der Nachweis von Abschnitt 12 („150 Prüfungen, acht Mutationsproben"). Jede Prüfung, deren Annahme dem Register hinterherhinkt, wird an das Register angepasst — nie umgekehrt, und nie gelöscht. Für G6: Faltennamen kommen aus dem Faltenplan (Abbild 33.3), nicht als Literale `"2020"`, `"2022"`. Für H3: Eine Mutationsprobe, die nicht mehr beisst, wird so gestellt, dass sie **mit der registrierten Faltenzahl** beisst (und die Mutationsprobe selbst bleibt Pflicht — eine Probe, die immer besteht, ist keine). **Tag-Vorbedingung nach 21.9 und A4: null rote Prüfungen, null „bekannt rot".** (3) ist damit ausgeschlossen, wie ihr sagt.

**Der Grund in 23a, zeichengleich:**

> Mein Satz „fertig, wenn `test_vorregistrierung.py` grün" hat zwei Dinge vermischt: eine **Tag-Vorbedingung** (21.9: der Test blockiert den Tag, solange er rot ist) und ein **Fertigkriterium für einen Punkt**. Das Fertigkriterium eines Punktes muss an dem hängen, was der Punkt ändert — sonst wird ein Punkt nie fertig, weil er für fremde Fehler haftet.

⇒ **Was ab hier gilt:**

| | |
|---|---|
| Fertigkriterium von Plan-Punkt 8 | der **Ersatztext oben** (23f/23a). Der Satz in 38.4 („`test_vorregistrierung.py` grün — die roten Prüfungen misst TB-88 —") bleibt **zeichengleich** stehen und trägt eine ERSETZT-Marke |
| Die offene Frage in 38.7 (d) („bleibt ‚grün' Fertigkriterium?") | **beantwortet** — Lesart (1) der Anfrage 22i: fertig, wenn der Absturz weg ist; `G6`/`H3` sind ein eigener Punkt |
| 21.9, Tabelle der Folgen, erste Zeile („bleibt **rot** … offen durch eigene Änderung — blockierend für den Tag") | **gilt unverändert für den Tag.** „Null rote Prüfungen, null ‚bekannt rot'" ist Tag-Vorbedingung (23a); sie wird mit dem Planpunkt „Testannahmen folgen dem Register" erreicht (`G6`, `H3`; TB-95), nicht mit Punkt 8 |

**Tatsachennotiz — was TB-92 gemessen hat (`docs/belege/TB-92/b1_ausgabe.txt`,
HEAD `0292e92`):** `trading-env/bin/python3
research/vorregistrierung/test_vorregistrierung.py` — Teil A bis H
durchlaufen, **Schlusszeile erreicht**, der `KeyError: '2017'` ist weg; **163
bestanden, 2 gescheitert** (`G6`, `H3`), rc `1`, 501 s. `G6` und `H3` werden in
diesem Abschnitt **weder gemessen noch erklärt noch angepasst** (TB-95).

**Marken am alten Ort:** bei **38.4**, direkt unter dem Zitat mit „grün"; bei
**21.9**, unter der Tabelle der Folgen; bei **38.7 (d)**, unter der offenen
Frage.

### 39.2 ⭐⭐ Vollzug von Sperrlistenpunkt 4 in Form (ii)

⭐⭐ **Der Punkttext von Abschnitt 10, Punkt 4, ist geändert — additiv.** Nach
der Zeile `   Interpolationsregel**` stehen drei neue Folgezeilen:

```
   — und, als die Tabelle, die der Lauf liest,
   `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (Vollzug der
   Form (ii), 39.2, 23.09.2026)
```

Die vier Zeilen davor und der Kasten aus 38.4 darunter sind zeichengleich; der
Kasten trägt jetzt die Vollzugsmarke. Punkt 4 nennt damit:

| Datei | Rolle | sha256 |
|---|---|---|
| `benchmark.py` | Erzeuger (Punkte 4 und 6), unverändert seit TB-91 | `d6bdd558…` |
| `ergebnisse/benchmark_drawdowns.json` | **registrierter historischer Stand**, gesperrt und byteweise unverändert — wie Punkt 2 (30.3) | `a163c498…` |
| `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` | **die Tabelle, die der Lauf liest** | `64fb2912…` |

(Gemessen in TB-94 am Stand `12f6089`, `a1_hashes.txt`; volle Hashes dort und
in 39.5.)

**Die Bedingung, nach der diese Datei die Tabelle ist — Fable, 23a Abschnitt 3,
zeichengleich (Registertext zu Sperrlistenpunkt 4 / 23 / 33, die Wache und die
Folge für den Vollzug):**

> **Registertext zu Sperrlistenpunkt 4 / 23 / 33:** Die Benchmark-Tabelle, die der Lauf liest, ist auf dem registrierten Faltenplan (33.2) gerechnet: Für jeden Bot ist die Faltenmenge der Tabelle gleich der Menge seiner Selektionsfalten nach 33.2 (plus Bestätigungsperiode, sofern die Tabelle sie führt) — nicht mehr, nicht weniger —, und ihre Benchmark-Definition ist die aus 23 (tagesgenau). Eine Tabelle, die diese Bedingung für auch nur einen Bot nicht erfüllt, wird nicht vollzogen; sie bleibt liegen und erhält eine Tatsachennotiz, auf welchem Planstand sie gerechnet wurde.
>
> **Wache (in den Vollzug und in den Laufwrapper):** Faltenmenge der vollzogenen Tabelle je Bot gegen das Abbild des Faltenplans — Abweichung ist 1, fehlende Datei 2. Der `KeyError '2017'` von heute ist genau dieser Befund, nur als Absturz statt als Wache.
>
> **Folge für den Vollzug:** Es wird **eine** Tabelle für alle neun Bots vollzogen, keine Mischung. Welche Datei das ist, entscheidet die Bedingung, nicht der Name: Ist `benchmark_drawdowns_tb72.json` für alle neun Bots auf 33.2 gerechnet und tagesgenau nach 23, dann ist sie die Tabelle, und `_vt.json` erhält eine Tatsachennotiz als Zwischenstand (23, vor 25); die Gruppe „bestimmt" in 37.2 wechselt entsprechend. Erfüllt keine vorhandene Tabelle die Bedingung für alle neun, wird die Tabelle **einmal neu gerechnet** — mit `benchmark.py` (Punkt 4/6), auf dem Abbild des Faltenplans, mit Beleg und Hash, vor dem Tag.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 23.7 („der Widerspruch zwischen berichtigtem Faltenplan und gesperrter Benchmark-Tabelle … wird mit demselben Amendment geschlossen") — geschlossen heisst: die Tabelle folgt dem Plan, nicht der Plan der Tabelle. Und 24.3 als Bauart: Die Regel steht hier, **bevor** ich weiss, welche Datei sie erfüllt; die Werte kenne ich nicht und brauche sie nicht. Kein Ergebnis.

**Und die Entscheidung, sie einmal neu zu rechnen — 23b Abschnitt 2,
zeichengleich:**

> **Ergänzung zu 23a, Abschnitt 3 (Registertext zu Sperrlistenpunkt 4):** Die Tabelle, die der Lauf liest, wird **nach** der Umsetzung von Weg (A) (Punkt 3, TB-90) **einmal** neu gerechnet — mit `benchmark.py` (Sperrlistenpunkt 4/6, unverändert), auf dem dann gültigen Plan, mit `--ziel` auf einen neuen Pfad nach der Schreibregel 36.1, mit Beleg und Hash. Ihre Bestätigungszeile trägt den Bezeichner nach 35 (`2026-01-01/2026-09-01`).

⇒ **Warum diese Datei und nicht `_vt.json`:** 23a hat die Bedingung gesetzt
(Faltenmenge je Bot gleich den Selektionsfalten nach 33.2, plus
Bestätigungsperiode; Benchmark tagesgenau nach 23; **keine Mischung** aus zwei
Tabellen), 23b hat entschieden, dass **einmal neu gerechnet** wird, und TB-91
hat sie gerechnet (`31008b6`, 39.4). ⭐ **Damit ist die zweite offene Frage aus
38.4 („welche Tabelle für `t3_supertrend`") beantwortet:** keine vorhandene —
die Neurechnung, für alle neun.

**Wie die drei Leser sie lesen — Fable, 23d Abschnitt 1, zeichengleich:**

> **Zu Sperrlistenpunkt 4, Vollzug, Schritt 1a:** `auswertung.py` liest die vollzogene Tabelle über **eine** Konstante am Modulanfang, deren Wert der registrierte Pfad der neuen Tabelle ist. **Kein Kommandozeilenschalter** — Abschnitt 12 sagt „`auswertung.py` hat keinen Schalter", und eine Option, die bestimmt, welche Tabelle gilt, wäre einer. Bedingungen: AST-Vergleich aller Funktionskörper unverändert; genau eine Zuweisung verändert (die Pfadkonstante); `test_vorregistrierung.py` und `beispieldaten.py` lesen dieselbe Konstante, damit Test und Lauf nicht auseinanderfallen können; Tatsachennotiz mit altem und neuem Hash von `auswertung.py`. Die Änderung geschieht in demselben Auftrag wie der Vollzug (TB-92), nicht danach.

**Tatsachennotiz — umgesetzt in TB-92, `0292e92`
(`docs/belege/TB-92/a1a_ast_vergleich.txt`, `a5_hashes_nachher.txt`):**
`research/vorregistrierung/auswertung.py` trägt **eine** Konstante
`BENCHMARK_TABELLE` (Pfad der Neurechnung), `main` öffnet sie; ⛔ **kein
Schalter** (Abschnitt 12). AST-Vergleich: 27 Funktionen und Klassen, **26
gleich**, verschieden nur `main` und dort nur im Argument von `open`; auf
Modulebene **genau eine neue Zuweisung** (`BENCHMARK_TABELLE`), keine entfernt.
`registerbericht.py` (Funktion `block`) und `test_vorregistrierung.py`
(Funktion `_tabellen`) lesen `aw.BENCHMARK_TABELLE`; `registerbericht.py` liest
dort den Schlüssel `symbole_handelbar_in_falte` (23.5) statt
`symbole_point_in_time` — der alte Schlüssel kam genau **einmal** vor.
⚠️ **`beispieldaten.py` liest keine Tabelle** (Hash `3e547014…` unverändert,
in TB-94 nachgemessen): Die vierte Leserin, die 23d („`test_vorregistrierung.py`
und `beispieldaten.py` lesen dieselbe Konstante") voraussetzt, gibt es nicht.
Repo-weit sind es **drei** Leser, wie TB-88 (38.4, Tatsachennotiz M5) gemessen
hat.

**Marken am alten Ort:** bei **Abschnitt 10, Punkt 4** (Vollzug); bei **38.4**,
am Ende (Form (ii) vollzogen).

### 39.3 Tatsachennotizen zu `_vt.json` und `_tb72.json` — und die Gruppe „bestimmt"

**Fable, 23b Abschnitt 2, zeichengleich:**

> `benchmark_drawdowns_vt.json` und `benchmark_drawdowns_tb72.json` bleiben unverändert liegen, erhalten je eine Tatsachennotiz (Planstand, auf dem sie gerechnet wurden; TB-66 bzw. TB-72) und kommen **nicht** auf die Sperrliste; die Gruppe „bestimmt" in 37.2 wechselt auf die neue Tabelle. Sperrlistenpunkt 4 nach Form (ii): `benchmark_drawdowns.json` als registrierter historischer Stand, die neue Tabelle als die, die der Lauf liest.

**Die Tatsachennotizen (in TB-94 nachgemessen, `a1_hashes.txt`):**

| Datei | gerechnet auf Planstand | Bestätigungszeile | sha256 | Sperrliste |
|---|---|---|---|---|
| `ergebnisse/benchmark_drawdowns_vt.json` | **TB-66** (tagesgenau nach 23, vor 25); `t3_supertrend` mit einer Falte `2018`, die der Plan seit TB-72 nicht mehr hat | alter Name (`2026` bzw. `2026-2027`) | `4549395f…` | ⛔ **nicht** |
| `ergebnisse/benchmark_drawdowns_tb72.json` | **TB-72** | alter Name (`2026` bzw. `2026-2027`) | `e4ba341d…` | ⛔ **nicht** |

Beide bleiben unverändert liegen. Die Neurechnung reproduziert `_tb72.json` in
allen Werten (39.4); `_vt.json` weicht von `_tb72.json` an **101** Blattwerten
ab (Selbsttest des Vergleichers, TB-91; Werte nach 27.1 nicht wiedergegeben).

⭐ **Folge für 37.2 (Gruppe „bestimmt"):** Die Gruppe nannte bisher
`ergebnisse/benchmark_drawdowns_vt.json`. Nach 23b **wechselt sie auf die neue
Tabelle** — und weil deren Pfad seit 39.2 in Punkt 4 steht, hat sie ihren
Punkt: **Die Gruppe „bestimmt" ist nach dem Registertext leer.** 37.2 verlangt
genau das für den Tag: *„Am Tag ist die zweite Gruppe leer."*

⚠️ **Tatsachennotiz — was die Sonde dazu meldet (TB-87 gemessen, in TB-94
nachgemessen):** Die Sonde führt die Gruppe nicht aus dem Abbild, sondern aus
einer **festen Konstante** in `shared/sperrlistensonde.py`
(`BESTIMMT_NICHT_EINGETRAGEN`, am Stand `12f6089` ein Eintrag:
`ergebnisse/benchmark_drawdowns_vt.json`, Begründungstext „Register
21.9/23.7 - fuer die Sperrliste bestimmt, Vollzug steht aus"); sie **nennt**
den Pfad, **prüft** ihn nicht (37.2, Tatsachennotiz TB-87). ⇒ Nach diesem
Eintrag und dem neuen Abbild meldet die Sonde dort weiter `_vt.json` mit
„Vollzug steht aus" — **das ist seit 39.2 sachlich überholt**, und die Sonde
kann es nicht wissen, weil die Konstante Code ist. ⛔ Die Sonde wird hier
**nicht** geändert (keine `.py`, 39.10). Die leere Gruppe ist Teil des
Sonden-Entwurfs aus TB-92 (`docs/belege/TB-92/sonde_je_datei_entwurf.patch`),
Handwerk mit eigener Freigabe. Was die Sonde nach dem neuen Abbild tatsächlich
ausgibt, steht in 39.9.

**Marke am alten Ort:** bei **37.2**, unter der Tatsachennotiz TB-87.

### 39.4 ⭐⭐ Determinismusnotiz — die Neurechnung reproduziert `_tb72.json` (TB-91, Bedingung aus 23b)

**Fables Bedingung, 23b Abschnitt 2, zeichengleich:**

> **Bedingung an die Neurechnung — der Determinismusnachweis:** Die neu gerechnete Tabelle muss `benchmark_drawdowns_tb72.json` für **alle neun Bots in allen Werten reproduzieren**; der einzige zulässige Unterschied ist der Name der Bestätigungszeile (und, sofern die Tabelle ihn führt, ein Feld, das diesen Namen wiederholt). Ein `diff`, der etwas anderes zeigt, ist ein **Befund**, kein Ergebnis: Dann hat sich zwischen TB-72 und TB-90 etwas bewegt, das nicht der Name ist — Plan, Daten oder Code —, und das ist vor dem Vollzug zu klären, nicht wegzurechnen. Die Tabelle wird in diesem Fall **nicht** vollzogen.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 35.1 (Bezeichner ist die Spanne, ein anderer ist unzulässig), 23a (Tabelle folgt dem Plan; Neurechnung dort schon vorgesehen), 36.1 (Schreibregel). Und die Bedingung ist 10.1 in Anwendung: Erlaubt sind nur Änderungen mit **bitidentischen** Ergebnissen — die Neurechnung ändert einen Namen, also müssen alle Zahlen gleich bleiben, und wenn sie es sind, ist das zugleich der Nachweis, dass `benchmark.py` deterministisch ist und der Plan sich seit TB-72 nicht bewegt hat (32 hat es behauptet; hier wird es an der Tabelle gemessen). **Kein Ergebnis:** Ich verlange Gleichheit mit einer Tabelle, deren Werte ich nicht kenne; ob sie „gut" oder „schlecht" sind, spielt für die Regel keine Rolle, und sie darf nach 27.1 auch nicht wiedergegeben werden — die Sonde meldet nur „gleich" oder „an Stelle X verschieden".

**Das Ergebnis (TB-91, `docs/belege/TB-91/c_determinismus_ergebnis.txt`,
`c_gegenprobe_text.txt`, `b_neurechnung_lauf.txt`; in TB-94 an den Belegen
nachgelesen) — ⚠️ ohne Werte, Sichtschutz 27.1:**

| | |
|---|---|
| Lauf | `trading-env/bin/python3 -W ignore research/vorregistrierung/benchmark.py --ziel research/vorregistrierung/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`, `benchmark.py` `d6bdd558…`, HEAD `31008b6`, **rc 0, 56 s** |
| Vergleich | gegen `benchmark_drawdowns_tb72.json` (`e4ba341d…`), rekursiv bis zum Blatt, Typ **und** Wert: **9 Bots, 77 Falten, 63 Botfelder, 9750 Blattwerte** |
| Abweichungen | **0 ausser dem Namen der Bestätigungszeile** (9/9: `2026` bzw. bei `elliott_wave` `2026-2027` → `2026-01-01/2026-09-01`); `dd_toleranz` 9/9 gleich; `status` 9/9 `endgueltig` |
| Gegenprobe auf Textebene | `_tb72.json` geladen, Bestätigungsfalte umbenannt, mit `indent=1, ensure_ascii=False, sort_keys=True` und Schluss-`"\n"` geschrieben → sha256 `64fb2912…`, **bytegleich** mit der Neurechnung |
| ⭐ Selbsttest des Vergleichers | `_tb72` gegen sich selbst **0** Abweichungen; `_tb72` gegen `_vt` **101** — *ein Vergleich, der nichts finden kann, ist keiner* |
| ⭐ Die Wache aus 23a (TB-91 Block D, `d_falten_abgleich_ergebnis.txt`) | Faltenmenge der Tabelle je Bot gegen den Plan im Speicher (`faltenplan.py` `7aa0b8cc…`): **18/18 gleich** (9 Bots × zwei Einstufungen, alle und Selektion), Bestätigungszeile **9/9** gleich der `bestaetigungsperiode` des Plans. Keine Falte fehlt, keine ist zusätzlich |

⇒ **Damit ist Festlegung 32 an der Tabelle gemessen:** Zwischen TB-72 und
TB-91 hat sich an den Benchmark-Drawdowns nichts bewegt ausser dem Namen der
Bestätigungszeile — und `benchmark.py` ist in diesem Umfang deterministisch.

### 39.5 ⭐⭐ Tatsachennotizen zu 37.3 — die fünf Hash-Übergänge

37.3 verlangt für jeden planmässigen Befund vor dem Tag: Auftrag, Freigabe,
alter und neuer Hash. **Vier davon standen bisher nicht im Register.** Alle
fünf, mit **vollem** Hash, gemessen in TB-94 aus der Historie
(`git show <commit>^:<pfad>` bzw. `<commit>:<pfad>`, `a1_hashes.txt`); die
Freigaben aus den Auftragsdokumenten nachgelesen:

| Datei | alt → neu | Auftrag / Commit | Freigabe | Sperrlistenpunkte |
|---|---|---|---|---|
| `research/vorregistrierung/faltenplan.py` | `6f96b95d13563f73b11be69c2bd6996037854df794da61315029216ad0b22bd9` → `fd3e5018ae930c2e29747562a140506d5d9a6bb70b87e96cf5c0089e09afdd79` | TB-86, `4daa254` | Betreiber 22.09.2026, 07:50 | 2 — *bereits in 37.3 notiert* |
| `research/vorregistrierung/faltenplan.py` | `fd3e5018ae930c2e29747562a140506d5d9a6bb70b87e96cf5c0089e09afdd79` → `7aa0b8ccf5619a21d5f082f68d81cb412f98ae9c9724e799da8b48dce7498cfb` | TB-90 (Weg (A), 38.1), `303a7fd` | Betreiber 22.09.2026 (`MAC_TB-90`, Kopf) | 2 — **neu** |
| `research/vorregistrierung/benchmark.py` | `3960375a539de8324ccfafaa42596a056fb5dd5c154cd2e05c0ba6a634f3611b` → `d6bdd55805344da09b6b43d791267b43c9702687fc1c7cdbad1473079443e061` | TB-91 (nach 36.1 abgesichert), `31008b6` | Betreiber 23.09.2026, 10:40 | **4 und 6** — neu |
| `research/vorregistrierung/auswertung.py` | `1c2e2daec562d9973f87809fd29ef369db76614ee4bc31c04c6ca201c52a3db0` → `c3b4e69d8f207d0c1982a538203dcf184072554fdc1beb0f612bf054cd2a0062` | TB-92 (39.2), `0292e92` | Betreiber 23.09.2026, 18:12, und Fable 23d | **3, 5 und 14** — neu |
| `research/vorregistrierung/registerbericht.py` | `2b1ce24a8f9b2ece8c98fe2aa84f1f5fdc6ac3da544c0aa765e381505bb1d78f` → `dace1b01826fa6a999beb9a15a8eda41a4e0c97dec584e451cfc0d9b26daac01` | TB-92, `0292e92` | dieselbe | ⭐ **auf keinem Punkt** — nur Tatsachennotiz |
| `research/vorregistrierung/test_vorregistrierung.py` | `55553739c819b78de2f7ac608af2341ec43b7c856c3e8699d5a6ffde67bd15c0` → `6e7defefb46903ccec8df60a350136f5961c137b45fb1a921407e7a8e76f3fbe` | TB-92, `0292e92` | dieselbe | ⭐ **auf keinem Punkt** — nur Tatsachennotiz |

Seit dem jeweiligen Commit hat sich keine der sechs Dateien bewegt (letzter
Commit je Datei = der genannte; Hashes am Stand `12f6089` = „neu").
⭐ **Nach 37.3 ist jeder dieser Befunde der planmässige Fall vor dem Tag** —
Auftrag, Freigabe, alter und neuer Hash stehen hiermit als Tatsachennotiz.
Geschlossen werden sie mit **einem** neuen Abbild (39.9); das alte bleibt.

⚠️ **Zählweise, damit niemand einen Widerspruch liest:** Die sechs Befunde der
Sonde gegen `sperrliste_abbild_2026-09-22.json` (Punkte 2, 3, 4, 5, 6, 14;
`docs/belege/TB-94/a2_sonde_vorher.txt`) stammen aus **drei** Dateien, nicht
aus sechs Änderungen: `faltenplan.py` an 2, `benchmark.py` an 4 und 6,
`auswertung.py` allein an 3, 5 und 14.

⭐ **Ein Fund aus TB-91, der nicht auf TB-91 beschränkt ist — Fables
Tatsachennotiz dazu, 23c Abschnitt 3, zeichengleich:**

> **Tatsachennotiz zu 36.5/37 (kein neuer Registertext):** Ein Punkt mit unmessbaren Bestandteilen wechselt von 2 auf 1, sobald ein messbarer Bestandteil abweicht (erstmals beobachtet TB-91: Punkte 4 und 6 durch `benchmark.py`, planmässig nach 37.3). Die Zahl der Punkte mit 2 ist keine Kenngrösse des Registers, sondern des jeweiligen Standes. Die Sonde meldet je Punkt; eine Datei, die an mehreren Punkten vorkommt, erzeugt eine Tatsachennotiz.

⇒ `A2` („konnte nicht messen ist ein eigenes Ergebnis") heisst **nicht** „bleibt
für immer unmessbar", und die Zahl der nicht prüfbaren Punkte ist keine feste
Grösse. Eine Bilanz mit mehr Punkten `1` ist deshalb nicht schlechter als eine
mit mehr Punkten `2`; sie zeigt nur, welche Dateien sich bewegt haben.

**Marke am alten Ort:** bei **37.3**, unter der Tatsachennotiz zu TB-86.

### 39.6 ⭐ Der Modus-Nachweis — die vollzogene Tabelle ist aus dem registrierten Snapshot bytegleich reproduzierbar (Fable 23e, TB-92 A1b)

**Fables Forderung, 23e Abschnitt 2, zeichengleich (Präzisierung zu 23d,
Registertext „Eingabestand"):**

> Der Reproduzierbarkeitsnachweis einer Eingabedatei wird **im Selektionsmodus** geführt — der Erzeuger liest aus `snapshots/<hash>/`, nicht aus `data/`, mit `--ziel` auf einen Beleg-Pfad; das Ergebnis muss bytegleich zur eingefrorenen Datei sein. Die Tatsachennotiz nennt Snapshot-Hash, Code-Commit und den Modus. Dass `data/` zum Messzeitpunkt bytegleich zum Snapshot war, ist eine eigene Tatsache und ersetzt den Modus-Lauf nicht: Der Lauf am Tag liest den Snapshot-Pfad, und der Nachweis muss denselben Weg gehen wie der Lauf.

**Und die Folge, die er für die Benchmark-Tabelle nennt, zeichengleich:**

> - **TB-92:** dasselbe für die Benchmark-Tabelle aus TB-91 — `benchmark.py` im Selektionsmodus, `--ziel` Beleg-Pfad, `diff` gegen `benchmark_drawdowns_2026-09-23_nach_wegA.json` → bytegleich. Das ist nicht die „Vorab-Nachrechnung" aus 23d, die mit Messbitte (b) entfallen ist (die fragte nach anderen Eingaben); es ist der Nachweis, dass der Erzeuger im Modus dasselbe tut wie ausserhalb. Wenn `benchmark.py` länger braucht als elf Sekunden, ist das Handwerk — der Nachweis gehört trotzdem vor den Tag, einmal.

**Das Ergebnis (TB-92, `docs/belege/TB-92/a1b_ergebnis.txt`,
`a1b_ergebnis_kinder.txt`, `a1b_lesequellen_kinder.txt`; in TB-94 an den
Belegen nachgelesen):**

| | |
|---|---|
| Wurzel | Snapshot `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` (Register 18), MANIFEST-`datenstand_hash` `d9449faf…`; `data/` war zum Messzeitpunkt **225/225** Dateien byteweise gleich dem Snapshot (Anfrage 23g, von Fable in 23e zur Kenntnis genommen) — ⚠️ nach 23e eine eigene Tatsache, die den Modus-Lauf **nicht** ersetzt |
| Umlenkung | `TB30A_BASE_DIR` auf einen Hilfsordner, dessen `data/` (223 Verknüpfungen) und `config/` auf den Snapshot zeigen. ⚠️ `TB_SELEKTIONSWURZEL` wirkt in `research/vorregistrierung/` **nicht** (0 Treffer) — der „Modus" ist hier die Umlenkung auf den Snapshot, wie in TB-93 |
| Code-Commit | `d136251` (`benchmark.py` `d6bdd558…`, `faltenplan.py` `7aa0b8cc…`) |
| ⭐ Ergebnis | **Vier Läufe, alle rc 0, je 51–52 s, alle bytegleich** `64fb2912…` mit `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`. Lauf 1 nach `docs/belege/TB-92/benchmark_modusnachweis.json`, die übrigen ins Scratchpad; **nichts in `ergebnisse/` geschrieben** |
| ⭐ Lesequellen | Lesehaken über `sys.addaudithook`, in Lauf 3 und 4 prozessübergreifend über `sitecustomize` (**11 Prozesse**): **0 Lesezugriffe auf `data/` oder `config/` des Repos**; **222** CSV und **2** Universumsdateien aus dem Snapshot. Dazu Eingaben **ausserhalb** des Snapshots — 39.8 |

⇒ **Die vollzogene Tabelle ist aus dem eingefrorenen Datenstand byteweise
wiederherstellbar**, auf dem Weg, den der Lauf am Tag nimmt. Snapshot-Hash,
Code-Commit und Modus stehen damit neben ihrem Hash, wie 23e es verlangt.

⚠️ **Tatsachennotiz:** Der Registertext „Eingabestand eingefrorener
Ergebnisdateien" (23d Abschnitt 2), den 23e präzisiert, ist mit diesem
Abschnitt **nicht** eingetragen — nach 23d Abschnitt 4 gehört er zum Planpunkt
`messgroessen.json` (TB-96). Hier stehen nur die Tatsachen, die er für die
Benchmark-Tabelle verlangt.

> ⭐⭐ **Zweiter Anwendungsfall (40.6, Fable 24a, TB-96, 24.09.2026):** Neben
> `messgroessen.json` fallen die **neun TB-24-Listen** unter 23d
> („Eingabestand") in voller Form — Fables Registertext „Ergänzung zu 23d und
> zu 5.4" steht in **40.6**. Der Registertext „Eingabestand eingefrorener
> Ergebnisdateien" selbst ist weiter **nicht** eingetragen. ⚠️ Die Nummer oben
> ist gerückt: `messgroessen.json` ist **TB-101**, nicht TB-96 (40.9 (c)).

### 39.7 ⚠️ Tatsachennotiz — `herkunft.py::EINGEFROREN` zeigt weiter auf den historischen Stand

`research/vorregistrierung/herkunft.py` ist **unverändert** (`56a1c2e1…`,
TB-94 gemessen). Seine Liste `EINGEFROREN` hasht damit weiter
`ergebnisse/benchmark_drawdowns.json` — **nicht** die Tabelle, die der Lauf
liest. **Fable, 23d Abschnitt 1, zeichengleich:**

> **(2) `EINGEFROREN` bleibt, wie es ist — es trägt weiter den alten Pfad, nicht beide.** Der Grund ist nicht der Wortlaut, sondern der Ort: `EINGEFROREN` steht in `herkunft.py` (Punkte 11/12), und in 22d habe ich entschieden, `herkunft.py` nicht zu öffnen, weil die Sperrlisten-Sonde die Lücke schliesst. Das gilt hier genauso: Die **neue** Tabelle ist durch Punkt 4 und das Abbild geschützt (Sonde); die **alte** bleibt in `EINGEFROREN` als das, was sie ist — der registrierte historische Stand, dessen Hash `register()` bezeugt. Die Tatsachennotiz zu 37.4 wird um den Satz ergänzt: „`register()` bezeugt die Abschnitt-0-Menge vom 14.09.; die vollzogene Benchmark-Tabelle bezeugt Sperrlistenpunkt 4 über die Sonde." Zwei Nachweise, zwei Gegenstände, kein Widerspruch (22d).

⇒ Die neue Tabelle schützen **Punkt 4** (39.2) und **das Abbild** (39.9);
beides ist mit diesem Abschnitt erfüllt. ⭐ **Deshalb ist das eine
Tatsachennotiz und kein Befund** — aber sie gehört ins Register, damit niemand
`EINGEFROREN` für vollständig hält. Der Satz, um den Fable die Tatsachennotiz
zu 37.4 ergänzt, steht dort als Marke.

**Fables Präzisierung zu 36.1 (1), 23c Abschnitt 2, zeichengleich** — „gesperrt"
umfasst jeden Pfad, dessen Hash am Tag bezeugt wird, **auch
`herkunft.py::EINGEFROREN`**:

> **Präzisierung zu 36.1 (1):** „auf der Sperrliste steht oder für sie bestimmt ist" umfasst jeden Pfad, dessen Hash am Tag bezeugt wird — die Punkte des Abschnitts 10, die Gruppe „bestimmt" (37.2) **und die Einträge von `herkunft.py::EINGEFROREN`**, solange `register()` über sie hasht. Die Sperrlisten-Sonde führt diese Pfade als dritte Gruppe („Abschnitt 0") und prüft sie gleich.

⚠️ **Tatsachennotiz:** Die „dritte Gruppe" („Abschnitt 0") führt die Sonde
heute **nicht** — sie kennt `EINGEFROREN` nicht (Kopf von
`shared/sperrlistensonde.py`). Offen, Handwerk mit eigener Freigabe.

**Marke am alten Ort:** bei **37.4**, vor der Marke am alten Ort des
Abschnitts.

### 39.8 ⭐⭐ Der Lesehaken — zwei Eingaben ohne registrierten Eingabestand

Der Modus-Lauf (39.6) hat neben dem Snapshot **zwei weitere Eingabequellen im
Repo** geöffnet (`docs/belege/TB-92/a1b_lesequellen_kinder.txt`, Lauf 3 und 4
gleich):

| Eingabe | Tatsache |
|---|---|
| `research/vorregistrierung/ergebnisse/messgroessen.json` | ⚠️ beschreibt nach TB-93 einen Datenstand, den es nicht mehr gibt (Eingabestand vor `90e3cbd`, TB-34). Wird mit **TB-96** geschlossen (23d, 23e) |
| **neun** `research/tb24_haltedauern/daten/*_alle_trades.csv` | ⚠️ Ergebnisdateien, keine Kursdaten; weder auf der Sperrliste noch im Snapshot. Der Weg führt über den Faltenplan (TB-92) |

**Fable, 23f Abschnitt 6, zeichengleich — der Fund:**

> Die Sitzung hat protokolliert, was der Modus-Lauf öffnet: 222 aus `snapshot/csv`, 2 aus `snapshot/config`, **dazu `ergebnisse/messgroessen.json` und neun Trade-Listen aus dem Repo.** Das ist die Sonde „Lesequellen" als Laufzeitmessung — genau 5e —, und sie zeigt zweierlei: Erstens liest der Benchmark-Lauf die Messdatei, deren Eingabestand 23d beanstandet hat (das ist bekannt und wird mit TB-94 geschlossen). Zweitens **neun Trade-Listen**. Die sind Ergebnisdateien, keine Kursdaten, und sie stehen weder auf der Sperrliste noch im Snapshot.

⚠️ **Berichtigung einer Nummer, damit die Ablage lesbar bleibt:** Fable nennt
oben (und in 23e Abschnitt 2) für den Eingabestand von `messgroessen.json` die
Nummer **TB-94**; so stand es im Plan des steuernden Chats vom Vormittag des
23.09. Die Nummern sind danach gerückt, weil der Registervollzug vorgezogen
wurde (`docs/auftraege/AKTUELLER_AUFTRAG.md`, 23.09.2026, 20:00): **TB-94 ist
dieser Eintrag, TB-95 sind `G6`/`H3` und die Messbitte unten, TB-96 ist
`messgroessen.json`.** *Eine Nummer, die zwei Sachen meint, ist schlimmer als
eine verschobene.*

⚠️⚠️ **OFFEN — Fables Messbitte, eingetragen, nicht beantwortet** (23f
Abschnitt 6, zeichengleich):

> **Messbitte, nur das Ob:** Welcher Schritt des Modus-Laufs öffnet die neun Trade-Listen — `benchmark.py` selbst, oder ein Nebenweg (`registerdaten.py`, `faltenplan.py`, Trockenlauf)? Und **gehen ihre Inhalte in die Tabelle ein** — oder werden sie nur geöffnet (etwa für eine Konsistenzprüfung)? Wenn sie eingehen, hat die Benchmark-Tabelle eine Eingabe, deren Eingabestand nicht registriert ist — derselbe Fall wie `messgroessen.json`, und die Regel aus 23d gilt für sie. Wenn sie nur geöffnet werden, ist es eine Tatsachennotiz und ein Kandidat für die Lesequellen-Sonde.

**Seine Unsicherheit dazu, zeichengleich:**

> **Unsicher:** ob die neun Trade-Listen die TB-24-Listen sind (dann alter Code, alter Datenstand — 26.5) — das ändert nicht die Frage, nur ihr Gewicht.

⛔ **In TB-94 nicht gemessen und nicht beantwortet** — Gegenstand von TB-95.

**Zwei weitere Tatsachen aus TB-92 (`docs/ERGEBNIS_TB-92_vollzug_punkt8.md`,
Abschnitt 2, A1b-6), die hierher gehören:** (1) `benchmark.py` und
`messgroessen.py` lesen an `shared/paths.py` **vorbei** (`TB30A_BASE_DIR` bzw.
`<BASE>/data`); die Kindprozesse des Faltenplans folgen **eigenen** Variablen
(`faltenplan_neun.py` `TB36_BASE_DIR`, `universum_trockenlauf.py` und
`loaderlauf.py` `TB40_BASE_DIR`) und haben gemessen trotzdem aus dem Snapshot
gelesen. (2) Der Lauf öffnet `logs/notifications/manuelle_eingriffe.log` im
Modus `a` (Import aus `notifications/`); die Datei blieb unverändert (mtime
11.09.). Beides ist Stoff für Fables Sonde „Lesequellen" (23d), nicht für
diesen Eintrag.

⭐⭐ **Nachtrag zu 39.8 (40.5, Fable 24a, TB-96, 24.09.2026) — die Messbitte
oben ist beantwortet.** Gemessen in TB-95 (`069370d`; Belege
`docs/belege/TB-95/d1_wer_oeffnet.txt`, `d2_stoerprobe.txt`, `d3_antwort.md`),
im Modus-Lauf gegen den Snapshot `63e4b6c8…`, Sichtschutz 27.1 (keine
Ergebnisgrössen):

| | |
|---|---|
| **Wer öffnet** | **`benchmark.py` selbst**, kein Nebenweg: `benchmark.py::je_bot` → `faltenplan.py::faltenplan` → `_plan` → `faltenlaenge_jahre` → `gefundene_trades_je_jahr` (`read_csv`). Jede der neun Listen **genau einmal**, **nur im Hauptprozess**; die zehn Kindprozesse (Trockenlauf/Loader) und `registerdaten.py` öffnen keine davon |
| **Gehen sie ein?** | **Ja — über genau eine Grösse, die Faltenlänge.** Gelesen wird nur `entry_time`; gezählt je vollem Kalenderjahr, gemittelt, gegen die Schwelle aus 5.4 verglichen ⇒ Faltenlänge 1 oder 2 ⇒ Faltengrenzen ⇒ Tabellenzeilen. Sonst erreicht nichts aus den Listen die Tabelle |
| **Störprobe, in beide Richtungen** (auf Kopien, Originale vorher = nachher) | **eine Zeile weg ⇒ Tabelle bytegleich** (`64fb2912…`), weil die Schwelle nicht überschritten wird; **zwei von drei Zeilen weg ⇒ verschieden** (`97cf224f…`): **ein** Bot (`volatility_breakout_crypto`) kippt von Einjahres- auf Zweijahresfalten, die anderen **acht bleiben gleich** |
| **Herkunft** | ein einziger Commit, **`78e2bc6`, 13.09.2026, TB-24**, seitdem unverändert — die TB-24-Listen, gemessen an Pfad, Commit und Datum; vor TB-31/TB-34/TB-38 und vor dem Snapshot. **Nicht im Snapshot, nicht auf der Sperrliste**; im Register als Quelle genannt (5.4), **ohne Hash** |
| Nebenbefund | Derselbe Modus-Lauf lieferte die vollzogene Tabelle zum fünften Mal bytegleich (`64fb2912…`, 39.6) |

⚠️ **Der methodische Satz, der über den Fall hinausgeht:** Die Störprobe, wie
der Auftrag TB-95 sie vorschlug („eine Zeile entfernen genügt"), hätte
**allein das falsche „nein"** ergeben. Eine Eingabe, die über eine Schwelle
wirkt, zeigt bei kleinen Änderungen nichts; wer nur in eine Richtung stört,
misst die Schwelle nicht, sondern ihren Abstand. ⇒ Eine Störprobe nach „geht
es ein?" wird in **beide** Richtungen geführt: klein (bleibt gleich?) **und**
über eine bekannte Schwelle hinweg (ändert sich?).

⇒ **Die Einordnung steht in 40.6:** Die neun Listen sind Eingabedateien nach
23d in voller Form — Neu-Erzeugung auf dem Snapshot, Sperrlistenpunkt,
Ableitung der Faltenlänge nach 5.4 und Vergleich gegen 33.2 (TB-98). Die
Nummer 40.5 verweist hierher.

### 39.9 Das neue Abbild und die Sonde

**Was 36.6 und 37.3 verlangen:** Jede Fortschreibung der Sperrliste vor dem Tag
erzeugt ein **neues** Abbild unter neuem Namen; das alte bleibt und wird nie
angepasst; das aktuelle Abbild steht selbst mit Hash im Register. Ein Befund
`1` aus beauftragter Änderung wird durch Tatsachennotiz (39.5) und neues
Abbild geschlossen. **Fable, 22g, zeichengleich:** *„Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde."*

**Was die Sonde am Tag liefern muss — Fable, 23c Abschnitt 3, zeichengleich:**
*„Die Tag-Vorbedingung aus 22d/37 lautet: kein Pfad-Bestandteil 1, jede 2 mit Tatsachennotiz."*
⇒ „Sonde 0 für die Pfade" im Fertigkriterium (39.1) heisst: **jede Datei
jedes Punktes gleich** und Prüfung (ii) `0`. Ein Gesamtausgang `2` wegen
Punkten, die Nicht-Dateibezogenes nennen (Werte, Funktionen,
Registerverweise), ist damit vereinbar; er ist keine Aussage über die Pfade.

**Reihenfolge:** Das Abbild liest den Listentext von Abschnitt 10. Es wird
deshalb **nach** dem Commit gezogen, der Punkt 4 (39.2) und diesen Abschnitt
enthält, mit `research/vorregistrierung/sperrliste_abbild.py --ziel` (keine
Voreinstellung, Einmal-Schreibsperre). Name, Hash und die Bilanz der Sonde
davor und danach werden **unmittelbar unten** eingetragen, in einem eigenen
Commit — additiv, der Listentext von Abschnitt 10 wird dabei nicht berührt.

**Ergebnis (Block D, TB-94, 23.09.2026; `docs/belege/TB-94/d1_abbild.txt`,
`d2_sonde_nachher.txt`, `a2_sonde_vorher.txt`,
`b_sonde_nach_blockB_altes_abbild.txt`):**

| | |
|---|---|
| ⭐ Neues Abbild | `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-23.json`, **sha256 `2f23f76c99e22991e4a331ec1107dc0f090a425bc9e050793470ee3cd52dd4fe`**, 7351 Bytes, erzeugt 2026-09-23T18:21:35Z am Stand `27b68b9` (der Commit mit 39.2 und diesem Abschnitt), 14 Punkte aus Abschnitt 10 (Z. 845–958 am Stand `27b68b9`), 15 Pfadnennungen; `sperrliste_abbild.py --ziel` rc 0, Ziel existierte vorher nicht |
| Altes Abbild | `sperrliste_abbild_2026-09-22.json` `6a1b732e…` — **nicht gelöscht, nicht geändert** (36.6); vor und nach dem Ziehen gemessen |
| Sonde vorher (altes Abbild, Stand `12f6089`) | rc **1**; Befund an **2, 3, 4, 5, 6, 14** (drei Dateien, 39.5); (ii) `0`; Bilanz 0 / 6 / 8 |
| Sonde nach Block B und C (altes Abbild, uncommittet) | rc **1**; dazu (ii) **1** an Punkt 4, Felder `pfade` und `nicht_dateibezogen` — der neue Pfad. Das ist der erwartete Nachweis, dass die Sonde die Pfadzeile liest |
| ⭐ Sonde gegen das neue Abbild (Stand `27b68b9`) | rc **2**; **0 Befunde**; **alle 15 Pfadnennungen „gleich"**, darunter `ergebnisse/benchmark_drawdowns.json` `a163c498…` und `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` `64fb2912…`; Punkte **2 und 5** `0`; Punkte 1, 3, 4 und 6–14 `2`, jeder wegen Nicht-Dateibezogenem im Punkttext; (ii) `0`, Listentext wie bei Erzeugung: ja. Bilanz **2 / 0 / 12** |
| Gruppe „bestimmt" | die Sonde nennt weiter `ergebnisse/benchmark_drawdowns_vt.json` (`4549395f…`) mit „Vollzug steht aus" — die feste Konstante aus 39.3; nach dem Registertext ist die Gruppe leer |

⇒ **Die planmässigen Befunde aus 39.5 sind geschlossen: kein Pfad-Bestandteil
ist `1`.** Der Gesamtausgang `2` sagt nichts über die Pfade, sondern über
Werte, Funktionen und Registerverweise in den Punkttexten (A2, je Sache; 23c).
Punkt 4 steht auf `2`, nicht auf `0`, weil schon sein alter Text
„einschliesslich der Interpolationsregel" nennt; die Pfadzeile aus 39.2
bringt weiteren Wortlaut dazu, ändert am Ausgang aber nichts. ⚠️ Ob **jede**
`2` eine Tatsachennotiz trägt, ist Tag-Vorbedingung (23c) und hier **nicht**
geprüft.

⭐ **Das aktuelle Abbild der Sperrliste (36.6) ist damit
`sperrliste_abbild_2026-09-23.json`, `2f23f76c…`.**

### 39.10 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert** — weder `auswertung.py`, `registerbericht.py`, `test_vorregistrierung.py`, `benchmark.py`, `faltenplan.py`, `messgroessen.py`, `herkunft.py` noch `shared/sperrlistensonde.py` | — |
| ⛔ | **Nichts gerechnet** — `benchmark.py`, `faltenplan.py main()`, `messgroessen.py` nicht aufgerufen; in `research/vorregistrierung/ergebnisse/` nichts geschrieben **ausser dem neuen Abbild** (39.9) | — |
| ⛔ | **`G6`/`H3` nicht angefasst** — weder gemessen noch erklärt noch angepasst | TB-95 |
| ⛔ | **Fables Messbitte zu den neun Trade-Listen nicht beantwortet** (39.8) | TB-95 |
| ⛔ | **`messgroessen.json` nicht angefasst**; der Registertext „Eingabestand" (23d) nicht eingetragen (39.6) | TB-96 |
| ⛔ | **Der Sonden-Entwurf `sonde_je_datei_entwurf.patch` nicht angewandt**; die Konstante `BESTIMMT_NICHT_EINGETRAGEN` und die dritte Gruppe (39.3, 39.7) bleiben, wie sie sind | Handwerk, eigene Freigabe |
| ⛔ | **Kein alter Registersatz umgeschrieben** — der Satz mit „grün" in 38.4, die offene Frage in 38.7 (d), der Kasten an Punkt 4 und die Punktzeilen 1–4 von Punkt 4 bleiben zeichengleich; ERSETZT-, Vollzugs- und Hinweis-Marken, nichts entfernt | — |
| ⭐ | **`benchmark_drawdowns.json` byteweise unverändert** (`a163c498…`) — vor Block B, nach Block B und nach dem Abbild gemessen (`a1_hashes.txt`, `d1_abbild.txt`) | — |
| ⭐ | **N = 653 (Festlegung 10) unberührt**; Zellenzahl je Bot 80/384/400/96/320/320/400/96/320, **Summe 2416**, wie Register Abschnitt 3 (ERZEUGT-Block; gemessen TB-92, `docs/belege/TB-92/d_zellenzahl.txt`) | — |
| ⚠️ | **Offen:** `G6`/`H3` und die Messbitte (TB-95) · `messgroessen.json` und der Registertext „Eingabestand" (TB-96) · die Sonde: leere Gruppe „bestimmt", dritte Gruppe „Abschnitt 0", „Schreibziele", „Lesequellen" (23c, 23d) · „null rote Prüfungen" als Tag-Vorbedingung (21.9, 23a) | TB-95 / TB-96 / Handwerk |

*Dieser Abschnitt ist rein additiv: Er vollzieht Sperrlistenpunkt 4 in Form
(ii) durch drei neue Folgezeilen, berichtigt ein Fertigkriterium, ohne den
alten Satz anzutasten, trägt die Messungen aus TB-91 und TB-92 als
Tatsachennotizen samt einer offenen Messbitte ein, setzt zehn Marken am alten
Ort — und entfernt nichts. Gebaut und gerechnet wird nichts.*

## 40. Testannahmen folgen dem Register, und die neun Handelslisten sind Eingabedateien — `G6`/`H3`, die Kopplung an 5.1 Nr. 4, jede Mutationsprobe mit Gegenprobe, was TB-97/TB-98 tun, und drei angenommene Berichtigungen an den Verfahrensprüfer (Fable 24a, TB-96, 24.09.2026)

⭐ **Reines Eintragen von Registertext und Tatsachen**, wie 34 bis 39. Der Test
ist seit TB-95 grün (40.1–40.4); Fable hat in **24a** geantwortet und dazu
**zwei neue Registertexte** gesetzt: die neun Handelslisten als
Eingabedateien nach 23d (40.6) und die Gegenprobe jeder Mutationsprobe als
Ergänzung zu 12 (40.7). Was daraus beschlossen, aber nicht ausgeführt ist,
steht in 40.8; drei Berichtigungen an ihn, die er angenommen hat, in 40.9.
Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md`
— **eingesetzt, nicht abgetippt** (Beleg `docs/belege/TB-96/d2_zitate.txt`, je
Zitat `diff` rc 0). Anfrage
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-24a_punkt8_vollzogen_test_gruen_neun_listen.md`;
Auftrag `docs/auftraege/MAC_TB-96_register_40.md`; Belege
`docs/belege/TB-96/`; Schritt-0-Commit `fc8d44c`. Messungen des Vorgängers:
TB-95 (`docs/ERGEBNIS_TB-95_testannahmen_und_lesehaken.md`, Belege
`docs/belege/TB-95/`), in TB-96 an Hashes und Register nachgemessen
(`a_messungen.txt`).
⛔ **Keine `.py` geändert, nichts gerechnet** — 40.10.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (5.1 Nr. 4; 5.4;
12; 21.9; 33.2; 33.5; 36.6; 37.2; 39.6; dazu der Nachtrag in 39.8 — zehn
Stellen). Die alten Sätze bleiben zeichengleich; `git diff --numstat` auf
dieses Register zeigt für TB-96 in der zweiten Spalte `0`.

**Fables Kenntnisnahme, 24a Abschnitt 1, zeichengleich:**

> **Punkt 8 im Register:** 575/0, 29 Zitate mit `diff` rc 0, zehn Marken, Abbild `2f23f76c…`, Sonde 0 Befunde — alle acht Kriterien erfüllt. **Plan-Punkt 8 ist fertig.** Der benannte Zwischenzustand hat eine Nacht gedauert und ist geschlossen; so war es gemeint.

### 40.1 Tatsachennotiz — der Test ist grün

`research/vorregistrierung/test_vorregistrierung.py` (`73c9b837…`, Commit
`9e2a071`, TB-95) läuft am 23.09.2026 **165/165, rc 0**, 534 s, in einem Zug
am echten Stand (`docs/belege/TB-95/c_test.txt`). ⇒ **Die Tag-Vorbedingung
„null rote Prüfungen, null ‚bekannt rot'" (21.9, A4; 23a, Wortlaut in 39.1) ist
für diesen Test erfüllt.** Geändert ist nur diese eine Datei
(`6e7defef…` → `73c9b837…`); keine Prüfung entfallen, keine Ausnahme für einen
Bot, keine Toleranz, `auswertung.py` unberührt; kein Sperrlistenhash bewegt;
Sonde gegen `sperrliste_abbild_2026-09-23.json` 0 Befunde, 15/15 Pfade gleich
(`docs/belege/TB-95/c_hashes.txt`, `c_sonde.txt`). In TB-96 nachgemessen:
Hash und letzter Commit unverändert (`a_messungen.txt`, A2).

**Fable, 24a Abschnitt 1, zeichengleich:**

> **Test grün:** 165/165, rc 0, nur eine Datei geändert, keine Prüfung entfernt, keine Toleranz, `auswertung.py` unberührt. Die zwei Berichtigungen der Sitzung an den Erwartungen des Auftrags sind das Wertvollste daran: H3 griff nicht ins Leere, sondern die **Zahl** war gealtert (vier reichten bei sieben, nicht bei neun) — dieselbe Klasse wie der Name, nur unsichtbarer; und die Quelle des Plans ist `faltenplan.py` zur Laufzeit, nicht die historische Datei (30.2 (1)). Die Bauart von G6 (Jahre maschinell aus 5.1 Nr. 4, sonst `None` ⇒ rot) und H3 (strikte Mehrheit, paritätsfest) ist genau das, was 23a verlangt hat, und die vier Gegenproben — vor allem „`ohne` leer ⇒ scheitert" — zeigen, dass sie aus dem richtigen Grund bestehen.

⚠️ **Was „erfüllt" hier heisst und was nicht:** Die Vorbedingung gilt für den
Stand von heute. 40.8 beschliesst weitere Änderungen an genau diesem Test
(`F4`, die vier Literale, Gegenproben); jede davon muss ihn wieder grün
hinterlassen. Und ein grüner Test ist nach 40.7 erst dann ein Nachweis, wenn
jede seiner Mutationsproben eine Gegenprobe hat — für `H3` ist sie geführt
(40.3), für die übrigen sieben steht sie aus (40.8 (c)).

**Marke am alten Ort:** bei **21.9**, unter der Tabelle der Folgen.

### 40.2 `G6` — die Jahre aus dem Register, die Abdeckung gerechnet

**Wie gebaut (TB-95, `9e2a071`):** `G6` liest die Jahre aus dem Registertext
**5.1 Nr. 4** (Funktion `_testjahre_aus_register`) und rechnet die Abdeckung
aus `von`/`bis_ausschliesslich` der Falten mit Rolle `selektion`
(`_abgedeckte_jahre`); die Bestätigungsperiode zählt nicht. Bis TB-95 stand
dort `"2020" in namen` — seit den Zweijahresfalten von `elliott_wave` traf das
nichts mehr.

**Gemessen vor der Änderung (TB-95, `a2_g6.txt`):** 2020 und 2022 lagen bei
**allen neun** Bots in genau einer Selektionsfalte, bei `elliott_wave` in
`2020-2021` und `2022-2023`. ⇒ **Die Sache hinter 5.1 Nr. 4 war erfüllt; rot war
nur die Formulierung.** Die Probe beisst (TB-95, `b_probe.txt`): Falte
`2020-2021` als Bestätigung ⇒ genau ein `G6` rot; Registersatz fehlt (Kopie) ⇒
neun `G6` rot.

⚠️⚠️ **Die Kopplung, gemessen (TB-96, `a_messungen.txt`, A6):** Die Funktion
sucht im ganzen Register **zeilenweise, am Zeilenanfang verankert**, die Zeile,
die mit `4. **JJJJ und JJJJ sind Testfalten, keine Trainingsjahre.**` beginnt
(Muster `^4\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*`).
Heute: **genau ein Treffer**, der Listenpunkt 5.1 Nr. 4; Ergebnis `[2020, 2022]`.
Kein Treffer **oder zwei** ⇒ `None` ⇒ `G6` rot für alle neun Bots. Daraus
folgt zweierlei:

| | |
|---|---|
| (1) | **Wer 5.1 Nr. 4 umformuliert** — auch gut gemeint, auch nur Satzzeichen oder Hervorhebung —, **macht `test_vorregistrierung.py` rot.** Eine Änderung der Sache (andere Jahre) braucht einen eigenen Registereintrag **und** die Anpassung von `G6` im selben Auftrag |
| (2) | **Wer irgendwo im Register eine zweite Zeile mit diesem Anfang schreibt**, etwa ein Zitat von 5.1 Nr. 4 in Spalte 0, macht ihn ebenso rot. Zitate dieser Zeile stehen deshalb eingerückt oder als Blockzitat (`> `) — so auch in diesem Abschnitt |

⭐ **Das ist eine Kopplung, die bis heute niemand sah:** Registertext wird
sonst gelesen, nicht geparst; die Sperrlisten-Sonde liest Abschnitt 10, und
dort steht es seit 36 im Register. Für 5.1 Nr. 4 stand es nirgends. **Die
Marke bei 5.1 Nr. 4 ist der eigentliche Schutz** — sie steht dort, wo jemand
ändern würde.

**Marke am alten Ort:** bei **5.1 Nr. 4**, direkt unter dem Listenpunkt.

### 40.3 `H3` — strikte Mehrheit statt fester Zahl

**Wie gebaut (TB-95, `9e2a071`):** `ohne` = die ersten `len(sel) // 2 + 1`
Selektionsfalten des Plans — eine **strikte Mehrheit**, die bei jeder Parität
beisst; beim Plan von TB-95 für `turtle_soup_stocks` fünf von neun
(`2017`–`2021`).

**Gemessen vor der Änderung (TB-95, `a3_h3.txt`):** Die vier alten Namen
(`2019`–`2022`) **trafen alle** — die Probe griff nicht ins Leere. Aber vier
Nullen verschieben den Median über **neun** Falten nicht (`0.1000` /
`0.1000`); bei sieben Falten, für die die Zahl einst gewählt war, reichten
vier. Allgemein ist das kleinste wirksame k = ⌈n/2⌉. **Die Probe beisst
wieder** (`0.0000` / `9.0000`), und **die Gegenprobe mit leerer Menge
scheitert** (`0.1000` / `0.1000`) — sie beisst aus dem richtigen Grund.

⭐ **Fables Einordnung, 24a Abschnitt 1, zeichengleich:**
*„H3 griff nicht ins Leere, sondern die **Zahl** war gealtert (vier reichten bei sieben, nicht bei neun) — dieselbe Klasse wie der Name, nur unsichtbarer"* — und weiter:
*„Die Bauart von G6 (Jahre maschinell aus 5.1 Nr. 4, sonst `None` ⇒ rot) und H3 (strikte Mehrheit, paritätsfest) ist genau das, was 23a verlangt hat"*.

### 40.4 Die weiteren Literale und `F4`

**Die Liste aus TB-95 (`a4_literale.txt`), in TB-95 nicht geändert, weil heute
grün:**

| Stelle (Datei, Teil) | Literal | Zustand | warum es trotzdem gealtert ist |
|---|---|---|---|
| `test_vorregistrierung.py`, Teil D | `ruhig, krise = "2021", "2020"` | grün | nur weil `BOT` Einjahresfalten hat; die Jahreswahl ist Registerinhalt 4.4. ⚠️ Bekommt `BOT` Zweijahresfalten, **bricht Teil D mit `KeyError`** |
| `test_vorregistrierung.py`, Teil F | `ohne = "2022"` | grün | aus demselben Grund; F1/F2 würden rot |
| `beispieldaten.py`, Krisen-Drawdown | `falte in ("2020", "2022")` | keine Prüfung | trifft bei `elliott_wave` nie |
| `beispieldaten.py`, Exposure | dasselbe | keine Prüfung | bei `elliott_wave` konstant; der Zufalls-Timing-Test ist dann nach dem eigenen Docstring **entartet** |

(Zeilennummern am Stand `9e2a071`: Teil D Z. 246, Teil F Z. 442,
`beispieldaten.py` Z. 69 und 77 — nach 38.2 nur mit Commit.)

⚠️ **Dazu `F4` (TB-95, Zusatzbefund):** Die Prüfung sagt „Median mit der Null
liegt **unter** …", prüft aber mit `<=`. Bei einer Null unter neun (oder
sieben) Falten sind beide Mediane gleich. **`F4` hat nie gebissen** — und das
hängt nicht am Plan.

**Fable, 24a Abschnitt 5, zeichengleich:**

> **Vor dem Tag.** Eine Prüfung, die nie beissen konnte (`<=` statt `<`, bei gleichen Medianen), ist kein Nachweis; sie steht aber in der Zahl, mit der Abschnitt 12 die Vollständigkeit belegt („150 Prüfungen, davon acht Mutationsproben"). Am Tag muss diese Zahl wahr sein — nicht als Anzahl, sondern als Aussage. Dass F4 nicht am Faltenplan hängt, ändert die Kategorie („Testannahmen folgen dem Register" → hier: „die Prüfung prüft, was sie sagt"), nicht den Zeitpunkt. `<=` → `<`, Probe mit Mehrheit wie H3, Gegenprobe „leere Menge ⇒ scheitert".

**Und zu den Literalen, 24a Abschnitt 6, zeichengleich:**

> Euer Satz ist der Grund: **Eine Prüfung, die grün ist, weil ihr Literal zufällig noch stimmt, ist genauso gealtert wie eine rote — sie sagt es nur noch nicht.** Teil D bricht mit `KeyError`, sobald der Bot Zweijahresfalten bekommt — und ob er das nach Abschnitt 3 dieser Antwort bekommt, weiss heute niemand. Also vor der Ableitung umstellen, nicht danach.

⇒ **Beides ist beschlossen (40.7, 40.8 (a)–(c)), nicht erledigt.**

### 40.5 ⛔ Entfällt als eigener Unterabschnitt — steht als Nachtrag in 39.8

Die Antwort auf Fables Messbitte zu den neun Handelslisten (23f Abschnitt 6)
steht als **Nachtrag am Ende von 39.8**, nicht hier. **Fable, 24a Abschnitt 4,
zeichengleich:**

> Eintragen, wie vorgeschlagen, mit: **40.5 als Nachtrag zu 39.8** (es setzt dessen Tatsache fort, und wer 39.8 liest, soll dort fündig werden — dieselbe Regel wie bei den Marken am alten Ort); und **40.6 neu:** die Entscheidung aus Abschnitt 3 dieser Antwort (Listen als Eingabedateien, Neu-Erzeugung, Vergleich gegen 33.2, Sperrlistenpunkt), damit 40.5 nicht mit „Einordnung steht aus" endet, sondern mit der Einordnung. 40.4 (Liste der weiteren Literale) bleibt, wird aber durch Frage (4) unten zum Auftrag.

⭐ *Diese Nummer steht trotzdem hier, damit niemand später 40.5 sucht und das
Register für lückenhaft hält.* Die Einordnung, mit der der Nachtrag endet,
steht in **40.6**.

### 40.6 ⭐⭐ Die neun Handelslisten — Eingabedateien nach 23d

**Was gemessen ist** (TB-95, Nachtrag in 39.8): `benchmark.py` öffnet die neun
`research/tb24_haltedauern/daten/<bot>_alle_trades.csv` über
`faltenplan.py::faltenlaenge_jahre`; ihre Inhalte gehen **über eine
Schwellenentscheidung** — die Faltenlänge nach 5.4 — in Faltenplan und Tabelle
ein. Sie stammen aus `78e2bc6` (TB-24, 13.09.2026), liegen nicht im Snapshot,
nicht auf der Sperrliste. Die Frage an Fable (Anfrage 24a): Genügt dafür ein
Hash-Eintrag, oder gilt die volle Regel aus 23d?

**Der Registertext — Fable, 24a Abschnitt 3, zeichengleich:**

> **Registertext, Ergänzung zu 23d („Eingabestand") und zu 5.4:** Die neun Trade-Listen, aus denen `faltenlaenge_jahre` die Faltenlänge nach 5.4 ableitet, sind Eingabe einer Herleitung von Registertext (33.2) und damit Eingabedateien im Sinn von 23d. Sie werden **vor dem Tag einmal auf dem registrierten Snapshot mit dem registrierten Code neu erzeugt** — im Selektionsmodus, mit den registrierten heutigen Parametern, durch einen Erzeuger unter 36.1 (`--ziel`, Einmal-Schreibsperre), mit Beleg, je Liste Hash, Snapshot-Hash und Commit als Tatsachennotiz — und als Punkt auf die Sperrliste aufgenommen; `faltenplan.py` liest sie über einen registrierten Pfad (Konstante, kein Schalter). Die alten Listen (`78e2bc6`) bleiben liegen als historischer Stand mit Tatsachennotiz. **Danach wird die Faltenlänge je Bot nach 5.4 aus den neuen Listen abgeleitet und gegen 33.2 verglichen.** Gleich ⇒ Tatsachennotiz. Verschieden ⇒ Berichtigung von 33.2 und allem, was daran hängt (Benchmark-Tabelle, Abbild), mit dem Grund „Eingabe war auf nicht-registriertem Datenstand erzeugt" — keine Wahl. Der Reproduzierbarkeitsnachweis (23e) ist der Modus-Lauf selbst: zweimal, bytegleich.

**Sein Grund, zeichengleich:**

> **Die volle Regel.** Und zwar aus dem Grund, den die Störprobe selbst liefert: Eine Schwellenentscheidung ist nicht „kleiner" als ein stetiger Einfluss, sie ist **unsichtbarer**. Kleine Änderungen zeigen nichts, ein Übertritt verschiebt den ganzen Faltenplan eines Bots — und damit 33.2, die Benchmark-Tabelle, die Zellen. Ein Hash-Eintrag würde festhalten, **dass** die Listen so sind, wie sie sind; er sagt nichts darüber, ob sie den Datenstand beschreiben, mit dem der Lauf rechnet. Genau das war der Befund bei `messgroessen.json` (23f/23d), und hier ist er derselbe: **erzeugt vor TB-34, die Krypto-Listen beginnen 2021-09, der Snapshot beginnt 2017-08.** Ob die Faltenlänge eines Krypto-Bots auf dem Snapshot anders ausfiele, weiss ich nicht — und das ist der Grund, die Regel zu halten, nicht sie zu lockern: Wer jetzt „Hash genügt" sagt, weil ein Nachrechnen Falten bewegen könnte, wählt nach Wirkung.

**Seine Antwort auf unseren Einwand — 23d verlangt „aus", nicht „im" Snapshot,
zeichengleich:**

> **Zu eurem Einwand „nicht möglich, ohne sie in einen Snapshot zu nehmen":** 23d verlangt nicht, dass jede Eingabe **im** Snapshot liegt — es verlangt, dass sie **aus** dem registrierten Snapshot und dem registrierten Code **reproduzierbar** ist. Kursdaten liegen im Snapshot; Ergebnisdateien werden daraus erzeugt. Die Listen sind Ergebnisdateien der neun Backtests mit heutigen Parametern; TB-90 hat gezeigt, dass diese Backtests byte-identisch reproduzieren. Also:

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 23d (Eingaben reproduzierbar aus Snapshot und Code), 5a/5e, 3 („erzeugt, nicht abgetippt"), 24.3 als Bauart — die Regel steht, bevor gerechnet ist. **Kein Ergebnis:** Ich verlange die Ableitung, ohne zu wissen, ob sie 33.2 bestätigt; und ich brauche danach nur das Ob je Bot (1 oder 2), keine Trade-Zahlen (27.1 nennt „Anzahl Trades" — die Sitzung meldet die Faltenlänge, nicht die Zählung).

**Zu unserem zweiten Umstand („über `git` reproduzierbar"), zeichengleich:**

> *Zu eurem Umstand 2* („über `git` reproduzierbar"): Aus der Git-Historie reproduzierbar heisst, aus einem Datenstand, den der Lauf nicht verwendet. Das ist genau die Unterscheidung aus 23d, Frage (1): historischer Stand, kein Eingabestand.

**Zu unserem ersten Umstand (die Kippung würde am Abbild sichtbar),
zeichengleich:**

> *Zu eurem Umstand 1* (die Faltenlänge ist als Ergebnis registriert, eine Kippung würde am Abbild sichtbar — „vorausgesetzt, das Abbild ist erzeugt, und es ist es nach 33.5 nicht"): richtig, und das ist die zweite Folge dieser Antwort — **Plan-Punkt 7 (Abbild des Faltenplans, Faltenplan-Sonde) rückt vor**; es ist die Wache, die diese Klasse fängt, und sie fehlt noch. Das Abbild wird nach der Ableitung erzeugt, nicht vorher — sonst bildet es einen Stand ab, der gerade geprüft wird.

**Die Folge für 5.4, zeichengleich:**

> **Eine Folge für 5.4 selbst:** 5.4 nennt die Listen „als Quelle, ohne Hash". Nach dieser Antwort nennt eine Tatsachennotiz zu 5.4 die neuen Listen mit Hash, Snapshot und Commit; der Regeltext von 5.4 (die Schwelle) bleibt unverändert.

⚠️ **Kein Ergebnis — ausdrücklich:** Fable verlangt die Ableitung, **ohne zu
wissen**, ob sie 33.2 bestätigt, und er braucht danach nur das Ob je Bot
(Faltenlänge 1 oder 2), **keine Trade-Zahlen** (27.1). Gleich ⇒
Tatsachennotiz; verschieden ⇒ Berichtigung von 33.2 und allem, was daran hängt
— keine Wahl. Die Regel steht hier, **bevor** gerechnet ist (Bauart 24.3).

**Tatsachennotiz zu 5.4 — Fables Unsicherheit, gemessen (`a_messungen.txt`,
A4/A5).** Seine Unsicherheit, 24a, zeichengleich:

> **Unsicher:** ob 5.4 die Schwelle „mit heutigen Parametern" ausdrücklich nennt — wenn nicht, gehört der Parameterstand der Neu-Erzeugung als Tatsachennotiz zu 5.4, sonst ist die Ableitung nicht reproduzierbar.

| | gemessen |
|---|---|
| ⭐ **Die Schwelle ist registriert** | „30 Trades je Jahr" ist **Festlegung 7** (Tabelle am Registeranfang) und steht als Regel in **5.1 Nr. 6** („Faltenlänge ein Jahr, zwei Jahre bei unter 30 gefundenen Trades je Jahr."); 5.4 wertet sie aus. `faltenplan.py::faltenlaenge_jahre` liest sie als `registerdaten.ZWEIJAHRES_SCHWELLE_TRADES`, **nicht** als Literal (0 Treffer für einen Vergleich mit `30`) |
| ⚠️ **Der Parameterstand der Erzeugung ist es nicht** | 5.4 nennt die Listen als Pfad (`<bot>_alle_trades.csv`) ohne Hash und ohne Commit und sagt nur, die Trades seien **„gefunden, nicht ausgeführt"**, weil das Positionslimit ein Rasterparameter ist. Mit welchen Parametern die Listen am 13.09.2026 erzeugt wurden, steht **nirgends im Register** (`78e2bc6`: 0 Treffer; „heutige Parameter" in 5.4: 0 Treffer). 5.4 sagt auch **nicht** „mit heutigen Parametern" |
| ausserhalb des Registers | Der TB-24-Bericht sagt „mit den heutigen `live_params.py` über die heutigen Bot-Funktionen" (Stand 13.09.). Die `<bot>_meta.json` daneben tragen Kapital, Allokation, Positionslimit und Zählungen, **keine Strategieparameter**. Die neun `live_params.py` haben sich seit `78e2bc6` nur in drei Kommentarzeilen geändert, **keine Zuweisung**; der übrige Code (Bots, Simulation, Entscheidungskerze TB-38, Kostenmodul TB-90) ist hier **nicht** gemessen |

⇒ **Nach Fables eigener Bedingung gehört der Parameterstand der Neu-Erzeugung
als Tatsachennotiz zu 5.4**, sonst ist die Ableitung nicht reproduzierbar: je
Bot die Hashes der Parameterdateien, der Code-Commit, der Snapshot-Hash und der
Modus — neben dem Hash der neuen Liste. ⛔ **Der Regeltext von 5.4 bleibt
unverändert.**

⚠️ **Tatsachennotiz zu einer Voraussetzung in Fables Einwand-Antwort (TB-96
gemessen, kein Registertext geändert):** Der Satz „TB-90 hat gezeigt, dass
diese Backtests byte-identisch reproduzieren" stützt sich auf **TB-90 B6**
(`docs/ERGEBNIS_TB-90_wegA_und_kostenmodul.md`, Beleg
`docs/belege/TB-90/b6_vergleich.txt`): je Bot **ein** Backtest vor und nach dem
Kostenmodul, `cmp` 9/9 identisch — am selben Tag, auf `data/`, mit den
Backtest-Skripten der Bots. **Der Erzeuger der TB-24-Listen**
(`research/tb24_haltedauern/alle_bots.py` → `positionen_holen.py`, der
**gefundene** statt ausgeführter Trades schreibt) **war daran nicht
beteiligt**, und ein Lauf auf dem Snapshot ebenfalls nicht. ⇒ Die Regel trägt
trotzdem: Sie verlangt ihren **eigenen** Reproduzierbarkeitsnachweis — den
Modus-Lauf zweimal, bytegleich (23e) —, nicht den aus TB-90. Die Voraussetzung
ist damit **Voraussetzung der Neu-Erzeugung (TB-98)**, keine gemessene
Tatsache. *Vorgelegt, nicht berichtigt — es ist Fables Satz.*

⚠️ **Tatsachennotiz zum Erzeuger (TB-96 gemessen):** `positionen_holen.py`
schreibt **fest** nach `research/tb24_haltedauern/daten/` (Konstante
`DATEN_DIR`, `to_csv` ohne Ziel-Schalter, `os.makedirs(…, exist_ok=True)`) —
es ist **kein** Erzeuger nach 36.1 (`--ziel`, Einmal-Schreibsperre). ⛔ **Ein
unveränderter Aufruf überschriebe die alten Listen**, die nach dem Registertext
oben als historischer Stand liegen bleiben. Die Neu-Erzeugung braucht deshalb
einen Erzeuger unter 36.1 (Handwerk mit Freigabe, TB-98).

**Folge für den Plan — Plan-Punkt 7 rückt vor.** Das Abbild des Faltenplans
(33.3) und die Faltenplan-Sonde sind die Wache, die genau diese Klasse fängt
(ein Schwellenübertritt, der den Faltenplan eines Bots verschiebt), und sie
fehlen (33.5). ⚠️ **Das Abbild wird NACH der Ableitung erzeugt, nicht vorher**
— sonst bildet es einen Stand ab, der gerade geprüft wird.

**Marken am alten Ort:** bei **5.4** (Listen sind Eingabedateien, werden neu
erzeugt; Parameterstand fehlt), bei **33.2** (Faltenlänge wird neu abgeleitet
und gegen diesen Text verglichen), bei **33.5** (Abbild rückt vor, nach der
Ableitung), bei **39.6** (Eingabestand: zweiter Anwendungsfall).

### 40.7 ⭐ Ergänzung zu 12 — jede Mutationsprobe hat eine Gegenprobe

**Der Registertext — Fable, 24a Abschnitt 5, zeichengleich:**

> **Registertext, Ergänzung zu 12:** Jede Mutationsprobe hat eine **Gegenprobe**, die zeigt, dass sie rot werden kann (die Mutation weggelassen ⇒ die Probe scheitert). Eine Mutationsprobe ohne Gegenprobe zählt nicht als Prüfung. Vor dem Tag wird die Gegenprobe für alle acht Mutationsproben einmal geführt und als Tatsachennotiz festgehalten.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* A8 (eine Wache ist, was ein anderer gegenprüfen kann) und 12. F4 ist der Beleg, dass eine Probe drei Wochen „bestehen" kann, ohne je gemessen zu haben — TB-45 in anderer Form. Kein Ergebnis.

⚠️ **Die Tatsache, die ihn ausgelöst hat:** **`F4` hat drei Wochen
„bestanden", ohne je gemessen zu haben** (40.4) — `<=`, wo der Text „unter"
sagt, bei gleichen Medianen. Und `H3` hat gezeigt, dass eine Probe auch dann
nicht beisst, wenn alle ihre Namen treffen (40.3).

⇒ **Vor dem Tag wird die Gegenprobe für alle acht Mutationsproben einmal
geführt und als Tatsachennotiz festgehalten** (40.8 (c)). Geführt ist sie
heute für **eine**: `H3` (TB-95, `ohne` leer ⇒ scheitert). ⚠️ **Welche acht
Prüfungen „die acht Mutationsproben" aus Abschnitt 12 sind, ist hier nicht
gemessen** — Abschnitt 12 nennt die Zahl, nicht die Namen; die Liste gehört in
die Tatsachennotiz von TB-97.

**Marke am alten Ort:** bei **12**, unter dem Absatz über den Schalter.

### 40.8 Beschlossen, nicht ausgeführt — was TB-97, TB-98, TB-100 und TB-101 tun

Damit das Register sagt, was offen ist und warum:

| | Sache | Auftrag |
|---|---|---|
| (a) | `F4`: `<=` → `<`, Probe mit Mehrheit wie `H3`, Gegenprobe „leere Menge ⇒ scheitert" | TB-97 |
| (b) | Die vier Literale (40.4) bauartgleich umstellen, nach Fables Regel (Zitat unten). Für 4.4: Tatsachennotiz, dass seine Beispieljahre der Stand vom 14.09. sind, und die Prüfung liest den **heutigen** Plan | TB-97 |
| (c) | Gegenproben für **alle acht** Mutationsproben, mit Tatsachennotiz (40.7) | TB-97 |
| (d) | Sonde: **getrennte Schlusszeilen** — „Pfad-Bestandteile: n geprüft, davon 0 / 1 / 2" und „Regel-Bestandteile: m nicht prüfbar (2), je mit Verweis auf die Tatsachennotiz". Der Gesamtwert bleibt, wie 36.5 ihn definiert | TB-97 |
| (e) | ⚠️ **Befund:** Die Gruppe „bestimmt" steht **fest verdrahtet** in `shared/sperrlistensonde.py` (`BESTIMMT_NICHT_EINGETRAGEN`, 39.3). Sie liest künftig **alle drei Gruppen** (Abschnitt 10, „bestimmt", `EINGEFROREN`) **aus dem Abbild**; Gegenprobe: Abbild mit erfundenem „bestimmt"-Pfad ⇒ Sonde meldet ihn | TB-97 |
| (f) | Neun Listen auf dem Snapshot neu erzeugen (Erzeuger unter 36.1), Sperrlistenpunkt, Tatsachennotizen; Faltenlänge nach 5.4 ableiten, gegen 33.2 vergleichen (40.6) | TB-98 |
| (g) | Abbild des Faltenplans (33.3) und Faltenplan-Sonde — **nach** (f) | TB-100 |
| (h) | `messgroessen.json` auf dem Snapshot (23d/23e), `registerdaten.py`, die zwölf Rasterachsen | TB-101 |

⚠️ **(b) vor (f):** Teil D bricht mit `KeyError`, sobald `BOT` Zweijahresfalten
bekommt — und **ob er das nach (f) bekommt, weiss vor der Ableitung niemand.**
(g) nach (f), weil das Abbild sonst einen Stand abbildet, der gerade geprüft
wird. ⚠️ **TB-99 ist kein Auftrag** — die Nummer ist für die Wächter-Sonde
reserviert (`ARBEITSWEISE` 22.2).

**Zu (b), Fable 24a Abschnitt 6, zeichengleich:**

> **Welche Registerstelle die Jahre trägt:** Wo eine Prüfung eine konkrete Registeraussage prüft (wie G6 mit 5.1 Nr. 4), liest sie die Jahre maschinell aus dieser Stelle; wo sie nur „irgendeine Selektionsfalte" braucht (Teil F, freies Beispiel; `beispieldaten.py` Z. 69/77), nimmt sie sie aus dem Plan (`faltenplan.py`), z. B. die zweite Selektionsfalte des Bots, ohne Literal. Für Teil D („2021", „2020"): Wenn 4.4 den TB-30a-Stand trägt und die Prüfung diesen Stand prüfen soll, dann bekommt 4.4 eine Tatsachennotiz, dass seine Beispieljahre der Stand vom 14.09. sind, und die Prüfung liest den **heutigen** Plan — sie prüft die Regel, nicht das Beispiel. Eine Prüfung, die an einem Beispieljahr hängt, prüft das Beispiel.

**Zu (d) und (e), Fable 24a Abschnitt 7, zeichengleich:**

> **(i) Ausgabe trennen: ja — die Regel bleibt.** Gesamtausgang 2 bei zwölf Punkten mit Regelanteil ist korrekt (36.5/37) und am Tag mit Tatsachennotiz zulässig (22g/37.3). Aber die Tag-Vorbedingung aus 22d lautet „kein Pfad-Bestandteil 1, jede 2 mit Notiz" — und die soll man an der Ausgabe **ablesen** können, ohne zu rechnen. Also zwei Zeilen im Schluss: „Pfad-Bestandteile: n geprüft, davon 0 / 1 / 2" und „Regel-Bestandteile: m nicht prüfbar (2), je mit Verweis auf die Tatsachennotiz". Der Gesamtwert bleibt, wie 36.5 ihn definiert.
>
> **(ii) Die Gruppe „bestimmt" fest verdrahtet in `sperrlistensonde.py`: ein Befund, vor dem Tag zu beheben.** 36.6 sagt: Das Abbild ist die maschinenlesbare Fassung, die Sonde prüft **gegen das Abbild** — auch die Gruppe „bestimmt" (37.2). Eine Gruppe, die im Code der Sonde steht, ist ein Literal in einer Wache — dieselbe Klasse wie G6, nur an der Sonde selbst. Sie liest alle drei Gruppen (10, „bestimmt", `EINGEFROREN`) aus dem Abbild; das Abbild führt die Gruppe „bestimmt" heute leer (39.3). Handwerk mit Freigabe; die Sonde ist nicht gesperrt; danach Nullpunkt-Lauf und Gegenprobe (Abbild mit einem erfundenen „bestimmt"-Pfad ⇒ Sonde meldet ihn).

**Marken am alten Ort:** bei **37.2** und **36.6** (die Gruppen kommen aus dem
Abbild).

### 40.9 ⚠️ Drei Berichtigungen an den Verfahrensprüfer — angenommen

| | gemessen | Fables Annahme, zeichengleich |
|---|---|---|
| (a) | `benchmark.py` an **zwei** Punkten (4 und 6; 39.5) | „Mein „drei" war nicht gemessen" |
| (b) | `beispieldaten.py` liest **keine** Benchmark-Tabelle (39.2) | „Ich habe es als Leserin **angenommen**, weil es die Testdaten erzeugt — nicht gemessen" |
| (c) | TB-94 → TB-96 für `messgroessen.json` (39.8) | „TB-94 → TB-96 für `messgroessen.json`. Angenommen; 39.8." |

**Fable, 24a Abschnitt 2, zeichengleich:**

> **(a)** `benchmark.py` an **zwei** Punkten (4 und 6), nicht drei. Mein „drei" war nicht gemessen; richtig, dass 39.5 die gemessene Zahl trägt und meinen Satz nicht zitiert. Die Sache (ein Übergang, mehrere Punkte, eine Notiz) trägt mit zwei genauso.
>
> **(b)** `beispieldaten.py` liest keine Benchmark-Tabelle. Ich habe es als Leserin **angenommen**, weil es die Testdaten erzeugt — nicht gemessen. Repo-weit drei Leser, wie TB-88 sagte. Die Bedingung „Test und Lauf lesen dieselbe Konstante" ist mit zwei Dateien erfüllt.
>
> **(c)** TB-94 → TB-96 für `messgroessen.json`. Angenommen; 39.8.
>
> Alle drei sind dieselbe Klasse wie die sechs Rücknahmen der ersten Woche: eine Tatsache über den Bestand behauptet statt als Voraussetzung genannt. Ich zähle sie mit.

⭐ **Er zählt sie mit** — dieselbe Klasse wie die sechs Rücknahmen der ersten
Woche: eine Tatsache über den Bestand behauptet statt als Voraussetzung
genannt.

⚠️⚠️ **Zu (c) — die Nummer ist wieder gerückt, und das gehört hierher, damit
die Ablage lesbar bleibt:** 39.8 hat „TB-94 → TB-96" berichtigt, und Fable hat
es angenommen. Seitdem ist **TB-96 dieser Eintrag** (Abschnitt 40), und
`messgroessen.json` ist **TB-101** (40.8 (h); `docs/auftraege/AKTUELLER_AUFTRAG.md`,
Stand 24.09.2026). Die Sache ist dieselbe, nur die Nummer nicht — *eine Nummer,
die zwei Sachen meint, ist schlimmer als eine verschobene* (39.8). ⇒ Wo 39.6,
39.8 oder 39.10 „TB-96" für `messgroessen.json` sagen, gilt **TB-101**; die
Sätze bleiben zeichengleich.

⚠️ **Ein vierter Fall derselben Klasse ist in 40.6 vorgelegt, nicht
berichtigt:** „TB-90 hat gezeigt, dass diese Backtests byte-identisch
reproduzieren" — TB-90 B6 hat die Backtest-Skripte der Bots gezeigt, nicht den
Erzeuger der Listen. Die Regel trägt davon unabhängig.

### 40.10 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert** — weder `test_vorregistrierung.py` (`F4`, die vier Literale, Gegenproben) noch `beispieldaten.py`, `shared/sperrlistensonde.py`, `faltenplan.py`, `benchmark.py` noch die Erzeuger unter `research/tb24_haltedauern/` | TB-97 / TB-98 |
| ⛔ | **Nichts gerechnet** — keine Liste neu erzeugt, keine Faltenlänge abgeleitet, der Test nicht erneut ausgeführt; in `research/vorregistrierung/ergebnisse/` nichts geschrieben | TB-98 |
| ⛔ | **Kein neues Abbild** — keine Sperrlistendatei hat sich bewegt; das gültige Abbild bleibt `sperrliste_abbild_2026-09-23.json` (`2f23f76c…`), Sonde vorher und nachher gleich (`d3_sonde.txt`) | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — 5.1 Nr. 4 (Wortlaut für `G6`), 5.4 (Regeltext), 12, 21.9, 33.2, 33.5, 36.6, 37.2, 39.6 und 39.8 bleiben zeichengleich; Marken und ein Nachtrag, nichts entfernt | — |
| ⛔ | **Die Listen nicht auf die Sperrliste genommen** — das geschieht mit den neu erzeugten Listen (40.6), nicht mit den alten | TB-98 |
| ⭐ | **N = 653 (Festlegung 10) unberührt**; Festlegung 7 (Schwelle 30) unberührt | — |
| ⚠️ | **Offen:** 40.8 (a)–(h) · der Parameterstand der Neu-Erzeugung als Tatsachennotiz zu 5.4 (40.6) · die Liste der acht Mutationsproben (40.7) · die Voraussetzung „TB-90 hat gezeigt" (40.6, bei Fable) · der Registertext „Eingabestand" (23d) selbst ist weiter **nicht** eingetragen (39.6) | TB-97 / TB-98 / TB-101 / Fable |

*Dieser Abschnitt ist rein additiv: Er trägt zwei Registertexte des
Verfahrensprüfers zeichengleich ein, hält eine Kopplung zwischen Registertext
und Test fest, die bisher niemand sah, beschliesst die nächsten vier Aufträge
mit ihrer Reihenfolge, setzt Marken an zehn Stellen — und entfernt nichts.
Gebaut und gerechnet wird nichts.*
