# Übergabe: Kurslücken im Trade-Pfad (APH-Befund)

**Branch** `claude/new-session-uqjk8h`, Basis `origin/main` (`94e0d7f`, nach
Merge von #80). **PR #81.**

---

## Zuerst die Frage, die der Auftrag an den Anfang stellt

> *Falls sich eine Kennzahl ändert, auf deren Grundlage ein Bot aktiviert
> wurde, gehört das ausdrücklich an den Anfang.*

**Sie ändert sich nicht.** Über alle 147 verwertbaren Aktien-Symbole, mit der
Live-Kombination von `elliott_wave_stocks` (Zigzag 5,0 / Stop 3,0 / Fib 0,236):

| Kennzahl | vorher | nachher |
|---|---|---|
| Trades | 510 | 510 |
| davon mit NaN | 0 | 0 |
| Trefferquote | 31,57 % | 31,57 % |
| Ø Rendite je Trade | 1,3505 % | 1,3505 % |
| Summe der Trade-Renditen | 688,77 % | 688,77 % |
| Endkapital (Kapitalsimulation) | 17.197,86 | 17.197,86 |

Der vergiftete Trade entsteht nur bei Parameterkombinationen, die **nicht** live
sind. Keine Live-Zahl, keine Aktivierungsentscheidung und kein
`live_params.py`-Eintrag ist betroffen.

Was sich ändert, steht in Abschnitt 4 — und dort ändert sich Wesentliches:
aus `nan` wird eine Zahl.

---

## 1. Ist-Zustand — belegt, nicht angenommen

### Wo genau entsteht das NaN

`strategies/elliott_wave_stocks/backtest_elliott.py`, Zeile 110, im
Zeitausstieg:

```python
return {"exit_time": last_row["open_time"], "exit_price": last_row["close"],
        "result": "time_exit"}
```

Steht in `last_row["close"]` ein NaN, wird daraus `exit_price = NaN` und
anschliessend `pnl_pct = NaN`.

Die drei anderen Aktien-Bots haben denselben Bau: ihr Zeitausstieg rechnet mit
`max_offset = min(max_hold_days, n - 1 - i)` und kann damit ebenfalls auf der
letzten Kerze landen.

### Wie weit der Schaden reicht — weiter als der Bericht sagt

`equity_simulation.simulate_portfolio` rechnet im Exit-Zweig

```python
pnl_pct = trade["pnl_pct"]
result_value = allocation * (1 + pnl_pct / 100)
capital += (result_value - allocation)
```

`capital` ist danach NaN — und bleibt es. **Jeder folgende Trade erbt das NaN.**
Gemessen an drei Trades, bei denen nur der mittlere kaputt ist: 2 von 3
Kapitalzeilen unbrauchbar, `final_capital` = `nan`, und `num_executed` zählt den
kaputten Trade trotzdem als ausgeführt. Steht das NaN am Anfang, ist die ganze
Kurve hin.

Der Bericht nannte „NaN als Portfolio-Rendite". Tatsächlich ist es keine
einzelne kaputte Zahl, sondern eine Kette.

### Welche Symbole betroffen sind

Alle 242 Kursdateien durchgesehen:

| | Dateien | mit unvollständiger Kerze |
|---|---|---|
| Aktien (Tageskerzen) | 150 | **1** — `APH`, genau **1** Zeile |
| Krypto (Tageskerzen) | 24 | 0 |

Die betroffene Zeile ist die **letzte**: `2026-09-01`, Datum und Volumen
(7.650.337) vorhanden, alle vier Kurswerte leer. Alle 150 Aktien-Dateien enden
auf dieses Datum; nur bei `APH` kam der Kurs nicht mit.

### Welche Bots es in der Praxis trifft

| Bot | geprüfte Kombinationen | mit NaN-Trade |
|---|---|---|
| `elliott_wave_stocks` | 48 (das offizielle Raster) | **24** |
| `rsi2_mean_reversion` | 4 | 0 |
| `turtle_soup_stocks` | 12 | 0 |
| `volatility_breakout` | 3 | 0 |

**Die Hälfte des Suchrasters** des Aktien-Elliott-Bots erzeugt den Trade. Bei
den anderen dreien heute nicht: ihr `entry_cutoff` hält Einstiege vom Rand der
Daten fern, sodass kein Zeitausstieg die letzte Kerze erreicht. Das ist eine
Eigenschaft ihrer heutigen Parameter, keine Absicherung — strukturell sind sie
demselben Fehler ausgesetzt und werden deshalb mit abgesichert.

### Wo das NaN unbemerkt verschwindet

Drei Stellen, in **jedem** der neun `multi_symbol_optimise.py`:

| Stelle | Verhalten |
|---|---|
| `avg_return = combined["pnl_pct"].mean()` | überspringt NaN (pandas-Voreinstellung) |
| `total_return = combined["pnl_pct"].sum()` | ebenso |
| `win_rate = (combined["pnl_pct"] > 0).mean()` | **`NaN > 0` ist `False`** — der kaputte Trade zählt als **Verlierer** |

Die dritte ist die unangenehmste, weil sie nicht nur verschweigt, sondern
verfälscht. An einem Beispiel mit vier Trades sinkt die Trefferquote dadurch von
66,7 % auf 50,0 %, ohne jeden Hinweis. Real gemessen: 55,35 % → 55,08 %.

### Wie `buy_and_hold_benchmark.py` es richtig macht

```python
if pd.isna(entry_price) or pd.isna(exit_price) or entry_price == 0:
    skipped_symbols.append(symbol)
    continue
...
if skipped_symbols:
    print(f"Hinweis: {len(skipped_symbols)} Aktie(n) wegen fehlerhafter "
          f"Kursdaten uebersprungen: {skipped_symbols}")
```

**Streichen und zählen, mit Meldung.** Genau dieses Muster wird hier
verallgemeinert — es ist keine zweite Erfindung.

---

## 2. Die Behandlung

Neu: `shared/kursdaten.py` — eine Stelle, an der definiert ist, was eine
unvollständige Kerze ist und was mit ihr geschieht.

* `unvollstaendige_maske(df)` — eine Kerze gilt als unvollständig, sobald
  **eine** der vier Kursspalten fehlt. Das Volumen zählt bewusst **nicht** mit:
  eine Kerze ohne Volumen, aber mit Kursen beschreibt einen handelbaren Zustand,
  eine ohne Kurse nicht. Genau so liegt der APH-Fall.
* `entferne_unvollstaendige(df, symbol)` → `(bereinigt, anzahl)` — streicht
  **und zählt**.
* `Zaehler` — sammelt die Streichungen eines Ladevorgangs zu **einer** Zeile
  mit Gesamtzahl und Symbolnamen.

### Eingebaut an zwei Stellen, beide so früh wie möglich

**1. `fetch_stock_data.fetch_historical_data` (4 Aktien-Bots, byte-identisch).**
Diese Funktion schreibt die CSVs **und** versorgt `forward_test.py` live. Die
Absicherung dort behebt den Live-Pfad, **ohne `forward_test.py` anzufassen** —
das ist der Grund für diese Wahl und nicht ein Zufall.

**2. `multi_symbol_optimise.load_all_symbol_data` (alle 9 Bots).** Für die
bereits vorhandenen CSVs, die die Lücke noch enthalten. Eingesetzt direkt nach
`pd.read_csv`, also vor jeder anderen Verarbeitung.

Alle neun statt nur der vier Aktien-Bots: die Krypto-Daten sind heute sauber,
aber eine Wache, die nur an manchen Stellen steht, ist genau das Muster, das in
diesem Projekt schon mehrfach einen Fehler verdeckt hat.

### Warum nicht in `equity_simulation.py`

Dort schlägt der Fehler zu, dort entsteht er nicht. Eine Absicherung an der
Wirkung statt an der Ursache hätte drei Nachteile: sie müsste in neun
gleichnamigen Dateien stehen, sie käme zu spät (die Trefferquote wäre schon
verfälscht), und sie würde einen Zustand tolerieren, den es nicht geben sollte.
Die Datei ist deshalb **unverändert** — ein Test prüft das gegen `origin/main`.

**Als Beobachtung weitergereicht, nicht umgesetzt:** `simulate_portfolio`
verarbeitet einen NaN heute stillschweigend weiter. Käme je ein NaN aus einer
anderen Richtung — etwa aus einer Live-Datenbank, in die `forward_test.py` vor
dieser Änderung ein NaN geschrieben hat —, wäre die Kapitalkurve wieder hin, und
seit PR #80 zeigt das Dashboard diese Kurve an. Eine Abweisung dort wäre eine
eigene, kleine Entscheidung des Nutzers.

---

## 3. Dafür sorgen, dass es auffällt

Der eigentliche Schaden war nicht die Lücke, sondern dass niemand sie bemerkt
hat. Drei Wege, bewusst gestaffelt:

1. **Beim Laden** — eine Zeile in der Ausgabe jedes Optimierungslaufs:
   `Datenqualitaet: insgesamt 1 unvollstaendige Kerze(n) in 1 Symbol(en)
   gestrichen - APH (1). Diese Kerzen gehen in KEINE Kennzahl ein.`
2. **Beim Holen** — eine Zeile je Symbol, sobald yfinance eine leere Kerze
   liefert. Sie erscheint damit auch im Cronjob-Log des Live-Bots.
3. **Als eigenes Werkzeug** — `python3 shared/kursdaten.py` durchsucht alle
   Kursdateien und meldet jeden Befund. **Rückgabewert 1 bei Befund**, damit ein
   Cronjob-Aufruf ihn sichtbar macht, statt ihn im Log zu begraben.

---

## 4. Was sich dadurch ändert — und um wie viel

Gemessen über alle 147 Symbole, jeweils vorher/nachher:

| Kombination | Kennzahl | vorher | nachher |
|---|---|---|---|
| **LIVE** (5,0 / 3,0) | alle | — | **unverändert** |
| Befund (6,0 / 16,0, ohne Ziel) | Endkapital | **`nan`** | **59.939,87** |
| | Trefferquote | 55,08 % | 55,35 % |
| | Ø Rendite | 10,1375 % | 10,1823 % |
| | Summe | 3781,30 % | 3808,17 % |
| Nachbar (3,0 / 3,0) | Endkapital | **`nan`** | **17.682,96** |
| | Ø Rendite | 0,5797 % | 0,5788 % |
| | Summe | 664,93 % | 664,49 % |

Die Trefferquote **steigt** in beiden Fällen — der kaputte Trade wurde vorher
als Verlierer gezählt. Die Trade-Zahl bleibt überall gleich: der Trade
verschwindet nicht, er endet nur eine Kerze früher und bekommt ein echtes
Ergebnis (im Befund-Fall +26,87 % statt NaN).

### Ein Nebeneffekt, der benannt gehört

Die Zeilenzahl von `APH` bleibt bei **2513** — nicht 2512. Grund: der
10-Jahres-Filter (`RECENT_YEARS_ONLY`) richtet sein Fenster am **letzten** Datum
aus. Fällt die leere Kerze weg, beginnt das Fenster einen Tag früher und nimmt
vorn eine Zeile auf (`2026-09-01` raus, `2016-08-31` rein).

Das ist vertretbar und sogar sauberer — das Fenster hängt jetzt an der letzten
**echten** Kerze. Erwähnenswert ist es trotzdem, denn eine Prüfung auf
„eine Zeile weniger" wäre grün gewesen, ohne etwas zu zeigen. Der Selbsttest
prüft deshalb das Ende der Reihe, nicht die Zeilenzahl.

---

## 5. Wohin der Befund gehört

**Nicht** in `docs/DATENLUECKEN.md`. Dort stehen Ausfälle, bei denen ein Bot
**gar nicht lief** (schlafender Mac, Cron holt nichts nach) — fehlende
*Läufe*. Hier lief alles, die **Kursdaten** waren löchrig. Andere Fehlerklasse,
andere Abhilfe, andere Zuständigkeit.

Damit die beiden nicht verwechselt werden, steht in `DATENLUECKEN.md` jetzt eine
kurze Abgrenzung mit Verweis auf `shared/kursdaten.py` — und nur die.

---

## 6. Tests

`python3 shared/test_kursdaten.py` — **83 Prüfungen**, 10 Abschnitte.

Der Kern ist Abschnitt 4: der NaN-Fall wird **erzeugt**, indem der echte
Bot-Loader einmal mit und einmal ohne die Absicherung läuft — in getrennten
Prozessen, weil neun Bots gleichnamige Module haben. Beobachtet wird der
**Ablauf**: entstehen NaN-Trades (ohne: **8**, mit: **0**), wird gezählt, wird
gemeldet.

Abschnitt 5 ist die Gegenprobe an einem Symbol **ohne** Lücke (`AAPL`): über
alle Kombinationen dieselben Trades, Fingerabdruck für Fingerabdruck — plus die
Prüfung, dass überhaupt Trades entstanden sind, damit der Vergleich nicht leer
gegen leer läuft.

Abschnitt 9 prüft den Holer am Verhalten, mit einer yfinance-Attrappe, die genau
den APH-Fall liefert. Das war nötig: eine Textsuche bliebe grün, wenn der
Aufruf zwar dasteht, sein Ergebnis aber verworfen wird — und genau diese
Mutation (M14) ist nur hier aufgefallen.

**14 Mutationsproben, alle 14 erkannt.**

Keine Regression: `dashboard/test_dashboard.py` 784/784,
`dashboard/test_portfolio_sicht.py` 90/90,
`notifications/test_schliess_benachrichtigung.py` 99/99,
`system/test_log_rotation.py` 117/117, `broker/test_broker.py` 163,
`broker/test_ibkr.py` 200, `shared/test_empfehlung_format.py` 70/70,
`system/test_caffeinate_plist.py` 52/52, `notifications/test_manual_close.py`
alle.

---

## 7. Was nicht angefasst wurde

`live_params.py`, `forward_test.py`, `equity_simulation.py` — keine einzige.
Nichts unter `broker/`, keine Crontab, keine launchd-Vorlage. **Keine
Kursdatei**: `data/APH_1d.csv` behält ihre leere Zeile, damit das Repo ein
echtes Beispiel des Fehlers enthält, an dem sich die Absicherung prüfen lässt.
Keine Backtest-Ergebnisse überschrieben. Alles vier per `git diff` gegen
`origin/main` im Selbsttest geprüft.

## 8. Offene Punkte

* **Die Ursache liegt bei yfinance**, nicht im Projekt: die Zeile kam mit Datum
  und Volumen, aber ohne Kurse. Ob das ein wiederkehrendes Muster ist (Feiertag,
  Handelsunterbrechung, verspätete Konsolidierung), ist offen — das Werkzeug aus
  Abschnitt 3 macht es künftig messbar.
* **`simulate_portfolio` toleriert ein NaN weiterhin** (Abschnitt 2, letzter
  Absatz) — bewusst nicht geändert, als Entscheidung weitergereicht.
* **Die drei anderen Aktien-Bots sind heute nur durch ihren `entry_cutoff`
  geschützt**, nicht durch eine Absicherung in ihrem eigenen Ausstiegspfad. Die
  Datenabsicherung deckt das ab; ändert jemand den Cutoff, bleibt sie die
  einzige Wache.
