#!/usr/bin/env python3
"""TB-119 Schritt B - Regelwerk-Nachtrag nach Fable 27b Teil E. Aufruf aus der Repo-Wurzel: [--probe]
Drei Abweichungen vom Wortlaut von Teil E, vom Betreiber entschieden (Auftrag TB-119, Schritt B):
BACKLOG_ENTSCHEIDUNGEN.md statt ENTSCHEIDUNGEN.md; 7b: docs/ als docs.tar.gz (nicht git bundle); neuer Abschnitt mit
der naechsten freien Nummer, gemessen (0b_ausgang.txt: hoechste '## 22.', also 23)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from einsetzen_lib import einsetzen  # noqa: E402

AW = "docs/projektfuehrung/ARBEITSWEISE.md"
UM = "docs/projektfuehrung/UMZUG.md"
DS = "docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md"
H = "(27b Teil E, TB-119, 27.09.2026)"

# ---------------------------------------------------------------- ARBEITSWEISE 7b
AW_7B_ALT = "Existenz prüfen, nie den Wert.**\n\n---\n\n## 7c."
AW_7B_NEU = """Existenz prüfen, nie den Wert.**

### Die tägliche Sicherung nach iCloud — auch `docs/` %s

⭐ **db-Sicherung sichert zusätzlich `docs/` als `docs.tar.gz`.**
`docs/werkzeuge/db_sicherung/db_sicherung.sh` (TB-112; Cron täglich 05:20, vom
Betreiber gesetzt — `UEBERGABE.md`, Nachtrag 5) legt je Lauf einen Satz unter
`~/Library/Mobile Documents/com~apple~CloudDocs/trading-bot-db-sicherung/<datum_zeit>/`
an: die Datenbanken und `docs.tar.gz` (`git archive` von `HEAD`, nur `docs/`;
Dateizahl gegen `git ls-tree`, `gzip -t`), dazu `SHA256SUMS` (TB-118, Schritt H).
Damit liegt jedes Dokument dreifach — Mac, GitHub, iCloud —, und keine Kopie
entsteht von Hand (27b G7, Abschnitt 23).

⚠️ **Nicht `git bundle`:** Das ganze Repo hätte je Lauf **117 MiB** gekostet,
`docs/` kostet **5,3 MiB** (gemessen TB-118). Betreiberentscheidung per
Auswahlkarte, wörtlich in `docs/belege/TB-118/h_entscheidung_sicherung.txt`.
*Kein Zip, kein Archiv von Hand* (Abschnitt 2).

---

## 7c.""" % H

# ---------------------------------------------------------------- ARBEITSWEISE 8
AW_8_ALT = "**Widersprüche**, nicht Fortschrittsberichte.\n"
AW_8_NEU = """**Widersprüche**, nicht Fortschrittsberichte.
  ⭐ **Dazu eine Füllstandszeile der Projektablage** %s:
  `knowledge_size` (Tokens und Anteil), Zahl der Dateien, und die Dateien, die
  nach **14 Tagen** noch kein Austrittsereignis hatten — **genannt, nicht
  gelöscht** (27b C2 und G6, Abschnitt 23). Gemessen vom steuernden Chat.
""" % H

# ---------------------------------------------------------------- ARBEITSWEISE 15 (Indexpflicht)
AW_15_ALT = "nicht prüfen, ob die Frage die Antwort schon enthielt.\n\n### ⭐ Bei jeder Übergabe"
AW_15_NEU = """nicht prüfen, ob die Frage die Antwort schon enthielt.

> ⭐ **Und jede angenommene Antwort bekommt ihre Zeile in
> `projektfuehrung/FABLE_DIALOG_INDEX.md`** %s — Antwort
> (Datum und Buchstabe), Frage in einem Satz, Entscheidung in einem Satz,
> Register-Fundstelle, Status (offen / registriert / ohne Registertext),
> Repo-Pfad.

**Wie:** `docs/werkzeuge/dialog_index.py`, die neue Zeile von Hand, danach
`--pruefen` (`ERGEBNIS_TB-118`, Abschnitt 8, Nr. 6). ⭐ **Warum eine Zeile und
nicht mehr:** Der Wortlaut steht im Register, die Begründung im Volltext; eine
dritte Fassung dazwischen wäre eine Quelle, die abweichen kann (27b G4). Ohne
Indexzeile verlässt kein Dialogpaar die Projektablage (Abschnitt 23, Klasse B6).

### ⭐ Bei jeder Übergabe""" % H

# ---------------------------------------------------------------- ARBEITSWEISE 23 (neu, am Dateiende)
AW_23_ALT = "und vorher nachsehen, ob ein altes im Weg steht.*\n"
AW_23_NEU = """und vorher nachsehen, ob ein altes im Weg steht.*

---

## 23. Die Projektablage — Arbeitsfläche, nicht Träger %s

⚠️ **Herkunft:** Fable 27b (`projektfuehrung/FABLE_ANTWORT_2026-09-27b_konzept_projektwissen.md`),
Teile A–C, eingetragen nach der Tabelle in Teil E. Freigaben: 26.09.2026, ca.
23:15 („Alle sechs übernehmen“, TB-118), und 27.09.2026, 18:08 und ca. 18:25
(wörtlich im Auftrag TB-119). Die Repo-Seite hat TB-118 gebaut; die Ablage hat
der steuernde Chat am 27.09.2026 geräumt. *Nummer gemessen (K2i): die höchste
vorhandene war 22; 19 ist der Sitzungswächter.*

⚠️ **Zwei Namen weichen vom Wortlaut von 27b ab, beide vom Betreiber per
Auswahlkarte entschieden (TB-118):** `BACKLOG_ENTSCHEIDUNGEN.md` statt
`ENTSCHEIDUNGEN.md` (`ERGEBNIS_TB-118`, Abschnitt 9, Punkt 2) · die tägliche
Sicherung nimmt `docs/` als `docs.tar.gz`, nicht als `git bundle` (ebd., Punkt 8;
Abschnitt 7b).

> ⭐⭐ **Die Projektablage ist die Arbeitsfläche des Prüfers, kein Träger.** Sie
> enthält, was für die **offenen** Vorgänge gelesen werden muss, in **einer**
> gültigen Fassung je Gegenstand. Träger ist das Repo. **Entfernen aus der
> Ablage verliert nichts.**

### 23.1 Die acht Grundsätze (27b Teil A)

| | Grundsatz |
|---|---|
| **G1** Träger und Arbeitsfläche | Träger sind der Repo-Klon auf dem Mac (`~/trading-bot`) und das GitHub-Remote, dazu die tägliche iCloud-Kopie (G7). Alles, was den Umzug überleben muss, liegt dort committet. Die Ablage zählt **nicht** als Träger (`DOKUMENTATIONSSTANDARD.md` 6, `UMZUG.md` 2) |
| **G2** Eine Fassung, feste Namen | Standdokumente tragen **kein Datum im Namen** (`UEBERGABE.md`, `REGISTER_KOPIE_teil<n>.md`, `AUFGABEN_BETREIBER.md`); das Datum steht im Kopf. Nur Vorgangsdokumente — Anfragen, Antworten, Aufträge, Ergebnisse — tragen ihre Nummer im Namen, weil sie zitiert werden. `DOKUMENTATIONSSTANDARD.md` 9 gilt ausdrücklich auch für die Ablage |
| **G3** Repo-Pfade bleiben stabil | Das Register zitiert Dateien mit Pfad und Hash; Verschieben bricht Leserpfade. ⛔ **Kein Archiv-Ordner im Repo** — „archiviert“ ist ein Zustand im Index. Die Ausnahme bleibt `_eingearbeitet/` für Nachträge (`DOKUMENTATIONSSTANDARD.md` 10) |
| **G4** Der Index ist die Verdichtung | Für Registertext ist das Register die Verdichtung. Was eine Antwort darüber hinaus entschieden hat, steht in **einer Zeile** in `FABLE_DIALOG_INDEX.md` (Indexpflicht: Abschnitt 15). Keine dritte Fassung in Prosa |
| **G5** Sichtschutz bestimmt Belege und Ergebnisse | Nach Register 27.1 und 27.5: `docs/belege/` und Laufergebnisse kommen **vor dem Tag nie** in die Ablage. `ERGEBNIS_TB-*` nur, wenn ihr Kopf die Sichtschutz-Zeile trägt; das prüft der steuernde Chat vor dem Ablegen (27.4). Nach dem Tag: Bericht und Belege des Laufs; Messungen auf dem Selektionsraum nur nach der Liste R7 (R6). `BACKLOG_SICHTSCHUTZ.md` und `BACKLOG_ERLEDIGT_2026-09.md` kommen nie in die Ablage |
| **G6** Ein- und Austritt sind Ereignisse | Jede Klasse hat ein Eintritts- und ein Austrittsereignis (23.2). Fristen sind nur Sicherheitsnetz: Was nach **14 Tagen** kein Austrittsereignis hatte, wird in der Wochenrückmeldung **genannt, nicht gelöscht** (Abschnitt 8) |
| **G7** Sicherung ohne Zip | Die tägliche db-Sicherung sichert zusätzlich `docs/` als `docs.tar.gz` nach iCloud (Abschnitt 7b). Drei Kopien — Mac, GitHub, iCloud —, keine von Hand |
| **G8** Wer misst, wer räumt | Der **steuernde Chat** legt ab, entfernt und misst den Füllstand (`knowledge_size` der Projektschnittstelle). Die **Mac-Sitzung** baut die Repo-Seite (Registerkopie, Index, Backlog-Teilung, Soll-Liste). Der **Betreiber** gibt frei und klickt sonst nichts |

### 23.2 Die Klassen (27b Teil B)

| Klasse | Ort | Eintritt in die Ablage | Austritt aus der Ablage | Beispiele, Hinweise |
|---|---|---|---|---|
| **B1 Regelwerk** | Repo **und** Ablage, eine Fassung | — | **nie**; nach jeder Änderung neu abgelegt, gleicher Name | `ARBEITSWEISE.md`, `PRUEFPRINZIPIEN.md`, `DOKUMENTATIONSSTANDARD.md`, `UMZUG.md`, `SITZUNGSWAECHTER_ausloeser_statt_tippen.md`. Ein Nachtrag zum Regelwerk bleibt, bis er eingearbeitet ist (`DOKUMENTATIONSSTANDARD.md` 10), danach nur Repo |
| **B2 Stand** | Repo **und** Ablage, eine Fassung ohne Datum im Namen | — | **nie** (jeweils die aktuelle Fassung) | `UEBERGABE.md`, `BACKLOG.md` (nur Offenes), `BACKLOG_ENTSCHEIDUNGEN.md`, `PLAN_VOR_DEM_TAG.md`, `AUFGABEN_BETREIBER.md`, `PROJEKTSTAND_einfache_sprache.md`, `FABLE_DIALOG_INDEX.md`, `KANDIDATEN_DURCHGANG_2.md` |
| **B2 Stand, nur Repo** | nur Repo | **nie** | — | `BACKLOG_ERLEDIGT_2026-09.md` (mit Abschnitt 8 „Gestrichen“), `BACKLOG_SICHTSCHUTZ.md`, die datierten `UEBERGABE_*` |
| **B3 Register** | Original im Repo, append-only; in der Ablage **Teile mit festen Namen** | — | **nie**; nach jedem Registerauftrag werden alle Teile erneuert | `REGISTER_KOPIE_teil1.md` … `teil4.md` (an Abschnittsgrenzen, je höchstens 240 000 B, Kopf mit KOPIE, Commit, Datum, Abschnitten, Teil n von m) und `REGISTER_INDEX.md`. Nachweis: die Bodies aneinandergehängt sind `cmp`-gleich mit dem Original am genannten Commit |
| **B4 Aufträge** | `docs/auftraege/MAC_TB-nnn_*.md` | mit der Freigabe | mit der **Annahme des Ergebnisses in einer Fable-Antwort**; ohne Fable-Bezug mit dem Abgabe-Commit | nur **offene** Aufträge liegen in der Ablage |
| **B5 Ergebnisse** | `docs/ERGEBNIS_TB-nnn_*.md` | mit der Anfrage, die es zitiert, nach Prüfung der Sichtschutz-Zeile (G5) | wenn die Antwort angenommen **und** der Registerauftrag mit den Tatsachennotizen abgegeben ist | Laufergebnisse vor dem Tag **nie**; nach dem Tag der Bericht als Standdokument |
| **B6 Fable-Dialog** | `docs/projektfuehrung/FABLE_ANFRAGE_*`, `FABLE_ANTWORT_*` | Anfrage mit dem Ablegen, Antwort mit ihrem Eingang | wenn **alle drei** gelten: (a) der Registertext der Antwort steht im Register, (b) keine Frage der Antwort ist offen, (c) die Indexzeile steht (Abschnitt 15) | es bleiben das offene Paar und die zwei jüngsten Paare (Lesart unten). `FABLE_ANTWORT_2026-09-25f` ist ein Standdokument: es bleibt, bis seine Ideen in `KANDIDATEN_DURCHGANG_2.md` und seine Entscheidungen in `BACKLOG_ENTSCHEIDUNGEN.md` stehen |
| **B7 Belege** | nur Repo (`docs/belege/TB-nnn/`) | vor dem Tag **nie** | — | nach dem Tag nur die Belege des Laufs und Messungen nach R7 |
| **B8 Bestandsaufnahmen, Stoffsammlungen, Recherchen, Erinnerungen** | Repo | solange ein offener Auftrag oder eine offene Frage sie braucht | mit dem Auftrag, den sie vorbereiten, oder mit dem Ereignis (Erinnerung → Frist) | gepflegt in `docs/werkzeuge/ablage_ereignisse.json` |

⚠️ **Zwei Lesarten sind bei Fable offen. Hier steht, wie `ablage_soll.py` heute arbeitet:**

- `FABLE_WOCHENRUECKMELDUNG_*` und `FABLE_UEBERGABE_*`: **nur die jüngste bleibt** —
  sie verlassen die Ablage mit der nächsten (27b B6), nicht sofort (27b C3 Nr. 3).
  *Lesart offen, Fable-Sammlung B4.*
- „Die zwei jüngsten Paare“ werden nach **Datum und Buchstabe** der Antwort gezählt
  (27b Teil D, E2), nicht nach Tagesanfragen (B6 nannte 26a und 27a). Eine Anfrage
  ohne Antwort bleibt, wenn sie jünger ist als die jüngste Antwort.
  *Lesart offen, Fable-Sammlung B5.*

*Wie `ablage_soll.py` „offen“ bei Aufträgen misst (gekoppelt an die Grundlage des
Auftrags, nicht an die Annahme), steht in seinem Kopf und in Fable-Sammlung B6.*

### 23.3 Der Mechanismus: Soll-Liste statt Sync (27b C1)

Es gibt keinen Upload und keine Ausschlussliste, sondern eine **Soll-Liste**.
`docs/werkzeuge/ablage_soll.py` leitet aus dem Repo-Stand ab, was nach 23.2 in der
Ablage liegen soll:

```
python3 docs/werkzeuge/ablage_soll.py --ist <ist.txt> --aus <ordner> [--heute JJJJ-MM-TT]
```

Die Ist-Liste holt der steuernde Chat aus der Projektschnittstelle. Zurück kommen
`soll.txt`, `entfernen.txt`, `ablegen.txt` und `ohne_regel.txt` — was zu keiner
Regel passt, wird **gemeldet, nicht entfernt**. Das Skript selbst löscht nichts
und legt nichts ab.

⭐ **Reihenfolge (27b C4): erst ablegen, dann entfernen, dann messen** — so ist
der Prüfer nie ohne Register. Danach `knowledge_size` messen und **eine Zeile**
in `UEBERGABE.md`. Kein Manifest, kein Zip: Git ist die Sicherung, weil im Repo
nichts verschoben oder gelöscht wird; gelöscht wird nur in der Ablage.

### 23.4 Schwellen und Routine (27b C2)

| Grösse | Wert oder Anlass | Wer |
|---|---|---|
| Zielgrösse | ≤ 1,0 Mio. Tokens (50 %%) | steuernder Chat, `knowledge_size` |
| Warnschwelle | 1,4 Mio. Tokens (70 %%): Soll/Ist-Abgleich **sofort**, nicht erst zur Routine | steuernder Chat |
| Registerkopie | nach jedem Registerauftrag erneuert; Kopf nennt den Commit. Die Mac-Sitzung erzeugt sie im Registerauftrag mit: `docs/werkzeuge/registerkopie.py`, Teile committen; `--marken` für `REGISTER_INDEX.md` | Mac-Sitzung erzeugt, steuernder Chat legt ab |
| Dialog | nach jeder angenommenen Antwort: Indexzeile (Abschnitt 15), Austritt prüfen | steuernder Chat |
| Übergabe | Soll/Ist-Abgleich als Schritt 4 von `UMZUG.md` | steuernder Chat |
| Wochenrückmeldung | Füllstandszeile: `knowledge_size`, Dateizahl, Dateien ohne Austrittsereignis nach 14 Tagen (Abschnitt 8) | steuernder Chat |
""" % H

# ---------------------------------------------------------------- UMZUG 1
UM_1_ALT = """⇒ **`UEBERGABE_<datum>.md` wird an jedem sauberen Stand fortgeschrieben** — nicht
am Ende."""
UM_1_NEU = """⇒ **`UEBERGABE.md` wird an jedem sauberen Stand fortgeschrieben** — nicht
am Ende. ⭐ **Ohne Datum im Namen**; das Datum steht im Kopf und in jedem
fortgeschriebenen Block. Die datierten Vorgänger (`UEBERGABE_2026-09-19.md`,
`_24.md`, `_25.md`) bleiben unverändert im Repo *%s*."""  % "(27b G2, Teil E, TB-119, 27.09.2026)"

# ---------------------------------------------------------------- UMZUG 2
UM_2_ALT = """| ⭐ **Projektdokumente** (claude.ai-Projekt „Trading Bots") | **Den Stand und die Führungsdokumente.** Sichtbar in **jedem** Chat des Projekts **und für Fable** | Nichts, was git prüfen muss — kein `numstat`, keine Versionsgeschichte |
| ⭐ **Das Repo** (`Manisch2886/trading-bot`) | **Die Belege.** Versioniert, mit Commit, prüfbar | Es wird von einem neuen Chat **nicht automatisch gelesen** — es braucht einen Verweis |
"""
UM_2_NEU = """| ⭐ **Das Repo** — Klon auf dem Mac (`~/trading-bot`) und GitHub-Remote (`Manisch2886/trading-bot`) | **Alles, was den Umzug überleben muss** — Belege, Stand, Führungsdokumente. Versioniert, mit Commit, prüfbar | Es wird von einem neuen Chat **nicht automatisch gelesen** — es braucht einen Verweis |
| ⭐ **Die iCloud-Kopie** (tägliche db-Sicherung, `ARBEITSWEISE.md` 7b) | `docs/` als `docs.tar.gz` und die Datenbanken, mit Quersummen — ohne Handarbeit | Code und alles ausserhalb von `docs/`; den Stand zwischen zwei Läufen (gesichert wird der committete `HEAD`) |

⭐ **Die Projektablage (claude.ai-Projekt „Trading Bots") ist Arbeitsfläche, kein
Träger** *%s*. Sie ist in **jedem** Chat des Projekts **und für Fable** sichtbar
und enthält, was für die offenen Vorgänge gelesen werden muss — je Gegenstand eine
Fassung, als Kopie aus dem Repo (`ARBEITSWEISE.md` Abschnitt 23). **Entfernen aus
der Ablage verliert nichts.** Sie trägt nichts, was git prüfen muss — kein
`numstat`, keine Versionsgeschichte.
""" % "(27b G1, Teil E, TB-119, 27.09.2026)"

# ---------------------------------------------------------------- UMZUG Schritt 3
UM_S3_ALT = "`docs/projektfuehrung/UEBERGABE_<datum>.md`, **und sie enthält immer diese neun"
UM_S3_NEU = ("`docs/projektfuehrung/UEBERGABE.md` — **ohne Datum im Namen, fortgeschrieben statt\n"
             "neu angelegt**; die Vorgänger bleiben im Repo *(27b G2, Teil E, TB-119, 27.09.2026)* —\n"
             "**und sie enthält immer diese neun")

# ---------------------------------------------------------------- UMZUG Schritt 4
UM_S4_ALT = """### Schritt 4 — In die Projektablage schreiben

**Die Übergabe und dieses Dokument gehen zusätzlich in das claude.ai-Projekt**
(`projektfuehrung/UEBERGABE_<datum>.md`, `projektfuehrung/UMZUG.md`).

⭐ **Warum zusätzlich und nicht stattdessen:** Das Projekt ist der Träger, den ein
neuer Chat **von selbst** sieht. Das Repo ist der Träger, der **Beweiskraft**
hat. Beides ist nötig, und sie müssen gleich lauten.
"""
UM_S4_NEU = """### Schritt 4 — Soll/Ist-Abgleich der Projektablage, Füllstand messen

*Ersetzt „In die Projektablage schreiben“ %s.*

**Die Ablage wird nicht beschrieben, sondern abgeglichen** (`ARBEITSWEISE.md`
Abschnitt 23):

1. Die Ist-Liste der Ablage aus der Projektschnittstelle holen.
2. `python3 docs/werkzeuge/ablage_soll.py --ist <ist.txt> --aus <ordner>` —
   liefert `ablegen.txt`, `entfernen.txt` und `ohne_regel.txt`.
3. **Erst ablegen, dann entfernen** (27b C4). `UEBERGABE.md` und dieses Dokument
   stehen als Stand und Regelwerk immer im Soll. `ohne_regel.txt` ansehen, nicht
   löschen.
4. **Füllstand messen** (`knowledge_size`, vorher und nachher) und eine Zeile in
   `UEBERGABE.md`.

⭐ **Warum ein Abgleich:** Die Ablage ist der Ort, den ein neuer Chat **von
selbst** sieht; **Beweiskraft** hat das Repo (Abschnitt 2). Was in der Ablage
liegt, muss mit dem Repo gleich lauten — und es liegt dort nur, was für die
offenen Vorgänge gebraucht wird.
""" % "(27b C2, Teil E, TB-119, 27.09.2026)"

# ---------------------------------------------------------------- DOKUMENTATIONSSTANDARD 6
DS_6_ALT = """| Träger | wofür |
|---|---|
| **Repo** | die Belege, versioniert |
| **Projektablage** | der Stand, sichtbar für jeden Chat und für Fable |
| **Erinnerung** | wie gearbeitet wird |
"""
DS_6_NEU = """| Träger | wofür |
|---|---|
| **Repo-Klon auf dem Mac** (`~/trading-bot`) | jedes Dokument, versioniert, mit den Belegen |
| **GitHub-Remote** (`Manisch2886/trading-bot`) | dieselbe Fassung, gepusht nach jedem fertigen Teil (`ARBEITSWEISE.md` 14, Regel 3) |
| dazu: **die tägliche iCloud-Kopie** | `docs/` als `docs.tar.gz` mit der db-Sicherung (`ARBEITSWEISE.md` 7b) |

⭐ **Neu bestimmt am 27.09.2026** *(27b G1, Teil E, TB-119)*: Die
**Projektablage ist kein Träger**, sondern Arbeitsfläche — sie hält Kopien aus
dem Repo für die offenen Vorgänge, und Entfernen dort verliert nichts
(`ARBEITSWEISE.md` Abschnitt 23). Die **Erinnerung** trägt kein Dokument,
sondern wie gearbeitet wird (`UMZUG.md` Abschnitt 2).
"""

# ---------------------------------------------------------------- DOKUMENTATIONSSTANDARD 9
DS_9A_ALT = "> ⭐⭐ **Jede Änderung sagt, was sie ablöst — und das Abgelöste wird entfernt,\n> nicht danebengestellt.**\n"
DS_9A_NEU = DS_9A_ALT + """
⭐ **Das gilt ausdrücklich auch für die Projektablage** %s: Dort liegt je
Gegenstand **eine** gültige Fassung unter festem Namen; die abgelöste wird
entfernt, nicht danebengestellt (`ARBEITSWEISE.md` Abschnitt 23). Die vier
Ausnahmen unten bleiben.
""" % "(27b G2, Teil E, TB-119, 27.09.2026)"
DS_9B_ALT = "| Überholte Fassungen einer Regel, sobald die neue steht | **Backlog-Abschnitt 8** (Gestrichen) |"
DS_9B_NEU = ("| Überholte Fassungen einer Regel, sobald die neue steht | **`BACKLOG_ERLEDIGT_2026-09.md`, Abschnitt 8** "
             "(Gestrichen) — seit der Backlog-Teilung (TB-118) dort, nicht mehr in `BACKLOG.md` *(27b Teil E, TB-119)* |")

STELLEN = [
    (AW, "7b: docs.tar.gz", AW_7B_ALT, AW_7B_NEU),
    (AW, "8: Füllstandszeile der Wochenrückmeldung", AW_8_ALT, AW_8_NEU),
    (AW, "15: Indexpflicht FABLE_DIALOG_INDEX.md", AW_15_ALT, AW_15_NEU),
    (AW, "23 (neu): Projektablage", AW_23_ALT, AW_23_NEU),
    (UM, "1: UEBERGABE.md ohne Datum", UM_1_ALT, UM_1_NEU),
    (UM, "2: Träger", UM_2_ALT, UM_2_NEU),
    (UM, "Schritt 3: UEBERGABE.md ohne Datum", UM_S3_ALT, UM_S3_NEU),
    (UM, "Schritt 4: Soll/Ist-Abgleich und Füllstand", UM_S4_ALT, UM_S4_NEU),
    (DS, "6: Träger neu bestimmt", DS_6_ALT, DS_6_NEU),
    (DS, "9: gilt auch für die Ablage", DS_9A_ALT, DS_9A_NEU),
    (DS, "9: Ausnahme Backlog Abschnitt 8 -> BACKLOG_ERLEDIGT_2026-09.md", DS_9B_ALT, DS_9B_NEU),
]

if __name__ == "__main__":
    # --nur-protokoll <commit>: Protokoll gegen den Stand <commit> neu schreiben, Dateien nicht anfassen, pruefen,
    # dass <commit> + Ersetzungen bytegleich mit dem Arbeitsbaum ist.
    import subprocess
    lesen = None
    if "--nur-protokoll" in sys.argv:
        basis = sys.argv[sys.argv.index("--nur-protokoll") + 1]
        lesen = lambda d: subprocess.run(["git", "show", "%s:%s" % (basis, d)], capture_output=True,  # noqa: E731
                                         check=True).stdout.decode("utf-8")
    sys.exit(einsetzen(STELLEN, "docs/belege/TB-119/b_stellen.md",
                       "TB-119 Schritt B — Stellen im Regelwerk (27b Teil E)", "--probe" in sys.argv, lesen))
