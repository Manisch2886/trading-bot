# TB-138 Verfahrensmessung am Snapshot, nur lesend — Kalender „NYSE“ gegen die Kurstage je Aktien-Bot (R74 (e)), Reihenenden und Symbol-Tage Lücke (R72 (d)), Paketfassung des Kalenders (54.6 Nr. 8)

**Sitzungstitel:** `TB-138` · **Modell:** Opus 5.5 (Standard) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 06.10.2026 vom steuernden Chat
**Vorgänger:** TB-133 (`0c70853`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-138_verfahrensmessung_snapshot.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3`, immer mit `-B` (*Grund:* kein `__pycache__` im Arbeitsbaum). **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.

**Vorbild:** `docs/auftraege/MAC_TB-115_drei_verfahrensmessungen.md` (Ergebnis `docs/ERGEBNIS_TB-115_drei_verfahrensmessungen.md`): Verfahrensmessungen vor dem Tag, nur lesend, Messskripte und Rohausgaben unter `docs/belege/TB-<Nr>/`. Schritt 0 und Abgabe haben die Form von TB-133 (`docs/auftraege/MAC_TB-133_regelwerk_nachtrag_umzug_sitzung_bruecke.md`). „Vor dem Tag“ heisst in diesem Auftrag und im Register: vor dem signierten Tag, an dem der registrierte Selektionslauf rechnet.

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei** (Betreiberentscheid 26.09.2026; so auch TB-127, TB-128, TB-131 und TB-133). Betreiber am 06.10.2026, 13:22: „Fahre im Backlog fort“. Dass TB-138 die Verfahrensmessung am Snapshot ist, stand am 06.10.2026, 13:34, als Vorgabe im steuernden Chat; der Betreiber hat nicht widersprochen (`UEBERGABE.md`, Umzug 06.10.2026, 13:43, Block 4 Nr. 1 und Block 6).

**An der Sperrliste gemessen** (steuernder Chat, 06.10.2026, am HEAD `0c70853`): Im gültigen Abbild `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json` (sha256 beginnt `46f0ad5d1d83a253`) liegt keiner der 22 Pfade der Liste `eingefroren` und keiner der Pfade in `hashes` der 14 Punkte unter `docs/`; die Liste `bestimmt` ist leer. Dieser Auftrag schreibt nur unter `docs/`.

Geschrieben wird nur: `docs/belege/TB-138/` (Messskript und Rohausgaben), `docs/ERGEBNIS_TB-138_verfahrensmessung_snapshot.md`, ein Block in `docs/projektfuehrung/BACKLOG.md` (Schritt B), ein Block in `docs/projektfuehrung/JOURNAL.md` (D2).

Gelesen werden: Register, Code, `requirements.lock`, `MANIFEST.json`, die zwei Universumsdateien und alle Kursdateien des Snapshots (jede Zeile; ausgewertet wird nur `open_time` und, ob `close` fehlt).

Die Vorgabe vom 06.10.2026 nennt 53.10 Nr. 10 nicht. Diese Nummer kommt dazu, weil Register Z. 11514 sie an die Verfahrensmessung nach Nr. 3 bindet.

⛔ **Nicht erlaubt, mit Grund:**
- Jede Änderung an Code, Tests, Register (`docs/VORREGISTRIERUNG_*`), Abbild, `requirements.lock`, `trading-env/`, `snapshots/`, `research/`, `shared/`, `strategies/`, `notifications/`, `docs/werkzeuge/`. *Grund:* Der Auftrag misst. Ein Befund wird gemeldet und vor dem Tag entschieden (R74 (e), R72 (d)), nicht behoben.
- `pip install`, ein Paketwechsel, ein neues venv. *Grund:* Gemessen wird die Umgebung, wie sie ist.
- `faltenplan.faltenplan()` oder `erste_falte()` aufrufen, den Zellen-Erzeuger oder einen Lauf des Selektionsraums starten. *Grund:* `faltenplan.faltenplan()` ist kein Lesen, es startet einen Trockenlauf (ARBEITSWEISE 0, „Wenn ich einen Auftrag schreibe“); ob `erste_falte()` rechnet, ist nicht gemessen.
- Kurse, Renditen, Kennzahlen oder Trade-Zahlen ausgeben oder in einen Beleg schreiben. *Grund:* Sichtschutz, Register 27.1. Zulässig ist die Verfahrensmessung nach 27.2. Ausgegeben werden nur Tage, Symbole, Dateinamen, Zählungen, Paketfassungen und Pfade.
- Einen anderen Kalendernamen als „NYSE“ rechnen oder vergleichen. *Grund:* R74 (e): Der Name wird nicht ohne Entscheidung gewechselt; ein Vergleich wäre der erste Schritt dazu.
- Den Registereintrag zu 54.5 (Stand zu R74 (e)) schreiben. *Grund:* Das ist nach dem Ergebnis eine Einzelfreigabe des Betreibers.
- Im Hauptordner etwas ausserhalb der genannten Pfade anlegen, auch keine Zwischenablage. *Grund:* 0a und D3 zählen die Einträge. Zwischenstände und Kopien für die Gegenprobe gehen nach `$TMPDIR`.

Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt (auch `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`); das ist kein Ändern im Sinn der Verbote. Von den acht Punkten aus 7c entfallen db-Sicherung und Basislauf (kein Bot läuft, kein Test, nichts wird geschrieben, was ein Bot liest); der Datenstand ist der Snapshot nach L1, geprüft in 0b. Datenbanken und `crontab` werden nicht berührt. Die Sperrlisten-Sonde läuft hier nicht: Ob sie `faltenplan.faltenplan()` aufruft, ist nicht gemessen. An ihrer Stelle stehen 0b, D0 und die Zeilenbilanz in D3.

## Die Registerstellen, zeichengleich

*Vom Bauskript des steuernden Chats aus `docs/VORREGISTRIERUNG_neuselektion.md` geschnitten (11 581 Zeilen, sha256 `8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc`, Stand `9b7b060`). Die Sitzung liest die Stellen im Register nach; der Wortlaut dort gilt.*

**R74 (54.1), Z. 11524, (a) und (e):**

> (a) Handelskalender nach R66 (a) ist der Kalender „NYSE“ des Pakets pandas_market_calendars in der Fassung des Locks (17.5). Handelstage der Aktien-Tagesreihe sind die Tage, die dieser Kalender im Zeitraum nach R66 (a) als Sitzungstage führt, verkürzte Sitzungen eingeschlossen. Ein anderer Kalendername des Pakets ist ein anderer Kalender, auch wenn er dieselbe Börse meint.

> (e) Vor dem signierten Tag wird in der Lock-Umgebung am Snapshot gemessen (Verfahrensmessung nach 27.2, zusammen mit der Messung nach R72 (d)), dass die Bedingung aus R66 (b) für den Kalender nach (a) erfüllt ist, je Aktien-Bot. Ist sie es nicht, wird gemeldet und vor dem Tag entschieden; der Name wird nicht ohne diese Entscheidung gewechselt. Die Vergleiche in 53.9 sind Ersatzmessungen ausserhalb der Lock-Umgebung und ersetzen diese Messung nicht.

**R66 (53.1), Z. 11414, (a) und (b):**

> (a) Die Tagesreihe einer Zelle führt jeden Handelstag des Kapitalpfads, vom 1. Januar der ersten Selektionsfalte des Bots (29.3) bis zum Ende der Bestätigungsperiode (35.1), ohne Lücke. Handelstage sind bei Krypto die Kalendertage (15.4, Anmerkung 1), bei Aktien die Tage des Handelskalenders nach 17.5 (Umgebung, im Lock). Ein Tag, an dem die Zelle keine Position hält, steht mit Rendite 0 und Exposure 0 in der Reihe (1a), auch ein Tag vor dem ersten Handelbar-Tag des Bots.

> (b) Kalender und Kurse stimmen überein: Im Zeitraum nach (a) trägt an jedem Handelstag mindestens ein Symbol der Universumsdatei des Bots (3a) im Snapshot einen Kurs, und kein Symbol der Universumsdatei trägt einen Kurs an einem Tag, der kein Handelstag ist. Eine Abweichung ist ein Befund über Daten oder Umgebung, kein Ausgang (Bauart R33). Der Zellen-Erzeuger prüft das im Lauf je Bot und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. [Voraussetzung, zu messen: welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld kalender); die Messung zur Anfrage 02.10.c verglich mit dem NYSE-Kalender.]

**R72 (53.7), Z. 11468, (d):**

> (d) Nach dem letzten Kurs eines Symbols führte derselbe Code das Symbol an jedem Folgetag mit Rendite 0 im Mittel weiter. Das wäre mit 3b (c) nicht vereinbar: Ein Symbol ohne weitere Kurse gehört nicht mehr zu der Menge, in der der Bot lebt. Am Bestand vom 02.10.2026 endet keine Reihe früher. Vor dem signierten Tag wird am Snapshot gemessen (Verfahrensmessung nach 27.2), dass keine Kursreihe eines Symbols der zwei Universumsdateien vor dem letzten Kurstag ihres Marktes endet, und wie viele Symbol-Tage Lücke im Zeitraum nach R66 (a) liegen. Endet eine Reihe früher, wird gemeldet und vor dem Tag entschieden. benchmark.py wird für nichts in diesem Block geöffnet.

**53.10, Z. 11507 und Z. 11514 · 54.6, Z. 11570 und Z. 11577 · 27.2, Z. 5164:**

```
| 3 | Verfahrensmessung am Snapshot (R72 (d)): keine Kursreihe endet vor dem letzten Kurstag ihres Marktes; Zahl der Symbol-Tage Lücke im Zeitraum nach R66 (a) | vor dem signierten Tag |
| 10 | `tagesschluss` (`benchmark.py:155`, `159–160`) normalisiert `open_time` nicht und prüft keine doppelten Daten; am Bestand vom 02.10.2026 folgenlos | mit der Verfahrensmessung nach Nr. 3 |
| 1 | Verfahrensmessung in der Lock-Umgebung am Snapshot (R74 (e)): die Bedingung aus R66 (b) für den Kalender „NYSE“, je Aktien-Bot; zusammen mit der Messung nach R72 (d) (53.10 Nr. 3) | vor dem signierten Tag |
| 8 | Das Feld `kalender` aus TB-47 nennt `paket_vorhanden` 5.4.0; der Lock und 17.5 nennen 4.6.1 | mit der Verfahrensmessung nach Nr. 1 |
> **27.2** Zulässig sind Verfahrensmessungen — Kalender, Datenbestand, Faltenzahl, Handelbarkeit, Benchmark-Seite — und Wirkungen einer Regel auf die registrierten heutigen Parameter, wenn die Regel vor der Messung geschrieben stand (Bauart 24.3).
```

## Belegt · erschlossen · offen

**Belegt** (gemessen 06.10.2026 vom steuernden Chat über die Geräteanbindung am HEAD `0c70853`, jede Zeile vom Bauskript an der Quelle geprüft; die Sitzung misst nach, ihre Zahl gilt):

- Snapshot-Ordner `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/`: 225 Einträge auf oberster Ebene, davon 174 `*_1d.csv`, 25 `*_1h.csv`, 24 `*_4h.csv`, `MANIFEST.json` und der Ordner `config/` mit `sp500_top150.txt` und `top25_symbols.txt`. `MANIFEST.json` führt als `snapshot_hash` den Ordnernamen; Register Z. 3044 und Z. 3049 nennen denselben Hash.
- Universumsdateien im Snapshot: `config/sp500_top150.txt`, sha256 `6acba892f38e998cf43ae9e5594c4707945143aba481429c44a5c6005339f607`, 150 nichtleere Zeilen ohne `#`; `config/top25_symbols.txt`, sha256 `3afc95a4f6b5ebc3a8f7bb7854b5dd59c4ecc4e3d86aa7b93c08066a3fccf810`, 25 solche Zeilen. Beide sind bytegleich mit `config/` im Repo. Das Register führt für Aktien 150 Symbole (Z. 1581) und für Krypto 24 (Z. 1580 mit der Korrektur Z. 1583–1586: 25 Zeilen abzüglich `XAUTUSDT`).
- Kopfzeile von `AAPL_1d.csv`, `BTCUSDT_1d.csv` und `BTCUSDT_1h.csv`: `open_time,open,high,low,close,volume`. Erste Datumszelle: `1980-12-12`, `2017-08-17`, `2017-08-17 04:00:00`.
- Die vier Aktien-Bots sind `elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks` und `volatility_breakout` (Namen und Markt: Register Z. 6001–6004); alle vier lesen dieselbe Universumsdatei (Z. 1588–1590), nach Z. 1581 `config/sp500_top150.txt`. Die fünf Krypto-Bots sind `elliott_wave`, `rsi2_crypto`, `t3_supertrend`, `turtle_soup_crypto` und `volatility_breakout_crypto` (Z. 5996–6000); alle fünf lesen dieselbe Datei (Z. 1588–1590), nach Z. 1580 `config/top25_symbols.txt`.
- Von den 25 Zeilen der Krypto-Datei hat nur `XAUTUSDT` nicht alle drei Reihen: Es gibt `XAUTUSDT_1h.csv`, aber keine `_1d`- und keine `_4h`-Reihe. Jede Zeile der Aktien-Datei hat ihre `_1d`-Reihe. Keine Reihe im Snapshot steht ohne Zeile in einer der zwei Dateien.
- Register 33.2, Tabelle Z. 5994–6004, Spalte „erste Falte“: `elliott_wave` 2018–2019, `t3_supertrend` 2019, `rsi2_crypto` 2019, `turtle_soup_crypto` 2018, `volatility_breakout_crypto` 2018, `elliott_wave_stocks` 2017, `rsi2_mean_reversion` 2018, `turtle_soup_stocks` 2017, `volatility_breakout` 2018. R53 (49.1, Z. 11005) sagt dazu: „die erste Falte ist nach dieser Präzisierung neu abzuleiten“; der Vorlauf nach R53 (a) ist offen geführt in Z. 11208 und Z. 11323.
- `notifications/boersenkalender.py`: Z. 70 `KALENDER_NAME = "NYSE"`, Z. 109 `mcal.get_calendar(KALENDER_NAME)`, Z. 125 `_kalender().schedule(start_date=von, end_date=bis)`.
- `requirements.lock`: Z. 37 `exchange-calendars==4.5.6`, Z. 50 `numpy==2.0.2`, Z. 51 `pandas-market-calendars==4.6.1`, Z. 52 `pandas==2.3.3`; Kopf Z. 6–8 nennt Interpreter 3.9.6 und die Plattform.
- `research/snapshotgrenze/ergebnisse/eingaben.json`, Feld `kalender`: `paket_vorhanden` ist „5.4.0“. Der Wert kommt aus `importlib.metadata.version` des Interpreters, der `erhebung_eingaben.py` startet (dort Z. 613–618). Ohne `--json` schreibt das Skript keine Datei (Z. 702, Z. 708–715); die Zeile „Paketfassung hier“ druckt Z. 675. Letzter Commit an `eingaben.json`: `fc38d25` (Autor „Claude“, 2026-09-18 05:18:53 +0000).
- `shared/snapshot.py --pruefen ORDNER` (Z. 1243) schreibt nur mit `--json` (Z. 1257); zwischen Z. 1045 und Z. 1157 (`pruefen`) steht keine Schreibstelle. Ausgänge 0, 1, 2 (Z. 294–296).
- `research/vorregistrierung/ergebnisse/faltenplan.json` (im Abbild eingefroren, sha256 gleich) führt bei den vier Aktien-Bots als erste Falte `2019` und bei den fünf Krypto-Bots `status` „platzhalter“ ohne Falten. Das Register nennt in 21.5 (Z. 3448) für die Aktien-Bots 2017 und 2018. **Die Datei ist deshalb nicht die Quelle für den Beginn des Zeitraums.**
- Vergleichswerte, kein Soll (Register Z. 11486 und Z. 11494, Bestand vom 02.10.2026, nicht der Snapshot, ausserhalb der Lock-Umgebung): Aktien 0 Tage nur im Kalender „NYSE“ und 0 Tage nur in den Daten; zwei Symbol-Tage Lücke (1974-06-03 `LMT`, 2026-08-10 `MNST`); Krypto keine Lücke; kein doppeltes Datum.

**Erschlossen — Lesarten des steuernden Chats, vorläufig.** Das Ergebnis sagt je Lesart, ob eine Aussage an ihr hängt.

- **L1** „Der Snapshot“ ist der Ordner `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/`. Ab Z. 11412 nennt das Register für diese Messung weder Pfad noch Hash.
- **L2** „Lock-Umgebung“ ist `trading-env/` mit `trading-env/bin/python3` (Register Z. 11491 setzt beides nebeneinander).
- **L3** Ende des Zeitraums nach R66 (a): der 31.08.2026 einschliesslich. Die Bestätigungsperiode ist `2026-01-01/2026-09-01`, Ende ausschliesslich (Register 35.1, Z. 6375 und Z. 6385–6388). Nach den Messungen beim Gegenlesen dieses Auftrags (06.10.2026) ändert weder die Berichtigung 38.1 (Z. 6413–6420) noch R37 (48.5, Z. 10837; Marke Z. 6443) dieses Ende: R37 führt einen zweiten Zeitraum gleichen Namens für den Papierpfad ein, R66 (a) verweist auf 35.1. Auch die Marke Z. 6404–6411 berührt das Ende nicht.
- **L4** Beginn des Zeitraums nach R66 (a), je Bot: der 1. Januar des ersten Jahres aus der Spalte „erste Falte“ in Register 33.2 (Z. 5994–6004, oben unter „Belegt“; für die Aktien-Bots gleich 21.5, Z. 3448). R66 (a) verweist für den Beginn auf 29.3 (Z. 5408); dort steht die Regel, keine Jahreszahl. Die Werte stehen unter dem Vorbehalt aus R53 (Z. 11005). Dieser Auftrag leitet die erste Falte nicht neu ab.
- **L5** „trägt einen Kurs“: Die Reihe `<SYMBOL>_1d.csv` hat an dem Tag eine Zeile, in der `close` nicht fehlt. `close` fehlt, wenn die Zelle leer ist oder einen Text trägt, den `pandas.read_csv` als Fehlwert liest (`nan`, `NaN`, `NA`, `null` und die übrigen; die Liste steht im Beleg). Leere Zellen und Fehlwert-Texte werden getrennt gezählt. Der Tag ist das Datum in `open_time`.
- **L6** „Sitzungstage“ (R74 (a)): der Index von `mcal.get_calendar("NYSE").schedule(start_date=…, end_date=…)`, also der Aufruf aus `boersenkalender.py` Z. 109 und Z. 125. Dass er verkürzte Sitzungen mitführt, ist nicht gemessen; M1 Nr. 6 misst es.
- **L7** „letzter Kurstag ihres Marktes“ (R72 (d)): der späteste Kurstag über alle `_1d`-Reihen der Symbole einer Universumsdatei.
- **L8** „Symbol-Tag Lücke“: ein Handelstag (Aktien nach L6, Krypto jeder Kalendertag nach R66 (a)) zwischen dem ersten und dem letzten Kurstag eines Symbols, an dem das Symbol keinen Kurs trägt. Tage vor dem ersten Kurstag eines Symbols sind keine Lücke und werden getrennt gezählt.
- **L9** „Kursreihe eines Symbols“ (R72 (d)): die Reihe `<SYMBOL>_1d.csv`. Die `_1h`- und `_4h`-Reihen der Krypto-Datei werden mitgezählt, aber ohne Urteil. `XAUTUSDT` zählt nach Register Z. 1583–1586 nicht zu den 24 Krypto-Symbolen; seine `_1h`-Reihe wird genannt, nicht bewertet.

Weil L3 und L4 vorläufig sind, misst das Skript **zuerst über die ganze Spanne der Daten und je Kalenderjahr** und nennt jede Abweichung mit Datum. Die Aussage je Bot folgt daraus für jeden Beginn und jedes Ende; dazu nennt das Ergebnis je Markt das früheste Jahr, ab dem bis zum Ende keine Abweichung liegt.

**Offen:**

- **O1** Die erste Selektionsfalte je Bot nach R53 (neu abzuleiten, Z. 11005; der Vorlauf nach R53 (a) offen in Z. 11208 und Z. 11323). Dieser Auftrag rechnet mit L4 und leitet nichts ab.
- **O2** Ob `trading-env/bin/python3` startet und welche Fassungen es zur Laufzeit meldet. Über die Geräteanbindung ist das nicht messbar (sie ist eine Linux-VM, `trading-env` ein macOS-venv).
- **O3** Woher „5.4.0“ stammt, also welcher Interpreter am 18.09.2026 `erhebung_eingaben.py` gestartet hat.
- **O4** Wie sich `shared/snapshot.py --pruefen` unter `-B` verhält, wenn die Umgebungsvariablen des Selektionslaufs (`shared/paths.py` Z. 205–208) nicht gesetzt sind.

## Schritt 0 — Sicherung, Ausgang

0a. **Zuerst, bevor `docs/belege/TB-138/` entsteht** (den Ordner gibt es noch nicht): `git rev-parse --abbrev-ref HEAD` (Soll `main`) und `git rev-parse --short HEAD` (Soll `0c70853`) nach `"$TMPDIR/tb138_0a_head.txt"`; weicht eines ab ⇒ Abbruch. Dann `git status --porcelain > "$TMPDIR/tb138_0a.txt"`. Soll: genau die Einträge unten; die Reihenfolge zählt nicht. Weicht etwas ab ⇒ Abbruch. Danach beide Dateien nach `docs/belege/TB-138/` kopieren (`0a_head.txt`, `0a_status.txt`).

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-138_verfahrensmessung_snapshot.md
```

Commit `TB-138 Schritt 0: Stand des steuernden Chats 06.10.2026`, pushen. Der Commit heisst im Folgenden **⟨S0⟩**.

0b. Ausgangswerte mit `docs/belege/TB-138/0b_ausgang.sh` ⇒ `docs/belege/TB-138/0b_ausgang.txt`:

| Wert | Soll |
|---|---|
| `trading-env/bin/python3 -B -c "import sys; print(sys.version)"` | startet; 3.9.6 |
| HEAD | ⟨S0⟩ |
| `docs/VORREGISTRIERUNG_neuselektion.md`: Zeilen, sha256 | 11 581, `8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc` |
| Abbild `…/sperrliste_abbild_2026-09-26_tb117.json`: sha256 | beginnt `46f0ad5d1d83a253` |
| `requirements.lock`: sha256 | nur messen |
| die zwei Universumsdateien unter `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/config/`: sha256 | wie unter „Belegt“ |
| `trading-env/bin/python3 -B shared/snapshot.py --pruefen snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` (ohne `--json`): Ausgabe und rc | rc 0 |
| sha256 über die sortierte Liste `sha256  Pfad` aller Dateien unter `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/` | nur messen; 226 Dateien |

Startet `trading-env/bin/python3` nicht ⇒ Abbruch nach 0b mit Meldung (dann gibt es keine Lock-Umgebung, in der gemessen werden kann; das ist der Befund zu O2). `--pruefen` mit Ausgang 1 oder 2 ⇒ Abbruch (dann ist der Ordner nicht nachweislich der registrierte Snapshot). Wie sich das Werkzeug dabei verhält, ist vom Werkzeug abhängig: im Ergebnis beschreiben (O4). Weicht „3.9.6“ oder „226 Dateien“ ab ⇒ vermerken, kein Abbruch. Weicht das Register, das Abbild oder eine Universumsdatei ab ⇒ kein Abbruch: vermerken; die Registerstellen über ihre Kennung suchen (R74, R66, R72, 53.10, 54.6).

## Schritt A — Das Messskript und die drei Messungen

Ein neues Skript `docs/belege/TB-138/verfahrensmessung_snapshot.py` (es wird committet). Es liest nur und schreibt nur nach stdout. Aufruf je Messung:

```
trading-env/bin/python3 -B docs/belege/TB-138/verfahrensmessung_snapshot.py m1 > docs/belege/TB-138/m1.txt 2>&1; echo "rc $?" >> docs/belege/TB-138/m1.txt
```

ebenso `m2` und `m3`. Schalter `--snapshot ORDNER` und `--bis JJJJ-MM-TT` (Vorgaben: der Ordner nach L1, das Ende nach L3), damit die Gegenprobe an einer Kopie laufen kann. Kopf jeder Ausgabe: `sys.executable`, `sys.version`, `platform.platform()`, die Fassungen von `pandas_market_calendars`, `pandas`, `exchange_calendars` und `numpy` aus `importlib.metadata`, der Snapshot-Ordner, der Zeitpunkt und die Zeile „Fassungen gleich Lock: ja/nein“ (Pakete gegen `requirements.lock` Z. 37, 50, 51, 52, Interpreter gegen Z. 6–7). Bei „nein“ gilt M1 nicht als Messung in der Lock-Umgebung; das Ergebnis sagt es. Rückgabe: 0 gemessen ohne Befund, 1 gemessen mit Befund, 2 nicht messbar (Prüfprinzipien A2: „konnte nicht messen“ ist ein eigenes Ergebnis). Bei rc 2 heisst die Messung „nicht gemessen“, der Grund steht im Beleg; das ist kein Abbruch. Die CSV liest das Skript als Text; `close` wird nur darauf geprüft, ob es nach L5 fehlt, und nicht in eine Zahl gewandelt (*Grund:* Sichtschutz; kein Kurs wird verarbeitet).

**Gegenprobe vor den Messungen** mit `docs/belege/TB-138/gegenprobe.sh` ⇒ `docs/belege/TB-138/gegenprobe.txt` (Prüfprinzipien B1, „Eine Mutationsprobe muss beissen“). Das Skript legt in `$TMPDIR` zwei Kopien eines kleinen Snapshots an: drei Aktien-Symbole und zwei Krypto-Symbole mit ihren Reihen, dazu die zwei Universumsdateien, auf diese Symbole gekürzt. Die erste Kopie bleibt unverändert. In der zweiten liegen acht Eingriffe, alle zwischen 2020 und 2025 ausser G4 (am Reihenende):

| | Eingriff | muss melden |
|---|---|---|
| G1 | bei einer Aktie eine Zeile an einem Handelstag entfernen | `m2`: ein Symbol-Tag Lücke |
| G2 | bei allen drei Aktien die Zeile desselben Handelstags entfernen | `m1`: ein Tag nur in H; `m2`: drei Symbol-Tage Lücke |
| G3 | bei einer Aktie eine Zeile an einem Samstag einfügen | `m1`: ein Tag nur in K |
| G4 | eine Aktienreihe um ihre letzten fünf Zeilen kürzen | `m2`: eine früher endende Reihe |
| G5 | bei einer Aktie eine Zeile verdoppeln | `m2`: ein doppeltes `open_time` |
| G6 | bei einer Aktie `close` an einem Handelstag leeren | `m1`: eine Zeile ohne `close`; `m2`: ein Symbol-Tag Lücke |
| G7 | bei einem Krypto-Symbol einem `open_time` der `_1d`-Reihe eine Uhrzeit ungleich `00:00:00` anhängen | `m2`: ein Zeitanteil |
| G8 | bei einem Krypto-Symbol eine Zeile der `_1d`-Reihe entfernen | `m2`: ein Symbol-Tag Lücke |

Soll: Verglichen werden nur die Zeilen der Einzelfälle (Symbol, Datum, Art) aus den Läufen an den zwei Kopien; ihr Unterschied sind genau diese Meldungen. An der zweiten Kopie enden `m1` und `m2` mit rc 1; der rc an der ersten Kopie ist kein Soll. Alle Ausgaben der vier Läufe samt rc stehen in `gegenprobe.txt`. Lädt der Kalender nicht, entfallen G2, G3 und das Soll für `m1`. `gegenprobe.txt` nennt je Eingriff nur Symbol, Datum und Art, keine Kurszeile; eine eingefügte Zeile trägt in den Kursspalten den Text `x`. Die Kopien bleiben in `$TMPDIR` und werden nicht committet. Meldet das Skript einen Eingriff nicht ⇒ das Skript berichtigen und die Gegenprobe wiederholen; erst danach laufen die Messungen.

### M1 — Bedingung aus R66 (b) für den Kalender „NYSE“, je Aktien-Bot (R74 (e); 54.6 Nr. 1)

Eingaben: die 150 Symbole aus `config/sp500_top150.txt` im Snapshot, je Symbol `<SYMBOL>_1d.csv`; der Kalender nach L6 in der Lock-Umgebung nach L2.

1. **K** = die Tage, an denen mindestens ein Symbol einen Kurs trägt (L5): erster Tag, letzter Tag, Anzahl.
2. **H** = die Sitzungstage vom ersten Tag aus K bis zum späteren von letztem Tag aus K und Ende nach L3: Anzahl.
3. Tabelle je Kalenderjahr: Zahl der Tage in H, Zahl der Tage in K, Tage nur in H (kein Symbol trägt einen Kurs), Tage nur in K (ein Kurs an einem Tag, der kein Handelstag ist), Symbol-Tage an Tagen, die kein Handelstag sind. Jede Abweichung einzeln mit Datum; bei „nur in K“ die Symbole, höchstens 20 je Tag, darüber die Anzahl.
4. Je Aktien-Bot für den Zeitraum vom Beginn (L4) bis zum Ende (L3), mit H über genau diesen Zeitraum: Zahl der Sitzungstage, Tage nur in H, Tage nur in K, Symbol-Tage an Tagen, die kein Handelstag sind; dazu der erste und der letzte Tag aus K gegen Beginn und Ende. **Urteil je Bot:** Die Bedingung aus R66 (b) ist erfüllt, wenn im Zeitraum kein Tag nur in H und kein Tag nur in K liegt; sonst ist sie nicht erfüllt. Dazu das früheste Jahr, ab dem das bis zum Ende gilt.
5. Zeilen, in denen `close` nach L5 fehlt: je Symbol die Anzahl, getrennt nach leerer Zelle und Fehlwert-Text, und die Einzelfälle mit Datum, höchstens 50 je Symbol, darüber nur die Anzahl (das Register führt sie als nicht gemessen, Z. 11494).
6. Verkürzte Sitzungen (L6): Zahl der Sitzungstage ab dem frühesten Beginn nach L4, deren Schluss laut `schedule` vor dem regulären Schluss liegt, und ob sie alle in H stehen; drei davon mit Datum. Wie der Kalender in der Fassung des Locks verkürzte Tage ausweist, ist vom Werkzeug abhängig: im Ergebnis beschreiben.

rc 1, wenn Nr. 4 bei einem Bot „nicht erfüllt“ ergibt. **Das ist ein Befund, kein Abbruch:** nennen und weitermessen.

### M2 — Reihenenden und Symbol-Tage Lücke (R72 (d); 53.10 Nr. 3), dazu 53.10 Nr. 10

Für beide Universumsdateien im Snapshot:

1. Je Zeile der Universumsdatei: welche Reihen im Snapshot liegen (`_1d`, bei Krypto auch `_1h` und `_4h`). Zeilen ohne `_1d`-Reihe und Reihen ohne Zeile in der Datei einzeln. Erwartet nach „Belegt“: nur `XAUTUSDT` ohne `_1d` und ohne `_4h`.
2. Der letzte Kurstag je Markt (L7, L9) und jede `_1d`-Reihe, die früher endet: Symbol und letzter Kurstag. Für `_1h` und `_4h` der Tag des letzten Zeitstempels je Reihe gegen den letzten Kurstag des Marktes; früher endende einzeln, ohne Urteil.
3. Symbol-Tage Lücke (L8) auf den `_1d`-Reihen: jede Lücke einzeln mit Symbol und Datum, dazu die Summe je Markt und je Kalenderjahr. Je Bot die Zahl im Zeitraum nach R66 (a): Aktien wie M1 Nr. 4; Krypto mit dem Beginn nach L4 und dem Ende nach L3. Getrennt und ohne Einzelliste: Symbol-Tage vor dem ersten Kurstag eines Symbols, gezählt ab dem ersten Tag aus K seines Marktes, je Kalenderjahr.
4. Zu 53.10 Nr. 10, je `_1d`-Reihe: Zahl der doppelten `open_time` (gleiche Zeichenkette), Zahl der doppelten Tage (gleiches Datum bei verschiedener Zeichenkette) und Zahl der `open_time` mit einem Zeitanteil, der nicht Mitternacht ist. Summen je Markt, Einzelfälle mit Symbol und Datum. `benchmark.py` wird nicht geändert (R72 (d)); die Zählung braucht die Datei nicht.

rc 1, wenn Nr. 2 eine früher endende `_1d`-Reihe zeigt (R72 (d): melden, vor dem Tag entscheiden). Lücken, doppelte Daten und Zeitanteile sind Zählungen ohne Urteil. Lässt sich der Kalender nicht laden, rechnet `m2` für Aktien die Tage K selbst (wie M1 Nr. 1) und nimmt sie anstelle von H; das heisst im Ergebnis „Ersatz“.

### M3 — Paketfassung des Kalenders (54.6 Nr. 8)

Nr. 1 misst das Messskript (`m3` ⇒ `m3.txt`). Nr. 2 bis Nr. 4 laufen in `docs/belege/TB-138/m3_shell.sh` ⇒ `m3_shell.txt`.

1. In `trading-env`: die Fassungen der vier Pakete aus dem Kopf gegen `requirements.lock` Z. 37, 50, 51, 52; dazu `__file__` von `pandas_market_calendars`. Soll: gleich dem Lock.
2. `trading-env/bin/python3 -B research/snapshotgrenze/erhebung_eingaben.py` **ohne** `--json`; in den Beleg nur die Zeile „Paketfassung hier“ (`grep`). Kein Soll; startet das Skript nicht, steht die Fehlermeldung im Beleg.
3. Für jeden Pfad aus `which -a python3 python3.9 python3.10 python3.11 python3.12 python3.13` (die Liste steht im Beleg): `<Pfad> -B -c "import sys, importlib.metadata as m; print(sys.version.split()[0], m.version('pandas_market_calendars'))"`. Ein Fehler heisst „nicht installiert“. Kein Soll (O3).
4. Nennt `docs/ERGEBNIS_TB-47_snapshotgrenze.md` oder die Commit-Nachricht von `fc38d25` den Interpreter des Laufs vom 18.09.2026? Fundstelle oder „nicht gefunden“. Autor und Zeit des Commits (oben unter „Belegt“) nennen, nicht deuten.

`eingaben.json` wird nicht neu erzeugt und nicht geändert. *Grund:* Die Datei ist ein Beleg von TB-47; was mit ihr geschieht, wird nach dem Ergebnis entschieden. rc 1, wenn Nr. 1 vom Lock abweicht.

Commit `TB-138 A: Messskript, Gegenprobe, M1–M3`, pushen (mit den Belegen aus 0a und 0b).

## Schritt B — BACKLOG (5b)

Eine Einfügung nach dem Verfahren aus TB-131 („Verfahren je Einfügung“, Nr. 1 bis 4, in `docs/auftraege/MAC_TB-131_regelwerk_nachtrag_ampel.md`), so wie TB-133 es für seine Blöcke E8 und E9 übernommen hat: Vorlagen `docs/belege/TB-133/einfuegen.py` und `docs/belege/TB-133/c3_vergleich.py`, nach `docs/belege/TB-138/` übernommen und umgestellt (Pfad dieses Auftrags, Belegordner, `BLOECKE` = `{"E1"}`, erwartete Nummernfolge E1, erwartete Anzahl 1, Kopfzeile der Ausgabedatei); Aufruf mit `trading-env/bin/python3 -B`. Genau eine Leerzeile vor und nach dem Block; eine vorhandene wird nicht verdoppelt. Ergebnis in `docs/belege/TB-138/einfuegungen.txt`, Zeichengleichheit in `c3_vergleich.txt`. Vorgezählt vom steuernden Chat am 06.10.2026 am HEAD `0c70853`: Anker 1 (Z. 306 von 317), erste Zeile des neuen Texts 0. Die Sitzung zählt selbst nach; ihre Zahl gilt. Anker ≠ 1 ⇒ nicht einfügen, nennen.

#### E1 — BACKLOG, Abschnitt 5: Abnahme TB-133 und TB-138

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile**

```
### Aus der Abnahme TB-133 (06.10.2026) und aus TB-138 — eingetragen mit TB-138

- **TB-133 abgenommen** am 06.10.2026 vom steuernden Chat: zehn Prüfungen, keine Abweichung gegen ein Soll. Zwei Befunde aus der Abnahme gehen in den nächsten Regelwerk-Nachtrag (`UEBERGABE.md`, Nachtrag 06.10.2026, 10:51).
- **TB-138:** Verfahrensmessung am Snapshot nach Register 54.6 Nr. 1 und Nr. 8 und 53.10 Nr. 3 und Nr. 10; Ausgang und Befunde stehen in `docs/ERGEBNIS_TB-138_verfahrensmessung_snapshot.md`. Der Stand zu R74 (e) in Register 54.5 wird erst nach einer Einzelfreigabe des Betreibers eingetragen.
- **Offen danach:** der Regelwerk-Nachtrag (nächste Nummer nach TB-138), die Abnahme von TB-137, die nächste Anfrage an Fable.
```

Commit `TB-138 B: BACKLOG`, pushen.

## Schritt D — Abgabe

D0. 0b wiederholen ⇒ `docs/belege/TB-138/0b_nachher.txt`. Soll: gleich wie `0b_ausgang.txt` bis auf HEAD. Ist ein anderer Wert anders ⇒ melden (Abbruchkriterium).

D1. `docs/ERGEBNIS_TB-138_verfahrensmessung_snapshot.md`: Kopf, Stand und Commits; Kurz-Tabelle (0a, 0b, Gegenprobe, M1, M2, M3, B, D0, je Soll und Ist); je Messung die Tabellen und die Einzelfälle; „Lesarten L1–L9 und offene Punkte O1–O4: woran welche Aussage hängt“; „Für das Register“ (die Tatsachen zu 54.5, Zeile R74 (54.1) (e), zu 53.10 Nr. 3 und Nr. 10 und zu 54.6 Nr. 1 und Nr. 8 als Sätze mit Fundstelle im Beleg, ohne Urteil über das Verfahren); „Für Fable“ (offene Fragen); „Nicht getan“; „In einfacher Sprache“. Keine Kurse, keine Kennzahlen.

D2. Journalblock nach dem letzten Buchstabenblock von `docs/projektfuehrung/JOURNAL.md`, vor `## Wiederkehrende Lehren`; Kennung messen (erwartet **EG**), mit Quellenzeile; verankern an der Zeichenfolge `\n---\n\n## Wiederkehrende Lehren\n` (sie steht in `JOURNAL.md` genau einmal; die Worte „Wiederkehrende Lehren“ stehen in drei Zeilen). Der Block nennt auch die Abnahme von TB-133 mit dem Wortlaut des ersten Spiegelstrichs aus E1.

D3. Abgabe-Commit `TB-138 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Danach `git diff --numstat ⟨S0⟩ HEAD` ⇒ `docs/belege/TB-138/d3_numstat.txt` (Soll: nur Pfade unter `docs/belege/TB-138/`, dazu `docs/ERGEBNIS_TB-138_verfahrensmessung_snapshot.md`, `docs/projektfuehrung/JOURNAL.md` ohne entfernte Zeile und `docs/projektfuehrung/BACKLOG.md` mit `6	0`: fünf Zeilen Block, eine Leerzeile) und `git status --porcelain` nach `$TMPDIR` und von dort als `docs/belege/TB-138/d3_porcelain.txt` (Soll: keine Zeile); kleiner letzter Commit, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab.
- `trading-env/bin/python3` startet nicht (0b).
- `shared/snapshot.py --pruefen` endet mit Ausgang 1 oder 2.
- Eine Messung verlangte, eine Ergebnisgrösse des Selektionsraums zu lesen oder zu rechnen, oder sie ginge nur mit einer Änderung ausserhalb der genannten Pfade.
- Ein Wert aus 0b ist in D0 anders (ausser HEAD).
- `git push` scheitert zweimal.

**Kein Abbruch:** jeder Befund aus M1, M2 und M3 · der Kalender lässt sich in `trading-env` nicht laden (M1 heisst dann „nicht gemessen“, M2 läuft mit „Ersatz“, M3 so weit wie möglich) · rc 2 einer Messung · ein Register, ein Abbild oder eine Universumsdatei mit anderem Hash · der BACKLOG-Anker ≠ 1.

Bei Abbruch nach dem Commit von Schritt 0: committen, was an Belegen da ist, Grund in `docs/belege/TB-138/abbruch.txt`, pushen, melden. Nie `JOURNAL.md` mit Platzhalter.

## In einfacher Sprache

Vor dem grossen Rechenlauf muss feststehen, dass der Börsenkalender und die eingefrorenen Kursdaten zusammenpassen. Dieser Auftrag prüft das und ändert nichts. Erstens: Hat an jedem Handelstag des Kalenders „NYSE“ mindestens eine der 150 Aktien einen Kurs, und hat keine Aktie einen Kurs an einem Tag, der kein Handelstag ist? Zweitens: Reichen alle Kursreihen bis zum selben letzten Tag, und wie viele einzelne Tage fehlen in den Reihen? Drittens: Warum nennt eine ältere Messdatei für das Kalenderpaket die Fassung 5.4.0, obwohl 4.6.1 festgeschrieben ist? Heraus kommen nur Tage und Zählungen, keine Kurse und keine Ergebnisse der Strategien. Zeigt sich eine Abweichung, wird sie gemeldet und vor dem Tag entschieden.
