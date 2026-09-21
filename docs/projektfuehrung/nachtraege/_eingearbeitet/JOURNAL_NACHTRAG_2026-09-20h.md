# Journal-Nachtrag (h) — 20.09.2026, TB-68: der Eröffnungstext steht nur noch einmal — und das Verfahren hatte die Kopie selbst bestellt

**Quelle:** Mac-Sitzung **TB-68 Eroeffnungstext**, 20.09.2026, ab etwa 18:20
Ortszeit, Ausgang `a15746f`, reine Dokumentation (kein Interpreter, keine
Kursdaten, nichts ausserhalb `docs/`). Commits `b1d8429` (Schritt 0, fünf
Betreiber-Dateien), `30d44f7` und `6e0378f` (Zwischencommits für Dateien, die
der Betreiber während der Sitzung ablegte), `643fadd` (Schritt 1, Messung),
`fa6b6ed` (Schritt 2/3, eine Fassung), `42fc34d` (Schritt 4, Suche), dann
Backlog `K4i`, dieser Nachtrag und die Abgabe. Ergebnisdokument
`docs/ERGEBNIS_TB-68_eroeffnungstext.md`. **Einzuarbeiten als nächster Block
nach dem höchsten vorhandenen** (am 20.09.2026 gemessen: `BT`; `(20g)` aus
TB-67 liegt davor und wird `BU`, dieser Nachtrag also voraussichtlich `BV` — die
Nummer vergibt die einarbeitende Sitzung).

⭐ **Quellenzeile für den Block, wörtlich zu übernehmen:**

```
*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20h.md`*
```

---

## Was der Auftrag wollte und was er bekam

Den Eröffnungstext für einen neuen Chat, der in `UMZUG.md` Abschnitt 6 und in
`UEBERGABE_2026-09-19.md` Block 9 in zwei einander widersprechenden Fassungen
stand (vier gegen fünf Dokumente, Platzhalter gegen festen Namen, beide mit dem
Pfad `projektfuehrung/PRUEFPRINZIPIEN.md`, unter dem die Datei nie lag), auf
**eine** Fassung an **einem** Ort bringen, den Pfad berichtigen, nach einer
dritten Fassung suchen, zwei Fragen dem Betreiber vorlegen statt sie zu
entscheiden.

**Bekommen hat er alles davon — und zwei Dinge, die er nicht wusste:**
Abschnitt 6 ist die einzige Fassung (fünf Dokumente, je mit Repo-Pfad,
`PRUEFPRINZIPIEN.md` ohne Ordner, Prüfung der Geräteanbindung im Text), Block 9
ist ein Verweis (9/20 Zeilen, jede entfernte zugeordnet), keine dritte Fassung
in `docs/` (drei Muster, je Trefferzahl vorher/nachher), `K4i` im Backlog. Die
beiden Fragen (`UEBERGABEPROTOKOLL.md` im Lesepfad; Platzhalter oder fester
Name) liegen mit Messung und Empfehlung vor.

---

## Drei Befunde

### 1. Die beiden Fassungen sind nicht auseinandergelaufen — sie wurden so geboren

`git log -L` über beide Zeilenbereiche: **derselbe Commit `2723c16`**
(19.09.2026, 21:40), **seither keine Änderung** an keiner der beiden. Der
Auftrag sprach von *„keine Kopie mehr, sondern ein Widerspruch"* — gemessen war
es nie eine Kopie. Die Fassung in der Übergabe hatte an zwei Stellen recht
(`UMZUG.md` gehört in die Liste, der feste Name ist der, der existiert) und an
einer unrecht (die Zusatzzeile zu `ARBEITSWEISE.md` Abschnitt 10 war seit
TB-62 überholt); die Fassung in `UMZUG.md` hatte den Ort, den das Verfahren
als *„Vorlage"* benennt. **Die bleibende Fassung nimmt den Ort der einen und
den Inhalt der anderen.**

### 2. ⭐ Das Verfahren hatte die zweite Fassung nicht zugelassen, sondern bestellt

`UMZUG.md` Abschnitt 4, Schritt 3 führt neun Pflichtblöcke jeder Übergabe —
**Zeile 9: „Der Eröffnungstext für den neuen Chat, fertig zum Kopieren."**
Schritt 6 nennt Abschnitt 6 die Vorlage. Vorlage plus Abschrift, angeordnet.
Wer nur Block 9 kürzt, bekommt die Kopie bei der nächsten Fortschreibung der
Übergabe pflichtgemäss zurück. **Deshalb ist Schritt 3, Zeile 9 mitgeändert:
sie verlangt jetzt den Verweis.** *Das stand nicht im Auftrag; es ist der Teil,
ohne den die Reparatur eine Übergabe lang gehalten hätte.*

⭐ **Regel:** *Ein Verfahren, das eine Vorlage und eine Abschrift verlangt, hat
die zweite Fassung nicht zugelassen, sondern bestellt — die Reparatur muss die
Anordnung ändern, nicht nur die Kopie.* **Und die Fehlerklasse hat ein drittes
Mitglied:** Abschnitt 8 behauptete, der Eröffnungstext enthalte *„ab jetzt"* die
Prüfung der Geräteanbindung — enthielt sie aber als *„Ergänzung zur Vorlage"*
am Dateiende, nicht im Text. Ein Text mit angehängtem Flicken ist dieselbe
Klasse wie zwei Fassungen. Jetzt steht der Vierzeiler (wortgleich, per `diff`)
im Text.

### 3. Der tote Pfad war nie lebendig — und die Projektablage ist vom Mac nicht messbar

`git log --all --diff-filter=A -- docs/projektfuehrung/PRUEFPRINZIPIEN.md`:
**0 Commits.** Die Datei liegt seit ihrem ersten Commit (`e456756`, 18.09.) in
`docs/`. Der Eröffnungstext nennt aber Namen der **Projektablage** („über den
Projects-Zugriff"), und ob die Ablage die Datei unter `PRUEFPRINZIPIEN.md` oder
anders führt, kann eine Mac-Sitzung nicht prüfen. Deshalb trägt jedes der fünf
Dokumente jetzt **zusätzlich seinen Repo-Pfad in Klammern** — ein Chat mit
Geräteanbindung findet jede Datei, gleichgültig, wie die Ablage sie nennt. *Das
ist die Antwort auf das zweite Projekt, das am 20.09. genau an diesem Pfad
gescheitert ist.*

---

## Was der Auftrag anders sah — und wo die Messung galt

| Auftrag | gemessen |
|---|---|
| *„vier gegen fünf"* — Zuordnung Abschnitt 6 als Ort, ohne Festlegung des Inhalts | Ort bestätigt; **Inhalt fünf**, weil der Chat nach `UMZUG.md` Abschnitt 3 selbst auf den Umzug hinweisen soll und dazu die Auslöser kennen muss. ⚠️ Der offene Auftrag `MAC_TB-63` nennt *„VIER Dokumente"* als Menge der Pflichtlektüre — dort eine markierte Vermerkzeile, sonst nichts geändert |
| Schritt 4: drei Muster im `docs/`-Baum und in `logs/auftraege/` | ausgeführt, Zahlen im Ergebnisdokument; **ausserhalb der Muster** eine dritte **Leseliste** anderer Formulierung: `START_HIER.md` Abschnitt 2 — andere Menge (`UMGEBUNGEN.md`, `JOURNAL.md` statt Übergabe und `UMZUG.md`), andere Leserschaft (Claude-Code-Sitzungen), mit totem Verweis auf *„Abschnitt 10, Schritt 2"* und Stand vom 18.09. **Nicht geändert, an TB-69 vorgelegt** |
| `UEBERGABEPROTOKOLL.md` *„messen, wie oft es in den letzten Sitzungen gebraucht wurde"* | gemessen über Auftrags-, Ergebnis- und Führungsdokumente, Journal und Commit-Historie (Zahlen in Nachweis 6). **Empfehlung: eine „bei Bedarf“-Zeile mit Pfad, nicht in die Pflichtliste** — jede Claude-Code-Sitzung liest es ohnehin über `CLAUDE.md` Z. 3 |

---

## Offen

| | wer |
|---|---|
| ~~`UEBERGABEPROTOKOLL.md` im Lesepfad~~ ✅ entschieden am Ende der Sitzung (anklickbare Frage): „bei Bedarf“-Zeile, umgesetzt in `UMZUG.md` Abschnitt 6 | — |
| ~~Platzhalter oder fester Name~~ ✅ entschieden: fest; offen bleibt nur die Umbenennung nach `UEBERGABE.md` aus dem Kopf der Übergabe | Betreiber |
| ⚠️ **Projektablage nachziehen:** `UMZUG.md` und `UEBERGABE_2026-09-19.md` sind geändert; nach `UMZUG.md` Schritt 4 und `K4e` müssen beide Fassungen gleich lauten | steuernder Chat / Betreiber |
| `logs/auftraege/_erledigt/UMZUG.md`, `…/UEBERGABE_2026-09-19.md`: Zwischenlager-Kopien mit erfüllter Bringschuld, tragen den alten Eröffnungstext — dürfen nach Regel 9 weg, Löschen fragt vorher | Betreiber |
| `START_HIER.md` — Leseliste, toter Verweis, Stand | TB-69 |
| Dieser Nachtrag ins Journal (Block nach `BU`) | nächste Einarbeitung / TB-64-Wächter |
