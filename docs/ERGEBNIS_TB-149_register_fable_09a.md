# TB-149: Ergebnis. Register Abschnitt 56 — Fable 09a (R84–R89) zeichengleich, Tatsachennotizen 56.7–56.8, 31 Marken am alten Ort an 21 Orten (5 davon nachgetragen nach R89 (d)), numstat 187/0; vorher gemessen: Anfrage, Eröffnungstext und Antwort 09.10.a mit Commit im Repo (R88 (g)) und an keinem Ort schon eine Marke zum Block der neuen; zwei BACKLOG-Blöcke; Registerkopie neu in 57 Abschnittsdateien und 5 Teilen, Index und Dialog-Index nachgezogen

**Sitzungstitel:** `TB-149` · **Stand:** 10.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-149_register_fable_09a.md` ·
**Belege:** `docs/belege/TB-149/`
**Eingang:** `15775a7` (TB-148, F; = `origin/main`), Arbeitsbaum wie 0a (drei Einträge). Commits: `c71dca9` (Schritt 0,
im Folgenden ⟨S0⟩), `ca687fc` (0: Ausgang, Vorprüfung, umgestellte Skripte), `d950e03` (A: Register, einziger
Registercommit), `21ec3f5` (B/C: BACKLOG, Registerkopie, Index, Dialog-Index), der Abgabe-Commit (D: dieses Dokument,
Journal EO) und ein kleiner Commit mit `d3_porcelain.txt`. Nach jedem Commit gepusht, jeder Push im ersten Versuch.
**⟨S0⟩ im Wortlaut:** `c71dca9` · **⟨DATUM⟩ im Wortlaut:** `10.10.2026` (`a4_datum.txt`, gemessen zu Beginn von A4 mit
`TZ=Europe/Berlin date +%d.%m.%Y`; derselbe Tag wie in 0a und 0d; die Sitzung lief von etwa 12:15 bis nach 12:40, kein
Tageswechsel).
**Quelle (md5 am ⟨S0⟩ und im Arbeitsbaum geprüft, `0b_ausgang.txt`):**
`docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md`,
`a6e5d3d277c5d4069b443a8f8f9df17f`, 52 721 B — gleich dem Soll; im Repo seit `7f0b59d`. Geschnitten nur aus dieser
Datei (Z. 216–232).
**Freigabe:** Betreiber, 10.10.2026 (Auswahlkarte im steuernden Chat, gestellt nach 11:24, eingetragen 11:26),
„Ja, freigeben (Empfohlen)“ (wörtlich im Auftrag). **Keine Rückfrage an den Betreiber.**
**Umgebung:** Mac, Hauptordner `~/trading-bot`, lokal; `trading-env/bin/python3` (3.9.6). Gestartet über den Einfügesatz
`TB-149: …`. Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst. Claude Code hat keinen Aufruf abgelehnt und keine Bestätigung verlangt.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a Arbeitsbaum | genau die drei Einträge des Auftrags; HEAD `15775a7` | genau diese drei (`0a_status.txt`); HEAD `15775a7` |
| 0a Skripte | sha256 `8e49504e…` (Prüfskript), `36f66703…` (Einfügeskript), `edd006b4…` (Umstellskript) | alle drei gleich; nach dem Kopieren nach `0d_vorpruefung.py`, `a4_eintrag.py`, `tb149_umstellen.py` noch einmal gleich |
| 0a Prüfskript `--arbeitsbaum` | rc 0; nach der Datumszeile geändert 2 / unverfolgt 1; Zeilen `Dateien 09.10.a …`, `Orte: …`, `Marken:` … `Bloecke:`, `Dateien:` wie „Prüfsumme“ | rc 0; genau so (`0a_pruefung.txt`; `*.py im Baum: 747`, kein Soll) |
| 0a Punkt 3 Umstellen | rc 0, 20 Zeilen `ok`, `Skripte: 20, Abweichungen: 0` | genau so; jede sha256 gleich der Tabelle „Übernommene Skripte“ (`0a_umstellen.txt`) |
| 0b | 11 733 Z., sha256 `ab97ae1e…`, md5 `eb7c3470…`; `register()` `ee6947a6…`, `fehlend []`, 23 Teile; Abbild `46f0ad5d…`; Sonde rc 2, 37/0/0, (ii) 0, Listentext ja; Quelle 09a `a6e5d3d2…`/52 721 B am ⟨S0⟩ und im Arbeitsbaum; Abschnitt 10 und ERZEUGT gleich `TB-139/0b_*_nachher.txt` | alles gleich (`0b_ausgang.txt`); Sonde-JSON ohne `zeilen` `9f7364ef…`; `registerbericht.py --pruefen` rc 1 (bekannt, Vergleichswert); Abschnitt 10 Z. 971–1177, ERZEUGT Z. 260–460, beide `cmp`-gleich mit den Dateien aus TB-139 |
| 0c | `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` | leer ⇒ Basis `docs/belege/TB-139/a5_test_vorregistrierung.txt` (196/196), kein eigener Basislauf |
| ⭐⭐ 0d | rc 0, Datumszeile, `Dateien 09.10.a …`, `Orte: …`, fünf Zeilen wie „Prüfsumme“, `rc 0: alles wie angegeben` | genau so (`0d_vorpruefung.txt`; `*.py im Baum: 764`, kein Soll); siehe „Vorprüfung“ |
| A4 | `git diff --quiet ⟨S0⟩ -- Auftrag Quelle Anfrage Eröffnungstext` rc 0; Probelauf an Kopie grün, dann echt, `cmp` gleich; `31 an 21`, `6 (R84-R89)`, `11733 → 11920, 187` | rc 0; Probelauf und echter Lauf je genau diese Ausgabe, `sha256 nachher:` in beiden `b2d56949…`; `cmp` rc 0; die Wachen (Block am Ort, Platzhalter) liefen in beiden Läufen ohne Meldung |
| A5 R-Diff | 6/6 rc 0; Mutation erkannt | **6/6**; `a5_r_diff.py` an der mutierten Kopie rc 1 (`a5_mutation.py` rc 0) |
| A5 Zitate | 2/2 | Kopf 56.0 und Schluss 56.7–56.8 **2/2** |
| A5 Überschriften/Ketten, Marken | 6/6, 31/31 | **6/6 und 6/6**, **31/31**, jede Markenzeile einmal (`TB-149, 10.10.2026` 31-mal); in Abschnitt 9, 10 und ERZEUGT-Block je 0; Zeilen nachher gleich der Tabelle in A5 (31/31) |
| A5 numstat, Zeilen | `187	0`, 11 920 | **187/0**, 11 920 |
| A5 Abschnitt 10, ERZEUGT | bytegleich gegen 0b | beide gleich; Abschnitt 10 Z. 971–1177, ERZEUGT Z. 260–460 (wandern nicht) |
| A5 `registerbericht --pruefen` | nachher = vorher | rc 1 / rc 1, Ausgabe bytegleich |
| A5 Sonde | JSON ohne `zeilen` gleich, (ii) 0, Listentext ja | `9f7364ef…` gleich, (ii) 0, ja; Sonde-Text vorher/nachher ohne Unterschied (`diff` rc 0) |
| A5 `register()` | ≠ vorher, `fehlend []`, 23 Teile | `1ddb56ee…`, `[]`, 23 |
| A5 `test_vorregistrierung` | 196/196, am echten Register vor dem Commit, ohne Zeitgrenze | **196/196**, rc 0, 905 s (`a5_test_vorregistrierung.txt`) |
| A Commit | genau Register und die A-Belege; keine Ausgabe für B, C, D | so (`a_commit.txt`: 14 Dateien); `a_commit.txt` selbst im Commit B/C |
| B | E1, E2: Probe je `vorher 1`, Ankerzeile 384, Textzeilen 9 und 9; Anker 1, Text nachher 1, je GLEICH; numstat `20	0` | Probe genau so (während des Tests, ohne Schreiben); eingefügt: je `Anker vorher 1 · ausgeführt ja · Text nachher 1`; Vergleich zweimal GLEICH, `alle zeichengleich, je genau einmal`; **20/0** |
| C1 | fünf Aufrufe rc 0; 57 Abschnittsdateien `_00`–`_56`; T1 220 839, T2 222 662, T3 232 851, T4 239 683, T5 145 682 B | alle fünf rc 0; Zuschnitt und Grössen **auf das Byte wie erwartet**, bytegleich; **57** Abschnittsdateien, bytegleich |
| C2 | Index nachgezogen (Liste Nr. 1 bis 11, Abschnitt 11, Pflegezeile) | 348 Zahlen in Zeilenangaben umgeschrieben (199 geändert), 7 Ersetzungen, 8 Tabellenzeilen und neue Zeile 56 in Tabelle 4, je Anker 1; Abschnitt 11 mit 31 Marken; Abschnittstabelle 0–56 aus den Köpfen; numstat 227/171 |
| C3 | vorher `Indexzeilen aus Fable 09a` 0; drei Zeilen zeichengleich | 0 vorher (vor C2 gezählt und im Skript vor C3); Block eingesetzt, 3/3 zeichengleich |
| C2/C3 Gegenprobe | rc 0 | rc 0: 410/410 Zeilenangaben auf Markenzeilen; 14/14, 12/12, 21/21, 15/15, 20/20, **31/31** (Abschnitt 6–11); C3 zeichengleich; Indexzeilen 01a 5; Indexzeilen E-2 6; 57/57 Tabellenzeilen (`c2_index_pruefen.txt`) |
| C4 | `--pruefen` rc 0; 58 Antworten; 09a Fundstelle 56; 07a unverändert (55) | rc 0 / rc 0; Schlüssel `09a` wie erwartet; Handfelder `cmp` gleich dem Auftrag; Zeile 09a: Status offen, Fundstelle 56, offen „ja“; „58 Antworten.“; numstat 2/1: die neue Zeile und die Schlusszeile — **keine weitere Zeile geändert** |
| D2 | Kennung EO, J1 GLEICH | letzte Kennung vorher EN, `## EO ` vorher 0; Block gesetzt; J1 Probe einsetzbar, dann eingesetzt (8 Zeilen), Vergleich GLEICH, rc 0; numstat Journal 48/0 |

## Umstellen der Skripte (0a Punkt 3)

`trading-env/bin/python3 docs/belege/TB-149/tb149_umstellen.py > docs/belege/TB-149/0a_umstellen.txt` ⇒ rc 0. Die
Ausgabe (20 Zeilen `ok`, je mit dem sha256 der Tabelle „Übernommene Skripte“; Zahl der Ersetzungen; alle Vorlagen unter
`docs/belege/TB-139/`):

```
ok   0b_ausgang.sh f57f31e6… (7)              ok   c1_registerkopie.sh f007ccf8… (1)
ok   a4_probelauf.sh 4df2bdf4… (6)            ok   c2_index_09a.py 58019d4f… (5, TB-139/c2_index_07a.py)
ok   a5_marken.py b4b8167c… (6)               ok   c2_index_eintraege.py 5f1eefde… (28)
ok   a5_mutation.py cc49bad7… (5)             ok   c2_index_pruefen.py 63a579de… (13)
ok   a5_nachweis.sh 004d3139… (2)             ok   c2_index_zeilen.py fce1dc96… (2)
ok   a5_r_diff.py cc059839… (10)              ok   c3_indexzeilen.py 992f3d55… (8)
ok   a5_zitate.py 08b9a851… (9)               ok   c4_dialog_index.sh 38fd07be… (6)
ok   b_einfuegen.py b8ac955e… (3)             ok   d2_journal.py 3e7506e7… (5)
ok   b_vergleich.py 10ef52bf… (3)             ok   j1_einsetzen.py f6d0a088… (5)
                                              ok   j1_vergleich.py 33ea34b3… (3)
                                              ok   test_vorregistrierung.sh 01b4f2a0… (2)
Skripte: 20, Abweichungen: 0
```

(Hier zweispaltig und gekürzt; die volle Ausgabe mit ganzen sha256 steht in `0a_umstellen.txt`.) Kein `FEHL`, kein
Skript von Hand umgestellt. 129 Ersetzungen.

## Vorprüfung (0d; R88 (g), R56 (b), R89 (b) und (d))

`trading-env/bin/python3 docs/belege/TB-149/0d_vorpruefung.py docs/auftraege/MAC_TB-149_register_fable_09a.md .
--datum 10.10.2026` am Commit ⟨S0⟩, ohne `--arbeitsbaum` ⇒ rc 0. Die Ausgabe im Wortlaut (`0d_vorpruefung.txt`):

```
Datum des Eintrags: 10.10.2026 (aus --datum)
Dateien 09.10.a (R88 (g), R56 (b)): 3 von 3 von git verfolgt, Arbeitsbaum gleich HEAD, dazugekommen in 7f0b59d, md5 und Bytes wie im Daten-Block
Orte: 21 Anker, je genau einmal: True; Zeilen am Ort (Anker bis vor die naechste Ueberschrift), die den Block der neuen Marke nennen (R89 (b), (d)): 0; Zeilen mit R84 bis R89 im Register: 0
Marken: 31 an 21 Einfuegestellen
je Abschnitt: 23: 1, 40: 1, 41: 1, 48: 13, 52: 1, 53: 3, 54: 3, 55: 8
Anker mit Zahl 1 (Original): 31 von 31
Anker mit Zahl 1 (nach Simulation): 31 von 31
Bloecke: 6 | Ueberschriften: 6 max. Laenge 140 | gekuerzt: 5
Dateien: 0 | Fundstellen: 29 | Zeilenlisten: 0 | Zaehlungen: 19 | *.py im Baum: 764
rc 0: alles wie angegeben
```

Damit hat die Sitzung vor dem Eintrag selbst gemessen:

- **Die drei Dateien 09.10.a** (Anfrage `FABLE_ANFRAGE_2026-10-09a_kern_marken_listen_handelbar_tag.md`, Eröffnungstext
  `FABLE_UEBERGABE_2026-10-09_eroeffnung.md`, Antwort `FABLE_ANTWORT_2026-10-09a_…`) sind von git verfolgt, im Commit
  `7f0b59d` dazugekommen, im Arbeitsbaum gleich HEAD und tragen md5 und Bytes wie im Daten-Block — R88 (g) und R56 (b)
  erfüllt.
- **An 48.14 (R46) nennt keine Zeile R60, R64, R66 oder R67, an 48.7 (R39) keine Zeile R81**, und an keinem der übrigen
  19 Orte nennt eine Zeile vom Anker bis vor die nächste Überschrift den Block der neuen Marke (0 Zeilen) — keine der
  fünf Marken aus R89 (d) und keine der 26 aus R89 (g) stand schon.
- **Jeder der 21 Orte ist genau einmal vorhanden**; R84 bis R89 kamen vor dem Eintrag in keiner Registerzeile vor.

Die Prüfung lief schon in 0a einmal am Arbeitsbaum (mit `--arbeitsbaum`, `0a_pruefung.txt`), mit demselben Ergebnis.
`git status --porcelain` danach: neu nur Dateien unter `docs/belege/TB-149/`.

## `herkunft.register()`

| | Wert |
|---|---|
| vorher (Register `ab97ae1e…`, 11 733 Z.) | `ee6947a611b71407605e9db1e3626f3597ffea1caf0d81a82c0b0ab64ff8f018` |
| nachher (Register `b2d56949…`, 11 920 Z.) | `1ddb56eec9a2da60270d9b49d27702cbc20583045256fe88caade62d6f7a1fee` |

`fehlend []` und 23 Teile vorher wie nachher. Der neue Wert steht nur hier, nicht im Register (42.5).

## Register nachher

11 920 Zeilen · sha256 `b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687` ·
md5 `4359577a57f2888949b10073b1aec755` — gerechnet mit ⟨S0⟩ = `c71dca9` und ⟨DATUM⟩ = `10.10.2026`; Probelauf an der
Kopie und echter Lauf nennen denselben sha256, `cmp` rc 0. Abschnitt 56 steht in Z. 11828–11920 (56.1 Z. 11832, 56.2
Z. 11839, 56.3 Z. 11846, 56.4 Z. 11853, 56.5 Z. 11860, 56.6 Z. 11867, 56.7 Z. 11874, 56.8 Z. 11898) — wie im Auftrag
gerechnet. ⟨S0⟩ ist im Register als `` `c71dca9` `` eingesetzt (einmal, im Kopf), das Datum einmal im Kopf
(„Eingetragen am 10.10.2026.“) und in jeder der 31 Markenzeilen. Kein Platzhalter `⟨S0⟩` oder `⟨DATUM⟩` steht im
Register.

## Wie eingetragen

- Einfügeskript aus Anhang A, unverändert (`a4_eintrag.py`, sha256 `36f66703…`), Probelauf mit `--s0 c71dca9 --datum
  10.10.2026 --register <Kopie im Scratch>` über `a4_probelauf.sh`, danach echt mit `--s0 c71dca9 --datum 10.10.2026
  --daten docs/belege/TB-149/a4_eintrag_daten.json`. `--vorschau` nicht benutzt.
- Nachweise mit den umgestellten Skripten `a5_*` über `a5_nachweis.sh`; sie lesen Auftrag und Quelle selbst per
  `git show c71dca9:…`.
- Ausgang und Nachher-Messung mit demselben Skript `0b_ausgang.sh`, `vorher` bzw. `nachher` (`0b_ausgang.txt`,
  `0b_nachher.txt`; an `0b_nachher.txt` sind die Vergleiche vorher/nachher angehängt, Bauart TB-139).
- `test_vorregistrierung` lief im Hintergrund am echten Register vor dem Commit A; währenddessen liefen nur lesende
  Prüfungen (`a5_nachweis.sh`, `0b_ausgang.sh nachher`) und `b_einfuegen.py --probe`, ohne Schreiben in BACKLOG, Index
  oder Kopie.
- Index: `c2_index_zeilen.py c71dca9 d950e03`, `c2_index_09a.py c71dca9 10.10.2026`, `c2_index_eintraege.py c71dca9
  d950e03 10.10.2026`, `c3_indexzeilen.py c71dca9`, Gegenprobe `c2_index_pruefen.py c71dca9 10.10.2026`.
- Dialog-Index: `c4_handfelder.json` mit dem awk-Ausdruck aus `c4_dialog_index.sh` aus dem Codeblock C4 des Auftrags am
  ⟨S0⟩ geschnitten (nicht abgetippt; `cmp` gegen den Auftrag: ja), dann `c4_dialog_index.sh c71dca9 <scratch>`.
- Journal: `d2_journal.py` (Block aus `d2_journal_block.md`), dann `j1_einsetzen.py --kennung EO --probe`, ohne
  `--probe`, `j1_vergleich.py --kennung EO`.

## Registerkopie

| Teil | Abschnitte | Bytes | Body | Luft bis 240 000 (Body + 240) | vorher (TB-139) |
|---|---|---|---|---|---|
| T1 | 0–22 | 220 839 | 220 604 | 19 156 | 220 839 (keine Marke) |
| T2 | 23–36 | 222 662 | 222 426 | 17 334 | 222 495 (+167, Marke an 23.3) |
| T3 | 37–42 | 232 851 | 232 615 | 7 145 | 232 575 (+276, Marken an 40.6 und 41.3 C2) |
| T4 | 43–53 | 239 683 | 239 447 | **313** | 236 927 (+2 756, 17 Marken) |
| T5 | 54–56 | 145 682 | 145 446 | 94 314 | 86 600 (54–55; +11 Marken, + Abschnitt 56) |

Der Zuschnitt ist genau der erwartete aus C1 (alle fünf Grössen auf das Byte); kein Abschnitt 0–55 wechselt den Teil,
kein sechster Teil, die Spalte T im Index bleibt für 0–55 gleich. **Luft je Teil nachher: T1 19 156 B, T2 17 334 B, T3
7 145 B, T4 313 B, T5 94 314 B.** ⚠️ **T4 hat nur noch 313 B Luft**: Die 17 Marken dieses Auftrags brachten im Mittel
rund 162 B je Marke nach T4 (2 756 B); danach passt dort eine weitere Marke solcher Länge, eine zweite nicht mehr, und
das Werkzeug teilt neu. Bodies
aneinander 1 060 538 B, bytegleich mit dem Register am `d950e03` (`c1_registerkopie.txt`, `c1_pruefen.txt`,
`c1_abschnitte_pruefen.txt`). Abschnittsdatei `_56.md` neu, 57 679 B, im Commit B/C; die Dateien `_00` bis `_55` tragen
im Kopf den neuen Commit und sind deshalb alle geändert.

## Markentabelle (gegen Anhang A)

| Nr | alter Ort (Anhang A) | nach Z. (alt) | Marke Z. (neu) | Wort | durch | Art | T |
|---|---|---|---|---|---|---|---|
| 1 | 23.3, Registertext 3b (c) | 3960 | 3962 | PRÄZISIERT | R87 (56.4) | MARKE | 2 |
| 2 | 40.6 | 8438 | 8443 | PRÄZISIERT | R86 (56.3) | MARKE | 3 |
| 3 | 41.3, Eintrag C2 | 8896 | 8904 | ERGÄNZT | R86 (56.3) | MARKE+ | 3 |
| 4 | 48.1 (R33) | 10819 | 10830 | PRÄZISIERT | R85 (56.2) | MARKE | 4 |
| 5 | 48.4 (R36) | 10849 | 10863 | PRÄZISIERT | R85 (56.2) | MARKE | 4 |
| 6 | 48.7 (R39) | 10885 | 10902 | ERGÄNZT | R81 (55.4), nachgetragen nach R89 (d) | MARKE+ | 4 |
| 7 | 48.11 (R43) | 10916 | 10936 | ERGÄNZT | R87 (56.4) | MARKE+ | 4 |
| 8 | 48.12 (R44) | 10923 | 10946 | PRÄZISIERT | R86 (56.3) | MARKE | 4 |
| 9 | 48.13 (R45) | 10930 | 10956 | PRÄZISIERT | R84 (56.1) | MARKE | 4 |
| 10 | 48.14 (R46) | 10943 | 10972 | ERGÄNZT | R60 (51.5), nachgetragen nach R89 (d) | MARKE+ | 4 |
| 11 | 48.14 (R46) | 10943 | 10975 | ERGÄNZT | R64 (52.2), nachgetragen nach R89 (d) | MARKE+ | 4 |
| 12 | 48.14 (R46) | 10943 | 10978 | ERGÄNZT | R66 (53.1), nachgetragen nach R89 (d) | MARKE+ | 4 |
| 13 | 48.14 (R46) | 10943 | 10981 | ERGÄNZT | R67 (53.2), nachgetragen nach R89 (d) | MARKE+ | 4 |
| 14 | 48.14 (R46) | 10943 | 10984 | ERGÄNZT | R84 (56.1) | MARKE+ | 4 |
| 15 | 48.14 (R46) | 10943 | 10987 | ERGÄNZT | R85 (56.2) | MARKE+ | 4 |
| 16 | 48.14 (R46) | 10943 | 10990 | ERGÄNZT | R87 (56.4) | MARKE+ | 4 |
| 17 | 52.3 (R65) | 11398 | 11448 | PRÄZISIERT | R89 (56.6) | MARKE | 4 |
| 18 | 53.3 (R68) | 11471 | 11524 | PRÄZISIERT | R85 (56.2) | MARKE | 4 |
| 19 | 53.5 (R70) | 11491 | 11547 | PRÄZISIERT | R89 (56.6) | MARKE | 4 |
| 20 | 53.7 (R72) | 11514 | 11573 | PRÄZISIERT | R88 (56.5) | MARKE | 4 |
| 21 | 54.2 (R75) | 11589 | 11651 | PRÄZISIERT | R84 (56.1) | MARKE | 5 |
| 22 | 54.2 (R75) | 11589 | 11654 | PRÄZISIERT | R85 (56.2) | MARKE | 5 |
| 23 | 54.5, Zeile „R75 (54.2) (a)“ | 11624 | 11692 | ERGÄNZT | R84 (56.1) | MARKE+ | 5 |
| 24 | 55.1 (R78) | 11650 | 11721 | BERICHTIGT | R88 (56.5) | MARKE+ | 5 |
| 25 | 55.1 (R78) | 11650 | 11724 | PRÄZISIERT | R88 (56.5) | MARKE | 5 |
| 26 | 55.3 (R80) | 11664 | 11741 | ERGÄNZT | R88 (56.5) | MARKE+ | 5 |
| 27 | 55.3 (R80) | 11664 | 11744 | ERGÄNZT | R89 (56.6) | MARKE+ | 5 |
| 28 | 55.4 (R81) | 11671 | 11754 | ERGÄNZT | R86 (56.3) | MARKE+ | 5 |
| 29 | 55.4 (R81) | 11671 | 11757 | ERGÄNZT | R87 (56.4) | MARKE+ | 5 |
| 30 | 55.5 (R82) | 11678 | 11767 | BERICHTIGT | R88 (56.5) | MARKE+ | 5 |
| 31 | 55.6 (R83) | 11685 | 11777 | ERGÄNZT | R88 (56.5) | MARKE+ | 5 |

Quelle: `a4_eintrag_daten.json`, `a5_marken.txt`, `c1_marken.txt`, `c2_index_09a_tabelle.md`. 31 Marken an 21
Einfügestellen, an den 21 Orten nach R89 (d) und (g); die Zeilen nachher gleichen der Soll-Tabelle in A5 (31/31). Je
Markenwort PRÄZISIERT 13, BERICHTIGT 2, ERGÄNZT 16. **Keine eigene Marke des steuernden Chats** (E6). **Nicht gesetzt
nach Anhang A (wie vorgesehen):** die Statuslisten 54.6 und 55.8; die Orte aus R89 (e) und (h); die drei Kandidaten aus
56.8 Nr. 10 (55.7, 15.5, 45.5); 48.20 (R52), 54.3 (R76) und Abschnitt 10, Punkt 10 (Indexzeilen, Abschnitt 11 des
Index); keine Marke in Abschnitt 9, 10 und im ERZEUGT-Block.

## Für Fable (nur Verfahrensfragen)

1. **56.8 Nr. 9, zur Kenntnis:** die drei Lesarten des steuernden Chats L1 („Unsicher“ 10 gegen den Block R84 (e)), L2
   (Lesart A in 15.5) und L3 (45.5, R5) und die zwei Befunde zur Form B1 (der Wortlaut, den R88 (e) „in R72 (d) und R78
   (d)“ zitiert, steht dort nicht so) und B2 (Schreibweise und Bytesumme im Antworttext). Ob ein Befund nach R76 (e)
   zählt, entscheidet Fable.
2. **56.8 Nr. 10:** Kandidaten für eine Marke, nicht gesetzt — 55.7, Zeile „R78 (55.1) (a), erste“, zu R88 (b) und (c);
   15.5 zu R87 (a); 45.5 (R5) zu R86 (d). Eine fehlende Marke lässt sich nachtragen.
3. **56.8 Nr. 11:** weiter vierzehn gezählte Fälle (R88 (f)), geführt als Indexzeilen an 48.20 (R52) und 54.3 (R76).
4. **56.8 Nr. 12:** Die nächste Anfrage geht an einen neuen Fable-Chat (Umzugsampel der Antwort 09.10.a rot).
5. **56.8 Nr. 14 bis 17, zur Kenntnis:** R87 (d) verweist auf „25c (1)“, 42.3 führt F1 (a) bis F8 (h); R86 (d) nennt
   R46 (48.14) als Bauart, R89 (g) verlangt dort keine Marke zu R86; R88 (f) nennt 55.7, R89 nennt 55.7 nicht; R88 (e)
   nennt 27.2, das ohne eigene Überschrift in 27.1 bis 27.5 steht.
6. **Reibung beim Setzen, Werkzeug (wie TB-129 bis TB-139):** `registerkopie.py --marken` zählt in Abschnitt 56 elf
   Zeilen mit, die keine Marken sind: sechs Überschriften mit Rückverweis (56.1 bis 56.6, Z. 11832, 11839, 11846, 11853,
   11860, 11867; `UEBERSCHRIFT`), die Blockzeile von R89 (Z. 11869, `MARKE`) und vier Tabellenzeilen von 56.7 (Z. 11885,
   11887, 11892, 11895; `MARKE+`). Damit stehen die Arten bei `MARKE` 114 = 100 + 13 + 1, `MARKE+` 167 = 145 + 18 + 4,
   `UEBERSCHRIFT` 102 = 96 + 6 — genau wie im Auftrag erwartet. Im Index ist keine der elf Zeilen als Marke geführt.
7. **Keine Reibung zwischen Fable-Text und Register beim Setzen gefunden**, die über 56.7 und 56.8 hinausgeht: jeder der
   21 Anker kam genau einmal vor, an keinem Ort stand schon eine Zeile zum Block der neuen Marke, die Schnittregel ergab
   genau R84–R89 in Z. 216–232.

## Nicht getan

- 56.8 (alle 17 Punkte): insbesondere die Messungen vor dem Bau (Nr. 2 bis 6; TB-148 hat sie durch Lesen gemessen, ihr
  Ergebnis ist nicht Gegenstand dieser Sitzung), der Bau der zwei Erzeuger mit Summenprobe, Drawdown, Schnitt, Wachen
  und Proben (Nr. 7), die Freigabe nach 37.3 für die Rückgabe nach R45 samt `shared/test_zuteilung.py` (Nr. 8), die
  Anfragen an Fable (Nr. 9, 10, 12, 14 bis 17).
- Kein Code gelesen, keine Voraussetzung neu gemessen; die strengere Fassung der Summenprobe nicht eingetragen (E3).
- Die Ablage (57 Abschnittsdateien, fünf Teile, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`) — macht der steuernde Chat.
- Kein Code, kein neues Abbild, kein zweiter Snapshot, nichts an `snapshots/` oder `data/`, keine Läufe von
  `auswertung.py`, Zellen-Erzeugern oder Backtests; `UEBERGABE.md` und die `FABLE_*`-Quellen nicht geändert (nur in
  Schritt 0 committet).
- `registerbericht.py --pruefen` rc 1 bleibt (schon vor TB-126; Zahlenteil veraltet).

## Nebenbemerkungen zum Ablauf

- `test_vorregistrierung` brauchte 905 s (TB-139: 919 s).
- `b_vergleich.txt` endet mit einer Restzeile ` 2 · Gesamt: alle zeichengleich, je genau einmal`: Das Skript schreibt die
  Datei selbst, und die Umleitung der Standardausgabe auf dieselbe Datei überlagert sie. Dieselbe Restzeile steht in
  `docs/belege/TB-139/b_vergleich.txt`. Der Inhalt davor ist vollständig und richtig (zweimal GLEICH).
- Der Index-Diff ist mit 227/171 gross, weil `c2_index_zeilen.py` 199 Zeilenangaben auf den neuen Stand umschreibt (die
  Marke an 23.3 verschiebt alles danach); inhaltlich neu sind nur die Einträge aus C2/C3.
- Index-Kopf „*Frühere Vierteilung*“ nennt weiter „T1“ … „T4“, die Liste danach fünf Teile (bekannt seit TB-136).
- Der Zeilenzähler der Sonde (`git status --porcelain` vorher/nachher) zeigt 1 bzw. 12 Zeilen: die Belege der Sitzung
  und das geänderte Register.

## In einfacher Sprache

Die Sitzung hat zuerst den Auftrag und die Unterlagen des steuernden Chats ins Repo gesichert. Dann hat sie selbst
nachgemessen, dass Fables Antwort vom 09.10. samt Anfrage und Eröffnungstext schon mit einem Commit im Repo liegt und
dass an keiner der 21 alten Stellen schon ein Hinweis auf die neuen Texte steht — beides traf zu. Erst danach hat sie
Fables sechs Regeltexte (R84–R89) Zeichen für Zeichen ins Register kopiert, als Abschnitt 56, mit der Tabelle der
Vormessungen und der Liste der offenen Punkte. An 21 alten Stellen weisen 31 kleine Marken auf die neuen Texte; fünf
davon trägt Fable für ältere Texte nach. Kein alter Satz wurde geändert (187 Zeilen dazu, 0 weg). Alle Prüfungen und der
grosse Registertest (196/196) sind grün. Danach sind die Aufgabenliste, die Kopie des Registers für die Ablage (jetzt
57 Dateien und fünf Teile; Teil 4 ist fast voll), der Wegweiser und die Liste der Fable-Antworten erneuert. Am Code und
an den Daten hat sich nichts geändert.
