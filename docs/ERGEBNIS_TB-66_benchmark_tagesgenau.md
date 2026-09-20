# ERGEBNIS TB-66 — Der Benchmark wird tagesgenau (Mac-Lauf, 20.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-66_benchmark_tagesgenau.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `1e6fcc7`, Interpreter `trading-env/bin/python3`
= **Python 3.9.6** (pandas 2.3.3, numpy 2.0.2), Kursdateien `data/` = **223**.
Grundlage: Fables Festlegung **VT** vom 20.09.2026
(`docs/projektfuehrung/FABLE_ANTWORT_2026-09-20_benchmarkfenster.md`). Vier
Commits vor diesem Dokument: **`19a1996`** (Code auf VT, Lauf daneben),
**`ec7eff4`** (Messung `dropna()` gegen `fillna(0)`), **`a901e03`** (Register
Abschnitt 23, Backlog-Begriff) und der Abgabe-Commit (dieses Dokument,
Journal-Nachtrag (f), Nachweise 8 und 9). Rohausgaben und das Messskript unter
`docs/belege/TB-66/`. Kein Zweig, kein PR, keine ZIP.

---

## Das Ergebnis zuerst — in sechs Sätzen, jeder mit Fundstelle

1. ⭐ **Registertext 3b (c) ist berichtigt, nichts ist entfernt.** In 16.7 steht
   vor dem alten Wortlaut die Marke *„(c) ERSETZT durch Abschnitt 23"*; der neue
   Abschnitt **23** trägt den berichtigten Satz wörtlich, Fables Festlegung mit
   Gründen, den Ersatztext, die Berichtigungsnotiz und die Begriffsberichtigung.
   `git diff --numstat` des Registers: **313 hinzugefügt, 0 entfernt**.
2. ⚠️ **Der Ersatztext trägt an einer Stelle einen sichtbaren Platzhalter** —
   bei Fables Satz *„Tage, an denen kein Symbol handelbar ist, tragen Rendite 0"*,
   weil `benchmark.py::bh_tagesrenditen` solche Tage mit `.dropna()` ausschliesst
   statt sie mit 0 zu führen. **Gemessen** (Nachweis 4): für den **Drawdown
   macht das keinen Unterschied** — 0 Abweichungen auf 78 Falten × 100 Stufen,
   0 in der `DD_Toleranz` —, für **`handelstage`** einen in vier (wörtliches
   `.fillna(0)`) bzw. fünf (voller Kalender) frühen Krypto-Falten. **Nicht
   entschieden**, wie der Auftrag es verlangt (Register 23.3).
3. ⭐ **`benchmark.py` rechnet seit `19a1996` tagesgenau nach dem Loader des
   Bots.** Der Vierjahresfilter `point_in_time(…, MINDESTTRAINING_JAHRE)` ist
   weg; das Handelbar-Datum je Symbol wird über das TB-56-Werkzeug
   `faltenschranke_messung.loader_lesart` **gelesen** (keine Konstantenkopie),
   jede Kursreihe beginnt an ihrem Handelbar-Tag. **Die vier gesperrten
   Rechenfunktionen sind im Code unverändert**; bei `bh_tagesrenditen` ist nur
   der Docstring berichtigt (*„täglich rebalanciert"* statt *„Buy-and-Hold"*,
   Auftrag 2b). `elliott_wave` ist **dabei**: die Kerzenzahl-Schranke liefert
   das Datum der 17 520. 1h-Kerze, wie in TB-65.
4. ⭐ **Der Lauf daneben:** `benchmark_drawdowns_vt.json`
   (`4549395f…8745d`), **neunmal `status: endgueltig`**, 30 s.
   `benchmark_drawdowns.json` **`a163c498…36d1ee`** und
   `benchmark_drawdowns_neu.json` **`e06812d2…4a062`** vor und nach der Aufgabe
   **gleich** (Nachweis 2). Gegen die VT-Spalte der TB-65-Rechnung: **78 / 78**
   Falten gleich, alle 100 Stufen, `handelstage`, Symbolzahlen.
5. ⚠️⚠️ **Widerspruch zum Auftrag (Abschnitt 4, Gegenprobe): die vier Aktien-Bots
   sind gegenüber TB-61 NICHT unverändert — und das ist kein Fehler des Laufs,
   sondern die Lesart.** Zeichengleich war in TB-65 **VH** (ganze Falte), nicht
   VT. Unter VT ändern sich bei allen vier die Falten **2019, 2025, 2026**
   (92 / 99 / 97 Stufen), weil `ANET`, `PLTR`/`DASH`/`ABNB` und `APP` mitten in
   der Falte handelbar werden und TB-61 sie für die ganze Falte mitzählte.
   `DD_Toleranz` ändert sich dadurch bei `rsi2_mean_reversion` und
   `volatility_breakout` (−12,89 → **−12,77** bei 100 %, **strenger** als TB-61),
   nicht bei `elliott_wave_stocks` und `turtle_soup_stocks` (Nachweis 5).
6. ⭐ **Krypto, gemessen:** `DD_Toleranz` gegenüber TB-61 beim **×2,39 bis
   ×4,98** (je Bot und Stufe) — in der aus TB-65 erwarteten Spanne 2,4 bis 5,0;
   `turtle_soup_crypto` 2018 **−3,60 %** statt −87,92 % (VH) bei 100 %
   Exposure. **Die Toleranz wird nachgiebiger; das ist die Wirkung, nicht der
   Grund** (F17, Register 23 Kopf).

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Leer (Ausgang `1e6fcc7`, 14:19 UTC). Schritt 0 hatte nichts zu committen.

---

## Nachweis 2 — SHA-256 der beiden geschützten Tabellen

| Datei | vor der Aufgabe (`docs/belege/TB-66/nachweis2_sha256_vorher.txt`) | nach dem letzten Schreiben |
|---|---|---|
| `benchmark_drawdowns.json` | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` | **gleich** ✅ |
| `benchmark_drawdowns_neu.json` | `e06812d2f5c26e73aee7265039e6b320b3de253837483c29e164ea07d404a062` | **gleich** ✅ |
| `benchmark_drawdowns_vt.json` *(neu, dieser Lauf)* | — | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` |

---

## Nachweis 3 — Registertext 3b (c): ERSETZT-Marke, neuer Text, Berichtigungsnotiz

| | Fundstelle | Ergebnis |
|---|---|---|
| Alter Wortlaut als ERSETZT markiert | `docs/VORREGISTRIERUNG_neuselektion.md:1944` — *„⚠️ **(c) ERSETZT durch Abschnitt 23 (Berichtigung TB-66, 20.09.2026), 23.3 — der Wortlaut bleibt stehen.**"* — eine **eingefügte** Zeile vor dem alten Absatz; der Absatz selbst (Z. 1946–1949) unverändert | ✅ |
| Neuer Wortlaut | Abschnitt **23.3**, Fables Text wörtlich, mit dem Platzhalter an einer Stelle (Satz 2 oben) und den Fassungen **W** und **C** darunter | ✅ |
| Berichtigungsnotiz | Abschnitt **23.4**: Lesart VT · Grund (Zweck-Satz) · Herkunft (Fable 20.09.2026) · Wirkung in drei Tabellen (Falte 2018, `DD_Toleranz` dreispaltig, W gegen C) | ✅ |
| Null entfernte Zeilen im Register | `git diff --numstat 1e6fcc7..HEAD -- docs/VORREGISTRIERUNG_neuselektion.md` → **`313 0`** | ✅ |

⚠️ **Eine Ergänzung, die der Auftrag nicht nennt und die im Register steht
(23.3, letzter Absatz):** was *„handelbar an diesem Tag"* heisst, kommt aus
Registertext 3b (b) — Schranke erreicht bis zu diesem Tag —, nicht aus einer
neuen Festlegung. Das ist eine Anwendung, kein neuer Registertext; sie steht
dort, damit der Ersatztext ohne Blick in den Code lesbar ist.

---

## Nachweis 4 — die Messung: `.dropna()` gegen `.fillna(0)`

**Werkzeug:** `docs/belege/TB-66/tb66_dropna_gegen_fillna.py` (rein lesend,
importiert `benchmark.py`; Rohausgabe `schritt3_dropna_gegen_fillna.txt`, Zahlen
`schritt3_dropna_gegen_fillna.json`). Drei Fassungen:

| Fassung | Was sie rechnet |
|---|---|
| **W** | `benchmark.py` wie er ist: Tage ohne Rendite fallen weg |
| **C_lit** | wörtlich Fassung C des Auftrags: `.dropna()` → `.fillna(0)`. ⚠️ Der Rahmen kennt nur Tage mit mindestens einem **Kurs**; Tage vor dem ersten Handelbar-Tag eines Bots stehen gar nicht darin |
| **C_voll** | Fables Wortlaut vollständig: Kalender der Falte (alle Tage, an denen irgendein Symbol des Universums einen Schluss hat), fehlende Tage 0 |

**Ergebnis über alle neun Bots und 78 Falten:**

| Grösse | W gegen C_lit | W gegen C_voll |
|---|---|---|
| Drawdown, 78 × 100 Stufen | **0** abweichende Stufen | **0** abweichende Stufen |
| `DD_Toleranz`, 9 × 100 Stufen | **0** | **0** |
| `handelstage` | **4 Falten**, je +1 | **5 Falten** |

**Die Falten mit anderer `handelstage`-Zahl, einzeln:**

| Bot | Falte | W | C_lit | C_voll | DD @ 100 % in allen drei |
|---|---|---:|---:|---:|---:|
| `elliott_wave` | 2018–2019 | 133 | 134 | 730 | −42,14 |
| `t3_supertrend` | 2018 | 0 | 0 | 365 | 0,00 |
| `t3_supertrend` | 2019 | 136 | 137 | 365 | −42,21 |
| `turtle_soup_crypto` | 2018 | 1 | 2 | 365 | −3,60 |
| `volatility_breakout_crypto` | 2018 | 1 | 2 | 365 | −3,60 |

⭐ **Ausdrücklich: Die Differenz ist überall null ausser bei `handelstage`** —
in allen 69 übrigen Falten auch dort, bei den vier Aktien-Bots in jeder Falte.
Der Grund ist kein Zufall: ein Tag mit Rendite 0 lässt `1 + e·r` bei 1 und
bewegt den Kapitalpfad nicht; Peak und Trough bleiben, wo sie sind. Das +1 bei
C_lit ist der erste Kurstag des frühesten Symbols (Kurs, aber noch keine
Rendite).

⚠️ **Zwei Dinge, die der Betreiber bei C mitentscheidet:** (1) `.fillna(0)`
allein setzt Fables Satz nur teilweise um (C_lit ≠ C_voll bei `handelstage`);
(2) Fassung C ändert `bh_tagesrenditen` — **Sperrliste Punkt 6** und Auflage
*„keine der vier gesperrten Rechenfunktionen anfassen"* — und `handelstage` in der
Tabelle, der Lauf wäre zu wiederholen. **Hier wurde nichts davon getan.**

---

## Nachweis 5 — der Dreispalten-Vergleich, mit der Aktien-Gegenprobe

`DD_Toleranz` je Bot bei 25 / 50 / 100 % Exposure
(`docs/belege/TB-66/schritt4_dreispalten_vergleich.txt`):

| Bot | Sel.-Falten gesperrt / TB-61 / TB-66 | gesperrt (TB-30a) | TB-61 (`_neu.json`) | **TB-66 (VT)** | Faktor TB-66 / TB-61 @ 25 / 50 / 100 % |
|---|---|---|---|---|---|
| `elliott_wave` | 0 / 4 / 4 | *Platzhalter* | −6,07 / −11,89 / −22,42 | **−16,42 / −31,21 / −55,91** | ×2,71 / ×2,62 / ×2,49 |
| `t3_supertrend` | 0 / 8 / 8 | *Platzhalter* | −3,24 / −6,32 / −12,01 | **−12,89 / −24,73 / −45,16** | ×3,98 / ×3,91 / ×3,76 |
| `rsi2_crypto` | 0 / 7 / 7 | *Platzhalter* | −6,48 / −12,64 / −24,02 | **−17,26 / −32,59 / −57,29** | ×2,66 / ×2,58 / ×2,39 |
| `turtle_soup_crypto` | 0 / 8 / 8 | *Platzhalter* | −3,24 / −6,32 / −12,01 | **−16,13 / −30,52 / −54,05** | ×4,98 / ×4,83 / ×4,50 |
| `volatility_breakout_crypto` | 0 / 8 / 8 | *Platzhalter* | −3,24 / −6,32 / −12,01 | **−16,13 / −30,52 / −54,05** | ×4,98 / ×4,83 / ×4,50 |
| `elliott_wave_stocks` | 7 / 9 / 9 | −2,18 / −4,33 / −8,55 | −2,18 / −4,33 / −8,55 | **−2,18 / −4,33 / −8,55** | ×1,00 |
| `rsi2_mean_reversion` | 7 / 8 / 8 | −2,18 / −4,33 / −8,55 | −3,35 / −6,61 / −12,89 | **−3,32 / −6,55 / −12,77** | ×0,99 |
| `turtle_soup_stocks` | 7 / 9 / 9 | −2,18 / −4,33 / −8,55 | −2,18 / −4,33 / −8,55 | **−2,18 / −4,33 / −8,55** | ×1,00 |
| `volatility_breakout` | 7 / 8 / 8 | −2,18 / −4,33 / −8,55 | −3,35 / −6,61 / −12,89 | **−3,32 / −6,55 / −12,77** | ×0,99 |

**Krypto:** Faktor **×2,39 bis ×4,98** — die Erwartung „2,4- bis 5,0-fach" aus
TB-65 trifft als Spanne über Bots und Stufen; bei 100 % allein ist es ×2,39 bis
×4,50 (das 5,0-fache war dort der VH-Wert von `turtle_soup_crypto`). `t3_supertrend`
ist **mit** seiner leeren Falte 2018 gerechnet (Register 21.3 (b) steht in keinem
Code, TB-61 Befund 2); ohne sie läge der Median bei −13,90 / −26,57 / −48,10
(TB-65, Tabelle C1).

### Die Gegenprobe der vier Aktien-Bots — und warum sie anders ausgeht als der Auftrag erwartet

Der Auftrag: *„Für die vier Aktien-Bots darf sich gegenüber TB-61 nichts ändern —
dort waren V0 und die Loader-Fassung auf allen 100 Stufen und in allen 40 Falten
zeichengleich. Weicht dort etwas ab, ist das ein Befund und der Lauf ist nicht
fertig."*

⚠️ **Es weicht etwas ab, und der Lauf ist trotzdem fertig — weil die
Zeichengleichheit aus TB-65 für VH galt, nicht für VT.** TB-65, Tabelle C1, weist
in der Spalte **VT** bereits −3,32 / −6,55 / −12,77 für `rsi2_mean_reversion` und
`volatility_breakout` aus; der Auftrag hat die VH-Aussage auf VT übertragen.
Der Mechanismus, gemessen (`docs/belege/TB-66/schritt4_aktien_gegenprobe.txt`,
für `volatility_breakout`; die anderen drei teilen Universum, Kursreihen und
Schranke 1 825 und zeigen dieselben Faltenwerte):

| Falte | Eintritte in der Falte (Symbol: Handelbar-Tag) | Tage mit abweichender Tagesrendite | DD @ 100 % TB-61 → TB-66 | Peak → Trough (VT) |
|---|---|---:|---|---|
| 2018 | `ABBV` 2018-01-01 (Faltenbeginn) | 1 | −18,69 → −18,69 | 09-21 → 12-24 |
| **2019** | `ANET` 2019-06-05 | 107 | **−7,30 → −7,23** | 05-03 → 05-31 |
| 2021 | `DELL` 08-16, `HWM` 10-31 | 210 | −4,74 → −4,74 | 11-16 → 12-01 |
| 2023 | `VRT` 08-01 | 145 | −8,55 → −8,55 | 08-01 → 10-27 |
| 2024 | `UBER` 05-08, `CRWD` 06-10 | 111 | −6,86 → −6,86 | 07-16 → 08-05 |
| **2025** | `PLTR` 09-29, `DASH` 12-08, `ABNB` 12-09 | 235 | **−17,23 → −16,99** | 02-19 → 04-08 |
| **2026** | `APP` 04-14, `HOOD` 07-28 | 142 | **−6,40 → −6,31** | 02-27 → 03-30 |

⭐ **Das Muster:** TB-61 (Kursdaten ≥ 4 Jahre vor dem 1. Januar) nahm ein Symbol,
dessen Loader-Schranke erst mitten im Jahr fällt, für das **ganze** Jahr. Der
Drawdown ändert sich genau dort, wo die Peak-Trough-Episode **vor** dem Eintritt
liegt (2019, 2025, 2026): dort enthielt TB-61 das Symbol während der Episode,
VT nicht. Liegt die Episode **nach** allen Eintritten (2021, 2023, 2024), sind
beide Pfade dort identisch. **Alle 100 Stufen je Falte** stehen in
`schritt4_dreispalten_vergleich.txt`: 2019 → 92, 2025 → 99, 2026 → 97 abweichende
Stufen bei allen vier Bots; `DD_Toleranz` 98 Stufen bei den beiden Acht-Falten-Bots
(Median = Mittel aus 2019 und 2023), 0 bei den Neun-Falten-Bots (Median = 2023).

⚠️ **Für die Sperrlisten-Änderung heisst das:** Fables Satz *„Für die vier
Aktien-Bots ändert sich nichts — die Sperrlisten-Änderung kann dort sofort
vollzogen werden"* (Antwort, „Was daraus folgt") gilt gegenüber **TB-61 nicht
mehr wörtlich**: zwei Aktien-Bots bekommen unter VT eine um 0,03 / 0,06 / 0,12
Punkte **strengere** Toleranz als in TB-61 — und weiterhin eine nachgiebigere als
in der gesperrten Tabelle (21.6). **Benannt, nicht entschieden.**

---

## Nachweis 6 — `status` je Bot in `benchmark_drawdowns_vt.json`

**Neunmal `endgueltig`** — `elliott_wave`, `t3_supertrend`, `rsi2_crypto`,
`turtle_soup_crypto`, `volatility_breakout_crypto`, `elliott_wave_stocks`,
`rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`
(`schritt4_dreispalten_vergleich.txt`, Zeile *„Anzahl 'endgueltig': 9 von 9"*).

---

## Nachweis 7 — die Begriffsstellen „Amendment", einzeln

**Fable:** *„Vor dem Tag ist es eine Berichtigung des Registers und ein Bug-Fix
am Auswerter; ‚Amendment' gehört zur Sperrliste des Codes, nicht zum Register."*

**Gemessen** (Stand `ec7eff4`): Register **24** Vorkommen auf 24 Zeilen, Backlog
**11** Vorkommen auf 10 Zeilen. Davon sagen die meisten *„kein Amendment"* oder
*„nach dem Tag Amendment"* — sie sind richtig und bleiben. ⚠️ **Der Auftrag
sagt „vor allem 21.9 und `T56b.3`" und zugleich „für `benchmark_drawdowns.json`
(Sperrliste Punkt 4) bleibt der Begriff richtig" — 21.9 und `T56b.3` sprechen
aber genau von dieser Tabelle.** Aufgelöst so: Der Begriff bleibt richtig für
eine Änderung **nach dem Tag** (10.1: *„der Lauf beginnt von vorn"*); der
bevorstehende Vorgang **vor** dem Tag ist nach Fable eine Berichtigung — und
genau so nennen ihn 21.6/21.9 und `T56b.3` nicht. Berichtigt sind deshalb die
Stellen, die den Vorgang vor dem Tag „Amendment" nennen.

**Im Register (append-only): die alten Zeilen bleiben; 23.6 stellt je Stelle den
Satz, wie er dasteht, neben den Satz, wie er zu lesen ist:**

| Fundstelle | vorher (steht weiter da) | nachher (23.6) |
|---|---|---|
| 21.6, Z. 2947–2949 | *„… und eine Änderung dort ist ein **Amendment** nach 10.1."* | *„… ist **vor dem Tag eine Berichtigung** (Register) samt **Bug-Fix am Auswerter**, **nach dem Tag ein Amendment** nach 10.1."* |
| 21.6, Z. 2991 (Weg A) | *„**Amendment vollziehen**: die neue Tabelle wird die registrierte, …"* | *„**Berichtigung vollziehen**: …"* — der Weg unverändert |
| 21.9, Z. 3071–3073 | *„Das Amendment wird **einmal** vollzogen, **nach** der Berechnung der Krypto-Falten (TB-31), und umfasst dann **alle neun Bots**."* | *„Die **Berichtigung der Benchmark-Tabelle** (Sperrliste Punkt 4) wird **einmal** vollzogen, …"* |
| 21.9, Z. 3081 | *„Ein Amendment jetzt bewegte eine gesperrte Zahl, …"* | *„Eine Berichtigung jetzt bewegte …"* |
| 21.9, Z. 3088 | *„Er wird mit demselben Amendment geschlossen"* | *„Er wird mit derselben Berichtigung geschlossen"* |

**Im Backlog (`docs/projektfuehrung/BACKLOG.md`, Regel 9: Wortlaut geändert,
`numstat 2 2`):**

| Zeile | vorher | nachher |
|---|---|---|
| 271, `T56b.3` | *„**BETREIBERENTSCHEIDUNG 19.09.2026: Das Amendment zu Sperrliste Punkt 4 wird EINMAL vollzogen, nach TB-61, für alle neun Bots.**"* | *„**BETREIBERENTSCHEIDUNG 19.09.2026: Die Berichtigung der Benchmark-Tabelle (Sperrliste Punkt 4) wird EINMAL vollzogen, nach TB-61, für alle neun Bots.**"* |
| 271, `T56b.3` | *„… ein Amendment jetzt bewegte die gesperrte Zahl zweimal."* | *„… eine Berichtigung jetzt bewegte die gesperrte Zahl zweimal. (Begriff nach Fable 20.09.2026, Register 23.6 … Bis TB-66 stand hier zweimal „Amendment".)"* |
| 308, Schlussblock Abschnitt 2 | *„**Das Amendment selbst braucht danach eine eigene Betreiberfreigabe.**"* | *„**Die Berichtigung der Tabelle selbst braucht danach eine eigene Betreiberfreigabe** (bis TB-66: „Das Amendment selbst …"; Begriff nach Register 23.6). ⚠️ **Seit TB-66 (20.09.2026) ist TB-61 überholt:** die Tabelle nach Lesart VT liegt als `benchmark_drawdowns_vt.json` daneben (Register 23); vor dem Vollzug steht die Entscheidung W/C aus Register 23.3."* |

Unverändert im Backlog (richtig): Z. 58 *„Danach wäre es ein Amendment"*, `V3`,
`Q1`, `T45.7`, `K6`, `F12`, `V5h`, `T46.1c` — alle „kein Amendment" oder „nach dem
Tag/Lauf".

---

## Nachweis 8 — `test_vorregistrierung.py`, Ergebnis je Teil

**Im Repo** (`trading-env/bin/python3 research/vorregistrierung/test_vorregistrierung.py`,
Rohausgabe `docs/belege/TB-66/nachweis8_test_vorregistrierung.txt`):

| Teil | Ergebnis |
|---|---|
| **A** | **Abbruch** mit `KeyError: '2017'` in `auswertung.py:237` (`zulaessigkeit`) — der Test liest die **gesperrte** Tabelle (`test_vorregistrierung.py:82`), die die Falte 2017 nicht kennt. ⚠️ **Erwartet und kein Befund** (Auftrag Nachweis 8; Register 21.9: *„offen durch eigene Änderung — blockierend für den Tag"*); zeichengleich mit TB-61 Nachweis 7 |
| B–H | nicht erreicht — das Skript bricht beim ersten Fehler ab |

**Zusätzlich, nachrichtlich, in einer Wegwerf-Kopie** `research/_tb66_kopie/`
(zwei Ebenen unter der Repo-Wurzel, wie TB-61/TB-65; **die VT-Tabelle an der
Stelle von `benchmark_drawdowns.json` der Kopie**; Kopie danach entfernt;
Rohausgabe `nachweis8_test_in_kopie_mit_vt_tabelle.txt`, Laufzeit ~15 min):

| Teil | Ergebnis |
|---|---|
| A, B, C, D, E, F | alle Prüfungen bestanden |
| **G** | **G6 rot**: *„elliott_wave — 2020 und 2022 sind Testfalten, keine Trainingsjahre — ['2018-2019', '2020-2021', '2022-2023', '2024-2025', '2026-2027']"* — die Probe erwartet Einjahresnamen, `elliott_wave` hat Doppeljahre (TB-61 Befund, unverändert) |
| **H** | **H3 rot**: *„ohne die gesetzte Null aendert sich die Statistik — 'Netto-Sharpe (Med.) 0.1000' / 'Netto-Sharpe (Med.) 0.1000'"* — Probe auf 7 Falten gebaut (TB-61 Befund, unverändert) |
| **Summe** | **163 bestanden, 2 gescheitert** — **dieselben zwei wie in TB-61 mit der `_neu`-Tabelle** (`docs/belege/TB-61/nachweis7_test_in_kopie_mit_neuer_tabelle.txt`). ⭐ Die VT-Tabelle bricht also keine weitere Prüfung; **Teil D** (Drawdown-Bedingung in beide Richtungen, ruhige Falte 2021 gegen Krisenfalte 2020 bei `turtle_soup_stocks`) **besteht mit den VT-Zahlen** |

⚠️ Beide roten Proben sind aus TB-61 bekannt und **nicht Gegenstand dieses
Auftrags** (Abschnitt 8: *„Die zwei roten Tests aus TB-61 reparieren"* — nein).

---

## Nachweis 9 — `git diff --numstat 1e6fcc7..HEAD`

`docs/belege/TB-66/nachweis9_numstat.txt`. **Nichts ausserhalb
`research/vorregistrierung/` und `docs/`**; die Wegwerf-Kopie
`research/_tb66_kopie/` ist entfernt (Nachweis 8) und war nie im Index.

---

## Widerspruch zum Auftrag — drei Stellen

| | Auftrag | Gemessen |
|---|---|---|
| **1** | Abschnitt 4: *„Für die vier Aktien-Bots darf sich gegenüber TB-61 nichts ändern"* | Ändert sich in 2019/2025/2026 bei allen vier, in der `DD_Toleranz` bei zweien — **Folge von VT selbst**, in TB-65 Spalte VT bereits ausgewiesen (Nachweis 5) |
| **2** | Abschnitt 5: *„vor allem 21.9 und `T56b.3`"* **und** *„für `benchmark_drawdowns.json` bleibt der Begriff richtig"* | Beide Stellen meinen dieselbe Tabelle; aufgelöst über den Zeitbezug vor/nach dem Tag (Nachweis 7) |
| **3** | Abschnitt 1, Fassung C: *„`.dropna()` durch `.fillna(0)` ersetzen"* | setzt Fables Satz nur teilweise um (C_lit ≠ C_voll bei `handelstage`) und änderte `bh_tagesrenditen` (Sperrliste 6) — als Vorlage gemessen, nicht getan (Nachweis 4) |

---

## Beobachtungen am Rande — NICHT ausgeführt, hier nur benannt

| | Beobachtung | Warum liegen gelassen |
|---|---|---|
| ⚠️ | `registerbericht.py:178` liest `symbole_point_in_time` aus der **gesperrten** Datei — läuft heute unverändert; **beim Vollzug der Sperrlisten-Änderung** braucht es den neuen Schlüssel `symbole_handelbar_in_falte` und eine andere Spaltenüberschrift als *„Titel (point-in-time)"* | Vollzug ist eine eigene Freigabe (Auftrag Abschnitt 8) |
| ⚠️ | `research/exposure_messung/exposure_kern.py::bh_tagesrenditen` trägt denselben Docstring *„Gleichgewichteter Buy-and-Hold"* — `benchmark.py` nennt ihn ausdrücklich als zeichengleiche Zwillingsrechnung | ausserhalb `research/vorregistrierung/` |
| ⚠️ | `registerdaten.MINDESTTRAINING_JAHRE` bleibt: `faltenplan.py:208` schreibt sie in jeden Plan, `registerbericht.py:140` druckt *„Mindesttraining vor der ersten Falte: 4 Jahre"*, `benchmark.py` selbst braucht sie nicht mehr | TB-65 Beobachtung 2; `T56b.6`-Klasse |
| | `research/krypto_historie/faltenplan.py:65` (`MINDESTTRAINING_JAHRE = 4`, `K4f`): **gemessen, dass sie nichts beeinflusst, was hier gerechnet wird** — kein Import aus `research/vorregistrierung/`, `faltenplan_neun.py` oder `faltenschranke_messung.py`; nur `test_faltenplan_neun.py:78` nennt den Pfad als TB-31-Werkzeug | `T56b.6`, Auftrag 2c |
| | Vorab gemessen, damit „gelesen über das TB-56-Werkzeug" auch die Loader-Zählung trifft: **keine** 1h-Datei enthält unvollständige Kerzen, **keine** 1d/4h-Datei beginnt mit einer (eine unvollständige Zeile insgesamt); Kerzenzahl und erster Kurstag des Werkzeugs sind damit die des Loaders nach `entferne_unvollstaendige` | Voraussetzung, keine Änderung |
| | `pandas` `FutureWarning` (`pct_change`, `fill_method='pad'`): 8 Zeilen in `schritt2_benchmark_lauf_stderr.txt`, Rechenweg unverändert (wie TB-56/61/65) | Sperrliste 6 |
| | Das Register nennt den Benchmark in 4.2 und Sperrliste Punkt 6 weiter *„point-in-time"* — richtig, tagesgenau ist die feinere Auflösung desselben Prinzips; 23.7 hält das fest | kein Registertext geändert, der nicht im Auftrag steht |
| | `AKTUELLER_AUFTRAG.md` führt die Zeile TB-66 weiter; die Tabelle pflegt der Betreiber (*„Bei jedem neuen Auftrag wird nur diese Tabelle gepflegt"*) | nicht angefasst |

---

## Was diese Aufgabe ausdrücklich NICHT getan hat

| | |
|---|---|
| ⛔ | **Die Sperrlisten-Änderung vollzogen.** `benchmark_drawdowns.json` ist byteweise dieselbe Datei; die VT-Tabelle liegt daneben. Vor dem Vollzug: Betreiberentscheidung **W oder C** (Register 23.3) — bei C Lauf wiederholen — und die Freigabe aus 21.9 |
| ⛔ | **Den Tag gesetzt**, **`T56b.6` erledigt**, **G6/H3 repariert**, **`VORREGISTRIERUNG_S-E1_nulltest.md` geändert** |
| ⛔ | **Die Formulierungsfrage entschieden** — gemessen und vorgelegt |
| ⛔ | **Eine der vier gesperrten Rechenfunktionen im Code geändert** — nur der Docstring von `bh_tagesrenditen` |

---

## In einfacher Sprache

**Was gemacht wurde:** Fable hat festgelegt, dass der Vergleichskorb eines Bots
jeden Tag nur die Kurse enthält, die der Bot an diesem Tag auch laden darf.
Das steht jetzt im Regelwerk — der alte Satz bleibt stehen und ist als ersetzt
markiert — und das Programm rechnet so. Die gesperrte Tabelle ist unberührt, die
neue liegt daneben.

**Was herauskam:** Für die fünf Krypto-Bots werden die Verlustgrenzen deutlich
nachgiebiger als in der Rechnung vom Vormittag (zwei- bis fünffach), weil dort
in den frühen Jahren ein leerer Korb den Mittelwert nach oben gezogen hatte. Bei
den Aktien-Bots ändert sich wenig — aber nicht nichts: drei Jahre rechnen sich
anders, weil in ihnen ein Wert erst mitten im Jahr dazukommt, und zwei Bots
bekommen eine um ein Zehntelprozent strengere Grenze. Der Auftrag hatte „nichts"
erwartet; das war die andere Lesart.

**Was offen bleibt:** Ein einziger Satz. Fable schreibt, Tage ohne handelbaren
Kurs zählen mit null Rendite; das Programm lässt sie weg. Gemessen: Für alle
Verlustzahlen ist das gleichwertig, nur die Zahl der Handelstage ändert sich in
fünf frühen Krypto-Jahren. Im Regeltext steht dort ein sichtbarer Platzhalter,
bis der Betreiber wählt. Danach kann die neue Tabelle die gesperrte ablösen —
mit eigener Freigabe.
