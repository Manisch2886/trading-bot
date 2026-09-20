# Journal-Nachtrag (l) — 20.09.2026, TB-73: die MtM-Wirkung ist gemessen, berichtet und nicht bewertet

**Quelle:** Mac-Sitzung **TB-73 MtM-Wirkung**, 20.09.2026, ab ca. 21:35
Ortszeit, Ausgang `537ca51` (= `origin/main` beim Start), Interpreter
`trading-env/bin/python3` 3.9.6. Commits `1b6cde7` (Schritt 0,
Betreiber-Dateien), `5e9ef2b` (Schritt 1, Grundlage und Kern), `732440c`
(Schritt 2, Proben), `5e4dd95` und `f27b6c0` (Schritt 3, Messung und Bericht),
`01da585` (Schritt 4, Register 24.6), dann Schritt 5 (dieser Nachtrag, Backlog
`K4m`, Ergebnisdokument `docs/ERGEBNIS_TB-73_mtm_wirkung.md`). **Einzuarbeiten
als nächster Block nach dem höchsten vorhandenen** (am 20.09.2026 gemessen:
`BT`; `(20g)` bis `(20k)` liegen davor — die Nummer vergibt die einarbeitende
Sitzung).

⭐ **Quellenzeile für den Block, wörtlich zu übernehmen:**

```
*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20l.md`*
```

---

## Was der Auftrag wollte und was er bekam

Register 24.3 stand seit TB-71: *„die Grösse der Abweichung zur
ereignisindizierten Kurve wird gemessen und berichtet und ist für die
Entscheidung ohne Belang."* Der Auftrag wollte die Zahl — je Bot, je Falte,
2020 und 2022 hervorgehoben — als Forschungsskript ausserhalb des Laufcodes,
mit zwei Proben vorweg und ohne Empfehlung am Ende.

**Bekommen hat er die Zahl für 64 Falten** (`research/mtm_drawdown/`): in 59
davon ist der tägliche Mark-to-Market-Drawdown tiefer als der
ereignisindizierte, Median der Differenzen je Bot −1,39 bis −3,09 pp. **Und
drei Tatsachen, die der Auftrag anders erwartete:** 2020 ist bei keinem
Krypto-Bot messbar; in fünf Falten ist M flacher als E, und der Pfad ist
trotzdem richtig; die drei Exposure-Stufen gehören dem Benchmark, nicht dem
Bot. Register 24.6 trägt alles als Tatsachennotiz (124/0). Keine Empfehlung,
keine Abwägung — auch nicht als *„Offen"*-Zeile, die eine Entscheidung
vorlegt.

---

## Vier Befunde

### 1. ⭐ Eine Richtungsaussage über zwei Masse ist erst ein Satz, wenn sie von Hand widerlegt werden kann

Der Auftrag (und der Kopf von Register 24) sagt: *„der tägliche Drawdown ist
nie flacher als der ereignisweise"* — und macht daraus eine Prüfregel: *„Findest
du einen Fall, in dem doch, ist der Pfad falsch."* Bevor die Messung lief, hat
die Sitzung versucht, den Satz **von Hand zu widerlegen**, und es ging in fünf
Zeilen (Probe 3): eine Position mit +20 % unrealisiert im Buch, eine zweite
schliesst mit −10 % — E fällt −1,00 %, M nur −0,98 %. Die Ereigniskurve bewertet
offene Positionen zum Einstand; das lässt sie unrealisierte Verluste **und**
unrealisierte Gewinne nicht sehen. Welche Richtung die Abweichung nimmt, hängt
davon ab, was am Tiefpunkt im Buch liegt.

Die Messung fand dann **fünf** solche Falten, darunter `elliott_wave_stocks`
2020 mit +3,90 pp: am E-Tief (13.05.2020) tragen sechs März-Einstiege +2 055
unrealisiert (CRWD +98 %), die E erst im Juli/August sieht. Hätte die Sitzung
die Prüfregel wörtlich genommen, hätte sie den Pfad „repariert" — und einen
Pfad gebaut, der unrealisierte Gewinne ignoriert und kein Mark-to-Market mehr
ist.

⭐ **Regel:** *Bevor eine Richtungsaussage über zwei Masse zur Prüfregel wird
(„A nie kleiner als B, sonst Fehler"), wird versucht, sie an einem
Handbeispiel zu widerlegen. Gelingt das, ist sie eine Näherung, und die
Prüfung lautet: jeden Gegenfall zerlegen und seinen Grund benennen — nicht den
Pfad an die Aussage anpassen.*

### 2. ⭐ „Die Grundlage liegt vor" ist eine Behauptung über einen Datenstand — und der hat ein Datum

Die TB-24-Trade-Listen entstanden am 13.09.2026. Zwei Tage später hat TB-34 die
Krypto-Kursdateien von rund fünf Jahren auf die volle Historie (2017/2018)
neu aufgebaut. Der Auftrag vom 20.09. sagte *„Die Grundlage liegt vor"* und
verlangte 2020 hervorgehoben — für fünf Bots, deren Listen 2021-09 bis 2022-03
beginnen. Schritt 1 hat das gemessen, bevor gebaut wurde, und die Falten
2018–2020 Krypto tragen keine Zahl statt einer erfundenen. Neue Listen wären ein
neuer Backtest, nicht die TB-24-Grundlage; der Auftrag hatte dafür die
richtige Zeile (*„miss nicht drumherum"*).

⭐ **Regel:** *Wer eine frühere Messung als Grundlage nennt, nennt ihren
Datenstand mit Datum — und prüft, ob sich der Bestand seither geändert hat
(hier: `research/kursdaten_neuaufbau/BERICHT.md`). Eine Liste, die älter ist als
der Datenbestand, deckt nicht, was der Bestand heute deckt.*

### 3. ⭐ Ein Argument, das dem Benchmark gehört, wird nicht auf den Bot übertragen

*„Bei 25 / 50 / 100 % Exposure"* ist die Form, in der das Register den
Benchmark tabelliert (`DD_Benchmark(f, e)`); der Auftrag hat die Form auf den
Bot übertragen. Ein Bot hat je Falte **eine** Exposure — sie folgt aus seinen
Positionen, und sie steht jetzt neben jeder Falte (0,04 bei `elliott_wave`
bis 0,86 bei `turtle_soup_stocks`). Sie auf drei Stufen zu setzen hiesse andere
Positionen (der Auftrag selbst verbietet das: *„sonst misst du zwei
verschiedene Bots"*) oder Hebel. Ebenso ist der *„Median über die
Selektionsfalten, der zur `DD_Toleranz` führt"* der Median der
**Benchmark**-Drawdowns (Festlegung 5), nicht der Bot-Drawdowns.

⭐ **Regel:** *Bevor eine Tabellenform aus dem Register auf ein anderes Objekt
angewendet wird, wird gefragt, wessen Argument die Spalte ist. Eine Spalte, die
beim Benchmark ein Regler ist, ist beim Bot ein Ergebnis — und ein Ergebnis
setzt man nicht.*

### 4. Der Raster-Effekt: E hat Zwischenstände, die gesäter Zufall ordnet

Probe 1 verlangte *„E = M, wenn alle Positionen am Tag schliessen"*. Exakt
gilt das nur mit höchstens einem Ausstieg je Tag. Bei mehreren Ausstiegen zum
selben Zeitstempel sieht E den Stand nach jedem einzelnen — und die Reihenfolge
legt `shared/zuteilung.py::ausstiegsreihenfolge` per gesätem Zufall fest
(Modulkopf: *„entscheidet … über die Zwischenstände der Kapitalkurve und damit
über den gemessenen Drawdown"*). Ein Tagesraster hat diese Zwischenstände
nicht. Gemessen ist der Effekt klein (höchstens 0,96 pp, `volatility_breakout`
2020), aber er ist da; deshalb steht E_tag in allen Tabellen zwischen E und M,
und die Abweichung E gegen M zerfällt lesbar in Raster und Bewertung.

---

## Was der Auftrag anders sah — und wo die Messung galt

| Auftrag | gemessen / getan |
|---|---|
| Schritt 3: E gegen M *„bei 25 / 50 / 100 % Exposure"* | bei der tatsächlichen Exposure der Positionen, je Falte daneben (Befund 3) |
| Schritt 3: Bot-Median *„führt zur `DD_Toleranz`"* | berichtet als Beschreibung; `DD_Toleranz` kommt vom Benchmark |
| Schritt 3: *„M nie flacher … sonst Pfad falsch"* | fünf Fälle, jeder zerlegt, Pfad richtig (Befund 1) |
| Schritt 2, Probe 1: *„gleich"* | 1a gleich; 1b E_tag = M, E tiefer (Befund 4) |
| Abschnitt 1: *„Grundlage liegt vor"* | Krypto nicht vor 2021-09 / 2022-03; 2020 Krypto nicht messbar (Befund 2) |
| *„sechs Commits"* | sieben plus Abgabe; der Bericht des Forschungsordners war ein eigener Teil |

---

## Offen

| | wer |
|---|---|
| Krypto-Falten 2018–2020 ohne Grundlage — neue Listen wären ein neuer Backtest auf heutigen Daten; **nicht vorgelegt**, weil nach 24.3 keine Zahl hier etwas entscheidet | Betreiber |
| Dieser Nachtrag ins Journal (Block nach dem höchsten vorhandenen) | nächste Einarbeitung / TB-64-Wächter |
| Projektablage nachziehen (`K4e`): `AKTUELLER_AUFTRAG.md` (TB-73-Zeile auf „erledigt") | steuernder Chat / Betreiber |
| `K4j` unverändert; die Zahl aus TB-73 ist für keine der drei Code-Stellen ein Argument (24.3) | TB-30b |
