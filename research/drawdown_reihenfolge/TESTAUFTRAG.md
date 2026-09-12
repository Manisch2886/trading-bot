# Testauftrag: Drawdown-Reihenfolge

**Für eine lokale Claude-Code-Sitzung auf dem Mac.** Geprüfter Stand:
Branch `claude/new-session-08numz`, Basis `origin/main` (`94e0d7f`, nach
Merge von #80).

> ## Was diese Sitzung darf und was nicht
>
> **Alles in diesem Testauftrag ist lesend.** Der gesamte Ordner
> `research/drawdown_reihenfolge/` rechnet neben den Bots, nicht in
> ihnen: er liest die CSVs in `data/`, ruft Bot-Funktionen auf und
> schreibt ausschliesslich unter `research/drawdown_reihenfolge/results/`.
> Die Bot-Skripte werden **nicht als Programm ausgeführt** — nur als
> Bibliothek eingebunden, der `__main__`-Block läuft dabei nicht. Genau
> das ist wichtig: ein `python3 strategies/<bot>/multi_symbol_optimise.py`
> würde `results/<bot>/multi_symbol_optimisation_results.csv`
> **überschreiben**, und diese Dateien sind hier Beweismittel.
>
> **Nicht anfassen:** `strategies/`, `shared/`, `results/`, `config/`,
> `docs/`, `broker/`, Crontab, launchd. Kein `--echt` irgendwo. Keine
> Datenbank.
>
> **Schritt 6 dauert rund 2,5 Stunden** (der Krypto-Elliott-Bot allein
> etwa 90 Minuten). Vorher fragen, ob der Rechner so lange laufen soll.

---

## Schritt 0 — Umgebung

```bash
cd ~/trading-bot
git status --short
git rev-parse --abbrev-ref HEAD
python3 --version
python3 -c "import pandas, numpy; print(pandas.__version__, numpy.__version__)"
```

Erwartet: `git status` leer, Branch `claude/new-session-08numz`.

**Zur Python-Version:** die Skripte benutzen nur `pandas`, `numpy` und
die Standardbibliothek, keine Syntax jenseits von Python 3.8. Auf dem
`trading-env` (3.9.6) sollten sie laufen. Entwickelt und gemessen wurden
sie gegen **pandas 2.2.3 / numpy 1.26.4**. Falls die lokalen Versionen
abweichen, ist das kein Fehler, aber Schritt 4 ist dann besonders
wichtig: er stellt die Zahlen gegen die im Repo gespeicherten.

---

## Schritt 1 — Selbsttests, ein Bot

```bash
cd research/drawdown_reihenfolge
python3 test_drawdown.py turtle_soup_crypto
```

Erwartet: **18/18 Prüfungen bestanden**, Rückgabewert 0. Dauer unter
10 Sekunden. (Bei anderen Bots ist die Gesamtzahl 17 oder 18 — siehe
Schritt 2.)

Fünf der Zeilen beginnen mit `GEGENPROBE` — sie sind bestanden, wenn die
absichtlich verfälschte Rechnung **abweicht**. Steht dort `FEHL`, prüft
der Test nichts mehr und die anderen Zeilen sind wertlos.

Zeilen mit `Hinweis: <SYMBOL> deckt nur ... Tage ab` sind **erwartet** —
das ist der Mindest-Historie-Filter des Bots, der jüngere Listings
überspringt.

---

## Schritt 2 — Selbsttests, alle neun Bots

```bash
for b in elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto \
         volatility_breakout_crypto elliott_wave_stocks \
         rsi2_mean_reversion turtle_soup_stocks volatility_breakout; do
  echo "### $b"
  python3 test_drawdown.py $b 2>&1 | grep -E "^\[FEHL|Pruefungen bestanden"
done
```

Erwartet: **keine `[FEHL`-Zeile**, und je Bot alle Prüfungen bestanden.
Die Gesamtzahl ist nicht überall gleich, und das ist Absicht:

| Bots | erwartet | warum |
|---|---|---|
| die sechs Prototyp-Bots (`rsi2_*`, `turtle_soup_*`, `volatility_breakout*`) | **18/18** | voller Satz |
| `t3_supertrend` | **18/18** | statt der einen Struktur-Prüfung laufen dort zwei (das Bot-Maß IST das chronologische, und die Blockreihenfolge ergibt einen anderen Wert) — dafür fehlt die In-Sample-Prüfung |
| `elliott_wave`, `elliott_wave_stocks` | **17/17** | ohne In-Sample-Prüfung |

Bei `elliott_wave`, `elliott_wave_stocks` und `t3_supertrend` steht
statt dieser Prüfung eine `[----]`-Zeile: deren In-Sample-Fenster ist
nicht ableitbar, weil sie die Kursreihe selbst schneiden. Das ist
Absicht und kein Fehlschlag (`adapters.py`, `unterstuetzt_is`).

`elliott_wave` braucht hier etwa **4 Minuten** (Stundenkerzen), die
übrigen je unter einer Minute.

---

## Schritt 3 — Die Gegenprobe zur Gegenprobe

Eine grüne Prüfung ist erst etwas wert, wenn belegt ist, dass sie rot
werden kann (Protokoll-Prinzip 12). Die fünf eingebauten Gegenproben
prüfen das für die Rechnung. Diese Schritte prüfen es für die
**Gleichheit mit dem Bot** — also für die Aussage, auf der alles ruht.

```bash
cd research/drawdown_reihenfolge
cp engine.py /tmp/engine_original.py

# Mutation: die Bot-Reihenfolge durch die chronologische ersetzen
python3 - <<'EOF'
s = open("engine.py").read()
neu = s.replace('    if order == "bot":\n        return trades.index',
                '    if order == "bot":\n        return trades.sort_values("entry_time", kind="stable").index')
assert neu != s, "Ersetzung griff nicht - Zeile geaendert?"
open("engine.py", "w").write(neu)
EOF

python3 test_drawdown.py turtle_soup_crypto 2>&1 | grep -E "^\[FEHL|Pruefungen bestanden"
cp /tmp/engine_original.py engine.py
git diff --stat engine.py        # muss LEER sein
```

Erwartet: **15/18**, mit diesen drei roten Zeilen (gemessen):

```
[FEHL] dd_bot und score_bot identisch zum Bot
[FEHL] Das Bot-Mass ist die Blockreihenfolge   (dd_bot=-629.0, dd_block=-164.66)
[FEHL] In-Sample-Fenster identisch zu multi_symbol_walk_forward...
```

Bleibt der Lauf grün, vergleicht der Test nicht das, was er behauptet zu
vergleichen — dann bitte melden und hier abbrechen.

Die letzte Zeile stellt den Originalzustand sicher wieder her. `git diff
--stat engine.py` muss leer ausgeben.

Zweite Mutation, diesmal am Raster:

```bash
cp adapters.py /tmp/adapters_original.py
python3 - <<'EOF'
s = open("adapters.py").read()
neu = s.replace("return [(p, m) for p in mo.DONCHIAN_PERIOD_RANGE for m in mo.STOP_MODE_RANGE]",
                "return [(p, m) for p in [10] for m in mo.STOP_MODE_RANGE]")
assert neu != s, "Ersetzung griff nicht - Zeile geaendert?"
open("adapters.py", "w").write(neu)
EOF

python3 analyse.py turtle_soup_crypto > /tmp/mutation.log 2>&1
python3 historie.py turtle_soup_crypto 2>&1 | grep -E "^ueber |^-> "

# aufraeumen: Original zurueck UND das Raster neu rechnen
cp /tmp/adapters_original.py adapters.py
python3 analyse.py turtle_soup_crypto > /dev/null 2>&1
python3 historie.py turtle_soup_crypto 2>&1 | grep -E "^ueber |^-> "
git diff --stat adapters.py      # muss LEER sein
```

Erwartet: der erste `historie.py`-Lauf meldet
`wiedergefunden: 4 von 8` und `-> NICHT reproduzierbar`, der zweite
wieder `8 von 8` und `-> BELEGT`. Damit ist belegt, dass der
Zeilenvergleich in Schritt 4 wirklich vergleicht — und nicht nur eine
Teilmenge findet und zufrieden ist.

Wichtig ist hier die Reihenfolge: `historie.py` vergleicht die
**gespeicherte** Raster-CSV dieses Ordners gegen die des Bots. Ohne den
`analyse.py`-Lauf zwischendurch würde es die alte, unverfälschte Datei
lesen und nichts merken.

---

## Schritt 4 — Die gespeicherten Bot-Ergebnisse wiederfinden

Zuerst die Raster rechnen (ohne sie gibt es nichts zu vergleichen):

```bash
for b in rsi2_crypto turtle_soup_crypto volatility_breakout_crypto \
         rsi2_mean_reversion turtle_soup_stocks volatility_breakout; do
  python3 analyse.py $b > /tmp/analyse_$b.log 2>&1
  echo "### $b"; python3 historie.py $b 2>&1 | grep -E "^ueber |^  |^-> "
done
```

Erwartet: sechs Mal `-> BELEGT`, und in jeder Spaltenzeile steht `==`
mit voller Trefferzahl (z. B. `max_drawdown_pct == dd_block  8/8`).

Dann der Sonderfall `t3_supertrend` — zwei Läufe, zwei Erwartungen:

```bash
python3 analyse.py t3_supertrend --ohne-regimefilter > /tmp/t3_ohne.log 2>&1
python3 historie.py t3_supertrend --ohne-regimefilter 2>&1 | grep -E "^ueber |^  |^-> "

python3 analyse.py t3_supertrend > /tmp/t3_mit.log 2>&1
python3 historie.py t3_supertrend 2>&1 | grep -E "^ueber |^  |^-> "
```

Erwartet: der **erste** Lauf (ohne Regimefilter) meldet `-> BELEGT` mit
23/23 in allen sieben Spalten. Der **zweite** meldet
`-> NICHT reproduzierbar` — das ist hier das richtige Ergebnis und der
Beleg dafür, dass die gespeicherte Datei aus der Zeit vor dem
Regimefilter stammt (BERICHT.md, Abschnitt 2.3).

Und der zweite Sonderfall:

```bash
python3 analyse.py elliott_wave_stocks > /tmp/ews.log 2>&1   # rund 18 Minuten
python3 historie.py elliott_wave_stocks 2>&1 | grep -E "^ueber |^  |^-> " | head -12
```

Erwartet: `-> NICHT reproduzierbar`, mit Abweichungen in jeder Spalte.
Auch das ist richtig: die Look-Ahead-Korrektur aus PR #26 hat die Trades
dieses Bots vollständig verändert (BERICHT.md, Abschnitt 2.4).

---

## Schritt 5 — Die Kernzahl des Berichts nachsehen

```bash
python3 - <<'EOF'
import pandas as pd
d = pd.read_csv("results/elliott_wave_stocks_raster.csv")
r = d[(d.deviation_pct == 5.0) & (d.stop_loss_pct == 3.0) & (d.use_take_profit == False)].iloc[0]
print("dd_block ", r.dd_block, " (erwartet -82.50)")
print("dd_entry ", r.dd_entry, " (erwartet -259.86)")
EOF
```

Erwartet genau `-82.5` und `-259.86`. Das sind die −82,5 % gegen
−259,9 %, die `research/elliott_wave_params/BERICHT.md` in Abschnitt 6
nennt — der Befund, der diese Untersuchung ausgelöst hat, unabhängig
nachgerechnet.

---

## Schritt 6 — Der vollständige Lauf (optional, rund 2,5 Stunden)

**Vorher fragen.** Nur sinnvoll, wenn der Rechner ohnehin läuft.

```bash
python3 run_all.py 2>&1 | tee /tmp/run_all.log | grep -E "^-> |^Alle Schritte|Schritte mit Fehler"
```

Erwartet: am Ende `Alle Schritte ohne Fehler.` und ein Rückgabewert von
0. Einzelne Schritte mit Rückgabewert ≠ 0 werden am Ende noch einmal
aufgelistet.

Danach die Tabellen des Berichts neu erzeugen und mit ihm vergleichen:

```bash
python3 uebersicht.py | head -25
```

Die Spalten „Sieger Blockreihenfolge", „Sieger chronologisch" und
„kippt?" müssen mit Abschnitt 4.1 von `BERICHT.md` übereinstimmen.

Ein einzelner Bot statt allen:

```bash
python3 run_all.py turtle_soup_crypto
```

---

## Schritt 7 — Nichts angefasst

```bash
cd ~/trading-bot
git status --porcelain | grep -v "research/drawdown_reihenfolge" ; echo "Rueckgabewert: $?"
git diff --stat -- strategies shared results config docs
```

Erwartet: die erste Zeile gibt **nichts** aus (Rückgabewert 1 von `grep`
bedeutet hier „keine Treffer" und ist das gewünschte Ergebnis), die
zweite ebenfalls nichts. Dieselben zwei Prüfungen laufen als Prüfung 16
und 17 in jedem `test_drawdown.py`-Lauf mit.

Geändert haben dürfen sich nur Dateien unter
`research/drawdown_reihenfolge/results/` — und dort auch nur, wenn die
Läufe andere Zahlen ergeben als die eingecheckten. **Genau das wäre der
interessanteste Befund dieses Testauftrags**: es hiesse, dass sich
zwischen der Cloud-Sitzung und dem Mac etwas unterscheidet (pandas- oder
numpy-Version, oder der Datenstand in `data/`). Dann bitte `git diff`
auf die betroffene Datei vorlegen, statt sie zu verwerfen.

---

## Was ein Fehlschlag bedeutet

| Beobachtung | Bedeutung |
|---|---|
| `[FEHL] Kennzahlen identisch zu evaluate_combination_multi` | die Nachbildung weicht vom Bot ab — dann beantwortet der Bericht die Frage nicht, und alle Zahlen sind vorläufig |
| `[FEHL]` in einer `GEGENPROBE`-Zeile | die Prüfung kann nicht rot werden, die grünen Zeilen daneben sind wertlos |
| Schritt 3 bleibt grün | derselbe Fall, eine Ebene höher |
| `historie.py` meldet bei einem der sechs Bots `NICHT reproduzierbar` | Bot-Code oder Datenstand haben sich seit der Cloud-Sitzung geändert; Abschnitt 2.2 des Berichts müsste dann neu geschrieben werden |
| Abweichende Zahlen in `results/` | Versions- oder Datenunterschied, siehe Schritt 7 |
| `git status` zeigt Änderungen ausserhalb dieses Ordners | **abbrechen und melden.** Diese Untersuchung darf nichts anderes anfassen |
