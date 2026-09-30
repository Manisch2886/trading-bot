# FABLE_ANFRAGE 2026-09-30a — drei vorgeprüfte Verfahrensfragen vor E-2 (Vorlauf 4a (i), Aggregation 2a/7 (c)/8.1, 7 (d) leere Menge) — an: Fable 5.1, bestehender Chat

*Fassung 2, 30.09.2026, steuernder Chat (eröffnet 29.09., ca. 20:55, Umzug vor E-2). Stand Repo: HEAD `0034960`. Das ist die erste Anfrage nach dem Fable-Filter (ARBEITSWEISE 22.11 in Vorbereitung, Wortlaut `UEBERGABE.md`, Nachtrag 29.09.2026, 13:20). Vorgeprüft haben zwei Helfer unabhängig voneinander Register und Code, nur lesend. Die Anfrage bezieht sich auf 27c und 29b und wiederholt sie nicht.*

⛔ **Sichtschutz 27.1:** Die Anfrage enthält keine Ergebnisgrössen des Selektionsraums. Die Zahlen darin sind Registerwerte, Codekonstanten oder Faltenjahre (Verfahrensmessung nach 27.2). Vor dem Übergeben hat ein Helfer sie gegengelesen (Fassung 1 → 2, Protokoll unten).

**Antwortform (22.11 Nr. 3):** je Frage „einverstanden“ oder „anders, weil …“. Registertext nur als R-Block, Nummern ab **R53**.

REG = `docs/VORREGISTRIERUNG_neuselektion.md`, AW = `research/vorregistrierung/auswertung.py`, KZ = `research/vorregistrierung/kennzahlen.py`.

---

## Teil 0. Kenntnis (je eine Zeile, keine Antwort nötig)

1. **Vormessungen zu 27c/29b sind gemacht** (`docs/projektfuehrung/VORMESSUNG_E-2_2026-09-29.md`):
   - Es passen R25 (Zusatz in AW Z. 53–62 als „Selektionsmodus“), R33 (`n_trades`), R36 (`mtm_kern.py`) und R48 (i).
   - R26 passt in der Sache, die Fundstelle ist aber TB-117 E (`852f253`, rc 0), nicht J-7.
   - R28: Die Probe fehlt, also greift dein Nein-Fall (Handwerk).
   - R41: 11,21 ist eine Zeitstempeldifferenz, also greift dein Abweichungsfall.
   - Diese Punkte gehen mit Tatsachennotiz in E-2.
2. **R48 (f)** geht ohne Frage in E-2. Die Kante richtet sich nach der Position (Grenzsätze REG:342 und REG:350, deine Begründung 29b:136 „denn sie stehen als Stufen der Achse“). „Eingeschlossen“ lesen wir als „zählt als Stufe mit“.
3. **TB-122 F3, F4 und die Bauart des Laders** sind Handwerk bzw. schon im Register beantwortet (F4: Punkt 11 „und der Repo-Commit“, 5e, 37.1). Sie gehen nicht an dich.
   - **F1** (Scanbeginn der Breakout-Bots an `WARMUP_PERIOD`) ist als Behebung Handwerk mit Betreiberfreigabe. Er spielt aber in Frage 1 hinein und steht dort.

---

## Teil 1. Fragen

### Frage 1 — 4a (i): Welcher Indikator-Vorlauf gilt, wenn er achsenabhängig ist?

**Register:**
- 4a (i), REG:4463: „am 1. Januar der Indikator-Vorlauf erfüllt ist“.
- Präzisierung, REG:5087: „gegen den Horizontbeginn des Bots gerechnet, nicht gegen den ersten Kurs im Bestand“.
- 2.7, REG:215: „Ein Raster je Bot, identisch über alle Falten“.
- Die Vorlauftabelle zu 3a (REG:1508–1535; die Zahlen darin nachrichtlich für Lesart B) regelt die Symbolzahl, nicht 4a.
- **Gegenstelle:** Das Register hat 4a (i) schon mit dem **festen** Vorlauf der Voreinstellung nachgemessen. REG:4447–4451 („150 Tagesbalken Vorlauf am 1. Januar 2018 brauchen Daten ab August 2017 …“), ebenso REG:1599 und REG:6014.

**Was offen ist:** Seit Posten 3 (TB-122) hängt der Vorlauf bei sechs Bots an einer Rasterachse. `research/faltenplan_neun/faltenplan_neun.py` führt je Bot eine feste Zahl, nämlich den Vorlauf der Voreinstellung. Die Zelle mit der grössten Stufe braucht mehr:

| Bot | Faltenplan heute | grösste Stufe | Fundstelle Stufe |
|---|---|---|---|
| `rsi2_crypto` | 150 (Z. 186) | 365 | REG:258 |
| `volatility_breakout_crypto` | 127 (Z. 198) | 365 | REG:265 |
| `rsi2_mean_reversion` | 200 (Z. 210) | 252 | REG:273 |
| `volatility_breakout` | 127 (Z. 221) | 252 | REG:280 |
| `turtle_soup_crypto` | 30 (Z. 192) | `donchian_period` 42 ⇒ 62 | REG:262 |
| `turtle_soup_stocks` | 30 (Z. 215) | `donchian_period` 26 ⇒ 46 | REG:275–277 |

- Bei `rsi2_crypto` besteht die Lage schon im registrierten Plan (150 gegen eine Achse bis 365, REG:258 und REG:1523).
- **Breakout-Bots:**
  - Ihr Scanbeginn hängt noch an `WARMUP_PERIOD` = 126 (`backtest_breakout.py:155` bzw. `:114`, TB-122 F1).
  - Der Vorlauf der Indikatoren hängt dagegen an der Achse: `indicators.py:39` `rolling(window=lookback_days)` ohne `min_periods`, dazu das Bollinger-Fenster 20.
  - Für die grösste Stufe sind es also etwa 272 bzw. 385 Balken.
- Welcher Wert für 4a (i) gilt, regelt keine Stelle.

**Folge, Verfahrensmessung** (erschlossen aus den Warm-ab-Daten REG:5544–5548, nicht neu gerechnet; die Zuordnung der fünf Krypto-Daten in REG:5544 folgt der Reihenfolge der Tabelle):
- Nur bei `volatility_breakout_crypto` verschiebt der grösste Vorlauf die erste Falte, nämlich von 2018 auf 2019.
- Bei den anderen fünf Bots bleibt das Jahr gleich.

**Neigung:** Es gilt ein Vorlauf je Bot, und zwar der Vorlauf der Zelle mit der grössten Stufe.
- Nur so ist jede Zelle am 1. Januar angelaufen. Mit der Voreinstellung wären Zellen mit langem Rückblick in der ersten Falte planmässig verkürzt, und 2.7 wäre nur formal erfüllt.
- Die Nachmessung REG:4447–4451 stammt aus der Zeit vor Posten 3 und trüge dann eine Tatsachennotiz.

### Frage 2 — 2a, 7 (c), 8.1: Wie werden Tagesrenditen über mehrere Tage zusammengefasst?

**Register:**
- 2a, REG:1364: „Die Falten-Rendite ist die Summe der täglichen Netto-Mark-to-Market-Renditen dieser Tage.“ Das ist die einzige Aggregationsregel für Renditen; REG:4043 und REG:4091 zitieren sie nur.
- 7 (c), REG:767: „Verglichen wird Calmar gegen Calmar.“ Eine Rechenart für die Rendite über die Selektionsfalten nennt die Stelle nicht.
- 8.1, REG:821–828: „Berichtet wird das 95. Perzentil der so erzeugten Renditen gegen die Rendite des Satzes“, ebenfalls ohne Rechenart.
- „verkettet“, „Produkt“ oder „kumuliert“ für Renditen findet sich nicht. REG:863 „Einfachverkettung“ betrifft Cluster, REG:4174 einen verworfenen Drawdown-Begriff.
- **Stützend:**
  - Der Kapital-Drawdown steht auf der MtM-Reihe des Kapitalpfads (24.2, REG:4104–4107).
  - Der Kapitalpfad beginnt mit dem registrierten Startkapital (REG:5158), und der Kapitalstand wird über die Falten mitgenommen (REG:4656–4657). Das ist eine Verkettung.
- **Dein R48 (g)**, 29b:242: „verglichen wird die Summe der täglichen Renditen (2a) der zyklisch verschobenen Exposure-Reihe …“

**Code** (KZ gehört zu `EINGEFROREN`, ist aber kein Sperrlistenpunkt, REG:6806, REG:6867):
- `gesamtrendite_pct` (KZ Z. 88–92) = `(np.prod(1 + r) - 1) * 100`, also verkettet, in Prozent.
  - Genutzt für die Rendite über die Selektionsfalten in 7 (c) (AW:530, in den Calmar AW:540) und für die konstante Exposure (KZ Z. 165).
- Das Zufalls-Timing (KZ Z. 199) rechnet ebenfalls `np.prod`. Die Seite „Rendite des Satzes“ in 8.1 kommt aus AW:530.
- Drawdowns rechnen über `cumprod` (KZ Z. 83; `benchmark.py:219`).
- Die Falten-Rendite `netto_rendite_pct` rechnet heute kein Code. Sie ist Pflichtspalte der Eingabe (AW:134) und kommt vom noch nicht gebauten Erzeuger.

**Was offen ist:**
- Wörtlich definiert 2a nur die Rendite **je Falte**, als Summe. Alles, was Code heute rechnet, verkettet. Einen Widerspruch zwischen Register und Code schafft erst R48 (g), das „Summe (2a)“ auf 8.1 überträgt.
- ⚠️ Berichtigung: Unsere Vormessung vom 29.09. hat das als direkten Widerspruch zwischen Register und Code gemeldet. Das war zu stark.

**Neigung:** überall verkettet (Produkt), auch je Falte. Das hiesse, 2a (der Satz REG:1364) und R48 (g) neu zu fassen und KZ nicht zu ändern.
- Begründung: Kapitalpfad und Drawdown sind im Register schon verkettet. Ein Calmar aus summierter Rendite über verkettetem Drawdown mischte zwei Rechenweisen.
- Falls du bei der Summe bleibst: Dann wäre KZ zu öffnen (`EINGEFROREN`), und das braucht eine eigene Freigabe.

### Frage 3 — 7 (d): Was gilt, wenn es keinen zulässigen Nicht-Spitzen-Punkt gibt?

**Register:**
- 7 (d), REG:753: „Der Gewinner ist eine Spitze und der beste Nicht-Spitzen-Punkt erfüllt (a)“.
- Präzisierung, REG:771–772: „der zulässige Nicht-Spitzen-Punkt mit dem höchsten Plateau-Mittel“.
- Zur leeren Menge sagt das Register hier nichts. In den Abschnitten 6–8 regelt nur REG:715–716 eine leere Menge („Ist `N(x)` leer, ist `x` keine Spitze“). Dein R48 (c) regelt nur den Fall „(a) nicht erfüllt“.

**Code:**
- AW:661–663: Ist `ohne_spitzen` leer, ist `bester_nicht_spitze = None`.
- Dann ergibt AW:556–558 (d) = False.
- Der Schlüssel heisst aber `d_spitze_ohne_tragfaehige_alternative` (AW:563). Dem Sinn nach spräche der Name für True, der Wortlaut der Und-Bedingung für False. Kein Test prüft den Fall.

**Nebenfall:**
- Ist keine Zelle zulässig, nimmt der Code den besten Nicht-Spitzen-Punkt aus **allen** Zellen (AW:661, `grundlage = … else tafel`). Das ist belegt. Es folgt derselben Bauart wie REG:757–759 (Plateau-Gewinner dann über alle Zellen).
- Dass das folgenlos bleibt, weil dann (b) greift, ist erschlossen.

**Neigung:** Es gilt der Wortlaut, also ist (d) nicht erfüllt, wie im Code.
- Dazu eine Tatsachennotiz, dass der Schlüsselname nicht die Regel ist. Der Gewinner bleibt nach R48 (c) ohnehin derselbe.
- Die zwei Helfer waren hier nicht einig (einer: im Wortlaut beantwortet, einer: offen). Deshalb fragen wir.

---

## Protokoll

- **Vorprüfung:** zwei Helfer, unabhängig, nur lesend, HEAD `0034960`.
  - Acht Punkte: F1, Vorlauf (jetzt Frage 1), F4, F3, Bauart Lader, R48 (g) (jetzt Frage 2), R48 (f), R48 (c) (jetzt Frage 3).
  - Einig bei sieben, uneinig bei R48 (c).
- **Gegenleser Fassung 1:** 16 Befunde (3 MUSS, 8 SOLLTE, 5 KANN), alle eingearbeitet.
  - Die MUSS-Befunde: Zeilen REG:258/1523 und REG:715–716 berichtigt; Turtle-Soup-Bots in Frage 1 ergänzt; Neigung in Frage 2 widerspruchsfrei gefasst.
