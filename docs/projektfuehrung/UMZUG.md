# Umzug in einen neuen Chat — das Verfahren

**Angelegt 19.09.2026 auf ausdrückliche Anweisung des Betreibers:** *„Organisiere
den Umzug in einen neuen Chat bis ins kleinste Detail und nehme die Schritte
eines solchen Umzugs für zukünftige Umzüge in die Arbeitsanweisung oder
Dokumentation mit auf. Es soll nichts verloren gehen."*

⚠️⚠️ **Dieses Dokument ersetzt Abschnitt 10 von `ARBEITSWEISE.md`** (dort Zeilen
674–743, Stand 19.09.2026). Der alte Abschnitt verlangte ein ZIP-Paket und
Anhänge an den neuen Chat. **Beides ist überholt:**

| | |
|---|---|
| ⚠️ **Das ZIP** | Anweisung des Betreibers, 19.09.2026: *„Ich lese die Zipp und berichte nie."* Übergabe über Archive ist damit ausgeschlossen |
| ⚠️ **Die Anhänge** | Sie sind unnötig. **Projektdokumente, Repo und Erinnerung tragen den Stand von selbst in jeden neuen Chat** — ein Anhang ist eine vierte Kopie, die mit den drei anderen auseinanderläuft |

---

## 1. ⭐⭐ Der Kernsatz: die Übergabe wird nicht beim Umzug geschrieben, sondern laufend gepflegt

**Das ist der Unterschied zwischen dem alten und dem neuen Verfahren, und alles
andere folgt daraus.**

> **Wer die Übergabe erst beim Umzug schreibt, hat ein Zeitfenster, in dem ein
> unerwarteter Abbruch Arbeit vernichtet. Wer sie laufend pflegt, hat keins.**

⇒ **`UEBERGABE_<datum>.md` wird an jedem sauberen Stand fortgeschrieben** — nicht
am Ende. Ein sauberer Stand ist: **keine Sitzung läuft, alles ist committet.**

⭐ **Folge, und sie ist der ganze Gewinn:** Eine überraschende Komprimierung des
Chats kostet dann **nichts**. Der neue Chat liest die Übergabe und ist auf dem
Stand. Der Umzug wird von einem Ereignis zu einer Formalie.

---

## 2. Die drei Träger — und was jeder NICHT trägt

**Ein Umzug verliert nur, was in genau einem Träger steht. Deshalb die
ausdrückliche Zuordnung:**

| Träger | trägt | ⚠️ trägt NICHT |
|---|---|---|
| ⭐ **Erinnerung** (`/projects/<id>/preferences.md`) | **Wie der Betreiber arbeiten will.** Wird beim Sitzungsstart von selbst gelesen, ohne dass er etwas tun muss | Fachstand, Zahlen, Befunde. **Keine Belege** — die Erinnerung ist keine Beweisführung |
| ⭐ **Projektdokumente** (claude.ai-Projekt „Trading Bots") | **Den Stand und die Führungsdokumente.** Sichtbar in **jedem** Chat des Projekts **und für Fable** | Nichts, was git prüfen muss — kein `numstat`, keine Versionsgeschichte |
| ⭐ **Das Repo** (`Manisch2886/trading-bot`) | **Die Belege.** Versioniert, mit Commit, prüfbar | Es wird von einem neuen Chat **nicht automatisch gelesen** — es braucht einen Verweis |

⚠️⚠️ **Die Regel, die daraus folgt, und sie ist die wichtigste dieses
Dokuments:**

> **Nichts, was den Umzug überleben muss, steht in nur einem Träger — und
> niemals nur im Chatverlauf.**

**Der Chatverlauf ist kein Träger.** Er wird komprimiert, und was nur dort stand,
ist dann eine Zusammenfassung von sich selbst.

⚠️ **Und `logs/auftraege/` ist auch keiner.** Der Ordner ist über
`.gitignore:27` (`logs/`) ausgeschlossen: eine Datei dort existiert auf **einem**
Rechner in **keiner** Version. ⭐ *Dieselbe Kategorie wie `~/Downloads`, und
dieselbe Regel gilt: ein Beleg dort ist kein Beleg.* Der Ordner ist ein
**Zwischenlager**, ausdrücklich nützlich, solange eine Mac-Sitzung läuft — aber
jede Datei dort hat eine offene Bringschuld ins Repo.

---

## 3. Wann umgezogen wird — und wann ausdrücklich nicht

### Die Auslöser, an denen ich den Umzug von selbst anspreche

⚠️⚠️ **Anweisung des Betreibers, 19.09.2026:** *„Zukünftig weise mich bitte auch
frühzeitig auf einen Umzug in einen neuen Chat hin, bevor der Chat komprimiert
wird."*

**Ich kann den verbleibenden Kontext nicht messen.** Deshalb hängen die Auslöser
an Zuständen, nicht an Zahlen — und das ist die bessere Lösung, weil ein Umzug an
einem sauberen Stand nichts kostet, während ein Umzug an einer Zahlengrenze
mitten in einer Sitzung landen kann.

| | Auslöser | ⭐ |
|---|---|---|
| **1** | **Eine Mac- oder Cloud-Sitzung ist fertig und ihr Ergebnis ist committet** | der beste Zeitpunkt überhaupt: nichts in der Luft |
| **2** | **Drei oder mehr grössere Dokumente sind im Chat entstanden** | dann hat der Chat seinen Zweck erfüllt |
| **3** | **Der Chat wurde schon einmal komprimiert** | dann beim **nächsten** sauberen Stand, nicht später |
| **4** | **Ein neuer mehrstündiger Arbeitsabschnitt beginnt** | ⚠️ **davor, nicht danach** — „frühzeitig" heisst vor dem Block |
| **5** | **Der Betreiber fragt danach** | dann gilt Abschnitt 4 |

⭐ **Der Hinweis wird ausgesprochen, nicht abgewartet** — nach derselben Regel
wie jede andere Aufgabe: *nie eine blosse Ankündigung, sondern ein Vorschlag mit
Zeitpunkt.*

### ⚠️ Wann NICHT umgezogen wird

| | |
|---|---|
| ⚠️⚠️ | **Während eine Mac- oder Cloud-Sitzung läuft.** Der neue Chat kennt den Zwischenstand nicht, und der alte kann ihn nicht mehr berichten |
| ⚠️⚠️ | **Solange Arbeit uncommittet ist.** Ein Umzug über einen unsauberen Arbeitsbaum verliert genau das, was noch nicht im Repo steht |
| ⚠️ | **Mitten in einer offenen Rückfrage** — an eine Sitzung, an Fable oder an den Betreiber. Erst die Antwort, dann der Umzug |
| ⚠️ | **Wenn ein Zeitanker oder ein Vergleichsfenster in derselben Stunde gesetzt werden soll.** Dann erst der Anker |

---

## 4. Der Ablauf, Schritt für Schritt

### Schritt 0 — Den Zustand prüfen, nicht annehmen

**Drei Messungen, und jede kann den Umzug verschieben:**

```
git status --short            → 0 Zeilen
git rev-parse --short HEAD    → und dieser Wert kommt in die Übergabe
ls -1t docs/belege/<laufende Aufgabe>/   → nichts Neues in den letzten Minuten
```

⚠️ **Zeitstempel sind UTC, die Ortszeit ist +02:00.** *Am 19.09.2026 habe ich aus
einem UTC-Zeitstempel geschlossen, eine Sitzung sei seit zwei Stunden tot — sie
arbeitete gerade.* **Immer `date -u` gegen `TZ=Europe/Berlin date` halten,
bevor aus einem Zeitstempel etwas gefolgert wird.**

### Schritt 1 — Alles Zwischengelagerte ins Repo

**Jede Datei aus `logs/auftraege/`, die zum Projekt gehört, wird abgelegt und
committet:**

| Art | Zielort |
|---|---|
| Nachträge zu Führungsdokumenten | `docs/projektfuehrung/nachtraege/` |
| Konzept- und Vorlagendokumente des Betreibers | `docs/vorlagen/` |
| Auftragsdokumente | `docs/auftraege/` |
| Belege und Messprotokolle | `docs/belege/<Aufgabe>/` |

⚠️ **Byteweise prüfen, nicht auf „geschrieben" vertrauen** — `cmp -s` je Datei,
und die Zahl der geprüften Dateien im Commit nennen. *Grund: ein Ablagewerkzeug
hat am 19.09. „written" gemeldet und die Datei nicht verändert.*

### Schritt 2 — `ARBEITSWEISE.md` vorlegen

⭐ **Das bleibt aus dem alten Abschnitt 10 unverändert, und es ist der wertvollste
Teil daran:**

> **Vor jedem Umzug wird der Betreiber gefragt, ob die Arbeitsweise noch passt
> oder ergänzt werden soll.**

**Drei Fragen, konkret:**

1. Gibt es etwas, das in diesem Chat **wiederholt** gesagt werden musste?
2. Hat sich eine Regel als unpraktisch erwiesen?
3. Ist eine Gewohnheit entstanden, die noch nirgends steht?

⚠️ **Und der Teil, der bisher fehlte:** Jede Regel, die in diesem Chat
**vereinbart** wurde, wird gegen `ARBEITSWEISE.md` und die Erinnerung **geprüft,
nicht erinnert.** *Am 19.09. waren neun neue Regeln im Chat vereinbart und keine
davon in `ARBEITSWEISE.md`.* ⇒ **Liste erstellen, abgleichen, Differenz in einen
Nachtrag.**

### Schritt 3 — Die Übergabe fortschreiben

`docs/projektfuehrung/UEBERGABE_<datum>.md`, **und sie enthält immer diese neun
Blöcke:**

| | Block | ⚠️ |
|---|---|---|
| **1** | **Stand in drei Zeilen** — was gerade fertig ist, was läuft, was als Nächstes kommt | |
| **2** | **`HEAD`, Zweig, und die Commit-Kette des Tages** | gemessen, nicht erinnert |
| **3** | **Die tragenden Zahlen** — Datenstand, Snapshot, Lock, Registerabschnitte | ⚠️ **jede mit ihrer Fundstelle** |
| **4** | **Offene Punkte vor dem nächsten Meilenstein**, in Reihenfolge | mit Begründung der Reihenfolge |
| **5** | **Wartezustände** — was auf wen wartet | Sitzung, Fable, Betreiber |
| **6** | **Freigaben und Sperrlisten-Stand** | ⚠️ **Freigaben verfallen nicht von selbst — sie müssen aufgeführt sein** |
| **7** | **Die Fehler dieses Chats und die daraus abgeleiteten Regeln** | ⭐ *das Wertvollste; ohne diesen Block wiederholt der neue Chat sie* |
| **8** | **Was zwischengelagert und noch nicht eingearbeitet ist** | mit Zielort |
| **9** | ⭐ **Verweis auf den Eröffnungstext in Abschnitt 6** — dort steht die einzige Fassung | ⚠️ **kein zweiter Text in der Übergabe.** *Bis TB-68 (20.09.2026) verlangte diese Zeile eine Kopie; die beiden Fassungen widersprachen sich vom ersten Commit an* |

### Schritt 4 — In die Projektablage schreiben

**Die Übergabe und dieses Dokument gehen zusätzlich in das claude.ai-Projekt**
(`projektfuehrung/UEBERGABE_<datum>.md`, `projektfuehrung/UMZUG.md`).

⭐ **Warum zusätzlich und nicht stattdessen:** Das Projekt ist der Träger, den ein
neuer Chat **von selbst** sieht. Das Repo ist der Träger, der **Beweiskraft**
hat. Beides ist nötig, und sie müssen gleich lauten.

### Schritt 5 — Die Erinnerung nachziehen

**Jede in diesem Chat vereinbarte Regel über die Arbeitsweise** kommt in
`/projects/<id>/preferences.md`. ⭐ **Sie ist der einzige Träger, der ohne
Zutun des Betreibers wirkt** — ein neuer Chat verhält sich richtig, bevor er
irgendetwas gelesen hat.

⚠️ **Fachstand gehört nicht hinein.** Zahlen, Hashes und Befunde stehen in der
Übergabe; die Erinnerung trägt nur, *wie* gearbeitet wird.

### Schritt 6 — Den Eröffnungstext ausgeben

⚠️ **Als Kopierblock in der Antwort** — kein Download, keine Datei, kein Anhang.
**Vorlage in Abschnitt 6 dieses Dokuments.**

### Schritt 7 — Den alten Chat nicht sofort schliessen

⚠️ **Der neue Chat bestätigt zuerst, was er verstanden hat.** Fehlt etwas, wird
es **aus dem alten Chat** nachgetragen — solange er noch offen ist. ⭐ *Erst
danach ist der Umzug abgeschlossen.*

---

## 5. Was am häufigsten verlorengeht — die Prüfliste

**Erfahrungswerte, keine Vermutungen: jeder Punkt ist mindestens einmal
eingetreten.**

| | ⚠️ Verlustkandidat | wo es hingehört |
|---|---|---|
| **1** | **Regeln, die im Chat vereinbart wurden** | `ARBEITSWEISE.md` **und** Erinnerung |
| **2** | **Freigaben für Sperrlisten-Dateien** — sie stehen im Auftrag, nicht im Dauerbestand | Übergabe, Block 6 |
| **3** | **Eigene Fehler und die Regeln daraus** | Übergabe, Block 7 — ⭐ *ohne sie werden sie wiederholt* |
| **4** | **Offene Rückfragen** an Sitzung, Fable oder Betreiber | Übergabe, Block 5 |
| **5** | **Zwischengelagerte Dateien** in `logs/auftraege/` | Schritt 1 |
| **6** | **Gemessene Nummernstände** (freier Block, freie K-Nummer, höchste Kettenzeile) | Übergabe, Block 3 — ⭐ *sonst werden wieder Nummern erfunden* |
| **7** | **Der Unterschied zwischen gemessen und erschlossen** in Aussagen des alten Chats | ⚠️ **jede Aussage in der Übergabe sagt, welches von beidem sie ist** |

---

## 6. Der Eröffnungstext — die einzige Fassung

⭐ **Dies ist die verbindliche Fassung des Eröffnungstextes; sie steht nur hier.**
`UEBERGABE_2026-09-19.md` Block 9 verweist hierher (TB-68, 20.09.2026 — davor
stand dort eine abweichende Kopie). ⚠️ **Keine Anhänge. Keine Dateien. Der neue
Chat holt sich alles selbst.**

```
Neue Sitzung zum Trading-Bot-Projekt. Das Projekt "Trading Bots" ist angehängt,
du kommst also an alle Führungsdokumente.

Lies in dieser Reihenfolge, über den Projects-Zugriff (in Klammern der Pfad im
Repo, falls du dort liest):

1. projektfuehrung/UEBERGABE_2026-09-25.md  — der Stand, das Wichtigste
                                              (docs/projektfuehrung/UEBERGABE_2026-09-25.md)
2. projektfuehrung/UMZUG.md                 — wann und wie umgezogen wird, inkl. Auslöser
                                              (docs/projektfuehrung/UMZUG.md)
3. projektfuehrung/ARBEITSWEISE.md          — wie ich arbeiten möchte, verbindlich
                                              (docs/projektfuehrung/ARBEITSWEISE.md)
4. PRUEFPRINZIPIEN.md                       — die gemessenen Lehren
                                              (docs/PRUEFPRINZIPIEN.md — NICHT unter projektfuehrung/)
5. projektfuehrung/BACKLOG.md               — die aktiven Punkte
                                              (docs/projektfuehrung/BACKLOG.md)

Bei Bedarf, nicht als Pflicht: docs/UEBERGABEPROTOKOLL.md — der Betrieb
(Cronjobs, Neustarts, Schlüsselbund); die Claude-Code-Sitzungen lesen es
ohnehin über CLAUDE.md.

Das Repo liegt auf dem MacBook unter ~/trading-bot und ist über die
Geräteanbindung lesbar. JOURNAL.md nur öffnen, wenn es um eine konkrete
frühere Messung geht.

Prüfe als Erstes, ob du über die Geräteanbindung auf ~/trading-bot lesen
kannst — nenne mir HEAD und die Zeilenzahl von docs/projektfuehrung/BACKLOG.md
als Beleg. Wenn das nicht geht, sag es ausdrücklich, denn dann müssen wir
Messungen wieder über mich laufen lassen.

Sag mir in wenigen Sätzen, was du verstanden hast — Stand, nächster Schritt,
und was gerade auf wen wartet. Dann fangen wir an.
```

> ⭐ **Der letzte Satz ist Absicht.** Er zeigt sofort, ob die Übergabe angekommen
> ist — und er nennt ausdrücklich die **Wartezustände**, weil das der Block ist,
> der am leichtesten durchfällt.

⚠️ **Was sich mit TB-68 (20.09.2026) geändert hat, gemessen:**

| | vorher | jetzt |
|---|---|---|
| `PRUEFPRINZIPIEN.md` | `projektfuehrung/PRUEFPRINZIPIEN.md` — **die Datei hat dort nie gelegen** (`git log --all`, 0 Commits); ein zweites Projekt ist am 20.09. genau daran gescheitert | `PRUEFPRINZIPIEN.md`, mit dem Repo-Pfad `docs/PRUEFPRINZIPIEN.md` daneben |
| `UMZUG.md` | fehlte hier, stand nur in der Kopie in der Übergabe | Nr. 2 — der Chat soll nach Abschnitt 3 **selbst** auf den Umzug hinweisen, dazu muss er die Auslöser kennen |
| Übergabe-Name | `UEBERGABE_<datum>.md` (Platzhalter) hier, `UEBERGABE_2026-09-19.md` (fest) in der Kopie | **der feste Name** — Betreiberentscheidung 20.09.2026 (TB-68, Nachweis 6): der Platzhalter wäre robuster gegen Umbenennung, aber ein eingefügter Platzhalter schickt den Chat auf eine Datei, die es nicht gibt. ⚠️ Beim Umbenennen der Übergabe (offener Punkt in ihrem Kopf: `UEBERGABE.md` ohne Datum) wird diese eine Zeile mitgezogen |
| `UEBERGABEPROTOKOLL.md` | nirgends genannt | **eine Zeile „bei Bedarf“ mit Repo-Pfad**, nicht in der Pflichtliste — Betreiberentscheidung 20.09.2026 (TB-68, Nachweis 6). Gemessen: jede Claude-Code-Sitzung liest es über `CLAUDE.md` Z. 3; der steuernde Chat hat es in keinem seiner Führungsdokumente und in 32 von 40 Ergebnisdokumenten nicht gebraucht; 141 KB Pflicht mehr widersprächen `K3p` |
| Prüfung der Geräteanbindung | als *„Ergänzung zur Vorlage"* am Ende von Abschnitt 8, **nicht im Text** | im Text, vor dem letzten Absatz |
| Repo-Pfade | fehlten | je Dokument in Klammern — ein Chat, der im Repo statt in der Projektablage liest, findet jede Datei |

---

## 7. Der Ersatztext für `ARBEITSWEISE.md`, Abschnitt 10 — eingearbeitet

✅ **Eingearbeitet am 19.09.2026; der gültige Text steht nur noch in
`ARBEITSWEISE.md` Abschnitt 10.** Die Kopie, die hier bis zum 20.09.2026 stand
(23 Zeilen, zeichengleich mit der eingearbeiteten Fassung, per `diff` geprüft),
ist mit TB-62 entfernt — `DOKUMENTATIONSSTANDARD.md` Regel 9: eine Kopie, deren
Inhalt anderswo im Repo steht, läuft nur auseinander. ⚠️ **Genau das wäre hier
passiert:** Abschnitt 10 wurde am 20.09.2026 umgestellt (ZIP ist überall
abgeschafft, nicht nur beim Umzug — Betreiberentscheidung, `ARBEITSWEISE.md`
Abschnitt 2), und die Kopie hätte weiterhin die Umzugs-Ausnahme behauptet.

⭐ **Warum ein Verweis und nicht der ganze Text:** dieselbe Begründung wie bei
Abschnitt 12 und `PRUEFPRINZIPIEN.md`. `ARBEITSWEISE.md` enthält **stehende
Anforderungen**; ein Verfahren mit Schritten, Prüflisten und Vorlagen ist etwas
anderes und wächst anders.

---

## In einfacher Sprache

**Worum es geht:** Wenn der Chat lang geworden ist, wird er teuer und wird
irgendwann automatisch zusammengefasst. Dann geht Genauigkeit verloren. Die
Lösung ist ein neuer Chat — aber nur, wenn vorher nichts verlorengeht.

⭐ **Der eine Gedanke, auf den alles hinausläuft:** Früher wurde die Übergabe
**beim** Umzug geschrieben. Das ist riskant, weil ein unerwarteter Abbruch genau
in dieses Fenster fallen kann. **Ab jetzt wird die Übergabe laufend
mitgeschrieben** — immer dann, wenn gerade nichts läuft und alles gesichert ist.
Dann ist der Umzug keine Aktion mehr, sondern nur ein Wechsel des Fensters.

**Warum keine Anhänge mehr:** Der neue Chat hängt am selben Projekt und sieht
alle Führungsdokumente von selbst. Zusätzlich liest er das Repo auf dem MacBook.
Und die Regeln, wie du arbeiten möchtest, stehen in der Erinnerung — die wirkt,
noch bevor er irgendetwas gelesen hat. **Drei Wege, die sich gegenseitig
absichern.** Ein Anhang wäre ein vierter, der mit den anderen auseinanderläuft.

**Wann ich dich künftig von selbst darauf hinweise:** wenn eine Sitzung fertig
und ihr Ergebnis gesichert ist · wenn drei größere Dokumente entstanden sind ·
wenn der Chat schon einmal zusammengefasst wurde · und **vor** einem neuen
längeren Arbeitsblock, nicht danach.

**Wann nicht:** solange eine Sitzung läuft, solange etwas nicht gesichert ist,
und solange eine Rückfrage offen ist. In diesen drei Fällen würde der Umzug genau
das kosten, was er verhindern soll.

---

## 8. ⚠️⚠️ Die Geräteanbindung muss den Umzug überleben — sie tut es nicht von selbst

**Nachgetragen 19.09.2026, 21:50, nach der Frage des Betreibers, ob im neuen
Chat unmittelbar so weitergearbeitet wird.**

**Der grösste Ertrag des 19.09. war nicht ein Dokument, sondern eine
Arbeitsteilung:** Wo eine Sitzung über die Geräteanbindung auf `~/trading-bot`
lesen kann, **messe ich selbst** — `HEAD`, `numstat`, Dateigrössen,
`cmp`-Vergleiche, Backlog-Nummernstände, der Fortschritt einer laufenden
Mac-Sitzung, die Datenauflösung. **Der Betreiber kopiert keine Terminalausgaben
mehr.** *(Vollständig in `UEBERGABE_2026-09-19.md`, Nachtrag 2.)*

⚠️⚠️ **Und genau das überlebt einen Umzug NICHT automatisch.** Die Anbindung
hängt daran, dass die Unterhaltung mit dem Rechner verbunden ist — nicht am
Projekt, nicht an der Erinnerung, nicht am Repo. **Ein neuer Chat ohne Anbindung
fällt auf den alten, aufwendigen Weg zurück, und zwar unbemerkt.**

### Die Regel für jeden Umzug

| | |
|---|---|
| ⭐⭐ **1** | **Der neue Chat wird aus der Claude-Desktop-App auf dem MacBook geöffnet, mit dem Rechner ausgewählt** — nicht aus dem Browser, nicht vom Mobiltelefon. *Bietet die App für eine bestehende Unterhaltung „Link to this computer" an, geht auch das.* |
| ⭐⭐ **2** | **Der erste Auftrag im neuen Chat ist eine Prüfung der Anbindung**, keine Behauptung. Eine gelesene Datei oder ein gelesener `HEAD` ist der Beleg; „die Tools sind da" ist keiner |
| ⚠️ **3** | **Fehlt die Anbindung, wird das ausdrücklich gesagt** — mit dem Satz, dass Messungen dann wieder über den Betreiber laufen. **Nicht stillschweigend zurückfallen** |

⭐ **Deshalb enthält der Eröffnungstext in Abschnitt 6 ab jetzt eine Zeile, die
diese Prüfung verlangt.** Sie kostet eine Antwort und sichert den Ertrag eines
ganzen Arbeitstages.

### Ergänzung zur Vorlage in Abschnitt 6 — eingearbeitet

✅ **Seit TB-68 (20.09.2026) steht der Vierzeiler zur Prüfung der
Geräteanbindung im Eröffnungstext selbst** (Abschnitt 6, vor dem letzten Absatz;
per `diff` wortgleich mit dem Text, der hier bis dahin als Nachsatz stand). Ein
Text mit angehängtem Flicken ist dieselbe Fehlerklasse wie zwei Fassungen —
`DOKUMENTATIONSSTANDARD.md` Regel 9.
