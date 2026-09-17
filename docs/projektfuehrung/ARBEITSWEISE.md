# Arbeitsweise — stehende Anforderungen des Nutzers

**Alles hier hat der Nutzer im Lauf der Zusammenarbeit ausdruecklich verlangt.
Es gilt dauerhaft, nicht nur fuer einzelne Aufgaben.**

> ⚠️ **Dieses Dokument wird bei JEDER Sitzungsuebergabe mitgegeben** — es ist
> Bestandteil des Uebergabepakets, nicht optional. Und **vor jeder Uebergabe
> wird der Nutzer gefragt, ob es noch passt oder ergaenzt werden soll**
> (Abschnitt 10).

---

## 1. Die vier Wege — und sie werden IMMER benannt

Bei **jedem** Dokument und **jeder** Aufgabe wird ausdrücklich gesagt, wohin es
geht. Nicht nur in der Datei, auch in der Begleitnachricht.

| Weg | Wofür | Erkennbar an |
|---|---|---|
| **Cloud-Claude-Code** | Alle Aufgaben mit `TB-<Nummer>`. Läuft auf Anthropics Servern gegen das GitHub-Repo, erzeugt Branches und Pull Requests | Sitzungstitel im Dateikopf |
| **Claude Code am Mac** *(vom Nutzer „Remote" genannt, weil er ihn über die Mobil-App anspricht)* | Die `TESTAUFTRAG_*.md` aus dem Repo. ⚠️ **Immer als fertiger Einzeiler mit Dateipfad** *(ergänzt 15.09.2026)* — nicht „`claude` starten, dann Satz einfügen" | Dateiname beginnt mit `TESTAUFTRAG_` |

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
| **Claude Fable 5.1** | Die methodischen Fragen. **Ein durchgehender Chat** — Rückfragen gehören dorthin, nicht in einen neuen | Dateien heissen `RUECKFRAGE_`, `ANFRAGE_`, `RUECKMELDUNG_` |
| **Diese Sitzung** | Planung, Aufgaben schreiben, Ergebnisse einordnen, Backlog führen | — |

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
  Statistik `live_params.py`, `forward_test.py` oder `equity_simulation.py`
  nennt — auch dann, wenn die Aufgabe die Änderung ausdrücklich freigegeben
  hatte. *Die Freigabe sagt, dass geändert werden durfte; sie sagt nicht, was
  geändert wurde.*
- ⭐ **Fundstellen werden nur genannt, wenn sie vor einem liegen.** Sonst steht
  ausdrücklich „aus dem Gedächtnis" dabei. *Am 17.09. von beiden Seiten
  unabhängig gezogen — die Fehlerliste im Journal (Block AX) zählt zwölf Fälle,
  acht davon aus derselben Ursache.*
- **Zeilen, die kein Befehl sind, werden als solche gekennzeichnet.** Ein
  öffentlicher SSH-Schlüssel, ein Auszug aus einer Datei, ein Beispieltext
  gehören ins Web-Formular oder in den Editor, nicht in die Eingabezeile.
  *Am 17.09. einmal passiert — folgenlos, aber vermeidbar.*

### Zugang zu GitHub vom Mac (Stand 17.09.2026)

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
| `BACKLOG.md` | ✅ die kanonische Quelle |
| `STRATEGIEN_uebersicht.md` | ✅ |
| `JOURNAL.md` | ✅ *(Hinweis mitgeben: nur bei Bedarf oeffnen)* |
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
