# TB-108 — Register 41 und 42: die entschiedenen Einträge aus Fable 24b bis 25c und die Tatsachennotizen TB-103 bis TB-107

**Sitzungstitel:** `TB-108` · **Angelegt:** 25.09.2026, 22:45, vom steuernden Chat
**Grundlage:**
- `docs/projektfuehrung/STOFFSAMMLUNG_REGISTER_41_42.md` (Liste aller Einträge mit Quelle, Art und Stand; **Arbeitsliste dieses Auftrags**);
- die Quellen: `FABLE_ANTWORT_2026-09-24b_…`, `…24c_…`, `…24d_…`, `…25a_…`, `…25b_…`, `…25c_…` (alle unter `docs/projektfuehrung/`, versioniert);
- Bauart: `docs/auftraege/MAC_TB-94_register_39.md` (eingesetzte Blockzitate, `diff` gegen die Quelle, Marken, `numstat` zweite Spalte 0).

**Vorgänger:** TB-107 (`f61bd97`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)
⭐ **Reine Registerarbeit: keine `.py` wird geändert, nichts gerechnet, kein neues Abbild.**

> **In einfacher Sprache, vorweg:** Seit dem 24.09. hat der Verfahrensprüfer in sechs Antworten gut sechzig Regeln, Berichtigungen und Notizen benannt, die ins Regelwerk gehören. Der Code ist längst danach gebaut, das Regelwerk steht aber noch auf dem Stand vom 23.09. Diese Sitzung trägt alles nach: wortgleich, mit Quelle, ohne einen alten Satz zu verändern.

---

## ⭐⭐ Freigabe des Betreibers, wörtlich

**25.09.2026, 22:34, Auswahlkarte im steuernden Chat:**

| Frage | Antwort |
|---|---|
| *„Was soll TB-108 sein? Fables Antworten auf 25d/25e fehlen noch. Unabhängig davon sind die Registereinträge aus 24b bis 25c entschieden.“* | **„Register 41/42 jetzt (Empfohlen)“**: 41 = 24b–24d (Nachweis, Resolver, Deckel, Mutationsproben), 42 = 25a–25c (Zugriffsklassen, Laufbereich, Rückfälle), dazu die Tatsachennotizen aus TB-103 bis TB-107 und die Marken an den alten Stellen. 25d/25e kommen später als 43. Nur das Register und die Zeigerdatei werden geändert, kein Code |

| freigegeben | Pfad | was |
|---|---|---|
| ✔ | `docs/VORREGISTRIERUNG_neuselektion.md` | **anhängen**: Abschnitte 41 und 42; **Marken** an alten Stellen, additiv (neue Zeilen, keine geänderte Zeile) |
| ✔ | `docs/belege/TB-108/`, `docs/ERGEBNIS_TB-108_…`, Journalblock | wie üblich |

⛔ **Nicht freigegeben:** jede `.py`, alles unter `research/`, `shared/`, `strategies/`, `snapshots/`, `ergebnisse/`; kein neues Abbild; die Zeigerdatei `AKTUELLER_AUFTRAG.md` schreibt der steuernde Chat.

⚠️ **Die Gliederung 41/42 hat der steuernde Chat vorgeschlagen und der Betreiber gewählt. Fable hat sie nicht entschieden** (er spricht nur von „Register 41/42“). Das steht so im Kopf von 41, damit Fable widersprechen kann.

---

## ⛔ Was in diesem Auftrag NICHT geschieht

| | |
|---|---|
| ⛔ | **Keine `.py` wird geändert, nichts gerechnet.** Auch wenn ein Registertext eine Codeänderung nahelegt: Dann ist das ein Befund fürs Ergebnis, kein Anlass zum Bauen |
| ⛔ | **Kein bestehender Registersatz wird umgeschrieben.** Das Register ist append-only. Marken sind **neue** Zeilen |
| ⛔ | **Keine Marke innerhalb des Listentexts von Abschnitt 10** (Z. 843 bis vor `## 11.`). Die Sonde prüft diesen Text gegen das Abbild (Prüfung (ii)); jede Zeile dort würde einen Befund erzeugen und ein neues Abbild erzwingen. Gehört eine Marke dorthin (z. B. zu Punkt 11/12, `herkunft.py`), steht sie stattdessen **im Text von 42** mit Verweis auf den Punkt |
| ⛔ | **Nichts aus 25d, 25e, 25f.** Die Antworten stehen aus; sie kommen später in Abschnitt 43 |
| ⛔ | **Sichtschutz 27.1:** keine Ergebnisgrösse des Selektionsraums im Register |

⭐ *Der Registertext folgt dem gemessenen Stand und Fables Wortlaut, nie umgekehrt.*

---

## 0. Schritt 0

**0a — Arbeitsbaum des steuernden Chats committen.** Erwartet:

| Datei | Stand |
|---|---|
| `docs/auftraege/MAC_TB-108_register_41_42.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger auf TB-108 |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-25e_tb107_abgegeben_drei_fragen.md` | neu |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-25f_gesamtanalyse_und_ideen.md` | neu |
| `docs/projektfuehrung/STOFFSAMMLUNG_REGISTER_41_42.md` | neu |
| `docs/projektfuehrung/AUFGABEN_BETREIBER_2026-09-26.md` | neu |
| `docs/projektfuehrung/UEBERGABE_2026-09-25.md` | Nachtrag 2 angehängt |

Weicht der Arbeitsbaum davon ab: melden, nichts Fremdes mitcommitten.

**0b — nach 7c:**
- keine `.git/*.lock`;
- HEAD am Eingang **`f61bd97`**;
- Register **7993 Zeilen** (`wc -l`), `numstat` am Eingang festhalten;
- `herkunft.register()` vorher (erwartet `0ece95e2…`);
- Sonde gegen **`sperrliste_abbild_2026-09-25b.json`** (`40ffe18d…`) vorher: erwartet Pfad-Bestandteile 25/0/0, Prüfung (ii) 0.

**0c — Quellen prüfen:** Alle sechs `FABLE_ANTWORT_…` aus der Grundlage liegen versioniert im Repo (gemessen vom steuernden Chat 22:40). Fehlt eine, brich ab und melde es.

⚠️ **Herkunft der Quellen, ins Register zu übernehmen:** 24b, 24c, 24d, 25a, 25b und 25c wurden vom steuernden Chat aus der Projektablage **abgeschrieben**, nicht byteweise übertragen (das Werkzeug liefert dort nur Text; Übergabe 25.09. Block 8). Die Zitate sind also zeichengleich **mit der Datei im Repo**; ob diese zeichengleich mit Fables Ablage ist, ist nicht gemessen. Genau so als Tatsachennotiz in 41.0 festhalten.

---

## Block A — Vorbereitung und Messung

- **A1:** Die Stoffsammlung Zeile für Zeile gegen die Quellen lesen. Für **jeden** Eintrag (A1–A12, B1–B8, C1–C9, D1–D12, E1–E8, F1–F8, G1–G10) die Stelle in der Quelldatei finden, die den Registertext trägt. Das ist meist ein Blockzitat `> **Registertext …:**`, `> **Berichtigung …:**`, `> **Präzisierung …:**`, `> **Ergänzung …:**` oder eine Tabellenzeile.
- **A2 — Einträge ohne zitierbaren Text:** Manche Einträge sind in der Quelle nur als Stichwort genannt, z. B. 24b D5 „Testrahmen-Notiz“. Für diese:
  - (a) Den Text an anderer Stelle derselben Antwort suchen.
  - (b) Findet sich keiner, als **Tatsachennotiz in eigenen Worten** eintragen, ausdrücklich so gekennzeichnet („eigene Fassung der Sitzung, kein Fable-Wortlaut“), mit Verweis auf die Stichwortstelle.
  - (c) Die Zahl solcher Einträge kommt ins Ergebnis.
- **A3 — Stand je Eintrag nachmessen:** Die Spalte „Stand“ der Stoffsammlung ist eine **Vormessung des steuernden Chats** aus den Ergebnisdokumenten TB-103 bis TB-107. Prüfe jede Angabe mit Commit oder Hash gegen das Repo (`git log`, `sha256sum`, das jeweilige Ergebnisdokument). **Weicht etwas ab, gilt deine Messung**; die Abweichung kommt ins Ergebnis.
- **A4 — Zielabschnitte der Marken lesen:** 2d, 5.4, 6, 11, 16.6, 19, 23.5, 24.x, 33.3, 35.4, 36.5, 37.3, 37.4, 38.x, 39.x, 40.x, soweit Einträge sie berichtigen oder präzisieren. **Keine Marke ohne gelesenen Zielabschnitt.**

Beleg: `a_eintraege.txt` (je Eintrag: Quelle mit Zeilen, Art, Zieltext gefunden ja/nein, Stand gemessen, Markenort).

---

## Block B — Abschnitt 41 (Fable 24b, 24c, 24d)

Neuer Abschnitt `## 41. …` am Ende des Registers. Überschrift sinngemäss: „Nachweis mit zwei Teilen, Resolver ohne Rückfall, Deckel statt Purge, Mutationsproben einzeln — die Einträge aus Fable 24b, 24c, 24d (TB-108, 25.09.2026)“.

- **41.0 Kopf:**
  - Anlass: Die Einträge wurden vom 24.09. an benannt, der Code ist mit TB-103 bis TB-107 danach gebaut, das Register ist erst jetzt nachgezogen. Ein benannter Abstand nach Fable 23f Abschnitt 3.
  - Die Gliederung 41/42 als Vorschlag des steuernden Chats, Betreiberentscheidung 22:34, von Fable nicht entschieden.
  - Die Herkunftsnotiz zu den Quellen (Schritt 0c).
- **41.1 ff.:** je Quelle ein Unterabschnitt, in der Reihenfolge 24b, 24c, 24d, darin die Einträge in der Reihenfolge der Stoffsammlung.
- **Je Eintrag:**
  1. Fables Text als **eingesetztes Blockzitat** (nie abgetippt; `diff` gegen die Quelle mit rc 0 als Beleg), mit Quelle („Fable 24c Abschnitt 6 Punkt 4“);
  2. die Art (Registertext, Berichtigung, Präzisierung, Rücknahme, Tatsachennotiz);
  3. der gemessene Stand aus A3, **ohne Ergebnisgrössen**: Commit, Hash, rc, Anzahl Stellen;
  4. wo er später berichtigt wurde (siehe Ketten unten).
- **24d (a), die Rücknahme:** Eintragen **mit Grund**, wie Fable es verlangt: „damit die Ablage nicht zwei Fassungen führt“.
- **24d (i):** mit dem Messergebnis (Lesehaken seit TB-92; das Register hatte recht; der Fehler lag beim steuernden Chat).

## Block C — Abschnitt 42 (Fable 25a, 25b, 25c, Tatsachennotizen TB-103 bis TB-107)

Neuer Abschnitt `## 42. …` direkt nach 41. Überschrift sinngemäss: „Zugriffsklassen, Laufbereich, die vier Rückfälle und ihr Schluss — die Einträge aus Fable 25a, 25b, 25c und die Tatsachennotizen TB-103 bis TB-107 (TB-108, 25.09.2026)“.

- **42.1 bis 42.3:** je Quelle (25a, 25b, 25c), Bauart wie 41.
- **42.4 Tatsachennotizen G1–G10** (Stoffsammlung Abschnitt G), je mit Ergebnisdokument und Commit. Mindestens:
  - 11.1 geschlossen, 11.2/11.3 offen;
  - Abbild `40ffe18d…`;
  - `register()` `57ec6573…` ⇒ `0ece95e2…` (TB-106);
  - Laufbereich 81 Module, Liste in `docs/belege/TB-107/f1_laufbereich_vereinigung.txt`;
  - Benchmark-Tabelle `64fb2912…` unverändert durch TB-103 bis TB-107;
  - Commit `f5fdb53` gebaut **vor** Fables Antwort auf 25d, revertierbar.
- **42.5 Tatsachennotiz zu 37.3, die Hash-Übergänge seit 39.5:** alle planmässigen Änderungen an Sperrlistendateien aus TB-104 und TB-106, je mit Auftrag, Freigabe, altem und neuem **vollem** Hash, Punkten. Quellen: `docs/belege/TB-104/e2_hashes.txt`, `docs/belege/TB-106/0_hashes_vorher.txt` und `h1_hashes_nachher.txt`, die Ergebnisdokumente.
- **42.6 Was offen bleibt:**
  - 25d (vier Fragen), 25e (drei Fragen), 25f (Gesamtanalyse), alle für Abschnitt 43;
  - die Erweiterung von 19 auf den Laufbereich (Tag-Vorbedingung, 25c 2 (d)); nach 25c (h) muss die Ausnahme für registrierte Protokolle **vorher** im Register stehen: Sie steht jetzt in 42, mit diesem Satz;
  - der Erzeuger auf dem Signalpfad;
  - das Faltenplan-Abbild samt Erzeugerkette (25c (d)).
- **42.7 Was hier ausdrücklich nicht getan wurde:** Tabelle wie 39.10.

## Die Ketten — beide Fassungen, die spätere mit Verweis

| frühere Fassung | berichtigt durch |
|---|---|
| 24c Punkt 4 „Berichtigung 2d-Herleitung“ (B2) | 24d (a)/(b) (C1/C2) |
| 24c „Resolver-Pflicht“, Fundstelle (B5) | 25a (a) (D1), achter Fall |
| 24d (e) `purge_tage` „hängt an Messung“ (C5) | 25a (e) (D5): historischer Stand |
| 25a (1) Präzisierung zu 33.3/35.4 (D5) | 25b (c) (E3): Plan schrumpft nicht, registrierte Abbildung |
| 25a Abschnitt 4 Laufbereich (D8) | 25b (e) (E5): Vereinigung aller Lauf-Typen, Messung am Tag-Commit |
| 25a (A) drei Klassen (D6) | ergänzt durch 25b (a) Klasse (iv), 25b (b) Klasse „Code“, 25c (g) Caches, 25c (h) registrierte Protokolle |
| 25b (h) „offen bis zur Messung“ (E8) | beantwortet in 25c 2 und 4 |
| 37.4 „`herkunft.py` nicht öffnen“ | 25c (b) (F2) |

An der früheren Fassung im **neuen** Text steht jeweils „⭐ BERICHTIGT durch 42.x“, an der späteren „berichtigt 41.x/42.x“.

## Marken am alten Ort

| Marke | wohin (Zielabschnitt vorher lesen) |
|---|---|
| Nachweis mit zwei Teilen; Modus-Lauf = Resolver-Modus | **38.x/39.6**, wo der Modus-Nachweis geführt wird |
| Resolver-Pflicht, kein Fallback unter dem Modus | **19**, unter dem Registertext 5e |
| Sauberkeit über den Laufbereich (Ergänzung, noch nicht vollzogen); Ausnahme registrierte Protokolle | **19**, unter der Tabelle der Startprüfungen |
| 5.4 „gefundene“ Trades | **5.4** |
| Deckel statt Purge; Bedingung auf den Positionen des Gewinners | **2d** und **16.6** |
| Rasterbedingung heisst „keine Rasterbedingung (Abschnitt 6)“; unbekannter Text ⇒ 2 | **6**, nach dem Absatz „Zellen, in denen die Strategie nicht definiert ist …“ |
| 11.1 geschlossen, 11.2/11.3 offen | **11**, am Ende |
| `herkunft.py` planmässig geöffnet | **37.4** |
| Plan schrumpft nicht; registrierte Abbildung; Feldliste | **33.3** und **35.4** |
| Drei Ausgänge gelten weiter; Zwischenablage und Protokolle als Klassen | **36.5** nur, wenn ein Eintrag 36.5 berührt, sonst keine Marke |
| TB-92-Lesehaken | **39.6**/**39.8** |
| „sieben statt acht“, Mutationsproben einzeln | **12**, **40.6**, **40.7** |

⚠️ **Setze keine Marke, deren Zielabschnitt du nicht gelesen hast.** Passt eine nicht, lass sie weg und **melde, welche und warum**. ⛔ Keine Marke in Abschnitt 10 (siehe oben).

---

## Block D — Nachweise

| | Soll |
|---|---|
| **D1** | `git --no-optional-locks log -1 --numstat -- docs/VORREGISTRIERUNG_neuselektion.md` nach dem Register-Commit: **zweite Spalte 0** |
| **D2** | Je eingesetztes Blockzitat ein `diff` gegen die Quelldatei, **rc 0**. Zahl der Zitate = Zahl der rc 0 (Bauart TB-89/TB-94) |
| **D3** | Sonde gegen `40ffe18d…` nach dem Commit: **Pfad-Bestandteile 25/0/0, Prüfung (ii) 0**, gleich wie vorher. Meldet (ii) etwas, liegt eine Zeile in Abschnitt 10 ⇒ abbrechen, melden |
| **D4** | `herkunft.register()` nachher: Der Hash ändert sich erwartungsgemäss (die Registerdatei ist Teil). Alt und neu voll ins Ergebnis und als letzte Zeile in 42.5 |
| **D5** | `test_vorregistrierung` am Endstand (liest Registerstellen per Parser, z. B. `G6`): **196/196**. Rot ⇒ nicht reparieren, melden |
| **D6** | `registerbericht.py --pruefen`: war vor TB-106 schon rot (Block Z. 392 ff. veraltet); nur Ausgang festhalten |
| **D7** | Hashes: Geändert sind nur das Register und `docs/`. Alle `.py`, `ergebnisse/`, Snapshot, Datenstand `d9449faf…`, `*.db` (bis auf den Cron) gleich |

**Commits:** (1) Schritt 0 · (2) ⭐ **Abschnitt 41, 42 und alle Marken in EINEM Commit** · (3) Belege, Ergebnis `docs/ERGEBNIS_TB-108_register_41_42.md`, Journalblock.

Das Ergebnis enthält:
- einen Abschnitt **„Für Fable“** mit der Liste der Einträge (Nummer im Register ⇒ Quelle), den Einträgen in eigener Fassung (A2), den nicht gesetzten Marken und den Abweichungen aus A3;
- „Für die Folgesitzung vorbereitet“;
- „In einfacher Sprache“.

## ⚠️ Abbruchkriterien

1. Eine Quelldatei fehlt (0c).
2. `numstat` zweite Spalte ≠ 0 nach einem Versuch, es zu richten.
3. Die Sonde meldet nach dem Commit etwas anderes als vorher (D3).
4. Ein Eintrag verlangt, einen bestehenden Registersatz zu ändern, damit er aufgeht. Dann stimmt eine Annahme dieses Auftrags nicht: melden.
5. Die Arbeit wird zu gross für eine Sitzung. Dann **41 vollständig** committen (mit numstat 0 und Zitat-Belegen), 42 als Folgeauftrag melden. **Nie einen halben Abschnitt committen.**

⭐ *Abweichungen in A3 und nicht gesetzte Marken sind keine Fehler, sondern Ergebnisse. Der Auftrag ist nur dann nicht abgearbeitet, wenn sie verschwiegen werden.*

---

## In einfacher Sprache

Das Regelwerk des Auswahllaufs wird nur ergänzt, nie umgeschrieben. Seit zwei Tagen hat der Verfahrensprüfer viele neue Regeln und Berichtigungen benannt, und die Programme sind längst danach gebaut. Im Regelwerk selbst fehlen sie noch.

Diese Sitzung trägt sie in zwei neuen Abschnitten nach:
- jede Regel wortgleich aus der Antwort des Prüfers kopiert und gegen das Original geprüft;
- dazu, was gemessen wurde und in welchem Auftrag es umgesetzt ist;
- an den alten Stellen im Regelwerk ein kurzer Hinweis „siehe Abschnitt 41/42“.

Am Programmcode ändert sich nichts. Die Liste der geschützten Dateien bleibt unberührt, deshalb ist kein neues Schutzabbild nötig. Die drei noch offenen Anfragen an den Prüfer kommen später in einen eigenen Abschnitt 43.
