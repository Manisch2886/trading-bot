# Dokumentationsstandard

**Angelegt 19.09.2026, unmittelbar vor einem Chatumzug, auf die Frage des
Betreibers: *„Wird im neuen Chat dann auch alles nahtlos so dokumentiert wie du
es nun auch gemacht hast?"***

⚠️⚠️ **Der Anlass ist eine Lücke, nicht eine Vollständigkeit.** `ARBEITSWEISE.md`
regelt, **wohin** dokumentiert wird und **dass** jede Bewertung ihren Nachtrag
mitbringt (§5b). Sie regelt nicht, **wie ein Dokument aussehen muss**, damit es
in einem Jahr noch trägt. Das existierte bisher nur als Beispiel in den
Dokumenten selbst — und ein Beispiel ist keine Zusicherung.

**Verhältnis zu den übrigen Führungsdokumenten:**

| Dokument | regelt |
|---|---|
| `ARBEITSWEISE.md` | die **stehenden Anforderungen des Betreibers** |
| `PRUEFPRINZIPIEN.md` | die **gemessenen Lehren** aus fehlgeschlagenen Prüfungen |
| `UMZUG.md` | den **Wechsel** in einen neuen Chat |
| ⭐ **dieses Dokument** | **wie ein Dokument geschrieben wird**, damit es prüfbar bleibt |

---

## 1. ⭐⭐ Jeder Satz sagt, ob er gemessen oder erschlossen ist

**Die wichtigste Regel, und sie entstand am 19.09.2026 aus vier Fehlern an einem
Abend.**

> ⚠️⚠️ **Ein Name ist kein Messwert.**

**Die vier Fälle, die sie erzwungen haben:**

| | behauptet | tatsächlich |
|---|---|---|
| 1 | *„feinste Auflösung: 1 Stunde"* | aus dem Bezeichner `MIN_HISTORY_HOURS` **geschlossen**. Gemessen ergab sich etwas Schärferes: **174× `1d`, 25× `1h`, 24× `4h`** — Stundenauflösung nur bei Krypto |
| 2 | *„vier der neun Bots fallen durch"* | aus den **Botnamen** geschlossen (`volatility_breakout`, `turtle_soup_*`), nicht aus Renditeverteilungen |
| 3 | *„fünf Tests sind heute rechenbar"* | **gar nicht nachgesehen** |
| 4 | *„Rechnung an der Struktur des Entwurfs"* | die Eingangsgrößen waren **eigene Annahmen**, nicht die des Dokuments |

**Was daraus folgt, für jedes Dokument:**

| | |
|---|---|
| ⭐ **Gemessenes** trägt **wie** gemessen wurde und **wann** | *„gemessen 19.09., 21:03, an den Dateinamen in `data/` und den ersten Datenzeilen"* |
| ⚠️ **Erschlossenes** wird als solches markiert | *„aus dem Bezeichner geschlossen, nicht gemessen"* |
| ⚠️ **Nicht Nachgesehenes** wird ausdrücklich so genannt | *„nicht gemessen"* — **niemals ausgelassen.** Prüfprinzip A1: ein fehlgeschlagener Nachweis und ein leeres Ergebnis sehen gleich aus |
| ⭐ **Und wenn nicht gemessen werden DARF, steht der Grund dabei** | *„kein Zugriff auf die Datenbanken, solange eine Sitzung sie quersummengesichert hat — SQLite kann `-wal`/`-shm` anlegen"* |

⭐ **Der Prüfsatz für jeden geschriebenen Satz:** *Könnte ich sagen, woher ich das
weiß?* Wenn nein, wird der Satz umgeschrieben, nicht gestrichen — er bekommt sein
Etikett.

---

## 2. Jede Zahl trägt ihre Fundstelle

**Keine Zahl ohne den Ort, an dem sie nachprüfbar ist.**

| | |
|---|---|
| Hash, Commit, Dateizahl | Datei, Abschnitt oder Befehl, der sie erzeugt |
| Testergebnisse | der Beleg im Repo, nicht der Bericht daneben |
| ⚠️ **Zahlen aus fremden Berichten** | **an der Rohausgabe nachgerechnet**, bevor sie weitergereicht werden |

⚠️ **Und eine Zahl, die zwei Dinge messen kann, wird abgegrenzt.** *Beispiel: Der
Snapshot-Name `63e4b6c8…` läuft über 225 Dateien; `4fee547d…` in Abschnitt 17.9
über 223. Beide sind richtig; sie beantworten verschiedene Fragen. Das steht im
Register selbst, nicht in einem Bericht daneben — genau dort, wo in einem Jahr
jemand die falsche abschreiben würde.*

---

## 3. ⭐⭐ Eigene Fehler kommen als Tabelle „Fehler → Regel", nicht als Entschuldigung

**`ARBEITSWEISE.md` §9 sagt, dass eigene Fehler benannt werden. Dieses Dokument
sagt, in welcher Form** — und die Form ist der Unterschied zwischen einem
Eingeständnis und einer Verbesserung.

| | |
|---|---|
| ⭐ **Zweispaltig** | links der Fehler, **rechts die Regel, die daraus folgt** |
| ⭐ **In der Übergabe als eigener Block** | *am 19.09. Block 7, elf Einträge — der wertvollste Block des Dokuments* |
| ⚠️ **Keine Entschuldigung, keine Abschwächung** | *„folgenlos, weil der Zielordner gitignoriert ist — das war die Vorsichtsmaßnahme, nicht mein Wissen"* ist die richtige Form. „Zum Glück nichts passiert" ist es nicht |
| ⭐ **Auch fremde Korrekturen** | Fables drei Korrekturen am 19.09. stehen im selben Block wie die eigenen Fehler |

⚠️ **Ein Fehler ohne abgeleitete Regel ist unvollständig dokumentiert.** *Grund:
Ein neuer Chat liest die Regel und wiederholt den Fehler nicht; ein
Eingeständnis allein warnt niemanden.*

---

## 4. Berichtigung statt stillem Ersetzen

**Wird ein abgelegtes Dokument falsch, entsteht eine eigene Berichtigung.**

| | |
|---|---|
| ⭐ **Eigene Datei** oder eigener Abschnitt am Ende | *`BACKLOG_NACHTRAG_2026-09-19q_r_berichtigung.md`, 19.09.* |
| ⭐ **Sie nennt den falschen Satz wörtlich**, dann die Messung, dann den Ersatztext | |
| ⚠️ **Der falsche Satz wird nicht entfernt** | *dasselbe Prinzip wie im Register: nur hinzufügen* |
| ⚠️ **`numstat`: entfernte Zeilen = 0** | der Beleg, dass nichts verschwunden ist |

⚠️ **Und bei mehreren Nachträgen zum selben Dokument steht im letzten, dass er
gilt:** *„Die Blöcke 1, 2, 4, 5 und 8 oben stehen auf dem Stand 21:15. Bei
Widerspruch gilt dieser Nachtrag."*

---

## 5. Keine erfundene Nummer, kein erfundener Bezeichner

**Regel K2i, am 19.09.2026 aus vier Kollisionen an einem Tag entstanden — alle
vier von derselben Ursache.**

> ⚠️⚠️ **Ein Nachtrag nennt keine Nummer, die er nicht selbst gemessen hat.**
> Er schreibt *„die nächste freie Nummer, gemessen"* und begründet die
> Einordnung; die Nummer vergibt die einarbeitende Sitzung.

⭐ **Wo gemessen werden kann, wird gemessen und der Stand mit Datum genannt** —
*„Stand `d66a2ce`, 20:47: höchster Block `2r`, höchste K-Nummer `K2k`, höchste
Kettenzeile `0,97`."*

⚠️ **Und eine erfundene Nummer wird beim Einarbeiten mit Vermerk umgeschrieben**,
nicht stillschweigend korrigiert: *„im Nachtrag (h) als 0,87 vergeben; 0,87 war
bereits belegt — Betreiberentscheidung 19.09.2026."*

---

## 6. Jedes Dokument steht in mindestens zwei Trägern

⚠️ **Aus `UMZUG.md` Abschnitt 2, hier als Dokumentationsregel wiederholt, weil sie
am häufigsten gebrochen wird:**

| Träger | wofür |
|---|---|
| **Repo** | die Belege, versioniert |
| **Projektablage** | der Stand, sichtbar für jeden Chat und für Fable |
| **Erinnerung** | wie gearbeitet wird |

⚠️⚠️ **`logs/auftraege/` ist kein Träger** — über `.gitignore:27` (`logs/`)
ausgeschlossen, also ein Rechner und keine Version. **Jede Datei dort hat eine
offene Bringschuld ins Repo.** *Am 19.09. lagen dort elf Dateien mit fünf Epics,
und sie waren nicht dokumentiert, sondern geparkt.*

---

## 7. Der Abschluss jedes Dokuments

| | |
|---|---|
| ⭐ **„In einfacher Sprache"** | `ARBEITSWEISE.md` §4 — bei jeder aufbereiteten Rückmeldung von aussen, **im Dokument und am Ende der Chatantwort** |
| ⭐ **Sie wiederholt nicht, sie erklärt** | was wir wissen wollten · was herauskam · warum · was das bedeutet |
| ⚠️ **Auch die unangenehmen Teile** | *am 19.09.: „Ein Name ist kein Messwert" stand in der einfachen Sprache, nicht nur im Fachteil* |

---

## 8. Die Prüfliste für ein fertiges Dokument

**Acht Fragen. Eine mit „nein" bedeutet: noch nicht fertig.**

| | |
|---|---|
| **1** | Sagt jeder Satz, ob er gemessen oder erschlossen ist? |
| **2** | Trägt jede Zahl ihre Fundstelle? |
| **3** | Sind Zahlen, die verwechselt werden könnten, gegeneinander abgegrenzt? |
| **4** | Stehen eigene Fehler mit der Regel daneben, die aus ihnen folgt? |
| **5** | Ist keine Nummer genannt, die nicht gemessen wurde? |
| **6** | Ist das Dokument in mindestens zwei Trägern, und ist einer davon das Repo? |
| **7** | Steht am Ende „In einfacher Sprache", wenn es eine fremde Rückmeldung aufbereitet? |
| **8** | ⚠️ **Wenn es ein bestehendes Dokument ändert: `numstat` mit null entfernten Zeilen, oder jede entfernte Zeile ihrer Ersetzung zugeordnet?** |

---

## 9. Aktuell halten statt anhäufen — und was gelöscht werden darf

⚠️⚠️ **Anweisung des Betreibers, 20.09.2026:** *„…dass wir keinen unnötigen
Datenwachstum erzeugen, sondern die Dokumentation lediglich auf dem neuesten
Stand halten … alte, obsolete Informationen, die keinerlei Relevanz haben,
dürfen natürlich gerne gelöscht werden."*

> ⭐⭐ **Jede Änderung sagt, was sie ablöst — und das Abgelöste wird entfernt,
> nicht danebengestellt.**

| ⭐ darf gelöscht werden | ⚠️ darf NICHT gelöscht werden |
|---|---|
| Kopien und Entwürfe, deren Inhalt anderswo im Repo steht | **Das Register** `VORREGISTRIERUNG_neuselektion.md` samt Nachträgen |
| Rückblicke auf erledigte Aufgaben, **deren Lehre bereits als Regel geführt wird** | **`JOURNAL.md`** — ergänzen, nie umschreiben |
| Überholte Fassungen einer Regel, sobald die neue steht | **Backlog-Abschnitt 8** (Gestrichen) |
| Zwischenlager-Dateien mit erfüllter Bringschuld | **`PRUEFPRINZIPIEN.md`** |

⚠️ **Warum die vier Ausnahmen keine Bürokratie sind: dort IST die Aufzeichnung
das Produkt.** Ein Register, aus dem etwas entfernt werden kann, beweist nichts
mehr; eine Liste verworfener Ideen, die schrumpft, lässt sie zurückkommen. *Der
Rest der Dokumentation beschreibt einen Zustand — diese vier beschreiben, dass
etwas vorher feststand.*

⭐ **Die Faustregel für alles andere: die Regel behalten, den Fall streichen** —
aber nur, wenn die Regel den Fall wirklich trägt. Ein Satz Fall **innerhalb** der
Regel reicht; die lange Erzählung nicht.

⚠️ **Gelöscht wird nur mit Nachweis** (`ARBEITSWEISE.md` §6 bleibt): Was
verschwindet, wird vorher **byteweise gegen seinen Verbleib geprüft** oder
ausdrücklich als **ersatzlos** benannt.

---

## 10. Jeder Nachtrag hinterlässt eine prüfbare Spur

**Eingeführt 21.09.2026 (TB-64), nach dem Fall `(m)`:** ein Backlog-Nachtrag
vom 19.09. wurde nie eingearbeitet, seine sechs Nummern wurden an andere
Inhalte vergeben, und aufgefallen ist es zwei Tage später durch Zufall.
*Die einzige Wache war, dass jemand daran denkt — das ist keine.*

| | Regel | Form |
|---|---|---|
| ⭐ **Journal** | **Jeder Journalblock, der aus einem Nachtrag entstanden ist, nennt seine Quelldatei** in einer eigenen Zeile direkt unter der Kopfzeile | `*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_<datum><buchstabe>.md`*` — der Pfad nennt den Hauptordner, auch wenn die Datei später unter `_eingearbeitet/` liegt; die Kennung ist der **Dateiname**. Eine zweite Herkunft (etwa ein Messprotokoll aus einem Backlog-Nachtrag) heisst **anders**: `*Messprotokoll: …*` |
| ⭐ **Backlog** | Eine Nummer, die bei der Einarbeitung anders vergeben wird als im Nachtrag vorgeschlagen, trägt den **Vergabevermerk, der den Nachtrag nennt** (Regel 5) | `| **K2p** *(im Nachtrag (n) als `K2r` vorgeschlagen; … vergeben als `K2p`, gemessen)* |` — bzw. für einen Block: *„Nummer `2t` im Nachtrag (n) vorgeschlagen …"* |
| ⭐ **Ort** | **Ein eingearbeiteter Nachtrag wird nach `docs/projektfuehrung/nachtraege/_eingearbeitet/` verschoben.** Was im Hauptordner liegt, ist offen | `git mv`, kein Byte geändert — **erst, wenn jede seiner Nummern bzw. seine Quellenzeile im Ziel gemessen ist** |
| ⚠️ **Wache** | `system/nachtragswaechter.py` prüft täglich beides: was länger als einen Tag offen liegt, und ob von den verschobenen wirklich alles angekommen ist — **über Nummer *und* Textkern**, nicht über die Nummer allein | Meldung wie bei den vier Cron-Wächtern (`notifications/waechter_melden.py nachtraege`); `system/README_NACHTRAGSWAECHTER.md` |
| ⭐ **Auslagerung** | **Wer etwas aus `BACKLOG.md` in eine eigene Datei auslagert, nennt diese Datei in `BACKLOG.md` mit Namen, und sie heisst `BACKLOG_<name>.md`** — der Wächter liest seine Zielmenge daraus (seit 21.09.2026, TB-76; vorher stand sie fest im Code, und die Auslagerung der Epics machte ihn rot) | wie bei TB-60 und TB-63: Verweistabelle an der alten Stelle, Satz im Kopf. Fehlt die Nennung, meldet der Wächter die verschobenen Nummern als nicht angekommen (rc 1) |

### ⭐⭐ Berichtigt am 21.09.2026 (TB-75, Betreiberentscheidung): Eine Mac-Sitzung schreibt ihren Journalblock DIREKT

⚠️ **Der Umweg über eine Nachtragsdatei war eine Sitzung lang die Regel und ist
es für Mac-Sitzungen nicht mehr.** TB-75 hat gemessen, was gegen den direkten
Weg spricht — und nichts davon trug:

| geprüft | Befund |
|---|---|
| Laufen zwei Sitzungen gleichzeitig? | **Nein** — seit dem 19.09. kein verschränktes Paar auf `main`, je TB-Nummer getrennt gemessen |
| Was, wenn eine Sitzung mitten im Schreiben abbricht? | Am 20./21.09. brachen **vier** ab; keine hinterliess einen halben Block. Ein Kollisionsversuch im Wegwerf-Repo endete in `push rejected` und `CONFLICT` — **kein stiller Doppelbuchstabe** |
| Trägt der Nachtrag etwas, das im Journal keinen Platz hat? | `(20m)` gegen Block `CA` je Abschnitt verglichen: **nein** |
| Was kostet der Wegfall? | ⚠️ **Der Wächter verliert die Sicht auf Mac-Blöcke** — ohne Nachtragsdatei gibt es nichts, was offen liegen könnte. Prüfung B und C bleiben |
| Wie lange dauerte der Umweg? | **0,7 bis 21,9 Stunden** je Nachtrag, bis er im Journal ankam |

**Was seither gilt:**

| | |
|---|---|
| ⭐ | **Eine Mac-Sitzung fügt ihren Journalblock bei der Abgabe selbst ans Ende von `JOURNAL.md` an** — keine Nachtragsdatei mehr. Die Quellenzeile zeigt dann auf ihr **Ergebnisdokument**: `*Quelle: `docs/ERGEBNIS_TB-<nr>_<stichwort>.md`*` |
| ⚠️ | **Chat-Nachträge bleiben unverändert** — was der steuernde Chat schreibt, geht weiter als Nachtragsdatei in den Hauptordner und wird eingearbeitet wie bisher. **Der Wächter bleibt dafür zuständig** |
| ⚠️ | **Der Blockbuchstabe wird weiterhin gemessen**, nicht geraten — letzter Block plus eins, und `git` fängt eine Kollision ab, statt sie zu verschlucken |
| ⭐ | **Erster Block auf dem neuen Weg: `CB`** (TB-75, 21.09.2026) |

⚠️ **Offen, benannt und nicht geschlossen:** Für Mac-Blöcke gibt es keine Wache
mehr. Eine Probe *„Ergebnisdokument ab Stichtag ohne Quellenzeile im Journal“*
würde sie ersetzen; sie ist nicht gebaut.

⚠️ **Warum die Quellenzeile den Dateinamen und nicht die TB-Nummer trägt:** Ein
Nachtrag ohne TB-Nummer im Titel (`(f)` vom 19.09.) war über die Nummer nicht
prüfbar; über den Dateinamen ist jeder prüfbar. ⚠️ **Und warum der Wächter den
Textkern mitprüft:** bei `(m)` standen alle sechs Nummern im Backlog — mit
fremdem Inhalt. Eine Prüfung, die nur die Nummer sieht, hätte genau den Fall
grün gemeldet, für den sie gebaut wurde.

---

## In einfacher Sprache

**Warum dieses Dokument existiert:** Du hast vor dem Umzug gefragt, ob im neuen
Chat genauso dokumentiert wird wie heute. Die ehrliche Antwort war: **der Weg ja,
der Maßstab nur, wenn er aufgeschrieben wird.** Wohin etwas dokumentiert wird,
stand schon in der Arbeitsweise. **Wie ein Dokument aussehen muss, damit es in
einem Jahr noch trägt, stand nur als Beispiel in den Dokumenten selbst** — und
ein Beispiel kann man nachahmen oder eben nicht.

**Die wichtigste der acht Regeln:** Jeder Satz sagt, ob er **gemessen** oder
**geschlossen** ist. Das klingt nach Formalie und ist der häufigste Fehler
überhaupt — ich habe ihn heute Abend viermal gemacht. Dass eine Konstante
„Stunden" heißt, sagt nichts über die Auflösung der Daten. Dass ein Bot
„Ausbruch" heißt, sagt nichts über seine Gewinnverteilung.

**Die zweitwichtigste:** Ein eigener Fehler wird nicht als Entschuldigung
aufgeschrieben, sondern **zweispaltig — links der Fehler, rechts die Regel, die
daraus folgt.** Eine Entschuldigung warnt niemanden. Eine Regel verhindert die
Wiederholung.

**Was das für dich ändert:** nichts an deinem Aufwand. Es ändert, was du in einem
halben Jahr über die Dokumente sagen kannst, die heute entstanden sind.
