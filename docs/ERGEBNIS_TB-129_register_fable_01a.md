# TB-129: Ergebnis. Register Abschnitt 51 — Fable 01a (R56–R62) zeichengleich, Tatsachennotizen 51.8–51.10, 14 Marken am alten Ort, numstat 131/0; Registerkopie neu in 52 Abschnittsdateien und 4 Teilen, Index und Dialog-Index nachgezogen

**Sitzungstitel:** `TB-129` · **Stand:** 02.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-129_register_fable_01a.md` ·
**Belege:** `docs/belege/TB-129/`
**Eingang:** `560ca75` (Abgabe TB-128), Arbeitsbaum wie 0a (drei Einträge). Commits: `477cef2` (Schritt 0, im Folgenden
⟨S0⟩), `b443bcb` (0: Ausgang, Vorprüfung), `f63ad4c` (A: Register, einziger Registercommit), `33b0999` (B/C: BACKLOG,
Registerkopie, Index, Dialog-Index), der Abgabe-Commit (D: dieses Dokument, Journal EA) und ein kleiner Commit mit
`d3_porcelain.txt`. Nach jedem Commit gepusht.
**Quelle (md5 am ⟨S0⟩ und im Arbeitsbaum geprüft, `0b_ausgang.txt`):**
`docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md`,
`4995260b7af91d2f4c058b1e2c49e788`, 22 084 B — gleich dem Soll.
**Freigabe:** Betreiber, 02.10.2026, Auswahlkarte im steuernden Chat (gestellt 09:13, eingetragen 10:02), „Freigeben wie
beschrieben (Empfohlen)“ (wörtlich im Auftrag). Keine Rückfrage an den Betreiber.
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | genau drei Einträge (` M` AKTUELLER_AUFTRAG, ` M` UEBERGABE, `??` Auftrag) | genau diese drei (`0a_status.txt`) |
| 0b | 11 094 Z., sha256 `b5804659…`, md5 `9a5a403f…`; `register()` `525c9c42…`, `fehlend []`, 23 Teile; Abbild `46f0ad5d…`; Sonde rc 2, 37/0/0, (ii) 0, Listentext ja, JSON ohne `zeilen` `9f7364ef…`; Quelle `4995260b…`/22 084 B | alles gleich (`0b_ausgang.txt`); `registerbericht.py --pruefen` rc 1 (bekannt, Vergleichswert); porcelain vor/nach Sonde 1/1 |
| 0c | `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` | leer ⇒ Basis `docs/belege/TB-126/a6_test_vorregistrierung.txt` (196/196), kein eigener Basislauf |
| 0d | Marken 14/14, Quelle R56–R62 je zwei Zeilen, `## 51.` 0 / `> R56 — ` 0, 43 Fundstellen, 7 Zählungen, Kalender beider Dateien, Git-Tatsachen | Prüfskript aus Anhang A (aus dem Auftrag am ⟨S0⟩ geschnitten, gegen den mit `git archive` ausgepackten Baum am ⟨S0⟩) rc 0; je Marke 14/14; Git-Tatsachen 3/3, Commit-Daten 2/2 (`0d_vorpruefung.txt`) |
| A4 | Probelauf an Kopie grün, dann echt, `cmp` gleich | Probelauf: 14 Marken an 11 Stellen, 11 094 → 11 225 Zeilen, alle Textprüfungen rc 0; echt identisch; `cmp` rc 0 |
| A5 R-Diff | 7/7 rc 0; Mutation rc 1 | **7/7**; Mutation (R60, „ die “ → „ der “) rc 1 |
| A5 Zitate | 2/2 | Kopf 51.0 und Schluss 51.8–51.10 **2/2** |
| A5 Überschriften/Ketten, Marken | 7/7, 14/14 | **7/7 und 7/7**, **14/14**; in Abschnitt 9, 10 und ERZEUGT-Block je 0 |
| A5 numstat | zweite Spalte 0 | **131/0** |
| A5 Abschnitt 10, ERZEUGT | bytegleich | beide `cmp` rc 0 (Abschnitt 10 jetzt Z. 962–1168, ERZEUGT Z. 260–460) |
| A5 `registerbericht --pruefen` | nachher = vorher | rc 1 / rc 1, Ausgabe `cmp` rc 0 |
| A5 Sonde | JSON ohne `zeilen` gleich, (ii) 0, Listentext ja | `9f7364ef…` gleich, (ii) 0, ja; Text der Sonde nennt jetzt Z. 987–1100 statt 969–1082 (erwartet) |
| A5 `register()` | ≠ vorher, `fehlend []`, 23 Teile | `a1e1366a…`, `[]`, 23 |
| A5 `test_vorregistrierung` | 196/196 | **196/196**, rc 0, 865 s |
| B | Anker 1, Text nachher 1, numstat 17/0, Block bytegleich | Anker 1 (Z. 243), erste Textzeile nachher 1, **17/0**, Bytevergleich GLEICH (3 097 B, 16 Zeilen, Leerzeile davor/danach, Anker danach) |
| C1 | fünf Aufrufe rc 0; 52 Abschnittsdateien | alle fünf rc 0; Teile 0–22 / 23–36 / 37–42 / **43–51**, bytegleich; **52** Abschnittsdateien `_00`–`_51`, bytegleich; keine Datei VERALTET |
| C2/C3 | Index nachgezogen | 184 Zahlen in Zeilenangaben umgeschrieben (175 geändert), 20 Ersetzungen je Anker 1, Abschnittstabelle 0–51 aus den Köpfen; Gegenprobe: 212/212 Zeilenangaben auf Markenzeilen, 14/14 Marken in Abschnitt 6, C3 zeichengleich, 52/52 Tabellenzeilen |
| C4 | `--pruefen` rc 0; Zeile 01a mit Fundstelle 51, Status offen; 51 Antworten | rc 0 / rc 0; Zeile 01a: Fundstelle 51, Status offen, offen ja; „51 Antworten.“; numstat 2/1, keine weitere Zeile geändert |

## `herkunft.register()`

| | Wert |
|---|---|
| vorher (Register `b5804659…`, 11 094 Z.) | `525c9c42af5022ad659388631c7959a0752a7cbaec05c3b319c280651caf1bfc` |
| nachher (Register `7f74b0e5…`, 11 225 Z.) | `a1e1366ab55719fe4724b9da3d9425f3029628d56460bcda8e2e4476dce8cc40` |

`fehlend []` und 23 Teile vorher wie nachher. Der neue Wert steht nur hier, nicht im Register (42.5).
Register nachher: sha256 `7f74b0e5a746cbc720b7b7c20af83acddd32d6652c3b57099f18769d3d4b16c4`, md5 `b4764e4e140caa37ecef515d73743e1f`.

## Wie eingetragen

- Vorlage `a4_vorlage_51.md` mit Platzhaltern, Einsetzskript `a4_eintrag.py` (Bauart TB-126 `a5_eintrag.py`). Alle Texte
  per `git show 477cef2:<pfad>`: Kopf und Schluss aus den zwei ````-Zäunen nach „Kopf:“ bzw. „Schluss:“, Überschriften,
  Ketten und Marken aus dem Daten-Block, die sieben Blöcke aus der Quelle Z. 113–132 nach der Schnittregel. ⟨S0⟩ ist als
  `` `477cef2` `` eingesetzt (mit Backticks, wie TB-126), ⟨DATUM⟩ als `02.10.2026`.
- Die Wachen des Auftrags stehen im Skript (Eingang 11 094, `## 51.` frei, keine Zeile `> R56 — `, alte Zeilen in
  Reihenfolge, Abschnitte 9 und 10 und ERZEUGT-Block unverändert, 14 Anker je 1 vorher und nachher).
- Die Nachweise (`a5_r_diff.py`, `a5_mutation.py`, `a5_zitate.py`, `a5_marken.py`) lesen Quelle und Auftrag selbst
  und schneiden selbst; Überschriften und Ketten liest `a5_marken.py` aus der Markdown-Tabelle 1, nicht aus dem JSON.
- 0d: Das Prüfskript aus Anhang A liest Dateien vom Dateisystem. Damit es „am Commit ⟨S0⟩“ prüft, packt
  `0d_vorpruefung.py` die 16 genannten Dateien mit `git archive 477cef2` in den Scratch und ruft es dort auf.

### Abweichungen vom Wortlaut der Vorlagen (nicht vom Auftrag)

1. **`c2_index_zeilen.py` schreibt jede Zahl einer Liste oder eines Bereichs um** („Z. 1297, 1300, …“, „Z. 2094–2189“).
   Die Vorlage aus TB-126 schrieb nur die erste Zahl um; damals lag keine Einfügung zwischen den Enden. Diesmal lag
   ebenfalls keine dazwischen, aber alle Bereiche lagen hinter Einfügungen, die zweite Zahl wäre also stehen geblieben.
   Ausgenommen ist die Zeile `*Frühere Vierteilung*`, die aus `c1` neu geschrieben ist.
2. **Index Z. 16** (Absatz „Kopie je Abschnitt“) nannte als Werkzeug `registerkopie_abschnitte.py`; seit TB-127 schneidet
   `registerkopie.py --abschnitte`. Der Satz nennt jetzt beides. Der Auftrag nennt für den Kopf nur Z. 3–5; der Satz
   gehört zum Verweis auf die Abschnittsdateien.
3. **Pflegezeile:** „Zuletzt nachgezogen in TB-126“ heisst jetzt „In TB-126“, die neue Zeile „Zuletzt nachgezogen in
   TB-129“ steht darunter.

## Markentabelle (gegen Anhang A)

| Nr | alter Ort (Anhang A) | nach Z. (alt) | Marke Z. (neu) | Wort | durch | Art | T |
|---|---|---|---|---|---|---|---|
| 1 | 1, Tabelle, Zeile 3 | 81 | 83 | PRÄZISIERT | R36 (48.4) | MARKE | 1 |
| 2 | 4.2 | 517 | 522 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 3 | 4.2 | 517 | 525 | PRÄZISIERT | R60 (51.5) | MARKE | 1 |
| 4 | 7, Tabelle, Zeile (b) | 805 | 816 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 5 | 8, Tabelle | 873 | 887 | PRÄZISIERT | R36 (48.4) | MARKE | 1 |
| 6 | 8, Tabelle | 873 | 890 | ERGÄNZT | R55 (49.3) | MARKE+ | 1 |
| 7 | 16.4, „Prüfung vor dem Tag“ | 2212 | 2232 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 8 | 25.3, Ersatztext | 4652 | 4675 | ERGÄNZT | R58 (51.3) | MARKE+ | 2 |
| 9 | Abschnitt 27 | 5164 | 5190 | ERGÄNZT | R56 (51.1) | MARKE+ | 2 |
| 10 | 43.2, Eintrag 43-7 | 9673 | 9702 | PRÄZISIERT | R33 (48.1) | MARKE | 4 |
| 11 | 48.16 (R48) | 10851 | 10883 | ERGÄNZT | R60 (51.5) | MARKE+ | 4 |
| 12 | 49.1 (R53) | 10898 | 10933 | PRÄZISIERT | R57 (51.2) | MARKE | 4 |
| 13 | 49.1 (R53) | 10898 | 10936 | ERGÄNZT | R59 (51.4) | MARKE+ | 4 |
| 14 | 50.5 | 11072 | 11113 | ERGÄNZT | R57 (51.2): die Lesart ist bestätigt | MARKE+ | 4 |

Quelle: `a4_eintrag_daten.json`, `a5_marken.txt`, `c1_marken.txt`, `c2_index_01a_tabelle.md`. Abschnitt 51 steht in
Z. 11138–11225. **Nicht gesetzt nach Anhang A (wie vorgesehen):** 47.9, 47.13, 25.2, 50.1, 50.4 — als Indexzeilen in
`REGISTER_INDEX.md` Abschnitt 6 (C3) und als Frage in 51.10 Nr. 7.

## Für Fable (nur Verfahrensfragen)

1. **51.9 (vorläufig) und 51.10 Nr. 6:** Lesart zu R60 (a) — die Voraussetzung trifft für den Ordner
   `research/exposure_messung/` nicht (`bot_lauf.py` steht im Laufbereich), wohl aber für die zwei Stellen, die die
   Grösse bilden; dazu R60 (b) und (c): über welche Tage gemittelt wird (`beta_bereinigung` nimmt die gemeinsamen Tage
   mit dem Benchmark; gegen „Handelstage des Zeitraums“ nach R48 (d) nicht gemessen). Die Fundstellen dazu hat 0d am
   ⟨S0⟩ nachgemessen, alle 43 wie in 51.8 angegeben.
2. **51.10 Nr. 7:** Fünf Orte ohne Marke (47.9, 47.13, 25.2, 50.1, 50.4). Sollen sie Marken tragen?
3. **Reibung beim Setzen, Werkzeug:** `registerkopie.py --marken` zählt die erste Zitatzeile von R61 (51.6) als Art
   `MARKE`, weil der Registertext selbst Marken mit „PRÄZISIERT durch“ aufzählt. Darum steht `MARKE` bei 64 statt
   55 + 8 = 63. Wer aus `--marken` Ketten liest, muss diese Zeile ausnehmen; im Index ist sie nicht als Marke geführt.
4. **Reibung, Markenwort:** „50.5 — bestätigt durch R57“ steht nach dem Auftrag mit ERGÄNZT und dem Zusatz „die Lesart
   ist bestätigt“, weil das Werkzeug kein Markenwort für Bestätigungen kennt (wie TB-126). Ob ein eigenes Wort
   (z. B. BESTÄTIGT) gewollt ist, wäre eine Regel für die Marken.

## Nicht getan

- 51.10 (alle acht Punkte): R56 (d)/(e), R59 (b)–(d), R57, R60 (a)–(c), die fünf Orte ohne Marke, R62 (b).
- Die Ablage (52 Abschnittsdateien, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`) — macht der steuernde Chat nach der
  27.4-Prüfung.
- Kein Code, kein neues Abbild, keine Einträge in `registerdaten.py`, keine Läufe von `auswertung.py`.
- `registerbericht.py --pruefen` rc 1 bleibt (schon vor TB-126; Zahlenteil veraltet).

## Nebenbemerkungen zum Ablauf

- `test_vorregistrierung` lief am echten Register vor dem Commit A (865 s); erst danach ist committet.
- Die Sonde nennt den Registertext von Abschnitt 10 jetzt in Z. 987–1100; der Abschnitt wandert um 18 Zeilen, wie
  im Auftrag erschlossen. Ihr JSON ohne `zeilen` ist gleich.
- Journal EA: Die `git diff`-Darstellung nach dem Einfügen sah nach einer Leerzeile zu viel aus; ein `git checkout`
  der Datei wurde von der Berechtigung abgelehnt (nicht freigegeben, zu Recht). Direkt gemessen war die Form richtig;
  nichts geändert (`d2_journal.txt`).
- Die Teile der Registerkopie bleiben vier (T4 = 43–51, 180 076 B); T3 ist mit 232 429 B nahe der Grenze 240 000 B,
  aber unverändert, weil in 37–42 keine Marke steht.

## In einfacher Sprache

Fables sieben neue Regeltexte vom 01.10. stehen jetzt Zeichen für Zeichen im Register, als Abschnitt 51, dazu die
Messungen und offenen Punkte des steuernden Chats. An 14 alten Stellen weist eine kleine Marke auf die neuen Texte.
Kein alter Satz wurde geändert (131 Zeilen dazu, 0 weg), alle Prüfungen und der grosse Registertest (196/196) sind
grün. Danach sind die Kopie des Registers für die Ablage (52 Dateien), der Wegweiser und die Liste der Fable-Antworten
neu erzeugt. Am Code hat sich nichts geändert.
