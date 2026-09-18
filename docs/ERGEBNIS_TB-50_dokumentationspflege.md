# Ergebnis TB-50 — Dokumentationspflege (Mac-Sitzung, 18.09.2026)

**Lokale Claude-Code-Sitzung auf dem Mac, direkt auf `main`, kein Zweig, kein
PR.** Ausgangsstand laut Auftrag `2f241d1`; tatsächlicher Ausgangsstand beim
Start **`e432ed8`** (der Betreiber hatte die Nachträge (b) und den
Prüfprinzipien-Nachtrag nach `2f241d1` bereits committet — genau die Dateien,
die dieser Auftrag voraussetzt).

**Commits dieser Sitzung:** `02de1f7` (die Einarbeitung, sechs Dateien) und der
Folgecommit mit den fünf Beleg-Köpfen und diesem Dokument. Beide gepusht.

⭐ **Diese Aufgabe ist der erste Anwendungsfall der Regel, die sie in Teil 1
einträgt** — Dokumentationsänderungen als Auftrag an die Mac-Sitzung, nicht als
Download.

---

## Die Fragen des Auftrags, zuerst

| Frage | Antwort |
|---|---|
| **Zeilen je Datei hinzugefügt / entfernt — ist jede entfernte erklärt?** | **Ja, alle 15.** `ARBEITSWEISE.md` 53/7 · `BACKLOG.md` 137/6 · `JOURNAL.md` 632/0 · `PRUEFPRINZIPIEN.md` 38/0 · `UMGEBUNGEN.md` 6/2 · `basislauf.py` 6/0. Jede der 15 entfernten Zeilen steht in Abschnitt 1 einzeln neben der Ersetzung, die sie verursacht hat. ⚠️ Zwei Erwartungszahlen des Auftrags weichen ab (7 statt 6 bei `ARBEITSWEISE.md`, 6 statt 8 bei `BACKLOG.md`) — beide Ursachen sind benannt und liegen im Diff-Verhalten von git, nicht in fehlenden oder überzähligen Änderungen |
| ⚠️ **Welcher Journal-Blockbuchstabe war wirklich der letzte?** | **AZ**, nicht AX — maschinell über alle 40 Blocküberschriften erhoben. **Alle sechs Blöcke sind um zwei Stellen gerückt:** AY→BA, AZ→BB, BA→BC, BB→BD, BC→BE, BD→BF. **Verweise:** in den fünf Nachtragsdateien gibt es **keinen** Textverweis auf die neuen Buchstaben (maschinell gesucht, nur die Überschriften selbst treffen) — es war also nichts mitzuziehen |
| **Wo liegt `START_HIER.md`?** | ⚠️ **Nirgends im Repo** — weder unter `docs/`, noch im Wurzelverzeichnis, noch sonst im Arbeitsbaum (`find` ohne `trading-env/`, `git ls-files`). Kein Wortlaut zu zitieren, **nichts angelegt, Teil 4 nicht ausgeführt** |
| ⚠️ **Wie heisst die Einstufung in `basislauf.py` jetzt?** | **Unverändert — es gibt keine.** Die Datei kennt genau drei Listen: `BEKANNT_ROT`, `UNGEPRUEFT`, `LAEUFT_WEITER`. **Eine Stufe „flackernd" war nicht vorhanden und ist nicht erfunden worden.** Der freigegebene Kommentar steht unmittelbar unter dem Streichungsvermerk aus TB-47, vor `BEKANNT_ROT = {`. ⚠️ **Folge, ehrlich benannt:** ein roter Lauf von `system/test_log_rotation.py` wird vom Basislauf weiterhin als UNERWARTET gemeldet — und ein Eintrag in `BEKANNT_ROT` hätte umgekehrt jeden grünen Lauf (70 %) als UNERWARTET gemeldet. Beides ist falsch; die richtige Stufe wäre eine Änderung am Messwerkzeug und ist nicht freigegeben |
| **Die drei Rückgabewerte von `system/test_log_rotation.py`** | **0 · 0 · 0**, je `117 von 117`. Nach 6a der wahrscheinlichste Ausgang (0,7³ ≈ 34 %) — **widerlegt nichts** (A6) |
| **`pruefe_register.py` weiterhin ohne Befund? Neun Datenbanken identisch?** | Siehe Abschnitt 8 — mit `--basis a1e7fb4` **KEIN BEFUND, rc 0**, vorher wie nachher. Ohne `--basis` meldet er vorher wie nachher denselben strukturellen Befund `LEERER VERGLEICH` (auf `main` nach dem Merge ist der Registerdiff leer — das ist sein A5-Selbsttest, kein Befund dieser Sitzung). **Neun Datenbanken byteweise identisch**, Datenstand `d9449faf…`/223 vorher = nachher |
| **Beobachtungen, die NICHT ausgeführt wurden** | Abschnitt 9, zwölf Punkte |

---

## 0. Schritt 0 — Datenbanken und Datenstand

| | vorher (14:21:54Z) | nachher |
|---|---|---|
| neun `paper_trading_*.db`, SHA-256 | `01_db_vorher.txt` | `23_db_nachher.txt` — **`diff` leer, byteweise identisch** |
| Datenstand | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223** | identisch, **223** |
| Snapshot-Ordner (`snapshots/`, `data/snapshots/`) | nicht vorhanden | nicht vorhanden |

Gemessen mit `research/vorregistrierung/herkunft.py::datenstand` (dieselbe
Funktion wie in TB-46 bis TB-49). Kein Bot gestartet, kein Abruf, kein
Broker-Endpunkt, kein Snapshot. Der Crontab wurde zu Beginn gesichert
(`03_crontab.txt`), um eine Abweichung gegenrechnen zu können — es gab keine.

---

## 1. `git diff --numstat` je Datei — und jede entfernte Zeile zugeordnet

```
38	0	docs/PRUEFPRINZIPIEN.md
6	2	docs/UMGEBUNGEN.md
53	7	docs/projektfuehrung/ARBEITSWEISE.md
137	6	docs/projektfuehrung/BACKLOG.md
632	0	docs/projektfuehrung/JOURNAL.md
6	0	research/datenordner_schnitt/basislauf.py
```

**15 entfernte Zeilen insgesamt. Jede einzeln:**

| # | Datei | entfernte Zeile (Anfang) | verursacht durch |
|---|---|---|---|
| 1 | `ARBEITSWEISE.md` | `> Dokumentation aktualisiert wird, mit dem Auslöser *„jede Bewertung bringt ihren` | **1d** Kopfvermerk, Zeile 2 von 6 |
| 2 | `ARBEITSWEISE.md` | `> Nachtrag mit"*), **6bb** (die Aufgaben des Betreibers am Ende jeder Antwort),` | **1d**, Zeile 3 |
| 3 | `ARBEITSWEISE.md` | `> **6d** (Entscheidungsvorlagen tragen eine Empfehlung), **7b** (Zugänge),` | **1d**, Zeile 4 |
| 4 | `ARBEITSWEISE.md` | `> **7c** (was in jedem Testauftrag steht), **11** (Änderungsverbote nennen ihren` | **1d**, Zeile 5 |
| 5 | `ARBEITSWEISE.md` | `> Zweck), **12** (Prüfprinzipien). Ergänzt: **2**, **6b**, **7**.` | **1d**, Zeile 6 |
| 6 | `ARBEITSWEISE.md` | `\| **1 — ganz ersetzen** \| Dokumente, die kurz genug sind …` | **1a** Tabellenzeile 1 |
| 7 | `ARBEITSWEISE.md` | `\| ⭐ **2 — Nachtrag** \| ⚠️ **`BACKLOG.md` und `JOURNAL.md`** …` | **1a** Tabellenzeile 2 |
| 8 | `BACKLOG.md` | `**Stand: 17.09.2026.** Nur **aktive Punkte**. …` | Nachtrag (a) **Ersetzung 1**, Kopfzeile |
| 9 | `BACKLOG.md` | `\| **0,5** \| **Krypto-Historie** (V2) …` | Nachtrag (a) **Ersetzung 2**, Kettenblock |
| 10 | `BACKLOG.md` | `\| **0,6** \| ⚠️ **T46.1 — die Ausstiegspfade prüfen.** …` | (a) Ersetzung 2 |
| 11 | `BACKLOG.md` | `\| **0,7** \| **TB-46 Erhebung + Snapshot-Werkzeug** …` | (a) Ersetzung 2 |
| 12 | `BACKLOG.md` | `\| **0,8** \| ⭐ **TB-47 — der eigentliche Umbau.** …` | (a) Ersetzung 2 |
| 13 | `BACKLOG.md` | `\| **0,9** \| **Registernachtrag** — 5a neu, 5e neu, …` | (a) Ersetzung 2 |
| 14 | `UMGEBUNGEN.md` | `\| `trading-env/` \| im `find` **ausschliessen** — sonst 1 312 statt 62 Testdateien \|` | **6b** Zahl 62 → 65 mit Datum |
| 15 | `UMGEBUNGEN.md` | `` `system/test_log_rotation.py` (1, Restfenster beim Rotieren) · `` | **6a** Ersetzung des Eintrags |

**Keine unerklärte entfernte Zeile.** Vollständige Zeilen in
`18_alle_entfernten_zeilen.txt`, der ganze Diff in `18_diff_gesamt_commit1.patch`.

### Warum 7 und nicht 6 bei `ARBEITSWEISE.md`

Der Auftrag erwartete 3 aus 1a und 3 aus 1d. Gemessen: **2 aus 1a, 5 aus 1d.**

- **1a:** Die dritte Tabellenzeile (`| **3 — neu dazulegen** | ein neues Dokument | wie Weg 1 |`) ist in Such- und Ersatztext **zeichengleich** — git sieht sie nicht als entfernt.
- **1d:** Nur die **erste** Zeile des Kopfvermerks ist unverändert. Der Ersatztext ist neu umbrochen (sieben statt sechs Zeilen), deshalb ist auch die vorletzte Zeile keine Zeile des alten Texts mehr (`> Zweck), **12** (Prüfprinzipien). Ergänzt: …` gegen `> steht), **11** (Änderungsverbote nennen ihren Zweck), **12**`). Ergebnis: fünf alte Zeilen entfernt, sechs neue hinzu.

Rechnung: 2 + 5 = **7**. Die Änderungen selbst sind genau die vier beauftragten.

### Warum 6 und nicht 8 bei `BACKLOG.md`

Der Auftrag erwartete Kopfzeile (1) + Kettenblock aus (a) + zwei Kettenzeilen aus (b).

- **Kettenblock:** In `main` umfasste der Block der Ränge 0,5 bis 0,95 **sechs** Zeilen (0,5 · 0,6 · 0,7 · 0,8 · 0,9 · 0,95). Die Zeile **0,95** (`| **0,95** | **`auswertung.py` auf Verfahren B** | zu formulieren |`) ist im neuen Block zeichengleich enthalten → git zählt sie nicht. Entfernt: **5**.
- **Die zwei Kettenzeilen 0,82/0,84 aus (b)** ersetzen Zeilen, die Nachtrag (a) in **derselben Sitzung** angelegt hat — sie waren nie in `main`. Im `numstat` gegen `main` erscheinen sie deshalb **weder als hinzugefügt noch als entfernt**. ⭐ **Belegt ist die Ersetzung trotzdem:** Der Stand nach (a) wurde als Datei gesichert und der Schritt (b) allein dagegen gemessen — `git diff --no-index --numstat`: **`38 2`**, und die beiden entfernten Zeilen sind genau `| **0,82** | …` und `| **0,84** | …` (`12_numstat_backlog_schritt_b_allein.txt`, `12_entfernte_zeilen_schritt_b_allein.txt`).

Rechnung: 1 + 5 = **6** gegen `main`; 2 weitere im Zwischenschritt, einzeln belegt.

---

## 2. Teil 1 — `ARBEITSWEISE.md` (53 / 7)

Voraussetzung geprüft: **38072 Bytes**, Abschnitte 5b, 6bb, 6d, 7b, 7c, 11, 12
vorhanden → Teil 1 ausgeführt. Alle vier Texte wurden **maschinell aus dem
Auftragsdokument zwischen den `--- ANFANG … ---`/`--- ENDE … ---`-Marken
gelesen**, nicht abgetippt (`bloecke.py`); jeder Suchtext und jeder Anker wurde
vor dem Ersetzen auf **genau einen Treffer** geprüft.

| | Stelle | Ergebnis |
|---|---|---|
| **1a** | Tabelle in 5b | zwei Zeilen ersetzt, dritte unverändert |
| **1b** | vor `### Der Auslöser: jede Bewertung bringt ihren Nachtrag mit` | 39 Zeilen + Leerzeile eingefügt |
| **1c** | vor `  > ⚠️ **Ab der ersten Ablage …` (zwei Leerzeichen) | 4 Zeilen + Leerzeile, mit zwei Leerzeichen Einrückung |
| **1d** | Kopfvermerk | 6 Zeilen → 7 Zeilen |

---

## 3. Teil 2 — `BACKLOG.md` (137 / 6)

**Reihenfolge eingehalten: erst (a), dann (b).** Alle Texte aus den beiden
Nachtragsdateien gelesen (Zeilenbereiche), nicht abgeschrieben.

| Schritt | was |
|---|---|
| (a) Ersetzung 1 | `**Stand: 17.09.2026.**` → `**Stand: 18.09.2026.**` |
| (a) Ersetzung 2 | Kettenblock 0,5–0,95 (6 Zeilen) → neuer Block (10 Zeilen) |
| (a) neu | Blöcke **2e, 2f, 2g** in dieser Reihenfolge nach Block 2d, vor „3 — Die Kette" |
| (a) neu | **K1a–K1i** an die Tabelle in Abschnitt 4, nach der Zeile `**Regel**` |
| (b) Ersetzung | Kettenzeilen **0,82** und **0,84** → Fassung aus (b) |
| (b) ⭐ Merge-Commit | an **beiden** Stellen, an denen (b) `claude/new-session-kfbw56` nennt (Kettenzeile 0,82 und Kopf von 2h): `Zweig `claude/new-session-kfbw56`, gemergt `2f241d1`` — nur das Wort „gemergt" und der Commit eingesetzt, sonst nichts |
| (b) neu | Block **2h** nach 2g |
| (b) Berichtigung | an **T47.9**: der alte Text bleibt, die Berichtigung steht als **eigene Tabellenzeile direkt darunter** (`| **T47.9** — Berichtigung | … |`) |
| (b) neu | Ergänzung an **T34.10** ebenso als eigene Zeile darunter (`| **T34.10** — Ergänzung | … |`); **K1j–K1m** nach K1i |

⚠️ **Zwei Formentscheidungen, offen benannt** (keine inhaltliche Änderung):

1. **Überschriftsebene.** Die Nachträge tragen die Blöcke als `### 2e …`, im
   Backlog stehen 2b/2c/2d als `## …` mit `###`-Unterabschnitten. Die vier
   neuen Blöcke stehen deshalb als `## 2e` … `## 2h`, der eine Unterabschnitt in
   2e (`#### Die Antwort auf T46.1 …`) als `###`. Als `###` eingefügt wären sie
   Unterabschnitte von 2d gewesen.
2. **T47.9 / T34.10.** Beide Punkte sind Tabellenzeilen; ein Zitatblock
   „darunter" würde die Tabelle beenden. Die Texte stehen deshalb als eigene
   Tabellenzeile unmittelbar darunter, Wortlaut unverändert, die `> `-Zeichen
   des Zitats entfallen in der Zelle. Bei T34.10 hat das zusätzlich den Zweck,
   die bestehende Zeile **nicht** anzufassen (sonst eine vierte, nicht
   beauftragte Ersetzung im `numstat`).

---

## 4. Teil 3 — `JOURNAL.md` (632 / 0)

**Zuerst gemessen, nicht übernommen.** Überschriften der Form `## <Buchstabe> —`
maschinell erhoben: **40 Blöcke**, L bis AZ (P fehlt seit jeher), keine
Dubletten, **höchster: AZ**. Damit lag die Annahme des Nachtrags (AX) um zwei
daneben — **AY** („Die Sichtbarkeitsreihe: TB-42 bis TB-45") und **AZ** („TB-46
und die beiden Fable-Runden") existierten bereits.

| Nachtrag | im Journal |
|---|---|
| AY — TB-46 gemergt, Zuschnitt B entschieden, zwei Fable-Runden | **BA** |
| AZ — TB-46b: der Sicherheitspunkt ist beantwortet | **BB** |
| BA — TB-47: die Snapshotgrenze, gemessen | **BC** |
| BB — Registertext 5a: die Ausnahme `rand_erste` | **BD** |
| BC — TB-48: der Registernachtrag, und zwei Fehler von mir | **BE** |
| BD — TB-49: das Werkzeug lernt die Ausnahme (Nachtrag b) | **BF** |

**Verweise:** In allen fünf Nachtragsdateien und im ganzen eingefügten Text
wurde nach `AX`–`BF` und nach „Journalblock"/„Block <Buchstabe>" gesucht — es
gibt **keinen** Verweis ausser den Überschriften selbst (`13_verweise_blockbuchstaben.txt`).
Nichts war mitzuziehen. Die beiden Journal-Nachtragsdateien nennen im Kopf
weiter „AY bis BC" bzw. „BD" — das sind Belegdokumente, sie bleiben unverändert;
der Beleg-Kopf (Teil 8) nennt die Zuordnung.

⚠️ **Zwei Formentscheidungen:**

1. **Einfügestelle.** Der Auftrag sagt „am Ende der Datei". Die Datei endet
   seit jeher mit dem Abschnitt `## Wiederkehrende Lehren` (ihr Kopf sagt: *„Am
   Ende: die wiederkehrenden Lehren."*), und der letzte Nachtrag (`66530f4`,
   AY/AZ) wurde ebenfalls **vor** diesen Abschnitt gesetzt. Die sechs Blöcke
   stehen deshalb **am Ende des chronologischen Teils, unmittelbar vor „Wiederkehrende
   Lehren"** — nicht hinter den Lehren. `numstat` bleibt `632 0`.
2. **Überschriftsform.** Die 40 vorhandenen Blöcke heissen `## AZ — …`; die
   Nachträge schreiben `## Block AY — …`. Die neuen Überschriften folgen der
   Form der Datei (`## BA — …`), damit eine künftige maschinelle Erhebung des
   höchsten Buchstabens sie findet. Der Buchstabe musste ohnehin geändert werden;
   sonst ist an den Überschriften nichts verändert.

---

## 5. Teil 3b — `PRUEFPRINZIPIEN.md` (38 / 0)

**A6** eingefügt, **zwei Zeilen** an die C1-Tabelle unmittelbar nach der
2022-Zeile. Keine Umnummerierung, keine bestehende Zeile geändert.

⚠️ **Eine Formentscheidung:** Zwischen A5 und `## B — …` steht ein
Trennstrich `---`. „Unmittelbar vor" der `## B`-Zeile hätte A6 **hinter** den
Trennstrich gesetzt, also optisch in den Abschnitt B. A6 steht deshalb vor dem
Trennstrich, als letztes Prinzip des Abschnitts A. Text unverändert.

---

## 6. Teil 4 — `START_HIER.md`

**Nicht gefunden.** Gesucht: `find` über den ganzen Arbeitsbaum ohne
`trading-env/` und `.git/` (`-iname '*start*hier*'`), `git ls-files | grep -i start`,
Textsuche unter `docs/`. Die Datei wird nur in `ARBEITSWEISE.md` (Abschnitt 5b,
10) **erwähnt**; es gibt sie im Repo nicht. **Nichts angelegt.** Der Text aus
Teil 4 des Auftrags wartet damit auf den Betreiber (er hat die Datei
offensichtlich lokal oder in einem Archiv, nicht im Repo).

---

## 7. Teil 6 und 7 — `UMGEBUNGEN.md` (6 / 2) und `basislauf.py` (6 / 0)

### `UMGEBUNGEN.md`

| | alt | neu |
|---|---|---|
| **6a** Liste „Bekannt rot auf dem Mac" | `` `system/test_log_rotation.py` (1, Restfenster beim Rotieren) · `` | `` `system/test_log_rotation.py` — grün im Regelfall, zeitabhängig flackernd — auf dem Mac 3 von 10 Läufen rot (gemessen 18.09.2026, TB-49). Eine Einzelmessung belegt hier nichts, siehe `docs/PRUEFPRINZIPIEN.md` A6 · `` (drei Zeilen) |
| **6b** Testdateien | `sonst 1 312 statt 62 Testdateien` | `sonst 1 312 statt 65 Testdateien *(65 gemessen 18.09.2026 im TB-49-Maclauf; die 62 stammte aus TB-45)*` |
| **6b** `pandas_market_calendars` | fehlte | neue Zeile nach `dateparser`: Mac **4.6.1**, Cloud **5.4.0** (TB-49) |
| **6b** Betriebssystem | fehlte | neue Zeile nach „Rolle": **macOS 15.7.9 (Build 24G830), Darwin 24.6.0, x86_64**; Cloud-Spalte *nicht gemessen* |

⭐ **An der Quelle gegengeprüft, nicht abgeschrieben** (`04_umgebung_messwerte.txt`):
`pandas_market_calendars` **4.6.1** (Import und `pip show`, `trading-env`) ·
`sw_vers` 15.7.9 / 24G830 · `uname` Darwin 24.6.0 x86_64 · `node` v24.21.0 ·
`scipy` fehlt · pandas/numpy/dateparser 2.3.3 / 2.0.2 / 1.2.2 ·
`basislauf.testdateien()` = **65**. Alle „bestätigt und unverändert zu
lassenden" Angaben treffen zu. Die Regel 4 („Abweichungen melden") steht
unverändert.

### `basislauf.py` — die eine freigegebene Stelle

Der sechszeilige Kommentar steht **wörtlich** unter dem Streichungsvermerk aus
TB-47 (alte Zeilen 54–60), unmittelbar vor `BEKANNT_ROT = {`. Die vier
Leerzeichen vor jeder Zeile im Auftrag sind die Codeblock-Einrückung des
Markdown; auf Modulebene steht der Kommentar wie der umgebende in Spalte 0.
`py_compile` grün. **Kein Eintrag in eine Liste, keine neue Liste, keine neue
Stufe** — siehe die Antwort oben.

**Nachweis:** drei Läufe `trading-env/bin/python3 system/test_log_rotation.py`
→ rc **0, 0, 0**, je 117/117 (`17_log_rotation_lauf1..3.txt`).

---

## 8. Gegenproben

| Prüfung | vorher | nachher |
|---|---|---|
| `pruefe_register.py --basis a1e7fb4` | KEIN BEFUND, rc 0, numstat `506 0 docs/VORREGISTRIERUNG_neuselektion.md` | **KEIN BEFUND, rc 0**, identisch |
| `pruefe_register.py` ohne `--basis` | 1 Befund: `LEERER VERGLEICH gegen e432ed8` | derselbe eine Befund, dieselbe Basis |
| neun Datenbanken | `01_db_vorher.txt` | **byteweise identisch** (`23_db_diff.txt` leer) |
| Datenstand | `d9449faf…`/223 | `d9449faf…`/223 |

Zum zweiten Punkt: Der Prüfer bestimmt seine Basis als `merge-base HEAD
origin/main`; auf `main` nach einem Merge steht dort keine Registerdatei im Diff,
und genau das meldet er als Befund statt als Erfolg (Prüfprinzip A5, B3; so
schon in TB-41 festgehalten). Der Lauf mit `--basis a1e7fb4` ist der Lauf, den
TB-48 und TB-49 als Nachweis verwendet haben. **Kein Registertext wurde
angefasst** (`git diff --stat` nennt keine `docs/VORREGISTRIERUNG_*`).

---

## 9. Beobachtungen, die NICHT ausgeführt wurden

1. ⚠️ **`basislauf.py`, Docstring Zeile 23:** *„findet `find` **1312** statt 62 Testdateien"* — dieselbe gealterte 62 wie in `UMGEBUNGEN.md`; nicht freigegeben, nicht geändert.
2. **Die 1 312 ist ebenfalls gealtert:** mit `trading-env/` zählt `find` heute **1 315** `test_*.py` (65 ohne). Der Auftrag nannte nur die 62; die 1 312 blieb stehen.
3. ⚠️ **Widerspruch innerhalb einer Zeile, absichtlich stehen gelassen:** Die Kettenzeile 0,82 sagt jetzt *„Zweig …, gemergt `2f241d1`. ⚠️ **Mac-Lauf und Merge offen**"*. Der Merge-Commit war einzusetzen, der übrige Text nicht umzuformulieren. Ebenso steht der Kopf von Block 2h und der Journal-Block BF weiter auf „Cloud fertig / Mac-Lauf und Merge offen", während T49.16 im selben Block den Mac-Lauf als erledigt führt. Für den Journal-Nachtrag (b) war das Einsetzen des Merge-Commits **nicht** beauftragt (Teil 2 betrifft das Backlog) — dort steht `kfbw56` ohne Commit.
4. **Inhaltliche Nähe zweier Journalblöcke:** Der vorhandene Block **AZ** (17.09., „TB-46 und die beiden Fable-Runden: der Zuschnitt der Datenbestände") und der neue Block **BA** (Nachtrag AY, „TB-46 gemergt, Zuschnitt B entschieden, zwei Fable-Runden") behandeln denselben Gegenstand; BA bringt den Merge-Commit `135c306` hinzu. Beide stehen; nichts zusammengelegt.
5. **Das Inhaltsverzeichnis des Journals** (`## Inhalt`) endet bei AG und wird seit langem nicht fortgeführt — die neuen Blöcke sind dort nicht eingetragen, wie auch AH–AZ nicht.
6. **Die Journal-Nachtragsdateien tragen im Kopf weiter „AY bis BC" / „BD".** Sie sind Belege und wurden nur um den EINGEARBEITET-Kopf ergänzt, der die tatsächlichen Buchstaben nennt.
7. **`ARBEITSWEISE.md` 5b, Abschnitt „Der feste Ablauf", Schritt 2 und 3** sprechen weiter von `CLOUD_TB-<Nr>_dokumentationspflege.md` und „Der Nutzer startet die Cloud-Sitzung" — das widerspricht dem neuen Regelweg (Mac-Sitzung) aus 1b. Nicht Teil des Auftrags, nicht geändert.
8. **`ARBEITSWEISE.md` Abschnitt 10, Schritt 2** führt `START_HIER.md` und `STRATEGIEN_uebersicht.md` als Paketbestandteile; beide liegen nicht unter `docs/projektfuehrung/`.
9. **Ausgangsstand:** Der Auftrag nennt `2f241d1`; `main` stand beim Start auf `e432ed8` (Nachträge (b) committet). Kein Widerspruch, aber der Bericht sollte den wirklichen Stand nennen.
10. **Prüfprinzipien-Nachtrag, Überschrift „Berichtigung — eine Zeile in der Tabelle von C1"** kündigt eine Zeile an und liefert zwei. Beide eingefügt, wie der Einfügetext sie enthält.
11. **`test_log_rotation.py` dreimal grün** — bei ~30 % Flackerrate ist das mit 34 % Wahrscheinlichkeit zu erwarten und sagt nichts über die Rate. Kein weiterer Lauf gestartet, weil nicht beauftragt.
12. **Der `git status --porcelain` nach dem allerletzten Commit** kann in diesem Dokument nicht stehen, weil das Dokument Teil dieses Commits ist. Er liegt als Datei `25_status_nach_letztem_commit.txt` im ZIP und in der Chat-Antwort.

---

## 10. Ablauf und Belege

| Schritt | Beleg im ZIP |
|---|---|
| Quersummen / Datenstand vorher | `01_db_vorher.txt`, `02_datenstand_vorher.txt`, `03_crontab.txt` |
| Umgebungswerte an der Quelle | `04_umgebung_messwerte.txt` |
| `pruefe_register.py` vorher (beide Varianten) | `05_pruefe_register_vorher*.txt` |
| Skripte, die die Texte aus den Quellen lesen und einfügen | `bloecke.py`, `teil1_arbeitsweise.py`, `teil2a_backlog.py`, `teil2b_backlog.py`, `teil3_journal.py`, `teil3b_pruefprinzipien.py`, `teil6_umgebungen.py` |
| numstat und entfernte Zeilen je Datei und Schritt | `10_…` bis `16_…`, `18_numstat_gesamt_vor_commit1.txt`, `18_alle_entfernten_zeilen.txt`, `18_diff_gesamt_commit1.patch` |
| drei Läufe `test_log_rotation.py` | `17_…` |
| Commit 1, Beleg-Köpfe, Gegenproben nachher | `19_commit1.txt`, `20_numstat_belegkoepfe.txt`, `21_…`, `22_…`, `23_…` |
| Push und Status nach dem letzten Commit | `24_push.txt`, `25_status_nach_letztem_commit.txt` |

Interpreter durchgehend `trading-env/bin/python3` (3.9.6). Keine
Konfigurationsdatei geöffnet.

---

## In einfacher Sprache

**Was wir wissen wollten:** Kommen die fertig geschriebenen Nachträge vom 18.09.
in die vier Führungsdokumente hinein, ohne dass dabei eine alte Zeile
verlorengeht — und lässt sich das beweisen?

**Was herauskam:** Ja. Sechs Dateien wurden geändert, 872 Zeilen kamen hinzu,
15 Zeilen sind weg — und jede dieser 15 ist eine, die der Auftrag ausdrücklich
ersetzen liess (Kopfvermerk, drei Tabellenzeilen, die alte Rangliste, zwei
gealterte Angaben zur Umgebung). Beim Journal und bei den Prüfprinzipien ist
keine einzige Zeile weg. Die Datenbanken der neun Bots und der Kursdatenstand
sind vor und nach der Arbeit byteweise gleich.

**Warum das so ist:** Nichts wurde von Hand eingetippt. Ein kleines Skript hat
die Texte direkt aus den Nachtragsdateien und dem Auftrag gelesen und an
Stellen eingesetzt, die es vorher auf Eindeutigkeit geprüft hat. Danach hat
git gezählt.

**Was falsch war:** Der Nachtrag ging davon aus, der letzte Journalblock heisse
AX. Tatsächlich gab es schon AY und AZ. Die sechs neuen Blöcke heissen deshalb
BA bis BF, und das steht jetzt auch in den Belegdateien. Ausserdem gibt es die
Datei `START_HIER.md` im Repo gar nicht — der Teil dazu konnte nicht ausgeführt
werden. Und der flackernde Test lässt sich im Basislauf-Werkzeug nicht als
„flackernd" führen, weil es diese Stufe nicht kennt; es steht jetzt als
Kommentar dort, aber ein roter Lauf wird weiterhin als unerwartet gemeldet.

**Was das für dich heisst:** Die Führungsdokumente sind auf dem Stand von
heute und liegen gepusht auf `main`. Offen bleiben bei dir: `START_HIER.md`
(wo liegt sie?), die Frage, ob `basislauf.py` eine Stufe „flackernd" bekommen
soll, und ein paar kleine Widersprüche, die absichtlich stehen geblieben sind,
weil nichts umformuliert werden durfte (Abschnitt 9).
