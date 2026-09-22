# Vorarbeit zur Sperrlisten-Sonde — was von den 14 Punkten überhaupt ein Hash ist

**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**Gemessen:** 22.09.2026, 07:55 Ortszeit · **HEAD:** `fdb181a`
**Art:** lesende Vorarbeit. ⛔ **Kein Byte geändert.**
**Zweck:** Fables Registertext (36.2) verlangt, die Sonde prüfe *„für **jeden**
Sperrlistenpunkt Pfad und Hash"*. ⚠️ **Gemessen: Das ist bei der Mehrzahl der
Punkte nicht möglich** — sie nennen keine prüfbare Datei allein.

---

## 1. Die 14 Punkte, klassifiziert nach dem, was eine Sonde daran messen kann

| # | Punkt | prüfbar als |
|---:|---|---|
| **1** | Rastergrenzen und Grenzsätze — `registerdaten.py` | ⭐ **Datei-Hash** |
| **2** | Faltengrenzen … — `faltenplan.py`, `ergebnisse/faltenplan.json` | ⭐ **zwei Datei-Hashes** |
| **3** | Selektionsstatistik, Plateau-Regel, Spitzen-Schwelle — `auswertung.py`, `registerdaten.SPITZEN_SCHWELLE` | ⚠️ Datei-Hash **+ Konstantenwert** |
| **4** | Drawdown-Bedingung … — `benchmark.py`, `ergebnisse/benchmark_drawdowns.json`, **einschliesslich der Interpolationsregel** | ⚠️ zwei Datei-Hashes **+ eine Regel im Text** |
| **5** | Abbruchkriterien und Kapitalregel — `auswertung.py` | ⭐ Datei-Hash *(dieselbe Datei wie 3)* |
| **6** | Benchmark-Definitionen — `benchmark.py::bh_tagesrenditen` | ⚠️ **eine Funktion**, nicht die Datei |
| **7** | N-Buchführung und Clusterschwelle — `registerdaten.N_HISTORISCH_JE_BOT`, `CLUSTER_SCHWELLE = 0,9` | ⚠️ **zwei Konstanten** |
| **8** | Universumsdateien — `config/top25_symbols.txt`, `config/sp500_top150.txt` | ⭐ **zwei Datei-Hashes** (im Nachtrag registriert) |
| **9** | Kosten und Fill-Konvention — `TRADING_FEE_PCT = 0,1`, `SLIPPAGE_PCT = 0,05` | ⚠️⚠️ **zwei Konstanten, keine Datei genannt** |
| **10** | Zuteilungskaskade — `shared/zuteilung.py`, `SEED = 20260913` | ⚠️ Datei-Hash **+ Konstante** |
| **11** | Commit-Hashes von Simulation, Erkennung, Optimierern — `herkunft.py::register()` **und der Repo-Commit** | ⚠️⚠️ **Funktion + eine Grösse ausserhalb des Repos** |
| **12** | Hash des Datenstands — `herkunft.py::datenstand()` | ⚠️ **Funktion** |
| **13** | Liste der berichteten Kennzahlen — **Abschnitt 8 dieses Registers** | ⛔⛔ **reiner Registertext, keine Datei** |
| **14** | Reihenfolge Selektion → Bestätigung → Bericht — **im Kopftext von `auswertung.py`** | ⚠️ **Docstring**, nicht die Datei als ganze |

### ⇒ Die Bilanz

| | Anzahl |
|---|---:|
| ⭐ Punkte, die **allein** über Datei-Hashes prüfbar sind | **1, 2, 5, 8** — vier |
| ⚠️ Punkte mit Datei **plus** Konstante oder Regel | **3, 4, 10** — drei |
| ⚠️ Punkte, die eine **Funktion** oder einen **Docstring** meinen | **6, 12, 14** — drei |
| ⚠️⚠️ Punkte **ohne** genannte Datei | **7, 9** — zwei |
| ⚠️⚠️ Punkt mit einer Grösse **ausserhalb** des Repos | **11** (Repo-Commit) |
| ⛔⛔ Punkt **ohne jede Datei** | **13** (Registertext) |

⭐ **Eindeutige Dateipfade insgesamt: sieben** — `registerdaten.py`,
`faltenplan.py`, `ergebnisse/faltenplan.json`, `auswertung.py`, `benchmark.py`,
`ergebnisse/benchmark_drawdowns.json`, `shared/zuteilung.py`, dazu die beiden
`config/*.txt` = **neun**.

---

## 2. ⚠️ Der dritte Sperrlisten-Hash steht gar nicht auf der Sperrliste

**Gemessen:** Das Projekt führt drei Hashes als „Sperrlisten-Hashes"
(Registerzeile 3907: *„Sperrlisten-Hashes (`a163c498…`, `4549395f…`,
`0e54ac5c…`)"*). Aber:

| Hash | Datei | in Abschnitt 10? |
|---|---|---|
| `a163c498…` | `ergebnisse/benchmark_drawdowns.json` | ⭐ **ja**, Punkt 4 |
| `0e54ac5c…` | `ergebnisse/faltenplan.json` | ⭐ **ja**, Punkt 2 |
| ⚠️ `4549395f…` | `ergebnisse/benchmark_drawdowns_vt.json` | ⚠️⚠️ **nein — kommt in keinem der 14 Punkte vor** |

**Der Grund, gemessen:** `_vt.json` liegt **neben** der gesperrten Datei und
soll deren Platz einnehmen, sobald die Sperrlisten-Änderung vollzogen ist
(Register 21.9, 23.7 — *„Die Sperrlisten-Änderung nicht vollzogen"*, Freigabe
steht aus, dazu die offene Entscheidung W/C aus 23.3).

⇒ ⭐ **Fables Schreibregel deckt den Fall bereits ab:** 36.1 (1) nennt Pfade,
*„die auf der Sperrliste stehen **oder für sie bestimmt sind**"*.
⚠️ **Seine Sonde nicht:** 36.2 sagt *„für jeden Sperrlistenpunkt"* — und
`_vt.json` ist kein Punkt.

---

## 3. Ein Folgebefund, der schon registriert ist

**Register 3560, wörtlich:** *„`registerbericht.py:178` liest den alten Schlüssel
aus der **gesperrten** Datei und läuft deshalb heute unverändert; **beim Vollzug
der Sperrlisten-Änderung ist er nachzuziehen**."*

⭐ Das ist bereits als offener Punkt geführt — hier nur genannt, damit die Sonde
ihn nicht als neuen Befund meldet.

---

## 4. Was daraus für TB-85 folgt — und was an Fable geht

| | |
|---|---|
| ⭐ **Baubar ohne Rückfrage** | Die neun Datei-Hashes (Punkte 1, 2, 4, 5, 8, 10 und 3 anteilig). Das ist der Kern der Sonde und deckt alle drei heute geführten Hashes ab |
| ⚠️ **Braucht eine Entscheidung** | Wie die Sonde mit den Punkten umgeht, die **keine** Datei sind (7, 9, 11, 13) und mit denen, die eine **Funktion oder einen Docstring** meinen (6, 12, 14) |
| ⚠️ **Dritte Frage an Fable** | Prüft die Sonde auch Pfade, die *„für die Sperrliste bestimmt"* sind (`_vt.json`)? Sein Schreibregel-Text kennt sie, sein Sonden-Text nicht |

⭐ **Vorschlag für TB-85, nicht vollzogen:** Die Sonde prüft, was sie prüfen
kann, und **meldet jeden Punkt, den sie nicht prüfen kann, mit Rückgabewert `2`
(NICHT PRÜFBAR)** — nach dem Muster aus `shared/snapshot.py` und nach `A2`.
⇒ Dann braucht sie **keine** der drei Entscheidungen vorab: Sie sagt selbst, wo
der Registertext ihr nichts Messbares gibt. ⚠️ **Das ist ein Vorschlag an Fable,
keine Wahl von uns.**

---

## In einfacher Sprache

Fable hat ein Prüfprogramm angeordnet, das **alle 14 geschützten Punkte** gegen
ihre Prüfsummen kontrolliert. **Gemessen: Nur vier davon sind reine Dateien.**

Die anderen nennen einzelne Zahlen in Dateien, einzelne Funktionen, einen
Kommentartext — und einer, Punkt 13, verweist nur auf einen Abschnitt des
Regelwerks selbst, also auf gar keine Datei. Zwei Punkte nennen überhaupt keine
Datei, nur Zahlenwerte.

**Und eine Merkwürdigkeit:** Das Projekt führt drei Prüfsummen als „geschützt" —
aber **eine davon gehört zu einer Datei, die auf der Liste gar nicht steht**. Sie
liegt dort bereit, um später den Platz einer anderen einzunehmen; der Wechsel ist
seit Tagen nicht vollzogen.

⭐ **Der Ausweg, den wir vorschlagen (aber nicht entscheiden):** Das Prüfprogramm
prüft, was prüfbar ist — und sagt bei jedem Punkt, den es nicht prüfen kann,
ausdrücklich **„nicht prüfbar"** statt „in Ordnung". Dann muss vorher niemand
entscheiden, was mit den schwierigen Punkten geschieht; das Programm zeigt es.
