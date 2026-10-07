# TB-140: Ergebnis. Verfahrensmessung 2, nur lesend — Voraussetzungen aus R78 und R79: Umgebung gleich Lock (67/67, Plattform gleich), `schedule` je Aktien-Bot gleich dem Ausschnitt, Bestand vom 02.10.2026 an `APH` belegt, `close` je Tagesreihe wie R79 (c); 5.4.0 nach `ERGEBNIS_TB-47` nur erschliessbar; im Code: kein Zellen-Erzeuger, Benchmark und Kern lesen `close` aus `<SYMBOL>_1d.csv`, Lader und Benchmark verwerfen Zeilen ohne `close`, Werte aus Zeilen ab dem Go-Live-Schnitt werden gebildet, `auswertung.py` fängt nicht endliche Werte nur teils

**Sitzungstitel:** `TB-140` · **Stand:** 07.10.2026, 11:05 (gemessen mit `date`) · **Auftrag:** `docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md` ·
**Belege:** `docs/belege/TB-140/`
**Eingang:** `8d172c0` (TB-138 D3). Commits: `8127f7f` (Schritt 0: Stand des steuernden Chats, **⟨S0⟩**), `7b22367`
(Teil 1: V4, V5, V6, Z1, Z2, mit den Belegen aus 0a und 0b, **⟨T1⟩**), `face453` (Teil 2: V1, V2, V3, Fundstellenprüfung),
`fa57fcb` (N: BACKLOG), der Abgabe-Commit **⟨A⟩** (dieses Dokument, Journal EH), danach **⟨D⟩** (`d3_numstat.txt`) und
der Commit mit `d3_porcelain.txt`. Nach jedem Commit gepusht, jeder Push im ersten Versuch.
**Freigabe:** Handwerk ohne Sperrlistennähe, pauschal frei (Betreiber 26.09.2026); Betreiber 07.10.2026, 08:10: „Arbeite heute
so viel wie möglich selbstständig ab, damit wir endlich wieder größere Fortschritte machen.“ **Keine Rückfrage an den Betreiber
in dieser Sitzung.**
**Umgebung:** Mac, `trading-env/bin/python3` 3.9.6, `macOS-15.7.9-x86_64-i386-64bit`, alle 67 Pakete gleich `requirements.lock`
(V4). Modell laut Selbstauskunft Opus 5.5. **Kein Abbruchkriterium ausgelöst.**
**Helfer:** Für V2 lasen drei Lese-Helfer (Unteragenten dieser Sitzung, nur lesend) den Code von je drei bzw. zwei Bots und
`shared/zuteilung.py`. Jede Codezeile, auf die sich dieses Ergebnis stützt, steht in `fundstellen.tsv`; den Wortlaut dort
hat ein Skript aus den Dateien gelesen (`fundstellen_bauen.py`), die Prüfung vergleicht ihn erneut (`fundstellen_pruefung.txt`,
291 Fundstellen, 0 ungleich). Zum Sichtschutz unten unter „Nicht getan“.

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | `main`, `8d172c0`; genau die sechs Einträge; md5 und Bytes der drei Fable-Dateien wie die Tabelle; Platzhaltersuche kein Treffer | **gleich** (`0a_head.txt`, `0a_status.txt`, `0a_md5.txt`: 11 681 B `06ae4b76…`, 7 295 B `6e9fa10d…`, 26 689 B `2fc513b9…`); Platzhaltersuche über Auftrag und `UEBERGABE.md`: **kein Treffer** (`0a_platzhalter.txt`). In `$TMPDIR` vor dem Belegordner gemessen |
| 0b | 3.9.6; Register 11 581 Z. `8d505a38…`; Abbild `46f0ad5d1d83a253…`; Lock `96a5c572…`; Universumsdateien `6acba892…`/`3afc95a4…`; `--pruefen` rc 0 | **alles gleich** (`0b_ausgang.txt`); Dateiliste des Snapshots 226 Dateien, `e810849e…` (gleich dem Vergleichswert) |
| Gegenproben | je „beisst“ bzw. das Soll | V4 `GEGENPROBE: beisst` (rc 0) · V5 rc 1, je Bot zwei `FALL`, viermal `NICHT gleich` · V6 Rückgaben `1001122`, `beisst` · Z1 `beisst` · Fundstellen zwei `UNGLEICH`, rc 1, `beisst` — alle beim ersten Lauf |
| V4 | rc 0, Lock gleich Register, W1 67/67, Kopf gleich | **rc 0; *erfüllt*** — W1 67/67, W2 67/67, Plattform gleich (`v4.txt`) |
| V5 | rc 0, je Bot gleich | **rc 0; *erfüllt*** — 2 428 / 2 177 / 2 428 / 2 177 Tage, 0 Abweichungen (`v5.txt`) |
| V6 | rc 0, `TEIL (i) ja · (ii) ja · (iii) ja` | **rc 0; *erfüllt*** (`v6.txt`) |
| Z1 | rc 0, je Datei eine Zeile `DATEI` | **rc 0; *erfüllt*** — 174 Zeilen `DATEI`, keine `NICHT LESBAR` (`z1.txt`) |
| Z2 | rc 0 | **rc 0; „nur erschliessbar“** (`z2.txt`, `z2_stellen.md`) |
| Zwischenstand | gepusht, eine Zeile | `teil1_zwischenstand.md` in `7b22367`, Zeile ausgegeben |
| Fundstellenprüfung | `ungleich 0`, rc 0 | **291 Fundstellen, ungleich 0, rc 0** |
| V1 | Urteile nach der Tabelle | Nr. 0 **„kein Zellen-Erzeuger gefunden“** · (i) **„Spalte und Datei wie die Klammer“** · (ii) am vorhandenen Kern **„Spalte und Datei wie die Klammer“**, für den Kern des Erzeugers **nicht messbar** |
| V2 | Urteile nach der Tabelle | (a) **verwirft** an allen fünf Stellen · (b) **„ein solcher Wert wird gebildet“** |
| V3 | Tabelle; Urteil (ii) | (i) 14 Zeilen, 7 mit Fall ohne Zahl, 7 „sagt nichts“ · (ii) **„trifft teils zu“** |
| N | Anker 1; C3 GLEICH; numstat `8	0` | E1: Anker 1 (Z. 312 von 323), erste Textzeile vorher 0, nachher 1; C3 **GLEICH** (2 577 Bytes, 7 Zeilen); `8	0`. Platzhalter in E1 und J1: 0/0 (`n_platzhalter.txt`) |
| J1 | `einsetzbar` / `eingesetzt`; `j1_vergleich.py` Vorkommen 1, an Zeilengrenzen 1, im Block ja, vor `### Was gemessen ist` ja, 6 Zeilen, GLEICH, rc 0 | Probe rc 0 `einsetzbar`, dann rc 0 `eingesetzt` in Block **EH** (`j1_einsetzen.txt`); `j1_vergleich.txt`: 2 548 Bytes, 6 Zeilen, Vorkommen 1, an Zeilengrenzen 1, im neuen Block EH ja, vor `### Was gemessen ist` ja, **GLEICH**, rc 0. Journal numstat `49	0` (Block samt Trennzeilen, darin J1 mit Leerzeile) |
| Tabellenvergleich | je Tabelle `Vorkommen 1`, `an Zeilengrenzen 1`, `GLEICH`; `Marken im Ergebnis: 0`; rc 0 | `--einsetzen` rc 0 (6 Tabellen); `--pruefen`: 6 × `Vorkommen 1`, `an Zeilengrenzen 1`, keine fremde Kennung, `GLEICH`; `Marken im Ergebnis: 0`; rc 0 (`ergebnis_tabellen.txt`) |
| D0 | `0b` gleich bis auf die ersten drei Zeilen | **gleich** bis auf Kopfzeile, `ZEIT`, `HEAD` (`0b_nachher.txt`) |

## Teil 1

### V4 — `trading-env` gegen den ganzen Lock (R79 (a))

Beleg `v4.txt` (rc 0), Gegenprobe `v4_gegenprobe.txt` (rc 0, `beisst`: an der zweiten Kopie rc 1, `KOPF plattform … ABWEICHUNG`,
vier Zeilen `PAKET` für `pandas` 0.0.1 und `kein-solches-paket-tb140` in W1 und W2; die erste Kopie ohne diese Zeilen).

| Wert | Ist |
|---|---|
| Lock | `requirements.lock`, sha256 `96a5c572…` **gleich Register**; 67 Paketzeilen, 0 Zeilen ohne `==` |
| `interpreter_voll` | `3.9.6 (default, Apr 30 2025, 02:07:18) [Clang 17.0.0 (clang-1700.0.13.5)]` — gleich |
| `plattform` | `macOS-15.7.9-x86_64-i386-64bit` — gleich |
| `interpreter_venv` | `3.9.6` — gleich |
| `maschine` | `x86_64` (Vergleichswert `x86_64`; ohne Urteil) |
| W1 (`importlib.metadata.version` je Lock-Zeile, der Weg des Laufs) | **67 von 67** |
| W2 (alle installierten Distributionen, PEP 503) | **67 von 67**; installiert, nicht im Lock: 0; mehr als eine Fassung: 0 |

**Urteil V4: *erfüllt*** — rc 0, der Lock trägt den Hash des Registers, W2 meldet keine Zeile. Vom Werkzeug (O3): Die
Lock-Schreibweisen (zum Beispiel `pandas-market-calendars`) löst `importlib.metadata.version` in 3.9.6 auf; W1 und W2 melden
dieselben (keine) Zeilen; `distributions()` zählt genau die 67 Distributionen des Locks auf.

### V5 — ein Aufruf von `schedule` je Aktien-Bot gegen den Ausschnitt (R79 (b))

Beleg `v5.txt` (rc 0), Gegenprobe `v5_gegenprobe.txt` (rc 1; je Bot `nur_im_aufruf` am 101. Tag — 2017-05-26 bzw.
2018-05-25 — und `nur_im_ausschnitt` am ersten Samstag 2017-01-07 bzw. 2018-01-06; viermal `NICHT gleich`). Kopf: 4.6.1,
2.3.3, 4.5.6, 2.0.2.

| Aktien-Bot | Zeitraum | Ausschnitt | Aufruf | doppelt | nur Ausschnitt | nur Aufruf | Urteil der Zeile |
|---|---|---|---|---|---|---|---|
| `elliott_wave_stocks` | 2017-01-01..2026-08-31 | 2 428 | 2 428 | 0 | 0 | 0 | gleich |
| `rsi2_mean_reversion` | 2018-01-01..2026-08-31 | 2 177 | 2 177 | 0 | 0 | 0 | gleich |
| `turtle_soup_stocks` | 2017-01-01..2026-08-31 | 2 428 | 2 428 | 0 | 0 | 0 | gleich |
| `volatility_breakout` | 2018-01-01..2026-08-31 | 2 177 | 2 177 | 0 | 0 | 0 | gleich |

Einmal gerechnete Menge 1962-01-02..2026-09-01: 16 275 Tage. Alle drei Vergleichswerte des Vorgängers (16 275, 2 428, 2 177)
gleich. **Urteil V5: *erfüllt*** — rc 0 und V4 *erfüllt*.

### V6 — der Bestand vom 02.10.2026 an `APH` (R79 (g))

Beleg `v6.txt` (rc 0), Gegenprobe `v6_gegenprobe.txt` (Rückgaben `1001122`, `beisst`).

| Teil | Ist |
|---|---|
| (i) Stand `0779453` (2026-10-02T18:11:14+02:00, „TB-131 D3: porcelain nach der Abgabe“), `data/APH_1d.csv` | genau eine Zeile `open_time` 2026-09-01; 6 Spalten; leer: `open`, `high`, `low`, `close`; **`close` fehlt: ja** |
| (ii) Blob | Arbeitsdatei (selbst gerechnet) `847a599c4d065f662dc1b096bf1618c69c81c719` = `0779453:data/APH_1d.csv` = `HEAD:data/APH_1d.csv`; Commits an der Datei nach `0779453`: **keiner**; einziger Commit an der Datei: `0f6491b` 2026-09-02T23:12:10+02:00 „Initial commit“ → **ja** |
| (iii) Änderungszeit | 2026-09-02T04:21:29+00:00, vor 2026-10-01T22:00:00+00:00 → **ja** |

Daneben, ohne Urteil: Die Snapshot-Datei `APH_1d.csv` trägt denselben Blob, dieselbe sha256 (`8d5d5324…`) und 821 714 Bytes;
`MANIFEST.json` nennt dieselbe sha256 und dieselbe Bytezahl. Die selbst gerechnete Blob-Prüfsumme trifft die von git geführte.
`--no-optional-locks` und `%cI` kennt git 2.39.5 (Apple Git-154); das Skript lief unverändert. Nicht messbar bleibt ein
zurückgesetzter Zeitstempel. **Urteil V6: *erfüllt*.**

### Z1 — `close` je Tagesreihe des Snapshots (Beleg zu R79 (c))

Beleg `z1.txt` (rc 0), Gegenprobe `z1_gegenprobe.txt` (`beisst`). Fehlwert-Liste: 19 Texte aus
`pandas._libs.parsers.STR_NA_VALUES`.

| | Aktien | Krypto |
|---|---|---|
| Universum | 150 | 25 (in beiden Dateien: keines) |
| Tagesreihen | 150 | 24 (`XAUTUSDT` ohne `_1d`-Reihe) |
| Zeilen | 1 417 557 | 44 163 |
| Zeilen ohne `close` | **1** — `APH_1d.csv` 2026-09-01, Zelle leer | **0** |
| letzte Zeile | 150-mal 2026-09-01 | 24-mal 2026-09-14 |
| letzte Zeile mit `close` | 149-mal 2026-09-01, einmal 2026-08-31 | 24-mal 2026-09-14 |

Dateien ohne Zuordnung: 0. Hinweise: 0. Beide Zeilen `SATZ R79 (c)` „trifft zu“. Alle Vergleichswerte (174 Dateien, eine
Zeile ohne `close`, 150 und 24 Reihenenden) gleich. **Urteil Z1: *erfüllt*.**

### Z2 — woher „5.4.0“ stammt (Beleg zu R79 (f))

Beleg `z2.txt` (rc 0). Datei `docs/ERGEBNIS_TB-47_snapshotgrenze.md`: 526 Zeilen, 25 988 Bytes, sha256 `577f1bb2…`. Feld
`kalender` in `eingaben.json`: `{"im_repo": […], "in_selektionshuelle": [], "paket_vorhanden": "5.4.0"}`. Zeilen je Muster:
`5\.4\.0` 2 · `cloud` 7 · `eingaben\.json` 2 · `kalender` 9 · `paket_vorhanden` 0 · `nachinstall` 4 · `python` 4 — alle
gleich den Vergleichswerten. Die Stellen, wörtlich:

**Z2 — Stellen in `docs/ERGEBNIS_TB-47_snapshotgrenze.md` (526 Zeilen, sha256 `577f1bb2…`), wörtlich, je Zeile mit Nummer; Überschriftzeilen zur Ortsangabe mitgenommen. Erzeugt per Skript aus der Datei, nicht abgetippt.**

*Sitzung der Datei:*

```
Z. 3: **Ergebnis der Cloud-Sitzung vom 18.09.2026.**
```

*Teil 1: Werkzeug und Rohdaten (der Satz über zwei Zeilen):*

```
Z. 66: ## Teil 1 — Erhebung: was gehört in den Snapshot?
Z. 68: **Werkzeug:** `research/snapshotgrenze/erhebung_eingaben.py` (misst, ändert
Z. 69: nichts). **Rohdaten:** `research/snapshotgrenze/ergebnisse/eingaben.json`.
```

*Teil 1, Abschnitt zum Handelskalender: der Satz mit 5.4.0 (über zwei Zeilen):*

```
Z. 102: ### ⭐ Der Handelskalender im Besonderen
Z. 121:    **Das ist eine Eigenschaft des Aufbaus, keine Lücke dieses Moduls** — aber
Z. 122:    es gehört benannt, und in der Cloud war die Fassung **5.4.0**.
```

*Abschnitt Umgebung: Nachinstallation mit 5.4.0:*

```
Z. 342: ## Umgebung — jede Abweichung von der Tabelle
Z. 344: *Gemessen in dieser Sitzung, nicht übernommen.*
Z. 355: **Nachinstalliert wurde** (`pip install`, in zwei Runden):
Z. 357: | Runde | Pakete |
Z. 358: |---|---|
Z. 359: | für Teil 1–4 | `pandas 3.0.6`, `numpy 2.4.6`, `pandas_market_calendars 5.4.0`, `pytz 2026.3.post1`, `dateparser 1.4.3` |
```

Muster ohne Treffer in der Datei: `paket_vorhanden` (0 Zeilen, `z2.txt`). Keine Zeile nennt 5.4.0 zusammen mit `eingaben.json` oder dem Feld `kalender`.

**Urteil Z2: „nur erschliessbar“.** Die Kette, Schritt für Schritt: Z. 3 nennt die Datei „Ergebnis der Cloud-Sitzung vom
18.09.2026“ · Z. 66–69: Teil 1 ist die Erhebung mit dem Werkzeug `erhebung_eingaben.py` und den Rohdaten `eingaben.json` ·
Z. 102, 121–122, in Teil 1: „in der Cloud war die Fassung **5.4.0**“ · Z. 342–359: „Nachinstalliert wurde (`pip install` …)“
für Teil 1–4 `pandas_market_calendars 5.4.0`. **Was der Kette fehlt:** Keine Zeile verbindet 5.4.0 mit `eingaben.json` oder
mit dem Feld `kalender`; das Wort `paket_vorhanden` steht in der Datei nicht. Dass die Erhebung das Feld aus der Fassung des
startenden Interpreters schreibt, steht im Code (`erhebung_eingaben.py` Z. 613–618, Auftrag des Vorgängers unter „Belegt“),
nicht in der Datei.

## Teil 2

Gelesen am Stand ⟨T1⟩ (`7b22367`), Code unverändert bis ⟨A⟩ (D3). Suchläufe `v1_suche.sh`, `v2_suche.sh`, `v3_suche.sh` mit
ihren Ausgaben (je rc 0); Bereich je Aufruf in der Zeile `BEREICH`. Die Fundstellen: `fundstellen.tsv`.

### Übersicht je Bot

**Übersicht je Bot** (zusammengezogen aus `v1_spalte.md` und `v2_lader_schnitt.md`; keine neue Aussage). Spalte E·A·B·I: Einstieg · Ausstieg · Bewertung · Indikatorwert.

| Bot | Lader `Datei:Zeile` | Lader liest: Datei, Spalten | Benchmark und Kern lesen: Datei, Spalte | Zeile ohne `close`: behalten / verwerfen, Codezeile | Wert aus einer Zeile ab dem Go-Live-Schnitt möglich? Einstieg · Ausstieg · Bewertung · Indikatorwert (je ja / nein / offen) | Kennungen | Stand |
|---|---|---|---|---|---|---|---|
| `elliott_wave` | `multi_symbol_optimise.py:53` (V2-34) | `<SYMBOL>_<INTERVAL>.csv`, `INTERVAL` = `Client.KLINE_INTERVAL_1HOUR` (V2-35, V2-160), ganze Zeile; Filter auf `open`/`high`/`low`/`close` | Benchmark `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); Kern `<symbol>_1d.csv`, `close` (V1-47, V1-50) | verwirft, `shared/kursdaten.py:85` über den Lader (V2-36, V2-04) | ja · offen · offen · ja | V2-34, V2-36, V1-25, V1-21, V1-47, V2-04 | Lader belegt · Spalte belegt · Schnitt: Einstieg und Indikatorwert erschlossen, Ausstieg und Bewertung offen |
| `t3_supertrend` | `multi_symbol_optimise.py:50` (V2-153) | `<SYMBOL>_<INTERVAL>.csv`, `INTERVAL` = `Client.KLINE_INTERVAL_4HOUR` (V2-46, V2-161), ganze Zeile; Filter wie oben | Benchmark `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); Kern `<symbol>_1d.csv`, `close` (V1-47, V1-50) | verwirft, `shared/kursdaten.py:85` über den Lader (V2-47, V2-04) | ja · offen · offen · ja | V2-153, V2-47, V1-25, V1-21, V1-47, V2-04 | Lader belegt · Spalte belegt · Schnitt: Einstieg und Indikatorwert erschlossen, Ausstieg und Bewertung offen |
| `rsi2_crypto` | `multi_symbol_optimise.py:59` (V2-154) | `<SYMBOL>_1d.csv` (V2-57, V2-163), ganze Zeile; Filter wie oben | Benchmark `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); Kern `<symbol>_1d.csv`, `close` (V1-47, V1-50) | verwirft, `shared/kursdaten.py:85` über den Lader (V2-58, V2-04) | ja · offen · offen · ja | V2-154, V2-58, V1-25, V1-21, V1-47, V2-04 | Lader belegt · Spalte belegt · Schnitt: Einstieg und Indikatorwert erschlossen, Ausstieg und Bewertung offen |
| `turtle_soup_crypto` | `multi_symbol_optimise.py:42` (V2-155) | `<SYMBOL>_1d.csv` (V2-67, V2-164), ganze Zeile; Filter wie oben | Benchmark `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); Kern `<symbol>_1d.csv`, `close` (V1-47, V1-50) | verwirft, `shared/kursdaten.py:85` über den Lader (V2-68, V2-04) | ja · offen · offen · ja | V2-155, V2-68, V1-25, V1-21, V1-47, V2-04 | Lader belegt · Spalte belegt · Schnitt: Einstieg und Indikatorwert erschlossen, Ausstieg und Bewertung offen |
| `volatility_breakout_crypto` | `multi_symbol_optimise.py:44` (V2-156) | `<SYMBOL>_1d.csv` (V2-77, V2-165), ganze Zeile; Filter wie oben | Benchmark `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); Kern `<symbol>_1d.csv`, `close` (V1-47, V1-50) | verwirft, `shared/kursdaten.py:85` über den Lader (V2-78, V2-04) | ja · offen · offen · ja | V2-156, V2-78, V1-25, V1-21, V1-47, V2-04 | Lader belegt · Spalte belegt · Schnitt: Einstieg und Indikatorwert erschlossen, Ausstieg und Bewertung offen |
| `elliott_wave_stocks` | `multi_symbol_optimise.py:60` (V2-90) | `<SYMBOL>_<INTERVAL>.csv`, `INTERVAL` = `"1d"` (V2-91, V2-162), ganze Zeile; Filter wie oben | Benchmark `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); Kern `<symbol>_1d.csv`, `close` (V1-47, V1-50) | verwirft, `shared/kursdaten.py:85` über den Lader (V2-92, V2-04) | ja · offen · offen · ja | V2-90, V2-92, V1-25, V1-21, V1-47, V2-04 | Lader belegt · Spalte belegt · Schnitt: Einstieg und Indikatorwert erschlossen, Ausstieg und Bewertung offen |
| `rsi2_mean_reversion` | `multi_symbol_optimise.py:55` (V2-157) | `<SYMBOL>_1d.csv` (V2-107, V2-166), ganze Zeile; Filter wie oben | Benchmark `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); Kern `<symbol>_1d.csv`, `close` (V1-47, V1-50) | verwirft, `shared/kursdaten.py:85` über den Lader (V2-108, V2-04) | ja · offen · offen · ja | V2-157, V2-108, V1-25, V1-21, V1-47, V2-04 | Lader belegt · Spalte belegt · Schnitt: Einstieg und Indikatorwert erschlossen, Ausstieg und Bewertung offen |
| `turtle_soup_stocks` | `multi_symbol_optimise.py:49` (V2-158) | `<SYMBOL>_1d.csv` (V2-120, V2-167), ganze Zeile; Filter wie oben | Benchmark `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); Kern `<symbol>_1d.csv`, `close` (V1-47, V1-50) | verwirft, `shared/kursdaten.py:85` über den Lader (V2-121, V2-04) | ja · offen · offen · ja | V2-158, V2-121, V1-25, V1-21, V1-47, V2-04 | Lader belegt · Spalte belegt · Schnitt: Einstieg und Indikatorwert erschlossen, Ausstieg und Bewertung offen |
| `volatility_breakout` | `multi_symbol_optimise.py:53` (V2-159) | `<SYMBOL>_1d.csv` (V2-133, V2-168), ganze Zeile; Filter wie oben | Benchmark `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); Kern `<symbol>_1d.csv`, `close` (V1-47, V1-50) | verwirft, `shared/kursdaten.py:85` über den Lader (V2-134, V2-04) | ja · offen · offen · ja | V2-159, V2-134, V1-25, V1-21, V1-47, V2-04 | Lader belegt · Spalte belegt · Schnitt: Einstieg und Indikatorwert erschlossen, Ausstieg und Bewertung offen |

### V1 — welche Spalte welcher Reihe aus welchem Ordner (R78 (a))

**V1 Nr. 0 — gibt es einen Zellen-Erzeuger?** Suche `V1-0a` und `V1-0b` in `docs/belege/TB-140/v1_suche.txt`: Bereich alle von git verfolgten `*.py` ausserhalb von `docs/` (482 Dateien), Muster `zellen.csv` (11 Treffer, 4 Dateien), `zellenbericht` (0), `tagesreihen/` (2, 1 Datei), `benchmark_tagesreihen` (11, 4 Dateien), `symbole_je_falte` (0), `herkunft.json` (22, 4 Dateien), dazu ohne Gross/Klein `zellen.?erzeuger` (0) und `lese.?audit` (6, 2 Dateien: `shared/paths.py`, `shared/test_startpruefungen.py`, nur Kommentare und Docstrings). Die Ausgaben aus R39: V1-01.

| Datei | Treffer (Kennungen) | was die Datei nach ihrem Docstring ist (Wortlaut, höchstens 300 Zeichen) | liest, schreibt oder nennt sie eine Ausgabe aus R39? Codezeile | woraus schreibt sie (Kursdaten, erfundene Werte, Testdaten)? | Stand |
|---|---|---|---|---|---|
| `research/vorregistrierung/auswertung.py` | `zellen.csv`, `tagesreihen/`, `benchmark_tagesreihen`, `herkunft.json` (V1-04, V1-05) | „TB-30a - Das eingefrorene Auswertungsskript“; „Dieses Programm liest die ROHERGEBNISSE eines Selektionslaufs und gibt aus:“ (V1-02, V1-03) | liest `zellen.csv` (Z. 321, V1-04) und `benchmark_tagesreihen/<markt>.csv` (Z. 379, V1-05) | schreibt keine Ausgabe aus R39 | belegt |
| `research/vorregistrierung/beispieldaten.py` | `zellen.csv`, `benchmark_tagesreihen`, `herkunft.json` (V1-07, V1-08, V1-09) | „TB-30a - Beispieldaten: Rohergebnisse mit frei erfundenen Werten“ (V1-06) | schreibt `zellen.csv` (Z. 200, V1-07), `herkunft.json` (Z. 210, V1-08), `benchmark_tagesreihen/<markt>.csv` (Z. 233, V1-09) | erfundene Werte (Docstring, V1-06) | belegt |
| `research/vorregistrierung/test_ersatzwerte.py` | `zellen.csv`, `benchmark_tagesreihen`, `herkunft.json` (V1-11) | „TB-106 - Rueckfall (d): stille Ersatzwerte in faltenplan.py, benchmark.py,“ (V1-10) | schreibt `zellen.csv` in einen Ordner unter `tempfile` (Z. 775, V1-11) | Testdaten | belegt |
| `research/vorregistrierung/test_vorregistrierung.py` | `zellen.csv`, `benchmark_tagesreihen` (V1-13) | „TB-30a - Selbsttest der Vorregistrierung“ (V1-12) | liest und ändert `zellen.csv` aus `beispieldaten` in einem Ordner unter `tempfile` (Z. 206, V1-13) | Testdaten aus `beispieldaten.py` | belegt |
| `research/tb24_haltedauern/positionen_holen.py` | nur `herkunft.json`, als Teil von `<bot>_herkunft.json` (V1-15) | „Ein Bot, ein Prozess: Positionen MIT Ausstiegsart und Kerzenzahl herausholen“ (V1-14) | schreibt `<bot>_herkunft.json` (Z. 219, V1-15); der Name ist nicht `herkunft.json` aus R39 (V1-01) | Positionslisten der Bots (TB-24), nicht gelesen | Zeile belegt · „nicht die Ausgabe aus R39“ erschlossen (Name verschieden, V1-01, V1-15) |

**Urteil V1 Nr. 0: „kein Zellen-Erzeuger gefunden“** — erschlossen: Im Bereich (482 Dateien) schreibt keine Datei eine Ausgabe aus R39 aus Kursdaten; die vier Dateien unter `research/vorregistrierung/` lesen sie oder schreiben sie aus erfundenen Werten oder Testdaten, die fünfte schreibt eine Datei anderen Namens. Ein Kandidat im Sinn der Aufgabe ist nicht gefunden.

**V1 — welche Spalte welcher Reihe aus welchem Ordner Benchmark und Kern lesen (R78 (a)).** Suchen `V1-1a`, `V1-1b`, `V1-2a`, `V1-2b` in `v1_suche.txt`. Kern nach N4: `research/mtm_drawdown/mtm_kern.py` mit `grundlage.lade_schlusskurse` (kein Zellen-Erzeuger gefunden, `v1_erzeuger.md`; „Welchen Kern der Zellen-Erzeuger übernimmt“ legt kein Registertext fest, V1-60).

| Bot | Markt, Zeitrahmen (Kennung) | Benchmark: Lesestelle `Datei:Zeile` | Benchmark: Ordner (Ausdruck, Herkunft `Datei:Zeile`) | Benchmark: Datei, Spalte | Kern: Ladestelle `Datei:Zeile` | Kern: Ordner (Ausdruck, Herkunft `Datei:Zeile`) | Kern: Datei, Spalte | Aufrufer und Argument | Stand |
|---|---|---|---|---|---|---|---|---|---|
| `elliott_wave` | krypto, 1h (V1-29) | `benchmark.py:152`, `:155` (V1-21, V1-22) | `DATA_DIR` = `paths.DATA_DIR` (`benchmark.py:120`, V1-16); ohne Modus `_LIVE_DATA_DIR` = `<BASE_DIR>/data` (`paths.py:685`, `:194`; V1-64, V1-61), unter dem Modus `_MODUS[0]` (`paths.py:692`, V1-65) | `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); die Wahl hängt nur an `markt` (V1-20, V1-25, V1-26), nicht am Bot oder Zeitrahmen | `grundlage.py:87`, `:90` (V1-45, V1-46); der Kern selbst liest keine Datei (`mtm_kern.py:55`, V1-38), `schlusskurse` ist Parameter (V1-39, V1-41) | `DATA_DIR = os.path.join(REPO_ROOT, "data")` (`grundlage.py:35`, `:34`; V1-43, V1-42) — fester Ordner, nicht über `shared/paths.py` | `<symbol>_1d.csv`, `close` (V1-47) über den Aufruf mit `"1d"` (`messung.py:147`, V1-50); daneben liest `grundlage.py:211` die Datei im Zeitrahmen aus dem TB-24-Meta des Bots (`close`) für den Einstandsvergleich, nicht für die MtM-Reihe (V1-48; das Meta ist nicht gelesen) | `tagesschluss`: `benchmark.py:253` mit `"aktien"`/`"krypto"` (V1-25), `test_vorregistrierung.py:1172` (V1-27), ersetzt in `test_ersatzwerte.py:225` (V1-28) · `lade_schlusskurse`: `messung.py:147` `"1d"` (V1-50; je Bot aufgerufen über `alle_bots.py:30`, `:32`, `messung.py:110`; V1-70, V1-71, V1-72; Botliste `grundlage.py:46`, V1-69), `richtungsfall.py:135` `"1d"` (V1-53), `test_mtm_kern.py:121` `"1d"` (V1-54), `grundlage.py:211` Zeitrahmen des Bots (V1-48), `:212` `"1d"` (V1-49) | Lesestellen belegt · Zuordnung zum Bot erschlossen (Markt aus `registerdaten.py`, V1-29) · Ordner im Lauf offen (O7) |
| `t3_supertrend` | krypto, 4h (V1-30) | `benchmark.py:152`, `:155` (V1-21, V1-22) | `DATA_DIR` = `paths.DATA_DIR` (`benchmark.py:120`, V1-16); ohne Modus `_LIVE_DATA_DIR` = `<BASE_DIR>/data` (`paths.py:685`, `:194`; V1-64, V1-61), unter dem Modus `_MODUS[0]` (`paths.py:692`, V1-65) | `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); die Wahl hängt nur an `markt` (V1-20, V1-25, V1-26), nicht am Bot oder Zeitrahmen | `grundlage.py:87`, `:90` (V1-45, V1-46); der Kern selbst liest keine Datei (`mtm_kern.py:55`, V1-38), `schlusskurse` ist Parameter (V1-39, V1-41) | `DATA_DIR = os.path.join(REPO_ROOT, "data")` (`grundlage.py:35`, `:34`; V1-43, V1-42) — fester Ordner, nicht über `shared/paths.py` | `<symbol>_1d.csv`, `close` (V1-47) über den Aufruf mit `"1d"` (`messung.py:147`, V1-50); daneben liest `grundlage.py:211` die Datei im Zeitrahmen aus dem TB-24-Meta des Bots (`close`) für den Einstandsvergleich, nicht für die MtM-Reihe (V1-48; das Meta ist nicht gelesen) | `tagesschluss`: `benchmark.py:253` mit `"aktien"`/`"krypto"` (V1-25), `test_vorregistrierung.py:1172` (V1-27), ersetzt in `test_ersatzwerte.py:225` (V1-28) · `lade_schlusskurse`: `messung.py:147` `"1d"` (V1-50; je Bot aufgerufen über `alle_bots.py:30`, `:32`, `messung.py:110`; V1-70, V1-71, V1-72; Botliste `grundlage.py:46`, V1-69), `richtungsfall.py:135` `"1d"` (V1-53), `test_mtm_kern.py:121` `"1d"` (V1-54), `grundlage.py:211` Zeitrahmen des Bots (V1-48), `:212` `"1d"` (V1-49) | Lesestellen belegt · Zuordnung zum Bot erschlossen (Markt aus `registerdaten.py`, V1-30) · Ordner im Lauf offen (O7) |
| `rsi2_crypto` | krypto, 1d (V1-31) | `benchmark.py:152`, `:155` (V1-21, V1-22) | `DATA_DIR` = `paths.DATA_DIR` (`benchmark.py:120`, V1-16); ohne Modus `_LIVE_DATA_DIR` = `<BASE_DIR>/data` (`paths.py:685`, `:194`; V1-64, V1-61), unter dem Modus `_MODUS[0]` (`paths.py:692`, V1-65) | `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); die Wahl hängt nur an `markt` (V1-20, V1-25, V1-26), nicht am Bot oder Zeitrahmen | `grundlage.py:87`, `:90` (V1-45, V1-46); der Kern selbst liest keine Datei (`mtm_kern.py:55`, V1-38), `schlusskurse` ist Parameter (V1-39, V1-41) | `DATA_DIR = os.path.join(REPO_ROOT, "data")` (`grundlage.py:35`, `:34`; V1-43, V1-42) — fester Ordner, nicht über `shared/paths.py` | `<symbol>_1d.csv`, `close` (V1-47) über den Aufruf mit `"1d"` (`messung.py:147`, V1-50) | `tagesschluss`: `benchmark.py:253` mit `"aktien"`/`"krypto"` (V1-25), `test_vorregistrierung.py:1172` (V1-27), ersetzt in `test_ersatzwerte.py:225` (V1-28) · `lade_schlusskurse`: `messung.py:147` `"1d"` (V1-50; je Bot aufgerufen über `alle_bots.py:30`, `:32`, `messung.py:110`; V1-70, V1-71, V1-72; Botliste `grundlage.py:46`, V1-69), `richtungsfall.py:135` `"1d"` (V1-53), `test_mtm_kern.py:121` `"1d"` (V1-54), `grundlage.py:211` Zeitrahmen des Bots (V1-48), `:212` `"1d"` (V1-49) | Lesestellen belegt · Zuordnung zum Bot erschlossen (Markt aus `registerdaten.py`, V1-31) · Ordner im Lauf offen (O7) |
| `turtle_soup_crypto` | krypto, 1d (V1-32) | `benchmark.py:152`, `:155` (V1-21, V1-22) | `DATA_DIR` = `paths.DATA_DIR` (`benchmark.py:120`, V1-16); ohne Modus `_LIVE_DATA_DIR` = `<BASE_DIR>/data` (`paths.py:685`, `:194`; V1-64, V1-61), unter dem Modus `_MODUS[0]` (`paths.py:692`, V1-65) | `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); die Wahl hängt nur an `markt` (V1-20, V1-25, V1-26), nicht am Bot oder Zeitrahmen | `grundlage.py:87`, `:90` (V1-45, V1-46); der Kern selbst liest keine Datei (`mtm_kern.py:55`, V1-38), `schlusskurse` ist Parameter (V1-39, V1-41) | `DATA_DIR = os.path.join(REPO_ROOT, "data")` (`grundlage.py:35`, `:34`; V1-43, V1-42) — fester Ordner, nicht über `shared/paths.py` | `<symbol>_1d.csv`, `close` (V1-47) über den Aufruf mit `"1d"` (`messung.py:147`, V1-50) | `tagesschluss`: `benchmark.py:253` mit `"aktien"`/`"krypto"` (V1-25), `test_vorregistrierung.py:1172` (V1-27), ersetzt in `test_ersatzwerte.py:225` (V1-28) · `lade_schlusskurse`: `messung.py:147` `"1d"` (V1-50; je Bot aufgerufen über `alle_bots.py:30`, `:32`, `messung.py:110`; V1-70, V1-71, V1-72; Botliste `grundlage.py:46`, V1-69), `richtungsfall.py:135` `"1d"` (V1-53), `test_mtm_kern.py:121` `"1d"` (V1-54), `grundlage.py:211` Zeitrahmen des Bots (V1-48), `:212` `"1d"` (V1-49) | Lesestellen belegt · Zuordnung zum Bot erschlossen (Markt aus `registerdaten.py`, V1-32) · Ordner im Lauf offen (O7) |
| `volatility_breakout_crypto` | krypto, 1d (V1-33) | `benchmark.py:152`, `:155` (V1-21, V1-22) | `DATA_DIR` = `paths.DATA_DIR` (`benchmark.py:120`, V1-16); ohne Modus `_LIVE_DATA_DIR` = `<BASE_DIR>/data` (`paths.py:685`, `:194`; V1-64, V1-61), unter dem Modus `_MODUS[0]` (`paths.py:692`, V1-65) | `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); die Wahl hängt nur an `markt` (V1-20, V1-25, V1-26), nicht am Bot oder Zeitrahmen | `grundlage.py:87`, `:90` (V1-45, V1-46); der Kern selbst liest keine Datei (`mtm_kern.py:55`, V1-38), `schlusskurse` ist Parameter (V1-39, V1-41) | `DATA_DIR = os.path.join(REPO_ROOT, "data")` (`grundlage.py:35`, `:34`; V1-43, V1-42) — fester Ordner, nicht über `shared/paths.py` | `<symbol>_1d.csv`, `close` (V1-47) über den Aufruf mit `"1d"` (`messung.py:147`, V1-50) | `tagesschluss`: `benchmark.py:253` mit `"aktien"`/`"krypto"` (V1-25), `test_vorregistrierung.py:1172` (V1-27), ersetzt in `test_ersatzwerte.py:225` (V1-28) · `lade_schlusskurse`: `messung.py:147` `"1d"` (V1-50; je Bot aufgerufen über `alle_bots.py:30`, `:32`, `messung.py:110`; V1-70, V1-71, V1-72; Botliste `grundlage.py:46`, V1-69), `richtungsfall.py:135` `"1d"` (V1-53), `test_mtm_kern.py:121` `"1d"` (V1-54), `grundlage.py:211` Zeitrahmen des Bots (V1-48), `:212` `"1d"` (V1-49) | Lesestellen belegt · Zuordnung zum Bot erschlossen (Markt aus `registerdaten.py`, V1-33) · Ordner im Lauf offen (O7) |
| `elliott_wave_stocks` | aktien, 1d (V1-34) | `benchmark.py:152`, `:155` (V1-21, V1-22) | `DATA_DIR` = `paths.DATA_DIR` (`benchmark.py:120`, V1-16); ohne Modus `_LIVE_DATA_DIR` = `<BASE_DIR>/data` (`paths.py:685`, `:194`; V1-64, V1-61), unter dem Modus `_MODUS[0]` (`paths.py:692`, V1-65) | `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); die Wahl hängt nur an `markt` (V1-20, V1-25, V1-26), nicht am Bot oder Zeitrahmen | `grundlage.py:87`, `:90` (V1-45, V1-46); der Kern selbst liest keine Datei (`mtm_kern.py:55`, V1-38), `schlusskurse` ist Parameter (V1-39, V1-41) | `DATA_DIR = os.path.join(REPO_ROOT, "data")` (`grundlage.py:35`, `:34`; V1-43, V1-42) — fester Ordner, nicht über `shared/paths.py` | `<symbol>_1d.csv`, `close` (V1-47) über den Aufruf mit `"1d"` (`messung.py:147`, V1-50) | `tagesschluss`: `benchmark.py:253` mit `"aktien"`/`"krypto"` (V1-25), `test_vorregistrierung.py:1172` (V1-27), ersetzt in `test_ersatzwerte.py:225` (V1-28) · `lade_schlusskurse`: `messung.py:147` `"1d"` (V1-50; je Bot aufgerufen über `alle_bots.py:30`, `:32`, `messung.py:110`; V1-70, V1-71, V1-72; Botliste `grundlage.py:46`, V1-69), `richtungsfall.py:135` `"1d"` (V1-53), `test_mtm_kern.py:121` `"1d"` (V1-54), `grundlage.py:211` Zeitrahmen des Bots (V1-48), `:212` `"1d"` (V1-49) | Lesestellen belegt · Zuordnung zum Bot erschlossen (Markt aus `registerdaten.py`, V1-34) · Ordner im Lauf offen (O7) |
| `rsi2_mean_reversion` | aktien, 1d (V1-35) | `benchmark.py:152`, `:155` (V1-21, V1-22) | `DATA_DIR` = `paths.DATA_DIR` (`benchmark.py:120`, V1-16); ohne Modus `_LIVE_DATA_DIR` = `<BASE_DIR>/data` (`paths.py:685`, `:194`; V1-64, V1-61), unter dem Modus `_MODUS[0]` (`paths.py:692`, V1-65) | `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); die Wahl hängt nur an `markt` (V1-20, V1-25, V1-26), nicht am Bot oder Zeitrahmen | `grundlage.py:87`, `:90` (V1-45, V1-46); der Kern selbst liest keine Datei (`mtm_kern.py:55`, V1-38), `schlusskurse` ist Parameter (V1-39, V1-41) | `DATA_DIR = os.path.join(REPO_ROOT, "data")` (`grundlage.py:35`, `:34`; V1-43, V1-42) — fester Ordner, nicht über `shared/paths.py` | `<symbol>_1d.csv`, `close` (V1-47) über den Aufruf mit `"1d"` (`messung.py:147`, V1-50) | `tagesschluss`: `benchmark.py:253` mit `"aktien"`/`"krypto"` (V1-25), `test_vorregistrierung.py:1172` (V1-27), ersetzt in `test_ersatzwerte.py:225` (V1-28) · `lade_schlusskurse`: `messung.py:147` `"1d"` (V1-50; je Bot aufgerufen über `alle_bots.py:30`, `:32`, `messung.py:110`; V1-70, V1-71, V1-72; Botliste `grundlage.py:46`, V1-69), `richtungsfall.py:135` `"1d"` (V1-53), `test_mtm_kern.py:121` `"1d"` (V1-54), `grundlage.py:211` Zeitrahmen des Bots (V1-48), `:212` `"1d"` (V1-49) | Lesestellen belegt · Zuordnung zum Bot erschlossen (Markt aus `registerdaten.py`, V1-35) · Ordner im Lauf offen (O7) |
| `turtle_soup_stocks` | aktien, 1d (V1-36) | `benchmark.py:152`, `:155` (V1-21, V1-22) | `DATA_DIR` = `paths.DATA_DIR` (`benchmark.py:120`, V1-16); ohne Modus `_LIVE_DATA_DIR` = `<BASE_DIR>/data` (`paths.py:685`, `:194`; V1-64, V1-61), unter dem Modus `_MODUS[0]` (`paths.py:692`, V1-65) | `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); die Wahl hängt nur an `markt` (V1-20, V1-25, V1-26), nicht am Bot oder Zeitrahmen | `grundlage.py:87`, `:90` (V1-45, V1-46); der Kern selbst liest keine Datei (`mtm_kern.py:55`, V1-38), `schlusskurse` ist Parameter (V1-39, V1-41) | `DATA_DIR = os.path.join(REPO_ROOT, "data")` (`grundlage.py:35`, `:34`; V1-43, V1-42) — fester Ordner, nicht über `shared/paths.py` | `<symbol>_1d.csv`, `close` (V1-47) über den Aufruf mit `"1d"` (`messung.py:147`, V1-50) | `tagesschluss`: `benchmark.py:253` mit `"aktien"`/`"krypto"` (V1-25), `test_vorregistrierung.py:1172` (V1-27), ersetzt in `test_ersatzwerte.py:225` (V1-28) · `lade_schlusskurse`: `messung.py:147` `"1d"` (V1-50; je Bot aufgerufen über `alle_bots.py:30`, `:32`, `messung.py:110`; V1-70, V1-71, V1-72; Botliste `grundlage.py:46`, V1-69), `richtungsfall.py:135` `"1d"` (V1-53), `test_mtm_kern.py:121` `"1d"` (V1-54), `grundlage.py:211` Zeitrahmen des Bots (V1-48), `:212` `"1d"` (V1-49) | Lesestellen belegt · Zuordnung zum Bot erschlossen (Markt aus `registerdaten.py`, V1-36) · Ordner im Lauf offen (O7) |
| `volatility_breakout` | aktien, 1d (V1-37) | `benchmark.py:152`, `:155` (V1-21, V1-22) | `DATA_DIR` = `paths.DATA_DIR` (`benchmark.py:120`, V1-16); ohne Modus `_LIVE_DATA_DIR` = `<BASE_DIR>/data` (`paths.py:685`, `:194`; V1-64, V1-61), unter dem Modus `_MODUS[0]` (`paths.py:692`, V1-65) | `<SYMBOL>_1d.csv`, `close` (V1-21, V1-24); die Wahl hängt nur an `markt` (V1-20, V1-25, V1-26), nicht am Bot oder Zeitrahmen | `grundlage.py:87`, `:90` (V1-45, V1-46); der Kern selbst liest keine Datei (`mtm_kern.py:55`, V1-38), `schlusskurse` ist Parameter (V1-39, V1-41) | `DATA_DIR = os.path.join(REPO_ROOT, "data")` (`grundlage.py:35`, `:34`; V1-43, V1-42) — fester Ordner, nicht über `shared/paths.py` | `<symbol>_1d.csv`, `close` (V1-47) über den Aufruf mit `"1d"` (`messung.py:147`, V1-50) | `tagesschluss`: `benchmark.py:253` mit `"aktien"`/`"krypto"` (V1-25), `test_vorregistrierung.py:1172` (V1-27), ersetzt in `test_ersatzwerte.py:225` (V1-28) · `lade_schlusskurse`: `messung.py:147` `"1d"` (V1-50; je Bot aufgerufen über `alle_bots.py:30`, `:32`, `messung.py:110`; V1-70, V1-71, V1-72; Botliste `grundlage.py:46`, V1-69), `richtungsfall.py:135` `"1d"` (V1-53), `test_mtm_kern.py:121` `"1d"` (V1-54), `grundlage.py:211` Zeitrahmen des Bots (V1-48), `:212` `"1d"` (V1-49) | Lesestellen belegt · Zuordnung zum Bot erschlossen (Markt aus `registerdaten.py`, V1-37) · Ordner im Lauf offen (O7) |

*Nicht der Kern nach Register Z. 11493, getrennt:* `research/exposure_messung/auswertung.py::mtm_reihen` (V1-58) bekommt `kurse` aus `lade_kurse`: Ordner `DATA_DIR = os.path.join(_REPO_ROOT, "data")` (`:32`, V1-55), Datei `<sym>_1d.csv` (`:86`, V1-56), Zeilen ohne Kurs gestrichen (`:91`, V1-68), Spalte `close` (`:96`, V1-57); `mtm_reihen` füllt vor dem ersten Kurs rückwärts auf (`.bfill()`, `:323`, V1-59). Stand: belegt.

**Der Weg zum Snapshot (V1 Nr. 4), beschrieben, nicht beurteilt.** `benchmark.py` bezieht `DATA_DIR` aus `shared/paths.py` (V1-16). Dort hängt der Wert am Modus: `_MODUS = _modus_aus_umgebung()` (`paths.py:679`, V1-63) liest die Umgebung, deren Wurzelvariable `TB_SELEKTIONSWURZEL` heisst (`paths.py:205`, V1-62); ohne Modus `DATA_DIR = _LIVE_DATA_DIR` (V1-64, V1-61), mit Modus `DATA_DIR = _MODUS[0]` (V1-65) und `CONFIG_DIR = <Wurzel>/config` (V1-66). Register Z. 8932: „Ein Modus-Lauf ist ein Lauf unter dem Selektionsmodus des Resolvers (`shared/paths.py`, `TB_SELEKTIONSWURZEL`).“ (V1-67). Die Ladestelle des Kerns nach N4 geht diesen Weg nicht mit: `grundlage.py` nennt den festen Ordner `<REPO_ROOT>/data` (V1-42, V1-43); `TB_SELEKTIONSWURZEL` und `import paths` kommen in `grundlage.py` nicht vor (Suche `V1-4b`, Bereich die fünf Ordner: `TB_SELEKTIONSWURZEL` 20 Treffer in 8 Dateien, `os.path.join(REPO_ROOT, "data")` 1 Treffer, `grundlage.py`). Ob der Lauf damit den Snapshot liest und ob eine Datei gleichen Namens in einem anderen Ordner „eine andere Reihe“ ist, beurteilt die Sitzung nicht (O7).

**Urteil V1 (i) Benchmark: „Spalte und Datei wie die Klammer“** — `tagesschluss` liest für alle neun Bots `close` aus `<SYMBOL>_1d.csv` (V1-21, V1-24); die Wahl hängt nur am Markt (V1-25, V1-26). Ordner als Tatsache: `paths.DATA_DIR`, ohne Modus `data/` der Repo-Wurzel, unter dem Modus die Snapshot-Wurzel.

**Urteil V1 (ii) Kern:** am vorhandenen Kern **„Spalte und Datei wie die Klammer“** — die Tagesreihe des Kerns kommt für jeden Bot aus `<symbol>_1d.csv`, Spalte `close` (V1-47, V1-50); Ordner als Tatsache: fest `data/` der Repo-Wurzel (V1-43). Für den Kern, den der Zellen-Erzeuger übernimmt: **nicht messbar** (O1; V1 Nr. 0: kein Zellen-Erzeuger gefunden).

### V2 — Zeile ohne `close`, und Werte aus Zeilen ab dem Go-Live-Schnitt (R78 (d))

**V2 (a) — Zeile ohne `close`: behalten oder verwerfen** (Suche `V2-a1` in `v2_suche.txt`, Bereich der Code des Laufs nach N5, 49 Dateien). Die Bedingung des gemeinsamen Filters: eine Zeile, in der mindestens eine der Spalten `open`, `high`, `low`, `close` fehlt (`shared/kursdaten.py:54`, `:70`; V2-02, V2-03), wird gestrichen (`:85`, V2-04); gezählt wird je Symbol (`:82`, `:104`; V2-87, V2-88), gemeldet nur bei `melden=True` (`:86`, V2-05) oder als eine Summenzeile über `Zaehler.melde()` (`:121`, V2-89). Der Ordner jeder Ladestelle der Bots ist `DATA_DIR` aus `shared/strategy_paths.py:155` (V2-06), also `paths.DATA_DIR` (V1-64, V1-65).

| Stelle | Lesestelle `Datei:Zeile` | Filter `Datei:Zeile`, Codezeile | Bedingung (Spalten) | behalten / verwerfen | gezählt, gemeldet? | weitere Lesestellen ohne Filter | Stand |
|---|---|---|---|---|---|---|---|
| `elliott_wave_stocks` | `multi_symbol_optimise.py:70` (V2-91) | `:81–82` `entferne_unvollstaendige(df, symbol=symbol, melden=False)` (V2-92, V2-93) | eine von `open`, `high`, `low`, `close` (V2-02, V2-03) | **verwirft** | gezählt (`:83`, V2-94), gemeldet als Summenzeile (`:102`, V2-95; V2-89); dazu streicht `equity_simulation.py:107`, `:111` Trades ohne Ein- oder Ausstiegskurs (V2-105, V2-106) | `backtest_elliott.py:216` liest ohne Filter, nur im Block `if __name__ == "__main__":` (`:212`; V2-146, V2-147) | belegt |
| `rsi2_mean_reversion` | `multi_symbol_optimise.py:65` (V2-107) | `:76` (V2-108) | wie oben | **verwirft** | gezählt (`:78`, V2-109), Summenzeile; Trades ohne Kurs gestrichen `equity_simulation.py:97` (V2-119) | `backtest_rsi2.py` nur im `__main__`-Block (`:182`, V2-148); `buy_and_hold_benchmark.py:34` ohne Filter (V2-151), nicht Teil des Laufs nach N5 | belegt |
| `turtle_soup_stocks` | `multi_symbol_optimise.py:54` (V2-120) | `:65` (V2-121) | wie oben | **verwirft** | gezählt (`:67`, V2-122), Summenzeile; `equity_simulation.py:99` (V2-132) | `backtest_turtle_soup.py` nur im `__main__`-Block (`:179`, V2-149) | belegt |
| `volatility_breakout` | `multi_symbol_optimise.py:61` (V2-133) | `:72` (V2-134) | wie oben | **verwirft** | gezählt (`:74`, V2-135), Summenzeile; `equity_simulation.py:99` (V2-145) | `backtest_breakout.py` nur im `__main__`-Block (`:227`, V2-150) | belegt |
| `benchmark.py::tagesschluss` | `benchmark.py:152`, `:155` (V1-21, V1-22) | `:156` `df = df.dropna(subset=["close"])` (V1-23) | nur `close` | **verwirft** | weder gezählt noch gemeldet (Suche `V1-1a`: in `benchmark.py` keine Zählstelle neben `:156`) | keine weitere Lesestelle in `benchmark.py` (Suche `V1-1a`: `read_csv` 1 Treffer) | Filter belegt · „nicht gezählt“ erschlossen |

*Auskunft ohne Urteil:* Die fünf Krypto-Lader filtern ebenso (`elliott_wave/multi_symbol_optimise.py:72`, `t3_supertrend/…:68`, `rsi2_crypto/…:75`, `turtle_soup_crypto/…:58`, `volatility_breakout_crypto/…:60`; V2-36, V2-47, V2-58, V2-68, V2-78): Bedingung wie oben, verwirft, gezählt, Summenzeile. `grundlage.lade_schlusskurse` verwirft nur nach `close` (`grundlage.py:90`, V1-46), ohne Zählung.

**Urteil V2 (a):** `elliott_wave_stocks` **verwirft** · `rsi2_mean_reversion` **verwirft** · `turtle_soup_stocks` **verwirft** · `volatility_breakout` **verwirft** · `benchmark.py::tagesschluss` **verwirft**. Im Lauf liest keine weitere Stelle dieser Bots eine Kursdatei ohne den Filter; ungefilterte Lesestellen stehen nur in `__main__`-Blöcken und in `buy_and_hold_benchmark.py` (erschlossen: Suche `V2-a1`, `read_csv` 25 Treffer in 24 Dateien des Bereichs; Zuordnung je Treffer in `v2_suche.txt`).

**V2 (b) — Werte aus Zeilen ab dem Go-Live-Schnitt** (`GO_LIVE_SCHNITT = "2026-09-01"`, V2-01). Suchen `V2-b1` und `V2-b2` in `v2_suche.txt`: im Code des Laufs (49 Dateien) `go.live` 0 Treffer, `2026-09` 12 Treffer, alle in Kommentaren oder Docstrings; `bfill|backfill` 0, `shift(-` 0, `center=True` 0. Den Schnitt lesen nur der Faltenplan (`faltenplan.py:326`, V2-25; Falten enden dort, `:312`, V2-26) und über ihn `benchmark.py` (`:280`, `:290`; V2-27, V2-28). Dass die Dateien Zeilen ab dem Schnitt führen, steht in Teil 1 (Z1: alle 174 Tagesreihen enden am 2026-09-01 oder 2026-09-14, `z1.txt`) und für `_1h`/`_4h` in `docs/belege/TB-138/m2.txt` Z. 54–55 (24 der 25 `_1h`-Reihen und alle 24 `_4h`-Reihen enden am 2026-09-14). Nach dem Gestrichen-Filter endet `APH` am 2026-08-31 (`z1.txt`, Zeile `DATEI aktien APH_1d.csv`).

Gemeinsame Stellen, auf die die Zeilen verweisen: **(Z)** Zuteilung ohne Zeitgrenze, Kapital nur an Ausstiegen (`zuteilung.py:703`, `:704`, `:714`, `:722`, `:730`, `:731`; V2-07 bis V2-12) · **(F)** Fenster der Stufen 2 und 3 enden vor dem Einstiegstag (`:334`, `:352`, `:400`, `:401`; V2-13 bis V2-16) · **(S)** der Zufallsschlüssel der Stufe 4 und der Ausstiegsreihenfolge wird auch aus `exit_time`, `exit_price`, `pnl_pct` gebildet (`:492`, `:493`, `:495`, `:540`, `:577`, `:782`; V2-17 bis V2-22) · **(E)** eine Begrenzung am Schnitt kommt im Code des Laufs nicht vor; sie läge nach Plan im Zellen-Erzeuger (Faltenzuordnung, Schnitt der Tagesreihe nach R66 (a)), den es nicht gibt (`v1_erzeuger.md`) · **(B)** Benchmark und Kern begrenzen über `bis` (`benchmark.py:290`, V2-28; `mtm_kern.py:147`, V2-30); `bis` gibt der Aufrufer, `messung.py:156` reicht über den Plan hinaus bis zum letzten Ausstieg (V2-31), gemessen wird je Falte bis `bis` ausschliesslich (`mtm_kern.py:298`, V2-32).

| Bot | Wertart | Wo begrenzt der Code den Zeitraum? `Datei:Zeile`, Codezeile | Grenze (Konstante, Ende der Datei, Parameter) | Wert aus einer Zeile ab dem Schnitt möglich? ja / nein / offen | Begründung an Codezeilen (Kennungen) | Stand |
|---|---|---|---|---|---|---|
| `elliott_wave` | Einstieg | nirgends; Scan über `confirm_idx <= run_bar` (`elliott_wave_counter.py:343`, `:358`; V2-42, V2-43) | Ende der Datei | **ja** | Einstieg auf jeder bestätigten Zeile bis zur vorletzten (V2-43; `backtest_elliott.py:100`, V2-41); vor dem Schnitt: ein umstrittener Platz kann über (S) an Ausstiegswerten ab dem Schnitt hängen | erschlossen |
| `elliott_wave` | Ausstieg | `backtest_elliott.py:82` (V2-38) | Haltedauer, Ende der Datei | **offen** | Ausstieg auf jeder Folgezeile; am Datenende offene Position wird zum `close` der letzten Zeile geschlossen (`:98`, `:99`; V2-39, V2-40) — auch eine vor dem Schnitt eröffnete; ob der Zellen-Erzeuger eine über den Schnitt offene Position mit diesem Ausstieg führt, legt kein gefundener Registertext fest (O5, (E)) | Code belegt · Ausgabe offen |
| `elliott_wave` | Bewertung | Zuteilung (Z): keine Zeitgrenze, Kapital nur an Ausstiegen; Benchmark und Kern (B): `bis` | Parameter `bis` (Plan, Aufrufer) | **offen** | Die Zuteilung bucht Ausstiege ab dem Schnitt ohne Grenze (Z); die tägliche Bewertung (Kern) und der Benchmark schneiden an `bis`, das der Aufrufer gibt — im Lauf der Zellen-Erzeuger (E), nach Plan der Schnitt der Tagesreihe nach R66 (a) | Code belegt · Begrenzung offen |
| `elliott_wave` | Indikatorwert | Zickzack vorwärts (`zigzag_indicator.py:163`, V2-44), Welle erst ab Bestätigung (V2-42) | — | **ja** | Indikatorwerte selbst kausal; aber die Aufnahme des Symbols prüft `len(df)` über die ganze Datei (`multi_symbol_optimise.py:83`, `:50`; V2-37, V2-152), also mit den Zeilen ab dem Schnitt | erschlossen |
| `t3_supertrend` | Einstieg | nirgends (`backtest_trend.py:101`, V2-49) | Ende der Datei | **ja** | Schleife bis zur letzten Zeile (V2-49); vor dem Schnitt (S) | erschlossen |
| `t3_supertrend` | Ausstieg | nirgends | Ende der Datei | **offen** | Ausstieg auf jeder späteren Zeile (`:121`, V2-50); eine am Datenende offene Position wird verworfen (Trade nur im Ausstiegszweig `:127`, Rückgabe `:137`; V2-51, V2-52); Ausgabe nach (E), O5 | Code erschlossen · Ausgabe offen |
| `t3_supertrend` | Bewertung | Zuteilung (Z): keine Zeitgrenze, Kapital nur an Ausstiegen; Benchmark und Kern (B): `bis` | Parameter `bis` (Plan, Aufrufer) | **offen** | Die Zuteilung bucht Ausstiege ab dem Schnitt ohne Grenze (Z); die tägliche Bewertung (Kern) und der Benchmark schneiden an `bis`, das der Aufrufer gibt — im Lauf der Zellen-Erzeuger (E), nach Plan der Schnitt der Tagesreihe nach R66 (a) | Code belegt · Begrenzung offen |
| `t3_supertrend` | Indikatorwert | rekursiv kausal (`indicators.py:23`, V2-53), Regime rückwärts angefügt (`regime_filter.py:43`, V2-54) | — | **ja** | Aufnahme des Symbols über `max()` der ganzen Datei (`multi_symbol_optimise.py:79`, V2-48); fällt `BTCUSDT` heraus, greift die Regimewache (`regimewache.py:86`, V2-55) | erschlossen |
| `rsi2_crypto` | Einstieg | Untergrenze `sma_trend_period`, Obergrenze keine (`backtest_rsi2.py:92`, V2-61); `entry_cutoff` wird nicht übergeben (`equity_simulation.py:63`, V2-60) | Ende der Datei | **ja** | Einstieg bis zur vorletzten Zeile; vor dem Schnitt (S) | erschlossen |
| `rsi2_crypto` | Ausstieg | `backtest_rsi2.py:107` (V2-62) | Haltedauer, Ende der Datei | **offen** | Ausstieg auf jeder späteren Zeile (`:117`, V2-63); am Datenende offene Position verworfen, Scan endet (`:120`, `:121`; V2-64, V2-65): ob ein Einstieg kurz vor dem Schnitt als Trade erscheint, hängt an Zeilen ab dem Schnitt; Ausgabe nach (E), O5 | Code belegt · Ausgabe offen |
| `rsi2_crypto` | Bewertung | Zuteilung (Z): keine Zeitgrenze, Kapital nur an Ausstiegen; Benchmark und Kern (B): `bis` | Parameter `bis` (Plan, Aufrufer) | **offen** | Die Zuteilung bucht Ausstiege ab dem Schnitt ohne Grenze (Z); die tägliche Bewertung (Kern) und der Benchmark schneiden an `bis`, das der Aufrufer gibt — im Lauf der Zellen-Erzeuger (E), nach Plan der Schnitt der Tagesreihe nach R66 (a) | Code belegt · Begrenzung offen |
| `rsi2_crypto` | Indikatorwert | nachlaufend (`indicators.py:21`, V2-66) | — | **ja** | Aufnahme des Symbols über `max()` (`multi_symbol_optimise.py:85`, V2-59) | erschlossen |
| `turtle_soup_crypto` | Einstieg | nur am Anfang; `while i < n` (`backtest_turtle_soup.py:130`, V2-71); kein `entry_cutoff` (`equity_simulation.py:54`, V2-70) | Ende der Datei | **ja** | Einstieg bis zur vorletzten Zeile; vor dem Schnitt (S) | erschlossen |
| `turtle_soup_crypto` | Ausstieg | `backtest_turtle_soup.py:154` (V2-72) | Haltedauer, Ende der Datei | **offen** | Zeitausstieg zum `close` (`:161`, V2-73); offene Position verworfen, Scan endet (`:164`, `:165`; V2-74, V2-75); Ausgabe nach (E), O5 | Code belegt · Ausgabe offen |
| `turtle_soup_crypto` | Bewertung | Zuteilung (Z): keine Zeitgrenze, Kapital nur an Ausstiegen; Benchmark und Kern (B): `bis` | Parameter `bis` (Plan, Aufrufer) | **offen** | Die Zuteilung bucht Ausstiege ab dem Schnitt ohne Grenze (Z); die tägliche Bewertung (Kern) und der Benchmark schneiden an `bis`, das der Aufrufer gibt — im Lauf der Zellen-Erzeuger (E), nach Plan der Schnitt der Tagesreihe nach R66 (a) | Code belegt · Begrenzung offen |
| `turtle_soup_crypto` | Indikatorwert | `low.shift(1).rolling(...)` (`indicators.py:15`, V2-76) | — | **ja** | Aufnahme des Symbols über `max()` (`multi_symbol_optimise.py:67`, V2-69) | erschlossen |
| `volatility_breakout_crypto` | Einstieg | nur am Anfang; `while i < n` (`backtest_breakout.py:135`, V2-81); kein `entry_cutoff` (`equity_simulation.py:73`, V2-80) | Ende der Datei | **ja** | Einstieg bis zur vorletzten Zeile; Regimefilter rückwärts (`regime_filter.py:39`, V2-86); vor dem Schnitt (S) | erschlossen |
| `volatility_breakout_crypto` | Ausstieg | `backtest_breakout.py:157` (V2-82) | Haltedauer, Ende der Datei | **offen** | offene Position verworfen, Scan endet (`:167`, `:168`; V2-83, V2-84); Ausgabe nach (E), O5 | Code belegt · Ausgabe offen |
| `volatility_breakout_crypto` | Bewertung | Zuteilung (Z): keine Zeitgrenze, Kapital nur an Ausstiegen; Benchmark und Kern (B): `bis` | Parameter `bis` (Plan, Aufrufer) | **offen** | Die Zuteilung bucht Ausstiege ab dem Schnitt ohne Grenze (Z); die tägliche Bewertung (Kern) und der Benchmark schneiden an `bis`, das der Aufrufer gibt — im Lauf der Zellen-Erzeuger (E), nach Plan der Schnitt der Tagesreihe nach R66 (a) | Code belegt · Begrenzung offen |
| `volatility_breakout_crypto` | Indikatorwert | nachlaufend (`indicators.py:19`, V2-85) | — | **ja** | Aufnahme des Symbols über `max()` (`multi_symbol_optimise.py:70`, V2-79) | erschlossen |
| `elliott_wave_stocks` | Einstieg | Fensteranfang `cutoff = df["open_time"].max() - …` (`multi_symbol_optimise.py:93`, `:94`, `:54`; V2-97, V2-98, V2-96) | Untergrenze aus der letzten Zeile der Datei; Obergrenze Ende der Datei | **ja** | Welche Zeilen vor dem Schnitt geladen werden, bildet sich aus `max(open_time)` — der letzten Zeile, nach Z1 der 2026-09-01 (bei `APH` nach dem Filter der 2026-08-31); davon hängen Zickzack-Start (`zigzag_indicator.py:160`, V2-104) und alle Einstiege ab; dazu (S) | erschlossen |
| `elliott_wave_stocks` | Ausstieg | `backtest_elliott.py:91` (V2-100) | Ende der Datei | **offen** | am Datenende offene Position zum `close` der letzten Zeile geschlossen (`:107`, `:108`; V2-101, V2-102); Ausgabe nach (E), O5 | Code belegt · Ausgabe offen |
| `elliott_wave_stocks` | Bewertung | Zuteilung (Z): keine Zeitgrenze, Kapital nur an Ausstiegen; Benchmark und Kern (B): `bis` | Parameter `bis` (Plan, Aufrufer) | **offen** | Die Zuteilung bucht Ausstiege ab dem Schnitt ohne Grenze (Z); die tägliche Bewertung (Kern) und der Benchmark schneiden an `bis`, das der Aufrufer gibt — im Lauf der Zellen-Erzeuger (E), nach Plan der Schnitt der Tagesreihe nach R66 (a) | Code belegt · Begrenzung offen |
| `elliott_wave_stocks` | Indikatorwert | Welle erst ab Bestätigung (`elliott_wave_counter.py:343`, V2-103) | — | **ja** | Aufnahme des Symbols über `max()` (`multi_symbol_optimise.py:96`, V2-99), Fensteranfang wie bei Einstieg | erschlossen |
| `rsi2_mean_reversion` | Einstieg | `entry_cutoff = df["open_time"].max() - …` (`multi_symbol_optimise.py:93`, `:52`; V2-112, V2-110), übergeben (`equity_simulation.py:74`, V2-113), Scanbeginn (`backtest_rsi2.py:131`, V2-114) | Untergrenze aus der letzten Zeile der Datei; Obergrenze Ende der Datei | **ja** | Der früheste zulässige Einstieg bildet sich aus der letzten Zeile (2026-09-01 nach Z1); dazu (S) | erschlossen |
| `rsi2_mean_reversion` | Ausstieg | `backtest_rsi2.py:150` (V2-115) | Haltedauer, Ende der Datei | **offen** | offene Position verworfen, Scan endet (`:163`, `:164`; V2-116, V2-117); Ausgabe nach (E), O5 | Code belegt · Ausgabe offen |
| `rsi2_mean_reversion` | Bewertung | Zuteilung (Z): keine Zeitgrenze, Kapital nur an Ausstiegen; Benchmark und Kern (B): `bis` | Parameter `bis` (Plan, Aufrufer) | **offen** | Die Zuteilung bucht Ausstiege ab dem Schnitt ohne Grenze (Z); die tägliche Bewertung (Kern) und der Benchmark schneiden an `bis`, das der Aufrufer gibt — im Lauf der Zellen-Erzeuger (E), nach Plan der Schnitt der Tagesreihe nach R66 (a) | Code belegt · Begrenzung offen |
| `rsi2_mean_reversion` | Indikatorwert | nachlaufend (`indicators.py:23`, V2-118) | — | **ja** | Aufnahme des Symbols über `max()` (`multi_symbol_optimise.py:86`, V2-111) | erschlossen |
| `turtle_soup_stocks` | Einstieg | `entry_cutoff` aus `max()` (`multi_symbol_optimise.py:81`, `:46`; V2-125, V2-123), übergeben (`equity_simulation.py:79`, V2-126), Scanbeginn (`backtest_turtle_soup.py:122`, V2-127) | Untergrenze aus der letzten Zeile der Datei; Obergrenze Ende der Datei | **ja** | wie `rsi2_mean_reversion`; dazu (S) | erschlossen |
| `turtle_soup_stocks` | Ausstieg | `backtest_turtle_soup.py:150` (V2-128) | Haltedauer, Ende der Datei | **offen** | offene Position verworfen, Scan endet (`:160`, `:161`; V2-129, V2-130); Ausgabe nach (E), O5 | Code belegt · Ausgabe offen |
| `turtle_soup_stocks` | Bewertung | Zuteilung (Z): keine Zeitgrenze, Kapital nur an Ausstiegen; Benchmark und Kern (B): `bis` | Parameter `bis` (Plan, Aufrufer) | **offen** | Die Zuteilung bucht Ausstiege ab dem Schnitt ohne Grenze (Z); die tägliche Bewertung (Kern) und der Benchmark schneiden an `bis`, das der Aufrufer gibt — im Lauf der Zellen-Erzeuger (E), nach Plan der Schnitt der Tagesreihe nach R66 (a) | Code belegt · Begrenzung offen |
| `turtle_soup_stocks` | Indikatorwert | `low.shift(1).rolling(...)` (`indicators.py:15`, V2-131) | — | **ja** | Aufnahme des Symbols über `max()` (`multi_symbol_optimise.py:74`, V2-124) | erschlossen |
| `volatility_breakout` | Einstieg | `entry_cutoff` aus `max()` (`multi_symbol_optimise.py:89`, `:50`; V2-138, V2-136), übergeben (`equity_simulation.py:75`, V2-139), Scanbeginn (`backtest_breakout.py:172`, V2-140) | Untergrenze aus der letzten Zeile der Datei; Obergrenze Ende der Datei | **ja** | wie `rsi2_mean_reversion`; dazu (S) | erschlossen |
| `volatility_breakout` | Ausstieg | `backtest_breakout.py:198` (V2-141) | Haltedauer, Ende der Datei | **offen** | offene Position verworfen, Scan endet (`:208`, `:209`; V2-142, V2-143); Ausgabe nach (E), O5 | Code belegt · Ausgabe offen |
| `volatility_breakout` | Bewertung | Zuteilung (Z): keine Zeitgrenze, Kapital nur an Ausstiegen; Benchmark und Kern (B): `bis` | Parameter `bis` (Plan, Aufrufer) | **offen** | Die Zuteilung bucht Ausstiege ab dem Schnitt ohne Grenze (Z); die tägliche Bewertung (Kern) und der Benchmark schneiden an `bis`, das der Aufrufer gibt — im Lauf der Zellen-Erzeuger (E), nach Plan der Schnitt der Tagesreihe nach R66 (a) | Code belegt · Begrenzung offen |
| `volatility_breakout` | Indikatorwert | nachlaufend (`indicators.py:25`, V2-144) | — | **ja** | Aufnahme des Symbols über `max()` (`multi_symbol_optimise.py:82`, V2-137) | erschlossen |

Zählung der 36 Zeilen: **ja** 18 (Einstieg 9, Indikatorwert 9) · **nein** 0 · **offen** 18 (Ausstieg 9, Bewertung 9).

**Urteil V2 (b): „ein solcher Wert wird gebildet“** — je Bot und zusammen, bei allen neun Bots. Die Stellen einzeln: (1) Aufnahme eines Symbols aus der ganzen Datei, also mit den Zeilen ab dem Schnitt: `max()` bzw. `len()` in allen neun Ladern (V2-37, V2-48, V2-59, V2-69, V2-79, V2-99, V2-111, V2-124, V2-137). (2) Bei den vier Aktien-Bots die Untergrenze der Einstiege bzw. der geladenen Zeilen aus `max(open_time)` (V2-97, V2-112, V2-125, V2-138). (3) In der Zuteilung bei allen neun der Zufallsschlüssel der Stufe 4 aus Ausstiegswerten (S). Daneben offen: Ausstieg und Bewertung ab dem Schnitt bildet der vorhandene Code (belegt), ob sie in eine Ausgabe nach R39 eingehen, entscheidet erst der Zellen-Erzeuger (E, O5). Nach der Klammer zu R78 (d) ist das zu melden und geht vor dem Tag an den Verfahrensprüfer.

### V3 — nicht endliche Werte in `zellen.csv` und `zellenbericht.csv` (R78 (e))

**V3 Nr. 1 — die registrierten Definitionen der Felder von `zellen.csv` und `zellenbericht.csv`.** Suchen `V3-1a` und `V3-1b` in `v3_suche.txt` (Bereich: die eine Datei `docs/VORREGISTRIERUNG_neuselektion.md`). Die Feldliste von `zellen.csv` ist die aus 50.2 (V3-01 bis V3-03), ergänzt durch R36 (V3-08 bis V3-10); für `zellenbericht.csv` führt 50.2 keine Feldliste (V3-24), die Felder nennt R34 (V3-15, V3-16). Die Sitzung stellt die Wortlaute nebeneinander und deutet nicht.

| Datei | Feld | Registerstelle (Block, Zeile) | Wortlaut der Definition (höchstens 300 Zeichen) | nennt die Definition einen Fall ohne Zahl? (Wortlaut) | nennt sie dafür einen Wert oder ein Wort? (Wortlaut) | Stand |
|---|---|---|---|---|---|---|
| `zellen.csv` | `zelle_id`, je Rasterachse eine Spalte, `falte`, `rolle` | 50.2, Z. 11066 (V3-01) | „zelle_id, <je Rasterachse eine Spalte>, falte, rolle, n_trades,“ | sagt nichts | sagt nichts | belegt |
| `zellen.csv` | `n_trades` | 50.2, Z. 11066 (V3-01); R33, Z. 10797 (V3-04) | „Eine (Zelle, Falte) ohne Trades trägt die Nullzeile: Trade-Zahl 0, Sharpe 0 nach 1c, Drawdown 0, nie nichts.“ | „ohne Trades“ | „Trade-Zahl 0“ | belegt |
| `zellen.csv` | `netto_sharpe` | 50.2, Z. 11067 (V3-02); 15.3 (c), Z. 1442–1443 (V3-05, V3-06); Formel Z. 1455 (V3-07); R33 (V3-04) | „*Formel für den Falten-Sharpe: Mittel / Standardabweichung der täglichen“ (Z. 1455) | „Ist die Standardabweichung 0 (kein Trade in der Falte), ist der“ / „Falten-Sharpe 0.“ (Z. 1442–1443); „ohne Trades“ (R33) | „Falten-Sharpe 0“; „Sharpe 0 nach 1c“ | belegt |
| `zellen.csv` | `netto_rendite_pct` | 50.2, Z. 11067 (V3-02); Messtabelle zu R54, Z. 11052 (V3-25) | nur der Feldname in der Liste; Z. 11052: „gelesen nur für die Bestätigungsperiode (Z. 624) … Berichtsgrösse ohne Leser im Urteil“ | sagt nichts | sagt nichts | belegt |
| `zellen.csv` | `kapital_drawdown_pct` (Feldliste 50.2) | 50.2, Z. 11067 (V3-02); R36, Z. 10827 (V3-10) | „Die Spalte kapital_drawdown_pct wird durch die zwei benannten ersetzt, nicht umgedeutet.“ | sagt nichts | sagt nichts | belegt |
| `zellen.csv` | `kapital_drawdown_mtm_pct` | R36, Z. 10827 (V3-08, V3-11); R33 (V3-04) | „zellen.csv trägt je (Zelle, Falte) kapital_drawdown_mtm_pct — den Kapital-Drawdown der Nebenbedingung auf der täglichen MtM-Reihe (1a) auf den Tagen des Benchmarks (3b (c))“ | „ohne Trades“ (R33) | „Drawdown 0“ (R33) | belegt |
| `zellen.csv` | `kapital_drawdown_ereignis_pct` | R36, Z. 10827 (V3-09); R33 (V3-04) | „und kapital_drawdown_ereignis_pct — den ereignisindizierten Drawdown, berichtet, nicht bewertet (24.2).“ | „ohne Trades“ (R33) | „Drawdown 0“ (R33) | belegt |
| `zellen.csv` | `mittlere_exposure` | 50.2, Z. 11068 (V3-03); R48 (d), Z. 10936 (V3-12); R64 (a), Z. 11342 (V3-13) | „Mittlere Exposure = Mittel über die Handelstage des Zeitraums (Krypto Kalendertage, 15.4 Anmerkung 1) des Anteils des Kapitals in offenen Positionen am Tagesschluss, bewertet wie die MtM-Reihe (1a).“ | sagt nichts (ein Mittel; zu einer leeren Menge von Tagen nach R64 (a) sagt die Stelle nichts) | sagt nichts | belegt |
| `zellen.csv` | alle Grössen der Zeile der Bestätigungsperiode | R68 (a), Z. 11431 (V3-14) | „Alle Grössen dieser Zeile stehen auf den Tagen ab bestaetigung_ab_effektiv der Zelle bis zum Ende der Spanne (35.1).“ | sagt nichts (zu einer leeren Menge solcher Tage sagt die Stelle nichts) | sagt nichts | belegt |
| `zellenbericht.csv` | Ertragsanteil der besten Selektionsfalte | R34, Z. 10810 (V3-15, V3-16, V3-17) | „Anteil = Beitrag ÷ Gesamtertrag; bei Gesamtertrag ≤ 0 wird kein Anteil gebildet, das Feld trägt „nicht definiert“.“ | „bei Gesamtertrag ≤ 0 wird kein Anteil gebildet“ | „nicht definiert“ | belegt |
| `zellenbericht.csv` | Ertragsanteil des besten Symbols | R34, Z. 10810 (V3-16, V3-17) | wie oben | „bei Gesamtertrag ≤ 0 wird kein Anteil gebildet“ | „nicht definiert“ | belegt |
| `zellenbericht.csv` | Ertragsanteil der fünf besten Trades | R34, Z. 10810 (V3-16, V3-17) | wie oben | „bei Gesamtertrag ≤ 0 wird kein Anteil gebildet“ | „nicht definiert“ | belegt |
| `zellenbericht.csv` | `haltedauer_median_handelstage` | R34, Z. 10810 (V3-16); R41, Z. 10880 (V3-18); 15.3 (b), Z. 1435 (V3-19) | „haltedauer_balken ist die Zahl der Kerzen des Zeitrahmens des Bots von der Einstiegskerze bis zur Ausstiegskerze, beide eingeschlossen“ | sagt nichts (ein Median; zu einer Zelle ohne Trade sagt die Stelle nichts) | sagt nichts | belegt |
| `zellenbericht.csv` | `bestaetigung_ab_effektiv` | R34, Z. 10810 (V3-16); R37 (i), Z. 10837 (V3-20, V3-21) | „Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position des Gewinners mehr offen ist“ | sagt nichts (ein Tag, kein Zahlenwert) | sagt nichts | belegt |

Daneben, ohne Feld der zwei Dateien: R67 verlangt „jeder Zahlenwert endlich“ für die Tagesreihen und die Benchmark-Tagesreihen (V3-22) und sagt „Für zellen.csv gilt R33.“ (V3-23).

**Zählung V3 (i):** 14 Zeilen der Tabelle (11 Felder von `zellen.csv` nach 50.2 und R36, als 8 Zeilen geführt, dazu die Zeile der Bestätigungsperiode; 5 Felder von `zellenbericht.csv` nach R34). Die Definition nennt einen Fall ohne Zahl: 7 Zeilen (`n_trades`, `netto_sharpe`, `kapital_drawdown_mtm_pct`, `kapital_drawdown_ereignis_pct`, die drei Ertragsanteile). Die Definition sagt nichts: 7 Zeilen. Unter den 7 mit einem Fall nennen 4 dafür einen Zahlenwert (0) und 3 ein Wort („nicht definiert“).

**V3 Nr. 2 — `auswertung.py` und nicht endliche Werte in `zellen.csv`.** Suchen `V3-2a` bis `V3-2c` in `v3_suche.txt` (Bereich: die eine Datei `research/vorregistrierung/auswertung.py`): `isfinite` 0, `isinf` 0, `finite` 0, `isna` 1 (Z. 355), `notna` 0, `fillna` 0, `dropna` 0, `np.inf` 0, `zellenbericht` 0 Treffer. Werkzeugprobe in `v3_suche.txt`: `pandas.isna` meldet in der Umgebung (pandas 2.3.3) NaN als fehlend, +inf und −inf nicht.

| Spalte | gelesen in `Datei:Zeile` | Prüfung `Datei:Zeile`, Codezeile | fängt NaN / +inf / −inf | Folge, Rückgabewert (Kennung) | Stand |
|---|---|---|---|---|---|
| `netto_sharpe` | `auswertung.py:353–354`, `:395`, `:577`, `:684` (V3-34, V3-35, V3-38, V3-42, V3-48) | `auswertung.py:355` `if df["netto_sharpe"].isna().any():` (V3-36), nach dem Setzen auf 0.0 bei `n_trades == 0` (V3-34) | NaN ja (in Falten mit Trade) · +inf nein · −inf nein | `raise Abbruch(…)` (`:356`, V3-37); `Abbruch` ist `SystemExit` mit `paths.RUECKGABEWERT_STARTPRUEFUNG` (`:137`, `:146`; V3-28, V3-29) = 2 (`paths.py:220`, V3-30) | Prüfung belegt · „±inf nicht gefangen“ erschlossen (Werkzeugprobe `isna`, Suche 0 Treffer `isinf`/`isfinite`) |
| `n_trades` | `auswertung.py:353`, `:621`, `:687` (V3-34, V3-43, V3-49) | keine | nein / nein / nein | keine Prüfung; Folge nicht gemessen (kein Lauf) | erschlossen (Suche `V3-2a`: 0 Treffer der Prüfmuster ausser Z. 355) |
| `netto_rendite_pct` | `auswertung.py:624` (V3-44) | keine | nein / nein / nein | keine Prüfung | erschlossen (wie oben) |
| `kapital_drawdown_pct` | `auswertung.py:413–414`, `:625`, `:681` (V3-40, V3-41, V3-45, V3-47) | keine | nein / nein / nein | keine Prüfung; der Vergleich `>= grenze` in `:414` (V3-41) läuft ohne Prüfung | erschlossen (wie oben) |
| `mittlere_exposure` | `auswertung.py:405`, `:626` (V3-39, V3-46) | keine | nein / nein / nein | keine Prüfung | erschlossen (wie oben) |
| `zelle_id`, `falte`, `rolle` | `auswertung.py:326` (V3-32) | Pflichtspalten `:133–134` (V3-26, V3-27), Abbruch bei fehlender Spalte `:329` (V3-33) | keine Zahlenspalten | Abbruch mit 2 nur bei fehlender Spalte | belegt |

`auswertung.py` liest `zellenbericht.csv` nicht (Suche `V3-2a`: 0 Treffer). Der einzige `except` in der Datei steht in `lies_herkunft` (`:179`, V3-50). Die Ausgänge der Datei nach ihrem Docstring: „Ausgaenge von `auswertung.py`: 0 oder 2, kein 1“ (`:140`, V3-51).

**Urteil V3 (ii): „trifft teils zu“** — `auswertung.py` beendet einen nicht endlichen Wert in `zellen.csv` mit 2 nur für die Spalte `netto_sharpe` und nur für NaN in einer Falte mit Trade (V3-36, V3-37, V3-29, V3-30); +inf und −inf in `netto_sharpe` und jeder nicht endliche Wert in `n_trades`, `netto_rendite_pct`, `kapital_drawdown_pct` und `mittlere_exposure` werden nicht geprüft. Kein Probelauf (Verbot „Kein Lauf“).

### Belegt · Erschlossen · Offen

**Belegt** (steht in der genannten Zeile): Die Lesestellen von `tagesschluss` und `lade_schlusskurse` mit Ordner, Datei und
Spalte (V1-16 bis V1-26, V1-42 bis V1-50); der Filter je Lader und in `tagesschluss` (V2-02 bis V2-05, V1-23); die
Bildung von `entry_cutoff` und Fensteranfang aus `max(open_time)` bei den vier Aktien-Bots (V2-97, V2-112, V2-125, V2-138)
und der Spanne aus `max()` bzw. `len()` in allen neun Ladern; das Verhalten am Datenende je Backtest; die Felder des
Zufallsschlüssels (V2-17, V2-18); die eine Prüfung in `auswertung.py` (V3-36) und ihr Rückgabewert 2 (V3-29, V3-30).

**Erschlossen** (Ketten): (1) Kein Zellen-Erzeuger: Suchmuster, Bereich 482 Dateien, Trefferzahlen in `v1_erzeuger.md`. (2) Die
Zuordnung „alle neun Bots“ bei `tagesschluss`: `tagesschluss(markt)` → `je_bot` ruft es für „aktien“ und „krypto“ (V1-25) →
je Bot `kurse[eig["markt"]]` (V1-26) → Markt und Zeitrahmen je Bot aus `registerdaten.py` (V1-29 bis V1-37). (3) Der
Zeilenwert ab dem Schnitt: die Dateien führen solche Zeilen (Z1; `docs/belege/TB-138/m2.txt` Z. 54–55) → `max()`/`len()`
über die ganze Datei (V2-37 …) → Aufnahme des Symbols bzw. `entry_cutoff`. (4) Stufe 4: Zufallsschlüssel aus Ausstiegswerten
(V2-17 bis V2-19) → Wahl bei Gleichstand (V2-21, V2-22) → ein Platz vor dem Schnitt kann an einem Ausstieg ab dem Schnitt
hängen; wie oft das eintritt, ist nicht gemessen. (5) „±inf nicht gefangen“: `isna` als einzige Prüfung (Suche `V3-2a`) und
die Werkzeugprobe (`pandas.isna`: NaN ja, ±inf nein).

**Offen** (was fehlt): Der Kern, den der Zellen-Erzeuger übernimmt (O1; es gibt keinen Erzeuger) · ob Ausstieg und Bewertung ab
dem Schnitt in eine Ausgabe nach R39 eingehen (der Erzeuger fehlt; O5) · der Ordner im Lauf (O7) · die Werte der
Bibliothekskonstanten `Client.KLINE_INTERVAL_1HOUR` und `…_4HOUR` (sie stehen in `trading-env`, nicht gelesen; der Dateiname
`_1h`/`_4h` ist daraus erschlossen, nicht belegt) · was `kennzahlen.py`, das `auswertung.py` aufruft, mit nicht endlichen
Werten tut (nicht im Bereich von V3 Nr. 2).

## Lesarten N1 bis N7 und offene Punkte O1 bis O7: woran welche Aussage hängt

| | woran es hängt |
|---|---|
| **N1** | V4. Weil W1 und W2 beide 67/67 zeigen und die Plattform gleich ist, hängt das Urteil nicht daran, ob „gleich“ über `version(name)` oder über `distributions()` gelesen wird |
| **N2** | V5. Ausschnitt und Aufruf sind als Mengen gleich, der Index ohne Doppel; das Urteil hängt an Beginn (L4) und Ende (L3) des Vorgängers |
| **N3** | V6. Mit (ii) und (iii) gilt die Aussage für den committeten Stand und für den Arbeitsbaum |
| **N4** | V1 (ii). Ohne Erzeuger misst die Sitzung am vorhandenen Kern (`mtm_kern.py` mit `grundlage.lade_schlusskurse`); die Aussage über den Kern des Erzeugers heisst „nicht messbar“ |
| **N5** | V2. Das Urteil (b) hängt daran, dass Lader und Zuteilung zum Code des Laufs gehören: Ohne die Lader fielen die Stellen (1) und (2) weg, ohne die Zuteilung (3) |
| **N6** | V3 (ii). NaN fängt die Prüfung, ±inf nicht |
| **N7** | V1 (i), V2 (a). `benchmark.py` wurde gelesen, nicht geändert, nicht ausgeführt, nicht importiert (D3: `numstat` nur unter `docs/`) |
| **O1** | offen; V1 (ii) „nicht messbar“ für den Kern des Erzeugers |
| **O2** | gemessen: `platform.platform()` liefert heute den Wert des Locks |
| **O3** | gemessen: W1 = W2, siehe V4 |
| **O4** | Ausser 50.2, R33, R34, R36 und R68 legen fest oder ergänzen: 15.3 (c) mit der Formel (Z. 1442–1443, Z. 1455), R48 (d) (Z. 10936), R64 (a) (Z. 11342), R37 (i) (Z. 10837), R41 (Z. 10880), 15.3 (b) (Z. 1435); R67 (Z. 11424) für die Tagesreihen |
| **O5** | Der Code: `elliott_wave` und `elliott_wave_stocks` schliessen eine am Datenende offene Position zum `close` der letzten Zeile (V2-39, V2-40, V2-101, V2-102); die übrigen sieben verwerfen sie und beenden den Scan des Symbols (V2-52, V2-64/65, V2-74/75, V2-83/84, V2-116/117, V2-129/130, V2-142/143). Einen Registersatz dazu hat die Sitzung nicht gesucht; sie deutet nichts |
| **O6** | nicht gebraucht |
| **O7** | Ordner je Stelle in `v1_spalte.md`: `benchmark.py` über `paths.DATA_DIR` (ohne Modus `data/`, mit Modus die Snapshot-Wurzel), `grundlage.py` fest `data/`; Frage unter „Für Fable“ |

## Für den steuernden Chat

| Teilfrage | Urteil | Tatsache, wie sie als Tatsachennotiz stehen könnte (Fundstelle) |
|---|---|---|
| V4 | *erfüllt* | In `trading-env` liefert `importlib.metadata.version` für alle 67 Zeilen des Locks die Fassung der Zeile, Interpreter und Plattform sind die des Locks (`v4.txt`, Zeilen `KOPF`, `W1 gleich 67 von 67`) |
| V5 | *erfüllt* | Ein eigener Aufruf von `schedule` je Aktien-Bot liefert dieselben Tage wie der Ausschnitt der Menge 1962-01-02..2026-09-01: 2 428 bzw. 2 177 Tage (`v5.txt`) |
| V6 | *erfüllt* | Am Stand `0779453` führt `data/APH_1d.csv` genau eine Zeile 2026-09-01 ohne `close`; die Arbeitsdatei trägt denselben Blob, ist seit 2026-09-02 unverändert, kein Commit nach dem Stand (`v6.txt`, Zeile `TEIL`) |
| Z1 | *erfüllt* | Im Snapshot fehlt `close` in den 150 Aktien-Tagesreihen nur in `APH_1d.csv` 2026-09-01, in den 24 Krypto-Tagesreihen in keiner Zeile (`z1.txt`, Zeilen `SUMME`) |
| Z2 | „nur erschliessbar“ | `ERGEBNIS_TB-47` nennt die Cloud-Sitzung (Z. 3) und die dort nachinstallierte Fassung 5.4.0 für Teil 1–4 (Z. 359, Z. 122), aber keine Zeile verbindet sie mit `eingaben.json` oder dem Feld `kalender` (`z2_stellen.md`) |
| V1 Nr. 0 | „kein Zellen-Erzeuger gefunden“ | Keine der 482 verfolgten Python-Dateien ausserhalb von `docs/` schreibt eine Ausgabe aus R39 aus Kursdaten (`v1_erzeuger.md`, `v1_suche.txt`) |
| V1 (i) | „Spalte und Datei wie die Klammer“ | `benchmark.py::tagesschluss` liest für alle neun Bots `close` aus `<SYMBOL>_1d.csv` in `paths.DATA_DIR` (V1-21, V1-24, V1-16) |
| V1 (ii) | am vorhandenen Kern „Spalte und Datei wie die Klammer“; Kern des Erzeugers „nicht messbar“ | `grundlage.lade_schlusskurse` liefert dem Kern `close` aus `<symbol>_1d.csv` im festen Ordner `data/` der Repo-Wurzel (V1-43, V1-45, V1-47, V1-50) |
| V2 (a) | verwirft (alle fünf Stellen) | Die vier Aktien-Lader streichen jede Zeile, in der eine der vier Kursspalten fehlt, gezählt und als Summenzeile gemeldet; `tagesschluss` streicht Zeilen ohne `close`, ohne Zählung (V2-02 bis V2-05, V1-23) |
| V2 (b) | „ein solcher Wert wird gebildet“ | Alle neun Lader bilden die Aufnahme eines Symbols aus der ganzen Datei, die vier Aktien-Lader den frühesten Einstieg aus `max(open_time)`; die Zuteilung bildet den Schlüssel der Stufe 4 aus Ausstiegswerten (`v2_lader_schnitt.md`) |
| V3 (i) | Zählung: 14 Zeilen, 7 mit Fall ohne Zahl (4 mit Wert 0, 3 mit „nicht definiert“), 7 „sagt nichts“ | `v3_endlich.md`, erste Tabelle |
| V3 (ii) | „trifft teils zu“ | `auswertung.py` endet mit 2 nur bei NaN in `netto_sharpe` einer Falte mit Trade; ±inf und die übrigen Zahlenspalten prüft es nicht (V3-36, V3-37, V3-29, V3-30) |

Wohin was geht:

- Der Registereintrag TB-139 braucht V4, V5, V6, Z1 und Z2.
- Vor dem signierten Tag an den Verfahrensprüfer geht jeder Befund aus V2 (b) (so die Klammer) und die Tabelle zu V3 (i) (für V3 (i) ist der Zeitpunkt Setzung des steuernden Chats; die Klammer zu R78 (e) nennt keinen).
- V1 — jede Stelle, die eine andere Spalte oder eine Datei anderen Namens liest (keine gefunden), dazu der Ordner je Stelle, die Beschreibung aus V1 Nr. 4 und O7 — steht unter „Für Fable“ und als Tatsache für „Voraussetzungen und Befunde“ des Registerauftrags.
- V2 (a) geht mit V2 (b) an den Verfahrensprüfer, weil V2 (b) einen Befund trägt.
- V3 (ii) geht als Tatsache an den steuernden Chat, für den Bau des Zellen-Erzeugers, und unter „Für Fable“ zur Kenntnis; ob die Prüfung „genügt“, entscheidet der Verfahrensprüfer.
- Wo die Klammer kein Ziel und keinen Zeitpunkt nennt, sind diese Ziele Setzung des steuernden Chats, vorläufig.

**Nachtrag 07.10.2026, 10:32 in `UEBERGABE.md` — die Angaben für E1 und J1 Nr. 4 und Nr. 5, je mit Zeile:** dass es die Bewertung
gibt: Z. 1751 · keine Abweichung gegen einen Messwert in einem Block: Z. 1763 · Abnahme durch einen Helfer, nur lesend:
Z. 1751, Z. 1763 · acht Abweichungen und Befunde für „Voraussetzungen und Befunde“: Z. 1766–1774 · zwei davon Aussagen eines
Blocks ohne Beleg, dafür Z1 und Z2: Z. 1769, Z. 1770, Z. 1795 · die Nachzählung (174 Dateien, eine Zeile ohne `close`, 150 und
24 Reihenenden): Z. 1764 · nicht nachgerechnet: Z. 1764; nicht gemessen: Z. 1781 · TB-140 misst die sechs Voraussetzungen
und zwei Belege: Z. 1785 · TB-140 vor TB-139: Z. 1786 · TB-139 trägt genau R78 bis R80 als Abschnitt 55: Z. 1787 · die
Einzelfreigabe steht aus: Z. 1788 · TB-137 steht aus: Z. 1788. **Keine Angabe fehlt.**

## Für Fable

1. **V2 (b), Befund nach der Klammer zu R78 (d):** Alle neun Lader entscheiden über die Aufnahme eines Symbols aus der Spanne
   der ganzen Datei (`max()` bzw. `len()`), die vier Aktien-Lader setzen den frühesten Einstieg (bzw. bei `elliott_wave_stocks`
   den Anfang der geladenen Zeilen) auf `max(open_time)` minus zehn Jahre; die letzte Zeile ist im Snapshot der 2026-09-01
   (Aktien) bzw. der 2026-09-14 (Krypto). Die Zuteilung bildet den Schlüssel der Stufe 4 auch aus `exit_time`, `exit_price`,
   `pnl_pct`. Ist das ein „Wert einer Ausgabe des Laufs aus einer Zeile mit Datum ab dem Go-Live-Schnitt“, und ist (d) neu zu
   entscheiden?
2. **O5:** Zwei Bots schliessen eine am Datenende offene Position zum letzten `close`, sieben verwerfen sie und beenden den
   Scan des Symbols; ob ein Einstieg kurz vor dem Schnitt als Trade erscheint, hängt damit an Zeilen ab dem Schnitt. Was gilt
   im Lauf für eine Position, die über den Schnitt offen ist?
3. **O7:** Die Ladestelle des vorhandenen Kerns nennt den festen Ordner `data/`, die Benchmark-Lesestelle den Resolver. Ist
   eine Datei gleichen Namens in einem anderen Ordner als dem Snapshot „eine andere Reihe“ im Sinn von R78 (a)?
4. **V3 (ii) zur Kenntnis:** `auswertung.py` fängt NaN in `netto_sharpe` (Falten mit Trade) mit 2, sonst nichts. Genügt das im
   Sinn der Klammer zu R78 (e)?
5. **V3 (i):** Bei sieben Zeilen sagt die Definition nichts zu einem Fall ohne Zahl, darunter `mittlere_exposure` (Mittel über
   eine Menge von Tagen) und `haltedauer_median_handelstage` (Median). Darf eines dieser Felder nicht endlich sein?
6. **Z2:** R79 (f) sagt „stammt nach `docs/ERGEBNIS_TB-47_snapshotgrenze.md` aus der Cloud-Sitzung vom 18.09.2026“. Die Datei
   belegt die Cloud-Sitzung und die dort installierte Fassung, verbindet sie aber nicht mit dem Feld. Bleibt der Satz so?
7. **V2 (a) zur Kenntnis:** Die Lader streichen eine Zeile, wenn eine der vier Kursspalten fehlt; `tagesschluss` nur, wenn
   `close` fehlt. Am Snapshot macht das keinen Unterschied (Z1 zählt nur `close`; ob andere Kursspalten fehlen, ist nicht gemessen).

## Nicht getan

- Kein Lauf von Code des Repos ausser `shared/snapshot.py --pruefen` ohne `--json` in 0b und D0; kein Import eines Moduls des
  Repos in ein Messskript. Kein Probelauf von `auswertung.py`, `benchmark.py` oder einem Lader.
- Nichts an Code, Register, Abbild, Lock, Daten oder Snapshot geändert (D3: `numstat` nur unter `docs/`). Kein Registereintrag,
  keine Marke. Keine Kurse, Renditen, Kennzahlen oder Trade-Zahlen in einem Beleg; aus `live_params.py` kein Text (in
  `fundstellen.tsv` 0 Zeilen aus einer solchen Datei).
- **Sichtschutz, Abweichung bei einem Helfer:** Ein Lese-Helfer meldet, dass zwei frühe `grep -rn … --include=*.py .` (Suche
  nach `GO_LIVE_SCHNITT` und „Zellen-Erzeuger“) auch die gesperrten Ordner (`data/`, `snapshots/`, `trading-env/`, `logs/`,
  `…/ergebnisse/`) durchsuchten — nur Python-Dateien; die Ausgabe hat er nach eigener Angabe gefiltert, aus diesen Ordnern
  wurde nichts angezeigt; beide Suchen hat er mit Ausschluss dieser Ordner wiederholt. In die Belege ist daraus nichts
  eingegangen: Die Suchen dieses Ergebnisses laufen über `suche.py` mit benanntem Bereich.
- Werkzeuge über die Skizzen hinaus: `fundstellen_bauen.py` mit `fundstellen_v2.py` (baut die Liste aus den Dateien),
  `fundstellen_pruefen.py`, `fundstellen_gegenprobe.sh`, `v1_suche.sh`, `v2_suche.sh`, `v3_suche.sh` (die Werkzeugprobe zu
  `pandas.isna` steht in `v3_suche.sh`), `n_platzhalter.txt`. Alle Skizzen des Auftrags liefen unverändert.

## In einfacher Sprache

Der Prüfer hatte sechs Sätze geschrieben, die nur gelten, wenn etwas stimmt, das noch niemand nachgemessen hatte. Die drei
schnellen Fragen sind beantwortet: Auf dem Mac sind alle 67 festgeschriebenen Programmpakete in genau der festgeschriebenen
Fassung installiert, das Betriebssystem ist das festgeschriebene; der Börsenkalender liefert für jeden Aktien-Bot einzeln
dieselben Handelstage wie einmal für alles; und die Zeile ohne Schlusskurs bei APH stand schon in dem Stand vom 2. Oktober.
Auch die zwei Nachweise sind da: In den Krypto-Tagesdateien fehlt nirgends ein Schlusskurs. Dass die Fassung 5.4.0 aus einer
Cloud-Sitzung stammt, sagt der ältere Bericht aber nur mittelbar: Er nennt die Cloud und die Fassung, verbindet sie aber nicht
ausdrücklich mit der Messdatei. Beim Lesen der Programme zeigte sich: Ein Programm, das die Ergebnistabellen des grossen
Laufs schreibt, gibt es noch nicht. Der Vergleichsmassstab und der vorhandene Bewertungskern lesen die richtige Spalte aus der
richtigen Datei; Zeilen ohne Schlusskurs werden überall weggelassen. Aber: Die Programme schneiden nirgends am 1. September
2026 ab. Ob eine Aktie überhaupt mitgerechnet wird und ab wann die Aktien-Bots einsteigen dürfen, hängt am letzten Datum der
Datei, und das liegt nach dem Stichtag. Das muss der Prüfer vor dem Tag entscheiden. Das Auswertungsprogramm bricht bei „keine
Zahl“ nur in einer Spalte ab, bei „unendlich“ gar nicht. Repariert wurde nichts.
