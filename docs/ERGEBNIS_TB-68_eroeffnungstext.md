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

