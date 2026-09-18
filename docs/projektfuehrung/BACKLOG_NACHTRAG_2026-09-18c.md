# Backlog-Nachtrag 18.09.2026 (c) — TB-50 und vier Berichtigungen

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a) und (b) voraus** — beide sind mit Commit `02de1f7` eingearbeitet.

> ⚠️ **Nichts wird entfernt** ausser den zwei ausdrücklich benannten
> Ersetzungen. Prüfung: `git diff --numstat`, jede entfernte Zeile zugeordnet.

---

## Berichtigung 1 — die Kettenzeile 0,82 widerspricht sich

**Zu finden** (eine Zeile in Abschnitt 3, „Die Kette"; sie enthält
`gemergt` **und** `Merge offen`):

```
| ~~0,82~~ | ~~TB-49 — die Ausnahme ins Werkzeug~~ | ⭐ **CLOUD FERTIG 18.09.**, Zweig `claude/new-session-kfbw56`, gemergt `2f241d1`. ⚠️ **Mac-Lauf und Merge offen** — der Mac-Lauf trägt hier wirklich etwas. Siehe Block **2h** |
```

⚠️ **Der genaue Wortlaut kann abweichen** — massgeblich ist: **die Zeile mit
`0,82`, die sowohl `gemergt` als auch `Merge offen` enthält.**

**Zu ersetzen durch:**

```
| ~~0,82~~ | ~~TB-49 — die Ausnahme ins Werkzeug~~ | ⭐ **ERLEDIGT 18.09.** — Cloud, Mac-Lauf (15:05–15:57, Python 3.9.6) und Merge `2f241d1`. **Beide Rechner liefern dieselben Zahlen.** Siehe Block **2h** |
```

> ⚠️ **Wie der Widerspruch entstand:** Der Nachtrag (b) wurde **vor** dem Merge
> geschrieben; beauftragt war nur das Einsetzen des Commits, nicht das
> Umschreiben des Satzes. **Meine Formulierung, nicht ein Fehler der Sitzung.**

---

## Berichtigung 2 — der Kopf von Block 2h

**Zu finden** (die Zeile unmittelbar unter der Überschrift von Block **2h**, die
`Mac-Lauf vor dem Merge` enthält):

```
⚠️ **Mac-Lauf vor dem Merge, nicht danach.**
```

**Zu ersetzen durch:**

```
⭐ **Mac-Lauf am 18.09. vor dem Merge gelaufen — alles bestätigt (T49.16), gemergt `2f241d1`.**
```

---

## Neuer Block 2i — aus TB-50

**Einzufügen NACH Block 2h.**

---

### 2i — Aus TB-50, Dokumentationspflege (Stand 18.09.2026)

**TB-50 ist erledigt — Mac-Sitzung, Commits `02de1f7` und `93eb894` auf `main`.**
⭐ **Erste Aufgabe nach dem neuen Regelweg (`ARBEITSWEISE.md` §5b): die
Mac-Sitzung legt ab und pusht selbst, ohne Zweig und ohne PR.**

| # | Punkt |
|---|---|
| **T50.1** | ⭐ **872 Zeilen hinzugefügt, 15 entfernt — jede der 15 einzeln ihrer Ersetzung zugeordnet.** `ARBEITSWEISE.md` 53/7 · `BACKLOG.md` 137/6 · `JOURNAL.md` **632/0** · `PRUEFPRINZIPIEN.md` **38/0** · `UMGEBUNGEN.md` 6/2 · `basislauf.py` **6/0**. ⭐ **Die Sicherung, die nicht zur Aufgabe gehört, hat gehalten:** `pruefe_register.py --basis a1e7fb4` **KEIN BEFUND, rc 0, vorher wie nachher**. Neun Datenbanken byteweise identisch, Datenstand `d9449faf…`/223 unverändert, kein Snapshot, `git status` nach dem letzten Commit leer |
| **T50.2** | ⭐⭐ **DIE BUCHSTABENPRÜFUNG HAT SICH SOFORT BEZAHLT GEMACHT.** Meine Annahme war *„letzter Journalblock ist AX"*; gemessen: **AZ**, 40 Blocküberschriften. **Versatz 2** ⇒ AY→BA, AZ→BB, BA→BC, BB→BD, BC→BE, BD→BF. ⚠️ **Nach meiner Annahme hätten zwei bestehende Blöcke denselben Buchstaben bekommen.** Verweise maschinell gesucht: keine zu ziehen. *Derselbe Fehlertyp wie die 2022 und die 62 — eine Zahl aus dem Gedächtnis, diesmal abgefangen* |
| **T50.3** | ⚠️⚠️ **`START_HIER.md` EXISTIERT NIRGENDS IM REPO** — weder unter `docs/`, noch im Wurzelverzeichnis, noch in `git ls-files`. **`ARBEITSWEISE.md` Abschnitt 10 führt sie als Pflichtbestandteil jedes Übergabepakets**, ebenso `STRATEGIEN_uebersicht.md`. ⚠️ **Das Übergabeverfahren verweist seit Wochen auf ein Dokument, das es nicht gibt — aufgefallen ist es erst, als jemand es öffnen wollte.** **Betreiberentscheidung: anlegen (der Stand-Text aus TB-50 Teil 4 liegt fertig vor) oder aus §10 streichen.** Teil 4 wurde ausdrücklich **nicht** ausgeführt, nichts angelegt |
| **T50.4** | ⚠️⚠️ **`basislauf.py` KENNT KEINE STUFE „FLACKERND" — und beide Alternativen sind falsch.** Die Datei kennt genau drei Listen: `BEKANNT_ROT`, `UNGEPRUEFT`, `LAEUFT_WEITER`. **Kein Eintrag ⇒ ein roter Lauf wird als UNERWARTET gemeldet (~30 %). Eintrag in `BEKANNT_ROT` ⇒ jeder grüne Lauf wird als UNERWARTET gemeldet (~70 %).** ⭐ **Das ist kein Umsetzungsfehler, sondern eine Lücke im Messwerkzeug.** Die Sitzung hat **keine Stufe erfunden**, wie verlangt, und den freigegebenen Kommentar unter den Streichungsvermerk gesetzt. **Eine vierte Stufe ist eine Änderung am Messwerkzeug: eigener kleiner Auftrag mit Mutationsprobe** |
| **T50.5** | ⭐ **Prüfprinzip A6 am Tag seiner Einführung angewandt:** `system/test_log_rotation.py` lief dreimal, **rc 0/0/0**. Die Sitzung rechnet selbst vor, dass das bei ~30 % Flackerrate **mit 34 % zu erwarten** ist und **nichts widerlegt** — und startet keinen weiteren Lauf, weil nicht beauftragt |
| **T50.6** | ⚠️ **Zwei weitere gealterte Zahlen, berichtet statt geändert:** die **1 312** im Docstring von `basislauf.py` (heute **1 315** mit `trading-env/`) und dieselbe gealterte **62**, die dort ebenfalls steht. **Nur die Stelle in `UMGEBUNGEN.md` war freigegeben** |
| **T50.7** | **Das Inhaltsverzeichnis des Journals (`## Inhalt`) endet bei AG** und wird seit langem nicht fortgeführt — auch AH–AZ fehlen. **Kein Handlungsdruck, aber es wächst** |
| **T50.8** | ⚠️ **Block AZ und der neue Block BA behandeln denselben Gegenstand** (TB-46 und die Fable-Runden). **Mein Nachtrag (a) hat einen Block geschrieben, den es schon gab** — BA bringt den Merge-Commit `135c306` hinzu. **Nichts zusammengelegt, nichts entfernt.** ⭐ **Die Lehre: vor dem Schreiben eines Journalblocks prüfen, ob der Gegenstand schon einen hat** |
| **T50.9** | ⚠️ **`ARBEITSWEISE.md` §5b widerspricht sich selbst:** Der neue Unterabschnitt sagt *„die Mac-Sitzung legt ab"*, der ältere Teil **„Der feste Ablauf"** darunter spricht weiter von `CLOUD_TB-<Nr>_dokumentationspflege.md` und *„Der Nutzer startet die Cloud-Sitzung"*. **Beim Einfügen nicht mitgezogen — meine Lücke.** ⭐ **In Berichtigung 3 dieses Nachtrags behoben** |
| **T50.10** | **Formentscheidungen der Sitzung, offen benannt und unbeanstandet:** Backlog-Blöcke als `## 2e…2h` statt `###` (sonst Unterabschnitte von 2d) · T47.9-Berichtigung und T34.10-Ergänzung als eigene Tabellenzeile darunter · A6 **innerhalb** von Abschnitt A · Journal-Überschriften in der Form der Datei (`## BA — …` ohne „Block") · Journalblöcke **vor** `## Wiederkehrende Lehren` eingefügt, wie beim letzten Nachtrag |

---

## Berichtigung 3 — `ARBEITSWEISE.md` §5b, „Der feste Ablauf"

⚠️ **Gehört in `docs/projektfuehrung/ARBEITSWEISE.md`, nicht ins Backlog** —
hier steht nur, was zu tun ist.

**Zu finden** (Abschnitt 5b, Unterabschnitt „Der feste Ablauf", Schritte 2 und 3):

```
2. **Ich formuliere die Aufgabe** (`CLOUD_TB-<Nr>_dokumentationspflege.md`), mit
   der Numstat-Auflage je Datei und der ausdrücklichen Regel, dass **nichts
   inhaltlich umformuliert** wird.
3. **Der Nutzer startet die Cloud-Sitzung** und legt parallel die Dateien aus
   Weg 1 selbst ab.
```

**Zu ersetzen durch:**

```
2. **Ich formuliere die Aufgabe** (`MAC_TB-<Nr>_<Kurzname>.md`), mit der
   Numstat-Auflage je Datei, dem wörtlichen Ankertext je Einfügestelle und der
   ausdrücklichen Regel, dass **nichts inhaltlich umformuliert** wird.
3. **Der Nutzer startet die Mac-Sitzung.** ⚠️ **Die Fassung v2.1.276 nimmt den
   Auftragstext NICHT aus dem `--remote-control`-Einzeiler mit** — die Sitzung
   öffnet und wartet; der Satz wird danach in ihre Eingabezeile eingefügt.
```

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K1n** | ⚠️ **`basislauf.py` braucht eine vierte Stufe „flackernd"** — siehe **T50.4**. Eigener kleiner Auftrag, mit Mutationsprobe |
| **K1o** | **Gealterte Zahlen im Docstring von `basislauf.py`** (1 312 und 62) — siehe **T50.6** |
| **K1p** | **Journal-Inhaltsverzeichnis endet bei AG** — siehe **T50.7** |
| **K1q** | ⚠️ **`STRATEGIEN_uebersicht.md` liegt ebenfalls nicht unter `docs/projektfuehrung/`** — dieselbe Frage wie **T50.3** |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — **entfernte Zeilen nur
   aus Berichtigung 1 und 2** (je eine), beide zugeordnet.
2. `git diff --numstat docs/projektfuehrung/ARBEITSWEISE.md` — **entfernte Zeilen
   nur aus Berichtigung 3** (vier).
3. `git branch --show-current && git status --short` **vor** dem Commit.
4. `git add` + `commit` + `push` **in einem Zug**, `git status` **danach**.
