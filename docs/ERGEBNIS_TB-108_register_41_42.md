# TB-108: Ergebnis. Register 41 und 42 eingetragen — 67 Einträge aus Fable 24b bis 25c und die Tatsachennotizen TB-103 bis TB-107, 108 Zitate mit `diff` rc 0, 20 Marken am alten Ort, numstat 1134/0; Sonde vorher = nachher; keine `.py` geändert

**Sitzungstitel:** `TB-108` · **Stand:** 25.09.2026, ca. 23:15 · **Auftrag:**
`docs/auftraege/MAC_TB-108_register_41_42.md` · **Belege:** `docs/belege/TB-108/`
**Eingang:** `f61bd97`. Commits: `4a84086` (Schritt 0), **`f4d3e2a` (Abschnitt 41, 42 und alle
Marken in einem Commit)** und der Abgabe-Commit (Belege, dieses Dokument, Journalblock DG).
**Grundlage:** Stoffsammlung `docs/projektfuehrung/STOFFSAMMLUNG_REGISTER_41_42.md`; Fable 24b, 24c,
24d, 25a, 25b, 25c. Freigabe des Betreibers 25.09.2026, 22:34 (Auswahlkarte, wörtlich im Auftrag).
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Arbeitsbaum wie erwartet (7 Dateien, `4a84086`). HEAD `f61bd97`, Register 7993 Zeilen, `register()` `0ece95e2…`, Sonde 25/0/0 und (ii) 0 — alles gleich dem Soll. Alle sechs Quellen versioniert |
| **A** | Jeder Eintrag der Stoffsammlung hat seine Fundstelle (`a_eintraege.txt`). **Ein** Eintrag ohne zitierbaren Text (E7), als eigene Fassung gekennzeichnet. **Fünf Abweichungen** zur Vormessung, die wichtigste: **H6 ist bis heute nicht eigenständig** (A3 unten) |
| ⭐⭐ **B/C** | **Abschnitt 41** (24b A1–A12, 24c B1–B8, 24d C1–C9) und **Abschnitt 42** (25a D1–D12, 25b E1–E8, 25c F1–F8, Tatsachennotizen G1–G10, Hash-Übergänge seit 39.5, Offenes, Nicht-Getanes). Jede Kette mit beiden Fassungen und Verweis. **20 Marken** an 19 Stellen, keine in Abschnitt 10 |
| ⭐ **D1** | `numstat` des Register-Commits **1134 / 0** |
| ⭐ **D2** | **108 Zitate** (81 ganze Zeilen, 27 Teilzitate), **108 × `diff` rc 0** |
| ⭐ **D3** | Sonde gegen `40ffe18d…` nach dem Commit: **Pfad-Bestandteile 25/0/0, Prüfung (ii) 0** — zeichengleich wie vorher bis auf die angezeigten Zeilennummern des Listentexts (868–981 ⇒ 894–1007) |
| **D4** | `register()` `0ece95e2fd4f5bd2787ea40f6a12988aadb0a414c5132553522b55000c6052d7` ⇒ **`c85dd6c3b6de7a302627f84244226b9ba1ad5e22d6a8cc260cc5c48b588c12e2`** (erwartet: die Registerdatei ist Teil). ⚠️ Der neue Wert kann **nicht** als letzte Zeile in 42.5 stehen — er hinge von sich selbst ab |
| **D5** | `test_vorregistrierung` am Register-Commit **196/196, rc 0** (911 s) |
| **D6** | `registerbericht.py --pruefen` rc **1** („der erzeugte Block steht nicht woertlich im Register") — wie seit vor TB-106 |
| **D7** | Geändert: nur das Register und `docs/`. Alle 1538 versionierten Dateien ausserhalb `docs/` gleich, Snapshot, Datenstand `d9449faf…`, `ergebnisse/` gleich. Eine `*.db` hat der Aktien-Cron um 22:50 geändert |

---

## 0. Schritt 0

| | |
|---|---|
| 0a | Sieben Dateien des steuernden Chats committet (`4a84086`); der Arbeitsbaum entsprach genau der Tabelle des Auftrags |
| 0b | Keine `.git/*.lock`. HEAD am Eingang `f61bd97`. Register 7993 Zeilen, letzter Commit `d0dc890` (463/0). `register()` `0ece95e2…`. Sonde gegen `sperrliste_abbild_2026-09-25b.json` (`40ffe18d…`): Pfad-Bestandteile 25/0/0, (ii) 0, rc 2 nur NICHT PRÜFBAR. Hashes vorher mit `hashes.sh` (Vorlage TB-107) in `0_hashes_vorher.txt`, `5_alle_vorher.txt` |
| 0c | Alle sechs `FABLE_ANTWORT_…` (24b, 24c, 24d, 25a, 25b, 25c) liegen versioniert im Repo. Die Herkunftsnotiz (abgeschrieben, nicht bytegeprüft gegen die Ablage) steht in 41.0 |

Beleg `0_schritt0.txt`.

## 1. Block A — Vorbereitung und Messung

**A1** — Für jeden Eintrag A1–A12, B1–B8, C1–C9, D1–D12, E1–E8, F1–F8, G1–G10 die Quellstelle
gefunden; je Eintrag Quelle mit Zeilen, Art, Stand und Markenort in `a_eintraege.txt`. Zusätzlich
eingesetzt: Fables eigene Liste je Antwort (24b Z. 119, 24c Z. 70, 24d Z. 91, 25a Z. 108, 25b Z. 90)
und Fable 23f zum „benannten Abstand" (41.0).

**A2 — Einträge ohne zitierbaren Text:**
- (a) **A7** „Testrahmen-Notiz" ist in der Stoffsammlung nur Stichwort (24b D5); der Text steht in derselben Antwort, 24b C4 (Z. 107) — eingesetzt.
- (b) **E7** „Tatsachennotizen TB-104" nennt Fable nur als Stichworte (25b Z. 100) — **eigene Fassung der Sitzung**, so gekennzeichnet, mit dem einen ausformulierten Satz aus 25b Z. 19 als Teilzitat.
- Dazu, gekennzeichnet: die Tatsachennotiz zu 5.4 bei **C4** in eigenen Worten neben Fables Absatz, und **G1–G10** (Sitzungsfakten, ihrer Natur nach eigene Fassung).
- (c) **Zahl: 1** Eintrag ohne zitierbaren Text (E7).

**A3 — Stand nachgemessen** (`a3_stand.sh` → `a3_stand.txt`, `c_hashuebergaenge.txt`). Alle Commits
und Hashes der Stoffsammlung stimmen. **Abweichungen — es gilt die Messung:**

| | Stoffsammlung | gemessen |
|---|---|---|
| 1 | A4: Regel „jede Mutationsprobe beisst allein" „seit TB-105 in jedem Auftrag angewandt" | ⚠️⚠️ Für **neue** Proben ja. **H6 selbst ist bis heute nicht eigenständig**: TB-97 hat gemessen, dass H6 nur zusammen mit H5 trägt; seit `ae8db0b` (TB-97) nicht umgebaut; der Test sagt es im Kommentar (Z. 861/965). ⇒ „sieben" (A1/A2) steht unter Vorbehalt; eingetragen als offen (41.1 A4, 42.6 (8)) |
| 2 | 42.5 soll die Übergänge aus **TB-104 und TB-106** nennen | Es gibt einen **dritten** an einem gesperrten Pfad: `messgroessen.py` (TB-103, `ae136fd`, `623f8d77…` → `59b396e7…`), auf keinem Punkt, aber in `EINGEFROREN` (nach 39.7 gesperrt). Freigegeben war er. In 42.5 aufgenommen und gekennzeichnet |
| 3 | A7 nur Stichwort | Text in 24b C4 gefunden (A2 (a)) |
| 4 | D3 und D7 als zwei Einträge | Derselbe Text (25a Z. 61) — einmal eingetragen, als D3/D7 |
| 5 | D4 „alt und neu als letzte Zeile in 42.5" | Selbstbezug: `register()` hasht die Registerdatei; ein Wert im Register ändert ihn. 42.5 nennt den alten Wert voll und verweist für den neuen auf dieses Dokument und `h1_hashes_nachher.txt` |

Weitere Messungen, die die Vormessung bestätigen oder schärfen: Ladeprotokoll-Teil (4) weiter offen
(`shared/ladeprotokoll.py` seit `55b991d`, TB-45, unverändert); `pruefe_einbau()` heute `vollstaendig:
True`; `ARBEITSBAUM_PFADE` unverändert (Z. 225); `registerdaten.py:605` vergleicht den Bedingungstext
weiter selbst; `MINDESTTRAINING_JAHRE` ohne Leser; Laufbereichsliste 84 Zeilen, davon 3 unter `docs/`
⇒ 81 Module; `herkunft_protokoll.jsonl` existiert nicht; `register()` je Commit seit `4faef05`
nachgebaut, Probe am Eingang gleich dem gemessenen Wert. **G5** („12 Stellen") nicht nachgezählt —
im Register ohne Zahl.

⚠️ **Eine Zahl bewusst weggelassen:** Übergabe 25.09. Block 7 Nr. 4 rügt die Positionenzahl von
`t3_supertrend` in Anfragen (27.1). Sie steht in 15.4 schon; im neuen Text steht sie nicht.

**A4 — Zielabschnitte gelesen** vor jeder Marke: 5.1, 5.4, 6, 11.1–11.3, 12, 15.4, 16.6, 19, 23.5,
33.3, 35.4, 36.5, 37.3, 37.4, 39.6, 39.7, 39.8, 40.6, 40.7; dazu 39.5 und 40 als Form, Abschnitt 10
(keine Marke).

## 2. Block B und C — die zwei Abschnitte

Eingesetzt mit `eintrag_register_41_42.py` (Bauart TB-96, mehrere Quellen): Zitate aus den
Quelldateien eingesetzt, nie abgetippt; jede Marke hinter einer Ankerzeile, die in ihrem
Zielabschnitt genau einmal vorkommt; Wachen für die Leser des Registers (`G6`-Muster genau einmal;
„ERSETZT durch Abschnitt 15", `| **730** |`, die Kopfzeile von Abschnitt 10 und die ERZEUGT-Marken
gleich oft wie vorher; jede alte Zeile in derselben Reihenfolge). Vorher ein **Probelauf gegen eine
Kopie** mit Zitatprüfung und Sonde; dann einmal gegen das Register.

| Abschnitt | Inhalt |
|---|---|
| **41.0** | Anlass (benannter Abstand, Fable 23f), Gliederung als Vorschlag des steuernden Chats und Betreiberentscheidung 22:34, **von Fable nicht entschieden**; Herkunftsnotiz der Quellen; Bauart |
| **41.1** | 24b: A1–A12 (sieben Mutationsproben, „alle sieben", TB-90-Satz, allein beissen **mit H6 offen**, Störproben, zwei Leser ein Parser, Testrahmen, `bot_lauf.py`, keine Kennzeichnung, kein Fallback, Tag-Vorbedingung, Signalpfad) |
| **41.2** | 24c: B4, B8, B5, B1, B2 (**zurückgenommen**, mit Grund), B3, B6/B7 |
| **41.3** | 24d: C1–C9; C9 mit der Messung (Lesehaken seit TB-92, das Register hatte recht, Fehler des steuernden Chats) |
| **42.1–42.3** | 25a D1–D12, 25b E1–E8, 25c F1–F8; F8 (Ausnahme von 19) steht damit **vor** dem 19-Auftrag im Register |
| **42.4** | G1–G10 und `f5fdb53` (revertierbar) |
| **42.5** | Neun Hash-Übergänge mit vollen Hashes, Auftrag, Freigabe, Punkten; die zwei Abbilder; `register()` je Commit seit `4faef05` |
| **42.6 / 42.7** | Was offen bleibt (12 Zeilen) / was nicht getan wurde, mit der Markenliste |

**Die Ketten** (beide Fassungen, die frühere „⭐ BERICHTIGT durch …", die spätere „berichtigt …"):
B2 → C1/C2 · B5 → D1 · B8 („TB-91") → C8 · C5 → D5 · D5 → E3 · D8 → E5 · D6 ergänzt durch E1, E2,
F7, F8 · D3/D7 präzisiert durch E6 · E8 beantwortet durch F1, F2, F4, E4 · 37.4 → F2 (Marke). Alle
acht Zeilen der Kettentabelle des Auftrags sind abgebildet.

**Die Marken** (20, an 19 Stellen): 5.1 Nr. 4 · 5.4 · 6 · 11 (Ende, in 11.3) · 12 · 15.4 · 16.6 ·
19 (zweimal) · 23.5 · 33.3 · 35.4 · 36.5 · 37.3 · 37.4 · 39.6 · 39.7 · 39.8 · 40.6 · 40.7.

## 3. Block D — Nachweise

| | Soll | Ist | Beleg |
|---|---|---|---|
| **D1** | numstat zweite Spalte 0 | **1134 / 0** (`f4d3e2a`) | `d1_numstat.txt` |
| **D2** | Zahl der Zitate = Zahl der rc 0 | **108 = 108** (81 Zeilen, 27 Teile); an der Probe vorher ebenso | `d2_zitate.py`, `d2_zitate.txt`, `zitate.json` |
| **D3** | Sonde 25/0/0, (ii) 0, wie vorher | **25/0/0, (ii) 0**, Ausgabe gleich bis auf „Z. 868-981" ⇒ „Z. 894-1007" (26 Markenzeilen vor Abschnitt 10; die Sonde vergleicht den Hash des Listentexts, die Zeilen sind Anzeige) | `0_sonde_vorher.txt`, `d3_sonde_nachher.txt` |
| **D4** | `register()` ändert sich | `0ece95e2…` ⇒ **`c85dd6c3b6de7a302627f84244226b9ba1ad5e22d6a8cc260cc5c48b588c12e2`**; einziger geänderter Teil ist die Registerdatei (`10ffa7b3…` ⇒ `ed20408c269e283efb2af42141c5a3390fcdbcdb68645b791313e16d13a351b1`) | `h1_hashes_nachher.txt` (9) |
| **D5** | 196/196 | **196/196, rc 0**, 911 s, am Stand `f4d3e2a` (die Parser des Registers, u. a. `G6`, treffen weiter) | `d5_test_roh.txt` |
| **D6** | Ausgang festhalten | rc 1, „die Zahlen dort sind veraltet" — unverändert gegenüber TB-106 | `d6_registerbericht.txt` |
| **D7** | nur Register und `docs/` | `5_alle_vorher.txt` = `5_alle_nachher.txt` (1538 Dateien ausserhalb `docs/`, diff rc 0); Snapshot, Datenstand, `ergebnisse/` gleich; `paper_trading_volatility_breakout.db` geändert **22:50:45** durch den Aktien-Cron (22:50), nicht durch diese Sitzung | `h1_vergleich.txt` |

## 4. Für Fable ⭐⭐

*Ohne Kontext lesbar.* Das Register trägt jetzt deine Einträge aus 24b bis 25c zeichengleich (mit der
Datei im Repo; ob diese mit deiner Ablage zeichengleich ist, ist nicht gemessen — 41.0).

**(1) Die Gliederung 41/42 ist nicht deine.** Der steuernde Chat hat sie vorgeschlagen, der Betreiber
gewählt: 41 = 24b, 24c, 24d; 42 = 25a, 25b, 25c und die Tatsachennotizen TB-103 bis TB-107. 25d, 25e,
25f kommen in 43. Du kannst widersprechen.

**(2) Wo was steht:**

| Register | Quelle |
|---|---|
| 41.1 A1, A2 | 24b B2 (Berichtigung zu 12 und 40.7) |
| 41.1 A3 | 24b C1 (Berichtigung zu 40.6, TB-90-Satz) |
| 41.1 A4 | 24b B3 (allein beissen, H6) |
| 41.1 A5 | 24b C2 (Störproben) |
| 41.1 A6 | 24b B4 (zwei Leser, ein Parser) |
| 41.1 A7 | 24b C4 (Testrahmen) |
| 41.1 A8, A9 | 24b A3 (`bot_lauf.py`, keine Kennzeichnung) |
| 41.1 A10, A11 | 24b A2 (kein Fallback; Tag-Vorbedingung) |
| 41.1 A12 | 24b A3 (Signalpfad, Präzisierung zu 40.6) |
| 41.2 B4, B8 | 24c 1 (zwei Teile; TB-93/TB-102 = 2) |
| 41.2 B5 | 24c 2 (Resolver-Pflicht) |
| 41.2 B1, B2, B3, B6/B7 | 24c 4 (Reichweite 5.4; Purge-Berichtigung, zurückgenommen; Donchian; Folge für die Eingabedateien) |
| 41.3 C1–C5 | 24d 1 und 2 (Rücknahme; Deckel; Bedingung beim Gewinner; `elliott_wave`; `purge_tage`) |
| 41.3 C6–C9 | 24d 3 (Modus-Lauf = Resolver; Hilfsordner-Läufe; TB-92 A1b; Lesehaken) |
| 42.1 D1–D12 | 25a (Fundstelle; drei Klassen; vier Teile; Tag-Commit; 33.3/35.4; Laufbereich; TB-103; Lesehaken; `manuelle_eingriffe.log`; vier Rückfälle) |
| 42.2 E1–E8 | 25b 3 und 2 (Klasse (iv); Klasse „Code" und 19; Plan-Feldliste; Verfahren-A-Reste; Laufbereich als Vereinigung; Stichtag; TB-104; offene Messungen) |
| 42.3 F1–F8 | 25c (Abschnitt 6; 37.4; 11; `_min_history` und Erzeugerkette; Ersatzmodule; `getattr`; Caches; registrierte Protokolle) |

**(3) In eigener Fassung (kein Wortlaut von dir):** E7 (Tatsachennotizen TB-104 — du hast nur
Stichworte genannt) und die Tatsachennotiz zu 5.4 bei C4 (neben deinem Absatz). Bitte prüfen.

**(4) Nicht gesetzte oder verlegte Marken:**
- **Abschnitt 10:** keine Marke (die Sonde vergleicht dessen Listentext). F3 (Schlusssatz zu 11) und F8 (10.1) stehen deshalb im Text von 42.3.
- **38.x:** keine Marke — der Modus-Nachweis wird in 39.6 geführt; dort steht sie.
- **Zusätzlich zur Liste des Auftrags gesetzt**, jeweils nach Lesen des Zielabschnitts: 15.4 (die Deckelzeile `t3_supertrend` stammt aus ausgeführten Positionen), 23.5 (die Zeile zu `MINDESTTRAINING_JAHRE` beschrieb einen Stand vor TB-106), 37.3 (Verweis auf 42.5, wie 39.5 es hielt), 39.7 („`herkunft.py` unverändert" ist Stand TB-94).

**(5) Abweichungen gegenüber der Vormessung** — Tabelle A3 oben. Für dich wichtig: **H6 ist nicht
eigenständig.** Nach deiner Regel aus 24b B3 heisst das bis zum Umbau „sechs plus ein Paar", nicht
„sieben". Eingetragen ist deine Berichtigung („sieben") mit diesem Vorbehalt; eine Folgeberichtigung
wäre deine Sache.

**(6) Nicht in der Stoffsammlung, deshalb nicht eingetragen** (Handwerk oder Regeln an dich selbst):
24b A4 (`faltenplan_neun.py` kein zweiter Ort), 24b B5 (Abbild nach dem Bündel), deine Regeln an dich
(24b C1, 24d 2), 25a 1 (2) (Prüfung „keine Achsenliste nennt `max_hold_*`", von dir als Vorschlag
bezeichnet), 25a 3 (C) Messbitte `makedirs` (beantwortet TB-104/105), 25a 4 zu `herkunft.py` (überholt
durch 25b/25c). Sag, wenn eines davon ins Register gehört.

## 5. Für die Folgesitzung vorbereitet

- **Abschnitt 43** (25d, 25e, 25f): Bauart dieses Auftrags wiederverwenden — `eintrag_register_41_42.py` (Platzhalter `⟦Z:q:n⟧`/`⟦T:q:n|…⟧`, mehrere Quellen, Probelauf über `TB108_PROBE=<kopie>`), `d2_zitate.py` (Bereiche je Abschnitt), `a3_stand.sh`, `hashes.sh`.
- **`register()` je Commit nachbauen:** `c_hashuebergaenge.py` erzeugt Übergänge und `register()`-Kette ohne Checkout; am HEAD nach dem Register-Commit ergibt es `c85dd6c3…` = gemessener Wert (`c_hashuebergaenge_nachher.txt`).
- **Der 19-Auftrag** kann sich auf 42.3 F8 stützen (Ausnahme registrierte Protokolle steht vorher im Register).
- **H6** (42.6 (8)) vor dem Tag: eigener Fehler oder Paar.
- Die Zeile **TB-100** in `AKTUELLER_AUFTRAG.md` ist als „aufgegangen in TB-108" vermerkt (steuernder Chat).

## 6. In einfacher Sprache

Das Regelwerk des Auswahllaufs hatte zwei Tage lang nicht mit dem Code Schritt gehalten: Der
Verfahrensprüfer hatte in sechs Antworten gut sechzig Regeln, Berichtigungen und Notizen benannt, die
Programme waren danach gebaut, im Regelwerk standen sie noch nicht. Diese Sitzung hat sie in zwei neuen
Abschnitten nachgetragen — jede Regel aus der Antwort des Prüfers hineinkopiert und 108-mal gegen das
Original verglichen, dazu, was gemessen ist und in welchem Auftrag es umgesetzt wurde. An neunzehn
alten Stellen steht jetzt ein kurzer Hinweis „siehe 41/42"; kein alter Satz ist geändert.

Zwei Dinge sind beim Nachmessen aufgefallen: Eine der Testproben (H6) schlägt bis heute nur zusammen mit
einer anderen an — das Regelwerk sagt jetzt ausdrücklich, dass das vor dem Stichtag zu beheben ist. Und
eine geschützte Datei war schon einen Auftrag früher geändert worden, als die Liste es vorsah; das steht
jetzt mit allen Prüfsummen im Regelwerk. Am Code hat sich nichts geändert, die Schutzprüfung zeigt
dasselbe wie vorher.
