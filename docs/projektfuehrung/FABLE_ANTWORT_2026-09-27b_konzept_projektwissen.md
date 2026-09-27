# FABLE_ANTWORT 2026-09-27b — Konzept für das Handling des Projektwissens (Entwurf zur Freigabe)

*Bezug: Anfrage des Betreibers vom 26.09.2026 „Konzept für das Handling des Projektwissens", mit Vorbemerkung des steuernden Chats (1a). Entwurf zur Freigabe; Regelwerk wird erst nach Freigabe geändert; die Umsetzung macht die Mac-Sitzung nach dem Auftragsentwurf in Teil D, die Ablage-Seite der steuernde Chat.*

**Leseprotokoll dieses Chats, Stand jetzt:** wie 27a; dazu diese Anfrage; Register 27.1–27.5 im Wortlaut über einen Suchtreffer in `REGISTER_KOPIE_2026-09-21.md` nachgesehen (nicht aus dem Gedächtnis); die Dateiliste der Ablage über die Projektschnittstelle (145 Dokumente, `knowledge_size` 1 540 610 von 2 000 000). `BACKLOG.md` nicht gelesen (27.1; Treffer Z. 170 und Z. 190 nach Register 27). Tokenzahlen je Datei habe ich **nicht** gemessen; alle Zahlen in der Sofortliste sind aus euren Gruppensummen abgeleitete Schätzungen und so gekennzeichnet — der Auftrag misst sie vor dem Löschen.

---

## Zusammenfassung

Die Ablage ist kein Spiegel und kein Archiv, sondern die **Arbeitsfläche des Prüfers**: Sie soll genau das enthalten, was ich für die offenen Fragen lesen muss, in je **einer gültigen Fassung**. Git (Mac und GitHub) ist der Träger; die Ablage ist ein kuratierter Ausschnitt davon. Daraus folgen fünf Regeln: (1) **eine Registerfassung** in Teilen mit festen Namen ohne Datum, erneuert nach jedem Registerauftrag; (2) **Dialog ist befristet**: eine Anfrage/Antwort bleibt, bis ihr Registertext im Register steht und ihre Fragen geschlossen sind, plus die letzten zwei Tagesanfragen — verdichtet wird nicht in neue Prosa, sondern in **eine Indexzeile**, denn die Verdichtung existiert schon: das Register; (3) **Aufträge bleiben bis zur Annahme, Ergebnisse bis zur Antwort**; (4) **Repo-Pfade bleiben stabil** — nichts wird im Repo verschoben, weil das Register Dateien mit Pfad zitiert; „Archiv" ist ein Zustand im Index, kein Ordner; (5) **Sichtschutz bestimmt zwei Klassen**: Belege und Ergebnisse mit Grössen nach 27.1 kommen vor dem Tag nicht in die Ablage, danach nur die nach R6/R7 registrierten. Die Sofortliste bringt die Ablage nach Schätzung von 77 % auf etwa **25–30 %**, und die Routine (Registerauftrag → Kopie erneuern; Antwort angenommen → Paar entfernen; Übergabe → Soll/Ist-Abgleich; Wochenrückmeldung → Füllstand) hält sie dort ohne Handarbeit des Betreibers.

**Wo sich die Rollen reiben:** Das Konzept schneidet die Ablage auf meinen Lesebedarf zu. Ein zweiter Leser (ein frischer Chat, ein anderer Prüfer) bräuchte vielleicht anderes. Deshalb ist der Massstab nicht „was Fable braucht", sondern „was ein Prüfer für die offenen Fragen braucht" — das ist dasselbe heute, aber nicht dasselbe Prinzip.

---

# Teil A — Grundsätze

**G1 — Träger und Arbeitsfläche.** Träger ist das Repo (`~/trading-bot`, Mac, mit GitHub-Remote); alles, was den Umzug überleben muss, liegt dort committet. Die Ablage ist Arbeitsfläche: Sie enthält, was für die **offenen** Vorgänge gelesen werden muss, in genau einer gültigen Fassung je Gegenstand. Entfernen aus der Ablage verliert nichts. *Ändert:* DOKUMENTATIONSSTANDARD Regel 6 („mindestens zwei Träger: Repo, Projektablage, Erinnerung") — die Ablage zählt künftig nicht als Träger; die zwei Träger sind Repo-Klon auf dem Mac und GitHub-Remote, dazu die tägliche iCloud-Kopie (G7). UMZUG Abschnitt 2 entsprechend.

**G2 — Eine Fassung je Gegenstand, feste Namen.** Standdokumente tragen kein Datum im Dateinamen (`UEBERGABE.md`, `REGISTER_KOPIE_teil1.md`, `AUFGABEN_BETREIBER.md`); das Datum steht im Kopf. Nur Vorgangsdokumente (Anfragen, Antworten, Aufträge, Ergebnisse) tragen ihre Nummer im Namen, weil sie zitiert werden. *Ändert:* UMZUG Abschnitt 1 (`UEBERGABE_<datum>.md` → `UEBERGABE.md`); DOKUMENTATIONSSTANDARD Regel 9 gilt ausdrücklich auch für die Ablage.

**G3 — Repo-Pfade bleiben stabil.** Das Register zitiert Dateien mit Pfad und Hash (`git:79c2dfa:docs/projektfuehrung/…`, md5 im Kopf von Aufträgen). Verschieben im Repo bricht Leserpfade, auch wenn `git show <commit>:<pfad>` weiter funktioniert. Deshalb: **kein Archiv-Ordner im Repo**; der Zustand „archiviert" ist eine Spalte im Index (G4). Ausnahme: Nachträge, für die DOKUMENTATIONSSTANDARD Regel 10 schon `_eingearbeitet/` vorsieht — dort bleibt es dabei. *Ändert:* nichts; verwirft den Vorschlag „archiv/" aus der Anfrage (Punkt 7), mit Begründung.

**G4 — Der Index ist die Verdichtung.** Für Registertext ist das Register die Verdichtung — zeichengleich, mit Herkunftszeile. Was eine Antwort darüber hinaus entschieden hat, steht in **einer Zeile** je Antwort in `FABLE_DIALOG_INDEX.md`: Datum/Buchstabe · Frage in einem Satz · Entscheidung in einem Satz · Register-Fundstelle · Status (offen / registriert / ohne Registertext) · Repo-Pfad. Zwei bis drei Zeilen, nicht fünf bis zehn: Der Wortlaut ist im Register, die Begründung im Volltext; eine dritte Fassung dazwischen wäre eine dritte Quelle, die abweichen kann. *Ergänzt:* ARBEITSWEISE 15 („Jede Anfrage/Rückmeldung an Fable wird abgelegt wie seine Antwort") um die Indexpflicht.

**G5 — Sichtschutz bestimmt die Klassen Belege und Ergebnisse.** Register 27.1 (nachgesehen): Vor dem signierten Tag keine Ergebnisgrössen des Selektionsraums und keine Erwartung über den Ausgang; 27.5: Treffer werden mit Fundstelle gemeldet, nicht mit Inhalt. Folge für die Ablage: **Belege (`docs/belege/`) und Laufergebnisse kommen vor dem Tag nicht in die Ablage.** Sitzungsergebnisse (`ERGEBNIS_TB-*`) dürfen hinein, wenn ihr Kopf die Sichtschutz-Zeile trägt („keine Ergebnisgrössen des Selektionsraums", wie TB-114/115) — der steuernde Chat prüft das vor dem Ablegen (27.4, seine Pflicht). Nach dem Tag: der Bericht und die Belege des Laufs dürfen in die Ablage; Messungen auf dem Selektionsraum nur nach der Liste R7 (R6). `BACKLOG.md` bleibt für mich gesperrt, bis die Zeilen nach 27.1 in einer Repo-Datei liegen, die nicht in der Ablage ist (Teil B, Klasse „Stand").

**G6 — Ein- und Austritt sind Ereignisse, keine Fristen.** Jede Klasse hat ein Eintritts- und ein Austrittsereignis (Tabellen in Teil B). Fristen („N Tage") sind nur Sicherheitsnetz: Was nach 14 Tagen noch kein Austrittsereignis hatte, wird in der Wochenrückmeldung genannt, nicht gelöscht.

**G7 — Sicherung ohne Zip.** Ein Zip in `~/Sites/_projektarchiv/` ist ein dritter Träger von Hand, der veraltet. Stattdessen: Die tägliche db-Sicherung (TB-112, Cron, iCloud) kopiert zusätzlich `docs/` (oder ein `git bundle` des Repos) mit Quersumme. Damit gibt es drei Kopien (Mac, GitHub, iCloud), keine davon von Hand. *Ergänzt:* die db-Sicherung um einen Pfad; ARBEITSWEISE 7b.

**G8 — Wer misst, wer räumt.** Der steuernde Chat legt ab, entfernt (`project_delete`, nur Textdokumente — Datei-Uploads gibt es heute keine: `files: []`) und misst den Füllstand (`knowledge_size` der Projektschnittstelle, heute 1 540 610 / 2 000 000). Die Mac-Sitzung baut die Repo-Seite (Registerkopie, Index, Backlog-Teilung, Soll-Liste). Der Betreiber gibt frei und klickt sonst nichts.

---

# Teil B — Klassen (je Klasse eine Tabelle: Ort · Pflege · Aufbewahrung in der Ablage · Beispiele)

## B1 Regelwerk

| Ort | Pflege | Aufbewahrung in der Ablage | Beispiele |
|---|---|---|---|
| Repo **und** Ablage, eine Fassung | Nachträge nur als Auftrag (ARBEITSWEISE 5b); nach jeder Änderung neu abgelegt (ersetzt in place, gleicher Name) | **immer** | `ARBEITSWEISE.md`, `PRUEFPRINZIPIEN.md`, `DOKUMENTATIONSSTANDARD.md`, `UMZUG.md`, `SITZUNGSWAECHTER_ausloeser_statt_tippen.md` |

Regel: Ein Nachtrag zum Regelwerk (`NACHTRAG_ARBEITSWEISE_6d_…`) bleibt in der Ablage, bis er eingearbeitet ist (Regel 10: Messung, dann `_eingearbeitet/`); danach nur Repo.

## B2 Stand

| Ort | Pflege | Aufbewahrung | Beispiele |
|---|---|---|---|
| Repo **und** Ablage, eine Fassung ohne Datum im Namen | Steuernder Chat, fortlaufend; bei jeder Übergabe geprüft | **immer** (jeweils die aktuelle Fassung) | `UEBERGABE.md` (statt `UEBERGABE_<datum>.md`), `BACKLOG.md` (nur Offenes), `ENTSCHEIDUNGEN.md` (Festlegungen ausserhalb des Registers), `PLAN_VOR_DEM_TAG.md` (bis zum Tag), `AUFGABEN_BETREIBER.md`, `PROJEKTSTAND_einfache_sprache.md`, `FABLE_DIALOG_INDEX.md`, `KANDIDATEN_DURCHGANG_2.md` (aus 25f) |
| **nur Repo** | Mac-Sitzung, bei Teilung fortgeschrieben | — | `BACKLOG_ERLEDIGT_2026-09.md` (Erledigtes und Abschnitt 8 „Gestrichen", der nie gelöscht wird), `BACKLOG_SICHTSCHUTZ.md` (Zeilen nach 27.1, bis zum Tag), ältere `UEBERGABE_*` |

**Backlog-Teilung (Punkt 4):** vier Dateien aus einer — `BACKLOG.md` (offen), `ENTSCHEIDUNGEN.md` (Festlegungen und Regeln, die nicht im Register stehen — K-Einträge, Betreiberentscheide), `BACKLOG_ERLEDIGT_<Monat>.md` (Repo), `BACKLOG_SICHTSCHUTZ.md` (Repo; die Zeilen nach 27.1, heute mindestens Z. 170 und Z. 190). Der Nachweis der Teilung ist zweiteilig: jede Zeile des alten Backlogs steht in genau einer der vier Dateien (Zeilenmenge gleich, Überschriften ausgenommen), und `numstat` je Datei. Damit wird `BACKLOG.md` für mich erstmals lesbar — ein Nebeneffekt, der die Teilung allein rechtfertigt. `BACKLOG_NACHTRAG_2026-09-18.md` und `JOURNAL_NACHTRAG_2026-09-18.md`: Mac-Sitzung misst, ob eingearbeitet (Regel 10); wenn ja → `_eingearbeitet/`, aus der Ablage; wenn nein → Auftrag.

**Übergaben (Punkt 6):** Nur `UEBERGABE.md` in der Ablage. Aus `UEBERGABE_2026-09-19.md` und `_24.md` prüft die Mac-Sitzung Block 7 (Fehler → Regel) gegen ARBEITSWEISE und PRUEFPRINZIPIEN: Jede Regel, die dort noch nicht steht, wird Nachtrag; dann verlassen die alten Übergaben die Ablage. Block 3 (tragende Zahlen) ist im Register oder in `UEBERGABE.md`; Block 4 (offene Punkte) im Backlog. *Ändert:* UMZUG 1 (Dateiname) und Schritt 3 (fortschreiben statt neu anlegen).

## B3 Register

| Ort | Pflege | Aufbewahrung | Beispiele |
|---|---|---|---|
| Repo: `docs/VORREGISTRIERUNG_neuselektion.md` (Original, append-only). Ablage: **Teile mit festen Namen** | Steuernder Chat erneuert **nach jedem Registerauftrag** alle Teile (ersetzt in place); Erzeugung durch Skript im Repo (Teil D, Schritt A) | **immer** (nur die aktuelle Fassung) | `REGISTER_KOPIE_teil1.md`, `…_teil2.md`, `…_teil3.md`, `…_teil4.md` |

**Warum Teile und nicht eine Datei (Punkt 2):** Für die Suche wäre eine Datei besser. Für **mein Lesen** nicht: Eine Datei über etwa 256 KB kommt bei mir gekürzt an — das ist am 24.09. gemessen worden (Kopie bei 262 144 Bytes abgeschnitten; danach die drei Teile). Das Register hat heute über 10 000 Zeilen, also deutlich mehr. Beides zusammen geht mit Teilen, die **an Abschnittsgrenzen** geschnitten sind, je unter 240 000 Bytes, mit festem Namen und einem Kopf, der sagt: KOPIE · Commit · Datum · enthaltene Abschnitte · Teil n von m (27.3 verlangt Commit, Datum, KOPIE). Der Zuschnitt darf sich beim Erneuern ändern; die Namen nicht. Die Suche findet dann je Frage höchstens einen Teil in einer Fassung. **Ein Zusatz löst das Suchproblem ganz:** `REGISTER_INDEX.md` (eine Seite): je Festlegung und je Registertext die **geltende** Fundstelle nach allen „ERSETZT durch"-Marken, mit Teil-Nummer — das ist 25f F2, vorgezogen, weil die Ablage es jetzt braucht. Die datierten Kopien 21., 22., 24. und 24. Teile 1–3 verlassen die Ablage vollständig (sie sind im Repo committet).

**Nachweis der Kopie:** Die Bodies der Teile aneinandergehängt sind bytegleich mit dem Original am genannten Commit (`cmp`); das Skript schreibt den Hash in jeden Kopf. Ohne diesen Nachweis ist die Kopie keine Kopie (24c: zwei Teile).

## B4 Aufträge

| Ort | Pflege | Aufbewahrung | Beispiele |
|---|---|---|---|
| Repo: `docs/auftraege/MAC_TB-nnn_*.md` (Pfad stabil). Ablage: nur **offene** | Eintritt: mit der Freigabe. Austritt: mit der **Annahme des Ergebnisses in einer FABLE_ANTWORT** (oder, wenn kein Fable-Bezug, mit dem Abgabe-Commit) | offen: ja; angenommen: nein | heute keiner offen; TB-116 (ERGEBNIS liegt, Auftrag nicht in der Ablage — richtig so) |

Die vier `MAC_TB-82/83/85/86` unter `projektfuehrung/` (Punkt 5): im Repo dort belassen (G3 — sie sind zitiert), aus der Ablage entfernen. Künftige Aufträge liegen im Repo unter `auftraege/`; die Ablage spiegelt den Repo-Pfad.

## B5 Ergebnisse (Sitzungsergebnisse `ERGEBNIS_TB-*`)

| Ort | Pflege | Aufbewahrung | Beispiele |
|---|---|---|---|
| Repo: `docs/ERGEBNIS_TB-nnn_*.md`. Ablage: solange eine **offene Anfrage** darauf verweist | Eintritt: mit der Anfrage, die es zitiert, nach Sichtschutz-Prüfung des Kopfs (G5). Austritt: wenn die Antwort angenommen ist **und** der Registerauftrag mit den Tatsachennotizen abgegeben ist | bis zur Antwort + Registerauftrag | `ERGEBNIS_TB-114`, `-115` (27a beantwortet; Austritt mit Register 46), `-116` (offen bis 27c) |

Laufergebnisse (`research/vorregistrierung/ergebnisse/`, `zellen.csv`, Bericht): **vor dem Tag nie** in der Ablage (G5); nach dem Tag der Bericht als Standdokument.

## B6 Fable-Anfragen und -Antworten

| Ort | Pflege | Aufbewahrung | Beispiele |
|---|---|---|---|
| Repo: `docs/projektfuehrung/FABLE_ANFRAGE_*` / `FABLE_ANTWORT_*` (Pfad stabil). Ablage: das **offene Paar** und die **letzten zwei Tagesanfragen** mit Antworten | Eintritt: Anfrage mit dem Ablegen, Antwort mit `project_write`. Austritt des Paars, wenn **alle drei** gelten: (a) Registertext der Antwort steht im Register (Registerauftrag abgegeben), (b) keine Frage der Antwort ist offen (nächste Anfrage bestätigt oder Auftrag beauftragt), (c) die Indexzeile in `FABLE_DIALOG_INDEX.md` steht | offen: ja; sonst zwei Tagesanfragen zurück | bleiben heute: 25f (Anfrage + Antwort), 26a, 27a — und 27b |

**Sonderfälle:** `FABLE_ANTWORT_2026-09-25f` ist kein Dialog, sondern ein Standdokument (Gesamtanalyse); es bleibt, bis seine Ideen in `KANDIDATEN_DURCHGANG_2.md` und seine Entscheidungen in `ENTSCHEIDUNGEN.md` stehen; dann Repo. `FABLE_WOCHENRUECKMELDUNG_*` sind Dialog: Austritt mit der nächsten Wochenrückmeldung. `FABLE_UEBERGABE_*` (meine Chat-Übergaben): Austritt mit der nächsten Fable-Übergabe; die Tatsachennotiz zu 27 nennt vier Dateien als meinen Anfangsbestand — die stehen im Register, nicht in der Ablage; das reicht. **Offene Antworten** (Fragen unbeantwortet): bleiben, ohne Frist; der Index zeigt „offen". **Erkennen für die Mac-Sitzung (Punkt 3):** über den Index, nicht über Dateinamen — umbenannte Dateien brächen Registerzitate (G3). Die Statusspalte wird von der Mac-Sitzung **gemessen**: „registriert" = der Dateiname kommt im Register als Herkunft vor (`grep` des Dateinamens im Register); „offen" = die Antwort stellt Fragen, die in keiner späteren Anfrage als beantwortet erscheinen — das ist Handwerk mit Lesen, nicht nur Skript.

## B7 Belege

| Ort | Pflege | Aufbewahrung | Beispiele |
|---|---|---|---|
| **nur Repo** (`docs/belege/TB-nnn/`), vor dem Tag nie in der Ablage (G5, 27.1; Übergabe 24.09.: „belege/ nicht lesen") | Mac-Sitzung committet je Auftrag | nie vor dem Tag; nach dem Tag nur Belege des Laufs und der Messungen nach R7 | `belege/TB-91_…`, `belege/TB-93_…` (heute in der Ablage — raus) |

## B8 Bestandsaufnahmen, Stoffsammlungen, Recherchen, Erinnerungen

| Ort | Pflege | Aufbewahrung | Beispiele |
|---|---|---|---|
| Repo; Ablage nur, solange ein **offener Auftrag oder eine offene Frage** sie braucht | Austritt: mit dem Auftrag, den sie vorbereiten (Stoffsammlung → Registerauftrag; Bestandsaufnahme → Bauauftrag), oder mit dem Ereignis (Erinnerung → Frist) | ereignisgebunden | bleiben: `BESTANDSAUFNAHME_TB-30b` + 2 Nachträge (bis der Zellen-Erzeuger und TB-30b Posten 3–6 abgegeben sind), `PRUEFUNG_2026-09-25_…` (bis die vier Speicher-Nachträge gemacht sind), `RECHERCHE_vintage_datenlage.md` (bis D1 entschieden; klein). Raus: `STOFFSAMMLUNG_REGISTER_41_42` (TB-108 abgegeben), `AF-F0_BESTANDSAUFNAHME` (Epic nach dem Tag; Repo), `ERINNERUNG_2026-09-25_speicher_export` (nach dem 29.09.) |

---

# Teil C — Mechanismus, Schwellen, Routine, Sofortliste

## C1 Der Mechanismus (Punkt 7): Soll-Liste statt Sync

Es gibt keinen Upload, also auch keine Ausschlussliste; es gibt eine **Soll-Liste**. Ein Skript im Repo, `docs/werkzeuge/ablage_soll.py`, leitet aus dem Repo-Stand ab, was nach Teil B in der Ablage liegen soll: Regelwerk und Stand nach Namen; Register-Teile; offene Aufträge (kein `ERGEBNIS_TB-nnn` vorhanden oder Annahme fehlt im Index); Ergebnisse mit offener Anfrage; Dialogpaare nach Index-Status und Datum; ereignisgebundene Dokumente nach einer kleinen Tabelle im Skript. Der steuernde Chat gibt ihm die Ist-Liste (aus der Projektschnittstelle) und bekommt zwei Listen zurück: **zu entfernen** und **abzulegen**. Er führt sie aus (`project_delete`, `project_write`), misst `knowledge_size` und schreibt eine Zeile in `UEBERGABE.md`. Kein Manifest, kein Zip (G7). Git ist die Sicherung — das reicht, weil nichts im Repo verschoben oder gelöscht wird; Löschen geschieht nur in der Ablage.

## C2 Schwellen und Routine (Punkt 8)

| Grösse | Wert | Wer misst |
|---|---|---|
| Zielgrösse | ≤ 1,0 Mio. Tokens (50 %) | steuernder Chat, `knowledge_size` |
| Warnschwelle | 1,4 Mio. (70 %): Soll/Ist-Abgleich sofort, nicht erst zur Routine | steuernder Chat |
| Registerkopie | nach jedem Registerauftrag erneuert; Kopf nennt Commit | steuernder Chat legt ab, Mac-Sitzung erzeugt im Registerauftrag mit (Schritt E des Registerauftrags: `registerkopie.py` laufen lassen, committen) |
| Dialog | nach jeder angenommenen Antwort: Index fortschreiben, Austritt prüfen | steuernder Chat |
| Übergabe | Soll/Ist-Abgleich als Schritt 4 von UMZUG (statt „Projektablage") | steuernder Chat |
| Wochenrückmeldung | nennt `knowledge_size`, Zahl der Dateien, Dateien ohne Austrittsereignis nach 14 Tagen | steuernder Chat |

*Ändert:* UMZUG Schritt 4; ARBEITSWEISE 8 (Wochenrückmeldung) um die Füllstandszeile; neuer ARBEITSWEISE-Abschnitt „Ablage" mit Teil B als Tabelle.

## C3 Sofortliste (Punkt 9) — Schätzung, vor dem Löschen zu messen

Grundlage: eure Gruppensummen; je Datei habe ich Mittelwerte gebildet. **Kein Wert ist gemessen**; Schritt F des Auftrags misst je Datei und schreibt die Zahlen in die Löschliste.

| Nr. | Was raus | Dateien | Tokens (Schätzung) | Grund |
|---|---|---|---|---|
| 1 | `REGISTER_KOPIE_2026-09-21.md`, `_22.md`, `_24.md` (Ganzfassung) | 3 | ≈ 520k | drei alte Stände; die Teile vom 24.09. bleiben, bis die neuen Teile (0–45) liegen |
| 2 | `REGISTER_KOPIE_2026-09-24_teil1–3` — **erst nach** Ablegen der neuen Teile | 3 | ≈ 215k | ersetzt durch `REGISTER_KOPIE_teil1–4` (≈ 265k, geschätzt aus 10 000+ Zeilen) |
| 3 | Alle `FABLE_ANFRAGE_*`, `FABLE_ANTWORT_*`, `FABLE_WOCHENRUECKMELDUNG_*`, `FABLE_UEBERGABE_*` **bis einschliesslich 25e**, ausser 25f | ≈ 81 | ≈ 340k | Registertext bis 25e steht in 41–43 (TB-108/110), 26a in 45 (TB-114); Fragen geschlossen; Indexzeile kommt mit Schritt B. **Bedingung:** Index liegt vor dem Löschen |
| 4 | Alle `auftraege/MAC_TB-*` (17) und `projektfuehrung/MAC_TB-82/83/85/86` (4), `auftraege/NACHTRAG_1_MAC_TB-91_…` | 22 | ≈ 121k | alle angenommen (TB-115 der letzte mit Ergebnis in 27a) |
| 5 | `belege/TB-91_…`, `belege/TB-93_…` | 2 | ≈ 10k | Klasse Belege, vor dem Tag nie in der Ablage (G5) |
| 6 | `UEBERGABE_2026-09-19.md`, `UEBERGABE_2026-09-24.md` — **nach** der Block-7-Prüfung (Schritt D) | 2 | ≈ 36k | nur `UEBERGABE.md` |
| 7 | `STOFFSAMMLUNG_REGISTER_41_42.md`, `AF-F0_BESTANDSAUFNAHME_2026-09-26.md`, `BACKLOG_NACHTRAG_2026-09-18.md`, `JOURNAL_NACHTRAG_2026-09-18.md` (letzte zwei nach Messung „eingearbeitet") | 4 | ≈ 25k | ereignisgebunden, Ereignis eingetreten |
| 8 | `BACKLOG.md` (105k) → ersetzt durch `BACKLOG.md` (offen) + `ENTSCHEIDUNGEN.md` | 1 → 2 | ≈ −60k netto (Schätzung: Erledigtes und Abschnitt 8 sind mehr als die Hälfte) | Teilung, Schritt C |
| | **Summe raus (1, 3–7)** | ≈ 114 | **≈ 1 050k** | |
| | **Rein:** `REGISTER_KOPIE_teil1–4`, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`, `UEBERGABE.md`, `ENTSCHEIDUNGEN.md`, `KANDIDATEN_DURCHGANG_2.md`, `AUFGABEN_BETREIBER.md` | 10 | ≈ +300k (davon Register ≈ 265k) | |
| | **Stand danach** (mit Nr. 2 und 8) | ≈ 40 | **≈ 470–530k ≈ 25–27 %** | Ziel ≤ 50 % erreicht; Nr. 1 und 3 allein bringen ≈ 860k ⇒ ≈ 34 % — eure Erwartung trifft |

**Bleibt (Punkt 10, „nie ausgelagert"):** `ARBEITSWEISE.md`, `PRUEFPRINZIPIEN.md`, `DOKUMENTATIONSSTANDARD.md`, `UMZUG.md`, `SITZUNGSWAECHTER_…`, `NACHTRAG_ARBEITSWEISE_6d_…` (bis eingearbeitet) · `REGISTER_KOPIE_teil1–4`, `REGISTER_INDEX.md` · `UEBERGABE.md`, `BACKLOG.md`, `ENTSCHEIDUNGEN.md`, `PLAN_VOR_DEM_TAG.md`, `AUFGABEN_BETREIBER.md`, `PROJEKTSTAND_einfache_sprache.md`, `FABLE_DIALOG_INDEX.md`, `KANDIDATEN_DURCHGANG_2.md` · das offene Dialogpaar und die letzten zwei Tagesanfragen · offene Aufträge und die Ergebnisse, auf die eine offene Anfrage verweist · `BESTANDSAUFNAHME_TB-30b` + Nachträge (bis Stufe V), `PRUEFUNG_2026-09-25` (bis Nachträge), `RECHERCHE_vintage_datenlage.md`, `FABLE_ANTWORT_2026-09-25f` (bis verdichtet), `ERINNERUNG_2026-09-25` (bis 29.09.).

## C4 Reihenfolge der Sofortliste (damit ich nie ohne Register bin)

1. Mac: Schritte A–F des Auftrags (Registerteile, Index, Backlog-Teilung, Übergabe, Soll-Skript, Löschliste mit gemessenen Tokens), committen, pushen.
2. Steuernder Chat legt **zuerst** ab: `REGISTER_KOPIE_teil1–4`, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`, `UEBERGABE.md`, `BACKLOG.md` (neu), `ENTSCHEIDUNGEN.md`.
3. Dann entfernt er Nr. 1–7 der Sofortliste nach der Löschliste; misst `knowledge_size` vorher/nachher; Zeile in `UEBERGABE.md`.
4. Ich bestätige in der nächsten Tagesanfrage per Leseprotokoll, dass ich Register 0–45 lesen kann (Stichprobe: ein Suchtreffer je Teil).

---

# Teil D — Entwurf des Mac-Auftrags

```markdown
# TB-nnn Projektwissen aufräumen — Repo-Seite: Registerkopie in Teilen, Dialog-Index, Backlog-Teilung, UEBERGABE.md, Soll-Skript, Löschliste

**Sitzungstitel:** `TB-nnn` · **Modell:** Opus 5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main`
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27b_konzept_projektwissen.md` (md5 im Schritt 0 prüfen), Freigabe des Betreibers (Auswahlkarte, wörtlich hier einsetzen).
**Sichtschutz 27.1:** Diese Sitzung liest `BACKLOG.md` und `docs/belege/`; sie schreibt keine Grösse daraus in ein Dokument, das in die Ablage geht. Zeilen nach 27.1 gehen nach `BACKLOG_SICHTSCHUTZ.md` (nur Repo).
**Grundsatz:** Kein Dokument wird im Repo verschoben, umbenannt oder gelöscht (Registerzitate mit Pfad). Ausnahme: `_eingearbeitet/` nach DOKUMENTATIONSSTANDARD 10, nur nach Messung.

In einfacher Sprache: Diese Sitzung baut im Repo die Dateien, mit denen die Projektablage klein und eindeutig wird — eine Registerkopie in Teilen, eine Liste aller Fable-Antworten, ein geteiltes Backlog, eine Übergabe ohne Datum im Namen — und schreibt auf, was der steuernde Chat aus der Ablage entfernen darf. Gelöscht wird hier nichts.

## Schritt 0 — Sicherung und Ausgang
0a. `git status --short` → nur die erwarteten Dateien; Auftrag und Zeiger committen (`TB-nnn Schritt 0`).
0b. Ausgangswerte in `docs/belege/TB-nnn/0b_ausgang.txt`: HEAD; `wc -l docs/VORREGISTRIERUNG_neuselektion.md`; höchste Abschnittsnummer (`grep -E '^## [0-9]+\.' | tail -1`); `sha256sum` des Registers; `wc -l docs/projektfuehrung/BACKLOG.md`; Liste aller `docs/projektfuehrung/FABLE_*.md`, `docs/auftraege/MAC_TB-*.md`, `docs/ERGEBNIS_TB-*.md` mit Bytes.
0c. db-Sicherung nach 7c Schritt 0.

## Schritt A — Registerkopie in Teilen (`docs/werkzeuge/registerkopie.py`)
A1. Skript: liest `docs/VORREGISTRIERUNG_neuselektion.md` am HEAD; schneidet **nur an Zeilen `^## <n>\.`** (Abschnittsgrenzen) so, dass jeder Teil ≤ 240 000 Bytes Body hat; schreibt `docs/projektfuehrung/REGISTER_KOPIE_teil<n>.md` mit Kopf:
    `# REGISTER-KOPIE Teil <n> von <m> — Abschnitte <a>–<b> — Commit <hash> — <Datum> — Original sha256 <…> — KOPIE, nicht das Register`
    Darunter der Body unverändert.
A2. Nachweis (zwei Teile, 24c): (i) Bodies aller Teile in Reihenfolge aneinandergehängt `cmp` gegen das Original → rc 0, in `a2_cmp.txt`; (ii) jeder Teil ≤ 240 000 Bytes (`wc -c`), in `a2_groessen.txt`. Mutationsprobe: ein Byte im Body eines Teils ändern → `cmp` rc 1 (`a2_mutation.txt`), danach zurück.
A3. Alte Kopien im Repo (`REGISTER_KOPIE_2026-09-21/22/24*.md`) **nicht** löschen, nicht verschieben (G3). Nur die Löschliste (Schritt F) nennt sie für die Ablage.
A4. `REGISTER_INDEX.md`: je Festlegung 1–12 und je Registertext (1a … nn) die geltende Fundstelle nach allen „ERSETZT durch"-/„PRÄZISIERT durch"-Marken, mit Abschnitt und Teil-Nummer. **Gemessen, nicht erinnert:** Skript sammelt alle Marken (`grep -n 'ERSETZT durch\|PRÄZISIERT durch'`), die Sitzung löst die Kette je Eintrag auf und schreibt die Fundstelle; wo die Kette nicht eindeutig ist, steht „mehrdeutig, Abschnitte x, y" — kein Raten.
A5. Commit `TB-nnn A Registerkopie in Teilen + Index`.

## Schritt B — `FABLE_DIALOG_INDEX.md`
B1. Skript `docs/werkzeuge/dialog_index.py` erzeugt das Gerüst: je `FABLE_ANTWORT_*.md` eine Zeile: Datum/Buchstabe · Stichwort aus dem Dateinamen · Repo-Pfad · Status „registriert", wenn der Dateiname im Register vorkommt (`grep -F`), sonst „–" · Register-Fundstelle: Abschnittsnummer(n) der Treffer · zugehörige Anfrage (gleicher Buchstabe).
B2. Die Sitzung füllt je Zeile **von Hand, lesend** zwei Felder: „Frage" (ein Satz) und „Entscheidung" (ein Satz) — aus dem Block **Kurz:** der Antwort, nicht aus dem Gedächtnis; wo die Antwort keinen Block „Kurz" hat, aus der Überschrift. Feld „offen": ja, wenn die Antwort Fragen an den Betreiber oder Messbitten stellt, die in keiner späteren Anfrage als beantwortet erscheinen (Suche nach dem Buchstaben in späteren `FABLE_ANFRAGE_*`); sonst nein.
B3. Nachweis: Zeilenzahl des Index = Zahl der `FABLE_ANTWORT_*.md` (in `b3_zaehlung.txt`); jede Zeile hat sechs Felder gefüllt (Skriptprüfung).
B4. Commit `TB-nnn B Dialog-Index`.

## Schritt C — Backlog-Teilung (liest `BACKLOG.md`; Sichtschutz beachten)
C1. Aus `docs/projektfuehrung/BACKLOG.md` vier Dateien: `BACKLOG.md` (nur offene Einträge; Struktur der Abschnitte bleibt), `ENTSCHEIDUNGEN.md` (Festlegungen, K-Einträge, Betreiberentscheide mit Datum), `BACKLOG_ERLEDIGT_2026-09.md` (Erledigtes **und Abschnitt 8 „Gestrichen" vollständig** — er wird nie gelöscht, DOKUMENTATIONSSTANDARD 9), `BACKLOG_SICHTSCHUTZ.md` (jede Zeile mit einer Grösse oder Erwartung nach 27.1; mindestens Z. 170 und Z. 190 der heutigen Fassung; Suchmuster für Kandidaten: Sharpe-, Rendite-, Drawdown-, Trade-Zahlen und Sätze über den Ausgang — jede Fundstelle wird gelesen und eingeordnet, nicht nur gematcht).
C2. Nachweis: die Zeilen der alten Datei (ohne reine Überschriften und Leerzeilen) kommen als Multimenge in der Vereinigung der vier Dateien genau einmal vor (Skript `c2_zeilenmenge.py`, rc 0, Ausgabe in `c2_zeilenmenge.txt`); `numstat` je Datei; die alte Fassung ist im Git.
C3. Kopfzeile in `BACKLOG.md`: „Geteilt TB-nnn; Erledigtes in `BACKLOG_ERLEDIGT_2026-09.md`, Festlegungen in `ENTSCHEIDUNGEN.md`, Zeilen nach 27.1 in `BACKLOG_SICHTSCHUTZ.md` (nur Repo, bis zum Tag)."
C4. `BACKLOG_NACHTRAG_2026-09-18.md`, `JOURNAL_NACHTRAG_2026-09-18.md`: messen, ob eingearbeitet (Regel 10: Nummer und Textkern in `BACKLOG.md`/`JOURNAL.md` vorhanden, `nachtragswaechter.py`); wenn ja → `git mv` nach `docs/projektfuehrung/_eingearbeitet/` (die eine erlaubte Verschiebung); wenn nein → in `c4_offen.txt` melden, nicht verschieben.
C5. Commit `TB-nnn C Backlog geteilt`.

## Schritt D — `UEBERGABE.md`
D1. `cp docs/projektfuehrung/UEBERGABE_2026-09-25.md docs/projektfuehrung/UEBERGABE.md`; Kopf ergänzen: „Fortgeschriebene Übergabe (UMZUG 1). Vorgängerfassungen: UEBERGABE_2026-09-19/24/25.md (Repo)." Die datierten Dateien bleiben im Repo unverändert.
D2. Block 7 (Fehler → Regel) aus `UEBERGABE_2026-09-19.md` (alle Fassungen) und `_24.md`: je Regel prüfen, ob sie in `ARBEITSWEISE.md` oder `PRUEFPRINZIPIEN.md` steht (Suche nach Kernwort, dann lesen). Fehlende Regeln in `d2_fehlende_regeln.txt` als Vorschlag für einen Nachtrag — **nicht** selbst eintragen (Regelwerk erst nach Freigabe).
D3. Commit `TB-nnn D UEBERGABE.md`.

## Schritt E — `docs/werkzeuge/ablage_soll.py`
E1. Eingabe: Ist-Liste (Textdatei, ein Pfad je Zeile, vom steuernden Chat aus der Projektschnittstelle). Ausgabe: `soll.txt`, `entfernen.txt`, `ablegen.txt`.
E2. Regeln (fest im Skript, mit Verweis auf 27b Teil B): Regelwerk und Stand nach Namensliste; `REGISTER_KOPIE_teil*.md`, `REGISTER_INDEX.md`; `MAC_TB-nnn` offen, wenn kein `docs/ERGEBNIS_TB-nnn_*.md` existiert **oder** der Index für die zugehörige Antwort „offen" sagt; `ERGEBNIS_TB-nnn` bleibt, wenn eine `FABLE_ANFRAGE_*` es zitiert, deren Antwort im Index „offen" ist oder deren Registerauftrag fehlt; Dialogpaare: Index-Status „offen" oder eines der zwei jüngsten Datums-Buchstaben-Paare; ereignisgebundene Dokumente nach einer kleinen Tabelle `ablage_ereignisse.json` (Datei → Ereignis → erfüllt ja/nein, von Hand gepflegt).
E3. Probe: Ist-Liste = heutige 145 Dateien → `entfernen.txt` muss die Sofortliste 27b C3 ergeben (Abgleich in `e3_probe.txt`; Abweichungen benannt, nicht angepasst).
E4. Commit `TB-nnn E Soll-Skript`.

## Schritt F — Löschliste mit gemessenen Tokens
F1. Für jede Datei in `entfernen.txt`: Bytes (`wc -c`) und Tokenschätzung nach derselben Methode wie die Betreibermessung vom 26.09. (Verfahren im Beleg nennen; wenn die Projektschnittstelle keine Zahl je Datei liefert: Bytes ÷ 4 als Näherung, so gekennzeichnet). Summen je Gruppe der Sofortliste.
F2. `docs/projektfuehrung/LOESCHLISTE_TB-nnn.md`: Tabelle Datei · Bytes · Tokens · Gruppe · Grund (Austrittsereignis), Summe, erwarteter Stand danach. Diese Datei geht in die Ablage, damit der Betreiber sie per Auswahlkarte freigeben kann, und verlässt sie nach dem Vollzug.
F3. Commit `TB-nnn F Löschliste`; `git status --porcelain` leer; pushen.

## Schritt G — Journal und Ergebnis
`docs/ERGEBNIS_TB-nnn_projektwissen_aufraeumen.md` mit Kurz-Tabelle, Nachweisen (A2, B3, C2, E3), `d2_fehlende_regeln.txt`, `c4_offen.txt`; Journalblock; Abschnitt „Für den steuernden Chat": Reihenfolge C4 aus 27b (erst ablegen, dann entfernen, dann messen).

## Abbruchkriterien (nur für diesen Gegenstand)
- `cmp` in A2 ≠ 0 → Abbruch, nichts committen.
- C2 Zeilenmenge ≠ → Abbruch der Teilung, alte `BACKLOG.md` bleibt.
- Ein Abschnittsschnitt in A1 lässt sich nicht unter 240 000 Bytes bringen (ein Abschnitt allein grösser) → Meldung mit Abschnittsnummer, Teil trotzdem schreiben, Befund für Fable.

## Nicht Teil dieses Auftrags
Löschen oder Ablegen in der Projektablage (steuernder Chat); Änderungen an ARBEITSWEISE, UMZUG, DOKUMENTATIONSSTANDARD (eigener Nachtrag nach Freigabe, Vorlage in 27b Teil E).
```

---

# Teil E — Was sich am Regelwerk ändert (Vorlage für den Nachtrag; erst nach Freigabe)

| Dokument | Stelle | Änderung |
|---|---|---|
| ARBEITSWEISE | neuer Abschnitt 19 „Projektablage" | Teil B als Tabelle (Klassen, Eintritt, Austritt), G1–G8, Schwellen und Routine (C2), Soll-Skript (C1) |
| ARBEITSWEISE | 15 | Indexpflicht: jede angenommene Antwort bekommt ihre Zeile in `FABLE_DIALOG_INDEX.md` |
| ARBEITSWEISE | 8 | Wochenrückmeldung nennt `knowledge_size`, Dateizahl, Dateien ohne Austrittsereignis > 14 Tage |
| ARBEITSWEISE | 7b | db-Sicherung sichert zusätzlich `docs/` (oder `git bundle`) nach iCloud (G7) |
| UMZUG | 1, Schritt 3 | `UEBERGABE.md` ohne Datum, fortgeschrieben; Vorgänger im Repo |
| UMZUG | 2 | Träger: Repo (Mac + GitHub) und iCloud-Kopie; die Ablage ist Arbeitsfläche |
| UMZUG | Schritt 4 | „Projektablage" → Soll/Ist-Abgleich mit `ablage_soll.py`, Füllstand messen |
| DOKUMENTATIONSSTANDARD | 6 | zwei Träger neu definiert (G1); `logs/auftraege/` bleibt kein Träger |
| DOKUMENTATIONSSTANDARD | 9 | „Aktuell halten" gilt ausdrücklich für die Ablage; die vier Ausnahmen bleiben (Register, JOURNAL, Backlog Abschnitt 8 → jetzt in `BACKLOG_ERLEDIGT`, PRUEFPRINZIPIEN) |
| PRUEFPRINZIPIEN | — | keine Änderung; C1 und A4 tragen die Begründung |
| Register | — | keine Änderung; 27.3 erfüllt (Kopf mit Commit, Datum, KOPIE); Tatsachennotiz zu 27.3 in der nächsten Tagesanfrage: „Kopie liegt in Teilen mit festen Namen" |

---

## Rückfragen — nur als Auswahl mit Empfehlung

1. **Registerkopie:** (a) Teile mit festen Namen, an Abschnittsgrenzen, plus `REGISTER_INDEX.md` — **empfohlen** (mein Lesen bricht bei ~256 KB ab; gemessen 24.09.) · (b) eine Datei (Suche besser, ich lese sie nicht vollständig).
2. **Verdichtung der Antworten:** (a) eine Indexzeile je Antwort, Register als Verdichtung — **empfohlen** (keine dritte Fassung) · (b) 5–10 Zeilen Festlegungstext je Antwort in `ENTSCHEIDUNGEN.md`.
3. **Repo-Archiv:** (a) keine Verschiebung, „archiviert" ist ein Indexzustand — **empfohlen** (Registerzitate mit Pfad) · (b) `archiv/`-Ordner wie in der Anfrage.
4. **Dritter Träger:** (a) `docs/` mit der täglichen db-Sicherung nach iCloud — **empfohlen** (läuft schon, nichts von Hand) · (b) Zip in `~/Sites/_projektarchiv/` · (c) nur Git.
5. **Austritt der Dialogpaare:** (a) ereignisgebunden (registriert + geschlossen + Indexzeile) plus die zwei jüngsten Tagesanfragen — **empfohlen** · (b) feste Frist 7 Tage · (c) bis zur nächsten Übergabe.
6. **Umfang jetzt:** (a) die ganze Sofortliste in der Reihenfolge C4 — **empfohlen** (ein Vorgang, ein Abgleich) · (b) nur Nr. 1 und 3 (Registerkopien und Dialog bis 25e), Rest später.

---

**Kurz:** Die Ablage wird Arbeitsfläche, Git bleibt Träger. Eine Registerfassung in Teilen mit festen Namen, erneuert nach jedem Registerauftrag, plus ein einseitiger Registerindex. Dialog ist befristet durch Ereignisse, verdichtet in eine Indexzeile — das Register ist die Verdichtung. Aufträge bis zur Annahme, Ergebnisse bis zur Antwort, Belege vor dem Tag nie. Nichts wird im Repo verschoben. Backlog in vier Dateien, davon zwei in der Ablage — und damit erstmals für mich lesbar. Sofortliste geschätzt ≈ 1 050k raus, ≈ 300k rein, Stand danach ≈ 25–27 %; Zahlen misst der Auftrag vor dem Löschen. Sechs Rückfragen als Auswahl.

**Unsicher:**
- Alle Tokenzahlen der Sofortliste sind Mittelwerte aus euren Gruppensummen, nicht gemessen; die Reihenfolge C4 sorgt dafür, dass ein Fehler in der Schätzung nichts kostet.
- Ob die Projektschnittstelle Tokens je Datei liefert; sonst Bytes ÷ 4 als gekennzeichnete Näherung.
- Die Grenze ~256 KB für mein vollständiges Lesen ist einmal gemessen (24.09.); 240 000 Bytes je Teil ist Sicherheitsabstand, keine gemessene Grenze.
- Ob `REGISTER_INDEX.md` (Kette der Marken) sich vollständig per Skript auflösen lässt; A4 verlangt deshalb Lesen und lässt „mehrdeutig" zu.
- Ob das geteilte `BACKLOG.md` nach Schritt C frei von Grössen nach 27.1 ist, kann nur der steuernde Chat prüfen (27.4) — ich lese es erst, wenn er es freigegeben hat.

---

## In einfacher Sprache

Die Projektablage ist zu drei Vierteln voll, und fast die Hälfte davon sind vier alte Abschriften desselben Regelwerks. Mein Vorschlag: Die Ablage soll nur das enthalten, was für die gerade offenen Fragen gelesen werden muss — und von jedem Dokument nur eine Fassung. Das Original von allem liegt sicher im Git-Repo auf dem Mac und bei GitHub, dazu täglich auf iCloud; aus der Ablage etwas herauszunehmen verliert deshalb nichts. Vom Regelwerk gibt es künftig eine Abschrift in vier Teilen mit festen Namen, die nach jeder Änderung erneuert wird, und eine Seite, die sagt, wo welche Regel gerade gilt. Meine Antworten bleiben nur so lange in der Ablage, bis ihr Text im Regelwerk steht und ihre Fragen beantwortet sind; danach steht eine Zeile in einer Liste, und der volle Text bleibt im Repo. Aufträge bleiben, bis ihr Ergebnis angenommen ist. Das lange Backlog wird in vier Dateien geteilt, von denen nur zwei in die Ablage kommen; damit kann ich es zum ersten Mal lesen, weil die Zeilen mit Ergebniserwartungen in einer eigenen Datei bleiben. Nichts wird im Repo verschoben, denn das Regelwerk verweist auf Dateien mit ihrem Pfad. Sofort können etwa 115 Dateien aus der Ablage; danach ist sie etwa zu einem Viertel gefüllt. Die Zahlen sind geschätzt und werden vor dem Löschen gemessen. Der Mac-Auftrag baut die neuen Dateien, der steuernde Chat räumt die Ablage, der Betreiber gibt einmal frei.
