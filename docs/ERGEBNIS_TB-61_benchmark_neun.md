# ERGEBNIS TB-61 — Benchmark-Tabelle für alle neun Bots, Lauf daneben (Mac-Lauf, 20.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-61_benchmark_neun.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `c493b1b`, Interpreter durchgehend
`trading-env/bin/python3` = **Python 3.9.6**, Kursdateien `data/` = **223**
(gezählt, `ls data | wc -l`). Vier Arbeits-Commits, jeder einzeln gepusht:
**`3c3e2c8`** (Schritt 0), **`d1b2175`** (Schritt 2), **`3d46a7b`**
(Schritt 3), **`b29f695`** (Schritt 4 und 5); dieses Dokument und der
Journal-Nachtrag folgen als fünfter. Kein Zweig, kein PR, keine ZIP. Rohausgaben
der Läufe liegen unter `docs/belege/TB-61/`.

---

## ⚠️⚠️ Das wichtigste Ergebnis zuerst: der Test bleibt rot — und darf es nach dieser Aufgabe nur so

**Nachweis 7, gemessen:** `trading-env/bin/python3
research/vorregistrierung/test_vorregistrierung.py` bricht **weiterhin** in
Teil A mit

```
File ".../auswertung.py", line 237, in zulaessigkeit
    falte = eintrag["falten"][z["falte"]]
KeyError: '2017'
```

ab. **Der Grund ist gemessen, nicht erschlossen:** `test_vorregistrierung.py:82`
lädt `ergebnisse/benchmark_drawdowns.json` — **die gesperrte Datei**, die diese
Aufgabe nach Register 21.9 byteweise unverändert lassen muss (Nachweis 2:
gehalten). Der Plan für `turtle_soup_stocks` beginnt seit TB-56 bei 2017, die
gesperrte Tabelle bei 2019. **Solange das Amendment nicht vollzogen ist, kann
kein Lauf diesen Test grün machen, ohne die Sperre zu brechen.**

⇒ Die Registerangabe in 21.9 — *„offen durch eigene Änderung — blockierend für
den Tag"* — ist **nicht überholt**. Sie gilt unverändert weiter.

**Was zusätzlich gemessen wurde — in einer Wegwerf-Kopie, nicht im Repo:** Der
Ordner `research/vorregistrierung/` wurde nach `research/_tb61_kopie_…/` kopiert
(untracked, danach entfernt), dort die neue Tabelle **an die Stelle** der
gesperrten gelegt (SHA-256 der Kopie `e06812d2…`, des Originals unverändert
`a163c498…`), und der Test dort gestartet:

| Lauf | Ergebnis |
|---|---|
| **im Repo** (gesperrte Tabelle), 11:25 UTC | ⚠️ **Abbruch in Teil A, `KeyError: '2017'`** — 0 Prüfungen gezählt |
| **in der Kopie** (neue Tabelle an der Stelle der gesperrten), 11:35–11:45 UTC, 9 min | **163 bestanden, 2 GESCHEITERT** — Teil A bis G laufen durch, der `KeyError` ist **in dieser Konstellation weg**. Die zwei Roten sind **neu und beide erklärt**: |
| ↳ **G6** `elliott_wave` | prüft `"2020" in namen and "2022" in namen`; die Falten heissen `2020-2021` und `2022-2023` (Doppeljahr). Bis heute erreichte kein Doppeljahr-Bot G6, weil Krypto Platzhalter war (G5) |
| ↳ **H3** (Mutationsprobe) | setzt **vier** Falten ohne Trade und erwartet, dass der Median sich verschiebt — gebaut für **sieben** Selektionsfalten. `turtle_soup_stocks` hat seit TB-56 **neun**: vier Nullen unter neun bewegen den Median nicht (`0.1000` / `0.1000`), die Probe beisst nicht mehr. Unabhängig von TB-61, sichtbar erst jetzt |

⇒ **Nach dem Amendment wird der Test aus zwei neuen Gründen rot**, beide in
`test_vorregistrierung.py` selbst, keiner in der Rechnung. Beide gehören
**vor** das Amendment (Aufgaben des Betreibers, unten). ⚠️ Ein erster
Kopie-Versuch **ausserhalb** des Repos scheiterte in Teil H komplett
(`No module named 'manual_close'`): `_umgebung()` leitet `TB30A_BASE_DIR` aus
dem Ort der Kopie ab; die Kopie muss zwei Ebenen unter der Repo-Wurzel liegen.
Rohausgaben: `docs/belege/TB-61/nachweis7_*.txt`.

---

## ⚠️⚠️ Drei Befunde über den Auftrag hinaus — jeder verlangt eine Betreiberentscheidung, keiner ist hier entschieden

### Befund 1 — die Krypto-DD_Toleranz ruht auf leeren Falten (`MINDESTTRAINING_JAHRE = 4`)

**Gemessen:** Das point-in-time-Universum des Krypto-Benchmarks
(`benchmark.py:181–183`, `point_in_time(…, rd.MINDESTTRAINING_JAHRE)`, Wert
**4** aus `registerdaten.py:108`) ist in den Falten **2018, 2019, 2020 und 2021
leer** — frühester Krypto-Datenbeginn ist **2017-08-17** (BTC/ETH), plus vier
Jahre = 2021-08-17, also erst in der Falte **2022** drei Symbole, 2023 sechs,
2024 neun, 2025 dreizehn.

| Bot | Selektionsfalten | davon **leer** (0 Symbole, 0 Handelstage) | DD_Toleranz 25 / 50 / 100 % **wie gerechnet** |
|---|---:|---:|---|
| `elliott_wave` | 4 | **2** (2018–2019, 2020–2021) | −6,07 / −11,89 / −22,42 |
| `t3_supertrend` | 8 | **4** (2018–2021) | −3,24 / −6,32 / −12,01 |
| `rsi2_crypto` | 7 | **3** (2019–2021) | −6,48 / −12,64 / −24,02 |
| `turtle_soup_crypto` | 8 | **4** (2018–2021) | −3,24 / −6,32 / −12,01 |
| `volatility_breakout_crypto` | 8 | **4** (2018–2021) | −3,24 / −6,32 / −12,01 |

⚠️ **Die Zahlen sind so gerechnet, wie der Code es heute definiert**
(`drawdown_bei_exposure()` liefert für eine leere Reihe `0.0`; der Median läuft
nach Festlegung 5 über **alle** Selektionsfalten). Dass die Hälfte der Falten
mit 0,00 eingeht, macht den Median zum Mittel aus einer echten Zahl und einer
Null — **die Toleranz der fünf Krypto-Bots ist damit vor der Entscheidung zu
`MINDESTTRAINING_JAHRE` nicht belastbar.** Das ist genau die Verfahrensfrage aus
Abschnitt 6 des Auftrags, nur ist sie nicht meldepflichtig, sondern
**ergebnisbestimmend**.

**Nachrichtlich, keine Entscheidung** — derselbe Median **nur über die
nicht-leeren Falten**, gerechnet aus den Faltenwerten der neuen Datei:

| Bot | nicht-leere Falten | 25 % | 50 % | 100 % |
|---|---:|---:|---:|---:|
| `elliott_wave` | 2 | −16,81 | −31,59 | −55,30 |
| `t3_supertrend`, `rsi2_crypto`, `turtle_soup_crypto`, `volatility_breakout_crypto` | 4 | −11,31 | −21,93 | −40,94 |

⚠️ **Und der Lauf brach daran zunächst ab.** Erster Lauf 11:21 UTC:
`TypeError: '>=' not supported between instances of 'numpy.ndarray' and
'Timestamp'` in `je_bot()` — `bh_tagesrenditen({})` liefert eine leere Reihe
**ohne Zeitindex**, und die Fensterfilterung verglich diesen Index mit einem
Zeitstempel. **Abweichung von „Nur der Schalter", ausdrücklich benannt:** In
`je_bot()` steht jetzt die kleinste Wache, die den Lauf durchlässt — eine leere
Reihe geht **unverändert** an `drawdown_bei_exposure()` weiter, das dafür schon
`0.0` definiert (Commit `b29f695`, numstat `8 1`; die eine entfernte Zeile ist
die Filterzeile, die jetzt im `else`-Zweig steht). **Keine der vier gesperrten
Rechenfunktionen und nicht die Medianbildung ist angefasst.** Die Alternative
wäre gewesen, gar keine Tabelle abzuliefern.

**Die zwei Fundstellen aus Abschnitt 6 des Auftrags, nachgemessen:**
`research/vorregistrierung/registerdaten.py:108` `MINDESTTRAINING_JAHRE = 4`
(benutzt in `benchmark.py:183`) und `research/etf_trendfolge/register.py:347`
`FALTEN_MINDESTTRAINING = None`. Ob Widerspruch oder zwei Dinge: **nicht
entschieden**, wie verlangt.

### Befund 2 — `t3_supertrend`: die neue Tabelle hat 8 Falten, Register 21.4 nennt 7

**Gemessen:** Die Regel, nach der `plan_aktien()` die erste Falte rechnet
(`erste_falte()` = Registertext **4a**, Kursdaten am 1. Januar), ergibt für
`t3_supertrend` **2018**. Register 21.4 nennt **2019** und begründet das mit
Registertext **3b (a)**: `MIN_HISTORY_DAYS = 730` macht in der Falte 2018 kein
Symbol handelbar (Trockenlauf: 0 Symbole), und nach **21.3 (b)** bindet dann
3b (a). ⚠️ **Diese Bindungsregel steht im Register, aber in keinem Code:**
`plan_aktien()` rechnet nur 4a — bei den vier Aktien-Bots fällt das nicht auf,
weil dort 4a und 3b (a) dasselbe Jahr liefern (TB-56, Spalten A und H gleich).
Der Auftrag verlangt für `plan_krypto()` *„dieselbe Regel"*; genau das ist
umgesetzt, und genau das erzeugt die Abweichung.

| | erste Falte | Selektionsfalten | DD_Toleranz 25 / 50 / 100 % |
|---|---|---:|---|
| **neue Tabelle** (4a, wie `plan_aktien`) | 2018 | 8 | −3,24 / −6,32 / −12,01 |
| **Register 21.4** (3b (a) bindet) | 2019 | 7 | *nachrichtlich, aus denselben Faltenwerten:* −6,48 / −12,64 / −24,02 |

Der Unterschied kommt allein daher, dass die leere Falte 2018 mitzählt (Befund
1). **Nicht entschieden**, ob 21.3 (b) in `faltenplan.py` gehört und woher der
Code die 3b (a)-Falte nähme (der Trockenlauf ist nach Registertext 3b das einzig
zulässige Werkzeug; seine Messung liegt in
`research/faltenplan_neun/daten/faltenplan_ohne_schranke.json`,
`trockenlauf_3b.je_bot`). Der Modulkopf von `faltenplan.py` (Regel 3) benennt
die Lücke.

### Befund 3 — Schritt 1 des Auftrags hätte zum Abbruch geführt, und der Abbruch wäre falsch gewesen

**Gemessen (Nachweis 3, Tabelle unten):** `faltenplan_neun.py` trägt auf der
Platte noch `FRUEHESTE_FALTE = 2019` (Zeile 120 — der Auftrag nennt sie selbst
in Abschnitt 5 als *„eigene Aufgabe"*). Seine Spalte **„1. Falte"** lautet
deshalb **neunmal 2019** und trifft die Tabelle in Abschnitt 0 bei **2 von 9**
Bots. Seine Spalte **„ohne Schranke"** (4a) trifft **8 von 9**; die eine
Abweichung ist `t3_supertrend` (Befund 2). Beides sind **keine** Abweichungen
zwischen Register und Werkzeug — beide haben exakt den Stand, den der Auftrag
gemessen hat (`faltenplan_ohne_schranke.json` bestätigt jede Zahl). Die Tabelle
in Abschnitt 0 ist die **3b (a)**-Tabelle aus 21.4; das Werkzeug rechnet
**4a**. Der Auftrag vergleicht zwei verschiedene Lesarten und deutet die
erwartbare Differenz als Befund. **Deshalb nicht abgebrochen** (Auftrag
Abschnitt 4: *„Widersprich diesem Auftrag, wo er falsch ist"*), sondern
gemessen, hier festgehalten und weitergemacht.

---

## Die acht Nachweise

| # | Nachweis | Ergebnis |
|---:|---|---|
| **1** | `git status --short` vor dem ersten Schreiben | ` M docs/projektfuehrung/ARBEITSWEISE.md` — **eine** Zeile, 48 unkommittierte Zeilen (neuer Unterabschnitt zu den Kopierblöcken, mit der Berichtigung 13:10). Nach Schritt 0 als `3c3e2c8` gesichert, inhaltlich unverändert; danach `git status --short` **leer** ✅ |
| **2** ⭐ | SHA-256 `benchmark_drawdowns.json` nach der Aufgabe | **`a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee`** — gemessen **viermal**: vor dem ersten Schreiben, nach dem abgebrochenen ersten Lauf, nach dem Lauf, vor diesem Dokument. Zweite Zählung: `git status` nennt die Datei nie; letzter Commit unverändert `a2fcf01` ✅ **Die Sperre hat gehalten** |
| **3** | Neun Faltenpläne aus Schritt 1 gegen Abschnitt 0 | Tabelle unten — **2/9** mit Schranke, **8/9** ohne; Abweichung `t3_supertrend`, erklärt in Befund 2 und 3 |
| **4** | `git diff --numstat` je Datei | `benchmark.py` **14 2** (`d1b2175`) + **0 11** (`3d46a7b`) + **8 1** (`b29f695`) = gesamt **22 14**; `faltenplan.py` **31 54** (`3d46a7b`); `benchmark_drawdowns_neu.json` **9485 0** neu (`b29f695`); dazu `ARBEITSWEISE.md` **48 0** aus Schritt 0 (vorgefunden, nicht von dieser Sitzung geschrieben) |
| **5** ⭐ | Vergleich alt → neu, neun Bots, drei Stufen | Tabelle unten. **Alle vier Vorhersagen aus 21.6 treffen auf die Stelle** |
| **6** | `status` je Bot in der neuen Datei | **neunmal `endgueltig`** (gezählt aus der Datei) ✅ |
| **7** ⭐ | Test je Testdatei; ist der `KeyError: '2017'` weg? | ⚠️ **Nein** — siehe oben. Es gibt in `research/vorregistrierung/` **eine** Testdatei (`test_vorregistrierung.py`); `pytest` ist in `trading-env` **nicht installiert** (`No module named pytest`), und die Datei ist ein Skript mit `main()`, kein pytest-Modul — sie wurde wie in TB-56 direkt gestartet |
| **8** | Nichts ausserhalb `research/vorregistrierung/` und `docs/` | `git diff --name-only 3c3e2c8..HEAD` ausserhalb dieser Pfade: **0** ✅ (Schritt 0 liegt in `docs/`) |

---

## Nachweis 3 — Schritt 1: `faltenplan_neun.py` gegen die Tabelle in Abschnitt 0

Lauf 11:12 UTC, 12,5 s, rc 0. Zweite, unabhängige Zählung: `fp.erste_falte()`
aus `research/vorregistrierung/faltenplan.py` (die Regel von `plan_aktien`) und
die TB-56-Messung `faltenplan_ohne_schranke.json` (Spalten A und H).

| Bot | Abschnitt 0 (= Register 21.4) | `faltenplan_neun.py` **mit** Schranke (Platte) | **ohne** Schranke (4a) | `fp.erste_falte()` (4a) | TB-56 Spalte H (3b (a)) | Treffer 4a |
|---|---|---|---|---|---|---|
| `elliott_wave` | 2018–2019, 4 | 2019–2020, 3 | 2018, 4 | 2018, 4 | 2018–2019 | ✅ |
| `t3_supertrend` | 2019, 7 | 2019, 7 | **2018, 8** | **2018, 8** | **2019** | ❌ |
| `rsi2_crypto` | 2019, 7 | 2019, 7 | 2019, 7 | 2019, 7 | 2019 | ✅ |
| `turtle_soup_crypto` | 2018, 8 | 2019, 7 | 2018, 8 | 2018, 8 | 2018 | ✅ |
| `volatility_breakout_crypto` | 2018, 8 | 2019, 7 | 2018, 8 | 2018, 8 | 2018 | ✅ |
| `elliott_wave_stocks` | 2017, 9 | 2019, 7 | 2017, 9 | 2017, 9 | 2017 | ✅ |
| `rsi2_mean_reversion` | 2018, 8 | 2019, 7 | 2018, 8 | 2018, 8 | 2018 | ✅ |
| `turtle_soup_stocks` | 2017, 9 | 2019, 7 | 2017, 9 | 2017, 9 | 2017 | ✅ |
| `volatility_breakout` | 2018, 8 | 2019, 7 | 2018, 8 | 2018, 8 | 2018 | ✅ |

Die Spalte H stimmt mit Abschnitt 0 **9/9** überein — das Register hat den
gemessenen Stand. Die Spalte 4a stimmt mit der Regel von `plan_aktien` **9/9**
überein — das Werkzeug hat ihn auch.

---

## Nachweis 5 — der Vergleich: `benchmark_drawdowns.json` (gesperrt) → `benchmark_drawdowns_neu.json`

Lauf 11:23 UTC, 30,4 s, rc 0. DD_Toleranz je Bot, drei Exposure-Stufen.
„leer" = in der gesperrten Datei `platzhalter` mit leerer `dd_toleranz`.

| Bot | 25 % alt → neu | Δ | 50 % alt → neu | Δ | 100 % alt → neu | Δ | 21.6 vorausgesagt |
|---|---|---:|---|---:|---|---:|---|
| `elliott_wave` | leer → **−6,07** | neu | leer → **−11,89** | neu | leer → **−22,42** | neu | — (⚠️ Befund 1) |
| `t3_supertrend` | leer → **−3,24** | neu | leer → **−6,32** | neu | leer → **−12,01** | neu | — (⚠️ Befund 1, 2) |
| `rsi2_crypto` | leer → **−6,48** | neu | leer → **−12,64** | neu | leer → **−24,02** | neu | — (⚠️ Befund 1) |
| `turtle_soup_crypto` | leer → **−3,24** | neu | leer → **−6,32** | neu | leer → **−12,01** | neu | — (⚠️ Befund 1) |
| `volatility_breakout_crypto` | leer → **−3,24** | neu | leer → **−6,32** | neu | leer → **−12,01** | neu | — (⚠️ Befund 1) |
| `elliott_wave_stocks` | −2,18 → −2,18 | 0,00 | −4,33 → −4,33 | 0,00 | −8,55 → −8,55 | 0,00 | unverändert ✅ |
| `rsi2_mean_reversion` | −2,18 → **−3,35** | −1,17 | −4,33 → **−6,61** | −2,28 | −8,55 → **−12,89** | −4,34 | −3,35 / −6,61 / −12,89 ✅ |
| `turtle_soup_stocks` | −2,18 → −2,18 | 0,00 | −4,33 → −4,33 | 0,00 | −8,55 → −8,55 | 0,00 | unverändert ✅ |
| `volatility_breakout` | −2,18 → **−3,35** | −1,17 | −4,33 → **−6,61** | −2,28 | −8,55 → **−12,89** | −4,34 | −3,35 / −6,61 / −12,89 ✅ |

**Drei unabhängige Gegenproben an der neuen Datei:**

| Probe | Ergebnis |
|---|---|
| Median der Selektionsfalten je Bot, nachgerechnet aus den Faltenwerten der Datei (`np.median`, alle 100 Stufen) | **9/9 Bots, 100/100 Stufen gleich** der eingetragenen `dd_toleranz` |
| Aktien-Falten 2019–2026 gegen die **gesperrte** Datei (`dd_benchmark` alle 100 Stufen, `symbole_point_in_time`) | **4 Bots × 8 Falten, 0 Abweichungen** — die Rechenlogik hat sich nicht bewegt |
| Alle Aktien-Falten und `dd_toleranz` gegen die **TB-56**-Datei `benchmark_drawdowns_ohne_schranke.json` (dort unter `bots`) | **4 Bots, 9–10 Falten, 0 Abweichungen; `dd_toleranz` 100/100 gleich** — der Auftrag nannte die 21.6-Zahlen als *„mit einem anderen Werkzeug gerechnet"*; gemessen: dieselbe Rechnung, dieselben Zahlen |

Die Aktien-Werte je Falte (Symbole point-in-time / Handelstage / DD bei 100 %):
2017 135/251/−2,37 · 2018 136/251/−18,69 · 2019 137/252/−7,30 · 2020
137/253/−35,42 · 2021 139/252/−4,74 · 2022 139/251/−19,96 · 2023 140/250/−8,55 ·
2024 142/252/−6,86 · 2025 145/250/−17,23 · 2026 (Bestätigung) 147/166/−6,40.
Die Krypto-Werte je Falte: 2022 3/365/−65,76 · 2023 6/365/−24,02 · 2024
9/366/−33,31 · 2025 13/365/−48,56 · 2026 (Bestätigung) 13/243/−41,68; alle
Falten davor 0/0/0,00.

---

## Die Schritte, wie sie gelaufen sind

| Schritt | Commit | Was |
|---|---|---|
| **0** | `3c3e2c8` | `ARBEITSWEISE.md` (48 0) gesichert, unverändert übernommen. ⚠️ Der erste `git push` wurde vom Werkzeug-Klassifikator der Sitzung abgewiesen (*„Modify Shared Resources"*); der zweite, nach Schritt 2, ging durch und trug beide Commits. Alle weiteren Pushes sofort erfolgreich — **jeder allein, nie in einem `&&`-Block** |
| **1** | — | Messung, nichts geändert (Nachweis 3, Befund 3) |
| **2** | `d1b2175` | `benchmark.py`: `main(argv=None)` mit `argparse`, `--ziel`, Standard derselbe Pfadausdruck wie vorher. `--help` geprüft. Keine Rechenfunktion berührt |
| **3** | `3d46a7b` | `faltenplan.py`: `plan_aktien()` und `plan_krypto()` rufen eine gemeinsame `_plan(bot, mess, markt)`; `status` neunmal `endgueltig`; Platzhalter mit Regel **entfernt**, Modulkopf Regel 2 und 3 sagen, was ihn ablöst (TB-31, TB-34, Register 21) und was die Regel **nicht** rechnet (21.3 (b)). `benchmark.py`: Hinweistext *„haengt an TB-31"* und die Platzhalter-Zeile in `main()` entfernt — kein Bot mehr Platzhalter, also auch der Zweig weg |
| **4** | `b29f695` | Lauf mit `--ziel …/benchmark_drawdowns_neu.json`; erster Versuch `TypeError` (Befund 1), Wache eingesetzt, zweiter Lauf rc 0, 30,4 s. Neue Datei 187 660 Bytes, SHA-256 `e06812d2f5c26e73aee7265039e6b320b3de253837483c29e164ea07d404a062` |
| **5** | `b29f695` | Vergleich und drei Gegenproben (oben) |
| **6** | *dieser Commit* | dieses Dokument, Belege, Journal-Nachtrag |

---

## Beobachtungen, die NICHT ausgeführt wurden

| | Beobachtung | Warum liegen gelassen |
|---|---|---|
| ⚠️ | **`test_vorregistrierung.py` G6** prüft `"2020" in namen and "2022" in namen` — bei **Doppeljahr-Falten** (`elliott_wave`: `2020-2021`, `2022-2023`) schlägt das fehl, obwohl 2020 und 2022 Testfalten **sind**. Bis TB-61 erreichte kein Doppeljahr-Bot G6 (Krypto war Platzhalter, G5). In der Kopie gemessen (oben) | Teständerung ausserhalb des Auftrags; braucht eine eigene Aufgabe, **vor** dem Amendment, sonst ist der Test danach aus einem neuen Grund rot |
| ⚠️ | **`test_vorregistrierung.py` H3** (Probe „vier Falten ohne Trade") ist auf sieben Selektionsfalten gebaut und beisst bei neun nicht mehr — Folge von TB-56, nicht von TB-61. In der Kopie gemessen (oben) | wie G6: eigene Aufgabe vor dem Amendment |
| ⚠️ | `research/vorregistrierung/ergebnisse/faltenplan.json` (Stand `a2fcf01`, Krypto `platzhalter`, Aktien ab 2019) ist **überholt** und steht in `herkunft.py:57` auf der `EINGEFROREN`-Liste. Erzeugt von `faltenplan.py::main()`, das der Auftrag nicht aufruft | nicht beauftragt; gehört in das Amendment-Paket |
| | `faltenplan.py` und `benchmark.py` stehen in `herkunft.py:57` auf der `EINGEFROREN`-Liste. Der Tag ist nicht gesetzt (21.6: *„10.1 greift ins Leere"*) — keine Sperre gebrochen, hier nur benannt | — |
| | `registerbericht.py:145–146, 162` und `auswertung.py:327, 434, 458–461` und `beispieldaten.py:100, 209` tragen noch Zweige und Texte *„Platzhalter (TB-31)"*. Sie werden jetzt nie mehr betreten | Der Auftrag nannte nur die zwei Stellen in `benchmark.py`; Regel 9 des Dokumentationsstandards spricht für das Entfernen, aber in einem eigenen Zug |
| | `pandas` `FutureWarning` in `bh_tagesrenditen()` (`pct_change` `fill_method`), neunmal je Lauf. Rechenlogik, Sperrliste Punkt 6 | nicht angefasst |
| | `pytest` fehlt in `trading-env`; Nachweis 7 wurde per Skriptstart erbracht | Umgebungsfrage, `docs/UMGEBUNGEN.md` |
| | Die beiden Code-Kopien der Faltenschranke (`faltenplan_neun.py:120`, `krypto_historie/faltenplan.py:64`) sind unverändert — wie im Auftrag verlangt (`T56b.6`) | eigene Aufgabe |

---

## Was diese Aufgabe ausdrücklich NICHT getan hat

Die gesperrte Datei ersetzt · den Tag gesetzt · Registertexte geändert ·
`MINDESTTRAINING_JAHRE` angefasst · die Schranken-Kopien angefasst · den Test
geändert · irgendetwas ausserhalb `research/vorregistrierung/` und `docs/`
geändert.

---

## Aufgaben des Betreibers

| | |
|---|---|
| ⭐⭐ **1** | **Befund 1 entscheiden:** `MINDESTTRAINING_JAHRE = 4` für den Krypto-Benchmark — behalten (dann sind 3–4 von 7–8 Krypto-Falten leer und die Toleranz halb Null), auf 0/None wie `etf_trendfolge` (Verfahren B kennt keines), oder eine andere Regel. *Empfehlung:* an Fable, zusammen mit Befund 2, **vor** dem Amendment — beides sind Verfahrensfragen vor dem Tag, und das Amendment soll einmal geschehen, nicht zweimal |
| ⭐ **2** | **Befund 2 entscheiden:** ob 21.3 (b) in `faltenplan.py` gehört und woher der Code die 3b (a)-Falte nimmt. *Empfehlung:* ja, mit dem Trockenlauf-Ergebnis als Eingabe und einer Prüfung, die beide Lesarten ausweist |
| ⚠️ **3** | **G6 und H3 vor dem Amendment reparieren lassen** (Doppeljahr-Falten; Mutationsprobe auf neun statt sieben Falten), sonst ist der Test nach dem Amendment aus zwei neuen Gründen rot |
| **4** | Die Registerangabe 21.9 (*„blockierend für den Tag"*) bleibt stehen — **nichts zu tun**, hier nur bestätigt |

---

## In einfacher Sprache

**Was gemacht wurde:** Die Tabelle, die jedem Bot sagt, wie tief er fallen
darf, ist für alle neun Bots neu gerechnet — in eine **neue Datei daneben**. Die
alte, gesperrte Datei ist Byte für Byte dieselbe geblieben; das wurde viermal
nachgemessen. Für die vier Aktien-Bots kam **genau** das heraus, was das
Register vorhergesagt hatte: zwei bleiben gleich, zwei werden nachgiebiger
(bei voller Positionsgrösse von −8,55 auf −12,89 Prozent).

**Was nicht klappte, und warum das richtig ist:** Der rote Test ist **weiter
rot**. Er liest die gesperrte alte Datei, und die darf diese Aufgabe nicht
anfassen. Er wird erst grün, wenn du die neue Tabelle freigibst — und dann
gleich aus einem anderen Grund wieder rot, weil er mit den Zweijahres-Falten
des Elliott-Wave-Bots nicht rechnen kann. Das ist gemessen, nicht vermutet.

**Was du entscheiden musst:** Für die fünf Krypto-Bots verlangt der Code vier
Jahre Kursgeschichte, bevor ein Symbol in den Vergleichsmassstab eingeht. Die
Krypto-Daten beginnen aber erst 2017, also ist der Massstab bis 2021 **leer** —
die Hälfte der Auswertungsjahre trägt eine Null bei, und die Toleranz der
Krypto-Bots ist deshalb nur halb so streng, wie sie ohne die leeren Jahre wäre.
Ob die Vier-Jahres-Regel bleibt, ist deine Entscheidung (oder Fables); ich habe
sie nicht getroffen. Dazu ein zweiter, kleinerer Punkt: Ein Krypto-Bot bekommt
in der neuen Tabelle ein Jahr mehr, als das Register ihm zugesteht, weil eine
Registerregel („wenn der Loader kein Symbol handelbar macht, zählt das Jahr
nicht") in keinem Code steht.

**Was du bekommst:** Die neue Datei, den Vergleich alt gegen neu für alle neun
Bots, drei Gegenproben, die die Zahlen unabhängig bestätigen, und drei klar
benannte Entscheidungen — keine davon ist hier vorweggenommen.

*Ausgeführt am 20.09.2026 von der Mac-Sitzung TB-61. Vier Arbeits-Commits, alle
gepusht; dieses Dokument im fünften.*
