# Testauftrag TB-20 — Wellenauswahl

**Autonom ausführbar.** Alles unten läuft ohne Rückfragen, ohne Netzzugriff
und ohne Schreibzugriff auf das Repo. Wer nur eine Zahl braucht: Schritt 1.

    cd <repo-wurzel>
    python3 shared/test_wellenauswahl.py

Erwartet: **`Ergebnis: 323 bestanden, 0 fehlgeschlagen`**, Rückgabewert 0.

---

## 0. Was geprüft wird — und was ausdrücklich nicht

Geprüft wird das **Verhalten** von

    strategies/elliott_wave/elliott_wave_counter.py
    strategies/elliott_wave_stocks/elliott_wave_counter.py

und zwar an den echten Funktionen: `nach_rangfolge`, `remove_overlapping`,
`find_impulse_waves`, `find_causal_waves`.

**Nicht** geprüft wird, ob `kind="stable"` oder `RANGFOLGE` im Quelltext
vorkommt. Eine Textsuche wäre hier besonders wertlos: sie prüft genau das,
was der Diff ohnehin zeigt, und sagt nichts darüber, ob die Zusicherung
trägt. Dass die Proben überhaupt unterscheiden, weist Abschnitt 9 am
**Ablauf** nach, nicht per Behauptung.

### Die geprüfte Zusicherung

    Die Reihenfolge der zurückgegebenen Wellenmuster ist eine Funktion der
    MUSTER — nicht der Zeilenreihenfolge der Eingabe und nicht der
    Sortierimplementierung.

Die Rangfolge dahinter:

| Rang | Kriterium | Richtung | Bedeutung |
|---:|---|---|---|
| 1 | `fib_score` | absteigend | bestes Fibonacci-Urteil zuerst |
| 2 | `end_time` | absteigend | bei Gleichstand das **jüngere** Muster |
| 3 | `start_time` | absteigend | bei gleichem Ende das **kürzere** |

---

## 1. Der Kernlauf

    python3 shared/test_wellenauswahl.py            # 323 Prüfungen, ca. 2 min
    python3 shared/test_wellenauswahl.py --schnell  # 322 Prüfungen, ca. 40 s

`--schnell` lässt Abschnitt 10 (`ergebniskurven.py`, der teure Teil) weg und
verkürzt Abschnitt 8 von 12 auf 4 Symbole je Bot.

Rückgabewert 0 = bestanden, 1 = mindestens eine Prüfung fehlgeschlagen.

### Die Abschnitte und was je einer allein sichert

Die Abschnitte sind so geschnitten, dass **je nur eine Wache greifen kann**.
Das ist der Grund, warum die Abschnitte 1 bis 4 `nach_rangfolge` direkt
aufrufen: Abschnitt 1 braucht Muster, deren `start_time` **gegen** ihre
`end_time` läuft — solche Muster überlappen sich zwangsläufig, und
`remove_overlapping` würde sie vorher zusammenstreichen. Die echten
Einstiegspunkte laufen in den Abschnitten 5 bis 8.

| Abschnitt | Gesicherte Zusicherung | Warum nur diese |
|---|---|---|
| **1** | Gleichstand im `fib_score` → jüngeres Muster zuerst | alle Scores gleich (Rang 1 entscheidet nichts), `end_time` eindeutig (Rang 3 und Stabilität entscheiden nichts). `start_time` läuft **gegen** `end_time`: ohne Rang 2 wäre die Reihenfolge genau umgekehrt |
| **2** | es wird überhaupt nach `fib_score` sortiert | alle Scores verschieden, `end_time` läuft **gegen** den Score: ohne Rang 1 wäre die Reihenfolge umgekehrt. Keine Gleichstände → sagt nichts über Stabilität |
| **3** | Gleichstand auch im `end_time` → kürzeres Muster zuerst | `fib_score` und `end_time` gleich, `start_time` eindeutig |
| **4** | Gleichstand im **ganzen** Schlüssel → Eingabereihenfolge bleibt | keine fachliche Regel kann hier noch entscheiden. Die Fremdzeilen tragen einen höheren Score und stehen deshalb alle davor — sie können die Gruppe inhaltlich nicht berühren |
| **5a** | der Überlappungs-Durchlauf ist chronologisch | alle `start_time` verschieden → stabil und unstabil gleichwertig |
| **5b** | der Überlappungs-Durchlauf ist stabil | mehrere Muster mit identischem `start_time`; `fib_score` überall gleich |
| **6** | Gegenprobe: ohne Gleichstand ändert sich **nichts** gegenüber `main` | vergleicht gegen den **Lauf** einer mutierten Fassung mit `main`s Sortierzeile, nicht gegen eine hingeschriebene Reihenfolge |
| **7** | Wiederholbarkeit | jede Eingabereihenfolge, zweimal gelaufen → genau **eine** Ausgabe |
| **8** | echte Daten | s. u. |
| **9** | Mutationsproben | s. u. |
| **10** | `shared/ergebniskurven.py` meldet `9x AKTUELL` | |
| **11** | der Test verändert nichts | `git status` **und** Ordnerliste |

### Abschnitt 8 — echte Kursdaten, echte Einstiegspunkte

Je Bot 12 Symbole (4 mit `--schnell`), aus `config/top25_symbols.txt` bzw.
`config/sp500_top150.txt`, mit den Live-Parametern:

| Prüfung | Erwartung |
|---|---|
| jedes Symbol hat Gleichstände im `fib_score` | der geprüfte Fall ist kein Laborfall |
| `start_time` und `end_time` je Symbol eindeutig | die Messung, auf die sich die Begründung im Quelltext beruft |
| **Menge** nach `remove_overlapping` wie auf `main` | die Umstellung sortiert um, sie streicht nichts anders |
| **`find_causal_waves` Zeile für Zeile wie auf `main`** | die Funktion speist Backtest, Optimierung und alle neun Kapitalkurven — hier hängt daran, dass sich kein Trade verschiebt |

Die Vergleichsfassung ist keine Kopie aus der Git-Historie, sondern eine
**mutierte Kopie der heutigen Datei**, in der die Rangfolge durch `main`s
Zeile ersetzt ist. Der Test ist damit autonom — er braucht weder Netz noch
einen zweiten Arbeitsbaum.

### Abschnitt 9 — die Mutationsproben

Neun Mutanten, je mit **exakter** Erwartung. Mehr wäre eine Wache, die zu
viel abdeckt; weniger eine Prüfung, die nichts sichert.

| Mutante | Es müssen **genau** diese Abschnitte anschlagen |
|---|---|
| wie `main` (einspaltig und unstabil) | 1, 3, 4 |
| nur `fib_score`, aber stabil | 1, 3 |
| `end_time` nicht im Schlüssel | 1 |
| `start_time` nicht im Schlüssel | 3 |
| `fib_score` nicht im Schlüssel | 2 |
| Rangfolge ersatzlos entfernt | 1, 2, 3 |
| **nur `kind=quicksort`** | **keiner** |
| Durchlauf rückläufig | 5a |
| Durchlauf ohne stabile Sortierung | 5b |

**Drei Zeilen dieser Tabelle sind selbst Befunde:**

* *„Rangfolge ersatzlos entfernt" lässt Abschnitt 4 bestehen.* Ohne
  Sortierung bleibt die Eingabereihenfolge trivial erhalten. Abschnitt 4
  sagt also nichts darüber, **ob** sortiert wird — genau die zweite Falle,
  hier gemessen statt behauptet.
* *„nur `fib_score`, aber stabil" lässt Abschnitt 4 bestehen und 1 und 3
  fallen.* Das ist die Aussage des Auftrags in Testform: `kind="stable"`
  allein macht das Ergebnis **reproduzierbar**, aber nicht **begründet**.
* *„nur `kind=quicksort`" darf **keinen** Abschnitt zum Anschlagen bringen.*
  pandas wertet `kind` bei einer **mehrspaltigen** `sort_values` nicht aus —
  der Pfad läuft über `lexsort` und ist ohnehin stabil. Schlägt hier je ein
  Abschnitt an, hat pandas sein Verhalten geändert; dann ist der Kommentar im
  Quelltext zu berichtigen, nicht der Test.

### Abschnitt 11 — warum `git status` allein nicht genügt

Git kennt keine leeren Ordner. Die erste Fassung dieses Tests legte ihre
Mutantenkopien im Strategie-Ordner ab; deren Import rief
`get_strategy_paths(__file__)` auf, und diese Funktion **legt Ordner an** —
so entstanden unbemerkt `strategies/results/` und `strategies/logs/` im Repo.
`git status` blieb grün. Deshalb prüft Abschnitt 11 zusätzlich die
Ordnerliste.

Gegenprobe von Hand (muss rot werden):

    sed -e 's/wurzel = tempfile.mkdtemp(prefix="tb20_")/wurzel = tempfile.mkdtemp(prefix="tb20_", dir=ordner)/' \
        -e 's|    nachbau = os.path.join(wurzel, "strategies", name)|    nachbau = wurzel|' \
        shared/test_wellenauswahl.py > shared/_probe.py
    python3 shared/_probe.py --schnell ; echo "Rueckgabewert $?"
    rm -f shared/_probe.py ; rm -rf strategies/results strategies/logs

Erwartet: `git status`-Probe **grün**, Ordnerprobe **rot** mit
`neu: ['strategies/logs', 'strategies/results']`, Rückgabewert 1.

---

## 2. Die abgelegten Kapitalkurven

    python3 shared/ergebniskurven.py ; echo "Rueckgabewert $?"

Erwartet: **`Zusammenfassung: 9x AKTUELL`**, Rückgabewert 0. Dauer rund
30 Sekunden.

Das ist die Probe darauf, dass sich das Auswahlverhalten **nicht** verschoben
hat. Eine Abweichung hier wäre der Beleg für das Gegenteil und gehörte an den
Anfang jeder Zusammenfassung.

---

## 3. Die bestehenden Tests

    python3 shared/test_stabile_sortierung.py      # TB-19, erwartet 46 von 46
    python3 shared/test_drawdown_beide_masse.py    # TB-18, erwartet 253 von 253
    python3 research/elliott_wave_lookahead/test_lookahead.py
    python3 research/trailing_stops/test_atr_core.py
    python3 research/order_sensitivity/test_order_core.py
    python3 shared/test_live_params_werte.py

Alle sechs müssen mit Rückgabewert 0 durchlaufen. Die ersten beiden sind die
Vorgänger-Wachen, die übrigen vier die Stellen, die `elliott_wave_counter.py`
direkt oder indirekt benutzen.

**Drei Tests brauchen einen Lauf ohne Nebenläufer**, weil sie den
Repo-Zustand prüfen: `shared/test_drawdown_beide_masse.py`,
`research/pnl_2025_fixed_size/test_pnl.py` und
`shared/test_wellenauswahl.py` (Abschnitt 11). Wer parallel committet oder
ein zweites Skript laufen lässt, das nach `results/` schreibt, erhält dort
einen Fehlschlag, der nichts über den Code aussagt. Ebenso muss die Änderung
**eingecheckt** sein: `test_pnl.py` vergleicht gegen `HEAD`, nicht gegen den
Arbeitsbaum.

Vollständiger Durchlauf aller 32 Testdateien:

    for t in $(find . -name "test_*.py" -not -path "./.git/*" | sort); do
        echo "### $t"; python3 "$t" >/dev/null 2>&1; echo "   -> $?"
    done

### Acht Dateien schlagen in dieser Cloud-Umgebung schon auf `main` fehl

Kein Befund dieser Aufgabe. Mit einem Basislauf auf unverändertem `main`
nachgewiesen:

| Datei | Grund |
|---|---|
| `broker/test_ibkr.py` | keine `tzdata` im Container |
| `dashboard/test_dashboard.py` | kein `fastapi` |
| `dashboard/test_portfolio_sicht.py` | kein `fastapi` |
| `research/hrp_portfolio/test_hrp_core.py` | kein `scipy` |
| `shared/test_kursdaten.py` | kein `binance` |
| `research/drawdown_reihenfolge/test_drawdown.py` | braucht einen Bot als Argument |
| `research/elliott_wave_params/test_params.py` | dasselbe |
| `system/test_dienst_plists.py` | Rückgabewert 2 by design — prüft macOS-Dienste |

Auf dem Rechner des Nutzers (macOS, vollständige Abhängigkeiten) ist das
anders zu erwarten. Ohne `node` überspringt `dashboard/test_dashboard.py`
vier Prüfungen und meldet 780/780 statt 784.

Basislauf zum Selbstnachvollziehen:

    git worktree add /tmp/basis_main origin/main --detach
    cd /tmp/basis_main && for t in $(find . -name "test_*.py" ...); do ... done
    git worktree remove /tmp/basis_main

---

## 4. Die Messungen aus der Übergabe nachrechnen

Die Skripte der Messläufe liegen **nicht** im Repo (sie gehören nicht zum
Bot-Code). Wer die Zahlen nachrechnen will, findet die Kernaussagen als
Prüfungen im Selbsttest wieder:

| Aussage der Übergabe | Wo sie im Test steht |
|---|---|
| Gleichstände kommen in echten Daten überall vor | Abschnitt 8, „jedes Symbol hat Gleichstände" |
| `start_time`/`end_time` je Symbol eindeutig | Abschnitt 8, „eindeutig" |
| Die Menge der Muster ändert sich nicht | Abschnitt 8, „MENGE … wie auf main" |
| Kein Trade verschiebt sich | Abschnitt 8, „`find_causal_waves` Zeile für Zeile wie auf main" |
| Die Kapitalkurven bleiben | Abschnitt 10 |

Die Häufigkeitsverteilung (87 % / 99 %) und die Gitter-Messung über
`deviation_pct` sind Einmalmessungen und stehen mit ihren Zahlen in der
Übergabe, Abschnitt 1.

Die strukturelle Aussage, auf der alles ruht, ist in drei Zeilen
nachrechenbar:

    python3 -c "
    import itertools
    v={round(sum(x for x,b in zip((0.34,0.33,0.33),bits) if b),2)
       for bits in itertools.product((0,1),repeat=3)}
    print(sorted(v)); print(sorted(x for x in v if x>=0.3))"

Erwartet: `[0.0, 0.33, 0.34, 0.66, 0.67, 1.0]` und `[0.33, 0.34, 0.66, 0.67, 1.0]`
— fünf mögliche Werte oberhalb der Schwelle. Deshalb sind Gleichstände hier
strukturell und nicht datenabhängig.

---

## 5. Was nicht angefasst wurde

Zur Kontrolle:

    git diff --stat origin/main

Erwartet, und nur das:

    shared/test_wellenauswahl.py                              (neu)
    strategies/elliott_wave/elliott_wave_counter.py
    strategies/elliott_wave_stocks/elliott_wave_counter.py
    docs/UEBERGABE_TB20_wellenauswahl.md                      (neu)
    docs/TESTAUFTRAG_TB20_wellenauswahl.md                    (neu)
    docs/ERGEBNIS_TB20_wellenauswahl.md                       (neu)

Unverändert: `forward_test.py`, `live_params.py`, `equity_simulation.py`,
`results/*/equity_curve.csv`, die abgelegten Optimierungsergebnisse,
`broker/`, Crontab, launchd-Vorlagen, `research/`-Berichte.

Ebenfalls unverändert: `results/BTCUSDT_impulse_waves.csv`. Sie entsteht im
`__main__`-Block von `elliott_wave_counter.py` und wird beim nächsten
manuellen Lauf mit **denselben Zeilen in neuer Reihenfolge** überschrieben.
Kein Skript liest sie.

Die beiden Bot-Dateien müssen sich weiterhin **nur** in den zwei
Symbolliteralen des `__main__`-Blocks unterscheiden:

    diff strategies/elliott_wave/elliott_wave_counter.py \
         strategies/elliott_wave_stocks/elliott_wave_counter.py

Erwartet: genau zwei Unterschiede (`BTCUSDT_zigzag.csv`/`AAPL_zigzag.csv` und
`BTCUSDT_impulse_waves.csv`/`AAPL_impulse_waves.csv`).
