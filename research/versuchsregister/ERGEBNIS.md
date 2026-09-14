# TB-29 — Ergebnis in Kürze

**13.09.2026 · Erhebung, keine Änderung · kein Bot-Code angefasst**

---

## Die Zahl

**2 798 belegbare Rasterauswertungen** über die gesamte Projektgeschichte.
Konservativer, nach Abzug jeder Wiederholung derselben Kombination:
**653 verschiedene Parameter-Kombinationen**.

**Beides sind Untergrenzen.**

| Bot | Rasterauswertungen | verschiedene Kombinationen |
|---|---:|---:|
| `elliott_wave_stocks` | 1 085 | 264 |
| `elliott_wave` | 977 | 252 |
| `t3_supertrend` | 406 | 81 |
| `rsi2_crypto` | 73 | 18 |
| `turtle_soup_crypto` | 49 | 12 |
| `turtle_soup_stocks` | 49 | 12 |
| `rsi2_mean_reversion` | 25 | 6 |
| `volatility_breakout` | 17 | 4 |
| `volatility_breakout_crypto` | 17 | 4 |
| bot-übergreifend | 100 | — |
| **Gesamt** | **2 798** | **653** |

Woraus sie sich zusammensetzt: 237 aus den neun Bot-Rastern, 246 aus den neun
Walk-Forward-Läufen, 153 aus den drei älteren Einzelsymbol-Rastern, 2 162 aus
den Rasterläufen unter `research/`.

---

## Was sich **nicht** rekonstruieren liess

1. **Die Runden vor dem 02.09.2026.** Die Git-Historie beginnt mit einem
   Commit, der bereits drei fertige Bots samt Rastern und Ergebnisdateien
   enthält. Mechanisch nachgerechnet für jeden Commit: **0 Rasteränderungen**
   über alle 21 Optimierungsstellen. Die Runden liegen davor und sind in
   diesem Repo nicht sichtbar.
2. **Überschriebene Ergebnisdateien.** Jede der neun
   `multi_symbol_optimisation_results.csv` wurde **genau einmal** committet —
   beim Anlegen des Bots — und nie wieder. Spätere Läufe sind lokal
   überschrieben oder nie abgelegt worden.
3. **Ein verlorenes Werkzeug mit Namen.**
   `elliott_wave_stocks/multi_symbol_optimise.py:39` begründet eine
   verschobene Rastergrenze mit „Erkenntnis aus `compare_exit_rules.py`".
   Diese Datei hat **nie** im Repo gelegen. Die Selektion ist belegt, ihr
   Umfang nicht.
4. **Informelle Versuche von Hand**, bevor ein Raster stand — Zeitrahmen-Suche
   des T3-Bots, Universumserweiterung 25 → 50 → 100 → 150, verworfene
   503-Werte-Variante. Nicht überliefert.

---

## Drei Befunde nebenbei

* **`t3_supertrend`:** die abgelegte Ergebnisdatei (23 Zeilen) passt zum
  Bot-Zustand **ohne** BTC-Regimefilter — mit ihm bestünden 64 von 81
  Kombinationen den Mindestfilter, ohne ihn genau 23. Die Datei, die die
  Parameterwahl getragen hat, beschreibt einen Zustand, den es nicht mehr gibt.
* **Beide Elliott-Bots:** ihre Ergebnisdateien stammen aus der Zeit vor der
  Look-Ahead-Korrektur. Auf korrigierter Grundlage besteht bei `elliott_wave`
  **keine einzige** der 36 Kombinationen mehr den Mindestfilter.
* **`results/elliott_wave/` existiert nicht.** Der Bot legt seit der
  Umstellung auf `strategy_paths.py` keine Optimierungsergebnisse mehr ab;
  seine Datei liegt bis heute unter dem alten Pfad in der Wurzel von
  `results/`.

---

## Einordnung für die Deflated Sharpe Ratio

Erwartetes Maximum reinen Rauschens bei N Versuchen: **√(2 ln N)**
Standardabweichungen. Auf einen Jahres-Sharpe umgerechnet
(√(2 ln N)/√T · √252):

| N | √(2 ln N) | Schwelle bei 1 Jahr | Schwelle bei 5 Jahren |
|---:|---:|---:|---:|
| 36 | 2,677 | 2,68 | 1,20 |
| 237 | 3,307 | 3,31 | 1,48 |
| **653** | **3,600** | **3,60** | **1,61** |
| **2 798** | **3,984** | **3,98** | **1,78** |

**Nicht bewertet, nur ausgerechnet.** Zwei Vorbehalte gehören dazu: die
Näherung setzt unabhängige Versuche voraus (benachbarte Rasterpunkte sind es
nicht — die Schwelle ist eher zu hoch), und N ist eine Untergrenze (das zieht
in die Gegenrichtung).

Bemerkenswert ist der geringe Abstand zwischen den Zeilen: von N = 36 auf
N = 2 798 steigt die Fünf-Jahres-Schwelle nur von 1,20 auf 1,78. Die
Multiplizität wächst mit dem Logarithmus — **eine Grössenordnung Unsicherheit
in N verschiebt die Schwelle nur wenig.** Genau deshalb ist eine belegte
Untergrenze brauchbar, obwohl sie unvollständig ist.

---

## Was abgegeben wurde

`research/versuchsregister/` — fünf Dateien, sonst nichts:

| Datei | Inhalt |
|---|---|
| `REGISTER.md` | das Register: eine Zeile je Versuchsblock, Summen je Bot, Gesamtsumme |
| `BERICHT.md` | Methodik, Befunde, Lücken, DSR-Einordnung |
| `raster.py` | AST-Zähler für Rastergrössen — ohne `pandas`, ohne Netz |
| `versuchsregister.py` | Erhebung, Wächter (`--pruefen`), Historie, DSR |
| `test_versuchsregister.py` | 41 Zusicherungen, davon zwei Mutationsproben |

```bash
python3 research/versuchsregister/versuchsregister.py --pruefen   # RC 1 bei Befund
```

Der Wächter prüft 53 Angaben — 21 Rastergrössen, 10 Ergebnisdateien,
22 Rasterläufe — gegen die im Werkzeug hinterlegten Stände und meldet, sobald
eine wächst, ohne dass das Register nachgezogen wurde.
