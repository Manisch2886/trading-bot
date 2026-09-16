# Testauftrag TB-43 — Blinde Wachen (Mac)

**Autonom ausführbar.** Nichts an diesem Auftrag verlangt eine Entscheidung
während des Laufs. Er ist von oben nach unten abzuarbeiten; jeder Schritt sagt,
was zu erwarten ist und was ein Abbruchgrund wäre.

**Warum der Mac hier der eigentliche Nachweis ist:** Fehler 1 entstand aus der
Kette `elliott_wave`-Loader → `python-binance` → `dateparser`. In der Cloud
kommt der Binance-Import gar nicht erst durch, und neuere `dateparser`-Fassungen
nehmen den fraglichen Aufrufweg nicht mehr. **Der Fehler ist dort also nicht
über diese Kette reproduzierbar.** Die neuen Prüfungen greifen den Aufrufweg
deshalb **direkt** an (`open(pfad, mode="rb")` gegen den Schreibschutz) — das
läuft überall. Was nur der Mac leisten kann, ist der Beweis, dass damit auch die
**echte Kette** wieder durchläuft: `test_universum_trockenlauf.py` soll dort von
**10/20 auf vollständig grün** gehen.

> ⚠️ **Dieser Auftrag ändert nichts.** Kein `--echt`, keine Order, keine
> Kursdatei, keine Registerdatei, kein `live_params.py`. Wenn ein Schritt
> schreiben will, ist das ein **Abbruchgrund**, kein Zwischenfall.

> ⚠️ **`docs/VORREGISTRIERUNG_neuselektion.md` und
> `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md` werden nur GELESEN.**

---

## 0. Voraussetzungen

```bash
cd ~/trading-bot            # Pfad ggf. anpassen
git fetch origin
git checkout claude/new-session-lwi4bi
git pull origin claude/new-session-lwi4bi
python3 --version           # notiert wird, was hier steht
```

**Erwartet:** Der Zweig enthält die geänderten Werkzeuge. Zur Kontrolle:

```bash
grep -c "_open_argumente" research/universum_trockenlauf/loaderlauf.py
grep -c "TABELLE_GUELTIG" research/universum_trockenlauf/universum_trockenlauf.py
grep -c "LEERER VERGLEICH" research/registernachtrag_tb41/pruefe_register.py
```

**Erwartet:** drei Zahlen **grösser als 0**. Steht irgendwo `0`, ist der falsche
Zweig ausgecheckt — **Abbruchgrund**.

Ein Ergebnisordner wird **ausserhalb des Repos** angelegt:

```bash
mkdir -p ~/Downloads/TB-43_ergebnisse
E=~/Downloads/TB-43_ergebnisse
```

---

## 1. Der Datenstand — VOR allem anderen

Er wird am Anfang und am Ende gemessen. Beide Werte müssen gleich sein; das ist
der Nachweis, dass dieser Auftrag keine Kursdatei angefasst hat.

```bash
python3 research/registernachtrag_tb41/pruefe_register.py \
    --nur datenstand 2>&1 | tee $E/01_datenstand_vorher.txt
```

**Erwartet:** `d9449faf51bffaaa…`, **223** Dateien, `KEIN BEFUND`.
**Abbruchgrund:** eine andere Zahl oder ein anderer Hash.

---

## 2. Fehler 1 — läuft `loaderlauf.py` auf dem Mac jetzt überhaupt?

**Das ist der Schritt, den nur der Mac leisten kann.**

### 2a. Zuerst der alte Stand — der Fehler muss sich zeigen

```bash
git stash list > /dev/null
git worktree add --detach /tmp/tb43_main origin/main
cd /tmp/tb43_main
python3 research/universum_trockenlauf/test_universum_trockenlauf.py \
    2>&1 | tee $E/02a_alter_stand.txt | tail -30
cd ~/trading-bot
```

**Erwartet:** Der Lauf **scheitert** — auf dem Mac in der Grössenordnung
**10 von 20** Prüfungen, mit
`TypeError: argument for open() given by name ('mode') and position (2)`
in der Ausgabe.

> ⚠️ **Wenn dieser Schritt grün durchläuft, ist der Rest des Auftrags
> wertlos** — dann findet die Prüfung den Fehler nicht, den sie finden soll.
> Das ist zu **melden**, nicht zu übergehen. (Möglich ist das, wenn auf dem Mac
> inzwischen eine neuere `dateparser`-Fassung liegt. Dann bitte zusätzlich
> notieren: `python3 -c "import dateparser; print(dateparser.__version__)"`.)

### 2b. Jetzt der neue Stand

```bash
python3 research/universum_trockenlauf/test_universum_trockenlauf.py \
    2>&1 | tee $E/02b_neuer_stand.txt | tail -30
```

**Erwartet:** **alle** Prüfungen bestanden (in der Cloud waren es 70/70; auf dem
Mac kann die Gesamtzahl abweichen, entscheidend ist **0 GESCHEITERT**).
Besonders zu beachten sind die Teile **J** und **K** — sie sind neu.

**Abbruchgrund:** irgendein `FEHL` in Teil J oder K.

### 2c. Der Schreibschutz ist nicht löchrig geworden

In `02b_neuer_stand.txt` müssen diese Zeilen stehen:

```bash
grep -E "K[1-6]" $E/02b_neuer_stand.txt | tee $E/02c_schreibschutz.txt
```

**Erwartet:** `ok` für **alle** K-Zeilen, darunter namentlich
`io.open`, `pathlib.Path(pfad).open("w")`, `Path(pfad).write_text(…)` und
`os.open(pfad, O_WRONLY|O_CREAT)` — und `K6`, das am **Dateibestand** zeigt,
dass keine verbotene Datei entstanden ist.

**Abbruchgrund:** ein `durchgelassen` in einer K4-Zeile. Dann wäre der
Durchgriff repariert und der Schutz dabei löchrig geworden — genau der Fehler,
den diese Aufgabe vermeiden sollte.

---

## 3. Fehler 3 — beide Richtungen, am selben Lauf

**Der eigentliche Nachweis ist die Gegenrichtung.** Ein Werkzeug, das gegen die
richtige Tabelle nichts meldet, könnte auch bloss schweigen.

```bash
python3 research/universum_trockenlauf/universum_trockenlauf.py \
    --json $E/03a_tabelle_1611.json 2>&1 | tee $E/03a_tabelle_1611.txt | head -12

python3 research/universum_trockenlauf/universum_trockenlauf.py \
    --register-abschnitt 15.5 \
    --json $E/03b_tabelle_155.json 2>&1 | tee $E/03b_tabelle_155.txt | head -14
```

**Erwartet in `03a`:** die Kopfzeile nennt
`Abschnitt 16.1.1` — und **keine** ACHTUNG-Zeile.
**Erwartet in `03b`:** die Kopfzeile nennt `Abschnitt 15.5`, gefolgt von
`ACHTUNG: 15.5 ist NICHT die gueltige Tabelle`.

Und jetzt ausgezählt:

```bash
python3 - <<'PY' | tee $E/03c_beide_richtungen.txt
import json, os
E = os.path.expanduser("~/Downloads/TB-43_ergebnisse")
def abw(p):
    b = json.load(open(os.path.join(E, p)))
    n = []
    for bot, e in b["bots"].items():
        sel = [f for f in e["falten"] if not f["bestaetigung"]]
        if [len(f["gemessen_H"]) for f in sel] != e["register"]["falten"]:
            n.append(bot)
    return b["register_abschnitt"], n
for p in ("03a_tabelle_1611.json", "03b_tabelle_155.json"):
    a, n = abw(p)
    print("Abschnitt %-8s -> %d abweichende Bot-Reihen von 9  %s" % (a, len(n), sorted(n)))
PY
```

**Erwartet — beide Zeilen, genau so:**

```
Abschnitt 16.1.1   -> 0 abweichende Bot-Reihen von 9  []
Abschnitt 15.5     -> 8 abweichende Bot-Reihen von 9  [… acht Bots, elliott_wave NICHT dabei]
```

**Abbruchgrund:** eine andere Zahl als 0 bzw. 8. `0 / 0` hiesse, das Werkzeug
wechselt die Tabelle gar nicht; `8 / 8`, dass es immer noch die alte liest.

---

## 4. Fehler 2 — ein leerer Vergleich ist kein Erfolg

### 4a. Am eigenen Zweig, der (noch) nicht gemergt ist

```bash
python3 research/registernachtrag_tb41/pruefe_register.py \
    2>&1 | tee $E/04a_standardbasis.txt | tail -12
echo "Rueckgabewert: $?"
```

**Erwartet:** eine Zeile `Quelle basis:` mit `herkunft` = `git merge-base HEAD
origin/main`. Der Rest hängt davon ab, ob der Zweig schon gemergt ist — beides
ist in Ordnung, **solange das Werkzeug sagt, was es getan hat**.

### 4b. Der Selbsttest — hier steckt der Verhaltensnachweis

```bash
python3 research/registernachtrag_tb41/test_registernachtrag_tb41.py \
    2>&1 | tee $E/04b_selbsttest.txt | tail -20
```

**Erwartet:** **alle** Prüfungen bestanden (Cloud: 50/50), darunter Teil **K**:

* `K0: der Zweig ist wirklich gemergt` — die Probe ist echt, nicht gestellt
* `K3: der Vergleich gegen den gemergten Zweig ist wirklich leer`
* `K4: und genau das wird als BEFUND gemeldet, nicht als Erfolg`
* `K5: der Rueckgabewert sagt dasselbe - 1, nicht 0`
* `K8: merge-base … haette nicht geholfen`

**Abbruchgrund:** ein `FEHLT` in Teil K.

### 4c. Gegenprobe am alten Stand

```bash
cp research/registernachtrag_tb41/test_registernachtrag_tb41.py \
   /tmp/tb43_main/research/registernachtrag_tb41/
cd /tmp/tb43_main
python3 research/registernachtrag_tb41/test_registernachtrag_tb41.py \
    2>&1 | tee $E/04c_alter_stand.txt | tail -15
cd ~/trading-bot
```

**Erwartet:** **K4, K5, K6 und K7 fallen durch**, K0 bis K3 und K8 bestehen.
Das ist der Nachweis, dass die Prüfung den Fehler wirklich findet — und nicht
bloss besteht.

**Abbruchgrund:** K4–K7 bestehen auch hier.

---

## 5. Die volle Prüfung des Registernachtrags gegen eine frische Messung

Auf dem Mac läuft der Trockenlauf wirklich — die Zahlen kommen aus einer
Messung, nicht aus einem Dokument.

```bash
BASIS=$(git log -1 --format=%H -- docs/VORREGISTRIERUNG_neuselektion.md)^
python3 research/registernachtrag_tb41/pruefe_register.py \
    --basis $BASIS 2>&1 | tee $E/05_voller_lauf.txt | tail -12
```

**Erwartet:** `Quelle beleg: trockenlauf` (nicht `dokument`), `Quelle numstat`
mit **`655 0`** und **`85 0`**, alle neun Prüfungen gelaufen, `KEIN BEFUND`.

**Abbruchgrund:** ein Befund, oder `Quelle numstat: []`.

---

## 6. Der Datenstand — NACH allem

```bash
python3 research/registernachtrag_tb41/pruefe_register.py \
    --nur datenstand 2>&1 | tee $E/06_datenstand_nachher.txt
diff $E/01_datenstand_vorher.txt $E/06_datenstand_nachher.txt \
    && echo "IDENTISCH" | tee $E/06_vergleich.txt
git status --short | tee $E/06_git_status.txt
```

**Erwartet:** `IDENTISCH`, und `git status --short` zeigt **nichts** unter
`data/` und **nichts** unter `docs/VORREGISTRIERUNG_*`.

**Abbruchgrund:** irgendeine Abweichung.

---

## 7. Aufräumen und abgeben

```bash
git worktree remove /tmp/tb43_main --force
cd ~/Downloads
zip -r TB-43_blinde_wachen_MACLAUF.zip TB-43_ergebnisse
ls -la ~/Downloads/TB-43_blinde_wachen_MACLAUF.zip
```

**Abzugeben ist die ZIP-Datei `~/Downloads/TB-43_blinde_wachen_MACLAUF.zip`.**
Sie liegt **ausserhalb des Repos** und wird **nicht** committet.

---

## Was gemeldet werden soll

| | |
|---|---|
| 1 | Fiel Schritt **2a** auf dem alten Stand wirklich durch? Mit welcher Zahl? |
| 2 | Ist **2b** vollständig grün — besonders Teil J und K? |
| 3 | Stehen in **3c** die Zahlen **0** und **8**? |
| 4 | Fielen in **4c** genau K4–K7 durch? |
| 5 | Sagt **5** `Quelle beleg: trockenlauf` und `655 0` / `85 0`? |
| 6 | Ist der Datenstand in **6** identisch? |

---

## In einfacher Sprache

**Was wir wissen wollten.**
Drei Prüfprogramme dieses Projekts hatten aufgehört zu prüfen, ohne das zu
sagen. Sie meldeten „alles in Ordnung", während sie in Wirklichkeit gar nichts
mehr gemessen haben. Wir wollten wissen, ob unsere Reparatur wirklich
funktioniert — und zwar auf Ihrem Mac, nicht nur auf dem Server.

**Was herauskam.**
Das steht nach diesem Testlauf fest. Erwartet wird: Auf dem **alten** Stand
fallen die neuen Prüfungen durch, auf dem **neuen** Stand bestehen sie alle.

**Warum das so ist.**
Ein Test, der immer besteht, beweist nichts — er könnte ja auch einfach nie
etwas bemerken. Deshalb lassen wir jeden Test **zweimal** laufen: einmal gegen
den alten, kaputten Stand (da muss er Alarm schlagen) und einmal gegen den
neuen (da muss er schweigen). Erst beides zusammen zeigt, dass der Test wirklich
hinsieht.
Einer der drei Fehler lässt sich nur auf Ihrem Mac in voller Länge vorführen:
Er hängt an einem Zusatzprogramm für Börsendaten, das auf dem Server gar nicht
erst startet.

**Was das für dich heisst.**
Dieser Auftrag verändert nichts — er liest nur und schreibt ausschliesslich in
einen Ergebnisordner in `~/Downloads`. Es werden keine Kursdaten angefasst, kein
Handelsparameter geändert und keine einzige Order ausgelöst. Am Ende liegt eine
ZIP-Datei in `~/Downloads`, und die sechs Fragen in der Tabelle darüber sind die
einzigen, die beantwortet werden müssen. Steht irgendwo „Abbruchgrund", dann
bitte an dieser Stelle aufhören und melden, was dort stand.
