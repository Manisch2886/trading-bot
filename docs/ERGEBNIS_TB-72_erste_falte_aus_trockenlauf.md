# ERGEBNIS TB-72 — `t3_supertrend` beginnt 2019, und der Faltenplan leitet die erste Falte aus dem Trockenlauf ab (Mac-Sitzung, 20.09.2026, Schritte 2–7)

**Auftrag:** `docs/auftraege/MAC_TB-72_erste_falte_aus_trockenlauf.md`, in der
Fassung **mit dem ERLEDIGT-Nachtrag vom 20.09.2026, 20:15** (Fables Antwort zur
Konjunktion, Schritte 2–7 freigegeben). **Ausgeführt am MacBook**, Zweig `main`,
Ausgang `7b73584` (= `origin/main` beim Start), Interpreter
**`trading-env/bin/python3`, Python 3.9.6**. Dritter Anlauf: der erste war ein
Verbindungsabbruch nach Schritt 1, der zweite hat Schritt 1 nachgemessen und
vor Schritt 2 angehalten (`docs/ERGEBNIS_TB-72_schritt1_erste_falte.md`, das
weiter gilt und hier nicht wiederholt wird).

⭐ **Kurz:** Genau ein Bot ändert sich — `t3_supertrend` beginnt 2019 statt 2018,
sieben Selektionsfalten statt acht, `DD_Toleranz` **−13,90 / −26,57 / −48,10**
statt −12,89 / −24,73 / −45,16 (25 / 50 / 100 %), Zahl für Zahl die Erwartung
aus TB-65 C1. Die acht anderen Bots sind gegen `benchmark_drawdowns_vt.json`
zeichengleich. `faltenplan.py` rechnet die erste Falte nicht mehr nach, sondern
leitet sie als Konjunktion aus 4a und dem Trockenlauf ab; ein Test mit
Mutationsprobe hält das fest; Register Abschnitt 25 trägt die Berichtigung mit
Fables Ersatztext. **Sperrliste nicht vollzogen, Tag nicht gesetzt, die drei
gesperrten Dateien byteweise unberührt.**

*In einfacher Sprache, zu Beginn:* Das Regelwerk sagt seit dem 19.09., dass ein
Jahr für einen Bot erst zählt, wenn sein Programm darin wenigstens einen Kurs
handeln darf. Das Programm, das den Jahresplan schreibt, hat das bisher nicht
angewendet und bei einem Bot ein leeres Jahr geführt. Jetzt fragt der Plan das
Programm selbst — und zählt ein Jahr nur, wenn **beide** Bedingungen gelten:
die Daten reichen aus **und** das Programm darf handeln. Dadurch kann keine der
beiden Regeln den Beginn nach vorn ziehen (das hätte vier Aktien-Bots 1967
gegeben). Ergebnis: ein Bot beginnt ein Jahr später, seine Verlustgrenze wird
etwas weiter. Das ist die Wirkung, nicht der Grund.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart, wörtlich:

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/auftraege/MAC_TB-72_erste_falte_aus_trockenlauf.md
 M docs/projektfuehrung/ARBEITSWEISE.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-09-20e_konjunktion.md
```

**Schritt 0:** alle vier sind Betreiber-Dateien (Fables Antwort, der
ERLEDIGT-Nachtrag im Auftrag, die TB-72-Zeile und die neue Zeile TB-74 in
`AKTUELLER_AUFTRAG.md`, die `screen`/Schlüsselbund-Blöcke in `ARBEITSWEISE.md`)
— gesichert als eigener Zwischencommit `96cc9c7`, im Text als *„nicht von
dieser Sitzung geschrieben, nicht verändert"* vermerkt (Muster TB-68/TB-71).
Danach `git status --short` = 0 Zeilen, gepusht.

**Vor dem ersten Schreiben gelesen:** der Auftrag vollständig,
`FABLE_ANTWORT_2026-09-20e_konjunktion.md`, `ERGEBNIS_TB-72_schritt1_erste_falte.md`,
`faltenplan.py`, `erste_falte_trockenlauf.py`, `faltenschranke_messung.py`,
`benchmark.py`, `universum_trockenlauf.py` (`messe_bot`), `loaderlauf.py`
(Kopf), `test_vorregistrierung.py`, `test_faltenplan_neun.py` (Kopf), Register
15.6, 16.7, 21.3, 21.4, 23, 24, `BACKLOG.md` Abschnitt 4, Journal-Nachtrag `(20j)`.

---

## Nachweis 2 — Die neun Zahlen (Schritt 1) und die Vormessung

Schritt 1 ist in `docs/ERGEBNIS_TB-72_schritt1_erste_falte.md` belegt (zwei
Anläufe byteweise gleich, zweite Methode `loader_lesart` 9/9). Die Vormessung
aus Abschnitt 1 des Auftrags hat für die Richtung *„später"* getroffen (genau
`t3_supertrend`, 2018 → 2019) und als Gesamtaussage nicht (fünf Bots
*„früher"*). **Unter der Konjunktion ist die Richtung *„früher"* gegenstandslos**
— (ii) kann den Beginn nicht vorziehen, weil (i) weiter gelten muss — und die
Vormessung trifft damit genau das, was der Plan jetzt rechnet:

| Bot | 4a (i) | Trockenlauf ab 4a (ii) | **Plan (Konjunktion)** | Register 21.4 | H je 4a-Kandidat |
|---|---:|---:|---:|---:|---|
| `elliott_wave` | 2018 | 2018 | **2018** (–2019) | 2018–2019 | 3 / 9 / 13 / 17 / 18 |
| **`t3_supertrend`** | 2018 | **2019** | **2019** | 2019 | **0** / 3 / 6 / 9 / 13 / 13 / 13 / 17 / 18 |
| `rsi2_crypto` | 2019 | 2019 | **2019** | 2019 | 6 / 9 / 10 / 13 / 13 / 17 / 18 / 20 |
| `turtle_soup_crypto` | 2018 | 2018 | **2018** | 2018 | 2 / 6 / 9 / … |
| `volatility_breakout_crypto` | 2018 | 2018 | **2018** | 2018 | 2 / 6 / 9 / … |
| `elliott_wave_stocks` | 2017 | 2017 | **2017** | 2017 | 135 / 136 / … |
| `rsi2_mean_reversion` | 2018 | 2018 | **2018** | 2018 | 136 / 137 / … |
| `turtle_soup_stocks` | 2017 | 2017 | **2017** | 2017 | 135 / 136 / … |
| `volatility_breakout` | 2018 | 2018 | **2018** | 2018 | 136 / 137 / … |

Gemessen im Test (Schritt 5, eigener `messe_bot`-Aufruf je Bot, alle
Kandidaten; `docs/belege/TB-72/schritt5_test_lauf.txt`) und im Plan
(`faltenplan_tb72.json`, Feld `erste_falte_trockenlauf_H`). **Plan = Trockenlauf
= Register 21.4 bei allen neun.**

**`rsi2_crypto` bleibt 2019, selbst nachgemessen** (Auftrag: *„Miss das selbst
nach"*; `docs/belege/TB-72/schritt2_rsi2_crypto_bedingung_i.txt`): BTC und ETH
beginnen 2017-08-17 und haben bis 2017-12-31 **137** Tagesbalken; der 150.
Balken (Indikator-Vorlauf) liegt am **2018-01-14**. Bedingung (i) ist am
1.1.2018 nicht erfüllt, (ii) schon (`H = 2`, BTC/ETH ab 2018-12-30). Konjunktion
→ 2019. Fables Zahl 137 trifft.

---

## Schritt 2 — was am Code geändert ist (Commit `e7a4108`)

| Datei | Änderung |
|---|---|
| `research/vorregistrierung/faltenplan.py` | `erste_falte(bot)` → **`erste_falte_4a(bot)`** (Bedingung (i), Rechnung unverändert). Neu **`erste_falte(bot, laenge, schnitt)`** = die Konjunktion: Kandidaten `_jahresfalten(erste_falte_4a, GO_LIVE_SCHNITT, laenge)`, dann `eft.erste_falte_nach_3b(bot, kandidaten)` — die erste Kandidatenfalte mit `H ≥ 1`. Rückgabe `(Jahr, Herkunft)`; der Plan trägt je Bot neu `erste_falte_4a` und `erste_falte_trockenlauf_H` (H je geprüfter Falte). `erste_falte_quelle` mitberichtigt (nennt die Neufassung, 4a als Regel, den Trockenlauf als operative Form, den Plan als Ableitung). Modulkopf Regel 2 und 3 berichtigt — der Satz *„das rechnet dieses Modul nicht"* bleibt als ersetzt stehen. **Faltenlänge, Purge, Embargo, Go-Live-Schnitt unangetastet** (Diff-Hunks berühren keine dieser Zeilen) |
| `research/faltenplan_neun/erste_falte_trockenlauf.py` | `erste_falte_nach_3b(bot, kandidaten, vollstaendig=False)`: ohne `vollstaendig` Falte für Falte, **ein Kindprozess je geprüftem Faltenende, Schluss beim ersten `H ≥ 1`**; mit `vollstaendig=True` alle Kandidaten in einem Prozess. Die Schritt-1-Messung `main()` ruft `vollstaendig=True` und ist unverändert (Ergebnis je Falte ist dasselbe, weil jeder Stichtag im Kindprozess ein eigener Loader-Lauf ist). Modulkopf um den Absatz zur Ableitung ergänzt |

**Keine Konstantenkopie:** `MIN_HISTORY_*` steht in keiner der beiden Dateien;
es wirkt im Bot-Code, im Kindprozess des TB-40-Werkzeugs (`loaderlauf.py`, mit
Schreibschutz). `benchmark.py` importiert `faltenplan` weiter unverändert.

⚠️ **Laufzeit, gemessen:** ein Aktien-Loader braucht rund **6 s je Kindprozess**
(+ ~1,7 s je weiterem Stichtag), ein Krypto-Loader 1,4–2,3 s. Über alle
Kandidaten in einem Prozess hätte die Ableitung ~75 s je `faltenplan()`
gekostet; Falte für Falte sind es **+25 s** (`faltenplan()` 12,4 s → 37,6 s im
ersten Aufruf je Prozess; danach `lru_cache`). Das zahlt jeder Prozess, der den
Plan importiert — auch `test_vorregistrierung.py` Teil H, das `auswertung.py`
sechsmal als eigenen Prozess startet (Nachweis 8).

---

## Nachweis 3 — SHA-256 der Sperrlisten-Dateien, vorher und nachher

`research/vorregistrierung/ergebnisse/`, `shasum -a 256`
(`nachweis3_sha256_vorher_schritt3.txt` vor Schritt 3,
`nachweis3_sha256_nachher_schritt4.txt` nach dem Benchmark-Lauf; `diff` leer):

| Datei | vorher | nachher |
|---|---|---|
| `benchmark_drawdowns.json` | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` | **gleich** |
| `benchmark_drawdowns_vt.json` | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` | **gleich** |
| `faltenplan.json` | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` | **gleich** |

Dieselben drei Werte wie in Schritt 1 (`nachweis3_sha256_vorher.txt`, erster
Anlauf 19:13). `benchmark_drawdowns_neu.json` und `_ohne_schranke.json`
ebenfalls nicht angefasst (`git status` sauber ausser den neuen Dateien).

## Nachweis 4 — `faltenplan.json` unverändert

Hash oben; `git diff --numstat -- research/vorregistrierung/ergebnisse/` vor
dem Commit von Schritt 3: **keine Zeile**. Der neue Plan heisst
`ergebnisse/faltenplan_tb72.json` (Commit `edd1bce`), geschrieben vom
Belegskript `docs/belege/TB-72/schritt3_faltenplan_tb72.py` mit denselben
`json.dump`-Einstellungen wie `faltenplan.py::main` — **ohne** dessen `main()`
aufzurufen, das immer nach `faltenplan.json` schreibt.

**Gegenüberstellung (Schritt 3, `docs/belege/TB-72/schritt3_gegenueberstellung.txt`):**

| gegen | Bots mit Änderung | Falten (Grenzen/Rolle/Training) | Folgeänderung nur `embargo_nach_falten` |
|---|---|---|---|
| **(a) Speicherstand vor TB-72** (`faltenplan_4a_stand_vor_tb72.json`, Schritt 0) | **1** — `t3_supertrend` | **1** — Falte 2018 entfällt; `erste_falte` 2018 → 2019; `selektionsfalten` 8 → 7 | 8 — Falten 2019–2026 verlieren `'2018'` aus der Embargo-Liste (eine entfallene Falte kann nicht embargiert werden) |
| (b) `faltenplan.json` auf der Platte | 9 — alle | 45 | 32 |

⭐ **Erwartung *„genau ein Bot, genau eine Falte"* trifft für (a).** ⚠️ Die erste
Fassung des Skripts zählte die acht Embargo-Folgen als Falten-Änderungen und
meldete *„NEIN (Befund)"*; nachgesehen: Grenzen, Rollen und
`training_bis_ausschliesslich` der Falten 2019–2026 sind gleich, nur die Liste
der embargierten Vorfalten ist um `'2018'` kürzer. Die zweite Fassung trennt
beides (Journal `(20k)`, Befund 3). **(b) ist kein Befund dieser Aufgabe:** die
Datei ist TB-30a-Stand (`a2fcf01`; Krypto `platzhalter`, Aktien ab 2019) und
seit TB-56/TB-61 nicht neu geschrieben — bekannt aus Schritt 1 (`K4k`). Zwei neue
Felder je Bot (`erste_falte_4a`, `erste_falte_trockenlauf_H`) sind in (a) bei
allen neun ausgewiesen; sie ändern keine registrierte Zahl.

---

## Nachweis 5 — Die Gegenprobe der acht anderen Bots (Schritt 4)

**Lauf:** `trading-env/bin/python3 research/vorregistrierung/benchmark.py --ziel research/vorregistrierung/ergebnisse/benchmark_drawdowns_tb72.json`,
20.09.2026, 20:29–20:31 Ortszeit, `rc 0` (Commit `27c58a2`; stdout/stderr
`docs/belege/TB-72/schritt4_benchmark_*.txt` — stderr nur die bekannte
`FutureWarning` zu `pct_change`).

`docs/belege/TB-72/schritt4_gegenprobe_vt.{py,txt}` — je Bot gegen `_vt.json`:

| Bot | Falten | Stufen | `handelstage` | Symbolzahl | `DD_Toleranz` | Ergebnis |
|---|---:|---:|---:|---:|---:|---|
| `elliott_wave` | 5 | 500 | 5 | 5 | 100 | zeichengleich |
| `elliott_wave_stocks` | 10 | 1 000 | 10 | 10 | 100 | zeichengleich |
| `rsi2_crypto` | 8 | 800 | 8 | 8 | 100 | zeichengleich |
| `rsi2_mean_reversion` | 9 | 900 | 9 | 9 | 100 | zeichengleich |
| `turtle_soup_crypto` | 9 | 900 | 9 | 9 | 100 | zeichengleich |
| `turtle_soup_stocks` | 10 | 1 000 | 10 | 10 | 100 | zeichengleich |
| `volatility_breakout` | 9 | 900 | 9 | 9 | 100 | zeichengleich |
| `volatility_breakout_crypto` | 9 | 900 | 9 | 9 | 100 | zeichengleich |

**69 Falten × 100 Stufen = 6 900 Stufen, dazu `handelstage`, Symbolzahl, Rolle
und Grenzen je Falte, `handelbar_ab`, `DD_Toleranz` 8 × 100 —
`json.dumps(sort_keys=True)` je Bot identisch. Abweichend: keiner.**

## Nachweis 6 — `t3_supertrend`, vorher / nachher

| Falte | Rolle | Tage vt / tb72 | Symb. vt / tb72 | 100 Stufen gleich |
|---|---|---:|---:|---|
| 2018 | Selektion → **entfällt** | 0 / – | 0 / – | (vt: 0,00 auf allen Stufen) |
| 2019 … 2025 | Selektion | 136 / 136, 366, 365, 365, 365, 366, 365 — gleich | 3, 6, 9, 13, 13, 13, 17 — gleich | **ja**, alle sieben |
| 2026 | Bestätigung | 243 / 243 | 18 / 18 | ja |

| Exposure | `_vt.json` (mit 2018) | **`_tb72.json`** | Erwartung TB-65 C1 *„ohne 2018"* | trifft |
|---|---:|---:|---:|---|
| 25 % | −12,89 | **−13,90** | −13,90 | ✅ |
| 50 % | −24,73 | **−26,57** | −26,57 | ✅ |
| 100 % | −45,16 | **−48,10** | −48,10 | ✅ |

`DD_Toleranz`: **100 von 100 Stufen** verschieden; die drei ausgewiesenen
treffen die Erwartung aus TB-65 (die aus einer anderen Rechnung stammte) auf die
zweite Nachkommastelle. **Die Toleranz wird nachgiebiger** — Wirkung, nicht
Grund (Register 25.4, F17).

---

## Nachweis 7 — Die Mutation aus Schritt 5

**Wo der Test liegt und warum:** `research/faltenplan_neun/test_erste_falte_trockenlauf.py`
— **neben** `faltenschranke_messung.py`, nicht in `test_vorregistrierung.py`.
Gründe: (1) `test_vorregistrierung.py` bricht im Repo in Teil A an der
gesperrten Tabelle ab (`KeyError: '2017'`, Nachweis 8) und erreichte eine
Prüfung in Teil G bis zum Vollzug der Sperrliste gar nicht; (2) der Test
gehört zu dem Modul, das Bedingung (ii) misst, und misst sie selbst noch einmal
mit einem **eigenen** `messe_bot`-Aufruf (unabhängig von
`erste_falte_trockenlauf`); (3) er trägt seine Mutationsprobe selbst (Teil D,
Wegwerf-Kopie im eigenen Prozess, Muster `test_vorregistrierung.py` Teil H).
Docstring mit Fables Einordnung: *„nicht mehr eine Wache gegen Abweichung,
sondern der Nachweis, dass die Ableitung nicht regrediert"*. **Lauf: 50/50,
2 min 37 s** (`docs/belege/TB-72/schritt5_test_lauf.txt`; Teile A neun Zahlen
Plan = Trockenlauf, Kandidaten davor `H = 0`, Messung im Plan; B erste Falte ≥
4a; C = Register 21.4; D Kontrolle und Mutation in der Kopie).

**Die Mutation am echten `faltenplan.py`** (`docs/belege/TB-72/schritt5_mutation.sh`,
Rohausgabe `schritt5_mutation_lauf.txt`):

| | |
|---|---|
| Änderung | `jahr, messung = eft.erste_falte_nach_3b(bot, kandidaten)` → `jahr, messung = erste_4a, []` — die Ableitung durch die 4a-Nachrechnung ersetzt (`git diff --numstat` 1/1) |
| Meldung | **38 bestanden, 12 GESCHEITERT, `rc 1`**: *„A: t3_supertrend — erste Falte laut Plan = erste Kandidatenfalte mit H >= 1 — Plan 2018, Trockenlauf 2019"*; *„C: t3_supertrend — erste Falte = Register 21.4 — Register 2019"*; neunmal *„der Plan fuehrt die Messung mit (erste_falte_trockenlauf_H) — []"*; *„D0: die unveraenderte Kopie sieht … die neun Zahlen des Trockenlaufs"* (die Kopie erbt die Mutation: `t3_supertrend: 2018`) |
| Zurückgenommen | `git checkout -- research/vorregistrierung/faltenplan.py`; `numstat` leer, `grep -c MUTATION` = 0; Endfassung des Tests danach erneut **50/50** |

⭐ **Die Probe beisst** (B1): ohne die Ableitung wird der Test rot, und zwar an
der Instanz (`t3_supertrend`) und an der Herkunft (leere Messung im Plan).

---

## Nachweis 8 — `test_vorregistrierung.py`, Ergebnis je Teil

**Im Repo** (`trading-env/bin/python3 research/vorregistrierung/test_vorregistrierung.py`,
`docs/belege/TB-72/nachweis8_test_im_repo.txt`, 20:40):

| Teil | Ergebnis |
|---|---|
| **A** | **Abbruch** mit `KeyError: '2017'` in `auswertung.py:237` (`zulaessigkeit`) — der Test liest die **gesperrte** Tabelle (`test_vorregistrierung.py:82`), die die Falte 2017 nicht kennt. ⚠️ **Erwartet und kein Befund** (Auftrag Nachweis 8; zeichengleich mit TB-61 Nachweis 7 und TB-66 Nachweis 8) |
| B–H | nicht erreicht — das Skript bricht beim ersten Fehler ab |

**In der Wegwerf-Kopie `research/_tb72_kopie/`** (zwei Ebenen unter der
Repo-Wurzel wie TB-61/TB-66; **`benchmark_drawdowns_tb72.json` an der Stelle von
`benchmark_drawdowns.json` der Kopie** — Hash der Kopie `e4ba341d…`, das
Original `a163c498…` unberührt; Kopie danach entfernt; Skript
`docs/belege/TB-72/nachweis8_test_vorregistrierung.sh`, Rohausgabe
`nachweis8_test_in_kopie_mit_tb72_tabelle.txt`, Laufzeit 20:41–20:53, **~12 min**
— parallel zum Test aus Schritt 5, daher nicht als Laufzeitmessung zu lesen):

| Teil | Ergebnis |
|---|---|
| A, B, C, D, E, F | alle Prüfungen bestanden — **auch mit dem neuen Plan** (`faltenplan()` aus der Kopie rechnet die Konjunktion, Bedingung (ii) über den Kindprozess; `TB30A_BASE_DIR` wird von der Kopie zwei Ebenen unter der Wurzel selbst richtig abgeleitet) |
| **G** | **G6 rot**: *„elliott_wave — 2020 und 2022 sind Testfalten, keine Trainingsjahre — ['2018-2019', '2020-2021', '2022-2023', '2024-2025', '2026-2027']"* — die Probe erwartet Einjahresnamen (TB-61 Befund, unverändert) |
| **H** | **H3 rot**: *„ohne die gesetzte Null aendert sich die Statistik — 'Netto-Sharpe (Med.) 0.1000' / 'Netto-Sharpe (Med.) 0.1000'"* — Probe auf 7 Falten gebaut (TB-61 Befund, unverändert) |
| **Summe** | **163 bestanden, 2 gescheitert — dieselben zwei wie in TB-61 und TB-66.** ⭐ Die `_tb72`-Tabelle und der abgeleitete Plan brechen keine weitere Prüfung; **Teil D** (Drawdown-Bedingung in beide Richtungen bei `turtle_soup_stocks`) besteht mit den `_tb72`-Zahlen (für diesen Bot zeichengleich mit `_vt`) |

⚠️ G6 und H3 sind aus TB-61 bekannt und **nicht Gegenstand dieses Auftrags**
(Abschnitt 5). ⚠️ *Nebenbefund am Werkzeug:* `pgrep -f <Skriptname>` trifft in
dieser Umgebung die eigene Warteschleife (bekannt aus TB-46b für `pkill -f`) —
zwei Warteschleifen dieser Sitzung hingen deshalb nach dem Ende des Laufs und
wurden von Hand beendet; der Lauf selbst war davon nicht berührt.

---

## Nachweis 9 — Register: `numstat` Spalte zwei = 0

`git diff --numstat docs/VORREGISTRIERUNG_neuselektion.md` vor dem Commit
`b5a1a80`: **`220 0`** (`docs/belege/TB-72/nachweis9_register_numstat.txt`).
Abschnitt 25 angehängt (25.1 Befund, 25.2 Instanz, 25.3 Ersatztext = Fables
Konjunktionssatz zeichengleich mit seiner Rücknahme als Herkunft, 25.4 Wirkung
mit dem F17-Satz, 25.5 was nicht getan wird, einfache Sprache); Marken *„(a)
ERSETZT durch Abschnitt 25"* in 15.6 und *„(b) ERSETZT durch Abschnitt 25"* in
21.3, je als angehängte Zeile — **kein bestehender Satz umgeschrieben, nichts
entfernt.**

## Nachweis 10 — `git diff --numstat 7b73584..HEAD` je Datei

`docs/belege/TB-72/nachweis10_numstat_7b73584_bis_schritt6.txt` (Stand nach
Schritt 6; Schritt 7 fügt dieses Dokument, den Journal-Nachtrag `(20k)`, eine
Backlog-Zeile und die Nachweis-8-Belege hinzu). **Nichts ausserhalb `docs/` und
`research/`** — gemessen: `awk '{print $3}' | grep -v '^docs/\|^research/'` leer.
Unter `research/` geändert: `vorregistrierung/faltenplan.py` (75/17),
`faltenplan_neun/erste_falte_trockenlauf.py` (28/5), `faltenplan_neun/BERICHT.md`
(20/0); neu: `faltenplan_neun/test_erste_falte_trockenlauf.py`,
`vorregistrierung/ergebnisse/faltenplan_tb72.json`,
`vorregistrierung/ergebnisse/benchmark_drawdowns_tb72.json`. `auswertung.py`,
`benchmark.py`, `registerdaten.py`, `faltenschranke_messung.py`,
`faltenplan_neun.py`, alle Bot-Dateien: **unverändert**. Die Wegwerf-Kopie
`research/_tb72_kopie/` (Nachweis 8) ist entfernt und war nie im Index.

---

## Was der Auftrag anders sah — und wo die Messung galt

| Auftrag | gemessen / getan |
|---|---|
| Schritt 3: Gegenüberstellung gegen `ergebnisse/faltenplan.json`, *„genau ein Bot, genau eine Falte"* | gilt gegen den **Speicherstand** vor TB-72 (Beleg aus Schritt 0); gegen die Datei weichen alle neun ab — TB-30a-Stand, bekannt (`K4k`) |
| Schritt 3: *„genau eine Falte"* | eine entfallene Falte **plus** acht Folgeänderungen an `embargo_nach_falten` — keine zweite Änderung; die erste Skriptfassung hatte sie mitgezählt |
| Schritt 2: *„Ändere nichts anderes an `faltenplan.py`"* | der Modulkopf (Regel 2/3) musste mit, weil er *„das rechnet dieses Modul nicht"* sagte; zwei neue Plan-Felder, damit die Herkunft im Plan steht. Faltenlänge, Purge, Embargo, Schnitt unberührt |
| Schritt 2: *„`erste` kommt aus dem Trockenlauf"* | aus der **Konjunktion** — Fables Neufassung, nicht der Wortlaut vor dem HALT (der 1967 ergäbe) |
| Schritt 5: `test_vorregistrierung.py` **oder** neben `faltenschranke_messung.py` | daneben; Begründung in Nachweis 7 |
| Nachweis 8 erwartet *„163 bestanden, 2 gescheitert, G6 und H3"* in der Kopie | **trifft** — 163/2, dieselben zwei |
| Nachweis 3 nennt `ergebnisse/…` | `research/vorregistrierung/ergebnisse/` |
| Abschnitt 4: *„sieben Commits"* | acht — Schritt 0 als eigener Zwischencommit für Betreiber-Dateien (Muster TB-68/TB-71), Schritt 7 in einem |

---

## Offen

| | wer |
|---|---|
| ⛔ **Vollzug der Sperrlisten-Änderung** (Register 21.9, Betreiberfreigabe): die neue registrierte Tabelle wäre `benchmark_drawdowns_tb72.json` (nicht mehr `_vt`), der Plan `faltenplan_tb72.json`; `registerbericht.py:178` dabei nachziehen (23.5) | Betreiber |
| ⚠️ **TB-74** — Bedingung (i) präzisieren (`asof` minus `RECENT_YEARS_ONLY`, Datenuhr; `entry_cutoff` je Symbol gegen `fensteranker` je Markt). Für `t3_supertrend` ohne Wirkung | eigener Auftrag |
| Laufzeit `faltenplan()` +25 s je Prozess (Nachweis 8: Teil H sechsmal) — erst messen, ob es stört; ein Zwischenspeicher neben dem Plan wäre eine Konstantenkopie durch die Hintertür | TB-30b |
| `AKTUELLER_AUFTRAG.md`: TB-72-Zeile auf „erledigt" (Betreiberdokument) | steuernder Chat |
| Journal-Nachtrag `(20k)` einarbeiten (Block nach `BT`, hinter `(20g)`–`(20j)`); Projektablage (`K4e`) | nächste Einarbeitung |

---

## Commit-Liste dieser Sitzung

| Commit | Schritt | Inhalt |
|---|---|---|
| `96cc9c7` | 0 | Betreiber-Dateien (Fable-Antwort e, ERLEDIGT-Nachtrag, TB-74-Zeile, ARBEITSWEISE) — nicht von dieser Sitzung geschrieben |
| `e7a4108` | 2 | `faltenplan.py`: `erste_falte` = Konjunktion, `erste_falte_4a`; `erste_falte_trockenlauf.py`: Falte für Falte |
| `edd1bce` | 3 | `faltenplan_tb72.json` daneben, Gegenüberstellung |
| `27c58a2` | 4 | `benchmark_drawdowns_tb72.json` daneben, Gegenprobe acht Bots, `t3_supertrend`, `rsi2_crypto`-Nachmessung |
| `814c2c5` | 5 | `test_erste_falte_trockenlauf.py` (50/50), Mutation 38/12, `BERICHT.md`-Nachtrag |
| `b5a1a80` | 6 | Register Abschnitt 25, Marken in 15.6 und 21.3 (220/0) |
| *(dieser)* | 7 | dieses Dokument, Journal-Nachtrag `(20k)`, Backlog `K4l`, Nachweis-8-Belege |

---

## In einfacher Sprache

**Was wir wollten:** Einen Bot berichtigen, der ein Jahr führte, in dem er
nichts handeln konnte — und den Rechenweg abschaffen, der das übersehen hat.

**Was herauskam:** Der Bot beginnt 2019 statt 2018. Alle anderen acht bleiben
Zahl für Zahl, wie sie waren — das ist geprüft über 6 900 Einzelwerte. Seine
Verlustgrenze wird etwas weiter, von −45,2 auf −48,1 Prozent bei voller
Investition, genau wie eine frühere Rechnung es vorausgesagt hatte.

**Was jetzt anders ist:** Der Plan fragt das Programm selbst, ab wann es handeln
darf, und zählt ein Jahr nur, wenn Daten **und** Programm es tragen. Ein Test
setzt die alte Nachrechnung künstlich wieder ein und wird dabei rot — so ist
belegt, dass er den Unterschied sieht. Im Regelwerk steht der neue Satz mit
seiner Herkunft; die alten bleiben als ersetzt stehen.

**Was nicht passiert ist:** Keine gesperrte Datei ist angefasst, kein Tag
gesetzt. Ob die neuen Tabellen die alten ablösen, entscheidet der Betreiber.
