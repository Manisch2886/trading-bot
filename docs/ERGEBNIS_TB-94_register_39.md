# TB-94 — Ergebnis: Der Vollzug von Punkt 8 im Register — Berichtigung 38.4, Abschnitt 39, neues Abbild; ⭐ Plan-Punkt 8 ist fertig

**Sitzungstitel:** `TB-94` · **Stand:** 23.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-94_register_39.md` · **Belege:** `docs/belege/TB-94/`
**Eingang:** `fcc3265` · Commits: `12f6089` (Schritt 0), **`27b68b9`** (Block B und
C in **einem** Commit), **`f65a0a0`** (Block D: Abbild, Ergebnis in 39.9, Belege),
Abgabe-Commit (dieses Dokument, Journalblock CV).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:** Punkt 4 der Sperrliste nennt jetzt **beide** Dateien. Die Pfadzeile
steht additiv unter dem alten Punkttext, die Vollzugsmarke unter dem Kasten
aus 38.4. Registerabschnitt **39** (39.1–39.10) ist eingetragen, dazu **zehn**
Marken am alten Ort. Der alte Satz mit „grün" in 38.4 bleibt zeichengleich und
trägt eine ERSETZT-Marke. `numstat` auf das Register: **575/0** (550/0 und
25/0). **29 Zitate**, alle mit `diff` rc 0. Das neue Abbild heisst
`sperrliste_abbild_2026-09-23.json` (`2f23f76c…`). Die Sonde dagegen meldet
**keinen einzigen Befund**: alle 15 Pfade gleich, (ii) `0`. Ihr Gesamtausgang
ist aber **`2`, nicht `0`**, weil zwölf Punkte Nicht-Dateibezogenes nennen
(siehe D2). `benchmark_drawdowns.json` ist durchgehend `a163c498…`. **Keine
Codedatei geändert, nichts gerechnet.**

---

## 0. Schritt 0 und Freigaben

| | |
|---|---|
| Arbeitsbaum | 3 geänderte und 6 neue Dateien des steuernden Chats → `12f6089` (`ARBEITSWEISE.md`, `LIESMICH.md`, Zeiger, Anfrage 23h, Antworten 23d/23e/23f, Aufträge TB-94/TB-95) |
| ⚠️ Hilfsdatei `_anhang_arbeitsweise_22.md` | Inhalt geprüft: `grep -c "^## 22\. Drei Festlegungen"` → **1**, und der Dateiinhalt ist bis auf die Trennzeilen am Kopf zeichengleich mit dem Schluss von `ARBEITSWEISE.md` (`diff`). ⚠️ **Nicht entfernt:** `rm` hat die Sitzung abgelehnt, `mv` ins Scratchpad der Auto-Modus-Klassifizierer. Einen weiteren Umweg habe ich nicht versucht. **Nicht committet**, sie liegt weiter unversioniert da. ⇒ Der Arbeitsbaum ist **nicht leer**, sondern hat genau diese eine unversionierte Datei. Der Betreiber muss sie von Hand löschen |
| Git-Sperrdateien | `find .git -name '*.lock'` → keine |
| F1 | `FABLE_ANTWORT_2026-09-23f_…` liegt im Repo (in `12f6089` committet) ✔ |
| F2 | 23d und 23e liegen im Repo ✔ |
| F3 | Betreiberfreigabe 21.9: `MAC_TB-92…md` Z. 8, „erteilt 23.09.2026, 18:12" ✔ |
| F4 | 23f Abschnitt 3: „Folgeauftrag, sofort" ✔ |

## 1. Block A — gemessen, bevor geschrieben wurde

| | Ergebnis | Beleg |
|---|---|---|
| **A1** | **Alle zwölf Hashes stimmen mit der Vormessung**, und alle Kürzel ergeben volle Hashes. Die vier Dateien mit vollem Soll-Hash sind zeichengleich. Ergänzend gemessen: `beispieldaten.py` `3e547014…`, `messgroessen.py`, `sperrlistensonde.py`, `sperrliste_abbild.py`. **Die fünf Hash-Übergänge** habe ich aus der Historie neu gebildet (`git show <c>^:` / `<c>:`), alle zwölf Werte sind gleich der Vormessung. Letzter Commit je Datei = der genannte | `a1_hashes.txt` |
| Freigaben in 39.5 | TB-86 „22.09.2026, 07:50", TB-90 „22.09.2026" (Kopf), TB-91 „23.09., 10:40", TB-92 „23.09.2026, 18:12". Alle stehen im jeweiligen `MAC_TB-…md` | grep in der Sitzung |
| **A2** | Sonde gegen `…_2026-09-22.json`: **rc 1**, Befund an **2, 3, 4, 5, 6, 14**, (ii) **0**, Listentext wie bei Erzeugung: ja. Wie erwartet | `a2_sonde_vorher.txt` |
| **A3** | Register **6955** Zeilen, letzter `numstat` `563fb54` **454/0** | `e1_numstat.txt` (Eingang) |
| Zahlen aus TB-91/TB-92 (A8) | 9/77/63/9750, 0 Abweichungen ausser Namen (9/9, `elliott_wave` `2026-2027`), 101 im Selbsttest, 18/18, 56 s, `31008b6` · vier Modus-Läufe bytegleich, 11 Prozesse, 222 + 2, 0 Repo-Zugriffe, zehn Repo-Eingaben (neun Trade-Listen, `messgroessen.json`) plus Log · Zellen 2416. **An den Belegen nachgelesen, alle gleich** | `docs/belege/TB-91/c_*`, `d_*`, `b_neurechnung_lauf.txt`, `docs/belege/TB-92/a1b_*` |

⇒ **Abbruchkriterium 3 tritt nicht ein:** keine Messabweichung.

## 2. Block B — der Vollzug im Punkttext

| | |
|---|---|
| Stelle | `Interpolationsregel**` genau **1**-mal im Register. Die drei Zeilen stehen nach `   Interpolationsregel**` (Z. 870), wörtlich wie im Auftrag. Die vier Zeilen davor sind unverändert |
| B2 | Die Vollzugsmarke steht nach `   > für \`t3_supertrend\`).` (Ende des Kastens), mit einer `   >`-Zeile als Absatztrenner. Sie ist wörtlich aus dem Auftrag übernommen, **ohne Leerzeile** vor `5.` (sonst endet die Liste für die Sonde) |
| **B3** | `numstat` 550/0, `git diff` **0** `-`-Zeilen, `benchmark_drawdowns.json` `a163c498…` **direkt danach gemessen** |
| Probe | Die Sonde lief lesend gegen das **alte** Abbild. Sie meldet (ii) **1** an Punkt 4, Feld `pfade` (drei statt zwei) und Feld `nicht_dateibezogen`. ⇒ Der Parser liest die Pfadzeile, wie beabsichtigt (`b_sonde_nach_blockB_altes_abbild.txt`) |

## 3. Block C — Abschnitt 39 und die Marken

Abschnitt 39 hat die Unterabschnitte 39.1–39.10. Eingesetzt hat sie
`eintrag_register_39.py` aus `abschnitt39_vorlage.md`. Wörtliche Zitate stehen
dort als Platzhalter `«Q:<quelle>:<zeile>»` (ganze Zeile) bzw.
`«S:<quelle>:<zeile>:<text>»` (Teilzitat, im Skript gegen die Quellzeile
geprüft).

| | Inhalt |
|---|---|
| 39.1 | Anlass; 23f Z. 13, 15, 17, 19; der Satz „Für eine ausführende Sitzung gilt das Register, nicht Fable." als Teilzitat; die Ursprungsentscheidung 23a Z. 21, 23 und ihr Grund Z. 17; eine Tabelle „was ab hier gilt"; die Messung aus TB-92 |
| 39.2 | Pfadzeile im Wortlaut; Tabelle mit drei Dateien; 23a Z. 37/39/41/43 (Registertext zu 4/23/33, Wache, Folge, Grund); 23b Z. 19; 23d Z. 19; Notiz zu TB-92 (Konstante, AST, drei Leser, `beispieldaten.py` ohne Tabelle) |
| 39.3 | 23b Z. 23; Planstände `_vt` (TB-66) und `_tb72` (TB-72); Gruppenwechsel ⇒ nach dem Register leer; ⚠️ die Sonde meldet anders (feste Konstante) |
| 39.4 | 23b Z. 21, 25; das Ergebnis **ohne Werte** (27.1); Selbsttest, Wache 18/18 |
| 39.5 | fünf Übergänge mit **vollen** Hashes (sechs Dateien), Auftrag/Freigabe; Zählweise; 23c Z. 39 (Fables Tatsachennotiz zur Hochstufung 2 → 1) |
| 39.6 | 23e Z. 23, 30; die Tabelle des Modus-Nachweises; ⚠️ Notiz, dass der Registertext „Eingabestand" (23d) **nicht** eingetragen ist (TB-96) |
| 39.7 | 23d Z. 21; 23c Z. 19 (Präzisierung zu 36.1 (1)); Notiz, dass es die dritte Sondengruppe nicht gibt |
| 39.8 | zwei Eingaben; 23f Z. 35; Berichtigung der Nummer TB-94 → TB-96; 23f Z. 37 (Messbitte, **offen**), Z. 45; die zwei TB-92-Tatsachen |
| 39.9 | Regel 36.6/37.3; 22g (Teilzitat); 23c Z. 37 (Teilzitat „kein Pfad-Bestandteil 1, jede 2 mit Tatsachennotiz"); Reihenfolge; **Ergebnis erst in Commit `f65a0a0` angefügt** |
| 39.10 | Tabelle wie 38.8 |

**Marken — zehn, alle Zielabschnitte vorher gelesen:**

| Marke | Ort | Anmerkung |
|---|---|---|
| Vollzug | Abschnitt 10, Punkt 4 (B2) | ohne Leerzeile |
| ERSETZT, Fertigkriterium | 38.4, direkt unter dem Zitat „…grün — die roten Prüfungen misst TB-88 —…" | |
| Berichtigung | 21.9, unter der Tabelle der Folgen (nach der Marke 38.7 (d)) | nennt zusätzlich, dass die **dritte** Zeile (ERZEUGT-Block) mit 39 nicht erledigt ist |
| BEANTWORTET | 38.7 (d), unter der offenen Frage | |
| Gruppenwechsel und Vollzug | 37.2 | ⚠️ **unter der Tatsachennotiz TB-87**, nicht direkt unter dem Registertext. So bleiben Fables Zitat und seine Quelle des Grundes beisammen, und die Marke steht bei dem Satz, den sie berichtigt („die Sonde nennt … `_vt.json`") |
| fünf Übergänge | 37.3, unter der Tatsachennotiz zu TB-86 | |
| Tabelle folgt dem Plan | 23.7, unter der Marke 38.7 (d) | |
| Tabelle folgt dem Plan | 33.2, am Ende des Unterabschnitts (nach dem Zitierhinweis) | |
| `EINGEFROREN` unvollständig | 37.4, nach dem Randbefund, vor „Marke am alten Ort" | enthält Fables Ergänzungssatz aus 23d als Teilzitat |
| VOLLZOGEN | 38.4, am Ende | |

## 4. Block D — Abbild und Sonde

| | |
|---|---|
| **D1** | `sperrliste_abbild.py --ziel …/sperrliste_abbild_2026-09-23.json`: Ziel existierte vorher nicht, **rc 0**, **7351 Bytes**, sha256 **`2f23f76c99e22991e4a331ec1107dc0f090a425bc9e050793470ee3cd52dd4fe`**, am Stand `27b68b9`, 14 Punkte (Z. 845–958), 15 Pfadnennungen. Altes Abbild `6a1b732e…` davor und danach gleich. `benchmark_drawdowns.json` davor und danach `a163c498…` (`d1_abbild.txt`) |
| **D2** | Sonde gegen das neue Abbild: **rc 2** · **0 Befunde** · alle **15** Pfadnennungen „gleich" · Punkte **2 und 5 `0`**, die Punkte 1, 3, 4, 6–14 `2` · (ii) **0**, Listentext wie bei Erzeugung: ja · Bilanz **2/0/12** (`d2_sonde_nachher.txt`). Nach dem Eintrag des Ergebnisses in 39.9 lesend wiederholt: unverändert (`d2b_…`) |

⚠️⚠️ **Abweichung vom erwarteten Gesamtausgang: `2` statt `0`.** Der Auftrag
erwartet `0`, „sofern kein Punkt aus anderem Grund `1` meldet". Das ist nach
dem Parser der Sonde (R6) von vornherein nicht erreichbar. Jeder Punkt, dessen
Text mehr nennt als Dateipfade, ist `2`. Das gilt für zwölf der vierzehn
Punkte, auch für Punkt 4: Er nannte schon vor TB-94 „**einschliesslich der
Interpolationsregel**". Das Fertigkriterium lautet aber „Sonde 0 **für die
Pfade**" (23a, 23f), und Fables Tag-Vorbedingung heisst „kein Pfad-Bestandteil
1, jede 2 mit Tatsachennotiz" (23c). **Das erste ist erfüllt**, das zweite ist
Sache des Tags und hier nicht geprüft. ⇒ **Abbruchkriterium 7 (`1`) tritt nicht
ein.** Eingetragen in 39.9.

⚠️ **Gruppe „bestimmt":** Die Sonde nennt weiter `…_vt.json` mit „Vollzug steht
aus". Das steht fest verdrahtet in `shared/sperrlistensonde.py`
(`BESTIMMT_NICHT_EINGETRAGEN`), ist nicht aus dem Abbild gelesen und nicht
geprüft. Nach dem Registertext ist die Gruppe leer (39.3). Ich habe es
gemeldet und nicht geändert (keine `.py`).

### D3 — Fertigkriterium nach der Berichtigung 38.4

| | erfüllt? | wo |
|---|---|---|
| Registertext eingetragen (Form (ii)) | **ja** | Punkt 4 (Pfadzeile + Marke), 39.2 |
| Tatsachennotiz mit altem und neuem Hash | **ja** | 39.5 (volle Hashes, sechs Dateien) |
| Die drei Leser lesen über eine Konstante | **ja** | TB-92, `0292e92`; bezeugt in 39.2 |
| `registerbericht.py` liest `symbole_handelbar_in_falte` | **ja** | TB-92; 39.2 |
| Absturz weg, Test läuft bis zur Schlusszeile | **ja** | TB-92 (163/2, rc 1, 501 s); 39.1. In TB-94 nicht neu gelaufen |
| Modus-Nachweis bytegleich | **ja** | TB-92 A1b; 39.6 |
| Neues Abbild | **ja** | D1, `2f23f76c…`; 39.9 |
| Sonde 0 für die Pfade | **ja** | D2: 0 Befunde, 15/15 gleich, (ii) 0. Gesamtausgang 2 wegen Nicht-Dateibezogenem |

⭐⭐ **Die Spalte ist vollständig „ja": Plan-Punkt 8 ist fertig.** Der Tag
bleibt trotzdem blockiert, weil `test_vorregistrierung.py` rot ist (21.9, 23a).
Das schliesst TB-95.

## 5. Block E — Nachweise

**E1** (`e1_numstat.txt`), zeichengleich:

```
$ git --no-optional-locks log -1 --numstat -- docs/VORREGISTRIERUNG_neuselektion.md
f65a0a0 TB-94 Block D: …
25	0	docs/VORREGISTRIERUNG_neuselektion.md

# je TB-94-Commit auf das Register:
27b68b9  550	0	docs/VORREGISTRIERUNG_neuselektion.md
f65a0a0  25	0	docs/VORREGISTRIERUNG_neuselektion.md
# gesamt 12f6089..HEAD:
575	0	docs/VORREGISTRIERUNG_neuselektion.md
# '-'-Zeilen im Gesamtdiff: 0
# wc -l:     7530 (Eingang 6955)
```

**E2** (`e2_zitate.txt`): **29 Zitate** (25 ganze Zeilen, 4 Teilzitate) aus
23a, 23b, 23c, 23d, 23e, 23f und 22g. **29-mal `diff` rc 0**, 0 Abweichungen.
Die Zuordnung zum Ort ist geschärft: Das Teilzitat in der Marke 37.4 steht auch
im Vollzitat in 39.7, und der erste Prüflauf hatte es dort gesucht.

**E3**: `a1_hashes.txt`, `a2_sonde_vorher.txt`, `d1_abbild.txt`,
`d2_sonde_nachher.txt`, `e1_numstat.txt`, `e2_zitate.txt`. Dazu
`b_sonde_nach_blockB_altes_abbild.txt`, `d2b_sonde_nach_eintrag_39_9.txt`,
die Skripte `eintrag_register_39.py`, `eintrag_39_9_ergebnis.py`,
`e2_zitate.py`, die Vorlage und `zitate.json`.

**Nicht geändert:** keine `.py` ausserhalb von `docs/belege/TB-94/`. In
`ergebnisse/` ist nur das neue Abbild hinzugekommen (`git diff --name-status
fcc3265 HEAD`). Alle Tabellen, `faltenplan.json`, beide alten Abbilder und alle
Codedateien der Vorregistrierung haben am Ende dieselben Hashes wie am Eingang
(`e1_numstat.txt`, Abschluss-Hashes).

## 6. Abweichungen und Befunde, zusammengefasst

1. **Sonde Gesamtausgang 2 statt 0.** Das ist keine Messabweichung, sondern
   eine Erwartung des Auftrags, die der Parser nicht erfüllen kann (D2).
2. **Gruppe „bestimmt"** ist in der Sondenausgabe nicht leer (feste
   Konstante, 39.3).
3. **Hilfsdatei nicht gelöscht.** `rm`/`mv` wurden abgelehnt. Die Datei liegt
   unversioniert da.
4. **Das Ergebnis von 39.9 steht in einem eigenen Commit** (`f65a0a0`), weil
   das Abbild erst nach dem B+C-Commit gezogen werden durfte. Der Nachtrag ist
   additiv und berührt den Listentext von Abschnitt 10 nicht; (ii) blieb `0`.
5. **23d nimmt an, `beispieldaten.py` lese dieselbe Konstante.** Die Datei
   liest keine Tabelle (in 39.2 festgehalten, wie TB-92).
6. **Der Registertext „Eingabestand" (23d) ist nicht eingetragen.** Er stand
   nicht im Auftrag und gehört nach 23d §4 zu `messgroessen.json` (39.6).
7. Keine Hash-Abweichung gegen die Vormessung.

## 7. Für die Folgesitzung vorbereitet (gemessen, nicht eingetragen)

| | |
|---|---|
| 23c Abschnitt 3 | Fable schreibt „`benchmark.py` an **drei** Punkten ist **ein** Übergang". Die Sonde misst `benchmark.py` an **zwei** Punkten (4 und 6), vor und nach TB-94. Der Satz ist nicht zitiert; 39.5 nennt die gemessene Zahl |
| 36.6 / Kopf von Abschnitt 10 | Der Hinweis unter der Überschrift von Abschnitt 10 (37.1–37.5) nennt als Abbild noch `…_2026-09-22.json`, `6a1b732e…`. Das aktuelle Abbild steht jetzt in **39.9**, eine Marke dort gab der Auftrag nicht vor. Kandidat für eine Marke |
| Sonde | `BESTIMMT_NICHT_EINGETRAGEN` ist veraltet. Der TB-92-Entwurf (`sonde_je_datei_entwurf.patch`) baut die leere Gruppe; sein Verweis auf „den Registerabschnitt, der nicht geschrieben ist" kann jetzt auf 39.3 zeigen. Dritte Gruppe „Abschnitt 0" (23c), „Schreibziele", „Lesequellen" (23d) offen |
| Punkt 4 und R6 | Die Pfadzeile bringt Prosa in den Rest „Nicht-Dateibezogenes" von Punkt 4. Am Ausgang ändert das nichts (schon vorher 2), aber wer Punkt 4 je auf 0 bringen will, muss die Interpolationsregel **und** diesen Wortlaut verorten |
| TB-95 | `G6`/`H3` sowie die Messbitte 23f §6 stehen in 39.8 als Blockzitat (Register Z. 7445 am Stand `f65a0a0`) |

---

## In einfacher Sprache

Die neue Vergleichstabelle stand bisher nur im Programm, nicht im Regelwerk.
Jetzt steht sie auch dort. In der Liste der geschützten Dateien ist sie
**zusätzlich** zur alten Tabelle genannt. Die alte bleibt Byte für Byte
unverändert als historischer Stand.

Den alten Satz „das Prüfprogramm muss fehlerfrei sein" habe ich nicht gelöscht.
Er hat einen sichtbaren Vermerk bekommen, dass er ersetzt ist, und der
Ersatztext des Verfahrensprüfers steht wörtlich im neuen Abschnitt 39. Der
Abschnitt hält auch fest, was die vorigen Sitzungen gemessen haben. Die neue
Tabelle gleicht der alten in allen 9750 Zahlen. Sie lässt sich aus dem
eingefrorenen Datenbestand exakt wiederherstellen. Und fünf Programmdateien
haben sich planmässig geändert, jeweils mit altem und neuem Fingerabdruck.

Danach habe ich ein neues Schutzabbild gezogen. Die Wache findet dagegen
**keinen einzigen Alarm**, alle 15 geschützten Dateien stimmen. Sie meldet
trotzdem „nicht vollständig prüfbar". Der Grund: Viele Einträge der Liste
nennen neben Dateien auch Regeln oder Zahlen, die man nicht per Fingerabdruck
prüfen kann. Das war schon vorher so und ist kein Fehler. Damit ist der
Arbeitspunkt „Tabelle tauschen" fertig. Zwei rote Prüfungen und eine Frage zu
neun Handelslisten bleiben für den nächsten Auftrag.

Eine Kleinigkeit ist liegen geblieben: Eine überflüssige Hilfsdatei durfte
diese Sitzung nicht löschen. Sie liegt unversioniert im Ordner
`docs/projektfuehrung/` und kann von Hand entfernt werden.
