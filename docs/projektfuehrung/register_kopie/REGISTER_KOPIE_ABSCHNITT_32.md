# REGISTER-KOPIE Abschnitt 32 (von 0–53) — Register-Z. 5709–5919 — Commit ee43f5f1339549238c0da023db7c9f324b26d28e — 2026-10-04 — Original sha256 9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff — KOPIE, nicht das Register

## 32. Bedingung (i) rechnet gegen den Horizontbeginn aus 28.4 — Umstellung des Faltenplans von der Datenuhr auf das absolute Datum (TB-80, 21.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben.**
Kein neuer Registertext: 25.3 (Konjunktion), 26.2 (Horizont als absolutes
Datum je Bot) und 28.4 (die vier Daten) bleiben zeichengleich stehen und
werden hier **umgesetzt**, nicht geändert. Was dieser Abschnitt trägt, sind
ein Befund, drei Tatsachennotizen und eine Entscheidungsvorlage.

**Anlass:** `docs/auftraege/MAC_TB-80_bedingung_i_auf_asof.md`. Betreiberfreigabe
vom 21.09.2026, 21:47 Ortszeit, für **genau eine** Datei:
`research/vorregistrierung/faltenplan.py`. Ergebnis
`docs/ERGEBNIS_TB-80_bedingung_i_auf_asof.md`, Belege `docs/belege/TB-80/`.

⭐⭐ **Die Regel stand vor der Messung.** Gemessen an der Git-Historie:
Abschnitt 26.2 ist mit Commit `729443c` am 21.09.2026, **17:13** Ortszeit
eingetragen worden (der Auftrag nennt 19:19; der Commit liegt früher), 28.4
mit Commit `003f894` um **19:20** Ortszeit; die Messung in 32.2 lief am
21.09.2026 ab 20:17 UTC (**22:17** Ortszeit). **Was herauskommt, ist keine
Wahl** — Bauart 24.3.

---

### 32.1 Der Befund — Bedingung (i) rechnete gegen die Datenuhr, 26.2 verlangt das absolute Datum

**Gemessen 21.09.2026 am Stand `41db199` (vor Schritt 1), Fundstellen:**

| | Fundstelle | Wortlaut / Wert |
|---|---|---|
| Was das Register verlangt | **26.2**, Z. 4323–4329 (Registertext 4a, Präzisierung) | *„Der Datenhorizont eines Bots ist ein absolutes Datum je Bot: Horizontbeginn = `asof` (5a) minus `RECENT_YEARS_ONLY` des Bots; Bots ohne diese Konstante haben keinen Horizont (Krypto). […] Es gilt für alle Symbole des Bots gleich"* |
| Der Wert | **28.4**, Z. 4684–4687 (gültige Fassung der Tatsachennotiz zu 4d) | `elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`: **2016-09-19**; die fünf Krypto-Bots: **kein Horizont** (Z. 4679–4683) |
| Woher der Wert kommt | **28.3** | `asof` = **2026-09-19** (`zeitpunkt_utc` des Snapshots `63e4b6c8…`, Abschnitt 18) |
| Was der Code tat | `research/vorregistrierung/faltenplan.py::erste_falte_4a`, Z. 175 (Stand `41db199`) | `beginn = fn.symbolbeginn(bot, fn.fensteranker(eig["markt"]))` |
| Was `fensteranker` ist | `research/faltenplan_neun/faltenplan_neun.py:271–295` | zehn Jahre vor dem **spätesten letzten Kurstag des Marktes** — die **Datenuhr**; gemessen am 21.09.2026: `aktien` **2016-09-01**, `krypto` `None` (`docs/belege/TB-80/schritt0_ausgangsstand.txt`) |
| Der Abstand | — | **18 Tage** (2016-09-01 → 2016-09-19). 28.4, „Abgegrenzt": *„Die Ähnlichkeit der beiden Daten (2016-09-01 gegen 2016-09-19) ist Zufall des Kalenders"* |

**Was geändert wurde (Commit `76c20ec`, Diff vollständig im Ergebnisdokument):**
`erste_falte_4a()` nimmt den Anker aus `HORIZONTBEGINN = {"aktien":
date(2016, 9, 19), "krypto": None}` — ein **benanntes Literal je Markt mit der
Registerfundstelle (26.2 / 28.4) im Kommentar**, wie der Auftrag es vorgibt:
**nicht** `asof` minus Konstante gerechnet, **nicht** aus den vier
`multi_symbol_optimise.py` gelesen (Sperrliste; `T56b.6`, keine
Konstantenkopie). Neu daneben `horizontbeginn(bot)` und
`erste_falte_4a_messung(bot)`; der Plan trägt je Bot die zwei neuen Felder
`horizontbeginn` und `erste_falte_4a_warm_ab` (das früheste Warm-Datum, auf
Tagesebene — damit im Plan steht, gegen welches Datum (i) gerechnet wurde).
**Unverändert:** Bedingung (ii) (`erste_falte_trockenlauf.erste_falte_nach_3b`),
die Konjunktion in `erste_falte()` (25.3), die Signaturen von `erste_falte_4a`
und `erste_falte`. **`fensteranker` bleibt bestehen** — gemessen, wer ihn
sonst benutzt: `faltenplan_neun.py::plan_fuer_bot` (Z. 415, 445),
`embargo_neun.py:176`, `faltenschranke_messung.py:220, 236`.

---

### 32.2 Tatsachennotiz — die Wirkung je Bot

**Gemessen 21.09.2026, `trading-env/bin/python3` (Python 3.9.6), vorher am
Stand `41db199` (`docs/belege/TB-80/schritt0_ausgangsstand.txt`,
`schritt0_warm_ab.txt`), nachher am Stand `76c20ec`
(`docs/belege/TB-80/schritt2_wirkung.txt`). Beides aus dem Code gerechnet,
nicht aus einer Datei gelesen.**

| Bot | Markt | `erste_falte_4a` vorher | nachher | `erste_falte` vorher | nachher | Zahl der Selektionsfalten vorher → nachher |
|---|---|---:|---:|---:|---:|---|
| `elliott_wave` | krypto | 2018 | 2018 | 2018 | 2018 | 4 → 4 |
| `t3_supertrend` | krypto | 2018 | 2018 | 2019 | 2019 | 7 → 7 |
| `rsi2_crypto` | krypto | 2019 | 2019 | 2019 | 2019 | 7 → 7 |
| `turtle_soup_crypto` | krypto | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `volatility_breakout_crypto` | krypto | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `elliott_wave_stocks` | aktien | 2017 | 2017 | 2017 | 2017 | 9 → 9 |
| `rsi2_mean_reversion` | aktien | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `turtle_soup_stocks` | aktien | 2017 | 2017 | 2017 | 2017 | 9 → 9 |
| `volatility_breakout` | aktien | 2018 | 2018 | 2018 | 2018 | 8 → 8 |

**Bots mit Änderung an `erste_falte_4a`, `erste_falte` oder Selektionsfalten:
0. Geänderte, neue oder entfallene Falten (Grenzen, Rolle, Training, Embargo):
0.** Die neun Zahlen stimmen mit 21.4 überein.

**Dieselbe Messung eine Ebene tiefer** — das früheste Datum, an dem ein Symbol
des Bots ab dem Anker warm ist (die Grösse hinter `erste_falte_4a`):

| Bot | Anker vorher (Datenuhr) | Horizontbeginn nachher | warm ab vorher | warm ab nachher | Verschiebung |
|---|---|---|---|---|---:|
| fünf Krypto-Bots | `None` | `None` | 2017-08-17 / 2017-08-17 / 2018-01-14 / 2017-09-16 / 2017-12-22 | unverändert | **+0 Tage** |
| `elliott_wave_stocks` | 2016-09-01 | 2016-09-19 | 2016-09-01 | 2016-09-19 | +18 Tage |
| `rsi2_mean_reversion` | 2016-09-01 | 2016-09-19 | 2017-06-20 | 2017-07-06 | +16 Tage |
| `turtle_soup_stocks` | 2016-09-01 | 2016-09-19 | 2016-10-14 | 2016-10-31 | +17 Tage |
| `volatility_breakout` | 2016-09-01 | 2016-09-19 | 2017-03-07 | 2017-03-22 | +15 Tage |

⭐ **Die fünf Krypto-Bots haben keinen Horizont (26.2), und bei ihnen ändert
sich nichts** — weder ein Jahr noch ein Tag. Das ist der Nachweis, dass die
Umstellung nur (i) trifft (Abbruchkriterium 4 des Auftrags, nicht
eingetreten). Ihre Einträge im neuen Plan unterscheiden sich vom
Ausgangsstand ausschliesslich im Text `erste_falte_quelle` und in den zwei
neuen Feldern.

⛔ **Nicht gemessen und nicht zu messen:** wie sich die Umstellung auf eine
Kennzahl eines Parametersatzes auswirkt (27.1, vor dem Tag).

---

### 32.3 Tatsachennotiz — der neue Plan daneben, die gesperrten Dateien unverändert

| Datei | SHA-256 | Stand |
|---|---|---|
| **`research/vorregistrierung/ergebnisse/faltenplan_tb80.json`** (neu, Commit `cadb968`) | **`2dd28291497e1233f6854651688f77d5d0a268370ef1ce423a42820917316794`** | Plan nach der Umstellung; zwei Läufe byteweise gleich; geschrieben vom Belegskript `docs/belege/TB-80/schritt2_faltenplan_tb80.py`, **nicht** von `faltenplan.py::main` (das schreibt immer nach `faltenplan.json`) |
| `research/vorregistrierung/ergebnisse/faltenplan.json` (Sperrliste Punkt 2) | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` | **byteweise unverändert**, vorher und nachher gemessen |
| `research/vorregistrierung/ergebnisse/faltenplan_tb72.json` | `19e8cbca874d6e7455f2f3bc0723def9ea058d0b314fa1772e04cd64ff1c9d24` | **byteweise unverändert**; der Speicherstand vor TB-80 (`docs/belege/TB-80/faltenplan_stand_vor_tb80.json`, aus dem Code gerechnet) hat **denselben Hash** — der Plan von TB-72 war am Ausgang reproduzierbar |
| `research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` (Sperrliste) | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` | unverändert |
| `research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json` (Sperrliste) | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` | unverändert |

⚠️ **`faltenplan_tb80.json` ist kein Sperrlistenpunkt und kein Registertext.**
Was der Plan nach 4a ist und wie er ins Register kommt, regelt Abschnitt 30
(genau eine Abbild-Datei, als neuer Sperrlistenpunkt, Betreiber). Diese Datei
liegt daneben, wie `faltenplan_tb72.json` daneben liegt.

---

### 32.4 Die Mutationsprobe — in beide Richtungen

**`docs/belege/TB-80/schritt3_mutationsprobe.py` / `.txt`, 21.09.2026, 20:25 UTC,
im Speicher (`HORIZONTBEGINN` ersetzt, `faltenplan.py` unverändert, nichts
committet), 49/49 Proben, `rc 0`.**

| Richtung | Eingriff | Ergebnis |
|---|---|---|
| **1 — die Datenuhr wieder eingesetzt** | `HORIZONTBEGINN = {markt: fn.fensteranker(markt)}` = `aktien 2016-09-01`, `krypto None` | Der Plan liefert **Bot für Bot den alten Stand** aus Schritt 0: `erste_falte_4a`, `erste_falte`, Selektionsfalten, alle Falten (Grenzen/Rolle/Training/Embargo) **und** die Warm-Daten auf Tagesebene (9 × 3 Proben). Gegen den neuen Plan weichen **alle vier Aktien-Bots** in `horizontbeginn` und `erste_falte_4a_warm_ab` ab; die fünf Krypto-Bots sind zeichengleich |
| ⚠️ **Wo Richtung 1 nicht beisst** | — | **Auf Jahresebene sind alter und neuer Stand gleich** (32.2: 0 Bots mit Änderung). Dort kann diese Richtung nichts verwerfen. **Sie beisst auf Tagesebene** — deshalb trägt der Plan seit TB-80 das Warm-Datum, und deshalb wurde es in Schritt 0 vor der Änderung gemessen |
| **2 — der Horizontbeginn ein Jahr nach hinten** | `aktien 2017-09-19` | **Alle vier Aktien-Bots bewegen sich um ein Jahr**: `erste_falte_4a` und `erste_falte` `elliott_wave_stocks` 2017 → 2018, `rsi2_mean_reversion` 2018 → 2019, `turtle_soup_stocks` 2017 → 2018, `volatility_breakout` 2018 → 2019; die Konjunktion hält (`erste_falte ≥ erste_falte_4a`, `H` in der ersten Kandidatenfalte 136/137); Krypto unverändert |
| Original wiederhergestellt | `{"aktien": 2016-09-19, "krypto": None}` | `erste_falte_4a_messung` je Bot = `faltenplan_tb80.json` (9/9) |

**Der Test** `research/faltenplan_neun/test_horizontbeginn.py` (Commit
`cb7f495`, 61/61 auf `trading-env/bin/python3` 3.9.6) prüft dauerhaft: die vier Aktien-Bots gegen 2016-09-19 und nicht
gegen die Datenuhr; die fünf Krypto-Bots gegen den Ausgangsstand aus Schritt 0;
die Konjunktion; und **das Literal gegen den Registertext 28.4** — der Test
liest die Tabelle in 28.4 und vergleicht sie mit `faltenplan.horizontbeginn(bot)`.
Gegenprobe: mit dem Literal auf 2016-09-01 wird er rot (15 Prüfungen,
`docs/belege/TB-80/schritt4_gegenprobe_test_rot.txt`).

---

### 32.5 ⭐ Entscheidungsvorlage, nicht vollzogen — wo der Horizontbeginn dauerhaft leben soll

**Heute (Zwischenstand, so benannt):** ein Literal je Markt in
`research/vorregistrierung/faltenplan.py` (`HORIZONTBEGINN`), mit der
Registerfundstelle im Kommentar und einem Test, der es gegen den Registertext
28.4 hält. Register 26.6 (letzte Zeile, „Entscheidungsvorlage, nicht
vollzogen") und 28.7 führen die Frage *„`RECENT_YEARS_ONLY` als registrierte
Grösse"* seit TB-77 offen; sie ist mit dieser Aufgabe nicht entschieden.

| Möglichkeit | Was es ist | Preis |
|---|---|---|
| **(a) `registerdaten.py` als registrierte Grösse** | `HORIZONTBEGINN` (oder `asof` und `RECENT_YEARS_ONLY` getrennt, mit dem Datum als Ableitung) wandert in das Modul, das *„die einzige Quelle für alles, was die Vorregistrierung festschreibt"* ist; `faltenplan.py` importiert es wie `GO_LIVE_SCHNITT` | Eine **Registeränderung** — `registerdaten.py` ist Träger der Festlegungen, die Änderung braucht den Betreiber (26.6). Und es entsteht die Frage, ob dort das Datum steht (eine Zahl, wie 28.4) oder die Formel (zwei Zahlen, eine davon aus den gesperrten Bot-Dateien — `T56b.6`) |
| **(b) aus dem Registertext gelesen** | Der Faltenplan liest die Tabelle in 28.4 zur Laufzeit, so wie der Test es heute tut | **Ein Parser auf Fliesstext** im Rechenpfad: das Register ist append-only, eine spätere Berichtigung stünde in einem neuen Abschnitt, und der Parser müsste wissen, welche Tabelle gilt. Was heute eine Prüfung ist, würde eine Abhängigkeit |
| **(c) Literal mit Test gegen das Register** | der heutige Stand | Die Zahl steht **zweimal** (Register, Code); der Test hält beide zusammen, solange er läuft. Läuft er nicht, ist es eine Konstante, die niemand gegenprüft |

⛔ **Keine Empfehlung nach Aufwand.** Die Vorlage nennt die drei Wege mit ihrem
Preis; die Wahl liegt beim Betreiber, gegebenenfalls nach Rückfrage beim
Verfahrensprüfer.

---

### 32.6 Was ausdrücklich NICHT getan wurde

| | |
|---|---|
| ⛔ | **Kein Bot-Code** — `strategies/`, `shared/` unberührt; die vier `multi_symbol_optimise.py` (TB-30b) unverändert |
| ⛔ | **Keine Sperrlisten-Datei** — `faltenplan.json`, `benchmark_drawdowns.json`, `benchmark_drawdowns_vt.json` byteweise unverändert (32.3); `faltenplan_tb72.json` unverändert; `auswertung.py` unberührt (auch nicht der Docstring) |
| ⛔ | **Kein `registerdaten.py`** — die Vorlage 32.5 ist nicht vollzogen |
| ⛔ | **Kein Tag, kein Lauf** — kein Selektionslauf, kein Parametersatz bewertet, keine Kennzahl gemessen (27.1) |
| ⛔ | **`fensteranker` nicht entfernt** — drei andere Aufrufer (32.1); ob er dort noch die richtige Grösse ist, ist eine andere Aufgabe |
| ⛔ | **Der Plan nach 4a nicht ins Register** — `faltenplan_tb80.json` liegt daneben; die Abbild-Datei nach Abschnitt 30 ist eine eigene, freizugebende Aufgabe |

---

### In einfacher Sprache

**Was schiefstand:** Das Regelwerk sagt seit dem Abend des 21.09., ab welchem
Tag jeder Aktien-Bot rechnen darf — dem 19. September 2016. Das Programm, das
die Auswertungsjahre bestimmt, nahm dafür noch ein anderes Datum: den letzten
Tag, für den Kursdaten vorliegen, zehn Jahre zurück, also den 1. September
2016. Achtzehn Tage Unterschied.

**Was gemacht wurde:** Das Datum aus dem Regelwerk steht jetzt im Programm,
mit Verweis auf die Stelle, aus der es kommt. Es wird nicht ausgerechnet und
nicht aus den Bot-Programmen abgeschrieben, sondern so genommen, wie das
Regelwerk es nennt. Ein Test liest die Tabelle im Regelwerk und prüft, dass
beide übereinstimmen.

**Was sich dadurch ändert:** Bei den Jahren — nichts. Alle neun Bots beginnen
in denselben Jahren wie vorher, mit denselben Auswertungsjahren. Achtzehn Tage
weniger Vorlauf haben bei keinem Bot gereicht, um ein Jahr zu verlieren. Auf
Tagesebene sieht man die Verschiebung: der Tag, an dem das erste Wertpapier
eines Aktien-Bots bereit ist, liegt jetzt 15 bis 18 Tage später. Bei den fünf
Krypto-Bots, die kein solches Fenster haben, ändert sich nicht einmal ein Tag.

**Warum das eine Zahl ist und keine Wahl:** Die Regel stand im Regelwerk,
bevor gemessen wurde, was sie kostet. Dass sie nichts kostet, ist ein
Ergebnis — es hätte auch anders ausgehen können, und dann hätte es genauso
dagestanden.

**Was noch offen ist:** Wo das Datum dauerhaft hingehört — in das Modul, das
alle Festlegungen trägt, oder als Literal mit Test. Das ist eine Entscheidung
des Betreibers; hier stehen die Wege mit ihrem Preis, ohne Empfehlung.

*Nachgetragen in TB-80, 21.09.2026. Umsetzung mit Befund, Tatsachennotizen,
Mutationsprobe und Entscheidungsvorlage: sie nennt, was der Code tat, was das
Register verlangt, was sich dadurch ändert (nichts an den Jahren, 15 bis 18
Tage darunter), was gesperrt bleibt und was offen ist — und entfernt nichts.*

---

