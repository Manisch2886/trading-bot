# TESTAUFTRAG TB-42 — Sichtbarkeit und Multiplikator

**Für den Mac des Betreibers. Autonom ausführbar: von oben nach unten
abarbeiten, nichts dazwischen entscheiden.**
Am Ende entsteht **ein ZIP in `~/Downloads`** — *nicht* im Repo.

| | |
|---|---|
| **Was geprüft wird** | Teil 1: jeder der neun Bots meldet jedes ausgelassene Symbol · Teil 2: der Quartals-Multiplikator wirkt nur auf die Positionsgrösse |
| **Dauer** | ca. 25–50 Minuten, das meiste davon Abschnitt 5 |
| **Netz nötig?** | **Nein.** Alle Prüfungen laufen gegen erzeugte Beispieldaten |
| **Wird etwas verändert?** | **Nein.** Keine Kursdatei, keine Bot-Datenbank, keine Order. Abschnitt 6 weist das nach |

> ⚠️ **Der Cloud-Lauf hat Binance und yfinance gesperrt vorgefunden (403).**
> Auf dem Mac ist Netz da. Das ändert an keiner Prüfung etwas — sie kommen
> alle ohne aus —, kann aber einzelne Bestandstests grüner machen als in der
> Cloud (siehe Abschnitt 4).

---

## 0. Vorbereitung

```bash
cd ~/trading-bot            # oder wo das Repo liegt
git fetch origin
git checkout claude/new-session-e3ey7f
git pull origin claude/new-session-e3ey7f

mkdir -p ~/Downloads/TB-42_sichtbarkeit
BERICHT=~/Downloads/TB-42_sichtbarkeit
python3 --version | tee $BERICHT/00_umgebung.txt
git log --oneline -3 | tee -a $BERICHT/00_umgebung.txt
```

> Läuft hier Python **3.9.6**? Gut — alle neuen Dateien sind darauf geprüft.
> `ib_async` wird **nicht** gebraucht; unter `broker/` wird nichts angefasst.

---

## 1. Der Datenstand vor der Prüfung

Er muss **vor und nach** dem ganzen Testauftrag derselbe sein. Das ist der
Nachweis, dass keine Prüfung eine Kursdatei angefasst hat.

```bash
python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; d = herkunft.datenstand()
print(d['datenstand'], d['dateien'], 'Dateien')
" | tee $BERICHT/01_datenstand_vorher.txt
```

**Erwartet:** `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`
und `223 Dateien`.

> Steht dort etwas anderes, ist der Kursdatenbestand seit der Aufgabenstellung
> gewachsen. Dann ist das **kein Fehler dieser Aufgabe** — notiere den neuen
> Wert und mach weiter; Abschnitt 6 vergleicht gegen *diesen* Stand.

---

## 2. Teil 1 — Ein Lauf, der ein Symbol auslässt, sagt es

```bash
python3 shared/test_ladeprotokoll.py 2>&1 | tee $BERICHT/02_teil1.txt
```

**Erwartet:** letzte Zeile `Alle N Pruefungen bestanden.` (N ≈ 180).

Was dort läuft — vier Blöcke, alle **am Verhalten**, keiner am Quelltext:

| Block | Was er zeigt |
|---|---|
| 1 | Der Melde-Baustein selbst: Zeilenform, Summenzeile, Wachposten |
| 2 | **Jeder der neun Bots** bekommt dieselben fünf Fälle hingehalten und muss jeden ausgelassenen melden — fehlende Datei, leere Datei, zu kurze Historie / zu wenige Kerzen |
| 3 | **Die geladene Symbolliste ist vor und nach TB-42 identisch.** Verglichen wird gegen den Loader, *wie Git ihn vor dieser Änderung führt* — nicht gegen eine Zahl in einem Dokument |
| 4 | Mutationsproben: wird eine Meldung aus einem Loader entfernt, **muss** Block 2 rot werden |

> Block 3 braucht die Git-Historie. Ist der Branch flach geklont (`--depth`),
> meldet der Test das offen als ungeprüft, statt still durchzuwinken.

### Und einmal mit eigenen Augen

```bash
python3 strategies/volatility_breakout/multi_symbol_optimise.py 2>&1 \
  | head -6 | tee $BERICHT/02b_vorher_lautlos.txt
```

**Erwartet** — genau die drei Zeilen, die dieser Bot bis TB-42 **verschwiegen**
hat, plus die neue Summenzeile:

```
Hinweis: GEV deckt nur 888 Tage ab (< 1825 noetig), wird uebersprungen.
Hinweis: SNDK deckt nur 565 Tage ab (< 1825 noetig), wird uebersprungen.
Hinweis: CEG deckt nur 1686 Tage ab (< 1825 noetig), wird uebersprungen.
Datenqualitaet: ...
Geladen: 147 von 150 Symbolen. 3 ausgelassen: 3x Historie zu kurz.
```

> Der volle Lauf rechnet danach noch das Optimierungsgitter durch und dauert
> lange. `head -6` schneidet ab — **das ist so gewollt**, ein `Broken pipe`
> darunter ist kein Fehler.

---

## 3. Teil 2 — Der Multiplikator, ohne die langen Läufe

```bash
python3 shared/test_groessenfaktor.py --nur 1,2,4 2>&1 \
  | tee $BERICHT/03_teil2_leseseite.txt
```

**Erwartet:** `Alle 63 Pruefungen bestanden.` (etwa eine halbe Minute)

Das prüft die Leseseite (fehlende, unlesbare, unvollständige Datei; eigener
Bot fehlt; keine Zahl; ausserhalb 0,25–4,0; `NaN`; `Infinity`), die neue
Datenbankspalte — und mit Mutationsproben, dass **jede Wache einzeln trägt**
und nicht eine zweite das Fehlen der ersten verdeckt.

---

## 4. Die bestehenden Tests

```bash
for f in shared/test_kursdaten.py shared/test_entscheidungskerze.py \
         notifications/test_manual_close.py shared/test_messkette.py \
         shared/test_live_params_werte.py shared/test_umstellungstag.py \
         shared/test_zuteilung.py dashboard/test_dashboard.py; do
  printf '%-45s ' "$f"
  if python3 "$f" > /tmp/tb42_$$.log 2>&1; then echo "OK"; else echo "ROT"; fi
done 2>&1 | tee $BERICHT/04_bestandstests.txt
```

**Erwartet: alle `OK`.** Drei davon mussten für TB-42 mitziehen und sind
deshalb besonders interessant:

| Test | Was daran neu ist |
|---|---|
| `notifications/test_manual_close.py` | spiegelt das Bot-Schema; die neue Spalte `groessenfaktor` gehört in den Nachbau. **Dieser Test hat die Änderung selbst gefunden** — genau dafür gibt es ihn |
| `shared/test_entscheidungskerze.py` | baut ein Miniatur-Repo aus echten `shared/`-Modulen; `groessenfaktor.py` gehört jetzt dazu |
| `shared/test_kursdaten.py` | verbot bisher **jede** Änderung an `forward_test.py`. Siehe Kasten unten |

> **Der Prüfer, der den Rückgriff bewacht.** `shared/test_kursdaten.py` sagte
> bisher „keine `forward_test.py` verändert“ — gegen `origin/main` geprüft. Die
> Freigabe vom 16.09.2026 macht diese Dateien zum ersten Mal überhaupt
> änderbar. Der Prüfer ist deshalb **präzisiert, nicht abgeschaltet**: er
> vergleicht jetzt, ob ein *Handelsparameter* sich ändert (Gebühr, Slippage,
> Lookback, Frischefenster) und ob der Satz der aus `live_params.py` geholten
> Namen derselbe bleibt. Dieselbe Entwicklung hat `live_params.py` in derselben
> Datei schon genommen. `equity_simulation.py` bleibt unverändert hart gesperrt.
>
> **Gegenprobe, dass der Prüfer noch beisst** (dauert eine Minute):
>
> ```bash
> cp strategies/t3_supertrend/forward_test.py /tmp/ft.bak
> sed -i '' 's/^TRADING_FEE_PCT = 0.1$/TRADING_FEE_PCT = 0.2/' \
>     strategies/t3_supertrend/forward_test.py
> python3 shared/test_kursdaten.py 2>&1 | grep -i "Handelsparameter veraendert" \
>     | tee $BERICHT/04b_gegenprobe.txt
> cp /tmp/ft.bak strategies/t3_supertrend/forward_test.py && rm /tmp/ft.bak
> git status --short strategies/   # MUSS wieder sauber sein
> ```
>
> **Erwartet:** eine Zeile mit `[FEHLER] ... TRADING_FEE_PCT: 0.1 -> 0.2`.
> Kommt sie nicht, ist der Prüfer taub — **das wäre ein Befund.**

> `shared/test_zuteilung.py` und `dashboard/test_dashboard.py` waren in der
> Cloud rot, weil dort das Netz bzw. Pakete fehlten. Auf dem Mac sollten sie
> `OK` melden. `shared/test_stabile_sortierung.py` und
> `shared/test_wellenauswahl.py` sind **unabhängig von TB-42** rot
> („`ergebniskurven.py` meldet 9x AKTUELL“) — nachgewiesen, indem sie ohne die
> TB-42-Änderungen genauso fehlschlagen. Sie stehen deshalb nicht in der Liste.

---

## 5. Der lange Lauf — der Multiplikator an allen neun Bots

**Das ist die Kernprüfung von Teil 2 und dauert am längsten (20–45 min).**

```bash
python3 shared/test_groessenfaktor.py --nur 3 2>&1 \
  | tee $BERICHT/05_teil2_neun_bots.txt
```

**Erwartet:** `Alle N Pruefungen bestanden.` (N ≈ 108)

Je Bot wird der **echte `forward_test.py` wirklich gestartet**, in einem
eigenen Prozess, gegen erzeugte Kursdaten, mit eigener Wegwerf-Datenbank — und
zwar fünfmal:

| Lauf | Erwartung |
|---|---|
| `m_b = 1,0` | erzeugt Trades (**sonst rot** — eine Prüfung ohne Trade wäre leer bestanden) |
| `m_b = 0,5` | **dieselben Ein- und Ausstiegszeitpunkte**, nur `groessenfaktor` verschieden |
| ohne Datei | läuft durch, es gilt 1,0, eine Protokollzeile |
| unlesbare Datei | läuft durch, 1,0 **und Warnung** |
| Wert 50 | wird **nicht** übernommen, 1,0 **und Warnung**, dieselben Trades |

> **Wenn Abschnitt 5 lange still ist:** das ist normal, der Test schreibt erst
> am Ende. Die vier Aktien-Bots legen je Lauf 150 Beispieldateien an.
>
> **Wenn ein Bot meldet „der Lauf erzeugt überhaupt keinen Trade":** dann hat
> keine der hinterlegten Datenformen bei ihm ein Signal ausgelöst. Der Test
> sucht selbst weiter, bevor er das sagt. Bleibt es dabei, ist das ein
> **Befund** (die Beispieldaten passen nicht mehr), **kein** Fehler am
> Multiplikator — bitte die Zeile mitschicken.

---

## 6. Der Datenstand danach — und dass nichts angefasst wurde

```bash
python3 -c "
import sys; sys.path.insert(0,'research/vorregistrierung')
import herkunft; d = herkunft.datenstand()
print(d['datenstand'], d['dateien'], 'Dateien')
" | tee $BERICHT/06_datenstand_nachher.txt

diff $BERICHT/01_datenstand_vorher.txt $BERICHT/06_datenstand_nachher.txt \
  && echo "DATENSTAND UNVERAENDERT" | tee -a $BERICHT/06_datenstand_nachher.txt

git status --short | tee $BERICHT/06b_arbeitsbaum.txt
ls -la *.db 2>/dev/null | tee $BERICHT/06c_datenbanken.txt
```

**Erwartet:**
* `DATENSTAND UNVERAENDERT`
* `git status --short` ist **leer** (Abschnitt 4b hat sein `cp` zurückgenommen)
* die echten `paper_trading_*.db` haben **dasselbe Änderungsdatum wie vorher** —
  kein Test schreibt in sie hinein

> ⚠️ Die Bots laufen per Cronjob. Ändert ein regulärer Cron-Lauf während des
> Testauftrags eine `.db`, ist das **normaler Betrieb**, kein Testbefund.
> Erkennbar an der Uhrzeit und daran, dass `git status` trotzdem leer bleibt
> (`*.db` ist gitignoriert).

---

## 7. Das ZIP für die Rückmeldung

```bash
cd ~/Downloads
zip -r TB-42_sichtbarkeit_ergebnisse.zip TB-42_sichtbarkeit/
ls -lh ~/Downloads/TB-42_sichtbarkeit_ergebnisse.zip
```

**Dieses ZIP liegt in `~/Downloads` und gehört ausdrücklich NICHT ins Repo.**
Es enthält die Protokolle aus den Abschnitten 0–6. Bitte zurückschicken —
zusammen mit der Antwort auf diese drei Fragen:

1. Hat Abschnitt 2 alle Prüfungen bestanden, **inklusive Block 3** (Symbolliste
   vor und nach TB-42 identisch) — oder wurde Block 3 als ungeprüft gemeldet?
2. Hat Abschnitt 5 bei **allen neun** Bots Trades erzeugt?
3. Hat die Gegenprobe in 4b den veränderten Gebührensatz gefunden?

---

## In einfacher Sprache

**Was wir wissen wollten.** Zwei Dinge. Erstens: Sagen die neun Handels-Bots
jetzt wirklich Bescheid, wenn sie eine Aktie oder eine Kryptowährung
weglassen? Drei von ihnen haben das früher stillschweigend getan. Zweitens:
Funktioniert die neue Stellschraube, mit der man später jedem Bot eine andere
Handelsgrösse geben kann — und zwar so, dass sie *nur* die Grösse ändert und
nichts anderes?

**Was herauskam.** Das sagt dieser Testauftrag noch nicht — er ist die
Anleitung, mit der du es auf deinem Rechner selbst nachprüfst. In der Cloud
haben alle Prüfungen bestanden.

**Warum das so ist.** Eine Prüfung, die nur der schreibt, der die Änderung
gebaut hat, ist wenig wert. Deshalb läuft hier nichts „auf Zuruf“: Jede
Prüfung startet den **echten** Bot-Code und schaut zu, was er tut — statt in
den Quelltext zu schauen und zu glauben, was dort steht. Und mehrere
Prüfungen sind absichtlich so gebaut, dass sie rot werden *müssen*, wenn man
die neue Meldung wieder herausnimmt. Ein Test, der immer grün ist, prüft
nämlich nichts.

**Was das für dich heisst.** Arbeite die Abschnitte 0 bis 7 der Reihe nach ab
— du musst nirgends etwas entscheiden, nur die Befehle ausführen. Es wird
dabei nichts an deinen Kursdaten, deinen Bot-Datenbanken oder deinem Geld
geändert; Abschnitt 6 rechnet dir das vor. Am Ende liegt eine ZIP-Datei in
deinem Download-Ordner. Schick sie zurück und beantworte die drei Fragen aus
Abschnitt 7. Rechne mit einer knappen Stunde, in der der Rechner meist allein
vor sich hin arbeitet.
