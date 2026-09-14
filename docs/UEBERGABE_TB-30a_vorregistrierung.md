# Übergabe TB-30a — Vorregistrierung der Neuselektion

**14.09.2026.** Diese Zusammenfassung beginnt, wie es die Aufgabenstellung
verlangt, mit dem Vollständigkeitstest.

---

## 1. Der Vollständigkeitstest

> **Liess sich das Auswertungsskript fertig schreiben, ohne ein einziges
> Ergebnis gesehen zu haben — und wenn nein, welche Festlegung fehlte?**

**Ja, es liess sich fertig schreiben.** `research/vorregistrierung/auswertung.py`
läuft vollständig gegen erzeugte Beispieldaten mit frei erfundenen Werten und
liefert alles, was nach dem Lauf gebraucht wird: Plateau-Gewinner je Bot,
Markierungen, Bleibt-Geht nach (a)–(d) einschliesslich Beta-Bereinigung, die
drei DSR-Werte, alle Kennzahlen der Beurteilung und zuletzt die
Bestätigungsperiode. Es hat **keinen Schalter**.

**Aber es liess sich nur fertig schreiben, weil an sieben Stellen eine Lesart
festgelegt werden musste**, wo die zwölf Festlegungen zwei zuliessen. Das ist
die ehrliche Antwort auf die zweite Hälfte der Frage: es fehlte keine
Festlegung, aber sieben waren **unterbestimmt**. Alle sieben stehen im
Register (Abschnitt 12), jede mit ihrer Begründung:

| # | Offene Stelle | Festgelegte Lesart |
|---|---|---|
| 1 | Trägt `DD_Toleranz` ein Exposure-Argument? | **Ja** |
| 2 | Zählt das Plateau-Mittel den Punkt selbst mit? | **Ja** |
| 3 | Zählt der Spitzentest den Punkt selbst mit? | **Nein** |
| 4 | Was ist eine Spitze bei Nachbarmittel ≤ 0? | `S(x) − M > 0,5·\|M\|`, total definiert |
| 5 | Muss der Gewinner zulässig sein? Was gilt bei (b)? | Ja; bei (b) Bericht mit Markierung „nicht zulässig" |
| 6 | Gehen unzulässige Nachbarn ins Plateau-Mittel ein? | **Ja** — die Regel misst Glattheit, nicht Zulässigkeit |
| 7 | Wie wird Gleichstand aufgelöst? | Statistik, dann Zellenname — kein Zufall |

**Die erste ist die tragende und verdient einen Absatz.** Festlegung 4 macht
den Benchmark-Drawdown ausdrücklich exposure-abhängig („im Lauf gilt die
mittlere Exposure des jeweiligen Parametersatzes in der jeweiligen Falte").
Festlegung 5 definiert `DD_Toleranz` als „Median der Benchmark-Drawdowns über
alle Selektionsfalten". Ein Median exposure-abhängiger Grössen ist selbst
exposure-abhängig — `DD_Toleranz` **erbt** das Argument. Das ist keine
zusätzliche Entscheidung, sondern die einzige Lesart, in der beide
Festlegungen zusammenpassen, und sie erfüllt genau, was Festlegung 5
bezweckt: *„ein Bot mit 21 % Zeit im Markt liegt auf einer anderen Skala als
einer mit 100 %"* — nur kommt die Skala jetzt aus der Exposure selbst statt
aus einem heute gemessenen Live-Zustand.

**Zwei weitere Stellen liessen sich nicht als Lesart lösen**, weil sie nicht
die Auswertung betreffen, sondern den Lauf: die beiden Bug-Fixes. Sie stehen
als **Voraussetzungen** im Register (Abschnitt 11) und auf der Sperrliste —
der Lauf darf nicht beginnen, bevor sie eingebaut sind.

---

## 2. Ist die Drawdown-Bedingung in 2020 und 2022 überhaupt erfüllbar?

**Ja, und zwar deutlich.** Die vorab berechneten Tabellen zeigen bei 50 %
Exposure:

| Falte | `DD_Benchmark` | `1,25 ×` | `DD_Toleranz` | **erlaubt** | wer bindet |
|---|---:|---:|---:|---:|---|
| 2019 | −3,69 % | −4,61 % | −4,33 % | **−4,61 %** | die relative Grenze |
| **2020** | −18,93 % | −23,66 % | −4,33 % | **−23,66 %** | die relative Grenze |
| 2021 | −2,38 % | −2,98 % | −4,33 % | **−4,33 %** | **`DD_Toleranz`** |
| **2022** | −10,09 % | −12,61 % | −4,33 % | **−12,61 %** | die relative Grenze |
| 2023 | −4,33 % | −5,41 % | −4,33 % | **−5,41 %** | die relative Grenze |
| 2024 | −3,47 % | −4,34 % | −4,33 % | **−4,34 %** | die relative Grenze (knapp) |
| 2025 | −8,89 % | −11,11 % | −4,33 % | **−11,11 %** | die relative Grenze |

In 2020 darf ein Parametersatz bei halber Exposure fast **24 %** verlieren, in
2022 gut **12 %**. **Die Krisenfalten sind die grosszügigsten des ganzen
Plans** — genau wie es Festlegung 6 vorhergesagt hat, als sie die absolute
Grenze verwarf: eine feste Untergrenze hätte dort gebunden, wo die relative
weit offen steht, und den Bot erledigt, bevor gewählt wurde.

**Gebunden wird in den ruhigen Jahren** — und auch dort erst oberhalb der
Rauschgrenze. 2021 löst `DD_Toleranz` die relative Grenze ab und hebt die
Schwelle von −2,98 % auf −4,33 %. Ohne sie entschieden dort drei schlechte
Tage über die Zulässigkeit eines Parametersatzes; das ist genau die Lücke,
die Festlegung 5 schliessen sollte, und sie schliesst sie.

**Eine Zeile verdient Aufmerksamkeit:** 2024 liegen relative Grenze (−4,34 %)
und `DD_Toleranz` (−4,33 %) einen Hundertstelpunkt auseinander. Das ist kein
Problem — die Regel ist auch dort eindeutig —, aber es zeigt, wie knapp die
beiden Mechanismen in einem durchschnittlichen Jahr beieinanderliegen.

---

## 3. Was gebaut wurde

### 3.1 Das Register — `docs/VORREGISTRIERUNG_neuselektion.md`

Rastergrenzen je Parameter mit Begründungssatz, Faltenplan, Plateau- und
Kantenregel, Drawdown-Bedingung, Abbruchkriterien, die drei Regeln für
mehrere Ausfälle (wörtlich), DSR-Buchführung, Sperrliste, Amendment-Regel.

**Der Kern ist, dass keine Rastergrenze eine Zahl ist.** Jede ist eine Regel
über eine gemessene Grösse:

```python
{"regel": "sigma_vielfaches", "zeitrahmen": "krypto_1d", "faktor": 0.5}
```

Damit ist die Zusicherung „der heutige Live-Wert ist kein Bezugspunkt" nicht
behauptet, sondern **maschinell prüfbar**: `pruefe_grenzsaetze.py` rechnet
jede Grenze nach und prüft zusätzlich, dass kein Begründungssatz eine Zahl
nennt, die ein Live-Wert dieses Bots ist. Ein Live-Wert kann nur noch durch
Zufall in einer Grenze landen — und dieser Zufall fällt auf.

**Der Zahlenteil des Registers ist erzeugt, nicht abgetippt.**
`registerbericht.py --pruefen` meldet mit Rückgabewert 1, sobald das Dokument
vom Code abweicht.

### 3.2 Das eingefrorene Auswertungsskript

`research/vorregistrierung/auswertung.py`, 150 Prüfungen in
`test_vorregistrierung.py`, davon acht Mutationsproben am Ablauf.

**Beta-Bereinigung und Zufalls-Timing-Test stecken darin**, nicht in einer
späteren Aufgabe — ohne sie wäre Abbruchkriterium (c) nicht entscheidbar und
der Vollständigkeitstest nicht bestanden.

Der Zufalls-Timing-Test verschiebt die Exposure-Reihe **zyklisch** über die
Benchmark-Renditen: Zeit im Markt, Exposure-Verteilung und Positionstage
bleiben Balken für Balken erhalten, allein die Lage ändert sich. Gerechnet
werden **alle** Verschiebungen — kein Ziehen, kein Startwert, keine Wahl.
Damit ist das Kriterium, das das Übergabeprotokoll für den Prüftermin des
Elliott-Aktien-Bots vorgemerkt hatte (Abschnitt 9, Punkt 4), erstmals als
Code vorhanden — als **berichtete Zeile**, nicht als Tor. Ein Tor wäre eine
dreizehnte Festlegung, und die hat niemand getroffen.

### 3.3 Die Vorab-Berechnungen

* **Benchmark-Drawdowns je Falte je Bot** — nicht eine Zahl, sondern die
  **Funktion über die ganze Exposure-Achse** (1 % bis 100 %), damit im Lauf
  die satzweise Verfeinerung möglich ist, ohne dass etwas im Register auf den
  Live-Zustand verweist. Die Interpolationsregel steht in derselben Datei wie
  die Tabelle und damit auf derselben Sperrliste.
* **`DD_Toleranz` je Bot** — Median über die Selektionsfalten, mit demselben
  Exposure-Argument.
* **Purge-Längen je Bot** aus TB-24: 10 bis 134 Tage.
* **Welche Bots Zweijahres-Falten bekommen:** genau einer, `elliott_wave`
  (26,0 gefundene Trades je vollem Kalenderjahr). Gerechnet, nicht geschätzt.
* **Volatilitäts- und Spannenkennzahlen** für die Rastergrenzen.

### 3.4 Die beiden Bug-Fixes

**AB2/U5 — Entscheidung: abbrechen.** Die Wache steht fertig und geprüft in
`shared/regimewache.py`. **Der Einbau an den drei Stellen ist TB-30b**, weil
er `equity_simulation.py` und `multi_symbol_optimise.py` berührt und die
Randbedingungen das ausschliessen. Der Lauf darf nicht starten, bevor er
erfolgt ist; `regimewache.pruefe_einbau()` beantwortet das maschinell.

**Agent 2 — umgestellt, in `shared/`.** Der fest verdrahtete Satz „es gilt das
chronologische" ist weg; an seine Stelle tritt eine dreistufige Kaskade
(Kapital-Drawdown → chronologisch → Block). Heute greift Stufe 2, weil der
Optimierer den Kapital-Drawdown noch nicht mitliefert — aber der Agent weist
den Ersatz jetzt **als Ersatz aus** und schaltet von selbst um, sobald TB-30b
das Feld nachrüstet.

### 3.5 Der Nulltest S-E1

Eigener Registereintrag (`docs/VORREGISTRIERUNG_S-E1_nulltest.md`) mit beiden
Bedingungen: Sweep-Zellen sind Robustheit, **nicht** Auswahl; S-E1 geht in die
Staging-Ebene, **nicht** ins Buch. N-Buchführung: **ein** Eintrag im
Versuchsregister (neuer Abschnitt 6a), **kein** Beitrag zur DSR.

---

## 4. Zwei Wachen haben angeschlagen — beide zu Recht

**Ein Grenzsatz nannte einen Live-Wert.** „20-Balken-Spanne" gegen
`ADX_THRESHOLD = 20.0` bei `t3_supertrend`. Umformuliert. Die Übereinstimmung
war unschuldig — und genau deshalb ein guter Beleg: eine Wache, die nur bei
Absicht anschlägt, prüft nichts.

**Die Wache aus TB-29 war falsch gebaut.**
`research/versuchsregister/test_versuchsregister.py` prüfte, dass `git status`
nichts ausserhalb von `research/` und `docs/` meldet. Das prüft nicht TB-29,
sondern den **Arbeitsbaum** — und der enthält alles, woran gerade sonst
gearbeitet wird. Sie meldete die ausdrücklich beauftragte Änderung an
`shared/` als Verstoss von TB-29.

Umgestellt auf das, was TB-29 tatsächlich zugesichert hat: *ein Lauf der
Untersuchung verändert nichts.* Der Arbeitsbaum wird vor und nach einem Lauf
aufgenommen, dazwischen läuft die Erhebung in allen Betriebsarten; dazu prüft
ein Syntaxbaum-Durchgang, dass sie nur in Wegwerf-Verzeichnisse schreibt.
Beide Hälften können rot werden, nachgewiesen an einer eingefügten
Schreibzeile.

**Das ist eine Änderung an fremder Arbeit und gehört deshalb genannt**, nicht
stillschweigend gemacht: die alte Fassung wäre bei jeder künftigen Aufgabe
rot geworden, die einen Produktivordner anfasst — und ein Wächter, der bei
fremder Arbeit rot wird, wird abgeschaltet. Dann fängt er auch den Fall nicht
mehr, für den er da ist.

---

## 5. Wo die Aufgabenstellung mit den Randbedingungen kollidierte

**Die Aufgabe verlangte zwei Bug-Fixes „vor den Lauf". Die Randbedingungen
verbieten, `equity_simulation.py` und `multi_symbol_optimise.py` anzufassen
— genau die Dateien, in denen AB2/U5 sitzt.**

Aufgelöst zugunsten der Randbedingungen, und zwar so, dass in TB-30b nichts
mehr zu entscheiden bleibt:

* die **Entscheidung** ist getroffen und im Register eingetragen (abbrechen),
* die **Mechanik** steht fertig und geprüft in `shared/regimewache.py`,
* die **drei Einbaustellen** stehen mit Zeilennummern im Register,
* ein **maschineller Prüfer** (`pruefe_einbau()`) sagt, ob der Einbau erfolgt
  ist,
* und die **Sperrliste** sagt: ohne Einbau kein Lauf.

Bei Agent 2 war die Kollision nicht da — `shared/param_search_agent.py` ist
`shared/`, also erlaubt. Dort ist umgestellt statt verwiesen.

**Ein zweiter Punkt, der in TB-30b landet und vorher niemandem aufgefallen
wäre:** zwei Rasterachsen existieren im Optimierer noch gar nicht.
`rsi2_mean_reversion` führt seinen Trendfilter als Konstante
(`SMA_TREND_PERIOD = 200`), und beide Volatility-Breakout-Bots führen
`BB_SQUEEZE_PERCENTILE`/`BB_LOOKBACK` nur in `live_params.py`. Ohne
Durchreichung gälte für Aktien- und Krypto-Variante **nicht dieselbe Regel**
— und das war eine ausdrückliche Vorgabe. Steht im Register, Abschnitt 11.3.

---

## 6. Was bewusst nicht ins Raster kam

Aufgenommen sind die Parameter, die der jeweilige Bot heute schon rastert,
dazu das Positionslimit, dazu die Vereinigung, wo Aktien- und Krypto-Variante
bisher verschieden rasterten.

**Draussen bleibt insbesondere die Zeitbremse** (`MAX_HOLD_DAYS`,
`MAX_HOLD_HOURS`). Nicht aus Bequemlichkeit, sondern wegen N: jede
zusätzliche Achse multipliziert die Zellenzahl und damit den Abschlag der
DSR. Bei 2 416 Zellen steht N schon bei 3 069; eine fünfte Achse bei fünf
Bots hätte es über 10 000 getrieben. TB-24 hat zudem gemessen, dass die
Zeitbremse der stärkste Einzelhebel auf die Haltedauer-Verteilung ist — sie
zu rastern wäre eine eigene, eigens vorzuregistrierende Untersuchung.

Die unselektierten Parameter behalten ihre heutige Einstellung, und zwar als
**festgeschriebene Konstante des Laufs**, nicht als Bezugspunkt einer Grenze.
Das steht so im Register, damit später niemand daraus einen Freiheitsgrad
macht.

**Eine eingetragene Ausnahme:** `elliott_wave` bekommt **keine** Limitachse.
Sein `equity_simulation.py` führt als einziges der neun kein
`max_concurrent_positions`, und zwölf Stellen im Repo erkennen genau daran,
welcher Bot keines hat — das Übergabeprotokoll (Abschnitt 8) hat die Signatur
ausdrücklich so entschieden. Die Achse nachzurüsten wäre eine Änderung an
Bot-Code **und** an einer dokumentierten Entscheidung. Folge, eingetragen: er
läuft gegen die Kapitalschranke `floor(1/ALLOCATION_PCT) = 10` und wird mit
der Markierung „ohne Limitachse" geführt. Sein gemessenes Maximum liegt bei
sieben — die Schranke bindet ohnehin nicht.

---

## 7. Prüfungen und Basislauf

| Test | Ergebnis |
|---|---|
| `research/vorregistrierung/test_vorregistrierung.py` | **150/150** |
| `research/vorregistrierung/pruefe_grenzsaetze.py` | **395/395**, Rückgabewert 0 |
| `research/vorregistrierung/registerbericht.py --pruefen` | Register stimmt mit dem Code überein |
| `shared/test_regimewache.py` | **16/16** |
| `shared/test_agent2_kapitalmass.py` | **34/34** |
| `shared/test_agent2_zielfunktion.py` (TB-22) | **41/41**, unverändert |
| `research/versuchsregister/test_versuchsregister.py` (TB-29) | **41/41**, nach der Umstellung aus Abschnitt 4 |

**Basislauf auf unverändertem `main`:** elf Tests scheitern schon dort
(fehlende `scipy`, `fastapi`, `binance`, `yfinance`, Zeitzone `US/Eastern`
sowie fünf vorbestehende Teilfehlschläge). **Dieselben elf scheitern auf dem
Branch — keiner mehr, keiner anders.** Die Liste steht im Testauftrag,
Schritt 11.

**Ein zwölfter Test ist zeitabhängig, nicht kaputt.**
`system/test_log_rotation.py` startet einen nebenläufigen Schreiberprozess
und wartet auf eine Mindestdateigrösse; unter Last schlagen drei Prüfungen
fehl, einzeln aufgerufen besteht er zuverlässig (`117 von 117`). Er hat mit
TB-30a nichts zu tun — `system/` ist unberührt —, aber er erklärt, warum ein
Reihenlauf je nach Maschinenlast elf oder zwölf Fehlschläge meldet. Das
gehört hierher, damit niemand später die Zahl gegen diese Übergabe hält.

---

## 8. Was der Betreiber tun muss

| | wo |
|---|---|
| **Signierter Tag** (GPG) auf `main`, nach dem Merge | Testauftrag Schritt 8 |
| **Externer Zeitanker** (OpenTimestamps) für Register- und Datenstand-Hash | Testauftrag Schritt 9 |

Beide brauchen Schlüssel bzw. Netz und liessen sich hier nicht erledigen.
`python3 research/vorregistrierung/herkunft.py` meldet den Stand aller vier
Verankerungen; die beiden anderen — *Herkunft in jeder Ergebnisdatei* und
*das Urteil ist Code* — sind erledigt.

---

## 9. Was als Nächstes kommt (TB-30b und TB-31)

1. **Regimewache einbauen**, drei Stellen. **Vorher kein Lauf.**
2. **`max_drawdown_kapital_pct`** in `evaluate_combination_multi` — dann
   wählt Agent 2 von selbst auf dem führenden Mass.
3. **Zwei Achsen durchreichen** (Abschnitt 11.3 des Registers).
4. **TB-31 abwarten** und danach die fünf Krypto-Faltenpläne aus der
   registrierten Regel erzeugen — die Regel steht, die Jahreszahlen nicht.
5. Erst dann: der Lauf. Und danach **keine Entscheidung mehr, nur eine
   Lektüre**.

---

## 10. Der Satz, der wörtlich ins Register gehörte

> **Dieses Ergebnis ist zulässig: Es kann sein, dass kein einziger Bot die
> Schwelle erreicht.** Eine Aussage über den **Backtest**, nicht über die
> Bots. *Wer das vorher nicht aufschreibt, wird es nachher nicht
> akzeptieren.*

Er steht als Zeichenkette in `registerdaten.py::FESTLEGUNGEN[12]` und wird am
Ende **jeder** Bleibt-Geht-Liste ausgegeben — auch dann, wenn kein Bot
ausscheidet. Damit ist er kein Vorsatz mehr, sondern Ausgabe.
