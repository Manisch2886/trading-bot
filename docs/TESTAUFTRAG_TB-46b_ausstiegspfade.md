# Mac-Testauftrag TB-46b — Ausstiegspfade bei fehlenden Kursdaten

**Zweig:** `claude/new-session-ql406l` · **Stand:** 17.09.2026
**Ergebnis der Cloud-Sitzung:** [`ERGEBNIS_TB-46b_ausstiegspfade.md`](ERGEBNIS_TB-46b_ausstiegspfade.md)

> ⚠️ **Der Mac-Teil läuft ausschliesslich gegen KOPIEN der neun Datenbanken.**
> Schritt 0 legt sie an, Schritt 7 weist nach, dass die echten **byteweise
> identisch** geblieben sind. Die neun `*.db` sind die einzige OOS-Evidenz
> dieses Projekts und **nicht neu berechenbar**.

> ⚠️ **Interpreter: `trading-env/bin/python3`, nie `python3`.**
> `/usr/bin/python3` ist dieselbe Fassung (3.9.6), hat aber weder `binance`
> noch `dateparser` — dort fällt rot aus, was gar nicht kaputt ist
> (`docs/UMGEBUNGEN.md`).

---

## Schritt 0 — Zweig auschecken und die neun Datenbanken sichern

⚠️ **Zuerst. Vor allem anderen.** Kopierfertig:

```bash
cd ~/trading-bot

# --- 0a  Die neun Datenbanken sichern, BEVOR irgendetwas läuft ------------
SICHERUNG=~/tb46b_db_sicherung_$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "$SICHERUNG"
cp -p paper_trading_*.db "$SICHERUNG"/
ls -l "$SICHERUNG"
# Erwartet: NEUN Dateien.
shasum -a 256 paper_trading_*.db | tee "$SICHERUNG/vorher.sha256"

# --- 0b  Und den Rest des Laufzeitzustands gleich mit ---------------------
cp -p benachrichtigungen_schliessung.db "$SICHERUNG"/ 2>/dev/null || true
cp -p notifications/rueckfall_zustand.json \
      notifications/waechter_zustand.json "$SICHERUNG"/ 2>/dev/null || true

# --- 0c  Zweig holen und auschecken --------------------------------------
git fetch origin claude/new-session-ql406l
git checkout claude/new-session-ql406l
git log --oneline -3
```

⚠️ **Meldet `cp` weniger als neun `*.db`, hier abbrechen** und den Befund
melden — dann stimmt etwas an der Ausgangslage nicht, und alles Weitere
misst das Falsche.

---

## Schritt 1 — Datenstand vorher

```bash
trading-env/bin/python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; s=herkunft.datenstand()
print(s['datenstand'][:16], s['dateien'])"
```

**Erwartet:** `d9449faf51bffaaa 223`

---

## Schritt 2 — Die beiden reparierten Gegenproben

⚠️ **Das ist der Kern des Mac-Teils.** In der Cloud sind beide grün; auf dem
Mac laufen sie auf Python 3.9.6 und mit `binance`/`dateparser` aus
`trading-env`.

```bash
trading-env/bin/python3 shared/test_leeres_symbol.py    2>&1 | tail -6
trading-env/bin/python3 shared/test_stille_ausfaelle.py 2>&1 | tail -6
```

**Erwartet:**

| Datei | vorher (TB-46-Maclauf) | **jetzt erwartet** |
|---|---|---|
| `shared/test_leeres_symbol.py` | 43/45 | **45 von 45, 0 fehlgeschlagen** |
| `shared/test_stille_ausfaelle.py` | 23/24 | **27 von 27, 0 fehlgeschlagen** |

⚠️ `test_stille_ausfaelle.py` hat jetzt **27 statt 24** Prüfungen — das ist
kein Fehler: `teil_2` bricht nicht mehr mit einer Ausnahme ab und kommt
deshalb zu drei Prüfungen, die es vorher nie erreicht hat.

⚠️ Steht dort `NICHT PRUEFBAR`, ist der Bezugscommit `97aea88` in diesem
Klon nicht lesbar. Abhilfe:

```bash
git cat-file -e 97aea8878c9fae5e1f12d30e2ea0318dd20aadc5 && echo "Bezugscommit da"
# fehlt er:  git fetch --unshallow
```

---

## Schritt 3 — Die Probe, gegen KOPIEN

⚠️ **Die Probe legt sich ihre Datenbanken selbst an, in Wegwerf-Ordnern
ausserhalb des Arbeitsbaums.** Sie fasst weder `data/` noch eine echte `*.db`
an. Die Sicherung aus Schritt 0 ist trotzdem verlangt — Schritt 7 braucht
sie.

```bash
mkdir -p ~/tb46b_wegwerf
trading-env/bin/python3 research/ausstiegspfade/probe.py \
    --arbeitswurzel ~/tb46b_wegwerf \
    --json ergebnisse/probe_mac.json 2>&1 | tee ~/tb46b_probe_mac.txt
echo "Rueckgabewert: $?"
```

**Erwartet — neunmal dasselbe Bild, 45 Läufe, Rückgabewert 0:**

| Lage | offen vorher → nachher |
|---|---|
| **A** (Kursdatei fehlt) | **2 → 2** |
| **B** (leerer Rahmen) | **2 → 2** |
| **C1** (veraltet, Abruf scheitert) | **2 → 2** |
| **C2** (veraltet, Abruf liefert denselben Rahmen) | **2 → 1** |
| **D** (Kontrolle) | **2 → 1** |

Und je Bot die Zeile

```
=> sicher, aber mit altem Kurs handelnd: ...
```

⚠️ **Auf dem Mac ist Binance/yfinance ERREICHBAR.** Das ändert nichts: die
Probe ersetzt `fetch_historical_data` in ihrer Wegwerf-Kopie durch eine
einstellbare Gegenstelle, es wird also **kein Abruf gesendet**. Sieht man im
Protokoll trotzdem einen echten Netzzugriff, **ist das ein Befund und gehört
gemeldet** — dann greift der Austausch nicht.

⚠️ **Weicht auch nur eine Zeile vom Cloud-Bild ab**, ist das der wichtigste
Einzelbefund dieses Auftrags. Besonders zu beachten:

* **pandas 2.3.3 statt 3.0.5.** Die Cloud hat auf 2.3.3 zurückgesetzt, um dem
  Mac zu entsprechen — geprüft ist das aber nur hier.
* **`datetime.fromisoformat`** auf 3.9.6: Der Aktien-Pfad von
  `entscheidungskerze` baut `f"{tag}T00:00:00"` selbst (TB-45). Die Probe
  geht denselben Weg. Bricht sie bei den vier Aktien-Bots ab, gehört die
  Ausgabe vollständig in den Bericht.

---

## Schritt 4 — Basislauf aller Tests

```bash
trading-env/bin/python3 research/datenordner_schnitt/basislauf.py \
    --grenze 900 --json ergebnisse/basislauf_tb46b_mac.json \
    2>&1 | tee ~/tb46b_basislauf_mac.txt
```

⚠️ `shared/test_drawdown_beide_masse.py` **terminiert nicht**. Der Runner
setzt die Zeitgrenze und **beendet den Kindprozess danach wirklich**. Zur
Sicherheit hinterher:

```bash
ps aux | grep -i drawdown_beide | grep -v grep
# falls noch etwas läuft:  kill <PID>
```

**Erwartet — bekannt rot auf dem Mac, kein neuer Befund:**

| Datei | erwartet |
|---|---|
| `shared/test_stabile_sortierung.py` | 3 Fehler |
| `shared/test_wellenauswahl.py` | 1 Fehler |
| `dashboard/test_portfolio_sicht.py` | 1 Fehler |
| `research/exposure_messung/test_exposure_kern.py` | 1 Fehler |
| `research/hrp_portfolio/test_hrp_core.py` | `scipy` fehlt |
| `shared/test_drawdown_beide_masse.py` | Zeitgrenze |

**Ungeprüft (verlangen ein Bot-Argument), NICHT rot:**
`research/drawdown_reihenfolge/test_drawdown.py` ·
`research/fib_score_stufen/test_stufen.py` ·
`research/elliott_wave_params/test_params.py`

⚠️ **`system/test_log_rotation.py` ist NICHT mehr in der Bekannt-rot-Liste.**
Der Eintrag war falsch (TB-46b hat ihn gestrichen). **Erwartet: grün,
117/117.** Ist er rot, bitte melden — dann war die Streichung voreilig.

⚠️ **`shared/test_zuteilung.py` ist in der CLOUD rot** (Netzsperre). Auf dem
Mac sollte er **grün** sein. Er steht bewusst **nicht** in der
Bekannt-rot-Liste, weil die nach `docs/UMGEBUNGEN.md` Regel 3 den Rechner
nennt und eine Cloud-Zeile dort nichts zu suchen hat.

---

## Schritt 5 — Kein echter Abruf, keine Order, keine Schreibvorgänge

```bash
git status --porcelain
git status --porcelain -- data
ls -l broker/STOP broker/STOP_IBKR 2>/dev/null   # nur ansehen, nicht anlegen
```

**Erwartet:** unter `data/` **nichts**. Im übrigen Arbeitsbaum höchstens die
neuen `ergebnisse/*.json` aus Schritt 3 und 4.

⚠️ **`--echt` wird in diesem Auftrag nirgends aufgerufen.** Kein Schritt
braucht es, kein Schritt legt es nahe.

---

## Schritt 6 — Die Frage, die nur der Mac beantworten kann

> ⚠️ **Wie viele Kein-Entscheid-Tage hat es seit dem Umstellungstag
> (2026-09-16, 04:42:24Z) gegeben?**

In der Cloud gibt es weder `logs/` noch die neun `*.db` — die Frage ist dort
strukturell nicht beantwortbar. **Auf dem Mac ist sie es nur teilweise**, und
das gehört ins Ergebnis:

```bash
# 6a  Gibt es überhaupt Protokolle, und wie weit reichen sie zurück?
ls -l logs/*/ | head -40
for d in logs/*/; do
  echo "--- $d"
  head -1 "$d"/*.log 2>/dev/null | head -4
done

# 6b  Die Rückfallzeilen seit dem Umstellungstag (16.09.2026)
grep -rn "Rueckfall auf den Live-Abruf" logs/ 2>/dev/null | wc -l
grep -rn "Rueckfall auf den Live-Abruf" logs/ 2>/dev/null | tail -30

# 6c  Läufe, in denen KEIN einziges Symbol geladen wurde
#     (der Bot schreibt dafür keine eigene Zeile - deshalb über die
#      Zusammenfassung; siehe Vorbehalt unten)
grep -rn "Fehler bei " logs/ 2>/dev/null | wc -l
grep -rc "FORWARD-TEST STATUS" logs/*/*.log 2>/dev/null

# 6d  Hat der Cron überhaupt gelaufen? (Punkt 2/10 des Übergabeprotokolls)
crontab -l | grep -E "forward_test|warteauftraege|quarterly" || \
    echo "KEIN Eintrag gefunden - das ist selbst ein Befund"
```

⚠️ **Drei Vorbehalte, die mit ins Ergebnis gehören:**

1. **Das Fenster ist anderthalb Tage lang.** Der Umstellungstag war der
   16.09.2026, 04:42:24Z. Was auch immer herauskommt, ist eine sehr kleine
   Stichprobe.
2. **`system/log_rotation.py` behält 5 Stände à 1 MB.** Für dieses Fenster
   reicht das; für dieselbe Frage in vier Wochen nicht mehr.
3. ⚠️ **Die Bots schreiben keine Zeile „kein Entscheid".** Gezählt wird über
   eine **Textsuche im Protokoll**, nicht über einen Datensatz. Genau das
   soll der Vorschlag in Teil 4 des Ergebnisberichts ablösen. Die Zahl aus
   6b/6c ist deshalb eine **Näherung mit Untergrenze**, keine Messung.

---

## Schritt 7 — Nachweis: die echten Datenbanken sind byteweise identisch

⚠️ **Der Abschluss. Ohne ihn ist der Testauftrag nicht erledigt.**

```bash
cd ~/trading-bot
shasum -a 256 paper_trading_*.db > /tmp/tb46b_nachher.sha256
diff "$SICHERUNG/vorher.sha256" /tmp/tb46b_nachher.sha256 \
  && echo "OK: alle neun Datenbanken byteweise identisch" \
  || echo "⚠️ ABWEICHUNG - sofort melden und NICHTS weiter tun"
```

⚠️ **Meldet `diff` einen Unterschied, bitte sofort abbrechen und melden** —
und die Sicherung aus Schritt 0 **nicht** löschen. Zwischen Schritt 0 und
Schritt 7 kann ein **Cronjob** gelaufen sein; das ist die erste Erklärung,
die zu prüfen ist (`crontab -l`), und noch kein Fehler dieses Zweiges.

Und der Datenstand zum Schluss — dieselbe Rechnung wie in Schritt 1:

```bash
trading-env/bin/python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; s=herkunft.datenstand()
print(s['datenstand'][:16], s['dateien'])"
```

**Erwartet:** `d9449faf51bffaaa 223` — derselbe Wert wie in Schritt 1.

---

## Was zurückgemeldet werden soll

1. Die Ausgabe von **Schritt 2** (beide Zahlen, vollständig).
2. Die Ausgabe von **Schritt 3** (alle neun Bots, alle fünf Lagen) und
   `ergebnisse/probe_mac.json`.
3. Die Ausgabe von **Schritt 4** (Basislauf, Zeile je Datei) und
   `ergebnisse/basislauf_tb46b_mac.json` — mit ausdrücklichem Vermerk zu
   `system/test_log_rotation.py` und `shared/test_zuteilung.py`.
4. Die Zahlen aus **Schritt 6**, mit den drei Vorbehalten.
5. **Schritt 7**, wörtlich — die Zeile `OK: alle neun Datenbanken byteweise
   identisch`.
6. ⚠️ **Jede Abweichung von `docs/UMGEBUNGEN.md`**, die dabei auffällt.

---

## Was dieser Auftrag NICHT tut

| | |
|---|---|
| ❌ | keine Änderung an `forward_test.py`, `live_params.py`, `equity_simulation.py` |
| ❌ | keine Änderung an `shared/entscheidungskerze.py` oder `shared/paths.py` |
| ❌ | **kein `--echt`**, keine Order, kein Broker-Endpunkt |
| ❌ | kein Bot gegen eine echte Datenbank |
| ❌ | nichts unter `data/` |
| ❌ | kein Registertext geändert — Teil 4 des Berichts **schlägt vor** |
