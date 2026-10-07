# TB-139: Ergebnis. Nachlesen der Voraussetzungen an Zwischenstand und Ergebnis TB-140 (V4 und V5 „erfüllt“, rc 0); Register Abschnitt 55 — Fable 07a (R78–R83 in der Fassung 07.10.a) zeichengleich, Tatsachennotizen 55.7–55.8, 20 Marken am alten Ort, die Fassung 06.10.a nicht eingetragen, numstat 152/0; zwei BACKLOG-Blöcke; Registerkopie neu in 56 Abschnittsdateien und 5 Teilen, Index und Dialog-Index nachgezogen

**Sitzungstitel:** `TB-139` · **Stand:** 07.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-139_register_fable_07a.md` ·
**Belege:** `docs/belege/TB-139/`
**Eingang:** `b07ec7d` (TB-140, D3; = `origin/main`), Arbeitsbaum wie 0a (sechs Einträge). Commits: `e16872e` (Schritt 0,
im Folgenden ⟨S0⟩), `35b4743` (0: Ausgang, Vorprüfung, Nachlesen der Voraussetzungen, umgestellte Skripte), `ad1fc0d`
(A: Register, einziger Registercommit), `be2fa85` (B/C: BACKLOG, Registerkopie, Index, Dialog-Index), der Abgabe-Commit
(D: dieses Dokument, Journal EI) und ein kleiner Commit mit `d3_porcelain.txt`. Nach jedem Commit gepusht, jeder Push im
ersten Versuch.
**⟨S0⟩ im Wortlaut:** `e16872e` · **⟨DATUM⟩ im Wortlaut:** `07.10.2026` (`a4_datum.txt`, gemessen zu Beginn von A4 mit
`TZ=Europe/Berlin date +%d.%m.%Y`; derselbe Tag wie in 0a und 0d; die Sitzung lief von 22:57 bis nach 23:20, kein
Tageswechsel bis zum Registercommit).
**Quelle (md5 am ⟨S0⟩ und im Arbeitsbaum geprüft, `0b_ausgang.txt`):**
`docs/projektfuehrung/FABLE_ANTWORT_2026-10-07a_schnitt_im_erzeuger_wache_ein_eintrag.md`,
`388187e2a69218fbe5077e3f0bc1815f`, 57 165 B — gleich dem Soll. Geschnitten nur aus dieser Datei (Z. 227–243).
**Freigabe:** Betreiber, 07.10.2026 (Auswahlkarte im steuernden Chat, gestellt gegen 22:05, eingetragen 22:44),
„Ja, freigeben (Empfohlen)“ (wörtlich im Auftrag). **Keine Rückfrage an den Betreiber.**
**Umgebung:** Mac, Hauptordner `~/trading-bot`, lokal; `trading-env/bin/python3` (3.9.6). Gestartet über den Einfügesatz
`TB-139: …`. Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a Arbeitsbaum | genau die sechs Einträge des Auftrags; HEAD `b07ec7d` | genau diese sechs (`0a_status.txt`); HEAD `b07ec7d` |
| 0a Skripte | sha256 `e42483a2…` (Prüfskript), `fea5ca29…` (Einfügeskript), `534051b5…` (Umstellskript) | alle drei gleich; nach dem Kopieren nach `0d_vorpruefung.py`, `a4_eintrag.py`, `tb139_umstellen.py` noch einmal gleich |
| 0a Prüfskript `--arbeitsbaum` | rc 0 | rc 0; `Datum des Eintrags: 07.10.2026 (aus --datum)`, Arbeitsbaum geändert 2 (Soll 2), unverfolgt 4 (Soll 4); die fünf Zeilen `Marken:` … `Bloecke:` und `Dateien:` bis vor `*.py im Baum` wie unter „Prüfsumme“ (`0a_pruefung.txt`; `*.py im Baum: 725`, kein Soll) |
| 0a Punkt 3 Umstellen | rc 0, 20 Zeilen `ok`, `Skripte: 20, Abweichungen: 0` | genau so; jede sha256 gleich der Tabelle „Übernommene Skripte“ (`0a_umstellen.txt`, siehe unten) |
| 0b | 11 581 Z., sha256 `8d505a38…`, md5 `757cda8c…`; `register()` `cfff54ca…`, `fehlend []`, 23 Teile; Abbild `46f0ad5d…`; Sonde rc 2, 37/0/0, (ii) 0, Listentext ja, JSON ohne `zeilen` `9f7364ef…`; Quelle 07a `388187e2…`/57 165 B am ⟨S0⟩ und im Arbeitsbaum; Abschnitt 10 `da8697c0…`, ERZEUGT `fda8ead1…` | alles gleich (`0b_ausgang.txt`); `registerbericht.py --pruefen` rc 1 (bekannt, Vergleichswert); Abschnitt 10 Z. 965–1171, ERZEUGT Z. 260–460 |
| 0c | `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` | leer ⇒ Basis `docs/belege/TB-136/a5_test_vorregistrierung.txt` (196/196), kein eigener Basislauf |
| 0d | rc 0, erste Zeile `Datum des Eintrags: <TT.MM.JJJJ> (aus --datum)`, fünf Zeilen wie „Prüfsumme“, `rc 0: alles wie angegeben` | genau so (`0d_vorpruefung.txt`; `*.py im Baum: 742`, die Skripte der Sitzung dazu; kein Soll) |
| ⭐⭐ 0e | jede `ok`/`FEHL`-Zeile beginnt mit `ok`; `rc 0: Voraussetzungen wie in 55.7`, `rc 0` | **46 von 46 Zeilen `ok`**, beide Schlusszeilen wie Soll (siehe unten) |
| A4 | `git diff --quiet ⟨S0⟩ -- Auftrag Quelle Anfrage Eröffnungstext` rc 0; Probelauf an Kopie grün, dann echt, `cmp` gleich; `20 an 14`, `6 (R78-R83)`, `11581 → 11733, 152` | rc 0; Probelauf und echter Lauf je genau diese Ausgabe, `sha256 nachher:` in beiden `ab97ae1e…`; `cmp` rc 0; die Wachen zu R79 (a), R79 (b) und zu Platzhaltern liefen in beiden Läufen |
| A5 R-Diff | 6/6 rc 0; Mutation erkannt | **6/6**; `a5_r_diff.py` an der mutierten Kopie rc 1 (`a5_mutation.py` rc 0) |
| A5 Zitate | 2/2 | Kopf 55.0 und Schluss 55.7–55.8 **2/2** |
| A5 Überschriften/Ketten, Marken | 6/6, 20/20 | **6/6 und 6/6**, **20/20**, jede Markenzeile einmal (`TB-139, 07.10.2026` 20-mal); in Abschnitt 9, 10 und ERZEUGT-Block je 0; Zeilen nachher gleich der Tabelle in A5 (20/20) |
| A5 numstat, Zeilen | `152	0`, 11 733 | **152/0**, 11 733 |
| A5 Abschnitt 10, ERZEUGT | bytegleich gegen 0b, Abschnitt 10 nachher Z. 971–1177 | beide gleich; Abschnitt 10 Z. 971–1177 (+6, wie erschlossen), ERZEUGT Z. 260–460 |
| A5 `registerbericht --pruefen` | nachher = vorher | rc 1 / rc 1, Ausgabe bytegleich |
| A5 Sonde | JSON ohne `zeilen` gleich, (ii) 0, Listentext ja | `9f7364ef…` gleich, (ii) 0, ja; im Text einzig die Zeilenangabe des Registertexts von Abschnitt 10 anders (Z. 990–1103 → Z. 996–1109) |
| A5 `register()` | ≠ vorher, `fehlend []`, 23 Teile | `ee6947a6…`, `[]`, 23 |
| A5 `test_vorregistrierung` | 196/196, am echten Register vor dem Commit, ohne Zeitgrenze | **196/196**, rc 0, 919 s (`a5_test_vorregistrierung.txt`) |
| A Commit | genau Register und die A-Belege; keine Ausgabe für B, C, D | so (`a_commit.txt`: 14 Dateien); `a_commit.txt` selbst im Commit B/C |
| B | E1, E2: Anker 1, Text nachher 1, je GLEICH; numstat `18	0` | Probe: je `vorher 1`, Ankerzeile 320, Textzeilen 8, `erste Textzeile schon 0`; eingefügt: je `Anker vorher 1 · ausgeführt ja · Text nachher 1`; Vergleich zweimal GLEICH, `alle zeichengleich, je genau einmal`; **18/0**; doppelte spitze Klammern in E1, E2 und J1: 0 |
| C1 | fünf Aufrufe rc 0; 56 Abschnittsdateien `_00`–`_55`; T1 220 839, T2 222 495, T3 232 575, T4 236 927, T5 86 600 B | alle fünf rc 0; Zuschnitt und Grössen **auf das Byte wie erwartet**, bytegleich; **56** Abschnittsdateien, bytegleich (siehe „Registerkopie“) |
| C2 | Index nachgezogen (Liste Nr. 1 bis 9, Abschnitt 10, Pflegezeile) | 308 Zahlen in Zeilenangaben umgeschrieben (271 geändert), 8 Ersetzungen und 5 Tabellenzeilen je Anker 1, neue Zeile 55 in Tabelle 4, neue Zeile 5.2 in Tabelle 2, Abschnitt 10 mit 20 Marken, Abschnittstabelle 0–55 aus den Köpfen; numstat 298/252 |
| C3 | vorher `Indexzeilen aus Fable 07a` 0; drei Zeilen zeichengleich | 0 vorher (vor C2 und vor C3 gezählt); Block eingesetzt, 3/3 zeichengleich |
| C2/C3 Gegenprobe | rc 0 | rc 0: 348/348 Zeilenangaben auf Markenzeilen; 14/14, 12/12, 21/21, 15/15, **20/20** (Abschnitt 6–10); C3 zeichengleich; Indexzeilen 01a 5; 56/56 Tabellenzeilen; Indexzeilen E-2 6 (`c2_index_pruefen.txt`) |
| C4 | `--pruefen` rc 0; 57 Antworten; 07a Fundstelle 55, offen; 06a Fundstelle 55, registriert; 04a unverändert (54, offen) | rc 0 / rc 0; genau so; Schlüssel `06a` und `07a` wie erwartet; Handfelder `cmp` gleich dem Auftrag; „57 Antworten.“; numstat 3/1: zwei neue Zeilen und die Schlusszeile — **keine weitere Zeile geändert** |
| D2 | Kennung EI, J1 GLEICH | letzte Kennung vorher EH, `## EI ` vorher 0; Block gesetzt; J1 Probe einsetzbar, dann eingesetzt, Vergleich GLEICH; numstat Journal 46/0 |

## Umstellen der Skripte (0a Punkt 3)

`trading-env/bin/python3 docs/belege/TB-139/tb139_umstellen.py > docs/belege/TB-139/0a_umstellen.txt` ⇒ rc 0. Die
Ausgabe (20 Zeilen `ok`, je mit dem sha256 der Tabelle „Übernommene Skripte“; Zahl der Ersetzungen und Vorlage):

```
ok   0b_ausgang.sh af9a7e4f… (9, TB-136/0b_ausgang.sh)          ok   b_vergleich.py cf6b78d7… (8, TB-140/c3_vergleich.py)
ok   a4_probelauf.sh 176bcee3… (6, TB-136)                       ok   c1_registerkopie.sh 1db8e97c… (5, TB-136)
ok   a5_r_diff.py e594b64b… (11, TB-136)                         ok   c2_index_zeilen.py ef5d1ca1… (3, TB-136)
ok   a5_zitate.py 59d81de9… (9, TB-136)                          ok   c2_index_07a.py 61473d15… (7, TB-136/c2_index_04a.py)
ok   a5_mutation.py e1b759c1… (7, TB-136)                        ok   c2_index_eintraege.py 5e406492… (25, TB-136)
ok   a5_marken.py a143f80f… (8, TB-136)                          ok   c2_index_pruefen.py 96bf9ee8… (13, TB-136)
ok   a5_nachweis.sh 23016a19… (4, TB-136)                        ok   c3_indexzeilen.py b913190a… (10, TB-136)
ok   test_vorregistrierung.sh a14e25af… (4, TB-136)              ok   c4_dialog_index.sh 47204417… (7, TB-136)
ok   b_einfuegen.py 25d5ee58… (9, TB-140/einfuegen.py)           ok   d2_journal.py f0f288bd… (6, TB-136)
                                                                 ok   j1_einsetzen.py e4e80582… (3, TB-140)
                                                                 ok   j1_vergleich.py 51fa7f73… (3, TB-140)
Skripte: 20, Abweichungen: 0
```

(Hier zweispaltig und gekürzt; die volle Ausgabe mit ganzen sha256 steht in `0a_umstellen.txt`.) Kein `FEHL`, kein
Skript von Hand umgestellt. 157 Ersetzungen.

## Nachlesen der Voraussetzungen (0e; R79 (a), R79 (b))

Aufruf genau wie im Auftrag, einmal, aus der Repo-Wurzel (`docs/belege/TB-139/0e_voraussetzungen.txt`). Endet mit
`rc 0: Voraussetzungen wie in 55.7` und `rc 0`. 46 Zeilen `ok`, 0 `FEHL`. Gelesen wurden nur der Zwischenstand und das
Ergebnis von TB-140 (die genannten Zeilen) und der sha256 von `requirements.lock`; gemessen wurde nichts neu, kein Skript
unter `docs/belege/TB-140/` aufgerufen.

Zwischenstand `docs/belege/TB-140/teil1_zwischenstand.md` (11 Zeilen, sha256 `0d3f5230…`), Kopfzeile
`# TB-140 Teil 1 — Zwischenstand · 2026-10-07 10:47:10 +0200 · ⟨S0⟩ 8127f7f`; die fünf Zeilen im Wortlaut:

```
V4 | erfüllt | W1 67 von 67, W2 67 von 67, Plattform gleich | docs/belege/TB-140/v4.txt
V5 | erfüllt | Tage je Bot 2428, 2177, 2428, 2177, Abweichungen 0 | docs/belege/TB-140/v5.txt
V6 | erfüllt | TEIL (i) ja · (ii) ja · (iii) ja | docs/belege/TB-140/v6.txt
Z1 | erfüllt | Aktien 150 Reihen, 1 Zeilen ohne `close`; Krypto 24 Reihen, 0 Zeilen ohne `close` | docs/belege/TB-140/z1.txt
Z2 | nur erschliessbar | „nur erschliessbar“, Stellen Z. 3, 66, 68–69, 102, 121–122, 342, 344, 355, 357–359 | docs/belege/TB-140/z2.txt
```

| Gruppe | gelesen | Ist |
|---|---|---|
| V4, R79 (a) | Zwischenstand und Ergebnis | je genau eine Zeile; Urteil `erfüllt` bzw. `*erfüllt*`; Kernzahl wie 55.7; `v4.txt` liegt im Repo — **die Voraussetzung ist als erfüllt gemessen** |
| V5, R79 (b) | Zwischenstand und Ergebnis | je genau eine Zeile; Urteil `erfüllt` bzw. `*erfüllt*`; Kernzahl wie 55.7; `v5.txt` liegt im Repo — **die Voraussetzung ist als erfüllt gemessen** |
| V6, Z1, Z2 | Zwischenstand | Urteil und Kernzahl wie 55.7; Rohausgaben im Repo |
| zwölf Teilfragen | Ergebnis (449 Zeilen, sha256 `5162fe15…`), Abschnitt „Für den steuernden Chat“ vor „Für Fable“, je einmal | V4, V5, V6, Z1 `*erfüllt*`; Z2 „nur erschliessbar“; V1 Nr. 0, V1 (i), V1 (ii), V2 (a), V2 (b), V3 (i), V3 (ii) je im Wortlaut wie 55.7 |
| Lock | `requirements.lock`, sha256 | `96a5c572…`, wie Register 20 |

`git status --porcelain` danach: neu nur Dateien unter `docs/belege/TB-139/`.

## `herkunft.register()`

| | Wert |
|---|---|
| vorher (Register `8d505a38…`, 11 581 Z.) | `cfff54ca81d3dbf594a28880b17d4ba8389e0436c2d48cd50248586c1de03a81` |
| nachher (Register `ab97ae1e…`, 11 733 Z.) | `ee6947a611b71407605e9db1e3626f3597ffea1caf0d81a82c0b0ab64ff8f018` |

`fehlend []` und 23 Teile vorher wie nachher. Der neue Wert steht nur hier, nicht im Register (42.5).

## Register nachher

11 733 Zeilen · sha256 `ab97ae1e31da161bc1aebed6b00bb2ec6eec07f760c45c645b9801e6e916b9cd` ·
md5 `eb7c3470a753e3853ad4fca8c4d507e5` — gerechnet mit ⟨S0⟩ = `e16872e` und ⟨DATUM⟩ = `07.10.2026`; Probelauf an der
Kopie und echter Lauf nennen denselben sha256, `cmp` rc 0. Abschnitt 55 steht in Z. 11643–11733 (55.1 Z. 11647, 55.2
Z. 11654, 55.3 Z. 11661, 55.4 Z. 11668, 55.5 Z. 11675, 55.6 Z. 11682, 55.7 Z. 11689, 55.8 Z. 11714) — wie im Auftrag
gerechnet. ⟨S0⟩ ist im Register als `` `e16872e` `` eingesetzt (dreimal im Kopf, einmal im Schluss), das Datum einmal im
Kopf („Eingetragen am 07.10.2026.“) und in jeder der 20 Markenzeilen. Kein Platzhalter `⟨S0⟩` oder `⟨DATUM⟩` steht im
Register.

## Wie eingetragen

- Einfügeskript aus Anhang A, unverändert (`a4_eintrag.py`, sha256 `fea5ca29…`), Probelauf mit `--s0 e16872e --datum
  07.10.2026 --register <Kopie im Scratch>` über `a4_probelauf.sh`, danach echt mit `--s0 e16872e --datum 07.10.2026
  --daten docs/belege/TB-139/a4_eintrag_daten.json`. `--vorschau` nicht benutzt.
- Nachweise mit den umgestellten Skripten `a5_*` über `a5_nachweis.sh`; sie lesen Auftrag und Quelle selbst per
  `git show e16872e:…`.
- Ausgang und Nachher-Messung mit demselben Skript `0b_ausgang.sh`, `vorher` bzw. `nachher` (`0b_ausgang.txt`,
  `0b_nachher.txt`; an `0b_nachher.txt` sind die Vergleiche vorher/nachher angehängt, Bauart `a5_messung_nachher.txt`
  aus TB-136).
- `test_vorregistrierung` lief mit `nohup` im Hintergrund am echten Register vor dem Commit A; währenddessen liefen nur
  lesende Prüfungen und `b_einfuegen.py --probe`, ohne Schreiben in BACKLOG, Index oder Kopie.
- Index: `c2_index_zeilen.py e16872e ad1fc0d`, `c2_index_07a.py e16872e 07.10.2026`, `c2_index_eintraege.py e16872e
  ad1fc0d 07.10.2026`, `c3_indexzeilen.py e16872e`, Gegenprobe `c2_index_pruefen.py e16872e 07.10.2026`.
- Dialog-Index: `c4_handfelder.json` mit dem awk-Ausdruck aus `c4_dialog_index.sh` aus dem Codeblock C4 des Auftrags am
  ⟨S0⟩ geschnitten (nicht abgetippt; `cmp` gegen den Auftrag: ja), dann `c4_dialog_index.sh e16872e <scratch>`.
- Journal: `d2_journal.py` (Block aus `d2_journal_block.md`), dann `j1_einsetzen.py --kennung EI --probe`, ohne
  `--probe`, `j1_vergleich.py --kennung EI` (GLEICH).

## Registerkopie

| Teil | Abschnitte | Bytes | Body | Luft bis 240 000 (Body + 240) | vorher (TB-136) |
|---|---|---|---|---|---|
| T1 | 0–22 | 220 839 | 220 604 | 19 156 | 220 538 (+301, zwei Marken an 5.2) |
| T2 | 23–36 | 222 495 | 222 259 | 17 501 | 222 495 |
| T3 | 37–42 | 232 575 | 232 339 | 7 421 | 232 429 (+146, Marke an 42.2 E6) |
| T4 | 43–53 | 236 927 | 236 691 | **3 069** | 234 587 (+2 340, 14 Marken) |
| T5 | 54–55 | 86 600 | 86 364 | 153 396 | 24 706 (nur 54) |

Der Zuschnitt ist genau der erwartete aus C1 (alle fünf Grössen auf das Byte); kein Abschnitt 0–54 wechselt den Teil,
kein sechster Teil, die Spalte T im Index bleibt für 0–54 gleich. **Luft von T4 nachher: 3 069 B.** Bodies aneinander
998 257 B, bytegleich mit dem Register am `ad1fc0d` (`c1_registerkopie.txt`, `c1_pruefen.txt`,
`c1_abschnitte_pruefen.txt`). Abschnittsdatei `_55.md` neu, 61 618 B, im Commit B/C; die Dateien `_00` bis `_54` tragen
im Kopf den neuen Commit und sind deshalb alle geändert.

## Markentabelle (gegen Anhang A)

| Nr | alter Ort (Anhang A) | nach Z. (alt) | Marke Z. (neu) | Wort | durch | Art | T |
|---|---|---|---|---|---|---|---|
| 1 | 5.2 | 671 | 673 | PRÄZISIERT | R81 (55.4) | MARKE | 1 |
| 2 | 5.2 | 671 | 676 | ERGÄNZT | R83 (55.6) | MARKE+ | 1 |
| 3 | 42.2, Eintrag E6 | 9250 | 9258 | ERGÄNZT | R81 (55.4) | MARKE+ | 3 |
| 4 | 46.4 (R13) | 10485 | 10496 | ERGÄNZT | R79 (55.2) | MARKE+ | 4 |
| 5 | 48.1 (R33) | 10804 | 10818 | ERGÄNZT | R82 (55.5) | MARKE+ | 4 |
| 6 | 48.2 (R34) | 10814 | 10831 | ERGÄNZT | R82 (55.5) | MARKE+ | 4 |
| 7 | 48.11 (R43) | 10895 | 10915 | ERGÄNZT | R81 (55.4) | MARKE+ | 4 |
| 8 | 48.14 (R46) | 10919 | 10942 | ERGÄNZT | R78 (55.1) und R81 (55.4) | MARKE+ | 4 |
| 9 | 48.18 (R50) | 10978 | 11004 | ERGÄNZT | R81 (55.4) und R83 (55.6) | MARKE+ | 4 |
| 10 | 53.1 (R66) | 11418 | 11447 | PRÄZISIERT | R78 (55.1) | MARKE | 4 |
| 11 | 53.1 (R66) | 11418 | 11450 | ERGÄNZT | R81 (55.4) | MARKE+ | 4 |
| 12 | 53.2 (R67) | 11425 | 11460 | ERGÄNZT | R78 (55.1) und R82 (55.5) | MARKE+ | 4 |
| 13 | 53.7 (R72) | 11469 | 11507 | PRÄZISIERT | R78 (55.1) | MARKE | 4 |
| 14 | 53.7 (R72) | 11469 | 11510 | BERICHTIGT | R78 (55.1) | MARKE+ | 4 |
| 15 | 53.7 (R72) | 11469 | 11513 | ERGÄNZT | R79 (55.2) | MARKE+ | 4 |
| 16 | 53.9, Zeile „R72 (53.7), zweite“ | 11499 | 11546 | ERGÄNZT | R78 (55.1) und R83 (55.6) | MARKE+ | 4 |
| 17 | 53.9, Zeile „R72 (53.7) (d)“ | 11499 | 11549 | ERGÄNZT | R79 (55.2) und R78 (55.1) | MARKE+ | 4 |
| 18 | 54.1 (R74) | 11525 | 11578 | PRÄZISIERT | R78 (55.1) | MARKE | 5 |
| 19 | 54.1 (R74) | 11525 | 11581 | ERGÄNZT | R79 (55.2): die Bedingung aus (e) ist gemessen erfüllt | MARKE+ | 5 |
| 20 | 54.5, Zeile „R74 (54.1) (e)“ | 11564 | 11623 | ERGÄNZT | R79 (55.2) | MARKE+ | 5 |

Quelle: `a4_eintrag_daten.json`, `a5_marken.txt`, `c1_marken.txt`, `c2_index_07a_tabelle.md`. 20 Marken an 14
Einfügestellen, alle an den 15 Orten nach R80 (a); die Zeilen nachher gleichen der Soll-Tabelle in A5 (20/20). **Keine
eigene Marke des steuernden Chats** (E2). **Nicht gesetzt nach Anhang A (wie vorgesehen):** die Statuslisten 53.10,
54.6 und 50.7; die Orte aus R80 (b); 48.20 (R52), 54.3 (R76) und Abschnitt 10, Punkte 6, 10 und 11 (Indexzeilen,
Abschnitt 10 des Index); keine Marke in Abschnitt 9, 10 und im ERZEUGT-Block. Kein Block der Antwort 06.10.a eingetragen.

## Für Fable (nur Verfahrensfragen)

1. **55.8 Nr. 5:** Messbitte aus „Unsicher“ Nr. 2 der Antwort 07.10.a — wie `shared/zuteilung.py` den Schlüssel aus
   `exit_time`, `exit_price` und `pnl_pct` bildet; dazu (Nr. 6), ob `open_time` und der Go-Live-Schnitt in derselben
   Zeitzone gelesen werden. Nicht gemessen in dieser Sitzung (kein Code gelesen).
2. **55.8 Nr. 6:** „Unsicher“ Nr. 4 (dürfen die neu erzeugten Trade-Listen Trades aus Zeilen ab dem Schnitt führen —
   vor der Neuerzeugung der Listen) und Nr. 3 (Einstieg vor dem Handelbar-Tag).
3. **55.8 Nr. 9, zur Kenntnis:** das Vorbild 25.2 (die Marke dort steht unter dem berichtigten Satz, nicht unter einem
   Blockzitat; hier stehen die drei Marken an 53.7 nach dem Blockzitat von R72), die Zeilen zur Abnahme von TB-140 und
   der Antwort 07.10.a in 55.7, „Unsicher“ Nr. 1, 5, 7, 8, 9, 10.
4. **55.8 Nr. 10:** Orte, die R80 (a) nicht oder nicht mit diesem Unterpunkt nennt; unsicher sind 48.7 (R39) zu R81 (a)
   und (b) und 53.1 (R66) (b) zu R79 (b). Dazu die Form „je Teil eine Marke, die beide Blöcke nennt“.
5. **55.8 Nr. 12 und Nr. 13, zur Kenntnis:** die Lesarten zu „`benchmark.py` wird nicht geöffnet“ und zu Z2; aus 54.6
   weiter Nr. 2, 6, 7, 9 und 10.
6. **Reibung beim Setzen, Werkzeug (wie TB-129 bis TB-136):** `registerkopie.py --marken` zählt in Abschnitt 55 sieben
   Zeilen mit, die keine Marken sind: die Blockzeile von R80 (Z. 11663, `MARKE`, sie nennt „PRÄZISIERT durch“), ihre
   Zeile „Quelle des Grundes“ (Z. 11664, `MARKE+`, sie nennt „ERGÄNZT“) und fünf Überschriften mit Rückverweis (55.1,
   55.2, 55.4, 55.5, 55.6; `UEBERSCHRIFT`). Damit stehen die Arten bei `MARKE` 100 = 95 + 4 + 1, `MARKE+` 145 = 128 + 16
   + 1, `UEBERSCHRIFT` 96 = 91 + 5 — genau wie im Auftrag erwartet. Im Index ist keine der sieben Zeilen als Marke
   geführt.
7. **Keine Reibung zwischen Fable-Text und Register beim Setzen gefunden**, die über 55.7 und 55.8 hinausgeht: jeder der
   20 Anker kam genau einmal vor, jede Einfügestelle begann mit dem angegebenen Anfang, die Schnittregel ergab genau
   R78–R83 in Z. 227–243.

## Nicht getan

- 55.8 (alle 14 Punkte): Zellen-Erzeuger mit Schnitt, Wachen und Feldern ohne Zahl (Nr. 1), Abnahme nach R46 mit drei
  Test-Snapshots (Nr. 2), Posten 4 (Nr. 3), die Messungen vor dem signierten Tag (Nr. 4), Anfragen an Fable (Nr. 5, 6,
  9, 10, 12, 13), Tatsachennotiz zu den übrigen Ausstiegskonventionen (Nr. 7), V1/V3-Folgen (Nr. 8), Regelwerk-Nachtrag
  und Abnahme TB-137 (Nr. 14).
- Keine Voraussetzung neu gemessen, kein Skript unter `docs/belege/TB-140/` aufgerufen, kein Code gelesen.
- Die Ablage (56 Abschnittsdateien, fünf Teile, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`) — macht der steuernde Chat.
- Kein Code, kein neues Abbild, kein zweiter Snapshot, nichts an `snapshots/` oder `data/`, keine Läufe von
  `auswertung.py`, Zellen-Erzeugern oder Backtests; `UEBERGABE.md` und die `FABLE_*`-Quellen nicht geändert (nur in
  Schritt 0 committet).
- `registerbericht.py --pruefen` rc 1 bleibt (schon vor TB-126; Zahlenteil veraltet).

## Nebenbemerkungen zum Ablauf

- Die Sitzung lief spät am Abend (0a um 22:57, Registercommit nach 23:16); ⟨DATUM⟩ ist der 07.10.2026, derselbe Tag wie
  die Freigabe.
- `test_vorregistrierung` brauchte 919 s (TB-136: 940 s).
- Der Index-Diff ist mit 298/252 gross, weil `c2_index_zeilen.py` 271 Zeilenangaben auf den neuen Stand umschreibt (die
  zwei Marken an 5.2 verschieben fast alles); inhaltlich neu sind nur die Einträge aus C2/C3.
- Index-Kopf „*Frühere Vierteilung*“ nennt weiter „T1“ … „T4“, die Liste danach fünf Teile (bekannt aus TB-136).
- T4 steht jetzt bei 236 691 B Body, 3 069 B Luft; ein weiterer Abschnitt kommt nach dem gierigen Zuschnitt in T5,
  Marken in 43–53 müssen aber in T4 Platz finden.
- Der Zeilenzähler der Sonde (`git status --porcelain` vorher/nachher) zeigt 1 bzw. 12 Zeilen: die Belege der Sitzung.

## In einfacher Sprache

Die Sitzung hat zuerst die Unterlagen des steuernden Chats ins Repo gesichert, darunter Fables Antwort vom 07.10. Dann
hat sie nachgelesen, ob die Messsitzung TB-140 die zwei Dinge, die vor dem Eintrag gemessen sein mussten, als „erfüllt“
festgehalten hat — beide sind erfüllt, und auch alle anderen Urteile stimmen mit dem überein, was im Registertext steht.
Erst danach hat sie Fables sechs Regeltexte (R78–R83) Zeichen für Zeichen ins Register kopiert, als Abschnitt 55, mit
der Tabelle der Messungen und der Liste der offenen Punkte; die erste Fassung vom Vortag ist nicht eingetragen. An 20
alten Stellen weist eine kleine Marke auf die neuen Texte. Kein alter Satz wurde geändert (152 Zeilen dazu, 0 weg). Alle
Prüfungen und der grosse Registertest (196/196) sind grün. Danach sind die Aufgabenliste, die Kopie des Registers für
die Ablage (jetzt 56 Dateien und fünf Teile), der Wegweiser und die Liste der Fable-Antworten erneuert. Am Code und an
den Daten hat sich nichts geändert.
