# Anfrage: Konzept für das Handling des Projektwissens (Projekt Trading Bots)

**An:** Projekt-Chat Trading Bots (Fable)
**Von:** Betreiber, 26.09.2026
**Ergebnis:** `projektfuehrung/FABLE_ANTWORT_<JJJJ-MM-TT><buchstabe>_konzept_projektwissen.md` (Entwurf zur Freigabe); die Umsetzung macht danach die Mac-Sitzung per Auftrag.

---

## 1. Ausgangslage (Vorbemerkung des Betreibers)

Das Projektwissen ist bei **145 Dateien, 1.540.610 von 2.000.000 Tokens (77 %)**. Das Projekt läuft noch, aber im Projekt Apps ist der Speicher in den letzten zwei Tagen dreimal vollgelaufen, und die Kurve hier zeigt in dieselbe Richtung. Ich will das lösen, bevor es hier passiert.

Der Bestand wurde am 26.09. maschinell über die Projektschnittstelle ausgelesen (Tokens gerundet):

| Bereich | Dateien | Tokens | Anteil |
|---|---|---|---|
| `projektfuehrung/REGISTER_KOPIE_*` (Stände 21.09., 22.09., 24.09. sowie 24.09. in drei Teilen) | 6 | 735k | **48 %** |
| `projektfuehrung/FABLE_ANFRAGE_*` / `FABLE_ANTWORT_*` / `FABLE_WOCHENRUECKMELDUNG_*` | 89 | 375k | 24 % |
| `projektfuehrung/BACKLOG.md` | 1 | 105k | 7 % |
| `auftraege/MAC_TB-*` (+ `projektfuehrung/MAC_TB-82…86`) | 21 | 121k | 8 % |
| `projektfuehrung/UEBERGABE_*` (19.09., 24.09., 25.09.) | 3 | 54k | 3 % |
| `projektfuehrung/ERGEBNIS_TB-114…116` | 3 | 32k | 2 % |
| `ARBEITSWEISE.md` (33k), `UMZUG.md`, `PRUEFPRINZIPIEN.md`, `DOKUMENTATIONSSTANDARD.md`, Nachträge | 8 | 60k | 4 % |
| Rest (Bestandsaufnahmen, Plan, Projektstand, Aufgaben, Stoffsammlung, Recherche, Belege …) | 14 | 58k | 4 % |

Auffällig:

- **Fast die Hälfte sind Register-Schnappschüsse.** Vier Stände desselben Registers liegen nebeneinander, der vom 24.09. sogar doppelt (ganz und in drei Teilen). Im Retrieval-Modus ist das der schlimmste Fall: Zu jeder Registerfrage findet die Suche vier Fassungen und weiß nicht, welche gilt.
- **Die Fable-Antworten wachsen täglich** um mehrere Dateien (allein 26.09.: acht). Sie sind Dialog, nicht Stand: Was daraus gilt, sollte im Backlog oder in einer Festlegung stehen, nicht nur in der Antwort.
- **BACKLOG.md mit 105k Tokens** ist als eine Datei zu groß, um bei jeder Frage vollständig mitgelesen zu werden.
- Anders als bei Apps liegt hier **alles auch im Repo** (`~/trading-bot`, Git). Das Projekt ist ein Spiegel der Projektführung, nicht der einzige Träger. Das macht Auslagern einfach: Was nicht ins Projekt gehört, wird schlicht nicht mehr hochgeladen.

Zum Hintergrund: Ab einer bestimmten Größe arbeitet das Projekt im Retrieval-Modus. Claude liest dann nicht mehr alles, sondern sucht die passenden Stellen. Ein kleiner, kuratierter Bestand mit einer gültigen Fassung je Dokument trifft dabei besser als ein großer mit Doppelungen. Anthropic-Doku: https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects

## 1a. Vorbemerkung des steuernden Chats (26.09.2026, 22:40, auf Wunsch des Betreibers ergänzt)

Drei Tatsachen, die das Konzept tragen muss. Die ersten beiden sind gemessen bzw. aus der Arbeitsweise dieses Chats belegt:

1. **Es gibt keinen automatischen Upload.** `projektfuehrung/` wird nicht gespiegelt. Jede Datei in der Projektablage hat der steuernde Chat einzeln mit dem Projektwerkzeug (`project_write`) abgelegt, oder der Betreiber hat sie hochgeladen. Beispiel 26.09.: ERGEBNIS_TB-114/115/116, FABLE_ANFRAGE_27a, UEBERGABE und AUFGABEN wurden gezielt abgelegt, damit du sie lesen kannst. Folgen für Punkt 7:
   - Ein Repo-Ordner, „den der Upload auslässt“, ist nicht nötig.
   - Nötig ist eine **Regel für den steuernden Chat**: was er ablegt, wann er es wieder entfernt, und wie er die Auslastung misst.
   - Das Werkzeug kann Textdokumente löschen (`project_delete`). Datei-Uploads (PDF, Bilder) kann es nicht löschen, die entfernt der Betreiber in claude.ai.
   - Git bleibt die Sicherung. Entfernen aus der Ablage verliert nichts, solange die Datei im Repo committet ist.
2. **Du liest nur die Projektablage, nicht das Repo.** Deine Prüfung stützt sich auf das, was dort liegt: Registerkopien, ERGEBNIS-Dateien, Anfragen.
   - In 26a hast du eine eigene Aussage erst nach einer Suche in `REGISTER_KOPIE_…_teil1` berichtigt; deine Regel dort lautet „im Text suchen, nicht erinnern“.
   - ⚠️ Die Registerkopien in der Ablage stehen auf dem Stand **24.09. (Abschnitte 0–40)**. Das Register hat heute die Abschnitte 0–45 (46 kommt mit TB-117) und über 10 000 Zeilen. Die Abschnitte 41–45 kennst du nur aus Anfragen und Antworten, nicht aus einer Kopie.
   - Das Konzept braucht deshalb **eine** aktuelle, vollständige Registerfassung in der Ablage (Punkt 2) und eine Regel, **wann** sie erneuert wird (etwa nach jedem Registerauftrag). Sonst prüfst du gegen einen alten Stand.
   - Dasselbe gilt für ERGEBNIS-Dateien, auf die eine offene Anfrage verweist: Sie müssen liegen, bis die Antwort da ist.
3. **Sichtschutz 27.1.** Alles in der Ablage siehst du. Bitte im Register 27 nachsehen, nicht aus dem Gedächtnis, und im Konzept festhalten, ob und ab wann Dateien mit Ergebnisgrössen des Selektionsraums in die Ablage dürfen. Das betrifft die Klassen „Ergebnisse“ und „Belege“.

**Nummern:** Deine Antwort auf diese Anfrage bekommt den Buchstaben **27b** (27a ist vergeben), also `FABLE_ANTWORT_2026-09-27b_konzept_projektwissen.md`. Die nächste Tagesanfrage mit TB-116 (Leiter-Lesarten) und TB-117 wird 27c.

## 2. Deine Aufgabe

Entwickle ein **Konzept für das Handling der Projektwissensdaten**, das

- **die Sicherung des Wissens gewährleistet** (nichts geht verloren; jede Festlegung, jede Messung, jedes Ergebnis bleibt auffindbar und belegbar),
- **im weiteren Verlauf tragfähig ist** (Register 60, TB-300, Monate Betrieb – ohne dass der Speicher vollläuft und ohne dass alle paar Tage von Hand aufgeräumt wird),
- **die Arbeitsteilung berücksichtigt:** Mac-Sitzung baut und misst (Aufträge `MAC_TB-*`, Ergebnisse `ERGEBNIS_*`), du prüfst und antwortest (`FABLE_ANFRAGE_*` → `FABLE_ANTWORT_*`), der Betreiber meldet nur „Fable ist fertig" und will möglichst wenig klicken.

Kernfrage: **Was muss im Projekt liegen, was bleibt nur im Repo, und wie kommt Wissen aus dem Dialog (Fable-Antworten, Ergebnisse) verlässlich in die Standdokumente?**

## 3. Was das Konzept mindestens beantworten soll

1. **Klassen von Inhalten** mit je: Ort (Projekt und Repo / nur Repo / Archiv), Pflege (wer, wann), Aufbewahrung im Projekt (bis wann). Mindestens: Regelwerk (ARBEITSWEISE, PRUEFPRINZIPIEN, DOKUMENTATIONSSTANDARD, UMZUG), Stand (Backlog, Projektstand, Aufgaben, aktuelle Übergabe), Register, Aufträge, Ergebnisse, Fable-Anfragen und -Antworten, Belege, Bestandsaufnahmen und Stoffsammlungen.

2. **Register.** Was ist die eine gültige Registerfassung im Projekt, wie heißt sie (ohne Datum im Namen, damit die Suche immer dieselbe findet), wie wird sie fortgeschrieben, und was passiert mit den datierten Kopien (21.09., 22.09., 24.09., 24.09. Teile 1–3)? Ist die Aufteilung in Teile nötig, oder ist eine Datei mit klaren Abschnittsüberschriften besser?

3. **Fable-Antworten.** Vorschlag prüfen: Antworten bleiben **N Tage** (oder bis zur nächsten Übergabe) im Projekt; danach wird jede Antwort in eine **Festlegung oder einen Backlog-Eintrag** verdichtet (5–10 Zeilen: Frage, Antwort, Konsequenz, Verweis auf den Volltext im Repo), der Volltext bleibt nur im Repo. Was ist mit Antworten, die noch offen sind? Wie erkennt die Mac-Sitzung, welche Antworten schon verdichtet sind (z. B. Markierung im Dateinamen oder eine Liste `FABLE_ANTWORTEN_VERDICHTET.md`)?

4. **Backlog.** Wie wird `BACKLOG.md` (105k) so aufgeteilt, dass die Suche trifft: z. B. `BACKLOG.md` nur offen, `ENTSCHEIDUNGEN.md` für Festlegungen, `ERLEDIGT_<Monat>.md` für Abgeschlossenes im Repo, nicht im Projekt? Was ist mit `BACKLOG_NACHTRAG_2026-09-18.md` und `JOURNAL_NACHTRAG_2026-09-18.md`?

5. **Aufträge und Ergebnisse.** Erledigte `MAC_TB-*`-Aufträge: bleiben sie im Projekt, oder nur der Ergebnisbericht? Wie lange? Vorschlag: nach `ERGEBNIS_TB-nnn` und Auswertung wandert der Auftrag ins Repo-Archiv. Was gilt für die vier MAC-Dateien, die in `projektfuehrung/` statt `auftraege/` liegen?

6. **Übergaben.** Nur die aktuelle im Projekt? Was aus älteren Übergaben noch gilt, gehört in ARBEITSWEISE oder Backlog.

7. **Der Sync-Mechanismus.** Heute wird `projektfuehrung/` offenbar vollständig hochgeladen. Schlage eine Regel vor, was der Upload **auslässt** (z. B. Ordner `projektfuehrung/archiv/` und `projektfuehrung/antworten_verdichtet/` im Repo, die nie ins Projekt gehen), und wie die Mac-Sitzung beim Aufräumen vorgeht: Datei im Repo verschieben (Git hält die Historie) → Betreiber entfernt im Projekt (oder eine Sitzung mit Browserzugriff) → Prüfung des Standes. Ein Manifest wie bei Apps ist hier nicht nötig, weil Git die Sicherung ist – prüfe, ob das reicht oder ob ein zusätzliches Zip in `~/Sites/_projektarchiv/` sinnvoll ist.

8. **Schwellen und Routine.** Zielgröße (Vorschlag: ≤ 1,0 Mio. Tokens = 50 %, damit Register und Antworten Platz haben und die Suche gut trifft), Warnschwelle (70 %), fester Aufräumschritt **vor jeder Übergabe** (UMZUG) und **wöchentlich** (die Wochenrückmeldung könnte den Stand des Speichers mit melden). Wer misst die Auslastung? (Die Projektansicht zeigt sie unter „Dateien".)

9. **Sofortliste.** Nach deinem Konzept: welche Dateien jetzt aus dem Projekt raus (mit Tokens, Summe, und was nach dem Aufräumen übrig bleibt), so dass ich sie per Auswahlkarte freigeben kann. Ich erwarte, dass allein die Register-Kopien und die verdichteten Antworten der ersten Tage das Projekt unter 50 % bringen; prüfe das.

10. **Was nie ausgelagert wird.** Nenne ausdrücklich, was immer im Projekt bleibt.

## 4. Form des Ergebnisses

- Eine Datei nach dem Schema `projektfuehrung/FABLE_ANTWORT_<JJJJ-MM-TT><buchstabe>_konzept_projektwissen.md`, gegliedert nach den Punkten oben, mit **einer Tabelle je Klasse** (Ort · Pflege · Aufbewahrung · Beispiel-Dateien) und der **Sofortliste**.
- Jede Regel mit Begründung und mit Angabe, welche bestehende Regel (ARBEITSWEISE, UMZUG, DOKUMENTATIONSSTANDARD, PRUEFPRINZIPIEN) sie ändert oder ergänzt. Regelwerk erst nach meiner Freigabe ändern.
- Dazu einen **Entwurf des Mac-Auftrags** (`auftraege/MAC_TB-nnn_projektwissen_aufraeumen.md`), der die Umsetzung Schritt für Schritt beschreibt, so dass die Mac-Sitzung ihn ohne Rückfrage ausführen kann.
- Abschnitt „In einfacher Sprache" am Ende.
- Rückfragen nur als Auswahl mit Empfehlung.

Sag mir kurz, was du verstanden hast, bevor du anfängst.
