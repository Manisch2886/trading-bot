# Übergabe TB-27 — Bestandsaufnahme Kapitalsimulation

**Stand: 2026-09-13.** Untersuchung, keine Änderung. Bericht:
`research/tb27_kapitalsimulation/BERICHT.md`, Kurzfassung zum Kopieren:
`docs/ERGEBNIS_TB27_bestandsaufnahme.md`.

---

## 1. Muss die Mass-Reparatur eine Stelle anfassen oder neun?

**Weder noch — und die Frage zielt an der entscheidenden Stelle vorbei.**

**In den neun `equity_simulation.py` sind es zwei Stellen, und beide sind
bereits einheitlich.** Die Kapitalrechnung steht seit TB-26 einmal in
`shared/zuteilung.py`. Das Drawdown-Mass steht neunmal da, aber
**zeichengleich** — `calculate_max_drawdown()` ist in allen neun Dateien
Zeichen für Zeichen dasselbe, ebenso die Renditeformel. Die Behauptung der
externen Analyse, das Messproblem sitze „in jeder Fassung an derselben
Stelle", ist damit für diese neun Dateien **bestätigt**, und zwar im
wörtlichsten Sinn.

**Nur: dort entsteht keine Zahl, die etwas entscheidet.** Diese neun Dateien
liefern die *ausgewiesenen* Zahlen (Kurve, Rendite, Drawdown). Die Zahl, nach
der **Parameter ausgewählt** werden, ist der `robustness_score`, und der
entsteht woanders:

| wo | wie oft | rechnet auf |
|---|---:|---|
| `multi_symbol_optimise.py::evaluate_combination_multi` | **9** | naive Summe der Trade-Prozente, beide Drawdown-Masse |
| `multi_symbol_walk_forward.py::evaluate_combination_multi_windowed` | **6** | naive Summe, **nur** das Blockmass |
| `optimise_elliott.py` (2×), `optimise_trend.py` (1×) | **3** | naive Summe, nur das Blockmass |

Für die Mass-Reparatur lautet die Antwort damit: **9 + 6 + 3 Stellen, und
keine davon liegt in `equity_simulation.py`.** Wer nur die neun
Kapitalsimulationen anfasst, ändert, was berichtet wird — nicht, was gewählt
wird.

---

## 2. Die stillen Divergenzen

**Eine mit möglicher Zahlenwirkung:**

**U5 — zwei entgegengesetzte Antworten auf dieselbe Frage.** Fehlt `BTCUSDT`
in den Kursdaten, überspringt `t3_supertrend` seinen BTC-Regimefilter
**stillschweigend** (`if "BTCUSDT" in all_data`, `equity_simulation.py:69`).
`volatility_breakout_crypto` **bricht ab** und begründet das im Docstring
ausdrücklich: „Fehlt BTCUSDT, wird NICHT stillschweigend ungefiltert
weitergerechnet — das wäre genau die Lücke, die hier geschlossen wird, nur
unsichtbar." Es gibt nirgends eine Entscheidung, warum die beiden Bots das
verschieden handhaben.

*Eingrenzung, damit der Befund nicht grösser wirkt als er ist:*
`t3_supertrend/forward_test.py` verhält sich live genauso (`btc_regime_bullish
= True`, wenn BTCUSDT fehlt). Es ist also **keine** Backtest-gegen-Live-
Abweichung wie damals bei `USE_TAKE_PROFIT`, sondern eine zwischen zwei Bots.
Erreichbar wird sie, wenn `data/BTCUSDT_4h.csv` fehlt oder noch nicht geholt
wurde; dann rechnet `t3_supertrend` ohne Filter und meldet es nicht.

**Drei ohne Zahlenwirkung, aber irreführend:**

* **U9** — ein Kommentar in `rsi2_mean_reversion/equity_simulation.py:48`
  verweist auf `run_from_walk_forward_best()`; diese Funktion existiert im
  ganzen Repo nicht.
* **U10** — zwei der drei `research/`-Kopien von `calculate_max_drawdown()`
  behaupten wörtlich, „identisch" zur Bot-Fassung zu sein, und sind es nicht
  (zusätzliches `float()` im `round`). Zahlenwirkung ist nicht zu erwarten,
  aber **nicht nachgemessen** — in dieser Umgebung fehlt `pandas`.
* **U6/U8** — `elliott_wave` ist der einzige der drei Bots mit hart
  verdrahtetem `ALLOCATION_PCT` ohne erklärenden Kommentar dazu; die in PR #48
  richtiggestellte Erklärung zu den übersprungenen Trades ist nur bei einem der
  acht Limit-Bots angekommen.

**Als unklar gemeldet, nicht geraten:** **U11** — `elliott_wave_stocks` kappt
die Historie **vor** der Indikatorberechnung, während die drei anderen
Aktien-Bots nur den Einstiegszeitpunkt kappen und genau das ausdrücklich
begründen. Ob das für Elliott nötig ist oder ein Rückstand, ist aus dem Code
nicht entscheidbar; die fehlende Information ist, ob es je entschieden wurde.
Die Stelle liegt in `multi_symbol_optimise.py`, also ausserhalb des
Auftragsrahmens — hier nur vermerkt.

**Ausdrücklich nicht gefunden:** keine abweichende Rechenformel, keine
abweichende Rundung, keine abweichende Reihenfolge, kein zweiter
Startkapital-Wert, keine Funktion, die in einem Bot etwas anderes tut als ihr
Name in den anderen sagt. Der Bauplan der neun Dateien ist derselbe.

---

## 3. Zwei Nebenbefunde, die vor der Entscheidung stehen sollten

**M1 hat den Walk-Forward nicht erreicht.** PR #90 hat
`max_drawdown_chronologisch_pct` in die neun `multi_symbol_optimise.py`
gebracht. Sechs der neun Bots haben aber einen **eigenen**
Walk-Forward-Rechner, und der kennt nur das Blockmass. Der Walk-Forward ist
Pflichtstufe der Methodik (Prinzip 7). Fällt die Entscheidung für das
chronologische Mass, wählt der Walk-Forward bei sechs Bots weiter nach dem
alten. Die drei Ausnahmen (`elliott_wave`, `elliott_wave_stocks`,
`t3_supertrend`) importieren `evaluate_combination_multi` und bekommen beide
Masse mit.

**`research/parameter_doku/pruefe_fundstellen.py` ist auf `main` rot.**
35 von 38 Prüfungen bestanden, Rückgabewert 1. Die drei Fehlschläge sind
dokumentierte Zeilennummern in `equity_simulation.py`-Dateien, die seit den
Einfügungen von TB-26 verrutscht sind:

| dokumentiert | tatsächlich |
|---|---|
| `t3_supertrend/equity_simulation.py:66` → `compute_btc_regime` | Zeile 70 |
| `volatility_breakout/equity_simulation.py:160` → `collect_all_trades` | 58 / 152 |
| `volatility_breakout_crypto/equity_simulation.py:176` → `collect_all_trades` | 54 / 167 |

Vorbestehend, nicht durch diese Untersuchung entstanden, mit drei Zahlen zu
beheben. Wichtiger als die drei Zahlen ist, was der Befund zeigt: es gibt eine
Abhängigkeitsklasse **Zeilennummern**, die bisher auf keiner Liste stand — und
jede Änderung an diesen Dateien verschiebt sie weiter.

---

## 4. Die Abhängigkeitsliste war deutlich unvollständig

TB-26 nannte fünf Werkzeuge und schrieb dazu, die Liste sei vermutlich nicht
vollständig. Mechanisch gesucht: 154 Python-Dateien nennen
`equity_simulation`, **125** fassen sie als Code an, **123 davon von aussen**.

Die tragende Abhängigkeit — die Signaturabfrage, die erkennt, dass
`elliott_wave` kein Positionslimit hat — steht an **zwölf** Stellen, nicht an
zwei: `shared/portfolio_overview.py:348`, `shared/determinismus_lauf.py:652`,
`shared/test_zuteilung.py:832` und neun Stellen unter `research/`
(`order_sensitivity`, `elliott_wave_lookahead` 2×, `elliott_wave_params`,
`exposure_messung`, `hrp_portfolio`, `sync_check`, `tb24_haltedauern`,
`trend_overlay`).

**Die schwerwiegendste bisher nicht gelistete:**
`notifications/manual_close.py` liest `ALLOCATION_PCT` **per AST als
Zahlen-Literal** direkt aus `strategies/<bot>/equity_simulation.py` — und ist
für `elliott_wave`, `elliott_wave_stocks` und `t3_supertrend` die **einzige**
Quelle dieser Zahl, weil deren `live_params.py` sie nicht führt. Die Zahl steht
im Bestätigungsdialog, mit dem im Dashboard Positionen geschlossen werden, also
in einem **schreibenden** Weg.

---

## 5. Empfehlung — mit Alternative, nicht entschieden

**Weg A (die neun Dateien zusammenlegen)** löst wenig und bricht viel: der
gemeinsame Teil ist bereits einheitlich, während ≥ 12 Signaturabfragen, drei
Bot-Listen, `manual_close.py`, die undokumentierte Namensschnittstelle
`max_dd`/`result`/`trades` zu `determinismus_lauf.py` und drei Zeilennummern
daran hängen.

**Weg B (die Zielfunktion an den vorhandenen Stellen tauschen)** bricht nichts
davon — die neun Stellen sind zeichengleich, also mechanisch —, löst aber die
eigentliche Frage nicht, solange die auswählende Kennzahl unangetastet bleibt.

**Der kleinste Eingriff, der die Zusicherung trägt** (falls die Zusicherung
lautet „das Mass steht ab jetzt an einer Stelle"):

1. `calculate_max_drawdown()` und die Renditeformel **einmal** nach `shared/`
   ziehen, nach dem Muster von `shared/zuteilung.py`; die neun importieren sie.
   Signatur, Dateipfad, `ALLOCATION_PCT` und alle zwölf Signaturabfragen
   bleiben unberührt — es fällt nur der neunfach kopierte Rumpf weg.
2. `shared/ergebniskurven.py::kennzahlen()` und `shared/determinismus_lauf.py`
   auf dieselbe Quelle umstellen, statt die Formel nachzurechnen.
3. **Getrennt danach:** welches Mass führt — und ob die 9 + 6 + 3 auswählenden
   Stellen mitwandern.

Schritt 1 und 2 ändern **keine Zahl**; das ist prüfbar, weil
`shared/ergebniskurven.py` danach weiterhin `9× AKTUELL` melden muss.
Schritt 3 ändert Zahlen und gehört hinter den Vergleich, nicht davor.

**Beide Wege bleiben offen. Die Entscheidung ist die des Nutzers, Frist
13.12.2026.**

---

## 6. Was entstanden ist, und warum ein Werkzeug bleibt

| Datei | Zweck |
|---|---|
| `research/tb27_kapitalsimulation/BERICHT.md` | der vollständige Bericht |
| `research/tb27_kapitalsimulation/vergleich.py` | Vergleich je Funktion auf vier Stufen; mit `--pruefen` ein **Wächter** |
| `research/tb27_kapitalsimulation/test_vergleich.py` | 23 Prüfungen, alle grün |
| `research/tb27_kapitalsimulation/abhaengigkeiten.py` | die Abhängigkeitsliste, mechanisch und wiederholbar |
| `docs/ERGEBNIS_TB27_bestandsaufnahme.md` | Kurzfassung zum Kopieren |
| `docs/TESTAUFTRAG_TB27_bestandsaufnahme.md` | Prüfauftrag |

Der Auftrag stellt ein Testdokument frei — nötig nur, wenn ausführbarer Code
entsteht, der bleiben soll. **Er entsteht**, und zwar genau der Kandidat, den
der Auftrag selbst nennt: `vergleich.py --pruefen` hält den Stand vom
13.09.2026 fest und meldet, wenn eine der neun Dateien später still
auseinanderläuft. Ein Wächter, der nie rot werden kann, ist schlimmer als
keiner (Methodik-Prinzip 12) — deshalb weist `test_vergleich.py` am Verhalten
nach, dass er bei einer verfälschten `calculate_max_drawdown()` rot wird und
Bot wie Funktion benennt, bei neuen Kommentaren und geänderten Docstrings aber
grün bleibt.

---

## 7. Randbedingungen — eingehalten

| Bedingung | Stand |
|---|---|
| `git diff origin/main HEAD --name-only` listet nur `research/` und `docs/` | **eingehalten** |
| keine `live_params.py`, `forward_test.py`, `equity_simulation.py`, `multi_symbol_optimise.py`, `shared/zuteilung.py` geändert | **eingehalten** (alle nur gelesen) |
| keine `results/*/equity_curve.csv` überschrieben | **eingehalten** — es wurde überhaupt kein Bot ausgeführt |
| nichts unter `broker/`, keine Crontab, keine launchd-Vorlage | **eingehalten** |
| nichts erfunden; Unentscheidbares als unklar gemeldet | **eingehalten** (U11, und die nicht nachgemessene Zahlenwirkung bei U10) |

**Was in dieser Umgebung nicht geprüft werden konnte:** `pandas`, `numpy`,
`binance`, `scipy`, `fastapi`, `yfinance` fehlen. Damit liess sich **nicht**
nachweisen, dass `shared/ergebniskurven.py` weiterhin `9× AKTUELL` meldet — das
braucht Kursdaten und einen Lauf aller neun Bots. Die Zusicherung ruht deshalb
auf einem strukturellen Argument statt auf einer Messung: es wurde kein Bot
ausgeführt und keine Datei ausserhalb von `research/tb27_kapitalsimulation/`
und `docs/` angelegt oder verändert (`git status` belegt es). **Wer auf Nummer
sicher gehen will, lässt `python3 shared/ergebniskurven.py` einmal auf dem
Rechner des Nutzers laufen** — dort sind die Abhängigkeiten vorhanden.

Basislauf auf unverändertem `main`: `notifications/test_manual_close.py` grün;
vier Prüfungen scheitern an fehlenden Modulen;
`research/parameter_doku/pruefe_fundstellen.py` scheitert inhaltlich (siehe
Abschnitt 3). Alle fünf Fehlschläge sind vorbestehend.
