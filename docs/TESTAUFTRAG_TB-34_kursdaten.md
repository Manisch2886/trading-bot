# Testauftrag TB-34 — Kursdaten neu aufbauen

**Autonom ausführbar.** Jeder Schritt nennt den Befehl, das erwartete Ergebnis
und was zu tun ist, wenn es abweicht. Schritte 1–7 laufen **überall**, Schritte
8–18 brauchen den **Mac** (der Binance-Endpunkt ist aus der Cloud gesperrt,
HTTP 403 der Egress-Richtlinie).

> ⚠️ **Der Neuaufbau ersetzt 72 Kursdateien.** Er ist der grösste schreibende
> Eingriff, den dieses Projekt auf `data/` kennt. Schritt 10 legt vorher eine
> Sicherung an; Schritt 14 zeigt, wie sie zurückgespielt wird. **Vor Schritt 11
> nichts anderes auf `data/` laufen lassen.**

Alle Befehle aus dem Repo-Wurzelverzeichnis (`cd ~/trading-bot`).

---

## Schritt 0 — Stand herstellen

```bash
cd ~/trading-bot
git fetch origin
git checkout claude/new-session-u5pehn
git pull origin claude/new-session-u5pehn
python3 -V
python3 -c "import pandas; print(pandas.__version__)"
```

**Erwartet:** Python 3.9+ und eine pandas-Version. `shared/zeitabdeckung.py`
braucht **kein** pandas; `kursdaten_neuaufbau.py` und die beiden Selbsttests
brauchen es.

---

## Schritt 1 — Basislauf: es ist nichts kaputtgegangen

```bash
for f in */test_*.py */*/test_*.py; do
  out=$(python3 "$f" 2>&1); rc=$?
  printf "%-3s %-58s %s\n" "$rc" "$f" "$(echo "$out" | tail -1 | cut -c1-70)"
done
```

**Erwartet:** dieselben Fehlschläge wie auf unverändertem `main`. In der Cloud
waren das **acht**, alle aus fehlenden Abhängigkeiten oder aus Tests, die ein
Argument verlangen:

| Test | Grund |
|---|---|
| `broker/test_ibkr.py` | Zeitzone `US/Eastern` fehlt |
| `dashboard/test_dashboard.py` | `fastapi` fehlt |
| `dashboard/test_portfolio_sicht.py` | Folgefehler daraus |
| `research/drawdown_reihenfolge/test_drawdown.py` | verlangt ein Argument |
| `research/elliott_wave_params/test_params.py` | verlangt ein Argument |
| `research/fib_score_stufen/test_stufen.py` | verlangt ein Argument |
| `research/hrp_portfolio/test_hrp_core.py` | `scipy` fehlt |
| `shared/test_kursdaten.py` | `yfinance` fehlt |

Auf dem Mac sind diese Abhängigkeiten vorhanden; dort sollten entsprechend
weniger fehlschlagen. **Ohne `node` meldet `dashboard/test_dashboard.py`
780/780 statt 784 — das ist richtig so, `node` ist auf dem Rechner des Nutzers
bewusst nicht installiert.**

**Weicht etwas anderes ab:** vergleichen mit einem Lauf auf unverändertem
`main` (`git stash` bzw. `git checkout main`), bevor es TB-34 zugerechnet wird.

---

## Schritt 2 — Die Teilkerzen-Wache: Selbsttest

```bash
python3 shared/test_zeitabdeckung.py; echo "rc=$?"
```

**Erwartet:** `40/40 Pruefungen bestanden.`, `rc=0`.

Darin enthalten und einzeln in der Ausgabe nachzulesen:

* **Teil B** — die Wache schlägt bei einer künstlich gekürzten Kerze an und
  **nicht** bei einer vollständigen (beide Richtungen).
* **Teil C** — dieselbe Datei durch beide Prüfungen: `kursdaten.py` meldet
  **null** Befunde, die Wache meldet die **11-Stunden-Kerze** mit vier
  gefüllten Kursspalten. Das ist der Kern der Aufgabe.
* **Teil G/H** — zwei zweistufige Mutationsproben und der Nachweis, dass eine
  Probe auf der falschen Lage **stumm** wäre, weil der Stand-Zeuge einspringt.

---

## Schritt 3 — Der Neuaufbau: Selbsttest

```bash
python3 shared/test_kursdaten_neuaufbau.py; echo "rc=$?"
```

**Erwartet:** `67/67 Pruefungen bestanden.`, `rc=0`.

Darin unter anderem: **Teil D** (eine Abweichung ausserhalb der Ränder
verhindert das Schreiben), **Teil E** (zweiter Lauf byte-identisch), **Teil F**
(Sicherung vollständig, verfälschte Sicherung wird abgelehnt, Zurückspielen am
Verhalten geprüft), **Teil I/J** (drei zweistufige Mutationsproben).

---

## Schritt 4 — Die bestehenden Werkzeuge laufen weiter

```bash
python3 shared/test_binance_historie.py | tail -2
python3 shared/test_kursdaten.py; echo "rc=$?"
```

**Erwartet:** `75/75 Pruefungen bestanden.` für TB-31. `test_kursdaten.py`
verhält sich wie im Basislauf.

---

## Schritt 5 — Probelauf gegen die **echten** 72 Kursdateien

```bash
python3 research/kursdaten_neuaufbau/probelauf.py --json daten/probelauf.json; echo "rc=$?"
```

**Erwartet:** `295/295 Pruefungen bestanden.`, `rc=0`, rund 25 Sekunden.
In der Tabelle je Datei: **innen = 0**, **Rand = 1** bei `1h`/`4h`, **Rand = 2**
bei `1d`.

```bash
git status --short data/
```

**Erwartet: leere Ausgabe.** Der Probelauf fasst keine Kursdatei an; seine
Schreibprobe läuft auf einer Kopie in einem temporären Ordner.

---

## Schritt 6 — Zeitabdeckung **vorher** messen

```bash
python3 shared/zeitabdeckung.py --json /tmp/tb34_vorher.json; echo "rc=$?"
```

**Erwartet:** `rc=1` (Befund ist hier richtig), rund 40 Sekunden, und am Ende:

```
Zusammenfassung: 29x rand_erste, 48x rand_letzte
BEFUND: 48 Datei(en) haben eine Randkerze, die ihren Zeitraum nicht abdeckt.
```

48 = 24 Tagesdateien + 24 Vier-Stunden-Dateien. Die 29 `rand_erste` sind die
24 Tagesdateien plus fünf 4h-Dateien spät gelisteter Symbole.

**Diese Zahl bitte notieren** — Schritt 13 vergleicht dagegen.

---

## Schritt 7 — Datenwege: wer rechnet auf dem alten Stand?

```bash
python3 research/kursdaten_neuaufbau/datenwege.py --json daten/datenwege.json
```

**Erwartet** (Abschnitt 2 und die Schlusszeilen):

```
   -> 9 von 9 lesen KEINE Datei aus data/.
...
Zusammenfassung: 37 Module lesen data/ unmittelbar, 64 weitere
ueber load_all_symbol_data() - zusammen 101. 9 Module schreiben
nach data/, 20 holen live.
```

---

# Ab hier: nur auf dem Mac (Binance-Endpunkt nötig)

---

## Schritt 8 — Erreichbarkeit prüfen

```bash
python3 shared/kursdaten_neuaufbau.py --symbole BTCUSDT --zeitrahmen 1d --pause 0.25
```

**Erwartet:** eine Zeile für `BTCUSDT 1d` mit `Endpunkt ab ...`, danach
`Trockenlauf - nicht geschrieben`. Rückgabewert 0 oder 1.

**Scheitert es mit HTTP 403/`connect_rejected`:** der Lauf findet auf dem
falschen Rechner statt. In der Cloud ist der Endpunkt gesperrt; das ist eine
Richtlinienentscheidung und wird nicht umgangen.

**Scheitert es mit `ABBRUCH: ... HTTP 418`:** die IP ist gesperrt. **Nicht
weiterprobieren** — das verlängert die Sperre. Mindestens eine Stunde warten.

---

## Schritt 9 — Trockenlauf über den **ganzen** Bestand

```bash
python3 shared/kursdaten_neuaufbau.py --bericht /tmp/tb34_trocken.json | tee /tmp/tb34_trocken.txt
echo "rc=$?"
```

Dauer: rund **10–20 Minuten** (72 Dateien, rund 3000 Anfragen, Mindestpause
0,25 s).

**Erwartet am Anfang der Zusammenfassung** — und das ist der entscheidende
Satz des ganzen Testauftrags:

```
Kein Befund: alle Abweichungen im gemeinsamen Bereich sitzen an den Raendern
(erste bzw. letzte Zeile des Altbestands) - genau dort, wo die Teilkerzen stehen.
```

**Steht dort stattdessen `BEFUND: n Datei(en) weichen ... AUSSERHALB der
Raender ab`, ist der Lauf hier zu Ende.** Das ist keine Kleinigkeit: es hiesse,
dass sich die Historie **im Innern** geändert hat. Dann:

1. Den Bericht ansehen: `python3 -m json.tool /tmp/tb34_trocken.json | less`
2. Die genannten Zeitpunkte von Hand gegen den Endpunkt halten.
3. **Nicht schreiben.** Es gibt bewusst keinen Schalter, der das übergeht.

**Erwartete Randabweichungen:** je `1h`- und `4h`-Datei **1**, je `1d`-Datei
**2**. Insgesamt also rund **96** Randzeilen bei 72 Dateien.

**Ebenfalls erwartet:** eine Zeile
`Laufende Kerzen verworfen (close_time > Stand ...): 72` (oder eine ähnliche
Zahl je nach Uhrzeit) — das ist die Wache, die verhindert, dass der Fehler sich
wiederholt.

---

## Schritt 10 — Der Lauf, mit Sicherung

```bash
python3 shared/kursdaten_neuaufbau.py --schreiben --bericht /tmp/tb34_lauf.json | tee /tmp/tb34_lauf.txt
echo "rc=$?"
```

**Erwartet:** `rc=0`, `72 Datei(en) geladen, 72 geschrieben.` und am Ende ein
Block:

```
Sicherung: 72 Datei(en), ~184.x MB in
  /Users/<du>/trading-bot/data_sicherung/2026-09-..._......
  Sie wird NICHT automatisch geloescht. Zurueckspielen mit:
    python3 shared/kursdaten_neuaufbau.py --zurueckspielen data_sicherung/...
```

**Den Pfad der Sicherung notieren** — Schritt 14 braucht ihn.

**Platz:** die Sicherung ist so gross wie der Krypto-Teil von `data/`, also
rund 184 MB. Vorher prüfen: `df -h .`

**Bricht der Lauf mittendrin ab:** das Manifest wird nach **jeder** Datei
fortgeschrieben, die Sicherung der bereits ersetzten Dateien ist also gültig.
Mit Schritt 14 zurückspielen, Ursache klären, neu beginnen.

---

## Schritt 11 — Was sich geändert hat

```bash
python3 - <<'PY'
import json
d = json.load(open("/tmp/tb34_lauf.json"))
print(f"{'Datei':<20} {'alt':>7} {'neu':>7} {'+/-':>7}  {'alt ab':<12} {'neu ab':<12}")
for e in sorted(d["ergebnisse"], key=lambda x: (x["symbol"], x["intervall"])):
    print(f"{e['symbol']+'_'+e['intervall']:<20} {e['alt_zeilen']:>7} {e['neu_zeilen']:>7} "
          f"{e['neu_zeilen']-e['alt_zeilen']:>+7}  {str(e['alt_von'])[:10]:<12} {str(e['neu_von'])[:10]:<12}")
PY
```

**Diese Tabelle ist die Antwort auf „was ändert der Neuaufbau je Datei".**
Sie gehört in die Übergabe-Zusammenfassung.

Erwartete Grössenordnung: die dreizehn langen Historien beginnen heute am
2021-09-01 und sollten danach beim jeweiligen Listing-Datum beginnen — für
`BTCUSDT` und `ETHUSDT` im Jahr **2017**. Die elf spät gelisteten Symbole
ändern ihren Beginn **nicht** (er ist schon das Listing-Datum), gewinnen aber
zwei Wochen am Ende.

---

## Schritt 12 — Gegenprobe: derselbe Lauf noch einmal

```bash
STAND=$(python3 -c "import json;print(json.load(open('/tmp/tb34_lauf.json'))['stand'])")
md5 -q data/BTCUSDT_1d.csv data/BTCUSDT_1h.csv data/ETHUSDT_4h.csv > /tmp/tb34_vorher.md5

python3 shared/kursdaten_neuaufbau.py --schreiben --stand "$STAND" \
        --sicherung /tmp/tb34_sicherung2 --bericht /tmp/tb34_lauf2.json | tail -20

md5 -q data/BTCUSDT_1d.csv data/BTCUSDT_1h.csv data/ETHUSDT_4h.csv > /tmp/tb34_nachher.md5
diff /tmp/tb34_vorher.md5 /tmp/tb34_nachher.md5 && echo "BYTE-IDENTISCH"
```

**Erwartet:** `BYTE-IDENTISCH`, und im Bericht des zweiten Laufs **0**
abweichende Zeilen (alt und neu sind jetzt dasselbe).

**Wichtig:** `--stand` muss gesetzt sein. Ohne ihn ist der Stand die aktuelle
Uhrzeit, und sobald seit dem ersten Lauf eine Kerze abgeschlossen wurde, kommt
sie berechtigterweise dazu.

**Ein eigener `--sicherung`-Ordner ist nötig:** das Werkzeug lehnt einen
bereits belegten Sicherungsordner ab, statt die erste Sicherung zu
überschreiben.

---

## Schritt 13 — Zeitabdeckung **nachher**

```bash
python3 shared/zeitabdeckung.py --datenbeginn /tmp/tb34_lauf.json --json /tmp/tb34_nachher.json
echo "rc=$?"
```

**Erwartet:** **kein Befund für die 72 Krypto-Dateien**. Genauer:

* Die 48 Befunde aus Schritt 6 sind weg.
* Eine kurze **erste** Kerze am gemessenen Datenbeginn erscheint jetzt als
  Hinweis „das ist der Listing-Tag. Kein Befund." — dafür ist `--datenbeginn`
  da.
* Die Aktien-Tagesdateien haben weiterhin keinen Deckungszeugen und melden
  nichts; das ist unverändert richtig.

**Bleibt ein Befund stehen,** sagt der Bericht welcher. Ein `rand_letzte` auf
einer Krypto-Datei nach dem Lauf wäre ernst: es hiesse, dass doch eine
angeschnittene Kerze geschrieben wurde.

```bash
python3 shared/kursdaten.py; echo "rc=$?"
```

**Erwartet:** unverändert zum Basislauf — der Neuaufbau bringt keine Kerze ohne
Kurse mit.

---

## Schritt 14 — Die Sicherung zurückspielen (und wieder vor)

**Das ist eine Übung, kein Rückbau.** Sie beweist, dass die Sicherung
vollständig ist.

```bash
SICHERUNG=data_sicherung/2026-09-..._......     # Pfad aus Schritt 10
md5 -q data/BTCUSDT_1d.csv                      # neuer Stand

python3 shared/kursdaten_neuaufbau.py --zurueckspielen "$SICHERUNG"
echo "rc=$?"
md5 -q data/BTCUSDT_1d.csv                      # muss jetzt der ALTE sein
head -2 data/BTCUSDT_1d.csv                     # 2021-09-01 -> alter Stand
```

**Erwartet:** `72 von 72 Datei(en) zurueckgespielt`, `rc=0`, und
`BTCUSDT_1d.csv` beginnt wieder am **2021-09-01**.

Danach den neuen Stand wiederherstellen — mit dem Stand aus Schritt 10, damit
dasselbe herauskommt:

```bash
python3 shared/kursdaten_neuaufbau.py --schreiben --stand "$STAND" \
        --sicherung /tmp/tb34_sicherung3 --bericht /tmp/tb34_lauf3.json | tail -10
md5 -q data/BTCUSDT_1d.csv                      # wieder der neue Stand
```

---

## Schritt 15 — Faltenpläne neu rechnen

Die Faltenpläne aus TB-31 beruhen auf der alten, beschnittenen Historie. Sie
sind jetzt überholt.

```bash
python3 research/krypto_historie/faltenplan.py \
        --json research/krypto_historie/daten/faltenplan_nach_tb34.json | tee /tmp/tb34_faltenplan.txt
```

**Erwartet:** **andere Zahlen als in TB-31.** Dort hiess es „heute 0 Falten je
Bot, nach dem Laden 2 bzw. 4". Die Nachher-Spalte war eine Rechnung auf
**angenommenen** Listing-Daten (`research/krypto_historie/daten/annahme_listing.json`);
jetzt stehen die **gemessenen** in den Dateien.

Zum Vergleich der beiden Lesarten der Faltenregel:

```bash
python3 research/krypto_historie/faltenplan.py --mindesttraining 2 | tail -20
```

**Das Ergebnis gehört ins Register** (`docs/VORREGISTRIERUNG_neuselektion.md`),
zusammen mit der Festlegung zur Lesart von „je Symbol" — siehe offener Punkt 1
in `docs/UEBERGABE_TB-31_krypto_historie.md`. **Diesen Schritt nicht selbst
entscheiden.**

---

## Schritt 16 — Ergebniskurven: die überprüfbare Vorhersage

```bash
python3 shared/ergebniskurven.py --json /tmp/tb34_kurven.json | tail -20
echo "rc=$?"
```

**Erwartet:** `rc=1` und in der Zusammenfassung **5× ABWEICHEND** (die fünf
Krypto-Bots) und **4× AKTUELL** (die vier Aktien-Bots).

* **ABWEICHEND bei den Krypto-Bots ist RICHTIG.** Mehr Historie und
  korrigierte Randkerzen ergeben andere Kurven.
* **Meldet ein AKTIEN-Bot ABWEICHEND, hat der Lauf etwas angefasst, was er
  nicht durfte.** Dann Schritt 14 (zurückspielen) und die Ursache klären.

> **Die Kurven bitte NICHT neu erzeugen.** `ABWEICHEND` ist nach dem Lauf
> richtig. Ob und wann neu gerechnet wird, entscheidet der Betreiber, und es
> gehört in denselben Schritt wie die Neuselektion.

---

## Schritt 17 — Der Datenstand-Hash der Vorregistrierung

```bash
grep -n -i "hash\|datenstand" docs/VORREGISTRIERUNG_neuselektion.md | head -20
```

**Zur Kenntnis, nicht zum Handeln:** der Datenstand-Hash **ändert sich durch
diesen Lauf**. Er steht auf der Sperrliste des Registers.

Das ist **kein Amendment**, sondern der Grund, warum TB-34 **vor** TB-30b
kommt: er ändert sich **vor** dem Selektionslauf, nicht danach. Wäre erst
selektiert und dann geladen worden, hätte die Selektion auf einer Historie
stattgefunden, die es danach nicht mehr gibt.

**Im Register nachtragen — als Tatsache, nicht als Nachtrag zu einer laufenden
Selektion.**

---

## Schritt 18 — Abschluss

```bash
git status --short data/ | head
git status --short | grep -v '^?? data_sicherung' | head -20
```

**Erwartet:** `data/` zeigt 72 geänderte Dateien (das ist der Zweck des Laufs),
`data_sicherung/` ist gitignoriert und taucht nicht auf.

> ⚠️ **Die geänderten Kursdateien nicht ohne ausdrückliche Entscheidung des
> Betreibers committen.** Der Branch `claude/new-session-u5pehn` enthält
> bewusst **keine** Änderung unter `data/`; der Lauf findet auf dem Mac statt,
> und ob der neue Bestand ins Repo soll, ist eine eigene Frage (184 MB
> Änderung in einem Commit).

---

## Zusammenfassung der erwarteten Zahlen

| Schritt | Erwartet |
|---|---|
| 2 | `40/40` |
| 3 | `67/67` |
| 4 | `75/75` (TB-31) |
| 5 | `295/295`, `git status data/` leer |
| 6 | `rc=1`, 48 Dateien mit Befund, 29× `rand_erste`, 48× `rand_letzte` |
| 7 | 9 von 9 Forward-Tests live, 37 + 64 = 101 Module auf `data/` |
| 9 | „Kein Befund" — alle Abweichungen an den Rändern, rund 96 Randzeilen |
| 10 | 72 geschrieben, Sicherung rund 184 MB |
| 12 | `BYTE-IDENTISCH` |
| 13 | **kein Befund** für die 72 Krypto-Dateien |
| 14 | 72 von 72 zurückgespielt, `BTCUSDT_1d.csv` wieder ab 2021-09-01 |
| 16 | **5× ABWEICHEND**, **4× AKTUELL** |
