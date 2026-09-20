# ERGEBNIS TB-72, Schritt 1 — Die erste Falte je Bot: Plan gegen Trockenlauf, in beide Richtungen (Mac-Sitzung, 20.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-72_erste_falte_aus_trockenlauf.md`, in der
Fassung **mit dem HALT-Nachtrag vom 20.09.2026, 19:40** („Was diese Sitzung
stattdessen tut, bis die Antwort da ist", Punkte 1–5). **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `25f568a` (= `origin/main` beim Start),
Interpreter **`trading-env/bin/python3`, Python 3.9.6** (gemessen: `--version`;
`pandas 2.3.3`). Zweiter Anlauf — der erste (bis 19:20) ist durch einen
Verbindungsabbruch beendet worden und hatte Schritt 0 und Schritt 1 ausgeführt.

⛔ **Dieses Dokument deckt nur Schritt 1.** Schritte 2 bis 7 des Auftrags sind
**nicht** ausgeführt; sie gelten erst nach Fables Antwort auf
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20e_erste_falte.md`. **Geändert
wurde kein Code.** `faltenplan.py`, `benchmark.py`, `auswertung.py`,
`faltenplan.json` und beide Benchmark-Tabellen sind unberührt (Nachweise 3 und
4 unten). Die Commit-Liste steht am Ende.

*In einfacher Sprache, zu Beginn:* Zwei Regeln sagen, wann das erste Jahr eines
Bots zählt. Der Auftrag ging davon aus, dass sie nur bei einem Bot auseinander
laufen — und zwar so, dass sein Beginn ein Jahr nach hinten rutscht. Gemessen
laufen sie bei **sechs** Bots auseinander, bei fünf davon in die **andere**
Richtung: vier Aktien-Bots könnten dem Wortlaut nach schon 1967 beginnen. Das
ist nicht gemeint, aber es ist auch nicht selbst zu entscheiden. Deshalb ist
hier gemessen und angehalten worden, nicht geändert.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart, wörtlich (Beleg
`docs/belege/TB-72/nachweis1_git_status_vor_schreiben_zweiter_anlauf.txt`):

```
 M docs/auftraege/MAC_TB-72_erste_falte_aus_trockenlauf.md
?? docs/belege/TB-72/
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20e_erste_falte.md
?? research/faltenplan_neun/erste_falte_trockenlauf.py
```

**Schritt 0, nach Urheber getrennt (HALT-Nachtrag Punkt 1):**

| Commit | Inhalt | Urheber |
|---|---|---|
| `c63bfed` | HALT-Nachtrag im Auftrag (`git diff --numstat` 49/0) und die Fable-Anfrage `…20e_erste_falte.md` | **Betreiber / steuernder Chat** — *erschlossen* aus dem Datum im Nachtrag („19:40", nach dem Abbruch) und aus der Form der Anfrage; nicht von dieser Sitzung geschrieben |
| `14c796b` | `research/faltenplan_neun/erste_falte_trockenlauf.py` und fünf Belegdateien unter `docs/belege/TB-72/` | **erster Anlauf** (abgebrochene Sitzung, Dateizeiten 19:13–19:20) — wie vorgefunden, unverändert gesichert, **vor** der Nachmessung |

Danach `git status --short` = 0 Zeilen (gemessen). Beide Commits gepusht
(`25f568a..14c796b`).

**Vor dem ersten Schreiben gelesen:** der Auftrag vollständig, die
Fable-Anfrage 20e, `research/faltenplan_neun/erste_falte_trockenlauf.py`
(vollständig), `faltenschranke_messung.py` (Modulkopf, `loader_lesart`,
`trockenlauf_ohne_schranke`), `research/vorregistrierung/faltenplan.py`
(vollständig), Register 15.6 (Registertext 4), 16.7 (Registertext 3b (a), (b)),
21.3, 21.4, `DOKUMENTATIONSSTANDARD.md` Regeln 1, 6–8, Übergabeprotokoll
Abschnitt 7 und 10, `ERGEBNIS_TB-71_register_schliessen.md` und
`JOURNAL_NACHTRAG_2026-09-20i.md` als Muster, `BACKLOG.md` Abschnitt 4.

---

## Nachweis 2 — Die neun Zahlen, aus dem Trockenlauf gemessen

### 2.1 Wie gemessen wurde

**Werkzeug:** das vorgefundene Skript
`research/faltenplan_neun/erste_falte_trockenlauf.py` (erster Anlauf), erneut
gelaufen — HALT-Nachtrag Punkt 2 (*„mit dem vorgefundenen Skript oder einem
eigenen"*). Es lässt je Bot den **Loader des Laufcodes** im Kindprozess des
Universum-Trockenlaufs laufen (`universum_trockenlauf.messe_bot`, TB-40, mit
Schreibschutz) — am **letzten Zeitpunkt jeder Falte** (Lesart H, Register 16.2)
— und zählt die handelbaren Symbole `H`. Zwei Richtungen:

| Richtung | Kandidatenfalten | Frage |
|---|---|---|
| **später** als 4a | die 4a-Falten des Plans (`faltenplan.erste_falte(bot)` bis `GO_LIVE_SCHNITT`, `faltenplan._jahresfalten`) | erste Falte mit `H ≥ 1` |
| **früher** als 4a | Falten gleicher Länge **vor** der ersten 4a-Falte, zurück bis zum ersten Kurstag des Marktes im Zeitrahmen des Bots | gibt es dort eine Falte mit `H ≥ 1`, und welche ist die früheste |

**Lauf:** 20.09.2026, 17:53–17:58 UTC (19:53–19:58 Ortszeit),
`trading-env/bin/python3`, Laufzeit **4 min 51 s**, `rc 0`, 18 Kindprozesse
(9 Bots × 2: Messung und Gegenprobe; `schritt1_nachmessung_zweiter_anlauf_stderr.txt`).
Rohausgabe: `docs/belege/TB-72/schritt1_nachmessung_zweiter_anlauf.{txt,json}`.

### 2.2 Die Tabelle (gemessen)

| Bot | Länge | Plan (`faltenplan()`) | 4a | Trockenlauf **ab 4a** | Falten **vor** 4a gemessen (davon `H ≥ 1`) | früheste vor 4a mit `H ≥ 1` | Trockenlauf **beide Richtungen** | Richtung |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `elliott_wave` | 2 J | 2018 (–2019) | 2018 | 2018 (–2019) | 1 (0) | — | 2018 (–2019) | gleich |
| **`t3_supertrend`** | 1 J | 2018 | 2018 | **2019** | 1 (0) | — | **2019** | ⛔ **später** |
| `rsi2_crypto` | 1 J | 2019 | 2019 | 2019 | 2 (**1**) | **2018** (`H = 2`) | **2018** | ⚠️ **früher** |
| `turtle_soup_crypto` | 1 J | 2018 | 2018 | 2018 | 1 (0) | — | 2018 | gleich |
| `volatility_breakout_crypto` | 1 J | 2018 | 2018 | 2018 | 1 (0) | — | 2018 | gleich |
| `elliott_wave_stocks` | 1 J | 2017 | 2017 | 2017 | 55 (**50**) | **1967** (`H = 16`) | **1967** | ⚠️ **früher** |
| `rsi2_mean_reversion` | 1 J | 2018 | 2018 | 2018 | 56 (**51**) | **1967** (`H = 16`) | **1967** | ⚠️ **früher** |
| `turtle_soup_stocks` | 1 J | 2017 | 2017 | 2017 | 55 (**50**) | **1967** (`H = 16`) | **1967** | ⚠️ **früher** |
| `volatility_breakout` | 1 J | 2018 | 2018 | 2018 | 56 (**51**) | **1967** (`H = 16`) | **1967** | ⚠️ **früher** |

`H` je Kandidatenfalte ab 4a (gemessen, aus der Rohausgabe):
`t3_supertrend` **0** / 3 / 6 / 9 / 13 / 13 / 13 / 17 / 18 (2018 … 2026);
`rsi2_crypto` 6 / 9 / … (ab 2019), davor 2017: 0, **2018: 2**;
Aktien-Bots vor 4a: 1962–1966 je **0**, ab 1967 **16**, dann monoton steigend
bis 131 (2016) bzw. 135 (2017). Erster Kurstag des Marktes: Krypto
`2017-08-17`, Aktien `1962-01-02` (gemessen aus den Kursdateien).

⭐ **Plan = 4a bei allen neun** — `faltenplan.py` rechnet heute nur 4a, wie sein
Modulkopf Z. 39–42 sagt (gemessen: Spalten „Plan" und „4a" sind gleich).
⭐ **Trockenlauf ab 4a = Register 21.4 bei allen neun** — die Spalte
„Trockenlauf ab 4a" stimmt Zeile für Zeile mit der berichtigten Faltenliste
in Register 21.4 überein (gemessen, neun Werte verglichen).

### 2.3 Erster Anlauf und Nachmessung stimmen überein (HALT-Nachtrag Punkt 2)

| | erster Anlauf (19:20) | Nachmessung (19:58) |
|---|---|---|
| `schritt1_….json` SHA-256 | `fb68537ad2d24be9736b8a223eac0cfcbe343e46e7a7f61aa2edd2849c05f6eb` | **dieselbe** |
| Textausgabe | — | **zeichengleich**, bis auf die Pfadzeile `Messung: …` |

Beleg: `docs/belege/TB-72/schritt1_vergleich_erster_zweiter_anlauf.txt`.
**Beide stimmen überein, byteweise.** ⚠️ *Das ist eine Reproduktion desselben
Skripts, keine unabhängige Messung — die steht in 2.4.*

### 2.4 Zweite Methode, unabhängig vom Kindprozess: `loader_lesart`

`faltenschranke_messung.loader_lesart(bot)` (TB-56) rechnet **ohne
Trockenlauf** aus `MIN_HISTORY_*` je Symbol den Tag, ab dem der Loader es
handelbar macht (erster Kurstag + `MIN_HISTORY_DAYS`; bei `elliott_wave` die
17 520. Kerze). Gelaufen 20.09., 19:59, Skript und Ausgabe
`docs/belege/TB-72/schritt1_loader_lesart_neun.{py,txt,json}`:

| Bot | Schranke (Register 3b (b)) | frühestes Symbol handelbar ab | Jahr | stimmt mit 2.2 „beide Richtungen"? |
|---|---|---|---:|---|
| `elliott_wave` | `MIN_HISTORY_HOURS` 17 520 | 2019-08-20 | 2019 | ja — liegt in der Zweijahresfalte 2018–2019 |
| `t3_supertrend` | `MIN_HISTORY_DAYS` 730 | 2019-08-17 | 2019 | **ja** |
| `rsi2_crypto` | `MIN_HISTORY_DAYS` 500 | 2018-12-30 | 2018 | **ja** |
| `turtle_soup_crypto` | `MIN_HISTORY_DAYS` 500 | 2018-12-30 | 2018 | ja |
| `volatility_breakout_crypto` | `MIN_HISTORY_DAYS` 500 | 2018-12-30 | 2018 | ja |
| vier Aktien-Bots | `MIN_HISTORY_DAYS` 1 825 | 1967-01-01 | 1967 | **ja** |

**9/9 gleich.** Die Richtung „früher" hängt damit nicht am Kindprozess: sie
folgt aus den fünf registrierten Schranken und dem ersten Kurstag der Dateien.

⚠️ *Erschlossen, nicht gemessen — warum der Trockenlauf 1967 sieht und 4a
2017/2018:* `faltenplan_neun.fensteranker` verankert das Zehnjahresfenster der
Aktien-Bots (`RECENT_YEARS_ONLY = 10`) am **letzten Kurstag der Daten** (2016-09-01,
Spalte „Fensteranker" im Beleg); der Trockenlauf reicht dem Loader am Stichtag
nur Daten **bis zum Faltenende**, und der Loader schneidet dann zehn Jahre vor
*diesem* Ende. Für die Falte 1967 ist das Fenster 1957–1967, und 16 Symbole
haben darin 1 825 Tage Historie. Genau das meint die Fable-Anfrage mit
*„eine Bedingung, die der Trockenlauf gar nicht prüft"* („Universum liegt
vor"). Nicht nachgemessen an `loaderlauf.py`; die Zahlen in 2.2 hängen nicht
an dieser Erklärung.

### 2.5 ⭐ Hat die Vormessung aus Abschnitt 1 des Auftrags getroffen?

Die Vormessung des Chats (20.09., 19:00, aus `benchmark_drawdowns_vt.json`)
sagt: *nur `t3_supertrend` weicht ab (Plan 2018, erste nicht-leere Falte 2019)*.
Nachvollzogen aus derselben Datei über `handelstage` je Falte
(`docs/belege/TB-72/schritt1_vormessung_aus_vt_json.txt`, 20.09., 19:59):
`t3_supertrend` 2018 hat **0** Handelstage, 2019 hat 136; bei den acht anderen
ist die erste Planfalte nicht leer (`turtle_soup_crypto` und
`volatility_breakout_crypto` 2018 mit **1** Handelstag, `elliott_wave`
2018–2019 mit 133).

**Antwort in zwei Teilen:**

| | |
|---|---|
| ✅ **Getroffen** für die Richtung, die sie sehen konnte | *später als der Plan:* genau **ein** Bot, `t3_supertrend`, 2018 → 2019. Neun Zahlen aus dem Trockenlauf ab 4a = neun Zahlen der Vormessung |
| ⛔ **Nicht getroffen** als Aussage *„nur `t3_supertrend` weicht ab"* | der blinde Fleck, den der Auftrag selbst benannt hat, ist real: **fünf** Bots haben vor ihrer 4a-Falte Falten mit `H ≥ 1` — `rsi2_crypto` eine (2018, `H = 2`), die vier Aktien-Bots je 50 bzw. 51 (ab 1967). Diese Falten stehen nicht in `_vt.json`, weil sie nicht im Plan stehen |

**Es gilt die Messung: das Auseinanderlaufen von 4a und 3b (a) ist nicht
einseitig.** Die Tabelle im HALT-Nachtrag (aus dem ersten Anlauf) ist damit
**bestätigt, Zahl für Zahl** (2.3, byteweise).

---

## Nachweis zur Gegenprobe gegen TB-56 (HALT-Nachtrag Punkt 3)

Der erste Anlauf meldet *„Gegenprobe TB-56 (trockenlauf_ohne_schranke): alle
gleich: ja"*. **Nachgeprüft, was das Flag vergleicht** (aus dem JSON gelesen,
`gegenprobe_tb56.je_bot[*]`, 20.09., 20:01):

| Bot | TB-56 `erste_falte_mit_loader_symbol_H` | Trockenlauf **ab 4a** | Trockenlauf **beide Richtungen** | Flag `gleich` vergleicht mit |
|---|---:|---:|---:|---|
| `elliott_wave` | 2018-2019 | 2018 | 2018 | ab 4a ✅ (= beide) |
| `t3_supertrend` | 2019 | 2019 | 2019 | ab 4a ✅ (= beide) |
| `rsi2_crypto` | 2019 | 2019 | **2018** | ab 4a ✅ — **nicht** mit „beide" |
| `turtle_soup_crypto` | 2018 | 2018 | 2018 | ab 4a ✅ (= beide) |
| `volatility_breakout_crypto` | 2018 | 2018 | 2018 | ab 4a ✅ (= beide) |
| `elliott_wave_stocks` | 2017 | 2017 | **1967** | ab 4a ✅ — **nicht** mit „beide" |
| `rsi2_mean_reversion` | 2018 | 2018 | **1967** | ab 4a ✅ — **nicht** mit „beide" |
| `turtle_soup_stocks` | 2017 | 2017 | **1967** | ab 4a ✅ — **nicht** mit „beide" |
| `volatility_breakout` | 2018 | 2018 | **1967** | ab 4a ✅ — **nicht** mit „beide" |

**Befund:** *„alle gleich: ja"* ist **richtig, aber nur für die Richtung
„später"**. `trockenlauf_ohne_schranke` setzt den vollen Trockenlauf
(`universum_trockenlauf.trockenlauf`) auf den Plan von `faltenplan_neun` ohne
Schranke an — und dieser Plan beginnt **bei 4a**; Falten davor kennt er nicht
(gemessen: `trockenlauf_ohne_schranke` schreibt `plan_ohne_schranke()` als Plan für den Trockenlauf, `faltenschranke_messung.py` Z. 315–326).
Das Skript vergleicht deshalb — zutreffend — mit `erste_falte_trockenlauf_ab_4a`
(`erste_falte_trockenlauf.py` Z. 232–237), nicht mit der Spalte „beide
Richtungen". Für die Richtung „früher" ist TB-56 konstruktionsbedingt blind;
dort steht als Gegenprobe die zweite Methode aus 2.4 (`loader_lesart`, 9/9).
Monotonie verletzt: nein; Schreibversuche: keine (beide gemessen, JSON).

⭐ *Der Satz „alle gleich: ja" im ersten Anlauf war also kein Fehler, aber ohne
diese Einordnung liesse er sich als „der Trockenlauf bestätigt die neun Zahlen
in beide Richtungen" lesen. Das tut er nicht.*

---

## Nachweis 3 — SHA-256 der drei Sperrlisten-Dateien, vorher und nachher

`research/vorregistrierung/ergebnisse/`, gemessen mit `shasum -a 256`
(`nachweis3_sha256_vorher.txt` vom ersten Anlauf 19:13; nachher 19:59 dieser
Sitzung, `nachweis3_sha256_nachher_schritt1.txt`):

| Datei | vorher | nachher |
|---|---|---|
| `benchmark_drawdowns.json` | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` | **gleich** |
| `benchmark_drawdowns_vt.json` | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` | **gleich** |
| `faltenplan.json` | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` | **gleich** |

## Nachweis 4 — `faltenplan.json` unverändert

Hash oben; `git log` für die Datei: ein einziger Commit `a2fcf01` (TB-30a,
14.09.2026). ⚠️ **Für Schritt 3 vorgemerkt (bekannt aus TB-61, Befund Z. 251):**
die Datei auf der Platte ist der **TB-30a-Stand** (Krypto `platzhalter`, Aktien
ab 2019, gemessen durch Vergleich mit dem Beleg des ersten Anlaufs
`faltenplan_4a_stand_vor_tb72.json`, der `faltenplan.faltenplan()` im Speicher
wiedergibt). *Die Gegenüberstellung „genau ein Bot, genau eine Falte" in
Schritt 3 kann nur gegen den Speicherstand (den Beleg) gelingen, nicht gegen die
Datei — dort weichen alle neun Bots ab.*

## Nachweis 10 — `git diff --numstat` je Datei, nichts ausserhalb `docs/` und `research/`

Diese Sitzung hat geschrieben (alle Commits gemessen mit `git show --stat`):
`docs/belege/TB-72/*` (15 Dateien, davon fünf aus dem ersten Anlauf),
`docs/ERGEBNIS_TB-72_schritt1_erste_falte.md`,
`docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20j.md`,
`docs/projektfuehrung/BACKLOG.md` (**eine** Zeile, `numstat` 1/0). Unter
`research/` nur `faltenplan_neun/erste_falte_trockenlauf.py` — **neu, aus dem
ersten Anlauf, unverändert übernommen**; keine bestehende Datei unter
`research/` geändert. Nachweise 5 bis 9 gehören zu Schritten 2 bis 7 und
stehen aus.

---

## Was der Auftrag anders sah — und wo die Messung galt

| Auftrag | gemessen / getan |
|---|---|
| Abschnitt 1: *„nur `t3_supertrend` weicht ab"* | in der Richtung „später" ja; insgesamt **sechs** Bots (2.5) |
| Abschnitt 0: Fables Prämisse *„`MIN_HISTORY_*` macht Symbole später handelbar, als 4a rechnet"* | bei **einem** Bot; bei fünf macht es sie **früher** handelbar (2.2, 2.4) |
| Schritt 2 in der Fassung vor dem HALT: *„`erste` kommt aus dem Trockenlauf"* | wörtlich umgesetzt gäbe das 1967 für vier Bots — **nicht ausgeführt**, HALT-Nachtrag Punkt 5 |
| HALT-Nachtrag Punkt 3: *„alle gleich: ja — prüfe das nach"* | stimmt für „später"; für „früher" ist TB-56 blind, Ersatz-Gegenprobe `loader_lesart` 9/9 |
| Schritt 3 (steht aus): Gegenüberstellung gegen `faltenplan.json` | die Datei ist TB-30a-Stand; Vergleich gegen den Speicherstand nötig (Nachweis 4) |
| Nachweis 3 spricht von `ergebnisse/…` | Dateien liegen unter `research/vorregistrierung/ergebnisse/` (wie schon TB-71) |

---

## Offen

| | wer |
|---|---|
| ⛔ **Fables Antwort auf die drei Fragen in `FABLE_ANFRAGE_2026-09-20e_erste_falte.md`** — Lesart `max(4a, 3b (a))`, Berichtigung oder Präzisierung von 21.3 (b), Satz zu „Universum liegt vor" in 4a | Fable / steuernder Chat |
| Schritte 2 bis 7 des Auftrags (Ableitung im `faltenplan.py`, `faltenplan_tb72.json`, `benchmark_drawdowns_tb72.json`, Test mit Mutation, Register 25, Backlog-Zeile „erledigt") | nächste Sitzung **nach** der Antwort — ⚠️ Schritt 2 in neuer Form (Fable-Anfrage: *„4a wie bisher UND Trockenlauf als Verschiebung nach hinten, in einer Funktion"*), falls die Lesart trifft |
| `erste_falte_trockenlauf.py` ist als Skript gesichert, aber noch von keinem Test aufgerufen und in keinem `BERICHT.md` erwähnt | Schritt 5 |
| Dieser Nachtrag ins Journal (Block nach dem höchsten vorhandenen, am 20.09. gemessen `BT`; `(20g)`, `(20h)`, `(20i)` liegen davor) | nächste Einarbeitung / TB-64-Wächter |
| Projektablage nachziehen (`K4e`): Backlog geändert, neues Ergebnisdokument | steuernder Chat / Betreiber |

---

## Commit-Liste dieser Sitzung

| Commit | Schritt | Inhalt |
|---|---|---|
| `c63bfed` | 0 | Betreiber-Dateien: HALT-Nachtrag im Auftrag, Fable-Anfrage 20e |
| `14c796b` | 0 | erster Anlauf: Skript und fünf Belege, unverändert |
| `0562c75` | 1 | Nachmessung (byteweise gleich), `loader_lesart` je Bot, Vormessung aus `_vt.json`, Nachweis 1, Hashes nachher |
| `72e512f` | 1 | Belegskript pfadunabhängig, Ausgabe unverändert |
| `5dcea37` | 4 | dieses Dokument, Journal-Nachtrag `(20j)`, eine Backlog-Zeile `K4k` |

---

## In einfacher Sprache

**Was wir wissen wollten:** Ob nur ein Bot davon betroffen ist, dass zwei
Regeln für das erste Jahr verschieden rechnen — und ob die schnelle Messung aus
dem Chat, die das behauptet hat, einen blinden Fleck hatte.

**Was herauskam:** Sie hatte ihn. In der einen Richtung — der Bot darf erst
später handeln, als die Datenlage vermuten lässt — ist wirklich nur
`t3_supertrend` betroffen, genau wie vorhergesagt. In der anderen Richtung
aber, die die schnelle Messung gar nicht sehen konnte, sind fünf Bots
betroffen: Ihr Programm dürfte dem Wortlaut nach schon Jahre oder Jahrzehnte
früher handeln als das Regelwerk meint — vier Aktien-Bots ab 1967. Zwei
unabhängige Rechenwege sagen dasselbe, und die Wiederholung der Messung ist
Byte für Byte gleich.

**Warum das wichtig ist:** Der Auftrag wollte den Plan künftig direkt aus dem
Programmverhalten ableiten. Wörtlich getan, hätte das vier Bots fünfzig
zusätzliche Jahre gegeben, in denen es weder die Bots noch ihr heutiges
Universum gab. Das meint niemand — aber welche Lesart des Regelwerks gilt, ist
eine Auslegungsfrage, und die Wirkung ist schon bekannt. Genau dann darf die
ausführende Sitzung nicht selbst entscheiden.

**Was passiert ist:** Gemessen, belegt, angehalten. Kein Code geändert, keine
Ergebnisdatei angefasst. Die Frage liegt bei Fable; die Antwort entscheidet,
wie es weitergeht.
