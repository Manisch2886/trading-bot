# Testauftrag TB-39 — S-B1 Vorbereitung (Datenlauf und Messung)

**Autonom ausführbar.** Jeder Schritt nennt den Befehl, das erwartete Ergebnis
und was zu tun ist, wenn es abweicht.

**Alle Befehle sind einzeilig.** Termius auf dem iPhone verliert
Zeilenumbrüche in Heredocs und Python-Blöcken — hier kommt keiner vor.

---

> # ⚠️ DIE EINE REGEL: `data/` WIRD NICHT ANGEFASST
>
> Der Datenstand-Hash der Vorregistrierung ist der SHA-256 über die Dateien
> in `data/`: `d9449faf51bffaaa…` bei **223** Dateien. **Eine einzige
> zusätzliche Datei dort ändert ihn** und entwertet den registrierten
> Zustand, bevor der Selektionslauf stattgefunden hat.
>
> Schritt 2 und Schritt 9 messen den Hash — **vorher und nachher**. Sie
> müssen dieselbe Zeichenkette und dieselbe Dateizahl liefern. Tun sie das
> nicht, ist das der wichtigste Befund dieses Testauftrags, und alles andere
> wartet.
>
> **Kein Schritt dieser Anleitung schreibt nach `data/`.** Die ETF-Kursdaten
> gehen nach `research/etf_trendfolge/daten/` — ein gitignorierter Ordner.

> # ⚠️ DIE ZWEITE REGEL: NICHTS WIRD GERECHNET
>
> Dieser Testauftrag holt Daten und **misst**, wie weit sie zurückreichen. Er
> rechnet **keinen Backtest**, keinen Ertrag und keine Sharpe-Zahl. Kommt
> irgendwo eine Ertragszahl heraus, ist das ein **Befund**, kein Ergebnis.

---

## Was gebraucht wird

* Zugang zum MacBook mit dem Repo unter `~/trading-bot`
* `python3`, `pandas`, `yfinance` (aus `requirements.txt`)
* Netz zu Yahoo für Schritt 4 — alles andere ist offline
* Rund 15 Minuten, davon die meiste Zeit der Datenabruf

**Ergebnis-Ordner anlegen, dorthin kommen alle Protokolle:**

```bash
mkdir -p ~/Downloads/TB-39_sb1_vorbereitung
```

---

## Schritt 1 — Auf den Stand kommen

```bash
cd ~/trading-bot && git fetch origin && git status --porcelain | tee ~/Downloads/TB-39_sb1_vorbereitung/01_status.txt
```

**Erwartet:** leere Ausgabe (sauberer Arbeitsbaum).

**Nicht leer?** Erst klären, was geändert ist. Ein Lauf auf einem schmutzigen
Baum ist nicht reproduzierbar — und genau das steht dann auch im
Herkunftsblock.

```bash
cd ~/trading-bot && git checkout claude/new-session-s2jhcc && git pull origin claude/new-session-s2jhcc | tail -3
```

---

## Schritt 2 — Der Datenstand VORHER (die wichtigste Zahl dieses Auftrags)

```bash
cd ~/trading-bot && python3 research/etf_trendfolge/datenstand.py --json ~/Downloads/TB-39_sb1_vorbereitung/02_datenstand_vorher.json | tee ~/Downloads/TB-39_sb1_vorbereitung/02_datenstand_vorher.txt
```

**Erwartet, wörtlich:**

```
  Ist    d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84  (223 Dateien)
  Soll   d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84  (223 Dateien)
  unveraendert
```

und darunter

```
  liegt ausserhalb von data/ - richtig so.
```

**Rückgabewert prüfen:**

```bash
cd ~/trading-bot && python3 research/etf_trendfolge/datenstand.py > /dev/null; echo "Rueckgabewert: $?"
```

**Erwartet:** `Rueckgabewert: 0`.

**Weicht der Hash schon hier ab?** Dann hat etwas anderes `data/` verändert,
nicht dieser Auftrag. **Nicht weitermachen** — das ist ein eigener Befund und
betrifft die Neuselektion, nicht `S-B1`.

---

## Schritt 3 — Der Selbsttest, bevor Daten da sind

```bash
cd ~/trading-bot && python3 research/etf_trendfolge/test_etf_trendfolge.py | tee ~/Downloads/TB-39_sb1_vorbereitung/03_selbsttest.txt
```

**Erwartet:** `64/64 Pruefungen bestanden.`

**Weniger?** Die gescheiterten Zeilen stehen namentlich am Ende. Nicht
weitermachen — ein Werkzeug, das seinen Test nicht besteht, misst nichts.

*Dieser Schritt läuft **vor** dem Datenabruf. Das ist Absicht: das
Auswertungswerkzeug soll seinen Test bestanden haben, als es noch nichts zu
deuten gab.*

---

## Schritt 4 — Der Datenlauf (der einzige Schritt, der ins Netz geht)

```bash
cd ~/trading-bot && python3 research/etf_trendfolge/datenlauf.py | tee ~/Downloads/TB-39_sb1_vorbereitung/04_datenlauf.txt
```

**Erwartet:** vierzehn Zeilen der Form

```
  SPY     8400 Handelstage  (0 unvollstaendig, 1 nach der Entscheidungskerze verworfen)
```

und am Ende `Manifest: .../daten/manifest.json`.

**Worauf zu achten ist:**

| | |
|---|---|
| **„nach der Entscheidungskerze verworfen" ist 0 oder 1** | 1, wenn der Lauf während der US-Handelszeit stattfindet (die laufende Tageskerze wird verworfen — genau so soll es sein). 0, wenn ausserhalb. **Eine grössere Zahl ist ein Befund** |
| **„Hinweis: Der Boersenkalender…"** | Erscheint das, fehlt `pandas_market_calendars`. Dann fällt die Regel auf die sichere Schranke zurück und verwirft **mehr** als nötig — ärgerlich, aber nicht falsch. Abhilfe: `pip3 install -r requirements.txt` |
| **„yfinance liefert nichts"** | Netz prüfen. Bleibt es dabei für ein bestimmtes Symbol, ist das ein Befund: das Symbol gibt es nicht mehr, und dann ist die Kandidatenliste zu ändern — **vom Betreiber, nicht von der Anleitung** |

**Der Lauf überschreibt nichts.** Liegen Dateien schon da, sagt er das und
lässt sie in Ruhe. Das ist Absicht (siehe Register, Abschnitt 3.2).

---

## Schritt 5 — Die Antwort auf die harte Frage

```bash
cd ~/trading-bot && python3 research/etf_trendfolge/historie.py --json ~/Downloads/TB-39_sb1_vorbereitung/05_historie.json | tee ~/Downloads/TB-39_sb1_vorbereitung/05_historie.txt
```

**Das ist der Schritt, um dessentwillen der ganze Auftrag existiert.** Er
beantwortet: **Reicht die Historie ab 2007 für acht Instrumente über vier
Anlageklassen?**

**Erwartet:** eine Tabelle mit vierzehn Zeilen, dann

```
  Untergrenze am 2008-01-01:
    Instrumente    NN von 8 verlangt   erfuellt
    Anlageklassen   N von 4 verlangt   erfuellt
```

**Rückgabewert prüfen — er ist die Antwort:**

```bash
cd ~/trading-bot && python3 research/etf_trendfolge/historie.py > /dev/null; echo "Rueckgabewert: $?"
```

| Rückgabewert | heisst |
|---|---|
| **0** | Die Untergrenze ist erfüllt. `S-B1` ist baubar |
| **1** | Sie ist **nicht** erfüllt. ⚠️ **Das ist ein Befund, kein Fehler.** Die Ausgabe nennt getrennt, welche der beiden Bedingungen gefallen ist. Ob stattdessen ein späterer Start oder ein Verzicht auf eine Anlageklasse richtig ist, **entscheidet der Betreiber** — nicht diese Anleitung und nicht das Werkzeug |

**Ausserdem zu notieren:**

* **Abweichungen zur Erwartung.** Erscheint ein Block „Abweichungen zur
  Erwartung", stimmt ein gemessenes Auflagedatum nicht mit dem im Register
  vermerkten überein. **Die Messung gilt.** Die Zeile gehört in den Bericht —
  sie ist entweder eine korrigierte Erwartung oder ein falsch geschriebenes
  Symbol, und das ist zweierlei.
* **Die Jahrestabelle am Ende.** Sie sagt, wie viele Selektionsfalten die
  Untergrenze tragen. Weniger als **3** löst Abbruchkriterium (b) aus.

---

## Schritt 6 — Das Raster und N

```bash
cd ~/trading-bot && python3 research/etf_trendfolge/raster.py --was-waere-wenn --json ~/Downloads/TB-39_sb1_vorbereitung/06_raster.json | tee ~/Downloads/TB-39_sb1_vorbereitung/06_raster.txt
```

**Erwartet:**

```
  N                  5
  N_historisch       653  (Neuselektion, Vorregistrierung Abschnitt 9)
  N gesamt, nominal  658
```

**Braucht keine Daten.** Läuft auch, wenn Schritt 4 übersprungen wurde.

---

## Schritt 7 — Die Kostenrechnung

```bash
cd ~/trading-bot && python3 research/etf_trendfolge/kosten.py --json ~/Downloads/TB-39_sb1_vorbereitung/07_kosten.json | tee ~/Downloads/TB-39_sb1_vorbereitung/07_kosten.txt
```

**Erwartet:** die Tabelle über Kipprate und Drift, darunter

```
  Obere Schranke (jeden Monat kippt alles): 1.80 Prozentpunkte je Jahr
  Massstab, ein VOLLER Round Trip je Monat:  3.60 Prozentpunkte je Jahr
```

**Braucht keine Daten.** Die Kostenlast folgt aus der Bauart der Strategie,
nicht aus den Kursen.

---

## Schritt 8 — Der Selbsttest noch einmal, jetzt MIT Daten

```bash
cd ~/trading-bot && python3 research/etf_trendfolge/test_etf_trendfolge.py | tee ~/Downloads/TB-39_sb1_vorbereitung/08_selbsttest_nachher.txt
```

**Erwartet:** wieder `64/64 Pruefungen bestanden.`

*Der Test läuft auf eigenen Wegwerf-Ordnern und darf sich durch die echten
Kursdateien nicht ändern. Ändert er sich, liest er etwas, das er nicht lesen
sollte — und das wäre ein Befund.*

---

## Schritt 9 — Der Datenstand NACHHER (die Gegenprobe zu Schritt 2)

```bash
cd ~/trading-bot && python3 research/etf_trendfolge/datenstand.py --json ~/Downloads/TB-39_sb1_vorbereitung/09_datenstand_nachher.json | tee ~/Downloads/TB-39_sb1_vorbereitung/09_datenstand_nachher.txt
```

**Erwartet:** **exakt** dieselbe Zeichenkette und dieselbe Dateizahl wie in
Schritt 2.

**Der maschinelle Vergleich:**

```bash
cd ~/trading-bot && diff <(grep Ist ~/Downloads/TB-39_sb1_vorbereitung/02_datenstand_vorher.txt) <(grep Ist ~/Downloads/TB-39_sb1_vorbereitung/09_datenstand_nachher.txt) && echo "IDENTISCH" || echo "ABWEICHUNG - BEFUND"
```

**Erwartet:** `IDENTISCH`.

**Und die zweite Gegenprobe — hat `git` etwas in `data/` gesehen?**

```bash
cd ~/trading-bot && git status --porcelain data/ | tee ~/Downloads/TB-39_sb1_vorbereitung/09_git_data.txt && echo "(leer = gut)"
```

**Erwartet:** leere Ausgabe.

---

## Schritt 10 — Prüfen, dass nichts Fremdes berührt wurde

```bash
cd ~/trading-bot && git status --porcelain | tee ~/Downloads/TB-39_sb1_vorbereitung/10_status_nachher.txt && echo "(leer = gut)"
```

**Erwartet:** leer. Die ETF-Kursdateien sind gitignoriert und tauchen hier
**nicht** auf — genau deshalb liegen sie dort.

```bash
cd ~/trading-bot && ls research/etf_trendfolge/daten/ | wc -l | tee ~/Downloads/TB-39_sb1_vorbereitung/10_dateizahl.txt
```

**Erwartet:** `15` (vierzehn Kursdateien plus `manifest.json`).

---

## Schritt 11 — Die bestehenden Tests

```bash
cd ~/trading-bot && python3 shared/test_entscheidungskerze.py 2>&1 | tail -3 | tee ~/Downloads/TB-39_sb1_vorbereitung/11_entscheidungskerze.txt
```

**Erwartet:** bestanden.

```bash
cd ~/trading-bot && python3 research/vorregistrierung/test_vorregistrierung.py 2>&1 | tail -3 | tee ~/Downloads/TB-39_sb1_vorbereitung/11_vorregistrierung.txt
```

**Erwartet:** bestanden. *Dieser Test liest denselben Datenstand-Hash — er
ist die unabhängige Gegenprobe zu Schritt 9.*

**Bekannt rot und TB-39-fremd** (nicht auf diesen Auftrag zurückzuführen):
`shared/test_drawdown_beide_masse.py` (Zeitüberschreitung),
`shared/test_kursdaten.py`, `shared/test_stabile_sortierung.py`,
`shared/test_wellenauswahl.py`, `dashboard/test_portfolio_sicht.py`,
`research/exposure_messung/test_exposure_kern.py`. Ohne `node` meldet
`dashboard/test_dashboard.py` 780/780 statt 784.

---

## Schritt 12 — Die Ergebnisse einpacken

```bash
cd ~/Downloads && zip -r TB-39_sb1_vorbereitung_ergebnisse.zip TB-39_sb1_vorbereitung > /dev/null && ls -lh TB-39_sb1_vorbereitung_ergebnisse.zip
```

⚠️ **Die ZIP-Datei liegt in `~/Downloads`, NICHT im Repo.** Sie enthält
Protokolle eines Laufs; sie gehört zum Zurückschicken, nicht zum Einchecken.

**Die Kursdateien gehören NICHT in die ZIP.** Sie sind gross, sie ändern sich
bei jeder Ausschüttung, und ihr Stand steht als Hash im `manifest.json`, das
mit drin ist. Wer sie trotzdem braucht:

```bash
cd ~/trading-bot && zip -r ~/Downloads/TB-39_sb1_kursdaten.zip research/etf_trendfolge/daten > /dev/null && ls -lh ~/Downloads/TB-39_sb1_kursdaten.zip
```

---

## Die Ergebnistabelle zum Ausfüllen

| # | Prüfung | erwartet | beobachtet |
|---|---|---|---|
| 1 | Arbeitsbaum sauber | leer | |
| 2 | **Datenstand vorher** | `d9449faf…` / 223 Dateien | |
| 3 | Selbsttest vorher | 64/64 | |
| 4 | Datenlauf | 14 Dateien | |
| 5 | **Erstes Datum je ETF** | 14 Zeilen, gemessen | |
| 5a | **Untergrenze am 2008-01-01** | erfüllt / nicht erfüllt | |
| 5b | **Rückgabewert `historie.py`** | 0 oder 1 (beides zulässig) | |
| 5c | Tragende Selektionsfalten | ≥ 3 | |
| 5d | Abweichungen zur Erwartung | Liste (darf leer sein) | |
| 6 | N | 5 | |
| 7 | Obere Kostenschranke | 1,80 pp/Jahr | |
| 8 | Selbsttest nachher | 64/64 | |
| 9 | **Datenstand nachher** | `IDENTISCH` | |
| 9a | `git status data/` | leer | |
| 10 | `git status` gesamt | leer | |
| 10a | Dateien in `daten/` | 15 | |
| 11 | Bestehende Tests | bestanden | |

---

## In einfacher Sprache

**Was wir wissen wollten.**
Zwei Dinge. Erstens: **Reichen die Kursdaten der vierzehn Wertpapierkörbe weit
genug zurück?** Sie müssen bis 2007 reichen, damit die Finanzkrise von 2008
mit dabei ist — eine Strategie, die Trends folgt, muss einmal einen echten
Crash gesehen haben, sonst weiss man nichts über sie. Zweitens: **Bleibt der
Kursdaten-Ordner des Projekts dabei unangetastet?**

**Was herauskam.**
Das steht nach dem Durchlauf in der Tabelle darüber. Zwei Zeilen sind die
wichtigsten:

* **Zeile 5a** — die eigentliche Antwort. Mindestens **acht** Körbe aus
  mindestens **vier** verschiedenen Bereichen (Aktien, Anleihen, Gold,
  Rohstoffe, Währungen, Kredit) müssen ab Anfang 2008 verfügbar sein.
* **Zeile 9** — muss `IDENTISCH` heissen. Der gespeicherte Kursordner des
  Projekts trägt eine Prüfsumme, die den Zustand zum Zeitpunkt der
  Strategie-Auswahl bezeugt. Wenn die sich ändert, ist dieser Nachweis
  wertlos.

**Warum das so ist.**
Wertpapierkörbe („ETFs") gibt es erst seit den 1990er Jahren, viele erst seit
2005 oder später. Dazu kommt: bevor die Strategie überhaupt ein Signal
erzeugen kann, braucht sie **zwölf Monate** Vorlauf — sie vergleicht ja den
heutigen Kurs mit dem von vor einem Jahr. Ein Korb, den es seit Januar 2007
gibt, liefert also erst ab Januar 2008 ein Signal. Deshalb lautet die
Anforderung auf 2007 und nicht auf 2008.

**Was das für dich heisst.**
Die Schritte der Reihe nach abarbeiten. Es wird **nichts** verändert, was mit
deinen laufenden Programmen zu tun hat — keine Datenbank, keine Einstellung,
kein Zeitplan. Der einzige Schritt, der ins Internet geht, ist Schritt 4.

**Und wenn Schritt 5 „Rückgabewert 1" meldet, ist nichts kaputt.** Dann heisst
es nur: die Kursdaten reichen nicht weit genug für acht Körbe aus vier
Bereichen. Das ist ein Ergebnis, kein Fehler — und dann entscheidest **du**,
ob später angefangen wird oder ob ein Bereich wegfällt. Die Anleitung
entscheidet das ausdrücklich nicht.

Am Ende (Schritt 12) entsteht eine ZIP-Datei in `~/Downloads`, die alle
Protokolle enthält. Die gehört **nicht** ins Repo, sondern nur zum
Zurückschicken.
