# Testauftrag TB-35 — Abrufskripte haltbar machen

**Autonom ausführbar.** Jeder Schritt nennt den Befehl, das erwartete Ergebnis
und was zu tun ist, wenn es abweicht. **Schritte 0–6 laufen überall**,
**Schritte 7–10 brauchen den Mac** (Binance und yfinance sind aus der Cloud
gesperrt, HTTP 403 der Egress-Richtlinie).

Alle Befehle aus dem Repo-Wurzelverzeichnis (`cd ~/trading-bot`).

---

> ## ⚠️ Die eine Regel dieses Testauftrags
>
> **Kein Schritt startet ein `fetch_*.py` so, dass es nach `data/` schreibt.**
>
> Das ist keine Vorsicht, sondern der Kern: ein echter Abruf **verlängert** die
> Kursdateien um die seit dem 15.09.2026 hinzugekommenen Kerzen. Das ist
> richtig und erwünscht — aber es **ändert den Datenstand-Hash**, und der steht
> als `d9449faf51bffaaa…` bei 223 Dateien in `docs/VORREGISTRIERUNG_neuselektion.md`.
> Ihn zu ändern wäre ein Amendment der Vorregistrierung und eine Entscheidung
> des Betreibers — **nicht Teil eines Tests.**
>
> Die echten Läufe (Schritte 7–8) laufen deshalb über
> `research/abrufskripte/echtlauf.py` in einen **Wegwerf-Ordner**. Das Werkzeug
> ist so gebaut, dass es `data/` gar nicht erreichen kann: es legt ein
> Miniatur-Abbild des Projekts unter `mktemp -d` an, in dem `DATA_DIR`
> woanders hinzeigt. **Schritt 9 weist nach, dass `data/` unverändert ist.**

---

## Schritt 0 — Stand herstellen

```bash
cd ~/trading-bot
git fetch origin
git checkout claude/new-session-we9a90
git pull origin claude/new-session-we9a90
git log --oneline -1
python3 -V
python3 -c "import pandas; print('pandas', pandas.__version__)"
```

**Erwartet:** der jüngste TB-35-Commit, Python 3.9+, eine pandas-Version.

**Falls `git checkout` scheitert**, weil lokale Änderungen im Weg sind:
`git stash` — **nicht** `git checkout -- .`, solange unklar ist, was dort
liegt.

---

## Schritt 1 — Der Datenstand VOR allem anderen

```bash
python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; print(herkunft.datenstand())"
```

**Erwartet exakt:**

```
{'datenstand': 'd9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84', 'dateien': 223}
```

**Diese Zeile aufschreiben.** Schritt 9 vergleicht dagegen.

**Weicht sie ab**, ist `data/` auf diesem Rechner nicht der Stand, auf den sich
TB-34 und die Vorregistrierung beziehen. Dann **hier abbrechen und melden** —
der Rest des Testauftrags setzt diesen Stand voraus.

---

## Schritt 2 — Basislauf: es ist nichts kaputtgegangen

```bash
for f in $(find . -name "test_*.py" -not -path "./.git/*" | sort); do
  d=$(dirname "$f"); b=$(basename "$f")
  out=$(cd "$d" && timeout 900 python3 "$b" 2>&1); rc=$?
  printf "%-4s %-58s %s\n" "$rc" "$f" "$(echo "$out" | grep -E 'bestanden|OK' | tail -1 | cut -c1-60)"
done | tee /tmp/tb35_tests.txt
```

**Erwartet:** **51 Tests**, davon `shared/test_abrufschutz.py` neu und grün.

**In der Cloud waren elf rot** — alle aus fehlenden Abhängigkeiten oder aus
Tests, die ein Argument verlangen, und alle **identisch auf unverändertem
`main`** (Basislauf auf `5318795`):

| Test | Grund (Cloud) |
|---|---|
| `broker/test_ibkr.py` | Zeitzone `US/Eastern` fehlt |
| `dashboard/test_dashboard.py` | `fastapi` fehlt |
| `dashboard/test_portfolio_sicht.py` | Folgefehler daraus |
| `research/drawdown_reihenfolge/test_drawdown.py` | verlangt ein Argument |
| `research/elliott_wave_params/test_params.py` | verlangt ein Argument |
| `research/fib_score_stufen/test_stufen.py` | verlangt ein Argument |
| `research/hrp_portfolio/test_hrp_core.py` | `scipy` fehlt |
| `shared/test_drawdown_beide_masse.py` | läuft in die Zeitüberschreitung (900 s) |
| `shared/test_kursdaten.py` | `yfinance` fehlt (62/66) |
| `shared/test_stabile_sortierung.py` | 45/46 |
| `shared/test_wellenauswahl.py` | 322/323 |

**Auf dem Mac sind diese Abhängigkeiten da; dort sollten entsprechend weniger
rot sein.** Drei gelten laut Aufgabenstellung als **TB-35-fremd** und dürfen
rot bleiben:

* `dashboard/test_portfolio_sicht.py` (86/87)
* `shared/test_stabile_sortierung.py` (44/46)
* `research/exposure_messung/test_exposure_kern.py` (1 Fehlschlag)

**Ohne `node` meldet `dashboard/test_dashboard.py` 780/780 statt 784** — das
ist richtig so, `node` ist auf dem Rechner des Nutzers bewusst nicht
installiert.

> **Eine Stolperstelle, falls der Arbeitsbaum nicht sauber ist:**
> `research/pnl_2025_fixed_size/test_pnl.py` prüft am Ende, dass
> `git diff HEAD -- strategies/` **leer** ist. Der Test schlägt fehl, solange
> **nicht committete** Änderungen unter `strategies/` liegen — auch wenn sie
> völlig in Ordnung sind. Auf einem sauberen Arbeitsbaum ist er grün
> (**93/93**). Bei einem Fehlschlag dieses Tests also zuerst
> `git status --short` ansehen, bevor irgendetwas anderes vermutet wird.

**Abweichung:** rot ist **nur dann ein TB-35-Befund**, wenn derselbe Test auf
`main` grün ist. Die Gegenprobe läuft in einem **zweiten Klon** — im
Arbeitsbaum hin- und herzuschalten ist der Weg, auf dem `data/` versehentlich
angefasst wird:

```bash
git clone . /tmp/tb35_main
cd /tmp/tb35_main && git checkout main
for f in $(find . -name "test_*.py" -not -path "./.git/*" | sort); do
  d=$(dirname "$f"); b=$(basename "$f")
  out=$(cd "$d" && timeout 900 python3 "$b" 2>&1); rc=$?
  printf "%-4s %s\n" "$rc" "$f"
done > /tmp/tb35_basis_main.txt
cd ~/trading-bot
diff <(cut -c1-4,6- /tmp/tb35_basis_main.txt) \
     <(cut -c1-4,6- /tmp/tb35_tests.txt | grep -v test_abrufschutz)
```

**Erwartet:** kein Unterschied ausser `shared/test_abrufschutz.py`, den es auf
`main` noch nicht gibt. Danach: `rm -rf /tmp/tb35_main`.

---

## Schritt 3 — Die neuen Selbsttests

```bash
python3 shared/test_abrufschutz.py
```

**Erwartet:** `77 von 77 Pruefungen bestanden, 0 fehlgeschlagen.`

Sieben Abschnitte. Die vier, auf die es ankommt:

* **Abschnitt 2** startet die **acht Abrufskripte wirklich** — in einem
  Miniatur-Abbild unter `/tmp`, gegen Attrappen. Geprüft wird, was danach in
  der CSV steht, nicht der Quelltext.
* **Abschnitt 3** ist die Gegenprobe dazu: die Absicherung wird zur
  Durchreiche gemacht, und dann müssen **8 von 8** Skripten die laufende Kerze
  schreiben. Steht dort eine kleinere Zahl, prüft Abschnitt 2 weniger, als er
  behauptet.
* **Abschnitt 4** lässt einen vollständigen Abruflauf **zweimal** laufen und
  vergleicht den Datenstand-Hash.
* **Abschnitt 6** schaltet die drei Kriterien der Wache **einzeln** ab. Jedes
  Mal muss genau ein Fall verlorengehen und die anderen beiden dürfen es
  nicht.

**Abweichung:** die Ausgabe nennt den fehlgeschlagenen Punkt namentlich. Bei
einem Fehlschlag in Abschnitt 2 oder 3 **nicht weitermachen** — dann greift
der Kern der Änderung nicht.

---

## Schritt 4 — Fasst irgendetwas `data/` an?

```bash
git status --porcelain data/ | wc -l
git diff origin/main HEAD --name-only | grep '^data/' | wc -l
```

**Erwartet:** zweimal `0`.

Die zweite Zeile ist die Randbedingung der Aufgabe wörtlich: `git diff
origin/main HEAD --name-only` darf **keine** Datei unter `data/` auflisten.

---

## Schritt 5 — Die Wache von Hand, an einer Kopie

```bash
ARBEIT=$(mktemp -d) && echo "$ARBEIT"
cp data/BTCUSDT_1d.csv data/ETHUSDT_1d.csv "$ARBEIT"/

python3 shared/abrufschutz.py --aufnehmen "$ARBEIT/vorher.json" --ordner "$ARBEIT"
python3 shared/abrufschutz.py --vergleiche "$ARBEIT/vorher.json" --ordner "$ARBEIT"; echo "rc=$?"
```

**Erwartet:** `Kein Befund: ...` und `rc=0`.

Jetzt den Schaden herstellen, den die Wache finden soll — **an der Kopie**:

```bash
# vorne etwas wegnehmen (spaeterer Beginn) und hinten etwas wegnehmen
head -1 "$ARBEIT/BTCUSDT_1d.csv" > "$ARBEIT/x" && tail -n +3 "$ARBEIT/BTCUSDT_1d.csv" >> "$ARBEIT/x" && mv "$ARBEIT/x" "$ARBEIT/BTCUSDT_1d.csv"
head -n -1 "$ARBEIT/ETHUSDT_1d.csv" > "$ARBEIT/y" && mv "$ARBEIT/y" "$ARBEIT/ETHUSDT_1d.csv"

python3 shared/abrufschutz.py --vergleiche "$ARBEIT/vorher.json" --ordner "$ARBEIT"; echo "rc=$?"
```

**Erwartet:** `rc=1`, dazu mindestens

```
  [verkuerzt]        BTCUSDT_1d.csv: ... Zeilen ...
  [spaeterer_beginn] BTCUSDT_1d.csv: beginnt jetzt bei ...
  [verkuerzt]        ETHUSDT_1d.csv: ...
  [frueheres_ende]   ETHUSDT_1d.csv: endet jetzt bei ...
```

und den Satz *„Es wurde nichts gestoppt und nichts zurückgenommen — diese
Wache meldet nur."*

> `head -n -1` gibt es auf macOS nur mit den GNU-Coreutils (`ghead`). Ohne sie:
> `sed '$d' "$ARBEIT/ETHUSDT_1d.csv" > "$ARBEIT/y" && mv "$ARBEIT/y" "$ARBEIT/ETHUSDT_1d.csv"`

Aufräumen: `rm -rf "$ARBEIT"`

---

## Schritt 6 — Wer hängt an der Datei, die nicht im Repo liegt?

```bash
python3 research/abrufskripte/abrufwege.py | tee /tmp/tb35_abrufwege.txt
```

**Erwartet:** `9 Modul(e) binden sie ein.` — vier schreiben nach `data/`, fünf
lassen eine Handelsentscheidung davon abhängen.

Und jetzt die Frage nach den Zugangsdaten — **ohne den Inhalt anzuzeigen**:

```bash
ls -l shared/fetch_binance_data.py
wc -l shared/fetch_binance_data.py
grep -c -iE 'api[_-]?key|api[_-]?secret|secret|token|passwo' shared/fetch_binance_data.py
git check-ignore -v shared/fetch_binance_data.py
```

**Erwartet:** die Datei existiert, `git check-ignore` bestätigt den Eintrag in
`.gitignore`, und `grep -c` gibt eine **Zahl** aus.

> ⚠️ **`grep -c` zählt, es zeigt nicht.** *Ob* die Datei Zugangsdaten enthält,
> geht in dieses Protokoll; *welche*, geht niemanden etwas an. **Kein `cat`,
> kein `head`, kein `grep` ohne `-c` auf diese Datei** — auch nicht „nur kurz
> zum Nachsehen".

**Ist die Zahl grösser als 0:** dann ist der Weg, den
`research/abrufskripte/BERICHT.md` (Punkt 4a) beschreibt, der richtige — eine
Trennung in versionierten Code und eine unversionierte `.env`, **nicht** ein
Commit der ganzen Datei. Das ist eine Entscheidung des Betreibers und
**nicht Teil dieses Testauftrags**. Nur die Zahl notieren.

**Ist die Zahl 0:** dann spricht nichts dagegen, die Datei zu versionieren —
auch das entscheidet der Betreiber.

---

# Ab hier: nur auf dem Mac

---

## Schritt 7 — Ein echter Krypto-Abruf, in einen Wegwerf-Ordner

```bash
python3 research/abrufskripte/echtlauf.py \
    --skript strategies/t3_supertrend/fetch_4h_data.py \
    --symbole BTCUSDT,ETHUSDT | tee /tmp/tb35_echtlauf_krypto.txt
echo "rc=$?"
```

Dann dasselbe für die Tageskerzen:

```bash
python3 research/abrufskripte/echtlauf.py \
    --skript strategies/rsi2_crypto/fetch_1d_data.py \
    --symbole BTCUSDT,ETHUSDT | tee -a /tmp/tb35_echtlauf_krypto.txt
```

**Erwartet je Datei:**

```
[OK ] BTCUSDT_4h.csv
        erzeugt : NNNNN Zeilen, 2017-08-17 04:00:00 .. <juengste ABGESCHLOSSENE Kerze>
        Bestand : NNNNN Zeilen, 2017-08-17 04:00:00 .. 2026-09-15 ...
        gemeinsam NNNNN Zeile(n), davon 0 abweichend
        letzte Kerze abgeschlossen: True
```

und am Ende:

```
Kein Befund: jede erzeugte Datei endet auf einer abgeschlossenen Kerze,
und der vorhandene Bestand wird zeichengleich wiedergegeben.
```

**Das sind die drei Aussagen, um die es in TB-35 geht:**

1. `letzte Kerze abgeschlossen: True` — die laufende Kerze wird **nicht mehr
   geschrieben.** Wäre sie es, stünde hier `False` und der Rückgabewert wäre 1.
2. `davon 0 abweichend` — der vorhandene Bestand wird **zeichengleich**
   wiedergegeben. Jede Abweichung hier änderte den Datenstand-Hash, ohne dass
   ein Kurs anders wäre.
3. **Mehr Zeilen als im Bestand** — der Abruf **verlängert**, er verkürzt
   nicht. Die Differenz sind die Kerzen seit dem 15.09.2026.

### Was zu tun ist, wenn es abweicht

| Beobachtung | Bedeutung | Nächster Schritt |
|---|---|---|
| `letzte Kerze abgeschlossen: False` | Die Regel greift nicht gegen die echte Antwort. | **Melden, nicht weitermachen.** Ausgabe vollständig ins Protokoll. Wahrscheinlichste Ursache: `open_time` hat eine fünfte, hier nicht abgedeckte Form. |
| `davon N abweichend`, N > 0, und die Abweichung ist **nicht** nur die letzte Bestandszeile | Das Modul schreibt vorhandene Zeilen anders, als sie dastehen. | **Melden.** Die Ausgabe nennt die erste abweichende Zeile in beiden Fassungen — die beiden Zeilen ins Protokoll. |
| `nur die LETZTE Zeile des Bestands weicht ab` | **Das ist der Normalfall und kein Fehler:** die letzte Zeile des Bestands ist noch die alte Teilkerze aus der Zeit vor TB-34/TB-35. | Weitermachen. |
| `WACHE [verkuerzt]` o. ä. | Der echte Abruf liefert weniger Historie als vorhanden. | **Melden.** Genau dafür ist die Wache da. |
| `ModuleNotFoundError: binance` | Das Paket fehlt. | `pip3 install python-binance` im `trading-env` |

**`data/` bleibt dabei unverändert** — der Lauf schreibt ausschliesslich in den
Wegwerf-Ordner, den er am Ende selbst löscht. Mit `--behalten` bleibt er
stehen, wenn man hineinsehen will.

---

## Schritt 8 — Ein echter Aktien-Abruf, in einen Wegwerf-Ordner

```bash
python3 research/abrufskripte/echtlauf.py \
    --skript strategies/volatility_breakout/fetch_stock_data.py \
    --symbole AAPL,MSFT | tee /tmp/tb35_echtlauf_aktien.txt
echo "rc=$?"
```

**Erwartet dasselbe Muster wie in Schritt 7** — mit einer Besonderheit:

> **Die Regel wartet bei Aktien absichtlich länger als nötig.** Eine
> NYSE-Tageskerze ist um 16:00 Ortszeit fertig (20:00 bzw. 21:00 UTC); die
> Regel verlangt `D 23:59:59` UTC. Läuft dieser Schritt **zwischen 22:00 und
> 02:00 mitteleuropäischer Zeit**, fehlt die Kerze des heutigen Handelstags
> noch, obwohl die Börse schon zu ist. **Das ist richtig so**, nicht ein
> Fehler: zu spät kostet nichts, zu früh schriebe eine Teilkerze. Die
> Begründung steht im Kopf von `shared/abrufschutz.py`.
>
> Wer das nachsehen will: `letzte` in der Ausgabe ist dann das Datum von
> **gestern**, und `letzte Kerze abgeschlossen` ist trotzdem `True`.

`AAPL` und `MSFT` reichen — `period="max"` lädt je Ticker die volle Historie,
und mehr Ticker machen den Schritt nur lang.

---

## Schritt 9 — Der Nachweis: `data/` ist unangetastet

```bash
python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; print(herkunft.datenstand())"
git status --porcelain data/ | wc -l
ls /tmp | grep tb35_echtlauf || echo "kein Wegwerf-Ordner uebrig - richtig"
```

**Erwartet:** **dieselbe Zeile wie in Schritt 1**, `0`, und kein
übriggebliebener Wegwerf-Ordner.

**Weicht der Hash ab**, hat in diesem Testlauf doch etwas nach `data/`
geschrieben. Dann:

```bash
git status --porcelain data/          # welche Dateien
git checkout -- data/                 # zuruecknehmen
```

und **melden** — mit der Angabe, nach welchem Schritt die Abweichung zuerst
auftrat.

---

## Schritt 10 — Ergebnisse einsammeln und als ZIP ablegen

```bash
ZIEL=~/Downloads/TB-35_abrufskripte_testergebnisse
rm -rf "$ZIEL" && mkdir -p "$ZIEL"

# Protokolle aus den Schritten oben
cp /tmp/tb35_tests.txt              "$ZIEL"/ 2>/dev/null
cp /tmp/tb35_abrufwege.txt          "$ZIEL"/ 2>/dev/null
cp /tmp/tb35_echtlauf_krypto.txt    "$ZIEL"/ 2>/dev/null
cp /tmp/tb35_echtlauf_aktien.txt    "$ZIEL"/ 2>/dev/null

# die Selbsttests noch einmal, diesmal in eine Datei
python3 shared/test_abrufschutz.py  > "$ZIEL/selbsttests.txt" 2>&1

# der Stand, gegen den alles lief
{
  echo "Commit:   $(git rev-parse HEAD)"
  echo "Branch:   $(git rev-parse --abbrev-ref HEAD)"
  echo "Datum:    $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  echo "Python:   $(python3 -V 2>&1)"
  echo -n "Datenstand: "
  python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; print(herkunft.datenstand())"
  echo -n "data/ geaendert: "; git status --porcelain data/ | wc -l
} > "$ZIEL/herkunft.txt"

cd ~/Downloads && zip -r TB-35_abrufskripte_testergebnisse.zip \
    TB-35_abrufskripte_testergebnisse >/dev/null && cd - >/dev/null
ls -lh ~/Downloads/TB-35_abrufskripte_testergebnisse.zip
```

> ⚠️ **Das ZIP liegt in `~/Downloads`, nicht im Repo.** Eine unversionierte
> Datei im Arbeitsbaum blockiert den nächsten `git pull`. Nach dem Packen:
>
> ```bash
> git status --porcelain | grep -v '^ M' || echo "Arbeitsbaum sauber"
> ```
>
> **Erwartet:** `Arbeitsbaum sauber` — nichts Unversioniertes im Repo.

**In keine dieser Dateien gehört der Inhalt von
`shared/fetch_binance_data.py`.** Aus Schritt 6 wandert **nur die Zahl** ins
Protokoll, die `grep -c` ausgegeben hat.

---

## Zusammenfassung zum Abhaken

| # | Schritt | Erwartet | ✓ |
|---|---|---|---|
| 1 | Datenstand vorher | `d9449faf…`, 223 Dateien | |
| 2 | Basislauf | 51 Tests, keine neue rote Zeile gegenüber `main` | |
| 3 | Selbsttests | **77/77**, Abschnitt 3 meldet **8 von 8** | |
| 4 | `data/` im Diff | zweimal `0` | |
| 5 | Wache von Hand | `rc=0` unverändert, `rc=1` nach Verkürzung | |
| 6 | Abrufwege + `grep -c` | 9 Module; **nur die Zahl** notiert | |
| 7 | echter Krypto-Abruf | `abgeschlossen: True`, `0 abweichend` | |
| 8 | echter Aktien-Abruf | dasselbe | |
| 9 | Datenstand nachher | **identisch zu Schritt 1** | |
| 10 | ZIP in `~/Downloads` | vorhanden, Arbeitsbaum sauber | |

---

## In einfacher Sprache

**Was wir wissen wollten.** Ob die acht kleinen Programme, die die Kursdaten
holen, jetzt wirklich nur fertige Zeiträume speichern — und zwar nicht bloss
gegen erfundene Testdaten, sondern gegen die echte Börse. Das geht nur auf
deinem Rechner, weil die Verbindung zur Börse aus der Cloud gesperrt ist.

**Was herauskam.** Das steht nach diesem Durchlauf in deinem
Ergebnis-ZIP. Der wichtigste Satz, auf den du achten sollst, ist
`letzte Kerze abgeschlossen: True` — er bedeutet, dass die gerade laufende,
unfertige Periode nicht mitgeschrieben wurde. Der zweitwichtigste ist
`0 abweichend`: die schon vorhandenen Kurse werden Zeichen für Zeichen genauso
zurückgeschrieben, wie sie dastehen.

**Warum das so ist.** Die Programme schreiben ihre Datei jedes Mal komplett
neu. Das ist mit Absicht so geblieben: ein Programm, das nur hinten etwas
anhängt und sich dabei irrt, hinterlässt den Fehler für immer; eines, das alles
neu schreibt, ist beim nächsten Mal wieder in Ordnung. Damit man trotzdem
merkt, wenn dabei etwas verlorengeht, läuft jetzt ein Wächter mit.

**Was das für dich heisst.** Arbeite die Schritte der Reihe nach ab; keiner
verändert deine Kursdaten — Schritt 9 weist das eigens nach. Wenn irgendwo
`False` oder `abweichend` mit einer Zahl grösser als null steht: aufhören,
Ausgabe kopieren, melden. Am Ende liegt ein ZIP in deinem Downloads-Ordner,
nicht im Projektordner — sonst blockiert es beim nächsten Mal das Aktualisieren
des Projekts.
