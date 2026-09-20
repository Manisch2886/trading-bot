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

