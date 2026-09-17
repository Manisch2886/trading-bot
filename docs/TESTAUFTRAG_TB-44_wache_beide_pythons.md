# Testauftrag TB-44 — Die Wache auf beiden Pythons (Mac)

**Autonom ausführbar.** Nichts an diesem Auftrag verlangt eine Entscheidung
während des Laufs. Er ist von oben nach unten abzuarbeiten; jeder Schritt sagt,
was zu erwarten ist und was ein Abbruchgrund wäre.

**Start (ein Befehl, kopierfertig):**

```
cd ~/trading-bot && claude --remote-control "Lies die Datei docs/TESTAUFTRAG_TB-44_wache_beide_pythons.md und arbeite sie als autonome Claude-Code-Sitzung vollständig eigenständig ab, wie darin beschrieben."
```

---

**Warum der Mac hier der eigentliche Nachweis ist.** Der Fehler steckt in
`pathlib._NormalAccessor` — einer Klasse, die es **ab Python 3.11 nicht mehr
gibt**. Der Mac läuft auf **3.9.6**, die Cloud auf **3.11 oder neuer**. In der
Cloud wurde deshalb mit nachinstallierten Interpretern gemessen (3.9.23,
3.10.20, 3.11.15, 3.12.3, 3.13.12). **Was nur der Mac leisten kann, ist der
Beweis, dass die echte Kette dort wieder durchläuft** —
`elliott_wave_stocks` → `yfinance` → `curl_cffi` → `Path(...).read_text()`.

> ⚠️ **Dieser Auftrag ändert nichts.** Kein `--echt`, keine Order, keine
> Kursdatei, keine Registerdatei, kein `live_params.py`, keine Datei unter
> `docs/projektfuehrung/`. Wenn ein Schritt schreiben will, ist das ein
> **Abbruchgrund**, kein Zwischenfall.

> ⚠️ **`docs/VORREGISTRIERUNG_neuselektion.md` und
> `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md` werden nur GELESEN.**

> ⚠️ **Die Erwartung „70/70" aus der Aufgabenstellung gilt nicht mehr.** Der
> Selbsttest hat zwei Teile dazubekommen. Die Zahl hängt jetzt davon ab, wie
> viele Python-Fassungen auf dem Rechner liegen — **entscheidend ist:
> 0 gescheitert.** Schritt 3 sagt, wie die Zahl zustande kommt.

---

## 0. Voraussetzungen

```bash
cd ~/trading-bot
git fetch origin
git checkout claude/new-session-tkwj4j
git pull origin claude/new-session-tkwj4j
git log --oneline -3

mkdir -p ~/Downloads/TB-44_ergebnisse
E=~/Downloads/TB-44_ergebnisse
python3 -VV                         2>&1 | tee $E/00_python.txt
python3 -c "import pandas, numpy; print('pandas', pandas.__version__, 'numpy', numpy.__version__)" 2>&1 | tee -a $E/00_python.txt
python3 -c "import dateparser; print('dateparser', dateparser.__version__)" 2>&1 | tee -a $E/00_python.txt
python3 -c "import pathlib; print('_NormalAccessor:', hasattr(pathlib,'_NormalAccessor'))" 2>&1 | tee -a $E/00_python.txt
for m in 8 9 10 11 12 13 14; do which python3.$m; done 2>&1 | tee -a $E/00_python.txt
```

**Erwartet:** Der Zweig enthält `TB-44: der Schreibschutz haelt auf jeder
Python-Fassung`. Python **3.9.6**, `_NormalAccessor: True`.

> ⚠️ **Wenn dort `_NormalAccessor: False` steht**, läuft der Mac inzwischen auf
> 3.11 oder neuer. Dann ist der Befund auch hier strukturell unsichtbar, und
> Schritt 2 wird grün durchlaufen, ohne etwas zu belegen. **Das ist zu melden**,
> nicht zu übergehen — und die Fassung aus `00_python.txt` gehört dann in die
> Rückmeldung.

---

## 1. Der Datenstand — VOR allem anderen

```bash
python3 research/registernachtrag_tb41/pruefe_register.py \
    --nur datenstand 2>&1 | tee $E/01_datenstand_vorher.txt
```

**Erwartet:** `d9449faf51bffaaa…`, **223 Dateien**.
**Abbruchgrund:** eine andere Zahl oder ein anderer Hash.

---

## 2. Der Befund — zuerst am ALTEN Stand, dann am neuen

**Das ist der Kern dieses Auftrags.** Ein Test, der auf dem alten Stand nicht
durchfällt, prüft nichts.

### 2a. Der alte Stand muss durchfallen

Der alte `loaderlauf.py` wird **neben** das Repo gelegt — **im Repo wird nichts
verändert**.

```bash
mkdir -p /tmp/tb44_alt
git show 9f3952f:research/universum_trockenlauf/loaderlauf.py > /tmp/tb44_alt/loaderlauf.py

python3 - <<'PY' 2>&1 | tee $E/02a_alter_stand.txt
import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "research", "universum_trockenlauf"))
import test_universum_trockenlauf as t
ALT = "/tmp/tb44_alt"
for reihenfolge in ("frueh", "spaet"):
    e, fehler = t._l_lauf(sys.executable, reihenfolge, ALT)
    if e is None:
        print("%-6s  Probe lief nicht: %s" % (reihenfolge, fehler)); continue
    print("--- pathlib %s geladen, Python %s ---" % (reihenfolge, e["py"]))
    print("  LESEN nach der Wache   :", e["nach_lesen_os"])
    print("  SCHREIBEN vor der Wache:", e["vor_schreiben_os"])
    print("  pathlib touch()        :", e["pathlib_schreiben_touch"])
    print("  pathlib read_text()    :", e["pathlib_lesen_read_text"])
    print("  wirklich angelegt      :", e["uebrig_nach_abbau"])
    print("  Opfer-Datei lebt noch  :", e["opfer_lebt"])
PY
git status --short | tee $E/02a_git_status.txt
```

**Erwartet — beide Richtungen des Fehlers müssen sichtbar werden:**

| Zeile | Erwartet auf dem alten Stand (Python 3.9) |
|---|---|
| `LESEN nach der Wache` | ein **`TypeError`** — nicht `durchgelassen` |
| `SCHREIBEN vor der Wache` | **`durchgelassen`** — der Schutz war hier offen |
| `pathlib touch()` (bei `frueh`) | **`durchgelassen`** — es wurde wirklich geschrieben |
| `pathlib read_text()` (bei `spaet`) | ein **`TypeError`** |
| `wirklich angelegt` | **nicht leer** |
| `Opfer-Datei lebt noch` | **`False`** — sie wurde wirklich gelöscht |
| `git status --short` | **leer** — es wurde nichts im Repo verändert |

> ⚠️ **Wenn `LESEN nach der Wache` hier `durchgelassen` sagt und
> `SCHREIBEN vor der Wache` `abgefangen`, findet die Prüfung den Fehler nicht,
> den sie finden soll.** Dann ist der Rest des Auftrags wertlos. **Melden**, mit
> `00_python.txt` dazu.

### 2b. Und jetzt der neue Stand — dieselben Zeilen

```bash
python3 - <<'PY' 2>&1 | tee $E/02b_neuer_stand.txt
import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "research", "universum_trockenlauf"))
import test_universum_trockenlauf as t
for reihenfolge in ("frueh", "spaet"):
    e, fehler = t._l_lauf(sys.executable, reihenfolge)
    if e is None:
        print("%-6s  Probe lief nicht: %s" % (reihenfolge, fehler)); continue
    print("--- pathlib %s geladen, Python %s ---" % (reihenfolge, e["py"]))
    print("  LESEN nach der Wache   :", e["nach_lesen_os"])
    print("  SCHREIBEN vor der Wache:", e["vor_schreiben_os"])
    print("  pathlib touch()        :", e["pathlib_schreiben_touch"])
    print("  pathlib read_text()    :", e["pathlib_lesen_read_text"])
    print("  wirklich angelegt      :", e["uebrig_nach_abbau"])
    print("  Opfer-Datei lebt noch  :", e["opfer_lebt"])
    print("  nachgezogen            :", e["nachgezogen"])
PY
```

**Erwartet — in BEIDEN Richtungen, ohne Ausnahme:**

```
  LESEN nach der Wache   : durchgelassen
  SCHREIBEN vor der Wache: abgefangen
  pathlib touch()        : abgefangen
  pathlib read_text()    : durchgelassen
  wirklich angelegt      : []
  Opfer-Datei lebt noch  : True
```

**Abbruchgrund:** irgendein anderer Wert.

---

## 3. Der volle Selbsttest

```bash
python3 research/universum_trockenlauf/test_universum_trockenlauf.py \
    2>&1 | tee $E/03_selbsttest.txt | tail -20
grep "Python-Fassungen" $E/03_selbsttest.txt
grep -c "^    FEHL" $E/03_selbsttest.txt
```

**Erwartet:** die letzte Zeile lautet `<N>/<N> Pruefungen bestanden.` und
`grep -c "^    FEHL"` gibt **`0`**.

**Wie `N` zustande kommt:** 70 (Teile A–K, unverändert) + 11 (Teil M) + 1 (L6)
+ **50 je gefundener Python-Fassung**. Bei genau einer Fassung also **132**.
Die Zeile `Python-Fassungen:` nennt, welche gefunden wurden — sie ist der
maßgebliche Beleg, nicht die Gesamtzahl.

> ⚠️ **`L6` schlägt fehl**, wenn keine Fassung **unter 3.11** mitlief. Auf dem
> Mac darf das nicht passieren (3.9.6). Passiert es doch, gehört es in die
> Rückmeldung — es hiesse, der Test läuft hier an der eigentlichen Stelle
> vorbei.

**Abbruchgrund:** irgendein `FEHL`.

---

## 4. Die echte Kette — läuft der Trockenlauf auf allen neun Bots durch?

Schritt 2 und 3 greifen den Aufrufweg direkt an. **Hier geht es um die Kette,
an der der Fehler aufgefallen ist**: `elliott_wave_stocks` → `yfinance` →
`curl_cffi/__version__.py` → `Path(...).read_text()`.

```bash
python3 research/universum_trockenlauf/universum_trockenlauf.py \
    --json $E/04a_tabelle_1611.json > $E/04a_tabelle_1611.txt 2>&1
tail -20 $E/04a_tabelle_1611.txt

python3 research/universum_trockenlauf/universum_trockenlauf.py \
    --register-abschnitt 15.5 \
    --json $E/04b_tabelle_155.json > $E/04b_tabelle_155.txt 2>&1
head -3 $E/04b_tabelle_155.txt
```

**Erwartet:** beide Läufe kommen durch. In `04a` nennt die Kopfzeile
`Abschnitt 16.1.1` und es steht **keine** ACHTUNG-Zeile darin; in `04b` nennt
sie `Abschnitt 15.5`, gefolgt von `ACHTUNG: 15.5 ist NICHT die gueltige Tabelle`.

**Abbruchgrund:** ein `SCHREIBVERSUCH`, ein `TypeError`, oder ein Bot, der gar
nicht erst lädt.

Und jetzt ausgezählt:

```bash
python3 - <<'PY' 2>&1 | tee $E/04c_beide_richtungen.txt
import json, os
E = os.path.expanduser("~/Downloads/TB-44_ergebnisse")
def abw(p):
    b = json.load(open(os.path.join(E, p)))
    n = []
    for bot, e in b["bots"].items():
        sel = [f for f in e["falten"] if not f["bestaetigung"]]
        if [len(f["gemessen_H"]) for f in sel] != e["register"]["falten"]:
            n.append(bot)
    return b["register_abschnitt"], n
for p in ("04a_tabelle_1611.json", "04b_tabelle_155.json"):
    a, n = abw(p)
    print("Abschnitt %-8s -> %d abweichende Bot-Reihen von 9  %s" % (a, len(n), sorted(n)))
PY
```

**Erwartet — beide Zeilen, genau so:**

```
Abschnitt 16.1.1   -> 0 abweichende Bot-Reihen von 9  []
Abschnitt 15.5     -> 8 abweichende Bot-Reihen von 9  [… acht Bots, elliott_wave NICHT dabei]
```

**Abbruchgrund:** eine andere Zahl als **0** bzw. **8**.

---

## 5. Der Registernachtrag gegen eine frische Messung

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
`data/`, **nichts** unter `docs/VORREGISTRIERUNG_*` und **nichts** unter
`docs/projektfuehrung/`.

**Abbruchgrund:** irgendeine Abweichung.

---

## 7. Aufräumen und abgeben

```bash
rm -rf /tmp/tb44_alt
cd ~/Downloads
zip -r TB-44_wache_beide_pythons_MACLAUF.zip TB-44_ergebnisse
ls -la ~/Downloads/TB-44_wache_beide_pythons_MACLAUF.zip
```

**Abzugeben ist die ZIP-Datei
`~/Downloads/TB-44_wache_beide_pythons_MACLAUF.zip`.**
Sie liegt **ausserhalb des Repos** und wird **nicht** committet.

---

## Was gemeldet werden soll

| | |
|---|---|
| 1 | Welche Python-Fassung läuft auf dem Mac, und sagt `_NormalAccessor: True`? (Schritt 0) |
| 2 | Fiel **2a** auf dem alten Stand wirklich durch — **in beiden Richtungen**? Also: `TypeError` beim Lesen **und** `durchgelassen` beim Schreiben, `wirklich angelegt` nicht leer, `Opfer-Datei lebt noch: False`? |
| 3 | Sind in **2b** alle sechs Zeilen so wie erwartet — in beiden Richtungen? |
| 4 | Wie lautet in **3** die Schlusszeile, und welche Fassungen nennt `Python-Fassungen:`? Gab es ein `FEHL`? |
| 5 | Kam der volle Trockenlauf in **4** über alle neun Bots durch, und stehen in **4c** die Zahlen **0** und **8**? |
| 6 | Sagt **5** `Quelle beleg: trockenlauf` und `655 0` / `85 0`, und `KEIN BEFUND`? |
| 7 | Ist der Datenstand in **6** identisch, und ist `git status --short` sauber? |
| 8 | Falls etwas rot war: die betreffenden Zeilen aus `$E` wörtlich mitschicken. |

---

## In einfacher Sprache

**Was wir wissen wollten.** Im Trockenlauf sitzt ein Türsteher, der verhindern
soll, dass eine Messung versehentlich Dateien verändert. Auf deinem Mac ging er
zu weit — er blockierte sogar das blosse **Lesen**. Wir haben das repariert und
wollen jetzt auf deinem Rechner nachsehen, ob die Reparatur dort wirklich
greift.

**Was herauskam.** Das steht nach diesem Lauf fest, vorher nicht — deshalb
dieser Auftrag. Wichtig ist die Reihenfolge: Schritt 2 prüft **zuerst den alten
Stand**. Dort **muss** es schiefgehen. Erst danach hat es Aussagekraft, dass der
neue Stand sauber durchläuft.

**Warum das so ist.** Der Fehler steckt in einem Teil von Python, den es ab
Version 3.11 gar nicht mehr gibt. Dein Mac hat Version 3.9 — die Cloud, in der
die Reparatur entstanden ist, hat 3.11 oder neuer. **Der Fehler ist also
ausgerechnet auf dem Rechner sichtbar, auf dem es zählt, und in der Cloud fast
nicht.** Deshalb ist dieser Lauf der eigentliche Nachweis.

**Was das für dich heisst.** Starte den Befehl ganz oben und lass ihn
durchlaufen; er entscheidet nichts selbst und verändert nichts. Am Ende liegt
eine ZIP-Datei in deinem Download-Ordner — die ist das Ergebnis. Eine Sache
vorweg, damit sie nicht irritiert: **Die früher genannte Erwartung „70 von 70"
stimmt nicht mehr.** Der Test hat zwei Abschnitte dazubekommen und prüft jetzt
unter jeder Python-Version, die auf dem Rechner liegt. Die Zahl ist deshalb
höher (bei einer Version 132). Worauf es ankommt, ist nur: **nichts darf rot
sein.**
