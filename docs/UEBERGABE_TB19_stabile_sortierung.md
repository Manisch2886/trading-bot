# TB-19 — Stabile Sortierung: Übergabe-Zusammenfassung

**Stand:** 2026-09-13 · **Zweig:** `claude/new-session-oxhn5e` · **Basis:** `main` (f735d4d)

---

## 1. Die verschobenen Zahlen

Beide vorhergesagten Werte sind **exakt** eingetroffen.

| Kennzahl | vorher | nachher |
|---|---:|---:|
| Kombinierter Vierer-Drawdown (`portfolio_correlation_analysis.py`) | −9,34 % | **−9,41 %** |
| Montags-Mail / Dashboard-Portfolio-Sicht, kombinierter Drawdown (`portfolio_overview.py`) | −11,29 % | **−11,41 %** |

**Nach dem Merge zeigt die Dashboard-Portfolio-Sicht −11,41 % statt −11,29 %.**
Das ist kein neuer Fehler, sondern die Korrektur.

### Es verschieben sich mehr Zahlen als die zwei genannten

Das war so nicht angekündigt und gehört deshalb hierher:

| Stelle | vorher | nachher |
|---|---:|---:|
| Einzel-Drawdown `rsi2_crypto` (Montags-Mail, Teil 1) | −13,11 % | −13,30 % |
| Einzel-Drawdown `turtle_soup_stocks` (Montags-Mail, Teil 1) | −18,67 % | −18,71 % |
| Einzel-Drawdown RSI-2 Mean-Reversion (Vierer-Analyse) | −11,17 % | −11,73 % |
| 21 der 26 bezifferten Korrelationen in Teil 3 der Montags-Mail | z. B. 0,08 | z. B. 0,12 |

Die **Schwelle 0,3** überschreitet keine der Korrelationen — vorher wie
nachher nicht; der grösste Betrag steigt von 0,14 auf 0,16. Die zehn
Paare unterhalb der Mindestzahl gemeinsamer Handelstage bleiben
unverändert ohne Zahl. Es ändert sich also keine Aussage, nur die Nachkommastellen.
Renditen sind unverändert (die hängen am ersten und letzten Tag, nicht an
Gleichständen).

---

## 2. Warum die neuen Zahlen die richtigen sind

Nicht „stabil ist ordentlicher", sondern nachgerechnet:

1. `equity_simulation.py` schreibt `results/<bot>/equity_curve.csv` in
   **Ereignisreihenfolge**. Nachgemessen: alle neun Dateien sind bereits
   chronologisch, und `sort_values(..., kind="stable")` lässt sie
   **Zeile für Zeile unverändert**.
2. Der Kapitalstand eines Tages ist damit der Wert der **letzten** Zeile
   dieses Tages. Genau den greift `groupby(...).last()` nach einer stabilen
   Sortierung ab.
3. Ohne `kind="stable"` vertauscht Quicksort die Gleichstände, und
   `.last()` liefert einen **Zwischenstand mitten im Tag**.

Die alten Zahlen waren also nicht „eine andere Konvention", sondern an
manchen Tagen schlicht der falsche Kapitalstand.

**Wie viele Tage betroffen sind** (Datenstand 13.09.2026):

| Kurve | Tage | davon abweichend |
|---|---:|---:|
| `elliott_wave` | 92 | 1 |
| `volatility_breakout_crypto` | 142 | 10 |
| `elliott_wave_stocks` | 281 | 11 |
| `rsi2_crypto` | 224 | 18 |
| `t3_supertrend` | 385 | 20 |
| `volatility_breakout` | 966 | 96 |
| `turtle_soup_crypto` | 604 | 120 |
| `rsi2_mean_reversion` | 1441 | 312 |
| `turtle_soup_stocks` | 2022 | **698** |

**Betroffen sind alle neun Bots, nicht nur die Aktien-Bots.** Der Auftrag
nannte nur die Aktien-Bots; die Krypto-Kurven haben dieselben
Gleichstände, weil auch dort mehrere Ausstiege auf denselben Zeitstempel
fallen.

---

## 3. Die weiteren `sort_values`-Stellen

**144 echte `sort_values`-Aufrufe** stehen auf `main`, davon **31 bereits
mit `kind="stable"`** (TB-18 und die `research/`-Untersuchungen) und
**113 ohne**. TB-19 stellt **2** davon um; **111 bleiben**.

| Schlüssel | Stellen | Doppelter Schlüssel möglich? | Verdikt |
|---|---:|---|---|
| `open_time` (Kursdaten) | 27 | **Nein** — 0 Dubletten in allen 242 `data/*.csv`, gemessen | ungefährdet, nicht angefasst |
| `time` auf Kapitalkurven → `groupby().last()` | 19 | **Ja**, alle neun Kurven | 2 umgestellt, **17 gefährdet** |
| `exit_time`, gleiches Muster (`research/exposure_messung/`) | 2 | **Ja** | **gefährdet** |
| `entry_time` auf Trade-Mengen | 24 | **Ja** — 4.888 von 5.391 bzw. 11.641 von 12.069 Zeilen teilen einen Zeitstempel | **gefährdet**, heute folgenlos (s. u.) |
| `fib_score` (Elliott-Wellen) | 4 | **Ja** — 8 von 11 Zeilen in `results/BTCUSDT_impulse_waves.csv` | **gefährdet, live wirksam** (s. u.) |
| `robustness_score` u. a. Ranglisten | 31 | Ja (`t3_supertrend`: 2 Gleichstände) | Spitzenplatz heute eindeutig → folgenlos |
| Anzeige- und Vergleichs-Sortierungen | 6 | teils | kosmetisch, benannt |

### Die drei Befunde, die aus dieser Tabelle herausragen

**a) 19 weitere Stellen haben denselben Fehler wie die beiden korrigierten.**
Dieselbe `build_daily_capital_curve`-Vorlage steht 21-mal im Repo
(`sort_values` → `groupby("date")["capital_after"].last()`). TB-19
korrigiert zwei davon. Die übrigen 19 stehen in Stress-Perioden-Skripten,
Kapitalmanagement-Zusammenfassungen und `research/exposure_messung/`.
**Nicht angefasst** — nicht weil sie ungefährdet wären, sondern weil ihre
Ausgaben in bereits veröffentlichten Experiment- und
`research/`-Dokumenten stehen. Diese Zahlen zu verschieben ist nach der
Projektregel ein eigener, ausdrücklich freigegebener Schritt. Vorschlag
als Folgeaufgabe.

**b) `elliott_wave_counter.py` entscheidet per Quicksort, welches Muster
live wird.** `find_impulse_waves` und `remove_overlapping` geben ihre
Wellen mit `sort_values("fib_score", ascending=False)` zurück — auf einer
Spalte mit vielen Gleichständen (8 von 11 Zeilen in der abgelegten
BTC-Datei). `elliott_wave_stocks/forward_test.py:168` bricht die Schleife
bei `MAX_CONCURRENT_POSITIONS = 8` ab. **Welches von mehreren
gleich bewerteten Mustern eine Paper-Position wird, hängt damit an der
Sortierimplementierung.** Das ist die einzige gefundene Stelle, die bis in
den laufenden Betrieb durchschlägt. `forward_test.py` steht auf der
Sperrliste dieser Aufgabe — unverändert, hiermit gemeldet.

**c) `equity_simulation.py` ist gefährdet, aber heute unauffällig.**
`collect_all_trades` sortiert `entry_time` instabil, und dort teilen fast
alle Zeilen ihren Zeitstempel. Nachgemessen für `rsi2_mean_reversion` und
`turtle_soup_stocks`: die instabile Sortierung liefert dort **heute
dieselbe** Reihenfolge wie die stabile — deshalb sind die abgelegten
Kurven unverändert und `shared/ergebniskurven.py` meldet weiterhin
`9x AKTUELL`. Garantiert ist das nicht; es hängt an Feldlänge und
pandas-Version. Ebenfalls Sperrliste, ebenfalls gemeldet.

---

## 4. Was geändert wurde

| Datei | Änderung |
|---|---|
| `shared/portfolio_overview.py` | **nur** die Sortierzeile (Zeile 211) |
| `strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py` | Sortierzeile + Begründung im Kommentar |
| `shared/test_stabile_sortierung.py` | **neu** — Selbsttest, 46 Prüfungen |

In `portfolio_overview.py` steht bewusst **kein** erklärender Kommentar:
der Auftrag verlangte dort „nur die Sortierzeile, nichts sonst".

**Nicht geändert:** `live_params.py`, `forward_test.py`,
`equity_simulation.py`, `results/*/equity_curve.csv`, die abgelegten
Optimierungsergebnisse, `broker/`, Crontab, launchd-Vorlagen,
`research/`-Berichte.

`results/portfolio_overview/portfolio_overview_curve_live.csv` wurde von
den Messläufen neu geschrieben und **auf den Stand von `main`
zurückgesetzt** — diese Aufgabe ändert keine abgelegte Kurve. Der nächste
Lauf (Cronjob oder der Knopf im Dashboard) erzeugt sie mit den neuen
Zahlen neu.

---

## 5. Ein Nebeneffekt, der mehr wert ist als 0,12 Prozentpunkte

Die **alten** Zahlen waren an die Sortierimplementierung gebunden: welche
Vertauschung Quicksort wählt, hängt an Feldlänge, Feldinhalt und
numpy-Version. Zwei Rechner mit verschiedenen pandas-Ständen konnten für
dieselbe Kurve verschiedene Drawdowns ausweisen, ohne dass irgendetwas
kaputt gewesen wäre.

Die **neuen** Zahlen sind das nicht mehr. Eine stabile Sortierung ist
definiert, nicht implementierungsabhängig: sie liefert auf jeder
pandas-Version dieselbe Reihenfolge. Ab jetzt ist eine Abweichung in
diesen Zahlen ein Befund und nicht mehr möglicherweise nur eine andere
Umgebung.

*Messumgebung dieser Aufgabe:* Python 3.11.15, pandas 3.0.5, numpy 2.4.6.
Die Vorher-Werte −9,34 % und −11,29 % sind dort exakt reproduziert worden
— dieselben, die PR #86 ausgewiesen hat.

---

## 6. Prüfungen

| Prüfung | Ergebnis |
|---|---|
| `shared/test_stabile_sortierung.py` (neu) | **46 von 46** |
| `shared/ergebniskurven.py` | **9x AKTUELL** |
| Wiederholbarkeit: beide Skripte zweimal | byteweise identisch |
| Bestehende Selbsttests | siehe Übergabe-Zusammenfassung (Basislauf auf unverändertem `main` zum Vergleich) |

Der neue Test prüft **Verhalten, nicht Quelltext**: er ruft die echten
Funktionen auf und weist an **mutierten Kopien** nach, dass er rot werden
kann. Einzelheiten im Testauftrag.
