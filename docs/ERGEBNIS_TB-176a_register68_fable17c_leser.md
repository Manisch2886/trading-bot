# Ergebnis TB-176a — Register 68 (Fable 17c, R108, neun Marken, S-B1 Nachtrag 10a.5) und Leser auf `alle_trades` (E2)

**Sitzung:** Mac (Claude Code, Opus 5.5), 17.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-176a_register68_fable17c_leser.md` · **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9.6) · **Belege:** `docs/belege/TB-176a/`

**Commits (alle auf `main`, gepusht):**

| Schritt | Commit | Inhalt |
|---|---|---|
| S0 | `17648ad` | Fable 17.10.c (Anfrage, Antwort, Übergabe) und Stand des steuernden Chats vor TB-176a (Auftrag) |
| R | `53e8d54` | Register 68 (Fable 17c, R108), neun Marken, S-B1 Nachtrag 10a.5 |
| K | `9f95602` | Registerkopie, Index, Dialog-Index |
| E2 | `8465533` | Leser auf `alle_trades.csv` (`auswertung.py`, `embargo_neun.py`; R107 (e), R108 (c)) |
| A | dieser Commit | Ergebnis, BACKLOG, Journal FM |
| F | folgt | porcelain und numstat |

## Kurz

Alle Schritte liefen wie im Soll, ohne Abbruch und ohne Nachfrage. Fable 17.10.c liegt md5-gleich im Repo, R108 steht zeichengleich als Abschnitt 68 im Register, dazu kommen neun Marken und in S-B1 die Marke an 10a.2 und der Nachtrag 10a.5. Die Tatsachennotiz mit äusserer Quelle fehlt und ist **nicht eingetragen**. Registerkopie, Index und Dialog-Index sind nachgezogen, jeder Beleg endet mit rc 0. `auswertung.py` und `embargo_neun.py` lesen jetzt `<bot>_alle_trades.csv`: Probe 9 von 9, Test grün auf 3.9.6, `nachher2` 17/0. Am Handelscode hat sich nichts geändert, auf Kursdaten lief nichts.

## Schritt 0

0a: `0a gut (4 Eintraege)`; Holbefehl: vier Anhänge mit den Soll-sha256, `Dateien 4`. `0a_md5.txt` wörtlich:

```
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17c/FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md = nachher docs/projektfuehrung/FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md = a2b38226f683d8d106a5dec61fa5f325
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17c/FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md = nachher docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md = 0a559c880aa422ca0d77f03c5aa240bc
ja    md5 vorher data_sicherung/steuernder_chat_tmp/f17c/FABLE_UEBERGABE_2026-10-17c_eroeffnung.md = nachher docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17c_eroeffnung.md = db41d912f05314a47dcc0e501c3aed5a
Pruefungen: 3, NEIN: 0
rc 0
```

Nach S0 war `git status --porcelain` leer.

## Schritt V

`v_voraussetzung.txt` wörtlich:

```
ja    unveraendert: research/faltenplan_neun/embargo_neun.py md5 b93af1460411
ja    unveraendert: research/faltenplan_neun/test_faltenplan_neun.py md5 ae43038a02e7
ja    unveraendert: research/mtm_drawdown/grundlage.py md5 81cf1c93243a
ja    unveraendert: research/mtm_drawdown/messung.py md5 00eb23079f1b
ja    unveraendert: research/mtm_drawdown/test_mtm_kern.py md5 80f1511a18d2
ja    unveraendert: research/tb24_haltedauern/alle_bots.py md5 7bb90ef438d5
ja    unveraendert: research/tb24_haltedauern/auswertung.py md5 c15e6375520e
ja    unveraendert: research/tb24_haltedauern/haltedauer_kern.py md5 60942de99b32
ja    unveraendert: research/tb24_haltedauern/live_haltedauern.py md5 7d21a66cd317
ja    unveraendert: research/tb24_haltedauern/positionen_holen.py md5 006375593b4b
ja    unveraendert: research/tb24_haltedauern/test_haltedauer_kern.py md5 a482804dde0c
ja    unveraendert: research/wf_kapital_dd/messung.py md5 94c091f4c4e1
ja    BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-176a
ja    Journal: hoechste FL (FL am Bau-HEAD)
ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md verfolgt, gleich HEAD, md5 a2b38226f683d8d106a5dec61fa5f325
ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md verfolgt, gleich HEAD, md5 0a559c880aa422ca0d77f03c5aa240bc
ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17c_eroeffnung.md verfolgt, gleich HEAD, md5 db41d912f05314a47dcc0e501c3aed5a
ja    Registerblock 17c: genau R108 und Quelle im Codeblock (Z. 13–16)
ja    R108 (a): Wortlaut 10a.5 genau einmal zwischen „Wortlaut: „“ und „“ Der Grund trägt“
ja    Register: 67 da, 68 nicht; R108 0 Treffer
ja    Register endet mit genau einer Leerzeile
ja    Ort 62.2: Einfuegestelle vor Z. 12339 eindeutig, R108 dort noch nicht genannt
ja    Ort 16.4: Einfuegestelle vor Z. 2258 eindeutig, R108 dort noch nicht genannt
ja    Ort 16.6: Einfuegestelle vor Z. 2367 eindeutig, R108 dort noch nicht genannt
ja    Ort 16.8: Einfuegestelle vor Z. 2471 eindeutig, R108 dort noch nicht genannt
ja    Ort 29.3: Einfuegestelle vor Z. 5446 eindeutig, R108 dort noch nicht genannt
ja    Ort 37.5: Einfuegestelle vor Z. 7273 eindeutig, R108 dort noch nicht genannt
ja    Ort 41.3 C2: Einfuegestelle vor Z. 8927 eindeutig, R108 dort noch nicht genannt
ja    Ort 66.1: Einfuegestelle vor Z. 12566 eindeutig, R108 dort noch nicht genannt
ja    Ort 67.1: Einfuegestelle vor Z. 12632 eindeutig, R108 dort noch nicht genannt
ja    S-B1: 10a.2 und 10a.4 je einmal, 10a.5 nicht, R108 nicht; Marke vor Z. 605, 10a.5 vor Z. 635
ja    Index-Kopf Z. 3 nennt 0–67
ja    Index: Zeile 67, Pflegezeile TB-175, Pflege-Anker je genau einmal; kein Abschnitt 19
ja    Dialog-Index: 17c noch nicht
ja    R108 (d): Register am Stand 7fe6342 lesbar (git show)
info  R108 (d) Voraussetzung (Messung, kein Urteil): Register am Stand 7fe6342 nennt einen Wert des Startkapitals an 1 Stelle(n):
info    Z. 12167 (59.1): nen** durchgehenden Kapitalpfad je Bot (Startkapital 10 000, ohne Neustart, R36), ausgeschn
info  R108 (d) Wert: strategies/elliott_wave/equity_simulation.py Z. 66 STARTING_CAPITAL = 10_000.0
info  R108 (d) Wert: strategies/elliott_wave_stocks/equity_simulation.py Z. 71 STARTING_CAPITAL = 10_000.0
info  R108 (d) Wert: strategies/rsi2_crypto/equity_simulation.py Z. 51 STARTING_CAPITAL = 10_000.0
info  R108 (d) Wert: strategies/rsi2_mean_reversion/equity_simulation.py Z. 62 STARTING_CAPITAL = 10_000.0
info  R108 (d) Wert: strategies/t3_supertrend/equity_simulation.py Z. 54 STARTING_CAPITAL = 10_000.0
info  R108 (d) Wert: strategies/turtle_soup_crypto/equity_simulation.py Z. 45 STARTING_CAPITAL = 10_000.0
info  R108 (d) Wert: strategies/turtle_soup_stocks/equity_simulation.py Z. 68 STARTING_CAPITAL = 10_000.0
info  R108 (d) Wert: strategies/volatility_breakout/equity_simulation.py Z. 61 STARTING_CAPITAL = 10_000.0
info  R108 (d) Wert: strategies/volatility_breakout_crypto/equity_simulation.py Z. 61 STARTING_CAPITAL = 10_000.0
info  R108 (d): neun Dateien, alle denselben Wert 10_000.0
Pruefungen: 35, NEIN: 0
rc 0
```

## Schritt R

Datum `17.10.2026`, S0 `17648ad`. Die Probe (`r_probe.txt`) endet mit `Pruefungen: 7, NEIN: 0` und `rc 0`. Die letzten Zeilen von `r_eintrag.txt`:

```
ja    nachher: 9 Marken Z. [2259, 2371, 2478, 5456, 7286, 8943, 12358, 12588, 12657]; Abschnitt 68 Z. 12717
ja    R108 mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)
ja    Register append-only bis auf die 9 Marken (je Leerzeile, Marke, Zeichengleich-Zeile)
ja    S-B1: Marke Z. [606], 10a.5 Z. [639]; sonst zeichengleich; Wortlaut = R108 (a)
Pruefungen: 11, NEIN: 0
rc 0
```

Marken nach `r_daten.json` (Ort, Kopf, Zeile):

| Ort | Kopf der Marke | Z. |
|---|---|---|
| 16.4 | 16.4 ERGÄNZT durch R108 (68.1) | 2259 |
| 16.6 | 16.6 ERGÄNZT durch R108 (68.1) | 2371 |
| 16.8 | 16.8 ERGÄNZT durch R108 (68.1) | 2478 |
| 29.3 | 29.3 ERGÄNZT durch R108 (68.1) | 5456 |
| 37.5 | 37.5 ERGÄNZT durch R108 (68.1) | 7286 |
| 41.3 C2 | 41.3 C2 ERGÄNZT durch R108 (68.1) | 8943 |
| 62.2 | 62.2 R101 ERGÄNZT und BERICHTIGT durch R108 (68.1) | 12358 |
| 66.1 | 66.1 R106 ERGÄNZT durch R108 (68.1) | 12588 |
| 67.1 | 67.1 R107 ERGÄNZT durch R108 (68.1) | 12657 |
| S-B1 10a.2 | S-B1 10a.2 ERGÄNZT durch 10a.5 | 606 (S-B1) |
| S-B1 10a.5 | Nachtrag vom 17.10.2026 | 639 (S-B1) |

Abschnitt 68 beginnt bei Z. 12717, das Register hat danach 12 785 Zeilen. 68.2 enthält den V-Beleg wörtlich eingerückt und die Tatsachennotizen (a) R108 (d) (nur gemessen, Wert und Ort nicht eingetragen), (b) R108 (a) (äussere Quelle liegt nicht vor, nicht eingetragen) und (c) R56 (b).

## Schritt K

| Beleg | rc |
|---|---|
| `k_registerkopie.txt` | 0 (bytegleich, 1 254 111 B, sha256 `c968a0ec5a2a92ea…`; Teil 6 = Abschnitte 58–68, 141 950 B) |
| `k_abschnitte.txt` | 0 (Abschnitte 0–68: 69 Dateien) |
| `k_pruefen.txt` | 0 |
| `k_index_zeilen.txt` | 0 (484 Zeilenangaben umgeschrieben, davon 345 geändert) |
| `k_index.txt` | 0 (5/0; Index-Kopf jetzt 0–68, Zeile `\| 68 aus 17c \|`, Abschnitt 19) |
| `k_handfelder.txt` | 0 |
| `k_dialog_index.txt` | 0 (69 von 69 Zeilen; offen 16, ohne Registertext 13, registriert 40) |
| `k_dialog_pruefen.txt` | 0 |

Es ist keine weitere Teildatei entstanden. Nach K war `git status --porcelain` leer.

## Schritt E2

`e2_probe.txt` (letzte Zeilen):

```
ja    embargo_fuer_bot(t3_supertrend): P95 9.0000 (von Hand), Embargo 10 = aufgerundet + 1, n_trades_gefunden 6, herkunft alle_trades
ja    Gegenprobe: embargo_neun.py am HEAD scheitert an derselben Kopie (liest <bot>_positionen.csv): FileNotFoundError
Ergebnis: 9 von 9 bestanden
rc 0
```

`e2_test.txt` (letzte Zeilen):

```
  ok    Gegenprobe 13: auswertung.py schreibt neben ERGEBNIS_DIR -> auswertung.py faellt auf

Alle Pruefungen bestanden.
rc 0
```

`e2_nachher.txt` (letzte Zeilen):

```
ja    Probe E2 = Anhang E
ja    e2_probe.txt: 9 von 9, rc 0
ja    e2_test.txt: Test am neuen auswertung.py gruen, Gegenprobe trifft
Pruefungen: 17, NEIN: 0
rc 0
```

`test_faltenplan_neun.py` lief nicht, weil er Kursdateien liest (Verbot). Nach R108 (c) bleibt D4 bei t3_supertrend auf den alten Listen rot, bis sie neu erzeugt werden.

## Schritt A

`a_kennung.txt`: `Kennung FM (hoechste FL)`. Backlog: Probe und Eintrag je 1/0 und rc 0, Rang 1 ergänzt. Journal: Probe und Eintrag je 3/0 und rc 0, Block FM vor „Wiederkehrende Lehren“.

## Offen

- **R108 (d):** Wert und Ort des Startkapitals (TB-176b, Handelscode), nach der Frage an den Verfahrensprüfer zur Voraussetzung in (d). Gemessen ist nur: Register am Stand `7fe6342` an einer Stelle (59.1) „10 000“, alle neun `equity_simulation.py` `10_000.0`.
- **R108 (e):** nachgeholte Prüfung mit gegen ohne Schranke (t3_supertrend, zwei Elliott-Bots), nach Fable 17.10.d.
- **Äussere Quelle zu 10a.5:** Die Tatsachennotiz mit äusserer Quelle und Datum (kein UCITS-Fonds auf ein einzelnes Edelmetall) fehlt.
- `research/mtm_drawdown/grundlage.py`, `messung.py` und `test_mtm_kern.py` sind nicht umgestellt (R94 (b), Startkapital erst mit TB-176b).

## In einfacher Sprache

Die neue Antwort des Verfahrensprüfers liegt jetzt mit Anfrage und Übergabe unverändert im Repo. Ihr Regeltext R108 steht wortgleich als Abschnitt 68 im Register, mit neun Hinweisen an älteren Stellen. Die Vorregistrierung des ETF-Vorhabens S-B1 hat einen datierten Nachtrag: Gold und Silber laufen über ETCs, weil es keinen UCITS-Fonds auf ein einzelnes Metall gibt. Die äussere Quelle für diesen Grund fehlt noch und ist als offen vermerkt. Wo das Startkapital steht, ist nur gemessen (überall 10 000), nicht entschieden. Zwei Auswertungen der Haltedauern rechnen jetzt auf allen gefundenen Trades statt nur auf den ausgeführten. Am Handelscode hat sich nichts geändert, auf Kursdaten lief nichts.
