# Testauftrag: TB-23 Determinismus-Test

**Autonom ausführbar.** Für eine lokale Claude-Code-Sitzung auf dem Mac oder
für einen Menschen. Geprüfter Stand: Branch `claude/new-session-f5zdsl`,
aufgesetzt auf `main` (Stand `0f39e3b`, nach PR #92/#93).

> ## Was diese Sitzung darf und was nicht
>
> **Alles hier ist lesend.** `shared/determinismus.py` und
> `shared/determinismus_lauf.py` rufen die Bots auf, verändern sie aber nicht
> und schreiben nichts ins Repo: `RESULTS_DIR` zeigt während jedes Laufs in
> einen temporären Ordner, und die Symboldateien werden nur gelesen. Die
> Permutation geschieht im Speicher.
>
> **Nicht anfassen:** `strategies/`, `config/`, `results/`, `data/`,
> `broker/`, Crontab, launchd. Kein `--echt` irgendwo. Keine Datenbank.
>
> **Schritt 5 dauert rund 15 Minuten** (gemessen in der Cloud-Umgebung:
> 800 s). Schritt 4 läuft in unter zwei Minuten. Wenn die Zeit knapp ist,
> Schritte 0–4 und 7–8 genügen für eine vollständige Prüfung des *Werkzeugs*;
> Schritt 5 wiederholt nur die *Messung*.

---

## Schritt 0 — Umgebung

```bash
cd ~/trading-bot
git status --short
git rev-parse --abbrev-ref HEAD
python3 --version
python3 -c "import pandas, numpy; print(pandas.__version__, numpy.__version__)"
```

Erwartet: `git status` leer, Branch `claude/new-session-f5zdsl`.

**Zur Python-Version:** benutzt werden nur `pandas` und die
Standardbibliothek (`numpy` kommt indirekt über die Bots). Keine Syntax
jenseits von Python 3.8. Gemessen wurde in der Cloud-Umgebung gegen
**Python 3.11.15 / pandas 3.0.5 / numpy 2.4.6**. Weichen die lokalen
Versionen ab, ist das kein Fehler — aber die absoluten Zahlen aus Schritt 5
können dann leicht abweichen. Die **Urteile** (deterministisch ja/nein) dürfen
es nicht.

---

## Schritt 1 — Der Basislauf: was war schon vorher rot?

Vor allem anderen der Nachweis, welche Testfehlschläge **nicht** von dieser
Arbeit stammen. Auf `main`, ohne die neuen Dateien:

```bash
cd ~/trading-bot
for t in shared/test_*.py research/*/test_*.py dashboard/test_*.py \
         notifications/test_*.py broker/test_*.py; do
  d=$(dirname "$t"); f=$(basename "$t")
  ( cd "$d" && python3 "$f" >/dev/null 2>&1 ); echo "$t rc=$?"
done
```

In der Cloud-Umgebung waren auf **unverändertem `main`** rot:

| Test | Grund |
|---|---|
| `broker/test_ibkr.py` | `ModuleNotFoundError: tzdata` |
| `dashboard/test_dashboard.py` | `ModuleNotFoundError: fastapi` (zusätzlich fehlt `node`) |
| `dashboard/test_portfolio_sicht.py` | `ModuleNotFoundError: fastapi` |
| `shared/test_kursdaten.py` | `ModuleNotFoundError: yfinance` |
| `research/hrp_portfolio/test_hrp_core.py` | `ModuleNotFoundError: scipy` |

Zwei weitere liefern `rc=1`, ohne fehlzuschlagen: `test_drawdown.py` und
`test_params.py` **erwarten einen Bot-Namen als Argument** und geben ohne ihn
nur ihre Nutzungszeile aus.

Auf dem Mac mit vollständiger Umgebung sollten alle grün sein. **Rot bleibt
rot, aber der Grund muss einer aus dieser Tabelle sein** — ein neuer Grund ist
ein Befund.

---

## Schritt 2 — Die Selbsttests des Werkzeugs

```bash
cd ~/trading-bot
python3 shared/test_determinismus.py
```

Erwartet: **49 bestanden, 0 fehlgeschlagen**, Rückgabewert 0. Dauer rund
40 Sekunden.

Der schnelle Weg (nur der Vergleichskern, unter 2 Sekunden):

```bash
python3 shared/test_determinismus.py --schnell    # 20 bestanden, 0 fehlgeschlagen
```

**Worauf zu achten ist — der Test ist nur dann etwas wert, wenn diese fünf
Zeilen grün sind:**

```
  OK    gehaerteter Bot: KEIN Befund (der Test kann auch gruen)
  OK    gehaertet + Zuteilung nach Dateireihenfolge: Befund gemeldet
  OK    Permutation kommt nicht an -> UNKLAR, nicht DETERMINISTISCH
  OK    der erste Aufruf sah die Originalreihenfolge
  OK    Lauf 0 trifft die abgelegte equity_curve.csv des Bots
```

* Zeile 1 ist die **Gegenprobe**: eine gehärtete Kopie von
  `turtle_soup_crypto` (totale Sortierung, kein Positionslimit, Allokation
  0,01 %) wird als *deterministisch* gemeldet. Fehlt sie, meldet das Werkzeug
  womöglich einfach jeden Bot als rot.
* Zeile 2 ist die **Mutationsprobe**: dieselbe gehärtete Kopie, plus genau
  einer eingebauten Zuteilung nach Dateireihenfolge bei drei Plätzen für
  24 Symbole. Sie geht wieder rot.
* Zeile 3 ist der **gefährlichste Fehler**: eine Kopie, deren
  `load_all_symbol_data()` die Reihenfolge ignoriert. Das Werkzeug muss
  `UNKLAR` melden — nicht `DETERMINISTISCH`.
* Zeile 4 beobachtet den **Ablauf**: die Kopie schreibt bei jedem Ladevorgang
  mit, welche Symbolreihenfolge sie tatsächlich gesehen hat.
* Zeile 5 ist der **Pflicht-Gegencheck**: Lauf 0 läuft in der unveränderten
  Originalreihenfolge und muss deshalb die abgelegte
  `results/rsi2_crypto/equity_curve.csv` treffen. Tut er das nicht, misst das
  Werkzeug etwas anderes als den Backtest des Bots.

Der Test legt seine Kopien in `tempfile.TemporaryDirectory()` an; `data/`,
`config/` und `shared/` sind darin Verweise auf das Original. Nach dem Lauf
ist `git status` unverändert (Abschnitt 8 prüft das selbst).

---

## Schritt 3 — Ein einzelner Bot, zum Anschauen

```bash
cd ~/trading-bot
python3 shared/determinismus.py --bot rsi2_crypto --perms 5 --voll
echo "Rueckgabewert: $?"
```

Erwartet: Urteil **NICHT DETERMINISTISCH**, Ursache „Zuteilung: andere Trades
bekommen das Kapital", Rückgabewert **1**. Dauer unter 5 Sekunden.

Und die Gegenprobe zum Rückgabewert — ein unbekannter Bot ist ein
Aufruffehler, kein stilles Grün:

```bash
python3 shared/determinismus.py --bot gibt_es_nicht ; echo "Rueckgabewert: $?"   # 2
```

---

## Schritt 4 — Der Schnellmodus (für den Cronjob)

```bash
cd ~/trading-bot
time python3 shared/determinismus.py --schnell
echo "Rueckgabewert: $?"
```

Erwartet: alle neun Bots, Rückgabewert **1**, Laufzeit **unter zwei Minuten**
(gemessen: 101 s). Die Urteilsspalte muss dieselbe sein wie in Schritt 5 —
nur die Spannen sind enger, weil fünf statt zwanzig Permutationen gelaufen
sind.

---

## Schritt 5 — Die vollständige Bestandsaufnahme

```bash
cd ~/trading-bot
time python3 shared/determinismus.py --voll --perms 20
```

Rund 15 Minuten. Erwartet:

| Bot | Urteil | umstrittene Trades |
|---|---|---|
| `elliott_wave` | **NUR REIHENFOLGE** | 0,0 % |
| `elliott_wave_stocks` | NICHT DETERMINISTISCH | ~28 % |
| `rsi2_crypto` | NICHT DETERMINISTISCH | ~14 % |
| `rsi2_mean_reversion` | NICHT DETERMINISTISCH | ~27 % |
| `t3_supertrend` | NICHT DETERMINISTISCH | ~15 % |
| `turtle_soup_crypto` | NICHT DETERMINISTISCH | ~31 % |
| `turtle_soup_stocks` | NICHT DETERMINISTISCH | ~36 % |
| `volatility_breakout` | NICHT DETERMINISTISCH | ~47 % |
| `volatility_breakout_crypto` | NICHT DETERMINISTISCH | ~12 % |

Die genauen Zahlen des Referenzlaufs stehen in
`research/determinismus/ergebnisse/gesamt_voll.json` und in `BERICHT.md`,
Abschnitt 1 und 4. **Die Urteile müssen übereinstimmen.** Bei den Prozentwerten
sind ein bis zwei Punkte Abweichung erwartbar, wenn die Kursdateien seit dem
Referenzlauf gewachsen sind — dann sind es andere Trades.

`elliott_wave` ist der wichtigste Einzelwert: er muss **NUR REIHENFOLGE**
melden, nicht „NICHT DETERMINISTISCH" und nicht „DETERMINISTISCH". Wäre er
rot, unterschiede das Werkzeug die beiden Befundarten nicht; wäre er grün,
übersähe es, dass die Zeilenreihenfolge seiner `equity_curve.csv` von der
Symbolreihenfolge abhängt.

---

## Schritt 6 — Reproduzierbarkeit bei festem Startwert

```bash
cd ~/trading-bot
python3 shared/determinismus.py --bot t3_supertrend --perms 6 --seed 4711 --json /tmp/a.json
python3 shared/determinismus.py --bot t3_supertrend --perms 6 --seed 4711 --json /tmp/b.json
python3 - <<'PY'
import json
a = json.load(open("/tmp/a.json"))["befunde"][0]["laeufe"]
b = json.load(open("/tmp/b.json"))["befunde"][0]["laeufe"]
schl = lambda x: [(l["signal_fp"], l["ausgefuehrt_fp"], l["kapitalpfad_fp"]) for l in x]
print("identisch:", schl(a) == schl(b))
PY
```

Erwartet: `identisch: True`.

Und die Gegenprobe — ein anderer Startwert muss etwas anderes liefern:

```bash
python3 shared/determinismus.py --bot t3_supertrend --perms 6 --seed 4712 --json /tmp/c.json
```

`/tmp/c.json` muss sich von `/tmp/a.json` unterscheiden, **ausser in Lauf 0**:
Lauf 0 ist bei jedem Startwert die unveränderte Originalreihenfolge.

---

## Schritt 7 — Der Zwischenspeicher verändert das Ergebnis nicht

Der Schnellmodus rechnet nicht jede Permutation neu. Dass das nichts ändert,
lässt sich direkt gegenprüfen:

```bash
cd ~/trading-bot
python3 shared/determinismus.py --bot turtle_soup_crypto --perms 8 --seed 77 --voll  --json /tmp/voll.json
python3 shared/determinismus.py --bot turtle_soup_crypto --perms 8 --seed 77         --json /tmp/cache.json
python3 - <<'PY'
import json
f = lambda p: [(l["signal_fp"], l["ausgefuehrt_fp"], l["kapitalpfad_fp"])
               for l in json.load(open(p))["befunde"][0]["laeufe"]]
print("identisch:", f("/tmp/voll.json") == f("/tmp/cache.json"))
PY
```

Erwartet: `identisch: True`.

Im JSON des zweiten Laufs steht zusätzlich, wie oft der Speicher sich selbst
geprüft hat:

```bash
python3 -c "import json;print(json.load(open('/tmp/cache.json'))['befunde'][0]['zwischenspeicher'])"
```

Erwartet: `abweichungen: []` und `kursdaten_abweichungen: []`, bei
`nachgerechnet_und_verglichen` > 0. Steht dort **0** nachgerechnet, prüft der
Speicher sich nicht mehr selbst — dann sind die Läufe 2..N nichts wert.

---

## Schritt 8 — Nichts wurde verändert

```bash
cd ~/trading-bot
git status --short
git diff --stat
python3 shared/ergebniskurven.py --nur-abweichung ; echo "Rueckgabewert: $?"
python3 shared/kursdaten.py ; echo "Rueckgabewert: $?"
```

Erwartet:

* `git status --short` zeigt **nur** die neuen Dateien unter `shared/` und
  `research/determinismus/` (bzw. nach dem Merge gar nichts).
* `git diff --stat` ist leer — keine bestehende Datei wurde angefasst.
* `ergebniskurven.py` meldet **9× AKTUELL**, Rückgabewert **0**. Das ist der
  Nachweis, dass keine `equity_curve.csv` überschrieben wurde: das Programm
  erzeugt jede Kurve neu und vergleicht sie Zeile für Zeile mit der
  abgelegten.
* `kursdaten.py` meldet denselben Stand wie vor der Arbeit.

Zusätzlich der direkte Nachweis, dass die Symboldateien unberührt sind:

```bash
md5 config/sp500_top150.txt config/top25_symbols.txt   # macOS
# md5sum config/sp500_top150.txt config/top25_symbols.txt   # Linux
```

Die Summen müssen dieselben sein wie vor dem Lauf. `git status` würde eine
Änderung ohnehin zeigen — die Prüfsumme fängt zusätzlich den Fall ab, dass
eine Datei geschrieben und mit identischem Inhalt zurückgeschrieben wurde.

---

## Schritt 9 — Was ausdrücklich **nicht** geprüft wird

Dieser Testauftrag prüft das **Messwerkzeug** und die **Bestandsaufnahme**.
Er prüft **nicht**:

* ob eine bestimmte Zuteilungsregel besser wäre (eigene Aufgabe),
* ob die 19 weiteren `sort_values`-Stellen ohne stabile Sortierung behoben
  sind (TB-19, eigene Aufgabe),
* ob die heutigen Live-Parameter unter einer anderen Symbolreihenfolge
  dieselben wären (das misst `research/drawdown_reihenfolge/`).

Ein grüner Lauf dieses Testauftrags heisst: **die Messung stimmt.** Er heisst
nicht, dass die Bots deterministisch sind — sie sind es, bis auf einen, nicht.
