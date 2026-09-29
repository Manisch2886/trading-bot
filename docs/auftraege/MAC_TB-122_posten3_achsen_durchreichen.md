# TB-122 TB-30b Posten 3 (E-1): drei Rasterachsen durchreichen — `sma_trend_filter` bei `rsi2_mean_reversion`, `bb_squeeze_percentile` und `bb_lookback` bei beiden Volatility-Breakout-Bots; Ausgabe mit heutigen Voreinstellungen bytegleich

**Sitzungstitel:** `TB-122` · **Aufwand:** hoch (ARBEITSWEISE 22.1) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 27.09.2026, 20:30, vom steuernden Chat
**Grundlagen (in Schritt 0 lesen):**
- Register **11.3** und Abschnitt 2 (Raster), Abschnitt 3 (Stufen der drei Achsen);
- `PLAN_VOR_DEM_TAG.md`, TB-30b Posten 3;
- `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md`, Abschnitt 4 (C4) und 5 (E-1);
- `docs/belege/TB-120/c_bestand.md`, `d_plan.md`, Zeile E-1.

**Vorgänger:** TB-121.
**Fable-Stand (nachgetragen 29.09.2026 vom steuernden Chat; hier stand „Kein Fable bis Dienstag, 29.09.“):** 27c und 29b liegen vor, im Repo unter `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md` und `docs/projektfuehrung/FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md` (in Schritt 0 lesen, nur die genannten Stellen). Für diesen Auftrag gelten daraus: **R44** (F-13: erst E-1, dann E-6, dann E-3/E-4) · **R43** (F-12: der Lauf rechnet jede Zelle über `collect_all_trades`; `evaluate_combination_multi` der Optimierer bleibt ausserhalb des Laufs — siehe B3) · **R47** (F-17: nach Posten 3 ist `SMA_TREND_PERIOD` Rasterachse — siehe D) · **R49 (h)** (11.3 ist E-1) · **27c R31 (b)** (eine Freigabe je Sperrlistendatei nennt deren Tests mit — siehe Freigabe-Nachtrag). Fragen an Fable gehen ins Ergebnis unter „Für Fable“; der steuernde Chat prüft sie nach dem Fable-Filter vor (`UEBERGABE.md`, Nachtrag 29.09.2026, 13:20).

## ⭐⭐ Freigabe des Betreibers, wörtlich

**27.09.2026, ca. 20:20, Auswahlkarte im steuernden Chat.** Frage: *„Nach TB-121 (kalter Leser): Welcher Code-Auftrag darf ohne Fable als Nächstes laufen? TB-120 nennt drei, die keine offene Fable-Frage berühren. Alle ändern Code und brauchen deshalb Ihre Freigabe.“* Gewählte Option:

> *„E-1: TB-30b Posten 3 (Empfohlen) — Drei Rasterachsen durchreichen (rsi2 SMA-Filter, zwei Breakout-Parameter), 7 Dateien. Nachweis: bytegleiche Ausgabe mit den heutigen Voreinstellungen. Sperrliste Punkt 11 bewegt sich planmässig nach 37.3.“*

**Nachtrag zur Freigabe, 29.09.2026, ca. 14:52, Auswahlkarte im steuernden Chat (27c R31 (b): eine Freigabe je Sperrlistendatei nennt deren Tests mit).** Frage: *„TB-122 soll je Bot eine neue Testdatei `test_posten3_durchreichung.py` anlegen (Nachweis, dass ein anderer Rasterwert wirklich ankommt). Fable verlangt, dass Tests in der Freigabe ausdrücklich stehen. Freigabe erweitern?“* Gewählte Option:

> *„Ja, bis 3 Testdateien (Empfohlen)“* — Freigabe um bis zu drei neue Dateien `strategies/<bot>/test_posten3_durchreichung.py` erweitert.

⛔ **Nicht freigegeben:**
- Register und Regelwerk. Die Tatsachennotiz zum Hash-Übergang wird nur als **Entwurf** ins Ergebnis geschrieben und kommt mit dem Registerauftrag E-2 ins Register;
- ein neues Sperrlisten-Abbild (37.3: „nach Bündeln“);
- Posten 4 und 5, `shared/zuteilung.py`, `herkunft.py`, `paths.py`;
- jede Datei ausser den sieben unten;
- Läufe auf dem Snapshot im Modus;
- Schreiben unter `research/**/ergebnisse/` oder `research/**/daten/`;
- `crontab`, Datenbanken.

**Sichtschutz 27.1:** Die Vergleichsläufe erzeugen Backtest-Ausgaben. Die Sitzung **liest keine Kennzahl daraus**, sie vergleicht nur Bytes (`cmp`, sha256). Die Ausgaben liegen **ausserhalb des Repos** in einem Wegwerf-Ordner (`$TMPDIR/tb122_*`); ins Repo kommen nur Hashes. Das Ergebnis enthält keine Ergebnisgrösse und geht in die Ablage.

In einfacher Sprache: Drei Einstellungen, die das Regelwerk im grossen Lauf durchprobieren will, kommen heute nicht bis zu den Bots durch. Beim einen Bot ist der Wert fest eingebaut, bei zwei anderen bleibt er unterwegs stecken. Diese Sitzung reicht sie durch. Mit den heutigen Werten muss danach jede Ausgabe Byte für Byte gleich sein wie vorher. Zusätzlich wird gezeigt, dass ein anderer Wert wirklich ankommt.

## Die sieben Dateien (aus TB-120 E-1; in Schritt 0 nachmessen)

| Bot | Dateien | heute (TB-120 C) |
|---|---|---|
| `rsi2_mean_reversion` | `backtest_rsi2.py`, `multi_symbol_optimise.py`, `equity_simulation.py` | `SMA_TREND_PERIOD = 200` ist eine Konstante; `compute_indicators(price_df)` wird ohne Argument aufgerufen |
| `volatility_breakout` | `multi_symbol_optimise.py`, `equity_simulation.py` | `load_all_symbol_data` ruft `compute_indicators(df)` beim Laden ohne Squeeze-Argumente auf |
| `volatility_breakout_crypto` | `multi_symbol_optimise.py`, `equity_simulation.py` | `get_trades_for_symbol` ruft `compute_indicators` ohne Squeeze-Argumente auf |

**Vorbild:** `rsi2_crypto` reicht `sma_trend_filter` schon durch (`docs/belege/TB-120/c_bestand.md`, Tabelle C4, Zeile `rsi2_crypto`: „Achse wird schon durchgereicht“; im Code, gemessen 29.09.2026: `rsi2_crypto/equity_simulation.py::collect_all_trades(…, sma_trend_period, …)` und `rsi2_crypto/multi_symbol_optimise.py::get_trades_for_symbol` ⇒ `compute_indicators(price_df, sma_trend_period)`). Die Sitzung liest dort, **wie** das gebaut ist, und baut die drei gleich, soweit die Bots es zulassen. Weicht die Bauart ab, steht der Grund im Ergebnis.

Muss eine achte Datei geändert werden (z. B. `backtest_*.py` der Breakout-Bots oder ein `live_params.py`) ⇒ nicht ändern, sondern melden. Das ist ein Abbruchkriterium, siehe unten.

## Schritt 0 — Sicherung und Ausgang

0a. `git status --short` — genau die erwarteten Dateien. Der steuernde Chat trägt die Liste beim Ablegen dieses Auftrags hier ein:
- ` M docs/auftraege/AKTUELLER_AUFTRAG.md`
- ` M docs/auftraege/MAC_TB-122_posten3_achsen_durchreichen.md`
- ` M docs/projektfuehrung/UEBERGABE.md`
- `?? docs/projektfuehrung/FABLE_ANFRAGE_2026-09-29b_tagesanfrage_sammlung_erzeuger_kalter_leser.md`
- `?? docs/projektfuehrung/FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md`
- `?? docs/projektfuehrung/FABLE_ANTWORT_2026-09-29a_betreiberentscheid_umzugstakt_ampel_agenten.md`
- `?? docs/projektfuehrung/FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md`
- `?? docs/projektfuehrung/FABLE_UEBERGABE_2026-09-29_neuer_chat.md`

*Gemessen vom steuernden Chat am 29.09.2026, ca. 14:52 (`ls-files --others`, `diff --name-only HEAD`). Die Reihenfolge der Zeilen ist ohne Bedeutung. `UEBERGABE.md`: nur angehängt, `numstat` gegen HEAD mit 0 entfernten Zeilen.*

Weicht etwas ab ⇒ Abbruch. Danach der Commit `TB-122 Schritt 0`, dann pushen.

0b. In `docs/belege/TB-122/0b_ausgang.txt` festhalten:
- HEAD;
- sha256 der sieben Dateien;
- `herkunft.register()` (Soll heute `01f5997a…`, Fundstelle `docs/ERGEBNIS_TB-117_wachen_vor_dem_tag.md`, Zeile F — messen, nicht annehmen);
- die Sonde gegen das gültige Abbild `sperrliste_abbild_2026-09-26_tb117.json`, nur lesend, wie in TB-119 A2 (vor und nach dem Lauf `git status --porcelain` zählen);
- welche der sieben Dateien in Abbild und Sperrliste stehen (Punkt 11) und welche in `herkunft.py::EINGEFROREN`, gemessen.

0c. db-Sicherung nach 7c Schritt 0.

0d. **Fundstellen:**
- Registertext 11.3 und die Zeilen der drei Achsen in Abschnitt 3 (Stufen) zeichengleich in `0d_register.txt`;
- dazu der heutige Wert je Achse aus dem Code (Datei:Zeile) und aus `live_params.py`.

Stimmt der Wert im Code nicht mit `live_params.py` überein ⇒ Befund, nicht angleichen, melden. Das ist kein Abbruch.

## Schritt A — Vorher-Läufe (Bauart TB-90 B6)

A1. Den Vergleichslauf von TB-90 B6 lesen: Werkzeug und Aufruf aus `docs/belege/TB-90/` und `ERGEBNIS_TB-90`, Block B6. Für die **drei betroffenen Bots** dieselbe Bauart ansetzen:
- je Bot ein Backtest-Lauf mit heutigen Parametern, **ohne** Modus, Ausgabe nach `$TMPDIR/tb122_vorher/<bot>/`;
- Lässt sich die B6-Bauart für einen der drei nicht anwenden ⇒ die Stelle, an der der Backtest seine Ausgabe schreibt, lesen und einen gleichwertigen Aufruf mit Zielordner ausserhalb des Repos wählen. Den Grund notieren.

A2. Zusätzlich je Bot ein **Optimierer-Kurzlauf** ohne Modus, auf die heutige Kombination begrenzt, falls der Optimierer das ohne Codeänderung zulässt. Die Ausgabe geht nach `$TMPDIR`. Lässt er es nicht zu ⇒ weglassen und benennen.

A3. sha256 jeder Ausgabedatei nach `a_vorher_hashes.txt`. **Inhalte nicht lesen.**

## Schritt B — Umbau

B1. Je Bot die Achse als Parameter von der Quelle, die die Achsen des Rasters liefert, bis zur Indikatorberechnung durchreichen. Voreinstellung ist genau der heutige Wert (0d). Die Rasterstufen aus Abschnitt 3 werden **nicht** in den Code geschrieben; die liefert `registerdaten.py`.

B2. `rsi2_mean_reversion`: `SMA_TREND_PERIOD` bleibt als Name der Voreinstellung stehen, wenn andere Stellen ihn lesen. Diese Leser vorher per `grep` messen und im Ergebnis nennen.

B3. Keine andere Änderung, kein Aufräumen, keine Umbenennung.

B4. ⭐ **Nach R43 (Fable 29b):** Der Lauf rechnet über den Signalpfad `equity_simulation.py::collect_all_trades`. Der importiert heute `load_all_symbol_data` und `get_trades_for_symbol` aus `multi_symbol_optimise.py` (gemessen 29.09.2026, je Bot die `from multi_symbol_optimise import …`-Zeile in `equity_simulation.py`; in Schritt 0 nachmessen). In `multi_symbol_optimise.py` werden **nur diese Funktionen** geändert, dazu ihre Aufrufe von `compute_indicators`. `evaluate_combination_multi` und das Optimierer-Raster bleiben unverändert (Punkt 11: Optimierer nicht ohne Not öffnen). Müsste dort doch etwas geändert werden, damit C1 oder C2 gelingt ⇒ melden, nicht ändern.

Commit `TB-122 B Achsen durchgereicht (Posten 3)`.

## Schritt C — Nachweis (bytegleich und Wertprobe)

*Berichtigt 29.09.2026 vom steuernden Chat: Hier stand „(zwei Teile, 24c)“. Der Zwei-Teile-Nachweis aus 24c (Register 41.2 B4) verlangt als Teil (b) einen Modus-Lauf; TB-122 läuft ohne Modus, Läufe im Modus sind nicht freigegeben. C2 ist eine Wertprobe, kein Nachweisteil (b).*

C1. **Nichts ändert sich mit Voreinstellungen:**
- A1 und A2 wiederholen, Ausgabe nach `$TMPDIR/tb122_nachher/`;
- `cmp` je Datei ⇒ **bytegleich 3/3** (und A2, falls gelaufen);
- nach `c1_vergleich.txt`.

Eine Abweichung ⇒ Abbruch, zurücksetzen (`git revert` des B-Commits) und melden.

C2. **Ein anderer Wert kommt an:**
- je Bot eine Probe, die mit einem Rasterwert ≠ Voreinstellung (erste Stufe aus Abschnitt 3) aufruft;
- zeigen, dass die Indikatorberechnung genau diesen Wert erhält. Das geschieht per Spion oder Monkeypatch im Test, **nicht** über eine Kennzahl;
- zusätzlich die Gegenprobe (40.7): Mit dem Code **vor** B schlägt dieselbe Probe fehl.

Das kommt als Testdatei `strategies/<bot>/test_posten3_durchreichung.py` oder, wenn es für Tests eine gemeinsame Stelle gibt, dort hinein. Eine Testdatei gilt nicht als achte Datei im Sinne des Abbruchkriteriums; sie wird im Ergebnis genannt.

C3. **Die bestehenden Tests:**
- vorher und nachher dieselbe Testmenge wie TB-117 Schritt F (siehe `docs/belege/TB-117/`), mindestens `research/vorregistrierung/test_vorregistrierung.py`;
- Ergebnis gleich, rc gleich.

C4. **Ohne Modus zeichengleich:** der Trockenlauf aus 44-8 bzw. TB-117 (Bauart dort nachlesen), soweit er ohne Snapshot-Lauf geht. Sonst benennen.

C5. **Sonde nachher:**
- erwartet sind Befunde **nur** an Punkt 11 (bzw. an den Punkten, die die sieben Dateien nennen), mit dem Übergang alter Hash ⇒ neuer Hash;
- jeder andere Befund ⇒ melden;
- `herkunft.register()` nachher.

Commit `TB-122 C Nachweis`.

## Schritt D — Ergebnis

`docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md` enthält:
- die Schritte mit Nachweisen;
- einen **Entwurf der Tatsachennotiz** für den Registerauftrag E-2 (37.3: Auftrag, Freigabe, alter und neuer Hash je Datei mit Commit — Form wie die Tabelle in 46.11: Datei, vorher, nachher, Commit, vollzieht —, `register()` alt und neu, Grund 11.3; dazu die Folge aus R47: `SMA_TREND_PERIOD` ist nach Posten 3 Rasterachse; der Wortlaut ist als Entwurf gekennzeichnet);
- „Für Fable“;
- „Nicht getan“;
- „In einfacher Sprache“.

Dazu ein Journal-Eintrag, der Abgabe-Commit und das Pushen. Den `$TMPDIR`-Ordner am Ende nicht löschen, wenn das nicht erlaubt ist; seinen Pfad nennen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab.
- C1 ist nicht bytegleich.
- Eine Datei ausserhalb der sieben (ausser der Testdatei) müsste geändert werden.
- Die Sonde zeigt nach B einen Befund an einem Punkt, den die sieben Dateien nicht berühren.
