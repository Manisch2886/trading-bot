# Übergabe — Stand 20.09.2026, 12:40 Ortszeit

⚠️ **Der Dateiname trägt das Datum der Anlage, nicht des Standes.** *Fortgeschrieben statt neu angelegt, nach `UMZUG.md` Abschnitt 1 — eine zweite Übergabedatei neben dieser wäre Danebenstellen (`DOKUMENTATIONSSTANDARD.md` Regel 9). ⇒ **Offener Punkt: der Name sollte `UEBERGABE.md` ohne Datum lauten**; sechs Verweise im Repo wären mitzuziehen, plus der Eintrag in der Projektablage.*

**Fortgeschrieben nach dem Verfahren in `docs/projektfuehrung/UMZUG.md`,
Abschnitt 4, Schritt 3. Neun Blöcke, jeder Wert mit Fundstelle.**

⚠️ **Jede Aussage hier sagt, ob sie gemessen oder erschlossen ist.** *Das ist
die Regel aus dem Fehler des Tages (Block 7, Punkt 3).*

---

## Block 1 — Der Stand in drei Zeilen

**Fertig, Stand 20.09.2026 12:40:** Die methodischen Grundlagen vor dem
signierten Tag sind weitgehend repariert — Snapshot gezogen und registriert,
Resolver mit Codeherkunft und Lock als blockierende Startprüfungen, **TB-56**
hat die Faltenschranke entfernt, **TB-56b** die Registerberichtigung (Abschnitt
21) eingetragen, **Fables Methodenantwort** ist als Abschnitt 22 verarbeitet,
und **TB-59/TB-60** haben das Backlog eingearbeitet und archiviert.

⭐ **Der Befund des 20.09., und er verändert die Kette:**
`research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` ist für **alle
neun Bots** überholt — fünf Krypto-Bots als `platzhalter` mit leerer
`dd_toleranz`, **vier Aktien-Bots als `endgueltig` mit Falten ab 2019**, während
Registerabschnitt 21 für sie **2017** bzw. **2018** nennt. ⚠️ **Damit erklärt
sich auch der eine unerwartet rote Test** (`KeyError: '2017'` an
`auswertung.py:237`).

**Als Nächstes:** **TB-61** (Benchmark-Tabelle für alle neun, Lauf **daneben**,
rechnet) und **TB-62** (Nachträge (m) und (v) einarbeiten, ZIP-Pflicht abbauen,
rechnet nicht). ⚠️ **Nacheinander, nie gleichzeitig** — beide schreiben nach
`docs/`.

---

## Block 2 — `HEAD`, Zweig, Commit-Kette

| | gemessen 20.09.2026 12:37 |
|---|---|
| Zweig | **`main`**, kein eigener Zweig, kein PR |
| `HEAD` | **`790f502`**, 20.09.2026 12:36:56 +0200 |
| `origin/main` | **gleich** — alles gepusht |
| Arbeitsbaum | **sauber**, 0 geänderte und 0 unversionierte Dateien unter `docs/` |
| Commits am 20.09. | **neun** |

**Die Kette des 20.09., in Reihenfolge:**

```
64cc2b5 0bb4c92 85ff363 c04b348 3ac4710 79742d1 496bfa5 28eea5c 198fc32 48a526b 790f502
```

⚠️ **Zeitstempel im Repo sind Ortszeit (+02:00), in der Projektablage UTC.**
⭐ *Am 20.09. beinahe zu einem Fehlbefund geführt: ein Vergleich beider ergab
scheinbar zwei Stunden Rückstand — es waren zwei Minuten.*

---

## Block 3 — Die tragenden Zahlen, jede mit Fundstelle

| | Wert | Fundstelle |
|---|---|---|
| **Datenstand** | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223** Kursdateien | an einem Tag über 20× gemessen, immer gleich |
| ⭐ **Auflösung** *(gemessen 19.09., 21:03)* | **174× `1d` · 25× `1h` · 24× `4h`** — Stundenauflösung **nur Krypto**, alle 174 Aktiendateien nur Tagesdaten | `ls data/*.csv`, erste Datenzeilen |
| **Snapshot** | `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` — **225** Dateien, **211 040 678** Bytes, `2026-09-19T06:49:32+00:00` | Commit `1075dec`, Register **Abschnitt 18** |
| ⚠️ **nicht verwechseln** | `4fee547d…` in Abschnitt **17.9** läuft nur über die **223** Kursdateien und bezeichnet **nicht** diesen Snapshot | in Abschnitt 18 ausdrücklich abgegrenzt |
| **Lock** | `requirements.lock`, SHA-256 `96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5`, **67** Pakete | Register **Abschnitt 20**, Commit `d852bce` |
| | `pandas==2.3.3` · `numpy==2.0.2` · `pandas-market-calendars==4.6.1` | |
| | Interpreter `3.9.6 (Clang 17.0.0)`, Plattform `macOS-15.7.9-x86_64-i386-64bit` | |
| **Registerabschnitte neu** | **18** (Tatsachennotiz Snapshot, `0fe61d7`) · **19** (Registertext 5e Codeherkunft, `409d71d`) · **20** (Tatsachennotiz 5f Lock) | |
| **Sperrklinken** | Wanduhr **6** · eigener Pfadbau **29** — grün, solange die Zahlen nicht wachsen | `research/selektionsmasse/ergebnisse/` |
| **Datenbanken** | **12** `*.db` außerhalb `trading-env/`, davon **9** `paper_trading_*` in der Wurzel | in jedem Lauf 12/12 byteweise identisch |

### ⚠️ Gemessene Nummernstände — damit keine Nummern mehr erfunden werden

**Gemessen 20.09.2026, 12:30, Stand `790f502`** — mit dem Muster
`^\| \*\*(K\d[a-z])\*\*` **ohne schliessenden Balken**, damit Zeilen mit
Vergabevermerk mitzählen:

| | in `BACKLOG.md` + `BACKLOG_ARCHIV.md` | nächste freie |
|---|---|---|
| Blockbezeichner Abschnitt 2 | höchster **`2y`** | **`2z`** — danach ist der `2x`-Raum erschöpft |
| K-Nummern Abschnitt 4 | **64 Zeilen, 62 verschiedene**, höchste **`K3j`** | ⚠️ **selbst messen** — Nachtrag (v) belegt `K3k` aufwärts, und er wächst noch |
| Kettenzeilen Abschnitt 3 | höchste **`0,98`** | — |

⚠️ **Zwei echte Doppelbelegungen, gefunden am 20.09.:** `K1o` und `K1q` stehen
je zweimal in `BACKLOG.md` (Zeilen 1331/1335 und 1333/1336). **In der Sache
harmlos** — Fortschreibungen von TB-50 nach TB-51 mit dem Vermerk
*"(unverändert)"*. **In der Form ein Verstoss gegen Regel 9**; TB-62 führt sie
zusammen.

⭐⭐ **Die Messregel selbst, und sie hat an einem Tag dreimal versagt:**
`K2[a-z]` sah keine `K3`-Nummern · `^\| \*\*K..\*\* \|` sah keine Zeile mit
Vergabevermerk · `sort -u` entfernte genau die Duplikate, die gesucht waren.
⇒ **Eine Kollisionsprobe zählt, sie vereinheitlicht nicht — und ihr Muster
darf an keinem Format hängen, das eine Ausnahme bekommen kann.**

---

## Block 4 — Offen vor dem signierten Tag, in Reihenfolge

| | | Begründung der Stelle |
|---|---|---|
| **1** | ⭐⭐ **TB-61 — Benchmark-Tabelle für alle neun Bots** (`docs/auftraege/MAC_TB-61_benchmark_neun.md`) | **Sie ist für alle neun überholt.** Fünf Bots haben keine `DD_Toleranz`, vier tragen Falten der entfernten Schranke. ⛔ Lauf **daneben** nach `benchmark_drawdowns_neu.json`; die gesperrte Datei bleibt byteweise unverändert (Registerabschnitt 21.9), SHA-256 `a163c498…36d1ee` ist der Nachweis |
| **2** | **TB-62 — Nachträge (m) und (v) einarbeiten, ZIP-Pflicht abbauen** (`docs/auftraege/MAC_TB-62_nachtraege_m_v.md`) | Reine Dokumentation, rechnet nicht. ⚠️ **Nachtrag (m) wurde nie eingearbeitet**, zwei seiner Regeln stehen nirgends im Repo |
| **3** | **`auswertung.py` auf Verfahren B** | ⚠️ **Berichtigt gegenüber dem 19.09.:** Der rote Test `KeyError: '2017'` hängt **nicht** hieran, sondern an der überholten Benchmark-Tabelle. *Nicht gemessen, sondern erschlossen: dass TB-61 ihn grün macht — das ist zu prüfen* |
| **4** | **Das Amendment zu Sperrliste Punkt 4** | **Eigene Betreiberfreigabe**, nach 21.9 einmal für alle neun. `DD_Toleranz` wird dabei nachgiebiger (100 % Exposure: −8,55 → **−12,89**) |
| **5** | **Lese-Audit** (Fables Schicht 3, Datenseite) | *"Der Lese-Audit beweist, welche DATEN gelesen wurden. Er sagt nichts darüber, welcher CODE gelesen hat"* — die Codeseite ist mit TB-58 erledigt, die Datenseite nicht |
| **6** | **Lauf-Reproduktion gegen den Lock** — frischer Klon in isolierter Umgebung, gleiche Maschine zulässig | F1b/Q2 ist **für die Daten** bewiesen (SHA-256 ist pandas-unabhängig), **nicht für den Lauf** |
| **7** | **T56b.6** — zwei Code-Kopien der Faltenschranke (`faltenplan_neun.py:120`, `krypto_historie/faltenplan.py:64`), mit Probe F in `test_faltenplan_neun.py:519` | Mac-Lauf, Freigabe liegt seit TB-56 vor |
| **8** | **Fables Q1** | |
| **9** | ⭐ **Der signierte Tag + Zeitanker** | alles davor |

✅ **Erledigt seit dem 19.09.:** der Commit der elf zwischengelagerten Dateien ·
TB-56 · TB-56b · Fables Methodenantwort (Registerabschnitt 22) · TB-59 · TB-60.

**Hinter dem Tag, in dieser Reihenfolge:** `AF → RT → QR → KG → MI`
*(begründet in Nachtrag (r), RT9).*

---

## Block 5 — Wartezustände

| wartet auf | was | Stand |
|---|---|---|
| **Betreiber** | **TB-61 und TB-62 starten** — Einfügesatz aus `docs/auftraege/AKTUELLER_AUFTRAG.md`, mit `TB-61:` bzw. `TB-62:` vorangestellt | ⏳ **beide bereit**, nacheinander |
| **Betreiber** | **Freigabe für das Amendment** zu Sperrliste Punkt 4 | erst **nach** TB-61 |
| **Betreiber** | **T46.1b/c** — der stille Stop-Loss-Übersprung in allen neun `forward_test.py`; Vorschlag *melden, nicht handeln* über `shared/ladeprotokoll.py` | freigabepflichtig, offen |
| **Betreiber** | **T56b.7** — die Übergabe nennt eine *"Änderung an Registertext 5f"*, die im Repo nirgends spezifiziert ist | Rückfrage offen |
| **Fable** | **Q1** — die Querprüfung zwischen Auswerter-Umbau und signiertem Tag | noch nicht gestellt |

✅ **Aufgelöst seit dem 19.09.:** Fables vier Methodenfragen sind beantwortet und
als Registerabschnitt 22 eingetragen — **ein offener Wartezustand auf ihn
besteht nicht mehr** (T56b-Block). Die TB-56-Mac-Sitzung ist abgeschlossen.

---

## Block 6 — Freigaben und Sperrliste

**Die Sperrliste, unverändert:**

`strategies/*/live_params.py` · `strategies/*/forward_test.py` ·
`strategies/*/equity_simulation.py` (hart) · `strategies/*/multi_symbol_optimise.py` ·
`shared/entscheidungskerze.py` · `shared/paths.py`

⚠️ **Vor jedem Merge wird der Diff der Sperrlisten-Dateien angesehen, auch bei
erteilter Freigabe:** *Die Freigabe sagt, dass geändert werden durfte; sie sagt
nicht, was geändert wurde.*

**Erteilte Freigaben, mit Aufgabe:**

| Datei | freigegeben für | Stand |
|---|---|---|
| `shared/paths.py` | TB-52, erneut TB-58 | in Anspruch genommen |
| `shared/strategy_paths.py` | TB-53b | in Anspruch genommen (`29016cf`) |
| `research/vorregistrierung/registerdaten.py` | TB-56 | in Anspruch genommen (`7387cc5`) |
| `research/vorregistrierung/faltenplan.py` | TB-56 | in Anspruch genommen |
| `research/faltenplan_neun/faltenplan_neun.py` | TB-56 | ⚠️ **erteilt, NICHT in Anspruch genommen** — Antwort zu Frage 3: bis TB-56b unverändert |
| `research/faltenplan_neun/test_faltenplan_neun.py` | TB-56 | ⚠️ **erteilt, NICHT in Anspruch genommen** |

⚠️⚠️ **Ausdrücklich NICHT freigegeben:**
`research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` (Sperrliste 4).
**Der gesperrte Wert `DD_Toleranz` würde sich bei zwei Bots ändern — das ist ein
Amendment und gehört nach TB-56b.** Entscheidung des Betreibers zu Frage 4:
**Option (a)** — neue Tabelle als eigene Datei daneben, die gesperrte byteweise
unverändert, `test_vorregistrierung.py` bis TB-56b rot.

⚠️ **Der neue rote Test darf NICHT als „bekannt rot" geführt werden.** Er braucht
die Marke **„offen durch eigene Änderung — blockierend für den Tag"**. *So sind
die fünf bestehenden roten Tests entstanden.*

### Die Entscheidungsaufteilung, vom Betreiber bestätigt 19.09.2026

| | |
|---|---|
| **Handwerk — ich entscheide allein** | Aufgabenreihenfolge, Schnitt, Nachweismethode, Dokumentstruktur |
| ⚠️⚠️ **Verfahren vor dem Tag — nie nach erwartetem Effekt** | geht an den Betreiber oder an Fable. **Ausdrücklich nicht** nach „bestmöglicher Rentabilität" entschieden — das ist genau der Fehler, den das Register verhindert |

---

## Block 7 — ⭐⭐ Die Fehler dieses Chats und die Regeln daraus

**Der wertvollste Block. Ohne ihn wiederholt der neue Chat sie.**

| | Fehler | ⇒ Regel |
|---|---|---|
| **1** | ⚠️ **Vier Nummernkollisionen**: `0,87` doppelt · `V1` doppelt · „TB-54" für zwei Aufgaben · **(p) nennt „Block 2v"/„K2y" frei erfunden** | ⭐ **K2i: Ein Nachtrag nennt keine Nummer, die er nicht selbst gemessen hat.** Er sagt „die nächste freie, gemessen" |
| **2** | ⚠️⚠️ **UTC als Ortszeit gelesen** → geschlossen, eine Sitzung sei seit zwei Stunden tot; sie arbeitete gerade und hatte 25 Minuten zuvor committet | ⭐ **Vor jeder Folgerung aus einem Zeitstempel `date -u` gegen `TZ=Europe/Berlin date` halten** |
| **3** | ⚠️⚠️ **Name statt Messung, vier Fälle**: KG5 aus `MIN_HISTORY_HOURS` erschlossen · RT3 aus Botnamen · RT1 gar nicht nachgesehen · KG1s „196 000" als *„Struktur des Entwurfs"* bezeichnet, obwohl es meine Annahmen waren | ⭐⭐ **Ein Name ist kein Messwert. Jeder Satz sagt, ob er gemessen oder geschlossen ist.** Dieselbe Klasse wie Fables Schicht-3-Befund. Berichtigung liegt vor |
| **4** | ⚠️ **Behauptet, `63e4b6c8…` stehe in den TB-52-Berichten** — gemessen: **0 Treffer** in beiden Archiven | Herkunft einer Zahl wird gezählt, nicht erinnert |
| **5** | ⚠️ **„F1b/Q2 ist erledigt"** — Fable korrigierte: **für die Daten** bewiesen (SHA-256 ist pandas-unabhängig), **nicht für den Lauf** | Ein Nachweis gilt für den Gegenstand, den er berührt, nicht für den Zweck, den er dienen sollte |
| **6** | ⚠️ **Abbruchkriterium nannte einen Stellvertreter** (*„ein Abschnitt mit einer Zahl darin"* statt *„der DIESEN Snapshot bezeichnet"*) | ⭐ **Ein Abbruchkriterium benennt die Sache, nie ihr Merkmal.** Und: fallen Wortlaut und Zweck auseinander und ist jemand erreichbar — **fragen**, nicht entscheiden |
| **7** | ⚠️ **`device_commit_files` mit `force: true` meldete „written" und änderte die Datei nicht** | ⭐ **Nie überschreiben, immer neuer Dateiname, danach mit `wc -c` und `grep` nachprüfen** |
| **8** | ⚠️ **`git status` über die Geräte-Brücke hinterließ ein `.git/index.lock`**, das die Brücke nicht löschen kann | ⭐ Über die Brücke **kein `git status`, kein `git add`**; lesende git-Befehle nur mit `--no-optional-locks` |
| **9** | ⚠️ **Aufgabendateien nach `~/Downloads` gelegt** — macOS TCC verweigert Claude-Code-Sitzungen den Zugriff dort. **Kostete drei Sitzungsstarts** | ⭐ Zwischenlager ist `logs/auftraege/`; endgültiger Ort ist immer das Repo |
| **10** | ⚠️ **Am Repo gearbeitet, während eine Mac-Sitzung lief.** Folgenlos, **weil der Zielordner gitignoriert ist** — das war die Vorsichtsmaßnahme, nicht mein Wissen | ⭐ Zustand der Sitzung **messen**, bevor am Repo gearbeitet wird |
| **11** | ⚠️ **Reihenfolge der Epics nach ihrem Anspruch eingeordnet statt nach ihren Voraussetzungen** (`AF→QR→KG→MI`) | korrigiert zu **`AF→RT→QR→KG→MI`**; RT braucht fast keine Vorbedingungen |

⚠️⚠️ **Die Fehler des 20.09.2026 stehen NICHT hier, sondern in
`docs/projektfuehrung/nachtraege/BACKLOG_NACHTRAG_2026-09-19v.md`** als `K3t`
bis `K4e` — sie werden mit TB-62 ins Backlog eingearbeitet. *Sie hier zu
wiederholen wäre Danebenstellen.* ⭐ **Ihr gemeinsamer Kern, in einem Satz:**
Fünf von ihnen sind Messungen, die mit einem Instrument gemacht wurden, das
ihren Suchraum nicht abdeckte — ein zu enges Muster, eine falsche Bezugsmenge,
ein `sort -u`. ⇒ **Ein Messergebnis wird gegen eine zweite, unabhängig
geschriebene Zählung gehalten, bevor es als Nachweis gilt.**

**Fremde Befunde, die diesen Chat geprägt haben:**

| | |
|---|---|
| ⭐⭐ **Fable, Schicht 3** | *„Der Lese-Audit beweist, welche DATEN gelesen wurden. Er sagt nichts darüber, welcher CODE gelesen hat."* → TB-58 (Codeherkunft) |
| ⭐⭐ **Fable, F17** | *„Die Grenze zwischen Berichtigung und nachträglicher Wahl ist nicht die Zeit, sondern die QUELLE DES GRUNDES."* |
| ⭐ **Fable, Tatsachennotiz** | *„Eine Tatsachennotiz hält fest, sie schafft nicht."* Jeder Satz ist Messwert mit Herkunft oder Verweis |
| ⭐ **Prüfprinzip A7** *(neu)* | Eine nachgeholte Vorher-Messung gilt nur, wenn der Zustand inhaltsadressiert wiederherstellbar ist — **und sie muss sagen, dass sie nachgeholt wurde** |
| ⭐⭐ **TB-56, Nachweis 4a/4b** | Die Schranke künstlich wieder eingesetzt: Plan ändert sich bei **8 von 9**; in einer Wegwerf-Kopie beginnen unmutiert `2017/2018`, mutiert **alle vier 2019**. **Die Probe beißt** |

---

## Block 8 — ✅ Zwischengelagert: abgearbeitet

✅ **Die elf Dateien aus `logs/auftraege/` sind committet** (19.09., `aa05cc1`
und Vorgänger) — fünf Nachträge, eine Berichtigung, fünf Vorlagen. Sie liegen
unter `docs/projektfuehrung/nachtraege/` und `docs/vorlagen/`.

⚠️ **Eine Datei hat noch eine offene Bringschuld:** `logs/auftraege/TB-58b_v2.md`
— ohne Gegenstück im Repo, und `logs/` ist gitignoriert (`.gitignore:27`).
*`logs/auftraege/` ist kein Träger (`UMZUG.md` Abschnitt 2).*

⚠️⚠️ **Und zwei Einarbeitungen stehen trotzdem aus, gemessen am 20.09.2026:**

| | |
|---|---|
| **Nachtrag (v)** | **nicht eingearbeitet** — seine Nummern ab `K3k` stehen nur dort. ⇒ **TB-62** |
| **Nachtrag (m)** | ⚠️⚠️ **nie eingearbeitet, und seine sechs Nummern `K2l`–`K2q` sind im Backlog an andere Inhalte vergeben.** Vier seiner Regeln stehen inhaltlich anderswo; **zwei stehen nirgends im Repo**. ⇒ **TB-62** |

**Die zwei verlorenen Regeln aus (m), wörtlich — damit sie diesen Text überleben:**

> **(1)** „Jede Rückfrage an den Betreiber und seine Antwort kommen wörtlich in
> den Bericht — sonst leben sie nur im Sitzungsverlauf, der mit der Sitzung
> verschwindet.“
>
> **(2)** „Die Sitzung committet ihren eigenen Auftrag mit (`docs/auftraege/`)
> und ihre Belege (`docs/belege/TB-xx/`).“

⭐⭐ **Regel (1) ist die Pointe: sie ist genau die Vorschrift, die verhindern
soll, dass Betreiberentscheidungen nur im Chat leben — und sie ist selbst im
Chat geblieben.**

### ⚠️ Und dasselbe ist der ZIP-Regel passiert

**Die Liste unten stand schon am 19.09. in diesem Block.** Ihr Punkt 9 lautet
*"Keine ZIPs, nichts nach `~/Downloads`"*. ⚠️ **Gemessen am 20.09.: `ARBEITSWEISE.md`
Abschnitt 1 verlangte weiterhin auf acht Zeilen das Gegenteil**, während
Abschnitt 10 derselben Datei ZIP als überholt bezeichnete. ⭐ **Betreiberentscheidung
20.09.2026: ZIP wird überall abgeschafft**; der Umbau ist Schritt 4 von TB-62.

| | Regel, vereinbart 19.09.2026 |
|---|---|
| 1 | Schritt für Schritt, **ein Terminalbefehl je Nachricht**, nummeriert |
| 2 | **Nie eine blosse Ankündigung** — entweder explizite Aufgabe oder fortfahren |
| 3 | Jede Antwort endet mit dem abgesetzten Block **"Deine Aufgaben"** |
| 4 | **Möglichst wenig eigener Aufwand** des Betreibers |
| 5 | Rückfragen über die **anklickbaren Fragen in der App**, mit Empfehlung |
| 6 | **`/remote-control` als eigener Block VOR** dem Anweisungstext |
| 7 | Jede Aufgabe trägt **`[ortsunabhängig]` oder `[Mac-pflichtig]`** |
| 8 | **Fable-Texte als Kopierblock in der Antwort** — keine Datei, kein Anhang |
| 9 | ✅ **Keine ZIPs, nichts nach `~/Downloads`** — am 20.09. bestätigt und in Arbeit |
| 10 | ⭐ **Frühzeitiger Hinweis auf einen nötigen Umzug**, bevor komprimiert wird |

✅ **Aus dieser Liste seit dem 19.09. eingetragen:** Punkt 2 als `ARBEITSWEISE.md`
Abschnitt 13, Punkt 6 und der Sitzungsstart als Abschnitt 14, dazu Abschnitt 15
(*"zukünftig"*), 16, 17 (einleitender Satz) und 18.

✅ **`ARBEITSWEISE.md` Abschnitt 10** ist durch den Verweis auf `UMZUG.md`
ersetzt (TB-59, ein Hunk am Ankertext).

---

## Block 9 — Der Eröffnungstext für den neuen Chat

⭐ **Der Text steht nur noch an einer Stelle: `UMZUG.md` Abschnitt 6** — die
verbindliche Fassung, mit den berichtigten Pfaden und der Prüfung der
Geräteanbindung im Text. *Die Kopie, die hier bis zum 20.09.2026 stand
(20 Zeilen, seit `2723c16` unverändert), wich von der Vorlage ab — fünf Dokumente
statt vier, fester Dateiname statt Platzhalter, ein Hinweis auf `ARBEITSWEISE.md`
Abschnitt 10, der seit TB-62 überholt war — und beide zeigten auf
`projektfuehrung/PRUEFPRINZIPIEN.md`, wo die Datei nie lag. Entfernt mit TB-68,
`DOKUMENTATIONSSTANDARD.md` Regel 9; `UMZUG.md` Schritt 3, Zeile 9 verlangt
seither hier einen Verweis, keinen zweiten Text.*

---

## In einfacher Sprache

**Wo wir stehen:** Die Grundlagen für den großen Auswahllauf sind fast fertig
repariert. Die eingefrorene Datenkopie steht im Regelwerk, die Startprüfungen
brechen ab, wenn Code oder Programmversionen nicht die registrierten sind, und
heute Abend ist die künstliche Jahresgrenze 2019 aus dem Code verschwunden —
nachdem gemessen wurde, dass sie bei acht von neun Bots wirkt und bei keinem
einzigen die Zulassung ändert.

**Was gerade läuft:** Die Mac-Sitzung rechnet alle 71 Testdateien noch einmal
durch, um zu belegen, dass die Änderung nichts kaputtgemacht hat außer der einen
Stelle, die wir kennen und benannt haben.

**Was als Nächstes dran ist:** Elf Dateien müssen ins Projektarchiv — fünf
Konzeptschichten, die du eingereicht hast, samt meiner Bewertung und einer
Berichtigung meiner eigenen Fehler. Danach muss das Regelwerk an der Stelle
korrigiert werden, an der es heute noch etwas behauptet, das die Messung von
heute widerlegt hat.

⭐ **Das Wichtigste an diesem Dokument ist Block 7.** Dort stehen elf Fehler, die
ich heute gemacht habe, und die Regel, die aus jedem folgt. **Der häufigste war
derselbe in vier Gestalten: Ich habe aus einem Namen geschlossen, statt
nachzumessen.** Dass eine Konstante „Stunden" heißt, sagt nichts über die
Auflösung der Daten. Dass ein Bot „Ausbruch" heißt, sagt nichts über seine
Gewinnverteilung. **Ab jetzt sagt jeder Satz, ob er gemessen oder geschlossen
ist.**

---

# Nachtrag zur Übergabe — 21:45 Ortszeit

⚠️ **Die Blöcke 1, 2, 4, 5 und 8 oben stehen auf dem Stand 21:15. Seither ist
folgendes eingetreten. Bei Widerspruch gilt dieser Nachtrag.**

## TB-56 ist abgeschlossen

| | gemessen 21:42 |
|---|---|
| Commits | `04b42b3` (Teil A, Messung) → `7387cc5` (Teil B, Schranke entfernt) → **`8946217`** (Ergebnisdokument, 32 119 Bytes) |
| **Basislauf nachher** | **60 grün / 6 rot / 1 flackernd / 3 ungeprüft / 1 Zeitgrenze = 71** |
| ⭐ **`UNERWARTET 1`** | `research/vorregistrierung/test_vorregistrierung.py`, `KeyError: '2017'` in `auswertung.py:237` — **ausdrücklich als unerwartet geführt, nicht als „bekannt rot"** |
| Datenstand nachher | `d9449faf…` ✓ · Snapshot `UNVERAENDERT` ✓ · Registerprüfer **KEIN BEFUND** ✓ |
| ⭐ **12 Datenbanken** | alle `OK`, `rc=0` — byteweise identisch |

## Die dreizehn Dateien sind committet

**`HEAD` = `2723c16`**, 19.09.2026 21:40:36 +0200, auf `origin/main`.
**13 Dateien, 7 032 Einfügungen, 0 Entfernungen.**

⇒ **Block 8 oben ist damit erledigt**, mit einer Ausnahme: die fünf Nachträge
(n)–(r) sind **abgelegt, aber in `BACKLOG.md` noch nicht eingearbeitet** —
gemessen 0 Treffer für `AF`, `MI`, `QR`, `KG`, `RT`. ⚠️ **Und die erfundenen
Nummern in (p) („Block 2v", „K2y/K2z") müssen beim Einarbeiten auf die gemessene
freie Nummer umgeschrieben werden, mit Vermerk.** Frei: Block **`2s`**,
K-Nummern ab **`K2l`**.

## Die nächsten drei Punkte

| | |
|---|---|
| **1** | ⚠️⚠️ **TB-56b — Registerberichtigung 15.6 Punkt 2.** Dort steht *„die Schranke dafür ist das Register, nicht die Datenlage"*; TB-56 hat gemessen, dass die Datenlage 2017/2018/2019 zulässt. **Solange das so dasteht, widerspricht der Code dem Register.** Dazu im selben Zug: das Amendment zu Sperrliste 4 (`benchmark_drawdowns.json`, `DD_Toleranz` bei zwei Bots), die Änderung an Registertext 5f, die Prüfung der Abschnitte 18/20 gegen den Tatsachennotiz-Test und die Drei-Kategorien-Regel in Registertext 0 |
| **2** | **Einarbeitung von (n)–(r) in `BACKLOG.md`** samt den fünf Sichtungsdurchgängen und dem Ersatz von `ARBEITSWEISE.md` Abschnitt 10 durch den Verweis auf `UMZUG.md` (Ersatztext dort in Abschnitt 7) |
| **3** | **`auswertung.py` auf Verfahren B** — damit fällt der unerwartete rote Test |

## Zwei Umgebungsbefunde aus dem Umzug

| | |
|---|---|
| ⚠️ | **Termius frisst Geviertstriche und Zeilenumbrüche in Befehlen.** Die vierzeilige Commitnachricht kam als **zwei** Zeilen an, und ein `—` verschwand aus einer Fehlermeldung. Folgenlos, aber: **in Befehlen für Termius keine Geviertstriche und keine Zeilenumbrüche verwenden** |
| ⚠️ | **`logs/auftraege/` ist über `.gitignore:27` (`logs/`) ausgeschlossen.** Eine Datei dort ist kein Beleg. Der Ordner ist Zwischenlager, und jede Datei darin hat eine offene Bringschuld ins Repo |

---

# Nachtrag 2 zur Übergabe — 21:50, die Arbeitsteilung

⚠️⚠️ **Dieser Nachtrag schließt eine Lücke, die beim Umzug aufgefallen ist.**
`ARBEITSWEISE.md` Abschnitt 7 („ein Befehl je Nachricht") und Abschnitt 6b
setzen voraus, dass der **Betreiber** Terminalbefehle ausführt und die Ausgabe
zurückkopiert. **Am 19.09.2026 war das überwiegend nicht mehr nötig** — und
niemand hatte es aufgeschrieben.

## Die Geräteanbindung an das MacBook

⭐⭐ **Wo eine Sitzung über die Geräteanbindung auf `~/trading-bot` zugreifen
kann, MESSE ICH SELBST.** Der Betreiber kopiert keine Terminalausgaben mehr.

**Was am 19.09. so gemessen wurde, ohne eine einzige Ausgabe von ihm:**

| | |
|---|---|
| `HEAD`, Commit-Kette, `numstat`, ob ein Commit auf `origin/main` liegt | ⚠️ nur lesend, **immer mit `--no-optional-locks`** |
| Dateigrößen, Zeilenzahlen, `cmp`-Vergleiche, `grep`-Zählungen | |
| ⭐ **Die Datenauflösung** (174× `1d`, 25× `1h`, 24× `4h`) — der Befund, der Epic KG geschärft hat | |
| Der Fortschritt einer laufenden Mac-Sitzung, ihre Belege, ihre Rückfragen | |
| Gemessene Nummernstände im Backlog (`2r`, `K2k`, `0,97`) | |
| Ablage von Dateien in `logs/auftraege/` | ⚠️ **nur dort, solange eine Sitzung läuft** |

## ⚠️ Die Grenzen, ehrlich benannt

| | |
|---|---|
| ⚠️⚠️ | **Die Anbindung ist nicht in jedem Chat vorhanden.** Sie hängt daran, dass die Unterhaltung mit dem Rechner verbunden ist. **Erst prüfen, dann behaupten** — und wenn sie fehlt, es sagen statt zu raten |
| ⚠️⚠️ | **Kein `git status`, kein `git add`, kein Commit über die Anbindung.** `git status` hat am 19.09. ein `.git/index.lock` hinterlassen, das die Anbindung nicht löschen konnte. **Schreibende git-Befehle bleiben beim Betreiber** |
| ⚠️ | **Keine SQLite-Datei öffnen, während eine Sitzung die Datenbanken quersummengesichert hat** — das kann `-wal`/`-shm` anlegen und den Byte-Vergleich scheitern lassen |
| ⚠️ | **Nichts nach `docs/` schreiben, solange eine Sitzung läuft** — eine unversionierte Datei reißt deren `git status --short`-Prüfung |
| ⚠️ | **Zeitstempel sind UTC**, Ortszeit +02:00 |

## Was beim Betreiber bleibt

| | |
|---|---|
| **1** | ⭐ **Befehle, die eine Freigabe brauchen**: `git add`/`commit`/`push`, Sitzungsstarts, Löschungen — **als EIN kopierfertiger Block, ohne Geviertstriche und ohne Zeilenumbrüche** (Termius frisst beides) |
| **2** | ⭐ **Rückfragen beantworten, per Multiple Choice mit Empfehlung** — anklicken, nicht formulieren |
| **3** | **Entscheidungen, die ihm gehören**: Freigaben für Sperrlisten-Dateien, Verfahrensfragen vor dem Tag, der Termin des Laufs |
| **4** | **Nachrichten an Fable einfügen** — als Kopierblock aus der Antwort |

⚠️ **Und Fables Antworten gehören in den Chat, in dem die betroffene Arbeit
läuft** — nicht in den, der die Frage formuliert hat. *Die vier Fragen vom
19.09. betreffen TB-56b und einen möglichen Registertext vor dem Tag; die Antwort
gehört also in den Chat, der TB-56b bearbeitet.*

## ⇒ Was daraus für `ARBEITSWEISE.md` folgt

⚠️ **Abschnitt 7 braucht einen Vorsatz** (Ersatztext für den nächsten
Mac-Auftrag):

> ⭐ **Vorbedingung zu Abschnitt 7:** Die folgenden Regeln gelten für Befehle,
> die der **Betreiber** ausführt. **Ist die Geräteanbindung an das MacBook
> verfügbar, wird lesend selbst gemessen** — dann entsteht für ihn gar kein
> Befehl. Ein Befehl an ihn wird nur noch formuliert, wenn er eine **Freigabe**
> trägt (`git add`/`commit`/`push`, Sitzungsstart, Löschung) oder die Anbindung
> fehlt.

---

# Nachtrag 3 zur Übergabe — 22:55, eine elfte stehende Regel

⚠️ **Block 8 führt zehn im Chat vom 19.09.2026 vereinbarte Regeln. Dies ist die
elfte, und sie ist nach dem Umzug entstanden.**

| | Regel, vereinbart 19.09.2026 |
|---|---|
| **11** | ⭐⭐ **Immer direkt weitermachen.** *„Mache immer direkt weiter ohne das ich dich fragen muss wie geht es weiter."* Eine Antwort endet nie mit einem Stillstand; der nächste Handwerksschritt wird getan, nicht angekündigt. ⚠️ **Die Grenze bleibt:** Verfahrensfragen vor dem Tag gehen weiter an den Betreiber oder an Fable — aber als anklickbare Entscheidungsvorlage **neben** der laufenden Arbeit, nicht als Haltepunkt. Freigabepflichtige Befehle bleiben beim Betreiber; „weitermachen" heisst, alles bis zu ihnen fertig zu haben |

**Eingetragen in:** `ARBEITSWEISE.md` **Abschnitt 13** (neu) · die Erinnerung
(`/projects/<id>/preferences.md`) · Backlog-Nachtrag **(t)**, Punkt `K2n`
(vorgeschlagene Nummer, gemessener Stand im Nachtrag). ⭐ **Drei Träger, wie es
`UMZUG.md` Abschnitt 2 verlangt** — die Erinnerung wirkt davon als einzige ohne
Zutun des Betreibers.

---

# Nachtrag 4 zur Übergabe — 21.09.2026, 17:10 Ortszeit (15:10 UTC)

⚠️⚠️ **Ab hier gilt der 21.09.** Die Blöcke 1–9 oben sind der Stand vom 20.09.,
12:40; sie bleiben stehen (append-only), sind aber überholt, wo dieser Nachtrag
etwas anderes sagt. **Dieser Nachtrag ist der Stand.**

⚠️ **Geschrieben, während TB-77 läuft.** Nach `UMZUG.md` Abschnitt 3 ist ein
Umzug in diesem Zustand ausdrücklich **nicht** erlaubt — laufende Sitzung **und**
offene Rückfrage an Fable. Dieser Nachtrag ist die Vorarbeit nach Abschnitt 1
(*„die Übergabe wird laufend gepflegt, nicht beim Umzug geschrieben"*), nicht
der Vollzug.

⭐ **Alle Zahlen unten sind am 21.09. zwischen 16:55 und 17:05 Ortszeit über die
Geräteanbindung gemessen**, nicht erinnert. Wo etwas erschlossen ist, steht es
dabei.

---

## Block 1 — Der Stand in drei Zeilen

| | |
|---|---|
| **Fertig** | Register **23** (VT, tagesgenau), **24 + 24.6** (MtM), **25** (Konjunktion) stehen vollständig · Doku aufgeräumt (BACKLOG −24 %, Epics ausgelagert, Journal vollständig, Nachtragsordner leer) · Nachtragswächter grün und per Cron täglich 04:50 · `ARBEITSWEISE.md` hat **Abschnitt 0**, die Ausgabe-Checkliste (TB-69) |
| **Läuft** | **TB-77** — Registerabschnitt **26**: Datenhorizont je Bot, `asof`, der Grenzfall. ⭐ **Mit einem Nachtrag**, der zwei Blocker des ursprünglichen Auftrags aufhebt (siehe Block 7) |
| **Als Nächstes** | **TB-78** (Sichtschutz als Abschnitt 27 · Falten nach 4a · Faltenplan als Registertext) → **TB-30b** (vier Optimierer + Fables Wache) → **Sperrlisten-Vollzug** → **der signierte Tag** |

---

## Block 2 — `HEAD`, Zweig, Commit-Kette

```
HEAD    2e9cdf9   Zweig main
Baum    0 geändert · 1 unversioniert: .claude/settings.local.json
```

⚠️ Die eine unversionierte Datei ist **kein** Arbeitsstand, sondern lokale
Werkzeugkonfiguration — Kandidat für `.gitignore`, bisher nicht entschieden.

**Kette des 21.09., von früh nach spät:**
`ff2e5ab` → `9a51add`/`f0ca921` (TB-64 Abgabe) → `f1124ba`…`c96c208` (TB-75) →
`f2e0a68`…`437428d` (TB-63) → `6f5f986`…`3c25d94` (TB-76) →
`495b7fc`…`1ded755` (TB-69) → `9250570` (TB-77 Schritt 0) → **`2e9cdf9`**
(TB-77, während Schritt 1).

---

## Block 3 — Die tragenden Zahlen, jede mit Fundstelle

| Grösse | Wert | Fundstelle |
|---|---|---|
| ⭐⭐ **`asof`** | **2026-09-19** | Register **Z. 2594**, `zeitpunkt_utc 2026-09-19T06:49:32+00:00`; als Regel: Fable 21b, Registertext 5a Ergänzung |
| **Datenende** | **15.09.2026** (Kursdaten), vier Tage vor `asof` | Fable 21b; gehört als eigenes Manifestfeld `datenende` ins `MANIFEST.json` — ⛔ **noch nicht eingetragen** |
| **Das Register** | `docs/VORREGISTRIERUNG_neuselektion.md` · **4 216 Zeilen · 254 698 B** | gemessen; ⚠️ **der Dateiname enthält nicht das Wort „Register"** — wer danach sucht, findet ihn nicht |
| **Höchster Abschnitt** | **25** (26 entsteht gerade in TB-77) | `grep -nE "^#+ *2[0-9]\."` |
| **`BACKLOG.md`** | 602 Zeilen · 204 879 B | |
| **`ARBEITSWEISE.md`** | 1 428 Zeilen · 80 018 B, mit Abschnitt 0 | TB-69 |
| **`JOURNAL.md`** | 8 058 Zeilen, letzter Block **CE** | TB-69 Schritt 5 |
| **Nachtragsordner** | **0** offene Nachträge | |
| **Sperrlisten-Hashes** | `a163c498…` · `0e54ac5c…` · `4549395f…` | unverändert seit 20.09. |

### ⚠️⚠️ Die Falle, die diesen Chat beinahe erwischt hat

**Es gibt sechs Dateien `faltenplan*.json` im Repo, und nur eine steht auf der
Sperrliste.**

| Datei | SHA-256 | Grösse | |
|---|---|---|---|
| `research/vorregistrierung/ergebnisse/faltenplan.json` | **`0e54ac5c…`** | 18 736 B | ⛔ **gesperrt** (Register Abschnitt 10, Punkt 2 nennt `ergebnisse/faltenplan.json`) |
| `research/faltenplan_neun/daten/faltenplan.json` | `93fbf09c…` | 262 871 B | nicht gesperrt (TB-56) |
| `research/vorregistrierung/ergebnisse/faltenplan_tb72.json` | `19e8cbca…` | 37 320 B | der neue Plan, daneben |
| `research/faltenplan_neun/daten/faltenplan_ohne_schranke.json` | `19632d13…` | 454 637 B | |
| `research/krypto_historie/daten/faltenplan_nach_tb34.json` | `ecbb9988…` | 15 364 B | |
| `docs/belege/TB-72/faltenplan_4a_stand_vor_tb72.json` | `73f4ee39…` | 33 883 B | Beleg |

⭐ **Regel daraus:** *Eine Sperrlisten-Datei wird nie mit ihrem blossen
Dateinamen geprüft, immer mit dem vollen Pfad.* Ein `find -name faltenplan.json
| head -1` trifft die falsche.

### Sichtschutz — zwei Messungen vom 21.09.

| | |
|---|---|
| ✅ **Das Register ist rein** | 24 Sharpe-Erwähnungen, **alle Regeltext** (Schwellen `≤ 0`, die Formel, *„keine Mindestzahl Trades"*, Plateau-Regel). **Keine gemessene Kennzahl je Parametersatz.** ⇒ Fables Annahme *„das Register hat sein Tor schon"* hält, jetzt belegt |
| ⚠️ **`BACKLOG.md` ist nicht rein** | Keine Kennzahlen, aber **Erwartungen über den Ausgang**: **Z. 190 `W14`** *„Plausibel ist, dass die Mehrzahl der neun Bots auf Schatten landet…"* und **Z. 170 `T39.2`** mit einer Sharpe-Schwelle. ⇒ Fables Selbstbeschränkung bleibt, mit Grund statt aus Unkenntnis |

---

## Block 4 — Offen vor dem signierten Tag, in Reihenfolge

⭐ **Die Reihenfolge ist Fables, aus 21b, und sie ist begründet:**
*„Der Faltenplan … wartet nicht auf den Tag; er muss vor ihm fertig sein, weil
die Falten Registertext sind."*

| | Schritt | warum hier |
|---|---|---|
| **1** | **TB-77 zu Ende** — `asof` als Tatsachennotiz, Horizontbeginn je Bot | läuft |
| **2** | **TB-78** — Sichtschutz als **Abschnitt 27** · Falten nach 4a ableiten · **Faltenplan als Registertext** | Falten sind Registertext |
| **3** | **TB-30b** — die vier `multi_symbol_optimise.py` (`entry_cutoff` einmal je Bot aus dem Register statt je Symbol aus `df["open_time"].max()`) **plus Fables Wache** (frühester Einstieg ≥ Horizontbeginn, sonst rc 2) | ⚠️ **Code im Selektionspfad.** Eine Änderung daran **nach** dem Tag wäre ein Amendment |
| **4** | **Sperrlisten-Vollzug** über alle neun Bots | braucht eine **eigene Betreiberfreigabe** (Register 21.9) |
| **5** | **Der Tag** | |

**Daneben, nicht blockierend:** `TB-70` (`BACKLOG.md` Abschnitt 2, 107 135 B,
grösster Einzelposten) · `T56b.6` (Konstantenkopien) · `T56b.7` · `T46.1b/c` ·
die zwei roten Proben `G6`/`H3` · die Kettenzeile `0,99`.

---

## Block 5 — Wartezustände

| wartet | worauf |
|---|---|
| **TB-77** | auf nichts — der Nachtrag ist eingefügt, die Sitzung arbeitet |
| ⚠️⚠️ **Fable** | auf **zwei** Dinge: unsere Antwort zur Sichtschutzfrage (Option 1 + drei Handwerksauflagen + zwei Ergänzungen) **und** auf unsere Rückfrage, ob der Sichtschutz **rückwirkend** für seinen bisherigen Chatinhalt gilt |
| **Betreiber** | nichts offen |

⛔ **Die offene Rückfrage an Fable ist nach `UMZUG.md` Abschnitt 3 eine
Umzugssperre.** Erst die Antwort, dann der Umzug.

---

## Block 6 — Freigaben und Sperrliste

| | |
|---|---|
| **Aktive Freigabe für eine Sperrlisten-Datei** | **keine** |
| **Sperrlisten-Vollzug neun Bots** | steht aus, braucht **eigene** Freigabe (Register 21.9) — ⚠️ *Freigaben verfallen nicht von selbst; diese wurde nie erteilt* |
| **`auswertung.py`** | eingefroren (Register Z. 31). ⭐ Fable hat seine eigene Ausnahme dafür am 21.09. **zurückgezogen**: *„Mein Vorschlag ‚in den Auswerter' war falsch adressiert."* |
| **Die drei Hashes** | unverändert seit 20.09. — Werte in Block 3 |

---

## Block 7 — ⭐⭐ Die Fehler dieses Chats und die Regeln daraus

| | Fehler | Regel |
|---|---|---|
| **1** | **Ein Auftrag lief mit einer überholten Prämisse.** TB-77 wies an, für `asof` einen **Platzhalter** ins append-only-Register zu schreiben — während der Wert seit dem 19.09. als Tatsache dort stand. Fables Antwort 21b hob den Blocker auf, nachdem der Auftrag schon lief | ⭐ **Nach jeder Fable-Antwort werden die laufenden Aufträge gegen sie geprüft, nicht nur die kommenden.** Ein Nachtrag in die laufende Sitzung ist billiger als eine Berichtigung im Register |
| **2** | **Eine Kette mit falschem Aktenzeichen in einen Auftrag geschrieben:** „(b) → Festlegung 11 → 6b → Schatten". Fable hat 21b klargestellt, dass **keine** Festlegung diesen Satz trägt | ⭐ **Fables eigene Regel, auf uns angewandt:** wo ein Aktenzeichen genannt wird, steht der Wortlaut daneben |
| **3** | **Einen Übergabetext an Fable gesendet, dessen vier Fragen er bereits beantwortet hatte** — die Antwort lag, als er rausging, seit einer Stunde vor | ⭐ **Ein Übergabetext bekommt eine Fassungszeile im Sendetext selbst**, nicht nur im Rahmendokument. Sonst ist von aussen nicht unterscheidbar, welche Fassung jemand hat |
| **4** | **Fables Annahme fast ungeprüft übernommen** — *„das Register hat sein Tor schon"*. Sie stimmt, aber das war beim Übernehmen nicht gemessen | ⭐ **Die Prüfung, die wir von einer Datei verlangen, gilt auch für die Datei, die wir für unverdächtig halten.** Gleiche Sonde, beide Dateien |
| **5** | **Einen Sperrlisten-Hash beinahe falsch gemeldet** — `find -name faltenplan.json | head -1` traf eine andere Datei desselben Namens | ⭐ Block 3, die Falle: **voller Pfad, nie der blosse Name** |

⚠️ **Und die Fehler, die die Gegenseite gemacht hat, damit der neue Chat sie
erwartet:** Fable hat am 21.09. zwei Aktenzeichen um eins verschoben, auf ein
Dokument verwiesen, das uns nie erreichte, und eine Wache in eine eingefrorene
Datei legen wollen. **Alle drei hat er auf Vorhalt zurückgenommen und den Grund
selbst genannt:** *„Ich habe es nicht nachgeprüft, weil ich das Register nicht
lesen kann — das ist der Grund für den Fehler, nicht eine Entschuldigung
dafür."*

---

## Block 8 — Was zwischengelagert und noch nicht eingearbeitet ist

| | Wo es liegt | Zielort |
|---|---|---|
| ⚠️ | `logs/auftraege/TB-58b_v2.md` (19.09.) | **offene Bringschuld ins Repo** — `logs/` ist gitignoriert, also kein Träger |
| ⚠️⚠️ | **Sechs Dokumente nur in der Projektablage, nicht im Repo** — weil `docs/` gesperrt ist, solange TB-77 läuft: `FABLE_ANTWORT_2026-09-20a`, `-21b`, `-21c`, `-21d`, `-21e`, `-21f`, dazu `FABLE_UEBERGABE_2026-09-21_neuer_chat.md` **Fassung 2** und dieser Nachtrag | **TB-78 zieht sie ins Repo nach** |
| | `.claude/settings.local.json` unversioniert | `.gitignore`-Entscheidung offen |

### Regeln, die in diesem Chat vereinbart wurden — abgeglichen, nicht erinnert

⭐ `UMZUG.md` Schritt 2 verlangt den Abgleich gegen `ARBEITSWEISE.md`. Ergebnis:

| | Regel | Stand |
|---|---|---|
| ✅ | Entscheidungen als anklickbare Frage **mit Empfehlung** · Kopierblöcke getrennt · Sitzungsende wird so vorgegeben wie der Anfang · kein Editor-Befehl ohne den Weg heraus | **stehen bereits** in `ARBEITSWEISE.md` (Abschnitt 0 und 6b/6d, TB-69) — **nichts nachzutragen** |
| ⛔ | **Fables Sichtschutz** — keine Ergebnisgrössen des Selektionsraums vor dem Tag | **neu, noch nirgends eingetragen** → Register **Abschnitt 27** (TB-78) |
| ⛔ | **Unsere Gegenprüfung dazu** — Fables Begründungen daraufhin lesen, ob sie Zahlen enthalten, die er nicht haben dürfte | **neu** → `PRUEFPRINZIPIEN.md` (TB-78). *Begründung: `A4` — eine Wache, die niemand ausführt, ist keine Wache; sein Leseprotokoll ist eine Selbstauskunft* |

---

## Block 9 — Der Eröffnungstext für den neuen Chat

⭐ **`UMZUG.md` Abschnitt 6, unverändert gültig.** Kein zweiter Text hier — die
beiden Fassungen würden vom ersten Commit an auseinanderlaufen (TB-68).

⚠️ **Eine Ergänzung zum Eröffnungstext, nur für diesen Umzug**, als zusätzlicher
Absatz anzuhängen:

```
Zusatz fuer diesen Umzug: Lies in UEBERGABE_2026-09-19.md zuerst NACHTRAG 4
samt seinen beiden Ergaenzungen (ganz am Ende) - das ist der Stand vom 21.09.,
17:40; die Bloecke 1-9 davor sind der Stand vom 20.09. und in allem ueberholt,
was der Nachtrag anders sagt. Ergaenzung 2 enthaelt die Abschlusspruefung nach
TB-77 und die vollstaendige Liste fuer TB-78 - das ist deine erste Aufgabe.
Danach drei Dateien, in dieser Reihenfolge:
  projektfuehrung/FABLE_ANTWORT_2026-09-21b_asof_und_wache.md   (asof)
  projektfuehrung/FABLE_ANTWORT_2026-09-21d_sichtschutz.md      (Sichtschutz)
  projektfuehrung/FABLE_ANTWORT_2026-09-21g_sichtschutz_nullpunkt.md
                                          (Abschnitt 27 im Wortlaut)
An diesen drei Entscheidungen haengt alles Weitere.
```

---

## Was der neue Chat als Erstes tun muss

| | |
|---|---|
| **1** | **Die Geräteanbindung prüfen** — `HEAD` und eine Zeilenzahl als Beleg. *„Die Tools sind da" ist kein Beleg* (`UMZUG.md` Abschnitt 8) |
| **2** | **TB-77 nachmessen:** gibt es `docs/ERGEBNIS_TB-77_horizont_je_bot.md`? Ist der Baum sauber? Steht Registerabschnitt 26? ⚠️ Solange die Sitzung läuft: **nichts nach `docs/` schreiben**, nur nach `logs/auftraege/` |
| **3** | **Fables offene Rückfrage abschliessen** (Block 5) — sie ist die zweite Umzugssperre und darf nicht mit dem alten Chat verschwinden |

---

## In einfacher Sprache

**Wo wir stehen:** Die Spielregeln für den grossen Auswahllauf sind fast
fertig. Heute sind vier Regelblöcke dazugekommen; der fünfte wird gerade
geschrieben. Danach fehlen noch drei Schritte bis zu dem Moment, in dem die
Regeln versiegelt werden und der Lauf beginnen darf.

**Was heute inhaltlich entschieden wurde:** Woher das Stichtagsdatum kommt
(vom Zeitpunkt, an dem der Datenbestand eingefroren wurde — nicht vom
Versiegeln selbst). Dass eine Kontrollzeile nicht in eine eingefrorene Datei
darf. Und dass der Verfahrensprüfer vor dem Versiegeln keine Ergebniszahlen
sehen darf — weil sonst später niemand mehr beweisen kann, dass eine Regel
nicht nach dem Ergebnis gewählt wurde.

**Warum noch nicht umgezogen wird:** Es läuft eine Sitzung am MacBook, und eine
Frage an den Prüfer ist offen. Das eigene Umzugsverfahren verbietet beides
ausdrücklich — ein Umzug in diesem Moment würde genau das kosten, was er
verhindern soll.

---

## Ergänzung zu Nachtrag 4 — 21.09.2026, 17:25 Ortszeit

**Fable hat geantwortet** (`FABLE_ANTWORT_2026-09-21g_sichtschutz_nullpunkt.md`).
⭐ **Damit fällt Umzugssperre 2 aus Block 5 weg.** Es bleibt nur noch TB-77.

### Was 21g entscheidet

| | |
|---|---|
| ⭐⭐ | **Registerabschnitt 27 liegt im Wortlaut vor** — 27.1 bis 27.5 samt Tatsachennotiz. Er ist in TB-78 **zeichengleich** einzutragen, nicht nachzuformulieren |
| ⭐ | **Die Regel ist um eine Klasse gewachsen:** 27.1 verbietet jetzt auch **Erwartungen, Schätzungen und Prognosen** über den Ausgang, „gleich ob als Zahl oder als Satz". Das kam aus unserer Messung 2 — ⭐ *aus der **Art** des Fundes, nicht aus seinem Inhalt; die Regel wäre dieselbe, hätte die Zeile das Gegenteil erwartet* |
| ⭐ | **Neu, 27.5:** *„Wer dem Verfahrensprüfer einen Treffer nach 27.1 in einer Datei meldet, nennt Datei und Fundstelle, nicht den Inhalt."* |
| ⭐ | **Der Nullpunkt:** Die Protokollkette beginnt **nicht** mit 21d, sondern mit der Tatsachennotiz zu 27, die Fables Wissensstand beim Inkrafttreten abzählt — vier Dateien, alle in der Ablage, alle wörtlich. *„Ein älterer Chat hätte diesen Vorteil nicht gehabt."* |
| | **Rückwirkung:** kein Pflichtenrückbau, sondern **Bestandsaufnahme** — *„Was ich beim Inkrafttreten wusste, wird festgehalten, nicht bewertet."* Für den Vorgängerchat gilt: seine Entscheidungen sind registriert, die Reihenfolge Regel → Messung steht im Register selbst (24.3 vor 24.6) |

### ⚠️ Ein sechster Fehler für Block 7 — meiner

| | Fehler | Regel |
|---|---|---|
| **6** | **Ich habe Fable den Inhalt des Sichtschutz-Treffers zitiert statt seiner Fundstelle.** `BACKLOG.md` Z. 190 wörtlich in die Antwort gesetzt — damit kennt er die Erwartung, die er nicht kennen sollte. Er hat es selbst gemeldet und in die Tatsachennotiz eingetragen: *„Durch das Zitat kenne ich die Zeile jetzt."* | ⭐⭐ **Registertext 27.5, jetzt Regel:** Fundstelle statt Inhalt. ⚠️ *Ich habe den Sichtschutz beim Melden des Sichtschutz-Verstosses selbst verletzt — die Fehlerklasse, gegen die A1 und B1 gebaut sind: wer prüft, fasst an* |

### Eine Handwerksentscheidung, die 21g offenlässt

Fable fragt, ob die Pflicht aus 27.4 (seine Begründungen gegen verbotene Grössen
prüfen) ein **eigenes** Prüfprinzip wird oder unter `A4` fällt — *„Handwerk, eure
Wahl."*

⭐ **Entschieden: eigenes Prinzip.** `A4` trifft einen Test, der dauerhaft
dieselbe Farbe zeigt; hier geht es um eine **Selbstauskunft, die niemand
gegenprüft** — eine andere Fehlerklasse, die unter `A4` unsichtbar bliebe.

> **`A5` (neu, für `PRUEFPRINZIPIEN.md`, TB-78):** *Eine Selbstauskunft ist erst
> dann eine Wache, wenn ein anderer sie gegenprüfen kann. Wo keine Gegenprüfung
> möglich ist, wird die Prüfung auf das verlagert, was nach aussen sichtbar ist
> — bei Fable: seine Begründungen, nicht sein Leseprotokoll.*

### Was TB-78 dadurch zusätzlich trägt

| | |
|---|---|
| **1** | Registerabschnitt **27**, zeichengleich aus 21g |
| **2** | `PRUEFPRINZIPIEN.md`: **`A5`** |
| **3** | Die **acht** Dokumente aus der Projektablage ins Repo (Block 8 nennt sieben; `FABLE_ANTWORT_2026-09-21g` kommt dazu) |
| **4** | Danach erst: die Register-**KOPIE** in die Ablage, mit Commit-Hash, Datum und der Kennzeichnung KOPIE im Kopf |

### Block 5 in der Fassung von 17:25

| wartet | worauf |
|---|---|
| **TB-77** | auf nichts |
| ✅ **Fable** | **auf nichts** — 21g beantwortet beide offenen Punkte. Nächste Frage an ihn erst, wenn der Faltenplan als Registertext steht |
| **Betreiber** | nichts offen |

⇒ ⭐ **Von den zwei Umzugssperren steht nur noch TB-77.** Sobald
`docs/ERGEBNIS_TB-77_horizont_je_bot.md` im Repo liegt und der Baum sauber ist,
ist der Umzug nach `UMZUG.md` Abschnitt 3 zulässig.

---

## Ergänzung 2 zu Nachtrag 4 — 21.09.2026, 17:40: die Abschlussprüfung nach TB-77

**TB-77 ist abgegeben.** `HEAD 83e3a85`, Zweig `main`, Baum sauber (0 geändert,
1 unversioniert: `.claude/settings.local.json`).

| Prüfung | Ergebnis |
|---|---|
| Ergebnisdokument | `docs/ERGEBNIS_TB-77_horizont_je_bot.md`, 13 145 B ✅ |
| Register append-only | `numstat` **330 / 0** ✅ |
| Abschnitt 26 | steht, Z. 4226, sieben Unterabschnitte ✅ |
| Sperrlisten-Hashes | `a163c498…` · `0e54ac5c…` · `4549395f…` **unverändert** ✅ |
| Nichts ausserhalb `docs/` | 0 Dateien ✅ |
| Abschnitt 27 | noch nicht da — richtig, er gehört zu TB-78 ✅ |

---

### ⛔ Befund 1 — der Nachtrag zu TB-77 ist nie angekommen

**Gemessen:** `grep` über Ergebnisdokument und `docs/belege/TB-77/` nach
*„Nachtrag zu TB-77"* und `FABLE_ANTWORT_2026-09-21b` — **0 Treffer.** Die
Sitzung hat durchgehend gegen die ursprüngliche Auftragsfassung gearbeitet.

**Folge im Register, append-only und damit dauerhaft sichtbar:**

| | Stelle | steht dort | richtig ist |
|---|---|---|---|
| **1** | **26.3** | *„⚠️ [PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]"*, für alle vier Aktien-Bots | `asof` = **2026-09-19** (Fable 21b, Registertext 5a Ergänzung); Horizontbeginn je Bot ableitbar |
| **2** | **26.6** | *„`asof` setzen. Wann und wodurch, ist Fables Frage (1) im neuen Chat; die Lesart ‚mit Snapshot und Tag zugleich' ist **nicht entschieden**"* | **entschieden** seit 21b: durch den Snapshot, nicht durch den Tag |
| **3** | „Offen" im Ergebnisdokument | *„Wache samt Mutationsprobe in `auswertung.py`"* | Fable hat das 21b **zurückgezogen**: die Wache geht in die vier Optimierer (TB-30b) |

⇒ **Alle drei sind in TB-78 als Berichtigung nachzutragen** — append-only, mit
ERSETZT-Marke, nicht durch Überschreiben.

---

### ⭐⭐ Befund 2 — Fables Berichtigung war falsch, und der Auftrag hatte recht

**Die Sitzung hat `registerdaten.FESTLEGUNGEN` selbst gelesen. Wortlaut:**

```
10: ('DSR-Basis', 'N = 653, dieser Lauf zaehlt dazu')
11: ('DSR ist Bericht, nicht Tor', 'Bleibt-Geht laeuft ueber die Abbruchkriterien')
12: ('Das zulaessige Ergebnis', 'Es kann sein, dass kein einziger Bot die Schwelle
     erreicht. Eine Aussage ueber den Backtest, nicht ueber die Bots.')
```

⭐⭐ **Festlegung 11 trägt den Satz sehr wohl** — als zweiten Teil desselben
Eintrags. Fables Satz in 21b, *„wo ich ‚Festlegung 10' für den Satz ‚Bleibt/Geht
läuft über die Abbruchkriterien' angeführt habe, trägt **keine** Festlegung
diesen Satz"*, ist damit **falsch**. Richtig ist die Kette, wie sie in **26.7**
steht und dort nachgemessen belegt ist:

> **(b), Abschnitt 7 → Festlegung 11 → Registertext 6 (b), 16.4 → Schatten**
> — und Festlegung 12 deckt „mehrere oder alle".

⚠️⚠️ **Und das heisst:** Hätte mein Nachtrag die Sitzung erreicht, hätte sie
Festlegung 11 aus der Kette **entfernt** — auf Fables Autorität, gegen die
Quelle. **Das Nichtankommen hat einen Registerfehler verhindert.**

### ⚠️ Ein siebter Fehler für Block 7 — meiner, und der teuerste

| | Fehler | Regel |
|---|---|---|
| **7** | **Ich habe Fables Berichtigung ungeprüft in einen Auftrag geschrieben.** Er korrigierte unser „Festlegung 11" zu „keine Festlegung"; ich habe das übernommen, obwohl er im selben Absatz sagt, er *könne das Register nicht lesen*. Der Auftrag hätte die richtige Kette zerstört | ⭐⭐ **Eine Berichtigung von Fable wird gemessen wie jede andere Behauptung — gerade dann, wenn sie uns berichtigt.** Wer sagt „ich kann die Quelle nicht lesen", liefert damit den Grund, seine Quellenangabe zu prüfen, nicht sie zu übernehmen |

⭐ **Dasselbe Muster wie Fehler 4** (Fables Annahme über das Register beinahe
ungeprüft übernommen) — nur ist es hier durch Zufall gutgegangen. **Zweimal an
einem Tag dieselbe Klasse.**

---

### Was TB-78 dadurch trägt — die vollständige Liste

| | |
|---|---|
| **1** | **Berichtigung zu 26.3** — `asof` = 2026-09-19 mit Fundstelle (Register Z. 2594), Horizontbeginn je Bot als absolutes Datum, Registertext 5a Ergänzung zeichengleich aus 21b. Der Platzhalter bleibt stehen, mit ERSETZT-Marke |
| **2** | **Berichtigung zu 26.6** — die drei Zeilen, die `asof` als offen führen |
| **3** | **Registerabschnitt 27**, zeichengleich aus 21g (27.1–27.5 samt Tatsachennotiz) |
| **4** | **`PRUEFPRINZIPIEN.md`: `A5`** — *eine Selbstauskunft ist erst dann eine Wache, wenn ein anderer sie gegenprüfen kann* |
| **5** | **`ARBEITSWEISE.md`:** die zwei Regeln aus Block 8 (Fable-Rückfragen mit Empfehlung · beim Übergeben sagen, was mitgeht) |
| **6** | **Acht Dokumente aus der Projektablage ins Repo** — `FABLE_ANTWORT_2026-09-20a`, `-21a`, `-21b`, `-21c`, `-21d`, `-21e`, `-21f`, `-21g`, dazu `FABLE_UEBERGABE…` Fassung 2 und diese Übergabe. ⚠️ Die Sitzung hat selbst gemeldet: *„Die Datei liegt nicht im Repo (`find` 0)"* |
| **7** | **Korrektur der „Offen"-Liste** — die Wache gehört nicht in `auswertung.py` |
| **8** | Danach: **Falten nach 4a** und **Faltenplan als Registertext** |
| **9** | Erst ganz am Ende: die Register-**KOPIE** in die Ablage (Commit-Hash, Datum, KOPIE) |

### Zwei Befunde der Sitzung, die wir übernehmen

| | |
|---|---|
| ⭐ | Mein Auftrag nannte **16.3** als Fundstelle für *„asof kommt aus dem Register, nie aus der Uhr"* — der Satz steht in **17.1**; 16.3 (a) ist die ersetzte Fassung. Von der Sitzung gefunden, nicht von mir |
| ⭐ | `FABLE_ANTWORT_2026-09-21a` liegt **in keinem Träger** ausser der Projektablage — TB-78 Punkt 6 |

### Block 5 in der Fassung von 17:40

| wartet | worauf |
|---|---|
| **Mac-Sitzung** | keine läuft |
| ⚠️ **Fable** | auf **eine Berichtigung**: Festlegung 11 trägt den Satz doch, mit Wortlaut aus `registerdaten.FESTLEGUNGEN`. Das ist die dritte Berichtigung an ihn heute und die erste, bei der er **uns** falsch berichtigt hat |
| **Betreiber** | Start von TB-78 |

---

## Ergänzung 3 zu Nachtrag 4 — 21.09.2026, 17:50: 21h geschlossen, 21c aufgearbeitet

### 21h — Fable nimmt vollständig zurück ✅

*„Festlegung 11 hat **zwei Teile** … **21b (1): ‚keine Festlegung trägt diesen
Satz' war falsch. Zurückgenommen.**"* Die Kette in 26.7 steht richtig und bleibt.
Seine neue eigene Regel, schärfer als die aus 21b:

> *„Ein Aktenzeichen gilt mir als vorgelegt, wenn der **ganze Eintrag** vorliegt
> — bei `FESTLEGUNGEN` also beide Felder des Tupels. Aus einem Teilzitat
> schliesse ich nichts über das, was nicht zitiert ist."*

Und zu unserer Regel: *„Meine Berichtigungen sind Behauptungen. Dass ich das
Register nicht lesen kann, macht meine Quellenangaben schwächer als eure, nicht
stärker … ich möchte, dass ihr sie anwendet."* Damit ist **21c 3.3
gegenstandslos** — der gemeldete Widerspruch war keiner.

---

### ⚠️⚠️ 21c trug zwei Entscheidungen, die bis jetzt unbearbeitet lagen

**Sie stehen vor dem Ableiten der Falten, nicht danach.** Fables eigene
korrigierte Reihenfolge:

> asof eintragen → Horizontbeginn je Bot → **3.1 eintragen, 3.2 messen und
> eintragen** → Falten nach 4a ableiten → Faltenplan als Registertext → Tag

#### 3.1 — Ein Registersatz ist beim Umschreiben verlorengegangen

Die 4a-Fassung vom 20.09. (20e) endete mit: *„Der Vorlauf wird gegen dieses
Datum gerechnet, nicht gegen den ersten Kurs im Bestand."* Die Fassung vom
21.09. (21a) trägt *„ersetzt die Fassung vom 20.09."* und **enthält den Satz
nicht mehr** — ohne dass irgendwo ein Grund dafür steht.

⭐ **Gemessen 21.09., 17:48 — der Befund trifft, und schärfer als Fable ahnte:**
Der Satz steht im Register **genau einmal**, in **Z. 4307** — und zwar
**innerhalb des Zitats der als ersetzt markierten Fassung** in 26.2. Er steht
also im Register ausschliesslich als Teil dessen, was ausser Kraft ist.

**Fables Entscheidung, einzutragen:**

> **4a, Präzisierung, Ergänzung:** Der Indikator-Vorlauf nach (i) wird gegen den
> Horizontbeginn des Bots gerechnet, nicht gegen den ersten Kurs im Bestand. Der
> Satz aus der Fassung vom 20.09. gilt fort; die Fassung vom 21.09. hat ihn
> nicht ersetzt, sondern ausgelassen.

*Kategorie: Berichtigung (Registertext an Registertext).* Sein Grund: *„Ein
Vorlauf, der auf Kursen vor dem Horizontbeginn rechnet, ist derselbe Zugriff",*
den 26 verbietet.

#### 3.2 — Die Lücke zwischen Horizontbeginn und dem 1. Januar

Der Horizontbeginn ist der **19.09.2016**; die erste Falte beginnt an einem
1. Januar. Dazwischen sind Einstiege nach 26 **zulässig**, tauchen in keiner
Falte auf und laufen durch den Kapitalpfad — *„genau der Schaden, mit dem (d)
begründet wurde, nur kürzer."* ⚠️ **Fables Wache aus 21b sieht das nicht**, weil
sie gegen den Horizontbeginn prüft.

**Sein Registertext-Vorschlag, Regel vor der Messung (Bauart 24.3):**

> **Zu 4a / 26:** Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten
> Selektionsfalte mit dem registrierten Startkapital und ohne offene Position.
> Kein Einstieg liegt vor diesem Datum. Die Grösse der Wirkung ist für diese
> Regel ohne Belang.
>
> **Wache (TB-30b), angepasst:** frühester Einstieg ≥ **Beginn der ersten
> Selektionsfalte** (nicht nur ≥ Horizontbeginn). Der Bericht führt je Bot drei
> Daten nebeneinander: Horizontbeginn, Beginn der ersten Falte, frühester
> Einstieg.

⇒ ⭐⭐ **TB-30b ändert sich dadurch.** Die Fassung aus 21b (nur Horizontbeginn)
ist überholt; die aus 21c 3.2 gilt.

**Gemessen zu seiner Frage „regelt das Register den Beginn des Kapitalpfads
schon?":** Nein. Einziger Treffer ist **Z. 4296**, und der beschreibt den
Schaden, nicht die Regel: *„der Kapitalpfad (Registertext 1a) beginnt die erste
Falte mit einem Kapitalstand, der aus nicht registrierten Jahren stammt."*
`Startkapital` kommt im Register **nicht vor**. ⇒ Sein Vorschlag ist **neuer
Registertext**, keine Berichtigung.

---

### ⛔ Was NICHT messbar war — `A2`, als eigenes Ergebnis

Fable bat: *„Bitte messen, ob `faltenplan.json` (0e54ac5c…) den Vorlauf gegen
den Horizontbeginn rechnet."* **Das lässt sich an dieser Datei nicht
beantworten, und der Grund ist wichtiger als die Frage:**

| | gemessen |
|---|---|
| ⚠️ | Der gesperrte Plan führt je Falte ein Feld **`training_bis_ausschliesslich`** (z. B. `2018-12-14`) und **`embargo_tage: 18`**. ⭐⭐ **Verfahren B hat ausdrücklich KEIN Trainingsfenster.** Die Datei stammt aus einem anderen Verfahrensstand |
| ⚠️ | Erste Selektionsfalte `turtle_soup_stocks` im gesperrten Plan: **2019** — nicht 2017 oder 2018, wie Fables Frage unterstellt |
| ⚠️ | TB-72 hat einen neuen Plan **daneben** gelegt (`faltenplan_tb72.json`, `19e8cbca…`); der gesperrte ist unberührt, aber nicht der Plan nach 4a |

⚠️ **Und eine Berichtigung an mich selbst, innerhalb derselben Stunde:** Meine
erste Sonde meldete für die vier Aktien-Bots *„Jahre im Eintrag: 2018, 2019,
2020"* und legte damit 2018 als erste Falte nahe. Falsch — die **2018** stammte
aus `training_bis_ausschliesslich`, nicht aus einer Falte. Erst das Auslesen der
ganzen Struktur hat es gezeigt. ⭐ *Eine Sonde, die auf Jahreszahlen im
Rohtext sucht, misst nicht das Feld, das sie zu messen glaubt.*

---

### ⚠️ Ein systemischer Befund aus 21c 3.3 — unsere Hälfte des Austauschs fehlt

Fable hält fest, dass unsere **Rückmeldung vom 21.09., 16:24 in keinem Träger
liegt** — *„nicht wegen eines Fehlers, sondern weil sie fehlt."*

⭐⭐ **Gemessen an der Projektablage: Das gilt für fast alles von unserer
Seite.** Fable legt seine Antworten ab (20a–21h, neun Dateien); von uns liegt
**eine einzige** Anfrage dort (`FABLE_ANFRAGE_2026-09-21a`). Die Rückmeldung
16:24, die Sichtschutz-Antwort und die Festlegungs-11-Berichtigung von 17:36
existieren nur im Chatverlauf — **und der ist kein Träger** (`UMZUG.md`
Abschnitt 2).

> ⭐ **Regel, neu:** *Jede Anfrage und jede Rückmeldung an Fable wird abgelegt wie
> seine Antwort* — `projektfuehrung/FABLE_ANFRAGE_<datum><buchstabe>_<stichwort>.md`.
> Ein halb abgelegter Austausch ist im Streitfall schlechter als keiner: Er sieht
> vollständig aus.

⇒ **TB-78 legt die drei fehlenden Stücke nach**, aus dem alten Chat, solange er
offen ist.

---

### TB-78 — die Liste in der Fassung von 17:50

| | | |
|---|---|---|
| **1** | Berichtigung **26.3** — `asof` = 2026-09-19, Horizontbeginn je Bot | neu gegenüber 17:40 |
| **2** | Berichtigung **26.6** — `asof` ist nicht mehr offen | |
| **3** | **Abschnitt 27**, zeichengleich aus 21g | |
| **4** | ⭐ **4a-Ergänzung aus 21c 3.1** — der Vorlauf-Satz gilt fort | ⚠️ **neu** |
| **5** | ⭐ **Neuer Registertext aus 21c 3.2** — Kapitalpfad ab 1. Januar der ersten Falte | ⚠️ **neu**, kein Berichtigungsfall (gemessen) |
| **6** | `PRUEFPRINZIPIEN.md`: **`A5`** | |
| **7** | `ARBEITSWEISE.md`: die drei Regeln (Fable-Rückfragen mit Empfehlung · beim Übergeben sagen, was mitgeht · **jede Anfrage an Fable ablegen**) | ⚠️ dritte ist neu |
| **8** | **Neun Fable-Dateien + drei eigene Anfragen/Rückmeldungen** ins Repo und in die Ablage | erweitert |
| **9** | Korrektur der „Offen"-Liste aus TB-77 — die Wache gehört nicht in `auswertung.py`, und sie prüft gegen die **erste Falte**, nicht gegen den Horizontbeginn | erweitert |
| **10** | **Erst danach:** Falten nach 4a · Faltenplan als Registertext · Register-KOPIE in die Ablage | |

### Block 5 in der Fassung von 17:50

| wartet | worauf |
|---|---|
| **Mac-Sitzung** | keine läuft; Baum sauber, `HEAD 83e3a85` |
| ⚠️ **Fable** | auf **eine Messmeldung**, noch nicht gesendet: (a) 3.1 trifft, Fundstelle Z. 4307, der Satz steht nur im ersetzten Zitat; (b) das Register regelt den Kapitalpfad-Beginn nicht, 3.2 ist neuer Text; (c) `faltenplan.json` beantwortet seine Frage nicht — Trainingsfenster-Felder, erste Falte 2019. ⭐ **Das ist eine Verfahrensmessung nach 27.2, keine Ergebnisgrösse** |
| **Betreiber** | Umzug in den neuen Chat, dann TB-78 |

⚠️ **Zum Umzug:** Die Messmeldung an Fable ist **noch nicht gestellt**, also ist
keine Rückfrage offen im Sinn von `UMZUG.md` Abschnitt 3 — es ist eine
dokumentierte Aufgabe, die der neue Chat als Erstes erledigt. Der Umzug bleibt
zulässig.


---

# Nachtrag 5 zur Übergabe — 21.09.2026, 21:35 Ortszeit: der Tag der vier Registerabschnitte

⚠️⚠️ **Ab hier gilt der Stand vom 21.09., 21:35.** Nachtrag 4 und seine drei
Ergänzungen bleiben stehen (append-only), sind aber überholt, wo dieser Nachtrag
etwas anderes sagt.

⭐ **Alle Zahlen unten sind am 21.09. zwischen 21:30 und 21:35 über die
Geräteanbindung gemessen**, nicht erinnert. Wo etwas erschlossen ist, steht es
dabei.

---

## Block 1 — Der Stand in drei Zeilen

| | |
|---|---|
| **Fertig** | **TB-78** und **TB-79** — Registerabschnitte **27** (Sichtschutz), **28** (`asof` gesetzt, Horizontbeginn, Vorlauf-Satz), **29** (Kapitalpfad ab erster Falte), **30** (der gesperrte Faltenplan), **31** (kein Manifest-Feld `asof`). Dazu Prüfprinzip **`A8`**, drei Regeln in `ARBEITSWEISE.md`, die Berichtigung der TB-77-Offen-Liste und die Wiederherstellung von `AKTUELLER_AUFTRAG.md` |
| **Läuft** | **nichts.** Keine Mac-Sitzung, Baum sauber |
| **Als Nächstes** | ⭐⭐ **Der Faltenplan nach 4a als Registertext** (30.2 (2)) → die Abbild-Datei mit Hash auf die Sperrliste (30.2 (3)) → der Abgleich Datei↔Registertext → **TB-30b** → Sperrlisten-Vollzug → **der signierte Tag** |

---

## Block 2 — `HEAD`, Zweig, Commit-Kette

```
HEAD    2250ed1   Zweig main
Baum    0 geändert · 1 unversioniert: .claude/settings.local.json
```

**Die Kette des Abends, von früh nach spät** (Ortszeit):

`83e3a85` (TB-77-Abgabe, 17:18) → `ee0b799` (TB-78 Schritt 0, 19:18) →
`2848b7a` `003f894` `94b3b3b` `2fd9498` `5d32be4` `7d2f739` (Schritte 1–6,
19:19–19:23) → `54bbe66` (Abgabe, 19:26) → `c843fd5` `e47ddfe` (Nachtrag v2:
Schritte 3b und 6b, 19:45–19:46) → `6f19aff` `0592af3` (Fortschreibung, 19:48) →
`85e80a2` `31a4665` (TB-79 Schritt 0, 21:08) → `b99214a` (Abschnitt 31, 21:10) →
**`2250ed1`** (Abgabe, 21:12).

⚠️ **Zeitstempel über die Geräteanbindung sind UTC**, auch mit
`--date=iso-local` — die Brücke läuft in UTC, nicht in Ortszeit. ⭐ *Neu gemessen
am 21.09.: `git log --date=format-local` liefert dort `+0000`. Zwei Stunden
Unterschied, dieselbe Fehlerklasse wie Block 7, Punkt 2 vom 20.09.*

---

## Block 3 — Die tragenden Zahlen, jede mit Fundstelle

| Grösse | Wert | Fundstelle |
|---|---|---|
| ⭐⭐ **`asof`** | **2026-09-19** | Abschnitt **28.3**; Quelle `zeitpunkt_utc` im Manifest, Abschnitt 18 Z. 2596 |
| ⭐⭐ **Horizontbeginn** | **2016-09-19**, alle vier Aktien-Bots; Krypto-Bots **kein Horizont** | Abschnitt **28.4** (ersetzt den Platzhalter in 26.3) |
| ⭐ **`datenende`** | **2026-09-15**, Abstand zu `asof` **4 Tage** | Abschnitt **31.5**, Mac-Lauf TB-79, zwei Zählungen (csv-Modul und pandas 2.3.3) |
| ⚠️ **je Markt verschieden** | 150 Aktien-Tagesdateien enden **2026-09-01** · 24 Krypto-Tagesdateien 2026-09-14 · 48 Krypto-4h/1h 2026-09-15 · `XAUTUSDT_1h` 2026-08-30. **Das Datenende der Aktien-Bots liegt 18 Tage vor `asof`** | Abschnitt **31.5**, Messnotiz |
| **Das Register** | `docs/VORREGISTRIERUNG_neuselektion.md` · **5 089 Zeilen · 313 878 B** · SHA-256 `aa3b4cf3…` | gemessen bei `2250ed1` |
| **Höchster Abschnitt** | **31** | `grep -nE "^## 3[0-9]\."` |
| **Manifest-Schlüssel** | **16**, keiner heisst `asof`; ohne die Dateiliste `dateien` sind es 15 | Abschnitt **31.6**, zwei unabhängige Zählungen |
| **Sperrlisten-Hashes** | `a163c498…` · `0e54ac5c…` · `4549395f…` | **unverändert** seit dem 20.09. |
| **Manifest-Hash** | `5cf1103e7487514b…` | vor und nach TB-79 identisch — Nachweis zu 31.3 |
| **Prüfprinzipien** | Gruppe A: **`A1`–`A8`**, keine Nummer doppelt | `docs/PRUEFPRINZIPIEN.md` |
| **Journal** | letzter Block **`CG`** | |

### ⚠️ Gemessene Nummernstände

| | Stand | nächste freie |
|---|---|---|
| Registerabschnitte | **31** | **32** |
| Prüfprinzipien Gruppe A | **`A7`** vor heute, **`A8`** seit TB-78 | **`A9`** |
| Journalblöcke | **`CG`** | **`CH`** |

⭐⭐ **`A5` war belegt, und das hat der Übergabe-Nachtrag 4 nicht gemessen.**
Ergänzung 1 zu Nachtrag 4 (17:25) schlug `A5` für das neue Prinzip vor — dort
steht seit dem 18.09. *„Ein Werkzeug, das nicht mehr misst, sagt es"*. Vergeben
wurde **`A8`**, gemessen. ⇒ **`K2i` gilt auch für unsere eigenen Nachträge:**
*ein Nachtrag nennt keine Nummer, die er nicht selbst gemessen hat.*

---

## Block 4 — Offen vor dem signierten Tag, in Reihenfolge

⭐ **Die Reihenfolge ist Fables, aus 21b und 21i, und sie ist begründet.**

| | Schritt | warum hier |
|---|---|---|
| **1** | ⭐⭐ **Der Faltenplan nach 4a als Registertext** — je Bot die Liste der Selektionsfalten, abgeleitet aus `asof`, `RECENT_YEARS_ONLY`, dem Indikator-Vorlauf gegen den Horizontbeginn und dem Trockenlauf nach 3b (b) | **30.2 (2)**. Alle vier Eingangsgrössen stehen jetzt im Register — vor heute fehlte `asof` |
| **2** | **Genau eine Abbild-Datei mit Hash auf die Sperrliste**, als neuer Punkt; der Lauf liest nur sie | **30.2 (3)** |
| **3** | **Der Abgleich Datei ↔ Registertext**, je Bot, je Jahr, als Tatsachennotiz mit Ergebnis | **30.2 (3)**. ⚠️ Ob `faltenplan_tb72.json` das Abbild ist, entscheidet **allein dieser Abgleich**, nicht ihre Herkunft (30.2 (4)) |
| **4** | **TB-30b** — die vier `multi_symbol_optimise.py` (`entry_cutoff` einmal je Bot aus dem Register) **plus die Wache**: frühester Einstieg ≥ **Beginn der ersten Selektionsfalte**, sonst rc 2; Bericht führt je Bot Horizontbeginn, Beginn der ersten Falte und frühesten Einstieg nebeneinander | **29.4**. ⚠️ Die Fassung aus 21b (nur Horizontbeginn) ist **ersetzt** |
| **5** | **Sperrlisten-Vollzug** über alle neun Bots | braucht die **eigene** Betreiberfreigabe aus Register 21.9 |
| **6** | **Der Tag** | |

**Daneben, nicht blockierend:** `TB-70` · `T56b.6` (Konstantenkopien, dazu `K4f`
Zeile 65) · `T56b.7` · `T46.1b/c` · die zwei roten Proben `G6`/`H3` · die
Kettenzeile `0,99` (Lauf-Reproduktion gegen den Lock).

⭐ **Zwei Messungen, die 29.5 verlangt und die noch niemand gemacht hat:**
(1) wo der Kapitalpfad der neun Optimierer **heute** beginnt; (2) **ob** es in
den vorhandenen Trade-Listen Einstiege zwischen Horizontbeginn und dem
1. Januar der ersten Falte gibt. ⛔ **Nur das Ob, nicht die Wirkung** — eine
Aussage über Kennzahlen fiele unter 27.1. ⚠️ **Und jede Messung an den neun
`paper_trading_*.db` läuft auf einer Kopie.**

---

## Block 5 — Wartezustände

| wartet | worauf |
|---|---|
| **Mac-Sitzung** | keine läuft; Baum sauber, `HEAD 2250ed1` |
| ✅ **Fable** | **auf nichts.** 21j ist eingearbeitet (Abschnitt 31), die Rückmeldung 21d ist abgelegt und stellt keine Frage. Nächste Frage an ihn erst, wenn der Faltenplan als Registertext steht |
| **Betreiber** | **Start des nächsten Auftrags** (Faltenplan nach 4a) |

⭐ **Kein Umzugshindernis nach `UMZUG.md` Abschnitt 3:** keine Sitzung, nichts
uncommittet, keine offene Rückfrage.

---

## Block 6 — Freigaben und Sperrliste

| | |
|---|---|
| ⭐⭐ **Aktive Freigabe für eine Sperrlisten-Datei** | **`research/vorregistrierung/faltenplan.py`** — Betreiberfreigabe 21.09.2026, 21:47 Ortszeit, für die Umstellung von Bedingung (i) auf `asof` (**TB-80**). ⚠️ *Die Freigabe sagt, dass geändert werden durfte; sie sagt nicht, was geändert wurde — der Diff wird vor dem Abschluss angesehen.* ⛔ Sie deckt `ergebnisse/faltenplan.json` (`0e54ac5c…`) ausdrücklich **nicht** |
| **Sperrlisten-Vollzug neun Bots** | steht aus, braucht **eigene** Freigabe (Register 21.9) — *Freigaben verfallen nicht von selbst; diese wurde nie erteilt* |
| ⭐ **Neu auf der Sperrliste zu erwarten** | **eine** Abbild-Datei des Faltenplans, mit Hash, als neuer Punkt (30.2 (3)) |
| ⭐ **Neu unter Punkt 2** | eine **Tatsachennotiz** (kein Ersatz, keine Streichung): `faltenplan.json` ist registrierter historischer Stand, nicht der Plan nach 4a (30.3) |
| **`auswertung.py`** | eingefroren (Abschnitt 0, Z. 31). Fables Ausnahme dafür bleibt **zurückgezogen** |
| **Der Snapshot** | ⭐ **einschliesslich Manifest** nach seiner Erzeugung nicht mehr zu schreiben (31.3, Ersteintrag) |

---

## Block 7 — ⭐⭐ Die Fehler dieses Chats und die Regeln daraus

| | Fehler | ⇒ Regel |
|---|---|---|
| **1** | ⚠️⚠️ **`AKTUELLER_AUFTRAG.md` mit einer Zeile überschrieben, ohne sie anzusehen.** Sie hatte **87 Zeilen** — Wache, Begründung, Planungstabelle; `numstat` zeigte `1 86`, und der Einzeiler ging mit einem Commit in die Historie | ⭐⭐ **Block 7, Punkt 7 vom 20.09. gilt unverändert: nie überschreiben.** Vor jedem Schreiben auf eine vorhandene Datei wird sie **gelesen**, nicht angenommen. *Verloren war nichts, weil git die Fassung hielt — das war Glück, nicht Verfahren* |
| **2** | ⚠️⚠️ **Ein Kopierblock ohne Empfänger — der Einfügesatz für die Mac-Sitzung landete im Fable-Chat.** Er hat ihn zurückgewiesen, in jedem Punkt richtig, auch in dem, der nicht dastand: dass das Eintragen von Registertext nicht seine Rolle ist | ⭐⭐ **`ARBEITSWEISE.md` Abschnitt 1 gilt für jeden Kopierblock:** *bei jedem Dokument und jeder Aufgabe wird ausdrücklich gesagt, wohin es geht — nicht nur in der Datei, auch in der Begleitnachricht.* **Der Betreiber führt mehrere Sitzungen parallel; ein Block ohne Adresse ist eine Wette** |
| **3** | ⚠️ **`A5` als Nummer vorgeschlagen, ohne sie zu messen** (Übergabe-Nachtrag 4, Ergänzung 1). Sie war seit dem 18.09. belegt | ⭐ **`K2i` gilt für unsere eigenen Nachträge:** die nächste freie Nummer wird **gemessen**, nicht geschätzt — auch in der Übergabe |
| **4** | ⚠️ **Ein Nachtrag wollte Registertext ändern, der zehn Minuten zuvor committet worden war** (v1 gegen 28.6/29.2) | ⭐⭐ **Append-only kennt kein „noch frisch".** Der Nachtrag wurde zurückgezogen (v2), die Präzisierungen stehen als **30.6/30.7** daneben. *Fable hat das unabhängig bestätigt: „ich sehe es nicht anders"* |
| **5** | ⚠️ **Ein Nachtrag erreichte eine bereits abgeschlossene Sitzung nicht** (TB-78b). Er lag in `logs/auftraege/` — **kein Träger** | ⭐ **Ein Nachtrag, der eine Sitzung nicht mehr erreicht, wird zum Auftrag** (`TB-79`) und geht nach `docs/auftraege/`, **bevor** er in `logs/` altert |

⭐⭐ **Der gemeinsame Kern der Fehler 1 und 2, in einem Satz:** *Beide entstanden
beim Schreiben an einen Empfänger, den ich nicht gemessen hatte* — einmal eine
Datei, deren Inhalt ich nicht gelesen hatte, einmal ein Chat, den ich nicht
benannt hatte. **Dieselbe Klasse wie „ein Name ist kein Messwert", nur auf der
Ausgabeseite.**

### Fremde Befunde, die diesen Chat geprägt haben

| | |
|---|---|
| ⭐⭐ **Fable, 21i** | *„Ich habe ‚gesperrt' als ‚gültig' gelesen. Gesperrt heisst nur: unverändert."* — die Frage, aus der Abschnitt 30 entstand |
| ⭐⭐ **Fable, 21i** | *„Die Sperrliste beweist, dass nichts bewegt wurde. Einen Punkt zu entfernen, weil er obsolet ist, öffnet die Frage, wer ‚obsolet' entscheidet."* |
| ⭐⭐ **Fable, 21j** | *„Ich habe einen zweiten Feldnamen für denselben Wert angeordnet — genau die Bauart ‚zwei Träger, die auseinanderlaufen können', die ich selbst abgelehnt habe."* — **zweite Rücknahme einer eigenen Anordnung an einem Tag** |
| ⭐ **Fable, 21j** | *„Ein Träger, der nach der Registrierung noch beschrieben wird, kann nicht mehr bezeugen, was bei der Registrierung galt, auch wenn der Hash ihn nicht deckt."* |
| ⭐⭐ **TB-79** | Die Messnotiz zu 31.5 — **von der Sitzung selbst gefunden**, nicht beauftragt: die 223 Kursdateien enden nicht am selben Tag, die Aktienseite 18 Tage vor `asof` |

---

## Block 8 — Was zwischengelagert und noch nicht eingearbeitet ist

| | Wo es liegt | Zielort |
|---|---|---|
| ✅ | **Alle Fable-Dokumente 20a bis 21j** und unsere Anfragen 21b, 21c, 21d | **im Repo**, `docs/projektfuehrung/`, committet |
| ✅ | Der Übergabe-Nachtrag 4 samt drei Ergänzungen | **im Repo**, 442 → 984 Zeilen, `542 0` |
| ⚠️ | `logs/auftraege/NACHTRAG_TB-78_fable_21i.md` (v1, **ersetzt**), `…_v2.md` und `NACHTRAG_TB-78b_fable_21j.md` | `logs/` ist gitignoriert. **v2 und TB-78b sind inhaltlich im Repo aufgegangen** (Abschnitte 30/31 und `MAC_TB-79_register_31.md`); v1 ist ersatzlos erledigt. **Keine offene Bringschuld** |
| ⚠️ | `logs/auftraege/TB-58b_v2.md` (19.09.) | **offene Bringschuld**, unverändert seit dem 19.09. |
| | `.claude/settings.local.json` unversioniert | `.gitignore`-Entscheidung offen |

### Regeln, die in diesem Chat vereinbart wurden — abgeglichen, nicht erinnert

| | Regel | Stand |
|---|---|---|
| ✅ | **Jede Anfrage und jede Rückmeldung an den Verfahrensprüfer wird abgelegt wie seine Antwort** | `ARBEITSWEISE.md` Abschnitt 15, eingetragen durch TB-78 Schritt 5 |
| ✅ | **Bei jeder Übergabe an ihn wird ungefragt gesagt, was mitgeht und was nicht** | dito |
| ✅ | **Seine Fragen an den Betreiber werden ungefragt mit einer Empfehlung beantwortet** | `ARBEITSWEISE.md` Abschnitt 6d, dito |
| ✅ | **Der Einfügesatz steht nur noch in einer Fassung** | `ARBEITSWEISE.md` Abschnitt 14 Regel 2 folgt jetzt `AKTUELLER_AUFTRAG.md`, mit ERSETZT-Marke und dem alten Wortlaut daneben |
| ⛔ | **Ein Kopierblock nennt seinen Empfänger** (Fehler 2) | **neu, noch nirgends eingetragen** → nächster Dokumentationsauftrag |

---

## Block 9 — Der Eröffnungstext für den neuen Chat

⭐ **`UMZUG.md` Abschnitt 6, unverändert gültig.** Kein zweiter Text hier
(TB-68).

⚠️ **Eine Ergänzung, nur für den nächsten Umzug**, als zusätzlicher Absatz
anzuhängen:

```
Zusatz fuer diesen Umzug: Lies in UEBERGABE_2026-09-19.md zuerst NACHTRAG 5
(ganz am Ende) - das ist der Stand vom 21.09., 21:35. Die Bloecke davor und
Nachtrag 4 bleiben stehen, sind aber ueberholt, wo Nachtrag 5 etwas anderes
sagt. Danach diese Dateien, in dieser Reihenfolge:
  projektfuehrung/FABLE_ANTWORT_2026-09-21i_gesperrter_faltenplan.md
  projektfuehrung/FABLE_ANTWORT_2026-09-21j_manifest_asof.md
  projektfuehrung/REGISTER_KOPIE_2026-09-21.md   (Abschnitte 27 bis 31)
An diesen Entscheidungen haengt der naechste Schritt: der Faltenplan nach 4a
als Registertext.
```

---

## In einfacher Sprache

**Wo wir stehen:** Heute Abend sind fünf Regelblöcke ins Regelwerk gekommen. Der
wichtigste setzt das Stichtagsdatum: Ab dem 19. September 2026 wird zehn Jahre
zurückgerechnet, also bis zum 19. September 2016 — und vorher darf kein Bot
rechnen. Bis heute stand dort ein Platzhalter.

**Was sonst entschieden wurde:** Der Prüfer, der die Regeln festlegt, darf vor
dem grossen Lauf nicht wissen, wie er ausgeht. Das Depot jedes Bots startet am
1. Januar seines ersten Auswertungsjahres mit leerem Bestand. Der alte
eingefrorene Auswertungsplan bleibt eingefroren, bekommt aber den Vermerk
„historisch, wird nicht benutzt". Und die Beschreibungsdatei des eingefrorenen
Datenbestands wird nach dem Einfrieren nicht mehr angefasst — auch nicht für
harmlose Zusätze.

**Was als Nächstes kommt:** Der eigentliche Auswertungsplan — welche Jahre bei
welchem Bot geprüft werden. Alle vier Zutaten dafür stehen seit heute im
Regelwerk; bis heute Abend fehlte das Stichtagsdatum. Danach sind es noch drei
Schritte bis zu dem Moment, in dem die Regeln versiegelt werden und der Lauf
beginnen darf.

**Zwei eigene Fehler, die hier stehen bleiben:** Ich habe eine Datei
überschrieben, ohne hineinzusehen — nichts ging verloren, aber nur, weil die
Versionsverwaltung sie noch hatte. Und ich habe einen Befehl für den Rechner in
den falschen Chat geschickt, weil ich nicht dazugeschrieben hatte, für wen er
ist.
