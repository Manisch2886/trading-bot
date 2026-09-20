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
