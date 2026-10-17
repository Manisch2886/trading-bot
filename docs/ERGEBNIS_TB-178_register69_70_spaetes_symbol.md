# Ergebnis TB-178 — Register 69 (Fable 17d, R109) und 70 (Fable 17e, R110) mit zehn Marken; Abnahme des späten Symbolfalls am Erzeuger (R110 (a))

**Sitzung:** Mac (Claude Code, Opus 5.5), 17.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-178_register69_70_fable17d17e_spaetes_symbol.md` · **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9.6) · **Belege:** `docs/belege/TB-178/`

**Commits (alle auf `main`, gepusht):**

| Schritt | Commit | Inhalt |
|---|---|---|
| S0 | `14833dd` | Fable 17.10.d und 17.10.e (je Anfrage, Antwort, Übergabe) und Stand des steuernden Chats vor TB-178 (Auftrag) |
| R | `47f184b` | Register 69 (Fable 17d, R109) und 70 (Fable 17e, R110), zehn Marken |
| K | `0d6ac21` | Registerkopie, Index, Dialog-Index |
| P | `ffbf069` | Abnahme später Symbolfall am Erzeuger (R110 (a)) |
| A | dieser Commit | Ergebnis, BACKLOG, Journal FO |
| F | folgt | porcelain und numstat |

## Kurz

Alle Schritte liefen wie im Soll, ohne Abbruch und ohne Nachfrage. Die sechs Fable-Dateien (17.10.d und 17.10.e) liegen md5-gleich im Repo. R109 und R110 stehen zeichengleich als Abschnitte 69 und 70 im Register, dazu zehn Marken; sonst append-only (numstat 109/0). Registerkopie, Index (mit neuem Abschnitt 20) und Dialog-Index sind nachgezogen, jeder Beleg in K endet mit rc 0. Die Probe am Erzeuger lief auf Python 3.9.6 **18 von 18** (je Bot 6 von 6, Gegenprobe in beide Richtungen angeschlagen). Kein Handelscode geändert, keine Kursdaten aus `data/` gelesen.

## Schritt 0

0a: `0a gut (2 Eintraege)`; Holbefehl: `tb178_werkzeug.py 552f5c4d…a1af`, `tb178_probe_spaetes_symbol.py 1fe6f12e…fa88`, `Dateien 2` — je wie Soll. `0a_md5.txt` wörtlich:

```
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17d/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md = nachher docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md = 007196934a22163335439c2888886047
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17d/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md = nachher docs/projektfuehrung/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md = 3b886ee769174d7c474679dd4452c9eb
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17d/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md = nachher docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md = b968fc124c5361f03e0f1118fdec1994
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17e/FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md = nachher docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md = 36389b7829a6e77c3ebe327fc58b7d25
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17e/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md = nachher docs/projektfuehrung/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md = 1d964b3107485a44ba29467ebc56c34a
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17e/FABLE_UEBERGABE_2026-10-17e_eroeffnung.md = nachher docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17e_eroeffnung.md = a204bed16a9f30adda7c2b34489856ba
Pruefungen: 6, NEIN: 0
rc 0
```

Nach S0 war `git status --porcelain` leer.

## Schritt V

`v_voraussetzung.txt` wörtlich:

```
ja    unveraendert: research/exposure_messung/bot_lauf.py md5 01fd9282ded2
ja    unveraendert: research/faltenplan_neun/faltenschranke_messung.py md5 584d9ff959da
ja    unveraendert: research/tb24_haltedauern/haltedauer_kern.py md5 60942de99b32
ja    unveraendert: research/tb24_haltedauern/positionen_holen.py md5 006375593b4b
ja    unveraendert: research/tb24_haltedauern/test_listen_erzeuger.py md5 d77e73ed5ff7
ja    unveraendert: strategies/elliott_wave/multi_symbol_optimise.py md5 bf11370b140d
ja    unveraendert: strategies/elliott_wave_stocks/multi_symbol_optimise.py md5 571076168d56
ja    unveraendert: strategies/t3_supertrend/multi_symbol_optimise.py md5 dc85993e8d42
ja    BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-178
ja    Journal: hoechste FN (FN am Bau-HEAD)
ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md verfolgt, gleich HEAD, md5 007196934a22163335439c2888886047
ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md verfolgt, gleich HEAD, md5 3b886ee769174d7c474679dd4452c9eb
ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md verfolgt, gleich HEAD, md5 b968fc124c5361f03e0f1118fdec1994
ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md verfolgt, gleich HEAD, md5 36389b7829a6e77c3ebe327fc58b7d25
ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md verfolgt, gleich HEAD, md5 1d964b3107485a44ba29467ebc56c34a
ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17e_eroeffnung.md verfolgt, gleich HEAD, md5 a204bed16a9f30adda7c2b34489856ba
ja    Registerblock 17d: genau R109 und Quelle im Codeblock (Z. 15–18)
ja    Registerblock 17e: genau R110 und Quelle im Codeblock (Z. 17–20)
ja    Register: 68 da, 69 und 70 nicht; R109/R110 0 Treffer
ja    Register endet mit genau einer Leerzeile
ja    Ort 68.1 (R109): Einfuegestelle vor Z. 12725 eindeutig, R109 dort noch nicht genannt
ja    Ort 29.3 (R109): Einfuegestelle vor Z. 5458 eindeutig, R109 dort noch nicht genannt
ja    Ort 66.1 (R109): Einfuegestelle vor Z. 12590 eindeutig, R109 dort noch nicht genannt
ja    Ort 67.1 (R109): Einfuegestelle vor Z. 12659 eindeutig, R109 dort noch nicht genannt
ja    Ort 66.1 (R110): Einfuegestelle vor Z. 12590 eindeutig, R110 dort noch nicht genannt
ja    Ort 37.2 (R110): Einfuegestelle vor Z. 7034 eindeutig, R110 dort noch nicht genannt
ja    Ort 37.5 (R110): Einfuegestelle vor Z. 7288 eindeutig, R110 dort noch nicht genannt
ja    Ort 29.3 (R110): Einfuegestelle vor Z. 5458 eindeutig, R110 dort noch nicht genannt
ja    Ort 38.5 (R110): Einfuegestelle vor Z. 7554 eindeutig, R110 dort noch nicht genannt
ja    Index-Kopf Z. 3 nennt 0–68
ja    Index: Zeile 68, Pflegezeile TB-176a, Pflege-Anker, Abschnitt 19 je genau einmal; kein Abschnitt 20
ja    Dialog-Index: 17d und 17e noch nicht
ja    R109 (b) Voraussetzung lesbar: research/tb24_haltedauern/test_listen_erzeuger.py hb() und Pruefung 3b je genau eine Zeile
info  R109 (b) Voraussetzung (Messung, kein Urteil; R110 (a): gesetzt): research/tb24_haltedauern/test_listen_erzeuger.py Z. [76] `x.update(t)` in hb() - die vom Test uebergebenen Tage ueberschreiben die Rechnung; Z. [161] Pruefung 3b setzt den Tag von CCC (`json.dumps({"CCC": ...})`)
ja    Probe noch nicht im Repo (docs/belege/TB-178/tb178_probe_spaetes_symbol.py)
Pruefungen: 34, NEIN: 0
rc 0
```

## Schritt R

Datum `17.10.2026`, S0 `14833dd`. Probe (`r_probe.txt`) 7/0, rc 0; Eintrag (`r_eintrag.txt`), letzte Zeilen:

```
ja    nachher: 10 Marken Z. [5459, 5462, 7041, 7298, 7567, 12606, 12609, 12681, 12750, 12823]; Abschnitt 69 Z. 12814, 70 Z. 12875
ja    R109 mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)
ja    R110 mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)
ja    Register append-only bis auf die 10 Marken (je Leerzeile, Marke, Zeichengleich-Zeile)
Pruefungen: 11, NEIN: 0
rc 0
```

Marken aus `r_daten.json`:

| Ort | Zeile | Kopf |
|---|---|---|
| 68.1 | 12750 | 68.1 R108 BERICHTIGT und ERGÄNZT durch R109 (69.1) |
| 29.3 | 5459 | 29.3 ERGÄNZT durch R109 (69.1) |
| 66.1 | 12606 | 66.1 R106 BERICHTIGT durch R109 (69.1) |
| 67.1 | 12681 | 67.1 R107 ERGÄNZT durch R109 (69.1) |
| 69.1 | 12823 | 69.1 R109 BERICHTIGT und ERGÄNZT durch R110 (70.1) |
| 66.1 | 12609 | 66.1 R106 ERGÄNZT durch R110 (70.1) |
| 37.2 | 7041 | 37.2 ERGÄNZT durch R110 (70.1) |
| 37.5 | 7298 | 37.5 ERGÄNZT durch R110 (70.1) |
| 29.3 | 5462 | 29.3 ERGÄNZT durch R110 (70.1) |
| 38.5 | 7567 | 38.5 ERGÄNZT durch R110 (70.1) |

Register vorher 12 785 Zeilen, nachher 12 894 (numstat `14833dd..47f184b`: 109/0).

## Schritt K

| Beleg | rc |
|---|---|
| `k_registerkopie.txt` | 0 (bytegleich, 1 274 246 B, sha256 `640ee3a0ff7cad55…`; Teil 6 = Abschnitte 58–70, 161 360 B ≤ 240 000) |
| `k_abschnitte.txt` | 0 (71 Abschnittsdateien 0–70, bytegleich) |
| `k_pruefen.txt` | 0 |
| `k_index_zeilen.txt` | 0 (495 Zeilenangaben, davon 292 geändert) |
| `k_index.txt` | 0 (6/0; 69 und 70 in Teil 6, zehn Marken je in genau einer Teildatei) |
| `k_handfelder.txt` | 0 |
| `k_dialog_index.txt` | 0 (71 Zeilen = 71 Antworten, 71 von 71 mit allen sechs Feldern) |
| `k_dialog_pruefen.txt` | 0 |

Keine weitere Teildatei entstanden.

## Schritt P

Die Probe (`docs/belege/TB-178/tb178_probe_spaetes_symbol.py`, sha256 `1fe6f12ef5f47603743524f5567cbf84f8edae81c459349d6284a1eeafe0fa88`) lief auf Python 3.9.6. Die 18 Prüfzeilen und die Zählzeilen aus `p_probe.txt`:

```
ja    t3_supertrend: 1 Tage aus der Rechnung nach 23.5, kein Tag gesetzt; SPAET 2025-05-31 vor dem Schnitt und nach den uebrigen (2023-06-01); Lauf nutzte die Rechnung (spur 2025-05-31)
ja    t3_supertrend: 2 rc S 0, rc O 0 (Wachen R86 (d), R87 (c) an)
ja    t3_supertrend: 3 Ausgaben S und O bytegleich (6116 Zeichen)
Zaehlzeile t3_supertrend: Zeilen S 58, O 58; von der Schranke entfernt 0; nur in S 0; SPAET-Trades 3, davon vor dem Tag 0, erster Einstieg 2025-11-26 16:00:00
ja    t3_supertrend: 4 Zaehlzeile entfernt 0, nur in S 0; SPAET traegt Trades ab dem Tag, keinen davor
ja    t3_supertrend: 5 Lesehaken: nur Snapshot-Dateien gelesen (S 5, O 5)
Zaehlzeile Gegenprobe t3_supertrend: mit Schranke rc 0, Zeilen 58; ohne Schranke und Wachen Zeilen 67; Zeilen nur ohne Schranke und Wachen 60
ja    t3_supertrend: 6 Gegenprobe beide Seiten (40.7, R110 (a)): SPAET mit Signal vor dem Tag -> ohne Schranke rc 2 ([positionen_holen] ABBRUCH t3_supertrend: Einstieg 2023-09-06 04:00:00 vor dem Handelbar-T); mit Schranke rc 0, Zaehlzeile (Zeilen nur ohne Schranke) 60
ja    elliott_wave: 1 Tage aus der Rechnung nach 23.5, kein Tag gesetzt; SPAET 2026-05-31 vor dem Schnitt und nach den uebrigen (2023-12-31); Lauf nutzte die Rechnung (spur 2026-05-31)
ja    elliott_wave: 2 rc S 0, rc O 0 (Wachen R86 (d), R87 (c) an)
ja    elliott_wave: 3 Ausgaben S und O bytegleich (1238 Zeichen)
Zaehlzeile elliott_wave: Zeilen S 11, O 11; von der Schranke entfernt 0; nur in S 0; SPAET-Trades 1, davon vor dem Tag 0, erster Einstieg 2026-07-03 23:00:00
ja    elliott_wave: 4 Zaehlzeile entfernt 0, nur in S 0; SPAET traegt Trades ab dem Tag, keinen davor
ja    elliott_wave: 5 Lesehaken: nur Snapshot-Dateien gelesen (S 5, O 5)
Zaehlzeile Gegenprobe elliott_wave: mit Schranke rc 0, Zeilen 11; ohne Schranke und Wachen Zeilen 15; Zeilen nur ohne Schranke und Wachen 11
ja    elliott_wave: 6 Gegenprobe beide Seiten (40.7, R110 (a)): SPAET mit Signal vor dem Tag -> ohne Schranke rc 2 ([positionen_holen] ABBRUCH elliott_wave: Einstieg 2024-12-03 21:00:00 vor dem Handelbar-Ta); mit Schranke rc 0, Zaehlzeile (Zeilen nur ohne Schranke) 11
ja    elliott_wave_stocks: 1 Tage aus der Rechnung nach 23.5, kein Tag gesetzt; SPAET 2024-01-01 vor dem Schnitt und nach den uebrigen (2012-12-31); Lauf nutzte die Rechnung (spur 2024-01-01)
ja    elliott_wave_stocks: 2 rc S 0, rc O 0 (Wachen R86 (d), R87 (c) an)
ja    elliott_wave_stocks: 3 Ausgaben S und O bytegleich (3055 Zeichen)
Zaehlzeile elliott_wave_stocks: Zeilen S 36, O 36; von der Schranke entfernt 0; nur in S 0; SPAET-Trades 2, davon vor dem Tag 0, erster Einstieg 2025-03-27 00:00:00
ja    elliott_wave_stocks: 4 Zaehlzeile entfernt 0, nur in S 0; SPAET traegt Trades ab dem Tag, keinen davor
ja    elliott_wave_stocks: 5 Lesehaken: nur Snapshot-Dateien gelesen (S 4, O 4)
Zaehlzeile Gegenprobe elliott_wave_stocks: mit Schranke rc 0, Zeilen 36; ohne Schranke und Wachen Zeilen 40; Zeilen nur ohne Schranke und Wachen 25
ja    elliott_wave_stocks: 6 Gegenprobe beide Seiten (40.7, R110 (a)): SPAET mit Signal vor dem Tag -> ohne Schranke rc 2 ([positionen_holen] ABBRUCH elliott_wave_stocks: Einstieg 2020-08-07 00:00:00 vor dem Hande); mit Schranke rc 0, Zaehlzeile (Zeilen nur ohne Schranke) 25
Ergebnis: 18 von 18 bestanden
rc 0
```

`p_nachher.txt` wörtlich:

```
ja    unveraendert: research/exposure_messung/bot_lauf.py md5 01fd9282ded2
ja    unveraendert: research/faltenplan_neun/faltenschranke_messung.py md5 584d9ff959da
ja    unveraendert: research/tb24_haltedauern/haltedauer_kern.py md5 60942de99b32
ja    unveraendert: research/tb24_haltedauern/positionen_holen.py md5 006375593b4b
ja    unveraendert: research/tb24_haltedauern/test_listen_erzeuger.py md5 d77e73ed5ff7
ja    unveraendert: strategies/elliott_wave/multi_symbol_optimise.py md5 bf11370b140d
ja    unveraendert: strategies/elliott_wave_stocks/multi_symbol_optimise.py md5 571076168d56
ja    unveraendert: strategies/t3_supertrend/multi_symbol_optimise.py md5 dc85993e8d42
ja    Probe im Repo = Anhang B (sha256 1fe6f12ef5f47603)
ja    R110 (a) t3_supertrend: 6 von 6 (Abnahme am Erzeuger)
ja    R110 (a) elliott_wave: 6 von 6 (Abnahme am Erzeuger)
ja    R110 (a) elliott_wave_stocks: 6 von 6 (Abnahme am Erzeuger)
ja    p_probe.txt: 18 von 18, rc 0; Gegenprobe beide Seiten mit Zaehlzeile
Pruefungen: 13, NEIN: 0
rc 0
```

Nach P lagen nur die drei neuen Dateien unter `docs/belege/TB-178/` im Arbeitsbaum.

**Folge nach R110 (a):** Die Abnahme am Erzeuger steht — Probe mit sha256 im Repo, 6 von 6 je Bot, Gegenprobe beide Seiten. Damit ist nach dem Wortlaut von R110 (a) **die Bedingung des Tags aus R105 (c) für t3_supertrend, elliott_wave und elliott_wave_stocks erfüllt und R107 (b) erledigt.** Ins Register ist das nicht eingetragen (70.2 (a) verweist hierher).

## Offen

- **R110 (b):** Bauauftrag nach 37.3 in vier Schritten — Nachtrag zu Punkt 9 (`shared/handelskosten.py` mit Pfad, drei Bezeichnern, Hash), Konstante `STARTING_CAPITAL`, neues Abbild unter neuem Namen, Ergänzung zu 29.3 nach R109 (a) mit den neun Fundstellen aus 68.2 (a) und Commit. Handelscode, Vorschlag TB-180, frischer Gegenleser Pflicht.
- **R110 (c):** Probe in `shared/test_ergebniskurven.py` (Mutation am Ort, genau einmal; alle neun Kurven weichen ab, zurückgesetzt bytegleich); mit TB-180.
- **R109 (a):** Der Registertext zu 29.3 ist nicht eingetragen; er folgt dem Bauauftrag nach R110 (b).
- **Das Ob aus R110 (a):** „ob eine andere Abnahme in 64.1 allein auf 3b steht“ — nicht gemessen.

BACKLOG Rang 1 trägt den Stand (`a_backlog.txt`, 1/0, rc 0); Journal FO (`a_journal.txt`, 3/0, rc 0).

## In einfacher Sprache

Die Sitzung hat zwei neue Antworten des Verfahrensprüfers mit Anfrage und Übergabe unverändert ins Repo gelegt und ihre Regeltexte R109 und R110 wortgleich als Abschnitte 69 und 70 ins Register geschrieben, nur angehängt, dazu zehn Hinweise an älteren Stellen. Danach hat sie an erfundenen Kursdaten mit einem spät beginnenden Symbol geprüft, was die Schranke am Handelbar-Tag bei t3_supertrend und den beiden Elliott-Bots bewirkt: Liegt vor dem Tag kein Signal, ändert sie nichts (Ergebnisse Zeichen für Zeichen gleich); liegt eines vor, greift sie, und ohne sie bricht der Lauf ab. Alle 18 Prüfungen sind grün. Wo das Startkapital im Code seinen festen Ort bekommt, ist ein Eingriff in Handelscode und kommt als eigener Auftrag.
