# TB-130: Ergebnis. Register Abschnitt 52 — Fable 02a (R63–R65) zeichengleich, Tatsachennotizen 52.4–52.5, 12 Marken am alten Ort, numstat 88/0; Registerkopie neu in 53 Abschnittsdateien und 4 Teilen, Index und Dialog-Index nachgezogen

**Sitzungstitel:** `TB-130` · **Stand:** 02.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-130_register_fable_02a.md` ·
**Belege:** `docs/belege/TB-130/`
**Eingang:** `1833839` (TB-129, D3), Arbeitsbaum wie 0a (sechs Einträge). Commits: `b0c7a35` (Schritt 0, im Folgenden
⟨S0⟩), `cd1bf02` (0: Ausgang, Vorprüfung), `ad351d5` (A: Register, einziger Registercommit), `2f6967c` (B/C: BACKLOG,
Registerkopie, Index, Dialog-Index), der Abgabe-Commit (D: dieses Dokument, Journal EB) und ein kleiner Commit mit
`d3_porcelain.txt`. Nach jedem Commit gepusht.
**Quelle (md5 am ⟨S0⟩ und im Arbeitsbaum geprüft, `0b_ausgang.txt`):**
`docs/projektfuehrung/FABLE_ANTWORT_2026-10-02a_exposure_tage_laufbereich_marken.md`,
`a7821eeb4f61faad5f74f72ec7201797`, 21 709 B — gleich dem Soll.
**Freigabe:** Betreiber, 02.10.2026, Auswahlkarte im steuernden Chat (gestellt 14:52, eingetragen 15:09), „Freigeben wie
beschrieben (Empfohlen)“ (wörtlich im Auftrag). Keine Rückfrage an den Betreiber.
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | genau sechs Einträge (` M` AKTUELLER_AUFTRAG, ` M` UEBERGABE, `??` Auftrag, `??` drei Fable-Dateien 02a/02) | genau diese sechs (`0a_status.txt`) |
| 0b | 11 225 Z., sha256 `7f74b0e5…`, md5 `b4764e4e…`; `register()` `a1e1366a…`, `fehlend []`, 23 Teile; Abbild `46f0ad5d…`; Sonde rc 2, 37/0/0, (ii) 0, Listentext ja, JSON ohne `zeilen` `9f7364ef…`; Quelle `a7821eeb…`/21 709 B | alles gleich (`0b_ausgang.txt`); `registerbericht.py --pruefen` rc 1 (bekannt, Vergleichswert); porcelain vor/nach Sonde 1/1 |
| 0c | `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` | leer ⇒ Basis `docs/belege/TB-129/a5_test_vorregistrierung.txt` (196/196), kein eigener Basislauf |
| 0d | Marken 12/12, Quelle R63–R65 je zwei Zeilen in Z. 112–119, `## 52.` 0 / `> R63 — ` 0, 33 Fundstellen, 7 Zählungen, 9 Dateien der Glob-Zählung | Prüfskript aus Anhang A (aus dem Auftrag am ⟨S0⟩ geschnitten, gegen den mit `git archive` ausgepackten Baum am ⟨S0⟩, 17 Dateien) rc 0; je Eintrag einzeln: 12/12 Marken, Blockanfänge Z. 112/115/118, 33/33 Fundstellen, 7/7 Zählungen, 9/9 `simulate_portfolio` (`0d_vorpruefung.txt`) |
| A4 | Probelauf an Kopie grün, dann echt, `cmp` gleich | Probelauf: 12 Marken an 11 Stellen, 11 225 → 11 313 Zeilen, alle Textprüfungen rc 0; echt identisch; `cmp` rc 0 |
| A5 R-Diff | 3/3 rc 0; Mutation rc 1 | **3/3**; Mutation (R64, „ die “ → „ der “) rc 1 |
| A5 Zitate | 2/2 | Kopf 52.0 und Schluss 52.4–52.5 **2/2** |
| A5 Überschriften/Ketten, Marken | 3/3, 12/12 | **3/3 und 3/3**, **12/12**; in Abschnitt 9, 10 und ERZEUGT-Block je 0 |
| A5 numstat | zweite Spalte 0 | **88/0** |
| A5 Abschnitt 10, ERZEUGT | bytegleich | beide gleich (Abschnitt 10 jetzt Z. 965–1171, ERZEUGT unverändert Z. 260–460) |
| A5 `registerbericht --pruefen` | nachher = vorher | rc 1 / rc 1, Ausgabe gleich |
| A5 Sonde | JSON ohne `zeilen` gleich, (ii) 0, Listentext ja | `9f7364ef…` gleich, (ii) 0, ja; der Text nennt jetzt Z. 990–1103 statt 987–1100 (erwartet, drei Zeilen aus 4.2) |
| A5 `register()` | ≠ vorher, `fehlend []`, 23 Teile | `4caf0179…`, `[]`, 23 |
| A5 `test_vorregistrierung` | 196/196 | **196/196**, rc 0, 894 s |
| B | Anker 1, Text nachher 1, numstat 10/0, Block bytegleich | Anker 1 (Z. 260), erste Textzeile nachher 1, **10/0**, Bytevergleich GLEICH (2 568 B, 9 Zeilen, Leerzeile davor/danach, Anker danach) |
| C1 | fünf Aufrufe rc 0; 53 Abschnittsdateien | alle fünf rc 0; Teile 0–22 / 23–36 / 37–42 / **43–52**, bytegleich; **53** Abschnittsdateien `_00`–`_52`, bytegleich; keine Datei VERALTET |
| C2 | Index nachgezogen | 212 Zahlen in Zeilenangaben umgeschrieben (182 geändert), 8 Ersetzungen und 5 Tabellenzeilen je Anker 1, Zeile 52, Abschnitt 7, Abschnittstabelle 0–52 aus den Köpfen |
| C3 | vorher 5, ersetzen | 5 → 5 ersetzt; „Tag-Vorbedingungen“ unverändert (siehe Nebenbemerkungen: erster Lauf rc 1 durch eigene Pflegezeile) |
| C2/C3 Gegenprobe | — | 236/236 Zeilenangaben auf Markenzeilen, 14/14 Marken in Abschnitt 6, 12/12 in Abschnitt 7, C3 5/0, 53/53 Tabellenzeilen, Indexzeilen E-2 6 |
| C4 | `--pruefen` rc 0; 02a Fundstelle 52, offen; 01a registriert, Frage/Entscheidung unverändert; 52 Antworten | rc 0 / rc 0; 02a: Fundstelle 52, Status offen, Anfrage „02a (gleicher Buchstabe)“; 01a: Status registriert, offen nein, Frage und Entscheidung zeichengleich; „52 Antworten.“; numstat 3/2, keine weitere Zeile geändert |

## `herkunft.register()`

| | Wert |
|---|---|
| vorher (Register `7f74b0e5…`, 11 225 Z.) | `a1e1366ab55719fe4724b9da3d9425f3029628d56460bcda8e2e4476dce8cc40` |
| nachher (Register `a7496780…`, 11 313 Z.) | `4caf01793c8c4bb979eeea0243cff7a1b13004c28716391f61e8a5978a407b56` |

`fehlend []` und 23 Teile vorher wie nachher. Der neue Wert steht nur hier, nicht im Register (42.5).
Register nachher: sha256 `a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece`, md5 `80af174f41b41d006bd28dce54730c3f`.

## Wie eingetragen

- Vorlage `a4_vorlage_52.md` mit Platzhaltern, Einsetzskript `a4_eintrag.py` (aus TB-129 übernommen, Werte angepasst).
  Alle Texte per `git show b0c7a35:<pfad>`: Kopf und Schluss aus den zwei ````-Zäunen nach „Kopf:“ bzw. „Schluss:“,
  Überschriften, Ketten und Marken aus dem Daten-Block, die drei Blöcke aus der Quelle Z. 112–119 nach der Schnittregel.
  ⟨S0⟩ ist als `` `b0c7a35` `` eingesetzt, ⟨DATUM⟩ als `02.10.2026`.
- Wachen im Skript wie TB-129: Eingang 11 225, `## 52.` frei, keine Zeile `> R63 — `, alte Zeilen in Reihenfolge,
  Abschnitte 9 und 10 und ERZEUGT-Block unverändert, 12 Anker je 1 vorher und nachher.
- Nachweise (`a5_r_diff.py`, `a5_mutation.py`, `a5_zitate.py`, `a5_marken.py`) lesen Quelle und Auftrag selbst;
  Überschriften und Ketten liest `a5_marken.py` aus der Markdown-Tabelle 1, nicht aus dem JSON.
- 0d: `0d_vorpruefung.py` packt die 17 genannten Dateien (die neun `equity_simulation.py` über `git ls-tree` aufgelöst)
  mit `git archive b0c7a35` in den Scratch und ruft dort das Prüfskript aus Anhang A auf; dazu je Eintrag einzeln.
- Index: `c2_index_zeilen.py` (Abbildung über die unveränderten alten Zeilen, jede Zahl in Listen und Bereichen),
  `c2_index_02a.py` (Tabelle für Abschnitt 7 aus `c1_marken.txt` und Anhang A), `c2_index_eintraege.py` (Kopf,
  „Wie gemessen“, 4.2 in Tabelle 2, Zeilen 25/47/48/50/51 und neue Zeile 52 in Tabelle 4, Abschnitt 7, Pflege; die
  Markenzeilen kommen aus `a4_eintrag_daten.json`), `c3_indexzeilen.py`, Gegenprobe `c2_index_pruefen.py`.

## Markentabelle (gegen Anhang A)

| Nr | alter Ort (Anhang A) | nach Z. (alt) | Marke Z. (neu) | Wort | durch | Art | T |
|---|---|---|---|---|---|---|---|
| 1 | 4.2 | 526 | 528 | PRÄZISIERT | R64 (52.2) | MARKE | 1 |
| 2 | 25.2, unter dem berichtigten Satz | 4650 | 4655 | BERICHTIGT | R62 (51.7) und R65 (52.3) | MARKE+ | 2 |
| 3 | 47.9 (R26) | 10704 | 10712 | BERICHTIGT | R61 (51.6) | MARKE+ | 4 |
| 4 | 47.13 (R30) | 10732 | 10743 | BERICHTIGT | R61 (51.6) | MARKE+ | 4 |
| 5 | 48.16 (R48) | 10884 | 10898 | PRÄZISIERT | R64 (52.2) | MARKE | 4 |
| 6 | 48.19 (R51) | 10913 | 10930 | PRÄZISIERT | R65 (52.3) | MARKE | 4 |
| 7 | 50.1, nach der Tabelle | 10978 | 10998 | ERGÄNZT | R60 (51.5) und 51.8 | MARKE+ | 4 |
| 8 | 50.4, nach dem Zitatblock | 11105 | 11128 | ERGÄNZT | R57 (51.2): der Schlusssatz ist bestätigt | MARKE+ | 4 |
| 9 | 51.5 (R60) | 11173 | 11199 | PRÄZISIERT | R63 (52.1) | MARKE | 4 |
| 10 | 51.5 (R60) | 11173 | 11202 | PRÄZISIERT | R64 (52.2) | MARKE | 4 |
| 11 | 51.6 (R61) | 11180 | 11212 | PRÄZISIERT | R65 (52.3) | MARKE | 4 |
| 12 | 51.9 | 11212 | 11247 | ERGÄNZT | R63 (52.1): die Lesart ist bestätigt | MARKE+ | 4 |

Quelle: `a4_eintrag_daten.json`, `a5_marken.txt`, `c1_marken.txt`, `c2_index_02a_tabelle.md`. Abschnitt 52 steht in
Z. 11263–11313 (52.1 Z. 11267, 52.2 Z. 11274, 52.3 Z. 11281, 52.4 Z. 11288, 52.5 Z. 11301). Nr. 2–4, 7, 8 zählt
R65 (b) auf; Nr. 1, 5, 6, 9–12 hat der steuernde Chat nach R65 (a) bestimmt (Kopf 52.0). **Nicht gesetzt nach Anhang A
(wie vorgesehen):** 7 (c) (52.5 Nr. 9), 51.8, 51.10; keine Marke in Abschnitt 9, 10 und im ERZEUGT-Block.

## Für Fable (nur Verfahrensfragen)

1. **52.5 Nr. 2** (02a, „Unsicher“ 1): Zeitachse des Falten-Sharpe in Falten mit teilweisem Benchmark — ob die Tagesreihe
   Tage vor dem ersten Handelbar-Tag führt; erst Vorprüfung in 16, 21, 29, 33.
2. **52.5 Nr. 5:** `beta_bereinigung` behandelt und prüft weder fehlende Werte noch doppelte Daten (in 0d nachgemessen:
   `dropna` in `auswertung.py` 0-mal; Fundstellen Z. 361–386 und 510–528 wie in 52.4).
3. **52.5 Nr. 6** (02a, „Unsicher“ 4): verschiebt `bestaetigung_ab_effektiv` (R37) den Beginn der Tage nach R64 für die
   Bestätigungsperiode?
4. **52.5 Nr. 7:** R39 nennt `benchmark_tagesreihen/<bot>.csv`, `auswertung.py:379` liest `<markt>.csv` (in 0d gemessen).
5. **52.5 Nr. 9:** Keine Marke an 7 (c) zu R64 (a).
6. **Reibung beim Setzen, Werkzeug (wie TB-129 bei R61):** `registerkopie.py --marken` zählt die erste Zitatzeile von
   R65 (52.3, Register-Z. 11283) als Art `MARKE+`, weil der Block selbst eine Berichtigung beschreibt. Darum steht
   `MARKE+` bei 111 statt 104 + 6 = 110 (`MARKE` 70 = 64 + 6, `UEBERSCHRIFT` 82 = 80 + 52.1 und 52.2). Im Index ist
   die Zeile nicht als Marke geführt.
7. **Reibung, Reihenfolge an 25.2:** Die neue Marke steht nach Anhang A und R65 (34.3) direkt unter dem berichtigten
   Satz und damit **vor** der älteren Marke aus R53 (TB-126). Am Ort ist die Reihenfolge der Marken deshalb nicht mehr
   die zeitliche; wer dort von unten liest, sieht die ältere Marke zuletzt.
8. **Reibung, Markenwort (wie TB-129):** Die beiden Bestätigungen (50.4 Schlusssatz, 51.9 Lesart) stehen mit ERGÄNZT und
   Zusatz „… ist bestätigt“, weil es kein eigenes Markenwort für Bestätigungen gibt (R65 (a) sieht das so vor).

## Nicht getan

- 52.5 (alle neun Punkte): Messung mit dem Zellen-Erzeuger (Nr. 1, 3, 4), Vorprüfungen und Anfragen (Nr. 2, 5, 6, 7, 9),
  51.10 Nr. 1–5 und 8 (Nr. 8).
- Die Ablage (53 Abschnittsdateien, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`) — macht der steuernde Chat.
- Kein Code (die Wache aus R64 (c) und die Probe aus R64 (d) kommen mit dem Zellen-Erzeuger), kein neues Abbild, keine
  Läufe von `auswertung.py`, Zellen-Erzeugern oder Backtests.
- `registerbericht.py --pruefen` rc 1 bleibt (schon vor TB-126; Zahlenteil veraltet).

## Nebenbemerkungen zum Ablauf

- `test_vorregistrierung` lief am echten Register vor dem Commit A (894 s); erst danach ist committet.
- **C3, erster Lauf rc 1 (eigener Fehler, behoben):** `c2_index_eintraege.py` schrieb in die neue Pflegezeile den alten
  Schluss „Ohne Marke; an Fable (51.10 Nr. 7).“ wörtlich hinein; damit zählte er im Index 6 statt 5, und
  `c3_indexzeilen.py` ersetzte nach der Regel des Auftrags nichts (`c3_indexzeilen_erster_lauf.txt`). Die Pflegezeile ist
  umformuliert, der Index aus `HEAD` (`ad351d5`) wiederhergestellt (`git show HEAD:… >`, die Datei war nur von dieser
  Sitzung geändert) und C2/C3 noch einmal vollständig gelaufen; die Belege `c2_*`/`c3_indexzeilen.txt` sind vom zweiten
  Lauf. Die Zählung im Auftrag (Soll 5) galt am ⟨S0⟩ und war richtig.
- Die Teile der Registerkopie bleiben vier (T4 = 43–52, 195 322 B); T3 unverändert 232 429 B (Kopfzeile neu).
- Der Index nennt in der Pflegezeile „vom Stand `f63ad4c`“: das ist der letzte Registercommit vor A; das Register am
  ⟨S0⟩ ist damit bytegleich (sha256 `7f74b0e5…`).

## In einfacher Sprache

Fables drei neue Regeltexte vom 02.10. stehen jetzt Zeichen für Zeichen im Register, als Abschnitt 52, dazu die
nachgelesenen Code-Stellen und die offenen Punkte des steuernden Chats. An zwölf alten Stellen weist eine kleine Marke auf
die neuen Texte. Kein alter Satz wurde geändert (88 Zeilen dazu, 0 weg), alle Prüfungen und der grosse Registertest
(196/196) sind grün. Danach sind die Kopie des Registers für die Ablage (53 Dateien), der Wegweiser und die Liste der
Fable-Antworten neu erzeugt. Am Code hat sich nichts geändert.
