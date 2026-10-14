# TB-161 S-B1-Datenlauf: 14 ETF-Reihen holen, Historie messen, Datenstand vorher/nachher — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 14.10.2026, 20:04** (Helfer BAU161, per Skript aus Bausteinen, `$HOME/sc/tb161/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; an einer Kopie simuliert. Urteil und Freigabe liegen beim steuernden Chat; ein frischer Gegenleser ist Pflicht (F8). **Gebaut am HEAD `4979589`.**

**Sitzungstitel:** `TB-161` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `4979589a50a21ec7782a8308d5770cb365a406fc` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-161`), nicht von Hand.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-161_sb1_datenlauf.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9), kurz `PY`; das Werkzeug `docs/belege/TB-161/tb161_werkzeug.py` (Anhang B) kurz `WZ`. **Belege:** `docs/belege/TB-161/`. **Ergebnis:** `docs/ERGEBNIS_TB-161_sb1_datenlauf.md`. **Journal:** die nächste freie Kennung zur Laufzeit (`PY WZ kennung`, Schritt E), unten `<Kennung>`; am Bau-HEAD höchste EV ⇒ EW.
**Ziel:** Die offenen Schritte 2–9 aus `docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md` (16.09.2026) am **aktuellen `main`** ausführen (F1): Datenstand vorher, Selbsttest, Datenlauf (der einzige Netzschritt), `historie.py`, `raster.py`, `kosten.py`, Selbsttest nachher, Datenstand nachher. Die Frage dahinter (Testauftrag Z. 151–153): **Reicht die Historie ab 2007 für acht Instrumente über vier Anlageklassen?** Grundlage: Betreiberkarte 13.10.2026, 22:34 („Handel zuerst“ … „parallel die Vorbereitung für den ETF-Bot“); BACKLOG Rang 4 (Z. 149: „Vorbereitung … **kann parallel laufen**; der Backtest erst nach Rang 1“).
**Bauart:** Messlauf ohne Code-Änderung, Mac-Auftrag nach ARBEITSWEISE 7c; Schritt 0, Abbruchweg, Abgabe und Anhang „Dateien und ihre Befehle“ wie `MAC_TB-159_agenten_aus.md`. Die Befehle der Schritte 2–9 sind **per Skript aus dem Testauftrag umgeschrieben** (je mit Quellzeile): ohne `cd ~/trading-bot &&` (die Sitzung steht im Repo), `python3` ⇒ `PY`, `~/Downloads/TB-39_sb1_vorbereitung/` ⇒ `docs/belege/TB-161/`, `| tee DATEI` ⇒ `> DATEI 2>&1; echo "rc $?" >> DATEI`. Bei Widerspruch gilt dieser Auftrag; es gelten nur die Schritte, die hier stehen.
**ARBEITSWEISE 7c — wo es hier steht:** Sicherung der `*.db` 0c · Datenstand vorher/nachher Schritt 2 und 9 (Sollwert `d9449faf…`, dasselbe Verfahren) · Interpreter `PY` in jedem Befehl · Abbruchkriterien nur für den Gegenstand · `git status --porcelain` nach dem letzten Commit (Abgabe) · Commit und Push nach jedem fertigen Teil (⟨S0⟩, ⟨M⟩, ⟨F⟩), Belege unter `docs/belege/TB-161/` · „In einfacher Sprache“ (Ergebnis und unten). Ein Basislauf der Bestandstests entfällt: kein Code wird geändert.
**Zeitgrenze:** jeder Bash-Aufruf mit dem Parameter `timeout` des Bash-Werkzeugs, 600000 ms (nicht der Shell-Befehl `timeout`); jeder Befehl der Schritte 2–9 in einem eigenen Aufruf.

## ⭐ Freigabe und Grenzen

**Betreiber 13.10.2026, 22:34:** „Handel zuerst“ … „parallel die Vorbereitung für den ETF-Bot“. Steuernder Chat 14.10.2026, 18:18: Entscheide F1–F8.

**Verboten (F2; Register S-B1 Abschnitt 11, Befund B3):** Backtest, Ertrags- oder Sharpe-Zahlen, Messung von w, Parametersuche, Auswahl nach Ergebnis; **Schreiben unter `data/`**; die Kandidatenliste ändern (`research/etf_trendfolge/register.py`); eine Vol-Grenze aus den geladenen Reihen ableiten. Erscheint irgendwo eine Ertragszahl, ist sie ein **Befund**, kein Ergebnis (Testauftrag Z. 29–30). Kein Programm des Repos ausser den hier genannten; kein `pip`, kein `brew` (beide in `deny`), keine Installation auf anderem Weg (F6).

**Die Sitzung darf schreiben, und nichts sonst:**

| Ziel | was | gitignoriert? |
|---|---|---|
| `research/etf_trendfolge/daten/` (14 × `<SYMBOL>_1d.csv`, `manifest.json`) | nur `datenlauf.py` (Schritt 4) | **ja** (`research/etf_trendfolge/.gitignore` Z. 8 `daten/`) — nie committen, nie `git add -f` |
| `docs/belege/TB-161/…` | Belege, Werkzeug, Ergebnis-JSON (`05_historie.json` u. a.) | nein — committen (F3) |
| `docs/projektfuehrung/BACKLOG.md` | `PY WZ backlog`: Vermerk an Rang 4 (Z. 149) und K15 (Z. 63) | nein |
| `docs/projektfuehrung/JOURNAL.md` | `PY WZ journal` | nein |
| `docs/ERGEBNIS_TB-161_sb1_datenlauf.md` | Schreibwerkzeug | nein |

**Das Manifest bleibt in `daten/`** (gitignoriert; F3 „soweit nicht gitignoriert“); ins Repo kommt seine Abschrift `04_manifest.txt` (sha256 der Datei und je Symbol erstes/letztes Datum, Grösse, sha256), erzeugt von `PY WZ manifest`.
**Nicht erlaubt:** jede Datei unter `data/`, `research/etf_trendfolge/*.py`, `research/etf_trendfolge/ergebnisse/`, `config/`, `shared/`, `strategies/`; `UEBERGABE.md` und `EROEFFNUNG_STEUERNDER_CHAT.md` nach Schritt 0.

## Lage nach dem Auslegen

Am Bau-HEAD `4979589` gemessen (`git ls-files -m` und `-o --exclude-standard`): geändert `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, `docs/projektfuehrung/UEBERGABE.md`; unverfolgt: nichts. Das Auslegen ändert dazu den Zeiger in `docs/auftraege/AKTUELLER_AUFTRAG.md` und legt diesen Auftrag ab. **Beim Start liegen genau 4 Einträge vor** (Soll in 0a).

## Belegt · erschlossen · offen

**Belegt (am Bau-HEAD):** `research/etf_trendfolge/daten/` gibt es nicht (ls); `ergebnisse/` enthält nur `datenstand_vorher.json`, `kosten.json`, `raster.json`. `datenlauf.py` holt über yfinance (Z. 126, `auto_adjust=True`), überschreibt vorhandene Dateien nicht und schreibt `daten/manifest.json`; seine Wache bricht ab, wenn das Ziel unter `data/` liegt. `historie.py` gibt 1 zurück, wenn die Untergrenze (8 Instrumente / 4 Klassen am Stichtag) fällt (Z. 285). Im Mount liegen `trading-env/lib/python3.9/site-packages/yfinance` (1.2.0, Ordner vom 31.08.2026), `pandas` (2.3.3) und `pandas_market_calendars` (4.6.1). `requirements.txt` nennt yfinance **nicht** (Testauftrag Z. 37 sagt es).
**Widerspruch zu F6:** F6 meldet „yfinance fehlt in trading-env (gemessen 14.10.2026, 18:18)“; der Mount zeigt das Paket. Darum prüft 0d den Import; scheitert er, **Abbruch vor dem Netz** — Installation ist nicht freigegeben; die Sitzung installiert nichts, auf keinem Weg (auch nicht `trading-env/bin/pip`, `python -m pip`) — F6.
**Erschlossen:** Der Selbsttest nutzt Wegwerf-Ordner (`tempfile`) und darf sich durch die echten Kursdateien nicht ändern (Testauftrag Z. 230–232).
**Offen (nur am Mac messbar):** ob `import yfinance` unter Python 3.9 gelingt; ob Yahoo antwortet und alle 14 Symbole liefert; die gemessenen ersten Daten und damit rc von `historie.py`; Laufzeit von Schritt 4 (Testauftrag Z. 39: „rund 15 Minuten“); ob der Datenstand-Hash am Mac dem Sollwert entspricht.

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-161/` entsteht:** `git status --porcelain > "$TMPDIR/tb161_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD `4979589a50a21ec7782a8308d5770cb365a406fc` und genau diese 4 Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-161_sb1_datenlauf.md
```

Dann das Werkzeug aus Anhang B holen (genau dieser Befehl):

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-161_sb1_datenlauf.md "$TMPDIR/tb161_werkzeug.py" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
a = z.index("```python", z.index("### Werkzeug"))
t = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
open(sys.argv[2], "w", encoding="utf-8").write(t)
print("tb161_werkzeug.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: `tb161_werkzeug.py 979d8e839a1fa9954af720b726ac03902b1d617dcd8c7f399d7d870d0c74e4fa`; sonst **ABBRUCH**. Commit `TB-161 Schritt 0: Stand des steuernden Chats vor TB-161` mit genau den Pfaden aus 0a (Block unten), pushen ⇒ **⟨S0⟩**. **Unmittelbar nach dem gepushten ⟨S0⟩:** `mkdir -p docs/belege/TB-161`; erst ab hier gibt es `abbruch.txt`. Dann `cp "$TMPDIR/tb161_0a.txt" docs/belege/TB-161/0a_status.txt` und `cp "$TMPDIR/tb161_werkzeug.py" docs/belege/TB-161/tb161_werkzeug.py` (je `cmp` gleich).

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
git add docs/projektfuehrung/UEBERGABE.md
git add docs/auftraege/MAC_TB-161_sb1_datenlauf.md
```

**0b. Ausgang** ⇒ `0b_ausgang.txt`, Befehl:

```
{ wc -l docs/projektfuehrung/BACKLOG.md docs/projektfuehrung/JOURNAL.md; md5 docs/projektfuehrung/BACKLOG.md docs/projektfuehrung/JOURNAL.md; ls -a research/etf_trendfolge research/etf_trendfolge/ergebnisse; } > docs/belege/TB-161/0b_ausgang.txt
```

Soll (am Bau-HEAD): `BACKLOG.md` 498 Z., `223c696f1fa0ad418939a06931d5a3f3` · `JOURNAL.md` 10999 Z., `e37e0af3c5b8fa9bb74bf68d1a0f4217`; in `research/etf_trendfolge` **kein** `daten`. Weicht eine Zahl ab: vermerken. Liegt `daten/` schon da: **ABBRUCH** (der Lauf überschriebe nichts; gemessen würde ein fremder Bestand).

**0c. Sicherung der `*.db`** (7c; nur lesen), genau diese drei Befehle: `mkdir -p "$TMPDIR/tb161_db"`, `cp -p paper_trading_*.db "$TMPDIR/tb161_db/"`, `md5 paper_trading_*.db "$TMPDIR"/tb161_db/paper_trading_*.db > docs/belege/TB-161/0c_db_sicherung.txt`. Soll: je Datenbank zwei gleiche md5. Ungleich (ein Cronjob schrieb): Befund, kein Abbruch; scheitert ein Befehl: **ABBRUCH**.

## Schritt 2 — Datenstand vorher (Stopp vor dem Netz)

Quelle Testauftrag Z. 70. Befehl:

```
trading-env/bin/python3 -B research/etf_trendfolge/datenstand.py --json docs/belege/TB-161/02_datenstand_vorher.json > docs/belege/TB-161/02_datenstand_vorher.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/02_datenstand_vorher.txt
```

Soll (Testauftrag Z. 76–78, wörtlich), danach `rc 0`:

```
  Ist    d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84  (223 Dateien)
  Soll   d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84  (223 Dateien)
  unveraendert
```

und `liegt ausserhalb von data/ - richtig so.` **Weicht Hash oder Dateizahl ab oder ist rc ≠ 0: ABBRUCH vor dem Netz** (F5) — Schritt 4 läuft dann nicht. Die getrennte rc-Prüfung des Testauftrags (Z. 90) entfällt: `rc` steht in der Belegdatei.

**0d. Umgebung (vor dem Netz, F6)** ⇒ `0d_umgebung.txt`, genau diese zwei Befehle:

```
trading-env/bin/python3 -B -c "import yfinance, pandas; print('yfinance', yfinance.__version__, 'pandas', pandas.__version__)" > docs/belege/TB-161/0d_umgebung.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/0d_umgebung.txt
trading-env/bin/python3 -B -c "import pandas_market_calendars as m; print('pandas_market_calendars', m.__version__)" >> docs/belege/TB-161/0d_umgebung.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/0d_umgebung.txt
```

Soll: erste Zeile `yfinance 1.2.0 pandas 2.3.3` (am Bau im Mount), dahinter `rc 0`. **Erstes rc ≠ 0: ABBRUCH vor dem Netz** — nichts installieren, keinen Ersatzweg suchen, den Wortlaut der Fehlermeldung melden. Das zweite rc ≠ 0 ist kein Abbruch: dann verwirft Schritt 4 mehr als nötig (Testauftrag Z. 137); Befund.

## Schritt 3 — Selbsttest vorher

Quelle Z. 104. Befehl:

```
trading-env/bin/python3 -B research/etf_trendfolge/test_etf_trendfolge.py > docs/belege/TB-161/03_selbsttest.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/03_selbsttest.txt
```

Soll: vorletzte Zeile `64/64 Pruefungen bestanden.` (Testauftrag Z. 107), dann `rc 0`. **Sonst ABBRUCH** (F5: Testfehler) — vor dem Netz.

## Schritt 4 — Datenlauf (der einzige Schritt ins Netz)

Quelle Z. 121. Befehl (Bash-Zeitgrenze 600000 ms):

```
trading-env/bin/python3 -B research/etf_trendfolge/datenlauf.py > docs/belege/TB-161/04_datenlauf.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/04_datenlauf.txt
```

Soll: vierzehn Zeilen `… Handelstage (… unvollstaendig, … nach der Entscheidungskerze verworfen)`, dann `Manifest: …/daten/manifest.json`, dann `rc 0`. „verworfen“ grösser als 1 ist ein **Befund** (Testauftrag Z. 136), kein Abbruch. **rc ≠ 0 oder Zeitgrenze: ABBRUCH** — nicht wiederholen; ein Symbol ohne Daten ist ein Befund für den Betreiber, **die Kandidatenliste ändert die Sitzung nicht** (F2). Bereits geholte Dateien bleiben in `daten/` liegen (gitignoriert; nicht löschen, nicht committen).
Danach die Abschrift des Manifests:

```
trading-env/bin/python3 -B docs/belege/TB-161/tb161_werkzeug.py manifest docs/belege/TB-161/04_manifest.txt; echo "rc $?" >> docs/belege/TB-161/04_manifest.txt
```

Soll: „Kursdateien (*.csv) in research/etf_trendfolge/daten: 14 · Eintraege im Manifest: 14 · davon vorhanden: 14“, `rc 0`; sonst **ABBRUCH**.

## Schritt 5 — Historie (die Antwort)

Quelle Z. 148. Befehl:

```
trading-env/bin/python3 -B research/etf_trendfolge/historie.py --json docs/belege/TB-161/05_historie.json > docs/belege/TB-161/05_historie.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/05_historie.txt
```

Soll: Tabelle mit vierzehn Zeilen, Block „Untergrenze am …“, Jahrestabelle; dann **`rc 0` oder `rc 1` — beides ist ein Ergebnis** (F5; Testauftrag Z. 172): 0 = Untergrenze erfüllt, 1 = nicht erfüllt. Bei `rc 1` weiter; ob später angefangen wird oder eine Klasse wegfällt, **entscheidet der Betreiber**, nicht die Sitzung. Jedes andere rc (Ausnahme, Zeitgrenze): **ABBRUCH**. „Abweichungen zur Erwartung“ und tragende Selektionsfalten unter 3 sind Befunde fürs Ergebnis (Testauftrag Z. 182), kein Abbruch. Die getrennte rc-Prüfung (Z. 166) entfällt.

## Schritt 6 und 7 — Raster und Kosten (brauchen keine Daten)

Quelle Z. 189 und Z. 207. Befehle:

```
trading-env/bin/python3 -B research/etf_trendfolge/raster.py --was-waere-wenn --json docs/belege/TB-161/06_raster.json > docs/belege/TB-161/06_raster.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/06_raster.txt
trading-env/bin/python3 -B research/etf_trendfolge/kosten.py --json docs/belege/TB-161/07_kosten.json > docs/belege/TB-161/07_kosten.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/07_kosten.txt
```

Soll Raster (Testauftrag Z. 195–197): `N                  5` · `N_historisch       653  (Neuselektion, Vorregistrierung Abschnitt 9)` · `N gesamt, nominal  658`; Soll Kosten (Z. 213–214): `Obere Schranke (jeden Monat kippt alles): 1.80 Prozentpunkte je Jahr` · `Massstab, ein VOLLER Round Trip je Monat:  3.60 Prozentpunkte je Jahr`; je `rc 0`. Abweichende Zahl: Befund. rc ≠ 0: **ABBRUCH**. Die Tabelle von `kosten.py` rechnet mit einem **angenommenen** Bruttoertrag (kosten.py Z. 52–53, 124); sie ist keine gemessene Ertragszahl und kein Befund nach Z. 16.

## Schritt 8 — Selbsttest nachher

Quelle Z. 225. Befehl:

```
trading-env/bin/python3 -B research/etf_trendfolge/test_etf_trendfolge.py > docs/belege/TB-161/08_selbsttest_nachher.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/08_selbsttest_nachher.txt
```

Soll wie Schritt 3. **Sonst ABBRUCH** (F5).

## Schritt 9 — Datenstand nachher und Gegenproben

Quellen Z. 239, 248, 256, 273. Befehle:

```
trading-env/bin/python3 -B research/etf_trendfolge/datenstand.py --json docs/belege/TB-161/09_datenstand_nachher.json > docs/belege/TB-161/09_datenstand_nachher.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/09_datenstand_nachher.txt
{ diff <(grep Ist docs/belege/TB-161/02_datenstand_vorher.txt) <(grep Ist docs/belege/TB-161/09_datenstand_nachher.txt) && echo "IDENTISCH" || echo "ABWEICHUNG - BEFUND"; } > docs/belege/TB-161/09_vergleich.txt 2>&1
git status --porcelain data/ > docs/belege/TB-161/09_git_data.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/09_git_data.txt
ls research/etf_trendfolge/daten/ | wc -l > docs/belege/TB-161/10_dateizahl.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/10_dateizahl.txt
```

Soll: `09_datenstand_nachher.txt` wie in Schritt 2; `09_vergleich.txt` = `IDENTISCH`; `09_git_data.txt` = nur `rc 0` (keine Statuszeile unter `data/`); `10_dateizahl.txt` = `15`, `rc 0` (Testauftrag Z. 276; `wc -l` rückt die Zahl am Mac ein). **`ABWEICHUNG - BEFUND` oder eine Statuszeile in `09_git_data.txt`: ABBRUCH** — das ist der wichtigste Befund (Testauftrag Z. 18–21). Eine andere Dateizahl: Befund.

**Commit ⟨M⟩** `TB-161 M: Datenstand, Datenlauf, Historie` (Block), pushen.

```
git add docs/belege/TB-161/0a_status.txt
git add docs/belege/TB-161/tb161_werkzeug.py
git add docs/belege/TB-161/0b_ausgang.txt
git add docs/belege/TB-161/0c_db_sicherung.txt
git add docs/belege/TB-161/02_datenstand_vorher.json
git add docs/belege/TB-161/02_datenstand_vorher.txt
git add docs/belege/TB-161/0d_umgebung.txt
git add docs/belege/TB-161/03_selbsttest.txt
git add docs/belege/TB-161/04_datenlauf.txt
git add docs/belege/TB-161/04_manifest.txt
git add docs/belege/TB-161/05_historie.json
git add docs/belege/TB-161/05_historie.txt
git add docs/belege/TB-161/06_raster.json
git add docs/belege/TB-161/06_raster.txt
git add docs/belege/TB-161/07_kosten.json
git add docs/belege/TB-161/07_kosten.txt
git add docs/belege/TB-161/08_selbsttest_nachher.txt
git add docs/belege/TB-161/09_datenstand_nachher.json
git add docs/belege/TB-161/09_datenstand_nachher.txt
git add docs/belege/TB-161/09_vergleich.txt
git add docs/belege/TB-161/09_git_data.txt
git add docs/belege/TB-161/10_dateizahl.txt
```

## Schritt E — Backlog, Journal, Ergebnis, Abgabe

**Backlog** (F3), genau diese zwei Befehle nacheinander:

```
trading-env/bin/python3 -B docs/belege/TB-161/tb161_werkzeug.py backlog --probe > docs/belege/TB-161/e_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/e_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-161/tb161_werkzeug.py backlog > docs/belege/TB-161/e_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/e_backlog.txt
```

Soll je: vier `ja`, `rc 0`. Endet die Probe nicht mit `rc 0`: den zweiten Befehl nicht ausführen, **ABBRUCH**. Danach endet Rang 4 (Z. 149) auf „| vorbereiten · Datenlauf TB-161: `docs/ERGEBNIS_TB-161_sb1_datenlauf.md`; UCITS-Paare (Register S-B1 10a) offen |“, und K15 (Z. 63) beginnt mit „| **K15** | **Vermerk TB-161: durch TB-41 erledigt, Paare offen** (Register `docs/VORREGISTRIERUNG_neuselektion.md` 16.9 (b), Commit `1bc2d57`; Proxy-Tabelle Register S-B1 10a.4 leer). …“ (Wortlaute in Anhang B, `R4_NEU`, `K15_NEU`).

**Journal.** Zuerst:

```
trading-env/bin/python3 -B docs/belege/TB-161/tb161_werkzeug.py kennung docs/belege/TB-161/e_kennung.txt; echo "rc $?" >> docs/belege/TB-161/e_kennung.txt
```

Soll „Kennung EW …“, `rc 0` (weicht HEAD ab, bricht schon 0a ab). Dann schreibt die Sitzung ihren Block nach `docs/belege/TB-161/e_block.md` (Schreibwerkzeug, Gliederung Anhang C), dann genau diese zwei Befehle nacheinander:

```
trading-env/bin/python3 -B docs/belege/TB-161/tb161_werkzeug.py journal docs/belege/TB-161/e_block.md --probe > docs/belege/TB-161/e_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/e_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-161/tb161_werkzeug.py journal docs/belege/TB-161/e_block.md > docs/belege/TB-161/e_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-161/e_journal.txt
```

Soll je: sechs `ja`, `rc 0`; endet die Probe nicht mit `rc 0`: den zweiten nicht ausführen, **ABBRUCH**.

**Ergebnis** `docs/ERGEBNIS_TB-161_sb1_datenlauf.md` (Schreibwerkzeug): Kopf (Stand, Commits ⟨S0⟩, ⟨M⟩) · „Kurz“: die Ergebnistabelle des Testauftrags (Z. 325–343) mit Spalte „beobachtet“ (Zeile 1 = 0a; Zeile 10 = `f_porcelain.txt`; Zeile 11 „nicht Teil von TB-161“) · „Historie“: die vierzehn Zeilen, Untergrenze, rc, tragende Falten, Abweichungen zur Erwartung — wörtlich aus `05_historie.txt` · „Manifest“: aus `04_manifest.txt` · „Datenstand“: vorher, nachher, Vergleich · „Belege“ (Datei · Befehl · Bytes · md5) · „Abweichungen“ · „Offen“: **UCITS-Paare** (Register S-B1 Abschnitt 10a; brauchen die Zulassung je Instrument durch den Betreiber; nicht Teil, F4), Backtest erst nach Rang 1 · **„In einfacher Sprache“**. **Keine** Ertrags- oder Sharpe-Zahl, keine Deutung der Reihen über die Historie hinaus (F2).

**Abgabe.** Commit `TB-161 Abgabe: Ergebnis, Backlog, Journal <Kennung>` (erster Block), pushen ⇒ **⟨F⟩**. Dann `git status --porcelain > "$TMPDIR/tb161_f.txt"`, `cp "$TMPDIR/tb161_f.txt" docs/belege/TB-161/f_porcelain.txt` (`cmp` gleich; Soll 0 B — `daten/` ist gitignoriert und erscheint nicht), erst danach `git diff --numstat ⟨S0⟩ ⟨F⟩ > docs/belege/TB-161/f_numstat.txt`. Commit `TB-161 F: porcelain und numstat nach der Abgabe` (zweiter Block), pushen. Zuletzt `git status --porcelain` im Chat melden (Soll leer).

```
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/ERGEBNIS_TB-161_sb1_datenlauf.md
git add docs/belege/TB-161/e_backlog_probe.txt
git add docs/belege/TB-161/e_backlog.txt
git add docs/belege/TB-161/e_kennung.txt
git add docs/belege/TB-161/e_block.md
git add docs/belege/TB-161/e_journal_probe.txt
git add docs/belege/TB-161/e_journal.txt
```

```
git add docs/belege/TB-161/f_porcelain.txt
git add docs/belege/TB-161/f_numstat.txt
```

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD), der sha256 des Werkzeugs weicht ab; 0b findet `daten/` schon vor; ein Befehl in 0c scheitert.
- Schritt 2: Hash, Dateizahl oder rc weichen ab (**Stopp vor dem Netz**, F5). 0d: `import yfinance, pandas` scheitert (F6, Stopp vor dem Netz).
- Schritt 3 oder 8: Selbsttest nicht vollständig bestanden oder rc ≠ 0 (F5).
- Schritt 4: rc ≠ 0 oder Zeitgrenze; `WZ manifest` rc ≠ 0 oder Soll-Zeile weicht ab. Schritt 5: rc ausser 0 und 1. Schritt 6/7: rc ≠ 0.
- Schritt 9: `ABWEICHUNG - BEFUND` oder eine Statuszeile unter `data/`.
- Schritt E: `kennung`, `backlog --probe`, `backlog`, `journal … --probe` oder `journal` endet nicht mit `rc 0`.
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung:** melden, nicht umgehen; verlangt schon Schritt 0 oder der Abbruchweg eine Bestätigung: nichts weiter versuchen, den Wortlaut der Frage melden.
- `git push` scheitert zweimal (gilt **nicht** für den Push des Abbruch-Commits).

**Kein Abbruch:** `historie.py` rc 1 (Ergebnis, F5); 0b-Zahlen weichen ab; md5 der `*.db` in 0c ungleich; „verworfen“ > 1; Abweichungen zur Erwartung; tragende Falten < 3; Raster- oder Kostenzahl weicht ab; `f_numstat.txt` oder `f_porcelain.txt` weichen ab — je weiter, unter „Abweichungen“ im Ergebnis.

**Abbruchweg — so wenig schreiben wie möglich** (wie TB-158/159, Karte 14.10.2026, 06:43). **Solange ⟨S0⟩ nicht gepusht ist:** nichts schreiben, nichts committen, nur im Chat melden (die Abweichung wörtlich). **Ab dem gepushten ⟨S0⟩:** genau eine neue Datei, `printf '%s\n' "<Schritt>: <Grund, ein Satz>" > docs/belege/TB-161/abbruch.txt`; dann `git add docs/belege/TB-161/abbruch.txt` und je eine Zeile `git add <Pfad>` **mit dem Namen** jeder Datei aus dem Anhang „Dateien und ihre Befehle“, die schon entstanden oder geändert und noch nicht committet ist (nie etwas unter `research/etf_trendfolge/daten/`, nie `git add -f`, nie `git add -A`). Commit `TB-161 Abbruch: <Schritt>`, pushen, melden. **Scheitert Commit oder Push des Abbruch-Commits: nicht wiederholen, kein Ersatzbefehl, anhalten, nur melden.** Nichts zurückdrehen (kein `git reset`, `revert`, `restore`, `checkout`); `daten/` und die Dateien unter `$TMPDIR` bleiben liegen (`deny`: `Bash(rm:*)`).

## Nicht in TB-161

- **UCITS-Paare** (Register S-B1 10a, Proxy-Tabelle 10a.4 leer): Kurse, Korrelation, Zulassung je Instrument — braucht den Betreiber (F4); im Ergebnis nur als offener Punkt.
- Backtest und alles aus F2; die Bestandstests aus Testauftrag Schritt 11 und die ZIP aus Schritt 12; Schritt 1 (Zweig `claude/new-session-s2jhcc`; F1: es gilt `main`).
- Jede Installation (F6); `.env`, Schlüssel, Cron, Handel.

## In einfacher Sprache

Der ETF-Bot soll Trends über vierzehn Wertpapierkörbe aus mehreren Bereichen folgen. Bevor er gebaut wird, muss feststehen, ob die Kurse weit genug zurückreichen — bis 2007, damit die Finanzkrise 2008 dabei ist. Diese Sitzung holt die Kurse einmal von Yahoo, legt sie in einen Ordner, der nicht ins Repo kommt, und misst, wie weit jede Reihe zurückgeht. Vorher und nachher prüft sie, dass der Kursordner der Aktien-Bots (`data/`) unberührt bleibt. Sie rechnet **keinen** Gewinn aus. Kommt heraus, dass es nicht reicht, ist das ein Ergebnis — dann entscheidest du, wie es weitergeht.

## Anhang — Dateien und ihre Befehle

| Datei | Befehl |
|---|---|
| `docs/belege/TB-161/0a_status.txt` | `git status --porcelain > "$TMPDIR/tb161_0a.txt"`, nach ⟨S0⟩ `cp` (0a) |
| `docs/belege/TB-161/tb161_werkzeug.py` | Holbefehl (0a) nach `$TMPDIR`, nach ⟨S0⟩ `cp` |
| `docs/belege/TB-161/0b_ausgang.txt` | Block 0b |
| `docs/belege/TB-161/0c_db_sicherung.txt` | `md5 …` (0c) |
| `docs/belege/TB-161/02_datenstand_vorher.json` | Befehl Schritt 2 |
| `docs/belege/TB-161/02_datenstand_vorher.txt` | Befehl Schritt 2 |
| `docs/belege/TB-161/0d_umgebung.txt` | zwei Befehle 0d |
| `docs/belege/TB-161/03_selbsttest.txt` | Schritt 3 |
| `docs/belege/TB-161/04_datenlauf.txt` | Schritt 4 |
| `docs/belege/TB-161/04_manifest.txt` | `PY WZ manifest` (Schritt 4) |
| `docs/belege/TB-161/05_historie.json` | Schritt 5 |
| `docs/belege/TB-161/05_historie.txt` | Schritt 5 |
| `docs/belege/TB-161/06_raster.json` | Schritt 6 |
| `docs/belege/TB-161/06_raster.txt` | Schritt 6 |
| `docs/belege/TB-161/07_kosten.json` | Schritt 7 |
| `docs/belege/TB-161/07_kosten.txt` | Schritt 7 |
| `docs/belege/TB-161/08_selbsttest_nachher.txt` | Schritt 8 |
| `docs/belege/TB-161/09_datenstand_nachher.json` | Schritt 9 |
| `docs/belege/TB-161/09_datenstand_nachher.txt` | Schritt 9 |
| `docs/belege/TB-161/09_vergleich.txt` | Schritt 9 (`diff`) |
| `docs/belege/TB-161/09_git_data.txt` | Schritt 9 (`git status --porcelain data/`) |
| `docs/belege/TB-161/10_dateizahl.txt` | Schritt 9 (`ls … | wc -l`) |
| `docs/projektfuehrung/BACKLOG.md` | `PY WZ backlog` (Schritt E) |
| `docs/projektfuehrung/JOURNAL.md` | `PY WZ journal …` (Schritt E) |
| `docs/ERGEBNIS_TB-161_sb1_datenlauf.md` | Schreibwerkzeug von Claude Code (Schritt E) |
| `docs/belege/TB-161/e_backlog_probe.txt` | Befehl in Schritt E |
| `docs/belege/TB-161/e_backlog.txt` | Befehl in Schritt E |
| `docs/belege/TB-161/e_kennung.txt` | Befehl in Schritt E |
| `docs/belege/TB-161/e_block.md` | Schreibwerkzeug von Claude Code, Gliederung Anhang C |
| `docs/belege/TB-161/e_journal_probe.txt` | Befehl in Schritt E |
| `docs/belege/TB-161/e_journal.txt` | Befehl in Schritt E |
| `docs/belege/TB-161/f_porcelain.txt` | `git status --porcelain > "$TMPDIR/tb161_f.txt"`, dann `cp` (Abgabe) |
| `docs/belege/TB-161/f_numstat.txt` | `git diff --numstat ⟨S0⟩ ⟨F⟩ > …` (Abgabe) |
| `docs/belege/TB-161/abbruch.txt` | nur bei Abbruch: `printf '%s\n' "…" > …` (Abbruchweg) |
| `research/etf_trendfolge/daten/*` | nur `datenlauf.py` (Schritt 4) — gitignoriert, nie `git add` |
| $TMPDIR/tb161_0a.txt, $TMPDIR/tb161_werkzeug.py, $TMPDIR/tb161_db/, $TMPDIR/tb161_f.txt | Befehle in 0a, 0c und Abgabe; bleiben liegen — nicht löschen, nicht committen |

## Anhang B — Werkzeug

### Werkzeug

```python
# TB-161 Werkzeug (Anhang B des Auftrags): manifest, kennung, backlog, journal. Nur Standardbibliothek, Python 3.9.
# Liest nur; schreibt allein mit `backlog` (BACKLOG.md) und `journal` (JOURNAL.md), jeweils erst nach bestandener Probe; ein Anker muss genau einmal vorkommen, sonst wird nichts geschrieben.
import hashlib, json, os, re, sys
DATEN = "research/etf_trendfolge/daten"
BL = "docs/projektfuehrung/BACKLOG.md"
R4_ANFANG, R4_ALT, R4_NEU = '| **4** | **`S-B1` Multi-Asset-ETF-Trend** ', "| vorbereiten |", '| vorbereiten · Datenlauf TB-161: `docs/ERGEBNIS_TB-161_sb1_datenlauf.md`; UCITS-Paare (Register S-B1 10a) offen |'
K15_ANFANG, K15_NEU = "| **K15** | ", '**Vermerk TB-161: durch TB-41 erledigt, Paare offen** (Register `docs/VORREGISTRIERUNG_neuselektion.md` 16.9 (b), Commit `1bc2d57`; Proxy-Tabelle Register S-B1 10a.4 leer). '
JO, JO_ANKER = "docs/projektfuehrung/JOURNAL.md", "## Wiederkehrende Lehren"


def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def schreib(p, t):
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)


def manifest(aus):
    p = os.path.join(DATEN, "manifest.json")
    if not os.path.isfile(p):
        print("NEIN: %s fehlt" % p)
        return 3
    roh = open(p, "rb").read()
    m = json.loads(roh.decode("utf-8"))
    csv = sorted(x for x in os.listdir(DATEN) if x.endswith(".csv"))
    z = ["manifest.json · %d B · sha256 %s · erzeugt %s · auto_adjust %s · intervall %s" % (
        len(roh), hashlib.sha256(roh).hexdigest(), m.get("erzeugt"), m.get("auto_adjust"), m.get("intervall")),
         "Kursdateien (*.csv) in %s: %d · Eintraege im Manifest: %d · davon vorhanden: %d" % (
        DATEN, len(csv), len(m["dateien"]), sum(1 for e in m["dateien"] if e.get("vorhanden")))]
    for e in m["dateien"]:
        if not e.get("vorhanden"):
            z.append("%-5s FEHLT" % e["symbol"])
        else:
            z.append("%-5s %s bis %s · %d B · sha256 %s" % (e["symbol"], e["erstes_datum"], e["letztes_datum"], e["groesse"], e["sha256"]))
    schreib(aus, "\n".join(z) + "\n")
    print("\n".join(z))
    return 0


def backlog(probe):
    z = lies(BL).split("\n")
    r4 = [i for i, l in enumerate(z) if l.startswith(R4_ANFANG)]
    k15 = [i for i, l in enumerate(z) if l.startswith(K15_ANFANG)]
    c = [("Rang-4-Zeile genau einmal", len(r4) == 1),
         ("Rang-4-Zeile endet auf '%s'" % R4_ALT, len(r4) == 1 and z[r4[0]].endswith(R4_ALT)),
         ("K15-Zeile genau einmal", len(k15) == 1),
         ("Vermerke noch nicht da", R4_NEU not in "\n".join(z) and K15_NEU not in "\n".join(z))]
    for n, g in c:
        print("%s: %s" % (n, "ja" if g else "nein"))
    if not all(g for _, g in c):
        print("NEIN - nichts geschrieben")
        return 3
    if not probe:
        i, k = r4[0], k15[0]
        z[i] = z[i][:-len(R4_ALT)] + R4_NEU
        z[k] = K15_ANFANG + K15_NEU + z[k][len(K15_ANFANG):]
        schreib(BL, "\n".join(z))
    print("%s: Rang 4 Z. %d, K15 Z. %d" % ("probe" if probe else "geschrieben", r4[0] + 1, k15[0] + 1))
    return 0


def naechste():
    m = max(re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M))
    return m, (m[0] + chr(ord(m[1]) + 1)) if m[1] != "Z" else chr(ord(m[0]) + 1) + "A"


def kennung(aus):
    letzte, nx = naechste()
    t = "Kennung %s (naechste freie; hoechste vorhandene %s)" % (nx, letzte)
    schreib(aus, t + "\n")
    print(t)
    return 0


def journal(block, probe):
    b, t = lies(block).rstrip("\n").split("\n"), lies(JO)
    z, k = t.split("\n"), re.findall(r"^## ([A-Z]{2}) — TB-", t, re.M)
    letzte, KENNUNG = naechste()
    i = z.index(JO_ANKER) if z.count(JO_ANKER) == 1 else -1
    c = [("Block beginnt mit '## %s — TB-161: ' (naechste freie nach %s)" % (KENNUNG, letzte), b[0].startswith("## %s — TB-161: " % KENNUNG)),
         ("keine weitere '## '-Zeile im Block", sum(l.startswith("## ") for l in b) == 1),
         ("kein '---' im Block", "---" not in b),
         ("Kennung %s noch frei" % KENNUNG, KENNUNG not in k),
         ("Anker einmal", i >= 0),
         ("vor dem Anker '---' und Leerzeile", i >= 2 and z[i - 1] == "" and z[i - 2] == "---")]
    for n, g in c:
        print("%s: %s" % (n, "ja" if g else "nein"))
    if not all(g for _, g in c):
        print("NEIN - nichts geschrieben")
        return 64
    if not probe:
        z[i - 1:i - 1] = [""] + b + ["", "---"]
        schreib(JO, "\n".join(z))
    print("%s: Kennung %s, %d Zeilen Block" % ("probe" if probe else "eingefuegt", KENNUNG, len(b)))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "manifest":
        sys.exit(manifest(a[1]))
    if len(a) == 2 and a[0] == "kennung":
        sys.exit(kennung(a[1]))
    if a in (["backlog"], ["backlog", "--probe"]):
        sys.exit(backlog(len(a) == 2))
    if len(a) in (2, 3) and a[0] == "journal" and a[2:] in ([], ["--probe"]):
        sys.exit(journal(a[1], len(a) == 3))
    print("Aufruf: manifest <beleg> | kennung <beleg> | backlog [--probe] | journal <block> [--probe]")
    sys.exit(2)
```

## Anhang C — Gliederung des Journalblocks

Erste Zeile `## <Kennung> — TB-161: S-B1-Datenlauf, Historie <erfuellt|nicht erfuellt> (historie.py rc <n>)`; dann eine Zeile *Quelle: `docs/ERGEBNIS_TB-161_sb1_datenlauf.md`, Commits ⟨S0⟩, ⟨M⟩, ⟨F⟩ = der Commit „TB-161 Abgabe: Ergebnis, Backlog, Journal <Kennung>“*; `**Quelle:**` (was die Sitzung tat, eigene Worte); `### Was gemessen ist` (Datenstand vorher/nachher, Selbsttest vorher/nachher, 14 Symbole mit erstem Datum, Untergrenze, rc, tragende Falten); `### Was offen bleibt` (mindestens: UCITS-Paare, Backtest erst nach Rang 1); `### In einfacher Sprache`. Keine weitere `## `-Zeile, kein `---`.
