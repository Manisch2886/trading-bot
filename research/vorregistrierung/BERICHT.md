# TB-30a — Vorregistrierung: Bericht

**Stand: 14.09.2026.** Dieser Ordner enthält die **Vorarbeit** zur
Neuselektion: das eingefrorene Auswertungsskript, die Vorab-Berechnungen und
die Wachen. Das Register selbst steht in
[`docs/VORREGISTRIERUNG_neuselektion.md`](../../docs/VORREGISTRIERUNG_neuselektion.md).

> **Kein Selektionslauf.** Kein Raster gerechnet, kein Parametersatz
> bewertet, kein Ergebnis erzeugt. Was unter `ergebnisse/` liegt, ist
> ausschliesslich aus Kursdaten, Universumsdateien und der Kostenkonvention
> gerechnet — nichts davon kommt aus einem Bot.

---

## 1. Was hier liegt

| Datei | Rolle |
|---|---|
| `messgroessen.py` | misst die Grössen, auf denen jede Rastergrenze ruht (σ, 20-Balken-Spanne, ATR, RSI- und ADX-Quantile, Haltedauern, Datenbereiche) |
| `registerdaten.py` | **die eingefrorenen Festlegungen als Datenstruktur** — Raster, Grenzsätze, Konstanten. Keine Grenze ist eine Zahl, jede ist eine Regel |
| `faltenplan.py` | Walk-Forward-Plan: verankert, expandierend, Purge und Embargo, Zweijahres-Falten, Krypto-Platzhalter |
| `benchmark.py` | Benchmark-Drawdowns je Falte über die ganze Exposure-Achse, `DD_Toleranz`, die Drawdown-Bedingung selbst |
| `kennzahlen.py` | Sharpe, Calmar, Alpha/Beta, Zufalls-Timing, DSR, Clustering — ohne `scipy` |
| **`auswertung.py`** | **das eingefrorene Auswertungsskript** |
| `beispieldaten.py` | erzeugt Rohergebnisse mit frei erfundenen Werten |
| `pruefe_grenzsaetze.py` | vier Wachen über die Rastergrenzen |
| `registerbericht.py` | erzeugt den Zahlenteil des Registers; `--pruefen` meldet ein veraltetes Register |
| `herkunft.py` | Commit-, Datenstand- und Register-Hash, append-only-Protokoll, Stand der Verankerung |
| `test_vorregistrierung.py` | 150 Prüfungen, davon acht Mutationsproben |
| `ergebnisse/` | die Vorab-Berechnungen |

---

## 2. Die Antwort zuerst: der Vollständigkeitstest

**Ja — das Auswertungsskript liess sich fertig schreiben, ohne ein Ergebnis
gesehen zu haben.** Es läuft gegen erzeugte Beispieldaten, und jede Regel ist
einzeln am Ablauf geprüft.

Fertigschreiben hiess allerdings an **sieben** Stellen: eine Lesart
festlegen, wo die zwölf Festlegungen zwei zuliessen. Alle sieben stehen im
Register, Abschnitt 12, mit ihrer Begründung. Die wichtigste ist die erste:

> Festlegung 4 macht den Benchmark-Drawdown **exposure-abhängig** (es gilt
> die mittlere Exposure des jeweiligen Parametersatzes). Festlegung 5
> definiert `DD_Toleranz` als **Median dieser Drawdowns**. Ein Median
> exposure-abhängiger Grössen ist selbst exposure-abhängig — also trägt
> `DD_Toleranz` dasselbe Argument. Das ist keine zusätzliche Entscheidung,
> sondern die einzige Lesart, in der beide Festlegungen zusammenpassen.

Damit ist auch die zweite Frage der Übergabe beantwortet.

---

## 3. Ist die Drawdown-Bedingung in 2020 und 2022 erfüllbar?

**Ja, und mit Abstand.** Bei 50 % Exposure (Werte aus
`ergebnisse/benchmark_drawdowns.json`):

| Falte | `DD_Benchmark` | `1,25 ×` | `DD_Toleranz` | **erlaubt** | wer bindet |
|---|---:|---:|---:|---:|---|
| 2019 | −3,69 % | −4,61 % | −4,33 % | **−4,61 %** | relativ |
| **2020** | −18,93 % | **−23,66 %** | −4,33 % | **−23,66 %** | relativ |
| 2021 | −2,38 % | −2,98 % | −4,33 % | **−4,33 %** | **`DD_Toleranz`** |
| **2022** | −10,09 % | **−12,61 %** | −4,33 % | **−12,61 %** | relativ |
| 2023 | −4,33 % | −5,41 % | −4,33 % | **−5,41 %** | relativ |
| 2024 | −3,47 % | −4,34 % | −4,33 % | **−4,34 %** | relativ (knapp) |
| 2025 | −8,89 % | −11,11 % | −4,33 % | **−11,11 %** | relativ |

**Die Krisenfalten sind die grosszügigsten des ganzen Plans.** Die Bedingung
bindet dort, wo sie soll — in den ruhigen Jahren —, und auch dort erst
oberhalb der Rauschgrenze, weil `DD_Toleranz` 2021 die relative Grenze
ablöst. Das ist genau die Lücke, die Festlegung 5 schliessen sollte: ohne sie
läge die Grenze 2021 bei −2,98 %, und drei schlechte Tage entschieden über
die Zulässigkeit.

---

## 4. Was die Wachen gefunden haben

**Beim Schreiben des Registers hat `pruefe_grenzsaetze.py` angeschlagen.** Der
Satz zur Obergrenze der T3-Längen enthielt „20-Balken-Spanne", und
`t3_supertrend` führt `ADX_THRESHOLD = 20.0`. Der Satz ist umformuliert
(„Zwanzig-Balken-Spanne"); die Ziffer steht seither in keinem Grenzsatz mehr.

Die Übereinstimmung war unschuldig — und genau deshalb ein guter Beleg: eine
Wache, die nur bei Absicht anschlägt, prüft nichts.

**Die zweite Wache aus TB-29 war falsch gebaut.**
`research/versuchsregister/test_versuchsregister.py` prüfte, dass `git
status` nichts ausserhalb von `research/` und `docs/` meldet. Das prüft nicht
TB-29, sondern den **Arbeitsbaum** — und der enthält alles, woran gerade
sonst gearbeitet wird. TB-30a ändert beauftragt `shared/`, und die Wache
meldete das als Verstoss von TB-29.

Sie ist jetzt auf das umgestellt, was TB-29 tatsächlich zugesichert hat: *ein
Lauf der Untersuchung verändert nichts.* Der Arbeitsbaum wird vor und nach
einem Lauf aufgenommen, dazwischen läuft die Erhebung in allen Betriebsarten;
dazu prüft ein Syntaxbaum-Durchgang, dass die Untersuchung nur in
Wegwerf-Verzeichnisse schreibt. Beide Hälften können rot werden — nachgewiesen
an einer eingefügten Schreibzeile.

---

## 5. Die Zahlen der Vorarbeit

| | |
|---|---:|
| Rasterzellen dieses Laufs, über neun Bots | **2 416** |
| N historisch (Versuchsregister, 13.09.2026) | 653 |
| N nominal | **3 069** |
| Bots mit Zweijahres-Falten | **1** (`elliott_wave`, 26,0 Trades/Jahr) |
| Selektionsfalten je Aktien-Bot | 7 (2019–2025) |
| Bestätigungsperiode | 2026-01-01 bis 2026-09-01, **wächst** |
| Krypto-Faltenpläne | **Platzhalter mit Regel** (TB-31) |
| Prüfungen in `test_vorregistrierung.py` | **150** |
| Prüfungen in `pruefe_grenzsaetze.py` | **395** |

---

## 6. Wie man es benutzt

```bash
# Vorab-Berechnungen erneuern (nur nötig, wenn sich data/ ändert)
python3 research/vorregistrierung/messgroessen.py
python3 research/vorregistrierung/faltenplan.py
python3 research/vorregistrierung/benchmark.py

# Die Wachen
python3 research/vorregistrierung/pruefe_grenzsaetze.py
python3 research/vorregistrierung/registerbericht.py --pruefen
python3 research/vorregistrierung/herkunft.py

# Der Selbsttest
python3 research/vorregistrierung/test_vorregistrierung.py

# Beispieldaten erzeugen und auswerten (kein echter Lauf)
python3 research/vorregistrierung/beispieldaten.py --ziel /tmp/roh
python3 research/vorregistrierung/auswertung.py --rohergebnisse /tmp/roh
```

**`auswertung.py` hat keinen Schalter, der eine Schwelle verschiebt, einen
Bot ausnimmt oder eine Kennzahl unterdrückt.** Das ist Absicht und der
eigentliche Gegenstand dieser Aufgabe.

---

## 7. Was hier NICHT passiert ist

* Kein Selektionslauf, kein Rasterergebnis.
* Keine Änderung an `live_params.py`, `forward_test.py`,
  `equity_simulation.py`, `multi_symbol_optimise.py`,
  `multi_symbol_walk_forward.py` — das ist TB-30b.
* `shared/zuteilung.py` und `shared/messkette.py` unberührt.
* Keine `results/*.csv` überschrieben.
* Nichts unter `broker/`, keine Crontab, keine launchd-Vorlage.
