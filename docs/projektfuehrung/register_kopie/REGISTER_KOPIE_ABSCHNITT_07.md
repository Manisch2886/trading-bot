# REGISTER-KOPIE Abschnitt 7 (von 0–52) — Register-Z. 799–869 — Commit ad351d5f0351d8a25479547edb96a32dd6cf3bd5 — 2026-10-02 — Original sha256 a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece — KOPIE, nicht das Register

## 7. Die Abbruchkriterien

Ein Bot bleibt **nicht**, wenn für den Plateau-Gewinner gilt:

| | |
|---|---|
| **(a)** | Falten-Median des Netto-Sharpe **≤ 0** |
| **(b)** | **Kein** Parametersatz erfüllt die Drawdown-Bedingung in allen Falten |
| **(c)** | **Beta-Bereinigung:** Netto-Alpha gegen das gleichgewichtete point-in-time-Universum **≤ 0 UND** Calmar unter dem der konstanten Exposure |
| **(d)** | Der Gewinner ist eine **Spitze** **und** der beste Nicht-Spitzen-Punkt erfüllt (a) |

> ⭐ **7 (d) PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (c), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **7 (a) ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **7 (d) ERGÄNZT durch R55 (49.3)** (Fable 30a R55, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **7 (b) PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, nachgetragen nach Fable 01a R61 (b), TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

Präzisierungen, die das eingefrorene Skript umsetzt:

* **(b) und der Gewinner.** Gewinnen kann nur ein zulässiger Punkt. Ist keiner
  zulässig, greift (b); berichtet wird dann der Plateau-Gewinner über *alle*
  Zellen, ausdrücklich mit der Markierung **„nicht zulässig"**.
* **(c), erste Hälfte.** Kleinste Quadrate auf den **Tagesrenditen** des
  Gewinners über die Selektionsfalten gegen die Tagesrenditen des
  gleichgewichteten point-in-time-Universums; `alpha` annualisiert. Beide
  Reihen werden auf gemeinsame Tage gebracht; weniger als drei gemeinsame
  Tage sind ein Abbruch, keine Annahme.
* **(c), zweite Hälfte.** „Konstante Exposure" ist die statische
  Benchmark-Position in Höhe der mittleren Exposure des Gewinners über
  dieselben Tage. Verglichen wird Calmar gegen Calmar.
* **(c) verlangt BEIDES.** Ein Satz mit `alpha ≤ 0`, aber besserem Calmar
  fällt **nicht** durch. `test_vorregistrierung.py` Teil E prüft genau diese
  Gegenprobe.
* **(d).** „Der beste Nicht-Spitzen-Punkt" ist der zulässige Nicht-Spitzen-Punkt
  mit dem höchsten Plateau-Mittel.
* **Calmar bei Drawdown 0** ist 0,0, nicht unendlich — sonst gewönne ein
  Satz, der gar nicht handelt.
* **Sharpe ohne Zinsabzug.** Eine Zinsannahme wäre eine weitere Wahl.

### 7.1 Die drei Regeln für mehrere Ausfälle — wörtlich

- ⚠️ **Die Anzahl ausscheidender Bots ist KEIN Grund, eine Schwelle zu
  ändern.**
- Das **Kapital** geht in eine **statische Benchmark-Position** in Höhe des
  mittleren Exposures — nicht in Kasse, nicht zu den Überlebenden.
- Der Bot läuft **als Schatten weiter**, kehrt nur über einen **neuen
  vorregistrierten Lauf mit veränderter Hypothese** zurück. **Kein „vorerst
  behalten".**

Alle drei stehen als Zeichenketten in
`research/vorregistrierung/auswertung.py::kapitalregel` und werden am Ende
jeder Bleibt-Geht-Liste ausgegeben — auch dann, wenn kein Bot ausscheidet.

> ⭐ **Messungen auf dem Selektionsraum nach dem Tag: siehe 45.6/45.7** (Fable
> 26a R6/R7, TB-114, 26.09.2026). Die drei Regeln und der Satz oben bleiben
> zeichengleich.

> ⭐ **7.1 ERGÄNZT durch R21 (47.4)** (Fable 27c R21, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **7.1 PRÄZISIERT durch R23 (47.6)** (Fable 27c R23, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

