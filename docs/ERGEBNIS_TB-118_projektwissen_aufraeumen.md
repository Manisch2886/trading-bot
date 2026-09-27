# TB-118: Ergebnis. Projektwissen aufräumen, Repo-Seite (Fable 27b Teil D) — Registerkopie in vier Teilen + `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md` (44 Zeilen), Backlog in vier Dateien, `UEBERGABE.md`, Soll-Skript, Löschliste; `docs/` in der täglichen Sicherung

**Sitzungstitel:** `TB-118` · **Stand:** 27.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-118_projektwissen_aufraeumen.md` · **Belege:** `docs/belege/TB-118/`
**Eingang:** `1e11457` (Abgabe TB-117). Commits: `f8056ef` (Schritt 0), `6797d70` (A), `8a3f6f6` (B), `3018657` (C),
`45ad4fb` (D), `6b5fef2` (E), `d39cab4` (F), `2f57be9` (H), der Abgabe-Commit (G: dieses Dokument, Journal DQ). Nach
jedem Commit gepusht.
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27b_konzept_projektwissen.md` (md5
`ad35734f99414c982741b0c3f5b27862`, 36 823 Bytes, geprüft); Anfrage 27b md5 `f22c54a1…` geprüft. Freigabe des
Betreibers 26.09.2026, ca. 23:15 (Auswahlkarte, wörtlich im Auftrag): „Alle sechs übernehmen (Empfohlen)“.
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Kein Abbruchkriterium ausgelöst. **Sichtschutz 27.1:** Diese
Sitzung hat `BACKLOG.md` gelesen und die Zeilen nach 27.1 nach `BACKLOG_SICHTSCHUTZ.md` getrennt; **dieses Dokument
enthält keine Ergebnisgrösse des Selektionsraums und keine Erwartung über den Ausgang** — Treffer sind mit Fundstelle
genannt (alte Zeilennummer), nicht mit Inhalt (27.5).

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Auftrag, Zeiger, Anfrage und Antwort 27b committet (`f8056ef`). 0b: HEAD `f8056ef`, Register 10 347 Zeilen, höchster Abschnitt 46, sha256 `18e39ee2…`, `BACKLOG.md` 603 Zeilen, 90 `FABLE_*`, 55 `MAC_TB-*`, 86 `ERGEBNIS_TB-*`. 0c: `db_sicherung.sh` 12/12 rc 0 |
| ⭐⭐ **A** | `docs/werkzeuge/registerkopie.py`: Register (`1e11457`, 746 596 B) in **vier Teile** an Abschnittsgrenzen — 0–23 / 24–37 / 38–43 / 44–46, **239 529 / 220 905 / 227 107 / 59 998 B**, je ≤ 240 000. **A2: Bodies aneinander `cmp` rc 0**, Mutationsprobe rc 1 und zurück, zweiter Lauf bytegleich. `REGISTER_INDEX.md` aus 23 Marken „ERSETZT/PRÄZISIERT durch“, 42 weiteren Markenzeilen und 49 Rückverweis-Überschriften; **drei Stellen mehrdeutig** benannt |
| ⭐⭐ **B** | `docs/werkzeuge/dialog_index.py` → `FABLE_DIALOG_INDEX.md`: **44 Zeilen = 44 Antworten** (B3), sechs Felder je Zeile gefüllt (`--pruefen` rc 0, Gegenprobe rc 1). Registriert 32, ohne Registertext 10, **offen 2 (27a, 27b)**. Frage/Entscheidung von Hand aus dem Block „Kurz“ |
| ⭐⭐ **C** | `BACKLOG.md` (478 Inhaltszeilen) → **`BACKLOG.md` 144 offen · `BACKLOG_ENTSCHEIDUNGEN.md` 109 · `BACKLOG_ERLEDIGT_2026-09.md` 215 (mit Abschnitt 8 ganz) · `BACKLOG_SICHTSCHUTZ.md` 10** (darunter Z. 170 und 190). **C2: Zeilenmenge rc 0** (jede alte Zeile genau einmal, neu nur vier Kopfzeilen), Gegenprobe rc 1; numstat 2/385, 145/0, 296/0, 30/0. ⚠️ Name `BACKLOG_ENTSCHEIDUNGEN.md` statt `ENTSCHEIDUNGEN.md` **per Auswahlkarte** (Nachtragswächter). Wächter vorher/nachher rc 0. C4: `JOURNAL_NACHTRAG_2026-09-18.md` 5/5 → `nachtraege/_eingearbeitet/`; `BACKLOG_NACHTRAG_2026-09-18.md` **bleibt** (`c4_offen.txt`) |
| **D** | `UEBERGABE.md` = Fassung 25.09. + Kopfzeile (Rumpf zeichengleich). **D2: 33 Regeln** aus Block 7 (19.09., drei Fassungen und zwei Ergänzungen) und Block 8 (24.09.) gegen ARBEITSWEISE/PRÜFPRINZIPIEN: **steht 10, teilweise 8, fehlt 14**, keine Regel 1 — Vorschlag in `d2_fehlende_regeln.txt`, nichts eingetragen |
| ⭐ **E** | `docs/werkzeuge/ablage_soll.py` + `ablage_ereignisse.json` (Regeln B1–B8 fest im Skript). **E3 auf einer rekonstruierten Ist-Liste** (145 Pfade; die echte hat nur der steuernde Chat): entfernen 121, C3 Nr. 1–7 auf derselben Liste 119, **116 davon deckungsgleich; 3 + 5 Abweichungen benannt**, nicht angepasst |
| ⭐ **F** | `LOESCHLISTE_TB-118.md`: **121 Dateien, 3 104 055 B, ≈ 1,33 Mio. Tokens** (kalibriert: Bytes ÷ 2,337 aus vier Gruppen der Betreibermessung; Bytes ÷ 4 = 776 013 steht daneben). Erwarteter Stand danach **≈ 564 000 ≈ 28 %**. `git status --porcelain` leer nach F |
| **H** | `db_sicherung.sh` schreibt je Lauf **`docs.tar.gz`** (git archive HEAD docs, 5,3 MiB, 1576 Dateien) mit sha256 — **statt `git bundle` (117 MiB, 48 s) per Auswahlkarte**. H2: Lauf von Hand rc 0, `gzip -t` rc 0, Dateizahl 1576 = 1576, `SHA256SUMS` 13/13 OK, Logzeile 1; Gegenprobe an beschädigter Kopie rc 1. Crontab unverändert |
| **G** | Dieses Dokument, Journalblock **DQ** |

---

## 1. Schritt A — Registerkopie in Teilen und `REGISTER_INDEX.md`

**Werkzeug** `docs/werkzeuge/registerkopie.py` (Standardbibliothek, Python 3.9): liest das Register am HEAD
(bricht mit 2 ab, wenn der Arbeitsbaum abweicht), schneidet nur an `^## <n>\.`, gierig bis 240 000 Bytes je Datei
**einschliesslich** Kopf, schreibt `REGISTER_KOPIE_teil<n>.md` mit dem Kopf aus A1 (Zeile 1), Leerzeile, Body ab Zeile 3.
`Commit` im Kopf ist der letzte Registercommit (`git log -1 -- <register>`), `Datum` sein Commit-Datum — ein zweiter
Lauf ohne Registeränderung gibt dieselben Dateien, gleich an welchem HEAD. `--pruefen` prüft die Bodies gegen das
Original am Commit aus dem Kopf; `--marken` sammelt die Marken für den Index.

| Nachweis | Beleg | Ergebnis |
|---|---|---|
| A2 (i) Bodies in Reihenfolge `cmp` gegen `git show HEAD:<register>` | `a2_cmp.txt` | **rc 0**, sha256 beider `18e39ee2…` |
| A2 (ii) Grösse je Teil (`wc -c`) | `a2_groessen.txt` | 239 529 / 220 905 / 227 107 / 59 998 — alle ≤ 240 000 |
| Mutationsprobe (Byte 100 000 in Teil 3 ± 1) | `a2_mutation.txt` | `cmp` **rc 1**, `--pruefen` rc 1; zurückgesetzt, sha256 vorher = nachher, `--pruefen` rc 0 |
| Wiederholbarkeit (zweiter Lauf in anderen Ordner) | `a2_wiederholung.txt` | 4 × `cmp` rc 0 |
| A3 alte Kopien | `a3_alte_kopien.txt` | im Repo nur `REGISTER_KOPIE_2026-09-22.md` und `_24.md`, unberührt. ⚠️ **`REGISTER_KOPIE_2026-09-21.md` und die drei Teile vom 24.09. waren nie im Repo** (in keinem Zweig) — sie liegen nur in der Ablage |

⚠️ **Teil 1 steht bei 239 529 Bytes**, 471 unter der Grenze. Das Register ist append-only, Teil 1 (Abschnitte 0–23)
wächst nicht mehr; es wächst Teil 4. Bei 240 000 kommt ein Teil 5 dazu — die Namen der ersten vier bleiben.

**`REGISTER_INDEX.md`** (13 423 B): Tabelle der Teile, Festlegungen 1–12 (nur Festlegung 1 trägt eine Marke:
PRÄZISIERT durch 24), die alten Abschnitte 2–14, Registertexte 0–7 mit Buchstaben (je Ersteintrag, Kette der Marken,
geltende Fundstelle, „dazu“ für Überschriften und andere Markenwörter) und eine Zeile je Abschnitt 18–46. Gemessen aus
`a4_marken.txt` (mit Spalte „unter“: Unterabschnitt bzw. Eintrag A1 …, R1 … vor der Marke). **Mehrdeutig benannt:**
4a (ob 28.6/30.6 den Wortlaut von 25.3 fortschreiben), 30.2 (3) (Abschnitte 33, 35, 45), 33.2/33.3 (Ergänzungen in
34, 35, 38, 42, 45).

## 2. Schritt B — `FABLE_DIALOG_INDEX.md`

`docs/werkzeuge/dialog_index.py` schreibt je Antwort: Antwort · Stichwort · Frage · Entscheidung · Status ·
Fundstelle · offen · Anfrage · Pfad. **Gemessen:** Fundstelle = Registerabschnitte, in denen der Dateiname ohne `.md`
vorkommt (`grep -F`-Bedeutung); Anfrage = die `FABLE_ANFRAGE`, die die Antwort in ihren ersten zwölf Zeilen nennt
(„Bezug“), sonst gleicher Buchstabe. ⚠️ **Der gleiche Buchstabe ist meist nicht die zugehörige Anfrage** (z. B.
Antwort 21i antwortet auf Anfrage 21b) — deshalb der Bezug zuerst, der Buchstabe nur als Rückfall und so gekennzeichnet.
**Von Hand:** Frage und Entscheidung aus dem Block „Kurz“ (sechs Antworten ohne „Kurz“: aus Überschrift und Kopf),
`b2_handfelder.json`. **offen:** `b2_offen.txt` misst je Antwort Frage-/Messbitte-Muster und spätere Anfragen, die
ihren Buchstaben nennen (nach Buchstabenfolge und nach Commit-Zeit); gelesen eingeordnet: **nur 27a und 27b offen**.
Ein zweiter Lauf ohne Handfelder-Datei behält die Handfelder (sha256 gleich). **B3** (`b3_zaehlung.txt`): 44 Zeilen =
44 Dateien, 44/44 mit sechs Feldern, `--pruefen` rc 0; ein geleertes Feld → rc 1.

## 3. Schritt C — Backlog-Teilung

**Gelesen, Zeile für Zeile** (603 Zeilen; `c1_zuordnung.txt` nennt je Inhaltszeile Kennung, Klasse, Grund).
Klassen: O offen (bei Mischzeilen: mindestens ein offener Teil), E Festlegung/Regel/Lehre/Betreiberentscheid, D
erledigt/beantwortet/abgelöst/Archivverweis und Abschnitt 8 ganz, S Grösse oder Erwartung nach 27.1.
⚠️ **K-Nummern sind nach Inhalt eingeordnet, nicht nach Präfix:** der K-Namensraum gehört zu Abschnitt 4 „Laufend,
klein“ und mischt offene Punkte (K1a–K1z), Regeln (K2b–K3j) und Lehren. Auftrag und 27b sagen „K-Einträge →
ENTSCHEIDUNGEN“ (Fable hat den Backlog nicht gelesen); wörtlich angewandt wären offene Aufgaben aus `BACKLOG.md`
verschwunden.

**Sichtschutz (S, 10 Zeilen, alte Zeilennummern):** 143, 167, **170**, **190**, 222, 224, 440, 441, 510, 531. Gefunden
über Suchmuster (Sharpe, Rendite, Drawdown, Trades, Erwartung …) über alle 603 Zeilen, jede Fundstelle gelesen.
Zwei davon sind offene Punkte (440, 531) — sie bleiben offen, liegen aber nur im Repo. Z. 441 ist eine Regel, deren
Wortlaut eine Kennzahl zitiert. Die Dateien für die Ablage (`BACKLOG.md`, `BACKLOG_ENTSCHEIDUNGEN.md`) sind danach
noch einmal auf Zahlen mit %, Sharpe, Calmar, Rendite, Trades durchgesehen.

**Die Rückfrage an den Betreiber, wörtlich** (`c1_entscheidung_dateiname.txt`): *„TB-118 Schritt C: Wie soll die
Datei mit den Festlegungen aus dem Backlog heissen? Mit dem Auftragsnamen ENTSCHEIDUNGEN.md meldet der Nachtragswächter
gemessen rc 1: 36 Nummern aus 8 Nachträgen gelten als nicht angekommen, gemeldet ab dem Cron-Lauf 04:50 täglich per
Telegram. DOKUMENTATIONSSTANDARD Regel 10 verlangt für jede Auslagerung aus dem Backlog den Namen
BACKLOG_<name>.md.“* — Antwort: **„BACKLOG_ENTSCHEIDUNGEN.md (Empfohlen)“**. Dazu stehen die Überschriften in den drei
neuen Dateien eine Ebene tiefer, sonst zählt der Wächter „## 2s“ doppelt (gemessen in der Probe).

| Nachweis | Beleg | Ergebnis |
|---|---|---|
| C2 Zeilenmenge (Counter, kein `set`, kein `sort -u`) | `c2_zeilenmenge.py/.txt` | alt 478 = neu 145 + 110 + 216 + 11 − 4 Kopfzeilen; fehlt 0, doppelt 0; **rc 0** |
| Gegenprobe (eine Zeile entfernt, eine verdoppelt) | `c2_gegenprobe.txt` | (a) 1, (b) 1, **rc 1** |
| numstat | `c2_numstat.txt` | `BACKLOG.md` 2/385 · `BACKLOG_ENTSCHEIDUNGEN.md` 145/0 · `BACKLOG_ERLEDIGT_2026-09.md` 296/0 · `BACKLOG_SICHTSCHUTZ.md` 30/0; alte Fassung im Git (`8a3f6f6`) |
| Nachtragswächter | `c_waechter_vorher.txt`, `c_waechter_nachher.txt` | beide **rc 0**, 0 falsch verschoben, 0 Doppelbelegung; „nicht prüfbar“ 4 → 5 (die verschobene Datei ohne Buchstaben kennt sein Dateimuster nicht) |

**C4** (`c4_messung.py/.txt`, `c4_offen.txt`): Der Wächter kann beide Dateien nicht prüfen (Name ohne Buchstabe,
liegen nicht unter `nachtraege/`), gemessen deshalb nach seiner Regel: `JOURNAL_NACHTRAG_2026-09-18.md` — 5/5 Blöcke
mit Titel und Kern im Journal (BA–BE) → `git mv` nach **`docs/projektfuehrung/nachtraege/_eingearbeitet/`** (der Ort nach
DOKUMENTATIONSSTANDARD 10; der Auftrag schreibt `docs/projektfuehrung/_eingearbeitet/`, diesen Ordner gibt es nicht).
`BACKLOG_NACHTRAG_2026-09-18.md` — 42/43, bei Kette **0,82** fehlt der Kern (die Zeile wurde später als erledigt
fortgeschrieben) → **nicht verschoben**, `c4_offen.txt`.

## 4. Schritt D — `UEBERGABE.md` und die Regeln aus Block 7

`UEBERGABE.md` = `UEBERGABE_2026-09-25.md` mit der Kopfzeile aus D1 als Zeile 3; `diff` des Rumpfs gegen die
Vorlage leer. Die datierten Dateien unverändert.

**D2** (`d2_fehlende_regeln.txt`): 33 Regeln — Block 7 der Übergabe vom 19.09. in drei Fassungen (Z. 181, 577, 1118)
und zwei Ergänzungen (Z. 687, 790), dazu Block 8 der Übergabe vom 24.09. (dort so nummeriert, gleicher Inhalt).
Suche je Regel mit bis zu drei Wortlauten in ARBEITSWEISE und PRÜFPRINZIPIEN, Fundstelle gelesen.

**Die 14, die fehlen** (Vorschlag für den Nachtrag, nicht eingetragen):
19/5 ein Nachweis gilt für den Gegenstand, den er berührt · 19/6 ein Abbruchkriterium benennt die Sache, nie ihr
Merkmal — ⚠️ mit **Widerspruch** zu ARBEITSWEISE 6d, Z. 898 („nie zu einer Rückfrage“) · 21/1 nach jeder
Fable-Antwort die **laufenden** Aufträge prüfen · 21/2 Aktenzeichen mit Wortlaut · 21/3 Fassungszeile im Sendetext ·
21/4 gleiche Sonde für die unverdächtige Datei · 21/6 Fundstelle statt Inhalt (steht als Register 27.5, dort kein
Verweis) · 21/7 Fables Berichtigung wird gemessen wie jede Behauptung · 21b/1 vor dem Schreiben auf eine vorhandene
Datei lesen · 21b/5 ein Nachtrag, der die Sitzung nicht mehr erreicht, wird Auftrag · 24/4 eine Kette ist erst
geprüft, wenn alle Eingaben geprüft sind · 24/5 Vormessung/Nachmessung · 24/6 Hilfsdateien über die Löschfreigabe der
Brücke · 24/R2 eine Fable-Anfrage ist erst übergeben, wenn sie als Kopierblock in der Antwort stand.

## 5. Schritt E — `ablage_soll.py`

Regeln fest im Skript (Docstring, je mit 27b-Verweis B1–B8); Index aus `FABLE_DIALOG_INDEX.md`; ereignisgebundene
Dateien aus `docs/werkzeuge/ablage_ereignisse.json` (14 Einträge, von Hand, mit Beleg je Eintrag; Fristen als Datum).
Ausgaben `soll.txt`, `entfernen.txt`, `ablegen.txt` und zusätzlich **`ohne_regel.txt`** — was zu keiner Regel passt,
wird gemeldet, nicht entfernt.

**Gemessen und im Skript berücksichtigt:** Die wörtliche B4-Regel („kein `docs/ERGEBNIS_TB-nnn_*.md`“) hätte
`MAC_TB-79` und `MAC_TB-88` als offen geführt und zum Ablegen vorgeschlagen — TB-79 steht als Nachtrag in
`ERGEBNIS_TB-78`, TB-88 unter `docs/belege/TB-88/`. Das Skript sucht auch dort.

**E3** (`e3_probe.py/.txt`, `e3_ausgabe/`): ⚠️ **Die Ist-Liste ist rekonstruiert** (`e3_ist_rekonstruiert.txt`) — die
Mac-Sitzung liest die Ablage nicht. 145 Pfade nach der Gruppentabelle der Anfrage 27b, Namen aus dem Repo, wo nur eine
Anzahl bekannt ist, jede Annahme im Kopf der Datei gekennzeichnet. Ergebnis: Ist 145 · Soll 37 · entfernen 121 ·
ablegen 13 · ohne Regel 0. C3 Nr. 1–7 auf derselben Liste: 119; **116 entfernt auch das Skript.**

| Abweichung | Skript | Grund |
|---|---|---|
| (a1) `BACKLOG_NACHTRAG_2026-09-18.md` | bleibt | Messung nach Regel 10 unvollständig (C4) |
| (a2) `FABLE_UEBERGABE_2026-09-24`, (a3) `FABLE_WOCHENRUECKMELDUNG_2026-09-22` | bleiben | 27b B6: Austritt erst mit der nächsten — **widerspricht 27b C3 Nr. 3** |
| (b1) `ERGEBNIS_TB-116` | geht | keine Anfrage zitiert es (27c fehlt); kommt mit 27c zurück |
| (b2) Anfrage und Antwort 26a | gehen | Index nicht offen; die zwei jüngsten Paare sind 27a, 27b (27b meinte „Tagesanfragen“) |
| (b3) `NACHTRAG_ARBEITSWEISE_6d_…` | geht | eingearbeitet (ARBEITSWEISE 6d) |
| (b4) `UEBERGABE_2026-09-25.md` | geht | `UEBERGABE.md` liegt seit D im Repo (G2) |

## 6. Schritt F — Löschliste

`docs/belege/TB-118/f1_loeschliste.py` → `f1_tokens.txt` und **`docs/projektfuehrung/LOESCHLISTE_TB-118.md`**
(Tabelle Datei · Bytes · Tokens · Gruppe · Grund, Summen je C3-Gruppe, „Rein“-Tabelle, Stand danach, Hinweise vor dem
Vollzug). **Token-Verfahren, im Beleg genannt:** Die Projektschnittstelle liefert keine Zahl je Datei (Anfrage 27b:
Gruppensummen). Deshalb (1) **kalibriert**: Bytes ÷ 2,337 — das Verhältnis aus den vier Gruppen der Betreibermessung,
die ganz im Repo liegen (`BACKLOG.md` 105k, `UEBERGABE_*` 54k, `ARBEITSWEISE.md` 33k, `ERGEBNIS_TB-114…116` 32k;
523 387 B ÷ 224 000 Tok); Gegenprobe an der Register-Gruppe (735k gemessen): 2,509 B/Tok, dort ~7 % zu hoch; (2)
**Bytes ÷ 4** nach Auftrag — gegen die Betreibermessung rund 40 % zu tief. Bytes der Fassung am `753ec11`
(26.09., 22:34).

| C3 | Dateien | Tokens kalibriert |
|---|---:|---:|
| 1 Registerkopien 21./22./24.09. | 3 | ≈ 553 000 |
| 2 Teile 24.09. | 3 | ≈ 236 000 (je Teil geschätzt) |
| 3 Dialog bis 25e | 81 | ≈ 311 000 |
| 4 Aufträge | 22 | ≈ 123 000 |
| 5 Belege | 2 | nicht messbar (nicht im Repo) |
| 6 Übergaben | 2 | ≈ 43 000 |
| 7 ereignisgebunden | 3 | ≈ 17 000 |
| Abweichungen (b1)–(b4) | 5 | ≈ 45 000 |
| **Summe** | **121** | **≈ 1 328 000** |

Rein ≈ 417 000 (davon die vier Registerteile ≈ 320 000), `BACKLOG.md` wird ≈ 65 000 kleiner ⇒ **≈ 564 000 ≈ 28 %**.

## 7. Schritt H — `docs/` in der täglichen Sicherung

**Die Rückfrage an den Betreiber, wörtlich** (`h_entscheidung_sicherung.txt`): *„TB-118 Schritt H: Was soll die
tägliche iCloud-Sicherung um 05:20 zusätzlich zu den Datenbanken mitnehmen? Gemessen: git bundle des ganzen Repos
117 MiB und 48 s je Lauf. docs/ als Archiv aus HEAD 5,3 MiB. Das Skript löscht keine alten Sätze, die Aufbewahrung ist
deine offene Frage.“* — Antwort: **„docs/ als Archiv, täglich (Empfohlen)“** (Freigabe 4 lautete „kopiert zusätzlich
docs/“; Schritt H „git bundle“).

`db_sicherung.sh` Schritt 4: `git archive --format=tar.gz HEAD docs` in den Zwischenordner, `mv -n` ins Ziel,
`gzip -t` und Dateizahl gegen `git ls-tree -r HEAD docs`, sha256 in `SHA256SUMS`; Protokoll nur Commit, Dateizahl,
Bytes. Fehler ⇒ Rückgabewert 1 wie bei einer Datenbank. `LIESMICH.md` um einen Absatz ergänzt.

| Probe | Beleg | Ergebnis |
|---|---|---|
| gegen Testziel im Scratchpad | `h2_probe_testziel.txt` | rc 0, `docs.tar.gz` 5 579 726 B, 1576 Dateien |
| von Hand ins iCloud-Ziel | `h2_probe_icloud.txt` | **rc 0**; `gzip -t` rc 0; 1576 = 1576; `shasum -c` 13/13 OK; `grep -c docs.tar.gz PROTOKOLL.txt` **1** |
| Gegenprobe der Prüfmittel (letzte 1000 B abgeschnitten) | ebd. | `gzip -t` **rc 1**, sha256 ungleich |
| Originaldatenbanken gegen 0c | ebd. | 11/12 byteweise gleich; `broker_testnet_t3_supertrend.db` geändert um **08:05:00** = Lauf der Broker-Brücke (Minute 5 alle 4 h), 0c war 07:52 |

## 8. Für den steuernden Chat

**Reihenfolge nach 27b C4 — erst ablegen, dann entfernen, dann messen:**

1. **Vorher prüfen (27.4, deine Pflicht):** `BACKLOG.md` (neu) und `BACKLOG_ENTSCHEIDUNGEN.md` auf Grössen nach
   27.1 — die Mac-Sitzung hat getrennt und nachgesehen, die Prüfung vor dem Ablegen bleibt deine.
2. **Ablegen:** `REGISTER_KOPIE_teil1–4.md`, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`, `UEBERGABE.md`,
   `BACKLOG.md` (ersetzt den gleichen Namen), `BACKLOG_ENTSCHEIDUNGEN.md`, `LOESCHLISTE_TB-118.md`; dazu nach dem Soll:
   Anfrage und Antwort 27b, `MAC_TB-117`, `MAC_TB-118`. ⛔ **Nie in die Ablage:** `BACKLOG_SICHTSCHUTZ.md`,
   `BACKLOG_ERLEDIGT_2026-09.md`, alles unter `belege/`.
3. **Ist-Liste holen und `python3 docs/werkzeuge/ablage_soll.py --ist <ist.txt> --aus <ordner>` laufen lassen.**
   Entfernt wird nur, was in dessen `entfernen.txt` steht **und** in der freigegebenen Löschliste; `ohne_regel.txt`
   ansehen, nicht löschen.
4. ⚠️ **Vor dem Entfernen entscheiden** (G1, das Repo ist der Träger): `REGISTER_KOPIE_2026-09-21.md`, die drei Teile
   vom 24.09. und `belege/TB-91_…`, `belege/TB-93_…` liegen **nur** in der Ablage. Die Registerkopien sind aus dem
   Registerstand ihres Tages rekonstruierbar, nicht bytegleich. Ebenso nur in der Ablage (bleiben aber):
   `FABLE_ANTWORT_2026-09-25f`, `SITZUNGSWAECHTER_ausloeser_statt_tippen.md`, `PROJEKTSTAND_einfache_sprache.md`,
   `PRUEFUNG_2026-09-25_…`, `ERINNERUNG_2026-09-25_…` — ins Repo holen.
5. `knowledge_size` vorher/nachher messen, eine Zeile in `UEBERGABE.md`.
6. Registerauftrag künftig: `registerkopie.py` laufen lassen, Teile committen; `--marken` für `REGISTER_INDEX.md`.
   Nach jeder angenommenen Antwort: `dialog_index.py`, neue Zeile von Hand, `--pruefen`.
7. `ablage_ereignisse.json` pflegen (z. B. `LOESCHLISTE_TB-118.md` nach dem Vollzug auf `true`).

## 9. Für Fable

1. **G1 trifft auf Dateien, die nur in der Ablage liegen** (Abschnitt 8, Punkt 4): Die Annahme in 27b B3 („die
   datierten Kopien … sind im Repo committet“) stimmt für zwei der sechs Registerkopien, nicht für die übrigen vier.
2. **`BACKLOG_ENTSCHEIDUNGEN.md` statt `ENTSCHEIDUNGEN.md`** (Auswahlkarte; DOKUMENTATIONSSTANDARD 10, Wächter).
   Für Teil E: überall, wo 27b `ENTSCHEIDUNGEN.md` nennt, gilt dieser Name.
3. **„K-Einträge“** sind im Backlog ein Namensraum von Abschnitt 4, keine Klasse — offene Aufgaben, Regeln und Lehren
   gemischt. Eingeordnet nach Inhalt.
4. **27b B6 gegen C3 Nr. 3:** Wochenrückmeldung und Fable-Übergabe verlassen die Ablage nach B6 erst mit der nächsten,
   nach C3 sofort. Das Skript folgt B6. Bitte eine Lesart.
5. **„Die zwei jüngsten Paare“:** Die Regel in Teil D E2 sagt Datums-Buchstaben-Paare (heute 27a, 27b), B6 nannte 26a
   und 27a als Tagesanfragen. Das Skript folgt E2; 26a verlässt die Ablage.
6. **„offen“ im Index** ist eng gemessen: Frage oder Messbitte ohne spätere Anfrage, die sie aufnimmt. 27a ist offen,
   weil die Rückmeldung zu TB-116/117 (27c) fehlt — damit hält B5 die Ergebnisse 114/115 in der Ablage, obwohl
   Register 46 steht. B4 hält `MAC_TB-117` (Grundlage 27a); `MAC_TB-116` (Grundlage 26a) geht, obwohl sein Ergebnis
   noch nicht angenommen ist — die Regel koppelt an die Grundlage des Auftrags, nicht an die Annahme.
7. **Drei mehrdeutige Stellen im `REGISTER_INDEX.md`** (4a, 30.2 (3), 33.2/33.3) — dort ist der Wortlaut zu lesen.
8. **G7:** gesichert wird `docs/` als Archiv, nicht das ganze Repo (Auswahlkarte). Für Teil E (ARBEITSWEISE 7b):
   „db-Sicherung sichert zusätzlich `docs/` als `docs.tar.gz`“.
9. **D2:** 14 Regeln aus den Übergaben stehen nicht im Regelwerk; eine davon (19/6) widerspricht ARBEITSWEISE 6d.
   Vorlage für den Nachtrag in `d2_fehlende_regeln.txt`.

## 10. Nicht getan, und warum

- Regelwerk (ARBEITSWEISE, UMZUG, DOKUMENTATIONSSTANDARD, PRÜFPRINZIPIEN) und Register unverändert — nicht freigegeben.
- Nichts im Repo gelöscht oder verschoben ausser `JOURNAL_NACHTRAG_2026-09-18.md` nach `_eingearbeitet/`.
- Nichts in der Projektablage abgelegt oder entfernt (steuernder Chat). Crontab und Datenbanken unberührt.
- E3 nicht gegen die echte Ist-Liste — die liegt nur beim steuernden Chat.

## 11. In einfacher Sprache

Die Projektablage war zu drei Vierteln voll, vor allem mit alten Abschriften des Regelwerks und alten
Fable-Antworten. Diese Sitzung hat im Repo alles gebaut, damit sie aufgeräumt werden kann: eine neue Abschrift des
Regelwerks in vier Teilen mit festen Namen, nachgewiesen Byte für Byte gleich mit dem Original, und eine Seite, die
sagt, wo welche Regel gerade gilt. Dazu eine Liste aller 44 Fable-Antworten mit Frage, Entscheidung und Status, das
lange Backlog in vier Dateien (Offenes, Entscheidungen, Erledigtes, und die Zeilen, die Fable vor dem Tag nicht sehen
darf), eine Übergabe ohne Datum im Namen, ein Skript, das aus dem Repo ausrechnet, was in die Ablage gehört, und eine
Löschliste mit Grössen. Geschätzt können 121 Dateien heraus; danach wäre die Ablage zu gut einem Viertel gefüllt.
Zweimal hast du entschieden: die Entscheidungsdatei heisst `BACKLOG_ENTSCHEIDUNGEN.md`, damit der Nachtragswächter
nicht Alarm schlägt, und die tägliche Sicherung nimmt jetzt den Ordner `docs/` mit (5 MiB), nicht das ganze Repo.
Offen für dich: die Löschliste freigeben und entscheiden, was mit den vier Registerkopien und zwei Belegen geschieht,
die es nur in der Ablage gibt.
