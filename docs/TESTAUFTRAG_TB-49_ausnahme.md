# Testauftrag TB-49 — Die Ausnahme `rand_erste` (Mac)

**Autonom ausführbar.** Nichts an diesem Auftrag verlangt eine Entscheidung
während des Laufs. Er ist von oben nach unten abzuarbeiten; jeder Schritt sagt,
was zu erwarten ist und was ein Abbruchgrund wäre.

**Start (ein Befehl, kopierfertig):**

```
cd ~/trading-bot && claude --remote-control "Lies die Datei docs/TESTAUFTRAG_TB-49_ausnahme.md und arbeite sie als autonome Claude-Code-Sitzung vollständig eigenständig ab, wie darin beschrieben."
```

---

> ⚠️ **TB-49 ÄNDERT EIN WERKZEUG, DAS DEN BESTAND LIEST.** Geändert sind
> `shared/snapshot.py` und `shared/test_snapshot.py`; neu ist
> `research/registernachtrag_tb48/`. **Kein Bot-Code, kein
> `live_params.py`, keine Kursdatei, kein Registertext.**
>
> ⚠️ **KEIN SNAPSHOT WIRD GEZOGEN — auch hier nicht.** Dieser Auftrag ruft
> `snapshot.py` ausschliesslich als **Trockenlauf** auf. Entsteht irgendwo ein
> Ordner `snapshots/` oder `data/snapshots/`, ist das ein **Abbruchgrund**.
> *Die Selbsttests ziehen in `tempfile.mkdtemp()` und räumen selbst auf — das
> ist etwas anderes und ausdrücklich in Ordnung.*
>
> ⚠️ **Kein `--echt`, keine Order, keine Gegenstelle, keine Crontab-Änderung.**
> Will ein Schritt nach `data/` schreiben, ist das ein **Abbruchgrund**, kein
> Zwischenfall.

---

## Warum der Mac hier gebraucht wird — und diesmal trägt der Lauf wirklich etwas

*TB-48 war eine Schreibaufgabe; der Mac-Teil war entsprechend klein. Dieser
hier ist es nicht.*

| Punkt | Was die Cloud strukturell nicht konnte |
|---|---|
| ⭐ **Python 3.9.6** | Die Ausnahme ist **neuer Code im Entscheidungspfad** des Snapshot-Werkzeugs. Die Cloud lief auf **3.11.15**. TB-40/TB-41 und TB-43/TB-44 haben je ein Werkzeug gezeigt, das auf dem Mac gar nicht erst startete. **Hier wird das Verhalten der Ausnahme auf 3.9.6 gemessen, nicht nur ihr Import.** |
| ⭐ **Die neunzehn Zahlen von Abschnitt 17** | Der Prüfer liegt seit diesem Zweig **im Repo** (`research/registernachtrag_tb48/pruefe_abschnitt17.py`). Er lässt sich damit zum ersten Mal auf dem Betriebsrechner laufen — **inklusive der einen erwarteten Abweichung**. |
| ⭐ **`pandas_market_calendars` 4.6.1** | **Registertext 5f (17.5) nennt diese Fassung als Tatsachennotiz** und sagt ausdrücklich „auf dem Betriebsrechner". In der Cloud steht 5.4.0. *In TB-48 stand dieser Punkt schon im Auftrag; er bleibt offen, bis er hier gemessen ist.* |
| **Die neun Live-Datenbanken** | Sie gibt es **nur auf dem Mac** und sie sind nicht neu berechenbar. |
| **Der laufende Cron** | Er schreibt **während des Laufs** in genau diese Dateien. Schritt 6 behandelt das ausdrücklich — ⭐ **gegen den Crontab-Eintrag desselben Bots, maschinell, nicht von Hand.** |

---

## Schritt 0 — Zweig auschecken, Fassungen festhalten, die neun Datenbanken sichern

```bash
cd ~/trading-bot
git fetch origin
git checkout claude/new-session-kfbw56
git pull origin claude/new-session-kfbw56
git log --oneline -5

mkdir -p ~/Downloads/TB-49_ergebnisse
E=~/Downloads/TB-49_ergebnisse

# --- Fassungen -------------------------------------------------------------
{
  echo "== System =="; sw_vers; uname -a
  echo "== Interpreter =="
  /usr/bin/python3 -VV
  trading-env/bin/python3 -VV
  echo "== Pakete (Betriebsinterpreter) =="
  trading-env/bin/python3 -c "import pandas, numpy; print('pandas', pandas.__version__, 'numpy', numpy.__version__)"
  trading-env/bin/python3 -c "import dateparser; print('dateparser', dateparser.__version__)"
  trading-env/bin/python3 -c "import pandas_market_calendars as m; print('pandas_market_calendars', m.__version__)"
  trading-env/bin/python3 -c "import scipy; print('scipy', scipy.__version__)" 2>&1 | tail -1
  node --version 2>&1 | tail -1
} > $E/00_fassungen.txt 2>&1
cat $E/00_fassungen.txt

# --- ⚠️ Sicherung der neun Datenbanken, VOR allem anderen -----------------
SICHERUNG=~/Downloads/TB-49_db_sicherung_$(date +%Y%m%d_%H%M%S)
mkdir -p "$SICHERUNG"
cp paper_trading_*.db "$SICHERUNG"/
shasum -a 256 paper_trading_*.db | tee "$SICHERUNG/vorher.sha256"
echo "SICHERUNG=$SICHERUNG" > $E/00_sicherung_pfad.txt
wc -l "$SICHERUNG/vorher.sha256"

# --- Datenstand VORHER -----------------------------------------------------
trading-env/bin/python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; s=herkunft.datenstand('data')
print('VORHER', s['datenstand'], s['dateien'])
" | tee $E/00_datenstand_vorher.txt
```

⚠️ **Abbruchgrund:** `vorher.sha256` ist leer oder zählt **nicht neun** Zeilen.
Dann **hier aufhören** und melden.

**Erwartet:**
`VORHER d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84 223`

⭐ **`trading-env/bin/python3` ist in diesem Auftrag durchgehend der
Interpreter** — nicht `/usr/bin/python3`. *Der TB-45-Auftrag schrieb an
mehreren Stellen `python3` vor; dort fiel alles rot aus, was `binance`
braucht, ohne dass irgendetwas kaputt war.*

---

## Schritt 1 — ⭐⭐ Die Ausnahme im Verhalten auf 3.9.6

**Das ist der Kern dieses Auftrags.** Bis TB-48 brach der Trockenlauf mit
**2** ab, weil die Teilkerzen-Prüfung 36 Befunde meldet. Seit TB-49 läuft er
durch — **ohne dass die Prüfung abgeschwächt wäre.**

```bash
E=~/Downloads/TB-49_ergebnisse
trading-env/bin/python3 shared/snapshot.py --quelle data \
  > $E/01_trockenlauf.txt 2>&1
echo "Rueckgabewert: $?" | tee -a $E/01_trockenlauf.txt
cat $E/01_trockenlauf.txt
```

**Erwartet — jede Zeile gehört wörtlich in den Bericht:**

| Angabe | Sollwert |
|---|---|
| **Rückgabewert** | ⭐ **0** — bis TB-48 war es hier **2** |
| `datenstand_hash` | `d9449faf…`, **223** Kursdateien |
| `snapshot_hash` | `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` — ⚠️ **das ist der Hash über die 225 Dateien des Laufs** (223 Kursdateien + die zwei Symbollisten), **nicht** der `4fee547d…` aus Abschnitt 17, der nur über `data/` läuft. **Beide sind richtig, sie beantworten zwei Fragen** |
| ⚠️ **Teilkerzen** | **36 Datei(en) mit Befund (223 Datei(en) geprüft)** — die Prüfung schlägt weiter an |
| ⭐ **davon zugelassen** | **36 Befund(e) in 36 Datei(en)** mit dem Verweis `docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3` |
| letzte Zeile | `TROCKENLAUF - nichts kopiert.` |

⚠️ **Abbruchgründe für diesen Schritt:**

* Der Rückgabewert ist **2** → die Ausnahme greift auf 3.9.6 nicht. **Das ist
  der Befund, für den dieser Auftrag da ist.** Vollständige Ausgabe melden.
* Es steht **`NICHT zugelassen`** in der Ausgabe → dann trägt eine Kursdatei
  einen Befund, den Registertext 5a, Zusatz nicht deckt. **Die genannte Datei
  melden, nicht weitermachen.**
* Es entsteht ein Ordner `snapshots/`.

### 1b — Und die vier Fälle, die weiterhin abbrechen müssen

⭐ **An einem Wegwerf-Bestand, nicht an `data/`.** Der Bestand wird gebaut,
geprüft und weggeworfen; `data/` wird dabei **nicht einmal gelesen**.

```bash
E=~/Downloads/TB-49_ergebnisse
trading-env/bin/python3 - <<'PY' > $E/01b_vier_faelle.txt 2>&1
import os, shutil, sys, tempfile
sys.path.insert(0, os.path.abspath("shared"))
import test_snapshot as T                       # bringt den Bestandsbauer mit

arbeit = tempfile.mkdtemp(prefix="tb49_mac_")
try:
    faelle = [
        ("36 zugelassene Befunde", dict(symbole=["S%02d" % i for i in range(36)]),
         0),
        ("rand_letzte kommt dazu",
         dict(symbole=["ANG"], letzte_stunden=range(0, 12)), 2),
        ("rand_erste NICHT abgeleitet",
         dict(symbole=["VER"], erste_verfaelschen=True), 2),
    ]
    for name, kw, erwartet in faelle:
        quelle = T._teilkerzen_quelle(
            os.path.join(arbeit, name.replace(" ", "_"), "quelle"), **kw)
        ziel = os.path.join(arbeit, name.replace(" ", "_"), "ziel")
        rc, ausgabe = T._lauf("--quelle", quelle, "--ziel", ziel,
                              "--kein-anker", "--ziehen")
        print("%-32s rc=%d (erwartet %d)  %s"
              % (name, rc, erwartet, "OK" if rc == erwartet else "ABWEICHUNG"))
        if rc != 0:
            print("    %s" % ausgabe.strip().splitlines()[0][:180])
        print("    Snapshot entstanden: %s" % os.path.exists(ziel))
finally:
    shutil.rmtree(arbeit, ignore_errors=True)
PY
cat $E/01b_vier_faelle.txt
```

**Erwartet:**

| Fall | Rückgabewert | Snapshot |
|---|---:|---|
| 36 zugelassene Befunde | **0** | entsteht |
| ⚠️ ein **`rand_letzte`** kommt dazu | **2**, Datei genannt | **entsteht nicht** |
| ⚠️ ein `rand_erste`, der **nicht** das Aggregat ist | **2**, Datei genannt | **entsteht nicht** |

⚠️ Der vierte und fünfte Fall (Befund an einer **späteren** Kerze, Befund
**ohne feineren Zeugen**) lassen sich aus Kursdateien nicht herstellen — die
Prüfung vergibt beides nicht. Sie stehen als gestellte Fälle in Schritt 2 und
laufen dort mit.

---

## Schritt 2 — ⭐ Die Wache: 164 Prüfungen auf 3.9.6

```bash
E=~/Downloads/TB-49_ergebnisse
trading-env/bin/python3 shared/test_snapshot.py > $E/02_test_snapshot.txt 2>&1
echo "Rueckgabewert: $?" | tee -a $E/02_test_snapshot.txt
tail -30 $E/02_test_snapshot.txt
```

**Erwartet:** `164 von 164 Pruefungen bestanden, 0 fehlgeschlagen.`,
Rückgabewert **0**.

⭐ **Darin enthalten und eigens zu berichten:** der Abschnitt
**`3c. TB-49 - DIE AUSNAHME rand_erste`** mit den acht Proben. Jede führt ihre
**Mutation** mit — die Fassung mit entfernter Bedingung muss die Abweichung
**übersehen**. Eine Probe, deren Mutation die Abweichung auch findet, prüft
eine andere Stelle als angenommen; sie fällt dann rot aus und ist zu melden.

⚠️ **`110 von 110`** wäre ein Befund: dann läuft eine alte Fassung der Datei.

---

## Schritt 3 — ⭐⭐ Die neunzehn Zahlen von Abschnitt 17, auf dem Betriebsrechner

**Der Prüfer liegt seit diesem Zweig im Repo.** Er rechnet jede Zahl an ihrer
Quelle nach — er schreibt keine ab.

```bash
E=~/Downloads/TB-49_ergebnisse
trading-env/bin/python3 research/registernachtrag_tb48/pruefe_abschnitt17.py \
  --json $E/03_abschnitt17.json > $E/03_abschnitt17.txt 2>&1
echo "Rueckgabewert: $?" | tee -a $E/03_abschnitt17.txt
cat $E/03_abschnitt17.txt
```

**Erwartet:**

* **19 von 19** geprüft, **keine** als `nicht pruefbar`.
* ⚠️ **Genau EINE Abweichung: `15 frueheste_selektionsfalte`** (Soll 2022 aus
  dem Wortlaut in 17.3, Ist **2019** aus dem Faltenplan).
* **Rückgabewert 1.**

⚠️ **Abbruchgründe:**

* **Null Abweichungen** → dann hat sich eine Quelle geändert, oder der Prüfer
  beisst nicht. **Beides ist ein Befund.**
* **Mehr als eine Abweichung** → jede zusätzliche wörtlich melden, mit Soll und
  Ist.
* Eine Prüfung meldet `nicht pruefbar` (Rückgabewert **2**) → sie konnte nicht
  messen. **Das ist nicht „in Ordnung"** und gehört mit Begründung in den
  Bericht.

> ⭐ **Warum die eine rote Zeile richtig ist.** Der beschlossene Wortlaut in
> 17.3 bleibt als der registrierte stehen; massgeblich ist die Befundnotiz
> darunter — dieselbe Behandlung wie bei der „vierten falschen Zahl" in 16.7.
> **Ein Prüfer, der die Abweichung wegdefiniert, wäre die stillschweigende
> Korrektur, die TB-48 ausdrücklich nicht vornehmen sollte.**

### 3b — Der Selbsttest des Prüfers

```bash
E=~/Downloads/TB-49_ergebnisse
trading-env/bin/python3 research/registernachtrag_tb48/test_abschnitt17.py \
  > $E/03b_test_abschnitt17.txt 2>&1
echo "Rueckgabewert: $?" | tee -a $E/03b_test_abschnitt17.txt
tail -20 $E/03b_test_abschnitt17.txt
```

**Erwartet:** `24 von 24 Pruefungen bestanden`, Rückgabewert **0**.
⚠️ Der Lauf dauert rund **zwei Minuten** — er rechnet am Ende den echten
Bestand durch. Das ist Absicht: ohne ihn wäre der Test die Behauptung statt
der Messung.

### 3c — Die früheste Falte je Bot (TB-49, Teil 4)

```bash
E=~/Downloads/TB-49_ergebnisse
trading-env/bin/python3 research/registernachtrag_tb48/pruefe_abschnitt17.py \
  --falten-je-bot > $E/03c_falten.txt 2>&1
cat $E/03c_falten.txt
```

**Erwartet:** neun Zeilen, **alle mit erstem Faltenjahr 2019** — Krypto wie
Aktien —, und darunter der Befund, dass eine Trennung „Krypto 2022 / alle neun
2019" dieser Faltenplan **nicht hergibt**.

---

## Schritt 4 — ⭐ `pandas_market_calendars` — die offene Zahl aus 17.5

```bash
E=~/Downloads/TB-49_ergebnisse
trading-env/bin/python3 -c "
import pandas_market_calendars as m; print('pandas_market_calendars', m.__version__)
" | tee $E/04_kalender.txt
```

**Erwartet:** **4.6.1** — so steht sie als Tatsachennotiz in Registertext 5f
(17.5).

⚠️ **Weicht sie ab, ist das ein MELDEPFLICHTIGER BEFUND**, kein Nebensatz: die
Fassung steht im Register und der Registertext verlangt für sie ein
`requirements.lock`, das es noch nicht gibt (17.10, Zeile 4).

---

## Schritt 5 — Basislauf

```bash
E=~/Downloads/TB-49_ergebnisse
trading-env/bin/python3 research/datenordner_schnitt/basislauf.py \
  --grenze 900 --json $E/05_basislauf.json > $E/05_basislauf.txt 2>&1
tail -40 $E/05_basislauf.txt
```

**Bekannt rot auf dem Mac — kein Befund dieses Zweiges:**
`shared/test_stabile_sortierung.py` (3) · `shared/test_wellenauswahl.py` (1) ·
`dashboard/test_portfolio_sicht.py` (1) ·
`research/exposure_messung/test_exposure_kern.py` (1) ·
`research/hrp_portfolio/test_hrp_core.py` (`scipy` fehlt).

⭐ **`system/test_log_rotation.py` ist auf beiden Rechnern grün** (TB-46b hat
den falschen Eintrag gestrichen).

⚠️ **NICHT rot, sondern UNGEPRÜFT** (verlangen ein Bot-Argument):
`research/drawdown_reihenfolge/test_drawdown.py` ·
`research/fib_score_stufen/test_stufen.py` ·
`research/elliott_wave_params/test_params.py`.

⚠️ **In die Zeitgrenze läuft bekannt:** `shared/test_drawdown_beide_masse.py`.
Nach dem Abbruch gehört die Zahl der überlebenden Prozesse in den Bericht
(seit TB-47 erwartet: **0**):

```bash
pgrep -fl "test_drawdown_beide_masse" | tee $E/05b_ueberlebende.txt
echo "(leer = 0 Ueberlebende)"
```

⭐ **`shared/test_zuteilung.py` ist auf dem Mac GRÜN** — der Rotbefund aus der
Cloud ist eine **Netzsperre**, kein Fehler.

**Die Erwartung, die diesem Zweig eigen ist:** TB-49 fasst **keinen Bot-Code**
an. Neu hinzu kommt genau **eine** Testdatei
(`research/registernachtrag_tb48/test_abschnitt17.py`, ~2 min), und
`shared/test_snapshot.py` wächst von 110 auf 164 Prüfungen. Der Basislauf zählt
deshalb **65** statt 64 Dateien. **Jede andere neue rote Datei ist ein Befund.**

> ⭐ **Weicht die Liste ab, MELDEN** — nicht stillschweigend für falsch halten.
> `docs/UMGEBUNGEN.md` altert, und drei Korrekturen dieser Liste stammen aus
> genau solchen Meldungen.

---

## Schritt 6 — Die neun Datenbanken sind byteweise identisch

⭐ **Der Cron schreibt während des Laufs in genau diese Dateien.** Eine
Abweichung wird deshalb **gegen den Crontab-Eintrag desselben Bots geprüft,
bevor sie gemeldet wird — maschinell, nicht von Hand.**

```bash
E=~/Downloads/TB-49_ergebnisse
SICHERUNG=$(cut -d= -f2 $E/00_sicherung_pfad.txt)

shasum -a 256 paper_trading_*.db > $E/06_nachher.sha256
diff "$SICHERUNG/vorher.sha256" $E/06_nachher.sha256 \
  > $E/06_diff.txt 2>&1 \
  && echo "OK: alle neun Datenbanken byteweise identisch" | tee $E/06_ergebnis.txt \
  || echo "ABWEICHUNG - weiter mit 6b" | tee $E/06_ergebnis.txt

crontab -l > $E/06_crontab.txt 2>&1
cat $E/06_diff.txt
```

### 6b — Nur falls es eine Abweichung gab

⚠️ **Eine Abweichung ist erst dann ein Befund dieses Zweiges, wenn sie NICHT
durch den Cron erklärt ist.** ⭐ **Der Abgleich geschieht gegen den
Crontab-Eintrag desselben Bots, maschinell:**

```bash
E=~/Downloads/TB-49_ergebnisse
trading-env/bin/python3 - <<'PY' 2>&1 | tee $E/06b_cron_abgleich.txt
import os, re, datetime as dt
E = os.path.expanduser("~/Downloads/TB-49_ergebnisse")
diff = open(os.path.join(E, "06_diff.txt")).read()
crontab = open(os.path.join(E, "06_crontab.txt")).read()

betroffen = sorted(set(re.findall(r"paper_trading_(\w+)\.db", diff)))
print("Abweichende Datenbanken:", betroffen or "keine")
for bot in betroffen:
    pfad = "paper_trading_%s.db" % bot
    mtime = dt.datetime.fromtimestamp(os.path.getmtime(pfad))
    zeilen = [z for z in crontab.splitlines()
              if bot in z and not z.strip().startswith("#")]
    print("\n%s" % pfad)
    print("  zuletzt geschrieben : %s" % mtime.isoformat(timespec="seconds"))
    print("  Crontab-Eintrag     : %s" % (zeilen or "KEINER GEFUNDEN"))
    print("  Urteil              : %s" % (
        "durch den Cron erklaert - KEIN Befund dieses Zweiges" if zeilen
        else "NICHT durch den Cron erklaert - BEFUND, bitte melden"))
PY
```

**Regel:** Gibt es für den Bot einen Crontab-Eintrag und passt die
Änderungszeit dazu, ist die Abweichung **erklärt und kein Befund dieses
Zweiges**. Fehlt der Eintrag, ist sie ein **Befund** und wird gemeldet.

⚠️ **Die gesicherten Kopien werden NICHT zurückgespielt.** Sie sind die
Rückfallebene, nicht das Ziel.

⚠️ **Die Crontab wird in diesem Auftrag nur GELESEN** (`crontab -l`), nie
geschrieben.

---

## Schritt 7 — Datenstand NACHHER, sauberer Arbeitsbaum, kein Snapshot

```bash
E=~/Downloads/TB-49_ergebnisse
trading-env/bin/python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; s=herkunft.datenstand('data')
print('NACHHER', s['datenstand'], s['dateien'])
" | tee $E/07_datenstand_nachher.txt

git status --porcelain | tee $E/07_git_status.txt
echo "(leer = sauber)"
ls -d data/snapshots snapshots 2>&1 | tee $E/07_kein_snapshot.txt
ls /tmp | grep -c "^tb49_" | tee $E/07_wegwerf_geraeumt.txt
```

**Erwartet:**

* `NACHHER d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84 223`
  — **identisch mit Schritt 0.**
* `git status --porcelain` ist **leer**.
* Der Snapshot-Befehl meldet **`No such file or directory`** für beide Pfade —
  ⚠️ **findet er einen Snapshot-Ordner, ist das ein Befund.**
* Die letzte Zahl ist **0** — die Wegwerf-Verzeichnisse der Selbsttests sind
  geräumt.

---

## Was zu berichten ist

1. **Schritt 1 wörtlich** — ⭐ **der Rückgabewert 0 und die Zeile
   `davon zugelassen 36 Befund(e) in 36 Datei(en)`** samt Registerverweis.
2. **Schritt 1b als Tabelle** — drei Fälle, je Rückgabewert und ob ein
   Snapshot entstanden ist.
3. **Schritt 2** — die Schlusszeile (`164 von 164`) und, falls rot, jede
   gefallene Probe mit Namen.
4. **Schritt 3 vollständig** — die 19 Zeilen, ⚠️ **die eine Abweichung
   ausdrücklich**, und der Rückgabewert.
5. **Schritt 3c** — die neun Zeilen der frühesten Falte je Bot.
6. **Schritt 4** — die Fassung von `pandas_market_calendars`, auch wenn sie
   4.6.1 ist.
7. **Schritt 5** — grün / rot / ungeprüft / Zeitgrenze als vier Zahlen, die
   roten je mit Datei und Ursache, und **überlebende Prozesse nach der
   Zeitgrenze**.
8. **Schritt 6 wörtlich** — die Zeile `OK: alle neun Datenbanken byteweise
   identisch`, oder bei Abweichung die Ausgabe von 6b **mit dem Urteil je
   Datei**.
9. **Schritt 7** — Datenstand vorher/nachher nebeneinander, `git status`
   wörtlich.
10. **Alle Abweichungen von `docs/UMGEBUNGEN.md`**, mit dem Vermerk, auf
    welchem Rechner gemessen.

**Der Bericht beantwortet ausdrücklich:**

* ⭐ **Zieht das Werkzeug auf 3.9.6 durch — Rückgabewert 0 statt 2?**
* ⚠️ **Bricht es weiterhin ab bei `rand_letzte` und bei einem
  nicht-abgeleiteten `rand_erste`?**
* **Führt das Manifest die zugelassenen Befunde samt Registerverweis?**
  (Schritt 2, Probe `3w`)
* ⭐ **Meldet der Prüfer für Abschnitt 17 auf dem Mac dieselben 19 Ergebnisse
  wie in der Cloud — 18 grün, eine Abweichung, Rückgabewert 1?**
* **Ist `pandas_market_calendars` auf dem Betriebsrechner wirklich 4.6.1?**
* **Sind die neun Datenbanken byteweise identisch — und wenn nicht, was sagt
  der Crontab-Abgleich?**
* **Ist `data/` unberührt, und ist kein Snapshot entstanden?**
