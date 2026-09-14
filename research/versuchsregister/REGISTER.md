# TB-29 — Versuchsregister

**Stand: 13.09.2026.** Eine Erhebung, keine Änderung. Diese Untersuchung fasst
**keinen** Bot-Code an: alles läuft lesend auf dem Quelltext und auf abgelegten
Ergebnisdateien; es wird nichts ausgeführt, nichts importiert, nichts
überschrieben.

Fortgeschrieben wird das Register mit
`research/versuchsregister/versuchsregister.py`; der Wächter
(`--pruefen`) meldet mit Rückgabewert **1**, sobald eine Rastergrösse oder eine
Ergebnisdatei wächst, ohne dass dieses Dokument nachgezogen wurde.

---

## 0. Die Zahl zuerst

> **2 798 belegbare Rasterauswertungen.** Das ist die Summe aller
> Parameter-Kombinationen, die in diesem Projekt nachweislich gerechnet wurden
> — jede belegt durch eine abgelegte Ergebnisdatei oder durch das Raster im
> Quelltext, das den Lauf definiert.
>
> Konservativer gerechnet, nach Abzug aller Wiederholungen derselben
> Parameter-Kombination: **653 verschiedene Parameter-Kombinationen** über die
> neun Bots.
>
> **Beides sind Untergrenzen** — und zwar nicht als Floskel, sondern messbar:
> die Git-Historie beginnt am 02.09.2026 mit einem Repo, in dem alle neun
> Raster bereits fertig stehen. Alles, was vor diesem Tag probiert wurde, ist
> in keiner Datei dieses Projekts sichtbar (Abschnitt 5).

| Grösse | Zahl | woraus |
|---|---:|---|
| Rasterauswertungen insgesamt | **2 798** | Abschnitt 1–3 |
| davon einem Bot zurechenbar | 2 698 | Abschnitt 4 |
| davon bot-übergreifend | 100 | Abschnitt 3.3 |
| verschiedene Parameter-Kombinationen (dedupliziert) | **653** | Abschnitt 4.2 |
| Rasteränderungen in der Git-Historie | **0** | Abschnitt 5.1 |

---

## 1. Rastersuchen im Bot-Code

Die neun `multi_symbol_optimise.py` definieren ihre Raster hart im Code. Die
Spalte **Kombinationen** ist mechanisch aus dem Quelltext gezählt
(`raster.py`, AST — kein Ablesen von Hand), die Spalte **Zeilen** ist die
abgelegte Ergebnisdatei.

| # | Bot | Commit (Einführung) | Art | Kombinationen | Zeilen abgelegt | Beleg |
|---|---|---|---|---:|---:|---|
| 1 | `elliott_wave` | `0f6491b` 02.09. | Rastersuche 4×3×3 | 36 | 36 | `results/multi_symbol_optimisation_results.csv` |
| 2 | `elliott_wave_stocks` | `0f6491b` 02.09. | Rastersuche 4×4×(3+1) | 64 | 64 | `results/elliott_wave_stocks/…` |
| 3 | `rsi2_crypto` | `b4c174c` 03.09. | Rastersuche 3×2×3 | 18 | 6 | `results/rsi2_crypto/…` |
| 4 | `rsi2_mean_reversion` | `f56c6d2` 03.09. | Rastersuche 2×3 | 6 | 6 | `results/rsi2_mean_reversion/…` |
| 5 | `t3_supertrend` | `0f6491b` 02.09. | Rastersuche 3×3×3×3 | 81 | 23 | `results/t3_supertrend/…` |
| 6 | `turtle_soup_crypto` | `88b9050` 04.09. | Rastersuche 3×4 | 12 | 8 | `results/turtle_soup_crypto/…` |
| 7 | `turtle_soup_stocks` | `88b9050` 04.09. | Rastersuche 3×4 | 12 | 12 | `results/turtle_soup_stocks/…` |
| 8 | `volatility_breakout` | `b603861` 03.09. | Rastersuche 4 | 4 | 4 | `results/volatility_breakout/…` |
| 9 | `volatility_breakout_crypto` | `b4c174c` 03.09. | Rastersuche 4 | 4 | 4 | `results/volatility_breakout_crypto/…` |
| | **Summe** | | | **237** | **163** | |

**Wo Rastergrösse und Zeilenzahl auseinandergehen, ist das ein Befund.** Hier
gehen sie bei vier Bots auseinander, und die Ursache ist in drei Fällen
nachgerechnet, nicht vermutet:

* **`rsi2_crypto` (18 → 6), `turtle_soup_crypto` (12 → 8):** die Mindestfilter
  (`MIN_TRADES`, `MIN_SYMBOLS_CONTRIBUTING`, `MIN_AVG_RETURN_PCT`). Gerechnet
  wurden 18 bzw. 12, abgelegt nur die bestandenen. **Nachgerechnet:** in
  `research/drawdown_reihenfolge/results/rsi2_crypto_raster.csv` (18 Zeilen)
  bestehen genau 6 den Mindestfilter, in
  `turtle_soup_crypto_raster.csv` (12 Zeilen) genau 8 — dieselben Zahlen.
* **`t3_supertrend` (81 → 23):** ebenfalls der Mindestfilter, aber auf einem
  **älteren Bot-Zustand**. Mit dem heutigen BTC-Regimefilter bestehen 64 von
  81 (`t3_supertrend_raster.csv`); **ohne** ihn bestehen genau **23**
  (`t3_supertrend_ohne_regimefilter_raster.csv`). Die abgelegte Datei stammt
  also aus der Zeit vor dem Regimefilter — so steht es auch in
  `research/drawdown_reihenfolge/adapters.py`.
* **`elliott_wave` (36 → 36) und `elliott_wave_stocks` (64 → 64):** hier gehen
  die Zahlen *nicht* auseinander — und genau das ist der Befund. Beide Dateien
  stammen aus der Zeit **vor** der Look-Ahead-Korrektur (PR #26, 07.09.2026).
  Auf korrigierter Grundlage besteht bei `elliott_wave` **keine einzige** der
  36 Kombinationen mehr den Mindestfilter
  (`research/elliott_wave_lookahead/BERICHT.md`, Abschnitt „36 von 36" gegen
  „0 von 36"; unabhängig nachgezählt in
  `drawdown_reihenfolge/results/elliott_wave_raster.csv`: 0 bestanden). Bei
  `elliott_wave_stocks` bestehen heute 17 von 64.

**Runden:** jede dieser neun Dateien wurde **genau einmal** committet — beim
Anlegen des Bots — und nie wieder verändert (Abschnitt 5.1). Für jeden Bot ist
damit **eine** Runde belegt; dass es mehr waren, ist wahrscheinlich, aber
nicht belegbar.

---

## 2. Walk-Forward-Läufe

Jede `multi_symbol_walk_forward.py` optimiert das **volle Raster** auf dem
In-Sample-Fenster und prüft die Siegerkombination **einmal** out-of-sample.
Kombinationen je Lauf = Rastergrösse + 1.

| # | Bot | Art | Kombinationen | Beleg |
|---|---|---|---:|---|
| 10 | `elliott_wave` | Walk-Forward (36 IS + 1 OOS) | 37 | Code; OOS-Kennzahlen im Übergabeprotokoll 3.1 |
| 11 | `elliott_wave_stocks` | Walk-Forward (64 IS + 1 OOS) | 65 | Code; Übergabeprotokoll 3.3 (132 OOS-Trades) |
| 12 | `rsi2_crypto` | Walk-Forward (18 IS + 1 OOS) | 19 | `drawdown_reihenfolge/results/rsi2_crypto_is_raster.csv` (18 Zeilen) |
| 13 | `rsi2_mean_reversion` | Walk-Forward (6 IS + 1 OOS) | 7 | `…/rsi2_mean_reversion_is_raster.csv` (6) |
| 14 | `t3_supertrend` | Walk-Forward (81 IS + 1 OOS) | 82 | Code; Übergabeprotokoll 3.2 (301 OOS-Trades) |
| 15 | `turtle_soup_crypto` | Walk-Forward (12 IS + 1 OOS) | 13 | `…/turtle_soup_crypto_is_raster.csv` (12) |
| 16 | `turtle_soup_stocks` | Walk-Forward (12 IS + 1 OOS) | 13 | `…/turtle_soup_stocks_is_raster.csv` (12) |
| 17 | `volatility_breakout` | Walk-Forward (4 IS + 1 OOS) | 5 | `…/volatility_breakout_is_raster.csv` (4) |
| 18 | `volatility_breakout_crypto` | Walk-Forward (4 IS + 1 OOS) | 5 | `…/volatility_breakout_crypto_is_raster.csv` (4) |
| | **Summe** | | **246** | |

**Lücke, ausdrücklich benannt:** die Walk-Forward-Skripte legen **keine**
Ergebnisdatei je Kombination ab — sie geben ihr Ergebnis nur auf dem
Bildschirm aus. Für sechs der neun Bots liegt ein nachgerechnetes IS-Raster in
`research/drawdown_reihenfolge/` vor und stützt die Zahl; für die drei, die
ihr IS-Raster über `run_multi_optimisation` aus dem Nachbarmodul beziehen
(`elliott_wave`, `elliott_wave_stocks`, `t3_supertrend`), ist der Beleg der
Quelltext plus die im Übergabeprotokoll berichteten OOS-Kennzahlen.

---

## 3. Ältere und Forschungs-Raster

### 3.1 Einzelsymbol-Optimierung (die drei `optimise_*.py`)

Die Vorläufer der Multi-Symbol-Suche. Sie stehen weiterhin im Repo und
definieren eigene Raster.

| # | Bot | Datei | Art | Kombinationen | Beleg |
|---|---|---|---|---:|---|
| 19 | `elliott_wave` | `optimise_elliott.py` | Einzelsymbol-Raster 4×3×3 | 36 | `results/BTCUSDT_optimisation_results.csv` (30 Zeilen bestanden) |
| 20 | `elliott_wave_stocks` | `optimise_elliott.py` | Einzelsymbol-Raster 4×3×3 | 36 | nur Code — **keine Ergebnisdatei abgelegt** |
| 21 | `t3_supertrend` | `optimise_trend.py` | Einzelsymbol-Raster 3×3×3×3 | 81 | nur Code — **keine Ergebnisdatei abgelegt** |
| | **Summe** | | | **153** | |

### 3.2 Forschungsraster mit Bot-Bezug

| # | Ordner | Bot | Art | Kombinationen | Beleg |
|---|---|---|---|---:|---|
| 22 | `elliott_wave_params` | `elliott_wave` | Rastersuche 7×6×6 auf 3 Fenstern | 756 | `results/elliott_wave_grid_{gesamt,is,oos}.csv`, je 252 Zeilen |
| 23 | `elliott_wave_params` | `elliott_wave_stocks` | Rastersuche 7×6×6 auf 3 Fenstern | 756 | `results/elliott_wave_stocks_grid_{gesamt,is,oos}.csv`, je 252 |
| 24 | `elliott_wave_lookahead` | `elliott_wave` | Bot-Raster auf **2** Grundlagen (mit/ohne Look-Ahead) | 72 | `grid.py`; BERICHT.md Abschnitt „36 von 36" / „0 von 36" |
| 25 | `elliott_wave_lookahead` | `elliott_wave_stocks` | Bot-Raster 4×4×3 auf 2 Grundlagen | 96 | `grid.py`; BERICHT.md „48 von 48" |
| 26 | `drawdown_reihenfolge` | alle neun | volle Raster nachgerechnet, 4 Drawdown-Masse | 237 | `results/<bot>_raster.csv`, Summe 237 Zeilen |
| 27 | `drawdown_reihenfolge` | 6 Bots | IS-Raster (Walk-Forward-Fenster) | 56 | `results/<bot>_is_raster.csv` |
| 28 | `drawdown_reihenfolge` | `t3_supertrend` | volles Raster **ohne** BTC-Regimefilter | 81 | `results/t3_supertrend_ohne_regimefilter_raster.csv` |
| 29 | `fib_score_stufen` | beide Elliott-Bots | 4 Fib-Score-Stufen je Bot | 8 | `auswertung.py::STUFEN`, `results/<bot>_muster.csv` |
| | **Summe** | | | **2 062** | |

### 3.3 Forschungsraster ohne einzelnen Bot-Bezug

| # | Ordner | Art | Kombinationen | Beleg |
|---|---|---|---:|---|
| 30 | `trailing_stops` | 5 Bots × 2 ATR-Fenster × 3 Stop-Varianten | 30 | `run_all.py::ATR_WINDOWS`, `run_one_bot.py::VARIANTS`, `results/stop_inventory.json` (5 `in_scope`) |
| 31 | `vbc_deepdive` | 4 Varianten × 3 Regime-Modi × 3 Perioden | 36 | `vbc_core.py::VARIANTS`, `regime.py::REGIME_MODES`, `compare_modes.py::PERIODS` |
| 32 | `volatility_scaled_sizing` | 9 Bots × 2 Positionsgrössen-Varianten | 18 | `run_all.py::BOTS`, `summary_table.json` |
| 33 | `hrp_portfolio` | 2 Gewichtungsverfahren × 4 Kurvenfassungen | 8 | `nachtrag_vbc_regimefilter.py::BASES`, `results/quarterly_weights.csv` |
| 34 | `trend_overlay` | 2 MA-Fenster × 3 Exposure-Varianten | 6 | `run_overlay_analysis.py::PRIMARY_WINDOW / ROBUSTNESS_WINDOW / EXPOSURE_VARIANTS` |
| 35 | `datenluecke_wurzelkorrektur` | 2 Wege (Wurzelkorrektur / Cron-Verschiebung) | 2 | `BERICHT.md` |
| | **Summe** | | **100** | |

### 3.4 Ausdrücklich **nicht** mitgezählt

Diese Untersuchungen haben gerechnet, aber **keine Parameter ausgewählt** — sie
messen dieselbe Konfiguration mehrfach. Sie erhöhen die Multiplizität einer
Selektion nicht und stehen deshalb mit Begründung hier statt in der Summe.

| Ordner | Läufe | warum nicht gezählt |
|---|---:|---|
| `order_sensitivity` | 9 Bots × 500 Permutationen = 4 500 | permutiert die Trade-Reihenfolge **einer** Konfiguration |
| `determinismus` / TB-23 | 9 Bots × 20 Permutationen = 180 | prüft Reproduzierbarkeit, wählt nichts aus |
| `exposure_messung`, `tb24_haltedauern`, `pnl_2025_fixed_size` | je 9 Bots | reine Messung auf der Live-Konfiguration |
| `sync_check`, `backtest_defaults`, `forward_test_sync`, `parameter_doku`, `tb27_kapitalsimulation`, `uebersprungene_trades`, `zuteilungskaskade` | — | Code- und Konfigurationsprüfungen ohne Parameterraster |
| `oos_take_profit`, `oos_positionslimit` | je 2 (vorher/nachher) | Fehlerbehebungen, keine Parameterwahl |

---

## 4. Summen

### 4.1 Je Bot

| Bot | Rastersuche (1) | Walk-Forward (2) | Einzelsymbol (3.1) | Forschung (3.2) | **Summe** |
|---|---:|---:|---:|---:|---:|
| `elliott_wave` | 36 | 37 | 36 | 868 | **977** |
| `elliott_wave_stocks` | 64 | 65 | 36 | 920 | **1 085** |
| `rsi2_crypto` | 18 | 19 | — | 36 | **73** |
| `rsi2_mean_reversion` | 6 | 7 | — | 12 | **25** |
| `t3_supertrend` | 81 | 82 | 81 | 162 | **406** |
| `turtle_soup_crypto` | 12 | 13 | — | 24 | **49** |
| `turtle_soup_stocks` | 12 | 13 | — | 24 | **49** |
| `volatility_breakout` | 4 | 5 | — | 8 | **17** |
| `volatility_breakout_crypto` | 4 | 5 | — | 8 | **17** |
| **Summe je Bot** | 237 | 246 | 153 | 2 062 | **2 698** |
| bot-übergreifend (3.3) | | | | 100 | **100** |
| | | | | | |
| **GESAMT — Untergrenze** | | | | | **2 798** |

### 4.2 Verschiedene Parameter-Kombinationen (dedupliziert)

Die Zahl oben zählt jede Auswertung. Wer nur **verschiedene**
Parameter-Kombinationen zählen will — also jede Kombination genau einmal, egal
wie oft sie gerechnet wurde —, kommt auf:

| Bot | verschiedene Kombinationen | Herleitung |
|---|---:|---|
| `elliott_wave` | 252 | das `elliott_wave_params`-Raster 7×6×6 **enthält** das Bot-Raster (4×3×3) vollständig |
| `elliott_wave_stocks` | 264 | 252 aus `elliott_wave_params` + 12 aus `optimise_elliott.py` (Stop 4 % steht in keinem anderen Raster) |
| `t3_supertrend` | 81 | Bot-Raster und `optimise_trend.py` haben **identische** Wertebereiche |
| `rsi2_crypto` | 18 | |
| `rsi2_mean_reversion` | 6 | |
| `turtle_soup_crypto` | 12 | |
| `turtle_soup_stocks` | 12 | |
| `volatility_breakout` | 4 | |
| `volatility_breakout_crypto` | 4 | |
| **Summe** | **653** | |

Diese 653 sind die **härtere** Untergrenze: sie unterstellt, dass jede
Wiederholung derselben Kombination auf korrigiertem Code, anderem Fenster oder
anderem Universum keinen eigenen Versuch darstellt. Für die Deflated Sharpe
Ratio ist das die konservative Lesart; die Auswahl selbst ist aber jedes Mal
neu getroffen worden, weshalb 2 798 die sachlich näherliegende Zahl ist.

---

## 5. Was **nicht** rekonstruierbar ist

Dies ist kein Nachtrag, sondern der Teil des Auftrags, der ausdrücklich
benannt und **nicht geschätzt** werden sollte.

### 5.1 Die Runden vor dem 02.09.2026

Die Git-Historie beginnt mit `0f6491b` **„Initial commit" vom 02.09.2026** —
und dieser eine Commit enthält bereits drei fertige Bots samt Rastern,
Ergebnisdateien und Übergabeprotokoll. Die sechs weiteren Bots kommen in den
zwei Tagen darauf hinzu, ebenfalls je in einem Commit und je fertig.

Mechanisch nachgezählt (`versuchsregister.py --historie`, rechnet die
Rastergrösse **für jeden Commit neu** aus dem damaligen Quelltext):

> **0 Rasteränderungen über alle 21 Optimierungsstellen.** Keines der neun
> Bot-Raster, keines der sechs eigenständigen Walk-Forward-Raster und keines
> der drei Einzelsymbol-Raster hat sich seit seinem ersten Commit in der
> Grösse verändert; auch die Rastergrenzen sind unverändert.

Das heisst **nicht**, dass es nur eine Runde gab — es heisst, dass die Runden
vor dem ersten Commit stattfanden. Zwei Spuren belegen, dass es sie gab, ohne
sie zählbar zu machen:

* `strategies/elliott_wave_stocks/multi_symbol_optimise.py:39` trägt den
  Kommentar **„erweitert (bis 8 %) nach Erkenntnis aus `compare_exit_rules.py`,
  dass breitere Stops bei Aktien-Trendfolge besser abschneiden können"** — eine
  Rastergrenze, die verschoben wurde, weil ein Ergebnis dazu Anlass gab. Der
  Zustand *davor* steht in keiner Datei. **`compare_exit_rules.py` gibt es im
  Repo nicht, und es hat nie darin gelegen** (`git log --all` auf diesen
  Dateinamen: leer). Das Werkzeug, das diese Rasteränderung ausgelöst hat, ist
  verloren; wie viele Kombinationen es geprüft hat, ist damit nicht
  rekonstruierbar. **Genau das ist der Fall, den Abschnitt 3 des Auftrags
  meint:** wer das Raster verschiebt, weil das Ergebnis nicht gefiel, hat
  selektiert — hier ist die Selektion belegt und ihr Umfang nicht.
* `docs/UEBERGABEPROTOKOLL.md` 3.3 beschreibt die Universumsentwicklung
  **Top 25 → 50 → 100 → 150** mit jeweils angehobenen Mindestschwellen. Das
  sind mindestens vier Durchgänge des Aktien-Elliott-Rasters; abgelegt ist die
  Ergebnisdatei genau **eines** davon.

### 5.2 Überschriebene Ergebnisdateien

Jede der neun `multi_symbol_optimisation_results.csv` wurde **genau einmal**
committet, beim Anlegen des Bots, und nie wieder. Läufe danach — und es gab
sie nachweislich, sonst wäre etwa die Look-Ahead-Korrektur ohne Nachrechnung
geblieben — haben entweder dieselbe Datei lokal überschrieben oder ihr
Ergebnis nur auf den Bildschirm geschrieben. Beides ist hier nicht mehr
sichtbar.

Besonders deutlich bei `elliott_wave`: die abgelegte Datei liegt bis heute
unter dem **alten** Pfad `results/multi_symbol_optimisation_results.csv`,
obwohl `strategy_paths.py` seit langem `results/elliott_wave/` vorsieht. Der
Ordner `results/elliott_wave/` existiert nicht. Seit der Umstellung auf
`strategy_paths.py` hat dieser Bot also **keinen** Optimierungslauf mehr
abgelegt.

### 5.3 Informelle Versuche von Hand

Was in einem Chatverlauf probiert wurde, bevor ein Raster im Code stand, ist
hier nicht rekonstruierbar — weder Zahl noch Richtung. Die
Zeitrahmen-Odyssee des T3-Bots (1 h → 15 min → 4 h, Übergabeprotokoll 3.2)
und die verworfene Erweiterung auf alle 503 S&P-500-Werte sind zwei bekannte
Beispiele; ihre Versuchszahl ist nicht überliefert.

### 5.4 Verworfene Varianten ohne Bericht

`docs/UEBERSICHT_RESEARCH.md` führt achtzehn Untersuchungsordner, das Repo
enthält inzwischen vierundzwanzig. Was **vor** dem ersten `BERICHT.md` einer
Untersuchung verworfen wurde, steht nirgends. Zwei Ordner
(`parameter_doku`, `uebersprungene_trades`) haben überhaupt keinen Bericht,
nur einen Docstring.

---

## 6. Einordnung: was bedeutet die Zahl für die Deflated Sharpe Ratio?

Bei **N** Versuchen mit reinem Rauschen liegt das erwartete Maximum der
standardisierten Kennzahl bei etwa **√(2 ln N)** Standardabweichungen.
Umgerechnet auf einen Jahres-Sharpe aus **T** Beobachtungen:
√(2 ln N) / √T · √252.

`python3 research/versuchsregister/versuchsregister.py --dsr`

| N | √(2 ln N) | Schwelle bei T = 252 (1 Jahr) | Schwelle bei T = 1 260 (5 Jahre) |
|---:|---:|---:|---:|
| 36 | 2,677 | 2,68 | 1,20 |
| 81 | 2,965 | 2,96 | 1,33 |
| 237 | 3,307 | 3,31 | 1,48 |
| **653** | **3,600** | **3,60** | **1,61** |
| **2 798** | **3,984** | **3,98** | **1,78** |

**Nicht bewertet, nur ausgerechnet.** Zwei Eigenschaften der Rechnung gehören
allerdings dazu, weil sie die Richtung des Fehlers bestimmen:

* Die Näherung setzt **unabhängige** Versuche voraus. Benachbarte Rasterpunkte
  sind stark korreliert (Stop 2 % und Stop 3 % handeln weitgehend dieselben
  Trades), die effektive Zahl unabhängiger Versuche liegt also **unter** N —
  die Schwelle ist damit eher zu hoch angesetzt.
* Dem steht entgegen, dass N selbst eine **Untergrenze** ist (Abschnitt 5).

Was daraus folgt, entscheidet der Nutzer.

---

## 6a. Vorgemerkte Versuche (noch nicht gerechnet)

Hier stehen Versuche, die **vorregistriert**, aber noch nicht gelaufen sind.
Sie zählen **nicht** in die Summen der Abschnitte 0 bis 4 — dort steht, was
belegbar gerechnet wurde. Sie stehen trotzdem hier, weil die Frage „wie oft
wurde in diesem Projekt etwas probiert?" sonst genau in dem Moment eine
falsche Antwort bekäme, in dem sie zum ersten Mal vorher gestellt wird.

| # | Versuch | Register | Kombinationen | zählt zur DSR? |
|---|---|---|---:|---|
| V1 | **Neuselektion der neun Bots** (TB-30a) | [`docs/VORREGISTRIERUNG_neuselektion.md`](../../docs/VORREGISTRIERUNG_neuselektion.md) | **2 416** (je Bot aufgeschlüsselt im Register) | **ja** — dort wird unter Alternativen gewählt |
| V2 | **S-E1, Turn-of-Month** (Nulltest) | [`docs/VORREGISTRIERUNG_S-E1_nulltest.md`](../../docs/VORREGISTRIERUNG_S-E1_nulltest.md) | **1** | **nein** — siehe unten |

### Zu V2: ein Versuch ohne Wahl ist trotzdem ein Versuch

`S-E1` bekommt hier **einen Eintrag** und zur DSR **keinen Beitrag**. Das ist
kein Widerspruch, sondern der Unterschied zwischen zwei Fragen:

* *Wie oft wurde etwas probiert?* — Darauf antwortet dieses Register, und
  S-E1 ist ein Versuch.
* *Wie viel Multiplizität muss eine Kennzahl vertragen?* — Multiplizität
  entsteht, wo unter **Alternativen gewählt** wird. Bei S-E1 gibt es keine:
  das Fenster stammt aus der Literatur, es wird kein Parameter gewählt,
  **N = 1**.

Die **Sweep-Zellen** von S-E1 zählen in keines von beiden. Sie sind
Robustheit, nicht Auswahl: fällt das Kernfenster durch und besteht eine
Sweep-Variante, wird sie nicht übernommen — *sonst wären es acht Versuche
und nicht einer*. Wird diese Bedingung je aufgehoben, ist das ein **neuer
vorregistrierter Lauf**, und dann zählen sie alle.

### Was beim Lauf zu tun ist

Sobald V1 oder V2 gerechnet ist, wandert die Zeile aus diesem Abschnitt in
Abschnitt 1 bis 3, die Summen in Abschnitt 0 und 4 werden nachgezogen, und
die `STAND_*`-Tabellen in `versuchsregister.py` ebenso. Bis dahin gilt: die
Zahlen oben sind **Vorhaben**, keine Belege.

---

## 7. Wie das Register fortgeschrieben wird

```bash
python3 research/versuchsregister/versuchsregister.py            # Erhebung anzeigen
python3 research/versuchsregister/versuchsregister.py --pruefen  # Wächter, RC 1 bei Befund
python3 research/versuchsregister/versuchsregister.py --historie # Rastergrösse je Commit
python3 research/versuchsregister/versuchsregister.py --dsr      # Einordnung nachrechnen
```

Der Wächter vergleicht 53 Angaben — 21 Rastergrössen, 10 Ergebnisdateien,
22 Rasterläufe unter `research/` — gegen die Tabellen `STAND_*` in
`versuchsregister.py`. Wer ein Raster erweitert oder einen neuen Rasterlauf
ablegt, zieht **beides** nach: die `STAND_*`-Tabelle und dieses Dokument. Das
ist der Zweck: eine Untergrenze, die leise nicht mehr stimmt, ist schlechter
als gar keine.

`--historie` braucht eine **vollständige** Git-Historie. In einem flachen Klon
(`git clone --depth …`, wie ihn manche Arbeitsumgebungen anlegen) bricht der
Befehl mit einem Hinweis ab, statt eine zu niedrige Rundenzahl zu melden.
