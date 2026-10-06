# TB-133 Regelwerk-Nachtrag 04.–06.10.2026 (Umzug nur auf Ansage, Sitzung über den Wächter, git über die Brücke, Ablage durch Helfer, Regeln aus vier Umzügen)

**Sitzungstitel:** `TB-133` · **Modell:** Opus 5.5 (Standard) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 06.10.2026 vom steuernden Chat
**Vorgänger:** TB-136 (`67a2202`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-133_regelwerk_nachtrag_umzug_sitzung_bruecke.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.

**Bauart wie TB-131** (`docs/auftraege/MAC_TB-131_regelwerk_nachtrag_ampel.md`, erledigt mit `0779453`): Verfahren je Einfügung, Schritt 0, Nachweis und Abgabe gelten wie dort. Dieser Auftrag nennt nur die Unterschiede und die Sollwerte. Einen Schritt B (Werkzeug) gibt es hier nicht.

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei** (Betreiberentscheid 26.09.2026; so auch TB-127, TB-128 und TB-131). Zwei Regeln hat der Betreiber wörtlich verlangt: am 05.10.2026, 21:25, „Legst du mir zukünftig wieder bereits eine claude code Sitzung an“ (E4), und am 05.10.2026, 23:58, „Nein du ziehst zukünftig um wenn ich das sage oder genehmige“ (E2, E8).

Geändert werden nur: `docs/projektfuehrung/ARBEITSWEISE.md`, `docs/projektfuehrung/UMZUG.md`, `docs/projektfuehrung/BACKLOG.md`, dazu Belege, Ergebnis und Journal.

⛔ **Nicht erlaubt, mit Grund:**
- Den vorgegebenen Text umformulieren, kürzen, glätten oder zusammenlegen. *Grund:* Die Wortlaute hat der steuernde Chat aus den Quellen festgelegt und gegenlesen lassen; die Sitzung trägt sie ein (5b).
- Register, `docs/VORREGISTRIERUNG_*`, `research/`, `shared/`, `strategies/`, jede Sperrlisten-Datei, jedes Werkzeug unter `docs/werkzeuge/`. *Grund:* nicht Gegenstand.
- `UEBERGABE.md`, `UEBERGABE_ARCHIV.md`, die `FABLE_*`-Dateien, `REGISTER_INDEX.md` und die Registerkopie ändern. *Grund:* Das sind die Quellen; Index und Kopie gehören zum Register.
- Bestehende Zeilen in `ARBEITSWEISE.md`, `UMZUG.md` und `BACKLOG.md` ändern oder entfernen. *Grund:* Dieser Auftrag fügt nur ein; wo eine neue Zeile einer alten vorgeht, sagt sie es selbst.

Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt (auch `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`); das ist kein Ändern im Sinn der Verbote und des Abbruchkriteriums.

**Sichtschutz:** entfällt, es werden keine Ergebnisse gelesen.

## Belegt · erschlossen · offen

- **Belegt:** Die Quellen der Regeln stehen in `docs/projektfuehrung/UEBERGABE.md` unter den Überschriften, die die Spalte „steht in“ nennt (gemessen 06.10.2026: Umzug 04.10.2026, 10:56; Umzug 04.10.2026, 13:17; Nachtrag 04.10.2026, 09:50; Nachtrag 04.10.2026, 21:07; Nachtrag 05.10.2026, 21:27; Umzug 05.10.2026, 22:31; Nachtrag 05.10.2026, 22:55; Umzug 05.10.2026, 23:46; Nachtrag 06.10.2026, 00:13).
- **Erschlossen:** Die Zeilenbilanz für E8 und E9 (C2) setzt voraus, dass vor dem Anker schon genau eine Leerzeile steht (gemessen für `UMZUG.md` Z. 107 und `BACKLOG.md` Z. 295) und dass das Skript sie nicht verdoppelt, wie bei E5 in TB-131.
- **Offen:** nichts.

## Verfahren je Einfügung (E1–E9)

*Vorgezählt vom steuernden Chat am 06.10.2026, 00:24, über die Geräteanbindung (Python `str.count`) am `67a2202`: jeder Anker genau 1; die ersten Zeilen der neuen Texte kommen in den Zieldateien noch nicht vor. `ARBEITSWEISE.md` hat 2 397 Zeilen (md5 `42e208032b02d9ab586fb3c8841e3f75`), `UMZUG.md` 378 (md5 `edfe2a34ffa016eaf3ab8ea5bdfdd5a8`), `BACKLOG.md` 307 (md5 `c005a57d88d84dd6c6bbfa626fbc8a95`). Die Sitzung zählt selbst nach; ihre Zahl gilt.*

Wie TB-131, „Verfahren je Einfügung“, Nr. 1 bis 4 (Vorlagen `docs/belege/TB-131/einfuegen.py` und `docs/belege/TB-131/c3_vergleich.py`; die Sitzung übernimmt sie nach `docs/belege/TB-133/` und stellt die festen Stellen um). Umzustellen sind in `einfuegen.py` der Pfad dieses Auftrags, der Belegordner, `BLOECKE` (dort `{"E5"}`, hier E8 und E9) und die erwartete Nummernfolge (dort E1–E5, hier E1–E9); in `c3_vergleich.py` der Pfad, der Belegordner, die erwartete Anzahl (dort 5, hier 9) und der Teil zu `ampel.py` (`Soll nachher: md5 …`), der hier entfällt; dazu in beiden Skripten die Kopfzeile der Ausgabedatei (`# TB-131 …`). Unterschiede:

- **Tabellenzeilen** sind E1 bis E7 (ohne Leerzeilen). **Blöcke** sind E8 und E9: genau eine Leerzeile davor und danach, eine vorhandene wird nicht verdoppelt (wie E5 in TB-131).
- Der Codeblock von E9 trägt eine Zeile, die mit `### ` beginnt. `c3_vergleich.py` schneidet deshalb nur an `#### E<n>` und an `## ` (so schon in TB-131, ERGEBNIS_TB-131 „Abweichungen und Lesarten“).
- Wird ein Skript per `sed` aus der Vorlage abgeleitet, danach den Vorlagenvermerk im Kopf prüfen (ERGEBNIS_TB-131: der Ersatz traf ihn mit).

Ergebnis je Einfügung in `docs/belege/TB-133/einfuegungen.txt`: `E<n> · Datei · Anker vorher · ausgeführt ja/nein · Text nachher`.

## Schritt 0 — Sicherung, Ausgang

0a. **Zuerst, bevor `docs/belege/TB-133/` verändert wird:** `git status --porcelain > "$TMPDIR/tb133_0a.txt"`. Soll: genau die Einträge unten; die Reihenfolge zählt nicht. Weicht etwas ab ⇒ Abbruch. Danach die Datei nach `docs/belege/TB-133/0a_status.txt` kopieren. (Der Ordner `docs/belege/TB-133/` besteht schon: Er trägt `vormessung/v1_vormessung_04a.md`, committet seit `753ae38`. Diese Datei bleibt unberührt.)

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-133_regelwerk_nachtrag_umzug_sitzung_bruecke.md
```

Commit `TB-133 Schritt 0: Stand des steuernden Chats 06.10.2026`, pushen. Der Commit heisst im Folgenden **⟨S0⟩**.

0b. sha256, md5 und Zeilenzahl der drei Zieldateien ⇒ `docs/belege/TB-133/0b_ausgang.txt`. Soll: md5 und Zeilenzahl aus der Vorzählung oben (sha256 nur messen); weicht eine Datei ab ⇒ ihre Einfügungen trotzdem nach dem Verfahren ausführen (der Anker entscheidet), die Abweichung vermerken (kein Abbruch). Die Belege aus 0a und 0b gehen mit dem Commit aus Schritt A.

## Schritt A — Die Einfügungen

#### E1 — Abschnitt 0, „Immer“: Uhrzeiten messen

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Fundstellen nur, wenn sie vor mir liegen; sonst steht` · Art: **nach der Zeile**

```
| ☐ | Uhrzeiten mit `date` messen, im selben Schritt, in dem sie in einen Text gehen — nie schätzen (05.10.2026: 23:50 geschrieben, 23:43 gemessen) | UEBERGABE, Umzug 05.10.2026, 23:46, Block 7 |
```

#### E2 — Abschnitt 0, „Wenn ein Arbeitsabschnitt endet oder ein Verlust droht“: Umzug nur auf Ansage

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Ein nötiger Umzug wird frühzeitig angekündigt — nach gemessener Ampel` · Art: **nach der Zeile**

```
| ☐ | ⭐⭐ Umgezogen wird nur, wenn der Betreiber es sagt oder genehmigt. Der steuernde Chat zieht nicht von sich aus um: Er kündigt den Umzug an (Zeile darüber, mit Zahl und Uhrzeit), fragt per Karte und arbeitet weiter, bis der Betreiber entscheidet (Betreiber 05.10.2026, 23:58: „Nein du ziehst zukünftig um wenn ich das sage oder genehmige“; Lesart des steuernden Chats, vorläufig: gilt bei jeder Ampelfarbe, Umzugsblock und Eröffnungstext erst nach dem Ja) | UMZUG 3; UEBERGABE, Nachtrag 06.10.2026, 00:13 |
```

#### E3 — Abschnitt 0, „Wenn Terminalbefehle drin sind“: git über die Brücke

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `auch nicht bei der allerersten Messung eines neuen Chats` · Art: **nach der Zeile**

```
| ☐ | Über die Geräteanbindung auch kein `git diff` (weder `--name-only` noch `--numstat`) und kein `git check-ignore`; erlaubt sind nur `rev-parse`, `log`, `show`, `ls-files` und `worktree list`, je mit `--no-optional-locks`. Geänderte Dateien zeigt `ls-files -m`, Unverfolgtes `ls-files -o --exclude-standard` (ein ignorierter Pfad erscheint dort nicht); Zeilenbilanzen mit `diff` zweier Kopien ausserhalb des Repos. Diese Zeile geht der Zeile darüber vor, soweit jene `diff --name-only` nennt (Liste aus der Vorgabe im Nachtrag 04.10.2026, 21:07; 04.10.2026: `diff --name-only` schrieb vermutlich `.git/index` neu, nicht bewiesen, und `diff --numstat` lag ausserhalb der Vorgabe; 05.10.2026: `check-ignore` ebenso) | UEBERGABE, Umzug 04.10.2026, 10:56, Block 7; Nachtrag 04.10.2026, 21:07; Umzug 05.10.2026, 22:31 und 23:46, Block 7 |
```

#### E4 — Abschnitt 0, „Wenn eine Mac-Sitzung startet, endet oder abbricht“: Sitzung über den Wächter, Fehler Nr. 20, Sonde

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Vor dem Schliess-Auslöser das Alter des letzten Commits messen` · Art: **nach der Zeile**

```
| ☐ | Ist ein Mac-Auftrag startklar, legt der steuernde Chat die Claude-Code-Sitzung selbst über den Sitzungswächter an, bevor er dem Betreiber „Satz abschicken“ als Aufgabe gibt. Weist der Wächter ab, weil eine alte Sitzung schläft, und hat sie nicht gearbeitet, schliesst der steuernde Chat sie über den Schliess-Auslöser und startet neu, ohne Rückfrage. „Nicht gearbeitet“ wird gemessen: kein Commit seit ihrem Start, letzter Commit älter als 600 s, nichts Neues unter dem Belegordner des Auftrags, Rechenzeit zwischen zwei Abweisungen des Wächters praktisch unverändert. Der Wächter ist seit dem 23.09.2026 der Weg (`docs/werkzeuge/sitzungswaechter/LIESMICH.md`); die Startblöcke weiter oben gelten für den Start von Hand (Betreiber 05.10.2026, 21:25: „Legst du mir zukünftig wieder bereits eine claude code Sitzung an“; Lesart des steuernden Chats, vorläufig) | UEBERGABE, Nachtrag 05.10.2026, 21:27 |
| ☐ | Ein Start ausserhalb des Wächters wird erst zugesagt, wenn gemessen ist, wo die Sitzung läuft (Fehler Nr. 20) | UEBERGABE, Umzug 04.10.2026, 10:56, Block 7 |
| ☐ | Ein abgewiesener Start-Auslöser taugt als Sonde: Der Wächter nennt PID, Laufzeit und Rechenzeit; zwei Abweisungen im Abstand zeigen, ob eine Sitzung arbeitet (05.10.2026) | UEBERGABE, Umzug 05.10.2026, 22:31, Block 7 |
```

#### E5 — Abschnitt 0, „Wenn Dateien abgelegt oder aus der Ablage gelesen werden“: Ablage durch Helfer, Zaunzeile, Suche der Ablage

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `„Frischer Stage-Pfad“ heisst ein neuer Pfadname` · Art: **nach der Zeile**

```
| ☐ | Die Erneuerung der Ablage (Abschnittsdateien, Index, Dialog-Index) macht ein Helfer, nicht der steuernde Chat; als Kontrolle genügt `project_info`. Statt vieler md5-Zeilen im Chat ein md5 über die md5-Liste (05.10.2026: 57 Antworten von `project_write` und eine Suche mit zwei ganzen Treffern standen im Chat) | UEBERGABE, Umzug 05.10.2026, 23:46, Block 7 |
| ☐ | Ausschnitte aus Codeblöcken an der Zaunzeile schneiden; weicht die gemessene Grösse von der erwarteten ab, zuerst den Bereich prüfen (05.10.2026: rund 15 KB statt rund 7 KB gelesen) | UEBERGABE, Umzug 05.10.2026, 22:31, Block 7 |
| ☐ | Die Suche der Ablage liefert Ausschnitte auch aus gesperrten Dateien (04.10.2026: `BACKLOG.md` im Leseprotokoll von Fable 04a). Wie ein solcher Ausschnitt unter dem Sichtschutz zählt, ist Lesart des steuernden Chats, vorläufig, und geht zur Kenntnis an Fable | UEBERGABE, Umzug 04.10.2026, 13:17, Block 4; Register 54.6 Nr. 9 |
```

#### E6 — Abschnitt 0, „Wenn ich ein fremdes Ergebnis bewerte“: Abnahme durch einen engen Helfer

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Ein „kein Widerspruch“ nennt, was gemessen ist und was nicht` · Art: **nach der Zeile**

```
| ☐ | Die Abnahme macht ein eng zugeschnittener Helfer, nur lesend, mit eigenem Ordner für Rohausgaben ausserhalb des Repos; er rechnet jede Zahl an der Rohausgabe nach (wie oben in dieser Gruppe), die Kernzahlen rechnet der steuernde Chat danach mit eigenen Befehlen nach (05.10.2026, Abnahme TB-136) | UEBERGABE, Nachtrag 05.10.2026, 22:55; Umzug 05.10.2026, 22:31 und 23:46, Block 7 |
```

#### E7 — Abschnitt 0, „Wenn ich einen Auftrag schreibe“: sechs Regeln aus den Umzügen vom 04.10. und 05.10.2026

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Folgeauftrag gleicher Bauart: auf den Vorgänger verweisen` · Art: **nach der Zeile**

```
| ☐ | Pfade und Inhaltsangaben in Helferaufträgen nur nach `ls` und Überschrift, nie aus dem Gedächtnis (04.10.2026) | UEBERGABE, Umzug 04.10.2026, 13:17, Block 7 |
| ☐ | Zeilenangaben, die in Registertext gehen, misst ein zweiter Helfer an der Quelle (04.10.2026: „02b Z. 128“ aus einem Helferbericht übernommen, richtig ist Z. 127) | UEBERGABE, Umzug 04.10.2026, 13:17, Block 7 |
| ☐ | Eigene Marken erst nennen, wenn die Markentabelle gemessen ist (04.10.2026: 48.7 angekündigt, richtig sind 48.1 und 48.14) | UEBERGABE, Umzug 04.10.2026, 13:17, Block 7 |
| ☐ | Der Chat, der eine Fable-Antwort bewertet, baut nicht auch den Registerauftrag (04.10.2026: Übernahme und Bewertung kosteten 173 189, der Bau im selben Chat führte auf 358 513) | UEBERGABE, Umzug 04.10.2026, 13:17, Block 7 |
| ☐ | Ein Registerauftrag sagt, was Schritt A committet (Abnahme TB-136: die Skripte für B, C und D lagen schon im Registercommit) | UEBERGABE, Nachtrag 05.10.2026, 22:55 |
| ☐ | Unveränderte Textteile übernimmt ein Skript aus der Quelle, mit `assert` auf die Ankerzeilen; abgetippt wird nichts (05.10.2026) | UEBERGABE, Umzug 05.10.2026, 23:46, Block 7 |
```

#### E8 — UMZUG, Abschnitt 3: Umzug nur auf Ansage oder mit Genehmigung

Zieldatei: `docs/projektfuehrung/UMZUG.md`
Anker: `### ⚠️ Wann NICHT umgezogen wird` · Art: **vor der Zeile**

```
⭐⭐ **Gilt seit 05.10.2026, 23:58 (Betreiber, „zukünftig“):** *„Nein du ziehst zukünftig um wenn ich das sage oder genehmige.“* Die Auslöser und die Ampel oben sagen, wann der steuernde Chat den Umzug **anspricht** — mit Zahl und Uhrzeit, als Karte. **Umgezogen wird erst, wenn der Betreiber es sagt oder genehmigt.** Bis dahin arbeitet der Chat weiter, bei jeder Ampelfarbe; den Umzugsblock nach Abschnitt 4 und den Eröffnungstext nach Abschnitt 6 schreibt er erst nach dem Ja (Lesart des steuernden Chats, vorläufig). Wo dieser Abschnitt einen Zeitpunkt für den Umzug nennt („am nächsten sauberen Stand“, „vor dem nächsten Auftrag“, „vor einer Pause“, „dann umziehen“, „vorher wird umgezogen“), ist das seither der Zeitpunkt für den Vorschlag. *Anlass: Am 05.10.2026, 23:46, schrieb der steuernde Chat bei grüner Ampel (Verlauf 184 639 um 23:44) von sich aus den Umzugsblock und gab den Eröffnungstext aus; der Betreiber lehnte ab und liess weiterarbeiten.*
```

#### E9 — BACKLOG, Abschnitt 5: aus der Abnahme TB-136 und aus den Umzügen und Nachträgen vom 04. bis 06.10.2026

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile**

```
### Aus der Abnahme TB-136 und aus den Umzügen und Nachträgen vom 04. bis 06.10.2026 — eingetragen mit TB-133

- **Ins Regelwerk eingetragen mit TB-133:** Umzug nur auf Ansage oder mit Genehmigung des Betreibers (05.10.2026, 23:58); die Claude-Code-Sitzung legt der steuernde Chat selbst über den Wächter an (05.10.2026, 21:25); git über die Brücke ohne `diff` und ohne `check-ignore`; die Erneuerung der Ablage macht ein Helfer; dazu die Regeln aus den Umzügen vom 04.10. und 05.10.2026 (`ARBEITSWEISE.md` Abschnitt 0, `UMZUG.md` Abschnitt 3). Damit ist die Zeile „Für TB-133“ oben erledigt.
- **Offen, Index-Bilanz TB-136:** Das Ergebnis nennt 193/155; `diff` zweier Kopien ergibt 192/154, der Saldo ist gleich. Ursache nicht gemessen.
- **Für den nächsten Registerauftrag:** T4 der Registerkopie steht bei 234 587 B; nach der Rechnung des Werkzeugs (Body 234 351 B, Reserve 240 B) bleiben 5 409 B bis zur Grenze 240 000. Setzt der nächste Eintrag Marken in 43–53, teilt das Werkzeug neu, und die Teilgrenzen im Indexkopf ändern sich (erschlossen, nicht gemessen). Die Bezeichnungen „Frühere Vierteilung“ und „T1 … T4“ im Index passen nicht mehr zu fünf Teilen.
- **Dialog-Index:** Das Handfeld `entscheidung` der Zeile 04a trägt einen Schlusssatz aus dem Auftrag TB-136, nicht aus Fables Antwort; die Zeile nennt die Anfragedatei nicht mit Dateinamen; `dialog_index.py` nennt als Quelle der Handfelder einen Block „**Kurz:**“, die Antwort hat „## Kurz“.
- **Aus dem Ergebnis TB-132, für später:** `registerkopie.py --marken` zählt Zeilen als Marken, die keine sind (Abschnitt 53: drei; dazu aus der Abnahme TB-136 die Registerzeilen 11538, 11545 und 11575); Reibung im Index, Tabelle 3, Zeile 3b (c); Markenwort ERGÄNZT an 48.7; `registerbericht.py --pruefen` rc 1. Dazu die Unschärfe der Freigabetabelle zu TB-132 (`UEBERGABE.md`, Nachtrag 04.10.2026, 09:50).
- **Cloud-Sitzungen, Regel noch nicht gefasst:** Betreiber 04.10.2026, 09:55: von Hand angelegte Cloud-Sitzung, Aufgabe als Kopierblock, Antwort als Textdatei im dortigen Chat, nichts wird abgelegt. Die Übergabe (Umzug 04.10.2026, 10:56, Block 4) fasst das als „nur für Leseaufgaben mit Textantwort“; `ARBEITSWEISE.md` Abschnitt 0 verlangt für angeleitete Läufe noch Belege unter `docs/belege/`. Zusammen mit dem Entwurf aus TB-137, Paket 15.
- **Nicht in TB-133:** der Fliesstext in `ARBEITSWEISE.md` 6b (Start) und 10 und die git-Liste im Eröffnungstext (`UMZUG.md` Abschnitt 6 nennt noch `diff --name-only`); beides zusammen mit dem Entwurf aus TB-137, Paket 15.
```

Commit `TB-133 A: Einfügungen E1–E9`, pushen (mit den Belegen aus 0a und 0b, den zwei Skripten und `einfuegungen.txt`).

## Schritt C — Nachweis

C1. `einfuegungen.txt`. Soll: E1–E9 je Anker vorher 1, ausgeführt, Text nachher 1.

C2. `git diff --numstat ⟨S0⟩ HEAD` je Datei ⇒ `docs/belege/TB-133/c2_numstat.txt`. Soll: `ARBEITSWEISE.md` `16	0` (1 + 1 + 1 + 3 + 3 + 1 + 6); `UMZUG.md` `2	0` (ein Absatz, eine Leerzeile); `BACKLOG.md` `10	0` (neun Zeilen Block, eine Leerzeile). Entfernte Zeilen gibt es nicht. Weicht nur die Zahl der Leerzeilen bei E8 oder E9 ab, gilt C3; die Abweichung steht im Ergebnis.

C3. Zeichengleichheit: `docs/belege/TB-133/c3_vergleich.py` liest je Einfügung den Text aus diesem Auftrag und prüft, dass er in der Zieldatei genau einmal als zusammenhängender Block vorkommt (Bytevergleich) ⇒ `c3_vergleich.txt`.

Commit `TB-133 C: Nachweis`, pushen.

## Schritt D — Abgabe

D1. `docs/ERGEBNIS_TB-133_regelwerk_nachtrag_umzug_sitzung_bruecke.md`: Kopf, Kurz-Tabelle (0a, 0b, E1–E9, C1, C2, C3), „Abweichungen und Lesarten“, „Nicht getan“ und „In einfacher Sprache“. Unter „Nicht getan“: die Ablage von `ARBEITSWEISE.md`, `UMZUG.md` und `BACKLOG.md` (macht der steuernde Chat, `BACKLOG.md` erst nach der 27.4-Prüfung); der Fliesstext in `ARBEITSWEISE.md` 6b und 10 und die git-Liste in `UMZUG.md` Abschnitt 6 (letzte Zeile von E9); dazu, was ERGEBNIS_TB-131 unter „Nicht getan“ als unverändert offen führt.

D2. Journalblock nach dem letzten Buchstabenblock von `JOURNAL.md`, vor `## Wiederkehrende Lehren`; Kennung messen (erwartet **EF**), mit Quellenzeile. Verankern wie in TB-131 (`\n---\n\n## Wiederkehrende Lehren\n`).

D3. Abgabe-Commit `TB-133 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Danach `git status --porcelain` in den Scratch und als `docs/belege/TB-133/d3_porcelain.txt`, kleiner letzter Commit, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab.
- Eine Datei ausserhalb der Zieldateien, Belege, Ergebnis und Journal müsste geändert werden.
- `git push` scheitert zweimal.

Bei Abbruch: committen, was an Belegen da ist, Grund in `docs/belege/TB-133/abbruch.txt`, pushen, melden.

## In einfacher Sprache

Seit dem 4. Oktober sind in der Zusammenarbeit neue Regeln entstanden, die bisher nur in der Übergabe stehen. Zwei davon hat der Betreiber selbst verlangt: Der steuernde Chat zieht nur um, wenn der Betreiber es sagt oder genehmigt, und er legt die Sitzung auf dem Mac selbst an. Dieser Auftrag schreibt diese und vierzehn weitere Zeilen an die richtigen Stellen der Arbeitsregeln, einen Absatz in die Umzugsanleitung und einen Block in die Aufgabenliste. Am Code, am Register und an den Werkzeugen ändert er nichts.
