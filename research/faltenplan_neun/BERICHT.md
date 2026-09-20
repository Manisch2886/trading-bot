# Faltenplan für alle neun Bots — Verfahren B (TB-36)

**Status: reine Untersuchung und Registerarbeit. KEINE Änderung an Bot-,
Backtest- oder Live-Dateien.** Alle Rechenteile liegen unter
`research/faltenplan_neun/`; geändert wurde ausserdem nur
`docs/VORREGISTRIERUNG_neuselektion.md` (Abschnitt 15 neu, vier Verweise im
alten Text) und `docs/`. `live_params.py`, `forward_test.py` und die
Backtest-Dateien wurden **als Text gelesen, nie importiert**. Der Datenstand
ist unverändert `d9449faf51bffaaa…` bei 223 Kursdateien.

---

## 1. Die Antwort zuerst

**Die Krypto-Gegenprobe stimmt — exakt.** Das neue Werkzeug liefert für alle
fünf Krypto-Bots dieselben Zahlen wie `research/krypto_historie/faltenplan.py`
mit `--mindesttraining 0`: erste Falte **2019**, sieben Selektionsfalten bei
den Tagesbots (und bei `t3_supertrend`), **drei** Doppeljahr-Falten bei
`elliott_wave`, Symbole je Falte **6 / 9 / 13 / 13 / 13 / 17 / 18**,
Bestätigung **23**. Verglichen wird nicht nur die Anzahl, sondern die
**Symbolliste je Falte, namentlich**, und beide Werkzeuge laufen dafür als
eigener Prozess auf denselben Kursdateien (`test_faltenplan_neun.py`, Teil A).

**Die vier Aktien-Bots haben je sieben Selektionsfalten** — 2019 bis 2025,
Bestätigungsperiode 2026 — und **je Falte 140 / 142 / 145 / 147 / 148 / 148 /
149 Symbole**, Bestätigung **150 von 150**. Alle vier teilen Universum
(`config/sp500_top150.txt`) und Faltenplan; es gibt keinen Unterschied
zwischen ihnen.

**Kein Bot ist unterbestimmt.** Der niedrigste Wert ist 3 (`elliott_wave`) und
erreicht die Schwelle aus Registertext 4b genau.

---

## 2. Was gerechnet wurde

| | |
|---|---|
| `faltenplan_neun.py` | Faltenliste je Bot, Symbolzahl je Falte, beide Lesarten des Indikator-Vorlaufs |
| `embargo_neun.py` | Embargo je Bot nach Registertext 2d |
| `test_faltenplan_neun.py` | 145 Prüfungen, davon vier Mutationsproben |
| `daten/faltenplan.json`, `daten/embargo.json` | die Ergebnisse, maschinenlesbar |

Beide Werkzeuge sind **reine Standardbibliothek** — kein `pandas`, kein
`numpy`. Das ist keine Sparsamkeit, sondern eine Voraussetzung: in der
Cloud-Umgebung ist `pandas` nicht installiert, und ein Werkzeug, das die Zahlen
des Registers erzeugt, muss überall dort laufen, wo jemand sie nachrechnen
will.

### Die Entscheidung: ein neues Werkzeug, die beiden alten unangetastet

Die Aufgabe stellt die Frage ausdrücklich — erweitern oder neu? Es gibt heute
zwei Werkzeuge, die Falten rechnen, und beide reichen nicht:

* `research/krypto_historie/faltenplan.py` (TB-31) rechnet Falten **und**
  Symbole je Falte, aber nur für die fünf Krypto-Bots, mit fest verdrahteter
  Bot-Liste und dem Argument `--mindesttraining`.
* `research/vorregistrierung/faltenplan.py` (TB-30a) deckt alle neun Bots ab,
  kennt aber **keine** Symbolzahl je Falte, trägt Trainingsfenster, Purge und
  Embargo zwischen den Falten und führt Krypto als Platzhalter.

Entschieden ist: **neu**, und zwar aus drei Gründen.

1. Beide sind **Belege abgeschlossener Untersuchungen**. Wer sie umschreibt,
   ändert rückwirkend, womit damals gerechnet wurde. Der TB-31-Faltenplan ist
   ausserdem genau die Zahlenreihe, an der das neue Werkzeug gemessen wird — er
   muss stehen bleiben, sonst misst die Gegenprobe sich selbst.
2. Beide sprechen **Verfahren A**. Eine Erweiterung hätte beide Sprachen
   gleichzeitig tragen müssen, und das ist die Art von Doppeldeutigkeit, die
   dieses Register gerade beseitigt.
3. Der Einwand „die Faltenlogik soll genau einmal existieren" ist berechtigt.
   Er wird hier nicht durch ein Versprechen eingelöst, sondern durch eine
   **Messung**: Teil A des Selbsttests rechnet die fünf Krypto-Bots mit beiden
   Werkzeugen und vergleicht Falte für Falte und Symbol für Symbol. Laufen sie
   auseinander, fällt der Test. Nach TB-30b, wenn die sechs bot-eigenen
   Walk-Forward-Rechner ersetzt sind, bleibt dieses Werkzeug übrig und die
   beiden alten sind Archiv.

Der Ordnername `krypto_historie` spricht ohnehin dagegen, einen Aktienteil dort
hineinzulegen — und der Modulname ist bewusst `faltenplan_neun.py` und nicht
`faltenplan.py`: drei gleichnamige Module kollidierten in `sys.modules`, genau
die Falle, vor der die Aufgabenstellung bei den neun `equity_simulation.py`
warnt.

---

## 3. Der Faltenplan

| Bot | Markt | Länge | Selektionsfalten | # | Bestätigung | Symbole je Falte |
|---|---|---:|---|---:|---|---|
| `elliott_wave` | krypto | 2 J | 2019–2020, 2021–2022, 2023–2024 | 3 | ab 2025-01-01 | 6 / 13 / 13 → 18 |
| `t3_supertrend` | krypto | 1 J | 2019 … 2025 | 7 | ab 2026-01-01 | 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 |
| `rsi2_crypto` | krypto | 1 J | 2019 … 2025 | 7 | ab 2026-01-01 | 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 |
| `turtle_soup_crypto` | krypto | 1 J | 2019 … 2025 | 7 | ab 2026-01-01 | 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 |
| `volatility_breakout_crypto` | krypto | 1 J | 2019 … 2025 | 7 | ab 2026-01-01 | 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 |
| `elliott_wave_stocks` | aktien | 1 J | 2019 … 2025 | 7 | ab 2026-01-01 | 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 |
| `rsi2_mean_reversion` | aktien | 1 J | 2019 … 2025 | 7 | ab 2026-01-01 | 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 |
| `turtle_soup_stocks` | aktien | 1 J | 2019 … 2025 | 7 | ab 2026-01-01 | 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 |
| `volatility_breakout` | aktien | 1 J | 2019 … 2025 | 7 | ab 2026-01-01 | 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 |

Drei Dinge, die man an dieser Tabelle nicht sieht und wissen sollte:

**Die erste Falte 2019 kommt vom Register, nicht aus den Daten.** Ohne die
Schranke `ERSTE_MOEGLICHE_FALTE = 2019` begänne der Plan bei **acht der neun**
Bots schon 2017 oder 2018 — Bitcoin-Daten reichen bis 2017-08-17 zurück, die
Aktiendaten im Zehnjahresfenster bis 2016-09-01. Nur bei `rsi2_crypto` bindet
die Datenlage selbst: sein SMA-Trendfilter braucht 150 Tagesbalken, und die
sind erst zum 1. Januar 2019 beisammen. Mutationsprobe F zeigt das, indem sie
die Schranke entfernt und nachweist, dass dann acht Pläne früher beginnen.

**Doppeljahre bekommt genau ein Bot, und die Regel dafür ist nachgerechnet.**
Registerregel 5.1 Nr. 6 („zwei Jahre bei unter 30 gefundenen Trades je Jahr",
Festlegung 7) auf den gefundenen Trades aus `research/tb24_haltedauern/`,
angeschnittene Randjahre ausgenommen wie in 5.4 beschrieben — Ergebnis wie
dort: `elliott_wave` mit 26,0 Trades je vollem Kalenderjahr, die übrigen acht
zwischen 50,9 und 1.202,2.

**Sieben Symbole haben keine Faltenevidenz.** Krypto: `BMTUSDT`, `ENSOUSDT`,
`PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT`. Aktien: `SNDK`. Für sie gilt der
gewählte Parametersatz live, ohne dass eine einzige Selektionsfalte etwas über
sie sagt. Das ist die Kehrseite des heutigen Universums und steht deshalb
namentlich im Register.

---

## 4. Das Embargo

Registertext 2d: **längste Zeitbremse in Handelstagen + 1**; ohne Zeitbremse
**95. Perzentil der Haltedauer + 1**.

| Bot | Grundlage | Handelstage | **Embargo** |
|---|---|---:|---:|
| `elliott_wave` | `MAX_HOLD_HOURS` = 240 Stundenbalken | 10 | **11** |
| `t3_supertrend` | **keine Zeitbremse** → P95 = 11,21 Tage | 11,21 | **13** |
| `rsi2_crypto` | `MAX_HOLD_DAYS` = 10 | 10 | **11** |
| `turtle_soup_crypto` | `MAX_HOLD_DAYS` = 10 | 10 | **11** |
| `volatility_breakout_crypto` | `MAX_HOLD_DAYS` = 15 | 15 | **16** |
| `elliott_wave_stocks` | `MAX_HOLD_HOURS` = 90 Tagesbalken | 90 | **91** |
| `rsi2_mean_reversion` | `MAX_HOLD_DAYS` = 10 | 10 | **11** |
| `turtle_soup_stocks` | `MAX_HOLD_DAYS` = 10 | 10 | **11** |
| `volatility_breakout` | `MAX_HOLD_DAYS` = 15 | 15 | **16** |

Die Fundstelle jeder Zahl — Datei und Zeilennummer — steht in
`daten/embargo.json` und in der Ausgabe von `embargo_neun.py`. Sie wird bei
jedem Lauf neu **aus der Bot-Datei gelesen**, nicht abgeschrieben;
Mutationsprobe I ändert die Zeitbremse in einer Kopie der Bot-Datei und weist
nach, dass das Embargo mitwandert.

**Genau ein Bot hat keine Zeitbremse: `t3_supertrend`.** Das ist die
TB-24-Messung, nicht eine Vermutung: seine Ausstiegsarten sind `stop_loss`,
`trend_flip` und `t3_crossunder` — keine Uhr darunter —, und der TB-24-Bericht
nennt ausdrücklich **acht** Bots mit Zeitausstieg. Sein P95 ist auf denselben
Positionen gerechnet wie die dortigen Kennzahlen; dass die Perzentilrechnung
zeichengleich zu `pandas.Series.quantile` arbeitet, prüft Teil D an den in
TB-24 veröffentlichten P90-Werten **aller neun** Bots nach.

`elliott_wave_stocks` führt als einziger **zwei** Zeitbremsen: 90 Tagesbalken
im Backtest, 130 **Kalendertage** im Live-Lauf. Die 130 Kalendertage sind an
der Kursreihe nachgemessen 89 Handelstage — die 90 Balken sind also die
längere. Der Kommentar im Bot („entspricht ~90 Handelstage") trifft damit auf
einen Tag genau.

---

## 5. Die eine Stelle, an der eine Lesart nötig war

Registertext 3a sagt: Symbole, „für die am 1. Januar der Falte Kursdaten
**einschliesslich Indikator-Vorlauf** vorliegen". Das lässt zwei Lesarten zu.

**Lesart A (eingetragen):** Kursdaten liegen am 1. Januar vor. Der
Indikator-Vorlauf speist sich aus der eigenen Historie des Symbols und läuft,
wo er noch nicht voll ist, in die Falte hinein — das Symbol handelt dort ein
paar Tage später und trägt für diese Tage 0 bei.

**Lesart B:** Kursdaten **und** voller Vorlauf liegen am 1. Januar vor, sonst
zählt das Symbol nicht mit.

Lesart A gilt, und die Begründung steht nicht im Werkzeug, sondern im Register
selbst:

* Registertext 3b nennt **eine** Zahlenreihe für **alle** Krypto-Tagesbots.
  Hinge die Zahl am Vorlauf, hätte jeder Bot seine eigene — `rsi2_crypto` 150
  Balken, `turtle_soup_crypto` 30, `volatility_breakout_crypto` 127.
* Der nächste Satz von 3a sagt, dass Symbole ohne Historie **0 beitragen**,
  nicht dass sie ausgeschlossen werden. Wer sie ausschliesst, kann sie nicht
  mehr 0 beitragen lassen.
* Die Gegenprobe aus TB-31 ist „nicht verhandelbar" — und sie ist die
  Zahlenreihe der Lesart A.

Der **Preis** dieser Lesart ist gerechnet und steht im Register neben der Zahl
(Abschnitt 15.5): bei fünf der neun Bots weicht Lesart B ab, am deutlichsten
bei `rsi2_crypto` (Falte 2021: 9 statt 13 Symbole; Bestätigung 20 statt 23).
Ein Preis, den eine Festlegung kostet, gehört neben die Festlegung.

---

## 6. Vier Befunde am Rande

Keiner ändert eine Zahl. Sie stehen hier, weil sie sonst beim nächsten Lesen
erneut Zeit kosten.

1. **Die Bezeichnung „AF.2 Nr. 6" gibt es in diesem Repo nicht.** Gemeint — und
   angewandt — ist die Doppeljahr-Regel aus **Abschnitt 5.1 Nr. 6** samt ihrer
   Auswertung in **5.4**. Die Regel wurde nachgelesen, nicht erfunden; nur ihr
   Aktenzeichen stimmt nicht.
2. **Drei „ersetzte Fassungen" haben im Register nie gestanden** — die
   Mindestzahl 10 Trades (1c), „mindestens 4" Selektionsfalten (4b) und „behält
   seine heutigen Parameter" (4c). Gesucht wurde im ganzen Register, in
   `research/vorregistrierung/` und in `docs/`. Sie stammen aus früheren
   Beratungsrunden. Die Klammerzusätze bleiben wörtlich stehen, weil sie
   festhalten, wogegen entschieden wurde; eingetragen sind sie als
   **Erstfassung**, nicht als Widerruf.
3. **`research/vorregistrierung/auswertung.py` rechnet weiterhin nach Verfahren
   A.** Es liest `faltenplan.py` mit Trainingsfenstern, Purge und Embargo
   zwischen den Falten und kennt für Krypto nur Platzhalter. Das ist Absicht:
   die Datei ist **eingefroren** und wurde nicht angefasst. Ihre Umstellung ist
   **TB-30b**. Bis dahin beschreibt der Nachtrag, was gerechnet wird, und
   `auswertung.py` kann es noch nicht — wer beides verwechselt, hält das
   Register für widersprüchlich, obwohl es nur voraus ist.
4. **Die Bots selbst überspringen kurze Historien** (`MIN_HISTORY_DAYS`: 1825
   Tage bei den vier Aktien-Bots, 500 bei drei Krypto-Bots). Betroffen sind
   `GEV`, `SNDK`, `CEG` (Aktien) sowie `ENSOUSDT`, `PUMPUSDT`, `ZKCUSDT`,
   `UUSDT` (Krypto). Die Symbolzahlen sagen also, wie viele Symbole Evidenz
   liefern **können**, nicht wie viele der heutige Bot-Code lädt. Auch diese
   Angleichung gehört in TB-30b.

---

## 7. Die Prüfungen

`python3 research/faltenplan_neun/test_faltenplan_neun.py` — **145 Prüfungen**,
Rückgabewert 0.

| Teil | Was er zeigt |
|---|---|
| A | Die Gegenprobe Krypto gegen das TB-31-Werkzeug, Falte für Falte und Symbol für Symbol, beide als eigener Prozess |
| B | Die im Register eingetragenen Tabellen stimmen mit der Rechnung überein — gelesen, nicht abgeschrieben |
| C | Ein Symbol ohne Historie in einer Falte wird **nicht ausgeschlossen**: „mit Historie + ohne Historie = Universum" gilt in jeder Falte, im Wegwerf-Universum und im echten |
| D | Embargo an einem Bot mit Zeitbremse und an einem ohne; P95 an einer Reihe mit bekanntem Ergebnis (1…100 → 95,05); P90 aller neun Bots gegen die TB-24-Veröffentlichung |
| E | Registertext vollständig, jede ersetzte Fassung gekennzeichnet — und **keine Zeile der Vorfassung gelöscht**, maschinell gegen die letzte committete Fassung ohne Nachtrag |
| F–I | Vier Mutationsproben |

**Zu den Mutationsproben.** Sie sind gegen die zwei Fallen gebaut, die in
diesem Projekt wiederholt aufgetreten sind:

*Eine Probe, deren Zustand der Test von Hand herstellt, bestätigt sich
selbst.* Deshalb wird keine Variable im laufenden Prozess umgebogen und
anschliessend dieselbe Variable abgefragt. Jede Probe kopiert den Ordner (bei I
die Bot-Datei), ändert dort **eine** Zeile und startet das Werkzeug als
**eigenen Prozess** auf denselben Daten; beobachtet wird der Ablauf. Und jede
zeigt zuerst, dass sie **ohne** Mutation das Richtige sieht — sonst belegte ein
rotes Ergebnis nichts.

*Eine zweite Wache verdeckt das Fehlen der ersten.* Die vier Proben greifen
deshalb vier verschiedene Wachen an, und jede weist nach, dass genau ihre Zahl
kippt und die anderen stehen bleiben:

* **F** entfernt die Registerschranke 2019. Ohne sie beginnen acht Pläne früher
  — und sehen dabei **besser** aus, weil es mehr Falten werden. Die
  Symbolzahlen bleiben dabei unverändert richtig; ohne eigene Probe fiele es
  nicht auf.
* **G** entfernt die Doppeljahr-Schwelle. `elliott_wave` bekommt sieben
  Einzeljahr-Falten statt drei Doppeljahre — erste Falte und Symbolzahlen
  bleiben richtig.
* **H** entfernt den Indikator-Vorlauf eines Bots. Die nachrichtliche Lesart B
  wird zur stillen Kopie von Lesart A; die eingetragene Zahl ändert sich nicht,
  die Aussage über ihren Preis schon.
* **I** ändert die Zeitbremse in der **Bot-Datei**, nicht im Werkzeug. Bliebe
  das Embargo stehen, käme die Zahl nicht aus dem Bot, sondern aus einer
  Abschrift — und nur bei diesem einen Bot darf sie sich ändern.

**Nachtrag TB-72 (20.09.2026) — zwei weitere Dateien in diesem Ordner.**
`erste_falte_trockenlauf.py` misst Bedingung (ii) der Neufassung von
Registertext 4a / 21.3 (b) (Register Abschnitt 25): ob der Loader eines Bots in
einer Falte mindestens ein Symbol handelbar macht — über `messe_bot` des
TB-40-Trockenlaufs im Kindprozess, nicht nachgerechnet. Seit TB-72 leitet
`research/vorregistrierung/faltenplan.py::erste_falte` die erste Falte daraus
ab (4a-Kandidaten, erste mit `H ≥ 1`); die Regel steht im Register, die
Messung hier, die Ableitung dort — keine Parallelrechnung. Sein `main()` ist
die Messung aus TB-72 Schritt 1 in beide Richtungen
(`docs/ERGEBNIS_TB-72_schritt1_erste_falte.md`).
`test_erste_falte_trockenlauf.py` (`trading-env/bin/python3`, rund drei
Minuten, **50 Prüfungen**) ist der Neun-Zahlen-Vergleich: erste Falte laut Plan
= erste 4a-Kandidatenfalte mit `H ≥ 1` (eigener `messe_bot`-Aufruf, unabhängig
von `erste_falte_trockenlauf`) = Register 21.4, erste Falte nie vor 4a, und
eine Mutationsprobe in einer Wegwerf-Kopie im eigenen Prozess: setzt jemand in
`faltenplan.py` die 4a-Nachrechnung wieder an die Stelle der Ableitung, meldet
die Probe `t3_supertrend` 2018 statt 2019. Nach Fable ist der Test damit
*„nicht mehr eine Wache gegen Abweichung, sondern der Nachweis, dass die
Ableitung nicht regrediert"*.

---

## 8. In einfacher Sprache

**Was wir wissen wollten.** Bevor die grosse Parametersuche startet, muss
festgeschrieben sein, *worauf* gerechnet wird: in welche Zeitabschnitte
(„Falten") die Vergangenheit zerlegt wird, welche Aktien und Kryptowährungen in
jedem Abschnitt überhaupt vorkommen, und wie viele Tage nach dem Stichtag
übersprungen werden müssen, damit alte Positionen die Prüfperiode nicht
verunreinigen. Das stand bisher nur für die Kryptowährungen fest, und selbst
dort nach einem Verfahren, das inzwischen verworfen ist.

**Was herauskam.** Acht der neun Bots bekommen sieben Abschnitte — die Jahre
2019 bis 2025 —, geprüft wird dann am Jahr 2026. Ein Bot (`elliott_wave`,
Kryptowährungen) handelt so selten, dass seine Abschnitte doppelt so lang sein
müssen; er bekommt drei. Bei den Kryptowährungen wächst die Zahl der
handelbaren Münzen von 6 im Jahr 2019 auf 18 im Jahr 2025, bei den Aktien von
140 auf 149 von 150. Die Wartezeit vor der Prüfperiode beträgt je nach Bot 11
bis 91 Tage. Sieben Wertpapiere sind so neu, dass über sie kein einziger
Abschnitt etwas aussagt.

**Warum das so ist.** Eine Münze kann erst gehandelt werden, wenn es sie gibt —
Bitcoin gibt es in unseren Daten seit 2017, andere erst seit 2025. Die
Wartezeit richtet sich danach, wie lange ein Bot eine Position höchstens hält:
`volatility_breakout` hält bis zu 15 Handelstage, also warten wir 16. Ein Bot
hat gar keine solche Obergrenze; für ihn haben wir gemessen, wie lange seine
längsten 5 % der Positionen dauern, und darauf einen Tag aufgeschlagen. Alle
diese Zahlen sind aus den vorhandenen Dateien **abgelesen oder nachgerechnet**,
keine ist geschätzt.

**Was das für dich heisst.** Der Registereintrag ist vollständig; die
Parametersuche kann darauf aufsetzen, ohne dass danach noch etwas entschieden
werden müsste — und genau darum geht es bei einer Vorregistrierung. Es wurde
nichts am Handel geändert: keine Order, kein Parameter, keine Kursdatei. Zwei
Dinge bleiben offen und sind bewusst nicht hier erledigt: das Auswertungsskript
rechnet noch nach dem alten Verfahren (das ist die nächste Aufgabe, TB-30b),
und die Bots überspringen von sich aus Wertpapiere mit sehr kurzer Historie —
auch das muss dort angeglichen werden.
