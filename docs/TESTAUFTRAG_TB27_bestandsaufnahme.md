# Testauftrag: Bestandsaufnahme der neun `equity_simulation.py` (TB-27)

**Stand: 2026-09-13** · Gegenstand: die Werkzeuge aus
`research/tb27_kapitalsimulation/` und die Befunde des Berichts. Dieses
Dokument ist **eigenständig ausführbar**: es setzt nichts voraus ausser dem
Repo und Python 3. Kein `pandas`, kein `numpy`, keine Kursdaten, kein Netz,
keine API-Schlüssel.

---

## 0. Worum es geht (in drei Sätzen)

TB-27 hat die neun `equity_simulation.py` Funktion für Funktion verglichen und
festgestellt: das Drawdown-Mass steht neunmal **zeichengleich** da, die
Kapitalrechnung längst nur einmal — die entscheidende Kennzahl entsteht aber
gar nicht in diesen Dateien. Aus der Untersuchung bleibt ein **Wächter**:
`vergleich.py --pruefen` hält den Stand vom 13.09.2026 fest und meldet, wenn
eine der neun Dateien später still auseinanderläuft.

**Das ist die Zusicherung, die zu prüfen ist: der Wächter wird rot, wenn eine
stille Divergenz entsteht, und bleibt grün, wenn nur ein Kommentar sich
ändert.** Alles andere in diesem Dokument dient ihr.

---

## 1. Voraussetzungen

| | |
|---|---|
| Python | 3.9+ (entwickelt mit 3.11) |
| Pflicht | nichts ausser der Standardbibliothek |
| Nicht nötig | `pandas`, `numpy`, `binance`, `scipy`, `yfinance`, `node`, Netzzugang |

Alle Werkzeuge lesen ausschliesslich Quelltext. Keines importiert Bot-Code,
keines führt einen Bot aus, keines schreibt eine Datei. Sie können deshalb
weder Kursdaten abrufen noch eine Kurve überschreiben.

---

## 2. Der eine Befehl

```bash
cd <repo>
python3 research/tb27_kapitalsimulation/test_vergleich.py
```

**Erwartet:** `23/23 bestanden.` und Rückgabewert `0`. Laufzeit unter zehn
Sekunden.

Der Test legt Kopien der neun Dateien in einem temporären Ordner an,
verfälscht sie gezielt und prüft, was der Wächter dazu sagt. Er räumt hinter
sich auf und fasst das Repo nicht an.

Was er im Einzelnen nachweist:

> **Nachtrag TB-28 (13.09.2026).** `calculate_max_drawdown()` steht seit
> TB-28 nicht mehr in den neun Dateien, sondern einmal in
> `shared/messkette.py`. Die beiden Proben, die an ihrem Rumpf ansetzten,
> hätten ab sofort ins Leere gegriffen — der Test wäre grün geblieben, ohne
> noch etwas zu prüfen. Aufgefallen ist es nur, weil beide Proben vorher
> belegen, dass die Verfälschung überhaupt greift. Sie sitzen jetzt im Rumpf
> von `simulate_portfolio()`; die Zeilen unten sind entsprechend
> nachgezogen. Der Nachweis, dass die Messkette wirklich nur an einer Stelle
> steht, führt seitdem `shared/test_messkette.py`
> (`docs/TESTAUFTRAG_TB-28_messkette.md`).

| Abschnitt | Nachweis |
|---|---|
| 1 | Der echte Bestand entspricht der festgehaltenen Erwartung; `simulate_portfolio` sind **zwei** Gruppen, `calculate_max_drawdown` kommt (seit TB-28) gar nicht mehr vor |
| 2 | Eine unveränderte Kopie bleibt grün |
| 3 | **Eine verfälschte `simulate_portfolio()` macht ihn ROT** — und er nennt Bot und Funktion |
| 4 | Ein neuer Kommentar und ein geänderter Docstring lassen ihn **grün**; die Übersicht stuft die Gruppe dafür sichtbar von `zeichengleich` auf `ohne Kommentar` bzw. `sachlich gleich` zurück |
| 5 | Eine neu hinzugekommene und eine verschwundene Funktion werden gemeldet |
| 6 | Rechnen und Reden werden auseinandergehalten (Stufe 4, `print`-Argumente ausgeblendet) |

Abschnitt 3 ist der Kern: **ohne ihn wäre nicht belegt, dass die Prüfung
überhaupt rot werden kann** (Methodik-Prinzip 12).

---

## 3. Der Wächter im Alltag

```bash
python3 research/tb27_kapitalsimulation/vergleich.py --pruefen
```

**Erwartet heute:**
`UNVERAENDERT gegenueber dem Stand TB-27 (13.09.2026). 5 Funktionen ueber 9 Bots geprueft.`
und Rückgabewert `0`.

Meldet er später eine Abweichung, gibt es genau zwei richtige Reaktionen:

1. **Die Abweichung ist ungewollt** — dann gehört sie behoben, nicht
   weggeschrieben.
2. **Sie war gewollt** — dann wird die Tabelle `ERWARTUNG` in `vergleich.py`
   nachgezogen **und im zugehörigen Pull Request begründet**. Die Tabelle ist
   eine Bestandsaufnahme, keine Zielvorgabe; sie darf sich ändern, aber nie
   stillschweigend.

Sinnvolle Einbindung: in denselben Durchlauf wie
`python3 research/parameter_doku/pruefe_fundstellen.py`. Beide laufen ohne
`pandas` in Sekunden — und dass letzterer seit TB-26 rot ist, ohne dass es
jemandem aufgefallen wäre, ist das Argument dafür (siehe Abschnitt 5).

---

## 4. Die Befunde des Berichts einzeln nachvollziehen

### 4.1 Der Vergleich

```bash
python3 research/tb27_kapitalsimulation/vergleich.py
```

**Erwartet**, im Abschnitt `GRUPPEN SACHLICHER GLEICHHEIT`:

* `calculate_max_drawdown` — **kommt seit TB-28 nicht mehr vor** (steht
  einmal in `shared/messkette.py` und wird importiert); bis dahin
  `(1 Gruppe)` → `alle 9, zeichengleich`
* `simulate_portfolio   (2 Gruppen)` → acht zeichengleich, `elliott_wave` allein
* `collect_all_trades   (9 Gruppen)`
* `__main__   (8 Gruppen)`, davon `turtle_soup_crypto, turtle_soup_stocks`
  zeichengleich

Den Quelltext einer Funktion je Gruppe nebeneinander:

```bash
python3 research/tb27_kapitalsimulation/vergleich.py --zeige simulate_portfolio
```

Dasselbe für die Datei, in der die auswählende Kennzahl steht:

```bash
python3 research/tb27_kapitalsimulation/vergleich.py --datei multi_symbol_optimise.py
```

**Erwartet:** `calculate_robustness_score   (1 Gruppe)` → `alle 9, sachlich
gleich` (die Rümpfe sind gleich, nur die Kommentare unterscheiden sich).

### 4.2 Die Abhängigkeiten

```bash
python3 research/tb27_kapitalsimulation/abhaengigkeiten.py --ohne-erwaehnung
```

**Erwartet** in der Schlusszeile: von **154** Dateien, die den Namen nennen,
fassen **125** ihn als Code an, **123** davon von aussen.

Mit den Fundzeilen:

```bash
python3 research/tb27_kapitalsimulation/abhaengigkeiten.py --ohne-erwaehnung --zeilen
```

### 4.3 Einzelbelege mit einer Zeile

```bash
# U4 - die NaN-Wache haben genau die vier Aktien-Bots
grep -l melde_uebersprungene_balken strategies/*/equity_simulation.py

# U5 - zwei entgegengesetzte Antworten auf fehlendes BTCUSDT
grep -n 'BTCUSDT' strategies/t3_supertrend/equity_simulation.py
grep -n 'BTCUSDT' strategies/volatility_breakout_crypto/equity_simulation.py

# U9 - der Kommentar verweist auf eine Funktion, die es nicht gibt
grep -rn run_from_walk_forward_best --include=*.py .          # genau 1 Treffer, der Kommentar

# Der Walk-Forward kennt das chronologische Mass bei sechs Bots nicht
ls strategies/*/multi_symbol_walk_forward.py | wc -l                            # 9
grep -l 'pnl_pct"\].cumsum' strategies/*/multi_symbol_walk_forward.py | wc -l   # 6
grep -l max_drawdown_chronologisch_pct strategies/*/multi_symbol_walk_forward.py  # keiner
```

---

## 5. Der vorbestehende rote Befund

```bash
python3 research/parameter_doku/pruefe_fundstellen.py ; echo "Rueckgabe: $?"
```

**Erwartet:** `35/38 Pruefungen bestanden.`, Rückgabewert `1`, und diese drei
Fehlschläge:

```
FEHLGESCHLAGEN: t3_supertrend/equity_simulation.py:66 nennt compute_btc_regime
FEHLGESCHLAGEN: volatility_breakout/equity_simulation.py:160 nennt collect_all_trades
FEHLGESCHLAGEN: volatility_breakout_crypto/equity_simulation.py:176 nennt collect_all_trades
```

**Das ist kein Fehler dieser Untersuchung.** Er tritt auf unverändertem `main`
genauso auf; die dokumentierten Zeilennummern sind durch die Einfügungen von
TB-26 verrutscht. Zum Gegenbeweis:

```bash
git stash -u && python3 research/parameter_doku/pruefe_fundstellen.py ; echo "Rueckgabe: $?" ; git stash pop
```

(oder, ohne `stash`, auf einem frischen Auscheck von `origin/main`.)

---

## 6. Was dieser Test NICHT prüft

* **Keine Zahlen.** Es wurde kein Bot ausgeführt, keine Kurve erzeugt, kein
  Backtest gerechnet. Der AST-Vergleich beweist Gleichheit des **Codes**, nicht
  Gleichheit des **Verhaltens**: zwei zeichengleiche `collect_all_trades()`
  könnten sich verschieden verhalten, weil `get_trades_for_symbol()` in jedem
  Bot eine andere Funktion ist.
* **Nicht, dass `shared/ergebniskurven.py` weiterhin `9× AKTUELL` meldet.** Das
  braucht `pandas` und Kursdaten und liess sich in der Cloud-Umgebung nicht
  ausführen. Die Zusicherung ruht hier auf einem strukturellen Argument: es
  wurde kein Bot ausgeführt und keine Datei ausserhalb von
  `research/tb27_kapitalsimulation/` und `docs/` angelegt oder verändert. Zum
  Nachweis auf dem Rechner des Nutzers:

  ```bash
  git status --short          # nur die neuen Dateien, sonst nichts
  python3 shared/ergebniskurven.py
  ```

  **Erwartet:** `9× AKTUELL`.
* **Nicht die Crontab und nicht die launchd-Vorlagen** — die liegen nicht im
  Repo und wurden auch nicht angefasst.
