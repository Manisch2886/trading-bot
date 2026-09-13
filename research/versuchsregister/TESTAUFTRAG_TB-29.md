# TESTAUFTRAG TB-29 — Versuchsregister

**Autonom ausführbar.** Dieses Dokument enthält alles, was zum Nachprüfen
nötig ist: Befehle, erwartete Ausgaben, Gegenproben und die vorbestehenden
Fehlschläge, die **nicht** dieser Änderung anzulasten sind.

* **Zweig:** `claude/new-session-ffmyo3`, Base `main`
* **Neu:** ausschliesslich `research/versuchsregister/` — fünf Dateien
* **Geändert:** nichts. Kein Bot-Code, keine `results/*.csv`, kein `broker/`,
  keine Crontab.

---

## 0. Vorbereitung

```bash
cd <repo>
git checkout claude/new-session-ffmyo3
```

**Wichtig für Prüfung 5:** `--historie` braucht eine **vollständige**
Git-Historie. Wurde das Repo flach geklont (`git clone --depth …`), zuerst:

```bash
git fetch --unshallow origin
git rev-parse --is-shallow-repository      # muss "false" ergeben
```

Ohne diesen Schritt bricht `--historie` mit einem Hinweis ab — das ist
gewollt, eine abgeschnittene Historie ergäbe eine zu niedrige Rundenzahl.

Die Prüfungen 1–4 und 6–8 brauchen **kein** `pandas`, keine Kursdaten und
kein Netz.

---

## 1. Die Erhebung läuft und liefert die Zahlen des Registers

```bash
python3 research/versuchsregister/versuchsregister.py
```

**Erwartet** (Rückgabewert 0), drei Abschnitte:

| Abschnitt | Schlüsselzahl |
|---|---:|
| 1 Rastergrössen aus dem Quelltext | `SUMME` = **636** |
| 2 abgelegte Ergebnisdateien | 36 / 64 / 6 / 6 / 23 / 8 / 12 / 4 / 4 (+ BTCUSDT 30) |
| 3 Rasterläufe unter `research/` | `SUMME` = **1886** |

In Abschnitt 1 darf **keine** Zeile `unklar` zeigen — alle 21
Optimierungsstellen müssen zählbar sein.

**Stichprobe von Hand** (die Rastergrössen sind im Code ablesbar):

```bash
grep -n 'RANGE = ' strategies/t3_supertrend/multi_symbol_optimise.py
# 4 Bereiche mit je 3 Werten -> 3*3*3*3 = 81, so steht es in der Ausgabe
```

---

## 2. Der Wächter schweigt auf unverändertem Stand (Gegenprobe)

```bash
python3 research/versuchsregister/versuchsregister.py --pruefen
echo "Rueckgabewert: $?"
```

**Erwartet:**

```
UNVERAENDERT gegenueber dem Register (Stand 13.09.2026). 53 Angaben geprueft:
  21 Rastergroessen, 10 Ergebnisdateien, 22 Rasterlaeufe unter research/.
Rueckgabewert: 0
```

Die Zeile „53 Angaben geprueft" ist Teil der Zusicherung: ein Wächter, der
nichts prüft, wäre ebenfalls grün.

---

## 3. Der Wächter schlägt an, wenn ein Raster wächst

**Nicht im Arbeitsverzeichnis mutieren.** Der Test macht das in einem
Sandkasten; von Hand geht es so:

```bash
cp strategies/volatility_breakout_crypto/multi_symbol_optimise.py /tmp/sicherung.py
sed -i 's/STOP_LOSS_RANGE = \[3.0, 5.0, 8.0, None\]/STOP_LOSS_RANGE = [3.0, 5.0, 8.0, 11.0, None]/' \
    strategies/volatility_breakout_crypto/multi_symbol_optimise.py

python3 research/versuchsregister/versuchsregister.py --pruefen
echo "Rueckgabewert: $?"

cp /tmp/sicherung.py strategies/volatility_breakout_crypto/multi_symbol_optimise.py
git diff --stat        # muss leer sein
```

**Erwartet:** Rückgabewert **1** und **zwei** Befunde, beide vom Typ
`RASTER GEAENDERT`:

```
  RASTER GEAENDERT     volatility_breakout_crypto/multi_symbol_optimise.py: Register 4, heute 5 (+1)
  RASTER GEAENDERT     volatility_breakout_crypto/multi_symbol_walk_forward.py: Register 5, heute 6 (+1)
```

**Zwei, nicht einer, ist richtig:** `multi_symbol_walk_forward.py` holt sein
Raster per Import aus `multi_symbol_optimise.py` und wächst mit. Entscheidend
ist, dass **ausschliesslich** die Rasterwache anspricht — keine Meldung vom
Typ `ZEILEN …`.

---

## 4. Die Testdatei — einundvierzig Zusicherungen

```bash
python3 research/versuchsregister/test_versuchsregister.py
echo "Rueckgabewert: $?"
```

**Erwartet:** `Alle 41 Zusicherungen bestanden.`, Rückgabewert 0.

Die elf Abschnitte im Einzelnen:

| # | prüft | warum dieser Prüffall |
|---|---|---|
| 1 | alle **vier** Rasterformen einzeln | ein Zähler, der nur `itertools.product` kennt, meldete für die anderen drei stillschweigend nichts — und „nichts" sieht in einer Summe aus wie „null Versuche" |
| 2 | Raster aus dem **Nachbarmodul** | `multi_symbol_walk_forward.py` hat keine eigenen Rastergrenzen; ohne Import-Auflösung käme 1 statt 19 heraus |
| 3 | Unzählbares wird als **`unklar`** gemeldet, nie als 0 | eine 0 fällt in einer Summe nicht auf |
| 4 | der Zähler folgt einer **Erweiterung** | ein Zähler, der die Zahl aus einem Kommentar oder einer zweiten Fundstelle läse, wäre hier grün und läse das Falsche |
| **5** | **Wächter, Rasterwache: schweigt → schlägt an → schweigt** | die Kernprobe, siehe unten |
| **6** | **Wächter, Zeilenwache: greift allein** | Gegenbeweis zur zweiten Falle, siehe unten |
| 7 | fehlende Ergebnisdatei ist ein Befund | eine fehlende Datei zählt naiv als 0 |
| 8 | Gegenprobe am echten Arbeitsstand | Voraussetzung dafür, dass 5 und 6 etwas aussagen |
| 9 | Wiederholbarkeit | zwei Läufe, zeichengleiche Ausgabe |
| 10 | die Summen, auf denen `REGISTER.md` steht | Brücke zwischen Programm und Dokument |
| 11 | `git status` / `git diff` | nichts ausserhalb `research/` und `docs/` |

### Die beiden Mutationsproben im Einzelnen

**Falle 1 — eine Probe bestätigt sich selbst.** Ein Test, der eine Datei
verändert und danach prüft, dass die Datei verändert ist, misst seine eigene
Vorbereitung. Abschnitt 5 prüft deshalb nie einen hergestellten *Zustand*,
sondern einen **Ablauf**: derselbe Sandkasten schweigt vor der Mutation,
schlägt danach an, schweigt nach dem Zurücksetzen wieder. Der mittlere Schritt
allein bewiese nichts — ein Wächter, der **immer** anschlägt, bestünde ihn
auch. Erst die beiden schweigenden Schritte machen die Aussage vollständig.

**Falle 2 — eine zweite Wache verdeckt das Fehlen der ersten.** Der Wächter
hat drei Wachen (Raster, Ergebnisdateien, Forschungsraster). Würde eine Probe
alle drei gleichzeitig stören, bliebe der Test auch dann grün, wenn eine davon
ersatzlos entfernt wäre. Deshalb nimmt `pruefen()` **drei getrennte Wurzeln**
an, und jede Probe spricht **genau eine** Wache an:

* Abschnitt 5 stört nur ein `strategies/`-Abbild (Ergebnisdateien und
  Forschungsraster zeigen unverändert auf das Original) und sichert zu, dass
  die Menge der Befundarten **exakt** `['RASTER GEAENDERT']` ist.
* Abschnitt 6 stört nur ein `results/`-Abbild und sichert ausdrücklich zu,
  dass **kein** Rasterbefund kommt.

Fiele eine der beiden Wachen ersatzlos weg, wäre genau einer dieser beiden
Abschnitte rot — und nicht beide grün.

**Gegenprobe zur Gegenprobe.** Wer prüfen will, dass Abschnitt 5 auch wirklich
rot werden kann: in `versuchsregister.py` in der Funktion `pruefen()` die
Zeile mit `RASTER_GEAENDERT` auskommentieren und den Test erneut laufen
lassen — Abschnitt 5 muss dann fehlschlagen, Abschnitt 6 weiterhin bestehen.
Danach zurücknehmen.

---

## 5. Die Historie — wie viele Runden gab es?

```bash
python3 research/versuchsregister/versuchsregister.py --historie | tail -5
```

**Erwartet:**

```
Ueber alle 21 Stellen: 0 Rasteraenderungen in der Git-Historie.
Aeltester Commit des Repos: 2026-09-02. …
```

Der Befehl rechnet die Rastergrösse **für jeden Commit neu** aus dem damaligen
Quelltext — er liest keinen Diff. Dass nichts herauskommt, ist das Ergebnis:
die Raster standen bereits im ersten Commit.

**Gegenprobe, dass der Befehl überhaupt etwas finden kann** — er findet für
jeden Commit eine Zahl, keine `unklar`:

```bash
python3 research/versuchsregister/versuchsregister.py --historie | grep -c unklar
# erwartet: 0
```

---

## 6. Die Einordnung nachrechnen

```bash
python3 research/versuchsregister/versuchsregister.py --dsr 36 81 237 653 2798
```

**Erwartet** (auf drei Nachkommastellen):

| N | √(2 ln N) | T = 252 | T = 1260 |
|---:|---:|---:|---:|
| 36 | 2,677 | 2,68 | 1,20 |
| 81 | 2,965 | 2,96 | 1,33 |
| 237 | 3,307 | 3,31 | 1,48 |
| 653 | 3,600 | 3,60 | 1,61 |
| 2798 | 3,984 | 3,98 | 1,78 |

Von Hand nachprüfbar: `python3 -c "import math; print(math.sqrt(2*math.log(2798)))"`

---

## 7. Nichts verändert

```bash
git status --porcelain
# erwartet:  ?? research/versuchsregister/    (und sonst nichts)

git diff origin/main HEAD --name-only
# erwartet:  ausschliesslich Pfade unter research/ und docs/
```

**Nach** dem Lauf zusätzlich:

```bash
python3 shared/ergebniskurven.py | tail -3
```

**Erwartet:** derselbe Stand wie auf unverändertem `main` — siehe Abschnitt 8.

---

## 8. Vorbestehende Fehlschläge — Basislauf auf unverändertem `main`

Nachgewiesen in einem separaten Arbeitsverzeichnis
(`git worktree add … origin/main`), mit **vollständig installierten**
Abhängigkeiten (`pandas`, `numpy`, `scipy`, `yfinance`, `python-binance`,
`fastapi`, `tzdata`, `pandas_market_calendars`) und vorhandenem `node`.

| Datei | `main` | Zweig | Bemerkung |
|---|---|---|---|
| `research/drawdown_reihenfolge/test_drawdown.py` | RC 1 | RC 1 | **kein Fehlschlag** — das Skript verlangt einen Bot als Argument und gibt sonst seine Nutzung aus |
| `research/elliott_wave_params/test_params.py` | RC 1 | RC 1 | dito |
| `research/fib_score_stufen/test_stufen.py` | RC 1 | RC 1 | dito |
| `shared/test_stabile_sortierung.py` | 45/46 | 45/46 | **eine** Zusicherung: `ergebniskurven.py` meldet nicht `9x AKTUELL` |
| `shared/test_wellenauswahl.py` | 322/323 | 322/323 | dieselbe Zusicherung |
| `system/test_dienst_plists.py` | RC 2 | RC 2 | „KEINE FEHLER, ABER NOCH OFFEN" — Rückgabewert 2 ist hier Absicht |

**Alle übrigen 34 Testdateien bestehen auf beiden Ständen**, darunter
`dashboard/test_dashboard.py` mit 784/784 (mit `node`; ohne `node` sind es
780/780) und `broker/test_ibkr.py` mit 168/168.

### Zum Punkt „`ergebniskurven.py` muss `9x AKTUELL` melden"

Der Auftrag nennt das als Randbedingung. **Auf unverändertem `main` meldet das
Programm `9x ABWEICHEND`** — nachgewiesen im Basislauf. Das ist ein bekannter,
gewollter Zustand: TB-26 hat die Zuteilungskaskade eingeführt und die
abgelegten Kurven ausdrücklich **nicht** mit erneuert (Übergabeprotokoll,
Nachtrag vom 13.09.2026: „Die abgelegten `results/*/equity_curve.csv` sind
bewusst nicht mit neu erzeugt — `shared/ergebniskurven.py` meldet sie bis dahin
zu Recht als ABWEICHEND").

Was diese Änderung zusichert und was geprüft wurde, ist deshalb die
**Unverändertheit**: vorher wie nachher `9x ABWEICHEND`, kein einziges
`results/*.csv` angefasst (Abschnitt 7). Wäre die Randbedingung wörtlich
erfüllbar gewesen, hätte sie ein Neuerzeugen der Kurven verlangt — und genau
das verbietet der Auftrag an anderer Stelle.

---

## 9. Was ein Fehlschlag bedeuten würde

| Befund | Bedeutung |
|---|---|
| Prüfung 2 gibt RC 1 | eine Rastergrösse oder Ergebnisdatei hat sich seit dem 13.09.2026 geändert. Das Register ist dann **veraltet**, nicht falsch — `STAND_*` und `REGISTER.md` nachziehen und im Pull Request begründen |
| Prüfung 1 zeigt `unklar` | eine Optimierungsstelle wurde so umgebaut, dass der Zähler sie nicht mehr liest. Der Zähler ist anzupassen — **nicht** die Zahl zu schätzen |
| Prüfung 3 gibt RC 0 | der Wächter ist wirkungslos. Das ist der ernsteste Fall: das Register verspräche dann eine Aktualität, die es nicht hat |
| Prüfung 5 bricht ab | flacher Klon — siehe Abschnitt 0 |
