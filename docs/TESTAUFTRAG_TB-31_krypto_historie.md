# Testauftrag TB-31 — Krypto-Historie zurückladen

**Autonom ausführbar.** Jeder Schritt steht für sich, mit erwarteter Ausgabe.
Die Schritte **1 bis 9 laufen überall**, auch in der Cloud. Die Schritte
**10 bis 14 brauchen den Binance-Endpunkt** und gehören damit auf den Mac —
`api.binance.com` ist aus der Cloud-Umgebung durch die Egress-Richtlinie
gesperrt (HTTP 403 auf den CONNECT).

> **Kein Befehl in diesem Dokument startet einen Selektionslauf**, und keiner
> der Schritte 1–9 schreibt irgendetwas unter `data/`. Die Schritte 12 und 13
> schreiben unter `data/`, und zwar nur dort — sie sind ausdrücklich als
> solche gekennzeichnet.

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

**Erwartet:** genau drei Zeilen, in dieser Reihenfolge — `docs`, `research`,
`shared`. **Kein `data`**, kein `strategies`, kein `results`, kein `broker`,
kein `config`.

```bash
git diff origin/main HEAD --name-only | grep -E "live_params|forward_test|equity_simulation|multi_symbol_" ; echo "Treffer: $?"
```

**Erwartet:** keine Zeile, `Treffer: 1`. (`grep` gibt 1 zurück, wenn es
nichts findet — hier ist das die gute Nachricht.)

```bash
git diff origin/main HEAD --name-only | grep -E "^(results|broker|config|data|strategies)/|zuteilung|messkette" ; echo "Treffer: $?"
```

**Erwartet:** keine Zeile, `Treffer: 1`.

---

## Schritt 2 — Selbsttest des Laders

```bash
python3 shared/test_binance_historie.py
echo "Rueckgabewert: $?"
```

**Erwartet:** als letzte Zeilen

```
75/75 Pruefungen bestanden.
Rueckgabewert: 0
```

**Was hier geprüft wird** — neun Teile, jeder unabhängig rot zu bekommen:

| Teil | Frage |
|---|---|
| A | Mindestpause, Gewichts-Kopffeld, 429 mit `Retry-After`, 418 **ohne** Wiederholung |
| B | Datenbeginn: geht die Anfrage wirklich mit `startTime=0, limit=1` hinaus? |
| C | Blättern über die 1000-Kerzen-Grenze, ohne Doppel und ohne Lücke |
| D | Überlappung Zeile für Zeile; Kurs hart, Volumen-Rundung weich, Lücke gemeldet |
| E | Verlängern statt überschreiben: Altzeilen **zeichengleich** |
| F | Wiederholbarkeit: zweiter und dritter Lauf byte-identisch |
| G | die führende Teilkerze der abgeleiteten `*_1d.csv` |
| H | **jede Wache einzeln** — die Sonderfall-Bedingung darf den Vergleich nicht ersetzen |
| I | drei zweistufige Mutationsproben |

Der Test geht **nicht** ins Netz und fasst `data/` nicht an.

---

## Schritt 3 — Selbsttest des Faltenplan-Rechners

```bash
python3 research/krypto_historie/test_faltenplan.py
echo "Rueckgabewert: $?"
```

**Erwartet:**

```
38/38 Pruefungen bestanden.
Rueckgabewert: 0
```

Teil A ist der tragende: **dieselbe Rechnung reproduziert den von Hand
geschriebenen Aktien-Faltenplan des Registers** (Selektion 2019–2025,
Bestätigung 2026) — und liest ihn dafür aus
`docs/VORREGISTRIERUNG_neuselektion.md`, nicht aus einer Kopie im Test.

---

## Schritt 4 — Probelauf gegen die echten Kursdateien

```bash
python3 research/krypto_historie/probelauf.py --alle
echo "Rueckgabewert: $?"
```

**Erwartet:** als letzte Zeilen

```
453/453 Pruefungen bestanden.
```
gefolgt vom Hinweis, dass die Vorgeschichte erzeugt ist, und
`Rueckgabewert: 0`. Dauer: rund zwei Minuten.

**Was hier läuft:** der echte Lader gegen Kopien der echten Repo-Dateien. Im
überlappenden Bereich liefert die nachgebildete Gegenstelle Zeile für Zeile
das, was in `data/` steht; erzeugt ist nur die Vorgeschichte davor. Belegt
ist damit der **Ablauf**, nicht der Kursinhalt.

```bash
git status --porcelain data/ ; echo "Treffer: $?"
```

**Erwartet:** keine Zeile. Der Probelauf arbeitet in einem Temporärordner.

---

## Schritt 5 — Die Faltenzahl heute

```bash
python3 research/krypto_historie/faltenplan.py
```

**Erwartet:** für **alle fünf** Krypto-Bots `#Sel` = **0** und
`Best.: 2026 (bis Go-Live-Schnitt)`, dann der Hinweisblock

```
!! KEIN Bot hat eine einzige Selektionsfalte.
```

und unter „Marktphasen": `fehlt` für den Zyklus 2018 und den Einbruch März
2020, `vollstaendig` für den Bärenmarkt 2022.

### Die Gegenrechnung mit zwei Jahren Mindesttraining

```bash
python3 research/krypto_historie/faltenplan.py --mindesttraining 2
```

**Erwartet:** erste Falte 2024; `#Sel` = **2** (2024, 2025) für die vier
Einjahres-Bots und **1** für `elliott_wave`. Ausserdem:
`11 von 24 Symbolen kommen in KEINER Selektionsfalte vor`.

> **Der Unterschied ist wichtig.** Der Auftragstext nennt „zwei Testfalten
> (2024, 2025)" — das ist die Rechnung mit **zwei** Jahren. Das Register legt
> in Abschnitt 5.1 Regel 2 aber **vier** Jahre fest, und damit sind es
> **null**. Die Lage ist schlechter als angenommen, nicht besser.

---

## Schritt 6 — Die drei unveränderten Wachen

```bash
python3 shared/kursdaten.py ; echo "Rueckgabewert: $?"
```

**Erwartet:** `Geprueft: 242 Datei(en)`, genau **ein** Befund —
`APH_1d.csv  1 von 8764 Kerze(n)  <- betrifft die LETZTE Kerze` — und
`Rueckgabewert: 1`. (Ein Aktien-Symbol; von TB-31 unberührt.)

```bash
python3 shared/determinismus.py --schnell | grep -c DETERMINISTISCH
```

**Erwartet:** `18` (jeder der neun Bots erscheint in zwei Tabellen).
Entscheidend: **kein** `NICHT DETERMINISTISCH`.

```bash
python3 shared/ergebniskurven.py | tail -4
```

**Erwartet:** `Zusammenfassung: 9x AKTUELL`.

---

## Schritt 7 — Der Basislauf für die vorbestehenden Fehlschläge

In der Cloud fehlen Bot-Abhängigkeiten. Diese Fehlschläge sind **vorbestehend**
und mit einem Lauf auf unverändertem `main` nachzuweisen:

```bash
git stash list >/dev/null; git worktree add /tmp/tb31_basis origin/main 2>/dev/null
cd /tmp/tb31_basis
for f in $(find . -name "test_*.py" -not -path "./.git/*" | sort); do
  ( cd $(dirname $f) && timeout 900 python3 $(basename $f) >/dev/null 2>&1 )
  printf "%-58s rc=%s\n" "$f" "$?"
done
cd ~/trading-bot; git worktree remove /tmp/tb31_basis
```

**Erwartet in der Cloud** (auf dem Mac mit vollständiger Umgebung sind es
weniger): `rc=1` bei

| Datei | Grund |
|---|---|
| `broker/test_ibkr.py` | Zeitzone `US/Eastern` fehlt |
| `dashboard/test_dashboard.py` | `fastapi` fehlt |
| `dashboard/test_portfolio_sicht.py` | 2 von 68 (`fastapi`) |
| `research/hrp_portfolio/test_hrp_core.py` | `scipy` fehlt |
| `shared/test_kursdaten.py` | 4 von 66 (`binance`, Bot-Module) |
| `research/drawdown_reihenfolge/test_drawdown.py` | braucht ein Argument |
| `research/elliott_wave_params/test_params.py` | braucht ein Argument |
| `research/fib_score_stufen/test_stufen.py` | braucht ein Argument |

Derselbe Lauf auf diesem Zweig muss **dieselbe** Liste ergeben, plus
`shared/test_binance_historie.py rc=0` und
`research/krypto_historie/test_faltenplan.py rc=0`.

Ohne `node` überspringt `dashboard/test_dashboard.py` vier Prüfungen und
meldet 780/780 statt 784.

---

## Schritt 8 — Gegenproben: die Wachen müssen rot werden können

Jede Probe verfälscht **eine** Stelle und stellt sie danach wieder her.

### 8a — Der Überlappungsvergleich

```bash
cp shared/binance_historie.py /tmp/bh.bak
python3 - <<'EOF'
p="shared/binance_historie.py"; t=open(p).read()
alt="    hart = harte_befunde(befunde)\n    fuehrende_teilkerze"
assert alt in t
open(p,"w").write(t.replace(alt, "    hart = []\n    fuehrende_teilkerze", 1))
EOF
python3 shared/test_binance_historie.py > /tmp/gegenprobe_8a.txt 2>&1
echo "Rueckgabewert: $?"
grep -c FEHLT /tmp/gegenprobe_8a.txt
cp /tmp/bh.bak shared/binance_historie.py
```

**Erwartet:** `Rueckgabewert: 1` und **13** `FEHLT`-Zeilen (bei einer spaeter
erweiterten Pruefung mehr; entscheidend ist: nicht null). Danach
`python3 shared/test_binance_historie.py` wieder `75/75`.

**Wenn hier `0` steht, ist der Test wertlos** — dann prüft er nicht, was er
zu prüfen vorgibt.

### 8b — Die Vorlaufzeit des Faltenplans

```bash
cp research/krypto_historie/faltenplan.py /tmp/fp.bak
sed -i'' -e 's/^MINDESTTRAINING_JAHRE = 4$/MINDESTTRAINING_JAHRE = 1/' research/krypto_historie/faltenplan.py
python3 research/krypto_historie/test_faltenplan.py > /tmp/gegenprobe_8b.txt 2>&1
echo "Rueckgabewert: $?"
grep -c FEHLT /tmp/gegenprobe_8b.txt
cp /tmp/fp.bak research/krypto_historie/faltenplan.py
```

**Erwartet:** `Rueckgabewert: 1` und **10** `FEHLT`-Zeilen. Danach
wieder `38/38`.

### 8c — Der Registerbezug

```bash
cp docs/VORREGISTRIERUNG_neuselektion.md /tmp/reg.bak
sed -i'' -e 's/| 2019, 2020, 2021, 2022, 2023, 2024, 2025 | 2026 |/| 2020, 2021, 2022, 2023, 2024, 2025 | 2026 |/' docs/VORREGISTRIERUNG_neuselektion.md
python3 research/krypto_historie/test_faltenplan.py 2>&1 | grep -c FEHLT
cp /tmp/reg.bak docs/VORREGISTRIERUNG_neuselektion.md
```

**Erwartet:** **12**, jedenfalls nicht `0`. Der Test liest den Plan wirklich aus dem
Register; eine Kopie im Testcode bliebe hier grün.

---

## Schritt 9 — Die Endkontrolle vor den Mac-Schritten

```bash
git status --porcelain ; echo "Treffer: $?"
```

**Erwartet:** keine Zeile (alle Gegenproben zurückgenommen).

---

# Ab hier: nur auf dem Mac (Binance-Endpunkt nötig)

> **Schritt 10 und 11 schreiben nichts.** Erst Schritt 12 verändert Dateien
> unter `data/`.

## Schritt 10 — Die Messung: ab wann reicht der Endpunkt je Symbol?

```bash
python3 shared/binance_historie.py --messen \
  --bericht research/krypto_historie/daten/messung_endpunkt.json
echo "Rueckgabewert: $?"
```

**Erwartet:** eine Tabelle `Symbol | Endpunkt 1h | Endpunkt 4h | Endpunkt 1d
| Datei heute (1h)`, rund 72 Anfragen, `Rueckgabewert: 0`.

**Worauf zu achten ist:**

1. Für die **13** Symbole, die heute am `2021-09-01` beginnen, muss dort ein
   **früheres** Datum stehen. Tut es das nicht, war die Annahme dieser
   Aufgabe falsch und der Rest entfällt.
2. Für die **11** übrigen (`PROMUSDT`, `SUIUSDT`, `PEPEUSDT`, `WLDUSDT`,
   `ENAUSDT`, `TRUMPUSDT`, `BMTUSDT`, `PUMPUSDT`, `ZKCUSDT`, `ENSOUSDT`,
   `UUSDT`) muss das Endpunkt-Datum mit dem Dateidatum **übereinstimmen** —
   das ist die Gegenprobe, dass `--messen` wirklich misst und nicht rät.

```bash
python3 research/krypto_historie/faltenplan.py \
  --messung research/krypto_historie/daten/messung_endpunkt.json
```

**Erwartet:** `#Sel` = **4** für `t3_supertrend`, `rsi2_crypto`,
`turtle_soup_crypto`, `volatility_breakout_crypto` und **2** für
`elliott_wave`, jeweils ab erster Falte **2022**.

> Weicht die erste Falte von 2022 ab, ist das kein Fehler, sondern eine
> Messung — dann stimmt die Annahme „BTC ab zweitem Halbjahr 2017" nicht, und
> die Zahlen des Berichts sind entsprechend zu korrigieren.

---

## Schritt 11 — Trockenlauf: lädt, vergleicht, schreibt nicht

```bash
python3 shared/binance_historie.py --trockenlauf \
  --bericht research/krypto_historie/daten/trockenlauf.json \
  | tee /tmp/tb31_trocken.txt
echo "Rueckgabewert: $?"
```

Dauer: rund 10–15 Minuten (etwa 2.500 Anfragen bei 0,25 s Mindestpause).

**Erwartet in der Zusammenfassung:**

* `Der ueberlappende Bereich ist in jeder Datei identisch.` für alle `_1h`-
  und `_4h`-Dateien, und
* bei den `_1d`-Dateien der 13 beschnittenen Symbole je ein harter Befund in
  der **ersten** Zeile mit dem Grund
  `fuehrende Teilkerze weicht ab - mit --teilkerze-ersetzen ...`

```bash
grep -c "harte Abweichung" /tmp/tb31_trocken.txt
git status --porcelain data/ ; echo "Treffer: $?"
```

**Erwartet:** die zweite Zeile ist leer, `Treffer: 1` — der Trockenlauf hat
**nichts** geschrieben.

> ⚠️ **Meldet eine `_1h`- oder `_4h`-Datei eine harte Abweichung, hier
> aufhören.** Das wäre ein Befund über die vorhandenen Kursdaten und keine
> Sache, die man mit einem Schalter wegschaltet. Der Bericht unter
> `daten/trockenlauf.json` nennt Zeitpunkt, Spalte, alten und neuen Wert.

---

## Schritt 12 — Der Ladelauf ⚠️ schreibt unter `data/`

```bash
python3 shared/binance_historie.py \
  --teilkerze-ersetzen \
  --bericht research/krypto_historie/daten/ladelauf.json \
  | tee /tmp/tb31_laden.txt
echo "Rueckgabewert: $?"
```

**Erwartet:** `72 Datei(en) geprueft` (24 Symbole × 3 Zeitrahmen) und
**mindestens 39 verlängert** — das sind die 13 vom 1825-Tage-Fenster
beschnittenen Symbole in drei Zeitrahmen. Die **11 spät gelisteten** Symbole
beginnen bereits am Datenbeginn des Endpunkts; bei ihnen meldet der Lauf
`Datei beginnt bereits am Datenbeginn des Endpunkts` und schreibt **nicht**.

In der Zeile `Datenqualitaet:` steht die Zahl der gestrichenen
unvollständigen Kerzen. **Diese Zahl gehört in den Bericht** — mit der
längeren Historie können es mehr sein als bisher.

### Die Wiederholbarkeitsprobe

```bash
md5 -q data/BTCUSDT_1h.csv data/BTCUSDT_4h.csv data/BTCUSDT_1d.csv > /tmp/tb31_vor.txt
python3 shared/binance_historie.py --teilkerze-ersetzen > /dev/null
md5 -q data/BTCUSDT_1h.csv data/BTCUSDT_4h.csv data/BTCUSDT_1d.csv > /tmp/tb31_nach.txt
diff /tmp/tb31_vor.txt /tmp/tb31_nach.txt && echo "byte-identisch"
```

**Erwartet:** `byte-identisch`. Ein zweiter Lauf liefert dieselben Dateien.

---

## Schritt 13 — Die Wirkung belegen ⚠️ liest `data/`, schreibt nichts

```bash
python3 shared/kursdaten.py ; echo "Rueckgabewert: $?"
```

**Erwartet:** die Zahl der Befunde — mit der neuen Historie möglicherweise
mehr als der eine `APH_1d.csv`. **Jeder neue Befund gehört in den Bericht.**

```bash
python3 research/krypto_historie/faltenplan.py \
  --json research/krypto_historie/daten/faltenplan_nachher.json
```

**Erwartet:** dieselben Zahlen wie in Schritt 10 — jetzt aus den Kursdateien
statt aus dem Messbericht gelesen. **Weichen sie voneinander ab, hat der
Ladelauf nicht geladen, was er gemessen hat.**

```bash
python3 shared/determinismus.py --schnell | grep -c "NICHT DETERMINISTISCH"
```

**Erwartet:** `0`.

```bash
python3 shared/ergebniskurven.py --json /tmp/tb31_nachher.json | tail -4
```

**Erwartet:** `Zusammenfassung: 5x ABWEICHEND, 4x AKTUELL`.

> **Das ist die schärfste Probe dieses Auftrags.** Die fünf Krypto-Bots
> **müssen** ABWEICHEND melden — sonst hat die neue Historie nichts bewirkt.
> Die vier Aktien-Bots **müssen** AKTUELL bleiben — meldet einer von ihnen
> ABWEICHEND, hat der Lauf etwas angefasst, was er nicht anfassen durfte.

```bash
python3 - <<'EOF'
import json
vor = {e["bot"]: e for e in json.load(open("research/krypto_historie/daten/kennzahlen_vorher.json"))}
nach = {e["bot"]: e for e in json.load(open("/tmp/tb31_nachher.json"))}
print(f"{'Bot':<28}{'Rendite vorher':>16}{'nachher':>12}{'MaxDD vorher':>16}{'nachher':>12}")
for bot in sorted(vor):
    a, b = vor[bot]["heute"], nach[bot]["heute"]
    print(f"{bot:<28}{a['rendite_pct']:>15.2f}%{b['rendite_pct']:>11.2f}%"
          f"{a['max_drawdown_pct']:>15.2f}%{b['max_drawdown_pct']:>11.2f}%")
EOF
```

**Erwartet:** die Vorher/Nachher-Tabelle je Bot. Bei den vier Aktien-Bots
müssen beide Spalten **gleich** sein.

> **Die Ergebniskurven bitte NICHT neu erzeugen** (`--erzeugen`). `ABWEICHEND`
> ist nach dem Laden richtig. Ob und wann neu gerechnet wird, entscheidet der
> Betreiber, und es gehört in denselben Schritt wie die Neuselektion.

---

## Schritt 14 — Was danach offen bleibt

Nichts davon gehört in diesen Auftrag; es steht hier, damit es nicht
untergeht:

1. **Der Krypto-Faltenplan gehört ins Register.** `docs/VORREGISTRIERUNG_neuselektion.md`
   Abschnitt 5.3 enthält noch die Platzhalter. Mit hineingehört die Lesart
   von „je Symbol" (mindestens **ein** Symbol — siehe `faltenplan.py`), weil
   die Regel das offenlässt.
2. **`elliott_wave` bleibt bei zwei Selektionsfalten** — wegen seiner
   Faltenlänge von zwei Jahren, nicht wegen der Daten. Ob das genügt, ist
   eine Entscheidung des Betreibers.
3. **Elf von 24 Symbolen kommen in keiner Selektionsfalte vor.** Ob das
   Universum der Selektion und das Universum des Handels auseinanderfallen
   dürfen, ist ebenfalls eine Entscheidung des Betreibers.
4. **Die abgeleiteten Tagesdateien.** Nach Schritt 12 sind sie vorn nativ und
   hinten abgeleitet. `strategies/rsi2_crypto/fetch_1d_data.py` und
   `strategies/volatility_breakout_crypto/fetch_1d_data.py` sind die nativen
   Abrufwege — ob sie den täglichen Cronjob-Pfad ersetzen sollen, ist eine
   getrennte Frage und hier bewusst **nicht** angefasst.
