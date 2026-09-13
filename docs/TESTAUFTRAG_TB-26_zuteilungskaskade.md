# Testauftrag TB-26 — Zuteilungskaskade

**Eigenständig ausführbar.** Dieses Dokument setzt keine Kenntnis der Sitzung
voraus, in der die Änderung entstanden ist. Wer es abarbeitet, kann die
Zusicherung von TB-26 selbst nachprüfen — und, wo etwas nicht stimmt,
unterscheiden, *was* nicht stimmt.

**Geprüft wird die Änderung an:** `shared/zuteilung.py` (neu),
`shared/test_zuteilung.py` (neu), den neun
`strategies/*/equity_simulation.py`, `shared/portfolio_overview.py` und
`shared/test_determinismus.py`.

---

## 0. Voraussetzungen

```bash
cd <projektwurzel>
python3 -c "import pandas, numpy; print(pandas.__version__, numpy.__version__)"
```

Gebraucht werden nur `pandas` und `numpy` — beides steht ohnehin in
`requirements.txt`. Die Kursdaten unter `data/` müssen vorhanden sein
(Tageskerzen für sieben Bots, `_1h` für `elliott_wave`, `_4h` für
`t3_supertrend`).

**Wenn Abhängigkeiten fehlen:** `binance`, `yfinance` oder das absichtlich
gitignorete `shared/fetch_binance_data.py` fehlen in manchen Umgebungen. Dann
lassen sich `elliott_wave` und `t3_supertrend` nicht laufen lassen. Das ist
eine Eigenschaft der Umgebung und **kein Befund** — aber es muss benannt
werden. Der Nachweis dafür ist ein **Basislauf auf unverändertem `main`**
(Abschnitt 6).

**Nichts von alledem schreibt ins Repo.** Alle Prüfungen lenken `RESULTS_DIR`
in temporäre Ordner um. Wer unsicher ist: `git status --porcelain` vorher und
nachher vergleichen (Abschnitt 5 tut genau das).

> **Einen Bot NICHT von Hand starten.** `python3 strategies/<bot>/equity_simulation.py`
> überschreibt `results/<bot>/equity_curve.csv`. Diese Dateien sollen im
> Rahmen dieser Prüfung unverändert bleiben — siehe Abschnitt 7.

---

## 1. Die Hauptzusicherung — neunmal `DETERMINISTISCH`

```bash
python3 shared/determinismus.py --voll --perms 20
echo "Rueckgabewert: $?"
```

**Erwartet:**

* In der Urteilsspalte steht für **alle neun** Bots `DETERMINISTISCH`.
* Die Spalte `umstr.` zeigt für alle neun `0.0%`.
* Beide Spannen (Rendite, Drawdown) sind je Bot ein einziger Wert
  (`x .. x`).
* **Rückgabewert 0.**
* Laufzeit: Größenordnung 10–15 Minuten auf einem Arbeitsrechner.

**Wenn ein Bot `NUR REIHENFOLGE` meldet:** dieselben Trades werden gehandelt,
aber in anderer Abrechnungsreihenfolge — dann greift die Ausstiegsreihenfolge
(`Zuteiler.ausstiegsreihenfolge`) nicht.

**Wenn ein Bot `NICHT DETERMINISTISCH` meldet:** die Auswahl selbst schwankt —
dann greift die Kaskade an einer Zuteilung nicht.

**Wenn ein Bot `UNKLAR` meldet:** der Lauf ist nicht durchgelaufen. Das ist
**keine Entwarnung**. Die Ursache steht in der Fehlerzeile darunter; bei
fehlenden Abhängigkeiten siehe Abschnitt 0 und 6.

Schnellere Zwischenprüfung (findet jeden Befund, beziffert die Streuung nur
gröber):

```bash
python3 shared/determinismus.py --schnell
```

---

## 2. Die Kaskade selbst

```bash
python3 shared/test_zuteilung.py
```

**Erwartet:** `Ergebnis: 65 bestanden, 0 fehlgeschlagen` (die genaue Zahl kann
abweichen, die Zahl der Fehlschläge nicht), dazu höchstens zwei Zeilen
`~ ausgelassen: … (Modul fetch_binance_data fehlt)` — siehe Abschnitt 0.

Was die Abschnitte prüfen, und woran man erkennt, was kaputt ist:

| Abschnitt | Zusicherung | schlägt an, wenn … |
|---|---|---|
| 1 | Stufe 1 (Signalstärke) entscheidet, und **nur sie kann es** | der Primärschlüssel nicht greift oder in die falsche Richtung sortiert |
| 2 | Stufe 2 (Diversifikation): der unkorrelierteste Kandidat gewinnt; das Fenster endet **vor** dem Einstiegstag | Richtung verdreht, Fenster verschoben, Korrelation falsch gerechnet |
| 3 | Stufe 3 (Liquidität): der liquidere gewinnt; bei leerem Buch rückt die Kaskade auf | Richtung verdreht, Dollar-Volumen falsch gebildet |
| 4 | Stufe 4: gleicher Startwert → gleiches Ergebnis, anderer → anderes; Startwert steht im Protokoll; unabhängig von `PYTHONHASHSEED` | der Zufall nicht mehr am Startwert hängt — oder gar nicht mehr zugeteilt wird |
| 5 | fehlende Angaben bekommen den **Median**, nicht das Ende und nicht die 0 | eine der beiden verworfenen Alternativen eingebaut ist |
| 6 | 20 Permutationen von Zeilen- **und** Symbolreihenfolge: identischer Kapitalpfad | irgendwo noch Reihenfolge durchschlägt |
| 7 | **Gegenprobe:** ohne Knappheit rechnet die neue Fassung Zeile für Zeile wie die Fassung vor TB-26 | die Kaskade dort greift, wo sie nicht greifen soll |
| 8 | **Mutationsproben:** sechs mutierte Kopien von `shared/zuteilung.py`; je Mutante müssen **genau** die erwarteten Abschnitte anschlagen | der Test seinen eigenen Gegenstand nicht mehr sieht — oder die Abschnitte nicht mehr unabhängig sind |
| 9 | die neun Bots benutzen die Kaskade wirklich (je ein Unterprozess) | ein Bot sie nicht aufruft oder seine Signatur sich geändert hat |
| 10 | der Test schreibt nichts ins Repo | — |

**Abschnitt 8 ist der wichtigste.** Er beantwortet die Frage, die ein grüner
Test sonst offenlässt: *Würde dieser Test es überhaupt merken?* Schlägt eine
Mutante **nicht** an, ist der Test durchgefallen — nicht bestanden.

Ohne Abschnitt 8 und 9 (schneller, für die Zwischenprüfung):

```bash
python3 shared/test_zuteilung.py --schnell
```

---

## 3. Das Messwerkzeug selbst

```bash
python3 shared/test_determinismus.py
```

**Erwartet:** `Ergebnis: 54 bestanden, 0 fehlgeschlagen`.

Dieser Test hat mit TB-26 seine Erwartung **umgedreht**, und das ist Absicht:

* **Abschnitt 3** — der unveränderte `turtle_soup_crypto` meldet jetzt *kein*
  Befund. Bis TB-23 war er der rote Fall. Mitgeprüft wird, dass sein
  Positionslimit trotzdem gebunden hat: ohne das wäre „kein Befund"
  trivial.
* **Abschnitt 5** — der rote Fall ist an eine Kopie gewandert, in der genau
  eine Sache auf den Stand vor TB-26 zurückgedreht ist (die Zuteilung nimmt
  wieder den ersten der Liste). Sie **muss** einen Befund erzeugen; sonst
  könnte das Werkzeug nur noch grün und wäre keine Messung mehr.
* **Abschnitt 7** — vergleicht Lauf 0 gegen einen **frischen** Lauf des Bots
  über `shared/kurven_lauf.py` statt gegen `results/<bot>/equity_curve.csv`.
  Die abgelegten Kurven stammen von vor TB-26 (siehe Abschnitt 7 dieses
  Dokuments).

---

## 4. Alle übrigen Selbsttests

```bash
for f in $(find . -name "test_*.py" | sort); do
  ( cd "$(dirname "$f")" && echo "--- $f" && python3 "$(basename "$f")" >/dev/null 2>&1; echo "    rc=$?" )
done
```

**Erwartet:** dieselben Rückgabewerte wie im Basislauf aus Abschnitt 6 — mit
**zwei benannten Ausnahmen**, die ausschließlich im ungemergten Zustand
auftreten:

| Datei | warum sie im Arbeitsbaum rot ist |
|---|---|
| `research/pnl_2025_fixed_size/test_pnl.py` | prüft `git diff HEAD -- strategies/` auf leer — eine Wache, die belegen soll, dass *jene* Untersuchung keinen Bot-Code angefasst hat. TB-26 fasst Bot-Code an; nach dem Merge ist der Diff gegen `HEAD` wieder leer. |
| `research/tb24_haltedauern/test_haltedauer_kern.py` | dieselbe Wache in der Form „keine fremden Pfade geändert". |

Beide **bestehen wieder, sobald der Stand gemergt ist** — sie messen den
Arbeitsbaum, nicht die Kaskade. Wer das nicht abwarten will, prüft sie in einem
sauberen Klon des gemergten Standes.

---

## 5. Nichts ins Repo geschrieben

```bash
git status --porcelain
```

**Erwartet:** genau die Dateien der Änderung — **keine** unter `results/`,
**keine** unter `data/`, **keine** `config/*.txt`,
**keine** `multi_symbol_optimisation_results.csv`.

Findet sich dort etwas, wurde ein Bot direkt gestartet statt über eines der
Werkzeuge. `git checkout -- results/` stellt den Stand wieder her.

---

## 6. Der Basislauf auf unverändertem `main` (nur bei Fehlschlägen nötig)

Fällt in Abschnitt 4 etwas anderes als die zwei genannten Dateien aus, muss
geklärt werden, ob es an TB-26 liegt:

```bash
git worktree add /tmp/tb26_basis origin/main
cd /tmp/tb26_basis
for f in $(find . -name "test_*.py" | sort); do
  ( cd "$(dirname "$f")" && printf "%-62s " "$f" && python3 "$(basename "$f")" >/dev/null 2>&1; echo "rc=$?" )
done
```

Alles, was **hier schon** rot ist, ist vorbestehend. Auf dem Stand vom
13.09.2026 sind das in einer Cloud-Umgebung ohne `node`, `scipy`, `fastapi`,
`yfinance` und Zeitzonendaten unter anderem: `dashboard/test_dashboard.py`,
`dashboard/test_portfolio_sicht.py`, `shared/test_kursdaten.py`,
`research/drawdown_reihenfolge/`, `research/elliott_wave_params/`,
`research/exposure_messung/`, `research/hrp_portfolio/test_hrp_core.py`,
`system/test_dienst_plists.py`.

Aufräumen: `git worktree remove /tmp/tb26_basis`.

---

## 7. Was nach dieser Prüfung ansteht — und nicht Teil von ihr ist

```bash
python3 shared/ergebniskurven.py
```

**Erwartet: `ABWEICHEND` für die Bots, deren Zuteilung sich geändert hat.**
Das ist **richtig und kein Fehler**: die abgelegten
`results/<bot>/equity_curve.csv` beschreiben die Zuteilung vor TB-26.

**Diese Prüfung erzeugt die Kurven NICHT neu.** Wann das geschehen sollte,
steht in `docs/TB-26_ZUTEILUNGSKASKADE.md`, Abschnitt „Was als Nächstes
ansteht". Es ist ein eigener, ausdrücklich freizugebender Schritt — und
sinnvollerweise derselbe, in dem auch die daran hängenden Kennzahlen
(Portfolio-Übersicht, Wochenmail, Dashboard) einmal gemeinsam nachgezogen
werden.

---

## 8. Kurzfassung für den eiligen Durchlauf

```bash
python3 shared/determinismus.py --voll --perms 20   # -> 9x DETERMINISTISCH, rc=0
python3 shared/test_zuteilung.py                    # -> 0 fehlgeschlagen
python3 shared/test_determinismus.py                # -> 54 bestanden, 0 fehlgeschlagen
git status --porcelain                              # -> nichts unter results/ oder data/
```

Diese vier Zeilen sind die Zusicherung. Alles andere in diesem Dokument dient
dazu, einen Fehlschlag einordnen zu können.
