# Testauftrag TB-48 — Registernachtrag Abschnitt 17 (Mac)

**Autonom ausführbar.** Nichts an diesem Auftrag verlangt eine Entscheidung
während des Laufs. Er ist von oben nach unten abzuarbeiten; jeder Schritt sagt,
was zu erwarten ist und was ein Abbruchgrund wäre.

**Start (ein Befehl, kopierfertig):**

```
cd ~/trading-bot && claude --remote-control "Lies die Datei docs/TESTAUFTRAG_TB-48_registernachtrag.md und arbeite sie als autonome Claude-Code-Sitzung vollständig eigenständig ab, wie darin beschrieben."
```

---

> ⚠️ **TB-48 IST EINE SCHREIBAUFGABE AM REGISTER.** Geändert wurde **eine
> einzige Datei**: `docs/VORREGISTRIERUNG_neuselektion.md`, und darin
> **ausschliesslich durch Hinzufügen** (506 neue Zeilen, **0 entfernte**).
> **Kein Code, keine Kursdatei, kein Snapshot, kein Parameter.**
>
> ⚠️ **Der Mac-Teil ist deshalb klein.** Er weist drei Dinge nach: dass der
> **Registerprüfer auf 3.9.6 läuft und grün meldet**, dass der **Basislauf**
> durch diesen Zweig nicht schlechter wird, und dass die **neun Datenbanken
> byteweise identisch** bleiben.
>
> ⚠️ **Kein `--echt`, keine Order, kein Snapshot ziehen, kein `live_params.py`,
> keine Crontab-Änderung.** Will ein Schritt nach `data/` schreiben, ist das ein
> **Abbruchgrund**, kein Zwischenfall.

---

## Warum der Mac hier überhaupt gebraucht wird

*Die Aufgabe hat keinen Fachcode angefasst — der Nachweis ist trotzdem nicht
entbehrlich.*

| Punkt | Was die Cloud strukturell nicht konnte |
|---|---|
| **Python 3.9.6** | Die Cloud lief auf **3.11.15**. `research/registernachtrag_tb41/pruefe_register.py` liest das Register und rechnet Zahlen nach; ob er die **neu eingefügten 506 Zeilen** auf 3.9.6 ebenso verarbeitet, ist hier nicht geprüft. TB-40/TB-41 und TB-43/TB-44 haben je ein Werkzeug gezeigt, das auf dem Mac gar nicht erst startete. |
| ⚠️ **`pandas` 2.3.3 gegen 3.0.6** | In der Cloud fehlten **alle** Fremdpakete und mussten nachinstalliert werden; `pandas` kam als **3.0.6** — eine **Hauptversion** über der 2.3.3 des Macs. Auch `pandas_market_calendars` kam als **5.4.0** statt **4.6.1**. Der Registerprüfer selbst braucht `pandas` nur für seinen Trockenlauf-Beleg, der Basislauf ringsum aber sehr wohl. |
| ⭐ **`pandas_market_calendars` 4.6.1** | **Registertext 5f (17.5) nennt diese Fassung als Tatsachennotiz** — und sie ist eine **Mac-Messung** aus TB-47. In der Cloud steht 5.4.0. **Schritt 3 prüft die im Register stehende Zahl dort nach, wo sie gilt.** |
| **Die neun Live-Datenbanken** | Sie gibt es **nur auf dem Mac** und sie sind nicht neu berechenbar. |
| **Der laufende Cron** | Er schreibt **während des Laufs** in genau diese Dateien. Schritt 5 behandelt das ausdrücklich — **maschinell, nicht von Hand.** |

---

## Schritt 0 — Zweig auschecken, Fassungen festhalten, die neun Datenbanken sichern

```bash
cd ~/trading-bot
git fetch origin
git checkout claude/new-session-e63hx4
git pull origin claude/new-session-e63hx4
git log --oneline -5

mkdir -p ~/Downloads/TB-48_ergebnisse
E=~/Downloads/TB-48_ergebnisse

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
SICHERUNG=~/Downloads/TB-48_db_sicherung_$(date +%Y%m%d_%H%M%S)
mkdir -p "$SICHERUNG"
cp paper_trading_*.db "$SICHERUNG"/
shasum -a 256 paper_trading_*.db | tee "$SICHERUNG/vorher.sha256"
echo "SICHERUNG=$SICHERUNG" > $E/00_sicherung_pfad.txt
wc -l "$SICHERUNG/vorher.sha256"
```

⚠️ **Abbruchgrund:** `vorher.sha256` ist leer oder zählt **nicht neun** Zeilen.
Dann **hier aufhören** und melden.

⭐ **`trading-env/bin/python3` ist in diesem Auftrag durchgehend der
Interpreter** — nicht `/usr/bin/python3`. *Der TB-45-Auftrag schrieb an
mehreren Stellen `python3` vor; dort fiel alles rot aus, was `binance`
braucht, ohne dass irgendetwas kaputt war.*

---

## Schritt 1 — ⭐ Null entfernte Zeilen, auf dem Mac nachgemessen

**Das ist die harte Auflage dieses Zweiges.** Sie ist in der Cloud gemessen;
hier wird sie unabhängig wiederholt.

```bash
E=~/Downloads/TB-48_ergebnisse
BASIS=$(git merge-base origin/main HEAD)
echo "Basis: $BASIS" | tee $E/01_numstat.txt
git diff --numstat "$BASIS" -- docs/VORREGISTRIERUNG_neuselektion.md | tee -a $E/01_numstat.txt
echo "--- alle Dateien des Zweiges ---" | tee -a $E/01_numstat.txt
git diff --numstat "$BASIS" | tee -a $E/01_numstat.txt
```

**Erwartet:**

* Für `docs/VORREGISTRIERUNG_neuselektion.md` eine Zeile der Form
  **`506	0	docs/VORREGISTRIERUNG_neuselektion.md`** — die **zweite Spalte
  muss `0` sein.**
* In der Gesamtliste stehen **nur** `docs/`-Dateien. ⚠️ **Steht dort irgendetwas
  unter `shared/`, `strategies/`, `research/`, `broker/`, `config/` oder
  `data/`, ist das ein Abbruchgrund** — TB-48 ändert keinen Code.

---

## Schritt 2 — ⭐ Der Registerprüfer auf 3.9.6

```bash
E=~/Downloads/TB-48_ergebnisse
BASIS=$(git merge-base origin/main HEAD)
trading-env/bin/python3 research/registernachtrag_tb41/pruefe_register.py \
  --basis "$BASIS" 2>&1 | tee $E/02_pruefe_register.txt
echo "Rueckgabewert: $?" | tee -a $E/02_pruefe_register.txt
```

**Erwartet:** `KEIN BEFUND - jede eingetragene Zahl stimmt mit ihrer Quelle
ueberein.` und in der Zeile `Quelle numstat:` das Paar **`506\t0`**.

> ⚠️ **WICHTIG — was dieser Prüfer NICHT prüft.** Er ist das **TB-41**-Werkzeug
> und **kennt Abschnitt 17 nicht**; im ganzen Quelltext kommt die Zahl 17 in
> dieser Bedeutung nicht vor. Er prüft:
>
> | prüft er | prüft er **nicht** |
> |---|---|
> | Symbolzahl je Falte, Faltenevidenz, `MIN_HISTORY_*`, Umstellungstag, Universumsdateien (alles Abschnitt 15/16) | **keine einzige Zahl aus Abschnitt 17** |
> | Datenstand `d9449faf…` / 223 und dass `data/` unberührt ist | den **Snapshot-Hash** |
> | **0 entfernte Zeilen** über das ganze Register — ⭐ **das schliesst Abschnitt 17 mit ein** | ob die neuen Ersetzungsvermerke sachlich am richtigen Ort stehen |
> | dass die **fünf** in TB-41 ersetzten Fassungen ihren Vermerk tragen (Text `ERSETZT durch Abschnitt 16`) | die **drei neuen** Vermerke in 16.3 — sie sagen `ERSETZT durch Abschnitt 17` und stehen in **keiner** seiner Listen |
>
> *Ein Prüfer, der die neuen Texte nicht sieht, meldet grün über den alten
> Stand.* **Sein „KEIN BEFUND" ist deshalb ein Nachweis über Abschnitt 15 und
> 16 und über die Null — nicht über die Richtigkeit von Abschnitt 17.**
> Das ist **kein Fehler dieses Zweiges**, sondern eine benannte Grenze; ob der
> Prüfer erweitert wird, ist eine eigene Entscheidung (siehe Ergebnisbericht).

---

## Schritt 3 — ⭐ Die drei Zahlen, die nur der Mac belegen kann

**Zwei Tatsachennotizen in Abschnitt 17 sind Mac-Messungen aus TB-47.** Hier
werden sie an ihrem Rechner nachgemessen.

```bash
E=~/Downloads/TB-48_ergebnisse
{
  echo "== 17.5: pandas_market_calendars (Register nennt 4.6.1) =="
  trading-env/bin/python3 -c "import pandas_market_calendars as m; print(m.__version__)"

  echo "== 17.3 / 17.9: Teilkerzen und die beiden Hashes =="
  trading-env/bin/python3 - <<'PY'
import os, sys
sys.path.insert(0, ".")
from shared import snapshot
sys.path.insert(0, "research/vorregistrierung")
import herkunft

stand = herkunft.datenstand("data")
print("datenstand_hash :", stand["datenstand"], stand["dateien"])
print("trifft Anker    :", stand["datenstand"] ==
      "d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84")

paare = {n: snapshot.quersumme(os.path.join("data", n))
         for n in sorted(os.listdir("data"))
         if os.path.isfile(os.path.join("data", n))}
sh = snapshot.snapshot_hash(paare)
print("snapshot_hash   :", sh, len(paare))
print("trifft TB-47    :", sh ==
      "4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608")

t = snapshot.teilkerzen("data")
from collections import Counter
arten = Counter(a for b in t["befunde"] for a in b["arten"])
print("Teilkerzen      : %d von %d, Arten %s"
      % (len(t["befunde"]), t["dateien_geprueft"], dict(arten)))
print("LETZTE betroffen:", "rand_letzte" in arten)
PY
} > $E/03_zahlen.txt 2>&1
cat $E/03_zahlen.txt
```

**Erwartet, wörtlich in den Bericht:**

| Angabe | Sollwert (steht so in Abschnitt 17) |
|---|---|
| `pandas_market_calendars` | **4.6.1** (17.5). ⚠️ **Weicht sie ab, ist das ein MELDEPFLICHTIGER BEFUND** — die Fassung steht als Tatsachennotiz im Register |
| `datenstand_hash` | `d9449faf…`, **223** Dateien, `trifft Anker: True` |
| `snapshot_hash` | `4fee547d…`, **223** Dateien, `trifft TB-47: True` |
| Teilkerzen | **36 von 223**, `{'rand_erste': 36}` |
| letzte Kerze | `LETZTE betroffen: False` |

⚠️ **Dieser Schritt zieht KEINEN Snapshot.** Er rechnet nur Hashes. Entsteht
irgendwo ein Ordner `snapshots/`, ist das ein **Abbruchgrund**.

---

## Schritt 4 — Basislauf

```bash
E=~/Downloads/TB-48_ergebnisse
trading-env/bin/python3 research/datenordner_schnitt/basislauf.py \
  --grenze 900 --json $E/04_basislauf.json > $E/04_basislauf.txt 2>&1
tail -40 $E/04_basislauf.txt
```

**Bekannt rot auf dem Mac — kein Befund dieses Zweiges:**
`shared/test_stabile_sortierung.py` (3) · `shared/test_wellenauswahl.py` (1) ·
`dashboard/test_portfolio_sicht.py` (1) ·
`research/exposure_messung/test_exposure_kern.py` (1) ·
`research/hrp_portfolio/test_hrp_core.py` (`scipy` fehlt) ·
`system/test_log_rotation.py` (1, Restfenster beim Rotieren).

⚠️ **NICHT rot, sondern UNGEPRÜFT** (verlangen ein Bot-Argument):
`research/drawdown_reihenfolge/test_drawdown.py` ·
`research/fib_score_stufen/test_stufen.py` ·
`research/elliott_wave_params/test_params.py`.

⚠️ **In die Zeitgrenze läuft bekannt:** `shared/test_drawdown_beide_masse.py`.
Nach dem Abbruch gehört die Zahl der überlebenden Prozesse in den Bericht
(seit TB-47 erwartet: **0**).

⭐ **`shared/test_zuteilung.py` ist auf dem Mac GRÜN** — der Rotbefund aus der
Cloud ist eine **Netzsperre**, kein Fehler.

> ⭐ **Weicht die Liste ab, MELDEN** — nicht stillschweigend für falsch halten.
> `docs/UMGEBUNGEN.md` altert, und drei Korrekturen dieser Liste stammen aus
> genau solchen Meldungen.

**Eine Erwartung, die diesem Zweig eigen ist:** TB-48 hat **keinen Code
angefasst**. Der Basislauf muss deshalb **genau so ausfallen wie vor dem
Zweig**. Jede neue rote Datei ist ein Befund — und zwar einer, der nichts mit
dem Register zu tun haben kann.

---

## Schritt 5 — Die neun Datenbanken sind byteweise identisch

⭐ **Der Cron schreibt während des Laufs in genau diese Dateien.** Eine
Abweichung wird deshalb **gegen den Crontab-Eintrag desselben Bots geprüft,
bevor sie gemeldet wird — maschinell, nicht von Hand.**

```bash
E=~/Downloads/TB-48_ergebnisse
SICHERUNG=$(cut -d= -f2 $E/00_sicherung_pfad.txt)

shasum -a 256 paper_trading_*.db > $E/05_nachher.sha256
diff "$SICHERUNG/vorher.sha256" $E/05_nachher.sha256 \
  > $E/05_diff.txt 2>&1 \
  && echo "OK: alle neun Datenbanken byteweise identisch" | tee $E/05_ergebnis.txt \
  || echo "ABWEICHUNG - weiter mit 5b" | tee $E/05_ergebnis.txt

crontab -l > $E/05_crontab.txt 2>&1
cat $E/05_diff.txt
```

### 5b — Nur falls es eine Abweichung gab

⚠️ **Eine Abweichung ist erst dann ein Befund dieses Zweiges, wenn sie NICHT
durch den Cron erklärt ist.** ⭐ **Der Abgleich geschieht gegen den
Crontab-Eintrag desselben Bots, maschinell:**

```bash
E=~/Downloads/TB-48_ergebnisse
trading-env/bin/python3 - <<'PY' 2>&1 | tee $E/05b_cron_abgleich.txt
import os, re, datetime as dt
E = os.path.expanduser("~/Downloads/TB-48_ergebnisse")
diff = open(os.path.join(E, "05_diff.txt")).read()
crontab = open(os.path.join(E, "05_crontab.txt")).read()

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

## Schritt 6 — Datenstand NACHHER und sauberer Arbeitsbaum

```bash
E=~/Downloads/TB-48_ergebnisse
trading-env/bin/python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; s=herkunft.datenstand('data')
print('NACHHER', s['datenstand'], s['dateien'])
" | tee $E/06_datenstand_nachher.txt

git status --porcelain | tee $E/06_git_status.txt
echo "(leer = sauber)"
ls -d data/snapshots snapshots 2>&1 | tee $E/06_kein_snapshot.txt
```

**Erwartet:**

* `NACHHER d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84 223`
  — **identisch mit Schritt 3.**
* `git status --porcelain` ist **leer**.
* Der letzte Befehl meldet **`No such file or directory`** für beide Pfade —
  ⚠️ **findet er einen Snapshot-Ordner, ist das ein Befund.**

---

## Was zu berichten ist

1. **Schritt 1 wörtlich** — die `numstat`-Zeile mit der **Null** in der zweiten
   Spalte.
2. **Schritt 2 wörtlich** — die Zeile `KEIN BEFUND …` **oder** jeder Befund.
   ⭐ **Und ausdrücklich der Satz, dass dieser Prüfer Abschnitt 17 nicht
   kennt** — damit sein Grün nicht später als Nachweis für Abschnitt 17 gelesen
   wird.
3. **Schritt 3 als Tabelle** — die fünf Sollwerte, je mit Ist-Wert.
   ⚠️ **`pandas_market_calendars` ausdrücklich**, auch wenn es 4.6.1 ist.
4. **Schritt 4** — grün / rot / ungeprüft / Zeitgrenze als vier Zahlen, die
   roten je mit Datei und Ursache, und **überlebende Prozesse nach der
   Zeitgrenze**.
5. **Schritt 5 wörtlich** — die Zeile `OK: alle neun Datenbanken byteweise
   identisch`, oder bei Abweichung die Ausgabe von 5b **mit dem Urteil je
   Datei**.
6. **Schritt 6** — Datenstand vorher/nachher nebeneinander, `git status`
   wörtlich.
7. **Alle Abweichungen von `docs/UMGEBUNGEN.md`**, mit dem Vermerk, auf welchem
   Rechner gemessen.

**Der Bericht beantwortet ausdrücklich:**

* **Null entfernte Zeilen — auch auf dem Mac?**
* **Läuft der Registerprüfer auf 3.9.6, und was sagt er?**
* **Ist `pandas_market_calendars` auf dem Betriebsrechner wirklich 4.6.1?**
* **Sind die neun Datenbanken byteweise identisch — und wenn nicht, was sagt
  der Crontab-Abgleich?**
* **Ist `data/` unberührt?**
