# REGISTER-KOPIE Abschnitt 2 (von 0–50) — Register-Z. 96–248 — Commit db108a68ec57316250ca792a0673b5932dd0f0e8 — 2026-10-01 — Original sha256 b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1 — KOPIE, nicht das Register

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

> ⭐ **2.1 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (i), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 2.2 Die vier zulässigen Grundlagen — und zwei benannte Ausnahmen

Zulässig sind `kosten`, `datenfrequenz`, `volatilitaet`, `haltedauer`.

Zwei Grenzen stützen sich auf keine davon. Das steht hier ausdrücklich statt
verdeckt:

| Kennzeichnung | Wo | Warum keine der vier |
|---|---|---|
| `ableitung` | Obergrenze des Positionslimits | `floor(1 / ALLOCATION_PCT)` ist keine Wahl, sondern eine Identität: ein Rasterpunkt darüber **ist derselbe Punkt**. Die Regel steht so in der Aufgabenstellung. |
| `methode` | Fibonacci-Leiter, Bollinger-Fenster | Eigenschaften des Verfahrens, nicht Einstellungen — dieselbe Rolle wie die Kostenkonvention von 0,30 %. |

Beide Sätze nennen **keine Zahl**; die Werte stehen in einem getrennten Feld.

> ⭐ **2.2 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (h), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **2.2 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (a), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

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

> ⭐ **2.5 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (f), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

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

> ⭐ **2.7 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (b), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

