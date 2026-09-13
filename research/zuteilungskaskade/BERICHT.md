# Die Zuteilungskaskade — Vorarbeiten und Festlegungen (TB-26)

**Stand: 13.09.2026.** Diese Untersuchung gehört zu TB-26 und dokumentiert die
beiden Festlegungen, die der Umsetzung in `shared/zuteilung.py` vorausgingen:
**welcher Bot einen Primärschlüssel hat** (Stufe 1) und **wie der
Diversifikationsbeitrag definiert ist** (Stufe 2). Sie fasst keinen Bot-Code
an; die Übernahme in die Bots ist ein getrennter Schritt und steht im
zugehörigen Pull Request.

Der Anlass steht in TB-23: acht von neun Bots sind nicht deterministisch, weil
bei knappem Platz die **Zeilenreihenfolge** des Trade-DataFrames entschied —
und die ist die Symbolreihenfolge der Konfigurationsdatei.

---

## 1. Schritt 1 — welcher Bot führt eine stetige Signalstärke?

Wiederholbar über

```
python3 research/zuteilungskaskade/messung_primaerschluessel.py
```

Gemessen wird je Zusatzspalte der Trade-Tabelle: Zahl der verschiedenen Werte,
Anteil der Trades mit geteiltem Einstiegszeitpunkt (nur dort wird überhaupt
zugeteilt) und — der entscheidende Wert — **wie viele davon nach einer
Rangregel auf dieser Spalte weiterhin gleichauf liegen**. Das ist Eigenschaft 2
der Prüfliste: höchstens 2 %.

| Bot | Trades | gleichzeitig | Kandidatenspalte | versch. Werte | gleichauf | Eig. 2 |
|---|---:|---:|---|---:|---:|:--:|
| `elliott_wave` | 130 | 33,8 % | `fib_score` | 5 | **38,6 %** | nein |
| `elliott_wave_stocks` | 510 | 58,8 % | `fib_score` | 5 | **72,7 %** | nein |
| `rsi2_crypto` | 439 | 65,8 % | `rsi_at_entry` | 330 | **0,0 %** | ja |
| `rsi2_mean_reversion` | 5391 | 90,7 % | `rsi_at_entry` | 442 | **2,1 %** | knapp nein |
| `t3_supertrend` | 980 | 43,8 % | — | — | — | — |
| `turtle_soup_crypto` | 1599 | 84,4 % | `setup_day_low` | 1561 | 0,0 % | ja¹ |
| `turtle_soup_stocks` | 12069 | 96,5 % | `setup_day_low` | 12041 | 0,0 % | ja¹ |
| `volatility_breakout` | 4510 | 87,7 % | — | — | — | — |
| `volatility_breakout_crypto` | 233 | 60,9 % | — | — | — | — |

¹ erfüllt Eigenschaft 2 mühelos und ist trotzdem kein Primärschlüssel — siehe
unten.

### Die neun Entscheidungen

**Drei Bots führen gar nichts** (`t3_supertrend`, `volatility_breakout`,
`volatility_breakout_crypto`): ihre Trade-Tabelle enthält Zeiten, Kurse,
Ergebnis und Haltedauer und sonst nichts. Der ADX zum Einstieg bzw. die
Bandbreite zum Ausbruch wären Kandidaten, werden aber nicht mitgeschrieben. Sie
nachzurechnen wäre eine **neue Größe** und damit eine Strategieänderung, keine
Rangregel — also unterbleibt es. Kaskade beginnt bei Stufe 2.

**Zwei Bots führen ein Kursniveau** (`turtle_soup_crypto`,
`turtle_soup_stocks`): `setup_day_low` ist der Donchian-Tiefpunkt, der das
Setup definiert. Es erfüllt Eigenschaft 2 mühelos und scheitert an den
anderen beiden:

* **Eigenschaft 1** — es drückt keine Signalstärke aus. Ein tieferer
  Setup-Kurs ist kein besseres Signal, er ist ein anderer Titel.
* **Eigenschaft 3** — es ist nicht skalenfrei. Bei den Kryptopaaren reicht der
  Wert von 6,3·10⁻⁷ bis 1,1·10⁵; eine Rangregel darauf sortierte schlicht nach
  Notierungshöhe und bevorzugte immer dieselben Symbole.

Kein Primärschlüssel.

**Zwei Bots führen einen diskreten Score** (`elliott_wave`,
`elliott_wave_stocks`): der `fib_score` nimmt oberhalb seiner Schwelle nur
**fünf** Werte an. Gemessen bleiben 38,6 % bzw. 72,7 % der gleichzeitigen
Trades darauf gleichauf; TB-23 hat denselben Befund für den Aktien-Bot mit 144
Trades (48,0 %) an der Limit-Kante beziffert. Eigenschaft 2 verfehlt, und zwar
um Größenordnungen. Kein Primärschlüssel.

> **TB-25 ist hier offen und bleibt es.** Ob unter dem Score stetige Abstände
> liegen (Retracement gegen Zielverhältnis), wird dort untersucht. Bis das
> geklärt ist — und bis geklärt ist, ob der Score überhaupt etwas trägt —
> beginnt die Kaskade für beide Elliott-Bots bei Stufe 2.

**Zwei Bots führen eine stetige Signalstärke** (`rsi2_crypto`,
`rsi2_mean_reversion`): `rsi_at_entry`, der RSI(2) zum Einstieg.

> **Das weicht von der Erwartung des Auftrags ab**, der „sieben führen keine"
> annahm und damit implizit alle außer den beiden Elliott-Bots. Die Messung
> sagt etwas anderes, und deshalb steht es hier deutlich: es sind **fünf**
> ohne brauchbare Größe, **zwei** mit einem untauglichen Kandidaten und
> **zwei** mit einer brauchbaren.

Die Begründung im Einzelnen:

* **Es ist keine neue Größe.** `backtest_rsi2.py` schreibt die Spalte seit
  jeher mit; sie steht in jeder Trade-Tabelle, die in die Zuteilung geht. Das
  Verbot des Auftrags richtet sich gegen das *Erfinden* einer Größe, nicht
  gegen das Benutzen einer vorhandenen.
* **Es ist die Signalstärke dieser Strategie.** RSI-2 steigt ein, weil der
  Indikator unter die Schwelle gefallen ist. Je tiefer er steht, desto
  überverkaufter der Titel — das ist die Prämisse, aus der die Schwelle
  überhaupt stammt. Richtung deshalb **aufsteigend**: der niedrigste zuerst.
* **Die Richtung kommt aus der Strategielogik, nicht aus den Zahlen.** Sie
  anhand des gemessenen Zusammenhangs zwischen `rsi_at_entry` und `pnl_pct` zu
  wählen wäre eine Anpassung an die Stichprobe — derselbe Fehler, den
  Abschnitt 7 des Übergabeprotokolls an mehreren Stellen benennt.
* **Eigenschaft 2:** 0,0 % bei `rsi2_crypto`, **2,1 %** bei
  `rsi2_mean_reversion`. Der zweite Wert liegt knapp über der Marke. Das ist
  eine Ermessensentscheidung und wird als solche geführt: die 2,1 % lösen die
  Stufen 2 bis 4 auf, die übrigen 97,9 % bekommen einen ökonomischen Grund,
  den sie sonst nicht hätten. Beim `fib_score` mit 38,6 %/72,7 % fiele dieselbe
  Abwägung umgekehrt aus.
* **Umkehrbar in einer Zeile.** `SIGNALSPALTE = None` in der
  `equity_simulation.py` des Bots, und die Kaskade beginnt dort bei Stufe 2.
  Die Wirkung auf die Kennzahlen steht in `docs/TB-26_ZUTEILUNGSKASKADE.md`.

---

## 2. Schritt 2 — der Diversifikationsbeitrag

Der Sekundärschlüssel trägt in sieben von neun Fällen die Hauptlast. Vier
Fragen waren zu beantworten.

### 2.1 Korrelation worauf?

**Festgelegt:** Tagesrenditen des Kandidaten gegen die **allokationsgewichtete
Renditereihe des aktuellen Buches**, über die letzten 60 Handelstage.

Die Alternative — Korrelation gegen jede offene Position einzeln, dann
gemittelt — ist verworfen. Sie misst eine andere Größe: der Mittelwert der
Einzelkorrelationen ignoriert, wie stark sich die Positionen **untereinander**
aufheben. Ein Buch aus zwei gegenläufigen Positionen ist als Ganzes kaum
schwankend; ein Kandidat, der zu beiden je 0,8 korreliert, konzentriert es
deutlich weniger als der Einzelmittelwert nahelegt. Die gewichtete Buchreihe
bildet genau das ab und ist zudem billiger (eine Korrelation je Kandidat statt
einer je Paar).

Gewichtet wird mit der **Allokation**, weil genau sie beschreibt, wie stark
eine Position das Buch prägt. Ein gleichgewichteter Mittelwert wäre eine
zweite, stillere Annahme über dasselbe Buch.

**Point-in-time:** gelesen werden ausschließlich Tage **vor dem Kalendertag des
Einstiegs**. Der Einstiegstag selbst bleibt außen vor — bei `elliott_wave` (1 h)
und `t3_supertrend` (4 h) wäre sein Tagesaggregat sonst aus Kerzen gebaut, die
zum Einstiegszeitpunkt noch gar nicht geschlossen waren. Für die Tagesbots ist
es der übliche Vorlauf.

**Die Kursquelle** ist der Datensatz, den der Bot selbst geladen hat
(`load_all_symbol_data()`), samt der dort bereits gelaufenen Bereinigung durch
`shared/kursdaten.entferne_unvollstaendige()`. Ein zweiter Lesepfad nach
`data/` wäre eine zweite Wahrheit über dieselben Kurse.

**Lücken:** fehlt für einen Tag der Kurs einer Buchposition (jüngeres Symbol,
Handelsruhe), werden die Gewichte an diesem Tag auf die vorhandenen Positionen
neu normiert, statt den Tag zu verwerfen. Sonst leerte eine einzige junge
Position das Fenster für das ganze Buch. Und die Tagesrenditen werden mit
`pct_change(fill_method=None)` gebildet: die pandas-Voreinstellung füllt Lücken
vorwärts und erzeugt damit an jedem fehlenden Tag eine Rendite von exakt 0 % —
eine erfundene Beobachtung, die die gemessene Korrelation ausgerechnet bei den
Symbolen senkt, über die am wenigsten bekannt ist.

### 2.2 Was bei zu kurzer Historie?

**Festgelegt:** weniger als **20** gemeinsame Beobachtungen mit dem Buch → kein
Wert. Der Kandidat bekommt dann den **Median der Kandidaten, für die an diesem
Zeitpunkt ein Wert vorliegt**. Dieselbe Regel gilt auf allen drei Stufen, auf
denen ein Wert fehlen kann.

Die 20 statt 60: das Maß ist hier ein Gleichstand-Auflöser und keine
Renditeprognose, und ein Symbol mit 40 Tagen Historie trägt mehr Information
als gar keine. Das Fenster verkürzt sich also bis 20 und fällt darunter aus.

Die drei naheliegenden Alternativen sind verworfen, jede aus einem Grund:

| Alternative | verworfen, weil |
|---|---|
| ans Ende stellen | benachteiligt junge Symbole systematisch — genau das soll die Kaskade nicht tun |
| Korrelation 0 einsetzen | 0 ist der **beste** erreichbare Wert auf Stufe 2; das Symbol würde umso mehr bevorzugt, je weniger man über es weiß |
| Stufe für dieses Paar überspringen | ergäbe einen nicht-transitiven Vergleich; eine Sortierung darauf ist nicht wohldefiniert und wäre ihrerseits reihenfolgeabhängig — derselbe Fehler in Grün |

Der Median kann den Kandidaten nie gewinnen lassen (er liegt nie unter dem
Minimum), stellt ihn aber vor die überdurchschnittlich korrelierten. Er
gewinnt und verliert durch die Lücke also nichts. Geprüft wird das in
`shared/test_zuteilung.py`, Abschnitt 5 — einschließlich der beiden
verworfenen Alternativen als Mutanten.

### 2.3 Was bei leerem Buch?

Die Stufe entfällt, die Kaskade rückt auf Stufe 3 vor. Deterministisch, weil
Stufe 3 und 4 es sind. Geprüft in Abschnitt 3 des Selbsttests.

### 2.4 Rechenaufwand — gemessen, nicht vermutet

Die Korrelation fällt bei **jeder** Zuteilungsentscheidung an, und nach jeder
Vergabe erneut: das Buch hat sich geändert. Gemessen auf dem Datenstand vom
13.09.2026 (`turtle_soup_stocks`, der teuerste Fall: 12 069 Trades, 147
Symbole, Buch bis 51 Positionen):

| | |
|---|---|
| umstrittene Zuteilungen | 1 952 |
| gerechnete Korrelationen | 27 854 |
| Rechenzeit Kaskade | **3,1 s** |
| Rechenzeit Aufbau der Tagesreihen | 2,4 s |

Der Auftrag vermutete „ein Zwischenspeicher je (Symbol, Tag) ist vermutlich
nötig". Die Messung präzisiert das:

* Ein Zwischenspeicher für die **Korrelation** — je (Symbol, Buch, Tag) —
  **trifft nie**: 27 854 Rechnungen, 0 Treffer. Nach jeder Vergabe ist das
  Buch ein anderes, also auch der Schlüssel. Er hätte nur Arbeitsspeicher
  gekostet (27 854 Schlüssel mit je bis zu 51 Buchpositionen) und ist deshalb
  nicht vorhanden.
* Was den Aufwand klein hält, ist der Speicher **eine Ebene tiefer**: die
  Tagesreihen je Symbol werden einmal je Lauf zu zwei breiten Tabellen
  (Tage × Symbole) verdichtet; ein 60-Tage-Fenster ist danach ein
  Array-Schnitt. Das ist der (Symbol, Tag)-Speicher, den der Auftrag meinte.
* Dazu kommt eine Ersparnis, die nichts kostet: passen alle Kandidaten eines
  Zeitpunkts ohnehin hinein, ist ihre Reihenfolge für jede Zahl des Ergebnisses
  bedeutungslos — dann wird die Kaskade gar nicht erst befragt. Von 96,5 %
  gleichzeitigen Trades bleiben so 1 952 wirklich umstrittene Entscheidungen.

Der Gesamtlauf von `shared/determinismus.py --voll --perms 20` über alle neun
Bots steigt dadurch von 616 s auf die im Ergebnisdokument genannte Zeit.

---

## 3. Was diese Untersuchung nicht getan hat

* **Keine Strategie geändert.** Die Menge der erzeugten Trades ist unverändert;
  verändert ist nur, welche davon Kapital bekommen, wenn es knapp wird.
* **Keinen Parameter geändert** — auch nicht `MAX_CONCURRENT_POSITIONS` bei
  `volatility_breakout`, wo TB-23 gefunden hat, dass das Limit 15 bei
  rechnerisch höchstens 10 finanzierbaren Positionen nie greift. Der Befund ist
  hier nur erwähnt; er ist ein eigener Punkt.
* **Keine `results/*/equity_curve.csv` überschrieben.** Wann sie neu erzeugt
  werden sollten, steht in `docs/TB-26_ZUTEILUNGSKASKADE.md`.
* **Keinen `fib_score` aufgewertet.** Was unter ihm liegt, ist Sache von TB-25.
