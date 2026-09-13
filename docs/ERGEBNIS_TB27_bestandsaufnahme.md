# Ergebnis: Bestandsaufnahme der neun `equity_simulation.py` (TB-27)

**Stand: 2026-09-13** · Untersuchung, keine Änderung. Vollständiger Bericht:
`research/tb27_kapitalsimulation/BERICHT.md`.

---

## Die Antwort zuerst

> **Muss die Mass-Reparatur eine Stelle anfassen oder neun?**
>
> **In den neun `equity_simulation.py`: zwei Stellen, und beide sind schon
> einheitlich.** Die Kapitalrechnung steht seit TB-26 einmal in
> `shared/zuteilung.py`; das Drawdown-Mass steht neunmal da, aber
> **zeichengleich**. Die Renditeformel ebenso.
>
> **Die Zahl, die eine Entscheidung trägt, entsteht dort aber nicht.**
> Parameter werden nach `robustness_score` ausgewählt, und der entsteht in
> `multi_symbol_optimise.py` (**9×**), in `multi_symbol_walk_forward.py`
> (**6×**) und in den älteren `optimise_*.py` (**3×**).
>
> Für die Mass-Reparatur lautet die Antwort damit weder „eine" noch „neun",
> sondern: **9 + 6 + 3 — und keine davon liegt in `equity_simulation.py`.**

---

## Der Vergleich, Funktion für Funktion

Verglichen auf **AST-Ebene ohne Docstrings** (Stufe 3), daneben Text,
Tokenstrom und eine Stufe, die alle `print`-Argumente ausblendet.

| Funktion | Gruppen | Befund |
|---|---:|---|
| `calculate_max_drawdown` | **1** | alle neun **zeichengleich** |
| `simulate_portfolio` | **2** | acht zeichengleich; `elliott_wave` allein (kein Positionslimit) |
| `apply_btc_regime_filter` | 1 | existiert nur bei `volatility_breakout_crypto` |
| `__main__` | 8 | nach Abzug der Bildschirmausgabe bleiben **drei** Unterschiede |
| `collect_all_trades` | **9** | jede Fassung für sich |

Die drei verbleibenden `__main__`-Unterschiede: die Argumentliste von
`collect_all_trades`, das fehlende Positionslimit bei `elliott_wave`, der
Regimefilter-Schritt bei `volatility_breakout_crypto` (PR #57). **Alle drei
bot-eigen nötig.** Die Messkette selbst ist in allen neun identisch.

---

## Die stillen Divergenzen

**Eine mit möglicher Zahlenwirkung:**

* **U5 — fehlt `BTCUSDT` in den Kursdaten, überspringt `t3_supertrend` seinen
  BTC-Regimefilter stillschweigend; `volatility_breakout_crypto` bricht ab**
  und begründet das ausdrücklich („wird NICHT stillschweigend ungefiltert
  weitergerechnet"). Dieselbe Frage, zwei entgegengesetzte Antworten, nirgends
  entschieden.
  *Eingrenzung:* `t3_supertrend/forward_test.py` verhält sich live genauso —
  es ist **keine** Backtest-gegen-Live-Abweichung, sondern eine zwischen zwei
  Bots. Erreichbar, wenn `data/BTCUSDT_4h.csv` fehlt.

**Drei ohne Zahlenwirkung, aber irreführend:**

* **U9** — `rsi2_mean_reversion/equity_simulation.py:48` verweist auf
  `run_from_walk_forward_best()`. Diese Funktion gibt es im ganzen Repo nicht.
* **U10** — zwei von drei `research/`-Kopien von `calculate_max_drawdown()`
  behaupten, „identisch" zur Bot-Fassung zu sein, und sind es nicht
  (zusätzliches `float()`). Zahlenwirkung nicht zu erwarten, **nicht
  nachgemessen** (kein `pandas` in dieser Umgebung).
* **U6/U8** — `elliott_wave` trägt als einziger der drei Bots mit hart
  verdrahtetem `ALLOCATION_PCT` keinen erklärenden Kommentar dazu; die in
  PR #48 korrigierte Erklärung zu den übersprungenen Trades ist nur bei einem
  der acht Limit-Bots angekommen.

**Als unklar gemeldet, nicht geraten:**

* **U11** — `elliott_wave_stocks` kappt die Historie **vor** der
  Indikatorberechnung, die drei anderen Aktien-Bots nur den
  Einstiegszeitpunkt und begründen genau das. Ob das für Elliott nötig ist
  oder ein Rückstand, **ist aus dem Code nicht entscheidbar**. Fehlende
  Information: ob die Abweichung je entschieden wurde — in `docs/` und
  `research/` steht nichts dazu. Liegt ausserhalb der neun Dateien.

**Nicht gefunden:** keine abweichende Rechenformel, keine abweichende Rundung,
keine abweichende Reihenfolge, kein zweiter Startkapital-Wert.

---

## Zwei Befunde, die vor der Entscheidung stehen sollten

**1. M1 hat den Walk-Forward nicht erreicht.** PR #90 hat
`max_drawdown_chronologisch_pct` in die neun `multi_symbol_optimise.py`
gebracht. **Sechs** der neun Bots haben aber einen eigenen
Walk-Forward-Rechner, und der kennt nur das Blockmass. Der Walk-Forward ist
Pflichtstufe der Methodik. Fällt die Entscheidung für das chronologische Mass,
wählt der Walk-Forward bei sechs Bots weiter nach dem alten.

**2. `research/parameter_doku/pruefe_fundstellen.py` ist auf `main` rot.**
35 von 38 Prüfungen bestanden; die drei Fehlschläge sind dokumentierte
Zeilennummern, die in `equity_simulation.py`-Dateien zeigen und seit TB-26
verrutscht sind. Vorbestehend, mit drei Zahlen zu beheben — und ein Hinweis
darauf, dass es eine Abhängigkeitsklasse **Zeilennummern** gibt, die bisher
nirgends gelistet war.

---

## Die Abhängigkeiten von aussen

154 Python-Dateien nennen `equity_simulation`, **125** fassen sie als Code an,
**123 davon von aussen**. TB-26 nannte fünf.

| Klasse | Anzahl | die wichtigsten |
|---|---:|---|
| **Signaturabfrage** auf `simulate_portfolio` (erkennt „hat kein Limit") | **12** | `shared/portfolio_overview.py`, `shared/determinismus_lauf.py`, `shared/test_zuteilung.py`, 9× unter `research/` |
| **Bot-Liste über Dateiexistenz** | 3 | `shared/ergebniskurven.py`, `shared/determinismus.py`, `research/zuteilungskaskade/` |
| **Datei-Inhalt per AST** | 1 | **`notifications/manual_close.py`** — liest `ALLOCATION_PCT` als Literal und ist für drei Bots die **einzige** Quelle der Positionsgrösse im **schreibenden** Schliess-Dialog |
| **Zeilennummern** | 1 | `research/parameter_doku/pruefe_fundstellen.py` (3 Fundstellen, heute falsch) |
| **`runpy` / `importlib` über den Pfad** | 8 | `shared/kurven_lauf.py`, `shared/determinismus_lauf.py`, 6× `research/` |
| **Unterprozess** (`subprocess`) | 34 | wegen der `sys.modules`-Kollision gleichnamiger Module |
| **Direktimport** nach `sys.path`-Umbiegung | 65 | 37 unter `strategies/`, 25 unter `research/`, 3 unter `shared/` |

---

## Die zwei Wege — nicht entschieden

| | **Weg A: zusammenlegen** | **Weg B: Zielfunktion tauschen** |
|---|---|---|
| löst | Mass an einer Stelle; `sys.modules`-Kollision entfällt | genau das, was die Mass-Reparatur will |
| Gewinn | **klein** — der gemeinsame Teil ist schon einheitlich | — |
| bricht | ≥ 12 Signaturabfragen, 3 Bot-Listen, `manual_close.py`, die Namensschnittstelle zu `determinismus_lauf.py`, 3 Zeilennummern | nichts davon |
| Umfang | 9 Dateien + 12 + 3 + 1 + 2 Testsuiten, danach 9 Kurven neu | 9 zeichengleiche Stellen + 2 Nachrechnungen in `shared/` |
| löst NICHT | — | die auswählende Kennzahl (9 + 6 + 3) |

**Der kleinste Eingriff, der die Zusicherung „das Mass steht an einer Stelle"
trägt** — ist keiner von beiden in Reinform:

1. `calculate_max_drawdown()` und die Renditeformel **einmal** nach `shared/`
   ziehen (Muster `shared/zuteilung.py`), die neun importieren sie. Signatur,
   Dateipfad, `ALLOCATION_PCT` und alle zwölf Signaturabfragen bleiben
   unberührt.
2. `shared/ergebniskurven.py::kennzahlen()` und `shared/determinismus_lauf.py`
   auf dieselbe Quelle umstellen, statt nachzurechnen.
3. **Getrennt danach:** welches Mass führt — und ob die 9 + 6 + 3 auswählenden
   Stellen mitwandern.

Schritt 1 und 2 ändern **keine Zahl** (prüfbar: `shared/ergebniskurven.py`
muss danach weiter `9× AKTUELL` melden). Schritt 3 ändert Zahlen und gehört
hinter den Vergleich, nicht davor.

**Nicht entschieden** — das ist eine Entscheidung des Nutzers, Frist
13.12.2026.

---

## Was entstanden ist

| Datei | Zweck |
|---|---|
| `research/tb27_kapitalsimulation/BERICHT.md` | der vollständige Bericht |
| `research/tb27_kapitalsimulation/vergleich.py` | der Vergleich, und mit `--pruefen` ein **Wächter**, der künftige stille Divergenz meldet |
| `research/tb27_kapitalsimulation/test_vergleich.py` | 23 Prüfungen, die belegen, dass der Wächter auch **rot** wird |
| `research/tb27_kapitalsimulation/abhaengigkeiten.py` | die Abhängigkeitsliste, mechanisch und wiederholbar |
| `docs/TESTAUFTRAG_TB27_bestandsaufnahme.md` | Prüfauftrag zum Nachvollziehen |

Alle laufen ohne `pandas`, ohne Kursdaten, ohne Netz und schreiben nichts.

---

## Belastbarkeit

* **AST beweist Gleichheit des Codes, nicht des Verhaltens** — zwei
  zeichengleiche `collect_all_trades()` könnten sich verschieden verhalten,
  weil `get_trades_for_symbol()` je Bot eine andere Funktion ist. Umgekehrt
  gilt der Befund streng.
* **Nichts wurde ausgeführt.** In dieser Umgebung fehlen `pandas`, `numpy`,
  `binance`, `scipy`, `fastapi`, `yfinance`. Kein Bot, kein Backtest, keine
  Kurve ist gelaufen; Aussagen zur Zahlenwirkung sind entsprechend
  gekennzeichnet.
* **Basislauf auf unverändertem `main`:** `notifications/test_manual_close.py`
  grün; `shared/test_zuteilung.py`, `shared/test_ergebniskurven.py`,
  `shared/test_determinismus.py`, `dashboard/test_dashboard.py` scheitern an
  fehlenden Modulen; `research/parameter_doku/pruefe_fundstellen.py` scheitert
  inhaltlich (siehe oben). Alle fünf Fehlschläge sind vorbestehend.
* **Suchmethode für die Abhängigkeiten:** mechanisch über den Namensstamm,
  von Hand gegengeprüft auf zusammengesetzte Namen und Verzeichnis-Listings
  (nichts gefunden). **Nicht erreichbar:** Crontab und launchd-Vorlagen des
  Nutzers, und die ZIP-Kopien im Downloads-Ordner.
* **Nicht angefasst:** keine `live_params.py`, `forward_test.py`,
  `equity_simulation.py`, `multi_symbol_optimise.py`, `shared/zuteilung.py`,
  keine `results/*/equity_curve.csv`, nichts unter `broker/`, keine Crontab,
  keine launchd-Vorlage.
