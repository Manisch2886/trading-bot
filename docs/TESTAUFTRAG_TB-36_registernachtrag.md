# Testauftrag TB-36 — Faltenplan und Registernachtrag

**Autonom ausführbar.** Jeder Schritt nennt den Befehl, das erwartete Ergebnis
und was zu tun ist, wenn es abweicht. **Alle Schritte laufen auf dem Mac ohne
Netzzugang** — TB-36 ruft keine Kursdaten ab und braucht weder Binance noch
yfinance.

Alle Befehle aus dem Repo-Wurzelverzeichnis (`cd ~/trading-bot`).

---

> ## ⚠️ Die eine Regel dieses Testauftrags
>
> **Kein Schritt schreibt nach `data/`, `strategies/` oder
> `research/vorregistrierung/`.**
>
> TB-36 ist Registerarbeit: es rechnet Zahlen aus vorhandenen Dateien und
> trägt sie ein. Die beiden Werkzeuge sind **rein lesend** und öffnen keine
> Datei zum Schreiben ausser der, die man ihnen mit `--json` nennt. Zwei
> Schritte dieses Auftrags legen Wegwerf-Kopien unter `mktemp -d` an und
> verändern dort etwas — **niemals im Repo**. Schritt 9 weist nach, dass der
> Arbeitsbaum danach sauber ist und der Datenstand-Hash unverändert.

---

## Schritt 0 — Stand herstellen

```bash
cd ~/trading-bot
git fetch origin
git checkout claude/new-session-wt4193
git pull origin claude/new-session-wt4193
git log --oneline -1
python3 -V
```

**Erwartet:** der jüngste TB-36-Commit, Python 3.9 oder neuer.

**Falls `git checkout` scheitert**, weil lokale Änderungen im Weg sind:
`git stash` — **nicht** `git checkout -- .`, solange unklar ist, was dort
liegt.

> **Hinweis:** TB-36 braucht **kein** `pandas` und kein `numpy`. Die beiden
> Werkzeuge sind reine Standardbibliothek und laufen auch auf Python 3.9.
> Wenn ein Schritt trotzdem `ModuleNotFoundError: pandas` meldet, stammt das
> von einem **anderen** Test, nicht von TB-36.

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
die Vorregistrierung bezieht. Dann **hier abbrechen und melden** — alle Zahlen
dieses Testauftrags setzen diesen Stand voraus.

---

## Schritt 2 — Basislauf: es ist nichts kaputtgegangen

```bash
for f in $(find . -name "test_*.py" -not -path "./.git/*" | sort); do
  d=$(dirname "$f"); b=$(basename "$f")
  out=$(cd "$d" && timeout 900 python3 "$b" 2>&1); rc=$?
  printf "%-4s %-58s %s\n" "$rc" "$f" "$(echo "$out" | grep -E 'bestanden|OK' | tail -1 | cut -c1-60)"
done | tee /tmp/tb36_tests.txt
```

**Erwartet:** `research/faltenplan_neun/test_faltenplan_neun.py` mit
Rückgabewert **0** und `145/145 Pruefungen bestanden`.

**Zu den roten Zeilen:** Auf dem Mac sollten deutlich weniger rot sein als in
der Cloud (dort fehlen `pandas`, `scipy`, `binance`, `yfinance`, `node` und die
Zeitzone `US/Eastern`). Die Liste der in der Cloud bekannten roten Tests steht
in `docs/UEBERGABE_TB-36_registernachtrag.md`, Abschnitt „Testlage". **Keiner
davon berührt TB-36.**

**Wenn eine Zeile rot ist, die dort nicht steht**, ist sie ein Befund: Datei,
Rückgabewert und die letzten Zeilen der Ausgabe notieren. Dann prüfen, ob sie
auch auf `main` rot ist:

```bash
git stash list   # nur zur Sicherheit: nichts Eigenes verlieren
git worktree add /tmp/tb36_basis origin/main
(cd /tmp/tb36_basis/<ordner> && python3 <testdatei>)
git worktree remove /tmp/tb36_basis
```

Ist sie dort **auch** rot, ist sie vorbestehend und nicht TB-36.

---

## Schritt 3 — Der Faltenplan für alle neun Bots

```bash
python3 research/faltenplan_neun/faltenplan_neun.py
```

**Erwartet — die erste Tabelle, Spalten „1. Falte" und „#Sel":**

| Bot | 1. Falte | #Sel | Falten |
|---|---:|---:|---|
| `elliott_wave` | 2019 | 3 | 2019-2020, 2021-2022, 2023-2024 · Best. 2025-2026 |
| `t3_supertrend` | 2019 | 7 | 2019 … 2025 · Best. 2026 |
| `rsi2_crypto` | 2019 | 7 | 2019 … 2025 · Best. 2026 |
| `turtle_soup_crypto` | 2019 | 7 | 2019 … 2025 · Best. 2026 |
| `volatility_breakout_crypto` | 2019 | 7 | 2019 … 2025 · Best. 2026 |
| `elliott_wave_stocks` | 2019 | 7 | 2019 … 2025 · Best. 2026 |
| `rsi2_mean_reversion` | 2019 | 7 | 2019 … 2025 · Best. 2026 |
| `turtle_soup_stocks` | 2019 | 7 | 2019 … 2025 · Best. 2026 |
| `volatility_breakout` | 2019 | 7 | 2019 … 2025 · Best. 2026 |

**Erwartet — die zweite Tabelle („Symbolzahl je Falte, Lesart A"):**

* die fünf Krypto-Bots: `6 / 9 / 13 / 13 / 13 / 17 / 18`, Bestätigung `23`
  (bei `elliott_wave` wegen der Doppeljahre: `6 / 13 / 13`, Bestätigung `18`)
* die vier Aktien-Bots: `140 / 142 / 145 / 147 / 148 / 148 / 149`,
  Bestätigung `150`

**Erwartet — die letzte Tabelle („Welche Schranke bindet"):** bei **acht** Bots
`Registerschranke 2019`, bei `rsi2_crypto` `Daten/Indikator-Vorlauf`.

**Weicht eine Zahl ab**, ist das ein **Befund** und der Testauftrag endet hier:
die Zahlen stehen genau so im Register (`docs/VORREGISTRIERUNG_neuselektion.md`,
Abschnitt 15.5 und 15.6). Ausgabe vollständig sichern und melden.

---

## Schritt 4 — Die Gegenprobe Krypto, von Hand

Das ist die Probe, die die Aufgabenstellung „nicht verhandelbar" nennt. Sie
läuft auch als Teil A des Selbsttests, aber sie ist wichtig genug, um sie
einmal mit eigenen Augen zu sehen.

```bash
python3 research/krypto_historie/faltenplan.py --mindesttraining 0
```

**Erwartet:** dieselben Faltenlisten und dieselben Symbolzahlen wie in
Schritt 3 für die fünf Krypto-Bots — erste Falte 2019, sieben Selektionsfalten
bei den Tagesbots, drei Doppeljahr-Falten bei `elliott_wave`, Symbole je Falte
`6 / 9 / 13 / 13 / 13 / 17 / 18`, Bestätigung `23`.

Und dieselben sechs Symbole ohne Faltenevidenz: `BMTUSDT`, `ENSOUSDT`,
`PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT`.

**Weicht etwas ab:** Befund, melden, nicht weiterrechnen.

---

## Schritt 5 — Das Embargo je Bot

```bash
python3 research/faltenplan_neun/embargo_neun.py
```

**Erwartet:**

| Bot | Art | Embargo |
|---|---|---:|
| `elliott_wave` | zeitbremse | **11** |
| `t3_supertrend` | **perzentil** | **13** |
| `rsi2_crypto` | zeitbremse | **11** |
| `turtle_soup_crypto` | zeitbremse | **11** |
| `volatility_breakout_crypto` | zeitbremse | **16** |
| `elliott_wave_stocks` | zeitbremse | **91** |
| `rsi2_mean_reversion` | zeitbremse | **11** |
| `turtle_soup_stocks` | zeitbremse | **11** |
| `volatility_breakout` | zeitbremse | **16** |

Im Abschnitt „Herkunft je Zahl" steht zu jeder Zahl die Datei **mit
Zeilennummer**. Stichprobe (eine reicht):

```bash
sed -n '34p' strategies/rsi2_crypto/live_params.py
sed -n '70p' strategies/elliott_wave_stocks/backtest_elliott.py
```

**Erwartet:** `MAX_HOLD_DAYS = 10 …` bzw. `MAX_HOLD_HOURS = 90 …`.

**Weicht die Zeilennummer ab**, weil jemand die Datei bearbeitet hat: das ist
**kein** Fehler des Werkzeugs — es liest die Zeile bei jedem Lauf neu. Wichtig
ist nur, dass der **Wert** derselbe ist.

---

## Schritt 6 — Der Selbsttest, ausführlich

```bash
python3 research/faltenplan_neun/test_faltenplan_neun.py; echo "Rueckgabewert: $?"
```

**Erwartet:** `145/145 Pruefungen bestanden.` und `Rueckgabewert: 0`.
Laufzeit rund eine Minute — die vier Mutationsproben starten das Werkzeug
jeweils als eigenen Prozess.

**Die vier Mutationsproben sind der eigentliche Gehalt dieses Schritts.**
Jede kopiert den Ordner (bzw. eine Bot-Datei) nach `mktemp -d`, ändert dort
**eine** Zeile und startet das Werkzeug neu:

| Probe | Was sie verfälscht | Was sich zeigen muss |
|---|---|---|
| F | die Registerschranke 2019 | acht der neun Pläne beginnen dann früher |
| G | die Doppeljahr-Schwelle 30 | `elliott_wave` bekommt sieben statt drei Falten |
| H | den Indikator-Vorlauf 150 | Lesart B fällt mit Lesart A zusammen |
| I | die Zeitbremse **in der Bot-Datei** | das Embargo wandert von 11 auf 43 |

**Wenn eine Probe grün bleibt, obwohl sie rot werden müsste**, ist das der
schwerste denkbare Befund dieses Testauftrags: dann trägt die zugehörige Regel
nicht. Ausgabe vollständig sichern und melden.

**Wenn Teil E scheitert** („eine Vorfassung ohne Nachtrag ist auffindbar"),
liegt das an der git-Historie, nicht am Register: Teil E sucht die jüngste
committete Fassung des Registers **ohne** Abschnitt 15 und prüft, dass keine
ihrer Zeilen verschwunden ist. In einem flachen Klon (`--depth 1`) findet er
sie nicht. Dann `git fetch --unshallow` und Schritt 6 wiederholen.

---

## Schritt 7 — Der Registernachtrag ist vollständig

```bash
grep -n "^### 15\.\|^## 15\." docs/VORREGISTRIERUNG_neuselektion.md
grep -c "ERSETZT durch Abschnitt 15" docs/VORREGISTRIERUNG_neuselektion.md
```

**Erwartet:** die Abschnitte 15.0 bis 15.9, darunter je einer mit
`Registertext 0` bis `Registertext 5` — und **3** Verweise im alten Text
(Abschnitt 3 „Der Faltenplan", 5.1, 5.3); der vierte Hinweis steht bei
Sperrliste Nr. 8 und ist eingerückt.

```bash
grep -n "ersetzt" docs/VORREGISTRIERUNG_neuselektion.md | grep -i "fassung\|mindestens 4\|heutigen Parameter"
```

**Erwartet:** die drei Kennzeichnungen aus Registertext 1c, 4b und 4c sowie der
Hinweis bei Registertext 3 („ersetzt die frühere Fassung vollständig").

```bash
git diff origin/main -- docs/VORREGISTRIERUNG_neuselektion.md | grep -c "^-[^-]"
```

**Erwartet: `0`.** Es ist **keine** Zeile entfernt worden — nur hinzugefügt.
Das ist der maschinelle Nachweis dafür, dass der Verlauf lesbar bleibt.

**Ist die Zahl grösser als 0**, wurde bestehender Text umgeschrieben. Das wäre
ein Befund: die entfernten Zeilen (`git diff origin/main -- docs/… | grep "^-"`)
sichern und melden.

---

## Schritt 8 — Keine Kursdatei, kein Bot-Code angefasst

```bash
git diff origin/main --name-only
```

**Erwartet — genau diese Dateien und keine weitere:**

```
docs/ERGEBNIS_TB-36_registernachtrag.md
docs/TESTAUFTRAG_TB-36_registernachtrag.md
docs/UEBERGABE_TB-36_registernachtrag.md
docs/VORREGISTRIERUNG_neuselektion.md
research/faltenplan_neun/BERICHT.md
research/faltenplan_neun/daten/embargo.json
research/faltenplan_neun/daten/faltenplan.json
research/faltenplan_neun/embargo_neun.py
research/faltenplan_neun/faltenplan_neun.py
research/faltenplan_neun/test_faltenplan_neun.py
```

```bash
git diff origin/main --name-only | grep -c "^data/"
git diff origin/main --name-only | grep -c "^strategies/"
git diff origin/main --name-only | grep -c "^broker/"
git diff origin/main --name-only | grep -c "research/vorregistrierung/"
```

**Erwartet: viermal `0`.** Keine Kursdatei, kein Bot-Code, nichts unter
`broker/`, und die eingefrorene Vorregistrierung unberührt.

---

## Schritt 9 — Der Datenstand am Ende

```bash
python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; print(herkunft.datenstand())"
git status --short
```

**Erwartet:** dieselbe Zeile wie in Schritt 1 (`d9449faf51bffaaa…`, 223
Dateien) und ein **leerer** `git status`.

**Weicht der Hash ab oder ist `git status` nicht leer**, hat ein Schritt
geschrieben, der nicht schreiben darf. Dann: `git status --short` sichern,
**nichts wegwerfen**, melden.

---

## Schritt 10 — Ergebnisse einpacken

⚠️ **Das ZIP gehört nach `~/Downloads`, nicht ins Repo.**

```bash
mkdir -p /tmp/tb36_ergebnisse
cd ~/trading-bot

python3 research/faltenplan_neun/faltenplan_neun.py \
  > /tmp/tb36_ergebnisse/schritt3_faltenplan.txt 2>&1
python3 research/krypto_historie/faltenplan.py --mindesttraining 0 \
  > /tmp/tb36_ergebnisse/schritt4_gegenprobe.txt 2>&1
python3 research/faltenplan_neun/embargo_neun.py \
  > /tmp/tb36_ergebnisse/schritt5_embargo.txt 2>&1
python3 research/faltenplan_neun/test_faltenplan_neun.py \
  > /tmp/tb36_ergebnisse/schritt6_selbsttest.txt 2>&1
echo "Rueckgabewert Selbsttest: $?" >> /tmp/tb36_ergebnisse/schritt6_selbsttest.txt

cp /tmp/tb36_tests.txt /tmp/tb36_ergebnisse/schritt2_basislauf.txt
git diff origin/main --name-only > /tmp/tb36_ergebnisse/schritt8_dateien.txt
{
  python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; print(herkunft.datenstand())"
  git status --short
  git log --oneline -1
} > /tmp/tb36_ergebnisse/schritt9_datenstand.txt

cd /tmp && zip -r ~/Downloads/TESTLAUF_TB-36_registernachtrag.zip tb36_ergebnisse
ls -la ~/Downloads/TESTLAUF_TB-36_registernachtrag.zip
```

**Erwartet:** `~/Downloads/TESTLAUF_TB-36_registernachtrag.zip` mit acht
Textdateien. **Diese Datei ist das Ergebnis des Testauftrags** — sie gehört
nicht ins Repo und wird nicht committet.

---

## Kurzprotokoll zum Ausfüllen

| # | Prüfung | Erwartet | Gesehen |
|---|---|---|---|
| 1 | Datenstand vorher | `d9449faf…`, 223 Dateien | |
| 2 | Basislauf | keine neue rote Datei | |
| 3 | Faltenplan | 8 × 7 Falten, `elliott_wave` 3 | |
| 3 | Symbole Krypto / Aktien | 6/9/13/13/13/17/18 · 140/142/145/147/148/148/149 | |
| 4 | Gegenprobe gegen TB-31 | gleiche Zahlen | |
| 5 | Embargo | 11 / 13 / 11 / 11 / 16 / 91 / 11 / 11 / 16 | |
| 6 | Selbsttest | 145/145, Rückgabewert 0 | |
| 7 | Registernachtrag | 15.0–15.9, 0 entfernte Zeilen | |
| 8 | geänderte Dateien | genau 10, keine unter `data/` | |
| 9 | Datenstand nachher | unverändert, `git status` leer | |
| 10 | ZIP in `~/Downloads` | vorhanden | |

---

## In einfacher Sprache

**Was wir wissen wollten.** Ob die Zahlen, die jetzt im Register stehen, auf
deinem Rechner genauso herauskommen wie in der Cloud — und ob dabei wirklich
nichts angefasst wurde, was nicht angefasst werden darf.

**Was herauskam.** Das weisst du nach dem Durchlauf. Erwartet wird: zehn
Schritte, alle grün, ein ZIP in `~/Downloads`. Die wichtigste Zahl ist der
Datenstand in Schritt 1 und Schritt 9 — sie muss **beide Male gleich** sein.

**Warum das so ist.** Die Werkzeuge lesen nur; sie schreiben nur dorthin, wo du
es ihnen mit `--json` ausdrücklich sagst. Zwei Prüfungen verändern absichtlich
etwas, aber in einer Wegwerf-Kopie ausserhalb des Projekts — sie sollen zeigen,
dass eine falsche Zahl auch wirklich auffällt. Wäre eine Regel nur Zierde,
bliebe die Prüfung grün, obwohl sie rot werden müsste; genau das suchen diese
vier Proben.

**Was das für dich heisst.** Wenn alle zehn Schritte so ausgehen wie
beschrieben, ist der Registereintrag belastbar und die nächste Aufgabe (TB-30b)
kann darauf aufsetzen. Wenn irgendein Schritt abweicht: **nicht selbst
korrigieren** — Ausgabe sichern und melden. Eine abweichende Zahl ist hier
wertvoller als eine passende, denn sie zeigt, dass die Prüfung funktioniert.
