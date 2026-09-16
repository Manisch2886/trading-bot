# TB-40 — Universum-Trockenlauf: Ergebnis

**Stand: 16.09.2026.** Gemessen in der Cloud auf `main` = `ab4a358`, Datenstand
`d9449faf51bffaaa…` (223 Dateien), vor und nach dem Lauf identisch.

> **Hier wurde gemessen und berichtet, nicht geschrieben.**
> `docs/VORREGISTRIERUNG_neuselektion.md` ist **unberührt**;
> `research/vorregistrierung/auswertung.py` und `research/faltenplan_neun/`
> ebenso. Keine Datei unter `data/`, `results/` oder `research/*/ergebnisse/`
> wurde angefasst. Kein Raster gerechnet, kein Parameter übernommen.

---

## Die drei Antworten zuerst

### 1. Die gemessene Symbolzahl je Bot und Falte gegen die eingetragene

Der Loader jedes Bots wurde je Falte einmal am **Faltenbeginn** und einmal am
**letzten Zeitpunkt der Falte** aufgerufen. Daraus zwei Lesarten:

* **H** — *„an mindestens einem Handelstag der Falte handelbar"*, der Wortlaut
  von **Registertext 3b**. Gemessen am Faltenende.
* **F** — *„die Schranke wird am Faltenbeginn geprüft"*, der Wortlaut der
  **Aufgabenbeschreibung TB-40**. Gemessen am Faltenbeginn.

| Bot | eingetragen (Lesart A) | **gemessen H** | gemessen F |
|---|---|---|---|
| `elliott_wave` | 6 / 13 / 13 · B 18 | **6 / 13 / 13 · B 18** | 0 / 6 / 13 · B 13 |
| `t3_supertrend` | 6 / 9 / 13 / 13 / 13 / 17 / 18 · B 23 | **3 / 6 / 9 / 13 / 13 / 13 / 17 · B 18** | 0 / 3 / 6 / 9 / 13 / 13 / 13 · B 17 |
| `rsi2_crypto` | 6 / 9 / 13 / 13 / 13 / 17 / 18 · B 23 | **6 / 9 / 10 / 13 / 13 / 17 / 18 · B 20** | 2 / 6 / 9 / 10 / 13 / 13 / 17 · B 18 |
| `turtle_soup_crypto` | 6 / 9 / 13 / 13 / 13 / 17 / 18 · B 23 | **6 / 9 / 10 / 13 / 13 / 17 / 18 · B 20** | 2 / 6 / 9 / 10 / 13 / 13 / 17 · B 18 |
| `volatility_breakout_crypto` | 6 / 9 / 13 / 13 / 13 / 17 / 18 · B 23 | **6 / 9 / 10 / 13 / 13 / 17 / 18 · B 20** | 2 / 6 / 9 / 10 / 13 / 13 / 17 · B 18 |
| `elliott_wave_stocks` | 140 / 142 / 145 / 147 / 148 / 148 / 149 · B 150 | **137 / 137 / 139 / 139 / 140 / 142 / 145 · B 147** | 136 / 137 / 137 / 139 / 139 / 140 / 142 · B 145 |
| `rsi2_mean_reversion` | dieselbe Reihe | **dieselbe gemessene Reihe** | dieselbe |
| `turtle_soup_stocks` | dieselbe Reihe | **dieselbe gemessene Reihe** | dieselbe |
| `volatility_breakout` | dieselbe Reihe | **dieselbe gemessene Reihe** | dieselbe |

`B` = Bestätigungsperiode. `elliott_wave` hat Doppeljahr-Falten
(2019–2020, 2021–2022, 2023–2024).

**Zwei Aussagen, die für alle neun Bots und alle Falten gelten:**

* **Es kommt nirgends ein Symbol hinzu.** In keiner einzigen Falte enthält die
  gemessene Liste ein Symbol, das die eingetragene Lesart A nicht hätte. Der
  Loader ist überall **strenger**: F ⊆ H ⊆ A.
* **Die Abweichung ist real, aber nicht überall.** `elliott_wave` stimmt unter
  Lesart H **exakt** mit der eingetragenen Reihe überein — bei ihm ist die
  Tatsachennotiz richtig. Bei den übrigen acht nicht.

### 2. Muss die Tatsachennotiz korrigiert werden — und wie lautet die korrigierte Zeile?

**Ja.** Acht der neun Zeilen sind falsch; eine (`elliott_wave`) stimmt.

Die korrigierte Tabelle unter **Lesart H** (Registertext 3b im Wortlaut) — zum
Kopieren, einzutragen in `docs/VORREGISTRIERUNG_neuselektion.md`, Abschnitt
15.5, Tabelle *„Die Symbolzahl je Falte (Tatsachennotiz zu 3b)"*:

```
| Bot | Symbolzahl je Selektionsfalte | Bestätigung | Universum |
|---|---|---:|---:|
| `elliott_wave` | 6 / 13 / 13 | 18 | 24 |
| `t3_supertrend` | 3 / 6 / 9 / 13 / 13 / 13 / 17 | 18 | 24 |
| `rsi2_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
| `turtle_soup_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
| `volatility_breakout_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 | 20 | 24 |
| `elliott_wave_stocks` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
| `rsi2_mean_reversion` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
| `turtle_soup_stocks` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
| `volatility_breakout` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |
```

Falls stattdessen **Lesart F** registriert wird (Faltenbeginn), lautet dieselbe
Tabelle:

```
| `elliott_wave` | 0 / 6 / 13 | 13 | 24 |
| `t3_supertrend` | 0 / 3 / 6 / 9 / 13 / 13 / 13 | 17 | 24 |
| `rsi2_crypto` | 2 / 6 / 9 / 10 / 13 / 13 / 17 | 18 | 24 |
| `turtle_soup_crypto` | 2 / 6 / 9 / 10 / 13 / 13 / 17 | 18 | 24 |
| `volatility_breakout_crypto` | 2 / 6 / 9 / 10 / 13 / 13 / 17 | 18 | 24 |
| die vier Aktien-Bots | 136 / 137 / 137 / 139 / 139 / 140 / 142 | 145 | 150 |
```

⚠️ **Eine zweite Tatsachennotiz im selben Abschnitt ist ebenfalls betroffen** und
in der Aufgabe nicht erwähnt: die Liste **„Symbole ohne Faltenevidenz"**. Heute
stehen dort zwei Listen, eine je Markt (krypto 6, aktien 1). Gemessen am Loader
sind es **Listen je Bot**, und sie fallen auseinander:

| Bot | Symbole ohne Faltenevidenz (Lesart H) |
|---|---|
| `elliott_wave` | 11: BMTUSDT, ENAUSDT, ENSOUSDT, PEPEUSDT, PROMUSDT, PUMPUSDT, SUIUSDT, TRUMPUSDT, UUSDT, WLDUSDT, ZKCUSDT |
| `t3_supertrend` | 7: BMTUSDT, ENAUSDT, ENSOUSDT, PUMPUSDT, TRUMPUSDT, UUSDT, ZKCUSDT |
| die drei Krypto-Tagesbots | 6: BMTUSDT, ENSOUSDT, PUMPUSDT, TRUMPUSDT, UUSDT, ZKCUSDT *(unverändert)* |
| die vier Aktien-Bots | 5: APP, CEG, GEV, HOOD, SNDK *(heute: nur SNDK)* |

Das ist die Kehrseite derselben Sache: was der Loader nicht lädt, liefert auch
keine Evidenz.

### 3. Unterschreitet ein Bot dadurch die Mindestzahl von 3 Falten?

**Unter Lesart H: nein.** Alle neun Bots behalten Falten mit Symbolen —
`elliott_wave` 3 von 3, die übrigen acht 7 von 7. Keine leere Falte, keine Falte
mit nur einem Symbol.

**Unter Lesart F: ja, genau einer.** `elliott_wave` verliert seine erste Falte
(2019–2020, **0 Symbole**) und steht dann bei **2 von 3** — unter der Schwelle
aus Registertext 4b. Damit griffe **Regel 4c**: „unterbestimmt", Schatten
ausserhalb des Buchs, statische Benchmark-Position, Selektion später
nachzuholen. `t3_supertrend` verlöre seine Falte 2019 (ebenfalls 0 Symbole),
bliebe mit 6 von 7 aber deutlich über der Schwelle.

**Die kleinste Falte je Bot** — für die Frage „ist eine Falte mit fast keinen
Symbolen noch eine Falte?":

| Bot | kleinste Selektionsfalte unter H | unter F |
|---|---:|---:|
| `elliott_wave` | 6 | **0** |
| `t3_supertrend` | **3** | **0** |
| die drei Krypto-Tagesbots | 6 | **2** |
| die vier Aktien-Bots | 137 | 136 |

⚠️ **Das ist eine Registerfrage, keine Entwurfsfrage,** und sie wird hier nicht
entschieden — aber sie ist jetzt scharf: **die Wahl zwischen H und F entscheidet
darüber, ob `elliott_wave` selektiert wird oder als unterbestimmt gilt.**

Und sie hat eine Fortsetzung, die die Festlegung ebenfalls nicht regelt: Auch
unter der milderen Lesart H hat `t3_supertrend` in seiner Falte 2019 nur **drei**
Symbole. Ob eine solche Falte zählt, sagt weder Registertext 4b noch 3b. Hier
wird nur ausgezählt.

---

## Wie die Frage gemessen wurde

`research/universum_trockenlauf/universum_trockenlauf.py --nur-universum`

Der **Loader des Bots** entscheidet — `load_all_symbol_data()` aus
`strategies/<bot>/multi_symbol_optimise.py`, unverändert ausgeführt. Nichts ist
nachgebaut.

**Der gemeldete Befund zum Import.** Die Aufgabe verlangt zugleich „der Laufcode
entscheidet" und „Bot-Dateien werden gelesen, nie importiert". Beides zusammen
geht nicht: `load_all_symbol_data()` ist eine Funktion in einem Modul und läuft
nur, wenn das Modul geladen wird. Aufgelöst ist das so: **der Import findet
statt, aber in einem eigenen Prozess je Bot.** Damit kann keine der neun
gleichnamigen Dateien eine andere in `sys.modules` verdrängen — nicht weil
jemand aufpasst, sondern weil jeder Prozess seinen eigenen `sys.modules` hat.
Das ist strenger als jede Namensvergabe im selben Prozess.

**Was am Laufcode verändert wurde:** genau zwei Dinge, beide an der *Eingabe*,
keines an der *Entscheidung*.

1. `pandas.read_csv` liefert die Kursdatei **bis zum Stichtag**. Das ist die
   Übersetzung von „je Falte, nicht nur heute": ein Lauf am 1. Januar 2019 sieht
   keine Kerze von 2024. Die Datei auf der Platte bleibt unberührt.
2. `binance.client.Client.ping` ist stillgelegt — siehe Nebenbefund 1 unten.

**Warum Lesart H am Faltenende genügt.** Jede der neun Schranken vergleicht eine
**nicht fallende** Grösse (Zeitspanne bzw. Kerzenzahl der sichtbaren Daten) mit
einer Konstanten. Wer irgendwann in der Falte handelbar ist, ist es am Ende der
Falte auch. Das Werkzeug verlässt sich darauf nicht, sondern **prüft es nach**:
über alle Stichtage aller neun Bots wächst die Menge der handelbaren Symbole nur
— keine Verletzung gemeldet.

---

## Die weiteren Fragen aus der Aufgabe

### Ist `MIN_HISTORY_DAYS` je Bot gleich?

**Nein — und bei einem Bot heisst sie nicht einmal so.** Gemessen am geladenen
Modul, nicht angenommen:

| Bot | Raster | Schranke | misst | Zehnjahresfenster |
|---|---|---|---|---|
| `elliott_wave` | 1h | **`MIN_HISTORY_HOURS` = 17520** | **Kerzenzahl** (`len(df)`) | – |
| `t3_supertrend` | 4h | `MIN_HISTORY_DAYS` = 730 | Zeitspanne | – |
| `rsi2_crypto` | 1d | `MIN_HISTORY_DAYS` = 500 | Zeitspanne | – |
| `turtle_soup_crypto` | 1d | `MIN_HISTORY_DAYS` = 500 | Zeitspanne | – |
| `volatility_breakout_crypto` | 1d | `MIN_HISTORY_DAYS` = 500 | Zeitspanne | – |
| `elliott_wave_stocks` | 1d | `MIN_HISTORY_DAYS` = 1825 | Zeitspanne | 10 Jahre, **vor** der Prüfung |
| `rsi2_mean_reversion` | 1d | `MIN_HISTORY_DAYS` = 1825 | Zeitspanne | 10 Jahre, nur für Einstiege |
| `turtle_soup_stocks` | 1d | `MIN_HISTORY_DAYS` = 1825 | Zeitspanne | 10 Jahre, nur für Einstiege |
| `volatility_breakout` | 1d | `MIN_HISTORY_DAYS` = 1825 | Zeitspanne | 10 Jahre, nur für Einstiege |

**Fünf verschiedene Werte und zwei verschiedene Grössen.** Registertext 3b sagt,
der Wert sei „fest auf dem heutigen Wert" — *je Bot* heisst dann wirklich je Bot,
und der Registereintrag muss beide Namen und beide Grössen nennen, nicht nur
`MIN_HISTORY_DAYS`.

Der Unterschied ist nicht nur begrifflich: `elliott_wave` zählt **Kerzen**.
Eine Reihe mit derselben Zeitspanne, aber Lücken, fällt bei ihm heraus und bei
den anderen acht nicht — das ist gemessen, nicht gelesen (siehe nächster
Abschnitt, Fall *luecke_gleiche_spanne*).

### Gibt es weitere stille Filter im Loader?

`research/universum_trockenlauf/universum_trockenlauf.py --stille-filter` hält
jedem der neun Loader dieselben sieben Fälle hin und schaut zu, was er damit
macht. **„STILL raus"** heisst: aussortiert, ohne dass der Loader das Symbol in
seiner Ausgabe überhaupt nennt — auch das gemessen, indem die Ausgabe des Laufs
mitgeschrieben wurde.

| Bot | voll | genau an der Grenze | eins zu kurz | Datei fehlt | Datei leer | nur leere Kerzen | Lücke, gleiche Spanne |
|---|---|---|---|---|---|---|---|
| `elliott_wave` | geladen | geladen | gemeldet | gemeldet | gemeldet | gemeldet | **gemeldet raus** |
| `t3_supertrend` | geladen | geladen | gemeldet | gemeldet | **STILL** | gemeldet | geladen |
| `rsi2_crypto` | geladen | geladen | gemeldet | gemeldet | **STILL** | gemeldet | geladen |
| `turtle_soup_crypto` | geladen | geladen | gemeldet | gemeldet | **STILL** | gemeldet | geladen |
| `volatility_breakout_crypto` | geladen | geladen | gemeldet | gemeldet | **STILL** | gemeldet | geladen |
| `elliott_wave_stocks` | geladen | geladen | gemeldet | gemeldet | **STILL** | gemeldet | geladen |
| `rsi2_mean_reversion` | geladen | geladen | **STILL** | **STILL** | **STILL** | gemeldet | geladen |
| `turtle_soup_stocks` | geladen | geladen | **STILL** | **STILL** | **STILL** | gemeldet | geladen |
| `volatility_breakout` | geladen | geladen | **STILL** | **STILL** | **STILL** | gemeldet | geladen |

Vier Befunde daraus:

1. **Die Grenze ist einschliesslich.** Exakt `MIN_HISTORY_DAYS` Tage bzw. exakt
   `MIN_HISTORY_HOURS` Kerzen werden **geladen**, eine Einheit weniger nicht.
   Gemessen an erzeugten Beispieldaten, an zwei Bots mit verschiedener Schranke.
2. **Drei Bots sortieren völlig lautlos aus:** `rsi2_mean_reversion`,
   `turtle_soup_stocks`, `volatility_breakout` schreiben bei zu kurzer Historie
   und bei fehlender Kursdatei **keine Zeile**. Der Befund, der diese Aufgabe
   ausgelöst hat, war bei `rsi2_crypto` sichtbar, weil dieser Bot es meldet — bei
   diesen dreien wäre dieselbe Sache unbemerkt geblieben.
3. **Eine leere Kursdatei ist bei acht von neun ein stiller Ausfall**
   (`if df.empty: continue`).
4. **Ein Symbol, dessen Kursspalten leer sind, verschwindet** — aber
   `shared/kursdaten.py` meldet es namentlich. Das ist die eine Stelle, an der
   das Projekt es schon richtig macht.

Ein Mindestvolumen-Filter im Loader existiert bei keinem der neun.

---

## Zwei Nebenbefunde am Rande

Beide ändern keine Zahl, kosten aber beim nächsten Lesen Zeit.

1. ⚠️ **Der Import von `strategies/elliott_wave/multi_symbol_optimise.py`
   braucht Netz.** Er holt `INTERVAL` aus `shared/fetch_multi_data.py`, und die
   Datei legt auf Modulebene ein `client = Client()` an; `python-binance` pingt
   im Konstruktor `api.binance.com`. In der Cloud scheitert das mit 403, auf dem
   Mac kostet es bei jedem Import eine Netzrunde — für eine Konstante. Der
   Trockenlauf legt den Ping still; die Konstanten der Klasse bleiben
   unangetastet. **Kein Handlungsbedarf für TB-40**, aber ein Kandidat für die
   nächste Aufräumrunde.
2. **Die Klammer hinter der Universumsgrösse stimmt rechnerisch nicht.**
   Registerabschnitt 15.5 schreibt für `config/top25_symbols.txt`
   „24 (26 Zeilen abzüglich `XAUTUSDT`, `PAXGUSDT`)". Die Datei mit dem
   **eingetragenen Hash** `3afc95a4…` hat **25 Zeilen**, und `PAXGUSDT` steht
   nicht darin; `shared/symbols_config.py` streicht nur `XAUTUSDT`. Das Ergebnis
   **24 ist richtig**, der Rechenweg in der Klammer nicht. Der Hash ist geprüft
   und identisch — es ist dieselbe Datei, nur die Beschreibung daneben stimmt
   nicht.

---

## Was nachgewiesen ist

| Nachweis | Wie |
|---|---|
| Datenstand vor und nach dem Lauf identisch | `herkunft.datenstand()` vor/nach: `d9449faf51bffaaa…`, 223 Dateien — unverändert. Test B. |
| Der Trockenlauf schreibt nichts | Schreibschutz im Kindprozess, der jeden Schreibversuch zum Abbruch macht. Test G. |
| Wiederholbar | zweiter Lauf, gleiche Listen — Symbol für Symbol, nicht nur gleiche Anzahl. Test C. |
| Ein künstlich verkürztes Symbol fällt heraus | erzeugte Beispieldaten, am Ablauf, an zwei Bots mit verschiedener Schranke. Test D. |
| Ein Symbol genau an der Grenze | exakt 500 Tage → geladen; 499 → nicht. Exakt 17520 Kerzen → geladen; 17519 → nicht. Test D. |
| Der Vergleich meldet eine Abweichung | veränderte Registerzahl in einer Kopie → die gemeldete Differenz verschiebt sich, die Messung bleibt. Test E. |
| Mutationsprobe Stichtag | Stichtag wirkungslos gemacht → jede Falte misst den heutigen Stand, und es fällt auf. Test F. |
| Mutationsproben, beide Wachen einzeln | Schreibschutz allein bricht ab (G); ohne ihn läuft derselbe Defekt klaglos durch und der Datenstand-Hash allein findet ihn (H). |
| Monotonie | über alle Stichtage wächst die Symbolmenge nur. Test I. |

`python3 research/universum_trockenlauf/test_universum_trockenlauf.py` →
**42/42 Prüfungen bestanden.**

---

## In einfacher Sprache

**Was wir wissen wollten.**
Neun Handelsprogramme („Bots") sollen demnächst neu eingestellt werden. Damit
das nachprüfbar bleibt, ist vorher aufgeschrieben, wie gerechnet wird — dieses
Vorab-Dokument heisst „Register". Darin steht unter anderem, **wie viele
Handelswerte** (Aktien oder Kryptowährungen) in jedem Prüfzeitraum überhaupt
mitgerechnet werden können. Ein Prüfzeitraum ist hier meist ein Kalenderjahr und
heisst im Register „Falte". Wir wollten wissen: **Stimmen diese Zahlen?**

**Was herauskam.**
Acht der neun Zahlenreihen stimmen **nicht**. Sie sind durchweg **zu hoch** —
die Programme rechnen mit **weniger** Werten, als im Register steht. Bei den
Aktien-Bots stehen dort zum Beispiel 150 für den jüngsten Zeitraum, tatsächlich
sind es 147. Bei drei Krypto-Bots stehen 23, tatsächlich sind es 20. Nur ein Bot
(`elliott_wave`) stimmt genau. Es kommt **nirgends** ein Wert hinzu — es fallen
nur welche weg.

**Warum das so ist.**
Zwei verschiedene Programme beantworteten bisher dieselbe Frage, und sie meinen
nicht dasselbe. Das eine fragt: *„Gibt es für diesen Wert überhaupt Kursdaten?"*
Das andere — das Programm, das später wirklich rechnet — fragt strenger:
*„Gibt es genug Kursdaten, nämlich mindestens so viele Jahre?"* Ein junges
Unternehmen oder eine junge Kryptowährung besteht die erste Frage, die zweite
aber nicht. Weil bisher die Antwort des ersten Programms im Register stand,
standen dort zu grosse Zahlen. Wir haben jetzt das **richtige** Programm gefragt
— dasselbe, das später auch rechnet.

Dabei ist noch etwas aufgefallen: Die Anforderung „genug Kursdaten" ist bei jedem
Bot **anders** — mal zwei Jahre, mal fünf. Und ein Bot zählt nicht Jahre, sondern
einzelne Kurspunkte. Ausserdem werfen drei Bots Werte **wortlos** heraus: In
ihrer Ausgabe steht kein Hinweis, dass etwas fehlt. Man sieht es nur, wenn man
gezielt nachschaut.

**Was das für dich heisst.**
Drei Dinge, und alle drei sind jetzt **noch kostenlos**, weil der Lauf noch nicht
gestartet ist:

1. **Die Zahlen im Register müssen korrigiert werden.** Die fertige, korrigierte
   Tabelle steht oben zum Kopieren. Eingetragen wird sie **nicht jetzt**, sondern
   gemeinsam mit den übrigen offenen Registertexten — so war es vorgesehen.
2. **Eine Entscheidung ist zu treffen, und nur du kannst sie treffen.** Es gibt
   zwei vertretbare Lesarten davon, was „in dieser Falte dabei" heisst: entweder
   *„irgendwann in diesem Jahr handelbar"* (Lesart H, so steht es im Register)
   oder *„schon am 1. Januar handelbar"* (Lesart F, so steht es in der
   Aufgabenbeschreibung). Beide Zahlenreihen liegen oben vor. **Der Unterschied
   ist nicht kosmetisch:** Bei Lesart F hat der Bot `elliott_wave` in seinem
   ersten Prüfzeitraum **null** Werte, ihm bleiben dann nur zwei statt der
   geforderten drei Prüfzeiträume — und er dürfte gar nicht neu eingestellt
   werden, sondern liefe als „unterbestimmt" weiter. Bei Lesart H passiert das
   nicht.
3. **Es ist nichts verloren gegangen.** Kein Kurs, kein Programm, keine
   Einstellung wurde verändert. Der Trockenlauf liest nur — das ist geprüft,
   nicht bloss behauptet: Wir haben das Programm absichtlich kaputt gemacht, so
   dass es schreiben *wollte*, und beide Sicherungen haben es erwischt.

---

*TB-40, 16.09.2026. Kein Selektionslauf, kein Registereintrag, keine
Parameterübernahme.*
