# TB-154: Ergebnis. Register Abschnitt 57 — Fable 10a (R90–R93) zeichengleich, Tatsachennotizen 57.5–57.6, 11 Marken am alten Ort an 9 Orten (2 davon nachgetragen nach R93 (a)), numstat 103/0; vorher gemessen: Anfrage, Übergabe und Antwort 10.10.a mit Commit im Repo (R91 (h), R56 (b)), Punkt (1) der Antwort 25c (R91 (f)), der Satz in 15.5 (R93 (a)) und die 9 Orte; zwei BACKLOG-Blöcke; Registerkopie neu in 58 Abschnittsdateien und 5 Teilen, Index und Dialog-Index nachgezogen

**Sitzungstitel:** `TB-154` · **Stand:** 11.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-154_register_fable_10a.md` ·
**Belege:** `docs/belege/TB-154/`
**Eingang:** `548b9a3` (TB-152, F; = `origin/main`), Arbeitsbaum wie 0a (vier Einträge). Commits: `4fbc2f3` (Schritt 0,
im Folgenden ⟨S0⟩), `336e752` (0: Ausgang, Vorprüfung, umgestellte Skripte), `3f2e97e` (A: Register, einziger
Registercommit), `bf6e992` (B/C: BACKLOG, Registerkopie, Index, Dialog-Index), der Abgabe-Commit (D: dieses Dokument,
Journal ER) und ein kleiner Commit mit `d3_porcelain.txt`. Nach jedem Commit gepusht, jeder Push im ersten Versuch.
**⟨S0⟩ im Wortlaut:** `4fbc2f3` · **⟨DATUM⟩ im Wortlaut:** `11.10.2026` (`a4_datum.txt`, gemessen zu Beginn von A4 mit
`TZ=Europe/Berlin date +%d.%m.%Y`; derselbe Tag wie in 0a und 0d; die Sitzung lief von etwa 13:30 bis nach 14:00, kein
Tageswechsel).
**Quelle (md5 am ⟨S0⟩ und im Arbeitsbaum geprüft, `0b_ausgang.txt`):**
`docs/projektfuehrung/FABLE_ANTWORT_2026-10-10a_m4_widerspruch_schranke_am_einstieg.md`,
`2b60d6863380bd89c8733b7866fa3328`, 30 026 B — gleich dem Soll; im Repo seit `82120cf`. Geschnitten nur aus dieser
Datei (Z. 130–140).
**Freigabe:** Betreiber, 11.10.2026 (Auswahlkarte im steuernden Chat, gestellt nach 13:08, eingetragen 13:23),
„Ja, freigeben (Recommended)“ (wörtlich im Auftrag). **Keine Rückfrage an den Betreiber.**
**Umgebung:** Mac, Hauptordner `~/trading-bot`, lokal; `trading-env/bin/python3` (3.9.6). Gestartet über den Einfügesatz
`TB-154: …`. Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst. Claude Code hat keinen Aufruf abgelehnt und keine Bestätigung verlangt.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a Arbeitsbaum | genau die vier Einträge des Auftrags; HEAD `548b9a3` | genau diese vier (`0a_status.txt`); HEAD `548b9a3` |
| 0a Skripte | sha256 `2dae5d06…` (Prüfskript), `ab62d959…` (Einfügeskript), `503bd2f3…` (Umstellskript) | alle drei gleich; nach dem Kopieren nach `0d_vorpruefung.py`, `a4_eintrag.py`, `tb154_umstellen.py` noch einmal gleich |
| 0a Prüfskript `--arbeitsbaum` | rc 0; nach der Datumszeile geändert 3 / unverfolgt 1; Zeilen `Dateien 10.10.a …`, `Orte: …`, `Voraussetzung R93 (a): …`, `Marken:` … `Bloecke:`, `Dateien:` wie „Prüfsumme“ | rc 0; genau so (`0a_pruefung.txt`; `*.py im Baum: 767`, kein Soll) |
| 0a Punkt 3 Umstellen | rc 0, 20 Zeilen `ok`, `Skripte: 20, Abweichungen: 0` | genau so; jede sha256 gleich der Tabelle „Übernommene Skripte“ (`0a_umstellen.txt`) |
| 0b | 11 920 Z., sha256 `b2d56949…`, md5 `4359577a…`; `register()` `1ddb56ee…`, `fehlend []`, 23 Teile; Abbild `46f0ad5d…`; Sonde rc 2, 37/0/0, (ii) 0, Listentext ja; Quelle 10a `2b60d686…`/30 026 B am ⟨S0⟩ und im Arbeitsbaum; Abschnitt 10 und ERZEUGT gleich `TB-149/0b_*_nachher.txt` | alles gleich (`0b_ausgang.txt`); Sonde-JSON ohne `zeilen` `9f7364ef…` (wie TB-149 nachher); `registerbericht.py --pruefen` rc 1 (bekannt, Vergleichswert); Abschnitt 10 Z. 971–1177, ERZEUGT Z. 260–460, beide `cmp`-gleich mit den Dateien aus TB-149 |
| 0c | `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` | leer ⇒ Basis `docs/belege/TB-149/a5_test_vorregistrierung.txt` (196/196), kein eigener Basislauf |
| ⭐⭐ 0d | rc 0, Datumszeile, `Dateien 10.10.a …`, `Orte: …`, `Voraussetzung R93 (a): …`, fünf Zeilen wie „Prüfsumme“, `rc 0: alles wie angegeben` | genau so (`0d_vorpruefung.txt`; `*.py im Baum: 784`, kein Soll); siehe „Vorprüfung“ |
| A4 | `git diff --quiet ⟨S0⟩ -- Auftrag Quelle Anfrage Übergabe` rc 0; Probelauf an Kopie grün, dann echt, `cmp` gleich; `11 an 9`, `4 (R90-R93)`, `11920 → 12023, 103` | rc 0; Probelauf und echter Lauf je genau diese Ausgabe, `sha256 nachher:` in beiden `459be94e…`; `cmp` rc 0; die Wachen (Block am Ort, Platzhalter) liefen in beiden Läufen ohne Meldung |
| A5 R-Diff | 4/4 rc 0; Mutation erkannt | **4/4**; `a5_r_diff.py` an der mutierten Kopie rc 1 (`a5_mutation.py` rc 0) |
| A5 Zitate | 2/2 | Kopf 57.0 und Schluss 57.5–57.6 **2/2** |
| A5 Überschriften/Ketten, Marken | 4/4, 11/11 | **4/4 und 4/4**, **11/11**, jede Markenzeile einmal (`TB-154, 11.10.2026` 11-mal); in Abschnitt 9, 10 und ERZEUGT-Block je 0; Zeilen nachher gleich der Tabelle in A5 (11/11) |
| A5 numstat, Zeilen | `103	0`, 12 023 | **103/0**, 12 023 |
| A5 Abschnitt 10, ERZEUGT | bytegleich gegen 0b | beide gleich; Abschnitt 10 Z. 971–1177, ERZEUGT Z. 260–460 (wandern nicht) |
| A5 `registerbericht --pruefen` | nachher = vorher | rc 1 / rc 1, Ausgabe bytegleich |
| A5 Sonde | JSON ohne `zeilen` gleich, (ii) 0, Listentext ja | `9f7364ef…` gleich, (ii) 0, ja; Sonde-Text vorher/nachher ohne Unterschied (`diff` rc 0) |
| A5 `register()` | ≠ vorher, `fehlend []`, 23 Teile | `08657b83…`, `[]`, 23 |
| A5 `test_vorregistrierung` | 196/196, am echten Register vor dem Commit, ohne Zeitgrenze | **196/196**, rc 0, 879 s (`a5_test_vorregistrierung.txt`) |
| A Commit | genau Register und die A-Belege; keine Ausgabe für B, C, D | so (`a_commit.txt`: 14 Dateien); `a_commit.txt` selbst im Commit B/C |
| B | E1, E2: Probe je `vorher 1`, Ankerzeile 452, Textzeilen 7 und 8; Anker 1, Text nachher 1, je GLEICH; numstat `17	0` | Probe genau so (während des Tests, ohne Schreiben); eingefügt: je `Anker vorher 1 · ausgeführt ja · Text nachher 1`; Vergleich zweimal GLEICH, `alle zeichengleich, je genau einmal`; **17/0** |
| C1 | fünf Aufrufe rc 0; 58 Abschnittsdateien `_00`–`_57`; T1 221 039, T2 222 813, T3 232 851, T4 239 831, T5 192 705 B | alle fünf rc 0; Zuschnitt und Grössen **auf das Byte wie erwartet**, bytegleich; **58** Abschnittsdateien, bytegleich |
| C2 | Index nachgezogen (Liste Nr. 1 bis 8, Abschnitt 12, Pflegezeile) | 410 Zahlen in Zeilenangaben umgeschrieben (312 geändert), 7 Ersetzungen, 5 Tabellenzeilen (Tabelle 3 „3a Universum“ und Tabelle 4 an 27, 48, 55, 56) und neue Zeile 57 in Tabelle 4, je Anker 1; Abschnitt 12 mit 11 Marken; Abschnittstabelle 0–57 aus den Köpfen; numstat 294/257 |
| C3 | vorher `Indexzeilen aus Fable 10a` 0; drei Zeilen zeichengleich | 0 vorher (vor C2 gezählt und im Skript vor C3); Block eingesetzt, 3/3 zeichengleich |
| C2/C3 Gegenprobe | rc 0 | rc 0: 432/432 Zeilenangaben mit Markenwort; 14/14, 12/12, 21/21, 15/15, 20/20, 31/31, **11/11** (Abschnitt 6–12); C3 zeichengleich; Indexzeilen 01a 5; Indexzeilen E-2 6; 58/58 Tabellenzeilen (`c2_index_pruefen.txt`) |
| C4 | `--pruefen` rc 0; 59 Antworten; 10a Fundstelle 57; 09a unverändert (56) | rc 0 / rc 0; Schlüssel `10a` wie erwartet; Handfelder `cmp` gleich dem Auftrag; Zeile 10a: Status offen, Fundstelle 57, offen „ja“, Anfrage „10a (Bezug)“; 09a unverändert (56); „59 Antworten.“; numstat 3/2 — **eine weitere Zeile geändert: 25c** (siehe „Nebenbemerkungen“) |
| D2 | Kennung ER, J1 GLEICH | letzte Kennung vorher EQ, `## ER ` vorher 0; Block gesetzt; J1 Probe einsetzbar, dann eingesetzt (6 Zeilen), Vergleich GLEICH, rc 0; numstat Journal 45/0 |

## Umstellen der Skripte (0a Punkt 3)

`trading-env/bin/python3 docs/belege/TB-154/tb154_umstellen.py > docs/belege/TB-154/0a_umstellen.txt` ⇒ rc 0. Die
Ausgabe (20 Zeilen `ok`, je mit dem sha256 der Tabelle „Übernommene Skripte“; Zahl der Ersetzungen; alle Vorlagen unter
`docs/belege/TB-149/`):

```
ok   0b_ausgang.sh 48ed7dfd… (7)              ok   c1_registerkopie.sh f5ed760f… (1)
ok   a4_probelauf.sh 7c0c8897… (6)            ok   c2_index_10a.py f4b4c804… (5, TB-149/c2_index_09a.py)
ok   a5_marken.py 3492d164… (7)               ok   c2_index_eintraege.py a28e49fe… (28)
ok   a5_mutation.py f6c031bd… (5)             ok   c2_index_pruefen.py 9022ec7b… (13)
ok   a5_nachweis.sh fe46d714… (2)             ok   c2_index_zeilen.py 26e6269f… (2)
ok   a5_r_diff.py f3231915… (12)              ok   c3_indexzeilen.py 95047c15… (8)
ok   a5_zitate.py 7f24c40f… (9)               ok   c4_dialog_index.sh daf02ea7… (6)
ok   b_einfuegen.py fbfcbdbf… (3)             ok   d2_journal.py 60f0837b… (5)
ok   b_vergleich.py 248438ab… (3)             ok   j1_einsetzen.py 9eadb2a5… (5)
                                              ok   j1_vergleich.py 9948ef59… (3)
                                              ok   test_vorregistrierung.sh 73a132e0… (2)
Skripte: 20, Abweichungen: 0
```

(Hier zweispaltig und gekürzt; die volle Ausgabe mit ganzen sha256 steht in `0a_umstellen.txt`.) Kein `FEHL`, kein
Skript von Hand umgestellt. 132 Ersetzungen.

## Vorprüfung (0d; R91 (f), R91 (h), R56 (b), R93 (a))

`trading-env/bin/python3 docs/belege/TB-154/0d_vorpruefung.py docs/auftraege/MAC_TB-154_register_fable_10a.md .
--datum 11.10.2026` am Commit ⟨S0⟩, ohne `--arbeitsbaum` ⇒ rc 0. Die Ausgabe im Wortlaut (`0d_vorpruefung.txt`):

```
Datum des Eintrags: 11.10.2026 (aus --datum)
Dateien 10.10.a (R91 (h), R56 (b)): 3 von 3 von git verfolgt, Arbeitsbaum gleich HEAD, dazugekommen in 82120cf, md5 und Bytes wie im Daten-Block
Orte: 9 Anker, je genau einmal: True; Zeilen am Ort (Anker bis vor die naechste Ueberschrift), die den Block der neuen Marke nennen: 0; Zeilen mit R90 bis R93 im Register: 0
Voraussetzung R93 (a): der zitierte Satz in 15.5 1-mal (Z. 1641 bis 1643); Zeilen mit Markenwort in 15.5: [1576, 1589, 1612, 1629, 1667], davon Markenzeilen (Markenwort und 'durch') 4, Markenwort im Satz 1; nach dem Satz: [1667]
Marken: 11 an 9 Einfuegestellen
je Abschnitt: 15: 1, 27: 1, 48: 1, 55: 1, 56: 7
Anker mit Zahl 1 (Original): 11 von 11
Anker mit Zahl 1 (nach Simulation): 11 von 11
Bloecke: 4 | Ueberschriften: 4 max. Laenge 140 | gekuerzt: 2
Dateien: 0 | Fundstellen: 30 | Zeilenlisten: 0 | Zaehlungen: 18 | *.py im Baum: 784
rc 0: alles wie angegeben
```

Damit hat die Sitzung vor dem Eintrag selbst gemessen:

- **Die drei Dateien 10.10.a** (Anfrage `FABLE_ANFRAGE_2026-10-10a_m4_kauf_vor_handelbar_tag.md`, Übergabe
  `FABLE_UEBERGABE_2026-10-10_eroeffnung.md`, Antwort `FABLE_ANTWORT_2026-10-10a_…`) sind von git verfolgt, im Commit
  `82120cf` dazugekommen, im Arbeitsbaum gleich HEAD und tragen md5 und Bytes wie im Daten-Block — R91 (h), erste
  Voraussetzung, und R56 (b) erfüllt.
- **R91 (f):** Der Beleg trägt dazu die Zeilen `Dateien: 0 | Fundstellen: 30 | …` und `rc 0: alles wie angegeben`. Unter
  den 30 Fundstellen des Daten-Blocks stehen die zwei in der Antwort 25c
  (`docs/projektfuehrung/FABLE_ANTWORT_2026-09-25c_rasterbedingung_abschnitt6_protokoll.md`): Z. 53
  „### (1) `_bedingung` — ja, mit Abschnitt 6 (oben)“ und Z. 17 „Ein nicht leerer `_bedingung`-Text, den der Code nicht
  als Rasterbedingung erkennt, ist ein Widerspruch zwischen Register und Code und endet mit 2 — unabhängig vom Modus.“
  (Fundstellen aus dem Daten-Block des Auftrags, nicht Ausgabe von 0d). Beide trafen.
- **R93 (a):** Der Satz, den 56.7 aus 15.5 zitiert, steht in 15.5 genau einmal (Z. 1641–1643, Zeilenumbrüche als
  Leerzeichen gelesen); 15.5 führt fünf Zeilen mit Markenwort (vier Markenzeilen, eine mit dem Wort im Satz); nach dem
  Satz steht nur die Marke zu R53 (49.1), Z. 1667. Keine Marke in 15.5 löst ihn ab — die Marke ist gesetzt.
- **Jeder der 9 Orte ist genau einmal vorhanden**; vom Anker bis vor die nächste Überschrift nennt an keinem Ort eine Zeile
  den Block der neuen Marke (0 Zeilen); R90 bis R93 kamen vor dem Eintrag in keiner Registerzeile vor.
- Nicht von der Sitzung gemessen (wie vorgesehen, E5): der Inhalt von `overview.md` gegen 27.1 (R91 (h), zweite
  Voraussetzung; Erinnerungsdatei, nicht im Repo) und die Klammern in R90 (f) und R92 (c) (keine Voraussetzung des
  Eintrags).

Die Prüfung lief schon in 0a einmal am Arbeitsbaum (mit `--arbeitsbaum`, `0a_pruefung.txt`), mit demselben Ergebnis.
`git status --porcelain` danach: neu nur Dateien unter `docs/belege/TB-154/`.

## `herkunft.register()`

| | Wert |
|---|---|
| vorher (Register `b2d56949…`, 11 920 Z.) | `1ddb56eec9a2da60270d9b49d27702cbc20583045256fe88caade62d6f7a1fee` |
| nachher (Register `459be94e…`, 12 023 Z.) | `08657b839d5751fe36a57073360d09cd6d6aa251fcb1773e35aa266392afa2b5` |

`fehlend []` und 23 Teile vorher wie nachher. Der neue Wert steht nur hier, nicht im Register (42.5).

## Register nachher

12 023 Zeilen · sha256 `459be94e388490fb4aac35e8955d5d1098ccff3a508991d3893cd7693449c350` ·
md5 `6309a2fc58b019a915da32522c171b0b` — gerechnet mit ⟨S0⟩ = `4fbc2f3` und ⟨DATUM⟩ = `11.10.2026`; Probelauf an der
Kopie und echter Lauf nennen denselben sha256, `cmp` rc 0. Abschnitt 57 steht in Z. 11955–12023 (57.1 Z. 11959, 57.2
Z. 11966, 57.3 Z. 11973, 57.4 Z. 11980, 57.5 Z. 11987, 57.6 Z. 12010) — wie im Auftrag gerechnet. ⟨S0⟩ ist im Register
als `` `4fbc2f3` `` eingesetzt (einmal, im Kopf), das Datum einmal im Kopf („Eingetragen am 11.10.2026.“) und in jeder
der 11 Markenzeilen. Kein Platzhalter `⟨S0⟩` oder `⟨DATUM⟩` steht im Register.

## Wie eingetragen

- Einfügeskript aus Anhang A, unverändert (`a4_eintrag.py`, sha256 `ab62d959…`), Probelauf mit `--s0 4fbc2f3 --datum
  11.10.2026 --register <Kopie im Scratch>` über `a4_probelauf.sh`, danach echt mit `--s0 4fbc2f3 --datum 11.10.2026
  --daten docs/belege/TB-154/a4_eintrag_daten.json`. `--vorschau` nicht benutzt.
- Nachweise mit den umgestellten Skripten `a5_*` über `a5_nachweis.sh`; sie lesen Auftrag und Quelle selbst per
  `git show 4fbc2f3:…`.
- Ausgang und Nachher-Messung mit demselben Skript `0b_ausgang.sh`, `vorher` bzw. `nachher` (`0b_ausgang.txt`,
  `0b_nachher.txt`; an `0b_nachher.txt` sind die Vergleiche vorher/nachher angehängt, Bauart TB-139/TB-149).
- `test_vorregistrierung` lief im Hintergrund am echten Register vor dem Commit A; währenddessen liefen nur lesende
  Prüfungen (`a5_nachweis.sh`, `0b_ausgang.sh nachher`) und `b_einfuegen.py --probe`, ohne Schreiben in BACKLOG, Index
  oder Kopie.
- Index: `c2_index_zeilen.py 4fbc2f3 3f2e97e`, `c2_index_10a.py 4fbc2f3 11.10.2026`, `c2_index_eintraege.py 4fbc2f3
  3f2e97e 11.10.2026`, `c3_indexzeilen.py 4fbc2f3`, Gegenprobe `c2_index_pruefen.py 4fbc2f3 11.10.2026`.
- Dialog-Index: `c4_handfelder.json` mit dem awk-Ausdruck aus `c4_dialog_index.sh` aus dem Codeblock C4 des Auftrags am
  ⟨S0⟩ geschnitten (nicht abgetippt; `cmp` gegen den Auftrag: ja), dann `c4_dialog_index.sh 4fbc2f3 <scratch>`.
- Journal: `d2_journal.py` (Block aus `d2_journal_block.md`), dann `j1_einsetzen.py --kennung ER --probe`, ohne
  `--probe`, `j1_vergleich.py --kennung ER`.

## Registerkopie

| Teil | Abschnitte | Bytes | Body | Luft bis 240 000 (Body + 240) | vorher (TB-149) |
|---|---|---|---|---|---|
| T1 | 0–22 | 221 039 | 220 804 | 18 956 | 220 839 (+200, Marke an 15.5) |
| T2 | 23–36 | 222 813 | 222 577 | 17 183 | 222 662 (+151, Marke an Abschnitt 27) |
| T3 | 37–42 | 232 851 | 232 615 | 7 145 | 232 851 (keine Marke) |
| T4 | 43–53 | 239 831 | 239 595 | **165** | 239 683 (+148, Marke an 48.14) |
| T5 | 54–57 | 192 705 | 192 469 | 47 291 | 145 682 (54–56; +8 Marken, + Abschnitt 57) |

Der Zuschnitt ist genau der erwartete aus C1 (alle fünf Grössen auf das Byte); kein Abschnitt 0–56 wechselt den Teil,
kein sechster Teil, die Spalte T im Index bleibt für 0–56 gleich. **Luft je Teil nachher: T1 18 956 B, T2 17 183 B, T3
7 145 B, T4 165 B, T5 47 291 B.** ⚠️ **T4 hat nur noch 165 B Luft**: Eine weitere Marke solcher Länge (≈ 150 B) passt
dort gerade noch, eine zweite nicht mehr; dann teilt das Werkzeug neu. Bodies aneinander 1 108 060 B, bytegleich mit dem
Register am `3f2e97e` (`c1_registerkopie.txt`, `c1_pruefen.txt`, `c1_abschnitte_pruefen.txt`). Abschnittsdatei `_57.md`
neu, 45 930 B, im Commit B/C; die Dateien `_00` bis `_56` tragen im Kopf den neuen Commit und sind deshalb alle geändert.

## Markentabelle (gegen Anhang A)

| Nr | alter Ort (Anhang A) | nach Z. (alt) | Marke Z. (neu) | Wort | durch | Art | T |
|---|---|---|---|---|---|---|---|
| 1 | 15.5, am Absatz zu Lesart A | 1668 | 1670 | ERGÄNZT | R87 (56.4), nachgetragen nach R93 (a) | MARKE+ | 1 |
| 2 | Abschnitt 27 | 5230 | 5235 | ERGÄNZT | R91 (57.2) | MARKE+ | 2 |
| 3 | 48.14 (R46) | 10991 | 10999 | ERGÄNZT | R90 (57.1) | MARKE+ | 4 |
| 4 | 55.7, Zeile „R78 (55.1) (a), erste“ | 11805 | 11816 | ERGÄNZT | R88 (56.5), nachgetragen nach R93 (a) | MARKE+ | 5 |
| 5 | 56.1 (R84) | 11835 | 11849 | ERGÄNZT | R91 (57.2) | MARKE+ | 5 |
| 6 | 56.3 (R86) | 11849 | 11866 | ERGÄNZT | R92 (57.3) | MARKE+ | 5 |
| 7 | 56.4 (R87) | 11856 | 11876 | ERGÄNZT | R90 (57.1) | MARKE+ | 5 |
| 8 | 56.5 (R88) | 11863 | 11886 | PRÄZISIERT | R91 (57.2) | MARKE | 5 |
| 9 | 56.7, Zeile „R87 (56.4) (d)“ | 11896 | 11922 | ERGÄNZT | R90 (57.1) | MARKE+ | 5 |
| 10 | 56.7, Zeilen „R84 (56.1) (e), erste“ und „R84 (56.1) (e), zweite“ | 11896 | 11925 | ERGÄNZT | R91 (57.2) | MARKE+ | 5 |
| 11 | 56.7, Zeile „R86 (56.3) (e)“ | 11896 | 11928 | ERGÄNZT | R92 (57.3) | MARKE+ | 5 |

Quelle: `a4_eintrag_daten.json`, `a5_marken.txt`, `c1_marken.txt`, `c2_index_10a_tabelle.md`. 11 Marken an 9
Einfügestellen, an den 9 Orten nach R93 (a) und (c); die Zeilen nachher gleichen der Soll-Tabelle in A5 (11/11). Je
Markenwort ERGÄNZT 10, PRÄZISIERT 1. **Keine eigene Marke des steuernden Chats** (E3; 57.6 Nr. 6). **Nicht gesetzt nach
Anhang A (wie vorgesehen):** die Statusliste 56.8; die Orte aus R93 (b) und (d); die 17 Paare aus 57.6 Nr. 6; Abschnitt
10, Sperrlistenpunkte 9 und 11, 48.20 (R52) und 54.3 (R76) (Indexzeilen, Abschnitt 12 des Index); keine Marke in
Abschnitt 9, 10 und im ERZEUGT-Block.

## Für Fable (nur Verfahrensfragen)

1. **57.6 Nr. 4:** Rückfragen aus der Bewertung der Antwort 10.10.a — F1 (R90 (c), der Verweis „(R81 (b))“; Lesefrage),
   F2 (R91 (f), die Aufzählung der Orte von „25c (1)“ ist nicht vollständig), F4 (Form der Antwort zu den Punkten 10, 11
   und 12 der Anfrage).
2. **57.6 Nr. 5:** Lesarten des steuernden Chats, vorläufig — der Platz der Marke an 15.5 (hinter der Marke zu R53, Ort
   „15.5, Absatz zu Lesart A“); die Punkte von Abschnitt 10 für die Indexzeile aus R93 (d) (Sperrlistenpunkte 9 und 11);
   F1 nicht als Fall gezählt; dazu offen, ob 48.16 (R48), 48.18 (R50) und 56.4 (R87) eine Marke zu R91 (f) tragen.
3. **57.6 Nr. 6:** keine eigene Marke des steuernden Chats; 17 Paare an 15 Orten geprüft. Eine fehlende Marke lässt sich
   nachtragen.
4. **57.6 Nr. 7:** weiter vierzehn gezählte Fälle (R91 (g)), geführt als Indexzeilen an 48.20 (R52) und 54.3 (R76); dazu
   die Indexzeile an Abschnitt 10, Sperrlistenpunkte 9 und 11.
5. **57.6 Nr. 8:** Die nächste Anfrage geht an einen neuen Fable-Chat (Umzugsampel der Antwort 10.10.a rot).
6. **Reibung beim Setzen, Werkzeug (wie TB-129 bis TB-149):** `registerkopie.py --marken` zählt in Abschnitt 57 sieben
   Zeilen mit, die keine Marken sind: drei Überschriften mit Rückverweis (57.1, 57.2, 57.3; Z. 11959, 11966, 11973;
   `UEBERSCHRIFT`), die Blockzeile von R93 (Z. 11982, `MARKE`), die Tabellenzeile „R93 (57.4) (a)“ in 57.5 (Z. 11998,
   `MARKE`), die Tabellenzeile „R93 (57.4) (a) und (c), Orte“ in 57.5 (Z. 12003, `MARKE+`) und die Zeile Nr. 6 in 57.6
   (Z. 12019, `MARKE+`). Damit stehen die Arten bei `MARKE` 117 = 114 + 1 + 2, `MARKE+` 179 = 167 + 10 + 2,
   `UEBERSCHRIFT` 105 = 102 + 3 — genau wie im Auftrag erwartet. Im Index ist keine der sieben Zeilen als Marke geführt.
7. **Keine Reibung zwischen Fable-Text und Register beim Setzen gefunden**, die über 57.5 und 57.6 hinausgeht: jeder der
   9 Anker kam genau einmal vor, an keinem Ort stand schon eine Zeile zum Block der neuen Marke, der Satz aus 15.5 stand
   wie zitiert, die Schnittregel ergab genau R90–R93 in Z. 130–140.

## Nicht getan

- 57.6 (alle 8 Punkte): insbesondere die Messung nach R92 (c) vor der Neuerzeugung der Listen (Nr. 2), die Schranke nach
  R90 (c), die Messung nach R90 (f) und die Abnahme nach R90 (g) mit den zwei Erzeugern (Nr. 3), die Rückfragen und die
  nächste Anfrage an Fable (Nr. 4, 5, 8).
- Kein Code gelesen; die Messungen nach R90 (f) und R92 (c) nicht gemacht; den Inhalt von `overview.md` gegen 27.1 nicht
  gemessen (Sache des steuernden Chats, E5).
- Die Ablage (58 Abschnittsdateien, fünf Teile, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`) — macht der steuernde Chat.
- Kein Code, kein neues Abbild, kein zweiter Snapshot, nichts an `snapshots/` oder `data/`, keine Läufe von
  `auswertung.py`, Zellen-Erzeugern oder Backtests; `UEBERGABE.md`, `EROEFFNUNG_STEUERNDER_CHAT.md` und die
  `FABLE_*`-Quellen nicht geändert (nur in Schritt 0 committet).
- `registerbericht.py --pruefen` rc 1 bleibt (schon vor TB-126; Zahlenteil veraltet).

## Nebenbemerkungen zum Ablauf

- ⚠️ **Dialog-Index, eine weitere geänderte Zeile (kein Abbruch, C4):** `dialog_index.py` hat in der Zeile `25c` die
  Spalte Fundstelle von „42“ auf „42, 57“ gesetzt. Grund: Abschnitt 57 nennt die Datei der Antwort 25c (57.5, Zeile
  „R91 (57.2) (f)“), und das Werkzeug liest die Fundstellen aus dem Register. Sonst ist an der Zeile nichts geändert
  (Status „registriert“, offen „nein“). numstat des Dialog-Index damit 3/2 statt 2/1 wie in TB-149.
- `test_vorregistrierung` brauchte 879 s (TB-149: 905 s).
- `b_vergleich.txt` endet mit einer Restzeile ` 2 · Gesamt: alle zeichengleich, je genau einmal`: Das Skript schreibt die
  Datei selbst, und die Umleitung der Standardausgabe auf dieselbe Datei überlagert sie (wie in TB-139 und TB-149). Der
  Inhalt davor ist vollständig und richtig (zweimal GLEICH).
- `j1_vergleich.py` schreibt seine Belegdatei ebenfalls selbst. Der erste Aufruf (mit Umleitung nach
  `j1_vergleich.txt`) hinterliess dieselbe Überlagerung; der lesende Vergleich lief danach noch einmal ohne Umleitung
  (rc 0, GLEICH), damit `j1_vergleich.txt` die vollständige Ausgabe des Skripts trägt.
- Der Index-Diff ist mit 294/257 gross, weil `c2_index_zeilen.py` 312 Zeilenangaben auf den neuen Stand umschreibt (die
  Marke an 15.5 verschiebt alles danach); inhaltlich neu sind nur die Einträge aus C2/C3.
- Der Zeilenzähler der Sonde (`git status --porcelain` vorher/nachher) zeigt 1 bzw. 12 Zeilen: die Belege der Sitzung
  und das geänderte Register.
- Die Vergleichszeilen am Ende von `0b_nachher.txt` hat die Sitzung mit `cmp`, `diff` und `grep` angehängt (Bauart der
  gleichnamigen Zeilen in TB-139 und TB-149).

## In einfacher Sprache

Die Sitzung hat zuerst den Auftrag und die Unterlagen des steuernden Chats ins Repo gesichert. Dann hat sie selbst
nachgemessen: Fables Antwort vom 10.10. liegt samt Anfrage und Übergabe mit einem Commit im Repo; der Satz aus einer
früheren Antwort (25c), auf den sich R91 beruft, steht dort so; der Satz in Abschnitt 15.5 steht noch so da, und kein
späterer Hinweis löst ihn ab; jede der 9 alten Stellen gibt es genau einmal. Alles traf zu. Erst danach hat sie Fables
vier Regeltexte (R90–R93) Zeichen für Zeichen ins Register kopiert, als Abschnitt 57, mit der Tabelle der Vormessungen
und der Liste der offenen Punkte. An 9 alten Stellen weisen 11 kleine Hinweise auf die neuen Texte; zwei davon trägt
Fable für Texte vom 09.10. nach. Kein alter Satz wurde geändert (103 Zeilen dazu, 0 weg). Alle Prüfungen und der grosse
Registertest (196/196) sind grün. Danach sind die Aufgabenliste, die Kopie des Registers für die Ablage (jetzt 58
Dateien und fünf Teile; Teil 4 ist fast voll, nur noch 165 Byte frei), der Wegweiser und die Liste der Fable-Antworten
erneuert. Am Code und an den Daten hat sich nichts geändert.
