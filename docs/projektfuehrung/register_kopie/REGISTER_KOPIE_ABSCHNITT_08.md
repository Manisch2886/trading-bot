# REGISTER-KOPIE Abschnitt 8 (von 0–56) — Register-Z. 876–930 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 8. Die Beurteilung — und die Regel, dass alles berichtet wird

Berichtet wird je Bot, unabhängig davon, ob er bleibt oder geht:

| Kennzahl | Quelle |
|---|---|
| Netto-Sharpe, Median über die Selektionsfalten | Selektionsstatistik |
| Netto-Sharpe je Falte | Rohergebnisse |
| Netto-Calmar über die Selektionsfalten | Tagesreihe des Gewinners |
| Mittelwert der **drei tiefsten** Falten-Drawdowns | Rohergebnisse |
| Kapital-Drawdown je Falte | Rohergebnisse |
| Falten ohne Trade | Rohergebnisse |
| Alpha (p. a.) und Beta gegen das point-in-time-Universum | Beta-Bereinigung |
| Rendite, Drawdown und Calmar der **konstanten Exposure** | Beta-Bereinigung |
| **Zufalls-Timing:** 95. Perzentil bei gleicher Zeit im Markt | siehe unten |
| Markierungen: Spitze, Kante, nicht zulässig, ohne Limitachse | Plateau-Regel |
| Verletzungen des Risikoappetits (−30 % je Falte) | Festlegung 6 |
| N_eff, N_nominal, 2 × N_nominal und die drei DSR-Werte | N-Buchführung |
| Bestätigungsperiode: Sharpe, Rendite, Drawdown, Trades | zuletzt |

> ⭐ **8, Tabelle PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, nachgetragen nach Fable 01a R61 (b), TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **8, Tabelle ERGÄNZT durch R55 (49.3)** (Fable 30a R55, nachgetragen nach Fable 01a R61 (b), TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Die Regel: alle werden berichtet, auch die unangenehmen.** Sie steht auf
der Sperrliste. `auswertung.py` hat keinen Schalter, der eine Zeile
unterdrückt.

### 8.1 Der Zufalls-Timing-Test

Die Exposure-Reihe des Parametersatzes wird **zyklisch verschoben** und auf
die Benchmark-Tagesrenditen gelegt: Zeit im Markt, Exposure-Verteilung und
Zahl der Positionstage bleiben Balken für Balken erhalten, allein die **Lage**
ändert sich. Gerechnet werden **alle** nichttrivialen Verschiebungen — kein
Ziehen, kein Startwert, keine Wahl. Berichtet wird das **95. Perzentil** der
so erzeugten Renditen gegen die Rendite des Satzes.

Damit ist das Kriterium, das das Übergabeprotokoll für den Prüftermin des
Elliott-Aktien-Bots vorgemerkt hat (*„gleiche Zeit im Markt gegen das
95. Perzentil von Zufalls-Timing"*, Abschnitt 9 Punkt 4), erstmals als Code
vorhanden — hier als **berichtete Zeile**, nicht als Tor. Ein Tor wäre eine
dreizehnte Festlegung, und die hat niemand getroffen.

*Eigenschaft, die man kennen muss:* bei **konstanter** Exposure liefert jede
Verschiebung denselben Wert, und das Perzentil ist keine Verteilung mehr. Der
Test trägt also nur, wo die Exposure über die Zeit schwankt — bei allen neun
Bots tut sie das.

> ⭐ **8.1 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (g), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

