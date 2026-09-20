# ERGEBNIS TB-68 — Der Eröffnungstext: eine Fassung, ein Ort (Mac-Sitzung, 20.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-68_eroeffnungstext.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `a15746f` (= `origin/main` beim Start), **reine
Dokumentation** — kein Interpreter, keine Kursdaten, nichts ausserhalb `docs/`.
Dieses Dokument wächst mit jedem Schritt und wird je Schritt committet; die
Commit-Liste steht am Ende.

*In einfacher Sprache, zu Beginn:* Der Text, den ein neuer Chat als Erstes
liest, steht zweimal im Repo und sagt zweimal etwas Verschiedenes. Diese Sitzung
misst, welche Fassung wo herkommt, lässt eine stehen, berichtigt darin den
Pfad, der ins Leere zeigt, ersetzt die zweite durch einen Verweis — und sucht,
ob es noch eine dritte gibt.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart, wörtlich:

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/auftraege/MAC_TB-64_nachtragswaechter.md
 M docs/projektfuehrung/ARBEITSWEISE.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20d_tagesreihe.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-09-20c_kapitalpfad.md
```

Fünf Dateien, keine davon von dieser Sitzung. **Schritt 0:** alle fünf in
`b1d8429` committet und gepusht (Auftragszeiger, TB-64 Schritt 5b,
`ARBEITSWEISE.md` 6d, zwei Fable-Dateien). Danach `git status --short` = 0 Zeilen
(gemessen).

⚠️ **Während der Sitzung hat der Betreiber weiter ins Repo geschrieben** —
`AKTUELLER_AUFTRAG.md` (TB-71 neu gefasst, TB-72 ergänzt) und
`FABLE_ANTWORT_2026-09-20d_mtm_messung.md`. Beides als eigene Zwischencommits
gesichert (`30d44f7`, `6e0378f`), damit kein Diff dieser Sitzung fremde Zeilen
trägt.

---

## Nachweis 2 — Schritt 1: die beiden Fassungen, Zeile für Zeile

**Herkunft, gemessen mit `git log -L` über die Zeilenbereiche:** beide Fassungen
stammen aus **demselben Commit `2723c16`** (19.09.2026, 21:40) und wurden
**seither nicht geändert**. ⇒ Es gab keinen Zeitpunkt, an dem sie gleich
lauteten — **sie sind als Widerspruch geboren worden, nicht auseinandergelaufen.**

| Zeile | `UMZUG.md` Abschnitt 6 (Z. 224–241) | `UEBERGABE_2026-09-19.md` Block 9 (Z. 282–301) | gleich? |
|---:|---|---|---|
| 1–2 | `Neue Sitzung zum Trading-Bot-Projekt. Das Projekt "Trading Bots" ist angehängt, du kommst also an alle Führungsdokumente.` | identisch | ✅ |
| 3 | `Lies in dieser Reihenfolge, über den Projects-Zugriff:` | identisch | ✅ |
| Nr. 1 | `projektfuehrung/UEBERGABE_<datum>.md — der Stand, das Wichtigste` | `projektfuehrung/UEBERGABE_2026-09-19.md — der Stand, das Wichtigste` | ⛔ Platzhalter gegen festen Namen |
| Nr. 2 | *(fehlt)* | `projektfuehrung/UMZUG.md — wie Umzüge laufen, inkl. Auslöser` | ⛔ nur rechts |
| Nr. 2 / 3 | `projektfuehrung/ARBEITSWEISE.md — wie ich arbeiten möchte, verbindlich` | dito **plus** Folgezeile `(Abschnitt 10 ist überholt, siehe UMZUG.md)` | ⛔ Zusatzzeile rechts — und die ist **seit TB-62 selbst überholt**: Abschnitt 10 ist am 20.09. durch den Verweis ersetzt worden (`ARBEITSWEISE.md` Z. 792 ff., gemessen) |
| Nr. 3 / 4 | `projektfuehrung/PRUEFPRINZIPIEN.md — die gemessenen Lehren` | identisch | ✅ gleich — **und in beiden falsch** (Nachweis 3) |
| Nr. 4 / 5 | `projektfuehrung/BACKLOG.md — die aktiven Punkte` | identisch | ✅ |
| Absatz | `Das Repo liegt auf dem MacBook unter ~/trading-bot und ist über die Geräteanbindung lesbar. JOURNAL.md nur öffnen, wenn es um eine konkrete frühere Messung geht.` | identisch | ✅ |
| Schluss | `Sag mir in wenigen Sätzen, was du verstanden hast — Stand, nächster Schritt, und was gerade auf wen wartet. Dann fangen wir an.` | identisch | ✅ |
| Zahl der Dokumente | **4** | **5** | ⛔ |

**Was in beiden fehlt, gemessen:** `UMZUG.md` Abschnitt 8 (Commit `d46fdde`,
19.09. 21:49) sagt in Z. 321: *„Deshalb enthält der Eröffnungstext in
Abschnitt 6 ab jetzt eine Zeile, die diese Prüfung [der Geräteanbindung]
verlangt."* **Keine der beiden Fassungen enthält sie.** Der Vierzeiler steht
stattdessen als *„Ergänzung zur Vorlage"* am Dateiende (Z. 325–334) — eine
Vorlage mit angehängtem Flicken, dieselbe Fehlerklasse wie die zwei Fassungen.

### ⭐ Welche Fassung hat der Betreiber zuletzt benutzt — und was sagt das Verfahren?

**Nicht messbar aus dem Repo:** was am 19.09. in den neuen Chat eingefügt
wurde, steht nur im Chatverlauf, und der ist kein Träger (`UMZUG.md`
Abschnitt 2). **Messbar ist, was das Verfahren vorschreibt** (`UMZUG.md`
Abschnitt 4, gemessen):

| Stelle | Wortlaut | Bedeutung |
|---|---|---|
| Schritt 3, Zeile 9 | *„Der Eröffnungstext für den neuen Chat, fertig zum Kopieren"* — als **einer der neun Pflichtblöcke jeder Übergabe** | die Übergabe **muss** eine Kopie tragen |
| Schritt 6 | *„Als Kopierblock in der Antwort … Vorlage in Abschnitt 6 dieses Dokuments."* | Abschnitt 6 ist die **Vorlage** |

⇒ **Das Verfahren selbst verlangt Vorlage plus Instanz** — es hat die Doppelung
nicht zugelassen, sondern **angeordnet**. Deshalb genügt es nicht, Block 9 zu
kürzen: **Schritt 3, Zeile 9 muss mitgeändert werden**, sonst schreibt die
nächste Fortschreibung der Übergabe die Kopie pflichtgemäss wieder hinein.
*(Das steht so nicht im Auftrag; ohne diese Änderung wäre die Reparatur nach
einer Übergabe hinfällig.)*

**Zuordnung:** Das Messergebnis **bestätigt** die Zuordnung des Auftrags —
Abschnitt 6 ist im Verfahren als Vorlage benannt, Block 9 als Abschrift. Beim
**Inhalt** hat aber die Abschrift an zwei Stellen recht: `UMZUG.md` gehört in
die Leseliste (der Chat soll nach Abschnitt 3 selbst auf den Umzug hinweisen —
das kann er nur, wenn er die Auslöser kennt), und der feste Dateiname ist der,
der existiert (Nachweis 3). **Die bleibende Fassung übernimmt beides.**

---

## Nachweis 3 — Schritt 1: jeder genannte Pfad einzeln mit `test -f`

Die Texte nennen Namen der **Projektablage** (`projektfuehrung/…`, „über den
Projects-Zugriff"). Die Projektablage ist vom Mac aus nicht messbar; gemessen
ist der **Repo-Pfad**, den die Namen spiegeln (`docs/` + Name):

| Name im Text | Repo-Pfad geprüft | `test -f` |
|---|---|---|
| `projektfuehrung/UEBERGABE_2026-09-19.md` | `docs/projektfuehrung/UEBERGABE_2026-09-19.md` | **JA** |
| `projektfuehrung/UEBERGABE_<datum>.md` | *(Platzhalter — kein prüfbarer Pfad; `ls docs/projektfuehrung/UEBERGABE_*` liefert genau eine Datei, die oben)* | — |
| `projektfuehrung/UMZUG.md` | `docs/projektfuehrung/UMZUG.md` | **JA** |
| `projektfuehrung/ARBEITSWEISE.md` | `docs/projektfuehrung/ARBEITSWEISE.md` | **JA** |
| `projektfuehrung/PRUEFPRINZIPIEN.md` | `docs/projektfuehrung/PRUEFPRINZIPIEN.md` | ⛔ **NEIN** |
| *(tatsächlicher Ort)* | `docs/PRUEFPRINZIPIEN.md` | **JA** |
| `projektfuehrung/BACKLOG.md` | `docs/projektfuehrung/BACKLOG.md` | **JA** |
| `JOURNAL.md` (im Absatz darunter) | `docs/projektfuehrung/JOURNAL.md` | **JA** |
| *(im Auftrag genannt, in keinem Text)* | `docs/UEBERGABEPROTOKOLL.md` | **JA** |
| *(Gegenprobe)* | `docs/projektfuehrung/UEBERGABEPROTOKOLL.md` | **NEIN** |

**Bestätigt die Aussage des Auftrags, gemessen:** `git log --all
--diff-filter=A -- docs/projektfuehrung/PRUEFPRINZIPIEN.md` → **0 Commits**. Die
Datei hat nie unter `projektfuehrung/` gelegen; ihr erster Commit ist `e456756`
(18.09.2026) unter `docs/`.

⚠️ **Einschränkung, ehrlich:** Ob die Projektablage die Datei unter
`PRUEFPRINZIPIEN.md` oder unter `projektfuehrung/PRUEFPRINZIPIEN.md` führt,
kann diese Sitzung nicht prüfen. Der berichtigte Text nennt deshalb **beides**:
den Namen ohne Ordner **und** den Repo-Pfad in Klammern — dann findet ihn ein
Chat mit Geräteanbindung auch dann, wenn die Ablage anders heisst.

---

## Schritt 2 und 3 — eine Fassung, ein Ort, berichtigte Pfade

**Bleibende Fassung: `UMZUG.md` Abschnitt 6** — Zuordnung des Auftrags, durch
Nachweis 2 bestätigt. Was dort jetzt steht und warum:

| Änderung | Begründung |
|---|---|
| Abschnitt 6 heisst *„die einzige Fassung"* und sagt es im ersten Satz | Auflage des Auftrags: *ein Satz genügt* |
| `projektfuehrung/PRUEFPRINZIPIEN.md` ⇒ `PRUEFPRINZIPIEN.md`, daneben `(docs/PRUEFPRINZIPIEN.md — NICHT unter projektfuehrung/)` | Nachweis 3 |
| **jedes** Dokument trägt in Klammern seinen Repo-Pfad | die Projektablage ist vom Mac nicht messbar (Nachweis 3); mit dem Repo-Pfad findet ein Chat mit Geräteanbindung jede Datei, wie auch immer die Ablage sie nennt |
| `UMZUG.md` als Nr. 2 aufgenommen (**fünf** Dokumente) | der Chat soll nach `UMZUG.md` Abschnitt 3 **selbst** auf den Umzug hinweisen (Anweisung des Betreibers, 19.09.); ohne die Auslöser gelesen zu haben, kann er das nicht. ⚠️ **Widerspricht der Zahl „vier" im Auftrag**, aber nicht seiner Zuordnung — der Auftrag hat den Ort festgelegt, nicht den Inhalt |
| Zusatzzeile *„(Abschnitt 10 ist überholt, siehe UMZUG.md)"* **nicht** übernommen | seit TB-62 ist Abschnitt 10 selbst der Verweis (`ARBEITSWEISE.md` Z. 792 ff.); der Hinweis wäre ein Hinweis auf einen erledigten Zustand |
| Vierzeiler zur Geräteanbindung **in den Text**, vor den letzten Absatz | genau dort, wo Abschnitt 8 ihn haben wollte (Z. 327: *„Vor den letzten Satz des Eröffnungstextes gehört"*); per `diff` wortgleich mit dem alten Nachsatz (gemessen) |
| Fester Name `UEBERGABE_2026-09-19.md` statt `<datum>` | **vorläufig**, als Empfehlung gekennzeichnet — Nachweis 6 |
| `UMZUG.md` Schritt 3, Zeile 9: *„Verweis auf den Eröffnungstext in Abschnitt 6 … kein zweiter Text"* | ohne diese Änderung ordnet das Verfahren die nächste Kopie selbst wieder an (Nachweis 2) |
| Abschnitt 8, *„Ergänzung zur Vorlage"* ⇒ Vermerk *„eingearbeitet"* | Regel 9: das Abgelöste wird entfernt, nicht danebengestellt |
| `UEBERGABE_2026-09-19.md` Block 9 ⇒ Verweis mit Begründung | Regel 9; die Übergabe ist keine der vier Ausnahmen |
| ⚠️ `MAC_TB-63_epics_auslagern.md`, Nachweis 5: Vermerk *„seither FÜNF"* | der offene TB-63-Auftrag nennt die Menge des Eröffnungstextes mit **„VIER Dokumente"** und misst daran Bytes. Er sagt zwar selbst *„lies die Menge dort nach"*, aber eine bekannt falsche Zahl in einem Auftrag, der genau an falschen Zahlen krankte, bleibt nicht unmarkiert stehen. **Eine Zeile, in sich gekennzeichnet; sonst nichts an TB-63 geändert** |

**Was in beiden Fassungen gleich war, steht unverändert in der bleibenden:**
Anrede, Reihenfolge-Satz, Repo-Absatz mit dem `JOURNAL.md`-Hinweis, Schlusssatz.

---

## Nachweis 5 — `git diff --numstat` je Datei (Schritt 2/3), jede entfernte Zeile zugeordnet

```
39	17	docs/projektfuehrung/UMZUG.md
9	20	docs/projektfuehrung/UEBERGABE_2026-09-19.md
1	1	docs/auftraege/MAC_TB-63_epics_auslagern.md
```

**`UMZUG.md`, 17 entfernte Zeilen:**

| entfernt | ersetzt durch |
|---|---|
| Schritt 3, Zeile 9 (*„fertig zum Kopieren"*) | dieselbe Zeile als Verweis-Anordnung |
| `## 6. Der Eröffnungstext — Vorlage` | `## 6. Der Eröffnungstext — die einzige Fassung` |
| `⚠️ **Keine Anhänge. Keine Dateien. …**` | derselbe Satz, jetzt im Absatz nach dem Verbindlichkeitssatz |
| `Lies in dieser Reihenfolge, über den Projects-Zugriff:` | dieselbe Zeile mit dem Klammerzusatz zu den Repo-Pfaden |
| 4 Zeilen Leseliste (`UEBERGABE_<datum>`, `ARBEITSWEISE`, `PRUEFPRINZIPIEN`, `BACKLOG`) | 10 Zeilen Leseliste (fünf Dokumente, je mit Repo-Pfad) |
| `### Ergänzung zur Vorlage in Abschnitt 6` | `### … — eingearbeitet` |
| `**Vor den letzten Satz des Eröffnungstextes gehört:**` + Leerzeile | der Vermerk *„eingearbeitet"* |
| 6 Zeilen Kopierblock (Zaun, Vierzeiler, Zaun) | wortgleich im Eröffnungstext, Abschnitt 6 |

**`UEBERGABE_2026-09-19.md`, 20 entfernte Zeilen:** der gesamte Kopierblock von
Block 9 (2 Zaunzeilen, 15 Textzeilen, 3 Leerzeilen) ⇒ **ersetzt durch den
Verweis auf `UMZUG.md` Abschnitt 6**, der jede Abweichung der entfernten Kopie
benennt. Die inhaltlich gleichen Zeilen stehen dort unverändert; die
abweichenden (fester Name, `UMZUG.md` als Eintrag) sind in die bleibende Fassung
**übernommen**, die überholte Zusatzzeile zu Abschnitt 10 ist **ersatzlos** —
mit Begründung im Verweis. ⚠️ **Die Kürzung ist gewollt** (Auftrag Nachweis 5:
Spalte zwei ist nicht null).

**`MAC_TB-63_epics_auslagern.md`, 1 entfernte Zeile:** dieselbe Zeile mit
angehängtem Vermerk; kein Zeichen davor geändert.

---

## Nachweis 6 — was dem Betreiber vorgelegt wird, statt es zu entscheiden

### (a) Gehört `docs/UEBERGABEPROTOKOLL.md` in den Lesepfad des Eröffnungstextes?

**Gemessen am 20.09.2026:**

| Messung | Ergebnis |
|---|---|
| Grösse | **986 Zeilen, 141 234 Bytes** (`wc`) — der Lesepfad ist laut `K3p` schon 462 594 Bytes |
| Wer es heute schon lesen **muss** | **jede Claude-Code-Sitzung**, über `CLAUDE.md` Z. 3 (*„Vor jeder Arbeit an diesem Repo zuerst lesen"*) — der Eröffnungstext richtet sich dagegen an den **steuernden Chat**, der keine Bots betreibt |
| Auftragsdokumente (`docs/auftraege/*.md`, 14 Dateien) | in **2** genannt — TB-62 (einmal, in einer Liste zu prüfender Dokumente) und TB-68 selbst; **12 ohne Treffer** |
| Ergebnisdokumente (`docs/ERGEBNIS_TB-*.md`, 40 Dateien) | in **8** genannt, **32 ohne Treffer**; sechs davon je einmal, TB-62 dreimal (Prüfung von ZIP-Stellen), TB-67 zweimal (Liste der elf Führungsdokumente) — **kein Fall, in dem eine Sitzung einen Inhalt daraus gebraucht hätte** |
| Führungsdokumente des Chats | `UMZUG.md` **0**, `UEBERGABE_2026-09-19.md` **0**, `DOKUMENTATIONSSTANDARD.md` **0**, `PRUEFPRINZIPIEN.md` **0**, `ARBEITSWEISE.md` **1** (Abschnitt 18: `P.5` dorthin zurückgeholt), `BACKLOG.md` **3** (T44.7, T38.11, K4d — Erwähnungen, keine Verweise zum Lesen), `START_HIER.md` **1** (*„Daneben, bei Bedarf"*) |
| `JOURNAL.md` | **3** Treffer (`grep -ic bergabeprotokoll`), alle in älteren Blöcken |
| Commits an der Datei seit 15.09. | **5** (TB-37, TB-38, dreimal am 20.09. — TB-60-Nachlese, zurückgeholte Regeln, TB-61-Nachtrag) — sie wird **gepflegt**, aber von Mac-Sitzungen, nicht vom Chat |

⭐ **Empfehlung (Empfehlung, nicht Entscheidung):** **nicht in die Pflichtliste**,
sondern **eine Zeile „bei Bedarf"** im Eröffnungstext, mit Repo-Pfad und
Stichwort (*Betrieb: Cronjobs, Neustarts, Schlüsselbund*) — wie `START_HIER.md`
es hält. **Begründung:** Die Claude-Code-Sitzungen bekommen es ohnehin über
`CLAUDE.md`; der Chat hat es in keinem der 40 Ergebnisdokumente und in keinem
seiner eigenen Führungsdokumente als Lesestoff gebraucht; 141 KB Pflichtlektüre
mehr widersprechen `K3p`. **Was dagegen spricht:** es trägt Wissen, das der Chat
sonst nirgends hat (Schlüsselbund, launchd, Cron-Zeiten) — eine Zeile „bei
Bedarf" mit richtigem Pfad deckt das.

**Die drei Wege, zum Anklicken:** (1) eine Zeile „bei Bedarf" mit Pfad
(empfohlen) · (2) als Nr. 6 in die Pflichtliste · (3) gar nicht nennen.
**Bis zur Entscheidung steht es nicht im Text** (Auflage ⛔ *nicht selbst
entscheiden*).

### (b) `UEBERGABE_<datum>.md` (Platzhalter) oder `UEBERGABE_2026-09-19.md` (fest)?

| Form | dafür | dagegen |
|---|---|---|
| **fest** (`UEBERGABE_2026-09-19.md`) | ist der Name der Datei, die existiert (Nachweis 3); ein Chat fügt ihn wörtlich ein und findet die Datei | muss bei einer Umbenennung mitgezogen werden (eine Zeile) |
| **Platzhalter** (`UEBERGABE_<datum>.md`) | überlebt jede Umbenennung | steht in einem Text, der *„fertig zum Kopieren"* ist — ein eingefügter Platzhalter schickt den Chat auf eine Datei, die es nicht gibt; und die Übergabe wird laut `UMZUG.md` Abschnitt 1 **fortgeschrieben, nicht neu angelegt**, das Datum wechselt also gar nicht |

⭐ **Empfehlung: fest** — und den offenen Punkt aus dem Kopf der Übergabe
(Umbenennung nach `UEBERGABE.md` ohne Datum, sechs Verweise) bei Gelegenheit
umsetzen; danach ist der feste Name auch stabil. **Vorläufig steht im Text der
feste Name** (er stand schon in einer der beiden Fassungen und ist der einzige,
der existiert); die Tabelle in `UMZUG.md` Abschnitt 6 kennzeichnet ihn als
Empfehlung.

---

## Nachweis 4 — Schritt 4: die dritte Fassung gesucht, Trefferzahl je Muster

`grep -rlF` / `grep -rnF`, im ganzen `docs/`-Baum und in `logs/auftraege/`,
**vor** und **nach** der Änderung aus Schritt 2/3 (jeweils Dateien / Zeilen):

| Muster | `docs/` vorher | `docs/` nachher | `logs/auftraege/` |
|---|---|---|---|
| `Lies in dieser Reihenfolge` | 3 / 3 (`UMZUG.md`, `UEBERGABE_2026-09-19.md`, `MAC_TB-68` im Suchauftrag) | 3 / 4 (`UMZUG.md`, `MAC_TB-68`, **dieses Ergebnisdokument** zweimal — Zitate in Nachweis 2 und 4) | 2 / 2 |
| `Neue Sitzung zum Trading-Bot-Projekt` | 2 / 2 (`UMZUG.md`, `UEBERGABE_2026-09-19.md`) | 2 / 2 (`UMZUG.md`, dieses Dokument) | 2 / 2 |
| `Das Projekt "Trading Bots" ist angehängt` | 3 / 3 (`UMZUG.md`, `UEBERGABE_2026-09-19.md`, `MAC_TB-68`) | 3 / 3 (`UMZUG.md`, `MAC_TB-68`, dieses Dokument) | 2 / 2 |

⭐ **Keine dritte Fassung im `docs/`-Baum** — jeder Treffer ausserhalb
`UMZUG.md` ist ein Zitat im Auftrag oder in diesem Ergebnisdokument, kein Text
zum Einfügen. **Nach der Änderung steht der Eröffnungstext im Repo genau einmal.**

**`logs/auftraege/`, 2 Treffer je Muster:** `logs/auftraege/_erledigt/UMZUG.md`
und `…/_erledigt/UEBERGABE_2026-09-19.md` — die Zwischenlager-Kopien vom 19.09.
(21:47 bzw. 21:45), deren Bringschuld mit `2723c16` erfüllt ist. Ihr
Eröffnungstext-Block ist **zeichengleich mit der jeweiligen alten Repo-Fassung**
(`diff` über die Zeilenbereiche: leer); die Dateien im Ganzen weichen ab
(`cmp`: `UMZUG.md` ab Z. 249, die Übergabe ab Z. 1 — beide Repo-Fassungen sind
seither fortgeschrieben). ⚠️ **Nicht angefasst:** der Ordner ist gitignoriert
und kein Träger (`UMZUG.md` Abschnitt 2); er liegt ausserhalb `docs/`
(Nachweis 7); Löschen fragt vorher (`ARBEITSWEISE.md` Abschnitt 6). *Nach
`DOKUMENTATIONSSTANDARD.md` Regel 9 dürften Zwischenlager-Dateien mit erfüllter
Bringschuld weg — das ist eine Aufgabe für den Betreiber, siehe „Offen".*

### ⚠️ Ausserhalb der drei Muster: eine dritte **Leseliste**, kein dritter Eröffnungstext

`docs/START_HIER.md` (*„Der Einstieg für jede neue Sitzung"*, TB-51, 18.09.)
trägt in Abschnitt 2 *„In dieser Reihenfolge lesen"* eine **eigene** Liste —
**fünf** Dokumente, **andere Menge**: `ARBEITSWEISE.md`, `PRUEFPRINZIPIEN.md`,
`BACKLOG.md`, `UMGEBUNGEN.md`, `JOURNAL.md`; die Übergabe und `UMZUG.md` fehlen,
`UEBERGABEPROTOKOLL.md` steht als *„bei Bedarf"*. Die Suchmuster treffen sie
nicht, weil sie anders formuliert ist. **Gemessen, nicht geändert:**

| | |
|---|---|
| Zielgruppe | Claude-Code-Sitzungen im Repo (Pfade mit `docs/`), nicht der steuernde Chat — **eine andere Leserschaft**, deshalb kein Widerspruch im engen Sinn |
| ⚠️ toter Verweis | Z. 6: *„`ARBEITSWEISE.md` Abschnitt 10, Schritt 2"* — Abschnitt 10 ist seit TB-62 ein Verweis ohne Schritte |
| ⚠️ Stand | Z. 3–7 versprechen Aktualisierung *„bei jeder Sitzungsübergabe"*; Abschnitt 3 nennt den Snapshot als *„wird erst am Tag gezogen"* (er ist seit TB-55, 19.09., gezogen), Z. 34 nennt `JOURNAL.md` mit *„rund 4 000 Zeilen"* (gemessen 7 491) |
| ⭐ Vorschlag | in **TB-69** (`ARBEITSWEISE.md` neu ordnen) mitnehmen: **eine** Regel, welche Leseliste für welche Leserschaft gilt, und `START_HIER.md` entweder auf den Stand bringen oder auf `UMZUG.md` Abschnitt 6 + `CLAUDE.md` zurückführen. ⛔ **Hier nicht geändert** — es ist kein Eröffnungstext, und der Auftrag erlaubt nur dessen Reparatur |

---

## Schritt 5 — eine Zeile im Backlog, der Journal-Nachtrag

| | gemessen |
|---|---|
| Höchste K-Nummer, Muster `^\| \*\*(K[0-9][a-z])\*\*` ohne schliessenden Balken, kein `sort -u` | **`K4h`** (86 Treffer in `BACKLOG.md`; `K4i` in `BACKLOG.md` und allen Nachträgen 0 Treffer) |
| Eingetragen | **`K4i`**, Abschnitt 4, direkt nach `K4h`; `numstat` `BACKLOG.md` **1/0** |
| Journal-Nachtrag | `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20h.md` — Buchstabe **h** (20a–20f liegen in `_eingearbeitet/`, 20g offen, 20h nirgends vergeben; gemessen). Trägt die **Quellenzeile aus TB-67** im Kopf, wörtlich zu übernehmen |

Commit `4326ff2`.

---

## Nachweis 7 — nichts ausserhalb `docs/` geändert

`git diff --stat a15746f HEAD -- . ':!docs'` → **leer**. Alle zwölf Dateien der
Sitzung liegen unter `docs/` (Liste unten). `logs/auftraege/` unangetastet
(Nachweis 4).

`git diff --numstat a15746f HEAD` — **alle Dateien seit Sitzungsbeginn**, mit
Zuordnung, wer sie geschrieben hat:

| Datei | + | − | von |
|---|---:|---:|---|
| `docs/ERGEBNIS_TB-68_eroeffnungstext.md` | 277 + Abgabe | 0 | diese Sitzung |
| `docs/projektfuehrung/UMZUG.md` | 39 | 17 | diese Sitzung — Nachweis 5 |
| `docs/projektfuehrung/UEBERGABE_2026-09-19.md` | 9 | 20 | diese Sitzung — Nachweis 5 |
| `docs/auftraege/MAC_TB-63_epics_auslagern.md` | 1 | 1 | diese Sitzung — Nachweis 5 |
| `docs/projektfuehrung/BACKLOG.md` | 1 | 0 | diese Sitzung — `K4i` |
| `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20h.md` | 109 | 0 | diese Sitzung |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | 14 | 10 | **Betreiber** (Schritt 0 + Zwischencommit) |
| `docs/auftraege/MAC_TB-64_nachtragswaechter.md` | 30 | 0 | **Betreiber** (Schritt 0) |
| `docs/projektfuehrung/ARBEITSWEISE.md` | 30 | 2 | **Betreiber** (Schritt 0 — Abschnitt 6d) |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20d_tagesreihe.md` | 125 | 0 | **Betreiber** (Schritt 0) |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-20c_kapitalpfad.md` | 112 | 0 | **Betreiber** (Schritt 0) |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-20d_mtm_messung.md` | 107 | 0 | **Betreiber** (Zwischencommit) |

⛔ **Auflage „In einfacher Sprache" bleibt unangetastet — eingehalten:**
`ARBEITSWEISE.md` Abschnitte 4 und 17, `DOKUMENTATIONSSTANDARD.md` Z. 150/168,
`UMZUG.md` Z. 267 (jetzt verschoben, inhaltlich unverändert) — keine dieser
Stellen von dieser Sitzung berührt; die 2 entfernten Zeilen in `ARBEITSWEISE.md`
stammen aus dem Betreiber-Stand vor Sitzungsbeginn (Nachweis 1).

---

## Was der Auftrag vorgab, und wo die Messung abweicht

| Auftrag | Messung / Handlung |
|---|---|
| *„keine Kopie mehr, sondern ein Widerspruch"* — unterstellt Auseinanderlaufen | **als Widerspruch geboren:** derselbe Commit `2723c16`, seither unverändert (Nachweis 2) |
| Abschnitt 6 bleibt, Block 9 wird Verweis — **nur diese zwei Stellen** | ⭐ **zusätzlich `UMZUG.md` Schritt 3, Zeile 9** — das Verfahren ordnete die Kopie an; ohne die Änderung käme sie mit der nächsten Übergabe zurück (Nachweis 2). **Und Abschnitt 8, „Ergänzung zur Vorlage"** — der Vierzeiler stand neben dem Text statt darin; jetzt darin, der Nachsatz ist Vermerk |
| „vier gegen fünf" — offen gelassen, welcher Inhalt gilt | **fünf**, mit Begründung (Schritt 2/3); der offene Auftrag TB-63 nennt „VIER" — markiert, nicht umgeschrieben |
| Schritt 4: drei Suchmuster | **plus** `START_HIER.md` als Leseliste anderer Formulierung — gemessen, nicht geändert, an TB-69 vorgelegt (Nachweis 4) |
| Nachweis 3: *„jeden Pfad mit `test -f`"* | ausgeführt für den Repo-Pfad; **die Projektablage ist vom Mac nicht messbar** — deshalb Repo-Pfade im Text (Nachweis 3) |
| Schritt 1: *„Welche Fassung hat der Betreiber zuletzt benutzt"* | **nicht messbar** (Chatverlauf ist kein Träger); ersetzt durch die Messung, was das Verfahren vorschreibt (Nachweis 2) |
| Arbeitsbaum sauber nach Schritt 0 | ja — aber der Betreiber hat **während der Sitzung zweimal** ins Repo geschrieben; je eigener Zwischencommit, damit kein Diff dieser Sitzung fremde Zeilen trägt |

---

## Offen — für den Betreiber und für Folgeaufträge

| | wer | Empfehlung |
|---|---|---|
| **(a)** `UEBERGABEPROTOKOLL.md` im Lesepfad — drei Wege (Nachweis 6) | **Betreiber** | eine „bei Bedarf“-Zeile mit Pfad |
| **(b)** Platzhalter oder fester Name (Nachweis 6) | **Betreiber** | fest; danach Umbenennung nach `UEBERGABE.md` aus dem Kopf der Übergabe |
| **(c)** ⚠️ **Projektablage nachziehen:** `UMZUG.md` und `UEBERGABE_2026-09-19.md` sind geändert, beide Fassungen müssen gleich lauten (`UMZUG.md` Schritt 4, `K4e`) | steuernder Chat / Betreiber | im nächsten Chat als Erstes, sonst liest der nächste Umzug die alte Fassung aus der Ablage |
| **(d)** `logs/auftraege/_erledigt/UMZUG.md` und `…/UEBERGABE_2026-09-19.md` tragen den alten Text; Bringschuld erfüllt | Betreiber | löschen (Regel 9) — auf Nachfrage, nicht von selbst |
| **(e)** `START_HIER.md`: dritte Leseliste, toter Verweis auf „Abschnitt 10, Schritt 2", Stand 18.09. | **TB-69** | eine Regel, welche Liste für welche Leserschaft; Datei auf Stand oder zurückführen |
| **(f)** Journal-Nachtrag (20h) einarbeiten | nächste Einarbeitung / TB-64 | Block nach `BU` |

---

## Die Commits dieser Sitzung

| Commit | Schritt | Inhalt |
|---|---|---|
| `b1d8429` | 0 | fünf Betreiber-Dateien aus dem Arbeitsbaum gesichert |
| `30d44f7` | — | Zwischencommit: Auftragszeiger (Betreiber, während der Sitzung) |
| `6e0378f` | — | Zwischencommit: Fable-Antwort 20d (Betreiber, während der Sitzung) |
| `643fadd` | 1 | Messung, Nachweise 1–3 |
| `fa6b6ed` | 2/3 | eine Fassung, berichtigte Pfade, Block 9 → Verweis, TB-63-Vermerk, Nachweise 5 und 6 |
| `42fc34d` | 4 | Suche nach der dritten Fassung, Nachweis 4 |
| `4326ff2` | 5 | `K4i`, Journal-Nachtrag (20h) |
| *(folgt)* | Abgabe | dieses Dokument abgeschlossen |

Alle auf `main`, jeder Schritt einzeln gepusht (`git push` allein, nie in einem
`&&`-Block).

---

## In einfacher Sprache

**Was wir wissen wollten:** Warum steht der Text, den ein neuer Chat als Erstes
liest, zweimal im Repo — und was gilt?

**Was herauskam:** Die beiden Texte sind nicht mit der Zeit auseinandergelaufen,
sie waren **von der ersten Minute an verschieden** — beide kamen im selben
Commit ins Repo und wurden danach nie angefasst. Und der eigentliche Grund für
die Doppelung stand im Verfahren selbst: Es verlangte eine Vorlage **und** eine
Abschrift in jeder Übergabe. Hätte man nur die Abschrift entfernt, wäre sie bei
der nächsten Übergabe vorschriftsmässig wieder aufgetaucht.

**Was jetzt gilt:** Der Text steht **einmal**, in `UMZUG.md` Abschnitt 6, und
sagt selbst, dass er die verbindliche Fassung ist. Er nennt fünf Dokumente,
jedes mit dem Pfad, unter dem es im Repo wirklich liegt — vor allem
`PRUEFPRINZIPIEN.md`, das nie dort lag, wo beide Texte es behauptet haben. Die
Prüfung der Geräteanbindung, die bisher als Nachsatz neben dem Text stand,
steht jetzt im Text. In der Übergabe steht statt der Abschrift ein Verweis, und
das Verfahren verlangt künftig den Verweis statt der Kopie.

**Was du entscheidest:** Ob das Betriebshandbuch (`UEBERGABEPROTOKOLL.md`,
141 KB) mit in die Leseliste soll. Gemessen: Die Claude-Code-Sitzungen lesen es
ohnehin, weil `CLAUDE.md` es verlangt; der steuernde Chat hat es in 32 von 40
Ergebnisdokumenten und in keinem seiner eigenen Führungsdokumente gebraucht.
**Empfehlung: eine Zeile „bei Bedarf" mit dem Pfad, nicht als Pflicht.** Und ob
im Text der feste Dateiname der Übergabe steht oder ein Platzhalter —
**Empfehlung: fest**, weil ein eingefügter Platzhalter den Chat auf eine Datei
schickt, die es nicht gibt.

**Was noch auffiel, aber nicht angefasst wurde:** `START_HIER.md` trägt eine
dritte Leseliste — für eine andere Leserschaft, mit anderer Menge und einem
Verweis, der ins Leere geht. Das gehört in die Neuordnung der Arbeitsweise
(TB-69), nicht in diese Reparatur.
