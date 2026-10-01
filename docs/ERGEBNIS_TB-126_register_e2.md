# TB-126: Ergebnis. Register E-2 — Fable 27c, 29b, 30a (R18–R55) zeichengleich als Abschnitte 47–49, Tatsachennotizen in 50, 88 Marken (87 am alten Ort, 1 unter 48.16), numstat 747/0; Registerkopie neu in 4 Teilen, Index nachgezogen

**Sitzungstitel:** `TB-126` · **Stand:** 01.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-126_register_e2.md` ·
**Belege:** `docs/belege/TB-126/`
**Eingang:** `41864d4` (Abgabe TB-125). Commits: `0f56aeb` (Schritt 0, im Folgenden ⟨S0⟩), `1e13135` (0: Worktrees,
BACKLOG, Ausgang, Vorprüfung), `db108a6` (A: Register, einziger Registercommit), `8687eef` (C: Registerkopie und
Index), der Abgabe-Commit (D: dieses Dokument, Journal DX) und ein kleiner Commit mit `d3_porcelain.txt`. Nach jedem
Commit gepusht.
**Quellen (md5 am ⟨S0⟩ geprüft, `0d_ausgang.txt`):** 27c `ff96392ed654fdcae2e991e51e424dc5` (48 420 B), 29b
`898d5bd53b6617209b7ce4f7e8992941` (73 703 B), 30a `f9cdbbef543ec54ed07ee0566c336dde` (12 925 B) — alle drei gleich
dem Soll im Auftrag.
**Freigabe:** Betreiber, 01.10.2026, ca. 08:22, Auswahlkarte „Freigeben wie beschrieben (Empfohlen)“ (wörtlich im
Auftrag). Keine Rückfrage an den Betreiber in dieser Sitzung.
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | genau fünf Einträge | genau die fünf ⇒ `0f56aeb` |
| 0b | beide Worktrees mit `git worktree remove` (ohne `--force`) | `tb123_vorher2` entfernt (rc 0, `test -d` rc 1). ⚠️ **`tb123_vorher` verweigert** (rc 128, „contains modified or untracked files“): vier unverfolgte Einträge, alle **Symlinks** auf den Hauptordner (`data_sicherung`, `logs`, `research/turn_of_month/daten`, `trading-env`). Nicht erzwungen, liegt noch. Kein Abbruch |
| 0c | Anker 1, erste Zeile nachher 1, numstat `5 0` | 1 / 1 / `5 0` |
| 0d | Register 10 347 Z., `18e39ee2…`, `c8a32c0f…`; `register()` `01f5997a…`, `fehlend []`, 23 Teile; Sonde rc 2, 37/0/0, (ii) 0, „ja“ | alles wie Soll. Sonde-JSON ohne `zeilen`: `9f7364ef…`; porcelain vor/nach Sonde 2/2. `registerbericht.py --pruefen`: **rc 1** („GESCHEITERT: der erzeugte Block steht nicht woertlich im Register - die Zahlen dort sind veraltet.“) — kein Soll, Vergleichswert |
| 0e | 196/196 | 196/196, rc 0, 895 s |
| 0f | leer, leer, `4f4b455e…` | leer, leer, `4f4b455e…` |
| 0g | Nr. 1–4 wie angegeben | 87/87 Anker genau 1, alle Einfügestellen wie angegeben (0 Abweichungen); Prüfskript aus Anhang A zeichengleich übernommen, gegen `git archive ⟨S0⟩` rc 0 mit derselben Ausgabe wie im Auftrag; Entwürfe TB-122/TB-124 Grenzen ja/ja; Docstring Z. 36–67, Zählungen 1/0/0/0 |
| A5 | Probelauf an Kopie grün, dann echt, `cmp` gleich | Probelauf rc 0, alle Textprüfungen grün; Echtlauf rc 0; `cmp` Register ↔ Kopie rc 0 |
| A6 R-Diff | 38/38 rc 0; Mutation rc 1 | **38/38 rc 0**; Mutation (R40, ein Wort) rc 1 |
| A6 Zitate | 4/4 und 3/3 | **4/4** (Köpfe 47.0, 48.0, 49.0, Text 50) und **3/3** (Docstring, Entwurf TB-122, Entwurf TB-124) |
| A6 Überschriften/Marken | 38/38; Marken gegen Anhang A | **38/38**; **88/88 gesetzt**, Markenzeilen im Register 88; in 9: 1, in 10: 0 |
| A6 numstat | zweite Spalte 0 | **747 / 0** |
| A6 Abschnitt 10, ERZEUGT | bytegleich | beide bytegleich (`cmp` rc 0; Abschnitt 10 jetzt Z. 944–1150, ERZEUGT Z. 257–457) |
| A6 `registerbericht --pruefen` | nachher = vorher | rc 1, Ausgabe bytegleich mit vorher (`cmp` rc 0) |
| A6 Sonde | JSON ohne `zeilen` = vorher; (ii) 0; „ja“ | `9f7364ef…` = vorher; (ii) 0; „Listentext wie bei Erzeugung: ja“ (jetzt Z. 969–1082); rc 2, 37/0/0 |
| A6 `register()` | ≠ vorher, `fehlend []`, 23 Teile | siehe unten; `fehlend []`, 23 Teile |
| A6 `test_vorregistrierung` | 196/196 | **196/196**, rc 0, 910 s |
| C1 | `--pruefen` rc 0, Teile ≤ 240 000 B | 4 Teile: 0–22 (218 584 B), 23–36 (221 323 B), 37–42 (232 429 B), 43–50 (157 838 B); `--pruefen` rc 0 „BYTEGLEICH“; kein Teil VERALTET |
| C2 | Index nach Bauart nachgezogen | Kopf, Messhinweis (MARKE 55, MARKE+ 98, UEBERSCHRIFT 76), Teiltabelle, 32 Zeilenangaben umgeschrieben, Spalte T (23 → T2, 37 → T3, 43 → T4), 88 Marken in Tabelle 1–4 und als neuer Abschnitt 5, Zeilen 47–50; Gegenprobe 184/184 Zeilenangaben zeigen auf Markenzeilen |
| C3 | sechs Indexzeilen | 6/6 (5 bei Abschnitt 10 in Tabelle 2, 1 bei 17.3/17.9/18 unter Abschnitt 18 in Tabelle 4) |

## `herkunft.register()`

| | Wert | Beleg |
|---|---|---|
| vorher (⟨S0⟩) | `01f5997a9a13b4b30162e2a04965670a9ffa8d725a93d579e530dc0708ec2a70` | `0d_ausgang.txt` |
| nachher (`db108a6`) | `525c9c42af5022ad659388631c7959a0752a7cbaec05c3b319c280651caf1bfc` | `a6_messung_nachher.txt` |

Der neue Wert steht nur hier, nicht im Register (Selbstbezug, 42.5). Register nachher: 11 094 Zeilen, sha256
`b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1`, md5 `9a5a403f1488e00cb61cab7a4de25953`.

## Wie eingetragen

- Vorlage `a5_vorlage_47_50.md` (nur Platzhalter `⟦KOPF:n⟧`, `⟦BLOCK:R⟧`, `⟦TEXT:50⟧`), Einsetzskript `a5_eintrag.py`.
  Das Skript liest alles am ⟨S0⟩ per `git show`: Köpfe und Text 50 aus den ````-Zäunen des Auftrags, Überschriften und
  Marken aus dem Daten-Block von Anhang A, die Blöcke mit der Schnittregel aus den drei Quellen, Docstring und
  Entwürfe aus ihren Dateien. ⟨S0⟩ ist als `` `0f56aeb` `` eingesetzt, ⟨DATUM⟩ als `01.10.2026`, ⟨Z_A⟩/⟨Z_B⟩ als 36/67.
- Die Nachweisskripte (`a6_r_diff.py`, `a6_zitate.py`, `a6_marken.py`, `a6_mutation.py`) schneiden und vergleichen
  selbst, unabhängig vom Einsetzskript. Alle Skripte und Vergleiche liegen unter `docs/belege/TB-126/`.

### Zwei Stellen, an denen ich vom Wortlaut des Auftrags abgewichen bin

1. **Trennzeichen in der Kette.** Der Auftrag sagt „kommagetrennt“. Die Orte aus Tabelle 2 tragen selbst Kommas
   („1, Tabelle, Zeile 4“, „45.5, Block R5, Punkt (a)“); kommagetrennt wäre „Marken: 1, Tabelle, Zeile 4, 1, Tabelle,
   Zeile 3, 2.1 …“ nicht mehr lesbar. Ich habe die Orte mit „; “ getrennt. Für R54 ist der Ort der Marke unter 48.16
   „48.16 (R48), neu in TB-126“ (Spalte Registerstelle, Zeile 88, ohne Klammerzusatz „Ankerzeile“, den diese Zeile nicht hat).
2. **Eine zusätzliche Leerzeile nach Marke Nr. 13** (5.1 Nr. 7). Das ist die einzige Einfügestelle, nach der keine
   Leerzeile folgt: direkt danach steht `8. **Falten ohne Trade …`. Ohne Leerzeile zöge Markdown diese Zeile als
   Fortsetzung ins Blockzitat der Marke. Die Marke selbst (Leerzeile, zwei Zeilen) ist wie vorgegeben; die alte Zeile
   ist unverändert (numstat 0).

Beides steht so im Docstring von `a5_eintrag.py`. Keine der Textprüfungen aus A6 hängt daran.

## Markentabelle (gegen Anhang A)

Alle 88 gesetzt, keine Abweichung in 0g, keine Marke ausgelassen. „Zeile“ ist die Zeile der ersten Markenzeile im
Register am `db108a6` (aus `a6_marken.txt`).

| Nr | R (Unterpunkt) | alter Ort | Wort und Ziel | Zeile | Stand |
|---|---|---|---|---|---|
| 1 | R49 (f) | Kopf, Absatz „Stand: 14.09.2026“ | ERGÄNZT durch R49 (48.17) | 6 | gesetzt |
| 2 | R48 (a) | 1, Tabelle, Zeile 4 | PRÄZISIERT durch R48 (48.16) | 74 | gesetzt |
| 3 | R48 (j) | 1, Tabelle, Zeile 3 | PRÄZISIERT durch R48 (48.16) | 77 | gesetzt |
| 4 | R51 | 1, Tabelle, Zeile 2 | ERGÄNZT (Verweis) durch R51 (48.19) | 80 | gesetzt |
| 5 | R48 (i) | 2.1 | PRÄZISIERT durch R48 (48.16) | 127 | gesetzt |
| 6 | R48 (h) | 2.2 | PRÄZISIERT durch R48 (48.16) | 144 | gesetzt |
| 7 | R49 (a) | 2.2 | ERGÄNZT durch R49 (48.17) | 147 | gesetzt |
| 8 | R48 (f) | 2.5 | PRÄZISIERT durch R48 (48.16) | 203 | gesetzt |
| 9 | R49 (b) | 2.7 | ERGÄNZT durch R49 (48.17) | 244 | gesetzt |
| 10 | R49 (c) | 3, Zahlenteil (nach ENDE ERZEUGT) | ERGÄNZT durch R49 (48.17) | 459 | gesetzt |
| 11 | R51 | 4.2 | ERGÄNZT (Verweis) durch R51 (48.19) | 516 | gesetzt |
| 12 | R49 (c) | 4.4 | ERGÄNZT durch R49 (48.17) | 571 | gesetzt |
| 13 | R37 | 5.1, Nr. 7 | PRÄZISIERT durch R37 (48.5) | 634 | gesetzt |
| 14 | R51 | 5.3 | ERGÄNZT (Verweis) durch R51 (48.19) | 688 | gesetzt |
| 15 | R48 (c) | 7, Tabelle, Zeile (d) | PRÄZISIERT durch R48 (48.16) | 798 | gesetzt |
| 16 | R51 | 7, Tabelle, Zeile (a) | ERGÄNZT (Verweis) durch R51 (48.19) | 801 | gesetzt |
| 17 | R55 | 7, Tabelle, Zeile (d) | ERGÄNZT durch R55 (49.3) | 804 | gesetzt |
| 18 | R21 | 7.1 | ERGÄNZT durch R21 (47.4) | 847 | gesetzt |
| 19 | R23 | 7.1 | PRÄZISIERT durch R23 (47.6) | 850 | gesetzt |
| 20 | R48 (g) | 8.1 | PRÄZISIERT durch R48 (48.16) | 899 | gesetzt |
| 21 | R48 (b) | 9, erster Absatz | PRÄZISIERT durch R48 (48.16) | 911 | gesetzt |
| 22 | R43 | 11.2 | ERGÄNZT durch R43 (48.11) | 1207 | gesetzt |
| 23 | R49 (h) | Abschnitt 11 | ERGÄNZT durch R49 (48.17) | 1226 | gesetzt |
| 24 | B3 | 11.3 | ERGÄNZT durch 50.3 und 50.4 | 1229 | gesetzt |
| 25 | R25 | Abschnitt 12 | ERGÄNZT durch R25 (47.8) | 1297 | gesetzt |
| 26 | R26 | Abschnitt 12 | ERGÄNZT durch R26 (47.9) | 1300 | gesetzt |
| 27 | R49 (d) | Abschnitt 12 | ERGÄNZT durch R49 (48.17) | 1303 | gesetzt |
| 28 | R50 | Abschnitt 12 | ERGÄNZT durch R50 (48.18) | 1306 | gesetzt |
| 29 | R41 | 15.3 (b) | ERGÄNZT durch R41 (48.9) | 1425 | gesetzt |
| 30 | R35 | 15.3 | ERGÄNZT durch R35 (48.3) | 1446 | gesetzt |
| 31 | R54 | 15.4 (a) | BERICHTIGT durch R54 (49.2) | 1474 | gesetzt |
| 32 | R41 B3 | 15.4 | ERGÄNZT durch R41 (48.9) und 50.1 | 1519 | gesetzt |
| 33 | R53 | 15.5 | ERGÄNZT durch R53 (49.1) | 1634 | gesetzt |
| 34 | R23 | 15.6 (c) | PRÄZISIERT durch R23 (47.6) | 1664 | gesetzt |
| 35 | R51 | 15.6 | ERGÄNZT (Verweis) durch R51 (48.19) | 1714 | gesetzt |
| 36 | R21 | 16.4 (b) | PRÄZISIERT durch R21 (47.4) | 2076 | gesetzt |
| 37 | R22 | 16.4 (a) | PRÄZISIERT durch R22 (47.5) | 2079 | gesetzt |
| 38 | R23 | 16.4 (b) | PRÄZISIERT durch R23 (47.6) | 2082 | gesetzt |
| 39 | R37 | 16.4 (c) | PRÄZISIERT durch R37 (48.5) | 2085 | gesetzt |
| 40 | R37 | 16.4 (d) | PRÄZISIERT durch R37 (48.5) | 2088 | gesetzt |
| 41 | R18 | 16.4 (m) | PRÄZISIERT durch R18 (47.1) | 2135 | gesetzt |
| 42 | R18 | 16.4 (h) | PRÄZISIERT durch R18 (47.1) | 2138 | gesetzt |
| 43 | R18 | 16.4 (l) | PRÄZISIERT durch R18 (47.1) | 2141 | gesetzt |
| 44 | R19 | 16.4 (h) | PRÄZISIERT durch R19 (47.2) | 2144 | gesetzt |
| 45 | R19 | 16.4 (j) | PRÄZISIERT durch R19 (47.2) | 2147 | gesetzt |
| 46 | R19 | 16.4 (k) | PRÄZISIERT durch R19 (47.2) | 2150 | gesetzt |
| 47 | R20 | 16.4 (l) | ERGÄNZT durch R20 (47.3) | 2153 | gesetzt |
| 48 | R20 | 16.4 (j) | ERGÄNZT durch R20 (47.3) | 2156 | gesetzt |
| 49 | R21 | 16.4 (i) | PRÄZISIERT durch R21 (47.4) | 2159 | gesetzt |
| 50 | R21 | 16.4 (j) | PRÄZISIERT durch R21 (47.4) | 2162 | gesetzt |
| 51 | R22 | 16.4 (i) | PRÄZISIERT durch R22 (47.5) | 2165 | gesetzt |
| 52 | R24 | 16.4 (h) | ERGÄNZT durch R24 (47.7) und 50.6 | 2168 | gesetzt |
| 53 | R24 | 16.4 (g) | ERGÄNZT durch R24 (47.7) und 50.6 | 2171 | gesetzt |
| 54 | R37 | 16.6 | PRÄZISIERT durch R37 (48.5) | 2317 | gesetzt |
| 55 | R38 | 16.7 (d) | ERGÄNZT durch R38 (48.6) | 2381 | gesetzt |
| 56 | R28 | Abschnitt 18 | ERGÄNZT durch R28 (47.11) | 3059 | gesetzt |
| 57 | R53 | 21.4 | ERGÄNZT durch R53 (49.1) | 3401 | gesetzt |
| 58 | R34 | 22.2 | ERGÄNZT durch R34 (48.2) | 3676 | gesetzt |
| 59 | R36 | 24.2 | PRÄZISIERT durch R36 (48.4) | 4293 | gesetzt |
| 60 | R53 | 25.2 | ERGÄNZT durch R53 (49.1) | 4631 | gesetzt |
| 61 | R53 | 25.3, Ersatztext (Bedingung (i) steht in dessen erster Zeile) | PRÄZISIERT durch R53 (49.1) | 4651 | gesetzt |
| 62 | R31 (d) | 27.3 (im Zitatblock 27.1 bis 27.5) | ERGÄNZT durch R31 (47.14) | 5124 | gesetzt |
| 63 | R32 | Abschnitt 27 | ERGÄNZT durch R32 (47.15) | 5163 | gesetzt |
| 64 | R53 | 28.6 | PRÄZISIERT durch R53 (49.1) | 5295 | gesetzt |
| 65 | R43 | 29.4 | BERICHTIGT durch R43 (48.11) | 5377 | gesetzt |
| 66 | R43 | 34.5 | BERICHTIGT durch R43 (48.11) | 6228 | gesetzt |
| 67 | R37 | 35.1 | PRÄZISIERT durch R37 (48.5) | 6386 | gesetzt |
| 68 | R26 | 35.4 | ERGÄNZT durch R26 (47.9) | 6466 | gesetzt |
| 69 | R49 (e) | 38.2 | ERGÄNZT durch R49 (48.17) | 7331 | gesetzt |
| 70 | R42 | 40.6 | ERGÄNZT durch R42 (48.10) | 8368 | gesetzt |
| 71 | R44 | 40.6 | ERGÄNZT durch R44 (48.12) | 8371 | gesetzt |
| 72 | R47 | 40.6 | PRÄZISIERT durch R47 (48.15) | 8374 | gesetzt |
| 73 | R41 | 41.2, Eintrag B6/B7 | ERGÄNZT durch R41 (48.9) | 8799 | gesetzt |
| 74 | R29 | 42.2, Eintrag E5 (e) | ERGÄNZT durch R29 (47.12) | 9185 | gesetzt |
| 75 | R29 | 44.1, Eintrag 44-6 | ERGÄNZT durch R29 (47.12) | 9959 | gesetzt |
| 76 | R42 | 45.3 | ERGÄNZT durch R42 (48.10) | 10179 | gesetzt |
| 77 | R29 | 45.4, Block R4 | ERGÄNZT durch R29 (47.12) | 10187 | gesetzt |
| 78 | R29 | 45.5, Block R5, Punkt (a) | ERGÄNZT durch R29 (47.12) | 10204 | gesetzt |
| 79 | R33 | 45.5, Block R5, Punkt (b) | BERICHTIGT durch R33 (48.1) | 10207 | gesetzt |
| 80 | R34 | 45.5 | ERGÄNZT durch R34 (48.2) | 10216 | gesetzt |
| 81 | R36 | 45.5 | PRÄZISIERT durch R36 (48.4) | 10219 | gesetzt |
| 82 | R39 | 46.3 | ERGÄNZT durch R39 (48.7) | 10410 | gesetzt |
| 83 | R42 | 46.3 | ERGÄNZT durch R42 (48.10) | 10413 | gesetzt |
| 84 | R25 | 46.5, Block R14 | ERGÄNZT durch R25 (47.8) | 10441 | gesetzt |
| 85 | R26 | 46.5, Block R14 | ERGÄNZT durch R26 (47.9) | 10444 | gesetzt |
| 86 | R27 | 46.5, Block R14 (Bedingung 5 steht in dessen erster Zeile) | ERGÄNZT durch R27 (47.10) | 10447 | gesetzt |
| 87 | R25 | 46.9 | ERGÄNZT durch R25 (47.8) | 10512 | gesetzt |
| 88 | R54 | 48.16 (R48), neu in TB-126 | BERICHTIGT durch R54 (49.2) | 10850 | gesetzt |

**Nicht gesetzt nach Anhang A (wie vorgesehen):**

- **Liste A (Indexzeilen statt Marken, 6):** R42 (10, künftiger Punkt 15), R45 (10, Punkt 10), R48 (k) (10.1),
  R49 (g)/R51 (10, Fortschreibung), R51 (Datenstand-Hash voll: 17.3, 17.9, 18), R30 (10, Punkt 14). Ausgeführt in C3.
- **Liste B (Ziel ohne Ort, 4):** R27 und R30 „Tag-Vorbedingungen“, R28 „Plan-Punkt 6“, R48 (d)/(e).
- **Liste C (ohne Bezugsform):** siehe „Für Fable“.

## Für Fable (nur Verfahrensfragen)

1. **Lesart 50.5** (Zählweise des Vorlaufs: erster definierter Index `BB_PERIOD + L − 1`, nicht Summe der
   Fensterlängen) — vorläufig, bis Fable bestätigt.
2. **Lesart zu R48 (d)** (50.1): wo der Code `mittlere_exposure` nicht bildet, gilt der Registertext.
3. **Reibung R53:** „nicht als Literal“ (R53) gegen „Literal mit Test nach 32.5 (c)“ (30a, „Unsicher“) — 50.7 Nr. 12.
4. **Nebenbefund R28:** `SOLL_DATENSTAND` in `research/registernachtrag_tb48/pruefe_abschnitt17.py:97`, ein weiteres
   Literal des Datenstands ohne eigene Registerprobe (50.1, 50.7 Nr. 6).
5. **Vereinigung der Markenorte für R48–R50** (Anhang A Regel 8): eine Marke je Ort, auch wo Unterpunkt und R51-Liste
   denselben Ort nennen; R51-eigene Orte als „ERGÄNZT (Verweis) durch R51“.
6. **Orte ohne Marke (Liste B und C):** u. a. R21 — die „Prüfung vor dem Tag“ in 16.4 (#### Prüfung vor dem Tag,
   4⁹ statt 3⁹) hat keine eigene Marke; die R21-Marken stehen hinter den Zitatblöcken von 16.4. Weiter: R36/R37/R54/R55
   als Lesarten zu Festlegung 3, 7 (b), 7 (c), 8.1 ohne Bezugsform; R33 zu 43-7; R38 zu 16.11 Zeile 7; R41 zu 41.2 B3;
   R47 zu 5.4 (als Teil von 40.6 gelesen); R48 (h) im ERZEUGT-Block (dort nie eine Marke); R49 (c) zu 40.8 (b), R49 (e)
   zu Abschnitt 6; R31 (a)/(e).
7. **Reibung beim Setzen, aufgefallen:** In **25.3** steht jetzt an Bedingung (i) eine zweite PRÄZISIERT-Marke
   (R53, Z. 4651) hinter der ersten (26.2, Z. 4649). Ob R53 die Fassung aus 26.2 präzisiert oder neben ihr steht, sagt
   keiner der beiden Texte; der Index führt deshalb beide (Tabelle 4, Zeile 25). Sonst keine Reibung zwischen
   Fable-Text und Register beim Setzen.
8. **Befund ohne Bezug zu E-2:** `registerbericht.py --pruefen` meldet **schon vor** dieser Sitzung rc 1 — der
   ERZEUGT-Block in Abschnitt 3 stimmt nicht mehr wörtlich mit dem Erzeuger überein. Der Block war für diese Sitzung
   gesperrt und ist unverändert (bytegleich); der Befund ist nur weitergegeben.

## Nicht getan

- 50.7 (alles dort Offene).
- Der Status von 27c, 29b und 30a im `FABLE_DIALOG_INDEX.md` und die Ablage — macht der steuernde Chat.
- Der Worktree `$TMPDIR/tb123_vorher` (siehe 0b) — Entscheidung beim Betreiber.

## Nebenbemerkungen zum Ablauf

- 0e lief am Commit `0f56aeb` mit uncommitteter BACKLOG-Änderung und neuen Belegdateien im Baum (Register und Code
  unverändert), parallel zu 0f/0g; committet wurde danach in `1e13135`.
- `a5_eintrag_daten.json` wurde zuerst vom Probelauf geschrieben und lag so im Commit `1e13135`; der Echtlauf hat es
  überschrieben (Stand in `db108a6`).
- `rm -rf` war gesperrt; Scratch-Ordner bekamen neue Namen statt gelöscht zu werden.

## In einfacher Sprache

Fable hat in drei Antworten 38 Regeltexte geschrieben. Ein Skript hat sie Zeichen für Zeichen ins Register kopiert
(Abschnitte 47, 48, 49) und an 54 alten Stellen 87 kurze Hinweise gesetzt, dazu einen unter 48.16. Abschnitt 50
enthält, was vorher im Code nachgemessen wurde, und die Notizen zu den Code-Änderungen vom 29. und 30.09. Kein alter
Satz wurde verändert, die Sperrliste (Abschnitt 10) und der erzeugte Zahlenteil sind Byte für Byte gleich geblieben,
und alle Prüfungen sind grün. Danach wurde die Kopie des Registers in vier Teilen neu geschrieben und der Wegweiser
(Index) nachgezogen. Am Code hat sich nichts geändert. Ein alter Arbeitsordner ließ sich nicht ohne Gewalt löschen
und liegt noch da.
