# ERGEBNIS TB-75 — Die Journal-Seite nachziehen: sieben Nachträge, die zweite Bewährung des Wächters, und ob der Umweg noch nötig ist (Mac-Sitzung, 21.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-75_journal_nachziehen.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `f0ca921` (= `origin/main` beim Start),
Interpreter `python3` (der Wächter braucht nur die Standardbibliothek; für die
Zählskripte dasselbe). Keine Kursdaten, kein Bot-Code, **nichts ausserhalb
`docs/`**. Sitzung ab 09:11 Ortszeit.

*In einfacher Sprache, zu Beginn:* Sieben Notizen über das, was die letzten
sieben Aufgaben gemessen haben, lagen neben dem Journal. Sie stehen jetzt drin —
als Kurzfassung mit Zeigern, nicht abgeschrieben. Die Wache, die gestern gebaut
wurde, hat vorher und nachher nachgesehen und beide Male das Richtige gesagt.
Und die Frage, ob der Umweg über solche Notizen überhaupt nötig ist, ist
gemessen und dem Betreiber vorgelegt worden; er hat entschieden.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart, 21.09.2026 09:11 Ortszeit, `HEAD` = `f0ca921`, wörtlich:

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-75_journal_nachziehen.md
```

Zwei Betreiber-Dateien (der Auftragszeiger, das Auftragsdokument), keine aus
dieser Sitzung; ein Urheber, also ein Commit. **Schritt 0:** unverändert
committet als **`f1124ba`**, gepusht (`f0ca921..f1124ba`). Danach
`git status --short`: **0 Zeilen** — erst dann wurde geschrieben.

---

## Schritt 1 / Nachweis 2 — der Wächter misst, was offen ist

`python3 system/nachtragswaechter.py --json docs/belege/TB-75/schritt1_waechter.json`,
09:12 Ortszeit, gegen `f1124ba`. Ausgabe wörtlich in
`docs/belege/TB-75/schritt1_waechter.txt`; die Zusammenfassung:

```
Ziel: BACKLOG.md 1504 Zeilen, BACKLOG_ARCHIV.md 566, JOURNAL.md 7491 (14 Quellenzeilen)
A - OFFEN im Hauptverzeichnis: 7 Datei(en)      20g 0.6 d, 20h 0.6 d, 20i 0.6 d, 20j 0.5 d, 20k 0.5 d, 20l 0.5 d, 20m 0.1 d
B - EINGEARBEITET (_eingearbeitet/): 30 Datei(en)   26 OK, 4 [?] (19q, 19q_r, 19r, 19u)
C - DOPPELBELEGUNG: keine
Zusammenfassung: 0x OFFEN UEBER DER FRIST, 7x offen in der Frist, 4x NICHT PRUEFBAR, 0x FALSCH VERSCHOBEN, 0x DOPPELBELEGUNG
rc 0
```

**Weicht seine Liste von Abschnitt 0 des Auftrags ab?** In der **Menge nicht**:
genau `(20g)`–`(20m)`, sieben Dateien, keine mehr, keine weniger. **Im Status
ja:** der Auftrag sagt *„der Wächter meldet sie ab dem zweiten Morgen"* — und
heute früh meldet er **nichts**, weil alle sieben noch **in** der Frist liegen
(Alter aus der Änderungszeit, ältester `(20g)` 0,6 d, Frist 1 d). Gemessen
(`schritt1_alter.txt`): mtime und Commit-Zeit stimmen bei allen sieben auf die
Minute überein — die Frist von `(20g)` wäre am 21.09. um 17:53 abgelaufen, der
Cron-Lauf am 22.09. früh hätte gemeldet. *Der Auftrag ist damit einen Tag vor
dem Wächter gekommen, nicht auf seine Meldung hin — was er selbst richtig
vorhersagt („ab dem zweiten Morgen").*

Die vier `[?]` sind dieselben wie in TB-64 (Nachträge ohne Nummer der drei
Klassen, einmalig von Hand gemessen) — kein Befund, aber sichtbar, wie gebaut.

Commit **`ac8bb9b`**, gepusht.

---

## Schritt 2 / Nachweise 3, 4, 5 — sieben Blöcke

**Letzter Block vorher, gemessen:** `BT` (`grep -n '^## ' JOURNAL.md | tail`,
Zeile 7027). Danach folgt `## Wiederkehrende Lehren` (7154). Die Blöcke stehen,
wie `(20g)` es für TB-67 festhält und wie `BG`–`BT` es tun, **vor** `##
Wiederkehrende Lehren` — *„am Ende anfügen" meint das Ende der Blockfolge*
(`JOURNAL.md` Z. 43: *„Am Ende: die wiederkehrenden Lehren"*). Das
Inhaltsverzeichnis am Kopf bleibt bei `AF` (`K1p`), wie bisher.

| Block | Nachtrag | Sitzung | Zeilen Nachtrag → Block |
|---|---|---|---|
| `BU` | `(20g)` | TB-67 | 120 → 51 |
| `BV` | `(20h)` | TB-68 | 109 → 46 |
| `BW` | `(20i)` | TB-71 | 113 → 45 |
| `BX` | `(20j)` | TB-72 Schritt 1 | 124 → 59 |
| `BY` | `(20k)` | TB-72 Schritte 2–7 | 135 → 50 |
| `BZ` | `(20l)` | TB-73 | 136 → 47 |
| `CA` | `(20m)` | TB-64 | 132 → 54 |

**Nachweis 3:** `git diff --numstat` für `JOURNAL.md` = **`352 0`**
(`schritt2_numstat.txt`); 7 491 → 7 843 Zeilen. **Nachweis 4:** letzter Block
vorher `BT`, nachher **`CA`** (nach `BZ` folgt `CA`); alle `## XX —`-Überschriften
gezählt (`schritt2_blockbuchstaben.txt`, 67 Blöcke), `sort | uniq -d` = **0**.
**Nachweis 5:** `*Quelle:`-Zeilen **14 → 21**, sieben neu, jede zeichengleich
aus dem Kasten des jeweiligen Nachtrags; **0** nicht zuordenbar
(`schritt2_quellenzeilen.txt`).

**Nicht abgeschrieben:** 352 Zeilen für 869 Zeilen Nachtrag (41 %). Jeder Block
trägt Kopf mit Commits und Ergebnisdokument, eine Tabelle *„Was gemessen wurde"*
mit den Zahlen, die Regeln, das Offene — nicht den Sitzungsverlauf, nicht die
Einarbeitungsanweisungen, nicht *„In einfacher Sprache"*. Die Nachträge bleiben
unter `_eingearbeitet/` als Quelle.

Commit **`a096a7f`**, gepusht.

---

## Schritt 3 / Nachweis 6 — verschoben, und der Wächter danach

Sieben `git mv` nach `docs/projektfuehrung/nachtraege/_eingearbeitet/`; der
Hauptordner ist danach **leer**. Wächter erneut, 09:26, Ausgabe in
`schritt3_waechter.txt`:

```
Ziel: ... JOURNAL.md 7843 (21 Quellenzeilen)
A - OFFEN im Hauptverzeichnis: 0 Datei(en)
B - EINGEARBEITET (_eingearbeitet/): 37 Datei(en)   33 OK, 4 [?]
      OK  JOURNAL_NACHTRAG_2026-09-20g.md ... 20m.md   Quellenzeile im Journal   (alle sieben)
C - DOPPELBELEGUNG: keine
Zusammenfassung: 0x OFFEN UEBER DER FRIST, 0x offen in der Frist, 4x NICHT PRUEFBAR, 0x FALSCH VERSCHOBEN, 0x DOPPELBELEGUNG
rc 0
```

**0 über der Frist, 0 falsch verschoben** — alles angekommen. Die zweite
Bewährung: vor der Arbeit sieben offen, nach der Arbeit null, dazwischen nur
das, was der Auftrag verlangt hat; kein Fehlalarm, kein Durchwinken.

Commit **`d83ee02`**, gepusht.

---

## Schritt 4 / Nachweis 7 — die Messung: ist der Umweg noch nötig?

⛔ Nichts geändert. Fünf Punkte, je mit Fundstelle. Belege
`docs/belege/TB-75/schritt4_*`, Commit **`8d486ac`**.

### 1. Laufen je zwei Sitzungen gleichzeitig im selben Arbeitsbaum?

`git log --since=2026-09-15` mit `Co-Authored-By`-Trailer als Kennzeichen
einer Sitzung (S) gegen Commits ohne Trailer (B, Betreiber/Chat/Merge), zu
Läufen gleicher TB-Nummer zusammengefasst (`schritt4_p1_laeufe.txt`, 90 Läufe).
**Auf `main` seit 19.09. (lineare Historie, direkt auf `main`) ist kein
S-Lauf einer TB-Nummer von einem S-Lauf einer anderen unterbrochen.** Die
naive Spannenmessung (`schritt4_p1_ueberlappung.txt`, 102 „Überlappungen") täuscht:
sie zählt die Betreiber-Commits, die den Auftrag *beauftragen* (`c493b1b` „TB-64
beauftragt" um 13:01, die Sitzung lief am nächsten Morgen), zur Sitzung.

Was es **gab**: der Betreiber schrieb während laufender Sitzungen über die
Geräteanbindung in denselben Baum — TB-62 (15:21–15:23, drei Dateien, `BS`),
TB-68 (`30d44f7`, `6e0378f`). Immer Aufträge, Anfragen, Nachträge. **`JOURNAL.md`
hat seit der Versionierung 7 Commits, 5 davon Sitzungen; keiner vom Betreiber
während einer Sitzung; seit TB-50 in jedem `numstat` Spalte zwei = 0**
(`schritt4_p1_journal_commits.txt`, `_numstat.txt`).

### 2. Was passiert, wenn eine Sitzung mitten im Schreiben abbricht?

Drei Abbrüche: **TB-59** (19.09. 23:28, vor der Abgabe; Ergebnisdokument und
Nachtrag fehlten, Chat holte nach: `ERGEBNIS_TB-59` Z. 5–11, `(19g)`),
**TB-60** (20.09. 10:57, SSH, vor der Abgabe; `ERGEBNIS_TB-60` Z. 3–8, `(20a)`
vom Chat), **TB-72** (19:20, nach Schritt 1, vor dem Nachtrag; `ERGEBNIS_TB-72_schritt1` Z. 8–9).
**Zwei von drei trafen genau die Abgabe** — den Moment, in dem heute der
Nachtrag und morgen der Block geschrieben würde. In keinem Fall lag eine halb
geschriebene Datei; es fehlte die ganze. *Ein halb geschriebener Block ist bei
Verbindungsabbruch unwahrscheinlich (ein Werkzeugaufruf schreibt ganz oder gar
nicht); ein fertiger, aber uncommitteter Block wird von Schritt 0 der nächsten
Sitzung mitcommittet — wie ein uncommitteter Nachtrag auch.*

⚠️ **Der Befund, der zählt, ist ein anderer:** **3 von 7 Nachträgen sind nach
ihrem ersten Commit umgeschrieben worden** (`schritt4_p2_nachtrag_nachbearbeitung.txt`):
`(20g)` `a15746f` 8/7 — *„Der Push war in dieser Umgebung gesperrt"* wurde zu
*„Der Push ging erst am Ende"*, eine **sachliche Berichtigung**; `(20h)`
`1a301b0` 2/2 — zwei Betreiberentscheidungen durchgestrichen und eingetragen;
`(20m)` `f0ca921` 1/1 — der Abgabe-Hash nachgetragen. **Im Journal geht das
nicht** (nie umschreiben): dort wären es drei angehängte Berichtigungszeilen.
Der Nachtrag ist eine Entwurfsstufe, die das Journal nicht hat.

### 3. Wer vergibt den Blockbuchstaben, und kann er kollidieren?

Heute misst ihn die einarbeitende Sitzung. Die Nachträge selbst hatten ihn
vorhergesagt, wo sie es taten, **3 von 3 richtig** (`(20h)` „voraussichtlich
`BV`", `(20i)` „`BW`", `(20j)` „nach `BW`"). Versuch im Wegwerf-Repo
(`schritt4_p3_git_kollision.txt`): zwei Klone messen `BT` und schreiben beide
`BU` an dieselbe Stelle — `push` **rejected**, `pull --rebase` **CONFLICT**,
`merge` **CONFLICT**. Ein stiller Doppelbuchstabe entsteht zwischen
Arbeitsbäumen nie, weil die Einfügestelle dieselbe Zeile ist. Er ist nur im
**selben** Baum möglich, wenn sich zwei Sitzungen zwischen Messen und Schreiben
überholen — der Fall aus Punkt 1, der nicht vorkam. Die Prüfung dafür ist
eine Zeile (`grep -o '^## [A-Z]\{1,2\} ' | sort | uniq -d`) und liegt in
`schritt2_blockbuchstaben.txt` bei.

### 4. Was bliebe vom Wächter übrig?

Gemessen am Code (`system/nachtragswaechter.py`, 518 Zeilen): der Journal-Anteil
ist der Zweig `elif m.group(1) == "JOURNAL"` in `pruefe_datei` (**7 Zeilen**,
Z. 328–334), die Methode `Ziel.quellenzeilen` und das Zählen der Quellenzeilen
im Umfang; im Test **2 von 12 Fällen** (6 „Journal ohne Quelle", 10 „Quelle über
Dateinamen"). Prüfung B (Textkern, Vergabevermerk mit Bindung) und C
(Doppelbelegung) — der Grund seines Baus, der Fall `(m)` — hängen ganz am
Backlog und bleiben.

⚠️ **Und der Umweg fällt nicht ganz:** von den 18 Journal-Nachträgen seit dem
19.09. kamen **7 vom Chat/Betreiber** ohne Terminal (`(19c)`–`(19g)`, `(20a)`,
`(20b)`; `schritt4_urheber_journal_nachtraege.txt`) — für sie gilt
`ARBEITSWEISE.md` 5b (*„IMMER als Auftrag an eine Sitzung, nie von Hand"*)
unverändert, und der Wächter behält dort seinen Gegenstand. **11 kamen von
Mac-Sitzungen**, die `numstat`, Einfügestelle und Blockmessung selbst können —
alle sieben seit TB-67.

**Was ein Wegfall für Mac-Sitzungen den Wächter kostet, ausdrücklich:** nicht
Code, sondern **Sicht**. Heute ist ein fehlender Block eine Datei im
Hauptordner — sichtbar, gemeldet ab dem zweiten Tag. Morgen ist ein fehlender
Mac-Block **nichts** — keine Datei, kein Befund. Ersatz wäre eine Wache
*„jedes `ERGEBNIS_TB-*.md` ab Stichtag hat seine `*Quelle:`-Zeile im Journal"*;
heute nennen **13 von 46** Ergebnisdokumente ihren Dateinamen dort, die Wache
müsste also ab einem Stichtag zählen. Das wäre ein eigener Auftrag, der den
gestern gebauten Wächter anfasst.

### 5. Trägt der Nachtrag etwas, das im Journal keinen Platz hat?

`(20m)` gegen `CA` je Abschnitt (`schritt4_p5_20m_gegen_CA.txt`, Wortformen ab
fünf Zeichen): 133 → 54 Zeilen (41 %). Kopf 73 %, Befunde 65 %, Fehler → Regel
56 %, *„In einfacher Sprache"* **15 %**. Nicht übernommen: die
Einarbeitungsanweisungen (Blockbuchstabe messen, Quellenzeile zum Kopieren —
**nur wegen des Umwegs nötig**), die Quellenzeile auf sich selbst, die
Alltagsfassung. Für die Alltagsfassung hat das Journal einen Platz (`BS` hat
eine). **Nichts im Nachtrag ist ohne Ort im Journal** — ausser dem, was den
Umweg selbst beschreibt.

⚠️ **Und die Verdichtung, die der Umweg verspricht, liefert er nicht
verlässlich:** TB-67 schrieb **965 Zeilen für 882 Zeilen Nachtrag** (109 % —
`BT` allein 125 Zeilen für 122), TB-75 352 für 869 (41 %). Eine von zwei
Einarbeitungen war eine Abschrift. Dazu der Verzug (`schritt4_umweg_dauer.txt`):
**0,7 bis 21,9 h** zwischen Nachtrag und Block, drei Einarbeitungssitzungen
(TB-54b, TB-67, TB-75) für 18 Nachträge, und 2 204 Zeilen Journal-Nachträge
unter `_eingearbeitet/`, die im Journal ganz oder verkürzt noch einmal stehen.

### Die Vorlage und die Entscheidung

Anklickbare Frage mit Empfehlung (`ARBEITSWEISE.md` 6d), drei Wege mit Preis:
**(a) direkt für Mac-Sitzungen** (empfohlen), **(b)** direkt plus Wache auf
Ergebnisdokumente, **(c)** Umweg beibehalten. ⭐ **Der Betreiber hat (a)
gewählt.** Was daraus folgt, steht in `K4n` und unten unter *Offen*; **diese
Sitzung ändert keine Regel** — nur ihren eigenen Block (Schritt 5).

---

## Schritt 5 / Nachweis 8 — Backlog-Zeile, Block `CB`, Abgabe

**K-Nummer gemessen:** `^\| \*\*(K\d[a-z])\*\*` ohne schliessenden Balken, kein
`sort -u`, über `BACKLOG.md` und `BACKLOG_ARCHIV.md`: `K4a`–`K4m` belegt, 0
doppelt → **`K4n`**, eine Zeile nach `K4m` in Abschnitt 4, `numstat 1 0`.

**Der Journalblock dieser Sitzung steht direkt im Journal** als **`CB`** — nach
Schritt 5 des Auftrags *(„falls Schritt 4 es nahelegt und der Betreiber
zustimmt, der Block direkt im Journal; dann sag es")*: **hiermit gesagt.** Er
ist der erste Block auf dem neuen Weg; seine Quellenzeile zeigt auf dieses
Ergebnisdokument, nicht auf eine Nachtragsdatei. Kein `JOURNAL_NACHTRAG_2026-09-21a.md`.

**Nachweis 8 — `git diff --numstat f0ca921..HEAD` je Datei:**

| Datei | + | − |
|---|---:|---:|
| `docs/auftraege/AKTUELLER_AUFTRAG.md` (Betreiber, Schritt 0) | 3 | 3 |
| `docs/auftraege/MAC_TB-75_journal_nachziehen.md` (Betreiber, Schritt 0) | 151 | 0 |
| `docs/projektfuehrung/JOURNAL.md` | **403** (352 Schritt 2 + 51 Block `CB`), 7 491 → 7 894 Zeilen, Quellenzeilen 14 → 22 | **0** |
| `docs/projektfuehrung/BACKLOG.md` | 1 | 0 |
| `docs/projektfuehrung/nachtraege/{ => _eingearbeitet}/JOURNAL_NACHTRAG_2026-09-20[g–m].md` | 0 | 0 (sieben Umbenennungen) |
| `docs/belege/TB-75/*` (17 Dateien, 2 641 Zeilen) | nur + | 0 |
| `docs/ERGEBNIS_TB-75_journal_nachziehen.md` | neu | 0 |
| **ausserhalb `docs/`** | `git diff --numstat f0ca921..HEAD -- . ':!docs'` → **0 Zeilen** | |

Nach dem Einfügen von `CB` lief der Wächter ein drittes Mal (`--knapp`): rc 0,
0 offen, 0 falsch verschoben — eine Quellenzeile auf ein Ergebnisdokument stört
ihn nicht, er zählt sie mit (22) und sucht seine Dateinamen darunter.

---

## Was der Auftrag vorgab, und wo die Messung abweicht

| Auftrag | gemessen |
|---|---|
| Abschnitt 0: *„Der Wächter meldet sie ab dem zweiten Morgen"* | richtig — und deshalb meldete er heute früh **nichts** (7 in der Frist, 0 darüber); die Menge stimmte |
| Schritt 2: *„am Ende von `JOURNAL.md`"* | vor `## Wiederkehrende Lehren`, wie alle Blöcke seit `BG` und wie `(20g)` es festhält — das Ende der Blockfolge, nicht der Datei |
| Schritt 4, Punkt 1: *„Commit-Zeitstempel zweier TB-Nummern überlappend"* | die wörtliche Messung liefert 102 Scheintreffer, weil Betreiber-Commits die TB-Nummer tragen; mit dem Trailer als Kennzeichen: 0 |
| Schritt 4, Punkt 2: *„halb geschriebener Journalblock"* | kam in drei Abbrüchen nicht vor; der messbare Unterschied ist die **Nachbearbeitung** (3 von 7 Nachträgen umgeschrieben) |
| Schritt 4: *„ist der Umweg noch nötig?"* | für Mac-Sitzungen nein (11 von 18); für Chat-Nachträge ja (7 von 18, `ARBEITSWEISE.md` 5b) — die Frage war eine für zwei Wege |
| Schritt 5: Journal-Nachtrag mit Quellenzeile | Block `CB` direkt, mit Zustimmung des Betreibers — gesagt |

## Fehler → Regel (`DOKUMENTATIONSSTANDARD.md` Regel 3)

| Fehler | ⇒ Regel |
|---|---|
| Erste Messung zu Punkt 1 zählte Commit-Spannen je TB-Nummer und fand 102 „Überlappungen" — darunter die Beauftragung von TB-64 (13:01) als Beginn einer Sitzung, die um 07:01 des Folgetags begann | ⭐ **Eine TB-Nummer im Commit-Text ist kein Sitzungskennzeichen.** Sitzung ist, was den `Co-Authored-By`-Trailer trägt; Beauftragung, Nachtrag und Merge tragen die Nummer auch |
| Die Zeitmessung „Nachtrag → Journal" nahm für `(19c)`–`(19e)` die Quellenzeile (TB-67) statt den Block (TB-54b, 31 h zu viel) | Bei einer Verzugsmessung nennen, **welches Ereignis** das Ende ist — Block und Quellenzeile kamen hier aus verschiedenen Sitzungen; die drei sind aus dem Mittel genommen (Rest: 0,7–21,9 h) |
| Ein `sed`-Filter zur Anzeige der Wächter-Ausgabe verdoppelte Zeilen im Bildschirmtext | Belegdatei per `tee` **vor** dem Filter — die Datei ist unverdoppelt; die Anzeige zählt nicht |

## Offen — für den Betreiber

| | wer |
|---|---|
| ⭐ **Die Entscheidung (a) eintragen:** `ARBEITSWEISE.md` 14 (Abgabe-Liste einer Mac-Sitzung: Block direkt statt Nachtrag), `DOKUMENTATIONSSTANDARD.md` 10 (Quellenzeile darf auf `ERGEBNIS_TB-*.md` zeigen; Chat-Nachträge unverändert) — Regeltexte, kein Teil von TB-75 | steuernder Chat / Betreiber |
| Optional: Wache *„Ergebnisdokument ab Stichtag ohne Quellenzeile im Journal"* — ersetzt die Sicht, die der Wächter für Mac-Blöcke verliert | eigener Auftrag |
| Cron-Zeile des Wächters (TB-64) weiterhin **nicht eingetragen** — gemessen: `crontab -l \| grep -c 'nachtragswaechter\|nachtraege'` = **0** (40 Zeilen crontab). Ohne sie meldet der Wächter nichts; er läuft nur, wenn eine Sitzung ihn aufruft | Betreiber |
| Projektablage nachziehen (`K4e`): Journal, Backlog, Ergebnisdokument, `AKTUELLER_AUFTRAG.md` (TB-75-Zeile) | steuernder Chat / Betreiber |
| Die vier `[?]`-Nachträge bleiben für den Wächter nicht prüfbar (A2), wie in TB-64 | — |

## Die Commits dieser Sitzung

| Commit | Schritt |
|---|---|
| `f1124ba` | 0 — zwei Betreiber-Dateien |
| `ac8bb9b` | 1 — Wächter vorher, Alter je Datei |
| `a096a7f` | 2 — Blöcke `BU`–`CA`, 352/0 |
| `d83ee02` | 3 — sieben `git mv`, Wächter nachher |
| `8d486ac` | 4 — Belege der Messung |
| Abgabe-Commit | 5 — `K4n`, Block `CB`, dieses Dokument |

Jeder Commit einzeln gepusht, `git push` nackt.

## In einfacher Sprache

**Was zu tun war:** Sieben Notizen ins Journal übertragen, die Wache zweimal
laufen lassen, und messen, ob der Umweg über Notizen noch nötig ist.

**Was herauskam:** Die sieben stehen im Journal, kurz und mit Zeigern; die Wache
sagte vorher „sieben liegen da, noch keine zu lange" und nachher „nichts liegt
da, alles angekommen" — beides richtig. Zur Frage: Wenn eine Mac-Sitzung ihren
Journaleintrag selbst schreibt, spart das eine spätere Sitzung und bis zu einen
Tag Verzug, und nichts, was gemessen wurde, spricht dagegen — ausser dass die
Wache einen fehlenden Eintrag dann nicht mehr sieht, weil keine Notiz mehr
herumliegt. Der Betreiber hat entschieden: Mac-Sitzungen schreiben direkt,
Notizen aus dem Chat gehen weiter den alten Weg. Dieser Eintrag ist der erste
auf dem neuen Weg.
