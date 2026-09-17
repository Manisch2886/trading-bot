# Testauftrag TB-45 — Stille Ausfälle (Mac)

**Autonom ausführbar.** Nichts an diesem Auftrag verlangt eine Entscheidung
während des Laufs. Er ist von oben nach unten abzuarbeiten; jeder Schritt sagt,
was zu erwarten ist und was ein Abbruchgrund wäre.

**Start (ein Befehl, kopierfertig):**

```
cd ~/trading-bot && claude --remote-control "Lies die Datei docs/TESTAUFTRAG_TB-45_stille_ausfaelle.md und arbeite sie als autonome Claude-Code-Sitzung vollständig eigenständig ab, wie darin beschrieben."
```

---

**Warum der Mac hier der eigentliche Nachweis ist.** Zwei der fünf Teile sind
in der Cloud **strukturell nicht vollständig prüfbar**:

| Teil | Was die Cloud nicht kann |
|---|---|
| **Teil 3** (`_ist_geraet`) | ⚠️ Auf dem Mac **existieren `results/<bot>` und `logs/<bot>`** (der Cron hat sie angelegt), in einem frischen Checkout nicht. **Genau daran hing der Befund.** In der Cloud wurde die Mac-Lage nachgestellt; hier ist sie echt. |
| **Teil 5** (`fromisoformat`) | Der Betrieb läuft auf **Python 3.9.6**. In der Cloud wurde mit einem nachinstallierten 3.9.23 gemessen. Und: **Binance und yfinance sind aus der Cloud gesperrt (403)** — der Live-Abruf lief dort nur über eine Attrappe. |

> ⚠️ **Dieser Auftrag ändert nichts am Betrieb.** Kein `--echt`, keine Order,
> keine Kursdatei, kein `live_params.py`, keine Datei unter
> `docs/projektfuehrung/`, keine Crontab. Wenn ein Schritt schreiben will, ist
> das ein **Abbruchgrund**, kein Zwischenfall.

> ⚠️ **Die neun Live-Datenbanken werden in Schritt 0 gesichert und in
> Schritt 8 als byteweise identisch nachgewiesen.** Schritt 5 lässt zwei
> `forward_test.py` wirklich laufen — mit umgelenkter Datenbank, aber der
> Nachweis gehört trotzdem geführt. Sie sind seit Verfahren B die **einzige
> OOS-Evidenz** des Projekts und **nicht neu berechenbar**.

---

## 0. Voraussetzungen und Sicherung

```bash
cd ~/trading-bot
git fetch origin
git checkout claude/new-session-l4l5k1
git pull origin claude/new-session-l4l5k1
git log --oneline -3

mkdir -p ~/Downloads/TB-45_ergebnisse
E=~/Downloads/TB-45_ergebnisse

# --- Fassungen -------------------------------------------------------------
python3 -VV                                             2>&1 | tee    $E/00_python.txt
trading-env/bin/python3 -VV                             2>&1 | tee -a $E/00_python.txt
trading-env/bin/python3 -c "import pandas, numpy; print('pandas', pandas.__version__, 'numpy', numpy.__version__)" 2>&1 | tee -a $E/00_python.txt
trading-env/bin/python3 -c "import dateparser; print('dateparser', dateparser.__version__)" 2>&1 | tee -a $E/00_python.txt
which node gh                                           2>&1 | tee -a $E/00_python.txt

# --- Die Lage, an der Teil 3 hängt: existieren die Ordner? ------------------
ls -d results/*/ logs/*/ 2>&1 | tee $E/00_ordner.txt

# --- Sicherung der neun Datenbanken ----------------------------------------
mkdir -p ~/Downloads/TB-45_db_sicherung
cp -p paper_trading_*.db ~/Downloads/TB-45_db_sicherung/
shasum -a 256 paper_trading_*.db 2>&1 | tee $E/00_db_vorher.txt
```

**Erwartet:** Der Zweig enthält `TB-45: stille Ausfaelle`. `trading-env` auf
**Python 3.9.6**. In `00_ordner.txt` stehen `results/<bot>/` **und**
`logs/<bot>/` für mehrere Bots.

> ⚠️ **Wenn `logs/` und `results/` je Bot LEER sind oder fehlen**, ist die
> Mac-Lage aus Teil 3 hier nicht gegeben, und Schritt 4 belegt dann dasselbe
> wie die Cloud. **Das ist zu melden**, nicht zu übergehen.

**Abbruchgrund:** Python ist nicht 3.9.x; die Sicherung der neun Datenbanken
ist unvollständig.

---

## 1. Der Datenstand — VOR allem anderen

```bash
python3 research/registernachtrag_tb41/pruefe_register.py \
    --nur datenstand 2>&1 | tee $E/01_datenstand_vorher.txt
```

**Erwartet:** `d9449faf51bffaaa…`, **223 Dateien**.
**Abbruchgrund:** ein anderer Hash oder eine andere Zahl.

---

## 2. Teil 1 und 2 — die zwei blinden Wachen

Dieser Test stellt sich seine Lagen selbst her (Kopie des Arbeitsbaums, eigene
git-Geschichte). Er fasst weder `data/` noch die echten Datenbanken an.

```bash
python3 shared/test_stille_ausfaelle.py 2>&1 | tee $E/02_stille_ausfaelle.txt
```

**Erwartet: 27 von 27 bestanden, 0 fehlgeschlagen.** Darin insbesondere:

* `Lage A … - gruen` für **beide** Prüfer — ⚠️ **das ist die Negativ-Probe.**
  Ein leeres Ergebnis aus einem *gelungenen* git-Aufruf **ist** der Nachweis
  und muss grün bleiben.
* `Lage B … - ROT` für beide Prüfer.
* `der unveraenderte Stand meldet in Lage B faelschlich 'bestanden'` — das ist
  der Befund selbst, am Stand aus `origin/main` nachgewiesen.
* Abschnitt 3: `die Drei-Punkt-Form sieht sie NICHT` — die gemessene Antwort
  auf T38.9.

**Und die beiden reparierten Prüfer selbst:**

```bash
python3 shared/test_kursdaten.py          2>&1 | tee $E/02_kursdaten.txt
python3 dashboard/test_portfolio_sicht.py 2>&1 | tee $E/02_portfolio_sicht.txt
```

**Erwartet `shared/test_kursdaten.py`: 88 von 88, 0 fehlgeschlagen.**
⚠️ **Er ist seit TB-42 grün und muss es bleiben.** Die Zahl ist von 81 auf 88
gestiegen, weil die beiden `forward_test.py` jetzt verändert sind und die
Parameter-Schleife deshalb wirklich läuft — **genau das ist der Sinn der
Wache.** Darin müssen stehen:
`strategies/elliott_wave/forward_test.py: kein Handelsparameter veraendert`
und `… derselbe Satz Parameter aus live_params.py`.

**Erwartet `dashboard/test_portfolio_sicht.py`:** ⚠️ **In der Cloud war er
GRÜN (90/90)** — die Aufgabenliste führte ihn als „bekannt rot, beide",
das stimmt für die Cloud nicht. Auf dem Mac ist er **bekannt rot**, weil zwei
Bots `MIN_LIVE_CLOSED_TRADES` erreicht haben und das gemeinsame Fenster leer
ist.

> ⭐ **Die Frage, die dieser Schritt beantworten soll:** Ist er aus **demselben**
> Grund rot wie vorher — dem leeren gemeinsamen Fenster — oder aus einem
> **anderen**? Dazu die roten Zeilen wörtlich in die Rückmeldung übernehmen.
> **Ein Test, der aus zwei Gründen rot sein kann, verdeckt den zweiten.**
> Kommt `der Vergleich gegen origin/main kam zustande` als **rot** vor, ist
> `origin/main` nicht geholt — dann zuerst `git fetch origin main` und
> wiederholen.

---

## 3. Teil 3 — die Gegenprobe am ALTEN Stand

**Zuerst zeigen, dass der Befund auf diesem Rechner existiert.** Ohne diesen
Schritt belegt Schritt 4 nur, dass etwas grün ist.

```bash
git stash list > $E/03_stash_vorher.txt        # muss unverändert bleiben
mkdir -p /tmp/tb45_alt && cd /tmp/tb45_alt
git -C ~/trading-bot show origin/main:research/universum_trockenlauf/loaderlauf.py > /tmp/tb45_alt/loaderlauf_alt.py
cd ~/trading-bot
python3 - <<'PY' 2>&1 | tee $E/03_ist_geraet_alt.txt
import importlib.util, os, sys, tempfile
spec = importlib.util.spec_from_file_location("ll_alt", "/tmp/tb45_alt/loaderlauf_alt.py")
alt = importlib.util.module_from_spec(spec); spec.loader.exec_module(alt)
ordner = tempfile.mkdtemp()
print("ALTER Stand  _ist_geraet(<Verzeichnis>) =", alt._ist_geraet(ordner))
print("ALTER Stand  _ist_geraet('/dev/null')   =", alt._ist_geraet("/dev/null"))
sys.path.insert(0, "research/universum_trockenlauf")
import loaderlauf as neu
print("NEUER Stand  _ist_geraet(<Verzeichnis>) =", neu._ist_geraet(ordner))
print("NEUER Stand  _ist_geraet('/dev/null')   =", neu._ist_geraet("/dev/null"))
PY
```

**Erwartet:**

```
ALTER Stand  _ist_geraet(<Verzeichnis>) = True      <- der Befund
ALTER Stand  _ist_geraet('/dev/null')   = True
NEUER Stand  _ist_geraet(<Verzeichnis>) = False     <- repariert
NEUER Stand  _ist_geraet('/dev/null')   = True      <- Ausnahme bleibt
```

**Abbruchgrund:** `NEUER Stand … = True` für das Verzeichnis.

---

## 4. Teil 3 — der Trockenlauf, dort wo die Ordner wirklich existieren

```bash
python3 research/universum_trockenlauf/test_universum_trockenlauf.py \
    2>&1 | tee $E/04_trockenlauf.txt
```

**Erwartet: 356/356 Prüfungen bestanden** (die Zahl hängt davon ab, wie viele
Python-Fassungen auf dem Rechner liegen — Teil L fährt jede ab; **entscheidend
ist: 0 gescheitert**).

**Darin besonders zu prüfen:**

* `B2: der Schreibschutz war waehrend des Laufs nachweislich aktiv - je Bot
  sind results/<bot> UND logs/<bot> als unterdrueckter Versuch verzeichnet`
  — ⭐ **Das ist der Schritt, der in der Cloud strukturell nichts belegen
  konnte.** Auf dem Mac gibt es diese Ordner; vorher war B2 deshalb hier rot
  und in der Cloud grün.
* `N5 vorhanden der makedirs-Versuch wird aufgezeichnet` — **beide** Lagen
  („fehlt" und „vorhanden") müssen grün sein.
* `N11 vorhanden makedirs ohne exist_ok wirft weiterhin FileExistsError`.
* `B3`/`B4`: der Lauf hat unter `logs/` und `results/` **nichts** angelegt.

**Abbruchgrund:** B2 rot, oder `N5 vorhanden` rot.

---

## 5. Teil 4 — ein leeres Symbol beendet keinen Lauf mehr

⚠️ **Dieser Schritt lässt `forward_test.py` beider Elliott-Bots wirklich
laufen.** Die Datenbank wird dabei in einen Wegwerf-Ordner umgelenkt
(`strategy_paths.get_strategy_paths` ist ersetzt); `results/` und `logs/`
ebenso. **Trotzdem gilt die Sicherung aus Schritt 0.**

```bash
python3 shared/test_leeres_symbol.py 2>&1 | tee $E/05_leeres_symbol.txt
```

**Erwartet: 45 von 45 bestanden, 0 fehlgeschlagen.** Darin:

* `auf echten Daten bricht die ALTE Fassung bei einem leeren Rahmen ab` —
  der Befund, gegen `origin/main` gemessen.
* `auf echten Daten Pivot fuer Pivot, Spalte fuer Spalte unveraendert` — ⭐
  **die Gegenprobe: am Signal ändert sich nichts.**
* `genau EINE Meldung zum ausgelassenen Symbol`.
* `die Trades der uebrigen Symbole sind Spalte fuer Spalte identisch` **und**
  `es sind ueberhaupt Trades entstanden` — beide Zeilen zusammen, sonst
  vergleicht der Test zwei leere Tabellen.
* Abschnitt 3, die Umfrage: **alle neun** Bots überleben ein leeres Symbol.

**Und die Gegenprobe am alten Stand** (zeigt, dass es hier je ein Problem gab):

```bash
cd ~/trading-bot
git stash push -- strategies/elliott_wave/forward_test.py \
    strategies/elliott_wave/zigzag_indicator.py \
    strategies/elliott_wave_stocks/forward_test.py \
    strategies/elliott_wave_stocks/zigzag_indicator.py 2>/dev/null || true
git checkout origin/main -- strategies/elliott_wave/forward_test.py \
    strategies/elliott_wave/zigzag_indicator.py \
    strategies/elliott_wave_stocks/forward_test.py \
    strategies/elliott_wave_stocks/zigzag_indicator.py
python3 shared/test_leeres_symbol.py 2>&1 | tee $E/05_leeres_symbol_ALT.txt
git checkout claude/new-session-l4l5k1 -- strategies/elliott_wave/forward_test.py \
    strategies/elliott_wave/zigzag_indicator.py \
    strategies/elliott_wave_stocks/forward_test.py \
    strategies/elliott_wave_stocks/zigzag_indicator.py
git status --short 2>&1 | tee $E/05_status_nach_ruecknahme.txt
```

**Erwartet in `05_leeres_symbol_ALT.txt`: 23 von 35, 12 fehlgeschlagen**,
darunter `elliott_wave: der Lauf kommt trotz des leeren Symbols durch`
(gescheitert) — **der ganze Lauf endet, das ist der Befund**.

**Abbruchgrund:** `05_status_nach_ruecknahme.txt` zeigt nach der Rücknahme
noch Änderungen an den vier Dateien.

---

## 6. Teil 5 — `fromisoformat`, auf dem echten 3.9.6 und am echten Endpunkt

⚠️ **Dieser Teil ändert `shared/entscheidungskerze.py` nicht.** Er misst.

```bash
python3 research/fromisoformat_registerfrage/messung.py \
    --zweite-fassung trading-env/bin/python3 2>&1 | tee $E/06_fromisoformat.txt
python3 research/fromisoformat_registerfrage/messung.py \
    --zweite-fassung trading-env/bin/python3 --json 2>&1 | tee $E/06_fromisoformat.json
```

**Erwartet — und das ist die eigentliche Frage des Teils:**

* **A)** genau **EIN** verschiedener Wert, `'2026-09-16T00:00:00'` (bzw. das
  aktuelle Datum des letzten Handelstags), Typ `str`.
  ⭐ **Auf dem Mac läuft der Rückfall gegen den ECHTEN Endpunkt** (Binance und
  yfinance sind erreichbar) — die Cloud konnte nur eine Attrappe einsetzen.
  **Steht dort mehr als ein Wert oder eine andere Schreibweise, ist das der
  Befund und gehört wörtlich in die Rückmeldung.**
* **B)** Die Spalte für **3.9.6** muss dieselben sechs Formen als
  `SCHEITERT` zeigen wie 3.9.23 in der Cloud: Nanosekunden, `Z`-Suffix,
  `20260916T000000`, `20260916`, `2026-W38-3`, Dezimalkomma.
  **Weicht sie ab, ist das ein Messwert für `docs/UMGEBUNGEN.md`** — er
  gehört in die Rückmeldung, wird aber **nicht** selbst eingetragen.
* **C)** `lade() Aktien: ValueError`, `lade() Krypto: durchgelaufen`, und der
  Bot läuft durch mit je einer Fehlerzeile pro Symbol.
* **D)** `os.fstat` ist auf **jeder** vorhandenen Fassung ein
  `builtin_function_or_method`, und **kein** Klassenrumpf bindet es.

---

## 7. Der Basislauf — alle Selbsttests

```bash
cd ~/trading-bot
: > $E/07_basislauf.txt
for t in $(find . -name "test_*.py" -not -path "./.git/*" | sort); do
  s=$(date +%s)
  python3 "$t" > /tmp/tb45_last.txt 2>&1; rc=$?
  e=$(date +%s)
  echo "rc=$rc  $((e-s))s  $t  $(grep -E 'bestanden|GESCHEITERT' /tmp/tb45_last.txt | tail -1)" \
      | tee -a $E/07_basislauf.txt
  cp /tmp/tb45_last.txt "$E/07_einzeln_$(echo $t | tr '/.' '__').txt"
done
```

**Bekannt rot auf dem Mac** (aus `docs/UMGEBUNGEN.md` und der
Aufgabenstellung, ⚠️ **mit Angabe des Rechners**):

| Test | Mac | Cloud |
|---|---|---|
| `shared/test_drawdown_beide_masse.py` | rot (Zeitüberschreitung) | rot |
| `shared/test_stabile_sortierung.py` | rot | rot |
| `shared/test_wellenauswahl.py` | rot | rot |
| `dashboard/test_portfolio_sicht.py` | **rot** (leeres gemeinsames Fenster) | ⚠️ **grün (90/90)** |
| `research/exposure_messung/test_exposure_kern.py` | rot | rot |
| `system/test_log_rotation.py` | flattert | flattert |
| `shared/test_zuteilung.py` | ⚠️ **grün** | rot |
| `dashboard/test_dashboard.py` | ⚠️ **grün** | rot (ohne `node`: 780/780 statt 784) |

> ⚠️ **Jeder rote Test, der NICHT in dieser Tabelle steht, ist ein Befund**
> und gehört mit seinen roten Zeilen in die Rückmeldung.
> ⚠️ **Und jeder Test aus dieser Tabelle, der grün ist, ebenfalls** — die
> Liste ist dann falsch und gehört korrigiert.

---

## 8. Der Datenstand und die Datenbanken — DANACH

```bash
python3 research/registernachtrag_tb41/pruefe_register.py \
    --nur datenstand 2>&1 | tee $E/08_datenstand_nachher.txt
diff $E/01_datenstand_vorher.txt $E/08_datenstand_nachher.txt \
    && echo "DATENSTAND IDENTISCH" | tee -a $E/08_datenstand_nachher.txt

shasum -a 256 paper_trading_*.db 2>&1 | tee $E/08_db_nachher.txt
diff $E/00_db_vorher.txt $E/08_db_nachher.txt \
    && echo "ALLE NEUN DATENBANKEN BYTEWEISE IDENTISCH" | tee -a $E/08_db_nachher.txt

git status --short 2>&1 | tee $E/08_git_status.txt
```

**Erwartet:** `DATENSTAND IDENTISCH`, `ALLE NEUN DATENBANKEN BYTEWEISE
IDENTISCH`, und `08_git_status.txt` zeigt **keine** Änderung unter `data/`,
`strategies/`, `broker/` oder `config/`.

**Abbruchgrund:** irgendetwas davon nicht erfüllt.

---

## 9. Die Ergebnisse einpacken

⚠️ **Das ZIP gehört nach `~/Downloads`, NICHT ins Repo.**

```bash
cd ~/Downloads
zip -r TB-45_ergebnisse.zip TB-45_ergebnisse > /dev/null
ls -lh ~/Downloads/TB-45_ergebnisse.zip
```

---

## 10. Rückmeldung — was berichtet wird

Diese fünf Punkte, in dieser Reihenfolge:

1. **Teil 1 und 2:** Zahl aus `02_stille_ausfaelle.txt` (erwartet 27/27) und
   aus `02_kursdaten.txt` (erwartet 88/88). ⚠️ **Und wörtlich: aus welchem
   Grund `dashboard/test_portfolio_sicht.py` auf dem Mac rot ist** — derselbe
   wie vorher oder ein anderer?
2. **Teil 3:** die vier Zeilen aus `03_ist_geraet_alt.txt` und der Zustand von
   `B2` und `N5 vorhanden` aus `04_trockenlauf.txt`. **Existierten
   `results/<bot>` und `logs/<bot>` auf diesem Rechner?** (`00_ordner.txt`)
3. **Teil 4:** 45/45 aus `05_leeres_symbol.txt`, und die Zahl aus
   `05_leeres_symbol_ALT.txt` (erwartet 23/35).
4. **Teil 5:** der **eine** Wert aus Messung A — am echten Endpunkt. Und ob
   die 3.9.6-Spalte in B dieselben sechs Formen ablehnt wie 3.9.23.
5. **Basislauf:** jede Abweichung von der Tabelle in Schritt 7, in beide
   Richtungen.

---

## In einfacher Sprache

**Was wir wissen wollten.**
Fünf Stellen im Projekt haben aufgehört zu arbeiten, ohne es zu sagen. Sie
wurden in der Cloud repariert. Zwei davon lassen sich in der Cloud aber gar
nicht richtig prüfen: Die eine hängt daran, dass auf deinem Rechner bestimmte
Ordner schon existieren (die Cloud legt sie nie an), die andere daran, dass
dein Rechner eine ältere Python-Ausgabe benutzt und echten Zugang zu den
Kursanbietern hat. Dieser Auftrag holt beides nach.

**Was herauskommt.**
Eine Reihe von Protokolldateien in `~/Downloads/TB-45_ergebnisse`, am Ende zu
einer ZIP-Datei gepackt. Jeder Schritt sagt vorher, welche Zahl zu erwarten
ist. Am wichtigsten sind zwei: `356/356` beim Trockenlauf und `45/45` beim
Test zum leeren Symbol.

**Warum das so ist.**
Ein Test, der nur dort grün ist, wo der Fehler ohnehin nicht auftreten kann,
beweist nichts. Deshalb wird hier jeder Befund **zweimal** vorgeführt: einmal
am alten Stand, wo er noch da ist, und einmal am neuen, wo er weg ist. Das
ist mehr Arbeit, aber es ist der Unterschied zwischen „grün" und „bewiesen".

**Was das für dich heißt.**
Du startest einen einzigen Befehl (ganz oben) und lässt ihn durchlaufen. Er
ändert nichts an deinen Bots, nichts an den Kursdaten und nichts an den neun
Datenbanken — das wird am Ende sogar nachgerechnet und ausdrücklich bestätigt.
Danach liegt eine ZIP-Datei in deinem Download-Ordner, die du zurückschicken
kannst. **Eine Sache musst du selbst entscheiden**, und sie steht in
`research/fromisoformat_registerfrage/BERICHT.md`: ob an einer Stelle im
Kern der Bots etwas geändert werden soll oder nicht. Dieser Auftrag misst
dafür nur die Grundlage.
