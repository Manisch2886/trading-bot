# Übergabe TB-44 — Die Wache auf beiden Pythons

**Sitzung:** Cloud-Claude-Code, `TB-44 Wache auf beiden Pythons`, 16.09.2026.
**Zweig:** `claude/new-session-tkwj4j`, aufgesetzt auf dem TB-43-Zweig
`claude/new-session-lwi4bi` (Commit `9f3952f` geprüft und enthalten).
**Pull Request gegen `main`** — ⚠️ **er enthält TB-43 und TB-44 zusammen**,
weil TB-43 nicht gemergt ist.

---

## Die drei Fragen aus der Aufgabe, zuerst

### 1. Hält die Reparatur den Schutz vollständig?

**Ja — und sie schliesst mehr, als gemeldet war.**

Der Schutz ist nach der Reparatur in **beiden** Import-Reihenfolgen und auf
**allen fünf** geprüften Python-Fassungen dicht: lesend geht durch, schreibend
wird abgefangen, Zeichengeräte bleiben ausgenommen, erlaubte Pfade bleiben
beschreibbar, und am **Dateibestand** ist nachgewiesen, dass nichts entstanden
und nichts verschwunden ist. Alle sieben Aufrufwege aus TB-43 bleiben
abgefangen (Teil K, unverändert 13/13).

⚠️ **Der vorliegende Patchvorschlag hätte das nicht geleistet**, und das ist
kein Ermessen, sondern gemessen:

* Er repariert auf 3.9 **nur das Lesen**. Die andere Reihenfolge — `pathlib`
  schon geladen, bevor die Wache angeht — bleibt offen: `Path.touch()` und
  `Path.mkdir()` schrieben dort **wirklich** auf die Platte.
* **Auf 3.10 trifft er die falsche Funktion.** Dort hält
  `pathlib._NormalAccessor.open` nicht `os.open`, sondern `io.open`. Ein
  `staticmethod(wach_os_open)` an dieser Stelle trägt eine Funktion mit
  **anderer Signatur** ein und bricht `Path.open("r")` erst recht. Auf 3.10
  schrieben auf dem alten Stand ausserdem `Path.open("w")` und
  `Path.write_text()` **wirklich**.

Stattdessen zwei Wachen, von denen **keine `pathlib` kennt**:

| | Deckt ab | Warum das reicht |
|---|---|---|
| **`_Wache`** (eingesetzt über `_huelle`) | Kopien, die **nach** der Wache entstehen | Die Wache ist eine aufrufbare **Instanz** statt einer Funktion, also kein Deskriptor — sie bindet sich wie das C-Original |
| **`_bindungen_nachziehen`** | Kopien, die **vor** der Wache schon dastanden | Sucht über **Identität**, nicht über Namen; ersetzt sie durch die Wache |

*Nebenbefund:* das Nachziehen schliesst im echten Lauf zwei Löcher, die **auch
auf 3.11** offen waren: `bz2._builtin_open` und `tokenize._builtin_open`.

⚠️ **Eine Einschränkung, gemessen und nicht weggeschrieben:** die beiden Wachen
sind **nicht unabhängig**. Ohne die Hülle arbeitet auch das Nachziehen falsch —
es lässt zwar immer noch nichts schreiben, bricht aber ebenfalls ab. Das steht
als Prüfung `M1c` da. Umgekehrt gilt es nicht (`M2b`).

### 2. Welcher Test findet den Fehler auf dem unveränderten Stand?

**Teil L**, neu. Auf dem TB-43-Stand: **133 bestanden, 118 gescheitert.**

Er prüft auf drei Ebenen, und die Ebenen sind bewusst verschieden:

* **L1/L2 — Nachstellung.** Eine Klasse bindet `os.open`, `io.open` und
  `os.unlink` in ihrem Rumpf — **wörtlich die Zeile, die CPython in
  `pathlib._NormalAccessor` schreibt**. Einmal **vor**, einmal **nach** der
  Wache. Das läuft auf **jeder** Fassung und **fällt auf dem alten Stand auf
  jeder Fassung durch, auch auf 3.11.**
* **L3 — am echten `pathlib`**, in beiden Reihenfolgen. Das ist der Nachweis,
  dass L1/L2 die richtige Stelle nachstellen. Auf 3.9/3.10 fällt L3 auf dem
  alten Stand durch; auf 3.11+ **kann** er es nicht — dort gibt es die Stelle
  nicht mehr.
* **L4–L6 — Zeichengeräte, Dateibestand, und die Frage, ob überhaupt eine
  Fassung mitlief, die die Stelle noch hat.**

Dazu **Teil M**: jede der beiden Wachen wird **einzeln** entfernt, an einer
Kopie des Werkzeugs, mit **einer** geänderten Zeile, in einem eigenen Prozess.
Beobachtet wird der Ablauf, nicht der Quelltext. `M0` zeigt zuerst, dass die
Probe ohne Mutation das Richtige sieht.

> ⚠️ **Teil K bleibt auf dem alten Stand grün** — nachgemessen, 13/13. Genau das
> ist die blinde Stelle, die die Mac-Sitzung benannt hat: dort ist `pathlib`
> schon geladen, bevor die Wache angeht. Das steht jetzt im Kopf des Tests.

### 3. Wo gehört der Python-Versionsunterschied hin?

**Vorschlag: ein neuer `docs/UMGEBUNGEN.md`, verwiesen aus `CLAUDE.md`.
Nicht in `ARBEITSWEISE.md`.** — ⚠️ **Nicht ausgeführt**, weil
`docs/projektfuehrung/*` in dieser Aufgabe unberührt bleibt.

Der Befund vorweg: **beide Zahlen stehen schon im Repo, aber nie zusammen und
nie als Regel.**

* `docs/UEBERGABEPROTOKOLL.md` (4.4, 9.11) nennt 3.9.6 — **als Eigenschaft der
  IBKR-Brücke**, nicht des Projekts.
* Die Cloud-Fassung steht verstreut als *„Messumgebung: Python 3.11.15"* am
  Fuss einzelner Übergabedokumente.
* Kein `python_requires`, keine `sys.version_info`-Prüfung, keine Festlegung
  einer Mindestfassung. **Das ist die Lücke, aus der TB-44 entstanden ist.**

Begründung der Ablage:

* **Nicht `ARBEITSWEISE.md`:** dort stehen *stehende Anforderungen des
  Nutzers* — wie gearbeitet wird. Eine Umgebungstatsache ändert sich, wenn sich
  ein **Rechner** ändert, nicht wenn sich die **Arbeitsweise** ändert. Beides
  in einer Datei heisst, dass die Tatsache dort veraltet, wo niemand sie sucht.
  Ausserdem wird die Datei ausserhalb der Sitzungen gepflegt — eine Sitzung,
  die eine neue Fassung **misst**, könnte sie dort gar nicht eintragen.
* **Nicht nur das Übergabeprotokoll:** dort steht es bereits, und es hat nicht
  geholfen — weil es unter „IBKR" steht und nicht unter „Umgebung".
* **`CLAUDE.md` braucht den Verweis**, weil es die einzige Datei ist, die
  **jede** Sitzung automatisch liest. Eine Tatsache, die nicht übersehen werden
  darf, kann nicht nur in einem Dokument stehen, das man aufschlagen muss.

Inhalt des vorgeschlagenen Vermerks (fertig zum Übernehmen):

> **Mac (`trading-env`)** Python **3.9.6** · `dateparser` **1.2.2** · voller
> Netzzugang.
> **Cloud-Claude-Code** Python **3.11 oder neuer** · `dateparser` **1.4.3** ·
> Binance und yfinance **gesperrt (403)** · ohne `node` meldet
> `dashboard/test_dashboard.py` 780/780 statt 784.
> ⚠️ **„Grün in der Cloud" heisst strukturell nicht „grün auf dem Mac".**
> Ab Python 3.11 gibt es `pathlib._NormalAccessor` nicht mehr — genau daran ist
> TB-43 unbemerkt vorbeigelaufen. Wer eine Standardbibliotheks-Funktion
> ersetzt, prüft auf **beiden** Fassungen.

---

## Zur Frage „trägt eine Nachstellung, oder bestätigt sie nur sich selbst?"

Die Aufgabe stellt sie ausdrücklich. **Sie hat sich in dieser Sitzung nicht
gestellt — und das ist der wichtigere Befund:**

> ⚠️ **Die Cloud-Umgebung hat Python 3.10 vorinstalliert (`/usr/bin/python3.10`)
> und kann über `uv python install 3.9` in Sekunden ein echtes 3.9 dazuholen.**
> Der Fehler ist in der Cloud also **nicht** strukturell unsichtbar. Er war nur
> unsichtbar, solange man ausschliesslich unter `sys.executable` prüft.

Gemessen wurde deshalb auf **echten Interpretern**: 3.9.23, 3.10.20, 3.11.15,
3.12.3, 3.13.12. Die Nachstellung (L1/L2) ist trotzdem geblieben, aber aus einem
anderen Grund: Sie ist die **einzige** Ebene, die auch auf einem Rechner
anschlägt, auf dem gar kein altes Python liegt. Ihre Grenze ist benannt — sie
beweist, dass die Wache eine Klassenkopie überlebt, nicht dass `pathlib` genau
diese Kopie zieht. **Deshalb steht L3 daneben**, und deshalb meldet **L6**
ausdrücklich, wenn auf einem Rechner keine Fassung mit `_NormalAccessor`
mitlief.

**Bewertung:** Eine Nachstellung trägt, wenn sie den **Mechanismus** nachstellt
und nicht das Symptom — hier: das Bindungsverhalten, das auf 3.9 und 3.11
identisch ist. Sie trägt **nicht** allein. Sie braucht den echten Fall daneben,
und sie muss sagen, wenn er fehlt.

---

## Was geändert wurde

| Datei | Was |
|---|---|
| `research/universum_trockenlauf/loaderlauf.py` | `_Wache`, `_huelle`, `_bindungen_nachziehen`; alle Wachen werden gehüllt eingesetzt; der Bericht führt `bindungen_nachgezogen` |
| `research/universum_trockenlauf/test_universum_trockenlauf.py` | **Teil L** (251 Prüfungen) und **Teil M** (11 Prüfungen) neu; `_l_lauf` mit Frist |
| `research/universum_trockenlauf/BERICHT.md` | Nachtrag TB-44 |
| `docs/ERGEBNIS_…`, `docs/UEBERGABE_…`, `docs/TESTAUFTRAG_…` | neu |

**Unberührt geblieben, wie verlangt:** `docs/projektfuehrung/*`, jede
Kursdatei, beide `VORREGISTRIERUNG_*.md`,
`research/vorregistrierung/auswertung.py`, `live_params.py`, alle neun
`forward_test.py`, `equity_simulation.py`, `multi_symbol_optimise.py`,
`multi_symbol_walk_forward.py`, `shared/`, `broker/`, `dashboard/`,
`research/faltenplan_neun/`, `research/etf_trendfolge/`,
`research/registernachtrag_tb41/`, Crontab, `results/*.csv`. **Die drei in
TB-43 berichteten blinden Wachen sind unberührt** — eigene Aufgabe.

## Zahlen

| | |
|---|---|
| Cloud, neuer Stand | **332/332** |
| davon Teil A–K | 70 (unverändert) · Teil L 251 · Teil M 11 |
| geprüfte Fassungen | 3.9.23 · 3.10.20 · 3.11.15 · 3.12.3 · 3.13.12, je beide Reihenfolgen |
| Cloud, **alter** Stand, Teil L | 133 bestanden, **118 gescheitert** |
| Cloud, **alter** Stand, Teil K | 13/13 grün — die blinde Stelle, bestätigt |
| Datenstand vor/nach | `d9449faf51bffaaa…`, 223 Dateien — **identisch** |

## Offen / nächste Schritte

1. ⚠️ **Der Mac-Lauf ist der eigentliche Nachweis.**
   `docs/TESTAUFTRAG_TB-44_wache_beide_pythons.md`.
   **Die Erwartung „70/70" aus der Aufgabenstellung gilt nicht mehr** — der
   Test hat zwei Teile mehr. Erwartet ist: **0 gescheitert**, und bei genau
   einer gefundenen Python-Fassung **132/132**.
2. **Umgebungsvermerk anlegen** (Abschnitt 3 oben) — Entscheidung des Nutzers.
3. **`shared/entscheidungskerze.py:323`** — `fromisoformat` verhält sich auf
   3.9 und 3.11 verschieden (gemessen). Kein Schaden bisher, aber dieselbe
   Fehlerklasse. **Berichtet, nicht geändert.**
4. **Eine Mindestfassung festlegen** (`python_requires` oder eine Prüfung beim
   Start). Heute gibt es keine.
5. Die **drei blinden Wachen aus TB-43** bleiben offen.

---

## In einfacher Sprache

**Was wir wissen wollten.** Im Trockenlauf sitzt ein Türsteher, der verhindern
soll, dass eine Messung versehentlich Dateien verändert. Auf deinem Mac ging er
zu weit: Er ging sogar dazwischen, wenn ein Programm eine Datei nur **lesen**
wollte. Wir sollten herausfinden, ob der vorgeschlagene Flicken wirklich trägt,
einen Test bauen, der so etwas künftig findet, und klären, wo im Projekt
stehen muss, dass dein Mac und die Cloud unterschiedliche Python-Versionen
benutzen.

**Was herauskam.** Der Flicken hätte **nicht** getragen. Er hätte das Lesen
repariert, aber ein Loch offen gelassen — und auf einer anderen Python-Version
sogar an der falschen Stelle angesetzt. Wir haben stattdessen die Ursache
behoben, und dabei zeigte sich, dass der Fehler zwei Seiten hatte: In der einen
brach alles ab, in der anderen **schaute der Türsteher weg** und liess wirklich
Dateien anlegen und löschen. Die zweite Seite war die gefährlichere, weil sie
still ist. Beides ist repariert und auf fünf Python-Versionen nachgemessen. Der
neue Test schlägt auf dem alten Stand 118 Mal an.

**Warum das so ist.** Python kennt zwei Sorten von Funktionen: in C geschriebene
und in Python geschriebene. Beim Einbau in eine Klasse bekommt die
Python-Variante heimlich ein zusätzliches Argument vorangestellt — dadurch
verrutschte beim Türsteher alles um eine Position. Der neue Türsteher ist so
gebaut, dass er sich in diesem Punkt genau wie das Original verhält. Das ist
unabhängig von der Python-Version und deshalb auch für die Zukunft haltbar.

**Was das für dich heisst.** Drei Dinge. Erstens: Bitte lass den Testauftrag auf
dem Mac laufen — das ist der eigentliche Nachweis, und die erwartete Zahl hat
sich geändert (nicht mehr 70, sondern mindestens 132; entscheidend ist, dass
**nichts** rot ist). Zweitens: Der Schutz ist jetzt **dichter als vor dem
Fehler**, nicht nur wieder heil. Drittens, und das wiegt am schwersten: Dass
dein Mac auf Python 3.9.6 läuft und die Cloud auf 3.11, steht bisher nirgends
so im Projekt, dass eine neue Sitzung es sieht. Wir schlagen einen kurzen
Umgebungsvermerk vor und einen Einzeiler in der Datei, die jede Sitzung
automatisch liest. Eintragen müsstest du das, weil diese Dokumente ausserhalb
der Sitzungen gepflegt werden. **Eine gute Nachricht dazu:** die Cloud kann
alte Python-Versionen nachinstallieren — der Fehler ist dort also künftig
prüfbar, nicht nur auf dem Mac.
