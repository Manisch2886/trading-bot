# Übergabe TB-36 — Faltenplan und Registernachtrag

**Stand: 15.09.2026.** Branch `claude/new-session-wt4193`, Base `main` bei
`6bec79c` (TB-35, PR #108) — der geforderte Commit ist enthalten, geprüft mit
`git merge-base --is-ancestor`.

---

## Die beiden Antworten zuerst

### 1. Stimmt die Krypto-Gegenprobe? — **Ja, exakt.**

Das neue Werkzeug liefert für alle fünf Krypto-Bots dieselben Zahlen wie
`research/krypto_historie/faltenplan.py --mindesttraining 0`: erste Falte
**2019**, **sieben** Selektionsfalten bei den Tagesbots und bei
`t3_supertrend`, **drei** Doppeljahr-Falten bei `elliott_wave`, Symbole je
Falte **6 / 9 / 13 / 13 / 13 / 17 / 18**, Bestätigung **23**. Auch die sechs
Symbole ohne Faltenevidenz sind dieselben.

Verglichen wird nicht die Anzahl, sondern die **Symbolliste je Falte,
namentlich**, und beide Werkzeuge laufen dafür als eigener Prozess auf
denselben Kursdateien (`test_faltenplan_neun.py`, Teil A — 24 Prüfungen).

### 2. Faltenzahl und Symbolzahl der vier Aktien-Bots

**Alle vier gleich.** Sie teilen Universum (`config/sp500_top150.txt`, 150
Symbole) und Faltenplan:

| | |
|---|---|
| Selektionsfalten | **7** — 2019, 2020, 2021, 2022, 2023, 2024, 2025 |
| Bestätigungsperiode | **2026**, bis Go-Live-Schnitt 2026-09-01 |
| Symbole je Selektionsfalte | **140 / 142 / 145 / 147 / 148 / 148 / 149** |
| Symbole Bestätigungsperiode | **150 von 150** |

Betrifft `elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks`,
`volatility_breakout`. **Kein Bot ist unterbestimmt** — der niedrigste Wert
über alle neun ist 3 (`elliott_wave`) und erreicht die Schwelle aus
Registertext 4b genau.

---

## Und: das ist kein Amendment

Es hat **kein Selektionslauf stattgefunden**, dessen Ergebnisse berührt wären —
kein Raster gerechnet, kein Parametersatz bewertet, kein Ergebnis erzeugt. Die
Sperrliste (Registerabschnitt 10) gilt laut ihrem eigenen ersten Satz erst „ab
dem signierten Tag", und der steht in Abschnitt 13 weiterhin als *offen —
Betreiber*. Es ist also nichts aufzubrechen; es wird nachgetragen, **bevor**
gerechnet wird. Genau deshalb kommt diese Arbeit vor TB-30b.

---

## Was entschieden wurde — und warum

### Ein neues Werkzeug, die beiden alten unangetastet

Die Aufgabe stellt die Frage ausdrücklich. Es gibt heute **zwei** Werkzeuge,
die Falten rechnen, und beide reichen nicht:
`research/krypto_historie/faltenplan.py` deckt nur Krypto ab,
`research/vorregistrierung/faltenplan.py` deckt alle neun ab, kennt aber keine
Symbolzahl je Falte und führt Krypto als Platzhalter. (Die Aufgabenstellung
nennt nur das erste; das zweite gibt es ebenfalls.)

Entschieden ist **neu**, in `research/faltenplan_neun/`:

1. Beide vorhandenen sind **Belege abgeschlossener Untersuchungen**. Wer sie
   umschreibt, ändert rückwirkend, womit damals gerechnet wurde — und der
   TB-31-Plan ist genau die Reihe, an der das neue Werkzeug gemessen wird.
2. Beide sprechen **Verfahren A** (`--mindesttraining`, Trainingsfenster,
   Purge zwischen Falten). Eine Erweiterung hätte beide Sprachen gleichzeitig
   tragen müssen.
3. Der Einwand „die Faltenlogik soll genau einmal existieren" ist berechtigt und
   wird **durch eine Messung** eingelöst, nicht durch ein Versprechen: Teil A
   des Selbsttests vergleicht beide Werkzeuge Falte für Falte und Symbol für
   Symbol. Laufen sie auseinander, fällt der Test. Nach TB-30b bleibt das neue
   übrig, die beiden alten sind Archiv.

Der Modulname ist bewusst `faltenplan_neun.py`: drei gleichnamige
`faltenplan.py` kollidierten in `sys.modules` — dieselbe Falle, vor der die
Aufgabenstellung bei den neun `equity_simulation.py` warnt.

**Beide Werkzeuge sind reine Standardbibliothek**, kein `pandas`, kein `numpy`.
In der Cloud-Umgebung ist `pandas` nicht installiert; ein Werkzeug, das die
Zahlen des Registers erzeugt, muss überall laufen, wo jemand sie nachrechnen
will.

### Die eine Lesart, die nötig war — und was sie kostet

Registertext 3a sagt: Symbole, „für die am 1. Januar der Falte Kursdaten
**einschliesslich Indikator-Vorlauf** vorliegen". Das lässt zwei Lesarten zu:

* **A (eingetragen):** Kursdaten liegen am 1. Januar vor; der Vorlauf speist
  sich aus der eigenen Historie des Symbols und läuft, wo er noch nicht voll
  ist, in die Falte hinein — das Symbol handelt dort ein paar Tage später und
  trägt für diese Tage 0 bei.
* **B:** Kursdaten **und** voller Vorlauf am 1. Januar, sonst zählt das Symbol
  nicht mit.

**Lesart A gilt**, und die Begründung steht im Register, nicht im Werkzeug:
3b nennt **eine** Zahlenreihe für **alle** Krypto-Tagesbots — hinge die Zahl am
Vorlauf, hätte jeder Bot seine eigene (150 / 30 / 127 Balken); der nächste Satz
von 3a lässt Symbole ohne Historie **0 beitragen** statt sie auszuschliessen;
und die Gegenprobe aus TB-31 ist die Zahlenreihe der Lesart A.

Der Preis ist gerechnet und steht **im Register neben der Zahl** (15.5): bei
fünf der neun Bots weicht Lesart B ab, am deutlichsten bei `rsi2_crypto`
(Falte 2021: 9 statt 13 Symbole, Bestätigung 20 statt 23). Ein Preis, den eine
Festlegung kostet, gehört neben die Festlegung.

---

## Das Embargo je Bot (Registertext 2d)

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

Vier Dinge, die dahinterstecken:

* **Genau ein Bot hat keine Zeitbremse: `t3_supertrend`.** Das ist die
  TB-24-Messung — seine Ausstiegsarten sind `stop_loss`, `trend_flip`,
  `t3_crossunder`, und der TB-24-Bericht nennt ausdrücklich **acht** Bots mit
  Zeitausstieg. Sein P95 ist auf denselben Positionen gerechnet wie die
  dortigen Kennzahlen; dass die Perzentilrechnung zeichengleich zu
  `pandas.Series.quantile` arbeitet, ist an den in TB-24 **veröffentlichten**
  P90-Werten aller neun Bots nachgeprüft (Teil D, gelesen statt abgeschrieben).
* **`elliott_wave_stocks` führt zwei Zeitbremsen.** 90 Tagesbalken im Backtest,
  130 **Kalendertage** im Live-Lauf. Die 130 Kalendertage sind an der Kursreihe
  nachgemessen **89** Handelstage — die 90 Balken sind die längere. Der
  Bot-Kommentar („entspricht ~90 Handelstage") trifft auf einen Tag genau.
* **„Handelstage" heisst bei Krypto Kalendertage** — der Markt läuft durch.
* **Ein gebrochenes Perzentil wird aufgerundet**, bevor die 1 dazukommt;
  abrunden machte den Rand kürzer, als die Messung ihn ausweist.

Jede Zahl wird bei jedem Lauf **aus der Bot-Datei gelesen**, mit Datei und
Zeilennummer in der Ausgabe — nicht abgeschrieben. Mutationsprobe I ändert die
Zeitbremse in einer Kopie der Bot-Datei und weist nach, dass das Embargo
mitwandert (11 → 43) und nur bei diesem einen Bot.

---

## Vier Befunde am Rande

Keiner ändert eine Zahl. Sie stehen auch im Register (15.8), damit sie beim
nächsten Lesen keine Zeit mehr kosten.

1. **„AF.2 Nr. 6" gibt es in diesem Repo nicht.** Gemeint und angewandt ist die
   Doppeljahr-Regel aus **Abschnitt 5.1 Nr. 6** samt Auswertung in **5.4**
   (Festlegung 7, Schwelle 30 Trades je Jahr). Die Regel wurde nachgelesen und
   nachgerechnet — sie kommt auf dieselbe Antwort wie 5.4: genau ein Bot,
   `elliott_wave`, mit 26,0 gefundenen Trades je vollem Kalenderjahr. Nur das
   Aktenzeichen stimmt nicht.
2. **Drei „ersetzte Fassungen" haben im Register nie gestanden** — die
   Mindestzahl 10 Trades (1c), „mindestens 4" Selektionsfalten (4b), „behält
   seine heutigen Parameter" (4c). Gesucht wurde im ganzen Register, in
   `research/vorregistrierung/` und in `docs/`. Sie stammen aus früheren
   Beratungsrunden. Die Klammerzusätze bleiben **wörtlich** stehen, weil sie
   festhalten, wogegen entschieden wurde; eingetragen sind die Texte als
   **Erstfassung**, nicht als Widerruf. Das ist als Tatsachennotiz vermerkt.
3. **`research/vorregistrierung/auswertung.py` rechnet weiterhin nach Verfahren
   A** — es liest `faltenplan.py` mit Trainingsfenstern und Purge zwischen den
   Falten und kennt für Krypto nur Platzhalter. Das ist Absicht: die Datei ist
   **eingefroren** und wurde nicht angefasst. Ihre Umstellung ist **TB-30b**.
   Wer beides verwechselt, hält das Register für widersprüchlich, obwohl es nur
   voraus ist.
4. **Die Bots überspringen kurze Historien von sich aus** (`MIN_HISTORY_DAYS`:
   1825 Tage bei den vier Aktien-Bots, 500 bei drei Krypto-Bots). Betroffen:
   `GEV`, `SNDK`, `CEG` (Aktien) und `ENSOUSDT`, `PUMPUSDT`, `ZKCUSDT`,
   `UUSDT` (Krypto). Die Symbolzahlen sagen also, wie viele Symbole Evidenz
   liefern **können**, nicht wie viele der heutige Bot-Code lädt — auch das
   gehört in TB-30b.

---

## Was im Register steht

`docs/VORREGISTRIERUNG_neuselektion.md`, **Abschnitt 15** (neu, 15.0 bis 15.9)
mit allen sechs Registertexten 0 bis 5, den Tatsachennotizen (Faltenliste je
Bot, Symbolzahl je Falte, Embargo je Bot, Universumsdateien mit SHA-256) und
den vier Befunden.

**Bestehender Text wurde nicht umgeschrieben.** Vier Stellen im alten Text
tragen einen Verweis auf Abschnitt 15: Abschnitt 3 „Der Faltenplan", 5.1
(Regeln 1, 2, 3, 5), 5.3 (Krypto-Platzhalter) und Sperrliste Nr. 8.
`git diff origin/main -- docs/VORREGISTRIERUNG_neuselektion.md` enthält **null
entfernte Zeilen**; der Selbsttest prüft das maschinell (Teil E: jede Zeile der
letzten committeten Fassung ohne Nachtrag steht unverändert und in derselben
Reihenfolge noch im Register).

---

## Testlage

**Neu:** `research/faltenplan_neun/test_faltenplan_neun.py` —
**145/145 Prüfungen**, Rückgabewert 0, Laufzeit rund eine Minute.

| Teil | Inhalt |
|---|---|
| A | Gegenprobe Krypto gegen TB-31, Falte für Falte und Symbol für Symbol |
| B | die im Register eingetragenen Tabellen gegen die Rechnung — gelesen, nicht abgeschrieben |
| C | ein Symbol ohne Historie wird nicht ausgeschlossen (am Ablauf, im Wegwerf-Universum und im echten) |
| D | Embargo mit und ohne Zeitbremse; P95 an 1…100 → 95,05; P90 aller neun Bots gegen TB-24 |
| E | Registertext vollständig, nichts gelöscht |
| F–I | vier Mutationsproben |

**Die Mutationsproben** sind gegen die zwei benannten Fallen gebaut. Gegen
*„eine Probe, deren Zustand der Test von Hand herstellt, bestätigt sich
selbst"*: keine Variable wird im laufenden Prozess umgebogen und dann dieselbe
abgefragt — jede Probe kopiert den Ordner (bei I die Bot-Datei), ändert dort
**eine** Zeile und startet das Werkzeug als **eigenen Prozess**; und jede zeigt
zuerst, dass sie ohne Mutation das Richtige sieht. Gegen *„eine zweite Wache
verdeckt das Fehlen der ersten"*: die vier Proben greifen vier verschiedene
Wachen an, und jede weist nach, dass genau ihre Zahl kippt und die anderen
stehen bleiben.

| Probe | verfälscht | zeigt sich |
|---|---|---|
| F | Registerschranke 2019 | acht der neun Pläne beginnen dann früher — und sähen mit *mehr* Falten sogar besser aus |
| G | Doppeljahr-Schwelle 30 | `elliott_wave` bekommt sieben statt drei Falten; erste Falte und Symbolzahlen bleiben richtig |
| H | Indikator-Vorlauf 150 | Lesart B fällt still mit Lesart A zusammen; die eingetragene Zahl ändert sich **nicht** |
| I | Zeitbremse in der **Bot-Datei** | Embargo 11 → 43, und nur bei diesem Bot |

**Bestehende Tests:** in der Cloud waren auf unverändertem `main`
**40 von 51** Testdateien grün; mit den TB-36-Änderungen sind es
**41 von 52** — dieselben elf roten wie vorher, plus die neue grüne Datei.
Kein Test ist durch TB-36 rot geworden.

Die elf roten sind vorbestehend und TB-36-fremd (Basislauf auf `origin/main`
zum Vergleich gefahren): `broker/test_ibkr.py`,
`dashboard/test_dashboard.py`, `dashboard/test_portfolio_sicht.py`,
`research/drawdown_reihenfolge/test_drawdown.py`,
`research/elliott_wave_params/test_params.py`,
`research/fib_score_stufen/test_stufen.py`,
`research/hrp_portfolio/test_hrp_core.py`, `shared/test_kursdaten.py`,
`shared/test_stabile_sortierung.py`, `shared/test_wellenauswahl.py` sowie
`shared/test_drawdown_beide_masse.py` (Zeitüberschreitung nach 240 s).
Ursachen: fehlende Bibliotheken (`scipy`, `ib_async`), fehlendes `node`,
fehlende Zeitzone `US/Eastern` und die im Auftrag genannten bekannten Fälle.
Auf dem Mac sollten die meisten davon grün sein — Schritt 2 des Testauftrags
prüft das.

---

## Was nicht getan wurde

* **Kein Selektionslauf**, kein Raster gerechnet.
* **Keine Parameterübernahme.** `live_params.py`, `forward_test.py` und die
  Backtest-Dateien wurden **als Text gelesen, nie importiert**.
* **Keine Kursdatei angefasst.** Datenstand unverändert
  `d9449faf51bffaaa…`, 223 Dateien; `git diff origin/main --name-only` listet
  keine Datei unter `data/`.
* **`research/vorregistrierung/auswertung.py` unberührt** (eingefroren), ebenso
  `shared/zuteilung.py`, `shared/messkette.py`, `shared/regimewache.py`,
  `shared/abrufschutz.py`, `shared/kursdaten_neuaufbau.py`,
  `shared/zeitabdeckung.py`, alles unter `broker/`, Crontab, launchd-Vorlagen
  und `results/*.csv`.

---

## Offene Punkte für TB-30b

1. **`auswertung.py` und die sechs bot-eigenen Walk-Forward-Rechner auf
   Verfahren B umstellen** — bzw. ersetzen. Der Nachtrag beschreibt, was
   gerechnet wird; der Code kann es noch nicht.
2. **`MIN_HISTORY_DAYS` angleichen**, damit „0 Trades beitragen" auch im
   Bot-Code gilt statt „Symbol wird übersprungen".
3. **Signierter Tag und Zeitanker** (Registerabschnitt 13) bleiben offen —
   Betreiber. Solange sie offen sind, ist die Sperrliste nicht scharf.

---

## In einfacher Sprache

**Was wir wissen wollten.** Bevor die grosse Parametersuche beginnt, muss
schriftlich feststehen, worauf gerechnet wird: in welche Zeitabschnitte die
Vergangenheit zerlegt wird, welche Wertpapiere in jedem Abschnitt vorkommen und
wie lange nach dem Stichtag gewartet wird, bevor die Prüfperiode anfängt. Für
die Aktien-Bots stand das noch gar nicht fest, und an vier Stellen widersprach
sich die Festlegung selbst.

**Was herauskam.** Acht der neun Bots bekommen sieben Abschnitte — die Jahre
2019 bis 2025 —, geprüft wird am Jahr 2026. Ein Bot handelt so selten, dass
seine Abschnitte doppelt so lang sein müssen; er bekommt drei, und das reicht
gerade. Bei den Kryptowährungen wächst die Zahl der handelbaren Münzen von 6 im
Jahr 2019 auf 18 im Jahr 2025, bei den Aktien von 140 auf 149 von 150. Die
Wartezeit vor der Prüfperiode liegt je nach Bot bei 11 bis 91 Tagen. Die
Kontrollrechnung gegen die frühere Untersuchung stimmt auf jedes einzelne
Symbol.

**Warum das so ist.** Eine Münze kann erst gehandelt werden, wenn es sie gibt —
Bitcoin haben wir seit 2017, manche Münzen erst seit 2025. Die Wartezeit
richtet sich danach, wie lange ein Bot eine Position höchstens hält; bei dem
einen Bot ohne feste Obergrenze haben wir gemessen, wie lange seine längsten
5 % der Positionen dauern, und einen Tag aufgeschlagen. Alle Zahlen sind aus
vorhandenen Dateien abgelesen oder nachgerechnet — geschätzt ist keine.

**Was das für dich heisst.** Der Registereintrag ist vollständig; die
Parametersuche kann darauf aufsetzen, ohne dass danach noch etwas entschieden
werden müsste, und genau darum geht es bei einer Vorregistrierung. Am Handel
hat sich nichts geändert: keine Order, kein Parameter, keine Kursdatei. Zwei
Dinge bleiben bewusst offen: das Auswertungsskript rechnet noch nach dem alten
Verfahren (das ist die nächste Aufgabe), und der signierte Tag, mit dem das
Register endgültig einfriert, braucht deinen Schlüssel.
