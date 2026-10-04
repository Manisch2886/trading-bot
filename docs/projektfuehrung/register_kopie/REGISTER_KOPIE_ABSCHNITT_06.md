# REGISTER-KOPIE Abschnitt 6 (von 0–53) — Register-Z. 744–798 — Commit ee43f5f1339549238c0da023db7c9f324b26d28e — 2026-10-04 — Original sha256 9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff — KOPIE, nicht das Register

## 6. Die Plateau-Regel

> Gewinner ist **nicht das Maximum**, sondern der Rasterpunkt, dessen
> **Nachbarschaft** (Punkte, die sich in genau **einer** Dimension um eine
> Stufe unterscheiden) den höchsten **Mittelwert** der Selektionsstatistik
> hat. Ein Punkt mehr als **50 %** über dem Nachbarschaftsmittel ist eine
> **Spitze** und wird markiert.

Zwei Lesarten mussten festgelegt werden, weil sie sonst schweigend
auseinanderlaufen:

**Das Plateau-Mittel zählt den Punkt selbst mit** — Mittelwert über
`{x} ∪ N(x)`. Der Punkt ist der Punkt, der gespielt wird; ein Punkt mit
hervorragenden Nachbarn und katastrophalem eigenem Wert darf nicht gewinnen.

**Der Spitzentest vergleicht ohne den Punkt selbst** — `M` = Mittel über
`N(x)` ohne `x`. Die Frage ist, ob der Punkt aus seiner Umgebung *herausragt*;
ein Punkt, der in seiner eigenen Vergleichsgrundlage steckt, dämpft genau
das, was gemessen werden soll. Formal:

```
x ist eine Spitze  ⟺  S(x) − M > 0,5 · |M|
```

Für `M > 0` ist das wörtlich „mehr als 50 % über dem Nachbarschaftsmittel".
Für `M ≤ 0` ist es dieselbe Bedingung, weiterhin monoton und definiert — die
Formel hat **keinen undefinierten Fall**. Ist `N(x)` leer, ist `x` keine
Spitze: aus nichts kann nichts herausragen.

**Zellen, in denen die Strategie nicht definiert ist, existieren nicht.** Bei
`t3_supertrend` sind das alle Zellen mit `t3_fast_length ≥ t3_slow_length`;
sie können weder gewinnen noch in ein Nachbarschaftsmittel eingehen. Von den
4 × 4 = 16 Längenpaaren bleiben 6, die Zellenzahl fällt entsprechend von
1.024 auf 384.

> ⭐ **Benennung dieses Zustands und unbekannter Bedingungstext (42.3 F1, Fable
> 25c, TB-108, 25.09.2026):** Ein Bot, bei dem alle Zellen existieren, hat
> „keine Rasterbedingung (Abschnitt 6)" — nicht „keine Nebenbedingung" und
> nicht „Abschnitt 4" (Abschnitt 4 ist die Drawdown-Bedingung). Ein nicht
> leerer Bedingungstext, den der Code nicht als Rasterbedingung erkennt, endet
> mit **2**, unabhängig vom Modus; gedeutet wird er an **einer** Stelle.
> Wortlaut in **42.3, F1**; die zweite Deutungsstelle (`registerdaten.py:605`)
> bleibt bis 40.8 (h). Der Absatz oben bleibt zeichengleich.

**Die Nachbarschaft ist geometrisch, nicht zulässigkeitsgefiltert.** Ein
unzulässiger Nachbar geht in das Plateau-Mittel ein, denn die Plateau-Regel
misst die *Glattheit der Fläche*, nicht die Zulässigkeit. **Gewinnen** kann
nur ein zulässiger Punkt.

**Gleichstand** wird reproduzierbar aufgelöst: erst höhere eigene Statistik,
dann der alphabetisch erste Zellenname. Ein Zufall wäre hier eine Wahl, die
in keinem N auftaucht.

---

