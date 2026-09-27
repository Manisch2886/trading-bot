# Wochenrückmeldung 19.09.2026 — an: Fable 5.1, bestehender Chat

**Drei Meldungen, eine Frage.** Die Frage betrifft deine Schicht 3.

---

## 1. ⭐⭐ Der Snapshot ist gezogen — und registriert

**Deine Empfehlung vom 18.09. („jetzt ziehen, nicht erst am Tag") wurde
befolgt.** Meine Auslegung von F1a war zu streng; bindend ist *„ein zweiter
Snapshot ist ein neuer Lauf"* — also **nur einmal**, nicht **nicht vorher**.

```
snapshot_hash   63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
datenstand      d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84  (223)
gezogen         2026-09-19T06:49:32+00:00     225 Dateien, 211 040 678 Bytes
versioniert     Commit 1075dec auf main
registriert     VORREGISTRIERUNG_neuselektion.md, Abschnitt 18 (Tatsachennotiz zu 5 / 5a)
```

**36 Befunde zugelassen, sämtlich `rand_erste`, nach Abschnitt 17.3;
`nicht_zugelassen` leer.** Nachprüfung `UNVERAENDERT`.

### Fünf voneinander unabhängige Belege

| # | |
|---|---|
| 1 | Jede der 225 Dateien **byteweise** beim Kopieren gegen die Quelle geprüft |
| 2 | `--pruefen` danach: `UNVERAENDERT`, beide Hashes Soll = Ist |
| 3 | ⭐⭐ **Beim Einchecken legte git für keine der 225 Dateien einen neuen Blob an** — 1 Commit, 4 Trees, 1 Blob, und der eine Blob ist das Manifest. *git adressiert über den Inhalt; es bezeugt die Gleichheit mit `data/`, ohne unser Werkzeug zu kennen* |
| 4 | Der Registerprüfer lief in einem Worktree auf dem Vorgänger-Commit und mass dort denselben Datenstand — **der versionierte Inhalt ist gleich dem Arbeitsbaum** |
| 5 | ⭐ **Der Name ist fünfmal unabhängig gerechnet:** TB-49 Cloud (echter Zug, Python 3.11) · TB-49 Mac (3.9.6) · TB-55 Cloud (3.11.15) · TB-55 Mac (3.9.6, der Zug) · **frischer Klon auf einer dritten Umgebung (3.11.15), gerechnet gegen den committeten Snapshot** |

⭐ **Beleg 5 ist zugleich F1b/Q2:** Der Snapshot wurde aus dem Repo auf eine
zweite Maschine geholt und dort nachgerechnet. **Die Reproduktion ist belegt,
und zwar vor dem Tag.**

⚠️ **Deine Bedingung gilt weiter und ist erfüllt:** Der Datencron läuft nicht
(T46.4), und der Prüfer rechnet nicht gegen `data/`.

---

## 2. ⭐ Deine Schicht 2 ist fertig — und der Engpass war enger als gedacht

**Gemessen, rein lesend:**

```
90 Selektionsmodule  (rolle == "Selektion/Backtest")
 ├─ 71  →  get_strategy_paths()            direkt
 └─ 19  →  multi_symbol_optimise  →  get_strategy_paths()
                                          ↓
                          shared/strategy_paths.py
```

| | |
|---|---|
| Module mit **eigenem** `data`-Pfad | ⭐ **0 von 90** |
| Module, die `get_strategy_paths()` nicht erreichen | ⭐ **0 von 90** |

⭐⭐ **Und die Sperrliste blieb unberührt:** Alle neun
`multi_symbol_optimise.py` nehmen `DATA_DIR = _P["DATA_DIR"]` — **sie bauen
keinen Pfad, sie bekommen einen.**

**`get_strategy_paths()` fragt jetzt `shared/paths.py`**, statt den Resolver ein
zweites Mal umzusetzen. Gemessen: 63 Pfade ohne Modus zeichengleich wie vorher ·
9/9 unter dem Modus in der Snapshot-Wurzel · falscher Hash **wirft** (9/9, rc 1) ·
`LIVE_DATA_DIR` wirft · beide AST-Sperrklinken unverändert (6 / 29) · Basislauf
**UNERWARTET 0** · 23 neue Proben, gegen die alte Fassung **14 rot**.

---

## 3. ⚠️⚠️ Die Frage — und sie betrifft Schicht 3

**Die beiden Dateien bestimmen ihre Wurzel verschieden:**
`paths.py` aus **seiner eigenen** Lage, `get_strategy_paths()` aus der Lage des
**Aufrufers**. Wir wollten die Gleichheit im Quelltext **zusichern**.

⚠️ **Die wörtliche Zusicherung machte vier grüne Tests rot** — und zwar nicht
wegen eines Fehlers, sondern wegen eines **bewussten Musters** dieses Projekts:

> `test_determinismus`, `test_ladeprotokoll` und `test_wellenauswahl` laden eine
> **Bot-Kopie aus einem Wegwerfbaum** und benutzen dabei die **echte `shared/`** —
> Ergebnisse und Datenbank in der Kopie, Kursdaten aus dem Projekt.
> **Die Zusicherung verbietet genau das.**

**Gewählt wurde stattdessen:**

| | |
|---|---|
| **Im Quelltext zugesichert** | dass das antwortende `paths.py` **physisch neben** `strategy_paths.py` liegt (`realpath`), sonst Fehler. ⭐ *Das schützt gegen ein fremdes `paths` auf `sys.path`, das sonst **still** einen Pfad aus einem anderen Baum liefert — mit Mutationsprobe belegt* |
| ⚠️ **Nur gemessen, nicht zugesichert** | dass der **Aufrufer** im selben Baum liegt. Das prüft eine Probe **bei jedem Testlauf**, nicht der Quelltext |

### Konkret gefragt

**(a)** Genügt für Schicht 3 eine **Messung bei jedem Lauf**, wo wir eine
**Zusicherung im Quelltext** wollten — oder muss die Lücke im Code geschlossen
werden?

**(b)** Falls im Code: **wie**, ohne das Wegwerfbaum-Muster zu verbieten?

**(c)** ⭐ **Die Frage dahinter, und sie ist uns erst beim Messen aufgefallen:**
Darf ein **Selektionslauf** überhaupt je mit Aufrufer und Resolver in
verschiedenen Bäumen laufen? Wenn nein, ist die Zusicherung genau für den
Selektionsmodus richtig und nur im Regelbetrieb falsch — **dann wäre sie an den
Modus zu koppeln statt ganz aufzugeben.** Wenn ja: **welche Wurzel gewinnt?**

---

## 4. Vier Regeln, die die Woche hervorgebracht hat

| | |
|---|---|
| **A7** | *Eine nachgeholte Vorher-Messung ist nur dann eine, wenn der Zustand **inhaltsadressiert** wiederherstellbar ist — und sie muss sagen, dass sie nachgeholt wurde* |
| **Stellvertreter** | *Ein Abbruchkriterium benennt die Sache, nie ihren Stellvertreter.* Unser „gibt es dort schon eine Zahl?" meinte „gibt es dort schon **diesen** Snapshot?" — und traf eine andere, richtige Zahl |
| **Fragen statt entscheiden** | *Fallen Wortlaut und Zweck eines Abbruchkriteriums auseinander und ist ein Mensch erreichbar — fragen.* ⭐ **Zweimal angewandt, beide Male zu Recht** |
| **Keine geratenen Nummern** | *Ein Nachtrag nennt keine Nummer, die er nicht selbst gemessen hat* — nach drei Nummernkollisionen an einem Tag |

---

## Was wir nicht von dir brauchen

⚠️ **Keine Prüfung des Registers als Ganzes.** Die steht weiterhin zwischen dem
Auswerter-Umbau und dem signierten Tag.

**Nur die Frage aus Abschnitt 3.**

---

## Der Stand, damit du nicht nachfragen musst

| | |
|---|---|
| **Snapshot** | gezogen, registriert, reproduziert |
| **Resolver** | Schicht 1 (TB-52) und Schicht 2 (TB-53b) im Repo. ⚠️ **Schicht 3, das Lese-Audit: offen** |
| **Offen vor dem Tag** | Lese-Audit · Faltenschranke `ERSTE_MOEGLICHE_FALTE = 2019` entfernen + Berichtigung 17.3 + Drei-Kategorien-Regel ins Register · `auswertung.py` auf Verfahren B · deine Querprüfung Q1 |
| **Datenstand** | `d9449faf…`, 223 — unverändert seit 15.09., heute elfmal gemessen |
