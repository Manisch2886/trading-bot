# Belege TB-56 — Herkunft

Sitzung **TB-56 Faltenschranke** (19.09.2026, Mac, `trading-env/bin/python3`
3.9.6), Auftrag `docs/auftraege/TB-56.md` (= `logs/auftraege/TB-56.md`,
byteweise gleich). Sicherungsordner
`~/Sicherungen/tb56_faltenschranke_20260919T180604Z/` (dort `kopien/` mit den
zwölf Datenbanken — Sicherung, kein Beleg). Ergebnisdokument:
`docs/ERGEBNIS_TB-56_faltenschranke.md`.

| Datei | Was sie belegt |
|---|---|
| `db_liste.txt`, `db_sha256_vorher.txt`, `db_vergleich_nachher.txt` | 12 `*.db` ausserhalb `trading-env/`, Quersummen vorher, `shasum -c` nachher |
| `datenstand_vorher.txt`, `datenstand_nachher.txt` | `snapshot.py --quelle data --nur-hash`: `d9449faf…`/223 |
| `snapshot_pruefen_vorher.txt`, `snapshot_pruefen_nachher.txt` | `snapshot.py --pruefen`: `UNVERAENDERT` |
| `registerpruefer_vorher.txt`, `registerpruefer_arbeitsbaum.txt`, `registerpruefer_nachher.txt` | `pruefe_register.py --basis a1e7fb4`: KEIN BEFUND vor jeder Änderung (A7), auf dem Arbeitsbaum, nach `7387cc5`; Quelle Beleg jeweils `trockenlauf` |
| `sperrklinken_vorher.txt`, `sperrklinken_nachher.txt` | `test_wanduhr.py` 6, `test_eigener_pfadbau.py` 29 — GRUEN |
| `basislauf_vorher_start.txt`, `basislauf_vorher.txt`, `basislauf_vorher.json` | Basislauf vor jeder Änderung: 61/5/1/3/1 = 71, UNERWARTET 0 |
| `basislauf_nachher_start.txt`, `basislauf_nachher.txt`, `basislauf_nachher.json` | Basislauf nach Teil B (siehe Ergebnisdokument, Nachweis 6) |
| `teil_a_messung.txt`, `teil_a_messung.json` | **Teil A**, rein lesend, vor jeder Änderung: je Bot erste Falte / Faltenzahl / Bestätigung / 4b mit und ohne Schranke, Kerzenzählung `elliott_wave`, Loader-Nachrechnung |
| `teil_a_plan_ohne_schranke.json` | der Plan ohne Schranke aus Teil A (Format `faltenplan_neun --json`); Vorlage von Nachweis 1 |
| `teil_a_trockenlauf.txt`, `teil_a_trockenlauf_ohne_schranke.json` | Trockenlauf des Laufcodes (TB-40) auf dem Plan ohne Schranke: H und F je Bot und Falte, `t3_supertrend` 2018 leer |
| `rueckfrage.md` | die **drei Rückfragen** an den Betreiber und seine Antworten, wörtlich |
| `teil_b_plan_schreiben.txt` | das Schreiben von `research/faltenplan_neun/daten/faltenplan_ohne_schranke.json` (mit Trockenlauf-Beilage) |
| `faltenplan_json_sha_vorher.txt` | SHA-256 von `daten/faltenplan.json` vor Teil B (`93fbf09c…`) |
| `vorregistrierung_ergebnisse_sha_vorher.txt` | SHA-256 der gesperrten `benchmark_drawdowns.json` und der `ergebnisse/faltenplan.json` vor Teil B |
| `benchmark_vergleich.txt` | gesperrte Benchmark-Tabelle gegen die neu gerechnete eigene Datei: Zeilen 2019–2026 zeichengleich, 2017/2018 neu, `DD_Toleranz` bei zwei Bots anders |
| `nachweise_1_3_4_8.txt` | Nachweise 1, 2, 3, 4 (a/b), 8 — 11/11 |
| `test_vorregistrierung_nachher.txt`, `test_faltenplan_neun_nachher.txt` | die beiden betroffenen Testdateien nach Teil B: Abbruch `KeyError: '2017'` (erwartet, Rückfrage 3) bzw. 145/145 |
| `skripte/nachweise.py` | Nachweise 1–4 und 8, gemessen |
| `skripte/benchmark_vergleich.py` | der Tabellenvergleich |

Das Messskript selbst ist versioniert:
`research/faltenplan_neun/faltenschranke_messung.py` (Teil A, Plan ohne
Schranke, Trockenlauf-Beilage, Mutationsgegenprobe).
