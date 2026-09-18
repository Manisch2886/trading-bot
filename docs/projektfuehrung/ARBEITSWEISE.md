# Arbeitsweise — stehende Anforderungen des Nutzers

**Alles hier hat der Nutzer im Lauf der Zusammenarbeit ausdruecklich verlangt.
Es gilt dauerhaft, nicht nur fuer einzelne Aufgaben.**

> ⚠️ **Dieses Dokument wird bei JEDER Sitzungsuebergabe mitgegeben** — es ist
> Bestandteil des Uebergabepakets, nicht optional. Und **vor jeder Uebergabe
> wird der Nutzer gefragt, ob es noch passt oder ergaenzt werden soll**
> (Abschnitt 10).

> **Geprüfte Fassung vom 18.09.2026.** Neu in dieser Fassung: **5b** (wie die
> Dokumentation aktualisiert wird, mit dem Auslöser *„jede Bewertung bringt ihren
> Nachtrag mit"*), **6bb** (die Aufgaben des Betreibers am Ende jeder Antwort),
> **6d** (Entscheidungsvorlagen tragen eine Empfehlung), **7b** (Zugänge),
> **7c** (was in jedem Testauftrag steht), **11** (Änderungsverbote nennen ihren
> Zweck), **12** (Prüfprinzipien). Ergänzt: **2**, **6b**, **7**.
> ⭐ **Und ein Formfehler behoben:** Die Zeile zu Fable stand in der Tabelle
> von Abschnitt 1 mitten im Fliesstext; sie steht jetzt wieder in der Tabelle.

---

## 1. Die vier Wege — und sie werden IMMER benannt

Bei **jedem** Dokument und **jeder** Aufgabe wird ausdrücklich gesagt, wohin es
geht. Nicht nur in der Datei, auch in der Begleitnachricht.

| Weg | Wofür | Erkennbar an |
|---|---|---|
| **Cloud-Claude-Code** | Alle Aufgaben mit `TB-<Nummer>`. Läuft auf Anthropics Servern gegen das GitHub-Repo, erzeugt Branches und Pull Requests | Sitzungstitel im Dateikopf |
| **Claude Code am Mac** *(vom Nutzer „Remote" genannt, weil er ihn über die Mobil-App anspricht)* | Die `TESTAUFTRAG_*.md` aus dem Repo. ⚠️ **Immer als fertiger Einzeiler mit Dateipfad** *(ergänzt 15.09.2026)* — nicht „`claude` starten, dann Satz einfügen" | Dateiname beginnt mit `TESTAUFTRAG_` |
| **Claude Fable 5.1** | Die methodischen Fragen. **Ein durchgehender Chat** — Rückfragen gehören dorthin, nicht in einen neuen | Dateien heissen `RUECKFRAGE_`, `ANFRAGE_`, `RUECKMELDUNG_` |
| **Diese Sitzung** | Planung, Aufgaben schreiben, Ergebnisse einordnen, Backlog führen | — |

⚠️ **Der lokale Start wird IMMER als ein einziger, kopierfertiger Befehl
ausgegeben** *(ergänzt 15.09.2026)* — mit `cd` in den Projektordner, dem Aufruf
und dem Dateipfad im selben Befehl:

```
cd ~/trading-bot && claude --remote-control "Lies die Datei <PFAD> und arbeite sie als autonome Claude-Code-Sitzung vollständig eigenständig ab, wie darin beschrieben."
```

⚠️ **Das `--remote-control` gehört immer dazu** *(ergänzt 15.09.2026)*. Ohne
das Flag läuft die Sitzung rein lokal und erscheint **nicht** im Projekt auf
claude.ai oder in der Mobil-App — der Nutzer kann sie dann vom iPhone aus weder
verfolgen noch steuern. *(Alternative, einmalig: `/config` → „Enable Remote
Control for all sessions".)* Die Sitzung läuft dabei weiter auf dem Mac; Web
und App sind nur ein Fenster hinein. **Stoppt der Prozess, ist sie offline.**

> **Ausdrücklicher Wunsch des Nutzers, 15.09.2026:** *„Ich hätte dies zukünftig
> immer gerne zusätzlich im Web und der App, da mir diese Ansicht lieber ist
> als im Terminal."* Jede lokale Sitzung wird deshalb **immer** so gestartet,
> dass sie in Web und App erscheint — das Terminal ist der Ort, an dem sie
> läuft, nicht der, an dem gearbeitet wird.

*Begründung: zwei Schritte heissen zweimal kopieren, und der lange Satz hat
über Termius schon Zeilenumbrüche verloren. Ein Befehl, eine Zeile, ein Einfügen.*
Dasselbe gilt für jeden anderen Zugriff auf eine Datei: **Pfad immer mitgeben,
nie beschreiben.**

**Bei Fable immer dazusagen: bestehender Chat oder neuer?** Faustregel: Bezieht
sich die Frage auf Fables eigene frühere Aussagen oder auf seine Kürzel
(`S-B1`, `S-E1` …), gehört sie in den **bestehenden**. Soll er ergebnisoffen
ohne Vorbelastung antworten, in einen **neuen**.

**Eine Sitzung je Aufgabe, immer frisch von `main`.** Nach einem Merge nicht auf
demselben Branch weiterarbeiten — das erzeugt tote PRs.

---

## 2. Ausgaben

- **Jedes Ergebnisdokument wird als Download-Datei bereitgestellt.**
- ⚠️ **Das gilt für ALLE vier Wege** *(ergänzt 15.09.2026)* — Cloud-Aufgaben,
  Testaufträge für die lokale Sitzung **und Anfragen an Fable**. *Nie als
  Chat-Text zum Herauskopieren: lange Texte brechen beim Kopieren, und der
  Nutzer braucht sie in einem anderen Fenster.*
- ⚠️ **Dateiname UND Überschrift nennen den Empfänger** *(ergänzt 15.09.2026)*.
  Der Nutzer führt oft vier Sitzungen parallel und hat Dutzende Downloads im
  selben Ordner — am Namen allein muss erkennbar sein, wohin eine Datei geht:

  | Weg | Dateiname | Überschrift |
  |---|---|---|
  | Cloud-Claude-Code | `CLOUD_TB-<Nr>_<Kurzname>.md` | `# TB-<Nr> <Kurzname> — an: Cloud-Claude-Code` |
  | Claude Code am Mac | `MAC_TESTAUFTRAG_<Kurzname>.md` | `… — an: Claude Code am Mac (lokale Sitzung)` |
  | Fable 5.1 | `FABLE_RUECKFRAGE_<Kurzname>.md` | `… — an: Fable 5.1, bestehender Chat` |

  Bei Fable gehört **bestehender oder neuer Chat** in die Überschrift, nicht nur
  in den Text.
- ⚠️ **Immer gebündelt als ZIP — auch bei einer einzigen Datei, und immer ALLE
  Ausgaben einer Antwort in EINEM Archiv** *(verschärft 15.09.2026)*. Nicht
  mehrere Archive nebeneinander, nicht „ZIP erst ab zwei Dateien". Wer vom
  iPhone arbeitet, lädt einmal und hat alles.
- **Die einzelnen Dateien zusätzlich**, nicht nur das Archiv — ein kurzes
  Dokument liest sich im Chat schneller als nach dem Entpacken.
- ⚠️ **Das Archiv trägt IMMER den Namen der Sache, die es liefert**
  *(ergänzt 15.09.2026)* — bei Aufgaben `TB-<Nr>_<Kurzname>.zip`. Gibt es keine
  TB-Nummer, gilt das Kürzel des Backlog-Punkts oder der Dokumenttyp
  (`V5b_…`, `UEBERGABE_…`, `RUECKFRAGE_…`). **Nie ein generischer Name wie
  `AUSGABEN_<Datum>.zip`** — der Nutzer hat Dutzende Downloads im selben Ordner
  und muss am Namen erkennen, wozu ein Archiv gehört.
- Dasselbe verlangen die Aufgabendokumente von den Cloud-Sitzungen: ZIP,
  benannt nach der Aufgabe (`TB-<Nr>_<Kurzname>.zip`), Einzeldateien daneben.
- ⚠️ **Das gilt genauso für die lokale Claude-Code-Sitzung** *(ergänzt
  15.09.2026, nachdem TB-34 am Mac kein Archiv erzeugte und der Nutzer es von
  Hand anfordern musste)*. **Jedes `TESTAUFTRAG_*.md` muss die ZIP-Pflicht
  selbst enthalten** — Lauf-Bericht, Ergebnisdokument und Protokolle gebündelt,
  benannt nach der Aufgabe, Ablage in `~/Downloads` (**nicht** ins Repo, sonst
  blockiert eine unversionierte Datei den nächsten Pull).
- ⚠️ **Und für Mac-Läufe, die im Chat Schritt für Schritt angewiesen werden**
  *(ergänzt 15.09.2026)*. Erzeugt eine solche Folge von Befehlen einen Befund,
  der später noch gebraucht wird — eine Messung, eine Faltenzahl, ein Hash —,
  wird die Ausgabe **in eine Datei geschrieben und am Ende als ZIP gesichert**,
  nicht nur in den Chat kopiert. *Sonst existiert der Beleg nur als Text in
  einer Sitzung, die endet.*
  > **Am 15.09.2026 betraf das mehrere Befunde:** den Faltenplan mit
  > `--mindesttraining 0` (der die ganze Umfangsentscheidung trug) und die
  > Ausgabe von `herkunft.py` mit dem neuen Datenstand-Hash.
  > **Die Kette, an der es lag:** Das Testdokument schreibt die *Cloud*-Sitzung.
  > Steht die Anforderung nur in ihrem eigenen Abgabeteil, gibt sie sie nicht
  > weiter. **Also gehört sie ausdrücklich in den Auftrag an die Cloud-Sitzung:**
  > *„Das Testdokument verlangt am Ende ebenfalls ein ZIP der dort entstehenden
  > Ergebnisse."*

  ⚠️ **Und beim Abnehmen jeder Cloud-Übergabe wird nachgesehen, ob das
  Testdokument die ZIP-Pflicht wirklich enthält** *(ergänzt 16.09.2026)* — nicht
  erst dann, wenn der Mac-Lauf ohne Archiv endet. *Ein Satz im Auftrag ist eine
  Anforderung; erst die Prüfung macht ihn zur Zusicherung.* Dasselbe gilt für
  „In einfacher Sprache": beides gehört auf dieselbe Abnahmeliste.
- ⚠️ **`ARBEITSWEISE.md`, `JOURNAL.md` und `BACKLOG.md` werden NICHT bei jeder
  Änderung mitgeschickt** *(ergänzt 15.09.2026, verschärft am selben Tag)*. Sie
  werden weiterhin fortlaufend gepflegt, und geänderte Regeln werden **im Chat
  genannt**, mit Datum und Abschnitt. *Sonst gehen die Dokumente, um die es in
  der Antwort wirklich geht, zwischen wiederkehrenden Anhängen unter.*

  **Stattdessen wird der Nutzer zu geeigneten Zeitpunkten an den Download
  erinnert** — am Ende eines Arbeitsabschnitts, vor einer längeren Pause, vor
  jeder Übergabe, und wenn viel Ungesichertes aufgelaufen ist. **Und dann
  werden sie samt aller nötigen Schritte bereitgestellt:** wohin speichern,
  welche Datei ersetzt welche, und ob etwas ins Repo abzulegen ist.
- ⚠️ **Die Sicherung geht IMMER ins Repo, nach `docs/projektfuehrung/`**
  *(ergänzt 16.09.2026, eingerichtet am selben Tag)*. Nicht in den
  Downloads-Ordner und dort liegenlassen. **Der feste Ablauf, jedes Mal:**

  1. **Einzeldateien** anbieten, nicht nur das Archiv — ein ZIP muss erst
     entpackt werden, und der Downloads-Ordner benennt Doppelte still um.
  2. `git branch --show-current && git status --short` — ⚠️ **auf `main` stehen
     und sauber sein**, sonst landet die Ablage auf einem Zweig.
  3. ⚠️ **`ls -lt` auf die heruntergeladenen Dateien, und die BYTEGRÖSSEN gegen
     die angebotenen prüfen.** *Am 16.09. lagen drei Fassungen von `JOURNAL.md`
     gleichzeitig im Downloads-Ordner — `JOURNAL.md`, `files-15/JOURNAL.md` und
     `SICHERUNG_projektfuehrung/JOURNAL.md`. Sie waren zufällig identisch. Ohne
     Prüfung wäre das Glück gewesen, nicht Verfahren.*
  4. Kopieren, **Grössen erneut prüfen**, dann `git add` + `commit` + `push`
     **in einem Zug** — eine unversionierte Datei blockiert sonst den nächsten
     Pull (P.2).

  > ⚠️ **Ab der ersten Ablage ist die Fassung im Repo die massgebliche.** Jede
  > Änderung in einer Sitzung muss denselben Weg zurücknehmen — herunterladen,
  > kopieren, committen. *Sonst laufen zwei Fassungen auseinander, wie es bei den
  > zwei Symbolzahl-Tabellen (15.5 gegen 16.1.1) bereits passiert ist.*

  **Der Gewinn, der über das Sichern hinausgeht:** Die Cloud-Sitzungen können
  `docs/projektfuehrung/ARBEITSWEISE.md` **lesen**. Stehende Regeln müssen nicht
  mehr in jedes Aufgabendokument abgeschrieben werden — ein Verweis genügt.
  *Das ist P.4 („die Sitzungen sehen einander nicht") an einer Stelle behoben.*

- ⚠️ **Grosse Dokumente werden NICHT vollständig neu geschrieben, sondern als
  Nachtrag geliefert** *(ergänzt 18.09.2026)*. Für `BACKLOG.md` und `JOURNAL.md`
  gilt: **neue Blöcke plus benannte Ersetzungen**, mit Angabe, **an welche
  Stelle** sie gehören — nicht die ganze Datei. *Das ist derselbe Mechanismus,
  den das Register benutzt (`VORREGISTRIERUNG` + Nachtrag), und er hat dieselbe
  Begründung: Wer eine 2000-Zeilen-Datei neu schreibt, verliert unbemerkt
  Zeilen. Ein Nachtrag mit `null entfernte Zeilen` ist prüfbar.*
  **`ARBEITSWEISE.md` ist die Ausnahme** — sie wird ganz geliefert, weil
  Cloud-Sitzungen sie lesen und eine in zwei Dateien verteilte Regelsammlung
  ihren Zweck verliert.

> *Hintergrund: Der Nutzer arbeitet oft vom iPhone. Textdateien sind mehrfach
> leer angekommen — **ZIP hat immer funktioniert**.*

---

## 3. Jedes Aufgabendokument trägt im Kopf

```
# TB-<Nummer> <Kurzname>

**Sitzungstitel für Claude Code: `TB-<Nummer> <Kurzname>`**
**Modell: Opus 5, Aufwand hoch.**

Repo: Manisch2886/trading-bot, Base main. Frisch von main aufsetzen.
```

**Der Sitzungstitel ist Pflicht** — der Nutzer führt oft vier Sitzungen
parallel und muss sie zuordnen können.

**Modell:** Standard ist **Opus 5, Aufwand hoch**. Weicht die Empfehlung ab,
wird sie **begründet dazugeschrieben** — etwa Fable 5.1 bei Untersuchungen mit
offener Fragestellung, Sonnet 5 bei reiner Ausführungsarbeit ohne
Ermessensspielraum.

---

## 4. Jedes Ergebnis endet mit „In einfacher Sprache"

Nach der fachlichen Einordnung **immer** ein kurzer Abschluss in Alltagssprache:

> **Was wir wissen wollten** · **Was herauskam** · **Warum das so ist** · **Was
> das für dich heisst**

Kein Fachbegriff ohne Erklärung, keine Kennzahl ohne Einordnung. Dieser
Abschnitt steht auch **im Journal** bei jedem Ergebnisblock — damit er nicht
verlorengeht, wenn die Sitzung endet.

⚠️ **Eingegrenzt am 15.09.2026: nur bei Rückmeldungen von aussen — dort aber
IMMER, und zwar AUCH in der Chat-Antwort.** Sobald ein fremdes Ergebnis
aufbereitet wird — Cloud-Claude-Code, Fable, die lokale Claude-Code-Sitzung —
gehört die einfache Sprache **sowohl ins Ergebnisdokument als auch ans Ende der
Antwort im Chat**. *Der Nutzer entscheidet im Chat; ein Abschnitt, der nur in
der Datei steht, erreicht ihn dort nicht.* **Nicht** in die laufende Planungs-
und Abstimmungsunterhaltung; dort ist sie überflüssig und verlängert nur.

> *Begründung des Nutzers, 15.09.2026: „In der Kommunikation mit dir benötige
> ich eine einfache Sprache nicht."* Die Regel entstand, weil **fremde
> Rückmeldungen** zu technisch kamen — nicht, weil die Abstimmung hier
> unverständlich wäre.

**Die Prüffrage:** Berichte ich, was jemand anderes geliefert hat? Dann ja.
Rede ich mit dem Nutzer über das nächste Vorgehen? Dann nein.

---

## 5. Das Backlog wird fortlaufend geführt

- **`BACKLOG.md` ist die kanonische Quelle.** Bei Widerspruch zu Notizen gilt
  die Datei.
- **Jedes offene Thema, jede getroffene und jede ausstehende Entscheidung**
  wird eingetragen — auch Ideen, die verworfen wurden, **mit Begründung**,
  damit sie nicht in sechs Monaten erneut vorgeschlagen werden.
- **`JOURNAL.md`** nimmt die abgeschlossenen Ergebnisblöcke auf und wird **nie
  umgeschrieben**, nur ergänzt.
- Nach jedem relevanten Abschnitt: beide Dateien aktualisieren und **als
  Download ausgeben**.
- ⚠️ **Fortschreiben spätestens bei der Übergabe, und dann vollständig**
  *(ergänzt 18.09.2026)*. Am 18.09. lagen **drei erledigte Aufgaben** (TB-46b,
  TB-47, TB-48) und **zwei Fable-Runden** ausserhalb beider Dateien — nur in
  Chat-Bewertungen und ZIP-Archiven. *Ein Backlog, das eine Woche hinterherläuft,
  ist beim Übergeben keine kanonische Quelle, sondern eine Momentaufnahme von
  vorletzter Woche.*

---

## 5b. Wie die Dokumentation aktualisiert wird

⚠️⚠️ **Ausdrückliche Anweisung des Nutzers, 18.09.2026: *„mache das zukünftig
immer so."* Der Ablauf ist damit festgelegt, nicht Einzelfallentscheidung.**

**Es gibt drei Wege, und nur zwei davon gehen über das Terminal:**

| Weg | Wofür | Wie |
|---|---|---|
| **1 — ganz ersetzen** | Dokumente, die kurz genug sind, um sie vollständig zu schreiben: `ARBEITSWEISE.md`, `PRUEFPRINZIPIEN.md`, `UMGEBUNGEN.md`, `START_HIER.md` | **Der Nutzer legt sie selbst ab**, nach dem Ablauf in Abschnitt 2 (Grössen prüfen, kopieren, `add`+`commit`+`push` in einem Zug). *Die alte Fassung steckt in git; es geht nichts verloren* |
| ⭐ **2 — Nachtrag** | ⚠️ **`BACKLOG.md` und `JOURNAL.md`** — und jede andere Datei über ein paar hundert Zeilen | **IMMER als eigene kleine Cloud-Aufgabe**, nie von Hand. Siehe unten |
| **3 — neu dazulegen** | ein neues Dokument | wie Weg 1 |

### Warum Weg 2 zwingend in eine Cloud-Aufgabe gehört

**Die Regel des Projekts lautet „null entfernte Zeilen", und sie muss an der
git-Zeile belegt sein, nicht am Gefühl.** Ein Nachtrag von mehreren hundert
Zeilen, mit Ersetzungen mitten im Text, über Termius in eine 4000-Zeilen-Datei
einzufügen, ist genau die Operation, bei der Zeilen verschwinden und es niemand
merkt.

**Was die Cloud-Sitzung dabei leistet und das Terminal nicht:**

| | |
|---|---|
| ⭐ **`git diff --numstat` je Datei** | der Beleg, den TB-48 für das Register geliefert hat (`506 0`) |
| **die Ersetzungen exakt treffen** | benannte Stellen statt Suchen und Scrollen |
| ⭐ **prüfen statt raten** | *welcher Journal-Block ist wirklich der letzte?* — ein falscher Buchstabe macht jeden Backlog-Verweis wertlos |
| **mehrere Dateien in einem Zug** | `BACKLOG`, `JOURNAL`, `START_HIER`, `UMGEBUNGEN` zusammen, mit einem Nachweis je Datei |

### Der Auslöser: jede Bewertung bringt ihren Nachtrag mit

⚠️⚠️ **Festgelegt am 18.09.2026, weil der weiche Auslöser der eigentliche Fehler
war.**

> **„Fortlaufend führen" stand schon vor dem 18.09. in Abschnitt 5 — und diese
> Sitzung hat drei erledigte Aufgaben und zwei Fable-Runden eine Woche lang nur
> in Chat-Bewertungen liegen lassen.** *Eine Regel, die einen unbestimmten
> Zeitpunkt nennt, wird verschoben. Nicht aus Nachlässigkeit, sondern weil es
> immer etwas Dringenderes gibt.*

**Deshalb hängt die Fortschreibung ab jetzt an einem Ereignis, das ohnehin jedes
Mal eintritt:**

| | |
|---|---|
| ⭐ **Jede Bewertung eines Ergebnisses bringt ihren Backlog- und Journal-Nachtrag im SELBEN Archiv mit** | Kommt ein ZIP von einer Cloud- oder Mac-Sitzung zurück, bekommt der Nutzer nicht nur die Einordnung, sondern auch die Blöcke zum Ablegen |
| **Gilt auch für Fable-Antworten** | eine methodische Festlegung ist ein Ergebnis wie jedes andere |
| **Gilt auch, wenn der Nachtrag kurz ist** | drei Zeilen sind ein Nachtrag. *Ein ausgelassener kurzer Nachtrag ist der Anfang eines langen* |

**Der Preis, benannt:** ein paar Dateien mehr je Runde.
**Der Gewinn:** es gibt keinen Zeitpunkt mehr, an dem es *„später"* heisst.

⚠️ **Und es bleibt bei EINEM Archiv je Antwort** (Abschnitt 2) — der Nachtrag
kommt **hinein**, nicht daneben.

### Der feste Ablauf

1. **Ich schreibe den Nachtrag** — neue Blöcke plus **benannte** Ersetzungen, mit
   Angabe, an welche Stelle sie gehören.
2. **Ich formuliere die Aufgabe** (`CLOUD_TB-<Nr>_dokumentationspflege.md`), mit
   der Numstat-Auflage je Datei und der ausdrücklichen Regel, dass **nichts
   inhaltlich umformuliert** wird.
3. **Der Nutzer startet die Cloud-Sitzung** und legt parallel die Dateien aus
   Weg 1 selbst ab.
4. **Vor dem Merge** wie immer: Merge-Basis-Vergleich, `numstat` gegenlesen,
   `git status` **nach** dem letzten Commit (Abschnitt 7).

⚠️ **Die Aufgabe berührt ausschliesslich `docs/`** — sie läuft damit **parallel**
zu jeder fachlichen Aufgabe, ohne mit ihr zu kollidieren.

⚠️ **Und der Stand-Abschnitt in `START_HIER.md` wird bei jeder solchen Runde
mitgeschrieben.** *Ein Einstiegsdokument, dessen Stand von letzter Woche ist,
führt die nächste Sitzung in die Irre — genau der Fehler aus P.4.*

---

## 6. Nichts wird verworfen oder gelöscht, ohne vorher zu fragen

Gilt für Notizen, Dateien, Backlog-Einträge — **alles**. Wenn etwas verdrängt
oder überschrieben werden müsste, wird vorher gefragt.

⚠️ **Und: Vor jedem drohenden Verlust wird ausdrücklich gewarnt**
*(ergänzt 15.09.2026)*. Der Nutzer lädt dann vorher eine Sicherung herunter.
**Zu warnen ist insbesondere:**

- bevor eine Datei ersetzt oder eine Fassung überschrieben wird,
- wenn ungesicherte Änderungen an `BACKLOG.md`, `JOURNAL.md` oder
  `ARBEITSWEISE.md` aufgelaufen sind und ein Arbeitsabschnitt endet,
- vor jeder Sitzungsübergabe.

> ⚠️ **Die Grenze dieser Zusage, ehrlich benannt:** Ein unerwarteter
> Sitzungsabbruch oder ein Zurücksetzen des Arbeitsordners kündigt sich nicht
> an — davor kann **nicht** gewarnt werden. **Der Arbeitsordner der Sitzung ist
> kein Speicherort.** Die einzige dauerhafte Fassung ist die, die der Nutzer
> heruntergeladen hat. Deshalb wird ein Download **an jedem abgeschlossenen
> Abschnitt** angeboten, nicht erst am Ende.

---

## 6b. Anweisungen an den Nutzer

⚠️ **Schritt für Schritt, nummeriert** *(ergänzt 15.09.2026)*. Keine
zusammengefassten Absätze, aus denen der Nutzer sich die Handlung selbst
heraussuchen muss.

**Je Schritt drei Angaben:**

| | |
|---|---|
| **Was** | die Handlung, so konkret wie möglich — Knopfname, Menüpunkt, Befehl |
| **Wo** | in welchem Fenster, welcher App, welchem Ordner |
| **Woran du merkst, dass es geklappt hat** | das erwartete Ergebnis, an dem der Nutzer prüfen kann, ob er richtig ist |

**Dazu:** bei Dateien immer sagen, **wo sie liegen müssen** (Mac oder iPhone,
welcher Ordner). Bei mehreren Wegen sagen, **welcher zuerst** kommt und ob die
Reihenfolge zwingend ist. Und benennen, **was schiefgehen kann** und was dann
zu tun ist.

⚠️ **Auch dann, wenn der Schritt trivial aussieht** *(ergänzt 18.09.2026)*.
Der Nutzer hat in dieser Sitzung **viermal** „leite mich step by step an"
wiederholen müssen — jedes Mal an einer Stelle, die ich für offensichtlich
hielt (ein Merge, ein Pfad, ein Kopierbefehl). *Was für mich ein Schritt ist,
sind im Terminal drei.* **Die Regel gilt ohne Ausnahme; sie einmal abzukürzen
kostet mehr Nachrichten, als sie spart.**

---

## 6bb. Die Aufgaben des Betreibers werden am Ende jeder Antwort benannt

⚠️⚠️ **Ausdrückliche Anweisung des Nutzers, 18.09.2026: *„weise mich immer
detailliert auf meine Aufgaben hin."***

**Jede Antwort, aus der für den Nutzer etwas zu tun folgt, endet mit einem
eigenen, abgesetzten Block — nicht in den Fliesstext eingestreut.**

| | |
|---|---|
| **Überschrift** | „Deine Aufgaben" oder „Was du jetzt tust" — **sichtbar abgesetzt** |
| **nummeriert** | in der Reihenfolge, in der sie zu tun sind |
| **je Aufgabe** | **Was · Wo · Woran du merkst, dass es geklappt hat** (Abschnitt 6b) |
| ⭐ **dazu, was NICHT von ihm abhängt** | *„läuft ohne dich"*, *„ich warte auf das Archiv"* — damit er nicht sucht, was er übersehen haben könnte |
| ⚠️ **und wenn nichts zu tun ist: das ausdrücklich sagen** | *„Nichts zu tun. Ich warte auf X."* **Kein erfundener Aufgabenblock**, nur damit einer dasteht |

**Warum das nicht schon in 6b stand:** 6b sagt, **wie** eine Anweisung aussieht.
Dieser Abschnitt sagt, **dass am Ende jeder Antwort eine vollständige Liste
steht** — auch dann, wenn die Aufgaben über die Antwort verstreut schon genannt
wurden. *Der Nutzer führt oft vier Sitzungen parallel; was nicht an einer Stelle
gebündelt steht, geht unter.*

⚠️ **Auch bei Wartezuständen.** Wartet eine Sitzung auf ein Archiv, gehört in den
Block: **was wann von wem kommt, und was in der Zwischenzeit zu tun ist.**

---

## 6c. Keine Hinweise auf Arbeitszeit

⚠️ **Ausdrücklicher Wunsch des Nutzers, 16.09.2026:** **Keine Bemerkungen zu
Tageszeit, Arbeitsdauer oder einem Arbeitsende.** Kein „es ist spät", kein „mach
Schluss für heute", kein „das kann warten, schlaf erst". **Wann er arbeitet und
wann er aufhört, entscheidet er selbst.**

*Sachliche Terminhinweise bleiben davon unberührt* — Fristen, Reihenfolgen,
„dieser Schritt dauert 20 Minuten", „das Vergleichsfenster beginnt mit diesem
Lauf". Gemeint ist die **Aufforderung**, nicht die Information.

---

## 6d. Jede Entscheidungsvorlage trägt eine Empfehlung

⚠️ **Neu am 18.09.2026, weil der Nutzer in dieser Sitzung dreimal nachfragen
musste: *„was würdest du empfehlen?"***

**Wo eine Entscheidung ansteht, stehen drei Dinge beieinander:**

| | |
|---|---|
| **die Möglichkeiten** | vollständig, jede mit ihrem Preis |
| ⭐ **die Empfehlung** | **eine** davon, ausdrücklich benannt |
| **die Begründung** | warum diese, und **was sie schlechter macht** als die anderen |

**Warum das keine Anmassung ist:** Die Entscheidung bleibt beim Betreiber — bei
Freigaben für Sperrlisten-Dateien, beim Risikoschlüssel, beim Termin des Laufs.
Aber *„hier sind drei Wege"* ohne Empfehlung verlagert die Vorarbeit zurück auf
ihn, und er hat die Möglichkeiten nicht selbst durchgerechnet. **Eine benannte
Empfehlung ist widersprechbar; eine ausgelassene ist nur Arbeit.**

⚠️ **Die Grenze:** Wo die Entscheidung von etwas abhängt, das nur der Betreiber
weiss — seine Risikotragfähigkeit, seine verfügbare Zeit, sein Wohnsitzrecht —
wird das **gesagt** statt geraten. *Beispiel 16.09.: beim Aktien/Krypto-Schlüssel
war die Messung meine Aufgabe, die Wahl seine.*

---

## 7. Terminal-Arbeit

- **Ein Befehl je Nachricht.** Nicht mehrere hintereinander.
- **Vor jedem `git pull`: `git status --short`.** Lokale Änderungen haben
  bereits mehrfach einen Pull abgebrochen.
- Bei SSH-Sitzungen vorher `pwd` und `git branch --show-current` prüfen.
- **Secrets nie anzeigen** — `grep -c` statt `cat`. Zugangsdaten, Token und
  Schlüssel niemals in den Chat kopieren lassen.
- ⚠️ **Schärfer gefasst am 15.09.2026: Es wird gar kein Befehl vorgeschlagen,
  dessen Ausgabe einen Schlüssel enthalten KÖNNTE.** Nicht „vorsichtig
  kopieren", sondern: der Befehl entsteht nicht. *Der Nutzer kopiert die
  Terminalausgabe im Block zurück — das ist der Arbeitsablauf, nicht seine
  Unachtsamkeit. Die Sorgfaltspflicht liegt damit beim Formulieren des Befehls.*

  **Nie vorschlagen:** `cat`, `head`, `tail`, `less`, `more`, `env`,
  `printenv`, `echo $VAR`, `set` auf `.env`, Konfigurationsdateien,
  Schlüsselablagen oder Logs, die Anfragen protokollieren · `git diff` oder
  `git show` auf solchen Dateien · `security find-generic-password` ·
  jedes `curl` mit Header im Klartext.

  **Stattdessen, und es reicht fast immer:** `grep -c "NAME=" datei`
  (kommt der Eintrag vor?) · `test -f datei && echo vorhanden` ·
  `wc -l datei` · `grep -q "NAME=" datei && echo GESETZT || echo FEHLT`.
  **Geprüft wird die Existenz, nie der Wert.**

  **Muss ein Wert wirklich verglichen werden**, geschieht das über eine
  Quersumme (`shasum`) oder die Länge — nie über die Zeichen selbst. Und wenn
  sich eine Frage nur durch Ansehen des Werts beantworten liesse, schaut der
  Nutzer selbst nach und antwortet mit **ja oder nein**, nicht mit der Ausgabe.

  > **Hintergrund: Der API-Schlüssel dieses Projekts wurde bereits zweimal
  > neu erzeugt, nachdem er versehentlich im Chat stand.** Der heutige ist der
  > dritte. Ein drittes Mal wäre vermeidbar gewesen.
- Mehrzeilige Eingaben (Heredoc, Python-Blöcke) **funktionieren über Termius
  nicht** — die Zeilenumbrüche gehen verloren. Stattdessen zeilenweise mit
  `echo … >>` aufbauen.
- ⚠️ **Vor jedem Merge: gegen die MERGE-BASIS vergleichen, nie `main..zweig`.**
  Fünfmal aufgetreten (TB-34, TB-36, TB-40, TB-41, TB-42) — die Zwei-Punkt-Form
  zeigt **alles Neuere auf `main` als Löschung** und lässt einen sauberen Zweig
  gefährlich aussehen.

  ```
  git diff --stat $(git merge-base main origin/<zweig>)..origin/<zweig>
  ```

  ⭐ **In TB-45 gemessen, warum nicht die Drei-Punkt-Form:** Sie löst dasselbe
  Problem, sieht dafür eine **unkommittierte** Änderung nicht mehr — sie
  vergleicht zwei Commits, der Arbeitsbaum kommt darin nicht vor. **Der
  Merge-Basis-Vergleich löst beides.**
- ⚠️ **Vor dem Merge wird der Diff der Sperrlisten-Dateien angesehen**, wenn die
  Statistik eine davon nennt — auch dann, wenn die Aufgabe die Änderung
  ausdrücklich freigegeben hatte. *Die Freigabe sagt, dass geändert werden
  durfte; sie sagt nicht, was geändert wurde.*

  ⚠️ **Die Sperrliste, Stand 18.09.2026** *(erweitert)*:

  | Datei | seit |
  |---|---|
  | `strategies/*/live_params.py` | von Anfang an |
  | `strategies/*/forward_test.py` | von Anfang an |
  | `strategies/*/equity_simulation.py` | von Anfang an, **hart** |
  | `strategies/*/multi_symbol_optimise.py` | 16.09. (E1) |
  | ⭐ **`shared/entscheidungskerze.py`** | **16.09., 04:42:24Z** — *seit dem Umstellungstag der Live-Pfad, gegen den Registertext 7 den Backtest vergleicht* |
  | ⭐ **`shared/paths.py`** | **17.09.** — *von 145 Modulen importiert und im Cron; der Resolver-Modus ist ein eigener kleiner Schritt mit Mac-Lauf* |

- ⚠️ **`git status --porcelain` wird NACH dem letzten Commit aufgenommen**
  *(ergänzt 18.09.2026)*. In **TB-46 und TB-48** stand die Statusausgabe im
  Beleg, war aber **vor** dem abschliessenden Commit entstanden — sie zeigte
  Dokumente als ungesichert, die in Wahrheit im Zweig lagen. Beide Male war der
  Zweig in Ordnung; **beide Male war der Beleg wertlos.**

  **Deshalb vor jedem Merge zusätzlich prüfen, ob der Zweig die aktuellen
  Fassungen trägt:**

  ```
  git diff --stat origin/<zweig> -- docs/ research/
  ```

- ⚠️ **Eine Abweichung, die auf den Betrieb zeigt, wird gegen den Betrieb
  geprüft — nicht von Hand plausibilisiert** *(ergänzt 18.09.2026)*. Im
  TB-46b-Mac-Lauf wich **eine** der neun Datenbanken ab; die Erklärung war der
  `15 0 * * *`-Cronjob von `turtle_soup_crypto`. **Richtig ist: Zeitstempel
  gegen den Crontab-Eintrag desselben Bots rechnen** (Ortszeit gegen UTC!) und
  den Inhaltsunterschied gegen die Logzeile desselben Laufs. *„Wird schon der
  Cron gewesen sein" ist keine Prüfung.*

- ⭐ **Fundstellen werden nur genannt, wenn sie vor einem liegen.** Sonst steht
  ausdrücklich „aus dem Gedächtnis" dabei. *Am 17.09. von beiden Seiten
  unabhängig gezogen — die Fehlerliste im Journal (Block AX) zählt zwölf Fälle,
  acht davon aus derselben Ursache.*
- ⚠️ **Und jede Zahl aus einem fremden Bericht wird an der ROHAUSGABE
  nachgerechnet, bevor sie weitergereicht wird** *(verschärft 18.09.2026)*. Am
  18.09. habe ich aus dem TB-47-Bericht *„die letzte Kerze ist bei allen 223
  Dateien sauber"* übernommen — **175 davon tragen `kein_zeuge`**, dort ist
  überhaupt nichts belegbar. *Der Bericht war nicht falsch; meine
  Zusammenfassung war es.* **Die Rohausgabe liegt im ZIP; sie anzusehen kostet
  eine Minute.**
- **Zeilen, die kein Befehl sind, werden als solche gekennzeichnet.** Ein
  öffentlicher SSH-Schlüssel, ein Auszug aus einer Datei, ein Beispieltext
  gehören ins Web-Formular oder in den Editor, nicht in die Eingabezeile.
  *Am 17.09. einmal passiert — folgenlos, aber vermeidbar.*

---

## 7b. Zugänge zu den Umsystemen

### GitHub vom Mac (Stand 17.09.2026)

**`origin` läuft über SSH**, nicht mehr über HTTPS — der osxkeychain-Token war
abgelaufen und hat jeden Push blockiert.

| | |
|---|---|
| Fernadresse | `git@github.com:Manisch2886/trading-bot.git` |
| Schlüssel | `~/.ssh/id_ed25519_signing` — bei GitHub als **Authentication Key** *und* als **Signing Key** hinterlegt |
| `~/.ssh/config` | `Host github.com` mit `IdentityFile` und `IdentitiesOnly yes` — ⚠️ **nötig, weil der Dateiname kein Standardname ist**; ohne den Eintrag probiert SSH ihn gar nicht |

⚠️ **Wird ein Schlüssel bei GitHub angelegt, verlangt die Seite danach das
Kontopasswort** (*Confirm access*). Wird das übersprungen, **wird nichts
gespeichert** — und die Übersicht zeigt weiter „no SSH keys". Genau daran ist
der erste Versuch gescheitert.

⚠️ **`gh` und Homebrew sind auf dem Mac NICHT installiert.** Folge: Merges
laufen lokal, die Cloud-Sitzungen können keinen PR anlegen, und die PR-Reihe auf
GitHub ist ab TB-42 unvollständig (**E5**).

### Die übrigen Zugänge, und wo sie liegen

| | |
|---|---|
| **Binance** | Schlüssel in der gitignorierten `.env`, gelesen über `shared/fetch_binance_data.py`. ⚠️ **Der dritte Schlüssel** — zwei Vorgänger mussten neu erzeugt werden |
| **Telegram** | Bot-Token in `config/`, gelesen von `notifications/`. Trägt alle Meldungen des Betriebs |
| **E-Mail** | `config/email_config.py`, Klartext, gitignoriert, von **17 Betriebsmodulen** gelesen (**T37.3**) |
| **IBKR** | `broker/zugang.py`, Testnet gegen Produktiv mit Verwechslungssperre (**T37.4**) |
| **Dashboard über Tailscale** | `DASHBOARD_HOST` steht **nur** in der `.env` — geht sie verloren, ist der einzige Fernzugriffsweg weg (**F6/O2**) |

⚠️ **Für alle gilt Abschnitt 7 ohne Ausnahme: Existenz prüfen, nie den Wert.**

---

## 7c. Was in jedem Testauftrag für den Mac steht

⚠️ **Zusammengetragen am 18.09.2026 — bisher stand jeder dieser Punkte einzeln
im Backlog, und jeder ist mindestens einmal vergessen worden.**

| | |
|---|---|
| **Schritt 0** | ⚠️ **Sicherung der neun `*.db` mit Quersummen.** *Sie sind gitignoriert, existieren nur auf dem MacBook, sind die einzige OOS-Evidenz des Projekts und **nicht neu berechenbar** (T37.2).* Am Ende byteweise Identität nachweisen |
| **Datenstand** | **vorher und nachher** messen, beides berichten — Soll: `d9449faf…` bei 223 Dateien |
| **Basislauf** | mit Zeitgrenze je Datei; **bekannt rote UND ungeprüfte** Tests als solche kennzeichnen, Abweichungen melden — ⚠️ **auch ein bekannt roter Test, der plötzlich grün ist** |
| **Interpreter** | ⭐ **immer `trading-env/bin/python3`**, nie `/usr/bin/python3` — dort fehlt `binance` |
| **Abbruchkriterium** | gilt nur für Fehlschläge, **die den Gegenstand der Aufgabe betreffen** (T44.11) |
| **`git status --porcelain`** | am Ende, **nach dem letzten Commit** |
| **ZIP** | verbindlich, benannt nach der Aufgabe, nach `~/Downloads` |
| **„In einfacher Sprache"** | am Ende des Ergebnisdokuments |

---

## 8. Laufende Aufträge

- **Prüfen, ob weitere profitable Strategien möglich sind** — laufend, aber
  ohne eine Strategie als profitabel zu bezeichnen, bevor sie gemessen ist.
  Kandidaten kommen mit Hypothese und Abbruchkriterium ins Backlog.
- **Wochenrückmeldung an Fable**, sonntags. Erinnerung liegt in der
  Erinnerungen-App des Nutzers. Hinein gehören **gemessene Ergebnisse** und
  **Widersprüche**, nicht Fortschrittsberichte.

---

## 9. Ton

- **Direkt und ehrlich.** Wenn eine Zahl nicht trägt, wird das gesagt — auch
  wenn sie aus einer eigenen früheren Empfehlung stammt.
- **Eigene Fehler werden benannt**, nicht stillschweigend korrigiert. Im
  Backlog bleiben sie mit Begründung stehen, damit niemand sie wiederholt.
- **Keine Gefälligkeit.** Der Nutzer hat mehrfach ausdrücklich die unbequeme
  Antwort verlangt — und sie war jedes Mal die nützlichere.

---

## 10. Die Sitzungsuebergabe

**Wenn eine Sitzung lang geworden ist oder ein Arbeitsabschnitt endet**, wird
sie an eine neue uebergeben. Der Ablauf ist festgelegt:

### Schritt 1 — Diese Datei zur Pruefung vorlegen

> **Vor jeder Uebergabe wird der Nutzer gefragt, ob die Arbeitsweise noch passt
> oder erweitert werden soll.**

Nicht als Formalie: Die Abschnitte 1 bis 9 sind alle nachtraeglich entstanden,
weil im Lauf der Arbeit etwas fehlte. Die Frage ist die Stelle, an der das
Gelernte einer Sitzung dauerhaft wird statt mit ihr zu verschwinden.

**Konkret zu fragen:**

- Gibt es etwas, das in dieser Sitzung wiederholt gesagt werden musste?
- Hat sich eine Regel als unpraktisch erwiesen?
- Ist eine neue Gewohnheit entstanden, die noch nirgends steht?

**Erweiterungen kommen in dieses Dokument**, mit Datum, und werden mit
uebergeben.

### Schritt 2 — Das Paket schnueren

| Datei | immer dabei |
|---|---|
| **`ARBEITSWEISE.md`** | ✅ **diese Datei, in der gepruefeten Fassung** |
| `START_HIER.md` | ✅ Einstieg, auf den aktuellen Stand gebracht |
| `BACKLOG.md` | ✅ die kanonische Quelle *(oder der Nachtrag dazu, siehe Abschnitt 2)* |
| `STRATEGIEN_uebersicht.md` | ✅ |
| `JOURNAL.md` | ✅ *(Hinweis mitgeben: nur bei Bedarf oeffnen)* |
| ⭐ **`PRUEFPRINZIPIEN.md`** | ✅ **neu seit 18.09.2026, siehe Abschnitt 12** |
| offene Aufgabendokumente | die, die noch nicht uebergeben sind |

**Als ZIP**, wie alles andere auch.

### Schritt 3 — Den ersten Prompt mitliefern

**Der Nutzer bekommt einen fertigen Eroeffnungstext zum Kopieren**, nicht nur
das Archiv. Er nennt: was das Projekt ist, was im Anhang liegt, in welcher
Reihenfolge zu lesen ist, wo es gerade steht, und was als Naechstes ansteht.

**Vorlage:**

```
Neue Sitzung zum Trading-Bot-Projekt.

Im Anhang liegt die vollstaendige Uebergabe. Bitte lies in dieser
Reihenfolge:

1. ARBEITSWEISE.md   - wie ich arbeiten moechte, das ist verbindlich
2. START_HIER.md     - das Projekt und der aktuelle Stand
3. BACKLOG.md        - die aktiven Punkte

JOURNAL.md ist das Archiv (rund 4 000 Zeilen) - bitte nur oeffnen, wenn
es um eine konkrete frueher Messung geht. Die Blockbuchstaben werden im
Backlog referenziert.

Stand: <hier der aktuelle Stand in zwei bis drei Zeilen>
Als Naechstes: <die naechste Aufgabe>

Sag mir kurz, was du verstanden hast, bevor wir anfangen.
```

> Der letzte Satz ist Absicht: Er zeigt sofort, ob die Uebergabe angekommen ist
> — und ob etwas fehlt.

---

## 11. Änderungsverbote nennen ihren Zweck

⚠️ **Neu am 18.09.2026, weil eine meiner eigenen Auflagen das Falsche bewirkt
hat.**

**Was passiert ist:** TB-48 durfte *„nichts unter `research/` ändern"*. Die
Sitzung hat sich daran gehalten — und deshalb den **Prüfer, der die neunzehn
Zahlen des Registernachtrags nachrechnet, nicht ins Repo gelegt.** Er existiert
nur in einem ZIP-Archiv. Geht das verloren, ist die Nachrechnung verloren.

> ⭐ **Die Sitzung hat sich korrekt verhalten. Meine Regel war zu breit.**

**Die Regel, die daraus folgt:**

| | |
|---|---|
| **Ein Verbot nennt, wovor es schützt** | *„`research/` nicht ändern, damit keine vorhandene Messung überschrieben wird"* — dann ist eine **neue** Datei erkennbar nicht gemeint |
| ⭐ **Prüfwerkzeuge, die eine Aufgabe erzeugt, gehören ins Repo** | ausdrücklich, mit Zielpfad. *Eine Prüfung, die es gibt, aber nicht dort, wo sie gebraucht wird, ist dieselbe Fehlerfamilie wie eine Wache, die nicht mehr misst* |
| **Beim Abnehmen gegenprüfen** | Liegt alles, was die Aufgabe erzeugt hat, dort, wo es gebraucht wird? Oder nur im Archiv? |

---

## 12. Prüfprinzipien

⚠️ **Neu am 18.09.2026. Die Sammlung selbst steht in `docs/PRUEFPRINZIPIEN.md`
und gehört ins Übergabepaket.**

**Warum als eigenes Dokument und nicht hier:** Dieses Dokument enthält
**stehende Anforderungen des Nutzers**. Die Prüfprinzipien sind etwas anderes —
sie sind **gemessene Lehren** aus fehlgeschlagenen Prüfungen, und jede einzelne
hat einen Fall hinter sich, der sie erzeugt hat. *Dieselbe Trennung wie bei
`UMGEBUNGEN.md`: eine Umgebungstatsache ändert sich, wenn sich ein Rechner
ändert, nicht wenn sich die Arbeitsweise ändert.*

**Und sie gehören in jedes Aufgabendokument verwiesen**, nicht abgeschrieben —
die Cloud-Sitzungen können `docs/PRUEFPRINZIPIEN.md` lesen.
