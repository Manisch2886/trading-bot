# Testauftrag TB-33 — Nulltest S-E1 Turn-of-Month

**Autonom ausführbar.** Jeder Schritt steht für sich, mit erwarteter Ausgabe.
Die Schritte 1 bis 5 und 8 bis 10 laufen ohne Netz; **Schritt 6 und 7
brauchen Netz und `yfinance`** und sind in der Cloud-Umgebung nicht gelaufen.

> **Kein Befehl in diesem Dokument ändert einen Bot, eine `live_params.py`,
> eine Datenbank oder eine `results/*.csv`.** Kein Befehl trägt einen Cronjob
> ein. Kein Befehl ruft `--echt` auf.

**Ein Befehl nach dem anderen**, jeweils die Ausgabe prüfen, dann der
nächste.

---

## Vorbereitung

```bash
cd ~/trading-bot
source trading-env/bin/activate
```

Erwartet: die Eingabeaufforderung beginnt mit `(trading-env)`.

---

## Schritt 1 — Nichts Verbotenes angefasst

```bash
git diff origin/main HEAD --name-only | cut -d/ -f1 | sort -u
```

**Erwartet:** genau zwei Zeilen — `docs` und `research`. Nichts anderes.

```bash
git diff origin/main HEAD --name-only | grep -E "live_params|forward_test|equity_simulation|multi_symbol_" ; echo "Treffer: $?"
```

**Erwartet:** keine Zeile, `Treffer: 1`. (`grep` gibt 1 zurück, wenn es nichts
findet — hier ist das die gute Nachricht.)

```bash
git diff origin/main HEAD --name-only | grep -E "^(results|broker|config|data|system|strategies)/|zuteilung|messkette|regimewache" ; echo "Treffer: $?"
```

**Erwartet:** keine Zeile, `Treffer: 1`.

```bash
git diff origin/main HEAD --name-only | grep -E "VORREGISTRIERUNG_neuselektion|vorregistrierung/auswertung" ; echo "Treffer: $?"
```

**Erwartet:** keine Zeile, `Treffer: 1`. Beide werden **gelesen, nicht
geändert**.

---

## Schritt 2 — Das Register zum Mitlesen

```bash
python3 research/turn_of_month/register.py
```

**Erwartet** unter anderem:

```
Kerninstrument            SPY
Kernfenster               -1 bis +3 Handelstage
Kosten je Round-Trip      0.30 Prozentpunkte  (= 3.6 p.a.)
Bootstrap                 10000 Ziehungen, Seed 20260915, Niveau 0.95
Mindest-Ereigniszahl      120
```

und darunter die **Sweep-Regel** sowie die **sieben Punkte der
Handelstags-Regel**.

> Prüfen Sie hier ausdrücklich, dass die Kostenschranke **3,6 p.a.** als
> *gerechneter* Wert dasteht (0,30 × 12) und nicht als abgeschriebene Zahl.

---

## Schritt 3 — Der Selbsttest. **Das ist die Pfadfrage.**

```bash
python3 research/turn_of_month/test_turn_of_month.py
echo "Rueckgabewert: $?"
```

**Erwartet** (Laufzeit knapp eine Minute):

```
110/110 Pruefungen bestanden.
==============================================================================
WEG SAUBER - alle neun Pfadkriterien P1 bis P9 bestanden.
Keine Stelle, an der eine Entscheidung ausserhalb des Registers noetig war.
Rueckgabewert: 0
```

Fällt etwas durch, nennt die Ausgabe **welches Pfadkriterium** — und das ist
die Antwort auf die Pfadfrage, nicht ein Nebenbefund.

> Der Test braucht **keine** echten Kursdaten. Er erzeugt sie sich selbst —
> genau das ist Pfadkriterium **P1**.

---

## Schritt 4 — Die neun Kurven sind unberührt

```bash
python3 shared/ergebniskurven.py 2>&1 | tail -4
```

**Erwartet:**

```
Zusammenfassung: 9x AKTUELL

Alle geprueften Kurven passen zur heutigen Konfiguration.
```

---

## Schritt 5 — Der Wächter des Versuchsregisters

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

> **Das ist richtig so.** S-E1 steht weiterhin unter „vorgemerkte Versuche",
> weil der Datenlauf noch aussteht. *Das Register ist ein Kassenbuch* — eine
> Zahlung, die noch nicht geflossen ist, wird nicht gebucht. Die vier
> Handgriffe für danach stehen ausgeschrieben in
> `research/versuchsregister/REGISTER.md`, Abschnitt 6a.

---

## Schritt 6 — Der Datenlauf. **Nur auf dem Mac.**

> In der Cloud-Umgebung ist Yahoo nicht erreichbar (Proxy antwortet **403**)
> und `yfinance` ist nicht installiert. Dieser Schritt ist deshalb dort
> **nicht gelaufen**; die Auswertung wurde gegen erzeugte Beispieldaten
> geführt.

```bash
python3 research/turn_of_month/datenlauf.py
```

**Erwartet:** vier Zeilen, eine je Instrument, etwa

```
  SPY     8300 Handelstage  (0 unvollstaendige Kerze(n) gestrichen)  .../daten/SPY_1d.csv
  QQQ     6700 Handelstage  ...
  IWM     6300 Handelstage  ...
  EFA     5900 Handelstage  ...
```

Die genauen Zeilenzahlen hängen vom Tag ab. Wichtig ist:

* **vier** Dateien unter `research/turn_of_month/daten/` — **nicht** unter
  `data/` (TB-31 arbeitet dort parallel);
* jede Zeile nennt die Zahl der **gestrichenen unvollständigen Kerzen**.
  Steht dort etwas anderes als 0, ist das kein Fehler, sondern der Zweck von
  `shared/kursdaten`: *streichen UND zählen.*

Nachsehen, was da ist, ohne zu holen:

```bash
python3 research/turn_of_month/datenlauf.py --pruefen
```

---

## Schritt 7 — Der Lauf. **Nur auf dem Mac, nach Schritt 6.**

```bash
python3 research/turn_of_month/auswertung.py \
    --json research/turn_of_month/ergebnisse/lauf.json --protokollieren
```

**Erwartet:** ein Bericht mit fünf Blöcken — Herkunft, Test 1, Test 2, die
drei Bedingungen mit Urteil, Test 3 (Sweep), Bestätigungsperiode.

**Worauf beim Lesen zu achten ist:**

1. **Das Urteil lautet `BESTANDEN`, `DURCHGEFALLEN` oder `NICHT
   AUSWERTBAR`.** Das dritte ist kein Sonderfall der ersten beiden: es heisst
   „weniger als 120 Ereignisse", also *zu wenig Daten* — und das ist keine
   Aussage über den Effekt.
2. **`DURCHGEFALLEN` ist ein zulässiges Ergebnis**, genau wie Festlegung 12
   im Hauptregister. Es ist kein Anlass, eine Schwelle zu ändern.
3. **Die Sweep-Zeilen sind ein Bild.** Besteht eine Sweep-Variante, während
   der Kern durchfällt, bleibt das Ergebnis `DURCHGEFALLEN`. Sollte der
   Bericht je etwas anderes sagen, ist das ein Fehler — Schritt 3, Teil C
   und Probe H4 prüfen genau das.
4. **Netto, nicht brutto.** Jede Renditezahl im Bericht hat bereits 0,30
   Prozentpunkte je Round-Trip abgezogen.

Wiederholbarkeit an Ort und Stelle prüfen:

```bash
python3 research/turn_of_month/auswertung.py --json /tmp/zweiter_lauf.json
python3 - <<'EOF'
import json
a = json.load(open("research/turn_of_month/ergebnisse/lauf.json"))
b = json.load(open("/tmp/zweiter_lauf.json"))
for d in (a, b): d["herkunft"].pop("zeitpunkt_utc", None)
print("gleich" if json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
      else "UNTERSCHIEDLICH")
EOF
```

**Erwartet:** `gleich`.

---

## Schritt 8 — Die Herkunft

```bash
python3 research/turn_of_month/herkunft.py
```

**Erwartet:** Commit-, Datenstand- und Register-Hash, und
`Protokoll     keine Kettenfehler`.

> Läuft dies **vor** Schritt 6, steht bei Datenstand `(0 Kursdateien)` — das
> ist richtig und kein Fehler.
>
> Steht bei Arbeitsbaum `GEAENDERT`, ist der Lauf **nicht reproduzierbar**.
> Das ist kein Abbruch, aber es steht dann auch so in jeder Ergebnisdatei —
> und das ist der Zweck.

---

## Schritt 9 — Die Staging-Ebene

```bash
python3 research/turn_of_month/staging.py --lauf
```

**Erwartet** (nach Schritt 6; ohne Kursdaten bricht der Befehl mit einem
Hinweis auf die fehlende Datei ab, und das ist richtig):

```
2026-09-15  SPY -1/+3  Position FLAT  Portfoliogewicht 0.0
  Staging: kein Portfoliogewicht, kein Crash-Knopf, keine Datenbank, kein Eintrag unter results/.
  Frist: 12 Ereignisse, spaetestens 2027-09-30
```

**Danach unbedingt nachsehen, dass nichts entstanden ist:**

```bash
ls paper_trading_*.db | wc -l          # erwartet: 9, nicht 10
ls strategies/ | wc -l                 # erwartet: 9, nicht 10
ls results/ | grep -i turn_of_month ; echo "Treffer: $?"   # erwartet: Treffer: 1
python3 shared/ergebniskurven.py 2>&1 | tail -3            # erwartet: 9x AKTUELL
```

Stand der Frist:

```bash
python3 research/turn_of_month/staging.py --status
```

**Erwartet:** `"portfoliogewicht": 0.0`, `"frist_abgelaufen": false`, und bei
`s1_rang3_entschieden` sowie `s2_backtest_bestanden` jeweils **`null`** — das
Staging-Modul stellt sich seine Freigabe **nicht selbst aus**.

### ⚠️ Der Cronjob — **Vorschlag, nicht eingetragen**

Wie bei der Log-Rotation (`30 3 * * *`) und der Portfolio-Sicht
(`40 3 * * *`) trägt der **Betreiber** die Zeile selbst ein:

```cron
# TB-33 / S-E1 Staging - taeglich nach US-Boersenschluss, werktags.
15 23 * * 1-5 cd ~/trading-bot && ./trading-env/bin/python3 research/turn_of_month/staging.py --lauf >> logs/s_e1_staging.log 2>&1
```

Eintragen mit `crontab -e`, prüfen mit:

```bash
crontab -l | grep turn_of_month
```

**Ohne den Eintrag passiert nichts** — Signale werden nicht protokolliert,
die Frist läuft nicht an. Das ist ein bewusst möglicher Zwischenschritt,
genau wie bei den Warteaufträgen.

> Auf dem Rechner des Nutzers liess sich die Crontab am 12.09.2026 nicht
> ändern (`Operation not permitted`, Festplattenvollzugriff fürs Terminal).
> Offener Punkt 14 des Übergabeprotokolls — zuerst beheben.

---

## Schritt 10 — Alle bestehenden Tests

```bash
for f in $(find . -name "test_*.py" -not -path "./.git/*" | sort); do
  ( cd $(dirname $f) && timeout 600 python3 $(basename $f) >/dev/null 2>&1 )
  echo "$? $f"
done
```

**Erwartet auf dem Mac:** überall `0`, mit den bekannten Ausnahmen:

* `dashboard/test_dashboard.py` meldet **780/780 statt 784**, weil `node`
  bewusst nicht installiert ist — vier Prüfungen werden übersprungen. Das ist
  kein Fehlschlag.
* `research/elliott_wave_params/test_params.py` und
  `research/fib_score_stufen/test_stufen.py` brauchen ein Argument
  (`elliott_wave` oder `elliott_wave_stocks`) und geben ohne eines `1` samt
  Benutzungshinweis zurück.

**In der Cloud-Umgebung** kommen fünf vorbestehende Fehlschläge dazu
(`binance`, `scipy`, `fastapi`, `yfinance`, Zeitzone `US/Eastern`). Sie sind
mit einem Basislauf auf unverändertem `main` nachgewiesen: **dort 37 grün /
7 rot, auf diesem Zweig 38 grün / 7 rot** — dieselben sieben, plus der neue
Test dieses Auftrags.

---

## Was dieser Auftrag **nicht** prüft

* Ob der Turn-of-Month-Effekt existiert. Das entscheidet Schritt 7 auf echten
  Daten — und das Ergebnis ist **nicht** der Massstab dieses Auftrags.
* Ob S-E1 ins Buch gehört. Das entscheidet **Rang 3**, frühestens nach der
  Frist, nach den Kriterien S1–S3 in `register.py`.
