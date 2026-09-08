# `elliott_wave_stocks`: Positionslimit in der OOS-Simulation nachgetragen

**Stand:** 2026-09-08 · **Branch:** `claude/oos-positionslimit`
**Ausgangspunkt:** Nebenbefund aus PR #47

---

## Kurzfassung

| | |
|---|---|
| Betroffen | `strategies/elliott_wave_stocks/oos_equity_simulation.py`, eine Aufrufstelle |
| Vorher | +70,37 % · −10,11 % MaxDD · Calmar 6,96 · 120 ausgeführt / 8 übersprungen |
| Nachher | **+72,39 %** · **−9,69 %** MaxDD · **Calmar 7,47** · 114 ausgeführt / 14 übersprungen |
| Vom Limit betroffen | **14 von 128 Trades (10,9 %)** — meine frühere Schätzung „8 von 128" war eine **Unterschätzung** |
| Kernaussage zur Take-Profit-Entscheidung | **unverändert** |
| `elliott_wave` (Krypto) | nicht betroffen — und zwar aus inhaltlichem Grund |
| `forward_test.py` / `live_params.py` | unverändert |

---

## 1. Der Fix

```python
from live_params import MAX_CONCURRENT_POSITIONS
...
result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT,
                             MAX_CONCURRENT_POSITIONS)
```

Der Wert kommt per **Import** aus `live_params.py`, nicht aus dem In-Sample-Gewinner:
`MAX_CONCURRENT_POSITIONS` ist kein Parameter des Suchrasters, sondern eine feste
Eigenschaft des laufenden Bots. Genau so macht es `equity_simulation.py:195` seit jeher.

**Zweite, kleinere Korrektur in derselben Datei.** Die Ausgabezeile lautete pauschal
„Übersprungene Trades: N (nicht genug freies Kapital)". Seit das Limit übergeben wird,
ist das die falsche Hälfte der Wahrheit — im gemessenen Lauf war ausnahmslos das
**Limit** der Grund, kein einziges Mal das Kapital. Die Zeile nennt jetzt beide Gründe.

---

## 2. Vorher/Nachher

| Kennzahl | Vorher (ohne Limit) | Nachher (Limit 8) | Δ |
|---|---|---|---|
| Endkapital (Start 10.000) | 17.036,74 | 17.239,11 | +202,37 |
| **Gesamtrendite** | +70,37 % | **+72,39 %** | **+2,02 pp** |
| **Max Drawdown** | −10,11 % | **−9,69 %** | **+0,42 pp (besser)** |
| **Calmar** | 6,96 | **7,47** | +0,51 |
| Trades gefunden | 128 | 128 | 0 |
| ausgeführt | 120 | 114 | −6 |
| übersprungen | 8 | 14 | +6 |

Der Vorher-Lauf reproduziert die Zahlen aus der letzten Übergabe **exakt** (+70,37 %,
−10,11 %, Calmar 6,96, 128/120/8) — sie wurden nachgerechnet, nicht übernommen.

**Regressionsnachweis, schärfer als `git diff`:** die Trade-Tabelle wird in beiden
Läufen gehasht. Beide Läufe: `277c1c2324422f60`. Die Änderung hat also nachweislich
nur die Portfolio-Ebene berührt — dieselben 128 Trades, derselbe In-Sample-Gewinner
(Zigzag 5,0 % / Stop 2,0 % / kein festes Ziel).

---

## 3. Wie viele Trades betrifft das Limit wirklich? (Frage 4)

`simulate_portfolio()` liefert nur **eine** Zahl übersprungener Trades und unterscheidet
nicht zwischen den beiden Abbruchgründen im Code. Für die Aufschlüsselung wird die
Ereignisschleife in `analyse.py` mit getrennten Zählern nachgebildet — und muss sich
vorher beweisen: sie trifft für **beide** Konfigurationen exakt die Zahlen der echten
Funktion (120/8 bzw. 114/14, Endkapital auf den Cent), sonst bricht das Skript ab.

| | ohne Limit | mit Limit 8 |
|---|---|---|
| ausgeführt | 120 | 114 |
| übersprungen gesamt | 8 | 14 |
| davon **wegen Limit** | 0 | **14** |
| davon **wegen Kapital** | **8** | **0** |
| max. gleichzeitig offen | **9** | 8 |

### Die Antwort — und die Korrektur meiner früheren Schätzung

**14 von 128 Trades (10,9 %) sind vom Limit betroffen, nicht 8.** Meine Einschätzung in
der PR-#47-Übergabe („nur 8 von 128 binden am Kapital, der Effekt dürfte klein sein")
maß die falsche Größe: die 8 waren **Kapital**-Übersprünge des Laufs *ohne* Limit — eine
andere Frage als „wie viele blockiert das Limit". Als Schätzung für die Limit-Wirkung
war sie eine Unterschätzung um Faktor 1,75.

### Der eigentlich interessante Befund

Mit aktivem Limit werden **null** Trades wegen Kapitalmangels übersprungen. Der Grund
ist Arithmetik: 8 Positionen × 10 % Allokation binden höchstens 80 % des Kapitals, es
bleibt also immer freies Kapital übrig. Ohne Limit stieg die Belegung auf **9**
gleichzeitige Positionen — die neunte hätte 90 % gebunden, und genau dort riss das
Kapital acht Mal.

Die beiden Beschränkungen sind hier also keine unabhängigen Effekte, sondern
**Quasi-Substitute**: das Positionslimit greift, bevor die Kapitalgrenze überhaupt
greifen kann. Es ersetzt eine unscharfe, kapitalgetriebene Begrenzung durch eine
explizite — was auch erklärt, warum das Ergebnis trotz sechs Trades weniger nicht
schlechter, sondern leicht besser ausfällt.

---

## 4. Ändert sich die Kernaussage? (Frage 5)

**Nein — in keiner der drei relevanten Hinsichten.**

**a) Die Take-Profit-Entscheidung bleibt unberührt.** Sie hängt daran, welche
Kombination die In-Sample-Optimierung auswählt, und das passiert **oberhalb** der
Portfolio-Ebene. Beweis statt Behauptung: identischer Trades-Hash und identischer
Gewinner in beiden Läufen (Zigzag 5,0 % / Stop 2,0 % / kein festes Ziel). Das
Positionslimit kann daran nichts ändern, weil es erst danach wirkt.

**b) Die Größenordnung bleibt dieselbe.** +70,4 % → +72,4 % ist eine Verschiebung um
2,0 Prozentpunkte auf gut 70 — rund 3 % relativ. Keine Aussage, die auf „etwa +70 %
über den OOS-Zeitraum" beruht, kippt dadurch.

**c) Die Richtung ist günstig, nicht ungünstig.** Rendite leicht höher, Drawdown
leicht geringer, Calmar besser. Das ist keine Beschönigung, sondern der erwartbare
Effekt einer Risikobegrenzung, die in einem gut laufenden Zeitraum wenige Trades kostet
und im Gegenzug die tiefste Auslastung kappt.

**Was sich sehr wohl ändert, ist die Vergleichbarkeit — zum Besseren.** Die OOS-Zahlen
sind jetzt mit `experiment_no_take_profit.py` vergleichbar, das
`MAX_CONCURRENT_POSITIONS` schon immer nutzt. Vorher verglich man ein simuliertes
Portfolio ohne Limit mit einem gemessenen mit Limit.

---

## 5. `elliott_wave` (Krypto) ist nicht betroffen (Frage 6)

Der Grund ist ein anderer als beim Take-Profit-Fund — dort ging es um eine fehlende
Suchdimension, hier um eine bewusste Eigenschaft des Bots:

`elliott_wave/live_params.py` (Zeilen 60–75) hält ausdrücklich fest, dass dieser Bot
**bewusst kein Positionslimit** hat (Verweis auf `research/order_sensitivity`), und dass
es dort zu ergänzen „eine Verhaltensänderung" wäre. `MAX_CONCURRENT_POSITIONS` steht
folgerichtig **nicht** in seiner `live_params.py`.

Entsprechend lassen dort **beide** Aufrufstellen den Parameter konsistent weg:

| Bot | `equity_simulation.py` | `oos_equity_simulation.py` | konsistent? |
|---|---|---|---|
| `elliott_wave` (Krypto) | ohne Limit (`:166`) | ohne Limit (`:73`) | **ja** |
| `elliott_wave_stocks` — vorher | **mit** Limit (`:195`) | **ohne** Limit | **nein** ← der Fehler |
| `elliott_wave_stocks` — nachher | mit Limit | mit Limit | **ja** |

Der Fehler war also nicht „Limit fehlt", sondern „die beiden Simulationen desselben
Bots widersprachen sich".

---

## 6. Nachweise

| Prüfung | Ergebnis |
|---|---|
| Vorher-Lauf reproduziert die Übergabe-Zahlen | exakt (+70,37 % / −10,11 % / 6,96 / 128/120/8) |
| Trades-Hash vorher = nachher | `277c1c2324422f60` = `277c1c2324422f60` |
| `limit_uebergeben` im Mitschnitt | vorher `null`, nachher `8` |
| Nachbild trifft die echte Funktion | beide Konfigurationen, auf den Cent |
| `py_compile` | fehlerfrei |
| `git diff` | nur `oos_equity_simulation.py` (Import, Aufrufstelle, Ausgabezeile) |
| `forward_test.py` / `live_params.py` | keine Treffer im Diff |

---

## 7. Nebenbefund, bewusst nicht angefasst

Dieselbe pauschale Ausgabezeile „(nicht genug freies Kapital)" steht an drei weiteren
Stellen:

- `strategies/elliott_wave_stocks/equity_simulation.py:206` — dort ist sie **schon
  heute falsch**, denn dieses Skript übergibt das Limit seit jeher (`:195`).
- `strategies/elliott_wave/equity_simulation.py:177` und
  `oos_equity_simulation.py:84` — dort ist sie korrekt, weil der Krypto-Bot kein Limit
  kennt.

Der erste Fall wäre eine eigenständige kleine Korrektur außerhalb dieser Aufgabe.

---

## 8. Dateien

| Datei | Zweck |
|---|---|
| `oos_lauf.py` | Vorher-/Nachher-Lauf des echten Skripts, isolierter Prozess, umgeleitete Ergebnispfade, Trade-Mitschnitt samt Hash |
| `analyse.py` | Aufschlüsselung Limit- vs. Kapital-Übersprung, mit vorgeschalteter Treue-Prüfung gegen die echte Funktion |
| `stubs/yfinance.py` | Attrappe — `fetch_stock_data.py` importiert `yfinance` auf Modulebene, obwohl der Lauf nur `INTERVAL` braucht. Ein echter Abruf wirft |
| `results/oos_{vorher,nachher}.json`, `trades_*.csv`, `analyse.json` | Rohdaten |
