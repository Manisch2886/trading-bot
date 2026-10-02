# REGISTER-KOPIE Abschnitt 9 (von 0–52) — Register-Z. 925–964 — Commit ad351d5f0351d8a25479547edb96a32dd6cf3bd5 — 2026-10-02 — Original sha256 a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece — KOPIE, nicht das Register

## 9. Die DSR-Buchführung

**N = 653 plus die Zellen dieses Laufs, je Bot getrennt.** Die 653 stehen in
`research/versuchsregister/REGISTER.md` (Stand 13.09.2026, Spalte
„verschiedene Kombinationen"); die Aufteilung je Bot steht in
`registerdaten.N_HISTORISCH_JE_BOT` und summiert sich auf 653.

> ⭐ **Abschnitt 9 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (b), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Drei Werte werden berichtet:**

| | woraus |
|---|---|
| bei **N_eff** | `N_historisch` + Zahl der Cluster dieses Laufs bei Korrelation **0,9** |
| bei **N_nominal** | `N_historisch` + alle Zellen dieses Laufs |
| bei **2 × N_nominal** | das Doppelte — **als Sicherheitsabstand gekennzeichnet, nicht als Wissen** |

Der dritte Wert trägt in der Ausgabe einen Satz, der genau das sagt: *„Der
Wert bei 2 × N_nominal ist ein Sicherheitsabstand, kein Wissen: er behauptet
nicht, dass doppelt so viele Versuche stattgefunden hätten."*

**Das Clustering** läuft über die Korrelation der **Falten-Sharpe-Vektoren**
zweier Zellen, transitiv fortgesetzt (Einfachverkettung). Zellen ohne
Streuung über die Falten haben keine definierte Korrelation; sie bilden
**einen** gemeinsamen Cluster — sie sind ununterscheidbar, und jede einzeln
zu zählen bliese N_eff genau in die falsche Richtung auf. Geclustert werden
nur die Zellen **dieses** Laufs; für die 653 historischen liegen keine
Falten-Vektoren vor, sie gehen ungeclustert ein.

**Die DSR ist Bericht, nicht Tor** (Festlegung 11). Sie erscheint in der
Ausgabe mit genau diesem Zusatz, und keines der vier Abbruchkriterien liest
sie.

Gerechnet wird nach Bailey/López de Prado, ohne `scipy` (das fehlt in der
Umgebung des Nutzers): Normalverteilung über `math.erf`, ihre Umkehrung nach
Acklam.

---

