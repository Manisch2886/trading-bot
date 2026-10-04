# TB-132: Ergebnis. Probe zu R71 in der Lock-Umgebung gleich der Vormessung; Register Abschnitt 53 — Fable 02c (R66–R73) zeichengleich, Tatsachennotizen 53.9–53.10, 21 Marken am alten Ort, numstat 158/0; Registerkopie neu in 54 Abschnittsdateien und 4 Teilen, Index und Dialog-Index nachgezogen

**Sitzungstitel:** `TB-132` · **Stand:** 04.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-132_register_fable_02c.md` (Neubau 04.10.2026) ·
**Belege:** `docs/belege/TB-132/`
**Eingang:** `0779453` (TB-131, D3; = `origin/main`), Arbeitsbaum wie 0a (zehn Einträge). Commits: `57ae0d8` (Schritt 0, im
Folgenden ⟨S0⟩), `f32b5c7` (0: Ausgang, Vorprüfung, Probe), `ee43f5f` (A: Register, einziger Registercommit), `12010b2`
(B/C: BACKLOG, Registerkopie, Index, Dialog-Index), der Abgabe-Commit (D: dieses Dokument, Journal ED) und ein kleiner
Commit mit `d3_porcelain.txt`. Nach jedem Commit gepusht, jeder Push im ersten Versuch.
**Quelle (md5 am ⟨S0⟩ und im Arbeitsbaum geprüft, `0b_ausgang.txt`):**
`docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md`,
`6aad30eca53d038b65f24577680f7774`, 30 216 B — gleich dem Soll.
**Freigabe:** Betreiber, 03.10.2026 (Auswahlkarte, eingetragen 07:28) und Neubau 04.10.2026 (Auswahlkarte, gestellt gegen
08:00, eingetragen 08:41), je „Freigeben wie beschrieben (Empfohlen)“ (wörtlich im Auftrag). Keine Rückfrage an den Betreiber.
**Umgebung:** Mac, Hauptordner `~/trading-bot`, lokal; `trading-env/bin/python3` (3.9.6). Gestartet über den Einfügesatz
`TB-132: …`; Datum des Rechners 04.10.2026 (0a, 08:51). Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a Datum | `04.10.2026` | `04.10.2026` (08:51:20) |
| 0a Arbeitsbaum | genau die zehn Einträge des Auftrags | genau diese zehn (`0a_status.txt`) |
| 0a Skripte | sha256 `8ef716ac…` (Prüfskript), `c75b6e88…` (Einfügeskript) | beide gleich; nach dem Kopieren nach `0d_vorpruefung.py` und `a4_eintrag.py` noch einmal gleich |
| 0a Prüfskript `--arbeitsbaum` | rc 0 | rc 0; `Datum: 04.10.2026 wie verlangt`, Arbeitsbaum geändert 2 (Soll 2), unverfolgt 16 (Soll 16); die fünf Zeilen `Marken:` … `Bloecke:` und `Dateien:` wie unter „Prüfsumme“ (`0a_pruefung.txt`) |
| 0b | 11 313 Z., sha256 `a7496780…`, md5 `80af174f…`; `register()` `4caf0179…`, `fehlend []`, 23 Teile; Abbild `46f0ad5d…`; Sonde rc 2, 37/0/0, (ii) 0, Listentext ja, JSON ohne `zeilen` `9f7364ef…`; Quelle `6aad30ec…`/30 216 B; Abschnitt 10 `da8697c0…`, ERZEUGT `fda8ead1…` | alles gleich (`0b_ausgang.txt`); `registerbericht.py --pruefen` rc 1 (bekannt, Vergleichswert); Abschnitt 10 Z. 965–1171, ERZEUGT Z. 260–460 |
| 0c | `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` | leer ⇒ Basis `docs/belege/TB-130/a5_test_vorregistrierung.txt` (196/196), kein eigener Basislauf |
| 0d | rc 0, erste Zeile `Datum: 04.10.2026 wie verlangt`, fünf Zeilen wie „Prüfsumme“, `rc 0: alles wie angegeben` | genau so; `*.py im Baum: 681` (679 + die zwei Skripte der Sitzung, wie im Auftrag erwartet) (`0d_vorpruefung.txt`) |
| ⭐⭐ 0e Probe | rc 0; Zeile 3 `  pandas 2.3.3, numpy 2.0.2, Python 3.9.6`; ab `A - Faelle` zeilengleich (20/20); Vergleich rc 0 | **alle vier erfüllt** (siehe unten) |
| A4 | Probelauf an Kopie grün, dann echt, `cmp` gleich; `21 an 13`, `8 (R66-R73)`, `11313 → 11471, 158` | Probelauf und echter Lauf je genau diese Ausgabe, sha256 nachher in beiden `9a2cefb7…`; `cmp` rc 0; `git diff --quiet ⟨S0⟩ -- Auftrag Quelle` rc 0 vor beiden Läufen |
| A5 R-Diff | 8/8 rc 0; Mutation rc 1 | **8/8**; Mutation (R66 unter 53.1, „ die “ → „ der “) rc 1 |
| A5 Zitate | 2/2 | Kopf 53.0 und Schluss 53.9–53.10 **2/2** |
| A5 Überschriften/Ketten, Marken | 8/8, 21/21 | **8/8 und 8/8**, **21/21**, jede Markenzeile einmal; in Abschnitt 9, 10 und ERZEUGT-Block je 0 |
| A5 numstat, Zeilen | `158	0`, 11 471 | **158/0**, 11 471 |
| A5 Abschnitt 10, ERZEUGT | bytegleich gegen 0b | beide gleich (Z. 965–1171 und 260–460, unverschoben) |
| A5 `registerbericht --pruefen` | nachher = vorher | rc 1 / rc 1, Ausgabe bytegleich |
| A5 Sonde | JSON ohne `zeilen` gleich, (ii) 0, Listentext ja | `9f7364ef…` gleich, (ii) 0, ja; diesmal auch der Text bytegleich (keine Marke vor Abschnitt 10) |
| A5 `register()` | ≠ vorher, `fehlend []`, 23 Teile | `66480962…`, `[]`, 23 |
| A5 `test_vorregistrierung` | 196/196, am echten Register vor dem Commit | **196/196**, rc 0, 892 s (`a5_test_vorregistrierung.txt`) |
| B | Anker 1, erste Textzeile nachher 1, numstat `10	0`, Block bytegleich | Anker 1 (Z. 276), erste Textzeile vorher 0 / nachher 1, **10/0**, GLEICH (2 579 B, 9 Zeilen, Leerzeile davor/danach, Anker danach) |
| C1 | fünf Aufrufe rc 0; 54 Abschnittsdateien `_00`–`_53` | alle fünf rc 0; Teile 0–22 / 23–36 / 37–42 / **43–53**, bytegleich (T4 232 545 B ≤ 240 000); **54** Abschnittsdateien, bytegleich; keine Datei VERALTET |
| C2 | Index nachgezogen | 236 Zahlen in Zeilenangaben umgeschrieben (159 geändert), 9 Ersetzungen und 5 Tabellenzeilen je Anker 1, Zeile 53, Abschnitt 8 mit 21 Marken, Abschnittstabelle 0–53 aus den Köpfen |
| C3 | vorher `Indexzeilen aus Fable 02c` 0; drei Zeilen zeichengleich | 0 vorher (vor C2 und vor C3 gezählt); Block eingesetzt, 3/3 zeichengleich |
| C2/C3 Gegenprobe | — | 278/278 Zeilenangaben auf Markenzeilen; 14/14 (Abschnitt 6), 12/12 (7), 21/21 (8); C3 zeichengleich; Indexzeilen 01a 5; 54/54 Tabellenzeilen; Indexzeilen E-2 6 (`c2_index_pruefen.txt`) |
| C4 | `--pruefen` rc 0; 54 Antworten; 02c Fundstelle 53, offen; 02b Fundstelle 53, registriert; 02a registriert, Frage/Entscheidung unverändert | rc 0 / rc 0; genau so; „54 Antworten.“; numstat 4/2: die Zeilen 02a (Status, offen), 02b, 02c und die Schlusszeile, **keine weitere Zeile geändert** |

## Probe in der Lock-Umgebung (0e; R71, R72 erste Voraussetzung)

Aufruf genau wie im Auftrag (Repo-Wurzel, Variablen `TB_SELEKTIONS*`, `TB30A_BASE_DIR`, `R71_BENCHMARK` gelöscht,
`PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 trading-env/bin/python3 docs/belege/TB-132/vormessung/r71_probe.py`), einmal.

| Punkt | Soll | Ist |
|---|---|---|
| 1 Rückgabewert | 0 | `rc 0` (`probe_lock_r71_rc.txt`) |
| 2 Zeile 3 | `  pandas 2.3.3, numpy 2.0.2, Python 3.9.6` | `  pandas 2.3.3, numpy 2.0.2, Python 3.9.6` (wörtlich) |
| 3 ab `A - Faelle` | zeilengleich mit `vormessung/ausgabe_pandas_2.3.3.txt` | `Zeilen ab 'A - Faelle': 20 (Vergleich 20)`; letzte Zeile `ERGEBNIS: Aussage bestaetigt unter pandas 2.3.3 -> Rueckgabewert 0` |
| 4 Vergleich | `rc 0: alles wie angegeben`, `rc 0` | genau so (`0e_probe_vergleich.txt`) |

- `probe_lock_r71_stderr.txt`: **leer** (0 B).
- `0e_pycache.txt`: **leer** — die Probe hat keinen `__pycache__` und keine `*.pyc` angelegt oder erneuert.
- Zeile 1–2 der Ausgabe: Pfad `/Users/jaquelineloffler/trading-bot/research/vorregistrierung/benchmark.py`, SHA-256
  `aeeec9b89bdadd1b2dc2be76b722dc90c328c9482014bbbbfcabd78edccae219`.
- `git status --porcelain` danach: neu nur Dateien unter `docs/belege/TB-132/` (`0e_status_nachher.txt`).
- Damit ist die Wiederholung, die R71 und R72 „vor dem Eintrag“ verlangen, auf dem Betriebsrechner in der Lock-Umgebung
  gelaufen; die Wache im Einfügeskript hat dieselbe Ausgabe im Probelauf und im echten Lauf noch einmal geprüft.

## `herkunft.register()`

| | Wert |
|---|---|
| vorher (Register `a7496780…`, 11 313 Z.) | `4caf01793c8c4bb979eeea0243cff7a1b13004c28716391f61e8a5978a407b56` |
| nachher (Register `9a2cefb7…`, 11 471 Z.) | `664809629137b537d233e19066ac6ab9d422c64be8841ff37c72862e0eb511b3` |

`fehlend []` und 23 Teile vorher wie nachher. Der neue Wert steht nur hier, nicht im Register (42.5).

## Register nachher

11 471 Zeilen · sha256 `9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff` ·
md5 `1ce393ae2f07513fa76ccc0b0f927d41`. Abschnitt 53 steht in Z. 11378–11471 (53.1 Z. 11382, 53.2 Z. 11389, 53.3
Z. 11396, 53.4 Z. 11403, 53.5 Z. 11410, 53.6 Z. 11417, 53.7 Z. 11424, 53.8 Z. 11431, 53.9 Z. 11438, 53.10 Z. 11456).
⟨S0⟩ ist im Register als `` `57ae0d8` `` eingesetzt.

## Wie eingetragen

- Einfügeskript aus Anhang A, unverändert (`a4_eintrag.py`, sha256 `c75b6e88…`), Probelauf mit `--s0 57ae0d8 --register
  <Kopie im Scratch>` über `a4_probelauf.sh`, danach echt mit `--s0 57ae0d8 --daten docs/belege/TB-132/a4_eintrag_daten.json`.
  `--vorschau` nicht benutzt. Beide Wachen (Datum, Probe) liefen in beiden Läufen.
- Nachweise nach der Bauart TB-130 (`a5_r_diff.py`, `a5_mutation.py`, `a5_zitate.py`, `a5_marken.py`, `a5_nachweis.sh`),
  angepasst auf 53/R66–R73/21 Marken; sie lesen Auftrag und Quelle selbst per `git show 57ae0d8:…`. `a5_marken.py` liest
  Überschriften und Ketten aus der Markdown-Tabelle 1 (dort ist gegenüber TB-130 die Spalte „Zeichen“ dazugekommen; das
  Skript überspringt sie).
- Ausgang und Nachher-Messung mit demselben Skript `0b_ausgang.sh` (Vorlage TB-130), `vorher` bzw. `nachher`.
- Index: `c2_index_zeilen.py` (Abbildung über die unveränderten alten Zeilen, Stand `ad351d5` = Register am ⟨S0⟩),
  `c2_index_02c.py` (Tabelle für Abschnitt 8 aus `c1_marken.txt` und Anhang A), `c2_index_eintraege.py` (Kopf, „Wie
  gemessen“, 1a und 1c in Tabelle 3, Zeilen 23/27/48/51/52 und neue Zeile 53 in Tabelle 4, Abschnitt 8, Pflege),
  `c3_indexzeilen.py` (Block aus dem Auftrag am ⟨S0⟩), Gegenprobe `c2_index_pruefen.py`. Die Pflegezeile nennt den
  Blocktitel absichtlich nicht wörtlich (Lehre aus TB-130: sonst zählt C3 vorher 1 statt 0).
- Dialog-Index: `c4_handfelder.json` aus dem Codeblock des Auftrags am ⟨S0⟩ geschnitten (`cmp` gegen den Auftrag: ja),
  dann `c4_dialog_index.sh`.

## Markentabelle (gegen Anhang A)

| Nr | alter Ort (Anhang A) | nach Z. (alt) | Marke Z. (neu) | Wort | durch | Art | T |
|---|---|---|---|---|---|---|---|
| 1 | 15.3 (a) | 1447 | 1449 | PRÄZISIERT | R66 (53.1) | MARKE | 1 |
| 2 | 15.3 (c) | 1447 | 1452 | PRÄZISIERT | R66 (53.1) | MARKE | 1 |
| 3 | 23.3, Registertext 3b (c) | 3939 | 3947 | PRÄZISIERT | R72 (53.7) | MARKE | 2 |
| 4 | 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse | 3964 | 3975 | BERICHTIGT | R71 (53.6) | MARKE+ | 2 |
| 5 | 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse | 3964 | 3978 | ERGÄNZT | R72 (53.7) | MARKE+ | 2 |
| 6 | Abschnitt 27 | 5197 | 5214 | ERGÄNZT | R73 (53.8) | MARKE+ | 2 |
| 7 | 48.1 (R33) | 10774 | 10794 | PRÄZISIERT | R68 (53.3) | MARKE | 4 |
| 8 | 48.5 (R37) | 10802 | 10825 | PRÄZISIERT | R68 (53.3) | MARKE | 4 |
| 9 | 48.7 (R39) | 10816 | 10842 | ERGÄNZT | R67 (53.2) | MARKE+ | 4 |
| 10 | 48.7 (R39) | 10816 | 10845 | ERGÄNZT | R69 (53.4): R39 ist bestätigt | MARKE+ | 4 |
| 11 | 48.16 (R48 (d)) | 10899 | 10931 | ERGÄNZT | R72 (53.7) | MARKE+ | 4 |
| 12 | 51.5 (R60) | 11203 | 11238 | PRÄZISIERT | R69 (53.4) | MARKE | 4 |
| 13 | 51.6 (R61) | 11213 | 11251 | PRÄZISIERT | R70 (53.5) | MARKE | 4 |
| 14 | 52.2 (R64) | 11277 | 11318 | ERGÄNZT | R66 (53.1) | MARKE+ | 4 |
| 15 | 52.2 (R64) | 11277 | 11321 | PRÄZISIERT | R68 (53.3) | MARKE | 4 |
| 16 | 52.2 (R64) | 11277 | 11324 | PRÄZISIERT | R69 (53.4) | MARKE | 4 |
| 17 | 52.2 (R64) | 11277 | 11327 | PRÄZISIERT | R71 (53.6): erster Kurstag | MARKE | 4 |
| 18 | 52.2 (R64) | 11277 | 11330 | PRÄZISIERT | R72 (53.7): Benchmark-Tag | MARKE | 4 |
| 19 | 52.3 (R65) | 11284 | 11340 | PRÄZISIERT | R70 (53.5) | MARKE | 4 |
| 20 | 52.4, nach der Tabelle | 11299 | 11358 | ERGÄNZT | R66 (53.1) | MARKE+ | 4 |
| 21 | 52.4, nach der Tabelle | 11299 | 11361 | BERICHTIGT | R69 (53.4) | MARKE+ | 4 |

Quelle: `a4_eintrag_daten.json`, `a5_marken.txt`, `c1_marken.txt`, `c2_index_02c_tabelle.md`. 21 Marken an 13
Einfügestellen. Nr. 1, 2, 4–21 zählt R70 (c) auf; Nr. 3 hat der steuernde Chat nach R65 (a) bestimmt (Kopf 53.0,
53.10 Nr. 8). **Nicht gesetzt nach Anhang A (wie vorgesehen):** 7 (c), 17.5, 50.7 Nr. 3 (Indexzeilen, Abschnitt 8 des
Index), 24.2, 29.3; keine Marke in Abschnitt 9, 10 und im ERZEUGT-Block.

## Für Fable (nur Verfahrensfragen)

1. **53.10 Nr. 1:** Kalendername für die Aktien-Tagesreihe (R66 (a), (b)). Der Code des Laufs benutzt keinen; im Repo
   steht nur „NYSE“ im Live-Pfad (`notifications/boersenkalender.py`); „XNYS“ führt im gemessenen Fenster einen
   Handelstag mehr (53.9).
2. **53.10 Nr. 2:** Deckelfall nach R68 (d) — Behandlung in den Gleichheitsproben nach R60 (c) und R64 (d) und in der
   Nachrechnung nach R36; vor der Öffnung nach R69 (b).
3. **53.10 Nr. 8, zur Kenntnis:** die Marke an 23.3, Registertext 3b (c), PRÄZISIERT durch R72 (b), vom steuernden Chat
   nach R65 (a) bestimmt; R70 (c) nennt sie nicht.
4. **53.10 Nr. 9, zur Kenntnis:** die zehn sinngemässen Verweise aus 53.9 (letzte Zeile).
5. **Reibung beim Setzen, Werkzeug (wie TB-129 bei R61, TB-130 bei R65):** `registerkopie.py --marken` zählt drei Zeilen
   in Abschnitt 53 als Marken, die keine sind: die erste Zitatzeile von R70 (Z. 11412, `MARKE`), seine Zeile „Quelle des
   Grundes“ (Z. 11413, `MARKE+`) und die Zeile 53.10 Nr. 8 (Z. 11467, `MARKE`, sie nennt „PRÄZISIERT durch R72 (b)“).
   Darum stehen die Arten bei `MARKE` 84 = 70 + 12 + 2, `MARKE+` 121 = 111 + 9 + 1, `UEBERSCHRIFT` 88 = 82 + 6 (53.1–53.5
   und 53.7 tragen einen Rückverweis im Titel). Im Index ist keine dieser drei Zeilen als Marke geführt.
6. **Reibung, Index Tabelle 3, Zeile 3b (c):** C2 nennt für Tabelle 3 nur 15.3. Die Kette 16.7 (c) ERSETZT durch 23.3 →
   23.3, Registertext 3b (c) PRÄZISIERT durch R72 (53.7) steht deshalb nur in Tabelle 4 (Zeile 23); in Tabelle 3 sagt
   die Spalte „gilt“ für 3b (c) weiter nur „**23.3** (T2)“. Nicht geändert, weil nicht beauftragt; Vorschlag für den
   nächsten Indexlauf: dort „**mit** 53.7 R72 (b) (T4)“ ergänzen.
7. **Reibung, Markenwort (wie TB-129, TB-130):** Die Bestätigung an 48.7 (Nr. 10) steht als ERGÄNZT mit Zusatz „R39 ist
   bestätigt“ (R65 (a)).

## Nicht getan

- 53.10 (alle zehn Punkte): Anfragen an Fable (Nr. 1, 2, 8, 9), Verfahrensmessung am Snapshot (Nr. 3, 10), Öffnung von
  `auswertung.py` (Nr. 4), Zellen-Erzeuger (Nr. 5), Wiederholung der Probe bei neuer pandas-Fassung (Nr. 6), Tagesbasis
  des DSR (Nr. 7).
- Die Ablage (54 Abschnittsdateien, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`) — macht der steuernde Chat.
- Kein Code (die Wachen nach R66 (b), R66 (e) und R67, die Bewertung nach R72 (c), die Öffnung nach R69 (b) sind nicht
  Gegenstand), kein neues Abbild, keine Läufe von `auswertung.py`, Zellen-Erzeugern oder Backtests; `p3_probe.py` nicht
  ausgeführt; die Dateien unter `vormessung/` nicht geändert.
- `registerbericht.py --pruefen` rc 1 bleibt (schon vor TB-126; Zahlenteil veraltet).

## Nebenbemerkungen zum Ablauf

- `test_vorregistrierung` lief am echten Register vor dem Commit A (892 s, mit `nohup` im Hintergrund); erst danach ist
  committet. Während des Laufs liefen nur lesende Prüfungen und das Vorbereiten der B/C-Skripte (ohne Schreiben in
  BACKLOG, Index oder Kopie); die Sonde zählte deshalb vorher/nachher 17 statt 6 Porcelain-Zeilen (die neuen Belege).
- Die Teile der Registerkopie bleiben vier; T4 = 43–53 wächst auf 232 545 B (Grenze 240 000). **Beim nächsten
  Registerabschnitt dieser Grösse dürfte T4 die Grenze überschreiten** — das Werkzeug schneidet dann neu.
- Abschnitt 10 und der ERZEUGT-Block haben sich nicht verschoben; der Sonde-Text ist diesmal bytegleich, nicht nur das JSON.
- Der Index nennt in der Pflegezeile „vom Stand `ad351d5`“: das ist der letzte Registercommit vor A; das Register am
  ⟨S0⟩ ist damit bytegleich (sha256 `a7496780…`).

## In einfacher Sprache

Zuerst hat die Sitzung auf dem Betriebsrechner, in genau der Programmumgebung, in der später gerechnet wird, einen kleinen
Test wiederholt. Er zeigt dasselbe wie die Vormessung. Erst danach hat sie Fables acht neue Regeltexte vom 02.10. Zeichen
für Zeichen ins Register kopiert, als Abschnitt 53. Dazu kommen die nachgemessenen Code-Stellen und die offenen Punkte des
steuernden Chats. An 21 alten Stellen weist eine kleine Marke auf die neuen Texte. Kein alter Satz wurde geändert
(158 Zeilen dazu, 0 weg). Alle Prüfungen und der grosse Registertest (196/196) sind grün. Danach sind die Kopie des
Registers für die Ablage (54 Dateien), der Wegweiser und die Liste der Fable-Antworten neu erzeugt. Am Code hat sich
nichts geändert.
