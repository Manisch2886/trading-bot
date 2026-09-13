# Testauftrag TB-28 — Die Messkette an einer Stelle

**Stand: 2026-09-13.** Dieses Dokument ist **eigenständig ausführbar**: alles
Nötige steht hier, es ist kein anderes Dokument zu lesen. Ergebnisbericht:
`docs/ERGEBNIS_TB-28_messkette.md`.

**Was geprüft wird:** dass `shared/messkette.py` die Messkette an eine Stelle
zieht, **ohne eine einzige Zahl zu ändern** — und dass die Abhängigkeiten,
die TB-27 als tragend benannt hat, weiter tragen.

**Voraussetzungen:** Python 3.9+, `pandas`, `numpy`, die Kursdaten unter
`data/`. Alle Befehle werden **aus dem Projektwurzelverzeichnis** gestartet.
Nichts davon sendet eine Order, schreibt in eine Bot-Datenbank oder verändert
`results/`.

---

## 0. Vorbereitung — der Basislauf auf unverändertem `main`

Mehrere Prüfungen dieses Repos schlagen **vorbestehend** fehl. Ohne einen
Basislauf ist hinterher nicht zu unterscheiden, was TB-28 verursacht hat und
was schon vorher so war.

```bash
git stash push -u          # die TB-28-Änderungen beiseitelegen
python3 shared/ergebniskurven.py --json /tmp/kurven_basis.json > /tmp/kurven_basis.txt; echo "RC=$?"
python3 research/parameter_doku/pruefe_fundstellen.py | tail -5; echo "RC=$?"
git stash pop              # zurückholen
```

**Erwartet auf `main`:**

| Prüfung | Rückgabewert | Meldung |
|---|---|---|
| `shared/ergebniskurven.py` | **1** | `Zusammenfassung: 9x ABWEICHEND` |
| `pruefe_fundstellen.py` | **1** | `35/38 Pruefungen bestanden.` |

Beide Befunde sind **vorbestehend**. Der erste, weil TB-26 (`f6d9a28`,
13.09.) die Zuteilungskaskade aller neun Bots geändert hat, die abgelegten
Kurven aber zuletzt am 12.09. (`0d1693e`) erneuert wurden. Der zweite, weil
dieselbe Änderung drei dokumentierte Zeilennummern verschoben hat.

Fehlen `binance`, `yfinance`, `scipy`, `fastapi` oder die Zeitzone
`US/Eastern`, schlagen einzelne Prüfungen zusätzlich umgebungsbedingt fehl;
ohne `node` meldet `dashboard/test_dashboard.py` 780/780 statt 784/784. Auch
das zeigt der Basislauf.

---

## 1. Die Hauptzusicherung: es ändert sich keine Zahl

### 1.1 Der Bericht von `ergebniskurven.py` ist derselbe

```bash
python3 shared/ergebniskurven.py --json /tmp/kurven_tb28.json > /tmp/kurven_tb28.txt; echo "RC=$?"
diff /tmp/kurven_basis.json /tmp/kurven_tb28.json && echo "BERICHT IDENTISCH"
```

**Erwartet:** Rückgabewert **1**, `Zusammenfassung: 9x ABWEICHEND`, und
`BERICHT IDENTISCH`. Der Rückgabewert 1 ist der **vorbestehende** Befund aus
Abschnitt 0 — dass er sich nicht verändert hat, ist genau die Zusicherung.

> **Warum nicht `9x AKTUELL`?** Weil `main` das auch nicht meldet. Die
> abgelegten Kurven passen seit TB-26 nicht mehr zur heutigen Konfiguration.
> `9x AKTUELL` würde nur sagen, dass neue und abgelegte Kurve zueinander
> passen; der Vergleich der beiden Berichte sagt mehr, nämlich dass sich in
> den **neu gerechneten** Kurven nichts bewegt hat.

### 1.2 Die neun Kurven sind byte-gleich

Der strengere Nachweis. Er rechnet jede der neun Kurven zweimal — einmal auf
`main`, einmal mit TB-28 — und vergleicht die Dateien.

```bash
cat > /tmp/schnappschuss.py <<'PY'
import hashlib, os, subprocess, sys
BASE = os.getcwd(); ZIEL = os.path.abspath(sys.argv[1])
bots = sorted(n for n in os.listdir(os.path.join(BASE, "strategies"))
              if os.path.exists(os.path.join(BASE, "strategies", n, "equity_simulation.py")))
for bot in bots:
    ordner = os.path.join(ZIEL, bot); os.makedirs(ordner, exist_ok=True)
    lauf = subprocess.run([sys.executable, "shared/kurven_lauf.py", bot, ordner],
                          capture_output=True, text=True, cwd=BASE)
    open(os.path.join(ordner, "stdout.txt"), "w").write(lauf.stdout)
    kurve = os.path.join(ordner, "equity_curve.csv")
    h = hashlib.sha256(open(kurve, "rb").read()).hexdigest()[:16] if os.path.exists(kurve) else "FEHLT"
    print(f"{bot:30s} rc={lauf.returncode} sha={h}")
PY

python3 /tmp/schnappschuss.py /tmp/tb28_nachher
git stash push -u
python3 /tmp/schnappschuss.py /tmp/tb28_vorher
git stash pop

for b in $(ls /tmp/tb28_vorher); do
  cmp -s /tmp/tb28_vorher/$b/equity_curve.csv /tmp/tb28_nachher/$b/equity_curve.csv \
    && echo "$b: KURVE IDENTISCH" || echo "$b: ABWEICHEND"
done
```

**Erwartet:** neunmal `KURVE IDENTISCH`, und die SHA-256-Anfänge stimmen mit
dieser Tabelle überein:

| Bot | SHA-256 (16 Stellen) | Zeilen | Rendite | Max DD |
|---|---|---:|---:|---:|
| `elliott_wave` | `0ac94d2a2aeb9cd4` | 130 | 67,77 % | −10,17 % |
| `elliott_wave_stocks` | `7ab94aa92332eeaf` | 394 | 419,07 % | −22,97 % |
| `rsi2_crypto` | `bce76ccd78ab1c2b` | 392 | 27,19 % | −13,94 % |
| `rsi2_mean_reversion` | `ef362dd66c514945` | 4218 | 36,28 % | −19,53 % |
| `t3_supertrend` | `cacc20ffe5ae4668` | 656 | 121,70 % | −22,40 % |
| `turtle_soup_crypto` | `224d2f30371863cc` | 1415 | 152,84 % | −34,85 % |
| `turtle_soup_stocks` | `f2a7bab7c446848d` | 8914 | 138,15 % | −29,07 % |
| `volatility_breakout` | `fb38978a45d9207e` | 1461 | 209,59 % | −22,46 % |
| `volatility_breakout_crypto` | `5902183834626c10` | 207 | 68,13 % | −16,29 % |

> Die Hashes gelten für den Datenbestand vom 13.09.2026. Kommen Kursdaten
> hinzu, ändern sie sich — dann zählt allein der **Vergleich vorher gegen
> nachher**, nicht der Abgleich mit dieser Tabelle.

Auch die Bildschirmausgabe je Bot ist identisch, bis auf die gemessene
Rechenzeit:

```bash
for b in $(ls /tmp/tb28_vorher); do
  diff <(sed 's#/tmp/tb28_vorher#P#g;/^  Rechenzeit:/d' /tmp/tb28_vorher/$b/stdout.txt) \
       <(sed 's#/tmp/tb28_nachher#P#g;/^  Rechenzeit:/d' /tmp/tb28_nachher/$b/stdout.txt) \
    > /dev/null && echo "$b: AUSGABE IDENTISCH" || echo "$b: AUSGABE ABWEICHEND"
done
```

**Erwartet:** neunmal `AUSGABE IDENTISCH`.

### 1.3 Der Determinismus-Test

```bash
python3 shared/determinismus.py --schnell; echo "RC=$?"
```

**Erwartet:** Rückgabewert **0** und neunmal `DETERMINISTISCH`, mit exakt den
Renditen und Drawdowns aus der Tabelle in 1.2. Laufzeit rund 100 Sekunden.

---

## 2. Der neue Selbsttest

```bash
python3 shared/test_messkette.py; echo "RC=$?"
```

**Erwartet:** `93/93 Pruefungen bestanden.`, Rückgabewert **0**. Laufzeit rund
17 Sekunden (`--schnell` lässt Teil E weg und braucht rund 9).

Was er im Einzelnen nachweist:

| Teil | Nachweis |
|---|---|
| **A** | Die gemeinsame Fassung liefert auf acht Kurvenformen dieselben Zahlen wie die **bis TB-27 gültige Formel**, die dort wörtlich hinterlegt ist. Inklusive der Stelle, an der die Formel schon einmal falsch sein könnte: ein Verlust im **ersten** Trade zählt mit (−10,0 statt 0,0). |
| **B** | `ergebniskurven.py::kennzahlen()` und die Bot-Fassung melden denselben Drawdown und dieselbe Rendite — und die **drei bewusst belassenen Unterschiede** (Typ, `pd.to_numeric`, leere Kurve) sind festgehalten, nicht wegdefiniert. |
| **C** | **Die Mutationsprobe.** Wird `shared/messkette.py` verfälscht, rechnet **jeder** der neun Bots verfälscht mit. |
| **D1** | Die **Signaturabfrage**: `inspect.signature` und `co_varnames` sagen für alle neun dasselbe, und genau **ein** Bot hat kein `max_concurrent_positions` — `elliott_wave`. |
| **D2** | Der **schreibende** Weg: `notifications/manual_close.py::allokation()` liefert für alle neun einen Anteil, und für `elliott_wave`, `elliott_wave_stocks`, `t3_supertrend` weiterhin aus `equity_simulation.py` (ihre `live_params.py` führt den Wert nicht). |
| **D3** | Es sind weiterhin **neun** `equity_simulation.py` an ihren Pfaden — die Bot-Liste dreier Werkzeuge hängt daran. |
| **E** | Auch der **`__main__`-Block** dreier Bots rechnet mit der gemeinsamen Fassung: die gedruckte Gesamtrendite und der gedruckte Max Drawdown tragen die Mutationsmarke. |

### 2.1 Die Mutationsprobe von Hand nachvollziehen

Eine Probe, die man nicht scheitern gesehen hat, ist keine. So sieht man sie
scheitern — ein Bot bekommt seine eigene Kopie zurück:

```bash
python3 - <<'PY'
p = "strategies/turtle_soup_crypto/equity_simulation.py"
t = open(p).read()
open(p + ".bak", "w").write(t)
open(p, "w").write(t.replace('if __name__ == "__main__":', '''def calculate_max_drawdown(equity_df, starting_capital):
    if equity_df.empty:
        return 0.0
    import pandas as pd
    s = pd.concat([pd.Series([starting_capital]), equity_df["capital_after"]], ignore_index=True)
    return round(((s - s.cummax()) / s.cummax() * 100).min(), 2)


if __name__ == "__main__":''', 1))
PY

python3 shared/test_messkette.py --schnell | tail -4; echo "RC=$?"
mv strategies/turtle_soup_crypto/equity_simulation.py.bak strategies/turtle_soup_crypto/equity_simulation.py
```

**Erwartet:** Rückgabewert **1** und **genau eine** gescheiterte Prüfung:

```
  - turtle_soup_crypto: mit Mutation traegt der Drawdown die Marke (-10.0 + 7.77)
```

Die zurückgebaute Kopie rechnet richtig — sie ist ja zeichengleich zur
gemeinsamen Fassung. Trotzdem meldet der Test rot, und das ist der Punkt:
geprüft wird nicht „rechnet es richtig", sondern **„steht es an einer
Stelle"**.

Danach muss `git status` wieder sauber sein (nur die TB-28-Änderungen).

> **Warum die Probe so gebaut ist.** Zwei Fallen sind in diesem Projekt
> wiederholt aufgetreten (#73, #77, #78, #79, #81, #86, TB-15, TB-20, TB-22,
> TB-26) — und der Wächter aus TB-27 ist der ersten in genau dieser Änderung
> selbst zum Opfer gefallen:
>
> 1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestätigt sich
>    selbst.** `test_vergleich.py` verfälschte bis TB-28 die Zeile
>    `capital_series.cummax()` in einer Kopie der neun Dateien. Diese Zeile
>    ist durch TB-28 aus den neun Dateien verschwunden — die Verfälschung
>    hätte ins Leere gegriffen, der Test wäre grün geblieben. Aufgefallen ist
>    es **nur**, weil jene Probe den Ablauf beobachtet
>    (`pruefe("die Verfaelschung greift ueberhaupt", ...)`). Deshalb belegt in
>    `test_messkette.py` jede Mutationsprobe **beide** Richtungen: ohne
>    Mutation den echten Wert, mit Mutation die Marke.
> 2. **Eine zweite Wache verdeckt das Fehlen der ersten.** Deshalb läuft jede
>    Bot-Probe in einem **eigenen Unterprozess** mit **einer** Frage, und die
>    Zusicherung „es ist eine Stelle" wird **nicht** über den Quelltext
>    gestützt — kein `grep` auf `from messkette import`, kein AST-Vergleich.
>    Ein Quelltext-Beleg bliebe grün, auch wenn der Import wirkungslos wäre.
>    Geprüft wird ausschliesslich, welche Zahl herauskommt.

---

## 3. Der Wächter aus TB-27

Er **musste** anschlagen: `calculate_max_drawdown` ist nicht mehr Teil der
neun Dateien. Sein Grundzustand ist nachgezogen.

```bash
python3 research/tb27_kapitalsimulation/vergleich.py --pruefen; echo "RC=$?"
python3 research/tb27_kapitalsimulation/test_vergleich.py | tail -3; echo "RC=$?"
python3 research/tb27_kapitalsimulation/vergleich.py | sed -n '/GRUPPEN/,/^$/p'
```

**Erwartet:**

* `UNVERAENDERT gegenueber dem Stand TB-27 (13.09.2026). 4 Funktionen ueber 9
  Bots geprueft.`, Rückgabewert 0 — **vier** statt vorher fünf Funktionen.
* `23/23 bestanden.`, Rückgabewert 0.
* In der Gruppenübersicht kommt `calculate_max_drawdown` **nicht mehr vor**;
  `simulate_portfolio (2 Gruppen)`, `collect_all_trades (9 Gruppen)`,
  `__main__ (8 Gruppen)`, `apply_btc_regime_filter (1 Gruppe)` bleiben
  unverändert.

**Was sich am Wächter verschoben hat:**

| | vorher | nachher |
|---|---|---|
| `ERWARTUNG` in `vergleich.py` | fünf Einträge, darunter `calculate_max_drawdown` mit allen neun Bots | vier Einträge; der Eintrag ist mit Begründung entfallen |
| Probe „stille Divergenz" in `test_vergleich.py` | `capital_series.cummax()` → `.expanding().max()` in `calculate_max_drawdown` | Positionslimit still fallen lassen (`max_concurrent_positions` → `None`) in `simulate_portfolio` |
| Probe „harmloser Kommentar" | im Rumpf von `calculate_max_drawdown` | im Rumpf von `simulate_portfolio` |
| Selbsttest-Prüfung 1 | „`calculate_max_drawdown` steht als **eine** Gruppe da" | „`calculate_max_drawdown` wird in keiner der neun Dateien mehr **definiert**" |

Die Renditeformel steht nicht in `ERWARTUNG` — sie ist keine Funktion,
sondern eine Zeile im `__main__`-Block. Dessen Gruppierung (acht Gruppen) ist
unverändert.

---

## 4. Die reparierten Zeilennummern

```bash
python3 research/parameter_doku/pruefe_fundstellen.py | tail -3; echo "RC=$?"
```

**Erwartet:** `38/38 Pruefungen bestanden.`, Rückgabewert **0** — gegenüber
`35/38`, RC 1 im Basislauf.

Dass die Zahlen an beiden Stellen stimmen, prüft man so:

```bash
grep -n "equity_simulation.py:" strategies/*/live_params.py
sed -n '78p' strategies/t3_supertrend/equity_simulation.py
sed -n '151p' strategies/volatility_breakout/equity_simulation.py
sed -n '166p' strategies/volatility_breakout_crypto/equity_simulation.py
```

**Erwartet:** die drei Kommentare nennen `:78`, `:151`, `:166`, und in genau
diesen Zeilen stehen `compute_btc_regime(...)` bzw.
`collect_all_trades(all_data, STOP_LOSS_PCT)`.

---

## 5. Alle übrigen Tests

```bash
python3 shared/test_ergebniskurven.py   | tail -2; echo "RC=$?"
python3 shared/test_determinismus.py    | tail -2; echo "RC=$?"
python3 shared/test_zuteilung.py        | tail -4; echo "RC=$?"
python3 notifications/test_manual_close.py | tail -2; echo "RC=$?"
python3 dashboard/test_dashboard.py     | tail -2; echo "RC=$?"
```

**Erwartet**, jeweils Rückgabewert **0**:

| Test | Meldung |
|---|---|
| `shared/test_ergebniskurven.py` | `44 von 44 Pruefungen bestanden` |
| `shared/test_determinismus.py` | `Ergebnis: 54 bestanden, 0 fehlgeschlagen` |
| `shared/test_zuteilung.py` | `65 bestanden, 0 fehlgeschlagen, 2 ausgelassen` — die beiden Auslassungen betreffen `elliott_wave` und `t3_supertrend` und kommen davon, dass `shared/fetch_binance_data.py` gitignored ist. Auf dem Rechner des Nutzers liegt die Datei, dort laufen sie mit und die Zahl ist entsprechend höher. **0 fehlgeschlagen** ist das, worauf es ankommt. |
| `notifications/test_manual_close.py` | `118 Pruefungen bestanden, 0 fehlgeschlagen` |
| `dashboard/test_dashboard.py` | `784/784` (ohne `node`: `780/780`) |

---

## 6. Was diese Änderung **nicht** getan hat — zum Gegenprüfen

```bash
git diff --stat main
```

**Erwartet:** kein Treffer für `multi_symbol_optimise.py`,
`multi_symbol_walk_forward.py`, `optimise_*.py`, `forward_test.py`,
`shared/zuteilung.py`, `results/`, `broker/`, `config/`.

Die drei `live_params.py` erscheinen mit je **einer** geänderten Zeile. Dass
es reine Kommentarzeilen sind:

```bash
git diff main -- strategies/*/live_params.py | grep "^[+-]" | grep -v "^[+-][+-]"
```

**Erwartet:** ausschliesslich Zeilen, die mit `+#` oder `-#` beginnen. Kein
Handelsparameter ist berührt.

Dass die abgelegten Kurven unangetastet sind:

```bash
git status --short results/
```

**Erwartet:** leere Ausgabe.
