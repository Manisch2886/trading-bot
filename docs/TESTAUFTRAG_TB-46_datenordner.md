# Testauftrag TB-46 — Zwei Datenbestände: Werkzeug und Wache (Mac)

**Autonom ausführbar.** Nichts an diesem Auftrag verlangt eine Entscheidung
während des Laufs. Er ist von oben nach unten abzuarbeiten; jeder Schritt sagt,
was zu erwarten ist und was ein Abbruchgrund wäre.

**Start (ein Befehl, kopierfertig):**

```
cd ~/trading-bot && claude --remote-control "Lies die Datei docs/TESTAUFTRAG_TB-46_datenordner.md und arbeite sie als autonome Claude-Code-Sitzung vollständig eigenständig ab, wie darin beschrieben."
```

---

## Warum der Mac hier der eigentliche Nachweis ist

| Punkt | Was die Cloud strukturell nicht konnte |
|---|---|
| **Python 3.9.6** | In der Cloud lief alles auf **3.10, 3.11, 3.12 und 3.13** — je 69 von 69 Prüfungen grün. ⚠️ **3.9 war dort nicht installiert** (geprüft: nur 3.10 bis 3.13 vorhanden). Für 3.9 ist bislang **nur die Syntax** geprüft, nicht der Lauf. TB-43/TB-44 haben gezeigt, dass genau dieser Unterschied ein Werkzeug auf dem Mac gar nicht starten lässt. |
| **Ein echter Snapshot über 223 Dateien** | In der Cloud wurde nur an Wegwerf-Verzeichnissen mit zwei Dateien gezogen. **211 MB zu kopieren und jede Datei byteweise gegenzuprüfen** ist ein anderer Lastfall — und es ist der Fall, der am Tag des signierten Tags eintritt. |
| **Der Live-Bestand** | Binance und yfinance sind aus der Cloud **gesperrt (403)**. Ein Abruf, der `data/` fortschreibt, war dort nicht auslösbar. |
| **Die Paketlage** | ⚠️ In der Cloud fehlten **pandas, numpy, scipy, dateparser, yfinance, binance, fastapi, pandas_market_calendars, python-telegram-bot und tzdata vollständig** und mussten nachinstalliert werden — und zwar in Fassungen, die der Mac nicht hat (**pandas 3.0.5** gegen **2.3.3** auf dem Mac, eine Hauptversion Unterschied). `scipy` gibt es auf dem Mac gar nicht. |
| **Die bekannt roten Tests** | Die Liste aus der Aufgabenstellung wurde **auf dem Mac** gemessen. In der Cloud sah einer davon anders aus (Schritt 5 prüft das nach). |

> ⚠️ **Dieser Auftrag ändert nichts am Betrieb.** Kein `--echt`, keine Order,
> keine Kursdatei, kein `live_params.py`, keine Crontab, kein Registertext.
> **Es wird kein Snapshot committet.** Wenn ein Schritt nach `data/` schreiben
> will, ist das ein **Abbruchgrund**, kein Zwischenfall.

> ⚠️ **Der echte Snapshot in Schritt 4 wird nach `~/Downloads` gezogen, nicht
> ins Repo**, und am Ende wieder gelöscht. 211 MB gehören nicht in diesen
> Zweig — der Snapshot für den Selektionslauf wird am Tag des signierten Tags
> gezogen, nicht heute.

---

## 0. Zweig auschecken, Fassungen festhalten, die neun Datenbanken sichern

```bash
cd ~/trading-bot
git fetch origin
git checkout claude/new-session-mmsrys
git pull origin claude/new-session-mmsrys
git log --oneline -3

mkdir -p ~/Downloads/TB-46_ergebnisse
E=~/Downloads/TB-46_ergebnisse

# --- Fassungen -------------------------------------------------------------
python3 -VV                                    2>&1 | tee    $E/00_python.txt
trading-env/bin/python3 -VV                    2>&1 | tee -a $E/00_python.txt
trading-env/bin/python3 -c "import pandas, numpy; print('pandas', pandas.__version__, 'numpy', numpy.__version__)" 2>&1 | tee -a $E/00_python.txt
trading-env/bin/python3 -c "import dateparser; print('dateparser', dateparser.__version__)" 2>&1 | tee -a $E/00_python.txt
trading-env/bin/python3 -c "import scipy; print('scipy', scipy.__version__)" 2>&1 | tee -a $E/00_python.txt
which node gh timeout                          2>&1 | tee -a $E/00_python.txt
df -h .                                        2>&1 | tee -a $E/00_python.txt

# --- Sicherung der neun Datenbanken ---------------------------------------
mkdir -p ~/Downloads/TB-46_db_sicherung
cp -p paper_trading_*.db ~/Downloads/TB-46_db_sicherung/
shasum -a 256 paper_trading_*.db 2>&1 | tee $E/00_db_vorher.txt
ls -1 paper_trading_*.db | wc -l               2>&1 | tee -a $E/00_db_vorher.txt
```

**Erwartet:** Der Zweig enthält `TB-46: zwei Datenbestaende`.
`trading-env/bin/python3` ist **3.9.6**. `scipy` **fehlt** (ImportError — das
ist richtig so und kein Abbruchgrund). **Neun** `paper_trading_*.db` gesichert.
Mindestens **1 GB** frei (Schritt 4 kopiert 211 MB).

> ⚠️ **Alle folgenden Python-Aufrufe benutzen `trading-env/bin/python3`, nicht
> `python3`** — `/usr/bin/python3` hat weder `binance` noch `dateparser`.

**Abbruchgrund:** `trading-env` ist nicht 3.9.x; die Sicherung ist
unvollständig (weniger als neun Dateien); weniger als 1 GB frei.

---

## 1. Der Datenstand — VOR allem anderen

```bash
trading-env/bin/python3 research/registernachtrag_tb41/pruefe_register.py \
    --nur datenstand 2>&1 | tee $E/01_datenstand_vorher.txt

trading-env/bin/python3 shared/snapshot.py --nur-hash 2>&1 | tee -a $E/01_datenstand_vorher.txt
```

**Erwartet: beide Aufrufe nennen dieselbe Zahl** —
`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223
Dateien**.

⚠️ Der zweite Aufruf ist kein Doppel, sondern der Nachweis, dass das neue
Werkzeug **dieselbe** Rechnung benutzt wie das Register und keine zweite
daneben.

**Abbruchgrund:** ein anderer Hash, eine andere Dateizahl, oder die zwei
Aufrufe nennen **verschiedene** Werte.

---

## 2. Die Wache über das Snapshot-Werkzeug — auf Python 3.9

```bash
trading-env/bin/python3 shared/test_snapshot.py 2>&1 | tee $E/02_test_snapshot.txt
echo "Rueckgabewert: $?"                       2>&1 | tee -a $E/02_test_snapshot.txt
```

**Erwartet: 69 von 69 Prüfungen bestanden, 0 fehlgeschlagen**, Rückgabewert 0.

⚠️ **Das ist der wichtigste Schritt dieses Auftrags.** In der Cloud war er auf
vier Python-Fassungen grün — **3.9 war nicht darunter.**

Darin besonders zu lesen:

* `snapshot.gesamthash(data/) reproduziert den registrierten Hash` — das
  Werkzeug und das Register rechnen dasselbe.
* Jede Zeile `ohne die Wache: …` — das ist die Mutationsprobe. Sie zeigt, dass
  die jeweilige Prüfung **beißt**: an der Fassung ohne sie geht dieselbe Lage
  durch.
* `3e ohne die Wache: aus 'nicht messbar' wird ein Urteil 'veraendert'` — die
  Lehre aus TB-45, hier am Ablauf vorgeführt.
* Abschnitt 5: `der Datenstand-Hash ist derselbe wie vor dem Lauf`.

**Abbruchgrund:** irgendeine Prüfung rot. ⚠️ **Auch ein Fehler mit dem
Vermerk `(Anker)` ist ein Abbruchgrund** — er bedeutet, dass die Probe die
Wache nicht mehr findet, die sie prüfen soll, und dann prüft sie nichts.

---

## 3. Der Trockenlauf am echten Bestand — es darf nichts entstehen

```bash
trading-env/bin/python3 shared/snapshot.py \
    --quelle data --ziel ~/Downloads/TB-46_snapshot 2>&1 | tee $E/03_trockenlauf.txt
echo "Rueckgabewert: $?"                       2>&1 | tee -a $E/03_trockenlauf.txt
ls -la ~/Downloads/TB-46_snapshot 2>&1 | tee -a $E/03_trockenlauf.txt
```

**Erwartet:** Rückgabewert 0, die Ausgabe nennt
`Datenstand d9449faf…`, `Kursdateien 223`, und darunter **`TROCKENLAUF -
nichts kopiert`**. Der Ordner `~/Downloads/TB-46_snapshot` **existiert nicht**
(`ls` meldet ihn als fehlend — das ist die erwartete Antwort).

**Abbruchgrund:** der Zielordner ist entstanden, oder es wurden Dateien
kopiert.

---

## 4. Der echte Snapshot — 223 Dateien, 211 MB, jede byteweise geprüft

⚠️ **Das ist der Lastfall, den die Cloud nicht hatte.** Er dauert; auf einer
langsamen Platte mehrere Minuten.

```bash
time trading-env/bin/python3 shared/snapshot.py \
    --quelle data --ziel ~/Downloads/TB-46_snapshot --ziehen \
    --json $E/04_snapshot.json 2>&1 | tee $E/04_ziehen.txt
echo "Rueckgabewert: $?"                       2>&1 | tee -a $E/04_ziehen.txt

H=d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84
ls -1 ~/Downloads/TB-46_snapshot/$H | wc -l    2>&1 | tee -a $E/04_ziehen.txt
du -sh ~/Downloads/TB-46_snapshot/$H           2>&1 | tee -a $E/04_ziehen.txt
```

**Erwartet:** Rückgabewert 0, `GEZOGEN - 223 Datei(en)`, der Zielordner heißt
**genau** `d9449faf51bff…`, enthält **224** Einträge (223 Kursdateien + das
`MANIFEST.json`) und wiegt rund **202 MB**.

**Abbruchgrund:** eine Meldung `ABWEICHUNG bei …` (dann stimmt eine Kopie
nicht mit der Quelle überein — das ist ein Befund über Platte oder
Dateisystem, kein Fehler des Werkzeugs); eine andere Dateizahl; ein anderer
Ordnername.

### 4b. Die Zeitstempel und das Manifest

```bash
stat -f "%N %m" data/AAPL_1d.csv ~/Downloads/TB-46_snapshot/$H/AAPL_1d.csv \
    2>&1 | tee $E/04b_zeitstempel.txt
trading-env/bin/python3 -c "
import json; m = json.load(open('$HOME/Downloads/TB-46_snapshot/$H/MANIFEST.json'))
print('Dateien im Manifest :', len(m['dateien']))
print('Kursdateien         :', m['kursdateien'])
print('Datenstand          :', m['datenstand'])
print('Zeitpunkt (UTC)     :', m['zeitpunkt_utc'])
print('Verfahren           :', m['verfahren'][:60])
" 2>&1 | tee $E/04b_manifest.txt
```

**Erwartet:** beide Zeitstempel **gleich** (`copy2` erhält sie). Im Manifest:
**223** Dateien, **223** Kursdateien, der registrierte Hash, ein Zeitpunkt,
der auf `+00:00` endet.

**Abbruchgrund:** abweichende Zeitstempel; ein Zeitpunkt ohne `+00:00`.

### 4c. Nachprüfen — dreimal, für alle drei Ausgänge

```bash
# (1) unveraendert
trading-env/bin/python3 shared/snapshot.py --pruefen ~/Downloads/TB-46_snapshot/$H \
    2>&1 | tee $E/04c_pruefen_unveraendert.txt
echo "Rueckgabewert: $?"                       2>&1 | tee -a $E/04c_pruefen_unveraendert.txt

# (2) ein zweiter Zug in dasselbe Ziel - muss abbrechen, nie ueberschreiben
trading-env/bin/python3 shared/snapshot.py --quelle data \
    --ziel ~/Downloads/TB-46_snapshot --ziehen 2>&1 | tee $E/04c_zweiter_zug.txt
echo "Rueckgabewert: $?"                       2>&1 | tee -a $E/04c_zweiter_zug.txt

# (3) veraendert - an einer KOPIE, nie am Snapshot selbst
cp -Rp ~/Downloads/TB-46_snapshot/$H ~/Downloads/TB-46_probe
echo "# eine Zeile zu viel" >> ~/Downloads/TB-46_probe/AAPL_1d.csv
trading-env/bin/python3 shared/snapshot.py --pruefen ~/Downloads/TB-46_probe \
    2>&1 | tee $E/04c_pruefen_veraendert.txt
echo "Rueckgabewert: $?"                       2>&1 | tee -a $E/04c_pruefen_veraendert.txt

# (4) nicht pruefbar
rm ~/Downloads/TB-46_probe/MANIFEST.json
trading-env/bin/python3 shared/snapshot.py --pruefen ~/Downloads/TB-46_probe \
    2>&1 | tee $E/04c_pruefen_unpruefbar.txt
echo "Rueckgabewert: $?"                       2>&1 | tee -a $E/04c_pruefen_unpruefbar.txt
rm -rf ~/Downloads/TB-46_probe
```

**Erwartet — die drei Ausgänge müssen unterscheidbar sein:**

| Aufruf | Ausgabe | Rückgabewert |
|---|---|---:|
| (1) unberührt | `UNVERAENDERT` | **0** |
| (2) zweiter Zug | `ABBRUCH: … existiert bereits` | **2** |
| (3) eine Zeile mehr | `VERAENDERT` und `AAPL_1d.csv` genannt | **1** |
| (4) Manifest weg | `NICHT PRUEFBAR` | **2** |

⚠️ **Der Rückgabewert ist hier die Aussage, nicht die Textausgabe.** Wenn (4)
den Wert 0 liefert, ist das genau der Ausfall, gegen den dieser Teil
geschrieben ist.

**Abbruchgrund:** irgendeiner der vier Werte stimmt nicht; (2) hat den
bestehenden Snapshot überschrieben.

---

## 5. Der Basislauf — alle Testdateien, mit Zeitgrenze

⚠️ Der Mac hat **kein GNU `timeout`**. Der Basislauf bringt seine Zeitgrenze
selbst mit und **beendet den Kindprozess** danach.

```bash
trading-env/bin/python3 research/datenordner_schnitt/basislauf.py \
    --grenze 420 --json $E/05_basislauf.json 2>&1 | tee $E/05_basislauf.txt
echo "Rueckgabewert: $?"                       2>&1 | tee -a $E/05_basislauf.txt
```

**Erwartet: 63 Testdateien.** Ausdrücklich **nicht** grün, und das ist richtig:

| Datei | erwartet auf dem Mac |
|---|---|
| `dashboard/test_portfolio_sicht.py` | bekannt rot (1 Fehler) |
| `shared/test_stabile_sortierung.py` | bekannt rot (3 Fehler) |
| `shared/test_wellenauswahl.py` | bekannt rot (1 Fehler) |
| `system/test_log_rotation.py` | bekannt rot (1 Fehler) |
| `research/exposure_messung/test_exposure_kern.py` | bekannt rot (1 Fehler) |
| `research/hrp_portfolio/test_hrp_core.py` | bekannt rot (`scipy` fehlt) |
| `research/drawdown_reihenfolge/test_drawdown.py` | **ungeprüft** (verlangt ein Bot-Argument) |
| `research/fib_score_stufen/test_stufen.py` | **ungeprüft** |
| `research/elliott_wave_params/test_params.py` | **ungeprüft** |
| `shared/test_drawdown_beide_masse.py` | **Zeitgrenze** (terminiert nicht) |

**Alles andere muss grün sein.** Der Lauf markiert jede Abweichung selbst mit
`<-- UNERWARTET` und liefert dann Rückgabewert 1.

> ⚠️ **Auch das Gegenteil ist zu melden:** ein als bekannt rot geführter Test,
> der auf dem Mac **grün** ist, wird ebenfalls als `UNERWARTET` markiert.

**In der Cloud sind vier davon grün gewesen**, und bei drei ist der Grund
**offen** — dieser Lauf entscheidet, welche Umgebung recht hat:

| Datei | Cloud | Liste (Mac 17.09.) | Grund |
|---|---|---|---|
| `research/hrp_portfolio/test_hrp_core.py` | grün | `scipy` fehlt | **geklärt** — `scipy` war in der Cloud nachinstalliert |
| `dashboard/test_portfolio_sicht.py` | **91/91 grün** | 1 Fehler | ⚠️ offen |
| `research/exposure_messung/test_exposure_kern.py` | grün | 1 Fehler | ⚠️ offen |
| `system/test_log_rotation.py` | **117/117 grün** | 1 Fehler | ⚠️ offen |

**Und zwei rote, die nicht in der Liste stehen** — in der Cloud gemessen, dort
**nicht** von TB-46 verursacht (nachgewiesen gegen denselben Commit ohne die
Neuzugänge):

| Datei | Cloud | erwartet auf dem Mac |
|---|---|---|
| `shared/test_leeres_symbol.py` | 43/45 — beide Fehler sind Gegenproben, die einen **echten Abruf** brauchen | ⚠️ auf dem Mac ist Binance erreichbar — **hier sollte er grün sein** |
| `shared/test_stille_ausfaelle.py` | 23/24, `teil_2` scheitert an einem `git commit` im nachgebauten Repo | ⚠️ unklar — bitte melden |
| `shared/test_zuteilung.py` | rot: `ProxyError … api.binance.com` | ⚠️ auf dem Mac ist Binance erreichbar — **hier sollte er grün sein** |

⚠️ **Diese drei sind der eigentliche Grund, warum der Basislauf hier noch einmal
läuft:** alle drei hängen an etwas, das die Cloud strukturell nicht hat.

**Abbruchgrund:** eine Datei, die weder in der Tabelle steht noch grün ist.

---

## 6. Die Erhebung nachmessen — dieselben Zahlen auf 3.9?

```bash
trading-env/bin/python3 research/datenordner_schnitt/erhebung.py \
    --json $E/06_erhebung.json 2>&1 | tee $E/06_erhebung.txt
trading-env/bin/python3 research/kursdaten_neuaufbau/datenwege.py \
    2>&1 | tail -5 | tee $E/06_datenwege_tb34.txt
```

**Erwartet — dieselben Zahlen wie in der Cloud:**

* **183** Module mit Fundstelle, **182** auf dem echten Bestand
* **29** bauen den Pfad selbst, **145** beziehen ihn mittelbar, **8** nennen
  ihn nur
* **11** Schreiber
* Abschnitt 9: `davon mit eigenem PFADBAU: 0 - keine` — **keine der neun
  `forward_test.py`, keine `live_params.py`, keine `equity_simulation.py` baut
  selbst einen Pfad auf `data/`**
* Aus TB-34: `37 Module lesen data/ unmittelbar, 64 weitere … zusammen 101`

**Abbruchgrund:** abweichende Zahlen. ⚠️ Eine Erhebung, die auf zwei
Python-Fassungen verschieden zählt, ist in beiden Fassungen nicht belastbar.

---

## 7. Der Repopreis — die Zahl aus der Aufgabenstellung

```bash
trading-env/bin/python3 research/datenordner_schnitt/repopreis.py \
    --json $E/07_repopreis.json 2>&1 | tee $E/07_repopreis.txt
```

**Erwartet:** `data/` wiegt **211,0 MB** in 223 Dateien; die byteidentische
Kopie lässt das Packfile um **weit unter 1 %** wachsen; `Derselbe Inhalt,
derselbe Blob: ja`.

**Abbruchgrund:** keiner — ⚠️ aber wenn `Derselbe Inhalt, derselbe Blob` hier
**NEIN** sagt, ist das ein Befund über die git-Fassung des Macs und gehört
gemeldet.

---

## 8. Alles zurück, und der Nachweis dafür

```bash
# Der Snapshot war ein Testobjekt - er wird nicht behalten.
rm -rf ~/Downloads/TB-46_snapshot
rm -rf ~/Downloads/TB-46_probe

# --- Der Datenstand danach -------------------------------------------------
trading-env/bin/python3 shared/snapshot.py --nur-hash 2>&1 | tee $E/08_datenstand_nachher.txt

# --- Die neun Datenbanken --------------------------------------------------
shasum -a 256 paper_trading_*.db 2>&1 | tee $E/08_db_nachher.txt
diff $E/00_db_vorher.txt $E/08_db_nachher.txt && echo "DATENBANKEN IDENTISCH" \
    2>&1 | tee -a $E/08_db_nachher.txt

# --- Der Arbeitsbaum -------------------------------------------------------
git status --porcelain            2>&1 | tee $E/08_git_status.txt
git status --porcelain -- data    2>&1 | tee -a $E/08_git_status.txt

# --- Die ZIP ---------------------------------------------------------------
cd ~/Downloads && zip -r TB-46_mac_ergebnisse.zip TB-46_ergebnisse >/dev/null \
    && ls -la TB-46_mac_ergebnisse.zip
```

**Erwartet:**

* Datenstand **unverändert** `d9449faf…`, **223 Dateien** — dieselbe Zahl wie
  in Schritt 1.
* `DATENBANKEN IDENTISCH` (die `diff`-Ausgabe ist leer).
* `git status --porcelain` ist **leer**. ⚠️ Insbesondere unter `data/` **nichts**.
* Eine ZIP-Datei in `~/Downloads`.

**Abbruchgrund:** ein anderer Datenstand; eine Datenbank hat sich geändert;
`git status` ist nicht leer.

---

## Was zurückzuschicken ist

`~/Downloads/TB-46_mac_ergebnisse.zip`.

**Und im Begleittext die vier Zahlen, auf die es ankommt:**

1. die Python-Fassung von `trading-env` (erwartet **3.9.6**),
2. das Ergebnis von `shared/test_snapshot.py` (erwartet **69/69**),
3. Dateizahl und Ordnername des echten Snapshots (erwartet **223** in
   `d9449faf…`),
4. die vier Rückgabewerte aus Schritt 4c (erwartet **0 / 2 / 1 / 2**).

---

## In einfacher Sprache

**Was wir wissen wollten.**
Das Register verlangt zwei Kursdatenbestände: einen, der täglich weiterläuft,
und einen, der eingefroren wird und den Namen seines eigenen Fingerabdrucks
trägt. In der Cloud ist das Werkzeug gebaut worden, das diese eingefrorene
Kopie zieht und später nachprüft. Geprüft wurde es dort an einem
Spielverzeichnis mit zwei Dateien und auf vier Python-Ausgaben — **die Ausgabe
deines Rechners war nicht darunter**, weil es sie in der Cloud nicht gibt.

**Was herauskommt.**
Eine Reihe von Protokolldateien in `~/Downloads/TB-46_ergebnisse`, am Ende zu
einer ZIP-Datei gepackt. Jeder Schritt sagt vorher, welche Zahl zu erwarten
ist.

**Warum das so ist.**
Ein Werkzeug, das eine eingefrorene Kopie zieht, hat genau eine Aufgabe: zu
merken, wenn etwas nicht stimmt. Ein solches Werkzeug lässt sich nicht daran
prüfen, dass es im Normalfall funktioniert — es muss vorgeführt werden, dass
es im **Fehlerfall** anhält. Deshalb macht dieser Auftrag absichtlich Dinge
kaputt: er hängt eine Zeile an eine Kopie, löscht ein Verzeichnisverzeichnis,
zieht zweimal in denselben Ordner. Jedes Mal ist vorher aufgeschrieben, welche
Zahl das Werkzeug zurückgeben muss.

**Was das für dich heißt.**
Du startest einen einzigen Befehl (ganz oben) und lässt ihn durchlaufen. Er
ändert nichts an deinen Bots, nichts an den Kursdaten und nichts an den neun
Datenbanken — das wird am Ende nachgerechnet und ausdrücklich bestätigt. Er
legt zwischendurch eine 202-MB-Kopie in deinem Download-Ordner an und löscht
sie am Ende wieder; sorge dafür, dass dort rund ein Gigabyte frei ist.
**Entscheiden musst du eine Sache, und sie steht nicht in diesem Auftrag,
sondern in `docs/ERGEBNIS_TB-46_datenordner.md`:** ob die beiden Ordner so
heißen sollen, wie das Register es aufgeschrieben hat, oder so, wie die Messung
es empfiehlt. Dieser Auftrag misst nur die Grundlage dafür.
