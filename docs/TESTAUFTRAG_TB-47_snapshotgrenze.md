# Testauftrag TB-47 — Die Snapshot-Grenze (Mac)

**Autonom ausführbar.** Nichts an diesem Auftrag verlangt eine Entscheidung
während des Laufs. Er ist von oben nach unten abzuarbeiten; jeder Schritt sagt,
was zu erwarten ist und was ein Abbruchgrund wäre.

**Start (ein Befehl, kopierfertig):**

```
cd ~/trading-bot && claude --remote-control "Lies die Datei docs/TESTAUFTRAG_TB-47_snapshotgrenze.md und arbeite sie als autonome Claude-Code-Sitzung vollständig eigenständig ab, wie darin beschrieben."
```

---

> ⚠️ **DIESER AUFTRAG ZIEHT KEINEN ECHTEN SNAPSHOT.**
> Er prüft das **Werkzeug** auf Python 3.9.6 und weist die byteweise
> Identität der neun Datenbanken nach. Nach Registertext 5c ist ein zweiter
> Snapshot ein **neuer Lauf** — und der echte Snapshot wird am Tag des
> signierten Tags gezogen, nicht heute.
>
> ⚠️ **Kein `--echt`, keine Order, keine Kursdatei, kein `live_params.py`,
> keine Crontab, kein Registertext.** Will ein Schritt nach `data/` schreiben,
> ist das ein **Abbruchgrund**, kein Zwischenfall.

---

## Warum der Mac hier der eigentliche Nachweis ist

| Punkt | Was die Cloud strukturell nicht konnte |
|---|---|
| **Python 3.9.6** | In der Cloud lief alles auf **3.11.15**. `shared/snapshot.py` benutzt neu `signal`, `os.killpg` und `start_new_session` — Letzteres in `basislauf.py`. Auf 3.9 ist bislang **nur die Syntax** geprüft, nicht der Lauf. TB-43/TB-44 haben gezeigt, dass genau dieser Unterschied ein Werkzeug auf dem Mac gar nicht starten lässt. |
| **`pandas` 2.3.3 gegen 3.0.6** | ⚠️ In der Cloud fehlten **alle** Fremdpakete und mussten nachinstalliert werden — `pandas` kam als **3.0.6**, also eine Hauptversion über der 2.3.3 des Macs. Die TB-47-Module kommen zwar **ohne `pandas` aus** (nur Standardbibliothek); der Basislauf ringsum tut es nicht. |
| **Die Prozessgruppen-Reparatur** | Der Befund — ein Enkelprozess, der 22 Minuten mit 99 % CPU weiterrechnet — ist **auf dem Mac** aufgetreten, in beiden Läufen. Der Nachweis muss dort geführt werden, wo der Befund war. Schritt 5 lässt ihn wirklich in die Zeitgrenze laufen. |
| **Die neun Live-Datenbanken** | Sie gibt es **nur auf dem Mac** und sie sind nicht neu berechenbar. |
| **Der laufende Cron** | Er schreibt **während des Laufs** in genau diese Dateien. Schritt 7 behandelt das ausdrücklich. |

---

## Schritt 0 — Zweig auschecken, Fassungen festhalten, die neun Datenbanken sichern

```bash
cd ~/trading-bot
git fetch origin
git checkout claude/new-session-ebo6mm
git pull origin claude/new-session-ebo6mm
git log --oneline -5

mkdir -p ~/Downloads/TB-47_ergebnisse
E=~/Downloads/TB-47_ergebnisse

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
  trading-env/bin/python3 -c "import scipy" 2>&1 | tail -1
  echo "== Werkzeuge =="
  which node gh timeout; node --version 2>/dev/null
  df -h .
} 2>&1 | tee $E/00_umgebung.txt

# --- ⚠️ Sicherung der neun Datenbanken, VOR allem anderen -----------------
SICHERUNG=~/Downloads/TB-47_db_sicherung_$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "$SICHERUNG"
cp -p paper_trading_*.db "$SICHERUNG"/
shasum -a 256 paper_trading_*.db | tee "$SICHERUNG/vorher.sha256"
ls -l "$SICHERUNG" | tee -a $E/00_umgebung.txt
echo "SICHERUNG=$SICHERUNG" | tee $E/00_sicherung_pfad.txt
```

⚠️ **Abbruchgrund:** weniger als neun `paper_trading_*.db` gesichert, oder
`vorher.sha256` ist leer. Dann **hier aufhören** und melden.

⚠️ **`SICHERUNG` wird in Schritt 7 wieder gebraucht.** Geht die Shell
verloren, steht der Pfad in `$E/00_sicherung_pfad.txt`.

---

## Schritt 1 — Der Datenstand VORHER

```bash
E=~/Downloads/TB-47_ergebnisse
trading-env/bin/python3 shared/snapshot.py --quelle data --nur-hash \
  2>&1 | tee $E/01_datenstand_vorher.txt
```

**Erwartet — wörtlich diese Zeile:**

```
d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84  (223 Kursdateien)  data
```

⚠️ **Weicht der Hash oder die Zahl 223 ab:** das ist **kein Abbruchgrund**,
sondern der wichtigste Einzelbefund dieses Laufs. Der Cron hat dann seit dem
15.09. Kursdaten fortgeschrieben. **Notieren, weitermachen** — und in Schritt 8
ausdrücklich berichten. Die Schritte 3 und 6 erwarten dann ebenfalls den
neuen Wert.

---

## Schritt 2 — Die Wache über das Werkzeug, auf 3.9.6

```bash
E=~/Downloads/TB-47_ergebnisse
trading-env/bin/python3 shared/test_snapshot.py 2>&1 | tee $E/02_test_snapshot.txt
echo "Rueckgabewert: $?" | tee -a $E/02_test_snapshot.txt
```

**Erwartet:** `110 von 110 Pruefungen bestanden, 0 fehlgeschlagen.`,
Rückgabewert 0.

⚠️ **Besonders hinsehen bei:**

* **`(Anker)`-Fehler** — eine Mutationsprobe hat ihren Ankertext nicht
  gefunden. Das ist **rot**, nicht übersprungen, und heisst: eine Wache ist
  umgezogen und wird nicht mehr bewacht.
* **Probe 3t** — sie prüft, dass eine nicht ausführbare Teilkerzen-Prüfung
  den Rückgabewert **2** ergibt und nie 0.
* **Probe 3u** — sie verlangt den verankerten Datenstand. Ist Schritt 1
  abgewichen, kann **nur diese eine Probe** rot werden; das wäre dann eine
  Folge des neuen Datenstands, kein Fehler des Werkzeugs.

---

## Schritt 3 — ⭐ Ergibt `datenstand_hash` weiterhin `d9449faf…`? (gezeigt, nicht behauptet)

```bash
E=~/Downloads/TB-47_ergebnisse
trading-env/bin/python3 - <<'PY' 2>&1 | tee $E/03_zwei_hashes.txt
import importlib.util, os, sys
sys.path.insert(0, "shared")
import snapshot

# 1. Der registrierte Weg - die Quelle der Wahrheit
spez = importlib.util.spec_from_file_location(
    "h", "research/vorregistrierung/herkunft.py")
h = importlib.util.module_from_spec(spez); spez.loader.exec_module(h)
stand = h.datenstand("data")
print("herkunft.datenstand   :", stand["datenstand"], stand["dateien"])

# 2. Der Weg ueber snapshot.py - er muss DENSELBEN Wert liefern
hash_, anzahl = snapshot.gesamthash("data")
print("snapshot.gesamthash   :", hash_, anzahl)
print("beide gleich          :", hash_ == stand["datenstand"])
print("verankerter Wert      :", snapshot.VERANKERTER_DATENSTAND,
      snapshot.VERANKERTE_KURSDATEIEN)
print("trifft den Anker      :", hash_ == snapshot.VERANKERTER_DATENSTAND
      and anzahl == snapshot.VERANKERTE_KURSDATEIEN)

# 3. Und der ZWEITE Hash, ueber dieselben Dateien - er ist ein ANDERER Wert
paare = {n: snapshot.quersumme(os.path.join("data", n))
         for n in sorted(os.listdir("data")) if n.endswith(".csv")}
print("snapshot_hash (223)   :", snapshot.snapshot_hash(paare))
print("die beiden Hashes sind verschieden:",
      snapshot.snapshot_hash(paare) != hash_)
PY
```

**Erwartet:** `beide gleich: True`, `trifft den Anker: True`,
`die beiden Hashes sind verschieden: True`.

⚠️ **`beide gleich: False` ist ein echter Abbruchgrund** — dann rechnet
`snapshot.py` etwas anderes als das registrierte Verfahren.

---

## Schritt 4 — ⭐ Ist der Bestand frei von Teilkerzen? (an der Quelle)

```bash
E=~/Downloads/TB-47_ergebnisse
trading-env/bin/python3 shared/zeitabdeckung.py --ordner data \
  --json $E/04_teilkerzen.json 2>&1 | tee $E/04_teilkerzen.txt
echo "Rueckgabewert: $?" | tee -a $E/04_teilkerzen.txt

trading-env/bin/python3 - <<'PY' 2>&1 | tee -a $E/04_teilkerzen.txt
import json, collections, os
d = json.load(open(os.path.expanduser(
    "~/Downloads/TB-47_ergebnisse/04_teilkerzen.json")))
mit = [e for e in d["befunde"] if e.get("befunde")]
arten = collections.Counter(x.get("art") for e in mit for x in e["befunde"])
print("Dateien mit Befund :", len(mit), "von", len(d["befunde"]))
print("Arten              :", dict(arten))
print("LETZTE Kerze betroffen:",
      any("letzte" in str(x.get("art")) for e in mit for x in e["befunde"]))
PY
```

**In der Cloud gemessen (18.09.2026):** **36 von 223**, alle `rand_erste`,
**keine** letzte Kerze betroffen.

⚠️ **Das ist die wichtigste Zahl dieses Laufs.** Weicht sie ab, ändert das
die Lage:

* **mehr als 36** oder eine **andere Art** → notieren und berichten;
* ⚠️ **eine betroffene LETZTE Kerze** → das ist der gefährliche Fall (ein
  Abruf hat mitten in eine Kerze geschrieben). **Ausdrücklich und
  hervorgehoben melden.**

---

## Schritt 5 — ⭐ Beendet der Runner jetzt die ganze Prozessgruppe?

**Der Befund stammt von diesem Rechner. Hier wird er nachgeprüft.**

### 5a — Der Nachweis mit Gegenprobe

```bash
E=~/Downloads/TB-47_ergebnisse
trading-env/bin/python3 research/datenordner_schnitt/test_prozessgruppe.py \
  2>&1 | tee $E/05a_prozessgruppe.txt
echo "Rueckgabewert: $?" | tee -a $E/05a_prozessgruppe.txt
```

**Erwartet:** `11 von 11 Pruefungen bestanden`. Zwei Zeilen zählen:

```
1.5 ⭐ DER ENKELPROZESS LEBT EBENFALLS NICHT MEHR
2.3 ⭐ der Enkelprozess ueberlebt das alte Verfahren - genau das war der Befund
```

⚠️ **Wäre 2.3 rot**, misst der Test nicht die Reparatur, und sein Grün wäre
wertlos. Das ist dann ein Befund über den **Test**, nicht über die Reparatur.

### 5b — Der echte Fall: `test_drawdown_beide_masse.py` in die Zeitgrenze

⚠️ **Das ist der Schritt, der den ursprünglichen Befund nachstellt.** Er
dauert rund **eine Minute** (kurze Zeitgrenze, nicht 900 s).

```bash
E=~/Downloads/TB-47_ergebnisse
ps -eo pid,ppid,%cpu,etime,command | grep -c "[d]rawdown" \
  | tee $E/05b_prozesse_vorher.txt

trading-env/bin/python3 - <<'PY' 2>&1 | tee $E/05b_zeitgrenze.txt
import importlib.util, os, time
spez = importlib.util.spec_from_file_location(
    "b", "research/datenordner_schnitt/basislauf.py")
b = importlib.util.module_from_spec(spez); spez.loader.exec_module(b)
beginn = time.time()
e = b.fuehre_aus("shared/test_drawdown_beide_masse.py", os.getcwd(), grenze=45)
print("Art      :", e.get("art"))
print("Dauer    : %.1f s" % (time.time() - beginn))
PY

sleep 10
echo "--- Laeuft danach noch etwas? (erwartet: NICHTS) ---" | tee -a $E/05b_zeitgrenze.txt
ps -eo pid,ppid,%cpu,etime,command | grep "[d]rawdown\|[b]ot elliott_wave" \
  | tee -a $E/05b_zeitgrenze.txt
echo "Gefundene Ueberlebende: $(ps -eo command | grep -c '[d]rawdown\|[b]ot elliott_wave')" \
  | tee -a $E/05b_zeitgrenze.txt
```

**Erwartet:** `Art: zeitgrenze`, und danach **`Gefundene Ueberlebende: 0`**.

⚠️ **Ist die Zahl grösser als 0**, ist die Reparatur auf diesem Rechner
**nicht** wirksam. Dann: die Zeile mit `ps` aufnehmen, die Prozesse von Hand
beenden (`kill -9 <PID>`) und den Befund melden. **Das ist der Kern von
Teil 4** — bitte nicht übergehen.

---

## Schritt 6 — Das Werkzeug am echten Bestand, aber im Trockenlauf

⚠️ **Ohne `--ziehen`. Es wird nichts kopiert.**

```bash
E=~/Downloads/TB-47_ergebnisse
trading-env/bin/python3 shared/snapshot.py \
  --quelle data --ziel ~/Downloads/TB-47_niemals \
  2>&1 | tee $E/06_trockenlauf.txt
echo "Rueckgabewert: $?" | tee -a $E/06_trockenlauf.txt

echo "--- Ist trotzdem etwas entstanden? (erwartet: nein) ---" \
  | tee -a $E/06_trockenlauf.txt
ls -la ~/Downloads/TB-47_niemals 2>&1 | tee -a $E/06_trockenlauf.txt
```

**Erwartet (Stand 18.09.2026):** **Rückgabewert 2** mit

```
ABBRUCH: Die Teilkerzen-Pruefung hat 36 Datei(en) mit Befund gefunden: …
Es wird NICHT gezogen.
```

und `~/Downloads/TB-47_niemals` existiert **nicht**.

⚠️ **Das ist das erwartete Verhalten, kein Fehler.** Registertext 5a verlangt
genau das. Läuft der Trockenlauf stattdessen **durch** (Rückgabewert 0), dann
ist `data/` inzwischen frei von Teilkerzen — ebenfalls ein berichtenswerter
Befund. In beiden Fällen weitermachen.

---

## Schritt 7 — Die neun Datenbanken sind byteweise identisch

⭐ **Und der Cron schreibt während des Laufs in genau diese Dateien.** Eine
Abweichung wird deshalb **gegen den Crontab-Eintrag desselben Bots geprüft,
bevor sie gemeldet wird.** *Im TB-46b-Maclauf hat das ein Mensch von Hand
getan; hier steht es als Schritt.*

```bash
E=~/Downloads/TB-47_ergebnisse
SICHERUNG=$(cut -d= -f2 $E/00_sicherung_pfad.txt)

shasum -a 256 paper_trading_*.db > $E/07_nachher.sha256
diff "$SICHERUNG/vorher.sha256" $E/07_nachher.sha256 \
  > $E/07_diff.txt 2>&1 \
  && echo "OK: alle neun Datenbanken byteweise identisch" | tee $E/07_ergebnis.txt \
  || echo "ABWEICHUNG - weiter mit 7b" | tee $E/07_ergebnis.txt

crontab -l > $E/07_crontab.txt 2>&1
cat $E/07_diff.txt
```

### 7b — Nur falls es eine Abweichung gab

⚠️ **Eine Abweichung ist erst dann ein Befund dieses Zweiges, wenn sie NICHT
durch den Cron erklärt ist.** Für jede abweichende Datei:

```bash
E=~/Downloads/TB-47_ergebnisse
trading-env/bin/python3 - <<'PY' 2>&1 | tee $E/07b_cron_abgleich.txt
import os, re, subprocess, datetime as dt
E = os.path.expanduser("~/Downloads/TB-47_ergebnisse")
diff = open(os.path.join(E, "07_diff.txt")).read()
crontab = open(os.path.join(E, "07_crontab.txt")).read()

betroffen = sorted(set(re.findall(r"paper_trading_(\w+)\.db", diff)))
print("Abweichende Datenbanken:", betroffen or "keine")
for bot in betroffen:
    pfad = "paper_trading_%s.db" % bot
    mtime = dt.datetime.fromtimestamp(os.path.getmtime(pfad))
    zeilen = [z for z in crontab.splitlines()
              if bot in z and not z.strip().startswith("#")]
    print("\n%s" % pfad)
    print("  zuletzt geschrieben : %s" % mtime.isoformat(timespec="seconds"))
    print("  Crontab-Eintrag     : %s" % (zeilen or "⚠️ KEINER GEFUNDEN"))
    print("  Urteil              : %s" % (
        "durch den Cron erklaert - KEIN Befund dieses Zweiges" if zeilen
        else "⚠️ NICHT durch den Cron erklaert - BEFUND, bitte melden"))
PY
```

**Regel:** Gibt es für den Bot einen Crontab-Eintrag und passt die
Änderungszeit dazu, ist die Abweichung **erklärt und kein Befund dieses
Zweiges**. Fehlt der Eintrag, ist sie ein **Befund** und wird gemeldet.

⚠️ **Die gesicherten Kopien werden NICHT zurückgespielt.** Sie sind die
Rückfallebene, nicht das Ziel.

---

## Schritt 8 — Basislauf und Datenstand NACHHER

```bash
E=~/Downloads/TB-47_ergebnisse
trading-env/bin/python3 research/datenordner_schnitt/basislauf.py \
  --grenze 900 --json $E/08_basislauf.json 2>&1 | tee $E/08_basislauf.txt
echo "Rueckgabewert: $?" | tee -a $E/08_basislauf.txt

# ⚠️ Und danach: laeuft noch irgendein Testprozess weiter?
sleep 15
echo "--- Ueberlebende Prozesse (erwartet: KEINE) ---" | tee -a $E/08_basislauf.txt
ps -eo pid,%cpu,etime,command | grep "[t]est_\|[b]ot elliott_wave" \
  | tee -a $E/08_basislauf.txt

trading-env/bin/python3 shared/snapshot.py --quelle data --nur-hash \
  2>&1 | tee $E/08_datenstand_nachher.txt
git status --porcelain | tee $E/08_git_status.txt
```

**Bekannt rot auf dem Mac** (nicht von diesem Zweig):
`shared/test_stabile_sortierung.py` (3) · `shared/test_wellenauswahl.py` (1) ·
`dashboard/test_portfolio_sicht.py` (1) ·
`research/exposure_messung/test_exposure_kern.py` (1) ·
`research/hrp_portfolio/test_hrp_core.py` (`scipy` fehlt).

**Ungeprüft, nicht rot** (verlangen ein Bot-Argument):
`research/drawdown_reihenfolge/test_drawdown.py` ·
`research/fib_score_stufen/test_stufen.py` ·
`research/elliott_wave_params/test_params.py`.

**Zeitgrenze erwartet:** `shared/test_drawdown_beide_masse.py`.

⭐ **Die Zeile „Überlebende Prozesse" muss leer sein.** Genau das ist der
Unterschied, den Teil 4 gebracht hat — und `git status --porcelain` darf
`data/` nicht nennen.

---

## Schritt 9 — Bericht und ZIP

```bash
E=~/Downloads/TB-47_ergebnisse
cd ~/Downloads && zip -r TB-47_macergebnisse_$(date -u +%Y%m%dT%H%M%SZ).zip \
  TB-47_ergebnisse && cd ~/trading-bot
```

**Der Bericht (`docs/MACLAUF_TB-47_snapshotgrenze.md`, committen und pushen)
beantwortet ausdrücklich:**

1. **Python- und Paketfassungen** — jede Abweichung von der Tabelle oben.
2. **Datenstand vorher und nachher** — beide Zeilen wörtlich.
3. ⭐ **Ergibt `datenstand_hash` weiterhin `d9449faf…`?** Mit der Ausgabe aus
   Schritt 3, nicht als Behauptung.
4. ⭐ **Wie viele Dateien haben einen Teilkerzenbefund, welcher Art — und ist
   eine LETZTE Kerze dabei?**
5. ⭐ **`test_snapshot.py`: 110/110?** Falls nicht: welche Probe, und ist es
   ein `(Anker)`-Fehler?
6. ⭐ **Beendet der Runner die ganze Prozessgruppe?** Die Zahl aus Schritt 5b
   (`Gefundene Ueberlebende`) und die Prozessliste aus Schritt 8.
7. **Schritt 7 wörtlich** — die Zeile `OK: alle neun Datenbanken byteweise
   identisch`, oder für jede Abweichung das Urteil aus 7b.
8. **Basislauf** — rot / bekannt rot / ungeprüft / Zeitgrenze, getrennt
   gezählt.
9. **Jede Abweichung von diesem Auftrag**, auch eine kleine.

⚠️ **Wenn nach dem Bericht noch etwas committet wird, ist
`git status --porcelain` erneut aufzunehmen.**
