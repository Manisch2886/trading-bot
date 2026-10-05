# REGISTER-KOPIE Abschnitt 4 (von 0–54) — Register-Z. 467–587 — Commit 9b7b06065ebdae3f36f3102306c76bb844300e90 — 2026-10-05 — Original sha256 8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc — KOPIE, nicht das Register

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

> ⭐ **4.2 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **4.2 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkte (d) und (e), nachgetragen nach Fable 01a R61 (b), TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **4.2 PRÄZISIERT durch R60 (51.5)** (Fable 01a R60, TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **4.2 PRÄZISIERT durch R64 (52.2)** (Fable 02a R64, Unterpunkt (a), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

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

> ⭐ **4.4 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (c), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

