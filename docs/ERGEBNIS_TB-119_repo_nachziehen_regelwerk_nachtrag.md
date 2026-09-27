# TB-119: Ergebnis. Repo nachgezogen und Regelwerk-Nachtrag nach Fable 27b Teil E — 15 gesicherte Dateien committet, `UEBERGABE.md` Z. 99 nach 27.5 und Stand 27.09.; ARBEITSWEISE 23 „Projektablage“ und zehn weitere Stellen aus Teil E; 13 Regeln aus D2

**Sitzungstitel:** `TB-119` · **Stand:** 27.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-119_repo_nachziehen_regelwerk_nachtrag.md` · **Belege:** `docs/belege/TB-119/`
**Eingang:** `2a0893b` (Abgabe TB-118). Commits: `7eadc7a` (Schritt 0), `4c1650d` (A1), `6126c64` (A2), `df825b6` (B),
`8c6ab75` (C), der Abgabe-Commit (D: dieses Dokument, Journal DR). Nach jedem Commit gepusht.
**Grundlagen:** `FABLE_ANTWORT_2026-09-27b_konzept_projektwissen.md` md5 `ad35734f99414c982741b0c3f5b27862` ✔ (geprüft
in 0a), `ERGEBNIS_TB-118` Abschnitte 8 und 9, `docs/belege/TB-118/d2_fehlende_regeln.txt`.
**Freigabe** (wörtlich im Auftrag): 27.09.2026, 18:08, Chat, und ca. 18:25, Auswahlkarte „Was soll bis Dienstag ohne
Fable laufen?“ ⇒ „Wir arbeiten alles strukturiert ab“.
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Kein Abbruchkriterium ausgelöst. **Rückfragen an den Betreiber:
keine.** **Sichtschutz 27.1:** Dieses Dokument enthält keine Ergebnisgrösse des Selektionsraums und keine Erwartung
über den Ausgang; Treffer sind nach 27.5 nur mit Fundstelle genannt.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | 16 md5 = Auftrag (15 Dateien + Antwort 27b), keine weitere Datei ⇒ 17 Dateien committet (`7eadc7a`). Ausgang HEAD `7eadc7a`, Register `18e39ee2…`. db-Sicherung 12/12 rc 0 |
| **A1** | Z. 99 ersetzt; `grep -c` auf den alten Wert **0**; md5 **`2b61283b190a3a90069207b2b3226758` = Soll** (Ablagefassung) |
| **A2** | Block `## Stand 27.09.2026 (TB-119)`, jede Zahl am HEAD gemessen: **keine Abweichung** von den Erwartungen des steuernden Chats |
| ⭐⭐ **B** | 11 Stellen aus Teil E in 3 Dateien (ARBEITSWEISE 7b, 8, 15, **neu 23**; UMZUG 1, 2, Schritt 3, Schritt 4; DOKUMENTATIONSSTANDARD 6, 9 zweimal). numstat 125/0 · 34/11 · 15/4; jede entfernte Zeile wörtlich in `b_stellen.md`. Drei offene Punkte (`b_offen.txt`) |
| ⭐⭐ **C** | **13 Regeln** eingetragen: ARBEITSWEISE 14 (3), 15 (6, davon 21/6 als Verweis auf 27.5), PRUEFPRINZIPIEN **A9, A10, B7, C8** (4). numstat 37/0 · 53/0. 19/6 als Frage in die Fable-Sammlung, Abschnitt D (**29/0**). `c_offen.txt`: keine offen |
| **Durchgehend** | Register sha256 vorher = nachher `18e39ee2…` · Datenbanken 12/12 sha256 gleich wie 0c · 0 Dateien ausserhalb `docs/` geändert |

---

## 1. Schritt 0 — Sicherung und Ausgang

**0a.** `git status --short` zeigte genau die 17 erwarteten Dateien (`AKTUELLER_AUFTRAG.md` geändert, 16 neu). Die 15
gesicherten Dateien und die Antwort 27b per `md5 -r` geprüft: **alle 16 gleich dem Auftrag**. Commit
`TB-119 Schritt 0: 15 gesicherte Dateien, Auftrag, Zeiger` = `7eadc7a`, gepusht.

**0b.** `0b_ausgang.txt`: HEAD `7eadc7a`; ARBEITSWEISE 2053 Zeilen, UMZUG 361, DOKUMENTATIONSSTANDARD 278,
PRUEFPRINZIPIEN 387, UEBERGABE 259 (je mit sha256); Überschriften `^## ` von ARBEITSWEISE (höchste **22**);
Register sha256 `18e39ee29b9bd4f03a2ad4953c85c2e59558de3aaab26844ae58fb7590fca93c`.

**0c.** `db_sicherung.sh` ins iCloud-Ziel: 12 von 12 gesichert, `docs.tar.gz` (Commit `7eadc7a`, 1596 Dateien =
`git ls-tree`, `gzip -t` ok), rc 0. sha256 der Originale in `0c_db_sicherung.txt`.

## 2. Schritt A — `UEBERGABE.md`

**A1** (`4c1650d`): genau die eine Ersetzung in Z. 99. Nachweis `a1_nachweis.txt`: `grep -c` auf den alten Wert = 0,
md5 = `2b61283b190a3a90069207b2b3226758` (Soll), numstat 1/1.

**A2** (`6126c64`): Block angehängt, numstat 18/0. Gemessen am HEAD `4c1650d`:

| Grösse | gemessen | Erwartung | |
|---|---|---|---|
| Register, höchster Abschnitt | 46 (10 347 Zeilen), sha256 `18e39ee2…` | 46 | ✔ |
| Abbild `sperrliste_abbild_2026-09-26_tb117.json` | sha256 `46f0ad5d1d83…` | `46f0ad5d…` | ✔ |
| Sonde dagegen | 37/0/0, `eingefroren` 22, Mengenvergleich 22/22, rc 2 (nur die zwölf Regel-Bestandteile, wie `ERGEBNIS_TB-117` Z. 163) | 37/0/0, 22 | ✔ |
| `herkunft.py` / `auswertung.py` / `sperrlistensonde.py` | `c6c13388…` / `8ec45123…` / `98c02e0e…` | — | gemessen |
| Fable | 27a, 27b Antwort im Repo; 27c nur Anfrage | 27c offen | ✔ |

⭐ **Die Sonde nur laufen lassen, wenn sie nichts schreibt:** ihr Kopf sagt „Sie schreibt nichts“; im Code kein
Schreibaufruf, einziger Unterprozess `git rev-parse HEAD`. Zusätzlich `git status --porcelain` vor und nach dem Lauf
gezählt: 2 = 2 (`a2_sonde.sh`, `a2_sonde.txt`). Die Zeile „Projektablage“ (148 → 40 Dateien, 79 % → 32 %) hat der
steuernde Chat gemessen; die Sitzung sieht die Ablage nicht — so im Block vermerkt.

## 3. Schritt B — Regelwerk nach 27b Teil E (`df825b6`)

Werkzeug `b_einsetzen.py` (mit `einsetzen_lib.py`): exakte Ersetzung, je Stelle genau ein Treffer, erst `--probe`
(„11 Stellen, alle eindeutig“), dann der Lauf; danach `--nur-protokoll HEAD`: **Basis + Ersetzungen bytegleich mit dem
Arbeitsbaum** (3 × ja). Protokoll `b_stellen.md`: je Stelle die ganze Zeile davor und danach und jede entfernte Zeile
wörtlich.

| Dokument | Stelle | Umsetzung | entfernt |
|---|---|---|---|
| ARBEITSWEISE | **neu 23** „Die Projektablage — Arbeitsfläche, nicht Träger“ | 23.1 G1–G8, 23.2 Klassen B1–B8 (Ort, Eintritt, Austritt), die zwei offenen Lesarten, 23.3 Soll-Skript (C1, Reihenfolge C4), 23.4 Schwellen und Routine (C2). **Nummer gemessen:** höchste vorhandene 22 | 0 |
| ARBEITSWEISE | 15 | Indexpflicht `FABLE_DIALOG_INDEX.md`, direkt nach „abgelegt wie seine Antwort“ (27b G4) | 0 |
| ARBEITSWEISE | 8 | Füllstandszeile der Wochenrückmeldung | 0 |
| ARBEITSWEISE | 7b | Unterabschnitt „Die tägliche Sicherung nach iCloud — auch `docs/`“: „db-Sicherung sichert zusätzlich `docs/` als `docs.tar.gz`“ | 0 |
| UMZUG | 1 | `UEBERGABE.md` ohne Datum, Vorgänger im Repo | 2 |
| UMZUG | 2 | Träger: Repo (Mac + GitHub), iCloud-Kopie; die Ablage ist Arbeitsfläche (eigener Absatz statt Tabellenzeile) | 2 |
| UMZUG | Schritt 3 | `UEBERGABE.md`, fortgeschrieben statt neu angelegt | 1 |
| UMZUG | Schritt 4 | „In die Projektablage schreiben“ → Soll/Ist-Abgleich mit `ablage_soll.py`, Füllstand messen | 6 |
| DOKUMENTATIONSSTANDARD | 6 | Träger neu bestimmt (G1); `logs/auftraege/` unverändert kein Träger | 3 |
| DOKUMENTATIONSSTANDARD | 9 | „gilt ausdrücklich auch für die Ablage“; Ausnahme „Backlog-Abschnitt 8“ → `BACKLOG_ERLEDIGT_2026-09.md`, Abschnitt 8 | 1 |
| PRUEFPRINZIPIEN, Register | — | keine Änderung (B4) | — |

**Die drei Abweichungen vom Wortlaut von Teil E, wie vom Betreiber entschieden, sind umgesetzt:**
`BACKLOG_ENTSCHEIDUNGEN.md` statt `ENTSCHEIDUNGEN.md` (in 23.2 und im Kopf von 23 genannt) · 7b mit `docs.tar.gz`,
nicht `git bundle` · Abschnittsnummer 23 gemessen. Die bei Fable offenen Lesarten stehen in 23.2 so, wie
`ablage_soll.py` arbeitet, mit „Lesart offen, Fable-Sammlung B4“ bzw. „B5“.

**Entfernt wurden nur Sätze, die Teil E ausdrücklich ersetzt** — 15 Zeilen, alle in `b_stellen.md`. numstat
(`b_numstat.txt`): ARBEITSWEISE 125/0, UMZUG 34/11, DOKUMENTATIONSSTANDARD 15/4.

**Offen (`b_offen.txt`), nicht geraten:** keine Stelle aus Teil E unauffindbar. Offen sind eine Lesart und zwei
Folgestellen, die Teil E nicht nennt, siehe Abschnitte 6 und 7.

## 4. Schritt C — 13 Regeln aus D2 (`8c6ab75`)

Wortlaut jeder Regel an der Fundstelle in der Übergabe gelesen (`UEBERGABE_2026-09-19.md` Z. 181 ff., 577 ff., 684 ff.,
790 ff., 1118 ff.; `UEBERGABE_2026-09-24.md` Z. 266 ff.), nicht aus der Kurzfassung übernommen. Jede Regel trägt
Übergabe, Block, Nr. und die D2-Kennung. Werkzeug `c_einsetzen.py`, Protokoll `c_stellen.md` (0 Zeilen entfernt),
Probe und Bytegleichheit wie in B.

| D2 | Regel (Kern) | Zielort |
|---|---|---|
| 19/5 | Ein Nachweis gilt für den Gegenstand, den er berührt | PRUEFPRINZIPIEN **A9** |
| 24/5 | Weicht die Nachmessung von der Vormessung ab, gilt die Nachmessung | PRUEFPRINZIPIEN **A10** |
| 21/4 | Gleiche Sonde, beide Dateien | PRUEFPRINZIPIEN **B7** |
| 24/4 | Eine Kette ist erst geprüft, wenn alle ihre Eingaben geprüft sind | PRUEFPRINZIPIEN **C8** |
| 21/1, 21/2, 21/3, 21/7, 24/R2 | laufende Aufträge gegen jede Antwort prüfen · Aktenzeichen mit Wortlaut · Fassungszeile im Sendetext · Fables Berichtigung messen · Anfrage erst übergeben als Kopierblock | ARBEITSWEISE 15, Unterabschnitt „Der Austausch mit dem Verfahrensprüfer“, Nr. 1–5 |
| 21/6 | Sichtschutz-Treffer: Fundstelle statt Inhalt — **nur Verweis auf Registertext 27.5**, Text nicht wiederholt | ebd., Nr. 6 |
| 21b/1, 21b/5, 24/6 | vor dem Schreiben lesen · Nachtrag wird Auftrag · Hilfsdateien über `device_request_delete_permission` | ARBEITSWEISE 14, Unterabschnitt „Schreiben auf Dateien und Nachträge“, Nr. 1–3 |

**Nummern in PRUEFPRINZIPIEN gemessen** (K2i): höchste vorhandene A8, B6, C7 ⇒ A9, A10, B7, C8; nichts umnummeriert.
**Zählung** (`c_zaehlung.txt`): jede der 13 Kennungen genau einmal in den hinzugefügten Zeilen; eine 14. Kennung (19/7)
steht nur als Verweis in der Anmerkung zu Nr. 1 in ARBEITSWEISE 14 und ist nicht eingetragen (C3).

**19/5 und 24/5 — Sinn nach dem Nachlesen eindeutig** (`c_offen.txt`): 19/5 ergibt sich aus dem Fall daneben. Bei 24/5
war in D2 nur der Verweis „A8“ unklar; die Aufträge MAC_TB-96 (Z. 64), -102 (Z. 69), -103 (Z. 54) und -104 (Z. 56)
schreiben „Vormessung … Nach `A8` misst du nach … gilt deine Messung“ — A8 angewandt, kein zweiter Sinn. Der
Hinweis steht in A10.

**C2.** 19/6 nicht eingetragen; an `FABLE_SAMMLUNG_fuer_2026-09-29.md`, Abschnitt D, angehängt: Eintrag „27.09.,
TB-119: D2 19/6 gegen ARBEITSWEISE 6d“, beide Wortlaute mit Fundstelle, der Hinweis zu K2h („in ARBEITSWEISE §7c“,
dort nichts; `grep` vier Treffer, keiner mit „fragen“), die Frage. **numstat 29/0.**

**C3.** Die acht Regeln mit Status TEILWEISE bleiben unverändert (Fundstellen aus D2, Zeilen am Stand `3018657`):

| D2 | Kern | Fundstelle nach D2 |
|---|---|---|
| 19/2 | vor jeder Folgerung aus einem Zeitstempel `date -u` gegen Ortszeit | ARBEITSWEISE 7 (Z. 1049), nur für DB-Abweichung gegen Cron |
| 19/3 | ein Name ist kein Messwert; jeder Satz: gemessen oder erschlossen | ARBEITSWEISE 0 (nur für Aufträge), Z. 643 als Verweis |
| 19/7 | nie überschreiben, neuer Dateiname, danach `wc -c`/`grep` | UMZUG Z. 130; PRUEFPRINZIPIEN D6 nur für `git pull` |
| 19/K | ein Messergebnis gegen eine zweite, unabhängige Zählung | PRUEFPRINZIPIEN C2, nur für Parser |
| 21/5 | voller Pfad, nie der blosse Name | ARBEITSWEISE 0/1, für Anleitungen |
| 21b/4 | append-only kennt kein „noch frisch“ | ARBEITSWEISE 22 (Z. 1826), Zusatz fehlt |
| 24/1 | vor jeder neuen Abschnittsnummer die vorhandenen messen | K2i über ARBEITSWEISE 15, für Abschnittsnummern nicht ausdrücklich |
| 24/7 | nach jedem Ablegen md5 und `wc -c` auf beiden Seiten | UMZUG Z. 130 (`cmp -s` je Datei) |

## 5. Schlussmessung (`d_schluss.txt`)

| | |
|---|---|
| Datenbanken | 12/12 sha256 gleich wie 0c |
| Register | sha256 `18e39ee2…` = 0b |
| numstat `7eadc7a..8c6ab75` | ARBEITSWEISE 162/0 · UMZUG 34/11 · DOKUMENTATIONSSTANDARD 15/4 · PRUEFPRINZIPIEN 53/0 · UEBERGABE 19/1 · Sammlung 29/0 · Register 0/0 |
| ausserhalb `docs/` | 0 Dateien |
| `git status --porcelain` nach dem letzten Commit | in der Abgabemeldung der Sitzung — nach dem letzten Commit gemessen, kann es in keinem Commit stehen |

## 6. Für Fable (am Dienstag in die Sammlung)

1. **Lesart „Erinnerung als Träger“** (`b_offen.txt` 1): G1 und Teil E nennen als Träger nur Repo (Mac + GitHub) und
   die iCloud-Kopie; die Erinnerung nennen sie nicht. Umgesetzt ohne Entscheidung: in UMZUG 2 bleibt die Zeile
   „Erinnerung“ stehen (dadurch stimmt „Die drei Träger“ weiter); in DOKUMENTATIONSSTANDARD 6 wurde sie zum Satz „trägt
   kein Dokument, sondern wie gearbeitet wird“. Ist das gemeint?
2. **Drei Stellen ausserhalb von Teil E nennen die Ablage weiter einen Träger** (`b_offen.txt` 2): ARBEITSWEISE 10
   („Die drei Sätze“, Satz 2), ARBEITSWEISE 15 (Tabelle „Die Träger …“, Zeile „Projektablage“), UMZUG-Einleitung
   (Zeile „Die Anhänge“). Nach G1 nachziehen?
3. **19/6 gegen 6d** — steht bereits in der Sammlung, Abschnitt D (C2).
4. **Kenntnis:** Die 13 D2-Regeln aus 27b/TB-118 sind eingetragen (Abschnitt 4); die acht TEILWEISE bleiben, wie sie
   sind, Entscheidung je Zeile offen (D2-Vorschlag).

## 7. Für den steuernden Chat

- ⭐ **In die Ablage (B1/B2: nach jeder Änderung neu ablegen, gleicher Name)** — md5 und Bytes am HEAD `8c6ab75`:

  | Datei | md5 | Bytes |
  |---|---|---|
  | `projektfuehrung/ARBEITSWEISE.md` | `cb31ae0e4ee1884fdfb6f0bd50e9de42` | 130 716 |
  | `projektfuehrung/UMZUG.md` | `20d173dd6ce791f734678fbe9c446b88` | 21 627 |
  | `projektfuehrung/DOKUMENTATIONSSTANDARD.md` | `dca3606d3b243f06d698aced3b2e890c` | 17 004 |
  | `PRUEFPRINZIPIEN.md` | `a13683e443a28c9d67bc386927906f98` | 21 472 |
  | `projektfuehrung/UEBERGABE.md` | `c5a64f62ee44133b0fd3a8eb17748c93` | 29 858 |
  | `projektfuehrung/FABLE_SAMMLUNG_fuer_2026-09-29.md` | `f290446a2e030611905cb40a7e74bc93` | 7 160 |

  ⚠️ `UEBERGABE.md` weicht jetzt von der Ablagefassung (`2b61283b…`) ab — um den Block A2.
- **UMZUG 6, Eröffnungstext** (`b_offen.txt` 3): nennt weiter `UEBERGABE_2026-09-25.md`; die Tabellenzeile
  „Übergabe-Name“ verlangt, diese Zeile beim Umbenennen mitzuziehen. Teil E nennt UMZUG 6 nicht ⇒ nicht geändert. Ein
  neuer Chat, der den Eröffnungstext befolgt, liest heute den Stand vom 25.09.
- **27.5, nur Fundstelle:** Der Wert, den A1 in `UEBERGABE.md` streicht, steht weiter im Auftrag
  `docs/auftraege/MAC_TB-119_repo_nachziehen_regelwerk_nachtrag.md`, Z. 69 und Z. 73, und im Beleg
  `docs/belege/TB-119/a1_nachweis.txt`, Z. 2 (der verlangte `grep`-Befehl). Belege gehen nach G5 nie in die Ablage;
  ein **offener Auftrag** geht nach B4 hinein — vor dem Ablegen von `MAC_TB-119` prüfen (27.4).
- `AKTUELLER_AUFTRAG.md`: Zeile TB-119 nach Abgabe entfernen (Pflege durch den steuernden Chat).

## 8. Nicht getan, und warum

- Register, Code des Laufs, Sperrliste, Abbilder, `crontab`, Datenbanken: nicht berührt (nicht freigegeben). Die Sonde
  lief nur lesend.
- Die acht TEILWEISE-Regeln: unverändert (C3). D2 19/6: nicht eingetragen (C2).
- Die Folgestellen ausserhalb von Teil E (Abschnitt 6, Nr. 2; Abschnitt 7, UMZUG 6): nicht geändert — der Auftrag
  erlaubt nur die Stellen aus Teil E.
- Nichts im Repo gelöscht, verschoben oder umbenannt. Nichts in der Projektablage (steuernder Chat).

## 9. In einfacher Sprache

Diese Sitzung hat das Repo wieder vollständig gemacht. Die 15 Dateien, die bisher nur in der Projektablage lagen,
sind jetzt committet, jede Byte für Byte gleich wie gesichert. In der Übergabe ist eine Zahl gestrichen, die Fable nicht
sehen soll. Danach war die Datei genau so, wie sie in der Ablage liegt. Dazu steht jetzt der heutige Stand, jede Zahl
gemessen und alle wie erwartet. Dann ist Fables Vorschlag für die Projektablage ins Regelwerk eingezogen: Die Ablage
ist ab jetzt ausdrücklich eine Arbeitsfläche und kein Aufbewahrungsort. Ein neuer Abschnitt 23 sagt, welche Datei
wann hinein und wann wieder heraus kommt, und dass ein Skript ausrechnet, was fehlt und was weg kann. Dazu kamen 13
Regeln aus alten Übergaben, die nirgends mehr standen, zum Beispiel „eine Datei vor dem Überschreiben erst lesen“ oder
„eine Korrektur von Fable wird nachgeprüft wie alles andere“. Eine Regel widerspricht einer bestehenden und liegt
deshalb als Frage für Dienstag in der Fable-Sammlung. Offen ist ausserdem, ob drei ältere Sätze nachgezogen werden
sollen, die die Ablage noch „Träger“ nennen, und ob der Eröffnungstext für einen neuen Chat auf die neue
Übergabedatei zeigen soll. Für dich ist nichts zu tun. Der steuernde Chat legt die geänderten Regelwerksdateien neu
in die Ablage.
