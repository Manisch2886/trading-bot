# TB-122 TB-30b Posten 3 (E-1): drei Rasterachsen durchreichen — `sma_trend_filter` bei `rsi2_mean_reversion`, `bb_squeeze_percentile` und `bb_lookback` bei beiden Volatility-Breakout-Bots; Ausgabe mit heutigen Voreinstellungen bytegleich

**Sitzungstitel:** `TB-122` · **Aufwand:** hoch (ARBEITSWEISE 22.1) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 27.09.2026, 20:30, vom steuernden Chat
**Grundlagen (in Schritt 0 lesen):**
- Register **11.3** und Abschnitt 2 (Raster), Abschnitt 3 (Stufen der drei Achsen);
- `PLAN_VOR_DEM_TAG.md`, TB-30b Posten 3;
- `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md`, Abschnitt 4 (C4) und 5 (E-1);
- `docs/belege/TB-120/c_bestand.md`, `d_plan.md`, Zeile E-1.

**Vorgänger:** TB-121.
**Kein Fable bis Dienstag, 29.09.** Fragen gehen ins Ergebnis unter „Für Fable“; der steuernde Chat überträgt sie in die Sammlung.

## ⭐⭐ Freigabe des Betreibers, wörtlich

**27.09.2026, ca. 20:20, Auswahlkarte im steuernden Chat.** Frage: *„Nach TB-121 (kalter Leser): Welcher Code-Auftrag darf ohne Fable als Nächstes laufen? TB-120 nennt drei, die keine offene Fable-Frage berühren. Alle ändern Code und brauchen deshalb Ihre Freigabe.“* Gewählte Option:

> *„E-1: TB-30b Posten 3 (Empfohlen) — Drei Rasterachsen durchreichen (rsi2 SMA-Filter, zwei Breakout-Parameter), 7 Dateien. Nachweis: bytegleiche Ausgabe mit den heutigen Voreinstellungen. Sperrliste Punkt 11 bewegt sich planmässig nach 37.3.“*

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

**Vorbild:** `rsi2_crypto` reicht `sma_trend_filter` schon durch (TB-120 C4). Die Sitzung liest dort, **wie** das gebaut ist, und baut die drei gleich, soweit die Bots es zulassen. Weicht die Bauart ab, steht der Grund im Ergebnis.

Muss eine achte Datei geändert werden (z. B. `backtest_*.py` der Breakout-Bots oder ein `live_params.py`) ⇒ nicht ändern, sondern melden. Das ist ein Abbruchkriterium, siehe unten.

## Schritt 0 — Sicherung und Ausgang

0a. `git status --short` — genau die erwarteten Dateien. Der steuernde Chat trägt die Liste beim Ablegen dieses Auftrags hier ein:
- `<<ERWARTET_0A>>`

Weicht etwas ab ⇒ Abbruch. Danach der Commit `TB-122 Schritt 0`, dann pushen.

0b. In `docs/belege/TB-122/0b_ausgang.txt` festhalten:
- HEAD;
- sha256 der sieben Dateien;
- `herkunft.register()` (Soll heute `01f5997a…` — messen, nicht annehmen);
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

Commit `TB-122 B Achsen durchgereicht (Posten 3)`.

## Schritt C — Nachweis (zwei Teile, 24c)

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
- einen **Entwurf der Tatsachennotiz** für den Registerauftrag E-2 (37.3: alter und neuer Hash je Datei, `register()` alt und neu, Grund 11.3; der Wortlaut ist als Entwurf gekennzeichnet);
- „Für Fable“;
- „Nicht getan“;
- „In einfacher Sprache“.

Dazu ein Journal-Eintrag, der Abgabe-Commit und das Pushen. Den `$TMPDIR`-Ordner am Ende nicht löschen, wenn das nicht erlaubt ist; seinen Pfad nennen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab.
- C1 ist nicht bytegleich.
- Eine Datei ausserhalb der sieben (ausser der Testdatei) müsste geändert werden.
- Die Sonde zeigt nach B einen Befund an einem Punkt, den die sieben Dateien nicht berühren.
