# TB-77 Schritt 1 — die beiden Blocker nachgemessen (21.09.2026, Mac)

Stand `2e9cdf9` (nach Schritt 0). Alle Suchen ohne `trading-env/` und `.git/`.

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-77_horizont_je_bot.md
```

Beides Betreiber-Dateien, committet in `9250570` (Schritt 0). Während Schritt 1
kam `docs/projektfuehrung/FABLE_UEBERGABE_2026-09-21_neuer_chat.md` hinzu
(Betreiber, mtime 16:29), getrennt committet in `2e9cdf9`.

## Nachweis 2 — Blocker A: ist `asof` irgendwo als Wert gesetzt?

| # | Ort | Befehl / Methode | Ergebnis |
|---:|---|---|---|
| A1 | alle `*.py` im Repo | `grep -rn --include='*.py' "asof"` | **8 Zeilen, alle `merge_asof`** (pandas; `research/drawdown_reihenfolge/adapters.py:232`, `engine.py:30`, `research/vbc_deepdive/regime.py:77,95`, `test_vbc_core.py:356`, `strategies/{volatility_breakout_crypto,rsi2_crypto,t3_supertrend}/regime_filter.py:36/40/40`) — kein Bezugsdatum |
| A2 | alle `*.json` im Repo | `grep -rln --include='*.json' "asof"` | **1 Datei**, `research/backtest_defaults/results/default_scan.json`: der Eintrag `"pandas.py:merge_asof"` in einer Aufrufliste — kein Wert |
| A3 | das Register `docs/VORREGISTRIERUNG_neuselektion.md` | `grep -n "asof"` | **3 Zeilen**: Z. 2190 und 2209 (Abschnitt **17.1**, Registertext 5a: *„Das Bezugsdatum des Laufs (`asof`) kommt aus dem Register, nie aus der Uhr"* und die Erläuterung dazu), Z. 4123 (25.3, Tatsachennotiz: Fables Präzisierung ist TB-74). **Keine Zahl, kein Datum** |
| A4 | `research/vorregistrierung/ergebnisse/` (8 JSON) | `grep -rl "asof"` | **0 Dateien** |
| A5 | Snapshot-Manifest `snapshots/63e4b6c8…/MANIFEST.json` | Schlüssel gelesen (`python3 json.load`) | 15 Schlüssel: `bytes_gesamt, dateien_gesamt, datenstand_hash, eingabeliste, kursdateien, quelle, snapshot_hash, teilkerzen, verfahren, werkzeug, wurzel, zeitpunkt_utc, zugelassene_befunde*` — **kein `asof`**. `zeitpunkt_utc` = `2026-09-19T06:49:32+00:00` ist der Ziehzeitpunkt, kein registriertes Bezugsdatum |
| A6 | `research/vorregistrierung/registerdaten.py` | `grep -n -i "asof\|bezugsdatum"` | **0 Treffer** |
| A7 | `docs/` (alle `*.md`) | `grep -rln "asof"` | 11 Dateien; die Zeilen mit `=`/`:`/Datum geprüft: **alle nennen `asof` als Grösse oder Formel** (`asof (5a) minus RECENT_YEARS_ONLY`), **keine trägt einen Wert** |
| A8 | `*.txt, *.csv, *.yaml, *.yml, *.toml, *.cfg, *.ini, *.env*` | `grep -rl` | **0 Dateien** |
| A9 | Umgebung, `.env` | `env \| grep -ic asof`; `.env` | 0; keine `.env` vorhanden |

**Befund A: `asof` ist nirgends als Wert gesetzt.** Das deckt sich mit der
Messung des steuernden Chats (21.09., 16:25). Zwei Ergänzungen, die der Auftrag
nicht hat:

1. ⚠️ **Die Fundstelle im Auftrag ist falsch:** der Satz *„kommt aus dem
   Register, nie aus der Uhr"* steht in **17.1** (Registertext 5a, TB-48), nicht
   in 16.3. 16.3 (a) ist die **ersetzte** Fassung (Z. 1628–1640, Vermerk
   *„ERSETZT durch Abschnitt 17"*) und enthält das Wort `asof` nicht. Das
   Aktenzeichen **5a** im Auftrag ist richtig.
2. ⭐ **Das einzige Datum, das einem Horizontbeginn ähnelt, steht in 15.6,
   Punkt 3** (Registertext 4, Tatsachennotiz vom 15.09.): *„`RECENT_YEARS_ONLY
   = 10`, gemessen vom letzten Kurstag (2026-09-01) zurück auf 2016-09-01 — so
   rechnen die vier Aktien-Bots selbst."* Das ist die **Datenuhr** (letzter Kurs
   im Bestand), nicht `asof`; es ist kein registriertes Bezugsdatum und wird
   hier **nicht** als solches verwendet. Es ändert den Schnitt nicht.

## Nachweis 3 — Blocker B: ist `auswertung.py` eingefroren, und wo steht das?

| Fundstelle | Wortlaut |
|---|---|
| Register **Z. 29–31** (Abschnitt 0) | *„Das Skript, das aus den Rohergebnissen die Auswahl und die Bleibt-Geht-Liste berechnet, ist vor dem Lauf geschrieben und eingefroren: `research/vorregistrierung/auswertung.py`."* |
| Register **15.8 Nr. 3** (Z. 1419–1424) | *„die Datei ist eingefroren und wurde nicht angefasst. Ihre Umstellung ist TB-30b."* |
| Register 24.5 (Z. 3835) | *„`auswertung.py` ist eingefroren (15.8 Nr. 3, TB-30b) und bleibt es, auch ihr Docstring"* |
| Register 25.5 (Z. 4181) | *„`auswertung.py` eingefroren (15.8 Nr. 3)"* |
| Sperrliste Abschnitt 10, Nr. 5 | *„Abbruchkriterien und Kapitalregel — `auswertung.py`"* |
| Docstring der Datei selbst, Z. 3 | *„TB-30a - Das eingefrorene Auswertungsskript"* |

**Befund B bestätigt.** Eine Wache im Auswerter ist heute nicht eintragbar,
ohne die eingefrorene Datei zu öffnen.

## Nebenbefund — Fables Antwort vom 21.09. liegt nicht im Repo

Der Auftrag zitiert `FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md`.
`find` über das Repo: **0 Treffer**; nur die Anfrage
(`FABLE_ANFRAGE_2026-09-21a_…`, `5a1f5e1`) liegt vor. Die Anfrage bat Fable,
die Antwort selbst in der Projektablage abzulegen; `FABLE_UEBERGABE_2026-09-21_neuer_chat.md`
Z. 9 sagt, sie *„kam als Datei zurück"* — abgelegt ist sie nirgends im Repo.
**Träger des Wortlauts im Repo ist damit allein Abschnitt 0 des Auftrags**
(und, als Paraphrase, `FABLE_UEBERGABE…` §3 (d)). Der Registertext in 26.2 wird
zeichengleich aus dem Auftrag übernommen und nennt diese Herkunft.

## Nachweis 4 — die beiden Festlegungsnummern, selbst nachgemessen

`registerdaten.FESTLEGUNGEN` (dict, 12 Einträge), gelesen mit `python3`:

```
10 ('DSR-Basis', 'N = 653, dieser Lauf zaehlt dazu')
11 ('DSR ist Bericht, nicht Tor', 'Bleibt-Geht laeuft ueber die Abbruchkriterien')
12 ('Das zulaessige Ergebnis', 'Es kann sein, dass kein einziger Bot die Schwelle erreicht. …')
```

Registertabelle Abschnitt 1 (Z. 56–58): 10 DSR-Basis N = 653 · 11 „DSR ist
Bericht, nicht Tor — Bleibt-Geht läuft über die Abbruchkriterien" · 12 „Das
zulässige Ergebnis — wörtlich". **Beide Berichtigungen des Auftrags treffen:**
Bleibt/Geht über die Abbruchkriterien ist **11**, nicht 10; „mehrere oder alle"
deckt **12** (und, als Verfahrensregel für mehrere Ausfälle, 7.1), nicht 11.

## Nachweis 5 — Abbruchkriterium (b) und Registertext 6 (b)

| | Fundstelle | Wortlaut |
|---|---|---|
| Abbruchkriterium **(b)** | Register Abschnitt 7, **Z. 686** | *„(b) Kein Parametersatz erfüllt die Drawdown-Bedingung in allen Falten"*; Präzisierung Z. 692–694 (*„Ist keiner zulässig, greift (b); berichtet wird dann der Plateau-Gewinner über alle Zellen, ausdrücklich mit der Markierung ‚nicht zulässig'"*) |
| Folge bei Ausfall | Register 7.1, **Z. 714–720** | Kapital in die statische Benchmark-Position; Bot läuft als Schatten weiter; Rückkehr nur über einen neuen vorregistrierten Lauf; kein „vorerst behalten" |
| Registertext **6 (b)** | Register 16.4, **Z. 1707–1711** | *„Nach dem Selektionslauf steht jeder Bot, der kein Abbruchkriterium erfüllt, auf Grundbudget; jeder, der eines erfüllt, auf Schatten — sein Budgetanteil hält die statische Benchmark-Position in Höhe seines mittleren Exposures. Die Zuweisung ist Ergebnis des eingefrorenen Skripts, keine Lesung."* |
| Rückkehr | Registertext 6 (d), Z. 1724–1725 | *„Rückkehr nur über einen neuen registrierten Lauf."* |

⚠️ Das Aktenzeichen „6b" gibt es im Register **nicht als Überschrift** — es
ist Registertext 6, Buchstabe (b), in 16.4. `grep -c "Registertext 6b"` = 0.

## Nachweis 6 — kam die 4a-Fassung vom 20.09. je in einen Registertext?

Gesucht im Register (`grep -c`): `Horizontbeginn` **0** · `4a, Präzisierung`
**0** · `Im Datenhorizont" heisst` **0** · `RECENT_YEARS_ONLY` 3 Zeilen (15.6
Punkt 3 als Datenuhr-Tatsachennotiz; 25.3 und 25.5 verweisen die Präzisierung
ausdrücklich an **TB-74**). **Die Fassung vom 20.09. wurde nie Registertext.**
Ausserhalb der Fable-Dateien und dieses Auftrags: `Horizontbeginn` in `docs/`
**0** Zeilen.

## Nachweis 8 (vorher) — Sperrlisten-Hashes

```
a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee  benchmark_drawdowns.json
0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339  faltenplan.json
```

## Fundstellen für 26.1, nachgemessen (Stand `2e9cdf9`)

| Bot | `RECENT_YEARS_ONLY = 10` | `df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)` |
|---|---:|---:|
| `elliott_wave_stocks` | Z. 54 | Z. 93 (`cutoff`; Z. 94 kappt die Kursreihe des Symbols selbst) |
| `rsi2_mean_reversion` | Z. 52 | Z. 93 (`entry_cutoff`, Z. 96 `data[symbol] = (df_ind, entry_cutoff)`) |
| `turtle_soup_stocks` | Z. 46 | Z. 81 (Z. 83 `data[symbol] = (df, entry_cutoff)`) |
| `volatility_breakout` | Z. 49 | Z. 88 (Z. 91 `data[symbol] = (df_ind, entry_cutoff)`) |

Alle vier innerhalb der Ladeschleife `for symbol in SYMBOLS` — **je Symbol**.
`research/faltenplan_neun/faltenplan_neun.py::fensteranker` Z. 271, Docstring
Z. 272–278: *„Genommen wird der SPAETESTE letzte Kurstag des Marktes, damit
alle Symbole desselben Bots auf demselben Fenster liegen."* — **je Markt**.
Die Zeilenangaben des Auftrags (54/52/46/49, 93/93/81/88, 271–278) treffen.

## Grundlage für 26.5 — die Ergebnisdateien der vier Aktien-Bots

`results/<bot>/multi_symbol_optimisation_results.csv`, je genau ein Commit,
seitdem unverändert (`git log` je Datei); im selben Commit steht der
Optimierer bereits mit der Je-Symbol-Rechnung (`git show <commit>:…` zählt
`DateOffset(years=RECENT_YEARS_ONLY)` je 1×), und `git log -S` findet keinen
älteren Stand des Ausdrucks:

| Bot | Datei-Commit | Optimierer je Symbol seit |
|---|---|---|
| `elliott_wave_stocks` | `0f6491b` 2026-09-02 | `0f6491b` |
| `rsi2_mean_reversion` | `f56c6d2` 2026-09-03 | `f56c6d2` |
| `turtle_soup_stocks` | `88b9050` 2026-09-04 | `88b9050` |
| `volatility_breakout` | `b603861` 2026-09-03 | `b603861` |
