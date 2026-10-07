# TB-140 Verfahrensmessung 2: Voraussetzungen aus R78 und R79, nur lesend — Umgebung gegen den ganzen Lock (R79 (a)), `schedule` je Aktien-Bot gegen den Ausschnitt (R79 (b)), Bestand vom 02.10.2026 an `APH` (R79 (g)), dazu zwei Belege: `close` je Tagesreihe des Snapshots (Z1, zu R79 (c)) und die Herkunft von 5.4.0 nach `ERGEBNIS_TB-47` (Z2, zu R79 (f)); danach Lesen des Codes zu R78 (a), (d) und (e)

**Sitzungstitel:** `TB-140` · **Modell:** Opus 5.5 (Standard) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 07.10.2026 vom steuernden Chat
**Vorgänger:** TB-138 (`8d172c0`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3`, immer mit `-B`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.

**Folgeauftrag gleicher Bauart.** Vorbild und Vorgänger ist `docs/auftraege/MAC_TB-138_verfahrensmessung_snapshot.md` (Ergebnis `docs/ERGEBNIS_TB-138_verfahrensmessung_snapshot.md`, Belege `docs/belege/TB-138/`). Lies ihn zuerst ganz. Er gilt in allem, was hier nicht anders steht — mit `TB-140` für `TB-138` in Pfaden, Dateinamen und Commit-Texten: die Form von Schritt 0 (0a, 0b), der Aufruf je Messung mit angehängtem `rc`, die Rückgaben 0 / 1 / 2 (unten unter „Rückgaben und Urteile“ für diesen Auftrag ausgeschrieben), die Form der Abgabe (D0 bis D3), die Regel für den Abbruch nach Schritt 0 und der Satz „Nie `JOURNAL.md` mit Platzhalter“. Dieser Auftrag nennt nur die Unterschiede und die Sollwerte. Die Lesarten L1 bis L9 des Vorgängers gelten weiter; der Verfahrensprüfer hat sie bestätigt (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-06a_verfahrensmessung_snapshot_aph.md`, Tabelle zu Frage 2 (a)), L2 mit einem anderen Begriff (unten, N1).

**Reihenfolge, und warum:** Teil 1 (V4, V5, V6 und die zwei Zusatzmessungen Z1 und Z2) ist kurz und wird zuerst gemessen, sofort committet und gepusht; die Sitzung gibt dazu eine Zeile aus und fährt ohne Halt mit Teil 2 fort. Auf ihn wartet der Registereintrag der Blöcke R78 bis R80 (TB-139; Nummer und Umfang nach dem Nachtrag, den der Abschnitt „Freigabe“ nennt): Die drei Klammern verlangen die Messung „vor dem Eintrag“ (V4, V5) oder entscheiden über einen Satz des Eintrags (V6); Z1 und Z2 liefern den Beleg zu zwei Sätzen aus R79 (c) und R79 (f), die der Eintrag als Tatsache führt. Teil 2 (V1, V2, V3) ist Lesen des Codes und darf dauern.

**Gemessen wird nur das Ob**, nie ein Ergebnis eines Laufs (Register 27.2). Bei jeder Abweichung: melden, nichts reparieren.

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei** (Betreiberentscheid 26.09.2026, so zitiert im Vorgänger, dort Z. 10; so auch TB-127, TB-128, TB-131, TB-133 und TB-138). Betreiber am 07.10.2026, 08:10: „Arbeite heute so viel wie möglich selbstständig ab, damit wir endlich wieder größere Fortschritte machen.“ Dass TB-140 die Voraussetzungen aus R78 und R79 misst und vor dem Registerauftrag TB-139 läuft, Teil 1 vor Teil 2, ist Vorgabe des steuernden Chats vom 07.10.2026 (`UEBERGABE.md`, Nachtrag 07.10.2026, 10:32); der Betreiber startet den Auftrag durch Absenden des Satzes.

**An der Sperrliste gemessen** (Helfer des steuernden Chats, 07.10.2026, am HEAD `8d172c0`): Im gültigen Abbild `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json` (sha256 beginnt `46f0ad5d1d83a253`) liegt keiner der 22 Pfade der Liste `eingefroren` und keiner der 11 Pfade in `hashes` der 14 Punkte unter `docs/belege/`, `docs/projektfuehrung/` oder auf `docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md`; die Liste `bestimmt` ist leer. Dieser Auftrag schreibt nur unter `docs/`. Von den Dateien, die dieser Auftrag **liest**, stehen in `eingefroren`: für Teil 1 `snapshots/63e4b6c8…/MANIFEST.json` (V6) und die zwei Universumsdateien `snapshots/63e4b6c8…/config/sp500_top150.txt` und `…/config/top25_symbols.txt` (Z1; alle drei liest auch 0b), für Teil 2 `research/vorregistrierung/benchmark.py`, `auswertung.py`, `registerdaten.py` und `faltenplan.py`; in `hashes` steht ausserdem `shared/zuteilung.py`. Die Namenssuche in V1 geht über alle verfolgten `*.py` ausserhalb von `docs/` und berührt damit lesend auch die übrigen eingefrorenen Python-Dateien (`kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`) und `herkunft.py` aus `hashes`. Gelesen wird nur; dass sich dabei nichts ändert, zeigen D0 (`--pruefen` am Snapshot) und D3 (`numstat`: nur Pfade unter `docs/`).

Geschrieben wird nur: `docs/belege/TB-140/` (Messskripte, Rohausgaben, Tabellen), `docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md`, ein Block in `docs/projektfuehrung/BACKLOG.md` (Schritt N, E1) und ein Block in `docs/projektfuehrung/JOURNAL.md` (D2, darin J1 aus Schritt N). Kopien und kleine Ordner für die Gegenproben entstehen in `$TMPDIR` (Vorgänger Z. 27) und werden nicht committet.

Gelesen werden: Register, `requirements.lock`, `trading-env/pyvenv.cfg`, die installierten Paket-Metadaten (über `importlib.metadata`), der Kalender des Pakets, von den Kursdaten **nur** `data/APH_1d.csv` (V6) und im Snapshot `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/` die Tagesreihen `*_1d.csv` samt `MANIFEST.json` und den zwei Universumsdateien unter `config/` (ausgewertet wird nur `open_time`, ob `close` fehlt, und in V6, welche Spalten der Zeile 2026-09-01 leer sind), für Z2 `docs/ERGEBNIS_TB-47_snapshotgrenze.md` und aus `research/snapshotgrenze/ergebnisse/eingaben.json` nur das Feld `kalender`, und in Teil 2 Python-Quelltext unter `research/vorregistrierung/`, `research/mtm_drawdown/`, `research/exposure_messung/`, `shared/` und `strategies/`; für die Namenssuche in V1 (Nr. 0: gibt es einen Zellen-Erzeuger; Nr. 1 und Nr. 2: wer ruft `tagesschluss` und `lade_schlusskurse`) alle von git verfolgten `*.py` ausserhalb von `docs/`, davon nur die Trefferzeilen. 0b und D0 lesen über `shared/snapshot.py --pruefen` und die Dateiliste alle 226 Dateien des Snapshots, nur für Hashes (Vorgänger Z. 121 und Z. 122).

⛔ **Nicht erlaubt, mit Grund.** Es gelten die sieben Verbote des Vorgängers (dort Z. 21 bis Z. 27) mit ihren Gründen. Dazu und anders:

- **Kein Lauf.** Kein Zellen-Erzeuger (ein Helfer fand keinen; V1 Nr. 0 misst es nach), kein Selektionslauf, kein `auswertung.py`, kein `benchmark.py`, kein `beispieldaten.py`, kein `faltenplan.faltenplan()`, kein `erste_falte()`, kein Backtest, kein Optimierer, kein Test, kein Bot; auch nicht „nur zur Probe“ auf anderen Daten. *Grund:* R78 (d) verlangt die Messung „durch Lesen des Codes und ohne Lauf auf dem registrierten Snapshot (27.2, nur das Ob)“; `benchmark.py::main` schreibt Tabellen (`schreibe_tabellen`, Z. 363), und was die übrigen Einstiegspunkte schreiben, ist nicht gemessen. Aus dem Repo ausgeführt wird nur, was der Vorgänger in 0b ausführt (`shared/snapshot.py --pruefen`, ohne `--json`).
- **Code wird gelesen, nie geändert.** Das gilt für jede Datei unter `research/`, `shared/`, `strategies/`, `notifications/`, `docs/werkzeuge/` und besonders für `benchmark.py`. *Grund:* R78 (d): „benchmark.py wird dafür nicht geöffnet (R72 (d))“; die Datei steht in der Sperrliste. Lesen ist erlaubt und ist die Messung (N7). Kein Import eines Moduls des Repos in ein Messskript. *Grund:* Ein Import führt Modulcode aus (Startprüfungen, Pfadauflösung); was dabei geschrieben wird, ist nicht gemessen.
- **Register, Abbild und alle Sperrlisten-Dateien bleiben unberührt.** R78 bis R80 werden nicht eingetragen, keine Marke gesetzt, keine Statusliste (53.10, 54.6) angefasst. *Grund:* Der Eintrag ist TB-139 und braucht eine Einzelfreigabe; dieser Auftrag liefert ihm nur Tatsachen.
- **Kein zweiter Snapshot, nichts an den Daten.** `snapshots/` und `data/` werden nur gelesen; die Zeile `APH` 2026-09-01 wird nicht ergänzt, keine Kursdatei neu geladen. *Grund:* Register 18, Punkt 4 („Ein zweiter Snapshot ist ein neuer Lauf“), 17.2 und R78 (d) („Der Snapshot bleibt (17.2) … die Zeile wird nicht ergänzt“).
- **Keine Kurse, Renditen, Kennzahlen oder Trade-Zahlen** in einer Ausgabe oder einem Beleg; aus Kursdateien nur Datum, Spaltennamen, Zählungen, Hashes. In Teil 2 nichts aus Ordnern `ergebnisse/` lesen (Ausnahme: das Abbild in 0b; in Teil 1 liest Z2 aus `research/snapshotgrenze/ergebnisse/eingaben.json` nur das Feld `kalender`), keine `*.db`, keine Trade-Liste. *Grund:* Sichtschutz, Register 27.1.
- **`pip`, ein Paketwechsel, ein Systemupdate, ein neues venv:** nicht, auch nicht bei einer Abweichung in V4. *Grund:* Gemessen wird die Umgebung, wie sie ist; Register 20, Punkt 2: „Nichts wird installiert, nachgezogen oder repariert.“
- **Kein Urteil über das Verfahren.** Ob ein Befund eine registrierte Regel verletzt, ob R78 (d) neu zu entscheiden ist, ob eine Prüfung „genügt“ (R78 (e)): Das entscheidet der Verfahrensprüfer. *Grund:* R78 (f). Das Ergebnis sagt je Teilfrage nur eines der Urteile, die die Tabelle „Urteile je Teilfrage“ (unten) für sie zulässt — und woran es hängt.

Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt; das ist kein Ändern im Sinn der Verbote. Für die acht Punkte aus 7c gilt der Vorgänger (Z. 29) unverändert.

## Die sechs Voraussetzungen, zeichengleich

*Vom Bauskript aus `docs/projektfuehrung/FABLE_ANTWORT_2026-10-06a_verfahrensmessung_snapshot_aph.md` geschnitten (159 Zeilen, 26 689 B; Codezaun ab Z. 150; R78 ist Z. 151, R79 Z. 154, R80 Z. 157). Die Blöcke stehen noch nicht im Register. Die Sitzung liest sie in der Datei nach; der Wortlaut dort gilt.*

Je Voraussetzung ein Codezaun (damit `<SYMBOL>` und ähnliche Zeichen stehen bleiben): erste Zeile der Satz, an dem die Klammer hängt, letzte Zeile die Klammer. Bei V2 ist die erste Zeile der Massstab aus R78 (c); bei V3 stehen in der Quelle zwischen Satz und Klammer zwei weitere Sätze, sie sind als mittlere Zeile mitgeschnitten.

**V1 — R78 (a):**

```
Ein Symbol trägt an einem Tag einen Kurs (R66 (b), R72), wenn seine Tagesreihe im Snapshot (<SYMBOL>_1d.csv) an dem Tag eine Zeile führt, in der close nicht fehlt. Eine Zeile ohne close ist ein Tag ohne Kurs.
[Voraussetzung, zu messen: dass benchmark.py::tagesschluss und der Kern, den der Zellen-Erzeuger für die MtM-Reihe übernimmt, für alle neun Bots die Spalte close dieser Reihe lesen; liest eine Stelle eine andere Spalte oder eine andere Reihe, wird gemeldet.]
```

**V2 — R78 (d); die erste Zeile ist der Massstab aus R78 (c):**

```
Endet sie erst danach, berührt ihr Ende 3b (c) im Lauf nicht, solange kein Wert einer Ausgabe des Laufs (R39) aus einer Zeile mit Datum ab dem Go-Live-Schnitt gebildet wird.
[Voraussetzung, vor dem signierten Tag zu messen, durch Lesen des Codes und ohne Lauf auf dem registrierten Snapshot (27.2, nur das Ob): ob die Lader der vier Aktien-Bots und benchmark.py eine Zeile ohne close behalten oder verwerfen; ob bei einem der neun Bots ein Wert einer Ausgabe des Laufs aus einer Zeile mit Datum ab dem Go-Live-Schnitt gebildet wird (Einstieg, Ausstieg, Bewertung, Indikatorwert). Wird ein solcher Wert gebildet, wird gemeldet, die Frage kommt vor dem Tag an den Verfahrensprüfer, und (d) wird neu entschieden.]
```

**V3 — R78 (e); die mittlere Zeile steht in der Quelle zwischen Satz und Klammer:**

```
Jeder Zahlenwert in zellen.csv und zellenbericht.csv ist endlich; „nicht definiert“ (R34) ist kein Zahlenwert.
Ein Verstoss ist ein Befund über den Erzeuger, kein Ausgang (Bauart R33, R67): Der Zellen-Erzeuger prüft das im Lauf, nachdem er die Dateien geschrieben hat, und endet sonst mit 2; die Abnahme prüft die Wache mit Gegenprobe.
[Voraussetzung, zu messen: dass kein Feld der zwei Dateien nach seiner registrierten Definition einen nicht endlichen Wert tragen darf; ob auswertung.py einen nicht endlichen Wert in zellen.csv schon mit 2 beendet. Trifft das Erste nicht zu, wird gemeldet; trifft das Zweite zu, genügt diese Prüfung, und der Erzeuger baut keine zweite.]
```

**V4 — R79 (a):**

```
Lock-Umgebung im Sinn von R74 (e) ist eine Umgebung, deren Angaben nach 17.5 (Python-Fassung, alle Pakete des Locks, Plattform) den registrierten gleich sind; kein Ordner ist es dem Namen nach.
[Voraussetzung, vor dem Eintrag zu messen: dass trading-env in allen Paketen des Locks und in der Plattform der registrierten Umgebung gleich ist; die Messung nennt vier Pakete und den Interpreter. Weicht etwas ab, wird gemeldet.]
```

**V5 — R79 (b):**

```
Die Sitzungstage je Bot sind ein Ausschnitt der einmal gerechneten Menge.
[Voraussetzung, vor dem Eintrag zu messen: dass ein Aufruf von schedule für den Zeitraum je Bot dieselben Tage liefert wie der Ausschnitt; sonst wird gemeldet.]
```

**V6 — R79 (g); nur die Klammer:**

```
[Voraussetzung, zu messen: dass der Bestand vom 02.10.2026 die Zeile APH 2026-09-01 ohne close führte; sonst traf der Satz, und es wird nicht gezählt.]
```

**Z1 und Z2 — zwei Sätze aus R79 ohne Klammer, zu denen der steuernde Chat einen Beleg verlangt** (Z. 154 der Antwort; der erste aus (c), der zweite aus (f) bis vor den Strichpunkt):

```
In den Aktien-Tagesreihen fehlt close in genau dieser Zeile, in den 24 Krypto-Tagesreihen in keiner.
Der Wert 5.4.0 im Feld kalender von eingaben.json stammt nach docs/ERGEBNIS_TB-47_snapshotgrenze.md aus der Cloud-Sitzung vom 18.09.2026
```

**Register 17.5, Registertext 5f (Z. 2829 bis Z. 2833) und 20, Tabelle (Z. 3231 bis Z. 3234):**

```
> Der Selektionslauf findet auf einer **registrierten Umgebung** statt:
> **Python-Fassung** (Tatsachennotiz: 3.9.6), ein **`requirements.lock`** mit
> exakten Versionen aller Pakete, dessen Hash im Register steht, und die
> **Plattform**. Der Lauf beginnt mit einer Prüfung dieser drei Angaben und
> **bricht bei Abweichung ab (Rückgabewert 2)**.
> | SHA-256 der Datei | **`96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5`** |
> | Pakete | **67**, sämtlich mit `==` |
> | Interpreter | `3.9.6 (default, Apr 30 2025, 02:07:18) [Clang 17.0.0 (clang-1700.0.13.5)]` |
> | Plattform | `macOS-15.7.9-x86_64-i386-64bit` |
```

## Belegt · erschlossen · offen

**Belegt** (gemessen 07.10.2026 von einem Helfer des steuernden Chats über die Geräteanbindung am HEAD `8d172c0`; die Sitzung misst nach, ihre Zahl gilt):

- Register `docs/VORREGISTRIERUNG_neuselektion.md`: 11 581 Zeilen, sha256 `8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc` — unverändert seit dem Vorgänger.
- `requirements.lock`: 83 Zeilen, sha256 `96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5` (gleich Register Z. 3231); 67 Zeilen der Form `name==version` (Z. 17 bis Z. 83), keine andere Zeile ohne `#`. Kopf: Z. 6 `interpreter_venv  3.9.6`, Z. 7 `interpreter_voll  3.9.6 (default, Apr 30 2025, 02:07:18) [Clang 17.0.0 (clang-1700.0.13.5)]`, Z. 8 `plattform         macOS-15.7.9-x86_64-i386-64bit`, Z. 9 `maschine          x86_64`. `trading-env/pyvenv.cfg`: `version = 3.9.6`.
- Vergleichswerte zu V4 (W2), kein Soll: Der Kopf des Locks sagt in Z. 2 bis Z. 4: „Erzeugt 19.09.2026 aus `pip freeze --all`, gegengeprueft gegen die dist-info-Ordner unter trading-env/lib/python3.9/site-packages und gegen importlib.metadata - drei unabhaengige Wege, 0 Unterschiede (TB-58).“ Am 07.10.2026 von einem Helfer über die Anbindung gezählt (nur Ordnernamen gelesen, `trading-env` nicht gestartet): 67 Ordner `*.dist-info` unter `trading-env/lib/python3.9/site-packages`; Name und Fassung aus dem Ordnernamen sind bei allen 67 Lock-Zeilen gleich (Namen nach PEP 503 angeglichen), kein Ordner steht ohne Lock-Zeile da.
- Die Prüfung des Laufs steht in `shared/paths.py`: `_lies_lock` (Z. 499) und `_pruefe_lock` (Z. 529 bis Z. 571). Verglichen werden `interpreter_voll` mit `" ".join(sys.version.split())` (Z. 540, Z. 548), `plattform` mit `platform.platform()` (Z. 541, Z. 551) und je Paketzeile `metadata.version(name)` (Z. 556); `maschine` und `interpreter_venv` vergleicht der Lauf nicht.
- Der Vorgänger hat vier Pakete und den Interpreter verglichen (`docs/belege/TB-138/verfahrensmessung_snapshot.py`, `PAKETE` Z. 41 bis Z. 44, `kopf` Z. 104 bis Z. 129) und die Plattform nur gedruckt: `macOS-15.7.9-x86_64-i386-64bit` (`docs/belege/TB-138/m3.txt` Z. 4, 06.10.2026).
- Der Vorgänger hat `schedule` für M1 einmal aufgerufen, von 1962-01-02 bis 2026-09-01 (Skript Z. 284 bis Z. 286; `m1.txt` Z. 19 und Z. 20: 16 275 Tage), und je Bot den Ausschnitt genommen (Z. 328 und Z. 329: `Hp = {t for t in H if von <= t <= bis}`). Der Aufruf selbst: `kal.schedule(start_date=von.isoformat(), end_date=bis.isoformat())`, Tage `ts.date()` aus `plan.index` (Z. 230 und Z. 231). Sitzungstage je Bot laut `m1.txt` Z. 95, 100, 105 und 110: 2 428 (ab 2017-01-01) und 2 177 (ab 2018-01-01), je bis 2026-08-31 — Vergleichswerte, kein Soll.
- Zeitraum je Aktien-Bot: Register 33.2, Z. 6001 bis Z. 6004, Spalte „erste Falte“ (`elliott_wave_stocks` 2017, `rsi2_mean_reversion` 2018, `turtle_soup_stocks` 2017, `volatility_breakout` 2018); der 1. Januar aus 29.3 (Z. 5408); Ende aus 35.1 (Z. 6375, Z. 6385 bis Z. 6388: Go-Live-Schnitt `2026-09-01`, ausschliesslich).
- „Bestand vom 02.10.2026“: Register Z. 11482 („Gemessen am 02.10.2026 am Stand `0779453`, nur lesend, durch Helfer des steuernden Chats“), `docs/belege/TB-132/vormessung/v3_daten.md` Z. 5 („der heutige Live-Bestand `data/` und `config/` der Repo-Wurzel — NICHT der spätere Snapshot des Laufs“) und Z. 6 („150 Aktien-Dateien vom 2026-09-02“). `data/` und `snapshots/` sind von git verfolgt.
- Vergleichswerte zu V6, kein Soll: `git log -- data/APH_1d.csv` nennt einen Commit (`0f6491b`, 2026-09-02T23:12:10+02:00, „Initial commit“), `git log 0779453..HEAD -- data/APH_1d.csv` nennt keinen; der Stand `0779453` ist der Commit vom 2026-10-02T18:11:14+02:00 („TB-131 D3: porcelain nach der Abgabe“); der Blob von `data/APH_1d.csv` ist an `0779453` und an `HEAD` `847a599c4d065f662dc1b096bf1618c69c81c719`, derselbe wie der von `snapshots/63e4b6c8…/APH_1d.csv`; beide Arbeitsdateien 821 714 B, sha256 `8d5d53241fd60d4f53258e38422b07e39cc01a8a9133aaf8ed1bb8e8ef1edc71`, gleich `MANIFEST.json` (`dateien["APH_1d.csv"]`); Änderungszeit über die Anbindung gelesen 2026-09-02 04:21:29 UTC; Zeile 2026-09-01: sechs Spalten, leer `open`, `high`, `low`, `close`.
- Zu Z1: Das Ergebnis des Vorgängers führt den Krypto-Teil als nicht gemessen — `docs/ERGEBNIS_TB-138_verfahrensmessung_snapshot.md` Z. 154 („Krypto nicht gemessen (M1 liest nur Aktien)“) und Z. 162 („**Der Krypto-Teil von „Zeilen ohne `close`“** ist nicht gemessen“). Der Snapshot-Ordner führt 174 Dateien `*_1d.csv`, 25 `*_1h.csv`, 24 `*_4h.csv`, `MANIFEST.json` und `config/` mit `sp500_top150.txt` (150 Symbole) und `top25_symbols.txt` (25 Symbole; `XAUTUSDT` ohne `_1d`-Reihe). Vergleichswerte, kein Soll: (a) Zählung des steuernden Chats (awk, 07.10.2026, nicht im Repo belegt): 174 Dateien; `close` fehlt in genau einer Zeile (`APH_1d.csv`, 2026-09-01); 150 Dateien enden 2026-09-01, 24 enden 2026-09-14. (b) Probelauf der Skizze `z1_close_je_datei.py` durch einen Helfer in der Linux-VM der Geräteanbindung (Python 3.10.12, pandas 2.3.3, nicht `trading-env`), 07.10.2026: rc 0 · Aktien 150 Dateien, 1 417 557 Zeilen, eine Zeile ohne `close` (`APH_1d.csv`, 2026-09-01, Zelle leer) · Krypto 24 Dateien, 44 163 Zeilen, keine Zeile ohne `close` · letzte Zeile: 150-mal 2026-09-01, 24-mal 2026-09-14 · letzte Zeile mit `close`: Aktien 149-mal 2026-09-01 und einmal 2026-08-31, Krypto 24-mal 2026-09-14 · keine Datei ohne Zuordnung, kein Hinweis.
- Zu Z2: `docs/ERGEBNIS_TB-47_snapshotgrenze.md` gibt es unter diesem Namen (`ls`; 25 988 B, 526 Zeilen). Einstiegsstellen, Zeiger und nicht ausgewertet: `5.4.0` steht in Z. 122 und Z. 359; Z. 3 lautet „**Ergebnis der Cloud-Sitzung vom 18.09.2026.**“; `eingaben.json` nennen Z. 69 und Z. 469; `paket_vorhanden` nennt keine Zeile. Das Ergebnis des Vorgängers führt Z. 3, Z. 122, Z. 348 und Z. 359 als Fundstelle (dort Z. 121, Z. 143, Z. 153). Die Anfrage 06.10.a sagt in K1 (dort Z. 79): „dass sie das Feld `kalender` schrieb, ist erschlossen“. Das Feld selbst, über die Anbindung gelesen am 07.10.2026: `kalender` ist ein Objekt mit `im_repo`, `in_selektionshuelle` und `paket_vorhanden`, der Wert von `paket_vorhanden` ist `5.4.0`.
- **Ein Zellen-Erzeuger als Code ist nicht gefunden** (Stand der Suche eines Helfers; die Sitzung misst es in V1 Nr. 0 nach, ihre Suche gilt). `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md` Z. 81: „**C2 Zellen-Erzeuger.** Kein Ansatz.“; geplant als E-7 und E-8 (dort Z. 122 und Z. 123). Am HEAD `8d172c0` nennen von den verfolgten Python-Dateien ausserhalb von `docs/` nur `research/vorregistrierung/auswertung.py`, `beispieldaten.py`, `test_ersatzwerte.py` und `test_vorregistrierung.py` die Wörter `zellen.csv` oder `zellenbericht`. Probelauf der Skizze `suche.py` am 07.10.2026 (Linux-VM, 482 verfolgte `*.py` ausserhalb von `docs/`), Vergleichswerte und kein Soll: `zellen.csv` 11 Vorkommen in 11 Zeilen in diesen vier Dateien, `benchmark_tagesreihen` 11 Vorkommen in 11 Zeilen in denselben vier, `tagesreihen/` 2 Vorkommen in 2 Zeilen (beide in `auswertung.py`), `zellenbericht` 0, `symbole_je_falte` 0 — gezählt sind Vorkommen, nicht Zeilen: `suche.py` druckt je Vorkommen eine Zeile `TREFFER`, und die Zahl hinter `Treffer` in der Zeile `MUSTER` ist ihre Zahl. Zeiger, nicht ausgewertet: `beispieldaten.py` Z. 200 schreibt `zellen.csv`; sein Docstring beginnt in Z. 3 mit „TB-30a - Beispieldaten: Rohergebnisse mit frei erfundenen Werten“. Register Z. 11493: „Einziger vorhandener Kern für eine tägliche MtM-Reihe ist `research/mtm_drawdown/mtm_kern.py`“ und „Welchen Kern der Zellen-Erzeuger übernimmt, legt kein Registertext fest“.
- Einstiegsstellen für Teil 2 (Zeiger, nicht ausgewertet): `research/vorregistrierung/benchmark.py` Z. 148 `def tagesschluss(markt: str) -> dict:`, Lesestelle Z. 152 bis Z. 160 · `research/mtm_drawdown/mtm_kern.py` Z. 135 `tagesraster`, Z. 151 `kurse_auf_raster`, Z. 176 `mtm_pfad`; seine Kurse lädt `research/mtm_drawdown/grundlage.py` Z. 82 `lade_schlusskurse(symbole, zeitrahmen="1d")`, Aufruf in `messung.py` Z. 147 · die neun Lader `strategies/<bot>/multi_symbol_optimise.py::load_all_symbol_data` (Z. 53, 60, 59, 55, 50, 42, 49, 53, 44 in der Reihenfolge `elliott_wave`, `elliott_wave_stocks`, `rsi2_crypto`, `rsi2_mean_reversion`, `t3_supertrend`, `turtle_soup_crypto`, `turtle_soup_stocks`, `volatility_breakout`, `volatility_breakout_crypto`), jeder ruft `shared/kursdaten.py::entferne_unvollstaendige` (dort Z. 73; `unvollstaendige_maske` Z. 57) · Signalpfad und Zuteilung nach R43 (Register Z. 10894): `strategies/<bot>/equity_simulation.py::collect_all_trades` und `::simulate_portfolio`, `shared/zuteilung.py::simuliere_portfolio` (Z. 657) · `research/vorregistrierung/auswertung.py` Z. 137 `class Abbruch(SystemExit):`, Z. 320 `lies_zellen`, darin Z. 355 `if df["netto_sharpe"].isna().any():`. · Ordner (Zeiger für V1, nicht ausgewertet): `benchmark.py` Z. 120 `DATA_DIR = paths.DATA_DIR`; `shared/paths.py` Z. 679 `_MODUS = _modus_aus_umgebung()`, Z. 685 `DATA_DIR = _LIVE_DATA_DIR` (Z. 194: `os.path.join(BASE_DIR, "data")`), Z. 692 `DATA_DIR = _MODUS[0]`, die Namen der Umgebungsvariablen in Z. 205 bis Z. 208; `grundlage.py` Z. 35 `DATA_DIR = os.path.join(REPO_ROOT, "data")`; Register Z. 8932: „Ein Modus-Lauf ist ein Lauf unter dem Selektionsmodus des Resolvers (`shared/paths.py`, `TB_SELEKTIONSWURZEL`).“ · Aufrufer (Zeiger): `lade_schlusskurse` in `grundlage.py` Z. 211 und Z. 212, `messung.py` Z. 147, `richtungsfall.py` Z. 135 und `test_mtm_kern.py` Z. 121 (alle unter `research/mtm_drawdown/`); `tagesschluss` in `benchmark.py` Z. 253 und `test_vorregistrierung.py` Z. 1172.
- Die neun Bots: `research/vorregistrierung/registerdaten.py` Z. 130 bis Z. 140 (`BOTS`, mit `markt` und `zeitrahmen`); Register 33.2, Z. 5996 bis Z. 6004. Go-Live-Schnitt: Register 5.2, Z. 667 („**`2026-09-01`, ausschliesslich.**“); `registerdaten.py` Z. 102 `GO_LIVE_SCHNITT = "2026-09-01"`, gelesen in `research/vorregistrierung/faltenplan.py` Z. 285 und Z. 326.
- Felder: Die Ausgaben des Zellen-Erzeugers zählt R39 auf (Register Z. 10857: „Ausgaben des Zellen-Erzeugers; Feldliste als Registertext“); `zellen.csv` in Register 50.2, Z. 11065 bis Z. 11070 (Zitat aus dem Docstring von `auswertung.py`), dazu R33 (Z. 10797), R36 (Z. 10827), R68 (Z. 11431); `zellenbericht.csv` in R34 (Z. 10810), dort auch „nicht definiert“; 50.2, Z. 11097: für `zellenbericht.csv` „führt der Docstring heute keine Feldliste“. R67 (Z. 11424): „jeder Zahlenwert endlich“ für die Tagesreihen; „Für zellen.csv gilt R33.“

**Erschlossen — Lesarten des steuernden Chats, vorläufig.** Das Ergebnis sagt je Lesart, ob eine Aussage an ihr hängt.

- **N1** (V4) „alle Pakete des Locks“: die 67 Zeilen `name==version`. „Gleich“: `importlib.metadata.version(name)` liefert genau die Fassung der Zeile — der Weg des Laufs (`shared/paths.py` Z. 556). „Plattform der registrierten Umgebung“: die Kopfzeile `plattform` des Locks, gleich Register Z. 3234, gegen `platform.platform()`. `maschine` und ein Paket, das installiert ist und nicht im Lock steht, werden genannt und gehören nicht zum Urteil. „Lock-Umgebung“ ist nach R79 (a) kein Ordner: `trading-env` ist sie nur, wenn V4 erfüllt ist.
- **N2** (V5) „Der Ausschnitt“: die Tage der einmal gerechneten Menge (`schedule` von 1962-01-02 bis 2026-09-01) zwischen Beginn und Ende des Bots, beide eingeschlossen. „Ein Aufruf von schedule für den Zeitraum je Bot“: `mcal.get_calendar("NYSE").schedule(start_date=Beginn, end_date=Ende)`, Tage aus dem Index. Beginn und Ende nach L4 und L3 des Vorgängers. „Dieselben Tage“: die zwei Mengen sind gleich, und der Index des Aufrufs führt keinen Tag doppelt.
- **N3** (V6) „Der Bestand vom 02.10.2026“: `data/` der Repo-Wurzel, wie die Helfer ihn am 02.10.2026 am Stand `0779453` lasen. „Führte ohne close“: Es gibt genau eine Zeile mit `open_time` 2026-09-01, und `close` fehlt dort nach L5 des Vorgängers.
- **N4** (V1) „Der Kern, den der Zellen-Erzeuger für die MtM-Reihe übernimmt“: Findet V1 Nr. 0 keinen Erzeuger (so die Suche des Helfers), gilt: Weil kein Registertext den Kern festlegt, misst die Sitzung am einzigen vorhandenen Kern (`mtm_kern.py` mit `grundlage.lade_schlusskurse`), und die Aussage über den Erzeuger selbst heisst „nicht messbar“. Findet V1 Nr. 0 einen Kandidaten, beschreibt die Sitzung ihn und misst auch an ihm.
- **N5** (V2) „Die Lader“: `load_all_symbol_data` der vier Aktien-Bots. „Ausgabe des Laufs“: die Ausgaben nach R39 (Register Z. 10857). „Code des Laufs“, soweit es ihn gibt: Lader, Signalpfad und Zuteilung nach R43, `benchmark.py` (`tagesschluss`, `tagesgenau`, `bh_tagesrenditen`) und der Kern nach N4. „Zeile mit Datum ab dem Go-Live-Schnitt“: `open_time` am oder nach dem 2026-09-01.
- **N6** (V3) „Nicht endlich“: NaN, +inf, −inf; eine leere Zelle liest `pandas.read_csv` als NaN (die leere Zeichenkette steht in `pandas._libs.parsers.STR_NA_VALUES` der Umgebung: `docs/belege/TB-138/m1.txt` Z. 117). „Registrierte Definition“ eines Feldes: der Wortlaut der unter „Belegt“ genannten Registerstellen und jeder weiteren, die die Sitzung findet (O4).
- **N7** (Lesart des steuernden Chats, vorläufig) „benchmark.py wird nicht geöffnet“ (R72 (d), R78 (d)) heisst: nicht geändert. Die Klammer V2 verlangt selbst, `benchmark.py` zu lesen. Der Vorgänger brauchte die Datei nicht: Sein Auftrag sagt in Z. 171 „`benchmark.py` wird nicht geändert (R72 (d)); die Zählung braucht die Datei nicht“, und sein Messskript nennt sie nicht (0 Treffer für `benchmark` in `docs/belege/TB-138/verfahrensmessung_snapshot.py`).

**Offen:**

- **O1** Welchen Kern der Zellen-Erzeuger übernimmt (Register Z. 11493). Folge: N4.
- **O2** Ob `platform.platform()` heute noch den Wert des Locks liefert (ein Systemupdate ändert ihn). V4 misst es.
- **O3** Wie `importlib.metadata.version` in 3.9.6 Schreibweisen von Paketnamen angleicht (`pandas-market-calendars` im Lock, `pandas_market_calendars` beim Import). Vom Werkzeug abhängig: im Ergebnis beschreiben. Register Z. 3248 belegt nur das Ergebnis vom 19.09.2026 („0 Abweichungen“). Ebenso vom Werkzeug abhängig ist, was `importlib.metadata.distributions()` aufzählt (W2 in V4).
- **O4** Ob ausser 50.2, R33, R34, R36 und R68 weitere Registerstellen ein Feld von `zellen.csv` oder `zellenbericht.csv` festlegen. Die Sitzung sucht (V3 Nr. 1).
- **O5** Was das Register zum Ausstieg einer Position sagt, die am Ende der Spanne offen ist. Der Verfahrensprüfer hat dazu keinen Satz gelesen (Antwort, „Unsicher“ Nr. 2). Die Sitzung sagt, was der Code tut, und deutet nichts.
- **O6** Das Ergebnis des Cloud-Auftrags TB-137 liegt nicht im Repo. Seine Pakete 10 und 11 lesen zum Teil dieselben Dateien wie Teil 2 (`shared/zuteilung.py`, `mtm_kern.py`, `auswertung.py`, `benchmark.py`), am Stand `d781f1b` und mit anderen Fragen — so der Auftrag `logs/steuernder_chat/CLOUD_TB-137_sammelauftrag_leseaufgaben.md` (dort Z. 3, Z. 40 und Z. 42). Diese Datei liegt nicht im Repo (`logs/` ist von git ignoriert, `.gitignore` Z. 27); die Sitzung braucht nichts daraus und wartet nicht auf TB-137.
- **O7** Ob „eine andere Reihe“ in der Klammer zu R78 (a) auch eine Datei gleichen Namens in einem anderen Ordner als dem Snapshot meint. Die Klammer sagt „seine Tagesreihe im Snapshot“; aus welchem Ordner eine Lesestelle liest, steht erst im Lauf fest. Die Sitzung stellt Ordner, Datei und Spalte je Stelle fest, beschreibt den Weg zum Snapshot, soweit Code und Register ihn nennen (V1 Nr. 4), und urteilt darüber nicht; die Frage steht im Ergebnis unter „Für Fable“.

## Rückgaben und Urteile

**Rückgaben der Skripte, einheitlich** (wie Vorgänger Z. 134; gilt für jedes Skript dieses Auftrags, das misst):

- **rc 0** — gemessen, die Frage des Skripts ist erfüllt.
- **rc 1** — gemessen, nicht erfüllt: mindestens eine Abweichung, jede steht als Zeile in der Ausgabe. rc 1 heisst nie „nicht messbar“.
- **rc 2** — nicht messbar: Eine Eingabe fehlt, ist leer oder nicht lesbar, ein Werkzeug lädt nicht, **oder eine Ausnahme wurde nicht gefangen.** Jedes Python-Skript dieses Auftrags fängt am Einstieg jede Ausnahme, druckt den Traceback nach stdout und endet mit 2. Steht in einer Ausgabe ein Traceback, heisst die Messung „nicht messbar“, gleich welcher rc dahinter steht.

Vier Zusätze: (1) rc 0 ist für das Urteil *erfüllt* nötig, bei V4, V5 und V6 aber nicht hinreichend; die weitere Bedingung nennt der Abschnitt (V4: Hash des Locks und W2 · V5: V4 · V6: die Teile (ii) und (iii)). (2) Skripte, die kein Urteil rechnen (`z2_tb47.sh`, `suche.py`), enden mit 0 („gelesen“, „gesucht“) oder mit 2. (3) In einer Gegenprobe muss der Lauf an den veränderten Daten anschlagen (die Probe muss beissen; Prüfprinzipien B1) — bei V4, V5 und Z1 mit rc 1, bei V6 mit den sieben Rückgaben des Solls; die drei Gegenprobe-Skripte (`v4_gegenprobe.sh`, `v6_gegenprobe.sh`, `z1_gegenprobe.sh`) prüfen ihre Sollzeilen selbst und enden mit 0 und der Zeile `GEGENPROBE: beisst`, mit 1 und `GEGENPROBE: beisst NICHT`, oder mit 2 und einer Zeile mit `NICHT MESSBAR`, wenn die Gegenprobe selbst nicht laufen konnte (bei `v6_gegenprobe.sh`: `v6_zeile.py` fehlt oder ist leer, oder der Interpreter ist nicht aufrufbar). (4) Die zwei Vorlagen des Vorgängers für Schritt N, `einfuegen.py` und `c3_vergleich.py`, bleiben in ihrer Bauart: `c3_vergleich.py` endet auch bei `ABWEICHUNG` mit 0, und eine Ausnahme endet dort mit 1 (am 07.10.2026 an einer Kopie geprobt). Für diese zwei gilt die Zeile der Ausgabe, nicht der rc.

**Urteile je Teilfrage** — je Zeile genau eines, kein anderes Wort:

| Teilfrage | zulässige Urteile | Abschnitt |
|---|---|---|
| V4 (R79 (a)) | *erfüllt* · *nicht erfüllt* · *nicht messbar* · Zwischenurteil „W1 gleich, W2 abweichend“ | Teil 1, V4 |
| V5 (R79 (b)) | *erfüllt* · *nicht erfüllt* · *nicht messbar* · Zwischenurteil „gleich, aber nicht in der Lock-Umgebung gemessen“ | Teil 1, V5 |
| V6 (R79 (g)) | *erfüllt* · *nicht erfüllt* · *nicht messbar* · Zwischenurteil „erfüllt für den committeten Stand; für den Arbeitsbaum vom 02.10.2026 nicht belegt“ | Teil 1, V6 |
| Z1 (zu R79 (c)) | *erfüllt* · *nicht erfüllt* · *nicht messbar* | Teil 1, Z1 |
| Z2 (zu R79 (f)) | „belegt (Wortlaut)“ · „nur erschliessbar“ · „nicht gefunden“ · „nicht messbar“ (die Datei fehlt oder ist leer) | Teil 1, Z2 |
| V1 Nr. 0 | „kein Zellen-Erzeuger gefunden“ · „Kandidat gefunden“ | Teil 2, V1 |
| V1 (i) Benchmark (R78 (a)) | „Spalte und Datei wie die Klammer“ · „weicht ab“ · „am Code nicht entscheidbar“ — der Ordner steht als Tatsache daneben, ohne Urteil | Teil 2, V1 |
| V1 (ii) Kern (R78 (a)) | am vorhandenen Kern wie (i); für den Kern, den der Zellen-Erzeuger übernimmt: „nicht messbar“ — nur bei „kein Zellen-Erzeuger gefunden“ in Nr. 0; bei „Kandidat gefunden“ stattdessen „am Kandidaten gemessen:“ mit einem der drei Urteile aus (i) | Teil 2, V1 |
| V2 (a) (R78 (d)) | je Stelle „behält“ · „verwirft“ · „am Code nicht entscheidbar“ | Teil 2, V2 |
| V2 (b) (R78 (d)) | „ein solcher Wert wird gebildet“ · „kein solcher Wert wird gebildet“ · „am vorhandenen Code nicht entscheidbar“ | Teil 2, V2 |
| V3 (i) (R78 (e)) | kein Urteil der Sitzung: die Tabelle und die Zählung | Teil 2, V3 |
| V3 (ii) (R78 (e)) | „trifft zu“ · „trifft teils zu“ · „trifft nicht zu“ · „am Code nicht entscheidbar“ | Teil 2, V3 |

Ein Zwischenurteil ist kein Wort für „fast erfüllt“: Es steht für genau den Fall, den sein Abschnitt nennt, und wird überall ganz geführt (Zwischenstand, Zeile nach Teil 1, Ergebnis). *Erfüllt* und *nicht erfüllt* vergibt die Sitzung nur bei V4, V5, V6 und Z1; dort misst sie die ganze Aussage. Bei V1, V2 und V3 misst sie am Code einen Teil der Aussage oder beantwortet ein „ob“; dort trägt das Urteil das Wort seiner Zeile.

## Schritt 0 — Sicherung, Ausgang

0a. Wie Vorgänger (dort Z. 101), Dateien `"$TMPDIR/tb140_0a_head.txt"` und `"$TMPDIR/tb140_0a.txt"`, **bevor `docs/belege/TB-140/` entsteht** (den Ordner gibt es noch nicht). Soll: `main`, `8d172c0`, und genau diese sechs Einträge; die Reihenfolge zählt nicht. Alles andere ⇒ Abbruch und Meldung. (`AKTUELLER_AUFTRAG.md` stellt der steuernde Chat beim Legen dieses Auftrags um; steht sie noch wie am HEAD, fehlt ihr Eintrag, und 0a bricht ab.)

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-06a_verfahrensmessung_snapshot_aph.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-06a_verfahrensmessung_snapshot_aph.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-06_eroeffnung.md
```

Dazu in 0a, vor dem Commit: `md5 -r` (so in `docs/belege/TB-136/0b_ausgang.sh` Z. 16) und `wc -c` der drei Fable-Dateien nach `"$TMPDIR/tb140_0a_md5.txt"`, danach als `docs/belege/TB-140/0a_md5.txt`. Soll (alle drei am 07.10.2026 von einem Helfer am Repo gemessen; die Werte der Anfrage und des Eröffnungstexts stehen auch in `UEBERGABE.md`, Umzug 07.10.2026, 06:59, Block 3; den Wert der Antwort hat der steuernde Chat am 07.10.2026 in Ablage und Repo gemessen):

| Datei unter `docs/projektfuehrung/` | Bytes | md5 |
|---|---|---|
| `FABLE_ANFRAGE_2026-10-06a_verfahrensmessung_snapshot_aph.md` | 11 681 | `06ae4b76831d547cff57b2d2ce425dfb` |
| `FABLE_UEBERGABE_2026-10-06_eroeffnung.md` | 7 295 | `6e9fa10d1e7ae7c733ad1d889c6e81d4` |
| `FABLE_ANTWORT_2026-10-06a_verfahrensmessung_snapshot_aph.md` | 26 689 | `2fc513b93ef8b3ecb794a543c9fe5dc3` |

Weicht ein Wert ab ⇒ Abbruch und Meldung, kein Commit: Dann liegt nicht die Datei im Arbeitsbaum, die der steuernde Chat bewertet hat.

**Platzhaltersuche, in 0a vor dem Commit** (nach `"$TMPDIR/tb140_0a_platzhalter.txt"`, danach als `docs/belege/TB-140/0a_platzhalter.txt`): `grep -n` über den **ganzen** Auftrag und über `docs/projektfuehrung/UEBERGABE.md` nach zwei Klammeraffen in Folge (beide Dateien in einem Aufruf; so trägt jede Trefferzeile ihren Dateinamen). Soll: kein Treffer. *Grund:* Der steuernde Chat setzt sein Kürzel für die Uhrzeit des Nachtrags beim Ablegen an jeder Stelle ein — unter „Freigabe“ und in den Blocktexten E1 und J1; bleibt es an einer Stelle stehen, ist die Fundstelle dort nicht benannt. Dasselbe Kürzel trägt der Entwurf des Nachtrags in seiner Überschrift; bleibt es in `UEBERGABE.md` stehen, nennt jede Quellenangabe mit der Uhrzeit des Nachtrags eine Überschrift, die es so nicht gibt. **Ein Treffer ist kein Abbruch:** Die Sitzung committet, nennt jede Trefferzeile im Zwischenstand nach Teil 1 und im Ergebnis, und fügt E1 und J1 nicht ein, wenn ein Treffer in einem der zwei Blocktexte liegt (Schritt N). Ein Treffer in `UEBERGABE.md` ist ebenso kein Abbruch: Die Sitzung nennt ihn an denselben zwei Stellen, mit Datei und Zeile. Das Muster steht hier in Worten, damit dieser Absatz selbst kein Treffer ist.

Commit **genau dieser sechs** `TB-140 Schritt 0: Stand des steuernden Chats 07.10.2026`, pushen. Der Commit heisst im Folgenden **⟨S0⟩**. (Damit liegen Anfrage, Eröffnungstext und Antwort 06.10.a mit Commit im Repo. Die Antwort sagt dazu in Teil 0 Nr. 6: „R56 (b): Der Eröffnungstext muss mit Commit im Repo liegen, bevor diese Antwort eingetragen wird“.)

0b. `docs/belege/TB-138/0b_ausgang.sh` nach `docs/belege/TB-140/0b_ausgang.sh` übernehmen (geändert wird nur: Die Kennung `TB-138` in Z. 2, Z. 3 und Z. 11 — zwei Kommentarzeilen und die Kopfzeile der Ausgabe — wird `TB-140`, und in Z. 21 wird aus „(nur messen)“ „(Soll: 96a5c572...)“) ⇒ `docs/belege/TB-140/0b_ausgang.txt`. Sollwerte wie im Vorgänger (Tabelle dort ab Z. 113) mit zwei Unterschieden: HEAD ist ⟨S0⟩; `requirements.lock` hat jetzt ein Soll, `96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5` (Register Z. 3231). Für die zwei Universumsdateien verweist die Tabelle auf „Belegt“; gemeint ist das „Belegt“ des Vorgängers (dort Z. 66): `6acba892f38e998cf43ae9e5594c4707945143aba481429c44a5c6005339f607` für `sp500_top150.txt` und `3afc95a4f6b5ebc3a8f7bb7854b5dd59c4ecc4e3d86aa7b93c08066a3fccf810` für `top25_symbols.txt`. Vergleichswert für die Dateiliste des Snapshots: 226 Dateien, sha256 beginnt `e810849e` (`docs/belege/TB-138/0b_ausgang.txt`). Abbruch und Vermerk wie im Vorgänger (Z. 124); weicht der Hash des Locks ab ⇒ kein Abbruch, vermerken: V4 misst dann gegen einen Lock, der nicht der registrierte ist, und heisst „nicht messbar“.

## Teil 1 — V4, V5, V6, Z1, Z2 (zuerst; danach sofort committen, pushen, eine Zeile ausgeben, weiter)

Neue Werkzeuge unter `docs/belege/TB-140/` (sie werden committet). Von den Werkzeugen für Teil 1 importiert keines ein Modul des Repos, und keines schreibt in den Arbeitsbaum: Die Messskripte lesen nur und schreiben nur nach stdout; `v4_gegenprobe.sh` und `z1_gegenprobe.sh` legen dazu Kopien und kleine Ordner in einem frischen Ordner unter `$TMPDIR` an (`mktemp -d`; erlaubt nach Vorgänger Z. 27), die dort bleiben; `v6_gegenprobe.sh` schreibt nichts. Die Skizzen unten geben Gegenstand und Ausgabeform vor, nicht jede Zeile; weicht die Sitzung ab, sagt das Ergebnis, wo und warum. Eine Erwartung an ein Werkzeug steht nur mit Fundstelle im Werkzeug da; wo keine steht, gilt: vom Werkzeug abhängig, im Ergebnis beschreiben.

**Probestand der Skizzen, und worin er von der Regel abweicht.** ARBEITSWEISE 0 („Wenn ich einen Auftrag schreibe“) verlangt: „das Prüfskript läuft vor der Freigabe am echten Repo, nicht nur an einer Kopie (TB-130)“. Das ist hier nur zum Teil erfüllt. *Grund:* `trading-env` ist ein macOS-venv und startet in der Linux-VM der Geräteanbindung nicht (Vorgänger O2), und ein Helfer liest das Repo nur. Jede Skizze ist auf Syntax geprüft (Python mit `ast` für 3.9, Shell mit `bash -n`) und am 07.10.2026 von einem Helfer in der VM gelaufen (Python 3.10.12, bash 5.1.16; am Repo nur lesend am HEAD `8d172c0`, Ausgaben ausserhalb des Repos): `v4_gegenprobe.sh` mit `v4_umgebung.py` an zwei Kopien des Locks (rc 0, `beisst`; die Pakete der VM sind erwartbar andere) · `v5_schedule_je_bot.py` mit dem echten Kalender und den vier Paketen in den Fassungen des Locks (`pandas_market_calendars` 4.6.1, `exchange_calendars` 4.5.6, `pandas` 2.3.3, `numpy` 2.0.2, in einem Ordner ausserhalb des Repos): Gegenprobe rc 1 mit den Sollzeilen, Messung rc 0 · `v6_gegenprobe.sh` (rc 0, `beisst`) und `v6_bestand.sh` als Ganzes am Repo (rc 0, `TEIL (i) ja · (ii) ja · (iii) ja`) · `z1_gegenprobe.sh` (rc 0, `beisst`) und `z1_close_je_datei.py` am Snapshot (rc 0, pandas 2.3.3) · `z2_tb47.sh` am Repo (rc 0) · `suche.py` am Repo (rc 0). Die Skizzen für Schritt N und D1 tragen ihren Probestand an ihrem Ort. **Nicht gelaufen** ist irgendetwas in `trading-env`, mit Python 3.9.6 oder auf macOS (die `bash` 3.2 des Macs und sein `mktemp`, `awk`, `diff`, `shasum`, `md5 -r`). Darum steht über jeder Skizze der Satz, dass die Sitzung sie anpasst, wenn sie am Werkzeug nicht passt.

### V4 — `trading-env` gegen den ganzen Lock und die Plattform (R79 (a))

`docs/belege/TB-140/v4_umgebung.py`, Aufruf aus der Repo-Wurzel:

```
trading-env/bin/python3 -B docs/belege/TB-140/v4_umgebung.py > docs/belege/TB-140/v4.txt 2>&1; echo "rc $?" >> docs/belege/TB-140/v4.txt
```

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```python
#!/usr/bin/env python3
"""TB-140 V4 - die Umgebung dieses Interpreters gegen requirements.lock:
jede Paketzeile, Interpreter, Plattform. Liest nur, schreibt nur nach stdout.
Rueckgabe: 0 Kopf und W1 gleich, 1 Abweichung in Kopf oder W1, 2 nicht messbar (der Lock fehlt
oder traegt keine Paketzeile, oder eine Ausnahme). W2 wird gedruckt und geht nicht in die
Rueckgabe ein (N1 und O3: vom Werkzeug abhaengig)."""
import argparse
import datetime as dt
import hashlib
import importlib.metadata as md
import os
import platform
import re
import sys
import traceback

LOCK = "requirements.lock"
LOCK_SHA256 = "96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5"  # Register Z. 3231
PAKETE_SOLL = 67                                                                    # Register Z. 3232


def norm(name):
    """Schreibweise nach PEP 503."""
    return re.sub(r"[-_.]+", "-", name).lower()


def lies_lock(pfad):
    """Gelesen wie shared/paths.py::_lies_lock (Z. 499): Kopf `# schluessel wert`, erste Nennung gilt."""
    kopf, pakete, fremd = {}, [], []
    with open(pfad, encoding="utf-8") as f:
        for nr, zeile in enumerate(f, 1):
            zeile = zeile.strip()
            if not zeile:
                continue
            if zeile.startswith("#"):
                teile = zeile[1:].split()
                if len(teile) >= 2:
                    kopf.setdefault(teile[0], " ".join(teile[1:]))
                continue
            if "==" not in zeile:
                fremd.append((nr, zeile))
                continue
            name, fassung = zeile.split("==", 1)
            pakete.append((nr, name.strip(), fassung.strip()))
    return kopf, pakete, fremd


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--lock", default=LOCK)
    x = a.parse_args(argv)
    if not os.path.isfile(x.lock):
        print("NICHT MESSBAR: %s fehlt" % x.lock)
        return 2
    kopf, pakete, fremd = lies_lock(x.lock)
    if not pakete:
        print("NICHT MESSBAR: keine Paketzeile in %s" % x.lock)
        return 2
    with open(x.lock, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    abw = 0
    print("# TB-140 V4")
    print("zeit             %s" % dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    print("sys.executable   %s" % sys.executable)
    print("sys.prefix       %s" % sys.prefix)
    print("lock             %s  sha256 %s  %s" % (
        x.lock, sha, "gleich Register" if sha == LOCK_SHA256 else "UNGLEICH Register"))
    print("Paketzeilen      %d (Register: %d), Zeilen ohne `==`: %d" % (len(pakete), PAKETE_SOLL, len(fremd)))

    print("\n## Kopf des Locks gegen die Umgebung")
    paare = (("interpreter_voll", " ".join(sys.version.split()), "prueft der Lauf"),
             ("plattform", platform.platform(), "prueft der Lauf"),
             ("interpreter_venv", sys.version.split()[0], "prueft der Lauf nicht; erstes Wort"),
             ("maschine", platform.machine(), "prueft der Lauf nicht; ohne Urteil"))
    for schluessel, ist, wer in paare:
        soll = kopf.get(schluessel)
        if schluessel == "interpreter_venv" and soll:
            soll = soll.split()[0]
        gleich = soll == ist
        if not gleich and schluessel != "maschine":
            abw += 1
        print("KOPF\t%s\t%r\t%r\t%s\t(%s)" % (schluessel, soll, ist, "gleich" if gleich else "ABWEICHUNG", wer))

    print("\n## W1  importlib.metadata.version(name) je Lock-Zeile (der Weg des Laufs)")
    w1_gleich = 0
    for nr, name, soll in pakete:
        try:
            ist = md.version(name)
        except md.PackageNotFoundError:
            ist = None
        if ist == soll:
            w1_gleich += 1
        else:
            abw += 1
            print("PAKET\tW1\t%d\t%s\t%s\t%s" % (nr, name, soll, ist if ist is not None else "FEHLT"))
    print("W1 gleich %d von %d" % (w1_gleich, len(pakete)))

    print("\n## W2  alle installierten Distributionen, Namen nach PEP 503 (ohne Einfluss auf die Rueckgabe)")
    w2 = "nicht messbar"
    try:
        inst = {}
        for d in md.distributions():
            n = d.metadata["Name"]
            if n:
                inst.setdefault(norm(n), set()).add(d.version)
        w2_gleich = 0
        for nr, name, soll in pakete:
            ist = inst.get(norm(name), set())
            if ist == {soll}:
                w2_gleich += 1
            else:
                print("PAKET\tW2\t%d\t%s\t%s\t%s" % (nr, name, soll, ",".join(sorted(ist)) or "FEHLT"))
        print("W2 gleich %d von %d" % (w2_gleich, len(pakete)))
        im_lock = {norm(n) for _, n, _ in pakete}
        nur_inst = sorted(n for n in inst if n not in im_lock)
        doppelt = sorted(n for n, v in inst.items() if len(v) > 1)
        print("installiert, nicht im Lock (ohne Urteil): %d %s" % (len(nur_inst), nur_inst))
        print("mehr als eine Fassung installiert (ohne Urteil): %d %s" % (len(doppelt), doppelt))
        w2 = "gleich" if w2_gleich == len(pakete) else "ABWEICHEND in %d Zeilen" % (len(pakete) - w2_gleich)
    except Exception as e:  # noqa: BLE001
        print("W2 NICHT MESSBAR: %s: %s" % (type(e).__name__, e))

    erfuellt = abw == 0 and not fremd
    print("\nURTEIL V4 gegen %s, Kopf und W1: %s" % (x.lock, "gleich" if erfuellt else "NICHT gleich"))
    print("W2 (ohne Einfluss auf die Rueckgabe): %s" % w2)
    print("RUECKGABE %d" % (0 if erfuellt else 1))
    return 0 if erfuellt else 1


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
```

**Gegenprobe vor der Messung** (Prüfprinzipien B1) mit `docs/belege/TB-140/v4_gegenprobe.sh`, Aufruf aus der Repo-Wurzel:

```
bash docs/belege/TB-140/v4_gegenprobe.sh > docs/belege/TB-140/v4_gegenprobe.txt 2>&1; echo "rc $?" >> docs/belege/TB-140/v4_gegenprobe.txt
```

Das Skript legt in einem frischen Ordner unter `$TMPDIR` zwei Kopien des Locks an. Die erste bleibt unverändert. In der zweiten drei Eingriffe: G1 die Zeile `pandas==2.3.3` wird `pandas==0.0.1` (die Probe aus Register Z. 3261) · G2 eine Zeile `kein-solches-paket-tb140==1.0` kommt dazu · G3 die Kopfzeile `# plattform` bekommt den Wert `andere-plattform`. Dann läuft `v4_umgebung.py` je Kopie mit `--lock`.

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```bash
#!/bin/bash
# TB-140 V4 - Gegenprobe: v4_umgebung.py an zwei Kopien des Locks in einem frischen Ordner unter $TMPDIR.
# Die erste Kopie bleibt unveraendert; die zweite traegt G1 (pandas==0.0.1), G2 (ein Paket, das es
# nicht gibt) und G3 (eine andere Plattform im Kopf). Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-140/v4_gegenprobe.sh
# Rueckgabe: 0 die Probe beisst (alle Sollzeilen da), 1 eine Sollzeile fehlt, 2 nicht messbar.
set -u
PY="${PY:-trading-env/bin/python3}"
V="${V:-docs/belege/TB-140/v4_umgebung.py}"
LOCK="${LOCK:-requirements.lock}"
echo "# TB-140 V4 GEGENPROBE"
if [ ! -s "$LOCK" ]; then echo "NICHT MESSBAR: $LOCK fehlt oder ist leer"; exit 2; fi
T="$(mktemp -d "${TMPDIR:-/tmp}/tb140_v4_gegenprobe.XXXXXX")" || { echo "NICHT MESSBAR: kein Ordner unter TMPDIR"; exit 2; }
echo "Ordner $T"
cp "$LOCK" "$T/k1.lock"
$PY -B - "$LOCK" "$T/k2.lock" <<'PYEOF' || { echo "NICHT MESSBAR: die zweite Kopie liess sich nicht bauen"; exit 2; }
import sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
g1 = [i for i, s in enumerate(z) if s.strip() == "pandas==2.3.3"]
g3 = [i for i, s in enumerate(z) if s.startswith("# plattform ")]
assert len(g1) == 1 and len(g3) == 1, (g1, g3)
z[g1[0]] = "pandas==0.0.1"                           # G1, die Probe aus Register Z. 3261
z[g3[0]] = "# plattform         andere-plattform"   # G3
while z and z[-1] == "":
    z.pop()
z.append("kein-solches-paket-tb140==1.0")            # G2
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(z) + "\n")
print("zweite Kopie: G1 in Z. %d, G3 in Z. %d, G2 als letzte Zeile" % (g1[0] + 1, g3[0] + 1))
PYEOF
echo "## erste Kopie (unveraendert)"
$PY -B "$V" --lock "$T/k1.lock" > "$T/a.txt" 2>&1; RC1=$?; cat "$T/a.txt"; echo "rc $RC1"
echo "## zweite Kopie (G1, G2, G3)"
$PY -B "$V" --lock "$T/k2.lock" > "$T/b.txt" 2>&1; RC2=$?; cat "$T/b.txt"; echo "rc $RC2"
echo "## Unterschied der Zeilen KOPF und PAKET (< erste Kopie, > zweite Kopie)"
diff <(grep -E '^(KOPF|PAKET)' "$T/a.txt") <(grep -E '^(KOPF|PAKET)' "$T/b.txt")
zahl() { awk -F'\t' "$1" "$2" | wc -l | tr -d ' '; }
S1=$(zahl '$1=="KOPF" && $2=="plattform" && $3 ~ /andere-plattform/ && $5=="ABWEICHUNG"' "$T/b.txt")
S2=$(zahl '$1=="PAKET" && $2=="W1" && $4=="pandas" && $5=="0.0.1"' "$T/b.txt")
S3=$(zahl '$1=="PAKET" && $2=="W1" && $4=="kein-solches-paket-tb140" && $6=="FEHLT"' "$T/b.txt")
N1=$(zahl '$1=="PAKET" && ($5=="0.0.1" || $4=="kein-solches-paket-tb140")' "$T/a.txt")
if grep -q '^W2 NICHT MESSBAR' "$T/b.txt"; then S4=-; S5=-
else
  S4=$(zahl '$1=="PAKET" && $2=="W2" && $4=="pandas" && $5=="0.0.1"' "$T/b.txt")
  S5=$(zahl '$1=="PAKET" && $2=="W2" && $4=="kein-solches-paket-tb140" && $6=="FEHLT"' "$T/b.txt")
fi
echo "## Soll"
echo "zweite Kopie: rc $RC2 (Soll 1) · KOPF plattform ABWEICHUNG $S1 (Soll 1) · PAKET W1 pandas 0.0.1: $S2 (Soll 1) · PAKET W1 kein-solches-paket-tb140 FEHLT: $S3 (Soll 1)"
echo "zweite Kopie, W2: PAKET W2 pandas 0.0.1: $S4 · PAKET W2 kein-solches-paket-tb140 FEHLT: $S5 (Soll je 1; ein Strich heisst: W2 war nicht messbar, die zwei Zeilen entfallen)"
echo "erste Kopie: keine dieser PAKET-Zeilen: $N1 (Soll 0)"
if [ "$RC1" = 2 ] || [ "$RC2" = 2 ]; then echo "GEGENPROBE: NICHT MESSBAR"; exit 2; fi
if [ "$RC2" = 1 ] && [ "$S1$S2$S3$N1" = "1110" ] && { [ "$S4$S5" = "11" ] || [ "$S4$S5" = "--" ]; }; then echo "GEGENPROBE: beisst"; exit 0; fi
echo "GEGENPROBE: beisst NICHT"; exit 1
```

**Soll der Gegenprobe:** rc 0 und die Zeile `GEGENPROBE: beisst`. Im Einzelnen: Der Lauf an der zweiten Kopie endet mit rc 1. Verglichen werden nur die Zeilen `KOPF` und `PAKET` der zwei Läufe (so vergleicht der Vorgänger nur die Zeilen der Einzelfälle, dort Z. 149); ihr Unterschied ist genau dieser: Die Zeile `KOPF plattform` trägt an der zweiten Kopie das Soll `andere-plattform` und `ABWEICHUNG` — sie ist geändert, nicht zusätzlich —, und vier Zeilen `PAKET` kommen dazu: W1 und W2 für `pandas` (Lock 0.0.1), W1 und W2 für `kein-solches-paket-tb140` mit `FEHLT` (dass `importlib.metadata.version` bei einem fehlenden Paket `PackageNotFoundError` wirft, setzt auch der Lauf voraus: `shared/paths.py` Z. 557). Die Zählzeilen (`lock … UNGLEICH Register`, `Paketzeilen 68`, `W1 gleich … von 68`, `W2 gleich … von 68`), die Zeile `URTEIL` und die Zeile `W2 (ohne Einfluss …)` ändern sich mit und sind kein Soll; der rc an der ersten Kopie ist kein Soll. Meldet der Lauf `W2 NICHT MESSBAR`, entfallen die zwei Sollzeilen für W2 (vom Werkzeug abhängig, im Ergebnis beschreiben). Steht `beisst NICHT` da ⇒ Skript berichtigen, Gegenprobe wiederholen; erst danach die Messung. Die Kopien bleiben in `$TMPDIR`.

**Soll der Messung:** rc 0 · `lock … gleich Register` · 67 Paketzeilen, keine Zeile ohne `==` · `KOPF interpreter_voll`, `plattform`, `interpreter_venv` gleich · W1 67 von 67. Vergleichswert für `maschine`: `x86_64` (Lock Z. 9). **Vom Werkzeug abhängig, im Ergebnis beschreiben:** W2 — was `importlib.metadata.distributions()` aufzählt, ob W2 dieselben Zeilen meldet wie W1 (O3) und wie viele Distributionen installiert sind und nicht im Lock stehen (der Lock entstand laut seinem Kopf, Z. 2, aus `pip freeze --all`). Für W2 steht keine Fundstelle im Werkzeug da, deshalb ist „W2 67 von 67“ kein Soll; Vergleichswerte stehen unter „Belegt“ (Lock Z. 2 bis Z. 4; 67 Ordner `*.dist-info`). Gehen W1 und W2 auseinander, beschreibt die Sitzung beide: jede Zeile `PAKET W1` und `PAKET W2` und die zwei Zeilen „installiert, nicht im Lock“ und „mehr als eine Fassung installiert“.

**Urteil V4** (eines aus der Tabelle „Urteile je Teilfrage“): *erfüllt*, wenn rc 0, der Lock den Hash des Registers trägt und W2 keine Zeile meldet. *Nicht erfüllt* bei rc 1 — das ist eine Zeile `KOPF … ABWEICHUNG` für `interpreter_voll`, `plattform` oder `interpreter_venv`, eine Zeile `PAKET W1` oder eine Paketzeile ohne `==`: jede einzeln nennen, mit Lock-Zeile, Soll und Ist. *Zwischenurteil „W1 gleich, W2 abweichend“*, wenn rc 0 ist und nur W2 eine Zeile meldet (etwa zwei Fassungen desselben Pakets nebeneinander) oder W2 nicht messbar war: Die Sitzung entscheidet dann nicht und beschreibt beide Wege, mit jeder Zeile. *Nicht messbar* bei rc 2, bei einem Traceback oder bei einem Lock mit anderem Hash als dem des Registers. **Ein Befund ist kein Abbruch:** nennen, V5, V6, Z1 und Z2 trotzdem messen. Heisst V4 nicht *erfüllt*, kann V5 höchstens das Zwischenurteil „gleich, aber nicht in der Lock-Umgebung gemessen“ tragen.

### V5 — ein Aufruf von `schedule` je Aktien-Bot gegen den Ausschnitt (R79 (b))

`docs/belege/TB-140/v5_schedule_je_bot.py`; es liest **keine** Kursdatei. Zuerst `… v5_schedule_je_bot.py --gegenprobe > docs/belege/TB-140/v5_gegenprobe.txt 2>&1`, dann ohne Schalter ⇒ `v5.txt`, je mit angehängtem `rc`.

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```python
#!/usr/bin/env python3
"""TB-140 V5 - ein eigener Aufruf von schedule je Aktien-Bot gegen den Ausschnitt
aus der einmal gerechneten Menge (R79 (b)). Liest keine Kursdatei, schreibt nur nach stdout.
Rueckgabe: 0 gleich bei allen vier Bots, 1 Abweichung, 2 nicht messbar (der Kalender laedt nicht,
schedule liefert keinen Tag, oder eine Ausnahme)."""
import argparse
import datetime as dt
import importlib.metadata as md
import platform
import sys
import traceback

KALENDER_NAME = "NYSE"                      # R74 (a); kein anderer Name
GANZ_VON = dt.date(1962, 1, 2)              # docs/belege/TB-138/m1.txt Z. 19
GANZ_BIS = dt.date(2026, 9, 1)              # ebd.
ENDE = dt.date(2026, 8, 31)                 # Register 35.1, Z. 6385-6388 (Ende ausschliesslich)
BOTS = (("elliott_wave_stocks", 2017),      # Register 33.2, Z. 6001-6004
        ("rsi2_mean_reversion", 2018),
        ("turtle_soup_stocks", 2017),
        ("volatility_breakout", 2018))
PAKETE = ("pandas_market_calendars", "pandas", "exchange_calendars", "numpy")


def tage(kal, von, bis):
    """Der Aufruf des Vorgaengers (verfahrensmessung_snapshot.py Z. 230-231)."""
    plan = kal.schedule(start_date=von.isoformat(), end_date=bis.isoformat())
    return [ts.date() for ts in plan.index]


def vergleiche(bot, ausschnitt, aufruf):
    """Druckt die Zeilen eines Bots; True, wenn beide Mengen gleich sind und der Index keinen Tag doppelt fuehrt."""
    a, b = set(ausschnitt), set(aufruf)
    nur_a, nur_b = sorted(a - b), sorted(b - a)
    for t in nur_a:
        print("FALL\tv5\tnur_im_ausschnitt\t%s\t%s" % (bot, t))
    for t in nur_b:
        print("FALL\tv5\tnur_im_aufruf\t%s\t%s" % (bot, t))
    doppelt = len(aufruf) - len(b)
    print("%s: Ausschnitt %d, Aufruf %d (doppelt im Index %d), nur im Ausschnitt %d, nur im Aufruf %d, "
          "erster Tag %s / %s, letzter Tag %s / %s"
          % (bot, len(a), len(b), doppelt, len(nur_a), len(nur_b),
             min(a) if a else "-", min(b) if b else "-", max(a) if a else "-", max(b) if b else "-"))
    return not nur_a and not nur_b and doppelt == 0


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--gegenprobe", action="store_true")
    x = p.parse_args(argv)
    print("# TB-140 V5%s" % (" GEGENPROBE" if x.gegenprobe else ""))
    print("zeit             %s" % dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    print("sys.executable   %s" % sys.executable)
    print("sys.version      %s" % " ".join(sys.version.split()))
    print("platform         %s" % platform.platform())
    for name in PAKETE:
        try:
            print("%-24s %s" % (name, md.version(name)))
        except md.PackageNotFoundError:
            print("%-24s nicht installiert" % name)
    try:
        import pandas_market_calendars as mcal
        kal = mcal.get_calendar(KALENDER_NAME)
    except Exception as e:  # noqa: BLE001
        print("NICHT MESSBAR: Kalender %r nicht ladbar: %s: %s" % (KALENDER_NAME, type(e).__name__, e))
        return 2
    ganz = tage(kal, GANZ_VON, GANZ_BIS)
    if not ganz:
        print("NICHT MESSBAR: schedule liefert fuer %s..%s keinen Tag" % (GANZ_VON, GANZ_BIS))
        return 2
    print("\neinmal gerechnete Menge %s..%s: %d Tage" % (GANZ_VON, GANZ_BIS, len(set(ganz))))
    alle_gleich = True
    for bot, jahr in BOTS:
        von = dt.date(jahr, 1, 1)
        ausschnitt = [t for t in ganz if von <= t <= ENDE]
        aufruf = tage(kal, von, ENDE)
        if x.gegenprobe:
            # ein Tag fehlt im Ausschnitt, ein Samstag steht zu viel darin
            samstag = von + dt.timedelta(days=(5 - von.weekday()) % 7)
            ausschnitt = ausschnitt[:100] + ausschnitt[101:] + [samstag]
        gleich = vergleiche(bot, ausschnitt, aufruf)
        alle_gleich = alle_gleich and gleich
        print("    URTEIL V5 %s, Zeitraum %s..%s: %s" % (bot, von, ENDE, "gleich" if gleich else "NICHT gleich"))
    print("\nRUECKGABE %d" % (0 if alle_gleich else 1))
    return 0 if alle_gleich else 1


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
```

**Soll der Gegenprobe:** rc 1; je Bot genau zwei Zeilen `FALL` — eine `nur_im_aufruf` (der 101. Tag des Ausschnitts) und eine `nur_im_ausschnitt` (der erste Samstag ab dem Beginn: 2017-01-07 und 2018-01-06) — und viermal `NICHT gleich`. Meldet das Skript das nicht ⇒ berichtigen und wiederholen. Dass ein Samstag kein Sitzungstag ist, ist dabei Erwartung an den Kalender: vom Werkzeug abhängig; fehlt die Zeile `nur_im_ausschnitt` nur deshalb, steht das im Ergebnis und ist kein Fehler des Skripts.

**Soll der Messung:** rc 0; je Bot Ausschnitt gleich Aufruf, keine Zeile `FALL`, kein doppelter Tag. **Vergleichswerte, kein Soll:** 16 275 Tage in der ganzen Menge (`m1.txt` Z. 20), 2 428 Tage ab 2017 und 2 177 ab 2018 (`m1.txt` Z. 95, 100, 105, 110). Dieselben drei Zahlen lieferte der Probelauf der Skizze in der Linux-VM am 07.10.2026 (Python 3.10.12, die vier Pakete in den Fassungen des Locks, nicht `trading-env`). Weicht eine dieser Zahlen ab und sind Ausschnitt und Aufruf trotzdem gleich ⇒ V5 ist gleich, die Abweichung zum Vorgänger wird eigens gemeldet.

**Urteil V5** (eines aus der Tabelle „Urteile je Teilfrage“): *erfüllt*, wenn rc 0 und V4 *erfüllt* heisst. *Nicht erfüllt* bei rc 1: jeden Tag einzeln nennen. *Nicht messbar* bei rc 2 oder einem Traceback. *Zwischenurteil „gleich, aber nicht in der Lock-Umgebung gemessen“*, wenn rc 0 ist und V4 nicht *erfüllt* heisst (auch bei einem Zwischenurteil oder „nicht messbar“ in V4). Kein anderer Kalendername wird gerechnet (Vorgänger Z. 25).

### V6 — der Bestand vom 02.10.2026 an `APH` (R79 (g))

Drei Werkzeuge: `docs/belege/TB-140/v6_zeile.py` (liest eine Tagesreihe von stdin, druckt zu einem Datum nur die Namen der Spalten, in denen der Wert fehlt), `docs/belege/TB-140/v6_gegenprobe.sh` und `docs/belege/TB-140/v6_bestand.sh`. Aufruf aus der Repo-Wurzel, zuerst die Gegenprobe:

```
bash docs/belege/TB-140/v6_gegenprobe.sh > docs/belege/TB-140/v6_gegenprobe.txt 2>&1; echo "rc $?" >> docs/belege/TB-140/v6_gegenprobe.txt
bash docs/belege/TB-140/v6_bestand.sh > docs/belege/TB-140/v6.txt 2>&1; echo "rc $?" >> docs/belege/TB-140/v6.txt
```

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```python
#!/usr/bin/env python3
"""TB-140 V6 - liest eine Tagesreihe von stdin und druckt zu einem Datum nur,
in welchen Spalten der Wert fehlt. Kein Kurs wird ausgegeben oder in eine Zahl gewandelt.
Rueckgabe: 0 genau eine Zeile mit dem Datum, und close fehlt dort; 1 close ist vorhanden, oder die
Zeile gibt es nicht genau einmal; 2 nicht messbar (leere Eingabe, Kopfzeile ohne open_time an
erster Stelle oder ohne close, oder eine Ausnahme)."""
import sys
import traceback

# L5 des Vorgaengers: leer oder ein Text, den pandas.read_csv als Fehlwert liest
FEHLWERT = {"#N/A", "#N/A N/A", "#NA", "-1.#IND", "-1.#QNAN", "-NaN", "-nan", "1.#IND", "1.#QNAN",
            "<NA>", "N/A", "NA", "NULL", "NaN", "None", "n/a", "nan", "null"}


def main(argv):
    datum = argv[1] if len(argv) > 1 else "2026-09-01"
    zeilen = sys.stdin.read().splitlines()
    if not zeilen:
        print("NICHT MESSBAR: leere Eingabe")
        return 2
    kopf = zeilen[0].split(",")
    if kopf[0] != "open_time" or "close" not in kopf:
        print("NICHT MESSBAR: Kopfzeile ohne open_time an erster Stelle oder ohne close (%d Felder, Inhalt nicht gedruckt)" % len(kopf))
        return 2
    treffer = [z.split(",") for z in zeilen[1:] if z.split(",")[0] == datum]
    print("Kopf %s; Datenzeilen %d; letzte Datumszelle %s" % (",".join(kopf), len(zeilen) - 1, zeilen[-1].split(",")[0]))
    print("Zeilen mit open_time %s: %d" % (datum, len(treffer)))
    if len(treffer) != 1:
        print("die Zeile gibt es nicht genau einmal")
        return 1
    felder = treffer[0]
    leer = [k for k, v in zip(kopf, felder) if v == ""]
    text = [k for k, v in zip(kopf, felder) if v in FEHLWERT]
    ohne = kopf[len(felder):]
    print("Zeile %s: %d Spalten; leer: %s; Fehlwert-Text: %s; Spalte fehlt: %s" % (datum, len(felder), leer, text, ohne))
    fehlt = "close" in leer or "close" in text or "close" in ohne
    print("close fehlt: %s" % ("ja" if fehlt else "nein"))
    return 0 if fehlt else 1


if __name__ == "__main__":
    try:
        RC = main(sys.argv)
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
```

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```bash
#!/bin/bash
# TB-140 V6 - Gegenprobe zu v6_zeile.py an sieben kleinen Texten; die Kursspalten tragen den Text x.
# Schreibt nichts. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-140/v6_gegenprobe.sh
# Rueckgabe: 0 alle sieben Rueckgaben wie das Soll (die Probe beisst), 1 eine weicht ab, 2 nicht messbar.
set -u
PY="${PY:-trading-env/bin/python3}"
ZP="${ZP:-docs/belege/TB-140/v6_zeile.py}"
IST=""
probe() {  # $1 Name, $2 Soll; der Text kommt von stdin
  echo "## $1 (Soll rc $2)"
  $PY -B "$ZP" 2026-09-01; local rc=$?
  echo "rc $rc"; IST="$IST$rc"
}
echo "# TB-140 V6 GEGENPROBE"
[ -s "$ZP" ] && command -v "$PY" >/dev/null 2>&1 || { echo "GEGENPROBE: NICHT MESSBAR: $ZP oder $PY fehlt"; exit 2; }
probe "G1 Zeile mit close" 1 <<'CSV'
open_time,open,high,low,close,volume
2026-08-31,x,x,x,x,x
2026-09-01,x,x,x,x,x
CSV
probe "G2 close leer" 0 <<'CSV'
open_time,open,high,low,close,volume
2026-08-31,x,x,x,x,x
2026-09-01,,,,,x
CSV
probe "G3 close mit Fehlwert-Text NaN" 0 <<'CSV'
open_time,open,high,low,close,volume
2026-09-01,x,x,x,NaN,x
CSV
probe "G4 Datum fehlt" 1 <<'CSV'
open_time,open,high,low,close,volume
2026-08-31,x,x,x,x,x
CSV
probe "G5 Zeile doppelt" 1 <<'CSV'
open_time,open,high,low,close,volume
2026-09-01,,,,,x
2026-09-01,,,,,x
CSV
probe "G6 leere Eingabe" 2 < /dev/null
probe "G7 Kopfzeile ohne close" 2 <<'CSV'
open_time,open,high,low,volume
2026-09-01,x,x,x,x
CSV
echo "## Soll"
echo "Rueckgaben $IST (Soll 1001122)"
if [ "$IST" = "1001122" ]; then echo "GEGENPROBE: beisst"; exit 0; fi
echo "GEGENPROBE: beisst NICHT"; exit 1
```

**Soll der Gegenprobe:** rc 0 und die Zeile `GEGENPROBE: beisst`. Die sieben Rückgaben von `v6_zeile.py`, in dieser Folge: Zeile mit `close` ⇒ 1 · `close` leer ⇒ 0 · `close` mit dem Text `NaN` ⇒ 0 · Datum fehlt ⇒ 1 · Zeile doppelt ⇒ 1 · leere Eingabe ⇒ 2 · Kopfzeile ohne `close` ⇒ 2. Steht `beisst NICHT` da ⇒ berichtigen und wiederholen; erst danach die Messung. Das Skript schreibt nichts.

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```bash
#!/bin/bash
# TB-140 V6 - der Bestand vom 02.10.2026 an APH. Rein lesend. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-140/v6_bestand.sh
# Rueckgabe: die von v6_zeile.py am Stand der Messung, das ist Teil (i): 0 genau eine Zeile
# 2026-09-01 ohne close, 1 nicht so, 2 nicht messbar. Die Teile (ii) und (iii) stehen in der Zeile TEIL.
set -u
PY="${PY:-trading-env/bin/python3}"
ZP="${ZP:-docs/belege/TB-140/v6_zeile.py}"
G="git --no-optional-locks"
S=snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
D=data/APH_1d.csv
B=0779453                          # Stand der Messung vom 02.10.2026 (Register Z. 11482; v3_daten.md Z. 3)
GRENZE=2026-10-01T22:00:00+00:00   # der 02.10.2026, 00:00 Uhr nach der Uhr des Repos (+02:00)
echo "# TB-140 V6"; echo "ZEIT $(date '+%Y-%m-%d %H:%M:%S %z')"; echo "HEAD $($G rev-parse HEAD)"
echo "## Stand der Messung vom 02.10.2026"
if ! $G rev-parse --verify --quiet "$B^{commit}" > /dev/null; then
  echo "NICHT MESSBAR: Stand $B unbekannt"; echo "TEIL (i) nicht messbar · (ii) nicht messbar · (iii) nicht messbar"; echo "## Ende"; exit 2
fi
$G log -1 --format='%H %cI %s' "$B"
echo "## Commits an $D (alle)"; $G log --format='%h %cI %s' -- "$D"
echo "## Commits an $D nach dem Stand $B"; NACH=$($G log --format='%h %cI %s' "$B..HEAD" -- "$D"); printf '%s\n' "${NACH:-keiner}"
echo "## Blobs in git"
BB=$($G rev-parse --verify --quiet "$B:$D") || BB=fehlt
echo "$B:$D $BB"
echo "HEAD:$D $($G rev-parse --verify --quiet "HEAD:$D" || echo fehlt)"
echo "$B:$S/APH_1d.csv $($G rev-parse --verify --quiet "$B:$S/APH_1d.csv" || echo fehlt)"
echo "HEAD:$S/APH_1d.csv $($G rev-parse --verify --quiet "HEAD:$S/APH_1d.csv" || echo fehlt)"
echo "## Arbeitsdateien: Blob (gerechnet wie git: sha1 ueber 'blob <Bytes>', ein Nullbyte und den Inhalt; git wird dafuer nicht aufgerufen), sha256, Bytes, Aenderungszeit (UTC)"
AD=$($PY -B -c "import datetime as d, hashlib, os, sys
grenze = d.datetime.fromisoformat(sys.argv[1])
for nr, p in enumerate(sys.argv[2:]):
    try:
        with open(p, 'rb') as f:
            b = f.read()
        zeit = d.datetime.fromtimestamp(os.stat(p).st_mtime, d.timezone.utc)
        blob = hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
        print('ARBEITSDATEI\t%s\tblob %s\tsha256 %s\tbytes %d\tmtime %s' % (
            p, blob, hashlib.sha256(b).hexdigest(), len(b), zeit.isoformat(timespec='seconds')))
        if nr == 0:
            print('WERT\tblob\t%s' % blob)
            print('WERT\tvor_grenze\t%s' % ('ja' if zeit < grenze else 'nein'))
    except Exception as e:
        print('ARBEITSDATEI\t%s\tNICHT LESBAR: %s' % (p, type(e).__name__))" "$GRENZE" "$D" "$S/APH_1d.csv")
printf '%s\n' "$AD"
WB=$(printf '%s\n' "$AD" | awk -F'\t' '$1=="WERT" && $2=="blob" {print $3}')
VOR=$(printf '%s\n' "$AD" | awk -F'\t' '$1=="WERT" && $2=="vor_grenze" {print $3}')
echo "## MANIFEST"
$PY -B -c "import json,sys
try:
    m=json.load(open(sys.argv[1], encoding='utf-8')); e=m['dateien']['APH_1d.csv']
    print('MANIFEST', e['sha256'], e['bytes'], m['zeitpunkt_utc'], m['quelle'])
except Exception as f:
    print('MANIFEST NICHT LESBAR: %s' % type(f).__name__)" "$S/MANIFEST.json"
echo "## Zeile 2026-09-01 am Stand $B (nur Spaltennamen)"
$G show "$B:$D" | $PY -B "$ZP" 2026-09-01; RI=${PIPESTATUS[1]}; echo "rc $RI"
echo "## Zeile 2026-09-01 in der Arbeitsdatei"
if [ -s "$D" ]; then $PY -B "$ZP" 2026-09-01 < "$D"; echo "rc $?"; else echo "NICHT MESSBAR: $D fehlt oder ist leer"; fi
echo "## Teile"
case "$RI" in 0) I=ja;; 1) I=nein;; *) I="nicht messbar";; esac
if [ "$BB" = fehlt ] || [ -z "$WB" ]; then II="nicht messbar"
elif [ "$WB" = "$BB" ] && [ -z "$NACH" ]; then II=ja
else II=nein; fi
case "$VOR" in ja|nein) III=$VOR;; *) III="nicht messbar";; esac
echo "TEIL (i) $I · (ii) $II · (iii) $III"
echo "## Ende"
case "$RI" in 0|1) exit "$RI";; *) exit 2;; esac
```

`v6_bestand.sh` ruft git nur lesend auf (`rev-parse`, `log`, `show`, je mit `--no-optional-locks`). Die Option `--no-optional-locks` (auch in `z2_tb47.sh` und in `suche.py`) ist vom Werkzeug abhängig; kennt die git-Fassung des Macs die Option nicht, lässt die Sitzung sie weg und beschreibt es im Ergebnis. Ebenso das Format `%cI` der drei `log`-Aufrufe: vom Werkzeug abhängig; kennt die git-Fassung des Macs es nicht, nimmt die Sitzung `%ci` und beschreibt es im Ergebnis. Den Blob der Arbeitsdatei rechnet es selbst — sha1 über `blob <Bytes>`, ein Nullbyte und den Inhalt —, statt `git hash-object` aufzurufen. *Grund:* So hängt die Messung an keiner Erwartung, was `git hash-object` in welcher Fassung schreibt. Dass diese Rechnung den Blob trifft, den git führt, ist am 07.10.2026 in der Linux-VM an `data/APH_1d.csv` geprobt (gleich `847a599c4d065f662dc1b096bf1618c69c81c719`); am Mac zeigt es die Messung selbst: die Zeile `ARBEITSDATEI` gegen die Zeilen unter „Blobs in git“. Die Rückgabe von `v6_bestand.sh` ist die von `v6_zeile.py` am Stand `0779453`, also Teil (i); die Teile (ii) und (iii) stehen in der Zeile `TEIL`.

**Urteil V6**, drei Teile:

| | Frage | Vergleichswert (Helfer, 07.10.2026) |
|---|---|---|
| (i) | Führt der Stand `0779453` in `data/APH_1d.csv` genau eine Zeile 2026-09-01, in der `close` fehlt? | ja; leer `open`, `high`, `low`, `close` |
| (ii) | Trägt die Arbeitsdatei `data/APH_1d.csv` heute denselben Blob wie am Stand `0779453`, und nennt `git log 0779453..HEAD -- data/APH_1d.csv` keinen Commit? | Blob `847a599c4d065f662dc1b096bf1618c69c81c719`; kein Commit nach dem Stand. Der einzige Commit an der Datei überhaupt ist `0f6491b` vom 2026-09-02T23:12:10+02:00 |
| (iii) | Liegt die Änderungszeit der Arbeitsdatei vor dem 02.10.2026, 00:00 Uhr (+02:00; das ist 2026-10-01T22:00:00 UTC)? | 2026-09-02 04:21:29 UTC |

**Wozu (ii) und (iii):** Der Stand `0779453` ist der Commit vom 02.10.2026, an dem die Helfer massen (N3); gelesen haben sie die Datei im Arbeitsbaum. (ii) zeigt, dass der Arbeitsbaum heute den committeten Inhalt trägt und dass seit dem Stand kein Commit die Datei geändert hat; (iii) zeigt, dass die Datei im Arbeitsbaum seit vor dem 02.10.2026 nicht mehr geschrieben wurde. Zusammen heisst das: Am 02.10.2026 lag im Arbeitsbaum dieser Inhalt.

Die Zeile `TEIL (i) … · (ii) … · (iii) …` in `v6.txt` gibt die drei Antworten. Das Urteil ist eines aus der Tabelle „Urteile je Teilfrage“; die Fälle, vollständig:

| (i) | (ii) und (iii) | Urteil |
|---|---|---|
| ja (rc 0) | beide ja | *erfüllt* |
| ja (rc 0) | eines oder beide „nein“ oder „nicht messbar“ | *Zwischenurteil „erfüllt für den committeten Stand; für den Arbeitsbaum vom 02.10.2026 nicht belegt“*, mit dem Teil, an dem es liegt |
| nein (rc 1) | gleich welche | *nicht erfüllt* (dann „traf der Satz“, R79 (g)); die Ausgabe sagt, ob `close` vorhanden ist oder ob es die Zeile nicht genau einmal gibt |
| nicht messbar (rc 2) | gleich welche | *nicht messbar*: Der Stand `0779453` ist unbekannt, die Datei fehlt an diesem Stand oder ist leer, die Kopfzeile trägt kein `open_time` oder kein `close`, oder in der Ausgabe steht ein Traceback |

Was offen bleibt, steht im Ergebnis: Ein zurückgesetzter Zeitstempel ist nicht messbar. Dazu als Tatsache ohne Urteil: ob Blob und sha256 der Snapshot-Datei gleich sind (Register 18, Z. 3072 und Z. 3073: „Die Inhalte sind identisch mit `data/`“).

### Z1 — `close` je Tagesreihe des Snapshots, Aktien und Krypto getrennt (Beleg zu R79 (c))

Zusatzmessung des steuernden Chats, keine Klammer des Verfahrensprüfers. *Grund:* R79 (c) sagt „in den 24 Krypto-Tagesreihen in keiner“; das Ergebnis des Vorgängers führt den Krypto-Teil als nicht gemessen (dort Z. 154 und Z. 162), die Zahl kam aus einer Zählung des steuernden Chats, die im Repo keinen Beleg hat. Z1 legt den Beleg ins Repo.

`docs/belege/TB-140/z1_close_je_datei.py` liest jede `*_1d.csv` unter `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/` als Text und druckt je Datei **eine Zeile** `DATEI`: Markt, Dateiname, Zeilen, Zeilen ohne `close` (davon leer, Fehlwert-Text, Spalte fehlt), Datum der letzten Zeile, Datum der letzten Zeile mit `close`. Die Zuordnung zu Aktien und Krypto kommt aus den zwei Universumsdateien unter `config/`, gelesen wie im Vorgänger (`docs/belege/TB-138/verfahrensmessung_snapshot.py` Z. 134 bis Z. 137); „`close` fehlt“ nach L5 (Auftrag des Vorgängers, Z. 84), gerechnet wie in seinem Messskript (`docs/belege/TB-138/verfahrensmessung_snapshot.py` Z. 62 bis Z. 73). Kein Kurs wird ausgegeben oder in eine Zahl gewandelt. `_1h`- und `_4h`-Reihen liest Z1 nicht. *Grund:* Der Satz aus R79 (c) spricht nur von Tagesreihen, und eine Kursdatei, die nicht gelesen wird, kann in keine Ausgabe geraten (Sichtschutz, Register 27.1). Aufruf aus der Repo-Wurzel:

```
trading-env/bin/python3 -B docs/belege/TB-140/z1_close_je_datei.py > docs/belege/TB-140/z1.txt 2>&1; echo "rc $?" >> docs/belege/TB-140/z1.txt
```

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```python
#!/usr/bin/env python3
"""TB-140 Z1 - je Tagesreihe (*_1d.csv) des Snapshots: Zeilen, Zeilen ohne close,
Datum der letzten Zeile, Datum der letzten Zeile mit close; getrennt nach Aktien und Krypto.
Liest die Dateien als Text; kein Kurs wird ausgegeben oder in eine Zahl gewandelt.
Rueckgabe: 0 wie der Satz aus R79 (c), 1 anders, 2 nicht messbar (Ordner oder Universumsdatei
fehlt, eine Tagesreihe ist leer oder nicht lesbar, oder eine Ausnahme)."""
import argparse
import csv
import datetime as dt
import os
import sys
import traceback

SNAPSHOT = "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
AKTIEN_DATEI = "sp500_top150.txt"      # docs/belege/TB-138/verfahrensmessung_snapshot.py Z. 37
KRYPTO_DATEI = "top25_symbols.txt"     # ebd. Z. 38
SATZ_AKTIEN = [("APH_1d.csv", "2026-09-01")]   # R79 (c): "in genau dieser Zeile"
SATZ_KRYPTO_REIHEN = 24                         # R79 (c): "in den 24 Krypto-Tagesreihen in keiner"
MAX_FAELLE_JE_DATEI = 50

# L5 des Vorgaengers: leer oder ein Text, den pandas.read_csv als Fehlwert liest.
# Die Liste der Umgebung gilt; diese hier ist nur der Rueckfall (Vorgaenger Z. 62-64).
_NA_RUECKFALL = {"", "#N/A", "#N/A N/A", "#NA", "-1.#IND", "-1.#QNAN", "-NaN",
                 "-nan", "1.#IND", "1.#QNAN", "<NA>", "N/A", "NA", "NULL",
                 "NaN", "None", "n/a", "nan", "null"}


def na_texte():
    """Wie der Vorgaenger (Z. 67-73)."""
    try:
        from pandas._libs.parsers import STR_NA_VALUES
        return set(STR_NA_VALUES), "pandas._libs.parsers.STR_NA_VALUES"
    except Exception as e:  # noqa: BLE001
        return set(_NA_RUECKFALL), "Rueckfall im Skript (%s)" % type(e).__name__


def universum(snapshot, datei):
    """Wie der Vorgaenger (Z. 134-137)."""
    with open(os.path.join(snapshot, "config", datei), encoding="utf-8") as f:
        return [z.strip() for z in f if z.strip() and "#" not in z]


def lies(pfad, na):
    """Zaehlt eine Tagesreihe. Rueckgabe dict oder Text mit dem Grund, warum sie nicht lesbar ist."""
    e = {"zeilen": 0, "leer": 0, "natext": 0, "spalte": 0, "ohne_datum": 0,
         "letzte": "-", "letzte_mit_close": "-", "groesstes": "-", "faelle": []}
    with open(pfad, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        try:
            kopf = next(r)
        except StopIteration:
            return "leer"
        if "open_time" not in kopf or "close" not in kopf:
            return "Kopfzeile ohne open_time/close"
        i_t, i_c = kopf.index("open_time"), kopf.index("close")
        for zeile in r:
            if not zeile:
                continue
            e["zeilen"] += 1
            tag = zeile[i_t][:10] if len(zeile) > i_t else ""
            try:
                dt.date.fromisoformat(tag)
            except ValueError:
                e["ohne_datum"] += 1
                tag = "kein_datum"
            if len(zeile) <= i_c:
                art = "spalte"
            elif zeile[i_c] == "":
                art = "leer"
            elif zeile[i_c] in na:
                art = "natext"
            else:
                art = None
            e["letzte"] = tag
            if tag != "kein_datum" and (e["groesstes"] == "-" or tag > e["groesstes"]):
                e["groesstes"] = tag
            if art is None:
                e["letzte_mit_close"] = tag
            else:
                e[art] += 1
                e["faelle"].append((tag, art))
    return e


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--snapshot", default=SNAPSHOT)
    x = p.parse_args(argv)
    na, na_quelle = na_texte()
    print("# TB-140 Z1")
    print("zeit             %s" % dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    print("sys.executable   %s" % sys.executable)
    print("snapshot         %s" % x.snapshot)
    print("Fehlwert-Texte   %d aus %s" % (len(na), na_quelle))
    if not os.path.isdir(x.snapshot):
        print("NICHT MESSBAR: Ordner fehlt")
        return 2
    try:
        markt = {s: "aktien" for s in universum(x.snapshot, AKTIEN_DATEI)}
        krypto = universum(x.snapshot, KRYPTO_DATEI)
    except OSError as e:
        print("NICHT MESSBAR: Universumsdatei: %s" % e)
        return 2
    doppelt = sorted(s for s in krypto if s in markt)
    for s in krypto:
        markt.setdefault(s, "krypto")
    dateien = sorted(n for n in os.listdir(x.snapshot) if n.endswith("_1d.csv"))
    print("Universum        aktien %d, krypto %d, in beiden %s" % (
        sum(1 for v in markt.values() if v == "aktien"), len(krypto), doppelt))
    print("Dateien *_1d.csv %d" % len(dateien))
    ohne_reihe = sorted(s for s in markt if s + "_1d.csv" not in dateien)
    print("Symbole ohne _1d-Reihe: %d %s" % (len(ohne_reihe), ohne_reihe))
    if not dateien:
        print("NICHT MESSBAR: keine Datei *_1d.csv")
        return 2

    print("\nDATEI\tmarkt\tdatei\tzeilen\tohne_close\tleer\tfehlwert_text\tspalte_fehlt\tletzte_zeile\tletzte_zeile_mit_close")
    summe, enden, faelle, unlesbar, hinweise = {}, {}, [], [], []
    for n in dateien:
        m = markt.get(n[:-len("_1d.csv")], "ohne_zuordnung")
        try:
            e = lies(os.path.join(x.snapshot, n), na)
        except Exception as f:  # noqa: BLE001
            e = type(f).__name__
        if isinstance(e, str):
            unlesbar.append((n, e))
            print("DATEI\t%s\t%s\tNICHT LESBAR: %s" % (m, n, e))
            continue
        ohne = e["leer"] + e["natext"] + e["spalte"]
        print("DATEI\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%s\t%s" % (
            m, n, e["zeilen"], ohne, e["leer"], e["natext"], e["spalte"], e["letzte"], e["letzte_mit_close"]))
        s = summe.setdefault(m, {"dateien": 0, "zeilen": 0, "ohne": 0})
        s["dateien"] += 1
        s["zeilen"] += e["zeilen"]
        s["ohne"] += ohne
        for art, tag in (("letzte_zeile", e["letzte"]), ("letzte_zeile_mit_close", e["letzte_mit_close"])):
            enden[(m, art, tag)] = enden.get((m, art, tag), 0) + 1
        faelle += [(m, n, tag, art) for tag, art in e["faelle"][:MAX_FAELLE_JE_DATEI]]
        if len(e["faelle"]) > MAX_FAELLE_JE_DATEI:
            hinweise.append("%s: %d weitere Zeilen ohne close nicht einzeln gedruckt" % (n, len(e["faelle"]) - MAX_FAELLE_JE_DATEI))
        if e["ohne_datum"]:
            hinweise.append("%s: %d Zeilen ohne lesbares Datum" % (n, e["ohne_datum"]))
        if e["letzte"] != e["groesstes"]:
            hinweise.append("%s: letzte Zeile %s, groesstes Datum %s" % (n, e["letzte"], e["groesstes"]))

    print("\nEinzelfaelle (Zeile ohne close)")
    for m, n, tag, art in faelle:
        print("FALL\tz1\t%s\t%s\t%s\t%s" % (m, n, tag, art))
    print("Einzelfaelle gedruckt: %d" % len(faelle))
    print("\nSummen je Markt")
    for m in sorted(summe):
        s = summe[m]
        print("SUMME\t%s\tdateien %d\tzeilen %d\tohne_close %d" % (m, s["dateien"], s["zeilen"], s["ohne"]))
    for (m, art, tag), anz in sorted(enden.items()):
        print("ENDE\t%s\t%s\t%s\t%d" % (m, art, tag, anz))
    print("\nHinweise: %d" % len(hinweise))
    for h in hinweise:
        print("HINWEIS\t%s" % h)
    if unlesbar:
        print("\nNICHT MESSBAR: %d Datei(en) nicht lesbar" % len(unlesbar))
        return 2

    ist_aktien = sorted((n, tag) for m, n, tag, _ in faelle if m == "aktien")
    krypto_ohne = summe.get("krypto", {"ohne": 0})["ohne"]
    krypto_reihen = summe.get("krypto", {"dateien": 0})["dateien"]
    fremd_ohne = summe.get("ohne_zuordnung", {"ohne": 0})["ohne"]
    aktien_wie = ist_aktien == sorted(SATZ_AKTIEN) and summe.get("aktien", {"ohne": 0})["ohne"] == len(SATZ_AKTIEN)
    print("\nSATZ R79 (c), Aktien: close fehlt in genau %s -> %s" % (SATZ_AKTIEN, "trifft zu" if aktien_wie else "TRIFFT NICHT ZU"))
    krypto_wie = krypto_ohne == 0 and krypto_reihen == SATZ_KRYPTO_REIHEN
    print("SATZ R79 (c), Krypto: close fehlt in keiner der %d Reihen -> %s (Zeilen ohne close: %d, Reihen: %d)" % (
        SATZ_KRYPTO_REIHEN, "trifft zu" if krypto_wie else "TRIFFT NICHT ZU", krypto_ohne, krypto_reihen))
    print("Dateien ohne Zuordnung: %d, darin Zeilen ohne close: %d" % (
        summe.get("ohne_zuordnung", {"dateien": 0})["dateien"], fremd_ohne))
    wie = aktien_wie and krypto_wie
    print("RUECKGABE %d" % (0 if wie else 1))
    return 0 if wie else 1


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
```

**Gegenprobe vor der Messung** mit `docs/belege/TB-140/z1_gegenprobe.sh` ⇒ `z1_gegenprobe.txt` (mit angehängtem `rc`): in einem frischen Ordner unter `$TMPDIR` ein erster Ordner mit einer Aktien-Reihe, deren letzte Zeile kein `close` führt, und einer Krypto-Reihe mit einer leeren `close`-Zelle und einer mit dem Text `NaN`, und ein zweiter Ordner mit einer leeren Tagesreihe; die Kursspalten tragen den Text `x`. Die Ordner bleiben in `$TMPDIR`.

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```bash
#!/bin/bash
# TB-140 Z1 - Gegenprobe an zwei kleinen Ordnern in einem frischen Ordner unter $TMPDIR (dorthin
# schreibt das Skript). Die Kursspalten tragen den Text x. Der zweite Ordner traegt eine leere Tagesreihe.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-140/z1_gegenprobe.sh
# Rueckgabe: 0 die Probe beisst (alle Sollzeilen da), 1 eine Sollzeile fehlt, 2 nicht messbar.
set -u
PY="${PY:-trading-env/bin/python3}"
Z="${Z:-docs/belege/TB-140/z1_close_je_datei.py}"
T="$(mktemp -d "${TMPDIR:-/tmp}/tb140_z1_gegenprobe.XXXXXX")" || { echo "NICHT MESSBAR: kein Ordner unter TMPDIR"; exit 2; }
G="$T/eins"; L="$T/leer"
mkdir -p "$G/config" "$L/config"
printf 'AAA\n' > "$G/config/sp500_top150.txt"
printf 'BBBUSDT\nCCCUSDT\n' > "$G/config/top25_symbols.txt"
cat > "$G/AAA_1d.csv" <<'CSV'
open_time,open,high,low,close,volume
2026-08-28,x,x,x,x,x
2026-08-31,x,x,x,x,x
2026-09-01,,,,,x
CSV
cat > "$G/BBBUSDT_1d.csv" <<'CSV'
open_time,open,high,low,close,volume
2026-09-11,x,x,x,x,x
2026-09-12,x,x,x,,x
2026-09-13,x,x,x,NaN,x
2026-09-14,x,x,x,x,x
CSV
cp "$G/config/sp500_top150.txt" "$G/config/top25_symbols.txt" "$L/config/"; : > "$L/AAA_1d.csv"
echo "# TB-140 Z1 GEGENPROBE"; echo "Ordner $T"
echo "## erster Ordner (Soll rc 1)"
$PY -B "$Z" --snapshot "$G" > "$T/a.txt" 2>&1; RC1=$?; cat "$T/a.txt"; echo "rc $RC1"
echo "## zweiter Ordner, leere Tagesreihe (Soll rc 2)"
$PY -B "$Z" --snapshot "$L" > "$T/b.txt" 2>&1; RC2=$?; cat "$T/b.txt"; echo "rc $RC2"
zahl() { awk -F'\t' "$1" "$2" | wc -l | tr -d ' '; }
S1=$(zahl '$1=="DATEI" && $2=="aktien" && $3=="AAA_1d.csv" && $4==3 && $5==1 && $9=="2026-09-01" && $10=="2026-08-31"' "$T/a.txt")
S2=$(zahl '$1=="DATEI" && $2=="krypto" && $3=="BBBUSDT_1d.csv" && $4==4 && $5==2 && $6==1 && $7==1' "$T/a.txt")
S3=$(zahl '$1=="FALL" && $2=="z1"' "$T/a.txt")
S4=$(grep -c "TRIFFT NICHT ZU" "$T/a.txt")
S5=$(grep -c "Symbole ohne _1d-Reihe: 1 \['CCCUSDT'\]" "$T/a.txt")
S6=$(grep -c "NICHT LESBAR: leer" "$T/b.txt")
echo "## Soll"
echo "erster Ordner: rc $RC1 (Soll 1) · DATEI aktien AAA $S1 (Soll 1) · DATEI krypto BBBUSDT $S2 (Soll 1) · FALL $S3 (Soll 3) · TRIFFT NICHT ZU $S4 (Soll 2) · Symbole ohne _1d-Reihe CCCUSDT $S5 (Soll 1)"
echo "zweiter Ordner: rc $RC2 (Soll 2) · NICHT LESBAR: leer $S6 (Soll 1)"
if [ "$RC1" = 1 ] && [ "$RC2" = 2 ] && [ "$S1$S2$S3$S4$S5$S6" = "113211" ]; then echo "GEGENPROBE: beisst"; echo "## Ende"; exit 0; fi
if [ "$RC1" = 2 ]; then echo "GEGENPROBE: NICHT MESSBAR"; echo "## Ende"; exit 2; fi
echo "GEGENPROBE: beisst NICHT"; echo "## Ende"; exit 1
```

**Soll der Gegenprobe:** rc 0 und die Zeile `GEGENPROBE: beisst`. Im Einzelnen am ersten Ordner: rc 1 · `DATEI aktien AAA_1d.csv` mit 3 Zeilen, 1 ohne `close`, letzte Zeile 2026-09-01, letzte Zeile mit `close` 2026-08-31 · `DATEI krypto BBBUSDT_1d.csv` mit 4 Zeilen, 2 ohne `close` (1 leer, 1 Fehlwert-Text) · drei Zeilen `FALL` · `Symbole ohne _1d-Reihe: 1 ['CCCUSDT']` · beide Zeilen `SATZ` mit `TRIFFT NICHT ZU`; am zweiten Ordner: rc 2 und `NICHT LESBAR: leer`. Steht `beisst NICHT` da ⇒ berichtigen und wiederholen; erst danach die Messung. `NaN` zählt als Fehlwert-Text nach der Liste der Umgebung (`pandas._libs.parsers.STR_NA_VALUES`; in `trading-env` am 06.10.2026 lieferbar und mit `NaN`: `docs/belege/TB-138/m1.txt` Z. 117) und ebenso nach dem Rückfall im Skript (`_NA_RUECKFALL`); die Gegenprobe hängt dafür nicht an der Umgebung.

**Soll der Messung:** rc 0; je Datei eine Zeile `DATEI`, keine Zeile `NICHT LESBAR`. **Vergleichswerte, kein Soll:** die zwei Zählungen unter „Belegt“ (174 Dateien; eine Zeile ohne `close`, `APH_1d.csv` 2026-09-01; 150 Dateien enden 2026-09-01, 24 enden 2026-09-14). Weicht eine dieser Zahlen ab ⇒ eigens melden, mit den Zeilen `DATEI`, an denen es liegt.

**Urteil Z1:** *erfüllt* bei rc 0 — dann fehlt `close` in den Aktien-Tagesreihen in genau der Zeile `APH_1d.csv` 2026-09-01 und in den 24 Krypto-Tagesreihen in keiner. *Nicht erfüllt* bei rc 1: jede Zeile `FALL` einzeln, dazu die zwei Zeilen `SATZ`. *Nicht messbar* bei rc 2 oder einem Traceback. Zeilen `HINWEIS` (die letzte Zeile trägt nicht das grösste Datum; eine Zeile ohne lesbares Datum) und Dateien `ohne_zuordnung` werden genannt und gehören nicht zum Urteil. Z1 hängt nicht an V4; welche Fehlwert-Liste galt, steht im Kopf der Ausgabe. **Ein Befund ist kein Abbruch.** Was Z1 nicht sagt: ob eine Zeile ein vollständiger Tag ist, und nichts über Stunden- und Vierstundenreihen.

### Z2 — woher „5.4.0“ im Feld `kalender` stammt (Beleg zu R79 (f))

Zusatzmessung des steuernden Chats, keine Klammer des Verfahrensprüfers. *Grund:* R79 (f) führt die Herkunft des Wertes als Tatsache („stammt nach `docs/ERGEBNIS_TB-47_snapshotgrenze.md` aus der Cloud-Sitzung vom 18.09.2026“); die Anfrage 06.10.a nannte sie „erschlossen“ (K1). Z2 liest nach, was die Datei wörtlich sagt.

**Nur Lesen.** Kein Lauf, nichts wird neu erzeugt: `research/snapshotgrenze/erhebung_eingaben.py` wird hier nicht aufgerufen (im Vorgänger M3 Nr. 2). *Grund:* Z2 fragt, was die Datei vom 18.09.2026 sagt, nicht, was das Skript heute meldet — das hat der Vorgänger gemessen —, und ein Aufruf wäre Code des Repos (Verbot „Kein Lauf“). `eingaben.json` wird nicht geändert. *Grund:* Die Datei ist ein Beleg von TB-47 (Vorgänger Z. 184). Gelesen wird daraus nur das Feld `kalender`. *Grund:* Sie liegt in einem Ordner `ergebnisse/` (Verbot oben, Sichtschutz). `docs/belege/TB-140/z2_tb47.sh` ⇒ `z2.txt`:

```
bash docs/belege/TB-140/z2_tb47.sh > docs/belege/TB-140/z2.txt 2>&1; echo "rc $?" >> docs/belege/TB-140/z2.txt
```

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```bash
#!/bin/bash
# TB-140 Z2 - was docs/ERGEBNIS_TB-47_snapshotgrenze.md zur Herkunft von 5.4.0 sagt. Rein lesend.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-140/z2_tb47.sh
# Rueckgabe: 0 gelesen (das Urteil liest die Sitzung aus der Ausgabe), 2 nicht messbar (die Datei fehlt oder ist leer).
set -u
PY="${PY:-trading-env/bin/python3}"
E=docs/ERGEBNIS_TB-47_snapshotgrenze.md
J=research/snapshotgrenze/ergebnisse/eingaben.json
echo "# TB-140 Z2"; echo "ZEIT $(date '+%Y-%m-%d %H:%M:%S %z')"; echo "HEAD $(git --no-optional-locks rev-parse HEAD)"
if [ ! -s "$E" ]; then echo "NICHT MESSBAR: $E fehlt oder ist leer"; echo "## Ende"; exit 2; fi
echo "## Datei"; echo "Zeilen $(wc -l < "$E" | tr -d ' '), Bytes $(wc -c < "$E" | tr -d ' ')"; shasum -a 256 "$E"
echo "## Feld kalender in $J (nur dieses Feld; die Datei wird nicht geaendert)"
$PY -B -c "import json,sys
try:
    print(json.dumps(json.load(open(sys.argv[1], encoding='utf-8')).get('kalender'), ensure_ascii=False, sort_keys=True))
except Exception as e:
    print('Feld kalender NICHT LESBAR: %s (ohne Einfluss auf die Rueckgabe)' % type(e).__name__)" "$J"
for m in '5\.4\.0' 'cloud' 'eingaben\.json' 'kalender' 'paket_vorhanden' 'nachinstall' 'python'; do
  echo "## Muster $m (ohne Gross/Klein): $(grep -c -i -- "$m" "$E") Zeilen"
  grep -n -i -- "$m" "$E"
done
echo "## Jede Zeile mit 5.4.0 mit drei Zeilen davor und danach"
grep -n -B3 -A3 -- '5\.4\.0' "$E"
echo "## Ende"
exit 0
```

Aus `z2.txt` schreibt die Sitzung `docs/belege/TB-140/z2_stellen.md`: jede Stelle, die sagt, in welcher Sitzung oder Umgebung der Wert entstand, **wörtlich** — Zeilennummer und die ganze Zeile, bei einem Satz über mehrere Zeilen alle seine Zeilen. Keine Deutung, keine Zusammenfassung.

**Vergleichswerte, kein Soll** (Probelauf der Skizze in der Linux-VM, 07.10.2026, mit dem `python3` der VM): Zeilen je Muster `5\.4\.0` 2 (Z. 122, Z. 359) · `cloud` 7 · `eingaben\.json` 2 · `kalender` 9 · `paket_vorhanden` 0 · `nachinstall` 4 · `python` 4; Feld `kalender` mit `paket_vorhanden` gleich `5.4.0`.

**Urteil Z2**, genau eines von dreien oder „nicht messbar“ (Tabelle „Urteile je Teilfrage“; die Abgrenzung der drei ist Lesart des steuernden Chats, vorläufig):

- **„belegt (Wortlaut)“** — eine Stelle der Datei sagt selbst, dass der Wert im Feld `kalender` von `eingaben.json` (oder: die Paketfassung, die die Erhebung dorthin schrieb) in einer benannten Sitzung oder Umgebung entstand. Die Stelle steht mit Zeilennummer da.
- **„nur erschliessbar“** — die Datei nennt 5.4.0 und eine Sitzung oder Umgebung, aber keine Stelle verbindet den Wert mit dem Feld oder mit `eingaben.json`. Die Kette steht da, Schritt für Schritt mit Zeilennummern, und was ihr fehlt.
- **„nicht gefunden“** — keine Stelle nennt 5.4.0 zusammen mit einer Sitzung oder Umgebung.

Fehlt die Datei unter diesem Namen oder ist sie leer (rc 2): „nicht messbar“, und nichts wird unter einem anderen Namen gesucht. *Grund:* R79 (f) nennt die Datei beim Namen; eine andere Datei wäre ein anderer Beleg als der, auf den der Satz sich stützt. Ob der Satz aus R79 (f) so stehen bleiben kann, entscheidet die Sitzung nicht.

### Zwischenstand — sofort nach Z2

Die Sitzung schreibt `docs/belege/TB-140/teil1_zwischenstand.md` (keine Deutung): eine Kopfzeile mit Zeit und ⟨S0⟩, dann je Messung **genau eine Zeile**, in der Reihenfolge V4, V5, V6, Z1, Z2 und in dieser Form:

```
<Kennung> | <Urteil> | <Kernzahl> | <Rohausgabe-Datei>
```

- **Kernzahl:** V4 „W1 ‹n› von 67, W2 ‹n› von 67, Plattform ‹gleich / ungleich›“ · V5 „Tage je Bot ‹vier Zahlen›, Abweichungen ‹n›“ · V6 die Zeile `TEIL (i) … · (ii) … · (iii) …` aus `v6.txt` · Z1 „Aktien ‹n› Reihen, ‹n› Zeilen ohne `close`; Krypto ‹n› Reihen, ‹n› Zeilen ohne `close`“ · Z2 „‹Urteil im Wortlaut›, Stellen Z. ‹…›“.
- **Rohausgabe-Datei:** `docs/belege/TB-140/v4.txt`, `v5.txt`, `v6.txt`, `z1.txt`, `z2.txt`.
- **Zweite Spalte:** das Urteil, das der Abschnitt der Messung vergibt, im Wortlaut der Tabelle „Urteile je Teilfrage“ — bei V4, V5, V6 und Z1 eines der drei Wörter oder das Zwischenurteil des Abschnitts, bei Z2 eines seiner drei Urteile oder „nicht messbar“. Ein Zwischenurteil steht ganz da, nie das blosse Wort „erfüllt“.
- Unter den fünf Zeilen jede Abweichung einzeln, eine Zeile je Fall mit Beleg und Zeile; gibt es keine, die Zeile `Abweichungen: keine`. Ein Treffer der Platzhaltersuche aus 0a steht hier als eigene Zeile, mit Zeilennummer.

Commit `TB-140 Teil 1: V4, V5, V6, Z1, Z2` (mit den Belegen aus 0a und 0b), **pushen**. Der Commit heisst **⟨T1⟩**. Danach gibt die Sitzung **genau eine Zeile** im Terminal aus, wörtlich in dieser Form:

```
TB-140 Teil 1 gepusht <Kurz-Hash ⟨T1⟩>: V4 <Urteil> · V5 <Urteil> · V6 <Urteil> · Z1 <Urteil> · Z2 <Urteil> · docs/belege/TB-140/teil1_zwischenstand.md
```

Die Sitzung **wartet nicht** auf eine Antwort: Sie fährt sofort mit Teil 2 fort. Der steuernde Chat liest den Stand am gepushten Commit und fasst im Arbeitsbaum nichts an.

## Teil 2 — V1, V2, V3: Lesen des Codes

**Nur lesen**, mit `grep -n`, `sed -n`, einem Editor im Lesemodus oder kleinen Lese-Skripten (`trading-env/bin/python3 -B`, die Quelltext als Text einlesen). Kein Import, kein Aufruf. Gelesen wird der Stand ⟨T1⟩.

**Form der Belege** — gilt für alle drei:

1. **Fundstellenliste** `docs/belege/TB-140/fundstellen.tsv`, eine Zeile je Fundstelle, fünf Spalten, getrennt durch **Tabulator** (Codezeilen tragen Kommas): `kennung`, `datei`, `zeile`, `art`, `wortlaut`. `kennung` hat die Form `V1-01`, `V2-17`, `V3-04`. `art` ist `zeile` (der Wortlaut ist die ganze Zeile ohne führende und schliessende Leerzeichen) oder `teil` (nur für Registerzeilen: ein Ausschnitt von höchstens 300 Zeichen, der in der Zeile steht). `wortlaut` ist die letzte Spalte: Der Prüfer teilt jede Zeile höchstens viermal am Tabulator, ein Tabulator im Wortlaut bleibt Teil des Wortlauts.
2. **Prüfung** `docs/belege/TB-140/fundstellen_pruefen.py` ⇒ `fundstellen_pruefung.txt`: liest jede Zeile der Liste, öffnet die Datei und vergleicht den Wortlaut mit der genannten Zeile; druckt je Abweichung `UNGLEICH`, Kennung, Datei und Zeile, am Ende `Fundstellen <n>, ungleich <m>`; rc 1 bei `m > 0`; rc 2, wenn die Liste fehlt oder leer ist, eine Zeile keine fünf Spalten trägt, eine genannte Datei nicht lesbar ist oder eine Ausnahme fällt. Soll: `ungleich 0`, rc 0. Davor eine Gegenprobe ⇒ `docs/belege/TB-140/fundstellen_gegenprobe.txt`: `fundstellen_pruefen.py --liste <Kopie>` an einer Kopie der Liste in `$TMPDIR`, in der in einer Zeile die Zeilennummer um eins verschoben ist (eine Zeile wählen, deren Nachbarzeile anders lautet) und in einer **anderen** Zeile ein Zeichen des Wortlauts geändert ist (Soll: zwei `UNGLEICH`, rc 1).
3. **Tabellen** in `docs/belege/TB-140/v1_spalte.md`, `v2_lader_schnitt.md`, `v3_endlich.md`. Jede Aussage in einer Tabelle nennt ihre Kennungen. Jede Zelle der Spalte **Stand** trägt genau eines der drei Wörter:
   - **belegt** — die Aussage steht in der genannten Codezeile (oder den genannten Zeilen) und braucht keinen Schluss darüber hinaus;
   - **erschlossen** — die Aussage folgt aus mehreren Stellen; die Kette steht da, Schritt für Schritt mit Kennungen;
   - **offen** — am Code nicht entscheidbar; daneben steht, was fehlt (zum Beispiel: „die Stelle läge im Zellen-Erzeuger, den es nicht gibt“).
   **Raten ist verboten.** *Grund:* Eine geratene Zelle sieht im Ergebnis aus wie eine gemessene, und der Verfahrensprüfer entscheidet an diesen Tabellen. Eine Aussage über ein Fehlen („keine Stelle schneidet am Go-Live-Schnitt“) ist nie „belegt“: Sie heisst „erschlossen“ und nennt das Suchmuster, die durchsuchten Dateien und die Trefferzahl.
4. **Suchläufe mit benanntem Bereich.** Der Suchlauf zu jeder Voraussetzung steht als Skript im Belegordner (`v1_suche.sh`, `v2_suche.sh`, `v3_suche.sh`), seine Ausgabe daneben (`*_suche.txt`, mit angehängtem `rc`), damit er wiederholbar ist. Jeder Aufruf darin geht über `docs/belege/TB-140/suche.py` (Skizze unter dieser Liste) und nennt seinen Bereich; die Zeile `BEREICH` der Ausgabe gibt ihn wieder. Durchsucht werden nur von git verfolgte Dateien. **Nie durchsucht** werden `data/`, `snapshots/`, `trading-env/`, `logs/`, `.git/` und jeder Ordner `ergebnisse/` — auch nicht von Hand mit `grep -r`. *Grund:* In `data/` und `snapshots/` trifft ein Muster wie `2026-09` Kurszeilen, und die Ausgabe trüge Kurse (Sichtschutz, Register 27.1); `ergebnisse/` ist oben verboten; `trading-env/` ist fremder Code, `logs/` und `.git/` gehören nicht zum Stand ⟨T1⟩. Die Bereiche:

   | Suche | Bereich | Aufruf |
   |---|---|---|
   | V1 Nr. 0 (gibt es einen Zellen-Erzeuger) und die Aufrufer von `tagesschluss` und `lade_schlusskurse` in V1 Nr. 1 und Nr. 2 | alle verfolgten `*.py` ausserhalb von `docs/` | `--ohne docs` |
   | V1 Nr. 1 und Nr. 2 sonst; V2 (a) und (b) | die verfolgten `*.py` unter `research/vorregistrierung/`, `research/mtm_drawdown/`, `research/exposure_messung/`, `shared/` und `strategies/` („die fünf Ordner“) | fünfmal `--pfad` |
   | V3 Nr. 1 | die eine Datei `docs/VORREGISTRIERUNG_neuselektion.md` | `--pfad docs/VORREGISTRIERUNG_neuselektion.md --endung .md` |
   | V3 Nr. 2 | die eine Datei `research/vorregistrierung/auswertung.py` | `--pfad research/vorregistrierung/auswertung.py` |

   **Keine Kennzahl in einer Suchausgabe.** Kommentare und Docstrings können Kennzahlen tragen (`strategies/elliott_wave_stocks/live_params.py` Z. 6 beginnt mit „GUELTIGE KENNZAHLEN“). `suche.py` druckt deshalb aus Dateien mit dem Namen `live_params.py` nur Datei und Zeilennummer, nie den Text. Breite Muster (`2026-09`, `iloc[-1]`, `tail(`) laufen zuerst mit `--nur-zaehlen`; den Text druckt danach ein zweiter Aufruf nur für die Dateien des Codes des Laufs nach N5. Zeigt eine Ausgabe trotzdem eine Zeile mit einer Kennzahl, Rendite oder Trade-Zahl, wird sie nicht committet: Die Suche läuft mit engerem Bereich oder mit `--nur-zaehlen` noch einmal, und das Ergebnis nennt Datei und Zeile ohne den Wortlaut. *Grund:* Sichtschutz, Register 27.1. Dasselbe gilt für jede Zeile in `fundstellen.tsv`.
5. **Übersicht je Bot** `docs/belege/TB-140/teil2_je_bot.md`, neun Zeilen, aus den Tabellen zu V1 und V2 zusammengezogen (keine neue Aussage, nur Kennungen und die Wörter der Einzeltabellen; die Spalte **Stand** trägt hier je Teilaussage ein Wort, zum Beispiel „Lader belegt · Schnitt offen“):

   | Bot | Lader `Datei:Zeile` | Lader liest: Datei, Spalten | Benchmark und Kern lesen: Datei, Spalte | Zeile ohne `close`: behalten / verwerfen, Codezeile | Wert aus einer Zeile ab dem Go-Live-Schnitt möglich? Einstieg · Ausstieg · Bewertung · Indikatorwert (je ja / nein / offen) | Kennungen | Stand |
   |---|---|---|---|---|---|---|---|

6. **Tabellen gehen per Skript ins Ergebnis, nicht abgetippt.** Jede Tabelle von Teil 2 entsteht als Datei unter `docs/belege/TB-140/`: `teil2_je_bot.md`, `v1_erzeuger.md`, `v1_spalte.md`, `v2_lader_schnitt.md`, `v3_endlich.md`; aus Teil 1 kommt `z2_stellen.md` dazu. Im Ergebnis steht an ihrem Ort zuerst je eine Zeile `[[TABELLE <datei>]]`. `docs/belege/TB-140/ergebnis_tabellen.py --einsetzen` ersetzt jede Marke durch den Inhalt der Datei (mit `assert`: jede Marke genau einmal und in eigener Zeile, sonst wird nichts geschrieben); `--pruefen` vergleicht danach bytegenau ⇒ `docs/belege/TB-140/ergebnis_tabellen.txt` (in D1). Soll: je Tabelle `Vorkommen 1`, `an Zeilengrenzen 1`, keine Kennung, die nicht in `fundstellen.tsv` steht, `GLEICH`; `Marken im Ergebnis: 0`; rc 0. *Grund:* ARBEITSWEISE 0: „Unveränderte Textteile übernimmt ein Skript aus der Quelle, mit `assert` auf die Ankerzeilen; abgetippt wird nichts“.

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```python
#!/usr/bin/env python3
"""TB-140 Teil 2 - Suche in Text mit benanntem Bereich. Durchsucht nur von git verfolgte Dateien,
liest sie als Text, importiert nichts aus dem Repo und schreibt nur nach stdout.
Je Treffer eine Zeile TREFFER: Muster, Datei, Zeilennummer, Text (hoechstens 300 Zeichen). Aus
Dateien namens live_params.py und mit --nur-zaehlen wird kein Text gedruckt (Sichtschutz 27.1).
Aufruf aus der Repo-Wurzel. Rueckgabe: 0 gesucht (auch bei 0 Treffern), 2 nicht messbar
(keine Datei im Bereich, git liefert keine Liste, oder eine Ausnahme)."""
import argparse
import re
import subprocess
import sys
import traceback

NIE = ("data/", "snapshots/", "trading-env/", "logs/", ".git/")   # nie durchsucht, auch wenn --pfad sie nennt
NIE_ORDNER = "ergebnisse"                                           # Sichtschutz, Register 27.1
OHNE_TEXT = ("live_params.py",)                                     # Kommentare dort tragen Kennzahlen
MAX_ZEICHEN = 300


def dateien(pfade, endungen, ohne):
    aus = subprocess.run(["git", "--no-optional-locks", "ls-files", "-z"],
                         stdout=subprocess.PIPE, check=True).stdout.decode("utf-8")
    liste = []
    for p in aus.split("\0"):
        if not p or not p.endswith(tuple(endungen)):
            continue
        if p.startswith(NIE) or NIE_ORDNER in p.split("/")[:-1]:
            continue
        if any(p == q or p.startswith(q.rstrip("/") + "/") for q in ohne):
            continue
        if pfade and not any(p == q or p.startswith(q.rstrip("/") + "/") for q in pfade):
            continue
        liste.append(p)
    return sorted(liste)


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--name", required=True, help="Kennung der Suche, zum Beispiel V1-A")
    a.add_argument("--pfad", action="append", default=[], help="Datei oder Ordner; ohne Angabe: alle verfolgten Dateien")
    a.add_argument("--endung", action="append", default=[], help="Vorgabe .py")
    a.add_argument("--ohne", action="append", default=[], help="Ordner, der im Bereich fehlt")
    a.add_argument("--muster", action="append", required=True)
    a.add_argument("--regex", action="store_true", help="Muster sind regulaere Ausdruecke, sonst feste Zeichenketten")
    a.add_argument("--ohne-gross-klein", action="store_true")
    a.add_argument("--nur-zaehlen", action="store_true", help="je Treffer nur Datei und Zeile, kein Text")
    x = a.parse_args(argv)
    endungen = x.endung or [".py"]
    liste = dateien(x.pfad, endungen, x.ohne)
    print("# TB-140 Suche %s" % x.name)
    print("BEREICH\tverfolgte Dateien, pfad %s, endung %s, ohne %s; nie %s und Ordner %s/" % (
        x.pfad or "alle", endungen, x.ohne or "nichts", list(NIE), NIE_ORDNER))
    print("DATEIEN\t%d" % len(liste))
    if not liste:
        print("NICHT MESSBAR: keine Datei im Bereich")
        return 2
    flags = re.IGNORECASE if x.ohne_gross_klein else 0
    muster = [(m, re.compile(m if x.regex else re.escape(m), flags)) for m in x.muster]
    treffer = {m: 0 for m, _ in muster}
    in_dateien = {m: set() for m, _ in muster}
    for p in liste:
        with open(p, encoding="utf-8", errors="replace") as f:
            for nr, zeile in enumerate(f, 1):
                text = zeile.strip()
                for m, r in muster:
                    for t in r.finditer(text):
                        treffer[m] += 1
                        in_dateien[m].add(p)
                        if x.nur_zaehlen or p.split("/")[-1] in OHNE_TEXT:
                            print("TREFFER\t%s\t%s\t%d\t(Text nicht gedruckt)" % (m, p, nr))
                            continue
                        von = max(0, min(t.start() - 100, len(text) - MAX_ZEICHEN))
                        print("TREFFER\t%s\t%s\t%d\t%s" % (m, p, nr, text[von:von + MAX_ZEICHEN].replace("\t", " ")))
    for m, _ in muster:
        print("MUSTER\t%s\tTreffer %d\tDateien %d" % (m, treffer[m], len(in_dateien[m])))
    print("RUECKGABE 0")
    return 0


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
```

Probelauf dieser Skizze (Helfer, 07.10.2026, Linux-VM, am HEAD `8d172c0`), Vergleichswerte und kein Soll: Der Bereich „alle verfolgten `*.py` ausserhalb von `docs/`“ hat 482 Dateien, der Bereich der fünf Ordner 249.

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```python
#!/usr/bin/env python3
"""TB-140 D1 - die Tabellen aus dem Belegordner gehen per Skript ins Ergebnis, nicht abgetippt.

  --einsetzen  ersetzt im Ergebnis jede Zeile `[[TABELLE <datei>]]` durch den Inhalt der Datei
               aus docs/belege/TB-140/ (jede Marke genau einmal, in eigener Zeile; sonst nichts geschrieben)
  --pruefen    Bytevergleich: jede Tabelle steht im Ergebnis genau einmal und an Zeilengrenzen,
               keine Marke steht mehr da, und jede Kennung der Tabellen (V1-01, V2-17, ...) steht
               in fundstellen.tsv; schreibt nichts

Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 -B docs/belege/TB-140/ergebnis_tabellen.py --einsetzen
  trading-env/bin/python3 -B docs/belege/TB-140/ergebnis_tabellen.py --pruefen > docs/belege/TB-140/ergebnis_tabellen.txt 2>&1; echo "rc $?" >> docs/belege/TB-140/ergebnis_tabellen.txt
Rueckgabe: 0 eingesetzt oder alles gleich, 1 Abweichung, 2 nicht messbar (eine Datei fehlt oder
ist leer, eine Marke steht nicht genau einmal da, oder eine Ausnahme)."""
import argparse
import os
import re
import sys
import traceback

BELEGE = "docs/belege/TB-140"
ERGEBNIS = "docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md"
TABELLEN = ("z2_stellen.md", "teil2_je_bot.md", "v1_erzeuger.md", "v1_spalte.md",
            "v2_lader_schnitt.md", "v3_endlich.md")
FUNDSTELLEN = "fundstellen.tsv"
RE_KENNUNG = re.compile(rb"\bV[123]-\d{2,}\b")


def lies(pfad):
    with open(pfad, "rb") as f:
        return f.read()


def marke(name):
    return b"[[TABELLE " + name.encode("utf-8") + b"]]"


def main(argv=None):
    a = argparse.ArgumentParser()
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument("--einsetzen", action="store_true")
    g.add_argument("--pruefen", action="store_true")
    x = a.parse_args(argv)
    pfade = [os.path.join(BELEGE, n) for n in TABELLEN] + [ERGEBNIS, os.path.join(BELEGE, FUNDSTELLEN)]
    for p in pfade:
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            print("NICHT MESSBAR: %s fehlt oder ist leer" % p)
            return 2
    tab = {n: lies(os.path.join(BELEGE, n)).rstrip(b"\n") for n in TABELLEN}
    erg = lies(ERGEBNIS)
    if x.einsetzen:
        for n in TABELLEN:
            assert erg.count(marke(n)) == 1 and erg.count(b"\n" + marke(n) + b"\n") == 1, (
                "Marke fuer %s steht nicht genau einmal in eigener Zeile" % n)
        for n in TABELLEN:
            erg = erg.replace(marke(n), tab[n])
        assert b"[[TABELLE " not in erg, "eine Marke blieb stehen"
        with open(ERGEBNIS, "wb") as f:
            f.write(erg)
        print("eingesetzt: %d Tabellen in %s" % (len(TABELLEN), ERGEBNIS))
        return 0
    bekannt = {z.split(b"\t", 1)[0] for z in lies(os.path.join(BELEGE, FUNDSTELLEN)).split(b"\n") if z}
    print("# TB-140 D1 - Tabellen im Ergebnis (ergebnis_tabellen.py --pruefen)")
    alle_gut = True
    for n in TABELLEN:
        gesamt = erg.count(tab[n])
        grenzen = (b"\n" + erg).count(b"\n" + tab[n] + b"\n")
        kenn = set(RE_KENNUNG.findall(tab[n]))
        fehlt = sorted(k.decode() for k in kenn - bekannt)
        gut = gesamt == 1 and grenzen == 1 and not fehlt
        alle_gut = alle_gut and gut
        print("TABELLE\t%s\t%d Bytes\t%d Zeile(n)\tVorkommen %d\tan Zeilengrenzen %d\tKennungen %d, nicht in %s: %d %s\t%s" % (
            n, len(tab[n]), tab[n].count(b"\n") + 1, gesamt, grenzen, len(kenn), FUNDSTELLEN, len(fehlt), fehlt,
            "GLEICH" if gut else "ABWEICHUNG"))
    marken = erg.count(b"[[TABELLE ")
    print("Marken im Ergebnis: %d (Soll 0)" % marken)
    alle_gut = alle_gut and marken == 0
    print("Gesamt: %s" % ("alle Tabellen zeichengleich, je genau einmal" if alle_gut else "ABWEICHUNG"))
    print("RUECKGABE %d" % (0 if alle_gut else 1))
    return 0 if alle_gut else 1


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben); nichts geschrieben")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
```

Geprobt (Helfer, 07.10.2026, Linux-VM, an erfundenen Dateien in einem Ordner ausserhalb des Repos): `--einsetzen` setzt sechs Tabellen ein; `--pruefen` danach: sechsmal `Vorkommen 1`, `an Zeilengrenzen 1`, `GLEICH`, dazu `Marken im Ergebnis: 0`, rc 0. Gegenproben: vor dem Einsetzen `Marken im Ergebnis: 6` und rc 1 · ein Zeichen in einer Tabellendatei geändert ⇒ `Vorkommen 0`, die geänderte Kennung „nicht in fundstellen.tsv“, `ABWEICHUNG`, rc 1 · ein zweites `--einsetzen` ⇒ rc 2, das Ergebnis bleibt bytegleich · eine Tabellendatei fehlt ⇒ rc 2.

Die Zeilenangaben unter „Belegt“ oben sind Einstiegsstellen eines Helfers. Die Sitzung misst jede selbst; ihre Zahl gilt.

### V1 — welche Spalte welcher Reihe aus welchem Ordner Benchmark und Kern lesen (R78 (a))

0. **Gibt es einen Zellen-Erzeuger?** Das wird gemessen, nicht vorausgesetzt. Suche im Bereich „alle verfolgten `*.py` ausserhalb von `docs/`“ nach den Namen der Ausgaben aus R39 (Register Z. 10857) — mindestens `zellen.csv`, `zellenbericht`, `tagesreihen/`, `benchmark_tagesreihen`, `symbole_je_falte`. Je Datei mit Treffer eine Zeile in `docs/belege/TB-140/v1_erzeuger.md`:

   | Datei | Treffer (Kennungen) | was die Datei nach ihrem Docstring ist (Wortlaut, höchstens 300 Zeichen) | liest, schreibt oder nennt sie eine Ausgabe aus R39? Codezeile | woraus schreibt sie (Kursdaten, erfundene Werte, Testdaten)? | Stand |
   |---|---|---|---|---|---|

   Urteil zu Nr. 0, eines von zweien: „kein Zellen-Erzeuger gefunden“ — keine Datei im Bereich schreibt eine Ausgabe aus R39 aus Kursdaten; das ist eine Aussage über ein Fehlen, also „erschlossen“, mit Suchmustern, Bereich, Zahl der Dateien und Trefferzahl. Oder „Kandidat gefunden“ — mit Datei und Codezeile; die Sitzung beschreibt ihn und urteilt nicht, ob er der Erzeuger im Sinn des Registers ist. Vergleichswerte, kein Soll: die Suche unter „Belegt“ (vier Dateien, alle unter `research/vorregistrierung/`; eine davon schreibt `zellen.csv` mit erfundenen Werten).
1. **Benchmark.** In `research/vorregistrierung/benchmark.py`: jede Stelle, die eine Kursdatei öffnet (Suchmuster mindestens `read_csv`, `open(`, `_1d`, `_1h`, `_4h`, `DATA_DIR`), mit **Ordner**, Dateimuster und gelesenen Spalten. Für `tagesschluss`: aus welchem Ordner (der Ausdruck, und woher er kommt, `Datei:Zeile`), welche Datei je Symbol, welche Spalte in die Reihe geht, welcher Parameter die Wahl steuert. Hängt Ordner, Datei oder Spalte am Bot oder an seinem `zeitrahmen` (`registerdaten.py`, `BOTS`: `elliott_wave` 1h, `t3_supertrend` 4h), oder nur am Markt? Wer ruft `tagesschluss` auf, mit welchem Argument (Aufrufer im Bereich „alle verfolgten `*.py` ausserhalb von `docs/`“)?
2. **Kern der MtM-Reihe (N4).** In `research/mtm_drawdown/mtm_kern.py`: woher `schlusskurse` kommt (Parameter, Aufrufer). In `grundlage.py::lade_schlusskurse`: **Ordner** (der Ausdruck, und woher er kommt), Dateimuster, Spalte, Vorgabe von `zeitrahmen`. Jeder Aufrufer von `lade_schlusskurse` im Bereich „alle verfolgten `*.py` ausserhalb von `docs/`“ mit dem Argument, das er übergibt — bekommt ein Bot eine andere Reihe als `_1d`? Daneben, getrennt und als „nicht der Kern nach Register Z. 11493“ gekennzeichnet: `research/exposure_messung/auswertung.py::mtm_reihen`.
3. **Tabelle** `v1_spalte.md`, neun Zeilen, eine je Bot:

   | Bot | Markt, Zeitrahmen (Kennung) | Benchmark: Lesestelle `Datei:Zeile` | Benchmark: Ordner (Ausdruck, Herkunft `Datei:Zeile`) | Benchmark: Datei, Spalte | Kern: Ladestelle `Datei:Zeile` | Kern: Ordner (Ausdruck, Herkunft `Datei:Zeile`) | Kern: Datei, Spalte | Aufrufer und Argument | Stand |
   |---|---|---|---|---|---|---|---|---|---|

4. **Der Weg zum Snapshot — beschreiben, nicht beurteilen.** Die Klammer sagt „seine Tagesreihe im Snapshot“. Aus welchem Ordner eine Lesestelle liest, steht erst im Lauf fest. Die Sitzung beschreibt mit Fundstellen, was Code und Register dazu sagen: welche Stelle den Ordner der Benchmark-Lesestelle im Lauf auf den Snapshot stellt (Zeiger unter „Belegt“: `shared/paths.py`, Register Z. 8932), und ob die Ladestelle des Kerns nach N4 diesen Weg mitgeht oder einen festen Ordner nennt. Findet sie dazu nichts, schreibt sie „nicht gefunden“, mit Suchmuster und Bereich. **Die Sitzung urteilt darüber nicht** — weder, ob der Lauf damit den Snapshot liest, noch, ob eine Datei gleichen Namens in einem anderen Ordner „eine andere Reihe“ im Sinn der Klammer ist (O7). *Grund:* das Verbot „Kein Urteil über das Verfahren“.
5. **Urteil V1**, zwei Teile, nicht zusammengezogen, je eines aus der Tabelle „Urteile je Teilfrage“. (i) Benchmark — „Spalte und Datei wie die Klammer“, wenn `tagesschluss` für alle neun Bots `close` aus `<SYMBOL>_1d.csv` liest; „weicht ab“, mit der Stelle, die eine andere Spalte oder eine Datei anderen Namens liest; „am Code nicht entscheidbar“, mit dem, was fehlt. Daneben, als Tatsache ohne Urteil: der Ordner je Stelle und die Beschreibung aus Nr. 4. Das Wort „erfüllt“ vergibt die Sitzung bei V1 nicht: Die Klammer sagt „im Snapshot“, und über den Ordner urteilt die Sitzung nicht. (ii) Kern — am vorhandenen Kern dieselben drei Urteile mit demselben Zusatz. Für „den Kern, den der Zellen-Erzeuger übernimmt“ heisst es **nicht messbar**, mit O1 als Grund — aber nur, wenn Nr. 0 „kein Zellen-Erzeuger gefunden“ ergibt; bei „Kandidat gefunden“ heisst es stattdessen „am Kandidaten gemessen:“ mit einem der drei Urteile aus (i) — die Sitzung misst dann auch an ihm und sagt es.

### V2 — Zeile ohne `close`, und Werte aus Zeilen ab dem Go-Live-Schnitt (R78 (d))

**(a) Behalten oder verwerfen.** Für die Lader der vier Aktien-Bots und für `benchmark.py`: Was geschieht mit einer Zeile, in der `close` fehlt? Die Codezeile, die filtert (oder die Feststellung, dass keine filtert); die Bedingung im Wortlaut (nur `close`, oder eine von mehreren Spalten — `shared/kursdaten.py::unvollstaendige_maske`); ob gezählt oder gemeldet wird; ob der Filter in jedem Aufrufweg liegt oder umgangen werden kann (jede weitere Stelle, die für diese Bots eine Kursdatei liest, ohne den Lader: `equity_simulation.py`, `indicators.py`, `elliott_wave_counter.py`, `shared/zuteilung.py` und was die Suche im Bereich der fünf Ordner sonst findet). Tabelle in `v2_lader_schnitt.md`:

   | Stelle | Lesestelle `Datei:Zeile` | Filter `Datei:Zeile`, Codezeile | Bedingung (Spalten) | behalten / verwerfen | gezählt, gemeldet? | weitere Lesestellen ohne Filter | Stand |
   |---|---|---|---|---|---|---|---|

   Zeilen: die vier Aktien-Bots, `benchmark.py::tagesschluss`. Darunter, als Auskunft ohne Urteil, die fünf Krypto-Lader und `grundlage.lade_schlusskurse`.

**(b) Der Go-Live-Schnitt.** Für jeden der neun Bots und jede der vier Wertarten der Klammer: Kann ein Wert einer Ausgabe des Laufs (N5) aus einer Zeile mit `open_time` am oder nach dem 2026-09-01 gebildet werden? Tabelle, 36 Zeilen (neun Bots mal vier Arten):

   | Bot | Wertart | Wo begrenzt der Code den Zeitraum? `Datei:Zeile`, Codezeile | Grenze (Konstante, Ende der Datei, Parameter) | Wert aus einer Zeile ab dem Schnitt möglich? ja / nein / offen | Begründung an Codezeilen (Kennungen) | Stand |
   |---|---|---|---|---|---|---|

   Wertarten: **Einstieg** (frühester und spätester Tag, an dem `collect_all_trades` einen Einstieg bilden kann) · **Ausstieg** (auch: der Ausstieg einer Position, die vor dem Schnitt eröffnet wurde; was mit einer Position geschieht, die am Ende der geladenen Daten offen ist — O5) · **Bewertung** (welche Tage die Bewertung am Tagesschluss führt: `mtm_kern.tagesraster` und sein `bis`, `benchmark.tagesgenau`, `bh_tagesrenditen`) · **Indikatorwert** (geht eine Zeile ab dem Schnitt in einen Indikatorwert eines Tages **vor** dem Schnitt ein: Rückwärtsfüllen, `shift` mit negativem Argument, zentrierte Fenster, Kennwerte über die ganze Reihe, eine Wellen- oder Zickzack-Bestätigung durch spätere Kerzen).
   Mindestens zu suchen, im Bereich der fünf Ordner (Suchmuster im Beleg; breite Muster zuerst mit `--nur-zaehlen`): `GO_LIVE`, `go_live`, `2026-09`, `RECENT_YEARS_ONLY`, `bfill`, `backfill`, `shift(-`, `center=True`, `iloc[-1]`, `tail(`, `max()`/`min()` über `open_time`, jede Stelle, die ein Enddatum setzt oder liest. Ein Helfer fand am 07.10.2026 für `go_live` (ohne Rücksicht auf Gross- und Kleinschreibung, auch `go-live`): 0 Treffer in `benchmark.py`, `auswertung.py`, `mtm_kern.py`, `grundlage.py`, `shared/paths.py`, `shared/strategy_paths.py`, `shared/zuteilung.py`, `shared/kursdaten.py` und den neun `multi_symbol_optimise.py` und `equity_simulation.py`; `2026-09`: dort 12 Treffer, zehn in Kommentaren (je Lader ein Kommentar „APH, 2026-09-01“, `elliott_wave_stocks/equity_simulation.py` Z. 59), einer in einem Docstring (`turtle_soup_stocks/equity_simulation.py` Z. 8) und einer in einem Dateinamen (`auswertung.py` Z. 111) — Suchergebnis, kein Urteil; die Sitzung misst nach. Im ganzen Bereich der fünf Ordner (249 Dateien) fand der Probelauf von `suche.py` am 07.10.2026: `go.live` als regulärer Ausdruck ohne Gross und Klein 18 Vorkommen in 13 Zeilen in 5 Dateien (`faltenplan.py`, `registerdaten.py`, `registerbericht.py`, `test_vorregistrierung.py`, `shared/binance_historie.py`), `2026-09` 244 Vorkommen in 195 Zeilen in 47 Dateien, davon 37 Vorkommen in 36 Zeilen in den neun `live_params.py` — Vergleichswerte, kein Soll; gezählt sind Vorkommen (die Zahl hinter `Treffer` in der Zeile `MUSTER`), nicht Zeilen.
   Liegt eine Begrenzung nach Plan erst im Zellen-Erzeuger (Faltenzuordnung, Schnitt der Tagesreihe nach R66 (a)), dann heisst die Zelle **offen** mit genau diesem Grund — nicht „nein“.

**Urteil V2**, je Teil eines aus der Tabelle „Urteile je Teilfrage“: zu (a) je Stelle „behält“, „verwirft“ oder „am Code nicht entscheidbar“ (mit dem, was fehlt), mit Codezeile; kein „erfüllt“, die Klammer fragt nur, welches von beiden. Zu (b) eines von dreien, je Bot und zusammen: „ein solcher Wert wird gebildet“ (jede Stelle einzeln; das ist nach der Klammer zu melden und geht vor dem Tag an den Verfahrensprüfer) · „kein solcher Wert wird gebildet“ (nur, wenn jede der 36 Zeilen „nein“ mit Begründung trägt) · „am vorhandenen Code nicht entscheidbar“ (mit der Liste der offenen Zeilen). **Ein Befund ist kein Abbruch.** Nichts wird am Code geändert.

### V3 — nicht endliche Werte in `zellen.csv` und `zellenbericht.csv` (R78 (e))

1. **Die registrierten Definitionen.** Jedes Feld der zwei Dateien mit der Registerstelle, die es festlegt (Einstieg unter „Belegt“: R39 in Register Z. 10857, dann 50.2, R33, R34, R36 und R68; dazu im Register suchen — Bereich: die eine Datei `docs/VORREGISTRIERUNG_neuselektion.md` — nach `zellen.csv`, `zellenbericht`, jedem Feldnamen, „nicht definiert“, „endlich“ — O4). Registerzeilen sind mehrere Kilobyte lang: nie eine ganz ausgeben, Ausschnitte per Skript, höchstens 300 Zeichen je Treffer. `suche.py` schneidet so. Tabelle in `v3_endlich.md`:

   | Datei | Feld | Registerstelle (Block, Zeile) | Wortlaut der Definition (höchstens 300 Zeichen) | nennt die Definition einen Fall ohne Zahl? (Wortlaut) | nennt sie dafür einen Wert oder ein Wort? (Wortlaut) | Stand |
   |---|---|---|---|---|---|---|

   Die Sitzung stellt die Wortlaute nebeneinander und **deutet nicht**: Ob ein Feld „nach seiner registrierten Definition einen nicht endlichen Wert tragen darf“, entscheidet der Verfahrensprüfer. Wo die Definition eine Division, eine Streuung oder einen Median über eine möglicherweise leere Menge verlangt und zum leeren oder Null-Fall nichts sagt, steht das als Tatsache in der vorletzten Spalte („sagt nichts“).
2. **`auswertung.py`.** Was geschieht mit einem nicht endlichen Wert (N6) in `zellen.csv`? Je Spalte, die `lies_zellen` und seine Verwender lesen (`PFLICHTSPALTEN` und die Stelle, die sie festlegt): Gibt es eine Prüfung, welche der drei Arten (NaN, +inf, −inf) fängt sie, mit welcher Folge (`Abbruch`; welcher Rückgabewert — die Stelle, die ihn setzt)? Tabelle:

   | Spalte | gelesen in `Datei:Zeile` | Prüfung `Datei:Zeile`, Codezeile | fängt NaN / +inf / −inf | Folge, Rückgabewert (Kennung) | Stand |
   |---|---|---|---|---|---|

   Ein Helfer fand am 07.10.2026 in `auswertung.py` 0 Treffer für `isfinite`, `isinf` und `finite` und einen für `isna` (Z. 355, nur `netto_sharpe`, nach dem Setzen auf 0 bei `n_trades == 0`) — Suchergebnis, kein Urteil. Liest `auswertung.py` die Datei `zellenbericht.csv` überhaupt? (Register Z. 11490: „`zellenbericht` 0 Treffer in `auswertung.py`“ — nachmessen.)
3. **Urteil V3**, zwei Teile (Tabelle „Urteile je Teilfrage“): (i) die Tabelle aus Nr. 1, ohne Urteil der Sitzung, mit der Zählung „Felder, Definition nennt einen Fall ohne Zahl, Definition sagt nichts“. (ii) „`auswertung.py` beendet einen nicht endlichen Wert in `zellen.csv` mit 2“: *trifft zu* (für jede Spalte und jede der drei Arten, mit Codezeile) · *trifft teils zu* (für welche Spalten und Arten) · *trifft nicht zu* · *am Code nicht entscheidbar* (mit dem, was zum Entscheid fehlt). Kein Probelauf von `auswertung.py`, auch nicht an Beispieldaten (Verbot oben): Liesse sich die Frage nur mit einem Lauf klären, heisst das Urteil „am Code nicht entscheidbar“.

Commit `TB-140 Teil 2: V1, V2, V3, Fundstellenprüfung`, pushen.

## Schritt N — Backlog- und Journal-Nachtrag (5b)

Dokumentationsauftrag nach ARBEITSWEISE 5b: Der Text steht wörtlich in **diesem Auftrag**, mit Ankertext und der Zieldatei je Einfügung in eigener Zeile; geschrieben wird nur unter `docs/`; `numstat` je Datei ist Soll; nichts wird umformuliert. Findet die Sitzung im Text einen Sachfehler: melden, nicht berichtigen.

**Zwei Texte, nicht vermischt.** E1 und J1 sind der Nachtrag des steuernden Chats zu dem, was zwischen der Abgabe von TB-138 und dem Start dieses Auftrags geschah: Abnahme TB-138, Anfrage und Antwort 06.10.a, Bewertung, Reihenfolge. Sie nennen kein Ergebnis dieses Auftrags, und die Sitzung ändert an ihnen kein Zeichen. Was die Sitzung selbst gemessen hat, schreibt sie selbst in ihren Journalblock (D2); den Nachtrag gibt sie dort nicht noch einmal in eigenen Worten wieder. So hält es der Vorgänger: dort E1 (Z. 192 bis Z. 203) und der letzte Satz von D2 (Z. 213); im Block EG steht der übernommene Wortlaut als eigener Absatz „Abnahme des Vorgängers, wie in `BACKLOG.md` Abschnitt 5 eingetragen“ (`JOURNAL.md` Z. 10064 und Z. 10065), getrennt von „Was gemessen ist“.

**Quellen der fünf Spiegelstriche** (zum Nachlesen, nicht einzufügen): Nr. 1 `UEBERGABE.md`, Umzug 07.10.2026, 06:59, Block 1 und Block 3 · Nr. 2 dieselbe Stelle, Block 3, und die Anfrage selbst (Fragen in Abschnitt 5 und 6, K1 bis K5 in Abschnitt 7) · Nr. 3 die Antwort selbst (Z. 3 „geschrieben am 07.10.2026“; die Blöcke in Z. 151, Z. 154 und Z. 157; die sechs Klammern oben) · Nr. 4 die Bewertung des steuernden Chats vom 07.10.2026, Abschnitt 3, 4 und 7 (im Entwurf des Nachtrags: Abschnitt 3, 4 und 6, dazu Abschnitt 8 Nr. 1) · Nr. 5 dieselbe Bewertung, Abschnitt 6 (im Entwurf des Nachtrags: Abschnitt 7), und `UEBERGABE.md`, Umzug 07.10.2026, 06:59, Block 1, Block 4 Nr. 2 und Block 6. Die Bewertung ist eine Arbeitsunterlage unter `logs/steuernder_chat/` (von git ignoriert); im Blocktext steht dafür der Nachtrag in `UEBERGABE.md`, den der steuernde Chat beim Legen dieses Auftrags schreibt. Der Nachtrag muss für Nr. 4 tragen: dass es die Bewertung gibt · keine Abweichung gegen einen Messwert in einem Block · Abnahme durch einen Helfer, nur lesend · acht Abweichungen und Befunde, die in „Voraussetzungen und Befunde“ gehen · dass zwei davon Aussagen eines Blocks ohne Beleg sind, für die TB-140 Z1 und Z2 misst · die Nachzählung (174 Dateien, eine Zeile ohne `close`, 150 und 24 Reihenenden) · was nicht nachgerechnet und was nicht gemessen ist. Für Nr. 5: TB-140 misst die sechs Voraussetzungen und zwei Belege · TB-140 läuft vor TB-139 · TB-139 trägt genau R78 bis R80 als Abschnitt 55 ein · die Einzelfreigabe steht aus · TB-137 steht aus. Die Sitzung liest das am Nachtrag nach und nennt im Ergebnis je Angabe die Zeile des Nachtrags oder „nicht gefunden“. Findet sie eine Angabe dort nicht, fügt sie trotzdem unverändert ein (*Grund:* 5b, nichts wird umformuliert; der Text ist der des steuernden Chats) und nennt die Angabe im Ergebnis.

**Verfahren für E1** wie Vorgänger, Schritt B (dort Z. 190): Vorlagen `docs/belege/TB-138/einfuegen.py` und `docs/belege/TB-138/c3_vergleich.py`, nach `docs/belege/TB-140/` übernommen und umgestellt (nur: Pfad dieses Auftrags und Belegordner in `einfuegen.py` Z. 21 und Z. 22 und in `c3_vergleich.py` Z. 17 und Z. 18, die Kopfzeile der Ausgabedatei in `einfuegen.py` Z. 120 und `c3_vergleich.py` Z. 43, die Kennung in den zwei Docstrings; `BLOECKE` = `{"E1"}`, erwartete Nummernfolge E1 und erwartete Anzahl 1 bleiben); Aufruf mit `trading-env/bin/python3 -B`, zuerst mit `--probe`. Genau eine Leerzeile vor und nach dem Block; eine vorhandene wird nicht verdoppelt. Ergebnis in `docs/belege/TB-140/einfuegungen.txt`, Zeichengleichheit in `docs/belege/TB-140/c3_vergleich.txt`.

**Warum die Vorlagen J1 nicht anfassen — nach Bauart, nicht nach Reihenfolge.** `einfuegen.py` liest eine Einfügung nur unter einer Überschrift `#### E<n> — ` (Z. 25) und nur mit einer Zeile der Form `Anker: … · Art: …` (Z. 27); J1 trägt keine von beiden. `c3_vergleich.py` teilt den Auftrag an jeder Zeile, die mit `#### E<n> ` oder mit `## ` beginnt (Z. 21), und nimmt aus dem Abschnitt E1 die erste `Zieldatei:`-Zeile und den ersten Codezaun (Z. 29 und Z. 30). J1 steht deshalb unter einer eigenen Überschrift der Ebene `## ` („Schritt N, zweiter Teil“): Der Abschnitt E1 endet davor und trägt genau eine `Zieldatei:`-Zeile und genau einen Codezaun. J1 hat eigene Werkzeuge (`j1_einsetzen.py`, `j1_vergleich.py`). Soll des Probelaufs mit `--probe`: genau eine Einfügung, E1, Zieldatei `docs/projektfuehrung/BACKLOG.md`, 7 Textzeilen.

Vorgezählt von einem Helfer des steuernden Chats am 07.10.2026 am HEAD `8d172c0` (`BACKLOG.md`: 323 Zeilen, 73 765 B, md5 `5721615ef4d59f600018e08d681fc5c8`): Anker 1 (Z. 312 von 323; Z. 311 ist leer), erste Zeile des neuen Texts 0. Die Sitzung zählt selbst nach; ihre Zahl gilt. Anker ≠ 1 ⇒ nicht einfügen, nennen.

**Geprobt** (Helfer, 07.10.2026, Linux-VM, Python 3.10.12): die zwei Vorlagen, umgestellt wie oben, und die zwei J1-Skripte, in einem Ordner ausserhalb des Repos, der die Pfade des Repos nachbildet — mit diesem Auftrag als Quelle und Kopien von `BACKLOG.md` und `JOURNAL.md`, bytegleich mit dem HEAD `8d172c0`. `einfuegen.py --probe`: eine Einfügung, E1, Ankerzeile 312, 7 Textzeilen. Nach dem Einfügen: hinzugefügt 8 Zeilen, entfernt 0. `c3_vergleich.py`: 7 Zeilen, `Vorkommen 1 · an Zeilengrenzen 1 · GLEICH`, Anzahl 1; der Abschnitt E1 trägt eine `Zieldatei:`-Zeile und einen Codezaun (an v2 dieses Auftrags, vor der eigenen Überschrift für J1, waren es je zwei). Gegenprobe: ein Zeichen im eingefügten Block der Kopie geändert ⇒ `Vorkommen 0`, `ABWEICHUNG`. Das weicht von ARBEITSWEISE 0 ab („das Prüfskript läuft vor der Freigabe am echten Repo, nicht nur an einer Kopie (TB-130)“). *Grund:* Der Helfer liest das Repo nur, und vor Schritt 0 legt der steuernde Chat keine weitere Datei in den Arbeitsbaum (ARBEITSWEISE 0; 0a zählt die Einträge).

**Vor dem Einfügen** sucht die Sitzung im Blocktext von E1 und im Blocktext von J1 nach einem stehengebliebenen Platzhalter: zwei Klammeraffen in Folge oder zwei öffnende spitze Klammern in Folge; Soll je 0 Treffer. Für die Klammeraffen gilt dazu die Suche über den ganzen Auftrag aus 0a (sie deckt auch die Stelle unter „Freigabe“ ab); die spitzen Klammern sucht die Sitzung nur in den zwei Blocktexten, weil die Shell-Skizzen dieses Auftrags sie für ihre Hier-Dokumente brauchen. Steht in einem der zwei Blocktexte ein Platzhalter, ist der Text nicht fertig: E1 und J1 entfallen dann beide, das Ergebnis nennt es, und die Sitzung erfindet keinen Ersatz.

#### E1 — BACKLOG, Abschnitt 5: Abnahme TB-138, Fable 06a, Reihenfolge

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile**

```
### Aus der Abnahme TB-138 (06.10.2026) und aus Fable 06a (Antwort vom 07.10.2026) — Bewertung nach 5b, eingetragen mit TB-140

- **TB-138 abgenommen** am 06.10.2026: zehn Prüfungen eines Helfers, drei formale Abweichungen, keine gegen einen Messwert; die Sitzung ist geschlossen. Ins Register ist davon nichts eingetragen (`UEBERGABE.md`, Umzug 07.10.2026, 06:59, Block 1 und Block 3).
- **Anfrage 06.10.a an den Verfahrensprüfer** (`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-06a_verfahrensmessung_snapshot_aph.md`, Eröffnungstext `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-06_eroeffnung.md`): zwei Fragen — (1) ob die Zeile ohne Kurs von `APH` ein „Endet eine Reihe früher“ nach R72 (d) ist und was dann vor dem Tag zu entscheiden ist, von wem; (2) ob die Lesarten L1–L9 gelten und in welcher Form das Ergebnis ins Register kommt. Dazu K1–K5 zur Kenntnis (`UEBERGABE.md`, Umzug 07.10.2026, 06:59, Block 3).
- **Antwort 06.10.a,** geschrieben am 07.10.2026 (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-06a_verfahrensmessung_snapshot_aph.md`, 26 689 B, md5 `2fc513b93ef8b3ecb794a543c9fe5dc3`): drei Blöcke R78–R80. Entscheidung zu `APH` (R78 (d)): Reihenende nach R72 (d); es berührt 3b (c) im Lauf nicht; der Snapshot bleibt. Sechs Voraussetzungen: vor dem Eintrag R79 (a) und R79 (b), vor dem signierten Tag R78 (d), ohne Zeitpunkt R78 (a), R78 (e) und R79 (g).
- **Bewertung des steuernden Chats vom 07.10.2026:** in den Blöcken keine Abweichung gegen einen Messwert (Abnahme durch einen Helfer, nur lesend); acht Abweichungen und Befunde, darunter zwei Aussagen eines Blocks ohne Beleg (dazu Z1 und Z2), sie gehen in „Voraussetzungen und Befunde“ des Registerauftrags; eigene Nachzählung am Snapshot `63e4b6c8…` über 174 Dateien `*_1d.csv`: `close` fehlt in genau einer Zeile (`APH`, 2026-09-01), 150 Dateien enden 2026-09-01, 24 enden 2026-09-14. Nicht nachgerechnet: Kalendervergleich, doppelte `open_time`, Paketfassungen (Ausgabe der Sitzung TB-138). Nicht gemessen: Fables Selbstauskünfte (Ampel, Leseprotokoll-Zahlen); 37.3, 34, 5.2, 2a, 24b A2; `gegenprobe.txt`, `c3_vergleich.txt` der Belege TB-138 (`UEBERGABE.md`, Nachtrag 07.10.2026, 10:32).
- **Reihenfolge:** TB-140 misst die sechs Voraussetzungen und zwei Belege zu R79 (c) und R79 (f), nur lesend, und läuft vor TB-139. TB-139 trägt die Blöcke R78–R80 als Abschnitt 55 ins Register ein; die Einzelfreigabe des Betreibers dafür steht aus. TB-137 steht weiter aus (`UEBERGABE.md`, Umzug 07.10.2026, 06:59, Block 1, Block 4 Nr. 2 und Block 6; Nachtrag 07.10.2026, 10:32).
```

Soll numstat für `docs/projektfuehrung/BACKLOG.md`: `8	0` (7 Zeilen Block und eine Leerzeile danach; vor dem Anker steht schon eine).

Commit `TB-140 N: BACKLOG`, pushen.

## Schritt N, zweiter Teil — J1, der Absatz im Journalblock (gesetzt in D2)

#### J1 — JOURNAL: der Nachtrag im Journalblock der Sitzung

Zieldatei: `docs/projektfuehrung/JOURNAL.md`
Ankertext des Blocks: `\n---\n\n## Wiederkehrende Lehren\n` · Art: **der Block der Sitzung steht davor** (D2). J1 steht **in** diesem Block: nach dem Absatz „**Quelle:**“ und vor `### Was gemessen ist`, mit je einer Leerzeile davor und danach (der Ort des entsprechenden Absatzes im Block EG).

```
**Nachtrag des steuernden Chats zum Stand vor TB-140, wie in `BACKLOG.md` Abschnitt 5 eingetragen:**
- **TB-138 abgenommen** am 06.10.2026: zehn Prüfungen eines Helfers, drei formale Abweichungen, keine gegen einen Messwert; die Sitzung ist geschlossen. Ins Register ist davon nichts eingetragen (`UEBERGABE.md`, Umzug 07.10.2026, 06:59, Block 1 und Block 3).
- **Anfrage 06.10.a an den Verfahrensprüfer** (`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-06a_verfahrensmessung_snapshot_aph.md`, Eröffnungstext `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-06_eroeffnung.md`): zwei Fragen — (1) ob die Zeile ohne Kurs von `APH` ein „Endet eine Reihe früher“ nach R72 (d) ist und was dann vor dem Tag zu entscheiden ist, von wem; (2) ob die Lesarten L1–L9 gelten und in welcher Form das Ergebnis ins Register kommt. Dazu K1–K5 zur Kenntnis (`UEBERGABE.md`, Umzug 07.10.2026, 06:59, Block 3).
- **Antwort 06.10.a,** geschrieben am 07.10.2026 (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-06a_verfahrensmessung_snapshot_aph.md`, 26 689 B, md5 `2fc513b93ef8b3ecb794a543c9fe5dc3`): drei Blöcke R78–R80. Entscheidung zu `APH` (R78 (d)): Reihenende nach R72 (d); es berührt 3b (c) im Lauf nicht; der Snapshot bleibt. Sechs Voraussetzungen: vor dem Eintrag R79 (a) und R79 (b), vor dem signierten Tag R78 (d), ohne Zeitpunkt R78 (a), R78 (e) und R79 (g).
- **Bewertung des steuernden Chats vom 07.10.2026:** in den Blöcken keine Abweichung gegen einen Messwert (Abnahme durch einen Helfer, nur lesend); acht Abweichungen und Befunde, darunter zwei Aussagen eines Blocks ohne Beleg (dazu Z1 und Z2), sie gehen in „Voraussetzungen und Befunde“ des Registerauftrags; eigene Nachzählung am Snapshot `63e4b6c8…` über 174 Dateien `*_1d.csv`: `close` fehlt in genau einer Zeile (`APH`, 2026-09-01), 150 Dateien enden 2026-09-01, 24 enden 2026-09-14. Nicht nachgerechnet: Kalendervergleich, doppelte `open_time`, Paketfassungen (Ausgabe der Sitzung TB-138). Nicht gemessen: Fables Selbstauskünfte (Ampel, Leseprotokoll-Zahlen); 37.3, 34, 5.2, 2a, 24b A2; `gegenprobe.txt`, `c3_vergleich.txt` der Belege TB-138 (`UEBERGABE.md`, Nachtrag 07.10.2026, 10:32).
- **Reihenfolge:** TB-140 misst die sechs Voraussetzungen und zwei Belege zu R79 (c) und R79 (f), nur lesend, und läuft vor TB-139. TB-139 trägt die Blöcke R78–R80 als Abschnitt 55 ins Register ein; die Einzelfreigabe des Betreibers dafür steht aus. TB-137 steht weiter aus (`UEBERGABE.md`, Umzug 07.10.2026, 06:59, Block 1, Block 4 Nr. 2 und Block 6; Nachtrag 07.10.2026, 10:32).
```

Die fünf Spiegelstriche von J1 sind die von E1, Zeichen für Zeichen (das Bauskript dieses Auftrags hat beide aus einer Quelle gesetzt); nur die erste Zeile ist eine andere. `einfuegen.py` setzt J1 nicht: Die Sitzung schreibt ihren Block (D2) und setzt J1 danach mit `docs/belege/TB-140/j1_einsetzen.py` hinein, nicht abgetippt — zuerst mit `--kennung <Kennung> --probe`, dann ohne `--probe` ⇒ `docs/belege/TB-140/j1_einsetzen.txt` (beide Aufrufe ohne Umleitung: das Skript schreibt diese Datei selbst, wenn es einsetzt, und druckt dieselbe Zeile; den rc nennt die Kurz-Tabelle). Das Skript liest J1 aus diesem Auftrag und prüft mit `assert`, bevor es schreibt: der Ankertext steht genau einmal im Journal; die Kopfzeile `## <Kennung> — TB-140` steht genau einmal und vor dem Ankertext, dazwischen kein weiterer Block; im neuen Block stehen genau ein Absatz `**Quelle:**` und genau eine Zeile `### Was gemessen ist`, in dieser Folge; die erste Zeile von J1 steht noch 0-mal im Journal. Trifft eine Bedingung nicht zu, schreibt es nichts und endet mit 2. Lief E1 nicht (Anker ≠ 1 oder ein Platzhalter), setzt die Sitzung auch J1 nicht ein — die erste Zeile von J1 träfe dann nicht zu — und schreibt in ihren Block nur, dass der Nachtrag aussteht und warum.

Vorgezählt vom Helfer am 07.10.2026 am HEAD `8d172c0` (`JOURNAL.md`: 10 433 Zeilen): Der Ankertext steht genau einmal, die Worte „Wiederkehrende Lehren“ stehen in drei Zeilen; der letzte Buchstabenblock ist `## EG — TB-138: …` (Z. 10056), seine Zeile 10090 lautet „- Nächste Journalkennung nach EG: **EH**.“; die erste Zeile von J1 steht 0-mal. Die Kennung misst die Sitzung selbst (erwartet **EH**).

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```python
#!/usr/bin/env python3
"""TB-140 D2 - setzt den Absatz J1 aus dem Auftrag in den Journalblock der Sitzung.

Liest J1 aus dem ersten Codezaun nach der Zeile `#### J1 — ` des Auftrags (nicht aus dem
Gedaechtnis) und setzt ihn im neuen Block vor die Zeile `### Was gemessen ist`, mit genau einer
Leerzeile davor und danach. Geschrieben wird nur docs/projektfuehrung/JOURNAL.md und die
Ausgabedatei. Trifft eine Bedingung nicht zu (assert), wird nichts geschrieben.

Aufruf aus der Repo-Wurzel, nachdem der Block der Sitzung im Journal steht:
  trading-env/bin/python3 -B docs/belege/TB-140/j1_einsetzen.py --kennung EH --probe   (nur lesen)
  trading-env/bin/python3 -B docs/belege/TB-140/j1_einsetzen.py --kennung EH
Rueckgabe: 0 eingesetzt (mit --probe: einsetzbar), 2 nicht eingesetzt."""
import argparse
import sys
import traceback
from pathlib import Path

AUFTRAG = Path("docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md")
JOURNAL = Path("docs/projektfuehrung/JOURNAL.md")
AUSGABE = Path("docs/belege/TB-140/j1_einsetzen.txt")
ANKER = "\n---\n\n## Wiederkehrende Lehren\n"
ZIEL_ZEILE = "### Was gemessen ist"
ERSTE_ZEILE = "**Nachtrag des steuernden Chats zum Stand vor TB-140"


def j1_lesen(text):
    zeilen = text.split("\n")
    kopf = [i for i, z in enumerate(zeilen) if z.startswith("#### J1 — ")]
    assert len(kopf) == 1, "Zeile `#### J1 — ` steht nicht genau einmal im Auftrag: %d" % len(kopf)
    j = kopf[0] + 1
    while zeilen[j] != "```":
        assert not zeilen[j].startswith("#"), "zwischen `#### J1 — ` und dem Codezaun steht eine Ueberschrift"
        j += 1
    k = j + 1
    while zeilen[k] != "```":
        k += 1
    block = zeilen[j + 1:k]
    assert block and block[0].startswith(ERSTE_ZEILE), "die erste Zeile von J1 lautet anders als erwartet"
    assert all(z != "" for z in block), "J1 traegt eine Leerzeile"
    return block


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--kennung", required=True, help="Kennung des neuen Journalblocks, zum Beispiel EH")
    a.add_argument("--probe", action="store_true", help="nur lesen, nichts schreiben")
    x = a.parse_args(argv)
    j1 = j1_lesen(AUFTRAG.read_text(encoding="utf-8"))
    inhalt = JOURNAL.read_text(encoding="utf-8")
    assert inhalt.count(ANKER) == 1, "Ankertext steht nicht genau einmal im Journal: %d" % inhalt.count(ANKER)
    assert inhalt.count(j1[0]) == 0, "die erste Zeile von J1 steht schon im Journal"
    kopfzeile = "\n## %s — TB-140" % x.kennung
    assert inhalt.count(kopfzeile) == 1, "Kopfzeile `## %s — TB-140` steht nicht genau einmal: %d" % (
        x.kennung, inhalt.count(kopfzeile))
    anfang, ende = inhalt.index(kopfzeile) + 1, inhalt.index(ANKER)
    assert anfang < ende, "der neue Block steht nicht vor dem Ankertext"
    block = inhalt[anfang:ende].split("\n")
    assert not [z for z in block[1:] if z.startswith("## ")], "zwischen Kopfzeile und Ankertext steht ein weiterer Block"
    quelle = [i for i, z in enumerate(block) if z.startswith("**Quelle:**")]
    ziel = [i for i, z in enumerate(block) if z == ZIEL_ZEILE]
    assert len(quelle) == 1, "Absatz `**Quelle:**` steht nicht genau einmal im neuen Block: %d" % len(quelle)
    assert len(ziel) == 1, "Zeile `%s` steht nicht genau einmal im neuen Block: %d" % (ZIEL_ZEILE, len(ziel))
    assert quelle[0] < ziel[0], "`**Quelle:**` steht nicht vor `%s`" % ZIEL_ZEILE
    g = ziel[0]
    vor = [] if block[g - 1] == "" else [""]
    neu = inhalt[:anfang] + "\n".join(block[:g] + vor + j1 + [""] + block[g:]) + inhalt[ende:]
    text = "\n".join(j1)
    assert neu.count(text) == 1 and neu.count("\n\n" + text + "\n\n" + ZIEL_ZEILE + "\n") == 1, "J1 stuende nicht genau einmal am Ort"
    zeile = "J1 · %s · Block %s · Ankertext 1 · `**Quelle:**` 1 · `%s` 1 · Textzeilen %d · %s" % (
        JOURNAL, x.kennung, ZIEL_ZEILE, len(j1), "einsetzbar (Probe, nichts geschrieben)" if x.probe else "eingesetzt")
    print(zeile)
    if not x.probe:
        JOURNAL.write_text(neu, encoding="utf-8")
        AUSGABE.write_text("# TB-140 D2 — Absatz J1 (erzeugt von j1_einsetzen.py)\n" + zeile + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        RC = main()
    except AssertionError as e:
        print("NICHT EINGESETZT: %s" % e)
        RC = 2
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT EINGESETZT: ungefangene Ausnahme (Traceback oben)")
        RC = 2
    sys.exit(RC)
```

Die Skizze ist in `trading-env` nie gelaufen; passt sie am Werkzeug nicht, passt die Sitzung sie an, legt die gelaufene Fassung unter `docs/belege/TB-140/` ab und beschreibt die Abweichung im Ergebnis.

```python
#!/usr/bin/env python3
"""TB-140 D2 - Zeichengleichheit des Absatzes J1 im Journal.

Eigener Leser (nicht der aus j1_einsetzen.py): nimmt den ersten Codeblock ohne Zaeune nach der
Zeile `#### J1 — ` des Auftrags und prueft als Bytevergleich, dass der Text in JOURNAL.md genau
einmal vorkommt, an Zeilengrenzen steht, zwischen der Kopfzeile des neuen Blocks und dem
Ankertext liegt und mit je einer Leerzeile vor `### Was gemessen ist` steht.
Mit --soll-vorkommen 0 (wenn E1 nicht lief): der Text darf im Journal nicht stehen, auch keine
seiner Zeilen einzeln.
Ausgabe nach j1_vergleich.txt.

Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 -B docs/belege/TB-140/j1_vergleich.py --kennung EH
Rueckgabe: 0 wie das Soll, 1 Abweichung, 2 nicht messbar."""
import argparse
import re
import sys
import traceback
from pathlib import Path

AUFTRAG = Path("docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md")
JOURNAL = Path("docs/projektfuehrung/JOURNAL.md")
AUSGABE = Path("docs/belege/TB-140/j1_vergleich.txt")
ANKER = b"\n---\n\n## Wiederkehrende Lehren\n"
ZIEL_ZEILE = b"### Was gemessen ist"


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--kennung", required=True)
    a.add_argument("--soll-vorkommen", type=int, choices=(0, 1), default=1)
    x = a.parse_args(argv)
    teile = re.split("\n(?=#### J1 — )".encode("utf-8"), AUFTRAG.read_bytes())
    cb = re.search(rb"\n```\n(.*?)\n```\n", teile[1], re.S) if len(teile) == 2 else None
    if cb is None:
        print("NICHT MESSBAR: `#### J1 — ` mit Codeblock steht nicht genau einmal im Auftrag")
        return 2
    text = cb.group(1)
    ziel = JOURNAL.read_bytes()
    kopf = ("\n## %s — TB-140" % x.kennung).encode("utf-8")
    gesamt = ziel.count(text)
    grenzen = ziel.count(b"\n" + text + b"\n")
    einzeln = sum(1 for z in text.split(b"\n") if b"\n" + z + b"\n" in ziel)
    im_block = (ziel.count(kopf) == 1 and ziel.count(ANKER) == 1
                and ziel.find(kopf) < ziel.find(text) < ziel.find(ANKER))
    am_ort = ziel.count(b"\n\n" + text + b"\n\n" + ZIEL_ZEILE + b"\n") == 1
    if x.soll_vorkommen == 1:
        gut = gesamt == 1 and grenzen == 1 and im_block and am_ort
        wort = "GLEICH" if gut else "ABWEICHUNG"
    else:
        gut = gesamt == 0 and einzeln == 0
        wort = "NICHT EINGESETZT, wie das Soll" if gut else "ABWEICHUNG"
    zeile = ("J1 · %s · %d Bytes · %d Zeile(n) · Soll Vorkommen %d · Vorkommen %d · an Zeilengrenzen %d · "
             "Zeilen von J1 einzeln im Journal %d · im neuen Block %s %s · vor `%s` %s · %s" % (
                 JOURNAL, len(text), text.count(b"\n") + 1, x.soll_vorkommen, gesamt, grenzen, einzeln,
                 x.kennung, "ja" if im_block else "nein", ZIEL_ZEILE.decode(), "ja" if am_ort else "nein", wort))
    AUSGABE.write_text("# TB-140 D2 — Zeichengleichheit J1 (j1_vergleich.py)\n" + zeile + "\n", encoding="utf-8")
    print(zeile)
    return 0 if gut else 1


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        RC = 2
    sys.exit(RC)
```

**Geprobt** (Helfer, 07.10.2026, Linux-VM, an der Kopie von `JOURNAL.md` aus der Probe zu E1): ein Probeblock `## EH — TB-140: …` in der Gliederung des Blocks EG vor dem Ankertext; `j1_einsetzen.py --kennung EH` setzt 6 Zeilen; `j1_vergleich.py --kennung EH`: `Vorkommen 1 · an Zeilengrenzen 1`, im neuen Block ja, vor `### Was gemessen ist` ja, `GLEICH`, rc 0. Gegenproben: ein Zeichen von J1 in der Kopie geändert ⇒ `ABWEICHUNG`, rc 1, auch mit `--soll-vorkommen 0` (die übrigen Zeilen stehen noch da) · ohne J1 und mit `--soll-vorkommen 0` ⇒ `NICHT EINGESETZT, wie das Soll`, rc 0 · ohne J1 und ohne den Schalter ⇒ `ABWEICHUNG`, rc 1 · ein zweiter Aufruf von `j1_einsetzen.py` an der Kopie mit J1 ⇒ `NICHT EINGESETZT`, rc 2, die Datei bleibt gleich · eine Kennung, die es im Journal nicht gibt ⇒ `NICHT EINGESETZT`, rc 2.

**Prüfung von J1** mit `docs/belege/TB-140/j1_vergleich.py` ⇒ `j1_vergleich.txt` (Aufruf ohne Umleitung: das Skript schreibt diese Datei selbst und druckt dieselbe Zeile; den rc nennt die Kurz-Tabelle), nach D2: Das Skript liest den ersten Codezaun nach der Zeile `#### J1 — ` aus diesem Auftrag und prüft als Bytevergleich, dass der Text in `JOURNAL.md` genau einmal vorkommt, an Zeilengrenzen steht, zwischen der Kopfzeile des neuen Blocks und dem Ankertext liegt und mit je einer Leerzeile vor `### Was gemessen ist` steht (Aufruf mit `--kennung <Kennung>`). **Soll, wenn E1 lief:** Vorkommen 1, an Zeilengrenzen 1, im neuen Block ja, vor `### Was gemessen ist` ja, 6 Zeilen, `GLEICH`, rc 0. **Soll, wenn E1 nicht lief** (J1 ist dann nicht eingesetzt; Aufruf dazu mit `--soll-vorkommen 0`): Vorkommen 0, keine Zeile von J1 einzeln im Journal, `NICHT EINGESETZT, wie das Soll`, rc 0.

Soll numstat für `docs/projektfuehrung/JOURNAL.md`: zweite Spalte `0`. Die erste Spalte ist die Zeilenzahl des Blocks der Sitzung samt Trennzeilen; sie hat kein festes Soll, das Ergebnis nennt sie (Vorgänger: `40	0`, `docs/belege/TB-138/d3_numstat.txt`). Fest ist, wenn E1 lief: Die 6 Zeilen von J1 und die Leerzeile danach liegen darin; lief E1 nicht, liegen sie nicht darin.

## Schritt D — Abgabe

Wie Vorgänger (dort Z. 207 bis Z. 215), mit diesen Unterschieden:

D0. 0b wiederholen ⇒ `docs/belege/TB-140/0b_nachher.txt`; gleich bis auf die ersten drei Zeilen: Kopfzeile („ausgang“ oder „nachher“), `ZEIT` und `HEAD`. So unterscheiden sich auch `docs/belege/TB-138/0b_ausgang.txt` und `0b_nachher.txt`: in genau diesen drei Zeilen.

D1. `docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md`:
- Kopf, Stand und Commits (⟨S0⟩, ⟨T1⟩, Teil 2, N, Abgabe) · Kurz-Tabelle (0a mit md5 und Platzhaltersuche, 0b, Gegenproben, V4, V5, V6, Z1, Z2, Zwischenstand, Fundstellenprüfung, V1, V2, V3, N mit E1 und J1, Tabellenvergleich, D0, je Soll und Ist).
- **Teil 1**, je Voraussetzung und je Zusatzmessung (Z1, Z2): Zahlen, Einzelfälle, Urteil, Beleg mit Zeile; bei Z2 die Stellen im Wortlaut.
- **Teil 2**: zuerst die Übersicht je Bot, dann je Voraussetzung die Tabellen aus dem Belegordner, ganz — eingesetzt mit `ergebnis_tabellen.py --einsetzen`, geprüft mit `--pruefen` ⇒ `ergebnis_tabellen.txt` (Form der Belege, Nr. 6); ebenso `z2_stellen.md` in Teil 1; darunter getrennt „Belegt“, „Erschlossen“ (jede Kette) und „Offen“ (was fehlt).
- **„Lesarten N1 bis N7 und offene Punkte O1 bis O7: woran welche Aussage hängt“** (Form des Vorgängers).
- **„Für den steuernden Chat“** — zwölf Zeilen, eine je Teilfrage der Tabelle „Urteile je Teilfrage“ (V4, V5, V6, Z1, Z2, V1 Nr. 0, V1 (i), V1 (ii), V2 (a), V2 (b), V3 (i), V3 (ii)), je: das Urteil im Wortlaut dieser Tabelle (bei V3 (i) die Zählung, kein Urteil), dazu ein Satz mit der Tatsache, wie sie als Tatsachennotiz stehen könnte, mit Fundstelle im Beleg und ohne Urteil über das Verfahren. Darunter, wohin was geht:
  - Der Registereintrag TB-139 braucht V4, V5, V6, Z1 und Z2.
  - Vor dem signierten Tag an den Verfahrensprüfer geht jeder Befund aus V2 (b) (so die Klammer) und die Tabelle zu V3 (i) (für V3 (i) ist der Zeitpunkt Setzung des steuernden Chats; die Klammer zu R78 (e) nennt keinen).
  - V1 — jede Stelle, die eine andere Spalte oder eine Datei anderen Namens liest, dazu der Ordner je Stelle, die Beschreibung aus V1 Nr. 4 und O7 — steht unter „Für Fable“ (die Klammer sagt „wird gemeldet“ und nennt keinen Zeitpunkt) und als Tatsache für „Voraussetzungen und Befunde“ des Registerauftrags.
  - V2 (a) — behält oder verwirft, je Stelle — ist die Tatsache, nach der die Klammer zu R78 (d) zuerst fragt: Sie geht mit V2 (b), bei einem Befund dort an den Verfahrensprüfer, sonst als Tatsachennotiz an den steuernden Chat.
  - V3 (ii) geht als Tatsache an den steuernden Chat, für den Bau des Zellen-Erzeugers (Klammer: „trifft das Zweite zu, genügt diese Prüfung, und der Erzeuger baut keine zweite“), und unter „Für Fable“ zur Kenntnis; ob die Prüfung „genügt“, entscheidet der Verfahrensprüfer.
  - Wo die Klammer kein Ziel und keinen Zeitpunkt nennt, sind diese Ziele Setzung des steuernden Chats, vorläufig.
- **„Für Fable“** (offene Fragen im Wortlaut, darunter O1, O5 und O7, soweit die Messung sie berührt) · **„Nicht getan“** · **„In einfacher Sprache“**.
- Keine Kurse, keine Kennzahlen. Codezeilen dürfen zitiert werden.

D2. Journalblock wie Vorgänger; Kennung messen (erwartet **EH**), mit Quellenzeile. Die Sitzung schreibt den Block selbst, in der Gliederung des Blocks EG (Kopfzeile, Quelle, „Was gemessen ist“, „Was aus dieser Sitzung an Regeln bleibt“, „Was offen bleibt“, Schlusszeile), und setzt J1 aus Schritt N mit `j1_einsetzen.py` zeichengleich an den dort genannten Ort (nur, wenn E1 lief); danach `j1_vergleich.py`, in beiden Fällen, mit dem Soll aus Schritt N.

D3. Drei Commits in dieser Folge (so lief es im Vorgänger: `b923a05` Abgabe, `439834c` „numstat und porcelain nach der Abgabe“, `8d172c0` „porcelain neu gemessen am Stand 439834c (keine Zeile)“):

1. Abgabe-Commit `TB-140 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Er heisst **⟨A⟩**.
2. `git diff --numstat ⟨S0⟩ ⟨A⟩` ⇒ `docs/belege/TB-140/d3_numstat.txt` (Soll: nur Pfade unter `docs/belege/TB-140/`, dazu `docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md`, `docs/projektfuehrung/JOURNAL.md` ohne entfernte Zeile und, wenn E1 lief, `docs/projektfuehrung/BACKLOG.md` mit `8	0`); Commit `TB-140 D3: numstat nach der Abgabe`, pushen. Er heisst **⟨D⟩**.
3. Am Stand ⟨D⟩, bevor eine weitere Datei entsteht: `git status --porcelain > "$TMPDIR/tb140_d3_porcelain.txt"` (Soll: keine Zeile), von dort als `docs/belege/TB-140/d3_porcelain.txt`; letzter Commit `TB-140 D3: porcelain gemessen am Stand <Kurz-Hash ⟨D⟩> (keine Zeile)`, pushen.

**`porcelain` wird nach dem letzten Commit gemessen** (7c, 5b): Die Datei aus Nr. 3 belegt den Baum am Stand ⟨D⟩. Nach dem letzten Commit misst die Sitzung noch einmal und nennt das Ergebnis in ihrer Schlussmeldung (Soll: keine Zeile); ein weiterer Commit entsteht dafür nicht, sonst nähme die Folge kein Ende.

## Abbruchkriterien (nur für diesen Gegenstand)

Die sechs Kriterien des Vorgängers (dort Z. 219 bis Z. 224) gelten, das vierte und das fünfte in dieser Fassung. Das vierte: Eine Messung verlangte, eine Ergebnisgrösse zu lesen oder zu rechnen, Code des Repos auszuführen oder zu importieren — ausgenommen `shared/snapshot.py --pruefen` ohne `--json` in 0b und D0 (so fasst es der Vorgänger, dort Z. 121) und die eigenen Skripte unter `docs/belege/TB-140/`, auch die dorthin übernommenen `0b_ausgang.sh`, `einfuegen.py` und `c3_vergleich.py` —, oder sie ginge nur mit einer Änderung ausserhalb der genannten Pfade. Das fünfte: Ein Wert aus 0b ist in D0 anders, ausser in den ersten drei Zeilen (Kopfzeile, `ZEIT`, `HEAD`).

**Kein Abbruch:** jeder Befund aus V1 bis V6, Z1 und Z2 · eine Abweichung in V4 (V5, V6, Z1 und Z2 laufen trotzdem) · der Kalender lässt sich nicht laden (V5 heisst „nicht messbar“) · rc 2 einer Messung · ein Register, ein Abbild, ein Lock oder eine Universumsdatei mit anderem Hash · eine Zeile `UNGLEICH` in der Fundstellenprüfung, die sich nicht berichtigen lässt (nennen) · ein Treffer der Platzhaltersuche (0a) oder ein stehengebliebener Platzhalter im Blocktext von E1 oder J1 (Schritt N) · der BACKLOG-Anker ≠ 1.

Bei Abbruch nach ⟨S0⟩ gilt der Vorgänger (Z. 228), Datei `docs/belege/TB-140/abbruch.txt`. Liegt ⟨T1⟩ schon auf `origin/main`, bleibt er dort.

## In einfacher Sprache

Der Prüfer des Verfahrens hat drei neue Regeltexte geschrieben. Sechs Sätze darin gelten nur, wenn etwas stimmt, das noch niemand nachgemessen hat. Dieser Auftrag misst diese sechs Dinge, soweit sie heute messbar sind. Er ändert nichts an Programmen, Daten und Regeln; er schreibt nur seine Belege, sein Ergebnis und einen Nachtrag in Backlog und Journal über das, was seit dem letzten Auftrag geschah. Zuerst die drei schnellen: Sind auf dem Mac wirklich alle 67 festgeschriebenen Programmpakete in genau der festgeschriebenen Fassung installiert, und ist das Betriebssystem das festgeschriebene? Liefert der Börsenkalender dieselben Handelstage, wenn man ihn für jeden Aktien-Bot einzeln fragt, statt einmal für alles? Und stand die letzte Zeile ohne Schlusskurs bei der Aktie APH schon in dem Datenstand, an dem am 2. Oktober gemessen wurde? Dazu kommen zwei Nachweise für Sätze, die der Prüfer als Tatsache geschrieben hat: Fehlt in den Tagesdateien der Kryptowährungen wirklich nirgends ein Schlusskurs? Und steht in dem älteren Bericht wörtlich, dass die Paketfassung 5.4.0 aus einer Cloud-Sitzung stammt? Diese fünf Antworten werden sofort gesichert und in einer Zeile gemeldet, weil der Eintrag der neuen Regeln darauf wartet; die Arbeit geht ohne Pause weiter. Danach wird Programmtext gelesen, ohne ihn auszuführen: Aus welchem Ordner, welcher Datei und welcher Spalte kommen die Schlusskurse? Wird eine Zeile ohne Schlusskurs weggelassen? Kann irgendein Ergebnis aus einer Kurszeile mit Datum am oder nach dem 2026-09-01 entstehen (der Stichtag selbst zählt mit)? Und bricht das Auswertungsprogramm ab, wenn in einer Ergebnistabelle statt einer Zahl „unendlich“ oder „keine Zahl“ steht? Nicht jede dieser Fragen lässt sich heute entscheiden: Ein Programm, das die Ergebnistabellen schreibt, ist bisher nicht gefunden (auch das wird nachgemessen); wo eine Antwort daran hängt, heisst sie „nicht messbar“ oder „am Code nicht entscheidbar“. Ob ein Fund eine Regel verletzt, entscheidet nicht dieser Auftrag, sondern der Prüfer. Heraus kommen Fundstellen, Tage und Zählungen — keine Kurse und keine Ergebnisse der Strategien. Was nicht stimmt, wird gemeldet und nicht repariert.
